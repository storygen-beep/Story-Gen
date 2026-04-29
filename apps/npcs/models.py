"""NPC models for Django backend."""

import uuid
from datetime import datetime
from typing import Any

from django.contrib.auth import get_user_model
from apps.common.compat import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.projects.models import Project

User = get_user_model()


class NPCStatus(models.TextChoices):
    """NPC development status."""

    CONCEPT = "concept", "Concept"
    IN_DEVELOPMENT = "in_development", "In Development"
    READY = "ready", "Ready"
    TESTING = "testing", "Testing"
    PUBLISHED = "published", "Published"


class NPC(models.Model):
    """NPC model for non-player characters."""

    # Core identity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="npcs",
        help_text="Project this NPC belongs to",
    )
    name = models.CharField(max_length=255, help_text="NPC display name")
    description = models.TextField(
        blank=True, null=True, help_text="NPC description and background"
    )
    status = models.CharField(
        max_length=50,
        choices=NPCStatus.choices,
        default=NPCStatus.CONCEPT,
        help_text="Development status of the NPC",
    )

    # Appearance and basic info
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        help_text="NPC age in years",
    )
    gender = models.CharField(
        max_length=50, blank=True, null=True, help_text="NPC gender identity"
    )
    appearance = models.TextField(
        blank=True, null=True, help_text="Physical appearance description"
    )
    portrait_url = models.URLField(
        blank=True, null=True, help_text="URL to NPC portrait image"
    )

    # Core traits only
    core_traits = models.JSONField(
        default=dict, blank=True, help_text="Core character traits data"
    )
    # Boolean flags (authoring as keys only)
    flag_keys = models.JSONField(
        default=list, blank=True, help_text="List of boolean flag names for NPC"
    )

    # AI behavior configuration
    ai_behavior_config = models.JSONField(
        default=dict, blank=True, help_text="AI behavior configuration"
    )

    # Location integration removed - NPCs automatically placed during game generation

    # Relationships and interactions
    relationships = models.JSONField(
        default=dict, blank=True, help_text="Relationships with other characters"
    )

    # Organization and metadata
    categories = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="Categories for organization",
    )

    # UI visibility — true = omit from Guide Page, Stats Page, and sidebar NPC-traits widget.
    # Runtime $npcs dict still contains the NPC so narrative/prologue UUID lookups keep working.
    hidden_from_ui = models.BooleanField(
        default=False,
        help_text=(
            "Hide this NPC from Guide Page, Stats Page, and sidebar NPC-traits widget. "
            "Runtime $npcs dict still contains the NPC so prologue/narrative UUID lookups keep working."
        ),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete support
    deleted_at = models.DateTimeField(
        blank=True, null=True, help_text="Soft deletion timestamp"
    )

    class Meta:
        db_table = "npcs"
        indexes = [
            models.Index(fields=["project"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__isnull=True) | models.Q(age__range=(1, 200)),
                name="npc_age_valid_range",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.status})"

    def clean(self):
        """Custom validation."""
        super().clean()
        if not self.name or not self.name.strip():
            from django.core.exceptions import ValidationError

            raise ValidationError("NPC name cannot be empty")

    def save(self, *args, **kwargs):
        """Override save to run validation."""
        self.clean()
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Soft delete the NPC."""
        self.deleted_at = datetime.now()
        self.save(update_fields=["deleted_at"])

    def is_deleted(self):
        """Check if NPC is soft deleted."""
        return self.deleted_at is not None

    def to_dict(self, include_details: bool = False) -> dict[str, Any]:
        """Convert NPC to dictionary format."""
        base_dict = {
            "id": str(self.id),
            "project_id": str(self.project.id),
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "age": self.age,
            "gender": self.gender,
            "appearance": self.appearance,
            "portrait_url": self.portrait_url,
            "current_location_id": None,
            "starting_location_id": None,
            "home_location_id": None,
            "categories": self.categories,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_details:
            base_dict.update(
                {
                    "core_traits": self.core_traits,
                    "flag_keys": self.flag_keys or [],
                    "ai_behavior_config": self.ai_behavior_config,
                    "relationships": self.relationships,
                }
            )

        return base_dict
