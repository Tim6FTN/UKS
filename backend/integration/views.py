import re
import requests

from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from branch.models import Branch
from commit.models import Commit, CommitMetaData
from integration.constants import *
from integration.webhook_handler import WebhookHandler
from project.models import Project

webhook_handler = WebhookHandler()


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook_request(request):
    webhook_handler.handle(request)
    return HttpResponse("", status=204)


@webhook_handler.hook(event_type="push")
def handle_github_push_event(data, *args, **kwargs):

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
        print(f'Handled commit {commit.id} | {commit.message}')
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

    commit_meta_data = diff_handler_func(commit_data, sha_of_previous_commit, compare_url_template)

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


def handle_public_diff(commit_data: dict, sha_of_previous_commit: str, compare_url_template: str) -> CommitMetaData:
    compare_url = re.sub('{base}', sha_of_previous_commit, compare_url_template)
    compare_url = re.sub('{head}', commit_data[COMMIT_ID], compare_url)

    diff_response = requests.get(url=compare_url)       # TODO: Add handling of unsuccessful request. Async.
    diff_data = diff_response.json()
    diff_files = diff_data[FILES]

    added_lines_count, deleted_lines_count, modified_lines_count = 0, 0, 0
    for file in diff_files:
        added_lines_count += file[ADDITIONS]
        deleted_lines_count += file[DELETIONS]
        modified_lines_count += file[CHANGES]

    return CommitMetaData.objects.create(
        file_additions_count=len(commit_data[ADDED]),
        file_deletions_count=len(commit_data[REMOVED]),
        file_modifications_count=len(commit_data[MODIFIED]),
        line_additions_count=added_lines_count,
        line_deletions_count=deleted_lines_count,
        line_modifications_count=modified_lines_count
    )


def handle_private_diff(commit_data: dict, sha_of_previous_commit: str, compare_url_template: str) -> CommitMetaData:
    return CommitMetaData.objects.create(
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
