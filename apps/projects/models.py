import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class ProjectStatus(models.TextChoices):
    """Project status enumeration."""

    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"
    DELETED = "deleted", "Deleted"


class ProjectComplexity(models.TextChoices):
    """Project complexity level."""

    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"


class Project(models.Model):
    """
    Project model for managing game creation projects.

    Compatible with FastAPI backend API and frontend interface.
    """

    # Primary key - UUID to match FastAPI
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic project information
    name = models.CharField(max_length=255, help_text="Project name")
    description = models.TextField(blank=True, help_text="Project description")
    summary = models.TextField(blank=True, help_text="Brief project summary")

    # Project configuration
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.DRAFT,
        help_text="Current project status",
    )
    complexity = models.CharField(
        max_length=20,
        choices=ProjectComplexity.choices,
        default=ProjectComplexity.BEGINNER,
        help_text="Project complexity level",
    )
    genre = models.CharField(
        max_length=100, blank=True, null=True, help_text="Game genre"
    )
    theme = models.CharField(
        max_length=100, blank=True, null=True, help_text="Game theme"
    )
    world_size = models.CharField(
        max_length=50, default="medium", help_text="World size setting"
    )

    # JSON fields for flexible data storage
    settings = models.JSONField(default=dict, help_text="Project settings")
    metadata = models.JSONField(default=dict, help_text="Project metadata")

    # Ownership and permissions
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        help_text="Project owner",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete support
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Starting canvas reference
    starting_canvas = models.ForeignKey(
        "stories.StoryCanvas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects_starting",
        help_text="Default starting canvas for this project",
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def soft_delete(self):
        """Mark project as deleted instead of actually deleting it."""
        self.status = ProjectStatus.DELETED
        self.deleted_at = timezone.now()
        self.save(update_fields=["status", "deleted_at"])

    def is_deleted(self):
        """Check if project is soft deleted."""
        return self.deleted_at is not None or self.status == ProjectStatus.DELETED

    def restore(self):
        """Restore soft deleted project."""
        self.status = ProjectStatus.DRAFT
        self.deleted_at = None
        self.save(update_fields=["status", "deleted_at"])

    def get_starting_canvas(self):
        """Get the starting canvas for this project."""
        return self.starting_canvas

    def set_starting_canvas(self, canvas):
        """Set the starting canvas for this project."""
        self.starting_canvas = canvas
        self.save(update_fields=["starting_canvas"])

    def get_time_settings(self):
        """
        Get time settings from metadata with proper defaults.

        Returns:
            dict: Time settings configuration
        """
        default_time_settings = {
            "enabled": True,
            "starting_hour": 8,
            "starting_day": "Monday",
            "starting_week": 1
        }

        # Get time_settings from metadata or use defaults
        time_settings = self.metadata.get("time_settings", {})

        # Ensure all required keys are present
        for key, default_value in default_time_settings.items():
            if key not in time_settings:
                time_settings[key] = default_value

        return time_settings

    def set_time_settings(self, time_settings):
        """
        Update time settings in metadata.

        Args:
            time_settings (dict): Time settings to update
        """
        if not isinstance(self.metadata, dict):
            self.metadata = {}

        self.metadata["time_settings"] = time_settings
        self.save(update_fields=["metadata"])

    def to_dict(self):
        """
        Convert project to dictionary for API response.

        Returns dictionary matching frontend interface expectations.
        """
        return {
            "id": str(self.id),  # Convert UUID to string
            "name": self.name,
            "description": self.description,
            "summary": self.summary,
            "complexity": self.complexity,
            "genre": self.genre,
            "theme": self.theme,
            "world_size": self.world_size,
            "settings": self.settings,
            "metadata": self.metadata,
            "user_id": str(self.owner.id),  # Frontend expects user_id, not owner_id
            "starting_canvas_id": str(self.starting_canvas.id)
            if self.starting_canvas
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
