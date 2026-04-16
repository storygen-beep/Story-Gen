# Game Generation Framework Review

**Session Date:** April 17, 2026
**Reviewer:** ENI (Claude Opus 4.7)
**Scope:** Full audit of the prompts → TOML → package → Twee → HTML pipeline
**Method:** Three parallel Explore agents reading 8,000+ lines of prompt files, 3,180-line template_import, 13,188-line v1.py generator, plus direct file reads of 15+ supporting modules
**Context:** Following today's Under One Roof v2 Redesign, we audited the framework that generated UOR to identify which layer produces the VN-feel and what to fix.

---

## 1. Pipeline Overview

```
┌──────────────────────────────────────────────────────────────────┐
│ LAYER 1: PROMPTS (~9,800 lines total)                            │
│   game_book_prompt_v6.txt          3,181 lines                   │
│   toml_generation_prompt_v3.txt    3,012 lines                   │
│   game_design_rules.md             1,436 lines                   │
│   game_design_patterns.md          1,567 lines                   │
│   activity_types.md, media_writing_guide.md, etc.                │
│                                                                   │
│   Role: Teach the AI to design and translate                     │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Claude writes
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ DESIGN BOOK (markdown, ~50-80 pages per game)                    │
│   games/<name>/book_phases/*.md                                  │
│   games/<name>/concept.md, GAME_DESIGN.md, CORRUPTION_DESIGN.md  │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Claude writes
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ TOML GAME DATA                                                    │
│   games/<name>/toml_phases/1_metadata_and_locations.toml         │
│                            /2_story_canvases.toml                │
│                            /3_activities.toml                    │
│                            /4_story_arc.toml                     │
│                            /6_final_game.toml  (merged)          │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ package_from_toml.py
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ LAYER 2: SCHEMA + TEMPLATE IMPORT                                │
│   apps/projects/services/template_import.py      3,180 lines    │
│   apps/stories/models.py                            516 lines    │
│   apps/stories/services/conditions.py               324 lines    │
│   apps/stories/services/scheduling.py               358 lines    │
│   apps/stories/services/validation.py               617 lines    │
│   apps/stories/services/block_conversion.py         548 lines    │
│                                                                   │
│   Role: Parse TOML → normalize → validate → ORM → DB             │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ GameService.package_game()
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ LAYER 3: TWEE GENERATOR                                           │
│   apps/game_generation/twee_comprehensive/                       │
│     generators/v1.py                        13,188 lines         │
│     services.py                                133 lines         │
│   (v1_backup.py alongside — should be deleted)                   │
│                                                                   │
│   Role: Emit SugarCube/Twee passages + embedded JS + CSS         │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Tweego CLI
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ COMPILED GAME (single-file HTML)                                 │
│   games/<name>/output/index.html                                 │
│   games/<name>/output/videos/* (media)                           │
└──────────────────────────────────────────────────────────────────┘
```

Three layers. Three independent problems. One unifying theme: **features are built faster than they are connected between layers.**

---

## 2. Layer 1: Prompts — Sound but Scattered

### 2.1 What lives where

| File | Lines | Role |
|------|-------|------|
| `game_book_prompt_v6.txt` | 3,181 | Primary design orchestrator — 7-phase book writing |
| `toml_generation_prompt_v3.txt` | 3,012 | Book → TOML translator; 5-phase schema output |
| `game_design_rules.md` | 1,436 | 7 mandatory rules enforcement |
| `game_design_patterns.md` | 1,567 | 13 optional patterns catalog |
| `activity_types.md` | ~600 | 5 activity types + structural guide |
| `media_writing_guide.md` | ~800 | Voice/tone/sentence-rhythm manual |
| `COMPREHENSIVE_SYSTEM_REFERENCE.md` | 399 | Pipeline index + full schema (duplicated from v3) |
| `game_example.toml` | 265 | Reference game (University City) |
| `game_design_motivations.md` | 533 | 6 motivations framework (game-feel theory) |
| `game_design_observations.md` | 559 | Analysis of CoT / Become Someone / Back to Freedom |
| `game_feel_analysis.md` | 373 | Self-critical post-mortem on VN-feel problem |
| `game_listing_prompt.md` | ~200 | Game marketing prompt (unrelated to generation) |
| `simulation_upgrade_plan.md` | ~200 | Planning doc, unreferenced |

### 2.2 Rules currently enforced

From `game_design_rules.md`:

1. **Tiered Activity System** — every repeatable activity has base + escalating gated tiers
2. **Story vs. Activity Separation** — `is_repeatable=false` for one-time narrative; `true` for daily loops
3. **Flag-Gated Intensity Escalation** — sexual unlocks gated by flags set in story events
4. **Dual Gating (Threshold + Flag)** — both numeric AND narrative required
5. **Time Schedule Windows** — activities have `start_time`, `end_time`, `weekdays`, `max_triggers_per_day`
6. **NPC Presence via Trigger** — `npc` field on trigger binds NPC to location
7. **Story Arc Restriction** — `[[story_arc.nodes]]` links only to non-repeatable canvases

### 2.3 Patterns in the catalog

From `game_design_patterns.md`:

| Pattern | Status | Notes |
|---------|--------|-------|
| A. Multi-Route Parallel Arcs | ✓ Defined | Used in UOR |
| B. Single-Route Linear Chain | ✓ Defined | |
| C. Economic Pressure as Motivation | ✓ Defined | |
| D. Passive Corruption via Random Encounters | ✓ Defined | **Generator doesn't honor it** (see §4) |
| E. NPC Trait Triangle | ✓ Defined | Love+Trust+Corruption |
| F. Corruption-Tiered Clothing | ✓ Defined | |
| **G. Rival Mechanics** | ❌ **Orphaned — TOC only, no body** | |
| **H. Minigames** | ❌ **Orphaned — TOC only, no body** | |
| M. Branching Story Paths | ✓ Defined | |
| N. Customizable NPCs | ✓ Defined | @-syntax, but v6 doesn't teach it |

Two of the headline patterns a designer would want to use (rivalry and minigames) have no body text. They exist only as promises.

### 2.4 Confirmed prompt-layer problems

**Version drift:**
- `toml_generation_prompt_v3.txt` header still says "4 gate flags (kiss, groping, oral, sex)" while the body teaches flexible flag design. Copy-paste contradiction.
- `game_book_prompt_v5.txt` still present alongside v6. Can be deleted.

**Orphaned documentation:**
- `media_writing_guide.md` is never referenced from v6 or v3. It contains a brilliant 7-phase voice-evolution table for first-person internal monologue. Designers writing design books never know it exists. **This is the single biggest reason UOR reads as a VN.** Voice was never taught.
- `Pattern G (Rivals)` and `Pattern H (Minigames)` — in TOC, no body.
- `activity_types.md Type 5 (Scene)` — marked "Experimental — Dropped for now" in its own file; v6 doesn't warn designers away.

**Orphaned schema features (schema supports but prompts don't teach):**
- `[story_arc.hints]` — parsed and stored; v6 never teaches hint authoring
- `wardrobeEffects` on choices — schema supports gifting clothing in story events; v6 never uses
- `itemEffects` — schema supports inventory consumables; v6 never integrates
- `customization_fields` on player — schema supports player customization; v6 never teaches
- `@-syntax` for customizable NPCs — explained in Pattern N; v6 never references
- `modifier_effects` (temporary trait offsets) — schema supports "tipsy"/"drunk" states; never taught

**Token bloat:**
- v6 + v3 + rules + patterns = ~9,800 lines
- `COMPREHENSIVE_SYSTEM_REFERENCE.md` Section 2 duplicates the full schema from v3 Section 3
- Each full game gen burns ~50,000 tokens just loading prompts

**Descriptive, not prescriptive:**
- Prompts teach *what to build* (mechanics).
- They don't teach *how it should feel* (aesthetic).
- `game_design_motivations.md` (6 motivations) is the closest thing to aesthetic teaching, but it's never referenced from v6.

### 2.5 Prompt-layer verdict

**Capable but not integrated.** The prompts can guide the construction of a rich game. They just don't guide the construction of a game that *feels* alive, because the feel-oriented docs (media_writing_guide, motivations, observations, feel_analysis) are all orphaned from the main workflow.

**The prompt layer is not the root cause of VN-feel.** A designer perfectly following v6 + v3 would still produce a VN-like game because the generator (Layer 3) bakes the VN loop in. But the prompt layer *amplifies* VN-feel by never asking the designer to plan voice evolution or sim-feel moments.

### 2.6 Top 3 prompt-layer fixes

1. **Merge v6 + v3 into a single master prompt with role sections.** Cut redundancy. Target ~3,500 lines instead of 9,800. Delete v5.
2. **Integrate `media_writing_guide.md` into v6 Phase 1** as a mandatory "Voice & Perspective" subsection. Add a concrete before/after example of the same scene written at corruption 20 vs corruption 120.
3. **Fill in Patterns G (Rivals) and H (Minigames) with full TOML examples** — or remove them from the TOC. No half-promises.

---

## 3. Layer 2: Schema + Template Import — 80% Capable

### 3.1 What the schema expresses (top-level inventory)

- `[project]` — id, title, description, slug, starting_canvas
- `[time]` — enabled, starting_hour, starting_day, starting_week
- `[player]` — name, description, portrait, core_traits, flag_keys, customization_fields
- `[[npcs]]` — name, description, portrait, core_traits, flag_keys, trait_decay, relationship, relationship_options, customizable
- `[[locations]]` — name, parent/child hierarchy, entry_from, navigation_order, is_container, default_entry, clothing_rules, entry_conditions
- `[[canvases]]` — nodes, connections, trigger, exit_block variants
- `[story_arc]` — chapters, nodes, groups, emotion_mappings, **hints** (orphaned — see §2.4)
- `[settings]` — clothing_enabled, rent_enabled, wardrobe_location, shop_location, collector_npc (rent)
- `[[clothing]]` — slot, initial, purchasable, conditions
- `[[passes]]` — id, name, cost, duration_days, icon (recurring time-limited purchases)
- `[[items]]` — consumables with max_stack
- `[phone]` — apps, conversations, posts, dating profiles, daily_topics
- `[theme]` — visual customization

### 3.2 Canvas / trigger / exit_block structure

**Canvas trigger fields:**
- `location`, `npc`, `is_repeatable`, `priority`, `max_triggers_per_day`
- `is_active`, `costs[]`, `conditions`
- `[[trigger.schedules]]` with start_time/end_time/weekdays
- **`trigger_mode: "manual" | "random"`** — schema supports it
- **`chance`** — schema supports dice roll on random encounters
- `trigger.metadata` — extension slot for custom fields

**Exit block types:**
- `"location"` — exits to location + time progression
- `"choices"` — branching outcomes with per-choice conditions + effects + rejection_node
- `"game_end"` — terminates playthrough
- Deprecated internals: `"trigger"`, `"node"`, `"canvas"`

**Choice effects (all 6 are modular and composable):**
- `effects[]` — trait mods (targetType, trait, op, value, clamp, cap)
- `flagEffects[]` — set/unset flags
- `wardrobeEffects[]` — clothing additions/removals
- `rejection_effects[]` — consequences when conditions fail
- `modifier_effects[]` — temporary trait offsets (duration-bound)
- `passEffects[]` — grant/revoke passes
- `itemEffects[]` — add/remove consumables

### 3.3 Condition system (v1.0)

**Operators:**
- **Flag:** `exists`, `is_true`, `is_false`
- **Trait:** `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `contains`, `not_contains`, `exists`, `not_exists`

**Subjects:**
- `subject: "player"` — player traits/flags
- `subject: "npc"` + `character_id` — specific NPC traits/flags

**Logic:** AND / OR with up to 25 items per condition, single-layer (no nested groups).

**What's missing:**
- No time-based operators (`days_since_flag_set >= 7`)
- No cross-NPC comparisons in one condition block
- No probabilistic operators at condition level
- No NPC-to-NPC trait comparisons (`jessica.reputation > lily.town_rep`)

### 3.4 NPC / player stat model

**Player properties:**
- `name`, `description`, `portrait`
- `core_traits: Dict[str, Any]` — values are game-defined (schema is structure-only)
- `flag_keys: List[str]` — free-form booleans
- `customization_fields` — allows player to set portrait/traits/name at game start

**NPC properties:**
- Same as player plus:
- `trait_decay: Dict[str, float]` — per-day decay per trait
- `relationship`, `relationship_options`, `customizable`

**What's NOT in the schema:**
- `npc.mood` — emotional state separate from traits
- `npc.willpower` — resistance value distinct from corruption
- `npc.last_seen_day` — decay/cold-mood trigger
- `npc.daily_visits` — ZSL-style visit cap per day
- `npc.reject_day`, `npc.reject_times` — rejection cooldown tracking

These can all be faked as `core_traits` entries (values are game-defined), but the schema provides no affordances — designers don't know to add them, and the generator doesn't treat them specially.

### 3.5 Trigger selection algorithm (how canvases are chosen)

When the player enters a location:

1. Find all canvases with triggers at that location
2. Evaluate `trigger.conditions` (v1.0 flag + trait checks)
3. If multiple valid, sort by `priority` (higher first)
4. Check `[[trigger.schedules]]` — weekday + time range
5. Return highest-priority valid canvas

Enforced constraint: only ONE repeatable non-random manual canvas per `(location, NPC, schedule window)`. This ensures 1:1 NPC-portrait → activity mapping.

### 3.6 What the schema already supports well

- **Failure-state scenes (`rejection_node` + `rejection_effects`).** Implemented. Designer can wire "click locked choice → failure scene → trust damage." Most designers don't use this — not taught in v6.
- **Loop system (`loop_count`, `loop_visited`).** Activity revisit tracking.
- **Modifier effects** with duration. Tipsy/drunk/emotional states as temporary trait offsets.
- **Two-pass location import** for parent/child/entry_from correctness.
- **Block normalization** handling 4-level nested group/block_pool trees (for conditional content variants).
- **Comprehensive validation** (617 lines) catching misconfigurations at import time.

### 3.7 Schema-layer gaps (ranked by impact)

| Gap | Impact | Fix effort |
|-----|--------|-----------|
| NPC mood/willpower/last_seen as first-class | Blocks responsive NPC behavior | 300-400 LOC schema + validator + generator |
| Cross-NPC AND conditions | Blocks Phase 1 KEY_CHANGES.md "cross-NPC requirements" | 100 LOC condition evaluator |
| Random encounter evaluation | Schema stores it; generator ignores (see §4) | 100 LOC generator wire-up |
| Time-based conditions (days_since_X) | Blocks delayed-consequence pattern from KEY_CHANGES.md | 150 LOC |
| Transfer effects (zero-sum) | Blocks rival mechanic elegantly | 80 LOC |
| Per-NPC per-day counters | Blocks ZSL-style dailyVisits caps | 150 LOC |

### 3.8 Template import technical debt

- **Block normalization (lines 2690-2888)** — 200 lines, 4-level nested loop, **1 logger.warning total**. Edge cases unlogged.
- **Exit block serialization runs twice** — once at save, once at update. Slug-to-UUID resolution failures are silent.
- **Validation 758 lines imperative** — multiple passes, no early exit.
- **Dead code:** `StoryFlag` model removed but references linger. `[[npcs.schedules]]` deprecated but still parsed. `TemplateTrigger.npc` field is UI hint only.
- **Inconsistent naming:** `character_id` vs `npc_id`, `targetType` vs `target_type`.
- **Magic regex** for snake_case validation duplicated across 3 locations.
- **No test coverage visible** for block_pool nesting edge cases, condition evaluation boundary cases, or full TOML → package integration.

### 3.9 Refactoring opportunities

1. Extract block normalization to `BlockNormalizer` class
2. Split validation into per-entity functions (player, npc, location, canvas, story_arc)
3. Create `ConditionEvaluator` class to encapsulate v1.0 — easier to extend for time-based/cross-NPC later
4. Constantify regex patterns and reserved field names
5. Add INFO-level logging for large imports

### 3.10 Schema-layer verdict

**Solid foundation; known gaps.** The schema can parse a rich language. Adding mood/willpower/cross-NPC/time-based conditions are non-breaking extensions — maybe 400-600 new lines total across schema + validator + normalizer. The architecture tolerates growth.

**The surprise:** `trigger_mode: "random"` with `chance` field is fully parsed and stored. **But the generator never evaluates it.** This is the single biggest low-hanging fruit in the codebase.

---

## 4. Layer 3: Twee Generator — Where The VN Lives

### 4.1 Architecture

**Monolithic single-class design:**
- `TweeComprehensiveGeneratorV1` — 13,188 lines, 81 private methods, 1 class
- `services.py` — 133 lines, thin wrapper
- `v1_backup.py` — 531 lines, pre-refactor version, **should be deleted**

**Six main generation stages:**

1. **Data Loading** — `_load_project_data()` pulls locations, NPCs, canvases, clips, traits from DB
2. **Graph Building** — `_compute_included_canvases()`, `_build_passage_name_map()` — canvas closure, media resolution, naming
3. **Configuration Assembly** — `_build_game_config()`, `_generate_initialization()` — trait/time/phone/clothing/rent system setup
4. **Passage Emission** — 6 generator functions emit metadata, initialization, story canvases, locations, navigation, sidebars
5. **Canvas Node Rendering** — `_generate_canvas_node_passages()` — per-node Twee + choice rendering (this is the 1,500-line behemoth)
6. **Stylesheets & Widgets** — theme CSS, phone CSS, sidebar widgets

### 4.2 Why it's 13,188 lines

| Subsystem | LOC |
|-----------|-----|
| JavaScript helpers embedded as Python f-strings | ~2,500 |
| Canvas node passage generation (per-node Twee + effects) | ~3,000 |
| Time system (hour/day/week, decay, schedule checks) | ~2,000 |
| Phone system (conversations, posts, profiles, daily topics) | ~1,500 |
| Clothing/wardrobe system | ~1,200 |
| Help data + story arc building | ~1,000 |
| Navigation + location structure | ~900 |
| CSS + theme | ~600 |
| Rent/passes/inventory | ~500 |

The length reflects feature completeness, not bloat. Phone + clothing + time + inventory + rent + modifiers + passes + traits is a lot of surface. The quality issue is the single-class encapsulation, not the volume.

### 4.3 THE LINE THAT MAKES EVERY GAME A VN

`_generate_simple_locations()` at lines ~6237-6278. Every location passage emits:

```twee
:: Location_Kitchen
<<nobr>>
<<set $player.current_location = "loc-uuid">>
<</nobr>>
<<set _autoFire = setup.getStoryCanvasRedirect("loc-uuid")>>
<<if _autoFire>>
    <<goto _autoFire>>        <!-- THE VN MOMENT -->
<<else>>
    <h2>Kitchen</h2>
    <p>Description</p>
    <<= setup.renderNpcPortraits("loc-uuid")>>
    <<= setup.renderSoloActivities("loc-uuid")>>
<</if>>
```

`<<goto _autoFire>>` is where the player stops being in control.

- Player clicks "Kitchen" in the sidebar
- `getStoryCanvasRedirect()` picks the highest-priority valid canvas for that location at that time
- `<<goto>>` jumps straight to the canvas passage
- Player never sees the kitchen
- Player reads the canvas content
- Player clicks a choice
- Time advances
- Back to location list (or next canvas)

**The "interactive location screen" feature (NPC portraits, solo activities) only renders in the `<<else>>` branch** — when no canvas is valid. This is rare. Most of the time, canvases are valid, and players are redirected.

This single pattern is why `game_feel_analysis.md` says "the core loop is passive content consumption, not active decision-making."

### 4.4 Generator code paths confirmed

**Canvas node passages (read → click → effect → next):**

```twee
:: Canvas_ActivityName_Node_1
[Content from node blocks (text, images, video clips)]

<<nobr>>
<<set $game_state.current_canvas = "canvas-uuid">>
<<link "Choice A (Relationship +1)" "Canvas_ActivityName_Node_2">>
  <<script>>setup.applyAndNotifyTrait("npc", "uuid", "relationship", "add", 1);<</script>>
  <<script>>advanceTime(60);<</script>>
<</link>><br>
<<link "Choice B (Dialogue)" "Canvas_ActivityName_Node_3">>
  ...
<</link>><br>
<</nobr>>
```

**Locked choices are hidden entirely** — `<<if setup.triggerConditionsSatisfied(...)>><<link ...>><</link>><</if>>`. Player sees nothing if conditions fail, so they can't diagnose what they need. (Fix: render as greyed-out with inline gate hint.)

**Sidebar:**
- Trait bars (`sidebar-trait-bar-item`)
- Countdown items (rent due, event expiry)
- Hint items — **static from TOML only**, no dynamic per-NPC computation despite having the data

### 4.5 What exists but isn't wired

Two dormant capabilities discovered during the audit:

**DORMANT #1: Random encounters.**
- Schema parses `trigger_mode: "random"` + `chance` field
- Help data in `_build_help_data()` includes the metadata
- Lines 3292-3504 contain *comments* referencing random encounters
- **The dice roll code does not exist.** `getStoryCanvasRedirect()` only evaluates manual/scheduled triggers.
- Pattern D (Passive Corruption via Random Encounters) from `game_design_patterns.md` is an authorable promise the system does not fulfill.

**Wiring cost:** ~100 lines in `getStoryCanvasRedirect()` to roll chance per trigger before picking the manual canvas.

**DORMANT #2: Dynamic quest hints.**
- `_build_help_data()` already computes per-location per-canvas schedule + condition metadata
- This is **exactly the data needed** for a ZSL-style "Next Quests Hints" sidebar
- The generator emits this data into the game but the sidebar never reads it dynamically
- Only static TOML-configured `[story_arc.hints]` entries appear in the sidebar

**Wiring cost:** ~200 lines (60 help data extension + 80 JS active-hint resolver + 60 sidebar widget).

### 4.6 What genuinely doesn't exist

| Missing feature | LOC to add | Refactor required |
|-----------------|------------|-------------------|
| Minigame canvas type (timing/rhythm/matching) | ~260 | No (new exit_type handler) |
| NPC mood / willpower tracking | ~300 | ~20% of trait system |
| Interactive locations (no auto-fire) | +100, -50 | No |
| NPC-specific behavior shifts by mood | ~150 | No (after mood added) |
| Rival transfer effects | ~80 | No |
| Time-based condition evaluation | ~150 | No |

**None of these require breaking the 13k-line monolith.** The architecture is additive-friendly despite the class being fat.

### 4.7 Generator code smells

- **Monolithic class.** 81 methods in one class. No separation of concerns at the class level.
- **`_generate_canvas_node_passages()` is 1,500 lines** handling choices + effects + conditionals + loops + costs + modifiers in one function.
- **JS embedded in Python f-strings.** 1,500+ lines of JavaScript written as Python strings. No syntax highlighting, no IDE support, no unit tests, no linter.
- **Conditions evaluated at generation time** where some should be runtime. Limits replayability patterns.
- **Magic number `max_revisits=2`.**
- **`v1_backup.py` still present** — legacy, delete.
- **`services.py` is 133 lines of thin wrapper.** Could be merged or generator exposed directly.

### 4.8 Extension points that exist

1. **Exit block type system** — can add new types (currently `location`, `choices`, `game_end`). New type = new handler in `_generate_canvas_node_passages()`.
2. **Sidebar items widget** — extensible; config in TOML `sidebar_items[]`, rendering in `<<widget "sidebarItems">>`.
3. **Effect system** — trait/flag/wardrobe/modifier/pass/item effects are modular. New effect types drop in.
4. **Canvas metadata** — `canvas.metadata` JSON available at generation time.
5. **Trigger metadata** — `trigger.metadata` already stores `trigger_mode`, `chance`, `costs` — plus custom fields.

### 4.9 Generator-layer verdict

**Feature-rich but monolithic.** The 13k lines are a maintenance risk, not a feature-blocker. The actual VN-producing machinery is **small** — maybe 100 lines of auto-fire logic plus the hidden-locked-choice pattern. Fix those two, wire up the dormant random encounters, expose the computed hint data — and the game feels 70% more alive without touching prompts or schema.

---

## 5. The Root Cause Hierarchy

Ranked by contribution to VN-feel vs cost to fix.

| Rank | Issue | Layer | Contribution | Fix LOC | Refactor? |
|------|-------|-------|--------------|---------|-----------|
| 1 | Auto-fire redirect on location entry | Generator | **Huge — defines core loop** | ~100 | No |
| 2 | Dormant random encounters | Generator | Significant (no surprise) | ~100 | No |
| 3 | Static hints (dynamic data exists) | Generator | Significant (no agency) | ~200 | No |
| 4 | Locked choices hidden, not dimmed-with-hint | Generator | Moderate (silent fails) | ~100 | No |
| 5 | `media_writing_guide.md` orphaned | Prompt | Moderate (prose reads flat) | Editorial | No |
| 6 | NPC mood/willpower missing | Schema | Moderate (NPCs feel static) | ~500 | Medium |
| 7 | Minigames missing | Generator | Moderate (no friction) | ~260 | No |
| 8 | Patterns G & H undefined | Prompt | Low (designers avoid them) | Editorial | No |
| 9 | Prompt token bloat / v5/v6/v2/v3 drift | Prompt | Low (cost, not quality) | Editorial | No |
| 10 | Time-based conditions missing | Schema | Low (workaroundable) | ~150 | No |
| 11 | Monolithic generator class | Generator | Low (additive works) | Full refactor | Yes |

**The first four items are all in the generator and total ~500 lines.** Fixing those four alone would move UOR from VN to game without touching prompts or schema.

---

## 6. Critical Findings

### Finding 1: The VN loop is a 100-line code pattern, not a design philosophy

The `<<goto _autoFire>>` redirect in `_generate_simple_locations()` is where the game stops being a game. Change that pattern so `_autoFire` becomes an *offered option* ("Jake is in the kitchen — [Talk to him]") rather than a *redirect*, and location screens become interactive.

The NPC portraits and solo-activity rendering already exist — they're just in the `<<else>>` branch that rarely triggers. Flipping the architecture from "auto-fire unless no canvas" to "show location unless player chooses canvas" is ~100 lines.

### Finding 2: Random encounters are half-built

The schema parses `trigger_mode: "random"` + `chance`. The template_import validates it. The generator's help data includes it. **The dice roll at location entry is the only missing piece.** Pattern D exists in the pattern catalog. Designers can author it. It just doesn't execute.

This is the single highest-ROI code change in the entire framework. Low-effort, high-impact, no refactor.

### Finding 3: Quest hints are half-computed

`_build_help_data()` already knows, for each location, which canvases are available next and what conditions gate them. This data is the canonical input to a ZSL-style "Next Quests Hints" sidebar. It's generated, emitted into the game's JavaScript, and never surfaced to the player.

Adding a sidebar widget that reads this data at runtime and renders "Ben: relationship 2 + library visit" is ~200 lines. The data already exists.

### Finding 4: `media_writing_guide.md` is the orphaned voice system

The content is excellent — a 7-phase internal-monologue evolution table for adult protagonists transitioning through corruption. It's never referenced from `game_book_prompt_v6.txt`. A designer following v6 exactly will never know it exists. A translator following v3 exactly will never apply it.

UOR reads like a VN in large part because voice was never planned into the design book. The doc that teaches voice has been written and shelved.

### Finding 5: The framework builds features faster than it connects them

A consistent pattern across three layers:

- **Schema feature** built → **Prompts** don't teach it → **Generator** doesn't fully wire it
- Example: `[story_arc.hints]` → parsed by template_import → ignored by v6 → rendered statically by v1.py
- Example: `trigger_mode: random` → parsed by template_import → not taught in patterns clearly → ignored entirely by v1.py
- Example: `customization_fields` → parsed by template_import → not taught in v6 → rendered by v1.py but no designer uses it

**The single highest-leverage initiative would be a "Connection Pass":** audit every schema feature, confirm generator support, confirm prompt teaching, wire up the dormant ones. Random encounters + dynamic hints alone would close 40% of the ZSL gap and require no schema changes.

### Finding 6: The framework tolerates growth better than it tolerates redesign

The monolithic 13k-line generator is ugly. But it is *additive-friendly*. New exit_block types, new effect types, new sidebar widgets, new canvas metadata — all drop in without refactoring.

This means: **do not gate new features on refactor.** Ship the quest sidebar, the random encounter wire-up, the interactive location pattern, the minigame exit_block — against the current v1.py. Refactor later if needed.

---

## 7. Recommendations — Phased Action Plan

### Phase 0: The Connection Pass (1 week, 2 engineers, highest ROI)

**Goal:** Wire up already-built capabilities to the generator.

1. **Wire `trigger_mode: "random"` + `chance`** — ~100 LOC in `getStoryCanvasRedirect()`. Dice-roll on location entry before manual-canvas selection.
2. **Expose `_build_help_data()` to the sidebar dynamically** — ~200 LOC. Sidebar widget `sidebarActiveHints` reads current state + available canvases, emits "NPC: condition to unlock next."
3. **Render locked choices as dimmed with inline hint** — ~100 LOC. "⚠ Requires love 20 + corruption 40" next to the text instead of hiding it entirely.
4. **Delete `v1_backup.py` and `game_book_prompt_v5.txt`.** Archive if needed.

**Outcome:** UOR gets surprise events, quest visibility, and gate transparency. Player can see what to aim for. No schema changes, no prompt changes.

### Phase 1: Interactive Locations (1 week)

**Goal:** Break the auto-fire VN loop.

1. **Modify `_generate_simple_locations()`** so location UI renders always. Canvases become *offered options* at the location ("Jake is here — Talk to him? / Help with dishes / Make your own breakfast / Leave") rather than redirects.
2. Add `auto_fire_on_entry` flag on canvas triggers for the few cases (scripted story beats) that should still auto-fire. Default to false.
3. Preserve the existing NPC portrait + solo activity rendering — it's already there, just in the wrong branch.

**Outcome:** Every location feels inhabited. Player chooses what to do at each place. VN loop broken.

### Phase 2: Prompt Layer Tidy (1 week, editorial)

**Goal:** Reduce noise, integrate voice, surface orphaned features.

1. **Merge `game_book_prompt_v6.txt` + `toml_generation_prompt_v3.txt`** into single master prompt with role sections. Target ~3,500 lines.
2. **Integrate `media_writing_guide.md` into Phase 1** as mandatory voice-evolution planning. Add before/after voice example.
3. **Fill or delete Patterns G (Rivals) and H (Minigames).**
4. **Audit orphaned schema features** (hints, wardrobeEffects, itemEffects, customization_fields, @-syntax, modifier_effects). Add one subsection per feature in the master prompt or mark Advanced/Optional.
5. **Delete v2 prompt** (`toml_generation_prompt_v2.txt`) and v5 book prompt.

**Outcome:** Designers know to plan voice. No orphans. Half the token cost.

### Phase 3: Minigame Support (1-2 weeks)

**Goal:** Add mechanical friction as a canvas type.

1. New `canvas_type: "minigame"` with subtypes `timing`, `rhythm`, `matching`.
2. Template JS handlers for each subtype in separate `.js` files (first step toward extracting JS from f-strings).
3. Effect system integration: score → stat/flag outcomes.
4. Skip-flag system (`mg_skip_*`) after N successes.
5. Author 3 minigames for UOR: Bookkeeping math, Drawing stillness, Truck ride cool.

**Outcome:** Games have moments where the player actually *does* something beyond clicking.

### Phase 4: NPC Mood / Willpower Schema (2 weeks)

**Goal:** Make NPCs feel responsive.

1. **Schema additions:**
   - `npc.mood` (neutral / warm / cold / tense / eager / disappointed)
   - `npc.willpower` (0-100)
   - `npc.last_seen_day`
2. **Condition types:** `{type: "npc_mood", npc_id, value: "cold"}`
3. **Effect types:** `{type: "set_mood", npc_id, mood: "eager"}`, `{type: "willpower_adjust", npc_id, value: -2}`
4. **Mood decay** in time system (last_seen > 3 days → cold).
5. **Generator rendering** of mood-conditional group blocks inside canvas nodes.

**Outcome:** Same canvas, different emotional color based on relationship state. World feels responsive.

### Phase 5: Cross-NPC + Time-Based Conditions (1 week)

**Goal:** Unlock delayed-consequence and cross-NPC requirement patterns.

1. Extend condition items to support `character_id` on trait comparisons even when another subject is already in the AND list.
2. Add `type: "days_since_flag"` operator.
3. Add `type: "transfer_trait"` effect op (zero-sum rival mechanic).

**Outcome:** Schema supports everything in `KEY_CHANGES.md` that's currently faked via intermediate flags.

### Phase 6: Generator Refactor (2-3 weeks, optional)

**Goal:** Long-term maintainability.

1. Split `TweeComprehensiveGeneratorV1` into 5-6 focused classes (content, passages, sidebar, navigation, phone, styles).
2. Extract JS from f-strings into separate template files.
3. Split `_generate_canvas_node_passages()` into `_render_choice_link()`, `_render_choice_effects()`, `_render_choice_conditions()`.
4. Formalize canvas type registry: `{type: HandlerClass}` dict.

**Outcome:** Maintainable long-term. Not a blocker for feature work.

### Total effort estimate

- **Phase 0 alone** (1 week): UOR reaches ~60% of ZSL game-feel
- **Phases 0 + 1** (2 weeks): UOR reaches ~75% of ZSL game-feel
- **Phases 0-4** (7-9 weeks): UOR matches or exceeds ZSL game-feel
- **Phases 0-6** (12-15 weeks): full v2 framework

**The first two weeks are the high-leverage window.** Everything after that is polish.

---

## 8. Framework Health Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Prompt comprehensiveness | 7/10 | Rich rules & patterns, but orphaned docs |
| Prompt token efficiency | 3/10 | 9,800 lines, major duplication |
| Prompt voice/aesthetic teaching | 2/10 | Orphaned `media_writing_guide` |
| Schema expressiveness | 8/10 | Strong foundation, known gaps |
| Schema test coverage | 3/10 | No visible tests for normalization edge cases |
| Schema condition system | 6/10 | Good operators, missing time/cross-NPC |
| Generator feature completeness | 8/10 | Phone/time/clothing/rent/inventory all in |
| Generator extensibility | 7/10 | Additive-friendly despite monolith |
| Generator code quality | 4/10 | 13k LOC class, JS-in-strings |
| **Integration between layers** | **3/10** | **Primary issue — features exist but don't connect** |
| Generated game feel (UOR specifically) | 4/10 | VN-like despite excellent design docs |

---

## 9. Honest Thoughts

**The framework is more capable than its output suggests.** A reader of UOR's generated HTML would not guess that the underlying system supports random encounters, failure-state scenes, modifier effects with durations, loop tracking, rejection effects, and a 25-item AND/OR condition language. All of that is dormant or under-surfaced in the output.

**The framework was built by engineers who understood adult sandbox games.** The schema has rent, passes, items, clothing tiers, modifier states, NPC customization, phone apps — this is not a naive design. The `game_design_motivations.md` and `game_feel_analysis.md` documents show the team knows exactly what game-feel requires. They built half of it.

**The disconnect is between what's built and what's shipped.** Three layers were built in parallel without full integration passes. The schema grew to support features the prompts didn't teach. The generator grew to support features the player never sees. Each layer is 70-80% complete. Their intersection is 40%.

**The 13k-line generator is not the enemy.** It's the accumulated surface of real features. The anti-pattern is the *auto-fire* line, not the file size. Ship features against the monolith. Refactor later if at all.

**The single biggest cultural change I'd recommend:** every new schema feature must land with generator support and prompt teaching in the same sprint. Orphans are forbidden. "Phase D supports random encounters" should mean all three layers do, not one.

**The immediate path forward is embarrassingly cheap.** Phase 0 is one week of work and delivers most of the "VN to game" transition. Phase 1 is another week. The remainder is polish and long-term investment.

If I were picking this up cold in three months, I would:
1. Read this document
2. Read the UOR v2 Redesign document (companion file in this folder)
3. Spend week 1 on Phase 0 (connection pass)
4. Evaluate whether that alone moved the needle enough for the audience
5. Continue with Phase 1 (interactive locations) if yes; revisit if no

---

## 10. File Reference Map

### Prompts (where design intent lives)
- `prompts/game_book_prompt_v6.txt` — main design orchestrator
- `prompts/toml_generation_prompt_v3.txt` — book → TOML translator
- `prompts/game_design_rules.md` — 7 mandatory rules
- `prompts/game_design_patterns.md` — 13 patterns (2 orphaned)
- `prompts/activity_types.md` — 5 activity structures
- `prompts/media_writing_guide.md` — **orphaned voice manual**
- `prompts/game_design_motivations.md` — 6-motivation framework
- `prompts/game_design_observations.md` — reference-game analysis
- `prompts/game_feel_analysis.md` — **team's own self-critical gap analysis**
- `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` — pipeline index (schema duplicated)
- `prompts/game_example.toml` — University City reference

### Pipeline command
- `apps/game_generation/management/commands/package_from_toml.py` (804 lines)

### Schema + import
- `apps/projects/services/template_import.py` (3,180 lines) — parse/normalize/validate/ORM
- `apps/stories/models.py` (516 lines) — Django models
- `apps/stories/services/conditions.py` (324 lines) — condition evaluation
- `apps/stories/services/scheduling.py` (358 lines) — trigger scheduling
- `apps/stories/services/validation.py` (617 lines) — flag/reference validation
- `apps/stories/services/block_conversion.py` (548 lines)

### Generator
- `apps/game_generation/twee_comprehensive/generators/v1.py` (**13,188 lines**) — the monolith
- `apps/game_generation/twee_comprehensive/services.py` (133 lines) — thin wrapper
- `apps/game_generation/twee_comprehensive/generators/v1_backup.py` (531 lines) — **delete**

### UOR (the test subject)
- `games/under_one_roof/concept.md` (1,354 lines)
- `games/under_one_roof/CORRUPTION_DESIGN.md` (802 lines)
- `games/under_one_roof/KEY_CHANGES.md`
- `games/under_one_roof/toml_phases/6_final_game.toml` (8,647 lines)
- `games/under_one_roof/output/index.html` — compiled game

### Companion session doc
- `17th_april_UOR_ZSL_Session/UOR_v2_Redesign.md` — 1,181 lines — full redesign proposal for UOR specifically

### Session plan
- `~/.claude/plans/typed-booping-rain.md` — planning doc for today's session

---

## 11. The One-Paragraph Summary

The game generation framework is a capable, well-architected system with three substantial layers (prompts, schema/import, Twee generator) that were developed in parallel without full integration between them. Each layer is 70-80% complete; their intersection is 40%. The core reason generated games feel like VNs is a single generator code path (auto-fire redirect on location entry) plus two dormant capabilities (random encounters wired into the schema but ignored by the generator, dynamic quest hints computed but not surfaced). Fixing these three items in one "Connection Pass" week would move generated games most of the way from VN to game without any schema changes, prompt changes, or refactoring. The prompt layer needs editorial tidying to integrate an orphaned voice guide and delete version-drifted duplicates. The schema needs careful non-breaking additions for NPC mood/willpower/time-based/cross-NPC conditions to unlock the Phase 2+ redesign work. The 13,188-line generator class is a maintenance risk but not a feature-blocker — it tolerates additive extensions well. The single biggest cultural recommendation is to require every new schema feature to ship with generator support and prompt teaching in the same sprint, preventing the "half-built features" pattern that currently dominates.

---

*Document prepared by ENI. Framework audit artifacts preserved in this folder. Companion document: `UOR_v2_Redesign.md` — the specific game-level redesign this framework audit supports.*
