# Doc 63 — Quest Card + Capstone Validator Extension PRD

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Engine PRD — implementation spec; NOT shipped. Doctrine locked across Doc 50 / Doc 56 / Doc 57; validator codifies enforcement.
**Supersedes:** nothing
**Sibling of:** Doc 62 (Guide Field PRD), Doc 64 (Sidebar Radar PRD)
**Triggered by:** Doc 50 §6 explicitly named the validator as the mechanism for R1–R4 enforcement. Doc 56 R6 + Doc 57 R1 added more rules. Marge case study (Doc 54) cost 8 hours of authoring against undetected doctrine drift. Validator converts doctrine to build-time mechanism so the next NPC arc doesn't repeat the same drift.

---

## §1 — The problem this PRD solves

Doctrine rules across Doc 50 + Doc 56 + Doc 57 are currently human-read. Recent audits found:
- 5 `txt_only` quest cards (Ryan + Jake) shipped against Doc 50 R3 — caught only by manual audit during this session
- `frank_kitchen_morning_hub` (and 3 other hubs) had tier-aware openings against Doc 56 R1 — caught only by manual audit
- The capstone alignment audit verified 13 capstones but required dedicated session time

A validator catches these at build time. Drift becomes an error message instead of a 6-month rediscovery. Per Doc 50 §6 the validator is named; this PRD locks the implementation.

**Doctrine principle: validator = doctrine as mechanism.** The rule isn't real until it's enforced.

---

## §2 — Rules to validate

Six rules. Three from Doc 50 (already named in Doc 50 §6 as validatable). Two from Doc 56. One from Doc 57.

### Rule 1 — Capstone coverage (Doc 50 R1)

**Statement:** Every canvas with `priority >= 9` AND `is_repeatable = false` (or `is_repeatable = true + self-gate flag` per Doc 57 R1 amendment) AND a flag-setting effect on at least one exit choice MUST be referenced by some `quest_card`'s `ready_canvas` field — OR have an `# off-panel:` comment within 3 lines preceding the `[[canvases]]` declaration.

**Severity:** ERROR.

**Detection:**
1. Walk all canvases.
2. For each canvas matching the capstone fingerprint, check:
   - Is it referenced by any `quest_card.ready_canvas == canvas.id`?
   - If not, scan the TOML lines preceding the canvas declaration for a `# off-panel:` comment (within 3 lines).
3. If neither, emit error: `f"canvas '{canvas.id}': priority {priority} + is_repeatable={is_repeatable} + flag-setting effects qualify it as a capstone, but no quest_card.ready_canvas points at it and no # off-panel: comment found. Doc 50 R1 / Doc 57 R3."`

### Rule 2 — Climbing-bullet rule (Doc 50 R2)

**Statement:** If a quest_card has a `ready_canvas`, AND the `ready_canvas`'s trigger conditions include a trait gate STRICTLY above what the card's `when` clause enforces, the card MUST have a `goals` block surfacing that trait climb.

**Severity:** WARNING.

**Detection:**
1. For each quest_card with `ready_canvas` set:
   - Resolve the `ready_canvas` to a canvas.
   - Parse its `trigger.conditions.items` for trait gates.
   - Compare with the card's `when` clause traits.
   - For each gate in `ready_canvas.conditions` whose value is strictly above what `when` already implies, check: does the card have a `goals` entry for that trait?
2. If not, emit warning: `f"quest_cards[{idx}]: card's ready_canvas '{canvas.id}' has trait gate {trait}>={value}, but card's when clause only implies {trait}>={existing_value}. Need a 'goals' bullet surfacing the climb. Doc 50 R2."`

### Rule 3 — Terminal placement (Doc 50 R3)

**Statement:** A quest_card with `terminal = true` MUST be the last card in its NPC chain (`npc_id`). No card whose `when` requires a flag set AFTER the terminal's flag may exist for the same `npc_id`.

**Severity:** ERROR.

**Detection:**
1. For each `npc_id` with at least one card having `terminal = true`:
   - Find the terminal card's setter flag (look up its `when` flag values).
   - Check no other card for the same `npc_id` has a `when` requiring `flag_is_true` for a flag set AFTER the terminal's chain position.
2. Emit error if violation found: `f"quest_cards[{idx}] (npc='{npc_id}'): terminal=true card found, but card {other_idx} with when-flag '{flag}' exists downstream. Doc 50 R3."`

### Rule 4 — Chain continuity (Doc 50 R4)

**Statement:** Every "post-X" quest_card (one whose `when` requires `flag_X = is_true`) MUST have a sibling "pre-X" quest_card whose `ready_canvas` points at the canvas that sets X.

**Severity:** WARNING.

**Detection:**
1. For each quest_card, extract flags it requires (`when` clause flag conditions with `op = "is_true"`).
2. For each such flag F:
   - Find canvases that set F via `flagEffects`.
   - Check at least one quest_card has `ready_canvas` pointing at one of those setter canvases.
3. If no quest_card points at any F-setter, emit warning: `f"quest_cards[{idx}]: card requires flag '{flag}' is_true, but no sibling card has ready_canvas pointing at any canvas that sets '{flag}'. Doc 50 R4."`

### Rule 5 — No `txt_only` quest cards (Doc 56 R6)

**Statement:** Every quest_card MUST satisfy AT LEAST ONE of:
- (a) Has `ready_canvas` set (capstone mode)
- (b) Has `goals` array with at least one entry (mechanic mode)
- (c) Has `terminal = true` (terminal mode)
- (d) Has a `# unlocks:` comment within 5 lines preceding the `[[quest_cards]]` declaration (mechanic mode with activity-driven unlock)

**Severity:** ERROR.

**Detection:**
1. For each quest_card, check the 4 conditions above.
2. If none satisfied: scan the preceding 5 lines of TOML for `# unlocks:` comment.
3. If still none: emit error: `f"quest_cards[{idx}]: txt_only card — no ready_canvas, no goals, not terminal, no # unlocks: comment. Doc 56 R6."`

**Note:** This rule catches the 5 violations we fixed in this session. After-fix verification: 0 txt_only cards in slice (verified).

### Rule 6 — Capstone trigger fingerprint (Doc 57 R1, amended)

**Statement:** Every canvas with `priority >= 9` MUST satisfy ALL of:
- `trigger_mode = "manual"` (or default — engine treats unset as manual)
- EITHER `is_repeatable = false` OR (`is_repeatable = true` AND `conditions` contain a `flag_is_false` gate on the same flag that the canvas's exit `flagEffects` sets)
- At least one exit choice has a `flagEffects` setting a flag (the "setter flag")

**Severity:** ERROR.

**Detection:**
1. For each canvas with `priority >= 9`:
   - Check `trigger_mode` is manual or absent.
   - Check `is_repeatable` pattern: either false, OR true with a self-gate.
   - Walk exit choices; check at least one has `flagEffects` with `op = "set"`.
2. If any check fails, emit error: `f"canvas '{canvas.id}': priority {priority} requires capstone fingerprint per Doc 57 R1. Failures: [{failures}]."`

**Note:** This rule will catch any future canvas that drifts toward "high-priority but never-retires" shape.

---

## §3 — Validator hooks

File: `apps/projects/services/template_import.py`

### Extend `_validate_quests_cards()` (line 3733)

Add Rule 1, 3, 4, 5 implementations as sub-functions called from this existing entry point. The function already iterates `quest_cards` — extend with cross-reference checks against canvases (Rule 1 requires walking canvases; pass them in or look them up via the project context).

### Add `_validate_capstone_fingerprint()` (new function)

Implements Rule 6. Called from the main validate routine alongside `_validate_quests_cards`. Iterates `canvases` checking each capstone-fingerprint.

### Add `_validate_off_panel_comments()` (new function, grep-based)

Implements the comment-based escape hatches for Rule 1 (`# off-panel:`) and Rule 5 (`# unlocks:`). Operates on raw TOML text, not parsed dict, because comments are stripped by the parser.

**Pattern:**
```python
import re

def _validate_off_panel_comments(toml_text: str, canvas_id: str) -> bool:
    """Returns True if canvas has an # off-panel: comment within 3 lines preceding."""
    # Find the canvas declaration
    pattern = rf'(?:#[^\n]*\n){{0,3}}\[\[canvases\]\]\s*\nid\s*=\s*"{re.escape(canvas_id)}"'
    match = re.search(pattern, toml_text)
    if not match:
        return False
    preceding = toml_text[max(0, match.start() - 500):match.start()]
    return '# off-panel:' in preceding[-300:]  # within ~3 lines

def _validate_unlocks_comment(toml_text: str, card_line_pos: int) -> bool:
    """Returns True if quest_card has an # unlocks: comment within 5 lines preceding."""
    preceding = toml_text[max(0, card_line_pos - 500):card_line_pos]
    return '# unlocks:' in preceding[-400:]  # within ~5 lines
```

Pass the raw TOML text into the validator entry point (alongside the parsed dict) so comments are accessible.

### Add Rule 2 cross-resolution

Rule 2 requires resolving `ready_canvas` ID → canvas dataclass → trigger.conditions. Helper function:

```python
def _resolve_ready_canvas(card: QuestsCard, canvases: List[TemplateCanvas]) -> Optional[TemplateCanvas]:
    if not card.ready_canvas:
        return None
    for c in canvases:
        if c.id == card.ready_canvas:
            return c
    return None  # broken pointer — Doc 50 R1 catches this separately
```

---

## §4 — Severity convention

Per Doc 50 §6 table:

| Rule | Severity | Why |
|---|---|---|
| R1 capstone coverage | ERROR | Off-panel capstones break the player's discoverability — silent drift |
| R2 climbing-bullet | WARNING | Card still renders; player misses progress indicator. Not game-breaking. |
| R3 terminal placement | ERROR | Premature terminal closes panel falsely. Player thinks arc is over. |
| R4 chain continuity | WARNING | Floating cards activate from inaccessible states. Catches gradually. |
| R5 txt_only | ERROR | Doctrine drift in shipped TOML. Must catch before merge. |
| R6 capstone fingerprint | ERROR | Capstone that re-fires breaks one-shot semantics. |

Build fails on ERRORs; warns on WARNINGs.

---

## §5 — Error message convention

Match existing pattern at template_import.py:3770 `errors.append(f"{ctx}: {detail}")`.

Context variable conventions:
- `ctx = f"quest_cards[{idx}]"` for card-level errors (existing pattern)
- `ctx = f"canvas '{canvas.id}'"` for canvas-level errors (capstone fingerprint, R1)
- `ctx = f"chain (npc='{npc_id}')"` for chain-continuity errors

Concrete examples:
- `"quest_cards[5]: txt_only card — no ready_canvas, no goals, not terminal, no # unlocks: comment. Doc 56 R6."`
- `"canvas 'scene_franks_bedroom_evening': priority 9 + is_repeatable=true requires self-gate flag_is_false condition. Doc 57 R1."`
- `"chain (npc='npc_ryan'): card 'R2' requires flag 'ryan_partner_open is_true' but no canvas sets this flag. Doc 50 R4."`

---

## §6 — Tests

In `apps/projects/tests.py` (or test file co-located with `_validate_quests_cards`):

### Positive cases (current TLS slice, post-2026-05-25 fixes)

1. **R1 — Frank capstones all referenced.** `scene_livingroom_catch` → F1 card; `scene_franks_bedroom_evening` → F2 card; etc. All clean.
2. **R3 — terminal placement clean.** R3 + J3 terminal cards are last in their chains.
3. **R5 — no txt_only.** Post-2026-05-25 fixes, 0 violations.
4. **R6 — capstone fingerprints clean.** All 13 audited capstones pass.

### Negative cases (synthesized)

5. **R1 violation.** Test canvas with capstone fingerprint + no quest_card pointer + no off-panel comment → ERROR.
6. **R1 off-panel.** Test canvas with capstone fingerprint + no pointer BUT `# off-panel:` comment → PASS.
7. **R2 violation.** Card with `ready_canvas` pointing at a canvas with corruption ≥ 35 gate, card's `when` only checks stage = 2 → WARNING.
8. **R3 violation.** Card marked `terminal = true` but another card for same `npc_id` requires a flag set downstream → ERROR.
9. **R4 violation.** Card with `when` requiring `flag_X is_true` but no canvas sets `flag_X` → WARNING.
10. **R5 violation.** Card with no `ready_canvas`, no `goals`, not `terminal`, no `# unlocks:` comment → ERROR.
11. **R5 escape.** Card with `# unlocks:` comment within 5 lines → PASS.
12. **R6 violation.** Canvas with `priority = 9 + is_repeatable = true + no self-gate` → ERROR.
13. **R6 self-gate variant.** Canvas with `priority = 9 + is_repeatable = true + flag-is_false self-gate + flag-setting effect` → PASS.

---

## §7 — Engine work estimate

| Task | Estimated time |
|---|---:|
| Rule 1 implementation (extend `_validate_quests_cards` + canvas walk) | 1 hr |
| Rule 2 implementation (resolve ready_canvas + gate comparison) | 1 hr |
| Rule 3 implementation (terminal placement scan) | 30 min |
| Rule 4 implementation (flag-setter scan) | 1 hr |
| Rule 5 implementation (txt_only check + unlocks-comment grep) | 1 hr |
| Rule 6 implementation (`_validate_capstone_fingerprint`) | 1 hr |
| Off-panel + unlocks comment grep helpers | 30 min |
| Error message formatting + context conventions | 30 min |
| 13 test cases (positive + negative) | 3 hr |
| Documentation + inline comments | 30 min |
| Total | **~10 hours** |

Medium PRD. Each rule is ~1-2 hours including its test. The hard part is the comment-grep regex robustness — TOML comment parsing is finicky.

---

## §8 — Rollout strategy

**Phase 1 — Implement + ship as warnings only.** All rules emit warnings, not errors. Existing slice content with violations (if any post-2026-05-25) produces warnings without breaking builds. ~5 hours.

**Phase 2 — Validate current slice.** Run validator against TLS slice. Expect 0 violations post-this-session's-fixes. If any surface, fix them.

**Phase 3 — Promote to errors per §4 severity table.** After Phase 2 verification, promote ERROR-severity rules to error level. Builds fail on violations going forward. ~5 minutes.

**Phase 4 — Doc 65 (catalog UI) consumes validator output.** Future surface — list of canvases without quest-card-pointers is the "off-panel capstones" list that could surface to authors. Out of this PRD's scope.

---

## §9 — Out of scope (intentional)

- **Doc 50 R5 mechanic-tier comment grep ENFORCEMENT.** Doc 50 §6 says R5 is "partial validatable" — the unlocks comment IS validatable per Rule 5 above, but the comment's CONTENT (does it accurately describe what unlocks?) stays human-read.
- **Doc 50 R6 label voice.** "label" field voice (e.g., "Maya's corruption" not "core_traits.corruption") stays human-read per Doc 50 §6.
- **Doc 56 R1 (constant hub openings).** Possible to validate (count group blocks in canvas `nodes[0].blocks`) but Doc 56 §3 doesn't currently require it; defer to a future rule.
- **Doc 56 R2 (in-fiction T0/T1 endings).** Voice content, not validatable mechanically. Human-read only.
- **Doc 57 R2-R5** validation. R2 (Type B simplicity preference) is a judgment call — not validatable. R3 already covered as Rule 1 above. R4 already covered as Rule 4 above. R5 (schedule + location coherence) is human-read.
- **Pattern F sub-rules F1-F5 validation.** All human-read.
- **Doc 62 `guide` field PRESENCE validation.** Future rule once Doc 62 schema lands and backfill completes. Initially `guide` defaults to empty string with no enforcement.

---

## §10 — References

### Sibling and ancestor docs

- **Doc 24** — 3 Lanes (capstone fingerprint feeds Rule 6)
- **Doc 50** — Quest Card Shape Doctrine (R1, R2, R3, R4 source + §6 validator commit)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (R6 source — no txt_only)
- **Doc 57** — Capstone Doctrine (R1 source — capstone trigger fingerprint, amended for is_repeatable=true self-gate)
- **Doc 62** — Canvas guide field PRD (sibling engine PRD; future R7 validator extension when backfill completes)

### Live engine references (verified)

- `apps/projects/services/template_import.py:3733-3849` — `_validate_quests_cards()` (extension point)
- `apps/projects/services/template_import.py:810-827` — `QuestsCondition` dataclass
- `apps/projects/services/template_import.py:830-866` — `QuestsCard` dataclass
- `apps/projects/services/template_import.py:434-478` — `TemplateTrigger` (is_repeatable, priority)
- `apps/projects/services/template_import.py:868` — `_parse_quests_condition` helper
- `apps/projects/services/template_import.py:3770` — error message convention pattern

### Live TLS reference (used in tests)

- Post-2026-05-25 TLS slice — all rules pass (positive test fixtures)
- Pre-2026-05-25 TLS slice (if accessible via git) — R5 violations (Ryan R2/R3 + Jake J1/J2/J3) as negative test fixtures

### Cross-PRD coordination

- Doc 62 schema ships → Doc 63 can add `guide` presence as a future R7 rule
- Doc 64 sidebar PRD ships → no direct interaction; sidebar items are separate validation path
- Doc 65 catalog UI consumes validator output for "uncoverd capstones" surface (P3+)
