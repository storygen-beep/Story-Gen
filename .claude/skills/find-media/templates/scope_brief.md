# Scope Brief — `{{item_id}}`

Fill this template during SCOPE phase. Write to `games/{{game}}/.find-media/scope/{{item_id}}.md`. Source for every field: the API response at `games/{{game}}/.find-media/game_review.json` (see `references/game_review_api.md`).

## Identity

- **item_id**: `{{item_id}}` (derived from `file` field, filesystem-safe)
- **file_path**: `{{file}}` (verbatim from API)
- **type**: `{{type}}` — one of `image`, `video`, `location_image`, `clothing_image`, `social_post_image`, `dating_profile_photo`
- **category**: `{{category}}` — one of `Activities`, `Story`, `Locations`, `Clothing`, `Social Media`, `Other`
- **canvas_id**: `{{canvas_id}}`
- **order**: `{{order}}`
- **tier**: `{{tier}}` (for canvas items: infer from filename `_tN` suffix; for location/clothing/social_post/dating_profile: always `base`)
- **content_rating**: `{{sfw|nsfw}}` (location/clothing/social_post/dating_profile: always `sfw`)
- **required_format**: (from `scripts/tier_format_check.py` rules — tier-driven for canvas items, `.jpg` for static non-canvas categories)

## Narrative context — branches by type

Fill ONE of the following subsections based on `{{type}}`.

### If `type` is `image` or `video` (canvas block)

Read the TOML at `games/{{game}}/toml_phases/6_final_game.toml`. Find the canvas block by matching `file = "{{file}}"` inside the canvas with id `{{canvas_id}}`. Extract the 2–3 narrative paragraphs/dialog blocks that appear BEFORE and AFTER this block in the same node.

**Before:**
> {{before_paragraph_1}}
>
> {{before_paragraph_2}}

**After:**
> {{after_paragraph_1}}
>
> {{after_paragraph_2}}

### If `type` is `social_post_image`

Description shape: `"@poster_name: caption"`.

- **Poster**: `{{poster_name}}` (the `@handle` from description)
- **Caption**: `{{caption}}` (everything after the first `:`)
- **Hashtags** (extracted from caption): `{{hashtags}}`
- **Content cues** (nouns/verbs from caption that ground the scene): `{{cues}}`

### If `type` is `location_image`

Description shape: `"Navigation image for {location_name}"`.

- **Location name**: `{{location_name}}`
- **Location TOML metadata** (read from `games/{{game}}/toml_phases/` — find `[[locations]]` entry with matching `image` field): indoor/outdoor, type, tone

### If `type` is `clothing_image`

Description shape: `"{item_name} ({slot})"`.

- **Item name**: `{{item_name}}`
- **Slot**: `{{slot}}` (one of top/bottom/dress/shoes/etc)
- **Style inference** (from name): casual / formal / athletic / underwear / etc

### If `type` is `dating_profile_photo`

Description shape: `"Dating profile photo for {npc_name or id}"`.

- **NPC**: `{{npc_name_or_id}}`
- **NPC lookup** — find the NPC in `game_review.json` → `npcs` array by matching id or name. Extract:
  - **age**: `{{npc_age}}`
  - **traits**: `{{npc_traits}}` (physical build, profession, hobbies)

## Derived facts for query planning

Fill by type:

- **canvas (image/video)**: setting, action, direction if ambiguous, people count (1|2|0), mood
- **social_post_image**: poster persona (e.g., `fit woman`, `travel influencer`), scene subject (activity implied by hashtags/caption), setting if implied, selfie-style required
- **location_image**: wide-angle vs interior, empty (no people), time of day if implied
- **clothing_image**: flat-lay product photo (no person), style tag, color (from name if declared)
- **dating_profile_photo**: selfie or candid, age range, gender, key trait hint

## Rejection criteria (auto-populated from type + tier)

### SFW types (always: location_image, clothing_image, social_post_image default, dating_profile_photo)

- Reject 3+ people on activity canvases (canvas items only)
- Reject commercial/restaurant when narrative says home (canvas only)
- **location_image**: reject lifestyle shots with people dominating the frame — the point is the space
- **clothing_image**: reject fashion editorial with model — the point is the item
- **social_post_image**: reject group shots, content that doesn't match the caption's persona
- **dating_profile_photo**: reject professional studio portraits — dating profiles are candid selfies/casual shots

### NSFW types (canvas image/video at t4+)

Full NSFW hard-reject list from `references/scoring_rubric.md` §Hard rejection filters.

## Ranked queries (filled after PLAN phase)

After the synthesis step (for empty `search_queries`) and after `validate_queries.py --from-api-json` runs:

1. `{{top_query}}` — primary
2. `{{backup_1}}` — alternate
3. `{{backup_2}}` — broadened
4. `{{backup_3}}` — last resort

## Mode

- **Quick**: SFW base tier only, no critique loop
- **Standard**: mixed SFW or t4, one critique cycle on failure
- **Deep**: any t5+, up to 3 critique cycles

For location/clothing/social_post/dating_profile categories: always quick mode (they're all SFW, low-complexity).

Selected mode for this item: `{{mode}}`

## Resume marker

Write these as the last line of the brief file:

```
PHASE: scope_complete
NEXT_PHASE: plan
SCORED: no
PACKAGED: no
```

On resume, the skill reads this to decide whether to redo SCOPE or skip to the next phase.
