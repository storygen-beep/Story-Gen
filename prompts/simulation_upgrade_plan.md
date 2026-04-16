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
