import asyncio
import re

import httpx as httpx
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from branch.models import Branch
from change.models import CloseCommitReference, CommitReference, UPDATE
from commit.models import Commit, CommitMetaData
from integration.constants import *
from integration.webhook_handler import WebhookHandler, GITHUB_EVENT_DESCRIPTION
from project.models import Project
from repository.models import Repository
from task.models import Task, CLOSED, OPEN

webhook_handler = WebhookHandler()


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook_request(request):
    webhook_handler.handle(request)
    return HttpResponse("", status=204)


@webhook_handler.hook(event_type="create")
def handle_github_branch_created_event(data, *args, **kwargs):
    if data['ref_type'] == 'branch':
        repository_url = data['repository']['html_url']
        repository = Repository.objects.filter(url=repository_url).first()
        if repository:
            branch_name = data['ref']
            Branch.objects.create(repository=repository, name=branch_name)


@webhook_handler.hook(event_type="delete")
def handle_github_branch_deleted_event(data, *args, **kwargs):
    if data['ref_type'] == 'branch':
        repository_url = data['repository']['html_url']
        branch_to_delete = Branch.objects.filter(repository__url=repository_url, name=data['ref']).first()
        if branch_to_delete:
            branch_to_delete.delete()


@webhook_handler.hook(event_type="push")
def handle_github_push_event(data, *args, **kwargs):

    event_description = data[GITHUB_EVENT_DESCRIPTION]
    repository_data = data[REPOSITORY]
    commits_data = data[COMMITS]
    sha_of_previous_commit = data[COMMIT_BEFORE]

    project = get_project(repository_data[HTML_URL])
    branch = get_branch(project.repository.id, data[COMMIT_REF])

    is_repository_private = repository_data[PRIVATE]
    compare_url_template = repository_data[COMPARE_URL]
    handle_diff_func = handle_private_diff if is_repository_private else handle_public_diff

    for commit_data in commits_data:
        commit = handle_commit(commit_data, branch, sha_of_previous_commit, compare_url_template, handle_diff_func)
        reference_changes = handle_task_references(commit, project, event_description)
        closing_changes = handle_closing_task_references(commit, project, event_description)

        # TODO: Logging?

        sha_of_previous_commit = commit_data[COMMIT_ID]


def get_project(repository_url: str) -> Project:
    projects = Project.objects.filter(repository__url=repository_url)
    if not projects:
        raise SuspiciousOperation(f'Project with repository URL "{repository_url}" not found.')

    return projects.first()


def get_branch(repository_id, git_ref: str) -> Branch:
    branch_name = re.sub('refs/heads/', '', git_ref)
    branches = Branch.objects.filter(repository_id=repository_id, name=branch_name)     # TODO: If required, find the last commit on the branch and verify
    if not branches:
        raise SuspiciousOperation(f'Branch "{branch_name}" not found.')

    return branches.first()


def handle_commit(commit_data: dict, branch: Branch, sha_of_previous_commit: str,
                  compare_url_template: str, diff_handler_func: callable):

    commit_id = commit_data[COMMIT_ID]
    commit_url = commit_data[COMMIT_URL]
    commit_message = commit_data[COMMIT_MESSAGE]
    commit_title, commit_description = extract_commit_message(commit_message)
    timestamp = commit_data[COMMIT_TIMESTAMP]

    author_data = commit_data[COMMIT_AUTHOR]
    author_name = author_data[COMMIT_AUTHOR_NAME]
    author_email = author_data[COMMIT_AUTHOR_EMAIL]

    existing_users = User.objects.filter(email=author_email)
    author = existing_users.first()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(diff_handler_func(commit_data, sha_of_previous_commit, compare_url_template))
    task_results, _ = loop.run_until_complete(asyncio.wait([task]))
    commit_meta_data = task_results.pop().result()

    return Commit.objects.create(
        author_username=author_name,
        hash_id=commit_id,
        message=commit_title,
        description=commit_description,
        url=commit_url,
        timestamp=timestamp,
        branch=branch,
        commit_meta_data=commit_meta_data,
        author=author)


async def handle_public_diff(commit_data: dict, sha_of_previous_commit: str, compare_url_template: str) -> CommitMetaData:
    compare_url = re.sub('{base}', sha_of_previous_commit, compare_url_template)
    compare_url = re.sub('{head}', commit_data[COMMIT_ID], compare_url)

    diff_files = []
    try:
        async with httpx.AsyncClient() as client:
            diff_response = await asyncio.gather(client.get(compare_url))
            if diff_response[0].status_code == httpx.codes.OK:
                diff_data = diff_response[0].json()
                diff_files = diff_data[FILES]
    except httpx.RequestError as e:
        print(f'An error occurred while requesting diff on URL {e.request.url!r}.')

    added_lines_count, deleted_lines_count, modified_lines_count = 0, 0, 0
    for file in diff_files:
        added_lines_count += file[ADDITIONS]
        deleted_lines_count += file[DELETIONS]
        modified_lines_count += file[CHANGES]

    return await sync_to_async(CommitMetaData.objects.create)(
        file_additions_count=len(commit_data[ADDED]),
        file_deletions_count=len(commit_data[REMOVED]),
        file_modifications_count=len(commit_data[MODIFIED]),
        line_additions_count=added_lines_count,
        line_deletions_count=deleted_lines_count,
        line_modifications_count=modified_lines_count
    )


async def handle_private_diff(commit_data: dict, *args, **kwargs) -> CommitMetaData:
    return await sync_to_async(CommitMetaData.objects.create)(
        file_additions_count=len(commit_data[ADDED]),
        file_deletions_count=len(commit_data[REMOVED]),
        file_modifications_count=len(commit_data[MODIFIED])
    )


def extract_commit_message(commit_message):
    tokens = commit_message.split(BLANK_LINE)
    try:
        return tokens[0], tokens[1]
    except IndexError:
        return tokens[0], ""


def handle_closing_task_references(commit: Commit, project: Project, event_description: str):
    closing_task_references = re.findall('closes #(.+?)', commit.message)
    if not closing_task_references:
        return list()

    tasks_to_close = Task.objects.filter(project=project, id__in=closing_task_references, state__in=[OPEN])
    if not tasks_to_close:
        return list()

    created_changes = [CloseCommitReference.objects.create(
        change_type=UPDATE, description=event_description, task=task, referenced_commit=commit) for task in tasks_to_close]
    tasks_to_close.update(state=CLOSED)

    return created_changes


def handle_task_references(commit: Commit, project: Project, event_description: str):
    task_references = re.findall('w*(?<!closes )#(.+?)', commit.message)
    if not task_references:
        return list()

    referenced_tasks = Task.objects.filter(project=project, id__in=task_references)
    if not referenced_tasks:
        return list()

    return [CommitReference.objects.create(
        change_type=UPDATE, description=event_description, task=task, referenced_commit=commit) for task in referenced_tasks]
