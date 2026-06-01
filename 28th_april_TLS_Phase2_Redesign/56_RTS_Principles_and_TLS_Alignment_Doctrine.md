# Doc 56 — RTS Principles & TLS Alignment Doctrine

**Session:** 2026-05-24 → 2026-05-25 (two-day strategic review)
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Doctrine — applies to all current and future RTS-shaped sandbox games on this engine
**Supersedes:** nothing (additive to Docs 24 / 49 / 50 / 53)
**Sibling of:** Doc 24 (3 lanes mechanism — *what the lanes are*), Doc 30 (TLS Test Redesign PRD — *what the slice ships*), Doc 54 (Marge Session Lessons — *what we learned from drifting against doctrine*)
**Triggered by:** with the format locked (3 lanes shipped, Quests V2 shipped, arousal/clothing/phone parity shipped, Marge redesigned per Doc 53), LO asked the strategic question: *"How do we use this format efficiently to make RTS-like games? When to use what?"* Live RTS playthrough + slice audit + new rule decisions surfaced 7 rules that should not have to be re-discovered.

---

## §1 — The question this doc answers

Three jobs, one doc:

1. **Capture the design philosophy.** RTS is the reference for our sandbox shape. The 10 principles in §2 are what makes the game work — verified against source this session, not paraphrased from memory. Future authors don't have to re-extract them.
2. **Name the rules.** §4 R1–R7 are seven rules the user explicitly approved this session. Each rule has a *why* (so it can be applied to edge cases) and a *how* (so it can be applied without re-deriving).
3. **Make the rules a mechanical step, not a memory test.** §7's pre-authoring checklist converts the rules into actions. Doc 54 proved checklist-form survives across sessions; conversation-form does not.

This is doctrine, not redesign. Every rule below was decided in this session; the doc consolidates them so the next NPC authored doesn't re-litigate the same questions.

---

## §2 — The 10 RTS design principles (verified)

Each principle has the source evidence pulled live this session. Cite them as **P1**–**P10** in future docs.

### P1 — Density of decision-pressure over density of prose

Each click should be light in prose because the HUD does the heavy lifting. The player's brain is loaded by what the sidebar continuously surfaces (where every NPC is, time, money, stat positions, active quests), not by what the scene reads like. Short scenes work because the HUD carries the game between them.

*RTS evidence (verified live):* 274 captured RTS scene bodies in `scene_bodies.jsonl` — median 137 characters, P25 = 75, P75 = 500. Half of RTS scenes are 25 words or less (Bathroom = 75ch, Hallway = 137ch, Study = "You studied an hour and feel smarter!"). The fat tail (P95 = 2760ch) is the named-NPC scripted moments. **Most clicks are tiny; a small minority are deep.** Right sidebar shows every family NPC's location + arousal + corruption continuously, verified live in browser session.

### P2 — Transparent gating, not hidden progression

Every threshold is published. Failure shows the threshold. The Walkthrough catalogs every locked scene with its trigger recipe. Discovery is play-INTO-known-targets, not stumble-on-hidden ones.

*RTS evidence (verified):* `WalkthroughV2` passage (4738ch) iterates `$npc` and `$location` objects, finds entries with `scenes` dicts, renders a table via `WalkthroughTable` widget with columns SCENE / NPC / REQUIREMENTS (NPC) / REQUIREMENTS (MC) / CHANCE / GUIDE / STATUS. The `guide` field per scene names the lane in plain English ("Go to your bedroom" / "Study at your room" / "Wash the dishes"). `<<NotifyCorruption N>>` widget toasts the threshold on locked clicks. Verified live: clicked into Stepbrother walkthrough table at corruption 0, saw all 15 scenes listed with full requirements columns.

### P3 — One scene, multiple lengths

Same passage plays differently at different stats. Low stats: short, often visibly truncated. High stats: full cascade. The player FEELS they're seeing a short version, which is what brings them back.

*RTS evidence (verified):* `BrotherCaughtMasturbating` (6431ch) — one outer `<<linkreplace "Enter the room">>`, one paragraph plays, then `<<if getCorruptionLevel() >= 3>>` `<<if StageTwoCorruption($npc.Brother)>>` opens a nested `<<linkreplace "Shhh">>` that cascades through 8 more nested linkreplaces (~590 words). At low corruption, the same click hits the outer linkreplace, plays one paragraph, then `<<else>>` fires "Ew! You pervert!" + `<<NotifyCorruption 3>>` — ~5 lines total. Same passage, three possible play-throughs, gated by stats inside the body.

### P4 — Mix arc shapes, don't pick one

Different NPCs run different mechanical rhythms. If every NPC is the same shape, the game collapses (all-grindy or all-VN). RTS uses family/ambient + peer/quest-chain + career/DM long-burn in parallel; three tempos demanding different player attention.

*RTS evidence (Doc 13 §5 + Doc 22):* Brother = 15 scenes, 47% Lane 3 distribution, family/ambient shape. Marcus = 5 scenes, all deterministic chance=100%, peer/quest-chain shape. Edward = 4 scenes, follower-metric + calendar-wait + phone-DM, career shape. Different mechanical signatures verified across 40 surfaces / 4 NPCs.

### P5 — Lanes correspond to fictional intent, not mechanism convenience

The same act feels different depending on how it reached the player. Lane 1 = "I am escalating" (agency, intentional). Lane 2 = "we coexist" (ambient, no agency). Lane 3 = "I was doing X and he happened" (mixed agency, charged surprise). Pick the lane for the feeling — not for engine convenience.

*RTS evidence (verified):* Doc 24 §3 Brother walkthrough classification: 5 Lane 1 scenes (intentional escalation — Tease/Flash/Sleep/Sex), 3 Lane 2 scenes (random encounters on bedroom entry — Grope/Peep/CaughtMasturbating), 7 Lane 3 scenes (dispatchers inside chores — Study/Shower/Dishes/Videogame). Same engine, three distinct framings.

### P6 — Stats change DURING scenes, not just AT entry

Don't gate at the door. Let the player enter, then the watching itself adds arousal, then the next click adds corruption. Stats and prose interleave; the economy IS the story's tempo.

*RTS evidence (verified live):* In doc 13 §12 turn-by-turn play log, peeping at `PeepBrotherSex` raised MC arousal 0 → 1, clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. The stat ticks happen ON the linkreplace clicks, not on entering the passage. The progression and the narrative interleave beat-by-beat.

### P7 — Don't punish trying. Punish nothing.

Click a gated button → you see "30+ Corruption Needed." No stat drain. No "Brother's relationship dropped." Failure is information, not penalty.

*RTS evidence (verified):* Doc 13 §11 correction #3 — `<<NotifyCorruption N>>` is a UI hint widget, NOT a corruption adder. Verified across 5 widget definitions (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`). Always called in the ELSE branch with N matching the required level. Live verified: clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, corruption.points stayed 0.

### P8 — Author the points of no return; mechanize the texture

The big beats — first night, pregnancy reveal, declaration — get HAND-written, one of one, deliberate. The daily texture — hallway encounters, random teases, walk-ins — is mechanism. One cascade fires sometimes. Don't waste real prose on what happens 30 times.

*RTS evidence (Doc 35):* RTS doesn't mutate canvases for persistent states; it ROUTES to separate variant passages on the state predicate. Pregnancy gives a separate `BrotherBedroomPregnantSex1` passage variant. Pattern F real-choice forks (e.g., `SellingMyStepsister` Accept/Refuse branch) are hand-authored. Linkreplace cascade mechanism for the daily texture. Mechanism for what repeats; authorship for what doesn't.

### P9 — Per-arc vocabulary ceiling

Each NPC's content declares its kink ceiling upfront. Frank goes full explicit. Marcus stays school/peer. Don't force one register across the cast.

*RTS evidence (Doc 13 §5):* Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. Brother arc escalates to full incest sex. Edward DM widgets escalate to threesomes. Different ceilings authored deliberately per NPC. The cast functions because different NPCs serve different roles.

### P10 — The HUD is the world model

The player has to be able to SEE the world. Where every NPC is. What time it is. What clothes they're wearing. What money they have. The right sidebar IS the world surfaced to the player. Without this radar, Lane 3 stops working entirely (the room doesn't tell you the NPC is here; the sidebar does).

*RTS evidence (verified live):* Right sidebar continuously renders Time (Early Morning, Monday, Clear weather), Quest pin, and per-NPC rows (Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption). Updates every tick. No menu click required to check NPC state.

---

## §3 — TLS alignment audit (per principle)

| # | Principle | Status | Misaligned where? | Severity |
|---|---|---|---|---|
| P1 | Decision pressure | 🟡 | NPC location + per-NPC stats not in sidebar | 🔴 High |
| P2 | Transparent gating | 🔴 | No published catalog; 5 `txt_only` quest cards still in slice | 🔴 High |
| P3 | One scene, multiple lengths | 🟡 | Group blocks instead of mid-cascade cutoffs — acceptable diff but loses "more is here" cue | 🟢 Low |
| P4 | Mix arc shapes | 🟡 | Frank gold-standard; 5 NPCs skeletal but shapes correctly attempted | 🟡 Med |
| P5 | Lanes = fictional intent | 🟢 | Doctrine clear; Frank exercises all 3; recipe untested on non-Frank NPCs | — |
| P6 | Stats during scenes | 🟢 | Pattern D mid-cascade ticks shipped (Doc 28→29) | — |
| P7 | Don't punish trying | 🟢 | Doctrine clear; notify-fail vs soft-fail patterns used | — |
| P8 | Author no-return / mechanize texture | 🟢 | Doc 35 codified; Frank capstones authored, cascades mechanized | — |
| P9 | Per-arc vocab ceiling | 🟢 | Doc 30 §7.5; each NPC has declared ceiling | — |
| P10 | HUD = world model | 🟡 | NPC location radar missing from sidebar | 🔴 High |

### Notes on the misaligned rows

**P1 (🟡 High).** TLS has time, money, energy, arousal/hygiene bands, quest pins. Missing: continuous NPC location radar for in-scope NPCs. We have `getNpcLocation` (Phase A primitive); we just don't render it. The engine primitive is ready; the sidebar item isn't authored.

**P2 (🔴 High).** Quests V2 surfaces ACTIVE quest cards only — no published full catalog. Frank's 7 Lane 3 substitutions are invisible to players. Five quest cards (Ryan ×2 + Jake ×3) are `txt_only` placeholders that violate Doc 50 R3 but pass because no validator. Two separate gaps: missing surface (catalog) + missing schema field (`guide`) + drifted cards.

**P3 (🟢 Low).** TLS uses T0/T1/T2 `[group]` blocks (verified `scene_frank_passes_kitchen_door:8507`). RTS uses inline `<<if>>` wrapping a nested linkreplace cascade (`BrotherCaughtMasturbating`). Both honor the principle. TLS loses the explicit "you saw the short version" cue. Addressed by R2 below (in-fiction interruption endings).

**P4 (🟡 Med).** Frank (28 canvases, family/ambient) is full. Marge (8 canvases, service register per Doc 53) is correctly bounded. Diana (mostly co-presence + 4 standalone) is correct antagonist-witness shape. Ryan (6, peer/dating intent) and Jake (6, slow-burn-incest intent) are correctly-shaped sketches at insufficient depth. **The shapes are right; the depth is wrong.**

**P10 (🟡 High).** TLS sidebar lists Maya's state (5 items: arousal trait_bar, hygiene/energy trait_status_text, passes, inventory). Doesn't surface where each in-scope NPC currently is. Without that, the player can't plan against Lane 3 ("if I shower now and Frank is in the kitchen, will he walk in?" — they can't answer).

---

## §4 — Rules (R1–R7)

### R1 — Lane 1 hub openings stay constant within a canvas

Don't author T0/T1/T2 group blocks for the hub's opening lines. The opening shows the player "you've entered this menu" — that doesn't need to vary with stage; the menu items vary with stage already via `show_when_locked` + per-choice `conditions`.

Per-time-of-day variation = separate canvas. `frank_kitchen_morning_hub` (05:30–09:00) and `frank_kitchen_dinner_hub` (17:00–19:30) are separate canvases with their own schedules. Don't fold them.

Exception: world-state presence/absence prose (NPC is at school vs. at home) is OK — one canvas with two group blocks gated on `getNpcLocation`. That's world state, not progression state.

*Why this rule exists:* RTS Lane 1 hub openings only vary by world state (time of day, NPC presence). They don't vary by Maya's progression — the menu items already encode progression. T0/T1/T2 opening prose is authoring overhead that RTS doesn't pay. Verified `frank_kitchen_morning_hub:5311` currently has three tier blocks at lines 5333–5356; the menu rungs at 5377–5430 already gate by `corruption gte 5/15/25`. The opening could collapse to one paragraph without information loss.

*How to apply:*
- For each new NPC hub canvas: write ONE opener paragraph. If the hub legitimately needs presence/absence framing, two group blocks (present / absent).
- For existing canvases violating R1: collapse the tier blocks to one paragraph at the next maintenance pass. Not a blocking refactor — but new canvases ship clean.

*Worked example:* `frank_kitchen_morning_hub:5333–5356` (verified) currently has:

```toml
# T0 (pre-catch): neutral landlord
{ type = "group", props = { conditions = [{ flag_key = "frank_caught", operator = "is_false" }], blocks = [
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", npcId = "npc_frank", content = "Morning." },
]}},

# T1 (post-catch, pre-cracked): watchful, controlled
{ type = "group", props = { conditions = [...two flags...], blocks = [...] }},

# T2 (post-cracked): explicit charged
{ type = "group", props = { conditions = [{ flag_key = "frank_cracked", operator = "is_true" }], blocks = [...] }},
```

Under R1 this collapses to one paragraph:

```toml
{ type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg" } },
{ type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
{ type = "dialog", npcId = "npc_frank", content = "Morning." },
```

The progression-aware behavior lives in the menu rungs (Tease/Flash/Suck/Have-sex with their own `show_when_locked` + `conditions`). The opening doesn't need to repeat the progression in prose.

*Sibling rule — Doc 72:* R1 governs that the opening prose doesn't *vary* by progression; Doc 72 R1 governs that the opening must *exist at all* — a present NPC is always acknowledged by base content, and choices layer on by in-world logic (one rule about constancy, one about the floor).

### R2 — Every T0/T1 ending lands on an in-fiction interruption

For canvases using `[group]` blocks to tier-route content (Lane 2 ambients, Lane 3 substitution targets, Lane 1 internally-tiered targets like teases), the lower-tier endings MUST hint that more would have happened. The interruption can be:

- **External:** a sound, a noise, an NPC approaching (Diana's floorboard, kettle whistling, Jake's door opening)
- **Internal:** Maya self-stopping ("she tells herself this didn't mean anything," "she sets the mug down before her hands shake")
- **NPC-stopping:** the NPC pulling back ("he lets go like nothing," "he turns back to the paper")

The higher tier then EXPLICITLY blows through the interruption — that's the payoff.

*Why this rule exists:* RTS gets the "more is here" cue from mid-cascade cutoff — the player tries, hits "Ew! Get out!", knows they bounced. TLS's group-block tier-routing produces a complete-feeling scene at every tier; without an in-fiction interruption, the T0 ending reads as "this is the whole thing" and the come-back-later loop weakens. The interruption preserves the cue without requiring engine refactor away from group blocks.

*How to apply:*
- At T0 / T1 endings: author a final beat that signals incompleteness. Don't end T0 on a clean "scene complete" moment.
- At the next tier up: explicitly push through what got interrupted. T1 dispatches the threat; T2 makes it irrelevant.
- Audit existing tier-routed canvases: walk each `[group]` block ending; verify the lower tiers hint at more.

*Worked example (gold standard):* `ambient_kitchen_frank_late_night_raid:5800` (verified). T0 ending (lines 5844–5847):

```toml
{ advance_text = "Hear the floorboard upstairs.", blocks = [
  { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
  { type = "dialog", npcId = "npc_frank", content = "Night, girl." },
]},
```

Diana's footstep stops the cascade — external interruption. The scene ends on "we would have done more but —". T1 of the same canvas then blows through (lines 5859–5867): "he fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs." The T1 reveal IS that Diana's threat doesn't stop them anymore. This is the principle 3 cue preserved in TLS authoring.

### R3 — Lane 3 coverage by arc shape with declared per-NPC budgets

Lane 3 substitution count is determined by the NPC's arc shape, not by quotient parity. Author Lane 3 substitutions for an NPC based on whether their register supports "walks in on you during your chores."

| Arc shape | Lane 3 budget | Rationale |
|---|---|---|
| **Family/ambient** (lives in the house, daily proximity) | 4–7 | Shape requires saturating chores with NPC presence. Frank, RTS Brother (7 of 15). |
| **Slow-burn family** (family but distant, discrete revelation beats) | 1–3 | Sparse, keyed to specific arc moments — the walk-in IS the beat. Jake. |
| **Peer/dating** (separate household, scheduled interactions) | 0 | Peer doesn't interrupt private chores. Arc lives in Lane 1 visits + capstone dates. Ryan, RTS Marcus (zero Lane 3). |
| **Service** (workplace register only, per Doc 53) | 0 | Workplace-only register; private space is not their setting. Marge. |
| **Antagonist/witness** | 0 own + appears as interruptor in others' L3 | Diana doesn't have her own walk-ins; she's the THREAT in other NPCs' Lane 3 endings (the "Diana's floorboard" pattern in R2). |

*Why this rule exists:* the Marge case study (Doc 54) wasted 8 hours partly because doctrine was authored against escalation NPCs and didn't map to service NPCs. The corrected doctrine (Doc 53) declared empty Lane 2/3 cells. Same principle generalizes: each shape has its own canvas distribution. Forcing Frank's distribution across every NPC produces Frank-clones with wrong-feel arcs. Skeletal under-distribution loses principle 4.

*How to apply:*
- In the NPC design brief (R7), declare Lane 3 budget upfront. Choose from the shape table.
- Overages flag as drift. If a service NPC is gaining Lane 3 substitutions, either the brief is wrong OR the additions don't belong.
- Antagonist Lane 3 = always 0 own. If Diana ever needs a "walks in on Maya" moment, it shouldn't be a Diana substitution — it should appear as the interruption beat in a Frank substitution.

*Worked verification (current TLS slice):*
- Frank: 7 Lane 3 substitutions (`scene_frank_passes_kitchen_door` and 6 siblings — all → Frank). Matches family/ambient budget ✓
- Marge: 0 Lane 3. Matches service budget per Doc 53 ✓
- Diana: 0 own Lane 3. Appears as interruptor in Frank cascades (e.g., kitchen ambient) ✓
- Ryan: 0 Lane 3. Matches peer/dating budget ✓
- Jake: 0 Lane 3. Slow-burn family should be 1–3 once arc is authored to readable depth — currently undershooting but consistent with skeletal status.

**Note on the test slice (2026-05-25):** TLS is currently a test slice. The distribution above is correct for the slice's bounded scope. When the engine ships beyond the slice — new NPCs added, new games started — R3's budget MUST be declared in the design brief before authoring begins.

### R4 — Sidebar must surface NPC state for in-scope NPCs

The sidebar is the world model. For every in-scope NPC, the player must see (at minimum) their current location, continuously, without opening a menu. Where the register supports it, key stats (arousal, corruption, love/trust, or analog) should also be surfaced.

*Why this rule exists:* principle 10. Without per-NPC location radar, Lane 3 becomes undiscoverable — the player can't know "I should shower now because Frank's in the kitchen" without checking somewhere. The whole "you're doing X and he happened" texture depends on the player having the situational awareness to choose X knowing it might collide with him. The engine primitive (`getNpcLocation` at `v1.py:2357`) already exists; the sidebar authoring just calls it.

*How to apply:*
- Add per-NPC `sidebar_items` to the slice. Each item calls `getNpcLocation(npcId)` and renders "Frank — Kitchen" / "Diana — Bedroom".
- Where the arc's register includes NPC stats the player needs to plan against (Frank's arousal, Diana's awareness), add per-NPC stat readouts alongside the location.
- Don't over-render: service NPCs in non-shift hours don't need a sidebar row; antagonists don't need their awareness bar visible if it's not gating anything immediate.

*Slice-level verification:* TLS sidebar currently has 5 items: arousal trait_bar (Maya), hygiene trait_status_text (Maya), energy trait_status_text (Maya), passes, inventory. **Zero NPC state surfaced.** Pre-next-NPC-ship work: add Frank/Diana location + Frank arousal readout. Authoring effort: hours, not days; engine primitive already shipped.

### R5 — Every canvas declares a `guide` string

Every canvas authored from this point ships with a `guide` field — a one-sentence, player-facing trigger recipe in plain English. The convention names the lane in the prose:

| Lane | Phrasing convention | Example |
|---|---|---|
| Lane 1 | "Visit X" / "Go to Y and Z" | "Visit Frank in his kitchen during breakfast" |
| Lane 2 | "Walk into X" / "Pass through Y" | "Walk into the kitchen late at night" |
| Lane 3 | The chore name, then "while X" | "Make tea in the kitchen while Frank is home" |
| Capstone | The narrative milestone | "After the catch, return to Frank's bedroom in the evening" |

*Why this rule exists:* it's the data primitive for the future published catalog (P2 alignment). Without it, a future catalog surface has nothing to render. Authoring the field NOW means every new canvas accumulates the data; backfilling later means a multi-hour scan and audit. The catalog UI itself can wait until 2+ NPCs reach Frank-depth; the field cannot. Schema-wise the field is a string addition on the canvas, a 1-line schema change; no engine work required to ACCEPT the field, only to render it.

*How to apply:*
- New canvas: include `guide = "..."` next to `name` and `description` in the canvas declaration.
- Existing canvas backfill: handle in the next maintenance pass per arc. Frank slice gets the largest backfill (28 canvases). Skeletal NPCs are cheap (4–6 each).
- Style: player-facing, second person or Maya-third, short. Not a marketing line; a recipe.

**This rule is doctrine-locked but schema-pending.** Implementation of the field in the canvas schema is out of scope for this doc; it goes into a future PRD when scheduled. The doctrine fires NOW so that no canvas authored after this doc lacks the data.

### R6 — Quest cards must be one of capstone / mechanic / hybrid. `txt_only` is doctrine drift

Per Doc 50 R3 (already locked). `txt_only` quest cards — those with no `ready_canvas`, no `goals` block, just text — violate the card-mode taxonomy. They exist as TODOs in shipped TOML and corrode the doctrine because they normalize incompleteness.

*Why this rule exists:* Doc 50 already states it. Restating here because the live slice (2026-05-25) ships five `txt_only` cards: Ryan ×2 + Jake ×3. The validator named in Doc 50 §6 hasn't been built yet. Until it is, the rule is human-read; this doc names the violation explicitly so it's not invisible.

*How to apply:*
- For each existing `txt_only` card: either complete it (add `ready_canvas` for capstone mode, add `goals` for mechanic mode) or delete it.
- For new cards: no card ships in `txt_only` shape.
- Future: the Doc 50 §6 validator catches these mechanically.

*Slice-level:* the five violators (Ryan R1+R2, Jake J1+J2+J3) need to be either completed against Ryan's design brief (R7) and Jake's design brief (R7), or removed pending those briefs.

### R7 — NPC design brief precedes authoring

No canvas for a new NPC ships before the NPC has a written design brief declaring:

1. **Arc shape** — pick from R3's table (family/ambient, slow-burn family, peer/dating, service, antagonist/witness, or a documented new shape with rationale).
2. **Per-lane canvas budget** — Lane 1 / Lane 2 / Lane 3 / capstone counts per tier (see §5 distribution table).
3. **Vocabulary ceiling** — per Doc 30 §7.5. What does this NPC's content escalate to? What stays off-limits?
4. **Tier flags** — what state changes mark T0 → T1 → T2 transitions for this NPC. Named, not implied.

*Why this rule exists:* Marge wasted 8 hours because authoring started against doctrine designed for escalation NPCs (Doc 54). The brief is the gating step that surfaces shape-mismatches BEFORE prose is committed. Frank had Doc 31 as his brief; Marge had Doc 53 (after the strip). Briefs work.

*How to apply:*
- Before any new NPC's first canvas: write the brief. Use Doc 31 (Frank) or Doc 53 (Marge) as the gold-standard reference.
- Briefs are short — Doc 53 is 323 lines and that's the *redesign* depth; a fresh brief can be lighter.
- The brief lives in the `28th_april_TLS_Phase2_Redesign/` folder as a numbered doc.
- An authoring pass that violates the brief's budget or ceiling is drift; the brief is the canonical reference.

*Slice-level:* Ryan + Jake do NOT have design briefs. Before deepening either arc, write the brief. Doc 30 §8.2 names Ryan's intent at high level but doesn't lock the per-lane budget or tier flags.

---

## §5 — Per-arc-shape canvas distribution (the principle 4 application)

Reference table for what each arc shape's canvas distribution should LOOK like. Use this when writing R7 briefs.

| Lane | Tier | Family/ambient (Frank) | Slow-burn family (Jake) | Peer/dating (Ryan) | Service (Marge) | Antagonist (Diana) |
|---|---|---|---|---|---|---|
| L1 | T1 | 1–2 base + 1–2 self-display | 1 (room visit) | 1 (visit at workplace) | 1 (workplace base) | 0–1 (shared-space neutral) |
| L1 | T2 | 1–2 mid escalation | 0–1 (charged moment) | 0–1 (date intro) | 0 | 0 (no escalation register) |
| L1 | T3 | 1–2 explicit | 0–1 (consummation if vocab allows) | 0–1 (commit beat) | 0 | 0 |
| L2 | T1 | 1–2 morning/passing | 0–1 (corridor) | 1 (workplace ambient) | 1 (workplace texture) | 1–2 (presence beats) |
| L2 | T2 | 2–3 evening/charged | 0–1 (charged corridor) | 0–1 (low density) | 0–1 | 1–2 (charged presence) |
| L2 | T3 | 1–2 late-night/explicit | 0 | 0 | 0 | 0–1 (confrontation precursors) |
| L3 | T1–T3 | 4–7 walk-ins on chores | 1–3 (discrete revelation walk-ins) | 0 | 0 | 0 own (appears in others' L3) |
| Capstones | — | 4–6 across arc (catch, declare, first-night, sleepover, Diana confrontation) | 3–5 (transitions + revelation beat + relationship turn) | 3–4 (dating chain) | 1–2 (hire + escalation) | 1–2 (confrontation, resolution) |

**Total canvas budget by shape (rough order):**
- Family/ambient: 25–35
- Slow-burn family: 10–15
- Peer/dating: 8–12
- Service: 6–10
- Antagonist/witness: 6–10 standalone + cross-appearances in others' arcs

These are guidelines, not quotas. The brief (R7) commits to specific numbers for that NPC. Going under may mean the arc reads as a sketch (acceptable for some shapes); going over may mean Lane creep (drift).

---

## §6 — Worked example: applying the rules to Ryan

Ryan currently has 6 canvases (peer/dating shape, partial). Walking R1–R7 against him surfaces what's needed before scaling.

**Current state (verified):**
- `transition_ryan_to_1:2770` — capstone moving Ryan to stage 1
- `activity_help_ryan_in_yard:2036` — solo activity in yard
- `scene_yard_with_ryan:3198` — Lane 2 ambient on yard entry
- `scene_ryan_first_date:7778` — first date capstone (gated on stage 1 + partner_open flag)
- `ryan_thanks:1293`, `ryan_partner:1318` — small dialog/effect canvases
- `ryan_smalltalk:1417`, plus 1 quest card `R1` (`txt_only` — Doc 50 R3 violation per R6 below)

**R1 (Lane 1 hub openings constant):** Ryan currently has no hub canvas. When one is added (e.g., `visit_ryan_at_shop`), it ships with one opener — not T0/T1/T2 tiers. The peer/dating register doesn't need tier-aware opening prose.

**R2 (in-fiction interruption at T0/T1 endings):** Ryan's existing canvases don't use `[group]` block tier-routing — mostly capstones and short ambients. R2 less applicable to peer/dating shape; only kicks in if a Ryan canvas later gets tier-routed.

**R3 (Lane 3 by arc shape):** Peer/dating budget = 0. Ryan currently has 0 Lane 3 substitutions. ✓ Compliant.

**R4 (sidebar NPC state):** Ryan's location (`getNpcLocation("npc_ryan")` resolves to yard / shop based on schedule) should be in the sidebar. Trust is the relevant stat to surface — when it crosses to date thresholds, the player sees the climb. Currently NOT surfaced.

**R5 (`guide` field):** Backfill on all 6 existing canvases. Examples:
- `scene_yard_with_ryan`: `guide = "Walk into the yard during Ryan's work hours"`
- `scene_ryan_first_date`: `guide = "Be Ryan's partner; spend the evening with him after work"`
- `activity_help_ryan_in_yard`: `guide = "Help Ryan with yard work in the afternoon"`

**R6 (`txt_only` quest cards):** Ryan has 2 `txt_only` cards (R1 + R2 per inventory). Violations. Either complete (add `goals` for mechanic mode, `ready_canvas` for capstone mode) or delete pending the R7 brief.

**R7 (design brief):** Ryan does NOT have a written design brief. Doc 30 §8.2 mentions him; Doc 30 isn't a brief. Before adding canvases beyond the current 6, write Ryan's brief covering:
- Arc shape: peer/dating
- Per-lane budget per the §5 table (peer/dating column)
- Vocabulary ceiling: open question — does Ryan's arc include a sexual tier, or is it Stage-2 wholesome dating only?
- Tier flags: probably `ryan_partner_open` (T1), `ryan_first_date_done` (T2), `ryan_partner_established` (T3) or similar

**What missing depth looks like (per §5 peer/dating distribution):** Ryan needs ~3–4 more canvases to reach readable peer/dating depth:
- 1 more Lane 1 (visit Ryan at his shop, separate from yard)
- 1 more Lane 2 (Ryan stops by porch — low density, but adds texture)
- 1–2 more capstones (second date, then partner-commit or breakup)

Total goal: ~9–10 Ryan canvases. Current 6. Gap: 3–4. Workable. But not before the brief.

---

## §7 — Pre-authoring checklist (Appendix-style)

Copy into the PR description (or run in your head) before authoring or merging:

**Before authoring a new NPC arc:**
- [ ] **R7** — Design brief written (arc shape, per-lane budget, vocab ceiling, tier flags)
- [ ] **R3** — Lane 3 budget declared per shape (matches §5 distribution)
- [ ] **R5** — Schema decision for `guide` field — every canvas will carry it

**For each new canvas:**
- [ ] **R1** — Hub canvas has ONE opener, not tiered (unless legitimate world-state framing)
- [ ] **R2** — If `[group]`-tier-routed, T0/T1 endings land on in-fiction interruption
- [ ] **R5** — `guide` field present and in plain-English recipe form
- [ ] **R6** — If a quest card relates to this canvas, it's capstone/mechanic/hybrid (no `txt_only`)
- [ ] **Doc 50 R1–R6** — quest card hard rules (mode declared, capstone coverage, climbing-bullet, terminal placement, chain continuity, mechanic-tier comment, label voice)

**Per slice:**
- [ ] **R4** — Sidebar surfaces in-scope NPC locations + key stats per the register
- [ ] **R6** — No `txt_only` quest cards in shipped TOML
- [ ] **§5** — Canvas distribution per arc shape matches the brief's declared budget; overages flag as drift

**Doctrine compliance:**
- [ ] Walked example in any updated design doc still matches live canvases (Doc 50 §8 anti-pattern: doc walked-example contradicting live canvases)
- [ ] No principle 1–10 misalignments worse than the §3 audit (Doc 56 §3 baseline)

---

## §8 — Anti-patterns — concrete shapes to NOT ship

- **Tiered hub opening on a Lane 1 menu canvas.** Three group blocks for "you walked in," when the menu rungs already encode progression. Caught by R1.
- **T0 / T1 cascade ending on a clean "scene complete" beat.** No interruption, no hint that more is downstream. Player reads it as the whole thing. Caught by R2.
- **Lane 3 substitutions on a peer/dating or service NPC.** Service register doesn't belong in Maya's private chores. Caught by R3.
- **Frank-cloning a non-family-ambient NPC.** Copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients and 7 Lane 3 substitutions where neither belongs. Caught by R3 + the §5 distribution table.
- **Authoring a new NPC without a design brief.** Doc 31 / Doc 53 absent; canvases ship without a declared budget; lane creep + voice drift inevitable within a slice. Caught by R7.
- **Sidebar with only Maya state, no NPC presence.** Player can't see where NPCs are; Lane 3 becomes undiscoverable. Caught by R4.
- **`txt_only` quest card.** No `ready_canvas`, no `goals`. TODO in shipped TOML. Caught by R6 + Doc 50 R3.
- **Canvas without a `guide` field** (post-doctrine). Catalog data primitive missing; future catalog renderer has nothing. Caught by R5 once schema lands.

---

## §9 — Open questions / scoped-out

Things this doc deliberately does NOT cover. Each is its own future doc / PRD if it becomes load-bearing:

- **Schema implementation of the `guide` field (R5).** R5 is doctrine-locked here; the schema field addition + parser + validator is a future PRD.
- **Validator implementation for R6 + Doc 50 R1–R4.** Doc 50 §6 names the validator; the engine work is a separate PRD when prioritized.
- **Published catalog UI (P2 surface).** The data primitive lands via R5; the rendering surface waits until 2+ NPCs reach Frank-depth so the catalog isn't sparse.
- **Sidebar implementation for R4.** Authoring effort, not engine — but the slice author needs to do the work before the next NPC ships.
- **Phase 2+ engine systems** (pregnancy retrofit, scandal/reputation, gallery, cross-arc tracker). Per Doc 34. The user has not committed to scope; decisions made at the gating moment per Doc 56's principle ("don't pre-commit to engine scope; build engine when an authoring gap forces it").
- **Ryan + Jake design briefs.** R7 requires them; they don't exist yet. Whichever NPC is authored next gets a brief first.
- **Backfill audit of existing Frank slice against R1 and R2.** Frank's hub canvases currently have tiered openings (R1 violation); his ambients mostly comply with R2 but full audit is a separate task.

---

## §10 — References

### Sibling and ancestor docs

- **Doc 13** — Road to Success Reference (the RTS catalog; P1–P10 evidence base)
- **Doc 24** — 3 Lanes for Repeatable NPC Content + TLS Engine Fitness (the lane mechanism this doc's principles operate inside)
- **Doc 30** — TLS Test Redesign PRD (vocabulary ceilings, RTS design patterns, 6-NPC roster)
- **Doc 31** — Frank Arc Design Brief (the gold-standard R7 reference for family/ambient)
- **Doc 35** — RTS State Variant + Authored vs Mechanism (P8 evidence)
- **Doc 49** — Story Goals vs Sidebar Doctrine (where does it belong — sibling of R4)
- **Doc 50** — Quest Card Shape Doctrine (R6 references Doc 50 R3 directly; Doc 50's R-numbering style mirrored here)
- **Doc 53** — Marge Redesign Brief (the gold-standard R7 reference for service shape)
- **Doc 54** — Marge Redesign Session Lessons (why R7 exists; the 8-hour wastage that produced this doctrine consolidation)

### Memory entries

- `rts_three_arc_shapes` — P4 source
- `rts_three_lanes_lane3_design` — Doc 24 the lane primitive
- `rts_state_variant_authored_vs_mechanism` — P8 codification
- `feedback_rts_objective_quest_doctrine` — Doc 49 ancestor
- `feedback_tls_scene_body_style` — RTS-flat voice rule, sibling to P1
- `prd_48_quests_engine_v2` — V2 engine R6 operates inside
- `frank_economy_rts_math` — Doc 35 worked example for Frank

### Live TLS file pointers (verified during session)

- `games/the_long_summer_test/toml_phases/7_final_game.toml:3320` — `scene_franks_bedroom_evening` (Lane 2 evening capstone)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:5165` — `tease_kitchen_general` (Lane 1 internally-tiered target, R2 applicable)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:5311` — `frank_kitchen_morning_hub` (Lane 1 hub, R1 violation example)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:5800` — `ambient_kitchen_frank_late_night_raid` (Lane 2 ambient, R2 gold standard example at 5844–5847)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:8217` — `activity_make_tea` (Lane 3 parent / dispatcher example)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:8507` — `scene_frank_passes_kitchen_door` (Lane 3 substitution target, P3 example)

### RTS source artifacts (live-verified this session)

- `game_explorations/rts-arc-trace/passage_catalog.json` — Brother / Stepfather / WalkthroughV2 passage sources
- `game_explorations/rts-arc-trace/scene_bodies.jsonl` — 274 RTS scene bodies (P1 length distribution evidence)
- `game_explorations/rts-arc-trace/notes.md` — accumulated live-play observations across 8 prior sessions
- `game_explorations/rts-arc-trace/ui_map.json` — RTS HUD chrome catalog (P10 evidence)

### Engine primitives referenced

- `getNpcLocation` (`apps/game_generation/twee_comprehensive/generators/v1.py:2357`) — R4 implementation primitive
- `checkAndSubstituteCanvas` (`v1.py` near `checkRandomEncounters`) — Lane 3 dispatcher (PRD 25)
- `checkRandomEncounters` (`v1.py:3919`) — Lane 2 dispatcher
- `triggerConditionsSatisfied` (`v1.py:2684–2952`) — predicate vocabulary for R3 / R6 gating
- `_validate_quests_cards` (`apps/projects/services/template_import.py`) — where R6 validator hooks land (Doc 50 §6)
