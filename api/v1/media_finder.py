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
- POST options/clear   {game, file, all}                     -> empty the shelf (refetch)
- POST grab            {game, file, url|local_path, source}  -> install -> videos/
- GET  proxy           ?url=&source=                         -> stream a remote URL

Replacement is a SWAP, never a destruction: grab fetches to a temp file first, and
only once that succeeds does the file currently in the slot get copied into
.find-media/previous/ and registered as an option of its own. A failed fetch leaves
the slot exactly as it was.
"""

import hashlib
import ipaddress
import json
import os
import re
import shutil
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


def _previous_dir(game_dir: Path) -> Path:
    """Where a replaced asset is parked so it stays selectable. Under .find-media/
    (not videos/) so the packager never treats an old pick as a live game asset."""
    return game_dir / ".find-media" / "previous"


# Suffixes that need a <video> element in the picker; .gif previews as an <img>,
# matching how the capture extension labels its own captures.
_VIDEO_SUFFIXES = {".webm", ".mp4", ".mov", ".mkv"}
# Everything else a pool folder may legitimately hold. Kept separate from
# _VIDEO_SUFFIXES because that set drives the <video>-vs-<img> choice.
_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}

# Media CDNs that reject a request lacking a full browser UA *and* a matching site
# Referer. phncdn answers 410/470 to a bare UA, which lands as a 0-byte file or a
# HEAD failure — the single most-rediscovered gotcha in this pipeline.
_REFERER_BY_HOST = (
    ("phncdn.com", "https://www.pornhub.com/"),
    ("pornhub.com", "https://www.pornhub.com/"),
    ("redgifs.com", "https://www.redgifs.com/"),
)


def _fetch_headers(url: str, extra: dict | None = None) -> dict:
    """Browser-shaped headers for a media fetch: full UA plus the Referer the host
    expects. Falls back to the URL's own origin, which is harmless when unneeded."""
    headers = {"User-Agent": _BROWSER_UA}
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        referer = ""
        for suffix, ref in _REFERER_BY_HOST:
            if host == suffix or host.endswith("." + suffix):
                referer = ref
                break
        if not referer and parsed.scheme and host:
            referer = f"{parsed.scheme}://{host}/"
        if referer:
            headers["Referer"] = referer
    except Exception:
        pass
    if extra:
        headers.update(extra)
    return headers


def _is_ua_rejection(error: str) -> bool:
    """True when a fetch failed the way an anti-bot filter rejects a SPOOFED browser.

    Cloudflare-style bot management scores a full Chrome User-Agent that arrives
    without the rest of a real browser's fingerprint (TLS signature, sec-ch-ua,
    Accept-Language) as a lying client and returns 403 — while letting an honest
    library UA straight through. So our browser-shaped headers are not universally
    safer: they help hotlink-checking CDNs like phncdn and actively hurt these.

    Measured 2026-07-29 on images.stockcake.com (Cloudflare):
        full Chrome UA -> 403      download_direct's plain UA -> 200
        no UA at all   -> 200      python-requests default    -> 200

    Deliberately narrow: only 403/Forbidden. A 401 is a real credential failure
    and retrying without headers would just fail again, more slowly.
    """
    e = (error or "").lower()
    return "403" in e or "forbidden" in e


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


def _clean_pool_dir(raw: str) -> str:
    """Normalise a pool folder to a games-relative path, or '' if unusable.

    Deliberately NOT `parse_scene_path`: that sanitizes every segment with
    `[^a-zA-Z0-9_-] -> _` and strips a trailing media extension, so a real folder
    name would silently become one that does not exist — a permanently-missing
    pool with no error anywhere. Here we reject bad input instead of mangling it.
    """
    if not isinstance(raw, str):
        return ""
    rel = raw.replace("\\", "/").strip().strip("/")
    if not rel:
        return ""
    parts = [p for p in rel.split("/") if p]
    if any(p in (".", "..") for p in parts):
        return ""
    if parts and parts[0] == "videos":
        parts = parts[1:]
    return "/".join(parts)


def _pool_member_stem(source: str) -> str:
    """A stable, collision-resistant filename stem for one clip inside a pool.

    Derived from the source URL so re-grabbing the SAME source is idempotent
    rather than piling up near-duplicates. Members are peers with no ordering
    meaning, so the name only has to be unique and stable — the review UI is
    where a human sees them, not the filename.
    """
    digest = hashlib.md5((source or "").encode("utf-8")).hexdigest()[:10]
    return f"c{digest}"


def _pool_members(pool_path: Path) -> list:
    """Every media file inside a pool folder, natural-sorted (clip_2 < clip_10)."""
    if not pool_path.is_dir():
        return []

    def natural(name: str):
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

    out = []
    for f in sorted(pool_path.iterdir(), key=lambda p: natural(p.name)):
        if f.is_file() and f.suffix.lower() in (_VIDEO_SUFFIXES | _IMAGE_SUFFIXES):
            out.append(f)
    return out


def _add_option(
    game_dir: Path,
    game: str,
    file_: str,
    url: str,
    type_: str = "image",
    media_kind: str = "img",
    local_path: str = "",
    origin: str = "",
) -> tuple[bool, int]:
    """Append one option to a slot's shelf. Deduped by url. Returns (added, count).

    `local_path` (games-relative) marks an option whose bytes are already on disk —
    a previously-installed pick. Those install by copy, so they never depend on a
    remote URL that may have expired.
    """
    now = datetime.now(timezone.utc).isoformat()
    data = _read_options(game_dir)
    lst = data["options"].setdefault(file_, [])
    if any(o.get("url") == url for o in lst):
        return False, len(lst)
    entry = {"url": url, "type": type_, "media_kind": media_kind, "added_at": now}
    if local_path:
        entry["local_path"] = local_path
    if origin:
        entry["origin"] = origin
    lst.append(entry)
    data["game"] = game
    data["updated_at"] = now
    _write_options(game_dir, data)
    return True, len(lst)


def _drop_option(game_dir: Path, game: str, file_: str, url: str) -> None:
    """Remove one option by url — used after it has been installed into the slot."""
    if not url:
        return
    data = _read_options(game_dir)
    lst = data["options"].get(file_)
    if not lst:
        return
    kept = [o for o in lst if o.get("url") != url]
    if len(kept) == len(lst):
        return
    data["options"][file_] = kept
    data["game"] = game
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _write_options(game_dir, data)


def _preserve_current_as_option(
    game: str, game_dir: Path, file_: str, output_dir: Path, filename_base: str
) -> list[str]:
    """Copy whatever fills the slot today into .find-media/previous/ and register it
    as an option, so a replacement is reversible from the picker. Returns the
    games-relative paths preserved (empty when the slot was unfilled)."""
    kept: list[str] = []
    if not output_dir.is_dir():
        return kept
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    prev_dir = _previous_dir(game_dir)
    for existing in sorted(output_dir.iterdir()):
        if not existing.is_file() or existing.stem != filename_base:
            continue
        prev_dir.mkdir(parents=True, exist_ok=True)
        dest = prev_dir / f"{filename_base}-{stamp}{existing.suffix}"
        try:
            shutil.copy2(existing, dest)
        except Exception:
            continue  # a preserve failure must not block the swap
        rel = str(dest.relative_to(GAMES_ROOT))
        is_video = existing.suffix.lower() in _VIDEO_SUFFIXES
        _add_option(
            game_dir,
            game,
            file_,
            url=f"/games/{rel}",  # same-origin; the picker serves it without the proxy
            type_="video" if is_video else "image",
            media_kind="video" if is_video else "img",
            local_path=rel,
            origin="previous",
        )
        kept.append(rel)
    return kept


def _clear_review_status(game_dir: Path, game: str, file_: str, note: str) -> None:
    """Blank the slot's approve/disapprove verdict — the bytes changed, so the old
    verdict is about an asset that no longer exists. Imported lazily to keep this
    module free of an import-time dependency on the review ledger."""
    try:
        from api.v1.media_review import _read_reviews, _write_reviews
    except Exception:
        return
    try:
        ledger = _read_reviews(game_dir)
        now = datetime.now(timezone.utc).isoformat()
        entry = ledger["reviews"].get(file_, {})
        entry.update({"status": None, "note": note, "updated_at": now})
        ledger["reviews"][file_] = entry
        ledger["game"] = game
        ledger["updated_at"] = now
        _write_reviews(game_dir, ledger)
    except Exception:
        return


@csrf_exempt
def options_add(request):
    """POST options/add {game, file, url, type, media_kind} — store a candidate URL
    (no download). `type` is the user's label (image/gif/video); `media_kind`
    (img/video) drives how the option previews. Deduped by url."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    # The shelf is keyed by `slot_key` — the slot's STABLE identity. It defaults
    # to `file`, so an untagged slot behaves exactly as before; a slot whose block
    # authored an `id` keeps its shelf when its path moves (pool conversion, retag).
    file_ = body.get("slot_key") or body.get("file", "")
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

    added, count = _add_option(
        game_dir, game, file_, url=url, type_=type_, media_kind=media_kind
    )
    if not added:
        return JsonResponse({"ok": True, "duplicate": True, "count": count})
    return JsonResponse({"ok": True, "count": count})


@csrf_exempt
def options_clear(request):
    """POST options/clear {game, file, before, all} — prune a slot's shelf.

    A refetch should end up with a fresh shelf, but it must never empty the shelf on
    the way IN: a search that then returns thin would leave the slot with nothing and
    the previous candidates gone. (That exact ordering bug once ate three harvests.)
    So the refetch order is STOCK FIRST, PRUNE AFTER:

        t0 = now  ->  stock the new candidates  ->  options/clear {before: t0}

    `before` (ISO-8601) drops only entries added before that instant, so the freshly
    stocked shelf survives. Omit it to drop everything.

    Previously-installed picks (origin="previous") are KEPT regardless — they are this
    slot's undo history, not search results. Pass all=true to drop those too.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    # The shelf is keyed by `slot_key` — the slot's STABLE identity. It defaults
    # to `file`, so an untagged slot behaves exactly as before; a slot whose block
    # authored an `id` keeps its shelf when its path moves (pool conversion, retag).
    file_ = body.get("slot_key") or body.get("file", "")
    drop_all = bool(body.get("all"))
    before = (body.get("before") or "").strip()

    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    if not file_:
        return JsonResponse({"error": "file is required"}, status=400)

    def _keep(option: dict) -> bool:
        if not drop_all and option.get("origin") == "previous":
            return True  # the undo history is never search noise
        if before and (option.get("added_at") or "") >= before:
            return True  # stocked by the run that is doing the pruning
        return False

    data = _read_options(game_dir)
    existing = data["options"].get(file_, [])
    kept = [o for o in existing if _keep(o)]
    data["options"][file_] = kept
    data["game"] = game
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _write_options(game_dir, data)
    return JsonResponse(
        {"ok": True, "removed": len(existing) - len(kept), "kept": len(kept)}
    )


@require_GET
def options_list(request):
    """GET options/list?game=&file= — the collected option URLs for one slot."""
    game = request.GET.get("game", "")
    # The shelf is keyed by `slot_key` — the slot's STABLE identity. It defaults
    # to `file`, so an untagged slot behaves exactly as before; a slot whose block
    # authored an `id` keeps its shelf when its path moves (pool conversion, retag).
    file_ = request.GET.get("slot_key") or request.GET.get("file", "")
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
    # The shelf is keyed by `slot_key` — the slot's STABLE identity. It defaults
    # to `file`, so an untagged slot behaves exactly as before; a slot whose block
    # authored an `id` keeps its shelf when its path moves (pool conversion, retag).
    file_ = body.get("slot_key") or body.get("file", "")
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
    # ⚠️ TWO DIFFERENT STRINGS, and conflating them corrupts a game.
    #
    #   file_     — the slot's declared PATH. Decides WHERE THE BYTES GO
    #               (`parse_scene_path` below). Must stay a real path.
    #   slot_key_ — the slot's stable IDENTITY. Decides which SHELF and which
    #               VERDICT this install touches.
    #
    # They are the same string for an untagged slot, which is nearly all of them.
    # They differ once a block authors an `id`: then `slot_key_` is e.g.
    # "renner_oral" while the bytes still belong at "sex/renner_oral_t5.webm".
    # Key the write on the id and the file lands at videos/renner_oral.gif.
    file_ = body.get("file", "")
    slot_key_ = body.get("slot_key") or file_
    url = body.get("url", "")
    local_path = body.get("local_path", "")
    source = body.get("source", "")
    # A pool install ADDS a clip to a folder instead of REPLACING a single slot.
    # `file` is then the folder, and the filename is invented here.
    pool_dir = _clean_pool_dir(body.get("pool_dir", ""))

    if not game or not file_ or not (url or local_path):
        return JsonResponse(
            {"error": "game, file, and one of url/local_path are required"}, status=400
        )
    # A local option (a previously-installed pick) carries no fetchable URL.
    if not local_path and urlparse(url).scheme not in ("http", "https"):
        return JsonResponse({"error": "Invalid URL scheme"}, status=400)

    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": f"Game '{game}' not found"}, status=404)

    if pool_dir:
        # NEVER route a pool_dir through parse_scene_path: it sanitizes every
        # segment with [^a-zA-Z0-9_-] -> "_" and strips a trailing media
        # extension, so a folder name would silently become one that does not
        # exist on disk — a permanently-missing pool with no error anywhere.
        output_dir = game_dir / "videos" / pool_dir
        filename_base = None  # invented below, once the extension is known
    else:
        # file -> (subfolder, stem); collapse a leading videos/ so we never double it.
        subfolder, filename_base = parse_scene_path(file_)
        if subfolder.startswith("videos/"):
            subfolder = subfolder[len("videos/"):]
        elif subfolder == "videos":
            subfolder = ""
        output_dir = (game_dir / "videos" / subfolder) if subfolder else (game_dir / "videos")
    if not _safe_path(GAMES_ROOT, output_dir):
        return JsonResponse({"error": "Invalid path"}, status=400)

    # A local option installs by copy — its bytes are already on disk, so there is
    # no network, no expiry, and the exact previously-approved file comes back.
    src_file = None
    extra_headers = None
    auth = None  # kept in scope so a UA-rejection retry can still carry the bearer
    if local_path:
        candidate = GAMES_ROOT / local_path
        if not _safe_path(GAMES_ROOT, candidate) or not candidate.is_file():
            return JsonResponse({"error": "local_path not found"}, status=400)
        src_file = candidate
        ext = candidate.suffix.lstrip(".").lower() or "jpg"
    else:
        # RedGIFs media needs the bearer token; others are open. Every fetch STARTS
        # with a full browser UA + host-appropriate Referer, which hotlink-checking
        # CDNs require — but see _is_ua_rejection: bot-managed hosts reject exactly
        # that, so a 403 falls back to the plain UA rather than failing the slot.
        if source == "redgifs":
            token = _redgifs_token()
            if token:
                auth = {"Authorization": f"Bearer {token}"}
        extra_headers = _fetch_headers(url, auth)

        # Extension from the SOURCE url / content-type (not the TOML ext); the renderer
        # matches extension-agnostically, so an mp4 in a .webm slot still plays.
        ext = get_extension_from_url(url)
        if not ext:
            try:
                head = requests.head(
                    url, timeout=10, headers=extra_headers, allow_redirects=True
                )
                ext = get_extension_from_content_type(head.headers.get("Content-Type", ""))
            except Exception:
                pass
        if not ext:
            ext = "jpg"

    output_dir.mkdir(parents=True, exist_ok=True)
    if pool_dir:
        # Every clip in a pool coexists, so each needs a name of its own. The stem
        # is derived from the SOURCE, which makes a refetch of the same url
        # idempotent (it replaces) while a different url lands beside it.
        filename_base = _pool_member_stem(url or local_path)
    output_path = output_dir / f"{filename_base}.{ext}"

    # Fetch to a temp file FIRST. Until this succeeds the slot is not touched, so a
    # dead URL can never leave the game with an empty slot and no way back. The temp
    # name deliberately does not share `filename_base` as its stem, so the cleanup
    # loop below cannot delete the very file it is about to install.
    tmp_path = output_dir / f".incoming-{filename_base}.{ext}"
    # download_direct resumes onto an existing partial when the server supports Range,
    # so a leftover temp from an earlier crash would be appended to, not replaced.
    tmp_path.unlink(missing_ok=True)
    if src_file is not None:
        try:
            shutil.copy2(src_file, tmp_path)
            success, error = True, None
        except Exception as exc:  # noqa: BLE001 - surfaced to the caller as-is
            success, error = False, str(exc)
    else:
        success, error = download_direct(url, tmp_path, extra_headers=extra_headers)
        # A 403 here often means the opposite of what it looks like: the host did not
        # refuse the file, it refused a client CLAIMING to be Chrome without a
        # browser's fingerprint. Drop the browser UA/Referer and let download_direct
        # use its own plain UA — the bearer, if any, still rides along. One retry.
        if not success and _is_ua_rejection(error):
            tmp_path.unlink(missing_ok=True)
            success, error = download_direct(url, tmp_path, extra_headers=auth)

    if not success:
        tmp_path.unlink(missing_ok=True)
        return JsonResponse({"success": False, "error": error}, status=400)

    preserved: list = []
    if pool_dir:
        # ⚠️ A pool install ADDS; it must never run the replace path below.
        # There is no incumbent to demote (every clip in the folder is a peer),
        # and that path's same-stem delete loop would wipe a SIBLING clip —
        # installing clip 2 would silently delete clip 1.
        #
        # The one same-stem file we DO clear is this url's own earlier download
        # under a different extension (the stem is url-derived, so nothing else
        # can collide with it). Without this a re-grab that resolves .webm where
        # it once resolved .gif would leave both, and the pool would play the
        # same clip twice.
        for existing in output_dir.iterdir():
            if existing.is_file() and existing.stem == filename_base and existing != output_path:
                existing.unlink()
        os.replace(tmp_path, output_path)
    else:
        # The replacement exists. Demote the incumbent to an option, THEN clear the slot
        # (any extension, so the generator never sees an orphan it can't match).
        preserved = _preserve_current_as_option(
            game, game_dir, slot_key_, output_dir, filename_base
        )
        for existing in output_dir.iterdir():
            if existing.is_file() and existing.stem == filename_base:
                existing.unlink()
        os.replace(tmp_path, output_path)

    # The option just consumed is no longer an alternative.
    _drop_option(game_dir, game, slot_key_, url=url)
    # A single slot now holds bytes nobody has judged, so its old verdict must not
    # carry over. A POOL keeps its verdict: adding a fourth clip does not un-judge
    # the three already approved.
    if not pool_dir:
        _clear_review_status(
            game_dir, game, slot_key_, note=f"replaced via finder {datetime.now(timezone.utc).date()}"
        )

    return JsonResponse(
        {
            "success": True,
            "file_path": str(output_path.relative_to(GAMES_ROOT)),
            "previous_kept_as_option": preserved,
        }
    )


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
# Pool folders — the SELECTED half of the picker
# =============================================================================
#
# A pool block names a folder; everything inside it plays, cycling one clip per
# visit. So "selected" is not a field anywhere — it is simply "the file is in the
# folder". That makes select/unselect a move, and it means there is no second
# source of truth to drift out of sync with the build.


@require_GET
def pool_list(request):
    """GET ?game=&dir= → the clips currently IN a pool folder (i.e. selected).

    Reads `videos/`, never `output/`: the packager wipes and regenerates output/,
    so listing from there would show contents that vanish on the next build.
    """
    game = request.GET.get("game", "")
    pool_dir = _clean_pool_dir(request.GET.get("dir", ""))
    game_dir = _safe_game_dir(game)
    if game_dir is None or not pool_dir:
        return JsonResponse({"error": "game and dir are required"}, status=400)

    pool_path = game_dir / "videos" / pool_dir
    if not _safe_path(GAMES_ROOT, pool_path):
        return JsonResponse({"error": "Invalid path"}, status=400)

    items = []
    for f in _pool_members(pool_path):
        rel = str(f.relative_to(game_dir))
        items.append({
            "filename": f.name,
            "url": f"/games/{game}/{rel}",
            "media_kind": "video" if f.suffix.lower() in _VIDEO_SUFFIXES else "img",
            "bytes": f.stat().st_size,
        })
    return JsonResponse({"game": game, "dir": pool_dir, "items": items, "count": len(items)})


@csrf_exempt
def pool_unselect(request):
    """POST {game, dir, filename} → move one clip OUT of the pool folder.

    The clip stops playing immediately (the folder is the truth) and reappears on
    the shelf as an `origin: "previous"` option, so the decision is reversible in
    one click. This is `_preserve_current_as_option` narrowed to a single named
    file and made a MOVE rather than a copy.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    pool_dir = _clean_pool_dir(body.get("dir", ""))
    filename = str(body.get("filename", "") or "").strip()

    game_dir = _safe_game_dir(game)
    if game_dir is None or not pool_dir or not filename:
        return JsonResponse({"error": "game, dir and filename are required"}, status=400)
    # A filename is exactly one path segment — never a traversal.
    if "/" in filename or "\\" in filename or filename in (".", ".."):
        return JsonResponse({"error": "Invalid filename"}, status=400)

    src = game_dir / "videos" / pool_dir / filename
    if not _safe_path(GAMES_ROOT, src) or not src.is_file():
        return JsonResponse({"error": "Not found in pool"}, status=404)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    prev_dir = _previous_dir(game_dir)
    prev_dir.mkdir(parents=True, exist_ok=True)
    dest = prev_dir / f"{src.stem}-{stamp}{src.suffix}"
    try:
        shutil.move(str(src), str(dest))
    except Exception as exc:  # noqa: BLE001 - surfaced to the caller as-is
        return JsonResponse({"error": f"move failed: {exc}"}, status=500)

    rel = str(dest.relative_to(GAMES_ROOT))
    is_video = dest.suffix.lower() in _VIDEO_SUFFIXES
    # Re-shelve it keyed by the POOL — the same key the picker and the review
    # ledger use — so it shows up as an option for this pool, not an orphan.
    _add_option(
        game_dir,
        game,
        pool_dir,
        url=f"/games/{rel}",  # same-origin; the picker serves it without the proxy
        type_="video" if is_video else "image",
        media_kind="video" if is_video else "img",
        local_path=rel,
        origin="previous",
    )
    return JsonResponse({"success": True, "moved_to": rel})


# =============================================================================
# URL patterns
# =============================================================================
urlpatterns = [
    path("options/add", options_add, name="media_finder_options_add"),
    path("options/list", options_list, name="media_finder_options_list"),
    path("options/remove", options_remove, name="media_finder_options_remove"),
    path("options/clear", options_clear, name="media_finder_options_clear"),
    path("pool/list", pool_list, name="media_finder_pool_list"),
    path("pool/unselect", pool_unselect, name="media_finder_pool_unselect"),
    path("grab", grab, name="media_finder_grab"),
    path("proxy", proxy, name="media_finder_proxy"),
]
