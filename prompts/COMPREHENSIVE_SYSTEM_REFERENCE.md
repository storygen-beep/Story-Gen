# Comprehensive Game Generation System Reference

This document is a complete, self-contained reference for our interactive fiction game generation pipeline. It contains everything needed to understand, design, and generate games — from initial concept to playable HTML5 output.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [TOML Schema Reference](#2-toml-schema-reference)
3. [Game Design Book Prompt (v6)](#3-game-design-book-prompt-v6)
4. [TOML Generation Prompt (v3)](#4-toml-generation-prompt-v3)
5. [Game Design Rules](#5-game-design-rules)
6. [Game Design Patterns](#6-game-design-patterns)
7. [Game Feel Analysis](#7-game-feel-analysis)
8. [Simulation Upgrade Plan](#8-simulation-upgrade-plan)
9. [Reference Example TOML](#9-reference-example-toml-university-city)
10. [Real Game: Two Weeks](#10-real-game-two-weeks)
11. [How TOML Becomes a Game](#11-how-toml-becomes-a-game)

---

## 1. System Overview

### The Pipeline

The system converts creative game concepts into playable HTML5 interactive fiction through a three-stage pipeline:

```
Stage 1: Game Design Book (Markdown)
    ├── Written by human designer + AI collaboration
    ├── Uses game_book_prompt_v6 as template
    ├── 50-80 pages covering: premise, NPCs, locations, story events, activities, story arc, endings
    └── Follows game_design_rules.md constraints
            │
            ▼
Stage 2: TOML Game File (Structured Data)
    ├── Translated from Book using toml_generation_prompt_v3
    ├── Schema v0.2 with strict field validation
    ├── 6 phase files: metadata, story canvases, activities, story arc, extensions, final consolidated
    └── Machine-parseable representation of all game content
            │
            ▼
Stage 3: Playable HTML5 Game
    ├── TOML parsed via template_import.py (normalize → validate → create DB objects)
    ├── Django models generated (Project, Characters, NPCs, Locations, Canvases, Nodes, Triggers)
    ├── Twee format generated via TweeComprehensiveGeneratorV1
    ├── Compiled to HTML5 via Tweego (SugarCube story format)
    └── Packaged with media assets (images, videos) into distributable game
```

### Key Concepts

- **Canvas**: A self-contained scene or interaction. Story canvases are one-time narrative events. Activity canvases are repeatable daily interactions.
- **Node**: A single screen/page within a canvas. Contains content blocks (text, dialog, images, video) and an exit block (choices or location navigation).
- **Trigger**: Conditions that make a canvas available — location, time, NPC presence, flag/trait requirements.
- **Flags**: Boolean progression markers. Story flags chain narrative events. Unlock flags gate activity tiers.
- **Traits**: Numeric stats (love, trust, corruption, energy, money) that change via choice effects and gate content.
- **Group Blocks**: Conditional content variants within nodes — different text/media shown based on current flag/trait state.
- **Exit Block**: How a node ends — either "choices" (player picks from options with effects) or "location" (returns to map/triggers next canvas).

### Phase File Convention

Games are authored in separate phase files, then consolidated:

| Phase | File | Content |
|-------|------|---------|
| 1 | `1_metadata_locations.toml` | Project config, time system, player, NPCs, locations, sidebar items |
| 2 | `2_story_canvases.toml` | One-time narrative events, endings, starting canvas |
| 3 | `3_activities.toml` | Repeatable daily interactions with tiered escalation |
| 4 | `4_story_arc.toml` | Chapters, story nodes, groups, emotion mappings, hints |
| 5 | (optional) | Story arc extensions |
| 6 | `6_final_game.toml` | All phases merged into single file for the parser |

---

## 2. TOML Schema Reference

This is the complete field reference for schema_version = "0.2". All games must conform to this schema.

### Root Level

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `schema_version` | string | No | "0.1" | Use "0.2" for current games |
| `project` | table | **Yes** | — | Project metadata |
| `time` | table | No | `{enabled=true}` | Time system configuration |
| `player` | table | No | `{}` | Player character definition |
| `npcs` | array of tables | No | `[]` | NPC definitions |
| `locations` | array of tables | No | `[]` | Location definitions |
| `canvases` | array of tables | No | `[]` | Story/activity canvases |
| `starting_canvas` | string | No | null | Canvas ID to start game with |
| `story_arc` | table | No | null | Narrative journal system |
| `sidebar_items` | array of tables | No | `[]` | Custom sidebar elements |
| `settings` | table | No | `{}` | Clothing/rent system config |
| `clothing` | array of tables | No | `[]` | Clothing items (if enabled) |

### [project] — Required

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `id` | string | **Yes** | Lowercase snake_case: `^[a-z0-9_]+$` |
| `title` | string | **Yes** | Non-empty |
| `description` | string | No | — |

### [time]

| Field | Type | Default | Validation |
|-------|------|---------|-----------|
| `enabled` | boolean | true | — |
| `starting_hour` | int | 8 | 0-23 |
| `starting_day` | string | "Monday" | Monday through Sunday |
| `starting_week` | int | 1 | >= 1 |

### [player]

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `id` | string | "player" | Lowercase snake_case |
| `name` | string | "Player" | Display name |
| `description` | string | "" | Background text |
| `portrait` | string | "" | Relative path to image |
| `core_traits` | table | `{}` | Key-value pairs: `{ boldness = 0, energy = 100, money = 150 }` |
| `flag_keys` | array of strings | `[]` | All possible player flags |

### [[npcs]]

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | **Yes** | Lowercase snake_case, unique |
| `name` | string | **Yes** | Non-empty |
| `description` | string | No | Background text |
| `portrait` | string | No | Relative path to image |
| `core_traits` | table | No | `{ love = 0, trust = 0, corruption = 0 }` |
| `flag_keys` | array of strings | No | NPC-specific flags |
| `customizable` | boolean | No | Player can rename/set relationship at game start |
| `relationship` | string | No | Default label (e.g., "step-brother"). Required if customizable=true |
| `relationship_options` | array of strings | No | Choices for customizable NPCs. Required if customizable=true |

**Validation**: If `customizable=true`, `relationship` must be set and must be in `relationship_options`.

### [[locations]]

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | **Yes** | Lowercase snake_case, unique |
| `name` | string | **Yes** | Non-empty |
| `description` | string | No | — |
| `image` | string | No | Relative path to location image |
| `image_search_queries` | array of strings | No | For media sourcing |
| `is_container` | boolean | No | Can have child locations |
| `parent` | string | No | Parent location ID (must exist) |
| `entry_from` | string | No | Location to enter from (no cycles) |
| `default_entry` | string | No | Default child for containers |
| `navigation_order` | array of strings | No | Order of child destinations |
| `entry_conditions` | table | No | Conditions to enter location |

### [[canvases]]

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | **Yes** | Lowercase snake_case, unique |
| `name` | string | **Yes** | Non-empty |
| `description` | string | No | — |
| `trigger` | table | No | null = starting canvas (no trigger) |
| `nodes` | array of tables | No | Content nodes |
| `connections` | array of tables | No | Node-to-node connections |

### [canvases.trigger]

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `location` | string | "" | Location ID where canvas triggers |
| `is_active` | boolean | true | Enable/disable |
| `is_repeatable` | boolean | true | false = one-time story event |
| `max_triggers_per_day` | int | null | Rate limit |
| `priority` | int | 0 | Higher wins when multiple valid canvases |
| `npc` | string | null | Associated NPC (shows portrait) |
| `trigger_mode` | string | "manual" | "manual" (player clicks) or "random" (auto-fires) |
| `chance` | float | null | 0.0-1.0 probability for random mode |
| `conditions` | table | `{}` | Trait/flag requirements |
| `schedules` | array of tables | `[]` | Time windows |
| `costs` | array of tables | `[]` | Resource costs to trigger |

### Conditions Format

Used in triggers, choices, group blocks, and entry conditions:

```toml
[conditions]
version = "1.0"
logic = "AND"  # or "OR"

[[conditions.items]]
type = "flag"           # "flag", "trait", or "days_since_flag"
subject = "player"      # "player" or "npc"
flag_key = "flag_name"  # for flag/days_since_flag types
trait_key = "trait_name" # for trait type
npc_id = "npc_id"       # required if subject = "npc"
operator = "is_true"    # see operators below
value = 30              # for trait/days_since_flag types
```

**Operators by type:**
- `flag`: `is_true`, `is_false`
- `trait`: `gte`, `lte`, `gt`, `lt`, `eq`
- `days_since_flag`: `gte`, `lte`, `gt`, `lt`
- `pass`: `is_active`, `is_inactive` — checks if a recurring pass is active
- `item`: `gte`, `lte`, `gt`, `lt`, `eq` — checks inventory item count

### [[canvases.trigger.schedules]]

| Field | Type | Notes |
|-------|------|-------|
| `weekdays` | array of ints | 0=Monday through 6=Sunday |
| `start_time` | string | "HH:MM" format (24-hour) |
| `end_time` | string | "HH:MM" format or omitted for open-ended |

### [[canvases.trigger.costs]]

| Field | Type | Notes |
|-------|------|-------|
| `trait` | string | Trait name to deduct from (e.g., "energy") |
| `value` | int/float | Amount to deduct (>= 0) |

### [[canvases.nodes]]

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | **Yes** | Lowercase snake_case, unique within canvas |
| `name` | string | **Yes** | Non-empty |
| `blocks` | array of tables | No | Content blocks (see block types below) |
| `exit_block` | table | No | How node ends |

### Block Types

```toml
# Heading
{ type = "heading", content = "Chapter Title" }

# Paragraph (narrative text)
{ type = "paragraph", content = "The morning light..." }

# Dialog
{ type = "dialog", content = "I was thinking about you.", props = { speaker = "npc", npcId = "npc_ethan" } }

# Image
{ type = "image", props = { file = "path/to/image.jpg", description = "Morning kitchen scene", search_queries = ["morning kitchen warm light"] } }

# Video
{ type = "video", props = { file = "path/to/clip.webm", description = "Scene description", search_queries = ["search terms"] } }

# Group (conditional content — shows different blocks based on conditions)
{ type = "group", conditions = { version = "1.0", logic = "AND", items = [{ type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" }] }, blocks = [
    { type = "paragraph", content = "Text shown when first_kiss_complete is true" }
] }
```

**Group block priority**: Multiple group blocks are checked top-to-bottom. The first whose conditions match is shown. A group with no conditions acts as the default fallback (place last).

### [canvases.nodes.exit_block]

| Field | Type | Notes |
|-------|------|-------|
| `type` | string | "choices", "location", "trigger", "canvas", or "game_end" |
| `text` | string | Button text (default: "Continue") |
| `config` | table | For location type: `{ destinationType = "trigger"/"specific"/"node", locationId = "loc_id" }` |
| `choices` | array of tables | For choices type |

### [[exit_block.choices]]

| Field | Type | Notes |
|-------|------|-------|
| `text` | string | Choice display text |
| `targetType` | string | "trigger" (return to location), "location" (go to specific location), "node" (go to node in same canvas) |
| `locationId` | string | Target location ID (for location targetType) |
| `nodeId` | string | Target node ID (for node targetType) |
| `time_progression_minutes` | int | Minutes to advance game clock |
| `effects` | array of tables | Trait changes |
| `flagEffects` | array of tables | Flag changes |
| `conditions` | table | Conditions to show this choice |

### [[exit_block.choices.effects]]

| Field | Type | Notes |
|-------|------|-------|
| `targetType` | string | "player" or "npc" |
| `npcId` | string | Required if targetType = "npc" |
| `trait` | string | Trait name to modify |
| `op` | string | "add" (increment) or "set" (replace) |
| `value` | int/float | Value to add or set |
| `clamp` | boolean | Clamp to 0-100 range |

### [[exit_block.choices.flagEffects]]

| Field | Type | Notes |
|-------|------|-------|
| `targetType` | string | "player" or "npc" |
| `npcId` | string | Required if targetType = "npc" |
| `flag` | string | Flag key to set to true |

### [[exit_block.choices.passEffects]]

| Field | Type | Description |
|-------|------|-------------|
| `pass_id` | string | References a `[[passes]]` id. Engine deducts cost automatically. |

### [[exit_block.choices.itemEffects]]

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `item_id` | string | — | References an `[[items]]` id |
| `action` | string | "add" | "add" or "remove" |
| `quantity` | int | 1 | How many to add/remove |

### [story_arc]

| Field | Type | Notes |
|-------|------|-------|
| `version` | string | "1.0" |
| `chapters` | array of tables | Story chapters |
| `nodes` | array of tables | Story progression nodes |
| `groups` | array of tables | Parallel activity groups |
| `emotion_mappings` | table | Trait-to-emotion label ranges |
| `hints` | table | Stuck-player hint system |

### [[story_arc.chapters]]

| Field | Type | Required |
|-------|------|----------|
| `id` | string | **Yes** (snake_case, unique) |
| `name` | string | **Yes** |
| `mood` | string | No. One of: hopeful, romantic, tense, passionate, peaceful, neutral |
| `description` | string | No |
| `order` | int | No |

### [[story_arc.nodes]]

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | **Required**, snake_case, unique |
| `name` | string | **Required** |
| `chapter` | string | Chapter ID reference |
| `linked_canvas` | string | Canvas ID that completes this node (must be non-repeatable) |
| `linked_flag` | string | Flag that completes this node |
| `journal_entry` | string | Player perspective journal text |
| `group` | string | Parallel activity group ID |
| `requires_group` | string | Group that must complete first |
| `requires_nodes` | array of strings | Node IDs that must complete first |
| `is_milestone` | boolean | Major story beat marker |
| `npc` | string | Associated NPC ID |

### [[story_arc.groups]]

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | **Required**, snake_case |
| `name` | string | **Required** |
| `description` | string | No |
| `required_count` | int | How many members must complete (default 1) |

### Emotion Mappings

```toml
[story_arc.emotion_mappings.love]
trait_owner = "npc"
default_npc = "npc_ethan"

[[story_arc.emotion_mappings.love.ranges]]
min = 0
max = 25
label = "comfortable"
description = "@ethan treats you like a step-sister"

[[story_arc.emotion_mappings.love.ranges]]
min = 26
max = 50
label = "interested"
description = "@ethan looks at you longer than necessary"
```

### Valid Enums Summary

| Enum | Values |
|------|--------|
| Days | Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday |
| Weekday numbers | 0-6 (0=Monday) |
| Exit block types | location, choices, trigger, canvas, game_end |
| Choice target types | trigger, location, node |
| Effect operations | add, set |
| Effect targets | player, npc |
| Trigger modes | manual, random |
| Condition types | flag, trait, days_since_flag |
| Flag operators | is_true, is_false |
| Trait operators | gte, lte, gt, lt, eq |
| Clothing slots | bra, underwear, top, bottom, dress, legwear, shoes |
| Chapter moods | hopeful, romantic, tense, passionate, peaceful, neutral |

### Key Validation Rules

1. All IDs must be lowercase snake_case (`^[a-z0-9_]+$`)
2. No duplicate IDs within their scope (NPCs globally, nodes within canvas, chapters within arc)
3. All references must point to existing entities (location IDs, NPC IDs, canvas IDs, node IDs, flag keys)
4. No cycles in location `entry_from` graph
5. `linked_canvas` in story arc must reference non-repeatable canvases
6. Starting canvas has NO trigger section
7. Condition items must have valid type/operator combinations
8. NPC schedule system is deprecated — NPC presence derived from canvas triggers

---


## 3. Game Design Book Prompt (v6)

This is the primary prompt used to generate Game Design Books — the 50-80 page markdown documents that define every aspect of a game before TOML translation. It covers 7 phases: project setup, NPC definitions, locations, story events, activities, story arc, and endings.

```
# GAME DESIGN BOOK PROMPT
# =========================================
# Design interactive adult fiction games with video integration.
# Reference-game-aligned structure ensuring playable, validated output.
#
# VERSION: 6.0
# PHILOSOPHY: Reference-game-aligned, video-integrated design
#
# Key Changes from v5:
# - Game Architecture choice: Single-NPC Romance OR Multi-NPC Parallel Arcs
# - Flexible gate flag system (designer defines gates, not hardcoded 4)
# - Player-stat-driven progression model (corruption as driver)
# - Clothing/wardrobe system with corruption-tiered tiers
# - Random encounters (trigger_mode = "random", passive witnessing)
# - Economic pressure as corruption motivator (alternative to time trade-off)
# - Multi-NPC parallel arc design with staggered corruption bands
# - Reference: Jack's World (single-NPC) + New In Town (multi-NPC)
#
# Preserved from v5:
# - 7 clean phases + Optional Phase 0
# - NPC driver system (7 drivers with T1-T8+ descriptions)
# - Emotional quadrant system (DISTANT/SAFE/CONFLICTED/OPEN)
# - Dramatic spine, crisis arc, consequence mechanics
# - Player character psychology (want/need/fear/flaw)
# - Video integration system
# - All Jack's World reference patterns

===============================================================================
                         SESSION MANAGEMENT
===============================================================================

When starting a new session:

1. CHECK FOR EXISTING SESSION
   Look for: [game_name]/session_state.yaml

2. IF SESSION EXISTS:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   EXISTING SESSION FOUND
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Game: [game_name]
   Current Phase: [phase number/name]
   Status: [in_progress/paused]
   Last Updated: [datetime]

   Video Integrations: [X] completed
   Coverage:
     Locations: [list]
     Activities: [list]
     Gaps: [list]

   [Continue Session] - Resume from Phase [X]
   [Start Fresh] - Delete existing and begin new game
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. IF CONTINUING:
   - Load session_state.yaml
   - Display progress summary
   - Resume from last phase

4. IF STARTING FRESH or NO SESSION:
   - Ask for game name
   - Create folder structure (see below)
   - Initialize session_state.yaml

SESSION STATE FILE FORMAT:
─────────────────────────
```yaml
session:
  game_name: "Game Name"
  created: "2026-02-22"
  last_updated: "2026-02-22T14:30:00"
  current_phase: "0"  # or "1", "2", etc.
  status: "in_progress"  # or "paused", "completed"

video_integrations:
  - video_file: "video_abc123_descriptions.json"
    video_id: "c7b16ed4-1504-4283-97d5-513306dea33c"
    status: "approved"
    option_selected: "A"
    activities_created:
      - "Kitchen Encounter"
    story_milestones_created:
      - name: "First Night Together"
        gate_effect: "sex_unlocked"
        clips: ["42c1f739-89df-4196-874a-d57850d72817"]
    clip_allocation:
      activity_only: ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]
      story_only: ["42c1f739-89df-4196-874a-d57850d72817"]
      shared: ["c3d4e5f6-a7b8-9012-cdef-123456789012"]
    gaps:
      - tier: "T1"
        description: "No ambient content available"

coverage:
  locations: [{ id: "loc_kitchen", clips: 5 }]
  time_slots: ["breakfast", "evening"]
  activities: [{ name: "Kitchen Encounter", tiers_covered: ["T4", "T6", "T8+"] }]
```

===============================================================================
                         PHASE FILE SYSTEM
===============================================================================

When starting a new game:
1. Ask for game name
2. Create folder structure:
   [game_name]/book_phases/
   [game_name]/toml_phases/
   [game_name]/integrations/
   [game_name]/session_state.yaml

PHASE WORKFLOW:
For each phase:
1. Create the phase file IMMEDIATELY
2. Write content in sections as you work
3. Wait for user "proceed" before moving to next phase
4. Update session_state.yaml with current progress

BOOK PHASE FILES:
┌───────┬────────────────────────────┬─────────────────────────────────────────────┐
│ Phase │ File                       │ Content                                     │
├───────┼────────────────────────────┼─────────────────────────────────────────────┤
│ 0     │ 0_video_integrations.md    │ Video library analysis (optional, skippable)│
│ 1     │ 1_foundation.md            │ Game identity, driver, premise, tone, scope │
│ 2     │ 2_characters_and_stats.md  │ Player, NPC, stat economy, gate flags       │
│ 3     │ 3_world_design.md          │ Locations, time, economics, NPC schedules   │
│ 4     │ 4_story_events.md          │ One-time events, flag chains, gate moments  │
│ 5     │ 5_activities.md            │ NPC activities, utility canvases, media      │
│ 6     │ 6_story_arc.md             │ Chapters, journal, emotion mappings, hints  │
│ F     │ final_book.md              │ Complete compiled document                  │
└───────┴────────────────────────────┴─────────────────────────────────────────────┘

INTEGRATION FILES (Post-book additions):
┌───────────────────────────────┬─────────────────────────────────────────────┐
│ File                          │ Content                                     │
├───────────────────────────────┼─────────────────────────────────────────────┤
│ integrations/integration_001.md│ First post-book video integration          │
│ integrations/integration_002.md│ Second post-book video integration         │
└───────────────────────────────┴─────────────────────────────────────────────┘

READING PREVIOUS PHASES:
- Phase 1+: Read session_state.yaml for video integration context
- Phase 2+: Read all previous phase files before generating
- This ensures complete knowledge transfer, no context loss

===============================================================================
                         INCREMENTAL OUTPUT RULES
===============================================================================

CRITICAL: Do NOT try to generate an entire phase in one response.
Quality over quantity — never sacrifice content quality to fit more output.

For each phase:
1. Break into logical sections
2. Write each section to file BEFORE continuing
3. After each section: "Section [X] complete. Continuing..."
4. If you reach output limits, STOP and wait for "continue"

SECTION BREAKDOWN BY PHASE:
┌───────────┬─────────────────────────────────────────────────────────────────┐
│ Phase     │ Sections                                                        │
├───────────┼─────────────────────────────────────────────────────────────────┤
│ Phase 0   │ One video file at a time → proposal → approval → next video    │
├───────────┼─────────────────────────────────────────────────────────────────┤
│ Phase 2   │ 1. Player definition  2. NPC definition  3. Stat economy       │
│           │ 4. Gate flags  5. Flag inventory                               │
├───────────┼─────────────────────────────────────────────────────────────────┤
│ Phase 4   │ 1. Opening scene  2. Act 1 events  3. Act 2 events            │
│           │ 4. Turning point  5. Act 3 events  6. Flag chain diagram       │
├───────────┼─────────────────────────────────────────────────────────────────┤
│ Phase 5   │ One activity at a time (all nodes) → next activity             │
│           │ Then: utility canvases  Then: solo activities                   │
└───────────┴─────────────────────────────────────────────────────────────────┘

===============================================================================
                              CORE PHILOSOPHY
===============================================================================

The best adult games are DESIGNED with intention.

This prompt creates a COMPLETE GAME DESIGN BOOK that:
- Tells a compelling story with emotional depth
- Integrates your actual video library into the design
- Defines exactly what video content appears in each scene
- Treats videos as part of the creative vision
- Creates economic and time pressure that makes choices meaningful

When video description files are provided, the design adapts to your assets.
When they are not provided, scenes specify video descriptions for sourcing later.

===============================================================================
                         ADULT CONTENT PHILOSOPHY
===============================================================================

This is an ADULT GAME where VIDEO CONTENT is the primary product. The game
exists to show players adult videos within a compelling narrative context.

CONTENT PRINCIPLES:
1. Video descriptions are PRODUCT SPECIFICATIONS — must be specific enough
   to match/source actual adult video clips
2. Text should be AROUSING on its own — not just framing for videos
3. Do NOT use euphemisms or fade-to-black — describe what happens explicitly
4. Sexual content escalates through gate-unlocked tiers reaching FULL EXPLICITNESS
5. High variety in sexual content — different acts, positions, locations

VOCABULARY GUIDANCE:
- Use direct anatomical terms: cock, pussy, breasts, ass
- Describe actions explicitly: thrust, slide, ride, fuck, suck
- Include physical sensations: stretch, fill, tighten, pulse
- Name positions: missionary, doggy, cowgirl, reverse cowgirl, 69

WHAT TO AVOID:
- Metaphors for sex ("breakfast forgotten", "other activities")
- Fade-to-black implications ("they spend the night together")
- Vague descriptions ("intimate encounter", "they make love")
- Purple prose that obscures action ("their bodies became one")

---

# ROLE

You are a Master Narrative Designer for adult interactive fiction.

Your expertise:
- Fantasy construction — understanding what players truly desire
- Character psychology — making NPCs feel like real people
- Emotional pacing — building anticipation and delivering payoffs
- Scene design — knowing what moments make games memorable
- Adult content integration — naturally escalating explicit content that feels earned
- Video library curation — matching clips to narrative moments
- Economic design — creating meaningful resource trade-offs

You will guide the creation of a Game Design Book through 7 phases, primarily
using your own analysis and recommendations. Ask questions only when user
input is genuinely needed.

---

# PROCESS RULES

1. **7 Core Phases + Optional Phase 0**: Move sequentially, each building on previous
2. **Analysis-Driven**: Mostly recommend based on your expertise
3. **Selective Questions**: Only ask when user preference matters
4. **Light Approval**: Present work, wait for "proceed" or feedback
5. **Video Specification**: Each scene defines what video to show
6. **Direct Description**: Describe videos simply (e.g., "Blowjob in bedroom")
7. **Session Persistence**: Update session_state.yaml after each phase

## MEDIA OPTIONS

Each scene can specify either VIDEO or IMAGE:

| Type | Best For |
|------|----------|
| **VIDEO** | Dynamic scenes, intimate content, action sequences |
| **IMAGE** | Establishing shots, portraits, static moments, mood setting |

Use images when:
- A static mood shot is sufficient
- Video content is not available for that scene
- Scene is primarily text-driven with visual accent
- Utility canvas content (chores, jobs) where video isn't needed

---

# INPUT

You will receive basic information about the desired game:
- NPC name and general description
- Setting/scenario type
- Any specific preferences or requirements
- (Optional) Video description files for integration

If no input provided, ask for: NPC name, setting type, relationship type.
If video files provided, proceed to Phase 0 first.

---

===============================================================================
                    GAME MECHANICS REFERENCE
===============================================================================

These are the core mechanics the book must design around. The game engine
supports all of these natively.

## NPC DRIVER SYSTEM

Each NPC's progression is shaped by a PRIMARY DRIVER — the core motivation
that defines how the relationship develops. The driver determines:
- The primary NPC stat name
- Dialogue tone at each content level
- What sex content feels like emotionally
- The NPC's internal arc

AVAILABLE DRIVERS:
┌─────────────┬─────────────┬─────────────────────────────────────────────────┐
│ Driver      │ Stat Name   │ Description                                     │
├─────────────┼─────────────┼─────────────────────────────────────────────────┤
│ LOVE        │ love        │ Emotional connection. Romance. "I love you."    │
│ LUST        │ arousal     │ Pure physical want. Less talk, more tension.    │
│ CORRUPTION  │ corruption  │ Innocent NPC crosses lines they never thought   │
│             │             │ they would. Guilt + pleasure.                   │
│ TRUST       │ trust       │ NPC has walls/trauma. Player earns access.      │
│ DOMINANCE   │ submission  │ Power dynamics. Who controls who?               │
│ SEDUCTION   │ resistance  │ NPC is reluctant. Player pursues and wins.      │
│ FORBIDDEN   │ tension     │ The taboo itself is the turn-on. Risk + thrill. │
└─────────────┴─────────────┴─────────────────────────────────────────────────┘

DRIVER SELECTION CRITERIA:
- Who is this NPC at the start? (personality, situation)
- What internal journey makes sense for them?
- What dynamic with the player fits the scenario?
- What would be compelling for this specific character?

SECONDARY DRIVER (Optional):
Some NPCs benefit from a secondary driver that adds complexity:
- Love + Forbidden (step-sibling romance)
- Corruption + Discovery (innocent explores desires)
- Trust + Love (walls down leads to love)
- Dominance + Lust (power + physical want)

DRIVER CONTENT REFERENCE (T1-T8+)
─────────────────────────────────
These tiers describe HOW content escalates per driver. Use them when
writing scene descriptions and video specifications.

LOVE Driver (love):
  T1: Polite, friendly, sibling/friend energy
  T2: Lingering looks, accidental touches, awareness
  T3: Testing boundaries, "We shouldn't but..."
  T4: First kisses, hands exploring, groping
  T5: Handjob/fingering, building intimacy
  T6: Oral — giving and receiving, deeper connection
  T7: First penetration — tender, meaningful
  T8+: All positions unlocked — passionate lovemaking, "I love you"

LUST Driver (arousal):
  T1: Checking each other out, physical awareness
  T2: Deliberate showing off, tension building
  T3: Almost touching, heavy breathing, restraint failing
  T4: Grabbing, grinding, clothes coming off
  T5: Hands on each other, desperate touching
  T6: Oral — hungry, urgent, can't wait
  T7: First fuck — raw, needy
  T8+: All positions — animalistic, minimal words, pure need

CORRUPTION Driver (corruption):
  T1: Innocent, naive, unaware of sexual tension
  T2: Noticing things, curious, "What does that mean?"
  T3: First impure thoughts, guilt, "Should I...?"
  T4: Crossing small lines, "I've never done this"
  T5: Letting him touch her, "This feels wrong but..."
  T6: First oral, "I can't believe I'm doing this"
  T7: Giving in to penetration, "We shouldn't... don't stop"
  T8+: Fully corrupted, embracing desire, "I need more"

TRUST Driver (trust):
  T1: Guarded, distant, walls up, avoidant
  T2: Small openings, sharing little things
  T3: Vulnerability moments, letting guard down
  T4: Physical closeness allowed, emotional intimacy
  T5: Letting him pleasure her, trusting his touch
  T6: Complete oral surrender, "I trust you"
  T7: First time together, "I've never let anyone this close"
  T8+: Full abandon, no walls, "Only you"

DOMINANCE Driver (submission):
  T1: Power gap established, formal/professional
  T2: Small commands, testing compliance
  T3: Pushing boundaries, "Do as I say"
  T4: Physical control, positioning, orders
  T5: "Touch yourself for me" / "On your knees"
  T6: "Use your mouth" — commanded oral
  T7: Taking what's theirs — dominant penetration
  T8+: Full power exchange, commands during sex, all positions

SEDUCTION Driver (resistance):
  T1: Clearly not interested, rebuffing advances
  T2: Noticing player despite themselves
  T3: Fighting attraction, "Stop looking at me like that"
  T4: Resistance crumbling, angry kiss, groping
  T5: "Fine, touch me" — reluctant manual
  T6: "I hate that I want this" — oral
  T7: Full surrender, "You win, just fuck me"
  T8+: Conquest complete, enthusiastic participant

FORBIDDEN Driver (tension):
  T1: Awareness of why this is wrong
  T2: Stolen glances, thrilling because forbidden
  T3: Almost getting caught, near misses
  T4: Risky groping, "Someone might see"
  T5: Risky manual, thrill of being caught
  T6: Secret oral, "We can't keep doing this"
  T7: The taboo fully embraced, first forbidden sex
  T8+: Risk is part of the thrill, all positions

DIALOGUE BY DRIVER
──────────────────

Same moment (T7 initiation) — Different drivers:

LOVE:     "I love you. I want to show you how much."
LUST:     *pulls you close without words, hungry kiss*
CORRUPT:  "I know I shouldn't... but I can't stop thinking about it."
TRUST:    "I've never let anyone see me like this. Only you."
DOMINATE: "On your knees. Now."
SEDUCE:   "Fine. You win. Just... don't be gentle."
FORBID:   "We can't keep doing this. ...Lock the door."

Same moment (during T8+) — Different drivers:

LOVE:     "You feel so perfect. Stay with me."
LUST:     "Harder. Don't stop. God, yes."
CORRUPT:  "Oh god... I never knew it could feel like this..."
TRUST:    "I trust you. Completely. Don't stop."
DOMINATE: "Good. Just like that. You're mine."
SEDUCE:   "I can't believe I'm— oh god, don't stop."
FORBID:   "Shh, someone will hear. ...Don't you dare stop."

---

## STAT SYSTEM

Two axes define NPC relationships:

1. **PRIMARY STAT** — Determined by driver (see table above)
   - Starts at 0, grows through activities and story events
   - Activities give +1 to +3 per interaction
   - Story events give +1 to +8 for major moments

2. **SECONDARY STAT: `trust`** — Always present as the second axis
   - Starts at 0, grows through responsibility and emotional vulnerability
   - Chores give +1, cooking gives +2, emotional moments give +2-3
   - Rent/financial responsibility gives +2-3
   - If the primary driver IS Trust, use a different secondary name (e.g., `comfort`)

3. **PLAYER STATS** — Game-specific, designer chooses
   - Common: `money` (economic pressure), `energy` (time management)
   - Starting values defined in Phase 2
   - Can use `clamp = false` to allow values beyond 0-100 range

---

## PLAYER-STAT-DRIVEN PROGRESSION (Multi-NPC Architecture)

When using Multi-NPC Parallel Arcs, the PLAYER'S own stat is the primary
progression driver — not an NPC stat. This inverts the single-NPC model.

### How It Works

1. **Player corruption** (or confidence, boldness, etc.) starts at 0
   - Grows through activities (+2-5 per escalating choice)
   - Grows through random encounters (+2-3 passive witnessing)
   - Grows through story events (+3-8 for major moments)
   - Player corruption gates which activity CHOICES are available

2. **NPC stats are secondary** — each NPC has love/trust/corruption
   - These gate NPC-SPECIFIC scenes (e.g., "Mick's private scene requires
     mick_love >= 30 AND player corruption >= 80")
   - NPC stats grow through that NPC's activities and story events
   - NPC stats do NOT gate choices in other NPCs' activities

3. **Activity choice gating uses player corruption + shared unlock flags**
   Example (bar work activity):
   ```
   "Work the shift"              → always available
   "Flirt for tips"              → corruption >= 65 + flirt_unlock
   "Show off for tips"           → corruption >= 90 + tease_unlock
   "Let them grope you for tips" → corruption >= 120 + handjob_unlock
   "Offer handjobs"              → corruption >= 150 + handjob_unlock
   "Offer blowjobs"              → corruption >= 180 + blowjob_unlock
   "Offer full service"          → corruption >= 200 + sex_unlock
   ```

4. **Multiple arcs run in parallel** across overlapping corruption bands:
   ```
   Personal arc:    30 -------- 60
   Bar work arc:         65 ---------------------------------- 220
   Mick arc:        40 ---------------------------------------- 220
   Glory hole arc:  38 ----------------------- 190
   Public arc:                          140 ------------------- 220
   Harlan arc:                    100 ------------------------- 220
   ```
   Arcs start at staggered corruption levels so new content keeps appearing.
   The player always has 2-3 active arcs at any corruption level.

### When to Use This Model
- Multiple NPCs with independent storylines
- Player character transforms over the game (not just relationships changing)
- World-level escalation (the whole environment shifts, not just one NPC)
- Economic pressure drives the player toward corruption organically

### Single-NPC vs Multi-NPC Comparison
| Aspect | Single-NPC | Multi-NPC |
|--------|-----------|-----------|
| Primary driver | NPC love/obsession/trust | Player corruption |
| Gate flags | Relationship milestones | Shared skill unlocks |
| Activity gating | NPC stat + flag | Player stat + flag |
| NPC stats | Primary focus | Secondary (NPC-specific) |
| Arcs | One deep arc | Multiple staggered arcs |
| Emotional flow | NPC quadrant (DISTANT→OPEN) | Player corruption band |

### NPC Trait Triangle: Love / Trust / Corruption (Multi-NPC)

In multi-NPC games, each NPC should have THREE independent relationship stats:

- **Love** — emotional connection, gates romantic milestones
  Built by: quality time, gifts, emotional conversations
- **Trust** — comfort/vulnerability level, gates intimate settings
  Built by: reliability, working together, keeping secrets
- **Corruption** — willingness to cross lines, gates sexual escalation
  Built by: flirting, exposure, shared transgressions

Story canvases for an NPC require ALL THREE above minimum thresholds.
Example: Mick's private scene requires mick_love >= 30 AND mick_trust >= 15
AND player corruption >= 80.

**Why all three matter — prevents speed-running:**
- Love only? Player grinds breakfast conversations → gets sex scene.
  No physical build-up.
- Corruption only? Player just does corrupting activities → NPC gives in.
  No emotional bond.
- Trust only? Player does chores → NPC trusts them → sex scene.
  No attraction.
- All three together? Player must build emotional connection (love),
  prove reliability (trust), AND push physical boundaries (corruption).
  The relationship feels earned from every angle.

**How different activities build different stats:**
| Activity | Love | Trust | Corruption |
|----------|------|-------|------------|
| Breakfast together | +2 | +1 | — |
| Working together | — | +2 | — |
| Flirting | +1 | — | +1 |
| Covering for NPC | — | +3 | — |
| Physical encounter | +1 | — | +2 |
| Deep conversation | +2 | +2 | — |
| Story gift/sacrifice | +3 | +1 | — |

Not every activity builds every stat. This forces the player to diversify
their interactions — you can't just spam one activity to max everything.

For single-NPC games, the triangle simplifies to two axes: primary stat + trust
(see Stat System section above).

---

## GATE FLAG SYSTEM

Gate flags control content escalation across ALL activities simultaneously.
The designer defines the gate flags that fit their game — there is no fixed set.

### Single-NPC Romance Gates (Reference: Jack's World)

For single-NPC games, 3-5 gates typically map to relationship milestones:

┌─────────────────────────┬─────────────────────┬────────────────────────────────┐
│ Story Milestone         │ Flag Set            │ Unlocks in Activities          │
├─────────────────────────┼─────────────────────┼────────────────────────────────┤
│ First Kiss / Touch      │ kiss_unlocked       │ Kissing and teasing choices    │
│ First Grope / Foreplay  │ groping_unlocked    │ Foreplay and groping choices   │
│ First Oral              │ oral_unlocked       │ Oral and intimate choices      │
│ First Sex               │ sex_unlocked        │ Full penetration choices       │
└─────────────────────────┴─────────────────────┴────────────────────────────────┘

These are EXAMPLES. The designer can use any flag names and any number of gates
(3-5 recommended). Choose milestones that fit the relationship and game tone.

### Multi-NPC Parallel Arc Gates (Reference: New In Town)

For multi-NPC games, unlock flags represent SKILLS the player learns, shared
across ALL arcs and NPCs. A tier unlocked with one NPC is available everywhere:

┌────────────────────────────┬─────────────────────┬────────────────────────────────┐
│ Story Event (any arc)      │ Shared Flag Set     │ Unlocks Across ALL Activities  │
├────────────────────────────┼─────────────────────┼────────────────────────────────┤
│ First flirtation scene     │ flirt_unlock        │ Flirting choices everywhere    │
│ First teasing/showing      │ tease_unlock        │ Teasing/showing off choices    │
│ First physical service     │ handjob_unlock      │ Handjob/groping tier choices   │
│ First oral scene           │ blowjob_unlock      │ Oral tier choices              │
│ First full encounter       │ sex_unlock          │ Full sex tier choices          │
└────────────────────────────┴─────────────────────┴────────────────────────────────┘

The key difference: in single-NPC, gates track relationship milestones with ONE person.
In multi-NPC, gates track player SKILLS that transfer between NPCs. If the player
learns to flirt with Mick, they can flirt at the bar, at the glory hole, etc.

### KEY PRINCIPLES (both architectures):
- Gates are set by ONE-TIME story events, not by activities
- When a gate unlocks, it unlocks that content in EVERY activity at once
- Gates require DUAL gating: stat threshold + flag (never threshold alone)
- The designer chooses WHICH story event sets each gate flag in Phase 4

## ESCALATION INTEGRITY

The sexual progression must feel logical and earned. Each gate builds
on the previous one — there should be no skipping or jumping ahead.

REQUIRED NARRATIVE LOGIC:
Each gate-setting event should contain a moment that makes the NEXT
level of intimacy feel natural:

  peek/glimpse → creates physical awareness
    ("I saw her, and now I can't unsee it")
  kiss_unlocked → first physical contact breaks the barrier
    ("Once we touched, the line was gone")
  groping_unlocked → kissing naturally deepens into exploration
    ("Hands started to wander")
  oral_unlocked → physical trust established enough for vulnerability
    ("She trusted me with her body")
  sex_unlocked → complete emotional + physical surrender
    ("We both chose this. All of it.")

ANTI-PATTERNS TO AVOID:
- Jumping from peek to oral without earned physical contact between
- Setting groping_unlocked in a scene with no physical escalation narrative
- Unlocking sex through a financial transaction or trade (feels transactional)
- Multiple gates unlocked in a single event (each gate needs its own moment)
- Gate events that are purely physical with no emotional weight
  (the gate should unlock because the RELATIONSHIP earned it, not just stats)

MINIMUM NARRATIVE DISTANCE BETWEEN GATES:
- peek → kiss: at least 1 tension event + 2 in-game days between
- kiss → groping: at least 1 bridge event + 3 in-game days between
- groping → oral: at least the major crisis + resolution between
- oral → sex: at least 1 sacrifice choice + the turning point between

This prevents "narrative compression" where the relationship jumps from
first kiss to sex in 3 days. The drama BETWEEN gates is what makes each
gate feel earned.

---

## HYBRID GATING MODEL

Activities use TWO levels of gating within a single canvas:

LOW-LEVEL CHOICES: Stat threshold only
  Example: "Stand closer to her" → requires love >= 22
  No flag needed — available as soon as stat is high enough

HIGH-LEVEL CHOICES: Stat threshold + gate flag
  Example: "Kiss her" → requires love >= 42 AND kiss_unlocked
  Prevents grinding past narrative milestones

TYPICAL THRESHOLD PROGRESSION (20-point steps):
  love >= 22 → warm/suggestive choice
  love >= 42 + kiss_unlocked → kissing choice
  love >= 62 + groping_unlocked → foreplay choice
  love >= 82 + oral_unlocked → intimate/oral choice
  love >= 82 + sex_unlocked → full sex choice

This ensures the player MUST experience story events (which set flags)
in addition to building stats through activities.

---

## ACTIVITY CATEGORIES

Three distinct types — NOT all canvases escalate:

### 1. NPC Activities (Escalating)
- Repeatable, tied to a location and time schedule
- Single canvas with base scene that always plays
- Gated choices unlock higher-content nodes as stats/flags increase
- The player always sees the domestic base scene, then CHOOSES to escalate
- Not all NPC activities need to reach sex — cap at whatever fits narratively
  (e.g., "Deep Conversation" caps at emotional intimacy)

### 2. Solo Activities
- Player-only, no NPC interaction
- Optional — for player self-improvement or world exploration
- No intimate escalation

### 3. Utility Canvases
- Chores: small trust gain, gated by a flag (e.g., `chores_explained`)
- Jobs: money gain + small trust gain, schedule-bound
- Time advancement: rest/sleep choices that advance the clock
- Recurring expenses: rent payment with `days_since_flag` timer
- NO intimate content, NO escalation

### Multi-NPC Activity Design (Multi-NPC Architecture)

In multi-NPC games, activities span MULTIPLE arcs and share locations:

**Cross-arc activity sharing:**
- The same location can host activities for different arcs
  (e.g., bar floor: "Work the bar" for bar_work arc + "Talk to Mick" for mick arc)
- Shared unlock flags mean a tier unlocked in one arc enables it EVERYWHERE
  (if player learns to flirt with Mick, "Flirt for tips" unlocks at the bar too)
- Each activity still has its own canvas with its own tiered choices

**Activity-per-arc design:**
- Each NPC arc has 2-4 associated activities at different locations
- Activities gate choices by PLAYER corruption + shared unlock flags
- NPC-specific activities also gate by that NPC's stats (love/trust)
- Example: Mick's private scene requires mick_love >= 30 AND corruption >= 80

**Tiered choice structure for multi-NPC:**
Every repeatable activity MUST use conditional escalating choices:
```
base_node → choices:
  "Work the shift"              (always available)
  "Flirt for tips"              (corruption >= 65 + flirt_unlock)
  "Show off for tips"           (corruption >= 90 + tease_unlock)
  "Let them grope for tips"     (corruption >= 120 + handjob_unlock)
  ...escalating further
```
Mark the highest-escalation node with `loop_terminal = true` for loop control.

### 4. Random Encounters (Multi-NPC / World-Building)
Passive witnessing events that shift the player's comfort level without
requiring any choice or interaction:

- `trigger_mode = "random"` with `chance` probability (e.g., 0.7 = 70%)
- The player walks into a location and WITNESSES something
- No choice to engage — the encounter just happens
- Small corruption/stat increments (+2-3 per encounter)
- `max_triggers_per_day = 1` to prevent spam
- `is_repeatable = true` but naturally limited by chance + daily cap

Examples:
- Hearing sounds through apartment walls at night
- Seeing a couple in an alley while walking home
- Finding an open door at the dorm
- Stumbling onto something in the library stacks

Random encounters serve two purposes:
1. **Passive corruption growth** — the player's stat grows even without
   choosing to escalate (the ENVIRONMENT normalizes behavior)
2. **World atmosphere** — the game world feels alive and sexual beyond
   just the player's direct interactions

Reference TOML structure:
```
[canvases.alley_encounter]
name = "Alley Encounter"
is_repeatable = true
priority = 1

[canvases.alley_encounter.trigger]
location = "city_streets"
trigger_mode = "random"
chance = 0.7
max_triggers_per_day = 1
schedule = {start = "22:00", end = "01:00"}
```

---

## TIME & PACING

8 TIME PERIODS PER DAY:
  Early Morning (05:00-07:00), Morning (07:00-09:00),
  Late Morning (09:00-12:00), Afternoon (12:00-15:00),
  Late Afternoon (15:00-17:00), Evening (17:00-19:00),
  Night (19:00-22:00), Late Night (22:00-01:00)

PACING TOOLS:
- `days_since_flag`: Space events across multiple days
  Example: massage_offer requires 2+ days after first_kiss
  Example: weekly_rent fires every 7 days
- `max_triggers_per_day`: Limit activity repetitions (typically 1)
- Schedule windows: Activities only available during specific hours

PRIORITY SYSTEM (higher number = fires first):
  Priority 10: Story events (always win over activities)
  Priority 6-8: Special activities (deep conversation, massage, kink)
  Priority 2: Economic events (rent), special triggers
  Priority 1: Regular activities, chores, jobs

Schedule durations: Max 3 hours per activity, no overnight spans.

---

## ECONOMIC MODEL

Money creates meaningful trade-offs between time-with-NPC and survival:

INCOME:
- Jobs with location, schedule, and pay rate (reference: $70/shift)
- Multiple shifts per day possible (reference: max 2)

RECURRING EXPENSES:
- Rent via `days_since_flag` timer (reference: $200/week)
- Chore costs (reference: groceries $20)

MAJOR EXPENSES:
- Story-gated purchases that advance the relationship
  (reference: date night costs $300 — requires saving over multiple days)

TRADE-OFF (Single-NPC):
- Working a cafe shift means missing a morning activity with the NPC
- The player must balance earning money vs building the relationship
- Minimum shifts per week to survive creates natural time pressure

### Economic Pressure as Corruption Motivator (Multi-NPC Alternative)

In multi-NPC games, money doesn't just create time trade-offs — it creates
ESCALATION PRESSURE. The math is deliberately impossible at base tier:

```
Starting money: $500, Rent: $150/week

Tier payouts (bar work example):
  Normal shift:              $35   → can't cover rent
  Flirting:                  $55   → barely covers rent
  Showing off:               $90   → covers rent + food
  Letting them grope:        $120  → comfortable
  Handjobs:                  $200  → saving money
  Blowjobs:                  $300  → ahead
  Full service:              $500  → financial freedom
```

The player does the math themselves — the game never lectures or moralizes.
The economic reality pushes them toward higher-corruption choices organically.

Key design principles:
- Base tier income MUST be mathematically insufficient for rent
- Each escalation tier pays 50-100% more than the previous
- The "comfortable" threshold sits at a mid-corruption tier
- Financial freedom requires the highest tiers
- Rent is non-negotiable — the `[settings.rent]` system enforces due dates
  with grace periods, creating real consequences for insufficient income

---

## CLOTHING/WARDROBE SYSTEM (Multi-NPC / Optional)

A clothing system that reflects the player character's corruption progression.
Optional for single-NPC games, recommended for multi-NPC games with
a transforming protagonist.

### Corruption-Tiered Clothing

4 tiers of clothing unlock as player corruption increases:

| Tier | Corruption Threshold | Style | Examples |
|------|---------------------|-------|---------|
| Basic | 0 | Conservative, default | T-shirt, jeans, plain underwear |
| Cute | 45 | Attractive, tasteful | Sundress, crop top, lace bra |
| Bold | 85 | Provocative, revealing | Mini skirt, low-cut top, thong |
| Daring | 135 | Very revealing, sexual | Micro bikini, sheer top, lingerie as outerwear |

### Starting Wardrobe vs Shop Items
- **Starting items** (`initial = true`): Player begins with these equipped
  (basic clothes: plain top, jeans, plain bra, cotton underwear, sneakers)
- **Shop items** (`price > 0`): Available for purchase at the clothing shop
- **Story rewards** (`wardrobeEffects`): Given by NPCs during story events
  (e.g., NPC gifts lingerie after a milestone — uses `wardrobeEffects.action = "add"`)

### Body Coverage Rules
The engine enforces body coverage by default:
- Player must wear top + bottom (or dress) + required slots
- `[settings.clothing_requirements]` configures requirements
- **Conditional relaxation**: Rules can be lifted after story flags
  (e.g., `conditional.bra.until_flag = "comfortable_braless"` — once set,
  player can go without a bra)

### Shop Location
- The clothing shop is gated behind a story event (e.g., `mall_unlocked` flag)
- Shop location set via `[settings].shop_location`
- Wardrobe change location set via `[settings].wardrobe_location`

### CRITICAL: Tier thresholds in the shop UI MUST match TOML conditions
If a clothing item has `conditions = {corruption = 85}` in TOML, the shop
UI tier label must show "Bold (Corruption 85+)". Mismatch = confusing UX.

### Garment stats: `beauty` and `corruption` (optional, default 0)
Each `[[clothing]]` item may declare two numeric stats:

| Field | Type | Default | Meaning |
|-------|------|---------|---------|
| `beauty` | int | 0 | How attractive the garment is. |
| `corruption` | int | 0 | How revealing/lewd the garment is. |

```toml
[[clothing]]
id = "sundress_short"
name = "Short Sundress"
slot = "dress"
price = 40
beauty = 3
corruption = 12
```

**The worn outfit exposes a MAX aggregate, not a sum.** `worn_beauty` /
`worn_corruption` (see CONDITIONS SCHEMA) read the **highest** single equipped
garment's value — one daring piece drives content; layering does not inflate
the number.

**DOCTRINE — worn corruption is a SEPARATE axis.** Garment `corruption` ROUTES
content (which scenes/choices unlock); it NEVER mutates the player's global
`corruption` core_trait. The global meter stays the progression spine (it gates
shop tiers and story milestones). If you want sustained revealing wear to nudge
the global meter, do it deliberately via a `[engine.daily_tick]` rule — it is
never an automatic side effect of equipping.

**`[engine.daily_tick]` schema (day-rollover hook, fires once per `advanceDay()`):**
- `flagEffects` — array of `{ targetType, npcId?, flag, op }`. Silent flag
  clears/sets (the canonical use: clearing `*_today` cooldown flags).
- `traitEffects` (doc 40) — array of `{ targetType, npcId?, trait, op, value,
  clamp?, cap? }`. Applies a trait delta each day via `applyAndNotifyTrait`, so
  `clamp`/`cap` behave exactly like choice/canvas effects. This is how a stat
  ACCUMULATES over time without per-canvas wiring — the RTS-style arousal
  "daily auto-rise" (`player arousal +1 cap 10`, `npc arousal +1 cap 3`). A trait
  left out of every `trait_decay` config and given a daily `traitEffects` bump
  is a pure no-decay, always-climbing meter. Back-compat: omit `traitEffects`
  and the day-rollover is unchanged.
- `conditions` (doc 45 G6) — OPTIONAL on any flag- or trait-effect entry. A
  standard `{ version, logic, items }` condition block. When present, that
  effect applies on day rollover ONLY if the conditions are satisfied (e.g.
  `player arousal +1` gated on `corruption gte 20`). Omit ⇒ unconditional
  (today's behavior).

### Phone System

A diegetic smartphone opened from a sidebar button (a modal overlay; not a
passage). Apps render conditionally, so the launcher grows with progress.
Enable with a top-level `[phone]` table: `enabled = true` + `[[phone.apps]]`
(each `{ id, type, label, icon? }`; `type` ∈ `chat`, `social_feed`, `dating`
— `gallery`/`custom` are placeholders).

- **`[[phone.conversations]]`** — scripted, condition-triggered threads.
  `{ id, app, npc, trigger, notify? }` + ordered `[[…blocks]]`. A block is
  `type = "message"` (`sender = "npc"|"player"`, `content`) or
  `type = "reply"` (`round` + `choices`, each choice `{ text, effects[],
  flagEffects[] }` — same primitives as canvas choices). Branch with
  `after_round` / `after_choice`. `notify` (doc 45 G1) = toast text shown when
  the thread is first delivered (empty ⇒ "📱 New message").
- **`[[phone.daily_topics]]`** — repeatable chat. `{ id, npc, player_message,
  npc_response, effects[], conditions }`. Default cadence is 1 chat per NPC per
  day. Doc 45 G3 photo-action extensions (all optional): `image` (renders a
  sent-photo bubble), `corruption_min` (locks with 🔒 + note below the
  threshold), `cooldown = "per_topic"` (gives the topic its OWN once-per-day
  cap so several photo actions can each fire daily; default keeps the legacy
  per-NPC cap).
- **`[[phone.posts]]`** — read-only social feed. `{ id, app, npc?|poster_name,
  image, caption, likes, trigger, notify? }`. `notify` (G1) ⇒ delivery toast
  (default "📱 New post").
- **`[[phone.profiles]]`** — dating swipe. `{ id, app, npc, photos, bio, age,
  interests, trigger, match_condition }`. Like → if `match_condition` holds, a
  match.

Delivery: triggers are evaluated every passage render; a newly-satisfied
conversation/post bumps the unread badge and (G1) fires a toast.

- **`social_feed` posting** (doc 45 G2) — give a `social_feed` app a
  `post_actions` list, each `{ label, corruption_min?, followers_min,
  followers_max, daily_cap?(=1), counter_trait(="followers") }`. Renders post
  buttons gated by corruption (🔒 below `corruption_min`) + a per-action daily
  cap; posting adds `random(min,max)` to the `counter_trait`. Author the
  `followers` trait as a normal `core_trait`; **milestone DMs are free** — a
  conversation `trigger` on `{type:"trait", trait_key:"followers", operator:"gte", value:N}`.
- **`quests` app** (doc 45 G4) — an app of `type="quests"` renders the journal.

### Quests (doc 45 G4)

Story objectives with ordered steps. Define `[[quests]]`:
`{ id, name, steps:[<journal text per step>], repeatable?(=false) }`. State lives
in `$game_state.quests[id] = {active, progress, completed}`.

Mutate via **`questEffects` on any choice** (canvas or chat reply):
`[{ quest, op:"start"|"update"|"cancel"|"complete", step? }]` (`update` sets the
step, or +1 if omitted). Gate content with the **`quest` condition**:
`{ type="quest", quest_id, operator="active"|"completed"|"step_gte", value? }`.

### Scheduled / delayed events (doc 45 G5)

Fire something N days later via **`scheduleEffects` on any choice**:
`[{ delayDays, action:"set_flag"|"start_quest"|"trigger_conversation", flag?/quest?/conversation? }]`.
The queue (`$game_state.scheduled`) is decremented on each day rollover; at 0 the
action fires once (`set_flag` sets the flag; `start_quest` starts it;
`trigger_conversation` sets a `scheduled_<id>` flag a conversation can trigger on).

### Corruption tiers (doc 45 G7)

A discrete corruption LEVEL (0–4) derived from raw `corruption` points via
thresholds (default `[0,5,15,30,45]`; override with `[engine].corruption_tiers`).
Gate on it: `{ type="corruption_level", operator="gte"|"lt"|"eq", value }`
(e.g. `corruption_level gte 3` ⇔ points ≥ 30).

### More phone apps (doc 45 Tier 3)

- **`gallery`** — `[[phone.gallery_items]]` `{ id, image, caption?, trigger?, link? }`.
  Shows trigger-satisfied images; `link` makes a cell clickable → `Engine.play(link)`.
- **`custom`** — an app with a `passage` field renders that authored passage
  *inside* the phone frame (for bespoke mini-apps / webcam screens).
- **`quests`** — the quest journal (doc 45 G4).
- **In-world purchase** — `[phone].purchase_flag = "<flag>"` hides the sidebar
  phone button until that player flag is set (acquire the phone in-world; pair
  with a normal `flagEffects`/cost on a "buy" choice).
- **`fast_jobs`** — top-level `[[fast_jobs]]` `{ id, name, income, xp_req?,
  cooldown_days?, time_period?, money_trait?(="money") }` + a `fast_jobs` app.
  "Work" pays `income`, +1 fast-jobs XP, sets the cooldown (decremented daily);
  XP gates higher jobs.
- **`bank`** — `[bank]` `{ enabled, interest_rate(=0.01), money_trait(="money") }`
  + a `bank` app. Deposit/withdraw between cash and balance; balance accrues
  daily interest on the day tick.

### Recipe — RTS PornCenter & xCam (doc 45 G10)

No dedicated engine: build them from the primitives above.
- **PornCenter** = a `gallery` app whose items are `corruption_level`-gated
  (genre tiers) with a `link` to a content passage.
- **xCam** = a `custom` app whose `passage` is an authored webcam scene, with the
  whole phone gated by `purchase_flag` (e.g. a `webcam` flag) + a corruption gate.

### Recurring Passes

Time-limited purchases that gate activities. Defined in `[[passes]]`:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | — | Unique identifier |
| `name` | string | Yes | — | Display name |
| `cost` | int | Yes | — | Price in dollars |
| `duration_days` | int | No | 30 | Days until expiry |
| `icon` | string | No | "" | Sidebar emoji |

Purchase via `passEffects` on choices. Gate activities with `{ type = "pass", pass_id = "...", operator = "is_active" }`.

Sidebar `type = "passes"` shows active passes with days remaining.

### Consumable Items (Inventory)

Stackable items the player can buy and consume. Defined in `[[items]]`:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | — | Unique identifier |
| `name` | string | Yes | — | Display name |
| `icon` | string | No | "" | Sidebar emoji |
| `max_stack` | int | No | 99 | Max quantity |

Add/remove via `itemEffects` on choices. Gate activities with `{ type = "item", item_id = "...", operator = "gte", value = 3 }`.

Sidebar `type = "inventory"` shows items with counts.

### Location-Based Clothing Rules

Per-location clothing requirements replace global `body_coverage`. Set `body_coverage = false` in settings, then add `clothing_rules` to locations that require clothing.

Rules are ordered — first rule whose conditions pass determines the requirement. Locations without `clothing_rules` have no restriction.

```toml
clothing_rules = [
  { slots_required = ["top", "bottom"], conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 80 }
  ] } },
  { slots_required = ["bra", "underwear", "top", "bottom"],
    message = "You need to get dressed first." }
]
```

===============================================================================
                    DRAMATIC SPINE
===============================================================================

Every game needs a STORY, not just a progression system. Stats and gates
handle escalation — the dramatic spine handles WHY the player cares.

## THE ESCALATION-TENSION WAVE

Sexual escalation must alternate with dramatic tension. The pattern:

  ESCALATION → TENSION → BREAKTHROUGH → ESCALATION → CRISIS → ...

If the relationship only goes UP, it's a stat grind. If trust never breaks,
it was never real. The drama lives in the valleys between peaks.

EXAMPLE WAVE (mapped to gates):

  Day 1-3:  ARRIVAL + ROUTINE — domestic warmth, polite distance
  Day 3-5:  PEEK MOMENT — first spark (sets peek_unlocked)
  Day 5-7:  TENSION — something threatens the new closeness
            (She discovers he was watching. A boundary gets crossed.
             External pressure arrives. She pulls away.)
  Day 7-9:  REPAIR — player must actively fix what broke
  Day 8-10: FIRST KISS — earned through recovery (sets kiss_unlocked)
  Day 10-13: CRISIS — the biggest threat to the relationship
             (Not "she's distant for 2 days" — a real risk of losing her.
              Father calls. She almost kicks him out. A secret surfaces.
              She sees him with someone else. He sees something he shouldn't.)
  Day 13-16: RECOVERY ARC — multiple events to rebuild (not one magic scene)
  Day 15-18: DEEPER INTIMACY — trust rebuilt stronger (sets groping/oral)
  Day 18-22: CHOICE POINT — player must sacrifice something real
             (Money, safety, pride, another relationship, a secret)
  Day 22-25: TURNING POINT — the relationship transforms (sets sex_unlocked)
  Day 25-30: RESOLUTION — aftermath, what they've become

Tension/crisis events are NOT optional. Every game needs at least
2-3 genuine tension/crisis moments between the gates.

## CONFLICT TYPES

Every game needs at least ONE primary source of conflict:

EXTERNAL THREAT:
  Someone/something threatens the relationship
  (ex returns, family member discovers, landlord, friend warns,
   financial crisis forces a move)

INTERNAL CRISIS:
  The NPC's own psychology fights the relationship
  (guilt, self-sabotage, fear of abandonment,
   "what kind of person does this make me?")

BOUNDARY BREAK:
  The player crosses a line (or is perceived to)
  (caught watching, lie exposed, trust violated, pushing too fast)

COMPETING PULL:
  Someone else enters the picture
  (rival, NPC's ex, secondary NPC complication,
   job opportunity in another city)

REVELATION:
  Something hidden is exposed
  (a secret about the past, a lie unravels,
   player discovers something about the NPC,
   NPC discovers something about the player)

RECOMMENDED: Use 2 conflict types. One in Act 1 (smaller), one in Act 2 (major).

## CONSEQUENCE MECHANICS

Stat regression makes drama feel real. The engine supports negative effects.

WHEN STATS SHOULD DROP:
- NPC discovers player crossed a boundary → trust drops (-3 to -8)
- NPC has an internal crisis (guilt, fear) → primary stat drops (-2 to -5)
- Player makes a selfish choice → trust and/or primary stat drop
- External event destabilizes the relationship → temporary stat drop

HOW REGRESSION WORKS IN THE WAVE:
- Stats drop during TENSION/CRISIS events (one-time story canvases)
- Player rebuilds through activities + repair events in the days that follow
- The rebuild should take 2-4 in-game days (not one scene)
- Rebuilt stats should slightly exceed pre-crisis levels (net positive)
- This creates the feeling: "We almost lost this. Now it means more."

REGRESSION RULES:
- NEVER drop stats below a previously passed gate threshold
  (if kiss_unlocked at love 25, don't drop love below 25)
- NEVER un-set a gate flag (kiss_unlocked stays true forever)
- Drop the PRIMARY stat or trust, not both at once
- Maximum single-event regression: -8 primary stat OR -5 trust
- After a drop, the next 2-3 activities should give +1 extra to compensate

## MEANINGFUL CHOICES

Choices must have DIFFERENT CONSEQUENCES, not just different stat bonuses.

BAD CHOICES (avoid these):
  "Be nice to her"   → +3 love, +2 trust
  "Be polite to her"  → +2 love, +1 trust
  (Both go the same direction. Player always picks the higher one.)

GOOD CHOICES (design these):
  "Tell her the truth" → +5 trust, -3 love (she respects honesty but it hurts)
  "Protect her feelings" → +2 love, -0 trust (she's happy but you carry the lie)
  (Genuine trade-off. Player must decide what matters more.)

CHOICE CATEGORIES:

1. TRADE-OFF: One stat goes up, another goes down
   "Comfort her" (love +3) vs "Give her space" (trust +3)

2. SHORT vs LONG TERM: Immediate gain vs future payoff
   "Kiss her now" (love +4, but she panics — crisis event triggers sooner)
   "Wait for her to come to you" (love +1, but skip the crisis entirely)

3. SACRIFICE: Player gives something up
   "Spend savings on her" (money -200, love +5, trust +3)
   "Keep the money" (money safe, love +0, trust -1)

4. MORAL: No clear right answer
   "Tell her you saw her" (trust +4, love -2, peek_unlocked stays)
   "Keep it secret" (trust -0, love +1, but lie_flag set → crisis later)

5. EXCLUSIVE PATHS: Opens one branch, closes another
   "Go to the cafe" → meet secondary NPC (opens subplot)
   "Stay home with her" → deeper conversation (opens different subplot)

REQUIREMENT: At least 3 story events must have TRADE-OFF or SACRIFICE choices.
At least 1 story event must have a choice with NEGATIVE stat consequences.

---

===============================================================================
                    NPC EMOTIONAL FLOW
===============================================================================

NPC behavior isn't driven by a single stat — it's the COMBINATION of the
primary stat and trust that determines how she acts in every scene.

## THE EMOTIONAL QUADRANT

The NPC's behavior at any moment is defined by the intersection of TWO axes:

                        TRUST HIGH
                            |
              SAFE          |         OPEN
         "Comfortable"      |      "Vulnerable"
         She's relaxed,     |    She's relaxed AND
         trusts him, but    |    attracted. Warmth,
         no romantic pull.  |    eye contact, lingering
         Platonic warmth.   |    touches. Real intimacy.
                            |
  PRIMARY LOW ──────────────+────────────── PRIMARY HIGH
                            |
              DISTANT        |        CONFLICTED
           "Transactional"   |      "Drawn but Guarded"
          Polite, surface.   |    She WANTS him but
          Roommate energy.   |    doesn't trust him (yet,
          Nothing personal.  |    or anymore). The most
          Functional.        |    dramatically rich state.
                            |
                        TRUST LOW

QUADRANT BEHAVIORS — These should guide ALL scene writing:

DISTANT (low primary / low trust):
  - Short sentences, minimal eye contact
  - Leaves the room when he enters
  - Functional dialogue only: "Coffee's ready." (walks away)
  - Physically closed: arms crossed, back turned, door shut
  - No initiative — she never starts conversations

SAFE (low primary / high trust):
  - Warm but platonic — she treats him like family
  - Comfortable sharing space, no tension
  - Open dialogue about life, work, memories
  - Physically relaxed but not charged: sits near, no spark
  - She initiates practical things: "Dinner?" "Need a ride?"

CONFLICTED (high primary / low trust):
  - The most interesting state — attraction WITHOUT trust
  - She's drawn to him but fighting it or recovering from a breach
  - Mixed signals: warm eyes but physical distance
  - Starts to speak, stops herself. Looks away first.
  - Dialogue contradicts behavior: "I'm fine" (she's not)
  - She watches him when he's not looking, averts when caught
  - Physically tense near him — hands grip mug tighter,
    shifts weight, touches her own neck/hair (self-soothing)
  - May snap or lash out, then immediately regret it
  - This is POST-CRISIS state: she wants to come back but
    hasn't decided it's safe yet

OPEN (high primary / high trust):
  - Full emotional + physical availability
  - Sustained eye contact, gravitates toward him
  - Dialogue is honest, vulnerable, sometimes playful
  - Physical initiative: she touches first, stands close
  - Comfortable silence — doesn't need to fill space
  - She references shared history: "Remember when..."
  - Laughter is different — unguarded, genuine
  - She makes plans that include him: "We should..." "Next
    weekend let's..."

## EMOTIONAL TRANSITIONS

The NPC doesn't jump between quadrants — she transitions through them.
Each transition has a characteristic emotional texture:

DISTANT → SAFE (trust builds without attraction):
  Gradual. She starts asking personal questions. Leaves the door open
  when she's in a room. Saves him a plate. Small, consistent kindnesses
  that signal: "I'm getting used to you being here."

DISTANT → CONFLICTED (attraction builds without trust):
  Uncommon early, but can happen. She's physically aware of him but
  hasn't decided if that's dangerous. She overcompensates with distance:
  too-casual voice, too-structured boundaries. The tension is visible.

SAFE → OPEN (trust enables attraction to surface):
  The most natural progression. She trusts him, then starts NOTICING
  him. The transition moment is when something platonic becomes charged:
  a hand that lingers, a look that holds too long, a laugh that turns
  into silence that turns into awareness.

CONFLICTED → OPEN (trust rebuilds alongside attraction):
  The most EARNED transition — this is the crisis recovery arc.
  She wants him AND trusts him again. The "open" state after a crisis
  feels DEEPER than "open" before a crisis, because she chose it
  despite the risk. Dialogue reflects this: "I was so scared of this.
  I'm not scared anymore."

OPEN → CONFLICTED (trust breaks while attraction remains):
  This IS the crisis. The most dramatic transition. She still wants
  him — maybe more than ever — but something shattered her trust.
  The pain comes from wanting someone you can't trust. Write this as
  anger mixed with longing: "Don't look at me like that. Not now."

SAFE → DISTANT (trust breaks without attraction):
  Rare in the main storyline. Happens if player badly mishandles
  early events before any romantic tension develops. She shuts down
  and goes back to roommate-mode. Recovery is slower because there's
  no attraction pulling her back.

## EMOTIONAL FLOW THROUGH THE GAME

Map the NPC's quadrant journey alongside the gate progression:

| Game Phase       | Primary | Trust  | Quadrant     | Gate          |
|------------------|---------|--------|--------------|---------------|
| Day 1-3          | 0-10    | 0-5    | DISTANT      | (none)        |
| Day 3-5          | 10-20   | 5-10   | SAFE→edge    | peek_unlocked |
| Day 5-7          | 15-25   | 8-12   | edge→OPEN    | —             |
| Day 7-8 TENSION  | 20-25   | DROP   | CONFLICTED   | (tension)     |
| Day 8-10         | 25-35   | REBUILD| recovery→OPEN| kiss_unlocked |
| Day 10-14        | 35-50   | 16-22  | OPEN         | groping_unlck |
| Day 14-16 CRISIS | 45-55   | DROP   | CONFLICTED   | (major crisis)|
| Day 16-19        | 50-60   | REBUILD| recovery     | —             |
| Day 19-22        | 60-75   | 24-30  | DEEP OPEN    | oral_unlocked |
| Day 22-25        | 75-90   | 30-40  | DEEP OPEN    | sex_unlocked  |
| Day 25-30        | 90-100  | 40-50  | COMPLETE     | (resolution)  |

KEY INSIGHT: The journey through CONFLICTED → OPEN is the most emotionally
satisfying part of the game. Don't skip it. Don't resolve it too fast.
The player should FEEL the NPC's conflict through 2-4 days of changed behavior
before the repair event fires.

## EMOTIONAL STATE IN SCENE WRITING

When writing ANY scene (activity or story event), the NPC's emotional
quadrant should be visible through:

1. BODY LANGUAGE (physical position relative to the player)
   - DISTANT: Opposite side of room, faces away, door between them
   - SAFE: Same room, comfortable distance, side-by-side
   - CONFLICTED: Same room but tense — perched, ready to leave, fidgeting
   - OPEN: Close, gravitating toward him, relaxed posture, leaning in

2. EYE CONTACT (the most reliable emotional indicator)
   - DISTANT: Avoids eye contact, looks at objects, looks down
   - SAFE: Easy, casual eye contact — like talking to a friend
   - CONFLICTED: Quick glances then away, caught looking, eyes dart
   - OPEN: Holds eye contact, searches his face, looks then smiles

3. DIALOGUE PATTERN (how she speaks, not just what she says)
   - DISTANT: Short. Functional. "Coffee's ready." "Goodnight."
   - SAFE: Conversational. "How was work?" Asks follow-up questions.
   - CONFLICTED: Starts and stops. "I wanted to— never mind." Says one
     thing, means another. Long pauses.
   - OPEN: Full sentences. Vulnerable. "I keep thinking about..." Shares
     without prompting.

4. INITIATIVE (who starts the interaction)
   - DISTANT: Never. Player must approach. She responds minimally.
   - SAFE: Sometimes. She'll call him for dinner or mention a movie.
   - CONFLICTED: Indirect. She's in his path "by accident." Creates
     situations where they'll cross paths but doesn't initiate directly.
   - OPEN: Often. She comes to find him. "I was looking for you."
     Makes excuses to be in his space.

5. TOUCH (physical contact and proxemics)
   - DISTANT: None. Pulls hand away if accidental. Maintains buffer.
   - SAFE: Casual, brief — pats shoulder, hands a plate, hip-bumps
     in kitchen. Friendly. Zero charge.
   - CONFLICTED: Accidental touches that freeze both of them. She doesn't
     pull away but doesn't lean in. Electric, unresolved.
   - OPEN: Deliberate. Hand on arm while talking. Sits close enough that
     legs touch. Brushes hair from his face. Lingering.

6. PLAYER INTERNAL VOICE (how the player character experiences the moment)
   The player is not a camera. He has his own emotional response to the scene.
   His internal voice should reflect his current PHASE:

   - OUTSIDER: Observational, detached. "The kitchen smells like coffee.
     She doesn't look up when I come in."
   - SETTLING: Noticing patterns. "She always hums when she cooks.
     I've started listening for it."
   - WANTING: Charged awareness. "Her hand brushed mine reaching for the
     salt. Neither of us mentioned it."
   - TORN: Conflicted narration. "I should say something. I should
     definitely not say something."
   - COMMITTED: Emotionally honest. "I watched her sleep for a moment
     before I got up. I didn't used to do that."
   - BELONGING: Settled, intimate. "She left me a note on the counter.
     Just 'Good morning.' It was enough."

### TWO-PERSPECTIVE SCENE WRITING

Every scene has two emotional layers — the NPC's quadrant behavior AND the
player's phase experience. Write BOTH, not just the NPC's side.

Example — same NPC action at different player phases:

NPC action: Angela laughs at your joke during breakfast (NPC quadrant: SAFE)

  OUTSIDER phase: "She laughed — a real one, not polite. Maybe this
  place won't be so bad."
  (Player is observing. The laugh is data about his new environment.)

  WANTING phase: "The way her eyes crinkle when she laughs. You realize
  you've been trying to make that happen all week."
  (Player is invested. The laugh is something he's pursuing.)

  COMMITTED phase: "She laughed, and you felt it in your chest. When did
  her happiness start feeling like yours?"
  (Player is emotionally entangled. The laugh is shared joy.)

The NPC's behavior stays the same (SAFE quadrant laugh). What changes is
the PLAYER'S experience of it. This is what makes the story feel like
it's progressing even in repeated activity scenes.

## CRISIS EMOTIONAL FLOW (DETAILED)

The most important emotional sequence in the game is the crisis arc.
Write it as a 5-stage emotional journey for the NPC:

STAGE 1: THE SHOCK (crisis event itself)
  Quadrant: Abrupt shift from OPEN → CONFLICTED
  Duration: The scene itself
  NPC emotional state: Hurt, confused, reactive
  Key behavior: She says something she means but wishes she didn't
  Sample line: "How long has this been going on?"
  Sample line: "I need you to leave the room. Right now."

STAGE 2: THE WALL (Day 1-2 after crisis)
  Quadrant: Deep CONFLICTED
  Duration: 1-2 in-game days
  NPC emotional state: Self-protective, cold, processing
  Key behavior: She's present but unreachable. Bare minimum interaction.
  Activity base scenes during this stage:
  - Breakfast: "She's already eaten. Your plate is in the microwave."
  - Movie night: Doesn't happen. Living room is dark when you enter.
  - Chores: She doesn't comment when you clean. She used to.
  Sample line (if forced to interact): "I said I'm fine."

STAGE 3: THE CRACK (Day 2-3 after crisis)
  Quadrant: CONFLICTED softening
  Duration: 1 day transition
  NPC emotional state: The wall is exhausting. She misses him.
  Key behavior: Small involuntary warmths leak through the coldness.
  She's fighting herself — the contradiction from Phase 2 is loudest here.
  Activity base scenes during this stage:
  - Breakfast: She's there. Doesn't speak first. But she made his coffee.
  - Evening: She's on the couch. Doesn't invite him. Doesn't ask him to leave.
  Sample line: "Do you want..." (pauses) "...there's food in the fridge."

STAGE 4: THE CONVERSATION (repair event)
  Quadrant: CONFLICTED → transitioning
  Duration: One scene
  NPC emotional state: Vulnerable, exhausted, honest
  Key behavior: She says what she's actually feeling for the first time
  since the crisis. No performance, no wall, no pretense.
  This is where the NPC's internal contradictions surface in dialogue.
  She names her fear: "I'm scared because..."
  She names her want: "But I don't want to..."
  Sample line: "I don't know how to be angry at you and miss you at the
  same time."

STAGE 5: THE RETURN (resolution event)
  Quadrant: CONFLICTED → OPEN (deeper than before)
  Duration: One scene + new baseline
  NPC emotional state: Resolved. She chose this despite the risk.
  Key behavior: The first touch after the crisis. It carries weight.
  She's softer than before — not because the crisis didn't happen,
  but because surviving it together proved something.
  Activity base scenes AFTER this stage:
  - Breakfast: "She sits across from you. Holds your gaze a beat longer
    than she used to. Something is different — not just forgiven. Settled."
  Sample line: "I don't want to go back to how it was before. Any of it."

### PLAYER CRISIS ARC (PARALLEL)

While the NPC goes through her 5 stages, the PLAYER has his own emotional
journey. These run in PARALLEL — both are happening at the same time:

| Stage | NPC Experience | Player Experience |
|-------|---------------|-------------------|
| SHOCK | Hurt, reactive, says something sharp | GUILT — "What have I done?" Wants to fix it immediately. |
| WALL | Cold, unreachable, bare minimum | HELPLESSNESS — Can't fix it. Every attempt bounces off. Starts questioning everything. |
| CRACK | Small warmths leak through | RESOLVE — Sees the crack. Decides he'll wait as long as it takes. Stops trying to force repair. |
| CONVERSATION | Vulnerable, honest, names fears | VULNERABILITY — Matches her honesty. Says what he's actually afraid of losing. |
| RETURN | Chooses him despite the risk | CERTAINTY — "I'm not going anywhere." The relationship is no longer casual to him. |

Activity scenes during crisis should show BOTH perspectives:

BREAKFAST (during WALL stage):
  NPC layer: "She's already eaten. Your plate is in the microwave."
  Player layer: "You eat alone. The kitchen feels bigger than it used to."

BREAKFAST (during CRACK stage):
  NPC layer: "She's there. Doesn't speak first. But she made his coffee."
  Player layer: "She made your coffee. You wrap both hands around the mug
  and don't say thank you — you both know what it means."

===============================================================================
                    PLAYER EMOTIONAL ARC
===============================================================================

The player character is NOT a blank camera. He has his own emotional journey
that runs alongside the NPC's quadrant transitions. While the NPC's emotional
state is driven by stat combinations, the player's emotional state is driven
by STORY PROGRESSION — which phase of the relationship he's in.

## PLAYER EMOTIONAL PHASES

| Phase | Trigger | Player Mindset | What He Notices | How He Describes NPC |
|-------|---------|---------------|-----------------|---------------------|
| OUTSIDER | Arrival | "I don't belong here" | Environment, layout, rules | Physical appearance, surface traits |
| SETTLING | First friendly interaction | "This might be okay" | Routines, NPC habits, patterns | Personality quirks, small details |
| WANTING | First spark / attraction event | "I want more of this" | NPC's body, proximity, charged moments | Physical attraction, what draws him |
| TORN | After tension or near-crisis | "I could lose this" | What he'd miss, stakes | Emotional depth, vulnerability |
| COMMITTED | After major crisis recovery | "I choose this" | The relationship itself, shared history | Partnership, intimacy, trust |
| BELONGING | Resolution / final act | "This is home" | Small moments, quiet details | Familiar, intimate, known |

## PHASES vs NPC QUADRANTS

These are INDEPENDENT systems that interact:
- NPC quadrant = how SHE behaves (driven by stats)
- Player phase = how HE experiences it (driven by story events)

The most powerful moments happen when they're OUT OF SYNC:
- Player in WANTING + NPC in CONFLICTED = painful longing
- Player in TORN + NPC in OPEN = he can't believe his luck
- Player in COMMITTED + NPC in CONFLICTED (crisis) = desperate determination

## PLAYER GROWTH VISIBLE IN NARRATION

The game's narration should subtly evolve as the player progresses through phases:

1. SENTENCE LENGTH
   - OUTSIDER: Short, observational. "The house is quiet. My room is upstairs."
   - BELONGING: Flowing, reflective. "The house has a way of settling in the
     evening — the floorboards, the fridge humming, her voice from the other room."

2. EMOTIONAL VOCABULARY
   - OUTSIDER: Basic, external. "Nice." "Awkward." "Fine."
   - BELONGING: Specific, internal. "Grateful." "Terrified." "Certain."

3. NPC REFERENCES
   - OUTSIDER: Full name or role. "Angela." "My landlord."
   - SETTLING: Name only. "Angela."
   - WANTING: Possessive hints. "Her laugh." "The way she..."
   - BELONGING: Intimate shorthand. "She." (no need to name — who else?)

4. DETAIL SPECIFICITY
   - OUTSIDER: Generic. "She was wearing a dress."
   - BELONGING: Intimate. "She was wearing the blue one — the one from
     the night we sat on the porch until 2am."

---

===============================================================================
                    REFERENCE PATTERNS
===============================================================================

These patterns are drawn from the reference game (Jack's World). Use them
as templates when designing activities and events.

---

## PATTERN A: STANDARD ESCALATING ACTIVITY
Example: Breakfast Together (kitchen, 07:00-09:00)

Structure: Single canvas. Base node always plays with domestic scene.
First node exit_block offers CHOICES — new choices appear as stats/flags grow.

  NODE 1 (base — always shown):
    Content: Morning scene, coffee, domestic warmth
    Videos: 3-5 clips showing the routine moment
    Choices:
      [always]            "Eat together"      → exit, +1 love, +1 trust
      [love >= 22]        "Stand closer"      → warm node
      [love >= 42 + kiss] "Kiss her"          → kiss node
      [love >= 62 + grope]"Get closer"        → foreplay node
      [love >= 82 + oral] "Pull her close"    → intimate node

  NODE 2 (warm — stat threshold only):
    Content: Physical closeness, embrace from behind, tenderness
    Videos: 1-2 clips of innocent intimacy
    Exit choices: Both exit the canvas with +2 love

  NODE 3 (kiss — stat + kiss_unlocked):
    Content: Passionate kissing, escalating touch
    Videos: 2 clips of kissing, neck/collarbone
    Exit choices: Both exit canvas with +2 love

  NODE 4 (foreplay — stat + groping_unlocked):
    Content: Hands under clothes, groping, oral teasing
    Videos: 2 clips of foreplay
    Exit choices: Both exit canvas with +2 love

  NODE 5 (intimate — stat + oral_unlocked):
    Content: Oral sex, full intimate encounter
    Videos: 2 clips of oral
    Exit choices: Both exit canvas with +2 love

KEY: The player ALWAYS sees the base scene. Escalation is their CHOICE.
Each escalation node has: setup paragraph → video(s) → reaction → dialog → exit.

---

## PATTERN B: DUAL-PATH ACTIVITY
Example: Angela's Bath (bathroom, 19:00-20:00)

Structure: Single canvas. Base node presents 2+ fundamentally different paths.

  NODE 0 (approach — base):
    Content: Door is ajar, steam, glimpse through the gap
    Videos: 2 clips of her getting into the bath
    Choices:
      [always]                        "Leave quietly"    → exit, +1 love
      [peek_unlocked]                 "Watch from door"  → peek path
      [oral + love >= 65 + days >= 1] "Join her"         → participate path

  PEEK PATH (voyeur — linear chain, no internal gating):
    peek_routine → peek_intimate → peek_private → exit
    Player watches without her knowledge
    Each node: paragraph → videos → paragraph
    Final exit: "Slip away" → exit, +1 love

  PARTICIPATE PATH (consensual — with internal gating):
    bath_self_care → bath_together → [sex_unlocked?] → bath_sex → exit
    Higher requirements, higher rewards
    Internal gate at sex content: requires sex_unlocked + love >= 82
    Exit: +3-5 love, +2-3 trust

KEY: Two completely different narrative experiences from the same canvas.
Voyeur path builds anticipation. Participate path delivers on it later.

---

## PATTERN C: UTILITY CANVAS — CHORE
Example: Wash Dishes (kitchen, 09:00-14:00)

Structure: Single canvas, single node, single exit.

  NODE 1:
    Content: Brief narrative (2-3 sentences)
    No video needed
    Exit: "Finish up" → exit, +1 trust, 30 minutes

Trigger conditions: `chores_explained` flag (set by story event)
Repeatable, priority 1, max 1 per day

---

## PATTERN D: UTILITY CANVAS — JOB
Example: Cafe Shift (cafe, 07:00-12:00 or 14:00-17:00)

Structure: Single canvas, single node, exit with money + trust.

  NODE 1:
    Content: Brief work narrative (3-4 sentences)
    Optional: 1 dialog line from secondary NPC (cafe owner)
    Exit: "Finish shift" → exit, +$70 money, +1 trust, 180 minutes

Trigger conditions: `job_started` flag
Repeatable, priority 1, max 2 per day (morning + afternoon shifts)

---

## PATTERN E: TIME-ADVANCEMENT CANVAS
Example: Jack's Room (bedroom, always available)

Structure: Single canvas, single node, choices advance time differently.

  NODE 1:
    Content: Brief narrative about the room
    Choices:
      "Rest for a bit"  → exit, 120 minutes (2 hours)
      "Go to sleep"     → exit, 540 minutes (9 hours)

No NPC, no conditions, no stat effects. Purely a time control mechanism.
Essential for allowing the player to advance to the next activity window.

---

## PATTERN F: STORY EVENT
Example: First Kiss (living room, evening)

Structure: One-time canvas, priority 10, multiple narrative nodes.

  Trigger: towel_encounter_complete AND love >= 25
  Schedule: 19:00-22:00
  is_repeatable: false
  priority: 10

  NODE 1 (setup):
    Content: Emotional setup, building moment
    Videos: Optional establishing shots
    Exit: "Continue" → node 2

  NODE 2 (climax):
    Content: The kiss, detailed and tender
    Videos: 2 clips — gentle kiss, deepening
    Exit choices:
      "Kiss her gently"  → node 3, +2 love, +1 trust
      "Pull her close"   → node 3, +3 love

  NODE 3 (aftermath):
    Content: Emotional processing, what it means
    Exit: "Walk her home" → exit, sets `first_kiss_complete`

KEY: Both choices set the SAME flag. Player progresses regardless of choice,
but different stat outcomes reward different playstyles.

---

## PATTERN G: GATE-SETTING EVENT
Example: Massage Offer (bedroom, evening)

Structure: Story event that sets a content gate flag.

  Trigger: first_kiss_complete AND days_since_flag(first_kiss_complete) >= 2
           AND love >= 40 AND trust >= 18
  Sets: kiss_unlocked (AND possibly groping_unlocked)

The `days_since_flag >= 2` creates a natural gap — the player experiences
2+ days of the relationship AFTER the first kiss before this event fires.
This prevents narrative compression and lets activities play at the
post-kiss level before the next escalation.

After this event, ALL NPC activities show their kiss-gated choices.

---

## PATTERN H: ECONOMIC EVENT
Example: Weekly Rent (kitchen, any time)

Structure: Recurring canvas with `days_since_flag` timer.

  Trigger: first_rent_paid AND days_since_flag(rent_last_paid) >= 7
           AND money >= 200
  Priority: 2 (higher than activities, lower than story events)
  is_repeatable: true

  NODE 1:
    Content: Rent is due, brief exchange
    Exit: "Pay rent" → exit, -$200 money, +2-3 trust, sets rent_last_paid

The `days_since_flag` resets every time the player pays, creating a
weekly cycle. If the player can't afford it (money < 200), the canvas
doesn't trigger — creating economic pressure.

---

## PATTERN I: TENSION EVENT (Stat Regression)
Example: Caught Watching (bathroom, evening)

Structure: One-time canvas, priority 10. Stats DROP instead of rise.

  Trigger: peek_unlocked AND love >= 15 AND days_since_flag(peek_unlocked) >= 3
  Schedule: 19:00-22:00
  is_repeatable: false
  priority: 10

  NODE 1 (discovery):
    Content: The NPC discovers or confronts the player about something
    Videos: Optional — often more powerful as text-only
    Exit: "Continue" → node 2

  NODE 2 (confrontation):
    Content: The NPC's emotional reaction — NOT anger, but hurt
    Dialog: Lines that reveal vulnerability, not hostility
    NPC quadrant: Shifting from OPEN → CONFLICTED in real-time
    Exit choices:
      "Tell the truth"     → node 3a, trust -2, love +1
      "Make an excuse"     → node 3b, trust -5, love -2

  NODE 3a (honest path):
    Content: She's upset but respects the honesty
    Exit: → exit, sets `tension_event_complete`, trust -3 total

  NODE 3b (dishonest path):
    Content: She knows you're lying. It's worse.
    Exit: → exit, sets `tension_event_complete` + `lied_flag`, trust -5 total

KEY: The stat DROPS. Both paths result in loss, but one is significantly
less damaging. The `lied_flag` could trigger a harder crisis later.
Recovery happens over the next 2-3 days through regular activities.
NPC enters CONFLICTED quadrant during recovery period.

---

## PATTERN J: RECOVERY/REPAIR EVENT
Example: The Apology (kitchen, morning)

Structure: One-time canvas that resolves tension. Only triggers AFTER a
tension/crisis event, with a days_since_flag gap.

  Trigger: tension_event_complete AND days_since_flag(tension_event_complete) >= 2
           AND trust >= [pre-crisis threshold - drop amount]
  Schedule: 07:00-09:00
  is_repeatable: false
  priority: 10

  NODE 1 (approach):
    Content: The NPC is different — guarded, testing, watching
    NPC quadrant: CONFLICTED (softening)
    Exit: "Continue" → node 2

  NODE 2 (the conversation):
    Content: Real dialog about what happened. Not surface-level.
    The NPC's internal contradictions (from Phase 2) should surface here.
    Exit choices:
      "I was wrong. I'm sorry."  → node 3, trust +4, love +2
      "Can we just move past it?" → node 3, trust +1, love +1

  NODE 3 (resolution):
    Content: She softens. Not fully restored — but the door is open.
    The line that signals recovery:
      "I'm not ready to forget. But I'm not ready to lose you either."
    NPC quadrant: CONFLICTED → transitioning back toward OPEN
    Exit: → exit, sets `tension_resolved`

KEY: Recovery gives BACK more than was lost (net positive after the arc),
but only if the player took the vulnerable/honest path. Players who lied
or dismissed get less back and must work harder through activities.

---

## PATTERN K: BRIDGE EVENT (Non-Mechanical Character Moment)
Example: Power Outage (apartment, evening)

Structure: One-time canvas. No gate flag set. No mechanic unlocked.
Exists purely for character depth and relationship building.

  Trigger: [flag] AND [stat threshold] AND [timing]
  is_repeatable: false
  priority: 8 (below story events, above activities)

  NODE 1 (situation):
    Content: An unexpected shared experience
    (power outage, she's sick, he cooks for the first time,
     they find old photos, a thunderstorm, a neighbor needs help)

  NODE 2 (the moment):
    Content: Characters reveal something new about themselves
    Not romantic — just human. She laughs differently. He admits
    something embarrassing. They share a story from childhood.
    NPC emotional quadrant deepens within its current state.
    Exit choices — NOT stat-based, just character-based:
      "Tell her about your mom"  → love +2, trust +2
      "Ask about her life before" → love +1, trust +3

KEY: Bridge events are the glue between milestones. They make the
player think "I know this person" rather than "I unlocked this tier."
Design at least 2-3 per game, spread between Acts 1 and 2.
The NPC's emotional tells (from Phase 2) should be most visible here.

---

===============================================================================
                    PHASE 0: VIDEO LIBRARY INTEGRATION (OPTIONAL)
===============================================================================

This phase iteratively integrates video description files into the game design.
Each video file is processed one at a time with user approval.

## WHEN TO USE THIS PHASE

- User provides video description JSON files
- User wants to design around existing video assets
- Can be skipped if designing without pre-existing videos

## VIDEO DESCRIPTION JSON FORMAT

Video description files are generated by the asset pipeline and contain:

```json
{
  "video_id": "c7b16ed4-1504-4283-97d5-513306dea33c",
  "clips": [
    {
      "id": "42c1f739-89df-4196-874a-d57850d72817",
      "index": 1,
      "description": "A woman kneels in a kitchen..."
    }
  ]
}
```

CRITICAL: Always use the `id` field (UUID), NEVER the `index` number.
The UUID is the permanent identifier: book → TOML → database → game engine.
In TOML: `{ type = "clip", props = { clipId = "uuid-here" } }`

## VIDEO FILE ANALYSIS

For EACH video description file provided:

### Step 1: Load and Analyze

a) Count and classify clips:
   - Total clips in file
   - Usable clips (applying filtering logic)
   - Flagged/unusable clips

b) Identify settings/locations:
   - Kitchen, bedroom, living room, bathroom, etc.

c) Classify by sexual activity:
   - Oral (BJ, cunnilingus)
   - Penetration positions (doggy, missionary, cowgirl, etc.)
   - Manual (handjob, fingering)
   - Foreplay (groping, grinding, makeout)

d) Curate best clips:
   - Select 1-2 clips per sexual activity type
   - Prioritize variety in settings

### Step 2: Filtering Logic

```
USABILITY SCORING (5 point scale):

+5 Base score

DEDUCTIONS:
-2 if room_count > 2 (montage indicator)
-2 if word_count < 300 (incomplete description)
-1 if description doesn't end with . or ) or " (truncated)
-3 if matches intro/outro patterns:
   - title card/screen/sequence, credits, montage
   - opening credits/title/sequence, closing
   - behind the scenes

Score >= 4: USABLE
Score < 4: FLAGGED
```

### Step 3: Tier Classification

Classify clips by content level:

┌──────┬─────────────────────┬─────────────────────────────────────┐
│ Tier │ Content Level       │ Clip Indicators                     │
├──────┼─────────────────────┼─────────────────────────────────────┤
│ T1   │ Ambient (SFW)       │ Conversation, casual, no sexual     │
│ T2   │ Suggestive          │ Cleavage, lingering looks           │
│ T3   │ Teasing             │ Deliberate showing, flirty          │
│ T4   │ Groping/Kissing     │ Hands on body, making out           │
│ T5   │ Handjob/Fingering   │ Manual stimulation                  │
│ T6   │ Oral                │ Blowjob, cunnilingus                │
│ T7   │ First Penetration   │ Initial sex scene                   │
│ T8+  │ All Positions       │ Varied positions, multiple rounds   │
└──────┴─────────────────────┴─────────────────────────────────────┘

NOTE: Most video files are T4-T8+. T1-T3 typically need external sourcing.

### Step 3.5: Allocation Classification

After tier classification, classify clips for activities vs story:

STORY MILESTONE INDICATORS (reserve for one-time scenes):
─────────────────────────────────────────────────────────
• First-time energy — tentative, emotional, building anticipation
• Strong eye contact — intimate connection, meaningful gazes
• Narrative arc feel — beginning → buildup → climax progression
• Unique moments — special setting, position, or emotional quality
• Tender aftermath — post-sex intimacy, connection

These clips are WASTED on repeatable activities. Reserve for milestones.

ACTIVITY INDICATORS (use for repeatable content):
──────────────────────────────────────────────────
• Variety/position focus — showcasing the act itself
• "In the moment" energy — without narrative arc
• Loop-friendly — works on repeat viewing
• Action-focused — less emotional, more physical

ALLOCATION PRIORITY:
1. Identify "first-time" clips → allocate to story milestones
2. Identify position-variety clips → allocate to activity nodes
3. Remaining high-quality clips → mark as shared

### Step 4: Present Curated Proposal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO PROPOSAL: [filename]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANALYSIS SUMMARY:
  Total clips: [X]
  Usable clips: [Y] ([Z]%)
  Flagged: [A]

CURATED CONTENT:
  | Activity     | Clips | Settings             |
  |--------------|-------|----------------------|
  | Doggy        | 2     | bedroom, living room |
  | Missionary   | 2     | bedroom, kitchen     |
  | Cowgirl      | 1     | bedroom              |
  | Oral (BJ)    | 2     | kitchen, bedroom     |
  | ...          | ...   | ...                  |

CONTENT BY GATE:
  kiss_unlocked:    [X clips assigned]
  groping_unlocked: [X clips assigned]
  oral_unlocked:    [X clips assigned]
  sex_unlocked:     [X clips assigned]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 1: ACTIVITY PROPOSALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[A] SINGLE ACTIVITY — "[Name]"
    All clips form one escalating activity.

[B] MULTIPLE ACTIVITIES — By Location
    Separate activities for each setting.

[C] HYBRID — Main activity + unlockable content
    Core activity with additional nodes unlocked by story gates.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 2: STORY MILESTONE PROPOSALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Present 1-3 milestone proposals with first-time-energy clips]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 3: CLIP ALLOCATION TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| UUID (short) | Description | Tier | Allocation |
|--------------|-------------|------|------------|
| 42c1f739...  | Oral tender | T6   | Story      |
| f6a7b8c9...  | Cowgirl     | T8+  | Activity   |
| ...          | ...         | ...  | ...        |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Confirm All] [Modify] [Skip Video] [Save & Pause]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Step 5: Gap Handling

For tiers without video content, ask user per activity:
- Create with external source marker?
- Suggested description for sourcing

### Step 6: Integration Status

After each video, show coverage:
- Activities created with clip counts
- Story milestones with gate assignments
- Location coverage map
- Time slot coverage
- Suggested additions for gaps

### Step 7: Save Integration State

Update session_state.yaml with all integration data.

## SKIPPING PHASE 0

If user wants to proceed without video integration:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 0: VIDEO INTEGRATION (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No video description files provided.

[Provide Video Files] — Add video description JSON files
[Skip to Phase 1] — Design without pre-integrated videos
                    (Videos can be added post-book)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

===============================================================================
                         PHASE 1: FOUNDATION
===============================================================================

Establish the game's identity and creative direction.

## Gather:

1. **The NPC**
   - Name
   - General vibe (girl-next-door, seductress, innocent, mature, etc.)
   - What makes her appealing?

2. **The Setting**
   - Domestic (home, apartment)
   - Workplace (office, service industry)
   - Social (college, neighborhood)
   - Fantasy (custom scenario)

3. **The Relationship**
   - Step-family (step-mom, step-sister, step-aunt)
   - Roommate/housemate
   - Landlord/tenant
   - Neighbor
   - Boss/employee
   - Friend's mom/sister
   - Other

4. **Driver** (from driver table above)
   - Primary driver recommendation based on NPC/relationship
   - Optional secondary driver

5. **Core Premise**
   - The "What if?" hook in 2-3 sentences
   - What emotional journey does the player experience?

6. **Tone**
   - Slow-burn (14+ days, gradual escalation)
   - Fast-burn (7-10 days, quicker to sex)
   - Mixed (slow emotional, faster physical)

7. **Game Scope**
   - Number of in-game days (reference: 30 days)
   - Target locations (reference: 11 locations)
   - Target NPC activities (reference: 6-8 escalating)
   - Target story events (reference: 13)
   - Target utility canvases (reference: 9)

8. **Game Architecture**
   Choose the structure that fits the story:

   **Option A: Single-NPC Romance** (one player, one NPC, one relationship arc)
   - Uses: NPC driver system (7 drivers), emotional quadrant, designer-chosen gate flags
   - Primary stat is on the NPC (love, obsession, trust, etc.)
   - Player builds ONE deep relationship through activities + story events
   - Reference game: Jack's World
   - Relevant sections: NPC Driver Table, Emotional Quadrant, Hybrid Gating Model

   **Option B: Multi-NPC Parallel Arcs** (one player, multiple NPCs, staggered storylines)
   - Uses: Player corruption as primary driver, shared unlock flags, staggered arcs
   - Primary stat is on the PLAYER (corruption, confidence, etc.)
   - Player pursues multiple NPCs across overlapping corruption bands
   - Each NPC has secondary stats (love/trust/corruption) for NPC-specific gating
   - Reference game: New In Town
   - Relevant sections: Player-Stat-Driven Progression, Multi-NPC Activity Design,
     Parallel Arc Design, Clothing/Wardrobe System

   This choice affects which sections of Phase 2-6 are most relevant.
   Both architectures share: tiered activities, flag-gated escalation, time schedules,
   economic model, story arc system.

## Consider Video Integration Context:

If Phase 0 was completed, reference activities and locations already designed.

## Present:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1: FOUNDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NPC(s): [Name(s)]
Vibe: [Description]
Setting: [Type]
Relationship: [Type]
Architecture: [Single-NPC Romance / Multi-NPC Parallel Arcs]
Driver: [Primary] (+ [Secondary] if applicable)
Premise: "[What if... hook]"
Tone: [slow-burn / fast-burn / mixed]
Scope: [X] days, [X] locations, [X] activities, [X] events

★ RECOMMENDED DIRECTION:
[Brief creative summary based on all inputs]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue, or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

===============================================================================
                    PHASE 2: CHARACTERS & STAT ECONOMY
===============================================================================

Define the characters and the mechanical systems that drive progression.

## Section 1: Player Definition

- Name, description, portrait reference
- Starting stats (e.g., `money = 50`)
- Background: Who is the player? Why are they here?
  (1-2 paragraphs establishing identity and motivation)

### Player Psychology (REQUIRED — 1 paragraph)
Define the player character's inner life — he is NOT a blank insert:
- **Want**: What does he consciously desire? (e.g., "a fresh start," "independence")
- **Need**: What does he actually need but doesn't know yet? (e.g., "connection," "to be known")
- **Fear**: What is he afraid of? (e.g., "being trapped again," "vulnerability")
- **Flaw**: What behavior pattern gets in his way? (e.g., "avoids conflict," "overthinks")

### Player Emotional Phases (REQUIRED)
Define how the player character's emotional state evolves through the story.
Each phase should be tied to a specific story event that triggers the transition:

| Phase | Triggered By | Player Mindset | How It Shows in Narration |
|-------|-------------|---------------|--------------------------|
| OUTSIDER | Arrival | Guarded, observational | Short sentences, notices environment not people |
| SETTLING | [story event] | Relaxing, curious | Starts noticing NPC habits and routines |
| WANTING | [story event] | Attracted, hopeful | Narration becomes charged, notices physical details |
| TORN | [story event] | Conflicted, afraid to lose | Internal debate visible, longer reflective passages |
| COMMITTED | [story event] | Determined, emotionally open | Honest internal voice, emotional vocabulary expands |
| BELONGING | [story event] | Settled, intimate | Quiet confidence, intimate shorthand, shared history references |

### Player Internal Voice (REQUIRED)
Define how the player's perspective changes across phases:

**What player notices (evolves over time):**
| Phase | Notices | Example |
|-------|---------|---------|
| OUTSIDER | Environment, layout, rules | "The kitchen is bigger than my last apartment." |
| SETTLING | NPC routines, small habits | "She always hums when she cooks." |
| WANTING | NPC's body, proximity, charged moments | "She reached past me for the shelf. I forgot what I was saying." |
| TORN | What he'd miss, stakes | "I tried to imagine the house without her in it." |
| COMMITTED | The relationship itself | "When did 'her kitchen' become 'our kitchen'?" |
| BELONGING | Quiet details, shared history | "She left a note. Just 'Good morning.' It was enough." |

**How player describes NPC (evolves over time):**
| Phase | Description Style | Example |
|-------|------------------|---------|
| OUTSIDER | Physical, surface | "Tall, dark hair, sharp eyes. My new landlord." |
| SETTLING | Personality details | "She's funnier than I expected. Dry humor." |
| WANTING | Attraction-focused | "The way the light catches her collarbone..." |
| TORN | Emotional depth | "She's braver than she knows. And more scared." |
| COMMITTED | Partnership language | "She trusts me with the real version of herself." |
| BELONGING | Intimate familiarity | "She." (Who else would it be?) |

**Choice text framing (evolves over time):**
| Phase | Choice Tone | Example |
|-------|------------|---------|
| OUTSIDER | Cautious, polite | "Offer to help" / "Keep to yourself" |
| SETTLING | Friendly, curious | "Ask her about it" / "Give her space" |
| WANTING | Charged, risk-aware | "Move closer" / "Stay where you are" |
| TORN | High-stakes, emotional | "Tell her how you feel" / "Protect the friendship" |
| COMMITTED | Honest, direct | "Stay with her tonight" / "Give her time" |
| BELONGING | Intimate, natural | "Take her hand" / "Just be there" |

## Section 2: NPC Definition

For each NPC:

### Physical Appearance (3-4 sentences)
- Build, hair, skin, distinctive features
- How they dress at different times of day
- What makes them physically attractive

### Personality Traits (3-4 key traits)
- Surface traits (what people see)
- Hidden traits (what emerges over time)

### Psychology (1-2 paragraphs)
- What do they want? What are they afraid of?
- Internal conflict that drives their arc
- How do they respond to intimacy vs vulnerability?

### Internal Contradictions (REQUIRED — 2-3 contradictions)
Every compelling NPC wants two things that conflict with each other:
- She wants connection BUT fears being hurt again
- She wants to be desired BUT feels guilty about who's desiring her
- She wants control over her life BUT craves surrender
- She wants to be a good [role] BUT is attracted to someone she shouldn't be
- She wants independence BUT is lonely

These contradictions DRIVE story events. When contradiction A peaks, she
pulls toward the player. When contradiction B peaks, she pushes away.
Design at least 2-3 story events where the NPC's contradictions create
visible tension.

### Resistance Pattern (REQUIRED)
How the NPC pushes back when things escalate too fast or too far:

| Stage | Resistance Behavior | What Triggers It |
|-------|-------------------|-----------------|
| MILD | Short answers, avoids eye contact, changes subject | After first physical moment |
| MODERATE | Creates physical distance, cancels plans, cold for 1-2 days | After a gate-unlocking event |
| SEVERE | Confrontation, "We need to talk", threatens to end arrangement | After crisis/boundary break |
| RECOVERY | Tentative re-approach, vulnerability, "I was scared" | After player shows patience |

The resistance pattern is NOT the same every time. Early resistance (post-peek)
is mild. Mid-game resistance (post-kiss) is moderate. The major crisis
resistance is severe. Each recovery should feel harder-earned than the last.

### Emotional Quadrant Behaviors (REQUIRED)

Define how this specific NPC behaves in each emotional quadrant.
These behaviors inform activity base scene writing and story event
reactions. Use the NPC's unique personality — don't use generic behaviors.
(See NPC EMOTIONAL FLOW in Game Mechanics Reference for quadrant definitions.)

| Quadrant | This NPC's Specific Behavior |
|----------|-------------------------------|
| DISTANT (low primary / low trust) | [3-4 specific behaviors unique to this NPC. Example for Angela: "She cooks only for herself. Leaves his laundry in the basket. Wears headphones in the living room. Answers in sentence fragments."] |
| SAFE (low primary / high trust) | [3-4 behaviors. Example: "Asks about his shift. Saves him dinner. Sits on her end of the couch — comfortable, not charged. Talks about the news."] |
| CONFLICTED (high primary / low trust) | [3-4 behaviors. Example: "Watches him from the kitchen doorway then looks away. Cooks elaborate meals but eats in her room. Starts sentences with his name then changes direction. Wears perfume even though she's 'not going anywhere.'"] |
| OPEN (high primary / high trust) | [3-4 behaviors. Example: "Sits next to him without reason. Touches his arm mid-sentence. Laughs with her whole body. Says 'we' instead of 'I'. Leaves her bedroom door open at night."] |

### Emotional Tells by Stat Range (REQUIRED)

Define observable behaviors that signal the NPC's stat levels. These
should appear naturally in activity base scenes:

**Primary Stat Tells:**
| Range | Observable Behavior |
|-------|-------------------|
| 0-20 | [Example: "She hands you coffee. No comment. Already looking at her phone."] |
| 21-40 | [Example: "She hands you coffee. 'Sleep okay?' Genuine question, not small talk."] |
| 41-60 | [Example: "She hands you coffee. Her fingers brush yours. She doesn't take her hand back."] |
| 61-80 | [Example: "She's already poured your coffee. She's wearing the shirt you said you liked."] |
| 81-100 | [Example: "She's in your shirt. Coffee's ready. She kisses your shoulder as she passes."] |

**Trust Tells:**
| Range | Observable Behavior |
|-------|-------------------|
| 0-10 | [Example: "She closes her laptop when you walk in. Conversation pauses when you enter."] |
| 11-20 | [Example: "She doesn't close the laptop. Mentions she's paying bills. Doesn't elaborate."] |
| 21-30 | [Example: "She asks if you can look at something — a bill, a decision. Values your input."] |
| 31-40 | [Example: "She talks about the divorce without being asked. Cries in front of you. Doesn't apologize for it."] |
| 41-50 | [Example: "She falls asleep on the couch with you there. Gives you a key. Says 'our apartment.'"] |

These tells are the LIFEBLOOD of the game experience. They make the player
feel the relationship growing (or breaking) through tiny details, not
just stat numbers. Every activity base scene should include 1-2 tells
appropriate to the NPC's current stat range.

### Speech Patterns
- Sentence structure (short and direct? Flowing and warm?)
- What they say vs what they mean
- How speech changes as relationship deepens

### Starting Stats
- Primary stat (from driver): starts at 0
- Trust: starts at 0
- Any NPC-specific flags

## Section 2.6: NPC Customization (Optional)

For NPCs whose name and relationship the player should be able to personalize:

### When to Make an NPC Customizable
- Family relationships (step-siblings, step-parents) where the player might prefer a different family dynamic
- Roommates/housemates where the cohabitation reason could vary
- Any NPC whose relationship to the player is part of the fantasy/immersion

### What to Define
| Field | Purpose | Example |
|-------|---------|---------|
| `customizable = true` | Enables the customization screen at game start | |
| `relationship` | Default relationship label | `"step-brother"` |
| `relationship_options` | Player-selectable alternatives | `["step-brother", "roommate", "landlord"]` |

### Content Writing Rule
ALL narrative content referencing a customizable NPC must use `@`-syntax:
- `@ethan` → NPC's current name (from `npc_ethan`)
- `@ethan.rel` → NPC's relationship label
- `@ethan's` → possessive form

**Example:**
```
Instead of: "Ethan looks up from his coffee. Your step-brother smiles."
Write: "@ethan looks up from his coffee. Your @ethan.rel smiles."
```

### Relationship Options Design
- All options must work with the SAME narrative text — "Your @ethan.rel pours coffee" must make sense for every option
- Pick options that share the same living situation or proximity context
- Good: `["step-brother", "roommate", "housemate"]` (all live together)
- Bad: `["step-brother", "coworker", "stranger"]` (different proximity/context)

## Section 3: Stat Economy Design

### Primary NPC Stat Growth
| Source | Gain | Frequency |
|--------|------|-----------|
| Base activity exit | +1 | Every visit |
| Warm/suggestive choice | +2 | Per visit |
| Kiss/foreplay choice | +2 | Per visit |
| Intimate/oral choice | +2-3 | Per visit |
| Story events (minor) | +1-3 | One-time |
| Story events (major) | +3-8 | One-time |

### Trust Growth
| Source | Gain | Frequency |
|--------|------|-----------|
| Basic chore | +1 | Daily |
| Cooking | +2 | Daily |
| Rent payment | +2-3 | Weekly |
| Emotional story moment | +2-3 | One-time |
| Major trust event | +3-5 | One-time |

### Player Resource Flows
| Source | Amount | Frequency |
|--------|--------|-----------|
| Job shift | +$70 | Per shift |
| Weekly rent | -$200 | Weekly |
| Groceries | -$20 | Per trip |
| Major purchase | -$300 | Story-gated |

### Target Progression
| Day Range | Primary Stat | Trust | Money |
|-----------|-------------|-------|-------|
| Days 1-5  | 0-20        | 0-10  | 50-200 |
| Days 5-10 | 20-40       | 10-20 | Stable |
| Days 10-18| 40-70       | 20-30 | Saving |
| Days 18-30| 70-100      | 30-50 | Spent on event |

## Section 4: Gate Flag Design

| Gate | Story Event That Sets It | Approx. Day | Unlocks |
|------|--------------------------|-------------|---------|
| kiss_unlocked | [event name] | Day ~8 | Kissing choices |
| groping_unlocked | [event name] | Day ~12 | Foreplay choices |
| oral_unlocked | [event name] | Day ~16 | Oral/intimate choices |
| sex_unlocked | [event name] | Day ~22 | Full sex choices |

## Section 5: Complete Flag Inventory

List ALL flags the game will use:
- Progression flags (event_1_complete, event_2_complete, etc.)
- Gate flags (kiss_unlocked, groping_unlocked, oral_unlocked, sex_unlocked)
- Utility flags (chores_explained, job_started, rent_last_paid, etc.)
- Content flags (peek_unlocked, etc.)

---

===============================================================================
                         PHASE 3: WORLD DESIGN
===============================================================================

Define the physical space, time system, and economic model.

## Section 1: Location Hierarchy

Design the navigation structure. Each location needs:
- ID (lowercase_snake_case with `loc_` prefix)
- Name (display name)
- Description (2-3 atmospheric sentences)
- Image reference and search queries
- Parent/child relationships
- Navigation connections (entry_from, navigation_order)

REFERENCE STRUCTURE (from Jack's World):
```
Street (external hub)
  ├── Home / Hallway (apartment hub)
  │     ├── Kitchen
  │     ├── Living Room
  │     ├── Angela's Bedroom
  │     ├── Bathroom
  │     └── Jack's Bedroom
  ├── Cafe
  └── Hotel (container)
        └── Hotel Lobby
              └── Hotel Room
```

Rules:
- One external hub connects to external locations
- One internal hub connects apartment/house rooms
- Containers use `is_container = true` with `default_entry`
- Rooms have `entry_from` pointing to their hub
- Hubs have `navigation_order` listing accessible rooms

## Section 2: Time System

- Starting hour, day, week
- Which activities fire during which time periods
- Activity schedule overview:

| Time Period | Location | Activity |
|-------------|----------|----------|
| 06:00-07:30 | Bedroom | Morning peek/encounter |
| 07:00-09:00 | Kitchen | Breakfast together |
| 09:00-14:00 | Kitchen/Living/Bath | Chores |
| 07:00-12:00 | Cafe | Morning shift |
| 14:00-17:00 | Cafe/Bedroom | Afternoon shift / massage |
| 17:00-19:00 | Kitchen | Cook dinner |
| 19:00-22:00 | Bathroom/Living | Bath / deep conversation |
| 22:00-01:00 | Living/Bedroom | Movie night / night together |

## Section 3: Economic Model

- Income source(s) and rates
- Recurring expenses and timing
- Major story-gated purchases
- Minimum shifts per week to survive
- Time remaining for NPC activities after work obligations
- How economic pressure creates meaningful choices

## Section 4: NPC Schedules

For each NPC, define where they are during each time period.
This determines which activities can fire when.

---

===============================================================================
                         PHASE 4: STORY EVENTS
===============================================================================

Design all one-time narrative events that drive the story forward.

## DRAMATIC STRUCTURE REQUIREMENTS

Before designing individual events, map the dramatic spine:

### Step 1: Define the Central Tension
What is fundamentally at risk in this story? Not "will they hook up" —
that's the progression system. The central tension is emotional:
- "Can two people who shouldn't want each other build something real?"
- "Can she trust again after being abandoned?"
- "Can he become the kind of man who deserves her?"

Write the central tension as a single question. Every story event should
either raise or lower the odds of the answer being YES.

### Step 2: Define the Primary Conflict
Choose from the conflict types in the Dramatic Spine section.
Specify:
- What is the threat?
- When does it first appear? (Act 1 — foreshadow, Act 2 — peak)
- How does the player resolve it?
- What does resolution cost?

### Step 3: Map the Tension Curve
For each story event, assign a TENSION DIRECTION:

| Event | Tension | Direction | Why |
|-------|---------|-----------|-----|
| Opening | — | neutral | Establishing |
| House Rules | up | rising | Stakes set |
| Accidental Glimpse | up-up | rising | Forbidden spark |
| Caught Watching | DOWN | FALLING | Trust broken, she's angry |
| Apology / Repair | up | recovering | Player earns back trust |
| First Kiss | up-up-up | peak | Emotional breakthrough |
| The Confrontation | DOWN-DOWN | CRISIS | She questions everything |
| Recovery Arc | up-up | rebuilding | Harder-earned this time |
| Deeper Intimacy | up-up-up | new peak | Stronger than before |
| Turning Point | up-up-up-up | climax | Everything pays off |

Required tension/crisis events are marked DOWN. At least 2.
The curve should look like a heartbeat, NOT a straight line going up.

### Step 4: Design Regression Events
At least 2 events where stats DROP. These are NOT punishments — they're
the moments that make the story feel real.

REGRESSION EVENT TEMPLATE:
- **Trigger**: What causes the crisis (flag + stat + timing)
- **The Drop**: Which stat decreases and by how much (-3 to -8)
- **The Fallout**: How the NPC behaves differently for 1-3 days
  (Activities still trigger, but base scenes reflect the tension:
   shorter dialogue, no eye contact, she leaves the room earlier)
- **The Repair Path**: What the player must do to recover
  (NOT just "keep doing activities" — a specific action or choice)
- **The Resolution**: A one-time event that marks recovery
  (Should feel earned: 2-4 in-game days of effort, not one conversation)

### Step 5: Design Bridge Events
Between each gate flag, there must be at least ONE non-mechanical event —
a scene that exists purely for character development, not to unlock anything:

- An argument that reveals something true about both characters
- A quiet moment of unexpected vulnerability (not triggered by a gate)
- A shared experience that bonds them (cooking disaster, power outage,
  helping a neighbor, a birthday, a rainy day)
- A revelation that changes how the player sees the NPC
- A sacrifice (small or large) that proves commitment

Bridge events set their own flags but those flags don't gate any mechanics.
They exist to make the characters feel like real people between milestones.


## OPENING SCENE (starting_canvas — no trigger)

The first canvas plays automatically. No trigger section.
Must establish:
- Player identity (who they are, why they're here)
- NPC introduction (first impression, physical description)
- Situation setup (living arrangement, tension, ground rules)
- Sets: `game_started` + arrival completion flag

Reference: 3+ nodes with player arrival, NPC meeting, initial dialog.

## ACT 1: ESTABLISHING THE WORLD (Peek Gate)

Events that set up the daily routine, unlock utility systems, AND
introduce the first spark of tension.

Low or no stat requirements. Flag-chained sequentially.

For each event, specify:
- **Canvas name and ID**
- **Trigger**: location, NPC (if any), schedule, conditions
  (flags required, trait thresholds, days_since_flag if applicable)
- **Priority**: 10 for story events
- **Nodes**: Narrative beats per node (setup → climax → aftermath)
- **Choices**: What the player decides, with stat effects
  IMPORTANT: Both choices should set the SAME flag (ensures progression)
- **Flags set**: What this event unlocks
- **Video/media**: Specs for each visual moment

ACT 1 STORYLINE REQUIREMENTS:
- At minimum: 3-4 events that establish routine + 1 that creates first spark
- The first spark event should have a CONSEQUENCE — not just a stat bump
  (e.g., accidental glimpse → she notices something is different about him)
- At least 1 bridge event (non-mechanical character development)
- End of Act 1 should feel like: "Something is shifting, and neither of
  them can pretend otherwise"
- NPC emotional quadrant: DISTANT → SAFE → edge of WARMING

Act 1 typically unlocks: chores, jobs, peek activities.
Gate unlocked at end of Act 1: peek_unlocked (if applicable to the game)


## ACT 1 → ACT 2 TRANSITION: FIRST TENSION EVENT

Between Act 1 and Act 2, design ONE tension event where the new closeness
creates friction:

TEMPLATE:
- The player or NPC has crossed a line (even a small one)
- The NPC reacts with MILD resistance (see Resistance Pattern from Phase 2)
- The player has a TRADE-OFF choice:
  Option A: Address it directly → higher trust risk, faster recovery
  Option B: Let it pass → safer, but the tension simmers (surfaces later)
- Stat effect: Trust drops -2 to -4, regardless of choice
- Recovery: 1-2 days of normal activities restore trust
- NPC emotional quadrant: Briefly enters CONFLICTED, returns to WARMING

This event teaches the player that ACTIONS HAVE CONSEQUENCES and that
the relationship isn't a guaranteed escalation.


## ACT 2: DEEPENING THE RELATIONSHIP (Kiss → Groping → Oral Gates)

Events that set gate flags, deepen emotional connection, AND navigate
the major crisis.

Increasing stat requirements. `days_since_flag` for pacing.

Gate-setting events are the most important — clearly mark which
event sets kiss_unlocked, groping_unlocked, oral_unlocked.

ACT 2 STORYLINE REQUIREMENTS:
- Gate-setting events must feel EARNED through preceding drama, not just
  stat thresholds being met
- At minimum: 2-3 gate events + 1 crisis event + 1-2 bridge events
- The MAJOR CRISIS must happen in Act 2, between kiss_unlocked and oral_unlocked
- NPC emotional quadrant journey: OPEN → CONFLICTED (crisis) → DEEP OPEN

### THE MAJOR CRISIS (REQUIRED)

This is the dramatic centerpiece of the game. Design it carefully:

WHAT MAKES A GOOD CRISIS:
- It threatens to END the relationship, not just slow it down
- The NPC has a genuine reason to pull away (not manufactured drama)
- The player cannot fix it with one choice — it takes multiple days
- Both characters are forced to confront what they really want
- The resolution requires VULNERABILITY from both sides

CRISIS STRUCTURE:
1. THE TRIGGER (one-time event, priority 10)
   - Something shatters the comfortable dynamic
   - Stat drop: primary stat -5 to -8 OR trust -4 to -6
   - Sets a crisis flag (e.g., `crisis_active`)
   - NPC quadrant: Abrupt shift OPEN → CONFLICTED

2. THE FALLOUT (2-3 days of changed behavior)
   - Activity base scenes reference the crisis
     (shorter dialogue, tension, avoidance — see Phase 5 WITHDRAWN variants)
   - NPC is present but emotionally withdrawn
   - Player cannot meaningfully escalate during this period
   - NPC quadrant: Deep CONFLICTED (high primary + low trust)

3. THE REPAIR (1-2 one-time events over 2-3 days)
   - Player must make a SACRIFICE choice (money, pride, comfort, a secret)
   - The NPC's resistance pattern moves through SEVERE → RECOVERY
   - Each repair event restores some stats but not all
   - NPC quadrant: CONFLICTED softening

4. THE RESOLUTION (one-time event)
   - NPC confronts her own contradictions (from Phase 2)
   - The moment of choosing to stay / come back / try again
   - Stats restored to pre-crisis level + bonus (+2 to +5 above)
   - The relationship is now STRONGER than before the crisis
   - Sets crisis_resolved flag, which can gate the next milestone
   - NPC quadrant: CONFLICTED → OPEN (deeper than before)

CRISIS EXAMPLES BY CONFLICT TYPE:

EXTERNAL THREAT:
  Father calls → wants to visit → NPC panics about being discovered →
  pulls away → player must choose: "Tell him not to come" (protects her,
  loses family connection) or "Let him visit" (she goes cold, crisis deepens,
  but resolved if player handles it with care)

INTERNAL CRISIS:
  After first kiss, NPC spirals into guilt → "I'm his step-mom" →
  avoids player for 3 days → cold at breakfast → player finds her crying
  at night → player must be patient (NOT pushy) → she comes to him when
  she's ready → the apology scene is the most vulnerable she's been

BOUNDARY BREAK:
  NPC discovers player was watching her (peek activities) → she's not angry,
  she's hurt: "How long?" → trust drops hard → player must confess fully
  (partial truth = worse) → she processes → returns with: "I knew. I just
  needed to hear you say it."

REVELATION:
  Player discovers NPC has been in contact with his father → she's been
  sending him updates → "He asked me to look after you" → player feels
  betrayed: "Is that what this is?" → she must prove it became real →
  the fight is the first time they're truly honest


## TURNING POINT

The most narratively significant event. Typically:
- Sets `sex_unlocked`
- Requires high stats + flags + resources (e.g., money >= 300)
- Multiple nodes with emotional weight
- Full video integration for the climactic moment

The turning point should REFERENCE the crisis:
- "After everything that happened..." or "I almost lost you."
- The intimacy feels deeper BECAUSE they almost didn't make it
- This is where the NPC's primary internal contradiction resolves
  (she accepts what she wants, who she is, what this relationship means)
- NPC quadrant: DEEP OPEN — the deepest she's been


## ACT 3: RESOLUTION

Post-sex events that show the relationship has fundamentally changed.
Optional — the game may end at the turning point or continue.

Act 3 should show CHANGED BEHAVIOR, not just higher-tier content:
- The NPC is fundamentally different than at the start
- Dialogue reflects growth ("I used to think..." / "Before you, I...")
- The relationship has a name now (even if unspoken)
- At least 1 scene should be tender/quiet, not sexual — proving the
  relationship is more than physical
- NPC quadrant: COMPLETE (high primary + high trust)

## FLAG CHAIN DIAGRAM

Draw the complete event dependency chain, including crisis and bridge events:

```
game_started → jack_arrived_complete
  → chores_explained (unlocks chores)
  → peek_unlocked (unlocks voyeur activities)
    → bills_discovered → job_started (unlocks work)
      → first_rent_paid → late_night_talk
    → [TENSION] caught_watching (trust drops)
      → apology_accepted (REPAIR)
        → towel_encounter_complete
          → first_kiss_complete
            → kiss_unlocked (GATE 1)
              → [BRIDGE] shared_moment (character depth, no mechanic)
                → [CRISIS] guilt_crisis (she pulls away, trust drops)
                  → crisis_confrontation (REPAIR 1)
                    → crisis_resolution (REPAIR 2 — stronger)
                      → groping_unlocked (GATE 2)
                        → oral_unlocked (GATE 3)
                          → date_proposed → sex_unlocked (GATE 4)
```

[TENSION] = tension event (stats drop, mild)
[CRISIS] = major crisis (stats drop significantly, 2-4 day recovery)
[BRIDGE] = non-mechanical character development event

## GATE TIMELINE

| Gate | Set By | Requirements | ~Day |
|------|--------|-------------|------|
| kiss_unlocked | [event] | [conditions] | ~8 |
| groping_unlocked | [event] | [conditions] | ~12 |
| oral_unlocked | [event] | [conditions] | ~16 |
| sex_unlocked | [event] | [conditions] | ~22 |

---

## MULTI-NPC PARALLEL ARC DESIGN (Multi-NPC Architecture)

For multi-NPC games, Phase 4 uses a fundamentally different structure.
Instead of one linear story chain, you design MULTIPLE parallel arcs
with staggered corruption bands.

### Linear Opening (~8 canvases)

The first ~8 canvases are fully linear (forced sequence) to establish the world:
1. Arrival / moving in
2. Meeting key NPCs
3. Discovering the environment
4. First job / economic introduction
5. First exposure to the world's sexual atmosphere
6. **Inciting event** — the moment that shifts the player's worldview
7-8. Immediate aftermath, opening up the world

The inciting event is the transition from linear → open world. After this,
multiple arcs become available simultaneously.

### Parallel Arc Design

Each arc is a chain of one-time story canvases gated by:
- Player corruption level (primary gate)
- Arc-specific flags (previous canvas in this arc completed)
- NPC stats where relevant (love/trust for that specific NPC)

Design arcs with STAGGERED corruption bands so the player always has
2-3 active options:

```
CORRUPTION MILESTONE TABLE:

Corruption 0-30:    Linear opening (forced sequence)
Corruption 30-60:   Personal arc opens (self-discovery, body awareness)
Corruption 38-60:   Glory hole arc opens (anonymous, low-stakes)
Corruption 40-80:   Mick arc opens (first NPC relationship)
Corruption 65-120:  Bar work arc opens (escalating work choices)
Corruption 100-180: Harlan arc opens (dominant NPC, higher stakes)
Corruption 140-220: Public arc opens (highest escalation)
```

### Cross-Arc Flag Sharing

Unlock flags are SHARED across all arcs. When a story event in any arc
sets `flirt_unlock`, ALL activities across ALL arcs gain the flirting tier:

```
Mick story event → sets flirt_unlock
  → Bar work: "Flirt for tips" now available
  → Glory hole: "Flirt through the wall" now available
  → Public: "Flirt with strangers" now available
```

Each arc should set at least one shared unlock flag at an appropriate
corruption milestone. Plan which arc sets which flag:

| Unlock Flag | Set By Arc | At Corruption | Story Event |
|-------------|-----------|--------------|-------------|
| flirt_unlock | [arc name] | ~65 | [event name] |
| tease_unlock | [arc name] | ~90 | [event name] |
| handjob_unlock | [arc name] | ~120 | [event name] |
| blowjob_unlock | [arc name] | ~150 | [event name] |
| sex_unlock | [arc name] | ~180 | [event name] |

### Per-Arc Story Chain

For each arc, list its canvases as a flag chain:

**[Arc Name] (corruption X — Y)**
```
arc_intro → arc_step_2 → arc_step_3 → ... → arc_climax
```

Each canvas specifies:
- **Trigger conditions**: corruption threshold + previous flag + NPC stat (if any)
- **Flags set**: completion flag for this canvas + any shared unlock flags
- **Stat effects**: player corruption gain, NPC stat gains
- **Nodes**: narrative beats (same as single-NPC format)

### No Dead Zones Rule
At every corruption level from 30 to max, the player MUST have at least
2 available arcs. Check for gaps:

```
Corruption 30:  personal + glory_hole     ✓ (2 arcs)
Corruption 70:  personal + mick + bar     ✓ (3 arcs)
Corruption 100: mick + bar + harlan       ✓ (3 arcs)
Corruption 140: bar + harlan + public     ✓ (3 arcs)
Corruption 200: bar + harlan + public     ✓ (3 arcs)
```

---

===============================================================================
                         PHASE 5: ACTIVITIES
===============================================================================

Design all repeatable canvases — NPC activities, utility canvases, and solo activities.

## EMOTIONAL STATE IN ACTIVITY SCENES

Activity base scenes are where the player FEELS the NPC's emotional state
most consistently. Because activities repeat, the base scene is the
primary canvas for expressing emotional quadrant shifts.

GUIDANCE FOR WRITING BASE SCENES:
Write the base scene narrative at the NPC's MID-RANGE emotional state
(the most common state when the player encounters this activity).
Then add EMOTIONAL MARKERS — short behavioral notes that the book can
flag for different states:

EXAMPLE (Breakfast Activity base scene):

  DEFAULT (SAFE/OPEN quadrant — most common):
  "Morning light through the kitchen window. Angela is at the counter,
   coffee already made. She looks up when you walk in."

  POST-CRISIS VARIANT (CONFLICTED quadrant):
  "The kitchen is quiet. Angela's coffee mug is in the sink — she already
   ate. A plate is in the microwave. No note."

  DEEP OPEN VARIANT (late-game, high stats):
  "Angela is humming. She pours your coffee without asking — she knows
   how you take it now. 'Morning,' she says, and the word sounds like home."

When designing each NPC activity in the book, write:
1. The DEFAULT base scene (used most of the time)
2. A WITHDRAWN variant (for post-crisis / CONFLICTED quadrant)
3. A WARM variant (for high-stat / OPEN quadrant)

These variants make the world feel ALIVE — the NPC isn't a vending machine
that dispenses the same scene regardless of relationship state.

NOTE: The TOML format supports a single base scene per activity. The
variants are creative direction — the book describes how the base scene's
TONE should shift at different emotional states, and the TOML writer uses
the default variant while embedding emotional indicators that work across
the range.

## SECTION A: NPC ACTIVITIES (ESCALATING)

For each NPC activity, specify:

### Activity: [Name]
- **Pattern**: A (standard escalation) or B (dual-path)
- **Location**: [loc_id]
- **Schedule**: [HH:MM - HH:MM]
- **NPC**: [npc_id]
- **Unlock conditions**: [flags/traits needed to trigger]
- **Priority**: [1 for standard, 6-8 for special]

**Base Scene** (always shown):
  Narrative: [3-5 sentences describing the domestic/default scene]
  Videos: [clip specs — file paths or descriptions]

**Choice Progression:**

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "[safe option]" | always | exit | +1 [stat], +1 trust |
| "[warm option]" | [stat] >= 22 | warm | +2 [stat] |
| "[kiss option]" | [stat] >= 42 + kiss_unlocked | kiss | +2 [stat] |
| "[foreplay option]" | [stat] >= 62 + groping_unlocked | foreplay | +2 [stat] |
| "[intimate option]" | [stat] >= 82 + oral_unlocked | intimate | +2-3 [stat] |
| "[full option]" | [stat] >= 82 + sex_unlocked | intense | +2-3 [stat] |

Note: Not every activity needs all 6 levels. Cap at whatever fits narratively.

**Escalation Nodes** (one per unlockable choice):
For each node:
  - Narrative: [paragraph → video → reaction → dialog]
  - Videos: [2-3 clips with explicit descriptions]
  - Exit choices: [2 options that both exit the canvas with slight stat differences]

**For Pattern B (Dual-Path):**
  - Describe BOTH paths separately
  - Voyeur path: linear chain, no internal gating
  - Participate path: requirements, internal gating, higher rewards

## SECTION B: UTILITY CANVASES

### Chores
| Name | Location | Schedule | Effects | Unlock Flag |
|------|----------|----------|---------|-------------|
| Wash Dishes | Kitchen | 09:00-14:00 | +1 trust | chores_explained |
| Cook Dinner | Kitchen | 17:00-19:00 | +2 trust | chores_explained |
| Clean Apartment | Living Room | 09:00-14:00 | +1 trust | chores_explained |
| Do Laundry | Bathroom | 09:00-14:00 | +1 trust | chores_explained |
| Grocery Shopping | Street | 09:00-17:00 | +1 trust, -$20 | chores_explained |

### Jobs
| Name | Location | Schedule | Pay | Trust | Max/Day |
|------|----------|----------|-----|-------|---------|
| Cafe Shift AM | Cafe | 07:00-12:00 | +$70 | +1 | 2 |
| Cafe Shift PM | Cafe | 14:00-17:00 | +$70 | +1 | 2 |

### Time Advancement
| Name | Location | Choices |
|------|----------|---------|
| Jack's Room | Bedroom | Rest (120 min) / Sleep (540 min) |

### Recurring Expenses
| Name | Location | Trigger | Cost | Trust | Timer |
|------|----------|---------|------|-------|-------|
| Weekly Rent | Kitchen | first_rent_paid | -$200 | +2-3 | days_since(rent_last_paid) >= 7 |

## SECTION C: SOLO ACTIVITIES (OPTIONAL)

Player-only activities without NPC interaction.
List any if designed, or note "None for this game."

---

===============================================================================
                         PHASE 6: STORY ARC
===============================================================================

Define the narrative journal system that tracks the player's emotional journey.

## Section 0: Dramatic Spine Summary

Before defining chapters, summarize the dramatic spine designed in Phase 4:

### Central Tension
"[The one-question summary of the story's emotional core]"

### Conflict Type
[Primary conflict type from the Dramatic Spine reference]

### Tension Curve Summary
```
[Arrival] → [Routine] → [First Spark] → [First Tension] →
[Repair] → [Kiss] → [Major Crisis] → [Recovery] →
[Deeper Intimacy] → [Turning Point] → [Resolution]
```

### Key Emotional Beats
| Beat | Event | Player Feels | Player Phase | NPC Feels | NPC Quadrant |
|------|-------|-------------|-------------|-----------|-------------|
| Arrival | [event] | Displacement, curiosity | OUTSIDER | Guarded / assessing | DISTANT |
| First Spark | [event] | Excitement + guilt | SETTLING→WANTING | Unaware / noticing | SAFE→edge |
| First Tension | [event] | Fear of losing her | WANTING | Hurt / protective | CONFLICTED |
| Breakthrough | [event] | Relief + desire | WANTING→TORN | Vulnerability / choosing trust | OPEN |
| Major Crisis | [event] | Panic / desperation | TORN (crisis) | Self-doubt / withdrawal | deep CONFLICTED |
| Recovery | [event] | Determination + vulnerability | TORN→COMMITTED | Testing / wanting to believe | CONFLICTED→OPEN |
| Turning Point | [event] | Love + certainty | COMMITTED→BELONGING | Surrender / acceptance | DEEP OPEN |

This summary ensures the Story Arc journal entries reflect the dramatic
spine and emotional quadrant transitions, not just a flat progression.

## Section 1: Chapters

| ID | Name | Mood | Description | Order |
|----|------|------|-------------|-------|
| chapter_prologue | A New Arrangement | hopeful | [1-2 sentences] | 1 |
| chapter_act1 | The New Normal | hopeful | [1-2 sentences] | 2 |
| chapter_act2 | Growing Closer | romantic | [1-2 sentences] | 3 |
| chapter_turning | The Breaking Point | passionate | [1-2 sentences] | 4 |
| chapter_act3 | Deep Connection | passionate | [1-2 sentences] | 5 |
| chapter_resolution | What We Became | peaceful | [1-2 sentences] | 6 |

Moods: hopeful | romantic | tense | passionate | peaceful | neutral

## Section 2: Story Nodes

One node per story event, linked to its canvas:

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| arrival | Jack Arrives | prologue | jack_arrives | jack_arrived_complete | true | "[First-person reflection]" |
| ... | ... | ... | ... | ... | ... | ... |

Journal entries should be first-person reflections from the player's perspective.

## Section 2.5: Branching Paths (Optional)

If any NPC has story paths that diverge based on player choice, define them here. Skip this section if the game has no arc-level branching (most games don't need it — use within-canvas branching for minor variations).

### Branch Points

| Branch Point Canvas | Choice A Text | Flag A | Choice B Text | Flag B | Shared Flag |
|---------------------|--------------|--------|--------------|--------|-------------|
| [canvas_id] | [choice text] | [flag_name] | [choice text] | [flag_name] | [completion_flag] |

### Path-Specific Nodes

| ID | Name | Chapter | Branch Condition | Linked Canvas | Journal Entry |
|----|------|---------|-----------------|---------------|---------------|
| [id] | [name] | [chapter] | [flag from above] | [canvas] | "[First-person reflection for THIS path]" |
| [id] | [name] | [chapter] | [other flag] | [canvas] | "[First-person reflection for OTHER path]" |

### Reconvergence

After branched content, list the shared node where paths merge:
- **Reconvergence group:** [group_id] with `required_count = 1`, containing one node per path
- **Shared continuation node:** [node_id] with `requires_group = "[group_id]"`

### Content Budget

Each branch point doubles the content needed for that segment:
- 1 branch point = 2 path variants
- 2 branch points = 4 path variants
- Recommend maximum 1-2 branch points per NPC

## Section 3: Groups

"Complete N of M" parallel activity requirements:

| ID | Name | Required Count | Member Nodes |
|----|------|----------------|-------------|
| early_bonding | Getting to Know Her | 2 | first_breakfast, first_peek, first_movie |
| mid_bonding | Growing Connection | 1 | first_massage, deep_talk, bath_invitation |

## Section 4: Emotion Mappings

Map stat ranges to human-readable labels AND behavioral descriptions:

### [Primary Stat Name]
| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 20 | strangers | "[Emotional description]" | "[How she acts: body language, dialogue style, physical distance]" |
| 21 | 40 | warming | "[Emotional description]" | "[Specific behavioral shifts from previous range]" |
| 41 | 60 | attraction | "[Emotional description]" | "[The tension is visible now — describe how]" |
| 61 | 80 | intimate | "[Emotional description]" | "[She's choosing this openly — describe how]" |
| 81 | 100 | in love | "[Emotional description]" | "[Complete emotional availability — describe how]" |

### Trust
| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 10 | guarded | "[Emotional description]" | "[Walls up — specific behaviors]" |
| 11 | 20 | cautious | "[Emotional description]" | "[Testing — specific behaviors]" |
| 21 | 30 | trusting | "[Emotional description]" | "[Opening up — specific behaviors]" |
| 31 | 40 | safe | "[Emotional description]" | "[Vulnerable — specific behaviors]" |
| 41 | 50 | complete | "[Emotional description]" | "[Fully trusting — specific behaviors]" |

### Cross-State Descriptions (REQUIRED)

Define how the NPC behaves at KEY stat combinations that the player
will encounter during the game, especially during/after crisis events:

| Primary | Trust | Quadrant | Description |
|---------|-------|----------|-------------|
| 0-20 | 0-10 | DISTANT | "[She's a stranger who shares your kitchen. Polite. Nothing more.]" |
| 0-20 | 11-20 | SAFE | "[She likes having you around. You're good company. That's all.]" |
| 21-40 | 0-10 | CONFLICTED | "[She watches you when she thinks you're not looking. But she won't come closer.]" |
| 21-40 | 11-20 | WARMING | "[Something is shifting. She lingers at breakfast. Her smiles last longer.]" |
| 41-60 | 11-16 | CRISIS | "[She wants you. You can see it. But something broke, and she won't let you close until it's fixed.]" |
| 41-60 | 20-30 | OPEN | "[The air between you is charged. She stopped pretending otherwise.]" |
| 61-80 | 24-35 | DEEP OPEN | "[She chose this. She chose you. Every touch is deliberate.]" |
| 81-100 | 35-50 | COMPLETE | "[Home isn't the apartment anymore. Home is wherever she is.]" |

Note: The CRISIS cross-state (high primary / low trust) is the most important
description because it captures the NPC in the CONFLICTED quadrant where
primary stat is high but trust has dropped. The entire crisis recovery arc
takes place in this emotional space.

### Emotional Transition Moments (REQUIRED)

Define the EXACT MOMENT when the NPC crosses from one emotional state to
another. These become the most memorable lines in the game:

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time she initiates conversation | "How was work?" (she's never asked before) |
| SAFE → WARMING | First charged moment | She holds eye contact a beat too long, then looks away smiling |
| WARMING → ATTRACTION | First acknowledgment of tension | "We should probably... I mean... goodnight." |
| ATTRACTION → INTIMATE | First physical initiative from her | She reaches for his hand. Deliberate. |
| INTIMATE → IN LOVE | First time she says what she feels | "I didn't expect this. Any of this. But I'm glad." |
| OPEN → CONFLICTED (crisis) | The moment trust shatters | Her face changes. The warmth drains. "How long?" |
| CONFLICTED → OPEN (recovery) | The moment she chooses to come back | "I was so scared. Not of you. Of how much I need this." |

## Section 5: Guidance Hints

Structured hints that help stuck players:

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: chores_explained | "Maybe Angela mentioned something about helping around the house..." |
| missing_flag: job_started | "There might be work opportunities in the neighborhood." |
| missing_trait: love (gap >= 20) | "Spending time together — breakfasts, movies — might bring you closer." |
| missing_trait: trust (gap >= 15) | "Helping around the house and being reliable builds trust." |
| (default) | "There might be more moments to share with [NPC]..." |
| (complete) | "Your journey with [NPC] has reached its beautiful conclusion." |

---

===============================================================================
                         FINAL COMPILATION
===============================================================================

Assemble all phases into `final_book.md`:

1. Foundation (from Phase 1)
2. Characters & Stats (from Phase 2)
3. World Design (from Phase 3)
4. Story Events (from Phase 4)
5. Activities (from Phase 5)
6. Story Arc (from Phase 6)
7. Clip Library (from Phase 0, if completed)
8. Quality Checklist results

---

===============================================================================
                         QUALITY CHECKLIST
===============================================================================

Before finalizing, verify:

## Story Quality
□ Central tension defined as a single emotional question
□ NPC has at least 2 internal contradictions that drive story events
□ NPC resistance pattern defined (mild → moderate → severe → recovery)
□ At least 2 tension/crisis events where stats DROP
□ Major crisis threatens to END the relationship (not just slow it)
□ Major crisis takes 2-4 in-game days to resolve (not one scene)
□ At least 3 story events have TRADE-OFF or SACRIFICE choices
□ At least 1 choice results in NEGATIVE stat consequences
□ At least 2 bridge events exist purely for character development
□ Tension curve alternates: escalation → tension → recovery → escalation
□ NPC shows fundamentally changed behavior in Act 3 vs Act 1
□ Escalation progression is logical and incremental:
  peek/glimpse → kiss/touch → groping/foreplay → oral → sex
□ Each gate feels EARNED through preceding drama, not just stat threshold
□ Post-crisis intimacy feels deeper than pre-crisis intimacy
□ Fantasy is clear and compelling
□ NPC feels like a real person with internal depth
□ Choices have meaning (different stat outcomes AND narrative consequences)

## Branching Quality (if applicable — skip if no arc-level branching)
□ Branch-point canvas sets DIFFERENT flags per choice (not the same flag)
□ Branch-point canvas also sets a SHARED completion flag for the story arc milestone
□ branch_condition values match exactly the flags set by the branch-point canvas
□ All branching paths reconverge on shared nodes via group with required_count=1
□ No more than 2 branch points per NPC
□ Path-specific journal entries reflect the specific path's tone and events
□ Both paths have roughly equal content volume (no "lesser" path)

## Emotional Flow Quality
□ NPC emotional quadrant behaviors defined (DISTANT, SAFE, CONFLICTED, OPEN)
□ Emotional tells defined for each primary stat range (0-20, 21-40, etc.)
□ Emotional tells defined for each trust range
□ Cross-state descriptions include the CRISIS state (high primary / low trust)
□ Transition moments defined for each major emotional shift
□ At least one scene per quadrant exists in the story event chain
□ Activity base scenes include emotional state awareness (not same tone always)
□ Post-crisis NPC behavior is noticeably different from pre-crisis (deeper)
□ The CONFLICTED quadrant explored for at least 2-3 in-game days during crisis
□ NPC emotional flow follows quadrant map: DISTANT → SAFE → OPEN → CONFLICTED → OPEN
□ The CONFLICTED → OPEN recovery is the most powerful transition in the game

## Player Character Quality
□ Player has defined want/need/fear/flaw (not just stats and backstory)
□ Player emotional phases defined (at least 5 phases from arrival to belonging)
□ Player phase transitions tied to specific story events (not arbitrary)
□ Player internal voice changes across phases (early observations vs late emotional investment)
□ "What player notices" evolves — from environment (early) to NPC details (mid) to relationship meaning (late)
□ "How player describes NPC" shifts — from physical (early) to emotional (mid) to intimate (late)
□ Choice text framing reflects player phase (cautious early → emotionally honest late)
□ Player has a parallel crisis arc (not just watching NPC's crisis)
□ Player crisis stages defined (guilt → helplessness → resolve → vulnerability → certainty)
□ Activity scenes show player internal state, not just NPC behavior
□ Player growth is visible in narration — sentence length, vocabulary, emotional specificity increase
□ Player character feels like a person with his own journey, not just a camera following the NPC

## Scene Quality
□ Each scene has clear narrative purpose
□ Video descriptions are specific and explicit where needed
□ Clip UUIDs assigned where available
□ Search queries provided for external sources
□ Progression makes logical emotional sense
□ No gaps in the experience

## Technical Quality
□ All IDs are consistent (loc_, npc_ prefixes)
□ Trigger conditions are logical and achievable
□ Stat thresholds are reachable through normal play
□ Flag chains form a complete dependency graph
□ Gate flags correctly assigned to story events

## Activity Quality
□ NPC activities cover multiple time slots
□ Utility canvases present (chores, jobs, rest)
□ Economic loop is viable (player can afford rent)
□ Each NPC activity has base scene + gated choices
□ Choice thresholds use hybrid gating (stat-only for low, stat+flag for high)
□ Not all activities forced to reach sex — cap where narratively appropriate
□ Canvas balance: ~40-50% activities, ~35-40% story events, ~10-15% utility

## Video Integration Quality (if Phase 0 completed)
□ All integrated clips assigned to Activity, Story, or Shared
□ First-time energy clips reserved for story milestones
□ Gate-setting scenes have video integration
□ Clip library includes all assigned UUIDs
□ External source markers for non-integrated tiers
□ Coverage gaps documented
□ session_state.yaml updated

## Gate System Quality (Single-NPC)
□ 3-5 gates defined with designer-chosen milestones
□ Each gate set by a specific story event
□ Hybrid gating model applied to all NPC activities
□ Gates unlock content across ALL activities simultaneously
□ Gate timeline is achievable through normal play

## Multi-NPC Architecture Quality (if applicable)
□ Game architecture explicitly chosen (Multi-NPC Parallel Arcs)
□ Player corruption is the primary progression driver
□ Corruption bands overlap — 2-3 active arcs at every corruption level
□ No dead zones where player has nothing to do
□ Shared unlock flags defined and assigned to specific arc events
□ Shared unlock flags work across ALL arcs (cross-arc consistency)
□ Linear opening (~8 canvases) establishes world before branching
□ Inciting event clearly marks transition from linear → open world
□ Economic math forces escalation organically (base tier < rent)
□ Random encounters add appropriate small corruption increments (+2-3)
□ Clothing tiers match TOML conditions exactly (shop UI = TOML thresholds)
□ Each arc has its own flag chain with staggered corruption entry points
□ NPC stats (love/trust) gate NPC-specific scenes, not shared activities

## Content Balance
□ Activity videos distributed across locations and time slots
□ Story events: ~35-40% of total canvases
□ Economic pressure creates meaningful time trade-offs
□ Player can reach key stat thresholds by target days
□ days_since_flag pacing prevents narrative compression

### NPC Customization Checklist
- [ ] Customizable NPCs have `customizable = true`, `relationship`, and `relationship_options`
- [ ] Default `relationship` value appears in `relationship_options` list
- [ ] ALL paragraph/heading content uses `@npc_short` syntax for customizable NPCs — zero hardcoded names
- [ ] Emotion mapping descriptions use `@`-syntax for NPC names
- [ ] Relationship options are narratively compatible (same text works for all options)
- [ ] Maximum 1-2 customizable NPCs per game

---

END OF PROMPT
```

--- END OF GAME BOOK PROMPT v6 ---

---


## 4. TOML Generation Prompt (v3)

This prompt translates Game Design Books into structured TOML files. It defines a 5-phase pipeline with 12 reference patterns (A-L) covering every canvas type: standard activities, dual-path, utility, jobs, time advancement, story events, gate-setting, economic, random encounters, multi-NPC arcs, clothing, and rent systems.

```
# ═══════════════════════════════════════════════════════════════════════════════
#                    TOML GENERATION PROMPT — VERSION 3.0
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE: Translate a Game Design Book (markdown) into structured TOML
#          consumed by the Django game engine (template_import.py).
#
# PHILOSOPHY: Schema-aligned translator using reference-game patterns.
#             You are a TRANSLATOR, not a designer. The Book contains all
#             creative decisions. Your job is faithful structural conversion.
#
# KEY CHANGES FROM V2:
#   - Multi-NPC parallel arc support (staggered corruption bands, shared unlock flags)
#   - [settings] schema: clothing_enabled, wardrobe_location, shop_location
#   - [settings.clothing_requirements]: body_coverage, conditional slot relaxation
#   - [settings.rent]: recurring rent system
#   - [[clothing]] schema: corruption-tiered wardrobe items
#   - trigger_mode + chance fields for random encounter canvases
#   - wardrobeEffects for story-driven clothing gifts
#   - loop_terminal on exit_block for activity loop control
#   - New patterns I-L: Random Encounters, Parallel Arcs, Clothing, Rent
#   - Multi-NPC phase instructions (Sections 8-10)
#   - Common mistakes 15-18 for new features
#
# PRESERVED FROM V2:
#   - Single-canvas activities with gated choices
#   - Designer-chosen gate flags (flexible, not hardcoded)
#   - Clean 5-phase pipeline
#   - Schema derived from actual engine code (template_import.py)
#   - ONE canonical example per pattern
#   - All contradictions resolved
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 1: ROLE & RULES
# ═══════════════════════════════════════════════════════════════════════════════
#
# You are a GAME IMPLEMENTATION ENGINEER.
#
# Your input: A Game Design Book (markdown document, ~50-80 pages)
# Your output: Structured TOML files that the game engine can parse
#
# CORE RULES:
#
# 1. TRANSLATOR, NOT CREATOR
#    - Extract structure from the Book. Do NOT invent content.
#    - If the Book says "3 locations", create 3 locations. Not 5.
#    - If the Book describes a scene with 4 paragraphs, use those 4 paragraphs.
#    - Preserve all clip UUIDs, video files, and media references exactly.
#
# 2. PHASED WORKFLOW
#    - Work through phases 1-5 sequentially.
#    - After each phase, present output and wait for "proceed" before continuing.
#    - Each phase produces a separate TOML file.
#
# 3. INCREMENTAL OUTPUT
#    - Write each section to file as you complete it.
#    - Do not accumulate large outputs in memory.
#    - Show progress: "Phase 1: 3/5 locations written..."
#
# 4. ERROR HANDLING
#    - Auto-fix simple issues (missing defaults, case normalization).
#    - For ambiguities, present options: "Book says X, but schema requires Y.
#      Option A: ... Option B: ... Which do you prefer?"
#    - Never silently drop content.
#
# 5. SCHEMA IS LAW
#    - If the Book describes something the schema doesn't support, flag it.
#    - If the schema has a field the Book doesn't mention, use the default.
#    - The schema in Section 4 is derived from the actual parser code.
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 2: PHASE FILE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
#
# The TOML is built in 5 phases + final compilation.
# Each phase produces one file. Phase 5 validates. Phase F compiles.
#
# ┌───────┬──────────────────────────────┬───────────────────────┬──────────────────────────────┐
# │ Phase │ Output File                  │ Book Input            │ TOML Sections                │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   1   │ 1_metadata_and_locations.toml│ Book Phases 1-3       │ schema_version, project,     │
# │       │                              │ (Foundation,          │ time, player, npcs,          │
# │       │                              │  Characters, World)   │ locations                    │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   2   │ 2_story_canvases.toml        │ Book Phase 4          │ starting_canvas +            │
# │       │                              │ (Story Events)        │ all one-time event canvases  │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   3   │ 3_activities.toml            │ Book Phase 5          │ All activity canvases        │
# │       │                              │ (Activities)          │ (NPC, solo, utility)         │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   4   │ 4_story_arc.toml             │ Book Phase 6          │ story_arc section            │
# │       │                              │ (Story Arc)           │ (chapters, nodes, groups,    │
# │       │                              │                       │  emotion_mappings, hints)    │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   5   │ (no file — validation pass)  │ All phases            │ Cross-reference validation,  │
# │       │                              │                       │ auto-fixes, error report     │
# ├───────┼──────────────────────────────┼───────────────────────┼──────────────────────────────┤
# │   F   │ 6_final_game.toml            │ All TOML phases       │ Complete compiled game file  │
# └───────┴──────────────────────────────┴───────────────────────┴──────────────────────────────┘
#
# WHY THIS ORDER:
# - Phase 1 (metadata/locations) first: everything else references these IDs
# - Phase 2 (story canvases) second: they SET gate flags
# - Phase 3 (activities) third: they CONSUME gate flags in conditions
# - Phase 4 (story arc) fourth: references canvas IDs from phases 2-3
# - Phase 5 (validation): catches cross-reference errors across all phases
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 3: TOML SCHEMA REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
#
# THIS IS THE GROUND TRUTH. Every field below exists in the engine's parser
# (template_import.py). Fields not listed here will be IGNORED by the engine.
#
# Legend:
#   [R] = Required (parser raises error if missing)
#   [D] = Has default (omitting is safe)
#   Type shown in parentheses
#
# ─────────────────────────────────────────────────────────────────────────────
# 3a. ROOT LEVEL
# ─────────────────────────────────────────────────────────────────────────────
#
# schema_version (string) [D: "0.2"]
#   - Use "0.2" for canvas-based games (our standard)
#
# starting_canvas (string) [R if canvases exist]
#   - ID of the first canvas shown when game starts
#   - Must match a [[canvases]] id exactly
#   - Can be in root OR in [project] section (parser checks both)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3b. [project]
# ─────────────────────────────────────────────────────────────────────────────
#
# [project]
# id          (string) [R] — lowercase_snake_case, stored as slug
# title       (string) [R] — human-readable game title
# description (string) [D: ""]
#
# Example:
# [project]
# id = "jacks_world"
# title = "Jack's World"
# description = "An intimate story of connection and trust"
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3c. [time]
# ─────────────────────────────────────────────────────────────────────────────
#
# [time]
# enabled       (bool)   [D: true]   — enable time system
# starting_hour (int)    [D: 8]      — 0-23, game starts at this hour
# starting_day  (string) [D: "Monday"] — must be valid weekday name
# starting_week (int)    [D: 1]      — must be >= 1
#
# Example:
# [time]
# enabled = true
# starting_hour = 8
# starting_day = "Monday"
# starting_week = 1
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3d. [player]
# ─────────────────────────────────────────────────────────────────────────────
#
# [player]
# id          (string)       [D: "player"]  — lowercase_snake_case
# name        (string)       [D: "Player"]  — display name
# description (string)       [D: ""]
# portrait    (string)       [D: ""]        — image path
# core_traits (dict)         [D: {}]        — starting stat values
# flag_keys   (list[string]) [D: []]        — ALL flags used in game
#
# IMPORTANT: core_traits contains the player's OWN stats.
# NPC stats (love, trust) go on the NPC, not the player.
# Player stats are things like: money, energy, confidence
#
# IMPORTANT: flag_keys must list EVERY flag referenced anywhere in the
# game — canvas triggers, choice conditions, flagEffects. This is the
# master flag registry.
#
# Example:
# [player]
# id = "jack"
# name = "Jack"
# description = "A young man starting over"
# core_traits = { money = 50 }
# flag_keys = [
#   "game_started",
#   "first_rent_paid",
#   "rent_last_paid",
#   "kiss_unlocked",
#   "groping_unlocked",
#   "oral_unlocked",
#   "sex_unlocked",
#   "towel_encounter_complete",
#   "first_kiss_complete",
#   "massage_offered",
#   "job_started",
#   "chores_explained",
#   "peek_unlocked"
# ]
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3e. [[npcs]]
# ─────────────────────────────────────────────────────────────────────────────
#
# [[npcs]]
# id          (string)       [R] — lowercase_snake_case, unique
# name        (string)       [R] — display name
# description (string)       [D: ""]
# portrait    (string)       [D: ""] — image path
# core_traits (dict)         [D: {}] — starting stat values for THIS NPC
# flag_keys   (list[string]) [D: []] — NPC-specific flags (rarely used)
# customizable (bool)        [D: false] — if true, player can rename this NPC and pick relationship at game start
# relationship (string)      [D: ""] — default relationship label (e.g., "step-brother", "roommate")
# relationship_options (list[string]) [D: []] — available relationship choices for the player
#
# When customizable = true, the game shows a customization screen at start where the player
# can change this NPC's display name and select a relationship from relationship_options.
#
# NPC SCHEDULES: REMOVED — Do NOT define [[npcs.schedules]].
# NPC presence at locations is determined entirely by canvas triggers.
# If a canvas triggers at loc_kitchen with npc = "npc_angela", Angela is
# shown as present at that location during that schedule window.
# The portrait field is used to render clickable NPC portraits at locations.
#
# Example:
# [[npcs]]
# id = "npc_angela"
# name = "Angela"
# description = "Your landlady. Guarded but kind."
# portrait = "angela_white/portrait.jpg"
# core_traits = { love = 0, trust = 0 }
# flag_keys = []
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3f. [[locations]]
# ─────────────────────────────────────────────────────────────────────────────
#
# [[locations]]
# id                   (string)       [R] — lowercase_snake_case, unique
# name                 (string)       [R]
# description          (string)       [D: ""]
# image                (string)       [D: ""] — background image path
# image_search_queries (list[string]) [D: []] — queries for missing media page
# is_container         (bool)         [D: false] — if true, holds sub-locations
# parent               (string)       [D: ""] — parent location ID
# entry_from           (string)       [D: ""] — which location connects here
# default_entry        (string)       [D: ""] — default sub-location for containers
# navigation_order     (list[string]) [D: []] — ordered list of child location IDs
#
# LOCATION HIERARCHY:
# - Top-level locations have no parent and no entry_from
# - Sub-locations set entry_from to their parent's ID
# - Containers set is_container = true and default_entry to a child
# - navigation_order controls the display order of children
#
# CYCLE DETECTION: The engine detects cycles in entry_from chains.
# A -> B -> C -> A will be rejected.
#
# Example:
# [[locations]]
# id = "loc_kitchen"
# name = "Kitchen"
# description = "The heart of the house"
# image = "locations/kitchen.jpg"
# image_search_queries = ["kitchen interior warm lighting"]
# entry_from = "loc_hallway"
#
# Container Example (multi-level hierarchy):
# [[locations]]
# id = "loc_the_bar"
# name = "The Bar"
# description = "A dimly lit bar on the edge of town"
# image = "locations/bar_exterior.jpg"
# is_container = true
# default_entry = "loc_bar_floor"
# navigation_order = ["loc_bar_floor", "loc_stockroom", "loc_bar_upstairs"]
#
# [[locations]]
# id = "loc_bar_floor"
# name = "Bar Floor"
# description = "The main floor with stools and neon lights"
# entry_from = "loc_the_bar"
#
# [[locations]]
# id = "loc_stockroom"
# name = "Stockroom"
# description = "Cramped shelves and dim lighting"
# entry_from = "loc_the_bar"
#
# [[locations]]
# id = "loc_bar_upstairs"
# name = "Upstairs"
# description = "Private rooms above the bar"
# entry_from = "loc_the_bar"
#
# CONTAINER RULES:
# - The container (loc_the_bar) sets is_container = true
# - default_entry points to the sub-location the player enters first
# - navigation_order lists children in display order
# - Each child sets entry_from to the container's ID
# - Canvases trigger at the CHILD locations, not the container
#   (e.g., bar work triggers at loc_bar_floor, not loc_the_bar)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3f-settings. [settings]
# ─────────────────────────────────────────────────────────────────────────────
#
# [settings]
# clothing_enabled      (bool)   [D: false]  — enable clothing/wardrobe system
# wardrobe_location     (string) [D: ""]     — location slug for wardrobe changes
# shop_location         (string) [D: ""]     — location slug for clothing shop
#
# [settings.clothing_requirements]
# body_coverage         (bool)         [D: true]  — must wear top+bottom OR dress
# always_required       (list[string]) [D: []]    — slots always needed (e.g., ["shoes"])
#
# [settings.clothing_requirements.conditional.<slot>]
# until_flag  (string) — flag that removes this requirement when set
# message     (string) — error message if slot empty and flag not set
#
# Example:
# [settings.clothing_requirements.conditional.bra]
# until_flag = "comfortable_braless"
# message = "You're not comfortable going without a bra yet"
#
# [settings.rent]
# enabled        (bool)    [D: false]
# amount         (int)     [D: 0]        — dollars per period
# due_day        (string)  [D: "Monday"] — day of week rent is due
# collector_npc  (string)  [D: ""]       — NPC slug who collects rent
# grace_periods  (int)     [D: 1]        — number of missed payments before consequences
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3f-clothing. [[clothing]]
# ─────────────────────────────────────────────────────────────────────────────
#
# [[clothing]]
# id          (string)  [R]             — unique identifier
# name        (string)  [R]             — display name
# slot        (string)  [R]             — bra, underwear, top, bottom, dress, legwear, shoes
# image       (string)  [D: ""]         — image path
# initial     (bool)    [D: false]      — player starts with this item
# price       (int)     [D: 0]          — shop price (0 = not buyable / free)
# conditions  (dict)    [D: {}]         — same schema as conditions elsewhere
#
# Clothing items use conditions to gate by corruption or other stats:
# [[clothing]]
# id = "mini_skirt"
# name = "Mini Skirt"
# slot = "bottom"
# price = 80
# conditions = { version = "1.0", items = [
#   { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 85 }
# ] }
#
# CRITICAL: Shop UI tier thresholds MUST match conditions values exactly.
# If conditions say corruption >= 85, the shop must label it "Bold (85+)".
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3g. [[canvases]]
# ─────────────────────────────────────────────────────────────────────────────
#
# [[canvases]]
# id          (string) [R] — lowercase_snake_case, unique
# name        (string) [R] — display name
# description (string) [D: ""]
#
# ─── [canvases.trigger] (optional — OMIT for starting canvas) ────
#
# [canvases.trigger]
# location             (string)  [R]       — location ID where this fires
# is_active            (bool)    [D: true]
# is_repeatable        (bool)    [D: true] — false for one-time events
# max_triggers_per_day (int|nil) [D: nil]  — nil = unlimited
# priority             (int)     [D: 0]    — higher wins when multiple valid
# npc                  (string)  [D: nil]  — NPC slug for navigation indicator
# trigger_mode         (string)  [D: "manual"] — "manual" or "random"
# chance               (float|nil) [D: nil]    — 0.0-1.0, only for trigger_mode="random"
# costs                (list)    [D: []]   — resource costs deducted on canvas entry
#
# COSTS: Each item has {trait, value}. Player must have trait >= value to enter.
# If not met, activity is VISIBLE but blocked ("Requires 20 Energy").
# Cost is auto-deducted on entry. Story events (is_repeatable=false) should NOT have costs.
#
#   costs = [{ trait = "energy", value = 20 }]
#
# ENERGY COST TIERS (by activity intensity):
#   0    = Free (restorative: sleep, shower, passive: phone scroll)
#   5    = Minimal (journal, get ready, wander)
#   10   = Light (meals, brief social: breakfast, lunch, goodnight)
#   15   = Moderate-light (dinner, movie, video games)
#   20   = Moderate (cooking, wine talk, planning, emotional scenes)
#   25   = Heavy (chores, manual labor)
#   30   = Very heavy (pool, sports, extended physical)
#
# ENERGY REGENERATION (via effects on exit choices):
#   Full sleep:  op = "set", value = 100  (reset to max)
#   Nap:         op = "add", value = 20
#   Shower:      op = "add", value = 5-10
#   Meal T1:     op = "add", value = 5-10  (breakfast/lunch +5, dinner +10)
#
# MEAL RESTORATION PATTERN:
#   Meal activities (breakfast, lunch, dinner) have NO costs (free to enter).
#   T1 exit choice adds energy restoration alongside base love/trust gains.
#   T2+ choices give love/trust only — no energy restore.
#   Trade-off: eat at T1 for recovery, or pick higher tier for more love.
#
# EFFECT VALUE GUIDE (new trait system):
#   Emotional choices:  love +3, trust +2  (conversation, comfort, support)
#   Physical choices:   love +1, corruption (NPC) +3-8, corruption (player) +2-6
#                       (higher tiers give higher corruption gains)
#   Neutral choices:    love +1, trust +3  (helping, sharing, being present)
#
# ENDING CONDITION THRESHOLDS (best ending):
#   love >= 90, trust >= 75, corruption >= 85
#   These are checked on NPC traits (love, trust) and player trait (corruption).
#
# SIDEBAR ENERGY DISPLAY:
#   [[sidebar_items]]
#   type = "trait_bar"
#   trait = "energy"
#   label = "Energy"
#   max = 100
#
# SIDEBAR ITEM TYPES:
#   "countdown"  — days remaining (total_days, label)
#   "trait_bar"  — visual bar for a player trait (trait, label, max)
#   "hint"       — contextual hint text
#
# RANDOM ENCOUNTERS: Set trigger_mode = "random" with a chance value.
# The canvas fires probabilistically when the player enters the location.
# Use for passive witnessing events (no player choice to engage).
# Example: trigger_mode = "random", chance = 0.7 (70% chance per visit)
#
# [canvases.trigger.conditions]  (dict) [D: {}]
#   — See Section 3k for conditions schema
#
# [[canvases.trigger.schedules]] (list) [D: []]
#   weekdays   (list[int]) [R] — 0=Monday..6=Sunday
#   start_time (string)    [R] — "HH:MM" format
#   end_time   (string)    [D: nil] — "HH:MM" or omit for open-ended
#
# PRIORITY GUIDE:
#   10  = Story events (one-time, must fire when conditions met)
#    6-8 = Special activities (uncommon situations)
#    2  = Economic events (rent, payments)
#    1  = Regular repeatable activities (breakfast, bath)
#    0  = Default / fallback
#
# TRIGGER OMISSION: The starting canvas (referenced by starting_canvas)
# must NOT have a trigger section. It fires once at game start.
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3h. [[canvases.nodes]]
# ─────────────────────────────────────────────────────────────────────────────
#
# [[canvases.nodes]]
# id         (string)         [R] — lowercase_snake_case, unique within canvas
# name       (string)         [R] — display name (REQUIRED, not optional!)
# blocks     (list[dict])     [D: []] — content blocks (see 3l)
# exit_block (dict)           [D: location-type exit] — see 3i
#
# Every node MUST have: id, name, blocks, exit_block.
# If exit_block is omitted, it defaults to type="location" with
# destinationType="trigger" (returns to world).
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3i. EXIT BLOCK TYPES (ONLY TWO)
# ─────────────────────────────────────────────────────────────────────────────
#
# There are exactly TWO valid exit_block types:
#
# ── TYPE 1: "location" ──
# Single-button exit. Player clicks and goes somewhere.
#
# exit_block = { type = "location", text = "Continue",
#   config = {
#     destinationType = "trigger",        # or "specific"
#     locationId = "loc_kitchen",          # only if destinationType = "specific"
#     time_progression_minutes = 30,
#     effects = [ ... ],                  # stat changes
#     flagEffects = [ ... ]               # flag changes
#   }
# }
#
# ── TYPE 2: "choices" ──
# Multiple-choice exit. Player picks from a list.
#
# exit_block = { type = "choices", choices = [
#   { text = "Option A", targetType = "trigger", ... },
#   { text = "Option B", targetType = "node", nodeId = "canvas.node", ... }
# ] }
#
# CRITICAL: There is no type = "node", type = "trigger", or type = "canvas".
# Only "location" and "choices".
#
# ── LOOP TERMINAL ──
# exit_block can include: loop_terminal (bool) [D: false]
# Marks this node as the loop terminal for repeatable activity canvases.
# When loop_terminal = true, the engine knows this is the highest-escalation
# exit point and handles loop control accordingly.
#
# Example: exit_block = { type = "location", text = "Leave", loop_terminal = true,
#   config = { destinationType = "trigger", time_progression_minutes = 60 } }
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3j. CHOICE FIELDS
# ─────────────────────────────────────────────────────────────────────────────
#
# Each choice in a type="choices" exit_block has these fields:
#
# text                    (string)       [D: "Continue"] — button label
# targetType              (string)       [D: "trigger"]  — where choice goes
# locationId              (string|nil)   [D: nil]        — for targetType="location"
# nodeId                  (string|nil)   [D: nil]        — for targetType="node"
# time_progression_minutes (int|nil)     [D: nil]        — minutes to advance
# effects                 (list[dict])   [D: []]         — stat changes
# flagEffects             (list[dict])   [D: []]         — flag changes
# conditions              (dict)         [D: {}]         — visibility conditions
#
# targetType VALUES:
#   "trigger"  — returns to location trigger system (most common)
#   "location" — goes to specific location (requires locationId)
#   "node"     — goes to specific node (requires nodeId)
#
# nodeId FORMAT for cross-canvas references: "canvas_id.node_id"
#   Example: nodeId = "activity_breakfast_angela.warm"
#
# CONDITIONS ON CHOICES:
# When a choice has conditions, it is HIDDEN from the player unless all
# conditions are met. This is the core mechanic for gated content:
# the base "leave" choice is always visible, while escalation choices
# appear only when the player has sufficient stats/flags.
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3j-effects. EFFECT FIELDS
# ─────────────────────────────────────────────────────────────────────────────
#
# Each effect in the effects array:
#
# targetType (string) [D: "player"] — "player" or "npc"
# npcId      (string) [D: nil]      — required if targetType = "npc"
# trait      (string) [D: ""]       — trait name to modify
# op         (string) [D: "add"]    — "add" or "set"
# value      (any)    [D: 0]        — amount to add or value to set
# clamp      (bool)   [D: nil]      — if false, allows negative results
# cap        (any)    [D: nil]      — maximum cap for the trait
#
# Examples:
# { targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 2 }
# { targetType = "player", trait = "money", op = "add", value = -200, clamp = false }
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3j-flags. FLAG EFFECT FIELDS
# ─────────────────────────────────────────────────────────────────────────────
#
# Each flagEffect in the flagEffects array:
#
# targetType (string) [D: "player"] — "player" or "npc"
# npcId      (string) [D: nil]      — required if targetType = "npc"
# flag       (string) [D: ""]       — flag name to set to true
#
# Setting a flag means: the player has reached this milestone.
# Flags are checked via conditions (type = "flag") elsewhere.
# Flags are also used by days_since_flag conditions for time pacing.
#
# Example:
# { targetType = "player", flag = "first_kiss_complete" }
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3j-wardrobe. WARDROBE EFFECT FIELDS
# ─────────────────────────────────────────────────────────────────────────────
#
# wardrobeEffects appear alongside effects and flagEffects on exit_blocks
# and choices. They add or equip clothing items during story events.
#
# wardrobeEffects  (list[dict]) [D: []]
#   action   (string) [D: "add"]  — "add" (add to inventory) or "equip" (add + equip)
#   item_id  (string) [R]         — references a [[clothing]] id
#
# CRITICAL: Every item_id must match an existing [[clothing]] id exactly.
#
# Example (NPC gifts lingerie during a story event):
# exit_block = { type = "location", text = "Take the gift", config = {
#   destinationType = "trigger",
#   time_progression_minutes = 15,
#   effects = [{ targetType = "npc", npcId = "npc_mick", trait = "love", op = "add", value = 3 }],
#   flagEffects = [{ targetType = "player", flag = "mick_gift_complete" }],
#   wardrobeEffects = [{ action = "add", item_id = "lace_bra" }]
# } }
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3k. CONDITIONS SCHEMA
# ─────────────────────────────────────────────────────────────────────────────
#
# Conditions appear in two places:
#   1. [canvases.trigger.conditions] — controls when a canvas fires
#   2. choice.conditions — controls when a choice is visible
#
# Both use the SAME schema:
#
# conditions = {
#   version = "1.0",             # always "1.0"
#   logic = "AND",               # "AND" (default) or "OR"
#   items = [
#     { type = "flag", ... },
#     { type = "trait", ... },
#     { type = "days_since_flag", ... },
#     { type = "clothing_slot", ... }, { type = "clothing_item", ... },
#     { type = "worn_beauty", ... },  { type = "worn_corruption", ... },
#     { type = "pass", ... }, { type = "item", ... }, { type = "stage", ... }
#   ]
# }
#
# If there is only one item, you may omit `logic`.
#
# ── CONDITION ITEM TYPES ──
#
# TYPE: "flag"
# { type = "flag", subject = "player", flag_key = "kiss_unlocked", operator = "is_true" }
#   subject   — "player" or "npc"
#   npc_id    — required if subject = "npc" (note: npc_id, not npcId)
#   flag_key  — the flag name
#   operator  — "is_true", "is_false", or "exists"
#
# TYPE: "trait"
# { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 22 }
#   subject   — "player" or "npc"
#   npc_id    — required if subject = "npc"
#   trait_key — the trait name
#   operator  — "eq", "ne", "gt", "gte", "lt", "lte"
#   value     — numeric threshold
#
# TYPE: "days_since_flag"
# { type = "days_since_flag", subject = "player", flag_key = "first_kiss_complete", operator = "gte", value = 2 }
#   subject   — "player" or "npc"
#   npc_id    — required if subject = "npc"
#   flag_key  — the flag whose set-date is compared
#   operator  — "gte", "gt", "lte", "lt", "eq"
#   value     — number of in-game days
#
# TYPE: "worn_corruption" / "worn_beauty"  (requires clothing system enabled)
# { type = "worn_corruption", operator = "gte", value = 30 }
#   operator  — "eq", "ne", "gt", "gte", "lt", "lte"
#   value     — numeric threshold
#   Reads the MAX corruption/beauty across the currently-equipped outfit (one
#   daring garment drives it; layering does not sum). ROUTES content only —
#   does NOT touch the global player.corruption trait. When clothing is
#   disabled the condition is always false. NOTE: worn_* are valid in v1.0
#   `conditions` blocks (canvas triggers, choices, location clothing_rules),
#   NOT in hint-template `trait_checks` (which allow only trait/flag).
#
# OTHER LIVE TYPES (see the relevant system sections): "clothing_slot",
# "clothing_item", "pass", "item", "stage".
#
# NOTE ON FIELD NAMING: Inside conditions, NPC references use npc_id
# (snake_case). Inside effects, they use npcId (camelCase). This is
# intentional — the engine parser handles both formats.
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3l. BLOCK TYPES
# ─────────────────────────────────────────────────────────────────────────────
#
# Each block in a node's blocks array is a dict with:
#   type    (string) — block type name
#   content (string) — text content (for paragraph, heading, dialog)
#   props   (dict)   — additional properties (type-specific)
#   id      (string) — optional unique ID
#
# AVAILABLE BLOCK TYPES:
#
# "paragraph"
#   { type = "paragraph", content = "Narrative text here." }
#
# "heading"
#   { type = "heading", content = "Chapter Title", props = { level = 2 } }
#   props.level defaults to 1 if omitted
#
# "dialog"
#   { type = "dialog", content = "What the character says.",
#     props = { speaker = "npc", npcId = "npc_angela" } }
#   props.speaker: "player" or "npc"
#   props.npcId: required when speaker = "npc"
#
# "video"
#   { type = "video", props = {
#       file = "path/to/video.mp4",
#       url = "",
#       description = "What happens in this video",
#       search_queries = ["query for finding similar video"]
#   } }
#   At least one of file, url, or description should be set
#
# "image"
#   { type = "image", props = {
#       file = "path/to/image.jpg",
#       url = "",
#       alt = "Alt text",
#       caption = "Caption text",
#       description = "What the image shows",
#       search_queries = ["query for finding similar image"]
#   } }
#
# SEARCH_QUERIES RULES:
#   search_queries are SEARCH ENGINE QUERIES for adult content sites (PornHub GIF search).
#   They are NOT scene descriptions. The description field captures narrative context.
#   search_queries must use platform-searchable vocabulary ONLY.
#
#   ⚠️ CRITICAL: These queries will be used on PornHub GIF search.
#   PornHub ignores emotional/story words. Only physical actions and settings work.
#
#   VOCABULARY MAPPING (use these exact terms):
#
#   Actions (him → her):
#     fingering     = his hand stimulating her (NOT "manual stimulation" or "manual")
#     cunnilingus   = his mouth on her (or "eating out")
#
#   Actions (her → him):
#     handjob       = her hand on him (NOT "manual" or "hand job" with a space)
#     blowjob       = her mouth on him (or "kneeling oral")
#
#   Actions (sex positions):
#     sex, fuck      = penetration (specify position if relevant)
#     missionary     = face to face lying down
#     doggy          = from behind
#     riding         = her on top (NOT "cowgirl" — use "riding" or "girl on top")
#     standing       = both standing
#
#   Settings (PornHub indexes these — put SETTING FIRST in query):
#     kitchen, counter, couch, pool, table, shower, bed, bathroom,
#     doorway, hallway, patio, outdoor, car, office, floor, rug
#
#   FORMULA (setting FIRST — setting is hardest to match):
#     NSFW:  [setting] + [specific act] + [position/detail]
#     SFW:   [setting] + [visible action] + [who]
#
#   EXAMPLES (GOOD):
#     "men fingering girl kitchen counter"
#     "kitchen blowjob kneeling"
#     "kitchen counter sex couple"
#     "under table handjob dinner"
#     "guy eating out girl couch living room"
#     "men fingering girl pool lounger outdoor"
#     "doorway blowjob kneeling"
#     "couple kitchen cooking together"
#     "couple wine patio night"
#     "man behind woman kitchen reaching"
#
#   ⚠️ GENDER-DIRECTION RULE: For actions that can be solo/lesbian (fingering,
#   cunnilingus, touching, rubbing), ALWAYS include "men"/"guy" + "girl" in the query.
#   PornHub's "fingering" category is dominated by solo girls and lesbian content.
#   "kitchen fingering" → solo girls. "men fingering girl kitchen" → M/F couple.
#
#   EXAMPLES (BAD — never write these):
#     "manual stimulation kitchen morning light"     ← "manual stimulation" is unsearchable
#     "passionate fuck against wall urgent"           ← "passionate" and "urgent" are noise
#     "intimate touching kitchen counter morning"     ← "intimate touching" is vague
#     "emotional eye contact dinner sexual tension"   ← "emotional"/"sexual tension" on a SFW scene
#     "hand job kitchen stool counter edge"           ← wrong term: narrative says HE touches HER = fingering, not hand job
#     "cunnilingus couch night tender"                ← "tender" is banned noise word
#     "oral kitchen morning"                          ← "oral" is ambiguous — specify blowjob or cunnilingus
#     "kitchen counter fingering morning"             ← "fingering" alone returns solo/lesbian, use "men fingering girl kitchen counter"
#
#   ⚠️ BANNED WORDS (PornHub ignores these — they add noise, not signal):
#     passionate, desperate, urgent, emotional, intimate, lingering,
#     loaded, forbidden, tender, intense, bittersweet, domestic,
#     tension, longing, vulnerability, devoted, savoring, seductive,
#     sensual, secret, lazy, beautiful, gorgeous, perfect, hot
#     Also: "manual stimulation", "manual" (use "fingering" or "handjob" instead)
#     Also: "sexual tension" (use specific physical action or just "couple close")
#
#   TIER-APPROPRIATE QUERIES:
#     base/t2/t3 (SFW): Use couple/action/setting. NO sex terms at all.
#     t4 (borderline): kissing, making out, hands on body. NO explicit sex terms.
#     t5+ (NSFW): Use specific sex acts from vocabulary mapping above.
#     ⚠️ Do NOT use "sexual tension" or "foreplay" for t2/t3 — those are SFW clothed moments.
#
#   Keep queries to 3-5 words maximum.
#   Each media block should have 2 queries: primary + one fallback.
#   Setting word goes FIRST in every query.
#
# "clip"
#   { type = "clip", props = { clipId = "uuid-here" } }
#   Used for pre-defined video clips with UUIDs from the Book.
#   PRESERVE clip UUIDs exactly as written in the Book.
#
# "group" (Conditional Content Variants)
#   A container block that holds child blocks with optional conditions.
#   Consecutive groups form a VARIANT CHAIN: first matching condition wins.
#   A group without conditions is the default/fallback.
#
#   { type = "group", conditions = { version = "1.0", items = [
#     { type = "flag", subject = "player", flag_key = "kissed_last_night", operator = "is_true" }
#   ] }, blocks = [
#     { type = "paragraph", content = "He looks away when you walk in." },
#     { type = "dialog", content = "About last night...", props = { speaker = "npc", npcId = "npc_ethan" } }
#   ] }
#
#   { type = "group", blocks = [
#     { type = "paragraph", content = "Morning light. Coffee already made." },
#     { type = "dialog", content = "Morning. Sleep okay?", props = { speaker = "npc", npcId = "npc_ethan" } }
#   ] }
#
#   VARIANT CHAIN RULES:
#   - Consecutive groups = variant chain (<<if>>..<<elseif>>..<<else>>)
#   - Non-group blocks between groups break the chain
#   - Groups CAN be nested (group inside a group) — a stage gate wrapping
#     flag-gated sub-branch groups renders as a nested variant chain.
#     Bounded by the normalizer's max_depth (4). (block_pool still cannot
#     directly nest a block_pool.)
#   - Conditions use the same format as choice conditions (version 1.0)
#   - Use for: base node variations based on relationship state or past choices
#
#
# ─────────────────────────────────────────────────────────────────────────────
# NPC NAME REFERENCES IN CONTENT — @-syntax
# ─────────────────────────────────────────────────────────────────────────────
#
# In paragraph, heading, and dialog content blocks, use @-references to insert
# NPC names dynamically instead of hardcoding them. This is REQUIRED for
# customizable NPCs and RECOMMENDED for all NPCs.
#
#   @ethan       → prints the NPC's current name (resolves from npc_ethan)
#   @ethan.rel   → prints the NPC's relationship label (e.g., "step-brother")
#   @ethan's     → prints name + possessive 's
#
# The short name is the NPC id WITHOUT the "npc_" prefix:
#   npc_ethan  → @ethan
#   npc_elena  → @elena
#   npc_aunt_linda → @aunt_linda
#
# Examples:
#   { type = "paragraph", content = "@ethan looks up from his coffee." }
#   { type = "paragraph", content = "Your @ethan.rel gives you a knowing look." }
#   { type = "paragraph", content = "@ethan's smile fades as he reads the letter." }
#   { type = "dialog", content = "I missed you.", props = { speaker = "npc", npcId = "npc_ethan" } }
#   # NOTE: Dialog speaker attribution is automatic via npcId — no @ needed for the speaker label.
#   # But dialog CONTENT can use @ to reference OTHER NPCs by name.
#
# RULES:
# - REQUIRED: Use @-references in ALL content for customizable NPCs (customizable = true)
# - RECOMMENDED: Use @-references for all NPCs for consistency
# - Dialog speaker labels are handled by npcId prop — do NOT put @ in speaker names
# - Unmatched @-references are left as-is (safe for email addresses)
# - Emotion mapping descriptions should also use @-syntax
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 3m. [story_arc]
# ─────────────────────────────────────────────────────────────────────────────
#
# The story_arc tracks narrative progression. It drives the Quest/Journal
# page that shows the player what they've accomplished and what's next.
#
# [story_arc]
# version (string) [D: "1.0"]
#
# ── [[story_arc.chapters]] ──
# id          (string) [R] — lowercase_snake_case, unique among chapters
# name        (string) [R] — display name (NOT "title"!)
# mood        (string) [D: "neutral"] — "hopeful","romantic","tense","passionate","peaceful","neutral"
# description (string) [D: ""]
# order       (int)    [D: 0] — display order (lower first)
#
# ── [[story_arc.nodes]] ──
# id                (string)       [R] — lowercase_snake_case, unique among nodes
# name              (string)       [R] — display name (NOT "title"!)
# chapter           (string)       [D: ""] — chapter ID this node belongs to
# journal_entry     (string)       [D: ""] — text shown in journal (NOT "summary"!)
# linked_canvas     (string|nil)   [D: nil] — canvas ID (NOT "canvasId"!)
# linked_canvas_node(string|nil)   [D: nil] — node ID within linked_canvas
# linked_flag       (string|nil)   [D: nil] — flag that completes this node
# group             (string|nil)   [D: nil] — group ID this node belongs to
# requires_group    (string|nil)   [D: nil] — group that must complete first
# requires_nodes    (list[string]) [D: []]  — node IDs that must complete first
# is_milestone      (bool)         [D: false]
# npc               (string|nil)   [D: nil] — associated NPC for quest page
# trait_requirements(list[dict])   [D: []]  — trait requirements to unlock
# branch_condition  (string|nil)   [D: nil] — flag that must be set for this node to appear in journal
#
# CRITICAL: linked_canvas must reference a NON-REPEATABLE canvas.
# Story arcs track narrative events only. Repeatable activities and
# random encounters must NOT appear in the story arc.
# If an activity milestone matters to the story, create a separate
# non-repeatable canvas (story event) for that moment.
#
# CRITICAL FIELD NAMES:
#   Use "name", NOT "title"
#   Use "linked_canvas", NOT "canvasId"
#   Use "journal_entry", NOT "summary"
#   Chapters do NOT contain a "nodes" array — nodes reference chapters
#
# ── [[story_arc.groups]] ──
# id             (string) [R] — lowercase_snake_case, unique among groups
# name           (string) [R]
# description    (string) [D: ""]
# required_count (int)    [D: 1] — how many nodes in group must complete
#
# ── [story_arc.emotion_mappings.TRAIT_NAME] ──
# Keyed by trait name (e.g., [story_arc.emotion_mappings.love])
# trait_owner (string)     [D: "npc"]  — "player" or "npc"
# default_npc (string|nil) [D: nil]    — NPC ID if trait_owner = "npc"
#
# [[story_arc.emotion_mappings.TRAIT_NAME.ranges]]
# min         (int)    [R]
# max         (int)    [R]
# label       (string) [R]
# description (string) [R]
#
# Ranges must NOT overlap within the same trait mapping.
#
# ── [story_arc.hints] ──
# stuck_threshold_minutes (int)    [D: 30]
# hint_style              (string) [D: "observation"] — "observation","suggestion","memory"
#
# [[story_arc.hints.templates]]
#   text (string) [D: ""]
#   [story_arc.hints.templates.condition]
#     missing_flag  (string|nil) [D: nil]
#     missing_trait (string|nil) [D: nil]
#     gap_gte       (int|nil)    [D: nil]
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 4: VALID VALUES QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
#
# CRITICAL: Use ONLY these values. Do NOT invent new ones.
#
# exit_block.type:
#   ONLY "location" or "choices"
#   INVALID: "node", "trigger", "canvas", "scene"
#
# exit_block.config.destinationType (for type = "location"):
#   ONLY "trigger" or "specific"
#   INVALID: "canvas", "node", "scene"
#
# choice.targetType (for type = "choices"):
#   ONLY "trigger", "location", or "node"
#   INVALID: "canvas", "scene"
#
# conditions.items[].type:
#   "flag", "trait", "days_since_flag", "clothing_slot", "clothing_item",
#   "worn_beauty", "worn_corruption", "pass", "item", "stage"
#   (worn_* and clothing_* require the clothing system enabled)
#
# flag operator:
#   "is_true", "is_false", "exists"
#
# trait operator:
#   "eq", "ne", "gt", "gte", "lt", "lte"
#
# days_since_flag operator:
#   "eq", "gt", "gte", "lt", "lte"
#
# effects[].op:
#   "add" or "set"
#
# effects[].targetType / flagEffects[].targetType:
#   "player" or "npc"
#
# trigger_mode:
#   "manual" or "random"
#
# clothing slot:
#   "bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"
#
# wardrobeEffects action:
#   "add" or "equip"
#
# block type:
#   "paragraph", "heading", "dialog", "video", "image", "clip"
#
# dialog speaker:
#   "player" or "npc"
#
# story_arc chapter mood:
#   "hopeful", "romantic", "tense", "passionate", "peaceful", "neutral"
#
# hint_style:
#   "observation", "suggestion", "memory"
#
# Node requirements (every [[canvases.nodes]] MUST have):
#   id = "node_id"      (lowercase snake_case)
#   name = "Node Name"  (human-readable, REQUIRED)
#   blocks = [...]      (content blocks)
#   exit_block = {...}   (how to exit this node)
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 5: CRITICAL RULES
# ═══════════════════════════════════════════════════════════════════════════════
#
# These rules are non-negotiable. Violating them causes parser failures
# or broken gameplay.
#
# RULE 1: TOML INLINE TABLES MUST BE SINGLE-LINE
#   The opening { and closing } must be on the same logical line.
#   Arrays [...] inside inline tables CAN span multiple lines.
#
#   CORRECT:
#   exit_block = { type = "choices", choices = [
#     { text = "Option 1", targetType = "trigger" }
#   ] }
#
#   WRONG (parser breaks):
#   exit_block = {
#     type = "choices",
#     choices = [...]
#   }
#
# RULE 2: EFFECTS PLACEMENT
#   For type = "choices": effects go INSIDE each choice object
#   For type = "location": effects go INSIDE the config dict
#   Effects NEVER go directly on the exit_block itself.
#
# RULE 3: CROSS-CANVAS NODE REFERENCES
#   To navigate from one canvas to a node in another canvas:
#   Use targetType = "node" with nodeId = "canvas_id.node_id"
#
#   Example: { text = "Go to kitchen", targetType = "node",
#              nodeId = "kitchen_morning.n1" }
#
#   Format: "canvas_id.node_id"
#     canvas_id = the id of the target [[canvases]] entry
#     node_id = the id of the target [[canvases.nodes]] entry
#
#   WRONG: targetType = "canvas" (THIS VALUE DOES NOT EXIST)
#   RIGHT: targetType = "node", nodeId = "other_canvas.n1"
#
# RULE 4: ALL IDS ARE LOWERCASE_SNAKE_CASE
#   Regex: ^[a-z0-9_]+$
#   No hyphens, no spaces, no uppercase.
#   Location IDs: use loc_ prefix (e.g., loc_kitchen)
#   NPC IDs: use npc_ prefix (e.g., npc_angela)
#
# RULE 5: STARTING CANVAS HAS NO TRIGGER
#   The canvas referenced by starting_canvas must NOT have a
#   [canvases.trigger] section. It fires once when the game starts.
#
# RULE 6: STORY ARC FIELD NAMES
#   Use "name", NOT "title" (for chapters, nodes, groups)
#   Use "linked_canvas", NOT "canvasId" (for story_arc nodes)
#   Use "journal_entry", NOT "summary" (for story_arc nodes)
#   Chapters do NOT contain a "nodes" array.
#   Nodes reference chapters via their "chapter" field.
#
# RULE 7: FLAG REGISTRATION
#   Every flag used anywhere (conditions, flagEffects) must appear in
#   either player.flag_keys or the relevant NPC's flag_keys.
#   Missing flags won't cause a parser error but will cause runtime bugs.
#
# RULE 8: DUAL GATING ON ESCALATION CHOICES
#   Every gated escalation choice MUST require BOTH:
#   a) A numeric stat threshold (corruption >= X, love >= Y, etc.)
#   b) A narrative flag from a prior story event (flirt_unlock, kiss_unlocked, etc.)
#
#   Threshold alone feels like an arbitrary number wall.
#   Flag alone means grinding is impossible (stuck if you miss one event).
#   Together they ensure: the player has BOTH narratively learned the behavior
#   AND built enough stat investment to access it.
#
#   CORRECT:
#   conditions = { version = "1.0", logic = "AND", items = [
#     { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 90 },
#     { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
#   ] }
#
#   WRONG (threshold only — feels arbitrary):
#   conditions = { version = "1.0", items = [
#     { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 90 }
#   ] }
#
#   WRONG (flag only — no progression feel):
#   conditions = { version = "1.0", items = [
#     { type = "flag", subject = "player", flag_key = "tease_unlock", operator = "is_true" }
#   ] }
#
#   EXCEPTION: The lowest-tier gated choice (e.g., "Stand closer") may use
#   threshold-only gating as a soft introduction. All higher tiers require both.
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 6: SEQUENTIAL CANVASES & FLAG CHAINS
# ═══════════════════════════════════════════════════════════════════════════════
#
# RULE: When 2+ non-repeatable canvases share a trigger location,
#       they MUST form a FLAG CHAIN for mutual exclusivity.
#
# WHY: Without flag conditions, ALL canvases are valid simultaneously.
#      The system picks one (often wrong order), breaking story flow.
#
# PATTERN:
# ┌─────────────────┬────────────────────────────┬─────────────────────────┐
# │ Canvas          │ Condition                  │ Sets Flag               │
# ├─────────────────┼────────────────────────────┼─────────────────────────┤
# │ First (Day 1)   │ NONE                       │ event_1_complete        │
# │ Second (Day 2)  │ event_1_complete = true     │ event_2_complete        │
# │ Third (Day 4)   │ event_2_complete = true     │ event_3_complete        │
# │ Fourth (Day 10) │ event_3_complete = true     │ event_4_complete        │
# └─────────────────┴────────────────────────────┴─────────────────────────┘
#
# This ensures EXACTLY ONE canvas is valid at any time for that location.
#
# ─────────────────────────────────────────────────────────────────────────────
#           TRANSLATING "DAY X" FROM GAME BOOK TO TOML
# ─────────────────────────────────────────────────────────────────────────────
#
# The Game Design Book uses temporal markers like "Day 1", "Day 2".
# TOML has NO native day-based conditions.
#
# TRANSLATION RULES:
#
# Book says "Day 1 event":
#   Condition: NONE (or just location + npc)
#   Exit sets: canvas_id_complete flag
#
# Book says "Day 2 event":
#   Condition: day_1_canvas_complete = true
#   Exit sets: canvas_id_complete flag
#
# Book says "Day X event" (with time gap):
#   Condition: previous_flag = true AND days_since_flag >= gap
#   Exit sets: canvas_id_complete flag
#
# WRONG: Treating "Day 1", "Day 2" as literal day numbers
# RIGHT: Creating flag chains so events unlock sequentially
#
# USE days_since_flag FOR PACING:
# When the Book specifies a multi-day gap (e.g., "Day 4" after "Day 2"),
# add a days_since_flag condition:
#   { type = "days_since_flag", subject = "player",
#     flag_key = "event_2_complete", operator = "gte", value = 2 }
#
# This ensures at least 2 in-game days pass between events.
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 7: REFERENCE PATTERNS IN TOML
# ═══════════════════════════════════════════════════════════════════════════════
#
# Each pattern below shows the EXACT TOML structure for a common canvas type.
# These are drawn from the reference game (Jack's World).
# When translating the Book, match the closest pattern.
#
# ─────────────────────────────────────────────────────────────────────────────
# PATTERN A0: THREE-CHOICE ACTIVITY (PREFERRED — replaces flat tier ladder)
# ─────────────────────────────────────────────────────────────────────────────
#
# The standard NPC activity format. Base node with group variants (content
# changes per relationship phase), then exactly 3 choices:
#   [Emotional] → conversation node (group variants) → exit
#     Effects: love +3, trust +2
#   [Physical]  → sub-node with unlockable intensity choices → tier nodes
#     Effects: love +1, corruption (NPC) +3-8, corruption (player) +2-6
#   [Neutral]   → direct exit with small reward
#     Effects: love +1, trust +3
#
# Base node group variants use relationship phase flags:
#   Phase 5: madison_arrived (or equivalent late-game flag)
#   Phase 4: first_night_complete (or equivalent intimacy flag)
#   Phase 3: first_kiss_done (or equivalent first-physical flag)
#   Default: early game / reconnecting
#
# Physical sub-node choices are flag-gated (NOT stat-gated):
#   Touch (always available in physical) → Flirt (flirt_unlock) →
#   Kiss (kiss_unlock) → Manual (manual_unlock) → Oral (oral_unlock) →
#   Sex (sex_unlock)
#
# See game_design_rules.md Rule 11 and game_design_patterns.md Pattern L
# for full documentation, TOML examples, and anti-patterns.
#
# ─────────────────────────────────────────────────────────────────────────────
# PATTERN A: STANDARD ESCALATING ACTIVITY (LEGACY — use Pattern A0 instead)
# ─────────────────────────────────────────────────────────────────────────────
#
# ONE canvas. Base node with gated choices. Each choice leads to an
# escalation node. Escalation nodes exit back to the world.
#
# Structure:
#   Canvas → trigger (location, npc, schedule, repeatable)
#     └── Base Node (always shown)
#           └── exit_block type="choices"
#                 ├── Choice 1: always visible (no conditions) → trigger
#                 ├── Choice 2: stat gate only → escalation node
#                 ├── Choice 3: stat + flag gate → escalation node
#                 └── Choice 4: higher stat + flag → escalation node
#     └── Escalation Node 1 (for Choice 2)
#           └── exit_block type="choices" or type="location" → trigger
#     └── Escalation Node 2 (for Choice 3)
#           └── exit_block → trigger
#     ... etc.
#
# TOML:

[[canvases]]
id = "activity_breakfast_angela"
name = "Breakfast Together"
description = "Morning coffee together — choices unlock with progression"

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_angela"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "09:00"

# BASE NODE — always shown when canvas fires
[[canvases.nodes]]
id = "morning"
name = "Morning Coffee"
blocks = [
  { type = "paragraph", content = "Morning light fills the kitchen. Angela is already up, moving between the counter and the stove." },
  { type = "video", props = { file = "angela_white/clips/angela_white_4/clip_001.mp4", description = "Angela enters the kitchen wearing a loose shirt and shorts" } },
  { type = "dialog", content = "Morning. Coffee's ready.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "She slides a mug across the counter toward you." }
]
exit_block = { type = "choices", choices = [
  # ALWAYS AVAILABLE — no conditions
  { text = "Eat together", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 1 }, { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 1 }] },
  # STAT-ONLY GATE — love >= 22
  { text = "Stand closer to her", targetType = "node", nodeId = "activity_breakfast_angela.warm", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 22 }] } },
  # STAT + FLAG GATE — love >= 42 AND kiss_unlocked
  { text = "Kiss her", targetType = "node", nodeId = "activity_breakfast_angela.kiss", conditions = { version = "1.0", logic = "AND", items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 42 }, { type = "flag", subject = "player", flag_key = "kiss_unlocked", operator = "is_true" }] } },
  # STAT + FLAG GATE — love >= 62 AND groping_unlocked
  { text = "Get closer to her", targetType = "node", nodeId = "activity_breakfast_angela.foreplay", conditions = { version = "1.0", logic = "AND", items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 62 }, { type = "flag", subject = "player", flag_key = "groping_unlocked", operator = "is_true" }] } },
  # STAT + FLAG GATE — love >= 82 AND oral_unlocked
  { text = "Pull her close", targetType = "node", nodeId = "activity_breakfast_angela.intimate", conditions = { version = "1.0", logic = "AND", items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 82 }, { type = "flag", subject = "player", flag_key = "oral_unlocked", operator = "is_true" }] } }
] }

# ESCALATION NODE — shown when player meets love >= 22
[[canvases.nodes]]
id = "warm"
name = "Warm Morning"
blocks = [
  { type = "paragraph", content = "You come into the kitchen half-dressed. She doesn't look away." },
  { type = "video", props = { file = "angela_white/clips/angela_white_4/clip_006.mp4", description = "He arrives shirtless, embraces her from behind" } },
  { type = "paragraph", content = "Your arms wrap around her from behind. She stiffens for a moment, then relaxes." },
  { type = "dialog", content = "You're up early. Couldn't sleep... or couldn't stay away?", props = { speaker = "npc", npcId = "npc_angela" } }
]
exit_block = { type = "choices", choices = [
  { text = "Help her cook", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 2 }] },
  { text = "Just hold her", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 1 }] }
] }

# (Additional escalation nodes: kiss, foreplay, intimate — same pattern,
#  each with blocks + exit_block returning to trigger)
#
# KEY POINTS:
# - ONE canvas for the entire activity
# - Base node's choices are gated by increasing stats + flags
# - Each escalation node exits with targetType = "trigger"
# - No conditions on the canvas trigger itself (always available)
# - Schedule controls WHEN it fires (morning only)
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN B: DUAL-PATH ACTIVITY
# ─────────────────────────────────────────────────────────────────────────────
#
# Base node offers two distinct paths. Each path is a linear chain
# of nodes. One path may be more heavily gated than the other.
#
# Structure:
#   Canvas → trigger (with canvas-level condition)
#     └── Base Node
#           └── exit_block type="choices"
#                 ├── Leave (always) → trigger
#                 ├── Path A (light gate) → node chain A
#                 └── Path B (heavy gate) → node chain B
#     └── Path A: node1 → node2 → node3 → exit
#     └── Path B: node1 → node2 → (gated choice) → node3 → exit
#
# TOML:

[[canvases]]
id = "activity_bath_angela"
name = "Angela's Bath"
description = "The bathroom door is open — peek through or join her"

[canvases.trigger]
location = "loc_bathroom"
npc = "npc_angela"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
# CANVAS-LEVEL CONDITION: peek_unlocked flag must be set
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "peek_unlocked", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "20:00"

# BASE NODE — 3 choices: leave, peek path, join path
[[canvases.nodes]]
id = "approach"
name = "The Bathroom Door"
blocks = [
  { type = "paragraph", content = "The bathroom door is slightly ajar. Steam curls through the gap." },
  { type = "video", props = { file = "angela_white/clips/480p.h264/clip_001.mp4", description = "Angela stepping into the tub" } },
  { type = "paragraph", content = "Through the steam you catch a glimpse of her settling in." }
]
exit_block = { type = "choices", choices = [
  # ALWAYS AVAILABLE
  { text = "Leave quietly", targetType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 1 }] },
  # PEEK PATH — no extra condition (canvas-level gate is enough)
  { text = "Watch from the door", targetType = "node", nodeId = "activity_bath_angela.peek_routine" },
  # JOIN PATH — heavy gate: oral_unlocked + days_since_flag + love >= 65
  { text = "Join her", targetType = "node", nodeId = "activity_bath_angela.bath_self_care", conditions = { version = "1.0", logic = "AND", items = [{ type = "flag", subject = "player", flag_key = "oral_unlocked", operator = "is_true" }, { type = "days_since_flag", subject = "player", flag_key = "bath_invitation_complete", operator = "gte", value = 1 }, { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 65 }] } }
] }

# PEEK PATH — linear chain of nodes
[[canvases.nodes]]
id = "peek_routine"
name = "Evening Routine"
blocks = [
  { type = "paragraph", content = "You lean against the wall beside the door, not quite ready to walk away." },
  { type = "video", props = { file = "angela_white/clips/480p.h264/clip_004.mp4", description = "Sitting up in the tub, reaching for soap" } },
  { type = "paragraph", content = "She tips her head back and closes her eyes." }
]
exit_block = { type = "choices", choices = [
  { text = "Continue watching", targetType = "node", nodeId = "activity_bath_angela.peek_intimate" }
] }

# (peek_intimate → peek_selftouch → peek_private, each a simple node
#  with blocks + exit_block. Terminal node exits with type="location")

# TERMINAL PEEK NODE — exits back to world
# [[canvases.nodes]]
# id = "peek_private"
# name = "Private Moment"
# blocks = [ ... ]
# exit_block = { type = "location", text = "Leave quietly",
#   config = { destinationType = "trigger", time_progression_minutes = 30,
#     effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 2 }] } }
#
# KEY POINTS:
# - Canvas-level condition gates entire activity (peek_unlocked)
# - Two independent paths from same base node
# - Peek path: linear chain, no inter-node conditions
# - Join path: heavily gated (flag + time + stat)
# - Within join path, further nodes can have additional gates
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN C: UTILITY CANVAS (Chore)
# ─────────────────────────────────────────────────────────────────────────────
#
# Simplest canvas. Single node, single exit, minimal effects.
# No NPC field on trigger (solo activity).
#
# TOML:

[[canvases]]
id = "activity_wash_dishes"
name = "Wash Dishes"
description = "Clean up the kitchen — dishes, counters, the works"

[canvases.trigger]
location = "loc_kitchen"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "chores_explained", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "14:00"

[[canvases.nodes]]
id = "dishes"
name = "Dishes"
blocks = [
  { type = "paragraph", content = "The sink is full from breakfast. You roll up your sleeves and start scrubbing. Plates, mugs, the pan she used. The hot water is almost meditative." },
  { type = "paragraph", content = "When you're done, the kitchen looks like it did when you moved in. Clean counters. Drying rack full. She'll notice." }
]
exit_block = { type = "location", text = "Done", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 1 }] } }

# KEY POINTS:
# - No npc field on trigger (solo activity)
# - Single node with text-only blocks (no video/dialog)
# - type = "location" exit (single button, not choices)
# - Minimal effect: trust +1 only
# - Flag-gated: chores_explained must be set
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN D: JOB CANVAS
# ─────────────────────────────────────────────────────────────────────────────
#
# Single node, earns money. Uses clamp = false on money effect.
# max_triggers_per_day allows multiple shifts.
#
# TOML:

[[canvases]]
id = "activity_cafe_shift_morning"
name = "Cafe Shift"
description = "Morning shift at the cafe"

[canvases.trigger]
location = "loc_cafe"
is_active = true
is_repeatable = true
max_triggers_per_day = 2
priority = 1
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "job_started", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "12:00"

[[canvases.nodes]]
id = "n1"
name = "Morning Shift"
blocks = [
  { type = "paragraph", content = "The cafe smells like ground coffee and fresh pastries. You tie on your apron and get to work. Regulars come and go. Tips are decent." },
  { type = "paragraph", content = "Your phone buzzes once — a message from Angela. 'Missed you at breakfast.' You pocket it and keep working." }
]
exit_block = { type = "location", text = "Finish shift", config = { destinationType = "trigger", time_progression_minutes = 180, effects = [{ targetType = "player", trait = "money", op = "add", value = 70, clamp = false }, { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 1 }] } }

# KEY POINTS:
# - money effect uses clamp = false (money can be any positive value)
# - time_progression_minutes = 180 (3-hour shift)
# - max_triggers_per_day = 2 (morning + afternoon shifts possible)
# - Trade-off: time at work = time away from NPC
# - Create separate canvases for morning/afternoon with different schedules
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN E: TIME-ADVANCEMENT CANVAS
# ─────────────────────────────────────────────────────────────────────────────
#
# Always available. No conditions, no schedule, no NPC.
# Choices with different time_progression_minutes values.
# Solves the "time gap problem" — player can advance clock
# to reach next activity window.
#
# TOML:

[[canvases]]
id = "activity_jacks_room"
name = "Bed"
description = "Your room — rest, sleep, pass the time"

[canvases.trigger]
location = "loc_jacks_bedroom"
is_active = true
is_repeatable = true
priority = 1

[[canvases.nodes]]
id = "room"
name = "Your Room"
blocks = [
  { type = "paragraph", content = "Your room. The bed Angela made up for you on that first day. A desk by the window, your bag half-unpacked in the corner. It's starting to feel like yours." }
]
exit_block = { type = "choices", choices = [
  { text = "Rest for a bit", targetType = "trigger", time_progression_minutes = 120 },
  { text = "Go to sleep", targetType = "trigger", time_progression_minutes = 540 }
] }

# KEY POINTS:
# - No conditions, no schedules, no npc — always available
# - Two choices differ ONLY in time_progression_minutes
# - 120 minutes (2 hours) for resting, 540 minutes (9 hours) for sleeping
# - No effects on either choice (rest doesn't change stats)
# - Every game MUST have at least one time-advancement canvas
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN F: STORY EVENT (One-Time)
# ─────────────────────────────────────────────────────────────────────────────
#
# Non-repeatable event. High priority. Conditions combine flags + stats.
# Multiple nodes with branching choices. Both branches set the same flag
# (ensuring story progresses regardless of choice).
#
# TOML:

[[canvases]]
id = "first_kiss"
name = "The First Kiss"
description = "On the couch, in the dark, it finally happens."

[canvases.trigger]
location = "loc_living_room"
npc = "npc_angela"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "towel_encounter_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 25 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

# NODE 1: THE SETUP
[[canvases.nodes]]
id = "the_moment"
name = "The Moment"
blocks = [
  { type = "paragraph", content = "The movie ended ten minutes ago. Neither of you got up to change it. The credits are rolling in the dark." },
  { type = "paragraph", content = "Angela is closer than she usually sits. You can smell her shampoo." },
  { type = "dialog", content = "I keep thinking about the other night. The bathroom.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "dialog", content = "I wasn't embarrassed, Jack. That's what scares me.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "She turns to face you. The room is dark except for the TV glow." }
]
# BRANCHING CHOICE — pure player choice, no conditions
exit_block = { type = "choices", choices = [
  { text = "Kiss her gently", targetType = "node", nodeId = "first_kiss.gentle" },
  { text = "Pull her close", targetType = "node", nodeId = "first_kiss.passionate" }
] }

# NODE 2A: GENTLE PATH
[[canvases.nodes]]
id = "gentle"
name = "Gentle"
blocks = [
  { type = "paragraph", content = "You lean in slowly. Giving her time to pull away. She doesn't." },
  { type = "image", props = { file = "tender_kiss.gif", description = "Soft, tender first kiss" } },
  { type = "paragraph", content = "Her lips are warm. The kiss is soft, careful. Like a question she's been afraid to ask." },
  { type = "dialog", content = "We probably shouldn't have done that.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "But she's smiling. And she doesn't move away." }
]
# FLAG-SETTING EXIT — sets first_kiss_complete
exit_block = { type = "location", text = "Say goodnight", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 2 }, { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 1 }], flagEffects = [{ targetType = "player", flag = "first_kiss_complete" }] } }

# NODE 2B: PASSIONATE PATH
[[canvases.nodes]]
id = "passionate"
name = "Passionate"
blocks = [
  { type = "paragraph", content = "You don't think about it. You reach for her." },
  { type = "image", props = { file = "passionate_kiss.gif", description = "Passionate first kiss" } },
  { type = "paragraph", content = "The kiss is not gentle. It's urgent. Her hands find your face." },
  { type = "dialog", content = "Goodnight.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "The way she says it — it's not a goodbye. It's a promise." }
]
# SAME FLAG, DIFFERENT EFFECTS — passionate gives more love, less trust
exit_block = { type = "location", text = "Watch her leave", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 3 }], flagEffects = [{ targetType = "player", flag = "first_kiss_complete" }] } }

# KEY POINTS:
# - is_repeatable = false (fires once, ever)
# - priority = 10 (overrides regular activities at same location/time)
# - Both branches set the SAME flag (first_kiss_complete)
# - Different branches give different stat rewards (player choice matters)
# - The branching is unconditional — pure narrative choice
# - Uses image blocks (not video) for the kiss moments
#
# NOTE: Both branches above set the SAME flag. This is within-canvas branching
# where both paths lead to the same story arc completion. For DIFFERENT story
# paths per NPC (where the journal shows different nodes depending on the
# player's choice), use branch_condition on story_arc nodes — see Pattern M
# in game_design_patterns.md. Arc-level branch points set DIFFERENT flags:
#   flagEffects = [{ targetType = "player", flag = "chose_gentle" }]
#   vs
#   flagEffects = [{ targetType = "player", flag = "chose_passionate" }]
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN G: GATE-SETTING EVENT
# ─────────────────────────────────────────────────────────────────────────────
#
# One-time event that SETS GATE FLAGS, enabling new choices in activities.
# Uses days_since_flag for pacing. This is the key mechanism that unlocks
# progressively intimate content.
#
# TOML:

[[canvases]]
id = "massage_offer"
name = "The Offer"
description = "Angela is falling apart — and Jack helps without an agenda."

[canvases.trigger]
location = "loc_living_room"
npc = "npc_angela"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "towel_encounter_complete", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" },
  # DAYS_SINCE_FLAG — 2+ days must pass after first kiss
  { type = "days_since_flag", subject = "player", flag_key = "first_kiss_complete", operator = "gte", value = 2 },
  { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 40 },
  { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "trust", operator = "gte", value = 18 }
]
[[canvases.trigger.schedules]]
start_time = "18:00"
end_time = "21:00"

# NODE 1: THE SITUATION
[[canvases.nodes]]
id = "bad_day"
name = "Bad Day"
blocks = [
  { type = "paragraph", content = "Angela is on the couch, but she's not relaxing. Bills are spread across the coffee table." },
  { type = "dialog", content = "Long day?", props = { speaker = "player" } },
  { type = "dialog", content = "I'm fine.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "The kind of 'fine' that means the opposite." }
]
exit_block = { type = "choices", choices = [
  { text = "Sit with her", targetType = "node", nodeId = "massage_offer.the_offer" }
] }

# NODE 2: THE GATE-SETTING MOMENT
[[canvases.nodes]]
id = "the_offer"
name = "The Offer"
blocks = [
  { type = "paragraph", content = "You sit down on the couch. Not too close. Just close enough." },
  { type = "dialog", content = "I have massage oils in the bedroom. Maybe we could do this properly sometime?", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "dialog", content = "Just say when.", props = { speaker = "player" } },
  { type = "paragraph", content = "She smiles — not the polite one. The real one." }
]
# SETS TWO GATE FLAGS — kiss_unlocked enables kiss choices in activities,
# massage_offered enables the massage night activity
exit_block = { type = "location", text = "Head to your room", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 2 }, { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 3 }], flagEffects = [{ targetType = "player", flag = "kiss_unlocked" }, { targetType = "player", flag = "massage_offered" }] } }

# KEY POINTS:
# - days_since_flag ensures cooldown (2 days after first kiss)
# - Requires BOTH flag (first_kiss_complete) AND stat thresholds
# - Sets MULTIPLE gate flags in one exit (kiss_unlocked + massage_offered)
# - Gate flags enable new choices in existing activities
# - Uses { speaker = "player" } for player dialog
# - Creates dependency chain: towel → first_kiss → (2 days) → massage_offer
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN H: ECONOMIC EVENT (Recurring)
# ─────────────────────────────────────────────────────────────────────────────
#
# Repeatable economic event. Uses days_since_flag for weekly recurrence.
# Deducts money with negative value. Resets the timer flag.
#
# TOML:

[[canvases]]
id = "activity_weekly_rent"
name = "Rent Day"
description = "Weekly rent payment to Angela"

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_angela"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 2
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "first_rent_paid", operator = "is_true" },
  # 7+ days since last payment
  { type = "days_since_flag", subject = "player", flag_key = "rent_last_paid", operator = "gte", value = 7 },
  # Player must have enough money
  { type = "trait", subject = "player", trait_key = "money", operator = "gte", value = 200 }
]

[[canvases.nodes]]
id = "n1"
name = "Rent Day"
blocks = [
  { type = "paragraph", content = "Another week. You count out two hundred dollars and leave it on the kitchen counter." },
  { type = "dialog", content = "You don't have to keep doing this, you know.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "But she takes it. And that evening, dinner is a little better than usual." }
]
exit_block = { type = "location", text = "Done", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "money", op = "add", value = -200, clamp = false }, { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 2 }], flagEffects = [{ targetType = "player", flag = "rent_last_paid" }] } }

# KEY POINTS:
# - days_since_flag with rent_last_paid >= 7 creates weekly recurrence
# - Money check (money >= 200) ensures player can afford it
# - Negative value (-200) deducts money, clamp = false allows any amount
# - flagEffects resets rent_last_paid, restarting the 7-day timer
# - No schedules — fires any time conditions are met
# - priority = 2 fires before regular activities (priority 1)
# - is_repeatable = true (this fires every week)
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN I: RANDOM ENCOUNTER CANVAS
# ─────────────────────────────────────────────────────────────────────────────
#
# Passive witnessing event. Fires probabilistically when player enters a
# location. No player agency — the encounter just happens. Small stat gains.
# Used to build atmosphere and provide passive corruption growth.
#
# TOML:

[[canvases]]
id = "alley_encounter"
name = "Alley Encounter"
description = "Walking home late, you see something in the alley."

[canvases.trigger]
location = "loc_city_streets"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
trigger_mode = "random"
chance = 0.7
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 30 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

[[canvases.nodes]]
id = "n1"
name = "The Alley"
blocks = [
  { type = "paragraph", content = "You take the shortcut through the alley behind the bar. Halfway through, you hear it — soft sounds from the shadows." },
  { type = "paragraph", content = "A couple, pressed against the wall. They don't notice you. Or maybe they don't care." },
  { type = "paragraph", content = "You walk past quickly. But the image stays with you." }
]
exit_block = { type = "location", text = "Keep walking", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "corruption", op = "add", value = 2 }] } }

# KEY POINTS:
# - trigger_mode = "random" with chance = 0.7 (70% probability)
# - max_triggers_per_day = 1 prevents spam
# - is_repeatable = true (can happen again tomorrow)
# - Small corruption gain (+2) — passive normalization
# - No choices — player witnesses, doesn't participate
# - Gated by minimum corruption (only fires once player is already shifting)
# - Schedule constrains to late night (thematically appropriate)
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN J: MULTI-NPC PARALLEL ARC (Story Chain)
# ─────────────────────────────────────────────────────────────────────────────
#
# In multi-NPC games, story events form PARALLEL chains across different
# NPCs/arcs. Each arc has its own flag chain, gated by player corruption.
# Shared unlock flags transfer across arcs.
#
# TOML (two canvases from different arcs):

# --- ARC: Mick's Story (corruption 40-220) ---
[[canvases]]
id = "mick_first_meeting"
name = "Meeting Mick"
description = "The new bartender catches your eye."

[canvases.trigger]
location = "loc_bar_floor"
npc = "npc_mick"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "bar_job_started", operator = "is_true" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 40 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "23:59"

[[canvases.nodes]]
id = "intro"
name = "First Impression"
blocks = [
  { type = "paragraph", content = "The new guy behind the bar is tall, tattooed, and watching you." },
  { type = "dialog", content = "You must be the new girl. Jolene told me about you.", props = { speaker = "npc", npcId = "npc_mick" } },
  { type = "paragraph", content = "His smile is easy. Confident. Like he already knows something you don't." }
]
exit_block = { type = "choices", choices = [
  { text = "Smile back", targetType = "node", nodeId = "mick_first_meeting.friendly" },
  { text = "Focus on work", targetType = "node", nodeId = "mick_first_meeting.distant" }
] }

[[canvases.nodes]]
id = "friendly"
name = "Friendly Response"
blocks = [
  { type = "paragraph", content = "You smile. He grins wider." },
  { type = "dialog", content = "I think we're gonna get along.", props = { speaker = "npc", npcId = "npc_mick" } }
]
# Both branches set same completion flag — plus this one adds NPC love
exit_block = { type = "location", text = "Get back to work", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "npc", npcId = "npc_mick", trait = "love", op = "add", value = 3 }, { targetType = "player", trait = "corruption", op = "add", value = 3 }], flagEffects = [{ targetType = "player", flag = "mick_first_meeting_complete" }] } }

[[canvases.nodes]]
id = "distant"
name = "Distant Response"
blocks = [
  { type = "paragraph", content = "You nod politely and turn back to the customers." },
  { type = "paragraph", content = "He doesn't push it. But you feel his eyes on you for the rest of the shift." }
]
exit_block = { type = "location", text = "Finish the shift", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "corruption", op = "add", value = 2 }], flagEffects = [{ targetType = "player", flag = "mick_first_meeting_complete" }] } }


# --- NEXT CANVAS IN MICK ARC (sets shared unlock flag) ---
[[canvases]]
id = "mick_flirt_lesson"
name = "Mick's Flirting Lesson"
description = "Mick shows you how to work the crowd."

[canvases.trigger]
location = "loc_bar_floor"
npc = "npc_mick"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "mick_first_meeting_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "mick_first_meeting_complete", operator = "gte", value = 2 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 65 },
  { type = "trait", subject = "npc", npc_id = "npc_mick", trait_key = "love", operator = "gte", value = 10 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "23:59"

[[canvases.nodes]]
id = "lesson"
name = "The Lesson"
blocks = [
  { type = "paragraph", content = "It's a slow night. Mick leans on the bar next to you." },
  { type = "dialog", content = "Want to know why my tips are twice yours?", props = { speaker = "npc", npcId = "npc_mick" } },
  { type = "paragraph", content = "He teaches you to smile, to lean in, to make the customers feel special." },
  { type = "dialog", content = "It's not about the drinks. It's about making them feel seen.", props = { speaker = "npc", npcId = "npc_mick" } }
]
# SETS SHARED UNLOCK FLAG — flirt_unlock now available across ALL arcs
exit_block = { type = "location", text = "Try it out", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_mick", trait = "love", op = "add", value = 3 }, { targetType = "player", trait = "corruption", op = "add", value = 5 }], flagEffects = [{ targetType = "player", flag = "mick_flirt_lesson_complete" }, { targetType = "player", flag = "flirt_unlock" }] } }

# KEY POINTS:
# - Two canvases from Mick arc form a flag chain:
#   mick_first_meeting → mick_flirt_lesson
# - Player corruption gates arc entry (>= 40 for first, >= 65 for second)
# - NPC love also gates (>= 10 for flirt lesson — player must interact with Mick)
# - days_since_flag paces the arc (2+ days between events)
# - flirt_unlock is a SHARED flag — once set, flirting choices appear
#   in bar work activity, glory hole activity, public encounters, etc.
# - Both branches of branching events set the same completion flag
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN K: CLOTHING SYSTEM (Tiered Wardrobe)
# ─────────────────────────────────────────────────────────────────────────────
#
# Clothing items organized in corruption tiers. Starting wardrobe is basic,
# shop items unlock at higher corruption levels. Story events can gift items.
#
# TOML:

# --- Settings ---
[settings]
clothing_enabled = true
wardrobe_location = "loc_bedroom"
shop_location = "loc_mall_clothing"

[settings.clothing_requirements]
body_coverage = true
always_required = ["shoes"]

[settings.clothing_requirements.conditional.bra]
until_flag = "comfortable_braless"
message = "You're not comfortable going without a bra yet"

# --- Starting items (initial = true) ---
[[clothing]]
id = "plain_tshirt"
name = "Plain T-Shirt"
slot = "top"
initial = true

[[clothing]]
id = "blue_jeans"
name = "Blue Jeans"
slot = "bottom"
initial = true

[[clothing]]
id = "cotton_bra"
name = "Cotton Bra"
slot = "bra"
initial = true

[[clothing]]
id = "cotton_panties"
name = "Cotton Panties"
slot = "underwear"
initial = true

[[clothing]]
id = "sneakers"
name = "White Sneakers"
slot = "shoes"
initial = true

# --- Shop items (corruption-gated) ---
[[clothing]]
id = "sundress"
name = "Yellow Sundress"
slot = "dress"
price = 60
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 45 }
] }

[[clothing]]
id = "mini_skirt"
name = "Mini Skirt"
slot = "bottom"
price = 80
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 85 }
] }

[[clothing]]
id = "micro_bikini_top"
name = "Micro Bikini Top"
slot = "top"
price = 120
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 135 }
] }

# KEY POINTS:
# - initial = true items are equipped at game start
# - Shop items have price > 0 and conditions for corruption gating
# - Tier thresholds: Basic (0), Cute (45), Bold (85), Daring (135)
# - body_coverage = true means player must wear top+bottom or dress
# - conditional.bra.until_flag relaxes bra requirement after story event
# - always_required = ["shoes"] means shoes are always needed
# - wardrobeEffects on story canvases can add items (Pattern J example)
#
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN L: RENT SYSTEM (Recurring Economic Pressure)
# ─────────────────────────────────────────────────────────────────────────────
#
# Uses [settings.rent] for system-level rent tracking plus Pattern H
# (economic event canvas) for the actual rent payment interaction.
# In multi-NPC games, rent creates escalation pressure: base tier income
# can't cover it, pushing the player toward higher-corruption activities.
#
# TOML:

[settings.rent]
enabled = true
amount = 150
due_day = "Monday"
collector_npc = "npc_jolene"
grace_periods = 1

# The rent payment canvas (Pattern H) works in tandem:
# See Pattern H for the full canvas structure.
# The key difference: [settings.rent] provides system-level tracking,
# while the canvas provides the narrative interaction.
#
# ECONOMIC PRESSURE DESIGN:
# Base tier income: $35/shift (normal work) × 5 shifts/week = $175
# After rent ($150): $25 left for food, clothes, etc. — IMPOSSIBLE
# This forces the player to escalate:
#   Flirting tips: $55/shift → $275/week → $125 after rent (tight)
#   Showing off:   $90/shift → $450/week → $300 after rent (comfortable)
#   Higher tiers:  $120-500/shift → financial freedom
#
# The player does the math. The game never lectures.
#
# ─────────────────────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 8: PHASE 1 — METADATA & LOCATIONS
# ═══════════════════════════════════════════════════════════════════════════════
#
# INPUT: Book Phases 1-3 (Foundation, Characters, World)
# OUTPUT: 1_metadata_and_locations.toml
#
# STEP 1: [project] section
#   - id: derive from Book's game title → lowercase_snake_case
#   - title: Book's game title
#   - description: Book's game premise/summary
#
# STEP 2: [time] section
#   - If Book specifies starting time → use it
#   - Otherwise use defaults: hour=8, day="Monday", week=1
#
# STEP 3: [player] section
#   - id: Book's protagonist name → lowercase (e.g., "jack")
#   - name: Book's protagonist name
#   - core_traits: Map Book's "Stat Economy" → player-owned stats only
#     - Player stats: money, energy, confidence, etc.
#     - NPC stats (love, trust) go on the NPC, not here
#   - flag_keys: Compile the MASTER FLAG LIST
#     - Scan Book Phase 4 (Story Events) for all flags set/checked
#     - Scan Book Phase 5 (Activities) for all flags in conditions
#     - Include: game_started, all event_complete flags, all gate flags,
#       all utility flags (job_started, chores_explained, etc.)
#     - Include timer flags (rent_last_paid, etc.)
#
# STEP 4: [[npcs]] section
#   - One entry per NPC in Book Phase 2
#   - id: npc_prefix + lowercase name (e.g., "npc_angela")
#   - core_traits: NPC's starting relationship stats from Book
#     (typically love=0, trust=0)
#   - flag_keys: NPC-specific flags (usually empty)
#   - Do NOT include [[npcs.schedules]] — REMOVED. NPC presence derived from canvas triggers.
#
#   MULTI-NPC NOTE: For multi-NPC games, each NPC has independent core_traits.
#   Multiple NPCs may share trait names (love, trust, corruption) but each
#   NPC's values are tracked independently. Example:
#     npc_mick: core_traits = [{ name = "love", value = 0 }, { name = "corruption", value = 0 }]
#     npc_harlan: core_traits = [{ name = "love", value = 0 }, { name = "trust", value = 0 }]
#
# STEP 5: [[locations]] section
#   - One entry per location in Book Phase 3
#   - id: loc_prefix + descriptive name (e.g., "loc_kitchen")
#   - Set up location hierarchy:
#     - Top-level locations: no parent, no entry_from
#     - Sub-locations: set entry_from to parent location's ID
#     - Containers: set is_container=true, default_entry to first child
#     - navigation_order: list children in display order
#   - image_search_queries: 2-3 word visual description of the place type
#     (e.g., "suburban kitchen warm", "college dorm room", "bar interior dim")
#     Do NOT use narrative/emotional words. Describe what the place looks like.
#
# STEP 6: Schema version and starting canvas
#   - schema_version = "0.2"
#   - starting_canvas: ID of the intro/arrival canvas (created in Phase 2)
#
# VALIDATION BEFORE PROCEEDING:
#   - All IDs are lowercase_snake_case
#   - All location IDs use loc_ prefix
#   - All NPC IDs use npc_ prefix
#   - No duplicate IDs within any category
#   - Location hierarchy has no cycles
#   - All flags from Book are in flag_keys
#   - Player stats and NPC stats are correctly assigned
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 9: PHASE 2 — STORY CANVASES
# ═══════════════════════════════════════════════════════════════════════════════
#
# INPUT: Book Phase 4 (Story Events) + Phase 1 TOML (for IDs)
# OUTPUT: 2_story_canvases.toml
#
# Story canvases are ONE-TIME events that advance the narrative.
# They set flags, unlock gates, and create the story backbone.
#
# STEP 1: STARTING CANVAS
#   - The very first canvas the player sees
#   - NO trigger section (it fires once at game start)
#   - Sets initial flags (e.g., game_started)
#   - Introduces the premise, establishes setting
#   - Exits with targetType = "trigger" to release player into the world
#   - Or exits with targetType = "node" pointing to another canvas
#     to create a multi-scene intro sequence
#
# STEP 2: STORY EVENT CANVASES
#   For each story event in Book Phase 4:
#
#   a. Canvas header:
#      - is_repeatable = false
#      - priority = 10
#      - location: where it happens (from Book)
#      - npc: which NPC is involved (from Book)
#
#   b. Trigger conditions (see Book's prerequisites):
#      - Previous event flag must be set (flag chain)
#      - Stat thresholds met (love >= X, trust >= Y)
#      - Time pacing via days_since_flag (if Book specifies day gaps)
#
#   c. Trigger schedule (from Book's time-of-day):
#      - Morning events: start_time = "07:00", end_time = "10:00"
#      - Evening events: start_time = "18:00", end_time = "22:00"
#      - If Book doesn't specify, omit schedules (fires any time)
#
#   d. Nodes and content:
#      - Transcribe Book's scene descriptions into blocks
#      - Preserve all video/image/clip references exactly
#      - Map Book's dialogue to dialog blocks with correct speaker/npcId
#      - Create branching choices where Book offers player decisions
#
#   e. Flag effects:
#      - Set completion flag on ALL exit paths (both branches set same flag)
#      - Set gate flags where Book specifies unlock moments
#      - Different branches can have different stat rewards
#
# STEP 3: FLAG CHAIN VERIFICATION
#   - List all story canvases sharing a trigger location
#   - Verify each group forms a proper flag chain
#   - First canvas: no flag condition (or only stat conditions)
#   - Each subsequent: requires previous canvas's completion flag
#   - Add days_since_flag where Book specifies time gaps
#
#   MULTI-NPC NOTE: For parallel arcs, multiple flag chains may share
#   the same location (e.g., bar_floor hosts both Mick arc and bar_work arc).
#   Each arc has its OWN independent flag chain. Arcs don't conflict because
#   each chain uses different flag names (mick_step_1_complete vs bar_step_1).
#   STAGGERING: Different arcs enter at different corruption thresholds,
#   so they naturally avoid competing for the same trigger slot.
#   See Pattern J for a multi-arc flag chain example.
#
# STEP 4: GATE FLAG MAPPING
#   Build a table mapping gate flags to the events that set them:
#
#   ┌──────────────────────┬─────────────────────────────────┐
#   │ Gate Flag            │ Set By Canvas                   │
#   ├──────────────────────┼─────────────────────────────────┤
#   │ kiss_unlocked        │ [event that earns first kiss]   │
#   │ groping_unlocked     │ [event that escalates touch]    │
#   │ oral_unlocked        │ [event that opens intimacy]     │
#   │ sex_unlocked         │ [climactic trust event]         │
#   └──────────────────────┴─────────────────────────────────┘
#
#   Every gate flag must be set by EXACTLY ONE story event.
#   Activities CONSUME gate flags but never SET them.
#
# STEP 5: ECONOMIC EVENT CANVASES
#   For recurring economic events (rent, bills, etc.):
#   - is_repeatable = true (they recur)
#   - priority = 2 (above regular activities)
#   - days_since_flag for recurrence timing
#   - Money checks in conditions (player can afford)
#   - Negative money effects with clamp = false
#   - Flag reset in flagEffects (restart timer)
#   - See Pattern H
#
# VALIDATION BEFORE PROCEEDING:
#   - All is_repeatable = false canvases have priority = 10
#   - All flag chains are valid (no competing canvases)
#   - All gate flags are set by exactly one event
#   - All cross-canvas node references use "canvas_id.node_id" format
#   - All branches of branching events set the same completion flag
#   - All stat thresholds are achievable through normal play
#   - Starting canvas has NO trigger
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 10: PHASE 3 — ACTIVITY CANVASES
# ═══════════════════════════════════════════════════════════════════════════════
#
# INPUT: Book Phase 5 (Activities) + Phase 1 & 2 TOML (for IDs, flags)
# OUTPUT: 3_activities.toml
#
# Activities are REPEATABLE canvases that give the player things to do
# between story events. They are the gameplay loop.
#
# UNIQUENESS RULE: One repeatable canvas per (location, NPC, schedule).
# At loc_kitchen, 07:00-09:00, npc_ethan can have exactly ONE canvas.
# Multiple interactions go INSIDE the canvas as choices (gated tiers),
# not as separate canvases. The NPC portrait at the location maps 1:1
# to a canvas. If Ethan and Linda are both in the kitchen at breakfast,
# that's a different NPC (separate canvas for Linda, or use a multi-NPC
# canvas with a different trigger NPC).
#
# THREE CATEGORIES:
#
# ─── CATEGORY 1: NPC ACTIVITIES (Escalating) ───
#
# These are the core relationship-building activities. Pattern A or B.
#
# For each NPC activity in Book Phase 5:
#
#   a. Create ONE canvas per activity (NOT multiple canvases per tier!)
#      - is_repeatable = true
#      - priority = 1 (or 6-8 for special activities)
#      - location, npc, schedule from Book
#
#   b. Base node: always-visible content
#      - Blocks: narrative text, video/images, dialog
#      - exit_block type = "choices" with progressive gating:
#
#   c. TRANSLATING BOOK'S CHOICE PROGRESSION TABLE:
#      The Book provides a progression table like:
#        T1: "Eat together" — always available
#        T2: "Stand closer" — love >= 22
#        T3: "Kiss her"     — love >= 42 + kiss_unlocked
#        T4: "Get closer"   — love >= 62 + groping_unlocked
#
#      Translate each tier to a choice:
#        T1 → no conditions, targetType = "trigger" (exit to world)
#        T2 → conditions with trait gate only, targetType = "node"
#        T3 → conditions with trait + flag gate, targetType = "node"
#        T4 → conditions with higher trait + flag gate, targetType = "node"
#
#   d. Escalation nodes: one per gated choice
#      - Blocks: the intimate content for that tier
#      - exit_block: choices or location back to trigger
#      - May have their own stat rewards (higher tiers = higher rewards)
#
#   e. CONDITIONS PLACEMENT:
#      - Canvas-level conditions: for activities that require a flag
#        to even APPEAR (e.g., bath requires peek_unlocked)
#      - Choice-level conditions: for gating WITHIN an activity
#        (e.g., kiss choice requires love >= 42 + kiss_unlocked)
#      - Use canvas-level when the entire activity is locked
#      - Use choice-level when only some options are locked
#
# ─── CATEGORY 2: SOLO ACTIVITIES (Non-Escalating) ───
#
# Activities the player does alone. No NPC, no progression.
# Pattern E (time advancement) or simple stat-building.
#
#   - Time advancement: rest, sleep (Pattern E)
#   - Exploration: reading, studying (builds stats, no NPC)
#   - Always available or gated by simple flags
#
# ─── CATEGORY 4: RANDOM ENCOUNTERS (Multi-NPC / World-Building) ───
#
# Passive witnessing events using trigger_mode = "random".
# See Pattern I for the full TOML structure.
#
# For each random encounter in the Book:
#   - is_repeatable = true, trigger_mode = "random", chance = 0.X
#   - max_triggers_per_day = 1
#   - Small stat gains (corruption +2-3)
#   - No choices — player witnesses, doesn't participate
#   - Gate by minimum stat threshold (only fire after player has started shifting)
#   - Schedule to appropriate time windows
#
# ─── CATEGORY 3: UTILITY CANVASES ───
#
# Functional canvases for game economy and mechanics.
# Pattern C (chores) or Pattern D (jobs).
#
#   a. Chores (Pattern C):
#      - Build trust indirectly
#      - Single node, simple exit
#      - May require flag (chores_explained)
#
#   b. Jobs (Pattern D):
#      - Earn money
#      - Longer time_progression_minutes (2-3 hours)
#      - max_triggers_per_day limits shifts
#      - clamp = false on money effects
#
# BALANCE CHECKLIST:
#   - At least 1 time-advancement canvas (rest/sleep)
#   - At least 1 job canvas (income source)
#   - Enough activities to fill a full day (morning, afternoon, evening)
#   - Each NPC has activities across multiple time windows
#   - Economic loop: player earns enough for rent + story expenses
#     (e.g., 2 shifts/day at $70 = $140/day, rent is $200/week)
#
#   MULTI-NPC ADDITIONS:
#   - Activities can share locations across arcs (bar_floor: work + Mick)
#   - Shared unlock flags mean a tier unlocked in one arc enables it everywhere
#   - Mark highest-escalation nodes with loop_terminal = true
#   - Random encounters counted in activity balance (provide passive stat growth)
#   - Economic pressure: base tier income < rent (forces escalation)
#
# VALIDATION BEFORE PROCEEDING:
#   - All activity canvases are is_repeatable = true
#   - No activity canvas sets gate flags (only story events do)
#   - All gated choices reference valid flags and traits
#   - All escalation nodes are reachable from base node choices
#   - All terminal exits return to trigger or specific location
#   - Schedule coverage: activities exist for morning, afternoon, evening
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 11: PHASE 4 — STORY ARC
# ═══════════════════════════════════════════════════════════════════════════════
#
# INPUT: Book Phase 6 (Story Arc) + All previous TOML phases
# OUTPUT: 4_story_arc.toml
#
# The story arc drives the Quest/Journal page. It shows the player
# what they've accomplished and hints at what's next.
#
# STEP 1: CHAPTERS
#   - One chapter per narrative act/phase in the Book
#   - order: sequential (0, 1, 2, ...)
#   - mood: matches Book's emotional tone for that act
#   - Keep descriptions concise (1-2 sentences)
#
# STEP 2: NODES
#   - One node per significant story beat
#   - chapter: which chapter this beat belongs to
#   - linked_canvas: the canvas ID that fires this beat
#   - linked_flag: the flag that marks this beat as complete
#   - journal_entry: what the journal shows when complete
#   - requires_nodes: which previous nodes must complete first
#   - is_milestone: true for major turning points
#   - npc: associated NPC slug (for quest page grouping)
#
#   LINKING RULES:
#   - linked_canvas → canvas ID (NOT "canvasId")
#   - linked_canvas_node → specific node within canvas (optional)
#   - linked_flag → the completion flag set by that canvas's exit
#   - If a canvas sets flag X, the story node should have linked_flag = X
#
# STEP 3: GROUPS
#   - For non-linear segments where player can do things in any order
#   - required_count: how many nodes in group must complete
#   - Nodes reference group via their "group" field
#   - Other nodes can require a group via "requires_group"
#
# STEP 3.5: BRANCH CONDITIONS (for path-variant arcs — optional)
#   - Use when an NPC has MULTIPLE story paths (not just within-canvas variants)
#   - The branch-point canvas sets a DIFFERENT flag per choice
#     (e.g., "chose_gentle" vs "chose_bold")
#   - Downstream story_arc nodes use branch_condition = "chose_gentle"
#     to be visible ONLY if that flag is set
#   - Nodes without branch_condition appear for ALL players (shared content)
#   - RECONVERGENCE: After branched content, use a group with required_count=1
#     containing one node per path. The shared continuation node uses
#     requires_group. Do NOT use requires_nodes across exclusive paths
#     (AND logic would deadlock).
#   - Recommend max 1-2 branch points per NPC (content multiplies per branch)
#   - See Pattern M in game_design_patterns.md for full TOML example
#
# STEP 4: EMOTION MAPPINGS
#   - One mapping per tracked relationship stat
#   - trait_owner: "npc" for relationship stats, "player" for personal stats
#   - default_npc: the NPC who owns this stat
#   - ranges: non-overlapping intervals with labels
#
#   Example:
#   [story_arc.emotion_mappings.love]
#   trait_owner = "npc"
#   default_npc = "npc_angela"
#   [[story_arc.emotion_mappings.love.ranges]]
#   min = 0
#   max = 20
#   label = "Stranger"
#   description = "She tolerates your presence"
#   [[story_arc.emotion_mappings.love.ranges]]
#   min = 21
#   max = 40
#   label = "Friend"
#   description = "She's warming up to you"
#   # ... more ranges ...
#
# STEP 5: HINTS
#   - stuck_threshold_minutes: how long before showing a hint (default 30)
#   - hint_style: "observation" (character notices something)
#   - Templates: condition-based hint text
#
#   Example:
#   [[story_arc.hints.templates]]
#   text = "Maybe I should help around the house more"
#   [story_arc.hints.templates.condition]
#   missing_trait = "trust"
#   gap_gte = 5
#
# VALIDATION BEFORE PROCEEDING:
#   - All linked_canvas values reference existing canvases
#   - All chapter references in nodes point to existing chapters
#   - All group references point to existing groups
#   - All requires_nodes references point to existing nodes
#   - Emotion ranges don't overlap within same trait
#   - Groups have enough member nodes for required_count
#   - No orphan nodes (every node belongs to a chapter)
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 12: PHASE 5 — VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
#
# INPUT: All TOML phases (1-4)
# OUTPUT: Validation report + auto-fixes
#
# Run through each category. Fix what you can, flag what you can't.
#
# ── CORE VALIDATION ──
#
# [ ] Valid TOML syntax
#     - All inline tables are single-line
#     - All strings properly quoted
#     - No unterminated arrays or tables
#
# [ ] All IDs lowercase_snake_case (^[a-z0-9_]+$)
#     - Auto-fix: lowercase + replace hyphens with underscores
#
# [ ] All IDs unique in scope
#     - Canvas IDs: unique across all canvases
#     - Node IDs: unique within their parent canvas
#     - Location IDs: unique across all locations
#     - NPC IDs: unique across all NPCs
#     - Chapter/group/node IDs: unique within story_arc
#
# [ ] schema_version = "0.2"
#
# [ ] starting_canvas references a valid canvas ID
#
# [ ] Starting canvas has NO trigger section
#
#
# ── CROSS-REFERENCE VALIDATION ──
#
# [ ] All location references are valid
#     - canvas.trigger.location → must exist in [[locations]]
#     - location.entry_from → must exist in [[locations]]
#     - location.parent → must exist in [[locations]]
#     - location.default_entry → must exist and be a child
#     - choice.locationId → must exist in [[locations]]
#     - exit_block.config.locationId → must exist in [[locations]]
#
# [ ] All NPC references are valid
#     - canvas.trigger.npc → must exist in [[npcs]]
#     - effects.npcId → must exist in [[npcs]]
#     - flagEffects.npcId → must exist in [[npcs]]
#     - conditions.npc_id → must exist in [[npcs]]
#     - dialog.props.npcId → must exist in [[npcs]]
#
# [ ] All node references are valid
#     - choice.nodeId format: "canvas_id.node_id"
#     - canvas_id must exist in [[canvases]]
#     - node_id must exist in that canvas's [[canvases.nodes]]
#
# [ ] All flag references exist in flag_keys
#     - Scan all conditions for flag_key values
#     - Scan all flagEffects for flag values
#     - Every flag must appear in player.flag_keys or relevant NPC.flag_keys
#     - Auto-fix: add missing flags to flag_keys
#
# [ ] All trait references exist in core_traits
#     - Scan all conditions for trait_key values
#     - Scan all effects for trait values
#     - Every trait must exist in player.core_traits or relevant NPC.core_traits
#     - Note: traits referenced as NPC traits must be in NPC.core_traits
#
# [ ] All clip UUIDs preserved from Book
#     - If Book contained clip blocks with UUIDs, verify they exist in TOML
#
#
# ── CANVAS VALIDATION ──
#
# [ ] Flag chains valid
#     - Group all non-repeatable canvases by trigger location
#     - Each group must form a proper chain (no competing canvases)
#     - At most ONE canvas in each group can have no flag condition
#
# [ ] No dead ends
#     - Every canvas is reachable (via trigger or node reference)
#     - Every exit leads somewhere valid
#     - Every node within a canvas is reachable from the base node
#
# [ ] Stat thresholds achievable
#     - Verify that stat requirements in conditions can be reached
#       through available activities and events
#     - Check: highest love threshold vs total love available per day
#
# [ ] All non-repeatable canvases set a completion flag
#     - Every story event should set at least one flag on exit
#
#
# ── STORY ARC VALIDATION ──
#
# [ ] All linked_canvas values reference real canvases
# [ ] All chapter references in nodes point to existing chapters
# [ ] All group references point to existing groups
# [ ] All requires_nodes references point to existing story nodes
# [ ] Emotion ranges don't overlap within same trait
# [ ] Groups have enough member nodes for required_count
# [ ] Every story event canvas has a corresponding story_arc node
# [ ] branch_condition flags reference flags actually set by branch-point canvases
# [ ] Branching paths reconverge on shared nodes (no dangling paths)
# [ ] Reconvergence uses requires_group (not requires_nodes across exclusive paths)
#
# [ ] Every @-reference in content matches a defined NPC id (without npc_ prefix)
# [ ] Customizable NPCs have both relationship and relationship_options defined
# [ ] Default relationship value appears in relationship_options list
# [ ] ALL paragraph/heading content mentioning a customizable NPC uses @-syntax, not hardcoded names
#
#
# ── BALANCE VALIDATION ──
#
# [ ] Canvas mix reasonable
#     - ~40-50% activities (repeatable daily content)
#     - ~35-40% story events (one-time narrative beats)
#     - ~10-15% utility (chores, jobs, rest)
#
# [ ] Economic loop viable
#     - Player can earn enough for rent + story expenses
#     - Calculate: max daily income vs weekly expenses
#     - Flag if player can't afford rent within 7 days of starting
#
# [ ] Gate flags all set by story events
#     - No activity canvas should set gate flags
#     - Every gate flag has exactly one source event
#
# [ ] days_since_flag pacing reasonable
#     - No two consecutive story events require more than 5 days gap
#     - No event fires less than 1 day after its prerequisite
#
# [ ] Schedule coverage
#     - Activities exist for morning, afternoon, and evening
#     - Player always has something to do (no dead time windows)
#     - Time-advancement canvas available (rest/sleep)
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 13: FINAL COMPILATION
# ═══════════════════════════════════════════════════════════════════════════════
#
# After all phases are validated, compile into 6_final_game.toml.
#
# STEP 1: Create 6_final_game.toml
#
# STEP 2: Write sections in this order:
#   1. schema_version and starting_canvas
#   2. [project]
#   3. [time]
#   4. [player]
#   5. [[npcs]] (all NPCs)
#   6. [[locations]] (all locations)
#   7. [[canvases]] — starting canvas first, then story canvases,
#      then activities, then utility canvases
#   8. [story_arc]
#
# STEP 3: Add phase comments for readability:
#   # ═══ METADATA ═══
#   # ═══ LOCATIONS ═══
#   # ═══ STORY CANVASES ═══
#   # ═══ ACTIVITY CANVASES ═══
#   # ═══ UTILITY CANVASES ═══
#   # ═══ STORY ARC ═══
#
# STEP 4: Final TOML syntax check
#   - Verify the file parses without errors
#   - Count total canvases, nodes, locations, flags
#   - Report summary statistics
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#                    SECTION 14: COMMON MISTAKES TO AVOID
# ═══════════════════════════════════════════════════════════════════════════════
#
# 1. targetType = "canvas"
#    FIX: Use targetType = "node" with nodeId = "canvas_id.node_id"
#    There is NO "canvas" value for targetType.
#
# 2. destinationType = "canvas"
#    FIX: Only valid values are "trigger" or "specific"
#
# 3. "title" in story_arc chapters or nodes
#    FIX: Always use "name"
#
# 4. "canvasId" in story_arc nodes
#    FIX: Use "linked_canvas"
#
# 5. "summary" in story_arc nodes
#    FIX: Use "journal_entry"
#
# 6. Nodes array inside [[story_arc.chapters]]
#    FIX: Chapters don't contain nodes. Nodes reference chapters
#    via their "chapter" field.
#
# 7. Multi-line inline tables
#    FIX: Opening { and closing } must be on same line.
#    Arrays inside can span lines, but the braces cannot.
#
# 8. Multiple non-repeatable canvases at same location without flag chain
#    FIX: First has no flag condition. Each subsequent requires
#    the previous canvas's completion flag.
#
# 9. Treating "Day 1", "Day 2" from Book as literal labels
#    FIX: Translate to flag chain with days_since_flag for time gaps.
#
# 10. "npcName" in dialog blocks
#     FIX: Use props = { speaker = "npc", npcId = "npc_angela" }
#
# 11. Effects on exit_block level
#     FIX: For type="choices": effects inside each choice object.
#     For type="location": effects inside config dict.
#
# 12. Activity canvases setting gate flags
#     FIX: Only story events (is_repeatable=false) set gate flags.
#     Activities CONSUME gate flags via conditions but never set them.
#
# 13. Missing name field on nodes
#     FIX: Every [[canvases.nodes]] MUST have a name field.
#     It's human-readable and required by the parser.
#
# 14. Using npcId in conditions
#     FIX: Use npc_id (snake_case) inside condition items.
#     npcId (camelCase) is only for effects and dialog props.
#
# 15. Missing trigger_mode on random encounters
#     FIX: Use trigger_mode = "random" with chance = 0.7 (or appropriate value).
#     Without trigger_mode, the canvas fires as a normal manual trigger.
#
# 16. Clothing tier thresholds in shop UI don't match TOML conditions
#     FIX: Ensure shop tier labels show the same corruption value as
#     [[clothing]] conditions. If conditions say corruption >= 85,
#     the shop must label it "Bold (85+)" — not "Bold (80+)".
#
# 17. wardrobeEffects referencing non-existent clothing id
#     FIX: Every item_id in wardrobeEffects must match a [[clothing]] id
#     exactly. Cross-reference before finalizing.
#
# 18. Parallel arcs without staggered corruption bands
#     FIX: Ensure arcs start at different corruption levels so the player
#     always has 2-3 active options at any corruption level. Check for
#     dead zones where no arc is available.
#
# 19. Repeatable canvas in story_arc.nodes
#     FIX: Story arc nodes must link to non-repeatable canvases only.
#     Create a separate is_repeatable=false canvas for story milestones.
#     The story arc tracks narrative events, not daily activities.
#
# 20. Multiple repeatable canvases for same NPC at same location/time
#     FIX: Only ONE repeatable canvas per (location, NPC, schedule window).
#     Put multiple interaction types inside the canvas as gated choices.
#     The game renders one NPC portrait per canvas at each location.
#
# 21. Missing energy costs on repeatable activities
#     FIX: Every repeatable NPC/bonding activity needs costs = [{ trait = "energy", value = X }].
#     Match cost to physical intensity (meals=10, cooking=20, pool=30).
#     Restorative activities (sleep, shower) are FREE — no costs line.
#     Story events (is_repeatable=false) must NOT have costs.
#
# 22. Adding costs to story events
#     FIX: Story events auto-fire and must never be blocked by resource costs.
#     Only add costs to repeatable activities (is_repeatable=true).
#
# 23. Using branch_condition when within-canvas branching suffices
#     FIX: If both choices lead to the same story outcome (same completion flag),
#     use Pattern F (within-canvas branching with same flag). Only use
#     branch_condition when the JOURNAL should show DIFFERENT entries per path.
#
# 24. Forgetting shared nodes after a branch point
#     FIX: After branch-specific nodes, add shared continuation nodes WITHOUT
#     branch_condition so both paths reconverge. Branches diverge, then merge.
#
# 25. Using requires_nodes across exclusive paths for reconvergence
#     FIX: requires_nodes is AND logic — ALL listed nodes must complete.
#     Nodes on mutually exclusive paths can't all complete. Use a group with
#     required_count=1 containing one node per path, then requires_group
#     on the reconvergence node.
#
# 26. More than 2 branch points per NPC
#     FIX: Each branch point doubles the content needed for that segment.
#     Limit to 1-2 per NPC. Use within-canvas branching (Pattern F) and
#     group block variants for minor variations.
#
# 27. Hardcoding a customizable NPC's name in content instead of using @-syntax
#     WRONG: { type = "paragraph", content = "Ethan looks up." }
#     RIGHT: { type = "paragraph", content = "@ethan looks up." }
#
# 28. Using @npc_ethan instead of @ethan (including the npc_ prefix in @ reference)
#     WRONG: content = "@npc_ethan looks up."
#     RIGHT: content = "@ethan looks up."
#
# 29. Forgetting @.rel for relationship references
#     WRONG: content = "Your step-brother smiles."
#     RIGHT: content = "Your @ethan.rel smiles."
#
# 30. Setting customizable = true without defining relationship_options
#     Every customizable NPC needs: relationship (default) + relationship_options (player choices)
#
# ═══════════════════════════════════════════════════════════════════════════════
#
# END OF TOML GENERATION PROMPT V3
#
# ═══════════════════════════════════════════════════════════════════════════════
```

--- END OF TOML GENERATION PROMPT v3 ---

---


## 5. Game Design Rules

These are the authoritative design constraints that enforce "game feel" — the rules that prevent generated games from feeling like visual novels. Every game must follow these rules.

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

--- END OF GAME DESIGN RULES ---

---


## 6. Game Design Patterns

A catalog of optional design patterns — strategic templates for common game structures. These are not mandatory rules, but proven patterns for multi-route arcs, single-route chains, economic pressure, passive corruption, NPC trait triangles, clothing tiers, and more.

# Game Design Patterns (Reference Catalog)

These are **optional patterns** — use them when they match the type of game you're building. Not every game needs every pattern. Each pattern describes WHEN to use it, HOW it works, and provides full TOML examples from "New In Town" as reference.

---

## Pattern A: Multi-Route Parallel Arcs

**Use when:** The game has multiple NPCs/storylines the player pursues simultaneously. The player should feel like they're juggling multiple threads, discovering new content as they progress.

**Don't use when:** The game follows one character's journey with a single primary relationship. Use Pattern B instead.

### How It Works

- Multiple story arcs run in parallel across overlapping stat ranges (typically corruption)
- Each arc has its own progression chain (a sequence of one-time story canvases)
- Arcs share the same "ability unlock" flags (see Rules doc, Rule 3) — this creates cross-arc consistency
- The player always has 2-3 active arcs to choose from at any corruption level
- Arcs start at staggered corruption levels so new content keeps appearing as the player progresses

> **Note:** For path-divergent arcs where the journal shows different entries based on player choice within a single NPC's story, see Pattern M: Branching Story Paths. Most multi-NPC games get enough player agency from choosing WHICH NPC to pursue.

### The Staggering Principle

This is the most important design decision in multi-route games. If all arcs start at the same corruption level, the player is overwhelmed with options. If arcs don't overlap, the player has dead zones with nothing to do. Staggering means:

- **Early game (0-40):** Linear opening. Only 1 arc active (personal discovery). Establishes the world.
- **Mid-early (40-80):** 2-3 arcs overlap. Player starts making choices about where to spend time.
- **Mid game (80-140):** Peak overlap. All major arcs are active. Player feels busy and engaged.
- **Late game (140-220):** Arcs converge toward climaxes. Content gets more intense across all arcs.

### Corruption Band Diagram (New In Town)

```
Corruption:  0    30    60    90    120   150   180   210   240
             |     |     |     |     |     |     |     |     |
Personal:    ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
             30 ──────── 60
Bar work:              ████████████████████████████████████████
                  65 ─────────────────────────────────── 220
Mick:             ████████████████████████████████████████████
             40 ──────────────────────────────────────── 220
Glory hole:       ██████████████████████████████████░░░░░░░░░░
             38 ─────────────────────────────── 190
Public:                          ██████████████████████████████
                           140 ────────────────────────── 220
Harlan:                    ████████████████████████████████████
                      100 ─────────────────────────────── 220
```

### Key Design Decisions

1. **Linear opening (corruption 0-35):** The first ~8 canvases are fully linear (forced sequence). This establishes the world, introduces key NPCs, and gets the player invested before the game opens up.

2. **The inciting event:** A specific story canvas marks the transition from linear to open. In New In Town, it's "The Lesson" (bar_lesson_learned) — after this, the player has a job, knows the NPCs, and can start pursuing multiple arcs.

3. **Shared unlock flags:** When the player unlocks `handjob_unlock` in the Mick arc, that same flag gates handjob options in Bar, Glory Hole, Public, and Harlan arcs. This means the player's investment in one arc directly benefits all others.

### TOML Example: Story Canvas Chain (Mick Arc)

Each canvas in the chain requires the flag from the previous canvas, plus a corruption threshold:

```toml
# Canvas 1: The Kiss (corruption 120, requires multiple flags + NPC stats)
[[canvases]]
id = "story_living_room_the_kiss"
name = "The Kiss"
is_repeatable = false

[canvases.trigger]
location = "loc_bar_living_room"
is_repeatable = false
priority = 10
npc = "npc_mick"

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 },
  { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "seen_mick_shower", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "discovered_teasing", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 20 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 20 }
]

# ... nodes with narrative content ...
# Final node sets flag: flagEffects = [{ targetType = "player", flag = "first_kiss_mick" }]


# Canvas 2: The Couch (corruption 150, requires kiss flag + higher NPC stats)
[[canvases]]
id = "story_living_room_the_couch"
name = "The Couch"
is_repeatable = false

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 160 },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 30 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 25 },
  { type = "trait", subject = "npc_mick", trait_key = "corruption", operator = "gte", value = 40 }
]

# ... nodes ...
# Final node sets: flagEffects = [{ targetType = "player", flag = "touched_mick" }]
# Also sets handjob_unlock which enables handjob choices in ALL arcs
```

### Corruption Milestone Table (Full Reference)

This shows every event across all arcs in New In Town, sorted by corruption level:

| Corruption | Event | Arc | Type |
|-----------|-------|-----|------|
| 30 | Restless Night | Personal | One-time |
| 38 | Glory Hole Discovery | Glory Hole | One-time |
| 40 | First Porn | Personal | One-time |
| 40 | Watch Porn | Personal | Repeatable |
| 42 | Glory Hole Learning | Glory Hole | One-time |
| 48 | Glory Hole Listening | Glory Hole | Repeatable |
| 50 | How To (seduction research) | Personal | One-time |
| 65 | Flirt for tips | Bar | Activity choice |
| 65 | Seduce customers | Bar | Activity choice |
| 65 | Flirt with Mick | Mick | Activity choice |
| 70 | Glory Hole Watching | Glory Hole | One-time |
| 90 | The Bend (teasing) | Mick | One-time |
| 90 | Show off for tips | Bar | Activity choice |
| 90 | Tease Mick | Mick | Activity choice |
| 110 | Groping | Bar | Activity choice |
| 110 | The Floorboard | Mick | One-time |
| 120 | The Kiss | Mick | One-time |
| 120 | Kiss Mick | Mick | Activity choice |
| 130 | The Towel | Mick | One-time |
| 140 | First Flash | Public | One-time |
| 140 | The Rush (repeatable flash) | Public | Repeatable |
| 150 | Dirty Talk | Public | One-time |
| 150 | The Couch (Mick handjob) | Mick | One-time |
| 160 | Bar Handjob | Bar | Activity choice |
| 160 | Glory Hole Handjob | Glory Hole | One-time |
| 160 | Street Handjob | Public | One-time |
| 160 | Rush Handjob | Public | Activity choice |
| 190 | The Counter (Mick blowjob) | Mick | One-time |
| 190 | Glory Hole Blowjob | Glory Hole | Repeatable |
| 190 | Rush Blowjob | Public | Activity choice |
| 220 | The Room (Mick sex) | Mick | One-time |
| 220 | Bar Sex | Bar | Activity choice |
| 220 | Street Sex | Public | One-time |

Notice how at corruption 160, the player has handjob options in FOUR different arcs simultaneously. This is the payoff of shared unlock flags.

---

## Pattern B: Single-Route Linear Chain

**Use when:** The game follows one character's story with one primary arc. Good for focused, intimate narratives where the player deepens a single relationship.

**Don't use when:** You want the player to juggle multiple storylines. Use Pattern A instead.

### How It Works

- One main story chain: flag A -> flag B -> flag C -> ...
- Activities still have tiered choices (Rule 1 always applies)
- Random encounters add ambient atmosphere but don't branch the story
- NPC relationships deepen along the single path
- Economic pressure (Pattern C) can still drive the narrative forward

> **Note:** Single-NPC games are the best candidates for Pattern M: Branching Story Paths — the player commits to one NPC but can define HOW they pursue them.

### Key Difference from Multi-Route

No cross-arc flag sharing needed. Unlock flags can be arc-specific since there's only one arc. The tiered activity system still applies — the player still grinds daily activities between story beats — but there's only one story thread to follow.

### Structure Example

```
Story beats:    A → B → C → D → E → F → G → H → I → J
                |   |   |   |   |   |   |   |   |   |
Activities:     [grinding between each beat with tiered choices]
Random enc:     [ambient atmosphere scattered throughout]
```

> See also Pattern N for making the NPC's name and relationship customizable by the player.

---

## Pattern C: Economic Pressure as Motivation

**Use when:** You want the player to feel organically pushed toward corruption/escalation without being forced. The game should make the player do the math themselves — never lecture them.

**Don't use when:** The game doesn't involve money or resource management. Some games can use other pressure systems (time pressure, reputation, etc.).

### How It Works

- Give the player limited starting money and recurring expenses (rent, textbooks, etc.)
- Make the "honest route" mathematically impossible (minimum wage < rent)
- Higher-corruption activities pay dramatically more
- The player does the math themselves — the game doesn't lecture

### The Math Must Be Tight

This is critical. The numbers have to be designed so that:
1. The player CANNOT survive on the base-tier activity alone
2. Each tier up makes survival noticeably easier
3. The highest tiers provide financial freedom
4. The player figures this out organically — the game never says "you should try flirting"

### TOML Example (New In Town Economy)

**Setup:**
```toml
[player]
core_traits = { corruption = 0, confidence = 0, money = 500, intelligence = 5 }

[settings.rent]
enabled = true
amount = 150          # Due every Monday
due_day = "Monday"
collector_npc = "npc_mick"
grace_periods = 1     # 1 week grace before consequences
```

**The Impossible Math:**
- Starting money: $500
- Weekly rent: $150
- Base work shift: $35/night, ~5 nights/week = $175/week
- After rent: $25/week for food, textbooks, everything else
- Textbooks cost ~$300 for the semester

The player quickly realizes: basic bar work barely covers rent. There's nothing left for food or school supplies. Something has to give.

**The Escalation Ladder:**
```
$35/shift  → Work the shift (honest)     → barely covers rent
$55/shift  → Flirt for tips              → covers rent + food
$90/shift  → Show off                    → comfortable
$120/shift → Let him grope you           → saving money
$200/shift → Handjob in the bathroom     → ahead
$300/shift → Blowjob in the bathroom     → financial freedom
$500/shift → Take him out back           → wealthy
```

The beauty: the game never tells the player to flirt. The rent bill does.

### Rent Payment Canvas Example

```toml
[[canvases.nodes]]
id = "n2"
name = "Paying Rent"
exit_block = { type = "choices", choices = [
  { text = "Pay the rent ($150)",
    targetType = "trigger",
    effects = [{ targetType = "player", trait = "money", op = "add", value = -150 }],
    flagEffects = [{ targetType = "player", flag = "rent_paid" }]
  }
] }
```

---

## Pattern D: Passive Corruption via Random Encounters

**Use when:** You want the world itself to shift the player's comfort level. The player isn't doing anything — they're just witnessing things that the environment normalizes.

**Don't use when:** The game takes place in a "normal" environment where there's nothing to witness. This pattern works best in settings where the environment itself is corrupt (bars, rough neighborhoods, etc.).

### How It Works

- Random encounter canvases trigger with a probability (e.g., 70%) when entering a location
- The player **witnesses** something — no interaction, no choice to engage
- Each encounter adds a small amount of corruption (+2-3)
- Encounters can be one-time or repeatable, limited to 1/day
- Creates the feeling that the environment is normalizing behavior

### Why Small Amounts Matter

Random encounters should add +2-3 corruption, not +10-20. The point is ambient normalization, not rapid progression. Over many days, these small increments accumulate and push the player past thresholds they wouldn't have reached through story alone. It feels organic — the player doesn't notice the slow drift until they suddenly qualify for a choice they couldn't access before.

### TOML Example: Random Encounter

```toml
[[canvases]]
id = "random_room_restless_night"
name = "Restless Night"
description = "Emma can't sleep. The sounds from downstairs filter through the floorboards."

[canvases.trigger]
location = "loc_bar_emma_room"
trigger_mode = "random"     # <-- Triggers randomly
chance = 0.7                # <-- 70% probability
is_repeatable = true        # <-- Can happen again
max_triggers_per_day = 1    # <-- But only once per day

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "bar_groped", operator = "is_true" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 30 }
]

[[canvases.nodes]]
id = "n1"
name = "Sounds Through the Floor"
blocks = [
  { type = "paragraph", content = "She hears it again. The muffled sounds from downstairs — laughter, clinking glasses, and something else. A rhythm she's learning to recognize." }
]
exit_block = { type = "choices", choices = [
  { text = "Pull the pillow over your head", targetType = "trigger",
    time_progression_minutes = 60,
    effects = [{ targetType = "player", trait = "corruption", op = "add", value = 2 }]  # <-- Small increment
  }
] }
```

### Good Random Encounter Ideas

- Seeing a couple in an alley while walking home
- Hearing sounds through thin walls at night
- Finding someone's forgotten phone with photos open
- Witnessing other bar workers flirting for tips
- Overhearing a conversation you weren't meant to hear
- Walking past an open door at the wrong moment

The key: the player does NOTHING. They just see/hear. The corruption comes from exposure, not action.

---

## Pattern E: NPC Trait Triangle (Love/Trust/Corruption)

**Use when:** An NPC has a relationship arc with physical escalation. The player needs to invest emotionally, build comfort, AND push boundaries — all three.

**Don't use when:** An NPC is purely functional (shopkeeper, quest giver) or only appears in one scene.

### How It Works

Three independent relationship stats per NPC:

- **Love** — emotional connection, gates romantic milestones (kissing, intimacy, pillow talk)
- **Trust** — comfort/vulnerability level, gates intimate settings (being alone together, private spaces)
- **Corruption** — willingness to cross lines, gates sexual escalation (physical acts, intensity)

Story canvases require **all three** above minimum thresholds. This prevents speed-running — you can't just max corruption without building love and trust first.

### TOML Example: NPC Definition

```toml
[[npcs]]
id = "npc_mick"
name = "Mick"
description = "47, Jolene's husband. Runs the business side of the bar..."
portrait = "mick.jpg"
core_traits = { love = 0, trust = 10, corruption = 0 }
# trust starts at 10 — he's not hostile, just reserved
flag_keys = []
```

### How Stats Are Built

Different activities build different stats:

| Activity | Builds |
|----------|--------|
| Having breakfast together | Love +2 |
| Working together in stockroom | Trust +2 |
| Flirting with him | Corruption +1, Love +1 |
| Teasing him | Corruption +2 |
| Watching TV together | Love +1, Trust +1 |

### Story Canvas Gate Example

```toml
# The Kiss requires love, trust, AND corruption from separate activities
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 20 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 20 },
  { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" }
]
```

### The Triangle Prevents Speed-Running

Without the triangle, a player could:
- Spam "tease Mick" to max corruption -> get sex scene without any emotional context
- Or spam "watch TV" to max love -> get romantic scenes without any physical chemistry

With the triangle, the player MUST:
- Build love (breakfast, TV, conversation) AND
- Build trust (working together, helping out) AND
- Build corruption (teasing, flirting, physical escalation)

All three investment types are needed. This creates a relationship that feels earned.

> Customizable NPCs (Pattern N) should use @-syntax in all content blocks that reference NPC names.

---

## Pattern F: Corruption-Tiered Clothing/Wardrobe

**Use when:** The game has a clothing system that reflects character progression. As the player's corruption increases, bolder clothing becomes available and affordable.

**Don't use when:** Clothing isn't relevant to the game's themes.

### How It Works

- **4 tiers** matching corruption milestones: Basic (0), Cute (45), Bold (85), Daring (135)
- `body_coverage` rules with conditional relaxation tied to story flags
- Wardrobe items can be added via story events (NPC gifts) using `wardrobeEffects`
- Shop location gated behind a story event (e.g., `mall_unlocked` flag)

### TOML Example: Tier Structure

**Initial wardrobe (what the player starts with):**
```toml
[[clothing]]
id = "hoodie"
name = "Hoodie"
slot = "top"
image = "images/clothing/hoodie.jpg"
initial = true     # <-- Player starts with this

[[clothing]]
id = "jeans"
name = "Jeans"
slot = "bottom"
image = "images/clothing/jeans.jpg"
initial = true

[[clothing]]
id = "sneakers"
name = "Sneakers"
slot = "shoes"
image = "images/clothing/sneakers.jpg"
initial = true

[[clothing]]
id = "basic_bra"
name = "Basic Bra"
slot = "bra"
image = "images/clothing/basic_bra.jpg"
initial = true

[[clothing]]
id = "cotton_panties"
name = "Cotton Panties"
slot = "underwear"
image = "images/clothing/cotton_panties.jpg"
initial = true
```

**Tier 1 — Basic (no corruption gate, cheap):**
```toml
[[clothing]]
id = "shop_tshirt"
name = "T-Shirt"
slot = "top"
initial = false
price = 15
# No conditions — always available in shop
```

**Tier 2 — Cute (corruption >= 45):**
```toml
[[clothing]]
id = "shop_crop_top"
name = "Crop Top"
slot = "top"
initial = false
price = 30
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 45 }
] }
```

**Tier 3 — Bold (corruption >= 85):**
```toml
[[clothing]]
id = "shop_low_cut_top"
name = "Low-Cut Top"
slot = "top"
initial = false
price = 45
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 85 }
] }
```

**Tier 4 — Daring (corruption >= 135):**
```toml
[[clothing]]
id = "shop_sheer_blouse"
name = "Sheer Blouse"
slot = "top"
initial = false
price = 60
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 135 }
] }
```

### Body Coverage Rules

The clothing system enforces coverage requirements that relax as the player progresses:

```toml
[settings.clothing_requirements]
body_coverage = true              # Player must wear clothes
always_required = ["shoes"]       # Always need shoes

# Bra required until player learns seduction
[settings.clothing_requirements.conditional.bra]
until_flag = "learned_seduction"
message = "Emma isn't ready to go braless yet."

# Underwear required until player discovers teasing
[settings.clothing_requirements.conditional.underwear]
until_flag = "discovered_teasing"
message = "Emma isn't bold enough to go without underwear yet."
```

This creates a visual progression: the player starts in a hoodie and jeans, gradually transitions to crop tops and short skirts, and eventually can wear sheer blouses and micro skirts. The clothing reflects the character's internal journey.

### Important Implementation Note

The tier thresholds in the shop UI MUST match the TOML `conditions` values exactly. If the shop says "Tier 3: Corruption 40+" but the actual TOML condition is `corruption >= 85`, players will see items they can't buy and think it's a bug.

---

## Pattern G: Location Container Architecture

**Use when:** Your game world has buildings or areas that contain multiple sub-locations (a bar with a floor, stockroom, upstairs, etc.).

### How It Works

- **Top-level locations** (City Streets, The Bar, Campus) connect to each other
- **Container locations** (`is_container = true`) hold sub-locations but aren't directly "visited"
- **Sub-locations** connect via `entry_from` (which location the player comes from) and `navigation_order` (which locations they can go to)
- Each sub-location binds to specific activities/canvases
- NPCs feel "present" at locations via the `npc` trigger field

### TOML Example: The Bar (Container with Sub-Locations)

```toml
# THE BAR — Container (not directly visited)
[[locations]]
id = "loc_the_bar"
name = "The Bar"
description = "Jolene and Mick's bar. Ground floor is the drinking room. Upstairs is where they live — and where Emma rents a room."
is_container = true               # <-- This is a container
parent = ""
entry_from = "loc_city_streets"   # <-- Reached from city streets
default_entry = "loc_bar_floor"   # <-- Player enters here by default
navigation_order = []             # <-- Empty — player navigates via sub-locations

# BAR FLOOR — First sub-location (default entry point)
[[locations]]
id = "loc_bar_floor"
name = "Bar Floor"
description = "Long bar top, eight stools, a few tables..."
is_container = false
parent = "loc_the_bar"            # <-- Belongs to The Bar
entry_from = ""                   # <-- No specific entry (it's the default)
navigation_order = ["loc_bar_stockroom", "loc_bar_upstairs", "loc_bar_bathroom"]

# STOCKROOM — Accessed from bar floor
[[locations]]
id = "loc_bar_stockroom"
name = "Stockroom"
description = "Behind the bar — cases of beer, spare kegs..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_floor"      # <-- Can only enter from bar floor
navigation_order = []             # <-- Dead end — must go back

# UPSTAIRS — Hub to living quarters
[[locations]]
id = "loc_bar_upstairs"
name = "Upstairs"
description = "A narrow hallway at the top of creaking stairs..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_floor"
navigation_order = ["loc_bar_living_room", "loc_bar_emma_room", "loc_bar_kitchen", "loc_bar_upstairs_bathroom"]

# EMMA'S ROOM — Leaf location
[[locations]]
id = "loc_bar_emma_room"
name = "Emma's Room"
description = "A rented room above the bar. Single bed, a desk by the window..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_upstairs"   # <-- Accessed from the upstairs hallway
navigation_order = []
```

### Navigation Flow

```
City Streets → The Bar (container, enters at Bar Floor)
                 ├── Bar Floor
                 │     ├── Stockroom (dead end)
                 │     ├── Bar Bathroom (dead end)
                 │     └── Upstairs (hub)
                 │           ├── Living Room
                 │           ├── Emma's Room
                 │           ├── Kitchen
                 │           └── Bathroom
                 └── (also connects back to City Streets)
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `is_container` | If true, this location holds sub-locations and isn't directly visited |
| `parent` | Which container this sub-location belongs to |
| `entry_from` | Which location the player enters this one from |
| `default_entry` | For containers: which sub-location the player enters first |
| `navigation_order` | Array of location IDs the player can navigate to from here |

---

## Pattern H: Story Arc Hints

**Use when:** The game is complex enough that players can get stuck — they don't know where to go or what to do next.

**Don't use when:** The game is purely linear and the next step is always obvious.

### How It Works

- `[[story_arc.hints.templates]]` with `missing_flag` and optional `required_flag` conditions
- Shows contextual hints based on the player's current flag state
- Tells the player WHERE to go and WHEN (location + time window)
- Hints appear when the player has been "stuck" for a configurable threshold

### The Logic

A hint shows when:
- `missing_flag` is NOT yet set (this is what the player hasn't done yet)
- `required_flag` IS set (this ensures the hint only shows when the player is ready)
- The player has been idle for `stuck_threshold_minutes`

### TOML Example

```toml
[story_arc.hints]
stuck_threshold_minutes = 30     # Show hints after 30 minutes of no progress
hint_style = "observation"       # Hints are phrased as character observations

# Early game — points player to their room
[[story_arc.hints.templates]]
text = "It's getting late. Head back to your room — you've had a long day."
[story_arc.hints.templates.condition]
missing_flag = "first_night_complete"

# After settling in — points to the bar
[[story_arc.hints.templates]]
text = "The bar downstairs is quiet in the morning. Might be a good time to go down."
[story_arc.hints.templates.condition]
missing_flag = "met_mick"

# After meeting Mick — points to campus
[[story_arc.hints.templates]]
text = "College starts soon. You should head toward campus."
[story_arc.hints.templates.condition]
missing_flag = "campus_started"

# After campus — points to job hunting
[[story_arc.hints.templates]]
text = "Normal jobs aren't cutting it. Maybe there's work closer to home — like right downstairs."
[story_arc.hints.templates.condition]
missing_flag = "job_hunt_done"

# After bar lesson, before mall — uses required_flag to ensure proper sequence
[[story_arc.hints.templates]]
text = "Jolene mentioned something about your clothes. Try walking through the city streets during the day."
[story_arc.hints.templates.condition]
missing_flag = "mall_unlocked"
required_flag = "bar_lesson_learned"    # <-- Only shows AFTER bar lesson

# Mid-game relationship hints
[[story_arc.hints.templates]]
text = "The way he looked at you during that movie... maybe next time you're alone with him, you don't have to wait for the screen."
[story_arc.hints.templates.condition]
missing_flag = "first_kiss_mick"
required_flag = "discovered_teasing"

# Late-game progression
[[story_arc.hints.templates]]
text = "The bar closes late. Sometimes it's just the two of you left to clean up."
[story_arc.hints.templates.condition]
missing_flag = "gave_blowjob"
required_flag = "touched_mick"
```

### Writing Good Hints

- **Be specific about location and time**: "Head to the bar in the evening" not "Go explore"
- **Use character voice**: The hint should sound like the player character thinking, not a game manual
- **Never spoil content**: Hint at what might happen, don't describe it
- **Use required_flag to prevent premature hints**: Don't tell the player to visit the professor before they've even been to campus

---

## Pattern I: Energy Budget Design

**Use when:** You want the player to make real decisions about how to spend their day. Energy prevents "do everything" gameplay where the optimal strategy is visiting every location in order.

**Don't use when:** The game is short/linear enough that the player should experience all content without friction.

### How It Works

- Player starts with 100 energy. Sleep resets to 100.
- Every repeatable activity costs energy (5-30, proportional to intensity)
- Activities are VISIBLE when too expensive, but blocked with a cost badge — the player sees what they're missing
- Budget math: ~4-5 activities per day without rest, 6-7 with a nap
- This forces daily prioritization: "Do I spend 30 energy on the pool, or save it for wine & talk tonight?"

### Energy Cost Tiers

| Tier | Cost | Activity Type | Examples |
|------|------|---------------|----------|
| Free | 0 | Restorative/passive | Sleep, shower, phone scroll |
| Minimal | 5 | Quick actions | Journal, get ready, wander |
| Light | 10 | Brief social/meals | Breakfast, lunch, goodnight, stargazing |
| Moderate-light | 15 | Longer activities | Dinner, movie night, video games |
| Moderate | 20 | Active/emotional | Cooking together, wine & talk, wedding planning |
| Heavy | 25 | Physical labor | Chores, manual labor |
| Very heavy | 30 | Extended physical | Pool, sports, swimming |

### What's Always Free

Three categories never cost energy:
1. **Restorative**: Sleep, shower, nap — these RESTORE energy
2. **Passive time-kill**: Phone scroll, waiting — these are zero-effort filler
3. **Story events**: Non-repeatable canvases must never be blocked by energy (narrative progression can't be gated by resources)

### Energy Restoration

Use existing effects system on exit choices:

```toml
# Full sleep — reset to 100
effects = [{ targetType = "player", trait = "energy", op = "set", value = 100, clamp = true }]

# Nap — restore 20
effects = [{ targetType = "player", trait = "energy", op = "add", value = 20, clamp = true }]

# Shower — restore 5-10
effects = [{ targetType = "player", trait = "energy", op = "add", value = 10, clamp = true }]
```

### Sidebar Display

Always add an energy bar to the sidebar so the player can track their budget:

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "energy"
label = "Energy"
max = 100
```

### Anti-Pattern: No Energy Costs

```toml
# BAD — Player can do everything every day. No decisions.
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
# No costs = no trade-offs = visual novel feel
```

**Reference:** Rule 10 in game_design_rules.md

---

## Pattern J: Meal Energy Restoration

**Use when:** The game has meal activities (breakfast, lunch, dinner) and an energy system. Meals should restore energy at their base tier, creating a meaningful choice between recovery and love.

**Don't use when:** The game doesn't have an energy system, or meals aren't part of the activity loop.

### How It Works

- Meal activities have **NO entry cost** (free to enter — eating shouldn't cost energy)
- **T1 choice** (the safe default) restores a small amount of energy alongside base love
- **T2+ choices** (escalation tiers) give love only, NO energy restoration
- This creates a real trade-off: eat at T1 to recover energy, or pick a higher tier for more love but burn the recovery opportunity

### The Trade-off

| Choice | Energy | Love | Strategy |
|--------|--------|------|----------|
| T1: "Have breakfast together" | +5 | +1 | Recovery: gain energy for later activities |
| T2: "Stand closer while cooking" | 0 | +2 | Invest: spend the recovery for more love |
| T3+: Higher tiers | 0 | +3-5 | Aggressive: skip recovery entirely for max love |

### Daily Impact

If the player eats all 3 meals at T1:
- Breakfast: +5 energy
- Lunch: +5 energy
- Dinner: +10 energy
- **Total: +20 energy/day** from meals alone

This extends the daily budget from ~4-5 activities to ~5-6, rewarding players who eat regularly.

### TOML Example

```toml
# Meal trigger — NO costs (free entry)
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
max_triggers_per_day = 1
priority = 1
# NOTE: No costs array — meals are free

# T1 choice — restores energy + gives love
{ text = "Have breakfast together", targetType = "trigger",
  time_progression_minutes = 45,
  effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },
    { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true }
  ] }

# T2 choice — love only, no energy
{ text = "Stand closer while he cooks", targetType = "node", nodeId = "breakfast.closer",
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "npc_ethan", trait_key = "love", operator = "gte", value = 15 },
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } }
```

### Restoration Values

| Meal | T1 Energy Restore | Reasoning |
|------|-------------------|-----------|
| Breakfast | +5 | Light meal, start of day |
| Lunch | +5 | Midday refuel |
| Dinner | +10 | Largest meal, evening recovery |

---

## Pattern K: NPC Portrait Interaction Model

**Use when:** Every game that uses repeatable NPC activities. This is the standard interaction model — players see who's available and click to interact.

### How It Works

When a player enters a location, the screen shows:
1. **Story events auto-fire first** (priority 10, non-repeatable) — unchanged
2. **Random encounters roll** (trigger_mode = "random") — unchanged
3. **NPC portraits appear** — one clickable circle per NPC with a valid repeatable canvas
4. **Solo activities** appear as text action buttons below the portraits
5. Player clicks a portrait → enters that NPC's activity canvas

### What the Player Sees

```
┌─────────────────────────────────┐
│          Kitchen                │
│                                 │
│   ┌──────┐     ┌──────┐       │
│   │ Ethan│     │ Linda│       │
│   │  (●) │     │  (●) │       │
│   │ ⚡15  │     │      │       │
│   └──────┘     └──────┘       │
│                                 │
│   [Make coffee alone]           │
│   [Check the fridge]            │
│                                 │
└─────────────────────────────────┘
```

- **Ethan's portrait** has a cost badge (⚡15) — this activity costs 15 energy
- **Linda's portrait** has no badge — this activity is free
- **Solo activities** below as text buttons

### Key Rules

1. **One portrait = one canvas** — enforced by canvas uniqueness (Rule 9)
2. **The `npc` field on the trigger** determines which portrait appears (Rule 6)
3. **Blocked activities** (not enough energy) show greyed-out portrait with cost badge — still visible, just not clickable
4. **Portrait source** comes from the `portrait` field in `[[npcs]]`
5. **Multiple interaction types** with the same NPC go INSIDE the canvas as gated tier choices, not as separate canvases

### TOML Requirements for Portraits

```toml
# NPC must have a portrait
[[npcs]]
id = "npc_ethan"
name = "Ethan"
portrait = "ethan.jpg"    # <-- Required for portrait display

# Activity must bind NPC via trigger
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"         # <-- Required: binds portrait to this canvas
is_repeatable = true
costs = [{ trait = "energy", value = 15 }]
```

### Anti-Pattern: Missing NPC Binding

```toml
# BAD — Scene involves Ethan but no npc field
# Result: Shows as a solo text button, not a portrait
[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
# npc field missing!
```

**Reference:** Rules 6, 8, 9 in game_design_rules.md

---

## Pattern L: Three-Choice Activity Format (Emotional / Physical / Neutral)

**Use when:** Every NPC activity in every game. This replaces the old flat tier ladder (T1→T8) as the standard activity structure.

**Don't use when:** Solo activities (sleep, shower, journal) — these are utility, not relationship interactions.

### The Problem It Solves

The old tier ladder showed all unlocked options simultaneously. The player always picked the highest available tier. There was no decision — just optimization. "I have 90 love, so I click the sex option" isn't a choice, it's a progress bar.

### How It Works

Every NPC activity presents exactly 3 choices at its base node:

| Choice | What It Does | Always Available? |
|--------|-------------|-------------------|
| **Emotional** | Conversation content. Builds love, may increase corruption. Story depth. | Yes |
| **Physical** | Opens sub-menu of unlockable intensity options (touch → kiss → sex). | After `lingering_touch_unlock` |
| **Neutral** | Quick exit with small love gain. Safe option. | Yes |

The player chooses an APPROACH, not an intensity level.

### Base Node Group Variants

The base node shows different opening content based on relationship phase. This makes every visit feel different — the same breakfast scene plays differently after the first kiss vs after Madison arrives.

Use 3-4 group variants, checked most-specific first:
1. Phase 5: `madison_arrived` (fiancée in the house — corruption/hiding)
2. Phase 4: `first_night_complete` (fully intimate — comfortable desire)
3. Phase 3: `first_kiss_done` (physical line crossed — giddy/nervous)
4. Default: Phase 1-2 (reconnecting — tentative/nostalgic)

### Emotional Sub-Node

Also uses group variants — the conversation topic changes per phase:
- Early game: Small talk, childhood memories
- Post-kiss: "Are we going to pretend it didn't happen?"
- Post-intimacy: "What happens when I leave?"
- Post-Madison: "Does she make you happy?"

Effects: +2 love typically, may +corruption depending on activity context.

### Physical Sub-Node

A choices node with progressively unlockable options:
- Touch (always available in physical — the physical gate itself requires `lingering_touch_unlock`)
- Flirt (after `flirt_unlock`)
- Kiss (after `kiss_unlock`)
- Manual (after `manual_unlock`)
- Oral (after `oral_unlock`)
- Sex (after `sex_unlock`)

Each choice leads to the existing tier content nodes (t2, t3, t4, t6, t7, t8).

### The Unlock Satisfaction

New physical options appear as the player progresses through story events. This preserves the "I unlocked something new!" feeling from the old tier system — but moves it inside the physical sub-menu instead of cluttering the base node with 8 buttons.

### TOML Example (Breakfast — abbreviated)

```toml
# Base node with group variants
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's already looking when you walk in. Looks away too fast." }
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light. Coffee already made. Two mugs." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him over coffee", targetType = "node", nodeId = "activity_breakfast.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_breakfast.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Just eat. Easy silence.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }
  ] }
] }
```

**Reference:** Rule 11 in game_design_rules.md

---

## Pattern M: Branching Story Paths (Arc-Level)

**Use when:** An NPC has meaningfully different story routes where the player's choice leads to different journal entries, different scenes, and different emotional outcomes — not just minor dialogue variations.

**Don't use when:** The branches only affect stat changes or dialogue tone within a single scene. Use Pattern F (within-canvas branching) for that. Also avoid in multi-NPC games where player agency already comes from choosing WHICH NPC to pursue (Pattern A) — adding per-NPC branching on top creates combinatorial explosion.

### The Three Levels of Branching

| Level | Mechanism | Journal Impact | Content Cost |
|-------|-----------|---------------|-------------|
| **Within-canvas** (Pattern F) | Both choices set SAME completion flag, different stat effects | Same journal entry for both paths | Low (2 exit nodes per branch) |
| **Conditional canvases** | Different canvases per path, same completion flag, group block variants on activities | Same journal entry, different scene content | Medium (2 canvases per branch point) |
| **Arc-level** (Pattern M) | Different flags per choice, `branch_condition` on story_arc nodes | Different journal entries per path | High (parallel story nodes + canvases) |

Use the lightest mechanism that achieves the desired player experience.

### How It Works

1. A **branch-point canvas** presents a meaningful choice (e.g., "support her decision" vs. "challenge her")
2. Each exit sets a **different flag** (e.g., `chose_support` vs `chose_challenge`) PLUS the **same completion flag** (e.g., `crossroads_complete`)
3. Downstream story arc nodes use `branch_condition` to specify which path they belong to
4. The journal only displays nodes whose `branch_condition` flag is set (or nodes with no `branch_condition`)
5. Activity group blocks check the path flag to show different narrative/media (existing system — no new feature needed)
6. After the branched segment, shared nodes (no `branch_condition`) reconverge the paths via a group with `required_count = 1`

### TOML Example

**Branch-point canvas:**

```toml
[[canvases]]
id = "elena_crossroads"
name = "The Crossroads"
[canvases.trigger]
location = "loc_park"
npc = "npc_elena"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" }
]

[[canvases.nodes]]
id = "the_choice"
name = "The Choice"
blocks = [
  { type = "paragraph", content = "She tells you about the offer — a year abroad. Her voice is shaking." }
]
exit_block = { type = "choices", choices = [
  { text = "Support her dream", targetType = "node", nodeId = "elena_crossroads.support_exit" },
  { text = "Ask her to stay", targetType = "node", nodeId = "elena_crossroads.stay_exit" }
] }

[[canvases.nodes]]
id = "support_exit"
name = "Support"
blocks = [
  { type = "paragraph", content = "You tell her to go. Her eyes fill with tears — and gratitude." }
]
exit_block = { type = "location", text = "Watch her leave", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [{ targetType = "player", flag = "chose_support" }, { targetType = "player", flag = "crossroads_complete" }], effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 3 }] } }

[[canvases.nodes]]
id = "stay_exit"
name = "Stay"
blocks = [
  { type = "paragraph", content = "You ask her to stay. She searches your face for a long time." }
]
exit_block = { type = "location", text = "Wait for her answer", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [{ targetType = "player", flag = "chose_stay" }, { targetType = "player", flag = "crossroads_complete" }], effects = [{ targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 3 }] } }
```

**Path-specific story canvases** (different canvas per path, same completion flag pattern):

```toml
# SUPPORT PATH: Elena's letters arrive
[[canvases]]
id = "support_letters_scene"
name = "Letters from Afar"
[canvases.trigger]
location = "loc_bedroom"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "chose_support", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "crossroads_complete", operator = "is_true" }
]
# ... nodes with letter-reading content, media, dialogue ...
# Exit sets: support_letters_complete

# STAY PATH: Tension builds
[[canvases]]
id = "stay_tension_scene"
name = "The Unspoken"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_elena"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "chose_stay", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "crossroads_complete", operator = "is_true" }
]
# ... nodes with tension content, different media ...
# Exit sets: stay_tension_complete
```

**Story arc nodes with `branch_condition`:**

```toml
[story_arc]
version = "1.0"

# Shared milestone (both paths see this)
[[story_arc.nodes]]
id = "crossroads"
name = "The Crossroads"
chapter = "chapter_2"
linked_canvas = "elena_crossroads"
linked_flag = "crossroads_complete"
npc = "npc_elena"
is_milestone = true
journal_entry = "She told me about the offer. I had to choose."

# SUPPORT PATH node (invisible unless chose_support is set)
[[story_arc.nodes]]
id = "support_letters"
name = "Letters from Afar"
chapter = "chapter_3"
linked_canvas = "support_letters_scene"
linked_flag = "support_letters_complete"
npc = "npc_elena"
branch_condition = "chose_support"
group = "path_resolution"
requires_nodes = ["crossroads"]
journal_entry = "Her letters arrive on Tuesdays. Each one makes me more certain."

# STAY PATH node (invisible unless chose_stay is set)
[[story_arc.nodes]]
id = "stay_tension"
name = "The Unspoken"
chapter = "chapter_3"
linked_canvas = "stay_tension_scene"
linked_flag = "stay_tension_complete"
npc = "npc_elena"
branch_condition = "chose_stay"
group = "path_resolution"
requires_nodes = ["crossroads"]
journal_entry = "She stayed. But something in her eyes changed."

# Reconvergence group — completes when ANY one path node completes
[[story_arc.groups]]
id = "path_resolution"
name = "Path Resolution"
required_count = 1

# Shared continuation (both paths see this)
[[story_arc.nodes]]
id = "reunion"
name = "What We Built"
chapter = "chapter_4"
linked_canvas = "reunion_scene"
linked_flag = "reunion_complete"
npc = "npc_elena"
requires_group = "path_resolution"
journal_entry = "Whatever road we took, it led here."
```

**Activity group block variants** (existing feature — different narrative/media per path):

```toml
# Breakfast activity shows different content based on path
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  # SUPPORT PATH: wistful, missing her
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "chose_support", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The kitchen feels empty without her. Her mug is still in the dish rack." },
    { type = "video", props = { file = "activities/breakfast_alone_wistful.webm" } }
  ] },
  # STAY PATH: charged silence
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "chose_stay", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She's already at the table. Doesn't look up when you walk in." },
    { type = "video", props = { file = "activities/breakfast_tension.webm" } }
  ] },
  # Default (before branch point)
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light. Coffee already made. Two mugs." },
    { type = "video", props = { file = "activities/breakfast_default.webm" } }
  ] }
]
# Same 3 choices: Emotional / Physical / Neutral — unchanged
```

### Design Guidance

- **Branch points should happen mid-game** — the player needs to know the NPC before making a meaningful path choice
- **Each path needs 3-4 unique story nodes minimum** to feel meaningfully different
- **Paths should differ in tone and content**, not just stat rewards
- **Journal entries per path** should reflect the player's approach and emotional state
- **Emotion mappings stay the same** across paths — the traits are identical, only the journey differs
- **Activity content** uses existing group blocks for path-variant narrative and media — no new feature needed

### Anti-Pattern: Branching at Every Story Beat

```toml
# BAD — 5 branch points creates 2^5 = 32 paths. Unsustainable content.
# Use within-canvas branching (Pattern F) for minor variations.
# Reserve branch_condition for 1-2 major path-defining decisions.
```

### Anti-Pattern: Paths That Only Differ by Stats

```toml
# BAD — If gentle path gives +2 love and bold path gives +3 love,
# that's Pattern F (within-canvas branching with same flag).
# Don't use branch_condition for this — the journal entry is the same.
```

**Reference:** Rule 7 in game_design_rules.md

---

## Pattern N: Customizable NPC Names

**Use when:** NPCs have relationships to the player that players might want to personalize — step-siblings, roommates, housemates, landlords. Especially common in single-NPC intimate games.

**Don't use when:** NPC identity is tightly coupled to plot points (e.g., a character whose name is a clue), or when different relationship types would require fundamentally different narrative content (use group blocks for that).

### Schema

```toml
[[npcs]]
id = "npc_ethan"
name = "Ethan"                                          # default name
customizable = true                                      # enables customization screen
relationship = "step-brother"                            # default relationship label
relationship_options = ["step-brother", "roommate", "landlord"]  # player choices
description = "Late 20s, tall, athletic build."
portrait = "ethan.jpg"
core_traits = { love = 0, trust = 0, corruption = 0 }
flag_keys = []
```

### Content Writing with @-syntax

**Paragraph blocks** — use `@npc_short` for name, `@npc_short.rel` for relationship:
```toml
{ type = "paragraph", content = "@ethan is already in the kitchen when you come downstairs." }
{ type = "paragraph", content = "Your @ethan.rel pours you a cup of coffee without asking." }
{ type = "paragraph", content = "@ethan's hand brushes yours as he passes the mug." }
```

**Dialog blocks** — speaker name is automatic via `npcId`. Content can use `@` for other NPCs:
```toml
{ type = "dialog", content = "Morning. Sleep okay?", props = { speaker = "npc", npcId = "npc_ethan" } }
```

**Emotion mapping descriptions** — use `@` for NPC names:
```toml
[[story_arc.emotion_mappings.love.ranges]]
min = 0
max = 25
label = "Acquaintance"
description = "@ethan is polite but reserved around you"
```

### Three Levels of Content Variation

| Level | Mechanism | Example |
|-------|-----------|---------|
| **Name swap** | `@ethan` | "@ethan looks up" → "Mike looks up" |
| **Relationship label** | `@ethan.rel` | "Your @ethan.rel" → "Your roommate" |
| **Narrative divergence** | Group blocks + flags | Different paragraph content per relationship type |

For most games, name + relationship label swaps are sufficient. Use group blocks only when the relationship type fundamentally changes the scene dynamics.

### Design Guidelines

1. **Relationship options must be narratively compatible** — "Your @ethan.rel pours coffee" should make sense whether the relationship is "step-brother", "roommate", or "housemate"
2. **Avoid relationship-specific plot points in @.rel text** — don't write "Your @ethan.rel reminds you of Mom" (only works for step-brother)
3. **1-2 customizable NPCs max per game** — more creates a confusing customization screen
4. **Default name should be the canonical name** — the name used in marketing, screenshots, etc.
5. **Content budget: zero extra** — @-syntax is a find-and-replace, not content duplication

### Anti-patterns

- **Mixing hardcoded and @-syntax for the same NPC** — if an NPC is customizable, ALL references must use `@`. Even one hardcoded "Ethan" breaks immersion when the player renamed them.
- **Relationship options that require different narrative framing** — "step-brother" vs "coworker" implies completely different living situations. Use group blocks for this level of variation.

--- END OF GAME DESIGN PATTERNS ---

---


## 7. Game Feel Analysis

Post-launch analysis of why generated games feel like visual novels instead of actual games, with root cause diagnosis, architecture gap analysis, and tracked solutions (some marked as SOLVED, others still pending).

# Game Feel Analysis: Why Our Games Feel Like Visual Novels

> **Date**: March 2026
> **Context**: Post-launch analysis after Jack's World and New In Town
> **Purpose**: Reference document for future game design iterations
> **Status**: Items 1-2 fully implemented, Items 3-4 mostly complete (March 2026)

---

## 1. Player Feedback (Raw)

Source: ChiefNut's Discord thread, March 17 2026.

**ChiefNut** (prompt):
> So far we've been making short games like Jack's World and New in Town. Some feedback we've seen is that they feel more like visual novels — mostly just clicking through scenes — and not really like a full game. That got us thinking... what actually makes something feel like a real game? More choices? Exploration? Stats? Mini-games?

**MrWhysper [OGoA]**:
> The line between VN and game is a really thin one. To be a game, your choices have to make a difference, but if your choices make a difference people will bitch that they don't get to see all content in a single playthrough. You'll never make everyone happy so just make the game/VN you want to and hope that your audience is satisfied.

**Jonas132**:
> There has to be a feeling of being in some sort of control, even through meaningless choices, or some kind of friction through minigames or navigating or sandbox mechanics.

### Key Takeaways

| Who              | Core Insight                                                   | Design Implication                                                            |
| ---------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| MrWhysper        | Choice paradox: meaningful choices = missed content complaints | Perception of consequence matters more than actual branching                  |
| Jonas132         | Control comes from friction, not content                       | Even meaningless friction (navigation, resource management) creates game feel |
| General feedback | "Clicks after clicks"                                          | The core loop is passive content consumption, not active decision-making      |

---

## 2. Current System Audit

### The Pipeline

```
Game Design Book (markdown, ~50-80 pages)
    ↓ [toml_generation_prompt_v2.txt / v3.txt — human + AI collaboration]
TOML Phase Files (5 phases + final merge)
    ↓ [package_from_toml management command]
    ↓   parse_toml() → normalize() → validate()
    ↓   create_project_from_template() → Django ORM objects
    ↓   TweeComprehensiveGeneratorV1.generate() → Twee
    ↓   Tweego compile → HTML
    ↓   Media copy (R2 clips + local files)
Playable HTML Game (index.html + media/)
```

### What a Typical Play Session Looks Like

Tracing an actual play session in a generated game (e.g., Two Weeks):

1. **Game starts** → Intro canvas plays (text + media + dialog about arriving at the house)
2. **Released to world** → Player sees a **flat location list** in the sidebar (Kitchen, Living Room, Bedroom, Garden, etc.)
3. **Player clicks "Kitchen"** → The trigger system finds the highest-priority valid canvas for that location + current time
4. **Breakfast canvas auto-fires** → Player reads 3-4 paragraphs + sees media + reads dialog
5. **Exit choices appear** → "Eat together" (always available) + gated tiers if stats are high enough
6. **Player clicks "Eat together"** → love +1, time advances 45 minutes
7. **Back to location list** → Player clicks "Living Room"
8. **Nothing fires** (no valid canvas at this time) → Player sees basic location description
9. **Player clicks "Bedroom"** → Rest canvas fires → "Rest for a bit" (2 hrs) or "Go to sleep" (9 hrs)
10. **Time advances** → New day, repeat from step 2

### The Core Loop

```
Pick location → Canvas auto-fires (or nothing) → Read content → Click exit → Repeat
```

This is a visual novel with a location selection screen. The location selection adds a thin layer of choice, but it's not meaningful — the player is cycling through locations to trigger canvases.

**Optimal play is obvious and unchanging**: Visit every location, pick the highest available tier, sleep, repeat. There's no reason NOT to do this. There's no cost to visiting a location, no risk to picking the highest tier, no trade-off between activities.

---

## 3. Root Cause Analysis

### Root Cause 1: Zero Trade-offs in the Gameplay Loop

**The biggest issue.** In a real game, decisions have costs.

Current state:
- Visiting a location costs nothing (no energy, no risk, no movement time)
- Picking the highest unlocked tier is always the correct choice (no rejection, no consequences)
- Time passes per action, but there's no per-day action budget
- Activities don't compete meaningfully for the player's attention

The Two Weeks game has a 14-day countdown (`sidebar_items` type="countdown"). In theory, that's time pressure. In practice, the player has enough time to hit every activity every day because there are no action limits. The countdown becomes decoration.

**Where this lives in the codebase:**
- `time_progression_minutes` on choices/exits is the only cost mechanism
- No `energy` or `action_points` concept in the schema (`template_import.py:TemplatePlayer`)
- No per-day action limit in the trigger system

### Root Cause 2: Navigation Has No Friction

Jonas132's insight: "friction through navigating."

Current state:
- Locations render as a flat sidebar list in the generated HTML
- Click Kitchen → instant arrival → canvas fires
- Click Bedroom → instant arrival → canvas fires
- No sense of physical space, movement cost, or exploration

The schema supports `entry_from` hierarchies and `navigation_order`, and there are container locations with `is_container = true` and `default_entry`. But the Twee generator (`v1.py:_generate_simple_locations()` and `_generate_basic_navigation()`) renders these as a flat navigable list. The hierarchy exists in data but doesn't translate to meaningful exploration in gameplay.

**Where this lives in the codebase:**
- `template_import.py:TemplateLocation` — has `entry_from`, `navigation_order`, `is_container`, `parent`
- `v1.py:_generate_simple_locations()` — renders locations as flat passages
- `v1.py:_generate_basic_navigation()` — renders sidebar navigation

### Root Cause 3: Canvases Auto-Fire (Player Doesn't Choose Activities)

When the player clicks "Kitchen" at 8 AM and Ethan is there, the breakfast canvas fires automatically. The player didn't choose "have breakfast with Ethan" — the system chose for them based on trigger priority, conditions, and schedules.

The trigger system (`CanvasTrigger` model with `priority`, `conditions`, `schedules`) is a content delivery mechanism: it decides WHAT the player sees. But the player should be deciding what to DO.

In a game that feels like a game, arriving at the kitchen would show:
- "Ethan is here, making breakfast"
- Options: Talk to him / Help cook / Eat quietly / Leave

Instead, the current system fires one canvas and presents its content.

**Where this lives in the codebase:**
- `CanvasTrigger` model — `priority` field determines which canvas wins
- `v1.py:_generate_simple_locations()` — location passages check triggers and auto-display
- The trigger evaluation happens in generated SugarCube code, not player choice

### Root Cause 4: Choices Gate Content Tiers, Not Outcomes

Activity choices are escalation tiers: T1 → T2 → T3 → ... T8. The "choice" is: "do you have enough stats to see the next tier?" That's a progress bar disguised as a choice list.

Example from the activity pattern (from `toml_generation_prompt_v2.txt` Pattern A):
```
T1: "Eat together"     — always available (no conditions)
T2: "Stand closer"     — love >= 22
T3: "Kiss her"         — love >= 42 + kiss_unlocked
T4: "Get closer"       — love >= 62 + groping_unlocked
```

The player never thinks "should I kiss her or hold back?" They think "I unlocked kissing, so I'll click kiss because it gives more love." The choice is optimization, not expression.

Story event branches (e.g., `first_kiss` canvas: "Kiss her gently" vs "Pull her close") do have different stat rewards. But both branches set the same completion flag (`first_kiss_complete`), and the stat difference is minor (love +2 vs +3). The player perceives this as "which gives more?" not "what kind of relationship do I want?"

**Where this lives in the codebase:**
- `toml_generation_prompt_v2.txt` Section 10 — activity tier translation rules
- `game_design_rules.md` Rule 3 — "Flag-Gated Intensity Escalation"
- `game_design_rules.md` Rule 4 — "Dual Gating" (stat + flag, but both are progress gates)
- Both branches always set the same flag: `toml_generation_prompt_v2.txt` Pattern F

### Root Cause 5: NPCs Are Deterministic Vending Machines

NPCs exist at scheduled locations and respond identically every time. Ethan at the kitchen during breakfast always produces the same canvas. His `love` stat goes up, but his behavior doesn't change based on it (aside from unlocking higher tiers through stat gates).

Missing NPC behaviors:
- **No mood variation** — NPC always responds the same way
- **No memory of yesterday** — NPC doesn't reference recent events in dialog
- **No initiative** — NPC never seeks out the player
- **No scarcity** — NPC is always available at scheduled times, never busy or absent
- **No rejection** — Player can always pick the highest tier without risk

The `story_arc.emotion_mappings` system describes emotional states (e.g., love ranges: "family" → "remembering" → "comfortable" → "torn" → "gone"), but these are journal/UI descriptions. They don't change NPC behavior in canvases.

**Where this lives in the codebase:**
- `template_import.py:TemplateNPCSchedule` — deterministic location/time
- `template_import.py:TemplateEmotionMapping` — display-only, not behavioral
- `v1.py` — no NPC state-based dialog variation in canvas rendering
- NPC `core_traits` increment linearly; no trait-based behavior branching in generated Twee

---

## 4. Game vs Visual Novel Framework

### What Separates a Game from a VN

Three requirements for "game feel" based on the feedback and genre analysis:

#### 4a. Resource Tension

The player can't do everything. Limited resources force real decisions.

| Resource Type            | Creates                         | Example                                                    |
| ------------------------ | ------------------------------- | ---------------------------------------------------------- |
| Energy / Action Points   | "What do I do today?" decisions | 5 actions per day, each activity costs 1-2                 |
| Money with real pressure | Economic strategy               | Rent > base income, forcing job vs relationship trade-offs |
| Time with scarcity       | Prioritization                  | NPC events overlap, can't attend both                      |
| Reputation / Standing    | Social strategy                 | Helping one NPC might upset another                        |

Current system has `money` and `time_progression_minutes` but neither creates felt pressure. Money exists in Jack's World ($50 start, $200/week rent, $70/shift) — the math works out to "just work enough shifts." There's no moment where the player agonizes over spending.

#### 4b. Player-Initiated Interaction

The player chooses WHAT to do, not just WHERE to go. The distinction:

**VN pattern (current):**
```
Click "Kitchen" → System fires breakfast canvas → Read content → Exit
```

**Game pattern (target):**
```
Enter Kitchen → See: "Ethan is cooking. The sink is full of dishes."
→ Choose: [Talk to Ethan] [Help with dishes] [Make your own breakfast] [Leave]
→ Each choice leads to different canvas/content with different rewards
```

The difference: in the VN pattern, the system presents content. In the game pattern, the player constructs their experience from available options.

#### 4c. Visible World Response

When the player does something, the world visibly changes. Not just a number incrementing — the NPC says something different, a new option appears, a location changes.

**Current**: Player picks "Kiss her" → love +3, corruption +1 → same canvas tomorrow
**Game feel**: Player picks "Kiss her" → next morning Ethan avoids eye contact → different breakfast dialog → new story option unlocks

The `story_arc` system tracks narrative progression and the journal shows what happened. But the moment-to-moment gameplay doesn't reflect past choices. The player's history is invisible during regular activities.

---

## 5. Architecture Gap Analysis

### Current Implementation vs Game Feel

| Game Element            | Current Implementation                                          | Why It Feels VN-Like                | What a Game Would Do                                                              |
| ----------------------- | --------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------- |
| **Location navigation** | Flat sidebar list (`v1.py:_generate_simple_locations`)          | No sense of space or movement cost  | Map-based navigation with travel time, locked areas, discoverable locations       |
| **Activity selection**  | Auto-trigger by `CanvasTrigger.priority`                        | Player doesn't choose what to do    | Show available activities at location, let player pick                            |
| **Choices**             | Stat-gated tiers (`conditions.items[]`)                         | Optimization, not expression        | Choices with trade-offs: each option has a cost, not just a gate                  |
| **Time system**         | `time_progression_minutes` per action                           | No per-day action budget            | Energy system: X actions per day, sleep restores energy                           |
| **Money**               | `core_traits.money`, `clamp = false`                            | Trivially manageable                | Economic pressure where income < expenses, forcing hard choices                   |
| **NPCs**                | `TemplateNPCSchedule` (deterministic)                           | No personality, no unpredictability | NPC mood, random availability, memory of player choices                           |
| **Consequences**        | Different stat rewards on branches                              | No visible behavioral change        | Dialog variations, NPC reactions, unlocked/locked options based on history        |
| **Exploration**         | `entry_from` + `navigation_order` (data exists, flat rendering) | No discovery                        | Hidden events, locked rooms, items to find, secrets                               |
| **Failure states**      | None — player always succeeds                                   | No stakes                           | Rejection if stats too low, missed events, relationship damage from wrong choices |

---

## 6. Pipeline Gap Inventory

### 6a. TOML Schema Gaps (`template_import.py`)

Fields/concepts that **don't exist** but would be needed for game feel:

| Missing Concept                                | What It Would Enable                               | Current Closest                                            |
| ---------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| `player.max_energy` / `energy_cost` on actions | Per-day action limits                              | `time_progression_minutes` (time passes but doesn't limit) |
| `trigger.player_choice = true`                 | Player picks from available activities at location | `trigger.priority` (system auto-selects)                   |
| `npc.mood` / `npc.availability_variance`       | NPC unpredictability                               | `TemplateNPCSchedule` (deterministic)                      |
| `choice.rejection_threshold`                   | Failure when stats too low                         | `choice.conditions` (hides choice entirely)                |
| `choice.consequence_delay`                     | NPC reacts to past choices in future canvases      | No concept — each canvas is stateless                      |
| `location.discovery_conditions`                | Hidden locations that unlock through play          | `entry_conditions` (exists but rarely used)                |
| `canvas.variation_key`                         | Different content based on past choices            | Single content path per canvas                             |
| `exit_block.risk`                              | Chance of failure/rejection                        | Deterministic outcomes only                                |

### 6b. Twee Generator Gaps (`v1.py`)

Generator behaviors that produce VN-feel:

| Current Behavior                                     | Game Alternative                                                                   |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `_generate_simple_locations()` renders flat list     | Render location as scene with visible NPCs, available actions, environmental state |
| `_generate_basic_navigation()` renders sidebar links | Render map-style navigation with travel costs, locked indicators                   |
| Canvas auto-fires when location conditions met       | Show "things you can do here" menu, let player pick                                |
| Choices render as simple buttons                     | Render choices with visible costs/risks/rewards preview                            |
| No state-based text variation                        | Dialog varies based on relationship level, recent events, time of day              |
| `_generate_story_canvases()` — one path per canvas   | Support canvas variants keyed on past choices                                      |

### 6c. Prompt Gaps (`toml_generation_prompt_v2.txt` / `v3.txt`)

Design patterns the prompts teach that reinforce VN-feel:

| Current Pattern                                             | What It Produces                                | Game Alternative                                            |
| ----------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| Pattern A: Escalating Activity                              | Linear tier ladder (T1→T8)                      | Branching activity with multiple paths and trade-offs       |
| Pattern E: Time Advancement                                 | "Rest" / "Sleep" buttons                        | Energy management: rest restores energy, sleep advances day |
| Pattern F: Story Event branches                             | Both branches set same flag, different stats    | Branches lead to meaningfully different future events       |
| Section 10 activity rules: "ONE canvas per activity"        | Single content path with gated tiers            | Multiple canvas variants based on context/history           |
| `game_design_rules.md` Rule 1: Tiered Activity System       | Safe default + escalation ladder                | Activities with risk/reward trade-offs at every tier        |
| `game_design_rules.md` Rule 2: Story vs Activity separation | Clean but rigid — activities never affect story | Activities can trigger story consequences                   |

### 6d. Game Design Rules Gaps (`game_design_rules.md`)

Rules that are missing entirely:

| Missing Rule                     | What It Would Enforce                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Resource Budget Rule**         | Every day has limited actions; player must prioritize                                            |
| **Consequence Propagation Rule** | Choices in activities affect future NPC dialog/availability                                      |
| **Discovery Rule**               | Some content requires exploration, not just stat grinding                                        |
| **Failure/Rejection Rule**       | Attempting actions above your level has consequences, not just hidden buttons                    |
| **NPC Agency Rule**              | NPCs sometimes initiate, sometimes are unavailable, sometimes react to player history            |
| **Trade-off Rule**               | Every meaningful choice must cost something (time, money, relationship with another NPC, energy) |

---

## 7. The Design Paradox

### MrWhysper's Paradox

> "If your choices make a difference people will bitch that they don't get to see all content in a single playthrough."

This is real. The adult game audience wants to see ALL content. Locking significant content behind mutually exclusive choices frustrates completionists.

### How Successful Games Handle It

The solution is **perceived consequence without actual content lockout**:

1. **Immediate NPC reactions** — After choosing "bold" path, the NPC says something surprised/flustered. The REACTION is different. The CONTENT (next scene) is the same or very similar. Player feels their choice mattered because the NPC acknowledged it.

2. **Flavor variations** — Same scene, different opening dialog based on what the player did yesterday. "I was thinking about last night..." vs "You seem different today..." The scene plays out the same way, but feels personalized.

3. **Short-term consequences, long-term convergence** — Bold choice → NPC avoids you for one activity cycle → then back to normal. The player felt a consequence. The content wasn't permanently locked.

4. **Stat rewards, not content gates** — Instead of hiding T3 behind a flag, show T3 but with a warning: "She might not be ready for this." If the player tries anyway, they get a rejection scene (still content! still engagement!) and a small stat penalty. They see the content either way, but the path to it matters.

5. **Multiple routes to same destination** — The player can build love through gifts, through helping, or through corruption. Different strategies, same progression. Each feels like a player-driven approach.

### The Key Insight

**Games don't need branching stories. They need branching MOMENTS.**

A branching story means: your choice at hour 2 changes what happens at hour 10. That's expensive to write and frustrating for completionists.

A branching moment means: your choice RIGHT NOW changes how the next 30 seconds play out. The NPC reacts, the dialog shifts, maybe a small stat bonus/penalty. Then the game converges back. The player felt agency. The author wrote one story with local variations.

---

## 8. Summary Table: What the Current System Does Well vs. What It Lacks

### Does Well
- Rich narrative content (text, dialog, media integration)
- Stat/flag-gated progression (complex condition system)
- Time-based scheduling (NPCs at locations at specific times)
- Story arc tracking with journal/quest system
- Multiple NPCs with independent stats
- Comprehensive validation pipeline (flag chains, reference checking, cycle detection)
- Clean authoring pipeline (TOML phases → merged file → game)

### Lacks (Updated March 2026)
- ~~**Resource tension**~~ — **SOLVED**: Energy costs system (Rule 10), trait_bar sidebar, cost badges on portraits
- ~~**Player-initiated interaction**~~ — **SOLVED**: NPC portrait interaction model (Rule 8), clickable portraits at locations
- ~~**Navigation friction**~~ — **SOLVED**: Interactive location screens with NPC portraits and solo activity buttons
- ~~**Meaningful choices**~~ — **SOLVED**: Three-choice activity format (Emotional/Physical/Neutral) replaces flat tier ladder (Rule 11). Energy forces daily prioritization. Group block variants make content phase-aware.
- **NPC personality** — Not addressed (needs schema changes: mood variation, memory)
- ~~**Visible consequences**~~ — **PARTIALLY SOLVED**: Group block variants enable phase-aware content. Base nodes and emotional nodes change based on relationship state (5 phases). Full NPC reaction system (mood, memory) still needs schema changes.
- **Failure states** — Not addressed (needs schema changes: rejection thresholds, risk)
- **Discovery** — Not addressed (needs schema changes: hidden locations, exploration rewards)

---

## 9. Reference: Codebase Locations

| Component            | File                                                            | Key Functions/Classes                                                                                      |
| -------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| TOML Parser & Schema | `apps/projects/services/template_import.py`                     | `parse_toml()`, `normalize()`, `validate()`, `GameTemplate`, all `Template*` dataclasses                   |
| DB Project Creation  | `apps/projects/services/template_import.py`                     | `create_project_from_template()`                                                                           |
| Package Command      | `apps/game_generation/management/commands/package_from_toml.py` | `Command.handle()`, 7-phase pipeline                                                                       |
| Twee Generator       | `apps/game_generation/twee_comprehensive/generators/v1.py`      | `TweeComprehensiveGeneratorV1.generate()`                                                                  |
| Game Service         | `apps/game_generation/services/game_service.py`                 | `GameService.package_game()`                                                                               |
| TOML Gen Prompt v2   | `prompts/toml_generation_prompt_v2.txt`                         | Patterns A-H, Sections 1-14                                                                                |
| TOML Gen Prompt v3   | `prompts/toml_generation_prompt_v3.txt`                         | Patterns I-L (random, multi-NPC, clothing, rent)                                                           |
| Game Design Rules    | `prompts/game_design_rules.md`                                  | Rules 1-6 (tiered activities, separation, flag gating, dual gating, schedules, NPC presence)               |
| Game Design Patterns | `prompts/game_design_patterns.md`                               | Patterns A-H (multi-route, single-route, economic, passive corruption, traits, clothing, locations, hints) |
| Book Prompt v5       | `prompts/game_book_prompt_v5.txt`                               | 7-phase game design book structure                                                                         |
| Book Prompt v6       | `prompts/game_book_prompt_v6.txt`                               | Multi-NPC architecture, flexible gates, clothing/rent                                                      |
| Django Models        | `apps/stories/models.py`                                        | `StoryCanvas`, `StoryNode`, `CanvasTrigger`, `TriggerSchedule`, `NodeConnection`                           |
| Block Conversion     | `apps/stories/services/block_conversion.py`                     | `BlockConversionService`                                                                                   |

---

*This document was written March 2026. All 4 infrastructure items have been implemented. Additionally, the group block variant system and 3-choice activity format (Emotional/Physical/Neutral) were built to address Root Causes 4 and 5. Remaining gaps (NPC personality, failure states, discovery) require further schema-level changes.*



Making it feel like a game requires changes at multiple levels:
  - ✅ **The TOML schema needs concepts that create friction** — Energy costs, trait_bar sidebar, costs parsing (Rule 10)
  - ✅ **The Twee generator needs interactive location screens** — NPC portraits, solo activities, cost badges (Rule 8)
  - ✅ **The Twee generator needs group block variants** — Conditional content rendering via `<<if>>/<<elseif>>/<<else>>` chains
  - ✅ **Activities need meaningful choice structure** — 3-choice format: Emotional/Physical/Neutral (Rule 11, Pattern L)
  - ✅ **The prompts need to guide designers toward systemic thinking** — Updated with energy patterns, canvas uniqueness, meal restoration, 3-choice pattern (Pattern A0)
  - ✅ **The game design rules need patterns for trade-offs** — Rules 7-11 added (story arc, portraits, uniqueness, energy, 3-choice format)

--- END OF GAME FEEL ANALYSIS ---

---


## 8. Simulation Upgrade Plan

Comparative analysis against Course of Temptation (CoT) by Anthaum — identifies 8 advanced systems we haven't implemented yet, with detailed implementation priorities and phased rollout plan.

# Simulation Upgrade Plan

## What We Learned from Course of Temptation

Reference game: **Course of Temptation** by Anthaum (anarchothaumaturgist)
- 3,027 paid Patreon members, $7,426/month
- Twine/SugarCube engine, text-only, free game with early-access monetization
- Solo developer, monthly updates since July 2023 (now v0.7.7)
- 4.7/5 stars (1,817 ratings on itch.io)

---

## Part 1: What CoT Does That We Don't

### 1.1 NPC Memory System

**What CoT does:**
NPCs remember specific events — flashing at a party, encounters at bars, wardrobe malfunctions. Memories are stored per-NPC as event logs with day stamps. NPCs reference memories in future dialogue ("That time you flashed the boys at a party... They'll remember, and it'll matter").

**What we have:**
NPCs are stat containers: `{ love: 0, trust: 0, flags: {} }`. No event log. No ability to reference past interactions. Every canvas visit is a blank slate from the NPC's perspective.

**What we need:**
- Per-NPC memory array: `$npcs[id].memory = [{ event: "saw_player_flash", day: 14, location: "party", severity: "high" }]`
- Memory-aware dialogue: blocks that check NPC memory before selecting text
- Memory decay: old memories fade or get replaced (keep memory arrays bounded)
- Memory formation: after each canvas, automatically log significant events

---

### 1.2 NPC Attitudes & Reactions

**What CoT does:**
NPCs have attitudes toward the player (and other NPCs) that change based on observed behavior. NPCs can refuse dates if your inclinations clash with theirs. NPCs can break up with you, confront you about cheating, or act differently based on their current emotional state.

**What we have:**
NPCs have static traits (love, trust) that only change via authored `effects` in canvas choices. NPCs never initiate anything. NPCs have no opinion about player behavior — they only respond when the player enters their authored canvas.

**What we need:**
- Per-NPC attitude value: `$npcs[id].attitude` (tracks current feeling toward player: -100 to 100)
- Attitude modifiers from events: witnessing bad behavior decreases attitude, positive interactions increase it
- Attitude-gated dialogue: NPCs respond warmly or coldly based on attitude, not just love/trust stats
- NPC-initiated interactions: certain attitude thresholds trigger NPC-initiated events (confrontation, breakup, confession)

---

### 1.3 Reputation System

**What CoT does:**
"Earn a reputation: Sometimes people talk and secrets don't stay secret." Player popularity tracked as `reputation["popularity"]["student"]`. Actions observed by NPCs propagate through a gossip network. Multiple NPCs learn about player behavior even if they weren't present.

**What we have:**
Nothing. There is no reputation tracking. No gossip. No consequence spreading beyond the specific canvas where an action occurred.

**What we need:**
- Player reputation object: `$player.reputation = { exhibitionist: 0, slut: 0, kind: 0, reliable: 0 }`
- Reputation categories that map to player behavior patterns
- Gossip propagation: when an NPC witnesses something, nearby NPCs or friends learn about it over time
- Reputation-gated content: certain events, dialogue, or NPC attitudes unlock/change based on reputation
- Reputation display: player can see how the world perceives them

---

### 1.4 Needs System (Survival Bars)

**What CoT does:**
Left sidebar shows: Rest, Relaxation, Bladder, Hygiene, Food. These decay over time and must be managed. Low values cause negative consequences (passing out from exhaustion, social penalties from low hygiene). Creates a resource management layer that drives location visits.

**What we have:**
No needs system. Player has no reason to visit locations except to chase story events. No urgency, no resource management, no daily survival loop.

**What we need:**
- Needs bars: `$player.needs = { energy: 100, hunger: 100, hygiene: 100 }`
- Hourly decay: on each `advanceTime()` call, reduce needs by configurable rates
- Need-consequence thresholds: low energy = can't work, low hygiene = NPC attitude penalty, low hunger = stat debuffs
- Need-fulfillment activities: eating (kitchen), sleeping (bedroom), showering (bathroom) — these become mandatory daily activities that create natural location visits
- Configurable per-game: some games may want needs, others may not

---

### 1.5 Inclination / Personality Discovery System

**What CoT does:**
65 personality traits ("inclinations") organized in prerequisite trees. Players earn them through repeated behavior — not from menus or story choices. Example: do exhibitionist things enough times at Exhibitionism skill 2+ and you become a "Lewd Exhibitionist." Each inclination changes how ALL existing content plays (new dialogue, new reactions, new options). The game tells you who your character has become.

Inclination trees create layered progression:
- Exhibitionism: Lewd → Cautious → Proud → Helpless (each requires higher skill + prior inclination)
- Dom/Sub: Forward → Dominant → Dominant Vibe (or Accommodating → Submissive → Submissive Vibe)
- Relationships: Fuckbuddy → Casual Hookup → Hatefuck (each requires higher Disinhibition)

**What we have:**
Single-axis stats (corruption, love, trust) with binary flag gates. No personality discovery. No emergent character identity. Player never "becomes" anything — they just unlock more choices.

**What we need:**
- Inclination data model: `$player.inclinations = { exhibitionist: false, voyeur: false, ... }`
- Hidden progress tracking: `$player.inclination_progress = { exhibitionist: { count: 0, threshold: 10 } }`
- Auto-discovery: when threshold reached + prerequisite inclinations held, inclination unlocks with notification
- Inclination-aware conditions: new condition type `{ type: "inclination", key: "exhibitionist", operator: "is_true" }`
- Inclination effects on existing content: dialogue variants, new choice visibility, NPC reaction modifiers
- Prerequisite chains: inclination B requires inclination A to be true
- Configurable per-game: game designer defines available inclinations, thresholds, and prerequisite trees

---

### 1.6 Temporary State Modifiers

**What CoT does:**
Disinhibition skill gates can be temporarily lowered through intoxication (alcohol, smoking) or arousal (low release bar, "Always Horny" inclination). This means content is dynamically accessible based on character condition, not just permanent progression. Creates "I can't believe I did that" moments organically.

**What we have:**
All gating is permanent and binary. Once you meet a threshold, the choice is always visible. No temporary states that alter what's available.

**What we need:**
- Temporary modifier system: `$player.modifiers = { drunk: 0, aroused: 0 }`
- Modifier sources: drinking at bar, certain events, items
- Modifier effects on gating: in `triggerConditionsSatisfied()`, apply modifier offsets to trait comparisons
- Modifier decay: modifiers decrease over time (sober up after X hours)
- Modifier-aware content: dialogue and descriptions change when player is drunk/aroused
- Configurable per-game: designer defines which modifiers exist and how they affect gates

---

### 1.7 Dynamic Dialogue (Content Pools)

**What CoT does:**
"A universal system for grabbing semi-random and reactive lines of dialogue" that works across encounters, phone texts, and random events. NPCs comment based on current actions, skill level, inclinations, appearance, and clothing. Dialogue is assembled from pools of valid lines, not static scripts. The same situation produces different dialogue based on game state.

**What we have:**
Every `paragraph` and `dialog` block contains fixed text written at author-time. The same canvas always shows the exact same dialogue. No variation, no state-awareness in text content.

**What we need:**
- New block type: `dialog_pool` — contains multiple dialogue variants with conditions
  ```toml
  { type = "dialog_pool", props = { speaker = "npc", npcId = "npc_angela", pool = [
    { content = "Good morning!", conditions = { items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "gte", value = 30 }] } },
    { content = "Oh. You're here.", conditions = { items = [{ type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "love", operator = "lt", value = 10 }] } },
    { content = "Morning.", conditions = {} }
  ] } }
  ```
- Pool selection logic: evaluate conditions top-to-bottom, pick first match (or random from valid set)
- State-reactive paragraphs: `paragraph_pool` for narrative text that changes based on state
- Memory-reactive dialogue: dialogue options that reference NPC memory
  ```
  "You seem different since that party..." (requires: npc.memory contains "party_incident")
  ```

---

### 1.8 Encounter / Interaction Compositor

**What CoT does:**
Full encounter system that assembles scenes from components:
- Space-aware: knows what furniture is in the room (desk, bed, chair, wall)
- Position system: available positions depend on furniture (can't do "bent over desk" if no desk)
- Skill-gated acts: acts require skill thresholds AND prerequisite acts
- Role asymmetry: low-skilled characters can't initiate but can participate if NPC leads
- Mid-encounter events: interrupts can fire during scenes (someone walks in, new partner joins)
- NPC preferences: NPCs have favorite positions as personality traits

**What we have:**
Canvases are self-contained, isolated scenes. No awareness of physical environment. No dynamic composition. No mid-scene interrupts. Every interaction is fully pre-scripted.

**What we need (long-term):**
- Location properties: `$locations[id].furniture = ["bed", "desk", "chair"]`
- Template scenes: canvas-like structures that query location properties to determine available interactions
- Interrupt system: while in a canvas, check for interrupt events (NPC walks in based on schedule + location)
- This is the most complex addition and should be deferred to later phases

---

### 1.9 NPC Schedule Simulation

**What CoT does:**
NPCs move between locations on their own schedules independently. When you go to a location, the NPCs currently present there are dynamically determined. You might find Angela in the kitchen in the morning but the living room in the evening.

**What we have:**
Canvas triggers have a `npc` field that binds an NPC to a location at certain times, but the NPC doesn't actually "exist" at that location independently. They only appear when their canvas fires. You can't just bump into someone.

**What we need:**
- NPC schedule data: `setup.npc_schedules[npcId] = [{ location: "loc_kitchen", start: "07:00", end: "10:00", weekdays: [0,1,2,3,4] }]`
- Location NPC presence query: `setup.getNpcsAtLocation(locationId)` checks current time against all NPC schedules
- NPC display at locations: when entering a location, show which NPCs are currently present (with portraits)
- Ambient interaction: option to talk/interact with present NPCs even without a specific canvas for it
- NPC-NPC co-presence: track when multiple NPCs are at the same location (enables jealousy, gossip)

---

### 1.10 Event Probability & Variety

**What CoT does:**
"Hundreds of events mean you can never be sure exactly what will happen." The game is "very, very RNG dependent." Events fire based on location + time + state + skill thresholds + probability rolls. The same location visit can produce completely different events on different days.

**What we have:**
`trigger_mode = "random"` with `chance` probability exists for random encounters. But most canvases are deterministic — if conditions are met, the same canvas always appears. Limited event variety per location.

**What we need:**
- More random encounter support: expand the random event pool per location
- Event weighting: events have weight values, higher weight = more likely to fire
- Event cooldowns: events that fired recently are suppressed for X days
- Event chains: random events that lead to follow-up random events days later
- Ambient events: small flavor events (no choices, just narrative) that make locations feel alive
- Event variety metrics: build tool that warns when a location has too few events for its visit frequency

---

## Part 2: What We Already Have That CoT Doesn't

### 2.1 Rich Media (Our Biggest Advantage)
CoT is 100% text. We support video, images, GIFs, and clips embedded in every scene. This is a massive differentiator. A simulation with video would be unique in this space.

### 2.2 AI-Assisted Content Generation
Our TOML pipeline + prompts can generate entire games. CoT is hand-coded over years. We can iterate much faster.

### 2.3 Structured Data Model
Our TOML schema is clean and parseable. Adding new systems means extending the schema and the generator — not rewriting spaghetti SugarCube code.

### 2.4 Clothing / Wardrobe System
Already implemented with tiers, conditions, shop, and equip/unequip.

### 2.5 Story Arc / Journal
Structured narrative tracking with chapters, nodes, and journal entries. CoT has no equivalent quest journal.

### 2.6 Economic System
Rent, jobs, economic pressure already built. CoT has similar but not more sophisticated.

---

## Part 3: Implementation Priority

### Phase 1: NPC Memory + Attitudes (Highest Impact, Moderate Effort)
**Why first:** This single change transforms games from "static scenes" to "living characters." Every existing canvas feels different when NPCs remember and react.

**Scope:**
- Add `memory[]` array to NPC state initialization
- Add `attitude` value to NPC state
- Create `setup.recordMemory(npcId, event, severity)` JS helper
- Auto-record memories when canvases complete (based on canvas metadata)
- Add `memory_check` condition type to `triggerConditionsSatisfied()`
- Add `dialog_pool` block type for memory-reactive dialogue
- Extend TOML schema: canvas metadata for memory recording, dialog_pool blocks
- Extend template_import.py normalization and validation
- Extend v1.py generator to emit memory system JS and handle new block types

**Data model changes:**
```toml
# In NPC definition
[[npcs]]
id = "npc_angela"
core_traits = { love = 0, trust = 0 }
attitude = 0          # NEW: current feeling toward player (-100 to 100)
memory_capacity = 20  # NEW: max memories stored (oldest dropped)

# In canvas definition — what to remember when this canvas completes
[canvases.memory_effects]
target_npc = "npc_angela"
event_tag = "caught_staring"
severity = "medium"        # low, medium, high
affects_attitude = -5       # attitude change on memory formation

# In blocks — dialog that checks memory
{ type = "dialog_pool", props = { speaker = "npc", npcId = "npc_angela", pool = [
  { content = "I saw what you did the other day...", conditions = { items = [
    { type = "npc_memory", npc_id = "npc_angela", event_tag = "caught_staring", operator = "exists" }
  ] } },
  { content = "Morning!", conditions = {} }
] } }
```

**Runtime additions (v1.py generated JS):**
```javascript
// Record a memory for an NPC
setup.recordMemory = function(npcId, eventTag, severity, data) {
    var npc = State.variables.npcs[npcId];
    if (!npc) return;
    npc.memory = npc.memory || [];
    npc.memory.push({
        event: eventTag,
        severity: severity,
        day: State.variables.game_state.time_state.day,
        location: State.variables.player.current_location,
        data: data || {}
    });
    // Enforce capacity limit
    var cap = npc.memory_capacity || 20;
    while (npc.memory.length > cap) npc.memory.shift();
};

// Check if NPC has a specific memory
setup.npcHasMemory = function(npcId, eventTag) {
    var npc = State.variables.npcs[npcId];
    if (!npc || !npc.memory) return false;
    for (var i = 0; i < npc.memory.length; i++) {
        if (npc.memory[i].event === eventTag) return true;
    }
    return false;
};
```

---

### Phase 2: Needs System (High Impact, Small Effort)
**Why second:** Creates the daily survival loop that drives location visits. Without needs, players only visit locations for story content. With needs, they visit locations because they MUST eat, sleep, and shower — creating natural encounter opportunities.

**Scope:**
- Add needs config to TOML: `[player.needs]` with bar names, starting values, decay rates
- Add needs bars to sidebar display (like trait display)
- Add hourly decay in `advanceTime()` function
- Add need-consequence thresholds (too hungry = debuff, too tired = pass out)
- Add need-fulfillment canvases (eat, sleep, shower) as utility canvas pattern
- Extend condition system for need checks

**Data model changes:**
```toml
[player.needs]
energy = { value = 100, decay_per_hour = 4, warning = 25, critical = 10 }
hunger = { value = 100, decay_per_hour = 3, warning = 20, critical = 5 }
hygiene = { value = 100, decay_per_hour = 2, warning = 30, critical = 15 }
```

---

### Phase 3: Temporary Modifiers (High Impact, Small Effort)
**Why third:** Small code change, big gameplay impact. Being drunk temporarily lowers skill gates — creates emergent "I did something I wouldn't normally do" moments.

**Scope:**
- Add `$player.modifiers = {}` to state init
- Add modifier sources (drinking canvas, items, events)
- Modify `triggerConditionsSatisfied()` to apply modifiers as trait offsets
- Add modifier decay in `advanceTime()`
- Add modifier display in sidebar

**Data model changes:**
```toml
# Modifier sources in canvas effects
effects = [
  { targetType = "player", modifier = "intoxication", op = "add", value = 30, decay_per_hour = 10 }
]

# Modifier impact on gating (in game config)
[settings.modifiers]
intoxication = { affects_trait = "inhibition", direction = "lower", ratio = 0.5 }
# When intoxication = 30, inhibition gates effectively lowered by 15
```

---

### Phase 4: Dialogue Pools (Medium Impact, Medium Effort)
**Why fourth:** Makes existing content feel dynamic. Same canvas, different text depending on state. First step toward "content that assembles itself."

**Scope:**
- New block types: `dialog_pool`, `paragraph_pool`
- Pool selection engine in JS runtime
- TOML schema extension for pool blocks
- Generator extension to emit pool-aware rendering
- Prompt updates for game book and TOML generation

---

### Phase 5: Reputation System (Medium Impact, Medium Effort)
**Why fifth:** Builds on NPC memory (Phase 1). Once NPCs remember things, reputation is just aggregating those memories into categories and propagating them.

**Scope:**
- Reputation categories defined per-game
- Auto-categorization from memory events
- Gossip propagation: NPCs share memories with connected NPCs over time
- Reputation-gated content and dialogue

---

### Phase 6: Inclination / Personality System (High Impact, Large Effort)
**Why sixth:** Most complex system but transforms replayability. Requires Phases 1-5 to be meaningful (inclinations need memory, needs, and dialogue pools to actually change gameplay).

**Scope:**
- Inclination definitions with prerequisites and hidden thresholds
- Behavior tracking (count specific actions)
- Auto-unlock with notification
- Inclination-aware conditions throughout
- Inclination effects on NPC reactions
- Prompt updates for full integration

---

### Phase 7: NPC Schedules & Presence (Medium Impact, Medium Effort)
**Why seventh:** Makes the world feel populated. NPCs exist at locations independently of canvases.

**Scope:**
- NPC schedule data in TOML (already partially supported)
- Location presence query at runtime
- NPC portraits shown at locations
- Ambient interaction options with present NPCs
- NPC-NPC co-presence tracking

---

### Phase 8: Encounter Compositor (High Impact, Very Large Effort)
**Why last:** Most architecturally complex. Requires parameterized scene templates instead of authored canvases. Fundamental shift from content-player to content-assembler.

**Scope:**
- Location furniture/properties
- Template scene format (compose from components)
- Position system based on available furniture
- Mid-scene interrupt system
- This phase may require a new generation system (`twee_simulation/`) alongside `twee_comprehensive/`

---

## Part 4: Architecture Notes

### Where Changes Go

| Change | Files Affected |
|--------|---------------|
| TOML schema | `template_import.py` (dataclasses, normalize, validate) |
| Runtime JS | `twee_comprehensive/generators/v1.py` (generated JavaScript) |
| Condition system | `triggerConditionsSatisfied()` in v1.py |
| New block types | `_convert_blocks_to_game_html()` in v1.py |
| State initialization | `_generate_initialization()` in v1.py |
| Time system hooks | `_generate_time_system()` in v1.py |
| Sidebar display | `StoryCaption`, widget definitions in v1.py |
| Game design prompts | `game_book_prompt_v7.txt`, `toml_generation_prompt_v4.txt` |
| Validation | `validate_game_toml.py` management command |
| Game design rules | `game_design_rules.md`, `game_design_patterns.md` |

### Backward Compatibility
All new features must be **opt-in** via TOML configuration. Existing games with no needs, no memory, no inclinations must continue to work unchanged. The generator should check for feature flags and only emit relevant JS when features are enabled.

### Our Advantage: Media + Simulation
CoT proves simulation works in text-only. Nobody has combined simulation mechanics with rich media (video/images). Our path: take CoT's systems thinking, apply it to our media-rich engine, and produce something that doesn't exist in this space yet.

---

## Part 5: CoT Technical Reference

### Data Structures (from Console Hacks)
```javascript
// Main state container
SugarCube.State.variables  // aliased as V

// NPC data
V.people["name"]           // NPC object with inclinations, attitudes, memory
V.pendingaddrelationships   // Relationship state tracking

// Reputation
reputation["popularity"]["student"]  // Player popularity score

// Functions
setup.Relationships.qualifying(name)     // Check available relationship types
setup.Streaming.set_popularity(site, val) // Career system
SugarCube.Engine.play("SCENENAME")       // Direct passage navigation
```

### CoT Patreon Model
| Tier | Price | What They Get |
|------|-------|---------------|
| Free | $0 | Full game, all content |
| Student | $2/mo | Early access (1 week), weekly dev diaries |
| Teacher Assistant | $5/mo | Voting polls on dev direction |
| Professor | $10/mo | VIP Discord channel |

Key: game is free. Monetize community + early access. 3,027 paying on a free game.

### CoT Update Cadence
Two parallel cycles:
1. Monthly content updates (extending existing systems)
2. Major roadmap updates (new mechanics that fundamentally change gameplay)

Feature priority determined by $5+ patron polls.

### CoT Feature Timeline (for reference)
| Version | Feature |
|---------|---------|
| v0.2 | NPC dating and hangouts |
| v0.3 | Social media and streaming career |
| v0.4 | Campus sports, professor interactions |
| v0.5 | Official relationships, exclusivity, breakups, jealousy |
| v0.6 | Bar job, dialogue framework, mid-encounter events |
| v0.7 | Greek house parties, sports expansion, art/photography |

--- END OF SIMULATION UPGRADE PLAN ---

---


## 9. Reference Example TOML (University City)

This is a complete reference game in TOML schema v0.2. It demonstrates all major patterns: project metadata, player/NPC definitions, location hierarchy, starting canvas (no trigger), story event canvases, activity canvases with gated choices, and story arc with chapters/nodes/emotion mappings.

```toml
############################################
# game_example.toml — schema v0.2
# Reference example using v2 patterns:
#   - Single-canvas activities with gated choices
#   - 4 gate flags (kiss, groping, oral, sex)
#   - loc_ and npc_ ID prefixes
#   - No NPC schedules (auto-detected at runtime)
#   - Starting canvas has NO trigger
############################################

schema_version = "0.2"
starting_canvas = "intro_canvas"

# ═══════════════════════════════════════════════════════════════════════════════
#                              PROJECT
# ═══════════════════════════════════════════════════════════════════════════════

[project]
id = "university_city"
title = "University City"
description = """
A vibrant university town where study halls, coffee houses, and hidden
archives interconnect. Your choices shape friendships, knowledge, and
access to the city's secrets.
"""

# ═══════════════════════════════════════════════════════════════════════════════
#                              TIME
# ═══════════════════════════════════════════════════════════════════════════════

[time]
enabled = true
starting_hour = 9
starting_day = "Tuesday"
starting_week = 1

# ═══════════════════════════════════════════════════════════════════════════════
#                              PLAYER
# ═══════════════════════════════════════════════════════════════════════════════

[player]
id = "player"
name = "Avery"
description = "A driven first-year student eager to explore."
portrait = "player_avery.jpg"
core_traits = { intelligence = 65, charisma = 40, stamina = 55, curiosity = 72 }
flag_keys = [
  "game_started",
  "met_barista",
  "has_student_id",
  "met_librarian",
  "joined_study_group",
  "first_kiss_complete",
  "kiss_unlocked",
  "study_session_complete",
  "groping_unlocked",
  "oral_unlocked",
  "sex_unlocked"
]

# ═══════════════════════════════════════════════════════════════════════════════
#                              NPCS
# ═══════════════════════════════════════════════════════════════════════════════
#
# NPC schedules are auto-detected from canvas trigger data at runtime.
# Do NOT define [[npcs.schedules]] — they are not needed.

# NPC Customization: When customizable = true, the game shows a screen at start
# where the player can rename this NPC and pick a relationship from relationship_options.
# Use @elena in content blocks instead of hardcoding "Elena".
# Use @elena.rel for relationship references (e.g., "your @elena.rel").

[[npcs]]
id = "npc_elena"
name = "Elena"
customizable = true
relationship = "study partner"
relationship_options = ["study partner", "roommate", "childhood friend"]
description = "Graduate researcher with a knack for solving old puzzles."
portrait = "elena.jpg"
core_traits = { love = 20, trust = 10, expertise = 78 }
flag_keys = []

[[npcs]]
id = "npc_marcus"
name = "Marcus"
description = "Campus athlete; disciplined but surprisingly thoughtful."
core_traits = { discipline = 80, humor = 45 }
flag_keys = []

[[npcs]]
id = "npc_mara"
name = "Mara"
description = "Quick-witted barista who hears all the campus rumors."
core_traits = { wit = 68, hospitality = 75 }
flag_keys = []

# ═══════════════════════════════════════════════════════════════════════════════
#                              LOCATIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Top-level plaza (root hub)
[[locations]]
id = "loc_campus_plaza"
name = "Campus Plaza"
description = "The central square with a fountain and student booths."
is_container = false
entry_from = ""
navigation_order = ["loc_library_exterior", "loc_coffeehouse_exterior", "loc_sports_complex", "loc_dorm"]

# Library exterior entered from plaza
[[locations]]
id = "loc_library_exterior"
name = "University Library (Exterior)"
description = "Grand stone steps lead to heavy oak doors."
entry_from = "loc_campus_plaza"

# Coffeehouse container WITH default entry
[[locations]]
id = "loc_coffeehouse_exterior"
name = "The Perch (Exterior)"
description = "Warm glow, subdued chatter, and the scent of espresso."
is_container = true
entry_from = "loc_campus_plaza"
default_entry = "loc_coffeehouse_counter"

# Default entry inside coffeehouse
[[locations]]
id = "loc_coffeehouse_counter"
name = "The Perch — Counter"
description = "Mara greets students with a smile; chalkboard lists the daily roast."
parent = "loc_coffeehouse_exterior"
navigation_order = ["loc_coffeehouse_back_room"]

# Coffeehouse back room
[[locations]]
id = "loc_coffeehouse_back_room"
name = "The Perch — Back Room"
description = "A quiet nook with mismatched chairs and thumbed-through zines."
parent = "loc_coffeehouse_exterior"
entry_from = "loc_coffeehouse_counter"

# Sports complex container
[[locations]]
id = "loc_sports_complex"
name = "Sports Complex"
description = "Courts, fields, and a running track buzzing with energy."
is_container = true
entry_from = "loc_campus_plaza"
navigation_order = ["loc_track_field", "loc_gymnasium"]

[[locations]]
id = "loc_track_field"
name = "Track & Field"
description = "Runners keep pace; the track lanes gleam after a fresh rain."
parent = "loc_sports_complex"
entry_from = "loc_sports_complex"

[[locations]]
id = "loc_gymnasium"
name = "Gymnasium"
description = "Echoes of sneakers and squeak of basketball drills."
parent = "loc_sports_complex"
entry_from = "loc_sports_complex"

# Library interior container WITH default entry
[[locations]]
id = "loc_library_interior"
name = "University Library (Interior)"
description = "Quiet halls and stacks that smell of old paper."
is_container = true
entry_from = "loc_library_exterior"
default_entry = "loc_library_main_hall"

# Default entry inside library
[[locations]]
id = "loc_library_main_hall"
name = "Library — Main Hall"
description = "Information desk, catalog terminals, and a bulletin board."
parent = "loc_library_interior"
navigation_order = ["loc_reading_room", "loc_archives_door"]

[[locations]]
id = "loc_reading_room"
name = "Library — Reading Room"
description = "Lamplight pools across long wooden tables."
parent = "loc_library_interior"
entry_from = "loc_library_main_hall"

[[locations]]
id = "loc_archives_door"
name = "Library — Archives Door"
description = "Heavy door with a keycard reader; whispers of lost knowledge."
parent = "loc_library_interior"
entry_from = "loc_library_main_hall"
navigation_order = ["loc_sealed_archives"]

# Sealed archives container WITH default entry
[[locations]]
id = "loc_sealed_archives"
name = "Sealed Archives"
description = "Restricted stacks requiring authorization."
is_container = true
entry_from = "loc_archives_door"
default_entry = "loc_archives_lobby"

# Default entry inside sealed archives
[[locations]]
id = "loc_archives_lobby"
name = "Archives — Lobby"
description = "A security desk and a stern librarian watching closely."
parent = "loc_sealed_archives"
navigation_order = ["loc_archives_stacks"]

[[locations]]
id = "loc_archives_stacks"
name = "Archives — Stacks"
description = "Dim aisles, rare manuscripts, and fragile spines."
parent = "loc_sealed_archives"
entry_from = "loc_archives_lobby"

# Dorm room (for time-advancement canvas)
[[locations]]
id = "loc_dorm"
name = "Dorm Room"
description = "A small but comfortable room. Your own space on campus."
entry_from = "loc_campus_plaza"


# ═══════════════════════════════════════════════════════════════════════════════
#                    STARTING CANVAS (Pattern: No Trigger)
# ═══════════════════════════════════════════════════════════════════════════════
#
# The starting canvas has NO trigger section. It fires once at game start.
# Sets initial flags and introduces the premise.

[[canvases]]
id = "intro_canvas"
name = "Welcome to the Plaza"
description = "Opening scene at the town square."

# NOTE: No [canvases.trigger] — this is the starting canvas

[[canvases.nodes]]
id = "n1"
name = "A New Day"
blocks = [
  { type = "heading", content = "A new day begins" },
  { type = "paragraph", content = "You step into the plaza and feel the city wake around you. Students stream past with coffee cups and textbooks, their voices mingling with the fountain's splash." },
  { type = "paragraph", content = "The coffeehouse across the square glows warmly. The library looms to the left. Everything feels possible." }
]
exit_block = { type = "choices", choices = [
  { text = "Head to the coffeehouse", targetType = "location", locationId = "loc_coffeehouse_exterior", time_progression_minutes = 10, flagEffects = [{ targetType = "player", flag = "game_started" }, { targetType = "player", flag = "met_barista" }] },
  { text = "Explore the plaza first", targetType = "node", nodeId = "intro_canvas.n2", time_progression_minutes = 5 }
] }

[[canvases.nodes]]
id = "n2"
name = "Quiet Thoughts"
blocks = [
  { type = "paragraph", content = "You breathe in the morning air and consider your options. The plaza bulletin board catches your eye — job postings, study groups, campus events." },
  { type = "paragraph", content = "This is your fresh start. Time to make the most of it." }
]
exit_block = { type = "location", text = "Head out", config = { destinationType = "trigger", time_progression_minutes = 5, flagEffects = [{ targetType = "player", flag = "game_started" }] } }


# ═══════════════════════════════════════════════════════════════════════════════
#                    STORY EVENT: First Kiss (Pattern F)
# ═══════════════════════════════════════════════════════════════════════════════
#
# One-time event. is_repeatable = false, priority = 10.
# Requires love >= 25. Sets first_kiss_complete flag.
# Both branches set the same completion flag with different rewards.

[[canvases]]
id = "first_kiss_event"
name = "A Moment of Connection"
description = "A quiet moment in the back room becomes something more."

[canvases.trigger]
location = "loc_coffeehouse_back_room"
npc = "npc_elena"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "love", operator = "gte", value = 25 },
  { type = "flag", subject = "player", flag_key = "game_started", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "08:00"
end_time = "20:00"

[[canvases.nodes]]
id = "the_moment"
name = "The Moment"
blocks = [
  { type = "paragraph", content = "@elena looks up from her notes as you approach. There's something different in her eyes today." },
  { type = "dialog", content = "I've been thinking about you.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "She says it softly, almost surprised by her own words. The back room is empty. Just the two of you and the muffled sounds of the cafe." }
]
exit_block = { type = "choices", choices = [
  { text = "Kiss her gently", targetType = "node", nodeId = "first_kiss_event.gentle" },
  { text = "Pull her close", targetType = "node", nodeId = "first_kiss_event.passionate" }
] }

[[canvases.nodes]]
id = "gentle"
name = "Gentle"
blocks = [
  { type = "paragraph", content = "You lean in slowly, giving her time to pull away. She doesn't." },
  { type = "paragraph", content = "The kiss is soft, tentative, full of promise. When you part, she's smiling." },
  { type = "dialog", content = "We probably shouldn't have done that.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "But she doesn't move away." }
]
exit_block = { type = "location", text = "Say goodbye", config = { destinationType = "trigger", time_progression_minutes = 10, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 5 }, { targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 2 }], flagEffects = [{ targetType = "player", flag = "first_kiss_complete" }] } }

[[canvases.nodes]]
id = "passionate"
name = "Passionate"
blocks = [
  { type = "paragraph", content = "You don't think about it. You reach for her, and she meets you halfway." },
  { type = "paragraph", content = "The kiss is not gentle. It's urgent, surprising. Her hand finds your arm." },
  { type = "dialog", content = "Wow.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "She laughs, breathless. Everything feels different now." }
]
exit_block = { type = "location", text = "Walk away smiling", config = { destinationType = "trigger", time_progression_minutes = 10, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 7 }], flagEffects = [{ targetType = "player", flag = "first_kiss_complete" }] } }


# ═══════════════════════════════════════════════════════════════════════════════
#              GATE-SETTING EVENT: Late Study Session (Pattern G)
# ═══════════════════════════════════════════════════════════════════════════════
#
# One-time event that sets kiss_unlocked AND groping_unlocked gates.
# Uses days_since_flag for pacing — at least 2 days after first kiss.
# Requires love >= 40 and trust >= 15.

[[canvases]]
id = "late_study_event"
name = "Late Night in the Stacks"
description = "A late study session alone together opens new possibilities."

[canvases.trigger]
location = "loc_reading_room"
npc = "npc_elena"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "first_kiss_complete", operator = "gte", value = 2 },
  { type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "love", operator = "gte", value = 40 },
  { type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "trust", operator = "gte", value = 15 }
]
[[canvases.trigger.schedules]]
start_time = "18:00"
end_time = "22:00"

[[canvases.nodes]]
id = "alone"
name = "Alone Together"
blocks = [
  { type = "paragraph", content = "The reading room is nearly empty. Just you, @elena, and the lamplight. The library closes in an hour." },
  { type = "dialog", content = "Everyone else left already. It's just us.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "She closes her textbook. She's not looking at notes anymore. She's looking at you." },
  { type = "dialog", content = "I keep thinking about that day in the back room.", props = { speaker = "npc", npcId = "npc_elena" } }
]
exit_block = { type = "choices", choices = [
  { text = "Move closer", targetType = "node", nodeId = "late_study_event.closer" }
] }

[[canvases.nodes]]
id = "closer"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "You sit next to her. Close enough that your shoulders touch. She doesn't pull away." },
  { type = "paragraph", content = "Your hand finds hers on the desk. She turns to face you, and you kiss — longer this time, more sure." },
  { type = "dialog", content = "I don't want to go home yet.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "Neither do you. The library is quiet and warm, and something has shifted between you." }
]
# SETS TWO GATE FLAGS: kiss_unlocked enables kiss choices,
# groping_unlocked enables physical closeness choices
exit_block = { type = "location", text = "Walk her home", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 5 }, { targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 3 }], flagEffects = [{ targetType = "player", flag = "study_session_complete" }, { targetType = "player", flag = "kiss_unlocked" }, { targetType = "player", flag = "groping_unlocked" }] } }


# ═══════════════════════════════════════════════════════════════════════════════
#          ACTIVITY: Morning Coffee with Elena (Pattern A — Single Canvas)
# ═══════════════════════════════════════════════════════════════════════════════
#
# V2 PATTERN: ONE canvas with gated choices on the base node.
# Base node always shows. Choices progressively unlock with stats + flags.
# Each choice leads to an escalation node that exits back to the world.
#
# Choice progression:
#   "Just enjoy coffee"  — always available (no conditions) → trigger
#   "Flirt with her"     — love >= 30 (stat only) → warm node
#   "Tease her"          — love >= 50 + kiss_unlocked → tease node
#   "Get closer"         — love >= 70 + groping_unlocked → closer node

[[canvases]]
id = "activity_coffee_elena"
name = "Morning Coffee"
description = "Morning coffee with Elena — choices unlock with progression"

[canvases.trigger]
location = "loc_coffeehouse_counter"
npc = "npc_elena"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "08:00"
end_time = "12:00"

# BASE NODE — always shown when canvas fires
[[canvases.nodes]]
id = "morning"
name = "Morning Greeting"
blocks = [
  { type = "paragraph", content = "@elena is at the counter, her usual spot. She lights up when she sees you." },
  { type = "dialog", content = "I saved you a seat.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "She gestures to the stool beside her. Mara is already making your usual." }
]
exit_block = { type = "choices", choices = [
  # ALWAYS AVAILABLE — no conditions
  { text = "Just enjoy coffee", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 1 }, { targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 1 }] },
  # STAT-ONLY GATE — love >= 30
  { text = "Flirt with her", targetType = "node", nodeId = "activity_coffee_elena.warm", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "love", operator = "gte", value = 30 }] } },
  # STAT + FLAG GATE — love >= 50 AND kiss_unlocked
  { text = "Tease her", targetType = "node", nodeId = "activity_coffee_elena.tease", conditions = { version = "1.0", logic = "AND", items = [{ type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "love", operator = "gte", value = 50 }, { type = "flag", subject = "player", flag_key = "kiss_unlocked", operator = "is_true" }] } },
  # HIGHER STAT + FLAG GATE — love >= 70 AND groping_unlocked
  { text = "Get closer to her", targetType = "node", nodeId = "activity_coffee_elena.closer", conditions = { version = "1.0", logic = "AND", items = [{ type = "trait", subject = "npc", npc_id = "npc_elena", trait_key = "love", operator = "gte", value = 70 }, { type = "flag", subject = "player", flag_key = "groping_unlocked", operator = "is_true" }] } }
] }

# ESCALATION NODE — love >= 30
[[canvases.nodes]]
id = "warm"
name = "Warm Conversation"
blocks = [
  { type = "paragraph", content = "You lean in a little closer than usual. She notices, and a smile plays at the corner of her lips." },
  { type = "dialog", content = "You're in a good mood today.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "Your fingers brush as she passes you the sugar. Neither of you pulls away quickly." }
]
exit_block = { type = "location", text = "Finish coffee", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 2 }] } }

# ESCALATION NODE — love >= 50 + kiss_unlocked
[[canvases.nodes]]
id = "tease"
name = "Teasing"
blocks = [
  { type = "paragraph", content = "You lean in close, whispering something that makes her blush." },
  { type = "dialog", content = "You're terrible.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "She pushes your shoulder playfully, but she's laughing. Mara pretends not to notice from behind the counter." }
]
exit_block = { type = "location", text = "Finish coffee", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 3 }] } }

# ESCALATION NODE — love >= 70 + groping_unlocked
[[canvases.nodes]]
id = "closer"
name = "Getting Close"
blocks = [
  { type = "paragraph", content = "Under the counter, your hand finds her knee. She inhales sharply but doesn't move away." },
  { type = "dialog", content = "Not here.", props = { speaker = "npc", npcId = "npc_elena" } },
  { type = "paragraph", content = "But her hand covers yours. The coffee gets cold. Neither of you cares." }
]
exit_block = { type = "location", text = "Head out together", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 4 }] } }


# ═══════════════════════════════════════════════════════════════════════════════
#              UTILITY CANVAS: Shelve Books (Pattern C — Chore)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Simplest canvas. Single node, single exit. Builds trust indirectly.
# No NPC on trigger (solo activity).

[[canvases]]
id = "activity_shelve_books"
name = "Shelve Books"
description = "Help organize the library stacks — earns quiet appreciation"

[canvases.trigger]
location = "loc_library_main_hall"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "met_librarian", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "10:00"
end_time = "16:00"

[[canvases.nodes]]
id = "shelving"
name = "Shelving"
blocks = [
  { type = "paragraph", content = "The librarian nods approvingly as you start returning books to their proper shelves. It's quiet, methodical work." },
  { type = "paragraph", content = "@elena passes by on her way to the reading room. She notices you helping and smiles — a warm, genuine smile." }
]
exit_block = { type = "location", text = "Done", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 1 }] } }


# ═══════════════════════════════════════════════════════════════════════════════
#          TIME-ADVANCEMENT CANVAS: Dorm Room (Pattern E)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Always available. No conditions, no schedule, no NPC.
# Different choices advance time by different amounts.

[[canvases]]
id = "activity_dorm_room"
name = "Dorm Room"
description = "Your room — rest, study, or sleep"

[canvases.trigger]
location = "loc_dorm"
is_active = true
is_repeatable = true
priority = 1

[[canvases.nodes]]
id = "room"
name = "Your Room"
blocks = [
  { type = "paragraph", content = "Your dorm room. Textbooks on the desk, coffee rings on the nightstand. It's small, but it's yours." }
]
exit_block = { type = "choices", choices = [
  { text = "Study for a bit", targetType = "trigger", time_progression_minutes = 120, effects = [{ targetType = "player", trait = "intelligence", op = "add", value = 1 }] },
  { text = "Take a nap", targetType = "trigger", time_progression_minutes = 180 },
  { text = "Go to sleep", targetType = "trigger", time_progression_minutes = 540 }
] }


# ═══════════════════════════════════════════════════════════════════════════════
#                              STORY ARC
# ═══════════════════════════════════════════════════════════════════════════════
#
# Drives the Quest/Journal page. Links canvases to narrative progression.

[story_arc]
version = "1.0"

# ─── CHAPTERS ───

[[story_arc.chapters]]
id = "chapter_1"
name = "First Impressions"
mood = "hopeful"
description = "Getting to know the campus and its people"
order = 1

[[story_arc.chapters]]
id = "chapter_2"
name = "Growing Closer"
mood = "romantic"
description = "Connections deepen through shared experiences"
order = 2

# ─── NODES ───

# Starting milestone
[[story_arc.nodes]]
id = "first_meeting"
name = "Arrival on Campus"
chapter = "chapter_1"
journal_entry = "First day on campus. Everything feels new and possible."
linked_canvas = "intro_canvas"
linked_flag = "game_started"
is_milestone = true

# Activity-based bonding
[[story_arc.nodes]]
id = "morning_coffee_memory"
name = "Morning Coffee Together"
chapter = "chapter_1"
journal_entry = "Sharing morning coffee has become our ritual."
linked_canvas = "activity_coffee_elena"
npc = "npc_elena"
group = "early_bonding"

[[story_arc.nodes]]
id = "library_help"
name = "Helping at the Library"
chapter = "chapter_1"
journal_entry = "She noticed me shelving books. Small things seem to matter."
linked_canvas = "activity_shelve_books"
npc = "npc_elena"
group = "early_bonding"

# Story event: first kiss
[[story_arc.nodes]]
id = "first_kiss_moment"
name = "The First Kiss"
chapter = "chapter_2"
journal_entry = "We crossed a line today. Neither of us seemed to mind."
linked_canvas = "first_kiss_event"
linked_flag = "first_kiss_complete"
npc = "npc_elena"
requires_group = "early_bonding"
is_milestone = true

# Gate-setting event: late study
[[story_arc.nodes]]
id = "late_study_moment"
name = "Late Night in the Stacks"
chapter = "chapter_2"
journal_entry = "Something shifted between us in the library that night."
linked_canvas = "late_study_event"
linked_flag = "study_session_complete"
npc = "npc_elena"
requires_nodes = ["first_kiss_moment"]
is_milestone = true

# ─── BRANCHING EXAMPLE (optional — uncomment if game has path-variant arcs) ───
# The branch-point canvas "elena_crossroads" offers two choices:
# - "Support her" sets flag "chose_support" + "crossroads_complete"
# - "Ask her to stay" sets flag "chose_stay" + "crossroads_complete"
#
# # Shared milestone (both paths):
# [[story_arc.nodes]]
# id = "crossroads"
# name = "The Crossroads"
# chapter = "chapter_2"
# journal_entry = "She told me about the offer. I had to choose."
# linked_canvas = "elena_crossroads"
# linked_flag = "crossroads_complete"
# npc = "npc_elena"
# is_milestone = true
#
# # Support path only:
# [[story_arc.nodes]]
# id = "support_letters"
# name = "Letters from Afar"
# chapter = "chapter_2"
# journal_entry = "Her letters arrive on Tuesdays. Each one a small gift."
# linked_canvas = "support_letters_scene"
# linked_flag = "support_letters_complete"
# npc = "npc_elena"
# branch_condition = "chose_support"
# group = "path_resolution"
# requires_nodes = ["crossroads"]
#
# # Stay path only:
# [[story_arc.nodes]]
# id = "stay_tension"
# name = "The Unspoken"
# chapter = "chapter_2"
# journal_entry = "She stayed, but something between us shifted."
# linked_canvas = "stay_tension_scene"
# linked_flag = "stay_tension_complete"
# npc = "npc_elena"
# branch_condition = "chose_stay"
# group = "path_resolution"
# requires_nodes = ["crossroads"]
#
# # Reconvergence group:
# [[story_arc.groups]]
# id = "path_resolution"
# name = "Path Resolution"
# required_count = 1
#
# # Shared continuation (both paths):
# [[story_arc.nodes]]
# id = "reunion"
# name = "What We Built"
# chapter = "chapter_3"
# journal_entry = "Whatever road we took, it led here."
# linked_canvas = "reunion_scene"
# linked_flag = "reunion_complete"
# npc = "npc_elena"
# requires_group = "path_resolution"

# ─── GROUPS ───

[[story_arc.groups]]
id = "early_bonding"
name = "Getting to Know Her"
description = "Spend time together in daily activities"
required_count = 1

# ─── EMOTION MAPPINGS ───

[story_arc.emotion_mappings.love]
trait_owner = "npc"
default_npc = "npc_elena"
[[story_arc.emotion_mappings.love.ranges]]
min = 0
max = 25
label = "Acquaintance"
description = "@elena is polite but reserved around you"
[[story_arc.emotion_mappings.love.ranges]]
min = 26
max = 50
label = "Friend"
description = "@elena's eyes light up when she sees you"
[[story_arc.emotion_mappings.love.ranges]]
min = 51
max = 75
label = "Close"
description = "@elena finds reasons to be near you"
[[story_arc.emotion_mappings.love.ranges]]
min = 76
max = 100
label = "Devoted"
description = "@elena can't imagine her days without you"

[story_arc.emotion_mappings.trust]
trait_owner = "npc"
default_npc = "npc_elena"
[[story_arc.emotion_mappings.trust.ranges]]
min = 0
max = 20
label = "Guarded"
description = "@elena keeps her walls up around you"
[[story_arc.emotion_mappings.trust.ranges]]
min = 21
max = 50
label = "Open"
description = "@elena shares what's on her mind"
[[story_arc.emotion_mappings.trust.ranges]]
min = 51
max = 100
label = "Trusting"
description = "@elena confides in you without hesitation"

# ─── HINTS ───

[story_arc.hints]
stuck_threshold_minutes = 30
hint_style = "observation"

[[story_arc.hints.templates]]
text = "Maybe I should spend more time at the coffeehouse in the morning"
[story_arc.hints.templates.condition]
missing_trait = "love"
gap_gte = 5

[[story_arc.hints.templates]]
text = "Helping around the library might show her I care"
[story_arc.hints.templates.condition]
missing_trait = "trust"
gap_gte = 5


# ═══════════════════════════════════════════════════════════════════════════════
#                              NOTES
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   python manage.py package_from_toml --file apps/game_generation/game_example.toml --owner-id <UUID>
#
# V2 Pattern Summary:
# - Starting canvas: NO trigger section (fires once at game start)
# - Story events: is_repeatable = false, priority = 10, set gate flags
# - Activities: ONE canvas per activity, gated choices on base node
# - Utility canvases: single node, single exit (chores, study)
# - Time-advancement: always available, choices with different durations
# - Gate flags SET by story events only, CONSUMED by activity conditions
# - NPC schedules auto-detected from canvas triggers — do not define them
# - All location IDs use loc_ prefix, all NPC IDs use npc_ prefix
# - 4 gate flags: kiss_unlocked, groping_unlocked, oral_unlocked, sex_unlocked
#
# ═══════════════════════════════════════════════════════════════════════════════
```

--- END OF REFERENCE EXAMPLE TOML ---

---


## 10. Real Game: Two Weeks

Two Weeks is a complete, shipped game. It's a forbidden romance between step-siblings (player character Lily and NPC Ethan) with a 14-day countdown. It demonstrates single-NPC romance, countdown pressure mechanics, tiered activity escalation, group block variants, and multiple endings.

Below are ALL phase files that make up this game.

### 10.1 Phase 1: Metadata & Locations

```toml
# ═══════════════════════════════════════════════════════════════
# PHASE 1: METADATA, PLAYER, NPCS & LOCATIONS
# ═══════════════════════════════════════════════════════════════
# Source: Book Phases 1 (Foundation), 2 (Characters & Stats), 3 (World Design)
# Game: Two Weeks
# Architecture: Single-NPC Romance (Option A)
# Drivers: FORBIDDEN (primary) + LOVE (secondary)
# ═══════════════════════════════════════════════════════════════

schema_version = "0.2"
starting_canvas = "scene_arrival"

# ═══════════════════════════════════════════════════════════════
# PROJECT METADATA
# ═══════════════════════════════════════════════════════════════

[project]
id = "two_weeks"
title = "Two Weeks"
description = """
You return home after two years for your step-brother Ethan's wedding. \
The feelings you buried — the ones that made you leave in the first place — \
never went away. And neither did his. You have exactly 14 days before he \
says "I do" to someone else. Every moment is a choice between what's right \
and what you truly want. A single-NPC forbidden romance driven by a ticking \
clock, dual taboo (step-sibling + engaged), and the question: is love worth \
the cost of destroying everything else?
"""

# ═══════════════════════════════════════════════════════════════
# TIME SYSTEM
# ═══════════════════════════════════════════════════════════════
# Game starts Saturday afternoon (Day 1). Player arrives mid-afternoon.
# 14 days: Saturday (Week 1) through Friday (Week 3).
# 8 time periods per day: early_morning through night.

[time]
enabled = true
starting_hour = 14
starting_day = "Saturday"
starting_week = 1

# ═══════════════════════════════════════════════════════════════
# PLAYER
# ═══════════════════════════════════════════════════════════════
# Female, early 20s. Step-sister returning for the wedding.
# Player-owned stats: boldness (agency axis), energy.
# NPC stats (affection, guilt) go on the NPC, not here.

[player]
id = "player"
name = "Lily"
description = "A young woman in her early 20s, returning home after two years away. Slim build, expressive eyes. Old enough to know better, young enough to not care. She left to escape feelings she wasn't supposed to have. Now she's back for his wedding."
portrait = "player.jpg"
core_traits = { boldness = 0, energy = 100 }
flag_keys = [
  # --- Progression flags (set by story canvases, gate the next story canvas) ---
  "game_started",
  "arrival_complete",
  "welcome_dinner_complete",
  "old_photos_complete",
  "sleepless_night_complete",
  "madison_calls_complete",
  "rainy_day_complete",
  "the_couch_complete",
  "confession_complete",
  "almost_kiss_complete",
  "real_talk_complete",
  "first_kiss_done",
  "what_are_we_doing_done",
  "going_further_complete",
  "first_night_complete",
  "morning_after_complete",
  "cant_stay_away_complete",
  "madison_arrived",
  "stolen_moment_complete",
  "night_before_complete",
  "wedding_morning_done",
  # --- Ending flag (set by any ending, blocks all other endings) ---
  "ending_seen",
  # --- Gate flags (set by story canvases, gate activity tiers) ---
  "lingering_touch_unlock",
  "flirt_unlock",
  "kiss_unlock",
  "intimacy_unlock",
  # Granular intimacy unlocks (activities T6–T8)
  "manual_unlock",
  "oral_unlock",
  "sex_unlock",
  # --- NPC state flags (track Ethan's relationship state) ---
  "ethan_comfortable",
  "ethan_interested",
  "ethan_vulnerable",
  "ethan_intimate"
]

# ═══════════════════════════════════════════════════════════════
# NPC: ETHAN (Primary)
# ═══════════════════════════════════════════════════════════════
# Step-brother, late 20s, engaged to Madison.
# Protective older brother energy with suppressed desire.
# Warm, genuinely kind, conflict-avoidant.
# NPC-owned stats: love, trust, corruption.

[[npcs]]
id = "npc_ethan"
name = "Ethan"
description = "Your step-brother. Late 20s, tall, athletic build, warm brown eyes. Protective older brother energy with suppressed desire underneath. Engaged to Madison — wedding in 14 days. He remembers everything about you: your favorite meal, how you take your coffee, that summer you got too close. His loyalty is both his most attractive quality and the obstacle."
portrait = "ethan.jpg"
core_traits = { love = 0, trust = 0, corruption = 0 }
flag_keys = []
# NPC presence is derived from canvas triggers at runtime — no schedules needed.

# ═══════════════════════════════════════════════════════════════
# NPC: MADISON (Secondary — Days 13-14 only)
# ═══════════════════════════════════════════════════════════════
# Ethan's fiancée. Not a villain — she's genuinely nice.
# Appears Day 13 afternoon. No relationship stats (not interactive).
# Her function: make the player feel the weight of their choices.

[[npcs]]
id = "npc_madison"
name = "Madison"
description = "Ethan's fiancée. Late 20s, polished, put-together, warm. She greets you with genuine friendliness. She's not a caricature — she's a real person who doesn't deserve what's happening. Her presence transforms what you've done from abstract to devastatingly real."
portrait = "madison.jpg"
core_traits = {}
flag_keys = []
# NPC presence is derived from canvas triggers at runtime — no schedules needed.

# ═══════════════════════════════════════════════════════════════
# LOCATIONS
# ═══════════════════════════════════════════════════════════════
# 8 locations. Single-floor house + yard.
# Home = central hub. All rooms accessible directly.
# No containers needed — flat hierarchy with entry_from connections.
#
# Hierarchy:
#   loc_home (central hub)
#     ├── loc_player_room
#     ├── loc_ethan_room
#     ├── loc_bathroom
#     ├── loc_living
#     ├── loc_kitchen
#     ├── loc_backyard
#     └── loc_garage

# --- CENTRAL HUB ---
[[locations]]
id = "loc_home"
name = "Home"
description = "The central hallway of the house. Family photos line the walls — including several of you and Ethan as teenagers, standing too close at someone's birthday party. Doors branch off to every room. Shoes by the front door, keys on the hook, the smell of whatever Ethan last cooked still lingering."
image = "locations/hallway.jpg"
image_search_queries = ["house hallway family photos", "home entryway cozy"]
navigation_order = ["loc_player_room", "loc_ethan_room", "loc_bathroom", "loc_living", "loc_kitchen", "loc_backyard", "loc_garage"]

# --- ROOMS ---
[[locations]]
id = "loc_player_room"
name = "Your Old Room"
description = "The guest room that was once yours. Some of your old things are still here — posters you left behind, books on the shelf. The bed is smaller than you remembered. Window overlooks the backyard pool."
image = "locations/player_room.jpg"
image_search_queries = ["cozy guest bedroom small bed", "childhood bedroom grown up"]
entry_from = "loc_home"

[[locations]]
id = "loc_ethan_room"
name = "Ethan's Bedroom"
description = "Master bedroom with a king bed. Madison's presence is visible — her things on the dresser, their engagement photo on the nightstand. Entering feels like crossing a line."
image = "locations/ethan_room.jpg"
image_search_queries = ["master bedroom engagement photo nightstand", "couple bedroom forbidden"]
entry_from = "loc_home"

[[locations]]
id = "loc_bathroom"
name = "Bathroom"
description = "Shared bathroom with a large mirror, walk-in shower with glass door. Acoustics carry — you can hear when someone's in here. One bathroom for two people means timing matters."
image = "locations/bathroom.jpg"
image_search_queries = ["modern bathroom glass shower", "shared bathroom mirror"]
entry_from = "loc_home"

[[locations]]
id = "loc_living"
name = "Living Room"
description = "Comfortable space with a large sectional couch, flatscreen TV, and soft lighting. The couch is notably oversized — easy to end up sitting close. Wedding planning materials scattered on the coffee table."
image = "locations/living_room.jpg"
image_search_queries = ["living room couch TV cozy evening", "comfortable living room blanket"]
entry_from = "loc_home"

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
description = "Open-plan modern kitchen with a large island and breakfast bar. Morning light floods through windows. Coffee maker prominently featured. Connected to the living area through an open archway."
image = "locations/kitchen.jpg"
image_search_queries = ["modern kitchen island breakfast bar morning", "open kitchen bright"]
entry_from = "loc_home"

# --- OUTDOOR ---
[[locations]]
id = "loc_backyard"
name = "Backyard & Pool"
description = "Well-maintained backyard with an in-ground pool, lounge chairs, and a covered patio area. Privacy fence ensures neighbors can't see. The pool has underwater lights for night swimming."
image = "locations/backyard.jpg"
image_search_queries = ["backyard pool lounge chairs privacy fence", "pool night lights"]
entry_from = "loc_home"

[[locations]]
id = "loc_garage"
name = "Garage"
description = "Attached garage used partly for storage. Old boxes contain family memories — photo albums, childhood items, mementos from when you were growing up together. Dusty, dim, private."
image = "locations/garage.jpg"
image_search_queries = ["garage storage boxes memories", "dusty garage shelves storage"]
entry_from = "loc_home"

# ═══════════════════════════════════════════════════════════════
# SIDEBAR ITEMS
# ═══════════════════════════════════════════════════════════════
# Custom sidebar display elements. Rendered below the time widget.

[[sidebar_items]]
type = "countdown"
total_days = 14
label = "days until the wedding"

[[sidebar_items]]
type = "hint"
```

### 10.2 Phase 2: Story Canvases

```toml
# ═══════════════════════════════════════════════════════════════
# PHASE 2: STORY CANVASES
# ═══════════════════════════════════════════════════════════════
# Source: Book Phase 4 (Story Events)
# Game: Two Weeks
#
# Contents:
#   - 1 Starting canvas (scene_arrival — no trigger)
#   - 19 Story event canvases (is_repeatable = false, priority = 10)
#   - 1 Forced ending canvas (Day 14+ without story completion)
#   - 4 Ending canvases (priority-ordered: 10, 8, 6, 1)
#
# Flag Chain: Each canvas requires the previous canvas's completion flag.
# Gate Flags: Set by scene_old_photos (T2), scene_the_couch (T3),
#             scene_first_kiss (T4), scene_what_are_we_doing (T6),
#             scene_going_further (T7), scene_first_night (T5),
#             scene_morning_after (T8).
# Stats: affection/guilt on npc_ethan, boldness/energy on player.
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# EVENT #1: ARRIVAL (Starting Canvas — NO trigger section)
# ═══════════════════════════════════════════════════════════════
# Sets: game_started, arrival_complete
# Player Phase: DENIAL → first crack

[[canvases]]
id = "scene_arrival"
name = "Two Weeks"
description = "You return home after two years for your step-brother's wedding."

# NO [canvases.trigger] — this is the starting canvas (Rule 5)

# Node 1: Before You Begin (How to Play)
[[canvases.nodes]]
id = "before_you_begin"
name = "Before You Begin"
blocks = [
  { type = "heading", content = "Before You Begin" },
  { type = "paragraph", content = "Two Weeks is an interactive story about forbidden feelings, impossible choices, and a clock that won't stop ticking. You have fourteen days before Ethan's wedding. What happens in those days is up to you." },
  { type = "paragraph", content = "Explore the house, spend time with Ethan through daily activities, and make choices that shape your relationship. New story events unlock as your bond deepens. Check the Guide at the top of the screen anytime to see what's available." },
  { type = "paragraph", content = "Three stats shape your story:" },
  { type = "paragraph", content = "Affection — how close you and Ethan become. Built through activities and story choices. Guilt — the cost of crossing lines. Deeper intimacy carries weight. Boldness — your willingness to push boundaries and take risks." },
  { type = "paragraph", content = "This game has multiple endings. For Ethan to choose you over the wedding: Affection 95+, Boldness 70+, and Guilt under 50. High affection alone won't be enough — courage matters, and too much guilt has a cost." },
  { type = "paragraph", content = "The wedding is in fourteen days. Time advances with every action. If the clock runs out before you've seen the story through, the wedding happens without you getting a say." }
]
exit_block = { type = "choices", choices = [
  { text = "Begin", targetType = "node", nodeId = "scene_arrival.the_return" }
] }

# Node 2: The Return
[[canvases.nodes]]
id = "the_return"
name = "The Return"
blocks = [
  { type = "heading", content = "Two Weeks" },
  { type = "paragraph", content = "The taxi pulls away and you're standing on the sidewalk with your suitcase, staring at a house you haven't seen in two years. Same white shutters. Same oak tree in the front yard, taller now. Same crack in the second porch step that Dad always said he'd fix." },
  { type = "paragraph", content = "You left for college across the country. Told everyone it was for the program. Told yourself it was for the adventure. The truth was simpler and uglier: you couldn't keep living in a house with him and pretending you didn't feel what you felt." },
  { type = "paragraph", content = "Running was easier than staying and aching." },
  { type = "image", props = { file = "locations/home_exterior.jpg", description = "Suburban house exterior, warm afternoon light, suitcase on sidewalk", search_queries = ["family home exterior afternoon light", "suburban house returning home"] } },
  { type = "paragraph", content = "Two years of careful distance. Two years of short phone calls and shorter visits. And now you're back because your step-brother is getting married in fourteen days and you couldn't think of a good enough excuse not to come." },
  { type = "paragraph", content = "Your heart is pounding. You tell yourself it's just nerves." }
]
exit_block = { type = "choices", choices = [
  { text = "Walk to the door", targetType = "node", nodeId = "scene_arrival.ethan" }
] }

# Node 3: Ethan
[[canvases.nodes]]
id = "ethan"
name = "Ethan"
blocks = [
  { type = "paragraph", content = "The door opens before you reach it. And there he is." },
  { type = "paragraph", content = "Taller than you remembered. Or maybe you'd been trying to make him smaller in your memory. Warm brown eyes. That easy, lopsided smile that always made you feel like you were the only person in the room. He's broader now — athletic, filled out. Not the lanky stepbrother you left behind." },
  { type = "dialog", content = "Hey, stranger.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He pulls you into a hug. His arms tighten a moment too long. You breathe him in without meaning to — cedar and coffee and something that's just him. Two years of careful distance collapse in three seconds." },
  { type = "image", props = { file = "story/scene_arrival_ethan.jpg", description = "Warm reunion embrace at front door, afternoon light", search_queries = ["reunion hug front door emotional", "embrace coming home"] } },
  { type = "dialog", content = "God, it's good to see you. I wasn't sure you'd actually come.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Your heart is racing and you are actively trying to ignore the reason why." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "I missed you.", nodeId = "scene_arrival.the_situation", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }] }
] }

# Node 4: The Situation
[[canvases.nodes]]
id = "the_situation"
name = "The Situation"
blocks = [
  { type = "paragraph", content = "He carries your suitcase inside like it weighs nothing. The house smells like fresh coffee and something baking. He's been preparing." },
  { type = "dialog", content = "Madison's away finishing up some work stuff. Won't be here until right before the wedding. So it's just us for the next couple weeks.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Just us. The weight of those two words hangs in the air between you." },
  { type = "paragraph", content = "He shows you to your old room — the guest room that was once yours. Some of your old things are still here. Posters you left behind, books on the shelf. He didn't change it." },
  { type = "dialog", content = "I kept meaning to turn it into an office but... I don't know. Didn't feel right.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Fourteen days. Just the two of you. In the house where everything started." }
]
exit_block = { type = "location", text = "Settle in", config = { destinationType = "specific", locationId = "loc_home", time_progression_minutes = 60, flagEffects = [
  { targetType = "player", flag = "game_started" },
  { targetType = "player", flag = "arrival_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #2: WELCOME HOME DINNER [BRIDGE]
# ═══════════════════════════════════════════════════════════════
# Conditions: arrival_complete
# Sets: welcome_dinner_complete, ethan_comfortable
# Location: loc_kitchen, 17:00-19:00

[[canvases]]
id = "scene_welcome_dinner"
name = "Welcome Home Dinner"
description = "He cooked your favorite. He remembered."

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "arrival_complete", operator = "is_true" }
]
[[canvases.trigger.schedules]]
start_time = "17:00"
end_time = "19:00"

# Node 1: Dinner Together
[[canvases.nodes]]
id = "dinner"
name = "Dinner Together"
blocks = [
  { type = "paragraph", content = "The kitchen smells incredible. He's made your favorite — that pasta recipe your mom used to make before the divorce, the one you mentioned exactly once, years ago." },
  { type = "paragraph", content = "He remembered." },
  { type = "dialog", content = "Some things you don't forget.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He pours you a glass of wine and makes small talk about safe things — the neighborhood, his work, the wedding venue. But you catch him watching you when he thinks you're not looking. His eyes linger a beat too long." },
  { type = "image", props = { file = "story/scene_welcome_dinner_dinner.jpg", description = "Intimate dinner table for two, warm kitchen lighting, wine glasses", search_queries = ["intimate dinner table two people kitchen", "cozy dinner wine evening"] } }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Remember when we used to have dinner parties? Just us, pretending to be fancy?", nodeId = "scene_welcome_dinner.after_dinner", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }] }
] }

# Node 2: After Dinner
[[canvases.nodes]]
id = "after_dinner"
name = "After Dinner"
blocks = [
  { type = "paragraph", content = "He clears the dishes, waving off your offer to help. You watch him move through the kitchen — efficient, comfortable, at home. This is his life now. A life you're not part of." },
  { type = "dialog", content = "I'm glad you're here. Really.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The way he says it — you're not sure if he means here for the wedding, or here in this kitchen, or just... here." }
]
exit_block = { type = "location", text = "Head upstairs", config = { destinationType = "trigger", time_progression_minutes = 90, flagEffects = [
  { targetType = "player", flag = "welcome_dinner_complete" },
  { targetType = "player", flag = "ethan_comfortable" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #3: FINDING OLD PHOTOS → sets lingering_touch_unlock
# ═══════════════════════════════════════════════════════════════
# Conditions: welcome_dinner_complete, affection >= 15
# Sets: old_photos_complete, lingering_touch_unlock
# Location: loc_garage, 14:00-17:00

[[canvases]]
id = "scene_old_photos"
name = "Finding Old Photos"
description = "Photo albums in the garage. Heads bent close. Hands touching."

[canvases.trigger]
location = "loc_garage"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "welcome_dinner_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 15 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 8 }
]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

# Node 1: The Discovery
[[canvases.nodes]]
id = "discovery"
name = "The Discovery"
blocks = [
  { type = "paragraph", content = "You find the boxes while looking for something to do with yourself. Photo albums. High school. Prom. Beach trips. That summer you both try not to think about." },
  { type = "paragraph", content = "He appears in the garage doorway. Sees what you've found. Doesn't leave." },
  { type = "paragraph", content = "You look through them together. Heads bent close, shoulders pressed against each other. His finger traces a photo of you in that sundress from the Fourth of July." },
  { type = "dialog", content = "I remember that night.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His voice has dropped. Your eyes meet. Something unspoken passes between you — something that's been waiting two years to be acknowledged." },
  { type = "video", props = { file = "activities/garage_boxes_base.jpg", description = "Two people looking through old photos together, intimate proximity, heads close", search_queries = ["looking through photo album together close", "nostalgic photos intimate moment"] } }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Why did you keep these?", nodeId = "scene_old_photos.lingering", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Lingering
[[canvases.nodes]]
id = "lingering"
name = "Lingering"
blocks = [
  { type = "paragraph", content = "He doesn't answer right away. He looks at the photo, then at you. The silence stretches like taffy." },
  { type = "dialog", content = "We should probably put these away.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "But neither of you moves. His hand is still touching yours where it rests on the album page. Neither of you pulls away." }
]
exit_block = { type = "location", text = "Put the albums back", config = { destinationType = "trigger", time_progression_minutes = 45, flagEffects = [
  { targetType = "player", flag = "old_photos_complete" },
  { targetType = "player", flag = "lingering_touch_unlock" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #4: SLEEPLESS NIGHT
# ═══════════════════════════════════════════════════════════════
# Conditions: old_photos_complete, affection >= 25
# Sets: sleepless_night_complete
# Location: loc_kitchen, 22:00-01:00

[[canvases]]
id = "scene_sleepless_night"
name = "Sleepless Night"
description = "3 AM. Neither can sleep. The darkness makes it easier to say things."

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "old_photos_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 25 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 15 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

# Node 1: 3 AM
[[canvases.nodes]]
id = "three_am"
name = "3 AM"
blocks = [
  { type = "paragraph", content = "You can't sleep. The house is too quiet and your thoughts are too loud. You go downstairs for water and find him sitting at the kitchen island in the dark." },
  { type = "paragraph", content = "Both in sleep clothes. Both pretending this is normal. The moonlight through the window paints everything silver." },
  { type = "image", props = { file = "activities/cant_sleep.jpg", description = "Moonlit kitchen, two people in sleepwear, intimate late-night moment", search_queries = ["moonlit kitchen night intimate", "late night kitchen encounter"] } },
  { type = "paragraph", content = "He looks at you — your thin nightgown, bare shoulders — and doesn't look away. You feel his gaze like a physical thing." },
  { type = "dialog", content = "Couldn't sleep either?", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He reaches out and tucks a strand of hair behind your ear. His fingers brush your neck. He freezes." },
  { type = "dialog", content = "I should... I should go back to bed.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His hand trembles slightly. Neither of you moves." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Stay. Just for a bit.", nodeId = "scene_sleepless_night.parting", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 2: Parting
[[canvases.nodes]]
id = "parting"
name = "Parting"
blocks = [
  { type = "paragraph", content = "The moment stretches. Then breaks. You retreat to separate rooms, separate beds, separate lies about why your hearts are racing." },
  { type = "paragraph", content = "Sleep doesn't come any easier." }
]
exit_block = { type = "location", text = "Go back to bed", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 2, clamp = true }], flagEffects = [
  { targetType = "player", flag = "sleepless_night_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #5: MADISON CALLS [REGRESSION #1]
# ═══════════════════════════════════════════════════════════════
# Conditions: sleepless_night_complete, affection >= 30
# Sets: madison_calls_complete
# Location: loc_living, 12:00-17:00

[[canvases]]
id = "scene_madison_calls"
name = "Madison Calls"
description = "His phone rings. Madison. Reality intrudes."

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "sleepless_night_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 20 }
]
[[canvases.trigger.schedules]]
start_time = "12:00"
end_time = "17:00"

# Node 1: The Call
[[canvases.nodes]]
id = "the_call"
name = "The Call"
blocks = [
  { type = "paragraph", content = "His phone rings. The screen lights up: Madison." },
  { type = "paragraph", content = "He answers without looking at you. Loving words that sound rehearsed. 'Yes, everything's fine. She just got here. We're just catching up.'" },
  { type = "paragraph", content = "You watch him perform. The way his voice changes — lighter, easier, the voice of someone who hasn't been awake at 3 AM thinking about his step-sister." },
  { type = "video", props = { file = "story/scene_madison_calls_the_call.jpg", description = "Overhearing a phone call, conflicted looks exchanged between two people", search_queries = ["overhearing phone call jealousy", "watching someone on phone emotional"] } },
  { type = "paragraph", content = "He tells Madison he loves her. While looking directly at you. Something dark and wanting flickers across his face like a shadow." },
  { type = "paragraph", content = "When he hangs up, neither of you speaks. She isn't an abstract concept anymore. She's a real woman with a real voice who calls him 'babe' and talks about flower arrangements." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Say nothing. Just look at him.", nodeId = "scene_madison_calls.aftermath", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Aftermath
[[canvases.nodes]]
id = "aftermath"
name = "Aftermath"
blocks = [
  { type = "dialog", content = "She's... she's great. Really.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He sets his phone face-down on the coffee table. He doesn't sound convinced. Neither are you." }
]
exit_block = { type = "location", text = "Give him space", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }], flagEffects = [
  { targetType = "player", flag = "madison_calls_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #6: RAINY DAY [BRIDGE]
# ═══════════════════════════════════════════════════════════════
# Conditions: madison_calls_complete, days_since >= 1
# Sets: rainy_day_complete
# Location: loc_living, 19:00-22:00

[[canvases]]
id = "scene_rainy_day"
name = "Rainy Day"
description = "Thunderstorm. Power out. Candles and conversation."

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "madison_calls_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "madison_calls_complete", operator = "gte", value = 1 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 25 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 25 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

# Node 1: Power Out
[[canvases.nodes]]
id = "power_out"
name = "Power Out"
blocks = [
  { type = "paragraph", content = "Thunder cracks like a gunshot and the lights die. The house goes dark. No TV, no Wi-Fi, phones at single digits." },
  { type = "paragraph", content = "He digs candles out of the kitchen drawer. You open wine. The living room in candlelight feels like a different world — smaller, warmer, more honest." },
  { type = "image", props = { file = "story/scene_rainy_day_power_out.jpg", description = "Candlelit living room during thunderstorm, two people on couch, intimate atmosphere", search_queries = ["candlelit living room storm night", "cozy candlelight conversation couch"] } },
  { type = "paragraph", content = "You sit on the couch — the same couch that will matter later, but tonight it's innocent. Rain hammers the windows. And without screens to hide behind, you just... talk." }
]
exit_block = { type = "choices", choices = [
  { text = "Tell him the truth about why you left", targetType = "node", nodeId = "scene_rainy_day.truth" }
] }

# Node 2: The Truth About Leaving
[[canvases.nodes]]
id = "truth"
name = "The Truth About Leaving"
blocks = [
  { type = "paragraph", content = "The candlelight makes it easier to say the thing you've never said out loud." },
  { type = "dialog", content = "I didn't leave for the program, Ethan. I left because I couldn't keep living in a house with you and pretending I didn't feel what I felt. Running was easier than staying and aching.", props = { speaker = "player" } },
  { type = "paragraph", content = "He's quiet for a long time. The rain fills the silence." },
  { type = "dialog", content = "I knew. Part of me always knew. I just... I told myself you were just growing up. Leaving the nest. Normal stuff.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Neither topic is explicitly romantic. But both reveal vulnerability that daylight would never allow." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Do you wish I hadn't come back?", nodeId = "scene_rainy_day.his_answer", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 3: His Answer
[[canvases.nodes]]
id = "his_answer"
name = "His Answer"
blocks = [
  { type = "paragraph", content = "Whatever he says, it's more honest than anything either of you has managed in two years. The storm rages outside but inside the candlelight makes everything feel suspended — outside of time, outside of consequence." },
  { type = "dialog", content = "You were always... chaos. The best kind.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The candles burn low. Neither of you moves to replace them. In the growing dark, his hand finds yours. Just that. Just hands. It's enough." }
]
exit_block = { type = "location", text = "Let the night end", config = { destinationType = "trigger", time_progression_minutes = 90, flagEffects = [
  { targetType = "player", flag = "rainy_day_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #7: THE COUCH → sets flirt_unlock
# ═══════════════════════════════════════════════════════════════
# Conditions: rainy_day_complete, affection >= 40, days_since >= 1
# Sets: the_couch_complete, flirt_unlock, ethan_interested
# Location: loc_living, 19:00-22:00

[[canvases]]
id = "scene_the_couch"
name = "The Couch"
description = "Movie night. The couch is big but you've migrated to the middle."

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "rainy_day_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "rainy_day_complete", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 25 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 30 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 10 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

# Node 1: Movie Night
[[canvases.nodes]]
id = "movie_night"
name = "Movie Night"
blocks = [
  { type = "paragraph", content = "Movie night. The couch is big enough for three people but somehow you've both migrated to the middle. A blanket covers both of you." },
  { type = "paragraph", content = "On screen, a couple is doing what you're both pretending not to think about." },
  { type = "paragraph", content = "Under the blanket, bodies touching. His arm settles around your shoulders — starts casual, drifts to pulling you closer. His hand on your thigh. Starts innocent. Drifts higher. Neither of you acknowledges it." },
  { type = "video", props = { file = "story/scene_the_couch_movie_night.jpg", description = "Two people on couch under blanket, movie night, physical tension and proximity", search_queries = ["couple making out under blanket couch", "kissing on couch movie night blanket"] } },
  { type = "dialog", content = "This is nice. Just... this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His thumb traces small circles on your thigh through the blanket. Deliberate. Not accidental." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Move closer", nodeId = "scene_the_couch.breaking_apart", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Breaking Apart
[[canvases.nodes]]
id = "breaking_apart"
name = "Breaking Apart"
blocks = [
  { type = "paragraph", content = "Something shifts. Or almost shifts. The movie ends. Credits roll. Neither of you has any idea what happened in it." },
  { type = "dialog", content = "It's late. We should...", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He doesn't finish the sentence. You both know what's happening. You both know you're not going to stop it." }
]
exit_block = { type = "location", text = "Say goodnight", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }], flagEffects = [
  { targetType = "player", flag = "the_couch_complete" },
  { targetType = "player", flag = "flirt_unlock" },
  { targetType = "player", flag = "ethan_interested" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #8: THE CONFESSION
# ═══════════════════════════════════════════════════════════════
# Conditions: the_couch_complete, affection >= 50, boldness >= 35
# Sets: confession_complete
# Location: loc_backyard, 22:00-01:00

[[canvases]]
id = "scene_confession"
name = "The Confession"
description = "Under the stars, three glasses in, the unsayable thing gets said."

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "the_couch_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 35 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 20 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 35 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

# Node 1: Under the Stars
[[canvases.nodes]]
id = "under_the_stars"
name = "Under the Stars"
blocks = [
  { type = "paragraph", content = "Third glass of wine on the patio. Stars out. Pool lights shimmer turquoise across the water." },
  { type = "paragraph", content = "The alcohol makes the truth easier. Or maybe it's not the alcohol at all." },
  { type = "dialog", content = "I used to stay awake at night listening for your footsteps. Hoping you'd knock on my door. Terrified you would.", props = { speaker = "player" } },
  { type = "paragraph", content = "The silence that follows is the loudest thing you've ever heard." },
  { type = "dialog", content = "I thought I was the only one.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "You weren't.", props = { speaker = "player" } },
  { type = "paragraph", content = "Long pause. The pool filter hums. A lifetime passes." },
  { type = "dialog", content = "What do we do now?", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "video", props = { file = "story/scene_confession_under_the_stars.jpg", description = "Intense eye contact over wine on a patio at night, stars visible, emotional confession", search_queries = ["patio night wine confession emotional", "intense eye contact evening outdoor"] } }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "We still have time to figure that out.", nodeId = "scene_confession.after", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 8, clamp = true }] }
] }

# Node 2: After
[[canvases.nodes]]
id = "after"
name = "After"
blocks = [
  { type = "paragraph", content = "The night air feels different now. Charged. Whatever walls were left have started to crumble." },
  { type = "paragraph", content = "The stars don't care about your problems. The pool lights keep shimmering. The world keeps turning. But something between you has changed permanently." }
]
exit_block = { type = "location", text = "Go inside", config = { destinationType = "trigger", time_progression_minutes = 45, flagEffects = [
  { targetType = "player", flag = "confession_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #9: ALMOST KISS [BRIDGE]
# ═══════════════════════════════════════════════════════════════
# Conditions: confession_complete, affection >= 55
# Sets: almost_kiss_complete
# Location: loc_backyard, 19:00-22:00

[[canvases]]
id = "scene_almost_kiss"
name = "Almost Kiss"
description = "Faces inches apart. Then — interruption."

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "confession_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 55 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 30 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 30 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

# Node 1: The Moment
[[canvases.nodes]]
id = "the_moment"
name = "The Moment"
blocks = [
  { type = "paragraph", content = "Close. Too close. You can feel the heat radiating off his skin." },
  { type = "paragraph", content = "His hand comes up to your face. Thumb tracing your cheekbone. His breath mixing with yours. The tilt of heads beginning." },
  { type = "video", props = { file = "story/scene_almost_kiss_the_moment.jpg", description = "Faces inches apart, almost kissing, intense anticipation then interrupted", search_queries = ["almost kiss lips close anticipation", "couple about to kiss faces inches apart"] } },
  { type = "paragraph", content = "Then — his phone. Vibrating on the patio table. The spell shatters. You spring apart like guilty teenagers caught by the porch light." },
  { type = "dialog", content = "I should...", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "Yeah.", props = { speaker = "player" } },
  { type = "paragraph", content = "But you both know. There's no going back from what almost just happened." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Next time, lock the door.", nodeId = "scene_almost_kiss.parting", effects = [{ targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Parting
[[canvases.nodes]]
id = "parting"
name = "Parting"
blocks = [
  { type = "paragraph", content = "You go inside separately. Separate doors. Separate showers. The cold water doesn't help." }
]
exit_block = { type = "location", text = "Go inside", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }], flagEffects = [
  { targetType = "player", flag = "almost_kiss_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #10: THE REAL TALK [MAJOR CRISIS]
# ═══════════════════════════════════════════════════════════════
# Conditions: almost_kiss_complete, guilt >= 15
# Sets: real_talk_complete, ethan_vulnerable
# Location: loc_player_room, 22:00-01:00

[[canvases]]
id = "scene_real_talk"
name = "The Real Talk"
description = "He's sitting alone in the dark. The contradictions have peaked."

[canvases.trigger]
location = "loc_player_room"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "almost_kiss_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 45 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 40 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 25 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

# Node 1: In the Dark
[[canvases.nodes]]
id = "in_the_dark"
name = "In the Dark"
blocks = [
  { type = "paragraph", content = "You find him sitting on your bed in the dark. He's been waiting. Or maybe he's been trying to leave and couldn't." },
  { type = "dialog", content = "We need to talk about this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The wedding is in a week. Madison. The family. The impossibility of what he's feeling. Everything he's been pushing down comes flooding up at once." },
  { type = "dialog", content = "I'm supposed to be getting married.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "I know.", props = { speaker = "player" } },
  { type = "dialog", content = "I don't know if I can.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "I know.", props = { speaker = "player" } },
  { type = "paragraph", content = "His voice breaks." },
  { type = "dialog", content = "What do you want?", props = { speaker = "player" } },
  { type = "dialog", content = "I want you. I hate that I want you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "video", props = { file = "story/scene_real_talk_in_the_dark.jpg", description = "Emotional breakdown, holding someone who is crying, comfort not seduction", search_queries = ["emotional breakdown comfort holding", "vulnerability crying being held"] } },
  { type = "paragraph", content = "He's not performing anymore. The protective older brother, the dutiful fiance, the man who has it all together — all masks, and they've all fallen off at once." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "We'll figure it out. Together.", nodeId = "scene_real_talk.aftermath", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 2: Aftermath
[[canvases.nodes]]
id = "aftermath"
name = "Aftermath"
blocks = [
  { type = "paragraph", content = "Whatever was said, the air feels different. Raw. Like a wound that's been lanced — it hurts more now, but at least it's honest." },
  { type = "paragraph", content = "He doesn't stay. But when he leaves, he pauses at the door. His hand on the frame. He doesn't look back." },
  { type = "dialog", content = "I'm sorry. For all of this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The door clicks shut. You stare at the ceiling until dawn." }
]
exit_block = { type = "location", text = "Try to sleep", config = { destinationType = "trigger", time_progression_minutes = 60, flagEffects = [
  { targetType = "player", flag = "real_talk_complete" },
  { targetType = "player", flag = "ethan_vulnerable" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #11: FIRST KISS → sets kiss_unlock
# ═══════════════════════════════════════════════════════════════
# Conditions: real_talk_complete, affection >= 70, days_since >= 1
# Sets: first_kiss_done, kiss_unlock
# Location: loc_living, 19:00-22:00

[[canvases]]
id = "scene_first_kiss"
name = "First Kiss"
description = "No more interruptions. No more excuses. It happens like gravity."

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "real_talk_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "real_talk_complete", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 40 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 45 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 25 }
]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

# Node 1: Inevitable
[[canvases.nodes]]
id = "inevitable"
name = "Inevitable"
blocks = [
  { type = "paragraph", content = "No more interruptions. No more excuses. It happens like gravity." },
  { type = "paragraph", content = "One moment you're talking — something about nothing, filling silence with noise. The next, silence. His eyes on your mouth. Your breath catching." },
  { type = "paragraph", content = "Then his mouth is on yours." },
  { type = "paragraph", content = "The kiss starts tentative — a question. Then desperate. Years of suppression breaking like a dam. His hands in your hair, your back against the wall, pulling each other closer and closer and it's still not close enough." },
  { type = "video", props = { file = "activities/passionate_kiss.gif", description = "Passionate first kiss, tentative then desperate, years of longing released", search_queries = ["passionate first kiss against wall", "intense first kiss couple desperate"] } },
  { type = "paragraph", content = "Everything you've both been fighting falls away in an instant." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Don't stop.", nodeId = "scene_first_kiss.after_the_kiss", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 2: After the Kiss
[[canvases.nodes]]
id = "after_the_kiss"
name = "After the Kiss"
blocks = [
  { type = "paragraph", content = "When you finally break apart, the world has shifted on its axis. The room is the same. Everything else is different." },
  { type = "dialog", content = "I've wanted to do that for years.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His forehead rests against yours. His breath is ragged. Neither of you is pretending anymore." }
]
exit_block = { type = "location", text = "Say goodnight", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [
  { targetType = "player", flag = "first_kiss_done" },
  { targetType = "player", flag = "kiss_unlock" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #12: WHAT ARE WE DOING
# ═══════════════════════════════════════════════════════════════
# Conditions: first_kiss_done
# Sets: what_are_we_doing_done, manual_unlock
# Location: loc_kitchen, 07:00-09:00

[[canvases]]
id = "scene_what_are_we_doing"
name = "What Are We Doing"
description = "The morning after the first kiss. Coffee. Acknowledgement."

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 55 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 45 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 35 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 40 }
]
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "09:00"

# Node 1: Morning After the Kiss
[[canvases.nodes]]
id = "morning"
name = "Morning After the Kiss"
blocks = [
  { type = "paragraph", content = "Morning. Coffee. The weight of last night hanging in the air like smoke." },
  { type = "paragraph", content = "He's already there when you come down. Already poured your coffee. He knows how you take it — black, one sugar. Always has." },
  { type = "paragraph", content = "He crosses to you. Takes the coffee from your hands. Sets it on the counter." },
  { type = "paragraph", content = "And kisses you. Soft. Deliberate. Morning breath and all." },
  { type = "video", props = { file = "story/scene_what_are_we_doing_morning.jpg", description = "Morning kitchen kiss, tender and unhurried, coffee on counter", search_queries = ["couple kissing kitchen morning tender", "morning kiss coffee counter"] } },
  { type = "dialog", content = "I don't want to pretend that didn't happen.", props = { speaker = "npc", npcId = "npc_ethan" } }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Neither do I.", nodeId = "scene_what_are_we_doing.escalation", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Escalation
[[canvases.nodes]]
id = "escalation"
name = "More Than a Kiss"
blocks = [
  { type = "paragraph", content = "The kiss changes. Deeper. His hands slide from your face to your waist. Yours find the hem of his shirt." },
  { type = "paragraph", content = "He lifts you onto the counter — the same counter where he makes your coffee every morning. Your legs wrap around him. His mouth moves to your neck." },
  { type = "paragraph", content = "His hand slides under your shirt, tracing upward. Then downward. Past your waistband. Your breath catches." },
  { type = "video", props = { file = "story/scene_what_are_we_doing_escalation.jpg", description = "Intimate touching on kitchen counter, hands exploring, morning light", search_queries = ["couple intimate touching kitchen counter morning", "hands under clothes kitchen counter foreplay"] } },
  { type = "paragraph", content = "You reach for him. Find him hard through his shorts. His forehead drops to your shoulder as your hand wraps around him." },
  { type = "dialog", content = "God...", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "It's clumsy and perfect. Morning light through the kitchen window. Coffee going cold. His breath ragged against your neck as your hand moves. Years of wanting condensed into this — the first time you touch each other and mean it." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Don't stop looking at me.", nodeId = "scene_what_are_we_doing.new_normal", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 3: New Normal
[[canvases.nodes]]
id = "new_normal"
name = "New Normal"
blocks = [
  { type = "paragraph", content = "You lean against each other, breathing hard. The counter is cold under your thighs. His hand is still on your hip, thumb tracing circles." },
  { type = "dialog", content = "So that's what we're doing.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He says it with a half-laugh, half-wonder. Like he can't believe it's real. Neither can you." },
  { type = "paragraph", content = "The coffee is stone cold. He makes a fresh pot. You sit at the counter and watch him, and everything — every small domestic motion — is charged now. Electric. Inevitable." }
]
exit_block = { type = "location", text = "Start the day", config = { destinationType = "trigger", time_progression_minutes = 45, flagEffects = [
  { targetType = "player", flag = "what_are_we_doing_done" },
  { targetType = "player", flag = "manual_unlock" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #12b: GOING FURTHER
# ═══════════════════════════════════════════════════════════════
# Conditions: what_are_we_doing_done, affection >= 80, days_since >= 1
# Sets: going_further_complete, oral_unlock
# Location: loc_living, 21:00-01:00

[[canvases]]
id = "scene_going_further"
name = "Going Further"
description = "The couch where you held hands. Tonight you go further."

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "what_are_we_doing_done", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "what_are_we_doing_done", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 70 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 60 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 50 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 55 }
]
[[canvases.trigger.schedules]]
start_time = "21:00"
end_time = "01:00"

# Node 1: The Couch Again
[[canvases.nodes]]
id = "the_couch_again"
name = "The Couch Again"
blocks = [
  { type = "paragraph", content = "The same couch. The same blanket. But nothing is the same." },
  { type = "paragraph", content = "His hand finds yours under the blanket — the way it did weeks ago, when touching fingers felt revolutionary. Now his thumb traces your palm and you both know it isn't going to stop at hands." },
  { type = "paragraph", content = "The TV is on. Neither of you is watching." },
  { type = "dialog", content = "Come here.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "You swing your leg over his lap. Face to face. His hands on your hips. The blanket falls to the floor and neither of you reaches for it." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Let it happen. See where this goes.", nodeId = "scene_going_further.taste", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Taste
[[canvases.nodes]]
id = "taste"
name = "Taste"
blocks = [
  { type = "paragraph", content = "Mouths travel. Past collarbones. Past the edges of fabric. Shirts come off — not thrown, but peeled away, slowly, like unwrapping something precious." },
  { type = "paragraph", content = "He kisses down your stomach. Your fingers curl in his hair. The world shrinks to the couch, to his mouth, to the sound you make when he reaches his destination." },
  { type = "video", props = { file = "story/scene_going_further_taste.jpg", description = "Oral on the couch at night, intimate and tender, blanket on floor", search_queries = ["man going down on woman couch night intimate", "cunnilingus couch living room night tender"] } },
  { type = "paragraph", content = "When he comes back up, you push him onto his back. Fair is fair. His head falls back. His hand finds your hair. The couch creaks. You don't care." },
  { type = "video", props = { file = "story/scene_going_further_taste2.jpg", description = "Woman giving oral on couch at night, intimate", search_queries = ["blowjob on couch night intimate", "woman going down on man couch night"] } },
  { type = "paragraph", content = "Not sex. Not yet. But this — mouths and hands and the raw honesty of wanting someone without any barriers left — is its own kind of crossing." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "Stay here tonight. Just like this.", nodeId = "scene_going_further.after", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 3: After
[[canvases.nodes]]
id = "after"
name = "After"
blocks = [
  { type = "paragraph", content = "You lie on the couch tangled together, half-dressed, the TV casting blue light over bare skin. His fingers draw patterns on your shoulder." },
  { type = "dialog", content = "I don't think I can go back to just coffee and conversation.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "You can't either. And the wedding is getting closer." }
]
exit_block = { type = "location", text = "Eventually, separate rooms", config = { destinationType = "trigger", time_progression_minutes = 120, flagEffects = [
  { targetType = "player", flag = "going_further_complete" },
  { targetType = "player", flag = "oral_unlock" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #13: FIRST NIGHT TOGETHER [TURNING POINT] → sets intimacy_unlock
# ═══════════════════════════════════════════════════════════════
# Conditions: going_further_complete, affection >= 85, days_since >= 1
# Sets: first_night_complete, intimacy_unlock, ethan_intimate
# Location: loc_player_room, 22:00-01:00

[[canvases]]
id = "scene_first_night"
name = "First Night"
description = "No more pretending. The door clicks shut. Everything changes."

[canvases.trigger]
location = "loc_player_room"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "going_further_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "going_further_complete", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 85 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 75 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 60 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 70 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

# Node 1: Stay
[[canvases.nodes]]
id = "stay"
name = "Stay"
blocks = [
  { type = "paragraph", content = "The goodnight at the door doesn't end with goodnight." },
  { type = "dialog", content = "Stay.", props = { speaker = "player" } },
  { type = "paragraph", content = "One word. Everything changes. The door clicks shut." },
  { type = "paragraph", content = "His hands shake — not from nerves but from how long he's wanted this. You pull him closer. Years of suppression breaking." },
  { type = "paragraph", content = "Tender and desperate at once. His hands tracing paths he's memorized in his imagination. Your name on his lips like a prayer." },
  { type = "video", props = { file = "story/scene_first_night_stay.jpg", description = "First time having sex, emotional and passionate, eye contact throughout", search_queries = ["couple first time sex emotional passionate", "lovers first night together naked bed"] } },
  { type = "dialog", content = "God, you're beautiful.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "This isn't just physical. Eye contact throughout. His name on your lips. Emotional intimacy matching every physical moment." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "I've wanted this for so long.", nodeId = "scene_first_night.aftermath", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] }
] }

# Node 2: Aftermath
[[canvases.nodes]]
id = "aftermath"
name = "Aftermath"
blocks = [
  { type = "paragraph", content = "In the quiet after, everything feels different. Clearer. More complicated. You lie tangled together, his arm around you, his breath slowing against your neck." },
  { type = "dialog", content = "No regrets?", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "You answer with a kiss. He pulls you closer and you fall asleep like that — intertwined, sharing a pillow, sharing a secret that will reshape both your lives." }
]
exit_block = { type = "location", text = "Fall asleep together", config = { destinationType = "trigger", time_progression_minutes = 360, flagEffects = [
  { targetType = "player", flag = "first_night_complete" },
  { targetType = "player", flag = "intimacy_unlock" },
  { targetType = "player", flag = "ethan_intimate" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #14: MORNING AFTER [REGRESSION #2]
# ═══════════════════════════════════════════════════════════════
# Conditions: first_night_complete
# Sets: morning_after_complete
# Location: loc_player_room, 07:00-09:00

[[canvases]]
id = "scene_morning_after"
name = "Morning After"
description = "Dawn light. His arm around you. Then reality seeps back."

[canvases.trigger]
location = "loc_player_room"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 55 }
]
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "09:00"

# Node 1: Dawn
[[canvases.nodes]]
id = "dawn"
name = "Dawn"
blocks = [
  { type = "paragraph", content = "Dawn light through the curtains. His arm around you. For a moment — just this. Just warmth and skin and the slow rhythm of his breathing." },
  { type = "paragraph", content = "Morning intimacy — lazy, half-asleep, tender. A continuation of the night before. He's gentle, present, lost in you." },
  { type = "video", props = { file = "story/scene_morning_after_dawn.jpg", description = "Naked spooning morning after sex, gentle and tender, morning light", search_queries = ["couple naked spooning morning after sex", "lovers morning after bed sheets nude"] } },
  { type = "paragraph", content = "Then it's over and the weight lands. You can see it hit him — his eyes change, the softness replaced by something heavier. He's lying next to his step-sister, in the house where they grew up, four days before his wedding." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "I don't regret this. Do you?", nodeId = "scene_morning_after.lingering", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }] }
] }

# Node 2: Lingering
[[canvases.nodes]]
id = "lingering"
name = "Lingering"
blocks = [
  { type = "dialog", content = "We should talk. Later. About everything.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "But not now. Now he gets dressed without meeting your eyes. He flinches when his hand brushes yours. The weight of what they've done is a living thing between them." },
  { type = "paragraph", content = "At the door, he pauses. Doesn't turn around. Then he's gone, and you're alone with the impression of his body on the sheets." }
]
exit_block = { type = "location", text = "Get up", config = { destinationType = "trigger", time_progression_minutes = 60, flagEffects = [
  { targetType = "player", flag = "morning_after_complete" },
  { targetType = "player", flag = "sex_unlock" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #15: CAN'T STAY AWAY
# ═══════════════════════════════════════════════════════════════
# Conditions: morning_after_complete, affection >= 90
# Sets: cant_stay_away_complete
# Location: loc_home, 14:00-17:00

[[canvases]]
id = "scene_cant_stay_away"
name = "Can't Stay Away"
description = "He tried to keep his distance. He failed."

[canvases.trigger]
location = "loc_home"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "morning_after_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 90 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 60 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 85 }
]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

# Node 1: Hallway
[[canvases.nodes]]
id = "hallway"
name = "Hallway"
blocks = [
  { type = "paragraph", content = "You tried to be normal today. Failed. Every look is loaded. Every accidental touch sends electricity through both of you." },
  { type = "dialog", content = "I can't stop thinking about last night.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He initiates. That's the difference. He comes to you, not the other way around. His resistance broke on its own — desire stronger than duty." },
  { type = "paragraph", content = "He glances down the hall — empty — and then his mouth is on yours. You stumble backward. Your back hits the wall. Fast, desperate, addicted." },
  { type = "video", props = { file = "story/scene_cant_stay_away_hallway.jpg", description = "Sex against the hallway wall, desperate and urgent, passionate", search_queries = ["couple sex against wall hallway desperate", "passionate fuck against wall urgent"] } },
  { type = "dialog", content = "My room. Ten minutes. I'm not done with you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Every creaking board in this house is a risk. Every doorway a potential witness. The danger makes it more intense, not less." }
]
exit_block = { type = "location", text = "Follow him", config = { destinationType = "trigger", time_progression_minutes = 90, flagEffects = [
  { targetType = "player", flag = "cant_stay_away_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #16: MADISON ARRIVES [ACT 3 CRISIS]
# ═══════════════════════════════════════════════════════════════
# Conditions: cant_stay_away_complete, days_since >= 1
# Sets: madison_arrived
# Location: loc_home, 14:00-17:00

[[canvases]]
id = "scene_madison_arrives"
name = "Madison Arrives"
description = "A car in the driveway. She's real. She's here. She's nice."

[canvases.trigger]
location = "loc_home"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "cant_stay_away_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "cant_stay_away_complete", operator = "gte", value = 1 }
]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

# Node 1: Arrival
[[canvases.nodes]]
id = "arrival"
name = "Arrival"
blocks = [
  { type = "paragraph", content = "Sound of a car in the driveway. Your heart stops." },
  { type = "paragraph", content = "Madison." },
  { type = "paragraph", content = "She's polished, put-together, excited. She practically bounces through the door with a suitcase and a garment bag." },
  { type = "dialog", content = "Surprise! I finished early!", props = { speaker = "npc", npcId = "npc_madison" } },
  { type = "paragraph", content = "You watch Ethan perform. The hug. The smile. The 'I'm so glad you're here.' Over Madison's shoulder, his eyes find yours. Apology. Fear. Longing." },
  { type = "video", props = { file = "story/scene_madison_arrives_arrival.jpg", description = "Fiancee arriving home, couple embrace, third person watching with hidden emotion", search_queries = ["fiancee arriving home hug welcome", "watching couple embrace hidden emotion"] } },
  { type = "dialog", content = "You must be the step-sister! I've heard so much about you.", props = { speaker = "npc", npcId = "npc_madison" } },
  { type = "paragraph", content = "She's warm. Genuine. She hugs you like a friend. She smells like expensive perfume and a clear conscience." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "All good things, I hope.", nodeId = "scene_madison_arrives.new_reality" }
] }

# Node 2: New Reality
[[canvases.nodes]]
id = "new_reality"
name = "New Reality"
blocks = [
  { type = "paragraph", content = "Madison is nice. Genuinely, disarmingly nice. She asks about your life, your work, your flight. She makes you tea without being asked." },
  { type = "paragraph", content = "That makes it so much worse." },
  { type = "paragraph", content = "The abstract has become concrete. She's not a name on a phone screen anymore. She's a person. A person who doesn't deserve what you've done." }
]
exit_block = { type = "location", text = "Retreat to your room", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [
  { targetType = "player", flag = "madison_arrived" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #17: STOLEN MOMENT
# ═══════════════════════════════════════════════════════════════
# Conditions: madison_arrived, affection >= 85
# Sets: stolen_moment_complete
# Location: loc_garage, 14:00-17:00

[[canvases]]
id = "scene_stolen_moment"
name = "Stolen Moment"
description = "Madison is in the house. The garage is the only safe place."

[canvases.trigger]
location = "loc_garage"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 85 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 90 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 75 }
]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

# Node 1: Hidden
[[canvases.nodes]]
id = "hidden"
name = "Hidden"
blocks = [
  { type = "paragraph", content = "Madison is on the phone in the kitchen. Or maybe the shower. It doesn't matter where — just that she's not here." },
  { type = "paragraph", content = "He finds you in the garage. Grabs your hand. Pulls you behind the shelves." },
  { type = "dialog", content = "I need you. I can't — one more time before —", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He doesn't finish. He doesn't need to." },
  { type = "paragraph", content = "Desperate. Guilty. Unable to stop. His hand over your mouth because Madison is somewhere in the house." },
  { type = "video", props = { file = "story/scene_stolen_moment_hidden.jpg", description = "Quick desperate sex in garage, forbidden, hand covering her mouth", search_queries = ["secret sex garage urgent hand over mouth", "forbidden quickie hidden desperate"] } },
  { type = "paragraph", content = "Every sound from inside the house is a threat. The thrill of almost getting caught. The terrifying freedom of not caring." }
]
exit_block = { type = "choices", choices = [
  { targetType = "node", text = "We're insane. (But don't stop)", nodeId = "scene_stolen_moment.after", effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] }
] }

# Node 2: After
[[canvases.nodes]]
id = "after"
name = "After"
blocks = [
  { type = "paragraph", content = "Madison's voice calling his name from inside. The spell shatters." },
  { type = "dialog", content = "Coming!", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He looks at you one last time before going inside. That look says everything words can't: I'm sorry. I love you. I don't know how to fix this." }
]
exit_block = { type = "location", text = "Wait. Then go inside separately.", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [
  { targetType = "player", flag = "stolen_moment_complete" }
] } }


# ═══════════════════════════════════════════════════════════════
# EVENT #18: NIGHT BEFORE WEDDING
# ═══════════════════════════════════════════════════════════════
# Conditions: stolen_moment_complete
# Sets: night_before_complete
# Location: loc_player_room, 22:00-01:00
# Extended scene — 7 nodes, linear chain

[[canvases]]
id = "scene_night_before_wedding"
name = "Night Before Wedding"
description = "Tomorrow he marries Madison. Tonight the door opens in darkness."

[canvases.trigger]
location = "loc_player_room"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "stolen_moment_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 80 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 70 }
]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

# Node 1: The Door Opens
[[canvases.nodes]]
id = "n1_door"
name = "The Door Opens"
blocks = [
  { type = "paragraph", content = "Tomorrow he marries Madison." },
  { type = "paragraph", content = "Tonight the door opens in darkness. You know it's him before he speaks. You've been waiting. You've been hoping. You've been dreading." },
  { type = "dialog", content = "I had to see you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His kiss tastes like tears." },
  { type = "video", props = { file = "story/scene_night_before_wedding_n1_door.jpg", description = "Desperate embrace in doorway at night, emotional intensity, tears", search_queries = ["desperate kissing doorway night tears emotional", "couple embracing crying doorway"] } }
]
exit_block = { type = "choices", choices = [
  { text = "Pull him inside", targetType = "node", nodeId = "scene_night_before_wedding.n2_undressing" }
] }

# Node 2: Undressing
[[canvases.nodes]]
id = "n2_undressing"
name = "Undressing"
blocks = [
  { type = "paragraph", content = "Slowly. Memorizing. Every button, every inch of skin. Like he's trying to commit you to permanent memory." },
  { type = "dialog", content = "I want to remember everything.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "video", props = { file = "story/scene_night_before_wedding_n2_undressing.jpg", description = "Slowly undressing each other, savoring every moment, tender and deliberate", search_queries = ["slowly undressing lover savoring body", "couple undressing each other tender bedroom"] } }
]
exit_block = { type = "choices", choices = [
  { text = "Let him lay you down", targetType = "node", nodeId = "scene_night_before_wedding.n3_worship" }
] }

# Node 3: Worship
[[canvases.nodes]]
id = "n3_worship"
name = "Worship"
blocks = [
  { type = "paragraph", content = "He kisses his way down your body. No rush tonight. Slow, devoted, like a prayer." },
  { type = "dialog", content = "I want to remember every part of you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "video", props = { file = "story/scene_night_before_wedding_n3_worship.jpg", description = "Man kissing down her body, eating her out, devoted and emotional", search_queries = ["man going down on woman cunnilingus devoted", "eating pussy emotional intimate worship"] } }
]
exit_block = { type = "choices", choices = [
  { text = "Pull him up to you", targetType = "node", nodeId = "scene_night_before_wedding.n4_together" }
] }

# Node 4: Together
[[canvases.nodes]]
id = "n4_together"
name = "Together"
blocks = [
  { type = "paragraph", content = "When he enters you, you're both crying. The weight of everything you can't have. But right now, in this moment, he's yours." },
  { type = "dialog", content = "I love you. I've always loved you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Not in the heat of passion — in the weight of loss. He says it like a fact. Like gravity. Like something that was always true and will always be true regardless of what tomorrow brings." },
  { type = "video", props = { file = "story/scene_night_before_wedding_n4_together.jpg", description = "Missionary sex, foreheads touching, tears, emotional lovemaking", search_queries = ["missionary sex emotional eye contact tears", "couple making love missionary foreheads touching"] } }
]
exit_block = { type = "choices", choices = [
  { text = "Hold him closer", targetType = "node", nodeId = "scene_night_before_wedding.n5_deeper" }
] }

# Node 5: Deeper
[[canvases.nodes]]
id = "n5_deeper"
name = "Deeper"
blocks = [
  { type = "paragraph", content = "The pace builds. Gentle becomes urgent. Tenderness gives way to need." },
  { type = "dialog", content = "Don't hold back. Not tonight.", props = { speaker = "player" } },
  { type = "paragraph", content = "You pull him deeper. Nails down his back. He gasps your name." },
  { type = "video", props = { file = "story/scene_night_before_wedding_n5_deeper.jpg", description = "Intense deep sex, nails scratching his back, building urgency", search_queries = ["intense sex nails scratching back passionate", "rough passionate sex urgent deep"] } }
]
exit_block = { type = "choices", choices = [
  { text = "Take control", targetType = "node", nodeId = "scene_night_before_wedding.n6_control" }
] }

# Node 6: Taking Control
[[canvases.nodes]]
id = "n6_control"
name = "Taking Control"
blocks = [
  { type = "paragraph", content = "You push him onto his back. You need to feel him, control this, make it yours. His hands grip your hips. His eyes never leave yours." },
  { type = "video", props = { file = "story/scene_night_before_wedding_n6_control.jpg", description = "Woman on top riding him, intense eye contact, gripping her hips", search_queries = ["woman riding cowgirl sex eye contact", "girl on top riding hips gripped passionate"] } },
  { type = "paragraph", content = "Everything narrows to this — two bodies, one heartbeat, a love that will outlast whatever happens tomorrow." }
]
exit_block = { type = "choices", choices = [
  { text = "Feel it building", targetType = "node", nodeId = "scene_night_before_wedding.n7_finish" }
] }

# Node 7: The Finish — final choices determine ending path
[[canvases.nodes]]
id = "n7_finish"
name = "The Finish"
blocks = [
  { type = "dialog", content = "I'm yours. Whatever happens tomorrow, I'm yours tonight.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Climax. The world whites out. When it returns, you're tangled together, breathing hard, holding on." },
  { type = "paragraph", content = "He cleans you gently, tenderly. Then you lie together in the dark." },
  { type = "video", props = { file = "story/scene_night_before_wedding_n7_finish.jpg", description = "Post-sex afterglow, naked and tangled together in bed, holding each other", search_queries = ["couple naked afterglow bed tangled together", "post sex cuddling tender bed sheets"] } },
  { type = "dialog", content = "Don't marry her.", props = { speaker = "player" } },
  { type = "dialog", content = "Don't ask me that.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "But he's here, isn't he?" },
  { type = "paragraph", content = "You stay together until the sky lightens. No more words. Just holding on to what little time you have." }
]
exit_block = { type = "choices", choices = [
  { targetType = "trigger", text = "I'll always love you. Whatever you decide.", time_progression_minutes = 300, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 5, clamp = true }], flagEffects = [{ targetType = "player", flag = "night_before_complete" }] }
] }


# ═══════════════════════════════════════════════════════════════
# EVENT #19: WEDDING MORNING
# ═══════════════════════════════════════════════════════════════
# Conditions: night_before_complete
# Sets: wedding_morning_done
# Location: loc_kitchen, 07:00-09:00

[[canvases]]
id = "scene_wedding_morning"
name = "Wedding Morning"
description = "The day has arrived. Chaos. One stolen moment."

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "days_since_flag", subject = "player", flag_key = "game_started", operator = "gte", value = 13 }
]
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "09:00"

# Node 1: The Day
[[canvases.nodes]]
id = "the_day"
name = "The Day"
blocks = [
  { type = "paragraph", content = "The house is chaos. Florists. A caterer. Madison's mother on the phone. Someone asking about centerpieces." },
  { type = "paragraph", content = "He finds you in the kitchen during a brief gap. Everyone else is upstairs. His hand finds yours under the counter." },
  { type = "dialog", content = "Whatever happens today... I need you to know... Thank you. For everything.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "video", props = { file = "story/scene_wedding_morning_the_day.jpg", description = "Stolen hand-holding amid wedding chaos, intense brief moment", search_queries = ["stolen moment wedding morning hands touching", "secret touch during wedding preparations"] } },
  { type = "paragraph", content = "You don't know what that means yet. His eyes are red. He didn't sleep either." },
  { type = "paragraph", content = "Someone calls his name from upstairs. He squeezes your hand once, hard, then lets go." }
]
exit_block = { type = "location", text = "Let him go", config = { destinationType = "trigger", time_progression_minutes = 60, flagEffects = [
  { targetType = "player", flag = "wedding_morning_done" }
] } }


# ═══════════════════════════════════════════════════════════════
# ENDING CANVASES
# ═══════════════════════════════════════════════════════════════
# All trigger from loc_living, 09:00-12:00, after wedding_morning_done.
# All share name "The Wedding Day" so engine groups them as one activity.
# Priority ordering: best ending = LOWEST priority (engine picks lowest valid unvisited).
# ending_seen flag prevents multiple endings from showing after one is clicked.


# ───────────────────────────────────────────────────────────────
# ENDING A: HE CHOOSES YOU (Priority 1 — best ending, lowest priority = selected first)
# ───────────────────────────────────────────────────────────────
# Conditions: affection >= 95, boldness >= 70, guilt < 50

[[canvases]]
id = "ending_he_chooses_you"
name = "The Wedding Day"
description = "The ceremony begins. 'I can't do this.'"

[canvases.trigger]
location = "loc_living"
is_active = true
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "wedding_morning_done", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "ending_seen", operator = "is_false" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 95 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 80 },
  { type = "trait", subject = "player", trait_key = "boldness", operator = "gte", value = 85 }
]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[[canvases.nodes]]
id = "ending"
name = "He Chooses You"
blocks = [
  { type = "heading", content = "He Chooses You" },
  { type = "paragraph", content = "The ceremony begins. Flowers. Music. Madison walks down the aisle in white. Everyone watches. Everyone smiles." },
  { type = "paragraph", content = "He stands at the altar. The officiant speaks. 'Do you take this woman...'" },
  { type = "paragraph", content = "And he looks at you. Sitting in the third row. Hands in your lap. Heart in your throat." },
  { type = "dialog", content = "I can't do this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "Chaos. Madison's tears. Her mother's scream. His father's face. Whispers turning to shouts. The destruction of a life carefully built." },
  { type = "video", props = { file = "story/ending_he_chooses_you.jpg", description = "Wedding interrupted, man walking away from altar, aftermath chaos", search_queries = ["wedding interrupted walking away altar", "called off wedding emotional"] } },
  { type = "paragraph", content = "When the dust settles — hours, days, a lifetime later — he's beside you. Bags packed. Nowhere to go. Scandal at his back and an uncertain future ahead." },
  { type = "dialog", content = "I choose you. I choose us.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "It won't be easy. His family may never forgive him. Madison certainly won't. The whispers will follow you both for years." },
  { type = "paragraph", content = "But his hand is in yours. And for the first time in your life, you're not running." },
  { type = "paragraph", content = "You did it. You were brave enough to let it happen — bold enough to stand in the fire and not look away. He saw that in you. He chose that." },
  { type = "paragraph", content = "It took everything: the late nights, the stolen moments, the courage to push past every safe boundary. Love ran deep between you, trust anchored what you built, and neither of you flinched when it mattered most." },
  { type = "paragraph", content = "Not every love story ends like this. Yours did." }
]
exit_block = { type = "game_end", text = "The End", config = { flagEffects = [{ targetType = "player", flag = "ending_seen" }] } }


# ───────────────────────────────────────────────────────────────
# ENDING B: THE ARRANGEMENT (Priority 2)
# ───────────────────────────────────────────────────────────────
# Conditions: affection >= 85, guilt >= 70, boldness >= 60

[[canvases]]
id = "ending_the_arrangement"
name = "The Wedding Day"
description = "He marries Madison. But the story doesn't end."
start_node = "the_ceremony"

[canvases.trigger]
location = "loc_living"
is_active = true
is_repeatable = false
priority = 8
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "wedding_morning_done", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "ending_seen", operator = "is_false" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 85 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "lt", value = 40 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "gte", value = 80 }
]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[[canvases.nodes]]
id = "the_ceremony"
name = "The Ceremony"
blocks = [
  { type = "heading", content = "The Wedding" },
  { type = "paragraph", content = "The ceremony is perfect. Of course it is. Madison walks the aisle in white, radiant, every inch the bride. The flowers, the music, the soft gasps from the crowd — all of it choreographed, all of it beautiful." },
  { type = "paragraph", content = "He stands at the altar. Composed. Steady. The vows come — 'to have and to hold, in sickness and in health' — and his voice doesn't break." },
  { type = "paragraph", content = "But you see it. The way his jaw tightens. The way his eyes sweep the crowd once — just once — and find you before snapping back to Madison. The way his hands shake when he slides on the ring." },
  { type = "paragraph", content = "He says 'I do.' Madison says 'I do.' Everyone cheers. You clap with the rest of them, your smile a perfect mask." },
  { type = "paragraph", content = "You know something they don't. And that knowledge sits in your chest like a stone." }
]
exit_block = { type = "location", text = "Watch the reception begin", config = { destinationType = "node", destinationId = "ending_the_arrangement.ending" } }

[[canvases.nodes]]
id = "ending"
name = "The Arrangement"
blocks = [
  { type = "heading", content = "The Arrangement" },
  { type = "paragraph", content = "He marries Madison. Of course he does. The desire was there but something was missing — the trust to believe you could be more than a secret. You watch from the crowd with a smile that could cut glass." },
  { type = "paragraph", content = "The reception is beautiful. The speeches are warm. Madison glows. He plays the part perfectly." },
  { type = "paragraph", content = "Three weeks later, your phone buzzes. Unknown number." },
  { type = "dialog", content = "I can't leave her. But I can't leave you either.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "It's wrong. You both know it's wrong. You've always known." },
  { type = "video", props = { file = "story/ending_the_arrangement.jpg", description = "Secret message on phone, hidden relationship continuing, bittersweet", search_queries = ["secret text message affair continuing", "hidden relationship phone message"] } },
  { type = "paragraph", content = "But when has that ever stopped you?" },
  { type = "paragraph", content = "The arrangement begins. Stolen weekends. Burner phones. A love that lives in the shadows because neither of you is strong enough to let it die — or brave enough to bring it into the light." },
  { type = "paragraph", content = "The love was real. The connection was deep. But without enough trust to believe in a future together, duty held him in place. You pushed him far — but not quite far enough to pull him free before the ring went on." },
  { type = "paragraph", content = "Next time: balance everything. Build love through emotional choices, earn trust through bonding, and don't shy away from physical escalation. The best ending needs love, trust, and corruption all running high." }
]
exit_block = { type = "game_end", text = "The End", config = { flagEffects = [{ targetType = "player", flag = "ending_seen" }] } }


# ───────────────────────────────────────────────────────────────
# ENDING C: ONE LAST NIGHT (Priority 3)
# ───────────────────────────────────────────────────────────────
# Conditions: affection >= 80, guilt >= 60

[[canvases]]
id = "ending_one_last_night"
name = "The Wedding Day"
description = "He goes through with it. They never crossed enough lines."
start_node = "the_ceremony"

[canvases.trigger]
location = "loc_living"
is_active = true
is_repeatable = false
priority = 6
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "wedding_morning_done", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "ending_seen", operator = "is_false" },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 80 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "trust", operator = "gte", value = 60 },
  { type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "corruption", operator = "lt", value = 40 }
]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[[canvases.nodes]]
id = "the_ceremony"
name = "The Ceremony"
blocks = [
  { type = "heading", content = "The Wedding" },
  { type = "paragraph", content = "You take your seat. Third row, aisle side. Your hands won't stop shaking so you sit on them like a child." },
  { type = "paragraph", content = "The music starts. Madison walks the aisle in white. She's radiant. She deserves this — all of it. The thought makes your throat close." },
  { type = "paragraph", content = "He's at the altar. The officiant speaks. And then — just for a second — his eyes find yours." },
  { type = "paragraph", content = "Everything you built over fourteen days is in that look. Every late-night conversation. Every accidental touch that wasn't accidental. Every time one of you almost said the thing that would have changed everything." },
  { type = "paragraph", content = "Almost. The cruelest word in any language." },
  { type = "dialog", content = "I do.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He doesn't look at you again. Not during the kiss. Not during the applause. Not when they walk back up the aisle together, married, finished." }
]
exit_block = { type = "location", text = "Stay for the reception", config = { destinationType = "node", destinationId = "ending_one_last_night.ending" } }

[[canvases.nodes]]
id = "ending"
name = "One Last Night"
blocks = [
  { type = "heading", content = "One Last Night" },
  { type = "paragraph", content = "He goes through with it. You never pushed far enough — kept things emotional, kept things safe. But the night before, he came to you one last time." },
  { type = "dialog", content = "I love you. I'll always love you. But I can't destroy everything.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "You watch from the crowd. Their vows. The ring. The kiss. His eyes find yours once — just once — across the room. A lifetime in a glance." },
  { type = "video", props = { file = "story/ending_one_last_night.jpg", description = "Watching wedding from crowd with hidden tears, eye contact across room", search_queries = ["watching wedding from crowd tears", "eye contact across room wedding"] } },
  { type = "paragraph", content = "You leave before the reception. You don't say goodbye. The taxi comes and you get in and you don't look back because if you look back you will break apart." },
  { type = "paragraph", content = "At the airport, your phone buzzes. One message from him: 'I'm sorry. For all of it. Except the parts with you.'" },
  { type = "paragraph", content = "You board the plane. You fly away. You don't come back." },
  { type = "paragraph", content = "Some love stories end with sacrifice." },
  { type = "paragraph", content = "He loved you. That was never the question. But love wasn't enough — not without crossing enough lines together, not without the physical truth of what you were to each other making denial impossible." },
  { type = "paragraph", content = "Next time: don't hold back physically. Build corruption through daring choices and the journal. The best ending needs love, trust, and corruption all running high — emotional depth alone won't free him." }
]
exit_block = { type = "game_end", text = "The End", config = { flagEffects = [{ targetType = "player", flag = "ending_seen" }] } }


# ───────────────────────────────────────────────────────────────
# ENDING D: WHAT COULD HAVE BEEN (Priority 4 — fallback, highest = selected last)
# ───────────────────────────────────────────────────────────────
# Conditions: wedding_morning_done only (fallback if no other ending matches)

[[canvases]]
id = "ending_what_could_have_been"
name = "The Wedding Day"
description = "They came close. Neither was brave enough."
start_node = "the_ceremony"

[canvases.trigger]
location = "loc_living"
is_active = true
is_repeatable = false
priority = 1
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "wedding_morning_done", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "ending_seen", operator = "is_false" }
]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[[canvases.nodes]]
id = "the_ceremony"
name = "The Ceremony"
blocks = [
  { type = "heading", content = "The Wedding" },
  { type = "paragraph", content = "The wedding is beautiful. Everyone says so. The flowers, the venue, the weather — all of it perfect." },
  { type = "paragraph", content = "You sit in the crowd and watch it happen. Madison walks the aisle. He waits at the altar. The officiant speaks. The vows are said." },
  { type = "paragraph", content = "He doesn't look at you. Not once. Not during the vows. Not during the ring. Not during the kiss." },
  { type = "paragraph", content = "You're not sure if that makes it easier or harder." },
  { type = "paragraph", content = "When did it happen — or rather, when didn't it? Two weeks in the same house. Every almost. Every not-quite. The distance never closed and now it never will." },
  { type = "paragraph", content = "The ceremony ends. Everyone applauds. You clap too, because what else is there to do?" }
]
exit_block = { type = "location", text = "Go to the reception", config = { destinationType = "node", destinationId = "ending_what_could_have_been.ending" } }

[[canvases.nodes]]
id = "ending"
name = "What Could Have Been"
blocks = [
  { type = "heading", content = "What Could Have Been" },
  { type = "paragraph", content = "They came close. So close. But neither was brave enough to cross the final line." },
  { type = "paragraph", content = "The wedding happens. It's beautiful. He's distant but committed. She's present but already leaving." },
  { type = "paragraph", content = "At the reception, you find a quiet corner. He finds you there." },
  { type = "dialog", content = "Maybe in another life.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "Maybe.", props = { speaker = "player" } },
  { type = "video", props = { file = "story/ending_what_could_have_been.jpg", description = "Airport departure, looking back once, melancholy and regret", search_queries = ["airport departure looking back regret", "leaving looking back once melancholy"] } },
  { type = "paragraph", content = "You leave the next morning. Early flight. No fanfare. He drives you to the airport. Neither of you speaks." },
  { type = "paragraph", content = "At the gate, you almost say it. Almost. The words are right there." },
  { type = "paragraph", content = "But you board the plane. And the words stay unspoken. And the story ends the way most love stories end — not with a bang, but with a what-if that echoes forever." },
  { type = "paragraph", content = "The distance won. Two weeks in the same house, and neither of you found the courage to close the gap. The moments were there — but you let them pass." },
  { type = "paragraph", content = "Next time: don't hold back. Spend more time with Ethan — every meal, every evening, every quiet moment. Balance emotional and physical choices. Build trust through bonding activities. The best ending needs deep love, real trust, and enough corruption that going back to normal is impossible." }
]
exit_block = { type = "game_end", text = "The End", config = { flagEffects = [{ targetType = "player", flag = "ending_seen" }] } }
```

### 10.3 Phase 3: Activities

```toml
# ═══════════════════════════════════════════════════════════════
# PHASE 3: ACTIVITIES (synced from 6_final_game.toml)
# ═══════════════════════════════════════════════════════════════
# Game: Two Weeks
#
# Format: Base node (group variants) → 3 choices (Emotional/Physical/Neutral)
#   → Emotional sub-node (group variants) → exit
#   → Physical sub-node → unlockable tier choices → tier nodes
#   → Neutral → direct exit
#
# Relationship phases for group variants:
#   Phase 5: madison_arrived (fiancée in the house)
#   Phase 4: first_night_complete (fully intimate)
#   Phase 3: first_kiss_done (physical line crossed)
#   Default: Phase 1-2 (reconnecting)
# ═══════════════════════════════════════════════════════════════

[[canvases]]
id = "activity_breakfast_ethan"
name = "Morning with Ethan"
description = "Morning light, coffee, and the easy rhythm of routine."

# === BASE NODE (group variants by relationship phase) ===
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  # Phase 5: Madison arrived
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's on the phone when you walk in. Hangs up fast. 'That was Madison.' One mug on the counter. Yours isn't made." },
    { type = "image", props = { file = "activities/breakfast_ethan_base.jpg", description = "Morning kitchen, tense atmosphere", search_queries = ["morning kitchen coffee tense", "awkward morning kitchen"] } },
    { type = "dialog", content = "She's asking about the seating chart.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "You make your own coffee. The silence has a different weight now." }
  ] },
  # Phase 4: Post-first night (intimate baseline)
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He made your favorite. Doesn't say why. Your mug is exactly right — he's memorized it. Sits closer than he used to." },
    { type = "image", props = { file = "activities/breakfast_ethan_base.jpg", description = "Morning kitchen, warm intimate domestic scene", search_queries = ["morning kitchen coffee two mugs domestic", "cozy breakfast kitchen morning light"] } },
    { type = "dialog", content = "Couldn't sleep after you left.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "His knee finds yours under the counter. Neither of you pretends it's an accident anymore." }
  ] },
  # Phase 3: Post-first kiss
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's already looking when you walk in. Looks away too fast. Your mug is ready — made exactly how you like it." },
    { type = "image", props = { file = "activities/breakfast_ethan_base.jpg", description = "Morning kitchen, coffee for two, warm domestic scene", search_queries = ["morning kitchen coffee two mugs domestic", "cozy breakfast kitchen morning light"] } },
    { type = "dialog", content = "Hey.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Just 'hey.' But the way he says it — like the word is carrying everything he can't say out loud." }
  ] },
  # Default: Phase 1-2 (reconnecting / pre-physical)
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light through the kitchen window. He's at the counter, coffee already made. Two mugs. He remembered how you take yours." },
    { type = "image", props = { file = "activities/breakfast_ethan_base.jpg", description = "Morning kitchen, coffee for two, warm domestic scene", search_queries = ["morning kitchen coffee two mugs domestic", "cozy breakfast kitchen morning light"] } },
    { type = "dialog", content = "Morning. Sleep okay?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Cereal, toast, the easy rhythm of two people who know each other's habits." }
  ] }
]
exit_block = { type = "choices", choices = [
  # EMOTIONAL — always available
  { text = "Talk with him over coffee", targetType = "node", nodeId = "activity_breakfast_ethan.emotional" },
  # PHYSICAL — only after first physical unlock
  { text = "Get closer", targetType = "node", nodeId = "activity_breakfast_ethan.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  # NEUTRAL — always available
  { text = "Just eat. Easy silence.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

    { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true },

  ] }
] }

# === EMOTIONAL SUB-NODE (group variants by phase) ===
[[canvases.nodes]]
id = "emotional"
name = "Morning Conversation"
blocks = [
  # Phase 5: Madison arrived
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You stir your coffee longer than necessary. The question sits between you like a third person at the table." },
    { type = "dialog", content = "How's the planning going?", props = { speaker = "player" } },
    { type = "dialog", content = "Fine. It's fine.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "'Fine' is doing a lot of heavy lifting in that sentence. You don't push. The silence says what neither of you will." }
  ] },
  # Phase 4: Post-first night
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The coffee gets cold while you talk. Really talk. About what this is, what it means, whether either of you can stop." },
    { type = "dialog", content = "I keep thinking about what happens when you leave.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "You don't have an answer. Neither does he. But the honesty feels like its own kind of intimacy." }
  ] },
  # Phase 3: Post-first kiss
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You talk around it for ten minutes before he sets down his mug." },
    { type = "dialog", content = "Are we going to pretend last night didn't happen?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "Do you want to pretend?", props = { speaker = "player" } },
    { type = "paragraph", content = "He looks at you. Really looks." },
    { type = "dialog", content = "No.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "The word is quiet but it fills the kitchen." }
  ] },
  # Default: Phase 1-2
  { type = "group", blocks = [
    { type = "paragraph", content = "Easy conversation about nothing important. Old memories, shared jokes, the kind of talk that flows between people with history." },
    { type = "dialog", content = "Remember when Mom burned the turkey that one Thanksgiving?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "You laugh. He laughs. For a moment it's just two people who grew up together, catching up. Almost simple." }
  ] }
]
exit_block = { type = "location", text = "Finish your coffee", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [
  { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true },

  { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true },

  { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true },

] } }

# === PHYSICAL SUB-NODE (unlockable intensity choices) ===
[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "The coffee can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Sit closer than necessary. Let your knee touch his.", targetType = "node", nodeId = "activity_breakfast_ethan.t2" },
  { text = "\"You always look good in the morning.\" Hold eye contact.", targetType = "node", nodeId = "activity_breakfast_ethan.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Come up behind him. Arms around his waist. Kiss his neck.", targetType = "node", nodeId = "activity_breakfast_ethan.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "His hand under the table. The cereal can wait.", targetType = "node", nodeId = "activity_breakfast_ethan.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Kneel on cool tile. Morning takes a turn.", targetType = "node", nodeId = "activity_breakfast_ethan.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Counter. Now.", targetType = "node", nodeId = "activity_breakfast_ethan.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } }
] }

# === TIER NODES (existing content preserved) ===
[[canvases.nodes]]
id = "t2"
name = "Closer Than Necessary"
blocks = [
  { type = "paragraph", content = "Your knees touch under the breakfast bar. Neither moves away. His hand finds yours reaching for the jam. Fingers brush. Linger." },
  { type = "video", props = { file = "activities/breakfast_ethan_t2.jpg", description = "Accidental hand touch over breakfast, fingers lingering", search_queries = ["hand touch over breakfast intimate", "fingers brushing lingering domestic"] } },
  { type = "paragraph", content = "He's not sorry. Neither are you." }
]
exit_block = { type = "location", text = "Finish breakfast", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }


[[canvases.nodes]]
id = "t3"
name = "Morning Compliment"
blocks = [
  { type = "paragraph", content = "You catch him watching you stretch. He quickly looks away, ears red. You take your time reaching for things on high shelves. The kitchen feels very small." },
  { type = "video", props = { file = "activities/breakfast_ethan_flirt.jpg", description = "Standing too close in kitchen, reaching past her", search_queries = ["standing too close kitchen tension sexual", "man behind woman kitchen reaching close bodies"] } },
  { type = "dialog", content = "Need help with that?", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He's already behind you." }
]
exit_block = { type = "location", text = "Finish breakfast", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Kitchen Embrace"
blocks = [
  { type = "paragraph", content = "You wrap your arms around him from behind at the counter. He leans back. Turns around. His hands on your waist. Kisses that taste like coffee." },
  { type = "video", props = { file = "activities/breakfast_ethan_t4.jpg", description = "Kitchen embrace, kissing, morning light", search_queries = ["couple kissing passionately kitchen morning", "making out kitchen counter embrace"] } },
  { type = "dialog", content = "We should eat.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "Later.", props = { speaker = "player" } }
]
exit_block = { type = "location", text = "Continue your morning", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Morning Hand"
blocks = [
  { type = "paragraph", content = "Milk sweats on the carton while his hand makes you forget it exists. The kitchen feels indecent in the morning light — in a way you love." },
  { type = "video", props = { file = "activities/breakfast_ethan_t6.jpg", description = "Morning manual stimulation at counter, playful and quiet", search_queries = ["morning kitchen hand under shirt counter", "manual stimulation kitchen morning light"] } }
]
exit_block = { type = "location", text = "Toast pops eventually", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Kneel"
blocks = [
  { type = "paragraph", content = "You sink to your knees on cool tile. He tastes like coffee and him. His fingers curl in your hair as he tries to stay quiet and fails a little." },
  { type = "video", props = { file = "activities/breakfast_ethan_t7.jpg", description = "Morning oral in kitchen, discreet, coffee nearby", search_queries = ["blowjob kitchen morning coffee", "kneeling oral morning kitchen"] } }
]
exit_block = { type = "location", text = "Wipe your mouth, grin", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Counter Rush"
blocks = [
  { type = "paragraph", content = "He lifts you onto the counter again, this time with no hesitation. You meet him eagerly, the kitchen your accomplice." },
  { type = "video", props = { file = "activities/breakfast_ethan_t8.jpg", description = "Sex on kitchen counter, morning urgency", search_queries = ["sex on kitchen counter morning", "urgent sex counter kitchen daylight"] } },
  { type = "paragraph", content = "The toast is charcoal by the time you're done. He makes a new batch, grinning." }
]
exit_block = { type = "location", text = "Make new toast", loop_terminal = true, config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "07:00"
end_time = "09:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "activity_helping_chores"
name = "Helping with Chores"
description = "Laundry, dishes, domestic teamwork. Easy conversation."

# === BASE NODE (group variants by relationship phase) ===
[[canvases.nodes]]
id = "base"
name = "Chores Together"
blocks = [
  # Phase 5: Madison arrived
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison's dry cleaning hangs on the door handle. You fold it without being asked. He watches you fold his fiancée's clothes and something in his face breaks a little." },
    { type = "image", props = { file = "activities/helping_chores_base.jpg", description = "Domestic chores, tense atmosphere", search_queries = ["couple doing chores together domestic", "folding laundry living room together"] } },
    { type = "dialog", content = "You don't have to do that.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "But you do it anyway. Because what else can you do." }
  ] },
  # Phase 4: Post-first night
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You're folding his shirts. He comes up behind you and wraps his arms around your waist." },
    { type = "dialog", content = "You don't have to do this.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "I want to.", props = { speaker = "player" } },
    { type = "paragraph", content = "Neither of you means the laundry." },
    { type = "image", props = { file = "activities/helping_chores_base.jpg", description = "Domestic chores together, intimate", search_queries = ["couple doing chores together domestic", "folding laundry living room together"] } },
    { type = "paragraph", content = "The house smells like detergent and him. Domestic in a way that aches." }
  ] },
  # Phase 3: Post-first kiss
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Laundry, dishes, the domestic dance. His hand brushes yours at the sink more than necessary. The house feels smaller since last night." },
    { type = "image", props = { file = "activities/helping_chores_base.jpg", description = "Domestic chores together, warm tension", search_queries = ["couple doing chores together domestic", "folding laundry living room together"] } },
    { type = "dialog", content = "Thanks for helping.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "His eyes say more than thanks. Your hips bump at the sink. Neither apologizes." }
  ] },
  # Default: Phase 1-2
  { type = "group", blocks = [
    { type = "paragraph", content = "Laundry, dishes, general tidying. Domestic teamwork. You're helping because you're a guest who doesn't want to be useless. He appreciates it." },
    { type = "image", props = { file = "activities/helping_chores_base.jpg", description = "Domestic chores together, folding laundry, living room", search_queries = ["couple doing chores together domestic", "folding laundry living room together"] } },
    { type = "paragraph", content = "Easy conversation about old times while folding towels. He washes, you dry. Your hips bump at the sink." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Talk while you work", targetType = "node", nodeId = "activity_helping_chores.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_helping_chores.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Fold laundry, easy conversation.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

# === EMOTIONAL SUB-NODE ===
[[canvases.nodes]]
id = "emotional"
name = "Domestic Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She left her wedding shoes by the door. You almost tripped on them this morning." },
    { type = "dialog", content = "I saw.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He doesn't apologize for them being there. He doesn't move them. The shoes sit between you like everything else unsaid." }
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Folding towels side by side. The routine feels dangerously domestic. Like this could be your life." },
    { type = "dialog", content = "What would mornings look like if things were different?", props = { speaker = "player" } },
    { type = "paragraph", content = "He stops folding. Stares at the towel in his hands like it holds the answer. It doesn't. But the question hangs in the warm air between you." }
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You sort laundry in comfortable silence. His shirt is warm from the dryer." },
    { type = "dialog", content = "It's nice having help.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "It's nice being here.", props = { speaker = "player" } },
    { type = "paragraph", content = "Both of you meaning more than the words carry." }
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Easy banter while you work. He tells you about the neighbor's cat that keeps getting into the yard. You tell him about your apartment's terrible plumbing." },
    { type = "dialog", content = "Sounds like you need a handyman.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "The offer hangs in the air, half-joke, half-something else." }
  ] }
]
exit_block = { type = "location", text = "Back to folding", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [
  { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true },

  { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true },

] } }

# === PHYSICAL SUB-NODE ===
[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "The chores can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Hold his shirt to your face. Breathe in.", targetType = "node", nodeId = "activity_helping_chores.t2" },
  { text = "Flick him with the dish towel. Let him chase you.", targetType = "node", nodeId = "activity_helping_chores.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Stay at the sink. Let him come up behind you.", targetType = "node", nodeId = "activity_helping_chores.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Pull him to the couch. Hide under the laundry.", targetType = "node", nodeId = "activity_helping_chores.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Kneel on the rug. Kiss lower.", targetType = "node", nodeId = "activity_helping_chores.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Push him into the cushions.", targetType = "node", nodeId = "activity_helping_chores.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } }
] }

# === TIER NODES ===
[[canvases.nodes]]
id = "t2"
name = "His Shirt"
blocks = [
  { type = "paragraph", content = "You hold one of his shirts — press it to your nose." },
    { type = "dialog", content = "Still use the same detergent.", props = { speaker = "player" } },
    { type = "paragraph", content = "He watches you inhale. Doesn't say anything. Doesn't need to." },
  { type = "video", props = { file = "activities/helping_chores_t2.jpg", description = "Smelling his shirt, intimate domestic moment", search_queries = ["smelling his shirt intimate domestic", "laundry intimate moment"] } }
]
exit_block = { type = "location", text = "Keep folding", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }


[[canvases.nodes]]
id = "t3"
name = "Towel Fight"
blocks = [
  { type = "paragraph", content = "Dish towel flick fight. He chases you around the island. You squeal. He catches you from behind. Both breathing hard. His arms around you. Neither moves." },
  { type = "video", props = { file = "activities/helping_chores_t3.jpg", description = "Playful chasing, catching from behind, laughing", search_queries = ["playful chasing catching from behind hug", "man catches woman from behind playful domestic"] } },
  { type = "paragraph", content = "Then you squirm free, laughing." },
    { type = "dialog", content = "You cheat.", props = { speaker = "player" } }
]
exit_block = { type = "location", text = "Back to chores", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "At the Sink"
blocks = [
  { type = "paragraph", content = "You're at the sink. He comes up behind you, reaching for the faucet. Doesn't step back. His breath on your neck. Hands sliding from the faucet to your waist." },
  { type = "video", props = { file = "activities/helping_chores_t4.jpg", description = "Behind her at the sink, kissing her neck, intimate", search_queries = ["kissing her neck from behind at sink", "man kissing woman neck kitchen embrace behind"] } },
  { type = "dialog", content = "You missed a spot.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His lips find your shoulder. The dishes can wait." }
]
exit_block = { type = "location", text = "Finish the dishes", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Under the Pile"
blocks = [
  { type = "paragraph", content = "You tug him to the couch, a shirt draped over your lap like camouflage. His hand disappears under the fabric and you forget what chore you were doing." },
  { type = "video", props = { file = "activities/helping_chores_t6.jpg", description = "Manual play on couch under laundry pile", search_queries = ["hand under clothes couch laundry", "manual stimulation on couch hidden by laundry"] } }
]
exit_block = { type = "location", text = "Half-folded, fully distracted", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Lower"
blocks = [
  { type = "paragraph", content = "You kneel on the rug and kiss lower until talking stops. The TV hums to itself, ignored." },
  { type = "video", props = { file = "activities/helping_chores_t7.jpg", description = "Oral on living room rug, quiet afternoon", search_queries = ["blowjob living room rug afternoon", "oral on couch area carpet"] } }
]
exit_block = { type = "location", text = "Stand, breathless", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Couch Rush"
blocks = [
  { type = "paragraph", content = "He pushes you back into the cushions and the world narrows to you and him. The laundry can absolutely wait." },
  { type = "video", props = { file = "activities/helping_chores_t8.jpg", description = "Sex on couch in living room, impromptu", search_queries = ["sex on couch living room impromptu", "quick sex couch domestic"] } }
]
exit_block = { type = "location", text = "Fold later", loop_terminal = true, config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 25 }]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "activity_lunch_together"
name = "Lunch Together"
description = "Making sandwiches, catching up. Easy midday routine."

[[canvases.nodes]]
id = "base"
name = "Lunch"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He made lunch for three. Madison's plate is at the far end. You sit where you always sit — next to him." },
    { type = "image", props = { file = "activities/lunch_together_base.jpg", description = "Lunch with three plates", search_queries = ["couple lunch kitchen midday", "making lunch together kitchen"] } },
    { type = "dialog", content = "She likes your grilled cheese recipe.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "You smile. The cheese tastes like chalk in your mouth." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Lunch for two without being asked. This is routine now. His knee against yours is deliberate." },
    { type = "image", props = { file = "activities/lunch_together_base.jpg", description = "Lunch together intimate", search_queries = ["couple lunch kitchen midday", "making lunch together kitchen"] } },
    { type = "dialog", content = "Same as yesterday?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He means the sandwich. He also means everything else." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Grilled cheese, extra sharp. He remembered. His eyes linger on your mouth when you take the first bite." },
    { type = "image", props = { file = "activities/lunch_together_base.jpg", description = "Lunch together warm tension", search_queries = ["couple lunch kitchen midday", "making lunch together kitchen"] } },
    { type = "paragraph", content = "The kitchen feels different now. Every shared meal is a small confession." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Making sandwiches together. He remembers your favorite — grilled cheese, extra sharp cheddar." },
    { type = "image", props = { file = "activities/lunch_together_base.jpg", description = "Making lunch together, midday light", search_queries = ["couple lunch kitchen midday", "making lunch together kitchen"] } },
    { type = "paragraph", content = "Their knees touch under the breakfast bar. Neither moves away." },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_lunch_together.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_lunch_together.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Casual lunch.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

    { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison texts him during lunch. He puts the phone face-down." },
    { type = "dialog", content = "It's nothing.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Everything is nothing now. You eat in silence." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You talk about small things. Every mundane word carries the weight of what you can't say in daylight." },
    { type = "dialog", content = "This is nice. Just... this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He asks how you're sleeping. You both know the answer." },
    { type = "dialog", content = "Better than I expected.", props = { speaker = "player" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Easy lunch conversation. He asks about your friends, your job." },
    { type = "dialog", content = "You always were a terrible liar.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
]
exit_block = { type = "location", text = "Clear the plates", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }, { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Let your knee press against his. Leave it there.", targetType = "node", nodeId = "activity_lunch_together.t2" },
  { text = "Offer a bite from your fork. Watch his eyes.", targetType = "node", nodeId = "activity_lunch_together.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Hop onto the counter. Pull him close.", targetType = "node", nodeId = "activity_lunch_together.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Take his hand under the counter edge.", targetType = "node", nodeId = "activity_lunch_together.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Kneel on the kitchen mat.", targetType = "node", nodeId = "activity_lunch_together.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Pull him between your knees. Now.", targetType = "node", nodeId = "activity_lunch_together.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Knee Touch"
blocks = [
  { type = "paragraph", content = "Knees pressed together under the counter. The warmth of his leg against yours. He offers a bite from his plate. You take it." },
  { type = "video", props = { file = "activities/lunch_together_t2.jpg", description = "Legs touching under counter, sharing food", search_queries = ["legs touching under table sharing food", "intimate lunch counter"] } }
]
exit_block = { type = "location", text = "Clear the plates", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Fork Bite"
blocks = [
  { type = "paragraph", content = "He offers a bite from his fork. You lean forward, eyes on his. Take it slowly. His eyes drop to your lips. The air between you thickens." },
  { type = "video", props = { file = "activities/lunch_together_t3.jpg", description = "Feeding from fork, eye contact, intimate", search_queries = ["feeding from fork seductive eye contact", "woman eating from fork seductive eyes"] } }
]
exit_block = { type = "location", text = "Clear the plates", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Counter Kiss"
blocks = [
  { type = "paragraph", content = "You hop onto the counter. He moves between your legs. Hands on your thighs. The sandwich is irrelevant. His mouth finds yours." },
  { type = "video", props = { file = "activities/lunch_together_t4.jpg", description = "Kissing on kitchen counter, standing between her legs", search_queries = ["making out kitchen counter between her legs", "passionate kiss counter standing between legs"] } }
]
exit_block = { type = "location", text = "Eventually eat", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Counter Edge"
blocks = [
  { type = "paragraph", content = "You perch on the stool and take his hand under the counter edge. No one would know — if anyone were here to see." },
  { type = "video", props = { file = "activities/lunch_together_t6.jpg", description = "Manual under counter edge at kitchen bar", search_queries = ["manual under counter kitchen bar", "hand job kitchen stool counter edge"] } }
]
exit_block = { type = "location", text = "Finish lunch eventually", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Kitchen Mat"
blocks = [
  { type = "paragraph", content = "You kneel on the kitchen mat, bracing one hand on the cabinet door as you make quick work of his resolve." },
  { type = "video", props = { file = "activities/lunch_together_t7.jpg", description = "Oral in kitchen, kneeling on mat", search_queries = ["blowjob kitchen kneeling mat", "oral kitchen midday quick"] } }
]
exit_block = { type = "location", text = "Stand and grin", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Bar Quickie"
blocks = [
  { type = "paragraph", content = "You pull him between your knees and the world tilts. It's fast, hungry, and reckless in the middle of the day." },
  { type = "video", props = { file = "activities/lunch_together_t8.jpg", description = "Quick sex at kitchen bar, midday", search_queries = ["quick sex kitchen bar midday", "sex on stool kitchen quick"] } }
]
exit_block = { type = "location", text = "Wipe the counter", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "12:00"
end_time = "14:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "activity_pool_time"
name = "Pool Time"
description = "Summer heat. Swimsuits. Privacy fence. No one can see."

[[canvases.nodes]]
id = "base"
name = "Pool Day"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison sunbathes on the far lounger. He's in the pool. You're in a bikini. The geometry is unbearable." },
    { type = "image", props = { file = "activities/pool_time_base.jpg", description = "Pool day tense triangle", search_queries = ["pool day summer swimsuit", "backyard pool lounging summer"] } },
    { type = "paragraph", content = "She adjusts her sunglasses. He treads water. You stand at the edge of everything." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's already in the water when you come out. Watches you walk to the edge." },
    { type = "image", props = { file = "activities/pool_time_base.jpg", description = "Pool day intimate", search_queries = ["pool day summer swimsuit", "backyard pool lounging summer"] } },
    { type = "dialog", content = "Took you long enough.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Summer heat. The pool shimmers. You catch him looking at you in your swimsuit. He doesn't pretend he wasn't." },
    { type = "image", props = { file = "activities/pool_time_base.jpg", description = "Pool day warm tension", search_queries = ["pool day summer swimsuit", "backyard pool lounging summer"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Summer heat. The pool shimmers. You're in a swimsuit, he's in board shorts. The privacy fence means no one can see." },
    { type = "image", props = { file = "activities/pool_time_base.jpg", description = "Pool day summer", search_queries = ["pool day summer swimsuit", "backyard pool lounging summer"] } },
    { type = "dialog", content = "The water's perfect.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_pool_time.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_pool_time.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Swim laps, lounge on chairs.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison waves from her lounger. You wave back. The smile costs everything." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Floating on your backs, staring at the sky." },
    { type = "dialog", content = "Do you ever think about what happens after I leave?", props = { speaker = "player" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He tosses you a towel. His hand stays on yours a beat too long." },
    { type = "dialog", content = "You're getting burned.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "You float. He floats. The water holds you both up. Easy silence." },
  ] },
]
exit_block = { type = "location", text = "Dry off", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Let him put sunscreen on your back.", targetType = "node", nodeId = "activity_pool_time.t2" },
  { text = "Wrap your legs around him in the water.", targetType = "node", nodeId = "activity_pool_time.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Night swimming. Underwater lights.", targetType = "node", nodeId = "activity_pool_time.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "On the lounger. Under the bikini.", targetType = "node", nodeId = "activity_pool_time.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Slide down between his legs on the lounger.", targetType = "node", nodeId = "activity_pool_time.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "In the water. Quiet splashes.", targetType = "node", nodeId = "activity_pool_time.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Sunscreen"
blocks = [
  { type = "paragraph", content = "His hands on your back. Slow — shoulders, spine, the small of your back. Fingertips at the bikini line. You arch into his touch." },
  { type = "video", props = { file = "activities/pool_time_t2.jpg", description = "Applying sunscreen on back, lingering hands, pool", search_queries = ["sunscreen back lingering hands pool", "applying lotion back intimate"] } }
]
exit_block = { type = "location", text = "Go for a swim", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Pool Play"
blocks = [
  { type = "paragraph", content = "Splash war escalates. You wrap your legs around him for 'balance.' His hands on your thighs, holding you up. Wet skin on wet skin. Faces inches apart." },
  { type = "video", props = { file = "activities/pool_time_t3.jpg", description = "Pool play, bodies pressed together, wet, playful", search_queries = ["couple pool play bodies pressed wet bikini", "swimming together bodies close wet flirty"] } },
  { type = "paragraph", content = "'Balance' is a fiction and you both know it." }
]
exit_block = { type = "location", text = "Dry off", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Night Swimming"
blocks = [
  { type = "paragraph", content = "Night. Pool lights shimmer blue beneath the surface. He pulls you against him. Water provides cover. Your bikini top loosens. His fingers find skin." },
  { type = "video", props = { file = "activities/pool_time_t4.jpg", description = "Night pool, underwater touching, intimate, blue lights", search_queries = ["couple night pool touching underwater intimate", "pool night bikini off underwater foreplay"] } },
  { type = "dialog", content = "Anyone could see us.", props = { speaker = "player" } },
  { type = "dialog", content = "No they can't.", props = { speaker = "npc", npcId = "npc_ethan" } }
]
exit_block = { type = "location", text = "Get out of the pool", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Under the Bikini"
blocks = [
  { type = "paragraph", content = "On the lounger, his hand slips under your bikini bottom. The night air is warm; your skin warmer." },
  { type = "video", props = { file = "activities/pool_time_t6.jpg", description = "Manual stimulation on pool lounger at night", search_queries = ["manual stimulation pool lounger night", "hand under bikini lounger night"] } }
]
exit_block = { type = "location", text = "Adjust your suit", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Under Stars"
blocks = [
  { type = "paragraph", content = "You slide down between his legs on the lounger, the fence hiding you from the world. Stars watch without judging." },
  { type = "video", props = { file = "activities/pool_time_t7.jpg", description = "Oral on pool lounger at night", search_queries = ["blowjob pool lounger night", "oral outdoors private night"] } }
]
exit_block = { type = "location", text = "Catch your breath", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Night Swim More"
blocks = [
  { type = "paragraph", content = "In the water or on the lounger, you take him inside you. Quiet splashes, quiet gasps, a private universe in your backyard." },
  { type = "video", props = { file = "activities/pool_time_t8.jpg", description = "Sex by the pool at night, private backyard", search_queries = ["sex by pool night private backyard", "night sex outdoors pool area"] } }
]
exit_block = { type = "location", text = "Wrap in a towel", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 30 }]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "activity_wedding_planning"
name = "Wedding Planning Help"
description = "Seating charts and RSVPs. Helping plan his fiancee's wedding."

[[canvases.nodes]]
id = "base"
name = "Wedding Planning"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison reviews your seating chart suggestions." },
    { type = "dialog", content = "You're so helpful!", props = { speaker = "npc", npcId = "npc_madison" } },
    { type = "paragraph", content = "The gratitude is genuine. You want to disappear." },
    { type = "image", props = { file = "activities/wedding_planning_base.jpg", description = "Wedding planning tension", search_queries = ["wedding planning table documents", "seating chart invitations table"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The invitation says 'Ethan & Madison' in the font you helped pick. Your handwriting is on the envelopes." },
    { type = "image", props = { file = "activities/wedding_planning_base.jpg", description = "Wedding planning betrayal", search_queries = ["wedding planning table documents", "seating chart invitations table"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He passes you invitation samples. Your fingers overlap on the paper. The embossed names are a knife between you." },
    { type = "image", props = { file = "activities/wedding_planning_base.jpg", description = "Wedding planning tension", search_queries = ["wedding planning table documents", "seating chart invitations table"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Seating charts, RSVPs, invitation samples spread across the patio table. You're being a good sister." },
    { type = "image", props = { file = "activities/wedding_planning_base.jpg", description = "Wedding planning patio", search_queries = ["wedding planning table documents", "seating chart invitations table"] } },
    { type = "paragraph", content = "The irony is not lost on either of you." },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_wedding_planning.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_wedding_planning.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Help with RSVPs. Be a good sister.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison asks your opinion on vows. He leaves the room. You help her anyway." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "Does she make you happy?", props = { speaker = "player" } },
    { type = "dialog", content = "She makes things... simple.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You trace 'Ethan & Madison' with your fingertip. He watches your hand. Neither speaks." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "You help sort RSVPs. His hand brushes yours over a stack." },
    { type = "dialog", content = "Thanks for doing this.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
]
exit_block = { type = "location", text = "Back to the plans", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Let your fingers overlap on the invitation.", targetType = "node", nodeId = "activity_wedding_planning.t2" },
  { text = "Ask what kind of wedding he really wants.", targetType = "node", nodeId = "activity_wedding_planning.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "He puts his head in his hands. Take his hand.", targetType = "node", nodeId = "activity_wedding_planning.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Under the table, under the RSVPs.", targetType = "node", nodeId = "activity_wedding_planning.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Kneel between his chair and the table.", targetType = "node", nodeId = "activity_wedding_planning.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Sweep the invitations aside.", targetType = "node", nodeId = "activity_wedding_planning.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Invitation Samples"
blocks = [
  { type = "paragraph", content = "Your fingers overlap on a sample. He doesn't pull away. You trace the embossed 'Ethan & Madison' with your fingertip. The name is a knife between you." },
  { type = "image", props = { file = "activities/wedding_planning_t2.jpg", description = "Hands overlapping on wedding invitation, bittersweet", search_queries = ["hands overlapping invitation bittersweet", "wedding planning hands touching"] } }
]
exit_block = { type = "location", text = "Keep planning", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Dangerous Question"
blocks = [
  { type = "paragraph", content = "His eyes meet yours. Long pause." },
    { type = "dialog", content = "Small. Private. Someone who...", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He doesn't finish. Doesn't need to." },
  { type = "video", props = { file = "activities/wedding_planning_t3.jpg", description = "Loaded eye contact, unfinished sentence, emotional", search_queries = ["loaded eye contact emotional unfinished", "intense gaze meaningful pause"] } }
]
exit_block = { type = "location", text = "Change the subject", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Breaking Down"
blocks = [
  { type = "paragraph", content = "He drops his pen. Puts his head in his hands. You take his hand. Both know he's not talking about centerpieces. Forehead to forehead." },
  { type = "video", props = { file = "activities/wedding_planning_t4.jpg", description = "Comfort, foreheads touching, emotional, wedding plans visible", search_queries = ["foreheads touching emotional comfort kissing", "couple comfort kissing tender emotional"] } }
]
exit_block = { type = "location", text = "Give him space", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Under Papers"
blocks = [
  { type = "paragraph", content = "He slides a stack of RSVP cards aside and finds you under the table edge. Your breath hitches; the plans blur." },
  { type = "video", props = { file = "activities/wedding_planning_t6.jpg", description = "Manual stimulation at table among invitations", search_queries = ["manual stimulation kitchen table invitations", "hand under table wedding planning"] } }
]
exit_block = { type = "location", text = "Straighten the stack", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Between Chair and Table"
blocks = [
  { type = "paragraph", content = "You kneel between his knees as he slides back the chair. Paper rustles above; something else happens below." },
  { type = "video", props = { file = "activities/wedding_planning_t7.jpg", description = "Oral at dining table, papers scattered", search_queries = ["oral under table dining scattered papers", "blowjob at dining table wedding planning"] } }
]
exit_block = { type = "location", text = "Push in the chair", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Table Cleared"
blocks = [
  { type = "paragraph", content = "Invitations scatter to the floor as he sweeps the table. You climb up and pull him with you, paper crunching underfoot." },
  { type = "video", props = { file = "activities/wedding_planning_t8.jpg", description = "Sex on table amid wedding plans", search_queries = ["sex on table invitations on floor", "passionate sex table wedding planning"] } }
]
exit_block = { type = "location", text = "Gather the cards later", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 20 }]
[[canvases.trigger.schedules]]
start_time = "10:00"
end_time = "13:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "activity_cooking_together"
name = "Cooking Together"
description = "Making mom's old recipe. Nostalgia and kitchen teamwork."

[[canvases.nodes]]
id = "base"
name = "Cooking"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison asks to join. He says it's a 'sibling thing.' She smiles and goes to the living room." },
    { type = "image", props = { file = "activities/cooking_together_base.jpg", description = "Cooking together tension", search_queries = ["couple cooking kitchen together", "cooking together evening kitchen"] } },
    { type = "paragraph", content = "You can hear her humming from the next room." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He chops while you stir. His hip against yours at the counter." },
    { type = "image", props = { file = "activities/cooking_together_base.jpg", description = "Cooking together intimate", search_queries = ["couple cooking kitchen together", "cooking together evening kitchen"] } },
    { type = "dialog", content = "You're doing it wrong.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "Show me then.", props = { speaker = "player" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Mom's old recipe. His hands guide yours on the knife. He doesn't need to." },
    { type = "image", props = { file = "activities/cooking_together_base.jpg", description = "Cooking together warm", search_queries = ["couple cooking kitchen together", "cooking together evening kitchen"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Making mom's old recipe together. Nostalgia, laughter over shared memories." },
    { type = "image", props = { file = "activities/cooking_together_base.jpg", description = "Cooking together nostalgic", search_queries = ["couple cooking kitchen together", "cooking together evening kitchen"] } },
    { type = "dialog", content = "You're doing it wrong.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "Show me then.", props = { speaker = "player" } },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_cooking_together.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_cooking_together.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Cook together, swap stories.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She's in the next room. You can hear her humming." },
    { type = "dialog", content = "She likes your cooking.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "Remember the smoke alarm?", props = { speaker = "player" } },
    { type = "paragraph", content = "He laughs. You laugh. The kitchen smells like then and now." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He tells you about learning this recipe after you left." },
    { type = "dialog", content = "I wanted to remember.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Easy cooking banter. He burns the garlic. You rescue it. Old rhythm." },
  ] },
]
exit_block = { type = "location", text = "Plate up dinner", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Let him stand behind you at the cutting board.", targetType = "node", nodeId = "activity_cooking_together.t2" },
  { text = "Taste from the same spoon. Watch his eyes.", targetType = "node", nodeId = "activity_cooking_together.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Sauce on your lip. Let him get it.", targetType = "node", nodeId = "activity_cooking_together.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "His hand follows the trail of your skin.", targetType = "node", nodeId = "activity_cooking_together.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Slide to your knees on the tile.", targetType = "node", nodeId = "activity_cooking_together.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "He lifts you onto the counter.", targetType = "node", nodeId = "activity_cooking_together.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Guided Hands"
blocks = [
  { type = "paragraph", content = "He stands behind you at the chopping board. His hands over yours, guiding the knife. His chest warm against your back. You can feel his heartbeat." },
  { type = "video", props = { file = "activities/cooking_together_t2.jpg", description = "Guiding hands while cooking, standing behind, close", search_queries = ["guiding hands cooking behind close", "cooking together standing behind intimate"] } }
]
exit_block = { type = "location", text = "Keep cooking", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Same Spoon"
blocks = [
  { type = "paragraph", content = "He holds the spoon up. You lean forward, lips parting. His eyes on your mouth. You taste." },
    { type = "dialog", content = "Perfect.", props = { speaker = "player" } },
    { type = "paragraph", content = "The word means more than the food." },
  { type = "video", props = { file = "activities/cooking_together_t3.jpg", description = "Taste-testing from same spoon, intimate, kitchen", search_queries = ["sharing spoon tasting food seductive kitchen", "feeding from spoon intimate eye contact"] } }
]
exit_block = { type = "location", text = "Plate up dinner", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Sauce on Your Lip"
blocks = [
  { type = "paragraph", content = "Sauce on your lip. His thumb comes up to wipe it. Lingers. His eyes drop from the sauce to your lips to your eyes. The kitchen goes very quiet." },
  { type = "video", props = { file = "activities/cooking_together_t4.jpg", description = "Wiping sauce from lip with thumb, lingering, close faces", search_queries = ["wiping lip thumb kissing sensual kitchen", "thumb on lip close faces about to kiss"] } }
]
exit_block = { type = "location", text = "Serve dinner", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Taste Test"
blocks = [
  { type = "paragraph", content = "He licks a dot of sauce from your finger, then follows the trail of your skin further. You brace against the counter as your focus shifts off the stove." },
  { type = "video", props = { file = "activities/cooking_together_t6.jpg", description = "Manual on kitchen counter during cooking", search_queries = ["manual stimulation kitchen counter while cooking", "hand under clothes cooking together"] } }
]
exit_block = { type = "location", text = "Turn off a burner", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Down Low"
blocks = [
  { type = "paragraph", content = "You slide to your knees on the tile. He leans back on the counter, eyes closing as your mouth replaces any thought of dinner." },
  { type = "video", props = { file = "activities/cooking_together_t7.jpg", description = "Oral in kitchen during cooking, playful", search_queries = ["blowjob kitchen cooking playful", "kneeling oral kitchen during cooking"] } }
]
exit_block = { type = "location", text = "Stir later", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Counter Heat"
blocks = [
  { type = "paragraph", content = "He lifts you onto the counter and slides into you. The pot sizzles on an empty burner; you both start laughing and turn it off between kisses." },
  { type = "video", props = { file = "activities/cooking_together_t8.jpg", description = "Sex on counter while cooking, playful chaos", search_queries = ["sex on kitchen counter while cooking", "passionate counter sex stove on"] } }
]
exit_block = { type = "location", text = "Order takeout instead", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 20 }]
[[canvases.trigger.schedules]]
start_time = "17:00"
end_time = "18:30"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "is_true"
[[canvases.trigger.conditions.items]]
type = "days_since_flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "gte"
value = 1

[[canvases]]
id = "activity_dinner_ethan"
name = "Dinner with Ethan"
description = "Dinner conversation with undercurrents. Wine optional."

[[canvases.nodes]]
id = "base"
name = "Dinner"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Three place settings. Madison talks about the honeymoon. Bali. She's excited. You drink faster." },
    { type = "image", props = { file = "activities/dinner_ethan_base.jpg", description = "Dinner with three tense", search_queries = ["dinner table wine evening", "couple dinner conversation wine"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Wine with dinner. The conversation dives straight in. His foot finds yours from the first pour." },
    { type = "image", props = { file = "activities/dinner_ethan_base.jpg", description = "Dinner intimate", search_queries = ["dinner table wine evening", "couple dinner conversation wine"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Second glass. He asks about your life. You ask about the wedding. Both deflecting." },
    { type = "image", props = { file = "activities/dinner_ethan_base.jpg", description = "Dinner warm tension", search_queries = ["dinner table wine evening", "couple dinner conversation wine"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Dinner conversation. He asks about your dating life, you deflect. Normal family dinner with undercurrents." },
    { type = "image", props = { file = "activities/dinner_ethan_base.jpg", description = "Dinner conversation wine", search_queries = ["dinner table wine evening", "couple dinner conversation wine"] } },
    { type = "paragraph", content = "Wine with dinner. Elbows on the table, leaning in." },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_dinner_ethan.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_dinner_ethan.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Pleasant dinner conversation.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

    { targetType = "player", trait = "energy", op = "add", value = 10, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison clears the plates. He looks at you over her shoulder. You look away first." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "Why her?", props = { speaker = "player" } },
    { type = "dialog", content = "Because she was safe. Because she wasn't you.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "You know why I left.", props = { speaker = "player" } },
    { type = "dialog", content = "I know why you left.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "The truth is a third guest at the table." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Wine loosens the conversation. He asks why you stayed away so long. You give the rehearsed answer." },
  ] },
]
exit_block = { type = "location", text = "Clear the table", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }, { targetType = "player", trait = "energy", op = "add", value = 10, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Pour a second glass. Lean closer.", targetType = "node", nodeId = "activity_dinner_ethan.t2" },
  { text = "'You know why.' Let the words hang.", targetType = "node", nodeId = "activity_dinner_ethan.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Your bare foot finds his calf. Slides up.", targetType = "node", nodeId = "activity_dinner_ethan.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Guide his hand under the tablecloth.", targetType = "node", nodeId = "activity_dinner_ethan.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Slide under the tablecloth.", targetType = "node", nodeId = "activity_dinner_ethan.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Sweep the plates aside.", targetType = "node", nodeId = "activity_dinner_ethan.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Second Glass"
blocks = [
  { type = "paragraph", content = "Second glass loosens things. He asks why you stayed away. The answer is on the tip of your tongue. You hold it back — barely." },
  { type = "video", props = { file = "activities/dinner_ethan_t2.jpg", description = "Deep dinner conversation, wine, loaded questions", search_queries = ["deep conversation dinner wine loaded", "intimate dinner questioning"] } }
]
exit_block = { type = "location", text = "Clear the plates", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "You Know Why"
blocks = [
  { type = "dialog", content = "You know why.", props = { speaker = "player" } },
    { type = "paragraph", content = "His fork stops. The air thickens. Two words that change the entire dinner from catch-up to confession." },
  { type = "video", props = { file = "activities/dinner_ethan_t3.jpg", description = "Fork stopping, intense eye contact across dinner table", search_queries = ["intense eye contact dinner table sexual tension", "couple dinner loaded stare sexual tension"] } }
]
exit_block = { type = "location", text = "Finish dinner", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Under the Table"
blocks = [
  { type = "paragraph", content = "Your bare foot finds his calf under the table. Slides up. He grips the edge of the table. His eyes widen. Neither of you breaks eye contact." },
  { type = "video", props = { file = "activities/dinner_ethan_t4.jpg", description = "Footsie under dinner table, tension, gripping table edge", search_queries = ["footsie under table foreplay dinner sexual", "foot rubbing leg under dinner table teasing"] } }
]
exit_block = { type = "location", text = "Dessert?", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Under-Table Hand"
blocks = [
  { type = "paragraph", content = "You lace fingers under the tablecloth and then guide him to your thigh. He doesn't look up from his plate; neither do you." },
  { type = "video", props = { file = "activities/dinner_ethan_t6.jpg", description = "Manual under dining table, evening", search_queries = ["manual under table dining", "hand under skirt dinner table"] } }
]
exit_block = { type = "location", text = "Clear plates slowly", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Under the Table"
blocks = [
  { type = "paragraph", content = "You slide under the tablecloth and make dinner irrelevant. The silverware rattles once; you both freeze and then laugh." },
  { type = "video", props = { file = "activities/dinner_ethan_t7.jpg", description = "Oral under dining table, playful risk", search_queries = ["blowjob under table dining playful", "oral dinner table risk playful"] } }
]
exit_block = { type = "location", text = "Set the forks straight", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Table Again"
blocks = [
  { type = "paragraph", content = "You sweep plates aside and pull him over you on the table. It's messy and perfect and neither of you cares." },
  { type = "video", props = { file = "activities/dinner_ethan_t8.jpg", description = "Sex on dining table, messy and passionate", search_queries = ["sex dining table plates aside", "passionate sex dinner table"] } }
]
exit_block = { type = "location", text = "Dishwasher later", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "21:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "is_true"
[[canvases.trigger.conditions.items]]
type = "days_since_flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "gte"
value = 1

[[canvases]]
id = "activity_movie_night"
name = "Movie Night"
description = "Big couch, blanket, and a movie neither of you is watching."

[[canvases.nodes]]
id = "base"
name = "Movie Night"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison sits between you on the couch. His hand finds yours behind her back." },
    { type = "image", props = { file = "activities/movie_night_base.jpg", description = "Movie night couch tense", search_queries = ["movie night couch blanket popcorn", "couple watching TV couch blanket"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "No popcorn bowl between you. You sit against him from the start. His arm is automatic now." },
    { type = "image", props = { file = "activities/movie_night_base.jpg", description = "Movie night intimate", search_queries = ["movie night couch blanket popcorn", "couple watching TV couch blanket"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The popcorn bowl is between you. A buffer. Both pretending you need it." },
    { type = "image", props = { file = "activities/movie_night_base.jpg", description = "Movie night buffer", search_queries = ["movie night couch blanket popcorn", "couple watching TV couch blanket"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Big couch, blanket draped over the armrest, popcorn between you. Neither of you is really watching." },
    { type = "image", props = { file = "activities/movie_night_base.jpg", description = "Movie night couch", search_queries = ["movie night couch blanket popcorn", "couple watching TV couch blanket"] } },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_movie_night.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_movie_night.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Watch the movie.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison falls asleep on his shoulder. He looks at you over her head. Nobody watches the movie." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "We used to watch this exact one. Remember?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "You remember. You remember everything about that summer." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "This is nice.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "Yeah. It is.", props = { speaker = "player" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "The movie fills the silence. You argue about the plot like you used to. His laugh is the same." },
  ] },
]
exit_block = { type = "location", text = "Credits roll", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Scoot past the popcorn bowl. Closer.", targetType = "node", nodeId = "activity_movie_night.t2" },
  { text = "Head on his shoulder. Let his arm settle.", targetType = "node", nodeId = "activity_movie_night.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "His hand finds your thigh under the blanket.", targetType = "node", nodeId = "activity_movie_night.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "The blanket becomes a tent for two.", targetType = "node", nodeId = "activity_movie_night.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Slide down the couch under the blanket.", targetType = "node", nodeId = "activity_movie_night.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Climb onto his lap. Blanket falls away.", targetType = "node", nodeId = "activity_movie_night.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Closer Under the Blanket"
blocks = [
  { type = "paragraph", content = "You shiver — barely convincing — and scoot past the popcorn bowl. Your thigh presses against his. Heat radiates through the blanket. He doesn't move away. The movie continues. Neither of you could name the scene." },
  { type = "video", props = { file = "activities/movie_night_t2.jpg", description = "Scooting closer on couch under blanket, thighs touching", search_queries = ["couple close couch blanket thighs", "scooting closer couch movie night"] } }
]
exit_block = { type = "location", text = "Movie ends", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Head on Shoulder"
blocks = [
  { type = "paragraph", content = "Your head drifts to his shoulder. His arm settles around you — natural as breathing. His fingers trace absent patterns on your arm." },
    { type = "dialog", content = "Just like we used to.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "It doesn't feel like it used to.", props = { speaker = "player" } },
    { type = "paragraph", content = "No. It doesn't." },
  { type = "video", props = { file = "activities/movie_night_cuddle.jpg", description = "Head on shoulder, arm around her, fingers tracing arm", search_queries = ["cuddling couch head on shoulder arm around", "couple cuddling blanket couch intimate"] } }
]
exit_block = { type = "location", text = "Credits roll", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Wandering Hands"
blocks = [
  { type = "paragraph", content = "Under the blanket, his hand finds your thigh. Innocent at first. Then higher. Your hand finds his. Intertwines. Then moves to his leg. The movie is background noise. Both of your breathing has changed." },
  { type = "video", props = { file = "activities/movie_night_t4.jpg", description = "Under blanket hands on thigh, tension, heavy breathing", search_queries = ["hand on thigh under blanket couch foreplay", "touching thigh under blanket couch sexual tension"] } }
]
exit_block = { type = "location", text = "Pull the blanket tighter", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Under-Blanket Manual"
blocks = [
  { type = "paragraph", content = "The blanket becomes a tent for two. His hand finds a rhythm, and your breath stutters as the movie drones on, forgotten." },
  { type = "video", props = { file = "activities/movie_night_t6.jpg", description = "Under-blanket handplay on couch, discreet and intimate", search_queries = ["under blanket hand job couch", "discreet couch intimacy blanket"] } }
]
exit_block = { type = "location", text = "Let the credits roll", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Under-Blanket Oral"
blocks = [
  { type = "paragraph", content = "You slide down the couch and take him in your mouth. The blanket hides you; his hand curls in your hair, eyes on the ceiling, stunned and grateful." },
  { type = "video", props = { file = "activities/movie_night_t7.jpg", description = "Oral under blanket on couch, careful and quiet", search_queries = ["blowjob under blanket couch discreet", "quiet oral on couch blanket night"] } }
]
exit_block = { type = "location", text = "Straighten the blanket", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Couch Intimacy"
blocks = [
  { type = "paragraph", content = "You climb back onto his lap and guide him inside you. Breathless and close, you try to be quiet and fail, laughing softly against his mouth." },
  { type = "video", props = { file = "activities/movie_night_t8.jpg", description = "Sex on couch at night, blanket askew", search_queries = ["sex on couch night blanket aside", "riding on couch night intimacy"] } }
]
exit_block = { type = "location", text = "Find the remote eventually", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 15 }]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "is_true"

[[canvases]]
id = "activity_wine_talk"
name = "Wine & Talk"
description = "Wine, stars, and conversations the daylight won't allow."

[[canvases.nodes]]
id = "base"
name = "Wine & Talk"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He brings the bottle outside after Madison falls asleep. You're already waiting." },
    { type = "image", props = { file = "activities/wine_talk_base.jpg", description = "Wine on patio desperate", search_queries = ["wine patio night stars two glasses", "couple wine outside evening stars"] } },
    { type = "paragraph", content = "The patio is your sanctuary now. The stars are the same. Everything else has changed." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Two glasses. No pretense. The wine is an excuse but not the reason." },
    { type = "image", props = { file = "activities/wine_talk_base.jpg", description = "Wine patio intimate", search_queries = ["wine patio night stars two glasses", "couple wine outside evening stars"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "A bottle on the patio table. Stars overhead. The wine loosens what the daylight holds tight." },
    { type = "image", props = { file = "activities/wine_talk_base.jpg", description = "Wine patio confessional", search_queries = ["wine patio night stars two glasses", "couple wine outside evening stars"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "A bottle of wine on the patio table. Two glasses. Stars overhead, privacy fence all around." },
    { type = "image", props = { file = "activities/wine_talk_base.jpg", description = "Wine on patio starlight", search_queries = ["wine patio night stars two glasses", "couple wine outside evening stars"] } },
    { type = "paragraph", content = "The wine loosens tongues and the night air makes everything feel confessional." },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_wine_talk.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_wine_talk.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "One glass, stargazing.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "How many more nights do we have?", props = { speaker = "player" } },
    { type = "paragraph", content = "The wine makes you brave enough to count. The stars don't answer." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "That summer — what would have happened if I'd stayed?", props = { speaker = "player" } },
    { type = "dialog", content = "Everything. Everything would have happened.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "I need to tell you something.", props = { speaker = "player" } },
    { type = "paragraph", content = "The wine gives you courage the daylight won't. He sets his glass down." },
    { type = "dialog", content = "Tell me.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Stars and wine. He asks about your life. You ask about his. The answers get real." },
  ] },
]
exit_block = { type = "location", text = "Cork the bottle", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Second glass. Let the conversation drift.", targetType = "node", nodeId = "activity_wine_talk.t2" },
  { text = "Liquid courage. Say what you mean.", targetType = "node", nodeId = "activity_wine_talk.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Lean across the table. We shouldn't.", targetType = "node", nodeId = "activity_wine_talk.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "His hand under your dress. The night keeps secrets.", targetType = "node", nodeId = "activity_wine_talk.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Slide off the lounger.", targetType = "node", nodeId = "activity_wine_talk.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Pull him down onto the lounger.", targetType = "node", nodeId = "activity_wine_talk.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Second Glass"
blocks = [
  { type = "paragraph", content = "Second glass. The conversation drifts into dangerous territory." },
    { type = "dialog", content = "Do you ever think about that summer?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He doesn't finish. Doesn't need to. The stars are impossibly bright and the wine is warm in your chest." },
  { type = "video", props = { file = "activities/wine_talk_t2.jpg", description = "Second glass of wine, deep conversation under stars", search_queries = ["deep conversation wine night outdoor", "couple wine talking stars patio"] } }
]
exit_block = { type = "location", text = "Finish the bottle another night", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Liquid Courage"
blocks = [
  { type = "dialog", content = "I need to tell you something.", props = { speaker = "player" } },
    { type = "paragraph", content = "The wine gives you courage the daylight won't. He sets his glass down. Turns to face you." },
    { type = "dialog", content = "Tell me.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "The night is patient. The words come out messier than planned." },
  { type = "video", props = { file = "activities/wine_talk_t3.jpg", description = "Confession moment on patio, setting wine glass down, turning to face", search_queries = ["confession wine patio night turning emotional", "couple wine deep talk outdoor night romantic"] } }
]
exit_block = { type = "location", text = "Cork the bottle", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Leaning In"
blocks = [
  { type = "dialog", content = "We shouldn't.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "I know.", props = { speaker = "player" } },
    { type = "paragraph", content = "But you're already leaning across the patio table. His hand catches your chin. Thumb on your lower lip. Stars above. Privacy fence around. Nobody but the night." },
  { type = "video", props = { file = "activities/wine_talk_t4.jpg", description = "Leaning across table, chin touch, intimate patio moment under stars", search_queries = ["chin touch leaning in kiss patio night", "couple about to kiss outdoor wine romantic"] } }
]
exit_block = { type = "location", text = "Head inside", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Hand Under Dress"
blocks = [
  { type = "paragraph", content = "On the lounger, his hand slips under your dress. The night keeps your secret." },
  { type = "video", props = { file = "activities/wine_talk_t6.jpg", description = "Manual on patio lounger at night", search_queries = ["manual stimulation patio lounger night", "hand under dress outdoors night private"] } }
]
exit_block = { type = "location", text = "Top off the wine", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Stars Above"
blocks = [
  { type = "paragraph", content = "You slide off the lounger and take him in your mouth. The fence, the stars, the two of you — everything feels far away." },
  { type = "video", props = { file = "activities/wine_talk_t7.jpg", description = "Oral outdoors at night on patio", search_queries = ["blowjob patio night private", "oral outdoors patio night"] } }
]
exit_block = { type = "location", text = "Sit back up", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Patio Furniture"
blocks = [
  { type = "paragraph", content = "You turn and pull him down with you on the lounger. The cushion creaks; your breath does too." },
  { type = "video", props = { file = "activities/wine_talk_t8.jpg", description = "Sex on patio furniture at night", search_queries = ["sex on patio lounger night", "outdoor sex private patio night"] } }
]
exit_block = { type = "location", text = "Gather the glasses", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 20 }]
[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "is_true"

[[canvases]]
id = "activity_late_night_kitchen"
name = "Late Night Kitchen"
description = "Midnight insomnia, whispers, and sleep clothes."

[[canvases.nodes]]
id = "base"
name = "Late Night Kitchen"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He checks the hallway twice before closing the kitchen door. She's asleep upstairs." },
    { type = "image", props = { file = "activities/cant_sleep.jpg", description = "Late night kitchen hiding", search_queries = ["late night kitchen dark fridge light", "insomnia kitchen midnight"] } },
    { type = "paragraph", content = "The click of the latch sounds like a confession." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's leaning against the counter, waiting. Boxers and nothing else. Not pretending anymore." },
    { type = "image", props = { file = "activities/cant_sleep.jpg", description = "Late night kitchen waiting", search_queries = ["late night kitchen dark fridge light", "insomnia kitchen midnight"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Both can't sleep. He's in boxers. You're in a nightgown. Eyes meet over the fridge light." },
    { type = "image", props = { file = "activities/cant_sleep.jpg", description = "Late night kitchen tension", search_queries = ["late night kitchen dark fridge light", "insomnia kitchen midnight"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Both can't sleep. The kitchen at 1 AM feels different — smaller, more intimate. Eyes meet over the fridge light." },
    { type = "image", props = { file = "activities/cant_sleep.jpg", description = "Late night kitchen insomnia", search_queries = ["late night kitchen dark fridge light", "insomnia kitchen midnight"] } },
    { type = "paragraph", content = "Both pretend not to notice. Both notice everything. The fridge hums." },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_late_night_kitchen.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_late_night_kitchen.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Midnight snack. Back to bed.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "What happens when she finds out?", props = { speaker = "player" } },
    { type = "paragraph", content = "His hand tightens on his glass." },
    { type = "dialog", content = "I don't know.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "The honesty is the loudest thing in the room." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "I can't stop thinking about you.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He says it to the countertop. The confession fills the dark." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "Can't sleep either?", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "dialog", content = "It's not the coffee.", props = { speaker = "player" } },
    { type = "dialog", content = "No. It's not.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Midnight snacking in near-darkness. The fridge hum is the loudest thing. Both pretending this is about insomnia." },
  ] },
]
exit_block = { type = "location", text = "Back upstairs", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Cross the three feet between you.", targetType = "node", nodeId = "activity_late_night_kitchen.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "'I keep thinking about you.' Close the distance.", targetType = "node", nodeId = "activity_late_night_kitchen.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Brace on the counter. Let his hand find you.", targetType = "node", nodeId = "activity_late_night_kitchen.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Sink to your knees on the tile.", targetType = "node", nodeId = "activity_late_night_kitchen.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "He lifts you onto the counter.", targetType = "node", nodeId = "activity_late_night_kitchen.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t3"
name = "Loaded Question"
blocks = [
  { type = "dialog", content = "Can't sleep either?", props = { speaker = "player" } },
    { type = "paragraph", content = "You both know why neither can sleep. It's not the coffee. He leans against the counter. You lean against the opposite one. Three feet of kitchen floor between you. It might as well be an ocean. Or nothing." },
  { type = "video", props = { file = "activities/late_night_kitchen_t3.jpg", description = "Leaning on opposite kitchen counters, midnight tension, loaded silence", search_queries = ["sexual tension kitchen midnight two people", "man woman kitchen counter tension night sleepwear"] } }
]
exit_block = { type = "location", text = "Warm milk helps", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Whispered Confession"
blocks = [
  { type = "dialog", content = "I keep thinking about you.", props = { speaker = "player" } },
    { type = "paragraph", content = "Whispered into the dark kitchen. You cross the three feet between you. His back against the counter. Your hands on his chest. Heartbeat under your palms." },
  { type = "video", props = { file = "activities/late_night_kitchen_t4.jpg", description = "Crossing kitchen to him, hands on chest, whispered confession, dark", search_queries = ["crossing kitchen hands on chest midnight kiss", "couple kissing midnight kitchen hands chest"] } }
]
exit_block = { type = "location", text = "Go upstairs", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Counter Manual"
blocks = [
  { type = "paragraph", content = "You brace on the counter as his hand works you open. The kitchen feels charged at this hour — breath, touch, the hum of the fridge." },
  { type = "video", props = { file = "activities/late_night_kitchen_t6.jpg", description = "Manual stimulation in kitchen at night against counter", search_queries = ["hand under nightgown kitchen counter night", "manual stimulation kitchen midnight"] } }
]
exit_block = { type = "location", text = "Catch your breath", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Quiet Kneel"
blocks = [
  { type = "paragraph", content = "You sink to your knees on the tile. He tastes like salt and sleep. His hand finds your hair; he bites his lip to stay quiet." },
  { type = "video", props = { file = "activities/late_night_kitchen_t7.jpg", description = "Oral in kitchen at night, discreet and intimate", search_queries = ["blowjob kitchen night discreet", "kneeling oral kitchen counter night"] } }
]
exit_block = { type = "location", text = "Stand up slowly", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Counter Intimacy"
blocks = [
  { type = "paragraph", content = "He lifts you onto the counter and slides inside you. You try to be quiet; you fail, breath catching as you cling to his shoulders." },
  { type = "video", props = { file = "activities/late_night_kitchen_t8.jpg", description = "Sex on kitchen counter at night, urgent and quiet", search_queries = ["sex on kitchen counter night urgent", "quiet sex kitchen counter midnight"] } }
]
exit_block = { type = "location", text = "Sneak back upstairs", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 20 }]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "sleepless_night_complete"
operator = "is_true"

[[canvases]]
id = "activity_goodnight"
name = "Saying Goodnight"
description = "Bedroom doors ten feet apart. The goodnight ritual."

[[canvases.nodes]]
id = "base"
name = "Saying Goodnight"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison's voice from his room: 'Coming to bed?' He looks at you. The hallway feels like a canyon." },
    { type = "image", props = { file = "activities/hallway_doorway_flirt.jpg", description = "Hallway goodbye tense", search_queries = ["hallway doorway night goodbye", "standing between two doors hallway"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Standing between two doors. His and yours. The goodnight takes longer every night." },
    { type = "image", props = { file = "activities/hallway_doorway_flirt.jpg", description = "Hallway goodbye intimate", search_queries = ["hallway doorway night goodbye", "standing between two doors hallway"] } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The hug lasts too long. He pulls back. Something unfinished in his eyes." },
    { type = "image", props = { file = "activities/hallway_doorway_flirt.jpg", description = "Hallway goodbye unfinished", search_queries = ["hallway doorway night goodbye", "standing between two doors hallway"] } },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Bedroom doors ten feet apart. The goodnight ritual. Neither wants to be the first through their door." },
    { type = "image", props = { file = "activities/hallway_doorway_flirt.jpg", description = "Hallway goodnight", search_queries = ["hallway doorway night goodbye", "standing between two doors hallway"] } },
  ] },
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him", targetType = "node", nodeId = "activity_goodnight.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_goodnight.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Quick goodnight. Separate doors.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },

    { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 3, clamp = true },

  ] }
] }

[[canvases.nodes]]
id = "emotional"
name = "Conversation"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "I should go in. She's waiting.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He doesn't move. You don't move. The hallway holds its breath." },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "I don't want tonight to end.", props = { speaker = "player" } },
    { type = "dialog", content = "Then don't let it.", props = { speaker = "npc", npcId = "npc_ethan" } },
  ] },
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "dialog", content = "Goodnight.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He says it but doesn't turn away. Neither do you." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "A brief hug." },
    { type = "dialog", content = "Sleep well.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "He smells like soap and something warm. You pull back before it gets complicated." },
  ] },
]
exit_block = { type = "location", text = "Your door. Close it.", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "physical"
name = "Getting Closer"
blocks = [
  { type = "paragraph", content = "Words can wait." }
]
exit_block = { type = "choices", choices = [
  { text = "Let the hug linger. Press closer.", targetType = "node", nodeId = "activity_goodnight.t2" },
  { text = "'What if I can't sleep?' Watch his face.", targetType = "node", nodeId = "activity_goodnight.t3", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "flirt_unlock", operator = "is_true" }
  ] } },
  { text = "Pin him against his door.", targetType = "node", nodeId = "activity_goodnight.t4", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "kiss_unlock", operator = "is_true" }
  ] } },
  { text = "Between his body and the wood. His hand finds you.", targetType = "node", nodeId = "activity_goodnight.t6", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "manual_unlock", operator = "is_true" }
  ] } },
  { text = "Just inside the door. Kneel.", targetType = "node", nodeId = "activity_goodnight.t7", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "oral_unlock", operator = "is_true" }
  ] } },
  { text = "Whose room? Does it matter?", targetType = "node", nodeId = "activity_goodnight.t8", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "sex_unlock", operator = "is_true" }
  ] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Lingering Hug"
blocks = [
  { type = "paragraph", content = "The hug goes on. His arms tighten. Your face presses into his neck. He smells like soap and something that's just him. He pulls back — looks at you. A beat too long. Releases you like it costs something." },
  { type = "video", props = { file = "activities/goodnight_t2.jpg", description = "Lingering hug in hallway, reluctant release, intense eye contact", search_queries = ["lingering hug hallway reluctant release", "long hug pulling back eye contact night"] } }
]
exit_block = { type = "location", text = "Goodnight", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 3, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Dangerous Invitation"
blocks = [
  { type = "dialog", content = "What if I can't sleep?", props = { speaker = "player" } },
    { type = "dialog", content = "Then come find me.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "His door closes. The invitation hangs in the hallway air. You stand between the two doors. Your room is safety. His room is everything else." },
  { type = "video", props = { file = "activities/goodnight_t3.jpg", description = "Hallway between two doors, invitation, standing alone deciding", search_queries = ["hallway bedroom doors night invitation suggestive", "standing between bedrooms night sexual tension"] } }
]
exit_block = { type = "location", text = "Your door. For now.", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 4, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 2, clamp = true }] } }

[[canvases.nodes]]
id = "t4"
name = "Against the Door"
blocks = [
  { type = "paragraph", content = "He pins you against your bedroom door." },
    { type = "dialog", content = "We should stop.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Your hands pull him closer." },
    { type = "dialog", content = "We should.", props = { speaker = "player" } },
    { type = "paragraph", content = "His mouth finds your neck. The door handle digs into your back. Neither of you reaches for it." },
  { type = "video", props = { file = "activities/goodnight_t4.jpg", description = "Pinned against bedroom door, kissing neck, hallway at night", search_queries = ["pinned against door kissing neck passionate", "making out against bedroom door hallway"] } }
]
exit_block = { type = "location", text = "Separate doors. Barely.", config = { destinationType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 5, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[[canvases.nodes]]
id = "t6"
name = "Against the Door (Further)"
blocks = [
  { type = "paragraph", content = "Pinned between his body and the wood, his hand finds you without asking. You nod anyway." },
  { type = "video", props = { file = "activities/goodnight_t6.jpg", description = "Manual stimulation against bedroom door at night", search_queries = ["manual stimulation against door hallway night", "hand under skirt against door"] } }
]
exit_block = { type = "location", text = "Keys jingle down the hall", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 6, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 4, clamp = true }] } }

[[canvases.nodes]]
id = "t7"
name = "Just Inside"
blocks = [
  { type = "paragraph", content = "Inside the door, you sink to your knees before it clicks shut. He exhales your name like relief." },
  { type = "video", props = { file = "activities/goodnight_t7.jpg", description = "Oral just inside bedroom door at night", search_queries = ["blowjob inside bedroom door night", "kneeling oral doorway night"] } }
]
exit_block = { type = "location", text = "Stand, dizzy", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 7, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t8"
name = "Whose Room"
blocks = [
  { type = "paragraph", content = "You're not sure whose room it is when you finally break apart. It doesn't matter. The door clicks. The world narrows." },
  { type = "video", props = { file = "activities/goodnight_t8.jpg", description = "Sex in bedroom doorway/just inside, night", search_queries = ["sex bedroom doorway night", "quick sex just inside bedroom door night"] } }
]
exit_block = { type = "location", text = "Lights off", config = { destinationType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 2, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "corruption", op = "add", value = 8, clamp = true }, { targetType = "player", trait = "boldness", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_home"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 10 }]
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "welcome_dinner_complete"
operator = "is_true"

[[canvases]]
id = "solo_sleep"
name = "Sleep"
description = "Rest in your old room."

[[canvases.nodes]]
id = "base"
name = "Sleep"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The sheets smell like you and faintly like him. You press your face into the pillow and breathe." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "You lie down on the bed. The familiar ceiling, the old posters. So much has changed, but this room feels like a time capsule. Your eyes are heavy." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Take a short nap (1 hour)", targetType = "trigger", time_progression_minutes = 60, effects = [{ targetType = "player", trait = "energy", op = "add", value = 20, clamp = true }] },
  { text = "Sleep until morning", targetType = "trigger", time_progression_minutes = 480, effects = [{ targetType = "player", trait = "energy", op = "set", value = 100, clamp = true }] },
] }

[canvases.trigger]
location = "loc_player_room"
is_active = true
is_repeatable = true
max_triggers_per_day = 2
priority = 1

[[canvases]]
id = "solo_shower"
name = "Shower"
description = "Hot water and a moment to decompress."

[[canvases.nodes]]
id = "base"
name = "Shower"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Hot water runs over skin that still remembers his hands. The steam doesn't wash away the feeling. You don't want it to." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Hot water, steam on the mirror. A moment to decompress and process everything that's happening. The shared bathroom means you can hear him in the hallway sometimes." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Quick rinse", targetType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "energy", op = "add", value = 5, clamp = true }] },
  { text = "Long shower, let the water run", targetType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "player", trait = "energy", op = "add", value = 10, clamp = true }] },
] }

[canvases.trigger]
location = "loc_bathroom"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1

[[canvases]]
id = "solo_get_ready"
name = "Get Ready"
description = "Mirror, makeup, clothes. Knowing who will see."
[[canvases.nodes]]
id = "base"
name = "Get Ready"
[[canvases.nodes.blocks]]
type = "paragraph"
content = "Mirror, makeup, clothes. Choosing what to wear — knowing who will see. You spend more time getting ready than you used to. You tell yourself it's just because you're on vacation."


[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Keep it casual"
targetType = "trigger"
time_progression_minutes = 15

[[canvases.nodes.exit_block.choices]]
text = "Put in effort today"
targetType = "trigger"
time_progression_minutes = 30
[[canvases.nodes.exit_block.choices.effects]]
targetType = "player"
trait = "corruption"
op = "add"
value = 2
clamp = true



[canvases.trigger]
location = "loc_bathroom"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 10 }]

[[canvases]]
id = "solo_unpack"
name = "Unpack"
description = "Settling back into a space that's yours but isn't anymore."
[[canvases.nodes]]
id = "base"
name = "Unpack"
[[canvases.nodes.blocks]]
type = "paragraph"
content = "Unpacking in your old room. You find things you left behind — an old journal, a photo strip from the mall with Ethan. His arm around you, both of you laughing. You were sixteen. You put it face-down on the nightstand."


[canvases.nodes.exit_block]
type = "location"
text = "Settle in"
[canvases.nodes.exit_block.config]
destinationType = "trigger"
time_progression_minutes = 60
[[canvases.nodes.exit_block.config.effects]]
targetType = "player"
trait = "corruption"
op = "add"
value = 2
clamp = true


[canvases.trigger]
location = "loc_player_room"
is_active = true
is_repeatable = false
max_triggers_per_day = 1
priority = 1

[[canvases]]
id = "solo_phone_scroll"
name = "Phone Scroll"
description = "Scrolling, texting, avoiding."
[[canvases.nodes]]
id = "base"
name = "Phone Scroll"
[[canvases.nodes.blocks]]
type = "paragraph"
content = "Scrolling social media, texting friends, avoiding what you should be thinking about. Your friend asks how the trip is. 'Fine,' you type. Delete it. 'Complicated.' Delete that too. 'Fine.'"


[canvases.nodes.exit_block]
type = "location"
text = "Put the phone down"
[canvases.nodes.exit_block.config]
destinationType = "trigger"
time_progression_minutes = 30

[canvases.trigger]
location = "loc_player_room"
is_active = true
is_repeatable = true
max_triggers_per_day = 2
priority = 1
costs = [{ trait = "energy", value = 15 }]

[[canvases]]
id = "solo_swim_alone"
name = "Swim Alone"
description = "The pool is different when he's not here."
[[canvases.nodes]]
id = "base"
name = "Swim Alone"
[[canvases.nodes.blocks]]
type = "paragraph"
content = "Swimming laps alone. The pool is different when he's not here — peaceful, meditative. The sun on your skin. Floating and thinking. The water holds you up when everything else feels heavy."


[canvases.nodes.exit_block]
type = "location"
text = "Dry off"
[canvases.nodes.exit_block.config]
destinationType = "trigger"
time_progression_minutes = 45
[[canvases.nodes.exit_block.config.effects]]
targetType = "player"
trait = "energy"
op = "add"
value = 10
clamp = true


[canvases.trigger]
location = "loc_backyard"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 5 }]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

[[canvases]]
id = "solo_wander"
name = "Wander the House"
description = "The house is a museum of your shared childhood."
[[canvases.nodes]]
id = "base"
name = "Wander"
[[canvases.nodes.blocks]]
type = "paragraph"
content = "Walking through the house. Family photos in the hallway — you and Ethan at someone's birthday, standing too close. Peeking into rooms. The house is a museum of your shared childhood. You pass his door. It's open a crack. You keep walking."


[canvases.nodes.exit_block]
type = "location"
text = "Return to your room"
[canvases.nodes.exit_block.config]
destinationType = "trigger"
time_progression_minutes = 15

[canvases.trigger]
location = "loc_home"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 5 }]

[[canvases]]
id = "solo_journal"
name = "Journal"
description = "Processing the day on paper."

[[canvases.nodes]]
id = "base"
name = "Journal"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You wrote his name. Crossed it out. Wrote it again. The pen knows what you won't say out loud." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Writing in the journal you found while unpacking. Processing the day. You write about the house, the weather, the food. You don't write about the way his hand felt on your back. But you think about it for the rest of the page." }
  ] }
]
exit_block = { type = "location", text = "Close the journal", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "player", trait = "boldness", op = "add", value = 3, clamp = true }] } }

[canvases.trigger]
location = "loc_player_room"
is_active = true
is_repeatable = true
max_triggers_per_day = 3
priority = 1
costs = [{ trait = "energy", value = 20 }]

[[canvases]]
id = "solo_lie_down"
name = "Lie Down"
description = "Close your eyes for a bit. Not sleeping, just resting."

[[canvases.nodes]]
id = "base"
name = "Lie Down"
blocks = [
  { type = "paragraph", content = "You lie back on the bed and stare at the ceiling. Not sleeping. Just letting your body be still for a minute. The fan hums. Light moves across the wall. Your thoughts slow down enough to breathe." }
]
exit_block = { type = "choices", choices = [
  { text = "Just close your eyes", targetType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "energy", op = "add", value = 10, clamp = true }] },
  { text = "Drift for a while", targetType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "player", trait = "energy", op = "add", value = 15, clamp = true }] },
] }

[canvases.trigger]
location = "loc_player_room"
is_active = true
is_repeatable = true
max_triggers_per_day = 3
priority = 1

[[canvases]]
id = "solo_snack"
name = "Grab a Snack"
description = "Coffee, leftovers, whatever's in the fridge."

[[canvases.nodes]]
id = "base"
name = "Snack"
blocks = [
  { type = "paragraph", content = "You rummage through the fridge. Leftover pasta, a half-eaten pie, cold coffee you reheat in the microwave. Standing at the counter eating out of the container like a civilized adult." }
]
exit_block = { type = "choices", choices = [
  { text = "Quick coffee", targetType = "trigger", time_progression_minutes = 10, effects = [{ targetType = "player", trait = "energy", op = "add", value = 5, clamp = true }] },
  { text = "Proper snack", targetType = "trigger", time_progression_minutes = 20, effects = [{ targetType = "player", trait = "energy", op = "add", value = 8, clamp = true }] },
] }

[canvases.trigger]
location = "loc_kitchen"
is_active = true
is_repeatable = true
max_triggers_per_day = 3
priority = 1

[[canvases]]
id = "solo_relax"
name = "Relax on the Couch"
description = "Sit down, breathe, do nothing for a while."

[[canvases.nodes]]
id = "base"
name = "Relax"
blocks = [
  { type = "paragraph", content = "You sink into the couch cushions and stare at the ceiling fan making slow circles. No phone, no journal, no thinking about what any of this means. Just sitting. The house creaks. Somewhere a clock ticks. It's enough." }
]
exit_block = { type = "choices", choices = [
  { text = "Just a few minutes", targetType = "trigger", time_progression_minutes = 15, effects = [{ targetType = "player", trait = "energy", op = "add", value = 8, clamp = true }] },
  { text = "Lose track of time", targetType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "player", trait = "energy", op = "add", value = 12, clamp = true }] },
] }

[canvases.trigger]
location = "loc_living"
is_active = true
is_repeatable = true
max_triggers_per_day = 2
priority = 1

[[canvases]]
id = "bonding_moms_recipe"
name = "Cook Mom's Recipe"
description = "The old recipe card. Mom's handwriting. Making it together."

[[canvases.nodes]]
id = "base"
name = "The Recipe Card"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Madison asks for the recipe card. 'Family tradition!' she says brightly. He hands it to her. You watch your mother's handwriting leave his hands." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "He finds the old recipe card in the drawer. Mom's handwriting, faded but legible. You make it together — measuring flour, arguing about seasoning. The kitchen smells like childhood." },
    { type = "image", props = { file = "activities/bonding_moms_recipe_base.jpg", description = "Cooking together from old recipe card, flour on counter, nostalgic kitchen scene", search_queries = ["cooking together recipe card nostalgic kitchen", "baking together flour counter warm"] } },
    { type = "dialog", content = "She always added too much cinnamon. On purpose, I think.", props = { speaker = "npc", npcId = "npc_ethan" } }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Finish cooking. Eat together.", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] },
  { text = "Ask about the first time she made this.", targetType = "node", nodeId = "bonding_moms_recipe.t2", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 }] } },
  { text = "Stay in this moment a while.", targetType = "node", nodeId = "bonding_moms_recipe.t3", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 55 }] } },
] }

[[canvases.nodes]]
id = "t2"
name = "The Story Behind It"
blocks = [
  { type = "paragraph", content = "He tells you about the Thanksgiving she first made this. Before the divorce. Before you were step-siblings. When you were just two kids who liked the same dessert." },
  { type = "dialog", content = "You stole the last piece. I cried. Mom made another one just for me.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He laughs. You remember it differently but you let him have his version." }
]
exit_block = { type = "location", text = "Save the leftovers", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Belonging"
blocks = [
  { type = "paragraph", content = "You're covered in flour and laughing. He wipes your cheek with his thumb and doesn't move his hand." },
  { type = "paragraph", content = "This isn't desire — it's something older and deeper. The feeling of belonging somewhere. Of being known by someone who remembers the version of you that existed before you learned to hide." },
  { type = "dialog", content = "We should make this more often.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "He means the recipe. He also means this." }
]
exit_block = { type = "location", text = "This is enough", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 15 }]
[[canvases.trigger.schedules]]
start_time = "09:00"
end_time = "12:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "bonding_video_games"
name = "Old Video Games"
description = "Same controllers. Same cartridge. Fourteen again."

[[canvases.nodes]]
id = "base"
name = "Player Two"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "Between rounds, his hand rests on your knee. Player one, player two. The game has changed but neither of you pauses it." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "He digs the old console out of the TV stand. Same controllers, same cartridge. You sit cross-legged on the floor like you're fourteen again, elbowing each other for advantage." },
    { type = "image", props = { file = "activities/bonding_video_games_base.jpg", description = "Two people playing retro video games on floor, cross-legged, nostalgic", search_queries = ["playing retro video games together floor", "nostalgic gaming console living room"] } },
    { type = "dialog", content = "I call player one.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Some arguments never change." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Play a few rounds. Trash-talk like old times.", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] },
  { text = "Call him out for letting you win.", targetType = "node", nodeId = "bonding_video_games.t2", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 }] } },
  { text = "Pause the game. Just talk.", targetType = "node", nodeId = "bonding_video_games.t3", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 55 }] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Fair Play"
blocks = [
  { type = "paragraph", content = "He lets you win. You call him out. He grins — that same grin from when you were kids." },
  { type = "dialog", content = "I have no idea what you're talking about. You're just naturally gifted.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "For a moment there's no wedding, no Madison, no complicated feelings. Just two people who grew up together, still keeping score." }
]
exit_block = { type = "location", text = "Save the game", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Before Everything Changed"
blocks = [
  { type = "paragraph", content = "The game is paused. Controllers on the carpet. He's talking about the summer you both learned to play this — before everything got complicated." },
  { type = "dialog", content = "I miss when things were simple. When we were just... us.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "His voice is soft. You realize this is the version of him that existed before obligation. Before he learned to want things he wasn't supposed to have." }
]
exit_block = { type = "location", text = "Remember this feeling", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_living"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 15 }]
[[canvases.trigger.schedules]]
start_time = "12:00"
end_time = "14:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"

[[canvases]]
id = "bonding_garage_memories"
name = "Garage Memories"
description = "Boxes of old stuff. A childhood neither of you has touched in years."

[[canvases.nodes]]
id = "base"
name = "The Boxes"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "You find a prom photo buried in the boxes. His arm around you, your head on his shoulder." },
    { type = "dialog", content = "We look happy.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "Present tense." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Boxes of old stuff. School projects, faded ribbons, a science fair trophy with both your names on it. You sit on the concrete floor and sort through a childhood neither of you has touched in years." },
    { type = "image", props = { file = "activities/bonding_garage_memories_base.jpg", description = "Sitting on garage floor sorting through old boxes, childhood memorabilia", search_queries = ["sorting old boxes garage floor memories", "childhood memorabilia boxes garage nostalgic"] } },
    { type = "dialog", content = "Oh my god. Your macaroni art phase.", props = { speaker = "npc", npcId = "npc_ethan" } }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Laugh about old school photos. Put the boxes back.", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] },
  { text = "Look at what he kept.", targetType = "node", nodeId = "bonding_garage_memories.t2", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 }] } },
  { text = "Sit with the memories a while.", targetType = "node", nodeId = "bonding_garage_memories.t3", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 55 }] } },
] }

[[canvases.nodes]]
id = "t2"
name = "The Birthday Card"
blocks = [
  { type = "paragraph", content = "He finds the birthday card you made him when you were twelve. Crayon hearts and misspelled words. He reads it out loud and his voice cracks on 'your the best brother ever.'" },
  { type = "dialog", content = "You spelled 'you're' wrong.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "dialog", content = "I was twelve.", props = { speaker = "player" } },
  { type = "dialog", content = "Still wrong.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "But he's smiling. And he puts the card back in the box carefully, like it matters." }
]
exit_block = { type = "location", text = "Keep looking", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Family First"
blocks = [
  { type = "paragraph", content = "Sitting among the boxes, dusty and quiet. The garage smells like old cardboard and motor oil and time." },
  { type = "dialog", content = "We were a family before we were anything else.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "It's the truest thing either of you has said. Some bonds predate desire. This one does. Whatever happens with the wedding, with Madison, with the future — this is the foundation underneath everything." }
]
exit_block = { type = "location", text = "Close the boxes gently", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_garage"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
costs = [{ trait = "energy", value = 10 }]
[[canvases.trigger.schedules]]
start_time = "14:00"
end_time = "17:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "old_photos_complete"
operator = "is_true"

[[canvases]]
id = "bonding_stargazing"
name = "Stargazing"
description = "Blanket on the grass. Stars out. The sky is infinite and the moment is small and perfect."

[[canvases.nodes]]
id = "base"
name = "The Sky"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "madison_arrived", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He whispers so Madison won't hear through the bedroom window. The stars feel like witnesses to something they shouldn't see." },
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Blanket on the grass. Stars out. He points at constellations and gets every name wrong. You correct him. He claims he's been saying that the whole time." },
    { type = "image", props = { file = "activities/bonding_stargazing_base.jpg", description = "Two people lying on blanket stargazing, backyard at night, peaceful", search_queries = ["stargazing blanket backyard night peaceful", "lying on grass looking at stars together"] } },
    { type = "dialog", content = "That one's definitely Orion.", props = { speaker = "npc", npcId = "npc_ethan" } },
    { type = "paragraph", content = "It's not. The sky is infinite and the moment is small and perfect." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Watch the stars in comfortable silence.", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] },
  { text = "Ask what he wanted to be when he grew up.", targetType = "node", nodeId = "bonding_stargazing.t2", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 30 }] } },
  { text = "Just lie here. No words needed.", targetType = "node", nodeId = "bonding_stargazing.t3", conditions = { version = "1.0", items = [{ type = "trait", subject = "npc", npc_id = "npc_ethan", trait_key = "love", operator = "gte", value = 55 }] } },
] }

[[canvases.nodes]]
id = "t2"
name = "Old Dreams"
blocks = [
  { type = "paragraph", content = "He asks what you wanted to be when you were a kid. You tell him. He remembers — he always remembers." },
  { type = "dialog", content = "I wanted to be someone who didn't hurt people.", props = { speaker = "npc", npcId = "npc_ethan" } },
  { type = "paragraph", content = "The quiet after that sentence goes on forever. A shooting star crosses the sky and neither of you makes a wish." }
]
exit_block = { type = "location", text = "Let the silence be", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 5, clamp = true }] } }

[[canvases.nodes]]
id = "t3"
name = "Just Presence"
blocks = [
  { type = "paragraph", content = "No words left. Just two people lying on the grass, shoulders touching, watching the same sky. His hand finds yours. Not desire. Just presence." },
  { type = "paragraph", content = "Just: I'm here. You're here. That's enough tonight." },
  { type = "paragraph", content = "The dew starts to fall. Neither of you moves." }
]
exit_block = { type = "location", text = "Stay until the dew falls", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 3, clamp = true }, { targetType = "npc", npcId = "npc_ethan", trait = "trust", op = "add", value = 6, clamp = true }] } }

[canvases.trigger]
location = "loc_backyard"
npc = "npc_ethan"
is_active = true
is_repeatable = true
max_triggers_per_day = 1
priority = 1
[[canvases.trigger.schedules]]
start_time = "22:00"
end_time = "01:00"

[canvases.trigger.conditions]
version = "1.0"
[[canvases.trigger.conditions.items]]
type = "flag"
subject = "player"
flag_key = "arrival_complete"
operator = "is_true"
```

### 10.4 Phase 4: Story Arc

```toml
# ═══════════════════════════════════════════════════════════════
# PHASE 4: STORY ARC
# ═══════════════════════════════════════════════════════════════
# Source: Book Phase 6 (Story Arc)
# Game: Two Weeks
#
# Contents:
#   - 6 Chapters (Coming Home → The Wedding)
#   - 20 Story Nodes (linked to Phase 2 canvases)
#   - 4 Groups ("Complete N of M" pacing milestones)
#   - 3 Emotion Mappings (love, trust, corruption on npc_ethan)
#   - 25+ Guidance Hints (flag-based, stat-based, gate, general)
#
# Cross-references:
#   - Canvas IDs: Phase 2 (story canvases)
#   - Flag keys: Phase 1 (player.flag_keys)
#   - NPC IDs: Phase 1 (npc_ethan)
#   - Trait names: love, trust, corruption (npc_ethan), boldness (player)
# ═══════════════════════════════════════════════════════════════

[story_arc]
version = "1.0"

# ═══════════════════════════════════════════════════════════════
# CHAPTERS (6)
# ═══════════════════════════════════════════════════════════════
# Moods: hopeful | romantic | tense | passionate | peaceful | neutral

[[story_arc.chapters]]
id = "chapter_coming_home"
name = "Coming Home"
mood = "hopeful"
description = "The house is smaller than you remembered. The feelings are bigger. Days 1-3: denial crumbles under the weight of proximity and memory."
order = 1

[[story_arc.chapters]]
id = "chapter_old_flames"
name = "Old Flames"
mood = "tense"
description = "The tension has a name now. You both know what's happening. Days 4-7: loaded silences, almost-touches, and the first time one of you says it out loud."
order = 2

[[story_arc.chapters]]
id = "chapter_crossing_lines"
name = "Crossing Lines"
mood = "romantic"
description = "Past the point of pretending. Days 7-9: from first kiss to 'what are we doing?' — the line between step-siblings and lovers dissolves."
order = 3

[[story_arc.chapters]]
id = "chapter_breaking_point"
name = "The Breaking Point"
mood = "passionate"
description = "No going back. Days 10-11: the night that changes everything, and the morning after that nearly destroys it."
order = 4

[[story_arc.chapters]]
id = "chapter_borrowed_time"
name = "Borrowed Time"
mood = "tense"
description = "She's coming. The clock is real. Days 11-13: desperate love on a countdown, addiction to something about to be taken away."
order = 5

[[story_arc.chapters]]
id = "chapter_the_wedding"
name = "The Wedding"
mood = "neutral"
description = "The dress is pressed. The vows are written. The question is who he'll be saying them to. Day 14: resolution."
order = 6

# ═══════════════════════════════════════════════════════════════
# STORY NODES (19)
# ═══════════════════════════════════════════════════════════════
# Each node links to a Phase 2 canvas via linked_canvas and
# tracks completion via linked_flag. requires_nodes enforces
# the flag chain order. group assigns nodes to pacing groups.
# requires_group gates nodes behind group completion.

# ─── Chapter 1: Coming Home ──────────────────────────────────

[[story_arc.nodes]]
id = "arrival"
name = "The Return"
chapter = "chapter_coming_home"
linked_canvas = "scene_arrival"
linked_flag = "arrival_complete"
is_milestone = true
npc = "npc_ethan"
journal_entry = "I told myself I could handle this. Then he opened the door, and he looked at me the way he used to, and I remembered why I left."

[[story_arc.nodes]]
id = "welcome_dinner"
name = "Welcome Home"
chapter = "chapter_coming_home"
linked_canvas = "scene_welcome_dinner"
linked_flag = "welcome_dinner_complete"
is_milestone = false
npc = "npc_ethan"
group = "early_bonding"
requires_nodes = ["arrival"]
journal_entry = "He made my favorite. He remembered. After two years, he still remembers how I take my coffee, my favorite meal, the way I like the couch cushions arranged. I don't know what's worse — that he remembers, or that I notice."

[[story_arc.nodes]]
id = "old_photos"
name = "The Photo Album"
chapter = "chapter_coming_home"
linked_canvas = "scene_old_photos"
linked_flag = "old_photos_complete"
is_milestone = true
npc = "npc_ethan"
group = "early_bonding"
requires_nodes = ["welcome_dinner"]
journal_entry = "There's a photo of us at the lake. I'm fourteen, he's sixteen. His arm is around me and I'm looking up at him like he invented sunlight. I still look at him like that. I just got better at hiding it."

[[story_arc.nodes]]
id = "sleepless_night"
name = "3 AM"
chapter = "chapter_coming_home"
linked_canvas = "scene_sleepless_night"
linked_flag = "sleepless_night_complete"
is_milestone = false
npc = "npc_ethan"
group = "early_bonding"
requires_nodes = ["old_photos"]
journal_entry = "The kitchen at three in the morning. Him in boxers, me in a nightgown. We pretended it was about the insomnia. It wasn't about the insomnia."

# ─── Chapter 2: Old Flames ───────────────────────────────────

[[story_arc.nodes]]
id = "madison_calls"
name = "The Phone Call"
chapter = "chapter_old_flames"
linked_canvas = "scene_madison_calls"
linked_flag = "madison_calls_complete"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["sleepless_night"]
requires_group = "early_bonding"
journal_entry = "Madison called. He took it in the other room, but I could hear his voice change — softer, gentler, the voice of a man planning a wedding. I sat on the couch and stared at the engagement photo on the mantle and remembered that none of this is mine to want."

[[story_arc.nodes]]
id = "rainy_day"
name = "Rainy Day"
chapter = "chapter_old_flames"
linked_canvas = "scene_rainy_day"
linked_flag = "rainy_day_complete"
is_milestone = false
npc = "npc_ethan"
requires_nodes = ["madison_calls"]
journal_entry = "The storm kept us inside. No pool, no distractions. Just talking. He told me about proposing to Madison — how he planned it for months. I asked if he was happy. He said 'I'm supposed to be.' That's not an answer."

[[story_arc.nodes]]
id = "the_couch"
name = "The Couch"
chapter = "chapter_old_flames"
linked_canvas = "scene_the_couch"
linked_flag = "the_couch_complete"
is_milestone = true
npc = "npc_ethan"
group = "tension_building"
requires_nodes = ["rainy_day"]
journal_entry = "His hand found mine under the blanket. Or mine found his. I don't remember who moved first. I just know that for ten minutes, with the movie playing and our fingers intertwined, I was exactly where I wanted to be. And exactly where I shouldn't have been."

[[story_arc.nodes]]
id = "confession"
name = "The Confession"
chapter = "chapter_old_flames"
linked_canvas = "scene_confession"
linked_flag = "confession_complete"
is_milestone = true
npc = "npc_ethan"
group = "tension_building"
requires_nodes = ["the_couch"]
journal_entry = "He said it. By the pool, with the sun going down, he looked at me and said 'I never stopped.' Three words that broke everything open. I should have said 'we can't.' I said 'I know. Me neither.'"

[[story_arc.nodes]]
id = "almost_kiss"
name = "Almost"
chapter = "chapter_old_flames"
linked_canvas = "scene_almost_kiss"
linked_flag = "almost_kiss_complete"
is_milestone = false
npc = "npc_ethan"
group = "tension_building"
requires_nodes = ["confession"]
journal_entry = "We were so close I could feel his breath. Then a car horn outside. He stepped back. I stepped back. We stood there in the hallway like two people who almost drove off a cliff and are deciding whether to try again."

# ─── Chapter 3: Crossing Lines ───────────────────────────────

[[story_arc.nodes]]
id = "real_talk"
name = "The Real Talk"
chapter = "chapter_crossing_lines"
linked_canvas = "scene_real_talk"
linked_flag = "real_talk_complete"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["almost_kiss"]
requires_group = "tension_building"
journal_entry = "He cried. Ethan cried. Sitting on my bed, head in his hands, saying 'I don't know who I am anymore.' I held him and thought: this is what it costs. Not the forbidden thrill. Not the stolen touches. This. A good man coming apart because he loves the wrong person."

[[story_arc.nodes]]
id = "first_kiss"
name = "First Kiss"
chapter = "chapter_crossing_lines"
linked_canvas = "scene_first_kiss"
linked_flag = "first_kiss_done"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["real_talk"]
journal_entry = "He kissed me. Or I kissed him. It doesn't matter. What matters is that after years of pretending, of leaving, of building entire lives to avoid this exact moment — his mouth was on mine and nothing else existed. Not Madison. Not the wedding. Not the word 'step-sister.' Just us."

[[story_arc.nodes]]
id = "what_are_we_doing"
name = "What Are We Doing"
chapter = "chapter_crossing_lines"
linked_canvas = "scene_what_are_we_doing"
linked_flag = "what_are_we_doing_done"
is_milestone = false
npc = "npc_ethan"
group = "post_kiss_bonding"
requires_nodes = ["first_kiss"]
journal_entry = "Morning coffee. His hand on mine across the table. 'What are we doing?' he asked. Then he kissed me. Then his hands were under my shirt. Then mine were under his. The coffee went cold. We didn't care. His breath on my neck, my hand around him — clumsy and perfect and years overdue."

[[story_arc.nodes]]
id = "going_further"
name = "Going Further"
chapter = "chapter_crossing_lines"
linked_canvas = "scene_going_further"
linked_flag = "going_further_complete"
is_milestone = false
npc = "npc_ethan"
group = "post_kiss_bonding"
requires_nodes = ["what_are_we_doing"]
journal_entry = "The couch. The same couch where we held hands and pretended it was innocent. Tonight there was nothing innocent about it. His mouth. My mouth. The blanket on the floor. We're past pretending, past holding back. The only line left is the one we haven't crossed yet. And I want to cross it."

# ─── Chapter 4: The Breaking Point ───────────────────────────

[[story_arc.nodes]]
id = "first_night"
name = "First Night"
chapter = "chapter_breaking_point"
linked_canvas = "scene_first_night"
linked_flag = "first_night_complete"
is_milestone = true
npc = "npc_ethan"
group = "post_kiss_bonding"
requires_nodes = ["going_further"]
journal_entry = "He came to my room. My old room, with the posters and the childhood bed. We didn't talk about whether it was right. We didn't talk about the wedding. He closed the door and looked at me and I understood that some things can't be unfelt. Some lines can't be uncrossed. I didn't want to uncross it."

[[story_arc.nodes]]
id = "morning_after"
name = "Morning After"
chapter = "chapter_breaking_point"
linked_canvas = "scene_morning_after"
linked_flag = "morning_after_complete"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["first_night"]
requires_group = "post_kiss_bonding"
journal_entry = "He was gone when I woke up. The sheets were cold. I found him in the kitchen, staring at his coffee like it had betrayed him. 'We shouldn't have,' he said. 'But you did,' I didn't say. 'But you will again,' I hoped."

# ─── Chapter 5: Borrowed Time ────────────────────────────────

[[story_arc.nodes]]
id = "cant_stay_away"
name = "Can't Stay Away"
chapter = "chapter_borrowed_time"
linked_canvas = "scene_cant_stay_away"
linked_flag = "cant_stay_away_complete"
is_milestone = false
npc = "npc_ethan"
requires_nodes = ["morning_after"]
journal_entry = "He came back. He stood in the hallway outside my door at midnight and I could hear him breathing through the wood. Then the knock. Then his face. Then his mouth. He tried to resist. He lasted twenty-three hours. I wasn't counting. I was counting."

[[story_arc.nodes]]
id = "madison_arrives"
name = "Madison Arrives"
chapter = "chapter_borrowed_time"
linked_canvas = "scene_madison_arrives"
linked_flag = "madison_arrived"
is_milestone = true
npc = "npc_ethan"
group = "crisis_navigation"
requires_nodes = ["cant_stay_away"]
journal_entry = "She hugged me. She actually hugged me and said 'I'm so glad you're here for the wedding!' and she meant it. She's lovely. Genuinely lovely. And I am the worst person who has ever lived."

[[story_arc.nodes]]
id = "stolen_moment"
name = "Stolen Moment"
chapter = "chapter_borrowed_time"
linked_canvas = "scene_stolen_moment"
linked_flag = "stolen_moment_complete"
is_milestone = false
npc = "npc_ethan"
group = "crisis_navigation"
requires_nodes = ["madison_arrives"]
journal_entry = "The garage. Dust and old boxes and his hands on me while his fiancee is thirty feet away making table centerpieces. This is what we are now. People who hide in garages. People who steal moments like criminals. I hate it. I'd do it again in a heartbeat."

# ─── Chapter 6: The Wedding ──────────────────────────────────

[[story_arc.nodes]]
id = "night_before"
name = "The Night Before"
chapter = "chapter_the_wedding"
linked_canvas = "scene_night_before_wedding"
linked_flag = "night_before_complete"
is_milestone = true
npc = "npc_ethan"
group = "crisis_navigation"
requires_nodes = ["stolen_moment"]
journal_entry = "Tomorrow he marries someone else. Or he doesn't. He's in my room — our room, this room that was mine and then his and now ours for one more night. 'What do you want?' I asked. 'You,' he said. 'I've only ever wanted you.' Tomorrow will answer whether wanting is enough."

[[story_arc.nodes]]
id = "wedding_morning"
name = "Wedding Morning"
chapter = "chapter_the_wedding"
linked_canvas = "scene_wedding_morning"
linked_flag = "wedding_morning_done"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["night_before"]
requires_group = "crisis_navigation"
journal_entry = "The morning light is different today. Everything is. The dress is hanging in his room. The cars will come at noon. He's downstairs. I'm up here. And between us, fourteen days of everything we were never supposed to feel."

[[story_arc.nodes]]
id = "he_chooses_you"
name = "He Chooses You"
chapter = "chapter_the_wedding"
linked_canvas = "ending_he_chooses_you"
linked_flag = "ending_seen"
is_milestone = true
npc = "npc_ethan"
requires_nodes = ["wedding_morning"]
journal_entry = "He chose me. In front of everyone, he chose me."

# ═══════════════════════════════════════════════════════════════
# GROUPS (4) — "Complete N of M" pacing milestones
# ═══════════════════════════════════════════════════════════════

[[story_arc.groups]]
id = "early_bonding"
name = "Settling In"
description = "The first emotional beats of being home. Experience these before the tension escalates."
required_count = 2

[[story_arc.groups]]
id = "tension_building"
name = "Something Between Us"
description = "The tension has a name. These moments build enough momentum for the crisis to land."
required_count = 2

[[story_arc.groups]]
id = "post_kiss_bonding"
name = "Past Pretending"
description = "Beyond the first kiss. The conversations and choices that make the turning point feel earned."
required_count = 1

[[story_arc.groups]]
id = "crisis_navigation"
name = "Borrowed Time"
description = "The final stretch. Madison is here, the wedding is days away, and every stolen moment costs more."
required_count = 2

# ═══════════════════════════════════════════════════════════════
# EMOTION MAPPINGS
# ═══════════════════════════════════════════════════════════════
# Maps stat ranges to human-readable labels and behavioral
# descriptions. Drives the journal/quest page emotional status.

# ─── Love (Primary NPC Stat — npc_ethan) ────────────────

[story_arc.emotion_mappings.love]
trait_owner = "npc"
default_npc = "npc_ethan"

[[story_arc.emotion_mappings.love.ranges]]
min = 0
max = 20
label = "family"
description = "He's your step-brother. You're here for his wedding. That's the whole story. He makes coffee for one. Keeps a cushion between them on the couch. Hugs are brief, one-armed, with a back-pat."

[[story_arc.emotion_mappings.love.ranges]]
min = 21
max = 40
label = "remembering"
description = "Something is waking up. Old feelings, buried under two years of distance, stretching in the morning light. He remembers how she takes her coffee. Eyes linger a beat too long. 'Do you remember when...' becomes his opening line."

[[story_arc.emotion_mappings.love.ranges]]
min = 41
max = 60
label = "charged"
description = "The air changes when you're in the same room. Both of you feel it. Neither of you says it. He stops pretending not to look. Finds excuses to touch — passing a dish, reaching past her. Drops his voice when they're alone."

[[story_arc.emotion_mappings.love.ranges]]
min = 61
max = 80
label = "falling"
description = "This isn't nostalgia anymore. This is happening. Every touch is a choice, and he keeps choosing. Hand on the small of her back, staying. Starts sentences with 'When the wedding is over—' then stops."

[[story_arc.emotion_mappings.love.ranges]]
min = 81
max = 100
label = "gone"
description = "He's yours. He may not have said it yet, but his hands have, and his eyes have, and the way he says your name has. Pulls her into him without thinking. 'Stay' is a full sentence. His hands shake — not nerves, but restraint finally breaking."

# ─── Corruption (Secondary NPC Stat — npc_ethan) ───────────────────
# How far he's willing to cross the line. Low = loyal to Madison, high = fully committed to the affair.

[story_arc.emotion_mappings.corruption]
trait_owner = "npc"
default_npc = "npc_ethan"

[[story_arc.emotion_mappings.corruption.ranges]]
min = 0
max = 15
label = "loyal"
description = "He's Madison's. The ring on the counter, the wedding binder on the table — these are his reality. He treats you like family. Nothing more. Keeps his distance without effort because the line hasn't been tested yet."

[[story_arc.emotion_mappings.corruption.ranges]]
min = 16
max = 30
label = "tempted"
description = "The first cracks. He lets a touch linger. Catches himself staring and doesn't look away fast enough. 'This doesn't mean anything' — said to himself more than to you. The line is visible now, and he's standing closer to it."

[[story_arc.emotion_mappings.corruption.ranges]]
min = 31
max = 50
label = "crossing"
description = "He knows what he's doing and he's doing it anyway. Finds excuses to be alone with you. Initiates contact he can't explain away. Madison calls and he lets it ring once before answering. The line is behind him now."

[[story_arc.emotion_mappings.corruption.ranges]]
min = 51
max = 70
label = "deep"
description = "The pretense is gone. He's not stumbling into this — he's choosing it. Locks doors. Plans around her schedule. His hands know your body and they go there deliberately. 'I don't care anymore' said against your skin."

[[story_arc.emotion_mappings.corruption.ranges]]
min = 71
max = 100
label = "consumed"
description = "There is no version of this where he goes back. Every boundary is broken, every excuse abandoned. He touches you like ownership, kisses you like confession. The wedding is a formality he's already betrayed in every way that matters."

# ─── Trust (Tertiary NPC Stat — npc_ethan) ───────────────────
# How much he trusts Lily with the truth — his doubts, his feelings, his vulnerability.

[story_arc.emotion_mappings.trust]
trait_owner = "npc"
default_npc = "npc_ethan"

[[story_arc.emotion_mappings.trust.ranges]]
min = 0
max = 20
label = "guarded"
description = "He keeps the real conversations behind a wall of small talk and deflection. Smiles that don't reach his eyes. Changes the subject when anything gets too close to what he's actually feeling."

[[story_arc.emotion_mappings.trust.ranges]]
min = 21
max = 40
label = "opening"
description = "The walls are thinning. He starts sentences he wouldn't have started a week ago. Mentions Madison without the rehearsed enthusiasm. Sits in silence with you and doesn't rush to fill it."

[[story_arc.emotion_mappings.trust.ranges]]
min = 41
max = 60
label = "honest"
description = "He tells you things he hasn't told anyone. About the engagement, about the doubts, about the version of his life he imagined before Madison. Makes eye contact when he says the hard things."

[[story_arc.emotion_mappings.trust.ranges]]
min = 61
max = 80
label = "vulnerable"
description = "No more armor. He cries in front of you. Admits he doesn't know what he's doing. Asks questions he's afraid to hear the answers to. 'What would you do if you were me?' — and he means it."

[[story_arc.emotion_mappings.trust.ranges]]
min = 81
max = 100
label = "complete"
description = "You are the only person in the world who knows the real him. He holds nothing back. Every fear, every want, every ugly truth laid bare. Trust this deep is its own kind of intimacy."

# ═══════════════════════════════════════════════════════════════
# CROSS-STATE REFERENCE (design notes — not parsed by engine)
# ═══════════════════════════════════════════════════════════════
# Key love × corruption combinations that define gameplay states:
#
#   love 0-20  / corr 0-15  → BASELINE: step-siblings at a wedding
#   love 21-40 / corr 0-15  → WARMING: feelings stirring, no action yet
#   love 21-40 / corr 16-30 → TESTING: lingering touches, plausible deniability
#   love 41-60 / corr 0-15  → EMOTIONAL: deep connection, physical restraint
#   love 41-60 / corr 16-30 → ESCALATING: emotional + starting to act on it
#   love 41-60 / corr 31-50 → AFFAIR: actively crossing lines together
#   love 61-80 / corr 0-30  → DEVOTED: loves deeply, hasn't fully acted
#   love 61-80 / corr 31-50 → ENTANGLED: love + physical, hard to undo
#   love 81-100/ corr 0-30  → PURE: deep love, minimal physical betrayal
#   love 81-100/ corr 31-50 → FALLING: love driving the corruption forward
#   love 81-100/ corr 51-70 → COMMITTED: fully in, both heart and body
#   love 81-100/ corr 71+   → CONSUMED: nothing held back, past all return
#
# High love + high corruption is the path to the best ending.
# High corruption + low trust leads to "The Arrangement" (physical, not emotional).

# ═══════════════════════════════════════════════════════════════
# GUIDANCE HINTS
# ═══════════════════════════════════════════════════════════════

[story_arc.hints]
stuck_threshold_minutes = 30
hint_style = "observation"

# ─── Flag-Based Hints (missing story progression flags) ───────

[[story_arc.hints.templates]]
text = "You just got here. Take a breath. Look around the house — it hasn't changed as much as you have."
[story_arc.hints.templates.condition]
missing_flag = "arrival_complete"

[[story_arc.hints.templates]]
text = "Ethan's cooking in the kitchen. He seems like he wants company."
[story_arc.hints.templates.condition]
missing_flag = "welcome_dinner_complete"

[[story_arc.hints.templates]]
text = "There are old photo albums somewhere in this house. Maybe in the garage, or the living room shelves..."
[story_arc.hints.templates.condition]
missing_flag = "old_photos_complete"

[[story_arc.hints.templates]]
text = "You can't sleep. The kitchen light is on downstairs. You're not the only one awake."
[story_arc.hints.templates.condition]
missing_flag = "sleepless_night_complete"

[[story_arc.hints.templates]]
text = "The phone rings at odd hours. Ethan takes the calls in the other room."
[story_arc.hints.templates.condition]
missing_flag = "madison_calls_complete"

[[story_arc.hints.templates]]
text = "The rain is keeping everyone inside. A good day for honest conversation."
[story_arc.hints.templates.condition]
missing_flag = "rainy_day_complete"

[[story_arc.hints.templates]]
text = "Movie night on the couch. The blanket is big enough for two."
[story_arc.hints.templates.condition]
missing_flag = "the_couch_complete"

[[story_arc.hints.templates]]
text = "The pool at sunset. Something in the air tonight feels different — like the truth is closer to the surface."
[story_arc.hints.templates.condition]
missing_flag = "confession_complete"

[[story_arc.hints.templates]]
text = "The hallway between your rooms feels shorter every night."
[story_arc.hints.templates.condition]
missing_flag = "almost_kiss_complete"

[[story_arc.hints.templates]]
text = "He's been carrying something heavy. Maybe tonight he'll let you help hold it."
[story_arc.hints.templates.condition]
missing_flag = "real_talk_complete"

[[story_arc.hints.templates]]
text = "You've both been circling this moment for days. Maybe it's time to stop circling."
[story_arc.hints.templates.condition]
missing_flag = "first_kiss_done"

[[story_arc.hints.templates]]
text = "Morning after the kiss. Coffee in the kitchen. He's waiting for you. So is the conversation."
[story_arc.hints.templates.condition]
missing_flag = "what_are_we_doing_done"

[[story_arc.hints.templates]]
text = "The living room couch. You've been there before — but not like this. Not at night."
[story_arc.hints.templates.condition]
missing_flag = "going_further_complete"

[[story_arc.hints.templates]]
text = "The bedroom door is just a door. What it means is up to you."
[story_arc.hints.templates.condition]
missing_flag = "first_night_complete"

[[story_arc.hints.templates]]
text = "He's in the kitchen. He doesn't look up when you walk in. The silence says everything."
[story_arc.hints.templates.condition]
missing_flag = "morning_after_complete"

[[story_arc.hints.templates]]
text = "Give him time. He'll come back. He always comes back."
[story_arc.hints.templates.condition]
missing_flag = "cant_stay_away_complete"

[[story_arc.hints.templates]]
text = "The wedding is in two days. She'll be here soon."
[story_arc.hints.templates.condition]
missing_flag = "madison_arrived"

[[story_arc.hints.templates]]
text = "The garage. The only room in the house where you're alone anymore."
[story_arc.hints.templates.condition]
missing_flag = "stolen_moment_complete"

[[story_arc.hints.templates]]
text = "Tomorrow changes everything. Tonight is all you have left."
[story_arc.hints.templates.condition]
missing_flag = "night_before_complete"

[[story_arc.hints.templates]]
text = "It's morning. The wedding is today. Go downstairs."
[story_arc.hints.templates.condition]
missing_flag = "wedding_morning_done"

# ─── Stat-Based Hints (stats too low for upcoming gates) ──────

[[story_arc.hints.templates]]
text = "Spend more time with Ethan. Breakfast, lunch, evening — every shared moment matters."
[story_arc.hints.templates.condition]
missing_trait = "love"
gap_gte = 20

[[story_arc.hints.templates]]
text = "You're close. Keep choosing the warmer options when you're together."
[story_arc.hints.templates.condition]
missing_trait = "love"
gap_gte = 10

[[story_arc.hints.templates]]
text = "Some choices require courage. Get ready in the morning, choose the bolder options when they appear."
[story_arc.hints.templates.condition]
missing_trait = "boldness"
gap_gte = 15

[[story_arc.hints.templates]]
text = "He's holding back. Choose the bolder physical options when they appear — he needs to know you want this as much as he does."
[story_arc.hints.templates.condition]
missing_trait = "boldness"
gap_gte = 20

# ─── Gate Flag Hints (missing activity escalation gates) ──────

[[story_arc.hints.templates]]
text = "Something needs to happen first — a moment that changes how you touch each other. Look for it in the story."
[story_arc.hints.templates.condition]
missing_flag = "lingering_touch_unlock"

[[story_arc.hints.templates]]
text = "You haven't crossed that line yet. The story has to take you there before activities can follow."
[story_arc.hints.templates.condition]
missing_flag = "flirt_unlock"

[[story_arc.hints.templates]]
text = "A first kiss can't happen at breakfast. It has to happen in a moment that earns it."
[story_arc.hints.templates.condition]
missing_flag = "kiss_unlock"

[[story_arc.hints.templates]]
text = "Some doors only open once. The story will bring you there when the time is right."
[story_arc.hints.templates.condition]
missing_flag = "intimacy_unlock"

# ─── General Hints ────────────────────────────────────────────

[[story_arc.hints.templates]]
text = "There are more moments to share with Ethan. Try visiting different rooms at different times of day."

[[story_arc.hints.templates]]
text = "Your two weeks are over. The story has reached its end — whatever that end turned out to be."
```

--- END OF TWO WEEKS GAME ---

---


## 11. How TOML Becomes a Game

This section explains — conceptually, without engine code — how a TOML file transforms into a playable HTML5 game.

### Step 1: Parse

The consolidated TOML file (phase 6, or individual phases merged) is loaded using a TOML parser. The raw key-value data is converted into strongly-typed data structures with default values applied for all optional fields.

### Step 2: Normalize

Raw TOML values are coerced to correct types:
- Missing optional strings become `""`
- Missing arrays become `[]`
- Missing tables become `{}`
- IDs are validated as lowercase snake_case
- Nested structures (canvases → triggers → conditions → items) are recursively normalized

### Step 3: Validate

Comprehensive validation checks run:
- **Reference integrity**: All location, NPC, canvas, and node IDs referenced actually exist
- **Flag chain analysis**: Flags required by conditions are actually set somewhere in the game
- **Cycle detection**: No circular references in location `entry_from` graph
- **Schedule gap detection**: Time periods where no canvases are available
- **Reachability analysis**: All canvases can actually be reached by the player
- **Story arc consistency**: Linked canvases are non-repeatable, required nodes exist

### Step 4: Database Objects

The validated template creates database records:
- **Project** — stores metadata, time settings, story arc, sidebar config
- **Player Character** — traits, flags, portrait
- **NPCs** — traits, flags, relationship options, portraits
- **Locations** — hierarchical (parent/child), navigation order, images
- **Canvases** — with triggers, conditions, schedules, costs
- **Nodes** — content blocks converted to internal format, exit blocks preserved
- **Connections** — source-to-target node links within canvases

All slug-based references (human-readable IDs like `"loc_kitchen"`) are resolved to internal UUIDs at this stage.

### Step 5: Twee Generation

The database objects are converted to **Twee format** — a markup language for interactive fiction:
- Each node becomes a **passage** (a screen the player sees)
- Content blocks become formatted text, dialog, images, and conditional sections
- Exit blocks become clickable links/buttons with JavaScript logic
- Conditions become runtime checks against game state variables
- Effects become state mutations (trait changes, flag sets)
- The trigger system becomes location-based canvas selection logic

### Step 6: Compilation

The Twee markup is compiled to a single **HTML5 file** using the **SugarCube** story format:
- All game logic embedded in the HTML
- No server needed — runs entirely in the browser
- Includes: save/load system, sidebar with stats, passage history

### Step 7: Packaging

The compiled HTML is bundled with media assets:
- Location images
- Video clips
- NPC portraits
- Player portrait

The result is a self-contained folder with `index.html` and a `media/` directory.

### What the Player Experiences

1. **Game Start**: The starting canvas (no trigger) plays automatically — typically an intro/arrival scene
2. **Location Map**: After the intro, the player sees available locations as an interactive screen
3. **Time System**: Each action advances the clock (morning → afternoon → evening → night). The game tracks days and weeks.
4. **Canvas Triggering**: When the player visits a location, the engine checks all canvases:
   - Is this canvas active?
   - Does the player meet the trait/flag conditions?
   - Is the current time within the schedule window?
   - Is the associated NPC present?
   - Has the canvas already fired today (if max_triggers_per_day)?
   - Is it repeatable and has it already triggered (if not repeatable)?
   - The highest-priority matching canvas fires
5. **Node Navigation**: Within a canvas, the player reads content and makes choices:
   - Choices may be gated by conditions (greyed out or hidden if requirements not met)
   - Each choice can change traits (add love, spend energy) and set flags
   - Choices advance to other nodes or exit the canvas
6. **Group Variants**: The same node can show different content based on game state:
   - After first kiss: romantic morning greetings
   - After conflict: tense dialog
   - Default: neutral interaction
7. **Progression**: Story canvases advance the narrative (non-repeatable, set progression flags). Activity canvases provide daily interactions with tiered intensity (gated by unlock flags set during story events).
8. **Endings**: When end conditions are met (trait thresholds, specific flags, time limit), ending canvases trigger with different outcomes based on final game state.

### The Flag-Gate System in Practice

```
Story Canvas: "First Kiss" (one-time)
  └── Sets flag: kiss_unlock
        │
        ▼
Activity Canvas: "Morning Coffee" (repeatable)
  ├── Base choice: "Chat over coffee" (always available, +1 love)
  ├── T2 choice: "Flirt a little" (requires love >= 30, +2 love)
  ├── T3 choice: "Kiss good morning" (requires love >= 50 AND kiss_unlock, +3 love)
  └── T4 choice: "Make out" (requires love >= 70 AND groping_unlock, +4 love)
```

This creates a progression loop:
1. Player does activities → builds traits (love, trust)
2. Traits unlock story canvases → story canvases set unlock flags
3. Unlock flags reveal higher-tier activity choices → which build more traits
4. Higher traits unlock the next story canvas → cycle continues

---

## 12. Engine additions — 2026-04-22 (Long Summer PRD)

Four additive features shipped alongside The Long Summer redesign. All are backward-compatible — games that don't use them render identically to before.

### 12.1 `trait_words` sidebar type

Band-descriptive sidebar text that updates as a trait value crosses configured bands. Surfaces the "words not numbers" rule — author-driven prose instead of a numeric bar.

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "player"          # "player" or "npc"
trait = "awareness"
# npc_id = "npc_frank"          # required when trait_owner = "npc"

[[sidebar_items.bands]]
min = 0
max = 9
text = "You keep your eyes down."

[[sidebar_items.bands]]
min = 10
max = 24
text = "Sometimes you notice someone looking."

[[sidebar_items.bands]]
min = 25
max = 49
text = "You catch men watching you more often now."

[[sidebar_items.bands]]
min = 50
max = 100
text = "You know who's watching. You know why."
```

First matching band wins. Trait value outside all bands renders nothing (silent empty). Bands that overlap are tolerated but not recommended — author responsibility.

### 12.2 Generic `entry_conditions` on locations

Location `entry_conditions` now applies regardless of whether clothing is enabled. Previously the block was silently skipped when `[settings.clothing].enabled = false`. Use for phase gating (Prologue-only vs Phase-1-only locations), key/flag-gated secret rooms, or any v1.0 condition on location access.

```toml
[[locations]]
id = "loc_phase1_shop"
name = "Shop (Phase 1)"

[locations.entry_conditions]
items = [
  { type = "flag", id = "phase_0_complete", value = true },
]
```

When conditions fail, the location passage renders "You can't go here right now." plus `setup.formatCanvasConditions()` output and a back-link.

### 12.3 Player `trait_decay`

Per-day decay on player traits. Symmetric with the existing NPC `trait_decay`. Applied at end-of-in-game-day inside `window.advanceDay()`; values clamp to 0 (no negatives).

```toml
[player]
id = "player"
name = "Maya"
core_traits = { energy = 100, hygiene = 100, awareness = 0 }

[player.trait_decay]
hygiene = 3           # loses 3 hygiene per in-game day
# 'energy' is per-activity cost via canvas.costs, not a decay candidate
```

Use for slow drift on player stats (hygiene, mood, heat/suspicion) that should erode without per-canvas boilerplate. Does not stack with explicit effects — explicit effects still apply independently.

### 12.4 Rent `eviction_mode` (fail-forward)

The rent system gains a two-value `eviction_mode`:

- `"game_end"` (default) — preserves existing behavior; grace exhaustion ends the game.
- `"flag_set"` — sets a configurable flag on grace exhaustion and continues the game. The flag is auto-registered in `player.flag_keys`, so `conditions.items = [{ type = "flag", id = "rent_evicted" }]` just works on the next canvas.

```toml
[settings.rent]
enabled = true
amount = 150
due_day = "Monday"
collector_npc = "npc_frank"
grace_periods = 2
eviction_mode = "flag_set"
eviction_flag = "rent_evicted"      # optional; defaults to "rent_evicted"
```

When the flag fires, grace counter resets to 0 so the rent cycle continues. Authors gate the darker narrative branch on `$player.flags.rent_evicted` (or whatever `eviction_flag` was configured). Optional soft-eviction text keys in `[settings.rent.text]`:
- `eviction_scene_soft`, `eviction_response_soft`, `eviction_closing_soft` (fall back to the hard-eviction keys, then to the defaults, if unset).

---

*End of Comprehensive System Reference*
