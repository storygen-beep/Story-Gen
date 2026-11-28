"""Tenants (agencies) and the people who work leads inside them.

Every other table hangs off Organization, so one deployment can serve many
agencies without their data ever mixing.
"""

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    class Status(models.TextChoices):
        PILOT = "pilot", "Pilot"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        CHURNED = "churned", "Churned"

    name = models.CharField(max_length=200)
    # Dubai brokerages are licensed by RERA; optional for other industries.
    license_number = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=2, default="AE", help_text="ISO 3166-1 alpha-2")
    timezone = models.CharField(max_length=64, default="Asia/Dubai")
    plan = models.CharField(max_length=32, default="pilot")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PILOT)

    def __str__(self):
        return self.name


class Agent(TimeStampedModel):
    """A human on the agency's team who receives hot leads."""

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MANAGER = "manager", "Manager"
        AGENT = "agent", "Agent"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="agents")
    name = models.CharField(max_length=200)
    # Handoffs go to the agent's own WhatsApp so they don't have to change habits.
    whatsapp_number = models.CharField(max_length=20, help_text="E.164, e.g. +971501234567")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.AGENT)
    languages = models.JSONField(default=list, blank=True, help_text='e.g. ["en", "ar"]')
    areas = models.JSONField(default=list, blank=True, help_text='e.g. ["Dubai Marina", "JVC"]')
    # Who gets the lead when this agent doesn't accept a handoff in time.
    backup_agent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="backs_up"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "whatsapp_number"], name="unique_agent_number_per_org"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.organization})"
