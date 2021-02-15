from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from branch.models import Branch
from commit.models import Commit, CommitMetaData
from integration.webhook_handler import WebhookHandler
from project.models import Project

webhook_handler = WebhookHandler()


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook_request(request):
    webhook_handler.handle(request)
    return HttpResponse("", status=204)


BLANK_LINE = "\n\n"

COMMITS = "commits"
REPOSITORY = "repository"
HTML_URL = "html_url"

COMMIT_ID = "id"
COMMIT_URL = "url"
COMMIT_MESSAGE = "message"
COMMIT_TIMESTAMP = "timestamp"
COMMIT_AUTHOR = "author"
COMMIT_AUTHOR_NAME = "name"
COMMIT_AUTHOR_EMAIL = "email"

@webhook_handler.hook(event_type="push")
def handle_github_push_event(data, *args, **kwargs):

    repository_data = data[REPOSITORY]
    repository_url = repository_data[HTML_URL]
    projects = Project.objects.filter(repository__url=repository_url)

    if not projects:
        raise SuspiciousOperation(f'Project with repository URL "{repository_url}" not found.')

    # TODO: Fix this - refs/heads/<branch_name>
    branch_name = 'main'
    branches = Branch.objects.filter(repository__project=projects.first(), name=branch_name)
    if not branches:
        raise SuspiciousOperation(f'Branch {None} not found.')

    commits_data = data[COMMITS]
    for commit_data in commits_data:
        commit = handle_commit(commit_data, branches.first())
        print(f'Handled commit {commit.id} | {commit.message}')


def handle_commit(commit_data, branch: Branch):

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

    # TODO: Parse insights data from request
    commit_meta_data = CommitMetaData.objects.create()

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


def extract_commit_message(commit_message):
    tokens = commit_message.split(BLANK_LINE)
    try:
        return tokens[0], tokens[1]
    except IndexError:
        return tokens[0], ""
