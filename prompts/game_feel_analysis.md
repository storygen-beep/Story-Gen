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
