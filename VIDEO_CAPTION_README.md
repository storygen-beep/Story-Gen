# Video Caption Generator

Comprehensive video captioning using LLaVA JoyCaption with time-based frame sampling and unified batch captioning.

## Features

✅ **Full Video Coverage** - No frame limits, processes entire video
✅ **Time-Based Sampling** - Extract frames every N seconds (default: 2s)
✅ **Unified Batch Captions** - Process 5 frames together for coherent narratives
✅ **Timestamped Segments** - Each segment has start/end times
✅ **Structured JSON Output** - Easy to parse and integrate
✅ **R2 Cloud Storage** - Direct integration with Cloudflare R2
✅ **Fixed Dtype Issues** - All "Half and Byte" errors resolved

## Requirements

```bash
# All dependencies already installed in Django project
torch>=2.8.0
transformers>=4.57.1
pillow>=10.4.0
boto3
ffmpeg (system package)
```

## Quick Start

### Option 1: Local Video File

```bash
python video_caption_generator.py --video /path/to/video.mp4
```

### Option 2: R2 Cloud Storage

```bash
# Set environment variables
export R2_ACCOUNT_ID="your_account_id"
export R2_ACCESS_KEY_ID="your_access_key"
export R2_SECRET_KEY="your_secret_key"
export R2_BUCKET="storygen"

# Process video from R2
python video_caption_generator.py --r2-key assets/clips/scene_000.mp4
```

## Configuration Options

```bash
# Custom sampling interval (default: 2.0 seconds)
python video_caption_generator.py --video video.mp4 --interval 3.0

# Custom batch size (default: 5 frames)
python video_caption_generator.py --video video.mp4 --batch-size 7

# Combined options
python video_caption_generator.py \
  --video video.mp4 \
  --interval 1.5 \
  --batch-size 5
```

## Output Format

```json
{
  "metadata": {
    "video_path": "assets/clips/scene_000.mp4",
    "duration_seconds": 45.0,
    "frames_sampled": 23,
    "batches_processed": 5,
    "sampling_interval": 2.0,
    "processing_time_seconds": 18.3
  },
  "segments": [
    {
      "segment_id": 1,
      "start_time": "0:00",
      "end_time": "0:10",
      "frames_analyzed": 5,
      "frame_timestamps": [0.0, 2.0, 4.0, 6.0, 8.0],
      "caption": "A woman enters a modern office and walks through the reception area toward the elevators"
    },
    {
      "segment_id": 2,
      "start_time": "0:10",
      "end_time": "0:20",
      "frames_analyzed": 5,
      "frame_timestamps": [10.0, 12.0, 14.0, 16.0, 18.0],
      "caption": "She takes the elevator to an upper floor and exits into a hallway with glass-walled offices"
    }
  ]
}
```

## How It Works

### 1. Frame Extraction
- Video is analyzed to determine duration
- Frames extracted at regular intervals (every 2s by default)
- All frames downscaled to 672px max dimension for VRAM efficiency

### 2. Batching
- Frames grouped into batches of 5 (configurable)
- Each batch represents ~10 seconds of video content
- Last batch may have fewer frames if total not divisible by batch size

### 3. Unified Captioning
- All frames in batch sent to model together
- LLaVA generates single coherent caption understanding temporal progression
- Much better than individual frame captions concatenated

### 4. Structured Output
- Each segment includes timing, frames analyzed, and caption
- Metadata tracks processing statistics
- JSON format for easy parsing and storage

## Performance Expectations

| Video Length | Frames (2s interval) | Batches | Est. Time | VRAM |
|--------------|---------------------|---------|-----------|------|
| 30 seconds | 15 | 3 | ~10s | ~16GB |
| 2 minutes | 60 | 12 | ~40s | ~16GB |
| 5 minutes | 150 | 30 | ~90s | ~16GB |
| 10 minutes | 300 | 60 | ~3min | ~16GB |

**Note**: Uses float16 model without quantization (~16GB VRAM required)

## Architecture Details

### Model Configuration
- **Model**: `fancyfeast/llama-joycaption-alpha-two-hf-llava`
- **Precision**: float16 (no quantization)
- **Attention**: Eager mode (SDPA disabled)
- **Device**: CUDA with optimized memory settings

### Key Fixes Applied
1. **Attention Mask Dtype** - Force int64 before GPU transfer
2. **No Quantization** - Vision tower incompatible with 4-bit
3. **SDPA Disabled** - Prevents dtype conflicts
4. **Proper Batching** - Multi-image support for LLaVA

### Error Handling
- Validates video duration before processing
- Handles missing frames gracefully
- VRAM clearing after each batch
- R2 credential validation

## Sampling Strategy Comparison

| Interval | Coverage | Speed | Best For |
|----------|----------|-------|----------|
| 1 second | Very Dense | Slow | Action scenes, sports |
| **2 seconds** ⭐ | Dense | Moderate | General purpose |
| 3 seconds | Good | Fast | Dialogue, static scenes |
| 5 seconds | Basic | Very Fast | Slow-moving content |

## Troubleshooting

### Out of Memory Error
```bash
# Reduce batch size
python video_caption_generator.py --video video.mp4 --batch-size 3

# Increase sampling interval
python video_caption_generator.py --video video.mp4 --interval 3.0
```

### R2 Connection Failed
```bash
# Verify credentials are set
echo $R2_ACCOUNT_ID
echo $R2_ACCESS_KEY_ID

# Test R2 connection
python -c "import boto3; s3=boto3.client('s3', endpoint_url='https://$R2_ACCOUNT_ID.r2.cloudflarestorage.com', aws_access_key_id='$R2_ACCESS_KEY_ID', aws_secret_access_key='$R2_SECRET_KEY', region_name='auto'); print(s3.list_objects_v2(Bucket='$R2_BUCKET', MaxKeys=1))"
```

### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

## Integration Examples

### Save to File
```bash
python video_caption_generator.py --video video.mp4 > captions.json
```

### Parse in Python
```python
import subprocess
import json

result = subprocess.check_output([
    "python", "video_caption_generator.py",
    "--video", "video.mp4"
])

data = json.loads(result)
for segment in data["segments"]:
    print(f"{segment['start_time']} - {segment['caption']}")
```

### Django Integration
```python
from pathlib import Path
import subprocess
import json

def caption_video(video_path: str) -> dict:
    """Generate captions for video"""
    script = Path(__file__).parent / "video_caption_generator.py"

    result = subprocess.check_output([
        "python", str(script),
        "--video", video_path
    ])

    return json.loads(result)

# Usage
captions = caption_video("/path/to/video.mp4")
```

## Future Enhancements

- [ ] Support for multiple captioning modes (dense/sparse/keyframe)
- [ ] Scene detection for adaptive sampling
- [ ] Batch processing of multiple videos
- [ ] GPU memory auto-scaling
- [ ] Caption quality confidence scores
- [ ] Optional full-video summary generation
- [ ] Support for pre-quantized models (lower VRAM)

## Related Files

- `Untitled0.ipynb` - Original notebook with initial implementation
- `apps/assets/` - Django asset management integration
- `requirements/base.txt` - Python dependencies

## Credits

- Model: [LLaVA JoyCaption Alpha Two](https://huggingface.co/fancyfeast/llama-joycaption-alpha-two-hf-llava)
- Based on fixes for "Half and Byte" dtype error
- Implements comprehensive time-based sampling strategy
