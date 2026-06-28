"""
Media Finder — dev backend for the find.html "options" workflow.

The user searches Google in a real browser tab and uses the capture extension to
collect candidate media URLs as per-slot OPTIONS (stored, NOT downloaded). This
module stores those option URLs in a per-game JSON ledger, streams previews through
a proxy (hotlink-safe, Tor-ready), and on the final pick downloads the chosen URL
into the game's videos/ source-of-truth — replacing the slot's media.

No auth, no DB — filesystem + JSON ledger. Local dev tool; relies on open CORS.

Endpoints (under /api/v1/dev/media-finder/):
- POST options/add     {game, file, url, type, media_kind}  -> append an option
- GET  options/list    ?game=&file=                          -> options for a slot
- POST options/remove  {game, file, url}                     -> drop an option
- POST grab            {game, file, url, source}             -> download -> videos/
- GET  proxy           ?url=&source=                         -> stream a remote URL
"""

import ipaddress
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from api.v1.dev import (
    download_direct,
    get_extension_from_content_type,
    get_extension_from_url,
    parse_scene_path,
)

GAMES_ROOT = Path(settings.BASE_DIR) / "games"

# A real browser UA — used for proxy/grab fetches.
_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Short-lived RedGIFs temp token — an option URL may be a redgifs mp4 whose CDN
# wants the bearer; proxy/grab attach it when source == "redgifs".
_REDGIFS_TOKEN = {"token": "", "ts": 0.0}
_REDGIFS_TTL = 3000  # ~50 min


# =============================================================================
# Helpers
# =============================================================================


def _safe_path(base: Path, target: Path) -> bool:
    """Check that target is under base (no traversal)."""
    try:
        base.resolve()
        target.resolve().relative_to(base.resolve())
        return True
    except (ValueError, RuntimeError):
        return False


def _safe_game_dir(game: str) -> Path | None:
    """Resolve games/<game>, guarding against path traversal. None if invalid."""
    if not game:
        return None
    game_dir = GAMES_ROOT / game
    try:
        if not game_dir.resolve().is_relative_to(GAMES_ROOT.resolve()):
            return None
    except Exception:
        return None
    return game_dir


def _parse_body(request):
    """Parse JSON body from request."""
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _redgifs_token(force=False):
    """Fetch/cache a RedGIFs temporary bearer token (clearnet, no account)."""
    now = time.time()
    if not force and _REDGIFS_TOKEN["token"] and now - _REDGIFS_TOKEN["ts"] < _REDGIFS_TTL:
        return _REDGIFS_TOKEN["token"]
    resp = requests.get(
        "https://api.redgifs.com/v2/auth/temporary",
        headers={"User-Agent": _BROWSER_UA},
        timeout=15,
    )
    resp.raise_for_status()
    token = resp.json().get("token", "")
    _REDGIFS_TOKEN.update(token=token, ts=now)
    return token


# =============================================================================
# Options store — per-game JSON ledger of candidate URLs, keyed by slot file.
# Shape: {game, updated_at, options: {<file>: [{url, type, media_kind, added_at}]}}
# Same atomic read/write + path-guard discipline as api/v1/media_review.py.
# =============================================================================


def _options_path(game_dir: Path) -> Path:
    return game_dir / ".find-media" / "media_options.json"


def _read_options(game_dir: Path) -> dict:
    path_ = _options_path(game_dir)
    if not path_.exists():
        return {"game": game_dir.name, "options": {}}
    try:
        with path_.open(encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"game": game_dir.name, "options": {}}
    data.setdefault("options", {})
    return data


def _write_options(game_dir: Path, data: dict) -> None:
    """Atomically replace the ledger (tmp + os.replace) so a crash can't truncate it."""
    path_ = _options_path(game_dir)
    path_.parent.mkdir(parents=True, exist_ok=True)
    tmp = path_.with_name(path_.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path_)


@csrf_exempt
def options_add(request):
    """POST options/add {game, file, url, type, media_kind} — store a candidate URL
    (no download). `type` is the user's label (image/gif/video); `media_kind`
    (img/video) drives how the option previews. Deduped by url."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_ = body.get("file", "")
    url = body.get("url", "")
    type_ = (body.get("type") or "image").lower()
    media_kind = (body.get("media_kind") or "img").lower()

    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    if not file_ or not url:
        return JsonResponse({"error": "file and url are required"}, status=400)
    if urlparse(url).scheme not in ("http", "https"):
        return JsonResponse({"error": "Invalid URL scheme"}, status=400)

    now = datetime.now(timezone.utc).isoformat()
    data = _read_options(game_dir)
    lst = data["options"].setdefault(file_, [])
    if any(o.get("url") == url for o in lst):
        return JsonResponse({"ok": True, "duplicate": True, "count": len(lst)})
    lst.append({"url": url, "type": type_, "media_kind": media_kind, "added_at": now})
    data["game"] = game
    data["updated_at"] = now
    _write_options(game_dir, data)
    return JsonResponse({"ok": True, "count": len(lst)})


@require_GET
def options_list(request):
    """GET options/list?game=&file= — the collected option URLs for one slot."""
    game = request.GET.get("game", "")
    file_ = request.GET.get("file", "")
    game_dir = _safe_game_dir(game)
    if game_dir is None:
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    data = _read_options(game_dir)
    return JsonResponse({"options": data["options"].get(file_, [])})


@csrf_exempt
def options_remove(request):
    """POST options/remove {game, file, url} — drop one option."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_ = body.get("file", "")
    url = body.get("url", "")
    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": "Invalid or missing game"}, status=400)

    data = _read_options(game_dir)
    kept = [o for o in data["options"].get(file_, []) if o.get("url") != url]
    data["options"][file_] = kept
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _write_options(game_dir, data)
    return JsonResponse({"ok": True, "count": len(kept)})


# =============================================================================
# Grab — download a chosen option into the game's SOURCE-OF-TRUTH videos/ folder.
# =============================================================================


@csrf_exempt
def grab(request):
    """Download a chosen option straight into games/<game>/videos/<subfolder>/<stem>.<ext>.

    Body: {game, file, url, source}. The target path is derived from the slot's
    declared `file` (extension re-derived from the source URL) — same rule as
    /api/v1/dev/media-capture, so the file survives the next package_from_toml.
    (Never output/, which is wiped on rebuild.) For RedGIFs, attaches the bearer.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    file_ = body.get("file", "")
    url = body.get("url", "")
    source = body.get("source", "")

    if not game or not file_ or not url:
        return JsonResponse({"error": "game, file, and url are required"}, status=400)
    if urlparse(url).scheme not in ("http", "https"):
        return JsonResponse({"error": "Invalid URL scheme"}, status=400)

    game_dir = GAMES_ROOT / game
    if not game_dir.is_dir():
        return JsonResponse({"error": f"Game '{game}' not found"}, status=404)

    # file -> (subfolder, stem); collapse a leading videos/ so we never double it.
    subfolder, filename_base = parse_scene_path(file_)
    if subfolder.startswith("videos/"):
        subfolder = subfolder[len("videos/"):]
    elif subfolder == "videos":
        subfolder = ""
    output_dir = (game_dir / "videos" / subfolder) if subfolder else (game_dir / "videos")
    if not _safe_path(GAMES_ROOT, output_dir):
        return JsonResponse({"error": "Invalid path"}, status=400)

    # RedGIFs media needs the bearer token; others are open.
    extra_headers = None
    if source == "redgifs":
        token = _redgifs_token()
        if token:
            extra_headers = {"Authorization": f"Bearer {token}"}

    # Extension from the SOURCE url / content-type (not the TOML ext); the renderer
    # matches extension-agnostically, so an mp4 in a .webm slot still plays.
    ext = get_extension_from_url(url)
    if not ext:
        try:
            head = requests.head(
                url,
                timeout=10,
                headers={"User-Agent": _BROWSER_UA, **(extra_headers or {})},
                allow_redirects=True,
            )
            ext = get_extension_from_content_type(head.headers.get("Content-Type", ""))
        except Exception:
            pass
    if not ext:
        ext = "jpg"

    output_dir.mkdir(parents=True, exist_ok=True)
    # Overwrite any existing same-stem file (any extension) so the generator never
    # sees an orphan it can't match — mirrors media_capture's game workflow.
    for existing in output_dir.iterdir():
        if existing.is_file() and existing.stem == filename_base:
            existing.unlink()
    output_path = output_dir / f"{filename_base}.{ext}"

    success, error = download_direct(url, output_path, extra_headers=extra_headers)
    if success:
        return JsonResponse(
            {"success": True, "file_path": str(output_path.relative_to(GAMES_ROOT))}
        )
    return JsonResponse({"success": False, "error": error}, status=400)


# =============================================================================
# Proxy — stream a remote media URL through the dev server for previews.
# =============================================================================

# Sources that can only be reached over Tor (a clearnet browser can't load them).
# Empty today — PornHub would register here, and needs PySocks installed.
_TOR_SOURCES = set()


def _tor_proxies(source):
    """Route through the local Tor SOCKS port for sources that require it; else None."""
    if source in _TOR_SOURCES:
        return {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    return None


def _blocked_host(url):
    """Cheap SSRF guard: refuse loopback/private IP literals + localhost. Domain
    names (the real media hosts) are allowed."""
    host = (urlparse(url).hostname or "").lower()
    if not host or host == "localhost":
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_reserved
    except ValueError:
        return False


@require_GET
def proxy(request):
    """Stream a remote media URL through the dev server so the browser's <img>/
    <video> never touches the source domain directly — hotlink-safe, private, and
    Tor-ready. Forwards the client's Range header so <video> seeking works; attaches
    the RedGIFs bearer. Dev-only, localhost."""
    url = request.GET.get("url", "")
    source = request.GET.get("source", "")
    if not url or urlparse(url).scheme not in ("http", "https"):
        return HttpResponse("bad url", status=400)
    if _blocked_host(url):
        return HttpResponse("blocked host", status=400)

    headers = {"User-Agent": _BROWSER_UA}
    rng = request.META.get("HTTP_RANGE")
    if rng:
        headers["Range"] = rng
    if source == "redgifs":
        token = _redgifs_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

    try:
        upstream = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=20,
            allow_redirects=True,
            proxies=_tor_proxies(source),
        )
    except Exception as e:
        return HttpResponse(f"proxy fetch failed: {e}", status=502)
    if upstream.status_code >= 400:
        upstream.close()
        return HttpResponse(f"upstream {upstream.status_code}", status=502)

    resp = StreamingHttpResponse(
        upstream.iter_content(chunk_size=65536),
        status=upstream.status_code,  # 200, or 206 when we forwarded a Range
        content_type=upstream.headers.get("Content-Type", "application/octet-stream"),
    )
    for h in ("Content-Length", "Content-Range", "Accept-Ranges"):
        if h in upstream.headers:
            resp[h] = upstream.headers[h]
    resp["Cache-Control"] = "private, max-age=300"
    return resp


# =============================================================================
# URL patterns
# =============================================================================
urlpatterns = [
    path("options/add", options_add, name="media_finder_options_add"),
    path("options/list", options_list, name="media_finder_options_list"),
    path("options/remove", options_remove, name="media_finder_options_remove"),
    path("grab", grab, name="media_finder_grab"),
    path("proxy", proxy, name="media_finder_proxy"),
]
