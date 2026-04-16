"""Split a video file into clips using scene detection.

Pure file-based operation: no database models, no AI captioning.
Input: a video file. Output: numbered clip files + clips.json metadata.

Usage:
    python manage.py split_video --video /path/to/video.mp4
    python manage.py split_video --video /path/to/video.mp4 --output ./my_clips
    python manage.py split_video --video /path/to/video.mp4 --threshold 8.0 --min-scene-length 3.0
    python manage.py split_video --video /path/to/video.mp4 --no-split
    python manage.py split_video --video /path/to/video.mp4 --posters
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from django.core.management.base import BaseCommand, CommandError

from apps.assets.services.video_file_utils import (
    detect_fps,
    extract_frame,
    probe_metadata,
    split_scenes,
)


def process_single_video(
    video_path: Path,
    output_dir: Path,
    threshold: float = 10.0,
    min_scene_length: float = 5.0,
    no_split: bool = False,
    posters: bool = False,
    stdout=None,
    style=None,
) -> dict:
    """Process a single video: detect scenes, split into clips, write metadata.

    Args:
        video_path: Resolved path to video file.
        output_dir: Directory where clips will be written.
        threshold: Scene detection sensitivity (5.0-15.0).
        min_scene_length: Minimum clip duration in seconds.
        no_split: Skip scene detection, use whole video as one clip.
        posters: Extract a thumbnail frame per clip.
        stdout: Output stream for messages (None for silent).
        style: Django command style object for colored output (None for plain).

    Returns:
        Dict with keys: clips (int), duration (float), error (str | None).
    """

    def write(msg: str) -> None:
        if stdout:
            stdout.write(msg)

    def warn(msg: str) -> None:
        if stdout:
            stdout.write(style.WARNING(msg) if style else msg)

    def success(msg: str) -> None:
        if stdout:
            stdout.write(style.SUCCESS(msg) if style else msg)

    output_dir.mkdir(parents=True, exist_ok=True)

    write(f"Input:  {video_path}")
    write(f"Output: {output_dir}")

    # ── Probe metadata ──────────────────────────────────────
    width, height, duration = probe_metadata(str(video_path))

    if duration <= 0:
        return {"clips": 0, "duration": 0.0, "error": f"Invalid duration: {duration}"}

    fps = detect_fps(str(video_path))

    write(f"Resolution: {width}x{height}, Duration: {duration:.1f}s, FPS: {fps:.2f}")

    # ── Scene detection ─────────────────────────────────────
    if no_split:
        write("Scene detection skipped (--no-split)")
        segments = [(0.0, duration)]
        scene_list = []
    else:
        write(
            f"Detecting scenes (threshold={threshold}, "
            f"min_length={min_scene_length}s)..."
        )
        segments, scene_list = split_scenes(
            str(video_path),
            min_scene_length=min_scene_length,
            threshold=threshold,
        )

        if not segments:
            warn("No scenes detected -- using full video as single clip")
            segments = [(0.0, duration)]
            scene_list = []
        else:
            write(f"Detected {len(segments)} scene(s)")

    # ── Split video into clips ──────────────────────────────
    write("Splitting video...")

    if scene_list:
        from scenedetect.video_splitter import split_video_ffmpeg  # type: ignore

        split_video_ffmpeg(
            [str(video_path)],
            scene_list,
            output_dir=str(output_dir),
            output_file_template="clip_$SCENE_NUMBER.mp4",
            suppress_output=True,
        )
    else:
        for i, (start, end) in enumerate(segments):
            clip_path = output_dir / f"clip_{i + 1:03d}.mp4"
            cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-ss", str(start),
                "-t", str(end - start),
                "-c", "copy",
                "-y",
                "-loglevel", "error",
                str(clip_path),
            ]
            subprocess.run(cmd, check=True, capture_output=True)

    # ── Poster extraction (optional) ────────────────────────
    if posters:
        posters_dir = output_dir / "posters"
        posters_dir.mkdir(exist_ok=True)
        write("Extracting poster frames...")

        for i, (start, end) in enumerate(segments):
            poster_ts = start + (end - start) * 0.1
            poster_path = posters_dir / f"clip_{i + 1:03d}.jpg"
            if not extract_frame(str(video_path), poster_ts, poster_path):
                warn(f"  Could not extract poster for clip_{i + 1:03d}")

    # ── Write clips.json ────────────────────────────────────
    clips_data = []
    for i, (start, end) in enumerate(segments):
        entry = {
            "filename": f"clip_{i + 1:03d}.mp4",
            "index": i + 1,
            "start_sec": round(start, 3),
            "end_sec": round(end, 3),
            "duration_sec": round(end - start, 3),
        }
        if posters:
            entry["poster"] = f"posters/clip_{i + 1:03d}.jpg"
        clips_data.append(entry)

    summary = {
        "source_video": video_path.name,
        "resolution": {"width": width, "height": height},
        "fps": round(fps, 2),
        "total_duration_sec": round(duration, 3),
        "scene_detection": {
            "threshold": threshold,
            "min_scene_length_sec": min_scene_length,
            "scenes_detected": len(segments),
            "skipped": no_split,
        },
        "clips": clips_data,
    }

    json_path = output_dir / "clips.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    # ── Summary ─────────────────────────────────────────────
    clip_files = sorted(output_dir.glob("clip_*.mp4"))

    success(f"\nGenerated {len(clip_files)} clip(s) in {output_dir}/")
    for clip in clips_data:
        write(
            f"  {clip['filename']}: "
            f"{clip['start_sec']:.1f}s - {clip['end_sec']:.1f}s "
            f"({clip['duration_sec']:.1f}s)"
        )
    write("  clips.json written")
    if posters:
        write("  posters/ written")

    return {"clips": len(clip_files), "duration": duration, "error": None}


class Command(BaseCommand):
    help = "Split a video file into clips using scene detection. No database required."

    def add_arguments(self, parser):
        parser.add_argument(
            "--video",
            type=str,
            required=True,
            help="Path to input video file",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Output directory (default: ./{video_stem}_clips/)",
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
            help="Skip scene detection, copy whole video as single clip",
        )
        parser.add_argument(
            "--posters",
            action="store_true",
            help="Extract a thumbnail frame from each clip",
        )

    def handle(self, *args, **options):
        video_path = Path(options["video"]).resolve()

        if not video_path.exists():
            raise CommandError(f"Video file not found: {video_path}")
        if not video_path.is_file():
            raise CommandError(f"Path is not a file: {video_path}")

        # Resolve output directory
        if options["output"]:
            output_dir = Path(options["output"]).resolve()
        else:
            output_dir = Path.cwd() / f"{video_path.stem}_clips"

        try:
            result = process_single_video(
                video_path=video_path,
                output_dir=output_dir,
                threshold=options["threshold"],
                min_scene_length=options["min_scene_length"],
                no_split=options["no_split"],
                posters=options["posters"],
                stdout=self.stdout,
                style=self.style,
            )
        except Exception as e:
            raise CommandError(str(e))

        if result["error"]:
            raise CommandError(result["error"])
