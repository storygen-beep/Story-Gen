import json

from django.test import TestCase, override_settings

from accounts.models import Organization
from leads.models import Lead

from .models import Channel, Message


def inbound_payload(phone_id="PHONE123", msg_id="wamid.1", text="Hi, is the Marina 2BR available?"):
    return {
        "entry": [{
            "changes": [{
                "value": {
                    "metadata": {"phone_number_id": phone_id},
                    "contacts": [{"wa_id": "971501112233", "profile": {"name": "Mark"}}],
                    "messages": [{"from": "971501112233", "id": msg_id, "type": "text", "text": {"body": text}}],
                }
            }]
        }]
    }


@override_settings(WHATSAPP_VERIFY_TOKEN="secret")
class WhatsAppWebhookTests(TestCase):
    def setUp(self):
        org = Organization.objects.create(name="Test Properties")
        self.channel = Channel.objects.create(
            organization=org, phone_number="+97140000000", provider_phone_id="PHONE123"
        )

    def post(self, payload):
        return self.client.post("/webhooks/whatsapp/", json.dumps(payload), content_type="application/json")

    def test_verification_handshake(self):
        ok = self.client.get("/webhooks/whatsapp/", {"hub.mode": "subscribe", "hub.verify_token": "secret", "hub.challenge": "42"})
        self.assertEqual(ok.content, b"42")
        bad = self.client.get("/webhooks/whatsapp/", {"hub.mode": "subscribe", "hub.verify_token": "wrong", "hub.challenge": "42"})
        self.assertEqual(bad.status_code, 403)

    def test_inbound_message_creates_lead_and_message(self):
        self.assertEqual(self.post(inbound_payload()).status_code, 200)
        lead = Lead.objects.get()
        self.assertEqual((lead.phone, lead.name), ("+971501112233", "Mark"))
        self.assertEqual(Message.objects.get().text, "Hi, is the Marina 2BR available?")

    def test_duplicate_delivery_is_ignored(self):
        self.post(inbound_payload())
        self.post(inbound_payload())
        self.assertEqual(Message.objects.count(), 1)

    def test_second_message_reuses_lead(self):
        self.post(inbound_payload(msg_id="wamid.1"))
        self.post(inbound_payload(msg_id="wamid.2", text="Cash buyer"))
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 2)

    def test_unknown_number_is_ignored(self):
        self.assertEqual(self.post(inbound_payload(phone_id="OTHER")).status_code, 200)
        self.assertFalse(Lead.objects.exists())
