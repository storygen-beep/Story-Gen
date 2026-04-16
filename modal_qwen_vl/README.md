# Modal Qwen2.5-VL Video Captioning

Direct video-to-description captioning using Qwen2.5-VL on Modal serverless GPUs.

**Replaces:** JoyCaption frame extraction → Grok aggregation pipeline
**With:** Single video → description API call

## Cost Comparison

| Approach | API Calls per Clip | Approx Cost |
|----------|-------------------|-------------|
| Old (JoyCaption + Grok) | ~25 frame captions + 1 aggregation | ~$0.05-0.10 |
| New (Qwen2.5-VL direct) | 1 | ~$0.01-0.02 |

## Setup

### 1. Install Modal

```bash
pip install modal
```

### 2. Create Modal Account & Authenticate

```bash
# This opens browser to create/login to Modal account
modal setup
```

### 3. Deploy the App

```bash
cd story_gen_django
modal deploy modal_qwen_vl/app.py
```

You'll see output like:
```
✓ Created objects.
├── 🔨 Created QwenVLCaptioner.
├── 🔨 Created caption_endpoint => https://your-username--qwen-vl-video-captioner-caption-endpoint.modal.run
└── 🔨 Created model volume.
```

**Save the endpoint URL** - you'll need it for Django config.

### 4. Test It

```bash
# Test with a video URL
modal run modal_qwen_vl/app.py --video-url "https://example.com/sample.mp4"

# Test with a local file
modal run modal_qwen_vl/app.py --video-path "./test_video.mp4"
```

## Django Integration

### Add to Settings

```python
# config/settings/base.py

MODAL_QWEN_VL_ENDPOINT = env(
    "MODAL_QWEN_VL_ENDPOINT",
    default="https://your-username--qwen-vl-video-captioner-caption-endpoint.modal.run"
)
```

### Use in Code

```python
from modal_qwen_vl import ModalQwenVLClient

# Initialize client
client = ModalQwenVLClient(
    endpoint_url=settings.MODAL_QWEN_VL_ENDPOINT
)

# Caption a video (URL or file path)
result = client.caption_video("https://r2.example.com/clips/clip_001.mp4")

print(result["description"])  # The video description
print(result["model"])        # "Qwen/Qwen2.5-VL-7B-Instruct"
print(result["output_tokens"])  # Token count
```

### Replace Existing Pipeline

In your `processing.py`, replace the frame extraction + Grok aggregation:

```python
# OLD (multiple steps)
# frames = extract_frames(clip_path)
# captions = [joycaption.caption(f) for f in frames]
# description = grok.aggregate(captions)

# NEW (single call)
from modal_qwen_vl import caption_video_modal

description = caption_video_modal(clip.signed_url)
clip.description = description
clip.description_model = "qwen2.5-vl-7b"
clip.save()
```

## API Reference

### HTTP Endpoint

```bash
curl -X POST https://your-endpoint.modal.run \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "prompt": "Describe this video in detail...",
    "max_tokens": 800
  }'
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `video_url` | string | Yes* | URL to video file |
| `video_base64` | string | Yes* | Base64-encoded video |
| `prompt` | string | No | Custom prompt (has NSFW default) |
| `max_tokens` | int | No | Max output tokens (default: 800) |

*Provide either `video_url` OR `video_base64`

**Response:**
```json
{
  "description": "The video shows...",
  "model": "Qwen/Qwen2.5-VL-7B-Instruct",
  "input_tokens": 8234,
  "output_tokens": 612
}
```

## Configuration Options

### Switch to Uncensored Model

Edit `app.py`:

```python
# Change this line
MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

# To this (fully uncensored)
MODEL_ID = "prithivMLmods/Qwen2.5-VL-7B-Abliterated-Caption-it"
```

Then redeploy: `modal deploy modal_qwen_vl/app.py`

### Change GPU

```python
# In app.py, change GPU_CONFIG:

# Budget option (slower, cheaper)
GPU_CONFIG = modal.gpu.T4()  # ~$0.30/hr

# Default (good balance)
GPU_CONFIG = modal.gpu.L40S()  # ~$1.95/hr

# High performance
GPU_CONFIG = modal.gpu.A100(size="40GB")  # ~$2.10/hr

# Maximum (for 72B model)
GPU_CONFIG = modal.gpu.A100(size="80GB")  # ~$3.50/hr
```

### Adjust Concurrency

```python
@app.cls(
    gpu=GPU_CONFIG,
    allow_concurrent_inputs=4,  # Process 4 videos at once
    container_idle_timeout=300,  # Keep warm for 5 minutes
)
```

## Monitoring

### View Logs

```bash
modal logs qwen-vl-video-captioner
```

### Check Usage

Visit [modal.com/usage](https://modal.com/usage) to see:
- GPU hours used
- Cost breakdown
- Request counts

## Pricing Estimate

| Volume | GPU Time | Est. Cost |
|--------|----------|-----------|
| 100 clips | ~30 min | ~$1 |
| 1,000 clips | ~5 hours | ~$10 |
| 10,000 clips | ~50 hours | ~$100 |

*Based on L40S @ $1.95/hr, ~20 seconds per clip*

**Free tier:** $30/month credits (~15 GPU-hours)

## Troubleshooting

### Cold Start Taking Too Long

First request after idle takes ~60-90 seconds (model loading). Subsequent requests are fast.

To keep warm:
```python
container_idle_timeout=600,  # 10 minutes
```

### Out of Memory

Reduce video resolution in the prompt:
```python
{"type": "video", "video": url, "max_pixels": 256 * 256, "fps": 0.5}
```

### Rate Limiting

Increase concurrency:
```python
allow_concurrent_inputs=8,
```

Or deploy multiple replicas:
```python
@app.cls(
    gpu=GPU_CONFIG,
    min_containers=2,  # Always have 2 ready
)
```
