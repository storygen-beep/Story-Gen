"""Batch split all videos in a directory into clips using scene detection.

Scans a directory for video files, runs scene detection on each, and outputs
clips into {dir}/clips/{video_stem}/. Skips videos whose output folder
already exists.

Usage:
    python manage.py batch_split_videos --dir /path/to/videos/angela_white
    python manage.py batch_split_videos --dir /path/to/videos/angela_white --posters
    python manage.py batch_split_videos --dir /path/to/videos/angela_white --threshold 8.0
"""
from __future__ import annotations

import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.assets.management.commands.split_video import process_single_video


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


class Command(BaseCommand):
    help = "Batch split all videos in a directory into clips. Skips already-processed videos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            type=str,
            required=True,
            help="Directory containing video files",
        )
        parser.add_argument(
            "--threshold",
            type=float,
            default=10.0,
            help="Scene detection sensitivity, 5.0-15.0 (default: 10.0)",
        )
        parser.add_argument(
            "--min-scene-length",
            type=float,
            default=5.0,
            help="Minimum clip duration in seconds (default: 5.0)",
        )
        parser.add_argument(
            "--no-split",
            action="store_true",
            help="Skip scene detection for all videos",
        )
        parser.add_argument(
            "--posters",
            action="store_true",
            help="Extract a thumbnail frame from each clip",
        )

    def handle(self, *args, **options):
        video_dir = Path(options["dir"]).resolve()
        threshold = options["threshold"]
        min_scene_length = options["min_scene_length"]
        no_split = options["no_split"]
        posters = options["posters"]

        # ── Validate directory ──────────────────────────────────
        if not video_dir.exists():
            raise CommandError(f"Directory not found: {video_dir}")
        if not video_dir.is_dir():
            raise CommandError(f"Path is not a directory: {video_dir}")

        # ── Scan for video files ────────────────────────────────
        video_files = sorted(
            f for f in video_dir.iterdir()
            if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
        )

        if not video_files:
            raise CommandError(f"No video files found in {video_dir}")

        clips_root = video_dir / "clips"

        self.stdout.write(f"Directory: {video_dir}")
        self.stdout.write(f"Output:    {clips_root}/")
        self.stdout.write(f"Videos found: {len(video_files)}")
        self.stdout.write("")

        # ── Process each video ──────────────────────────────────
        processed = 0
        skipped = 0
        failed = 0
        total_clips = 0

        for idx, video_path in enumerate(video_files, 1):
            video_output_dir = clips_root / video_path.stem
            label = f"[{idx}/{len(video_files)}] {video_path.name}"

            # Skip if output folder already exists
            if video_output_dir.exists():
                self.stdout.write(self.style.WARNING(f"{label} -- skipped (folder exists)"))
                skipped += 1
                continue

            self.stdout.write(self.style.HTTP_INFO(f"\n{'=' * 60}"))
            self.stdout.write(self.style.HTTP_INFO(f"{label}"))
            self.stdout.write(self.style.HTTP_INFO(f"{'=' * 60}"))

            start_time = time.time()

            try:
                result = process_single_video(
                    video_path=video_path,
                    output_dir=video_output_dir,
                    threshold=threshold,
                    min_scene_length=min_scene_length,
                    no_split=no_split,
                    posters=posters,
                    stdout=self.stdout,
                    style=self.style,
                )

                elapsed = time.time() - start_time

                if result["error"]:
                    self.stdout.write(
                        self.style.ERROR(f"  Error: {result['error']} ({elapsed:.1f}s)")
                    )
                    failed += 1
                else:
                    processed += 1
                    total_clips += result["clips"]
                    self.stdout.write(f"  Completed in {elapsed:.1f}s")

            except Exception as e:
                elapsed = time.time() - start_time
                self.stdout.write(
                    self.style.ERROR(f"  Failed: {e} ({elapsed:.1f}s)")
                )
                failed += 1

        # ── Batch summary ───────────────────────────────────────
        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(self.style.SUCCESS("Batch complete"))
        self.stdout.write(f"  Processed: {processed}")
        self.stdout.write(f"  Skipped:   {skipped}")
        if failed:
            self.stdout.write(self.style.ERROR(f"  Failed:    {failed}"))
        else:
            self.stdout.write(f"  Failed:    {failed}")
        self.stdout.write(f"  Total clips generated: {total_clips}")
        self.stdout.write(f"  Output: {clips_root}/")
