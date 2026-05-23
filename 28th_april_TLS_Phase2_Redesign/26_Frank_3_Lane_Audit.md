# 26 — Frank 3-Lane Audit (RTS doctrine vs shipped TLS Frank content)

> **Status:** In progress (Lane 1 complete, Lane 2 + Lane 3 pending). Authored 2026-05-11.
> **Purpose:** Structural audit of the shipped Frank Lane 1 / 2 / 3 content (Passes 1+3+4+5+6+7) against RTS source doctrine. Identify drifts, doctrine matches, gaps, and decide where to remediate.
> **Method:** Trust the canonical RTS docs (21 / 22 / 24) for source-of-truth. Re-read shipped TLS TOML directly (no Pass-completion summaries). Per-lane: pattern table + quantity table + prose verdict + exploration recommendation. Trust-but-verify; live-play RTS only if a lane's docs feel under-covered.
> **Scope:** Frank only. Cross-NPC (Ryan/Jake/Diana) out of scope.
> **Source:** `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` + `22_RTS_Cross_NPC_Mechanism_Comparison.md` + `24_RTS_Three_Lanes_Repeatable_Activities.md`. Shipped TLS content at `games/the_long_summer_test/toml_phases/7_final_game.toml`.

---

## TL;DR (will fill as audit completes)

| Lane | Pattern match | Quantity match | Severity | Exploration needed? |
|---|---|---|---|---|
| **1 — Hub button (intentional escalation)** | Partial — Pattern E ✅, Pattern F ✅ exceeds RTS, but Pattern A missing | Menu items exceed RTS, but rendered scenes underweight | **Medium drift** (click-only tease doctrine departure) | No |
| **2 — Location-entry random (ambient)** | ❌ **Severe drift** — 81% of RTS Lane 2 is cascade-bodied; 0% of TLS Frank Lane 2 is. Cooldown mechanism also wrong. | TLS Frank has MORE surfaces (15 vs Brother's 3 / catalog-wide 16) but all are flat single-renders | **HIGH drift** — biggest structural divergence in the entire conversion | Attempted (2 agent timeouts); resolved via passage_catalog source extraction instead |
| **3 — Dispatcher inside menu activity (walk-in)** | ✅ **Faithful** — 100% cascade match (RTS 100% / TLS 100%), exceeds RTS on Pattern F refuse-path adoption | TLS 7 substitutions vs RTS 7 Brother Lane 3 surfaces — exact match by count | **LOW drift** — 1:1 vs 1:N dispatcher economy (architectural divergence, not user-visible) | No |

---

## 📋 LANE 1 AUDIT — Frank's "Intentional Escalation" Lane

### RTS Source of Truth (Brother)

Per doc 21 §3 + doc 22 §3 + doc 24 §3+§10.2.A, Lane 1 in RTS Brother = **5 of 15 surfaces (33%)**:

| # | RTS Scene | Pattern | Words | Stat gate | Where gate sits | Media |
|---|---|---|---:|---|---|---|
| 1 | `BrotherBedroomTease` | **A — single-render utility** | 69 | corr ≥ 5 | At hub button | 5-image rotation pool |
| 2 | `BrotherBedroomFlash` | **A — single-render utility** | 93 | corr ≥ 5 | At hub button | 11-image rotation pool |
| 3 | `BrotherBedroomSex1` | **E — linear cascade** | 811 | None in scene; gate at hub button | At hub button (`getCorruptionLevel() >= 3 + getArousal() > 0`) | 13 video stubs across cascade |
| 4 | `BrotherBedroomPregnantSex1` | **E — variant** | 523 | Pregnancy flag | At hub button | 9 video stubs |
| 5 | `SleepingBrother` | **D — top-of-cascade gate** | 527 | relation ≥ 10 (LN only) | At hub button (visibility) + top of cascade (rejection variant) | 11 video stubs |

**Lane 1 vocabulary** per doc 24 §10.2.A: relational (Talk) / self-display (Tease, Flash) / consummation (Sex 1 variants) / late-game intimacy (Sleep with him).

**Crucial RTS shape:** Lane 1 surfaces are **rendered passages** — Player clicks Tease → loads `BrotherBedroomTease` passage → reads 69w + sees random image from pool + stat tick on render + returns via button.

### TLS Frank Lane 1 — What Shipped

| Surface | Hub | Pattern | Render | Stat gate | Pre-Pass-3? |
|---|---|---|---|---|---|
| **Office hub** menu items | | | | | |
| Help with bookkeeping (pre-catch) | Office | Hub→sub-canvas | Yes (`activity_bookkeeping_with_frank`) | `frank_offered_bookkeeping + !frank_caught` | Existing |
| Help with bookkeeping (post-catch) | Office | Hub→sub-canvas | Yes (`scene_franks_office_supervised`) | `frank_offered_bookkeeping + frank_caught` | Existing |
| Talk 💬 | Office | Hub→sub-canvas | Yes (`activity_talk_to_frank`) | None | Existing |
| **Lean over desk** 🆕 | Office | **CLICK-ONLY** (targetType=trigger) | ❌ No render | corr ≥ 5 | **Pass 3** |
| **Stretch when standing** 🆕 | Office | **CLICK-ONLY** | ❌ No render | corr ≥ 5 | **Pass 3** |
| **Sit on edge of desk** 🆕 | Office | **CLICK-ONLY** | ❌ No render | corr ≥ 5 | **Pass 3** |
| Bend over the page ❤️‍🔥 | Office | Hub→sub-canvas | Yes (`scene_office_after_crack` Pattern E+F) | `frank_cracked + frank_restrict_declared` | Existing |
| Take the receipts | Office | Exit | n/a | None | Existing |
| **Bedroom hub** menu items | | | | | |
| Talk 💬 | Bedroom | Exit + stat | ❌ No render (location exit) | None | Existing |
| Get into bed 🛏️ | Bedroom | Hub→sex loop | Yes (`loop_franks_bedroom_sex`) | None | Existing |
| Undress for him ❤️‍🔥 | Bedroom | Hub→sex loop w/ +3 pre-arousal | Yes (routes to loop) | corr ≥ 30 | Existing |
| **Sit on edge of bed and wait** 🆕 | Bedroom | Hub→sex loop w/ +5 pre-arousal | Yes (routes to loop) | corr ≥ 50 | **Pass 3** |
| **Open your robe slowly** 🆕 | Bedroom | Hub→sex loop w/ +8 pre-arousal | Yes (routes to loop) | corr ≥ 70 | **Pass 3** |
| Goodnight | Bedroom | Exit | n/a | None | Existing |

**Plus 6 pre-existing tease items** in other surfaces (kitchen Brush past / dinprep Reach for plate / hallway Linger in robe / radio Sit on rug / porch Sit on railing / office supervised Lean against desk). All **CLICK-ONLY** — no rendered scenes.

**Total Lane 1 menu items across Frank's hubs + Lane 2 distributions: ~13** (10 in hubs + 6 ambient tease distributions, some overlap).

**Total rendered Lane 1 SCENES: 4** (`activity_bookkeeping_with_frank` + `scene_franks_office_supervised` + `activity_talk_to_frank` + `scene_office_after_crack` + multi-node bedroom sex loop counted as 1).

### Pattern × Quantity Comparison Table

| Dimension | RTS Brother Lane 1 | TLS Frank Lane 1 | Verdict |
|---|---|---|---|
| **Total surfaces** | 5 rendered scenes | 4 rendered scenes + ~11 click-only menu items | **Different shape** — same density via different mechanism |
| **Pattern A (single-render tease/flash)** | 2 (Tease 69w + Flash 93w) | **0** | ❌ **DRIFT** — TLS chose click-only distribution; zero rendered Pattern A scenes for Frank |
| **Pattern E (hub-gated sex cascade)** | 2 (Sex1 811w + PregSex1 523w) | 2 (`scene_office_after_crack` + `loop_franks_bedroom_sex`) | ✅ **MATCH** — both express via cascade primitive |
| **Pattern F (branching cascade)** | 0 (Brother doesn't have one) | 1 (`scene_office_after_crack` has Pattern F refuse fork) | ✅ **EXCEEDS** RTS Brother (matches Marcus ParkDate / Edward DM doctrine) |
| **Pattern D (top-of-cascade gate)** | 1 (SleepingBrother) | 0 | ❌ **DRIFT** — Frank has no "low-stat rejection variant + high-stat full cascade" Lane 1 scene |
| **First-tease threshold** | corr ≥ 5 (Tease/Flash) | corr ≥ 5 (office Pass 3 items) | ✅ **MATCH** — exact threshold |
| **Sex threshold** | corr ≥ 3 + arousal > 0 (Sex 1) | `frank_cracked + frank_restrict_declared` capstone-gated (Bend over) | ⚠️ **DIVERGENT MECHANISM** — RTS uses stat thresholds; TLS uses capstone flag (which is itself stat-gated at corr 35). Equivalent in effect, different shape. |
| **Late-game intimacy** | Sleep with Brother (relation ≥ 10, LN only) | None directly equivalent | ❌ **GAP** — no "spend the night" surface |
| **Hub menu item count** | 5-6 max (Brother bedroom) | 6 office + 6 bedroom = 12 | ✅ **EXCEEDS** — TLS Frank has DENSER menus |
| **Media variety per scene** | 5-11 image pool per Tease/Flash | No media on click-only items; scene-level media on rendered | ❌ **DRIFT** — no per-click replay variety mechanism |
| **Replay variety** | Random image rotation per click | None on tease items; loop randomness on sex | ❌ **DRIFT** for tease items |

### Prose Audit — What This Actually Means

**The big finding: Pass 3's Lane 1 tease items are structurally underweight compared to RTS.**

RTS Brother's `BrotherBedroomTease` is a tiny 69-word passage but it IS a passage — Maya clicks Tease, the screen reloads with a heading ("You give a little show to your Stepbrother"), one of 5 images renders, stat ticks fire, return button shows. The narrative beat exists. The player gets **acknowledgment** that something happened.

TLS Frank's `Lean over the desk to read the receipts.` ships as `targetType = "trigger"` — Maya clicks, stat ticks fire, the engine re-evaluates triggers, and either Maya re-enters the office setter (Frank's still there) or lands at the bare hallway. **There is no rendered narrative beat.** No prose says "Frank's pen pauses." No image. No "Maya, eyes on the receipts, asking what this column means" — just the click text, then back to where she was.

This is documented as a deliberate choice ("Click-only doctrine documented" per Pass 3 memory) but **it costs us the RTS texture**. The 6 existing pre-Pass-3 tease items have the same problem — kitchen "Brush past him at the coffee maker" gives no scene, just stat ticks.

**Where Frank's Lane 1 IS strong:**

- **Office Pattern E+F**: `scene_office_after_crack` is the canonical RTS Brother Sex1 equivalent done well — cascade body, Pattern F refuse fork. This is doctrine-matching.
- **Bedroom sex loop**: multi-node loop hub is a TLS-original mechanism that doesn't exist in RTS (RTS just renders a single linear cascade). Arguably an improvement.
- **Threshold match**: corruption 5 for tease, exactly matches RTS.
- **Pre-arousal carryover ladder** (corr 30 → +3, corr 50 → +5, corr 70 → +8 on the bedroom items): this is mechanically clever and doesn't exist in RTS — it gives a stat-tiered "intensity of intent" gradient. **TLS-original but rhymes with RTS-doctrine spirit.**

**Where Frank's Lane 1 has real gaps:**

1. **No rendered Pattern A tease/flash scenes.** ~11 click-only tease items across Frank's surfaces, ZERO rendered. RTS's player feels the show happened; TLS's player feels stats moved.
2. **No "Sleep with him" terminal intimacy beat.** Frank has bedroom hub access at Stage 4, but no separate "fall asleep next to him" Lane 1 surface that's distinct from the sex loop. This is an LN-band scene RTS specifically reserves.
3. **No replay variety mechanism on tease items.** RTS uses image-pool randomization to give per-click variety. TLS click-only items are identical every time.
4. **No exhibitionism-explicit (Flash equivalent).** RTS Brother has separate Tease (suggestive) and Flash (explicit show) at the same corr 5 threshold — two flavors of self-display. TLS has 3 office tease items but they're all "lean / stretch / sit" — same suggestive register, no exhibitionist register.

### Verdict

**Lane 1: Partial doctrine match with one significant drift.**

- ✅ **Pattern E (sex cascade)**: faithful — office after-crack + bedroom sex loop are doctrine-matching
- ✅ **Pattern F (branching)**: faithful — refuse path in office is RTS-shape
- ✅ **First-tease threshold (corr 5)**: exact match
- ✅ **Menu density**: equals or exceeds RTS Brother
- ❌ **Pattern A (tease/flash render)**: missing — 11 click-only items where RTS has 2 rendered scenes. This is the documented "click-only doctrine" divergence but it's the BIGGEST Lane 1 drift.
- ❌ **Late-game intimacy (Sleep with him)**: missing — no LN-band terminal intimacy surface
- ⚠️ **Replay variety**: missing — no per-click image pool / text variation on tease items
- ⚠️ **Exhibitionism register (Flash)**: missing — all 3 office teases are "suggestive proximity" register, none is overt show

### Exploration recommendation for Lane 1

**Not needed.** RTS Lane 1 is the most-documented lane — docs 21 + 22 walked all 5 Brother surfaces with source extracts. Adding live-play of Tease/Flash would just confirm what's already known (the rendered scenes exist, they're thin, they use image rotation).

The drift is well-understood. The decision is **whether to fix the click-only divergence** (promote tease items to rendered Pattern A scenes with image pools) or **explicitly accept it** as a TLS doctrine departure.

### Candidate fixes (for later decision)

| Fix | Effort | What it buys |
|---|---|---|
| Promote 3 office Pass-3 tease items to rendered Pattern A canvases (each ~80w, 1 image, return) | ~3-4 hr | Closes the biggest Lane 1 drift; gives player narrative ack on tease clicks |
| Promote the 6 existing pre-Pass-3 tease items to rendered Pattern A canvases | ~6-8 hr | Same as above but fuller-coverage; converts 6 silent stat-ticks into 6 short beats |
| Add 1 dedicated Flash equivalent at corr 5 (e.g., bedroom or bathroom mirror tease) | ~1-2 hr | Closes the exhibitionism-register gap |
| Add 1 Sleep-with-Frank terminal intimacy surface (Stage 4 LN, post sex-loop) | ~2-3 hr | Closes the late-game intimacy gap |
| Add image-pool randomization to existing rendered scenes | ~1 hr engine + asset work | Closes replay variety gap |

---

## 📋 LANE 2 AUDIT — Frank's "Ambient World-Presence" Lane

### Method note

The plan called for a 45-minute live RTS exploration session. **Two consecutive Sonnet agents timed out** (stream/connection errors after ~11 minutes each), neither completing the planned phases. Pivoted to **source extraction from `game_explorations/rts-arc-trace/passage_catalog.json`** — a frozen 361-passage dump from RTS v0.25 (captured 2026-04-29). All Lane 2 findings below are source-verified by direct parse of RTS location-passage code. Live-verification of three specific Lane 2 scenes (PeepBrotherSex Pattern C, BrotherCaughtMasturbating Pattern D, BedroomGrope Pattern A) was previously done in doc 22 §11 (2026-05-06).

### RTS Source of Truth — full 16-scene catalog

**Mechanism in source:** RTS Lane 2 fires via `<<goto "SceneName">>` inside an `<<if random(1,N) == 1 && conditions>>` block at the **end** of a location passage. The passage renders normally OR (on dice hit + conditions met) gets substituted with the Lane 2 scene. Most use a stored-roll pattern `<<set $game.random = random(1,4)>>` then `<<if $game.random == 1>>` for multi-target dispatch from a single roll.

| # | Scene | Location | Words | LR | Media | Pattern | `previous()` gate | `executedToday` cooldown | NPC presence gate |
|---|---|---|---:|---:|---:|---|:-:|:-:|:-:|
| 1 | `PeepBrotherSex` | BrotherBedroom | 211 | 4 | 9 | **C — short cascade** | ✅ | ✅ | ✅ |
| 2 | `BrotherCaughtMasturbating` | BrotherBedroom | 317 | 10 | 11 | **D — top-gate cascade** | ✅ | ✅ | ✅ |
| 3 | `BedroomGrope` | Bedroom (Maya's) | 21 | 0 | 5 | **A — single-render** | ✅ | — | ✅ (Dad OR Brother) |
| 4 | `SellingMyStepsister` | Bedroom (Maya's) | 186 | 18 | 16 | **E/F — long cascade w/ branch** | ✅ | — | ✅ |
| 5 | `DadShowerSex` | Bathroom | 297 | 9 | 13 | **D — cascade** | ✅ | ✅ | ✅ (Dad in Bathroom) |
| 6 | `DadShowerSexPregnant` | Bathroom | 181 | 7 | 7 | **D — cascade variant** | ✅ | ✅ | ✅ |
| 7 | `DadPeepSex` | Bathroom | 268 | 9 | 8 | **D — cascade** | ✅ | ✅ | ✅ |
| 8 | `DadPeepSexBedroom` | DadBedroom | 159 | 10 | 11 | **E — cascade** | — | ✅ | ✅ (Dad in Bedroom) |
| 9 | `GrandpaShowerSex` | Bathroom | 177 | 14 | 14 | **D — cascade** | ✅ | ✅ | ✅ |
| 10 | `GrandpaKitchenSex` | Kitchen | 164 | 11 | 12 | **E — cascade** | — | — | ✅ (Grandpa in Kitchen) |
| 11 | `XCamBlackmail` | Hallway | 215 | 16 | 17 | **E — cascade** | ✅ (from Residential) | — | — (story flag gated) |
| 12 | `GarageDrunk` | Hallway | 194 | 13 | 12 | **E — cascade** | ✅ | — | — |
| 13 | `TyreFixSex` | Garage | 241 | 16 | 16 | **E — cascade** | — | — | — (quest-gated) |
| 14 | `BathroomLactation` | Bathroom | 23 | 1 | 7 | **B/C — 1-beat reveal** | ✅ (!= self) | — | — (pregnancy) |
| 15 | `BathroomMorningSickness` | Bathroom | 42 | 0 | 0 | **A — single-render** | — | — | — (pregnancy) |
| 16 | `BathroomBellyAwareness` | Bathroom | 49 | 0 | 0 | **A — single-render** | — | — | — (pregnancy) |

**Aggregate stats:**
- **13 of 16 (81%) are cascade-bodied** (≥4 linkreplace beats — Patterns B'/C/D/E/F)
- **3 of 16 (19%) are single-render Pattern A** — but ALL three are tiny utility/notification beats (pregnancy info or 21-word grope flash), not the canonical "ambient encounter" content
- Average prose: 172 words per scene
- **`previous()` gate (fires only on fresh hub-entry): 13 of 16 = 81%** — the implicit cooldown mechanism
- **`executedToday` daily cooldown: 7 of 16 = 44%** — explicit per-scene daily cap
- **NPC presence gate: 11 of 16 = 69%** — encounter only fires when NPC is plausibly at the location
- **Stored-roll dispatch pattern** (`<<set $game.random = random(1,4)>>` then branch by value) lets one dice roll dispatch among multiple candidates

### TLS Frank Lane 2 — What Shipped (15 canvases)

**Mechanism in TOML:** `trigger_mode = "random"` + `chance` value on a canvas with `npc = "npc_frank"`. The engine's `checkRandomEncounters` rolls per location entry. Lane 2 fires substitute the location's hub render. Body branching via `[group]` blocks with mutually-exclusive conditions.

| # | Canvas | Loc | Schedule | Chance | Prose words | `[group]` tiers | Cascade? | Daily cooldown? | Pre-Pass-4? |
|---|---|---|---|---:|---:|---:|:-:|:-:|---|
| 1 | scene_hallway_frank_pass | hallway | N (21:30-23:00) daily | 0.30 | 115 | 3 | ❌ | ❌ | Existing |
| 2 | scene_hallway_franks_door_evening | hallway | N | 0.40 | 87 | 0 | ❌ | ❌ | Existing (Stage-4 polish 2026-05-06) |
| 3 | scene_kitchen_frank_coffee_alone | kitchen | EM | 0.35 | 217 | 3 | ❌ | ❌ | Existing |
| 4 | scene_living_room_frank_radio | living_room | aft 14-16 | 0.25 | 410 | 5 | ❌ | ❌ | Existing |
| 5 | scene_porch_frank_evening_smoke | back_porch | evening 18:30-18:59 | 0.40 | 361 | 5 | ❌ | ❌ | Existing |
| 6 | scene_kitchen_late_night_raid | kitchen | N | **1.0** | 328 | 2 | ❌ | ❌ | Existing |
| 7 | scene_yard_frank_mending_fence | yard | aft 14-16 | 0.30 | 123 | 3 | ❌ | ❌ | Existing |
| 8 | scene_living_room_frank_evening_paper | living_room | pre-dinner 17-17:59 | 0.25 | 151 | 3 | ❌ | ❌ | Existing |
| 9 | scene_kitchen_frank_afternoon_alone | kitchen | Wed/Sat 14-15 | 0.20 | 77 | 1 | ❌ | ❌ | Existing |
| 10 | scene_office_frank_diana_call_intercept | office | wkdy eve | 0.25 | 81 | 0 | ❌ | one-time mutex | Existing |
| 11 | scene_hallway_frank_late_drink | hallway | N | 0.25 | 75 | 0 | ❌ | one-time mutex | Existing |
| 12 | scene_hallway_frank_morning_pass | hallway | wkdy M 08-09 | 0.30 | 313 | 5 | ❌ | ❌ | **Pass 4** |
| 13 | scene_living_room_frank_dusk | living_room | wkdy 18-18:30 | 0.30 | 287 | 5 | ❌ | ❌ | **Pass 4** |
| 14 | scene_back_porch_frank_weekend_morning | back_porch | wkend 06:30-08 | 0.40 | 352 | 5 | ❌ | ❌ | **Pass 4** |
| 15 | scene_yard_frank_late_afternoon | yard | aft 16-17 | 0.25 | 301 | 5 | ❌ | ❌ | **Pass 4** |

**Aggregate stats:**
- **0 of 15 (0%) are cascade-bodied** — every TLS Frank Lane 2 surface is single-render
- 100% use `[group]` tier branching (1-5 tiers per canvas) gated on Frank.trust + capstone flags
- Average prose: **219 words per scene** (HIGHER than RTS's 172w average — but with no cascade pacing)
- Chance% range: 0.20-0.40 (one outlier at 1.0 — `late_night_raid` is deterministic)
- **`previous()`-equivalent gate: 0 of 15** — TLS has no "only-fires-on-fresh-hub-entry" mechanism
- **Per-canvas daily cooldown: 2 of 15** — and those are one-time-per-arc mutex flags, not daily caps
- **Global Layer-3 cooldown: applies to all 15** — 3-visit per-location quiet period after ANY random fires (engine-wide, not per-canvas)
- **NPC presence gate: implicit** via NPC scheduling — Frank's `[canvases.trigger]` with `npc = "npc_frank"` only fires when his schedule places him at that location (matches RTS effect)

### Pattern × Quantity Comparison Table

| Dimension | RTS Lane 2 (16-scene catalog) | RTS Brother Lane 2 (3 scenes) | TLS Frank Lane 2 (15 canvases) | Verdict |
|---|---|---|---|---|
| **Total surfaces** | 16 across 7 locations | 3 (PeepSex / Caught / Grope) | 15 across 5 locations | ⚠️ TLS exceeds Brother by 5x but with different structure |
| **Cascade-bodied %** | **81%** (13/16) | **67%** (2/3) | **0%** (0/15) | ❌ **MASSIVE DRIFT** — biggest structural divergence in entire conversion |
| **Single-render %** | 19% (mostly pregnancy/utility) | 33% (BedroomGrope only) | 100% | ❌ TLS shipped 15 single-renders where RTS has 0 ambient single-renders |
| **Avg prose words** | 172w | 183w | **219w** | ⚠️ TLS HAS the words — they're just not arranged as cascades |
| **`previous()` gate (anti-toggle cooldown)** | 81% (13/16) | 100% (3/3) | **0%** (0/15) | ❌ Missing — TLS rolls chance% on every entry, including sub-passage returns |
| **`executedToday` daily cooldown** | 44% (7/16) | 67% (2/3) | 13% (2/15 — one-time mutex only) | ❌ TLS has no per-canvas daily cap mechanism for ambient set |
| **Global Layer-3 cooldown (3-visit)** | None observed | None | 100% (engine-wide) | ⚠️ TLS uses a different — broader — cooldown |
| **NPC presence gate** | 69% | 100% (Brother location check) | 100% (via schedule) | ✅ MATCH (different mechanism, same effect) |
| **Stored-roll multi-dispatch** (`$game.random == 1` / `== 2` from one roll) | Yes (BrotherBedroom, Bathroom) | Yes (Peep + Caught share roll) | No — independent chance% per canvas | ❌ Architectural difference |
| **Per-tier prose escalation** | Inside cascade beats (Pattern C/D) | Inside cascade beats | Via `[group]` tier branches | ⚠️ Equivalent purpose, very different shape |
| **Capstone-flag tier branching in body** | Not used in Lane 2 (gates are stat/relation/scene-flag based) | Not used | Heavy use (`frank_caught`, `frank_restrict_declared`, `frank_cracked`, `frank_invited_to_bedroom`) | ⚠️ TLS innovation — RTS doesn't gate Lane 2 body by capstone flags |
| **Chance% values** | random(1,2-5) = 20-50% per fire | random(1,2-4) = 25-50% per fire | 0.20-0.40 (+ one 1.0 deterministic) | ✅ MATCH on range |

### Prose Audit — What This Actually Means

**The big finding: RTS Lane 2 is a fundamentally different mechanism than TLS Frank Lane 2 shipped.**

In RTS, when Maya walks into BrotherBedroom from the Hallway, the engine rolls one dice (`<<set $game.random = random(1,4)>>`) and 25% of the time substitutes `PeepBrotherSex` (a 211-word, 4-linkreplace cascade — player clicks "Peep" → "Stroke your pussy" → "Masturbate" → "Cum!", each gated on stats). 25% of the time substitutes `BrotherCaughtMasturbating` (317w, 10 LR — top-of-cascade gate at corruption ≥ 3 opens a sex cascade, otherwise rejection variant). 50% renders the normal hub. Once a scene fires that day, it's locked out via `!executedToday`. Re-entering BrotherBedroom from the menu (after clicking Tease and returning) doesn't re-roll — `previous() == "Hallway"` gates that.

In TLS Frank, when Maya walks into the hallway at 21:30, the engine rolls `chance = 0.30`. If hit, renders `scene_hallway_frank_pass` — a 115-word single-render with `[group]` tier branching (3 tiers: low/mid/high Frank.trust). Same prose layout every fire within a tier. No click-through cascade. No daily cap on this specific canvas. After the random fires, the 3-visit global cooldown blocks ANY Lane 2 at hallway for the next 3 visits.

**The shapes do different things:**

- **RTS cascade** gives a click-paced "the encounter develops" feel. Each click is a beat in real time. Maya gets to bail at any beat (return button persists). The cascade body is ~200-300 words but the player only sees 30-50 at a time. Stat gates inside cascade mean low-corruption Maya sees 2 beats then a rejection ("I should get out of here..."); high-corruption Maya sees 4 beats to climax.

- **TLS group-branched single-render** gives a "current state's tier renders all at once" feel. Player reads ~219 words top-to-bottom. The current tier prose fires fully; other tiers' prose isn't shown. No replay variety within a tier — same words every time.

**Where Frank's Lane 2 IS strong:**

- **Quantity coverage**: 15 surfaces across 5 home locations (vs Brother's 3 across 2 locations). TLS Frank has DENSER ambient scheduling — Frank shows up in more times/places.
- **Word count per canvas exceeds RTS**: 219w avg vs 172w. The PROSE is there.
- **Tier branching by NPC trust + capstone flag**: TLS innovation. RTS Lane 2 doesn't have post-catch register branching in ambient encounters; TLS does. Post-restrict Frank ambient prose reads differently from pre-catch register — a doctrine-positive feature.
- **NPC schedule gating**: Frank's `npc = "npc_frank"` field + scheduled canvases means Lane 2 only fires during his actual location/time windows. Equivalent to RTS's `GetNpcLocation()` check.
- **Chance% range matches RTS** (20-40% per fire).

**Where Frank's Lane 2 has serious gaps:**

1. **Zero cascades.** This is the dominant RTS Lane 2 pattern (81%). Every TLS Frank Lane 2 surface ships as flat single-render. The "encounter develops in clicks" texture doesn't exist in TLS Frank.
2. **No `previous()` gate equivalent.** TLS Lane 2 rolls chance% on every location entry — INCLUDING re-entries from sub-passages. Player could exit a setter → re-enter location → re-roll Lane 2. RTS prevents this by `previous() == "Hallway"` requirement.
3. **No per-canvas `executedToday` daily cooldown.** Once a Frank ambient fires today, the SAME canvas can fire again that day (subject only to the 3-visit global cooldown). RTS's 44% of Lane 2 surfaces have explicit daily caps preventing this.
4. **No stored-roll multi-dispatch.** TLS evaluates each Lane 2 canvas's chance% independently. RTS's `<<set $game.random = random(1,4)>>` pattern lets one dice cover N candidates at the same location — economical and ensures only ONE Lane 2 fires per entry.
5. **No mid-cascade stat gates.** Pattern C ("come back when corruption higher to see deeper beat") is impossible in TLS Frank Lane 2 because there are no cascade beats to put gates between. Replay value within a single ambient surface is zero — tier-branching gives different prose at different stat levels but doesn't gradually reveal more content per click.
6. **No threshold notification on rejection.** RTS Lane 2 cascade gates publish `NotifyCorruption(N)` when player can't proceed at a beat — telling player "do X to unlock more." TLS Frank Lane 2 has no rejection-variant mechanism because there's nothing to reject at.

**Doctrine claim refutation (doc 24 §8.1):** The audit doc claimed "RTS lane 2 truly has zero cross-attempt cooldown — each entry rolls fresh." This is **wrong by source.** RTS uses TWO cooldown mechanisms simultaneously: `previous()` gate (only-fresh-hub-entry) covering 81% of Lane 2 fires + `executedToday` (per-scene daily cap) covering 44%. TLS's 3-visit global cooldown is a DIFFERENT mechanism (broader scope, no per-scene granularity) — not "stricter than RTS," just structurally different. Doc 24 §8.1 should be revised.

### Verdict

**Lane 2: SEVERE drift — biggest structural divergence in the entire Frank conversion.**

- ❌ **Cascade structure**: 0% TLS vs 81% RTS. This is the dominant Lane 2 pattern doctrine-wide and is entirely absent in TLS Frank.
- ❌ **Cooldown mechanism**: TLS shipped a different shape (global 3-visit Layer 3) where RTS uses `previous()` + `executedToday`. Not "missing" — wrong.
- ❌ **No mid-cascade stat gates** (Pattern C). The "come back when stats higher to see more" loop within a single Lane 2 scene is impossible in TLS Frank.
- ❌ **No stored-roll multi-dispatch**. Each TLS canvas evaluates independently.
- ✅ **Surface quantity**: 15 vs 3 — TLS exceeds Brother
- ✅ **Average word count**: 219 vs 172 — TLS has the prose
- ✅ **Tier branching by capstone flag**: TLS innovation that RTS doesn't have (post-catch register in ambient body)
- ✅ **Chance% values**: in range
- ✅ **NPC schedule gating**: equivalent

**The good news: cascade primitive already ships in TLS.** Pass 7 of the original Frank conversion used cascades for Lane 1 high-content scenes (kitchen morning cascade, office crack, office after crack, bedroom anchor). The engine supports `type = "cascade"` blocks with `beats` array, per-beat effects, mid-cascade gates, and `show_when_locked` siblings. The work to retrofit Lane 2 isn't an engine project — it's a content rewrite.

### Candidate fixes

| Fix | Effort | Severity addressed | What it buys |
|---|---|---|---|
| Promote 3-4 top TLS Frank Lane 2 surfaces to cascades (e.g., `late_night_raid`, `office_diana_call_intercept`, `living_room_radio`, `kitchen_with_frank_morning`) | ~6-8 hr | Cascade-structure drift | Most click-feel impact — these are the canvases with the richest prose that would benefit most |
| Add `previous_in` filter to TLS Lane 2 trigger condition (only fire on hub-entry, not sub-passage returns) | ~1 hr engine + 15 min TOML | Anti-toggle cooldown drift | Close the "spam the bathroom for Lane 2" exploit |
| Add per-canvas `daily_cap` on each Lane 2 canvas (`max_triggers_per_day = 1`) | 15 min TOML | Daily cap drift | Match RTS's `executedToday` doctrine |
| Add `NotifyCorruption(N)`-equivalent threshold messages when Lane 2 fires at low stat (rejection variant inside the cascade) | ~2 hr per converted cascade | Mid-cascade gate drift | Restore the "do X to see deeper" replay loop |
| Add stored-roll dispatcher at hub locations (1 roll → branches to N candidates) | ~3 hr engine + 30 min TOML per hub | Stored-roll architectural drift | Match RTS economy of dice + ensure only one Lane 2 fires per entry |
| Promote ALL 15 Frank Lane 2 surfaces to cascades | ~30-40 hr | Full cascade parity | Full RTS Lane 2 doctrine match — biggest content lift in the audit-fix work |
| Tune global Layer-3 cooldown from 3 visits → 0 (rely on per-canvas + previous() gates instead) | 1 line engine change | TLS over-throttling per doc 24 §8.1 self-flag | Allow denser Lane 2 firing rate when other cooldowns mature |

### Exploration recommendation — retrospectively

The plan called for full RTS live-play. Two agents timed out; the audit pivoted to source extraction. **Verdict: source extraction was sufficient and the audit reached HIGH confidence without the live session.** The cascade-experience question was already answered in doc 22 §11 (2026-05-06 live verification of Patterns D + E + F). The remaining questions (density, cooldown semantics, cross-NPC) are all answerable from passage source — and indeed yielded sharper data than live-play would have (full 16-scene catalog vs whatever a 45-min walk-through would have caught). The live-play approach was over-spec'd for this audit.

For future audits, consider: source-first if `passage_catalog.json` exists for the game, live-play only when behavior (UX feel, layout, animation) matters more than mechanism.

---

## 📋 LANE 3 AUDIT — Frank's "Walk-In / Dispatcher" Lane

### Method note

Same source-extraction approach as Lane 2 (live-play deemed unnecessary — doc 24 §4 already live-verified the BathroomShowerMasturbate dispatcher mechanism in 2026-05-10 session). Used the same nested-if parser from Lane 2 to extract RTS Lane 3 dispatchers from `passage_catalog.json`. TLS inventory hit one parser bug (id-regex matched `target_canvas_id` rule references instead of canvas declarations) — fixed via section-split-then-strict-id-match.

### RTS Source of Truth — full Lane 3 catalog

**Mechanism in source:** RTS Lane 3 fires from a **transient dispatcher passage** reached via an activity menu (e.g., player picks Shower → Masturbate → lands on `BathroomShowerMasturbate`). The dispatcher rolls dice (`<<set $game.dice = random(1,N)>>` or inline `random(1,N) == 1`), checks NPC conditions, and `<<goto>>`s a substitution scene OR falls through to vanilla activity body. Two stored-roll dispatchers (BedroomStudy, BathroomShowerMasturbate) handle multi-NPC dispatch from a single roll.

**4 dispatchers, 10 NPC-bound substitution targets:**

| Dispatcher | Parent activity | Target scene | Chance | NPC + stat gate | Words | LR | Pattern |
|---|---|---|---|---|---:|---:|---|
| `BathroomShowerMasturbate` | Shower → Masturbate | `BrotherShowerSex` | 1/3 = 33% | StageOneCorruption(Brother) + at home | 220 | 9 | **D/E** |
| `BedroomStudy` | Study (Maya bedroom) | `BedroomStudyDadGrope` | dice==1 = 17% | Dad arousal+corr > 0 | 26 | 8 | D/E |
| `BedroomStudy` | Study | `BedroomStudyBrotherGrope` | dice==2 = 17% | Brother arousal+corr > 0 | 13 | 1 | **B'** (1-beat reveal) |
| `BedroomStudy` | Study | `BedroomStudyBrotherGropePregnant` | dice==2 = 17% | same + pregnant | 186 | 11 | D/E |
| `BedroomStudy` | Study | `BrotherHelpStudy` | dice==3 = 17% | Brother arousal+corr > 0 | 205 | 10 | D/E |
| `WashDishes` | Wash Dishes (kitchen) | `DadWashDishesSex` | 1/3 = 33% | Dad arousal > 0 + at home | 247 | 6 | E |
| `WashDishes` | Wash Dishes | `DadWashDishesSexPregnant` | 1/3 = 33% | same + pregnant | 153 | 6 | E |
| `WashDishes` | Wash Dishes | `BrotherWashDishesSex` | 1/3 = 33% | Brother arousal > 0 + StageTwoCorruption + at home | 165 | 8 | D/E |
| `PlayingVideogame` | Playing Videogame (living room) | `PlayingGamesSex` | 1/3 = 33% | StageTwoCorruption(Brother) + Brother in LR | 299 | 11 | D/E |
| `PlayingVideogame` | Playing Videogame | `PlayingGamesSexPregnant` | 1/3 = 33% | same + pregnant | 115 | 8 | D/E |

**Aggregate stats:**
- **10 NPC-bound substitution targets across 4 dispatchers** (Brother gets 7 of these — matches doc 24 §3's Brother count exactly ✓)
- **10 of 10 (100%) are cascade-bodied** (LR ≥ 1)
- Average prose: **163 words per scene**
- **No `executedToday` daily cooldowns on Lane 3 dispatchers** (asymmetric with Lane 2's 44% cooldown rate — apparently because the player must choose the activity, so re-firing is acceptable)
- **Zero stat gates inside cascade beats** (Pattern C absent in Lane 3 — gates live at scene-entry only)
- **Zero Pattern F refuse paths** (no Accept/Decline branching cascades in any Lane 3 scene; RTS reserves Pattern F for once-per-arc story moments like SellingMyStepsister or MarcusParkDate)
- **Stored-roll multi-dispatch in 2 of 4 dispatchers** (BedroomStudy: 1 dice → 4 NPC variants; PlayingVideogame: 1 dice → 2 variants)

### TLS Frank Lane 3 — What Shipped (7 substitutions)

**Mechanism in TOML:** Per PRD 25 (engine work shipped Pass 5 with `<<set>>+<<goto>>` fix), each parent activity carries a `[[canvases.trigger.substitutions]]` block referencing target canvas slugs. On parent canvas render, engine's `setup.checkAndSubstituteCanvas` rolls dice + checks conditions + `<<goto>>`s the target. Target canvases have `substitution_only = true` (excluded from selectors). 1:1 parent-to-target ratio (each parent has exactly one substitution rule pointing to one target).

| Parent activity | Loc | Target scene | Chance | Tier | Stat gate | Words | Cascade beats | Pattern |
|---|---|---|---|---|---|---:|---:|---|
| `activity_make_tea` | kitchen | `scene_frank_passes_kitchen_door` | 0.40 | T1 PG | corr ≥ 5 + Frank.arousal ≥ 1 | 51 | 2 | **E** |
| `activity_make_coffee_solo` | kitchen | `scene_frank_arrives_during_coffee` | 0.30 | T1 | corr ≥ 10 + Frank.arousal ≥ 10 + Frank.trust ≥ 5 | 84 | 3 | **E** |
| `activity_sit_on_porch` | back_porch | `scene_frank_joins_porch` | 0.30 | T2 | corr ≥ 10 + Frank.trust ≥ 10 | 123 | 3 | **E** |
| `activity_read_on_couch` | living_room | `scene_frank_joins_couch` | 0.30 | T2 (tier-branched) | corr ≥ 10 (low tier) → ≥ 25 + Frank.corr ≥ 10 (high tier) | 239 | 4 | **E** w/ tier groups |
| `activity_wash_dishes_solo` | kitchen | `scene_frank_at_kitchen_sink_behind` | 0.20 | T3 | corr ≥ 20 + Frank.corr ≥ 10 | 347 | 3 | **F (refuse fork)** |
| `activity_brush_teeth` (Pass 7) | bathroom | `scene_frank_at_open_bathroom_door` | 0.30 | T1 | corr ≥ 5 + Frank.arousal ≥ 1 | 67 | 2 | **E** |
| `activity_masturbate_at_shower` (Pass 7, triggerless dispatcher) | bathroom | `scene_frank_walks_in_shower` | 0.33 | T3 | corr ≥ 20 + Frank.arousal ≥ 30 + Frank.corr ≥ 10 (RTS BrotherShowerSex thresholds) | 366 | 3 | **F (refuse fork)** |

**Aggregate stats:**
- **7 substitutions across 7 parent dispatchers** (1:1 ratio — no multi-dispatch)
- **7 of 7 (100%) are cascade-bodied** ✓ matches RTS
- Average prose: **182 words per scene** (slightly higher than RTS's 163)
- **2 of 7 (29%) are Pattern F with refuse path** (kitchen sink + shower walk-in) — TLS exceeds RTS Lane 3 (which has 0 Pattern F)
- **Tier ladder: 3 T1 + 2 T2 + 2 T3** — covers low/mid/high stat thresholds
- **Stat-threshold gating only** (no `executedToday` daily cooldowns) ✓ matches RTS Lane 3 doctrine
- **Substitution rules use exact RTS BrotherShowerSex thresholds for the shower walk-in** (corr 20 + Frank.arousal 30 + Frank.corr 10) — explicit doctrine port

### Pattern × Quantity Comparison Table

| Dimension | RTS Lane 3 (10 surfaces, 4 dispatchers) | RTS Brother Lane 3 (7 surfaces) | TLS Frank Lane 3 (7 substitutions, 7 dispatchers) | Verdict |
|---|---|---|---|---|
| **Total substitution scenes** | 10 (across 4 NPCs incl pregnant variants) | 7 | 7 | ✅ **MATCH** vs Brother count |
| **Cascade-bodied %** | **100%** | **100%** | **100%** | ✅ **EXACT MATCH** — opposite of Lane 2 |
| **Avg prose words** | 163w | 197w | **182w** | ✅ MATCH |
| **Pattern F refuse path %** | 0% (none in Lane 3) | 0% | **29%** (2/7) | ✅ TLS **EXCEEDS** RTS — Pattern F doctrine deeper in TLS |
| **Pattern A single-render %** | 0% (excluding 1-beat B' reveal) | 0% | 0% | ✅ MATCH |
| **Stored-roll multi-dispatch** | Yes (BedroomStudy: 1 dice → 4 variants; WashDishes: implicit 1/3 per NPC) | Yes (3 of 7 Brother surfaces share BedroomStudy roll) | **No** (1:1 parent:target) | ⚠️ **Architectural divergence** — TLS uses N parents for N targets where RTS uses 1 parent for N targets |
| **In-cascade stat gates (Pattern C)** | 0 of 10 | 0 of 7 | 0 of 7 | ✅ MATCH |
| **`executedToday` daily cooldown** | 0% (Lane 3 doesn't use this — asymmetric with Lane 2's 44%) | 0% | 0% | ✅ MATCH |
| **NPC presence gate at dispatcher** | 100% (all dispatchers check `IsNpcAtHome` or `GetNpcLocation`) | 100% | 100% (TLS via NPC schedule + canvas trigger) | ✅ MATCH (different mechanism, same effect) |
| **Stat threshold ladder** | StageOneCorruption / StageTwoCorruption (composite gates) | Same | Maya.corruption + Frank.arousal/trust/corr explicit values | ✅ MATCH (RTS uses helpers, TLS uses raw values; equivalent gates) |
| **Chance% range** | 17%-33% per fire (depending on dispatcher) | Same | 20%-40% per fire | ✅ MATCH |
| **Number of dispatchers** | 4 | 4 (Brother shares with Dad on most) | **7** (1:1 design) | ⚠️ TLS has more dispatcher canvases — content density positive |
| **Activity types covered** | Shower / Study / WashDishes / Videogame | Same | Tea / Coffee / Porch / Couch / Dishes / Brush teeth / Shower-masturbate | ✅ TLS covers different daily-routine surfaces (matches "Frank in your daily life" doctrine) |

### Prose Audit — What This Actually Means

**The big finding: Lane 3 is the FAITHFUL lane — opposite of Lane 2's drift.**

Where Lane 2 shipped 15 single-render canvases against RTS's 13/16 cascades (0% match), Lane 3 shipped 7 cascades against RTS's 10/10 cascades (100% match). The reason: Lane 3 was authored AFTER Pass 5 shipped the engine specifically for it. The PRD 25 work + Pass 6+7 content authoring deliberately targeted RTS-faithful behavior, including a critical engine fix mid-authoring (`<<set>>+<<goto>>` replacing PRD's broken `<<script>>+return`).

**TLS Frank Lane 3 is a complete RTS port with two architectural divergences and one improvement:**

**Divergences (acceptable):**

1. **1:1 parent:target ratio.** RTS uses one dispatcher (`BedroomStudy`) to handle 4 NPC-variant substitutions via `<<set $game.dice = random(1,6)>>`. TLS uses 7 separate parents (one per substitution). This is more verbose in TOML but easier to author + reason about + the engine's `[[canvases.trigger.substitutions]]` array on a single parent COULD support multi-dispatch — TLS just didn't author it that way. Not a doctrine drift; an authoring economy difference.

2. **No Maya-bedroom substitutions.** RTS `BedroomStudy` puts NPC walk-ins in MAYA's bedroom (Brother + Dad both come to Maya's room while she studies). TLS Frank doesn't visit Maya's bedroom — narrative reason (Frank's a stepfather, doesn't enter stepdaughter's bedroom uninvited). So the RTS Lane 3 grammar of "NPC enters Maya's space mid-activity" doesn't translate fully — TLS Frank Lane 3 is "Frank enters shared spaces mid-Maya-activity" (kitchen, living room, back porch, bathroom). Same mechanism, narratively-appropriate location-set.

**Improvement over RTS:**

3. **Pattern F refuse-path adoption in T3 scenes.** RTS Lane 3 has ZERO Pattern F surfaces — even the heaviest BrotherShowerSex is Pattern D (top-of-cascade gate, no fork). TLS shipped 2 of 7 (29%) as Pattern F: `scene_frank_at_kitchen_sink_behind` (Lean back / Step away) and `scene_frank_walks_in_shower` (Don't pull curtain / Pull curtain closed). The fork at peak-stakes lets player elect engagement vs decline at the climax beat. This matches the RTS doctrine in §10.5 ("Lane 3's specific structural rule worth surfacing: low-agency setup, choice-driven payoff") more precisely than RTS Lane 3 itself does. **Frank Lane 3 honors the doctrine more strictly than RTS Brother Lane 3.**

**Where Frank's Lane 3 IS strong:**
- ✅ **100% cascade structure** matches RTS exactly
- ✅ **Word count** in range (slightly above RTS avg)
- ✅ **Tier ladder** (T1/T2/T3) maps cleanly to RTS's StageOne/StageTwoCorruption helpers via raw stat thresholds
- ✅ **Pattern F refuse adoption** exceeds RTS — doctrine-positive innovation
- ✅ **Cooldown asymmetry preserved** (no daily caps on Lane 3, unlike Lane 2) — matches RTS doctrine
- ✅ **NPC presence gating** correct via NPC schedule + canvas trigger (equivalent to RTS's IsNpcAtHome check)
- ✅ **Activity coverage** spans the full daily routine (kitchen 3× / bathroom 2× / living room / back porch) — denser than RTS Brother's 4 activities
- ✅ **Substitution_only flag** correctly excludes targets from Lane 1/2 selectors per Pass 5 doctrine
- ✅ **Critical engine fix during authoring** (`<<set>>+<<goto>>` per Pass 6 memory) — discovered + corrected the PRD's `<<script>>+return` mistake
- ✅ **Live-verified end-to-end** in Pass 6 + Pass 7 playtest sessions

**Where Frank's Lane 3 has minor gaps:**
- ⚠️ **No multi-dispatch dispatchers.** RTS's `BedroomStudy` (1 dice → 4 NPCs) is more economical and yields a "you don't know which NPC will walk in" surprise quality. TLS Frank's 1:1 design gives predictable per-activity outcomes (e.g., washing dishes ALWAYS rolls for Frank-at-sink, not for Ryan or Jake). For a multi-NPC future expansion, this is a structural limit — though the engine supports adding more rules to a single parent.
- ⚠️ **No Pattern C (in-cascade stat gates).** Same as RTS Lane 3 doctrine — but RTS Lane 2 uses Pattern C extensively (PeepBrotherSex). Pattern C is missing across BOTH lanes in TLS Frank.

### Verdict

**Lane 3: FAITHFUL doctrine match — strongest of the three lanes.**

- ✅ **Cascade structure**: 100% match (10/10 RTS, 7/7 TLS)
- ✅ **Word count + chance% + tier ladder**: in range
- ✅ **NPC presence gating**: equivalent
- ✅ **No-daily-cooldown doctrine**: preserved
- ✅ **Pattern F refuse-path**: TLS EXCEEDS RTS (RTS has 0 in Lane 3, TLS has 2/7)
- ⚠️ **Multi-dispatch architecture**: TLS uses 1:1 where RTS uses 1:N — minor architectural divergence, not user-visible
- ⚠️ **Maya-bedroom Lane 3**: TLS doesn't translate this RTS surface (Frank narrative reason — accepted deviation)

Lane 3 is the success story of the Frank conversion. PRD 25 engine work + Pass 5 implementation + Pass 6/7 content authoring landed an RTS-faithful Lane 3 with the critical engine fix discovered mid-authoring. **Zero remediation needed.**

### Candidate fixes (low priority — Lane 3 is already healthy)

| Fix | Effort | What it buys |
|---|---|---|
| Convert 1-2 dispatchers to multi-target (e.g., make `activity_wash_dishes_solo` carry rules for both Frank-at-sink AND a future Ryan-at-sink) | ~30 min per dispatcher | Future-proofing for cross-NPC Lane 3 expansion; matches RTS economy |
| Add 1-2 Maya-bedroom Lane 3 surfaces for OTHER NPCs (Ryan/Jake — out of Frank-only scope) | n/a — out of scope | n/a |
| Add per-canvas `daily_cap` if playtest shows Lane 3 fires too frequently in a single in-game day | ~5 min per canvas | Throttle if needed; not currently needed per Pass 6+7 verification |

---

## Cross-lane synthesis + remediation roadmap

### The three verdicts — at a glance

| Lane | Verdict | Severity | What shipped | What RTS does | Gap |
|---|---|---|---|---|---|
| **1 (Hub button)** | Partial match | **MEDIUM drift** | ~11 click-only tease items + 2 rendered sex scenes (Pattern E+F) | 5 rendered scenes (2 Pattern A tease/flash + 2 Pattern E sex + 1 Pattern D sleep-with) | No rendered Pattern A; no late-game intimacy; no replay variety on tease items |
| **2 (Random/ambient)** | Severe drift | **HIGH drift** | 15 single-render canvases (0% cascade) with `[group]` tier branching, global 3-visit cooldown | 16 surfaces total (81% cascade, 19% pregnancy-utility) with `previous()` gate + `executedToday` daily caps | Zero cascades; wrong cooldown mechanism; no stored-roll multi-dispatch |
| **3 (Dispatcher walk-in)** | Faithful + improvement | **LOW drift** | 7 cascaded substitutions (100% cascade, 29% Pattern F refuse) | 10 surfaces (100% cascade, 0% Pattern F) | Minor architectural — 1:1 vs 1:N dispatcher economy |

### The shape of the drift

The three lanes shipped at very different doctrine-fidelity levels — and the pattern is **chronological**:

- **Lane 1 (Pass 3)**: Authored quickly using a pre-existing TLS "click-only tease distribution" doctrine (kitchen brush-past / hallway robe / radio rug already shipped that way). Pass 3 followed precedent without re-evaluating against RTS. Result: matching menu density but underweight rendered content.

- **Lane 2 (Pass 1 doctrine flip + Pass 4 expansion)**: The 11 existing TLS ambient canvases were originally authored in the pre-Phase-2 era as `trigger_mode = "manual"` portrait scenes. Pass 1's "doctrine flip" changed `manual → random` to match RTS Lane 2 mode — but didn't restructure the BODIES. So they became randomly-fired single-renders that LOOK like Lane 2 but BEHAVE like flattened versions of cascades. Pass 4 then authored 4 new canvases in the same shape, doubling down on the drift.

- **Lane 3 (Pass 5 engine + Pass 6+7 content)**: Built from scratch AFTER doc 24's RTS Lane 3 analysis was complete. PRD 25 explicitly named the mechanism; engine was implemented to match; content authoring deliberately ported BrotherShowerSex thresholds verbatim. Result: faithful.

**The lesson**: doctrine fidelity correlates with WHEN the doctrine was clearly understood. Lane 3 was authored with clear RTS reference in hand. Lane 1 + Lane 2 inherited pre-Phase-2 TLS doctrines that don't match RTS.

### Severity ranking + remediation priorities

Ranked by **player-visible impact** (not authoring effort):

**🔴 #1 priority — Lane 2 cascade conversion.** Frank's "world feels alive" texture lives or dies on Lane 2. Currently 15 ambient surfaces fire as flat single-renders. The cascade primitive ALREADY ships (used in Lane 1 kitchen morning + capstones). Highest-impact remediation: promote the top 4-6 Frank Lane 2 surfaces to cascades (`late_night_raid`, `kitchen_coffee_alone`, `office_diana_call_intercept`, `living_room_radio`, `porch_evening_smoke`, `hallway_pass`). Estimated effort: ~12-16 hours. **Buys**: RTS-shape Lane 2 click-feel + the come-back-later-for-deeper-cascade replay loop that's currently impossible in TLS Frank.

**🟡 #2 priority — Lane 2 cooldown mechanism.** Add `previous_in` filter (only fire on hub-entry) + per-canvas `max_triggers_per_day = 1` to all Lane 2 canvases. Restores the RTS anti-toggle behavior + matches the 44%-of-RTS-Lane-2 daily-cooldown norm. Estimated effort: ~2 hr engine + 30 min TOML. **Buys**: prevents player from exploit-rolling Lane 2 by toggling sub-passages; matches RTS pacing.

**🟡 #3 priority — Lane 1 Pattern A tease/flash rendering.** Promote 3-5 highest-impact click-only tease items to rendered Pattern A scenes (~80w + 1 image + return). Bedroom + kitchen ones first. Estimated effort: ~6-8 hours. **Buys**: narrative acknowledgement on tease clicks (currently absent in TLS); RTS texture.

**🟢 #4 priority — Lane 1 late-game intimacy (Sleep-with-Frank).** Add 1 Stage-4 LN-band terminal intimacy surface distinct from the bedroom sex loop. Matches RTS's `SleepingBrother` doctrine slot. Estimated effort: ~2-3 hours.

**🟢 Optional polish — Lane 3 multi-dispatch.** Future-proof 1-2 dispatchers (e.g., `activity_wash_dishes_solo` carrying both Frank + future-NPC rules). Not needed for current single-NPC Frank scope. ~30 min per dispatcher.

### The "if you only have N hours" recommendation

| If you have... | Do priority(ies) | Net effect |
|---|---|---|
| **3 hours** | Lane 1 Sleep-with-Frank only | Smallest user-visible win; closes the LN-band gap |
| **8 hours** | Lane 1 Pattern A promotions (3-5 items) + Sleep-with-Frank | Closes Lane 1 drift; Lane 2 remains broken but at least Lane 1 reads correctly |
| **18 hours** | Lane 2 cascade conversion (top 4-6 surfaces) + Lane 2 cooldown engine fix | Fixes the biggest structural drift; Frank starts feeling "alive" in RTS-shape |
| **30 hours** | All of the above + Lane 1 Pattern A + Sleep-with-Frank | Full doctrine alignment; Frank ships RTS-faithful across all 3 lanes |
| **50+ hours** | Above + remaining 9-11 Lane 2 surfaces converted to cascade | Full conversion; nothing left on the table |

### Methodology notes for future audits

**What worked:**
- Source extraction from `passage_catalog.json` was sharper than live-play would have been. The full 16-scene Lane 2 catalog + 10-scene Lane 3 catalog wouldn't have surfaced via 45-min walk-through (too many scenes wouldn't fire in one play session).
- Cross-referencing doc claims against source revealed at least one doc error (doc 24 §8.1 "no Lane 2 cooldown") — methodology rule §N (don't trust doc claims without re-verification) confirmed correct.
- The same nested-if parser handled Lane 2 + Lane 3 dispatcher detection with zero changes. Reusable.

**What didn't work:**
- Live-play attempts (2 agent timeouts at ~11 min each). Sonnet agents seem to time out on long Chromium driving sessions. For future audits, prefer source-first if a `passage_catalog.json` exists.

**One trip hazard documented:**
- Python regex `id\s*=\s*"slug"` matches `target_canvas_id = "slug"` rule references as well as canvas declarations. For canvas inventory work, split by `[[canvases]]` first and find id within each section — OR use `^id` / `\nid` anchored match.

---

End of doc.
