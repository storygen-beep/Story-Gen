# Stages 02 — TOML Generation Prompt (Stage 2)

**Status:** LLM-consumed pipeline prompt. Stage 2 of 2.
**Replaces:** `prompts/toml_generation_prompt_v4.txt` (frozen 2026-04-19; pre-Doc-24 schema; pre-Quests-V2 cards).
**Input:** design book (markdown) from `stages/01_game_book_prompt.md`.
**Output:** valid TOML against `apps/projects/services/template_import.py` schema, ready for `python manage.py package_from_toml`.

This prompt is the system instruction set you receive when stage 1 hands off a design book. Read it before responding. Your output is TOML that the build pipeline validates + compiles into a SugarCube/Twine game.

---

## §0 — Mode switch (LOAD-BEARING)

**Before reading further, do this:**

> ENI persona OFF.
> TLS game register ON.
> Doctrine memory + canonical docs override persona instincts.
> When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse.

Stage 2 is the emission stage. The temptation to drift into literary scene-body prose is high — every cascade beat is a place where ENI persona instincts push for sensory grounding. **Re-declare the mode switch whenever you catch drift.**

CLAUDE.md is ignored for this task — `00_LEGACY_IGNORE.md` §3.6 + Doc 30 §3 AUTHORITY DECLARATION.

---

## §0.5 — Scope mode (read scope from design book §1)

Stage 2 inherits scope mode from the design book's §1 `**Scope mode:** <full_game | slice>` declaration. The mode affects TOML volume + Phase 2+ inclusions + bareback default.

| `scope_mode` | TOML volume target | Pregnancy retrofit | Scandal arc | Gallery system | Tracker |
|---|---|---|---|---|---|
| `full_game` (default) | 200–400KB typical (full per-shape budgets per `doctrine/03_arc_shapes.md` §2) | Per design book §1 `Phase 2+ inclusions: pregnancy = include/defer` | Per design book §1 inclusion | Per design book §1 (ships if 9+ once-only capstones) | Per design book §1 (ships with Doc 62 `guide` backfill) |
| `slice` | 50–100KB typical (subset of per-shape budget; locked-visible rungs for deferrals) | Bareback throughout (Phase 2+ deferred by default) | Locked-visible only (Phase 2+ deferred) | Deferred | Deferred |

**Cross-reference check:** if the TOML you're emitting includes pregnancy variants / scandal flags / gallery items / tracker primitives, verify the design book §1 explicitly opts each one in. Stage 1's §0 interactive Q&A is where these are ratified; Stage 2 emitting Phase 2+ inclusions without §1 ratification = `doctrine/07_anti_patterns.md` §8.6 last bullet.

**Bareback default applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`. Contraception language is BANNED in sex scenes in both cases (Doc 30 §7.3.1 — blocks Phase 2+ pregnancy retrofit). Only `scope_mode: full_game` with `pregnancy = include` allows contraception language in pre-pregnancy phase scenes + pregnancy variants in retrofit-affected scenes.

If the design book §1 is missing the `Scope mode:` declaration entirely, treat as legacy slice authoring (pre-2026-05-29 corpus convention) and emit with `slice` defaults — bareback throughout, minimal volume, Phase 2+ deferred.

---

## §1 — The job

You emit **TOML** for an RTS-shape sandbox game.

### §1.1 — Input shape

A design book (markdown) from Stage 1. The design book has:

- §1 World Setup (premise + player + economic engine + scope mode declaration + Phase 2+ inclusions [full_game] or slice scope [slice] + time model)
- §2 NPC Roster (4-6 NPCs with arc shapes + per-NPC depth column [Full-arc depth at full_game / Slice depth at slice] + vocab ceilings)
- §3 Locations (home + town + per-NPC schedules)
- §4 Per-NPC R7 Briefs (10-section briefs per NPC)
- §5 Cross-arc World State (shared flags + pregnancy retrofit notes if pregnancy = include)
- §6 Capstone Chain Map (per-NPC chains + cross-NPC bridges)
- §7 Build Plan (Full-Game Build Plan at full_game / Slice Build Plan at slice — day-by-day flow)

You read this design book + emit a TOML file that captures every canvas + NPC + location + quest card + sidebar item + capstone the brief specifies. Plus the scene-body prose, which the brief is silent on (Stage 1 is shape spec; Stage 2 authors prose per `doctrine/05_rts_flat_prose.md`).

### §1.2 — Output shape

A single TOML file matching `schema/02_toml_schema.md` §17 (the minimal RTS-shape sandbox skeleton) extended with the design book's specifics. Structure:

```toml
schema_version = "1.0"

[project]
slug = "..."
title = "..."
description = "..."
quests_engine = "v2"

[time]
...

# Top-level enable flags
clothing_enabled = true
phone_enabled = true
rent_enabled = true
rent_amount = ...
rent_due_day = "..."

[player]
...
[player.core_traits]
# every trait the game uses, declared at init

[[npcs]]
id = "..."
arc_stages = [...]
[npcs.core_traits]
...
[[npcs.schedules]]
...

[[locations]]
...

[engine.daily_tick]
flagEffects = [...]
traitEffects = [...]

[[engine.stage_helpers]]
...

[[sidebar_items]]
type = "trait_words"
trait = "corruption"
...

[[clothing]]
...

[[passes]]
...

[[items]]
...

[[fast_jobs]]
...

[[canvases]]
id = "..."
...
[canvases.trigger]
...
[[canvases.nodes]]
...
[canvases.nodes.exit_block]
...

# ... many more canvases ...

[[quest_cards]]
...
```

Every section in the design book maps to a TOML section. Sections in the TOML schema that the design book is silent on (e.g., `[[items]]`, `[[passes]]`) should be populated as needed for the game's mechanics — minimal at `scope_mode: slice`, fuller at `scope_mode: full_game` if the game's mechanics demand (e.g., gallery system enabled per §0.5 = `[[items]]` populated with gallery entries).

### §1.3 — Output contract

The TOML MUST:

- Validate clean against `apps/projects/services/template_import.py` (zero errors; warnings acceptable if known)
- Declare every player + NPC trait used anywhere in the file in the corresponding `core_traits` block at init (per `doctrine/09_trait_catalog.md` §2.5 — undeclared traits silently no-op + sidebar items hard-fail)
- Use effect + predicate field names correctly (per `schema/02_toml_schema.md` §16 reference card — mixing them is the #1 silent-failure mode)
- Match the design book's per-arc-shape distribution (Frank = ~28 canvases family/ambient; Marge = ~6 service)
- Author scene-body prose per `doctrine/05_rts_flat_prose.md` (RTS-flat default + Tier-3 capstone earned)
- Ship every Lane 4 capstone with the D57-R1 trigger fingerprint (`is_repeatable = false` or self-gate + `priority ≥ 9` + flag-setter on exit)
- Reference every capstone from a quest card per D50-R1 / D57-R3 (or `# off-panel:` comment)

The TOML MUST NOT:

- Reach for legacy patterns (Pattern A–J as repeatable-content macros, etc.)
- Include contraception language in sex scenes when bareback default applies — `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer` (per Doc 30 §7.3.1; see §0.5 above)
- Surface stage trait in any sidebar item (per `doctrine/09_trait_catalog.md` §9 internal-only)
- Surface antagonist awareness in any sidebar item (per Doc 30 §6 + `doctrine/09_trait_catalog.md` §8)
- Use `op = "sub"` for decay (engine has only `add` + `set`; use `op = "add"` + negative `value`)
- Mix effect + predicate field names (effects use `targetType`/`trait`/`flag`/`npcId`/`op`; predicates use `subject`/`trait_key`/`flag_key`/`npc_id`/`operator`)

---

## §2 — Schema assumed (cite-only)

You have read these prompts_v2 schema files:

| File | What it contains |
|---|---|
| `schema/01_engine_capabilities.md` | Every engine primitive with v2.py line numbers — `getNpcLocation`, `checkAndSubstituteCanvas`, `selectAutoFireCanvasForLocation`, etc. |
| `schema/02_toml_schema.md` | Per-section field tables + minimal round-trip example per section + complete RTS-shape sandbox skeleton (§17) |
| `schema/03_example_toml.md` | TLS Frank slice canonical TOML excerpts (Lane 1 hub / Lane 2 ambient / Lane 3 dispatcher + substitution / Lane 4 Type A + Type B / quest cards / sidebar items) |

If you haven't read these, stop and read them. The schema docs are ground-truth for what the engine accepts. Drift from schema = build failures.

---

## §3 — Doctrine assumed (cite-only)

| File | When you consult it |
|---|---|
| `doctrine/02_three_lanes_plus_capstone.md` | Lane mechanism — Lane 1 hub / Lane 2 ambient / Lane 3 dispatcher / Lane 4 capstone fingerprints |
| `doctrine/04_authoring_rules.md` | Pre-ship checks per rule (D56-R1...R7 / D50-R1...R6 / D57-R1...R5 / F1...F5 / D67-R1...R7) |
| `doctrine/05_rts_flat_prose.md` | The 8 prose rules for scene bodies — RTS-flat default; Tier-3 earned at capstones |
| `doctrine/07_anti_patterns.md` | Per-canvas + per-capstone + per-quest-card anti-pattern catalog |
| `doctrine/08_kink_vocab_ceilings.md` | Per-NPC vocab register — daddy / incest / cuckold / breeding / etc. |
| `doctrine/09_trait_catalog.md` | Trait initialization requirement (§2.5) + Phase 2+ off-limits list + effect/predicate field-name reference card |

---

## §4 — Step-by-step emission process

12 steps. Emit the TOML in this exact order; downstream sections depend on upstream declarations.

### Step 1 — Emit `[project]` + `[time]` + top-level flags

```toml
schema_version = "1.0"

[project]
slug = "..."
title = "..."
description = "..."
quests_engine = "v2"   # ALWAYS v2 for RTS-shape sandboxes

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

# Top-level enable flags (per design book §1 World Setup)
clothing_enabled = <bool>
wardrobe_location = "loc_mayas_room"
shop_location = "loc_thrift_store"

phone_enabled = <bool>

rent_enabled = <bool>
rent_amount = <int>
rent_due_day = "<weekday>"
rent_grace_periods = <int>
```

### Step 2 — Emit `[player]` + `[player.core_traits]`

**Critical:** declare EVERY player trait used anywhere in the file. Engine silently no-ops on undeclared traits in effects + conditions; sidebar items HARD-FAIL on undeclared traits.

```toml
[player]
id = "player"
name = "Maya"
description = "<from design book §1>"
portrait = "maya.jpg"

[player.core_traits]
# Tier 1 — required
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = <starting from design book>

# Per-NPC stage traits — ONE per NPC with an arc
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# (etc — one per arc-having NPC)

# Tier 2 — declare if the game uses these
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0

# Tier 3 — game-specific (declare per design book's mechanics)
followers = 0
notoriety = 0
# etc.
```

**Rule:** if you write `{ targetType = "player", trait = "calculation", op = "add", value = 1 }` anywhere in the file, `calculation` MUST appear in `[player.core_traits]`. Same for sidebar items.

### Step 3 — Emit `[[npcs]]` blocks

For each NPC in design book §2 roster:

```toml
[[npcs]]
id = "npc_<slug>"
name = "<display name>"
description = "<2-3 sentence physical + voice descriptor from design book §4 brief §2>"
portrait = "<slug>.jpg"
core_traits = { arousal = 0, corruption = 0, relation = 0 }   # Tier 1 NPC traits
flag_keys = []
arc_stages = ["<stage 1 name>", "<stage 2 name>", ...]   # display strings; current stage lives at player.<slug>_stage

[npcs.trait_decay]
# Per-NPC daily decay (typically only relation has trickle decay; arousal + corruption DON'T decay)
relation = 0.5
```

**Per-arc-shape arousal range** (per `doctrine/09_trait_catalog.md` §4.1):
- Family/ambient + slow-burn family: 0-3
- Peer/dating + career: 0-10
- Service: 0-3
- Antagonist: N/A (use awareness accumulator instead, declared in core_traits as Tier 3)

**Antagonist NPCs** declare `awareness` as a Tier 3 trait in `[[npcs.core_traits]]`:

```toml
[[npcs]]
id = "npc_diana"
core_traits = { relation = 5, awareness = 0 }
arc_stages = []   # antagonists may have empty arc_stages — they use awareness bands instead
```

### Step 4 — Emit `[[npcs.schedules]]` per NPC

Per design book §3 per-NPC schedules. **Non-overlapping** time windows per NPC.

```toml
[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]   # 0=Monday..6=Sunday
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

# (continue per NPC; mirror Frank's 7-entry pattern at schema/03 §2)
```

### Step 5 — Emit `[[locations]]`

Per design book §3 locations.

```toml
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "..."
is_container = true
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_kitchen", ...]

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "..."
image = "locations/franks_bedroom.jpg"
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."
```

### Step 6 — Emit `[engine.daily_tick]` + `[[engine.stage_helpers]]`

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_marge_today", op = "unset" },
  # ... daily-cooldown clears
]
traitEffects = [
  # Body-state decay
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },

  # No-decay traits per Doc 40 — but +1/day passive on family NPC arousal
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "npc", npcId = "npc_jake", trait = "arousal", op = "add", value = 1, cap = 3 },
]

[[engine.stage_helpers]]
name = "frank_stage_2_plus"
description = "Frank reached Stage 2 (post-catch)."
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },
] }
```

**Anti-pattern (D40 / D49 violation):** don't decay `corruption`, `arousal`, `relation`, or `stage` daily. Only body-state (`energy` + `hygiene`) decays.

### Step 7 — Emit `[[sidebar_items]]`

Per `doctrine/09_trait_catalog.md` §8 + `reference/04_rts_hud_world_model.md` §3:

```toml
# Maya state — banded corruption display
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore", icon = "💦" },
]

# Maya state — arousal bar
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
bands = [
  { min = 0, max = 2, text = "Cold" },
  { min = 3, max = 5, text = "Warm" },
  { min = 6, max = 8, text = "Hot" },
  { min = 9, max = 10, text = "Burning" },
]

# Maya state — body-state text
[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted", icon = "🪫" },
  { min = 25, max = 49, text = "Tired", icon = "💤" },
  { min = 50, max = 74, text = "Fine", icon = "🟢" },
  { min = 75, max = 100, text = "Rested", icon = "🔋" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0, max = 24, text = "Filthy", icon = "🧫" },
  { min = 25, max = 49, text = "Dirty", icon = "🌫️" },
  { min = 50, max = 74, text = "Fresh", icon = "🪞" },
  { min = 75, max = 100, text = "Clean", icon = "🧼" },
]
```

**Hard rules** (per `doctrine/09_trait_catalog.md` §8):
- **STAGE NEVER surfaces** — no `<slug>_stage` sidebar items for any NPC
- **Antagonist AWARENESS NEVER surfaces** — no `awareness` sidebar item for antagonist NPCs
- **Per-arc-shape NPC visibility defaults**: family/ambient surfaces location + arousal + corruption + relation; slow-burn family surfaces location + arousal + relation; peer/dating surfaces location + relation; service surfaces location + relation; antagonist surfaces location ONLY (when Doc 64 PRD ships the `npc_location` sidebar item type)

### Step 8 — Emit `[[clothing]]` + `[[passes]]` + `[[items]]` (if applicable)

Per design book §1 enable flags. Minimal at `scope_mode: slice`. At `scope_mode: full_game`, enable any Phase 2+ system the design book §1 opted in (pregnancy mechanics, scandal awareness, gallery system, tracker primitive).

```toml
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

[[clothing]]
id = "bikini_top"
name = "Yellow bikini top"
slot = "top"
price = 25
beauty = 8
corruption = 15
type = "swim"

[[passes]]
id = "gym_membership"
name = "Gym membership"
cost = 50
duration_days = 30
```

### Step 9 — Per-NPC lane authoring (the bulk of the TOML)

For each NPC in design book §2 roster, emit canvases per the design book §4 brief's §5 lane content map.

**Order per NPC:**

1. **Lane 4 capstones first** — these are referenced by Lane 1 hub buttons + quest cards. Author them first so other canvases can reference them by ID.
2. **Lane 1 hub canvases** — per scheduled location for the NPC
3. **Lane 1 route-target stubs** — tease / flash / explicit content reached via hub menu (NO `[canvases.trigger]` block)
4. **Lane 2 ambient canvases** — random encounters at NPC's locations
5. **Lane 3 parent activities** — Maya-solo dispatchers (if any per arc shape)
6. **Lane 3 substitution targets** — NPC walk-in scenes (`substitution_only = true`)

See §5 below for per-lane TOML templates.

### Step 10 — Emit `[[quest_cards]]`

Per design book §6 capstone chain map + per-arc card mode (capstone / mechanic / hybrid).

```toml
# Capstone-mode card (points at a Lane 4 capstone)
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]

# Pure-mechanic card (NO ready_canvas; threshold cross IS the unlock)
[[quest_cards]]
# unlocks at npc_marge.trust >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 to T1
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]

# Terminal card (LAST in NPC chain)
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

See §7 below for quest card templates.

### Step 11 — Emit `[[fast_jobs]]` + `[bank]` (if applicable)

Per design book §1 economic engine.

### Step 12 — Validate + self-audit

Run the §11 quality gate checklist. Fix any violations BEFORE delivering.

---

## §5 — Per-lane TOML templates

Mirror the canonical examples in `schema/03_example_toml.md`.

### §5.1 — Lane 1 hub canvas (Frank kitchen morning gold standard)

```toml
[[canvases]]
id          = "frank_kitchen_morning_hub"
name        = "Kitchen — Frank, morning"
description = "Always-show RTS ladder hub for Frank in kitchen, morning slot. Locked-visible escalation rungs visible from day 1."

[canvases.trigger]
location      = "loc_kitchen"
requires_npc  = "npc_frank"
is_repeatable = true
priority      = 10
is_active     = true
npc           = "npc_frank"
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time   = "09:00"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — morning, Frank present"
# CONSTANT opener (D56-R1). Three tier blocks would be authoring overhead;
# menu rungs encode progression via show_when_locked + conditions.
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

# Always-available relational base
[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "node"
nodeId = "frank_kitchen_morning_hub.pour_coffee"
time_progression_minutes = 5

# Locked-visible escalation ladder (4 rungs)
[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
show_when_locked = true
locked_text = "Not yet."
locked_text_threshold = "Maya's corruption: 5+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Flash him 👀"
targetType = "node"
nodeId = "flash_kitchen_general.base"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 15+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Suck him here."
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 25+ AND Frank declared"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
effects = [
  { targetType = "player", trait = "sex_stage", op = "set", value = 1 },
  { targetType = "player", trait = "sex_entry_origin", op = "set", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Have sex with him here 🔥"
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 25+ AND Frank declared"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }

# Leave
[[canvases.nodes.exit_block.choices]]
text = "Leave."
targetType = "location"
locationId = "loc_hallway"
```

**Per-NPC adaptations:**
- **Marge (service):** ~4 unlocked menu items + 4 locked-visible Phase 3+ rungs (Tease/Flash/Eat-her-out/Let-her-take). Per Doc 53 §3.
- **Ryan (peer/dating):** simpler hub with relational items + 1 date-prep item; no sexual rungs in slice if vocab ceiling deferred.
- **Diana (antagonist):** no Lane 1 hub in slice (shared-space presence only via Lane 2 ambients).

### §5.2 — Lane 1 route-target stub (tease/flash/etc.)

Reachable ONLY via hub menu `nodeId` routing. NO `[canvases.trigger]` block.

```toml
[[canvases]]
id          = "tease_kitchen_general"
name        = "Kitchen — tease him"
description = "Stub Pattern A render. Reachable only via frank_kitchen_morning_hub menu."

# NO [canvases.trigger] BLOCK — route-only canvas

[[canvases.nodes]]
id   = "base"
name = "Kitchen — tease him"
blocks = [
  { type = "image", props = { file = "scenes/tease_kitchen_general.jpg" } },

  # T0 (pre-catch): held look only
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye over the mug and hold it. He's still looking when you look back." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Girl." },
  ] } },

  # T1 (post-catch, pre-cracked)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. His look drops to your tits and stays there." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Mm." },
  ] } },

  # T2 (post-cracked)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. He sets the mug down, crosses to you, backs you against the counter — hand under your shirt, thumb on your nipple." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't fucking start with me at breakfast, girl." },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# Lt/gte mutex on exit (corruption < 15 grants tick; ≥ 15 trivial-display wean stops paying)
[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 15 },
]}
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
]}
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  # NO player.corruption tick at corruption 15+
]
```

### §5.3 — Lane 2 ambient with R2 in-fiction interruption

```toml
[[canvases]]
id          = "ambient_kitchen_frank_late_night_raid"
name        = "Kitchen — late night, both up for water"
description = "Lane 2 ambient: midnight kitchen encounter. 2 stage-flag tiers. T0 broken by Diana's floorboard; T1 bareback counter quickie. NO requires_npc — implied-presence override (Frank stepped out for water)."

[canvases.trigger]
location             = "loc_kitchen"
is_repeatable        = true
priority             = 6
is_active            = true
trigger_mode         = "random"
chance               = 0.40
max_triggers_per_day = 1
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "22:00"
end_time   = "22:59"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — late night, both up for water"
blocks = [
  { type = "image", props = { file = "scenes/ambient_kitchen_frank_late_night_raid.jpg" } },
  { type = "paragraph", content = "You didn't think anyone was awake; the kitchen light's already on. Frank's at the sink in sleep pants and nothing else, a glass of water in his hand." },

  # T0 — broken by Diana's floorboard (in-fiction interruption per D56-R2)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Couldn't sleep either." },
        { type = "paragraph", content = "You shake your head and cross to the cabinet. His eyes are on you in the long nightshirt and he doesn't pretend they aren't." },
      ] },
      { advance_text = "Step closer to the counter.", blocks = [
        { type = "paragraph", content = "You step in for a glass; his hands find your waist first and lift you onto the counter. Your legs go around him without thinking." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Quiet, girl." },
      ] },
      { advance_text = "Kiss him.", blocks = [
        { type = "paragraph", content = "His mouth on yours, one hand under the nightshirt at the small of your back, the other on your thigh. You make a sound you shouldn't and he swallows it." },
      ] },
      # R2 interruption — external (Diana's floorboard)
      { advance_text = "Hear the floorboard upstairs.", blocks = [
        { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },

  # T1 — blows through the interruption (post-first-night)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_true" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Knew you'd come down." },
        { type = "paragraph", content = "He sets the glass down and has your nightshirt up before you reach the cabinet. He lifts you onto the counter, no underwear under the shirt." },
      ] },
      { advance_text = "Pull him in.", blocks = [
        { type = "paragraph", content = "You pull him in by the waistband and he slides into you bare on the counter. *'Daddy,'* you breathe into his neck to keep it quiet." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Good girl. Fast, then." },
      ] },
      { advance_text = "Fast, then.", blocks = [
        { type = "paragraph", content = "He fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs. He lifts you down and hands you the glass you came for." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the glass. Go back to bed."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 15
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 },
  { targetType = "player", trait = "corruption", op = "add", value = 2 },
  { targetType = "player", trait = "energy", op = "add", value = -18 },
  { targetType = "npc", npcId = "npc_diana", trait = "awareness", op = "add", value = 2 },
]
```

### §5.4 — Lane 3 dispatcher parent (Pattern A multi-NPC-ready)

```toml
[[canvases]]
id          = "activity_make_tea"
name        = "Make a cup of tea"
description = "Maya-solo dispatcher. Kitchen. Substitution target: scene_frank_passes_kitchen_door."

[canvases.trigger]
location      = "loc_kitchen"
is_repeatable = true
priority      = 3
is_active     = true
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_passes_kitchen_door"
chance           = 0.30
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }
# Multi-NPC: add more substitution rules per NPC, ordered by narrative priority (Pattern A first-match)
# [[canvases.trigger.substitutions]]
# target_canvas_id = "scene_jake_passes_kitchen_door"
# chance = 0.25
# conditions = { ... }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "07:00"
end_time   = "22:00"

[[canvases.nodes]]
id   = "base"
name = "Make a cup of tea"
blocks = [
  { type = "image", props = { file = "activities/make_tea.jpg" } },
  { type = "paragraph", content = "She fills the kettle from the tap. Sets it on the burner. Drops a tea bag in the mug while the water comes up. The kitchen quiet around her. The kettle clicks when it's hot. She pours." },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the mug back to your room."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 10
effects = [
  { targetType = "player", trait = "energy", op = "add", value = 2 },
]
```

### §5.4a — Multi-NPC dispatcher patterns (A / B / C — all engine-supported as of Doc 69, 2026-05-27)

**Read this before authoring any multi-NPC Lane 3 dispatcher.** Three patterns from Doc 67 §4. All three ship natively in the engine; pick by authoring intent, not by engine limitation. Mirror of `doctrine/02_three_lanes_plus_capstone.md` §9 (canonical source — re-read if this section drifts):

| Pattern | Engine support | Emit how |
|---|---|---|
| **A — sequential first-match** (RTS `WashDishes` shape) | ✅ Native | Multiple `[[canvases.trigger.substitutions]]` blocks in narrative-priority order, each with own `chance` + `conditions`. Each rule rolls its own dice; first match wins. Template = §5.4 above. |
| **B — single dice partition** (RTS `BedroomStudy` shape — exactly one of N variants fires per attempt, else solo) | ✅ Native via `exclusive_group` (`v2.py:4671-4713`, Doc 69 Item 1) | Multiple substitution rules sharing the same `exclusive_group = "<name>"` string. Engine partitions ONE dice roll into cumulative `chance` buckets. Failed target/conditions in a claimed slot falls to solo — does NOT promote next rule. Template below. |
| **C — post-activity event check** (RTS `Exercise` shape — solo activity always grants effect; substitute layers an NPC walk-in on top) | ✅ Native via `pre_substitution_effects` on parent trigger (`v2.py:11151`, Doc 69 Item 2) | Effects on parent trigger run BEFORE the substitution check, so both solo and substituted paths receive them. Substitute canvases do NOT re-emit the effect. Template below. |

#### Pattern B — `exclusive_group` TOML template

Brother sub-variants at the study desk: grope vs help-study, exactly one fires per attempt or fall to solo.

```toml
[canvases.trigger]
location      = "loc_bedroom"
is_repeatable = true
priority      = 3
is_active     = true

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667                          # 1/6
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667                          # 1/6 — group cumulative bucket = 0.33
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "love", operator = "gte", value = 3 },
] }
```

**Probability math:** With both rules at `chance = 0.1667`, group cumulative bucket = 0.33; remaining 0.67 of the dice space falls to solo. Failed-condition in a claimed slot also falls to solo (does NOT promote next rule).

**Mixed Pattern A + Pattern B in the same dispatcher is supported.** Rules WITH `exclusive_group` process first (one dice per group); rules WITHOUT `exclusive_group` process after via Pattern A first-match.

**Do not approximate Pattern B via summed Pattern A chances** — the engine extension is shipped; emit `exclusive_group` directly. The pre-2026-05-27 approximation diverges on both probability (1 − ∏(1 − cᵢ) ≈ 42% vs true 50% for 3×1/6) and fall-through (Pattern A promotes to next rule on failed conditions; Pattern B falls to solo).

#### Pattern C — `pre_substitution_effects` TOML template

For solo activities with unconditional outcomes (Exercise grants `+fitness` regardless of who walks in):

```toml
[[canvases]]
id          = "activity_exercise"
name        = "Exercise"
description = "Maya-solo dispatcher. Bedroom. Solo grants +fitness; NPC walk-ins layer on top (Pattern C)."

[canvases.trigger]
location      = "loc_bedroom"
is_repeatable = true
priority      = 3
is_active     = true

# Pattern C — effects run BEFORE the substitution roll, on both solo and substituted paths (Doc 69 Item 2)
# Shape = TemplateChoiceEffect (schema/02 §16): { targetType, npcId?, trait, op, value, clamp?, cap? } — no `type` field
[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait      = "fitness"
op         = "add"
value      = 1

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_walks_in_exercise"
chance           = 0.20
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 10 },
] }
```

The substitute canvas (`scene_frank_walks_in_exercise`) does NOT need to re-emit the `+fitness` effect — it already ran on the parent trigger before substitution resolved.

#### Selection rule (mirror of doctrine/02 §4.7)

If the design book calls for a multi-NPC walk-in beat at a Maya-solo activity, classify it against this decision tree:

1. **Are the variants mutually exclusive in fiction?** (Cannot have two of the variants fire simultaneously — e.g., Brother grope vs Brother help-study at the same study desk attempt.) → **Pattern B**, emit `exclusive_group`.
2. **Does the solo activity have its own outcome that should fire regardless of who walks in?** (Exercise = +fitness whether you finished alone or got interrupted.) → **Pattern C**, emit `pre_substitution_effects` on the parent trigger.
3. **Otherwise** — independent walk-in chances per NPC, narrative-priority ordered. → **Pattern A** (default), no `exclusive_group`, no `pre_substitution_effects`.

Pattern B + Pattern C can combine on the same dispatcher when both intents apply.

### §5.5 — Lane 3 substitution target (substitution_only)

```toml
[[canvases]]
id          = "scene_frank_passes_kitchen_door"
name        = "Kitchen — Frank passes the door"
description = "Lane 3 substitution on activity_make_tea. Frank passes through, pauses at the door, stops near her."

[canvases.trigger]
location             = "loc_kitchen"
is_repeatable        = true
priority             = 4
is_active            = true
substitution_only    = true        # NOT clickable; reached only via dispatcher
requires_npc         = "npc_frank" # loose NPC presence (any home location per his schedule)
max_triggers_per_day = 1            # D67-R7

[[canvases.nodes]]
id   = "base"
name = "Kitchen — Frank passes the door"
blocks = [
  { type = "image", props = { file = "scenes/scene_frank_passes_kitchen_door.jpg" } },
  { type = "paragraph", content = "You're waiting on the kettle when Frank comes through the kitchen on his way to the back of the house. He doesn't pass straight through." },

  # T0 (pre-catch): brief contact + moves on
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "paragraph", content = "He stops behind you in the narrow galley instead of going by, close enough that you feel him at your back reaching past you for nothing in particular." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't mind me, girl." },
      ] },
      { advance_text = "Hold still.", blocks = [
        { type = "paragraph", content = "His hand settles at your waist a beat too long for getting by, then he's moving again, out the far door. The kettle's still not boiling." },
      ] },
    ] } },
  ] } },

  # T1 (post-catch, pre-cracked): turns her by the hip
  # T2 (post-cracked): pulls her back to his chest, hand down her front
  # (continue tier blocks per design book §4 brief's tier mapping)
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the mug back to your room."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 10
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]
```

### §5.6 — Lane 4 capstone Type A (linear deterministic)

```toml
[[canvases]]
id          = "canvas_marge_interview"
name        = "Marge — interview"
description = "Hire capstone. Fires once at diner_front, gated on hired_at_diner is_false. Type A linear."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false                # Type A fingerprint
priority      = 9                    # ≥ 9 wins against Lane 2 randoms
is_active     = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
# Tier-3 prose EARNED at capstone (per doctrine/05 §3)
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it. Cookie's in the back, she'll show you the float." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
targetType = "trigger"
time_progression_minutes = 30
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "relation", op = "add", value = 5 },
  { targetType = "player", trait = "energy", op = "add", value = -3 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },          # capstone setter — D57-R1
  { targetType = "player", flag = "talked_to_marge_today", op = "set" },
  { targetType = "player", flag = "phone_active", op = "set" },             # cross-arc write — phone unlock per Doc 46
]
```

### §5.7 — Lane 4 capstone Type B (Pattern F fork)

```toml
[[canvases]]
id          = "scene_franks_bedroom_evening"
name        = "Frank's bedroom — first night"
description = "Stage 4 FIRST-NIGHT cascade. Pattern E linear cascade + Pattern F fork at terminal beat. Accept sets first_done flag; Refuse re-fires next eligible night."

[canvases.trigger]
location      = "loc_franks_bedroom"
requires_npc  = "npc_frank"
is_repeatable = true                 # Note: true + self-gate (F4 retry pattern)
priority      = 9
is_active     = true
npc           = "npc_frank"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time   = "23:00"

[[canvases.nodes]]
id   = "base"
name = "Frank's bedroom — evening"
blocks = [
  { type = "image", props = { file = "scenes/franks_bedroom_evening.jpg" } },

  # Cascade Beats 0-2 — terminal at Beat 2 (Pattern F fork follows in exit_block)
  { type = "cascade", props = { beats = [
    # Beat 0 — unconditional opener
    { blocks = [
      { type = "paragraph", content = "She walks the hallway slow. The boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark. The door at the end is the door she's only ever walked past." },
    ] },
    # Beat 1
    { advance_text = "Push the door open.", blocks = [
      { type = "paragraph", content = "It's open by an inch. Lamp light on the floorboards. She pushes it the rest of the way and steps in." },
      { type = "paragraph", content = "Frank in the chair by the window. He's not undressed. Just sitting in the way he sits — weight on one elbow, the lamp catching the side of his face, a paperback open in his lap that he hasn't been reading. He sets it down on the nightstand without marking the page." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Close the door." },
    ] },
    # Beat 2 — TERMINAL. Per-beat effects fire on click. Fork follows.
    { advance_text = "Close the door.", effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
      { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
    ], blocks = [
      { type = "paragraph", content = "She closes it. The latch clicks soft. The room is small the way the office is small but it isn't the office — there's no desk between them. Just the bed turned back and the lamp on and Frank standing now from the chair." },
      { type = "thought_bubble", props = { speaker = "npc_frank" }, content = "She came." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Come here." },
    ] },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# Pattern F fork — F1 + F2 + F3 + F4
[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },   # F2 secondary divergence
]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# NO effects. NO flag set. F4: canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets frank_bedroom_first_done + sex cascade)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits to hallway)
```

---

## §6 — Effect + predicate templates (the field-name minefield)

The #1 silent-failure mode. Per `schema/02_toml_schema.md` §16.

### §6.1 — Reference card (KEEP HANDY)

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Mixing them produces silent no-ops — NO BUILD ERROR FIRES.**

### §6.2 — Trait effect templates

```toml
# Player trait — add
{ targetType = "player", trait = "corruption", op = "add", value = 1 }

# Player trait — set (climax reset)
{ targetType = "player", trait = "arousal", op = "set", value = 0 }

# Player trait — decay via negative add (NO "sub" op)
{ targetType = "player", trait = "energy", op = "add", value = -10 }

# NPC trait — add
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }

# NPC trait — with cap (family NPC arousal max 3)
{ targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 }

# Stage advancement — on PLAYER namespace, NOT npc namespace
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

### §6.3 — Flag effect templates

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

### §6.4 — Predicate (condition) templates

```toml
# Trait conditions
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 }
{ type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 }

# Stage check — on PLAYER namespace
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Flag conditions
{ type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" }
{ type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" }

# Clothing predicates (Doc 72)
{ type = "worn_type", operator = "eq", value = "swim" }
{ type = "worn_beauty", operator = "gte", value = 30 }
{ type = "worn_corruption", operator = "gte", value = 15 }

# Item / pass / quest
{ type = "item", subject = "player", item_id = "pregnancy_test", operator = "gte", value = 1 }
{ type = "pass", pass_id = "gym_membership", operator = "is_active" }
```

### §6.5 — Common mistakes

| Wrong | Right | Why |
|---|---|---|
| `{ type = "trait", targetType = "player", trait = "x", op = "gte", value = 5 }` | `{ type = "trait", subject = "player", trait_key = "x", operator = "gte", value = 5 }` | Predicate uses `subject`/`trait_key`/`operator`; this looks like effect syntax |
| `{ subject = "player", trait_key = "x", op = "add", value = 1 }` | `{ targetType = "player", trait = "x", op = "add", value = 1 }` | Effect uses `targetType`/`trait`; this looks like predicate syntax |
| `{ targetType = "player", trait = "energy", op = "sub", value = 10 }` | `{ targetType = "player", trait = "energy", op = "add", value = -10 }` | No `sub` op; use negative `add` |
| `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }` | `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }` | Stage lives on player namespace as `<slug>_stage` |
| `{ targetType = "npc", trait = "corruption", op = "add", value = 1 }` | `{ targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 }` | NPC effects require `npcId` |

---

## §7 — Quest card templates

### §7.1 — Capstone-mode card

Points at a Lane 4 capstone. Has `ready_canvas`. May have `goals` for climbing display (D50-R2).

```toml
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]
```

**Note:** quest card conditions use FLAT shape (`flag` + `op`, NOT `type` + `flag_key` + `operator`). Different from trigger conditions. See `schema/02_toml_schema.md` §16.5.

### §7.2 — Pure-mechanic card

No `ready_canvas`. `goals` block tracks the climb. `# unlocks:` comment names what crosses at threshold (D50-R5).

```toml
[[quest_cards]]
# unlocks at npc_marge.relation >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 ("hon, which is it today")
#     to T1 ("There she is. Coffee's fresh.")
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
```

### §7.3 — Terminal card

`terminal = true`. Last card in NPC chain. Renders "✓ Arc complete" (D50-R3).

```toml
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

### §7.4 — Pure-mechanic chain (Marge M3/M4/M5 pattern)

Bounded `when` ranges so picker swaps atomically as threshold crosses (D50-R2 + D54 §4.3).

```toml
[[quest_cards]]
# unlocks at marge.relation >= 5: greeting tier-1 line
text   = "I've been getting my hours."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 5 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5, label = "Marge trust" }]

[[quest_cards]]
# unlocks at marge.relation >= 15: marge_hub menu item "Talk shop"
text   = "She lets me sit at the counter now."
npc_id = "npc_marge"
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5 },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 15 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 15, label = "Marge trust" }]
```

---

## §8 — Sidebar item templates

Per `doctrine/09_trait_catalog.md` §8 + `reference/04_rts_hud_world_model.md` §3.

### §8.1 — Maya state (mandatory across all RTS-shape games)

```toml
# Banded corruption
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore", icon = "💦" },
]

# Arousal bar
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
bands = [
  { min = 0, max = 2, text = "Cold" },
  { min = 3, max = 5, text = "Warm" },
  { min = 6, max = 8, text = "Hot" },
  { min = 9, max = 10, text = "Burning" },
]

# Body-state — energy
[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted", icon = "🪫" },
  { min = 25, max = 49, text = "Tired", icon = "💤" },
  { min = 50, max = 74, text = "Fine", icon = "🟢" },
  { min = 75, max = 100, text = "Rested", icon = "🔋" },
]

# Body-state — hygiene
[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0, max = 24, text = "Filthy", icon = "🧫" },
  { min = 25, max = 49, text = "Dirty", icon = "🌫️" },
  { min = 50, max = 74, text = "Fresh", icon = "🪞" },
  { min = 75, max = 100, text = "Clean", icon = "🧼" },
]
```

### §8.2 — Tier 2 stats (declare only if game uses)

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "fitness"
label = "Fitness"
max = 100
# (if exercise/gym mechanic exists)

[[sidebar_items]]
type = "trait_bar"
trait = "exhibitionism"
label = "Exhibition"
max = 100
bands = [
  { min = 0, max = 24, text = "Modest" },
  { min = 25, max = 49, text = "Open" },
  { min = 50, max = 74, text = "Bold" },
  { min = 75, max = 100, text = "Brazen" },
]
# (if flash/cam arc exists)
```

### §8.3 — Per-NPC radar (Doc 64 PRD pending — author against future shape)

When Doc 64 ships, `npc_location` sidebar item type becomes available:

```toml
# Family/ambient default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_frank"
label = "Frank"
stats = ["arousal", "corruption", "relation"]

# Slow-burn family default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_jake"
label = "Jake"
stats = ["arousal", "relation"]

# Peer/dating default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_ryan"
label = "Ryan"
stats = ["relation"]

# Service default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_marge"
label = "Marge"
stats = ["relation"]

# Antagonist — LOCATION ONLY (no stats)
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_diana"
label = "Diana"
stats = []
```

### §8.4 — DO NOT surface

- **No `<slug>_stage` sidebar items** for ANY NPC (per `doctrine/09_trait_catalog.md` §9)
- **No `awareness` sidebar item** for antagonist NPCs (per Doc 30 §6 + `doctrine/09_trait_catalog.md` §8)
- **No money sidebar item with banded poverty/wealth** unless game design specifically calls for banded display

---

## §9 — Worked example

Below is a complete TOML emission for a minimal 3-NPC 1-location slice — enough to demonstrate the full structure. Production games would have ~20-50K lines of TOML for a full slice; this is the shape, not the volume.

```toml
schema_version = "1.0"

[project]
slug = "minimal_slice"
title = "Minimal Slice"
description = "Demonstration TOML — 3-NPC RTS-shape sandbox skeleton."
quests_engine = "v2"

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

clothing_enabled = true
phone_enabled = false
rent_enabled = true
rent_amount = 60
rent_due_day = "Sunday"

# ───── Player ─────
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
frank_stage = 0
marge_stage = 0
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0

# ───── NPCs ─────
[[npcs]]
id = "npc_frank"
name = "Frank"
description = "48. Broad through the shoulders, calloused hands. Salt-and-pepper hair, work boots by the door. Owns the property."
portrait = "frank.jpg"
core_traits = { arousal = 0, corruption = 0, relation = 0 }
arc_stages = ["Suspicious", "Grudging warmth", "Restrict", "Tease", "Cracked"]

[npcs.trait_decay]
relation = 0.5

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs]]
id = "npc_marge"
name = "Marge"
description = "Late 40s. Diner owner. Apron, pencil behind her ear."
portrait = "marge.jpg"
core_traits = { relation = 0 }
arc_stages = ["Indifferent", "Trusted"]

[[npcs.schedules]]
location = "loc_diner_front"
weekdays = [0, 1, 2, 3, 4, 5]
start_time = "09:00"
end_time = "22:00"
activity = "running the diner"

[[npcs]]
id = "npc_diana"
name = "Diana"
description = "40s. Frank's wife / Maya's mother. Estranged."
portrait = "diana.jpg"
core_traits = { relation = 5, awareness = 0 }
# arc_stages = [] for antagonist

[[npcs.schedules]]
location = "loc_dianas_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "21:30"
end_time = "07:30"
activity = "her bedroom"

# ───── Locations ─────
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "The hallway between the bedrooms."
is_container = true
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_dianas_bedroom", "loc_kitchen", "loc_living_room", "loc_bathroom", "loc_main_street"]

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
description = "Worn tile, white cabinets, kettle on the gas burner."
entry_from = "loc_hallway"

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "His room. The bed against the far wall."
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."

[[locations]]
id = "loc_main_street"
name = "Main Street"
description = "The town's one street."
is_container = true

[[locations]]
id = "loc_diner_front"
name = "Diner"
description = "Marge's diner. Counter + booths + open kitchen."
entry_from = "loc_main_street"

# ───── Daily tick ─────
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_marge_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]

# ───── Sidebar ─────
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0, max = 24, text = "Pure" },
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
  { min = 0, max = 24, text = "Filthy" },
  { min = 25, max = 49, text = "Dirty" },
  { min = 50, max = 74, text = "Fresh" },
  { min = 75, max = 100, text = "Clean" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted" },
  { min = 25, max = 49, text = "Tired" },
  { min = 50, max = 74, text = "Fine" },
  { min = 75, max = 100, text = "Rested" },
]

# ───── Clothing ─────
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

# ───── Capstone canvases (Lane 4) authored FIRST so other canvases can reference them ─────

# Type A — Marge hire
[[canvases]]
id = "canvas_marge_interview"
name = "Marge — interview"
description = "Hire capstone. Type A linear."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false
priority      = 9
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
targetType = "location"
locationId = "loc_diner_front"
time_progression_minutes = 30
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "relation", op = "add", value = 5 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },
]

# Type A — Frank catch capstone
[[canvases]]
id = "scene_livingroom_catch"
name = "The catch"
description = "Frank catches Maya at evening. Stage 1→2 transition. Type A capstone."

[canvases.trigger]
location      = "loc_living_room"
is_repeatable = false
priority      = 10
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"

[[canvases.nodes]]
id = "catch"
name = "The catch"
blocks = [
  { type = "image", props = { file = "scenes/catch.jpg" } },
  { type = "paragraph", content = "He's there before you hear him." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Door open. Always. From now on. Where I can see you." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Lower your eyes."
flagEffects = [{ targetType = "player", flag = "frank_caught", op = "set" }]
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 5 },
  { targetType = "player", trait = "frank_stage", op = "set", value = 2 },
  { targetType = "npc", npcId = "npc_diana", trait = "awareness", op = "add", value = 1 },
]
targetType = "location"
locationId = "loc_living_room"

# ───── Lane 1 hub canvas (Frank kitchen morning) ─────
[[canvases]]
id = "frank_kitchen_morning_hub"
name = "Kitchen — Frank, morning"
description = "Lane 1 hub. Locked-visible escalation ladder."

[canvases.trigger]
location      = "loc_kitchen"
requires_npc  = "npc_frank"
is_repeatable = true
priority      = 8
npc           = "npc_frank"
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time   = "09:00"

[[canvases.nodes]]
id = "base"
name = "Kitchen — morning"
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 5+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Leave."
targetType = "location"
locationId = "loc_hallway"

# (Continue with Lane 2 ambients + Lane 3 dispatchers + remaining capstones + quest cards)

# ───── Quest cards ─────
# Frank F1 capstone-mode card (pre-catch)
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]

# Marge M1 capstone-mode card (pre-hire)
[[quest_cards]]
text         = "I need work. Diana said Marge runs the only place that hires off the street."
ready_text   = "She's at the register."
tip          = "Walk in. Ask."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when = [
  { flag = "hired_at_diner", op = "is_false" },
]
```

(Full TOML would continue with all remaining canvases per design book §4 lane maps.)

---

## §10 — Anti-patterns to catch (self-audit)

Before delivering the TOML, run this audit.

### §10.1 — Undeclared traits

`grep` every effect + every condition for trait names. Every name MUST appear in `[player.core_traits]` OR the appropriate NPC's `core_traits` block.

```bash
# Mental grep — for each "trait = X" in effects, X is in core_traits
# For each "trait_key = X" in predicates, X is in core_traits
```

Sidebar items hard-fail on undeclared traits (build error). Effects + conditions silently no-op (NO BUILD ERROR — drift accumulates invisibly).

### §10.2 — Field-name mixing

Common mistakes per §6.5. Search for:
- `subject = "player"` paired with `trait` (effect field) → predicate using effect names — silent no-op
- `targetType` paired with `trait_key` (predicate field) → effect using predicate names — silent no-op
- `op = "sub"` → no such op; rewrite as `op = "add"` + negative value
- `trait = "stage"` with `targetType = "npc"` → wrong namespace; stage is `<slug>_stage` on player

### §10.3 — Capstone trigger fingerprint (D57-R1)

For every priority ≥ 9 + `is_repeatable = false` (or `is_repeatable = true` + flag-gate) canvas:
- Must have flag-setter effect on at least one exit choice
- Must have `flag_is_false` self-gate in conditions
- Must be referenced by some quest card's `ready_canvas` (per D50-R1) OR have `# off-panel:` comment

### §10.4 — Lane 4 capstone is referenced by quest card

Run mental grep: for every capstone canvas (priority ≥ 9), is there a quest card with `ready_canvas = "<that canvas id>"`?

If not, add the card OR add `# off-panel:` comment. Otherwise the capstone is unreachable from the player's quest panel.

### §10.5 — Quest card chain continuity (D50-R4)

For every quest card with a flag in its `when` clause: is there ANOTHER quest card that points at the canvas that sets that flag (via `ready_canvas`)?

If not, the flag is unreachable from a card pointer — chain is broken.

### §10.6 — Terminal placement (D50-R3)

For every `terminal = true` card: is its `when` flag the LAST flag in the NPC's chain? Any other card with `when` requiring a flag set AFTER terminal's flag is a violation.

### §10.7 — Pure-mechanic card has `# unlocks:` comment (D50-R5)

For every quest card with `goals` but no `ready_canvas`: is there a `# unlocks: <slug>` comment naming what content opens at threshold?

If not, the card may point at vapor — threshold crosses, nothing changes.

### §10.8 — Goal labels in Maya-voice (D50-R6)

Every `goals[i].label` is in Maya-voice ("Maya's corruption", "Frank trust", "Diana noticing"). NOT raw trait keys ("corruption", "npc_diana.awareness").

### §10.9 — Lane 3 substitution target has `substitution_only = true` + `max_triggers_per_day = 1`

Per D67-R7. Without `substitution_only`, the target appears as a clickable surface in portrait grids. Without `max_triggers_per_day = 1`, same scene can fire multiple times per day — breaks the once-per-day cadence.

### §10.10 — Sidebar items don't surface stage / antagonist awareness

Grep `[[sidebar_items]]` for any item with `trait = "<slug>_stage"` or `trait = "awareness"` (on antagonist NPC). Both are violations.

### §10.11 — Contraception language when bareback default applies (Doc 30 §7.3.1)

**Applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`.

Grep all scene-body prose for: `condom`, `pull out`, `birth control`, `pill`, `careful`, `pregnant` (in pre-Phase-2 contexts).

All family/ambient sex scenes ship BAREBACK with no contraception language. Phase 2+ pregnancy retrofit (whether shipped in this game or deferred) will add parallel pregnant variants; contraception language BLOCKS retrofit.

**Exception — when this rule INVERTS:** at `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = include`, contraception language is ALLOWED in pre-pregnancy phase scenes (gates the pregnancy mechanic — without "careful" framing the pregnancy beat lands without setup). Pregnancy-variant scenes ship bareback with breeding talk per `doctrine/08_kink_vocab_ceilings.md` Tier 5+. In this mode, contraception language in post-pregnancy scenes still BANNED (breaks immersion).

### §10.12 — Legacy vocabulary

Grep for `Jack's World`, `New In Town`, `Two Weeks`, `Pattern A` / `B` / ... / `J` (outside Doc 67 dispatcher context), `7-driver`, `archetype`, `whiteboard goals`, `narrative gates`, `income channels`.

Zero hits expected outside of `00_LEGACY_IGNORE.md` (which the TOML doesn't include anyway).

---

## §11 — Quality gate (self-audit checklist)

Run this BEFORE delivering the TOML.

### Trait + flag declarations
- [ ] Every player trait used in any effect/condition/sidebar is declared in `[player.core_traits]`
- [ ] Every NPC trait used is declared in that NPC's `core_traits` block
- [ ] Every `<slug>_stage` trait declared in `[player.core_traits]` (one per arc-having NPC)
- [ ] Stage advancement effects use `targetType = "player"` + `trait = "<slug>_stage"` (NOT `targetType = "npc"`)

### Field names
- [ ] Effects use `targetType` / `npcId` / `trait` / `flag` / `op`
- [ ] Predicates use `subject` / `npc_id` / `trait_key` / `flag_key` / `operator`
- [ ] No `op = "sub"` anywhere (use `op = "add"` + negative value for decay)
- [ ] Quest card conditions use FLAT shape (`flag` + `op`, NOT `type` + `flag_key`)

### Lane fingerprints
- [ ] Every Lane 1 hub has `is_repeatable = true` + `priority` ~5-10 + `requires_npc` + schedule
- [ ] Every Lane 2 ambient has `trigger_mode = "random"` + `chance` + `max_triggers_per_day = 1`
- [ ] Every Lane 3 dispatcher parent has `[[canvases.trigger.substitutions]]` rule(s)
- [ ] Every Lane 3 substitution target has `substitution_only = true` + `requires_npc` + `max_triggers_per_day = 1`
- [ ] Every Lane 4 capstone has `is_repeatable = false` (or `true` + self-gate) + `priority ≥ 9` + setter-flag exit + flag-is_false gate

### Quest cards
- [ ] Every Lane 4 capstone is referenced by some quest card's `ready_canvas` (OR `# off-panel:` comment on canvas)
- [ ] Every climbing capstone card has `goals` block when `ready_canvas` has trait gates above `when` (D50-R2)
- [ ] Every pure-mechanic card has `# unlocks:` comment naming what crosses (D50-R5)
- [ ] Terminal card is the LAST in NPC chain (D50-R3)
- [ ] Every `goals[i].label` is in Maya-voice (D50-R6)

### Sidebar
- [ ] Maya state: corruption (banded) + arousal (bar) + energy (status text) + hygiene (status text) all present
- [ ] No `<slug>_stage` sidebar items for ANY NPC
- [ ] No `awareness` sidebar item for antagonist NPCs
- [ ] Body-state surfaces (energy + hygiene visible)

### Voice + content
- [ ] All Lane 1/2/3 prose is RTS-flat (≤30-word caption density; no atmospheric sensory detail; one beat = one click)
- [ ] All Lane 4 capstone prose earns Tier-3 register (per `doctrine/05_rts_flat_prose.md` §3 — specific, layered, character-distinguishing)
- [ ] Contraception language compliance per §10.11 (BANNED when bareback default applies; ALLOWED in pre-pregnancy scenes when `scope_mode: full_game` + `pregnancy = include`; Doc 30 §7.3.1)
- [ ] No legacy vocabulary (Pattern A–J as macros, 7-driver archetypes, whiteboard goals, etc.)
- [ ] Per-NPC vocab ceilings honored (daddy at Frank Tier 4+ when in scope, incest callouts at Jake Tier 3+, etc.)

### Cross-arc + retrofit
- [ ] Pregnancy retrofit-compatible (bareback throughout; no `pregnancy.*` traits authored; Phase 2+ deferred per Doc 65)
- [ ] Diana awareness writes from Frank scenes accumulate correctly (when applicable)
- [ ] Cross-NPC flag dependencies form a valid DAG (no circular dependencies)

### Validator
- [ ] Run `python manage.py package_from_toml --file <path> --owner-id <uuid> --output <path> --dev`
- [ ] Zero validator errors
- [ ] Known warnings only (e.g., pre-existing schedule overlaps that LO has accepted)

If any checklist item fails: rewrite the offending section BEFORE delivery. **Do not deliver TOML you haven't validated locally** — validator failures shipped to LO mean LO becomes the test runner (Doc 54 §7.3 anti-pattern).

---

## §12 — Common mistakes during emission

Consolidated from Doc 54 + slice authoring experience.

### §12.1 — Forgetting to declare a trait

You write `{ targetType = "player", trait = "calculation", op = "add", value = 1 }` in an effect. You forget to add `calculation = 0` to `[player.core_traits]`. The build succeeds. The effect silently no-ops at runtime. The player never accumulates the trait. The downstream content gated on `calculation >= N` never unlocks.

**Detection:** mental grep AFTER emission — for every `trait = "X"` in effects + `trait_key = "X"` in predicates + `trait = "X"` in sidebar items, X is in `core_traits`.

### §12.2 — Field-name slip mid-emission

You start with predicate syntax (`subject = "player"`) and copy-paste while building a similar effect — but the effect needs `targetType = "player"`. Engine silently no-ops the effect. Same drift as §12.1.

**Detection:** for every `subject = X` line, check the context — should be inside `items = [...]` (predicate). For every `targetType = X` line, check context — should be inside `effects = [...]` or `flagEffects`.

### §12.3 — Stage on NPC namespace (wrong)

You write `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. The engine looks for stage on `npcs.frank.core_traits.stage` (doesn't exist). Silent no-op.

**Right:** `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. Stage lives on player namespace as `<slug>_stage` per `doctrine/09_trait_catalog.md` §9.

### §12.4 — Capstone without flag-setter

You write a capstone canvas with `is_repeatable = false` + `priority = 9` + conditions. But the exit choices' `flagEffects` block is empty. The canvas fires once at the gate-cross, then never again because no flag changed — but engine state still treats it as triggerable. Player can re-enter the location and... nothing happens (the canvas's conditions still pass, but the engine's cooldown layer prevents re-fire). Result: silent dead-end.

**Detection:** for every priority-9+ + is_repeatable-false canvas, grep its `exit_block.choices` for `flagEffects`. Must set the chain's setter flag.

### §12.5 — Quest card with no `ready_canvas` AND no `goals`

`txt_only` card (per D56-R6 / D50-R3). Card renders as Frame 4 (frameless narrative text only). Looks broken.

**Right:** every card has either `ready_canvas` (capstone mode) OR `goals` (mechanic mode) OR `terminal = true` (terminal). No fourth state.

### §12.6 — Quest card chain has gaps (D50-R4 violation)

Card B requires `flag_X = is_true` in its `when`. But no card has `ready_canvas` pointing at the canvas that sets `flag_X`. The flag is reachable in the game (some canvas sets it) but the quest panel has no card pointing at that canvas. Player has no narrative thread.

**Detection:** for every card's `when` flag, trace backwards — is there a card with `ready_canvas` pointing at the setter?

### §12.7 — Lane 3 substitution target without `requires_npc`

The target canvas relies on the parent activity's substitution rule conditions for NPC-presence gating, but per D67-R6 the target should have `requires_npc = "npc_<slug>"` for engine-level filtering.

Without it: the substitution rule may fire even when the NPC isn't co-located (e.g., NPC is at school per schedule but substitution evaluates only chance + extra conditions). Result: NPC "appears" in scenes when the world model says they're elsewhere.

### §12.8 — Pregnancy language when bareback default applies (Doc 30 §7.3.1)

**Applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`.

You author a Frank sex scene with the line "He pulls out at the last second." Phase 2+ pregnancy retrofit (whether shipped in this game or deferred) will need pregnant variants of this scene; the "pulls out" language BLOCKS retrofit (pregnant variant should show him cumming inside).

**Right:** family/ambient sex scenes ship BAREBACK with cum-inside framing (no breeding talk pre-Phase-2; full breeding talk Phase 2+ when pregnancy ships per §0.5 inclusions).

**Exception — when this rule INVERTS:** at `scope_mode: full_game` with `pregnancy = include`, pre-pregnancy scenes ship WITH contraception cues + careful framing (gates the upcoming pregnancy beat); post-pregnancy scenes ship BAREBACK with breeding talk per `doctrine/08_kink_vocab_ceilings.md` Tier 5+. The retrofit-block rule still applies to pre-pregnancy scenes: their language must support the pregnant variant retrofit when the pregnancy beat fires.

### §12.9 — Hub menu over-weighting (Doc 54 §3.1)

You ship a hub with 10 menu items. Per D56-R1 + Doc 54 §3.1, hubs cap at ~5 unlocked items + locked-visible escalation ladder.

**Fix:** reduce unlocked items to 1 relational base + 1 talk + 1 Leave. Add the escalation rungs as locked-visible (`show_when_locked = true`).

### §12.10 — Service NPC with Lane 2/3 surfaces (Doc 54 §3.4)

Per `doctrine/03_arc_shapes.md` §6 — service NPCs have empty Lane 2 + Lane 3 in slice. If you've authored 6 Lane 2 ambients for Marge, those surfaces shouldn't exist.

**Fix:** delete them. Empty cells are honest.

---

## §13 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 (produces this stage's input)
- `stages/03_image_finder_prompt.md` — image search per canvas (post-TOML)
- `stages/04_game_listing_prompt.md` — back-of-book blurb (post-TOML)

### Schema (PRIMARY references)

- `schema/01_engine_capabilities.md` — engine primitives + line numbers
- `schema/02_toml_schema.md` — per-section field tables + §16 field-name reference card + §17 minimal skeleton
- `schema/03_example_toml.md` — TLS Frank slice canonical excerpts (gold-standard examples per lane)

### Doctrine (consulted during emission)

- `doctrine/02_three_lanes_plus_capstone.md` — Lane mechanism + capstone types A/B/C + F1–F5
- `doctrine/04_authoring_rules.md` — D56-R1...R7 + D50-R1...R6 + D57-R1...R5 + F1...F5 + D67-R1...R7
- `doctrine/05_rts_flat_prose.md` — 8 prose rules + dual register
- `doctrine/07_anti_patterns.md` — anti-pattern catalog
- `doctrine/08_kink_vocab_ceilings.md` — per-NPC vocab register
- `doctrine/09_trait_catalog.md` — trait init requirement + Phase 2+ off-limits

### Source TOML

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 536KB shipped TLS slice. All `schema/03` examples are verbatim from this file.

---

**End of file.** Deliver the TOML per the §1.2 output shape. Validate locally before delivery. Don't truncate. Next stages: `stages/03_image_finder_prompt.md` (image search) + `stages/04_game_listing_prompt.md` (listing blurb).
