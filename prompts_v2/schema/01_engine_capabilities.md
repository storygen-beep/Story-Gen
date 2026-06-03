# Schema 01 — Engine Capabilities

**Status:** Ground-truth schema reference. Extracted live from engine source on 2026-05-28. Every line number below verified against current `apps/projects/services/template_import.py` + `apps/game_generation/twee_comprehensive/generators/v2.py`.
**Authority:** This file is the ground truth for what the engine actually does. Doctrine files (`prompts_v2/doctrine/`) cite this file; this file does not cite them.
**Purpose:** Name every engine primitive an authoring LLM may legitimately reach for, with the file path + line range where the primitive lives. When a doctrine doc says *"the engine emits X via Y"*, the cross-reference resolves here.

**Reading order for fresh LLM sessions:** §3 (canvas + trigger) → §6 (effect + predicate vocabulary — most authoring touches this) → §7 (quest cards) → §8 (sidebar items) → others as needed.

**Engine files:**
- **Schema + validator:** `apps/projects/services/template_import.py` (~9,800 lines). Source of all TOML dataclasses. Runs `normalize()` (TOML → GameTemplate) + `validate()` (semantic checks).
- **Active generator:** `apps/game_generation/twee_comprehensive/generators/v2.py` (~17,500 lines). Emits SugarCube/Twine passages + runtime `setup.*` helpers. Default generator.
- **Frozen rollback:** `apps/game_generation/twee_comprehensive/generators/v1.py` (~17,000 lines). Wholesale copy of v2 at 2026-05-14. **Do NOT edit v1.** Reference v2 for line numbers in this doc.

---

## §1 — What this file is, and what it is NOT

### Is

- Per-primitive: name + dataclass file:line (schema side) + runtime file:line (generator side) + brief one-paragraph behavior.
- Schema field tables.
- The exhaustive list of supported predicate types + effect types + sidebar item types.

### Is not

- Doctrine. *"When to use Lane 3 vs Lane 4"* lives in `doctrine/02_three_lanes_plus_capstone.md`. This file only tells you *"Lane 3 is implemented as `substitutions` + `substitution_only` on `TemplateTrigger`, with runtime dispatch at `v2.py:4649`."*
- Tutorial. Each primitive gets one paragraph of behavior + a TOML shape example, not a walkthrough.
- A migration log. If a primitive was added in PRD N, the citation is in this file. The PRD itself is not summarized.

---

## §2 — Top-level TOML structure

A complete game template emits these top-level sections. Order in the TOML file is not significant.

```toml
[project]                 # § 2.1
[settings]                # § 2.1
[player]                  # § 2.2
[[npcs]]                  # § 2.3
[[locations]]             # § 2.4
[[canvases]]              # § 3
[[quest_cards]]           # § 7
[[sidebar_items]]         # § 8
[engine.daily_tick]       # § 9
[[clothing]]              # § 10
[[stage_helpers]]         # § 11
[[trait_labels]]          # § 12.2
[[flag_labels]]           # § 12.2
[[passes]]                # § 12.3
[[items]]                 # § 12.4
[[fast_jobs]]             # § 12.5
[[banks]]                 # § 12.6
[[modifiers]]             # § 12.7
[[themes]]                # § 12.8
[phone]                   # § 13
[hints]                   # § 14 (deprecated — Quest cards Doc 47/48 supersede)
```

Field-by-field schema for each section is in `schema/02_toml_schema.md`. This file documents the runtime behavior + engine primitives those sections feed.

### §2.1 — `[project]` + `[settings]`

| Dataclass | File:line |
|---|---|
| `TemplateProject` | `template_import.py:43` |
| Top-level `quests_engine` selector | parsed in `normalize()` at `template_import.py:1441+` |

**`quests_engine`** — set to `"v2"` in `[project]` to enable the V2 Quests engine (`[[quest_cards]]` mode). Default `"v1"` (deprecated; `[hints]` system; do not author against). All RTS-shape sandbox games declare `quests_engine = "v2"`.

### §2.2 — `[player]`

| Dataclass | File:line |
|---|---|
| `TemplatePlayer` | `template_import.py:81` |
| `TemplatePlayerCustomizationField` | `template_import.py:70` |

`[player.core_traits]` — initial trait values. **Every player trait referenced anywhere in the game MUST be declared here at game start with an initial integer value.** Engine reads `(player.core_traits || {})[key]` at runtime; undeclared = `undefined` = silent garbage. Sidebar items referencing undeclared traits are hard-rejected by the validator; effects + conditions on undeclared traits silently no-op. See `doctrine/09_trait_catalog.md` §2.5.

### §2.3 — `[[npcs]]`

| Dataclass | File:line |
|---|---|
| `TemplateNPC` | `template_import.py:107` |
| `TemplateNPCSchedule` | `template_import.py:94` |

`[[npcs.schedules]]` — see §5.

`[[npcs.core_traits]]` — per-NPC initial trait values, parallel structure to `[player.core_traits]`. Same declare-before-use rule.

`arc_stages = [...]` — list of stage NAMES (display strings) for the NPC's arc. The CURRENT stage integer lives on the player namespace as `player.core_traits.<slug>_stage`. See §6.7 + `doctrine/09_trait_catalog.md` §9.

---

## §3 — Canvas + Trigger primitives (Lane 1/2/3/4 mechanism support)

The canvas is the engine's universal content primitive. Lane 1 (hub button), Lane 2 (location-entry random), Lane 3 (dispatcher substitution), Lane 4 (capstone auto-fire) — all four lanes are implemented as canvases with different trigger field combinations. There is no separate "lane" dataclass.

### §3.1 — `TemplateCanvas`

| Field | Type | Where used |
|---|---|---|
| `id` | str | unique slug |
| `name` | str | display |
| `description` | str | author-side |
| `guide` | str (Doc 56 R5 — currently not yet a parsed field, see §10.7) | published-catalog recipe |
| `trigger` | `TemplateTrigger` | gating + scheduling — §3.2 |
| `nodes` | `List[TemplateNode]` | body |
| (others) | — | see `schema/02_toml_schema.md` |

`TemplateCanvas` dataclass: `template_import.py:673`.

### §3.2 — `TemplateTrigger` (THE Lane gating mechanism)

Dataclass: `template_import.py:448–502`.

| Field | Type | Lane implication |
|---|---|---|
| `location` | str | Where the canvas anchors. Lane 1/2/3/4 all require `location`. |
| `is_active` | bool (default `true`) | Soft on/off switch. |
| `is_repeatable` | bool (default `true`) | Lane 1/2/3 = `true`. Lane 4 capstone = `false` OR `true` + `flag_is_false` self-gate (see Doc 57 R1). |
| `max_triggers_per_day` | Optional[int] | Per-day cap. Lane 3 substitution targets typically `1` (Doc 67 R7). |
| `priority` | int (default 0) | Tie-break in `selectAutoFireCanvasForLocation`. Lane 4 capstones use `priority ≥ 9` (Doc 57 R1). |
| `conditions` | dict | The `{version, logic, items: [...]}` block. See §6.3 for predicate vocabulary. |
| `schedules` | `List[TemplateTriggerSchedule]` | Per-canvas time windows. See §5. |
| `npc` | Optional[str] | NPC slug for navigation indicator. |
| `trigger_mode` | str | `"manual"` (Lane 1 / Lane 3 / Lane 4) or `"random"` (Lane 2). |
| `chance` | Optional[float] (0.0–1.0) | Lane 2 random fire probability. |
| `costs` | List[dict] | Resource costs deducted on entry. |
| `show_when_blocked` | bool | E21 — render grayed-out entry on QuestsPage when daily-cooldown blocks fire. |
| `cooldown_message` | Optional[str] | Text shown on blocked entry. |
| `entry_only_from` | List[str] | Lane 2 anti-toggle cooldown (L2-2 doctrine fix). Canvas only fires if previous location matched. |
| `substitutions` | List[dict] | Lane 3 substitution rules — see §4. |
| `substitution_only` | bool | When true, canvas is excluded from `renderNpcPortraits` + `renderSoloActivities` + `selectAutoFireCanvasForLocation`. Only reachable via another canvas's substitution rule. |
| `requires_npc` | Optional[str] | Phase A (2026-05-14). Lane 2/3 NPC-presence gate via NPC schedule. Engine ANDs with all other gates. |
| `pre_substitution_effects` | List[dict] | Doc 69 §4 + §5.2 — Pattern C unconditional effects that run BEFORE substitution check. Activity "counts" even if NPC walks in. |

### §3.3 — Lane fingerprints (recognition rules)

| Lane | Diagnostic fields |
|---|---|
| **Lane 1 — Hub button** | `trigger_mode = "manual"` + `is_repeatable = true` + `npc` set + `location` matches NPC's schedule. Rendered by `renderNpcPortraits` (`v2.py:4295`) at NPC's location. **The hub's portrait renders only when the hub's OWN `schedules` window is live (`isCanvasValid`, `v2.py:4356`) AND the NPC is present (presence gate, `v2.py:4384`).** So presence coverage is per schedule row: a hub at the location with a narrower `schedules` than the NPC's presence leaves the uncovered windows dead. Author one hub per scheduled window (D72-R6, `doctrine/04` §6.1). |
| **Lane 2 — Location-entry random** | `trigger_mode = "random"` + `chance` set + `is_repeatable = true`. Dispatched by `checkRandomEncounters` (`v2.py:4520`) on location entry. |
| **Lane 3 — Dispatcher substitution** (parent activity) | `trigger_mode = "manual"` + `is_repeatable = true` + `substitutions = [...]`. Player-clickable solo activity. |
| **Lane 3 — Substitution target** | `substitution_only = true` + `requires_npc` set + `is_repeatable = true` + `max_triggers_per_day = 1`. Not in any portrait/activity grid. |
| **Lane 4 — Capstone** | `trigger_mode = "manual"` (default) + `priority ≥ 9` + (`is_repeatable = false` OR `flag_is_false` self-gate) + flag-setter effect on exit. Auto-fires on location entry via `selectAutoFireCanvasForLocation` (`v2.py:3885`). |

### §3.4 — Engine entry points for each lane

| Lane | Engine function | File:line |
|---|---|---|
| Lane 1 portraits | `renderNpcPortraits` | `v2.py:4295` |
| Lane 1 solo-activity buttons | `renderSoloActivities` | `v2.py:4419` |
| Lane 2 random encounters | `checkRandomEncounters` | `v2.py:4520` |
| Lane 3 substitution dispatch | `checkAndSubstituteCanvas` | `v2.py:4649` |
| Lane 4 capstone auto-fire | `selectAutoFireCanvasForLocation` | `v2.py:3885` |
| Location-entry dispatcher | `getStoryCanvasRedirect` | `v2.py:4272` |
| Canvas validity check | `isCanvasValid` / `isCanvasValidForSelection` | `v2.py:4005` / `v2.py:4030` |
| Trigger cooldown checks | `canTriggerCanvas` / `canTriggerActivity` | `v2.py:3621` / `v2.py:3661` |
| Mark canvas fired | `markCanvasTriggered` | `v2.py:3722` |

---

## §4 — Lane 3 substitution primitive (PRD 25)

The dispatcher mechanism is a `substitutions` list on the PARENT activity's `TemplateTrigger`. Each rule names a target canvas, a `chance`, and optional extra `conditions`.

### §4.1 — TOML shape

```toml
# Parent activity (Lane 3 host)
[[canvases]]
id = "activity_wash_dishes"
name = "Wash dishes"
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"  # slug (resolves to UUID at build time)
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "stage", operator = "gte", value = 2 },
] }

# Substitution target (Lane 3 walk-in scene)
[[canvases]]
id = "scene_frank_kitchen_dishes"
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1
substitution_only = true        # NOT in portrait/activity grids
requires_npc = "npc_frank"      # NPC must be co-located per schedule
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]
```

### §4.2 — Engine semantics (`checkAndSubstituteCanvas` at `v2.py:4649`)

Order of evaluation per substitution rule:
1. Resolve `target_canvas_id` slug → UUID via `setup.canvasSubstitutions[parentCanvasId]` registry (built at emission).
2. Look up the target canvas via `getCanvasById` (`v2.py:2669`).
3. Call `isCanvasValid(target)` — checks `is_active`, schedule, `requires_npc`, cooldown, conditions.
4. If rule has its own `conditions`, evaluate them via `triggerConditionsSatisfied` (§6.3).
5. Roll `Math.random() < chance`.
6. First match returns; `Engine.play(target.passageName)` preempts the parent passage body.

**Two evaluation modes (Doc 69 Item 1 shipped 2026-05-27):**

1. **Pattern B groups first.** Rules sharing an `exclusive_group` string share ONE dice roll, partitioned into cumulative buckets by `chance`. If the dice lands in a bucket whose target/conditions/`requires_npc` fail, the engine **falls through to solo** — it does NOT promote the next rule in the group. This is the true Pattern B semantic (Doc 67 §4.2). Multiple groups process in declaration order, each with its own dice.

2. **Pattern A independent rules next.** Rules WITHOUT an `exclusive_group` field roll their own dice (first-match wins). Pattern A per Doc 67 §4.1. Mixed A+B in the same dispatcher is supported — groups always evaluate before independents.

Rule order within a group = priority order (cumulative bucket order). Rule order across groups = first-seen order in the TOML.

Pattern C (unconditional pre-substitution effects) is shipped separately via `pre_substitution_effects` — see §4.3.

### §4.3 — `pre_substitution_effects` (Pattern C — shipped Doc 69 Item 2)

Effects that run unconditionally on canvas entry, BEFORE the substitution check. If a substitution preempts via `<<goto>>`, these effects have already executed. RTS Pattern C analog (Exercise's `<<AddFit>>` runs before NPC interrupt).

Each entry is the same shape as `TemplateChoiceEffect` (see `schema/02_toml_schema.md` §16): `{ targetType, npcId?, trait, op, value, clamp?, cap? }` — no `type` field.

```toml
[canvases.trigger]
# ... existing fields ...

[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait      = "fitness"
op         = "add"
value      = 1
```

Engine: `v2.py:11151` reads `canvas.trigger.metadata.pre_substitution_effects` and emits `<<script>>setup.applyAndNotifyTrait(...)<</script>>` macros at the top of the passage body, before the substitution `<<goto>>`. Schema: `TemplateTrigger.pre_substitution_effects` field on the trigger dataclass.

### §4.4 — `exclusive_group` (Pattern B partition — shipped Doc 69 Item 1)

Per-substitution-rule field that marks the rule as part of a Pattern B exclusive group.

```toml
[canvases.trigger]
location = "loc_bedroom"
# ... existing trigger fields ...

# Pattern B — Brother sub-variants at the study desk; one fires per attempt or fall to solo
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667                          # 1/6
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667                          # 1/6 — combined group bucket = 0.33
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "love", operator = "gte", value = 3 },
] }
```

Engine: `v2.py:4671-4713` partitions `subs` by `exclusive_group` string, rolls one dice per group, walks cumulative buckets. Buckets that fail target/conditions/`requires_npc` fall through to solo (the parent canvas's body runs). Rules without `exclusive_group` go through the Pattern A independent-rules pipeline after all groups process.

---

## §5 — Schedule + NPC presence primitives (Phase A, 2026-05-14)

### §5.1 — `[[npcs.schedules]]` — NPC location source of truth

| Field | Type | Notes |
|---|---|---|
| `location` | str | Location slug — resolved to UUID at build time |
| `weekdays` | List[int] | 0=Monday … 6=Sunday. Empty = all days |
| `start_time` | str (`HH:MM`) | Window start (24h) |
| `end_time` | Optional[str] (`HH:MM`) | Window end |
| `activity` | str | Description (author-side / sidebar) |

Dataclass: `template_import.py:94`. Parsing: `normalize()` resolves slug→UUID; build fails on invalid location slug (Phase A bugfix shipped 2026-05-14).

**Schedule entries should be non-overlapping for a single NPC.** Where in-fiction the NPC's activity differs by time band (kitchen morning vs kitchen evening), use separate entries.

**Each schedule row is a promise of a Lane 1 hub (D72-R6).** Because the schedule page advertises where every NPC is per room per window, every row must have a Lane 1 hub whose own `trigger.schedules` covers that window (per-window = separate hub canvas; §3.3). A row with no live hub is dead presence. An NPC with no physical hub anywhere (a rent/phone-only "system" NPC) must carry NO schedule row. See `doctrine/04` §6.

### §5.2 — `getNpcLocation` runtime (`v2.py:2923`)

```javascript
setup.getNpcLocation = function(npcId) { ... }
```

Computes NPC's current location on-demand by scanning the NPC's schedule entries and returning the location whose time window contains the current in-game day + time. Returns location ID, or `null` if no schedule entry matches.

**There is no stored `npcs[uuid].location` field.** Location is derived. Authoring can use the location either via `requires_npc` (Lane 2/3 presence gate) or via the `stage` trait predicate (NPC's stage — distinct from location).

### §5.3 — `requires_npc` trigger gate

When set on a `TemplateTrigger`, the engine ANDs `(getNpcLocation(requires_npc) === canvas.location)` with all other gates. The NPC must currently be at the canvas's location per their schedule.

Use case: Lane 2/3 canvases that need NPC co-presence WITHOUT the author duplicating the NPC's schedule on every canvas. Single source of truth = `[[npcs.schedules]]`.

### §5.4 — Predicate semantic: walk-in direction (Doc 67 §3.5)

Two distinct presence patterns:

| Pattern | TOML | Use case |
|---|---|---|
| **NPC walks in on Maya (Lane 3)** | `requires_npc = "npc_X"` with NPC's schedule resolving to **any** home location (e.g., a meta-location). | "Frank wandered into the kitchen because Maya is there." |
| **Maya walks in on NPC (Lane 2)** | `requires_npc = "npc_X"` with NPC's schedule resolving to **exact** canvas location. | "Maya enters the kitchen and Frank is already there." |

Both use the same `requires_npc` field; the semantic difference lives in the NPC's schedule shape, not in the canvas's predicate.

---

## §6 — Trait effect + predicate primitives

⚠️ **Effect syntax and predicate syntax use DIFFERENT field names.** Mixing them silently fails (no build error). The single most common authoring mistake. See §6.5 reference card.

### §6.1 — Trait effects (mutations)

```toml
# Player trait — add
{ targetType = "player", trait = "corruption", op = "add", value = 1 }

# Player trait — set (e.g., arousal climax reset)
{ targetType = "player", trait = "arousal", op = "set", value = 0 }

# Player trait — decay via negative add
{ targetType = "player", trait = "energy", op = "add", value = -10 }

# NPC trait
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }

# With clamp + cap
{ targetType = "player", trait = "arousal", op = "add", value = 1, clamp = true, cap = 10 }
```

| Field | Required? | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `trait` | yes | Trait name (NOT `trait_key`) |
| `op` | yes | `"add"` or `"set"` — **no `"sub"` op** (use `op = "add"` + negative `value`) |
| `value` | yes | Integer |
| `npcId` | yes when `targetType = "npc"` | NPC slug (NOT `npc_id`) |
| `clamp` | no | If true, result floored at 0 |
| `cap` | no | Integer upper bound |

Schema: `TemplateChoiceEffect` at `template_import.py:503`. Runtime application: `applyAndNotifyTrait` at `v2.py:5174`.

### §6.2 — Flag effects

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

| Field | Required? |
|---|---|
| `targetType` | yes |
| `flag` | yes |
| `op` | yes — `"set"`, `"unset"`, or `"toggle"` |
| `npcId` | yes when `targetType = "npc"` |

Schema: `TemplateFlagEffect` at `template_import.py:521`.

### §6.3 — Predicate (trigger condition) vocabulary

```toml
[canvases.trigger.conditions]
version = "1.0"   # required — schema version
logic = "AND"     # optional (default "AND"); also "OR"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
]
```

Runtime: `triggerConditionsSatisfied` at `v2.py:3275`.

**Supported `type` values** (verified at `v2.py:3275–3700`):

| `type` | Required fields | Operators |
|---|---|---|
| `"flag"` | `subject`, `flag_key` | `is_true`, `is_false`, `exists` |
| `"modifier"` | (impl-specific) | `is_active`, else |
| `"trait"` | `subject`, `trait_key`, `operator`, `value` | numeric: `eq`/`ne`/`gt`/`gte`/`lt`/`lte`; set: `in`/`not_in`; existence: `exists`/`not_exists` |
| `"days_since_flag"` | `subject`, `flag_key`, `operator`, `value` | numeric (compares days since flag was set via `flags_meta.set_day`) |
| `"clothing_slot"` | `slot`, `operator` | `equipped`, `unequipped` |
| `"clothing_item"` | `item_id`, `operator` | `equipped`, `unequipped`, `owned`, `not_owned` |
| `"worn_beauty"` | `operator`, `value` | numeric. MAX aggregate of equipped beauty. Doc 37. |
| `"worn_corruption"` | `operator`, `value` | numeric. MAX aggregate of equipped corruption. Doc 37. |
| `"worn_type"` | `operator`, `value` | `eq` / `neq` — outfit category check via `setup.getWornTypes()`. Doc 72. |
| `"pass"` | `pass_id`, `operator` | `is_active`, else |
| `"item"` | `item_id`, `operator`, `value` | numeric inventory count |
| `"stage"` | `helper`, `operator` | resolves named helper from `setup.stage_helpers_map` (`v2.py:2641`) — recursively evaluates the helper's condition block |
| `"quest"` | (V2 quests engine) | quest-card-state predicate |
| `"corruption_level"` | `operator`, `value` | banded corruption check |

`subject` values: `"player"` or `"npc"`. When `"npc"`, requires `npc_id`.

### §6.4 — Logical composition

```toml
items = [
  { type = "trait", ... },                  # implicit AND
  { type = "trait", ... },
]
# OR with explicit logic
logic = "OR"
```

Nested logic groups: pass `subgroup` items with their own `items` + `logic`. Recursion handled in `triggerConditionsSatisfied`.

### §6.5 — Field-name reference card (KEEP HANDY)

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Using effect field names in a predicate (or vice versa) causes silent no-ops — no build error fires.** Validators at `template_import.py:1077` (`_validate_effect_field_names`) + `:1098` (`_validate_predicate_field_names`) catch some cases as warnings; not all.

### §6.6 — Daily decay (`[engine.daily_tick]`)

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_ryan_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

Dataclass: `TemplateDailyTick` at `template_import.py:404`. Each `traitEffects` entry reuses the choice-effect shape (`targetType`/`npcId`/`trait`/`op`/`value`/`clamp`/`cap`).

**Doctrine constraint** (Doc 40, `doctrine/09_trait_catalog.md` §3 + §4): only `hygiene` (and similar body-state) decays daily; `corruption`, `arousal`, `relation`, `stage` do NOT decay. Authoring `corruption -1` in `traitEffects` is wrong.

### §6.7 — Stage advancement (special-case)

`applyAndNotifyTrait` at `v2.py:5183–5189` matches the trait name against `/^([a-z_]+)_stage$/` and, when `targetType === 'player'` + delta > 0:
- Updates `setup.npc_arc_stages[slug]` registry.
- Writes `game_state.stage_advancement_log[slug] = currentDay`.

**Mutation shape (capstone exit — advance Frank to stage 2):**

```toml
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

NOT `targetType = "npc"`. Stage lives on the player namespace as `<slug>_stage`. The NPC's `arc_stages = [...]` block is just the LIST of stage NAMES (display strings).

**Predicate (check Frank's stage):**

```toml
# Form A — raw player-trait check (recommended)
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Form B — via helper (engine plumbing; avoid in authoring)
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

---

## §7 — Quest card primitives (V2 engine, PRD 48)

### §7.1 — `QuestsCard` dataclass

Dataclass: `template_import.py:852`.

| Field | Type | Notes |
|---|---|---|
| `text` | str | Maya-voice narrative copy (when card is climbing) |
| `ready_text` | Optional[str] | Maya-voice "moment is on her" line (when goals met) |
| `tip` | Optional[str] | Maya-voice interior observation |
| `npc_id` | Optional[str] | When set → renders in that NPC's section. When absent → top "Story Goals" section. |
| `priority` | int (default 0) | Tie-breaker among matching cards |
| `group` | Optional[str] | Story Goals only — group key for crisis-variant collapse |
| `when` | `List[QuestsCondition]` | Routing — ALL items must eval true for this card to win the picker |
| `goals` | `List[QuestsCondition]` | The 🎯 To advance bullets — `◯ <label> — X / Y` rendering |
| `ready_canvas` | Optional[str] | When `goals.allMet` AND set, renders 🔓 Ready frame with 📍 + 🕒 from the canvas's metadata |
| `terminal` | bool (default `false`) | When true AND `when` matches → renders ✓ Arc complete |

`QuestsCondition` dataclass: `template_import.py:832`.

### §7.2 — Three card modes (Doc 50 §2)

| Mode | Has `ready_canvas`? | Has `goals`? | What player sees |
|---|---|---|---|
| **Capstone** | yes | optional (climb bullets above `when`) | 🔓 Ready frame when goals met; otherwise 🎯 climbing |
| **Mechanic** | no | yes | 🎯 climbing only — threshold cross IS the unlock; picker swaps to next template atomically |
| **Hybrid** (arc level, not card level) | mixed across cards in chain | mixed | Each card is one mode at a time |

### §7.3 — Picker semantics

Engine walks all cards' `when` against current state. Cards whose `when` passes are candidates. Sort: (priority desc, `when.length` desc, file-order asc). Top candidate wins. Story Goals additionally group by `group` key.

### §7.4 — Renderer frames

Runtime: `renderQuestsGoalBlock` (v2 generator).

| Frame | When |
|---|---|
| ✓ Arc complete (Frame 1) | `terminal = true` AND `when` matches |
| 🔓 Ready (Frame 2) | `goals.allMet` AND `ready_canvas` set |
| 🎯 To advance — bullets (Frame 3) | `goals` exist AND NOT `allMet` |
| (Frame 4 — narrative only) | DO NOT use — renders frameless; deprecated |

### §7.5 — Quest card validators (R1–R5)

Wired at `_validate_quests_cards` in `template_import.py:4469`. Validates Doc 50 R1–R4. Doc 56 R6 (`txt_only` ban) folds into R1 + R2 (every card must be capstone or mechanic; mechanic with no `goals` is rejected).

---

## §8 — Sidebar item primitives (Doc 49 + 56 R4)

`[[sidebar_items]]` — each entry is `{ type = "X", ... type-specific fields }`. Validator at `template_import.py:3024`+.

### §8.1 — Supported sidebar item types

| `type` | Use case | Schema location |
|---|---|---|
| `"trait_words"` | Banded prose label (Pure/Lewd/Slutty/Whore for corruption). 4 named bands. Raw number hidden. | `template_import.py:3032`+ |
| `"trait_bar"` | Numeric bar with optional band-text overlay + color tiers. NPC-owner mode supported (`trait_owner = "npc"` + `npc_id`). | `template_import.py:3083`+ |
| `"trait_status_text"` | Banded body-state text (Filthy/Dirty/Fresh/Clean for hygiene). Renders nothing when no band matches. | `template_import.py:3171`+ |
| `"trait_decay_warning"` | Amber warning when a decaying trait dropped today AND is within range of a band gate. Sibling of `trait_status_text`. | `v1.py:5620` (`getDecayWarnings` helper) + `v1.py:13850` (SugarCube template) |
| (more: passes, inventory, etc.) | — | see `schema/02_toml_schema.md` |

**Visibility doctrine** (Doc 68 §8): stage NEVER surfaces to any sidebar item. Antagonist awareness NEVER surfaces. See `doctrine/09_trait_catalog.md` §8.

### §8.2 — Validator enforcement

`template_import.py:2382–2547` — `_player_trait_keys` is built from `(template.player.core_traits or {}).keys()`. Sidebar items (`trait_words`, `trait_bar`, `trait_status_text`) referencing undeclared traits are **hard-rejected** with an error. (Effects + conditions on undeclared traits silently no-op; sidebar is the only surface with build-time enforcement.)

---

## §9 — Clothing primitives (Doc 36/37/71/72)

### §9.1 — `[[clothing]]` items

Dataclass: `TemplateClothingItem` at `template_import.py:164`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | unique slug |
| `slot` | str | Must be in `VALID_CLOTHING_SLOTS` = `{"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}` (`template_import.py:153`) |
| `beauty` | int | Per-item beauty value. `worn_beauty` predicate returns MAX across equipped items. |
| `corruption` | int | Per-item corruption value. `worn_corruption` returns MAX across equipped items. **NOTE: this is a content-router stat; does NOT feed `player.corruption`.** (Doc 37) |
| `type` | str (Doc 72, 2026-05-28) | Outfit category — e.g. `"casual"`, `"swim"`, `"costume"`, `"schoolwear"`, `"fitness"`, `"uniform"`, `"sleepwear"`. Recommended set in `RECOMMENDED_CLOTHING_TYPES` (`template_import.py:158`); any string accepted; typo-catch warning fires when no item declares the referenced type. |

### §9.2 — Runtime helpers

| Helper | Returns |
|---|---|
| `setup.getWornBeauty()` (`v2.py:1236`) | MAX beauty across equipped items |
| `setup.getWornCorruption()` (`v2.py:1237`) | MAX corruption across equipped items |
| `setup.getWornTypes()` (`v2.py:1243`) | Array of unique non-empty `type` strings across equipped items |

### §9.3 — Predicates

- `worn_beauty` — numeric ops (`gte`, `lt`, etc.)
- `worn_corruption` — numeric ops
- `worn_type` — `eq` / `neq` against a single type string

See §6.3 row entries.

---

## §10 — Other engine primitives

### §10.1 — `selectAutoFireCanvasForLocation` (`v2.py:3885`)

Walks all canvases tagged to a location. For each, calls `isCanvasValid`. Among valid + `is_repeatable = false` + (their flag-gates) canvases, picks highest priority. If found, REPLACES the hub render entirely. Once per matching condition (the flag-setter on exit retires the canvas).

This is the Lane 4 capstone entry point.

### §10.2 — `getStoryCanvasRedirect` (`v2.py:4272`)

Location-entry dispatcher. Checks all of: Lane 2 random encounters → Lane 4 capstones → falls through to hub render. Order matters: high-priority capstones win over Lane 2 randoms at the same location.

### §10.3 — Cooldown layers

| Layer | Function | Scope |
|---|---|---|
| 1 — Per-canvas | `canTriggerCanvas` (`v2.py:3621`) | Single canvas ID. Tracks `total`/`dayKey`/`dayCount` in `trigger_history[id]`. |
| 2 — Per-activity-name | `canTriggerActivity` (`v2.py:3661`) | Shared across same-`name` tier canvases. `activity_trigger_history[name]`. |
| 3 — Per-location random | `random_cooldowns[locId]` (Lane 2 only) | Visit-decremented integer. Set to 3 visits after a Lane 2 random fires. |

**Lane 3 substitutions inherit Layers 1 + 2 automatically via `markCanvasTriggered`; do NOT inherit Layer 3.** Doc 24 §8.

### §10.4 — Notifications + soft-fail

`<<Notification 'warning' "...">>` — toast banner. Used for time-of-day fails, threshold-publish on locked clicks (Doc 56 P2).

Per-choice `show_when_locked = true` + `locked_text = "..."` (+ optional `locked_text_threshold`) renders the choice greyed-out with a click-to-toast pattern. Doc 56 P7 — failure is information, not penalty. No stat drain on locked click.

### §10.5 — `<<NotifyCorruption N>>` (RTS-style)

UI-hint widget that toasts the required corruption level. **NOT a state mutator** — does not change `player.corruption`. Used in the ELSE branch of a corruption gate to publish the threshold transparently.

### §10.6 — `formatCanvasConditions` (`v2.py:7043`)

Renders condition blocks as human-readable strings for the published catalog + walkthrough. Each predicate type has its own formatter branch (e.g., `worn_type` → "Wearing swim" / "Not wearing schoolwear").

### §10.7 — Canvas `guide` field (Doc 56 R5)

**Status:** Doctrine-locked. Schema field NOT YET PARSED — Doc 62 PRD (currently HELD per Doc 66 §10). Authors should still include `guide = "..."` next to `name` and `description`; the validator will tolerate the field even before the dataclass adds it. When Doc 62 ships, every canvas's `guide` becomes the published-catalog recipe.

---

## §11 — Stage helpers + arc stages

### §11.1 — `[[stage_helpers]]`

Dataclass: `TemplateStageHelper` at `template_import.py:418`.

Named composite gates. Helpers reference primitive condition types ONLY — recursion (helper → helper) rejected at `validate()` time. Single-level lookup keeps cycle risk zero.

`dev_only = true` silences the unused-flag-setter validator for helpers used only by dev shortcuts.

Runtime registry: `setup.stage_helpers_map` at `v2.py:2641`.

### §11.2 — Arc stages declaration (per NPC)

```toml
[[npcs]]
id = "npc_frank"
arc_stages = [
  "neutral",
  "noticed",
  "caught",
  "first_night",
  "cracked",
  "sleepover",
]
```

These are display strings only. The CURRENT stage integer lives at `player.core_traits.frank_stage`. Engine recognizes the `<slug>_stage` trait name pattern at `v2.py:5183–5189`.

---

## §12 — Secondary primitives (brief)

For full schema, see `schema/02_toml_schema.md`. Listed here for cross-reference.

### §12.1 — `[[locations]]`

Dataclass: `TemplateLocation` at `template_import.py:135`. Fields: `id`, `name`, `description`, `entry_from` (parent for back-navigation), `entry_conditions`, `blocked_message`, image, ambient/menu fields.

### §12.2 — `[[trait_labels]]` + `[[flag_labels]]`

Dataclasses at `template_import.py:372` + `:386`. Map trait/flag keys to display names + descriptions for catalog / sidebar / debug surfaces.

### §12.3 — `[[passes]]`

Dataclass: `TemplatePass` at `template_import.py:570`. Recurring purchase items (gym membership, bus pass). Predicate type `"pass"` checks active state.

### §12.4 — `[[items]]`

Dataclass: `TemplateItem` at `template_import.py:579`. Inventory items. Predicate type `"item"` checks counts.

### §12.5 — `[[fast_jobs]]`

Dataclass: `TemplateFastJob` at `template_import.py:550`. Quick-job mechanic (income channel via single trait, not via separate channels — see `00_LEGACY_IGNORE.md` §3.4).

### §12.6 — `[[banks]]`

Dataclass: `TemplateBank` at `template_import.py:562`. Money mechanics (interest, transfers).

### §12.7 — `[[modifiers]]`

Dataclass: `TemplateModifierEffect` at `template_import.py:531`. Temporary state buffs/debuffs. Predicate type `"modifier"` checks `is_active`.

### §12.8 — `[[themes]]`

Dataclass: `TemplateTheme` at `template_import.py:587`. UI theme variants (visual register, not gameplay).

---

## §13 — Phone primitives (Doc 43 + 44 + 46)

Phone is an in-game device (purchase-gated via `pass = "phone_active"` per RTS pattern). Apps:
- **Messages** — chat threads with NPC reply effects + flag-setters + daily small-talk topics
- **Social feed** — post + comment pattern
- **Dating apps** — branching profile interactions
- (others — see `template_import.py:192–370` for full Phone dataclass set)

Dataclass: `TemplatePhone` at `template_import.py:286`. Subordinate: `TemplatePhoneApp`, `TemplatePhoneConversation`, `TemplatePhoneConversationBlock`, `TemplatePhonePost`, `TemplatePhoneProfile`, `TemplatePhoneDailyTopic`, `TemplatePhoneGalleryItem`.

---

## §14 — Validator hooks (the contract)

All validators live in `template_import.py` `validate()` function (entry: `template_import.py:2755`).

| Validator | What it catches | Severity |
|---|---|---|
| Predicate field-name typos | `subject` vs `targetType` etc. | warning (`_validate_predicate_field_names` at `:1098`) |
| Effect field-name typos | `trait_key` vs `trait` etc. | warning (`_validate_effect_field_names` at `:1077`) |
| Undeclared trait in sidebar | trait_words/trait_bar/trait_status_text references trait not in `core_traits` | **error** (`:2382–2547`) |
| Undeclared trait in effect (Doc 69 Item 4) | warning | (`_validate_trait_declaration_in_effect` at `:1274`) |
| Undeclared trait in predicate (Doc 69 Item 4) | warning | (`_validate_trait_declaration_in_predicate` at `:1351`) |
| `worn_type` typo / uncommon type (Doc 72) | warning / info | (`_validate_worn_type_items_block` at `:1168`) |
| Quest card R1–R4 (Doc 50) | error/warning | (`_validate_quests_cards` at `:4469`) |
| Weekday validation | error | (`_validate_weekdays` at `:1034`) |
| Stage helper recursion | error | inside `validate()` |
| (many others — full list out of scope here) | — | — |

Build proceeds on warnings; halts on errors.

---

## §15 — Reference card — one-line lookups

| Question | Answer |
|---|---|
| How does Lane 1 fire? | Player clicks NPC portrait at location → routes to canvas → `exit_block.choices` renders the hub menu |
| How does Lane 2 fire? | `checkRandomEncounters` rolls on location entry (`v2.py:4520`) |
| How does Lane 3 fire? | Player clicks solo activity → `checkAndSubstituteCanvas` rolls (`v2.py:4649`) → may preempt parent body |
| How does Lane 4 (capstone) fire? | `selectAutoFireCanvasForLocation` on location entry (`v2.py:3885`); priority ≥ 9 wins |
| How do I check player corruption? | `{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 }` |
| How do I check NPC stage? | `{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }` |
| How do I add 1 to player corruption? | `{ targetType = "player", trait = "corruption", op = "add", value = 1 }` |
| How do I set a flag? | `{ targetType = "player", flag = "frank_caught", op = "set" }` |
| How do I decay energy daily? | `[[engine.daily_tick.traitEffects]]` with `op = "add"`, `value = -10` |
| How do I make a Lane 3 substitution target? | Set `substitution_only = true` + `requires_npc = "npc_X"` + `max_triggers_per_day = 1` on its `TemplateTrigger` |
| How do I make a capstone? | `is_repeatable = false` (or `true` + `flag_is_false` self-gate) + `priority ≥ 9` + flag-setter on exit choice |
| How do I gate on what Maya's wearing? | `{ type = "worn_type", operator = "eq", value = "swim" }` (Doc 72) |

---

**End of file.** Next: `schema/02_toml_schema.md` for full per-section TOML field tables.
