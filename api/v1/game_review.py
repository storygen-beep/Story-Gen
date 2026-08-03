"""
Game Review — dev tool for reviewing TOML game structure and progression.

Parses the game's merged *_final_game.toml and renders an interactive overview showing:
- Story arc flow (chapters, nodes, flag chains)
- Activity canvases with conditional choices
- Trait/flag control panel for testing unlock states

No authentication, no database. Pure filesystem + TOML parsing.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import tomli

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from apps.common.media_blocks import block_media_paths, block_media_pool, block_slot_key

GAMES_ROOT = Path(settings.BASE_DIR) / "games"


def _resolve_final_toml(game_dir: Path) -> Path | None:
    """Find a game's merged final TOML, whatever its phase number.

    Games are packaged to ``<n>_final_game.toml`` where n varies (older games
    use 6_, the newest 7_). Pick the highest *numeric* prefix so the newest merge
    wins — by integer value, not lexical order, so a future 10_ beats 7_. Names
    whose prefix isn't purely digits (e.g. ``backup_7_final_game.toml``) are
    ignored. Returns None if none exists.
    """
    phases_dir = game_dir / "toml_phases"
    if not phases_dir.is_dir():
        return None
    suffix = "_final_game.toml"
    best, best_n = None, -1
    for f in phases_dir.iterdir():
        if not f.name.endswith(suffix):
            continue
        prefix = f.name[: -len(suffix)]
        if not prefix.isdigit():  # excludes backup_7_, draft_, etc.
            continue
        n = int(prefix)
        if n > best_n:
            best_n, best = n, f
    return best


# =============================================================================
# Utilities
# =============================================================================

def _extract_flag_effects(canvas_data: dict) -> list[str]:
    """Extract all flag names set by any node's exit_block in this canvas."""
    flags = []
    for node in canvas_data.get("nodes", []):
        eb = node.get("exit_block", {})
        # Direct flagEffects on location-type exit
        config = eb.get("config", {})
        for fe in config.get("flagEffects", []):
            if "flag" in fe:
                flags.append(fe["flag"])
        # flagEffects inside choices
        for choice in eb.get("choices", []):
            for fe in choice.get("flagEffects", []):
                if "flag" in fe:
                    flags.append(fe["flag"])
    return list(dict.fromkeys(flags))  # dedupe preserving order


def _extract_choices(canvas_data: dict) -> list[dict]:
    """Extract choices from the first node's exit_block (conditional choice pattern)."""
    nodes = canvas_data.get("nodes", [])
    if not nodes:
        return []
    first_node = nodes[0]
    eb = first_node.get("exit_block", {})
    if eb.get("type") != "choices":
        return []
    choices = []
    for c in eb.get("choices", []):
        cond = c.get("conditions")
        choices.append({
            "text": c.get("text", ""),
            "conditions": cond.get("items", []) if cond else None,
            "conditions_logic": cond.get("logic", "AND") if cond else None,
            "effects": c.get("effects", []),
        })
    return choices


def _extract_all_node_choices(canvas_data: dict) -> list[dict]:
    """Extract choices from ALL nodes in a canvas (for story canvases with multi-node paths)."""
    all_choices = []
    for node in canvas_data.get("nodes", []):
        eb = node.get("exit_block", {})
        if eb.get("type") != "choices":
            continue
        for c in eb.get("choices", []):
            cond = c.get("conditions")
            if cond and cond.get("items"):
                all_choices.append({
                    "text": c.get("text", ""),
                    "node_id": node.get("id", ""),
                    "node_name": node.get("name", ""),
                    "conditions": cond.get("items", []),
                    "conditions_logic": cond.get("logic", "AND"),
                })
    return all_choices


def _extract_all_effects(canvas_data: dict) -> list[dict]:
    """Extract all trait effects from all nodes' exit_blocks in this canvas."""
    all_effects = []
    for node in canvas_data.get("nodes", []):
        eb = node.get("exit_block", {})
        config = eb.get("config", {})
        for eff in config.get("effects", []):
            if "trait" in eff:
                all_effects.append(eff)
        for choice in eb.get("choices", []):
            for eff in choice.get("effects", []):
                if "trait" in eff:
                    all_effects.append(eff)
    return all_effects


def _simplify_blocks(blocks: list[dict]) -> list[dict]:
    """Reduce block data to type + truncated text for the detail view."""
    simplified = []
    for b in blocks:
        btype = b.get("type", "")
        if btype == "paragraph":
            text = b.get("content", "")
            simplified.append({
                "type": "paragraph",
                "text": text[:120] + ("..." if len(text) > 120 else ""),
            })
        elif btype == "video":
            props = b.get("props", {})
            simplified.append({
                "type": "video",
                "file": props.get("file", ""),
                "description": props.get("description", ""),
            })
        elif btype == "image":
            props = b.get("props", {})
            simplified.append({
                "type": "image",
                "file": props.get("file", ""),
                "search_queries": props.get("search_queries", []),
            })
        elif btype == "dialog":
            props = b.get("props", {})
            text = b.get("content", "")
            simplified.append({
                "type": "dialog",
                "speaker": props.get("speaker", ""),
                "npcId": props.get("npcId", ""),
                "text": text[:120] + ("..." if len(text) > 120 else ""),
            })
        else:
            simplified.append({"type": btype})
    return simplified


def _simplify_exit_block(exit_block: dict, canvas_id: str) -> dict:
    """Process exit_block for detail view, stripping canvas prefix from nodeIds."""
    eb = dict(exit_block)
    if "choices" in eb:
        choices = []
        prefix = canvas_id + "."
        for c in eb["choices"]:
            choice = dict(c)
            node_id = choice.get("nodeId", "")
            if node_id.startswith(prefix):
                choice["nodeId"] = node_id[len(prefix):]
            choices.append(choice)
        eb["choices"] = choices
    return eb


def _process_canvas(canvas: dict) -> dict:
    """Process a raw TOML canvas into a simplified review structure."""
    trigger = canvas.get("trigger", {})
    conditions = trigger.get("conditions", {})
    schedules = trigger.get("schedules", [])

    schedule = None
    if schedules:
        s = schedules[0]
        schedule = {
            "start_time": s.get("start_time", ""),
            "end_time": s.get("end_time", ""),
        }

    is_repeatable = trigger.get("is_repeatable", False)

    result = {
        "id": canvas.get("id", ""),
        "name": canvas.get("name", ""),
        "description": canvas.get("description", ""),
        "is_repeatable": is_repeatable,
        "location": trigger.get("location", ""),
        "npc": trigger.get("npc", ""),
        "schedule": schedule,
        "priority": trigger.get("priority", 0),
        "max_triggers_per_day": trigger.get("max_triggers_per_day", None),
        "trigger_conditions": conditions.get("items", []) if conditions else [],
        "trigger_logic": conditions.get("logic", "AND") if conditions else "AND",
        "choices": _extract_choices(canvas),
        "flag_effects": _extract_flag_effects(canvas),
        "all_effects": _extract_all_effects(canvas),
        "node_count": len(canvas.get("nodes", [])),
    }

    # Node details for canvas detail view
    canvas_id = canvas.get("id", "")
    nodes_detail = []
    for node in canvas.get("nodes", []):
        nodes_detail.append({
            "id": node.get("id", ""),
            "name": node.get("name", ""),
            "blocks": _simplify_blocks(node.get("blocks", [])),
            "exit_block": _simplify_exit_block(node.get("exit_block", {}), canvas_id),
        })
    result["nodes"] = nodes_detail

    # For story canvases, also include conditional choices from deeper nodes
    if not is_repeatable:
        result["deep_choices"] = _extract_all_node_choices(canvas)

    return result


def _iter_media_blocks(blocks: list[dict]):
    """Yield every image/video block reachable in `blocks`, descending into the
    nested-block containers the game generator actually renders.

    A flat walk over `node["blocks"]` only sees media that are DIRECT children of a
    node. But the hottest content is always nested one level deeper:
      - sex-loop FINISHERS + ambient sex  → `group` blocks   (`block["blocks"]`)
      - OPENING / first-time sex          → `cascade` beats   (`props["beats"][*]["blocks"]`)
      - random-still pools                → `block_pool`      (`props["blocks"]`)
    The flat walk missed all of it, so those files never reached the missing-media
    list and shipped without art while the audit reported "0 missing". This mirrors
    v2.py `_convert_blocks_to_game_html`'s descent so the list matches the real build.
    """
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if (block.get("type") or "").strip() in ("image", "video"):
            yield block
        props = block.get("props") or {}
        # group (and any block carrying a direct child list)
        yield from _iter_media_blocks(block.get("blocks") or [])
        # block_pool — children under props.blocks
        yield from _iter_media_blocks(props.get("blocks") or [])
        # cascade — children under props.beats[*].blocks
        for beat in (props.get("beats") or []):
            if isinstance(beat, dict):
                yield from _iter_media_blocks(beat.get("blocks") or [])


def _extract_missing_media(data: dict, game_name: str) -> dict:
    """Extract all media references from TOML, split into found vs missing.

    Returns {"missing": [...], "found": [...]}.
    """
    missing = []
    found = []
    game_dir = GAMES_ROOT / game_name
    order_idx = 0

    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
    VIDEO_EXTS = {'.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv'}
    ALL_MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS

    def find_file(file_path: str) -> tuple:
        """Extension-agnostic file lookup mirroring _find_media_file().

        Returns (actual_filename, actual_ext, serve_path) or (None, None, None).
        serve_path is relative to game_dir for URL building.
        """
        from pathlib import Path as P
        base = P(file_path).stem          # e.g., "activity_visit_tom_kiss"
        parent = P(file_path).parent      # e.g., "videos/activities"

        # Candidate roots to search in
        candidate_roots = [
            game_dir / "output",
            game_dir,
        ]
        # videos/ is the media root — add it for non-videos/ paths
        if not file_path.startswith("videos/"):
            candidate_roots.append(game_dir / "videos")

        for root in candidate_roots:
            candidate_dir = root / parent
            if candidate_dir.is_dir():
                for f in candidate_dir.iterdir():
                    if f.is_file() and f.stem == base:
                        serve_path = str(f.relative_to(game_dir))
                        return (f.name, f.suffix.lower(), serve_path)
        return (None, None, None)

    def _natural_key(name: str):
        """Order clip_2 before clip_10 — plain lexical sort does the opposite."""
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]

    def find_pool(pool_dir: str) -> list:
        """Every media file currently inside a pool folder, in natural order.

        Returns [{file, actual_file, actual_type, serve_path}, ...] — empty when
        the folder is absent or has no media in it.

        Deliberately reads `videos/` and NOT `output/`, unlike find_file above:
        `output/` is wiped and regenerated by the packager, so listing a pool from
        there would show stale contents that vanish on the next build. The folder
        under `videos/` is the source of truth, and it is what the review UI edits.
        """
        from pathlib import Path as P
        rel = pool_dir.replace("\\", "/").strip().rstrip("/")
        root = game_dir / "videos"
        if rel.startswith("videos/"):
            rel = rel[len("videos/"):]
        candidate_dir = root / rel
        if not candidate_dir.is_dir():
            return []

        items = []
        for f in sorted(candidate_dir.iterdir(), key=lambda p: _natural_key(p.name)):
            # A dot-prefixed name is never a clip somebody selected: it is staging, an
            # editor swap file, or macOS AppleDouble (`._clip.gif` — a REAL media
            # suffix, so the suffix test alone lets it through). Listing one shifts
            # every caption and offers a partial file as pickable.
            if f.name.startswith("."):
                continue
            if not f.is_file() or f.suffix.lower() not in ALL_MEDIA_EXTS:
                continue
            items.append({
                "file": f"{rel}/{f.name}",
                "actual_file": f.name,
                "actual_type": "image" if f.suffix.lower() in IMAGE_EXTS else "video",
                "serve_path": str(f.relative_to(game_dir)),
            })
        return items

    # 1. Location images
    for loc in data.get("locations", []):
        image = loc.get("image", "")
        if not image:
            continue
        entry = {
            "file": image,
            "type": "location_image",
            "category": "Locations",
            "description": f"Navigation image for {loc.get('name', loc.get('id', ''))}",
            "search_queries": loc.get("image_search_queries", []),
            "canvas_id": "navigation",
            "order": order_idx,
        }
        order_idx += 1
        actual_name, actual_ext, serve_path = find_file(image)
        if actual_name is not None:
            entry["actual_file"] = actual_name
            entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
            entry["serve_path"] = serve_path
            found.append(entry)
        else:
            missing.append(entry)

    # 2. Canvas blocks (images and videos)
    for canvas in data.get("canvases", []):
        canvas_id = canvas.get("id", "")
        canvas_name = canvas.get("name", canvas_id)
        for node in canvas.get("nodes", []):
            # Recurse into nested containers (group / cascade / block_pool) — the
            # flat `node["blocks"]` walk was blind to finishers + opening sex.
            for block in _iter_media_blocks(node.get("blocks", [])):
                btype = block.get("type", "")
                props = block.get("props", {})

                # ── Folder pool: ONE row for the whole block ──────────────────
                # Keyed by `pool_dir`, never by the discovered filenames. Three
                # ledgers hang off this key — the options store, the review
                # verdicts and the options-page URL — so keying on contents would
                # re-key the shelf and orphan every verdict on each unselect.
                #
                # The row comes from the TOML and is merely POPULATED from disk:
                # an unstocked pool must still appear, or it vanishes from the
                # audit exactly like the bug apps/common/media_blocks.py fixed.
                pool_spec = block_media_pool(props)
                if pool_spec is not None:
                    pool_items = find_pool(pool_spec["dir"])
                    fl = pool_spec["dir"].lower()
                    if "activities" in fl:
                        cat = "Activities"
                    elif "story" in fl or "opening" in fl:
                        cat = "Story"
                    elif "locations" in fl:
                        cat = "Locations"
                    else:
                        cat = "Other"

                    entry = {
                        "file": pool_spec["dir"],   # the row's identity — never empty
                        # What the shelf and the verdict file under. Equals `file`
                        # unless the block authored an `id`, in which case the
                        # ledgers survive the path moving (pool conversion, retag).
                        "slot_key": block_slot_key(block),
                        "type": btype,
                        "category": cat,
                        "description": props.get("description", ""),
                        "search_queries": props.get("search_queries", []),
                        "canvas_id": canvas_id,
                        "canvas_name": canvas_name,
                        "order": order_idx,
                        "pool_dir": pool_spec["dir"],
                        "pool_target": pool_spec["target"],
                        "pool_count": len(pool_items),
                        "pool_items": pool_items,
                    }
                    order_idx += 1
                    if pool_items:
                        # It renders, so it is FOUND. Being under target is a
                        # softer signal (pool_count < pool_target) — hard-splitting
                        # on it would send find-media hunting a working pool.
                        entry["actual_file"] = pool_items[0]["actual_file"]
                        entry["actual_type"] = pool_items[0]["actual_type"]
                        entry["serve_path"] = pool_items[0]["serve_path"]
                        found.append(entry)
                    else:
                        missing.append(entry)
                    continue

                # A legacy `files = [...]` pool declares its paths, so each entry
                # gets its own row — they are separate files to hunt and install.
                for file_path in block_media_paths(props):

                    # Categorize
                    fl = file_path.lower()
                    if "activities" in fl:
                        cat = "Activities"
                    elif "story" in fl or "opening" in fl:
                        cat = "Story"
                    elif "locations" in fl:
                        cat = "Locations"
                    else:
                        cat = "Other"

                    entry = {
                        "file": file_path,
                        # A legacy `files = [...]` pool declares N paths, and each is
                        # its own slot — so the key is the path, not the block's id.
                        # Only a single-file block can inherit an authored id.
                        "slot_key": (
                            block_slot_key(block)
                            if len(block_media_paths(props)) == 1 else file_path
                        ),
                        "type": btype,
                        "category": cat,
                        "description": props.get("description", ""),
                        "search_queries": props.get("search_queries", []),
                        "canvas_id": canvas_id,
                        "canvas_name": canvas_name,
                        "order": order_idx,
                    }
                    order_idx += 1
                    actual_name, actual_ext, serve_path = find_file(file_path)
                    if actual_name is not None:
                        entry["actual_file"] = actual_name
                        entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
                        entry["serve_path"] = serve_path
                        found.append(entry)
                    else:
                        missing.append(entry)

    # 3. Clothing item images
    for item in data.get("clothing", []):
        image = item.get("image", "")
        if not image:
            continue
        entry = {
            "file": image,
            "type": "clothing_image",
            "category": "Clothing",
            "description": f"{item.get('name', item.get('id', ''))} ({item.get('slot', '')})",
            "search_queries": item.get("image_search_queries", []),
            "canvas_id": "wardrobe",
            "order": order_idx,
        }
        order_idx += 1
        actual_name, actual_ext, serve_path = find_file(image)
        if actual_name is not None:
            entry["actual_file"] = actual_name
            entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
            entry["serve_path"] = serve_path
            found.append(entry)
        else:
            missing.append(entry)

    # 4. Phone post images (Flaunt social feed)
    phone = data.get("phone", {})
    for post in phone.get("posts", []):
        image = post.get("image", "")
        if not image:
            continue
        poster = post.get("poster_name", post.get("id", ""))
        entry = {
            "file": image,
            "type": "social_post_image",
            "category": "Social Media",
            "description": f"{poster}: {post.get('caption', '')}",
            "search_queries": post.get("search_queries", []),
            "canvas_id": "phone",
            "order": order_idx,
        }
        order_idx += 1
        actual_name, actual_ext, serve_path = find_file(image)
        if actual_name is not None:
            entry["actual_file"] = actual_name
            entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
            entry["serve_path"] = serve_path
            found.append(entry)
        else:
            missing.append(entry)

    # 5. Phone profile photos (dating apps)
    for prof in phone.get("profiles", []):
        for photo in (prof.get("photos") or []):
            if not photo:
                continue
            entry = {
                "file": photo,
                "type": "dating_profile_photo",
                "category": "Social Media",
                "description": f"Dating profile photo for {prof.get('npc', prof.get('id', ''))}",
                "search_queries": prof.get("search_queries", []),
                "canvas_id": "phone",
                "order": order_idx,
            }
            order_idx += 1
            actual_name, actual_ext, serve_path = find_file(photo)
            if actual_name is not None:
                entry["actual_file"] = actual_name
                entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
                entry["serve_path"] = serve_path
                found.append(entry)
            else:
                missing.append(entry)

    # 6. Portraits — NPC faces, the player-portrait states, and any image-valued
    # customization option.
    #
    # These were invisible to this API for its whole life, so they never appeared in
    # the review page, the missing list, or the finder. They surfaced only as
    # "File not found" lines during packaging, which is why a new NPC's face kept
    # shipping absent and getting discovered late. 21 such assets in vesper alone.
    def _add_portrait(image, description, canvas_id):
        nonlocal order_idx
        if not image or not isinstance(image, str):
            return
        entry = {
            "file": image,
            "type": "portrait_image",
            "category": "Portraits",
            "description": description,
            # Portraits are UI chrome (a face in the sidebar), never a scene, so they
            # are always SFW regardless of how explicit the game is.
            "search_queries": [],
            "canvas_id": canvas_id,
            "order": order_idx,
        }
        order_idx += 1
        actual_name, actual_ext, serve_path = find_file(image)
        if actual_name is not None:
            entry["actual_file"] = actual_name
            entry["actual_type"] = "image" if actual_ext in IMAGE_EXTS else "video"
            entry["serve_path"] = serve_path
            found.append(entry)
        else:
            missing.append(entry)

    for npc in data.get("npcs", []) or []:
        name = npc.get("name") or npc.get("id") or ""
        _add_portrait(npc.get("portrait"), f"Portrait for {name}", "portraits")

    player_portrait = data.get("player_portrait") or {}
    if isinstance(player_portrait, dict):
        for key, value in player_portrait.items():
            if key.endswith("_image") and isinstance(value, str):
                state = key[: -len("_image")].replace("_", " ")
                _add_portrait(value, f"Player portrait — {state}", "portraits")
        for outfit in player_portrait.get("outfits", []) or []:
            if isinstance(outfit, dict):
                label = outfit.get("name") or outfit.get("id") or "outfit"
                _add_portrait(
                    outfit.get("image"), f"Player portrait — {label}", "portraits"
                )

    for field in (data.get("player", {}) or {}).get("customization_fields", []) or []:
        if not isinstance(field, dict) or field.get("type") != "image_select":
            continue
        label = field.get("label") or field.get("id") or "customization"
        for option in field.get("options", []) or []:
            if isinstance(option, dict):
                opt_name = option.get("label") or option.get("value") or ""
                _add_portrait(
                    option.get("image"), f"{label} — {opt_name}", "portraits"
                )

    # Every entry carries a `slot_key` — what its shelf and verdict file under.
    # Canvas media blocks set it above (an authored `id` when present); the other
    # five categories (locations, clothing, phone, dating, portraits) have no block
    # to tag, so their key IS the path. Defaulting here rather than at five call
    # sites means a new category can never ship without one.
    for entry in missing + found:
        if not entry.get("slot_key"):
            entry["slot_key"] = entry.get("file", "")

    return {"missing": missing, "found": found}


# =============================================================================
# Views
# =============================================================================

@require_GET
def list_games(request):
    """Return list of games that have a merged *_final_game.toml."""
    if not GAMES_ROOT.exists():
        return JsonResponse({"games": []})

    games = []
    for game_dir in sorted(GAMES_ROOT.iterdir()):
        if not game_dir.is_dir():
            continue
        toml_path = _resolve_final_toml(game_dir)
        if toml_path is not None:
            games.append({"name": game_dir.name, "toml_path": str(toml_path)})
    return JsonResponse({"games": games})


@require_GET
def load_game(request):
    """Parse a game's TOML and return structured JSON for the review panel."""
    game = request.GET.get("game", "")
    if not game:
        return JsonResponse({"error": "Missing game parameter"}, status=400)

    game_dir = GAMES_ROOT / game
    # Path traversal check (is_relative_to avoids the sibling-prefix bypass that a
    # bare startswith allows, e.g. ../games_secret).
    try:
        if not game_dir.resolve().is_relative_to(GAMES_ROOT.resolve()):
            return JsonResponse({"error": "Invalid path"}, status=400)
    except Exception:
        return JsonResponse({"error": "Invalid path"}, status=400)

    toml_path = _resolve_final_toml(game_dir)
    if toml_path is None or not toml_path.exists():
        return JsonResponse({"error": "TOML file not found"}, status=404)

    try:
        with open(toml_path, "rb") as f:
            data = tomli.load(f)
    except Exception as e:
        return JsonResponse({"error": f"Failed to parse TOML: {e}"}, status=500)

    # Extract project info
    project = data.get("project", {})

    # Extract player
    player_data = data.get("player", {})
    player = {
        "id": player_data.get("id", "player"),
        "name": player_data.get("name", "Player"),
        "traits": player_data.get("core_traits", {}),
        "flag_keys": player_data.get("flag_keys", []),
    }

    # Extract NPCs
    npcs = []
    for npc in data.get("npcs", []):
        npcs.append({
            "id": npc.get("id", ""),
            "name": npc.get("name", ""),
            "core_traits": npc.get("core_traits", {}),
        })

    # Extract locations
    locations = []
    for loc in data.get("locations", []):
        locations.append({
            "id": loc.get("id", ""),
            "name": loc.get("name", ""),
        })

    # Process canvases
    canvases = [_process_canvas(c) for c in data.get("canvases", [])]

    # Extract story arc
    story_arc = data.get("story_arc", {})

    # Extract missing media
    media_info = _extract_missing_media(data, game)

    return JsonResponse({
        "project": {
            "id": project.get("id", game),
            "title": project.get("title", game),
        },
        "player": player,
        "npcs": npcs,
        "locations": locations,
        "canvases": canvases,
        "story_arc": story_arc,
        "starting_canvas": data.get("starting_canvas", ""),
        "missing_media": media_info["missing"],
        "found_media": media_info["found"],
    })


@csrf_exempt
def canvas_review(request):
    """Read or update canvas review statuses (approved/review/disapproved)."""
    if request.method == "GET":
        game = request.GET.get("game", "")
        if not game:
            return JsonResponse({"error": "Missing game parameter"}, status=400)
        review_path = GAMES_ROOT / game / "canvas_review.json"
        try:
            resolved = review_path.resolve()
            if not str(resolved).startswith(str(GAMES_ROOT.resolve())):
                return JsonResponse({"error": "Invalid path"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid path"}, status=400)
        if review_path.exists():
            statuses = json.loads(review_path.read_text())
        else:
            statuses = {}
        return JsonResponse({"statuses": statuses})

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        game = body.get("game", "")
        canvas_id = body.get("canvas_id", "")
        status = body.get("status")
        notes = body.get("notes", "")
        if not game or not canvas_id:
            return JsonResponse({"error": "Missing game or canvas_id"}, status=400)
        review_path = GAMES_ROOT / game / "canvas_review.json"
        try:
            resolved = review_path.resolve()
            if not str(resolved).startswith(str(GAMES_ROOT.resolve())):
                return JsonResponse({"error": "Invalid path"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid path"}, status=400)
        if review_path.exists():
            statuses = json.loads(review_path.read_text())
        else:
            statuses = {}
        if status is None:
            statuses.pop(canvas_id, None)
        else:
            statuses[canvas_id] = {
                "status": status,
                "notes": notes,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        review_path.write_text(json.dumps(statuses, indent=2))
        return JsonResponse({"ok": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def media_review(request):
    """Read or update media review statuses (approved/disapproved)."""
    if request.method == "GET":
        game = request.GET.get("game", "")
        if not game:
            return JsonResponse({"error": "Missing game parameter"}, status=400)
        review_path = GAMES_ROOT / game / "media_review.json"
        try:
            resolved = review_path.resolve()
            if not str(resolved).startswith(str(GAMES_ROOT.resolve())):
                return JsonResponse({"error": "Invalid path"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid path"}, status=400)
        if review_path.exists():
            statuses = json.loads(review_path.read_text())
        else:
            statuses = {}
        return JsonResponse({"statuses": statuses})

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        game = body.get("game", "")
        file_path = body.get("file_path", "")
        status = body.get("status")
        notes = body.get("notes", "")
        if not game or not file_path:
            return JsonResponse({"error": "Missing game or file_path"}, status=400)
        review_path = GAMES_ROOT / game / "media_review.json"
        try:
            resolved = review_path.resolve()
            if not str(resolved).startswith(str(GAMES_ROOT.resolve())):
                return JsonResponse({"error": "Invalid path"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid path"}, status=400)
        if review_path.exists():
            statuses = json.loads(review_path.read_text())
        else:
            statuses = {}
        if status is None:
            statuses.pop(file_path, None)
        else:
            statuses[file_path] = {
                "status": status,
                "notes": notes,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        review_path.write_text(json.dumps(statuses, indent=2))
        return JsonResponse({"ok": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def media_download(request):
    """Download media file directly to game output directory."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    game = body.get("game", "")
    file_path = body.get("file_path", "")
    url = body.get("url", "")

    if not all([game, file_path, url]):
        return JsonResponse(
            {"success": False, "error": "Missing game, file_path, or url"},
            status=400,
        )

    # Path safety
    output_path = (GAMES_ROOT / game / "output" / file_path).resolve()
    if not str(output_path).startswith(str(GAMES_ROOT.resolve())):
        return JsonResponse({"success": False, "error": "Invalid path"}, status=400)

    # Create directories
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Download
    try:
        import requests as req

        headers = {"User-Agent": "Mozilla/5.0"}
        resp = req.get(url, timeout=60, headers=headers, stream=True)
        resp.raise_for_status()

        # Reject HTML responses
        ct = resp.headers.get("Content-Type", "")
        if "text/html" in ct:
            return JsonResponse(
                {"success": False, "error": "URL returned HTML instead of media"},
                status=400,
            )

        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)

        relative = str(output_path.relative_to(GAMES_ROOT))
        return JsonResponse({"success": True, "file_path": relative})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# =============================================================================
# HTML Page
# =============================================================================

def page(request):
    """Serve the game review HTML page."""
    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Game Review</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f0f; color: #e0e0e0; display: flex; height: 100vh; overflow: hidden; }

/* Sidebar - Trait Control Panel */
#sidebar { width: 280px; background: #1a1a1a; border-right: 1px solid #333; overflow-y: auto; flex-shrink: 0; padding: 16px; }
#sidebar h2 { font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
.back-link { font-size: 12px; color: #6b8afd; text-decoration: none; text-transform: none; letter-spacing: 0; }
.back-link:hover { color: #93aaff; }

/* Game selector */
.game-select { width: 100%; background: #222; border: 1px solid #444; color: #e0e0e0; padding: 8px 10px; border-radius: 6px; font-size: 13px; margin-bottom: 16px; }

/* Section headers */
.section-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin: 16px 0 8px; padding-bottom: 4px; border-bottom: 1px solid #2a2a2a; }

/* Trait sliders */
.trait-group { margin-bottom: 16px; }
.trait-row { margin-bottom: 10px; }
.trait-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.trait-name { font-size: 12px; color: #ccc; font-weight: 600; }
.trait-value { font-size: 12px; color: #6b8afd; font-family: monospace; min-width: 24px; text-align: right; }
.trait-slider { width: 100%; height: 4px; -webkit-appearance: none; appearance: none; background: #333; border-radius: 2px; outline: none; }
.trait-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 14px; background: #6b8afd; border-radius: 50%; cursor: pointer; }
.emotion-label { font-size: 10px; color: #888; font-style: italic; margin-top: 2px; }

/* Flag checkboxes */
.flag-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.flag-row input[type=checkbox] { accent-color: #6b8afd; }
.flag-row label { font-size: 12px; color: #aaa; cursor: pointer; }
.flag-row label:hover { color: #ccc; }
.flag-filter-btn { background: none; border: 1px solid transparent; color: #555; cursor: pointer; font-size: 10px; padding: 1px 4px; border-radius: 3px; margin-left: auto; flex-shrink: 0; }
.flag-filter-btn:hover { color: #818cf8; border-color: #818cf8; }
.flag-filter-btn.active { color: #818cf8; border-color: #818cf8; background: #6366f118; }
.flag-filter-chip { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; color: #818cf8; background: #6366f118; border: 1px solid #818cf8; padding: 4px 10px; border-radius: 10px; cursor: pointer; }
.flag-filter-chip:hover { background: #6366f130; }
.flag-filter-chip .chip-x { font-weight: 700; font-size: 13px; }

/* Preset buttons */
.presets { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.preset-btn { background: #2a2a2a; border: 1px solid #444; color: #aaa; padding: 4px 10px; border-radius: 4px; font-size: 11px; cursor: pointer; }
.preset-btn:hover { background: #333; color: #fff; }
.preset-btn.active { background: #6b8afd22; border-color: #6b8afd; color: #6b8afd; }

/* Main content */
#main { flex: 1; overflow-y: auto; padding: 24px 32px; }
#main h1 { font-size: 22px; margin-bottom: 4px; color: #fff; }
.subtitle { font-size: 13px; color: #666; margin-bottom: 24px; }

/* Chapter sections */
.chapter { margin-bottom: 20px; }
.chapter-header { display: flex; align-items: center; gap: 10px; cursor: pointer; padding: 10px 14px; background: #1a1a1a; border-radius: 8px; border-left: 3px solid #444; }
.chapter-header:hover { background: #222; }
.chapter-header.mood-hopeful { border-left-color: #22c55e; }
.chapter-header.mood-romantic { border-left-color: #ec4899; }
.chapter-header.mood-passionate { border-left-color: #ef4444; }
.chapter-header.mood-tense { border-left-color: #f59e0b; }
.chapter-header.mood-peaceful { border-left-color: #6366f1; }
.chapter-arrow { font-size: 10px; color: #666; transition: transform 0.2s; }
.chapter-arrow.open { transform: rotate(90deg); }
.chapter-name { font-size: 14px; font-weight: 600; color: #fff; }
.chapter-mood { font-size: 11px; color: #888; background: #222; padding: 2px 8px; border-radius: 10px; }
.chapter-body { display: none; padding: 8px 0 8px 20px; }
.chapter-body.open { display: block; }

/* Story nodes */
.story-node { display: flex; align-items: flex-start; gap: 10px; padding: 8px 12px; margin: 4px 0; border-radius: 6px; border-left: 2px solid transparent; }
.story-node.unlocked { background: #162016; border-left-color: #22c55e; }
.story-node.locked { background: #201616; border-left-color: #ef4444; opacity: 0.7; }
.node-icon { font-size: 14px; flex-shrink: 0; margin-top: 1px; }
.node-content { flex: 1; min-width: 0; }
.node-name { font-size: 13px; font-weight: 600; color: #e0e0e0; }
.node-meta { font-size: 11px; color: #888; margin-top: 2px; }
.node-conditions { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.cond-pill { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #2a2a2a; color: #aaa; white-space: nowrap; }
.cond-pill.met { background: #22c55e22; color: #4ade80; }
.cond-pill.unmet { background: #ef444422; color: #f87171; }
.cond-pill.unknown { background: #333; color: #999; border: 1px solid #555; }
.daily-limit-badge { font-size: 10px; background: #3b3b1a; color: #fbbf24; padding: 1px 6px; border-radius: 8px; margin-left: 6px; }
.logic-sep { font-size: 9px; color: #666; font-weight: 600; text-transform: uppercase; vertical-align: middle; margin: 0 2px; }
.flag-set-pill { font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #6366f122; color: #818cf8; white-space: nowrap; }
.sim-btn { background: none; border: 1px solid #444; color: #888; cursor: pointer; font-size: 9px; padding: 1px 5px; border-radius: 3px; margin-left: 6px; vertical-align: middle; }
.sim-btn:hover { background: #333; color: #6b8afd; border-color: #6b8afd; }

/* Groups */
.group-box { margin: 8px 0; padding: 8px 12px; background: #1a1a2a; border: 1px solid #333; border-radius: 6px; }
.group-header { font-size: 12px; color: #818cf8; font-weight: 600; margin-bottom: 4px; }
.group-desc { font-size: 11px; color: #888; margin-bottom: 6px; }

/* Divider */
.section-divider { border: none; border-top: 1px solid #2a2a2a; margin: 28px 0; }

/* Activity cards */
.activities-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 12px; }
.activity-card { background: #1a1a1a; border-radius: 8px; overflow: hidden; border: 1px solid #2a2a2a; }
.activity-header { padding: 10px 14px; background: #222; border-bottom: 1px solid #2a2a2a; }
.activity-name { font-size: 14px; font-weight: 600; color: #fff; }
.activity-meta { font-size: 11px; color: #888; margin-top: 2px; display: flex; gap: 8px; }
.activity-meta span { display: inline-flex; align-items: center; gap: 3px; }
.activity-body { padding: 10px 14px; }
.activity-trigger { font-size: 11px; color: #888; margin-bottom: 8px; }
.choice-row { display: flex; align-items: flex-start; gap: 8px; padding: 5px 0; border-bottom: 1px solid #1f1f1f; }
.choice-row:last-child { border-bottom: none; }
.choice-icon { font-size: 12px; flex-shrink: 0; margin-top: 2px; }
.choice-text { font-size: 12px; color: #ccc; flex: 1; }
.choice-conds { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 2px; }

/* Loading / empty */
.loading { color: #666; padding: 40px; text-align: center; }

/* Stats bar */
.stats-bar { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
.stat-item { background: #1a1a1a; padding: 8px 14px; border-radius: 6px; font-size: 12px; color: #aaa; }
.stat-item strong { color: #fff; }

/* ─── Missing Media View ─── */
.mm-section { margin-bottom: 24px; }
.mm-section-header { font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #2a2a2a; display: flex; align-items: center; gap: 8px; }
.mm-section-count { font-size: 11px; color: #888; font-weight: 400; }
.mm-item { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; }
.mm-item-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.mm-type-badge { font-size: 9px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0; }
.mm-type-badge.image { background: #3b82f622; color: #60a5fa; }
.mm-type-badge.video { background: #a855f722; color: #c084fc; }
.mm-type-badge.location_image { background: #22c55e22; color: #4ade80; }
.mm-file-path { font-size: 12px; color: #8af; font-family: monospace; word-break: break-all; }
.mm-canvas-tag { font-size: 10px; color: #888; margin-left: auto; flex-shrink: 0; }
.mm-description { font-size: 11px; color: #999; margin-bottom: 8px; font-style: italic; }
.mm-search-row { display: flex; flex-wrap: wrap; gap: 6px; }
.mm-search-btn { display: inline-block; font-size: 11px; color: #fff; background: #3b82f6; padding: 4px 12px; border-radius: 6px; text-decoration: none; transition: background 0.15s; white-space: nowrap; max-width: 100%; overflow: hidden; text-overflow: ellipsis; }
.mm-search-btn:hover { background: #2563eb; color: #fff; }
.mm-summary-bar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.mm-summary-item { font-size: 12px; color: #aaa; background: #1a1a1a; padding: 6px 12px; border-radius: 6px; }
.mm-summary-item strong { color: #fff; }
.mm-found { opacity: 0.4; border-color: #22c55e44; }
.mm-found .mm-file-path { color: #4ade80; }
.mm-actual-file { color: #4ade80; font-size: 11px; margin-left: 8px; }
.mm-type-switch { color: #facc15; font-size: 11px; margin-left: 8px; font-style: italic; }
.mm-find-btn { display: inline-block; font-size: 11px; color: #fff; background: #22c55e; padding: 4px 12px; border-radius: 6px; text-decoration: none; transition: background 0.15s; margin-left: auto; flex-shrink: 0; }
.mm-find-btn:hover { background: #16a34a; color: #fff; }

/* ─── Media Review View ─── */
.mr-summary-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; align-items: center; }
.mr-filter-btn { font-size: 12px; color: #aaa; background: #1a1a1a; padding: 6px 12px; border-radius: 6px; cursor: pointer; border: 1px solid transparent; transition: all 0.15s; }
.mr-filter-btn:hover { background: #222; color: #ccc; }
.mr-filter-btn strong { color: #fff; }
.mr-filter-btn.active { border-color: #6b8afd; color: #fff; }
.mr-filter-btn.active.f-approved { border-color: #4ade80; color: #4ade80; }
.mr-filter-btn.active.f-approved strong { color: #4ade80; }
.mr-filter-btn.active.f-disapproved { border-color: #f87171; color: #f87171; }
.mr-filter-btn.active.f-disapproved strong { color: #f87171; }
.mr-filter-btn.active.f-missing { border-color: #facc15; color: #facc15; background: #f59e0b15; }
.mr-filter-btn.active.f-missing strong { color: #facc15; }
.mr-sep { width: 1px; height: 24px; background: #333; margin: 0 4px; }
.mr-section { margin-bottom: 16px; }
.mr-section[open] > .mr-section-header { margin-bottom: 8px; }
.mr-section-header { font-size: 14px; font-weight: 600; color: #fff; cursor: pointer; padding: 10px 14px; background: #1a1a1a; border-radius: 8px; border-left: 3px solid #6b8afd; list-style: none; display: flex; align-items: center; gap: 8px; }
.mr-section-header::-webkit-details-marker { display: none; }
.mr-section-header:hover { background: #222; }
.mr-section-count { font-size: 11px; color: #888; font-weight: 400; }
.mr-section-reviewed { font-size: 11px; color: #4ade80; font-weight: 400; margin-left: auto; }
.mr-section-arrow { font-size: 10px; color: #666; transition: transform 0.15s; margin-right: 4px; }
.mr-section[open] .mr-section-arrow { transform: rotate(90deg); }
.mr-items-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 12px; padding: 4px 0; }
.mr-item { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; overflow: hidden; transition: border-color 0.15s; }
.mr-item.mr-status-approved { border-color: #22c55e55; }
.mr-item.mr-status-disapproved { border-color: #ef444455; }
.mr-preview { width: 100%; max-height: 200px; object-fit: contain; background: #111; display: block; }
.mr-preview-img { width: 100%; max-height: 200px; object-fit: contain; background: #111; display: block; cursor: pointer; }
.mr-item-body { padding: 10px 12px; }
.mr-item-header { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap; }
.mr-item-file { font-size: 11px; color: #8af; font-family: monospace; word-break: break-all; margin-bottom: 6px; }
.mr-item-desc { font-size: 11px; color: #999; font-style: italic; margin-bottom: 8px; }
.mr-controls { display: flex; gap: 6px; margin-bottom: 8px; align-items: center; }
.mr-btn { background: none; border: 1px solid #333; color: #888; padding: 4px 12px; border-radius: 5px; font-size: 11px; cursor: pointer; transition: all 0.15s; }
.mr-btn:hover { border-color: #555; color: #ccc; }
.mr-btn.active-approved { border-color: #4ade80; color: #4ade80; background: #22c55e18; }
.mr-btn.active-disapproved { border-color: #f87171; color: #f87171; background: #ef444418; }
.mr-status-label { font-size: 10px; margin-left: auto; font-weight: 600; }
.mr-status-label.sl-approved { color: #4ade80; }
.mr-status-label.sl-disapproved { color: #f87171; }
.mr-notes { width: 100%; box-sizing: border-box; background: #111; border: 1px solid #333; color: #ccc; border-radius: 5px; padding: 6px 8px; font-size: 11px; font-family: inherit; resize: vertical; min-height: 36px; }
.mr-notes:focus { border-color: #6b8afd; outline: none; }
.mr-notes::placeholder { color: #555; }

/* Media grouping sub-toggle */
.mr-groupby-bar { display: flex; gap: 6px; align-items: center; margin-bottom: 16px; }
.mr-groupby-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px; }
.mr-groupby-btn { font-size: 11px; color: #888; background: #1a1a1a; padding: 4px 12px; border-radius: 4px; cursor: pointer; border: 1px solid transparent; }
.mr-groupby-btn:hover { background: #222; color: #ccc; }
.mr-groupby-btn.active { border-color: #6b8afd; color: #6b8afd; background: #6b8afd12; }
.mr-tier-label { font-size: 12px; color: #aaa; font-style: italic; }

/* ─── Flowchart View ─── */
.fc-container { max-width: 900px; margin: 0 auto; position: relative; padding-left: 8px; }
.fc-container::before { content: ''; position: absolute; left: 32px; top: 0; bottom: 0; width: 2px; background: #333; }
.fc-tier { position: relative; padding: 0 0 28px 64px; }
.fc-tier:last-child { padding-bottom: 0; }
.fc-tier::before { content: ''; position: absolute; left: 25px; top: 8px; width: 16px; height: 16px; border-radius: 50%; background: #333; border: 2px solid #555; z-index: 1; }
.fc-tier.unlocked::before { background: #22c55e; border-color: #4ade80; }
.fc-tier.locked::before { background: #ef4444; border-color: #f87171; }
.fc-tier-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.fc-story { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; border-left: 3px solid #6366f1; }
.fc-story.unlocked { border-left-color: #22c55e; background: #162016; }
.fc-story.locked { border-left-color: #ef4444; background: #201616; opacity: 0.7; }
.fc-story-name { font-size: 14px; font-weight: 600; color: #fff; }
.fc-story-chapter { font-size: 11px; color: #888; margin-left: 8px; }
.fc-story-meta { font-size: 11px; color: #888; margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
.fc-story-flags { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
.fc-schedule { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: #2a2a2a; border: 1px solid #2a2a2a; border-radius: 6px; overflow: hidden; margin-top: 10px; }
.fc-time-col { background: #141414; padding: 8px; min-height: 60px; display: flex; flex-direction: column; gap: 6px; }
.fc-time-label { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; padding-bottom: 4px; border-bottom: 1px solid #2a2a2a; }
.fc-act-card { background: #1a1a2a; border: 1px solid #2a2a3a; border-radius: 5px; padding: 6px 10px; }
.fc-act-card.locked { opacity: 0.5; }
.fc-act-card.fc-act-new { border-left: 2px solid #6b8afd; }
.fc-act-new-badge { font-size: 8px; color: #6b8afd; font-weight: 700; letter-spacing: 0.5px; margin-left: 6px; }
.fc-act-name { font-size: 11px; font-weight: 600; color: #ccc; }
.fc-act-loc { font-size: 10px; color: #888; margin-top: 1px; }
.fc-act-effects { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 3px; }
.fc-effect-pill { font-size: 9px; padding: 1px 5px; border-radius: 8px; background: #22c55e22; color: #4ade80; white-space: nowrap; }
.fc-act-conds { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 3px; }
.fc-empty-slot { font-size: 10px; color: #444; font-style: italic; }

/* ─── NPC Sections ─── */
.npc-section { margin-bottom: 20px; }
.npc-header { display: flex; align-items: center; gap: 10px; cursor: pointer; padding: 12px 16px; background: #1a1a1a; border-radius: 8px; border-left: 4px solid #444; transition: background 0.15s; }
.npc-header:hover { background: #222; }
.npc-header-name { font-size: 15px; font-weight: 700; color: #fff; }
.npc-header-count { font-size: 11px; color: #888; background: #222; padding: 2px 10px; border-radius: 10px; margin-left: auto; }
.npc-arrow { font-size: 10px; color: #666; transition: transform 0.2s; }
.npc-arrow.open { transform: rotate(90deg); }
.npc-body { display: none; padding: 8px 0 8px 12px; }
.npc-body.open { display: block; }
.npc-header-general { border-left-color: #666; }
.npc-header-general .npc-header-name { color: #aaa; }
.npc-activities-label { font-size: 13px; font-weight: 600; margin: 16px 0 8px; padding-left: 10px; border-left: 3px solid #666; }
.fc-npc-section { margin-bottom: 32px; }
.fc-npc-label { font-size: 15px; font-weight: 700; color: #fff; padding: 8px 14px; border-left: 4px solid #6b8afd; background: #1a1a1a; border-radius: 0 8px 8px 0; margin-bottom: 12px; }

/* ─── Canvas Detail View ─── */
.canvas-link { cursor: pointer; text-decoration: underline; text-decoration-color: #444; text-underline-offset: 2px; }
.canvas-link:hover { text-decoration-color: #6b8afd; color: #6b8afd; }
.cd-back-btn { background: none; border: 1px solid #444; color: #aaa; padding: 6px 14px; border-radius: 6px; font-size: 12px; cursor: pointer; margin-bottom: 16px; }
.cd-back-btn:hover { background: #222; color: #fff; border-color: #6b8afd; }
.cd-canvas-header { background: #1a1a1a; border-radius: 8px; padding: 16px; margin-bottom: 20px; border: 1px solid #2a2a2a; }
.cd-canvas-name { font-size: 18px; font-weight: 700; color: #fff; }
.cd-canvas-desc { font-size: 12px; color: #888; margin-top: 4px; }
.cd-canvas-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.cd-meta-tag { font-size: 11px; color: #aaa; background: #222; padding: 3px 10px; border-radius: 10px; }
.cd-node { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; margin-bottom: 12px; overflow: hidden; }
.cd-node.cd-entry { border-left: 3px solid #6b8afd; }
.cd-node.cd-child { margin-left: 32px; border-left: 3px solid #333; }
.cd-node-header { display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: #222; border-bottom: 1px solid #2a2a2a; }
.cd-node-name { font-size: 14px; font-weight: 600; color: #fff; }
.cd-color-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.cd-blocks { padding: 10px 14px; border-bottom: 1px solid #1f1f1f; }
.cd-block-item { font-size: 11px; color: #999; padding: 2px 0; display: flex; gap: 6px; align-items: flex-start; }
.cd-block-icon { flex-shrink: 0; font-size: 12px; width: 16px; text-align: center; }
.cd-block-text { flex: 1; line-height: 1.4; }
.cd-media-row { display: flex; flex-wrap: wrap; gap: 8px; padding: 6px 0; }
.cd-thumb-wrap { position: relative; flex-shrink: 0; }
.cd-thumb { width: 220px; height: auto; border-radius: 6px; border: 1px solid #333; background: #111; transition: border-color 0.15s; }
.cd-thumb:hover { border-color: #6b8afd; }
.cd-thumb-desc { font-size: 10px; color: #888; margin-top: 2px; max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Pool preview — a folder of clips the game cycles one per visit. Tiles are
   smaller than .cd-thumb's 220px so a 4-clip set reads as one row. */
.mr-pool { padding: 6px 0; }
.mr-pool-head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.mr-pool-count { font-size: 11px; font-weight: 600; color: #4ade80; background: #4ade8018; border: 1px solid #4ade8040; border-radius: 4px; padding: 1px 7px; }
.mr-pool-count.mr-pool-short { color: #fbbf24; background: #fbbf2418; border-color: #fbbf2440; }
.mr-pool-count.mr-pool-empty { color: #f87171; background: #f8717118; border-color: #f8717140; }
.mr-pool-dir { font-size: 11px; color: #666; font-family: ui-monospace, monospace; }
.mr-pool-none { font-size: 11px; color: #666; font-style: italic; padding: 10px 0; }
.mr-pool .cd-thumb { width: 150px; }
.mr-pool .cd-thumb-desc { max-width: 150px; }
.cd-noaud-btn { font-size: 9px; background: none; border: 1px solid #444; color: #888; padding: 2px 6px; border-radius: 4px; cursor: pointer; margin-top: 3px; }
.cd-noaud-btn:hover { border-color: #f87171; color: #f87171; }
.cd-noaud-btn.done { border-color: #4ade80; color: #4ade80; cursor: default; }
.cd-exit { padding: 10px 14px; }
.cd-exit-label { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.cd-choice { display: flex; align-items: flex-start; gap: 8px; padding: 6px 8px; margin-bottom: 4px; border-radius: 6px; background: #161616; }
.cd-choice:last-child { margin-bottom: 0; }
.cd-choice-text { font-size: 12px; color: #ccc; }
.cd-choice-target { font-size: 10px; color: #888; margin-top: 2px; }
.cd-choice-meta { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.cd-exit-badge { font-size: 9px; font-weight: 700; color: #fb923c; background: #fb923c22; padding: 2px 6px; border-radius: 4px; letter-spacing: 0.5px; flex-shrink: 0; margin-top: 2px; }
.cd-time-pill { font-size: 9px; color: #888; background: #222; padding: 2px 6px; border-radius: 8px; }
.cd-effect-pill { font-size: 9px; padding: 2px 6px; border-radius: 8px; background: #22c55e22; color: #4ade80; white-space: nowrap; }
.cd-loc-exit { padding: 8px; background: #161616; border-radius: 6px; }
.cd-loc-exit-name { font-size: 12px; color: #ccc; }
.cd-loc-exit-meta { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }

/* ─── Review Status ─── */
.rv-badge { font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: 600; margin-left: 8px; white-space: nowrap; }
.rv-approved { background: #22c55e22; color: #4ade80; }
.rv-review { background: #f59e0b22; color: #fbbf24; }
.rv-disapproved { background: #ef444422; color: #f87171; }
.rv-controls { display: flex; gap: 8px; margin-bottom: 16px; align-items: center; }
.rv-btn { background: none; border: 1px solid #333; color: #888; padding: 6px 14px; border-radius: 6px; font-size: 12px; cursor: pointer; transition: all 0.15s; }
.rv-btn:hover { border-color: #555; color: #ccc; }
.rv-btn.active-approved { border-color: #4ade80; color: #4ade80; background: #22c55e18; }
.rv-btn.active-review { border-color: #fbbf24; color: #fbbf24; background: #f59e0b18; }
.rv-btn.active-disapproved { border-color: #f87171; color: #f87171; background: #ef444418; }
.rv-notes { width: 100%; background: #1a1a1a; border: 1px solid #333; color: #ccc; border-radius: 6px; padding: 8px; font-size: 12px; font-family: inherit; resize: vertical; min-height: 60px; margin-bottom: 16px; display: none; }
.rv-notes.visible { display: block; }
.rv-notes:focus { border-color: #fbbf24; outline: none; }
.rv-filter-btn { cursor: pointer; transition: all 0.15s; }
.rv-filter-btn:hover { background: #222; }
.rv-filter-btn.active { border: 1px solid; }
.rv-filter-btn.active.rv-approved { border-color: #4ade80; color: #4ade80; background: #22c55e15; }
.rv-filter-btn.active.rv-approved strong { color: #4ade80; }
.rv-filter-btn.active.rv-review { border-color: #fbbf24; color: #fbbf24; background: #f59e0b15; }
.rv-filter-btn.active.rv-review strong { color: #fbbf24; }
.rv-filter-btn.active.rv-disapproved { border-color: #f87171; color: #f87171; background: #ef444415; }
.rv-filter-btn.active.rv-disapproved strong { color: #f87171; }
</style>
</head>
<body>

<div id="sidebar">
  <h2>Game Review <a href="/api/v1/dev/video-browser/" class="back-link">Videos</a></h2>
  <select class="game-select" id="game-select" onchange="loadGame(this.value)">
    <option value="">Select a game...</option>
  </select>
  <div id="controls"></div>
</div>

<div id="main">
  <div class="loading">Select a game to review</div>
</div>

<script>
const API = '/api/v1/dev/game-review';
let DATA = null;
let TRAITS = {};   // { npc_angela: { love: 0, trust: 0 }, player: { money: 50 } }
let FLAGS = {};    // { game_started: false, kiss_unlocked: false, ... }
let VIEW_MODE = 'list';  // 'list' or 'flowchart'
let DETAIL_CANVAS_ID = null;  // when set, shows canvas detail view
let REVIEW = {};  // { canvas_id: { status, notes, updated_at } }
let REVIEW_FILTER = null;  // null=all, 'approved', 'review', 'disapproved', 'unmarked'
let FLAG_FILTER = null;    // null=no filter, 'flag_name'=show only canvases that set this flag
let MEDIA_REVIEW = {};     // { "videos/path.mp4": { status, notes, updated_at } }
let MEDIA_FILTER = null;   // null | 'approved' | 'disapproved' | 'unreviewed' | 'missing'
let MEDIA_GROUP_BY = 'canvas';  // 'canvas' | 'tier'
const NODE_COLORS = ['#6b8afd', '#4ade80', '#fb923c', '#f472b6', '#22d3ee', '#facc15', '#a78bfa', '#f87171', '#34d399', '#e879f9'];

// ─── URL Params ────────────────────────────────────
function readUrlParams() {
  const p = new URLSearchParams(window.location.search);
  return {
    game: p.get('game') || '',
    view: p.get('view') || 'list',
    canvas: p.get('canvas') || null,
    filter: p.get('filter') || null,
    flag: p.get('flag') || null,
    mfilter: p.get('mfilter') || null,
    mgroupby: p.get('mgroupby') || 'canvas',
  };
}

function syncUrlParams() {
  const p = new URLSearchParams();
  const sel = document.getElementById('game-select');
  if (sel && sel.value) p.set('game', sel.value);
  if (VIEW_MODE && VIEW_MODE !== 'list') p.set('view', VIEW_MODE);
  if (DETAIL_CANVAS_ID) p.set('canvas', DETAIL_CANVAS_ID);
  if (REVIEW_FILTER) p.set('filter', REVIEW_FILTER);
  if (FLAG_FILTER) p.set('flag', FLAG_FILTER);
  if (MEDIA_FILTER) p.set('mfilter', MEDIA_FILTER);
  if (MEDIA_GROUP_BY && MEDIA_GROUP_BY !== 'canvas') p.set('mgroupby', MEDIA_GROUP_BY);
  const qs = p.toString();
  history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : ''));
}

// ─── Init ──────────────────────────────────────────
async function init() {
  const urlState = readUrlParams();

  const res = await fetch(API + '/games');
  const data = await res.json();
  const sel = document.getElementById('game-select');
  data.games.forEach(g => {
    const opt = document.createElement('option');
    opt.value = g.name;
    opt.textContent = g.name;
    sel.appendChild(opt);
  });

  // Apply non-game state from URL
  if (['list', 'flowchart', 'media'].includes(urlState.view)) VIEW_MODE = urlState.view;
  if (['approved', 'review', 'disapproved', 'unmarked'].includes(urlState.filter)) REVIEW_FILTER = urlState.filter;
  if (urlState.flag) FLAG_FILTER = urlState.flag;
  if (['approved', 'disapproved', 'unreviewed', 'missing'].includes(urlState.mfilter)) MEDIA_FILTER = urlState.mfilter;
  if (['canvas', 'tier'].includes(urlState.mgroupby)) MEDIA_GROUP_BY = urlState.mgroupby;

  // Determine which game to load
  const gameToLoad = urlState.game || (data.games.length === 1 ? data.games[0].name : '');
  if (gameToLoad && data.games.some(g => g.name === gameToLoad)) {
    sel.value = gameToLoad;
    await loadGame(gameToLoad);
    // Deferred: apply canvas detail after game data is loaded
    if (urlState.canvas && DATA && DATA.canvases.some(c => c.id === urlState.canvas)) {
      DETAIL_CANVAS_ID = urlState.canvas;
      renderMain();
    }
  }

  syncUrlParams();
}

async function loadGame(name) {
  if (!name) return;
  document.getElementById('main').innerHTML = '<div class="loading">Loading...</div>';
  const res = await fetch(API + '/load?game=' + encodeURIComponent(name));
  DATA = await res.json();
  if (DATA.error) {
    document.getElementById('main').innerHTML = '<div class="loading">Error: ' + esc(DATA.error) + '</div>';
    return;
  }
  // Load review statuses
  try {
    const revRes = await fetch(API + '/canvas-review/?game=' + encodeURIComponent(name));
    const revData = await revRes.json();
    REVIEW = revData.statuses || {};
  } catch(e) { REVIEW = {}; }
  try {
    const mrRes = await fetch(API + '/media-review/?game=' + encodeURIComponent(name));
    const mrData = await mrRes.json();
    MEDIA_REVIEW = mrData.statuses || {};
  } catch(e) { MEDIA_REVIEW = {}; }
  initTraitsAndFlags();
  renderControls();
  renderMain();
  syncUrlParams();
}

function initTraitsAndFlags() {
  TRAITS = {};
  FLAGS = {};
  // Player traits
  TRAITS.player = {};
  const pt = DATA.player.traits || {};
  Object.keys(pt).forEach(k => { TRAITS.player[k] = pt[k]; });
  // NPC traits (start at 0)
  DATA.npcs.forEach(npc => {
    TRAITS[npc.id] = {};
    Object.keys(npc.core_traits || {}).forEach(k => {
      TRAITS[npc.id][k] = 0;
    });
  });
  // Flags (all false)
  (DATA.player.flag_keys || []).forEach(f => { FLAGS[f] = false; });
}

// ─── Controls ──────────────────────────────────────
function renderControls() {
  let html = '';
  // NPC traits
  DATA.npcs.forEach(npc => {
    html += '<div class="section-label">' + esc(npc.name) + ' Traits</div>';
    html += '<div class="trait-group">';
    Object.keys(npc.core_traits || {}).forEach(trait => {
      const val = TRAITS[npc.id][trait];
      const emo = getEmotionLabel(trait, val);
      html += '<div class="trait-row">' +
        '<div class="trait-header"><span class="trait-name">' + esc(trait) + '</span><span class="trait-value" id="tv-' + esc(npc.id) + '-' + esc(trait) + '">' + val + '</span></div>' +
        '<input type="range" class="trait-slider" min="0" max="50" value="' + val + '" ' +
        'oninput="updateTrait(\'' + esc(npc.id) + '\',\'' + esc(trait) + '\',this.value)">' +
        '<div class="emotion-label" id="emo-' + esc(npc.id) + '-' + esc(trait) + '">' + esc(emo) + '</div>' +
        '</div>';
    });
    html += '</div>';
  });
  // Player traits
  const playerTraits = Object.keys(DATA.player.traits || {});
  if (playerTraits.length > 0) {
    html += '<div class="section-label">Player Traits</div>';
    html += '<div class="trait-group">';
    playerTraits.forEach(trait => {
      const val = TRAITS.player[trait];
      html += '<div class="trait-row">' +
        '<div class="trait-header"><span class="trait-name">' + esc(trait) + '</span><span class="trait-value" id="tv-player-' + esc(trait) + '">' + val + '</span></div>' +
        '<input type="range" class="trait-slider" min="0" max="100" value="' + val + '" ' +
        'oninput="updateTrait(\'player\',\'' + esc(trait) + '\',this.value)">' +
        '</div>';
    });
    html += '</div>';
  }
  // Flags
  html += '<div class="section-label">Player Flags</div>';
  (DATA.player.flag_keys || []).forEach(flag => {
    const isActive = FLAG_FILTER === flag;
    html += '<div class="flag-row">' +
      '<input type="checkbox" id="flag-' + esc(flag) + '" ' + (FLAGS[flag] ? 'checked' : '') +
      ' onchange="updateFlag(\'' + esc(flag) + '\',this.checked)">' +
      '<label for="flag-' + esc(flag) + '">' + esc(flag) + '</label>' +
      '<button class="flag-filter-btn' + (isActive ? ' active' : '') + '" onclick="toggleFlagFilter(\'' + esc(flag) + '\')" title="Filter canvases that set this flag">&#9907;</button>' +
      '</div>';
  });
  // View mode toggle
  html += '<div class="section-label">View</div>';
  html += '<div class="presets">';
  html += '<button class="preset-btn ' + (VIEW_MODE === 'list' ? 'active' : '') + '" onclick="setViewMode(\'list\')">List</button>';
  html += '<button class="preset-btn ' + (VIEW_MODE === 'flowchart' ? 'active' : '') + '" onclick="setViewMode(\'flowchart\')">Flowchart</button>';
  html += '<button class="preset-btn ' + (VIEW_MODE === 'media' ? 'active' : '') + '" onclick="setViewMode(\'media\')">Media (' + ((DATA && DATA.missing_media) ? DATA.missing_media.length : 0) + ')</button>';
  html += '</div>';
  // Reset button
  html += '<div class="section-label">Controls</div>';
  html += '<button class="preset-btn" onclick="resetTraits()">Reset Traits</button>';
  document.getElementById('controls').innerHTML = html;
}

function updateTrait(subject, trait, value) {
  value = parseInt(value);
  TRAITS[subject][trait] = value;
  const tvEl = document.getElementById('tv-' + subject + '-' + trait);
  if (tvEl) tvEl.textContent = value;
  const emoEl = document.getElementById('emo-' + subject + '-' + trait);
  if (emoEl) emoEl.textContent = getEmotionLabel(trait, value);
  renderMain();
}

function updateFlag(flag, checked) {
  FLAGS[flag] = checked;
  renderMain();
}

function resetTraits() {
  FLAG_FILTER = null;
  initTraitsAndFlags();
  renderControls();
  renderMain();
  syncUrlParams();
}

function setViewMode(mode) {
  DETAIL_CANVAS_ID = null;
  REVIEW_FILTER = null;
  FLAG_FILTER = null;
  VIEW_MODE = mode;
  renderControls();
  renderMain();
  syncUrlParams();
}

function simulateToNode(targetNodeId) {
  // Reset to starting state
  DATA.npcs.forEach(npc => {
    Object.keys(TRAITS[npc.id] || {}).forEach(t => { TRAITS[npc.id][t] = 0; });
  });
  const pt = DATA.player.traits || {};
  TRAITS.player = {};
  Object.keys(pt).forEach(k => { TRAITS.player[k] = pt[k]; });
  Object.keys(FLAGS).forEach(f => { FLAGS[f] = false; });

  // Build canvas lookup
  const canvasMap = {};
  DATA.canvases.forEach(c => { canvasMap[c.id] = c; });

  // Walk story arc nodes in chapter order until we reach the target
  const chapters = (DATA.story_arc.chapters || []).slice().sort((a, b) => a.order - b.order);
  const allNodes = DATA.story_arc.nodes || [];
  let found = false;

  for (const ch of chapters) {
    const chNodes = allNodes.filter(n => n.chapter === ch.id);
    for (const node of chNodes) {
      const canvas = canvasMap[node.linked_canvas];
      if (canvas) {
        // Accumulate max trait requirements from trigger conditions
        (canvas.trigger_conditions || []).forEach(cond => {
          if (cond.type === 'trait' && cond.operator === 'gte') {
            const subject = cond.subject === 'npc' ? cond.npc_id : 'player';
            if (TRAITS[subject] && TRAITS[subject][cond.trait_key] !== undefined) {
              TRAITS[subject][cond.trait_key] = Math.max(TRAITS[subject][cond.trait_key], cond.value);
            }
          }
        });
        // Set flags this canvas sets on completion
        (canvas.flag_effects || []).forEach(f => { FLAGS[f] = true; });
      }
      // Set the node's own linked flag
      if (node.linked_flag) FLAGS[node.linked_flag] = true;

      if (node.id === targetNodeId) { found = true; break; }
    }
    if (found) break;
  }

  renderControls();
  renderMain();
}

function getEmotionLabel(traitKey, value) {
  const mappings = DATA.story_arc?.emotion_mappings || {};
  const mapping = mappings[traitKey];
  if (!mapping || !mapping.ranges) return '';
  for (const r of mapping.ranges) {
    if (value >= r.min && value <= r.max) return r.label;
  }
  return '';
}

// ─── Condition Evaluation ─────────────────────────
function evalCondition(item) {
  if (item.type === 'trait') {
    const subject = item.subject === 'npc' ? item.npc_id : 'player';
    const val = (TRAITS[subject] || {})[item.trait_key] ?? 0;
    if (item.operator === 'gte') return val >= item.value;
    if (item.operator === 'lte') return val <= item.value;
    if (item.operator === 'eq') return val === item.value;
  }
  if (item.type === 'flag') {
    return !!FLAGS[item.flag_key];
  }
  // days_since_flag - can't evaluate without game state
  if (item.type === 'days_since_flag') return null;
  return true;
}

function evalConditions(items, logic) {
  if (!items || items.length === 0) return true;
  if (logic === 'OR') return items.some(i => { const r = evalCondition(i); return r === true || r === null; });
  return items.every(i => { const r = evalCondition(i); return r === true || r === null; });
}

function conditionText(item) {
  if (item.type === 'trait') {
    const opMap = { gte: '>=', lte: '<=', eq: '=' };
    return item.trait_key + ' ' + (opMap[item.operator] || item.operator) + ' ' + item.value;
  }
  if (item.type === 'flag') return item.flag_key;
  if (item.type === 'days_since_flag') {
    const opMap = { gte: '\u2265', lte: '\u2264', eq: '', gt: '>', lt: '<' };
    return (opMap[item.operator] || '') + item.value + ' days after ' + item.flag_key;
  }
  return JSON.stringify(item);
}

function renderCondPills(items, logic) {
  if (!items || items.length === 0) return '';
  const pills = items.map(c => {
    const met = evalCondition(c);
    const cls = met === null ? 'unknown' : (met ? 'met' : 'unmet');
    return '<span class="cond-pill ' + cls + '">' + esc(conditionText(c)) + '</span>';
  });
  if (pills.length <= 1) return pills.join('');
  const sep = ' <span class="logic-sep">' + (logic === 'OR' ? 'OR' : 'AND') + '</span> ';
  return pills.join(sep);
}

// ─── Main Render ──────────────────────────────────
function renderMain() {
  if (DETAIL_CANVAS_ID) { renderCanvasDetail(); return; }
  if (VIEW_MODE === 'flowchart') { renderFlowchart(); return; }
  if (VIEW_MODE === 'media') { renderMediaView(); return; }
  renderListView();
}

function renderListView() {
  const main = document.getElementById('main');
  const sa = DATA.story_arc || {};
  const chapters = (sa.chapters || []).slice().sort((a, b) => a.order - b.order);
  const nodes = sa.nodes || [];
  const groups = sa.groups || [];

  // Build canvas lookup
  const canvasMap = {};
  DATA.canvases.forEach(c => { canvasMap[c.id] = c; });

  // Build group membership
  const groupMembers = {};
  groups.forEach(g => { groupMembers[g.id] = []; });
  nodes.forEach(n => {
    if (n.group && groupMembers[n.group]) groupMembers[n.group].push(n);
  });

  // Stats
  const storyCanvases = DATA.canvases.filter(c => !c.is_repeatable);
  const activityCanvases = DATA.canvases.filter(c => c.is_repeatable);
  const totalChoices = activityCanvases.reduce((s, c) => s + (c.choices?.length || 0), 0);

  let html = '<h1>' + esc(DATA.project.title) + '</h1>';
  html += '<div class="subtitle">Game Review Panel</div>';
  html += '<div class="stats-bar">';
  if (!isSingleNpcGame()) html += '<div class="stat-item"><strong>' + getUniqueNpcs().length + '</strong> NPCs</div>';
  html += '<div class="stat-item"><strong>' + chapters.length + '</strong> chapters</div>';
  html += '<div class="stat-item"><strong>' + storyCanvases.length + '</strong> story events</div>';
  html += '<div class="stat-item"><strong>' + activityCanvases.length + '</strong> activities</div>';
  html += '<div class="stat-item"><strong>' + totalChoices + '</strong> conditional choices</div>';
  const mmCount = (DATA.missing_media || []).length;
  if (mmCount > 0) html += '<div class="stat-item" style="cursor:pointer;color:#f87171" onclick="setViewMode(\'media\')"><strong>' + mmCount + '</strong> missing media</div>';
  const rc = reviewCounts();
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'approved' ? ' active rv-approved' : '') + '" onclick="toggleReviewFilter(\'approved\')"><strong>' + rc.approved + '</strong> approved</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'review' ? ' active rv-review' : '') + '" onclick="toggleReviewFilter(\'review\')"><strong>' + rc.review + '</strong> review</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'disapproved' ? ' active rv-disapproved' : '') + '" onclick="toggleReviewFilter(\'disapproved\')"><strong>' + rc.disapproved + '</strong> disapproved</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'unmarked' ? ' active' : '') + '" onclick="toggleReviewFilter(\'unmarked\')"><strong>' + rc.unmarked + '</strong> unmarked</div>';
  if (FLAG_FILTER) {
    html += '<div class="flag-filter-chip" onclick="toggleFlagFilter(\'' + esc(FLAG_FILTER) + '\')">flag: ' + esc(FLAG_FILTER) + ' <span class="chip-x">&times;</span></div>';
  }
  html += '</div>';

  // ── Story Arc ──
  html += '<h2 style="font-size:16px;color:#fff;margin-bottom:12px">Story Arc</h2>';

  if (isSingleNpcGame()) {
    // Single NPC: render chapters directly (original behavior)
    chapters.forEach((ch, ci) => {
      const chapterNodes = nodes.filter(n => n.chapter === ch.id);
      html += renderChapterSectionForNpc(ch, ci, chapterNodes, groups, groupMembers, canvasMap);
    });
  } else {
    // Multi-NPC: grouped by NPC
    const npcOrder = getUniqueNpcs();
    let globalChapterIdx = 0;

    npcOrder.forEach((npcId, npcIdx) => {
      const npcNodes = getNodesForNpc(npcId);
      const npcChapters = getChaptersForNodes(npcNodes);
      const color = getNpcColor(npcIdx);
      const name = npcName(npcId);

      html += '<div class="npc-section">';
      html += '<div class="npc-header" style="border-left-color:' + color + '" onclick="toggleNpcSection(' + npcIdx + ')">';
      html += '<span class="npc-arrow" id="npc-arrow-' + npcIdx + '">&#9654;</span>';
      html += '<span class="npc-header-name">' + esc(name) + '</span>';
      html += '<span class="npc-header-count">' + npcNodes.length + ' events</span>';
      html += '</div>';
      html += '<div class="npc-body" id="npc-body-' + npcIdx + '">';

      npcChapters.forEach(ch => {
        const chapterNpcNodes = npcNodes.filter(n => n.chapter === ch.id);
        if (chapterNpcNodes.length === 0) return;
        html += renderChapterSectionForNpc(ch, globalChapterIdx, chapterNpcNodes, groups, groupMembers, canvasMap);
        globalChapterIdx++;
      });

      html += '</div></div>';
    });

    // Orphan nodes (no NPC)
    const orphans = getOrphanNodes();
    if (orphans.length > 0) {
      const orphanChapters = getChaptersForNodes(orphans);
      const orphanIdx = npcOrder.length;

      html += '<div class="npc-section">';
      html += '<div class="npc-header npc-header-general" onclick="toggleNpcSection(' + orphanIdx + ')">';
      html += '<span class="npc-arrow" id="npc-arrow-' + orphanIdx + '">&#9654;</span>';
      html += '<span class="npc-header-name">Cross-NPC &amp; General Events</span>';
      html += '<span class="npc-header-count">' + orphans.length + ' events</span>';
      html += '</div>';
      html += '<div class="npc-body" id="npc-body-' + orphanIdx + '">';

      orphanChapters.forEach(ch => {
        const chOrphans = orphans.filter(n => n.chapter === ch.id);
        if (chOrphans.length === 0) return;
        html += renderChapterSectionForNpc(ch, globalChapterIdx, chOrphans, groups, groupMembers, canvasMap);
        globalChapterIdx++;
      });

      html += '</div></div>';
    }
  }

  // ── Activities ──
  html += '<hr class="section-divider">';
  html += renderActivitiesSection(activityCanvases);

  main.innerHTML = html;

  // Auto-open first section
  if (isSingleNpcGame()) {
    if (chapters.length > 0) toggleChapter(0);
  } else {
    toggleNpcSection(0);
  }
}

function renderStoryNode(node, canvasMap) {
  const canvas = canvasMap[node.linked_canvas] || {};
  const conditions = canvas.trigger_conditions || [];
  const logic = canvas.trigger_logic || 'AND';
  const flagEffects = canvas.flag_effects || [];
  const isMilestone = node.is_milestone;

  // Check requires_nodes
  let reqNodesMet = true;
  if (node.requires_nodes) {
    reqNodesMet = node.requires_nodes.every(reqId => {
      // Find the linked_flag for the required node
      const reqNode = (DATA.story_arc.nodes || []).find(n => n.id === reqId);
      if (reqNode && reqNode.linked_flag) return !!FLAGS[reqNode.linked_flag];
      return true;
    });
  }

  // Check requires_group
  let reqGroupMet = true;
  if (node.requires_group) {
    // A group is "met" if we toggle the concept - for now, approximate
    // In real game, groups track completion. Here we just check if a linked flag exists
    reqGroupMet = true; // Can't fully evaluate without play state
  }

  const condsMet = evalConditions(conditions, logic) && reqNodesMet && reqGroupMet;
  const stateClass = condsMet ? 'unlocked' : 'locked';
  const icon = isMilestone ? (condsMet ? '\u2605' : '\uD83D\uDD12') : (condsMet ? '\u25CB' : '\uD83D\uDD12');

  let html = '<div class="story-node ' + stateClass + '">';
  html += '<span class="node-icon">' + icon + '</span>';
  html += '<div class="node-content">';
  html += '<div class="node-name"><span class="canvas-link" onclick="event.stopPropagation();openCanvasDetail(\''+esc(node.linked_canvas)+'\')">' + esc(node.name) + '</span>' + reviewBadge(node.linked_canvas) + ' <button class="sim-btn" onclick="event.stopPropagation();simulateToNode(\''+esc(node.id)+'\')" title="Simulate to here">&#9654;</button></div>';

  // Meta
  const metaParts = [];
  if (canvas.location) metaParts.push(canvas.location);
  if (canvas.schedule) metaParts.push(canvas.schedule.start_time + '-' + canvas.schedule.end_time);
  if (node.linked_canvas) metaParts.push(node.linked_canvas);
  if (node.linked_canvas_node) {
    const targetNode = (canvas.nodes || []).find(n => n.id === node.linked_canvas_node);
    const targetLabel = targetNode ? targetNode.name + ' (' + node.linked_canvas_node + ')' : node.linked_canvas_node;
    metaParts.push('\u2192 ' + targetLabel);
  }
  if (metaParts.length > 0) {
    html += '<div class="node-meta">' + metaParts.map(esc).join(' | ') + '</div>';
  }

  // Conditions
  if (conditions.length > 0 || node.requires_nodes?.length > 0) {
    html += '<div class="node-conditions">';
    html += renderCondPills(conditions, logic);
    if (node.requires_nodes) {
      node.requires_nodes.forEach(reqId => {
        const reqNode = (DATA.story_arc.nodes || []).find(n => n.id === reqId);
        const met = reqNode?.linked_flag ? !!FLAGS[reqNode.linked_flag] : true;
        html += '<span class="cond-pill ' + (met ? 'met' : 'unmet') + '">after: ' + esc(reqId) + '</span>';
      });
    }
    if (node.requires_group) {
      html += '<span class="cond-pill met">group: ' + esc(node.requires_group) + '</span>';
    }
    // Flag effects
    flagEffects.forEach(f => {
      html += '<span class="flag-set-pill">sets: ' + esc(f) + '</span>';
    });
    html += '</div>';
  } else if (flagEffects.length > 0) {
    html += '<div class="node-conditions">';
    flagEffects.forEach(f => {
      html += '<span class="flag-set-pill">sets: ' + esc(f) + '</span>';
    });
    html += '</div>';
  }

  html += '</div></div>';
  return html;
}

function renderActivityCard(canvas) {
  const hasTriggerConds = canvas.trigger_conditions && canvas.trigger_conditions.length > 0;
  const triggerMet = evalConditions(canvas.trigger_conditions, canvas.trigger_logic);

  let html = '<div class="activity-card" style="' + (triggerMet ? '' : 'opacity:0.6') + '">';
  html += '<div class="activity-header">';
  html += '<div class="activity-name">' + (triggerMet ? '' : '\uD83D\uDD12 ') + '<span class="canvas-link" onclick="openCanvasDetail(\''+esc(canvas.id)+'\')">' + esc(canvas.name) + '</span>' + reviewBadge(canvas.id) + '</div>';
  html += '<div class="activity-meta">';
  if (canvas.location) html += '<span>' + esc(canvas.location) + '</span>';
  if (canvas.schedule) html += '<span>' + canvas.schedule.start_time + '-' + canvas.schedule.end_time + '</span>';
  if (canvas.npc) html += '<span>' + esc(canvas.npc) + '</span>';
  if (canvas.max_triggers_per_day) html += '<span class="daily-limit-badge">' + canvas.max_triggers_per_day + 'x/day</span>';
  html += '</div>';
  html += '</div>';

  html += '<div class="activity-body">';

  // Trigger conditions
  if (hasTriggerConds) {
    html += '<div class="activity-trigger">Requires: ';
    html += renderCondPills(canvas.trigger_conditions, canvas.trigger_logic);
    html += '</div>';
  }

  // Choices
  if (canvas.choices && canvas.choices.length > 0) {
    canvas.choices.forEach(ch => {
      const hasCond = ch.conditions && ch.conditions.length > 0;
      const choiceMet = !hasCond || evalConditions(ch.conditions, ch.conditions_logic);
      const icon = choiceMet ? '\u2705' : '\uD83D\uDD12';
      html += '<div class="choice-row">';
      html += '<span class="choice-icon">' + icon + '</span>';
      html += '<div>';
      html += '<div class="choice-text">' + esc(ch.text) + '</div>';
      if (hasCond) {
        html += '<div class="choice-conds">';
        html += renderCondPills(ch.conditions, ch.conditions_logic);
        html += '</div>';
      }
      html += '</div></div>';
    });
  }

  html += '</div></div>';
  return html;
}

// ─── NPC-Grouped Rendering Helpers ──────────────────────────

function renderChapterSectionForNpc(ch, ci, filteredNodes, groups, groupMembers, canvasMap) {
  const groupedNodeIds = new Set();
  const chapterGroups = [];
  filteredNodes.forEach(n => {
    if (n.group && groupMembers[n.group] && !chapterGroups.find(g => g.id === n.group)) {
      const grp = groups.find(g => g.id === n.group);
      if (grp) chapterGroups.push(grp);
    }
    if (n.group) groupedNodeIds.add(n.id);
  });

  let html = '<div class="chapter">';
  html += '<div class="chapter-header mood-' + (ch.mood || 'neutral') + '" onclick="toggleChapter(' + ci + ')">';
  html += '<span class="chapter-arrow" id="arrow-' + ci + '">&#9654;</span>';
  html += '<span class="chapter-name">' + esc(ch.name) + '</span>';
  html += '<span class="chapter-mood">' + esc(ch.mood || '') + '</span>';
  html += '</div>';
  html += '<div class="chapter-body" id="chbody-' + ci + '">';

  // Ungrouped nodes
  filteredNodes.filter(n => !groupedNodeIds.has(n.id)).forEach(n => {
    if (!matchesReviewFilter(n.linked_canvas) || !matchesFlagFilter(n.linked_canvas, n)) return;
    html += renderStoryNode(n, canvasMap);
  });

  // Groups — only members within this NPC's set
  chapterGroups.forEach(grp => {
    const allGrpMembers = groupMembers[grp.id] || [];
    const members = allGrpMembers.filter(n =>
      filteredNodes.some(fn => fn.id === n.id) &&
      matchesReviewFilter(n.linked_canvas) &&
      matchesFlagFilter(n.linked_canvas, n)
    );
    if (members.length === 0 && (REVIEW_FILTER || FLAG_FILTER)) return;
    html += '<div class="group-box">';
    html += '<div class="group-header">GROUP: ' + esc(grp.name) + ' (' + grp.required_count + ' of ' + members.length + ' in this arc)</div>';
    html += '<div class="group-desc">' + esc(grp.description || '') + '</div>';
    members.forEach(n => { html += renderStoryNode(n, canvasMap); });
    html += '</div>';
  });

  html += '</div></div>';
  return html;
}

function renderActivitiesSection(activityCanvases) {
  let html = '';

  if (isSingleNpcGame()) {
    const filtered = activityCanvases.filter(c => matchesReviewFilter(c.id) && matchesFlagFilter(c.id));
    html += '<h2 style="font-size:16px;color:#fff;margin-bottom:12px">Activities (' + filtered.length + ((REVIEW_FILTER || FLAG_FILTER) ? ' / ' + activityCanvases.length : '') + ')</h2>';
    html += '<div class="activities-grid">';
    filtered.forEach(c => { html += renderActivityCard(c); });
    html += '</div>';
    return html;
  }

  // Multi-NPC: group by canvas.npc
  const npcOrder = getUniqueNpcs();
  const npcActivities = {};
  const generalActivities = [];

  activityCanvases.forEach(c => {
    if (c.npc && npcOrder.includes(c.npc)) {
      if (!npcActivities[c.npc]) npcActivities[c.npc] = [];
      npcActivities[c.npc].push(c);
    } else {
      generalActivities.push(c);
    }
  });

  const totalFiltered = activityCanvases.filter(c => matchesReviewFilter(c.id) && matchesFlagFilter(c.id)).length;
  html += '<h2 style="font-size:16px;color:#fff;margin-bottom:12px">Activities (' + totalFiltered + ((REVIEW_FILTER || FLAG_FILTER) ? ' / ' + activityCanvases.length : '') + ')</h2>';

  npcOrder.forEach((npcId, idx) => {
    const acts = (npcActivities[npcId] || []).filter(c => matchesReviewFilter(c.id) && matchesFlagFilter(c.id));
    if (acts.length === 0) return;
    const color = getNpcColor(idx);
    html += '<div class="npc-activities-label" style="color:' + color + ';border-left-color:' + color + '">' + esc(npcName(npcId)) + ' Activities (' + acts.length + ')</div>';
    html += '<div class="activities-grid">';
    acts.forEach(c => { html += renderActivityCard(c); });
    html += '</div>';
  });

  const genFiltered = generalActivities.filter(c => matchesReviewFilter(c.id) && matchesFlagFilter(c.id));
  if (genFiltered.length > 0) {
    html += '<div class="npc-activities-label" style="color:#888;border-left-color:#666">General Activities (' + genFiltered.length + ')</div>';
    html += '<div class="activities-grid">';
    genFiltered.forEach(c => { html += renderActivityCard(c); });
    html += '</div>';
  }

  return html;
}

// ─── Missing Media View ──────────────────────────
function renderMediaView() {
  const main = document.getElementById('main');
  const missing = DATA.missing_media || [];
  const found = DATA.found_media || [];
  const gameName = DATA.project.id;

  // Count review statuses
  const approvedCount = found.filter(f => MEDIA_REVIEW[f.file] && MEDIA_REVIEW[f.file].status === 'approved').length;
  const disapprovedCount = found.filter(f => MEDIA_REVIEW[f.file] && MEDIA_REVIEW[f.file].status === 'disapproved').length;
  const unreviewedCount = found.length - approvedCount - disapprovedCount;

  let html = '<h1>' + esc(DATA.project.title) + '</h1>';
  html += '<div class="subtitle">Media Review</div>';

  // Summary / filter bar
  html += '<div class="mr-summary-bar">';
  html += '<div class="mr-filter-btn' + (!MEDIA_FILTER ? ' active' : '') + '" onclick="toggleMediaFilter(null)"><strong>' + found.length + '</strong> found</div>';
  html += '<div class="mr-filter-btn f-approved' + (MEDIA_FILTER === 'approved' ? ' active' : '') + '" onclick="toggleMediaFilter(\'approved\')"><strong>' + approvedCount + '</strong> approved</div>';
  html += '<div class="mr-filter-btn f-disapproved' + (MEDIA_FILTER === 'disapproved' ? ' active' : '') + '" onclick="toggleMediaFilter(\'disapproved\')"><strong>' + disapprovedCount + '</strong> disapproved</div>';
  html += '<div class="mr-filter-btn' + (MEDIA_FILTER === 'unreviewed' ? ' active' : '') + '" onclick="toggleMediaFilter(\'unreviewed\')"><strong>' + unreviewedCount + '</strong> unreviewed</div>';
  html += '<div class="mr-sep"></div>';
  html += '<div class="mr-filter-btn f-missing' + (MEDIA_FILTER === 'missing' ? ' active' : '') + '" onclick="toggleMediaFilter(\'missing\')"><strong>' + missing.length + '</strong> missing</div>';
  html += '</div>';

  // ─── Grouping sub-toggle ───
  if (MEDIA_FILTER !== 'missing') {
  html += '<div class="mr-groupby-bar">';
  html += '<span class="mr-groupby-label">Group by</span>';
  html += '<div class="mr-groupby-btn' + (MEDIA_GROUP_BY === 'canvas' ? ' active' : '') + '" onclick="setMediaGroupBy(\'canvas\')">Canvas</div>';
  html += '<div class="mr-groupby-btn' + (MEDIA_GROUP_BY === 'tier' ? ' active' : '') + '" onclick="setMediaGroupBy(\'tier\')">Tier</div>';
  html += '</div>';

  // ─── Found media ───
  if (found.length > 0) {
    if (MEDIA_GROUP_BY === 'canvas') {
      // ─── Group by canvas_id ───
      const groups = {};
      found.forEach(item => {
        const key = item.canvas_id || '_unknown';
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      });

      const sortedKeys = Object.keys(groups).sort((a, b) => {
        const minA = Math.min(...groups[a].map(i => i.order != null ? i.order : 9999));
        const minB = Math.min(...groups[b].map(i => i.order != null ? i.order : 9999));
        return minA - minB;
      });

      sortedKeys.forEach(k => {
        groups[k].sort((a, b) => (a.order || 0) - (b.order || 0));
      });

      const pseudoNames = { navigation: 'Locations', wardrobe: 'Wardrobe' };

      sortedKeys.forEach(canvasId => {
        const items = groups[canvasId];
        const filtered = MEDIA_FILTER ? items.filter(i => matchesMediaFilter(i.file)) : items;
        if (filtered.length === 0) return;

        const displayName = pseudoNames[canvasId] || (items[0].canvas_name || canvasId);
        const reviewed = items.filter(i => MEDIA_REVIEW[i.file]).length;

        html += '<details class="mr-section" open>';
        html += '<summary class="mr-section-header">';
        html += '<span class="mr-section-arrow">&#9654;</span>';
        html += esc(displayName);
        html += ' <span class="mr-section-count">(' + filtered.length + ' items)</span>';
        if (reviewed > 0) {
          html += '<span class="mr-section-reviewed">' + reviewed + '/' + items.length + ' reviewed</span>';
        }
        html += '</summary>';
        html += '<div class="mr-items-grid">';
        filtered.forEach(item => {
          html += renderMediaReviewItem(item);
        });
        html += '</div></details>';
      });
    } else {
      // ─── Group by tier ───
      const tierGroups = {};
      found.forEach(item => {
        const tier = extractTier(item.file);
        if (!tierGroups[tier]) tierGroups[tier] = [];
        tierGroups[tier].push(item);
      });

      const tierOrder = ['base', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 'misc'];

      tierOrder.forEach(tier => {
        const items = tierGroups[tier];
        if (!items || items.length === 0) return;
        const filtered = MEDIA_FILTER ? items.filter(i => matchesMediaFilter(i.file)) : items;
        if (filtered.length === 0) return;

        const meta = TIER_META[tier] || TIER_META.misc;
        const reviewed = items.filter(i => MEDIA_REVIEW[i.file]).length;
        const approvedInTier = items.filter(i => MEDIA_REVIEW[i.file] && MEDIA_REVIEW[i.file].status === 'approved').length;
        const disapprovedInTier = items.filter(i => MEDIA_REVIEW[i.file] && MEDIA_REVIEW[i.file].status === 'disapproved').length;

        html += '<details class="mr-section" open>';
        html += '<summary class="mr-section-header" style="border-left-color:' + meta.color + '">';
        html += '<span class="mr-section-arrow">&#9654;</span>';
        html += '<strong>' + esc(tier) + '</strong> ';
        html += '<span class="mr-tier-label">' + esc(meta.label) + ' \u2014 ' + esc(meta.desc) + '</span>';
        html += '<span class="mr-section-count">(' + filtered.length + ' items)</span>';
        if (reviewed > 0) {
          html += '<span class="mr-section-reviewed">' + approvedInTier + '\u2713 ' + disapprovedInTier + '\u2717 / ' + items.length + '</span>';
        }
        html += '</summary>';
        html += '<div class="mr-items-grid">';
        filtered.forEach(item => {
          html += renderMediaReviewItem(item);
        });
        html += '</div></details>';
      });
    }
  }

  if (found.length === 0 && missing.length === 0) {
    html += '<div style="padding:40px;text-align:center;color:#4ade80;font-size:14px">No media references found.</div>';
  }
  } // end if (MEDIA_FILTER !== 'missing')

  // ─── Missing media (unchanged category layout) ───
  if (missing.length > 0) {
    const isMissingOnly = MEDIA_FILTER === 'missing';
    html += '<div style="' + (isMissingOnly ? '' : 'margin-top:32px;padding-top:20px;border-top:1px solid #2a2a2a') + '">';
    html += '<div class="subtitle">Missing Media (' + missing.length + ')</div>';

    const categories = {};
    const categoryOrder = ['Locations', 'Story', 'Activities', 'Clothing', 'Social Media', 'Other'];
    missing.forEach(m => {
      const cat = m.category || 'Other';
      if (!categories[cat]) categories[cat] = [];
      categories[cat].push(m);
    });

    categoryOrder.forEach(cat => {
      const items = categories[cat];
      if (!items || items.length === 0) return;
      html += '<div class="mm-section">';
      html += '<div class="mm-section-header">' + esc(cat) + ' <span class="mm-section-count">(' + items.length + ' missing)</span></div>';
      items.forEach(item => {
        html += renderMediaItem(item, gameName, false);
      });
      html += '</div>';
    });
    html += '</div>';
  }

  main.innerHTML = html;
}

function buildSearchUrl(query, gameName, filePath) {
  const params = new URLSearchParams({
    q: query,
    _tmc_game: gameName,
    _tmc_scene: filePath
  });
  return 'https://www.google.com/search?' + params.toString();
}

function renderMediaItem(item, gameName, isFound) {
  let html = '<div class="mm-item' + (isFound ? ' mm-found' : '') + '">';
  html += '<div class="mm-item-header">';
  html += '<span class="mm-type-badge ' + esc(item.type) + '">' + esc(item.type.replace('_', ' ')) + '</span>';
  html += '<span class="mm-file-path">' + esc(item.file) + '</span>';
  if (item.actual_file) {
    html += '<span class="mm-actual-file">' + esc(item.actual_file) + '</span>';
  }
  if (item.actual_type && item.actual_type !== item.type) {
    html += '<span class="mm-type-switch">renders as ' + esc(item.actual_type) + '</span>';
  }
  if (item.canvas_id && item.canvas_id !== 'navigation') {
    const canvasName = item.canvas_name || item.canvas_id;
    html += '<span class="mm-canvas-tag">' + esc(canvasName) + '</span>';
  }
  html += '</div>';

  if (item.description) {
    html += '<div class="mm-description">' + esc(item.description) + '</div>';
  }

  // Search query buttons
  const queries = item.search_queries || [];
  if (queries.length > 0 && !isFound) {
    html += '<div class="mm-search-row">';
    queries.forEach(q => {
      const url = buildSearchUrl(q, gameName, item.file);
      html += '<a class="mm-search-btn" href="' + esc(url) + '" target="_blank" title="' + esc(q) + '">\uD83D\uDD0D ' + esc(q.length > 80 ? q.substring(0, 80) + '...' : q) + '</a>';
    });
    html += '</div>';
  }

  html += '</div>';
  return html;
}

// ─── Flowchart View ──────────────────────────────
function summarizeEffects(canvas) {
  const effects = canvas.all_effects || [];
  if (effects.length === 0) return '';
  const byTrait = {};
  effects.forEach(e => {
    const key = e.trait || '';
    if (!key) return;
    if (!byTrait[key]) byTrait[key] = [];
    byTrait[key].push(e.value || 0);
  });
  const parts = [];
  Object.keys(byTrait).forEach(trait => {
    const vals = byTrait[trait];
    const mn = Math.min(...vals);
    const mx = Math.max(...vals);
    parts.push(mn === mx ? '+' + mn + ' ' + trait : '+' + mn + '-' + mx + ' ' + trait);
  });
  return parts.join(', ');
}

const TIME_SLOTS = [
  { id: 'morning', label: 'Morning (7\u201312)', start: 7, end: 12 },
  { id: 'afternoon', label: 'Afternoon (12\u201317)', start: 12, end: 17 },
  { id: 'evening', label: 'Evening (17\u201322)', start: 17, end: 22 },
  { id: 'night', label: 'Night (22\u20131)', start: 22, end: 25 },
];

function getTimeSlot(act) {
  if (!act.schedule || !act.schedule.start_time) return 'morning';
  const h = parseInt(act.schedule.start_time.split(':')[0], 10);
  for (const s of TIME_SLOTS) {
    if (h >= s.start && h < s.end) return s.id;
  }
  return 'morning';
}

function locName(locId) {
  if (!locId) return '';
  const l = (DATA.locations || []).find(l => l.id === locId);
  return l ? l.name : locId.replace('loc_', '').replace(/_/g, ' ');
}

function buildFlowchartTiers() {
  const sa = DATA.story_arc || {};
  const chapters = (sa.chapters || []).slice().sort((a, b) => a.order - b.order);
  const allNodes = sa.nodes || [];
  const canvasMap = {};
  DATA.canvases.forEach(c => { canvasMap[c.id] = c; });

  const activities = DATA.canvases.filter(c => c.is_repeatable);
  const assignedActivities = new Set();

  // Simulated state
  const simT = {};
  DATA.npcs.forEach(npc => {
    simT[npc.id] = {};
    Object.keys(npc.core_traits || {}).forEach(k => { simT[npc.id][k] = 0; });
  });
  simT.player = {};
  Object.keys(DATA.player.traits || {}).forEach(k => { simT.player[k] = DATA.player.traits[k]; });
  const simF = {};
  (DATA.player.flag_keys || []).forEach(f => { simF[f] = false; });

  function simAccessible(act) {
    const items = act.trigger_conditions || [];
    const logic = act.trigger_logic || 'AND';
    if (items.length === 0) return true;
    const chk = (item) => {
      if (item.type === 'trait') {
        const subj = item.subject === 'npc' ? item.npc_id : 'player';
        const val = (simT[subj] || {})[item.trait_key] ?? 0;
        if (item.operator === 'gte') return val >= item.value;
        if (item.operator === 'lte') return val <= item.value;
        if (item.operator === 'eq') return val === item.value;
      }
      if (item.type === 'flag') return !!simF[item.flag_key];
      if (item.type === 'days_since_flag') return !!simF[item.flag_key];
      return true;
    };
    return logic === 'OR' ? items.some(chk) : items.every(chk);
  }

  function collectNewActivities(storyCanvasIds) {
    return activities.filter(a => {
      if (assignedActivities.has(a.id)) return false;
      if (storyCanvasIds && storyCanvasIds.has(a.id)) { assignedActivities.add(a.id); return false; }
      if (simAccessible(a)) { assignedActivities.add(a.id); return true; }
      return false;
    });
  }

  function applyNode(node) {
    const canvas = canvasMap[node.linked_canvas];
    if (canvas) {
      (canvas.trigger_conditions || []).forEach(cond => {
        if (cond.type === 'trait' && cond.operator === 'gte') {
          const subj = cond.subject === 'npc' ? cond.npc_id : 'player';
          if (simT[subj] && simT[subj][cond.trait_key] !== undefined) {
            simT[subj][cond.trait_key] = Math.max(simT[subj][cond.trait_key], cond.value);
          }
        }
      });
      (canvas.flag_effects || []).forEach(f => { simF[f] = true; });
    }
    if (node.linked_flag) simF[node.linked_flag] = true;
  }

  const tiers = [];
  let cumulativeActs = []; // all activities accessible up to this tier

  function makeTier(storyNodes, chapter, newActs, label) {
    cumulativeActs = cumulativeActs.concat(newActs);
    const newIds = new Set(newActs.map(a => a.id));
    // Group all cumulative activities by time slot
    const byTime = { morning: [], afternoon: [], evening: [], night: [] };
    cumulativeActs.forEach(act => {
      const slot = getTimeSlot(act);
      byTime[slot].push({ act: act, isNew: newIds.has(act.id) });
    });
    tiers.push({ storyNodes, chapter, newActivities: newActs, allActivities: cumulativeActs.slice(), byTimeSlot: byTime, label });
  }

  // Tier 0: starting state
  const startNode = allNodes.find(n => n.linked_canvas === DATA.starting_canvas);
  if (startNode) applyNode(startNode);
  const startIds = new Set(startNode ? [startNode.linked_canvas] : []);
  const tier0acts = collectNewActivities(startIds);
  makeTier(startNode ? [startNode] : [], startNode ? chapters.find(c => c.id === startNode.chapter) : chapters[0], tier0acts, 'Game Start');

  const processedStart = startNode ? startNode.id : null;
  let pendingNodes = [];

  for (const ch of chapters) {
    const chNodes = allNodes.filter(n => n.chapter === ch.id);
    for (const node of chNodes) {
      if (node.id === processedStart) continue;
      applyNode(node);
      const nodeCanvasIds = new Set([...pendingNodes.map(n => n.linked_canvas), node.linked_canvas].filter(Boolean));
      const newActs = collectNewActivities(nodeCanvasIds);
      if (node.is_milestone || newActs.length > 0) {
        makeTier([...pendingNodes, node], ch, newActs, node.name);
        pendingNodes = [];
      } else {
        pendingNodes.push(node);
      }
    }
  }

  const remaining = activities.filter(a => !assignedActivities.has(a.id));
  if (remaining.length > 0 || pendingNodes.length > 0) {
    makeTier(pendingNodes, chapters[chapters.length - 1], remaining, 'Late Game');
  }

  return tiers;
}

function buildFlowchartTiersForNpc(npcId) {
  const sa = DATA.story_arc || {};
  const chapters = (sa.chapters || []).slice().sort((a, b) => a.order - b.order);
  const allNodes = sa.nodes || [];
  const canvasMap = {};
  DATA.canvases.forEach(c => { canvasMap[c.id] = c; });

  // Filter activities: NPC-tagged activities for that NPC, or general (no npc) if npcId is null
  const activities = DATA.canvases.filter(c => {
    if (!c.is_repeatable) return false;
    if (npcId === null) return !c.npc;
    return c.npc === npcId || !c.npc;
  });
  const assignedActivities = new Set();

  // Simulated state — walk ALL nodes globally for correct cross-NPC deps
  const simT = {};
  DATA.npcs.forEach(npc => {
    simT[npc.id] = {};
    Object.keys(npc.core_traits || {}).forEach(k => { simT[npc.id][k] = 0; });
  });
  simT.player = {};
  Object.keys(DATA.player.traits || {}).forEach(k => { simT.player[k] = DATA.player.traits[k]; });
  const simF = {};
  (DATA.player.flag_keys || []).forEach(f => { simF[f] = false; });

  function simAccessible(act) {
    const items = act.trigger_conditions || [];
    const logic = act.trigger_logic || 'AND';
    if (items.length === 0) return true;
    const chk = (item) => {
      if (item.type === 'trait') {
        const subj = item.subject === 'npc' ? item.npc_id : 'player';
        const val = (simT[subj] || {})[item.trait_key] ?? 0;
        if (item.operator === 'gte') return val >= item.value;
        if (item.operator === 'lte') return val <= item.value;
        if (item.operator === 'eq') return val === item.value;
      }
      if (item.type === 'flag') return !!simF[item.flag_key];
      if (item.type === 'days_since_flag') return !!simF[item.flag_key];
      return true;
    };
    return logic === 'OR' ? items.some(chk) : items.every(chk);
  }

  function collectNewActivities(storyCanvasIds) {
    return activities.filter(a => {
      if (assignedActivities.has(a.id)) return false;
      if (storyCanvasIds && storyCanvasIds.has(a.id)) { assignedActivities.add(a.id); return false; }
      if (simAccessible(a)) { assignedActivities.add(a.id); return true; }
      return false;
    });
  }

  function applyNode(node) {
    const canvas = canvasMap[node.linked_canvas];
    if (canvas) {
      (canvas.trigger_conditions || []).forEach(cond => {
        if (cond.type === 'trait' && cond.operator === 'gte') {
          const subj = cond.subject === 'npc' ? cond.npc_id : 'player';
          if (simT[subj] && simT[subj][cond.trait_key] !== undefined) {
            simT[subj][cond.trait_key] = Math.max(simT[subj][cond.trait_key], cond.value);
          }
        }
      });
      (canvas.flag_effects || []).forEach(f => { simF[f] = true; });
    }
    if (node.linked_flag) simF[node.linked_flag] = true;
  }

  const tiers = [];
  let cumulativeActs = [];

  function makeTier(storyNodes, chapter, newActs, label) {
    cumulativeActs = cumulativeActs.concat(newActs);
    const newIds = new Set(newActs.map(a => a.id));
    const byTime = { morning: [], afternoon: [], evening: [], night: [] };
    cumulativeActs.forEach(act => {
      const slot = getTimeSlot(act);
      byTime[slot].push({ act: act, isNew: newIds.has(act.id) });
    });
    tiers.push({ storyNodes, chapter, newActivities: newActs, allActivities: cumulativeActs.slice(), byTimeSlot: byTime, label });
  }

  // Walk all nodes globally, but only create tiers for target NPC's nodes
  const isTarget = (node) => npcId === null ? !node.npc : node.npc === npcId;
  let pendingNodes = [];
  let firstTier = true;

  for (const ch of chapters) {
    const chNodes = allNodes.filter(n => n.chapter === ch.id);
    for (const node of chNodes) {
      applyNode(node); // always simulate for correct state
      if (!isTarget(node)) continue; // skip non-target nodes for tier creation

      const nodeCanvasIds = new Set([...pendingNodes.map(n => n.linked_canvas), node.linked_canvas].filter(Boolean));
      const newActs = collectNewActivities(nodeCanvasIds);
      const label = firstTier ? npcName(npcId) + ' Start' : node.name;
      if (firstTier || node.is_milestone || newActs.length > 0) {
        makeTier([...pendingNodes, node], ch, newActs, label);
        pendingNodes = [];
        firstTier = false;
      } else {
        pendingNodes.push(node);
      }
    }
  }

  const remaining = activities.filter(a => !assignedActivities.has(a.id));
  if (remaining.length > 0 || pendingNodes.length > 0) {
    makeTier(pendingNodes, chapters[chapters.length - 1], remaining, 'Late Game');
  }

  return tiers;
}

function renderFlowchartTier(tier, ti, canvasMap) {
  let tierUnlocked = true;
  if (tier.storyNodes.length > 0) {
    const primary = tier.storyNodes[tier.storyNodes.length - 1];
    const canvas = canvasMap[primary.linked_canvas] || {};
    tierUnlocked = evalConditions(canvas.trigger_conditions || [], canvas.trigger_logic || 'AND');
  }

  let html = '<div class="fc-tier ' + (tierUnlocked ? 'unlocked' : 'locked') + '">';
  html += '<div class="fc-tier-label">Tier ' + ti + ': ' + esc(tier.label) + '</div>';

  // Story nodes
  tier.storyNodes.forEach(node => {
    if (!matchesReviewFilter(node.linked_canvas) || !matchesFlagFilter(node.linked_canvas, node)) return;
    const canvas = canvasMap[node.linked_canvas] || {};
    const conds = canvas.trigger_conditions || [];
    const condsMet = evalConditions(conds, canvas.trigger_logic || 'AND');
    const stateClass = condsMet ? 'unlocked' : 'locked';
    const icon = node.is_milestone ? (condsMet ? '\u2605' : '\uD83D\uDD12') : (condsMet ? '\u25CB' : '\uD83D\uDD12');

    html += '<div class="fc-story ' + stateClass + '">';
    html += '<span style="margin-right:6px">' + icon + '</span>';
    html += '<span class="fc-story-name canvas-link" onclick="openCanvasDetail(\''+esc(node.linked_canvas)+'\')">' + esc(node.name) + '</span>';
    html += reviewBadge(node.linked_canvas);
    html += '<span class="fc-story-chapter">' + esc(tier.chapter?.name || '') + '</span>';
    html += ' <button class="sim-btn" onclick="event.stopPropagation();simulateToNode(\'' + esc(node.id) + '\')" title="Simulate to here">&#9654;</button>';

    if (conds.length > 0) {
      html += '<div class="fc-story-meta">Requires: ';
      html += renderCondPills(conds, canvas.trigger_logic || 'AND');
      html += '</div>';
    }

    if (node.linked_canvas_node) {
      const targetNode = (canvas.nodes || []).find(n => n.id === node.linked_canvas_node);
      const targetLabel = targetNode ? targetNode.name + ' (' + node.linked_canvas_node + ')' : node.linked_canvas_node;
      html += '<div class="fc-story-meta" style="color:#60a5fa">Target node: <strong>' + esc(targetLabel) + '</strong></div>';
    }

    const flags = canvas.flag_effects || [];
    if (flags.length > 0 || node.linked_flag) {
      html += '<div class="fc-story-flags">';
      if (node.linked_flag) html += '<span class="flag-set-pill">sets: ' + esc(node.linked_flag) + '</span>';
      flags.forEach(f => { if (f !== node.linked_flag) html += '<span class="flag-set-pill">sets: ' + esc(f) + '</span>'; });
      html += '</div>';
    }
    html += '</div>';
  });

  // Daily schedule grid
  const hasActs = tier.allActivities && tier.allActivities.length > 0;
  if (hasActs) {
    html += '<div class="fc-schedule">';
    TIME_SLOTS.forEach(slot => {
      html += '<div class="fc-time-col">';
      html += '<div class="fc-time-label">' + slot.label + '</div>';
      const items = tier.byTimeSlot[slot.id] || [];
      if (items.length === 0) {
        html += '<div class="fc-empty-slot">\u2014</div>';
      }
      items.forEach(item => {
        const act = item.act;
        if (!matchesReviewFilter(act.id) || !matchesFlagFilter(act.id)) return;
        const actMet = evalConditions(act.trigger_conditions || [], act.trigger_logic || 'AND');
        html += '<div class="fc-act-card' + (actMet ? '' : ' locked') + (item.isNew ? ' fc-act-new' : '') + '">';
        html += '<div class="fc-act-name">' + (actMet ? '' : '\uD83D\uDD12 ') + '<span class="canvas-link" onclick="event.stopPropagation();openCanvasDetail(\''+esc(act.id)+'\')">' + esc(act.name) + '</span>';
        html += reviewBadge(act.id);
        if (item.isNew) html += '<span class="fc-act-new-badge">NEW</span>';
        if (act.max_triggers_per_day) html += '<span class="daily-limit-badge">' + act.max_triggers_per_day + 'x/day</span>';
        html += '</div>';
        if (act.location) html += '<div class="fc-act-loc">' + esc(locName(act.location)) + '</div>';
        const effectSummary = summarizeEffects(act);
        if (effectSummary) html += '<div class="fc-act-effects"><span class="fc-effect-pill">' + esc(effectSummary) + '</span></div>';
        if (act.trigger_conditions && act.trigger_conditions.length > 0) {
          html += '<div class="fc-act-conds">';
          html += renderCondPills(act.trigger_conditions, act.trigger_logic || 'AND');
          html += '</div>';
        }
        html += '</div>';
      });
      html += '</div>';
    });
    html += '</div>';
  }

  html += '</div>';
  return html;
}

function renderFlowchart() {
  const main = document.getElementById('main');
  const canvasMap = {};
  DATA.canvases.forEach(c => { canvasMap[c.id] = c; });

  const storyCanvases = DATA.canvases.filter(c => !c.is_repeatable);
  const activityCanvases = DATA.canvases.filter(c => c.is_repeatable);
  const totalChoices = activityCanvases.reduce((s, c) => s + (c.choices?.length || 0), 0);
  const uniqueNpcs = getUniqueNpcs();
  const singleNpc = isSingleNpcGame();

  let html = '<h1>' + esc(DATA.project.title) + '</h1>';
  html += '<div class="subtitle">Flowchart View \u2014 Progression Map</div>';
  html += '<div class="stats-bar">';
  html += '<div class="stat-item"><strong>' + storyCanvases.length + '</strong> story events</div>';
  html += '<div class="stat-item"><strong>' + activityCanvases.length + '</strong> activities</div>';
  html += '<div class="stat-item"><strong>' + totalChoices + '</strong> choices</div>';
  if (!singleNpc) html += '<div class="stat-item"><strong>' + uniqueNpcs.length + '</strong> NPCs</div>';
  const rc2 = reviewCounts();
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'approved' ? ' active rv-approved' : '') + '" onclick="toggleReviewFilter(\'approved\')"><strong>' + rc2.approved + '</strong> approved</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'review' ? ' active rv-review' : '') + '" onclick="toggleReviewFilter(\'review\')"><strong>' + rc2.review + '</strong> review</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'disapproved' ? ' active rv-disapproved' : '') + '" onclick="toggleReviewFilter(\'disapproved\')"><strong>' + rc2.disapproved + '</strong> disapproved</div>';
  html += '<div class="stat-item rv-filter-btn' + (REVIEW_FILTER === 'unmarked' ? ' active' : '') + '" onclick="toggleReviewFilter(\'unmarked\')"><strong>' + rc2.unmarked + '</strong> unmarked</div>';
  if (FLAG_FILTER) {
    html += '<div class="flag-filter-chip" onclick="toggleFlagFilter(\'' + esc(FLAG_FILTER) + '\')">flag: ' + esc(FLAG_FILTER) + ' <span class="chip-x">&times;</span></div>';
  }
  html += '</div>';

  if (singleNpc) {
    // Single-NPC: original flowchart behavior
    const tiers = buildFlowchartTiers();
    html += '<div class="fc-container">';
    tiers.forEach((tier, ti) => { html += renderFlowchartTier(tier, ti, canvasMap); });
    html += '</div>';
  } else {
    // Multi-NPC: separate flowchart sections per NPC
    html += '<div class="fc-container">';

    uniqueNpcs.forEach((npcId, ni) => {
      const color = getNpcColor(ni);
      const npcNodes = getNodesForNpc(npcId);
      const tiers = buildFlowchartTiersForNpc(npcId);

      html += '<div class="fc-npc-section">';
      html += '<div class="fc-npc-label" style="border-left:4px solid ' + color + ';padding-left:10px;margin:20px 0 8px 0;font-size:1.15em;font-weight:700;color:' + color + '">';
      html += esc(npcName(npcId)) + ' <span style="font-weight:400;color:#94a3b8;font-size:0.85em">(' + npcNodes.length + ' nodes, ' + tiers.length + ' tiers)</span>';
      html += '</div>';

      tiers.forEach((tier, ti) => { html += renderFlowchartTier(tier, ti, canvasMap); });
      html += '</div>';
    });

    // Orphan / Cross-NPC nodes
    const orphans = getOrphanNodes();
    if (orphans.length > 0) {
      const orphanTiers = buildFlowchartTiersForNpc(null);
      if (orphanTiers.length > 0) {
        html += '<div class="fc-npc-section">';
        html += '<div class="fc-npc-label" style="border-left:4px solid #64748b;padding-left:10px;margin:20px 0 8px 0;font-size:1.15em;font-weight:700;color:#94a3b8">';
        html += 'Cross-NPC &amp; General Events <span style="font-weight:400;font-size:0.85em">(' + orphans.length + ' nodes)</span>';
        html += '</div>';
        orphanTiers.forEach((tier, ti) => { html += renderFlowchartTier(tier, ti, canvasMap); });
        html += '</div>';
      }
    }

    html += '</div>';
  }

  main.innerHTML = html;
}

// ─── Canvas Detail View ──────────────────────────────

function npcName(npcId) {
  if (!npcId) return '';
  const npc = (DATA.npcs || []).find(n => n.id === npcId);
  return npc ? npc.name : npcId.replace('npc_', '');
}

// ─── NPC Section Helpers ───
const NPC_SECTION_COLORS = ['#6b8afd', '#f472b6', '#fb923c', '#4ade80', '#22d3ee', '#a78bfa', '#facc15', '#f87171'];

function getNpcColor(npcIndex) {
  return NPC_SECTION_COLORS[npcIndex % NPC_SECTION_COLORS.length];
}

function getUniqueNpcs() {
  const sa = DATA.story_arc || {};
  const chapters = (sa.chapters || []).slice().sort((a, b) => a.order - b.order);
  const allNodes = sa.nodes || [];
  const seen = new Set();
  const ordered = [];
  for (const ch of chapters) {
    const chNodes = allNodes.filter(n => n.chapter === ch.id);
    for (const node of chNodes) {
      if (node.npc && !seen.has(node.npc)) {
        seen.add(node.npc);
        ordered.push(node.npc);
      }
    }
  }
  return ordered;
}

function isSingleNpcGame() {
  return getUniqueNpcs().length <= 1;
}

function getNodesForNpc(npcId) {
  return (DATA.story_arc.nodes || []).filter(n => n.npc === npcId);
}

function getOrphanNodes() {
  return (DATA.story_arc.nodes || []).filter(n => !n.npc);
}

function getChaptersForNodes(filteredNodes) {
  const sa = DATA.story_arc || {};
  const chapters = (sa.chapters || []).slice().sort((a, b) => a.order - b.order);
  const chapterIds = new Set(filteredNodes.map(n => n.chapter));
  return chapters.filter(ch => chapterIds.has(ch.id));
}

function toggleNpcSection(npcIdx) {
  const body = document.getElementById('npc-body-' + npcIdx);
  const arrow = document.getElementById('npc-arrow-' + npcIdx);
  if (body && arrow) {
    body.classList.toggle('open');
    arrow.classList.toggle('open');
  }
}

function formatMinutes(mins) {
  if (!mins) return '';
  if (mins < 60) return mins + 'min';
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m > 0 ? h + 'h ' + m + 'min' : h + 'h';
}

function posterUrl(filePath) {
  if (!filePath) return '';
  const parts = filePath.split('/');
  const clipFile = parts.pop();
  const posterFile = clipFile.replace('.mp4', '.jpg');
  parts.push('posters', posterFile);
  return '/games/' + encodeURI(DATA.project.id + '/videos/' + parts.join('/'));
}

function videoUrl(filePath) {
  if (!filePath) return '';
  return '/games/' + encodeURI(DATA.project.id + '/videos/' + filePath);
}

function buildColorMap(nodes) {
  const map = {};
  let idx = 0;
  nodes.forEach(node => {
    const eb = node.exit_block || {};
    (eb.choices || []).forEach(c => {
      if (c.targetType === 'node' && c.nodeId && !map[c.nodeId]) {
        map[c.nodeId] = { color: NODE_COLORS[idx % NODE_COLORS.length] };
        idx++;
      }
    });
  });
  return map;
}

function openCanvasDetail(canvasId) {
  DETAIL_CANVAS_ID = canvasId;
  renderMain();
  document.getElementById('main').scrollTop = 0;
  syncUrlParams();
}

function closeCanvasDetail() {
  DETAIL_CANVAS_ID = null;
  renderMain();
  syncUrlParams();
}

// ─── Review Status ──────────────────────────────

function reviewBadge(canvasId) {
  const r = REVIEW[canvasId];
  if (!r) return '';
  const labels = { approved: '\u2713 Approved', review: '\u2691 Review', disapproved: '\u2717 Disapproved' };
  return '<span class="rv-badge rv-' + r.status + '">' + (labels[r.status] || '') + '</span>';
}

function reviewCounts() {
  let approved = 0, review = 0, disapproved = 0, unmarked = 0;
  DATA.canvases.forEach(c => {
    const r = REVIEW[c.id];
    if (!r) unmarked++;
    else if (r.status === 'approved') approved++;
    else if (r.status === 'review') review++;
    else if (r.status === 'disapproved') disapproved++;
    else unmarked++;
  });
  return { approved, review, disapproved, unmarked };
}

function toggleReviewFilter(status) {
  REVIEW_FILTER = (REVIEW_FILTER === status) ? null : status;
  renderControls();
  renderMain();
  syncUrlParams();
}

function matchesReviewFilter(canvasId) {
  if (!REVIEW_FILTER) return true;
  const r = REVIEW[canvasId];
  if (REVIEW_FILTER === 'unmarked') return !r;
  return r && r.status === REVIEW_FILTER;
}

function toggleFlagFilter(flag) {
  FLAG_FILTER = (FLAG_FILTER === flag) ? null : flag;
  renderControls();
  renderMain();
  syncUrlParams();
}

function matchesFlagFilter(canvasId, storyNode) {
  if (!FLAG_FILTER) return true;
  const canvas = DATA.canvases.find(c => c.id === canvasId);
  if (canvas && canvas.flag_effects && canvas.flag_effects.includes(FLAG_FILTER)) return true;
  // For story canvases, also check the story arc node's linked_flag
  if (storyNode && storyNode.linked_flag === FLAG_FILTER) return true;
  if (!storyNode) {
    const arcNode = (DATA.story_arc?.nodes || []).find(n => n.linked_canvas === canvasId);
    if (arcNode && arcNode.linked_flag === FLAG_FILTER) return true;
  }
  return false;
}

async function setReviewStatus(canvasId, status, notes) {
  const current = REVIEW[canvasId];
  if (current && current.status === status && notes === undefined) {
    status = null;  // toggle off
  }
  const body = { game: DATA.project.id, canvas_id: canvasId, status: status, notes: notes || '' };
  await fetch(API + '/canvas-review/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (status === null) {
    delete REVIEW[canvasId];
  } else {
    REVIEW[canvasId] = { status: status, notes: notes || '', updated_at: new Date().toISOString() };
  }
  renderMain();
}

async function saveReviewNotes(canvasId, notes) {
  if (!REVIEW[canvasId]) return;
  REVIEW[canvasId].notes = notes;
  const body = { game: DATA.project.id, canvas_id: canvasId, status: REVIEW[canvasId].status, notes: notes };
  await fetch(API + '/canvas-review/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
}

function promptReviewNotes(canvasId) {
  const cur = REVIEW[canvasId];
  if (cur && cur.status === 'review') {
    setReviewStatus(canvasId, 'review');
    return;
  }
  const notesEl = document.getElementById('rv-notes-input');
  const notes = notesEl ? notesEl.value : '';
  setReviewStatus(canvasId, 'review', notes);
}

// ─── Tier Grouping Helpers ────────────────────────

const TIER_META = {
  base: { label: 'Establishing', desc: 'domestic, safe, no contact', color: '#22c55e' },
  t2:   { label: 'Flirtatious',  desc: 'lingering looks, light touches', color: '#4ade80' },
  t3:   { label: 'Tension',      desc: 'close proximity, suggestive', color: '#86efac' },
  t4:   { label: 'First Contact', desc: 'kissing, neck kisses', color: '#f59e0b' },
  t5:   { label: 'Clothed Grinding', desc: 'friction through clothes', color: '#ef4444' },
  t6:   { label: 'Manual',       desc: 'hands under clothes, fingering', color: '#dc2626' },
  t7:   { label: 'Oral',         desc: 'blowjob or cunnilingus', color: '#b91c1c' },
  t8:   { label: 'Full Sex',     desc: 'penetration', color: '#991b1b' },
  misc: { label: 'Miscellaneous', desc: 'special scenes, one-offs', color: '#6b7280' },
};

function extractTier(filePath) {
  const stem = filePath.split('/').pop().replace(/\.[^.]+$/, '');
  const m = stem.match(/_t(\d+)$/);
  if (m) return 't' + m[1];
  if (stem.endsWith('_base')) return 'base';
  return 'misc';
}

function setMediaGroupBy(mode) {
  MEDIA_GROUP_BY = mode;
  syncUrlParams();
  renderMain();
}

// ─── Media Review Helpers ─────────────────────────

function mediaServeUrl(item) {
  if (!item.serve_path) return '';
  return '/games/' + encodeURI(DATA.project.id + '/' + item.serve_path);
}

async function setMediaReviewStatus(b64Path, status) {
  const filePath = atob(b64Path);
  const current = MEDIA_REVIEW[filePath];
  if (current && current.status === status) {
    status = null;  // toggle off
  }
  const notesEl = document.getElementById('mr-notes-' + b64Path);
  const notes = notesEl ? notesEl.value : (current ? current.notes || '' : '');
  const body = { game: DATA.project.id, file_path: filePath, status: status, notes: notes };
  await fetch(API + '/media-review/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (status === null) {
    delete MEDIA_REVIEW[filePath];
  } else {
    MEDIA_REVIEW[filePath] = { status: status, notes: notes, updated_at: new Date().toISOString() };
  }
  renderMain();
}

async function saveMediaReviewNotes(b64Path, notes) {
  const filePath = atob(b64Path);
  const cur = MEDIA_REVIEW[filePath];
  if (!cur) return;
  cur.notes = notes;
  const body = { game: DATA.project.id, file_path: filePath, status: cur.status, notes: notes };
  await fetch(API + '/media-review/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
}

function matchesMediaFilter(filePath) {
  if (!MEDIA_FILTER) return true;
  const r = MEDIA_REVIEW[filePath];
  if (MEDIA_FILTER === 'unreviewed') return !r;
  return r && r.status === MEDIA_FILTER;
}

function toggleMediaFilter(status) {
  MEDIA_FILTER = (MEDIA_FILTER === status) ? null : status;
  syncUrlParams();
  renderMain();
}

// A pool row's preview: one small tile per clip currently in the folder, in the
// order the game will cycle them. Reuses the .cd-thumb grid the canvas-detail
// cards already use rather than inventing a second thumbnail style.
function renderPoolPreviewGrid(item) {
  const items = item.pool_items || [];
  const target = item.pool_target || 0;
  const count = items.length;

  // The shortfall is a SOFT signal: a 2-of-4 pool plays fine, it is just thinner
  // than intended. Say so plainly instead of flagging the row as broken.
  const short = target && count < target;
  let html = '<div class="mr-pool">';
  html += '<div class="mr-pool-head">';
  html += '<span class="mr-pool-count' + (count === 0 ? ' mr-pool-empty' : (short ? ' mr-pool-short' : '')) + '">'
        + count + ' of ' + target + '</span>';
  html += '<span class="mr-pool-dir">' + esc(item.pool_dir) + '/</span>';
  html += '</div>';

  if (count === 0) {
    html += '<div class="mr-pool-none">empty — nothing installed yet</div>';
  } else {
    html += '<div class="cd-media-row">';
    items.forEach((m, i) => {
      const url = '/games/' + encodeURI(DATA.project.id + '/' + m.serve_path);
      html += '<div class="cd-thumb-wrap">';
      if (m.actual_type === 'video') {
        // #t=0.1 forces the first frame to paint as a poster; preload="none"
        // renders a black rectangle, which makes a contact sheet useless.
        html += '<video class="cd-thumb" src="' + esc(url) + '#t=0.1" muted loop preload="metadata"'
              + ' onmouseover="this.play()" onmouseout="this.pause()"'
              + ' onclick="window.open(this.src)"></video>';
      } else {
        html += '<img class="cd-thumb" src="' + esc(url) + '" loading="lazy"'
              + ' onclick="window.open(this.src)" />';
      }
      html += '<div class="cd-thumb-desc">' + (i + 1) + '. ' + esc(m.actual_file) + '</div>';
      html += '</div>';
    });
    html += '</div>';
  }
  html += '</div>';
  return html;
}

function renderMediaReviewItem(item) {
  const filePath = item.file;
  const b64 = btoa(filePath);
  const review = MEDIA_REVIEW[filePath];
  const curStatus = review ? review.status : null;
  const curNotes = review ? (review.notes || '') : '';
  const statusClass = curStatus ? ' mr-status-' + curStatus : '';

  let html = '<div class="mr-item' + statusClass + '">';

  // Preview. A POOL is a folder of clips the game cycles one per visit, so the
  // question a reviewer needs answered is "does this SET work" — which one big
  // preview cannot show. Render every member as a small tile instead, in cycle
  // order, so a near-duplicate or an off-tone clip is visible at a glance.
  if (item.pool_dir) {
    html += renderPoolPreviewGrid(item);
  } else {
    const url = mediaServeUrl(item);
    if (url) {
      if (item.actual_type === 'video') {
        html += '<video class="mr-preview" src="' + esc(url) + '" controls preload="metadata"></video>';
      } else {
        html += '<img class="mr-preview-img" src="' + esc(url) + '" loading="lazy" onclick="window.open(this.src)" />';
      }
    }
  }

  // Body
  html += '<div class="mr-item-body">';

  // Type badge + actual file
  html += '<div class="mr-item-header">';
  html += '<span class="mm-type-badge ' + esc(item.type) + '">' + esc(item.type.replace(/_/g, ' ')) + '</span>';
  if (item.actual_file) {
    html += '<span class="mm-actual-file">' + esc(item.actual_file) + '</span>';
  }
  if (item.actual_type && item.actual_type !== item.type) {
    html += '<span class="mm-type-switch">renders as ' + esc(item.actual_type) + '</span>';
  }
  html += '</div>';
  html += '<div class="mr-item-file">' + esc(filePath) + '</div>';

  if (item.description) {
    html += '<div class="mr-item-desc">' + esc(item.description) + '</div>';
  }

  // Review controls
  html += '<div class="mr-controls">';
  html += '<button class="mr-btn' + (curStatus === 'approved' ? ' active-approved' : '') + '" onclick="setMediaReviewStatus(\'' + b64 + '\',\'approved\')">&#10003; Approve</button>';
  html += '<button class="mr-btn' + (curStatus === 'disapproved' ? ' active-disapproved' : '') + '" onclick="setMediaReviewStatus(\'' + b64 + '\',\'disapproved\')">&#10007; Disapprove</button>';
  if (curStatus) {
    html += '<span class="mr-status-label sl-' + curStatus + '">' + curStatus + '</span>';
  }
  html += '</div>';

  // Notes textarea (always visible)
  html += '<textarea class="mr-notes" id="mr-notes-' + esc(b64) + '" placeholder="Notes..." onblur="saveMediaReviewNotes(\'' + b64 + '\', this.value)">' + esc(curNotes) + '</textarea>';

  html += '</div></div>';
  return html;
}

async function removeClipAudio(filePath, btn) {
  const parts = filePath.split('/');
  const collection = parts[0];
  const video_stem = parts[2];
  const clip_filename = parts[3];
  btn.disabled = true;
  btn.textContent = '...';
  try {
    const res = await fetch('/api/v1/dev/video-browser/remove-audio', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game: DATA.project.id, collection, video_stem, clip_filename })
    });
    const data = await res.json();
    if (data.success) {
      btn.textContent = 'Done';
      btn.className = 'cd-noaud-btn done';
    } else {
      btn.textContent = 'NoAud';
      btn.disabled = false;
      alert(data.error || 'Failed');
    }
  } catch(e) {
    btn.textContent = 'NoAud';
    btn.disabled = false;
    alert('Request failed');
  }
}

function renderCanvasDetail() {
  const main = document.getElementById('main');
  const canvas = DATA.canvases.find(c => c.id === DETAIL_CANVAS_ID);
  if (!canvas) {
    main.innerHTML = '<div class="loading">Canvas not found</div>';
    return;
  }

  const nodes = canvas.nodes || [];
  const colorMap = buildColorMap(nodes);

  let html = '<button class="cd-back-btn" onclick="closeCanvasDetail()">&larr; Back to ' + esc(VIEW_MODE) + ' view</button>';

  // Review controls
  const curStatus = REVIEW[canvas.id] ? REVIEW[canvas.id].status : null;
  const curNotes = REVIEW[canvas.id] ? REVIEW[canvas.id].notes || '' : '';
  html += '<div class="rv-controls">';
  html += '<button class="rv-btn' + (curStatus === 'approved' ? ' active-approved' : '') + '" onclick="setReviewStatus(\'' + esc(canvas.id) + '\',\'approved\')">&#10003; Approve</button>';
  html += '<button class="rv-btn' + (curStatus === 'review' ? ' active-review' : '') + '" onclick="promptReviewNotes(\'' + esc(canvas.id) + '\')">&#9873; Review</button>';
  html += '<button class="rv-btn' + (curStatus === 'disapproved' ? ' active-disapproved' : '') + '" onclick="setReviewStatus(\'' + esc(canvas.id) + '\',\'disapproved\')">&#10007; Disapprove</button>';
  html += '</div>';
  html += '<textarea class="rv-notes' + (curStatus === 'review' ? ' visible' : '') + '" id="rv-notes-input" placeholder="Review notes...">' + esc(curNotes) + '</textarea>';

  // Header
  html += '<div class="cd-canvas-header">';
  html += '<div class="cd-canvas-name">' + esc(canvas.name) + '</div>';
  if (canvas.description) html += '<div class="cd-canvas-desc">' + esc(canvas.description) + '</div>';
  html += '<div class="cd-canvas-meta">';
  if (canvas.location) html += '<span class="cd-meta-tag">\uD83D\uDCCD ' + esc(locName(canvas.location)) + '</span>';
  if (canvas.npc) html += '<span class="cd-meta-tag">\uD83D\uDC64 ' + esc(npcName(canvas.npc)) + '</span>';
  if (canvas.schedule) html += '<span class="cd-meta-tag">\uD83D\uDD52 ' + esc(canvas.schedule.start_time) + '-' + esc(canvas.schedule.end_time) + '</span>';
  html += '<span class="cd-meta-tag">' + nodes.length + ' nodes</span>';
  if (canvas.is_repeatable) html += '<span class="cd-meta-tag">\u21BB repeatable</span>';
  else html += '<span class="cd-meta-tag">\u2605 story</span>';
  if (canvas.max_triggers_per_day) html += '<span class="cd-meta-tag"><span class="daily-limit-badge">' + canvas.max_triggers_per_day + 'x/day</span></span>';
  html += '</div>';

  // Trigger conditions
  if (canvas.trigger_conditions && canvas.trigger_conditions.length > 0) {
    html += '<div style="margin-top:10px"><span style="font-size:10px;color:#666;text-transform:uppercase">Requires (' + esc(canvas.trigger_logic) + '):</span> ';
    html += renderCondPills(canvas.trigger_conditions, canvas.trigger_logic);
    html += '</div>';
  }
  html += '</div>';

  // Nodes
  nodes.forEach((node, ni) => {
    html += renderNodeCard(node, ni, colorMap);
  });

  main.innerHTML = html;

  // Wire up notes auto-save on blur
  const notesEl = document.getElementById('rv-notes-input');
  if (notesEl) {
    notesEl.addEventListener('blur', function() {
      if (REVIEW[canvas.id] && REVIEW[canvas.id].status === 'review') {
        saveReviewNotes(canvas.id, this.value);
      }
    });
  }
}

function renderNodeCard(node, index, colorMap) {
  const isEntry = (index === 0);
  let html = '<div class="cd-node ' + (isEntry ? 'cd-entry' : 'cd-child') + '">';

  // Header
  html += '<div class="cd-node-header">';
  if (colorMap[node.id]) {
    html += '<span class="cd-color-dot" style="background:' + colorMap[node.id].color + '"></span>';
  }
  html += '<span class="cd-node-name">' + esc(node.name) + '</span>';
  html += '<span style="font-size:10px;color:#555;margin-left:auto">' + esc(node.id) + '</span>';
  html += '</div>';

  // Blocks — group consecutive videos into thumbnail rows
  if (node.blocks && node.blocks.length > 0) {
    html += '<div class="cd-blocks">';
    let videoQueue = [];
    function flushVideos() {
      if (videoQueue.length === 0) return;
      html += '<div class="cd-media-row">';
      videoQueue.forEach(v => {
        const pUrl = posterUrl(v.file);
        const vUrl = videoUrl(v.file);
        html += '<div class="cd-thumb-wrap">';
        html += '<video class="cd-thumb" poster="' + pUrl + '" src="' + vUrl + '" controls preload="none"></video>';
        html += '<div style="font-size:11px;color:#8af;font-family:monospace;padding:2px 0">' + esc(v.file.split('/').pop()) + '</div>';
        html += '<div class="cd-thumb-desc">' + esc(v.description || '') + '</div>';
        html += '<button class="cd-noaud-btn" onclick="removeClipAudio(\'' + esc(v.file) + '\', this)">NoAud</button>';
        html += '</div>';
      });
      html += '</div>';
      videoQueue = [];
    }
    node.blocks.forEach(b => {
      if (b.type === 'video') {
        videoQueue.push(b);
        return;
      }
      flushVideos();
      html += '<div class="cd-block-item">';
      if (b.type === 'paragraph') {
        html += '<span class="cd-block-icon">\u00B6</span>';
        html += '<span class="cd-block-text">' + esc(b.text) + '</span>';
      } else if (b.type === 'image') {
        html += '<span class="cd-block-icon">\uD83D\uDDBC</span>';
        html += '<span class="cd-block-text" style="color:#60a5fa">[IMAGE] ' + esc(b.file || '') + '</span>';
      } else if (b.type === 'dialog') {
        html += '<span class="cd-block-icon">\uD83D\uDCAC</span>';
        const speaker = b.npcId ? npcName(b.npcId) : (b.speaker || '?');
        html += '<span class="cd-block-text"><strong>' + esc(speaker) + ':</strong> "' + esc(b.text) + '"</span>';
      } else {
        html += '<span class="cd-block-icon">?</span>';
        html += '<span class="cd-block-text">' + esc(b.type) + '</span>';
      }
      html += '</div>';
    });
    flushVideos();
    html += '</div>';
  }

  // Exit block
  const eb = node.exit_block || {};
  if (eb.type === 'choices' && eb.choices) {
    html += '<div class="cd-exit">';
    html += '<div class="cd-exit-label">Choices</div>';
    eb.choices.forEach(c => {
      html += renderDetailChoice(c, colorMap);
    });
    html += '</div>';
  } else if (eb.type === 'location') {
    html += '<div class="cd-exit">';
    html += '<div class="cd-exit-label">Exit</div>';
    html += renderLocationExit(eb);
    html += '</div>';
  }

  html += '</div>';
  return html;
}

function renderDetailChoice(choice, colorMap) {
  let html = '<div class="cd-choice">';

  // Color dot or EXIT badge
  if (choice.targetType === 'node' && choice.nodeId) {
    const cm = colorMap[choice.nodeId];
    if (cm) {
      html += '<span class="cd-color-dot" style="background:' + cm.color + ';margin-top:4px"></span>';
    }
  } else if (choice.targetType === 'trigger') {
    html += '<span class="cd-exit-badge">EXIT</span>';
  }

  html += '<div style="flex:1">';
  html += '<div class="cd-choice-text">' + esc(choice.text || '(no text)') + '</div>';

  // Target
  if (choice.targetType === 'node' && choice.nodeId) {
    html += '<div class="cd-choice-target">\u2192 ' + esc(choice.nodeId) + '</div>';
  }

  // Conditions
  const cond = choice.conditions;
  if (cond && cond.items && cond.items.length > 0) {
    html += '<div class="cd-choice-meta">';
    html += renderCondPills(cond.items, cond.logic || 'AND');
    html += '</div>';
  }

  // Effects + time
  const effects = choice.effects || [];
  const flagEffects = choice.flagEffects || [];
  if (effects.length > 0 || flagEffects.length > 0 || choice.time_progression_minutes) {
    html += '<div class="cd-choice-meta">';
    effects.forEach(e => {
      const sign = (e.op === 'add' && e.value > 0) ? '+' : '';
      html += '<span class="cd-effect-pill">' + sign + e.value + ' ' + esc(e.trait || '') + '</span>';
    });
    flagEffects.forEach(fe => {
      html += '<span class="flag-set-pill">sets: ' + esc(fe.flag || '') + '</span>';
    });
    if (choice.time_progression_minutes) {
      html += '<span class="cd-time-pill">\uD83D\uDD52 ' + formatMinutes(choice.time_progression_minutes) + '</span>';
    }
    html += '</div>';
  }

  html += '</div></div>';
  return html;
}

function renderLocationExit(eb) {
  const config = eb.config || {};
  let html = '<div class="cd-loc-exit">';
  html += '<div class="cd-loc-exit-name">' + esc(eb.text || 'Continue') + '</div>';
  html += '<div class="cd-loc-exit-meta">';

  if (config.destinationType === 'trigger') {
    html += '<span class="cd-exit-badge">EXIT</span>';
  } else if (config.locationId) {
    html += '<span class="cd-meta-tag">\u2192 ' + esc(locName(config.locationId)) + '</span>';
  }

  (config.effects || []).forEach(e => {
    const sign = (e.op === 'add' && e.value > 0) ? '+' : '';
    html += '<span class="cd-effect-pill">' + sign + e.value + ' ' + esc(e.trait || '') + '</span>';
  });
  (config.flagEffects || []).forEach(fe => {
    html += '<span class="flag-set-pill">sets: ' + esc(fe.flag || '') + '</span>';
  });
  if (config.time_progression_minutes) {
    html += '<span class="cd-time-pill">\uD83D\uDD52 ' + formatMinutes(config.time_progression_minutes) + '</span>';
  }

  html += '</div></div>';
  return html;
}

function toggleChapter(ci) {
  const body = document.getElementById('chbody-' + ci);
  const arrow = document.getElementById('arrow-' + ci);
  if (body && arrow) {
    body.classList.toggle('open');
    arrow.classList.toggle('open');
  }
}

function esc(s) {
  if (s == null) return '';
  const d = document.createElement('div');
  d.textContent = String(s);
  return d.innerHTML;
}

init();
</script>
</body>
</html>"""
    response = HttpResponse(html, content_type="text/html")
    response["Cache-Control"] = "no-store"
    return response


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("", page, name="game_review_page"),
    path("games", list_games, name="game_review_games"),
    path("load", load_game, name="game_review_load"),
    path("canvas-review/", canvas_review, name="game_review_canvas_review"),
    path("media-download", media_download, name="game_review_media_download"),
    path("media-review/", media_review, name="game_review_media_review"),
]
