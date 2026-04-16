# Product Requirements Document (PRD)

## Product Name
Twine Developer Media Capture Tool (Dev-only)

---

## 1. Purpose & Vision

The Twine Developer Media Capture Tool is an **internal development utility** designed to help the game developer quickly discover, select, and download media assets (images, GIFs, videos) from the web into a Twine game’s local asset folders.

This tool is **not player-facing** and will never ship with the game. It exists solely to remove manual friction in the asset acquisition workflow during development.

The guiding principle is:
> *Manual discovery, automated execution.*

The developer chooses media visually; the tool handles downloading, naming, and placement.

---

## 2. In-Scope vs Out-of-Scope

### In Scope
- Developer-only usage
- Manual browsing of web pages (Google, Reddit, etc.)
- Detecting media present on the current browser page
- Multi-selecting media items
- Downloading selected media into a configured local folder
- File naming and folder routing via metadata passed from Twine
- Integration with an existing local Django backend

### Out of Scope (Phase 1)
- Player-facing UI
- Automated ranking or AI selection of media
- Full Google search emulation
- Cross-device sync
- Copyright enforcement or licensing checks

---

## 3. Target User

- **Primary user:** Game developer (single-user)
- Technical proficiency: High
- Environment: Local development machine
- Browser: Chromium-based (Chrome)

---

## 4. High-Level Architecture

```
Twine HTML (dev mode)
   ↓
External Search Page (Google, etc.)
   ↓
Chrome Extension (Media Detection + Selection)
   ↓
Django Backend (Download + File System Write)
   ↓
Local Game Asset Folders
```

---

## 5. Core Workflow (Phase 1)

### Step 1: Twine Dev Link
- Twine passages contain dev-only links for missing media
- Clicking a link opens a new browser tab to a search page
- The URL contains embedded metadata for the extension

Example (conceptual):
- Scene ID
- Target folder
- File prefix
- Media type

---

### Step 2: Browser Navigation
- Developer manually browses search results
- No automation of search logic required
- Developer scrolls and evaluates media visually

---

### Step 3: Chrome Extension Detection

The Chrome extension:
- Runs on all pages
- Detects presence of a specific URL parameter (e.g. `nutdev=`)
- Parses and stores metadata locally
- Scans the current page for media elements:
  - `<img>`
  - `<video>`
  - GIF sources

---

### Step 4: Media Picker UI

Extension UI provides:
- Thumbnail grid of detected media
- Media type labels (image / gif / video)
- Multi-select (checkbox or click-to-select)
- Manual confirmation before download

---

### Step 5: Download Execution

- Extension sends selected media URLs + metadata to Django backend
- Backend downloads media files
- Files are written to the specified folder
- Files are renamed using provided prefix and numbering

---

## 6. URL Metadata Contract (Draft)

Metadata passed via URL parameters may include:

- `scene_id` (string)
- `target_folder` (relative path)
- `file_prefix` (string)
- `media_type` (image | gif | video)

This metadata is advisory and may be overridden by backend rules.

---

## 7. Backend Responsibilities (Django)

- Accept download requests from extension
- Validate URLs
- Download files safely
- Deduplicate files (hash-based or filename-based)
- Write files to local asset directories
- Return success / failure response

---

## 8. Non-Functional Requirements

- Must work fully offline after download
- No cloud dependencies
- Minimal latency acceptable
- Failures should be visible and debuggable

---

## 9. Security & Safety

- Tool is developer-only
- No sandbox escape attempts
- No persistent scraping or crawling
- No credential handling

---

## 10. Success Criteria

- Developer can go from missing media → downloaded asset in under 1 minute
- No manual file renaming required
- No copy-paste of URLs required
- No player exposure

---

## 11. Future Enhancements (Not Phase 1)

- Twine-side missing asset detection
- Asset manifest auto-update
- Scene-to-asset mapping
- Basic media quality filtering
- AI-assisted suggestions

---

## 12. Open Questions

- Final URL parameter format
- Deduplication strategy
- Default folder mappings
- Extension UI placement (popup vs sidebar)

---

**Status:** Draft PRD – Phase 1

