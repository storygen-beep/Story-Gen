"""
Frame extraction and captioning service for asset library.

This service extracts frames from video clips and generates captions using vLLM.
Frames are extracted in-memory (no file storage) and captions are saved to database.
"""
import logging
from typing import Dict, List
import cv2

from django.conf import settings

from apps.assets.models import AssetClip, ClipFrame
from apps.assets.services.vllm_captioning import get_vllm_client
from apps.assets.services.processing import _probe_metadata

logger = logging.getLogger(__name__)


class FrameCaptioningService:
    """Service for extracting frames and generating captions."""

    @staticmethod
    def extract_and_caption_clip(
        clip: AssetClip,
        video_file_path: str,
        config: dict
    ) -> dict:
        """Extract frames from clip and caption via vLLM.

        Args:
            clip: AssetClip instance
            video_file_path: Path to video file (temp_file_path)
            config: ASSET_FRAME_EXTRACTION configuration dict

        Returns:
            {
                "frames_created": int,
                "frames_captioned": int,
                "frames_pending": int,
                "frames_failed": int,
                "errors": list[str]
            }
        """
        errors = []

        # Step 1: Extract frames
        try:
            frame_data = FrameCaptioningService.extract_frames_for_clip(
                clip=clip,
                video_file_path=video_file_path,
                interval_sec=config.get("frame_interval_sec", 2.0)
            )
        except Exception as e:
            logger.error(f"Frame extraction failed for clip {clip.id}: {e}", exc_info=True)
            errors.append(f"Frame extraction failed: {str(e)}")
            return {
                "frames_created": 0,
                "frames_captioned": 0,
                "frames_pending": 0,
                "frames_failed": 0,
                "errors": errors
            }

        if not frame_data:
            logger.warning(f"No frames extracted from clip {clip.id}")
            return {
                "frames_created": 0,
                "frames_captioned": 0,
                "frames_pending": 0,
                "frames_failed": 0,
                "errors": errors
            }

        # Step 2: Caption frames via vLLM
        try:
            caption_results = FrameCaptioningService.caption_frames_batch(
                frame_data=frame_data,
                batch_size=config.get("caption_batch_size", 4)
            )
        except Exception as e:
            logger.error(f"Captioning failed for clip {clip.id}: {e}", exc_info=True)
            errors.append(f"Captioning failed: {str(e)}")
            # Create frames with pending status if captioning fails
            caption_results = [
                {
                    "timestamp_sec": fd["timestamp_sec"],
                    "caption": "",
                    "error": str(e)
                }
                for fd in frame_data
            ]

        # Step 3: Create ClipFrame records
        try:
            created_frames = FrameCaptioningService.create_frame_records(
                clip=clip,
                caption_results=caption_results
            )
        except Exception as e:
            logger.error(f"Failed to create frame records for clip {clip.id}: {e}", exc_info=True)
            errors.append(f"Database error: {str(e)}")
            return {
                "frames_created": 0,
                "frames_captioned": 0,
                "frames_pending": 0,
                "frames_failed": 0,
                "errors": errors
            }

        # Step 4: Calculate statistics
        frames_captioned = sum(1 for f in created_frames if f.status == "complete")
        frames_pending = sum(1 for f in created_frames if f.status == "pending")
        frames_failed = sum(1 for f in created_frames if f.status == "failed")

        logger.info(
            f"Clip {clip.id}: {len(created_frames)} frames created, "
            f"{frames_captioned} captioned, {frames_pending} pending, {frames_failed} failed"
        )

        return {
            "frames_created": len(created_frames),
            "frames_captioned": frames_captioned,
            "frames_pending": frames_pending,
            "frames_failed": frames_failed,
            "errors": errors
        }

    @staticmethod
    def extract_frames_for_clip(
        clip: AssetClip,
        video_file_path: str,
        interval_sec: float
    ) -> List[dict]:
        """Extract frames at intervals using OpenCV (in-memory, no file storage).

        Args:
            clip: AssetClip instance
            video_file_path: Path to video file
            interval_sec: Time interval between frames in seconds

        Returns:
            List of dicts: [{"timestamp_sec": float, "image_data": bytes}, ...]
        """
        # Get video metadata
        try:
            width, height, duration = _probe_metadata(video_file_path)
        except Exception as e:
            logger.error(f"Failed to probe metadata for {video_file_path}: {e}")
            raise

        if duration <= 0:
            logger.warning(f"Invalid duration ({duration}) for {video_file_path}")
            return []

        # Calculate timestamps
        timestamps = []
        current = 0.0
        max_frames = 100  # Safety limit
        while current <= duration and len(timestamps) < max_frames:
            timestamps.append(current)
            current += interval_sec

        if not timestamps:
            return []

        # Extract frames using OpenCV
        frame_data = []
        cap = cv2.VideoCapture(video_file_path)

        if not cap.isOpened():
            logger.error(f"Could not open video: {video_file_path}")
            cap.release()
            raise RuntimeError(f"Could not open video: {video_file_path}")

        try:
            for ts in timestamps:
                # Seek to timestamp
                cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
                ret, frame = cap.read()

                if not ret:
                    logger.warning(f"Failed to extract frame at {ts}s from {video_file_path}")
                    continue

                # Encode frame to JPEG bytes
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    logger.warning(f"Failed to encode frame at {ts}s")
                    continue

                frame_data.append({
                    "timestamp_sec": ts,
                    "image_data": buffer.tobytes()
                })

        finally:
            cap.release()

        logger.info(f"Extracted {len(frame_data)} frames from clip {clip.id}")
        return frame_data

    @staticmethod
    def caption_frames_batch(
        frame_data: List[dict],
        batch_size: int = 4
    ) -> List[dict]:
        """Batch caption frames via vLLM.

        Args:
            frame_data: List of dicts with "timestamp_sec" and "image_data"
            batch_size: Number of concurrent requests to vLLM

        Returns:
            List of dicts: [{"timestamp_sec": float, "caption": str, "error": str|None}, ...]
        """
        client = get_vllm_client()

        # Check vLLM availability
        if not client.is_available():
            logger.warning("vLLM service unavailable, skipping captioning")
            # Return pending status for all frames
            return [
                {
                    "timestamp_sec": fd["timestamp_sec"],
                    "caption": "",
                    "error": "vLLM service unavailable"
                }
                for fd in frame_data
            ]

        # Save frames to temp files for vLLM processing
        # (vLLM client expects file paths, not byte data)
        import tempfile
        import os

        temp_files = []
        temp_paths = []

        try:
            # Create temp files for each frame
            for fd in frame_data:
                temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                temp_file.write(fd["image_data"])
                temp_file.flush()
                temp_file.close()
                temp_files.append(temp_file)
                temp_paths.append(temp_file.name)

            # Batch caption via vLLM
            vllm_results = client.caption_images_batch(
                paths=temp_paths,
                max_workers=batch_size
            )

            # Build results with timestamps
            caption_results = []
            for fd, (path, caption, error) in zip(frame_data, vllm_results):
                caption_results.append({
                    "timestamp_sec": fd["timestamp_sec"],
                    "caption": caption or "",
                    "error": error
                })

            return caption_results

        finally:
            # Cleanup temp files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file.name)
                except Exception:
                    pass

    @staticmethod
    def create_frame_records(
        clip: AssetClip,
        caption_results: List[dict]
    ) -> List[ClipFrame]:
        """Create ClipFrame database records (without image_file).

        Args:
            clip: AssetClip instance
            caption_results: List of dicts with "timestamp_sec", "caption", "error"

        Returns:
            List of created ClipFrame instances
        """
        created_frames = []

        for result in caption_results:
            timestamp_sec = result["timestamp_sec"]
            caption = result["caption"]
            error = result.get("error")

            # Determine status
            if caption:
                status = "complete"
            elif error and "unavailable" in error.lower():
                status = "pending"  # Can retry later
            elif error:
                status = "failed"
            else:
                status = "pending"

            # Create ClipFrame record
            frame = ClipFrame.objects.create(
                clip=clip,
                timestamp_sec=timestamp_sec,
                caption_text=caption,
                caption_model="joycaption2",
                status=status,
                error=error or ""
            )

            created_frames.append(frame)

        return created_frames
