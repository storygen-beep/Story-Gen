# 08 — Engine PRD: Phase 2 Doctrine Additions

> **Created 2026-04-29.**
> Sibling addendum to `03_Engine_Changes_PRD.md`. Does not supersede it.
> Scope: the engine work the Phase 2 doctrine (`01_Repeatable_First_Doctrine.md`) demands beyond what 03 already covers.
> Three items: E9, E10, E11. Phase-2-doctrine items only — nice-to-haves and deferrals are explicitly listed in §9.

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
| E9 | Stage-flag stalled-progress detection | P1 | Medium — interacts with existing `is_stuck` flow; mitigation is OR logic, not replacement | ~80–120 lines, 4–6h | 🟦 specified |
| E10 | Stage-gated hint pool + per-NPC stage routing | P1 | Medium — schema + validator + runtime selector. Backwards-compatible | ~100–150 lines, 6–8h | 🟦 specified |
| E11 | NPC stage display in sidebar | P2 | Low — cosmetic + small validator extension | ~40–60 lines, 2–3h | 🟦 specified |

**Total effort estimate: ~12–17 hours of engineering work.** Three small, independent items shippable in any order.

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

**As of 2026-04-29:**

| Item | Status | Owner | Target |
|---|---|---|---|
| E9 | 🟦 Specified, not started | TBD | Phase 2 vertical-slice prerequisite |
| E10 | 🟦 Specified, not started | TBD | Phase 2 vertical-slice prerequisite |
| E11 | 🟦 Specified, not started | TBD | Phase 2 polish (post-vertical-slice acceptable) |

E9 and E10 should land before the vertical slice is authored, because the slice's stage-chain content can't be playtested without stage-aware hints. E11 can ship later — the slice plays correctly without it; players just don't see the named stage in the sidebar until E11 is in.

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

E9, E10, E11 all sit at 🟦 as of 2026-04-29.

---

## §10 What this doc is not

It is not a redesign spec. (Those are 01, 02, 04, plus deferred 05/06/07.)
It is not a rewrite of 03. (E1–E8 stay valid; this doc adds E9–E11.)
It is not the implementation. (The work is specified; engineering execution is a separate task.)
It is not the journal display spec. (That's `07_Journal_Display_Spec.md`, deferred.)

It is the engine work the Phase 2 doctrine demands beyond what was already shipped in 03. Three items, ~12–17 engineering hours, no new primitives, no breaking changes. When E9, E10, E11 land, the engine is end-to-end ready for the doctrine-driven Phase 2 rewrite.
