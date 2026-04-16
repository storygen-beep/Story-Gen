"""
Modal Qwen-VL Client for Django Integration

This client replaces the JoyCaption + Grok pipeline with direct video captioning.

Usage in Django:
    from modal_qwen_vl.client import ModalQwenVLClient

    client = ModalQwenVLClient()
    description = client.caption_video(video_url_or_path)
"""

import base64
import logging
from pathlib import Path
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class ModalQwenVLClient:
    """
    Client for Modal-hosted Qwen2.5-VL video captioning.

    Supports two modes:
    1. Web endpoint (HTTP) - for deployed Modal app
    2. Direct Modal SDK - for local development
    """

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        use_sdk: bool = False,
        timeout: int = 300,
    ):
        """
        Initialize the client.

        Args:
            endpoint_url: Modal web endpoint URL (from `modal deploy`)
            use_sdk: If True, use Modal SDK directly (requires modal package)
            timeout: Request timeout in seconds
        """
        self.endpoint_url = endpoint_url
        self.use_sdk = use_sdk
        self.timeout = timeout
        self._modal_captioner = None

    def _get_modal_captioner(self):
        """Lazy-load Modal SDK captioner."""
        if self._modal_captioner is None:
            try:
                from modal_qwen_vl.app import QwenVLCaptioner
                self._modal_captioner = QwenVLCaptioner()
            except ImportError:
                raise RuntimeError(
                    "Modal SDK not available. Either install modal (`pip install modal`) "
                    "or provide endpoint_url for HTTP mode."
                )
        return self._modal_captioner

    def caption_video(
        self,
        video_source: str,
        prompt: Optional[str] = None,
        max_tokens: int = 800,
    ) -> dict:
        """
        Generate description for a video.

        Args:
            video_source: URL, file path, or base64-encoded video
            prompt: Custom prompt (uses default NSFW prompt if None)
            max_tokens: Maximum output tokens

        Returns:
            dict with 'description', 'model', 'input_tokens', 'output_tokens'
        """
        # Determine if source is a file path
        is_file = Path(video_source).exists() if not video_source.startswith(('http', 'data:')) else False

        if self.use_sdk:
            return self._caption_via_sdk(video_source, prompt, max_tokens, is_file)
        else:
            return self._caption_via_http(video_source, prompt, max_tokens, is_file)

    def _caption_via_sdk(
        self,
        video_source: str,
        prompt: Optional[str],
        max_tokens: int,
        is_file: bool,
    ) -> dict:
        """Caption using Modal SDK directly."""
        captioner = self._get_modal_captioner()

        if is_file:
            with open(video_source, "rb") as f:
                video_bytes = f.read()
            return captioner.caption_video_from_bytes.remote(
                video_bytes, prompt, max_tokens
            )
        else:
            return captioner.caption_video.remote(
                video_source, prompt, max_tokens
            )

    def _caption_via_http(
        self,
        video_source: str,
        prompt: Optional[str],
        max_tokens: int,
        is_file: bool,
    ) -> dict:
        """Caption using Modal web endpoint."""
        if not self.endpoint_url:
            raise ValueError(
                "endpoint_url required for HTTP mode. "
                "Get it from `modal deploy app.py` output."
            )

        # Build request payload
        payload = {"max_tokens": max_tokens}
        if prompt:
            payload["prompt"] = prompt

        if is_file:
            # Read and base64 encode file
            with open(video_source, "rb") as f:
                video_bytes = f.read()
            payload["video_base64"] = base64.b64encode(video_bytes).decode("utf-8")
        elif video_source.startswith("data:"):
            # Already base64
            payload["video_base64"] = video_source.split(",")[1]
        else:
            # URL
            payload["video_url"] = video_source

        # Make request
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(self.endpoint_url, json=payload)
            response.raise_for_status()
            return response.json()

    def is_available(self) -> bool:
        """Check if the Modal endpoint is available."""
        if self.use_sdk:
            try:
                self._get_modal_captioner()
                return True
            except Exception as e:
                logger.warning(f"Modal SDK not available: {e}")
                return False
        else:
            if not self.endpoint_url:
                return False
            try:
                # Simple health check
                with httpx.Client(timeout=10) as client:
                    response = client.get(self.endpoint_url.replace("/caption", "/health"))
                    return response.status_code == 200
            except Exception as e:
                logger.warning(f"Modal endpoint not available: {e}")
                return False


# Convenience function matching existing interface
def caption_video_modal(
    video_source: str,
    endpoint_url: Optional[str] = None,
    prompt: Optional[str] = None,
    max_tokens: int = 800,
) -> str:
    """
    Simple function to caption a video.

    Args:
        video_source: URL or file path to video
        endpoint_url: Modal web endpoint (from settings or env)
        prompt: Custom prompt
        max_tokens: Max output tokens

    Returns:
        Video description string
    """
    from django.conf import settings

    # Get endpoint from settings if not provided
    if endpoint_url is None:
        endpoint_url = getattr(settings, "MODAL_QWEN_VL_ENDPOINT", None)

    client = ModalQwenVLClient(endpoint_url=endpoint_url)
    result = client.caption_video(video_source, prompt, max_tokens)
    return result["description"]
