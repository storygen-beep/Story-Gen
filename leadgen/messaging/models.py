"""WhatsApp numbers, approved templates, conversations and messages."""

from django.db import models

from accounts.models import Organization, TimeStampedModel
from leads.models import Lead
from playbooks.models import PlaybookVersion


class Channel(TimeStampedModel):
    class Provider(models.TextChoices):
        META_CLOUD = "meta_cloud", "WhatsApp Cloud API (Meta)"
        DIALOG360 = "360dialog", "360dialog"
        TWILIO = "twilio", "Twilio"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending setup"
        CONNECTED = "connected", "Connected"
        DISCONNECTED = "disconnected", "Disconnected"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="channels"
    )
    provider = models.CharField(max_length=16, choices=Provider.choices, default=Provider.META_CLOUD)
    phone_number = models.CharField(max_length=20, help_text="E.164")
    # Meta's ID for the number; incoming webhooks are routed to a channel by this.
    provider_phone_id = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.phone_number} ({self.organization})"


class MessageTemplate(TimeStampedModel):
    """WhatsApp only lets a business start a chat (or write after 24h of silence)
    with a template Meta has approved."""

    class Approval(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class Purpose(models.TextChoices):
        FIRST_REPLY = "first_reply", "First reply"
        FOLLOW_UP = "follow_up", "Follow-up"
        RE_ENGAGE = "re_engage", "Re-engage"

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="templates")
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=8, default="en")
    purpose = models.CharField(max_length=16, choices=Purpose.choices)
    body = models.TextField(help_text="Use {{1}}, {{2}} for variables, as Meta requires")
    approval = models.CharField(max_length=16, choices=Approval.choices, default=Approval.DRAFT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "name", "language"], name="unique_template_per_channel"
            )
        ]

    def __str__(self):
        return f"{self.name} [{self.language}]"


class Conversation(TimeStampedModel):
    class Mode(models.TextChoices):
        AI = "ai", "AI"
        HUMAN = "human", "Human"  # AI stays silent the moment a human types
        PAUSED = "paused", "Paused"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="conversations")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="conversations")
    mode = models.CharField(max_length=8, choices=Mode.choices, default=Mode.AI)
    # Free-form replies are allowed until this time; after it, templates only.
    service_window_ends_at = models.DateTimeField(null=True, blank=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lead", "channel"], name="one_conversation_per_lead_channel")
        ]

    def __str__(self):
        return f"{self.lead} on {self.channel.phone_number}"


class Message(models.Model):
    class Direction(models.TextChoices):
        INBOUND = "in", "Inbound"
        OUTBOUND = "out", "Outbound"

    class Sender(models.TextChoices):
        LEAD = "lead", "Lead"
        AI = "ai", "AI"
        AGENT = "agent", "Agent"
        SYSTEM = "system", "System"

    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        PENDING_APPROVAL = "pending_approval", "Waiting for approval"
        BLOCKED = "blocked", "Blocked by rules"
        QUEUED = "queued", "Queued"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        READ = "read", "Read"
        FAILED = "failed", "Failed"

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    direction = models.CharField(max_length=3, choices=Direction.choices)
    sender = models.CharField(max_length=8, choices=Sender.choices)
    text = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    # Voice notes are transcribed and then handled like text.
    transcript = models.TextField(blank=True)
    template = models.ForeignKey(MessageTemplate, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=Status.choices)
    # Why the rules checker blocked it, if it did.
    block_reason = models.CharField(max_length=300, blank=True)
    provider_message_id = models.CharField(max_length=128, blank=True, db_index=True)
    # Lets the owner see which rules the AI was following when it said something.
    playbook_version = models.ForeignKey(
        PlaybookVersion, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_sender_display()}: {(self.text or self.transcript)[:50]}"
