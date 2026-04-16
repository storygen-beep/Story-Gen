"""
Media Finder — dev tool for searching and downloading media for games.

Uses DuckDuckGo image search to find SFW media matching TOML search queries.
Downloads to staging folder (games/{game}/media_finder/) for review before use.

No authentication, no database. Pure filesystem + web search.
"""

import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from api.v1.dev import (
    download_direct,
    get_extension_from_content_type,
    get_extension_from_url,
)

GAMES_ROOT = Path(settings.BASE_DIR) / "games"

# In-memory search cache: (game, file_path) -> {results, timestamp}
_SEARCH_CACHE = {}
CACHE_TTL = 600  # 10 minutes

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v"}


def _staging_dir(game: str, file_path: str) -> Path:
    """Get staging directory for a media item."""
    p = Path(file_path)
    stem = p.stem
    parent = str(p.parent).replace("/", "--").replace("\\", "--")
    folder_name = f"{parent}--{stem}" if parent and parent != "." else stem
    return GAMES_ROOT / game / "media_finder" / folder_name


def _safe_path(base: Path, target: Path) -> bool:
    """Check that target is under base (no traversal)."""
    try:
        base.resolve()
        target.resolve().relative_to(base.resolve())
        return True
    except (ValueError, RuntimeError):
        return False


def _parse_body(request):
    """Parse JSON body from request."""
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


# =============================================================================
# Views
# =============================================================================


@require_GET
def page(request):
    """Serve the Media Finder HTML page."""
    game = request.GET.get("game", "")
    file_path = request.GET.get("file", "")
    desc = request.GET.get("desc", "")
    media_type = request.GET.get("type", "")
    canvas = request.GET.get("canvas", "")
    queries_raw = request.GET.get("queries", "[]")
    try:
        queries_safe = json.dumps(json.loads(queries_raw))
    except (json.JSONDecodeError, ValueError):
        queries_safe = "[]"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Media Finder — {_esc(file_path or 'Search')}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0d0d0d; color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }}
a {{ color: #60a5fa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* Header */
.header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #2a2a2a; }}
.back-link {{ font-size: 13px; color: #888; flex-shrink: 0; }}
.back-link:hover {{ color: #fff; }}
.header-title {{ font-size: 20px; font-weight: 700; color: #fff; }}

/* Item info */
.item-info {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px; }}
.item-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }}
.item-row:last-child {{ margin-bottom: 0; }}
.item-label {{ font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; min-width: 60px; }}
.item-value {{ font-size: 13px; color: #ccc; }}
.item-value.mono {{ font-family: monospace; color: #8af; }}
.type-badge {{ font-size: 9px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
.type-badge.image {{ background: #3b82f622; color: #60a5fa; }}
.type-badge.video {{ background: #a855f722; color: #c084fc; }}

/* Search controls */
.search-section {{ margin-bottom: 24px; }}
.search-label {{ font-size: 12px; color: #888; margin-bottom: 8px; }}
.query-chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
.query-chip {{ font-size: 12px; color: #e0e0e0; background: #2a2a2a; border: 1px solid #3a3a3a; padding: 6px 14px; border-radius: 20px; cursor: pointer; transition: all 0.15s; }}
.query-chip:hover {{ background: #3a3a3a; border-color: #4a4a4a; }}
.query-chip.active {{ background: #3b82f633; border-color: #3b82f6; color: #60a5fa; }}
.search-actions {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
.btn {{ font-size: 12px; font-weight: 600; padding: 8px 18px; border-radius: 8px; border: none; cursor: pointer; transition: all 0.15s; }}
.btn-primary {{ background: #3b82f6; color: #fff; }}
.btn-primary:hover {{ background: #2563eb; }}
.btn-primary:disabled {{ background: #333; color: #666; cursor: not-allowed; }}
.btn-green {{ background: #22c55e; color: #fff; }}
.btn-green:hover {{ background: #16a34a; }}
.btn-red {{ background: #ef4444; color: #fff; }}
.btn-red:hover {{ background: #dc2626; }}
.btn-sm {{ font-size: 10px; padding: 4px 10px; border-radius: 6px; }}
.btn-outline {{ background: transparent; border: 1px solid #3a3a3a; color: #aaa; }}
.btn-outline:hover {{ border-color: #60a5fa; color: #60a5fa; }}
.custom-search {{ display: flex; gap: 8px; margin-top: 8px; }}
.custom-search input {{ flex: 1; background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 8px 14px; color: #e0e0e0; font-size: 12px; outline: none; }}
.custom-search input:focus {{ border-color: #3b82f6; }}

/* Loading */
.loading {{ text-align: center; padding: 40px; color: #666; }}
.spinner {{ display: inline-block; width: 20px; height: 20px; border: 2px solid #333; border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}

/* Results */
.results-header {{ font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #2a2a2a; display: flex; align-items: center; gap: 8px; }}
.results-count {{ font-size: 11px; color: #888; font-weight: 400; }}
.query-group {{ margin-bottom: 24px; }}
.query-group-label {{ font-size: 12px; color: #60a5fa; margin-bottom: 10px; font-style: italic; }}
.thumb-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }}
.thumb-card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; overflow: hidden; transition: all 0.15s; }}
.thumb-card:hover {{ border-color: #3b82f6; transform: translateY(-2px); }}
.thumb-img-wrap {{ position: relative; width: 100%; padding-top: 75%; overflow: hidden; background: #111; cursor: pointer; }}
.thumb-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }}
.thumb-img-wrap img.loading-img {{ opacity: 0.3; }}
.thumb-meta {{ padding: 8px 10px; }}
.thumb-dims {{ font-size: 10px; color: #666; }}
.thumb-source {{ font-size: 10px; color: #555; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.thumb-actions {{ display: flex; gap: 4px; margin-top: 6px; }}
.thumb-status {{ font-size: 10px; padding: 4px 8px; border-radius: 4px; margin-top: 4px; }}
.thumb-status.success {{ background: #22c55e22; color: #4ade80; }}
.thumb-status.error {{ background: #ef444422; color: #f87171; }}

/* Preview modal */
.preview-overlay {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.85); z-index: 1000; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
.preview-overlay img {{ max-width: 90vw; max-height: 90vh; border-radius: 8px; box-shadow: 0 0 40px rgba(0,0,0,0.5); }}

/* Staging */
.staging-section {{ margin-top: 32px; padding-top: 20px; border-top: 2px solid #2a2a2a; }}
.staging-header {{ font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
.staging-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }}
.staged-card {{ background: #1a2a1a; border: 1px solid #22c55e44; border-radius: 8px; overflow: hidden; }}
.staged-img-wrap {{ position: relative; width: 100%; padding-top: 75%; overflow: hidden; background: #111; cursor: pointer; }}
.staged-img-wrap img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }}
.staged-meta {{ padding: 8px 10px; }}
.staged-name {{ font-size: 11px; color: #ccc; font-family: monospace; word-break: break-all; }}
.staged-size {{ font-size: 10px; color: #666; margin-top: 2px; }}
.staged-actions {{ display: flex; gap: 4px; margin-top: 6px; }}

/* Toast notifications */
.toast {{ position: fixed; bottom: 20px; right: 20px; padding: 12px 20px; border-radius: 8px; font-size: 12px; z-index: 2000; animation: slideIn 0.3s ease; }}
.toast.success {{ background: #22c55e; color: #fff; }}
.toast.error {{ background: #ef4444; color: #fff; }}
@keyframes slideIn {{ from {{ transform: translateX(100px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}

/* Empty state */
.empty-state {{ text-align: center; padding: 60px 20px; color: #555; }}
.empty-state h3 {{ color: #888; margin-bottom: 8px; }}
</style>
</head>
<body>

<div class="header">
    <a class="back-link" href="/api/v1/dev/game-review/?game={_esc(game)}&view=media">&#8592; Game Review</a>
    <span class="header-title">Media Finder</span>
</div>

<div class="item-info" id="itemInfo">
    <div class="item-row">
        <span class="item-label">File</span>
        <span class="item-value mono" id="infoFile"></span>
        <span class="type-badge" id="infoType"></span>
    </div>
    <div class="item-row">
        <span class="item-label">Canvas</span>
        <span class="item-value" id="infoCanvas"></span>
    </div>
    <div class="item-row">
        <span class="item-label">Desc</span>
        <span class="item-value" id="infoDesc" style="font-style:italic; color:#999;"></span>
    </div>
</div>

<div class="search-section">
    <div class="search-label">Search Queries</div>
    <div class="query-chips" id="queryChips"></div>
    <div class="search-actions">
        <button class="btn btn-primary" id="searchAllBtn" onclick="searchAll()">Search All</button>
        <button class="btn btn-outline" id="clearCacheBtn" onclick="clearCacheAndSearch()">Clear Cache &amp; Re-search</button>
    </div>
    <div class="custom-search">
        <input type="text" id="customQuery" placeholder="Custom search query..." onkeydown="if(event.key==='Enter')searchCustom()">
        <button class="btn btn-primary btn-sm" onclick="searchCustom()">Search</button>
    </div>
</div>

<div id="resultsArea"></div>
<div id="stagingArea"></div>

<script>
const API_BASE = '/api/v1/dev/media-finder';
const PARAMS = {{
    game: {json.dumps(game)},
    file: {json.dumps(file_path)},
    desc: {json.dumps(desc)},
    type: {json.dumps(media_type)},
    canvas: {json.dumps(canvas)},
    queries: {queries_safe}
}};

let SEARCH_RESULTS = [];
let IS_SEARCHING = false;

function esc(s) {{
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}}

function init() {{
    // Populate item info
    document.getElementById('infoFile').textContent = PARAMS.file || '(none)';
    const typeBadge = document.getElementById('infoType');
    typeBadge.textContent = PARAMS.type || 'unknown';
    typeBadge.className = 'type-badge ' + (PARAMS.type || '');
    document.getElementById('infoCanvas').textContent = PARAMS.canvas || '(none)';
    document.getElementById('infoDesc').textContent = PARAMS.desc || '(no description)';

    // Render query chips
    const chips = document.getElementById('queryChips');
    const queries = PARAMS.queries || [];
    queries.forEach((q, i) => {{
        const chip = document.createElement('span');
        chip.className = 'query-chip';
        chip.textContent = q;
        chip.onclick = () => searchSingle(q);
        chips.appendChild(chip);
    }});

    // Auto-search if we have queries
    if (queries.length > 0 && PARAMS.game && PARAMS.file) {{
        searchAll();
    }}

    // Load staging
    loadStaging();
}}

async function searchAll() {{
    const queries = PARAMS.queries || [];
    if (queries.length === 0) return;
    await doSearch(queries, false);
}}

async function clearCacheAndSearch() {{
    const queries = PARAMS.queries || [];
    if (queries.length === 0) return;
    await doSearch(queries, true);
}}

async function searchSingle(query) {{
    await doSearch([query], false);
}}

async function searchCustom() {{
    const input = document.getElementById('customQuery');
    const q = input.value.trim();
    if (!q) return;
    await doSearch([q], false);
}}

async function doSearch(queries, clearCache) {{
    if (IS_SEARCHING) return;
    IS_SEARCHING = true;

    const area = document.getElementById('resultsArea');
    area.innerHTML = '<div class="loading"><span class="spinner"></span> Searching ' + queries.length + ' quer' + (queries.length === 1 ? 'y' : 'ies') + '...</div>';

    document.getElementById('searchAllBtn').disabled = true;

    try {{
        const body = {{
            game: PARAMS.game,
            file_path: PARAMS.file,
            queries: queries,
            max_per_query: 10,
        }};
        if (clearCache) body.clear_cache = true;

        const resp = await fetch(API_BASE + '/search', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(body),
        }});

        const data = await resp.json();
        if (!resp.ok) {{
            area.innerHTML = '<div class="empty-state"><h3>Search Error</h3><p>' + esc(data.error || 'Unknown error') + '</p></div>';
            return;
        }}

        SEARCH_RESULTS = data.results || [];
        renderResults(data);
    }} catch (err) {{
        area.innerHTML = '<div class="empty-state"><h3>Search Failed</h3><p>' + esc(err.message) + '</p></div>';
    }} finally {{
        IS_SEARCHING = false;
        document.getElementById('searchAllBtn').disabled = false;
    }}
}}

function renderResults(data) {{
    const area = document.getElementById('resultsArea');
    const results = data.results || [];

    if (results.length === 0) {{
        let errHtml = '<div class="empty-state"><h3>No Results</h3><p>Try different search terms</p>';
        if (data.errors && data.errors.length > 0) {{
            errHtml += '<p style="color:#f87171;margin-top:8px;">' + data.errors.map(e => esc(e)).join('<br>') + '</p>';
        }}
        errHtml += '</div>';
        area.innerHTML = errHtml;
        return;
    }}

    // Store results globally for data-index lookups
    window._searchResults = results;

    // Group by source_query, tracking global index
    const groups = {{}};
    results.forEach((r, globalIdx) => {{
        const q = r.source_query || 'Results';
        if (!groups[q]) groups[q] = [];
        r._globalIdx = globalIdx;
        groups[q].push(r);
    }});

    let html = '<div class="results-header">Results <span class="results-count">' + results.length + ' found' + (data.cached ? ' (cached)' : '') + '</span></div>';

    Object.keys(groups).forEach(query => {{
        const items = groups[query];
        html += '<div class="query-group">';
        html += '<div class="query-group-label">"' + esc(query) + '" (' + items.length + ')</div>';
        html += '<div class="thumb-grid">';

        items.forEach(r => {{
            const gi = r._globalIdx;
            const thumbUrl = r.thumbnail || r.image || '';
            const w = r.width || '?';
            const h = r.height || '?';
            const source = r.source || '';
            let domain = '';
            try {{ domain = new URL(source || r.image || '').hostname.replace('www.', ''); }} catch(e) {{}}

            html += '<div class="thumb-card" id="tc_' + gi + '">';
            html += '<div class="thumb-img-wrap" data-idx="' + gi + '" data-action="preview">';
            html += '<img src="' + esc(thumbUrl) + '" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display=&quot;none&quot;">';
            html += '</div>';
            html += '<div class="thumb-meta">';
            html += '<div class="thumb-dims">' + w + ' x ' + h + '</div>';
            html += '<div class="thumb-source">' + esc(domain) + '</div>';
            html += '<div class="thumb-actions">';
            html += '<button class="btn btn-green btn-sm" data-idx="' + gi + '" data-action="stage">Stage</button>';
            html += '<button class="btn btn-primary btn-sm" data-idx="' + gi + '" data-action="use">Use</button>';
            html += '</div>';
            html += '<div id="tc_' + gi + '_status"></div>';
            html += '</div>';
            html += '</div>';
        }});

        html += '</div></div>';
    }});

    area.innerHTML = html;

    // Event delegation — single listener for all clicks
    area.addEventListener('click', function(e) {{
        const el = e.target.closest('[data-action]');
        if (!el) return;
        const idx = parseInt(el.dataset.idx);
        const r = window._searchResults[idx];
        if (!r) return;
        const action = el.dataset.action;
        if (action === 'preview') {{
            previewImage(r.image);
        }} else if (action === 'stage') {{
            downloadMedia(r.image, 'staging', 'tc_' + idx);
        }} else if (action === 'use') {{
            downloadMedia(r.image, 'output', 'tc_' + idx);
        }}
    }});
}}

function previewImage(url) {{
    const overlay = document.createElement('div');
    overlay.className = 'preview-overlay';
    overlay.onclick = () => overlay.remove();
    const img = document.createElement('img');
    img.src = url;
    overlay.appendChild(img);
    document.body.appendChild(overlay);
}}

async function downloadMedia(url, destination, cardId) {{
    const statusEl = document.getElementById(cardId + '_status');
    if (statusEl) statusEl.innerHTML = '<div class="thumb-status" style="color:#facc15;">Downloading...</div>';

    try {{
        const resp = await fetch(API_BASE + '/download', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                game: PARAMS.game,
                file_path: PARAMS.file,
                url: url,
                destination: destination,
            }}),
        }});

        const data = await resp.json();
        if (data.success) {{
            const label = destination === 'staging' ? 'Staged!' : 'Saved to output!';
            if (statusEl) statusEl.innerHTML = '<div class="thumb-status success">' + label + '</div>';
            showToast(label, 'success');
            if (destination === 'staging') loadStaging();
        }} else {{
            if (statusEl) statusEl.innerHTML = '<div class="thumb-status error">' + esc(data.error) + '</div>';
            showToast('Download failed: ' + (data.error || 'unknown'), 'error');
        }}
    }} catch (err) {{
        if (statusEl) statusEl.innerHTML = '<div class="thumb-status error">' + esc(err.message) + '</div>';
        showToast('Download error: ' + err.message, 'error');
    }}
}}

async function loadStaging() {{
    if (!PARAMS.game || !PARAMS.file) return;
    const area = document.getElementById('stagingArea');

    try {{
        const resp = await fetch(API_BASE + '/staging?game=' + encodeURIComponent(PARAMS.game) + '&file_path=' + encodeURIComponent(PARAMS.file));
        const data = await resp.json();
        const files = data.files || [];

        if (files.length === 0) {{
            area.innerHTML = '<div class="staging-section"><div class="staging-header">Staged Candidates <span class="results-count">(none yet)</span></div></div>';
            return;
        }}

        let html = '<div class="staging-section">';
        html += '<div class="staging-header">Staged Candidates <span class="results-count">(' + files.length + ')</span></div>';
        html += '<div class="staging-grid">';

        files.forEach(f => {{
            html += '<div class="staged-card">';
            html += '<div class="staged-img-wrap" onclick="previewImage(\\'' + esc(f.serve_url).replace(/'/g, "\\\\'") + '\\')">';
            html += '<img src="' + esc(f.serve_url) + '" loading="lazy">';
            html += '</div>';
            html += '<div class="staged-meta">';
            html += '<div class="staged-name">' + esc(f.name) + '</div>';
            html += '<div class="staged-size">' + formatBytes(f.size) + '</div>';
            html += '<div class="staged-actions">';
            html += '<button class="btn btn-green btn-sm" onclick="promoteStaged(\\'' + esc(f.name).replace(/'/g, "\\\\'") + '\\')">Use</button>';
            html += '<button class="btn btn-red btn-sm" onclick="deleteStaged(\\'' + esc(f.name).replace(/'/g, "\\\\'") + '\\')">Delete</button>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
        }});

        html += '</div></div>';
        area.innerHTML = html;
    }} catch (err) {{
        area.innerHTML = '<div class="staging-section"><div class="staging-header">Staged Candidates</div><p style="color:#666;">Failed to load staging</p></div>';
    }}
}}

async function promoteStaged(filename) {{
    try {{
        const resp = await fetch(API_BASE + '/promote', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                game: PARAMS.game,
                file_path: PARAMS.file,
                staged_file: filename,
            }}),
        }});
        const data = await resp.json();
        if (data.success) {{
            showToast('Promoted to output!', 'success');
            loadStaging();
        }} else {{
            showToast('Promote failed: ' + (data.error || 'unknown'), 'error');
        }}
    }} catch (err) {{
        showToast('Error: ' + err.message, 'error');
    }}
}}

async function deleteStaged(filename) {{
    try {{
        const resp = await fetch(API_BASE + '/delete-staged', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                game: PARAMS.game,
                file_path: PARAMS.file,
                staged_file: filename,
            }}),
        }});
        const data = await resp.json();
        if (data.success) {{
            showToast('Deleted', 'success');
            loadStaging();
        }} else {{
            showToast('Delete failed: ' + (data.error || 'unknown'), 'error');
        }}
    }} catch (err) {{
        showToast('Error: ' + err.message, 'error');
    }}
}}

function formatBytes(bytes) {{
    if (!bytes || bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}}

function showToast(msg, type) {{
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}}

// Init on load
init();
</script>
</body>
</html>"""
    response = HttpResponse(html)
    response["Cache-Control"] = "no-store"
    return response


def _esc(s):
    """Escape HTML entities for Python-side template injection."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


@csrf_exempt
def search(request):
    """Run DuckDuckGo image searches for media queries."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_path = body.get("file_path", "")
    queries = body.get("queries", [])
    max_per_query = min(body.get("max_per_query", 10), 25)
    clear_cache = body.get("clear_cache", False)

    if not queries:
        return JsonResponse({"error": "No queries provided"}, status=400)

    # Check cache
    cache_key = (game, file_path, tuple(queries))
    if not clear_cache:
        cached = _SEARCH_CACHE.get(cache_key)
        if cached and time.time() - cached["timestamp"] < CACHE_TTL:
            return JsonResponse({"results": cached["results"], "cached": True})

    def do_search(query):
        """Search DuckDuckGo for images matching query."""
        try:
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                return query, list(
                    ddgs.images(
                        keywords=query,
                        max_results=max_per_query,
                        safesearch="on",
                    )
                )
        except Exception as e:
            return query, [{"_error": str(e)}]

    # Run searches in parallel
    all_results = []
    seen_urls = set()
    errors = []

    with ThreadPoolExecutor(max_workers=min(len(queries), 5)) as executor:
        futures = [executor.submit(do_search, q) for q in queries]
        for future in as_completed(futures):
            try:
                query, results = future.result()
                for r in results:
                    if "_error" in r:
                        errors.append(f"Query '{query}': {r['_error']}")
                        continue
                    img_url = r.get("image", "")
                    if img_url and img_url not in seen_urls:
                        seen_urls.add(img_url)
                        all_results.append(
                            {
                                "image": img_url,
                                "thumbnail": r.get("thumbnail", img_url),
                                "title": r.get("title", ""),
                                "width": r.get("width"),
                                "height": r.get("height"),
                                "source": r.get("url", ""),
                                "source_query": query,
                            }
                        )
            except Exception as e:
                errors.append(str(e))

    # Only cache if we got results (don't cache rate limit failures)
    if all_results:
        _SEARCH_CACHE[cache_key] = {"results": all_results, "timestamp": time.time()}

    resp = {"results": all_results, "cached": False}
    if errors:
        resp["errors"] = errors
    return JsonResponse(resp)


@csrf_exempt
def download(request):
    """Download a media file to staging or output."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_path = body.get("file_path", "")
    url = body.get("url", "")
    destination = body.get("destination", "staging")  # "staging" or "output"

    if not game or not file_path or not url:
        return JsonResponse(
            {"error": "game, file_path, and url are required"}, status=400
        )

    game_dir = GAMES_ROOT / game
    if not game_dir.is_dir():
        return JsonResponse({"error": f"Game '{game}' not found"}, status=404)

    # Determine file extension from URL
    ext = get_extension_from_url(url)
    if not ext:
        # Try HEAD request to get content type
        try:
            head = requests.head(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                },
                allow_redirects=True,
            )
            ct = head.headers.get("Content-Type", "")
            ext = get_extension_from_content_type(ct)
        except Exception:
            pass
    if not ext:
        ext = "jpg"  # fallback

    if destination == "output":
        # Save directly to output with the original file path
        # Use the original extension from file_path if we got a compatible type
        orig_ext = Path(file_path).suffix.lstrip(".")
        if orig_ext:
            # Keep original extension from TOML
            out_path = game_dir / "output" / file_path
        else:
            out_path = game_dir / "output" / f"{file_path}.{ext}"

        if not _safe_path(GAMES_ROOT, out_path):
            return JsonResponse({"error": "Invalid path"}, status=400)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        success, error = download_direct(url, out_path)

        if success:
            return JsonResponse(
                {
                    "success": True,
                    "file_path": str(out_path.relative_to(GAMES_ROOT)),
                    "destination": "output",
                }
            )
        return JsonResponse({"success": False, "error": error})

    else:
        # Save to staging
        staging = _staging_dir(game, file_path)
        staging.mkdir(parents=True, exist_ok=True)

        if not _safe_path(GAMES_ROOT, staging):
            return JsonResponse({"error": "Invalid path"}, status=400)

        # Find next candidate number
        existing = list(staging.glob("candidate_*"))
        next_num = len(existing) + 1
        out_path = staging / f"candidate_{next_num}.{ext}"

        success, error = download_direct(url, out_path)

        if success:
            return JsonResponse(
                {
                    "success": True,
                    "file_path": str(out_path.relative_to(GAMES_ROOT)),
                    "destination": "staging",
                    "filename": out_path.name,
                }
            )
        return JsonResponse({"success": False, "error": error})


@require_GET
def staging_list(request):
    """List staged candidate files for a media item."""
    game = request.GET.get("game", "")
    file_path = request.GET.get("file_path", "")

    if not game or not file_path:
        return JsonResponse({"files": []})

    staging = _staging_dir(game, file_path)
    if not staging.is_dir():
        return JsonResponse({"files": []})

    files = []
    for f in sorted(staging.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            files.append(
                {
                    "name": f.name,
                    "size": f.stat().st_size,
                    "serve_url": f"/api/v1/dev/media-finder/serve-staged?game={game}&file_path={file_path}&name={f.name}",
                }
            )

    return JsonResponse({"files": files})


@require_GET
def serve_staged(request):
    """Serve a staged file for preview."""
    game = request.GET.get("game", "")
    file_path = request.GET.get("file_path", "")
    name = request.GET.get("name", "")

    if not game or not file_path or not name:
        return HttpResponse("Missing params", status=400)

    staging = _staging_dir(game, file_path)
    fpath = staging / name

    if not _safe_path(GAMES_ROOT, fpath) or not fpath.is_file():
        return HttpResponse("Not found", status=404)

    # Determine content type
    ext = fpath.suffix.lower()
    ct_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
        ".mp4": "video/mp4",
        ".webm": "video/webm",
    }
    content_type = ct_map.get(ext, "application/octet-stream")

    with open(fpath, "rb") as f:
        return HttpResponse(f.read(), content_type=content_type)


@csrf_exempt
def promote(request):
    """Promote a staged file to the output directory."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_path = body.get("file_path", "")
    staged_file = body.get("staged_file", "")

    if not game or not file_path or not staged_file:
        return JsonResponse(
            {"error": "game, file_path, and staged_file required"}, status=400
        )

    staging = _staging_dir(game, file_path)
    src = staging / staged_file

    if not _safe_path(GAMES_ROOT, src) or not src.is_file():
        return JsonResponse({"error": "Staged file not found"}, status=404)

    # Determine output path — use original file_path but with the staged file's extension
    orig_path = Path(file_path)
    staged_ext = src.suffix  # e.g., .jpg, .png
    out_name = orig_path.stem + staged_ext
    out_path = GAMES_ROOT / game / "output" / orig_path.parent / out_name

    if not _safe_path(GAMES_ROOT, out_path):
        return JsonResponse({"error": "Invalid output path"}, status=400)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out_path)

    return JsonResponse(
        {
            "success": True,
            "file_path": str(out_path.relative_to(GAMES_ROOT)),
        }
    )


@csrf_exempt
def delete_staged(request):
    """Delete a staged candidate file."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_path = body.get("file_path", "")
    staged_file = body.get("staged_file", "")

    if not game or not file_path or not staged_file:
        return JsonResponse(
            {"error": "game, file_path, and staged_file required"}, status=400
        )

    staging = _staging_dir(game, file_path)
    target = staging / staged_file

    if not _safe_path(GAMES_ROOT, target):
        return JsonResponse({"error": "Invalid path"}, status=400)

    if target.is_file():
        target.unlink()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "File not found"}, status=404)


# =============================================================================
# URL patterns
# =============================================================================
urlpatterns = [
    path("", page, name="media_finder_page"),
    path("search", search, name="media_finder_search"),
    path("download", download, name="media_finder_download"),
    path("staging", staging_list, name="media_finder_staging"),
    path("serve-staged", serve_staged, name="media_finder_serve_staged"),
    path("promote", promote, name="media_finder_promote"),
    path("delete-staged", delete_staged, name="media_finder_delete_staged"),
]
