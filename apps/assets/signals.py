"""
Signal handlers for automatic file cleanup when assets are deleted.
"""
import logging
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

from .models import AssetClip, ClipFrame

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=AssetClip)
def collect_clip_files_for_deletion(sender, instance, **kwargs):
    """
    Collect file paths before CASCADE deletes related objects.

    This runs before the clip is deleted from the database, allowing us to
    capture file references before related ClipFrame records are CASCADE deleted.
    """
    files_to_delete = []

    # Collect clip video file
    if instance.file:
        try:
            files_to_delete.append(("clip_file", instance.file))
        except Exception as e:
            logger.warning(f"Could not access clip file for {instance.id}: {e}")

    # Collect clip poster image
    if instance.poster:
        try:
            files_to_delete.append(("poster_file", instance.poster))
        except Exception as e:
            logger.warning(f"Could not access clip poster for {instance.id}: {e}")

    # Collect frame images (before CASCADE deletion)
    try:
        for frame in instance.frames.all():
            if frame.image_file:
                files_to_delete.append(("frame_image", frame.image_file))
    except Exception as e:
        logger.warning(f"Could not collect frame files for clip {instance.id}: {e}")

    # Store on the instance for post_delete to use
    instance._files_to_cleanup = files_to_delete
    logger.info(f"Collected {len(files_to_delete)} files for cleanup on clip {instance.id}")


@receiver(post_delete, sender=AssetClip)
def cleanup_clip_files_post_delete(sender, instance, **kwargs):
    """
    Delete files from storage after the database transaction commits.

    This runs after the clip and all related records are deleted from the database.
    File deletion failures are logged but don't prevent the deletion from completing.
    """
    files_to_delete = getattr(instance, '_files_to_cleanup', [])

    if not files_to_delete:
        logger.info(f"No files to clean up for clip {instance.id}")
        return

    success_count = 0
    failure_count = 0

    for file_type, file_field in files_to_delete:
        try:
            # delete(save=False) prevents saving the model instance
            # This is important because the instance is already deleted from DB
            file_field.delete(save=False)
            success_count += 1
            logger.debug(f"Deleted {file_type} for clip {instance.id}")
        except Exception as e:
            failure_count += 1
            logger.error(f"Failed to delete {file_type} for clip {instance.id}: {e}")

    logger.info(
        f"Cleanup complete for clip {instance.id}: "
        f"{success_count} files deleted, {failure_count} failures"
    )


@receiver(post_delete, sender=ClipFrame)
def cleanup_frame_image(sender, instance, **kwargs):
    """
    Delete frame image file when a ClipFrame is deleted.

    This handles cases where individual frames are deleted independently
    (not as part of clip CASCADE deletion).
    """
    if instance.image_file:
        try:
            instance.image_file.delete(save=False)
            logger.debug(f"Deleted frame image for frame {instance.id}")
        except Exception as e:
            logger.error(f"Failed to delete frame image for frame {instance.id}: {e}")
