# 🎬 Video Caption Generator - Google Colab Quick Start

## 📤 Upload to Google Colab

1. **Go to Google Colab**: https://colab.research.google.com/
2. **Upload the notebook**:
   - Click `File` → `Upload notebook`
   - Select `Video_Caption_Generator_Colab.ipynb`
3. **Set GPU runtime**:
   - Click `Runtime` → `Change runtime type`
   - Select `GPU` (T4 recommended)
   - Click `Save`

## 🚀 Quick Start (6 Steps)

### Step 1: Check GPU
Run the first cell to verify GPU is available:
```
✅ PyTorch version: 2.x
✅ CUDA available: True
✅ GPU: Tesla T4
```

### Step 2: Install Dependencies
Run the installation cell (takes ~2 minutes):
```
✅ All dependencies installed
```

### Step 3: Load Model
Run model loading cell (takes ~3 minutes first time):
```
✅ Model loaded on cuda
```

### Step 4: Configure R2
Set your Cloudflare R2 credentials in cell 13:
```python
R2_ACCOUNT_ID = "your_account_id"
R2_ACCESS_KEY_ID = "your_access_key"
R2_SECRET_KEY = "your_secret_key"
R2_BUCKET = "storygen"  # Your bucket name
```

### Step 5: Configure Jobs
Edit the JOBS list in cell 15 to add your videos:
```python
JOBS = [
    {
        "id": "scene_000.mp4",
        "clip_path": "assets/clips/scene_000.mp4",
        "status": "pending",
        "caption": None
    },
]
```

### Step 6: Process Videos
Run cell 18 to process all pending jobs. Results will be displayed automatically!

## 📊 Expected Output

```json
{
  "metadata": {
    "video_path": "scene_000.mp4",
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
      "caption": "Unified caption for first 10 seconds"
    }
    // ... more segments
  ]
}
```

Plus a pretty HTML table view!

## ⚙️ Configuration Options

### Adjust Sampling Rate
```python
SAMPLING_INTERVAL = 3.0  # Extract frame every 3 seconds instead of 2
```

### Adjust Batch Size
```python
FRAMES_PER_BATCH = 7  # Process 7 frames together instead of 5
```

After changing, re-run the processing cells.

## 🎯 Features

✅ **Full Video Coverage** - No frame limits
✅ **Time-Based Sampling** - Every 2 seconds (configurable)
✅ **Unified Captions** - Coherent narratives for each segment
✅ **Timestamped Output** - Each segment has start/end times
✅ **R2 Integration** - Load videos directly from cloud storage
✅ **Pretty Display** - HTML table view in Colab
✅ **Downloadable Results** - Save JSON file

## ⏱️ Performance

| Video Length | Frames | Batches | Processing Time |
|--------------|--------|---------|-----------------|
| 30 seconds | 15 | 3 | ~10 seconds |
| 2 minutes | 60 | 12 | ~40 seconds |
| 5 minutes | 150 | 30 | ~90 seconds |
| 10 minutes | 300 | 60 | ~3 minutes |

**GPU Required**: Tesla T4 or better (free tier works!)

## 💡 Tips

1. **Free Tier**: Google Colab free tier works perfectly
2. **GPU Runtime**: Always use GPU, not CPU
3. **Large Videos**: For videos >10 minutes, increase `SAMPLING_INTERVAL` to 3.0 or 5.0
4. **VRAM Error**: If out of memory, reduce `FRAMES_PER_BATCH` to 3
5. **Multiple Videos**: Just re-run the upload/processing cells for each video

## 📝 Example Workflow

```python
# 1. Upload video
uploaded = files.upload()  # Select your video

# 2. Process
result = process_video(video_bytes, video_filename)

# 3. View results
display(HTML(html))  # Pretty table

# 4. Download JSON
files.download(f"{video_filename}_captions.json")
```

## 🐛 Troubleshooting

### "CUDA out of memory"
```python
# Reduce batch size
FRAMES_PER_BATCH = 3

# Or increase sampling interval
SAMPLING_INTERVAL = 3.0
```

### "No GPU available"
- Runtime → Change runtime type → GPU → Save
- Restart runtime

### "R2 connection failed"
- Check credentials are correct
- Use Option 1 (upload local file) instead

### "FFmpeg not found"
- Should auto-install, but if not:
```python
!apt-get install -y ffmpeg
```

## 🔗 Related Files

- `Untitled0.ipynb` - Original notebook with fixes
- `video_caption_generator.py` - Standalone Python script version
- `VIDEO_CAPTION_README.md` - Detailed documentation

## 📧 Notes

- **Model**: Uses LLaVA JoyCaption (float16, no quantization)
- **VRAM**: Requires ~16GB (T4 has 16GB - perfect fit!)
- **All Fixes Applied**: attention_mask dtype fix, no quantization issues
- **Colab Optimized**: Progress bars, pretty output, file downloads

Happy captioning! 🎬✨
