# Schema 02 — TOML Schema Reference

**Status:** Ground-truth TOML section reference. Extracted live from `apps/projects/services/template_import.py` dataclasses (43–956) + validator (2755+) on 2026-05-28.
**Authority:** Per-section field tables; minimal round-trip examples. Doctrine + behavior live in `schema/01_engine_capabilities.md` + `prompts_v2/doctrine/`.
**Purpose:** Reference card for emitting valid TOML. Author looks up "what fields does `[[canvases.trigger]]` accept?" and finds the table here.

**Convention:** Every section below shows the dataclass + the file:line in `template_import.py`. When a field's value drives a runtime feature, the cross-reference is to `schema/01_engine_capabilities.md`.

---

## §0 — Reading guide + reference card index

| Section | What lives there |
|---|---|
| §1 | `[project]` + `[time]` + `[settings]` |
| §2 | `[player]` + `[player.core_traits]` + customization |
| §3 | `[[npcs]]` + `[[npcs.schedules]]` + `[[npcs.core_traits]]` |
| §4 | `[[locations]]` |
| §5 | `[[canvases]]` — the big one |
| §6 | `[[canvases.trigger]]` + sub-sections (schedules, substitutions, pre_substitution_effects) |
| §7 | `[[canvases.nodes]]` + blocks vocabulary + `exit_block` + choices |
| §8 | `[[quest_cards]]` (V2 engine) |
| §9 | `[[sidebar_items]]` per-type tables |
| §10 | `[engine.daily_tick]` |
| §11 | `[[engine.stage_helpers]]` |
| §12 | `[[clothing]]` + `[clothing_requirements]` |
| §13 | `[phone]` + sub-apps |
| §14 | Rent system fields (`rent_enabled` etc. — top-level GameTemplate fields) |
| §15 | Secondary sections (passes / items / fast_jobs / banks / themes / labels / tips_page) |
| §16 | Effect + predicate field reference (cross-ref to schema/01 §6) |
| §17 | Round-trip minimal-example for a complete RTS-shape sandbox |

---

## §1 — `[project]` + `[time]` + `[settings]`

### §1.1 — `[project]`

Dataclass: `TemplateProject` at `template_import.py:43`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `slug` | str | required | URL-safe identifier |
| `title` | str | required | Display title |
| `description` | str | `""` | Free text |
| `quests_engine` | str | `"v1"` | **Set to `"v2"`** for RTS-shape games (enables `[[quest_cards]]`). PRD 48. |

```toml
[project]
slug = "the_long_summer"
title = "The Long Summer"
description = "A 90-day summer with Frank at the lake house."
quests_engine = "v2"
```

### §1.2 — `[time]`

Dataclass: `TemplateTime` at `template_import.py:54`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `true` | Whether the in-game clock runs |
| `starting_hour` | int | `8` | Hour 0–23 |
| `starting_day` | str | `"Monday"` | Day name |
| `starting_week` | int | `1` | Week counter at game start |

```toml
[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1
```

### §1.3 — Top-level `GameTemplate` flags (rent + clothing + phone enable-switches)

The top-level `GameTemplate` dataclass (`template_import.py:300`) carries several enable-flags + their config. These are NOT inside any section header — they're written directly under `[project]` or top-of-file:

| Field | Type | Default | Notes |
|---|---|---|---|
| `clothing_enabled` | bool | `false` | Activates `[[clothing]]` + wardrobe/shop |
| `wardrobe_location` | str | — | Location slug for wardrobe |
| `shop_location` | str | — | Location slug for clothing shop |
| `phone_enabled` | bool | `false` | Activates `[phone]` |
| `rent_enabled` | bool | `false` | Activates rent system — see §14 |
| `rent_amount` | int | `0` | Rent due per period |
| `rent_due_day` | str | `"Monday"` | Weekly rent collection day |
| `rent_collector_npc` | Optional[str] | — | NPC slug who collects |
| `rent_grace_periods` | int | `1` | Periods skipped before eviction |
| `rent_start_after_flag` | str | `""` | Flag that activates rent |
| `rent_eviction_mode` | str | `"game_end"` | `"game_end"` (legacy) or `"flag_set"` (fail-forward) |
| `rent_eviction_flag` | str | `"rent_evicted"` | Flag set on eviction (`flag_set` mode) |
| `corruption_tiers` | List[int] | `[0,5,15,30,45]` | Per-band corruption thresholds |

```toml
clothing_enabled = true
wardrobe_location = "loc_mayas_room"
shop_location = "loc_thrift_store"

phone_enabled = true

rent_enabled = true
rent_amount = 400
rent_due_day = "Sunday"
```

---

## §2 — `[player]` + customization

Dataclass: `TemplatePlayer` at `template_import.py:81`.

### §2.1 — `[player]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | `"player"` | Internal identifier |
| `name` | str | `"Player"` | Display name (overridable via customization) |
| `description` | str | `""` | Free text |
| `portrait` | str | `""` | Image path relative to media folder |
| `core_traits` | dict | `{}` | **Required:** every trait used in game pre-declared with initial value |
| `flag_keys` | List[str] | `[]` | Pre-declared flag names |
| `customizable` | bool | `false` | When true, customization_fields render at game start |
| `trait_decay` | Dict[str, float] | `{}` | Per-trait daily decay (e.g., `{"hygiene": 10}`) |

### §2.2 — `[player.core_traits]`

**Critical:** every player trait referenced anywhere in the game MUST appear here with an integer initial value. Sidebar items referencing undeclared traits hard-fail; effects/conditions silently no-op. See `schema/01_engine_capabilities.md` §2.2 + `doctrine/09_trait_catalog.md` §2.5.

```toml
[player]
id = "player"
name = "Maya"
description = "20, escaped the city."
portrait = "maya.jpg"

[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
# Per-NPC stage traits (one per NPC with an arc)
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# Tier 2 player traits
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
```

### §2.3 — `[[player.customization_fields]]`

For `customizable = true`. Each field renders at game start; the player's choice writes into `$player.<id>`.

Dataclass: `TemplatePlayerCustomizationField` at `template_import.py:70`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Lowercase snake_case |
| `type` | str | `"text"`, `"select"`, or `"image_select"` |
| `label` | str | Display label |
| `default` | str | Initial value |
| `options` | List | For `select`: string list. For `image_select`: TemplatePlayerCustomizationOption list (`{id, image, label}`) |
| `sets_portrait` | bool | `image_select` only — selected image becomes `$player.portrait` |

```toml
[[player.customization_fields]]
id = "name"
type = "text"
label = "Your name"
default = "Maya"

[[player.customization_fields]]
id = "look"
type = "image_select"
label = "Choose your look"
sets_portrait = true
options = [
  { id = "blonde", image = "maya_blonde.jpg", label = "Blonde" },
  { id = "brunette", image = "maya_brunette.jpg", label = "Brunette" },
]
```

---

## §3 — `[[npcs]]` + `[[npcs.schedules]]`

Dataclass: `TemplateNPC` at `template_import.py:107`.

### §3.1 — `[[npcs]]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug (e.g., `"npc_frank"`) |
| `name` | str | required | Display name |
| `description` | str | `""` | Free text |
| `portrait` | str | `""` | Image path |
| `core_traits` | dict | `{}` | **Required** when NPC has any trait references |
| `flag_keys` | List[str] | `[]` | Pre-declared NPC flag names |
| `schedules` | List[`TemplateNPCSchedule`] | `[]` | Location/time windows |
| `customizable` | bool | `false` | Player can rename at game start |
| `relationship` | Optional[str] | — | Default relationship label (e.g., `"step-brother"`) |
| `relationship_options` | List[str] | `[]` | Choices for relationship picker |
| `trait_decay` | Dict[str, float] | `{}` | Per-NPC trait daily decay |
| `hidden_from_ui` | bool | `false` | Omit from Guide / Stats / sidebar widget |
| `arc_stages` | List[str] | `[]` | Display strings for stage names. Length implies max stage value (len−1). |

### §3.2 — `[[npcs.schedules]]` fields

Dataclass: `TemplateNPCSchedule` at `template_import.py:94`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `location` | str | required | Location slug — resolved to UUID at build time |
| `weekdays` | List[int] | `[]` (all days) | 0 = Monday, 6 = Sunday |
| `start_time` | str | `"00:00"` | `HH:MM` 24-hour |
| `end_time` | Optional[str] | — | `HH:MM` 24-hour |
| `activity` | str | `""` | Author-side description |

Schedule entries should be NON-OVERLAPPING per NPC. Engine resolves NPC location via `getNpcLocation` (`v2.py:2923`) by scanning entries.

### §3.3 — Round-trip example

```toml
[[npcs]]
id = "npc_frank"
name = "Frank"
description = "50s, your landlord."
portrait = "frank.jpg"
arc_stages = [
  "neutral",
  "noticed",
  "caught",
  "first_night",
  "cracked",
  "sleepover",
]

[npcs.core_traits]
arousal = 0
corruption = 0
relation = 0

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4]
start_time = "07:00"
end_time = "09:00"
activity = "Making coffee"

[[npcs.schedules]]
location = "loc_yard"
weekdays = [0, 1, 2, 3, 4]
start_time = "14:00"
end_time = "17:00"
activity = "Fixing fence"

[[npcs.schedules]]
location = "loc_living_room"
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"
activity = "Reading the paper"
```

---

## §4 — `[[locations]]`

Dataclass: `TemplateLocation` at `template_import.py:135`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display name |
| `description` | str | `""` | Free text |
| `image` | str | `""` | Image path |
| `image_search_queries` | List[str] | `[]` | For Missing Media page |
| `is_container` | bool | `false` | True for hub locations (Hallway, Main Street) |
| `parent` | str | `""` | Parent location slug |
| `entry_from` | str | `""` | Parent for back-navigation |
| `default_entry` | str | `""` | Default child location to render |
| `navigation_order` | List[str] | `[]` | Ordered child slugs for layout |
| `entry_conditions` | dict | `{}` | `{version, items}` predicate block; deny entry when fails |
| `blocked_message` | str | `""` | Shown when `entry_conditions` fail |
| `clothing_rules` | List[dict] | `[]` | Per-location clothing gates |

```toml
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "The hallway between the bedrooms."
is_container = true
entry_from = ""
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_kitchen", "loc_living_room", "loc_bathroom", "loc_yard"]

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "His room. The bed is unmade."
image = "locations/franks_bedroom.jpg"
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."
```

---

## §5 — `[[canvases]]`

The universal content primitive. Lane 1 / 2 / 3 / 4 are all implemented as canvases with different `trigger` field combinations. See `schema/01_engine_capabilities.md` §3 for lane fingerprints.

Dataclass: `TemplateCanvas` at `template_import.py:673`.

### §5.1 — Top-level fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display |
| `description` | str | `""` | Free text (author-side) |
| `trigger` | `TemplateTrigger` | — | See §6 |
| `nodes` | List[`TemplateNode`] | `[]` | See §7 |
| `connections` | List[`TemplateConnection`] | `[]` | Graph editor only — runtime ignores |
| `loop` | dict | `{}` | Loop config (advanced — see Frank bedroom sex loop) |

Note: `guide` field (Doc 56 R5) is doctrine-locked but schema-pending — Doc 62 PRD held. Authors should still emit `guide = "..."` next to `description`; the parser tolerates the field even before it becomes a parsed attribute.

---

## §6 — `[[canvases.trigger]]` and sub-sections

Dataclass: `TemplateTrigger` at `template_import.py:448`.

### §6.1 — Trigger fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `location` | str | required | Location slug (the canvas anchors here) |
| `is_active` | bool | `true` | Soft on/off switch |
| `is_repeatable` | bool | `true` | Lane 1/2/3 = `true`. Lane 4 capstone = `false` (or `true` + flag-gate). |
| `max_triggers_per_day` | Optional[int] | — | Per-day cap. Lane 3 substitution targets typically `1`. |
| `priority` | int | `0` | Lane 4 capstones use ≥ 9. Tie-break in `selectAutoFireCanvasForLocation`. |
| `conditions` | dict | `{}` | `{version, logic, items: [...]}` — see §16 |
| `schedules` | List[`TemplateTriggerSchedule`] | `[]` | Per-canvas time windows — see §6.2 |
| `npc` | Optional[str] | — | NPC slug; navigation indicator |
| `trigger_mode` | str | `"manual"` | `"manual"` (Lane 1/3/4) or `"random"` (Lane 2) |
| `chance` | Optional[float] | — | 0.0–1.0; Lane 2 only |
| `costs` | List[dict] | `[]` | Resource costs on entry: `[{trait: str, value: int}]` |
| `show_when_blocked` | bool | `false` | Render grayed-out entry on QuestsPage when daily-cooldown blocks |
| `cooldown_message` | Optional[str] | — | Custom blocked text |
| `entry_only_from` | List[str] | `[]` | Lane 2 anti-toggle cooldown: only fire if previous location matched |
| `substitutions` | List[dict] | `[]` | Lane 3 dispatcher rules — see §6.3 |
| `substitution_only` | bool | `false` | Canvas only reachable via another canvas's substitution rule |
| `requires_npc` | Optional[str] | — | NPC presence gate — ANDs with all gates; engine consults `getNpcLocation` |
| `pre_substitution_effects` | List[dict] | `[]` | Pattern C — effects run before substitution check (Doc 69 Item 2) |

### §6.2 — `[[canvases.trigger.schedules]]`

Dataclass: `TemplateTriggerSchedule` at `template_import.py:441`.

| Field | Type | Notes |
|---|---|---|
| `weekdays` | List[int] | 0 = Monday … 6 = Sunday |
| `start_time` | str | `HH:MM` |
| `end_time` | Optional[str] | `HH:MM` |

### §6.3 — `[[canvases.trigger.substitutions]]` (Lane 3)

Each entry is a free-form dict (not a dataclass — schema lives in `setup.checkAndSubstituteCanvas` runtime).

| Field | Type | Notes |
|---|---|---|
| `target_canvas_id` | str | Slug of the substitution target canvas (resolves to UUID at build) |
| `chance` | float | 0.0–1.0 fire probability |
| `conditions` | Optional[dict] | Extra `{version, items}` block (ANDs with target canvas's own gates) |

### §6.4 — `[[canvases.trigger.pre_substitution_effects]]` (Doc 69 Item 2)

Effects that run before the substitution check. Same shape as `TemplateChoiceEffect` (see §16).

### §6.5 — Trigger examples per lane

**Lane 1 — Hub canvas (player clicks NPC portrait):**

```toml
[canvases.trigger]
location = "loc_franks_bedroom"
npc = "npc_frank"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "20:00", end_time = "23:00" }]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
```

**Lane 2 — Random ambient (dice on location entry):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "random"
chance = 0.25
is_repeatable = true
requires_npc = "npc_frank"
schedules = [{ weekdays = [0,1,2,3,4], start_time = "07:00", end_time = "09:00" }]
```

**Lane 3 — Parent activity (Maya picks Wash Dishes):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"
chance = 0.33
```

**Lane 3 — Substitution target (Frank walks in mid-chore):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1
substitution_only = true
requires_npc = "npc_frank"
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]
```

**Lane 4 — Capstone (auto-fire on location entry):**

```toml
[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = false
priority = 10
schedules = [{ weekdays = [0,1,2,3,4], start_time = "19:30", end_time = "21:00" }]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
```

---

## §7 — `[[canvases.nodes]]` + blocks + exit_block

A canvas is composed of one or more `nodes`. Each node has a body (`blocks` list) + an `exit_block` (how it ends).

### §7.1 — `[[canvases.nodes]]`

Dataclass: `TemplateNode` at `template_import.py:654`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug within the canvas |
| `name` | str | required | Display |
| `blocks` | List[dict] | `[]` | Body content — see §7.2 |
| `exit_block` | `TemplateExitBlock` | (default) | How the node ends — see §7.3 |
| `loop_terminal` | bool | `false` | For loop canvases — terminates the loop |
| `modifier_redirect` | Optional[dict] | — | `{modifier_key, node}` — if modifier active, render different node |

### §7.2 — Block vocabulary (`canvases.nodes.blocks`)

Each block is `{type = "X", ... type-specific fields}`. Supported types:

| `type` | Required fields | Notes |
|---|---|---|
| `"paragraph"` | `content` | Prose. RTS-flat default (Doc 30 §7.1). |
| `"dialog"` | `npcId` + `content` | Character dialogue. Speaker tag rendered. |
| `"thought_bubble"` | `content` | Maya interior (used sparingly). |
| `"image"` | `props.file` | Image asset. `props = { file, alt? }` |
| `"video"` | `props.file` | Video asset |
| `"clip"` | `props.file` | Looping clip |
| `"heading"` | `content` | Section heading |
| `"group"` | `props = { conditions, blocks }` | Tier-routed block group. `blocks` is a nested list. Inner blocks render only when conditions pass. |
| `"block_pool"` | `props = { variants: [...], pick: "random"|"sequential" }` | Pretext variation per Doc 30 Pattern E |
| `"cascade"` | `props = { beats: [...] }` | Linkreplace cascade — each beat unfolds on click |

**Group block (tier-routing) example:**

```toml
[[canvases.nodes.blocks]]
type = "group"
props.conditions = { items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
] }
props.blocks = [
  { type = "image", props = { file = "scenes/kitchen_morning.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", npcId = "npc_frank", content = "Morning." },
]
```

**Cascade block (RTS linkreplace) example:**

```toml
[[canvases.nodes.blocks]]
type = "cascade"
props.beats = [
  { advance_text = "Push the door open.", blocks = [
    { type = "paragraph", content = "The door swings. He's reading at the desk." },
  ]},
  { advance_text = "Step inside.", blocks = [
    { type = "dialog", npcId = "npc_frank", content = "Quiet." },
  ]},
  # ... more beats
]
```

### §7.3 — `[canvases.nodes.exit_block]`

Dataclass: `TemplateExitBlock` at `template_import.py:646`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `type` | str | `"location"` | `"location"` or `"choices"` |
| `text` | str | `"Continue"` | Button label (for `type = "location"`) |
| `config` | dict | `{}` | For `type = "location"`: `{destinationType, locationId, time_progression_minutes}` |
| `choices` | List[`TemplateChoice`] | `[]` | For `type = "choices"`: the menu — see §7.4 |

**`type = "location"` (single return-to-location button):**

```toml
[canvases.nodes.exit_block]
type = "location"
text = "Return to the kitchen"
[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId = "loc_kitchen"
time_progression_minutes = 10
```

**`type = "choices"` (multi-button hub menu — Lane 1):**

```toml
[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee"
# ... (TemplateChoice fields — §7.4)
```

### §7.4 — `TemplateChoice` (exit_block.choices)

Dataclass: `TemplateChoice` at `template_import.py:609`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `text` | str | `"Continue"` | Button label |
| `targetType` | str | `"trigger"` | `"trigger"` / `"location"` / `"node"` |
| `locationId` | Optional[str] | — | For `targetType = "location"` |
| `nodeId` | Optional[str] | — | For `targetType = "node"` (route to another node within same canvas, or `"canvas_id.node_id"` cross-canvas) |
| `time_progression_minutes` | Optional[int] | — | Time advance on click |
| `effects` | List[`TemplateChoiceEffect`] | `[]` | Trait effects — see §16 |
| `flagEffects` | List[`TemplateFlagEffect`] | `[]` | Flag effects — see §16 |
| `wardrobeEffects` | List[dict] | `[]` | `[{op: "equip"|"unequip", slot: str, item_id?: str}]` |
| `conditions` | dict | `{}` | Per-choice gating — `{version, items}` |
| `show_when_locked` | bool | `false` | Mode A: render greyed-out when conditions fail |
| `locked_text` | str | `""` | Tooltip/reason when locked |
| `locked_text_threshold` | str | `""` | S4 (RTS-style): toast text published on locked-click (e.g., `"30+ Corruption Needed"`) |
| `rejection_node` | Optional[str] | — | Mode B: route to rejection node on locked-click |
| `rejection_effects` | List[`TemplateChoiceEffect`] | `[]` | Effects on rejection-click |
| `modifier_effects` | List[`TemplateModifierEffect`] | `[]` | Temporary trait offset modifiers |
| `pass_effects` | List[dict] | `[]` | `[{pass_id, op}]` — pass purchase |
| `item_effects` | List[dict] | `[]` | `[{item_id, op, count}]` — inventory |
| `quest_effects` | List[dict] | `[]` | V1 quests — `[{quest, op, step?}]` |
| `schedule_effects` | List[dict] | `[]` | Delayed events — `[{delayDays, action, flag?/quest?/conversation?}]` |
| `text_variants` | List[dict] | `[]` | Per-state text — `[{text, conditions}]`; first match wins |

**Locked choice (always-show with threshold publish — RTS pattern):**

```toml
[[canvases.nodes.exit_block.choices]]
text = "Suck him"
show_when_locked = true
locked_text = "I need to know him better first"
locked_text_threshold = "Maya's corruption: 35+"
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 35 },
  { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
] }
nodeId = "frank_bedroom_sex_loop"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

---

## §8 — `[[quest_cards]]` (V2 engine)

Activated by `[project].quests_engine = "v2"`. Dataclass: `QuestsCard` at `template_import.py:852`.

### §8.1 — `[[quest_cards]]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `text` | str | `""` | Maya-voice narrative copy (climbing) |
| `ready_text` | Optional[str] | — | Maya-voice "moment is on her" line (when goals met) |
| `tip` | Optional[str] | — | Maya-voice interior observation |
| `npc_id` | Optional[str] | — | When set → renders in NPC section. When absent → top "Story Goals" section |
| `priority` | int | `0` | Tie-breaker |
| `group` | Optional[str] | — | Story Goals only — group key for crisis-variant collapse |
| `when` | List[`QuestsCondition`] | `[]` | Routing — ALL must eval true |
| `goals` | List[`QuestsCondition`] | `[]` | 🎯 To advance bullets |
| `ready_canvas` | Optional[str] | — | When all goals met AND set → 🔓 Ready frame |
| `terminal` | bool | `false` | When true AND `when` matches → ✓ Arc complete |

### §8.2 — `QuestsCondition` (used in `when` + `goals`)

Dataclass: `QuestsCondition` at `template_import.py:832`. Flat shape (NOT a `type` discriminator like trigger conditions).

| Field | Type | Notes |
|---|---|---|
| `flag` | Optional[str] | Flag gate — pair with `op` (`"is_true"` / `"is_false"`) |
| `trait` | Optional[str] | Trait gate — pair with `subject`, `op`, `value`, `label` |
| `subject` | Optional[str] | `"player"` or `"npc"` (trait gates only) |
| `npc_id` | Optional[str] | Required when `subject = "npc"` |
| `op` | str | `"is_true"`/`"is_false"` (flags); `"gte"`/`"lte"`/`"gt"`/`"lt"`/`"eq"` (traits) |
| `value` | Optional[float] | For trait gates |
| `label` | Optional[str] | For goals — text rendered next to ◯ bullet (e.g., `"Maya's corruption"`) |

### §8.3 — Examples (capstone + mechanic modes)

**Capstone card (Frank F4 — sleepover):**

```toml
[[quest_cards]]
npc_id = "npc_frank"
priority = 4
text = "He moved the line. The bedroom is the venue now."
ready_text = "Tonight I don't leave."
tip = "Diana down the hall. Quiet."
ready_canvas = "scene_frank_sleepover"
when = [
  { flag = "frank_cracked", op = "is_true" },
  { flag = "frank_sleepover_done", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 50, label = "Maya's corruption" },
]
```

**Mechanic card (Ryan trust climb):**

```toml
[[quest_cards]]
# unlocks: ryan_yard_hub menu item "Help him in the yard" at trust >= 10
npc_id = "npc_ryan"
priority = 1
text = "He's around the yard most afternoons. I should make him notice me."
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "lt", value = 10 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10, label = "Ryan trust" },
]
# NO ready_canvas — mechanic mode. Threshold cross IS the unlock.
```

**Terminal card:**

```toml
[[quest_cards]]
npc_id = "npc_frank"
priority = 99
terminal = true
text = "It's the way it is now. Daddy's house. Daddy's bed. Diana down the hall."
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

See `doctrine/04_authoring_rules.md` for Doc 50 R1–R6 + Doc 56 R6.

---

## §9 — `[[sidebar_items]]`

Validator: `template_import.py:3024`+. Each entry is `{ type = "X", ... type-specific fields }`.

### §9.1 — `type = "trait_words"`

Banded prose label. Renders a band's text string; raw number hidden. Used for corruption (Pure / Lewd / Slutty / Whore).

| Field | Notes |
|---|---|
| `type` | `"trait_words"` |
| `trait` | Trait key (must be declared in `core_traits`) |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `label` | Display prefix (e.g., `"Corruption"`) — optional |
| `bands` | List of `{min, max, text, icon?}` |

```toml
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore",  icon = "💦" },
]
```

### §9.2 — `type = "trait_bar"`

Numeric bar with optional band-text overlay + color tiers.

| Field | Notes |
|---|---|
| `type` | `"trait_bar"` |
| `trait` | Trait key |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `label` | Display label |
| `max` | Bar max value (default 100) |
| `hide_value` | When true, only the label renders (not `X / Y` numeric) |
| `color_tiers` | List of `{up_to, class}` — drives `.trait-bar-fill.<class>` CSS |
| `bands` | List of `{min, max, text, icon?}` — overlay text inside the bar |

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
color_tiers = [
  { up_to = 30,  class = "low" },
  { up_to = 70,  class = "medium" },
  { up_to = 100, class = "high" },
]
bands = [
  { min = 0,  max = 2,  text = "Cold" },
  { min = 3,  max = 5,  text = "Warm" },
  { min = 6,  max = 8,  text = "Hot" },
  { min = 9,  max = 10, text = "Burning" },
]
```

### §9.3 — `type = "trait_status_text"`

Banded body-state text. Renders nothing when no band matches (passive — no min/max value declared shows nothing). Used for hygiene/energy bands (Filthy/Dirty/Fresh/Clean).

| Field | Notes |
|---|---|
| `type` | `"trait_status_text"` |
| `trait` | Trait key |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `bands` | List of `{min, max, text, icon?}` — only matching band renders |

```toml
[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy", icon = "🧫" },
  { min = 25,  max = 49,  text = "Dirty",  icon = "🌫️" },
  { min = 50,  max = 74,  text = "Fresh",  icon = "🪞" },
  { min = 75,  max = 100, text = "Clean",  icon = "🧼" },
]
```

### §9.4 — `type = "trait_decay_warning"`

Amber warning when a decaying trait dropped today AND is within range of a band gate. Sibling of `trait_status_text`.

| Field | Notes |
|---|---|
| `type` | `"trait_decay_warning"` |
| `trait` | Trait key |
| `threshold` | Numeric threshold within which the warning fires |
| `text` | Display string |

### §9.5 — Other sidebar types

| Type | Notes |
|---|---|
| `"passes"` | Renders all active passes (e.g., gym, bus) |
| `"inventory"` | Renders inventory items |
| (others) | See validator at `template_import.py:3000+` |

**Visibility doctrine (Doc 68 §8):** stage NEVER surfaces to any sidebar item. Antagonist awareness NEVER surfaces. Body-state (energy + hygiene) MUST surface. See `doctrine/09_trait_catalog.md` §8 for per-arc-shape defaults.

---

## §10 — `[engine.daily_tick]`

Dataclass: `TemplateDailyTick` at `template_import.py:404`.

Effects that fire once per in-game day at `advanceDay()` rollover.

| Field | Type | Notes |
|---|---|---|
| `flagEffects` | List[`TemplateFlagEffect`] | Clear/set daily-cooldown flags (silent) |
| `traitEffects` | List[`TemplateChoiceEffect`] | Per-day trait deltas. Each reuses the choice-effect shape (`targetType`/`npcId`/`trait`/`op`/`value`/`clamp`/`cap`). Optional per-entry `conditions` block. |

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_ryan_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "npc", npcId = "npc_jake", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

**Doctrine constraint (Doc 40 / Doc 68 §3–§4):** body-state (`hygiene`, `energy`) decays daily. Progression traits (`corruption`, `arousal`, `relation`, `stage`) do NOT decay daily. NPC arousal climbs daily (no-decay rule per Doc 40).

---

## §11 — `[[engine.stage_helpers]]`

Dataclass: `TemplateStageHelper` at `template_import.py:418`.

Named composite gates. A `type = "stage"` condition references a helper by name; engine recursively evaluates the helper's `conditions` block.

| Field | Type | Default | Notes |
|---|---|---|---|
| `name` | str | required | Helper identifier |
| `description` | str | `""` | Author-side |
| `conditions` | dict | `{}` | `{version, items}` — primitive types only (no helper → helper recursion) |
| `dev_only` | bool | `false` | Silences flag-setter-coverage validator warning (helpers used only by dev shortcuts) |

```toml
[[engine.stage_helpers]]
name = "frank_stage_2_plus"
description = "Frank reached Stage 2 (post-catch)."
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },
] }
```

---

## §12 — `[[clothing]]` + `[clothing_requirements]`

Dataclass: `TemplateClothingItem` at `template_import.py:164`.

### §12.1 — `[[clothing]]`

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display |
| `slot` | str | required | Must be in `VALID_CLOTHING_SLOTS` = `{"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}` |
| `image` | str | `""` | Image path |
| `initial` | bool | `false` | Player starts with this item |
| `conditions` | dict | `{}` | v1.0 conditions for wearing |
| `price` | int | `0` | Dollars; 0 = free/initial |
| `beauty` | int | `0` | Beauty contribution (worn_beauty reads MAX) |
| `corruption` | int | `0` | Content-router stat (worn_corruption reads MAX). **Does NOT mutate `player.corruption`.** |
| `type` | str | `""` | Outfit category (`"swim"`, `"casual"`, etc.). Read by `worn_type` predicate (Doc 72). |

Recommended type values (typo-catch reference set; any string accepted): `casual`, `swim`, `costume`, `schoolwear`, `fitness`, `uniform`, `sleepwear`.

```toml
[[clothing]]
id = "starter_outfit"
name = "Jeans and a tee"
slot = "top"
initial = true
beauty = 5
corruption = 0
type = "casual"

[[clothing]]
id = "bikini_top"
name = "Yellow bikini top"
slot = "top"
price = 25
beauty = 8
corruption = 15
type = "swim"
```

### §12.2 — `[clothing_requirements]`

Dataclass: `TemplateClothingRequirements` at `template_import.py:180`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `body_coverage` | bool | `true` | Must wear (top + bottom) OR dress |
| `always_required` | List[str] | `[]` | Slots that can never be removed |
| `conditional` | Dict[str, Dict[str, str]] | `{}` | `{slot: {until_flag, message}}` — slot required until flag set |

---

## §13 — `[phone]`

`phone_enabled = true` at top level activates the phone. Dataclass tree: `TemplatePhone` at `template_import.py:286` (with sub-apps in §13.2+).

### §13.1 — `[phone]` top-level

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `true` | Master on/off |
| `purchase_flag` | str | `""` | Sidebar button hidden until this flag is true |

### §13.2 — `[[phone.apps]]`

Dataclass: `TemplatePhoneApp` at `template_import.py:192`. Valid types: `"chat"`, `"social_feed"`, `"gallery"`, `"dating"`, `"custom"`, `"quests"`, `"fast_jobs"`, `"bank"`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `type` | str | one of valid types |
| `label` | str | Display name |
| `icon` | str | Image path |
| `post_actions` | List[dict] | `social_feed` only — `[{label, corruption_min?, followers_min, followers_max, daily_cap?, counter_trait}]` |

### §13.3 — `[[phone.conversations]]` (chat thread)

Dataclass: `TemplatePhoneConversation` at `template_import.py:216`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `app` | str | App slug |
| `npc` | str | NPC slug |
| `trigger` | dict | conditions block — when does this conversation become available |
| `blocks` | List[`TemplatePhoneConversationBlock`] | Thread structure |
| `notify` | str | Toast text on delivery (default `"📱 New message"`) |

### §13.4 — `[[phone.conversations.blocks]]`

Dataclass: `TemplatePhoneConversationBlock` at `template_import.py:203`.

| Field | Type | Notes |
|---|---|---|
| `type` | str | `"message"` (NPC sends) or `"reply"` (player chooses) |
| `sender` | str | `"npc"` or `"player"` (for message type) |
| `content` | str | Message body |
| `after_reply` | bool | Show after the preceding reply was picked |
| `choices` | List[dict] | For reply type — `[{text, effects, flagEffects, conditions, schedule_effects}]` |
| `round` | Optional[int] | Multi-round conversation: which round (1, 2, 3…) |
| `after_round` | Optional[int] | Show only after this round answered |
| `after_choice` | Optional[int] | Show only if this choice picked in `after_round` |

### §13.5 — `[[phone.posts]]` (social_feed)

Dataclass: `TemplatePhonePost` at `template_import.py:228`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `app` | str | App slug (`social_feed` type) |
| `npc` | str | NPC slug (empty for stranger posts) |
| `poster_name` | str | Display name for non-NPC posters |
| `image` | str | Image path |
| `caption` | str | Post text |
| `likes` | int | Like count display |
| `trigger` | dict | Conditions for visibility |
| `notify` | str | Toast text (default `"📱 New post"`) |

### §13.6 — `[[phone.profiles]]` (dating app)

Dataclass: `TemplatePhoneProfile` at `template_import.py:244`.

| Field | Notes |
|---|---|
| `id`, `app`, `npc` | identifiers |
| `photos` | List[str] image paths |
| `bio`, `age`, `interests` | display fields |
| `trigger` | conditions for profile availability |
| `match_condition` | conditions for "match" (NPC swipes back) |

### §13.7 — `[[phone.daily_topics]]`

Dataclass: `TemplatePhoneDailyTopic` at `template_import.py:258`. Per-NPC daily small-talk + photo actions.

| Field | Notes |
|---|---|
| `id`, `npc` | identifiers |
| `player_message` | What Maya sends |
| `npc_response` | NPC reply |
| `effects` | List of trait/flag effects on send |
| `conditions` | Visibility gating |
| `image` | Photo-action: media path rendered as sent photo |
| `corruption_min` | Lock until player corruption ≥ this |
| `cooldown` | `"per_topic"` = per-topic daily cap; default = per-NPC daily cap |

### §13.8 — `[[phone.gallery_items]]`

Dataclass: `TemplatePhoneGalleryItem` at `template_import.py:276`.

| Field | Notes |
|---|---|
| `id`, `image`, `caption` | display |
| `trigger` | Visibility gate |
| `link` | Optional passage to open on click |

---

## §14 — Rent system (top-level GameTemplate fields)

See §1.3 for the toggle/config fields. The rent engine fires on `rent_due_day` weekly. If `player.money < rent_amount`:
- `rent_eviction_mode = "game_end"` — game over.
- `rent_eviction_mode = "flag_set"` — sets `rent_eviction_flag` (e.g., `"rent_evicted"`); fail-forward (author handles downstream).

`rent_text` is a dict of override strings: `{paid, late, evicted, due_warning, ...}`.

`rent_grace_periods = N` allows N skipped periods before eviction fires.

---

## §15 — Secondary sections

### §15.1 — `[[passes]]` (recurring purchases)

Dataclass: `TemplatePass` at `template_import.py:570`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `cost` | int | Purchase price |
| `duration_days` | int | Validity period |
| `icon` | str | Image path |

### §15.2 — `[[items]]` (inventory consumables)

Dataclass: `TemplateItem` at `template_import.py:579`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `icon` | str | Image path |
| `max_stack` | int | Inventory cap per item |

### §15.3 — `[[fast_jobs]]`

Dataclass: `TemplateFastJob` at `template_import.py:550`. Phone-app-driven repeatable money jobs.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `income` | int | Dollars per shift |
| `xp_req` | int | Fast-jobs XP needed to unlock |
| `cooldown_days` | int | Days locked after working |
| `time_period` | str | Optional `game.time` gate (e.g. `"M"`, `"A"`) |
| `money_trait` | str | Trait that accumulates (default `"money"`) |

### §15.4 — `[bank]`

Dataclass: `TemplateBank` at `template_import.py:562`.

| Field | Type | Notes |
|---|---|---|
| `enabled` | bool | Master |
| `interest_rate` | float | Daily compound rate (e.g., `0.01`) |
| `money_trait` | str | Money trait name (default `"money"`) |

### §15.5 — `[theme]`

Dataclass: `TemplateTheme` at `template_import.py:587`. UI theme — colors + fonts + border-radius + optional custom CSS.

| Field | Default |
|---|---|
| `mode` | `"light"` (or `"dark"`) |
| `primary`, `secondary`, `accent`, `success`, `danger`, `warning` | hex colors |
| `font_heading`, `font_mono` | CSS font strings |
| `border_radius` | CSS length |
| `bg`, `surface`, `surface_alt`, `border`, `text`, `text_muted` | auto-derived if empty |
| `custom_css` | freeform |

### §15.6 — `[[trait_labels]]` + `[[flag_labels]]`

Dataclasses: `TemplateTraitLabel` at `template_import.py:372`, `TemplateFlagLabel` at `template_import.py:386`.

Map internal trait/flag names to player-facing labels used by `setup.computeHintGoal` when auto-rendering 🎯 goal blocks.

```toml
[[trait_labels]]
key = "corruption"
label = "Maya's corruption"
verb = "reach"
unit = ""

[[trait_labels]]
key = "relation"
label = "Ryan trust"
verb = "reach"
unit = ""

[[flag_labels]]
key = "frank_caught"
label = "Caught by Frank"
```

### §15.7 — `[ui.tips_page]`

Dataclass: `TemplateTipsPage` at `template_import.py:393`. Standalone game-mechanics page. Engine prints `content` verbatim (raw HTML).

| Field | Notes |
|---|---|
| `title` | Default `"Tips"` |
| `content` | Raw HTML body |

---

## §16 — Effect + predicate field reference (the field-name minefield)

See `schema/01_engine_capabilities.md` §6 for full behavior. This is the reference card.

### §16.1 — Trait EFFECT (mutation)

Dataclass: `TemplateChoiceEffect` at `template_import.py:503`.

```toml
{ targetType = "player", trait = "corruption", op = "add", value = 1 }
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }
{ targetType = "player", trait = "arousal", op = "set", value = 0 }   # climax reset
{ targetType = "player", trait = "energy", op = "add", value = -10 }  # decay via negative
```

| Field | Required | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `npcId` | when `targetType = "npc"` | NPC slug |
| `trait` | yes | trait name (NOT `trait_key`) |
| `op` | yes | `"add"` or `"set"` — no `"sub"` |
| `value` | yes | integer |
| `clamp` | no | floor at 0 |
| `cap` | no | upper bound |
| `conditions` | no | gate this effect (only applies if conditions pass) |

### §16.2 — Flag EFFECT

Dataclass: `TemplateFlagEffect` at `template_import.py:521`.

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

| Field | Required | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `npcId` | when `targetType = "npc"` | NPC slug |
| `flag` | yes | flag name (NOT `flag_key`) |
| `op` | yes | `"set"`, `"unset"`, or `"toggle"` |
| `conditions` | no | gate the effect |

### §16.3 — Trigger / canvas PREDICATE (condition gate)

The `{version, logic, items: [...]}` block on `[canvases.trigger.conditions]`, `[canvases.exit_block.choices.conditions]`, `[locations.entry_conditions]`, etc.

```toml
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"   # or "OR"; default "AND"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
  { type = "worn_type", operator = "eq", value = "swim" },
]
```

**Supported `type` values** (from `triggerConditionsSatisfied` at `v2.py:3275+`):

| `type` | Required fields | Operators |
|---|---|---|
| `"flag"` | `subject`, `flag_key` | `is_true`, `is_false`, `exists` |
| `"modifier"` | (impl) | `is_active` |
| `"trait"` | `subject`, `trait_key`, `operator`, `value` | numeric: `eq`/`ne`/`gt`/`gte`/`lt`/`lte`; set: `in`/`not_in`; existence: `exists`/`not_exists` |
| `"days_since_flag"` | `subject`, `flag_key`, `operator`, `value` | numeric |
| `"clothing_slot"` | `slot`, `operator` | `equipped`, `unequipped` |
| `"clothing_item"` | `item_id`, `operator` | `equipped`, `unequipped`, `owned`, `not_owned` |
| `"worn_beauty"` | `operator`, `value` | numeric |
| `"worn_corruption"` | `operator`, `value` | numeric |
| `"worn_type"` | `operator`, `value` | `eq`, `neq` |
| `"pass"` | `pass_id`, `operator` | `is_active` |
| `"item"` | `item_id`, `operator`, `value` | numeric |
| `"stage"` | `helper`, `operator` | resolves named helper, recursively evaluates |
| `"quest"` | (V2 quests engine) | quest-state predicate |
| `"corruption_level"` | `operator`, `value` | banded check |

`subject` values: `"player"` or `"npc"`. When `"npc"`, requires `npc_id`.

### §16.4 — Field-name reference card

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` | `operator` |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required) |

**Mixing effect + predicate field names silently no-ops with NO build error.** Validators at `template_import.py:1077` + `:1098` catch some cases as warnings, not all.

### §16.5 — Quest card condition shape (different from trigger condition!)

Quest card `when` + `goals` use the FLAT `QuestsCondition` shape (NOT a `type` discriminator):

```toml
{ flag = "frank_caught", op = "is_true" }
{ trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" }
{ trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10, label = "Ryan trust" }
```

vs trigger conditions which use the typed shape:

```toml
{ type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" }
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 }
```

**Two different shapes for the same semantic.** Match the shape to the consumer (`[[quest_cards]]` uses flat; everything else uses typed).

---

## §17 — Minimal round-trip example

A complete RTS-shape sandbox skeleton — copy-paste starting point. Trim/expand to game scope. References every section above.

```toml
schema_version = "1.0"

[project]
slug = "test_game"
title = "Test Game"
description = "Minimal RTS-shape sandbox skeleton."
quests_engine = "v2"

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

clothing_enabled = true
phone_enabled = false
rent_enabled = true
rent_amount = 400
rent_due_day = "Sunday"

# ---- Player ----
[player]
id = "player"
name = "Maya"
portrait = "maya.jpg"

[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
frank_stage = 0

# ---- NPCs ----
[[npcs]]
id = "npc_frank"
name = "Frank"
arc_stages = ["neutral", "caught", "first_night", "cracked"]

[npcs.core_traits]
arousal = 0
corruption = 0
relation = 0

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0,1,2,3,4]
start_time = "07:00"
end_time = "09:00"

# ---- Locations ----
[[locations]]
id = "loc_hallway"
name = "Hallway"
is_container = true

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
entry_from = "loc_hallway"

# ---- Daily tick ----
[engine.daily_tick]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]

# ---- Sidebar ----
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure" },
  { min = 25, max = 49, text = "Lewd" },
  { min = 50, max = 74, text = "Slutty" },
  { min = 75, max = 100, text = "Whore" },
]

[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy" },
  { min = 25,  max = 49,  text = "Dirty" },
  { min = 50,  max = 74,  text = "Fresh" },
  { min = 75,  max = 100, text = "Clean" },
]

# ---- Clothing ----
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

# ---- Capstone canvas (Lane 4) ----
[[canvases]]
id = "scene_livingroom_catch"
name = "The catch"
description = "Frank catches Maya. Sets frank_caught."

[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = false
priority = 10
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
schedules = [{ weekdays = [0,1,2,3,4], start_time = "19:30", end_time = "21:00" }]

[[canvases.nodes]]
id = "catch"
name = "The catch"
blocks = [
  { type = "image", props = { file = "scenes/catch.jpg" } },
  { type = "paragraph", content = "He's there before you hear him." },
  { type = "dialog", npcId = "npc_frank", content = "Quiet." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Lower your eyes."
flagEffects = [{ targetType = "player", flag = "frank_caught", op = "set" }]
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 5 },
  { targetType = "player", trait = "frank_stage", op = "set", value = 2 },
]
targetType = "location"
locationId = "loc_living_room"

# ---- Quest card (capstone mode) ----
[[quest_cards]]
npc_id = "npc_frank"
priority = 1
text = "He's around the house all day. He notices."
ready_text = "I think he's about to call it."
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]
```

---

**End of file.** For doctrine (when to use which primitive), read `prompts_v2/doctrine/`. For runtime behavior, read `prompts_v2/schema/01_engine_capabilities.md`.
