"""WhatsApp Cloud API webhook.

GET  — Meta's one-time verification handshake when the webhook URL is registered.
POST — incoming messages and delivery-status updates.

For now POST only stores inbound text so the connection can be tested end to
end. Lead matching, the AI reply and scoring are the next build steps.
TODO before production: verify Meta's X-Hub-Signature-256 header with the app secret.
"""

import json
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from leads.models import Inquiry, Lead, LeadEvent

from .models import Channel, Conversation, Message

logger = logging.getLogger(__name__)


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        return _verify_subscription(request)
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("invalid JSON")
        _handle_payload(payload)
        # Always 200 quickly, or Meta retries the delivery.
        return HttpResponse("ok")
    return HttpResponse(status=405)


def _verify_subscription(request):
    token = settings.WHATSAPP_VERIFY_TOKEN
    if (
        token
        and request.GET.get("hub.mode") == "subscribe"
        and request.GET.get("hub.verify_token") == token
    ):
        return HttpResponse(request.GET.get("hub.challenge", ""))
    return HttpResponseForbidden("verification failed")


def _handle_payload(payload):
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            phone_id = value.get("metadata", {}).get("phone_number_id")
            channel = Channel.objects.filter(provider_phone_id=phone_id).first()
            if channel is None:
                logger.warning("Webhook for unknown phone_number_id %s", phone_id)
                continue
            names = {c.get("wa_id"): c.get("profile", {}).get("name", "") for c in value.get("contacts", [])}
            for msg in value.get("messages", []):
                _store_inbound(channel, msg, names.get(msg.get("from"), ""))


def _store_inbound(channel, msg, profile_name):
    phone = "+" + msg["from"].lstrip("+")
    lead, created = Lead.objects.get_or_create(
        organization=channel.organization, phone=phone, defaults={"name": profile_name}
    )
    if created:
        LeadEvent.objects.create(lead=lead, kind=LeadEvent.Kind.CREATED)
        Inquiry.objects.create(lead=lead, source=Inquiry.Source.WHATSAPP_DIRECT, raw_payload=msg)

    conversation, _ = Conversation.objects.get_or_create(lead=lead, channel=channel)
    # Idempotent: Meta can deliver the same webhook more than once.
    if Message.objects.filter(provider_message_id=msg.get("id", "")).exists():
        return
    Message.objects.create(
        conversation=conversation,
        direction=Message.Direction.INBOUND,
        sender=Message.Sender.LEAD,
        text=msg.get("text", {}).get("body", ""),
        status=Message.Status.RECEIVED,
        provider_message_id=msg.get("id", ""),
    )
