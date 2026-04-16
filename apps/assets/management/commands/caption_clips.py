"""Management command to extract frames from clips and generate captions using vLLM."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List

from django.core.management.base import BaseCommand, CommandError

from apps.assets.services.vllm_captioning import get_vllm_client
from apps.assets.services.video_file_utils import (
    extract_frames_from_video,
    is_frame_captioned,
    rename_frame_with_caption,
    sanitize_caption_for_filename,
)
from apps.assets.services.processing import _probe_metadata


class Command(BaseCommand):
    help = "Extract frames from video clips and generate captions using vLLM."

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            type=str,
            required=True,
            help="Directory containing clips OR single clip file",
        )
        parser.add_argument(
            "--interval",
            type=float,
            default=2.0,
            help="Frame extraction interval in seconds (default: 2.0)",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=4,
            help="Batch size for vLLM captioning (default: 4)",
        )
        parser.add_argument(
            "--resume", action="store_true", help="Skip already-captioned frames"
        )
        parser.add_argument(
            "--output-json",
            action="store_true",
            help="Generate captions.json with full metadata",
        )
        parser.add_argument(
            "--max-caption-length",
            type=int,
            default=60,
            help="Maximum caption length in filename (default: 60)",
        )

    def handle(self, *args, **options):
        input_path = Path(options["input"])
        interval = options["interval"]
        batch_size = options["batch_size"]
        resume = options["resume"]
        output_json = options["output_json"]
        max_caption_length = options["max_caption_length"]

        # Check if input exists
        if not input_path.exists():
            raise CommandError(f"Input path not found: {input_path}")

        # Check vLLM availability
        client = get_vllm_client()
        if not client.is_available():
            raise CommandError(
                "vLLM captioning service not available.\n"
                "Ensure joycaption container is running:\n"
                "  docker ps | grep joycaption\n"
                "Or start it with:\n"
                "  docker-compose up -d joycaption"
            )

        self.stdout.write("✓ vLLM service available")

        # Discover clips (directory or single file)
        if input_path.is_file():
            clip_files = [input_path]
            clips_base = input_path.parent
        elif input_path.is_dir():
            clip_files = sorted(input_path.glob("*.mp4"))
            if not clip_files:
                raise CommandError(f"No .mp4 files found in {input_path}")
            clips_base = input_path
        else:
            raise CommandError(f"Invalid input path: {input_path}")

        self.stdout.write(f"Processing {len(clip_files)} clip(s)...")
        self.stdout.write(f"  Frame interval: {interval}s")
        self.stdout.write(f"  Batch size: {batch_size}")

        # Process each clip
        total_frames = 0
        total_captioned = 0
        total_skipped = 0
        start_time = time.time()

        for clip_idx, clip_path in enumerate(clip_files):
            self.stdout.write(f"\n[{clip_idx + 1}/{len(clip_files)}] {clip_path.name}")

            stats = self._process_clip(
                clip_path,
                clips_base,
                interval,
                batch_size,
                resume,
                output_json,
                max_caption_length,
                client,
            )

            total_frames += stats["frames_extracted"]
            total_captioned += stats["frames_captioned"]
            total_skipped += stats["frames_skipped"]

        # Final summary
        elapsed = time.time() - start_time

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ All clips processed ({elapsed:.1f}s)")
        )
        self.stdout.write(f"  Total frames: {total_frames}")
        self.stdout.write(f"  Captioned: {total_captioned}")
        if total_skipped > 0:
            self.stdout.write(f"  Skipped (already captioned): {total_skipped}")

    def _process_clip(
        self,
        clip_path: Path,
        clips_base: Path,
        interval: float,
        batch_size: int,
        resume: bool,
        output_json: bool,
        max_caption_length: int,
        client,
    ) -> dict:
        """Process a single clip: extract frames and caption them.

        Returns dict with stats: frames_extracted, frames_captioned, frames_skipped
        """
        # Create frames directory: {clips_base}/frames/{clip_name}/
        clip_name = clip_path.stem
        frames_dir = clips_base / "frames" / clip_name
        frames_dir.mkdir(parents=True, exist_ok=True)

        # Get clip duration
        try:
            _, _, duration = _probe_metadata(str(clip_path))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Failed to read video: {e}"))
            return {"frames_extracted": 0, "frames_captioned": 0, "frames_skipped": 0}

        # Extract frames
        self.stdout.write(f"  Extracting frames...")

        try:
            frame_paths = extract_frames_from_video(
                clip_path, frames_dir, interval_sec=interval
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Frame extraction failed: {e}"))
            return {"frames_extracted": 0, "frames_captioned": 0, "frames_skipped": 0}

        self.stdout.write(f"  Extracted {len(frame_paths)} frames")

        # Filter for uncaptioned frames if resume mode
        if resume:
            uncaptioned = [f for f in frame_paths if not is_frame_captioned(f)]
            skipped = len(frame_paths) - len(uncaptioned)

            if skipped > 0:
                self.stdout.write(f"  Skipping {skipped} already-captioned frames")

            frames_to_caption = uncaptioned
        else:
            frames_to_caption = frame_paths
            skipped = 0

        if not frames_to_caption:
            self.stdout.write("  No frames to caption")
            return {
                "frames_extracted": len(frame_paths),
                "frames_captioned": 0,
                "frames_skipped": skipped,
            }

        # Batch caption
        self.stdout.write(f"  Captioning {len(frames_to_caption)} frames...")

        try:
            results = client.caption_images_batch(
                [str(p) for p in frames_to_caption], max_workers=batch_size
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Captioning failed: {e}"))
            return {
                "frames_extracted": len(frame_paths),
                "frames_captioned": 0,
                "frames_skipped": skipped,
            }

        # Rename frames with captions and collect metadata
        captioned_count = 0
        failed_count = 0
        metadata_frames = []

        for frame_path, (_, caption, error) in zip(frames_to_caption, results):
            if error:
                self.stdout.write(
                    self.style.WARNING(f"    ✗ {frame_path.name}: {error}")
                )
                failed_count += 1
                continue

            try:
                # Rename frame with caption
                new_path = rename_frame_with_caption(
                    frame_path, caption, max_length=max_caption_length
                )

                captioned_count += 1

                # Collect metadata for JSON
                if output_json:
                    # Parse timestamp from filename
                    parts = frame_path.stem.split("_")
                    timestamp = float(parts[-1]) if len(parts) > 1 else 0.0

                    metadata_frames.append(
                        {
                            "timestamp": timestamp,
                            "filename": new_path.name,
                            "caption_full": caption,
                            "caption_short": sanitize_caption_for_filename(
                                caption, max_caption_length
                            ),
                            "error": None,
                        }
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"    ✗ Failed to rename {frame_path.name}: {e}")
                )
                failed_count += 1

        self.stdout.write(
            f"  ✓ {captioned_count}/{len(frames_to_caption)} frames captioned"
        )

        if failed_count > 0:
            self.stdout.write(self.style.WARNING(f"  {failed_count} frames failed"))

        # Generate captions.json if requested
        if output_json and metadata_frames:
            metadata = {
                "clip_name": clip_path.name,
                "duration_sec": duration,
                "frame_interval": interval,
                "frames": sorted(metadata_frames, key=lambda x: x["timestamp"]),
            }

            metadata_path = frames_dir / "captions.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            self.stdout.write(f"  Saved metadata to {metadata_path.name}")

        # Show sample captions
        if captioned_count > 0:
            sample_frames = sorted(metadata_frames, key=lambda x: x["timestamp"])
            for frame in sample_frames:
                caption = frame["caption_full"]
                self.stdout.write(f"    {frame['timestamp']:.2f}s: \"{caption}\"")

        return {
            "frames_extracted": len(frame_paths),
            "frames_captioned": captioned_count,
            "frames_skipped": skipped,
        }
