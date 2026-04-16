# Image & Video Captioning Alternatives Guide

> **Last Updated**: February 2025
> **Purpose**: Reference guide for image/video captioning solutions, especially for adult content processing where commercial APIs have restrictions.

## Table of Contents

1. [Problem Context](#problem-context)
2. [Critical Consideration: Adult Content](#critical-consideration-adult-content)
3. [Recommended Solutions](#recommended-solutions)
4. [Commercial APIs (SFW Only)](#commercial-apis-sfw-only)
5. [Serverless GPU Platforms](#serverless-gpu-platforms)
6. [Local/Self-Hosted Options](#localself-hosted-options)
7. [Cost Optimization Strategies](#cost-optimization-strategies)
8. [Implementation Examples](#implementation-examples)
9. [Cost Comparison](#cost-comparison)
10. [Decision Matrix](#decision-matrix)

---

## Problem Context

The asset library feature processes videos to generate video description files. The current workflow:

1. Extract frames from video
2. Process images with **JoyCaption 2** model
3. Generate clip descriptions using **Grok API**

**Challenge**: JoyCaption 2 requires significant GPU resources (~16GB VRAM) and cannot run on standard development machines. Currently requires AWS EC2 Deep Learning instances.

**Goal**: Find easier, cheaper, or more accessible alternatives.

---

## Critical Consideration: Adult Content

### APIs That BLOCK Adult/NSFW Images

| Provider | Policy | Behavior |
|----------|--------|----------|
| OpenAI (GPT-4o/Vision) | Strict block | Returns safety policy error |
| Claude Vision | Strict block | Refuses to process |
| Google Gemini | Strict block | Content filtered |
| Groq (LLaVA) | Filtered | May refuse NSFW |
| Together AI (Llama Vision) | Filtered | May refuse NSFW |
| Cloudflare Workers AI | Filtered | Unknown exact behavior |
| SambaNova | Filtered | Unknown exact behavior |

**Bottom Line**: All major commercial APIs have content policies blocking NSFW image analysis.

### APIs/Models That ALLOW Adult Content

| Solution | Type | Notes |
|----------|------|-------|
| **JoyCaption** | Open Source | Purpose-built for NSFW, "equal coverage of SFW and NSFW" |
| **Llama 3.2 Vision Uncensored** | Open Source | Requires self-hosting |
| **X-Ray Alpha** | Open Source | Fully uncensored VLM |
| **Self-hosted open models** | Any | No restrictions when you control the model |

---

## Recommended Solutions

### For Adult Content (Primary Use Case)

#### Option 1: JoyCaption on RunPod Serverless (RECOMMENDED)

**Why**: Purpose-built for training diffusion models, explicitly supports NSFW, pay-per-use.

```
Setup: One-time RunPod configuration
Cost: ~$0.50-1.00 per 1000 images
Quality: Excellent (same as current)
Effort: Medium (one-time setup)
```

#### Option 2: JoyCaption on Modal Labs

**Why**: $30 free monthly credits, fast cold starts.

```
Setup: Deploy with Python script
Cost: $30 free/month, then ~$0.001/image
Quality: Excellent
Effort: Medium
```

#### Option 3: Local with Ollama (if you have GPU)

**Why**: Zero ongoing cost, full control.

```
Setup: ollama pull + script
Cost: $0 (electricity only)
Quality: Good (Moondream) to Excellent (LLaVA)
Effort: Low
Requirements: 8GB+ VRAM for LLaVA, CPU-only for Moondream
```

---

## Commercial APIs (SFW Only)

> **Warning**: These will NOT work for adult content.

### Tier 1: Best Quality + Reasonable Price

| Provider | Model | Cost/Image | Quality | Speed |
|----------|-------|------------|---------|-------|
| Google Gemini | 2.5 Flash | ~$0.001 | Excellent | Fast |
| OpenAI | GPT-4o | ~$0.002-0.003 | Excellent | Fast |
| Claude | 3.5 Sonnet | ~$0.001-0.003 | Excellent | Fast |

### Tier 2: Budget Options

| Provider | Model | Cost/Image | Quality | Speed |
|----------|-------|------------|---------|-------|
| Together AI | Llama Vision FREE | $0 (rate limited) | Good | Fast |
| Fireworks AI | Qwen 2.5 VL | ~$0.0005 | Very Good | Very Fast |
| DeepSeek | V3 Vision | ~$0.0003 | Good | Fast |

### Tier 3: Free Tiers (Stack for Maximum Free Usage)

| Provider | Free Tier | Limit | Vision Model |
|----------|-----------|-------|--------------|
| Groq | Generous | ~100+ req/day | LLaVA 1.5 7B |
| SambaNova | Free API key | Unknown | Llama 4 Maverick |
| Together AI | $25 credits + Llama-Vision-Free | 36 req/hr | Llama 3.2 11B |
| OpenRouter | Multiple free models | Varies | Llama 4 Maverick/Scout |
| Cloudflare Workers AI | 10,000 Neurons/day | ~100-200 images | Llama 3.2 11B |
| Google AI Studio | 20-50 req/day (reduced Dec 2025) | ~50 images | Gemini 2.5 Flash |

---

## Serverless GPU Platforms

### RunPod Serverless

**Best for**: JoyCaption deployment, high volume processing

```yaml
Pricing:
  - T4 GPU: $0.40/hr
  - A10G GPU: $0.75/hr
  - A100 GPU: $2.17/hr

Features:
  - Pay only when processing
  - OpenAI-compatible vLLM API
  - FlashBoot reduces cold start to ~10s
  - Auto-scaling to thousands of GPUs
```

**JoyCaption Configuration**:
```bash
Model: fancyfeast/llama-joycaption-beta-one-hf-llava
Max Model Length: 4096
GPU: A10G or A100 (16GB+)
Enable Prefix Caching: Yes
FlashBoot: Enabled
Idle Timeout: 15 seconds
```

### Modal Labs

**Best for**: Flexibility, experimentation, Python-native deployment

```yaml
Pricing:
  - $30 free credits/month
  - T4: ~$0.27/hr
  - A100-40GB: ~$2.78/hr

Features:
  - Sub-second cold starts
  - Native Python deployment
  - Built-in secrets management
  - Volume mounting for models
```

### Replicate

**Best for**: Easiest setup, pre-built models

```yaml
Pricing:
  - ~$0.001-0.01 per prediction
  - Pay per output

Features:
  - Many vision models ready to use
  - Simple API
  - No deployment needed
```

### fal.ai

**Best for**: Zero cold start, production use

```yaml
Pricing:
  - Pay per output
  - Model-specific pricing

Features:
  - ~0ms cold start
  - Moondream2 ready to use
  - Any-VLM routing (Claude/Gemini/Llama)
```

---

## Local/Self-Hosted Options

### Ollama (Easiest Local Setup)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# For CPU-only (works without GPU!)
ollama pull moondream        # 1.86B params, ~3-5s/image on CPU

# For GPU (8GB+ VRAM)
ollama pull llava:7b-q4_0    # 4-bit quantized, ~4GB VRAM
ollama pull llava:13b        # Better quality, ~8GB VRAM
```

**API Usage**:
```python
import requests
import base64

def caption_with_ollama(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "moondream",  # or "llava:7b-q4_0"
            "prompt": "Describe this image in detail for training a diffusion model.",
            "images": [image_b64]
        }
    )
    return response.json()["response"]
```

### Llama 3.2 Vision Uncensored (For NSFW)

**Hugging Face**: `Guilherme34/Llama-3.2-11b-vision-uncensored`

```python
from transformers import AutoProcessor, LlavaForConditionalGeneration
from peft import PeftModel
import torch

# Load base model with 4-bit quantization
model = LlavaForConditionalGeneration.from_pretrained(
    "alpindale/Llama-3.2-11B-Vision-Instruct",
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16
)

# Apply uncensored adapter
model = PeftModel.from_pretrained(
    model,
    "Guilherme34/Llama-3.2-11b-vision-uncensored"
)

processor = AutoProcessor.from_pretrained(
    "alpindale/Llama-3.2-11B-Vision-Instruct"
)
```

### JoyCaption Local (Current Approach)

See `VIDEO_CAPTION_README.md` for current implementation details.

**Requirements**: 16GB+ VRAM, CUDA-capable GPU

---

## Cost Optimization Strategies

### Strategy 1: Keyframe Extraction (99% Cost Reduction)

Don't process every frame - extract only frames that differ significantly.

```python
import cv2
import numpy as np

def extract_keyframes(video_path: str, threshold: float = 30.0) -> list:
    """
    Extract only frames that differ significantly from previous.
    Typically reduces 1800 frames (1 min @ 30fps) to 10-20 keyframes.
    """
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    keyframes = []
    frame_indices = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            keyframes.append(frame)
            frame_indices.append(frame_idx)
        else:
            diff = cv2.absdiff(prev_frame, gray).mean()
            if diff > threshold:
                keyframes.append(frame)
                frame_indices.append(frame_idx)

        prev_frame = gray
        frame_idx += 1

    cap.release()
    return keyframes, frame_indices
```

### Strategy 2: Perceptual Hashing (Deduplication)

Skip visually similar frames using perceptual hashing.

```python
import imagehash
from PIL import Image

def deduplicate_frames(frames: list, threshold: int = 5) -> list:
    """Remove near-duplicate frames using perceptual hashing."""
    unique_frames = []
    seen_hashes = []

    for frame in frames:
        img = Image.fromarray(frame)
        phash = imagehash.phash(img)

        is_duplicate = any(phash - h < threshold for h in seen_hashes)

        if not is_duplicate:
            unique_frames.append(frame)
            seen_hashes.append(phash)

    return unique_frames
```

### Strategy 3: Caption Caching

Never re-process the same image twice.

```python
import hashlib
import json
from pathlib import Path

CACHE_FILE = Path("caption_cache.json")

def get_cached_caption(image_bytes: bytes, caption_func) -> str:
    """Cache captions to avoid re-processing."""
    img_hash = hashlib.md5(image_bytes).hexdigest()

    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text())

    if img_hash in cache:
        return cache[img_hash]  # Free!

    caption = caption_func(image_bytes)
    cache[img_hash] = caption
    CACHE_FILE.write_text(json.dumps(cache))

    return caption
```

### Strategy 4: Two-Stage Processing

Use free/cheap model to filter, quality model only for interesting frames.

```python
def process_video_two_stage(frames: list) -> list:
    """
    Stage 1: Free model filters uninteresting frames
    Stage 2: Quality model captions only interesting frames
    """
    # Stage 1: Quick filter with free API
    interesting_frames = []
    for frame in frames:
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is this frame interesting or just static? Reply YES or NO only."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"}}
                ]
            }]
        )
        if "YES" in response.choices[0].message.content:
            interesting_frames.append(frame)

    # Stage 2: Quality captions for filtered frames only
    captions = []
    for frame in interesting_frames:
        caption = joycaption_client.caption(frame)  # Paid/quality model
        captions.append(caption)

    return captions
```

### Strategy 5: Batch Processing with Gemini

Google Gemini offers 50% discount for batch processing (24hr turnaround).

```python
import google.generativeai as genai

genai.configure(api_key="your-key")

# Use batch API for 50% discount
batch_request = genai.BatchRequest()
for image in images:
    batch_request.add(
        model="gemini-2.5-flash",
        contents=[
            "Describe this image in detail.",
            image
        ]
    )

# Submit batch (results in 24 hours)
batch_result = batch_request.submit()
```

---

## Implementation Examples

### Example 1: RunPod JoyCaption (Recommended for NSFW)

```python
from openai import OpenAI
import base64

# Configure RunPod endpoint
client = OpenAI(
    api_key="your-runpod-api-key",
    base_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1"
)

def caption_with_joycaption(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="fancyfeast/llama-joycaption-beta-one-hf-llava",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Write a detailed caption for this image, describing the scene, subjects, actions, and mood."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                }
            ]
        }],
        max_tokens=500
    )

    return response.choices[0].message.content
```

### Example 2: Free Tier Stacking (SFW Only)

```python
import os
from typing import Optional

class MultiProviderCaptioner:
    """Rotate between free tier providers to maximize free usage."""

    def __init__(self):
        self.providers = [
            self._caption_groq,
            self._caption_together,
            self._caption_cloudflare,
        ]
        self.current_provider = 0

    def caption(self, image_b64: str) -> str:
        # Try providers in rotation, fall back on rate limit
        for _ in range(len(self.providers)):
            try:
                provider = self.providers[self.current_provider]
                result = provider(image_b64)
                self.current_provider = (self.current_provider + 1) % len(self.providers)
                return result
            except Exception as e:
                if "rate" in str(e).lower():
                    self.current_provider = (self.current_provider + 1) % len(self.providers)
                    continue
                raise
        raise Exception("All providers rate limited")

    def _caption_groq(self, image_b64: str) -> str:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            }]
        )
        return response.choices[0].message.content

    def _caption_together(self, image_b64: str) -> str:
        from together import Together
        client = Together(api_key=os.environ["TOGETHER_API_KEY"])
        response = client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            }]
        )
        return response.choices[0].message.content

    def _caption_cloudflare(self, image_b64: str) -> str:
        import requests
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CF_ACCOUNT_ID']}/ai/run/@cf/meta/llama-3.2-11b-vision-instruct",
            headers={"Authorization": f"Bearer {os.environ['CF_API_TOKEN']}"},
            json={
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail."},
                        {"type": "image", "image": image_b64}
                    ]
                }]
            }
        )
        return response.json()["result"]["response"]
```

### Example 3: Local Ollama (Zero Cost)

```python
import requests
import base64
from pathlib import Path

class OllamaCaptioner:
    """Local captioning with Ollama - zero API cost."""

    def __init__(self, model: str = "moondream"):
        self.model = model
        self.base_url = "http://localhost:11434"

    def caption(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": "Describe this image in detail, including the subjects, their actions, the setting, lighting, and mood.",
                "images": [image_b64],
                "stream": False
            }
        )

        return response.json()["response"]

    def batch_caption(self, image_paths: list) -> list:
        """Caption multiple images sequentially."""
        return [self.caption(path) for path in image_paths]

# Usage
captioner = OllamaCaptioner(model="moondream")  # CPU-friendly
# captioner = OllamaCaptioner(model="llava:7b-q4_0")  # GPU, better quality

caption = captioner.caption("/path/to/image.jpg")
```

---

## Cost Comparison

### Per 1000 Images

| Solution | Cost | Quality | NSFW Support | Setup |
|----------|------|---------|--------------|-------|
| **AWS EC2 + JoyCaption** (current) | $5-15 | Excellent | Yes | High |
| **RunPod Serverless + JoyCaption** | $0.50-1.00 | Excellent | Yes | Medium |
| **Modal Labs + JoyCaption** | $0-1.00 | Excellent | Yes | Medium |
| **Replicate JoyCaption** | ~$10 | Excellent | Yes | Very Low |
| **Stacked Free APIs** | $0 | Good | No | Low |
| **Local Moondream (CPU)** | $0 | Good | Yes | Very Low |
| **Local LLaVA (GPU)** | $0 | Very Good | Yes | Low |
| **Gemini Batch** | ~$0.50 | Excellent | No | Very Low |

### Monthly Estimate (10,000 Images)

| Solution | Monthly Cost |
|----------|-------------|
| EC2 Deep Learning (current) | $50-150 |
| RunPod Serverless | $5-10 |
| Modal Labs | $0-10 (free tier) |
| Local GPU | $0 |
| Free APIs (SFW) | $0 |

---

## Decision Matrix

### Choose RunPod Serverless + JoyCaption if:
- Processing adult/NSFW content
- Want same quality as current setup
- Prefer pay-per-use over server management
- Processing 100+ images regularly

### Choose Modal Labs if:
- Want to try with free credits first
- Need fastest cold starts
- Comfortable with Python deployment
- Processing variable volumes

### Choose Local Ollama if:
- Have a GPU (8GB+ VRAM) OR willing to use CPU (slower)
- Processing adult content
- Want zero ongoing cost
- Privacy is important

### Choose Stacked Free APIs if:
- SFW content only
- Budget is primary concern
- Low volume (<500 images/day)
- Quality is "good enough"

### Keep EC2 Deep Learning if:
- Already have infrastructure
- Need guaranteed availability
- Processing very high volumes
- Cost is not primary concern

---

## Quick Reference: API Keys Needed

| Provider | Environment Variable | Get Key At |
|----------|---------------------|------------|
| RunPod | `RUNPOD_API_KEY` | https://runpod.io/console/user/settings |
| Groq | `GROQ_API_KEY` | https://console.groq.com/keys |
| Together AI | `TOGETHER_API_KEY` | https://api.together.xyz/settings/api-keys |
| Cloudflare | `CF_API_TOKEN`, `CF_ACCOUNT_ID` | https://dash.cloudflare.com/profile/api-tokens |
| SambaNova | `SAMBANOVA_API_KEY` | https://cloud.sambanova.ai/ |
| OpenRouter | `OPENROUTER_API_KEY` | https://openrouter.ai/keys |
| Google AI | `GOOGLE_API_KEY` | https://aistudio.google.com/app/apikey |

---

## Resources & Links

### Models
- [JoyCaption GitHub](https://github.com/fpgaminer/joycaption)
- [JoyCaption Beta on HuggingFace](https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava)
- [Llama 3.2 Vision Uncensored](https://huggingface.co/Guilherme34/Llama-3.2-11b-vision-uncensored)
- [Moondream](https://moondream.ai/)

### Platforms
- [RunPod Serverless Docs](https://docs.runpod.io/serverless/vllm/get-started)
- [Modal Labs](https://modal.com/)
- [Replicate Vision Models](https://replicate.com/collections/vision-models)
- [fal.ai](https://fal.ai/)

### APIs
- [Groq Vision Docs](https://console.groq.com/docs/vision)
- [Together AI Vision](https://docs.together.ai/docs/vision-overview)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- [OpenRouter Free Models](https://openrouter.ai/collections/free-models)

---

## Changelog

- **2025-02**: Initial documentation created from research session
