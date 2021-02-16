from unittest.mock import MagicMock, Mock

import six
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.test import SimpleTestCase, Client, TransactionTestCase
from django.urls import reverse, resolve

from branch.models import Branch
from integration.views import receive_webhook_request
from integration.webhook_handler import WebhookHandler, _format_event
from project.models import Project
from repository.models import Repository


class TestWebhookHandler(SimpleTestCase):

    def test_if_secret_not_initialized(self):
        webhook_handler = WebhookHandler()

        self.assertIsNone(webhook_handler.secret)

    def test_if_secret_properly_initialized(self):
        webhook_handler = WebhookHandler(secret="test-secret")

        self.assertIsNotNone(webhook_handler.secret)
        self.assertIsInstance(webhook_handler.secret, bytes)
        self.assertEqual(webhook_handler.secret, "test-secret".encode("utf-8"))

    def test_format_event_if_key_is_present(self):
        data = {'pusher': {'name': 'test_name'}, 'ref': 'test_ref',
                'repository': {'full_name': 'test_repository_full_name'}}
        push_event_description = _format_event("push", data)

        self.assertEqual(push_event_description, "test_name pushed test_ref in test_repository_full_name")

    def test_format_event_if_key_is_not_present(self):
        push_event_description = _format_event("non-existing-key", {})

        self.assertEqual(push_event_description, "non-existing-key")

    def test__get_header_if_key_is_present(self):
        request = Mock()
        request.headers = {WebhookHandler.X_GITHUB_DELIVERY: 'some-guid'}
        header_value = WebhookHandler._get_header(WebhookHandler.X_GITHUB_DELIVERY, request)

        self.assertEqual(header_value, 'some-guid')

    def test__get_header_if_key_is_not_present(self):
        with self.assertRaisesMessage(SuspiciousOperation, f'Missing header: {WebhookHandler.X_GITHUB_DELIVERY}'):
            request = Mock()
            request.headers = {}
            WebhookHandler._get_header(WebhookHandler.X_GITHUB_DELIVERY, request)

    def test__get_digest_if_secret_is_present(self):
        request = Mock()
        request.body = '{"key": "value"}'.encode('utf-8')
        webhook_handler = WebhookHandler(secret="test-secret")
        digest = webhook_handler._get_digest(request)

        self.assertIsNotNone(digest)
        self.assertIsInstance(digest, six.text_type)

    def test__get_digest_if_secret_is_not_present(self):
        request = Mock()
        request.body = {}
        webhook_handler = WebhookHandler()
        digest = webhook_handler._get_digest(request)

        self.assertIsNone(digest)

    def test_handle_if_no_signature(self):
        request = Mock()
        request.headers = {WebhookHandler.X_HUB_SIGNATURE_256: 'incorrect-digest'}
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value="sha256-digest")

        with self.assertRaisesMessage(SuspiciousOperation, "Signature required."):
            webhook_handler.handle(request)

    def test_handle_if_signature_invalid(self):
        request = Mock()
        request.headers = {WebhookHandler.X_HUB_SIGNATURE_256: 'sha256=incorrect-digest'}
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value="sha256-digest")

        with self.assertRaisesMessage(SuspiciousOperation, "Invalid signature."):
            webhook_handler.handle(request)

    def test_handle_if_event_type_missing(self):
        request = Mock()
        request.headers = {}
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value=None)

        with self.assertRaisesMessage(SuspiciousOperation, f'Missing header: {WebhookHandler.X_GITHUB_EVENT}'):
            webhook_handler.handle(request)

    def test_handle_when_content_type_form(self):
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {'content-type': 'application/x-www-form-urlencoded', WebhookHandler.X_GITHUB_EVENT: 'push'}

        with self.assertRaisesMessage(SuspiciousOperation, "Unsupported operation."):
            webhook_handler.handle(request)

    def test_handle_when_content_type_json_and_data_invalid(self):
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {
            'content-type': 'application/json',
            'X-Github-Delivery': 'some-guid',
            WebhookHandler.X_GITHUB_EVENT: 'push'
        }
        request.body = ''.encode('utf-8')
        with self.assertRaisesMessage(SuspiciousOperation, "Request body must contain valid JSON data."):
            webhook_handler.handle(request)

    def test_handle_when_content_type_json_and_data_valid(self):
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {
            'content-type': 'application/json',
            'X-Github-Delivery': 'some-guid',
            WebhookHandler.X_GITHUB_EVENT: 'push'
        }
        request.body = '{"key": "value"}'.encode('utf-8')

        webhook_handler.handle(request)

    def test_if_webhook_handler_handle_called(self):
        webhook_handler = WebhookHandler()
        webhook_handler.handle = MagicMock(return_value=None)
        webhook_handler.handle(request=Mock())

        webhook_handler.handle.assert_called_once()

    def test_if_webhook_handler_called_all_registered_hook_handlers(self):
        webhook_handler = WebhookHandler()
        webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {
            'content-type': 'application/json',
            'X-Github-Delivery': 'some-guid',
            WebhookHandler.X_GITHUB_EVENT: 'push'
        }
        request.body = '{"key": "value"}'.encode('utf-8')

        @webhook_handler.hook(event_type="push")
        @MagicMock
        def first_decorated_func(): pass

        @webhook_handler.hook(event_type="push")
        @MagicMock
        def second_decorated_func(): pass

        @webhook_handler.hook(event_type="ping")
        @MagicMock
        def third_decorated_func(): pass

        webhook_handler.handle(request)

        first_decorated_func.assert_called_once()
        second_decorated_func.assert_called_once()
        third_decorated_func.assert_not_called()


class TestIntegrationURLs(SimpleTestCase):

    def test_notify_url(self):
        notify_url = reverse('notify')

        self.assertEquals(resolve(notify_url).func, receive_webhook_request)


class TestIntegrationViews(TransactionTestCase):

    def setUp(self):
        self.client = Client()
        self.notify_url = reverse('notify')

        self.user = User.objects.create_user('test_username', 'test@email.com', 'test_password')
        self.repository = Repository.objects.create(
            url="https://github.com/fivkovic/uks-demo",
            name="uks-demo",
            description="uks-demo repository description",
            is_public=True)
        self.project = Project.objects.create(
            name="UKS DEMO PROJECT",
            description="UKS demo project description",
            is_public=True,
            wiki_content="Wiki",
            repository=self.repository,
            owner=self.user)
        self.branch = Branch.objects.create(name="main", repository=self.repository)
        self.task = None

    def test_receive_webhook_request_view(self):
        headers = {
            'HTTP_' + WebhookHandler.X_GITHUB_EVENT: 'push',
            'HTTP_' + WebhookHandler.X_GITHUB_DELIVERY: 'some-guid'
        }
        response = self.client.post(
            self.notify_url,
            INTEGRATION_TEST_REQUEST_BODY,
            content_type='application/json',
            **headers)

        self.assertEquals(response.status_code, 204)


INTEGRATION_TEST_REQUEST_BODY = {
    "ref": "refs/heads/main",
    "before": "2f781a5371291ce8ba3f3a8acdf8bd673889dcaf",
    "after": "9549a348a9c4e175cf8a27e45bab93407d178767",
    "repository": {
        "id": 339193534,
        "node_id": "MDEwOlJlcG9zaXRvcnkzMzkxOTM1MzQ=",
        "name": "uks-demo",
        "full_name": "fivkovic/uks-demo",
        "private": False,
        "owner": {
            "name": "fivkovic",
            "email": "f.ivkovic16@gmail.com",
            "login": "fivkovic",
            "id": 17569172,
            "node_id": "MDQ6VXNlcjE3NTY5MTcy",
            "avatar_url": "https://avatars.githubusercontent.com/u/17569172?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/fivkovic",
            "html_url": "https://github.com/fivkovic",
            "followers_url": "https://api.github.com/users/fivkovic/followers",
            "following_url": "https://api.github.com/users/fivkovic/following{/other_user}",
            "gists_url": "https://api.github.com/users/fivkovic/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/fivkovic/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/fivkovic/subscriptions",
            "organizations_url": "https://api.github.com/users/fivkovic/orgs",
            "repos_url": "https://api.github.com/users/fivkovic/repos",
            "events_url": "https://api.github.com/users/fivkovic/events{/privacy}",
            "received_events_url": "https://api.github.com/users/fivkovic/received_events",
            "type": "User",
            "site_admin": False
        },
        "html_url": "https://github.com/fivkovic/uks-demo",
        "description": "Demo repository for testing UKS project",
        "fork": False,
        "url": "https://github.com/fivkovic/uks-demo",
        "forks_url": "https://api.github.com/repos/fivkovic/uks-demo/forks",
        "keys_url": "https://api.github.com/repos/fivkovic/uks-demo/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/fivkovic/uks-demo/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/fivkovic/uks-demo/teams",
        "hooks_url": "https://api.github.com/repos/fivkovic/uks-demo/hooks",
        "issue_events_url": "https://api.github.com/repos/fivkovic/uks-demo/issues/events{/number}",
        "events_url": "https://api.github.com/repos/fivkovic/uks-demo/events",
        "assignees_url": "https://api.github.com/repos/fivkovic/uks-demo/assignees{/user}",
        "branches_url": "https://api.github.com/repos/fivkovic/uks-demo/branches{/branch}",
        "tags_url": "https://api.github.com/repos/fivkovic/uks-demo/tags",
        "blobs_url": "https://api.github.com/repos/fivkovic/uks-demo/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/fivkovic/uks-demo/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/fivkovic/uks-demo/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/fivkovic/uks-demo/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/fivkovic/uks-demo/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/fivkovic/uks-demo/languages",
        "stargazers_url": "https://api.github.com/repos/fivkovic/uks-demo/stargazers",
        "contributors_url": "https://api.github.com/repos/fivkovic/uks-demo/contributors",
        "subscribers_url": "https://api.github.com/repos/fivkovic/uks-demo/subscribers",
        "subscription_url": "https://api.github.com/repos/fivkovic/uks-demo/subscription",
        "commits_url": "https://api.github.com/repos/fivkovic/uks-demo/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/fivkovic/uks-demo/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/fivkovic/uks-demo/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/fivkovic/uks-demo/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/fivkovic/uks-demo/contents/{+path}",
        "compare_url": "https://api.github.com/repos/fivkovic/uks-demo/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/fivkovic/uks-demo/merges",
        "archive_url": "https://api.github.com/repos/fivkovic/uks-demo/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/fivkovic/uks-demo/downloads",
        "issues_url": "https://api.github.com/repos/fivkovic/uks-demo/issues{/number}",
        "pulls_url": "https://api.github.com/repos/fivkovic/uks-demo/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/fivkovic/uks-demo/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/fivkovic/uks-demo/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/fivkovic/uks-demo/labels{/name}",
        "releases_url": "https://api.github.com/repos/fivkovic/uks-demo/releases{/id}",
        "deployments_url": "https://api.github.com/repos/fivkovic/uks-demo/deployments",
        "created_at": 1613419653,
        "updated_at": "2021-02-15T20:07:41Z",
        "pushed_at": 1613420915,
        "git_url": "git://github.com/fivkovic/uks-demo.git",
        "ssh_url": "git@github.com:fivkovic/uks-demo.git",
        "clone_url": "https://github.com/fivkovic/uks-demo.git",
        "svn_url": "https://github.com/fivkovic/uks-demo",
        "homepage": None,
        "size": 0,
        "stargazers_count": 0,
        "watchers_count": 0,
        "language": None,
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "forks_count": 0,
        "mirror_url": None,
        "archived": False,
        "disabled": False,
        "open_issues_count": 0,
        "license": {
            "key": "mit",
            "name": "MIT License",
            "spdx_id": "MIT",
            "url": "https://api.github.com/licenses/mit",
            "node_id": "MDc6TGljZW5zZTEz"
        },
        "forks": 0,
        "open_issues": 0,
        "watchers": 0,
        "default_branch": "main",
        "stargazers": 0,
        "master_branch": "main"
    },
    "pusher": {
        "name": "fivkovic",
        "email": "f.ivkovic16@gmail.com"
    },
    "sender": {
        "login": "fivkovic",
        "id": 17569172,
        "node_id": "MDQ6VXNlcjE3NTY5MTcy",
        "avatar_url": "https://avatars.githubusercontent.com/u/17569172?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/fivkovic",
        "html_url": "https://github.com/fivkovic",
        "followers_url": "https://api.github.com/users/fivkovic/followers",
        "following_url": "https://api.github.com/users/fivkovic/following{/other_user}",
        "gists_url": "https://api.github.com/users/fivkovic/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/fivkovic/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/fivkovic/subscriptions",
        "organizations_url": "https://api.github.com/users/fivkovic/orgs",
        "repos_url": "https://api.github.com/users/fivkovic/repos",
        "events_url": "https://api.github.com/users/fivkovic/events{/privacy}",
        "received_events_url": "https://api.github.com/users/fivkovic/received_events",
        "type": "User",
        "site_admin": False
    },
    "created": False,
    "deleted": False,
    "forced": False,
    "base_ref": None,
    "compare": "https://github.com/fivkovic/uks-demo/compare/2f781a537129...9549a348a9c4",
    "commits": [
        {
            "id": "9549a348a9c4e175cf8a27e45bab93407d178767",
            "tree_id": "20f7ae1a25f3c039e7d6442440672bd012c3a78d",
            "distinct": True,
            "message": "First test commit closes #1 #2",
            "timestamp": "2021-02-15T21:12:35+01:00",
            "url": "https://github.com/fivkovic/uks-demo/commit/9549a348a9c4e175cf8a27e45bab93407d178767",
            "author": {
                "name": "Filip Ivkovic",
                "email": "fivkovic@uns.ac.rs",
                "username": "fivkovic"
            },
            "committer": {
                "name": "Filip Ivkovic",
                "email": "fivkovic@uns.ac.rs",
                "username": "fivkovic"
            },
            "added": [
                "F1.txt",
                "F2.txt"
            ],
            "removed": [],
            "modified": []
        }
    ],
    "head_commit": {
        "id": "9549a348a9c4e175cf8a27e45bab93407d178767",
        "tree_id": "20f7ae1a25f3c039e7d6442440672bd012c3a78d",
        "distinct": True,
        "message": "First test commit closes #1 #2",
        "timestamp": "2021-02-15T21:12:35+01:00",
        "url": "https://github.com/fivkovic/uks-demo/commit/9549a348a9c4e175cf8a27e45bab93407d178767",
        "author": {
            "name": "Filip Ivkovic",
            "email": "fivkovic@uns.ac.rs",
            "username": "fivkovic"
        },
        "committer": {
            "name": "Filip Ivkovic",
            "email": "fivkovic@uns.ac.rs",
            "username": "fivkovic"
        },
        "added": [
            "F1.txt",
            "F2.txt"
        ],
        "removed": [],
        "modified": []
    }
}
