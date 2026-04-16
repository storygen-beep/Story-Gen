# Game-Review API Contract

The find-media skill uses `GET /api/v1/dev/game-review/load` as the authoritative source for missing-media enumeration. This file documents the endpoint and its response shape so the skill can stop rediscovering what the backend already knows.

Source implementation: `api/v1/game_review.py:214-394` (`_extract_missing_media`), `api/v1/game_review.py:2926-2933` (`urlpatterns`).

## Endpoint

```
GET http://localhost:8000/api/v1/dev/game-review/load?game=<game_name>
```

**No trailing slash** on `load`. The URL pattern at `api/v1/game_review.py:2929` is `path("load", load_game, ...)`. Requesting `/load/` returns 404.

Requires: Django dev server running on localhost:8000, game folder exists at `games/<game_name>/`.

## Response — top-level keys

JSON body, ~474KB typical for a populated game. Keys:

| Key | Type | Used by find-media? |
|---|---|---|
| `project` | object | No — informational |
| `player` | object | No |
| `npcs` | array of objects | **Yes** — for `dating_profile_photo` synthesis (look up age, traits by id) |
| `locations` | array | No — location entries are already expanded into `missing_media` / `found_media` as `location_image` |
| `canvases` | array | No — canvas blocks are already expanded into `missing_media` / `found_media` as `image` / `video` |
| `story_arc` | object | No |
| `starting_canvas` | string | No |
| **`missing_media`** | array | **Yes** — primary input |
| **`found_media`** | array | Optional — for dedup awareness and progress tracking |

## `missing_media` entry schema

Each entry has exactly 7 fields (verified empirically against under_one_roof):

```json
{
  "file": "social/jess_gym_1.jpg",
  "type": "social_post_image",
  "category": "Social Media",
  "description": "@jessicafit_: 5am grind. no days off. #legday",
  "search_queries": [],
  "canvas_id": "phone",
  "order": 147
}
```

| Field | Type | Notes |
|---|---|---|
| `file` | string | TOML-declared path (relative to game root). Extension is advisory — the actual saved extension comes from the source URL (see `references/api_behavior.md`). |
| `type` | string | One of 6 values — see §Type vocabulary below |
| `category` | string | UI grouping — see §Category vocabulary below |
| `description` | string | Human-readable context. Shape varies by type — see §Description shapes |
| `search_queries` | array of strings | **Can be empty.** The API faithfully preserves what the TOML declared — it does not strip or synthesize. If empty, the find-media skill synthesizes queries during PLAN (see `query_rewriting.md` §Synthesizing queries). |
| `canvas_id` | string | Real canvas id for canvas blocks, or literal `"navigation"` / `"wardrobe"` / `"phone"` for non-canvas items |
| `order` | integer | UI sort order, preserves the TOML-declaration order |

## `found_media` entry schema

Found entries have the same 7 fields plus 3 more:

```json
{
  "file": "locations/property.jpg",
  "type": "location_image",
  "category": "Locations",
  "description": "Navigation image for The Harmon Property",
  "search_queries": ["rural American contractor property ..."],
  "canvas_id": "navigation",
  "order": 0,
  "actual_file": "property.jpg",
  "actual_type": "image",
  "serve_path": "videos/locations/property.jpg"
}
```

| Field | Type | Notes |
|---|---|---|
| `actual_file` | string | Filename of the file that was found (includes actual extension, which may differ from `file`'s declared extension) |
| `actual_type` | string | `"image"` or `"video"` based on the actual file's extension |
| `serve_path` | string | Path relative to game root for URL construction |

## Type vocabulary

Six values, each with a single intended source in the TOML:

| Type | TOML source | Find-media pipeline |
|---|---|---|
| `image` | Canvas block with `type = "image"` | Standard SFW pipeline if tier ≤ t3, NSFW otherwise |
| `video` | Canvas block with `type = "video"` | NSFW pipeline (these are always t5+ in practice) |
| `location_image` | `[[locations]]` entries | SFW always, wide establishing shots |
| `clothing_image` | `[[clothing]]` entries | SFW always, flat-lay product style |
| `social_post_image` | `[[phone.posts]]` entries | SFW lifestyle (unless caption explicitly escalates) |
| `dating_profile_photo` | `[[phone.profiles]]` entries (per-photo in `photos` list) | SFW selfie style |

## Category vocabulary

| Category | Contains |
|---|---|
| `Activities` | Canvas image/video blocks with `"activities"` in path |
| `Story` | Canvas image/video blocks with `"story"` or `"opening"` in path |
| `Locations` | All `location_image` entries |
| `Clothing` | All `clothing_image` entries |
| `Social Media` | `social_post_image` + `dating_profile_photo` |
| `Other` | Canvas image/video blocks not matching the above path patterns |

## Description shapes by type

| Type | Shape | Extraction cues |
|---|---|---|
| `image` / `video` | Whatever `props.description` says | Narrative context from surrounding TOML paragraphs |
| `location_image` | `"Navigation image for {name}"` | Location name |
| `clothing_image` | `"{name} ({slot})"` | Item name + slot (top/bottom/etc) |
| `social_post_image` | `"{poster_name}: {caption}"` | Poster persona + caption hashtags/nouns |
| `dating_profile_photo` | `"Dating profile photo for {npc_name or id}"` | NPC lookup via response's `npcs` array for age/traits |

## Verified behaviors (non-obvious)

**1. Empty `search_queries` are preserved, not stripped.**
Source: empirical test against under_one_roof — all 34 phone posts have `search_queries = []` in the API response because the TOML declared no queries for them. The API does not invent queries, does not refuse to list the item. The skill synthesizes during PLAN.

**2. Items without the declared path field are silently skipped.**
Source: `game_review.py:254`, `:286`, `:323`, `:348`, `:373` — all check `if not image: continue` (or equivalent) before emitting the entry. Example: under_one_roof has 60 `[[clothing]]` entries but 0 declare an `image` field, so 0 clothing items appear in either `missing_media` or `found_media`. The API is a faithful reader, not a schema auditor. Catching "should have but doesn't" is a separate concern.

**3. `find_file` checks three roots in order: `output/`, game root, `videos/`.**
Source: `game_review.py:234-240`. Search order means "found" status can include stale copies in `output/` (from a previous `package_from_toml` run) even when the source `videos/` file was deleted. For find-media this doesn't matter — the `missing_media` list already confirmed the file is absent from ALL three roots. But when consuming `found_media` / `serve_path`, be aware `output/` wins first.

**4. Canvas categorization from file path substring.**
Source: `game_review.py:290-298` — looks for `"activities"`, `"story"` or `"opening"`, `"locations"` substring in the file path to assign the category. So a canvas block at `story/scene_kiss.jpg` → category `Story`. A block at `activities/activity_dinner.jpg` → `Activities`. Anything else → `Other`. The `canvas_id` field carries the actual canvas UUID/slug separately.

**5. `starting_canvas` and other routing fields do not appear in media lists.**
Source: the extraction function only visits the 5 documented TOML structures. Flags, triggers, choices, clothing unlocks — none contain media references so none contribute to missing/found.

## Invocation pattern for find-media

```bash
# Fetch
mkdir -p games/<game>/.find-media
curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=<game>" > games/<game>/.find-media/game_review.json

# Extract missing count
jq '.missing_media | length' games/<game>/.find-media/game_review.json

# Validator against the payload (after synthesizing queries for empty entries)
python .claude/skills/find-media/scripts/validate_queries.py \
  --from-api-json games/<game>/.find-media/game_review.json
```

The skill's §Decision tree step 3 does the curl. The `.find-media/game_review.json` file is the durable input for the entire run — SCOPE reads it, PLAN synthesizes into it, RETRIEVE works from it.

## Offline fallback

When Django isn't running, the validator falls back to walker mode:

```bash
python .claude/skills/find-media/scripts/validate_queries.py \
  --toml games/<game>/toml_phases/6_final_game.toml
```

This mode misses locations (wrong key name), clothing, phone posts without queries, and phone profile photo lists — same gap that motivated the API-first design. Use only when the server is unreachable; re-run with `--from-api-json` once the server is back.
