# API Behavior — How Extensions and Downloads Actually Work

Read this to understand:
1. Why `validate_queries.py` FORMAT MISMATCH warnings are advisory, not blocking
2. What the TOML extension actually controls (almost nothing) vs. what the source URL controls (everything)
3. How the renderer finds files even when extensions disagree

## The media-capture endpoint

`POST http://localhost:8000/api/v1/dev/media-capture`

Request body:

```json
{
  "url": "https://source.example.com/video.webm",
  "scene_id": "scenes/kiss",
  "game": "two_weeks"
}
```

Implementation: `api/v1/dev.py:451-589`.

### Extension detection order

From `dev.py:543-556`:

1. **`get_extension_from_url(url)`** — parses the URL path for a known extension
2. **Fallback**: `requests.head(url)` → read `Content-Type` header → `MIME_TO_EXT` lookup
3. **Last resort**: `"jpg"`

`MIME_TO_EXT` (from `dev.py:65-76`):

| Content-Type | Extension |
|--------------|-----------|
| image/jpeg | jpg |
| image/png | png |
| image/gif | gif |
| image/webp | webp |
| image/bmp | bmp |
| video/mp4 | mp4 |
| video/webm | webm |
| video/quicktime | mov |
| video/x-matroska | mkv |
| video/avi | avi |

Anything outside this map → fallback `.jpg`.

### The TOML extension is stripped, not honored

From `dev.py:116-123`, inside `parse_scene_path(scene_id)`:

```python
known_extensions = {'.mp4', '.webm', '.mov', '.mkv', '.avi', '.m4v',
                    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
scene_path = Path(scene_id)
if scene_path.suffix.lower() in known_extensions:
    scene_id = str(scene_path.with_suffix(''))
```

The scene_id you pass (including from TOML file paths) gets its extension stripped before the output path is built. The final saved filename is `{stem}.{detected_ext}` where `detected_ext` comes from the source URL, not your request.

### Overwrite-on-match (game workflow only)

From `dev.py:558-564`, when `game` is provided:

```python
for existing in output_dir.iterdir() if output_dir.exists() else []:
    if existing.is_file() and existing.stem == filename_base:
        existing.unlink()
```

Any existing file with the same stem is deleted before writing, regardless of extension. This means re-downloading a scene is safe across format changes:

```
before: scenes/kiss.jpg  (saved on first try, turned out static)
re-run with a video URL
→ API deletes scenes/kiss.jpg
→ saves scenes/kiss.webm
```

No orphan `_1` suffixed files. No manual cleanup between tries.

This behavior is **game-only**. Without a `game` parameter, files go to `DOWNLOADS_DIR` with unique-name collision handling (`_1`, `_2`, etc.).

## The renderer's extension-agnostic lookup

From `apps/game_generation/twee_comprehensive/generators/v1.py:8040-8079`:

```python
def _find_media_file(self, requested_path: str) -> tuple[str | None, str | None]:
    # 1. Exact match first (backward compat)
    if normalized in self.video_files:
        ext = Path(normalized).suffix.lower()
        return normalized, ext

    # 2. Extension-agnostic search
    base_path = str(Path(normalized).with_suffix(''))
    for file_path in self.video_files.keys():
        file_base = str(Path(file_path).with_suffix(''))
        if file_base == base_path:
            ext = Path(file_path).suffix.lower()
            return file_path, ext
```

Returns `(actual_path, actual_extension)`. The **actual extension drives rendering** — the generator decides `<video>` vs `<img>` from what's on disk, not what's in the TOML.

## End-to-end flow

```
TOML:    scenes/kiss.jpg
           │
           ▼
find-media picks source: https://source.com/clip.webm
           │
           ▼
POST /api/v1/dev/media-capture
           │
           ├─ parse_scene_path: strip .jpg   → stem = "kiss"
           ├─ detect extension from URL path → ".webm"
           ├─ overwrite any scenes/kiss.*    → deletes scenes/kiss.jpg
           └─ save scenes/kiss.webm
           │
           ▼
DISK:    scenes/kiss.webm (actual)
           │
           ▼
Generator _find_media_file("scenes/kiss.jpg")
           │
           ├─ base_path = "scenes/kiss"
           ├─ matches available key "scenes/kiss.webm"
           └─ returns ("scenes/kiss.webm", ".webm")
           │
           ▼
RENDERER: emits <video src="scenes/kiss.webm">
```

## Implications for find-media

1. **Download from the right kind of source** — this is what determines the saved extension. For a kiss scene, search video sources (GIFs, webm); the API will honor that. For a dinner scene, search image sources.

2. **TOML extension is advisory** — `validate_queries.py`'s FORMAT MISMATCH warnings are TOML-cleanup hints, not download-blockers. The API saves in the source's format regardless.

3. **Iteration is safe** — re-downloading a scene from a better source overwrites the previous file, even across extensions. No cleanup step needed.

4. **`tier_format_check.py` is the final gate** — it runs on the actual downloaded file. If the result is wrong (t5+ scene ended up as a .jpg because the source was a static thumbnail), this catches it regardless of what the TOML said.

5. **Beware the `.jpg` fallback** — if a URL has no extension AND no Content-Type, the API saves as `.jpg` by default. This is a trap for video sources that serve raw bytes without headers. Always prefer sources that send proper `Content-Type`, or URLs with explicit extensions in the path.

## Edge cases

**URL extension vs Content-Type disagreement** (URL says `.mp4` but server sends `application/octet-stream`):
- URL wins (detected first in the chain)
- File saved as `.mp4` regardless of actual content
- `tier_format_check.py` catches this via magic-byte check — it reads the first 16 bytes and verifies against expected magic for the extension

**Video platforms (YouTube, Vimeo, Twitter, TikTok, Instagram, Reddit, etc.)**:
- `is_video_platform()` returns true → routes to `yt-dlp` instead of direct download
- `yt-dlp` decides the final extension based on its format selection
- File lands with whatever `yt-dlp` chose — not necessarily what the URL path suggested

**Age-gate redirect to HTML** (common for adult sites without proper headers):
- `download_direct` detects `text/html` Content-Type and aborts
- Returns error: `"URL returned HTML instead of media"`
- NSFW pipeline must handle this — retry with Tor-routed URL, check referer header requirements

**Source URL returns an error page with 200 OK**:
- No fallback detection — file lands with whatever extension the URL/CT indicated
- Size check (`> 1KB` images, `> 50KB` videos) in `tier_format_check.py` catches tiny error-page bodies

## What this means practically

The API is tolerant and source-driven. Your job in find-media is to:
1. Pick URLs that serve the right kind of content for each scene
2. Let the API figure out the extension
3. Let the generator find it via extension-agnostic lookup
4. Let `tier_format_check.py` verify the final file is what you expected

You do NOT need to:
- Match TOML extensions to URLs
- Pre-fetch headers to determine extensions before calling the API
- Clean up old files between iterations
- Specify extensions in requests to the API (it ignores them)

This is why the skill's format-classification logic targets **the SOURCE you pick** during PLAN/RETRIEVE, not the TOML declaration. The TOML is a hint for humans; the source URL is the contract.
