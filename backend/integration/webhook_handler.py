import collections
import json
import logging
import six
import hashlib
import hmac

from django.core.exceptions import SuspiciousOperation
from django.core.handlers.wsgi import WSGIRequest

from integration.constants import GITHUB_EVENT_DESCRIPTIONS

GITHUB_EVENT_DESCRIPTION = 'gh-event-description'


class WebhookHandler:

    X_GITHUB_DELIVERY = "X-Github-Delivery"
    X_HUB_SIGNATURE_256 = "X-Hub-Signature-256"
    X_GITHUB_EVENT = "X-Github-Event"

    def __init__(self, secret=None):
        self.secret = secret
        if secret is not None:
            self.secret = secret
        self.__hooks = collections.defaultdict(list)
        self.__logger = logging.getLogger(name="webhook_handler")
        self.__logger.setLevel(logging.INFO)

    @property
    def secret(self):
        return self.__secret

    @secret.setter
    def secret(self, secret):
        if secret is not None and not isinstance(secret, six.binary_type):
            secret = secret.encode("utf-8")
        self.__secret = secret

    def hook(self, event_type="push"):
        def decorator(func):
            self.__hooks[event_type].append(func)
            return func
        return decorator

    @staticmethod
    def _get_header(key: str, request: WSGIRequest) -> str:
        try:
            return request.headers[key]
        except KeyError:
            raise SuspiciousOperation(f'Missing header: {key}')

    def _get_digest(self, request: WSGIRequest) -> hmac.HMAC:
        return hmac.new(self.__secret, request.body, hashlib.sha256).hexdigest() if self.__secret else None

    def handle(self, request: WSGIRequest):
        digest = self._get_digest(request)
        if digest is not None:
            if not isinstance(digest, six.text_type):
                digest = six.text_type(digest)

            signature_parts = self._get_header(WebhookHandler.X_HUB_SIGNATURE_256, request).split("=", 1)
            if len(signature_parts) < 2:
                raise SuspiciousOperation("Signature required.")

            signature_algorithm, signature_hash = signature_parts[0], signature_parts[1]
            if signature_algorithm != hashlib.sha256 or not hmac.compare_digest(signature_hash, digest):
                raise SuspiciousOperation("Invalid signature.")

        event_type = self._get_header(WebhookHandler.X_GITHUB_EVENT, request)
        content_type = self._get_header("content-type", request)

        request_data = None
        if content_type == "application/x-www-form-urlencoded":
            raise SuspiciousOperation("Unsupported operation.")
            # json.loads(request.form.to_dict(flat=True)["payload"])
        elif content_type == "application/json":
            try:
                request_data = json.loads(request.body.decode("utf-8"))
            except Exception:
                raise SuspiciousOperation("Request body must contain valid JSON data.")

        event_description = _format_event(event_type, request_data)
        print(f'{WebhookHandler.X_GITHUB_DELIVERY}: {self._get_header(WebhookHandler.X_GITHUB_DELIVERY, request)} | ',
              f'{event_description}')
        self.__logger.debug(
            f'{WebhookHandler.X_GITHUB_DELIVERY}: {self._get_header(WebhookHandler.X_GITHUB_DELIVERY, request)} | ',
            f'{event_description}')

        request_data[GITHUB_EVENT_DESCRIPTION] = event_description
        for handler in self.__hooks.get(event_type, []):
            handler(request_data)


def _format_event(event_type: str, data: dict) -> str:
    try:
        return GITHUB_EVENT_DESCRIPTIONS[event_type].format(**data)
    except KeyError:
        return event_type
