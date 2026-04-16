"""
Service for validating and executing clip deletion operations.
"""
import logging
from typing import Dict, List
from django.db import transaction
from django.core.exceptions import ValidationError

from ..models import AssetClip

logger = logging.getLogger(__name__)


class ClipDeletionService:
    """Business logic for clip deletion validation and execution."""

    @staticmethod
    def validate_clip_deletion(clip: AssetClip) -> Dict:
        """
        Validate whether a clip can be deleted.

        Args:
            clip: The AssetClip instance to validate

        Returns:
            Dictionary with validation results:
            {
                "can_delete": bool,
                "blocking_issues": List[str],  # Issues that prevent deletion
                "warnings": List[str]  # Non-blocking concerns
            }
        """
        blocking_issues = []
        warnings = []

        # Check if the parent video is being processed
        if clip.video.status == "processing":
            blocking_issues.append(
                "Parent video is currently being processed. "
                "Please wait for processing to complete before deleting clips."
            )

        # Check if the clip itself is being processed
        if clip.status == "processing":
            blocking_issues.append(
                "This clip is currently being processed. "
                "Please wait for processing to complete before deleting."
            )

        # Check for frames being processed
        processing_frames = clip.frames.filter(status="processing").count()
        if processing_frames > 0:
            blocking_issues.append(
                f"This clip has {processing_frames} frame(s) currently being processed. "
                "Please wait for frame processing to complete."
            )

        # Warning about frame count (not blocking)
        frame_count = clip.frames.count()
        if frame_count > 0:
            warnings.append(
                f"This clip has {frame_count} frame(s) that will also be deleted."
            )

        # Warning about AI-generated content
        if clip.description:
            warnings.append(
                "This clip has an AI-generated description that will be lost."
            )

        return {
            "can_delete": len(blocking_issues) == 0,
            "blocking_issues": blocking_issues,
            "warnings": warnings
        }

    @staticmethod
    def soft_delete_clip(clip: AssetClip) -> Dict:
        """
        Soft delete a clip by setting deleted_at timestamp.

        Args:
            clip: The AssetClip instance to soft delete

        Returns:
            Dictionary with operation results:
            {
                "success": bool,
                "clip_id": str,
                "deletion_type": "soft",
                "frames_affected": int
            }

        Raises:
            ValidationError: If clip cannot be deleted
        """
        # Validate before deleting
        validation = ClipDeletionService.validate_clip_deletion(clip)
        if not validation["can_delete"]:
            error_msg = "; ".join(validation["blocking_issues"])
            raise ValidationError(f"Cannot delete clip: {error_msg}")

        frame_count = clip.frames.count()

        try:
            with transaction.atomic():
                clip.soft_delete()
                logger.info(
                    f"Soft deleted clip {clip.id} (index={clip.index}) "
                    f"from video {clip.video_id}"
                )

            return {
                "success": True,
                "clip_id": str(clip.id),
                "deletion_type": "soft",
                "frames_affected": frame_count
            }
        except Exception as e:
            logger.error(f"Failed to soft delete clip {clip.id}: {e}")
            raise ValidationError(f"Failed to delete clip: {str(e)}")

    @staticmethod
    def hard_delete_clip(clip: AssetClip) -> Dict:
        """
        Permanently delete a clip and all associated files.

        Args:
            clip: The AssetClip instance to permanently delete

        Returns:
            Dictionary with operation results:
            {
                "success": bool,
                "clip_id": str,
                "deletion_type": "hard",
                "frames_deleted": int
            }

        Raises:
            ValidationError: If clip cannot be deleted or is not soft-deleted
        """
        # Ensure clip is already soft-deleted
        if not clip.deleted_at:
            raise ValidationError(
                "Clip must be soft-deleted first before permanent deletion. "
                "This is a safety measure to prevent accidental data loss."
            )

        # Validate before deleting
        validation = ClipDeletionService.validate_clip_deletion(clip)
        if not validation["can_delete"]:
            error_msg = "; ".join(validation["blocking_issues"])
            raise ValidationError(f"Cannot delete clip: {error_msg}")

        frame_count = clip.frames.count()
        clip_id = str(clip.id)

        try:
            with transaction.atomic():
                # hard_delete=True triggers actual database deletion
                # This will also trigger CASCADE deletion of ClipFrame records
                # Signal handlers will clean up files from storage
                clip.delete(hard_delete=True)
                logger.info(
                    f"Hard deleted clip {clip_id} with {frame_count} frames"
                )

            return {
                "success": True,
                "clip_id": clip_id,
                "deletion_type": "hard",
                "frames_deleted": frame_count
            }
        except Exception as e:
            logger.error(f"Failed to hard delete clip {clip_id}: {e}")
            raise ValidationError(f"Failed to permanently delete clip: {str(e)}")
