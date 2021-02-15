from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from integration.webhook_handler import WebhookHandler

webhook_handler = WebhookHandler()


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook_request(request):
    webhook_handler.handle(request)
    return HttpResponse("", status=204)


@webhook_handler.hook(event_type="push")
def handle_github_push_event(data, *args, **kwargs):
    print("Handled push with: {0}".format(data))
    # TODO: Implement logic
