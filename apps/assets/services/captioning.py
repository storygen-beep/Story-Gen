"""Image captioning service using vLLM server.

This module provides image captioning via a vLLM server running the JoyCaption model.
The vLLM server keeps the model loaded in GPU memory for fast inference (~1-2s per image).
"""
from __future__ import annotations

import logging

from apps.assets.services.vllm_captioning import get_vllm_client

logger = logging.getLogger(__name__)


def caption_image(path: str, *, max_new_tokens: int = 64) -> str:
    """Generate a concise caption for a local image file.

    Uses the vLLM server for fast inference. The server must be running
    and healthy for captioning to work.

    Args:
        path: Absolute or relative path to the image file.
        max_new_tokens: Maximum tokens to generate for caption.

    Returns:
        Caption string describing the image.

    Raises:
        RuntimeError: If the vLLM captioning service is not available.
    """
    client = get_vllm_client()

    if not client.is_available():
        raise RuntimeError(
            "vLLM captioning service is not available. "
            "Ensure the joycaption container is running and healthy. "
            "Check with: docker ps | grep joycaption"
        )

    logger.info("Using vLLM server for captioning")
    return client.caption_image(path)
