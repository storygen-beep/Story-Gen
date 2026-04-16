"""
Story models for canvas-based story system.
Implements Phase 1 story canvas management with nodes, connections, and flags.
"""

import uuid

from apps.common.compat import ArrayField
from django.db import models
from django.utils import timezone

from apps.projects.models import Project
from django.conf import settings
import os


def get_default_exit_block():
    """Default exit block configuration for story nodes"""
    return {
        "type": "location",
        "text": "Continue",
        "config": {
            "destinationType": "trigger",
            "time_progression_minutes": 3
        }
    }




class CanvasType(models.TextChoices):
    """Types of story canvases"""

    STORY = "story", "Story Canvas"
    INTRO = "intro", "Introduction Canvas"
    DIALOGUE = "dialogue", "Dialogue Canvas"
    TUTORIAL = "tutorial", "Tutorial Canvas"


class CanvasStatus(models.TextChoices):
    """Status states for story canvases"""

    DRAFT = "draft", "Draft"
    IN_PROGRESS = "in_progress", "In Progress"
    REVIEW = "review", "Under Review"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class ApprovalStatus(models.TextChoices):
    """Approval status for canvas review workflow (tracking only, does not affect game generation)"""

    NOT_SUBMITTED = "not_submitted", "Not Submitted"
    PENDING = "pending", "Pending Review"
    APPROVED = "approved", "Approved"
    NEEDS_CHANGES = "needs_changes", "Needs Changes"


class ConnectionType(models.TextChoices):
    """Types of connections between nodes"""

    DEFAULT = "default", "Default"
    CHOICE = "choice", "Choice"
    CONDITION = "condition", "Conditional"
    RANDOM = "random", "Random"
    TIMED = "timed", "Timed"
    HIDDEN = "hidden", "Hidden"


## StoryFlag removed: scopes and data types no longer used


class StoryCanvas(models.Model):
    """Main story canvas containing nodes and connections"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="story_canvases"
    )

    # Basic info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    canvas_type = models.CharField(
        max_length=20, choices=CanvasType.choices, default=CanvasType.STORY
    )
    status = models.CharField(
        max_length=20, choices=CanvasStatus.choices, default=CanvasStatus.DRAFT
    )

    # Canvas metadata
    metadata = models.JSONField(default=dict, blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    version = models.IntegerField(default=1)

    # Canvas statistics
    node_count = models.IntegerField(default=0)
    connection_count = models.IntegerField(default=0)
    estimated_play_time = models.IntegerField(
        null=True, blank=True, help_text="Estimated play time in minutes"
    )

    # Validation status
    is_valid = models.BooleanField(default=False)
    validation_errors = models.JSONField(default=list, blank=True)
    last_validated_at = models.DateTimeField(null=True, blank=True)

    # Favorites and ordering
    is_favorite = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Approval workflow fields (for tracking only, does not affect game generation)
    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.NOT_SUBMITTED,
        help_text="Review/approval status for tracking purposes"
    )
    review_notes = models.TextField(
        blank=True,
        help_text="Reviewer feedback and notes"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_canvases"
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "story_canvases"
        ordering = ["display_order", "-created_at"]
        indexes = [
            models.Index(fields=["project", "canvas_type"]),
            models.Index(fields=["project", "status"]),
            models.Index(fields=["project", "is_favorite"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.canvas_type})"

    def soft_delete(self):
        """Soft delete the canvas"""
        self.deleted_at = timezone.now()
        self.save()

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "name": self.name,
            "description": self.description,
            "canvas_type": self.canvas_type,
            "status": self.status,
            "metadata": self.metadata,
            "tags": self.tags,
            "version": self.version,
            "node_count": self.node_count,
            "connection_count": self.connection_count,
            "estimated_play_time": self.estimated_play_time,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
            "last_validated_at": self.last_validated_at.isoformat()
            if self.last_validated_at
            else None,
            "is_favorite": self.is_favorite,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "approval_status": self.approval_status,
            "review_notes": self.review_notes,
            "approved_by_id": str(self.approved_by_id) if self.approved_by_id else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }


class StoryNode(models.Model):
    """Individual nodes within a story canvas - simplified for clean story content"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    canvas = models.ForeignKey(
        StoryCanvas, on_delete=models.CASCADE, related_name="nodes"
    )

    # Core content (simplified)
    name = models.CharField(max_length=255)  # Keep existing field name
    node_data = models.JSONField(default=dict, blank=True)  # Only contains 'content'
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    # Exit Block configuration (always present, terminal block)
    exit_block = models.JSONField(
        default=get_default_exit_block,
        blank=True,
        help_text="Configuration for the story node's exit behavior"
    )

    # Position on canvas (keep for React Flow)
    position_x = models.FloatField(default=0)  # Renamed for consistency
    position_y = models.FloatField(default=0)  # Renamed for consistency
    width = models.FloatField(default=400)  # Better default for BlockNote editor
    height = models.FloatField(default=566)  # A4-ish aspect ratio, good editor space

    # Audit fields (keep for tracking)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "story_nodes"
        indexes = [
            models.Index(fields=["canvas", "created_at"]),
        ]

    def __str__(self):
        return f"{self.name}"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "canvas_id": str(self.canvas_id),
            "name": self.name,
            "node_data": self.node_data,
            "exit_block": self.exit_block,
            "tags": self.tags,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "width": self.width,
            "height": self.height,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class NodeConnection(models.Model):
    """Connections between story nodes"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    canvas = models.ForeignKey(
        StoryCanvas, on_delete=models.CASCADE, related_name="connections"
    )

    # Connection endpoints
    source_node = models.ForeignKey(
        StoryNode, on_delete=models.CASCADE, related_name="outgoing_connections"
    )
    target_node = models.ForeignKey(
        StoryNode, on_delete=models.CASCADE, related_name="incoming_connections"
    )

    # Connection properties
    connection_type = models.CharField(
        max_length=20, choices=ConnectionType.choices, default=ConnectionType.DEFAULT
    )
    label = models.CharField(max_length=255, blank=True)

    # Connection data
    conditions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Conditions for this connection to be available",
    )
    effects = models.JSONField(
        default=dict, blank=True, help_text="Effects when this connection is traversed"
    )
    metadata = models.JSONField(default=dict, blank=True)

    # Visual properties
    path_data = models.JSONField(
        default=dict, blank=True, help_text="SVG path data for custom routing"
    )
    style = models.JSONField(
        default=dict, blank=True, help_text="Visual styling properties"
    )

    # Connection properties
    priority = models.IntegerField(
        default=0, help_text="Priority for multiple connections from same node"
    )
    weight = models.FloatField(default=1.0, help_text="Weight for random selection")
    is_bidirectional = models.BooleanField(default=False)

    # Validation
    is_valid = models.BooleanField(default=False)
    validation_errors = models.JSONField(default=list, blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "node_connections"
        indexes = [
            models.Index(fields=["canvas", "source_node"]),
            models.Index(fields=["canvas", "target_node"]),
            models.Index(fields=["canvas", "connection_type"]),
        ]

    def __str__(self):
        return f"{self.source_node.name} -> {self.target_node.name}"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "canvas_id": str(self.canvas_id),
            "source_node_id": str(self.source_node_id),
            "target_node_id": str(self.target_node_id),
            "connection_type": self.connection_type,
            "label": self.label,
            "conditions": self.conditions,
            "effects": self.effects,
            "metadata": self.metadata,
            "path_data": self.path_data,
            "style": self.style,
            "priority": self.priority,
            "weight": self.weight,
            "is_bidirectional": self.is_bidirectional,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


## StoryFlag model removed


class CanvasTrigger(models.Model):
    """Triggers for canvas activation (e.g., intro canvas at specific locations)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    canvas = models.OneToOneField(
        StoryCanvas, on_delete=models.CASCADE, related_name="trigger"
    )

    # Trigger conditions
    location_id = models.UUIDField(
        null=True, blank=True, help_text="Location where this canvas triggers"
    )
    conditions = models.JSONField(
        default=dict, blank=True, help_text="Additional trigger conditions"
    )

    # Trigger properties
    is_active = models.BooleanField(default=True)
    is_activity = models.BooleanField(default=False, help_text="Whether this trigger represents an activity")
    is_repeatable = models.BooleanField(default=True, help_text="Whether this trigger can repeat over time")
    max_triggers_per_day = models.IntegerField(
        null=True, blank=True, help_text="Maximum number of times this can trigger per day"
    )
    priority = models.IntegerField(
        default=0,
        help_text="Higher priority canvases are selected first when multiple are valid. Default 0 for backward compatibility."
    )

    # Trigger metadata
    metadata = models.JSONField(default=dict, blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "canvas_triggers"
        indexes = [
            models.Index(fields=["location_id"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"Trigger for {self.canvas.name}"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "canvas_id": str(self.canvas_id),
            "location_id": str(self.location_id) if self.location_id else None,
            "conditions": self.conditions,
            "is_active": self.is_active,
            "is_activity": self.is_activity,
            "is_repeatable": self.is_repeatable,
            "max_triggers_per_day": self.max_triggers_per_day,
            "priority": self.priority,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TriggerSchedule(models.Model):
    """Schedule definitions for story triggers"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trigger = models.ForeignKey(
        CanvasTrigger, on_delete=models.CASCADE, related_name="schedules"
    )

    # Schedule properties
    name = models.CharField(max_length=255)
    weekdays = models.JSONField(
        help_text="List of weekdays [0-6] where 0=Monday, 6=Sunday"
    )
    start_time = models.TimeField()
    end_time = models.TimeField(
        null=True, blank=True, help_text="End time for range triggers, null for point triggers"
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "trigger_schedules"
        indexes = [
            models.Index(fields=["trigger", "start_time"]),
            models.Index(fields=["start_time", "end_time"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.trigger.canvas.name}"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "trigger_id": str(self.trigger_id),
            "name": self.name,
            "weekdays": self.weekdays,
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M") if self.end_time else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class MediaKind(models.TextChoices):
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"
    GIF = "gif", "GIF"


def media_upload_to(instance, filename: str) -> str:
    # Store by project/kind/date to keep paths tidy
    project_id = str(instance.project_id)
    kind = instance.kind or "other"
    return os.path.join("media", project_id, kind, timezone.now().strftime("%Y/%m/%d"), filename)


class MediaAsset(models.Model):
    """Project-scoped uploaded media (images, videos, gifs)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="media_assets")
    kind = models.CharField(max_length=10, choices=MediaKind.choices)
    file = models.FileField(upload_to=media_upload_to)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField(default=0)

    # Optional metadata
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    duration_sec = models.FloatField(null=True, blank=True)
    poster = models.ImageField(upload_to=media_upload_to, null=True, blank=True)

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "media_assets"
        indexes = [
            models.Index(fields=["project", "kind"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.kind}: {os.path.basename(self.file.name)}"

    @property
    def url(self) -> str:
        try:
            return self.file.url
        except Exception:
            return ""

    @property
    def poster_url(self) -> str | None:
        try:
            return self.poster.url if self.poster else None
        except Exception:
            return None

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "kind": self.kind,
            "url": self.url,
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "width": self.width,
            "height": self.height,
            "duration_sec": self.duration_sec,
            "poster_url": self.poster_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
