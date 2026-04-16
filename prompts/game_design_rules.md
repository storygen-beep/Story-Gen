# Game Design Rules (Always Enforce)

These rules apply to **every game build** regardless of game type, setting, or story structure. They directly improve game quality and player experience. Violating any of these rules produces a noticeably worse game.

---

## Rule 1: Tiered Activity System

Every repeatable activity canvas MUST use conditional escalating choices. The player always has a safe default option, and higher-intensity choices unlock progressively as the player meets conditions.

### Why This Matters

Without tiered choices, repeatable activities feel static. The player does the same thing every time they visit a location, and the game gets boring fast. Tiered choices make the daily gameplay loop feel alive — the same location offers new options as the player progresses, rewarding investment and creating a sense of growing capability.

### How It Works

- **Base choice** — always available, safe default (e.g., "Work the shift" for basic tips)
- **Higher-tier choices** — gated by conditions (corruption thresholds + flags)
- Each tier gives incrementally better rewards (more money, more stat gains)
- Mark the highest-escalation node with `loop_terminal = true` for loop control
- Choices are listed in escalating order so the player sees their progression

### TOML Example (New In Town: "Work the bar")

```toml
[[canvases]]
id = "activity_bar_shift"
name = "Work the bar"
description = "Emma works the bar alongside Jolene. Tips depend on how she presents herself."
is_repeatable = true

[canvases.trigger]
location = "loc_bar_floor"
is_repeatable = true
npc = "npc_jolene"
max_triggers_per_day = 1
priority = 1

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "bar_lesson_learned", operator = "is_true" }
]

[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "23:59"

[[canvases.nodes]]
id = "base"
name = "The Shift"
blocks = [
  { type = "paragraph", content = "Evening. The bar fills up..." }
]
exit_block = { type = "choices", choices = [
  # TIER 1: Always available — safe default
  { text = "Work the shift", targetType = "trigger", time_progression_minutes = 240,
    effects = [
      { targetType = "player", trait = "money", op = "add", value = 35 },
      { targetType = "player", trait = "confidence", op = "add", value = 1 }
    ] },

  # TIER 2: Requires corruption >= 65 + learned_seduction + flirt_unlock
  { text = "Flirt for tips", targetType = "node", nodeId = "activity_bar_shift.flirt_tips",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 65 },
      { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
    ] } },

  # TIER 3: Requires corruption >= 90 + discovered_teasing + tease_unlock
  { text = "Show off for tips", targetType = "node", nodeId = "activity_bar_shift.let_them_look",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 90 },
      { type = "flag", subject = "player", flag_key = "discovered_teasing", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
    ] } },

  # TIER 4: Requires corruption >= 110 + tease_unlock
  { text = "Let him grope you", targetType = "node", nodeId = "activity_bar_shift.groping",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 110 },
      { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
    ] } },

  # TIER 5: Requires corruption >= 160 + handjob_unlock
  { text = "Handjob in the bathroom", targetType = "node", nodeId = "activity_bar_shift.bar_handjob",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 160 },
      { type = "flag", subject = "player", flag_key = "handjob_unlock", operator = "is_true" }
    ] } },

  # TIER 6: Requires corruption >= 190 + blowjob_unlock
  { text = "Blowjob in the bathroom", targetType = "node", nodeId = "activity_bar_shift.bar_blowjob",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 190 },
      { type = "flag", subject = "player", flag_key = "blowjob_unlock", operator = "is_true" }
    ] } },

  # TIER 7: Requires corruption >= 220 + sex_unlock
  { text = "Take him out back", targetType = "node", nodeId = "activity_bar_shift.bar_sex",
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 220 },
      { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
    ] } }
] }
```

### Pay Escalation Pattern

Each tier pays more, creating a natural economic incentive for the player to push their comfort level:

| Tier | Choice | Pay | Corruption Gate | Flag Gate |
|------|--------|-----|-----------------|-----------|
| 1 | Work the shift | $35 | None | None |
| 2 | Flirt for tips | $55 | 65 | learned_seduction + flirt_unlock |
| 3 | Show off | $90 | 90 | discovered_teasing + tease_unlock |
| 4 | Groping | $120 | 110 | tease_unlock |
| 5 | Handjob | $200 | 160 | handjob_unlock |
| 6 | Blowjob | $300 | 190 | blowjob_unlock |
| 7 | Sex | $500 | 220 | sex_unlock |

### Anti-Pattern: Flat Activities

```toml
# BAD — No escalation. Player does the same thing every visit.
exit_block = { type = "choices", choices = [
  { text = "Work the shift", targetType = "trigger",
    effects = [{ targetType = "player", trait = "money", op = "add", value = 50 }] }
] }
```

This makes the activity feel dead after the first visit. The player has no reason to come back except to grind money, and no sense of progression.

---

## Rule 2: One-Time Story vs. Repeatable Activities

Strict separation between two canvas types. Story canvases drive the narrative. Activities are the daily loop. Never mix these roles.

### Why This Matters

Mixing story and activity content creates confusion. If a repeatable activity moves the plot forward, the player might accidentally trigger story beats while grinding. If a story canvas is repeatable, the player might re-watch pivotal moments, destroying emotional impact. Clean separation keeps the narrative tight and the daily loop engaging.

### The Two Types

**Story Canvases** (one-time events):
- `is_repeatable = false`
- `priority = 10` (high priority — always triggers before activities when conditions are met)
- Sets flags that advance the plot
- Contains narrative scenes with dialogue and consequences
- Once seen, never seen again

**Repeatable Activities** (daily gameplay):
- `is_repeatable = true`
- `priority = 1-3` (low priority — only triggers when no story canvas is available)
- Provides stat grinding, money earning, relationship building
- Uses tiered choices (see Rule 1)
- Can be done every day within schedule windows

**Random Encounters** (passive witnessing):
- `trigger_mode = "random"` with a `chance` probability
- Player witnesses something — no choice to engage
- Adds small stat changes (+2-3 corruption)
- Can be one-time or repeatable depending on design intent

### TOML Example: One-Time Story Canvas

```toml
[[canvases]]
id = "first_night"
name = "The noise downstairs"
description = "Emma can't sleep. The bar is loud beneath her."
# Story canvas — happens once, high priority
is_repeatable = false

[canvases.trigger]
location = "loc_bar_emma_room"
is_active = true
is_repeatable = false
priority = 10    # <-- Always triggers before activities

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "game_started", operator = "is_true" }
]

[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "20:00"
end_time = "23:59"

# ... narrative nodes ...

# Final node sets flag to advance the story
[[canvases.nodes]]
id = "n2"
name = "The Math"
exit_block = { type = "choices", choices = [
  { text = "Stare at the ceiling until sleep comes",
    targetType = "location", locationId = "loc_bar_emma_room",
    time_progression_minutes = 120,
    flagEffects = [{ targetType = "player", flag = "first_night_complete" }]  # <-- Advances plot
  }
] }
```

### TOML Example: Repeatable Activity

```toml
[[canvases]]
id = "activity_bar_shift"
name = "Work the bar"
is_repeatable = true    # <-- Can be done daily

[canvases.trigger]
location = "loc_bar_floor"
is_repeatable = true
priority = 1            # <-- Low priority, yields to story canvases
max_triggers_per_day = 1
```

### TOML Example: Random Encounter

```toml
[canvases.trigger]
location = "loc_bar_upstairs"
trigger_mode = "random"
chance = 0.7              # <-- 70% chance when entering location
is_repeatable = true
max_triggers_per_day = 1  # <-- Once per day max
```

### Anti-Pattern: Mixing Story and Activity

```toml
# BAD — A repeatable canvas that sets a plot flag
[[canvases]]
id = "daily_bar_work"
is_repeatable = true
# ... nodes that set "met_important_npc" flag ...
# Player might trigger this on their 5th visit, making the meeting feel random
```

---

## Rule 3: Flag-Gated Intensity Escalation

Sexual/intensity escalation MUST be gated by flags set in **one-time story events**, not just by stat thresholds alone. The player must narratively "learn" or "experience" a behavior before they can repeat it.

### Why This Matters

Without flag gating, a player with high corruption could jump straight to the most intense content without any story context. The player would get a handjob option at the bar without ever having experienced what that means narratively. Flag gating ensures every escalation has a story behind it — the player watched someone do it, tried it for the first time with a specific NPC, or discovered it through exploration.

### How It Works

1. A **one-time story canvas** plays out a narrative scene where the player experiences something new for the first time
2. That canvas sets an **unlock flag** (e.g., `flirt_unlock`, `tease_unlock`, `handjob_unlock`)
3. ALL repeatable activities across ALL arcs check for that flag before offering that tier of choice

### The Unlock Chain (New In Town Example)

| Story Event | Flag Set | What It Unlocks |
|------------|----------|-----------------|
| The Bend (Mick teasing scene) | `tease_unlock` | Tease/show off choices everywhere |
| The Kiss (Mick kiss scene) | `flirt_unlock` | Flirting choices everywhere |
| The Couch (Mick handjob scene) | `handjob_unlock` | Handjob choices everywhere |
| The Counter (Mick blowjob scene) | `blowjob_unlock` | Blowjob choices everywhere |
| The Room (Mick sex scene) | `sex_unlock` | Sex choices everywhere |

### Cross-Arc Consistency

This is the most powerful aspect. Once the player unlocks `handjob_unlock` through the Mick story arc, that same flag gates handjob options in:
- Bar work activity (handjob in the bathroom)
- Glory hole activity (through the wall)
- Public arc (against the wall)
- Harlan arc (under the desk)

The player learned the behavior in one context and can now apply it everywhere. This feels natural and earned.

### Anti-Pattern: Threshold-Only Gating

```toml
# BAD — Only checks corruption level, no flag
{ text = "Give him a handjob",
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 160 }
  ] } }
# Player could reach corruption 160 just from watching porn and random encounters
# without ever having done anything physical with anyone
```

---

## Rule 4: Dual Gating (Threshold + Flag)

Every gated choice should require BOTH a numeric threshold AND a narrative flag from a prior story event. Never gate content with just a threshold alone.

### Why This Matters

A threshold alone feels like an arbitrary number wall — "you need 90 corruption to do this" with no narrative reason. A flag alone doesn't account for gradual progression — the player might have the flag but isn't "ready" stat-wise. Both together create a gate that feels both narratively justified AND mechanically earned.

### The Pattern

```toml
conditions = { version = "1.0", items = [
  # Numeric threshold — the player has progressed enough statistically
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 90 },
  # Narrative flag — the player has experienced this in a story context
  { type = "flag", subject = "player", flag_key = "discovered_teasing", operator = "is_true" },
  # Unlock flag — the player has "learned" this skill
  { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
] }
```

### For NPC-Specific Gates, Add Relationship Thresholds

When a gated choice involves a specific NPC, also check the NPC's relationship stats:

```toml
# Mick kiss scene requires both player corruption AND relationship investment
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 },
  { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 20 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 20 }
] }
```

This prevents speed-running relationships — you need both emotional investment AND physical readiness.

### Anti-Pattern: Threshold Only

```toml
# BAD — Just a number, no narrative justification
{ text = "Kiss him",
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 }
  ] } }
```

### Anti-Pattern: Flag Only

```toml
# BAD — Flag but no threshold. Player could trigger this at corruption 5.
{ text = "Tease him",
  conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
  ] } }
```

---

## Rule 5: Time Schedule Windows

Activities and story canvases MUST have schedule constraints. The game world operates on a clock, and things happen at specific times on specific days. This prevents the player from doing everything all at once and creates a rhythm to gameplay.

### Why This Matters

Without time constraints, the player can grind every activity in a single in-game hour. Time windows force the player to plan their day, make choices about what to prioritize, and experience the game world as a living place where things happen on schedules. It also creates natural pacing — the player can't rush through all content in one sitting.

### Key Schedule Fields

- **`start_time` / `end_time`** — When the activity is available (24-hour format)
- **`weekdays`** — Which days of the week (0=Monday through 6=Sunday)
- **`max_triggers_per_day`** — Prevents spamming the same activity
- **`days_since_flag`** — Forces waiting between story beats (prevents rushing major moments)
- **`time_progression_minutes`** — How much time passes when doing the activity

### TOML Examples

**Bar work only available in the evening:**
```toml
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "23:59"
```

**Classes only in the morning on weekdays:**
```toml
[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4]    # Mon-Fri
start_time = "08:00"
end_time = "12:00"
```

**Forcing a 1-day delay between story beats:**
```toml
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "first_night_complete", operator = "gte", value = 1 }
]
```

**Limiting activity frequency:**
```toml
[canvases.trigger]
location = "loc_bar_floor"
is_repeatable = true
max_triggers_per_day = 1    # Once per day only
```

**Time progression on choices:**
```toml
{ text = "Work the shift", targetType = "trigger",
  time_progression_minutes = 240,   # 4 hours pass
  effects = [...] }
```

### Anti-Pattern: No Time Constraints

```toml
# BAD — No schedule, no frequency limit. Player can spam this infinitely.
[canvases.trigger]
location = "loc_bar_floor"
is_repeatable = true
```

---

## Rule 6: NPC Presence via Trigger

When a canvas involves an NPC, set the `npc` field in the trigger to bind that NPC to the location during the scene. This ensures the NPC portrait and name display correctly in the UI.

### Why This Matters

The game engine uses the `npc` field to show the NPC's portrait, name, and relationship stats in the scene UI. Without it, the player sees a scene about talking to Mick but the UI shows no NPC — breaking immersion. It also helps the engine know which NPC's stats to display for relationship-gated choices.

### TOML Example

```toml
# Mick is present at the stockroom during this activity
[canvases.trigger]
location = "loc_bar_stockroom"
is_repeatable = true
npc = "npc_mick"              # <-- Binds Mick to this scene
max_triggers_per_day = 1
priority = 1

# Jolene is present at the bar floor during work shifts
[canvases.trigger]
location = "loc_bar_floor"
is_repeatable = true
npc = "npc_jolene"            # <-- Binds Jolene to this scene
max_triggers_per_day = 1
priority = 1
```

### Anti-Pattern: Missing NPC Binding

```toml
# BAD — Scene is about talking to Mick but no NPC binding
[canvases.trigger]
location = "loc_bar_stockroom"
is_repeatable = true
# npc field missing — UI won't show Mick's portrait
```

---

## Rule 7: Story Arc Restriction (Non-Repeatable Only)

Story arc nodes (`[[story_arc.nodes]]`) must only link to **non-repeatable canvases** (`is_repeatable = false`). Repeatable activities and random encounters are gameplay mechanics, not narrative events — they belong in the stat-building loop, not the story tracker.

### Why This Matters

The story arc drives the Quest/Journal page and the hint system. If a repeatable activity is in the story arc, the player is "required" to do a specific activity to progress. With the NPC portrait interaction system, activities are player-initiated — the player should never be forced to do a specific activity. Story events auto-fire when conditions are met; activities are optional choices.

### The Clean Cycle

```
Activities (repeatable, player-chosen) → stats go up
    → stat thresholds + flags met → story event auto-fires (non-repeatable)
        → sets new flags, unlocks new activity tiers
            → player has new options → back to activities
```

The story arc tracks the story events. Activities are the engine.

### If an Activity Is a Story Milestone

Create a **separate non-repeatable canvas** for the milestone moment. After it fires once and sets its flag, the repeatable activity canvas takes over for future visits.

```toml
# GOOD: Separate story event for the milestone
[[canvases]]
id = "scene_first_breakfast"       # One-time story event
name = "First Morning Together"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = false              # Story event
priority = 10

# Repeatable activity starts after the story event
[[canvases]]
id = "activity_breakfast_ethan"    # Daily repeatable
name = "Breakfast with Ethan"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true               # Activity
priority = 1
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "first_breakfast_complete", operator = "is_true" }
]
```

### Branch Conditions for Path-Variant Journal Entries

When a single NPC has multiple story paths (e.g., a "gentle" route vs. an "aggressive" route), use `branch_condition` on story arc nodes to show different journal entries depending on which path the player chose.

**How it works:**
1. A branch-point story canvas offers a meaningful choice that sets **different flags** per option (e.g., `chose_gentle` vs. `chose_bold`)
2. Both choices also set the **same completion flag** (e.g., `crossroads_complete`) so the story arc tracks the shared milestone
3. Downstream story arc nodes that belong to one path set `branch_condition = "chose_gentle"` — these are **invisible** in the journal unless that flag is set
4. Nodes without `branch_condition` appear for ALL players (shared content)
5. After branch-specific content, reconverge using a **group** with `required_count = 1`

**Key rules:**
- `branch_condition` is a single flag name (string), not a complex condition
- Invisible nodes are completely excluded — not shown as locked, not counted in progress
- Branch points must happen in **story canvases** (non-repeatable), never in activities
- Use `requires_group` (not `requires_nodes`) for reconvergence — `requires_nodes` is AND logic which deadlocks across exclusive paths
- Limit to **1-2 branch points per NPC** — each doubles the content needed

```toml
# Branch-point canvas sets different flags per choice:
# Choice A exit: flagEffects = [
#   { targetType = "player", flag = "chose_gentle" },
#   { targetType = "player", flag = "crossroads_complete" }
# ]
# Choice B exit: flagEffects = [
#   { targetType = "player", flag = "chose_bold" },
#   { targetType = "player", flag = "crossroads_complete" }
# ]

# Shared milestone (both paths see this):
[[story_arc.nodes]]
id = "crossroads"
name = "The Crossroads"
chapter = "chapter_2"
linked_canvas = "elena_crossroads"
linked_flag = "crossroads_complete"
is_milestone = true
journal_entry = "She told me about her dream. I had to choose."

# Gentle path only:
[[story_arc.nodes]]
id = "gentle_aftermath"
name = "Letters from Afar"
chapter = "chapter_3"
linked_canvas = "gentle_letters"
linked_flag = "gentle_letters_complete"
branch_condition = "chose_gentle"
group = "path_resolution"
journal_entry = "Her letters arrive on Tuesdays. Each one a small gift."

# Bold path only:
[[story_arc.nodes]]
id = "bold_aftermath"
name = "The Unspoken"
chapter = "chapter_3"
linked_canvas = "bold_tension"
linked_flag = "bold_tension_complete"
branch_condition = "chose_bold"
group = "path_resolution"
journal_entry = "She stayed, but something between us shifted."

# Reconvergence group:
[[story_arc.groups]]
id = "path_resolution"
name = "Path Resolution"
required_count = 1

# Shared continuation (both paths):
[[story_arc.nodes]]
id = "reunion"
name = "What We Built"
chapter = "chapter_4"
linked_canvas = "reunion_scene"
linked_flag = "reunion_complete"
requires_group = "path_resolution"
journal_entry = "Whatever road we took, it led here."
```

See Pattern M in `game_design_patterns.md` for the full design pattern.

---

## Rule 8: NPC Presence via Portraits

At locations, repeatable NPC activities display as **clickable circular NPC portraits**. The player sees who is present and clicks to interact. Solo activities (no NPC) display as text action buttons.

### How It Works

1. Player enters a location
2. **Story events auto-fire** if a valid non-repeatable canvas exists (unchanged)
3. **Random encounters roll** if a random-mode canvas exists (unchanged)
4. **NPC portraits appear** for each NPC with a valid repeatable manual canvas
5. **Solo activities** appear as text buttons below portraits
6. Player clicks a portrait → enters that NPC's activity canvas

### Portrait Source

The NPC's portrait image comes from `portrait` field in `[[npcs]]`. If no portrait is set, a fallback circle with the NPC's initial letter is shown.

### The `npc` Field is Critical

The trigger's `npc` field determines which portrait appears. Every NPC activity MUST have `npc` set on its trigger. Without it, the activity shows as a solo text button instead of an NPC portrait.

---

## Rule 9: Canvas Uniqueness Constraint

**One repeatable canvas per (location + NPC + schedule window).** This ensures each NPC portrait at a location maps to exactly one canvas.

### Why This Matters

The portrait system shows one portrait per NPC at a location. If multiple canvases could fire for the same NPC at the same time, the system wouldn't know which canvas to open when the player clicks the portrait. The uniqueness constraint eliminates this ambiguity.

### What Goes Inside vs. Outside

- **Different interactions with same NPC** → choices INSIDE the canvas (gated tiers)
- **Different NPCs at same location** → separate canvases (one per NPC)
- **Same NPC at different times** → separate canvases with non-overlapping schedules

### TOML Example

```toml
# GOOD: One canvas for Ethan at kitchen in the morning
[[canvases]]
id = "activity_breakfast_ethan"
name = "Breakfast with Ethan"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "10:00"

# GOOD: Different NPC at same location/time = separate canvas
[[canvases]]
id = "activity_breakfast_linda"
name = "Breakfast with Linda"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_linda"
is_repeatable = true
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "10:00"

# GOOD: Same NPC at different time = separate canvas
[[canvases]]
id = "activity_lunch_ethan"
name = "Lunch with Ethan"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
[[canvases.trigger.schedules]]
start_time = "12:00"
end_time = "14:00"
```

### Anti-Pattern

```toml
# BAD: Two canvases for same NPC at same location/time
[[canvases]]
id = "activity_breakfast_ethan"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "10:00"

[[canvases]]
id = "activity_cook_with_ethan"     # CONFLICT! Same NPC, location, time
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
[[canvases.trigger.schedules]]
start_time = "08:00"
end_time = "09:00"

# FIX: Merge into one canvas. "Cook together" becomes a choice inside
# activity_breakfast_ethan's exit_block.
```

### NPC Name Variables (`@`-syntax) and Customizable NPCs

When writing narrative content, use `@`-references instead of hardcoding NPC names. This enables player customization of NPC names and relationships.

**Syntax:**
- `@ethan` → resolves to the NPC's current display name (from `npc_ethan`)
- `@ethan.rel` → resolves to the NPC's relationship label (e.g., "step-brother")
- `@ethan's` → name + possessive 's

**Customizable NPCs:** Mark NPCs with `customizable = true` when the player should be able to rename them and choose a relationship type. The game generates a customization screen at start.

**Key Rules:**
1. `@`-references are REQUIRED for customizable NPCs in ALL paragraph and heading content
2. `@`-references are RECOMMENDED for all NPCs for consistency
3. Dialog speaker labels are automatic (via `npcId` prop) — no `@` needed for speaker name
4. Dialog content CAN use `@` to reference other NPCs by name
5. Emotion mapping descriptions should use `@`-syntax too
6. Relationship options should be narratively compatible — the same scene text must work with any option

**TOML Example:**
```toml
[[npcs]]
id = "npc_ethan"
name = "Ethan"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "roommate", "landlord"]
description = "Late 20s, tall, athletic build."
portrait = "ethan.jpg"
core_traits = { love = 0, trust = 0 }
flag_keys = []

# Content using @-syntax:
# { type = "paragraph", content = "@ethan is already in the kitchen. Your @ethan.rel pours you coffee." }
# { type = "paragraph", content = "@ethan's eyes meet yours across the table." }
# { type = "dialog", content = "Good morning.", props = { speaker = "npc", npcId = "npc_ethan" } }
```

**Choosing Relationship Options:**
Pick options where the narrative framing works interchangeably:
- Good: `["step-brother", "roommate", "housemate"]` — all explain shared living space
- Bad: `["step-brother", "stranger", "boss"]` — "Your boss pours you coffee in the kitchen" doesn't fit a cohabitation narrative

For narratively divergent relationship types, use group blocks with flag conditions instead of the relationship label swap.

---

## Rule 10: Energy/Resource Costs

**Every repeatable activity should have an energy cost proportional to its physical/mental intensity.** Energy creates real trade-offs — players can see all activities but can't afford them all, forcing decisions about what to prioritize each day.

### How It Works

The `costs` array on a canvas trigger defines resource requirements:

```toml
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
costs = [{ trait = "energy", value = 20 }]
```

- **If affordable**: Player enters the canvas, cost is auto-deducted, toast shows "-20 Energy"
- **If not affordable**: Activity is VISIBLE but blocked — clicking shows "Requires 20 Energy (you have 15)"
- **Sidebar**: Add a `trait_bar` sidebar item to display current energy

### Energy Cost Tiers

| Tier | Cost | Activities |
|---|---|---|
| Free | 0 | Sleep, shower, phone scroll (restorative/passive) |
| Minimal | 5 | Journal, get ready, wander |
| Light | 10 | Meals, brief social (breakfast, lunch, goodnight, stargazing) |
| Moderate-light | 15 | Dinner, movie night, video games, garage memories |
| Moderate | 20 | Cooking, wine talk, planning, late night, emotional scenes |
| Heavy | 25 | Chores, manual labor |
| Very heavy | 30 | Pool, sports, extended physical activity |

### Energy Restoration

Energy is restored via effects on solo activities (existing effects system):
- **Full sleep**: `op = "set", value = 100` (reset to full)
- **Nap**: `op = "add", value = 20`
- **Shower**: `op = "add", value = 5-10`
- Players start each game at 100 energy

### Rules

1. **Story events (is_repeatable=false) must NOT have costs** — narrative progression can't be blocked by resources
2. **Random encounters must NOT have costs** — they auto-fire probabilistically
3. **Restorative activities are FREE** — sleep, shower have no cost (they restore energy via effects)
4. **Time-kill activities are FREE** — phone scroll, passive waiting have no cost
5. **Energy budget**: A full day's activities should require strategic rest breaks. Target: 4-5 activities per day without rest, 6-7 with a nap

### Sidebar Energy Display

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "energy"
label = "Energy"
max = 100
```

---

## Rule 11: Three-Choice Activity Format

Every NPC activity MUST present exactly **three approach choices** at its base node: Emotional, Physical, and Neutral. The player chooses what KIND of interaction they want, not which intensity tier to consume.

### Why This Matters

The old tier ladder (T1→T8 visible simultaneously) made activities feel like a progress bar. The player always picked the highest unlocked option. There was no decision — just optimization. The three-choice format turns every visit into a real choice: do I want story depth (emotional), physical content (physical), or a quick interaction (neutral)?

### How It Works

```
Base node (with group variants — content changes per relationship phase)
  → [Emotional] "Talk with him"  → conversation node → exit (love +3, trust +2)
  → [Physical]  "Get closer"     → intensity sub-node → unlockable tier choices
  → [Neutral]   "Just eat"       → direct exit (love +1, trust +3)
```

- **Emotional** — Always available. Leads to a conversation node with group variants. Content evolves per relationship phase. Builds love and trust. This is where story depth lives.
- **Physical** — Gated by `lingering_touch_unlock` (first physical flag). Leads to a sub-node with progressively unlockable intensity choices (touch → flirt → kiss → manual → oral → sex). Each gated by its own unlock flag.
- **Neutral** — Always available. Direct exit with small love gain and moderate trust gain. The "safe" option.

### Trait Definitions (Two Weeks)

**Player traits:**
- `corruption` (0-100) — How far the player has been drawn into physical/moral compromise
- `energy` (0-100) — Daily resource spent on activities, restored by sleep/rest

**Ethan traits:**
- `love` (0-100) — Romantic attachment and emotional bond
- `trust` (0-100) — Comfort level and willingness to be vulnerable
- `corruption` (0-100) — How far Ethan has been pushed past his own boundaries

No guilt trait. No Madison traits.

### Effect Values by Choice Type

| Choice Type | Effects |
|-------------|---------|
| Emotional | love +3, trust +2 |
| Physical (per tier) | love +1, Ethan corruption +3-8 (scales by tier), player corruption +2-6 (scales by tier) |
| Neutral | love +1, trust +3 |
| Bonding (special emotional) | love +2-3, trust +4-6 |
| Journal (solo) | player corruption +3 |

### Base Node Group Variants

The base node uses `group` blocks to show different opening content based on relationship phase:

```toml
blocks = [
  # Most specific phase first (checked top-to-bottom, first match wins)
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Phase 5 content — fiancée is in the house" }
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Phase 4 content — fully intimate" }
  ] },
  # Default (no conditions) — fallback for early game
  { type = "group", blocks = [
    { type = "paragraph", content = "Default content — reconnecting" }
  ] }
]
```

### Physical Sub-Node Structure

```toml
[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  # First option always available (physical node itself is gated)
  { text = "Touch choice", targetType = "node", nodeId = "canvas_id.t2" },
  # Subsequent options gated by unlock flags
  { text = "Kiss choice", targetType = "node", nodeId = "canvas_id.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  # ... more tiers
] }
```

### Anti-Pattern: Flat Tier Ladder

```toml
# BAD — 8 choices visible at base node. Player always picks highest.
exit_block = { type = "choices", choices = [
  { text = "T1: Eat together", ... },
  { text = "T2: Sit closer", ..., conditions = { ... } },
  { text = "T3: Flirt", ..., conditions = { ... } },
  { text = "T4: Kiss", ..., conditions = { ... } },
  { text = "T5: Manual", ..., conditions = { ... } },
  { text = "T6: Oral", ..., conditions = { ... } },
  { text = "T7: Sex", ..., conditions = { ... } },
  { text = "T8: Sex again", ..., conditions = { ... } }
] }
# This is a progress bar, not a choice.
```

---

## Rule 12: Rejection & Visible Failure

Gated choices SHOULD be **visible even when locked**, not hidden. Players must see what they COULD do, creating anticipation and tension. When appropriate, locked choices should allow **rejection** — the player clicks, but the NPC refuses, with consequences.

### Why This Matters

Hidden choices create invisible progression — the player doesn't know what they're working toward. Visible locked choices create desire ("I need to build more trust before she'll let me..."). Rejection creates **failure states** — the player can overstep and face consequences, which makes success feel earned rather than inevitable.

Without rejection, NPCs are vending machines that always give the player what they want. With rejection, NPCs have boundaries, creating tension and authenticity.

### How It Works

Every gated choice in an activity canvas can use two rejection modes:

**Mode A — Locked-Visible (show_when_locked):** Choice appears greyed out with a `locked_text` explanation. Player sees it but can't click it. Creates anticipation.

**Mode B — Rejection Redirect (rejection_node):** Choice appears styled as risky (italic, warning color). Player CAN click it, but redirects to a `rejection_node` instead of the real target, and applies `rejection_effects` (typically trust -3 or love -2). The rejection node contains authored prose describing the NPC's refusal.

### TOML Pattern

```toml
# Mode A: Visible but locked (player sees what they're working toward)
{ text = "Kiss her good morning",
  targetType = "node", nodeId = "activity_breakfast.t4",
  conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] },
  show_when_locked = true,
  locked_text = "She's not ready for that yet." }

# Mode B: Clickable rejection (NPC refuses with consequences)
{ text = "Pull her close and kiss her",
  targetType = "node", nodeId = "activity_breakfast.t4",
  conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] },
  show_when_locked = true,
  locked_text = "She might not be ready for this...",
  rejection_node = "activity_breakfast.t4_rejection",
  rejection_effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = -3, clamp = true }
  ] }
```

**The rejection node** is a regular node in the same canvas with authored rejection prose:
```toml
[[canvases.nodes]]
id = "t4_rejection"
name = "Rejected Kiss"
blocks = [
  { type = "paragraph", content = "You lean in, but @ethan pulls back, eyes wide. \"What are you doing?\" The moment shatters like dropped glass." },
  { type = "dialog", content = "I... I'm not... we can't do that.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The kitchen feels ten degrees colder. @ethan turns back to the stove without looking at you." }
]
exit_block = { type = "location", text = "Leave quietly", config = { destinationType = "trigger", time_progression_minutes = 15 } }
```

### When to Use Each Mode

| Mode | Use When | Example |
|------|----------|---------|
| **Mode A** (locked-visible) | The gate is a flag unlock — player needs a story event first | Kiss locked until `kiss_unlock` set by story canvas |
| **Mode B** (rejection) | The gate is a stat threshold — player is building toward it and might try early | Kiss requires love ≥ 50, player at 35 |
| **Both together** | Physical escalation with both flag + stat gates | T6 requires `manual_unlock` (Mode A) AND love ≥ 70 (Mode B) |

### Anti-Pattern

```toml
# BAD — Choice is completely invisible until conditions are met.
# Player has no idea this option exists. No tension, no anticipation.
{ text = "Kiss her", targetType = "node", nodeId = "t4",
  conditions = { ... } }

# GOOD — Player sees it from the start, greyed out with reason.
# Creates desire and direction. Player knows what to work toward.
{ text = "Kiss her", targetType = "node", nodeId = "t4",
  conditions = { ... },
  show_when_locked = true,
  locked_text = "You haven't earned that kind of trust yet." }
```

---

## Rule 13: Trait Decay (NPC Relationship Maintenance)

NPC relationship traits SHOULD decay over time if the player doesn't interact with that NPC. This prevents "grind and forget" — once love hits 80, it should require ongoing attention, not permanent conquest.

### Why This Matters

Without decay, NPCs are permanently conquered. The player grinds love to the threshold, unlocks content, then ignores the NPC forever while pursuing others. With decay, relationships require maintenance — visiting an NPC is both progression AND upkeep. This creates real daily prioritization ("Do I spend today with Ethan to keep his love up, or visit Marcus to push his story forward?").

In multi-NPC games, decay is essential. Without it, the player can max all NPCs sequentially. With decay, juggling multiple relationships becomes the core tension.

### How It Works

Add `trait_decay` to any NPC whose relationship should require maintenance:

```toml
[[npcs]]
id = "npc_ethan"
name = "Ethan"
core_traits = { love = 0, trust = 0, corruption = 0 }

[npcs.trait_decay]
love = 1        # Loses 1 love per day without interaction
trust = 0.5     # Loses 0.5 trust per day without interaction
# corruption not listed = never decays (corruption is permanent)
```

**Runtime behavior:**
- When a canvas with `npc = "npc_ethan"` fires, Ethan is marked as "interacted with today"
- At midnight (day rollover), any NPC NOT interacted with has their configured traits reduced
- Traits clamp at 0 (never go negative)
- The player never sees the decay formula — they just notice "Ethan's love was 45 yesterday and it's 44 today"

### Design Guidelines

| Trait | Recommended Decay | Rationale |
|-------|-------------------|-----------|
| love | 0.5 – 2.0 | Love fades without attention. Higher decay = more pressure. |
| trust | 0.5 – 1.0 | Trust erodes slowly. Lower decay than love. |
| corruption | 0 (no decay) | Corruption is permanent — once you've crossed a line, it stays crossed. |
| comfort | 0.5 – 1.0 | NPC reverts to baseline comfort without reinforcement. |

**Single-NPC games**: Use low decay (0.5–1.0). Maintenance should be achievable through normal daily interaction. The decay creates a gentle "don't ignore them" pressure but shouldn't punish the player.

**Multi-NPC games**: Use moderate decay (1.0–2.0). The tension comes from needing to split time between NPCs, knowing that focusing on one means others will slip.

### Anti-Pattern

```toml
# BAD — No decay. Player grinds love to 80, unlocks all content, ignores NPC.
[[npcs]]
id = "npc_ethan"
core_traits = { love = 0, trust = 0 }
# No trait_decay section — love stays at 80 forever once reached.

# GOOD — Love requires ongoing attention.
[[npcs]]
id = "npc_ethan"
core_traits = { love = 0, trust = 0 }
[npcs.trait_decay]
love = 1
trust = 0.5
```

---

## Rule 14: NPC-Initiated Confrontation Events

When NPC traits drop below critical thresholds (often due to trait decay from Rule 13), the game SHOULD include **confrontation canvases** — high-priority one-time events where the NPC initiates a conversation about the deteriorating relationship.

### Why This Matters

NPCs feel alive when they react to being neglected. Without confrontation events, the player might not even notice trait decay happening. With them, the NPC says "We need to talk" — creating drama, urgency, and a chance to repair the relationship.

### How It Works

This uses **existing TOML features** — no new schema needed. A confrontation canvas is simply a high-priority non-repeatable canvas with low-trait trigger conditions:

```toml
[[canvases]]
id = "ethan_confrontation_distant"
name = "Ethan Confrontation: Growing Apart"

[canvases.trigger]
location = "loc_living_room"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 15  # Higher than activities (1-3) — fires FIRST

[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "lte", value = 15 },
  { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
]

[[canvases.trigger.schedules]]
start_time = "08:00"
end_time = "22:00"
weekdays = [0, 1, 2, 3, 4, 5, 6]
```

The combination of `love <= 15` AND `first_kiss_done` means: the player had a real relationship that has deteriorated. The confrontation presents a fork:
- **Repair path**: Apologize, invest effort, love +10
- **Withdraw path**: Accept distance, sets `ethan_distant` flag that changes future group block variants

### Design Guidelines

- Include 1-2 confrontation events per NPC with significant trait decay
- Place them at locations where the NPC is commonly found
- Set priority higher than activities (15+) so they fire before normal interactions
- Gate behind a relationship milestone flag (only confront after a real bond existed)
- Both outcomes should be narratively interesting — repair is earned, withdrawal has consequences
- Confrontation canvases are `is_repeatable = false` — they fire once and set a flag

---

## Rule 15: Temporary Modifiers

Certain choices SHOULD apply **temporary modifiers** that change what the player can do for a limited time. Modifiers add offsets to trait condition checks without changing actual trait values. This creates "moment of weakness" gameplay — the player does something they couldn't normally do, and the consequences are permanent even after the modifier expires.

### Why This Matters

Without modifiers, every gate is permanent math. You need boldness 40? Grind boldness to 40. There's no "liquid courage," no "I got carried away," no "the wine made me brave." Progression is always deliberate and calculated.

With modifiers, a player drinks wine (+20 boldness for 3 hours) and suddenly a physical choice they couldn't reach is available. They click it. Next morning, the modifier expires and boldness is back to 25 — but the `first_night_complete` flag is permanently set. The story moved forward because of a moment, not a grind.

### How It Works

**Applying a modifier** — a choice includes `modifier_effects`:
```toml
{ text = "Have another glass of wine",
  targetType = "trigger",
  time_progression_minutes = 30,
  modifier_effects = [
    { key = "tipsy", name = "Tipsy", duration_hours = 3,
      trait_offsets = { corruption = 15, boldness = 20 } }
  ] }
```

**Modifier affects condition checks** — at runtime, when evaluating player trait conditions, active modifier offsets are added to the trait value. A player with boldness 25 and a +20 tipsy offset passes a `boldness >= 40` gate. The actual boldness value stays at 25 — only the check is modified.

**Modifier-aware base nodes** — use `modifier_redirect` on nodes to show a completely different base experience when a modifier is active:
```toml
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
modifier_redirect = { modifier_key = "tipsy", node = "base_tipsy" }
blocks = [{ type = "paragraph", content = "Morning light through the window." }]
exit_block = { type = "choices", choices = [...sober choices...] }

[[canvases.nodes]]
id = "base_tipsy"
name = "Morning Kitchen (Tipsy)"
blocks = [{ type = "paragraph", content = "Everything feels closer than usual." }]
exit_block = { type = "choices", choices = [...tipsy choices...] }
```

**Modifier as condition type** — group blocks and choices can check modifier state:
```toml
{ type = "group", conditions = { items = [
  { type = "modifier", modifier_key = "tipsy", operator = "is_active" }
] }, blocks = [
  { type = "paragraph", content = "The wine has made everything soft at the edges." }
] }
```

**Modifier expiry** — modifiers expire automatically after `duration_hours` of game time. The sidebar shows active modifiers with remaining time.

### Design Guidelines

| Modifier | Source | Duration | Trait Offsets | Use Case |
|----------|--------|----------|-------------|----------|
| Tipsy | Wine/beer choices | 2-3 hours | corruption +15, boldness +20 | Lowered inhibitions at evening events |
| Confident | Compliment from NPC | 2 hours | boldness +15 | Temporary courage after validation |
| Aroused | Steamy scene | 1 hour | corruption +20 | Post-scene heightened state |
| Angry | Fight/confrontation | 2 hours | boldness +25, trust -10 | Reckless after conflict |

### Anti-Pattern

```toml
# BAD — Modifier with 24+ hour duration (defeats the purpose of being temporary)
modifier_effects = [{ key = "tipsy", duration_hours = 48, ... }]

# BAD — Modifier that replaces stat grinding entirely
modifier_effects = [{ key = "super", trait_offsets = { corruption = 100, boldness = 100 } }]

# GOOD — Short duration, moderate offset, creates a window of opportunity
modifier_effects = [{ key = "tipsy", duration_hours = 3, trait_offsets = { boldness = 20 } }]
```

---

## Rule 16: Consequence Echo

When a story event presents a meaningful branching choice, each branch MUST set a **choice-specific flag** in addition to the shared completion flag. Activities that fire during the next 1-3 days MUST check those choice flags via group blocks and show **different NPC reactions** based on which path the player chose.

### Why This Matters

Without consequence echoes, story choices are invisible. The player picks "Kiss her gently" vs "Pull her close" — both set `first_kiss_complete`, both advance the story. Next morning at breakfast, the NPC acts exactly the same regardless. The choice was meaningless.

With consequence echoes, the gentle path sets `chose_gentle` AND `first_kiss_complete`. Next morning's breakfast activity checks `chose_gentle` and opens with: "She touches her lips when she sees you. 'I keep thinking about last night,' she says quietly." The passionate path sets `chose_passionate` instead, and breakfast opens with: "She can't quite look at you. Her cheeks are pink. She pours your coffee without a word."

Same activity. Same exit block. Same choices. But the opening atmosphere is completely different based on yesterday's decision. The NPC **remembers**.

### How It Works

**Step 1: Story event sets choice-specific flags**

Each branch sets TWO flags — the shared completion flag AND a choice-specific flag:

```toml
# Gentle path exit
exit_block = { type = "location", config = { destinationType = "trigger",
  flagEffects = [
    { targetType = "player", flag = "first_kiss_complete" },
    { targetType = "player", flag = "chose_gentle" }
  ] } }

# Passionate path exit
exit_block = { type = "location", config = { destinationType = "trigger",
  flagEffects = [
    { targetType = "player", flag = "first_kiss_complete" },
    { targetType = "player", flag = "chose_passionate" }
  ] } }
```

**Step 2: Activities check choice flags in group blocks**

The consequence group blocks go FIRST in the chain (most specific), before phase variants:

```toml
[[canvases.nodes]]
id = "base"
name = "Morning Breakfast"
blocks = [
  # ── CONSEQUENCE ECHOES (checked first, most specific) ──

  # Gentle kiss echo (days 1-3 after the choice)
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_gentle", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_gentle", operator = "lte", value = 3 }
  ] }, blocks = [
    { type = "paragraph", content = "She touches her lips when she sees you. A small smile." },
    { type = "dialog", content = "I keep thinking about last night.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },

  # Passionate kiss echo (days 1-3 after the choice)
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_passionate", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_passionate", operator = "lte", value = 3 }
  ] }, blocks = [
    { type = "paragraph", content = "She can't quite look at you. Her cheeks are pink." },
    { type = "dialog", content = "Coffee's ready.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },

  # ── PHASE VARIANTS (checked after consequence echoes) ──

  # Post-first-night phase
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She made your favorite. Sits closer than usual." }
  ] },

  # Post-first-kiss phase
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She looks up when you walk in. Something has shifted." }
  ] },

  # Default
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light through the kitchen window. Two mugs." }
  ] }
]
```

### Group Block Priority Order

Group blocks are evaluated top-to-bottom. First match wins. The correct ordering is:

1. **Consequence echoes** (most specific — choice flag + days_since_flag)
2. **Modifier variants** (temporary state — modifier condition)
3. **Phase variants** (broad relationship milestones — phase flags)
4. **Default** (no conditions — always-available fallback)

Consequence echoes naturally expire because of the `days_since_flag <= 3` condition. After 3 days, the echo stops matching, and the group block chain falls through to phase variants. The NPC's reaction fades naturally without needing to clear any flags.

### Flag Naming Convention

| Choice Type | Flag Pattern | Example |
|-------------|-------------|---------|
| Gentle vs bold | `chose_gentle` / `chose_bold` | First kiss approach |
| Honest vs lied | `told_truth` / `kept_secret` | Confession moment |
| Support vs challenge | `chose_support` / `chose_challenge` | Argument resolution |
| Stay vs leave | `chose_stay` / `chose_leave` | Crisis decision |

### Designer Checklist

For each story event with a branching choice:
1. What flags does each branch set? (completion flag + choice-specific flag)
2. Which activities fire during the next 1-3 days at this NPC's locations?
3. For each affected activity, write 1-2 sentences of consequence opening per choice path
4. Add consequence group blocks FIRST in the base node block chain
5. Include `days_since_flag <= 3` to auto-expire the echo

### Content Cost

Each consequence echo adds **1-2 paragraphs** per affected activity per choice path. For a typical story event with 2 paths affecting 3 activities, that's 6-12 extra paragraphs total — not full scene rewrites.

### Anti-Pattern

```toml
# BAD — Both branches set only the completion flag. No consequence differentiation.
# Gentle: flagEffects = [{ flag = "first_kiss_complete" }]
# Bold:   flagEffects = [{ flag = "first_kiss_complete" }]
# Result: Activities can't tell which path the player chose. No echo.

# GOOD — Each branch sets completion flag AND choice-specific flag.
# Gentle: flagEffects = [{ flag = "first_kiss_complete" }, { flag = "chose_gentle" }]
# Bold:   flagEffects = [{ flag = "first_kiss_complete" }, { flag = "chose_passionate" }]
# Result: Activities check chose_gentle/chose_passionate for different opening prose.
```

---

## Rule 17: Block Pools for Repeatable Activities

Repeatable activity base nodes and emotional sub-nodes SHOULD use `block_pool` blocks to provide 3-5 text variants that the engine randomly selects each visit. This prevents the "same text every morning" problem that makes daily activities feel dead.

### Why This Matters

Without pools, visiting breakfast 10 times shows the exact same opening paragraph. "Morning light through the kitchen window. Two mugs." Every time. The group block system handles phase changes (post-first-kiss vs default), but WITHIN each phase, the text is frozen. Block pools add variety within phases — the player sees a different ambient moment each visit.

### How It Works

`block_pool` is a block type that holds multiple blocks of the same type. The engine randomly picks one each render.

**Paragraph pool** (most common — randomize ambient descriptions):
```toml
{ type = "block_pool", blocks = [
  { type = "paragraph", content = "She looks up from her phone and smiles." },
  { type = "paragraph", content = "The kitchen smells like fresh bread today." },
  { type = "paragraph", content = "She's humming while stirring her coffee." },
  { type = "paragraph", content = "She's staring out the window. Doesn't hear you come in." }
] }
```

**Dialog pool** (randomize greetings):
```toml
{ type = "block_pool", blocks = [
  { type = "dialog", content = "Morning! Sleep okay?", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "dialog", content = "I made extra today.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "dialog", content = "You're up early.", props = { speaker = "npc", npcId = "npc_angela" } }
] }
```

**Group pool** (randomize complete scene openings — paragraph + dialog as a unit):
```toml
{ type = "block_pool", blocks = [
  { type = "group", blocks = [
    { type = "paragraph", content = "She's at the counter, humming." },
    { type = "dialog", content = "I had the weirdest dream last night.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "She's reading something on her phone, laughing." },
    { type = "dialog", content = "You have to see this.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] }
] }
```

### Pools Inside Group Variants

Pools work INSIDE group block variants. The group selects by phase, then the pool randomizes within that phase:

```toml
blocks = [
  # Post-first-kiss phase — with randomized openings
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "block_pool", blocks = [
      { type = "paragraph", content = "She blushes when your eyes meet." },
      { type = "paragraph", content = "She's already smiling when you walk in." },
      { type = "paragraph", content = "She touches her lips, then looks away." }
    ] }
  ] },

  # Default phase — with randomized openings
  { type = "group", blocks = [
    { type = "block_pool", blocks = [
      { type = "paragraph", content = "Morning light through the kitchen window." },
      { type = "paragraph", content = "She's making coffee. Two mugs on the counter." },
      { type = "paragraph", content = "The kitchen is quiet. She nods when you walk in." }
    ] }
  ] }
]
```

### Where to Use

| Location | Use Pool? | Why |
|----------|-----------|-----|
| Activity base node opening | **Yes** | Player sees this every visit — variety matters most here |
| Emotional sub-node | **Yes** | Conversation topics should rotate |
| Neutral sub-node exit | **Yes** | Quick exits benefit from variety |
| Physical sub-node tiers | **No** | Specific gated content — should be consistent |
| Story event nodes | **No** | One-time content — player sees it once |
| Ending nodes | **No** | Climactic moments — should be crafted, not random |

### Content Cost

Each pool needs 3-5 short variants. For a typical activity with pooled base opening + pooled emotional dialog:
- 3-5 ambient paragraphs (base opening)
- 3-5 conversation starters (emotional sub-node)
- Total: 6-10 short sentences per activity

### Anti-Pattern

```toml
# BAD — Fixed text repeats identically every visit
blocks = [
  { type = "paragraph", content = "Morning light through the kitchen window." }
]

# GOOD — 4 variants, different ambient moment each visit
blocks = [
  { type = "block_pool", blocks = [
    { type = "paragraph", content = "Morning light through the kitchen window." },
    { type = "paragraph", content = "Rain against the glass. She's made hot chocolate." },
    { type = "paragraph", content = "She's singing along to the radio. Badly." },
    { type = "paragraph", content = "The coffee maker gurgles. She's still in her pajamas." }
  ] }
]
```
