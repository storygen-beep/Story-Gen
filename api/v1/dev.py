"""
Development tools endpoints - NOT for production use.
"""

import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

logger = logging.getLogger(__name__)

import requests
from django.conf import settings
from django.urls import path
from rest_framework import status
from collections import defaultdict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone

# Constants
GAMES_BASE_PATH = Path(settings.BASE_DIR) / "games"  # Game folders are under games/
DOWNLOADS_DIR = GAMES_BASE_PATH / "downloads"  # Fallback when no game specified
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
TIMEOUT = 60

# ffmpeg binary paths to search
FFMPEG_PATHS = [
    "ffmpeg",  # In PATH
    "/usr/local/bin/ffmpeg",
    "/opt/homebrew/bin/ffmpeg",  # macOS Homebrew ARM
    "/usr/bin/ffmpeg",
]

# Valid video extensions for cutting
VALID_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v"}

# Media type mappings
EXTENSION_MAP = {
    # Images
    "jpg": "jpg",
    "jpeg": "jpg",
    "png": "png",
    "gif": "gif",
    "webp": "webp",
    "bmp": "bmp",
    # Videos
    "mp4": "mp4",
    "webm": "webm",
    "mov": "mov",
    "mkv": "mkv",
    "avi": "avi",
}

MIME_TO_EXT = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
    "image/bmp": "bmp",
    "video/mp4": "mp4",
    "video/webm": "webm",
    "video/quicktime": "mov",
    "video/x-matroska": "mkv",
    "video/avi": "avi",
}

# Known video platforms that need yt-dlp
VIDEO_PLATFORMS = [
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "twitter.com",
    "x.com",
    "reddit.com",
    "v.redd.it",
    "tiktok.com",
    "instagram.com",
    "dailymotion.com",
    "twitch.tv",
]


def sanitize_path_segment(segment: str) -> str:
    """Sanitize a single path segment to be filesystem-safe."""
    # Allow only alphanumeric, underscore, and hyphen
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", segment)
    # Ensure it's not empty
    return sanitized or "unnamed"


def parse_scene_path(scene_id: str) -> tuple[str, str]:
    """
    Parse scene_id that may contain path separators.
    Returns (subfolder_path, filename_base).

    Examples:
    - "bedroom_test" → ("", "bedroom_test")
    - "scenes/bedroom_test" → ("scenes", "bedroom_test")
    - "chapter1/intro/bg" → ("chapter1/intro", "bg")
    - "scenes/intro.mp4" → ("scenes", "intro")  # Extension stripped
    - "images/locations/bar.jpg" → ("images/locations", "bar")

    Security: Filters out ".." and empty segments, sanitizes each part.
    """
    # Strip known media extensions from scene_id first
    # e.g., "activities/morning_coffee.mp4" -> "activities/morning_coffee"
    # This prevents the dot from being sanitized to underscore
    known_extensions = {'.mp4', '.webm', '.mov', '.mkv', '.avi', '.m4v',
                        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
    scene_path = Path(scene_id)
    if scene_path.suffix.lower() in known_extensions:
        scene_id = str(scene_path.with_suffix(''))

    # Split by forward slash
    parts = scene_id.split("/")

    # Filter and sanitize each segment
    sanitized_parts = []
    for part in parts:
        part = part.strip()
        # Skip empty segments and path traversal attempts
        if not part or part == "." or part == "..":
            continue
        sanitized_parts.append(sanitize_path_segment(part))

    # Handle empty result
    if not sanitized_parts:
        return "", "unnamed"

    # Last part is the filename, rest is subfolder path
    filename_base = sanitized_parts[-1]
    subfolder = "/".join(sanitized_parts[:-1]) if len(sanitized_parts) > 1 else ""

    return subfolder, filename_base


def get_unique_filepath(output_dir: Path, filename_base: str, ext: str) -> tuple[Path, str]:
    """
    Get a unique filepath, adding a counter if file exists.
    Returns (full_path, filename).

    Examples:
    - bedroom_test.jpg (if doesn't exist)
    - bedroom_test_1.jpg (if bedroom_test.jpg exists)
    - bedroom_test_2.jpg (if both exist)
    """
    filename = f"{filename_base}.{ext}"
    filepath = output_dir / filename

    if not filepath.exists():
        return filepath, filename

    # File exists, add counter
    counter = 1
    while True:
        filename = f"{filename_base}_{counter}.{ext}"
        filepath = output_dir / filename
        if not filepath.exists():
            return filepath, filename
        counter += 1


def get_extension_from_url(url: str) -> str | None:
    """Extract file extension from URL path."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    # Get the last part after the last dot
    if "." in path:
        ext = path.rsplit(".", 1)[-1]
        # Remove any query string artifacts
        ext = ext.split("?")[0].split("&")[0]
        if ext in EXTENSION_MAP:
            return EXTENSION_MAP[ext]
    return None


def get_extension_from_content_type(content_type: str) -> str | None:
    """Extract file extension from Content-Type header."""
    if not content_type:
        return None
    # Get the main type (ignore charset etc.)
    main_type = content_type.split(";")[0].strip().lower()
    return MIME_TO_EXT.get(main_type)


def is_video_platform(url: str) -> bool:
    """Check if URL is from a known video platform."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return any(platform in domain for platform in VIDEO_PLATFORMS)


def download_direct(url: str, output_path: Path, progress_callback=None, max_retries=5, extra_headers: dict | None = None) -> tuple[bool, str]:
    """
    Attempt direct download of media file with resume support.
    Returns (success, error_message).
    progress_callback(percent: int, phase: str) is called periodically if provided.
    Automatically retries and resumes from partial file on network errors.
    extra_headers (optional) are merged into every request — e.g. an auth Bearer
    token for sources like RedGIFs whose CDN rejects the bare UA.
    """
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    if extra_headers:
        base_headers.update(extra_headers)

    # First request: check content type and get total size
    try:
        head_resp = requests.head(url, timeout=TIMEOUT, headers=base_headers, allow_redirects=True)
        head_resp.raise_for_status()
        content_type = head_resp.headers.get("Content-Type", "")
        if "text/html" in content_type.lower():
            return False, "URL returned HTML instead of media"
        total_bytes = int(head_resp.headers.get("Content-Length", 0))
        if total_bytes > MAX_FILE_SIZE:
            return False, f"File too large: {total_bytes} bytes"
        supports_range = head_resp.headers.get("Accept-Ranges", "").lower() == "bytes"
    except requests.exceptions.RequestException as e:
        return False, f"HEAD request failed: {str(e)}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    last_error = ""

    for attempt in range(max_retries):
        try:
            headers = dict(base_headers)
            downloaded_bytes = 0
            file_mode = "wb"

            # Resume from partial file if it exists and server supports Range
            if supports_range and output_path.exists():
                downloaded_bytes = output_path.stat().st_size
                if total_bytes and downloaded_bytes >= total_bytes:
                    # Already complete
                    if progress_callback:
                        progress_callback(100, "downloading")
                    return True, ""
                if downloaded_bytes > 0:
                    headers["Range"] = f"bytes={downloaded_bytes}-"
                    file_mode = "ab"  # Append mode
                    print(f"[Video Capture] Resuming from {downloaded_bytes} bytes (attempt {attempt + 1})", flush=True)

            response = requests.get(
                url, stream=True, timeout=TIMEOUT, headers=headers, allow_redirects=True
            )
            response.raise_for_status()

            # On first attempt without resume, check content type
            if file_mode == "wb":
                resp_ct = response.headers.get("Content-Type", "")
                if "text/html" in resp_ct.lower():
                    return False, "URL returned HTML instead of media"

            # Update total if we didn't get it from HEAD
            if not total_bytes:
                cl = response.headers.get("Content-Length")
                if cl:
                    total_bytes = int(cl) + downloaded_bytes

            last_report = 0

            with open(output_path, file_mode) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_bytes += len(chunk)
                    if progress_callback and total_bytes:
                        pct = int(downloaded_bytes / total_bytes * 100)
                        if pct >= last_report + 2:
                            progress_callback(pct, "downloading")
                            last_report = pct

            if progress_callback:
                progress_callback(100, "downloading")

            return True, ""

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                wait = min(2 ** attempt, 30)
                print(f"[Video Capture] Download interrupted: {last_error}. Retrying in {wait}s...", flush=True)
                if progress_callback:
                    progress_callback(
                        int(downloaded_bytes / total_bytes * 100) if total_bytes else 0,
                        "downloading"
                    )
                time.sleep(wait)
            else:
                print(f"[Video Capture] Download failed after {max_retries} attempts", flush=True)

    return False, f"Download failed after {max_retries} retries: {last_error}"


def download_with_ytdlp(url: str, output_dir: Path, filename_base: str, progress_callback=None) -> tuple[bool, str, str | None]:
    """
    Attempt download using yt-dlp.
    Returns (success, error_message, actual_filename).
    progress_callback(percent: int, phase: str) is called periodically if provided.
    phase is "downloading" or "processing".
    """
    try:
        import yt_dlp
    except ImportError:
        return False, "yt-dlp not installed", None

    output_template = str(output_dir / f"{filename_base}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": "best[ext=mp4]/best[ext=webm]/best",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "continuedl": True,        # Resume partial downloads
        "retries": 10,             # Retry on HTTP errors
        "fragment_retries": 10,    # Retry individual fragments
        "retry_sleep_functions": {"http": lambda n: min(2 ** n, 30)},  # Exponential backoff
    }

    if progress_callback:
        last_pct = [0]

        def hook(d):
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    pct = int(downloaded / total * 100)
                    if pct >= last_pct[0] + 2:
                        progress_callback(pct, "downloading")
                        last_pct[0] = pct
            elif d.get("status") == "finished":
                # Reset for next stream (audio after video)
                last_pct[0] = 0
                progress_callback(100, "downloading")

        def pp_hook(d):
            pp_status = d.get("status", "?")
            print(f"[Video Capture] pp_hook: {pp_status}", flush=True)
            if pp_status == "started":
                progress_callback(100, "processing")

        ydl_opts["progress_hooks"] = [hook]
        ydl_opts["postprocessor_hooks"] = [pp_hook]

    try:
        print(f"[Video Capture] yt-dlp extract_info starting...", flush=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"[Video Capture] yt-dlp extract_info returned, info={'yes' if info else 'None'}", flush=True)
            if info:
                # Try exact path first
                ext = info.get("ext", "mp4")
                actual_path = output_dir / f"{filename_base}.{ext}"
                print(f"[Video Capture] Checking file: {actual_path} exists={actual_path.exists()}", flush=True)
                if actual_path.exists():
                    return True, "", actual_path.name
                # Scan directory for files matching the filename_base
                # (yt-dlp may merge into a different extension)
                for f in output_dir.iterdir():
                    if f.is_file() and f.name.startswith(filename_base + "."):
                        print(f"[Video Capture] Found via scan: {f.name}", flush=True)
                        return True, "", f.name
                # List what's actually in the directory for debugging
                all_files = [f.name for f in output_dir.iterdir() if f.is_file()]
                print(f"[Video Capture] File not found! Looking for '{filename_base}.*' in: {all_files}", flush=True)
        return False, "yt-dlp download completed but file not found", None
    except Exception as e:
        print(f"[Video Capture] yt-dlp exception: {e}", flush=True)
        return False, f"yt-dlp error: {str(e)}", None


def find_ffmpeg() -> str | None:
    """Find ffmpeg binary path."""
    for ffmpeg_path in FFMPEG_PATHS:
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return ffmpeg_path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return None


def parse_video_path(video_path: str, base_dir: Path) -> tuple[Path, str]:
    """
    Parse and validate video path, returning (absolute_path, relative_path).

    Security: Prevents path traversal attacks.

    Args:
        video_path: Relative path like "media/assets/clips/clip_023.mp4"
        base_dir: Base directory for game files (e.g., angelas_desire/game/)

    Returns:
        Tuple of (resolved absolute path, sanitized relative path)

    Raises:
        ValueError: If path is invalid or attempts traversal
    """
    # Normalize and clean the path
    clean_path = video_path.replace("\\", "/")

    # Remove leading slash if present
    if clean_path.startswith("/"):
        clean_path = clean_path[1:]

    # Split into parts and filter dangerous segments
    parts = clean_path.split("/")
    safe_parts = []
    for part in parts:
        part = part.strip()
        if not part or part == "." or part == "..":
            continue
        # Allow alphanumeric, underscore, hyphen, and dots (for extension)
        if not re.match(r"^[\w\-\.]+$", part):
            raise ValueError(f"Invalid path segment: {part}")
        safe_parts.append(part)

    if not safe_parts:
        raise ValueError("Empty path after sanitization")

    # Build paths
    relative_path = "/".join(safe_parts)
    absolute_path = base_dir / relative_path

    # Resolve and verify it's under base_dir (prevent symlink attacks)
    try:
        resolved = absolute_path.resolve()
        base_resolved = base_dir.resolve()
        if not str(resolved).startswith(str(base_resolved)):
            raise ValueError("Path escapes base directory")
    except Exception as e:
        raise ValueError(f"Path resolution failed: {e}")

    return resolved, relative_path


@api_view(["POST"])
@permission_classes([AllowAny])
def media_capture(request):
    """
    Download media from URL to local game folder or downloads folder.

    Request body:
    {
        "url": "https://example.com/image.jpg",
        "scene_id": "bedroom_morning",
        "game": "step_sister_wedding"  // optional - if provided, saves to game/media/
    }

    Response:
    {
        "success": true,
        "file_path": "step_sister_wedding/media/bedroom_morning_20260120_143052.jpg"
    }
    """
    # Extract and validate input
    url = request.data.get("url")
    scene_id = request.data.get("scene_id", "unnamed")
    game = request.data.get("game")  # Optional game folder name

    if not url:
        return Response(
            {"success": False, "error": "URL is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate URL scheme
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        return Response(
            {"success": False, "error": "Invalid URL scheme (must be http or https)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Parse scene_id for subfolder support (e.g., "scenes/bedroom_test")
    subfolder, filename_base = parse_scene_path(scene_id)

    # Determine output directory based on game parameter
    if game:
        # Sanitize game name
        game = sanitize_path_segment(game)
        game_folder = GAMES_BASE_PATH / game

        # Validate game folder exists
        if not game_folder.exists() or not game_folder.is_dir():
            return Response(
                {"success": False, "error": f"Game folder not found: {game}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save into game's videos folder (the established media root)
        # Strip "videos/" prefix from subfolder to avoid videos/videos/ doubling
        media_subfolder = subfolder
        if media_subfolder and media_subfolder.startswith("videos/"):
            media_subfolder = media_subfolder[7:]  # strip "videos/"
        elif media_subfolder == "videos":
            media_subfolder = ""

        if media_subfolder:
            output_dir = game_folder / "videos" / media_subfolder
            relative_base = f"{game}/videos/{media_subfolder}"
        else:
            output_dir = game_folder / "videos"
            relative_base = f"{game}/videos"
    else:
        # Fallback to downloads folder (backward compatible)
        if subfolder:
            output_dir = DOWNLOADS_DIR / subfolder
            relative_base = f"downloads/{subfolder}"
        else:
            output_dir = DOWNLOADS_DIR
            relative_base = "downloads"

    # Create output directory (including any subfolders)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine if we should use yt-dlp
    use_ytdlp = is_video_platform(url)

    if use_ytdlp:
        # Try yt-dlp first for video platforms
        success, error, actual_filename = download_with_ytdlp(url, output_dir, filename_base)
        if success:
            relative_path = f"{relative_base}/{actual_filename}"
            return Response({"success": True, "file_path": relative_path})
        # If yt-dlp fails, we could try direct download as fallback
        # but for video platforms it's unlikely to work

    # Determine file extension from the actual source (not the TOML-requested ext).
    # The generator uses extension-agnostic matching (_find_media_file), so a GIF
    # saved for an .mp4 TOML slot will be found and rendered correctly.
    ext = get_extension_from_url(url)
    if not ext:
        # Try HEAD request for Content-Type
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            head_response = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
            ext = get_extension_from_content_type(head_response.headers.get("Content-Type", ""))
        except Exception:
            pass
    if not ext:
        ext = "jpg"  # Default to jpg for images

    if game:
        # Game workflow: overwrite any existing file with the same base name (any extension).
        # This prevents _1 suffixed orphans that the generator would never match.
        for existing in output_dir.iterdir() if output_dir.exists() else []:
            if existing.is_file() and existing.stem == filename_base:
                existing.unlink()
        filename = f"{filename_base}.{ext}"
        output_path = output_dir / filename
    else:
        # Downloads folder: keep unique naming to avoid accidental overwrites
        output_path, filename = get_unique_filepath(output_dir, filename_base, ext)

    # Try direct download
    success, error = download_direct(url, output_path)

    if success:
        relative_path = f"{relative_base}/{filename}"
        return Response({"success": True, "file_path": relative_path})

    # If direct download failed and we haven't tried yt-dlp yet, try it
    if not use_ytdlp:
        success, ytdlp_error, actual_filename = download_with_ytdlp(url, output_dir, filename_base)
        if success:
            relative_path = f"{relative_base}/{actual_filename}"
            return Response({"success": True, "file_path": relative_path})
        # Combine error messages
        error = f"Direct download: {error}. yt-dlp: {ytdlp_error}"

    return Response(
        {"success": False, "error": error},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def video_cut(request):
    """
    Cut/trim a video file using ffmpeg.

    Request body:
    {
        "video_path": "media/assets/clips/clip_023.mp4",  // Relative to game folder
        "start_time": 5.0,         // Start time in seconds
        "end_time": 15.0,          // End time in seconds
        "precise_mode": false,     // If true, use re-encoding for frame-accurate cuts
        "game": "angelas_desire"   // Optional: game folder name (default: angelas_desire)
    }

    Response (success):
    {
        "success": true,
        "backup_path": "media/assets/clips/clip_023.mp4.bak",
        "duration": 10.0,  // Duration of trimmed video
        "mode": "fast"     // "fast" (stream copy) or "precise" (re-encode)
    }

    Response (error):
    {
        "success": false,
        "error": "Error message"
    }
    """
    # Extract and validate input
    video_path = request.data.get("video_path")
    start_time = request.data.get("start_time")
    end_time = request.data.get("end_time")
    precise_mode = request.data.get("precise_mode", False)
    game = request.data.get("game", "angelas_desire")

    # Validate required fields
    if not video_path:
        return Response(
            {"success": False, "error": "video_path is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if start_time is None or end_time is None:
        return Response(
            {"success": False, "error": "start_time and end_time are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate time values
    try:
        start_time = float(start_time)
        end_time = float(end_time)
    except (TypeError, ValueError):
        return Response(
            {"success": False, "error": "start_time and end_time must be numbers"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if start_time < 0:
        return Response(
            {"success": False, "error": "start_time cannot be negative"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if start_time >= end_time:
        return Response(
            {"success": False, "error": "start_time must be less than end_time"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Find ffmpeg
    ffmpeg_cmd = find_ffmpeg()
    if not ffmpeg_cmd:
        return Response(
            {"success": False, "error": "ffmpeg not found. Install with: brew install ffmpeg"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Determine base directory
    game = sanitize_path_segment(game)
    game_dir = GAMES_BASE_PATH / game / "game"

    if not game_dir.exists() or not game_dir.is_dir():
        return Response(
            {"success": False, "error": f"Game folder not found: {game}/game"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Parse and validate video path
    try:
        absolute_path, relative_path = parse_video_path(video_path, game_dir)
    except ValueError as e:
        return Response(
            {"success": False, "error": f"Invalid video path: {e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check video exists
    if not absolute_path.exists():
        return Response(
            {"success": False, "error": f"Video file not found: {relative_path}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check it's actually a video file
    if absolute_path.suffix.lower() not in VALID_VIDEO_EXTENSIONS:
        return Response(
            {"success": False, "error": "File is not a supported video format"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create backup path (always keep backup)
    backup_path = absolute_path.with_suffix(absolute_path.suffix + ".bak")

    # If backup doesn't exist yet, create it (preserve original)
    if not backup_path.exists():
        try:
            shutil.copy2(absolute_path, backup_path)
        except Exception as e:
            return Response(
                {"success": False, "error": f"Failed to create backup: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Create temp output file
    temp_output = absolute_path.with_suffix(".temp" + absolute_path.suffix)

    # Calculate duration
    duration = end_time - start_time

    # Build ffmpeg command
    if precise_mode:
        # Precise mode: Re-encode for frame-accurate cutting
        # Slower but exact frame positioning
        cmd = [
            ffmpeg_cmd,
            "-y",  # Overwrite output
            "-i", str(absolute_path),
            "-ss", str(start_time),
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",  # High quality
            "-c:a", "aac",
            "-b:a", "128k",
            str(temp_output)
        ]
        mode_used = "precise"
    else:
        # Fast mode: Stream copy (keyframe-based cutting)
        # Very fast but may include a few extra frames
        cmd = [
            ffmpeg_cmd,
            "-y",  # Overwrite output
            "-ss", str(start_time),  # Seek BEFORE input for faster seeking
            "-i", str(absolute_path),
            "-t", str(duration),
            "-c", "copy",  # Stream copy (no re-encoding)
            "-avoid_negative_ts", "make_zero",
            str(temp_output)
        ]
        mode_used = "fast"

    try:
        # Run ffmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode != 0:
            # Clean up temp file if it exists
            if temp_output.exists():
                temp_output.unlink()
            return Response(
                {"success": False, "error": f"ffmpeg failed: {result.stderr[:500]}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Verify output exists and has content
        if not temp_output.exists() or temp_output.stat().st_size == 0:
            if temp_output.exists():
                temp_output.unlink()
            return Response(
                {"success": False, "error": "ffmpeg produced no output"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Replace original with trimmed version
        temp_output.replace(absolute_path)

        # Calculate relative backup path for response
        relative_backup = relative_path + ".bak"

        return Response({
            "success": True,
            "backup_path": relative_backup,
            "duration": round(duration, 2),
            "mode": mode_used
        })

    except subprocess.TimeoutExpired:
        if temp_output.exists():
            temp_output.unlink()
        return Response(
            {"success": False, "error": "ffmpeg timed out (5 minute limit)"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        if temp_output.exists():
            temp_output.unlink()
        return Response(
            {"success": False, "error": f"Unexpected error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# =============================================================================
# Canvas Approval Endpoints (file-based storage for tracking workflow)
# =============================================================================

APPROVAL_FILENAME = "canvas_approvals.json"


def get_approval_file_path(game: str) -> Path:
    """Get path to the approval JSON file for a game (inside game/ subdirectory)."""
    return GAMES_BASE_PATH / game / "game" / APPROVAL_FILENAME


def load_approvals(game: str) -> dict:
    """Load approval data from JSON file."""
    filepath = get_approval_file_path(game)
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_approvals(game: str, data: dict) -> bool:
    """Save approval data to JSON file."""
    filepath = get_approval_file_path(game)
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


@api_view(["GET"])
@permission_classes([AllowAny])
def canvas_approval_get(request):
    """
    Get approval status for a canvas or all canvases in a game.

    Query params:
    - game: Game folder name (required)
    - canvas_id: Specific canvas ID/slug (optional, returns all if not provided)

    Response:
    {
        "success": true,
        "approvals": {
            "activity_kitchen_angela_t8": {
                "status": "approved",
                "notes": "Looks good",
                "updated_at": "2024-..."
            },
            ...
        }
    }
    """
    game = request.query_params.get('game')
    canvas_id = request.query_params.get('canvas_id')

    if not game:
        return Response(
            {"success": False, "error": "game parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    game = sanitize_path_segment(game)
    game_folder = GAMES_BASE_PATH / game

    if not game_folder.exists():
        return Response(
            {"success": False, "error": f"Game folder not found: {game}"},
            status=status.HTTP_404_NOT_FOUND
        )

    approvals = load_approvals(game)

    if canvas_id:
        # Return single canvas approval
        canvas_data = approvals.get(canvas_id, {
            "status": "not_reviewed",
            "notes": "",
            "updated_at": None
        })
        return Response({
            "success": True,
            "canvas_id": canvas_id,
            "approval": canvas_data
        })

    # Return all approvals
    return Response({
        "success": True,
        "approvals": approvals
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def canvas_approval_update(request):
    """
    Update canvas approval status and review notes.

    Request body:
    {
        "game": "angelas_desire",
        "canvas_id": "activity_kitchen_angela_t8",
        "status": "approved" | "needs_changes" | "not_reviewed",
        "notes": "Optional review feedback"
    }

    Response:
    {
        "success": true,
        "canvas_id": "...",
        "status": "approved",
        "notes": "...",
        "updated_at": "..."
    }
    """
    game = request.data.get('game')
    canvas_id = request.data.get('canvas_id')
    approval_status = request.data.get('status')
    notes = request.data.get('notes', '')

    if not game:
        return Response(
            {"success": False, "error": "game is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not canvas_id:
        return Response(
            {"success": False, "error": "canvas_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Reject canvas IDs that look like unprocessed SugarCube templates
    if '<<' in canvas_id or '>>' in canvas_id:
        return Response(
            {"success": False, "error": "Invalid canvas_id - appears to be unprocessed template variable"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not approval_status:
        return Response(
            {"success": False, "error": "status is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    valid_statuses = ['approved', 'needs_changes', 'not_reviewed']
    if approval_status not in valid_statuses:
        return Response(
            {"success": False, "error": f"Invalid status. Must be one of: {valid_statuses}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    game = sanitize_path_segment(game)
    game_folder = GAMES_BASE_PATH / game

    if not game_folder.exists():
        return Response(
            {"success": False, "error": f"Game folder not found: {game}"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Load existing approvals
    approvals = load_approvals(game)

    # Update this canvas
    updated_at = datetime.now().isoformat()
    approvals[canvas_id] = {
        "status": approval_status,
        "notes": notes,
        "updated_at": updated_at
    }

    # Save
    if not save_approvals(game, approvals):
        return Response(
            {"success": False, "error": "Failed to save approval data"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        "success": True,
        "canvas_id": canvas_id,
        "status": approval_status,
        "notes": notes,
        "updated_at": updated_at
    })


VIDEOS_DIR = Path(settings.BASE_DIR) / "videos"


def sanitize_folder_name(name: str) -> str:
    """Sanitize a folder name, allowing spaces but blocking traversal and dangerous chars."""
    # Block path traversal
    name = name.replace("..", "").replace("/", "").replace("\\", "").replace("\x00", "")
    # Strip leading/trailing dots and whitespace
    name = name.strip(". ")
    return name or "unnamed"


def get_next_counter(output_dir: Path) -> int:
    """Scan folder for highest existing counter prefix and return next value."""
    max_counter = 0
    if output_dir.exists():
        for f in output_dir.iterdir():
            if f.is_file():
                # Match files starting with digits followed by underscore or dot
                match = re.match(r"^(\d+)[_.]", f.name)
                if match:
                    max_counter = max(max_counter, int(match.group(1)))
    return max_counter + 1


def get_basename_from_url(url: str) -> str | None:
    """Extract a useful filename base from a URL path."""
    parsed = urlparse(url)
    path_part = parsed.path.rstrip("/")
    if not path_part or path_part == "/":
        return None
    basename = path_part.rsplit("/", 1)[-1]
    # Strip extension
    if "." in basename:
        basename = basename.rsplit(".", 1)[0]
    # Sanitize: allow alphanumeric, underscore, hyphen
    basename = re.sub(r"[^a-zA-Z0-9_-]", "_", basename)
    # Collapse multiple underscores
    basename = re.sub(r"_+", "_", basename).strip("_")
    return basename if basename and len(basename) > 1 else None


DOWNLOAD_LOG_FILE = VIDEOS_DIR / ".download_log.json"
PROGRESS_DIR = VIDEOS_DIR / ".progress"


def write_progress(task_id: str, data: dict):
    """Write progress data to a task-specific JSON file."""
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    progress_file = PROGRESS_DIR / f"{task_id}.json"
    progress_file.write_text(json.dumps(data))


def cleanup_old_progress():
    """Delete progress files older than 5 minutes."""
    if not PROGRESS_DIR.exists():
        return
    cutoff = time.time() - 300
    for f in PROGRESS_DIR.iterdir():
        if f.is_file() and f.stat().st_mtime < cutoff:
            f.unlink(missing_ok=True)


def load_download_log() -> dict:
    """Load the download log from disk."""
    if DOWNLOAD_LOG_FILE.exists():
        try:
            return json.loads(DOWNLOAD_LOG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_download_log(log: dict):
    """Save the download log to disk."""
    DOWNLOAD_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_LOG_FILE.write_text(json.dumps(log, indent=2))


def log_download(url: str, file_path: str):
    """Record a successful download in the log."""
    log = load_download_log()
    log[url] = {
        "file_path": file_path,
        "downloaded_at": datetime.now().isoformat(),
    }
    save_download_log(log)


def _do_download(url, output_dir, relative_base, filename_base, use_ytdlp, task_id):
    """Background thread: performs the actual download and logs the result."""
    short_url = url[:80] + ("..." if len(url) > 80 else "")
    print(f"[Video Capture] ⏳ Starting download: {short_url}", flush=True)
    cleanup_old_progress()
    write_progress(task_id, {"status": "downloading", "percent": 0})

    def on_progress(pct, phase="downloading"):
        write_progress(task_id, {"status": phase, "percent": pct})

    try:
        if use_ytdlp:
            print(f"[Video Capture] Using yt-dlp...", flush=True)
            success, error, actual_filename = download_with_ytdlp(url, output_dir, filename_base, progress_callback=on_progress)
            if success:
                file_path = f"{relative_base}/{actual_filename}"
                log_download(url, file_path)
                write_progress(task_id, {"status": "done", "file_path": file_path})
                print(f"[Video Capture] ✓ Downloaded: {file_path}", flush=True)
                return

        # Detect extension
        ext = get_extension_from_url(url)
        if not ext:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                head_response = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
                ext = get_extension_from_content_type(head_response.headers.get("Content-Type", ""))
            except Exception:
                pass
        if not ext:
            ext = "mp4" if use_ytdlp else "jpg"

        output_path, filename = get_unique_filepath(output_dir, filename_base, ext)
        success, error = download_direct(url, output_path, progress_callback=on_progress)

        if success:
            file_path = f"{relative_base}/{filename}"
            log_download(url, file_path)
            write_progress(task_id, {"status": "done", "file_path": file_path})
            print(f"[Video Capture] ✓ Downloaded: {file_path}", flush=True)
            return

        # If direct failed and haven't tried yt-dlp, try it
        if not use_ytdlp:
            print(f"[Video Capture] Direct failed, trying yt-dlp...", flush=True)
            success, ytdlp_error, actual_filename = download_with_ytdlp(url, output_dir, filename_base, progress_callback=on_progress)
            if success:
                file_path = f"{relative_base}/{actual_filename}"
                log_download(url, file_path)
                write_progress(task_id, {"status": "done", "file_path": file_path})
                print(f"[Video Capture] ✓ Downloaded: {file_path}", flush=True)
                return
            error = f"Direct: {error}. yt-dlp: {ytdlp_error}"

        write_progress(task_id, {"status": "error", "error": error})
        print(f"[Video Capture] ✗ Failed: {short_url} — {error}", flush=True)

    except Exception as e:
        write_progress(task_id, {"status": "error", "error": str(e)})
        print(f"[Video Capture] ✗ Exception: {short_url} — {e}", flush=True)


@api_view(["POST"])
@permission_classes([AllowAny])
def video_capture(request):
    """
    Async download media from URL to a named subfolder under ./videos/.
    Returns immediately while download proceeds in background.

    Request body:
    {
        "url": "https://example.com/clip.mp4",
        "folder": "angela white"
    }

    Response (started):
    {"success": true, "message": "Download started...", "async": true}

    Response (duplicate):
    {"success": false, "duplicate": true, "file_path": "videos/...", "error": "Already downloaded"}
    """
    url = request.data.get("url")
    folder = request.data.get("folder")

    if not url:
        return Response(
            {"success": False, "error": "URL is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not folder or not folder.strip():
        return Response(
            {"success": False, "error": "Folder name is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate URL scheme
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        return Response(
            {"success": False, "error": "Invalid URL scheme (must be http or https)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check duplicate
    download_log = load_download_log()
    if url in download_log:
        entry = download_log[url]
        return Response({
            "success": False,
            "duplicate": True,
            "file_path": entry["file_path"],
            "error": f"Already downloaded: {entry['file_path']}",
        })

    # Sanitize folder name (allows spaces)
    folder = sanitize_folder_name(folder)
    output_dir = VIDEOS_DIR / folder
    output_dir.mkdir(parents=True, exist_ok=True)

    # Verify path doesn't escape videos dir
    resolved = output_dir.resolve()
    if not str(resolved).startswith(str(VIDEOS_DIR.resolve())):
        return Response(
            {"success": False, "error": "Invalid folder path"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    relative_base = f"videos/{folder}"

    # Build counter-based filename
    use_ytdlp = is_video_platform(url)
    counter = get_next_counter(output_dir)
    url_basename = get_basename_from_url(url)

    if url_basename:
        filename_base = f"{counter:03d}_{url_basename}"
    else:
        filename_base = f"{counter:03d}"

    # Generate task ID for progress tracking
    task_id = str(uuid4())[:8]

    # Start download in background thread
    thread = threading.Thread(
        target=_do_download,
        args=(url, output_dir, relative_base, filename_base, use_ytdlp, task_id),
        daemon=True,
    )
    thread.start()

    return Response({
        "success": True,
        "task_id": task_id,
        "message": f"Download started → {relative_base}/",
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def video_capture_progress(request, task_id):
    """Get download progress for a given task ID."""
    # Sanitize task_id
    task_id = re.sub(r"[^a-zA-Z0-9-]", "", task_id)
    progress_file = PROGRESS_DIR / f"{task_id}.json"

    if not progress_file.exists():
        return Response({"status": "unknown"})

    try:
        data = json.loads(progress_file.read_text())
        return Response(data)
    except (json.JSONDecodeError, OSError):
        return Response({"status": "unknown"})


urlpatterns = [
    path("media-capture", media_capture, name="media_capture"),
    path("video-cut", video_cut, name="video_cut"),
    path("video-capture", video_capture, name="video_capture"),
    path("video-capture/progress/<str:task_id>", video_capture_progress, name="video_capture_progress"),
    # Canvas approval endpoints (file-based)
    path("canvas-approval", canvas_approval_get, name="canvas_approval_get"),
    path("canvas-approval/update", canvas_approval_update, name="canvas_approval_update"),
]
