#!/usr/bin/env python
"""
Quick test script for Modal Qwen-VL captioning.

Usage:
    # Test with Modal SDK (runs on Modal's GPUs)
    python modal_qwen_vl/test_local.py --video-url "https://example.com/video.mp4"

    # Test with deployed HTTP endpoint
    python modal_qwen_vl/test_local.py --endpoint "https://your-endpoint.modal.run" --video-url "..."
"""

import argparse
import time


def test_with_sdk(video_source: str, is_file: bool = False):
    """Test using Modal SDK directly."""
    print("Testing with Modal SDK...")
    print(f"Video: {video_source}")
    print("-" * 50)

    from app import QwenVLCaptioner

    captioner = QwenVLCaptioner()

    start = time.time()

    if is_file:
        with open(video_source, "rb") as f:
            video_bytes = f.read()
        result = captioner.caption_video_from_bytes.remote(video_bytes)
    else:
        result = captioner.caption_video.remote(video_source)

    elapsed = time.time() - start

    print(f"\n{'=' * 50}")
    print("RESULT")
    print(f"{'=' * 50}")
    print(f"\nDescription:\n{result['description']}")
    print(f"\n{'=' * 50}")
    print(f"Model: {result['model']}")
    print(f"Input tokens: {result['input_tokens']}")
    print(f"Output tokens: {result['output_tokens']}")
    print(f"Time: {elapsed:.1f}s")


def test_with_http(endpoint_url: str, video_source: str, is_file: bool = False):
    """Test using HTTP endpoint."""
    import base64
    import httpx

    print("Testing with HTTP endpoint...")
    print(f"Endpoint: {endpoint_url}")
    print(f"Video: {video_source}")
    print("-" * 50)

    payload = {"max_tokens": 800}

    if is_file:
        with open(video_source, "rb") as f:
            video_bytes = f.read()
        payload["video_base64"] = base64.b64encode(video_bytes).decode("utf-8")
        print(f"Video size: {len(video_bytes) / 1024 / 1024:.1f} MB")
    else:
        payload["video_url"] = video_source

    start = time.time()

    with httpx.Client(timeout=300) as client:
        response = client.post(endpoint_url, json=payload)
        response.raise_for_status()
        result = response.json()

    elapsed = time.time() - start

    print(f"\n{'=' * 50}")
    print("RESULT")
    print(f"{'=' * 50}")
    print(f"\nDescription:\n{result['description']}")
    print(f"\n{'=' * 50}")
    print(f"Model: {result['model']}")
    print(f"Input tokens: {result['input_tokens']}")
    print(f"Output tokens: {result['output_tokens']}")
    print(f"Time: {elapsed:.1f}s")


def main():
    parser = argparse.ArgumentParser(description="Test Modal Qwen-VL captioning")
    parser.add_argument("--video-url", help="URL to video file")
    parser.add_argument("--video-path", help="Path to local video file")
    parser.add_argument("--endpoint", help="HTTP endpoint URL (if not using SDK)")
    args = parser.parse_args()

    if not args.video_url and not args.video_path:
        print("Error: Provide --video-url or --video-path")
        return

    video_source = args.video_path or args.video_url
    is_file = bool(args.video_path)

    if args.endpoint:
        test_with_http(args.endpoint, video_source, is_file)
    else:
        test_with_sdk(video_source, is_file)


if __name__ == "__main__":
    main()
