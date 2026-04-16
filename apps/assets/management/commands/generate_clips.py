"""Management command to generate video clips from a video file using scene detection."""
from __future__ import annotations

import subprocess
from fractions import Fraction
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.assets.services.processing import _split_scenes, _probe_metadata


class Command(BaseCommand):
    help = "Generate video clips from a video file using scene detection."

    def add_arguments(self, parser):
        parser.add_argument(
            '--video',
            type=str,
            required=True,
            help='Path to input video file'
        )
        parser.add_argument(
            '--output',
            type=str,
            required=True,
            help='Output directory for clips'
        )
        parser.add_argument(
            '--threshold',
            type=float,
            default=10.0,
            help='Scene detection threshold (5.0-15.0, default: 10.0)'
        )
        parser.add_argument(
            '--min-scene-length',
            type=float,
            default=5.0,
            help='Minimum scene length in seconds (default: 5.0)'
        )
        parser.add_argument(
            '--no-split',
            action='store_true',
            help='Skip scene detection, use full video as single clip'
        )

    def handle(self, *args, **options):
        video_path = Path(options['video'])
        output_base = Path(options['output'])
        threshold = options['threshold']
        min_scene_length = options['min_scene_length']
        no_split = options['no_split']

        # Validate video file exists
        if not video_path.exists():
            raise CommandError(f"Video file not found: {video_path}")

        if not video_path.is_file():
            raise CommandError(f"Path is not a file: {video_path}")

        # Create output directory structure: {output}/{video_name}/
        video_name = video_path.stem
        clips_dir = output_base / video_name
        clips_dir.mkdir(parents=True, exist_ok=True)

        self.stdout.write(f"Processing {video_path.name}...")

        # Probe video metadata
        try:
            width, height, duration = _probe_metadata(str(video_path))
        except Exception as e:
            raise CommandError(f"Failed to read video metadata: {e}")

        self.stdout.write(
            f"  Resolution: {width}×{height}, Duration: {duration:.1f}s"
        )

        # Detect video FPS for frame conversion
        try:
            fps_result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                 '-show_entries', 'stream=r_frame_rate', '-of',
                 'default=noprint_wrappers=1:nokey=1', str(video_path)],
                capture_output=True, text=True, check=True
            )
            fps_str = fps_result.stdout.strip()
            fps = float(Fraction(fps_str)) if '/' in fps_str else float(fps_str)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  Could not detect FPS, using 30.0: {e}"))
            fps = 30.0

        # Convert min_scene_length from seconds to frames
        min_scene_frames = int(min_scene_length * fps)

        self.stdout.write(
            f"  Video FPS: {fps:.2f}, Min scene: {min_scene_length}s = {min_scene_frames} frames"
        )

        # Scene detection or single clip
        if no_split:
            self.stdout.write("  Scene detection disabled, using full video as single clip")
            segments = [(0.0, duration)]
            scene_list = []
        else:
            self.stdout.write(
                f"  Detecting scenes (threshold={threshold})..."
            )

            # Temporarily update constants in processing module
            import apps.assets.services.processing as processing_module
            original_threshold = getattr(processing_module, 'SCENE_DETECTION_THRESHOLD', 10.0)
            original_min_length = getattr(processing_module, 'SCENE_MIN_LENGTH_FRAMES', 10)

            try:
                processing_module.SCENE_DETECTION_THRESHOLD = threshold
                processing_module.SCENE_MIN_LENGTH_FRAMES = min_scene_frames

                segments, scene_list = _split_scenes(str(video_path))
            finally:
                # Restore original values
                processing_module.SCENE_DETECTION_THRESHOLD = original_threshold
                processing_module.SCENE_MIN_LENGTH_FRAMES = original_min_length

            if not segments:
                self.stdout.write(
                    self.style.WARNING(
                        "  No scenes detected - using full video as single clip"
                    )
                )
                segments = [(0.0, duration)]
                scene_list = []
            else:
                self.stdout.write(f"  Detected {len(segments)} scene(s)")

        # Split video into clips using FFmpeg
        self.stdout.write(f"  Splitting video into clips...")

        try:
            if scene_list:
                # Use scenedetect's built-in FFmpeg splitter
                from scenedetect.video_splitter import split_video_ffmpeg

                split_video_ffmpeg(
                    [str(video_path)],
                    scene_list,
                    output_dir=str(clips_dir),
                    suppress_output=True
                )
            else:
                # Manual FFmpeg splitting for single clip or fallback
                import subprocess

                for i, (start, end) in enumerate(segments):
                    output_path = clips_dir / f"clip_{i:03d}.mp4"
                    clip_duration = end - start

                    cmd = [
                        'ffmpeg',
                        '-i', str(video_path),
                        '-ss', str(start),
                        '-t', str(clip_duration),
                        '-c', 'copy',  # Stream copy (fast, lossless)
                        '-y',  # Overwrite existing
                        '-loglevel', 'error',  # Suppress verbose output
                        str(output_path)
                    ]

                    subprocess.run(cmd, check=True, capture_output=True)

        except Exception as e:
            raise CommandError(f"Failed to split video: {e}")

        # Output summary
        clip_files = sorted(clips_dir.glob('*.mp4'))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Generated {len(clip_files)} clip(s) in {clips_dir}/"
            )
        )

        # Show clip details
        for i, (start, end) in enumerate(segments):
            clip_duration = end - start
            self.stdout.write(
                f"    clip_{i:03d}.mp4: {start:.1f}s - {end:.1f}s ({clip_duration:.1f}s)"
            )

        self.stdout.write(
            f"\nNext steps:"
        )
        self.stdout.write(
            f"  python manage.py caption_clips --input {clips_dir}"
        )
