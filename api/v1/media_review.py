"""
Media Review — dev tool for reviewing a game's media (approve / disapprove / note).

Auto-detects every image and video a game declares (reusing the game-review media
enumeration), classifies each into a lane (location / npc / solo / story / clothing /
phone), and persists per-item review decisions to a JSON ledger on disk.

No authentication, no database. Pure filesystem + TOML parsing — same shape as
game_review.py. Local authoring tool; relies on DEBUG media serving + open CORS.

Endpoints (under /api/v1/dev/media-review/):
- GET  list?game=<slug>     -> enriched media items with lane + names + media_url + status
- POST reviews?game=<slug>  -> upsert one {file, status, note} into media_reviews.json
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

from .game_review import GAMES_ROOT, _extract_missing_media, _resolve_final_toml

# Display order for lanes in the review UI. Lanes not listed fall to the end.
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
    reviews = _read_reviews(game_dir).get("reviews", {})

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
            item["status"] = rev.get("status")  # "approved" | "disapproved" | None
            item["note"] = rev.get("note", "")

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
            "missing": sum(1 for i in items if not i["found"]),
            "approved": sum(1 for i in items if i["status"] == "approved"),
            "disapproved": sum(1 for i in items if i["status"] == "disapproved"),
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

    Body: {"file": "...", "status": "approved"|"disapproved"|null, "note": "..."}
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
    status = body.get("status")
    if status not in ("approved", "disapproved", None):
        return JsonResponse({"error": "status must be approved, disapproved, or null"}, status=400)
    note = body.get("note", "")

    with _reviews_lock(game_dir):
        ledger = _read_reviews(game_dir)
        now = datetime.now(timezone.utc).isoformat()
        entry = ledger["reviews"].get(file_, {})
        entry.update({"status": status, "note": note, "updated_at": now})
        ledger["reviews"][file_] = entry
        ledger["game"] = game
        ledger["updated_at"] = now
        _write_reviews(game_dir, ledger)

    return JsonResponse({"ok": True, "file": file_, "review": entry})


urlpatterns = [
    path("list", list_media, name="media_review_list"),
    path("reviews", post_review, name="media_review_post"),
]
