#!/usr/bin/env python3
"""
Video Caption Generator - Comprehensive Video Captioning with LLaVA JoyCaption

Generates detailed, timestamped captions for videos using:
- Time-based frame sampling (every 2 seconds)
- Batched unified captioning (5 frames per segment)
- Full video coverage without limits
- Structured JSON output with timestamps

Usage:
    python video_caption_generator.py --video assets/clips/scene_000.mp4
    python video_caption_generator.py --r2-key assets/clips/scene_000.mp4 --interval 3.0
"""

import os
import sys
import argparse
import json
import time
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration


@dataclass
class CaptionConfig:
    """Configuration for video captioning"""
    sampling_interval: float = 2.0  # Extract frame every N seconds
    frames_per_batch: int = 5       # Process N frames together for unified caption
    max_side: int = 672             # Max image dimension (VRAM optimization)
    model_name: str = "fancyfeast/llama-joycaption-alpha-two-hf-llava"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype: torch.dtype = torch.float16


@dataclass
class VideoMetadata:
    """Video processing metadata"""
    video_path: str
    duration_seconds: float
    frames_sampled: int
    batches_processed: int
    sampling_interval: float
    processing_time_seconds: float


@dataclass
class CaptionSegment:
    """Single caption segment with timing"""
    segment_id: int
    start_time: str  # Format: "M:SS"
    end_time: str
    frames_analyzed: int
    frame_timestamps: List[float]
    caption: str


class VideoCaption:
    """Main video captioning engine"""

    def __init__(self, config: Optional[CaptionConfig] = None):
        """Initialize model and configuration"""
        self.config = config or CaptionConfig()
        self.processor = None
        self.model = None

        print(f"🚀 Initializing VideoCaption on {self.config.device}")
        print(f"📊 Config: {self.config.sampling_interval}s interval, {self.config.frames_per_batch} frames/batch")

        self._setup_environment()
        self._load_model()

    def _setup_environment(self):
        """Configure PyTorch environment"""
        # Avoid torchvision in transformers pipeline
        os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"

        # Reduce CUDA fragmentation
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True,max_split_size_mb:128"

        # Disable fused SDPA to avoid dtype conflicts
        if self.config.device == "cuda":
            torch.backends.cuda.enable_flash_sdp(False)
            torch.backends.cuda.enable_mem_efficient_sdp(False)
            torch.backends.cuda.enable_math_sdp(True)

    def _load_model(self):
        """Load LLaVA model with float16 (no quantization)"""
        print(f"📥 Loading model: {self.config.model_name}")

        self.processor = AutoProcessor.from_pretrained(
            self.config.model_name,
            trust_remote_code=True
        )

        self.model = LlavaForConditionalGeneration.from_pretrained(
            self.config.model_name,
            torch_dtype=self.config.torch_dtype,  # float16 without quantization
            device_map="auto",
            attn_implementation="eager",
            trust_remote_code=True,
        )

        self.model.eval()
        print(f"✅ Model loaded successfully on {self.config.device}")
        print(f"⚠️  Note: Using float16 without quantization (~16GB VRAM)")

    def _normalize_inputs_for_generate(self, inputs: Dict, device: str) -> Dict:
        """FIXED: Properly normalize dtypes for model.generate()

        Critical fixes:
        1. Force attention_mask to int64 regardless of input dtype
        2. Move to device AFTER dtype conversion (not before)
        3. Ensure pixel_values are float16
        """
        fixed = {}

        for k, v in inputs.items():
            if not hasattr(v, "to"):
                # Non-tensor values
                fixed[k] = v
                continue

            # Step 1: Fix dtype BEFORE moving to device
            if k == "pixel_values":
                if v.dtype != torch.float16:
                    v = v.to(torch.float16)
            elif k == "input_ids":
                if v.dtype != torch.int64:
                    v = v.to(torch.int64)
            elif k in ("attention_mask", "pixel_attention_mask", "cross_attention_mask"):
                # CRITICAL FIX: Always force int64 for mask tensors
                if v.dtype != torch.int64:
                    v = v.to(torch.int64)

            # Step 2: Now move to device
            v = v.to(device)
            fixed[k] = v

        return fixed

    def _probe_duration(self, video_path: str) -> float:
        """Get video duration in seconds using ffprobe"""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            return float(output)
        except Exception as e:
            print(f"⚠️  Warning: Could not probe duration: {e}")
            return 0.0

    def _extract_frame_at_time(self, video_path: str, timestamp: float, output_path: str):
        """Extract single frame at specific timestamp"""
        cmd = [
            "ffmpeg",
            "-ss", f"{timestamp:.3f}",
            "-i", video_path,
            "-vframes", "1",
            "-y",
            output_path
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def _downscale_image(self, img: Image.Image) -> Image.Image:
        """Downscale image to max_side for VRAM efficiency"""
        w, h = img.size
        if max(w, h) <= self.config.max_side:
            return img

        scale = self.config.max_side / float(max(w, h))
        new_size = (int(w * scale), int(h * scale))
        return img.resize(new_size, Image.BICUBIC)

    def extract_frames_at_intervals(self, video_bytes: bytes) -> Tuple[List[Image.Image], List[float]]:
        """Extract frames at regular time intervals

        Returns:
            Tuple of (frames, timestamps)
        """
        frames = []
        timestamps = []

        with tempfile.TemporaryDirectory() as td:
            # Write video to temp file
            video_path = Path(td) / "video.mp4"
            video_path.write_bytes(video_bytes)

            # Get duration
            duration = self._probe_duration(str(video_path))
            if duration <= 0:
                raise ValueError("Could not determine video duration")

            # Calculate timestamps for sampling
            current_time = 0.0
            while current_time < duration:
                timestamps.append(current_time)
                current_time += self.config.sampling_interval

            # Add final frame if not already included
            if timestamps[-1] < duration - 0.5:
                timestamps.append(duration - 0.5)

            print(f"📊 Video duration: {duration:.1f}s, sampling {len(timestamps)} frames")

            # Extract frames
            for i, ts in enumerate(timestamps):
                frame_path = Path(td) / f"frame_{i:04d}.jpg"
                self._extract_frame_at_time(str(video_path), ts, str(frame_path))

                img = Image.open(frame_path).convert("RGB")
                img = self._downscale_image(img)
                frames.append(img)

        return frames, timestamps

    def batch_frames(self, frames: List[Image.Image], timestamps: List[float]) -> List[Dict]:
        """Group frames into batches for unified captioning

        Returns:
            List of batch dicts with frames, timestamps, and time range
        """
        batches = []

        for i in range(0, len(frames), self.config.frames_per_batch):
            batch_frames = frames[i:i + self.config.frames_per_batch]
            batch_timestamps = timestamps[i:i + self.config.frames_per_batch]

            start_time = batch_timestamps[0]
            end_time = batch_timestamps[-1] + self.config.sampling_interval

            batches.append({
                "batch_id": len(batches) + 1,
                "frames": batch_frames,
                "timestamps": batch_timestamps,
                "start_time": start_time,
                "end_time": end_time,
            })

        return batches

    def _format_time(self, seconds: float) -> str:
        """Format seconds as M:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"

    def caption_batch(self, images: List[Image.Image], prompt: str = None) -> str:
        """Generate unified caption for batch of frames

        Uses LLaVA's multi-image capability to understand temporal progression
        """
        if prompt is None:
            prompt = "Write a concise, descriptive caption that captures the progression of events shown in these video frames."

        # Build conversation
        convo = [
            {"role": "system", "content": "You are an expert video analyst. Describe what happens across the sequence of frames."},
            {"role": "user", "content": prompt},
        ]

        convo_string = self.processor.apply_chat_template(
            convo,
            tokenize=False,
            add_generation_prompt=True
        )

        # Process multiple images together
        raw_inputs = self.processor(
            text=[convo_string],
            images=[images],  # List of images for multi-image support
            return_tensors="pt",
            padding=True
        )

        # Fix dtypes
        inputs = self._normalize_inputs_for_generate(raw_inputs, self.config.device)

        # Generate caption
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                use_cache=True,
            )[0]

        # Decode (skip prompt tokens)
        output_ids = output_ids[inputs["input_ids"].shape[1]:]
        caption = self.processor.tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        ).strip()

        # Clear VRAM
        if self.config.device == "cuda":
            torch.cuda.empty_cache()

        return caption

    def process_video(self, video_bytes: bytes, video_path: str = None) -> Dict:
        """Process entire video and generate structured output

        Args:
            video_bytes: Raw video data
            video_path: Optional path for metadata

        Returns:
            Structured dict with metadata and segments
        """
        start_time = time.time()

        print(f"\n🎬 Processing video: {video_path or 'unknown'}")

        # Extract frames
        print("🔍 Extracting frames...")
        frames, timestamps = self.extract_frames_at_intervals(video_bytes)

        # Create batches
        print(f"📦 Creating {len(frames) // self.config.frames_per_batch + 1} batches...")
        batches = self.batch_frames(frames, timestamps)

        # Process each batch
        segments = []
        for batch in batches:
            print(f"   Processing batch {batch['batch_id']}/{len(batches)}... ", end="", flush=True)

            caption = self.caption_batch(batch["frames"])

            segment = CaptionSegment(
                segment_id=batch["batch_id"],
                start_time=self._format_time(batch["start_time"]),
                end_time=self._format_time(batch["end_time"]),
                frames_analyzed=len(batch["frames"]),
                frame_timestamps=batch["timestamps"],
                caption=caption
            )

            segments.append(segment)
            print(f"✅")

        # Calculate metadata
        processing_time = time.time() - start_time
        duration = timestamps[-1] + self.config.sampling_interval

        metadata = VideoMetadata(
            video_path=video_path or "unknown",
            duration_seconds=duration,
            frames_sampled=len(frames),
            batches_processed=len(batches),
            sampling_interval=self.config.sampling_interval,
            processing_time_seconds=round(processing_time, 2)
        )

        print(f"\n✅ Processing complete! {len(segments)} segments generated in {processing_time:.1f}s")

        return {
            "metadata": asdict(metadata),
            "segments": [asdict(seg) for seg in segments]
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate timestamped captions for videos using LLaVA JoyCaption"
    )

    parser.add_argument(
        "--video",
        type=str,
        help="Path to local video file"
    )

    parser.add_argument(
        "--r2-key",
        type=str,
        help="R2 object key (e.g., assets/clips/scene_000.mp4)"
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Frame sampling interval in seconds (default: 2.0)"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Frames per batch for unified captioning (default: 5)"
    )

    args = parser.parse_args()

    # Validate input
    if not args.video and not args.r2_key:
        parser.error("Must provide either --video or --r2-key")

    # Create config
    config = CaptionConfig(
        sampling_interval=args.interval,
        frames_per_batch=args.batch_size
    )

    # Initialize captioner
    captioner = VideoCaption(config)

    # Load video
    if args.video:
        print(f"📂 Loading video from: {args.video}")
        video_bytes = Path(args.video).read_bytes()
        video_path = args.video
    else:
        # R2 integration (requires env vars)
        print(f"☁️  Downloading from R2: {args.r2_key}")
        import boto3

        account_id = os.environ.get("R2_ACCOUNT_ID")
        access_key = os.environ.get("R2_ACCESS_KEY_ID")
        secret_key = os.environ.get("R2_SECRET_KEY")
        bucket = os.environ.get("R2_BUCKET", "storygen")

        if not all([account_id, access_key, secret_key]):
            print("❌ Error: R2 credentials not found in environment")
            print("   Set: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_KEY")
            sys.exit(1)

        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="auto"
        )

        obj = s3.get_object(Bucket=bucket, Key=args.r2_key)
        video_bytes = obj["Body"].read()
        video_path = args.r2_key

    # Process video
    result = captioner.process_video(video_bytes, video_path)

    # Output JSON
    print("\n" + "="*80)
    print(json.dumps(result, indent=2))
    print("="*80)


if __name__ == "__main__":
    main()
