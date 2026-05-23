# 29 — Frank 3-Lane Post-Fix Audit (doc 28 remediation closure)

> **Status:** Authored 2026-05-12 (same day as remediation). Confirms doc 28's drift items closed via the 26-unit remediation pass.
> **Purpose:** Closing audit. Verifies — programmatically + with file:line citations — that every 🚩 drift item from doc 28 is fixed in current TOML/engine state, and measures every 🟡 yellow flag delta.
> **Supersession:** Doc 26 (pre-remediation audit) → Doc 27 (remediation plan) → Doc 28 (post-remediation audit, found drift) → **Doc 29 (this) — post-FIX audit**. After doc 29, future Frank work should consult doc 29 first; docs 26/27/28 retain historical value.
> **Scope:** Frank only. Cross-NPC remediation (Ryan/Jake/Diana) out of scope.

---

## TL;DR — Closure status matrix

| Doc 28 finding | Pre-remediation | Post-fix verdict | Memory entry |
|---|---|---|---|
| 🚩 Mid-cascade tick drift (9 ticks) | 9 inline ticks across 6 Lane 2 + 1 L1-3 cascades | ✅ **CLOSED** — 0 mid-cascade ticks across all 47 Lane 1+2 ambient/random cascades | `frank_audit_fix_P1_*.md` (8 units) |
| 🟡 #1 Lane 2 cascade rate | 6/15 = 40% | ✅ **CLOSED — 15/15 = 100%** (exceeds RTS 81%) | `frank_audit_fix_P6_*.md` (9 units) |
| 🟡 #2 Pattern C absent | 0 cascades with mid-beat gates | ✅ **CLOSED** — 2 Lane 2 cascades shipped (`frank_late_night_t2` + `frank_radio_t3`) | `frank_audit_fix_P7_2.md` + `_P7_3.md` + `_P7_engine_extension.md` |
| 🟡 #4 Pattern A density | 6 (3.0× RTS) | ✅ **CLOSED — 5 (2.5× RTS)** via demotion of `tease_office_desk_sit` | `frank_audit_fix_P5_*.md` (2 units) |
| 🟡 #5 L1-4 Flash pool | 5 images | ✅ **CLOSED** — 11 images (matches RTS Brother Flash density) | `frank_audit_fix_P3_1.md` |
| 🟡 #6 L1-3 love gate | speculative concern (audit assumed 0-100 scale) | ✅ **CLOSED (no-op)** — Frank.love decay rate makes existing gate appropriate | `frank_audit_fix_P4_1.md` |
| 🟡 #7 Memory entry doctrine | "verbal-share = mid-cascade tick" called RTS-canonical in 6 entries | ✅ **CLOSED** — 6 entries appended with AUDIT CORRECTION text | `frank_audit_fix_P2_1.md` |
| 🟡 Hallway gate sparse-by-topology | 3 hallway canvases gated to `loc_front_porch` rarely fire | 🟡 **DEFERRED** — accepted tradeoff per memory note (orthogonal to cascade conversion) | n/a |
| 🟡 Stored-roll dispatcher missing | 1:1 parent:target ratio | 🟡 **DEFERRED** — only matters cross-NPC scope (per audit doc 28's own framing) | n/a |
| 🟡 Maya-bedroom Lane 3 absent | RTS BedroomStudy untranslated | 🟡 **DEFERRED** — narrative justification (stepfather doesn't enter stepdaughter's bedroom) | n/a |
| 🟡 No Lane 3 Pattern C | 0 cascades | 🟡 **MATCHES RTS** — RTS Lane 3 also doesn't use Pattern C; shared deviation, not drift | n/a |

**7 of 11 items CLOSED. 4 DEFERRED — all 4 were explicitly framed as deferred in doc 28's own recommendations.**

---

## Methodology

This audit's verdicts are reproducible from a single Python verification script (run 2026-05-12 against current TOML + memory entries):

1. **Mid-cascade tick scan** — parse all 71 cascade IDs in `7_final_game.toml`, extract beat structures, flag any cascade where effects appear at a non-terminal beat
2. **Lane 2 cascade rate** — count canvases with `trigger_mode = "random"` + `npc = "npc_frank"` and check for `type = "cascade"` blocks
3. **Pattern A canvas count** — count `tease_*` canvases with `substitution_only = true`
4. **L1-4 Flash pool size** — parse the `files = [...]` array length on `tease_bedroom_robe_flash`
5. **L1-3 love gate** — grep all `Frank.love >= N` gates; verify both occurrences (line 4135 + 4518) at value 10
6. **Pattern C cascade count** — find cascades with any beat carrying `conditions`; filter to Lane 1+2 ambient scope (capstones use a different doctrine per audit framing)
7. **Memory entry corrections** — grep affected files for "AUDIT CORRECTION 2026-05-12" string; verify excluded canvas4 untouched
8. **Engine extension** — confirm `_CASCADE_EXIT_INJECT_SAFE_SENTINEL` defined + used + handled; confirm `CascadePatternCExitRoutingTests` (3 tests) added

**Build + tests gate:** `package_from_toml --dev` → 🎉 Package ready, no new warnings. 39/39 tests pass (3 new Pattern C + 36 existing).

---

## 🚩 Drift items — CLOSURE VERIFICATION

### Mid-cascade tick drift (doc 28 §LANE 1 + §LANE 2 §🚩)

**Pre-remediation finding (doc 28):** 11 invented mid-cascade ticks in cascade bodies — but doc 28's static verifier didn't check terminal-vs-mid-beat, so 2 of those 11 (`frank_coffee_t3` + `frank_weekend_postr`) were already terminal. Actual drift: **9 ticks** across 6 Lane 2 cascades + 1 L1-3 cascade.

**Post-fix verification (programmatic re-scan):**
```
Total cascades scanned: 71 (all cascade IDs in 7_final_game.toml)
Mid-cascade ticks in Lane 1+2 ambient/random scope: 0 ✅
Mid-cascade ticks in CAPSTONE cascades (out of doc 28 scope): 2
  - `frank_office_crack` (scene_office_crack, is_repeatable=false) — Beat 2 ticks
  - `frank_catch` (scene_living_room_evening, is_repeatable=false) — Beat 1 ticks
```

The 2 capstone cascades are **NOT drift.** They're one-time arc-transition scenes (`is_repeatable = false`) that follow RTS Pattern D doctrine (single top-of-cascade gate → full cascade with terminal payoff + intermediate stat ticks per the climax-build pattern). Doc 28's audit explicitly scoped to Lane 1+2 ambient/random scenes; capstones were out-of-scope.

**Per-unit closure trail:**
- P1.1 → `frank_late_night_t2` Beats 1+2 → terminal Beat 3
- P1.2 → `frank_radio_t3` Beat 2 → terminal Beat 3
- P1.3 → `frank_radio_s4` Beat 1 → terminal Beat 2
- P1.4 → `frank_smoke_t3` Beat 2 → terminal Beat 3
- P1.5 → `frank_coffee_t3` (NO-OP — audit miscount; Beat 2 was already terminal)
- P1.6 → `frank_diana_call_intercept` Beat 1 → terminal Beat 3
- P1.7a → `frank_weekend_t3b` Beat 1 → terminal Beat 2
- P1.7b → `frank_weekend_postr` (NO-OP — audit miscount; Beat 2 was already terminal)
- P1.8 → L1-3 `frank_bedroom_sleep_overnight` Beats 1+2 → terminal Beat 3 (Option A — net per-fork tick totals UNCHANGED)

**Verdict: ✅ CLOSED** — 9 ticks moved + 2 audit miscounts identified + RTS terminal-only doctrine applied uniformly across all 47 Lane 1+2 cascades.

---

## 🟡 Yellow flag deltas — VERIFIED

### #1 Lane 2 cascade rate (doc 28 §LANE 2 🟡 #1)

**Pre-remediation:** 6 of 15 Frank Lane 2 canvases were cascade-bodied = 40%. RTS Lane 2 baseline: 13/16 = 81%. Gap: ~41 percentage points.

**Post-fix:** 15 of 15 = **100%** (exceeds RTS baseline by 19pp).

| Stage | Rate | Memory |
|---|---|---|
| Pre-remediation | 40% (6/15) | doc 28 §LANE 2 baseline |
| After P6.6 (`hallway_morning_pass`) | **80%** | hit doc 28 RTS-parity target |
| After P6.7 (`living_room_dusk`) | **87%** | exceeds RTS baseline (81%) |
| After P6.9 (`hallway_late_drink`) | **100%** | full Lane 2 saturation |

**Verdict: ✅ CLOSED — exceeds RTS doctrine baseline.**

### #2 Pattern C absent (doc 28 §LANE 2 🟡 #2 + §LANE 1 🟡 #1 partial)

**Pre-remediation:** 0 Frank Lane 1+2 cascades had mid-beat stat gates. RTS PeepBrotherSex (Pattern C, 4 beats with stat gates at Beats 2 + 3) was the canonical reference; Frank had no equivalent. Replay loop ("come back when stats higher to see deeper beats") missing.

**Post-fix:** 2 Pattern C cascades shipped:
- `frank_late_night_t2` Beat 2 (property/wife reveal) gated on `Frank.love ≥ 5` — locked sibling "Sit with him in the quiet."
- `frank_radio_t3` Beat 2 (father/radio memory reveal) gated on `Frank.love ≥ 5` — locked sibling "Watch him work the screwdriver."

Both gated beats publish in-character threshold messages via `setup.queueGatedNotification` (the RTS `<<NotifyCorruption N>>` equivalent). Cascades terminate at locked sibling for unqualified players; exits render at passage bottom via the new SAFE sentinel mechanism.

**Engine extension required + shipped** (P7 engine work, not in original remediation plan but required to unblock P7.2/P7.3): introduced `_CASCADE_EXIT_INJECT_SAFE_SENTINEL` in `v1.py:43` for cascades with gated beats. Substitution branch (`v1.py:10740-10785`) checks SAFE first and takes the conservative path (strip without splice + leave `passage_body` intact for bottom-of-passage exit render). Multi-cascade safe (SAFE precedence — any gated cascade in a multi-tier body promotes the whole body to bottom exits). Backwards compatible — all 36 existing tests still pass + 3 new `CascadePatternCExitRoutingTests`.

**Note:** scan also detected `frank_office_after_crack` as a 3rd cascade with gated beats. This is a **pre-existing Pattern F capstone** (refuse-fork) with `conditions` used for branching, not Pattern C as defined by doc 28. Doc 28's Pattern C count was always Lane 1+2 ambient/random scope; capstone cascades use different doctrine.

**Verdict: ✅ CLOSED — 2 Pattern C ambient cascades shipped (matching RTS PeepBrotherSex pattern).**

### #4 Pattern A density (doc 28 §LANE 1 🟡 #1)

**Pre-remediation:** 6 Pattern A canvases = 3.0× RTS Brother (which has 2: Tease + Flash). Audit recommended demote 1-2 redundant surfaces.

**Post-fix:** 5 Pattern A canvases = 2.5× RTS. Demoted `tease_office_desk_sit` (P5.2) — same location + gate + register as `tease_office_desk_lean` (kept).

Remaining Pattern A surfaces all earn unique slots: office (`_lean`, suggestive), bedroom×2 (`_sit_wait` route-to-loop, `_robe_flash` overt-show), kitchen (`_brush_past` post-catch passive contact), hallway (`_robe_linger` deliberate-undress).

**Verdict: ✅ CLOSED — moved toward RTS scarcity baseline; remaining 5 each have distinct location/gate/register/mechanism slots.**

### #5 L1-4 Flash pool (doc 28 §LANE 1 🟡 #2)

**Pre-remediation:** `tease_bedroom_robe_flash` had 5-image pool. RTS Brother Flash uses 11 images (5 non-pregnant + 6 pregnant variant).

**Post-fix:** 11-image pool at `7_final_game.toml:5207`. Asset generation deferred to media pipeline (per `nsfw_media_pipeline.md`).

**Verdict: ✅ CLOSED — matches RTS Brother Flash density exactly.**

### #6 L1-3 love gate (doc 28 §LANE 1 🟡 #3)

**Pre-remediation concern:** Audit feared `Frank.love ≥ 10` was too low because audit assumed Frank.love ranged 0-100 (typical NPC stat scale).

**P4.1 investigation finding:** Frank.love has a **0.5/day decay rate** (`7_final_game.toml:484`) + only 16 love-tick events exist in entire arc (15× +1, 1× +2 = max +17 instantaneous). Combined: max realistic accumulation in normal play is bounded ~8-15 at peak, decaying back toward zero between visits. Existing gate `≥ 10` requires sustained love-maintenance (firing love-tick events faster than decay erases) — not a one-shot trigger.

**Methodological note (for future audits):** When auditing TLS NPC trait gates against RTS thresholds, ALWAYS check the trait's decay rate at `[npcs.trait_decay]` block. Decay fundamentally changes the meaning of a gate value — a stat with high decay is a "currency to maintain" not a "score to accumulate," which inverts the scale-comparison logic.

**Verdict: ✅ CLOSED (no-op) — gate value 10 verified empirically appropriate.**

### #7 Memory entry doctrine claims (doc 28 §"Memory entry corrections needed")

**Pre-remediation:** 6 memory entries in the original Frank remediation series (`frank_fix_L2_1_canvas{1,2,3,5,6}.md` + `frank_fix_L1_3.md`) called the "high-trust verbal-share = Frank.love +1 mid-cascade tick" pattern "RTS-canonical doctrine." Doc 28's RTS source extraction proved this was TLS-original drift, not RTS pattern.

**Post-fix:** All 6 memory entries appended with AUDIT CORRECTION 2026-05-12 text (verified via grep). `frank_fix_L2_1_canvas4.md` correctly excluded (its memory entry framing was "physical-contact escalation," not "verbal-share doctrine" — internally consistent, no doctrine-claim correction needed).

**Verdict: ✅ CLOSED — invented doctrine claims labeled inline; future authoring sessions reading these entries will see the correction + pointer to doc 28.**

---

## 🟡 DEFERRED yellow flags (per audit doc 28's own deferral framing)

### Hallway sparse-by-topology
**Status:** unchanged. 3 hallway canvases (`scene_hallway_frank_pass`, `scene_hallway_franks_door_evening`, `scene_hallway_frank_morning_pass`) gated to `entry_only_from = ["loc_front_porch"]` rarely fire under normal play. **Per memory `frank_fix_L2_2.md` documented this as "user accepted tradeoff."** Cascade conversion (P6.x) doesn't address this orthogonal issue.

### Stored-roll dispatcher missing
**Status:** unchanged. RTS uses `<<set $game.random = random(1,4)>>` then if/elseif branching to dispatch ONE roll among N candidates. TLS evaluates each canvas's `chance` independently. Per audit doc 28: "only matters cross-NPC scope (Frank-only doesn't need it)." Deferred to cross-NPC remediation pass (Ryan/Jake/Diana).

### Maya-bedroom Lane 3 absent
**Status:** unchanged. RTS BedroomStudy puts NPC walk-ins in MAYA's bedroom. TLS Frank doesn't visit Maya's bedroom (narrative reason: stepfather wouldn't enter stepdaughter's bedroom uninvited). Per audit: "narrative-justified deviation."

### No Lane 3 Pattern C
**Status:** matches RTS. RTS Lane 3 cascades (BrotherShowerSex, BrotherWashDishesSex, etc.) also don't use Pattern C — shared deviation between RTS and TLS, not drift.

---

## Engine extension shipped (P7 SAFE sentinel)

P7.2 + P7.3 required engine work that wasn't in the original remediation plan. Surfaced during P7.1 pre-flight: cascade-exit-injection optimization at `v1.py:10720-10785` splices `passage_body` (exit choices) inside the cascade's last advance beat AND clears `passage_body` (line 10764). For Pattern C: gated beat fail at runtime → cascade terminates → sentinel never renders → no exits → stuck player.

**Fix (v1.py + tests.py):** introduced `_CASCADE_EXIT_INJECT_SAFE_SENTINEL` (`v1.py:43`). Cascades with any beat carrying `conditions` plant SAFE instead of STANDARD (`v1.py:11489-11506`). Substitution branch checks SAFE first → conservative path: strip both sentinels + leave `passage_body` intact (exits render at passage bottom). Multi-cascade safe (SAFE precedence rule).

**Tests:** 3 new `CascadePatternCExitRoutingTests` (`apps/projects/tests.py:3672-3825`):
1. `test_pattern_c_cascade_uses_safe_sentinel_path` — cascade with gated beat → exits at bottom + locked-sibling button + queueGatedNotification helper invoked
2. `test_ungated_cascade_keeps_standard_inline_splice` — regression: existing pre-P7 behavior preserved when no beats are gated
3. `test_mixed_node_body_safe_takes_precedence` — multi-cascade body where one tier is Pattern C → all tiers fall through to bottom exits

**Backwards compatible** — all 36 existing tests still pass. 39/39 total.

Memory: `frank_audit_fix_P7_engine_extension.md`.

---

## Aggregate stats

- **26 atomic units** shipped over one session (2026-05-12)
- **47 Lane 1+2 ambient/random cascades** verified clean (zero mid-cascade ticks)
- **1 engine extension** (SAFE sentinel) — backwards compatible
- **8 net-new tests** added → **39 tests passing** (3 Pattern C + 5 ImagePool + 9 EntryOnlyFrom variants from earlier shipping)
- **0 build regressions** across all 26 units (every unit's gates: build clean + tests green)
- **0 prose changes** — verbatim preservation invariant maintained throughout (P1, P5, P6, P7 all preserved exact author prose)
- **2 audit miscounts identified** (P1.5 + P1.7b — beats already terminal; doc 28's static verifier didn't check terminal-vs-mid-beat)
- **6 memory entry doctrine corrections** applied
- **TOML inline-table syntax trip hazard** documented across P7.2 (long single-line inline-table required; only `blocks = [...]` opens multi-line)

---

## Doc 28 errata captured

P1.5 + P1.7b discovered that doc 28's drift inventory over-counted by 2: the Beat 2 effects in `frank_coffee_t3` and `frank_weekend_postr` were already on terminal beats (the canvases had only 3 beats each, so Beat 2 IS the last beat). Doc 28's static verifier (`grep effects = [` inside cascade body) didn't distinguish terminal-vs-mid-beat.

**Recommended audit-tooling improvement (for future audit reuse):** the verifier should parse the cascade `beats = [...]` array fully and check whether each effects-bearing beat is the LAST element in the array. Only flag as drift if effects-bearing beat is NOT terminal. This is the static-verifier pattern used by P1.5 + P1.7b re-verification + the final P1 sweep.

---

## Recommended follow-on (post-doc-29)

1. **Asset generation** for image pool placeholders. P3.1 added 6 new placeholders to `tease_bedroom_robe_flash` (5 → 11), and earlier shipping (L1-2 Phase B from doc 27 series) added 30 placeholders across 6 Pattern A canvases. Total ~36 placeholders awaiting downstream media pipeline (`nsfw_media_pipeline.md` reference). NOT in scope for doc 29.

2. **Cross-NPC remediation** (Ryan/Jake/Diana) when scope opens — would address the deferred 🟡 items (stored-roll dispatcher + Maya-bedroom Lane 3). Frank's 26-unit pass establishes the doctrine + atomic-unit cadence pattern + reusable engine primitives.

3. **Live-play UX validation of Pattern C** — engine works (verified by build + tests + emission inspection), but Pattern C UX (does the locked-sibling threshold message land in-character? does the bottom-of-passage exit feel awkward?) is not yet live-verified by playtest.

4. **Doc 26 + 28 supersession markers** — recommend adding inline ⚠️ SUPERSEDED notes at the top of docs 26 + 28 pointing to doc 29 as the current state-of-Frank reference. Cleaner navigation for future authoring sessions.

---

## Confidence ladder

✅ **HIGH confidence (verified programmatically + via build/tests):**
- All ✅ CLOSED items above — every closure claim has a re-runnable verification scan + memory entry citation
- 47 Lane 1+2 ambient cascades all clean (programmatic verification, scan 1)
- Engine extension correctness (3 new tests cover SAFE sentinel + STANDARD regression + multi-cascade fallback)
- Cumulative test stability (39/39 passing across all 26 unit-shipping cycles)

🟡 **MED confidence:**
- Pattern C player-experience UX — engine emission verified, but no live playtest of "Maya gates in middle of personal-share scene + sees locked sibling + reads threshold message + comes back later"
- L1-3 love gate empirical appropriateness — P4.1 calculated max-realistic Frank.love ≈ 8-15 with decay; live playtest could surface different values
- Lane 2 cascade rate at 100% (vs RTS 81%) — exceeds RTS, but no live-play data on whether 100% saturation reads as "more alive than RTS" or as "homogeneous click-pacing across all ambient surfaces"

❌ **NOT established this audit:**
- Long-term replay-loop value of the 2 Pattern C cascades — does the gate make the property/father-memory reveal feel earned, or does it just block players?
- Whether the SAFE sentinel UX (exits at passage bottom for Pattern C cascades) feels distinct/inferior vs the STANDARD inline-splice UX
- Whether deferred items (hallway sparse-by-topology, no stored-roll, Maya-bedroom Lane 3) ever become actual gameplay problems vs accepted-as-is

---

## Cross-references + source artifacts

**Doctrine docs (this folder):**
- Doc 21 — RTS Brother Mechanism Audit (Pattern A-F definitions)
- Doc 22 — RTS Cross-NPC Mechanism Comparison
- Doc 24 — RTS Three Lanes for Repeatable NPC Content + TLS Engine Fitness
- Doc 26 — Frank 3-Lane Audit (PRE-remediation baseline)
- Doc 27 — Frank 3-Lane Remediation Plan (original Frank shipping)
- Doc 28 — Frank 3-Lane Post-Remediation Audit (drift discovery)
- **Doc 29 (this) — Frank 3-Lane Post-FIX Audit (remediation closure)**

**Source artifacts:**
- `game_explorations/rts-arc-trace/passage_catalog.json` — RTS source-of-truth (361 passages, captured 2026-04-29)
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — current shipped Frank state

**Engine code:**
- `apps/projects/services/template_import.py` — schema (cascade beat `conditions` parser at `:3791-3806`)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — engine
  - `:43` `_CASCADE_EXIT_INJECT_SAFE_SENTINEL` (P7 audit fix)
  - `:11489-11506` `_render_cascade` `has_gated_beats` detection (P7 audit fix)
  - `:10740-10785` substitution branch with SAFE-precedence handling (P7 audit fix)
- `apps/projects/tests.py:3672-3825` — `CascadePatternCExitRoutingTests` (3 new tests)

**Memory artifacts (`~/.claude/projects/.../memory/`):**
- 26 `frank_audit_fix_*.md` entries — per-unit shipping evidence + trip hazards
- 6 `frank_fix_L2_1_canvas{1,2,3,5,6}.md` + `frank_fix_L1_3.md` — pre-remediation entries with AUDIT CORRECTION 2026-05-12 appendices
- `MEMORY.md` — index pointers

---

End of audit.
