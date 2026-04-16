"""
Upload video to asset group and process automatically.

This command replicates the frontend upload workflow via CLI.
"""

import time
import mimetypes
from pathlib import Path
from typing import Optional

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.contrib.auth import get_user_model

from apps.assets.models import AssetGroup, AssetVideo, AssetVideoStatus, ClipFrame
from apps.assets.services.processing import (
    process_video_sync,
    DEFAULT_FRAME_INTERVAL_SEC,
    SCENE_MIN_LENGTH_SEC,
    SCENE_DETECTION_THRESHOLD,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Upload video to asset group and process (completes fully)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--group-id",
            type=str,
            required=True,
            help="UUID of the AssetGroup to upload to",
        )
        parser.add_argument(
            "--video-file", type=str, required=True, help="Path to local video file"
        )
        parser.add_argument(
            "--min-scene-length",
            type=float,
            default=SCENE_MIN_LENGTH_SEC,
            help=f"Minimum scene length in seconds (default: {SCENE_MIN_LENGTH_SEC})",
        )
        parser.add_argument(
            "--threshold",
            type=float,
            default=SCENE_DETECTION_THRESHOLD,
            help=f"Scene detection threshold (default: {SCENE_DETECTION_THRESHOLD})",
        )
        parser.add_argument(
            "--user-email",
            type=str,
            help="Owner email (optional, uses group owner by default)",
        )

    def handle(self, *args, **options):
        """Execute the upload command."""
        group_id = options["group_id"]
        video_file = options["video_file"]
        min_scene_length = options["min_scene_length"]
        threshold = options["threshold"]
        user_email = options.get("user_email")

        # Phase 1: Validate inputs
        self.stdout.write("Validating inputs...")

        video_path = self._validate_video_file(video_file)
        size_bytes = video_path.stat().st_size
        group = self._validate_asset_group(group_id)

        if user_email:
            self._validate_user_email(user_email, group)

        # Phase 2: Create AssetVideo record
        self.stdout.write(self.style.SUCCESS(f'✓ Asset group found: "{group.name}"'))
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Video file validated: {video_path.name} ({size_bytes / 1024 / 1024:.1f} MB)"
            )
        )

        video = self._create_video_record(video_path, size_bytes, group)

        self.stdout.write(self.style.SUCCESS(f"✓ Created video record: {video.id}"))
        self.stdout.write(f"  Storage path: {video.file.name}")

        # Phase 3: Process video
        self.stdout.write("\nStarting video processing...")
        self.stdout.write("  This may take several minutes depending on video length\n")

        success = self._process_video(video, min_scene_length, threshold)

        if not success:
            return

        # Phase 4: Display results
        self._display_results(video)

    def _validate_video_file(self, video_file: str) -> Path:
        """Validate video file exists and is readable."""
        video_path = Path(video_file)

        if not video_path.exists():
            raise CommandError(f"Video file not found: {video_path}")

        if not video_path.is_file():
            raise CommandError(f"Path is not a file: {video_path}")

        # Check file size
        size_bytes = video_path.stat().st_size
        max_size = 1000 * 1024 * 1024  # 500MB limit

        if size_bytes > max_size:
            size_mb = size_bytes / 1024 / 1024
            raise CommandError(f"File too large: {size_mb:.1f}MB (maximum: 500MB)")

        # Validate MIME type
        mime_type, _ = mimetypes.guess_type(str(video_path))

        if not mime_type or not mime_type.startswith("video/"):
            # Check by extension as fallback
            valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
            if video_path.suffix.lower() not in valid_extensions:
                raise CommandError(
                    f"File is not a video. Supported formats: {', '.join(valid_extensions)}"
                )

        return video_path

    def _validate_asset_group(self, group_id: str) -> AssetGroup:
        """Validate asset group exists and is not deleted."""
        try:
            group = AssetGroup.objects.get(id=group_id, deleted_at__isnull=True)
            return group
        except AssetGroup.DoesNotExist:
            raise CommandError(f"Asset group not found or deleted: {group_id}")

    def _validate_user_email(self, email: str, group: AssetGroup) -> User:
        """Validate user exists and matches group owner."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f"User not found: {email}")

        if user.id != group.owner_id:
            raise CommandError(f"User {email} is not the owner of group {group.name}")

        return user

    def _create_video_record(
        self, video_path: Path, size_bytes: int, group: AssetGroup
    ) -> AssetVideo:
        """Create AssetVideo record and upload file to storage."""
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(str(video_path))
        mime_type = mime_type or "application/octet-stream"

        # Create video record
        video = AssetVideo(
            group=group,
            mime_type=mime_type,
            size_bytes=size_bytes,
            status=AssetVideoStatus.PENDING,
        )

        # Upload file to storage (respects R2_ENABLED setting)
        with open(video_path, "rb") as f:
            video.file.save(video_path.name, File(f), save=False)

        video.save()

        return video

    def _process_video(
        self, video: AssetVideo, min_scene_length: float, threshold: float
    ) -> bool:
        """Process video and show progress."""
        try:
            # Start processing
            error = process_video_sync(
                video,
                frame_interval=DEFAULT_FRAME_INTERVAL_SEC,
                min_scene_length=min_scene_length,
                threshold=threshold,
            )

            if error:
                self.stdout.write(self.style.ERROR(f"\n✗ Processing failed: {error}"))
                return False

            # Poll for progress
            self.stdout.write("Processing stages:")

            while video.status == AssetVideoStatus.PROCESSING:
                video.refresh_from_db()

                stage = getattr(video, "processing_stage", "Processing")
                progress = getattr(video, "processing_progress", 0)

                # Update progress line
                self.stdout.write(f"\r  {stage}... {progress}%", ending="")
                self.stdout.flush()

                time.sleep(2)  # Poll every 2 seconds

            self.stdout.write("")  # New line after progress

            return True

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n✗ Processing exception: {e}"))
            raise

    def _display_results(self, video: AssetVideo):
        """Display final processing results."""
        video.refresh_from_db()

        if video.status == AssetVideoStatus.COMPLETE:
            clips = video.clips.all()
            frames = ClipFrame.objects.filter(clip__video=video)

            self.stdout.write(self.style.SUCCESS("\n✅ SUCCESS!"))
            self.stdout.write(f"   Status: {video.status}")
            self.stdout.write(f"   Clips uploaded: {clips.count()}")
            self.stdout.write(f"   Frames extracted: {frames.count()}")
            self.stdout.write(
                f"   Frames captioned: {frames.filter(status='complete').count()}"
            )

            if video.duration_sec:
                self.stdout.write(f"   Duration: {video.duration_sec:.1f}s")
            if video.width and video.height:
                self.stdout.write(f"   Resolution: {video.width}x{video.height}")

            self.stdout.write(f"\n👉 View clips at:")
            self.stdout.write(
                f"   http://localhost:3000/dashboard/assets/videos/{video.id}"
            )

        elif video.status == AssetVideoStatus.FAILED:
            self.stdout.write(self.style.ERROR("\n✗ FAILED"))
            self.stdout.write(f"   Error: {video.error}")

        else:
            self.stdout.write(
                self.style.WARNING(f"\n⚠ Unexpected status: {video.status}")
            )
