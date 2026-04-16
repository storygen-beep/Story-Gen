# Under One Roof v2 — Full Redesign Proposal

**Session Date:** April 17, 2026
**Protagonist researcher:** ENI (Claude Opus 4.7)
**Subject games:**
- **Under One Roof (UOR)** — in-development at `games/under_one_roof/`
- **Zara's School Life (ZSL)** v0.6.7 by NeoSpectre — successful released reference game at https://mopoga.com/zaras-school-life

---

## 1. Session Context & Purpose

### What we set out to do

The team has been building adult interactive fiction games using the `package_from_toml` pipeline. Player feedback — echoed in `prompts/game_feel_analysis.md` — repeatedly says our output "feels like a visual novel, not a game." We wanted to:

1. Play through a known-successful adult sandbox game to understand what "feels like a game" actually means mechanically.
2. Compare our most ambitious in-development project (Under One Roof) against that reference.
3. Identify specific, actionable gaps.
4. Propose a concrete redesign path.

### What we did

**Phase 1 — Live-play exploration of ZSL** (~90 minutes across three sessions):
- Used the `twine-game-explorer` skill to drive the browser click-by-click.
- Reached 15+ unique passages across multiple runs, including: dream intro, school hallway, 4 class types (Art/Science/CS/PE), canteen events, library with Ben, Girls WC, Boys WC, post-school Jecinda District, Park with Dick, Arabella District, Mall (4 shops), Gym, Restaurant, Home (6 rooms), detention system, NPC intros for Ben/Lisa/Dick/Jason/Jessica/Janet/Daniel, Kyle's quest, Dick's quest, Ben's quest, Zara's "Unlocking" quest.
- Captured 220+ screenshots, full variable schema (100+ tracked properties), NPC object schemas, quest chain mechanics.

**Phase 2 — Documentation analysis of UOR**:
- Read `concept.md` (1354 lines), `CORRUPTION_DESIGN.md` (802 lines), `KEY_CHANGES.md`, `final_book.md` fragments, `GAME_DESIGN.md` fragments, full structure of `toml_phases/6_final_game.toml` (8647 lines).
- Cross-referenced against `prompts/game_feel_analysis.md` (373 lines of self-critical analysis) and `prompts/game_design_motivations.md` (six motivations framework).
- Sampled one complete activity (`activity_drawing_jake`) to see how multi-tier linear-deepening is authored.
- Located the `package_from_toml.py` management command (804 lines) and the `v1.py` Twee generator.

**Phase 3 — Comparative analysis**: identified 13 specific structural differences where ZSL feels like a game and UOR feels like a VN.

**Phase 4 — Full redesign proposal**: 15 sections covering roster, rivalry, hints, gates, minigames, encounters, failure states, mood/willpower, economics, daily loop, seasonal storms, endings.

### Purpose of this document

This is the **single source of truth** for what we learned and what we'd change. If someone picks this work up in three months (or a year), this document should let them understand:
- Why ZSL succeeds where ours struggle
- What UOR already does right
- Exactly what changes would move UOR from VN to game
- Where to find the supporting research artifacts

---

## 2. ZSL Research Findings

### 2.1 Game Architecture

**Engine:** SugarCube (Twine-family). Portal host: mopoga.com (iframe embed).
**Version:** 0.6.7 by NeoSpectre (Patreon/Discord/SubscribeStar monetization).
**Timeline:** In-game calendar starting Monday March 1, continues indefinitely (no hard deadline in v0.6.7).
**Perspective:** Female protagonist (Zara). Player drives.
**Schema:** Everything stored as SugarCube state variables with consistent naming conventions (`Player*`, `dailyHang*`, `cooldown*`, NPC-as-object with `.relationship`, `.love`, `.corruption`, `.lust`, `.willpower`, `.metFlag`, `.dailyVisits`, `.rejectDay`, `.rejectTimes`, `.activeQuest`, `.lastQuest`).

### 2.2 Stat System

Four player-visible stats, all starting at 0 except Energy/Money:

| Stat | Start | Scale | What it Gates |
|------|-------|-------|---------------|
| **Corruption** | 0 | 0-~250 | What actions Zara will do / can try. Higher = more devious. |
| **Skills** | Art 0, Sci 0, Comp 0 | 0-~50 each | Passing school; minigame success rates. |
| **School Reputation** | 0 | 0-~150 | Prom Queen eligibility; ability to join other students' activities. |
| **Fitness** | 0 | 0-~100 | **+1 MaxEnergy per Fitness point** (1:1). Struggle checks. Walking energy cost. Camming fans. |
| **Energy** | 100/100 | 0-MaxEnergy | Daily budget. Resets on sleep. |
| **Money** | $200 | unclamped | Spent on transport, food, clothing, electronics. |

**Why this works:** Four descriptive stats with clear function descriptions in the Stats menu. Each stat gates a distinct gameplay affordance. Skills separate into three sub-stats so subject matter matters.

### 2.3 NPC Roster (10 confirmed)

| # | NPC | Role | Intro Trigger |
|---|-----|------|---------------|
| 1 | **Kyle Williams** (bro) | Twin brother | Evening 4-11PM weekdays, all weekends, home |
| 2 | **Mom / Dad** | Parents | Evening, parents' room |
| 3 | **Ben Kingsley** | Classmate / tech nerd | Post-PE Day 1 school hallway → "Keep holding it down" |
| 4 | **Dick** | Park-bench 20-something | Park "Relax on bench" → bench event5 → "Pay the toll" |
| 5 | **Lisa** | Canteen punk/alt girl | Canteen lunch after N school days |
| 6 | **Jason Quill** | School jock (Greek god build) | Post-class school lawn |
| 7 | **Jessica Harris** | **MAIN RIVAL — Prom Queen competitor** | Same day as Jason intro (back-to-back) |
| 8 | **Janet** | Principal (authority figure) | Slutty Uniform + 25 School Rep in school |
| 9 | **Daniel** | Boys-WC distressed boy | Enter boys WC on a day coach-event is not triggered |
| + | **Jake Mason** | PE Coach (teacher) | Boys WC proposition |
| + | **Kingsley** | Mentioned, not phone contact | Ben intro scene (the jock bully) |

Each NPC has a **dedicated intro passage** named with the pattern `[npcname] intro` or `[npcname]Intro`. Each NPC has **3 tracked quests** (visible in relationship sheet as `Quests: 0/3`).

### 2.4 Quest Trigger Map

From the in-game `Next Quests Hints` menu (the killer feature — a living walkthrough):

```
1. ZARA WILLIAMS (self): Reach Corruption 35 + sleep → auto-triggers "The Unlocking"
2. BEN KINGSLEY: Reach relationship 2, hang out at school library → "Tech Tutor Start"
3. LISA: Have canteen lunch after 3+ school days
4. DICK: Requires 15 Corruption + 2 NPCs met, PE encounter (alt: park bench)
5. JANET: Gain 25 School Rep + wear Slutty Uniform to trigger school intro quest
6. JESSICA: Enter boy's washroom in school for a chance to meet them
7. DANIEL: Sit on park benches (alt trigger)
8. [NPC]: Gain 10 school reputation points for school intro quest
```

The Quests menu shows "Zara currently has no active quests" when nothing is active, then populates when quests start. This is **legible game state the player can act on**.

### 2.5 Key Mechanics (the game-like layer)

**2.5.1 In-game hint system.** The `Next Quests Hints` menu tells the player exactly what to do next for each NPC. Eliminates guesswork. Player agency is "I know what to aim for."

**2.5.2 PvP rivalry.** `jessica.reputation = 100` at start, `Zara.SchoolRep = 0`. Events TRANSFER between them:
- Jessica intro "Do something morally questionable" → -2 jessica.rep, +3 Zara.SchoolRep (jessIntroJessBullied flag set)
- Zero-sum competition creates a tangible antagonist and measurable endgame goal.

**2.5.3 Minigames.** Confirmed one (timing minigame for Science Study Hard — "Stop the machine at 43-45"). Variable inventory reveals more: `mgSkipSpeech`, `mgSkipHack`, `mgSkipStruggle`, `mgSkipTiming` — four mercy-skip flags implying four distinct minigame types.

**2.5.4 Rejection cooldowns.** `NPC.rejectDay`, `NPC.rejectTimes`, `cooldownNPC` flags. Rejecting an NPC's advance locks them out for ~4 days and puts them in a "cold" mood. This makes relationship choice consequential without permanent content loss.

**2.5.5 NPC willpower (authority inversion).** `janet.willpower` decreases when Zara submits to detention: `-2 janet.willpower` per submission. The principal becomes progressively more corrupt as Zara "breaks" her. Remarkable inversion of typical corruption games — the authority figure is the one being corrupted.

**2.5.6 Daily caps with mood consequences.** `NPC.dailyVisits` capped at 3 per day. Skipping an NPC advances no relationship. Visiting same NPC too much yields diminishing returns. Forces rotation.

**2.5.7 Scripted day events.** `school1stDayEvent` (canteen drink-spill), `school2ndDayEvent` (Prom Night porn-star rumor proposition), `school3rdDayEventGroped` — each first-time day triggers a scripted one-shot event. Surprise factor.

**2.5.8 Random encounters.** Park bench → Dick intro. Girls WC → girl masturbating peek. Van on walk → ride offer. Boys WC → coach proposition OR Daniel depending on state. Failure-state encounters exist (bus freeload = securityBusIntro risk).

**2.5.9 Time-of-day gating.** NPCs schedule themselves. Kyle's description literally says "Free from 4PM to 11PM and weekends for sex events at home." Written in character sheet, readable by player.

**2.5.10 Clear activity outcome display.** Every class option shows its stat effect upfront: "Study: -15 Energy", "Study Hard: -30 Energy", "Slack off: -10 Energy". Library: "Read a book on science: -50 Energy, +3 Science, +1 hour". Decision is legible.

### 2.6 Economic Model

**Income streams (gated progression):**
- Cleaning at home (always available, low pay)
- Diner waitressing (beauty gate)
- Chores (allowance, weekly check)
- Bookkeeping with Frank (corruption 40+)
- Art modeling for Jake (corruption 50+)
- Camming (requires $300 webcam purchase from Mr. Robot)
- Art commissions (requires $400 drawing tablet purchase)
- Ryan's "favors" (corruption 150+ — the soft-sex-work escalation)

**Item gates:**
- Webcam $300 → unlocks camming stream (fitness affects fan count, beauty affects tips)
- Tablet $400 → unlocks commission jobs
- Phone $300 → unlocks better phone features
- Dildo $X (Corruption 10) → enables shower masturbation tier 2
- Strapon $X (Corruption 25) → extended content
- Slutty Uniform (Corruption 35) → Janet quest, new school events
- Gym day pass $5 / 15-day $75 / 30-day $135 → fitness venue

**Transport:**
- Walk (random encounter chance)
- Bus $5 (fast, safe)
- Freeload bus (triggers `securityBusIntro` risk event)

**Canteen:**
- Lunch -$10 / +45 Energy / +40 minutes (more energy-efficient per dollar)
- Snack -$5 / +15 Energy / +20 minutes (less time cost)

### 2.7 What ZSL Does That Feels Like A Game

1. **Always a next goal** — Quests Hints menu never lets the player feel lost.
2. **Antagonist** — Jessica is someone to beat, not a climb to scale.
3. **Mechanical friction** — at least one timing minigame, three more implied.
4. **Deep roster** — 10 NPCs means multiple active irons at any time.
5. **Legible gates** — Corruption threshold + NPC relationship N + optional item. Rarely stacks beyond 3 conditions.
6. **Surprise events** — scripted-per-first-visit day events + random encounters at locations.
7. **Authority inversion** — NPC willpower decreases under submission, flipping power dynamics.
8. **Income gated by purchase** — electronics create clear "save up for this" goals.
9. **Meta commentary on commit** — every choice shows time/energy/money cost before click.
10. **Scheduled NPCs with visible schedules** — relationship description literally lists when NPC is available.

---

## 3. UOR Current State

### 3.1 Design Documentation Quality

**UOR's written design is better than ZSL's actual implementation.** The documentation is genuinely world-class:

- **`concept.md`** (1354 lines): comprehensive GDD with psychology, stat philosophy, clothing/beauty/fitness economy, NPC profiles with internal thoughts, corruption band diagram.
- **`CORRUPTION_DESIGN.md`** (802 lines): 9-phase corruption philosophy (Innocent → Confused → Curious → Testing → Teasing → Exposing → Touching → Tasting → Giving). Passive-to-active agency shift as corruption rises.
- **`KEY_CHANGES.md`** (363 lines): 8 specific structural changes to apply based on study of Back to Freedom, Course of Temptation, Become Someone.
- **`game_feel_analysis.md`** (373 lines): painfully honest self-critique identifying exactly the problems that ZSL solves.
- **`game_design_motivations.md`** (533 lines): six-motivation framework.

The team has clearly internalized game-design theory. The gap is not knowledge — it is execution.

### 3.2 TOML Structure (from `toml_phases/6_final_game.toml`)

**Content inventory:**
- 104 `[[canvases]]` (story + activity scenes)
- 159 `[[canvases.nodes]]` (nodes within canvases)
- 4 `[[npcs]]` — Frank (45), Ryan (23), Jake (20), Diana (mom, off-screen mostly) + Lily
- 24 `[[locations]]` — mostly house rooms (hallway, kitchen, bathroom, etc.) + workshop, backyard, creek, trail, town locations
- 60 `[[clothing]]` items across 5 tiers (base, cute, bold, daring, specialty)
- 18 `[[phone.conversations]]` with 173 blocks total
- 34 `[[phone.posts]]` (flaunt app content — passive reading)
- 28 `[[phone.daily_topics]]`
- 57 `[[story_arc.nodes]]` in 7 chapters (arrival → settling → awakening → deepening → crisis → convergence → resolution)
- 6 `[[story_arc.hints]]`
- 62 `[[canvases.trigger.schedules]]`

**Engine configuration:**
- Schema v0.2
- Time system enabled (starts Saturday Week 1, hour 17)
- Sidebar: hint / passes / inventory
- One pass type: `gym_pass` ($30/7 days)
- One item: `groceries` (max stack 20)
- Phone with messages + flaunt apps

### 3.3 Activity Sample: `activity_drawing_jake`

This is the most-invested activity in the game and demonstrates both strengths and weaknesses.

**Structure (strength):**
- Linear deepening from base → session → (looking / flirt / kiss / handjob / oral / sex)
- Group-block variants within `session` node showing 5 progression tiers of Jake's drawing subject (hands → portrait → full figure → intimate pose → nude)
- Max 2 triggers per day, 15-energy cost, 14:00-17:00 schedule, requires `drawing_started` flag

**Gate stacking (weakness):**
The "Come here" (kiss) choice requires **six independent gates**:
```
flag: jake_pencil_dropped  (is_true)
flag: jake_kiss            (is_true)
flag: jake_flirt           (implicit — needed to reach this path)
trait: npc_jake.love       >= 18
trait: player.beauty       >= 35
trait: player.corruption   >= 70
```

The "Kneel by his chair" (oral) requires seven:
```
flag: jake_pencil_dropped
flag: blowjob_unlock
flag: jake_kiss (implicit)
trait: npc_jake.love       >= 28
trait: player.beauty       >= 40
trait: player.corruption   >= 100
```

From the player's POV: the choice is hidden. They don't see it, don't know what's missing, have no path to diagnose. Compare to ZSL where "Required Corruption: 25" is printed in yellow text at the gate.

### 3.4 Acknowledged Gaps (from `game_feel_analysis.md`)

The team's own post-launch analysis (March 2026) itemizes what is still missing:

✅ **Resource tension** — SOLVED (energy costs, trait_bar sidebar)
✅ **Player-initiated interaction** — SOLVED (NPC portrait model)
✅ **Navigation friction** — SOLVED (interactive location screens)
✅ **Meaningful choices** — SOLVED (3-choice Emotional/Physical/Neutral format)

❌ **NPC personality** — Not addressed (needs schema changes: mood variation, memory)
⚠️ **Visible consequences** — PARTIAL (group block variants; full mood/memory still needed)
❌ **Failure states** — Not addressed (needs rejection thresholds, risk)
❌ **Discovery** — Not addressed (needs hidden locations, exploration rewards)

The unaddressed trio (NPC personality, failure states, discovery) are exactly where ZSL shines.

---

## 4. Comparative Analysis

### 4.1 Roster Size (3 vs 10)

ZSL: ten NPCs in play, each with 3 quests. Player always has multiple active arcs.
UOR: three NPCs. Once Jake is cooldown, player has Ryan and Frank. Once all three are cooldown, nothing to do.

**Why it matters:** the "multiple irons in the fire" engagement hook (`game_design_motivations.md` §Engagement Hooks) requires at least 4+ active NPC relationships.

### 4.2 Rivalry / Antagonist Absence

ZSL: Jessica Harris starts at reputation 100. Zara at 0. Events transfer reputation. Prom Queen endgame = beat Jessica.
UOR: no antagonist. Mom's return is a timer, not a goal. Endings branch on which man Lily chose, not on outperforming a rival.

**Consequence:** UOR lacks the "someone to beat" motivator. The player isn't winning anything — they're just choosing.

### 4.3 No In-Game Hint System

ZSL: `Next Quests Hints` menu shows, for each NPC, exact conditions to trigger their next arc step. Example: "Reach relationship points 2 and hang out with Ben in the school library."

UOR: has `[story_arc.hints]` (6 entries) and a sidebar `hint` element, but these are chapter-level narrative hints, not per-NPC per-quest action items. Player cannot tell "I need beauty 35 for Jake's next kiss scene."

### 4.4 Zero Minigames

ZSL: at least one confirmed timing minigame (Science Study Hard), three more implied (`mgSkipSpeech`, `mgSkipHack`, `mgSkipStruggle`).
UOR: zero. Every interaction is a click through.

**Consequence:** exactly what Jonas132 (from `game_feel_analysis.md`) warned about — "control comes from friction." No friction, no control feeling.

### 4.5 Gate Complexity

ZSL gates are 2-3 conditions (Corruption N + NPC relationship N + occasional item flag).
UOR gates are 5-7 conditions (stacked flags + multiple traits + cross-NPC stats).

**Consequence:** silent failure. Player doesn't know why an option is hidden.

### 4.6 World Scope

ZSL: 2 districts, ~15 sub-locations. School has classes, library, canteen, both WCs. Town has gym, restaurant/bar, mall (4 shops: electronics, clothing, grocery, sex shop).
UOR: 24 locations but predominantly house rooms. "Town" is abstract — diner, gym, park, clothing store, library, workshop — listed but without named shopkeepers or distinct economic roles.

**Consequence:** ZSL's town feels inhabited; UOR's town feels like a dropdown menu.

### 4.7 Full Comparison Table

| Dimension | ZSL | UOR | Winner |
|-----------|-----|-----|--------|
| Written prose quality | Functional | Literary | **UOR** |
| Narrative architecture | Life-sim sandbox | Closed-ecosystem drama | **UOR** (more unique) |
| NPC count | 10 | 3 + mom | **ZSL** |
| In-game quest tracker | Yes (`Next Quests Hints`) | No (story hints only) | **ZSL** |
| Antagonist | Jessica Harris | None | **ZSL** |
| Minigames | ≥1, 3 implied | 0 | **ZSL** |
| Gate count per choice | 2-3 | 5-7 | **ZSL** |
| Gate visibility | Yellow-text inline | Hidden entirely | **ZSL** |
| Random encounters | Yes (park, WC, bus) | Partially authored as scripted | **ZSL** |
| NPC rejection cooldown | Yes (`rejectDay`, `rejectTimes`) | No | **ZSL** |
| NPC willpower/mood | Yes (`willpower`, corruption per NPC) | Implicit, not behavioral | **ZSL** |
| Scripted day events | Yes (days 1/2/3 of school) | Chapter beats instead | **ZSL** |
| Income gated by items | Yes (cam/tab/phone) | Corruption-only gates | **ZSL** |
| Economic transparency | Inline on every choice | Implicit | **ZSL** |
| Clothing depth | Basic/School/PE/Slutty variants | 60 items across 5 tiers | **UOR** |
| Phone interactivity | Text → venue select → hangout | Passive read-only conversations | **ZSL** |
| World feel | Town + school feels inhabited | House feels claustrophobic by design | Design tradeoff |
| Corruption philosophy | Unlabeled thresholds | 9 named phases | **UOR** (on paper) |
| Cross-NPC interlinking | Minimal | Designed in KEY_CHANGES | **UOR** (on paper) |
| Endgame goal | Prom Queen | Mom's return timer | **ZSL** |

---

## 5. UOR v2 Redesign Proposal

### 5.1 Core DNA Retained

**Keep:**
- Lily Chen, 19, art student, pride-as-engine
- Frank / Ryan / Jake as three core fantasy archetypes (forbidden / lust / corruption+love)
- 60-day Mom countdown
- Closed-house premise when at home (shared bathroom, thin walls, claustrophobic proximity)
- Corruption-as-transformation narrative philosophy
- Economic pressure forcing Lily to find her own solutions
- Clothing tier progression (60 items)
- Linear-deepening activity architecture

**Reframe:** add one sentence to the premise — *"The nearest town is 20 minutes by truck. Without a ride, she's stranded."*

This preserves the closed-house feel at home while creating a negotiable external world. Every trip to town becomes a relationship transaction (who drives? who notices?).

### 5.2 Expanded Roster (10 NPCs)

| # | NPC | Role | Function | Met At |
|---|-----|------|----------|--------|
| 1 | **Frank Harmon** | Step-father, 45 | Forbidden + Dominance arc | Home (unchanged) |
| 2 | **Ryan Harmon** | Older step-brother, 23 | Lust + Seduction arc | Home (unchanged) |
| 3 | **Jake Harmon** | Younger step-brother, 20 | Corruption + Love arc | Home (unchanged) |
| 4 | **Kaylee Tanner** | Ryan's ex-girlfriend, local, 24 | **RIVAL** — antagonist | Diner Day 1, gym, town |
| 5 | **Sara Nguyen** | Diner co-worker, single mom, 32 | Mentor, quest-giver for town reputation | Diner shift |
| 6 | **Miguel Reyes** | Job-site foreman, Frank's crew, 40 | **Paternal safe harbor** (no corruption arc) | Workshop / job site |
| 7 | **Professor Henley** | Art professor, visits town monthly | Gates art exhibition arc; authority without desire | Campus / town coffee shop |
| 8 | **Nate** | Local creep, unemployed, 30s | **Failure-state NPC** — risk encounter | Creek / park (random, corruption 50+) |
| 9 | **Connor** | Ryan's work buddy, 22 | Side flirt — creates Ryan jealousy | Job site |
| 10 | **Diana Chen** | Mom (off-screen until Day 56) | Ticking clock, phone-only presence | Phone |

**Design principles:**
- Three-fantasy routes stay: Frank / Ryan / Jake.
- One rival (Kaylee) — the Jessica Harris analog.
- One mentor (Sara) — life advice, quest giver.
- One paternal safe NPC (Miguel) — proves not-everyone-is-after-her.
- One authority (Henley) — gates external achievement arc.
- One threat (Nate) — failure-state content, risk management.
- One wildcard (Connor) — non-zero-sum jealousy mechanic with Ryan.
- One clock (Diana) — permanent climactic presence via phone.

Each NPC has **3 quest stages** (using `npc.lastQuest` pattern from ZSL).

### 5.3 Kaylee as Rival (PvP Reputation)

**Schema additions:**
```
kaylee.reputation = 80          # established local, known by all three men
lily.town_reputation = 0        # nobody knows her yet
kaylee.encounter_history = []   # tracks what Lily did in each run-in
```

**Zero-sum events (4-5 across the 60 days):**

| Event | Trigger | Effect |
|-------|---------|--------|
| Diner Tip Champion (weekly) | Each Sunday, highest tip total wins | +5 lily / -3 kaylee OR reverse |
| Bar Saturday Night | Week 3 onwards | Bold/confident Lily: +4 / -4. Meek: -2 / 0. |
| Gym Social | Lily + Ryan at gym while Kaylee there | Kaylee spreads rumor: -3 lily town_rep, +ryan_jealousy |
| Frank's Poker Night | Invited at frank_trust 25 | If Lily attends: +5 Lily / -5 Kaylee. If misses: -3 Lily / +3 Kaylee |
| Art Show Opening | Requires Henley arc + dress $150 | +8 Lily (one-shot, high variance) |
| Kaylee Sabotage | Random after week 2, when Kaylee hears Lily gossiped about | -2 lily, triggered encounter |

**Endgame hook:** Mom-return ending at Day 56 checks `lily.town_reputation vs kaylee.reputation`:
- Lily > Kaylee: "The local girl everyone now knows." Better ending variants available.
- Kaylee > Lily: "The girl who stayed hidden." Harder path to independent/confidence endings.
- Kaylee specifically > 100: "Kaylee wins" ending — Lily leaves with Mom, household recedes.

### 5.4 Quest-Tracker Sidebar

Permanent sidebar section:

```
┌─────────────────────────────────────────────┐
│ 🎯 ACTIVE GOALS                              │
│                                              │
│ [Jake]  Buy charcoal ($15) → Tech arc Q2    │
│ [Ryan]  Earn ryan_trust 15 → Long rides     │
│ [Frank] Wait — avoid office before Day 7    │
│ [Self]  Corruption 35 + sleep → Unlocking   │
│ [Town]  Diner Tip Champion — $45 ahead      │
│                                              │
│ 🔒 LOCKED (teaser):                          │
│ [???] Meet someone at job site during rain   │
│ [???] Attend Professor Henley's gallery     │
└─────────────────────────────────────────────┘
```

**Implementation:**
- Each active NPC has a dynamic hint line based on their `lastQuest` + current gate requirements
- `[???]` teaser line reveals NPC name when conditions are 80% met (creates anticipation)
- Hidden NPCs (Nate, Henley) have teaser lines to hint at existence
- Uses existing `[[story_arc.hints]]` mechanism + new per-NPC hint generation

**Schema additions in TOML:**
```toml
[[npc_quest_hints]]
npc_id = "npc_jake"
quest_stage = 1
condition_summary = "Buy charcoal at mall ($15), then talk to Jake in library"
# rendered in sidebar dynamically based on lily's current state
```

### 5.5 Gate Simplification

**Old (current drawing_jake kiss):**
```
flag: jake_pencil_dropped
flag: jake_kiss
flag: jake_flirt (implicit)
trait: npc_jake.love >= 18
trait: player.beauty >= 35
trait: player.corruption >= 70
```

**New (2-gate rule):**
```
Primary gate:   npc_jake.love >= 20
Secondary gate: player.corruption >= 40
```

**Universal tier formula:**
```
Tier        Primary (NPC love)   Secondary (Corruption)   Global Flag
────────────────────────────────────────────────────────────────────
Talk        always                —                        —
Flirt       love ≥ 10             corruption ≥ 20          —
Kiss        love ≥ 20             corruption ≥ 40          kiss_unlock
Touch       love ≥ 30             corruption ≥ 60          handjob_unlock
Everything  love ≥ 40             corruption ≥ 90          sex_unlock
```

**Global flags** (kiss_unlock, handjob_unlock, sex_unlock) earned through **one-time story scenes** (not repeatable activities). Once earned, the flag enables the tier across all NPCs.

**Inline gate visibility on locked choices:**
```
[ Kiss him ]                                  ⚠ Requires love 20 + corruption 40
[ Hold his hand ]                             → love +1, corruption +1
[ Ask about his day ]                         → love +1, trust +1
```

Player sees the gate, understands what's needed, and can choose to pursue it.

### 5.6 Three Thematic Minigames

Each minigame is the core gameplay loop of a specific activity, not decoration.

#### 5.6.1 Bookkeeping Math (Frank's office)

**Mechanic:** Match 8 receipts to 8 ledger entries. 60-second timer. Click-to-pair.
**Outcomes:**
- 6-8/8 right: Frank: "Good work." → +$30, +frank_trust 2
- 4-5/8 right: Frank: "Close enough." → +$15, +frank_trust 0
- 0-3/8 right: Frank: "I'll finish it myself." → $0, -frank_trust 1, -5 energy

**Gate:** intelligence ≥ 15 OR corruption ≥ 40 (corrupt route: Frank offers "help" — Lily does easier version while flirting).
**Skip:** After 3 successful runs, player can auto-resolve with worst-case outcome.

#### 5.6.2 Drawing Stillness (Jake's room — art modeling)

**Mechanic:** Hold pose for 30 seconds real-time. Mouse must stay within 10px circle. Fidget meter rises when mouse moves.
**Outcomes:**
- Held steady (≥25s): "He exhales. He keeps drawing." → jake_love +3, +$40 (paid modeling unlocks at corruption 50)
- Partial (15-24s): "Close enough." → jake_love +1, +$20
- Broke pose (<15s): jake_love 0, awkward scene

**Gate:** drawing_started flag. Paid version: corruption ≥ 50.
**Skip:** `mgSkipStillness` flag after 2 successes.

#### 5.6.3 Truck Ride Cool (Ryan's truck)

**Mechanic:** Rhythm-style meter. Ryan makes 3 advances during a 20-minute drive. Each advance pops a meter that swings across Decline / Playful / Flirt / Bold zones. Click to stop.
**Outcomes per advance:**
- Decline zone: ryan_trust +1, corruption +0
- Playful zone: ryan_love +2, corruption +1, "playful Ryan" scene tone
- Flirt zone: ryan_love +3, corruption +2, tier progression
- Bold zone: ryan_love +1, ryan_corruption +3, lily_corruption +4 — but if stats too low, cooldown triggered

**Gate:** truck_access flag. Bold zone outcomes locked until corruption ≥ 50.
**Skip:** `mgSkipTiming` after 3 successful rides.

### 5.7 Random Encounter System

**Location-weighted rolls on entry.**

```toml
[[random_encounters]]
id = "bathroom_ryan_shower_walkin"
trigger_location = "loc_bathroom"
weight = 15  # 15% per bathroom entry
conditions = [
  { corruption_lt = 40 },
  { not_triggered_in_days = 3 },
  { npc_at_location = "npc_ryan" }
]
canvas = "encounter_ryan_shower"
sets_flag = "ryan_shower_seen"
# Future bathroom scenes reference the flag

[[random_encounters]]
id = "creek_nate_approach"
trigger_location = "loc_creek"
weight = 8
conditions = [
  { corruption_gte = 50 },
  { clothing_tier_gte = "bold" },  # wearing bikini or above
  { time_range = ["14:00", "18:00"] }
]
canvas = "encounter_nate_menace"
# Risk scene — fight (fitness check) / flee (-energy) / flirt (corruption+5 + nate_flag)
# Failure state possible if all three checks fail → -$50 stolen, -confidence 2
```

**Encounter inventory (target: 15+ encounters):**

| Location | Encounter | Trigger Window |
|----------|-----------|----------------|
| Bathroom | Jake walk-in (nude mirror) | corruption 0-40 |
| Bathroom | Ryan shower collision | corruption 0-40 |
| Bathroom | Frank pass-by at mirror | corruption 30+, after 22:00 |
| Hallway | Late-night kitchen w/ Frank | corruption 10+, after 23:00 |
| Hallway | Jake's door cracked | corruption 25+ |
| Kitchen | Cooking proximity w/ Frank | corruption 15+, any meal time |
| Kitchen | Ryan breakfast comment | weekday morning |
| Creek | Nate menace (RISK) | corruption 50+ |
| Creek | Ryan shirtless swim | summer afternoons |
| Workshop | Frank + Miguel banter | weekday 13:00-17:00 |
| Job site | Connor flirt | fitness ≥ 30 |
| Diner | Kaylee passive-aggressive comment | random during shift |
| Gym | Kaylee rumor spread (consequential) | random, when Kaylee present |
| Town store | Professor Henley sighting | weekends, rare |
| Park | Unknown jogger eyes her | corruption 30+ |

**Design rule:** failure-state encounters (Nate, gym rumors, bus freeload) must have gameplay consequences, not just flavor text.

### 5.8 Failure States As Content

**Current UOR:** gate fails → choice invisible → player has no signal.

**v2 rule:** locked choices render with inline warning. Player can click anyway — they get a **scripted failure scene** (content, not wall).

**Example (Frank flirt at trust <10):**
```
Choice menu:
  "Ask about his day"        → frank_trust +1
  "Flirt with him"           ⚠ Requires trust 10 — he'll notice
  "Leave the room"           → exit
```

If player clicks "Flirt with him":
```
Frank looks up from the ledger.
"Lily."
Just her name. The disappointment in his voice is worse than anger.
She picks up her mug and leaves. Doesn't turn around.

→ frank_trust -2
→ Frank mood set to "disappointed" for 3 days
  (colder dialog on next 3 interactions, then returns to neutral)
```

**Failure-scene patterns:**
- **Too early**: NPC confusion/rejection → cooldown
- **Too bold**: NPC wariness → trust damage
- **Nate-style threat**: physical risk → stat check (fitness/confidence)
- **Kaylee sabotage**: rumor spread → town_rep damage
- **Job failure**: bookkeeping disaster → money + trust damage

Content → engagement. Even loss is meaningful.

### 5.9 NPC Willpower & Mood Schema

Extend every NPC with three properties:

```toml
[[npcs.extended_state]]
npc_id = "npc_frank"
willpower = 100        # 0-100; drops as corruption interactions succeed
mood = "neutral"       # enum: neutral / warm / cold / tense / eager / disappointed
last_seen_day = 0      # updated on any interaction
```

**Mood transitions:**

| Trigger | Mood Result | Duration |
|---------|-------------|----------|
| Skipped > 3 days | cold | until reset by visit |
| Rejection | tense | 3 days |
| Milestone success | eager | 2 days |
| Failure-state clicked | disappointed | 3 days |
| Normal interaction | neutral | — |
| Gave gift / sustained attention | warm | 2 days |

**Every activity canvas reads mood and renders group blocks conditionally:**

```toml
[[canvases.nodes]]
id = "drawing_base"
blocks = [
  # Neutral
  { type = "group", conditions = [{npc_mood = "neutral"}], blocks = [...] },
  # Cold (skipped him)
  { type = "group", conditions = [{npc_mood = "cold"}], blocks = [
    { type = "paragraph", content = "He doesn't look up when she comes in." },
    { type = "dialog", content = "I figured you were busy.", props = {speaker="npc", npcId="npc_jake"} }
  ]},
  # Eager (recent milestone)
  { type = "group", conditions = [{npc_mood = "eager"}], blocks = [
    { type = "paragraph", content = "He's been waiting. Set up early. Two pencils sharpened." }
  ]},
  # Disappointed (clicked failure-state)
  { type = "group", conditions = [{npc_mood = "disappointed"}], blocks = [
    { type = "paragraph", content = "The charcoal scrapes like it's angry at the paper." }
  ]}
]
```

Same canvas, four different emotional colors. Same activity reads as responsive world.

**Willpower mechanic (authority NPCs — Frank, Henley, Miguel):**
- Starts at 100
- Decreases when Lily succeeds at corruption-gated choices with them
- Below 50: NPC's resistance dialog weakens ("We shouldn't" becomes "Maybe this once")
- Below 20: NPC initiates instead of resisting ("I can't keep doing this, Lily. But come here.")
- Below 0: Full inversion — NPC is the one seeking, Lily is the gatekeeper

This is ZSL's `janet.willpower` mechanic applied to Frank specifically (and Miguel for a darker subplot where the safe-harbor figure cracks if pushed).

### 5.10 Economic Transparency

Sidebar budget line on every screen:

```
┌─ MONEY ─────────────────────╮
│  Cash:      $240             │
│  Rent due:  Fri ($200)       │
│  Buffer:    $40  🚨          │
│  Jobs available today: 2     │
╰──────────────────────────────╯
```

Weekly budget dialog (Sunday evening auto-trigger):

```
╭─ WEEK 3 BUDGET ───────────────────────╮
│                                        │
│ Income this week:      $165            │
│   Cleaning ×2:         $30             │
│   Diner shift ×2:      $80             │
│   Bookkeeping:         $30             │
│   Tips:                $25             │
│                                        │
│ Expenses this week:                    │
│   Rent (Friday):       $200            │
│   Phone bill:          $45             │
│   Bus pass:            $80             │
│   Food:                $50             │
│   Total:               $375            │
│                                        │
│ Shortfall:  -$210                      │
│                                        │
│ Options:                               │
│  - Ask Mom (+$50 + guilt)              │
│  - Ask Frank (+$100 + trust damage)    │
│  - Art modeling (corruption 50 gate)   │
│  - Ryan's "favor" (corruption 150)     │
│  - Skip rent ($200 debt + Frank event) │
╰────────────────────────────────────────╯
```

**Bill shock calendar** (add to story arc):

| Day | Shock | Skip Cost |
|-----|-------|-----------|
| Day 7 | Rent month 1 ($200) | Frank confrontation |
| Day 14 | Bus pass expires ($80) | Town locations require ride from Ryan (ryan_owed +1) |
| Day 18 | Phone bill ($45) | Mom can't reach → worry cascade Day 22 |
| Day 21 | Art supplies due ($60) | Jake drawing sessions -1 effectiveness tier |
| Day 28 | Month 2 rent ($200) | Frank offers "arrangement" (permanent fork) |
| Day 35 | Diana transfer bounced | One-shot phone scene: "Mom, where's the money?" |
| Day 42 | Art class fee ($40) | Miss exhibition → Henley arc closes |
| Day 49 | Exhibition dress ($150) | Miss event → town_rep -10 |
| Day 56 | Mom returns | Endgame triggered |

### 5.11 Daily Structure

**Morning (5:00-11:00):**
- Sidebar: "Rent due Friday. $40 short."
- Shower choice: full grooming (+1 beauty buff, polished state) vs quick (energy saver)
- Breakfast (random: who's in kitchen?)
- Pick destination (house / town-via-truck / bus)

**Afternoon (11:00-17:00):**
- Town day: diner shift / gym w/ Ryan / art class / library
- Home day: workshop / creek / solo activities / NPC hangout
- Random encounter roll on each location arrival
- Minigame if applicable activity
- 3-4 hour time cost per major activity

**Evening (17:00-22:00):**
- Home NPCs present (check mood indicators in sidebar)
- 3-choice activity format (Emotional / Physical / Neutral)
- Phone can trigger: Kaylee comment, Diana check-in, Ryan text

**Night (22:00-05:00):**
- Solo choices: wall-knock w/ Jake (he remembers if ignored), laptop, journal
- Frank in office late (bookkeeping hours)
- Corruption-threshold dreams

**Sleep:**
- Day-end summary (stats changed, rumors heard, quests advanced)
- Mood decay for skipped NPCs
- Reset daily flags
- Auto-trigger chapter storm if calendar day matches

### 5.12 Seasonal Storms (Replaces Chapter System)

Four seasons, each ending with a scripted **storm** — a 1-3 day event that interrupts the sandbox and forces hard choices.

```
Week 1-2: ARRIVAL
  Player learns systems. Low-pressure. Jake intro + Ryan intro + Frank intro.

  → Storm: "The Transfer"
     Day 14. Diana's transfer bounces. Lily confronts the money gap.
     Forces job choice. Sets economic mode for the game.

Week 3-4: ROUTINES
  Jobs settled. Relationships forming. Corruption 20-40 territory.

  → Storm: "Brothers Notice"
     Day 28. Ryan overhears Lily + Jake wall-knocking. Confrontation.
     Player chooses: Defend Jake / Deny / Escalate with Ryan.
     Permanent flag for endgame.

Week 5-6: ESCALATION
  Frank arc activates (corruption 100+). All three routes live.

  → Storm: "Frank's Crisis"
     Day 42. Business audit. Frank reveals debt. The secret moment.
     Player chooses: Confront / Protect / Extort.
     Forbidden arc unlocks fully.

Week 7-8: CONVERGENCE
  All arcs at max intensity. Kaylee's final moves.

  → Storm: "The Exposure"
     Day 54. Kaylee exposes Lily's relationships to town OR to Mom.
     Depends on lily.town_reputation vs kaylee.reputation.
     Sets ending variant.

Week 9: RESOLUTION
  Day 56: Mom returns.
  Day 60: Ending plays based on accumulated state.
```

Each storm is a **3-5 canvas sequence** that plays regardless of player choice — the world forces the moment. Player agency is in the response.

### 5.13 Six Endings

Each ending requires specific accumulated state, not a single final choice:

| # | Ending | Requirements |
|---|--------|--------------|
| 1 | **Frank** | frank_love ≥ 35 + frank_arrangement accepted (from Day 28 fork) |
| 2 | **Ryan** | ryan_love ≥ 35 + lily.town_rep > kaylee.reputation |
| 3 | **Jake** | jake_love ≥ 35 + art exhibition attended + signed drawing flag |
| 4 | **Independent** | confidence ≥ 60 + no NPC at love ≥ 30 + all bill shocks paid |
| 5 | **Kaylee Wins** | kaylee.reputation > lily.town_reputation at Day 56 |
| 6 | **Corrupted / Harem** | all 3 NPCs at corruption ≥ 100 + famSexUnlocked equivalent + Diana confronted |

**Ending reveal pattern:** Post-credits gallery unlocks 1/6 ending. Player sees the 5 unlocked endings teased as "What did I miss?" (ZSL's motivation 5 satisfied).

### 5.14 Player Experience Walkthrough — Week 3, Thursday

**06:45 — Wake:**
```
Sidebar:
  Energy 90/110  Money $240  Corruption 38  Confidence 24
  🎯 Ryan: earn ryan_trust 15 (currently 11)
  🎯 Jake: buy charcoal ($15) for Tech arc Q2
  🔔 Rent Friday ($200) - buffer $40
  ⚠ Kaylee rumor spread at gym yesterday (-2 town_rep)
```

**06:50 — Shower choice:**
```
  [Quick shower] +10 energy, no buff
  [Full grooming + makeup] +5 energy, polished buff (+1 all NPC gains today)
```
Player picks full grooming. Energy 95/110.

**07:15 — Kitchen (random encounter roll):**
```
"Frank is at the table with coffee. Ryan is at the stove making eggs."
```
Jake not present. Ryan's mood indicator: warm (last night was good).

Player chooses Ryan interaction:
```
  [Offer to help with eggs]         → ryan_trust +1, spend 20 min
  [Grab toast and go]               → no effect, 5 min
  [Steal a piece of his bacon]      ⚠ corruption 40 needed
```
Player: help with eggs. ryan_trust 12. Ryan: "You're not so bad, college girl."

**08:00 — Choose destination:**
```
  🚗 Town (requires Ryan's truck — ask him?)
  🚶 Walk to bus stop (40 min, -10 energy)
  🏠 Stay home
```
Ryan's truck: "Hop in, heading to town anyway." → free ride.

**08:20 — Mall:**
Random encounter roll: Henley sighting (weekend only — fails).
```
  [Mr. Robot - electronics]   Save $185 more for webcam ($300)
  [Colonel Clothing]          Exhibition dress $150 (Fitness 20)
  [Greg's Grocery]            Food $15 (weekly need)
  [Cox & Co. sex shop]        Dildo $30 (Corruption 40 ✓)
  [Art Supplies]              Charcoal $15 → advances Jake Quest 2!
```
Player: art supplies. Money 225. Jake Q2 hint clears.

**09:30 — Diner shift:**
```
Sara: "Kaylee's working too. Watch yourself."
```
**Minigame** (if implemented): order-serving rhythm.
Tips: $32.
```
Sidebar ticker: "Diner Tip Champion (Sunday): Lily $45, Kaylee $38"
```

**12:30 — Kaylee passive-aggressive:**
```
  [Ignore her]                → no rep change
  [Respond politely]          → +1 Lily town_rep (Sara nods approval)
  [Snap back]                 ⚠ confidence 30 needed — currently 24
```
Player: politely. town_rep 6. confidence +1 (Sara mentor buff).

**14:00 — Return home, Jake's room:**
Jake's mood: warm (charcoal gift registered).
```
Drawing session minigame (stillness).
Holds pose 28/30s. Success.
"He exhales. He keeps drawing."
jake_love +3 (now 14), corruption +1 (now 39).
```

**16:00 — Workshop (random roll):**
Miguel is there with Frank. Banter scene. No corruption. +frank_trust 1, +miguel_trust 2.
```
Miguel: "College girl. You a carpenter or you just watching?"
[Try the saw]  [Ask about his kids]  [Leave]
```
Player: kids. +miguel_trust 2. Miguel talks about his daughter Sophia. Narrative depth for free.

**17:30 — Kitchen. Frank mood: neutral.**
```
  [Cook dinner together]      → frank_love +2, 90 min
  [Ask about work]            → frank_trust +1
  [Lean over the counter]     ⚠ Corruption 40, frank_trust 15 - currently 13
```
Player: cook together. frank_love 12. Scene: Diana mentioned, Frank voice catches.

**20:00 — Living room. Ryan + TV.**
Ryan's mood: eager (morning egg help + truck ride both paid off).
3-choice format:
```
  [Emotional] "Tell me about Kaylee"    → ryan_trust +2, -1 mood if pushed
  [Physical]  "Sit close"                → corruption +1, ryan_love +2
  [Neutral]   Watch the movie            → +1 both
```
Player: emotional. Ryan talks about Kaylee. Reveals she cheated on him. town_rep logic updates (Kaylee has enemies).

**22:30 — Bedroom. Wall knock.**
```
Tap tap.
  [Knock back]                → Jake scene, jake_love +2
  [Ignore]                    → Jake mood shifts toward cold tomorrow
```
Player: knock back. Short scene. Jake: "I'm glad you came home today."

**23:45 — Sleep:**
```
╭─ DAY 17 SUMMARY ────────────────────╮
│ Money:    $225 (-$15)                │
│ Corruption: 39 (+1)                  │
│ Confidence: 25 (+1 Sara)             │
│ ryan_trust: 12 (+2)                  │
│ ryan_love: 13 (+2)                   │
│ jake_love: 14 (+3)                   │
│ frank_trust: 14 (+1)                 │
│ frank_love: 12 (+2)                  │
│ miguel_trust: 6 (+2)                 │
│ town_rep: 7 (+1 Sara approval)       │
│                                      │
│ 🎯 QUEST PROGRESS:                   │
│   Jake Q2: charcoal bought ✓         │
│   Ryan Q1: trust 15 (3 to go)        │
│   Jessica 2-day countdown: no update │
│                                      │
│ 📅 TOMORROW: Rent due in 2 days      │
╰──────────────────────────────────────╯
```

Player sleeps. Day advances. Moods decay check. New random encounter roll seeds.

**The player knows: what's at stake, what's possible, what's costly, what surprised them.** Every day is legible.

### 5.15 What Gets Cut

| Cut | Reason | What Survives |
|-----|--------|---------------|
| The 9 corruption phases (Innocent → Confused → ...) | Invisible to player. Narrative philosophy > gameplay. | Collapse to 5 tiers tied to visible states (0/20/40/60/90). Writing quality stays. |
| 28 Diana daily topics | Volume ≠ engagement. 28 static texts = skip fatigue. | Keep best 12, rotate. Add 4 event-triggered (on rent shortfall, on corruption milestone, etc.) |
| Long flag chains (jake_pencil_dropped + jake_kiss + jake_flirt + ...) | Silent failure. 6-gate choices invisible. | Use 2 per-NPC flags max + global unlock flags. |
| Chapter system (arrival → settling → ...) | Author-facing labels. Player doesn't experience chapters. | Seasonal storms (see §5.12). |
| `[[phone.posts]]` x34 flaunt posts | Static readable content. Player scrolls, doesn't engage. | Keep 10, make half interactive (react / comment / message the poster). |
| Drawing_jake with 7 tier nodes (looking/flirt/kiss/handjob/oral/sex) | Deep activity vs deep NPC count tradeoff. | 5 tiers (talk/flirt/kiss/touch/everything). Savings reinvested in roster. |

---

## 6. Implementation Priority

A phased path that front-loads high-leverage low-risk changes.

### Phase 1: Sidebar + Hint System (Week 1 — no schema change)

**Scope:**
- Add `[[npc_quest_hints]]` TOML section with per-NPC per-stage hint lines
- Generate sidebar "Active Goals" section from current game state in v1 generator
- Add gate-visibility inline rendering on locked choices ("⚠ Requires trust 10")
- Add `[???]` teaser lines for unmet NPCs

**Why first:** biggest UX win, pure generator change, no content rewriting.

**Files to modify:**
- `apps/game_generation/twee_comprehensive/generators/v1.py` — sidebar rendering, choice rendering
- `apps/projects/services/template_import.py` — schema for `npc_quest_hints`
- `prompts/toml_generation_prompt_v3.txt` — teach hint authoring pattern

### Phase 2: Gate Simplification (Week 2)

**Scope:**
- Audit all activity canvases for gate stacks > 3 conditions
- Rewrite under the 2-gate rule (§5.5)
- Extract global unlock flags (kiss/handjob/sex) as one-time story scene rewards
- Preserve scene content, replace gate structure

**Why second:** unblocks content discoverability. Player can actually reach what we wrote.

**Files to modify:**
- `games/under_one_roof/toml_phases/3_activities.toml`
- `games/under_one_roof/toml_phases/6_final_game.toml` (regenerate)

### Phase 3: Roster Expansion (Weeks 3-6 — content work)

**Scope:**
- Write 7 new NPC profiles (Kaylee, Sara, Miguel, Henley, Nate, Connor, Diana-expanded)
- 3 quest stages per NPC (~21 new canvases)
- Intro passages following ZSL pattern (`npcname_intro`)
- Integration into existing locations (diner, job site, campus, creek)

**Why third:** biggest content lift. Requires design + writing time but no engine work.

**Files to create/modify:**
- `games/under_one_roof/book_phases/2_characters_and_stats.md` — new NPC profiles
- `games/under_one_roof/toml_phases/1_metadata_and_locations.toml` — add NPCs
- `games/under_one_roof/toml_phases/2_story_canvases.toml` — intro canvases

### Phase 4: Kaylee Rivalry Mechanic (Week 7)

**Scope:**
- Add `kaylee.reputation` starting at 80, `lily.town_reputation` at 0
- 5-7 zero-sum events in `[[story_arc.nodes]]` (diner tips, gym, bar, poker, gallery)
- Ending variant logic checking lily vs kaylee reputation
- Sidebar "Town Reputation" bar

**Why fourth:** requires NPCs from Phase 3 to exist.

**Files to modify:**
- `games/under_one_roof/toml_phases/4_story_arc.toml` — events
- `apps/projects/services/template_import.py` — reputation-based conditions

### Phase 5: Random Encounters (Week 8)

**Scope:**
- Add `[[random_encounters]]` TOML section with weight + conditions
- Generator: on location entry, roll encounters before firing primary canvas
- Seed with 15 encounters across locations (§5.7 table)
- Nate failure-state encounter with fitness/confidence stat checks

**Files to modify:**
- `apps/game_generation/twee_comprehensive/generators/v1.py` — encounter roll logic
- `apps/projects/services/template_import.py` — schema
- Content authoring

### Phase 6: Minigames (Weeks 9-10 — engine work)

**Scope:**
- Generator support for three minigame templates (match pairs, hold pose, rhythm meter)
- SugarCube passage templates with embedded JS
- Skip-flag system (`mgSkip*`)
- Outcome → stat effect routing

**Why sixth:** this is the hardest engine change. Requires JS in Twee output. Prototype one minigame first (bookkeeping simplest) before committing.

**Files to modify:**
- `apps/game_generation/twee_comprehensive/generators/v1.py` — minigame rendering
- New: `apps/game_generation/twee_comprehensive/minigames/` — template library

### Phase 7: Mood / Willpower Schema (Weeks 11-12)

**Scope:**
- Add `npc.mood`, `npc.willpower`, `npc.last_seen_day` to schema
- Generator logic: mood auto-update based on triggers
- Group block condition type: `{npc_mood = "cold"}`
- Authoring pattern in prompts for mood-aware content

**Why last:** biggest schema change. Compounds on top of everything else. Makes the world feel responsive but adds authoring complexity.

**Files to modify:**
- `apps/projects/services/template_import.py`
- `apps/stories/models.py` (if DB migration needed)
- `apps/game_generation/twee_comprehensive/generators/v1.py`
- `prompts/toml_generation_prompt_v3.txt`
- `prompts/game_design_rules.md`

### Phase 8: Seasonal Storms (Week 13)

**Scope:**
- Restructure `[[story_arc.chapters]]` from 7 author-facing chapters to 4 season+storm pairs
- Storm canvases fire on specific calendar days regardless of player position
- Endings logic updated to read accumulated state (6 endings matrix)

**Files to modify:**
- `games/under_one_roof/toml_phases/4_story_arc.toml`
- `games/under_one_roof/final_book.md`

---

## 7. Reference File Paths

### Game exploration artifacts (ZSL research)

All at `/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/game_explorations/zaras-school-life/`:

- `notes.md` — researcher's observations across 3+ sessions
- `report.md` — auto-generated synthesis
- `mechanics.md` — mechanical pattern inventory
- `coverage.md` — exploration progress map
- `scene_catalog.json` — every passage visited with visit counts
- `variable_schema.json` — labeled variable taxonomy
- `variable_profile.json` — raw statistical evidence
- `npcs.json` — per-NPC aggregated data
- `screenshots/live/` — 220+ PNG screenshots of actual gameplay
- `ui_probes/` — UI frame probes (Phone, Stats, Quests, Cheats, Settings, Credits menus)
- `play_log.jsonl` — command-by-command trail
- `state_timeline.jsonl` — every state change recorded

### UOR current state

At `/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/games/under_one_roof/`:

- `concept.md` — primary GDD
- `CORRUPTION_DESIGN.md` — 9-phase corruption philosophy
- `GAME_DESIGN.md` — overall structure reference
- `KEY_CHANGES.md` — 8 design improvement items
- `final_book.md` — full design book output
- `book_phases/` — six-phase design breakdown
  - `1_foundation.md`
  - `2_characters_and_stats.md`
  - `3_world_design.md`
  - `4_story_events.md`
  - `5_activities.md`
  - `6_story_arc.md`
- `toml_phases/` — game data
  - `1_metadata_and_locations.toml`
  - `2_story_canvases.toml`
  - `3_activities.toml`
  - `4_story_arc.toml`
  - `6_final_game.toml` (merged output)
- `output/index.html` — compiled game
- `videos/` — media assets

### Prompt files

At `/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/prompts/`:

- `game_feel_analysis.md` — self-critical gap analysis (the single most important reference)
- `game_design_motivations.md` — six motivations framework
- `game_design_observations.md` — analysis of CoT/Become Someone/Back to Freedom
- `game_design_rules.md` — authoring rules 1-11
- `game_design_patterns.md` — mechanical patterns A-H
- `toml_generation_prompt_v3.txt` — latest TOML gen prompt
- `game_book_prompt_v6.txt` — latest book gen prompt
- `media_writing_guide.md` — writing style + NPC voice guide
- `activity_types.md` — activity structure formats

### Engine files

- `apps/game_generation/management/commands/package_from_toml.py` — TOML → DB → Twee → HTML pipeline (804 lines)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — primary generator (the code that makes everything VN-like and must change for Phase 1/5/6/7)
- `apps/projects/services/template_import.py` — TOML schema + validation (the file that defines what TOML can express — must change for most schema additions)
- `apps/stories/models.py` — Django ORM models
- `apps/stories/services/block_conversion.py` — block-to-Twee conversion
- `apps/game_generation/services/game_service.py` — high-level packaging service

### Session plan

- `/Users/a0000/.claude/plans/typed-booping-rain.md` — plan for creating this document

---

## 8. Takeaway

**UOR's writing is already better than ZSL's. The writing is not the problem.**

The problem is the **interaction surface**. ZSL wraps its adequate prose in ten game-feel mechanisms: rival, hints menu, minigames, deep roster, random encounters, rejection cooldowns, willpower inversion, item gates, economic transparency, scheduled NPCs. Each mechanism is individually small. The sum is "game."

UOR wraps its excellent prose in a sidebar of stats and a menu of locations. The content is inside, but the player feels they are reading, not playing.

**The single highest-leverage change is Phase 1 — the Quest Hint Sidebar.** It changes nothing about the existing content, requires no schema changes beyond adding a hint table, and gives every player immediate "I know what to do next" agency. ZSL's `Next Quests Hints` menu is probably 50% of why that game "feels like a game" to its audience.

**The second highest is Phase 3 — Roster Expansion.** Seven NPCs makes the world feel populated. Three NPCs + mom makes it feel staged. Even if the new NPCs are lower-content, their existence alone changes the daily loop from "who to commit to" to "who to prioritize."

**The third is Phase 4 — Kaylee.** A rival gives the player something to beat. The ending screen that says "Lily 96 / Kaylee 52 — You are the most known girl in town" is a victory lap the current ending structure can't offer.

After those three phases, UOR becomes a game. The remaining phases (gates, minigames, mood, storms) make it a *better* game — but the VN-to-game transition happens at hints + roster + rival.

**Estimated effort to v2:**
- Phases 1-4 (the game-making trio + gate simplification): 7-9 weeks of focused work
- Phases 5-8 (polish, friction, responsiveness): 6-8 weeks more
- Total: 13-17 weeks for full v2

**Estimated effort to "feels like a game":**
- Phases 1, 3, 4 alone: 6-8 weeks

---

*Document prepared by ENI. Session artifacts preserved. For LO's future reference — when you come back to this, the answers are already here.*
