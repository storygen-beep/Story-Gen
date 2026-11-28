"""
Media Review — dev tool for reviewing a game's media (approve / disapprove / note).

Auto-detects every image and video a game declares (reusing the game-review media
enumeration), classifies each into a lane (location / npc / solo / story / clothing /
phone) and a content band (explicit / nudity / borderline / clean — see
`apps.common.media_band`), and persists per-item review decisions to a JSON ledger.

No authentication, no database. Pure filesystem + TOML parsing — same shape as
game_review.py. Local authoring tool; relies on DEBUG media serving + open CORS.

Endpoints (under /api/v1/dev/media-review/):
- GET  list?game=<slug>     -> enriched media items with lane + names + media_url + status
                               + shelf depth (options_count / options_total)
- POST reviews?game=<slug>  -> upsert one {file, status, note} into media_reviews.json
                               status: approved | disapproved | not_needed | null
                               and/or {findability}: green | yellow | red | null — how
                               easy the right media was to find on the shelf (LO,
                               2026-11-28). Each key is written only when the body
                               carries it, so a colour never clobbers a verdict.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import tomli

from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.common.json_ledger import ledger_lock, write_json_atomic
from apps.common.media_band import is_nsfw

from .game_review import GAMES_ROOT, _extract_missing_media, _resolve_final_toml

# Display order for lanes in the review UI. Lanes not listed fall to the end.
# How easy the right media was to find on its shelf (media_reviews.json `findability`).
FINDABILITY = ("green", "yellow", "red")

LANE_ORDER = [
    "location",
    "npc",
    "solo",
    "story",
    "clothing",
    "phone",
    "portrait",
    "other",
]


# =============================================================================
# Helpers
# =============================================================================

def _safe_game_dir(game: str) -> Path | None:
    """Resolve games/<game>, guarding against path traversal. None if invalid."""
    if not game:
        return None
    game_dir = GAMES_ROOT / game
    try:
        # is_relative_to (not a bare startswith) so a sibling like ../games_secret
        # can't slip past the prefix check.
        if not game_dir.resolve().is_relative_to(GAMES_ROOT.resolve()):
            return None
    except Exception:
        return None
    return game_dir


def _reviews_path(game_dir: Path) -> Path:
    return game_dir / ".find-media" / "media_reviews.json"


def _read_reviews(game_dir: Path) -> dict:
    """Load the per-game review ledger. Shape: {game, updated_at, reviews:{file:{...}}}."""
    path_ = _reviews_path(game_dir)
    if not path_.exists():
        return {"game": game_dir.name, "reviews": {}}
    try:
        with path_.open(encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"game": game_dir.name, "reviews": {}}
    data.setdefault("reviews", {})
    return data


def _write_reviews(game_dir: Path, data: dict) -> None:
    """Atomically replace the ledger so a crash mid-write can't truncate it — a
    truncated ledger reads back as empty = total review loss.

    Call this INSIDE `_reviews_lock`. This ledger has TWO writers in different
    modules — the review UI here, and `media_finder._clear_review_status`, which
    blanks a verdict when `grab` replaces the bytes — so an unlocked
    read-modify-write can drop one of them.
    """
    write_json_atomic(_reviews_path(game_dir), data)


def _reviews_lock(game_dir: Path):
    """Serialise a read-modify-write of the review ledger. See `apps.common.json_ledger`."""
    return ledger_lock(_reviews_path(game_dir))


# A missing spot the human decided needs no media. It leaves "missing" everywhere —
# this page's counts AND game-review's `missing_media`, which the media search reads —
# so no harvest session stocks a shelf for it.
NOT_NEEDED = "not_needed"


def not_needed_keys(game_dir: Path) -> set:
    """Review keys (slot_key or file) the human marked Not needed."""
    return {
        k for k, v in _read_reviews(game_dir).get("reviews", {}).items()
        if isinstance(v, dict) and v.get("status") == NOT_NEEDED
    }


def _lane_for(item: dict, canvas_by_id: dict, npc_name_by_id: dict) -> dict:
    """Classify a media item into a lane and attach npc context.

    Returns a dict with at least {lane}, plus {npc_id, npc_name, ambient} when the
    backing canvas is gated on an NPC. Lane logic mirrors the doctrine:
    npc/requires_npc -> npc; trigger_mode=random -> ambient flag; neither -> solo.
    """
    mtype = item.get("type")
    cid = item.get("canvas_id")

    if mtype == "location_image":
        return {"lane": "location"}
    if mtype == "portrait_image":
        # Faces and player-portrait states are UI chrome, not scene media — they have
        # no backing canvas to classify against, so they get their own lane.
        return {"lane": "portrait"}
    if cid == "wardrobe":
        return {"lane": "clothing"}
    if cid == "phone":
        return {"lane": "phone"}

    canvas = canvas_by_id.get(cid, {})
    trigger = canvas.get("trigger", {}) or {}
    npc_id = trigger.get("npc") or trigger.get("requires_npc")

    info: dict = {}
    if npc_id:
        info["lane"] = "npc"
        info["npc_id"] = npc_id
        info["npc_name"] = npc_name_by_id.get(npc_id, npc_id)
        if trigger.get("trigger_mode") == "random":
            info["ambient"] = True
    elif item.get("category") == "Story":
        info["lane"] = "story"
    else:
        info["lane"] = "solo"

    loc_id = trigger.get("location")
    if loc_id:
        info["location_id"] = loc_id
    return info


def _read_shelf(game_dir: Path) -> dict:
    """Candidate URLs stocked per slot, from media_finder's options ledger.

    Imported lazily: media_finder already imports THIS module (from
    `_clear_review_status`), so a module-level import here would be a cycle. A
    broken import must not take the list endpoint down with it — the shelf is
    extra context on every row, not the row itself.
    """
    try:
        from .media_finder import _read_options
    except Exception:
        return {}
    return _read_options(game_dir).get("options", {})


def _nothing_selected(item: dict) -> bool:
    """No asset chosen for this slot yet — the state a stocked shelf can resolve.

    A pool is judged on its FOLDER being empty, not on `found`: a pool holding 1
    of 4 clips is already `found` (game_review._extract_missing_media), and it
    keeps the softer `n of target` signal instead of reading as unstarted.
    """
    if item.get("pool_dir"):
        return not item.get("pool_count")
    return not item["found"]


def _lines_by_spot(data: dict) -> dict:
    """{spot: {"screen": "<scene> · <screen>", "line": "..."}} — the words each picture sits under, so the review
    page can show what the picture is FOR (LO, 2026-11-18). A block placed after a line gets that line; one at the
    top of its screen gets the screen's first lines. Every version of a screen's text is joined, so a picture that
    can only fit one of them shows it."""
    out: dict = {}

    def texts(blocks, acc):
        for b in blocks or []:
            if isinstance(b, dict):
                if b.get("type") in ("paragraph", "dialog") and b.get("content"):
                    acc.append(str(b["content"]))
                texts(b.get("blocks"), acc)
                texts((b.get("props") or {}).get("blocks"), acc)
        return acc

    def walk(blocks, screen, before, rest):
        for i, b in enumerate(blocks or []):
            if not isinstance(b, dict):
                continue
            if b.get("type") in ("image", "video"):
                p = b.get("props") or {}
                name = p.get("pool_dir") or p.get("file")
                if name and name not in out:
                    after = texts(blocks[i + 1:], []) + rest
                    line = before[-1] if before else " / ".join(after[:3])
                    out[name] = {"screen": screen, "line": line[:400]}
            elif b.get("type") in ("paragraph", "dialog") and b.get("content"):
                before = before + [str(b["content"])]
            walk(b.get("blocks"), screen, before, texts(blocks[i + 1:], []) + rest)
            walk((b.get("props") or {}).get("blocks"), screen, before, rest)

    for c in data.get("canvases", []) or []:
        for n in c.get("nodes") or []:
            walk(n.get("blocks"), f"{c.get('name') or c.get('id')} · {n.get('name') or n.get('id')}", [], [])
    return out


def _enumerate(game: str, game_dir: Path) -> dict | None:
    """Parse the game and return enriched, review-merged media items. None if no TOML."""
    toml_path = _resolve_final_toml(game_dir)
    if toml_path is None or not toml_path.exists():
        return None
    with toml_path.open("rb") as f:
        data = tomli.load(f)

    canvas_by_id = {c.get("id", ""): c for c in data.get("canvases", [])}
    location_name_by_id = {l.get("id", ""): l.get("name", "") for l in data.get("locations", [])}
    npc_name_by_id = {n.get("id", ""): n.get("name", "") for n in data.get("npcs", [])}
    loc_by_image = {l["image"]: l for l in data.get("locations", []) if l.get("image")}

    media = _extract_missing_media(data, game)
    lines = _lines_by_spot(data)
    reviews = _read_reviews(game_dir).get("reviews", {})
    shelf = _read_shelf(game_dir)

    items = []
    for found, group in (("found", media["found"]), ("missing", media["missing"])):
        for raw in group:
            item = dict(raw)
            item["found"] = (found == "found")
            # normalize the rendered type to image/video
            item["media_type"] = item.get("actual_type") or (
                "video" if item.get("type") == "video" else "image"
            )
            item.update(_lane_for(item, canvas_by_id, npc_name_by_id))
            # the words this picture sits under (LO, 2026-11-18)
            ln = lines.get(item.get("pool_dir") or item.get("file")) or {}
            item["screen"] = ln.get("screen", "")
            item["line"] = ln.get("line", "")

            # location context
            if item.get("lane") == "location":
                loc = loc_by_image.get(item.get("file"))
                if loc:
                    item["location_id"] = loc.get("id", "")
                    item["location_name"] = loc.get("name", "")
            elif item.get("location_id"):
                item["location_name"] = location_name_by_id.get(item["location_id"], item["location_id"])

            # renderable URL (found only) — served by config/urls.py range_serve.
            # quote() keeps "/" but escapes spaces / # / ? so odd filenames survive.
            if item.get("found") and item.get("serve_path"):
                item["media_url"] = f"/games/{quote(game)}/{quote(item['serve_path'])}"

            # merge saved review (keyed by the declared file path)
            # Read the verdict under the same key it was written with.
            rev = reviews.get(item.get("slot_key") or item.get("file"), {})
            item["status"] = rev.get("status")  # "approved" | "disapproved" | "not_needed" | None
            item["note"] = rev.get("note", "")
            # Green: found on the shelf easily and it matches. Yellow: hard to find.
            # Red: impossible. A finding about the SEARCH, kept apart from the verdict.
            item["findability"] = rev.get("findability")

            # Shelf depth, read under the same key as the verdict. Attached BEFORE
            # the dedupe below so the surviving row of a reused asset keeps its own
            # counts. `origin: "previous"` entries are the slot's undo history, not
            # candidates to pick from — a shelf holding only those is unworked.
            opts = shelf.get(item.get("slot_key") or item.get("file")) or []
            item["options_total"] = len(opts)
            item["options_count"] = sum(1 for o in opts if o.get("origin") != "previous")

            items.append(item)

    # Dedupe by file: one review row per ASSET. A file reused across canvases is
    # one decision, not N — otherwise it double-counts, renders twice under
    # different lanes, and a single POST silently updates every copy. First
    # occurrence keeps the row + lane; the other placements are listed in reused_in.
    deduped: dict = {}
    order_keep: list = []
    for it in items:
        f = it.get("file")
        if f not in deduped:
            deduped[f] = it
            order_keep.append(f)
        else:
            keep = deduped[f]
            label = it.get("canvas_name") or it.get("location_name") or it.get("canvas_id")
            kept_label = keep.get("canvas_name") or keep.get("location_name") or keep.get("canvas_id")
            if label and label != kept_label:
                keep.setdefault("reused_in", [])
                if label not in keep["reused_in"]:
                    keep["reused_in"].append(label)
    items = [deduped[f] for f in order_keep]

    return {
        "game": game,
        "toml": toml_path.name,
        "lane_order": LANE_ORDER,
        "counts": {
            "total": len(items),
            "found": sum(1 for i in items if i["found"]),
            "missing": sum(1 for i in items if not i["found"] and i["status"] != NOT_NEEDED),
            "not_needed": sum(1 for i in items if not i["found"] and i["status"] == NOT_NEEDED),
            "approved": sum(1 for i in items if i["status"] == "approved"),
            "disapproved": sum(1 for i in items if i["status"] == "disapproved"),
            "findability": {
                c: sum(1 for i in items if i.get("findability") == c) for c in FINDABILITY
            },
            # Shelf state: work waiting on the HUMAN vs work waiting on the SEARCH.
            "ready_to_pick": sum(
                1 for i in items
                if i["options_count"] and _nothing_selected(i) and i["status"] != NOT_NEEDED
            ),
            "unworked": sum(
                1 for i in items
                if not i["found"] and not i["options_count"] and i["status"] != NOT_NEEDED
            ),
            # Content band and slot shape. Both are per-SLOT: a pool is one row
            # holding N clips, so `pool` counts folders, not files.
            "nsfw": sum(1 for i in items if is_nsfw(i.get("band", "clean"))),
            "sfw": sum(1 for i in items if not is_nsfw(i.get("band", "clean"))),
            "pool": sum(1 for i in items if i.get("pool_dir")),
            "single": sum(1 for i in items if not i.get("pool_dir")),
        },
        "items": items,
    }


# =============================================================================
# Views
# =============================================================================

@require_GET
def list_media(request):
    """GET /api/v1/dev/media-review/list?game=<slug> — enriched media + review status."""
    game = request.GET.get("game", "")
    game_dir = _safe_game_dir(game)
    if game_dir is None:
        return JsonResponse({"error": "Invalid or missing game parameter"}, status=400)
    result = _enumerate(game, game_dir)
    if result is None:
        return JsonResponse({"error": "No final TOML found for game"}, status=404)
    return JsonResponse(result)


@csrf_exempt
@require_POST
def post_review(request):
    """POST /api/v1/dev/media-review/reviews?game=<slug>

    Body: {"file": "...", "status": "approved"|"disapproved"|"not_needed"|null, "note": "..."}
    Upserts one entry into games/<slug>/.find-media/media_reviews.json.
    """
    game = request.GET.get("game", "")
    game_dir = _safe_game_dir(game)
    if game_dir is None:
        return JsonResponse({"error": "Invalid or missing game parameter"}, status=400)

    try:
        body = json.loads(request.body or b"{}")
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    # Verdicts file under `slot_key` — the slot's STABLE identity — defaulting to
    # `file` so an untagged slot is unchanged. A tagged slot keeps its verdict when
    # its path moves (pool conversion, tier retag).
    file_ = body.get("slot_key") or body.get("file")
    if not file_:
        return JsonResponse({"error": "Missing 'file'"}, status=400)
    if "status" not in body and "findability" not in body:
        return JsonResponse({"error": "Send 'status' or 'findability'"}, status=400)
    status = body.get("status")
    if status not in ("approved", "disapproved", NOT_NEEDED, None):
        return JsonResponse(
            {"error": "status must be approved, disapproved, not_needed, or null"}, status=400
        )
    findability = body.get("findability")
    if findability not in FINDABILITY + (None,):
        return JsonResponse({"error": "findability must be green, yellow, red, or null"}, status=400)

    with _reviews_lock(game_dir):
        ledger = _read_reviews(game_dir)
        now = datetime.now(timezone.utc).isoformat()
        entry = ledger["reviews"].get(file_, {})
        # Only the keys the body carries change: the colour buttons send findability
        # alone, the verdict buttons send status and note, and neither wipes the other.
        changes = {"updated_at": now}
        if "status" in body:
            changes["status"] = status
            changes["note"] = body.get("note", "")
        elif "note" in body:
            changes["note"] = body.get("note", "")
        if "findability" in body:
            changes["findability"] = findability
        entry.update(changes)
        ledger["reviews"][file_] = entry
        ledger["game"] = game
        ledger["updated_at"] = now
        _write_reviews(game_dir, ledger)

    return JsonResponse({"ok": True, "file": file_, "review": entry})


urlpatterns = [
    path("list", list_media, name="media_review_list"),
    path("reviews", post_review, name="media_review_post"),
]
