"""
Modal Serverless Qwen3-VL Video Captioning

Deploy with: modal deploy app.py
Test with: modal run app.py --video-url "https://example.com/video.mp4"

This replaces the entire JoyCaption frame extraction + Grok aggregation pipeline
with a single direct video-to-description call.
"""

import modal

# Define the container image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libgl1-mesa-glx", "libglib2.0-0", "git")
    .pip_install(
        "torch>=2.1.0",
        "torchvision>=0.16.0",  # Required by qwen-vl-utils for video processing
        "transformers @ git+https://github.com/huggingface/transformers",  # Qwen3-VL requires >= 4.57
        "accelerate>=0.26.0",
        "qwen-vl-utils[decord]>=0.0.14",  # With decord for faster video loading + video metadata support
        "Pillow",
        "httpx",
        "av",  # For video decoding
        "fastapi[standard]",  # Required for web endpoints
    )
)

app = modal.App("qwen-vl-video-captioner", image=image)

# Persistent volume for model weights (avoids re-downloading)
model_volume = modal.Volume.from_name("qwen-vl-models", create_if_missing=True)

# Model to use - abliterated (uncensored) Qwen3-VL-8B
MODEL_ID = "huihui-ai/Huihui-Qwen3-VL-8B-Instruct-abliterated"


@app.cls(
    gpu="L40S",
    volumes={"/models": model_volume},
    timeout=600,  # 10 min max per request
    scaledown_window=300,  # Keep warm for 5 min
)
class QwenVLCaptioner:
    """Qwen3-VL video captioning service."""

    @modal.enter()
    def load_model(self):
        """Load model once when container starts."""
        import torch
        from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

        print(f"Loading model: {MODEL_ID}")

        self.model = Qwen3VLForConditionalGeneration.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            cache_dir="/models",
        )

        self.processor = AutoProcessor.from_pretrained(
            MODEL_ID,
            cache_dir="/models",
            min_pixels=128 * 28 * 28,   # 100,352 - quality floor
            max_pixels=512 * 28 * 28,   # 401,408 - quality ceiling (balanced for L40S)
        )

        print("Model loaded successfully!")

    @modal.method()
    def caption_video(
        self,
        video_source: str,
        prompt: str | None = None,
        max_tokens: int = 1500,
    ) -> dict:
        """
        Generate description for a video.

        Args:
            video_source: URL or local file path
            prompt: Custom prompt (uses default prompt if None)
            max_tokens: Maximum output tokens (default 1500 for detailed descriptions)

        Returns:
            dict with 'description', 'model', 'tokens_used'
        """
        from qwen_vl_utils import process_vision_info

        # Default NSFW video captioning prompt
        if prompt is None:
            prompt = self._get_default_prompt()

        # Build message with video
        # Balance quality vs memory: 2x resolution, 16 frames
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": video_source,
                        "max_pixels": 360 * 420 * 2,  # 302,400 - 2x resolution (balanced)
                        "fps": 2,  # 2 frames per second - adapts to video length
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Process inputs
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        images, videos, video_kwargs = process_vision_info(
            messages,
            return_video_kwargs=True,
            return_video_metadata=True,
        )

        # Unpack video metadata from tuples
        if videos is not None:
            videos, video_metadatas = zip(*videos)
            videos = list(videos)
            video_metadatas = list(video_metadatas)
        else:
            video_metadatas = None

        # Filter out generation params that don't belong in processor call
        generation_keys = {"temperature", "top_p", "top_k", "do_sample"}
        processor_kwargs = {k: v for k, v in video_kwargs.items() if k not in generation_keys}

        inputs = self.processor(
            text=[text],
            images=images,
            videos=videos,
            video_metadata=video_metadatas,
            padding=True,
            return_tensors="pt",
            **processor_kwargs,
        ).to(self.model.device)

        # Generate with greedy decoding (deterministic output)
        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.3,
            repetition_penalty=1.1,
        )

        # Decode output (skip input tokens)
        generated_ids = output_ids[:, inputs.input_ids.shape[1]:]
        description = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]

        return {
            "description": description.strip(),
            "model": MODEL_ID,
            "input_tokens": inputs.input_ids.shape[1],
            "output_tokens": len(generated_ids[0]),
        }

    @modal.method()
    def caption_video_from_bytes(
        self,
        video_bytes: bytes,
        prompt: str | None = None,
        max_tokens: int = 1500,
    ) -> dict:
        """
        Caption video from raw bytes.

        Args:
            video_bytes: Raw video file bytes
            prompt: Custom prompt
            max_tokens: Max output tokens

        Returns:
            dict with description and metadata
        """
        import tempfile
        import os

        # Save bytes to temp file (Qwen needs file path or URL)
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(video_bytes)
            temp_path = f.name

        try:
            # Use .local() to call the modal.method within the same container
            result = self.caption_video.local(
                video_source=temp_path,
                prompt=prompt,
                max_tokens=max_tokens,
            )
            return result
        finally:
            os.unlink(temp_path)

    @modal.method()
    def caption_batch(
        self,
        videos: list[tuple[str, bytes]],
        prompt: str | None = None,
        max_tokens: int = 1500,
    ) -> list[dict]:
        """
        Process multiple videos sequentially in ONE container.

        Args:
            videos: List of (filename, video_bytes) tuples
            prompt: Custom prompt (applies to all videos)
            max_tokens: Max output tokens per video

        Returns:
            List of result dicts with 'filename' added to each
        """
        results = []
        total = len(videos)

        for i, (filename, video_bytes) in enumerate(videos, 1):
            print(f"Processing {i}/{total}: {filename}")

            result = self.caption_video_from_bytes.local(
                video_bytes=video_bytes,
                prompt=prompt,
                max_tokens=max_tokens,
            )
            result["filename"] = filename
            results.append(result)

            print(f"  ✓ Completed: {result['output_tokens']} tokens")

        return results

    def _get_default_prompt(self) -> str:
        """Default prompt for adult video captioning - comprehensive and detailed."""
        return """Describe this adult video clip in exhaustive, explicit detail. Capture EVERYTHING that happens.

CRITICAL: Only describe what you ACTUALLY SEE in the video frames. Do NOT assume, invent, or extrapolate actions that are not clearly visible. If the clip shows groping but no penetration, describe only the groping. If the clip ends before sex, say "the clip ends before penetration" - do not invent what might happen next.

PARTICIPANTS:
- How many people? Genders?
- Physical descriptions: body type, skin tone, hair color/style, any tattoos or distinctive features

SETTING:
- Location (bedroom, kitchen, bathroom, living room, outdoors, shower, pool, etc.)
- Time of day if visible (morning light, evening, night)
- Notable furniture or environment details

CLOTHING & STATE:
- What is each person wearing at the start?
- What clothing gets removed and when during the clip?
- End state: fully nude, partially clothed, or specific items remaining?

ENERGY & MOOD:
- Overall energy: tender, passionate, urgent, playful, dominant, aggressive, romantic, raw/lustful?
- Does the mood shift during the clip?

ACTIVITIES - Describe ALL actions in sequence:
- What happens at the BEGINNING?
- How do activities PROGRESS or change?
- ALL sexual acts: oral (blowjob, deepthroat, cunnilingus, licking), manual (handjob, fingering, stroking, groping), penetration, kissing, grinding
- Which body parts: breasts, nipples, ass, pussy, cock, balls, neck, thighs, etc.
- Multiple activities happening simultaneously?

POSITIONS:
- Name specific positions: missionary, doggy, cowgirl, reverse cowgirl, spooning, prone bone, standing, bent over, etc.
- Do positions change? List the sequence.
- Who is on top/bottom/behind?

DYNAMICS:
- Who initiates or leads?
- Active vs passive roles?
- Does control or dominance shift?

INTENSITY:
- Soft/teasing, moderate, intense, or rough?
- Pace: slow and sensual, building gradually, fast and urgent?

EXPRESSIONS & CONNECTION:
- Eye contact between participants? Looking at camera?
- Visible expressions: pleasure, intensity, ecstasy, playfulness?
- Any visible moaning, talking, or reactions?

CAMERA:
- Angle: close-up, medium, wide shot, POV?
- Movement: static, panning, following action?
- What body parts are emphasized by framing?

UNIQUE ELEMENTS:
- Any distinctive props, furniture, or setting details?
- Lighting quality (natural, dim, bright)?
- What makes this clip visually distinctive?

Be exhaustive and explicit. Use standard position names and anatomical terms. Describe the full progression from start to finish.

ACCURACY IS PARAMOUNT: If you cannot clearly see an action in the video frames, do not describe it. Only describe confirmed visible activities. State what the clip shows, not what you expect or assume happens off-screen.

Do not mention watermarks, logos, or video sources."""


@app.function(gpu="L40S", volumes={"/models": model_volume}, timeout=120)
def caption_single_video(video_url: str, prompt: str | None = None) -> dict:
    """
    Standalone function to caption a single video.
    Useful for one-off calls without instantiating the class.
    """
    captioner = QwenVLCaptioner()
    return captioner.caption_video.local(video_url, prompt)


# Web endpoint for HTTP API access
@app.function(gpu="L40S", volumes={"/models": model_volume}, timeout=600)
@modal.fastapi_endpoint(method="POST")
def caption_endpoint(request: dict) -> dict:
    """
    HTTP endpoint for video captioning.

    POST body:
    {
        "video_url": "https://...",  // or "video_base64": "..."
        "prompt": "optional custom prompt",
        "max_tokens": 1500
    }
    """
    captioner = QwenVLCaptioner()

    video_source = request.get("video_url") or request.get("video_base64")
    if not video_source:
        return {"error": "Must provide video_url or video_base64"}

    # If base64, decode and use bytes method
    if request.get("video_base64"):
        import base64

        video_bytes = base64.b64decode(request["video_base64"])
        return captioner.caption_video_from_bytes.local(
            video_bytes,
            prompt=request.get("prompt"),
            max_tokens=request.get("max_tokens", 1500),
        )

    return captioner.caption_video.local(
        video_source=video_source,
        prompt=request.get("prompt"),
        max_tokens=request.get("max_tokens", 1500),
    )


# CLI entrypoint for testing
@app.local_entrypoint()
def main(
    video_url: str = None,
    video_path: str = None,
    video_dir: str = None,
    output_file: str = None,
    prompt: str = None,
    chunk_size: int = 5,
):
    """
    Caption videos from command line.

    Examples:
        # Single video by URL
        modal run app.py --video-url "https://example.com/video.mp4"

        # Single video by path
        modal run app.py --video-path "./local_video.mp4"

        # Batch process directory (sequential, cost-efficient)
        modal run app.py --video-dir "./clips/"

        # Batch with custom output file
        modal run app.py --video-dir "./clips/" --output-file "./results.json"
    """
    import json
    from pathlib import Path

    captioner = QwenVLCaptioner()

    # === BATCH MODE ===
    if video_dir:
        dir_path = Path(video_dir)
        if not dir_path.exists():
            print(f"Error: Directory not found: {video_dir}")
            return

        # Collect all video files
        video_files = list(dir_path.glob("*.mp4")) + list(dir_path.glob("*.MP4"))
        video_files += list(dir_path.glob("*.webm")) + list(dir_path.glob("*.mov"))
        video_files = sorted(video_files)

        if not video_files:
            print(f"Error: No video files found in {video_dir}")
            return

        # Determine output file
        if output_file:
            out_path = Path(output_file)
        else:
            out_path = dir_path / "descriptions.json"

        total = len(video_files)
        total_chunks = (total + chunk_size - 1) // chunk_size
        print(f"Found {total} videos in {video_dir}")
        print(f"Processing in {total_chunks} chunks of {chunk_size}")
        print("=" * 60)

        all_results = []

        for chunk_start in range(0, total, chunk_size):
            chunk_files = video_files[chunk_start:chunk_start + chunk_size]
            chunk_num = chunk_start // chunk_size + 1

            print(f"\nChunk {chunk_num}/{total_chunks}: Reading {len(chunk_files)} videos...")

            # Read only this chunk's bytes
            chunk_videos = []
            for vf in chunk_files:
                print(f"  Reading: {vf.name}")
                chunk_videos.append((vf.name, vf.read_bytes()))

            print(f"  Sending chunk {chunk_num} to Modal...")
            results = captioner.caption_batch.remote(chunk_videos, prompt)
            all_results.extend(results)

            # Save incrementally after each chunk (crash-safe)
            output_data = {
                "total_videos": len(all_results),
                "model": all_results[0]["model"] if all_results else MODEL_ID,
                "results": {r["filename"]: r for r in all_results}
            }
            with open(out_path, "w") as f:
                json.dump(output_data, f, indent=2)

            print(f"  ✓ Chunk {chunk_num} done ({len(all_results)}/{total} total)")

        print("\n" + "=" * 60)
        print(f"✓ Processed {len(all_results)} videos")
        print(f"✓ Results saved to: {out_path}")

        # Print summary
        total_in = sum(r["input_tokens"] for r in all_results)
        total_out = sum(r["output_tokens"] for r in all_results)
        print(f"✓ Total tokens: {total_in} in, {total_out} out")
        return

    # === SINGLE VIDEO MODE (existing behavior) ===
    if video_path:
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        result = captioner.caption_video_from_bytes.remote(video_bytes, prompt)
    elif video_url:
        result = captioner.caption_video.remote(video_url, prompt)
    else:
        print("Error: Provide --video-url, --video-path, or --video-dir")
        return

    print("\n" + "=" * 60)
    print("VIDEO DESCRIPTION")
    print("=" * 60)
    print(result["description"])
    print("=" * 60)
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
