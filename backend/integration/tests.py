from unittest.mock import MagicMock, Mock

from django.core.exceptions import SuspiciousOperation
from django.test import TestCase, SimpleTestCase

from integration.constants import GITHUB_EVENT_DESCRIPTIONS
from integration.webhook_handler import WebhookHandler, _format_event


class TestWebhookHandler(SimpleTestCase):

    def test_if_secret_not_initialized(self):
        self.webhook_handler = WebhookHandler()
        self.assertIsNone(self.webhook_handler.secret)

    def test_if_secret_properly_initialized(self):
        self.webhook_handler = WebhookHandler(secret="test-secret")

        self.assertIsNotNone(self.webhook_handler.secret)
        self.assertIsInstance(self.webhook_handler.secret, bytes)
        self.assertEqual(self.webhook_handler.secret, "test-secret".encode("utf-8"))

    def test_format_event_if_key_is_present(self):
        data = {'pusher': {'name': 'test_name'}, 'ref': 'test_ref', 'repository': {'full_name': 'test_repository_full_name'}}
        push_event_description = _format_event("push", data)
        self.assertEqual(push_event_description, "test_name pushed test_ref in test_repository_full_name")

    def test_format_event_if_key_is_not_present(self):
        push_event_description = _format_event("non-existing-key", {})
        self.assertEqual(push_event_description, "non-existing-key")

    def test__get_header_if_key_is_present(self):
        request = Mock()
        request.headers = {'X-Github-Delivery': 'some-guid'}
        header_value = WebhookHandler._get_header('X-Github-Delivery', request)
        self.assertEqual(header_value, 'some-guid')

    def test__get_header_if_key_is_not_present(self):
        with self.assertRaisesMessage(SuspiciousOperation, 'Missing header: X-Github-Delivery'):
            request = Mock()
            request.headers = {}
            WebhookHandler._get_header('X-Github-Delivery', request)

    # _get_digest if secret present?

    def test__get_digest_if_secret_is_not_present(self):
        self.webhook_handler = WebhookHandler()
        request = Mock()
        request.body = {}
        digest = self.webhook_handler._get_digest(request)
        self.assertIsNone(digest)

    def test_handle_if_no_signature(self):
        request = Mock()
        request.headers = {WebhookHandler.X_HUB_SIGNATURE_256: 'incorrect-digest'}
        self.webhook_handler = WebhookHandler()
        self.webhook_handler._get_digest = MagicMock(return_value="sha256-digest")

        with self.assertRaisesMessage(SuspiciousOperation, "Signature required."):
            self.webhook_handler.handle(request)

    def test_handle_if_signature_invalid(self):
        request = Mock()
        request.headers = {WebhookHandler.X_HUB_SIGNATURE_256: 'sha256=incorrect-digest'}
        self.webhook_handler = WebhookHandler()
        self.webhook_handler._get_digest = MagicMock(return_value="sha256-digest")

        with self.assertRaisesMessage(SuspiciousOperation, "Invalid signature."):
            self.webhook_handler.handle(request)

    def test_handle_when_content_type_form(self):
        self.webhook_handler = WebhookHandler()
        self.webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {'content-type': 'application/x-www-form-urlencoded', WebhookHandler.X_GITHUB_EVENT: 'push'}

        with self.assertRaisesMessage(SuspiciousOperation, "Unsupported operation."):
            self.webhook_handler.handle(request)

    def test_handle_when_content_type_json_and_data_valid(self):
        self.webhook_handler = WebhookHandler()
        self.webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {'content-type': 'application/json', 'X-Github-Delivery': 'some-guid', WebhookHandler.X_GITHUB_EVENT: 'push'}
        request.body = '{"key": "value"}'.encode('utf-8')

        self.webhook_handler.handle(request)
        # check if all webhooks for event type were called

    def test_handle_when_content_type_json_and_data_invalid(self):
        self.webhook_handler = WebhookHandler()
        self.webhook_handler._get_digest = MagicMock(return_value=None)
        request = Mock()
        request.headers = {'content-type': 'application/json', 'X-Github-Delivery': 'some-guid', WebhookHandler.X_GITHUB_EVENT: 'push'}
        request.body = ''.encode('utf-8')
        with self.assertRaisesMessage(SuspiciousOperation, "Request body must contain valid JSON data."):
            self.webhook_handler.handle(request)

    def test_if_webhook_handler_handle_called(self):
        self.webhook_handler = WebhookHandler()
        self.webhook_handler.handle = MagicMock(return_value=None)
        self.webhook_handler.handle(request=None)

        self.webhook_handler.handle.assert_called_once_with(request=None)

    def test_should_not(self):
        self.webhook_handler = WebhookHandler()

        @self.webhook_handler.hook(event_type="push")
        def handle_github_push_event(data, *args, **kwargs):
            pass

        mock_request = {'headers': {}}
        mock_request['headers'][WebhookHandler.X_GITHUB_EVENT] = "ping"
        mock_request['headers']["content-type"] = "application/json"
        self.webhook_handler.handle = MagicMock(return_value=None)
        self.webhook_handler.handle(request=mock_request)

        # handle_github_push_event.assert_not_called()

