"""
Modal Qwen2.5-VL Video Captioning

This module provides direct video-to-description captioning using Qwen2.5-VL,
replacing the multi-step JoyCaption + Grok aggregation pipeline.

Quick Start:
    # Deploy to Modal
    modal deploy modal_qwen_vl/app.py

    # Use in Django
    from modal_qwen_vl.client import ModalQwenVLClient
    client = ModalQwenVLClient(endpoint_url="https://your-endpoint.modal.run")
    result = client.caption_video("https://example.com/video.mp4")
"""

from .client import ModalQwenVLClient, caption_video_modal

__all__ = ["ModalQwenVLClient", "caption_video_modal"]
