import os
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


def assets_upload_to(instance, filename: str) -> str:
    # Store by owner/video to keep paths tidy and scoped to user
    owner_id = None
    video_id = None
    if hasattr(instance, "group") and instance.group and instance.group.owner_id:
        owner_id = str(instance.group.owner_id)
    if hasattr(instance, "id") and instance.id:
        video_id = str(instance.id)
    # Fallbacks
    owner_id = owner_id or "unknown"
    video_id = video_id or "temp"
    return os.path.join("assets", owner_id, video_id, "original", filename)


def asset_file_path(owner_id: uuid.UUID, video_id: uuid.UUID, *parts: str) -> str:
    return os.path.join("assets", str(owner_id), str(video_id), *parts)


class AssetGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="asset_groups"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "asset_groups"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "created_at"]) ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AssetVideoStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETE = "complete", "Complete"
    FAILED = "failed", "Failed"


class AssetVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(AssetGroup, on_delete=models.CASCADE, related_name="videos")
    file = models.FileField(upload_to=assets_upload_to, max_length=500)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField(default=0)

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    duration_sec = models.FloatField(null=True, blank=True)
    poster = models.ImageField(upload_to="assets/posters/", null=True, blank=True, max_length=255)

    status = models.CharField(max_length=16, choices=AssetVideoStatus.choices, default=AssetVideoStatus.PENDING)
    error = models.TextField(blank=True)

    # Progress tracking for UX
    processing_stage = models.CharField(max_length=100, blank=True, help_text="Current processing stage")
    processing_progress = models.IntegerField(default=0, help_text="Processing progress 0-100")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "asset_videos"
        indexes = [
            models.Index(fields=["group", "created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"Video {os.path.basename(self.file.name)}"

    @property
    def poster_url(self) -> str | None:
        try:
            return self.poster.url if self.poster else None
        except Exception:
            return None

    @property
    def file_url(self) -> str:
        try:
            return self.file.url
        except Exception:
            return ""

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "group_id": str(self.group_id),
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "width": self.width,
            "height": self.height,
            "duration_sec": self.duration_sec,
            "poster_url": self.poster_url,
            "file_url": self.file_url,
            "status": self.status,
            "error": self.error or None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AssetClip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(AssetVideo, on_delete=models.CASCADE, related_name="clips")
    index = models.IntegerField()
    start_sec = models.FloatField()
    end_sec = models.FloatField()
    duration_sec = models.FloatField()
    file = models.FileField(upload_to="assets/clips/", max_length=255, blank=True)
    poster = models.ImageField(upload_to="assets/posters/", null=True, blank=True, max_length=255)
    status = models.CharField(max_length=16, default="complete")
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    # AI-generated description fields
    description = models.TextField(
        blank=True,
        help_text="AI-generated description from frame captions"
    )
    description_model = models.CharField(
        max_length=50,
        blank=True,
        help_text="Model used (e.g., grok-4-fast)"
    )
    description_generated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When description was generated"
    )
    description_error = models.TextField(
        blank=True,
        help_text="Error message if generation failed"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "asset_clips"
        indexes = [
            models.Index(fields=["video", "index"]),
            models.Index(fields=["video", "created_at"]),
            models.Index(fields=["deleted_at"]),
        ]

    @property
    def file_url(self) -> str:
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
            "video_id": str(self.video_id),
            "index": self.index,
            "start_sec": self.start_sec,
            "end_sec": self.end_sec,
            "duration_sec": self.duration_sec,
            "file_url": self.file_url,
            "poster_url": self.poster_url,
            "status": self.status,
            "description": self.description,
            "description_model": self.description_model,
            "description_generated_at": self.description_generated_at.isoformat()
                if self.description_generated_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def soft_delete(self):
        """Soft delete clip by setting deleted_at timestamp."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def delete(self, using=None, keep_parents=False, hard_delete=False):
        """Override delete to support both soft and hard delete."""
        if hard_delete:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.soft_delete()


class ClipFrame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clip = models.ForeignKey(AssetClip, on_delete=models.CASCADE, related_name="frames")
    timestamp_sec = models.FloatField()
    image_file = models.ImageField(
        upload_to="assets/frames/",
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional frame image file. For caption-only extraction, this can be null."
    )
    caption_text = models.TextField(blank=True)
    caption_model = models.CharField(max_length=100, default="joycaption2")
    status = models.CharField(max_length=16, default="pending")
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "asset_clip_frames"
        indexes = [
            models.Index(fields=["clip", "timestamp_sec"]),
        ]

    @property
    def image_url(self) -> str:
        try:
            return self.image_file.url
        except Exception:
            return ""

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "clip_id": str(self.clip_id),
            "timestamp_sec": self.timestamp_sec,
            "image_url": self.image_url,
            "caption_text": self.caption_text,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
