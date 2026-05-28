# Schema 03 — Example TOML (TLS Frank Slice — Canonical Authoring Examples)

**Source:** `games/the_long_summer_test/toml_phases/7_final_game.toml` (Frank slice, verified 2026-05-28).
**Authority:** Reference. Gold-standard authoring examples per Doc 66 §15.2 — the load-bearing canvases the LLM should mirror.
**Purpose:** Show, with verbatim TOML excerpts, what each pattern + lane + capstone type LOOKS like in shipped slice. Each excerpt has an explanatory frame naming which rules + patterns + anti-patterns it demonstrates.

This file is the empirical-example complement to `schema/02_toml_schema.md` (field tables) and `schema/01_engine_capabilities.md` (engine primitives).

**Per Doc 66 §15.2:** the TLS Frank slice TOML is the canonical reference for `schema/03_example_toml.md`. The Frank arc is the gold-standard authoring example. Pull excerpts from here when populating per-arc-shape briefs — don't synthesize new TOML.

---

## §1 — What this file is

Verbatim TOML excerpts from the shipped TLS slice (commit `9c2e450` working tree, 2026-05-28). Each excerpt:
- Lives at a specific line range in `7_final_game.toml`
- Demonstrates a specific lane + pattern + rule combination
- Has commentary naming which rules it follows + which anti-patterns it avoids

The excerpts are organized lane-by-lane (Lane 1 hub + route-target / Lane 2 ambient / Lane 3 dispatcher parent + substitution target / Lane 4 capstone Type A + Type B) + supporting structures (NPC + schedules + quest cards + sidebar).

**Note on completeness:** these are EXCERPTS — load-bearing canonical patterns. For the complete shipped slice, see `games/the_long_summer_test/toml_phases/7_final_game.toml`. For full schema documentation, see `schema/02_toml_schema.md`.

---

## §2 — Frank NPC block + schedules (gold standard)

**Demonstrates:** `[[npcs]]` definition + `arc_stages` declaration + per-NPC `[[npcs.schedules]]` with non-overlapping time windows.

**Source:** `7_final_game.toml:402–466`.

```toml
[[npcs]]
id          = "npc_frank"
name        = "Frank"
description = "Forty-eight. Broad through the shoulders, calloused hands with a web of small framing scars. Salt-and-pepper hair, work boots by the door. Addresses Maya by name — *Maya* — and the name lands like a door closing. Owns the property. The rent and the rules come from him."
portrait    = "frank.jpg"
core_traits = { love = 0, trust = 0, corruption = 0, arousal = 0 }
flag_keys   = []
arc_stages  = ["Suspicious", "Grudging warmth", "Restrict", "Tease", "Cracked"]

[npcs.trait_decay]
love  = 0.5
trust = 0.3

# Phase B (2026-05-14): Frank's location schedule. First-match-wins; entries are
# non-overlapping by design so getNpcLocation always returns a single answer.

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

[[npcs.schedules]]
location = "loc_yard"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "14:00"
end_time = "17:00"
activity = "yard work"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4]
start_time = "17:00"
end_time = "19:30"
activity = "dinner prep"

[[npcs.schedules]]
location = "loc_living_room"
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"
activity = "evening"

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time = "23:00"
activity = "winding down"

[[npcs.schedules]]
location = "loc_hallway"
weekdays = [5, 6]
start_time = "21:30"
end_time = "23:00"
```

### Key features

- **`arc_stages = [...]`**: list of stage NAMES (display strings). Frank has 5 stages. The CURRENT stage integer lives on the player namespace as `player.core_traits.frank_stage` (per `doctrine/09_trait_catalog.md` §9).
- **`core_traits`**: 4 traits declared at game start. Engine reads `(npc.core_traits || {})[key]` — undeclared = silent garbage; sidebar items referencing undeclared traits hard-fail.
- **`trait_decay`**: per-NPC daily decay map. `love` decays 0.5/day; `trust` decays 0.3/day. NPCs Maya neglects lose relationship slowly.
- **7 schedule entries**: non-overlapping coverage of 24h. `getNpcLocation` (`v2.py:2923`) scans these to compute Frank's current location at any time.
- **Weekend variant**: weekdays = [5,6] vs [0,1,2,3,4] gives Saturday/Sunday a different evening pattern (Frank in the hallway 21:30-23:00 weekend instead of living room then bedroom).

### Anti-patterns avoided

- **Overlapping schedules**: each entry's time window is non-overlapping with siblings. Engine first-match-wins on time scan; overlapping entries would produce indeterminate `getNpcLocation` returns.
- **Hidden stage on NPC**: `arc_stages` is the LIST of stage names; the current stage integer lives at `player.core_traits.frank_stage`. Wrong: `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. (See `doctrine/09_trait_catalog.md` §9.)

---

## §3 — Lane 1 hub canvas (gold standard)

**Demonstrates:** Lane 1 hub with `requires_npc` + locked-visible escalation ladder + `show_when_locked` + RTS-direct verbs.

**Source:** `7_final_game.toml:5353–5460` (excerpt).

```toml
[[canvases]]
id          = "frank_kitchen_morning_hub"
name        = "Kitchen — Frank, morning"
description = "Always-show RTS ladder hub for Frank in kitchen, morning slot (daily 05:30-09:00). 2026-05-17 hub-collapse: 4 rungs (Tease/Flash/Suck/Have-sex) + Pour coffee + Leave; locked rungs shown greyed (show_when_locked). Suck + Have-sex route to loop_franks_bedroom_sex.intro. Sex gate unified at corr 25."

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
# 2026-05-25 R1 collapse — Doc 56 R1: hub openings stay constant within a canvas.
# Three tier blocks (frank_caught is_false / is_true+cracked is_false / cracked is_true)
# were authoring overhead. The menu rungs already encode progression via show_when_locked
# + per-choice conditions. Opening collapsed to one constant paragraph + dialog.
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg", description = "Frank at the counter. Coffee. Paper. You in the doorway." } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

# ─── Pour him coffee — always available (relational base interaction) ──────
[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "node"
nodeId = "frank_kitchen_morning_hub.pour_coffee"
time_progression_minutes = 5

# ─── Tease him ❤️‍🔥 — corr 5+ (locked-visible) ──────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

# ─── Flash him 👀 — corr 15+ (locked-visible) ──────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Flash him 👀"
targetType = "node"
nodeId = "flash_kitchen_general.base"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }

# ─── Suck him here. — corr 25+ (locked-visible) ────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Suck him here."
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag",  subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
effects = [
  { targetType = "player", trait = "sex_stage",            op = "set", value = 1, clamp = false },
  { targetType = "player", trait = "sex_entry_origin",     op = "set", value = 1, clamp = false },
]

# ─── Have sex with him here 🔥 — corr 25+ (locked-visible) ─────────────────
[[canvases.nodes.exit_block.choices]]
text = "Have sex with him here 🔥"
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag",  subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
# ... + effects for the sex loop entry
```

### Key features

- **`requires_npc = "npc_frank"`**: Lane 2/3 NPC-presence gate (Phase A 2026-05-14). Engine ANDs `getNpcLocation("npc_frank") === "loc_kitchen"` with all other gates. Frank's schedule (§2) places him in kitchen 05:30–09:00, so the canvas fires only during his morning slot.
- **`priority = 10`**: hub priority. Lane 4 capstones at the same location use `priority ≥ 9` to win against this hub.
- **`is_repeatable = true`**: hub re-fires every visit. Distinct from Lane 4 capstones which use `is_repeatable = false`.
- **Constant opener** (post-Doc 56 R1 collapse): one paragraph + dialog. No tier-routed group blocks for the opening. Progression-aware behavior lives in the menu rungs, not the opening prose.
- **Locked-visible escalation ladder**: Tease (corr 5+) / Flash (corr 15+) / Suck (corr 25+) / Have sex (corr 25+). All four rungs have `show_when_locked = true` — visible from day 1 even at Stage 0, telegraphing the arc shape.
- **`locked_text_threshold`** (not shown in this excerpt): per `doctrine/04_authoring_rules.md` §3 P7 — locked-click publishes the threshold, no stat drain.
- **Pronoun-in-the-verb test passes**: all menu verbs have NPC as object — "Pour HIM coffee" / "Tease HIM" / "Suck HIM" / "Have sex with HIM."

### Rules + patterns demonstrated

- **D56-R1**: hub opener constant (no T0/T1/T2 group blocks for opening)
- **D56-R7**: gated rungs ship with `show_when_locked = true` (the locked-visible ladder)
- **P5**: Lane 1 = intentional escalation; verbs match (Maya owns the act)
- **P10**: requires_npc consults the sidebar/`getNpcLocation`; the world model is the gate

### Anti-patterns avoided

- **Lane 1 over-weighting (Doc 54 §3.1)**: hub has 5 items (Pour + Tease + Flash + Suck + Sex) + Leave. Cap at ~5 unlocked items honored.
- **Verb register failure (Doc 54 §3.2)**: every menu verb has NPC as object. No "Take a long shift" / "Wash the dishes" (those are solo activities, parallel surfaces).
- **Missing locked-visible ladder (Doc 54 §4.5)**: all 4 escalation rungs visible from Stage 0.
- **Tiered hub opener (Doc 56 R1)**: post-2026-05-25 collapse — opener is one constant paragraph, not 3 tier blocks.

---

## §4 — Lane 1 route-target stub (route-only pattern)

**Demonstrates:** route-target canvas with NO `[canvases.trigger]` block + internal `[group]` tier-routing.

**Source:** `7_final_game.toml:5207–5260` (excerpt).

```toml
[[canvases]]
id          = "tease_kitchen_general"
name        = "Kitchen — tease him"
description = "Stub Pattern A render: corr 5+ kitchen general tease. Maya catches his eye, holds it, looks away. 1-beat. Reachable only via frank_kitchen_morning_hub menu item."

# NOTE: NO [canvases.trigger] block. This canvas only reachable via nodeId
# routing from a hub menu item. Frank's tease/flash pattern.

[[canvases.nodes]]
id   = "base"
name = "Kitchen — tease him"
blocks = [
  { type = "image", props = { file = "scenes/tease_kitchen_general.jpg", description = "You. Mug at your mouth. Held look across the kitchen." } },

  # T0 (pre-catch): held look, nothing else
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye over the mug and hold it. He's still looking when you look back." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Girl." },
  ] } },

  # T1 (post-catch, pre-cracked): he openly looks at your tits
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. His look drops to your tits and stays there — he doesn't pretend he wasn't looking." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Mm." },
  ] } },

  # T2 (post-cracked): he steps in, backs you against the counter
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. He sets the mug down, crosses to you, backs you against the counter — hand under your shirt, thumb on your nipple." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't fucking start with me at breakfast, girl." },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# WEAN @15 (2026-05-21): trivial self-display stops paying PLAYER corruption past 15.
# lt/gte mutex on one same-text button — exactly one renders.
[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 15 },
]}
effects = [
  { targetType = "npc",    npcId = "npc_frank", trait = "arousal",    op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]
```

### Key features

- **NO `[canvases.trigger]` block**: this canvas isn't a clickable surface. It's only reachable via `nodeId = "tease_kitchen_general.base"` from `frank_kitchen_morning_hub.exit_block.choices`.
- **Internal tier-routing via `[group]` blocks**: three tiers (T0 pre-catch / T1 post-catch / T2 post-cracked) gated on flag state. Same scene grows in intensity as Maya's arc advances.
- **Lt/gte mutex on exit**: at corruption < 15, click grants +1 corruption. At corruption ≥ 15 (the trivial-display wean), the same-text button has a different conditions block (not shown here) — no player corruption tick. The mutex means exactly one button renders.

### Rules + patterns demonstrated

- **Route-target stub pattern (Doc 54 §6.1)**: NO `[canvases.trigger]` — reachable only via hub routing
- **P3** (one scene, multiple lengths) via `[group]` tier-routing
- **D56-R2**: T0 + T1 endings are slim ("Girl." / "Mm.") — they read as "more is possible at higher tier" without an explicit in-fiction interruption. T2 blows through (he crosses to her, hand under shirt).

### Anti-patterns avoided

- **Stub with trigger block (Doc 54 §6.1)**: Frank's tease/flash/sex canvases are route-only. Authoring with a trigger block would produce validator overlap warnings + make the stub directly clickable (defeats the routing purpose).

---

## §5 — Lane 2 ambient with R2 in-fiction interruption (gold standard)

**Demonstrates:** Lane 2 random encounter + `trigger_mode = "random"` + `chance` + tier-routed cascade with in-fiction interruption at T0 ending (Doc 56 R2 / D56-R2).

**Source:** `7_final_game.toml:5802–5889`.

```toml
[[canvases]]
id          = "ambient_kitchen_frank_late_night_raid"
name        = "Kitchen — late night, both up for water"
description = "Lane 2 ambient: midnight kitchen encounter. Entry corr 25+. 2 stage-flag tiers (T0 pre-first-night makeout broken by Diana's floorboard / T1 post-first-night bareback counter quickie + daddy call/response before Diana wakes). NOTE: NO requires_npc — Frank scheduled bedroom / hallway this hour; the ambient's premise is 'neither was supposed to be here' — Frank stepped out for water, presence implied by the ambient itself."

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
  { type = "image", props = { file = "scenes/ambient_kitchen_frank_late_night_raid.jpg", description = "Kitchen near midnight, one bulb. Frank in sleep pants, no shirt. You in a long nightshirt. House dark." } },
  { type = "paragraph", content = "You didn't think anyone was awake; the kitchen light's already on. Frank's at the sink in sleep pants and nothing else, a glass of water in his hand." },

  # T0 (frank_first_night_done is_false): midnight makeout, broken by Diana's floorboard
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "ambient_kitchen_frank_late_night_raid_t0_cascade", beats = [
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
      { advance_text = "Hear the floorboard upstairs.", blocks = [
        { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },

  # T1 (post-first-night): they don't stop — bareback counter quickie before Diana wakes
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_true" },
    ] }, blocks = [
    { type = "cascade", props = { id = "ambient_kitchen_frank_late_night_raid_t1_cascade", beats = [
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
  { targetType = "npc",    npcId = "npc_frank", trait = "arousal",    op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc",    npcId = "npc_frank", trait = "corruption", op = "add", value = 1 },
  { targetType = "player",                       trait = "corruption", op = "add", value = 2 },
  { targetType = "player",                       trait = "energy",     op = "add", value = -18 },
  { targetType = "npc",    npcId = "npc_diana", trait = "awareness",  op = "add", value = 2 },
]
```

### Key features

- **`trigger_mode = "random"` + `chance = 0.40`**: dispatched by `checkRandomEncounters` on location entry. 40% probability per visit (when conditions met).
- **`max_triggers_per_day = 1`**: same canvas can't fire twice in a day.
- **NO `requires_npc`**: deliberate per the description — the ambient's premise is "Frank stepped out for water" (implied presence), so no schedule gate. Doc 67 R6 doctrine adapted: implied-presence overrides loose presence check.
- **Two-tier `[group]` cascade**: T0 (pre-first-night) + T1 (post-first-night). Same canvas, different cascade depending on flag state.
- **R2 in-fiction interruption at T0**: T0 ending is "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." The interruption is EXTERNAL (Diana's footsteps stop the cascade). T1 explicitly blows through: "He fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs."
- **Cross-arc state write**: `npc_diana.awareness +2`. The Diana arc reads this; high awareness eventually triggers `scene_diana_confrontation` capstone.

### Rules + patterns demonstrated

- **D56-R2 gold standard**: T0 ending lands on in-fiction interruption (Diana's floorboard); T1 explicitly blows through.
- **P3**: one scene, multiple lengths — same canvas grows in intensity at higher tier.
- **P5**: Lane 2 = ambient coexistence; "you walked into the kitchen and Frank was there" framing.
- **P8**: mechanism (cascade with conditional groups) carries the daily texture; the once-only Frank-Diana confrontation gets the Tier-3 capstone authoring.

### Anti-patterns avoided

- **Clean T0 ending (Doc 56 R2 violation)**: T0 does NOT end on a complete-feeling beat. The Diana interruption signals "more is here." P3's "you saw the short version" cue is preserved.
- **Tier-3 leakage in Lane 2 (Doc 57 §9)**: voice register stays RTS-flat with specific detail. Frank's "Quiet, girl." / "Knew you'd come down." carry character without literary cadence. Tier-3 prose reserved for capstones.

---

## §6 — Lane 3 dispatcher parent (Pattern A multi-NPC-ready)

**Demonstrates:** Maya-solo activity with `[[canvases.trigger.substitutions]]` rule + Lane 3 dispatcher mechanism.

**Source:** `7_final_game.toml:8175–8216`.

```toml
[[canvases]]
id          = "activity_make_tea"
name        = "Make a cup of tea"
description = "Maya-solo dispatcher. Kitchen, T1. Maya makes a cup of tea at the counter (kettle, bag, hot water). Substitution target: scene_frank_passes_kitchen_door."

[canvases.trigger]
location      = "loc_kitchen"
is_repeatable = true
priority      = 3
is_active     = true
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_passes_kitchen_door"
chance           = 0.30
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "07:00"
end_time   = "22:00"

[[canvases.nodes]]
id   = "base"
name = "Make a cup of tea"
blocks = [
  { type = "image", props = { file = "activities/make_tea.jpg", description = "Kitchen counter. Kettle on the gas burner. Maya at the counter with a mug, tea bag tag hanging over the rim. Window light." } },
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
flagEffects = []
```

### Key features

- **Maya-solo body**: the activity prose is third-person Maya making tea. No NPC interaction in the solo branch.
- **`[[canvases.trigger.substitutions]]` rule**: 30% chance + `corruption ≥ 5` conditions → if hit, replaces this canvas's body with `scene_frank_passes_kitchen_door` (see §7).
- **`priority = 3`**: lower than NPC hubs (priority 10) and Lane 2 ambients (priority 6). The solo activity is a base-tier surface; substitutions are more interesting.
- **Stat cost on exit_block** (Pattern A placement): `+2 energy` only fires on solo branch return. If Frank's substitution preempts, Maya doesn't "complete" the tea-making — no energy gain.
- **NO `requires_npc`**: the solo body is the default. The substitution mechanism handles NPC-presence routing internally.

### Rules + patterns demonstrated

- **D67-R1**: solo activity is a separate canvas, not a sub-block of the kitchen hub.
- **D67-R2**: stat cost placement INSIDE `exit_block.effects` — costs only if Maya completes the chore.
- **D67-R3**: menu-level gating not duplicated here. The location button gates time-of-day + energy; this dispatcher trusts the menu's gating.
- **Pattern A (Doc 67 §4.1)**: sequential first-match dispatcher. Currently 1 rule; would extend to multi-NPC by adding more rules ordered by narrative priority.
- **P5**: Lane 3 = "I was doing X and he happened" — the solo body sets Maya up as authentically not-about-Frank; the substitution arrives as charged surprise.

### Anti-patterns avoided

- **Solo activity body inline in hub (Doc 67 §9)**: this activity is its own canvas, not a sub-block of `frank_kitchen_morning_hub`. Lane 3 substitutions require addressable parent canvases.
- **Time-of-day gate on dispatcher (Doc 67 §9)**: the schedule `07:00–22:00` is broad. Specific time-of-day gates live on the kitchen hub's menu button (energy/time-of-day check); the dispatcher just confirms Maya can attempt this chore.

---

## §7 — Lane 3 substitution target (tier-routed Pattern D-shape)

**Demonstrates:** `substitution_only = true` + tier-routed prose escalation with cascade.

**Source:** `7_final_game.toml:8467–8540` (excerpt).

```toml
[[canvases]]
id          = "scene_frank_passes_kitchen_door"
name        = "Kitchen — Frank passes the door while you're making tea"
description = "T1 Lane 3 substitution on activity_make_tea. Frank passes through the kitchen on his way somewhere — pauses at the door, sees her, the briefest moment. substitution_only."

[canvases.trigger]
location          = "loc_kitchen"
is_repeatable     = true
priority          = 4
is_active         = true
substitution_only = true

[[canvases.nodes]]
id   = "base"
name = "Kitchen — Frank passes the door"
blocks = [
  { type = "image", props = { file = "scenes/scene_frank_passes_kitchen_door.jpg", description = "Kitchen. You at the counter waiting on the kettle. Frank stopped close at your back instead of passing through." } },
  { type = "paragraph", content = "You're waiting on the kettle when Frank comes through the kitchen on his way to the back of the house. He doesn't pass straight through." },

  # T0 (frank_caught is_false): stops at your back, hand at your waist
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "scene_frank_passes_kitchen_door_t0_cascade", beats = [
      { blocks = [
        { type = "paragraph", content = "He stops behind you in the narrow galley instead of going by, close enough that you feel him at your back reaching past you for nothing in particular." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't mind me, girl." },
      ] },
      { advance_text = "Hold still.", blocks = [
        { type = "paragraph", content = "His hand settles at your waist a beat too long for getting by, then he's moving again, out the far door. The kettle's still not boiling." },
      ] },
    ] } },
  ] } },

  # T1 (post-catch, pre-cracked): turns you by the hip against the counter
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "scene_frank_passes_kitchen_door_t1_cascade", beats = [
      { blocks = [
        { type = "paragraph", content = "He stops at your back and turns you by the hip before you can pretend not to notice, his hand flat and low on you against the counter." },
        { type = "dialog", props = { speaker = "player" }, content = "Daddy, the kettle—" },
      ] },
      { advance_text = "Let him.", blocks = [
        { type = "paragraph", content = "He keeps you there one-handed, the other still holding his coffee, in no hurry, until the kettle starts going. Then he lets go and walks on like nothing." },
      ] },
    ] } },
  ] } },

  # T2 (post-cracked): pulls your back to his chest, hand down your front
  # ... (similar [group] block with cracked flag is_true)
]
```

### Key features

- **`substitution_only = true`**: this canvas is excluded from `renderNpcPortraits` + `renderSoloActivities` + `selectAutoFireCanvasForLocation`. Only reachable via the substitution rule on `activity_make_tea`.
- **`priority = 4`**: irrelevant for substitution-only canvases (engine doesn't priority-sort them in selection paths).
- **Three-tier `[group]` cascade**: T0 (pre-catch) / T1 (post-catch, pre-cracked) / T2 (post-cracked). Pattern D-shape — gate at top-of-group, then linear cascade within each tier.
- **Daddy register at T1+**: Maya's "Daddy, the kettle—" at T1 reflects the Doc 31 §2 daddy framing rule (Stage 3+ tease tier).
- **No exit_block** (in shown excerpt): substitution targets often end with the parent activity's exit. Or they have their own exit_block returning to the location.

### Rules + patterns demonstrated

- **D67-R7**: substitution target. Note: this canvas's `max_triggers_per_day` should be `1` per Doc 67 R7 (not visible in this excerpt — verify in full TOML).
- **P3 + R2**: tier-routed cascade with `[group]` gates. T0's "the kettle's still not boiling" is the in-fiction interruption (nothing happens; the kettle continues; Frank moves on).
- **P5**: Lane 3 = "I was doing X and he happened" — Maya is making tea; Frank passes through; he stops.
- **`doctrine/08_kink_vocab_ceilings.md` daddy register**: Maya's daddy call emerges at T1 (post-catch = Stage 3 register on).

### Anti-patterns avoided

- **Missing `substitution_only = true` (Doc 67 §9)**: without this flag, the canvas would appear as its own clickable surface in the kitchen, defeating the "you were doing X and he happened" framing.
- **Strict `getNpcLocation == "loc_kitchen"` gate (Doc 67 R6)**: Lane 3 walk-ins use loose presence (Frank at home) — he wandered into the kitchen because Maya was there. No strict-location predicate.

---

## §8 — Lane 4 capstone Type A (Marge interview — service register short form)

**Demonstrates:** Type A linear deterministic capstone + Tier-3 prose at short length + trigger fingerprint (D57-R1).

**Source:** `7_final_game.toml:1617–1665`.

```toml
[[canvases]]
id          = "canvas_marge_interview"
name        = "Marge — interview"
description = "First visit to the diner. Marge sizes Maya up in 90 seconds, hires her on the spot. Fires once, gated on `hired_at_diner == false`."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false
priority      = 9
is_active     = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg", description = "Marge behind the diner counter, late forties, broad and quick. Apron, pencil behind her ear, the look of a woman who has read the resume of every girl who walks in.", search_queries = [
    "diner owner woman behind counter apron pencil southern",
    "late forties woman diner counter coffee pot apron rural",
  ] } },

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
  { targetType = "npc", npcId = "npc_marge", trait = "trust", op = "add", value = 5 },
  { targetType = "player",                    trait = "energy", op = "add", value = -3 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },
  { targetType = "player", flag = "talked_to_marge_today", op = "set" },
  { targetType = "player", flag = "phone_active", op = "set" },
]
```

### Key features (Type A capstone fingerprint)

- **`is_repeatable = false`**: classic Type A trigger fingerprint (Doc 57 R1). Fires once.
- **`priority = 9`**: Lane 4 minimum priority (winning against Lane 2 randoms on entry).
- **Single flag-is_false gate**: `hired_at_diner is_false` is the only gate. Simple Type A.
- **Single node + single exit choice**: no fork. The "Take the apron" exit is the only path forward — the fiction is that Marge wasn't waiting for an answer.
- **Setter flag on exit**: `hired_at_diner = set` retires the canvas after the Accept path fires.
- **Tier-3 prose at 1,900 chars**: focused, not long. "The up-and-down a woman who had hired forty waitresses did. The shoes. The hands." — inferential character work + composed fragments = Tier-3 register.
- **Cross-arc flag write**: `phone_active = set`. Doc 46 — first wage in hand reactivates Maya's phone. The capstone is a hinge for a different system (phone) too.

### Rules + patterns demonstrated

- **D57-R1**: trigger fingerprint clean (is_repeatable = false + priority = 9 + flag-gate + flag-setter on exit)
- **D57-R2**: Type A simplicity preference — no Pattern F fork (Marge wasn't waiting for an answer)
- **D57-R3 / D50-R1**: capstone is referenced by quest card M1's `ready_canvas = "canvas_marge_interview"` (see §10)
- **Tier-3 voice register earned** (`doctrine/05_rts_flat_prose.md` §3): inferential character work + composed fragments + Marge-specific diction
- **P8**: author the points of no return; mechanize the texture — Marge hire is once-only, gets Tier-3; Marge's daily floor work is mechanism

### Anti-patterns avoided

- **`is_repeatable = true` capstone (Doc 57 §9)**: fingerprint is clean. Once-only behavior locked.
- **RTS-flat-bland voice in capstone (Doc 57 §9)**: the prose is Tier-3 (inferential character work). Wouldn't waste the once-only nature.
- **Capstone with no flag-setter (Doc 57 §9)**: `hired_at_diner` flag set on Accept exit. Canvas retires.

---

## §9 — Lane 4 capstone Type B with Pattern F fork (first-night)

**Demonstrates:** Type B branching capstone + Pattern F fork at terminal cascade beat + F1–F5 sub-rules.

**Source:** `7_final_game.toml:3362–3450` (excerpt; full canvas is ~350 lines including both branch nodes).

```toml
[[canvases]]
id          = "scene_franks_bedroom_evening"
name        = "Frank's bedroom — first night"
description = "Stage 4 FIRST-NIGHT cascade. Fires once when player first enters Frank's bedroom at evening — the dramatic threshold-cross moment. Pattern E linear cascade (entry-gated). Two choice exits (stay through / leave before dawn) write Stage-4 closure effects + register-distinguishing secondary stat. Entry gate: corruption ≥ 25 + frank_caught + first_done is_false."

[canvases.trigger]
location      = "loc_franks_bedroom"
requires_npc  = "npc_frank"
is_repeatable = true     # see note below
priority      = 9
is_active     = true
npc           = "npc_frank"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag",  subject = "player", flag_key  = "frank_caught",              operator = "is_true"  },
  { type = "flag",  subject = "player", flag_key  = "frank_bedroom_first_done",   operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption",                 operator = "gte",      value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time   = "23:00"

[[canvases.nodes]]
id   = "base"
name = "Frank's bedroom — evening"
blocks = [
  { type = "image", props = { file = "scenes/franks_bedroom_evening.jpg", description = "Frank's bedroom at evening. The lamp on the nightstand on. Bed against the far wall, covers turned back. Frank in a chair by the window, robe over the back of the chair. Quiet, charged." } },

  # ─── First-night cascade ─────────────────────────────────────────────
  # Cascade Beats 0/1/2 stay in base. Beat 2 is now terminal — fork choices
  # in exit_block.choices route to node_first_night_climax (Accept) or
  # node_first_night_refuse (Refuse). RTS Pattern F equivalent.
  { type = "cascade", props = { id = "frank_bedroom_first", beats = [
    # Beat 0 — opens unconditionally on scene entry. The hallway approach.
    { blocks = [
      { type = "paragraph", content = "She walks the hallway slow. The boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark. The door at the end is the door she's only ever walked past." },
    ] },

    # Beat 1 — click "Push the door open."
    { advance_text = "Push the door open.", blocks = [
      { type = "paragraph", content = "It's open by an inch. Lamp light on the floorboards. She pushes it the rest of the way and steps in." },
      { type = "paragraph", content = "Frank in the chair by the window. He's not undressed. Just sitting in the way he sits — weight on one elbow, the lamp catching the side of his face, a paperback open in his lap that he hasn't been reading. He sets it down on the nightstand without marking the page." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Close the door." },
    ] },

    # Beat 2 — terminal. Click "Close the door." Per-beat effect: Frank.arousal +1.
    # Cascade ends here; exit_block.choices below render TWO fork options.
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

# ─── FORK CHOICES — Accept / Refuse mid-cascade ─────
# RTS Pattern F equivalent. Both choices route via intra-canvas nodeId.
# Accept → node_first_night_climax (cross + sex + aftermath + standard
# overnight exits). Refuse → node_first_night_refuse (Frank stops, brief
# disengagement, exits to hallway). Refuse does NOT set
# frank_bedroom_first_done — the canvas can re-fire next eligible night.

[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# No effects. Does NOT set frank_bedroom_first_done — canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets first_done + tier-routed closing)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits)
```

### Key features (Type B + Pattern F fingerprint)

- **`is_repeatable = true` + self-gate**: the canvas is marked repeatable but conditions include `frank_bedroom_first_done is_false`. Functionally identical to `is_repeatable = false` when Accept fires (flag sets, gate fails next visit). **Refuse path leaves flag unset** → canvas re-fires next eligible night. This is the Doc 57 R1 `is_repeatable = true + flag_is_false self-gate` variant supporting F4.
- **`priority = 9` + flag gate + trait gate**: Type B fingerprint clean.
- **Cascade with TERMINAL fork beat (F3)**: Beat 2 ("Close the door.") is the cascade's last beat. The fork lives in `exit_block.choices`, not mid-cascade.
- **Per-beat effects on Beat 2**: Frank.arousal +1 + Maya.arousal +1 fire on the click. P6 (stats change during scenes).
- **Two distinct fork options (F1 + F2)**: "Cross to him." (Accept path) sets `frank_bedroom_first_done` on its climax node + Maya.corruption +1 on the cross. "Hesitate. Step back." (Refuse path) sets NOTHING — canvas re-fires next night.
- **Thought bubble on Beat 2**: `{ type = "thought_bubble", props = { speaker = "npc_frank" }, content = "She came." }` — Doc 13 §16 Finding 1 + `doctrine/05_rts_flat_prose.md` §7 4th-dimension primitive.
- **Tier-3 prose throughout**: "the boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark" — inferential character work + memory-callback + composed rhythm = Tier-3.

### Rules + patterns demonstrated

- **D57-R1**: trigger fingerprint (Type B variant with self-gate)
- **D57-R2**: Type B justified — branches diverge in flag-effect (Accept sets first_done; Refuse doesn't)
- **F1**: both branches playable in good faith (Refuse is honest no, not punishment)
- **F2**: real divergence (different flags set; different downstream content)
- **F3**: fork at terminal beat of cascade
- **F4**: Refuse keeps canvas alive for retry — Maya can hesitate tonight and accept tomorrow
- **F5 ⚠️**: F5 boundary. The climax node has T0 (corruption < 40) vs T1 (corruption ≥ 40) closing register inside the Accept branch. Two structural devices stacked — upper bound of complexity per capstone.
- **P8**: capstone gets Tier-3 prose; daily texture stays mechanism

### Anti-patterns avoided

- **F1 — Refuse-as-punishment (Doc 57 §9)**: Refuse path is "Hesitate. Step back." — honest disengagement. Not a snarky one-liner signaling "don't pick this."
- **F2 — Collapsible branches (Doc 57 §9)**: Accept sets `frank_bedroom_first_done`; Refuse doesn't. Real downstream divergence.
- **F3 — Mid-cascade fork (Doc 57 §9)**: Beat 2 is cascade-terminal. No N beats downstream of both branches.

---

## §10 — Quest cards (Frank F1–F6 + Marge M1–M2)

**Demonstrates:** Capstone-mode + mechanic-mode quest cards + chain continuity + climbing-bullet + terminal placement.

**Source:** `7_final_game.toml:2460–2580` (excerpt).

```toml
# F1 — Pre-catch climbing
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

# F2 — Post-catch / pre-first-night
[[quest_cards]]
text         = "Upstairs now. The office stays for the books."
ready_text   = "He'll be in his bedroom tonight."
tip          = "Diana down the hall. Quiet."
npc_id       = "npc_frank"
ready_canvas = "scene_franks_bedroom_evening"
when = [
  { flag = "frank_caught", op = "is_true" },
  { flag = "frank_bedroom_first_done", op = "is_false" },
]

# F3 — Post-first-night / pre-declaration
[[quest_cards]]
text         = "He took me upstairs. He hasn't said the word yet."
ready_text   = "He's going to break tonight."
tip          = "Diana's asleep by then. The hallway is dark."
npc_id       = "npc_frank"
ready_canvas = "scene_frank_declaration"
when = [
  { flag = "frank_bedroom_first_done", op = "is_true" },
  { flag = "frank_cracked", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 35, label = "Maya's corruption" },
]

# F4 — Post-declaration / pre-sleepover
[[quest_cards]]
text         = "He moved the line. The bedroom is the venue now."
ready_text   = "Tonight I don't leave."
tip          = "Diana down the hall. Quiet."
npc_id       = "npc_frank"
ready_canvas = "scene_frank_sleepover"
when = [
  { flag = "frank_cracked",         op = "is_true"  },
  { flag = "frank_sleepover_done",  op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 50, label = "Maya's corruption" },
]

# F5 — Post-sleepover / pre-Diana confrontation
[[quest_cards]]
text         = "The house feels smaller now. She's home all the time and she's watching."
ready_text   = "She's going to ask."
tip          = "She doesn't say anything. She doesn't have to."
npc_id       = "npc_frank"
ready_canvas = "scene_diana_confrontation"
when = [
  { flag = "frank_sleepover_done", op = "is_true"  },
  { flag = "diana_confronted",     op = "is_false" },
]
goals = [
  { trait = "awareness", subject = "npc", npc_id = "npc_diana", op = "gte", value = 8, label = "Diana noticing" },
]

# F6 — Post-Diana terminal
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]

# M1 — Pre-hire pointer (capstone). Points at canvas_marge_interview.
[[quest_cards]]
text         = "I need work. Diana said Marge runs the only place that hires off the street."
ready_text   = "She's at the register."
tip          = "Walk in. Ask."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when = [
  { flag = "hired_at_diner", op = "is_false" },
]

# M2 — T0 climbing toward marge.trust >= 20 (PURE MECHANIC).
[[quest_cards]]
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
# unlocks at marge.trust >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 ("You're either on the floor
#     or you're a customer, hon.") to T1 ("Coffee's fresh if you're not here to work
#     for once."). The greeting tier flip IS the entire unlock. No new menu items,
#     no new ambients, no new substitutions open at this threshold.
```

### Key features

- **F1: Capstone-mode card with climbing bullet** — `ready_canvas` set + `goals` block surfaces the corruption 0 → 25 climb. D50-R2.
- **F2: Capstone-mode card without `goals`** — D50-R2 doesn't apply because the canvas's gate (corruption ≥ 25) is already guaranteed by F2's `when` (which kicks in after `frank_caught` was set via F1's `ready_canvas`).
- **F3: Climbing-bullet on post-first-night** — `goals` surfaces the corr 25 → 35 climb between first-night and declaration. D50-R2 — this fix landed 2026-05-24.
- **F4: Sleepover capstone pointer** — `ready_canvas = scene_frank_sleepover` + corr 50 climb. D50-R1 — fix landed 2026-05-24 (sleepover was off-panel before).
- **F5: Diana confrontation pointer with NPC-stat goal** — `goals` block tracks `npc_diana.awareness` climb. D50-R6 — label "Diana noticing" in Maya-voice, not raw `npc_diana.awareness` key.
- **F6: Terminal card** — `terminal = true` placed at the LAST Frank flag (`diana_confronted`). D50-R3 — replaces old terminal at `frank_cracked` which was two scenes too early.
- **M1: Capstone-mode pointer for hire** — `ready_canvas = canvas_marge_interview`. D50-R1.
- **M2: PURE MECHANIC card** — NO `ready_canvas`. `goals` tracks trust 0 → 20. Threshold cross IS the unlock. D50-R5 `# unlocks:` comment names what crosses at threshold (greeting tier flip).

### Rules + patterns demonstrated

- **D50-R1 (capstone coverage)**: every Frank capstone has a card pointer (F1 → catch, F2 → first-night, F3 → declaration, F4 → sleepover, F5 → Diana confrontation). Marge hire covered by M1.
- **D50-R2 (climbing-bullet)**: F1 + F3 + F4 + F5 all have `goals` blocks for the trait climbs above their `when` gate. F2 correctly omits `goals` (no climb above `when`).
- **D50-R3 (terminal placement)**: F6 is the LAST card. No card requires a flag set after `diana_confronted`.
- **D50-R4 (chain continuity)**: F1's `ready_canvas` sets `frank_caught` → F2 requires `frank_caught is_true`. F2's `ready_canvas` sets `frank_bedroom_first_done` → F3 requires it. And so on.
- **D50-R5 (mechanic-tier comment)**: M2 has the `# unlocks:` comment naming the greeting tier flip.
- **D50-R6 (label voice)**: all `goals.label` entries are in Maya-voice ("Maya's corruption", "Diana noticing", "Marge trust").

### Anti-patterns avoided

- **Capstone with no card pointer (D50-R1 violation)**: every Frank capstone is referenced. Sleepover + Diana confrontation moved from off-panel to F4/F5 cards on 2026-05-24.
- **Premature terminal (D50-R3 violation)**: F6 at `diana_confronted` is the absolute last Frank flag. Old F4 at `frank_cracked` was wrong.
- **Climbing card with no `goals` bullet (D50-R2 violation)**: F3 had this violation before 2026-05-24; fixed with corruption 35+ goal.
- **Mechanic card with `ready_canvas` (D50-R5 violation)**: M2 correctly omits `ready_canvas`. Earlier draft had `ready_canvas = scene_marge_diner_hub` which violated mechanic-mode shape.

---

## §11 — Sidebar items (Maya stats — pending NPC radar)

**Demonstrates:** `[[sidebar_items]]` per Doc 49 + Doc 68 §8.

**Source:** TLS slice (extract from current `7_final_game.toml`).

```toml
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

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy", icon = "🧫" },
  { min = 25,  max = 49,  text = "Dirty",  icon = "🌫️" },
  { min = 50,  max = 74,  text = "Fresh",  icon = "🪞" },
  { min = 75,  max = 100, text = "Clean",  icon = "🧼" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0,   max = 24,  text = "Exhausted", icon = "🪫" },
  { min = 25,  max = 49,  text = "Tired",     icon = "💤" },
  { min = 50,  max = 74,  text = "Fine",      icon = "🟢" },
  { min = 75,  max = 100, text = "Rested",    icon = "🔋" },
]

# When Doc 64 PRD ships, add per-NPC items:
# [[sidebar_items]]
# type = "npc_location"
# npc_id = "npc_frank"
# label = "Frank"
# stats = ["arousal", "corruption", "relation"]    # family/ambient default per Doc 68 §8
```

### Key features

- **`trait_words` for corruption** (banded display, raw number hidden) — Doc 68 Q2 lock
- **`trait_bar` for arousal** (0–10 with bands) — Doc 40 lock
- **`trait_status_text` for body-state** (hygiene + energy) — Doc 49
- **`npc_location` items** (commented out, pending Doc 64 PRD) — when shipped, per-NPC radar with per-arc-shape stat surfacing

### Anti-patterns avoided

- **Stage surfaced (Doc 68 §9 violation)**: no `frank_stage` / `ryan_stage` / etc. sidebar items. Stage is internal-only.
- **Antagonist awareness surfaced (Doc 68 §8)**: no `diana_awareness` sidebar item (will not be added).
- **Body-state hidden (Doc 49)**: energy + hygiene visible. Player needs to know when to sleep/shower.

---

## §12 — Cross-references

### Sibling schema files

- `schema/01_engine_capabilities.md` — engine primitives referenced (`getNpcLocation`, `checkAndSubstituteCanvas`, `selectAutoFireCanvasForLocation`)
- `schema/02_toml_schema.md` — per-section field tables (TemplateNPC, TemplateNPCSchedule, TemplateCanvas, TemplateTrigger, TemplateChoice, QuestsCard, sidebar item types)

### Sibling doctrine files

- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanism + capstone types (Type A / Type B / Type C-chain)
- `doctrine/03_arc_shapes.md` — Frank = family/ambient gold standard; Marge = service gold standard
- `doctrine/04_authoring_rules.md` — all D56 / D50 / D57 / F1–F5 / D67 rules cited above
- `doctrine/05_rts_flat_prose.md` — Lane 1/2/3 RTS-flat vs Lane 4 Tier-3 register
- `doctrine/06_design_brief_template.md` — R7 brief Doc 31 (Frank) + Doc 53 (Marge) are the gold-standard briefs these canvases were authored from
- `doctrine/07_anti_patterns.md` — Doc 54 27 failure modes (Marge case study)
- `doctrine/08_kink_vocab_ceilings.md` — Frank daddy register / Marge service register / Diana cuckold framing

### Source TOML

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 536KB shipped TLS slice. All excerpts above are verbatim from this file.

### Source briefs

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — Frank brief (informed `frank_kitchen_morning_hub`, `tease_kitchen_general`, `ambient_kitchen_frank_late_night_raid`, `scene_franks_bedroom_evening`, all 5 capstones)
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — Marge brief (informed `canvas_marge_interview`, M1, M2)

---

**End of file.** Batch 2 complete pending quality gate + commit.
