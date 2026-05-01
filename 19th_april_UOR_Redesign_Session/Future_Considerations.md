# The Long Summer — Future Considerations

*Companion to `Game_Redesign.md`. Captures items NOT locked in the current redesign but worth keeping on the radar for future passes. Avoids losing good ideas while keeping the redesign doc focused on what's locked.*

**Started:** 2026-04-20
**Purpose:** Parking lot for design ideas to revisit when we move to content / mechanics passes.

---

## Status Key

- 🔵 **CONSIDER LATER** — worth designing in a future pass, not now
- 💭 **DISCUSSED** — explored in conversation, deliberately deferred
- 🆕 **NEW IDEA** — fresh proposal, not yet explored in depth
- 🔒 **DEFERRED INDEFINITELY** — interesting but probably not in scope

---

## Section 1 — Items from reference-game audit (2026-04-20)

These came from a fresh audit of Shady Deals / NLP / ZSL after the redesign was sketched. Worth considering but not locked into the current design or Chapter 1/2 sketches.

### 1.1 World REACTIONS to Maya's choices

🔵 **Status:** Worth implementing in content design pass.

The world should ACKNOWLEDGE Maya's changes via gossip, NPC commentary, and ambient reactions — not just internal stat changes.

**Examples for The Long Summer:**
- Diner regulars comment to Marge about Maya
- Cookie mentions outside-shift gossip
- Church couple recognizing her at the diner
- Frank at dinner: *"People've been mentioning you in town."*
- Ryan: *"Some guy at the bar last night was asking about you."*

**Reference game pattern:**
- Shady Deals' in-fiction news forum where the player's crimes appear as headlines
- NLP's sidebar status updates ("You're currently single. Loser." → "You're dating Zack")

**Why it matters:** Without world reactions, corruption feels INTERNAL only. With it, the world becomes a mirror reflecting Maya's changes back at her.

---

### 1.2 Soft failure states (fail forward, not game-over)

🔵 **Status:** High priority for future design. Expanded below with specific systems.

**The principle:** Failures should have TEXTURE without ending the game. Each failure becomes content (a darker scene, a worse interaction, a different consequence) instead of a game-over screen.

**Reference game patterns:**
- Shady Deals: heat blocks districts but doesn't end the game — pay bribes, work it off
- NLP: rent due triggers events (sometimes darker content) but doesn't game-over
- ZSL: energy depletion gates activities, doesn't crash

**Specific systems to consider:**

#### A. Rent system
💭 **Partially locked at $150/week in Chapter sketches.**

Failure state options:
- Can't pay → Frank deferral with permanent trust drop
- Can't pay → Frank's "arrangement" offer surfaces earlier than otherwise
- Repeated failures → Frank's patience exhausts → "kicked out" scene (game continues, housing changes — maybe Ryan's room? sleep at the diner? darker options?)

#### B. Hygiene system
🆕 **Proposed for future design.**

Maya needs to maintain hygiene through regular showering. Decays over days.

States:
- **Clean** (default — standard NPC reactions)
- **Slightly off** (NPCs notice subtly, prose tone shifts)
- **Smell** (NPCs comment openly, tips drop at diner, certain interactions blocked)

Solo activity: **shower** (~15 min, restores hygiene). Required ~3×/week.

Reference: NLP's allure decay (-15/day without shower).

#### C. Energy system
🆕 **Proposed for future design.**

Maya has limited energy per day. Activities cost energy. Sleep restores.

States:
- **Rested** (default)
- **Tired** (some activities harder, lower performance)
- **Exhausted** (can't do certain things, must sleep)

Reference: ZSL's PlayerEnergy stat (100 max, depletes per activity).

#### D. Could be more — other systems to consider
🆕

- **Food / Hunger:** Maya needs to eat. Skipping meals → mood/health drops, energy drops faster.
- **Sleep debt:** Distinct from energy — too few hours per night creates next-day penalties (slower, less perceptive, scenes go worse).
- **Mood:** Emotional state that affects which choices are available + colors prose tone (sad Maya reads different than determined Maya).
- **Cleanliness of clothes:** Distinct from body hygiene — laundry as a maintenance activity.
- **Social capacity:** If Maya overwhelms an NPC with attention, they need recovery time before re-engaging.

**Tuning consideration:** Adding ALL of these = NLP-territory grim. Adding 1-2 = balanced. Adding 0 = thinner game. My lean: rent + hygiene + energy as the core three. Mood as a stretch goal.

---

### 1.3 Sidebar as EVOLVING NARRATIVE TEXT

🔵 **Status:** High-value, low-cost. Worth designing in content pass.

Sidebar shows EVOLVING TEXT, not just stats. Updates as Maya changes.

**Examples:**

Day 1 sidebar:
```
Maya — Saturday, Day 1
Money: $400
Frank's house — newly arrived
Single. Recovering.
```

Day 14 sidebar (mid-Chapter 2):
```
Maya — Friday, Day 14
Money: $235  |  Saving: $85 toward Sept tuition
Working at the diner. Tips when she smiles.
Knows the rhythm now.
```

Day 21 sidebar (end-Chapter 2):
```
Maya — Friday, Day 21
Money: $290  |  Saving: $135
Marge offered more shifts.
You catch men watching you more often now.
```

**Why it matters:** Player reads the sidebar between every scene. Evolving text there does heavy narrative lifting — describes Maya's trajectory without scene effort.

**Reference game pattern:** Shady Deals' dynamic reputation tier name + NLP's sidebar status updates.

---

### 1.4 Time-gated content rotation (day-of-week specific scenes)

🔵 **Status:** Partially implicit in our schedule system. Worth making explicit in content pass.

Same scheduled activity reads differently based on which weekday it fires.

**Examples:**
- **Friday night diner shifts** = different content (busier, more truckers, higher tips, more ambient gazes)
- **Tuesday night diner shifts** = quiet, locals, less variation
- **Saturday Frank** = home all day, hardware store run mornings
- **Sunday Frank** = different rhythm (newspaper porch, Mom's call evening)
- **Wednesday Ryan** = working in the yard alone (sketching-while-watching scene possible)
- **Tuesday Jake** = at college (out of house) vs **Monday Jake** at home

**Reference game pattern:** NLP's day/period gating, Shady Deals' time-of-day specific locations.

---

### 1.5 Visible accumulation moments

🔵 **Status:** Worth designing in content pass.

Specific corruption thresholds trigger one-time micro-moments that MARK Maya's change. Not arc beats — just observations.

**Examples:**
- First time she crosses a corruption threshold: ambient scene where Maya catches her reflection in a window and pauses
- First time she charges a customer "extra for the smile": one-line internal monologue beat
- First smooth lie she tells: moment of noticing how easy it was

**Reference game pattern:** NLP's masturbation widget labels morphing ("Masturbate" → "Play with yourself" → "Fuck yourself") makes change felt without arc beats.

**Why it matters:** Stats rise invisibly. Stat-shifts need to occasionally LAND as moments.

---

## Section 2 — NPC Arousal mechanic

🆕 **NEW IDEA — flagged for future design**

Each NPC has an arousal stat that rises based on Maya's behavior toward them. Tracks the EFFECT Maya is having ON THEM, not just her own state.

### How it would work

- Each NPC (Frank, Ryan, Jake — TBD if applies to others) has private arousal stat (0-100 scale, likely hidden from player)
- Maya's actions tick it up:
  - Walking past in a towel → +arousal
  - Lingering nearby in revealing clothing → +arousal
  - Direct flirtation → +arousal
  - Holding eye contact a beat too long → +arousal
  - Specific tease scenes → larger +arousal
- Arousal **decays over time** (hours within a day? overnight? TBD cadence)
- **High arousal** = NPC more receptive when Maya approaches
- **Very high arousal** = NPC may initiate or behave differently than usual
- **Sustained high arousal** could unlock specific scene variants

### Why this is interesting for the game

- **Maya's role as active agent becomes MECHANICALLY real** — she's not just rolling against static gates; she's WORKING the NPC, reading him, building him up
- Creates **strategic tease patterns** — Maya works him up, then approaches when he's primed
- **Each NPC has a different "tease threshold"** — Frank slow to arouse (disciplined), Ryan faster (peer-male), Jake possibly easiest (but most awkward) — different challenges per NPC
- Adds a layer **above** relationship stats — love/trust/corruption are PERMANENT progression; arousal is TEMPORAL state
- Matches our locked "corruption tracks willingness, not skills" insight — arousal is the moment-to-moment state that LETS willingness translate to action

### Open design questions

- **Visible to player or hidden?** Hidden lean (more like real perception); but soft hints in prose (he glances at her more, his voice is rougher) could telegraph state
- **Decay rate?** Hours within a day? Resets overnight? Weekly cooldown after a peak?
- **Ceiling effect?** Does over-stimulating backfire (he gets defensive, ashamed, angry)?
- **Per-NPC tunability?** Frank's curve different from Ryan's (slower rise, slower decay vs. faster both)?
- **Applies to all NPCs?** Family men only, or also: town regulars, college students, strangers?

### Reference game patterns

- **NLP** has an arousal stat but it's MAYA'S, not per-NPC. Different mechanic.
- Some adult games (specific titles unverified — would need fresh research) have per-NPC arousal that builds through interactions.
- This would be a genuinely innovative addition compared to what we've explored.

### Why it's "future consideration" not "lock now"

- Adds significant mechanical complexity
- Needs careful tuning (could feel gamey if too visible, could feel pointless if too hidden)
- Should be designed AFTER the core corruption + relationship systems are solid
- Best added as a layer on top of working NPCs, not designed in parallel

---

## Section 3 — Canvas structure patterns from explored games (2026-04-21)

Three distinct multi-beat shapes observed in Shady Deals + NLP. Useful reference when rewriting atomic (1-node) canvases into scenes with a middle.

### 3.1 Pattern A — Push-your-luck state loop

🔵 **Status:** Worth using for risk-taking repeatable activities.

**Reference:** Shady Deals — *Complex Burglary*

Single passage. Player stays on it across multiple clicks. State evolves inside the scene:

- Containers / options get consumed as clicked (disappear from the list)
- Loot accumulates visibly (*"You've found Silver Ring!"*)
- A tension header dynamically shifts: *"You think you've alerted someone"* → *"Someone is coming, run!"*
- Bail button always visible, gets more attractive as risk rises

**Candidate in our game:** diner shift Tier 3 ("Lean over the counter"). Instead of one-click-one-outcome, player serves multiple tables in the same passage; awareness meter ticks up one regular at a time; bail at any moment.

---

### 3.2 Pattern B — Inline dialog beat

🔵 **Status:** Already in use — most of our existing canvases are this shape.

**Reference:** NLP — *introCafe*

Single passage. Dialog blocks play in sequence with narrative glue. Inline stat ticks appear mid-passage (*"She's wearing a skimpy uniform — Inhibition"*). Player reads through a mini-scene, then picks a choice at the end.

**Our examples:** `story_arrival.base`, `story_first_dinner`, `story_first_town_walk`. Per-block prose + dialog pattern is exactly this.

---

### 3.3 Pattern C — Ladder of passages

🔵 **Status:** Use for long-arc moments needing breathing room.

**Reference:** NLP — `Cafe` → `cafeJob` → `cafeWorkImproved` → `cafeDishes` (full job shift across 4 sequential passages)

Scene split across 2-4 sequential nodes. Each node is a focused beat with its own prose and single advance button. Chained via `targetType = "node"`.

**Our examples (already shipped):** `story_arrival` (base → tour).

**Candidates to rewrite (1-node → multi-node):**
- `story_first_diner_shift` → 4 nodes: meet Marge / meet Cookie / the rush / closeout
- `story_first_dinner` → 3 nodes: seating / small talk / goodnight
- `story_first_town_walk` → 2 nodes: the walk in / arriving at town

---

### Rule of thumb

- **Pattern A** — when the scene IS the activity and tension = keep going vs. bail
- **Pattern B** — when the scene is about reading an exchange (dialog-heavy)
- **Pattern C** — when the scene is a sequence of moments, each deserving its own click

---

## Change Log

### 2026-04-20 (doc creation)
- Doc created as parking lot for ideas not being locked in current redesign
- Captured 5 items from reference-game audit:
  1. World reactions / NPC gossip
  2. Soft failure states (expanded with rent / hygiene / energy / mood / food / sleep / clothes / social capacity systems)
  3. Sidebar as evolving narrative text
  4. Time-gated content rotation
  5. Visible accumulation moments
- Added NEW idea: per-NPC arousal mechanic — tracks the EFFECT Maya has on each NPC, separate from relationship stats

### 2026-04-21
- Added Section 3: Canvas structure patterns from explored games — three shapes (push-your-luck state loop / inline dialog beat / ladder of passages) with reference examples from Shady Deals and NLP, plus candidates in our TOML for each.

### 2026-04-22
- Added Section 4: Items reserved during the big redesign pass.

---

## Section 4 — Reserved during the 2026-04-22 pass

### 4.1 Diner owner / appraisal sexual dynamic

🔵 **Status:** Reserved. Not in Phase 1. Potential Phase 2+ content or late-Phase-1 expansion.

The diner has a 4-tier shift stance system (Game_Redesign.md Section 8). Tier 3 ("after close") is customer-initiated sex work. **The appraisal layer — where Maya's relationship to the owner shifts based on her tier performance — is deliberately NOT in Phase 1.** Marge remains a simple employer-figure in Phase 1: shift dynamics, some intense shift-floor teasing as ambient, but no sexual or power-inverted dynamic between Maya and Marge.

**What to design if / when we pick this up:**
- Whether the owner is Marge (with a Tier-3 past) or a male owner introduced later (with direct sexual power).
- Appraisal mechanic: as Maya's tier performance rises, the owner changes treatment — better shifts, promoted hours, more trust, and eventually sexual proposition or dynamic.
- Marge-specific version: she once worked Tier 3 herself, years ago. Her reading of Maya is colored by recognition. Not sexual directly, but a mentor dynamic that acknowledges the path.
- Male-owner version: owner only appears after Maya has reached Tier 2. Direct sexual power over shift assignment. Cleaner mechanically, more genre-native.

**Why reserved:** adding this to Phase 1 thickens the diner arc past its current weight. Phase 1 already has three NPC arcs + backbone + Prologue + Ryan's shop. Appraisal is Phase 2+ texture.

---

### 4.2 Shadow layer — criminal undercurrent

🔵 **Status:** Reserved. Not in Phase 1. Add if Phase 2+ pacing needs more external threat.

**The idea:** the town has a methamphetamine underground (or comparable shadow economy). Not drama — just atmosphere. Runs through the road crowd. Touches the equipment economy at the edges (Ryan might sell a truck to someone he suspects is involved; he doesn't ask). Everyone who matters knows without saying.

**What reserving it gives us:**
- Plausible "sketchy buyer" for Ryan's Crack-tier deal without the buyer needing on-the-nose invention.
- Ambient danger for Maya's corruption arc — she's not going dark in a pristine place.
- A specific threat NPC slot (a dealer, a dealer's girlfriend, a cop who knows something) for Phase 2+.
- Plausibility for Diana's strictness — *"in a place with this much underneath, you hold your daughter tight."*

**Why deferred:** user decision 2026-04-22 — keep Phase 1 tonal register clean of active dark plot. Ambient permissive-register tension is enough.

---

### 4.3 Phase 2+ recurring events

🔵 **Status:** Reserved. Not in Phase 1.

Phase 1 has Sunday only as a recurring weekly event (Game_Redesign.md Section 2.10). The following are held for Phase 2+:

- **Friday night football.** High school game, whole town attends. Diner surges after halftime. The post-game bar crowd at the truck stop is the largest of the week.
- **Saturday morning farmer's market.** Mixed crowd on Main Street. Summer foot-traffic peak.
- **First Saturday of the month flea market.** County fairground. All three sub-reputations at once.
- **Seasonal county fair or music night.** Three-day spike that changes the town. Seasonal.

These would layer into the existing Phase 1 schedule without structural surgery — they're content additions, not system additions. Add when Phase 2 widens the scope.

---

### 4.4 The ex from the Prologue — possible Phase 1-late appearance

🔵 **Status:** Reserved with caveat. Currently NOT planned.

The 2026-04-22 decision was: the Prologue ex stays in the Prologue, doesn't return. This stands.

**BUT** — noting as reserved — an alternative treatment where Daniel (or whoever) re-appears briefly late in Phase 1 would thicken the shame thread substantially. He'd be the only person alive who knew her before the revenge act; his presence would force her to measure what she's become against who she was. Would require keeping Prologue character names lockable, not placeholder.

If we ever want this: one beat where he shows up in town (passing through, not plot), one encounter, one choice about whether to talk. Doesn't need an arc.

Not being planned unless specifically picked up later.

---

### 4.5 Diana's Phase 2+ arc

🔵 **Status:** Reserved. Diana is a household anchor in Phase 1, no arc. Her arc opens in Phase 2+.

What Phase 2 Diana might do:
- Notice specifically. The `diana_awareness` accumulator from Phase 1 becomes load-bearing.
- Confront (or not). If she does, shape + timing is a Phase 2+ design question.
- Reveal something about her first husband, or her own history, that recontextualizes her strictness.
- Marriage with Frank strain or crack — Diana's arc is also a Frank-Diana arc from her side.

None of this is designed. Reserving.

---

### 4.6 Peer NPC for Maya

🔵 **Status:** Reserved. World design + world population locked 2026-04-22, but specific peer NPC slot deferred.

The world has three sub-reputation tracks. Maya needs at least one peer NPC who isn't family and isn't a customer — someone her own age who sees her from outside the house. Candidates:
- Another young waitress at the diner (probably older than Maya, been in this town longer, already made the choices Maya is making)
- A college-crowd friend (if college activates as a real track in Phase 2+)
- An old friend from the Prologue world who reaches out digitally (wouldn't appear physically but would be a voice)

Decision at 2026-04-22: design the world first, pick the NPC later. World is now designed. Picking the NPC can happen when she adds clear mechanical value — probably at Phase 2+ when college opens, or mid-Phase-1 if the diner arcs need a witness-of-Maya voice that isn't Marge.

---

### 4.7 Hour-scale per-NPC arousal decay (engineering) — ✅ RESOLVED 2026-04-22

~~Engineering flag — not a content item but a system-build need.~~

**Resolution:** Audit against the engine confirmed native support. Per-NPC arousal is a base trait (default `0`) plus temporary `modifier_effects` offsets with `duration_hours`; the engine auto-expires offsets at the configured hour. No engine work was required — the PRD audit corrected the original assumption. See `template_import.py:322-327` for the schema and `Game_Redesign.md §3.8` for the updated pattern.

---

### 4.8 Dynamic sidebar-text (engineering) — ✅ RESOLVED 2026-04-22

~~Engineering flag.~~

**Resolution:** Shipped as Engine PRD **F1 — `trait_words` sidebar type**. Configure `[[sidebar_items]]` with `type = "trait_words"`, a target trait, and an ordered `bands` array of `{min, max, text}` entries. The widget reads the current trait value on every state refresh and renders the matching band's text. Supports both player traits (`trait_owner = "player"`) and per-NPC traits (`trait_owner = "npc"` + `npc_id`). See `Game_Redesign.md §3.8`.
