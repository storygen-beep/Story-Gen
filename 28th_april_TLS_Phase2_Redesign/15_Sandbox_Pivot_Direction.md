# 15 — Sandbox Pivot: Design Philosophy & Reasoning Chain

> **Created 2026-05-03.**
> Synthesis doc capturing everything learned across the 2026-05-02 → 2026-05-03 session that led to TLS pivoting from VN-style stage chains to RTS-style sandbox content.
> Sibling to `00_TLS_Phase2_Diagnosis_and_Direction.md` — this is the *next* direction update, written after RTS was actually played and the diagnosis updated.
> Reading order for future contributors: **read this doc 15 FIRST**, then `13_Road_to_Success_Reference.md` for the empirical RTS observations, then `14_Engine_PRD_Sandbox_Additions.md` for the engine work needed.
>
> **Status: direction locked, content authoring not started.** Phase 1 Frank pilot is the next concrete step (see §14).

---

## §0 Why this doc exists

Across one ~12-hour session (2026-05-02 → 2026-05-03), the TLS direction shifted from "complete the Phase 2 stage-chain redesign" to "pivot toward RTS-style sandbox content." Three docs came out of the session:

- **`13_Road_to_Success_Reference.md`** — empirical reference of what RTS does (763 lines)
- **`14_Engine_PRD_Sandbox_Additions.md`** — engineering spec for the changes needed (709 lines)
- **`15_Sandbox_Pivot_Direction.md`** (this doc) — the *why* and the reasoning chain that connects them

The two prior docs are *reference* + *spec*. This doc is *direction*. Without it, future contributors will read 13 and 14 and not understand which parts of the older Phase 2 design (`01_Repeatable_First_Doctrine.md`, `02_NPC_Stage_Chains.md`, `04_Scene_Cascade_Pattern.md`) still hold, which are now demoted, and which decisions are open vs locked.

This doc is **deliberately reflective**. It includes the methodology lessons we learned, the inferences I (Claude, the assistant working with the user) got wrong and corrected mid-session, the doctrinal trade-offs we considered, and the open questions still unanswered. The honesty is the point — without seeing what changed and why, the new direction reads like an arbitrary reversal of the old. With the reasoning chain visible, the pivot is clearly an empirically-grounded update.

---

## §1 The methodology lesson — extract for structure, play for behavior

**The single most important lesson from the session.**

Early in the session, I (Claude) explored RTS by reading source code: `npc.X.scenes` data structure dumps, `BrotherBedroom` passage source, all Speech-widget definitions. From this I wrote the first version of doc 13 with confident claims about how RTS works.

When the user pushed back ("did you play the game or extract the information??"), the answer was: extracted, mostly. ~6 meaningful clicks of live play. Everything else was source-code archaeology.

We then ran two focused playthroughs (~30 + ~80 turns). **Five of the inferences from data extraction turned out to be wrong:**

1. ❌ "Walkthrough requirements are strict gates" → actually they're *suggested thresholds for full content*; random encounters fire at MC corruption 0 even though walkthrough says 15 needed
2. ❌ "Higher stats unlock new scenes" → actually they unlock *more content within the same scene* via linkreplace branching
3. ❌ "`<<NotifyCorruption N>>` raises corruption when failing taboo actions" → actually it's a *UI hint widget* showing "you need corruption N for this"; never modifies stat
4. ❌ "Three arc shapes (family/peer/career) cleanly categorize NPCs" → actually every NPC is *hybrid*; the shapes are tendencies not categories
5. ❌ "NPC arousal is stored as emoji-tier string (`🔥`/`🔥🔥`)" → actually stored as *integer*; emoji is the walkthrough display threshold format

Plus a craft layer I missed entirely: **NPC interior thought bubbles** (`💭 Alfred is thinking... <em>thought text</em>`) rendered as styled bubbles distinct from speech. Source-reading didn't surface this — only seeing it during the `BedroomSleepDadScene` playthrough did.

### Rule going forward

> **Source extraction generates clean stories. Live play generates messy truth.**
>
> Use source extraction for *structure* (data shapes, schemas, code paths). Use live play for *behavior* (does the runtime actually do what the code looks like it should). Neither alone is sufficient. The two complement each other.

This rule applies to every future "let's see what game X does" exploration. **Don't write design conclusions from source-only extraction.** Always play, even if briefly, before writing recommendations.

This rule was added to `MEMORY.md` and `13_Road_to_Success_Reference.md` §16.

---

## §2 What we learned about RTS (compressed)

Full reference is `13_Road_to_Success_Reference.md`. This section is the compressed essentials that drove our pivot decisions.

### Game shape

- 53 NPC keys defined; 16 with predefined `scenes` objects
- ~130+ total scenes (60 NPC-bound + 70 location-bound)
- 27 quest definitions (3 active at game start, 24 latent)
- 41 locations
- 7-day week × 6 time buckets (EM/M/A/E/N/LN)

### The walkthrough is the planning UI

The Walkthrough panel publishes the literal scene table to the player verbatim:

| SCENE | NPC | REQUIREMENTS (NPC) | REQUIREMENTS (MC) | CHANCE | GUIDE | STATUS |

Same fields as the engine's internal scene struct. **Player loop is "open Walkthrough → pick a near-unlock → close the gap."** Transparency is the design, not a fallback.

### Three arc tendencies (not categories)

Same `npc.X.scenes` engine drives three radically different player experiences depending on *ratio* of trigger types per NPC:

- **Family / proximity tendency** (Brother, Dad, Grandpa) — mostly random ambient encounters on room entry, dice rolls, NPC arousal as tier ladder. Player walks past them constantly; content needs to be ambient.
- **Peer / quest-chain tendency** (Marcus) — mostly deterministic chance=100 scenes gated by narrative prerequisites ("get test grade ≥ 8", "wait for invite"). Traditional VN beat-by-beat.
- **Career / digital tendency** (Edward) — mostly metric+wait+DM-mediated. Phone-based, async, calendar-driven.

**Every NPC mixes triggers** — Brother has random encounters AND deterministic player-initiated buttons (Tease/Flash/Have sex) AND time-of-day deterministic (Sleep With Him at LN+relation 10) AND cross-NPC bridges (SellingMyStepsister). The "tendencies" describe the dominant trigger ratio, not strict categorization.

### Three writing tiers, used deliberately

- **Tier 1 (utility one-liner):** "STUDY / You studied an hour and feel smarter!" — for activities and stat-tick acknowledgments
- **Tier 2 (vignette prose):** "You push open the door, only to stop dead in your tracks. He's in bed with a girl..." — for random encounters with anonymous partners
- **Tier 3 (scripted character writing):** Natasha intro ("She slips something into her book to hold the page... Same girl from the hallway. This is the first time you actually stop to talk.") — for named-NPC introductions, quest beats, arc transitions

RTS doesn't waste Tier-3 on Tier-1 moments. **Reserved for moments that earn it.** This is part of why a 130-scene game ships at all.

### NPC interior thought bubbles

A 4th writing dimension orthogonal to the three tiers. Styled bubble with `💭` icon, "thinking..." label, italic content:

> 💭 *Alfred is thinking...*
> *I can't help myself... she looks so peaceful, so innocent. I just need to touch her...*

Distinct from regular speech bubbles. Adds character interiority without text density. Drastically increases narrative depth in the same word count.

### Linkreplace-drip scene structure

Each scene = multi-step in-place reveal, not single-render passage. Click → reveal +paragraph + image. Click → reveal +video + new line. Click → next reveal.

This is the IF-craft layer that converts "a dice roll triggered this" into "I'm reading a story." Without it, scenes feel like popups even when they're well-written.

### Content branches INSIDE scenes by stat tier

The most counter-intuitive RTS pattern. **Same scene plays differently for different stats — same passage, different reveal length.**

- `BrotherCaughtMasturbating` at MC corruption 6 = 5-line scene ending "Ew! you pervert! Stop it!" → Brother yells "Get out!"
- `BrotherCaughtMasturbating` at MC corruption 31 = same opening, but new `[Shhh]` linkreplace appears → multi-stage seduction (~590 words, full sex sequence)

**Player's reward for grinding stats isn't a *new* scene — it's *more of the same scene*.** Drives the come-back-later loop that makes RTS feel deep.

### Day 1 immediate content

The single most-cited finding for the pivot decision. **On Day 1 Evening, just walking from Hallway → Brother's room and Dad's room, the game served two full random encounters with images + video at MC corruption 0.** Voyeur content access requires *zero* stat-grinding.

Stat grinding is for *escalation to active participation* (flash/sex), not initial content access. The game lures you in fast, then makes deeper participation the long-tail goal.

### Other patterns worth noting

- **Soft-fail vs notify-fail:** chrome buttons silently no-op; high-stakes buttons show notification with the threshold ("30+ Corruption Needed")
- **Cross-NPC scene flag dependencies:** `SellingMyStepsister` gates on Brother corruption + Josh-not-unlocked. Once unlocked, transfers Brother arc INTO Josh arc. Arcs converge instead of running parallel forever.
- **Passive NPC trait drift:** Brother arousal climbed 0→3 over 3 in-game days *without me doing anything to him*. NPCs have a passive trickle. World feels alive, not waiting.
- **Real branching choices exist** for major story moments (`SellingMyStepsister` Accept/Refuse), rare but reserved for stakes
- **Travel friction is real but mitigated** by sidebar shortcuts (`🏫 Go to School`)

---

## §3 Honest corrections — where I was wrong

Recorded so future sessions don't make the same mistakes. Each was confident-but-wrong before live play corrected it.

### Correction 1: Walkthrough thresholds are not strict gates

- **Original claim:** "Triple gating — NPC stats AND Player stats AND probability — strictly enforced"
- **Truth:** Random encounter passage source only checks `previous() == "Hallway" && random(1,4) == 1 && !executedToday`. The `requirementsMC.corruption: 15` field for `PeepBrotherSex` is bypassed at trigger time.
- **Implication:** Walkthrough's "REQUIREMENTS (MC)" column is *suggested threshold for full content*, not entry gate. Player can stumble into scenes early and get truncated versions.

### Correction 2: Higher stats unlock more content INSIDE scenes, not new scenes

- **Original claim:** "Player has to reach the threshold to unlock the scene as binary access"
- **Truth:** Every visit shows entry beat + image + first paragraph. Linkreplace beats *after* that branch by stat. Verified live: clicked "Keep Watching" on Dad's `ProstituteSex` at MC corruption 0 → linkreplace inserted *empty content*. Scene literally has no more body for me at that tier.
- **Implication:** Every scene has a "low-stat short version" and a "high-stat full version" inside the same passage. Player can't be punished for trying. Player knows there's more, comes back later.

### Correction 3: `<<NotifyCorruption N>>` is a UI hint, not a corruption-adder

- **Original claim:** "Failing taboo actions raises corruption — rejection trains the player. Brilliant design loop."
- **Truth:** `<<NotifyCorruption N>>` is a UI feedback widget that displays "you need corruption level N for this." Always called in the ELSE branch with N matching the required level. Pattern verified across 5+ widget definitions (`JimDM`, `RichardDM`, `EdwardDM`, etc.).
- **Live verified:** clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, corruption.points stayed 0.
- **Implication:** The rejection-trains-corruption loop **does not exist** in RTS. Failure is *information* (publishes the threshold), not *progress*.

### Correction 4: NPC arousal is integer, not emoji-tier string

- **Original claim:** "Stored as emoji-tier string `''` / `'🔥'` / `'🔥🔥'` / `'🔥🔥🔥'`"
- **Truth:** Stored as integer (Brother arousal observed at `1`, `3`, `5` from `eval` reads). The emoji notation is the *display threshold format* in the walkthrough's REQUIREMENTS column.
- **Implication:** NPC stats compose normally (numeric thresholds). Doc 13 §10 was wrong, now patched.

### Correction 5: "Three arc shapes" was oversimplified

- **Original claim:** "Brother = pure family ambient. Marcus = pure peer quest-chain. Edward = pure career metric."
- **Truth:** Brother is a hybrid — has random encounters AND deterministic player-initiated buttons AND time-gated AND cross-NPC bridges. Same engine, mixed triggers per NPC. Doc 13 §5 was a clean story I told from data; live play shows messier reality.
- **Implication:** When TLS authors a new NPC, don't pick "one shape." Pick a *ratio* of triggers (mostly random + some deterministic, or mostly deterministic + tiny random splash, etc.).

### Bonus correction: Even "100% chance" deterministic scenes can have rejection variants

- **Original assumption:** Deterministic = full content always plays.
- **Truth:** `SleepingBrother` walkthrough says "100% chance" — but at relation 12 the scene plays a 134-word *rejection* outcome ("Brother wakes, tells player to leave"). Higher relation gates the consummation.
- **Implication:** The walkthrough's `CHANCE: 100%` means trigger always fires when reqs met, but content within still gates by stats. Players can "unlock" mechanically and still see a stub. Even hidden tier-laddering inside deterministic scenes.

### Bonus correction: Passive NPC trait accumulation

- **Original assumption:** NPC stats only change from MC actions.
- **Truth:** Brother arousal climbed 0→3 over 3 in-game days passively. Day 1 Evening voyeur content works because by then, family arousals are already non-zero.
- **Implication:** World drifts on its own. Not just decay (TLS already supports) but also passive *gains*.

### Bonus correction: Being groped raises MC corruption

- **Original assumption:** Tutorial said "1 arousal per day OR after being groped" — only mentioned arousal.
- **Truth:** Live observed: BedroomGrope scene gave MC +1 corruption. Bootstrap is *faster* than tutorial implies — passive groping accelerates corruption naturally.
- **Implication:** Game gives more than it advertises. Encourages exploration through pleasant surprise.

---

## §4 The TLS diagnosis (current state vs RTS)

Audit done by reading TLS test slice TOMLs (`games/the_long_summer_test/toml_phases/`) and comparing against RTS findings. **The slice is well-engineered but tells the wrong kind of story for the engine it's running on.**

### Misalignments (ranked by impact)

| # | RTS Principle | TLS Status | Evidence | Impact |
|---|---|---|---|---|
| 1 | Hand the player content immediately | MISALIGNED | All 3 NPCs require 3+ prerequisite activities before any content unlocks. Frank needs 3 bookkeeping sessions; Ryan needs settle-in flag (3 of 4 conditions); Jake needs beauty 40+ | **HIGH** |
| 2 | Mix arc shapes per NPC | MISALIGNED | Frank, Ryan, Jake all on deterministic quest-chain pacing. No ambient random-encounter NPC. No metric-grind NPC. | **HIGH** |
| 3 | Same scene, different stats | MISALIGNED | Entry-gate `chance = 0.30` produces empty visits 70% of the time. No in-scene branching by stat tier. | MED |
| 4 | Walkthrough is quest log with thresholds | PARTIALLY MISALIGNED | Hints publish stage-level guidance ("Frank wants help with the books") but counter values (`frank_bookkeeping_count ≥ 3`) are invisible to player. | MED |
| 5 | Three writing tiers, used deliberately | MISALIGNED | All TLS canvas bodies use Tier-2 vignette prose uniformly. Even pure utility activities (Sleep, Eat from fridge) get sensory writing. Arc transitions don't *land different* because peaks lose punch. | MED |
| 6 | Story at scene level, not arc level | MISALIGNED (doctrinal) | TLS authors arc coherence per NPC (Stage 0→1→2→3 narrative escalation). RTS scatters 130 disconnected vignettes. **Intentional, not a bug — but worth naming.** | MED |
| 7 | Scenes are flows (linkreplace) | NOT USED | TLS canvases are single-render. Doctrinal choice, not bug. | LOW |
| 8 | Time × clothing × location compose into gates | ALIGNED (AHEAD) | TLS multi-schedule OR-logic per canvas is more expressive than RTS. | — |
| 9 | Don't punish trying | ALIGNED | Soft-fail / no-render for gated choices. Same principle, different channel. | — |
| 10 | Failure is information, not progress | ALIGNED | Thresholds published via hints (different channel than RTS notifications, same effect). | — |
| 11 | Stage hybrid system | AHEAD | TLS `stage_npc/stage_op/stage_value` lets one NPC mix sequential beats AND stat-tier escalation. RTS picks one shape per NPC. | — |

### Bottom line

The slice **proves the stage-system architecture works** — that's what it was designed to do. But it **abandons three textures that make RTS feel like a sandbox**:

1. **Immediate content access** (Day 1 voyeur scenes at corruption 0)
2. **Three parallel arc tempos** (not all NPCs on the same deterministic metronome)
3. **Transparent counter thresholds** in the player-facing quest log (`X/3 bookkeeping done` visible)

The 10-day slice with 3 NPCs on the same pacing makes the game feel **linear**. Mixing arc shapes (e.g., make Diana an ambient random-encounter NPC, Marge a metric-grind NPC, keep Jake as the deterministic anchor) would restore tempo variety without changing the engine — same `stage_npc/stage_op/stage_value` system, different per-NPC `chance` values + different gate styles in helpers.

---

## §5 The doctrinal split — what kind of game are we building?

**This is the deepest question the session surfaced.** Not "what features should the engine have" but "what *kind* of experience are we authoring."

### Two valid options

| If we want to be **RTS** (sandbox content library): | If we want to be **character-arc VN**: |
|---|---|
| Content count > arc depth | Arc depth > content count |
| Many small scenes (60+ per NPC) | Few long scripted scenes (5-15 per NPC) |
| Random encounters > stage scenes | Stage scenes > random encounters |
| Stat-tier reveals > narrative throughline | Narrative throughline > stat-tier reveals |
| Transparency (publish all gates) | Mystery (discover what unlocks) |
| Player constructs their story by sequencing | Authored arc per NPC |
| ~130 scenes total | ~30 scenes total |

The current slice sits *between* these. **That's the deepest problem.** Caught between gives the worst of both worlds — VN-level grinding for sandbox-level reward.

### User decision (2026-05-03)

> "We want to be like RTS, lets change our design philosophy to be more sandbox."

**Direction locked.** TLS pivots toward RTS-style sandbox.

### What this means concretely

1. **Stop authoring per-NPC arcs as the spine.** Stage transitions become *capstones* (big flag-gated moments) not the narrative throughline.
2. **Start authoring scenes as the daily texture.** Each NPC gets 8-15 scenes with mixed triggers (random + deterministic + time-gated + cross-NPC bridges).
3. **Stats become the player's leverage to see deeper content** (via in-scene branching), not the gate to unlock new content.
4. **The Quests panel becomes a planning tool**, publishing counter values + thresholds per NPC.
5. **Three writing tiers used deliberately.** Tier-1 utility for activities. Tier-2 vignette for ambient encounters. Tier-3 character writing reserved for capstones and intros.
6. **Mix arc tendencies across NPCs.** Not all NPCs on deterministic quest-chain pacing.

### What this does NOT mean

- We're not throwing out the stage system. Stages stay as *capstones*.
- We're not throwing out the existing 4 Frank scenes. They become the *anchors* of the new library.
- We're not adopting RTS verbatim. TLS keeps multi-schedule OR-logic and the `stage_npc/stage_op/stage_value` hybrid, both ahead of RTS.
- We're not promising to ship 130 scenes. The volume target is "enough that the world feels alive" — TBD per playtest.

---

## §6 What changes about the design philosophy

### Old TLS thinking

> "Each NPC has a story arc. Player progresses the arc by doing the right things. The arc has stages (0→1→2→3). At each stage, new scenes unlock. Eventually the arc completes."

### New RTS-style thinking

> "The world is a content library. NPCs live in it. Scenes happen when the player walks into the right place at the right time with the right stats. There is no 'completing' an arc — there's just discovering more scenes. Stats are the player's leverage to see deeper content."

### Eight philosophical shifts

1. **Author scenes, not arcs.** A scene is a contained moment. Multiple scenes per NPC contribute to *implied* character development through cumulative encounter, not scripted beat ladders.

2. **Stat thresholds replace stage transitions for routine content.** Each scene checks its own gates: this kitchen scene needs trust ≥ 5 AND time = evening. This crisis scene needs trust ≥ 15 AND first_rent_paid = false. **No central stage ladder.** Gates compose, they don't chain.

3. **Content shows up everywhere, not at story beats.** Player walks into kitchen → maybe a Frank scene fires (random check). Player goes to porch → maybe Diana scene fires. Player sleeps → maybe night event fires. **Constant content texture.** The player is rewarded for *moving around*, not for *executing the right sequence*.

4. **The Quests panel becomes a planning tool, not a tutorial.** Old: "Frank: Help with the books. (next: ???)". New: "Frank scenes: Bookkeeping evening kitchen — trust 0+ — locked (need trust 5). Crisis: rent unpaid — UNLOCKED. Porch evening cigarette — trust 10+ — locked." Player opens panel, sees what's close to unlocking, plans their day around it.

5. **Random encounters, not narrative beats, become the heartbeat.** Player does activities to raise stats → stats unlock random encounter pool → encounters fire as you move around → each visit is a content lottery (but a fair one — every visit shows *something*).

6. **Content branches inside scenes, not between them.** Old: low corruption = scene A unlocked, high corruption = scene B unlocked, two separate scenes. New: low corruption = scene shows 2 paragraphs + image, high corruption = same scene shows 4 paragraphs + image + video + new dialogue choice. **One scene, two depths.** This is the come-back-later loop.

7. **NPCs are hybrid, not single-shape.** Family/proximity NPCs (Frank, Diana, Marge) get random ambient + deterministic player-initiated mix. Peer NPCs (Jake) keep more deterministic shape. Career NPCs (future) get metric+wait. **Mix across the 12 NPCs of the full game.**

8. **Domain matches geography.** NPCs you're physically near = ambient random encounters. NPCs in their own domain = quest-chain unlocks. NPCs accessible only via metrics = patient long-tail.

---

## §7 What stays the same — don't throw out

Every Phase 2 doc up to 12 still has parts that hold. The pivot is *additive*, not a wholesale rewrite. Here's what survives intact.

| What survives | Why | Doc reference |
|---|---|---|
| Stage system as **capstone layer** | Stages still author the big moments (the catch, the cracked summons). They're flag-gated checkpoints, not the spine. | `02_NPC_Stage_Chains.md` |
| Hint priority + specificity picker | `(priority desc, condition_items.length desc, file_order asc)` is exactly the picker we need for scene-variant selection too. Same picker, new use. | `12_Engine_PRD_09_Hint_System_Completeness.md` |
| Triple gating (NPC stats / MC stats / chance) | The gating model is correct. We just need to apply it across more scenes per NPC. | `04_Scene_Cascade_Pattern.md` |
| Scene cascade pattern (`group` blocks with conditions) | Already supports tier-branching inside a single canvas. We just need to use it more aggressively. | `04_Scene_Cascade_Pattern.md` |
| Time bucket schedule (6 bands + weekday) | RTS uses near-identical structure. TLS multi-schedule OR-logic per canvas is *ahead* of RTS. Keep. | `01_Repeatable_First_Doctrine.md` |
| Helper-driven stage transitions | Keep for capstones. Stage 0→1 helper still needed for "first catch" type moments. | `08_Engine_PRD_Phase2_Additions.md` E4 |
| `stage_npc/stage_op/stage_value` hybrid hint conditions | Lets one NPC support both Marcus-style sequential beats AND Brother-style stat-tier escalation. **Ahead of RTS.** Keep. | `12_Engine_PRD_09_Hint_System_Completeness.md` |
| Quests/Walkthrough panel as primary UI | Already exists. Just needs counter-display extension (S3 in doc 14). | `09_Future_Polish_Items.md` |

What needs *minor* revision (not throw out):

- `01_Repeatable_First_Doctrine.md` — add §X: "Repeatable scenes can ALSO have stat-tier branching internally (S1)"
- `02_NPC_Stage_Chains.md` — add note: stage chains are now the *capstone* layer; scene library is the *daily texture* layer

What needs *major* revision (currently blocking the pivot):

- `feedback_tls_scene_body_style.md` (memory entry) — currently mandates RTS-flat for ALL scene bodies. Blocks Tier-3 character writing. Must be updated before content authoring.
- `11_Hint_Authoring_Guide.md` — currently teaches stage-keyed hints. Sandbox style adds scene-keyed hints with priority/specificity (already supported by picker). Need new section.

---

## §8 The honest engine state

Full audit in `14_Engine_PRD_Sandbox_Additions.md` §1.

### Already shipped (5 of 12 sandbox capabilities)

✅ Random encounters with `chance` field  (v1.py:3751-3820)
✅ Cross-NPC scene flag conditions (v1.py:9225, JSON `{version, logic, items}`)
✅ Passive trait drift — decay direction (v1.py:629-641 + advanceDay v1.py:3929-3944)
✅ `chance` field on canvas triggers
✅ Choice text_variants (template_import.py:459-460, picker v1.py:9689-9697)

### Partial (5 of 12 — need extension, S1-S6 in doc 14)

🟡 Per-block text_variants — choices only today, blocks need it (S1)
🟡 Per-canvas executedToday — only per-activity-name today (S2)
🟡 QuestsPage counter display — hint text only today (S3)
🟡 Threshold notifications on gated choices — costs only today (S4)
🟡 Sidebar travel shortcuts — data-driven but no shortcuts authored (S5)
🟡 Passive trait *gains* — only decay supported (S6)

### Missing / structural (2 of 12 — S7-S8 in doc 14, optional pending playtest)

❌ Linkreplace-drip multi-step scenes (S7, ~150 LOC)
❌ NPC thought bubble block type (S8, ~50 LOC)

### Net engine effort

- Phase 2 (S1-S6): ~95 LOC, all additive, zero breaking schema changes
- Phase 3 (S7-S8): ~200 LOC, optional pending Phase 2 playtest

**The engine is ~85% ready.** Closing the gap takes ~95 LOC of small additions. The biggest work is content, not engineering.

---

## §9 The honest content state

This is the **biggest practical risk** of the pivot.

### Volume math

- Current TLS: ~3 scenes per NPC × 12 NPCs = ~36 scenes
- Target sandbox volume: ~10-15 scenes per NPC × 12 NPCs = ~120-180 scenes
- **Net: ~3-5x content authoring increase**

For comparison:
- RTS has ~130 NPC-bound scenes + ~70 location-bound scenes = ~200 scenes total
- RTS development was a multi-year solo project
- TLS test slice has 3 NPCs (Frank, Ryan, Jake), full game has 12

### Three writing tiers, deliberately

| Tier | Where used | Approx word count per scene | % of total scenes |
|---|---|---|---|
| Tier 1 (utility one-liner) | Activities, stat-tick acknowledgments | 5-15 words | ~30% |
| Tier 2 (vignette prose) | Random ambient encounters | 30-100 words | ~50% |
| Tier 3 (scripted character) | Named-NPC intros, stage capstones, arc transitions | 200-600 words | ~20% |

If we hit ~150 total scenes:
- ~45 Tier-1 utility (~5 hours total writing)
- ~75 Tier-2 vignette (~30 hours total)
- ~30 Tier-3 scripted (~40 hours total)

Roughly **75 hours of focused content writing** for the full sandbox library. **This is the biggest commitment of the pivot.**

### Quality bar

- Every scene must work standalone (player may encounter it as their first or tenth Frank scene)
- No scene assumes prior scene was seen (unless it's a flag-gated capstone)
- Voice consistency across the library (Frank sounds like Frank in scene 1 and scene 14)
- Tier-3 reserved discipline — don't waste density on Tier-1 moments

### Author requirements

- Knows TLS canon (NPC voices, world rules, locations)
- Can write Tier-2 vignette efficiently (most of the volume)
- Can write Tier-3 character moments (most of the difficulty)
- Comfortable with TOML authoring + the `[group]` block tier-branching pattern

**Open question:** is there one author who can do this, or do we need to split? Flagged in §11 risks.

---

## §10 What's locked vs what's open

### Locked (decisions made, won't revisit without strong reason)

✅ **Sandbox direction.** TLS pivots from VN-style stage chains to RTS-style sandbox content. (User confirmed 2026-05-03)
✅ **Phase 1 = Frank pilot, content-only.** No engine changes until pilot validates the philosophy. (User confirmed 2026-05-03)
✅ **Family/proximity NPCs get Day 1 ambient encounters.** Frank, Diana, Marge each need random ambient content from Day 1.
✅ **Peer NPCs (Jake) get domain-gated intros.** Quest-chain shape stays.
✅ **Career NPCs (future, town/job) get metric-gated content.** Patient long-tail tempo.
✅ **Doc 14 engine PRD is approved** for incremental work (S1-S6 small additions, S7-S8 deferred pending Phase 2 playtest).
✅ **Three writing tiers (vs single Tier-2)** are part of the doctrine, with Tier-3 explicitly carved out for capstones and intros.
✅ **Stage system stays as capstone layer.** Existing stage-flag scenes (catch, cracked summons) are preserved.
✅ **Per-NPC arc tendencies, not categories.** Mix triggers per NPC; no NPC is purely one shape.

### Open (need decisions before specific work proceeds)

🟦 **RTS-flat doctrine update** — need to update `feedback_tls_scene_body_style.md` (memory entry). Three options proposed in Phase 1 step 0:
  - A: Lift the flat mandate entirely (risk: over-write everywhere as Tier-3)
  - B: Keep flat as default, carve out Tier-3 for specific scene types (recommended)
  - C: Defer; Phase 1 in Tier-2 only (risk: pilot fails the playtest)
🟦 **Stage 3→4 natural content scope** — currently dev-only. Phase 1 includes it, or defer because Stage 3→4 helper has 5 unmet conditions in slice anyway?
🟦 **Phase 3 structural work (S7 linkreplace, S8 thought bubbles)** — pending Phase 2 playtest. Not committed yet.
🟦 **Content authoring throughput** — flagged as biggest risk in §11. Who writes? At what cadence?
🟦 **Number of NPCs to apply pattern to** — Frank pilot first; if success, expand to all 12? Or pick 5? Phased rollout?
🟦 **Final per-NPC scene count target** — 8? 10? 15? Depends on Phase 1 playtest pacing.
🟦 **Random encounter chance values** — RTS uses 25-50%. TLS will start at similar; tune per playtest.
🟦 **Should existing 4 Frank scenes be rewritten as Tier-3 or kept as-is?** — depends on doctrine option chosen above.

### Deferred (acknowledged but not in scope right now)

⏸ **Cross-NPC bridge scenes** — RTS pattern (Brother → Josh transfer). Engine supports today (S5 cross-NPC conditions). Not in Phase 1 scope; consider for Phase 2 expansion.
⏸ **Career/digital arc NPCs** — town/job NPCs not in test slice. Defer to full-game build.
⏸ **`under_one_roof` issue list** — separate game's bug list. Tracked in `games/under_one_roof/issue.md`. Not in scope of this pivot.

---

## §11 Risks (honest)

### High severity

**R1. Content authoring volume.** Going from ~36 to ~120-180 scenes is the single biggest commitment. ~75 hours of focused writing, with sustained voice consistency and tier discipline. **No one has committed to this volume yet.**
- *Mitigation:* Phase 1 Frank pilot validates the per-scene cost before scaling. If 10-15 scenes for one NPC takes 2 weeks, full game = 24 weeks of writing alone.

**R2. RTS-flat doctrine collision.** Memory entry `feedback_tls_scene_body_style.md` will block Tier-3 character writing. Authors will keep producing Tier-2 prose for Tier-3 moments by default. Pilot will fail to demonstrate the tier difference.
- *Mitigation:* Update doctrine BEFORE Phase 1 authoring begins. Step 0 of Phase 1 plan.

### Medium severity

**R3. Linkreplace gap may be required for full RTS feel.** Without S7, even with all other engine additions, scenes will feel less alive than RTS. Phase 3 may not be optional.
- *Mitigation:* Phase 2 playtest answers this. Budget 2-3 weeks for Phase 3 in case it's required.

**R4. Stage system tension.** TLS authored coherent per-NPC arcs. Sandbox shift trades that for emergent narrative. Players may miss the scripted progression.
- *Mitigation:* Keep stage-flag capstones intact. Emergent narrative is the *daily texture*; scripted arcs are the *milestones*. Both coexist.

**R5. Author skill — Tier-3 character writing requires craft.** Not all writers can do sensory-grounded character voice. If we have a Tier-2-only writer pool, the pivot fails the playtest.
- *Mitigation:* Reserve Tier-3 scenes for the strongest writer(s). Spread Tier-2 work more broadly.

### Lower severity

**R6. Counter discovery for S3.** If stage helpers don't expose thresholds in a parseable way, S3 generator pass might miss some counters.
- *Mitigation:* Walk all `[[engine.stage_helpers]]` definitions, parse `conditions.items` for trait + value pairs. Manual override field for edge cases.

**R7. Per-canvas executedToday backward compatibility (S2).** Existing TOMLs that share activities will get more permissive cooldowns under S2.
- *Mitigation:* Default change is more permissive, which authors can tighten if needed. Document the change.

**R8. Player confusion at the pivot.** Players who know the current TLS may find the new sandbox jarring.
- *Mitigation:* Test slice is the right place to land this — early-access players expect change. Full game can reflect lessons.

---

## §12 Decision audit trail

Chronological record of how the session reached its conclusions. Useful for future contributors who want to know *when* and *why* a decision was made.

| Date | Event | Outcome |
|---|---|---|
| 2026-05-02 | RTS exploration session 1 — data extraction (npc.X.scenes, passage source, widget defs) | Initial doc 13 written, with errors |
| 2026-05-02 | User pushback: "did you play the game or extract the information??" | Acknowledged: ~6 meaningful clicks of live play, mostly extraction |
| 2026-05-02/03 | Brother arc playthrough — ~30 + ~80 turns across two sessions | 5 confident inferences corrected by live observation |
| 2026-05-03 | Doc 13 §16 added with corrections + NPC thought bubble finding | Doc 13 status: empirically grounded |
| 2026-05-03 | TLS slice misalignment audit (Explore agent) | Identified Day 1 gap, single arc shape, hidden counters as top issues |
| 2026-05-03 | "10 things RTS teaches us" in simple words | Direction implications surfaced |
| 2026-05-03 | "What we're doing wrong" honest assessment | User saw doctrinal split clearly |
| 2026-05-03 | User decision: "We want to be like RTS, lets change our design philosophy to be more sandbox" | **Direction locked: sandbox pivot** |
| 2026-05-03 | Engine readiness audit (Explore agent) | ~85% of sandbox capabilities already shipped |
| 2026-05-03 | Doc 14 engine PRD specified | 6 small + 2 structural engine additions, ~95 LOC for Phase 2 |
| 2026-05-03 | Phase 1 Frank pilot proposed | Decision pending on RTS-flat doctrine option (A/B/C) |
| 2026-05-03 | This doc 15 created | Synthesis of session reasoning chain |

---

## §13 Reading guide for future contributors

If you're new to this project and trying to understand the current direction, **read in this order:**

1. **`15_Sandbox_Pivot_Direction.md`** (this doc) — current direction + why
2. **`13_Road_to_Success_Reference.md`** — the empirical RTS observations that drove the pivot. Pay special attention to §11 (corrections) and §16 (playthrough findings).
3. **`14_Engine_PRD_Sandbox_Additions.md`** — the engine work needed. §1 is the audit; §3 is the additions table.
4. **`feedback_tls_scene_body_style.md`** (memory entry) — current scene-body style mandate. **Note: needs revision** per §10 above.
5. **`02_NPC_Stage_Chains.md`** — the stage system, which now lives as the *capstone* layer.
6. **`04_Scene_Cascade_Pattern.md`** — the scene-cascade engine primitive that supports in-scene tier branching.
7. **`12_Engine_PRD_09_Hint_System_Completeness.md`** — the hint picker that handles priority + specificity.

If you're confused by docs 00-12, **they're earlier-state foundations**. Some still hold (the engine PRDs in 03, 08, 12 are doctrine-compatible). Some are now demoted (the stage chain as spine concept in 02). The pivot doc 15 is the current direction.

---

## §14 What to do next (Phase 1 Frank pilot)

The concrete next step. Detailed proposal in conversation 2026-05-03; summarized here.

### Step 0 — Resolve RTS-flat doctrine option (decision required)

User chooses A / B / C from §10 above (B recommended). Update `feedback_tls_scene_body_style.md` accordingly.

### Step 1 — Sketch new Frank scene library on paper

Create `16_Frank_Scene_Library.md` (next slot). Lists 10-15 Frank scenes with: trigger, location, time, content tier, one-line pitch. **No TOML changes yet.**

### Step 2 — Get sign-off on scene list

User reviews 12-scene table proposed in conversation. Adds/removes/swaps as needed.

### Step 3 — Author 2-3 sample scenes first

Pick the most pattern-establishing:
- Hallway pass (simplest random ambient — proves chance + group-block tier branching)
- Talk to Frank button (proves per-day relationship-builder + tier-branched dialogue)
- Catch scene Tier-3 polish (proves doctrine update works in practice)

Build slice → play 10 minutes → validate before writing the rest.

### Step 4 — Author the rest of the library

~5-6 more scenes. One TOML file at a time. Build + play after each batch.

### Step 5 — Phase 1 playtest (1 hour focused session)

Validate three properties:
1. Day 1 ambient content fires within first 5-10 turns at zero stats
2. Come-back-later loop works (different group-block content at different stats)
3. Frank feels alive vs mechanical

### Step 6 — Decision gate

- ✅ If Frank works → propose Phase 2 (S1-S6 engine additions) + extend pattern to Diana/Marge/Ryan/Jake
- ❌ If Frank still feels mechanical → revisit doctrine before any engine work or scaling

---

## §15 Questions still unanswered

Captured here for transparency. Some need playtest data; some need design decisions.

### Need playtest data

- How aggressive should ambient encounter chance be? (RTS uses 25-50%)
- Will players miss the scripted per-NPC arc progression?
- Is content-tier branching inside scenes enough to drive the come-back-later loop, or is linkreplace required?
- Does the increased ambient encounter frequency feel "alive" or "spammy"?
- Will the Quests panel counter display motivate stat-grinding, or just clutter the UI?

### Need design decisions

- Should existing 4 Frank scenes be rewritten as Tier-3 capstones or kept verbatim?
- Should Stage 3→4 natural content be Phase 1 scope (currently dev-only)?
- How many NPCs should the pattern apply to in the next iteration after Frank pilot? (5 / 8 / all 12)
- What's our final per-NPC scene count target? (8 / 10 / 15)
- Who authors the new content? Single writer or team?
- What's the target authoring cadence? (1 NPC per week? 2 weeks?)
- Should we rebuild the test slice fresh, or evolve in place?

### Need product decisions

- Is the test slice player audience tolerant of mid-stream design pivots?
- Should the full TLS commit to sandbox before all 12 NPCs are reshaped, or stage in?
- Does the sandbox pivot affect monetization / pricing assumptions?

---

## §16 TL;DR

After ~12 hours of session work across two days:

**What we learned:**
- RTS's design is more layered than data extraction reveals — playing surfaced 5+ wrong inferences
- Same engine ships three arc *tendencies* (family/peer/career), all hybrids
- Walkthrough-as-quest-log + stat-tier branching inside scenes + immediate Day 1 content + linkreplace-drip + thought bubbles + mixed triggers per NPC = the RTS recipe
- TLS slice has the engine for either RTS-style sandbox or character-arc VN, but its content commits to neither

**What we decided:**
- Pivot to sandbox direction (locked 2026-05-03)
- Phase 1 = Frank pilot, content-only, validates philosophy before engine work
- Engine ~85% ready; ~95 LOC of small additions close most of remaining gap
- Stage system stays as capstone layer; new scene library is the daily texture layer

**What's the biggest risk:**
- Content authoring volume — ~75 hours for full sandbox library
- Doctrine doc updates (RTS-flat memory entry) blocking Tier-3 writing

**What to do next:**
- Resolve RTS-flat doctrine option (Step 0)
- Sketch Frank scene library (Step 1, doc 16)
- Author 2-3 sample scenes, build, play, validate (Steps 3-5)
- Decide on expansion at Step 6 gate

**The honesty discipline:**
- Source extraction generates clean stories; live play generates messy truth
- Use both, never one alone
- Document corrections explicitly so future sessions don't repeat the mistakes

---

**End of doc 15.** 🟦 Direction locked. Status updates land in §10 (locked vs open) and §11 (risks) as decisions are made.
