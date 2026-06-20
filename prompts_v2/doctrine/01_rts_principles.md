# Doctrine 01 — The 10 RTS Design Principles (P1–P10)

**Source:** Doc 56 §2 (`28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md`, 2026-05-24/25).
**Authority:** Doctrine. Every principle is verified against RTS source extraction in `game_explorations/rts-arc-trace/` (live-play + passage_catalog.json + variable_index.json).
**Purpose:** Name the 10 design principles every RTS-shape sandbox follows. Each principle has its RTS evidence cite reproduced verbatim. **Cite these as P1–P10 in all downstream prompts + docs.**

These principles describe *why* RTS works. The mechanism vocabulary (Lane 1/2/3/4) is in `doctrine/02_three_lanes_plus_capstone.md`. The arc-shape taxonomy + per-arc canvas budgets are in `doctrine/03_arc_shapes.md`. The authoring rules that operationalize these principles are in `doctrine/04_authoring_rules.md`.

---

## P1 — Density of decision-pressure over density of prose

Each click should be light in prose because the HUD does the heavy lifting. The player's brain is loaded by what the sidebar continuously surfaces (where every NPC is, time, money, stat positions, active quests), not by what the scene reads like. Short scenes work because the HUD carries the game between them.

**RTS evidence (live-verified):**

> 274 captured RTS scene bodies in `scene_bodies.jsonl` — median 137 characters, P25 = 75, P75 = 500. Half of RTS scenes are 25 words or less (Bathroom = 75 chars, Hallway = 137 chars, Study = "You studied an hour and feel smarter!"). The fat tail (P95 = 2760 chars) is the named-NPC scripted moments. **Most clicks are tiny; a small minority are deep.** Right sidebar shows every family NPC's location + arousal + corruption continuously, verified live in browser session.

**Authoring implication:** the Lane 1/2/3 prose target is the RTS-flat 30-word caption density (Doc 30 §7.1). The HUD is what makes 30-word scenes survive — without continuous sidebar feedback, the player has nothing to plan against. Image-first composition + sparse stage directions + dialogue doing the character work. Density goes into Lane 4 capstones, not into the daily texture.

**Cross-reference:** `doctrine/05_rts_flat_prose.md` (the 8 rules); `schema/01_engine_capabilities.md` §8 (sidebar item types).

---

## P2 — Transparent gating, not hidden progression

Every threshold is published. Failure shows the threshold. The Walkthrough catalogs every locked scene with its trigger recipe. Discovery is play-INTO-known-targets, not stumble-on-hidden ones.

**RTS evidence (verified):**

> `WalkthroughV2` passage (4738 chars) iterates `$npc` and `$location` objects, finds entries with `scenes` dicts, renders a table via `WalkthroughTable` widget with columns SCENE / NPC / REQUIREMENTS (NPC) / REQUIREMENTS (MC) / CHANCE / GUIDE / STATUS. The `guide` field per scene names the lane in plain English ("Go to your bedroom" / "Study at your room" / "Wash the dishes"). `<<NotifyCorruption N>>` widget toasts the threshold on locked clicks. Verified live: clicked into Stepbrother walkthrough table at corruption 0, saw all 15 scenes listed with full requirements columns.

**Authoring implication:** every canvas should ship with a `guide` string (Doc 56 R5 doctrine; schema field pending Doc 62 PRD). Every locked-choice Lane 1 menu item ships with `locked_text_threshold` publishing the gate value (RTS-style `<<NotifyCorruption N>>` pattern). The published catalog UI will render from these data primitives once Doc 62 ships.

**Cross-reference:** `doctrine/04_authoring_rules.md` R5 + R6; `schema/01_engine_capabilities.md` §10.4–§10.5.

---

## P3 — One scene, multiple lengths

Same passage plays differently at different stats. Low stats: short, often visibly truncated. High stats: full cascade. The player FEELS they're seeing a short version, which is what brings them back.

**RTS evidence (verified):**

> `BrotherCaughtMasturbating` (6431 chars) — one outer `<<linkreplace "Enter the room">>`, one paragraph plays, then `<<if getCorruptionLevel() >= 3>>` `<<if StageTwoCorruption($npc.Brother)>>` opens a nested `<<linkreplace "Shhh">>` that cascades through 8 more nested linkreplaces (~590 words). At low corruption, the same click hits the outer linkreplace, plays one paragraph, then `<<else>>` fires "Ew! You pervert!" + `<<NotifyCorruption 3>>` — ~5 lines total. Same passage, three possible play-throughs, gated by stats inside the body.

**Authoring implication:** for canvases that internally tier (Lane 2 ambients, Lane 3 substitution targets, Lane 1 escalation rungs), the lower-tier endings MUST hint at incompleteness — interrupted by an external sound (Diana's floorboard), self-stopping ("she sets the mug down before her hands shake"), or NPC pulling back ("he turns back to the paper"). The higher tier explicitly blows through the interruption — that's the payoff. This is Doc 56 R2 — *in-fiction interruption at T0/T1 endings.*

TLS uses `[group]` blocks instead of nested linkreplace, which loses the "you saw the short version" cue unless the in-fiction interruption is authored. Without it, the T0 ending reads as the whole thing.

**Cross-reference:** `doctrine/04_authoring_rules.md` R2.

---

## P4 — Mix arc shapes, don't pick one

Different NPCs run different mechanical rhythms. If every NPC is the same shape, the game collapses (all-grindy or all-VN). RTS uses family/ambient + peer/quest-chain + career/DM long-burn in parallel; three tempos demanding different player attention.

**RTS evidence (Doc 13 §5 + Doc 22):**

> Brother = 15 scenes, 47% Lane 3 distribution, family/ambient shape. Marcus = 5 scenes, all deterministic chance=100%, peer/quest-chain shape. Edward = 4 scenes, follower-metric + calendar-wait + phone-DM, career shape. Different mechanical signatures verified across 40 surfaces / 4 NPCs.

**Authoring implication:** the cast is 4–6 NPCs, each picking ONE arc shape from the 5-shape taxonomy (family/ambient, slow-burn family, peer/dating, service, antagonist/witness). Per-arc-shape per-lane canvas budgets in `doctrine/03_arc_shapes.md` are not interchangeable. Forcing one NPC's shape onto another produces drift — see Doc 54 Marge case study (escalation-NPC doctrine forced onto service register; 8 hours wasted before strip-clean recovery).

**Cross-reference:** `doctrine/03_arc_shapes.md`; `doctrine/04_authoring_rules.md` R3 + R7.

---

## P5 — Lanes correspond to fictional intent, not mechanism convenience

The same act feels different depending on how it reached the player. Lane 1 = "I am escalating" (agency, intentional). Lane 2 = "we coexist" (ambient, no agency). Lane 3 = "I was doing X and he happened" (mixed agency, charged surprise). Pick the lane for the feeling — not for engine convenience.

**RTS evidence (verified):**

> Doc 24 §3 Brother walkthrough classification: 5 Lane 1 scenes (intentional escalation — Tease/Flash/Sleep/Sex), 3 Lane 2 scenes (random encounters on bedroom entry — Grope/Peep/CaughtMasturbating), 7 Lane 3 scenes (dispatchers inside chores — Study/Shower/Dishes/Videogame). Same engine, three distinct framings.

**Authoring implication:** when scoping a beat, ask *"who is making this happen?"* before deciding the mechanism.
- Maya consciously claims the act → Lane 1.
- World produces ambient presence → Lane 2.
- Maya was solo + NPC arrives → Lane 3.
- Once-only narrative milestone → Lane 4 capstone.

Tease via Lane 1 = Maya decided to put on a show. Tease via Lane 3 = Maya was changing her clothes and NPC walked in mid-strip. Same physical act, different fictional weight. Picking the wrong lane neutralizes the beat.

**Cross-reference:** `doctrine/02_three_lanes_plus_capstone.md` §1–§3.

---

## P6 — Stats change DURING scenes, not just AT entry

Don't gate at the door. Let the player enter, then the watching itself adds arousal, then the next click adds corruption. Stats and prose interleave; the economy IS the story's tempo.

**RTS evidence (verified live):**

> In Doc 13 §12 turn-by-turn play log, peeping at `PeepBrotherSex` raised MC arousal 0 → 1, clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. The stat ticks happen ON the linkreplace clicks, not on entering the passage. The progression and the narrative interleave beat-by-beat.

**Authoring implication:** stat-effect macros should appear on individual cascade beat clicks + per-choice in `exit_block.choices.effects`. NOT only on canvas entry. The progression should feel beat-by-beat — each click moves both narrative and economy.

The corollary: per-beat `effects` lists in cascade blocks let small acts accumulate. A 4-beat cascade can author 4 separate +1 corruption ticks. The whole scene moves Maya 4 corruption, but the player FELT each move.

**Cross-reference:** `schema/01_engine_capabilities.md` §6.1 (effect schema); `schema/02_toml_schema.md` §7.4 (choice effects).

---

## P7 — Don't punish trying. Punish nothing.

Click a gated button → you see "30+ Corruption Needed." No stat drain. No "NPC's relationship dropped." Failure is information, not penalty.

**RTS evidence (verified):**

> Doc 13 §11 correction #3 — `<<NotifyCorruption N>>` is a UI hint widget, NOT a corruption adder. Verified across 5 widget definitions (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`). Always called in the ELSE branch with N matching the required level. Live verified: clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, corruption.points stayed 0.

**Authoring implication:** locked-choice clicks render `locked_text_threshold` as a toast banner (the TLS analog of `<<NotifyCorruption N>>`). Zero stat effects. Zero flag effects on failure. The player must be able to discover gates by clicking them without paying a price.

Anti-pattern: a Lane 1 menu item that decrements `relation` on locked-click. That penalizes exploration. RTS doesn't do this anywhere. Don't ship it.

**Cross-reference:** `schema/01_engine_capabilities.md` §10.4 (notifications + soft-fail); `doctrine/07_anti_patterns.md`.

---

## P8 — Author the points of no return; mechanize the texture

The big beats — first night, pregnancy reveal, declaration — get HAND-written, one of one, deliberate. The daily texture — hallway encounters, random teases, walk-ins — is mechanism. One cascade fires sometimes. Don't waste real prose on what happens 30 times.

**Mechanize the prose, not the priority.** "Texture" here means the *writing* is templated and re-readable (RTS-flat) — it does NOT mean the daily loop is low-value or low-coverage. For a cohabitation game the daily routine is the **primary content channel by volume** (`doctrine/02` §6, §3.1): it is where the corruption the player built gets spent. Mechanize each chore's prose so it survives 30 readings; do not *under-build the routine itself*. A thin daily loop — few solo hosts, no walk-ins, no feeder floor — starves the game no matter how good the capstones are.

**RTS evidence (Doc 35):**

> RTS doesn't mutate canvases for persistent states; it ROUTES to separate variant passages on the state predicate. Pregnancy gives a separate `BrotherBedroomPregnantSex1` passage variant. Pattern F real-choice forks (e.g., `SellingMyStepsister` Accept/Refuse branch) are hand-authored. Linkreplace cascade mechanism for the daily texture. Mechanism for what repeats; authorship for what doesn't.

**Authoring implication:** voice register is dual:
- **Lane 1 / 2 / 3 = RTS-flat default.** Re-readable without grating. Specific detail, but flat structure. ~30-word captions.
- **Lane 4 capstones = Tier-3 literary register, earned by the once-only nature of the scene.** Interior monologue, layered sensory detail per beat, character-distinguishing diction. (Doc 57 §6.)

The voice contract is "specificity, not literary density." Lane 2/3 prose can be specific ("the runner Diana picked out") without being literary (no interior monologue, no extended metaphor). Tier-3 is reserved for canvases the player will see once.

**Cross-reference:** `doctrine/05_rts_flat_prose.md`; `doctrine/02_three_lanes_plus_capstone.md` §4 (Lane 4 voice register).

---

## P9 — Per-arc vocabulary ceiling

Each NPC's content declares its kink ceiling upfront. Frank goes full explicit. Marcus stays school/peer. Don't force one register across the cast.

**RTS evidence (Doc 13 §5):**

> Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. Brother arc escalates to full incest sex. Edward DM widgets escalate to threesomes. Different ceilings authored deliberately per NPC. The cast functions because different NPCs serve different roles.

**Authoring implication:** each NPC's R7 design brief declares the vocab ceiling per Doc 30 §7.5. The ceiling determines:
- Crude diction permitted at full intensity (Frank breeding talk vs Marcus peer slang)
- Anatomy + cum + degradation language allowance
- Power-dynamic register (dom-sub / cuckold / sibling incest / public exhibitionism)
- What's off-limits even at maximum tier

Per-arc ceiling = per-arc TONE. Forcing one register flat across the cast produces sameness; the cast functions because the registers contrast.

**Cross-reference:** `doctrine/08_kink_vocab_ceilings.md`.

---

## P10 — The HUD is the world model

The player has to be able to SEE the world. Where every NPC is. What time it is. What clothes they're wearing. What money they have. The right sidebar IS the world surfaced to the player. Without this radar, Lane 3 stops working entirely (the room doesn't tell you the NPC is here; the sidebar does).

**RTS evidence (verified live):**

> Right sidebar continuously renders Time (Early Morning, Monday, Clear weather), Quest pin, and per-NPC rows (Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption). Updates every tick. No menu click required to check NPC state.

**Authoring implication:** the sidebar must surface, for every in-scope NPC:
- Current location (via `getNpcLocation`; surfaced by the `npc_panel` `location` row — shipped)
- Key stats per the register (arousal + corruption + relation for family/ambient; relation only for peer/service; location-only for antagonist)

Without per-NPC location radar, Lane 3 becomes undiscoverable — the player can't plan "if I shower now and Frank is in the kitchen, will he walk in?" The whole "you were doing X and he happened" texture depends on the player having the situational awareness to choose X knowing it might collide with the NPC.

**Visibility doctrine:** stage NEVER surfaces (internal-only per Doc 68 §9). Antagonist awareness NEVER surfaces (dramatic surprise depends on player NOT seeing how close confrontation is). Body-state (energy + hygiene) MUST surface.

**Cross-reference:** `doctrine/09_trait_catalog.md` §8 (NPC sidebar visibility per arc shape); `doctrine/04_authoring_rules.md` R4.

---

## Cross-references

### Sibling doctrine files

- `doctrine/02_three_lanes_plus_capstone.md` — the mechanism vocabulary the principles operate inside
- `doctrine/03_arc_shapes.md` — per-arc canvas distribution that operationalizes P4
- `doctrine/04_authoring_rules.md` — R1–R7 + Doc 50 R1–R6 + Doc 57 R1–R5 + F1–F5 (the rule layer)
- `doctrine/09_trait_catalog.md` — trait vocabulary the principles reference

### Schema files

- `schema/01_engine_capabilities.md` — engine primitives that implement each principle
- `schema/02_toml_schema.md` — per-section field tables

### Source docs (this folder's ancestor)

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — RTS catalog
- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — Brother source extraction
- `28th_april_TLS_Phase2_Redesign/22_RTS_Cross_NPC_Mechanism_Comparison.md` — 40 surfaces / 4 NPCs
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane mechanism source + §10 framework
- `28th_april_TLS_Phase2_Redesign/35_RTS_State_Variant_Authored_vs_Mechanism.md` — P8 codification
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` — source for this file

### RTS source artifacts (live-verified)

- `game_explorations/rts-arc-trace/passage_catalog.json` — RTS passage bodies (P1 length distribution; P3 nested cascade example; P8 variant passages)
- `game_explorations/rts-arc-trace/scene_bodies.jsonl` — 274 RTS scene bodies (P1 evidence)
- `game_explorations/rts-arc-trace/ui_map.json` — RTS HUD chrome catalog (P10 evidence)
- `game_explorations/rts-arc-trace/notes.md` — accumulated live-play observations

---

## Appendix — Mental check before authoring

Before any new canvas, ask:

| Question | Principle |
|---|---|
| Is the prose ≤ 30-word caption density (Lane 1/2/3) or earned-Tier-3 (Lane 4)? | P1 + P8 |
| Is the gate threshold published when the choice is locked? | P2 + P7 |
| Does the canvas tier-route in a way that hints at "more to come"? | P3 |
| Does this NPC's arc shape match the chosen lane distribution? | P4 |
| Is the lane chosen for fictional intent, not engine convenience? | P5 |
| Are stat-effect macros on cascade beats, not just on entry? | P6 |
| Are locked-click failures pure information (no stat drain)? | P7 |
| Is voice register matched to the lane (RTS-flat vs Tier-3)? | P8 |
| Does the content respect the NPC's declared vocab ceiling? | P9 |
| Does the sidebar surface the state the player needs to plan this beat? | P10 |

If any answer is "no," fix it before shipping. If unsure, surface to LO.

**End of file.** Next: `doctrine/02_three_lanes_plus_capstone.md` for the mechanism vocabulary.
