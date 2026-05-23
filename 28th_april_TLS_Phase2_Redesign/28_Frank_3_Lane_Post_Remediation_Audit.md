# 28 — Frank 3-Lane Post-Remediation Audit

> **Status:** Authored 2026-05-12 evening. Read-only audit performed in-conversation against current `7_final_game.toml`, current engine (`v1.py` + `template_import.py`), and RTS source extracted from `game_explorations/rts-arc-trace/passage_catalog.json`.
> **Purpose:** Re-verify what shipped during the Frank 3-Lane Doctrine Remediation (17 atomic units, completed 2026-05-12 per docs 26 + 27) against RTS source-of-truth. Three-bucket verdict per claim. No memory-entry trust — every TLS claim cited to TOML file:line, every RTS claim cited to passage source, every engine claim cited to v1.py/template_import.py file:line.
> **Supersession map:** Doc 26 = pre-remediation audit (now historical baseline). Doc 27 = the remediation plan (now historical execution record). **Doc 28 (this) = post-remediation audit**. Future Frank work should consult doc 28 first; docs 26/27 retain value as the snapshot of what existed before remediation + what was planned.
> **Scope:** Frank only. Cross-NPC out of scope.

---

## TL;DR — The 3 lane verdicts at a glance

| Lane | Pre-remediation (doc 26) | What shipped | Post-remediation verdict | Outstanding drift |
|---|---|---|---|---|
| **1 — Hub button** | 🟡 MEDIUM drift (no Pattern A renders, no Sleep-with-Frank, no replay variety) | 5 L1-1 Pattern A renders + 1 L1-4 Flash + 1 L1-3 Sleep-with-Frank + L1-2 image pool engine + 6 pool applications | ✅ Mostly faithful with **1 🚩 drift + 3 🟡 flags** | L1-3 has 2 invented per-beat effects; Pattern A density (6 vs RTS 2 — 3x); Flash pool size (5 vs RTS 11) |
| **2 — Random/ambient** | 🔴 SEVERE drift (0% cascade, no `previous()` gate, no daily caps) | L2-2 engine extension + L2-3 daily caps on 12/14 + L2-2 entry_only_from on 12/14 + 6 cascade conversions | ✅ ~80% closed with **1 🚩 drift + 4 🟡 flags** | 9 per-beat effect ticks invented; cascade rate 40% (RTS 81%); no Pattern C; hallway gates sparse |
| **3 — Dispatcher walk-in** | 🟢 LOW drift (faithful) | No remediation needed — already faithful from Pass 5+6+7 | ✅ **CLEANEST of three** — 0 drift items | None. Outstanding 🟡 flags are narrative-justified deviations (Maya-bedroom omission). |

**Headline finding:** Drift is **chronological**. Lane 3 (built first after doc 24 RTS analysis was fresh) is RTS-faithful. Lane 1 + 2 cascade work (built later) introduced an invented "high-trust verbal-share = Frank.love +1 mid-cascade" doctrine that does NOT match RTS. RTS ticks stats only at terminal beats / rejection branches, never on successful mid-cascade beats. This drift appears in 9 Lane 2 cascade beats + 2 L1-3 cascade beats = **11 invented mid-cascade ticks total**.

**Magnitude:** Small per-tick (+1), but additive. A player completing all 6 L2-1 cascades + L1-3 in a playthrough gains ~+6 Frank.love, +3 Frank.arousal, +1 Frank.trust, -1 player.calculation that wouldn't exist in RTS-faithful shape.

---

## Methodology

This audit's findings are reproducible from three artifact classes — every claim below is traceable:

1. **RTS source-of-truth** = `game_explorations/rts-arc-trace/passage_catalog.json` (361 passages, captured 2026-04-29). All RTS pattern claims cite specific passages by name; verbatim source extracted in this audit's working session.

2. **TLS shipped state** = `games/the_long_summer_test/toml_phases/7_final_game.toml` as of 2026-05-12. All TLS claims cite line numbers in this file. Memory entries (`frank_fix_*.md`) describe author intent at write time; **TOML is what shipped**. Where memory and TOML disagreed, TOML wins.

3. **Engine state** = `apps/projects/services/template_import.py` + `apps/game_generation/twee_comprehensive/generators/v1.py`. All engine claims cite line numbers. Test claims cite class names in `apps/projects/tests.py`.

**Verdict bucket definitions:**
- **✅ MATCH** — RTS does X, TLS shipped X, the implementation paths are equivalent.
- **⚠️ DEFENSIBLE DEVIATION** — TLS shipped Y where RTS does X, but Y has a stated reason (TLS engine constraint, narrative justification, doctrinal improvement) and produces equivalent or improved player experience.
- **🚩 DRIFT** — TLS shipped Z that RTS does NOT do, AND the deviation was claimed (in memory entries or doc text) to be RTS-canonical when it isn't. Drift is the failure mode this audit is designed to surface.
- **🟡 YELLOW FLAG** — Gap between RTS doctrine baseline and what shipped. Not invented (so not 🚩) but not closed either. Either acknowledged-and-deferred or unrecognized-yet.

---

## 📋 LANE 1 — Hub button ("intentional escalation")

### What RTS does (extracted from passage_catalog.json)

RTS Brother Lane 1 = 5 rendered scenes:

| RTS Scene | Pattern | Words | Stat gate | Where gate sits | Image pool | Per-beat ticks |
|---|---|---:|---|---|---:|---|
| `BrotherBedroomTease` | **A — single-render** | 69 | corr ≥ 5 | At hub button | **5** images | 0 (only on-render: `<<AddArousal>><<AddBrotherCorruption>><<AddTime '1'>>`) |
| `BrotherBedroomFlash` | **A — single-render** | 93 | corr ≥ 5 | At hub button | **11** images (preg variant: 6) | 0 (only on-render: `<<AddExb>><<AddArousal>><<AddBrotherCorruption>><<AddTime '1'>>`) |
| `BrotherBedroomSex1` | **E — pure linear cascade** | 811 | None in scene; gate at hub button (`getCorruptionLevel() >= 3 + getArousal() > 0`) | At hub button | 13 video stubs | 0 mid-cascade; only terminal `<<FinishSex>><<UnlockNPCScene>>` |
| `BrotherBedroomPregnantSex1` | **E variant** | 523 | Pregnancy flag | At hub button | 9 video stubs | Same — 0 mid-cascade |
| `SleepingBrother` | **D — top-of-cascade gate** | 527 | At HUB: `$npc.Brother.relation >= 10` (visibility). At SCENE entry: `getArousal() >= 1 && getCorruptionLevel() >= 3`. Inner gate: `StageTwoCorruption(Brother)`. | Both at hub + at scene | 11 video stubs | 0 mid-cascade; only terminal `<<UnlockNPCScene>><<FinishSex>>` |

**Critical RTS shape rules (verified across all 5 source extracts):**

1. **Pattern A is short and image-heavy** — 69-93 words, 5-11 image pool via `<<set $game.randomMedia to either(...)>>`, single render with stat ticks on entry, return button.
2. **Pattern E is "either you get it or you don't"** — entry-gate at hub button → if pass, ALL 12 cascade beats reveal linearly with NO mid-cascade stat checks. Stats fire ONLY at terminal `<<FinishSex>>`.
3. **Pattern D has rejection variants** — top-of-cascade gate; if pass, full cascade; if fail, low-stat variant published as `<<NotifyCorruption(N)>>` + bail message.
4. **Stats NEVER tick mid-cascade on successful beats.** Verified across 5 source extracts. RTS terminal-only doctrine for relationship ticks.

### What shipped for Frank — per-canvas inventory

| # | Canvas | Lines | Type | substitution_only | Conditions | Cascade beats | Image pool size | Per-beat ticks | Exit shape |
|---|---|---|---|---|---|---:|---:|---:|---|
| 1 | `tease_office_desk_lean` | 4821-4880 | L1-1 Pattern A | ✅ true | corr ≥ 5 | 3 | **5** | **0** | location → office, +10min, 4 effects |
| 2 | `tease_office_desk_sit` | 4891-4950 | L1-1 Pattern A | ✅ true | corr ≥ 5 | 3 | **5** | **0** | location → office, +15min, 4 effects |
| 3 | `tease_bedroom_sit_wait` | 4963-5023 | L1-1 Pattern A | ✅ true | corr ≥ 50 | 3 | **5** | **0** | choices: routes to sex loop with arousal +5 carryover |
| 4 | `tease_kitchen_brush_past` | 5034-5093 | L1-1 Pattern A | ✅ true | frank_restrict_declared | 3 | **5** | **0** | location → kitchen, +30min, 4 effects |
| 5 | `tease_hallway_robe_linger` | 5105-5165 | L1-1 Pattern A | ✅ true | frank_restrict_declared + corr ≥ 35 | 3 | **5** | **0** | location → hallway, +10min, 4 effects |
| 6 | `tease_bedroom_robe_flash` | 5181-5240 | L1-4 Pattern A (Flash) | ✅ true | corr ≥ 5 | 3 | **5** | **0** | location → hallway, +5min, 4 effects |
| 7 | `scene_frank_bedroom_sleep_overnight` | 4504-4607 | L1-3 Pattern D + F-light | ✅ true | frank_invited_to_bedroom + frank_bedroom_first_done + Frank.love ≥ 10 | 4 | n/a | **2** ← drift | choices fork: stay-through-morning vs leave-before-dawn |

**L1-2 image pool engine:**
- `apps/game_generation/twee_comprehensive/generators/v1.py:11833-11920` — pool handler
- Macro emitted (line 11907): `<<set _img to either("path1", "path2", ...)>>`
- Image tag (line 11909): `<img @src="_img" ...>`
- Fallback path: missing-pool → placeholder `[IMAGE POOL MISSING — N files]` if `--debug` set
- 5 ImagePoolTests in `apps/projects/tests.py`

### Three-bucket verdicts

#### ✅ MATCH

- **Pattern A canvas mechanics**: All 6 Pattern A canvases use `substitution_only = true` (excluded from selectors), reachable only via cross-canvas `nodeId` routing from menu items. Per Pass 7 doctrine.
- **Pattern A NO-mid-cascade-ticks**: All 6 Pattern A cascades have ZERO per-beat effects. Effects fire on exit only. Matches RTS Pattern A terminal-only doctrine exactly.
- **First-tease threshold**: corr ≥ 5 on items 1, 2, 6 = exact match to RTS Brother Tease/Flash threshold.
- **Image pool macro shape**: `<<set _img to either(...)>>` + `<img @src="_img">` is structurally identical to RTS's `<<set $game.randomMedia to either(...)>>` + `[img[setup.ImagePath+'/...'+$game.randomMedia]]`. TLS uses temp variable `_img` (underscore prefix) instead of story variable `$game.randomMedia` (dollar prefix) — temp vars don't pollute save state, mild engineering improvement.
- **Menu item conversion**: Verified at `7_final_game.toml:4722-4729` (item 1) and `4756-4763` (item 2): original `targetType = "trigger"` flipped to `targetType = "node"`, `nodeId = "tease_*.base"`, effects/time correctly removed and moved to canvas exit_block.
- **Effect-delta preservation on canvas conversion**: Original click-only items shipped with effect arrays of (Frank.arousal +1, Frank.corruption +1, Maya.corruption +1, energy -2). Verified those exact effects landed on canvas exit_block at lines 4873-4878 (item 1), 4943-4948 (item 2), 5086-5091 (item 4), 5158-5163 (item 5). Zero effect loss.

#### ⚠️ DEFENSIBLE DEVIATIONS

- **L1-1 item 3 (`tease_bedroom_sit_wait`) routes INTO sex loop, not back to location.** RTS Tease is render-then-return-to-hub. TLS item 3 is render-then-route-to-loop with `Frank.arousal +5` pre-arousal carryover (TOML:5022). No exact RTS equivalent. Defensible — corruption-50 gate is high enough that the player's intent is clearly "have sex," not "tease and return."
- **Stat tick model differences** between TLS and RTS Pattern A. RTS Tease ticks `<<AddArousal>>` (PLAYER arousal) + `<<AddBrotherCorruption>>` (NPC corruption) + `<<AddTime '1'>>`. TLS Tease ticks Frank.arousal +1 + Frank.corruption +1 + Maya.corruption +1 + energy -2. Different model (TLS tracks player corruption + energy where RTS tracks player arousal + time). Both track an NPC corruption escalator. Defensible — TLS engine has its own stat vocabulary.
- **L1-3 is non-sex sleep variant.** RTS `SleepingBrother` IS a sex scene (8-beat cascade with pregnancy/sex variants). TLS `scene_frank_bedroom_sleep_overnight` is a 4-beat relational beat with no sex content. Deliberate choice — fills the "late-game relational intimacy" doctrine slot WITHOUT overlapping the existing `loop_franks_bedroom_sex` content. Defensible variation.

#### 🚩 DRIFT — invented doctrine

- **L1-3 Sleep-with-Frank has 2 per-beat effects in cascade body.** Verified at TOML lines 4546 (Beat 1: Frank.love +1) and 4556 (Beat 2: player.calculation -1). RTS `SleepingBrother` has ZERO mid-cascade ticks across its entire 8-beat sex cascade — terminal `<<UnlockNPCScene>><<FinishSex>>` only. The L1-3 per-beat ticks are part of the broader "high-trust verbal-share = inline +1 tick" pattern that leaked across all the Lane 2 cascade conversions; doc 27 sub-step 4 inherited the doctrine claim from L2-1 sub-steps. Memory entry `frank_fix_L1_3.md` describes these ticks; they are NOT in RTS source.

#### 🟡 YELLOW FLAGS

1. **Pattern A density: 6 vs RTS 2 (3x).** RTS Brother has only 2 Pattern A surfaces (Tease + Flash) out of 16 total = 13% density. TLS Frank now has 6 Pattern A surfaces (5 L1-1 + 1 L1-4) — and given Frank's full canvas count is heavier than Brother's, the proportion may also be higher. RTS deliberately keeps Pattern A SCARCE relative to Pattern E sex cascades. Memory entry `frank_fix_L1_4.md` celebrates "3x density" as positive — but the doctrine signal is that scarcity is intentional. Worth re-evaluating whether the 6 surfaces are all earning their slot or whether some are redundant.
2. **L1-4 Flash uses 5-image pool, RTS Flash uses 11.** Verified at TOML:5204 — `tease_bedroom_robe_flash` ships with a 5-element `files` array. RTS `BrotherBedroomFlash` source uses `<<set $game.randomMedia to either(brotherflash1.webp, ..., brotherflash5.webp)>>` for non-pregnant + `either(preg_brotherflash1.webp, ..., preg_brotherflash6.webp)` for pregnant — 5+6=11 distinct images across both branches. TLS Flash pool is half the RTS Flash density. Memory `frank_fix_L1_2_phase_b.md` rationale ("matches RTS Tease density") applies the wrong RTS reference — Tease is the corruption-5 SUGGESTIVE register, Flash is the corruption-5 OVERT register. Easy fix: bump Flash pool to 8-11 images.
3. **L1-3 gate `Frank.love ≥ 10` vs RTS `relation ≥ 10` — scale not proven equivalent.** RTS relation is bounded around 0-30 in Brother arc. TLS love appears to range 0-100. Gate value 10 means very different things on different scales. Audit doc 26 flagged this as "audit-time concern that wasn't resolved" — still unresolved. Could mean L1-3 unlocks at a meaningfully different point in arc than RTS doctrine intends. Could also mean L1-3 unlocks too easily (love=10 is low on a 100-scale).

### Outstanding gaps from doc 26 not closed by remediation

- **Pattern E density rebalance not addressed.** Doc 26 noted TLS Frank has 2 Pattern E sex scenes (office after-crack + bedroom sex loop) vs RTS Brother's 2 (Sex1 + PregSex1). Match by count — but RTS uses Pattern E as the heavyweight content surface (~800w each). Frank's office-after-crack + bedroom-sex-loop combined are similar weight; verified-aligned, no gap.
- **Sleep-with-Frank as RTS twin**: doc 26 said "no Sleep-with-Frank LN-band intimacy surface." L1-3 closes this. ✅
- **Replay variety on tease items**: doc 26 said "no replay variety mechanism on tease items." L1-2 closes this for the 6 Pattern A canvases. ✅
- **Exhibitionism register (Flash equivalent)**: doc 26 said all 3 office teases are "suggestive proximity, no exhibitionist register." L1-4 closes this with bedroom robe flash. ✅

---

## 📋 LANE 2 — Random/ambient encounter

### What RTS does (extracted from passage_catalog.json)

RTS Lane 2 = 16 surfaces (per doc 26 §LANE 2 source-extracted catalog). Canonical patterns verified in this audit:

**`BrotherCaughtMasturbating` (Pattern D — 902w / 10 LR):**
- Top-of-cascade gate: `<<if getCorruptionLevel() >= 3>><<if StageTwoCorruption($npc.Brother)>>` ⇒ enter 9-beat sex cascade
- Else corruption ≥ 3 + below stage gate: `"He hides his dick"` rejection + `<<StageNotification $npc.Brother 2>>`
- Else low corruption: `"Ew you pervert!"` rejection + `<<NotifyCorruption 3>>`
- **Inner cascade has ZERO per-beat stat ticks.** Beats 1-9 are pure linkreplace reveals with dialog + video. Terminal beat fires `<<UnlockNPCScene Brother BrotherCaughtMasturbating>><<FinishSex Brother false>>`.

**`PeepBrotherSex` (Pattern C — 211w / 4 LR):**
- 4-beat cascade with stat gates AT EACH BEAT inside linkreplace bodies
- Beat 2 gate: `<<if getArousal() > 0>>` ⇒ continue; else `<<NotifyCorruption 2>>` + `<<AddArousal>>` consolation tick + bail message
- Beat 3 gate: `<<if getCorruptionLevel() >= 2>>` ⇒ continue; else same consolation pattern
- Climax beat (Beat 4) fires `<<UnlockNPCScene>><<AddCorruption>><<ResetArousal>>`
- **No mid-cascade ticks on SUCCESSFUL beats.** Ticks only fire on rejection branches as consolation.

**`BrotherBedroom` hub dispatcher (the anti-toggle gate source):**
- Inside hub passage: `<<if previous() == "Hallway">><<set $game.random = random(1,4)>><<if $game.random == 1 && !$npc.Brother.scenes.PeepBrotherSex.executedToday>><<goto 'PeepBrotherSex'>><<elseif $game.random == 2 && !$npc.Brother.scenes.BrotherCaughtMasturbating.executedToday>><<goto 'BrotherCaughtMasturbating'>><</if>><</if>>`
- The `previous() == "Hallway"` gate AND the stored-roll dispatch (`random(1,4)`) AND the `executedToday` flag AND the `<<goto>>` to substituted scenes ALL live at the HUB passage, NOT on the random scenes themselves.

**Critical RTS shape rules:**
1. **Cascade rate** ≈ 81% of Lane 2 surfaces are cascade-bodied (per doc 26 catalog).
2. **Anti-toggle gate**: 81% use `previous() == "X"` to limit firing to fresh hub-entry. Single allowed previous passage (scalar, not list).
3. **Daily cooldown**: 44% have explicit `!executedToday` flag.
4. **Stored-roll multi-dispatch**: `<<set $game.random = random(1,4)>>` then `<<if $game.random == 1>>` ... `<<elseif $game.random == 2>>` ... — one dice roll dispatches to N candidates (verified at `BrotherBedroom` hub).
5. **Mid-cascade stat gates** present in Pattern C scenes only (PeepBrotherSex). Pattern D doesn't have them — top-of-cascade gate decides full-cascade vs rejection.
6. **Stats NEVER tick mid-cascade on successful beats.** Same rule as Lane 1.

### What shipped for Frank — verified inventory

Lane 2 canvases in current `7_final_game.toml`: **15 total** (per doc 26's count, verified by grep: 14 with explicit `npc = "npc_frank"` + 1 implicit at `scene_hallway_frank_pass`:6035 which is Frank-scoped via prose without the `npc` field).

| Item | Coverage | Verification location |
|---|---|---|
| **L2-3 daily caps** (`max_triggers_per_day = 1`) | **13 of 15** | TOML grep: 13 canvases have field. 2 mutex-skipped (`scene_office_frank_diana_call_intercept` + `scene_hallway_frank_late_drink` carry `frank_*_used = true` mutex flags = stricter than daily cap). 3rd mutex (`scene_kitchen_late_night_raid` `frank_late_night_used`) correctly given daily cap as defense-in-depth. |
| **L2-2 anti-toggle gate** (`entry_only_from = [...]`) | **13 of 15** | Same 13/15. Engine wired at `v1.py:4008-4026` — uses native SugarCube `previous()` to filter random encounter candidates. Build-time slug→passage translation at `v1.py:9354-9360`. Validator integration at `template_import.py:2352-2364` (rejects if used on non-`random` mode). 9 EntryOnlyFromTests in `apps/projects/tests.py`. |
| **L2-1 cascade conversions** | **6 of 15** | 21 cascade IDs verified in TOML across 6 canvases: `frank_late_night_t1/t2` (lines 6982/7016), `frank_radio_t1/t2/t3/s3/s4` (lines 6496/6515/6540/6573/6594), `frank_smoke_t1/t2/t3/s3/s4` (lines 6704/6723/6751/6785/6809), `frank_coffee_t1/t2/t3` (lines 6358/6380/6406), `frank_weekend_t1/t2/t3a/t3b/postr` (lines 7797/7817/7836/7856/7878), `frank_diana_call_intercept` (line 7399). |
| **Per-beat effects in L2-1 cascades** | **9 inline ticks** | TOML lines 6419 (coffee t3), 6551 (radio t3), 6601 (radio s4), 6764 (smoke t3), 7028 (late-night t2), 7037 (late-night t2), 7409 (diana intercept), 7863 (weekend t3b), 7890 (weekend postr). 5× Frank.love +1, 3× Frank.arousal +1, 1× Frank.trust +1. |

### Three-bucket verdicts

#### ✅ MATCH

- **L2-2 engine implementation matches RTS mechanism.** SugarCube `previous()` is the same primitive RTS uses (verified at `v1.py:4014`: `prevPassage = previous() || ''`). The schema-based `entry_only_from` field translates to runtime passage names at build time, comparing with RTS's hard-coded `previous() == "Hallway"`.
- **L2-3 daily caps match RTS `executedToday` doctrine.** RTS uses 7/16 = 44% daily cap; TLS Frank applies it to 13/15 = 87% (more aggressive than RTS, but aligned in shape).
- **Cascade primitive emission matches RTS `<<linkreplace>>` shape.** TLS `type = "cascade"` blocks emit nested linkreplace structure matching RTS PeepBrotherSex / BrotherCaughtMasturbating / BrotherShowerSex cascades. Per-beat dialog interleave matches RTS's `<<Speech NPC ...>>` pattern.
- **chance% values in range** (0.20-0.40 + one deterministic 1.0 for `late_night_raid`) — matches RTS's `random(1,2)` to `random(1,5)` range.

#### ⚠️ DEFENSIBLE DEVIATIONS

- **TLS uses tier-branched cascades (no rejection variants).** RTS Pattern D pattern: ONE cascade entry + 1-2 low-stat rejection variants (`"Ew you pervert!"` + `<<NotifyCorruption(N)>>`). TLS shipped MULTIPLE cascades per canvas — different prose at different trust tiers, but the LOWEST tier always still gets a 4-beat cascade. **More generous than RTS** (no "you don't qualify yet — come back later" rejection feel), but defensible — the TLS prose is intentionally non-confrontational.
- **`entry_only_from` schema accepts a list** vs RTS's single allowed `previous()`. Schema is more general; in practice TLS applies 1-element lists. Engineering acceptable.
- **Build-time slug→passage translation** (`v1.py:9354-9360`) is cleaner than RTS's hard-coded passage names in source. Mild engineering improvement.

#### 🚩 DRIFT — invented doctrine

**The 9 per-beat effect ticks across L2-1 cascades are not RTS-canonical.** Verified pattern across all 5 RTS source extracts (BrotherCaughtMasturbating / BrotherShowerSex / PeepBrotherSex / SleepingBrother / BrotherBedroomSex1):

- RTS terminal-only ticks: `<<UnlockNPCScene>>`, `<<FinishSex>>`, `<<AddCorruption>>` at climax beat
- RTS rejection-branch ticks: `<<NotifyCorruption(N)>>` + `<<AddArousal>>` consolation
- **RTS NEVER ticks relationship stats at successful mid-cascade beats.**

TLS L2-1 cascades ship with:
- 5× Frank.love +1 (coffee t3, radio t3, smoke t3, late-night t2 property reveal, diana intercept "don't bring her name")
- 3× Frank.arousal +1 (radio s4 hand-on-thigh, weekend t3b knee touch, weekend postr small-of-back)
- 1× Frank.trust +1 (late-night t2 "pushing-glass" beat)

Memory entries (`frank_fix_L2_1_canvas1.md` through `_canvas6.md`) consistently call this "the canonical doctrine pattern" and "the high-trust verbal-share = Frank.love +1 doctrine pattern" — but the canon is RTS source, and RTS does not do this. **The doctrine claim is invented.**

**Magnitude:** small (+1 each), but additive. A player completing all 6 cascades earns +5 Frank.love, +3 Frank.arousal, +1 Frank.trust extra that wouldn't exist in RTS-faithful shape.

**Two valid fixes:**
- **A. RTS-faithful refactor**: move all 9 ticks to terminal beats / exit_block. Ticks fire on cascade completion, not mid-stream.
- **B. Accept as TLS-original variation**: keep — but stop calling it "RTS doctrine" in memory entries. Re-document as deliberate tick-on-narrative-share design choice.

#### 🟡 YELLOW FLAGS

1. **Cascade-rate gap not closed.** Frank Lane 2 = 6/15 = **40%** cascade-bodied. RTS Lane 2 = 13/16 = **81%**. Audit doc 26 framed remaining 9 as "optional saturation" but doctrine baseline says 6 closes only half the gap. Outstanding flat single-renders: `scene_hallway_frank_pass`, `scene_hallway_franks_door_evening`, `scene_kitchen_frank_afternoon_alone`, `scene_yard_frank_mending_fence`, `scene_living_room_frank_evening_paper`, `scene_hallway_frank_morning_pass`, `scene_living_room_frank_dusk`, `scene_yard_frank_late_afternoon`, `scene_hallway_frank_late_drink`.
2. **Pattern C (mid-cascade stat gates) absent everywhere.** RTS PeepBrotherSex gates EACH beat on stat (`getArousal() > 0` at beat 2, `getCorruptionLevel() >= 2` at beat 3) so player partial-completes + gets `<<NotifyCorruption(N)>>` to learn what to grind. Frank shipped 21 cascades, ZERO have this. The "come back when stats higher to see deeper beats" replay loop doesn't exist for Frank L2.
3. **No stored-roll multi-dispatch.** RTS hub passages dispatch `<<set $game.random = random(1,4)>>` to choose between candidate substitutions. Frank L2 evaluates each canvas's chance% independently — multiple Frank Lane 2 canvases at the same location/time can each consume a roll. Architectural divergence not addressed.
4. **Hallway entry_only_from gate is sparse-by-topology.** 3 hallway canvases gated to `["loc_front_porch"]` (per TOML:6047 / 6147 etc). Player rarely enters hallway from front porch in normal play loop (kitchen/living/bedroom returns are common). Net effect: hallway Lane 2 fires much less than chance% suggests. Memory `frank_fix_L2_2.md` documented this as "user accepted tradeoff."

### Outstanding gaps from doc 26 not closed by remediation

- ❌ Pattern C (mid-cascade gates) — flagged in doc 26, not addressed.
- ❌ Stored-roll dispatcher — flagged in doc 26, not addressed.
- ❌ 9 of 15 cascade conversions — flagged in doc 26 as "optional saturation," explicitly deferred.
- ✅ L2-2 anti-toggle gate — closed via engine extension.
- ✅ L2-3 daily caps — closed via TOML application.
- ✅ Top-6 cascade conversions — closed.

---

## 📋 LANE 3 — Dispatcher walk-in

### What RTS does (extracted from passage_catalog.json)

RTS Lane 3 = 4 dispatchers, 10 substitution targets (per doc 24 §3 + verified in this audit):

**`BathroomShowerMasturbate` (single-NPC dispatcher):**
```
<<if isPlayerAtHouse() && random(1,3) == 1 && StageOneCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
    <<goto 'BrotherShowerSex'>>
<<else>>
    [vanilla masturbate content]
<</if>>
```
- 33% chance, Brother-only
- Stat gate: `StageOneCorruption($npc.Brother)` (composite helper)
- Presence gate: `IsNpcAtHome("Brother")`
- Inline `<<goto>>` to substituted scene; vanilla fallback

**`BedroomStudy` (multi-NPC stored-roll dispatcher):**
```
<<set $game.dice to random(1,6)>>
<<if $game.dice == 1 && $npc.Dad.arousal > 0 && $npc.Dad.corruption > 0>>
    <<goto 'BedroomStudyDadGrope'>>
<<elseif $game.dice == 2 && $npc.Brother.arousal > 0 && $npc.Brother.corruption > 0>>
    <<if changeMediaPregnant()>>
        <<goto 'BedroomStudyBrotherGropePregnant'>>
    <<else>>
        <<goto 'BedroomStudyBrotherGrope'>>
    <</if>>
<<elseif $game.dice == 3 && $npc.Brother.arousal > 0 && $npc.Brother.corruption > 0>>
    <<goto 'BrotherHelpStudy'>>
<<else>>
    [vanilla study content]
<</if>>
```
- 1 dice → 4 NPC variants (Dad / Brother grope / Brother help / vanilla)
- 50% NPC dispatch (3/6) + 50% vanilla (3/6 includes the catch-all else)
- Each NPC variant has its own `arousal > 0 && corruption > 0` gate

**Substitution scene shapes (from RTS source):**
- `BedroomStudyBrotherGrope` (~80w, 1 LR): Pattern B'-like with single linkreplace "Keep studying"; on-render ticks `<<AddBrotherCorruption>><<AddCorruption>>`. NO per-beat ticks.
- `BrotherHelpStudy` (Pattern D): 9-beat sex cascade with 2 nested stat gates (`StageOneCorruption` → `StageTwoCorruption` → `StageThreeCorruption`). NO per-beat ticks; only terminal `<<UnlockNPCScene>><<FinishSex>>`.
- `BrotherWashDishesSex` (Pattern D + F-light): 8-beat cascade with `getCorruptionLevel() >= 3` top gate + refuse path. NO per-beat ticks; only terminal `<<UnlockNPCScene>><<FinishSex>>`.

**Critical RTS Lane 3 shape rules:**
1. **100% cascade rate** in NPC-dispatched substitution scenes.
2. **No mid-cascade per-beat ticks** (same as Lane 1 + Lane 2 — terminal-only).
3. **No `executedToday` daily caps on Lane 3** (asymmetric with Lane 2's 44%; player must choose the activity, so re-firing acceptable).
4. **Stat-threshold gating only** at scene-entry / dispatcher level.
5. **Pattern F refuse paths** absent from RTS Lane 3 (RTS reserves Pattern F for once-per-arc story moments like `SellingMyStepsister`).

### What shipped for Frank — verified inventory

7 Lane 3 substitutions across 7 dispatchers (1:1 ratio; doc 26 counted 7 — verified):

| # | Dispatcher (parent) | Target substitution canvas | Chance | Tier | substitution_only | Per-beat ticks |
|---|---|---|---|---|---|---:|
| 1 | `activity_make_tea` | `scene_frank_passes_kitchen_door` (line 8115) | 0.40 | T1 PG | ✅ true | **0** |
| 2 | `activity_make_coffee_solo` | `scene_frank_arrives_during_coffee` (line 8237) | 0.30 | T1 | ✅ true | **0** |
| 3 | `activity_sit_on_porch` | `scene_frank_joins_porch` (line 8362) | 0.30 | T2 | ✅ true | **0** |
| 4 | `activity_read_on_couch` | `scene_frank_joins_couch` (line 8487) | 0.30 | T2 (tier-branched) | ✅ true | **0** |
| 5 | `activity_wash_dishes_solo` | `scene_frank_at_kitchen_sink_behind` (line 8638) | 0.20 | T3 Pattern F | ✅ true | **0** |
| 6 | `activity_brush_teeth` | `scene_frank_at_open_bathroom_door` (line 8844) | 0.30 | T1 | ✅ true | **0** |
| 7 | `activity_masturbate_at_shower` (triggerless) | `scene_frank_walks_in_shower` (line 8980) | 0.33 | T3 Pattern F | ✅ true | **0** |

**L3 engine code locations:**
- Schema: `template_import.py:418` (`substitution_only: bool = False`), `:1047` (parser), `:2387-2391` (validator: substitution_only + npc warn), `:2513` (overlap-check exclusion — the Pass 6 fix), `:4354` (serializer)
- Engine: `v1.py:2143` (`setup.canvasSubstitutions`), `:4068-4087` (`setup.checkAndSubstituteCanvas` runtime helper), `:9346-9379` (substitution_only flag emission), `:10300-10307` (emitter injection at canvas Node 1 top — the Pass 6 `<<set>>+<<goto>>` fix)

### Three-bucket verdicts

#### ✅ MATCH (cleanest of the three lanes)

- **Engine substitution helper returns target passage NAME (string), not boolean.** `v1.py:4068-4087` — the Pass 6 fix for SugarCube's `<<script>>` not allowing naked `return`. Emitter at `v1.py:10305-10307` emits `<<set _sub_target = setup.checkAndSubstituteCanvas("X")>><<if _sub_target>><<goto _sub_target>><</if>>`. PRD 25 §5.4's broken `<<script>>+return` pattern is NOT in the codebase.
- **`substitution_only` flag wired correctly across schema → parser → validator → emitter.** Verified at `template_import.py:418/1047/2387/2513/4354` + `v1.py:9346-9379`. Selectors skip `substitution_only` canvases (per Pass 5 doctrine).
- **All 7 substitution targets are `substitution_only = true`.** Verified by grep against TOML (lines 4514, 4831, 4901, 4973, 5044, 5115, 5191 = Lane 1; 8115, 8237, 8362, 8487, 8638, 8844, 8980 = Lane 3).
- **ZERO per-beat effect ticks across all 7 Lane 3 cascade bodies.** Programmatically verified by parsing TOML cascade beats and excluding exit_block content. **Matches RTS terminal-only doctrine exactly.** Lane 3 is the lane the per-beat-effect drift did NOT contaminate.
- **Stat thresholds direct doctrine port.** `scene_frank_walks_in_shower` substitution rule (TOML:8922-8926) gates on corruption ≥ 20 + Frank.arousal ≥ 30 + Frank.corruption ≥ 10 — memory `frank_fix_pass5.md` documents this as a direct RTS BrotherShowerSex threshold port. Verified the values exist; semantically equivalent to RTS's `StageOneCorruption($npc.Brother)` composite.
- **Chance% values in range.** TLS 0.20-0.40, RTS 0.17-0.33. ✅
- **No daily caps on Lane 3** — matches RTS's asymmetric Lane-2-vs-Lane-3 cooldown doctrine.
- **Validator overlap-check skip** (`template_import.py:2513`) — Pass 6 fix verified, prevents 5 spurious warnings from Lane 3 substitutions.
- **`<<set>>+<<goto>>` runtime pattern + `markCanvasTriggered` integration** — substitution targets correctly inherit Layer 1 + Layer 2 cooldowns from `markCanvasTriggered`, no double-tracking.

#### ⚠️ DEFENSIBLE DEVIATIONS

- **1:1 parent:target ratio (TLS) vs 1:N (RTS BedroomStudy 1 dice → 4 NPC variants).** TLS uses 7 separate parent activities for 7 substitution targets. RTS BedroomStudy uses ONE dispatcher to handle 4 NPC variants via stored-roll. TLS architecture supports 1:N (multiple `[[canvases.trigger.substitutions]]` rules per parent), but Frank-only scope didn't need it. Future cross-NPC work (Ryan/Jake) would benefit from converting some dispatchers to 1:N.
- **Pattern F refuse-path adoption EXCEEDS RTS.** TLS shipped 2 of 7 (29%) Lane 3 surfaces as Pattern F refuse forks (kitchen sink behind + shower walk-in). RTS Lane 3 has ZERO Pattern F surfaces. TLS innovation matches the RTS Lane-3-doctrine (per doc 24 §10.5: "low-agency setup, choice-driven payoff") more strictly than RTS Brother Lane 3 itself does. Doctrine-positive deviation.
- **Triggerless dispatcher pattern** at `activity_masturbate_at_shower` (no `[canvases.trigger]` proper, just `substitutions = [...]` block) — TLS-original mechanism not present in RTS. Reachable only via cross-canvas nodeId from `activity_shower`. Defensible engineering — gives the activity a clean parent without polluting the shower hub itself with the substitution rule.

#### 🚩 DRIFT

**None.** Lane 3 is the cleanest of the three lanes.

#### 🟡 YELLOW FLAGS

1. **No Maya-bedroom Lane 3.** RTS BedroomStudy puts NPC walk-ins in MAYA's bedroom. TLS Frank doesn't visit Maya's bedroom (narrative reason: stepfather doesn't enter stepdaughter's bedroom uninvited). The RTS Lane 3 grammar of "NPC enters Maya's space mid-activity" is partially translated — TLS Frank Lane 3 is "Frank enters SHARED spaces mid-Maya-activity" (kitchen, living room, back porch, bathroom). Narratively justified, accepted deviation.
2. **No Pattern C (in-cascade stat gates) anywhere in Lane 3.** Same gap as Lane 2 — Pattern C is the "come back when stats higher to see deeper beats" replay primitive. RTS Lane 3 doesn't use Pattern C either, so this is shared-with-RTS deviation, not a TLS-only gap.

### Outstanding gaps from doc 26 not closed (intentional)

- ❌ L3-1 (1:1 vs 1:N dispatcher economy) — only matters cross-NPC; deferred per audit.
- ❌ L3-2 (no Maya-bedroom Lane 3) — narratively justified deviation; deferred per audit.

Both are 🟢 LOW severity and were explicitly out-of-scope for Frank-only remediation.

---

## Cross-lane synthesis

### The drift inventory (post-remediation)

Single ranked table of every 🚩 + 🟡 across all 3 lanes:

| # | Severity | Lane | Drift item | Magnitude | Fix cost |
|---|---|---|---|---|---|
| 1 | 🚩 | 2 | 9 per-beat effect ticks invented as "doctrine" — RTS terminal-only, TLS mid-cascade | +5 Frank.love + 3 Frank.arousal + 1 Frank.trust per playthrough | Refactor: 1 hr (move ticks to terminal/exit). Re-document: 30 min (correct memory entries). |
| 2 | 🚩 | 1 | L1-3 Sleep-with-Frank has 2 per-beat ticks (Frank.love +1 Beat 1 + player.calculation -1 Beat 2) | +1 Frank.love + -1 calculation per playthrough | Same as #1 (related drift). |
| 3 | 🟡 | 2 | Cascade rate 40% (TLS) vs 81% (RTS) — 9 canvases still flat | Significant ambient texture gap | ~18-24 hr to convert remaining 9 cascades. |
| 4 | 🟡 | 1 | Pattern A density 6 vs RTS 2 (3x); RTS deliberately scarce | Risk of menu-bloat / over-saturation | Re-evaluate: which 2-3 Pattern A surfaces earn slot, demote others. ~2 hr. |
| 5 | 🟡 | 1 | L1-4 Flash uses 5-image pool; RTS Flash uses 11 | Less replay variety on Flash | Bump to 8-11 in TOML. ~5 min. Asset generation deferred. |
| 6 | 🟡 | 1 | L1-3 gate `Frank.love ≥ 10` vs RTS `relation ≥ 10` — scale not proven equivalent | L1-3 may unlock too easily on TLS love=0-100 scale | Calibration audit + likely raise gate to ≥ 25-40. ~30 min. |
| 7 | 🟡 | 2 | Pattern C (mid-cascade stat gates) absent from all Frank Lane 2 cascades | No "come back when stats higher" replay loop in Lane 2 | Author 1-2 Pattern C cascades. ~3-4 hr. |
| 8 | 🟡 | 2 | No stored-roll multi-dispatch | Architecturally divergent; minor user-visible effect | ~3 hr engine + 30 min TOML per hub. Defer until cross-NPC scope. |
| 9 | 🟡 | 2 | Hallway canvases gated to `loc_front_porch` rarely fire | 3 canvases under-fire vs chance% suggests | Re-evaluate gate target (or allow multi-list). ~30 min. |
| 10 | 🟡 | 3 | No Maya-bedroom Lane 3 | RTS surface not translated | Narrative deviation; defer. |
| 11 | 🟡 | 3 | No Pattern C anywhere in Lane 3 | RTS Lane 3 doesn't use Pattern C either; shared deviation | No fix needed. |

### Memory entry corrections needed

The "high-trust verbal-share = Frank.love +1 mid-cascade" doctrine claim appears in **at least 5 memory entries** and is contradicted by RTS source. Affected files in `~/.claude/projects/.../memory/`:

| Memory file | Drift claim | Correct framing |
|---|---|---|
| `frank_fix_L2_1_canvas1.md` | "Per-beat Frank.trust+1 + Frank.love+1 on Tier 2's let-in + property-reveal moments" called canonical | TLS-original variation; not in RTS source |
| `frank_fix_L2_1_canvas2.md` | "Tier 3 carries the canonical radio-history reveal (Frank.love +1)" + "third in the high-trust personal-share doctrine pattern" | Doctrine pattern is invented, not RTS-canonical |
| `frank_fix_L2_1_canvas3.md` | "fourth/fifth in the canonical doctrine pattern" claims | Same — invented doctrine claim |
| `frank_fix_L2_1_canvas5.md` | "fourth instance of the doctrine pattern matching kitchen_late_night property reveal + radio father memory + smoke 'best ten minutes'" | Same |
| `frank_fix_L2_1_canvas6.md` | "5th doctrine instance" (diana intercept beat 1) | Same |
| `frank_fix_L1_3.md` | Beat-1 + Beat-2 ticks framed as relational-beat doctrine | Same drift pattern leaked into L1-3 |

**Recommended correction text** (paste into each affected memory entry's frontmatter description or as an addendum):

> **AUDIT CORRECTION 2026-05-12 (doc 28):** The "high-trust verbal-share = Frank.love +1" mid-cascade tick pattern is TLS-original, NOT RTS-canonical. RTS source (BrotherCaughtMasturbating, BrotherShowerSex, PeepBrotherSex, SleepingBrother, BrotherBedroomSex1) ticks relationship stats only at terminal beats / rejection branches, never at successful mid-cascade beats. Treat the per-beat ticks here as deliberate TLS variation, not as RTS doctrine match. See doc 28 §LANE 2 🚩 DRIFT for full evidence.

### Recommended follow-on work — ranked

If the goal is RTS-faithful Frank, prioritize fixing 🚩 drift first, then 🟡 by player-visible impact:

| Priority | Item | Effort | Why |
|---|---|---|---|
| **🔴 1** | Refactor 11 mid-cascade ticks (9 in L2-1 + 2 in L1-3) to terminal beats / exit_block | 1 hr | The only 🚩 items. Closes the doctrine drift. |
| **🟡 2** | Update 6 memory entries with the AUDIT CORRECTION text above | 30 min | Prevents drift from leaking into future authoring. |
| **🟡 3** | Bump L1-4 Flash pool 5 → 11 images (matches RTS Brother Flash density) | 5 min TOML; asset generation deferred | Trivially small; closes the most-clickable-surface variety gap. |
| **🟡 4** | Calibrate L1-3 `Frank.love ≥ 10` against TLS love scale; raise to ≥ 25-40 if love range = 0-100 | 30 min | L1-3 currently unlocks too easily; misses the "earned late-game intimacy" doctrine. |
| **🟢 5** | Re-evaluate Pattern A density (6 vs RTS 2) — demote 1-2 less-essential L1-1 surfaces if they don't earn their slot | 2 hr | RTS scarcity doctrine; menu-bloat risk. |
| **🟢 6** | Convert remaining 9 Lane 2 canvases to cascades (close cascade-rate gap to ≥ 80%) | 18-24 hr | Doctrine-baseline saturation; biggest single content lift. |
| **🟢 7** | Author 1-2 Pattern C cascades (mid-cascade stat gates with NotifyCorruption-equivalent threshold publication) | 3-4 hr | Adds the "come back when stats higher" replay loop. |
| **🟢 8** | Add stored-roll multi-dispatch | ~3 hr engine | Architecturally aligns Lane 2 with RTS. Defer until cross-NPC scope makes it useful. |

The "if you only have N hours" recommendation:

| Hours | Do priorities | Net effect |
|---|---|---|
| **1.5 hr** | 1 + 2 + 3 + 4 | All 🚩 drift fixed + memory entries corrected + 2 quick 🟡 closed |
| **3 hr** | + 5 | + Pattern A re-balance audit |
| **27 hr** | + 6 | + Cascade-rate gap closed (full RTS parity on Lane 2 saturation) |
| **34 hr** | + 7 + 8 | Full doctrine alignment |

---

## Confidence ladder

✅ **HIGH confidence (verified against source + TOML + engine):**
- All 🚩 + 🟡 drift items above are reproducible by re-running the same TOML reads + RTS extracts
- L1-1 Pattern A canvas mechanics, L1-2 image pool emission, L1-3 + L1-4 + L2-1 + L2-2 + L2-3 + L3 substitution mechanics — all engine + TOML paths verified file:line
- 9 Lane 2 per-beat ticks at exact TOML lines 6419 / 6551 / 6601 / 6764 / 7028 / 7037 / 7409 / 7863 / 7890; 2 Lane 1 ticks at 4546 / 4556
- 0 per-beat ticks across 7 Lane 3 substitution canvases (programmatically verified by parsing TOML)
- L2-2 anti-toggle gate uses native SugarCube `previous()` at v1.py:4014 — same primitive RTS uses
- L2-3 daily caps applied to 13 of 15 Lane 2 canvases
- L3 engine fix: `<<set>>+<<goto>>` pattern in place at v1.py:10305, NOT broken `<<script>>+return`

🟡 **MED confidence:**
- Pattern A density doctrine claim ("RTS deliberately scarce") — based on RTS Brother only; cross-NPC density (Dad/Marcus/Edward Pattern A counts) not re-verified this audit
- L1-3 Frank.love scale comparison to RTS relation scale — TLS love range (0-100?) inferred from typical NPC trait ranges; not source-verified against TLS character spec
- Pattern F adoption "exceeds RTS" claim — RTS Lane 3 0/10 Pattern F vs TLS 2/7 — verified for Brother only; Dad/Marcus/Edward Lane 3 Pattern F counts not re-verified

❌ **NOT established this audit:**
- Whether RTS BrotherBedroomFlash actually delivers higher player-perceived variety with 11 images vs 5 (no live playthrough comparison)
- Whether the 9 Lane 2 mid-cascade ticks meaningfully change player-perceived pacing vs an RTS-faithful terminal-only shape (no live playtest comparison)
- Whether the 6/15 Lane 2 cascade saturation reads as "alive" enough or whether the 9 flat single-renders create perceptible texture drops between cascade hits
- Whether L1-3 unlocking at Frank.love=10 fires at a satisfying point in the arc or feels too early

---

## Cross-references + source artifacts

**Doctrine docs (this folder, in dependency order):**
- Doc 13 — Road to Success Reference (broad RTS catalog)
- Doc 21 — RTS Brother Mechanism Audit (Pattern A-F definitions, source-extracted from `passage_catalog.json`)
- Doc 22 — RTS Cross-NPC Mechanism Comparison (40 surfaces / 4 NPCs)
- Doc 24 — RTS Three Lanes for Repeatable NPC Content + TLS Engine Fitness + Lane 3 Design (lane taxonomy + engine assessment + PRD 25 design)
- Doc 26 — Frank 3-Lane Audit (PRE-remediation baseline, now superseded by this doc as the current state-of-Frank reference)
- Doc 27 — Frank 3-Lane Remediation Plan (execution record; all 17 atomic units shipped 2026-05-12)
- **Doc 28 (this) — Frank 3-Lane POST-Remediation Audit** (current state reference)

**Source artifacts:**
- `game_explorations/rts-arc-trace/passage_catalog.json` — 1.2 MB, 361 passages, captured 2026-04-29 (engine: SugarCube). All RTS pattern claims in this doc cite passages by name extractable from this file.
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — current shipped Frank state. All TLS claims cite file:line in this file as of 2026-05-12.

**Engine code (TLS):**
- `apps/projects/services/template_import.py`:
  - `:382` `TemplateTrigger` dataclass (where `entry_only_from`, `substitutions`, `substitution_only` schema fields live)
  - `:1028-1030` parser for `entry_only_from`
  - `:1047` parser for `substitution_only`
  - `:2352-2364` validator for `entry_only_from` (rejects on non-`random` mode)
  - `:2387-2391` validator: substitution_only + npc warning
  - `:2513` validator: overlap-check exclusion for substitution_only canvases (Pass 6 fix)
  - `:4354-4356` serializer pass-through for both fields
- `apps/game_generation/twee_comprehensive/generators/v1.py`:
  - `:2143` `setup.canvasSubstitutions` global emission
  - `:4008-4026` L2-2 `entry_only_from` runtime check inside `checkRandomEncounters` (uses native SugarCube `previous()`)
  - `:4068-4087` `setup.checkAndSubstituteCanvas` runtime helper (returns target passage NAME, not boolean — Pass 6 fix)
  - `:9263` build-time slug→passage map for `entry_only_from`
  - `:9346-9379` `substitution_only` flag emission + selector skip metadata
  - `:9354-9360` build-time slug→passage translation for `entry_only_from`
  - `:10305-10307` substitution emitter injection at canvas Node 1 top (uses `<<set _sub_target>>+<<if>>+<<goto>>` — Pass 6 fix)
  - `:11833-11920` L1-2 image pool emitter (`<<set _img to either(...)>>` + `<img @src="_img">`)

**Test classes (`apps/projects/tests.py`):**
- `SubstitutionsRoundTripTests` + `SubstitutionsValidatorTests` + `SubstitutionsEngineEmissionTests` — 17 tests covering Lane 3 substitution mechanism (Pass 5)
- `EntryOnlyFromTests` — 9 tests covering L2-2 anti-toggle gate
- `ImagePoolTests` — 5 tests covering L1-2 image pool emitter
- **Total: 31 tests passing as of 2026-05-12**

**Memory artifacts (`~/.claude/projects/.../memory/`):**
- 17 `frank_fix_*.md` entries documenting each atomic unit shipped during remediation
- 6 entries flagged for AUDIT CORRECTION (per the cross-lane synthesis above)

---

End of audit.
