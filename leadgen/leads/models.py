"""Leads and everything that happens to them.

A Lead is one real person (unique by phone within an agency). Each time they
reach out — a portal enquiry, a Meta form, a direct WhatsApp — that is an
Inquiry. The split is what stops one buyer who asks about three listings on
two portals from being messaged three times.
"""

from django.db import models

from accounts.models import Agent, Organization, TimeStampedModel
from playbooks.models import KnowledgeItem


class Lead(TimeStampedModel):
    class Score(models.TextChoices):
        UNSCORED = "unscored", "Unscored"
        HOT = "hot", "Hot"
        WARM = "warm", "Warm"
        COLD = "cold", "Cold"

    class Status(models.TextChoices):
        NEW = "new", "New"
        QUALIFYING = "qualifying", "Qualifying"
        HANDED_OFF = "handed_off", "Handed off"
        NURTURING = "nurturing", "Nurturing"
        CLOSED = "closed", "Closed"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="leads")
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, help_text="E.164")
    language = models.CharField(max_length=8, blank=True)
    # Keyed by the playbook's question keys, e.g. {"budget_aed": 2500000, "area": "Marina"}.
    answers = models.JSONField(default=dict, blank=True)
    score = models.CharField(max_length=16, choices=Score.choices, default=Score.UNSCORED)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    assigned_agent = models.ForeignKey(
        Agent, null=True, blank=True, on_delete=models.SET_NULL, related_name="leads"
    )
    # Once a lead says stop, nothing automated is ever sent again.
    opted_out = models.BooleanField(default=False)
    opted_out_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "phone"], name="unique_lead_phone_per_org")
        ]
        indexes = [models.Index(fields=["organization", "score", "status"])]

    def __str__(self):
        return self.name or self.phone


class Inquiry(models.Model):
    class Source(models.TextChoices):
        PROPERTY_FINDER = "property_finder", "Property Finder"
        BAYUT = "bayut", "Bayut"
        DUBIZZLE = "dubizzle", "Dubizzle"
        META_FORM = "meta_form", "Meta lead form"
        WEBSITE = "website", "Website"
        WHATSAPP_DIRECT = "whatsapp_direct", "WhatsApp direct"
        OTHER = "other", "Other"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="inquiries")
    source = models.CharField(max_length=32, choices=Source.choices)
    listing = models.ForeignKey(
        KnowledgeItem, null=True, blank=True, on_delete=models.SET_NULL, related_name="inquiries"
    )
    message = models.TextField(blank=True)
    # The untouched email/webhook body, kept so parsing bugs can be replayed.
    raw_payload = models.JSONField(default=dict, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "inquiries"
        ordering = ["-received_at"]

    def __str__(self):
        return f"{self.lead} via {self.get_source_display()}"


class Handoff(models.Model):
    """A hot lead offered to an agent. Its own table because missed handoffs are
    where agencies lose the most money, so they need to be measured."""

    class Outcome(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        TIMED_OUT = "timed_out", "Timed out"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="handoffs")
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="handoffs")
    summary = models.TextField()
    offered_at = models.DateTimeField(auto_now_add=True)
    accept_deadline = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    outcome = models.CharField(max_length=16, choices=Outcome.choices, default=Outcome.PENDING)
    # Set when this handoff timed out and the lead moved to the backup agent.
    escalated_to = models.OneToOneField(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="escalated_from"
    )

    class Meta:
        ordering = ["-offered_at"]


class FollowUpTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        CANCELLED = "cancelled", "Cancelled"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="follow_ups")
    step = models.PositiveSmallIntegerField(help_text="Index into the playbook follow_up plan")
    due_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["due_at"]


class LeadEvent(models.Model):
    """Append-only history. Dashboard numbers (reply time, time to handoff,
    results per source) are computed from here."""

    class Kind(models.TextChoices):
        CREATED = "created", "Created"
        INQUIRY = "inquiry", "New inquiry"
        FIRST_REPLY = "first_reply", "First reply sent"
        ANSWER_CAPTURED = "answer_captured", "Answer captured"
        SCORE_CHANGED = "score_changed", "Score changed"
        HANDED_OFF = "handed_off", "Handed off"
        HANDOFF_ACCEPTED = "handoff_accepted", "Handoff accepted"
        HANDOFF_TIMED_OUT = "handoff_timed_out", "Handoff timed out"
        HUMAN_TOOK_OVER = "human_took_over", "Human took over"
        RETURNED_TO_AI = "returned_to_ai", "Returned to AI"
        VIEWING_BOOKED = "viewing_booked", "Viewing booked"
        OPTED_OUT = "opted_out", "Opted out"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="events")
    kind = models.CharField(max_length=32, choices=Kind.choices)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.lead}: {self.get_kind_display()}"
