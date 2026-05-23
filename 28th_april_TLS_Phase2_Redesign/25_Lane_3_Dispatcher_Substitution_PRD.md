# 25 — Lane 3 Dispatcher Substitution — Engine PRD

> **Status:** PRD — design-locked, implementation deferred.
> **Authored:** 2026-05-11.
> **Source:** Extends doc 24 §7-§9 (RTS Three Lanes for Repeatable NPC Content + TLS Engine Fitness + Lane 3 Design). Doc 24 stays canonical for design rationale; this doc is the executable spec.
> **Predecessor PRDs:** Engine PRDs 03, 08, 12, 14 (all archived 2026-05-05). Naming + structure conventions inherited; freshly framed for the Lane 3 substitution mechanism.

---

## §1 Problem statement

Lane 3 is RTS's largest bucket for repeatable NPC content (7 of Brother's 15 surfaces — 47%). It's the mechanism that produces the "the NPC just wandered in while you were doing X" texture: player picks a non-NPC menu activity (Shower, Study, Wash Dishes), a transient dispatcher passage rolls dice, and on hit substitutes a multi-beat NPC narrative scene in place of the activity's normal content. The player picked the activity; they didn't pick the encounter.

Doc 24 §6 verified TLS already supports Lane 1 (NPC portrait + exit_block 'choices' menus) and Lane 2 (`trigger_mode = "random"` location-entry encounters — Frank Lane 2 doctrine alignment shipped 2026-05-11). Lane 3 is the remaining engine gap.

**This PRD specifies the engine extension that closes that gap.** The mechanism is design-locked per doc 24 §7 (Option A: substitutions config delegating to `isCanvasValid`). What follows is the execution-grade spec: schema fields, runtime helper, emission injection, selector tweaks, acceptance criteria, test plan.

**One-line statement of what this PRD enables:** authors can declare "when player clicks this menu activity, with X% chance and Y conditions, substitute scene Z instead of rendering normal content" — and the engine fires that substitution before any visible content renders, exactly mirroring RTS's dispatcher passage primitive.

---

## §2 Goals + non-goals

### IN SCOPE

- New `TemplateTrigger` fields: `substitutions` (list of substitution rules) + `substitution_only` (boolean exclusion flag for selectors)
- Schema parser + cross-canvas validator + serializer pass-through (`apps/projects/services/template_import.py`)
- Runtime helper `setup.checkAndSubstituteCanvas` + supporting `setup.canvasSubstitutions` helper data + `setup.getCanvasById` lookup if not already present (`apps/game_generation/twee_comprehensive/generators/v1.py`)
- Emission injection at canvas passage body top for canvases with non-empty `substitutions`
- Selector tweaks: `renderNpcPortraits`, `renderSoloActivities`, defensively `selectAutoFireCanvasForLocation` skip canvases with `substitution_only = true`
- Test coverage per §9

### OUT OF SCOPE

- **Authoring** Lane 3 substitutions for Frank/Ryan/Jake/Diana/etc. (separate work; uses this PRD's mechanism once shipped)
- UI surfacing of Lane 3 in Quests/Walkthrough panels (discoverability work per doc 24 §5; tracked separately)
- Tuning the existing TLS Lane 2 per-location 3-visit cooldown (doc 24 §8.1 — separate decision)
- Cross-NPC RTS click-tests (Dad/Marcus/Edward) for further verification of the doctrine
- Engine perf optimization (substitution check is O(rules-per-canvas), not a concern at expected scale of 0-3 rules per canvas)
- Multi-substitution-per-target ("if both Frank and Dad could substitute here at the same time, both roll independently") — first-match policy is sufficient; multi-roll is YAGNI

---

## §3 Functional spec — player POV (verbatim contract)

1. Player clicks a menu activity (e.g., `Cook Breakfast` solo activity at the kitchen, or an NPC portrait routing to a per-NPC canvas)
2. Engine routes to that activity's canvas as normal — passage transition fires
3. **BEFORE rendering the canvas's body**, engine evaluates the canvas's substitution rules in declaration order
4. For each rule: evaluates `isCanvasValid(target_canvas)` → optional extra `conditions` predicate → rolls `Math.random() < chance`
5. **First rule with all gates passing fires `Engine.play(target_canvas.passageName)` and returns immediately** — the parent canvas's body is never rendered
6. If no rule matches (all dice miss, or all conditions fail, or all targets invalid): the parent canvas renders its own body normally
7. The substituted scene (target canvas) plays as its own narrative cascade with its own exit choices — player gets soft-escape via the substituted canvas's own exit blocks
8. On exit, player returns to the location hub (per the substituted canvas's own exit routing)

**Contract guarantee:** the substitution check is invisible to the player. They click the activity, they either get the activity's normal content or they get the substituted scene. There is no "loading" passage, no flicker, no "do you want to substitute?" prompt.

---

## §4 Schema additions — `apps/projects/services/template_import.py`

### §4.1 Dataclass field additions on `TemplateTrigger` (around line 392, after `chance`)

```python
substitutions: List[Dict[str, Any]] = field(default_factory=list)
# Lane 3 doctrine (doc 24 §7). Each rule shape:
#   {
#     "target_canvas_id": str,         # required, must reference an existing canvas
#     "chance": float,                 # required, 0.0–1.0
#     "conditions": Optional[Dict],    # optional, same shape as TemplateTrigger.conditions
#   }
# Engine walks rules at canvas-render entry; first rule with all gates passing
# fires Engine.play(target.passageName) before parent body renders.

substitution_only: bool = False
# When True, this canvas is excluded from renderNpcPortraits +
# renderSoloActivities + selectAutoFireCanvasForLocation. The canvas can ONLY
# be reached as the target of another canvas's substitution rule.
# Used for Frank-substitution-target canvases that should not show as their
# own portrait/button at their location.
```

### §4.2 Parser

Read from raw TOML at the same indentation level as other trigger fields:

```toml
[canvases.trigger]
location          = "loc_kitchen"
trigger_mode      = "manual"
is_repeatable     = true
substitution_only = false
[[canvases.trigger.substitutions]]
target_canvas_id  = "frank_kitchen_morning_substitution"
chance            = 0.33
conditions        = { version = "1.0", items = [...] }
```

Parser walks `trigger.get("substitutions", [])` and validates each entry has `target_canvas_id` (str) + `chance` (float). `conditions` optional; if present, normalize as a `TemplateHintCondition`-shaped dict (re-use the existing condition normalizer).

### §4.3 Validator additions

In `_validate_canvas` or a sibling, after existing trigger validation:

1. **Cross-canvas reference check:** for each rule, `target_canvas_id` must resolve to an existing canvas ID in the project. If not, raise `ValueError(f"Canvas '{canvas.id}' substitution rule references unknown target_canvas_id '{rule['target_canvas_id']}'")`.
2. **Chance bounds:** `chance` must be a float in `[0.0, 1.0]`. Reject otherwise.
3. **Substitution + auto-fire conflict warning:** if `substitution_only = true` AND canvas has `npcId` set, log a warning that the canvas may have been intended to surface as an NPC portrait — but proceed (author may want both behaviors intentionally for special cases).
4. **Substitution + Lane 2 conflict warning:** if both `substitutions` (non-empty) AND `chance` (the trigger-level chance for Lane 2 random firing) are set on the same canvas, warn — the canvas would behave both as a Lane 3 dispatcher AND as a Lane 2 random encounter target. Likely an authoring mistake.
5. **Empty substitutions list:** if `substitutions = []` is explicitly set (vs. omitted), accept silently — same as omitted.

### §4.4 Serializer pass-through

In `_serialize_canvas` (or sibling responsible for emitting canvas trigger to JSON):

```python
"substitutions": [
    {
        "target_canvas_id": rule["target_canvas_id"],
        "chance": float(rule["chance"]),
        "conditions": rule.get("conditions") or None,
    }
    for rule in (canvas.trigger.substitutions or [])
],
"substitutionOnly": bool(canvas.trigger.substitution_only),
```

Note camelCase `substitutionOnly` for the runtime JS (matches existing pattern: `triggerMode`, `isRepeatable`, `npcId`, `maxPerDay`, `hasSchedules`, `scheduleParams`).

---

## §5 Runtime additions — `apps/game_generation/twee_comprehensive/generators/v1.py`

### §5.1 New runtime helper — `setup.checkAndSubstituteCanvas`

Place near `setup.checkRandomEncounters` (around `v1.py:3919`):

```javascript
// Lane 3 dispatcher substitution. Called from the top of a canvas's emitted
// passage body (via the §5.2 injection). Walks the canvas's substitution
// rules, evaluates target validity + optional extra conditions + rolls dice,
// and if all gates pass for any rule, fires Engine.play(target) and returns
// true. If no rule fires, returns false and the parent canvas renders normally.
//
// Doctrine: doc 24 §7 + PRD 25 §3. First-match policy.
setup.checkAndSubstituteCanvas = function(parentCanvasId) {{
    try {{
        var subs = (setup.canvasSubstitutions || {{}})[parentCanvasId] || [];
        if (subs.length === 0) return false;
        for (var i = 0; i < subs.length; i++) {{
            var s = subs[i];
            var target = setup.getCanvasById(s.target_canvas_id);
            if (!target) continue;
            if (!setup.isCanvasValid(target)) continue;
            if (s.conditions && !setup.triggerConditionsSatisfied(s.conditions)) continue;
            if (Math.random() < (s.chance || 0)) {{
                setup.markCanvasTriggered(target.id);
                Engine.play(target.passageName);
                return true;
            }}
        }}
        return false;
    }} catch (e) {{
        return false;  // Fail-open: don't break gameplay if substitution misfires
    }}
}};
```

### §5.2 New runtime helper — `setup.getCanvasById` (if not already present)

Verify whether the engine already has a canvas-id → canvas-data lookup. If not, build one at boot:

```javascript
// Boot-time index: canvas.id -> canvas object. Built once from
// setup.help_data.locationCanvases. O(N) one-time construction; O(1) lookup.
setup._canvasByIdMap = null;
setup.getCanvasById = function(canvasId) {{
    if (!setup._canvasByIdMap) {{
        setup._canvasByIdMap = {{}};
        var lc = (setup.help_data || {{}}).locationCanvases || {{}};
        for (var loc in lc) {{
            var list = lc[loc] || [];
            for (var i = 0; i < list.length; i++) {{
                if (list[i] && list[i].id) {{
                    setup._canvasByIdMap[String(list[i].id)] = list[i];
                }}
            }}
        }}
    }}
    return setup._canvasByIdMap[String(canvasId)] || null;
}};
```

### §5.3 New helper data — `setup.canvasSubstitutions`

Map of canvas-id → array of substitution rules. Built at engine emit time from each canvas's `substitutions` field. Emitted alongside `setup.help_data` in the engine init block.

Python emission (in the engine init block builder, alongside `setup.help_data` emission):

```python
canvas_subs_map = {}
for canvas in self._compute_included_canvases():
    rules = canvas.trigger.substitutions or [] if canvas.trigger else []
    if rules:
        canvas_subs_map[canvas.id] = [
            {
                "target_canvas_id": r["target_canvas_id"],
                "chance": float(r["chance"]),
                "conditions": r.get("conditions") or None,
            }
            for r in rules
        ]

emitted_js += f"setup.canvasSubstitutions = {json.dumps(canvas_subs_map)};\n"
```

### §5.4 Emission injection — `_generate_canvas_node_passages` (`v1.py:10028`)

For each canvas with non-empty `substitutions`, inject at the very top of its emitted passage body (BEFORE any preamble blocks):

```
:: Canvas_<canvas_id>_Node_<node_idx>
<<script>>if (setup.checkAndSubstituteCanvas("<canvas_id>")) return;<</script>>

[normal canvas content...]
```

Canvases with empty `substitutions` get NO injection — zero overhead for the common case.

**Note on canvas ID format:** the embedded canvas ID in the script call must match the runtime's canvas-id format. Per doc 24's verification, runtime stores canvases by UUID under `setup.help_data.locationCanvases`. Confirm whether the emission step has access to the UUID at this point in the build, or whether the slug is the right key. If slug-based emission, `setup.getCanvasById` may need to also accept slug lookups. Decision deferred to implementation — see §11 open question 3.

### §5.5 Selector tweaks

**`renderNpcPortraits`** (`v1.py:3703-3812`): add `if (c.substitutionOnly) continue;` near the existing `triggerMode === "random"` filter (line 3728):

```javascript
if (!c.isRepeatable) continue;
if ((c.triggerMode || "manual") === "random") continue;
if (c.substitutionOnly) continue;  // NEW: PRD 25 §5.5
if (!c.npcId) continue;
```

**`renderSoloActivities`** (`v1.py:3817-3917`): same pattern near line 3833.

**`selectAutoFireCanvasForLocation`** (`v1.py:3236`): defensively add the same filter near line 3244, even though substitution_only canvases will be repeatable so they wouldn't auto-fire anyway. Cost is one line; safety is one line.

---

## §6 Cooldown semantics

Per doc 24 §8 — **decided, do not re-litigate:**

- Substituted canvases inherit Layer 1 (per-canvas) + Layer 2 (per-activity-name) cooldowns automatically via the `setup.markCanvasTriggered(target.id)` call inside `checkAndSubstituteCanvas` (§5.1)
- Layer 3 (per-location 3-visit cooldown set by `checkRandomEncounters` at `v1.py:3979`) is NOT extended to Lane 3 substitutions
- TLS Lane 2 cooldown stays at 3 visits — separate tunable, out of scope here

**Why no Layer 3 for Lane 3:** RTS doesn't have Layer-3-style cooldowns (per source audit doc 21). Layer 3 in TLS exists to throttle "random encounter spam at a single location"; that concern doesn't apply to Lane 3 because each parent activity has its own daily limits via Layer 1 + 2.

---

## §7 Predicate vocabulary

Per doc 24 §9 — **decided, do not re-litigate:**

- No new predicate types needed
- `isCanvasValid(target)` (`v1.py:3406`) evaluates the target canvas's own `location` + `schedules` + `npc` + `conditions`, which collectively gate "is the NPC at the right place at the right time with the right state"
- Optional `conditions` on the substitution rule itself uses the existing predicate vocabulary: `flag`, `trait`, `modifier`, `days_since_flag`, `clothing_slot`, `clothing_item`, `pass`, `item`, `stage` (catalog at `v1.py:2684-2952`)

The Lane 3 design works **because** the target canvas's own trigger gates inherently express "is this scene currently appropriate to fire here." Authors don't have to redeclare those gates on the substitution rule — they just point at the target.

---

## §8 Acceptance criteria

The PRD is delivered when:

1. ✅ Author can write `[[canvases.trigger.substitutions]]` blocks in TOML and the build accepts them
2. ✅ Build emits the `<<script>>if (setup.checkAndSubstituteCanvas("<id>")) return;<</script>>` injection at the top of canvases that have substitutions; **no overhead** on canvases without
3. ✅ At runtime: clicking a parent canvas with a substitution rule triggers the dice roll
4. ✅ When dice + isCanvasValid(target) + optional conditions all pass: target canvas plays in place of parent (verified via passage-name observation)
5. ✅ When dice fails or any gate fails: parent canvas renders normally (verified via passage-name observation)
6. ✅ Substituted canvas's own cooldowns (canvas-level + activity-level) properly increment via markCanvasTriggered (verified via `trigger_history` inspection)
7. ✅ Canvases with `substitution_only = true` are excluded from NPC portrait grid + solo activity button list
8. ✅ Validator rejects substitution rules with missing/invalid `target_canvas_id`, out-of-range `chance`
9. ✅ Validator warns on conflicting setups (substitution_only + npcId, or trigger-level chance + substitutions on same canvas)
10. ✅ Sample author test passes: write one Frank substitution on `activity_help_with_chores` (or similar parent) pointing to a `frank_chore_substitution` canvas; build cleanly; verify in browser that 1 in N kitchen-chores plays the substitution

---

## §9 Test plan

### §9.1 Schema tests (`apps/projects/tests.py`)

- **`SubstitutionsRoundTripTests`**:
  - `test_substitution_round_trips` — parse + serialize a canvas with substitutions, verify field preservation (target_canvas_id, chance, conditions)
  - `test_substitution_default_empty` — canvas without substitutions field gets `[]` default
  - `test_substitution_only_default_false` — flag defaults to false when absent
- **`SubstitutionsValidatorTests`**:
  - `test_validator_rejects_missing_target_canvas_id` — raises ValueError
  - `test_validator_rejects_invalid_chance_value` — out of [0, 1] range
  - `test_validator_rejects_unknown_target_canvas_id` — references nonexistent canvas
  - `test_validator_warns_on_substitution_only_with_npcid` — warning logged, no error
  - `test_validator_warns_on_substitutions_plus_trigger_chance` — same

### §9.2 Engine emission tests

- `test_substitution_check_emitted_in_html` — find the `<<script>>if (setup.checkAndSubstituteCanvas("<id>")) return;<</script>>` at top of canvas passage body for canvases with substitutions
- `test_substitution_check_NOT_emitted_for_empty_substitutions` — no injection for canvases without
- `test_canvasSubstitutions_map_populated` — `setup.canvasSubstitutions` JSON object includes all canvases with substitutions, keyed by canvas ID
- `test_renderNpcPortraits_skips_substitution_only` — generated `renderNpcPortraits` source includes the `if (c.substitutionOnly) continue;` filter
- `test_renderSoloActivities_skips_substitution_only` — same

### §9.3 Runtime behavior tests (browser-driven via twine-game-explorer or jsdom)

- `test_substitution_fires_on_chance_hit` — mock Math.random to return 0.0 (always hit), navigate to parent canvas, verify Engine.play landed on target's passage
- `test_substitution_skipped_on_chance_miss` — mock Math.random to return 0.99 (always miss), navigate to parent, verify parent's passage rendered
- `test_substitution_skipped_on_invalid_target` — set state so target canvas's isCanvasValid fails, verify parent renders
- `test_substitution_skipped_on_failed_extra_conditions` — set state so optional conditions fail, verify parent renders
- `test_markCanvasTriggered_increments_target_history` — after substitution fires, verify `State.variables.game_state.trigger_history[target_id]` updated
- `test_substitution_only_canvas_excluded_from_portraits` — verify a substitution_only canvas at a location does not appear in the portrait grid even when conditions met

### §9.4 Sample integration test

- Author one `frank_chore_substitution` canvas in the test slice TOML, attach a substitution rule on `activity_help_with_chores`, build, navigate to kitchen, click "Help with chores" 30 times with reset cooldowns + mocked dice, count substitution fires vs. parent renders, verify ratio matches declared chance

---

## §10 Out of scope (explicit)

- Authoring Lane 3 substitutions for Frank/Ryan/Jake/Diana/etc. (separate authoring pass, after this PRD ships)
- UI surfacing of Lane 3 in Quests/Walkthrough panels (per doc 24 §5 — discoverability is its own design problem)
- Tuning the existing TLS Lane 2 per-location 3-visit cooldown (one-line change at `v1.py:3979`, separate decision)
- Cross-NPC RTS click-tests (Dad/Marcus/Edward) for further verification of the doctrine
- Engine perf optimization
- Multi-substitution-per-target multi-roll behavior

---

## §11 Open questions

These need to be resolved during implementation, not before:

1. **Does `setup.getCanvasById` already exist?** If yes, reuse it. If no, build the boot-time map per §5.2. Greppable check during implementation.

2. **Should `substitution_only` be excluded from `selectAutoFireCanvasForLocation`?** Defensively yes, per §5.5. Cost is one line. The auto-fire selector targets one-shot story canvases (`isRepeatable = false`); substitution targets will typically be repeatable so they wouldn't auto-fire anyway, but the filter is cheap insurance.

3. **Canvas ID format in the emitted script — slug or runtime UUID?** Doc 24 §6 verified runtime stores canvases under UUIDs in `setup.help_data.locationCanvases`. The emission in §5.4 uses `<canvas_id>` — confirm at implementation time whether this is the slug (author-facing) or the UUID (runtime-facing). Likely UUID; if slug, `setup.getCanvasById` needs to map both.

4. **Pruning — does `_compute_included_canvases` need to walk substitution rules?** A canvas marked `substitution_only = true` that's only referenced by another canvas's substitution rule may be pruned by the existing canvas-inclusion logic (which likely keys on "is this canvas reachable from a location/exit"). The build needs to walk substitution rules as a reachability source, otherwise substitution targets get silently dropped from the build. Verify in implementation.

5. **Substitution chains?** If canvas A substitutes to canvas B, and canvas B itself has a substitution rule pointing to canvas C, the engine will recursively check B's substitutions on render → may chain to C. Is this desired? Probably yes (it's an emergent property, not explicit), but worth flagging. No infinite-loop risk because each canvas only substitutes if `Math.random() < chance` hits AND target's isCanvasValid passes — eventually a chain terminates.

---

## §12 Cross-references

**Predecessor docs:**
- Doc 24 §7 (Lane 3 design rationale)
- Doc 24 §8 (cooldown decision)
- Doc 24 §9 (predicate vocabulary check)
- Doc 24 §11 (estimated work breakdown)
- Doc 21 (RTS Brother mechanism audit — source-extracted)
- Doc 22 (RTS cross-NPC mechanism comparison)

**Source artifacts:**
- `game_explorations/rts-arc-trace/synthesis_repeatable_narrative_auto_2026-05-10.md` (live-play evidence — Lane 3 verified first-try)
- `game_explorations/tls-frank-lane2-verify/` (Frank Lane 2 doctrine alignment verification, 2026-05-11)

**Memory:**
- `~/.claude/.../memory/rts_lane3_dispatcher_pattern.md`
- `~/.claude/.../memory/rts_three_lanes_lane3_design.md`

**Engine code touched (file:line — for implementation reference):**
- `apps/projects/services/template_import.py:382` (TemplateTrigger schema — §4.1)
- `apps/game_generation/twee_comprehensive/generators/v1.py:3236` (selectAutoFireCanvasForLocation — §5.5 defensive filter)
- `v1.py:3406` (isCanvasValid — reused unchanged)
- `v1.py:3703` (renderNpcPortraits — §5.5)
- `v1.py:3817` (renderSoloActivities — §5.5)
- `v1.py:3919` (checkRandomEncounters — sibling location for new helper §5.1)
- `v1.py:10028` (_generate_canvas_node_passages — §5.4 emission injection)

---

## §13 Estimated work (refined from doc 24 §11)

| Task | Estimate |
|---|---:|
| §4.1-§4.2 Schema field + parser | 30 min |
| §4.3 Validator (cross-canvas reference + bounds + warnings) | 20 min |
| §4.4 Serializer pass-through | 10 min |
| §5.1 Runtime helper `checkAndSubstituteCanvas` | 15 min |
| §5.2 `getCanvasById` lookup helper (if needed) | 10 min |
| §5.3 Helper data emission (`canvasSubstitutions` map) | 15 min |
| §5.4 Emitter injection at canvas passage body top | 30 min |
| §5.5 Selector tweaks (3 selectors) | 15 min |
| Pruning fix in `_compute_included_canvases` if needed (§11 Q4) | 20 min |
| §9.1 Schema tests | 20 min |
| §9.2 Engine emission tests | 20 min |
| §9.3 Runtime tests (browser-driven) | 30 min |
| §9.4 Sample integration test (one Frank substitution) | 30 min |
| Build + grep verification + iteration buffer | 30 min |
| **Total** | **~5 hr** (revised up from doc 24's ~2.5 hr after PRD-level test coverage scoping) |

---

End of PRD.
