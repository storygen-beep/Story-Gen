# Generated manually for review process removal
from django.db import migrations


def cleanup_review_state(apps, schema_editor):
    """Clean up videos in READY_FOR_REVIEW status before removing review fields."""
    AssetVideo = apps.get_model('assets', 'AssetVideo')
    AssetClip = apps.get_model('assets', 'AssetClip')

    # Move READY_FOR_REVIEW videos to appropriate status
    videos = AssetVideo.objects.filter(status='ready_for_review')

    for video in videos:
        # Check if clips have uploaded files
        clips_with_files = video.clips.exclude(file='').count()
        total_clips = video.clips.count()

        if total_clips == 0:
            # No clips - mark as failed
            video.status = 'failed'
            video.error = 'Migration: No clips found'
        elif clips_with_files == total_clips:
            # All clips uploaded - mark as complete
            video.status = 'complete'
        else:
            # Some clips missing - mark as failed
            video.status = 'failed'
            video.error = f'Migration: Only {clips_with_files} of {total_clips} clips have uploaded files'

        video.save(update_fields=['status', 'error'])

    # Clear temp file paths (files are ephemeral and likely already gone)
    AssetClip.objects.update(temp_file_path='')

    print(f"Migrated {videos.count()} videos from ready_for_review status")


def reverse_migration(apps, schema_editor):
    """Reverse migration - no-op since we can't restore deleted temp files."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_make_clipframe_image_optional'),
    ]

    operations = [
        migrations.RunPython(cleanup_review_state, reverse_migration),
    ]
