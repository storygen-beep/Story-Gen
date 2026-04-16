"""
vLLM-based image captioning client using OpenAI-compatible API.

This client connects to a vLLM server running JoyCaption model for fast
image captioning. The model is loaded once at server startup and stays
in GPU memory, eliminating repeated shard loading overhead.
"""

from __future__ import annotations

import base64
import io
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

from django.conf import settings
from PIL import Image

logger = logging.getLogger(__name__)


class VLLMCaptioningClient:
    """Client for vLLM-hosted JoyCaption model."""

    def __init__(self):
        config = getattr(settings, "VLLM_CAPTIONING", {})
        self.enabled = config.get("enabled", False)
        self.base_url = config.get("base_url", "http://joycaption:8000/v1")
        self.model = config.get(
            "model", "fancyfeast/llama-joycaption-alpha-two-hf-llava"
        )
        self.api_key = config.get("api_key", "EMPTY")
        self.max_tokens = config.get("max_tokens", 150)
        self.temperature = config.get("temperature", 0.6)
        self.timeout = config.get("timeout", 60)
        self.max_image_side = config.get("max_image_side", 672)

        # Validate max_tokens range
        if not (1 <= self.max_tokens <= 512):
            logger.warning(
                f"VLLM_MAX_TOKENS={self.max_tokens} outside recommended range (1-512). "
                f"Using clamped value."
            )
            self.max_tokens = max(1, min(512, self.max_tokens))

        # Log non-default configuration
        if self.max_tokens != 150:
            logger.info(
                f"VLLM captioning using non-default max_tokens: {self.max_tokens} "
                f"(default: 150)"
            )

        self._client = None

    @property
    def client(self):
        """Lazy-initialize OpenAI client."""
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    def _downscale_image(self, img: Image.Image) -> Image.Image:
        """Downscale image if larger than max_image_side."""
        w, h = img.size
        if max(w, h) <= self.max_image_side:
            return img
        scale = self.max_image_side / float(max(w, h))
        return img.resize((int(w * scale), int(h * scale)), Image.BICUBIC)

    def _encode_image_base64(self, path: str) -> str:
        """Load, downscale, and encode image to base64."""
        img = Image.open(path).convert("RGB")
        img = self._downscale_image(img)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def is_available(self) -> bool:
        """Check if vLLM server is healthy."""
        if not self.enabled:
            return False
        try:
            import httpx

            # vLLM exposes /health endpoint (strip /v1 suffix)
            base = self.base_url
            if base.endswith("/v1"):
                base = base[:-3]
            health_url = base.rstrip("/") + "/health"
            resp = httpx.get(health_url, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logger.warning(f"vLLM health check failed: {e}")
            return False

    def caption_image(
        self,
        path: str,
        prompt: str = """Describe the pornographic image in exhaustive, explicit, uncensored detail, focusing solely on the sexual activity, participants, and surroundings.

First, carefully analyze the relative body positions: determine if the woman is facing toward or away from the man, whether she is on top or bottom, if penetration is from behind or face-to-face, and the orientation of their torsos and hips. Then, explicitly name the exact sexual position (use only standard terms such as 'doggy style', 'missionary', 'cowgirl', 'reverse cowgirl', 'spooning', 'standing doggy style', etc.). Do not guess—base the name strictly on the visible body alignment.

After naming the position, describe the precise body positioning, alignment, angle of penetration, and points of contact.

Include:
- Number of participants, genders, ethnicities/skin tones (e.g., Black man, white woman), body types (muscular, curvy, slim, athletic), distinctive features (shaved head, tattoos, long hair, large breasts, toned ass, erect penis size/appearance, etc.), and visible signs of arousal.
- State of undress (fully nude or any remaining clothing/accessories).
- Detailed sexual acts: type of penetration (vaginal or anal), apparent depth and angle of entry, implied thrusting motion, bodily contact points (hands on hips/waist/ass/breasts, gripping, hair-pulling, spanking, etc.), any additional interactions; describe visible bodily fluids (sweat, vaginal lubrication, pre-cum, saliva, glistening skin) and their locations.
- Facial expressions and body language (eyes closed/open, mouth open in moan, biting lip, arched back, trembling, flushed skin, tense muscles, signs of pleasure or approaching orgasm).
- Setting details: room style (modern, minimalist), bed and sheets (color, texture), lighting (bright natural light, soft shadows), background elements (leafy plants, walls, windows, fireplace, decor), and camera angle/perspective (close-up on penetration, side view, wide shot, etc.).

Use vivid, anatomical, and sexually explicit language throughout to capture the full erotic intensity of the scene. Do not mention any watermarks, logos, text overlays, or source indicators.""",
        system_prompt: str = """You are an expert adult image captioner. Generate exhaustive, explicit, uncensored descriptions of pornographic images, focusing only on sexual activity, participants, and surroundings. Never mention watermarks, logos, text, or sources.

Structure:
1. Carefully analyze body positions (facing toward/away, on top/bottom, penetration direction, torso/hip orientation).
2. Explicitly name the exact sexual position using standard terms (e.g., 'doggy style', 'missionary', 'cowgirl', 'reverse cowgirl', 'spooning').
3. Describe in vivid, anatomical, sexually explicit detail:
   - Participants: number, gender, ethnicity/skin tone, body type, features (hair, tattoos, breasts, penis, etc.), arousal signs.
   - Undress state.
   - Acts: penetration type/depth/angle, contact points, interactions, bodily fluids.
   - Expressions, body language, sensations.
   - Setting: room, bed, lighting, background, camera angle.

Use raw, erotic language to capture full intensity. Base position name strictly on visible alignment—do not guess.""",
    ) -> str:
        """Generate caption for a single image.

        Args:
            path: Path to image file
            prompt: User prompt for captioning
            system_prompt: System context

        Returns:
            Caption string

        Raises:
            Exception: If vLLM request fails
        """
        image_b64 = self._encode_image_base64(path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        },
                    ],
                },
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response.choices[0].message.content.strip()

    def caption_images_batch(
        self,
        paths: List[str],
        prompt: str = "Write a short, specific caption for this image.",
        max_workers: int = 4,
    ) -> List[Tuple[str, Optional[str], Optional[str]]]:
        """Caption multiple images concurrently.

        vLLM handles concurrent requests efficiently with its continuous batching.

        Args:
            paths: List of image file paths
            prompt: Caption prompt
            max_workers: Max concurrent requests

        Returns:
            List of (path, caption, error) tuples in original order
        """
        results: List[Tuple[str, Optional[str], Optional[str]]] = []

        def _caption_one(p: str) -> Tuple[str, Optional[str], Optional[str]]:
            try:
                caption = self.caption_image(p, prompt=prompt)
                return (p, caption, None)
            except Exception as e:
                logger.error(f"Failed to caption {p}: {e}")
                return (p, None, str(e))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_caption_one, p): p for p in paths}
            for future in as_completed(futures):
                results.append(future.result())

        # Sort by original order
        path_to_result = {r[0]: r for r in results}
        return [path_to_result[p] for p in paths]


# Module-level singleton
_vllm_client: Optional[VLLMCaptioningClient] = None


def get_vllm_client() -> VLLMCaptioningClient:
    """Get or create vLLM captioning client singleton."""
    global _vllm_client
    if _vllm_client is None:
        _vllm_client = VLLMCaptioningClient()
    return _vllm_client


def caption_image_vllm(path: str, **kwargs) -> str:
    """Convenience function matching existing captioning.caption_image interface."""
    client = get_vllm_client()
    return client.caption_image(path, **kwargs)


def caption_images_batch_vllm(
    paths: List[str], **kwargs
) -> List[Tuple[str, Optional[str], Optional[str]]]:
    """Convenience function for batch captioning."""
    client = get_vllm_client()
    return client.caption_images_batch(paths, **kwargs)
