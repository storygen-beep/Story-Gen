"""
Processing pipeline for Asset Videos: scene split, frame sampling, JoyCaption2 captions.

Synchronous best-effort pipeline suitable for development use. Relies on
OpenCV for probing/frames and optionally PySceneDetect/ffmpeg for scenes. If
scene detection isn't available, falls back to a single clip covering the
entire video and samples frames at a fixed interval.
"""

from __future__ import annotations

import os
import math
import shutil
from pathlib import Path
import tempfile
from typing import Optional, List, Tuple

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.utils import timezone

from ..models import AssetVideo, AssetVideoStatus, AssetClip, ClipFrame
from .grok_clip_service import get_grok_client


DEFAULT_FRAME_INTERVAL_SEC = 2

# Scene detection configuration
# Lower threshold = more sensitive to scene changes (detects subtler transitions)
# Higher threshold = only detects hard cuts (abrupt changes)
# Recommended: 5.0-10.0 for most videos, 15.0+ for only hard cuts
SCENE_DETECTION_THRESHOLD = 10.0

# Minimum scene length in SECONDS (will be converted to frames based on actual FPS)
# This ensures clips are at least 5 seconds long for better usability
SCENE_MIN_LENGTH_SEC = 5.0


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _owner_video_base_dir(video: AssetVideo) -> Path:
    """Return a temporary working directory for processing this video.

    Use a temp directory rather than MEDIA_ROOT so that processing works
    with remote storage backends (e.g., Cloudflare R2 via django-storages).
    """
    owner_id = str(video.group.owner_id)
    vid = str(video.id)
    base = Path(tempfile.gettempdir()) / "assets_processing" / owner_id / vid
    _ensure_dir(base)
    return base


def _download_to_tempfile(storage_name: str, suffix: str = "") -> Path:
    """Download a stored file by its storage name to a local temp file.

    Returns the local Path to the downloaded file. Caller is responsible
    for cleanup when appropriate.
    """
    # NamedTemporaryFile with delete=False so downstream libs can reopen by path
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path = Path(tmp.name)
    with default_storage.open(storage_name, "rb") as src:
        shutil.copyfileobj(src, tmp)
    tmp.close()
    return tmp_path


def _probe_metadata(video_path: str) -> Tuple[int, int, float]:
    import cv2  # type: ignore

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0) or 30.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = float(frame_count) / float(fps) if fps > 0 and frame_count > 0 else 0.0
    cap.release()
    return width, height, duration


def _extract_frame(video_path: str, timestamp_sec: float, out_path: Path) -> bool:
    import cv2  # type: ignore

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0) or 30.0
    frame_index = max(0, int(round(timestamp_sec * fps)))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return False
    _ensure_dir(out_path.parent)
    ok = cv2.imwrite(str(out_path), frame)
    cap.release()
    return bool(ok)


def _detect_fps(video_path: str) -> float:
    """Detect video FPS using ffprobe.

    Returns:
        FPS as float. Defaults to 30.0 if detection fails.
    """
    import subprocess
    from fractions import Fraction
    import logging

    logger = logging.getLogger(__name__)

    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=r_frame_rate', '-of',
             'default=noprint_wrappers=1:nokey=1', video_path],
            capture_output=True, text=True, check=True, timeout=10
        )
        fps_str = result.stdout.strip()
        fps = float(Fraction(fps_str)) if '/' in fps_str else float(fps_str)
        logger.info(f"Detected video FPS: {fps:.2f}")
        return fps
    except Exception as e:
        logger.warning(f"Could not detect FPS for {video_path}: {e}. Using default 30.0 fps")
        return 30.0


def _split_scenes(
    video_path: str,
    min_scene_length: float = SCENE_MIN_LENGTH_SEC,
    threshold: float = SCENE_DETECTION_THRESHOLD
) -> Tuple[List[Tuple[float, float]], List]:
    """Return list of (start_sec, end_sec) scene segments and raw scene_list for FFmpeg.

    Args:
        video_path: Path to video file
        min_scene_length: Minimum scene length in seconds (default: 5.0)
        threshold: Scene detection threshold (default: 10.0)

    Returns:
        Tuple of (segments, scene_list) where:
        - segments: List of (start_sec, end_sec) tuples
        - scene_list: Raw scene list for split_video_ffmpeg()
    """
    import logging
    logger = logging.getLogger(__name__)

    # Auto-detect FPS and convert minimum scene length from seconds to frames
    fps = _detect_fps(video_path)
    min_scene_frames = int(min_scene_length * fps)

    logger.info(f"Starting scene detection with threshold={threshold}, min_scene_len={min_scene_length}s ({min_scene_frames} frames at {fps:.2f} fps)")

    try:
        # Try importing PySceneDetect
        try:
            from scenedetect import VideoManager, SceneManager  # type: ignore
            from scenedetect.detectors import ContentDetector  # type: ignore
            logger.info("PySceneDetect imported successfully")
        except ImportError as e:
            logger.error(f"PySceneDetect import failed: {e}. Scene detection unavailable.", exc_info=True)
            return [], []

        # Initialize scene detection
        try:
            video_manager = VideoManager([video_path])
            scene_manager = SceneManager()
            scene_manager.add_detector(
                ContentDetector(
                    threshold=threshold,
                    min_scene_len=min_scene_frames
                )
            )
            base_timecode = video_manager.get_base_timecode()
            logger.info("Scene detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize scene detector: {e}", exc_info=True)
            return [], []

        # Run scene detection (matching TripleX working pattern)
        try:
            video_manager.start()
            logger.info("VideoManager started, beginning scene detection...")
            scene_manager.detect_scenes(frame_source=video_manager)
            scene_list = scene_manager.get_scene_list(base_timecode)
            logger.info(f"Scene detection completed. Raw scenes detected: {len(scene_list)}")
        except Exception as e:
            logger.error(f"Scene detection execution failed: {e}", exc_info=True)
            return [], []
        finally:
            # Explicitly release video resources (critical for proper cleanup)
            video_manager.release()
            logger.debug("VideoManager resources released")

        # Convert to seconds
        segments: List[Tuple[float, float]] = []
        for idx, (start, end) in enumerate(scene_list):
            start_sec = start.get_seconds()
            end_sec = end.get_seconds()
            duration = end_sec - start_sec
            segments.append((start_sec, end_sec))
            logger.debug(f"Scene {idx}: {start_sec:.2f}s - {end_sec:.2f}s (duration: {duration:.2f}s)")

        if segments:
            logger.info(f"Successfully detected {len(segments)} scene(s) after filtering")
            return segments, scene_list
        else:
            logger.warning(f"No scenes passed filtering criteria (threshold={threshold}, min_scene_len={min_scene_length}s / {min_scene_frames} frames)")
            return [], []

    except Exception as e:
        # Catch-all for any unexpected errors
        logger.error(f"Unexpected error during scene detection: {e}", exc_info=True)
        return [], []


def _joycaption2_generate(image_path: Path) -> Optional[str]:
    """Best-effort JoyCaption2 caption. Returns caption or None if unavailable."""
    try:
        # Add TripleX to path to reuse local captioner if available
        import sys
        base_dir = Path(__file__).resolve().parents[3]  # story_gen_django/
        triplex = base_dir.parent / "TripleX"
        if triplex.exists() and str(triplex) not in sys.path:
            sys.path.insert(0, str(triplex))
        # Import the local captioner
        from captioners.joycaption2 import describe_image  # type: ignore

        # describe_image writes a .txt next to the image; we also want the content
        # For now, read the file after it runs.
        describe_image(str(image_path))
        txt = image_path.with_suffix('.txt')
        if txt.exists():
            return txt.read_text(encoding='utf-8').strip()
    except Exception:
        return None
    return None


def process_video_sync(
    video: AssetVideo,
    frame_interval: int = DEFAULT_FRAME_INTERVAL_SEC,
    min_scene_length: float = SCENE_MIN_LENGTH_SEC,
    threshold: float = SCENE_DETECTION_THRESHOLD
) -> Optional[str]:
    """Process an uploaded video end-to-end. Returns error string if failed.

    Args:
        video: AssetVideo instance to process
        frame_interval: Seconds between frame samples (default: 2.0)
        min_scene_length: Minimum scene length in seconds (default: 5.0)
        threshold: Scene detection threshold (default: 10.0)

    Steps:
      - Probe metadata (OpenCV)
      - Extract poster
      - Detect scenes and split to clips (fallback: single full-length clip)
      - Sample frames every N seconds
      - Caption with JoyCaption2 when available
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        # Initialize processing
        video.status = AssetVideoStatus.PROCESSING
        video.error = ""
        video.processing_stage = "Initializing"
        video.processing_progress = 0
        video.save(update_fields=["status", "error", "processing_stage", "processing_progress"])
        logger.info(f"Starting video processing for {video.id}")

        # Access source video via storage (works for local or remote)
        video.processing_stage = "Downloading video"
        video.processing_progress = 10
        video.save(update_fields=["processing_stage", "processing_progress"])

        src_name = video.file.name
        suffix = Path(src_name).suffix or ".mp4"
        src_path = _download_to_tempfile(src_name, suffix=suffix)
        base_dir = _owner_video_base_dir(video)
        posters_dir = base_dir / "posters"
        clips_dir = base_dir / "clips"
        frames_dir = base_dir / "frames"
        _ensure_dir(posters_dir)
        _ensure_dir(clips_dir)
        _ensure_dir(frames_dir)
        logger.info(f"Video downloaded to {src_path}")

        # Metadata
        video.processing_stage = "Extracting metadata"
        video.processing_progress = 20
        video.save(update_fields=["processing_stage", "processing_progress"])

        width, height, duration = _probe_metadata(str(src_path))
        video.width = width
        video.height = height
        video.duration_sec = duration
        logger.info(f"Video metadata: {width}x{height}, {duration}s")

        # Video poster at ~1s (or 0)
        video.processing_stage = "Generating poster"
        video.processing_progress = 30
        video.save(update_fields=["processing_stage", "processing_progress"])

        poster_path = posters_dir / "video.jpg"
        if not _extract_frame(str(src_path), min(1.0, duration or 0.0), poster_path):
            # fallback to 0
            _extract_frame(str(src_path), 0.0, poster_path)
        if poster_path.exists():
            with open(poster_path, "rb") as f:
                video.poster.save(poster_path.name, File(f), save=False)
        video.save(update_fields=["width", "height", "duration_sec", "poster"])
        logger.info("Poster generated successfully")

        # Scenes (fallback to single segment)
        video.processing_stage = "Detecting scenes"
        video.processing_progress = 40
        video.save(update_fields=["processing_stage", "processing_progress"])

        segments, scene_list = _split_scenes(str(src_path), min_scene_length=min_scene_length, threshold=threshold)

        if not segments:
            logger.warning("Scene detection returned no scenes - using full video as single segment")
            segments = [(0.0, float(duration or 0.0))]
            scene_list = []
            logger.info(f"Fallback: Created 1 segment covering full {duration:.2f}s duration")
        else:
            total_duration = sum(end - start for start, end in segments)
            logger.info(f"Successfully detected {len(segments)} scene(s) covering {total_duration:.2f}s of {duration:.2f}s video")
            for idx, (start, end) in enumerate(segments):
                logger.debug(f"  Segment {idx}: {start:.2f}s - {end:.2f}s ({end - start:.2f}s)")

        # Use FFmpeg to slice video into actual clips
        video.processing_stage = "Splitting video into clips"
        video.processing_progress = 50
        video.save(update_fields=["processing_stage", "processing_progress"])

        if scene_list:
            try:
                from scenedetect.video_splitter import split_video_ffmpeg  # type: ignore
                logger.info(f"Using FFmpeg to split video into {len(scene_list)} clips...")
                split_video_ffmpeg([str(src_path)], scene_list, output_dir=str(clips_dir), suppress_output=True)
                logger.info("FFmpeg video splitting completed successfully")
            except Exception as e:
                # Fallback: if FFmpeg fails, copy entire video as single clip
                logger.error(f"FFmpeg split failed: {e}", exc_info=True)
                logger.warning("Falling back to copying full video as single clip")
                import shutil
                clip_path = clips_dir / "scene_000.mp4"
                shutil.copyfile(str(src_path), clip_path)
                logger.info(f"Fallback clip created: {clip_path}")
        else:
            # No scenes detected, copy entire video as single clip
            logger.info("No scenes detected - copying full video as single clip (no splitting needed)")
            import shutil
            clip_path = clips_dir / "scene_000.mp4"
            shutil.copyfile(str(src_path), clip_path)
            logger.info(f"Single clip created: {clip_path} ({duration:.2f}s)")

        # Create clip records for each generated clip file
        video.processing_stage = "Creating clip records"
        video.processing_progress = 70
        video.save(update_fields=["processing_stage", "processing_progress"])

        clip_files = sorted(clips_dir.glob("*.mp4"))
        logger.info(f"Found {len(clip_files)} clip file(s) to process")

        # Keep track of temp file paths for frame extraction (not stored in DB)
        temp_file_mapping = {}

        for idx, clip_path in enumerate(clip_files):
            # Get segment info if available
            if idx < len(segments):
                start, end = segments[idx]
                seg_duration = max(0.0, (end - start))
            else:
                start, end = 0.0, float(duration or 0.0)
                seg_duration = float(duration or 0.0)

            # Create clip and upload to R2 immediately
            clip = AssetClip.objects.create(
                video=video,
                index=idx,
                start_sec=float(start),
                end_sec=float(end),
                duration_sec=float(seg_duration),
            )

            # Upload clip file to R2 storage
            try:
                with open(clip_path, 'rb') as f:
                    clip.file.save(f"clip_{idx:03d}.mp4", File(f), save=True)
                logger.info(f"Uploaded clip {idx} to R2 storage")
            except Exception as e:
                logger.error(f"Failed to upload clip {idx} to R2: {e}", exc_info=True)
                raise

            # Clip poster (extract from temp file before cleanup)
            cposter = posters_dir / f"clip_{idx:03d}.jpg"
            if _extract_frame(str(clip_path), 0.0, cposter):
                with open(cposter, "rb") as f:
                    clip.poster.save(cposter.name, File(f), save=True)

            # Store temp file path for frame extraction (not in DB)
            temp_file_mapping[clip.id] = str(clip_path)

        # Finalize
        logger.info(f"Created {len(clip_files)} clip(s)")

        # Frame extraction and captioning
        if settings.ASSET_FRAME_EXTRACTION["enabled"]:
            video.processing_stage = "Extracting frames"
            video.processing_progress = 85
            video.save(update_fields=["processing_stage", "processing_progress"])

            from apps.assets.services.frame_captioning import FrameCaptioningService

            logger.info(f"Starting frame extraction and captioning for {len(clip_files)} clips")

            total_frames_created = 0
            total_frames_captioned = 0
            total_frames_pending = 0

            for idx, clip in enumerate(video.clips.all()):
                # Get temp file path from mapping (not stored in DB anymore)
                temp_path = temp_file_mapping.get(clip.id)
                if not temp_path or not os.path.exists(temp_path):
                    logger.warning(f"Skipping clip {clip.id}: temp file not found")
                    continue

                try:
                    result = FrameCaptioningService.extract_and_caption_clip(
                        clip=clip,
                        video_file_path=temp_path,
                        config=settings.ASSET_FRAME_EXTRACTION
                    )

                    total_frames_created += result["frames_created"]
                    total_frames_captioned += result["frames_captioned"]
                    total_frames_pending += result["frames_pending"]

                    # Update progress
                    progress = 85 + int((idx + 1) / len(clip_files) * 10)
                    video.processing_progress = min(progress, 95)
                    video.save(update_fields=["processing_progress"])

                except Exception as e:
                    logger.error(f"Frame extraction failed for clip {clip.id}: {e}", exc_info=True)
                    # Continue with other clips

            logger.info(
                f"Frame extraction complete: {total_frames_created} frames created, "
                f"{total_frames_captioned} captioned, {total_frames_pending} pending"
            )

        # Generate clip descriptions using Grok AI
        grok_client = get_grok_client()
        if grok_client.is_available():
            logger.info(f"Generating clip descriptions for video {video.id}")

            # Update progress
            video.processing_stage = "Generating clip descriptions"
            video.processing_progress = 95
            video.save(update_fields=["processing_stage", "processing_progress"])

            clips = video.clips.all()
            total_clips = clips.count()

            for idx, clip in enumerate(clips):
                try:
                    # Generate description
                    description = grok_client.generate_description(clip)

                    if description:
                        clip.description = description
                        clip.description_model = grok_client.model
                        clip.description_generated_at = timezone.now()
                        clip.save(update_fields=[
                            'description',
                            'description_model',
                            'description_generated_at'
                        ])
                        logger.info(f"Generated description for clip {clip.id} ({idx+1}/{total_clips})")
                    else:
                        logger.info(f"Skipped description for clip {clip.id} (insufficient frames)")

                except Exception as e:
                    # Log error but continue processing other clips
                    clip.description_error = str(e)
                    clip.save(update_fields=['description_error'])
                    logger.error(
                        f"Failed to generate description for clip {clip.id}: {e}",
                        exc_info=True
                    )
                    # Continue with other clips

            logger.info(f"Completed clip description generation for video {video.id}")
        else:
            logger.info("Grok clip descriptions disabled or unavailable, skipping")

        # Clean up temp files (clips now uploaded to R2)
        logger.info(f"Cleaning up temp files for video {video.id}")
        owner_id = str(video.group.owner_id)
        vid = str(video.id)
        temp_base = Path(tempfile.gettempdir()) / "assets_processing" / owner_id / vid
        if temp_base.exists():
            import shutil
            shutil.rmtree(temp_base, ignore_errors=True)
            logger.info(f"Cleaned up temp directory: {temp_base}")

        # Finalization
        video.processing_stage = "Finalizing"
        video.processing_progress = 95
        video.save(update_fields=["processing_stage", "processing_progress"])

        video.status = AssetVideoStatus.COMPLETE
        video.processing_stage = "Complete"
        video.processing_progress = 100
        video.save(update_fields=["status", "processing_stage", "processing_progress"])
        logger.info(f"Video processing completed successfully for {video.id}")
        return None
    except ImportError as e:
        # Specific handling for missing dependencies
        error_msg = f"Missing required dependencies: {str(e)}. Please ensure OpenCV and PySceneDetect are installed."
        logger.error(f"Import error during video processing: {error_msg}", exc_info=True)
        video.status = AssetVideoStatus.FAILED
        video.error = error_msg
        video.processing_stage = "Failed"
        video.save(update_fields=["status", "error", "processing_stage"])
        return error_msg
    except Exception as e:  # pragma: no cover - safety catch
        # User-friendly error messages
        error_msg = str(e)
        if "libGL" in error_msg:
            error_msg = "OpenCV system libraries not available. Please contact administrator."
        elif "FFmpeg" in error_msg or "ffmpeg" in error_msg:
            error_msg = "FFmpeg not available for video processing. Please contact administrator."
        elif "Permission" in error_msg:
            error_msg = "File permission error during processing."
        elif "No space" in error_msg or "Disk" in error_msg:
            error_msg = "Insufficient disk space for processing."

        logger.error(f"Video processing failed for {video.id}: {e}", exc_info=True)
        video.status = AssetVideoStatus.FAILED
        video.error = error_msg[:500]  # Truncate for DB field
        video.processing_stage = "Failed"
        video.save(update_fields=["status", "error", "processing_stage"])
        return error_msg


def recaption_frame_sync(frame: ClipFrame) -> Optional[str]:
    """DISABLED: Regenerate caption for a single frame using JoyCaption2 when available."""
    # Captioning is currently disabled
    return "Captioning is currently disabled"
    # try:
    #     if not frame.image_file or not frame.image_file.name:
    #         return "Missing frame image"
    #     frame.status = "processing"
    #     frame.error = ""
    #     frame.save(update_fields=["status", "error"])
    #     # Download image to a local temp path for captioning
    #     img_name = frame.image_file.name
    #     img_suffix = Path(img_name).suffix or ".jpg"
    #     local_img = _download_to_tempfile(img_name, suffix=img_suffix)
    #     caption = _joycaption2_generate(local_img)
    #     if caption:
    #         frame.caption_text = caption
    #         frame.status = "complete"
    #         frame.save(update_fields=["caption_text", "status"])
    #         return None
    #     frame.status = "pending"
    #     frame.save(update_fields=["status"])
    #     return None
    # except Exception as e:
    #     frame.status = "failed"
    #     frame.error = str(e)
    #     frame.save(update_fields=["status", "error"])
    #     return str(e)
