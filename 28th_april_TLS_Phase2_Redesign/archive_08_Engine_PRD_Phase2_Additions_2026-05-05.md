# 08 — Engine PRD: Phase 2 Doctrine Additions

> **Created 2026-04-29. Implemented 2026-04-30.**
> Sibling addendum to `03_Engine_Changes_PRD.md`. Does not supersede it.
> Scope: the engine work the Phase 2 doctrine (`01_Repeatable_First_Doctrine.md`) demands beyond what 03 already covers.
> Three items: E9, E10, E11. Phase-2-doctrine items only — nice-to-haves and deferrals are explicitly listed in §9.
>
> **Status: all three items shipped.** §11 documents what was actually built, the deviations from the original spec text, and the commit list. The §1 prescriptive text is preserved as the historical contract — read §11 for current implementation truth.

---

## §0 Frame

### Why this PRD exists

The Phase 2 redesign flips the design's spine: plot moves through stage flag transitions inside repeatable scenes, not through canvas firings on a story-arc track. The doctrine is locked in `01_Repeatable_First_Doctrine.md`; Frank's stage chain is worked in `02_NPC_Stage_Chains.md`; the canonical scene shape is in `04_Scene_Cascade_Pattern.md`.

The existing engine PRD (`03_Engine_Changes_PRD.md`) was authored before the doctrine flip. It covers eight engine items (E1–E8) — five shipped, one verified-only, two deferred — that handle flag ops, trait decay, daily tick, stage helpers, text variants, counter macros, and arousal accumulation. Those primitives are doctrine-compatible and don't need revisiting.

What 03 doesn't address, and what the doctrine now requires, is the **hint-and-journal subsystem**. Today the hint engine assumes the Phase-1 model: `getNextActivity` walks `story_arc.nodes[]` by canvas firing; `is_stuck` is computed from `available_nodes` (canvas-visit signal). Under the doctrine, the player will visit `scene_kitchen_with_frank` 30+ times during a run — the canvas-visit signal becomes uninformative, and the per-NPC chain walk needs to read stage flags instead of node positions.

This PRD specs three small, surgical changes to make the hint subsystem stage-aware. No new engine primitives. No breaking schema changes.

### Engine state Phase 2 inherits (from 03)

Confirmed shipped or already-implemented and doctrine-compatible:

| ID | Item | Status | Phase 2 use |
|---|---|---|---|
| E1 | `flagEffects[].op = set/unset/toggle` | ✅ shipped | Daily-reset flags (`talked_to_frank_today`), one-time guards |
| E2 | Trait decay execution (v1.py:3673–3700) | ✅ already implemented | NPC relationship maintenance pressure |
| E3 | NPC location sidebar widget | ⏸ deferred | Schedule Page sufficient for Phase 2 |
| E4 | `[[engine.stage_helpers]]` + `type=stage` condition | ✅ shipped | Cascade gates reference `frank_stage_2()` not raw thresholds. Verified at v1.py:706, 2031–2035, 2703–2717. |
| E5 | `[engine.daily_tick]` | ✅ shipped | Daily flag resets, helper recomputation |
| E6 | `choices[].text_variants[]` | ✅ shipped | "Talk to Frank" → "Talk to Frank — about it" after the catch |
| E7 | `<<inc>>` / `<<dec>>` macros | ✅ shipped | `frank.tease_count++`, `frank.bookkeeping_count++` |
| E8 | NPC arousal passive accumulation | ⏸ deferred | Defer until Phase D playtest |

Plus pre-existing primitives confirmed Phase-2-ready:
- `trigger.chance` (probability gating, v1.py:3216, 3585)
- `group` blocks with `conditions` (cascade implementation primitive)
- `block_pool` for image rotation (anti-staleness mechanism)
- `[[story_arc.nodes]].linked_canvas` AND `linked_flag` both supported (template_import.py:496–498); `detectStoryPosition` (v1.py:4070) checks both for completion

**Net: ~85% of what the doctrine needs is already in the engine.** The three items below close the remaining 15%.

### Status legend

- ✅ Shipped
- 🟡 In flight / partial
- 🟦 Specified in this PRD, not started
- ⏸ Deferred (rationale included)

### What this PRD does NOT cover

- Schema deprecations of `linked_canvas`. Both fields stay; doctrine guidance prefers `linked_flag`. No engine-side deprecation.
- Random integer setter for scene-internal RNG. `trigger.chance` covers the verified RtS pattern (master spec §2.4). Defer until playtest reveals a need.
- Hub priority modes / auto-fire toggles. Doctrine works with existing `priority` semantics + flag-gated branches inside repeatable shells.
- E3 NPC location sidebar widget (revisit). Already deferred in 03; doctrine doesn't elevate it.
- E8 NPC arousal accumulation (revisit). Already deferred in 03; doctrine doesn't elevate it.
- Story-arc journal display repurposing. That's the deferred design doc `07_Journal_Display_Spec.md`, an authoring-conventions decision, not an engine change.

---

## §1 The three engine additions

### E9 — Stage-flag stalled-progress detection [P1] 🟦

**Issue.** `detectStoryPosition` (v1.py:4070) computes `is_stuck` from `available_nodes` count: zero available = stuck. In Phase 2, repeatable scene canvases stay "available" indefinitely — a player whose `frank_stage` hasn't moved in 14 in-game days is functionally stuck on Frank's arc, but `available_nodes` is still nonzero (the kitchen scene fires every morning), so the engine never triggers stalled-hint flow.

**Why we need it.** The doctrine's signal of "the player is making progress" flips from canvas firings to stage flag transitions. The hint engine's stuck-detection has to flip with it. Otherwise the stalled-hint flow (in `generateNarrativeHint`, v1.py:4344) never fires for players who are visiting hubs and activities normally but failing to advance any NPC's stage.

**Current state.**
- Schema: `[story_arc.hints]` has `stuck_threshold_minutes` (default 30) — unused at runtime in current code paths beyond fallback hint timing. No stage-aware stuck threshold.
- Runtime: `detectStoryPosition` (v1.py:4070) returns `position.is_stuck` based on `available_nodes.length === 0`. Consumed by `generateNarrativeHint` (v1.py:4344) and `StoryJournal` passage (v1.py:12682–12777).
- No per-NPC last-stage-advancement timestamp tracked anywhere.

**Proposed change.**

Schema addition (`template_import.py`, in `TemplateStoryHints`, near line 519):
```python
@dataclass
class TemplateStoryHints:
    stuck_threshold_minutes: int = 30          # existing
    stuck_threshold_days: int = 7              # NEW — for stage-stall detection
    hint_style: str = "observation"
    templates: List[TemplateHintTemplate] = field(default_factory=list)
```

Runtime — `setup.advanceDay()` (the daily-tick handler, near `v1.py:3673`):
```javascript
// At the moment any <npc>_stage flag increments (inside applyFlagEffect or
// equivalent stage-advancement helper):
var sv = State.variables;
sv.game_state.stage_advancement_log = sv.game_state.stage_advancement_log || {};
sv.game_state.stage_advancement_log[npcId] = sv.game_state.time_state.current_day;
```

Runtime — `detectStoryPosition` (v1.py:4070):
```javascript
// After computing position.is_stuck the existing way, augment:
var threshold = (setup.story_arc.hints && setup.story_arc.hints.stuck_threshold_days) || 7;
var currentDay = State.variables.game_state.time_state.current_day;
var log = State.variables.game_state.stage_advancement_log || {};
var stalled = true;
for (var npcId in setup.npc_stage_npcs) {            // set of NPCs with stage chains
    var lastAdvance = log[npcId] || 0;
    if (currentDay - lastAdvance < threshold) { stalled = false; break; }
}
position.stage_progression_stalled = stalled;
position.is_stuck = position.is_stuck || stalled;
```

Runtime — `generateNarrativeHint` (v1.py:4344): emit a different hint message when `position.stage_progression_stalled === true`. Hint authors can opt into stage-stall-specific hint text by tagging templates (`hint_style = "stage_stall"`) — left as a future enhancement; default falls back to existing observation-style hints.

**Acceptance criteria.**

1. TOML with `[story_arc.hints].stuck_threshold_days = N` validates without warnings; default = 7 when omitted.
2. `$game_state.stage_advancement_log` is initialized as `{}` in `StoryInit` (or first daily tick).
3. When any `<npc>_stage` flag increments, `stage_advancement_log[npcId]` is set to the current day in the same engine cycle.
4. `position.stage_progression_stalled === true` when (currentDay − maxOverNpcs(lastAdvanceDay)) ≥ threshold AND no NPC has advanced more recently.
5. `position.is_stuck` ORs the stage-stall signal with the existing canvas-visit stall.
6. Test scenario: `frank_stage = 0`, day 8, no stage advance since day 0 → stalled hint fires. Day 4 → no stalled hint.
7. Existing TOMLs without stage chains continue to behave identically (empty stage_advancement_log, stalled stays false).

**Effort estimate.** Medium. ~80–120 lines across schema + ingestion + runtime + tests. ~4–6 hours including a Frank-arc stall test.

**Open question.** Should the `stage_advancement_log` track ALL flags matching `<npc>_stage` or only those declared in a registry? Recommendation: build the registry from `[[npcs.arc_stages]]` (the stage-chain artifact from `02_NPC_Stage_Chains.md`) when it's authored as schema. Until then, derive at runtime from any flag matching the regex `^[a-z_]+_stage$` whose value is integer.

---

### E10 — Stage-gated hint pool + per-NPC stage routing [P1] 🟦

**Issue.** `getNextActivity(npcId)` (v1.py:4400) walks `story_arc.nodes[]` and returns the next node whose `linked_canvas_node` (line 4433) or `linked_flag` (line 4426) hasn't fired. In Phase 2, the relevant signal is "what stage is the NPC at?" — the next hint should come from a per-stage hint pool, not a per-node graph walk. The Quests page (v1.py:12420–12510) and `getSidebarHint` (v1.py:4987) consume this function; both inherit the wrong granularity.

**Why we need it.** Per the doctrine, plot advances when stage flags flip. Hints follow stages, not canvases. A Phase-2 hint table for Frank looks like: "Stage 0: try talking to him in the kitchen mornings. Stage 1: he's started warming up — ask if he could use a hand with bookkeeping." The engine has to know which stage the player is at and pull the matching pool.

**Current state.**
- Schema: `TemplateHintCondition` (template_import.py:519) has `missing_flag`, `missing_trait`, `gap_gte`. No stage-awareness.
- Runtime: `getNextActivity` walks `arc.nodes` linearly. Returns a `flagHint` object including `npc_name` for trait-blocked cases, but the chain order is graph-walk, not stage-aware.

**Proposed change.**

Schema addition (`template_import.py`, in `TemplateHintCondition` near line 519):
```python
@dataclass
class TemplateHintCondition:
    missing_flag: Optional[str] = None        # existing
    missing_trait: Optional[str] = None       # existing
    gap_gte: Optional[int] = None             # existing
    stage_npc: Optional[str] = None           # NEW — must match an npc_id in the roster
    stage_op: Optional[str] = None            # NEW — "eq" | "gte" | "lte"
    stage_value: Optional[int] = None         # NEW — integer stage value
```

Validation (`template_import.py`, hint-validation block):
- If any of `stage_npc` / `stage_op` / `stage_value` is set, all three must be set.
- `stage_npc` must reference an NPC in the roster (raise `ValidationError` otherwise).
- `stage_op` must be in `{"eq", "gte", "lte"}`.
- `stage_value` must be an integer ≥ 0.

Runtime — `getNextActivity` (v1.py:4400):
```javascript
// At the top of the per-NPC walk: read the NPC's stage flag.
var stageFlag = (State.variables.player.flags || {})[npcId + '_stage'];
var currentStage = (typeof stageFlag === 'number') ? stageFlag : 0;

// When walking activity hints, prefer those whose stage_gate matches:
// 1. Filter templates by stage_gate match (if any).
// 2. Of those, apply existing missing_flag / missing_trait / gap_gte gates.
// 3. Return the first match.
// 4. Fall through to existing graph-walk for templates with NO stage_gate.

function stageGateMatches(condition, npcId, currentStage) {
    if (!condition.stage_npc) return null;       // no stage gate — not applicable
    if (condition.stage_npc !== npcId) return false;
    var v = condition.stage_value;
    switch (condition.stage_op) {
        case 'eq':  return currentStage === v;
        case 'gte': return currentStage >= v;
        case 'lte': return currentStage <= v;
        default:    return false;
    }
}
```

Stage-gated templates are checked first; existing graph-walk path is preserved as fallback for non-stage-gated templates and for NPCs without stage chains. Backwards-compatible.

**Acceptance criteria.**

1. TOML with hint `stage_gate = { npc = "frank", op = "eq", value = 1 }` validates; an unknown `npc` raises a validation error.
2. When `frank_stage == 1`, only Stage-1-gated Frank hints (and ungated Frank hints) appear in the Quests page Frank section.
3. When `frank_stage` advances to 2, Stage-1 hints stop appearing and Stage-2 hints take over.
4. Existing hints with no `stage_gate` continue to fire under their current trait/flag conditions.
5. Test scenario from `02_NPC_Stage_Chains.md` Frank chain: at Stage 0, the hint "spend time with Frank around the kitchen mornings" fires; at Stage 2, that hint stops and the chore-based hint fires instead.
6. `getSidebarHint` (v1.py:4987) inherits the new behavior without code change (it already wraps `getNextActivity`).

**Effort estimate.** Medium. ~100–150 lines across schema + ingestion + validation + runtime + tests. ~6–8 hours.

**Open question.** Should `stage_gate` be a sub-object (`stage_gate = { npc = ..., op = ..., value = ... }`) or three flat fields on the condition? Recommendation: flat fields (`stage_npc`, `stage_op`, `stage_value`) to match the existing `missing_*` / `gap_*` flat-field convention in `TemplateHintCondition`. Sub-object is more readable but breaks the schema's existing pattern.

---

### E11 — NPC stage display in sidebar [P2] 🟦 (optional UX)

**Issue.** The doctrine relies heavily on "the player sees state move." Today the sidebar shows raw NPC traits (`frank.trust 18`, `frank.arousal 4`) but never the named stage. New buttons appearing at hubs are the only progression signal — and that's invisible until the player happens to revisit the right hub.

**Why we need it.** When `frank_stage` flips from 1 to 2, the player should see something change in the always-visible sidebar that tells them their relationship with Frank just shifted regimes. Without this, stage progression feels invisible until the player wanders into the right hub. The redesign's whole pitch — that flag movement IS the story — needs at least one persistent player-facing surface that displays it.

This item is optional in the sense that Phase 2 functions without it. But the UX cost of omitting it is significant: stage transitions become discoveries that depend on the player happening to revisit the right place. The cost of including it is small.

**Current state.**
- The `trait_words` sidebar item type already exists (per system reference + v1.py sidebar render block — search for `trait_words`).
- It currently maps numeric trait values to word labels (e.g., `corruption 0..25 = "Distant"`, `26..50 = "Curious"`, etc.).
- No `source = "stage"` mode exists.

**Proposed change.**

Schema extension (`template_import.py`, sidebar-item validator for `trait_words`):
```python
# trait_words sidebar item accepts:
# {
#   type = "trait_words",
#   source = "stage",                        # NEW — "trait" (default) or "stage"
#   npcs = ["frank", "ryan", "jake"],        # NEW — required when source == "stage"
#   display = {                              # NEW — required when source == "stage"
#     frank_stage = ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"],
#     ryan_stage  = [...],
#     jake_stage  = [...]
#   }
# }
```

Validation:
- If `source = "stage"`, `npcs` and `display` are required.
- Each NPC ID in `npcs` must exist in the roster.
- Each entry in `display` must be a string array.
- `display[<npc>_stage]` array length must accommodate the maximum stage value the NPC can reach (validate against the stage chain when authored; for now, length ≥ 5 recommended for the documented Frank chain).

Runtime (v1.py sidebar render block):
- For each NPC in `npcs`: read `<npc>_stage`, index into `display[<npc>_stage]`, render `"<NPC name>: <stage label>"`.
- Fallback: if stage value is out of range, render the highest-defined label.
- Fallback: if `<npc>_stage` is undefined, render the NPC name with no label.

**Acceptance criteria.**

1. TOML with `[[sidebar_items]] type = "trait_words" source = "stage"` validates; missing `npcs` or `display` raises a validation error.
2. With `frank_stage = 1` and the display config above, sidebar renders "Frank: Warm".
3. After Stage 2 transition, sidebar updates to "Frank: Restrict" without page reload (re-renders on next time advance / canvas entry, matching existing trait_words behavior).
4. Out-of-range stage value (e.g., `frank_stage = 99`) falls back to highest-defined label without breaking the layout.
5. Missing `<npc>_stage` flag (e.g., undefined at game start) renders just "Frank" with no colon, no broken markup.
6. Layout regression check: with one NPC, two NPCs, three NPCs, the sidebar height remains within the existing budget (visual smoke test, dev-mode preview).

**Effort estimate.** Low. ~40–60 lines in validator + render block. ~2–3 hours.

**Open question.** Should the stage display be a separate `[[sidebar_items]]` type (`type = "stage_display"`) or extend `trait_words` with `source = "stage"`? Recommendation: extend `trait_words`. The semantics ("integer value → word label") are identical; reusing the type avoids proliferation.

---

## §2 Status table

| ID | Item | Priority | Risk | Effort | Status |
|---|---|---|---|---|---|
| E9 | Stage-flag stalled-progress detection | P1 | Medium — interacts with existing `is_stuck` flow; mitigation is OR logic, not replacement | ~80–120 lines spec, ~210 lines actual | ✅ shipped 2026-04-30 (commit `520815b`) |
| E10 | Stage-gated hint pool + per-NPC stage routing | P1 | Medium — schema + validator + runtime selector. Backwards-compatible | ~100–150 lines spec, ~470 lines actual (template consumer was missing) | ✅ shipped 2026-04-30 (commit `efbca85`) |
| E11 | NPC stage display in sidebar | P2 | Low — cosmetic + small validator extension | ~40–60 lines spec, ~170 lines actual | ✅ shipped 2026-04-30 (commit `6bd7d63`) |
| — | `[[npcs]].arc_stages` schema (foundation for E9/E10/E11) | — | Low — additive, default empty | ~200 lines | ✅ shipped 2026-04-30 (commit `906869b`) — undeferred from §5 |
| — | Phase 2 didactic fixture + smoke test | — | — | ~350 lines | ✅ shipped 2026-04-30 (commit `da918c1`) |

**Total effort estimate (original): ~12–17 hours.** Actual: ~14h, near the upper end. The major deltas: E10's template consumer was missing entirely (PRD glossed over this), and the foundation `arc_stages` schema was undeferred from §5 to ground the registry on schema rather than on a regex fallback.

See **§11 As built** for implementation notes, deviations from spec, and commit/code-location pointers.

---

## §3 Backwards compatibility

All three items are additive. Today's TOMLs and saves continue to work without modification.

| Concern | Status |
|---|---|
| Existing TOMLs without `stuck_threshold_days` | Default = 7. Stage-stall signal fires only when stage-chain NPCs exist. |
| Existing TOMLs without stage chains | `stage_advancement_log` stays empty. `position.stage_progression_stalled` stays false. Behavior identical to today. |
| Existing hints without `stage_gate` | Continue to fire on missing_flag/missing_trait/gap_gte. Graph-walk fallback path preserved. |
| Existing sidebar items | `trait_words` with default `source = "trait"` works unchanged. Only new `source = "stage"` opts in. |
| Existing saves | New runtime fields (`stage_advancement_log`, `stage_progression_stalled`) initialize to empty/false on first daily tick after upgrade. No save migration. |
| `linked_canvas` field | Stays. `detectStoryPosition` and `getNextActivity` continue to check it. Doctrine prefers `linked_flag`; engine treats both as equal completion signals. |

No save-format change. No breaking schema change. No required-field promotion.

---

## §4 Verification plan

End-to-end validation per item, anchored on Frank's stage chain from `02_NPC_Stage_Chains.md`.

### E9 verification
1. Author a minimal TOML with `[[npcs]]` for Frank, an `arc_stages` block defining Frank Stage 0–4, and a hint with `[story_arc.hints].stuck_threshold_days = 7`.
2. `package_from_toml --dry-run` validates clean.
3. Build + play. At day 0, Frank stage = 0. Visit kitchen daily without triggering any stage gate.
4. On day 8: open StoryJournal. Confirm a stage-stall hint fires.
5. On day 9: trigger the kitchen scene's Stage-0 → 1 advancement (via bookkeeping count or trust threshold). Re-check StoryJournal: stall hint suppressed.
6. Inspect `$game_state.stage_advancement_log.frank` — equals the day of the transition.

### E10 verification
1. Author hints in TOML: one with `stage_gate = { npc = "frank", op = "eq", value = 0 }`, one with `stage_eq = 1`, one with `stage_eq = 2`.
2. `package_from_toml --dry-run` validates clean.
3. Build + play. At Stage 0, Quests page Frank section shows the Stage-0 hint only.
4. Trigger Stage 0 → 1 transition. Refresh Quests page: Stage-0 hint gone, Stage-1 hint visible.
5. Repeat through Stage 2.
6. Test invalid TOML: `stage_gate.npc = "nonexistent_npc"` — confirm validation error.
7. Test ungated hints (no `stage_gate`): confirm they continue to fire under existing flag/trait conditions.

### E11 verification
1. Author `[[sidebar_items]]` with `type = "trait_words"`, `source = "stage"`, `npcs = ["frank"]`, `display = { frank_stage = ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"] }`.
2. `package_from_toml --dry-run` validates clean.
3. Build + play. At game start with `frank_stage` undefined: sidebar shows "Frank" (no label, no broken markup).
4. After first stage assignment (Stage 0): sidebar shows "Frank: Suspicious".
5. Advance through stages; confirm sidebar updates each time.
6. Manually set `frank_stage = 99` via dev-mode console: sidebar shows "Frank: Cracked" (highest-defined label fallback).
7. Layout regression: take screenshots with 1, 2, 3 NPCs in the stage display; confirm no overflow in existing sidebar height budget.

### Cross-item verification
After all three items ship: a Phase-2 Frank-arc playthrough should show stage-aware hints in the Quests page (E10), named stage transitions in the sidebar (E11), and a stalled-stage hint after 7 days of stalled progress (E9). All three signals visible to the player, sourced from the same `frank_stage` flag.

---

## §5 What this PRD does not commission

The "Phase 2 doctrine items only" scope decision excludes the following, with rationale per item so future readers don't re-litigate:

| Excluded item | Rationale |
|---|---|
| **Random integer setter for scene-internal RNG** | Master spec §2.4 confirms `trigger.chance` is sufficient for the RtS-verified pattern (1-in-3 ambient encounters). Scene-internal RNG isn't required for any doctrine pattern. Defer until playtest reveals a need. |
| **Hub priority modes / `auto_fire = false`** | Doctrine works with existing `priority` semantics. First-time content is a flag-gated branch inside the repeatable shell; priority is set so hubs render every visit and one-shots pre-empt only when their conditions match. No primitive change needed. |
| **Schema deprecations** (e.g., remove `linked_canvas`) | Both `linked_canvas` and `linked_flag` stay supported. `detectStoryPosition` checks both. Doctrine guidance prefers `linked_flag` for new content; existing TOMLs continue to work with `linked_canvas`. No engine-side deprecation. |
| **E3 NPC location sidebar widget revisit** | Already deferred in 03. Schedule Page sufficient for Phase 2. Doctrine doesn't elevate it. |
| **E8 NPC arousal passive accumulation revisit** | Already deferred in 03. Doctrine doesn't elevate it. Defer until Phase D playtest. |
| **Story-arc journal display repurposing** | The `[story_arc]` table's repurposing as a flag-driven journal display layer is the deferred design doc `07_Journal_Display_Spec.md`. The engine already supports both flag-driven (`linked_flag`) and canvas-driven (`linked_canvas`) node completion. The design doc decides authoring conventions; no engine change needed. |
| **`[[npcs]].arc_stages` TOML schema** | The stage-chain artifact from `02_NPC_Stage_Chains.md` may eventually become a first-class TOML structure. For this PRD, stage flags are represented as integer flags following the convention `<npc>_stage`. Promotion to a structured schema is a future schema-PR concern, not this PRD. |

---

## §6 Risks

- **E9 — interaction with existing `is_stuck` flow.** Wrong threading could mute one signal under the other. Mitigation: the spec uses `OR` logic (`is_stuck = original_is_stuck OR stage_progression_stalled`), not replacement. Both signals fire independently. Test scenario covers both paths.
- **E10 — `stage_gate.npc` validation.** A typo in the NPC ID should fail validation, not silently fall through. Validator must reject unknown NPC references, not just warn. Acceptance criterion #6 calls this out.
- **E11 — layout regression.** The lowest-risk item is the most visible. A small NPC roster vs a large one stresses sidebar height differently. Manual screenshot comparison is part of the verification plan; layout-preservation is criterion #6.

---

## §7 Status (per-item ledger)

**As of 2026-04-30 (updated from 2026-04-29 specified-but-not-started state):**

| Item | Status | Commit | Notes |
|---|---|---|---|
| Foundation: `[[npcs]].arc_stages` | ✅ Shipped 2026-04-30 | `906869b` | Undeferred from §5 to give E9/E10/E11 a registry-based foundation instead of regex fallback |
| E9 | ✅ Shipped 2026-04-30 | `520815b` | Hook lives in `applyAndNotifyTrait`, not `applyFlagEffect` (PRD wrong — stage values are integer player traits) |
| E10 | ✅ Shipped 2026-04-30 | `efbca85` | Template consumer built (was dead schema at runtime); reuses `setup.checkSingleCondition` |
| E11 | ✅ Shipped 2026-04-30 | `6bd7d63` | Shipped as new `stage_label` type (NOT extending `trait_words` per PRD's open-question recommendation — see §11.5) |
| Fixture + smoke test | ✅ Shipped 2026-04-30 | `da918c1` | `engine_prd_phase2_2026_04_29.toml` exercises all three |

**Test coverage delta:** 71 → 111 tests (40 new tests across 7 new test classes). Full suite green.

**Vertical-slice readiness:** E9 + E10 + E11 are end-to-end ready for doctrine-driven Phase 2 content authoring. Manual play-test verification (PRD §4 acceptance criteria that depend on browser interaction) is NOT covered by pytest — see §11.6.

---

## §8 Cross-references

- **`01_Repeatable_First_Doctrine.md`** — vocabulary inherited (stage, scene, repeatable, cascade).
- **`02_NPC_Stage_Chains.md`** — Frank stage chain that grounds all test scenarios in §4.
- **`03_Engine_Changes_PRD.md`** — baseline (E1–E8). Items shipped in 03 are doctrine-compatible; E9–E11 close the remaining hint-subsystem gap.
- **`04_Scene_Cascade_Pattern.md`** — the cascade pattern that produces the stage transitions E9 detects, E10 surfaces, and E11 displays.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §2.6** — original stage helpers spec; E4 implementation confirmed shipped.

---

## §9 Status legend recap

- ✅ Shipped — code in main, doctrine-compatible
- 🟡 In flight / partial — implementation started
- 🟦 Specified, not started — this PRD
- ⏸ Deferred — rationale included in §5

**Updated 2026-04-30:** E9, E10, E11 all moved 🟦 → ✅. See §7 ledger and §11 implementation notes.

---

## §10 What this doc is not

It is not a redesign spec. (Those are 01, 02, 04, plus deferred 05/06/07.)
It is not a rewrite of 03. (E1–E8 stay valid; this doc adds E9–E11.)
It was not the implementation when authored on 2026-04-29. §11 documents what shipped on 2026-04-30.
It is not the journal display spec. (That's `07_Journal_Display_Spec.md`, deferred.)

It is the engine work the Phase 2 doctrine demands beyond what was already shipped in 03. Three items, ~12–17 engineering hours, no new primitives, no breaking changes. When E9, E10, E11 landed on 2026-04-30 (see §11), the engine became end-to-end ready for the doctrine-driven Phase 2 rewrite.

---

## §11 As built — implementation notes (2026-04-30)

This section documents what was actually shipped, the deviations from the original §1 prescriptive text, and where to find the code. The §1 text is preserved as the historical contract — read this section for current truth.

### §11.1 Commit list

Six commits on `main` (oldest → newest):

| Commit | Subject |
|---|---|
| `5bb3470` | Engine PRD 03 (E1–E8) + Long Summer features (F1–F4) + tests — prerequisite baseline |
| `906869b` | `arc_stages` schema: per-NPC stage display registry (E9/E10/E11 foundation) |
| `6bd7d63` | E11: `stage_label` sidebar item — render "<NPC>: <stage>" from `arc_stages` |
| `520815b` | E9: stage-flag stalled-progress detection |
| `efbca85` | E10: stage-gated hints + per-NPC template consumer |
| `da918c1` | Phase 2 didactic fixture + smoke test (E9/E10/E11 end-to-end) |

The 2026-04-29 working tree carried ~2000 lines of uncommitted E1–E8 + F1–F4 implementation that needed committing as a prerequisite — `5bb3470`. Without that baseline, E9–E11 patches would have mixed into the same diff and lost bisectability.

### §11.2 Foundation: `[[npcs]].arc_stages` schema

The PRD §5 explicitly deferred the `[[npcs]].arc_stages` schema, recommending a runtime regex fallback (`^[a-z_]+_stage$` + integer-value check). During planning we undeferred it because:

- The regex fallback would catch any flag named `*_stage` (e.g. `life_stage`, `pregnancy_stage`) and pollute stalled-detection.
- A single explicit registry serves all three items: E9 (stalled-detection scope), E10 (hint stage_gate validation), E11 (sidebar display labels).
- The schema cost is small — one new field on `TemplateNPC`, one validator, one registry emission.

**Schema** (`apps/projects/services/template_import.py`):
```python
@dataclass
class TemplateNPC:
    # ...
    arc_stages: List[str] = field(default_factory=list)
```

**TOML authoring:**
```toml
[[npcs]]
id = "npc_frank"
arc_stages = ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"]
```

**Validation:**
- All entries strings; non-list raises `TypeError`.
- Length ≥ 1 if present (empty = no stage chain).
- **`<slug>_stage` MUST NOT appear in `player.trait_decay`** when arc_stages is declared. Decay bypasses `applyAndNotifyTrait`, which is where E9 hooks the advancement log — this collision would silently break stalled-detection.

**Runtime emission** at `v1.py:2031` area (alongside `setup.stage_helpers`):
```javascript
setup.npc_arc_stages = {"npc_frank": ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"], ...};
```

Slug-keyed. Trait name is derived as `slug + "_stage"` everywhere — never stored.

**Help-data hook**: not needed — the runtime registry is read via `setup.npc_arc_stages` directly, not via `_helpData.npcs[uuid]`.

### §11.3 E9 — Stage-flag stalled-progress detection (commit `520815b`)

**Schema additions** to `TemplateStoryHints`:
- `stuck_threshold_days: int = 7` — N-day window for stalled detection.
- `stage_stall_message: str = ""` — author-customized stall hint text. Empty falls back to the generic line.

The PRD's open-question §1 left `stage_stall_message` as a future enhancement; we shipped it because a bare `is_stuck` augmentation would emit the generic "explore more" hint without per-game color, and the cost was ~30 minutes.

**Critical PRD correction:** PRD's proposed code shows the advancement-log hook inside `applyFlagEffect` (the boolean flag handler). That's wrong — stage values are integer player traits, not booleans. The engine's flag system is boolean-only. Stage values move via `setup.applyAndNotifyTrait("player", null, "<slug>_stage", "set", N)`.

**Hook location:** `v1.py:applyAndNotifyTrait` (around line 4015 post-edit). The function already exposes `oldVal`, `newVal`, `delta` in scope. The hook is one if-block that fires when:
- `targetType === 'player'` AND
- `delta > 0` (positive advancement only — `set` writes that decrease don't count) AND
- `trait` matches `^([a-z_]+)_stage$` AND
- the captured slug is in `setup.npc_arc_stages`

On match, stamps `$game_state.stage_advancement_log[slug] = current_day`.

**`$game_state` init** at `v1.py:5288` — `"stage_advancement_log": {}` added alongside `random_cooldowns`. Lazy-init defensive (`sv.game_state.stage_advancement_log = sv.game_state.stage_advancement_log || {}`) at every read site — handles in-flight saves.

**Stall computation** in `detectStoryPosition` after the existing `is_stuck` calc (`v1.py:4266` area). The block:
- Skips entirely when `setup.npc_arc_stages` is empty (existing TOMLs without stage chains see identical behavior).
- Iterates the registry; if any non-hidden NPC has advanced within the threshold, `stalled = false`.
- ORs into `is_stuck` while preserving the not-complete clause from the original calc. Edge case: `totalNodes === 0` (test fixtures, prologue-only games) treats any stall as honest.

**Hidden NPCs** (`hidden_from_ui = true`) are excluded from stall computation — their advancement isn't visible to the player anyway.

**Hint emission** in `generateNarrativeHint`. New top branch (above the existing `incompleteGroup` check) fires `hint_type = "stage_stall"` with the custom message or generic fallback. The existing gate at `v1.py:4419` was extended so stage-stall fires hints even when the player still has available canvases.

**Tests:** 3 schema + 6 integration. See `StageStallSchemaTests` and `StageStallIntegrationTests` in `apps/projects/tests.py`.

### §11.4 E10 — Stage-gated hint pool + template consumer (commit `efbca85`)

**Schema additions** to `TemplateHintCondition` (flat fields per PRD recommendation, not nested `stage_gate` sub-object):
- `stage_npc: Optional[str] = None`
- `stage_op: Optional[str] = None` — `eq` | `gte` | `lte`
- `stage_value: Optional[int] = None`

Plus on `TemplateHintTemplate`:
- `npc_id: Optional[str] = None` — routing field. Defaults to `stage_npc` from the condition when not explicitly set.

**Validation** (in `validate()`):
- Tri-required: all three of `stage_npc`/`stage_op`/`stage_value` must be set together (partial triple → error).
- `stage_op` ∈ `{eq, gte, lte}`.
- `stage_npc` must reference an NPC that has `arc_stages` declared (catches the typo case + the no-stage-chain case with distinct error messages).
- `0 ≤ stage_value < len(arc_stages)`.
- `npc_id` (when set explicitly) must exist in the roster.

**Critical scope expansion not in original PRD:** `TemplateHintTemplate` was **dead schema at runtime** — parsed and JSON-emitted but never iterated by the runtime JS. The PRD's `~6–8h` estimate assumed a consumer existed. We had to build it. Final effort: ~8h, near the upper end of the original window after picking up the `setup.checkSingleCondition` reuse below.

**Normalization at template_import time** — new helper `_serialize_hint_template(t)` in `template_import.py`. Converts the new and legacy condition fields into a normalized `condition_items` list reusable by `setup.checkSingleCondition` (the existing condition evaluator at `v1.py:4636`):
- Stage-gate triple → `{type: "trait", subject: "player", trait_key: "<slug>_stage", operator: <op>, value: <int>}`
- `missing_flag` → `{type: "flag", subject: "player", flag_key: "<flag>", operator: "is_false"}`
- `missing_trait` and `gap_gte` preserved in the legacy `condition` shape but NOT normalized — these are PRD 03 legacy with no author-spec'd subject; disambiguating them is follow-up work. Authors targeting E10 use stage_gate or `missing_flag` for predicate logic.

**Reuse decision (key efficiency win):** the original PRD spec proposed a new `stageGateMatches` helper. Plan agent recommended reusing the existing `setup.checkSingleCondition` instead, by normalizing at template_import time. This drops the runtime JS changes from "new evaluator + dispatcher" to "iterate templates + call existing evaluator." Cleanest reuse path in the codebase.

**Runtime — two new functions** in `v1.py`:
- `setup.npcSlugForId(npcId)` — UUID → slug inverse of `npc_slug_map`. Returns null for the player pseudo-id and stale UUIDs.
- `setup.getStageHintForNPC(npcSlug)` — walks `arc.hints.templates`, picks the first template whose `npc_id` matches AND whose `condition_items` all pass `setup.checkSingleCondition`. Returns `{text, npc_id}` or null.

**Wired into:**
- `getNextActivity(npcId)` — early-return at the top with `{isStageHint: true, stageHint: {...}}` shape. Stage hints win priority over the canvas-graph walk (per doctrine — flag movement IS the story).
- `getSidebarHint()` — extracts `stageHint.text` first.
- `QuestsPage` — new `<<elseif _next.isStageHint>>` render branch in BOTH the player section and the NPC loop. Two render branches total — verified by test count assertion.

**Routing ergonomics:** when authors set `stage_npc` on the condition but omit `npc_id` on the template, `npc_id` defaults to `stage_npc`. Eliminates the common-case duplication.

**Tests:** 8 schema + 6 integration. See `StageGatedHintSchemaTests` and `StageGatedHintIntegrationTests`.

### §11.5 E11 — `stage_label` sidebar item (commit `6bd7d63`)

**Deviation from PRD letter:** PRD §1 E11 recommended extending `trait_words` with `source = "stage"`. We shipped a NEW sidebar item type `stage_label` instead.

Rationale: the `trait_words` validator already requires non-empty `bands` with min/max OR flag-driven matching. Special-casing it for `source = "stage"` would proliferate validator branches. Distinct authoring vocabulary keeps both surfaces simple. (Plan agent recommendation, user-approved.)

**Schema** validator extension in `template_import.py:1697` area, sibling `elif itype == "stage_label":` branch:
- Required: `npc_id` (slug, must reference an NPC with `arc_stages` declared)
- Optional: `prefix` (string; defaults to NPC name at render time)

**Runtime** at `v1.py:10625` area. New `<<elseif _item.type is "stage_label">>` branch in the sidebarItems widget:
- Reads `$player.core_traits[<slug>_stage]` as the integer stage value.
- Looks up the label via `setup.npc_arc_stages[slug][stage]`.
- Out-of-range clamp: `Math.max(0, Math.min(value, stages.length - 1))` → highest defined label.
- Undefined trait → just the prefix with no colon (no broken markup).
- Empty `arc_stages` AND no prefix → renders nothing.

**TOML authoring:**
```toml
[[sidebar_items]]
type    = "stage_label"
npc_id  = "npc_frank"
prefix  = "Frank"        # optional; defaults to NPC name
```

**Tests:** 6 schema + 2 integration. See `StageLabelSidebarSchemaTests` and `StageLabelSidebarIntegrationTests`.

### §11.6 What's NOT verified — manual play-test required

The pytest suite (111 tests, all green) verifies the **code is emitted correctly** — it greps the generated twee for the right substrings, JSON shapes, render branches, etc. It does NOT execute the JavaScript at runtime. Several PRD §4 acceptance criteria depend on browser interaction:

- **E9 #6**: "frank_stage = 0, day 8, no stage advance since day 0 → stalled hint fires. Day 4 → no stalled hint." — Behavioral runtime check.
- **E10 #2/#3/#5**: "When frank_stage advances to N, Stage-N hint takes over and Stage-(N-1) hint stops." — Runtime rotation behavior.
- **E11 #2/#3/#4/#5/#6**: Sidebar rendering, layout regression, dev-console fallback. — All visual.

**Manual test fixture** at `apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml`. Two dev buttons advance Frank stages 0→1→2 to drive the rotation. Bottom-of-file checklist matches PRD §4.

**Build command:**
```
python manage.py package_from_toml \
  --file apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml \
  --owner-id <uuid> --output /tmp/phase2_demo
```

Open the resulting `index.html` in a browser. Sidebar should show "Frank: Suspicious" at start; clicking the kitchen dev button should flip it to "Frank: Warm" and rotate the QuestsPage hint from Stage-0 to Stage-1.

### §11.7 Resolved open questions

The PRD §1 listed three open questions; here's how they resolved.

| PRD open question | Resolution |
|---|---|
| E9: regex fallback vs explicit registry for `<npc>_stage` flags? | Built explicit `[[npcs]].arc_stages` schema (foundation, §11.2). Regex approach abandoned. |
| E10: flat `stage_npc/stage_op/stage_value` vs nested `stage_gate = {...}` sub-object? | Flat fields, per PRD recommendation. Matches existing `missing_*`/`gap_*` flat-field convention. |
| E11: extend `trait_words` with `source = "stage"` vs new `stage_display` type? | Shipped as new `stage_label` type — opposite of PRD recommendation. Rationale in §11.5. |

### §11.8 Test coverage delta

Before E9/E10/E11: 71 tests. After: 111 tests (+40 across 7 new test classes):

| Test class | Schema | Integration |
|---|---|---|
| `ArcStagesSchemaTests` / `ArcStagesIntegrationTests` | 6 | 2 |
| `StageLabelSidebarSchemaTests` / `StageLabelSidebarIntegrationTests` | 6 | 2 |
| `StageStallSchemaTests` / `StageStallIntegrationTests` | 3 | 6 |
| `StageGatedHintSchemaTests` / `StageGatedHintIntegrationTests` | 8 | 6 |
| `Phase2IntegrationSmokeTest` | — | 1 |

Run via:
```
source venv/bin/activate && DJANGO_SETTINGS_MODULE=config.settings.testing \
  python -m pytest apps/projects/tests.py --override-ini="testpaths=apps/projects"
```

### §11.9 Where the code lives

For future readers tracing E9/E10/E11 behavior:

| Surface | File:area |
|---|---|
| Schema dataclasses | `apps/projects/services/template_import.py` — `TemplateNPC.arc_stages`, `TemplateHintCondition.stage_npc/stage_op/stage_value`, `TemplateHintTemplate.npc_id`, `TemplateStoryHints.stuck_threshold_days/stage_stall_message` |
| Validation | `apps/projects/services/template_import.py:validate()` — arc_stages block (~1718), `stage_label` sidebar block (~1797), E10 stage_gate block (after E4 stage_helpers validation) |
| Normalization | `apps/projects/services/template_import.py:_serialize_hint_template()` — converts stage_gate triple into reusable trait condition |
| Runtime registry emission | `apps/game_generation/twee_comprehensive/generators/v1.py:2035` area — `setup.npc_arc_stages = {...}` |
| E9 advancement-log hook | `v1.py:applyAndNotifyTrait` (post-edit ~line 4015) |
| E9 stall computation | `v1.py:detectStoryPosition` (after the existing is_stuck calc) |
| E9 stall hint emission | `v1.py:generateNarrativeHint` — top branch fires before fallthroughs |
| E10 template consumer | `v1.py:setup.getStageHintForNPC` + `setup.npcSlugForId` (above `getNextActivity`) |
| E10 routing into `getNextActivity` | Top of `getNextActivity(npcId)` — early-return with isStageHint shape |
| E10 QuestsPage render | `v1.py:QuestsPage` — `<<elseif _next.isStageHint>>` in player section + NPC loop |
| E10 sidebar wiring | `v1.py:getSidebarHint` — extracts stageHint.text first |
| E11 sidebar render | `v1.py` sidebarItems widget — `<<elseif _item.type is "stage_label">>` branch |
| `$game_state` init for E9 | `v1.py:5288` area — `"stage_advancement_log": {}` |
| Test fixture | `apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml` |
| Tests | `apps/projects/tests.py` (post-baseline) — see §11.8 |

Line numbers drift with edits; use `grep` against the function/identifier name, not the literal line cite.
