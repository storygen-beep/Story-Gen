"""File-based video processing utilities.

This module provides utilities for file-based video processing that don't require
database models. Designed for standalone clip generation and frame captioning workflows.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

from apps.assets.services.processing import (
    _detect_fps,
    _extract_frame,
    _probe_metadata,
    _split_scenes,
    _ensure_dir,
)


def probe_metadata(video_path: str) -> Tuple[int, int, float]:
    """Probe video file for resolution and duration using OpenCV.

    Returns:
        Tuple of (width, height, duration_seconds).
    """
    return _probe_metadata(video_path)


def detect_fps(video_path: str) -> float:
    """Detect video frame rate using ffprobe.

    Returns:
        FPS as float. Defaults to 30.0 if detection fails.
    """
    return _detect_fps(video_path)


def split_scenes(
    video_path: str,
    min_scene_length: float = 5.0,
    threshold: float = 10.0,
) -> Tuple[List[Tuple[float, float]], List]:
    """Detect scene boundaries in a video using PySceneDetect.

    Returns:
        Tuple of (segments, scene_list) where segments is a list of
        (start_sec, end_sec) tuples and scene_list is the raw PySceneDetect
        list for split_video_ffmpeg(). Returns ([], []) if unavailable.
    """
    return _split_scenes(video_path, min_scene_length=min_scene_length, threshold=threshold)


def extract_frame(video_path: str, timestamp_sec: float, out_path: Path) -> bool:
    """Extract a single frame from video at a given timestamp using OpenCV.

    Returns:
        True if the frame was successfully extracted and written.
    """
    return _extract_frame(video_path, timestamp_sec, out_path)


def sanitize_caption_for_filename(caption: str, max_length: int = 60) -> str:
    """Sanitize caption text for use in filenames.

    Removes filesystem-unsafe characters, collapses whitespace, and truncates
    to maximum length at word boundaries.

    Args:
        caption: Raw caption text from captioning model
        max_length: Maximum length for sanitized caption (default: 60)

    Returns:
        Sanitized caption safe for use in filenames

    Examples:
        >>> sanitize_caption_for_filename("A woman in a red dress / beautiful!")
        'A woman in a red dress  beautiful'
        >>> sanitize_caption_for_filename("Person at 5:30 PM", max_length=15)
        'Person at 5 30'
    """
    # Replace filesystem-unsafe characters with space
    # Unsafe chars: / \ : * ? " < > |
    unsafe_chars = r'[/\\:*?"<>|]'
    clean = re.sub(unsafe_chars, ' ', caption)

    # Collapse multiple spaces
    clean = re.sub(r'\s+', ' ', clean)

    # Truncate at word boundary if too long
    if len(clean) > max_length:
        # Find last space before max_length
        truncated = clean[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            clean = truncated[:last_space]
        else:
            # No spaces found, just truncate
            clean = truncated

    return clean.strip()


def parse_captioned_filename(filename: str) -> Tuple[str, float, str]:
    """Parse a captioned frame filename.

    Expected format: "frame_{timestamp}_{caption}.jpg"

    Args:
        filename: Filename to parse (e.g., "frame_002.50_A woman dancing.jpg")

    Returns:
        Tuple of (prefix, timestamp, caption)
        If no caption found, returns (prefix, timestamp, "")

    Examples:
        >>> parse_captioned_filename("frame_002.50_A woman dancing.jpg")
        ('frame', 2.5, 'A woman dancing')
        >>> parse_captioned_filename("frame_002.50.jpg")
        ('frame', 2.5, '')
    """
    # Remove extension
    name_without_ext = Path(filename).stem

    # Split by underscores
    parts = name_without_ext.split('_', 2)

    if len(parts) < 2:
        raise ValueError(f"Invalid frame filename format: {filename}")

    prefix = parts[0]
    try:
        timestamp = float(parts[1])
    except ValueError:
        raise ValueError(f"Invalid timestamp in filename: {filename}")

    caption = parts[2] if len(parts) > 2 else ""

    return prefix, timestamp, caption


def is_frame_captioned(frame_path: Path) -> bool:
    """Check if frame file has caption in filename.

    Checks if the filename follows the captioned format: frame_{ts}_{caption}.jpg

    Args:
        frame_path: Path to frame file

    Returns:
        True if filename contains caption (has underscore after timestamp)

    Examples:
        >>> is_frame_captioned(Path("frame_002.50_A woman dancing.jpg"))
        True
        >>> is_frame_captioned(Path("frame_002.50.jpg"))
        False
    """
    try:
        _, _, caption = parse_captioned_filename(frame_path.name)
        return bool(caption)  # Non-empty caption means it's captioned
    except ValueError:
        return False


def rename_frame_with_caption(
    frame_path: Path,
    caption: str,
    max_length: int = 60
) -> Path:
    """Rename frame file to include caption in filename.

    Args:
        frame_path: Original frame path (e.g., "frame_002.50.jpg")
        caption: Caption text to embed in filename
        max_length: Maximum caption length in filename

    Returns:
        New path with caption embedded

    Raises:
        FileNotFoundError: If frame_path doesn't exist

    Examples:
        >>> rename_frame_with_caption(
        ...     Path("frame_002.50.jpg"),
        ...     "A woman dancing in the park"
        ... )
        Path("frame_002.50_A woman dancing in the park.jpg")
    """
    if not frame_path.exists():
        raise FileNotFoundError(f"Frame file not found: {frame_path}")

    # Sanitize caption for filename
    safe_caption = sanitize_caption_for_filename(caption, max_length)

    # Parse existing filename to get timestamp
    try:
        prefix, timestamp, _ = parse_captioned_filename(frame_path.name)
    except ValueError:
        # Fallback: assume format is "frame_{timestamp}.jpg"
        stem = frame_path.stem
        parts = stem.rsplit('_', 1)
        if len(parts) == 2:
            prefix = parts[0]
            try:
                timestamp = float(parts[1])
            except ValueError:
                raise ValueError(f"Cannot parse timestamp from: {frame_path.name}")
        else:
            raise ValueError(f"Invalid frame filename format: {frame_path.name}")

    # Build new filename
    new_name = f"{prefix}_{timestamp:06.2f}_{safe_caption}{frame_path.suffix}"
    new_path = frame_path.parent / new_name

    # Rename file
    frame_path.rename(new_path)

    return new_path


def extract_frames_from_video(
    video_path: Path,
    output_dir: Path,
    interval_sec: float = 2.0,
    name_prefix: str = "frame"
) -> List[Path]:
    """Extract frames from video at regular intervals.

    Uses existing _extract_frame() and _probe_metadata() from processing.py
    to extract frames without requiring database models.

    Args:
        video_path: Path to input video file
        output_dir: Directory for output frames
        interval_sec: Time interval between frames in seconds (default: 2.0)
        name_prefix: Prefix for frame filenames (default: "frame")

    Returns:
        List of paths to successfully extracted frame files

    Raises:
        RuntimeError: If video cannot be opened

    Examples:
        >>> frames = extract_frames_from_video(
        ...     Path("video.mp4"),
        ...     Path("./frames"),
        ...     interval_sec=3.0
        ... )
        >>> len(frames)
        20
    """
    # Ensure output directory exists
    _ensure_dir(output_dir)

    # Get video metadata
    width, height, duration = _probe_metadata(str(video_path))

    if duration <= 0:
        raise RuntimeError(f"Invalid video duration: {duration}")

    # Calculate frame timestamps
    timestamps = []
    current = 0.0
    while current <= duration:
        timestamps.append(current)
        current += interval_sec

    # Ensure last timestamp doesn't exceed duration
    if timestamps and timestamps[-1] > duration:
        timestamps[-1] = duration

    # Extract frames at each timestamp
    extracted = []
    for ts in timestamps:
        frame_path = output_dir / f"{name_prefix}_{ts:06.2f}.jpg"

        # Use existing _extract_frame from processing.py
        success = _extract_frame(str(video_path), ts, frame_path)

        if success and frame_path.exists():
            extracted.append(frame_path)

    return extracted
