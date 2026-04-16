"""
Character Management models for Django.

Converted from FastAPI SQLModel implementation to Django ORM.
Supports comprehensive character creation with traits, relationships, and AI behavior.
"""

import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from apps.projects.models import Project
from apps.world.models import Location

User = get_user_model()


class CharacterStatus(models.TextChoices):
    """Character development status."""

    CONCEPT = "concept", "Concept"
    DEVELOPMENT = "development", "Development"
    COMPLETE = "complete", "Complete"
    ARCHIVED = "archived", "Archived"


class Character(models.Model):
    """Character model for comprehensive character management."""

    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign keys
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="player_character"
    )

    # Basic character information
    name = models.CharField(max_length=255, help_text="Character name")
    description = models.TextField(blank=True, help_text="Character description")
    status = models.CharField(
        max_length=20,
        choices=CharacterStatus.choices,
        default=CharacterStatus.CONCEPT,
        help_text="Character development status",
    )

    # Visual characteristics
    age = models.PositiveIntegerField(
        null=True, blank=True, help_text="Character age (0-200)"
    )
    gender = models.CharField(
        max_length=50, blank=True, null=True, help_text="Character gender"
    )
    appearance = models.TextField(
        blank=True, help_text="Physical appearance description"
    )
    portrait_url = models.URLField(
        max_length=1000, blank=True, null=True, help_text="Character portrait image URL"
    )

    # Character traits (flexible system)
    core_traits = models.JSONField(
        default=dict, blank=True, help_text="Core character traits and values"
    )
    # Boolean flags (authoring as keys only in list elsewhere; here stored as names for convenience)
    flag_keys = models.JSONField(
        default=list, blank=True, help_text="List of boolean flag names for player character"
    )

    # World integration
    current_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="characters",
        help_text="Character's current location",
    )

    # Relationships with other characters
    relationships = models.JSONField(
        default=dict, blank=True, help_text="Character relationships data"
    )

    # AI behavior configuration
    ai_behavior_config = models.JSONField(
        default=dict, blank=True, help_text="AI behavior configuration data"
    )

    # Character metadata and game properties
    character_metadata = models.JSONField(
        default=dict, blank=True, help_text="Additional character metadata"
    )
    game_properties = models.JSONField(
        default=dict, blank=True, help_text="Game-specific character properties"
    )

    # Tags and organization
    tags = models.JSONField(
        default=list, blank=True, help_text="Character tags for organization"
    )
    categories = models.JSONField(
        default=list, blank=True, help_text="Character categories"
    )

    # Development tracking
    development_notes = models.TextField(
        blank=True, help_text="Character development notes"
    )
    inspiration_sources = models.JSONField(
        default=list, blank=True, help_text="Inspiration sources for character"
    )

    # Character-specific gameplay fields (removed is_player_character and is_main_character as redundant)

    # Character progression
    experience_points = models.PositiveIntegerField(
        default=0, help_text="Character experience points"
    )
    character_level = models.PositiveIntegerField(
        default=1, help_text="Character level"
    )
    progression_data = models.JSONField(
        default=dict, blank=True, help_text="Character progression data"
    )

    # Inventory and possessions
    inventory = models.JSONField(
        default=dict, blank=True, help_text="Character inventory data"
    )
    equipment = models.JSONField(
        default=dict, blank=True, help_text="Character equipment data"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete support
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "characters"
        ordering = ["created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__lte=200), name="valid_character_age"
            ),
            models.CheckConstraint(
                check=models.Q(character_level__gte=1), name="valid_character_level"
            ),
        ]
        indexes = [
            models.Index(fields=["project"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def clean(self):
        """Validate model data."""
        # Validate age range
        if self.age is not None and (self.age < 0 or self.age > 200):
            raise ValidationError("Age must be between 0 and 200")

        # Validate character level
        if self.character_level < 1:
            raise ValidationError("Character level must be at least 1")

        # Ensure current location belongs to same project if set
        if (
            self.current_location
            and self.current_location.project_id != self.project_id
        ):
            raise ValidationError("Character location must belong to the same project")

    def save(self, *args, **kwargs):
        """Override save to run validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Mark character as deleted instead of actually deleting."""
        from django.utils import timezone

        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def is_deleted(self):
        """Check if character is soft deleted."""
        return self.deleted_at is not None

    def restore(self):
        """Restore soft deleted character."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def to_dict(self, include_details=False):
        """Convert character to dictionary for API responses."""
        data = {
            "id": str(self.id),
            "project_id": str(self.project.id),
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "age": self.age,
            "gender": self.gender,
            "appearance": self.appearance,
            "portrait_url": self.portrait_url,
            "current_location_id": str(self.current_location.id)
            if self.current_location
            else None,
            "tags": self.tags or [],
            "categories": self.categories or [],
            "experience_points": self.experience_points,
            "character_level": self.character_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "core_traits": self.core_traits or {},
            "flag_keys": self.flag_keys or [],
        }

        if include_details:
            data.update(
                {
                    "relationships": self.relationships or {},
                    "ai_behavior_config": self.ai_behavior_config or {},
                    "character_metadata": self.character_metadata or {},
                    "game_properties": self.game_properties or {},
                    "development_notes": self.development_notes,
                    "inspiration_sources": self.inspiration_sources or [],
                    "progression_data": self.progression_data or {},
                    "inventory": self.inventory or {},
                    "equipment": self.equipment or {},
                }
            )

        return data
