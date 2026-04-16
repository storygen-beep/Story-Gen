# Twine Media Capture - Chrome Extension

A developer tool for capturing media assets from any website directly into Twine game project folders.

## Overview

This Chrome extension streamlines the asset discovery workflow for game developers. Browse any website, hover over images or videos, and save them directly to your project's media folder with proper naming.

## Features

### Media Detection
- Automatically detects `<img>` and `<video>` elements on any webpage
- Filters out small elements (< 50px) to ignore icons and thumbnails
- Supports lazy-loaded images via `data-src` and `data-lazy-src` attributes
- Uses `MutationObserver` to detect dynamically added content

### One-Click Capture
- Blue download button appears on hover (top-left corner of media)
- Inline form for entering Scene ID without leaving the page
- Keyboard shortcuts: Enter to save, Escape to cancel
- Click outside form to dismiss

### Context Persistence
- Remembers last used game folder and scene ID
- Form pre-fills with stored values for faster workflow
- Context persists across page loads and browser sessions

### URL Parameter Support
Open any URL with parameters to pre-set context:
```
https://google.com/search?q=bedroom+background&_tmc_game=step_sister_wedding&_tmc_scene=bedroom_morning
```

| Parameter | Description |
|-----------|-------------|
| `_tmc_game` | Game folder name |
| `_tmc_scene` | Scene ID for file naming |

### Smart File Handling
- Detects file extension from URL or Content-Type header
- Supports streaming platforms via `yt-dlp` (YouTube, Vimeo, TikTok, Reddit)
- Auto-numbers duplicate filenames (`image.jpg` → `image_1.jpg`)
- Sanitizes paths to prevent directory traversal attacks

### Toast Notifications
- Success: Green toast showing saved file path
- Error: Red toast with error message
- Auto-dismiss after 4 seconds

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (top-right toggle)
3. Click "Load unpacked"
4. Select the `media_capture_extension/` folder
5. Extension icon appears in toolbar (optional - extension works automatically)

## Usage

### Basic Workflow

1. **Start Django backend** (required for file downloads)
   ```bash
   cd story_gen_django
   python manage.py runserver
   ```

2. **Browse to any website** with images or videos

3. **Hover over media** - blue download button appears

4. **Click the button** - form popup appears

5. **Enter Scene ID** (e.g., `bedroom_morning` or `scenes/intro/bg`)

6. **Press Enter or click Save** - file downloads to project folder

7. **Check toast notification** for success/error status

### Setting Game Context

**Option 1: URL Parameters**
```
https://example.com?_tmc_game=my_game&_tmc_scene=intro
```

**Option 2: First Capture**
- Enter game name in the form on first capture
- Context is remembered for subsequent captures

### Nested Folders

Use `/` in Scene ID to create subdirectories:
```
Scene ID: chapter1/day1/bedroom
Result:   my_game/media/chapter1/day1/bedroom.jpg
```

## File Structure

```
media_capture_extension/
├── manifest.json    # Extension configuration (Manifest V3)
├── content.js       # Main logic - detection, UI, API calls
├── styles.css       # Overlay button and form styling
└── FEATURE_DOC.md   # This documentation
```

## Backend API

### Endpoint
```
POST http://localhost:8000/api/v1/dev/media-capture
```

### Request
```json
{
  "url": "https://example.com/image.jpg",
  "scene_id": "bedroom_morning",
  "game": "step_sister_wedding"
}
```

### Response (Success)
```json
{
  "success": true,
  "file_path": "step_sister_wedding/media/bedroom_morning.jpg"
}
```

### Response (Error)
```json
{
  "success": false,
  "error": "File too large: 600000000 bytes"
}
```

## Supported Media

### Direct Downloads
| Type | Extensions |
|------|------------|
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`, `.bmp` |
| Videos | `.mp4`, `.webm`, `.mov`, `.avi`, `.mkv` |
| Audio | `.mp3`, `.wav`, `.ogg`, `.m4a` |

### Streaming Platforms (via yt-dlp)
- YouTube
- Vimeo
- TikTok
- Reddit videos
- Twitter/X videos
- And 1000+ other sites supported by yt-dlp

## Limitations

- **File size**: Maximum 500MB per file
- **Timeout**: 60 seconds per download
- **Local only**: Requires Django backend running on localhost
- **No authentication**: Developer tool only, not for production

## Permissions

| Permission | Purpose |
|------------|---------|
| `activeTab` | Access current tab for media detection |
| `storage` | Persist game/scene context |
| `<all_urls>` | Detect media on any website |
| `localhost:8000` | Communicate with Django backend |

## Troubleshooting

### Button doesn't appear
- Check element is at least 50x50 pixels
- Verify it's an `<img>` or `<video>` element
- Reload page to re-scan media

### Download fails
- Ensure Django server is running (`python manage.py runserver`)
- Check browser console for errors
- Verify URL is accessible (not behind auth)

### Wrong file extension
- Backend detects from URL or Content-Type
- Falls back to `.jpg` if unknown
- Rename file manually if needed

### Duplicate files
- Backend auto-numbers: `file.jpg` → `file_1.jpg`
- Delete unwanted duplicates manually

## Security

- **Path sanitization**: Special characters replaced with underscores
- **No directory traversal**: `..` sequences are filtered
- **Size limits**: 500MB maximum prevents disk abuse
- **Localhost only**: No remote server communication
- **MIME validation**: Rejects HTML disguised as media

## Development

### Modifying the Extension

1. Edit files in `media_capture_extension/`
2. Go to `chrome://extensions/`
3. Click refresh icon on the extension card
4. Reload target webpage to see changes

### Backend Endpoint

Located at: `api/v1/dev.py`

The `media_capture` view handles:
- URL validation
- File downloading (direct or yt-dlp)
- Extension detection
- Path sanitization
- File storage

## Future Enhancements

- Twine editor integration for auto-detecting needed assets
- Batch capture mode for multiple images
- AI-powered asset suggestions based on scene content
- Preview before download
- Custom naming templates
