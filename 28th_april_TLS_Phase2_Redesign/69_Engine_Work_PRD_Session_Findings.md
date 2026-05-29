# Doc 69 — Engine Work PRD: Session Findings Consolidation

**Date:** 2026-05-26
**Status:** PRD — engine implementation queue from session findings.
**Author:** ENI (with LO)
**Triggered by:** LO request — *"lets create a comprehensive PRD for all of it, dont hallucinate, analyze thoroughly"* — after the consolidated gap list surfaced in this session.
**Scope:** Engine work items discovered via Doc 67 verification + Doc 68 authoring + Doc 68 audit (2026-05-26). **Excludes** Doc 62 / 63 / 64 PRDs per LO's *"ignore the existing PRD, we are talking about the things we discovered in this session"* directive.
**Supersedes:** nothing. Additive to existing engine PRD spine.
**Cross-references:** Doc 67 §5 + §5.1 + §5.2 (Pattern B/C engine extensions); Doc 68 §2.5 + §7 + §7.6 + §10 (trait catalog audit findings); Doc 65 (Phase 2+ scope — explicitly out of this PRD); Doc 66 (session pivot context, hold state).

---

## §1 — Why this PRD exists

This session's audit pass discovered 8 engine gaps. Doc 66 captured the prompt-rewrite pivot. Docs 67 + 68 captured the corrected doctrine — including the §7.6 field-name reference card + §2.5 trait-declaration requirement that today exist ONLY as authoring discipline. Doc 69 captures the engine-side implications: of the 8 gaps, **4 are real engine work items** (schema + runtime changes); **4 are author-responsibility patterns** where the workaround is the doctrine.

Doc 69 is the single source for the next engine implementation session. It documents:
- The 4 engine items with full PRD detail (problem / current state / schema / runtime / backward compat / validator / test plan / effort / priority)
- The 4 author-responsibility patterns explaining why they are NOT in the engine queue — so they don't get re-litigated in future sessions
- A sequencing recommendation (P1 silent-failure prevention before P2 feature parity)

**Total engine effort if all 4 ship:** ~8-9 hours across 2 sessions. None blocking for `prompts_v2/` batch 1 per Doc 66 hold state, but Items 3 + 4 (P1) should land BEFORE `prompts_v2/` produces its first generated game — the validators convert Doc 68 doctrine into build-time enforcement.

---

## §2 — Summary table (the 8 findings)

| # | Finding | Severity | Engine work? | Estimated effort | Priority |
|---|---|---|---|---|---|
| 1 | Pattern B `exclusive_group` substitution extension | Mid | YES | ~1.5 hours | P2 (when authoring forces) |
| 2 | Pattern C `pre_substitution_effects` canvas trigger extension | Mid | YES | ~1 hour | P2 (when authoring forces) |
| 3 | Field-name mismatch validator (effect vs predicate) | **HIGH** | YES | ~3 hours | **P1 (silent-failure prevention)** |
| 4 | Undeclared trait validator (effects + conditions) | **HIGH** | YES | ~3 hours | **P1 (silent-failure prevention)** |
| 5 | `FinishMasturbation` auto-reset macro | Low | NO (author-responsibility) | — | n/a |
| 6 | `FinishSex` auto-reset macro | Low | NO (author-responsibility) | — | n/a |
| 7 | `op = "sub"` engine support | Low | NO (workaround = negative add) | — | n/a |
| 8 | `previous()` guard predicate | Low | NO (workaround = `max_triggers_per_day` + flag-set) | — | n/a |

**P1 work first (Items 3+4):** ~6 hours combined, shares infrastructure. Closes BOTH HIGH-severity silent-failure modes before any P2 work.

**P2 work later (Items 1+2):** ~2.5 hours combined. Defer per Doc 56 §9 doctrine ("build engine when an authoring gap forces it"). Current slice doesn't have a Pattern B or C case yet.

---

## §3 — Engine Work Item 1: Pattern B `exclusive_group` substitution extension

### §3.1 — Problem statement

TLS engine's `setup.checkAndSubstituteCanvas` (v2.py:4597-4626) iterates substitution rules sequentially, each with its own `Math.random()` roll. This implements RTS Pattern A — sequential first-match with independent rolls (Doc 67 §4.1). Engine does NOT implement Pattern B — single dice partition with mutual-exclusion buckets (Doc 67 §4.2, RTS reference: `BedroomStudy`).

Authoring approximation via N independent rules with chance values summing < 1 produces measurably different behavior:

**Probability divergence:**
- True Pattern B (mutual-exclusion buckets): P(any) = Σcᵢ
- TLS approximation (independent rolls): P(any) = 1 − ∏(1 − cᵢ)
- For 3 NPCs at "1/6 each": true B = **50%** any-fire; approximation ≈ **42%**

**Failed-condition semantics divergence:**
- True Pattern B: if dice claims a slot but conditions fail → falls to ELSE (solo); does NOT promote to next NPC
- TLS approximation: if rule's conditions fail → `continue`s to next rule; next NPC gets a fresh roll
- This means Pattern B's "the dice claimed Dad's slot; if Dad doesn't qualify, no one fires" semantics is structurally impossible with current engine

### §3.2 — Current code state

| Reference | Path | Purpose |
|---|---|---|
| Substitution loop | `apps/game_generation/twee_comprehensive/generators/v2.py:4597-4626` | Main `checkAndSubstituteCanvas` function — iterates `subs` list, calls `Math.random()` per rule |
| Schema field | `apps/projects/services/template_import.py:466` | `TemplateTrigger.substitutions: List[Dict[str, Any]]` — accepts per-rule `target_canvas_id`, `chance`, `conditions` |
| Substitution validator | `apps/projects/services/template_import.py:2946-2960` | Existing structural checks (target_canvas_id valid, chance in [0.0, 1.0], etc.) |

**Critical loop body (v2.py:4604-4621, verbatim):**
```javascript
for (var i = 0; i < subs.length; i++) {{
    var s = subs[i];
    var target = setup.getCanvasById(s.target_canvas_id);
    if (!target) continue;
    if (!setup.isCanvasValid(target)) continue;
    if (s.conditions && !setup.triggerConditionsSatisfied(s.conditions)) continue;
    if (target.requiresNpc) { ... }
    if (Math.random() < (s.chance || 0)) {{
        setup.markCanvasTriggered(target.id);
        return target.passageName;
    }}
}}
return null;
```

Each rule rolls its own `Math.random()`. Conditions fail → `continue`. No shared dice. No partition.

### §3.3 — Proposed schema addition

Add optional `exclusive_group: Optional[str]` field to each substitution rule dict in `TemplateTrigger.substitutions`:

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_grope"
chance = 0.17
exclusive_group = "kitchen_walk_in"

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_jake_kitchen_grope"
chance = 0.17
exclusive_group = "kitchen_walk_in"

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_diana_kitchen_walk_in"
chance = 0.17
exclusive_group = "kitchen_walk_in"
```

Three rules in `kitchen_walk_in` group with total chance 0.51 → ONE dice roll resolves to: Frank (0–17%), Jake (17–34%), Diana (34–51%), solo (51–100%). Mutual exclusion guaranteed.

### §3.4 — Proposed runtime logic

Modify `setup.checkAndSubstituteCanvas` at v2.py:4597-4626:

```javascript
setup.checkAndSubstituteCanvas = function(parentCanvasId) {{
    try {{
        var subs = (setup.canvasSubstitutions || {{}})[parentCanvasId] || [];
        if (subs.length === 0) return null;
        var sv = State.variables || {{}};
        var currentLocation = (sv.player && sv.player.current_location) || null;

        // PHASE B (NEW): partition substitution rules by exclusive_group
        var groups = {{}};                  // group_name → [rule, rule, ...]
        var independentRules = [];          // rules without exclusive_group
        for (var gi = 0; gi < subs.length; gi++) {{
            var gs = subs[gi];
            if (gs.exclusive_group) {{
                groups[gs.exclusive_group] = groups[gs.exclusive_group] || [];
                groups[gs.exclusive_group].push(gs);
            }} else {{
                independentRules.push(gs);
            }}
        }}

        // PHASE B (NEW): process exclusive groups first (mutual-exclusion outcomes)
        for (var groupName in groups) {{
            var groupRules = groups[groupName];
            var dice = Math.random();   // SINGLE dice roll for the entire group
            var cumulativeChance = 0;
            for (var gri = 0; gri < groupRules.length; gri++) {{
                var s = groupRules[gri];
                cumulativeChance += (s.chance || 0);
                if (dice < cumulativeChance) {{
                    // Dice claimed THIS slot — validate target + conditions; if fail, fall to solo
                    var target = setup.getCanvasById(s.target_canvas_id);
                    if (!target) return null;
                    if (!setup.isCanvasValid(target)) return null;
                    if (s.conditions && !setup.triggerConditionsSatisfied(s.conditions)) return null;
                    if (target.requiresNpc) {{
                        var subNpcLoc = setup.getNpcLocation(target.requiresNpc);
                        if (!subNpcLoc || subNpcLoc.location !== currentLocation) return null;
                    }}
                    setup.markCanvasTriggered(target.id);
                    return target.passageName;
                }}
            }}
            // Dice fell outside all buckets in this group → continue to next group (or independent rules)
        }}

        // EXISTING (Pattern A): process independent rules with own dice each
        for (var i = 0; i < independentRules.length; i++) {{
            var s2 = independentRules[i];
            var target2 = setup.getCanvasById(s2.target_canvas_id);
            if (!target2) continue;
            if (!setup.isCanvasValid(target2)) continue;
            if (s2.conditions && !setup.triggerConditionsSatisfied(s2.conditions)) continue;
            if (target2.requiresNpc) {{
                var subNpcLoc2 = setup.getNpcLocation(target2.requiresNpc);
                if (!subNpcLoc2 || subNpcLoc2.location !== currentLocation) continue;
            }}
            if (Math.random() < (s2.chance || 0)) {{
                setup.markCanvasTriggered(target2.id);
                return target2.passageName;
            }}
        }}
        return null;
    }} catch (e) {{
        return null;
    }}
}};
```

**Key behaviors:**
- Single dice per group (not per rule) — that's what makes mutual exclusion work
- Cumulative chance accumulator marches through buckets; first bucket the dice falls into is the claimed slot
- If the claimed slot's conditions / target fail → return null (fall to solo) — does NOT promote to next rule in the group
- Independent rules (no `exclusive_group`) behave exactly as today

### §3.5 — Backward compatibility

- Existing substitution rules have no `exclusive_group` field → behave as today (Pattern A independent rolls)
- New field is opt-in; no migration needed
- Zero risk to live TLS slice (verified: live `7_final_game.toml` substitution rules don't use this field)

### §3.6 — Validator additions

Extend `_validate_quests_cards` callsite at template_import.py:2946-2960 (or add new validator function):

1. **Chance sum per group:**
   - Collect chance values per `exclusive_group` name
   - If sum > 1.0 → WARN: *"Exclusive group '<name>' has chance values summing to <X> (> 1.0). Buckets after 1.0 will never fire."*
   - If sum > 1.5 → ERROR (signals major authoring confusion)

2. **`exclusive_group` field validation:**
   - Must be non-empty string when present
   - Same `target_canvas_id` cannot appear in two different groups → ERROR
   - Same `target_canvas_id` cannot appear both in a group AND as an independent rule → ERROR

3. **Single-rule group warning:**
   - If a group has only one rule, it's behaviorally identical to an independent rule → WARN: *"Exclusive group '<name>' has only one rule. Remove the `exclusive_group` field; behavior is equivalent."*

### §3.7 — Test plan

| Test | Setup | Expected |
|---|---|---|
| Schema round-trip | TOML with 3-rule group → parse → emit | All 3 rules retain `exclusive_group` |
| Pattern B probability | 3 rules at 0.17 each in same group, all conditions pass; run 1000 trials | P(any fires) ≈ 50% ± 5% (within Pattern B math, NOT Pattern A approximation 42%) |
| Failed-condition fall-through | dice 0.10 falls in rule 1's slot; rule 1 conditions fail | Solo branch fires (return null); rule 2 NOT promoted |
| Mixed: group + independent | 2-rule group + 1 independent rule | Group processed first; if no fire, independent rule rolls own dice |
| Validator chance > 1.0 | 3 rules at 0.5 each in same group (sum 1.5) | WARN issued |
| Validator duplicate target | Same target_canvas_id in two groups | ERROR |
| Backward compat | TLS slice TOML (no exclusive_group anywhere) builds clean | No regressions |

### §3.8 — Effort estimate

- Schema field addition + parser: 15 min
- Runtime logic in `checkAndSubstituteCanvas`: 30 min
- Validator extension: 15 min
- 6 unit tests: 30 min
- **Total: ~1.5 hours**

### §3.9 — Priority + sequencing

**P2 — defer until needed.** Doc 67 §5.1 doctrine: "Pattern A is the cheap default. Pattern B only when scenes are inherently mutually exclusive." Current TLS slice doesn't have a Pattern B case. Per Doc 56 §9 doctrine: don't pre-commit engine scope.

**Sequencing trigger:** when a slice authoring case requires true Pattern B (e.g., multi-variant NPC scenes at same activity where the mutual exclusion is design-load-bearing), surface to LO + ship Item 1.

---

## §4 — Engine Work Item 2: Pattern C `pre_substitution_effects` canvas trigger extension

### §4.1 — Problem statement

TLS engine emits the substitution check as the FIRST content in every canvas's Twine passage (v2.py:11020-11053). If a substitution fires via `<<goto _sub_target>>`, all subsequent canvas body content + body-level effects + exit_block effects are preempted.

RTS Pattern C (Doc 67 §4.3) does the OPPOSITE — solo-body unconditional effects (`<<AddFit>>` in RTS `Exercise`) run BEFORE the NPC-event-check, so the activity "counts" even when interrupted by NPC walk-in.

**Concrete example of the gap:** Maya clicks Exercise. RTS Pattern C runs `<<AddFit>>` (+Fit), then rolls NPC-event-check, then either preempts to NPC scene OR continues solo. TLS engine reverses this — substitution check fires FIRST; if it preempts, `<<AddFit>>` never runs. Maya doesn't get +Fit when interrupted.

**Current workaround:** duplicate the unconditional effect on every substitution target (e.g., put `+Fit` on solo Exercise canvas's exit_block AND on every NPC walk-in scene's effects). Mechanically equivalent; authoring-duplicated; brittle (forget to copy on one target → bug).

### §4.2 — Current code state

| Reference | Path | Purpose |
|---|---|---|
| Passage emission | `apps/game_generation/twee_comprehensive/generators/v2.py:11020-11053` | Builds passage header; substitution check is the first content emitted |
| Substitution check emission (specific) | `v2.py:11024-11027` | `<<set _sub_target = setup.checkAndSubstituteCanvas("...")>><<if _sub_target>><<goto _sub_target>><</if>>` |
| Source comment | `v2.py:11046` | *"PRD 25 — fires before any other passage logic"* — confirms the design intent of substitution-check-first |
| TemplateTrigger dataclass | `apps/projects/services/template_import.py:430+` | Currently has no pre-substitution-effects field |

**Critical passage emission (v2.py:11044-11053, verbatim):**
```python
passage_header = (
    f":: {{node_passage_name}}\n"
    f"{{substitution_check}}"  # PRD 25 — fires before any other passage logic
    f"{{dev_canvas_info}}"
    f"{{node_content}}\n\n"
    f"<<set $game_state.current_canvas = \"{{canvas.id}}\">>\n"
    f"<<set $game_state.current_node = \"{{node.id}}\">>\n"
    f"{{mark_trigger}}"
    f"{{track_visited_node}}"
)
```

Substitution check is line 2. Any content emitted before it would run before the substitution preempt.

### §4.3 — Proposed schema addition

Add optional `pre_substitution_effects: List[Dict[str, Any]]` field to `TemplateTrigger` dataclass at template_import.py:430+. Each entry uses the same shape as `TemplateChoiceEffect` (per Doc 68 §7.1 — `targetType` / `trait` / `op` / `value` / optional `clamp` / `cap`):

```toml
[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = true

[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait = "fitness"
op = "add"
value = 1
cap = 100

[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait = "energy"
op = "add"
value = -15
```

These effects fire unconditionally whenever the canvas is entered — even when a substitution rule preempts the rest of the passage. The activity's stat outcome "counts."

### §4.4 — Proposed emitter logic

In v2.py:11020-11053 passage emission, insert a new `pre_substitution_macros` string BEFORE the existing `substitution_check`:

```python
# NEW — build pre-substitution effects emission
pre_substitution_macros = ""
if i == 0 and hasattr(canvas, 'trigger') and canvas.trigger:
    pre_effects = getattr(canvas.trigger, 'pre_substitution_effects', None) or []
    for eff in pre_effects:
        # Same emission pattern as exit_block effects (v2.py:11291)
        ttype = eff.get('targetType', 'player')
        npc_id_js = self._format_npc_id_js(eff.get('npcId'))
        trait_js = eff.get('trait', '')
        op = eff.get('op', 'add')
        val = self._resolve_effect_value(eff.get('value', 0))
        clamp_js = 'true' if eff.get('clamp') else 'false'
        cap_js = json.dumps(eff.get('cap')) if eff.get('cap') is not None else 'null'
        pre_substitution_macros += (
            f'<<script>>setup.applyAndNotifyTrait("{ttype}", {npc_id_js}, '
            f'"{trait_js}", "{op}", {val}, {clamp_js}, {cap_js});<</script>>\n'
        )

# Insert into passage_header BEFORE the existing substitution_check
passage_header = (
    f":: {{node_passage_name}}\n"
    f"{{pre_substitution_macros}}"  # NEW — runs unconditionally
    f"{{substitution_check}}"        # existing
    f"{{dev_canvas_info}}"
    ...
)
```

**Critical: emission ordering matters.** `pre_substitution_macros` must precede `substitution_check` so the effects run before the `<<goto>>` can preempt.

### §4.5 — Backward compatibility

- Empty / absent `pre_substitution_effects` → current behavior unchanged
- Opt-in; no migration
- Zero risk to live TLS — verified: no current TLS canvas uses this field (field doesn't exist yet)

### §4.6 — Validator additions

1. **Each effect entry validates as a standard `TemplateChoiceEffect`** — reuse existing effect-parsing logic + field-name validation (which Item 3 will add).

2. **Suspicious-config warning:**
   - If `pre_substitution_effects` is set BUT canvas has NO substitution rules → WARN: *"Canvas '<id>' has pre_substitution_effects but no substitutions. Effects would apply on every canvas entry; consider moving to body or exit_block effects."*
   - The point of `pre_substitution_effects` is "applies even when substitution preempts." If there's no substitution, body effects achieve the same outcome with less indirection.

### §4.7 — Test plan

| Test | Setup | Expected |
|---|---|---|
| Schema round-trip | TOML with pre_substitution_effects → parse → emit | Effects retained in emitted passage |
| Solo branch | Substitution rules don't fire (dice misses) | Pre-substitution effects applied + solo body runs |
| Substitution branch | Substitution rule fires | Pre-substitution effects applied + `<<goto>>` preempts body |
| Ordering | Mock dice + check stat delta | Pre-substitution effects applied BEFORE `<<goto>>` (the load-bearing test) |
| Empty list | No pre_substitution_effects | Behaves identically to current engine |
| Validator: pre-effects without subs | Canvas has effects but no substitutions | WARN issued |

### §4.8 — Effort estimate

- Schema field addition + parser: 15 min
- Emitter logic in v2.py:11020-11053: 20 min
- Validator warning: 5 min
- 5 unit tests: 20 min
- **Total: ~1 hour**

### §4.9 — Priority + sequencing

**P2 — defer until needed.** Current TLS slice doesn't have an activity that "counts when interrupted" by design. The workaround (duplicate effect on substitution targets) is acceptable for the rare case. Per Doc 56 §9 doctrine: build when authoring forces.

**Sequencing trigger:** when a slice authoring case proposes an activity with unconditional stat outcome (Exercise → +Fit always; Sleep → energy restore always), surface to LO + ship Item 2.

---

## §5 — Engine Work Item 3: Field-name mismatch validator (P1)

### §5.1 — Problem statement

TLS effect schema uses field names `targetType` / `trait` / `npcId` (TemplateChoiceEffect dataclass at template_import.py:481-495). TLS predicate schema uses different field names `subject` / `trait_key` / `npc_id` (per `triggerConditionsSatisfied` at v2.py:3364-3386 + parsing at template_import.py:3604+). The two schemas are NOT mutually translated by any layer.

**Concrete silent-failure scenario:** LLM writes the following in a canvas effect context:
```toml
{ type = "trait", subject = "player", trait_key = "corruption", op = "add", value = 1 }
```

This is the PREDICATE syntax (Doc 68 §7.5). In an EFFECT context, the parser at template_import.py:2049 reads:
```python
trait=_require_str(te, "trait", "")  # reads "" — the "trait" field is missing
```

The effect dispatches to `applyAndNotifyTrait("player", null, "", "add", 1, ...)` — mutates an empty-string trait. **No build error. No runtime error.** The corruption never goes up. Player progression silently breaks.

**Severity: HIGH.** Doc 68 §7.6 reference card is the doctrine-only defense. This PRD converts it to build-time enforcement.

### §5.2 — Current code state

| Reference | Path | Purpose |
|---|---|---|
| Effect dataclass | `apps/projects/services/template_import.py:481-495` | `TemplateChoiceEffect` — fields: `targetType`, `npcId`, `trait`, `op`, `value`, `clamp`, `cap`, `flag`, `conditions` |
| Flag effect dataclass | `apps/projects/services/template_import.py:498-505` | `TemplateFlagEffect` — fields: `targetType`, `npcId`, `flag`, `op`, `conditions` |
| Effect parsing call sites | `apps/projects/services/template_import.py:1305, 1361, 2049` | Multiple `_require_str(e, "trait", "")` etc. |
| Predicate parsing | `apps/projects/services/template_import.py:3604+` | Cross-field validation: `subject + (trait_key XOR flag_key) + operator` |
| Predicate runtime | `apps/game_generation/twee_comprehensive/generators/v2.py:3364-3386` | Reads `it.trait_key`, `it.npc_id`, `it.operator` |

**The mismatch:**

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` | `operator` |
| Type discriminator | (dispatched by `trait` vs `flag` presence) | `type` (required) |

### §5.3 — Proposed validator additions

Add new validator function `_validate_effect_field_names(effect_dict, context_ctx) -> List[str]` (returns list of error messages):

**For effect contexts** (canvas node effects, exit_block effects, choice effects, daily_tick effects):

```python
def _validate_effect_field_names_in_effect(eff, ctx):
    errors = []
    FORBIDDEN_IN_EFFECT = {
        'subject': "Field `subject` not allowed in effect block (use `targetType`). See Doc 68 §7.6 field-name reference card. Likely cause: predicate syntax mixed into effect context.",
        'trait_key': "Field `trait_key` not allowed in effect block (use `trait`). See Doc 68 §7.6.",
        'flag_key': "Field `flag_key` not allowed in effect block (use `flag`). See Doc 68 §7.6.",
        'npc_id': "Field `npc_id` not allowed in effect block (use `npcId`). See Doc 68 §7.6.",
        'operator': "Field `operator` not allowed in effect block (use `op`). See Doc 68 §7.6.",
    }
    for forbidden_field, message in FORBIDDEN_IN_EFFECT.items():
        if forbidden_field in eff:
            errors.append(f"{{ctx}}: {{message}} Field appeared with value: {{eff[forbidden_field]!r}}")
    return errors
```

**For predicate contexts** (canvas trigger conditions, choice conditions, exit_block conditions, daily_tick effect conditions):

```python
def _validate_effect_field_names_in_predicate(item, ctx):
    errors = []
    FORBIDDEN_IN_PREDICATE = {
        'targetType': "Field `targetType` not allowed in predicate item (use `subject`). See Doc 68 §7.6 field-name reference card. Likely cause: effect syntax mixed into condition context.",
        'npcId': "Field `npcId` not allowed in predicate item (use `npc_id`). See Doc 68 §7.6.",
    }
    # Conditional bans: only if type is trait/flag
    if item.get('type') == 'trait' and 'trait' in item:
        errors.append(f"{{ctx}}: Field `trait` not allowed in predicate item with type='trait' (use `trait_key`). See Doc 68 §7.6.")
    if item.get('type') == 'flag' and 'flag' in item:
        errors.append(f"{{ctx}}: Field `flag` not allowed in predicate item with type='flag' (use `flag_key`). See Doc 68 §7.6.")
    if 'op' in item:
        errors.append(f"{{ctx}}: Field `op` not allowed in predicate item (use `operator`). See Doc 68 §7.6.")
    for forbidden_field, message in FORBIDDEN_IN_PREDICATE.items():
        if forbidden_field in item:
            errors.append(f"{{ctx}}: {{message}}")
    return errors
```

### §5.4 — Where the validator hooks in

**Effect-context check points** (call `_validate_effect_field_names_in_effect` before `_require_str` calls):
- template_import.py:1305 (choice effects parsing)
- template_import.py:1361 (additional choice effects parsing)
- template_import.py:2049 (daily_tick.traitEffects parsing)
- Wherever else effects are parsed — grep `_require_str.*\"trait\"` for all call sites

**Predicate-context check points** (call `_validate_effect_field_names_in_predicate` before condition item validation):
- template_import.py:3604+ (the existing condition-item parsing block)
- Apply to every condition source: canvas trigger conditions, choice conditions, exit_block.choices conditions, etc.

### §5.5 — Backward compatibility

- **Only catches WRONG field names** (which today silently fail; no valid TOML uses them)
- Live TLS verified: 7_final_game.toml uses correct effect field names (line 82: `{ targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 }`)
- Existing TLS slice + any other clean TOML will pass through unchanged
- Zero false positives expected

### §5.6 — Test plan

| Test | Setup | Expected |
|---|---|---|
| Effect with `subject` field | `{ subject = "player", trait = "X", op = "add", value = 1 }` | ERROR with Doc 68 §7.6 cite |
| Effect with `trait_key` field | `{ targetType = "player", trait_key = "X", op = "add", value = 1 }` | ERROR |
| Effect with `npc_id` field | `{ targetType = "npc", npc_id = "Y", trait = "X" }` | ERROR |
| Effect with `operator` field | `{ targetType = "player", trait = "X", operator = "add" }` | ERROR |
| Condition with `targetType` field | `{ type = "trait", targetType = "player", trait_key = "X", operator = "gte", value = 1 }` | ERROR |
| Condition with `trait` field (when type=trait) | `{ type = "trait", subject = "player", trait = "X", operator = "gte", value = 1 }` | ERROR |
| Condition with `op` field | `{ type = "trait", subject = "player", trait_key = "X", op = "gte", value = 1 }` | ERROR |
| Correct effect | `{ targetType = "player", trait = "X", op = "add", value = 1 }` | passes |
| Correct predicate | `{ type = "trait", subject = "player", trait_key = "X", operator = "gte", value = 1 }` | passes |
| TLS slice build | Live `7_final_game.toml` | passes (no regressions) |

### §5.7 — Effort estimate

- Two validator functions + helper: ~30 min
- Integration at ~6 parser call sites: ~45 min
- ~10 unit test cases + integration test against live TLS slice: ~1 hour
- Helpful error messages with Doc 68 citation: ~30 min
- **Total: ~3 hours**

### §5.8 — Priority + sequencing

**P1 — DO FIRST.** This is the single highest-risk silent-failure mode discovered this session. Without it, `prompts_v2/` batch 1 + every subsequent game generation depends on Doc 68 §7.6 reference card being correctly followed by the LLM. The validator converts doctrine-prevented to mechanism-prevented.

**Critical sequencing constraint:** ship before `prompts_v2/` generates its first test game. Otherwise the first generated game has unverifiable correctness (might silently no-op on every effect; might not).

---

## §6 — Engine Work Item 4: Undeclared trait validator (P1)

### §6.1 — Problem statement

TLS validator at template_import.py:2382-2547 builds `_player_trait_keys = set((template.player.core_traits or {}).keys())` and rejects sidebar items referencing undeclared traits. BUT: effects + conditions are NOT validated against the same set.

The LLM can emit an effect on `corruption` without declaring `corruption` in `[player.core_traits]`, and:
- The runtime executes `applyAndNotifyTrait("player", null, "corruption", "add", 1, ...)` against an uninitialized trait
- Initial reads return `undefined` (per v2.py:5065: `(npc && npc.core_traits) ? (npc.core_traits[trait] || 0) : 0` falls through to 0)
- Some downstream comparisons evaluate against `undefined` returning false unconditionally
- Conditions silently never unlock content
- No build error fires

**Concrete failure scenario:**
```toml
# Author forgets to declare corruption in [player.core_traits]

# Effect emits fine (parser doesn't check):
{ targetType = "player", trait = "corruption", op = "add", value = 1 }

# Condition checks:
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 }

# Runtime at v2.py:3370 reads:
#   leftVal = (player.core_traits || {{}})["corruption"]   →  undefined
#   compare("gte", undefined, 15)                          →  false (always)

# Content never unlocks. No error logged.
```

**Severity: HIGH.** Doc 68 §2.5 (trait pre-declaration requirement) is the doctrine-only defense. This PRD converts it to build-time enforcement.

### §6.2 — Current code state

| Reference | Path | Purpose |
|---|---|---|
| Sidebar trait validator | `apps/projects/services/template_import.py:2382-2547` | Builds `_player_trait_keys` set from `template.player.core_traits.keys()`; rejects sidebar items referencing undeclared traits |
| Effect parsing call sites | `apps/projects/services/template_import.py:1305, 1361, 2049` | NO trait-key validation against declared traits |
| Condition parsing | `apps/projects/services/template_import.py:3604+` | NO trait-key validation against declared traits |
| Player core_traits declaration | TOML `[player.core_traits]` table → `template.player.core_traits: Dict[str, Any]` |
| NPC core_traits declaration | Per-NPC TOML `core_traits` table → `template.npcs[i].core_traits: Dict[str, Any]` |
| Stage advancement detection | `apps/game_generation/twee_comprehensive/generators/v2.py:5077-5087` | Matches `/^([a-z_]+)_stage$/` against trait names on player namespace |
| NPC trait read runtime | `apps/game_generation/twee_comprehensive/generators/v2.py:3380` | `npc2.core_traits[String(tkey)]` — reads undefined if not declared |

### §6.3 — Proposed validator additions

Add new validator function `_validate_trait_declaration(template) -> List[str]` (or extend the existing validator pass):

**For each effect with trait reference:**

```python
def _validate_trait_declaration_in_effect(eff, template, ctx):
    errors = []
    if eff.get('trait'):  # only validate trait effects (not flag effects)
        target = eff.get('targetType', 'player')
        trait_name = eff['trait']
        if target == 'player':
            if trait_name not in (template.player.core_traits or {}).keys():
                # Special-case: stage trait pattern <slug>_stage
                stage_match = re.match(r'^([a-z_]+)_stage$', trait_name)
                if stage_match:
                    slug = stage_match.group(1)
                    matching_npc = next((n for n in template.npcs if n.id == slug or n.id.endswith('_' + slug)), None)
                    if matching_npc and matching_npc.arc_stages:
                        # Stage trait must be declared in [player.core_traits] even though it's stage-pattern
                        if trait_name not in (template.player.core_traits or {}).keys():
                            errors.append(
                                f"{ctx}: Effect references stage trait '{trait_name}' (matches stage pattern + NPC '{slug}' has arc_stages declared), "
                                f"but '{trait_name}' is NOT declared in `[player.core_traits]`. "
                                f"Declare it with initial value 0. See Doc 68 §2.5 + §9.0."
                            )
                else:
                    errors.append(
                        f"{ctx}: Effect references undeclared player trait '{trait_name}'. "
                        f"Declare it in `[player.core_traits]` block with an initial value before use. See Doc 68 §2.5."
                    )
        elif target == 'npc':
            npc_id = eff.get('npcId')
            if not npc_id:
                return errors  # field-name validator catches missing npcId
            npc = next((n for n in template.npcs if n.id == npc_id), None)
            if npc and trait_name not in (npc.core_traits or {}).keys():
                errors.append(
                    f"{ctx}: Effect references undeclared NPC trait '{trait_name}' for NPC '{npc_id}'. "
                    f"Declare it in `[[npcs]] ... core_traits` block. See Doc 68 §2.5."
                )
    return errors
```

**For each condition item with trait reference:**

```python
def _validate_trait_declaration_in_predicate(item, template, ctx):
    # Same logic mirrored for predicate field names (subject / trait_key / npc_id)
    ...
```

### §6.4 — Where the validator hooks in

Same call sites as Item 3 (the field-name validator). Combined Item 3 + Item 4 in one pass over the parser is more efficient — both extend the same effect-parsing + condition-parsing loops.

- After `_require_str(e, "trait", "")` at template_import.py:1305 / 1361 / 2049 — call `_validate_trait_declaration_in_effect`
- Inside condition-parsing block at template_import.py:3604+ — call `_validate_trait_declaration_in_predicate`

### §6.5 — Backward compatibility

- Existing TLS slice declares all its traits in `[player.core_traits]` (verified during Doc 68 audit) — should pass clean
- Catches drift only; no risk to currently-correct content
- Stage trait pattern handled gracefully (see §6.3 special-case)

**Edge case:** TLS Tier 2 traits (fitness, beauty, exhibitionism, intelligence per Doc 68 §5) that are referenced but not used in current slice. If TLS slice doesn't declare these in `[player.core_traits]` AND doesn't reference them in any effect/condition → no error. If author adds an effect on `fitness` without declaring it → error. Correct behavior.

### §6.6 — Test plan

| Test | Setup | Expected |
|---|---|---|
| Effect on undeclared player trait | `[player.core_traits]` missing `corruption`; effect uses it | ERROR with Doc 68 §2.5 cite |
| Effect on declared player trait | `[player.core_traits.corruption] = 0`; effect uses it | passes |
| Effect on declared NPC trait | NPC has `core_traits.arousal = 0`; effect targets it | passes |
| Effect on undeclared NPC trait | NPC missing `core_traits.arousal`; effect targets it | ERROR |
| Condition on undeclared player trait | Condition references missing trait | ERROR |
| Condition on declared player trait | Trait declared | passes |
| Stage trait declared in player + NPC has arc_stages | `frank_stage = 0` in `[player.core_traits]` + Frank has `arc_stages = [...]` | passes |
| Stage trait NOT declared in player | NPC has arc_stages but `frank_stage` not in `[player.core_traits]` | ERROR with stage-pattern hint |
| Stage trait declared but NPC has no arc_stages | `frank_stage = 0` in player but Frank's `arc_stages = []` | WARNING (allowed but suspicious — stage trait exists with no arc) |
| TLS slice build | Live `7_final_game.toml` | passes (all traits declared per Doc 68 audit) |

### §6.7 — Effort estimate

- Validator function + helpers: ~45 min
- Integration at same parser call sites as Item 3: ~30 min (shared infrastructure with Item 3)
- ~10 unit test cases + integration test against TLS slice: ~1 hour
- Helpful error messages with Doc 68 §2.5 / §9.0 citations: ~30 min
- Stage-trait special-case logic: ~30 min
- **Total: ~3 hours**

### §6.8 — Priority + sequencing

**P1 — DO FIRST (alongside Item 3).** Closes the second-highest silent-failure mode. Items 3 + 4 together close BOTH HIGH-severity gaps the session discovered. They share the parser call-site infrastructure (both extend the same effect/condition parsing loops), so implementing them together is ~1.5 hours cheaper than separately.

**Critical sequencing constraint:** ship with Item 3 BEFORE `prompts_v2/` generates its first test game.

---

## §7 — Author-responsibility patterns (no engine work)

Cataloged for completeness — explaining why these 4 items are NOT in the engine queue, so they don't get re-litigated in future sessions.

### §7.1 — `FinishMasturbation` auto-reset macro (RTS-only)

**Discovered via:** Doc 68 audit (2026-05-26). Grep across v2.py + template_import.py returned **zero hits** for `FinishMasturbation`. This is an RTS macro, not a TLS engine primitive.

**RTS pattern:** macro that automatically sets `$player.arousal = 0` at masturbation climax.

**Why this is NOT engine work:**
- The author already controls climax canvas content. Adding an auto-reset macro is one more engine primitive to maintain.
- Authors lose visibility — if the macro auto-zeroes, the author can't easily tell from TOML reading WHEN arousal gets reset.
- The doctrine-only pattern (author emits explicit reset) is mechanically equivalent and more readable.

**Workaround pattern:**
```toml
# At the masturbation climax canvas's exit_block:
[canvases.exit_block]
effects = [
  { targetType = "player", trait = "arousal", op = "set", value = 0 },
  # ... other climax effects
]
```

**Doctrine reference:** Doc 68 §3 (player arousal modifier note) + §7.3 (per-trait operation conventions). The trait catalog teaches the workaround explicitly.

**Net cost of NOT shipping an engine fix:** one TOML line per climax canvas. Acceptable.

### §7.2 — `FinishSex` auto-reset macro (RTS-only)

**Discovered via:** Doc 68 audit. Same grep pass as §7.1; zero hits.

**RTS pattern:** macro that zeroes BOTH `$player.arousal` AND the partner NPC's `$npc.X.arousal` at sex climax.

**Why this is NOT engine work:** same reasoning as §7.1. Authors emit TWO explicit reset effects per sex climax canvas. The doctrine teaches the pattern; the engine doesn't need to know.

**Workaround pattern:**
```toml
# At the sex climax canvas's exit_block:
[canvases.exit_block]
effects = [
  { targetType = "player", trait = "arousal", op = "set", value = 0 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "set", value = 0 },
  # ... other climax effects
]
```

**Doctrine reference:** Doc 68 §4 (NPC arousal modifier note) + §3 (player arousal).

**Net cost of NOT shipping:** two TOML lines per sex climax canvas (per NPC variant). Acceptable.

### §7.3 — `op = "sub"` for trait effects

**Discovered via:** Doc 68 audit at v2.py:4962-4964. Engine has only:
```javascript
if (op === 'add') { ... } else if (op === 'set') { ... }
```
No `case 'sub'`. Doc 68's first draft listed `sub`; wrong claim.

**RTS pattern:** N/A. RTS uses `<<set $player.energy -= 10>>` Twine-native syntax; doesn't have a structured effect schema.

**Why this is NOT engine work:**
- The negative-add pattern (`op = "add"`, `value = -10`) is mechanically equivalent.
- Adding a third op (`sub`) means engine maintenance + documentation + tests for zero functional gain.
- Adds confusion: now there's both `op = "sub" value = 10` AND `op = "add" value = -10`; redundant.

**Workaround pattern:**
```toml
# Decay 10 energy:
{ targetType = "player", trait = "energy", op = "add", value = -10 }

# Daily hygiene decay:
[[engine.daily_tick.traitEffects]]
targetType = "player"
trait = "hygiene"
op = "add"
value = -10
```

**Doctrine reference:** Doc 68 §7.2 (allowed `op` values — only `add` + `set`) + §10 anti-pattern bullet on `op = "sub"`.

**Net cost of NOT shipping:** one negative sign per decay effect. Trivial.

### §7.4 — `previous()` guard predicate (per-passage immediate guard)

**Discovered via:** Doc 67 §3.6 source extraction (RTS `BedroomSleep`). Pattern:
```twee
<<if previous() isnot "BedroomSleepDadScene" && previous() isnot "SleepingBrother">>
```
Prevents the same scene from re-firing if player just came back from it.

**RTS pattern:** Twine-native `previous()` function call inside `<<if>>`. Not a structured predicate type.

**Why this is NOT engine work:**
- `max_triggers_per_day = 1` (already shipped) handles ~95% of cases where loop-spam matters. RTS uses `executedToday` per-scene flag for the same purpose.
- The rare cases that need same-day immediate-re-fire prevention can use:
  1. Flag-set on canvas exit (`{ targetType = "player", flag = "just_finished_X", op = "set" }`)
  2. Flag-clear on day rollover via `[engine.daily_tick].traitEffects`
  3. Condition check on next canvas entry referencing the flag
- 3 TOML lines per rare case. Acceptable workaround.

**Why adding a `previous()` predicate type is wrong:**
- It would require runtime to track passage history (engine doesn't today).
- Couples doctrine to Twine internals (`previous()` is Twine, not engine).
- Per-day caps cover most cases more cleanly.

**Workaround pattern:**
```toml
# Canvas A's exit sets a flag:
[canvases.exit_block]
effects = [
  { targetType = "player", flag = "just_did_A", op = "set" },
]

# Canvas A's trigger conditions check the flag:
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "just_did_A", operator = "is_false" },
]

# Daily tick clears the flag:
[[engine.daily_tick.traitEffects]]
# (would need flag-effect support in daily_tick — currently traitEffects only handles traits;
#  see Doc 65 if this needs to scale)
```

**Doctrine reference:** Doc 67 §3.6 (per-day cooldowns section) names the workaround.

**Net cost of NOT shipping:** for the rare case, ~3 TOML lines. Acceptable.

---

## §8 — Prioritization + sequencing recommendation

### §8.1 — Recommended ship order

1. **Items 3 + 4 together (P1, ~6 hours combined):**
   - Field-name mismatch validator (§5)
   - Undeclared trait validator (§6)
   - Both extend the same parser infrastructure (effect-parsing + condition-parsing loops). Combined session is ~1.5 hours cheaper than separately due to shared integration work.
   - **Closes BOTH HIGH-severity silent-failure modes.**
   - **Must ship BEFORE `prompts_v2/` generates its first test game** — otherwise the first generated game has unverifiable correctness.

2. **Items 1 + 2 (P2, ~2.5 hours combined):**
   - Pattern B `exclusive_group` (§3)
   - Pattern C `pre_substitution_effects` (§4)
   - Independent of each other; can ship in either order or separately.
   - Defer until slice authoring case forces either per Doc 56 §9 doctrine.
   - **Pattern B more likely to come up first** (multi-NPC dispatchers exist in slice; just no mutual-exclusion case yet).

### §8.2 — Total engine effort

If all 4 ship: **~8-9 hours across 2 sessions** (one P1 session, one P2 session when triggered).

### §8.3 — Sequencing rationale

**P1 first because:**
- Silent-failure prevention > feature parity (a generated game that builds-but-doesn't-work is worse than one that fails-fast)
- Items 3 + 4 share infrastructure (~1.5 hours saved)
- Items 3 + 4 are zero-feature, pure-correctness — no design decisions to relitigate
- Items 3 + 4 enable safe `prompts_v2/` rollout — mechanism-prevented validation lets us trust generated games without manual audit

**P2 deferred because:**
- Pattern B + C are feature extensions; current slice doesn't need them
- Doc 56 §9 doctrine: build engine when authoring forces, not speculatively
- Pattern B workaround (Pattern A approximation) is acceptable for the slice's rare Pattern-B-shaped use cases (if any arise)
- Pattern C workaround (duplicate effect on substitution targets) is ugly but functional

### §8.4 — Risks of NOT shipping

| Item | Risk if never shipped |
|---|---|
| 1 (Pattern B) | Slice can't author truly mutually-exclusive NPC variants. Acceptable; current slice doesn't need it. |
| 2 (Pattern C) | Some activities can't have unconditional stat outcomes. Acceptable; workaround exists. |
| **3 (Field-name validator)** | **Every `prompts_v2/` generation depends on Doc 68 §7.6 being perfectly followed by the LLM. One slip = silent broken game. HIGH risk.** |
| **4 (Undeclared trait validator)** | **Every generation depends on Doc 68 §2.5 being perfectly followed. One slip = silent broken content gates. HIGH risk.** |

Items 3 + 4 are the ones that genuinely shouldn't stay unshipped. Items 1 + 2 are optional polish.

---

## §9 — Out of scope (intentional)

Things this PRD does NOT cover. Each is its own queue.

- **Doc 62 / 63 / 64 engine PRDs.** Pre-existing; tracked separately. Per LO's "ignore the existing PRD" directive this session, those are not in Doc 69's scope. They remain in the queue independently.
- **Phase 2+ engine systems** (pregnancy / scandal / gallery / cross-arc tracker per Doc 65). Strategic decisions pending LO call. Not engine implementation queue until LO scopes per Doc 65.
- **TLS slice content changes.** Held per Doc 66.
- **`prompts_v2/` authoring.** Held per Doc 66. Doc 69 enables `prompts_v2/` to ship safely (via Items 3+4) but doesn't author the v2 prompts themselves.
- **CLAUDE.md updates.** Held per Doc 66.
- **MEMORY.md updates.** Optional housekeeping; can be added in a follow-up.
- **Existing-engine refactoring.** No changes to `applyAndNotifyTrait`, `checkAndSubstituteCanvas`, `triggerConditionsSatisfied`, or any other shipped function — Doc 69 ADDS validation + ADDS optional schema fields. Nothing existing changes behavior.

---

## §10 — Cross-references

### Redesign docs (this folder)

- **Doc 24** — 3 Lanes for Repeatable NPC Content (§8 cooldowns; §9 predicate vocabulary — context for §7.4 workaround)
- **Doc 56** §9 doctrine: *"don't pre-commit to engine scope; build engine when an authoring gap forces it"* — the basis for P2 deferral
- **Doc 65** — Phase 2+ Strategic Scope (explicitly out of Doc 69's scope; cross-referenced for §9 boundary)
- **Doc 66** — Session Record / Prompts Rewrite Pivot (session context; engine work held per pivot; Doc 69 captures what gets unblocked when P1 items ship)
- **Doc 67** §5 + §5.1 + §5.2 — Pattern B/C engine extension specs (source for Items 1 + 2 here)
- **Doc 68** §2.5 + §7 + §7.6 + §10 — trait catalog audit findings (source for Items 3 + 4 here)

### Engine files (line numbers verified this session)

| Reference | File:line | What lives there |
|---|---|---|
| `TemplateChoiceEffect` | `apps/projects/services/template_import.py:481-495` | Effect dataclass — fields used by §5 validator |
| `TemplateFlagEffect` | `apps/projects/services/template_import.py:498-505` | Flag effect dataclass — fields used by §5 validator |
| Effect parsing call sites | `apps/projects/services/template_import.py:1305, 1361, 2049` | Where §5 + §6 validators integrate |
| Sidebar trait validator | `apps/projects/services/template_import.py:2382-2547` | Reference for §6 — builds `_player_trait_keys` |
| Substitution rule validator | `apps/projects/services/template_import.py:2946-2960` | Where §3 validator additions integrate |
| Predicate parsing | `apps/projects/services/template_import.py:3604+` | Cross-field validation; where §5 + §6 validators integrate for predicates |
| `triggerConditionsSatisfied` trait predicate | `apps/game_generation/twee_comprehensive/generators/v2.py:3364-3386` | Reference for §5 — actual field names predicate uses at runtime |
| `checkAndSubstituteCanvas` | `apps/game_generation/twee_comprehensive/generators/v2.py:4597-4626` | Where §3 runtime logic modifies |
| `applyTraitEffect` op dispatch | `apps/game_generation/twee_comprehensive/generators/v2.py:4962-4964` | Reference for §7.3 — only `add` + `set` |
| `applyAndNotifyTrait` | `apps/game_generation/twee_comprehensive/generators/v2.py:5071+` | Reference for §6 — runtime trait mutation; stage advancement detection at lines 5077-5087 |
| Passage emission | `apps/game_generation/twee_comprehensive/generators/v2.py:11020-11053` | Where §4 emitter modifies |
| `daily_tick.traitEffects` execution | `apps/game_generation/twee_comprehensive/generators/v2.py:4787-4807` | Reference for §7.4 workaround (flag-clear on day rollover) |

### Live TLS source artifacts referenced

- `games/the_long_summer_test/toml_phases/7_final_game.toml:82` — canonical effect syntax in live TLS (verifies §3.5 + §5.5 backward compat claims)

---

## §11 — Verification (when each item ships)

When future engine sessions ship any of Items 1-4, verify per these checks.

### §11.1 — Item 1 (`exclusive_group`)

- [ ] Pytest includes new test cases covering Pattern B partition (1000-trial probability check ≈ 50% for 3 NPCs at 0.17 each)
- [ ] Pytest covers failed-condition fall-through-to-solo semantics (dice claims slot, conditions fail → solo, not next rule)
- [ ] Validator: chance sum > 1.0 in same group → WARN
- [ ] Validator: duplicate target_canvas_id across groups → ERROR
- [ ] Validator: single-rule group → WARN
- [ ] Live build: TLS slice (no `exclusive_group` field anywhere) builds clean — backward compat verified
- [ ] Live test: author 3-rule exclusive group in test canvas; verify probability matches Pattern B math

### §11.2 — Item 2 (`pre_substitution_effects`)

- [ ] Pytest verifies effects apply in BOTH branches:
  - Solo branch (substitution misses) — effects + body + exit_block all run
  - Substitution branch (substitution preempts) — effects run, but body + exit_block skip
- [ ] Pytest verifies ordering: pre_substitution_effects run BEFORE substitution check (mock dice, check stat delta)
- [ ] Validator warning: pre_substitution_effects without substitutions
- [ ] Live build: TLS slice (empty / absent field) builds clean
- [ ] Live test: author Exercise-like canvas with `+Fit` in pre_substitution_effects + substitution to Grandpa scene; verify Fit applies even when Grandpa fires

### §11.3 — Item 3 (field-name validator)

- [ ] Deliberately-wrong test canvases:
  - Effect with `subject` → build fails with Doc 68 §7.6 cite
  - Effect with `trait_key` → build fails
  - Effect with `npc_id` → build fails
  - Effect with `operator` → build fails
  - Condition with `targetType` → build fails
  - Condition with `trait` (when type=trait) → build fails
  - Condition with `op` → build fails
- [ ] TLS slice builds clean (effect-context = all `targetType`; predicate-context = all `subject` — verified during Doc 68 audit)
- [ ] Error messages include corrected line snippet for copy-paste fix
- [ ] All error messages cite Doc 68 §7.6

### §11.4 — Item 4 (undeclared trait validator)

- [ ] Deliberately-undeclared trait reference (effect):
  - Build fails with Doc 68 §2.5 cite
  - Error names the trait + tells author to declare it in `[player.core_traits]`
- [ ] Deliberately-undeclared trait reference (condition):
  - Build fails with Doc 68 §2.5 cite
- [ ] Stage trait pattern:
  - `frank_stage` declared in `[player.core_traits]` + Frank has `arc_stages` → passes
  - `frank_stage` NOT declared → ERROR with stage-pattern hint
  - `frank_stage` declared but Frank's arc_stages is empty → WARNING
- [ ] NPC trait pattern:
  - NPC `core_traits` declares trait → effect on it passes
  - NPC missing trait declaration → effect ERROR
- [ ] TLS slice builds clean (all traits declared per Doc 68 audit verification)

### §11.5 — Combined Item 3 + Item 4 session

When Items 3 + 4 ship together (recommended P1 session):
- [ ] Single PR introduces both validators
- [ ] Shared integration at parser call sites is consolidated (don't duplicate the loop traversal)
- [ ] Combined pytest suite covers ~18 cases across both validators
- [ ] TLS slice + any other test fixtures build clean
- [ ] One end-to-end test: generate a test game with deliberately-broken canvas (one field-name mismatch + one undeclared trait reference) → build fails with TWO errors, both helpful

---

## §12 — Confidence ladder

Per Doc 24 methodology — what's source-verified vs assumed.

✅ **HIGH confidence (verified this session against engine source):**
- Pattern A native at v2.py:4597-4626 (read line-by-line)
- Pattern B + C NOT shipped (proven by code reading + audit pass)
- `FinishMasturbation` / `FinishSex` NOT in TLS (grep zero hits)
- Effect schema field names: `targetType` / `trait` / `npcId` (verified at template_import.py:481-505 + live TOML line 82)
- Predicate schema field names: `subject` / `trait_key` / `npc_id` / `operator` (verified at v2.py:3364-3386 + template_import.py:3604+)
- Engine has only `op = "add"` + `op = "set"` (verified at v2.py:4962-4964)
- Sidebar validator catches undeclared traits at template_import.py:2382-2547; effect/condition parsers do NOT (verified by reading parser loops)
- Stage advancement detection on player namespace pattern `<slug>_stage` (verified at v2.py:5077-5087)
- All 4 sidebar item types shipped (`trait_words`, `trait_bar`, `trait_status_text`, `stage_label`) — verified at template_import.py:2388, 2439, 2527, 2588

🟡 **MED confidence (proposed implementation; tested only in design):**
- Proposed runtime logic for Item 1 (`exclusive_group` partition) — designed against current loop shape; not yet tested
- Proposed emitter logic for Item 2 (`pre_substitution_effects`) — designed against current passage_header pattern; not yet tested
- Proposed validator functions for Items 3 + 4 — designed against current parser call sites; not yet integrated
- Effort estimates — based on code structure visible during audit; could vary ±50%

❌ **NOT yet established (deferred):**
- Whether the Pattern B partition logic should process groups before independent rules or vice versa — recommended groups-first in §3.4, but this is a design call LO could override
- Whether the field-name validator should be ERROR (recommended) or WARN — recommended ERROR per §5.3 severity, but LO could downgrade to WARN if false positives surface during initial rollout
- Whether stage trait without NPC `arc_stages` should be ERROR or WARN — recommended WARN per §6.6 (allowed but suspicious), but LO could tighten to ERROR

---

**End of Doc 69.**
