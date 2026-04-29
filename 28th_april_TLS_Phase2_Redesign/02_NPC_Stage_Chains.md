# 02 — NPC Stage Chains

> **Created 2026-04-29.**
> Establishes the per-NPC stage chain as the design's first-class authoring artifact.
> **This round: Frank only, in full depth.** Other NPCs are scaffolded for the next authoring round.
> Inherits vocabulary from `01_Repeatable_First_Doctrine.md`.

---

## The stage-chain contract

A **stage** is a named position in an NPC's arc. Stages are flags. Every scene the player can enter with that NPC reads the stage flag and picks a branch from the cascade. Stage advancement is the act of flipping the flag — usually from inside a scene, sometimes from a state-pump button, occasionally from a true one-shot canvas.

A **stage chain** is the ordered list of an NPC's stages from arrival to terminal beat, plus the gate that advances each one and the content that opens at each. It is the single document an author consults when deciding what content lives where for that NPC.

The contract has four columns:

| Column | What it holds |
|---|---|
| **Stage** | Numbered position (0..N) and a one-line name |
| **Gate** | The composite condition that means "Maya is currently in this stage" |
| **Advancing trigger** | The flag that flips to move to the next stage, and where it gets flipped |
| **Content unlocked** | Buttons that appear at hubs, branches that fire in scenes |

Every cascade in `04_Scene_Cascade_Pattern.md` reads from this table. Every new button described in `05_Hub_and_Location_Specs.md` (deferred) traces back to a stage transition listed here.

---

## Stage-flag naming convention

Flag names below are illustrative. The schema PR finalizes them. The shape is what matters.

- **Stage flag.** One per NPC, integer-valued. Illustrative: `frank_stage = 0..4`.
- **Sub-stage advancement counters.** Numeric counters that gate within-stage transitions. Illustrative: `frank.bookkeeping_count`, `frank.tease_count`. Per master spec §2.5b: per-act counters increment on scene completion.
- **One-time guards.** Boolean flags set when a one-time branch fires inside a repeatable shell. Illustrative: `frank_caught`, `frank_restrict_declared`, `frank_cracked`. Once set, they stay set.
- **Daily reset flags.** Cleared by `activity_sleep`. Illustrative: `talked_to_frank_today`. Used by state-pump buttons.
- **Helper functions.** Per master spec §2.6, named composite gates expressed as engine helpers (E4 shipped). Illustrative: `frank_stage_2()`, `frank_stage_3()`. Cascades reference the helper, not the raw threshold — tuning happens in one place.

The integer stage flag (`frank_stage = 0..4`) is the spine. The helper functions, counters, and one-time guards feed into it.

---

## Frank — full chain

Five stages collapsed from the eight stages in `archive_02_TLS_Rewrite_Spec_2026-04-29.md` §6. The collapse is intentional: each numbered stage represents a regime change in the player's interactions with Frank. Sub-stage transitions inside a regime are tracked by counters and one-time guards.

### Stage table

| Stage | Name | Gate (current state) | Advancing trigger → next | Content unlocked at this stage |
|---|---|---|---|---|
| **0** | Suspicious landlord | `frank_stage == 0` (default at arrival) | `frank.trust >= 20` AND `frank.bookkeeping_count >= 3` → `frank_stage = 1` | hub_franks_office: "Talk", "Help with bookkeeping". Kitchen scene fires terse Stage-0 branch. |
| **1** | Grudging warmth | `frank_stage == 1` | `frank_caught` flag set (from one-time branch in `hub_living_room` evening) → `frank_stage = 2` | hub_back_porch E-band: "Sit with Frank on the porch". Kitchen scene fires Stage-1 branch (he asks if she's any good with numbers). Office scene fires Stage-1 branch (working warmth). |
| **2** | Restrict | `frank_stage == 2` AND `frank_restrict_declared` | `frank.tease_count >= N` AND `corruption >= 50` AND `frank.arousal >= 30` → `frank_stage = 3` | hub_kitchen + hub_living_room: chore buttons (porch sweep, kitchen cleanup, yard clean, office filing). Kitchen + office scenes fire post-catch register. New scene `scene_franks_office_supervised` available. |
| **3** | Tease under compliance | `frank_stage_3()` (helper: `corruption >= 50` AND `frank_restrict_declared` AND `frank.arousal >= 30`) | `frank_cracked` flag set (from one-time branch inside `scene_franks_office_supervised` after enough tease firings) → `frank_stage = 4` | hub_franks_office: "Linger by the desk" appears. Tease cascade in office scene unlocks. Crack-adjacent register in kitchen scene. |
| **4** | Cracked / Keep route | `frank_stage == 4` AND one of `frank_keep_route in {romantic, arrangement, rupture, power_inverted}` | Terminal — arc closes. (Summer end is the next external event.) | hub_franks_bedroom unlocks. Office bookkeeping button replaced by Keep-route options. Per-route scene branches in bedroom + office. |

### What this looks like to the player

Same hubs every day. Same scene canvases every visit. The arc moves because:

1. **Stage 0 → 1.** The player talks with Frank a few times, helps with bookkeeping three times. Trust ticks up. Eventually `frank_stage_1()` clears. The next time the player enters the kitchen during a Frank time-band, the cascade picks the Stage-1 branch — Frank asks about numbers. A new button appears at the back porch in the evening: "Sit with Frank."

2. **Stage 1 → 2.** The player triggers a corruption-25-gated solo activity in the living room while Frank is scheduled home. The living-room hub's evening branch fires its `frank_caught == false` one-time guard: the catch scene plays, the flag flips. Subsequent visits to the living room route to a different branch. The player sees `frank_stage = 2`, `frank_restrict_declared`. Chore buttons appear at kitchen and living room. The kitchen scene's Stage-2 branch fires from now on (supervised tone).

3. **Stage 2 → 3.** The player accumulates tease counter via the supervised office scene. At `corruption >= 50` AND `frank.arousal >= 30` AND `frank.tease_count >= N`, the helper `frank_stage_3()` clears. New button at the office: "Linger by the desk." The office scene's Stage-3 branch carries tease content from now on.

4. **Stage 3 → 4.** Tease scene fires enough times under compliance; the one-time `frank_cracked` branch fires inside the scene's deepest tier. Stage flips to 4. The Crack is a branch, not a separate canvas. Bedroom hub unlocks. Office button set transforms.

**Five stages × ~3 scene surfaces (kitchen, office, living room/back porch) = ~15 effective scene textures from ~3 repeatable canvases plus the hub branches.** That's the leverage Phase 2 is designed for.

### Where stages get advanced (audit)

Per the doctrine: "stage advancement is the act of flipping the flag — usually from inside a scene, sometimes from a state-pump button, occasionally from a true one-shot canvas."

| Transition | Where the flag flips | Mechanism |
|---|---|---|
| 0 → 1 | Computed: `frank_stage_1()` helper evaluates on canvas entry. Implemented per master spec §2.6 note (a) — derived flag computed and stored. | Helper-driven |
| 1 → 2 | One-time branch inside `hub_living_room` evening. Sets `frank_caught` and (after player choice) `frank_restrict_declared`. The `frank_stage = 2` value is the helper-derived consequence. | Branch inside repeatable shell |
| 2 → 3 | Computed: `frank_stage_3()` helper evaluates after counter + threshold conditions clear. | Helper-driven |
| 3 → 4 | One-time branch inside `scene_franks_office_supervised` deepest cascade tier. Sets `frank_cracked`. | Branch inside repeatable shell |
| 4 → terminal | Player choice inside the Crack branch sets the keep-route flag. Arc closes at summer-end (external). | Branch + external timer |

**No transition uses a separate non-repeatable "story arc" canvas.** Every flag flip happens either as a derived consequence of state movement or as a one-time guard inside a repeatable shell. This is the doctrine in action.

### Stage-content cross-reference

For each Frank stage, the canvases the cascade lives in:

| Stage | Kitchen scene | Office scene | Living room hub | Back porch hub | Bedroom hub |
|---|---|---|---|---|---|
| 0 | Stage-0 branch (terse, careful) | Stage-0 branch (bookkeeping ask, neutral) | — | — | locked |
| 1 | Stage-1 branch (numbers warmth) | Stage-1 branch (working warmth) | Catch one-time branch (gated `frank_caught == false`) | "Sit with Frank" button + Stage-1 chat | locked |
| 2 | Stage-2 branch (supervised tone) | Stage-2 branch (paper-filing, supervised) | catch already fired; new register | Stage-2 chat | locked |
| 3 | Stage-3 branch (Crack-adjacent register) | Stage-3 tease cascade (Linger by desk button) | Stage-3 register | Stage-3 chat | locked |
| 4 | Stage-4 register per keep-route | Per-keep-route branches | Stage-4 register | Stage-4 chat | unlocked; per-keep-route scenes |

This is the input that `04_Scene_Cascade_Pattern.md` consumes. The Stage-X branch column for "Kitchen scene" is exactly what gets implemented as the kitchen scene's internal cascade in that doc.

### What's deliberately NOT in Frank's stage chain

- **No `event_frank_meet` canvas.** Frank's meet is a flag-gated branch inside `event_arrival_at_franks` (the one-shot arrival cutscene per master spec §8). After arrival, the kitchen scene's Stage-0 branch carries Frank's "Suspicious landlord" register on every subsequent visit.
- **No `event_frank_offers_books` canvas.** The bookkeeping offer is the Stage-1 branch of the kitchen or office scene. It fires the first visit after `frank_stage = 1` clears, and on choice sets a flag that opens the bookkeeping button.
- **No `event_frank_first_tease` canvas.** First tease is the first visit at `frank_stage = 3` to the office scene. The cascade picks the Stage-3 branch.
- **No `event_frank_call_out` canvas.** Call-out is a player choice inside the Crack branch.

**Six Phase-1 one-shot canvases collapse to four repeatable shells (kitchen scene, office scene, living-room hub, back-porch hub) plus one true one-shot (the Crack moment, which lives as a branch inside the office scene per the doctrine — not a separate canvas).** This is the per-NPC inventory shrink the redesign delivers.

### Counters and one-time guards used by Frank's chain

- **Counters** (numeric, increment on scene completion):
  - `frank.bookkeeping_count` — increments on bookkeeping activity completion. Gates Stage 0 → 1.
  - `frank.tease_count` — increments on each tease cascade firing. Gates Stage 2 → 3.
  - `frank.chore_count` (optional) — tracks supervision compliance. May gate within Stage 2.
- **One-time guards** (boolean, set once):
  - `frank_caught` — set inside living-room evening branch. Gates the catch from re-firing.
  - `frank_restrict_declared` — set on catch resolution. Used by every post-catch cascade branch.
  - `frank_cracked` — set inside office scene Stage-3 deepest tier. Gates the Crack branch from re-firing.
  - `frank_keep_route_<x>` — set on player choice inside the Crack branch. Gates per-route content.
- **Helper functions** (composite gates per master spec §2.6):
  - `frank_stage_1()` = `frank.trust >= 20 AND frank.bookkeeping_count >= 3`
  - `frank_stage_2()` = `frank_stage == 2 AND frank_restrict_declared` (mostly identity for cleanliness)
  - `frank_stage_3()` = `corruption >= 50 AND frank_restrict_declared AND frank.arousal >= 30 AND frank.tease_count >= N`
  - `frank_stage_4()` = `frank_cracked == true`

Tuning Frank's pacing means editing the helper. Cascade gates throughout the codebase reference the helper, not the raw threshold.

---

## Cross-NPC stage interactions

Placeholder for next round. Three known cases that will need explicit treatment when Ryan/Jake/Diana/Marge/Cookie chains are authored:

1. **Ryan's Big-deal close requires `corruption >= 75`,** which is the same axis Frank's Stage 3 sits on. The two arcs share the corruption stat but have independent stage flags. Open question: does Ryan's Big-deal force Frank's Stage 3 to be reachable, or are they independent? Likely independent.
2. **Jake's Hand requires `corruption >= 50`,** overlapping Frank's Stage-3 gate. Same independence question.
3. **The Crack moments (Frank Crack, Beach proposal, Jake Hand) are mutually-aware in the design book.** A player who lands all three must see the keep-route choices as informed by what already happened with the other NPCs. Mechanism is read-only flag references in keep-route branches; will be specified per-NPC in the next round.

These are not yet authored. They are flagged here so they aren't forgotten.

---

## Other NPCs — stubs (next round)

Each NPC follows the Frank template. Full chains are deferred. What's known from the master spec §6:

### Ryan — `ryan_stage = 0..4`
- Stage 0 — First encounter at hub_yard.
- Stage 1 — Help tier open (`ryan_help_tier_open`, gated by trust + group_settled_in). Small-ticket close scenes.
- Stage 2 — Partner (corruption >= 25 + partner_invitation event). Mid-ticket closes.
- Stage 3 — Big deal (corruption >= 75 + big customer). Sex-included close.
- Stage 4 — Beach proposal + keep route.
- Helper functions per master spec §2.6: `ryan_stage_2()`, `ryan_stage_3()`. Lift-ready.
- **80% liftable from master spec §6 in next round.**

### Jake — `jake_stage = 0..N`
- Stage 0 — Hostile (knock silently rebuffed).
- Stage 1 — Noticed (beauty >= 50 + first-glance ambient event). No new buttons yet.
- Stage 2 — Peek/draw open (`jake_peek_draw_open`). "Lean in the doorway" tease button at hub_jakes_bedroom.
- Stage 3 — Caught + Hand. Hub transforms.
- Stage 4 — Keep route.
- **80% liftable from master spec §6 in next round.**

### Diana — `diana_stage = 0..N` (Phase 2+ deferred)
- Stage 0 — Default. Accumulator runs invisibly via `diana_awareness`.
- No Phase-1 buttons surface beyond state-pump "Help Diana" / "Sit with Mom."
- Full chain deferred per master spec §6.
- **20% liftable; this NPC needs fresh authoring in a later round.**

### Marge — clean arc, no stage chain
- Marge stays clean per design lock (master spec §6).
- hub_diner_front: "Take a shift" → diner-tier scene canvases (gated by player corruption + rep + beauty, not Marge's stage). "Talk to Marge" state-pump.
- **Treat Marge as a service NPC, not an arc NPC. No stage chain doc entry needed.**

### Cookie — minimal stage chain
- One state-pump button confirmed: "Talk to Cookie 💬."
- Specific arc progression undefined in master spec.
- **20% liftable; needs fresh authoring in a later round.**

---

## Template for adding additional NPCs (next round)

When Ryan/Jake/Diana/Cookie chains are authored in round 2, each gets a section with:

```
### NPC name — `<npc>_stage = 0..N`

#### Stage table
| Stage | Name | Gate | Advancing trigger | Content unlocked |
|---|---|---|---|---|

#### What this looks like to the player
[Narrative walk-through of what changes per stage]

#### Where stages get advanced (audit)
| Transition | Where the flag flips | Mechanism |
|---|---|---|

#### Stage-content cross-reference
| Stage | Surface 1 | Surface 2 | ... |
|---|---|---|---|

#### What's deliberately NOT in this chain
[Explicit list of one-shot canvases that fold into branches]

#### Counters, one-time guards, helpers
- counters
- guards
- helpers

#### Cross-NPC notes
[References to interactions with other NPCs' stages]
```

Frank's section above is the canonical worked example. Other NPCs match its shape.

---

## Cross-references

- **`01_Repeatable_First_Doctrine.md`** — vocabulary (stage, cascade, repeatable, one-shot) defined.
- **`04_Scene_Cascade_Pattern.md`** — implements Frank's Stage 0/1/2/3/4 branches inside `kitchen_with_frank` and `office_with_frank` scenes.
- **`05_Hub_and_Location_Specs.md`** (deferred) — uses Frank's stage table to specify which buttons appear at which hub at which stage.
- **`06_One_Shot_Inventory.md`** (deferred) — confirms that no canvas in Frank's chain is a true one-shot. The Crack and the catch live as branches inside repeatable shells.
- **`07_Journal_Display_Spec.md`** (deferred) — journal entries fire on Frank's stage transitions (0→1, 1→2, etc.) by reading the stage flag.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §6** — original Frank arc table; this doc lifts it and restructures around the doctrine.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §2.6** — stage helpers pattern; this doc names the specific helpers Frank uses.

---

## What this doc is not

It is not the implementation of any cascade. (That's `04_Scene_Cascade_Pattern.md`.) It is not the hub button spec. (That's `05_Hub_and_Location_Specs.md`, deferred.) It is not the journal spec. (That's `07_Journal_Display_Spec.md`, deferred.) It is not the TOML schema spec — flag and helper names are illustrative; the schema PR finalizes them.

It is the per-NPC arc skeleton. Frank in full; the others scaffolded. The next authoring round fills in Ryan, Jake, Diana, and Cookie following the Frank template.
