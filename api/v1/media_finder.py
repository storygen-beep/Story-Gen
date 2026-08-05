"""
Media Finder — dev backend for the find.html "options" workflow.

The user searches Google in a real browser tab and uses the capture extension to
collect candidate media URLs as per-slot OPTIONS (stored, NOT downloaded). This
module stores those option URLs in a per-game JSON ledger, streams previews through
a proxy (hotlink-safe, Tor-ready), and on the final pick downloads the chosen URL
into the game's videos/ source-of-truth — replacing the slot's media.

No auth, no DB — filesystem + JSON ledger. Local dev tool; relies on open CORS.

Endpoints (under /api/v1/dev/media-finder/):
- POST options/add     {game, file, url, type, media_kind, query?, docid?} -> append an option
- POST queries/add     {game, file, query, urls, stocked, hosts, seed_url?} -> record a SEARCH
- POST related/fetch   {game, file, url}  -> run the related-feed fetch for one option
- GET  options/list    ?game=&file=                          -> options + queries for a slot
- POST options/remove  {game, file, url}                     -> drop an option
- POST options/clear   {game, file, all}                     -> empty the shelf (refetch)
- POST grab            {game, file, url|local_path, source}  -> install -> videos/
- GET  proxy           ?url=&source=                         -> stream a remote URL

Every stocked option remembers WHICH SEARCH found it (`found_by`), and every search
that ran is recorded whether or not it yielded anything (the `queries` root). That is
what lets the picker show one bucket per search instead of one undifferentiated pile,
and it is why nothing here ever needs to destroy a shelf to make a refetch legible.

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
import subprocess
import sys
import threading
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
from apps.common.json_ledger import ledger_lock, write_json_atomic

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
# Shape: {game, updated_at,
#         options: {<slot>: [{url, type, media_kind, added_at,
#                             found_by?:[q,…], docid?}]},
#         queries: {<slot>: [{q, at, last_at, runs, source, urls, stocked, hosts,
#                             seed_url?}]}}
# `docid` = Google's index id for the image (harvested with the url); `seed_url`
# on a source:"related" record = the option whose related-feed that run was. The
# picker derives "related fetched" from the (seed_url ↔ option.url) join.
# Both roots are keyed on the same slot identity, so they move together — see
# check_shelves._move_key. Same atomic read/write + path-guard discipline as
# api/v1/media_review.py.
# =============================================================================


def _options_path(game_dir: Path) -> Path:
    return game_dir / ".find-media" / "media_options.json"


def _previous_dir(game_dir: Path) -> Path:
    """Where a replaced asset is parked so it stays selectable. Under .find-media/
    (not videos/) so the packager never treats an old pick as a live game asset."""
    return game_dir / ".find-media" / "previous"


def _incoming_dir(game_dir: Path) -> Path:
    """Where a download is staged before it is installed — NOT the target folder.

    Every enumerator that lists a media folder filters on SUFFIX ONLY, so a partial
    file staged inside a live pool gets advertised as a real clip while it is still
    growing (measured: 3,350,528 -> 4,235,264 bytes across consecutive polls), and it
    holds tile #1 because "." sorts before "c" in natural order. Worse, the build-time
    index does the same, so a staging file present at build time can ship a truncated
    clip to a player.

    .find-media/ is the right home for exactly the reason `_previous_dir` gives: same
    filesystem as videos/ (so installing stays one atomic os.replace) but never walked
    as game media.
    """
    return game_dir / ".find-media" / "incoming"


# download_direct retries up to 5 times at TIMEOUT=60s per socket read (api/v1/dev.py),
# so no grab that is still alive can own a file this old.
_INCOMING_MAX_AGE = 6 * 3600


def _reap_stale_incoming(staging: Path) -> None:
    """Delete staging files that no in-flight grab could still own.

    A crash between download and install leaks the temp forever, and nothing else in
    this repo ever looks in that directory — so the leak is invisible and unbounded.
    The sweep lives here rather than on a schedule because this is the only code that
    creates them, the directory normally holds zero or one file, and it costs one
    iterdir. mtime rather than ctime: a live download rewrites the file continuously.
    """
    cutoff = time.time() - _INCOMING_MAX_AGE
    for leftover in staging.iterdir():
        try:
            if leftover.is_file() and leftover.stat().st_mtime < cutoff:
                leftover.unlink()
        except OSError:
            continue  # best effort — never fail a grab over housekeeping


def _install(tmp_path: Path, output_path: Path) -> str:
    """Move the staged file into place. Returns "" on success, else the reason.

    os.replace is atomic only within one filesystem. .find-media/incoming/ and videos/
    are both children of games/<game>/, so this is same-filesystem by construction —
    asserted by a test rather than assumed, because a game whose videos/ was symlinked
    onto another volume would raise EXDEV here.

    Deliberately no shutil.move fallback: that is copy-then-delete, i.e. a growing
    partial inside the live pool, i.e. the exact bug this staging split exists to kill.
    A loud error beats a silent regression on a path nobody exercises.
    """
    try:
        os.replace(tmp_path, output_path)
        return ""
    except OSError as exc:  # noqa: BLE001 - surfaced to the caller as-is
        return f"install failed: {exc}"


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
    """Load the options ledger, always fully shaped.

    ONE normalizer, deliberately — the missing-file and unparseable-file paths used to
    return their own hand-written `{"game": …, "options": {}}` literals, so every new
    root key had to be added in three places and a caller touching one the literals
    forgot would KeyError only on a game that had never been searched. Now a new root
    is one `setdefault`.
    """
    try:
        data = json.loads(_options_path(game_dir).read_text(encoding="utf-8"))
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("game", game_dir.name)
    data.setdefault("options", {})
    # Which SEARCH produced each option. Absent on every ledger written before
    # 2026-08-05 — those options carry no `found_by` and the picker files them
    # under "older searches".
    data.setdefault("queries", {})
    return data


def _write_options(game_dir: Path, data: dict) -> None:
    """Atomically replace the ledger so a crash can't truncate it.

    Call this INSIDE `_options_lock` — on its own it still loses updates, because
    the read it is writing back happened before the lock would have been taken.
    """
    write_json_atomic(_options_path(game_dir), data)


def _options_lock(game_dir: Path):
    """Serialise a read-modify-write of the options shelf. See `apps.common.json_ledger`.

    Every mutation of this file rewrites it whole, so two concurrent writers lose one
    of the two changes AND the loser's caller still gets `200 {"ok": true}`. Measured
    at 40 concurrent adds: 16 landed, 24 lost, 15 hard 500s.
    """
    return ledger_lock(_options_path(game_dir))


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
        # A dot-prefixed name is never a clip somebody selected: it is staging, an
        # editor swap file, or macOS AppleDouble (`._clip.gif` — a REAL media suffix,
        # so the suffix test alone lets it through). Listing one shifts every caption
        # and offers a partial file as pickable.
        if f.name.startswith("."):
            continue
        if f.is_file() and f.suffix.lower() in (_VIDEO_SUFFIXES | _IMAGE_SUFFIXES):
            out.append(f)
    return out


def _canon_query(raw) -> str:
    """The one canonical form of a query string.

    Whitespace-collapsed, case PRESERVED. An option's `found_by` label and the record
    in the `queries` table are joined on this string, so canonicalizing makes the join
    a pure function of the text and `options/add` never has to read the query table to
    resolve an id. Case-folding would merge "Renner oral" with "renner oral" — but the
    agent authors both sides, so that merge buys nothing and costs the pure join.
    """
    return " ".join(str(raw or "").split())


def _ensure_query(data: dict, slot: str, q: str, now: str) -> bool:
    """Open a stub record for a query seen on an option but never declared.

    A `found_by` label with no record is an INVISIBLE BUCKET — the picker groups by
    the query table, so those options would only ever be reachable through "All".
    Auto-registering here makes `queries/add` an enrichment call rather than a
    prerequisite, so an agent that crashes mid-loop still produces a coherent strip.
    Never bumps `runs`: this fires once per option, not once per search.
    """
    lst = data["queries"].setdefault(slot, [])
    if any(rec.get("q") == q for rec in lst):
        return False
    lst.append({"q": q, "at": now, "last_at": now, "runs": 1, "auto": True})
    return True


def _upsert_query(data: dict, slot: str, q: str, now: str, fields: dict) -> tuple[dict, bool]:
    """Record one SEARCH against a slot. Caller holds the options lock.

    Stored oldest-first — the picker reverses for display; `_add_option`'s
    `lst.insert(0, …)` below is an undo affordance, not an ordering convention, and
    reversing storage here would make "append" a lie and break `at` monotonicity.

    `at` is when this query FIRST ran and never moves. The yield fields are
    overwritten rather than summed: the newest evidence is the interesting one, and
    a total across runs would describe no search that ever happened.
    """
    lst = data["queries"].setdefault(slot, [])
    for rec in lst:
        if rec.get("q") != q:
            continue
        # A stub opened by the stock loop is THIS run, not a previous one — enriching
        # it must not read as a second run.
        if rec.pop("auto", None):
            pass
        else:
            rec["runs"] = int(rec.get("runs") or 1) + 1
        rec["last_at"] = now
        rec.update(fields)
        return rec, True
    rec = {"q": q, "at": now, "last_at": now, "runs": 1}
    rec.update(fields)
    lst.append(rec)
    return rec, False


def _add_option(
    game_dir: Path,
    game: str,
    file_: str,
    url: str,
    type_: str = "image",
    media_kind: str = "img",
    local_path: str = "",
    origin: str = "",
    query: str = "",
    docid: str = "",
) -> tuple[bool, int]:
    """Append one option to a slot's shelf. Deduped by url. Returns (added, count).

    `local_path` (games-relative) marks an option whose bytes are already on disk —
    a previously-installed pick. Those install by copy, so they never depend on a
    remote URL that may have expired.

    `query` is the search that produced this url. It lands in `found_by`, which is a
    LIST because dedup is by url: when a sibling query legitimately returns a url an
    earlier one already stocked, a single-valued field would record nothing and the
    picker would hide, under the second query's chip, a result that search really did
    produce. Cross-query duplicates are the common case, not the edge.

    `docid` is Google's index id for this image, harvested from the results page it
    appeared on. It is what makes "fetch related" a one-navigation lookup later
    (`tbs=rimg:` is built from its first 8 bytes), so it is stored FIRST-WRITE-WINS:
    a later harvest carrying a different docid for the same url never churns the
    file — the related feed any stored docid reaches is equivalent evidence.
    """
    now = datetime.now(timezone.utc).isoformat()
    q = _canon_query(query)
    with _options_lock(game_dir):
        data = _read_options(game_dir)
        lst = data["options"].setdefault(file_, [])
        dup = next((o for o in lst if o.get("url") == url), None)
        if dup is not None:
            # Already shelved. Credit the query that just re-found it and keep a
            # docid we did not have — but ONLY write if something actually changed.
            # Without this short-circuit a re-harvest of 400 already-stocked urls
            # becomes 400 whole-file rewrites of a 2.9 MB ledger under the lock.
            # NOTE the docid branch must work with an EMPTY q: the legacy-shelf
            # lookup enriches a bare url with its docid and sends no query.
            changed = False
            if q and q not in (dup.get("found_by") or []):
                dup.setdefault("found_by", []).append(q)
                _ensure_query(data, file_, q, now)
                changed = True
            if docid and not dup.get("docid"):
                dup["docid"] = docid
                changed = True
            if not changed:
                return False, len(lst)
            data["game"] = game
            data["updated_at"] = now
            _write_options(game_dir, data)
            return False, len(lst)

        entry = {"url": url, "type": type_, "media_kind": media_kind, "added_at": now}
        if local_path:
            entry["local_path"] = local_path
        if origin:
            entry["origin"] = origin
        if docid:
            entry["docid"] = docid
        # A demoted pick has no search behind it, so it never gets a label — it is
        # undo history, and filing it under a query would be a category error.
        if q and origin != "previous":
            entry["found_by"] = [q]
            _ensure_query(data, file_, q, now)

        if origin == "previous":
            # A just-demoted pick goes to the FRONT. Appending buried it: media_lab's
            # shelf is 148 deep, so an unselected clip landed at position 149 and the
            # "one click to undo" this is supposed to give you meant scrolling past
            # everything first. Fresh candidates still append — their order is the
            # harvest order, which the fetcher re-ranks anyway.
            lst.insert(0, entry)
        else:
            lst.append(entry)
        data["game"] = game
        data["updated_at"] = now
        _write_options(game_dir, data)
        return True, len(lst)


class _MangledHost(ValueError):
    """A hostname arrived carrying the display-only `" DOT "` transform."""


def _clean_hosts(raw):
    """Validate an agent-supplied host histogram. Returns [[host, count], …] or None.

    None means "unusable, drop the field" — a malformed histogram must not fail the
    whole query record, because the record is still worth having without it.

    Raises `_MangledHost` on a `" DOT "`-separated name. That transform exists ONLY to
    keep bare dotted CDN hostnames out of a tool's RETURN VALUE, where a secret-scanner
    redacts them as `[BLOCKED: JWT token]` — a POST body never passes through that
    filter. If a transformed name ever reaches the store the damage is permanent: a
    hostname that legitimately contains " DOT " is indistinguishable from a mangled
    one, so nothing downstream could ever undo it. Hard refusal, never a silent repair.
    """
    if raw is None:
        return None
    if not isinstance(raw, list):
        return None
    out = []
    for pair in raw[:64]:
        if not isinstance(pair, list | tuple) or len(pair) != 2:
            return None
        host, count = pair
        if not isinstance(host, str) or not host or len(host) > 253:
            return None
        if " DOT " in host:
            raise _MangledHost(host)
        try:
            out.append([host, int(count)])
        except (TypeError, ValueError):
            return None
    return out


def _append_query_ledger(
    game_dir: Path,
    slot: str,
    q: str,
    source: str,
    urls: int,
    round_,
    status: str,
    seed_url: str = "",
) -> None:
    """Mirror one query into `.find-media/query_ledger.jsonl` — the durable copy.

    `media_options.json` is rewritten whole on every write, and `_read_options` reads a
    torn file back as EMPTY, so one bad write can take the entire query history with
    it. This file is only ever appended to, which makes it the copy that survives —
    and it is the raw log the lexicon's verdicts are derived from, so it has to outlive
    the shelf.

    Writing it here rather than by hand is also what finally makes the skill's
    long-standing "the only machine-written record" claim true, and removes the drift
    that two hand-maintained logs of one fact guarantee.

    Best-effort: a logging failure must never fail the call that did the real work.
    """
    try:
        path_ = game_dir / ".find-media" / "query_ledger.jsonl"
        path_.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "slot": slot,
            "query": q,
            "date": datetime.now(timezone.utc).date().isoformat(),
            "round": round_,
            "source": source,
            "urls_yielded": urls,
            "status": status,
        }
        if seed_url:
            row["seed_url"] = seed_url
        # O_APPEND: concurrent per-slot agents interleave whole lines, never bytes.
        with path_.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception:
        return


def _drop_option(game_dir: Path, game: str, file_: str, url: str, local_path: str = "") -> None:
    """Remove one option, by url or by local_path — it has just been installed.

    `local_path` matters because a previously-demoted pick is re-selected by COPY:
    its `url` is empty, so matching on url alone left it sitting on the shelf as an
    available option while it was already back in the slot.
    """
    if not url and not local_path:
        return
    with _options_lock(game_dir):
        data = _read_options(game_dir)
        lst = data["options"].get(file_)
        if not lst:
            return
        kept = [
            o for o in lst
            if not ((url and o.get("url") == url)
                    or (local_path and o.get("local_path") == local_path))
        ]
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
        from api.v1.media_review import _read_reviews, _reviews_lock, _write_reviews
    except Exception:
        return
    try:
        with _reviews_lock(game_dir):
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
    """POST options/add {game, file, url, type, media_kind, query?} — store a candidate
    URL (no download). `type` is the user's label (image/gif/video); `media_kind`
    (img/video) drives how the option previews. Deduped by url.

    `query` is optional and the request is byte-identical to the pre-2026-08-05
    behaviour without it — the capture extension still posts without one, and ~19,300
    already-stocked options carry no label."""
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

    # docid: Google's index id for this image, when the harvest could pair it.
    # Malformed → drop the FIELD and store the option anyway (the `_clean_hosts`
    # precedent, not `_MangledHost`'s): a bad docid is recoverable later via the
    # grid lookup, so it is never worth losing the option over.
    docid = str(body.get("docid") or "")
    if docid and not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", docid):
        docid = ""

    added, count = _add_option(
        game_dir, game, file_, url=url, type_=type_, media_kind=media_kind,
        query=body.get("query", ""), docid=docid,
    )
    if not added:
        return JsonResponse({"ok": True, "duplicate": True, "count": count})
    return JsonResponse({"ok": True, "count": count})


@csrf_exempt
def queries_add(request):
    """POST queries/add — record one SEARCH against a slot, whatever it yielded.

    Body: {game, file|slot_key, query, source?, urls?, stocked?, hosts?, round?,
           status?, seed_url?}

    `seed_url` marks a RELATED fetch (source "related"): the stocked option whose
    Google related-feed this run harvested. It is the join key the picker derives
    "related fetched or not" from, so it is validated hard (400) and guarded against
    label collisions (409) — a record that silently lost or swapped its seed is a
    related bucket that can never again be attributed to its seed.

    This is what turns a slot's shelf from one undifferentiated pile into labelled
    buckets. Two things here are not obvious:

    - **Zero-yield queries are the point, not an edge case.** A search that came back
      with nothing is the record that stops the same dead query being re-run three
      rounds later, and it is unrecoverable if not written down at the moment it fails.
    - **The response carries no hostnames.** The caller is a `javascript_tool` REPL
      whose return value passes through a secret-scanner that redacts bare dotted
      hostnames; echoing the histogram back would blank the very confirmation the
      agent needs to know the POST landed.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    # Same key discipline as every other options endpoint: the shelf and its query
    # table are both keyed on the slot's STABLE identity.
    file_ = body.get("slot_key") or body.get("file", "")
    q = _canon_query(body.get("query", ""))

    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    if not file_ or not q:
        return JsonResponse({"error": "file and query are required"}, status=400)

    try:
        hosts = _clean_hosts(body.get("hosts"))
    except _MangledHost as exc:
        return JsonResponse(
            {
                "error": f"host '{exc}' carries the display-only ' DOT ' transform. "
                "POST real hostnames; apply that transform only to the value your "
                "script RETURNS, never to what it sends."
            },
            status=400,
        )

    seed_url = str(body.get("seed_url") or "")
    if seed_url and (
        urlparse(seed_url).scheme not in ("http", "https") or len(seed_url) > 2048
    ):
        return JsonResponse(
            {"error": "seed_url must be http(s) and ≤2048 chars"}, status=400
        )

    fields = {
        "source": str(body.get("source") or "google"),
        "urls": int(body.get("urls") or 0),
        "stocked": int(body.get("stocked") or 0),
    }
    if hosts is not None:
        fields["hosts"] = hosts
    if seed_url:
        fields["seed_url"] = seed_url
    if body.get("round") is not None:
        fields["round"] = body.get("round")
    if body.get("status"):
        fields["status"] = str(body.get("status"))

    now = datetime.now(timezone.utc).isoformat()
    with _options_lock(game_dir):
        data = _read_options(game_dir)
        # Label-collision guard: `_upsert_query` matches on q and `rec.update(fields)`
        # would silently RESEAT an existing label onto a new seed — merging two seeds'
        # buckets and corrupting the first seed's derived status. The runner suffixes
        # labels client-side, but two concurrent fetches can race; this makes the
        # invariant server-owned.
        existing = next(
            (r for r in data["queries"].get(file_, []) if r.get("q") == q), None
        )
        if (
            existing is not None
            and seed_url
            and existing.get("seed_url")
            and existing["seed_url"] != seed_url
        ):
            return JsonResponse(
                {"error": f"label '{q}' already belongs to a different seed — "
                          "suffix the label and retry"},
                status=409,
            )
        _rec, duplicate = _upsert_query(data, file_, q, now, fields)
        data["game"] = game
        data["updated_at"] = now
        _write_options(game_dir, data)
        count = len(data["queries"].get(file_, []))

    _append_query_ledger(
        game_dir, file_, q, fields["source"], fields["urls"],
        body.get("round"), str(body.get("status") or "ok"), seed_url=seed_url,
    )
    return JsonResponse({"ok": True, "duplicate": duplicate, "count": count})


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

    with _options_lock(game_dir):
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
    """GET options/list?game=&file= — one slot's option URLs AND the searches that
    produced them.

    `queries` is additive; a caller that only reads `options` is unaffected. It is
    ~2-4 KB per slot against an options array that reaches 816 entries, so it rides
    the picker's existing poll for free."""
    game = request.GET.get("game", "")
    # The shelf is keyed by `slot_key` — the slot's STABLE identity. It defaults
    # to `file`, so an untagged slot behaves exactly as before; a slot whose block
    # authored an `id` keeps its shelf when its path moves (pool conversion, retag).
    file_ = request.GET.get("slot_key") or request.GET.get("file", "")
    game_dir = _safe_game_dir(game)
    if game_dir is None:
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    data = _read_options(game_dir)
    return JsonResponse({
        "options": data["options"].get(file_, []),
        "queries": data["queries"].get(file_, []),
    })


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

    with _options_lock(game_dir):
        data = _read_options(game_dir)
        kept = [o for o in data["options"].get(file_, []) if o.get("url") != url]
        data["options"][file_] = kept
        # `game` too — every other write site stamps both, and this one silently
        # didn't, so a ledger that ever lost its `game` key could never regain it
        # through the one endpoint a human clicks most.
        data["game"] = game
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
        # A dot-prefixed basename is staging or OS metadata, never a pick. One such
        # entry reached a shelf before the guards above existed, so an open picker tab
        # can still be holding a rendered tile for it — refuse the click rather than
        # reinstall a truncated file.
        if candidate.name.startswith("."):
            return JsonResponse({"error": "Refusing a dot-prefixed local_path"}, status=400)
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
    # dead URL can never leave the game with an empty slot and no way back.
    #
    # The temp lives in .find-media/incoming/, NOT in output_dir. It used to sit in the
    # target folder under a ".incoming-<stem>" name, and the ONLY thing stopping the
    # cleanup loops below from deleting the file they were about to install was that the
    # dotted stem happened not to equal `filename_base` — a lexical coincidence. Staging
    # elsewhere makes that structural: the loops cannot reach it under any name, and no
    # enumerator can advertise a half-written file as a real clip. Do not move it back.
    staging = _incoming_dir(game_dir)
    staging.mkdir(parents=True, exist_ok=True)
    _reap_stale_incoming(staging)
    # pid + thread id, the same collision-safe convention write_json_atomic uses
    # (apps/common/json_ledger.py). `filename_base` alone is NOT unique: _pool_member_stem
    # is md5(url), so the same url grabbed into two different pools yields the same base,
    # and the dev server is thread-per-request.
    tmp_path = staging / f"{filename_base}.{os.getpid()}.{threading.get_ident()}.{ext}.part"
    try:
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
            #
            # The staged download is NOT in this folder, so this loop cannot reach it.
            for existing in output_dir.iterdir():
                if existing.is_file() and existing.stem == filename_base and existing != output_path:
                    existing.unlink(missing_ok=True)  # a concurrent unselect may have won
            reason = _install(tmp_path, output_path)
        else:
            # The replacement exists. Demote the incumbent to an option, THEN clear the slot
            # (any extension, so the generator never sees an orphan it can't match).
            preserved = _preserve_current_as_option(
                game, game_dir, slot_key_, output_dir, filename_base
            )
            for existing in output_dir.iterdir():
                if existing.is_file() and existing.stem == filename_base:
                    existing.unlink(missing_ok=True)
            reason = _install(tmp_path, output_path)
        if reason:
            # JSON, not an uncaught raise: find.html parses every response body
            # unconditionally, so Django's HTML debug 500 page would surface as the
            # misleading "server unreachable" instead of the real reason.
            return JsonResponse({"success": False, "error": reason}, status=500)

        # The option just consumed is no longer an alternative.
        # Pass both: a re-selected previous pick carries a local_path and no url, so
        # dropping by url alone would leave it listed as an option it no longer is.
        _drop_option(game_dir, game, slot_key_, url=url, local_path=local_path)
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
    finally:
        # Every exit path — success, refusal, exception — leaves nothing behind. After a
        # successful install the temp is already gone, so this is a no-op there. The inner
        # guard is not decoration: a raise inside `finally` REPLACES the pending exception,
        # so a permissions hiccup here would mask the actual download failure.
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass  # a leaked staging file is the reaper's problem, not the caller's


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
    # A filename is exactly one path segment — never a traversal, and never a dotfile.
    # A leading dot means staging or OS metadata, and shelving one as a "previous pick"
    # is how a truncated 2 MB GIF became a one-click option. startswith(".") subsumes
    # the old `filename in (".", "..")` check.
    if "/" in filename or "\\" in filename or filename.startswith("."):
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


_RUNNER_LAUNCH = (
    '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" '
    '--user-data-dir="$HOME/.chrome-find-media" --remote-debugging-port=9222'
)

# ONE related fetch at a time. The runner is a single browser: concurrent CDP
# clients contend on its one debug websocket and lose intermittently (measured
# live 2026-08-05 — rapid ⇢ clicks produced `<ws disconnected> code=1000` connect
# failures). The picker also gates client-side; this lock is the guarantee.
_RELATED_FETCH_LOCK = threading.Lock()


@csrf_exempt
def related_fetch(request):
    """POST related/fetch {game, file|slot_key, url} — shelve one option's Google
    related-feed as a new labelled bucket, via scripts/fetch_related.py.

    The fetch runs in the dedicated find-media Chrome (CDP on :9222); this view is
    only the orchestrator: preflight the port so a dead runner fails in 1.5s with
    the launch command instead of a 180s hang, shell the script, map its exit codes
    onto HTTP. 180s not 120: a legacy option without a stored docid costs an extra
    grid navigation for the lookup.

    NOTE the script POSTs back to THIS server (one options/add per url), so a
    single-threaded server (--nothreading, 1-worker sync) deadlocks here until the
    timeout. The threaded dev runserver is fine — run it threaded.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body = _parse_body(request)
    game = body.get("game", "")
    slot_key = body.get("slot_key") or body.get("file", "")
    file_ = body.get("file") or slot_key
    url = body.get("url", "")

    game_dir = _safe_game_dir(game)
    if game_dir is None or not game_dir.is_dir():
        return JsonResponse({"error": "Invalid or missing game"}, status=400)
    if not slot_key or not url:
        return JsonResponse({"error": "file and url are required"}, status=400)
    if urlparse(url).scheme not in ("http", "https"):
        return JsonResponse({"error": "Invalid URL scheme"}, status=400)

    try:
        requests.get("http://localhost:9222/json/version", timeout=1.5)
    except requests.RequestException:
        return JsonResponse(
            {"error": "Related-fetch runner is not connected — no Chrome on :9222. "
                      f"Launch the dedicated profile: {_RUNNER_LAUNCH}"},
            status=503,
        )

    if not _RELATED_FETCH_LOCK.acquire(blocking=False):
        return JsonResponse(
            {"error": "Another related fetch is already running — the runner is one "
                      "browser, one fetch at a time. Retry when it finishes."},
            status=429,
        )
    script = Path(settings.BASE_DIR) / "scripts" / "fetch_related.py"
    try:
        proc = subprocess.run(  # noqa: S603 - fixed script path, validated args
            [sys.executable, str(script), "--game", game, "--slot-key", slot_key,
             "--file", file_, "--seed-url", url],
            capture_output=True, text=True, timeout=180,
        )
    except subprocess.TimeoutExpired:
        return JsonResponse({"error": "Related fetch timed out after 180s"}, status=504)
    finally:
        _RELATED_FETCH_LOCK.release()

    tail = (proc.stderr or "").strip()[-400:]
    if proc.returncode == 3:
        return JsonResponse(
            {"error": "Google served a captcha — wait a while and retry, or ask "
                      "the agent to fetch instead.", "detail": tail},
            status=502,
        )
    if proc.returncode == 4:
        return JsonResponse(
            {"error": "No Google id stored for this clip — nothing was fetched. "
                      "Run a search on this slot; any search that re-finds this "
                      "clip attaches an id to it in place.",
             "detail": tail},
            status=404,
        )
    if proc.returncode == 5:
        # The runner answered the preflight but could not be driven. Own the
        # message here rather than relaying a stderr tail — that tail is a
        # websocket log, and it reads as gibberish on a tile.
        return JsonResponse(
            {"error": "The find-media Chrome answered but could not be driven. "
                      f"Quit it and relaunch: {_RUNNER_LAUNCH}", "detail": tail},
            status=503,
        )
    if proc.returncode == 7:
        return JsonResponse(
            {"error": "The related feed came back empty of porn hosts — that is "
                      "usually the wrong Chrome on :9222, or SafeSearch back ON in "
                      "the find-media profile.", "detail": tail},
            status=503,
        )
    if proc.returncode != 0:
        return JsonResponse(
            {"error": f"runner exited {proc.returncode}", "detail": tail}, status=500
        )
    try:
        result = json.loads((proc.stdout or "").strip().splitlines()[-1])
    except (ValueError, IndexError):
        return JsonResponse(
            {"error": "runner returned no result line", "detail": tail}, status=500
        )
    return JsonResponse(result)


# =============================================================================
# URL patterns
# =============================================================================
urlpatterns = [
    path("options/add", options_add, name="media_finder_options_add"),
    path("queries/add", queries_add, name="media_finder_queries_add"),
    path("related/fetch", related_fetch, name="media_finder_related_fetch"),
    path("options/list", options_list, name="media_finder_options_list"),
    path("options/remove", options_remove, name="media_finder_options_remove"),
    path("options/clear", options_clear, name="media_finder_options_clear"),
    path("pool/list", pool_list, name="media_finder_pool_list"),
    path("pool/unselect", pool_unselect, name="media_finder_pool_unselect"),
    path("grab", grab, name="media_finder_grab"),
    path("proxy", proxy, name="media_finder_proxy"),
]
