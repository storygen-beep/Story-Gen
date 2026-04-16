"""
Service for generating clip descriptions using Grok AI.
Aggregates frame captions and generates coherent video descriptions.
"""

import logging
import time
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.conf import settings
from django.utils import timezone
from openai import OpenAI
from apps.assets.models import AssetClip, ClipFrame

logger = logging.getLogger(__name__)


class GrokClipDescriptionClient:
    """Client for Grok AI clip description generation."""

    def __init__(self):
        """Initialize Grok client from Django settings."""
        config = getattr(settings, "GROK_CLIP_DESCRIPTIONS", {})
        self.enabled = config.get("enabled", False)
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("api_base_url", "https://api.x.ai/v1")
        self.model = config.get("model", "grok-4-fast")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 800)
        self.min_frames = config.get("min_frames", 3)
        self.timeout = config.get("timeout", 30)

        # Log non-default configuration
        if self.max_tokens != 800:
            logger.info(
                f"Grok clip descriptions using non-default max_tokens: {self.max_tokens} "
                f"(default: 800)"
            )

        if self.enabled and self.api_key:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
            )
        else:
            self._client = None

    def is_available(self) -> bool:
        """Check if Grok service is available."""
        if not self.enabled:
            logger.debug("Grok clip descriptions disabled in settings")
            return False

        if not self.api_key:
            logger.warning("Grok API key not configured")
            return False

        if self._client is None:
            logger.error("Grok client not initialized")
            return False

        return True

    def generate_description(self, clip: AssetClip) -> Optional[str]:
        """
        Generate description for a clip from its frame captions.

        Args:
            clip: AssetClip instance with captioned frames

        Returns:
            Generated description or None if skipped/failed

        Raises:
            Exception: If API call fails after retries
        """
        if not self.is_available():
            return None

        # Get captioned frames
        frames = (
            clip.frames.filter(status="complete")
            .exclude(caption_text="")
            .order_by("timestamp_sec")
        )

        frame_count = frames.count()

        # Skip if insufficient frames
        if frame_count < self.min_frames:
            logger.info(
                f"Skipping clip {clip.id}: insufficient frames "
                f"({frame_count} < {self.min_frames})"
            )
            return None

        # Build prompt from frame captions
        prompt = self._build_prompt(clip, frames)

        # Call Grok API with retry logic
        try:
            description = self._call_api(prompt)
            logger.info(
                f"Generated description for clip {clip.id} "
                f"({frame_count} frames, {len(description)} chars)"
            )
            return description
        except Exception as e:
            logger.error(
                f"Failed to generate description for clip {clip.id}: {e}", exc_info=True
            )
            raise

    def generate_with_result(self, clip: AssetClip) -> dict:
        """
        Generate description and return structured result for API.

        Returns:
            {
                "success": bool,
                "clip_id": str,
                "description": str or None,
                "model": str or None,
                "generated_at": str or None,
                "skipped": bool,
                "skip_reason": str or None,
                "error": str or None
            }
        """
        try:
            # Use existing generate_description method
            description = self.generate_description(clip)

            if description is None:
                # Clip was skipped (insufficient frames)
                frames_count = clip.frames.filter(
                    status="complete",
                    caption_text__isnull=False
                ).exclude(caption_text="").count()

                return {
                    "success": False,
                    "clip_id": str(clip.id),
                    "description": None,
                    "model": None,
                    "generated_at": None,
                    "skipped": True,
                    "skip_reason": f"Insufficient frames: {frames_count} (minimum {self.min_frames} required)",
                    "error": None
                }

            # Success - save to database
            clip.description = description
            clip.description_model = self.model
            clip.description_generated_at = timezone.now()
            clip.description_error = ""  # Clear any previous errors
            clip.save(update_fields=[
                "description", "description_model",
                "description_generated_at", "description_error"
            ])

            return {
                "success": True,
                "clip_id": str(clip.id),
                "description": description,
                "model": self.model,
                "generated_at": clip.description_generated_at.isoformat(),
                "skipped": False,
                "skip_reason": None,
                "error": None
            }

        except Exception as e:
            # Error - save to database
            error_msg = str(e)
            clip.description_error = error_msg
            clip.save(update_fields=["description_error"])

            return {
                "success": False,
                "clip_id": str(clip.id),
                "description": None,
                "model": None,
                "generated_at": None,
                "skipped": False,
                "skip_reason": None,
                "error": error_msg
            }

    def batch_generate_for_video(
        self,
        video,
        only_missing: bool = True,
        force_regenerate: bool = False
    ) -> dict:
        """
        Batch generate descriptions for clips in a video.

        Args:
            video: AssetVideo instance
            only_missing: Only generate for clips without descriptions
            force_regenerate: Regenerate even if description exists

        Returns:
            {
                "video_id": str,
                "total_clips": int,
                "processed": int,
                "skipped": int,
                "results": List[dict],
                "summary": {
                    "successful": int,
                    "failed": int,
                    "skipped": int
                }
            }
        """
        from django.db.models import Q

        # Get clips to process
        clips_query = video.clips.filter(deleted_at__isnull=True)

        if only_missing and not force_regenerate:
            # Only clips without descriptions
            clips_query = clips_query.filter(
                Q(description__isnull=True) | Q(description="")
            )

        clips = list(clips_query.order_by("index"))

        if not clips:
            return {
                "video_id": str(video.id),
                "total_clips": 0,
                "processed": 0,
                "skipped": 0,
                "results": [],
                "summary": {
                    "successful": 0,
                    "failed": 0,
                    "skipped": 0
                }
            }

        # Process each clip and collect results
        results = []
        successful = 0
        failed = 0
        skipped = 0

        for clip in clips:
            result = self.generate_with_result(clip)
            results.append({
                "clip_id": str(clip.id),
                "clip_index": clip.index,
                "success": result["success"],
                "description": result["description"],
                "skipped": result["skipped"],
                "skip_reason": result.get("skip_reason"),
                "error": result.get("error")
            })

            if result["success"]:
                successful += 1
            elif result["skipped"]:
                skipped += 1
            else:
                failed += 1

        return {
            "video_id": str(video.id),
            "total_clips": len(clips),
            "processed": len(clips),
            "skipped": skipped,
            "results": results,
            "summary": {
                "successful": successful,
                "failed": failed,
                "skipped": skipped
            }
        }

    def _build_prompt(self, clip: AssetClip, frames) -> str:
        """Build Grok prompt from clip metadata and frame captions."""
        # Format frame captions with timestamps
        frame_captions = "\n".join(
            [f"- {frame.timestamp_sec:.1f}s: {frame.caption_text}" for frame in frames]
        )

        prompt = f"""You are analyzing a pornographic video clip. Below are detailed, explicit captions from frames extracted at regular intervals.

LENGTH REQUIREMENT: Write exactly 500 words (MAXIMUM). Do not exceed 500 words.

Clip Information:
- Duration: {clip.duration_sec:.1f} seconds
- Time range: {clip.start_sec:.1f}s to {clip.end_sec:.1f}s
- Number of frames: {frames.count()}

Frame Captions (timestamp: caption):
{frame_captions}

Generate a script-style description of the sexual activities in this clip, written in present tense. Focus exclusively on observable actions, movements, and interactions without describing physical appearances.

Script Format Guidelines:
- Present tense, action-focused writing (like a screenplay/stage direction)
- Chronological progression through the clip's timeline

Essential Content:
- Participant identification: number of people and their genders (e.g., "two men", "a woman and a man")
- Sexual activities: explicit positions (named accurately), penetration type and depth, specific bodily contact
- Physical interactions: gripping, spanking, hair-pulling, kissing, caressing, etc.
- Bodily responses: visible fluids, arousal indicators, physical reactions
- Spatial dynamics: positioning, movement patterns, orientation changes
- Setting details: room characteristics, furniture, lighting, props
- Temporal flow: how activities build, transition, intensify, and conclude

Excluded Content:
- Do NOT describe: body types, ethnicities, skin tones, facial features, hair styles/colors, tattoos, piercings, breast size, penis appearance, muscle definition, or any physical appearance details
- Do NOT mention: watermarks, logos, production sources, or non-visual elements

Write in continuous prose using vivid, anatomically explicit language. Describe what happens, not what people look like.

Remember: Keep your description to exactly 500 words to ensure the complete description is delivered without truncation.

Description:"""

        return prompt

    def _call_api(self, prompt: str, max_retries: int = 3) -> str:
        """
        Call Grok API with exponential backoff retry logic.

        Args:
            prompt: The prompt to send to Grok
            max_retries: Maximum number of retry attempts

        Returns:
            Generated description text

        Raises:
            Exception: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that analyzes video content.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )

                description = response.choices[0].message.content.strip()
                return description

            except Exception as e:
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2**attempt
                    logger.warning(
                        f"Grok API call failed (attempt {attempt + 1}/{max_retries}), "
                        f"retrying in {wait_time}s: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    raise

    def process_clips_batch(
        self, clips: List[AssetClip], max_workers: int = 4
    ) -> List[tuple]:
        """
        Process multiple clips in parallel.

        Args:
            clips: List of AssetClip instances
            max_workers: Maximum concurrent API calls

        Returns:
            List of (clip, description, error) tuples
        """
        if not self.is_available():
            return [(clip, None, "Service not available") for clip in clips]

        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._process_single_clip, clip): clip for clip in clips
            }

            for future in as_completed(futures):
                clip = futures[future]
                try:
                    description = future.result()
                    results.append((clip, description, None))
                except Exception as e:
                    results.append((clip, None, str(e)))

        return results

    def _process_single_clip(self, clip: AssetClip) -> Optional[str]:
        """Helper for batch processing."""
        return self.generate_description(clip)


# Singleton client instance
_grok_client: Optional[GrokClipDescriptionClient] = None


def get_grok_client() -> GrokClipDescriptionClient:
    """Get or create singleton Grok client."""
    global _grok_client
    if _grok_client is None:
        _grok_client = GrokClipDescriptionClient()
    return _grok_client


def generate_clip_description(clip: AssetClip) -> Optional[str]:
    """
    Convenience function to generate clip description.

    Args:
        clip: AssetClip instance

    Returns:
        Generated description or None if skipped/disabled
    """
    client = get_grok_client()

    if not client.is_available():
        return None

    return client.generate_description(clip)
