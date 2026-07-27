# Game-Review API Contract

The find-media skill uses `GET /api/v1/dev/game-review/load` as the authoritative source for missing-media enumeration. This file documents the endpoint and its response shape so the skill can stop rediscovering what the backend already knows.

Source implementation: `api/v1/game_review.py:269-512` (`_extract_missing_media`), `api/v1/game_review.py:3045-3052` (`urlpatterns`).

## Endpoint

```
GET http://localhost:8000/api/v1/dev/game-review/load?game=<game_name>
```

**No trailing slash** on `load`. The URL pattern at `api/v1/game_review.py:3048` is `path("load", load_game, name="game_review_load")`. Requesting `/load/` returns 404. (Sibling routes are inconsistent about this — `canvas-review/` and `media-review/` DO take a trailing slash, `games`, `load` and `media-download` do not. Copy the exact form.)

**Where `game` goes: follow the HTTP verb, not the app.** On `game-review/*` it is a query
param on the GETs (`load`, `games`, and the GET halves of `canvas-review/` /
`media-review/` — `game_review.py:538`, `:619`, `:675`) and a JSON **body** field on the
POSTs (`canvas-review/`, `media-review/`, `media-download` — `:640`, `:696`, `:738`). On the
media-finder side it is a body field on the POSTs and a query param on `options/list` (GET).

Requires: Django dev server running on localhost:8000, game folder exists at `games/<game_name>/`.

## Response — top-level keys

JSON body, ~474KB typical for a populated game. Keys:

| Key | Type | Used by find-media? |
|---|---|---|
| `project` | object | No — informational |
| `player` | object | No |
| `npcs` | array of objects | **Yes** — for `dating_profile_photo` / `portrait_image` synthesis (look up an NPC by id). Each entry carries **only** `id`, `name`, `core_traits` (`game_review.py:576-580`) — no age, no description. For anything richer, read the game's TOML. |
| `locations` | array | No — location entries are already expanded into `missing_media` / `found_media` as `location_image` |
| `canvases` | array | No — canvas blocks are already expanded into `missing_media` / `found_media` as `image` / `video` |
| `story_arc` | object | No |
| `starting_canvas` | string | No |
| **`missing_media`** | array | **Yes** — primary input |
| **`found_media`** | array | Optional — for dedup awareness and progress tracking |

## `missing_media` entry schema

Every entry has these 7 fields. Canvas image/video entries carry an **8th**, `canvas_name`
(`game_review.py:365`) — only that one type gets it, so treat it as optional and don't key
your schema off a fixed field count.

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
| `type` | string | One of 7 values — see §Type vocabulary below |
| `category` | string | UI grouping — see §Category vocabulary below |
| `description` | string | Human-readable context. Shape varies by type — see §Description shapes |
| `search_queries` | array of strings | **Can be empty.** The API faithfully preserves what the TOML declared — it does not strip or synthesize. If empty, the find-media skill synthesizes queries during PLAN (see `query_rewriting.md` §Synthesizing queries). The TOML key it reads differs by type — see the note below. |
| `canvas_id` | string | Real canvas id for canvas blocks, or literal `"navigation"` / `"wardrobe"` / `"phone"` / `"portraits"` for non-canvas items |
| `order` | integer | UI sort order, preserves the TOML-declaration order |
| `canvas_name` | string | **Canvas image/video entries only.** The canvas's display name. |

**`search_queries` reads a different TOML key per type**: `image_search_queries` for
locations and clothing (`game_review.py:319`, `:388`); `search_queries` for canvas blocks
and phone posts (`:363`, `:414`); `search_queries` on the **profile**, not the photo, for
`dating_profile_photo` (`:438`) — so every photo of one profile shares one query list;
and always `[]` for portraits (`:470`, hard-coded — portraits are never TOML-queried).

## `found_media` entry schema

Found entries have the same 7 fields plus 3 more:

```json
{
  "file": "locations/property.jpg",
  "type": "location_image",
  "category": "Locations",
  "description": "Navigation image for The Harmon Property",
  "search_queries": ["rural American contractor property wide shot"],
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

Seven values, each with a single intended source in the TOML. This is the complete set —
`_iter_media_blocks` yields only blocks whose `type` is exactly `image` or `video`
(`game_review.py:256`), and the other five types are assigned as literals.

That walk is no longer flat: `_iter_media_blocks` recurses into `group` children,
`block_pool` `props.blocks`, and `cascade` `props.beats[*].blocks`
(`game_review.py:260-266`), mirroring the generator's own descent. Nested media — sex-loop
finishers, opening cascades, random-still pools — used to be invisible here, which is how
a game could report "0 missing" and still ship art-less hot scenes. If you remember that
blind spot, it is closed.

| Type | TOML source | Find-media treatment |
|---|---|---|
| `image` | Canvas block with `type = "image"` | SFW vocabulary if tier ≤ t3, adult otherwise |
| `video` | Canvas block with `type = "video"` | Adult vocabulary (these are t5+ in practice) |
| `location_image` | `[[locations]]` entries | SFW always, wide establishing shots |
| `clothing_image` | `[[clothing]]` entries | SFW always, flat-lay product style |
| `social_post_image` | `[[phone.posts]]` entries | SFW lifestyle (unless caption explicitly escalates) |
| `dating_profile_photo` | `[[phone.profiles]]` entries (per-photo in `photos` list) | SFW selfie style |
| `portrait_image` | NPC `portrait`, `[player_portrait]` `*_image` keys + its `outfits[].image`, and `image_select` customization option images | **SFW always** — a portrait is UI chrome (a face in the sidebar), never a scene, no matter how explicit the game is |

## Portraits are enumerated (they used to not be)

`_extract_missing_media` step 6 (`game_review.py:452-510`, helper `_add_portrait`) walks
three portrait sources that the endpoint was blind to for most of its life:

- `[[npcs]] portrait` → `"Portrait for {name}"` (`:484-486`)
- `[player_portrait]` — every key ending `_image`, plus each `outfits[].image` (`:488-499`)
- `[player] customization_fields` where `type == "image_select"` → each `options[].image` (`:501-510`)

All land as `type: "portrait_image"`, `category: "Portraits"`, `canvas_id: "portraits"`,
`search_queries: []`. Before this existed, a new NPC's face surfaced only as a
`File not found` line during packaging, which is how faces kept shipping absent. Do not
build a separate portrait-enumeration path — the API covers it; synthesize the query.

## Category vocabulary

| Category | Contains |
|---|---|
| `Activities` | Canvas image/video blocks with `"activities"` in the file path |
| `Story` | Canvas image/video blocks with `"story"` or `"opening"` in the file path |
| `Locations` | All `location_image` entries — **plus** canvas image/video blocks with `"locations"` in the file path (`game_review.py:353-354`), so this bucket is not type-pure |
| `Clothing` | All `clothing_image` entries |
| `Social Media` | `social_post_image` + `dating_profile_photo` |
| `Portraits` | All `portrait_image` entries |
| `Other` | Canvas image/video blocks not matching the above path patterns |

## Description shapes by type

| Type | Shape | Extraction cues |
|---|---|---|
| `image` / `video` | Whatever `props.description` says | Narrative context from surrounding TOML paragraphs |
| `location_image` | `"Navigation image for {name}"` | Location name |
| `clothing_image` | `"{name} ({slot})"` | Item name + slot (top/bottom/etc) |
| `social_post_image` | `"{poster_name}: {caption}"` | Poster persona + caption hashtags/nouns |
| `dating_profile_photo` | `"Dating profile photo for {npc_name or id}"` | NPC lookup via the response's `npcs` array for name + `core_traits` |
| `portrait_image` | `"Portrait for {name}"` / `"Player portrait — {state}"` / `"{field label} — {option}"` | The state or option name IS the brief — `"Player portrait — bottomless"` means exactly that |

## Verified behaviors (non-obvious)

**1. Empty `search_queries` are preserved, not stripped.**
Source: empirical test against under_one_roof — all 34 phone posts have `search_queries = []` in the API response because the TOML declared no queries for them. The API does not invent queries, does not refuse to list the item. The skill synthesizes during PLAN.

**2. Items without the declared path field are silently skipped.**
Source: `game_review.py:312`, `:344`, `:381`, `:406`, `:431` — all check `if not image: continue` (or equivalent) before emitting the entry. Example: under_one_roof has 60 `[[clothing]]` entries but 0 declare an `image` field, so 0 clothing items appear in either `missing_media` or `found_media`. The API is a faithful reader, not a schema auditor. Catching "should have but doesn't" is a separate concern.

**3. `find_file` checks `output/` and the game root always, `videos/` conditionally.**
Source: `game_review.py:292-298` (inside `find_file`). The root list is built as
`[game_dir/"output", game_dir]`, and `game_dir/"videos"` is appended **only when the
declared path does not already start with `videos/`** — a path that carries the prefix is
resolved against the game root, where the same `videos/…` segment does the work. The
consequence: `output/` wins first, so "found" status can include a stale copy left by a
previous `package_from_toml` run even when the source `videos/` file was deleted. For
find-media that doesn't matter — the `missing_media` list already confirmed the file is
absent from every root that was searched. But when consuming `found_media` / `serve_path`,
be aware you may be looking at the packaged copy, not the source.

**4. Canvas categorization from file path substring.**
Source: `game_review.py:348-356` — looks for `"activities"`, `"story"` or `"opening"`, `"locations"` substring in the file path to assign the category. So a canvas block at `story/scene_kiss.jpg` → category `Story`. A block at `activities/activity_dinner.jpg` → `Activities`. Anything else → `Other`. The `canvas_id` field carries the actual canvas UUID/slug separately.

**5. `starting_canvas` and other routing fields do not appear in media lists.**
Source: the extraction function visits exactly six TOML structures — locations, canvas
blocks, clothing, phone posts, phone profile photos, portraits — and nothing else. Flags,
triggers, choices, clothing unlocks contain no media references, so none contribute to
missing/found.

**6. Three phone media keys are NOT enumerated — the one real blind spot.**
The generator resolves all three through the same `_find_media_file`, but
`_extract_missing_media` never walks them, so they are invisible to `missing_media`, to the
review page, and to this skill:

| TOML key | Generator handling (`generators/v2.py`) |
|---|---|
| `[phone] apps[].icon` | resolved at `v2.py:1271`; **no missing-entry emitted at all** — a broken icon is silent everywhere |
| `[phone] daily_topics[].image` | resolved at `v2.py:1331`; on miss emits `type: "phone_chat_photo"` into the generator's own `missing_media` |
| `[phone] gallery_items[].image` | resolved at `v2.py:1348`; on miss emits `type: "phone_gallery_image"` into the generator's own `missing_media` |

The two generator-side types are the generator's list, not this endpoint's — neither can
ever appear in a `game-review/load` response, because the type vocabulary above is the
complete set. So if a game declares phone gallery items, photo-action images, or app icons,
grep its TOML for those keys directly; the API will not tell you they are absent.
(Portraits are **not** in this bucket — they used to be, and are enumerated now; see
§Portraits are enumerated.)

## Invocation pattern for find-media

```bash
# Fetch
mkdir -p games/<game>/.find-media
curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=<game>" > games/<game>/.find-media/game_review.json

# Extract missing count
jq '.missing_media | length' games/<game>/.find-media/game_review.json

# Validator against the payload (after synthesizing queries for empty entries)
python3 .claude/skills/find-media/scripts/validate_queries.py \
  --from-api-json games/<game>/.find-media/game_review.json
```

The skill's §Decision tree step 3 does the curl. The `.find-media/game_review.json` file is the durable input for the entire run — SCOPE reads it, PLAN synthesizes into it, SEARCH and STOCK work from it.

## Offline fallback

When Django isn't running, the validator falls back to walker mode:

```bash
python3 .claude/skills/find-media/scripts/validate_queries.py \
  --toml games/<game>/toml_phases/<N>_final_game.toml
```

`<N>` is the highest numeric phase prefix actually present in `toml_phases/` — `7_` on
current games, `6_` on older ones. That is the same file the backend resolves
(`_resolve_final_toml`, `game_review.py`); `ls games/<game>/toml_phases/*_final_game.toml`
if you're unsure.

This mode misses locations (wrong key name), clothing, phone posts without queries, and phone profile photo lists — same gap that motivated the API-first design. Use only when the server is unreachable; re-run with `--from-api-json` once the server is back.
