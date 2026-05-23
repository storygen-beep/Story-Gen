# 12 — Engine PRD 09: Hint System Completeness (As Built)

> **Shipped 2026-05-01.** This doc is the canonical as-built record for the PRD 09 batch. It mirrors the structure of `08_Engine_PRD_Phase2_Additions.md` §11.

## §0 Frame

### What triggered this batch

Playtest of the Long Summer Test Slice (10-day vertical) surfaced a class of player-facing failures that all traced back to the same root: **hint authoring couldn't keep up with the doctrine the game was trying to express.**

Specific incidents:

- **The Ryan stuck-state bug.** Player drove Ryan trust from 5 to 12 over five in-game days. Hint still read *"Ryan's in the yard with the belt sander. He could use a water. Make him notice me work."* — same words as Day 1. Player thought the engine was broken. Actual cause: stage 0→1 helper required `trust >= 10 AND group_settled_in == true`, and the hint mentioned only the trust-building action. Multi-gate AND helpers had no way to surface "you cleared one, here's the other."

- **The hallucinated water mechanic.** "He could use a water" implied a bring-water interaction that doesn't exist. The author wrote a vibe; the engine had no way to flag that the vibe didn't map to a canvas.

- **The Frank corruption hallucination.** Hint said *"Auto-fires when corruption ≥ 25"*; actual scene_living_room_evening trigger required `corruption >= 45`. Player pushed corruption to 26, expected something to fire, nothing did. 20-point gap, undetected for a week.

- **Backbone hints silently dropped.** Rent / hygiene / energy templates had no `npc_id` and were filtered out of `setup.getStageHintForNPC` at v1.py:4517. They never rendered. Author thought they were live.

- **No counter visibility.** Hints said *"need ×3 bookkeeping sessions"* but `frank_bookkeeping_count` lived in `core_traits` with no sidebar surface. Player had no way to track progress.

- **Silent decay.** Trust decays 0.8/day (Ryan) or 1.0/day (Frank). Player drove Ryan to 14, skipped a day, came back to 13.2 — silently. Then their hint still said "need trust ≥ 15" and they had no idea why progress went BACKWARDS.

The PRD 08 doctrine (E1–E11) shipped a working stage-helper system but stopped short of player visibility into it. PRD 09 closes the visibility loop.

### What's covered

8 engine extensions, organized into 4 phases for ship discipline:

| Phase | Items | What it does |
|---|---|---|
| A | E23 | Build-time hint linter — catches drift before publish |
| B | E14, E22 | Schema extensions — `trait_checks` + cross-NPC prerequisite |
| C | E15, E17 | Engine render — global hints + cleared-but-not-triggered |
| D | E18, E20, E21 | Sidebar/UI — counter bars + decay warnings + opt-in cooldown |

E16 (visual split for hint text) shipped earlier in the same arc and is included here for completeness.

### What's not covered

Per user direction, deferred to future PRD batches:

- **E12** — Bracket-safe link emitter (separate concern, slice-side workaround already in place)
- **E13** — Reverse slug map determinism (shipped in earlier session, captured in memory)
- **E19** — Stage progress visualization (UX polish, no urgency)
- **E24** — Stage advancement toast (UX polish)
- **E25** — Hint completion markers (UX polish)
- **E26** — Dev mode hint debug overlay (author tool, not user-facing)
- **E27** — NPC section sorting (refinement)
- **E28** — Cross-stage preview (refinement)
- **E29** — Click-to-navigate (refinement)

---

## §1 Per-feature status

| ID | Description | Phase | Status | Notes |
|----|-------------|-------|--------|-------|
| E14 | `trait_checks` items in hint conditions | B | ✅ Shipped | Used by picker as a `condition_items` predicate; 1+ items contributes to specificity tiebreak |
| E15 | Global hints rendering ("Story Goals" section) | C | ✅ Shipped | Slice re-exposes rent / hygiene / energy; renders narrative + tip cards |
| E16 | Stage hint visual split (` — 🎯 ` separator) | (pre-batch) | 🗑 Removed | Goal block gone with Pattern 2 (§2.10 reverted); widget renders narrative + tip only |
| E17 | Cleared-but-not-triggered detection | C | ✅ Shipped | Synthesized hint passes through the simplified renderer |
| E18 | Counter sidebar items (auto-emitted) | D | ✅ Shipped | 4 bars auto-emit in slice (sidebar surface; unaffected by Quests revert) |
| E20 | Decay warnings (auto-emitted) | D | ✅ Shipped | Snapshot-vs-current; amber banner (sidebar surface) |
| E21 | Cooldown opt-in (`show_when_blocked`) | D | ✅ Shipped | No slice demo |
| E22 | Cross-NPC prerequisite reference | B | ✅ Shipped | No slice demo today (Diana arc deferred); now drives narrative variants per §2.12 picker |
| E23 | Build-time hint linter | A | ✅ Shipped | Pattern 2 rules removed; new picker-tie rule added (§2.12) |
| §2.10 | Pattern 2 — auto-rendered 🎯 goal block | — | 🗑 Reverted 2026-05-01 | Preserved in commit 28b8f6e; replaced by narrative variants |
| §2.11 | Pattern 3 — per-NPC activity list | — | 🗑 Reverted 2026-05-01 | Preserved in commit 28b8f6e; replaced by narrative variants |
| §2.12 | Narrative-priority picker | — | ✅ Shipped 2026-05-01 | Replaces Pattern 2/3 — `priority` field + specificity tiebreak |
| §2.13 | Tips page (game-level mechanics surface) | — | ✅ Shipped 2026-05-01 | Replaces per-template `tip` field; opt-in `[ui.tips_page]` + sidebar button + Quests rename |

---

## §2 Per-feature implementation notes

### §2.1 E23 — Hint linter (Phase A)

**Where:** `apps/projects/services/template_import.py` — new function `_lint_hint_templates(template)` invoked from `validate()` at the existing validation pass.

**Detection rules** (all warn-only — heuristic checks, not certain failures):

| Rule | Detection | Cross-check |
|---|---|---|
| Numeric threshold drift | `(trust\|corruption\|beauty\|...)\s*[≥>=]+\s*(\d+)` | matching `[[engine.stage_helpers]]` for next stage |
| Counter drift | `×(\d+)\s*(sessions\|times)` or `(\d+)\+\s*times` | matching helper's counter trait threshold |
| Time band drift | `(\d{2}:\d{2})[–\-](\d{2}:\d{2})` | matching canvas's `[[trigger.schedules]]` |
| Unknown location | `\(([A-Z][\w\s']+),\s*\d{2}:\d{2}` | exists in `[[locations]]` `name` field |
| Internal name leak | `\b\w+_(count\|done\|today\|open\|...)\b` | flag if outside whitelist |
| ✓-as-bullet | `\w+\s+✓(?!\s*\(already)` | character ban |
| Missing `npc_id` (silently dropped) | template has neither `npc_id` nor `stage_npc` | warns about engine drop, points at E15 |
| Gate count mismatch | helper has N AND-gates; hint mentions <N | counts "BOTH"/"ALL of"/"•"/" + " markers |

**How it links hint → helper:** templates with `condition.stage_npc = "npc_X"` and `stage_value = N` are checked against helper named `X_stage_<N+1>` (the helper that gates the NEXT advancement — what the player is racing toward).

**Output:** prints to build console alongside existing warnings:
```
⚠️  HINT LINTER FAIL story_arc.hints.templates[0]: hint says 'corruption ≥ 25' but
   helper 'frank_stage_2' requires 'corruption >= 45'. Update hint to match helper.
```

**Severity:** all findings emit as Python `UserWarning` (caught by `package_from_toml` and surfaced as `⚠️` lines). Never blocks the build — these are heuristics that can have false positives.

**Known false positives in current TLS slice:**
1. **Frank Stage 1 hint** — gate-count mismatch flag because Frank 1→2 is a "branch-inside-shell" transition (gate is on `scene_living_room_evening` trigger, not the helper). Hint is correct; linter doesn't know about branch-inside-shell.
2. **Jake Stage 0 hint** — `beauty ≥ 40` flagged against helper `beauty >= 50`. Hint is correct because helper is OR-logic (`beauty ≥ 50 OR jake_first_glance_noticed`), and the flag-setter path needs only beauty 40. Linter doesn't understand OR-logic alternate paths.

Both documented as future linter refinements — not blockers.

**Linter v2 (2026-05-01) — 5 additional rules added** in the same `_lint_hint_templates` function. All warn-only. Brief catalog (full rule logic in source):

| Rule | Catches | Example |
|---|---|---|
| Tier abbreviation | `T0`, `T1`, `T2` | "T0 shift = $20" → `T0/T1` are author shorthand |
| Money-claim cross-check | `$N` not in any canvas's `money += N` payouts | "T0 shift = $20" but only payout is `+$45` |
| Fourth-wall / dev memo | "NOT REACHABLE", "dev shortcut", "🔧", "slice testing", etc. | "use 🔧 dev shortcut to test" |
| Stage-arrow framing | `Stage N→M`, `advances Stage N` | "Stage 2→3 needs ALL of:" — engine-jargon |
| Author scene tags | "the X flag", "the catch fires", "the reveal", "first-glance moment", "doorway confrontation" | "the partner-invitation flag" |

Each rule is a self-contained regex/keyword block following the v1 pattern. The full guide-style writeup (when to suppress, idiomatic rephrasings) is deferred until after Pattern 2 (computed 🎯 line) is decided — many of these rules become moot once the engine generates the goal line itself.

### §2.2 E14 — `trait_checks` schema (Phase B)

**Where:** `apps/projects/services/template_import.py`

**Dataclass** addition to `TemplateHintCondition`:
```python
trait_checks: List[Dict[str, Any]] = field(default_factory=list)
```

**TOML usage** (single-line, due to TOML inline-table constraint):
```toml
condition = { stage_npc = "npc_frank", stage_op = "eq", stage_value = 0, trait_checks = [ { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "trust", operator = "gte", value = 15 }, { type = "trait", subject = "player", trait_key = "frank_bookkeeping_count", operator = "lt", value = 3 } ] }
```

**Loader:** parses `trait_checks` as a list of dicts, no shape enforcement at parse time (validator runs after).

**Serializer:** appends each item verbatim into the runtime `condition_items` array. Engine evaluator (`setup.checkSingleCondition` at v1.py:4636) already handles trait/flag items — **zero JS change needed**.

**Validator:** checks each item has `type` (trait/flag), `subject` (player/npc), valid `operator`, `trait_key` for traits / `flag_key` for flags. NPC subject must reference real NPC.

**Slice usage:** Frank Stage 0 baseline replaced with three ordered templates:
- **Transitional A** — stage 0 + `npc_frank.trust >= 15` + `frank_bookkeeping_count < 3` → *"He's looser at the table now. Now finish the bookkeeping sessions..."*
- **Transitional B** — stage 0 + `frank_bookkeeping_count >= 3` + `npc_frank.trust < 15` → *"The numbers add up; he doesn't yet. Now grind trust to 15..."*
- **Baseline** — stage 0 (no extra) → original "need BOTH" hint

Verified in compiled HTML: Transitional A emits 3 stacked condition_items.

### §2.3 E22 — `prerequisite_npc_stage` (Phase B)

**Where:** `apps/projects/services/template_import.py`

**Dataclass** addition to `TemplateHintCondition`:
```python
prerequisite_npc_stage: Optional[str] = None
```

**TOML format:** `"npc_<slug> <op> <int>"` — e.g., `"npc_frank >= 2"`.

**Parser:** new helper `_parse_prerequisite_npc_stage(spec)` returns `(npc_slug, op, value)` or `None`. Op map: `>=`→`gte`, `<=`→`lte`, `==`/`=`→`eq`, etc.

**Serializer:** parses the string and appends a trait condition_item on `<other_npc>_stage` to `condition_items`.

**Validator:** confirms (a) syntax parses, (b) referenced NPC exists, (c) NPC has `arc_stages`, (d) value in range.

**Slice usage:** none. Current TLS slice has no cross-NPC arc dependencies (e.g., Diana's arc was deferred per game_design plan). Schema is wired and ready for any future game that needs it.

### §2.4 E15 — Global hints rendering (Phase C)

**Where:** `apps/game_generation/twee_comprehensive/generators/v1.py`

**New walker:** `setup.getGlobalHints()` — mirrors `getStageHintForNPC` but walks templates with `!tpl.npc_id` and returns ALL matches (not just first — global goals can stack).

**New section in `:: QuestsPage`:** inserted before the per-NPC loop:
```sugarcube
<<set _globals = setup.getGlobalHints()>>
<<if _globals.length > 0>>
  <div class="npc-section">
    <h3 class="npc-name">Story Goals</h3>
    <<for _g range _globals>>
      <<renderStageHint _g.text>>
    <</for>>
  </div>
<</if>>
```

**Slice usage:** rent / hygiene / energy templates re-added to `4_story_arc.toml` with the 🎯 format. All three confirmed in compiled output.

### §2.5 E17 — Cleared-but-not-triggered detection (Phase C)

**Where:** `apps/game_generation/twee_comprehensive/generators/v1.py`

**Modified:** `setup.getStageHintForNPC` now checks the **next-stage helper FIRST** before walking templates. Falls through to the regular template walk if no ready state.

**New helpers:**
- `setup._getReadyHintForNPC(npcSlug)` — looks up next-stage helper via convention `<bare>_stage_<N+1>` (where `bare = npcSlug.replace("npc_", "")`), evaluates via `setup.triggerConditionsSatisfied(helper.conditions)`, and synthesizes a hint when cleared.
- `setup._findHelperTransitionLocation(helperName)` — walks `setup.help_data.locationCanvases`, finds the canvas where the helper appears as a trigger condition (`type === "stage" && operator === "is_true"`), resolves location UUID → slug → display name via `_getLocUuidToSlug` + `setup.locations[slug].name`.

**Synthesized hint format:** *"All gates cleared. — 🎯 Visit Back Yard to seal the moment."* — uses the existing `<<renderStageHint>>` widget with the standard ` — 🎯 ` separator.

**Returns object shape:** `{ text, npc_id, isReadyHint: true }` — `isReadyHint` flag available for future styling differentiation if desired.

**Slice usage:** auto-applies to all 3 arc NPCs (Frank, Ryan, Jake) without slice changes. Test by setting trait values via dev console and opening Quests page.

### §2.6 E16 — Stage hint visual split

**Where:** `apps/game_generation/twee_comprehensive/generators/v1.py` — `<<renderStageHint>>` widget defined in `TimeWidgets` passage.

**Behavior:** splits hint text on ` — 🎯 ` separator into flavor (italic, dimmed) on top + goal (highlighted block) below. Falls back to single-line render when separator absent — backwards compatible with games that don't follow the convention.

**CSS:** `.stage-hint-card`, `.stage-hint-flavor`, `.stage-hint-goal`, `.stage-hint-target` (4 rules in QuestsPage stylesheet).

**Slice usage:** all 13 templates use the format. Browser-verified rendering: italic flavor + bold-green goal stack.

### §2.7 E18 — Counter sidebar (Phase D)

**Where:** `apps/game_generation/twee_comprehensive/generators/v1.py` — new method `_auto_emit_counter_sidebar_items()` called during `_load_project_data` before `sidebar_items_json` serialization.

**Logic:**
1. Walk every stage helper's `conditions.items`
2. Find trait references with `_count` or `_done` suffix on `subject="player"` with `operator="gte"`
3. Pick the **lowest** threshold per counter (most-immediate gate)
4. Skip if author already authored a sidebar item with the same `trait` field (manual override wins)
5. Append a `trait_bar` entry with humanized label and `show_when` to hide once counter exceeds max

**Reuses existing `trait_bar` widget** at v1.py:10808+ — no new render code needed.

**Slice usage:** 4 bars auto-emitted on game generation:
- `Frank bookkeeping: 0 / 3`
- `Frank chore: 0 / 3`
- `Frank tease: 0 / 3`
- `Ryan help: 0 / 5`

Once a counter exceeds its max (gate cleared), the `show_when` clause hides the bar — no clutter for completed gates.

### §2.8 E20 — Decay warnings (Phase D)

**Where:** `apps/game_generation/twee_comprehensive/generators/v1.py`

**Three pieces:**

1. **Auto-emit at generation:** `_auto_emit_decay_warning_sidebar_items()` emits a single `trait_decay_warning` sidebar item if any decaying traits are configured. The item carries a `thresholds` map (synthetic-key → list of helper threshold entries) so render-time logic can find "next gate above current value."

2. **Snapshot in `advanceDay`:** new IIFE `_snapshotDecayingTraits()` runs **before** decay applies. Captures all decaying player + NPC trait values into `State.variables.last_day_snapshot` keyed as `player::<trait>` or `npc:<uuid>:<trait>`.

3. **Render-time evaluator:** `setup.getDecayWarnings(thresholds)` walks the threshold map, compares snapshot vs current, and returns warning objects when:
   - Snapshot exists AND current < snapshot (trait dropped today)
   - Next gate exists above current (player still racing toward something)
   - Within 2.0 of next gate (close enough to matter)

**Render shape:** *"⚠ Ryan trust dropping (12.4 today, was 13.2 yesterday). Next gate at 15 — interact today or lose more."*

**CSS:** `.trait-decay-warning-item` (amber banner with left border).

### §2.9 E21 — Cooldown opt-in (Phase D)

**Where:** `apps/projects/services/template_import.py` (schema) + `apps/game_generation/twee_comprehensive/generators/v1.py` (render).

**Schema additions** to `TemplateTrigger` dataclass:
```python
show_when_blocked: bool = False
cooldown_message: Optional[str] = None
```

Loader parses both. Canvas trigger metadata propagates the fields. `help_data.locationCanvases[].showWhenBlocked` and `.cooldownMessage` exposed at runtime.

**Render:** `setup.renderSoloActivities` extended with `soloCooldownBlocked` collection. When `setup.isCanvasValid(c)` returns false, if `c.showWhenBlocked === true`, the canvas is added to the blocked list and rendered as a non-clickable dimmed entry: *"Help Ryan with the work — Available again tomorrow"*.

**CSS:** `.solo-activity-cooldown` (dimmed text, italic message, no underline).

**Default:** off (silent filter — preserves existing game behavior). Author opts in per-canvas.

**Slice usage:** none. Current TLS slice has no daily-cooldown solo activities (Help Ryan, Diner shift, etc. are all NPC-tagged and accessed via portrait click — different render path). Schema is wired for any future game with daily-cooldown solo mechanics (shower-once-a-day, gym-once-a-day, etc.).

### §2.10 Pattern 2 — Computed 🎯 goal block (Option D) — **REVERTED 2026-05-01**

> **Status:** Shipped 2026-05-01, reverted same day after a usability review. Code preserved in commit **28b8f6e** for future reference. The auto-rendered 🎯 block was structurally elegant — author writes narrative, engine computes mechanics — but in playtest it added cognitive weight without adding information the player didn't already get from the narrative. The team's stated belief was *"the more we show, the more complex it gets and the more the player gets confused"*, and the goal block was the most visually heavy thing on the Quests card. Cross-state pressure that Pattern 2 hoped to convey via gate progress ("◯ trust 14/15") is now conveyed by **narrative variants** instead — a separate template gated on the urgency state, picked automatically by the new priority/specificity picker (§2.12). See `apps/game_generation/twee_comprehensive/generators/v1.py` Quests card path: only narrative + 💡 tip render. The historical design notes below are kept for context.
>
> *— Original spec follows —*

**Shipped 2026-05-01.** The biggest payoff in the PRD 09 batch family — and the architectural answer to the recurring drift / leak / transitional-proliferation bugs that the linter rules (E23 + linter v2) only *detected*.

**Problem this solves:** Every `text` field in a hint template was a hardcoded single-line string combining narrative flavor + structured goal data ("Frank trust ≥ 15", "Bookkeeping ×3", "Frank's Office, 19:00–21:30 weekdays"). Three classes of bug followed: (1) numbers/locations/time bands drifting from their helpers (`beauty ≥ 40` vs `>= 50` Jake bug; `T0 shift = $20` vs actual `$45` rent bug); (2) internal flag/counter names + engine-jargon leaking into player UI (`group_settled_in`, `tease count`, `T0/T1`, `Stage 1→2`, `🔧 dev shortcut`); (3) Frank Stage 0 needing 3 separate templates (Transitional A / B / Baseline) just to highlight which gate was unmet.

**The fix:** Author writes only the narrative flavor line + an optional `tip`. Engine pulls helper conditions, looks each gate's trait/flag key up in two new label registries, evaluates against current state, and renders the 🎯 block as a bulleted progress card with ✓/◯ markers and live `current/target` numbers.

**Schema additions** (`apps/projects/services/template_import.py`):
```python
@dataclass
class TemplateTraitLabel:
    key: str          # internal trait name, e.g. "frank_bookkeeping_count"
    label: str        # player-facing, e.g. "Bookkeeping"
    verb: str = "reach"
    unit: str = ""    # optional, for counter pluralization

@dataclass
class TemplateFlagLabel:
    key: str
    label: str

# New optional fields on TemplateHintTemplate:
tip: Optional[str] = None        # rendered as 💡 line below goal block
auto_goal: bool = True           # set false to opt out, use legacy text path
```

Loaders mirror the `[[engine.stage_helpers]]` pattern — `[[traits.labels]]` and `[[flags.labels]]` are top-level TOML blocks. `_serialize_hint_template` adds `tip` + `auto_goal` to the runtime payload. `create_project_from_template` writes `trait_labels` + `flag_labels` dicts to `project.metadata`.

**Engine renderer** (`apps/game_generation/twee_comprehensive/generators/v1.py`):

- **Python side:** `_build_stage_setter_canvases_index` (~50 lines) scans every `story_canvas`'s exit_block effects (both `choice.effects` typed objects and `config.effects` raw dicts) for `<npc>_stage = N` setters. Result: `{npc_slug: {stage_value: canvas_id}}`. Used as fallback for branch-inside-shell transitions where no helper exists (Frank 1→2 fires inside `scene_living_room_evening` choices).
- **Runtime data shipped:** `setup.trait_labels`, `setup.flag_labels`, `setup.stage_setter_canvases`.
- **`setup.computeHintGoal(hintObj)` (~80 lines)** — main entry. Returns HTML string for the structured goal block, or `""` if hint doesn't qualify (no stage condition / `auto_goal === false` / no helper or canvas-setter found).
- **6 sub-functions (~100 lines)**: `_currentTraitValue`, `_labelForTrait`, `_labelForFlag`, `_renderGoalGate`, `_renderGoalPath` (OR-logic branches), `_findStageSetterCanvas`, `_formatCanvasSchedule`, `_locNameFromUuid`.
- **`<<renderStageHint>>` widget extended** to accept either a string (legacy callers) OR a hint object. When passed an object with `auto_goal !== false` and a stage condition, calls `computeHintGoal` and renders the structured block + tip. Falls back to legacy `" — 🎯 "` split for global hints (rent / hygiene / energy) and synthesized "ready" hints (E17).
- **Three caller sites updated** (`:: QuestsPage` global loop + per-NPC + sidebar) to pass the full hint object.

**OR-logic case** (Jake Stage 1: `beauty >= 50 OR jake_first_glance_noticed`): renderer detects `helper.conditions.logic === "OR"`, emits `"Two paths to advance:"` header with each branch as a sub-block (`Path A` / `Path B`).

**Branch-inside-shell case** (Frank Stage 1→2: `scene_living_room_evening` writes `npc_frank_stage = 2` in choice effects, no helper exists): renderer falls back to `setup._findStageSetterCanvas` which uses the precomputed `stage_setter_canvases` index → reads the canvas's trigger conditions + schedule + location, renders bullets from those.

**Transitional collapse:** Frank Stage 0 had 3 templates pre-Pattern 2 (Transitional A / B / Baseline with `trait_checks` discriminators). Under Pattern 2, the auto-rendered ✓/◯ marks make the discriminator templates redundant — a single baseline template covers all gate states. Author decision (2026-05-01): drop transitionals A/B entirely; the bullet block conveys gate state better than a narrative shift.

**CSS:** ~70 lines added alongside existing `.stage-hint-card` block. New classes: `.stage-hint-goal-header`, `.stage-hint-goal ul/li`, `.stage-hint-met` / `.stage-hint-unmet` (✓/◯ markers), `.stage-hint-met-row` / `.stage-hint-unmet-row` (text color), `.stage-hint-progress` (mono `14/15`), `.stage-hint-where` (📍 line), `.stage-hint-tip` (💡 amber-bordered card), `.stage-hint-path` (OR-branch container).

**Author-facing label registries** for the slice (`1_metadata_and_locations.toml`): 9 trait labels (`frank_bookkeeping_count` → "Bookkeeping", `corruption` → "Corruption", `trust` → "trust", etc.) + 7 flag labels (`group_settled_in` → "Settled into the household", `frank_caught` → "Frank caught you", etc.). Renderer auto-prepends NPC display name when subject is `npc` (e.g., `"Frank trust 14/15"`).

**Slice migration:** 14 templates → 12 (Frank Stage 0 collapsed 3→1). Every `text` field stripped of the `" — 🎯 "` portion. Strategic advice moved to `tip =`. Two templates (Ryan Stage 2, Jake Stage 2) marked `auto_goal = false` — they're "out of scope for slice" placeholders that don't need a goal block.

**Linter additions** (paired with Pattern 2):
- New rule: warn when `auto_goal = true` (default) AND `condition.stage_npc/stage_value` set AND `text` contains `" — 🎯 "` — manual goal will be stripped at render.
- New post-template scan: warn when a helper-referenced trait/flag has no `[[traits.labels]]` / `[[flags.labels]]` entry. Cosmetic — the auto-render falls back to the raw key if no label.

**Backwards compatibility:**
- Legacy hints with `" — 🎯 "` in `text` and no stage condition (e.g., backbone rent/hygiene/energy): widget falls through to legacy split path. Works as today.
- Hints with `auto_goal = false`: opt-out, legacy split path.
- Games with no `[[traits.labels]]` / `[[flags.labels]]` registries: `setup.trait_labels` / `setup.flag_labels` are empty objects; renderer falls back to printing raw keys (ugly but functional). Linter warns to add labels.
- All 119 existing tests + 8 new Pattern 2 tests pass.

**Verification:** Slice rebuild produces `🎉 Package ready!`. Linter warnings on the slice dropped from 17 to 9 (the 9 remaining are pre-Pattern-2 false positives — gate-enumeration rule fires because the engine now does the enumeration in the rendered block, not in the narrative line; missing-npc_id rule fires on global hints which work fine via E15).

**Files modified for Pattern 2:**

| File | Change |
|---|---|
| `apps/projects/services/template_import.py` | 2 new dataclasses (`TemplateTraitLabel`, `TemplateFlagLabel`); 2 new fields on `GameTemplate`; 2 new fields on `TemplateHintTemplate` (`tip`, `auto_goal`); loaders for `[[traits.labels]]`/`[[flags.labels]]`; serializer extension; validator for label registries; runtime metadata writer; 2 new linter rules |
| `apps/game_generation/twee_comprehensive/generators/v1.py` | `_build_stage_setter_canvases_index` Python method; 3 new runtime dicts shipped; `setup.computeHintGoal` + 8 helper sub-functions; `<<renderStageHint>>` widget rewrite; 3 caller-site updates; ~70 lines CSS |
| `games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml` | 9 `[[traits.labels]]` + 7 `[[flags.labels]]` blocks |
| `games/the_long_summer_test/toml_phases/4_story_arc.toml` | All 14 templates rewritten — narrative-only `text` + `tip`; Frank Stage 0 collapsed 3→1 |
| `games/the_long_summer_test/toml_phases/7_final_game.toml` | Mirrored migration of both above |
| `apps/projects/tests.py` | 8 new tests for label loader + serializer + runtime metadata |

**What's deliberately deferred:**
- `11_Hint_Authoring_Guide.md` comprehensive rewrite — this doc + a one-line pointer in the linter section is enough to teach the new pattern; the guide gets a single batch update later
- Migration of other games (TLS main game) to Pattern 2 — they keep working with legacy `" — 🎯 "` rendering; ~30 min per game when the team gets to it
- Structured `goals` field for global hints (rent/hygiene/energy) — partially solved by Pattern 3 §2.11 (engine auto-discovers contributing canvases); full goal-block computation for global hints still deferred
- Linter rule pruning — keep all v1 + v2 rules enabled; they still help on legacy hints and on the narrative line / `tip` of new hints

### §2.11 Pattern 3 — Activity-list panel under each Quest section — **REVERTED 2026-05-01**

> **Status:** Shipped 2026-05-01, reverted same day. Code preserved in commit **28b8f6e**. The story-goal branch was first to go (Fix A/B/D rollback), then the per-NPC branch followed. Reason: alongside the Pattern 2 goal block, the activity table made each Quests card a 4-row mechanical grid, which the team felt was player-confusing. With Pattern 2 also reverted, narrative + 💡 tip is the whole card; cross-state pressure becomes a narrative variant (§2.12 picker) rather than a structured row. The collapsed `<details>/<summary>` toggle we shipped just before the revert is also gone. The original spec is kept below for historical context.
>
> *— Original spec follows —*



**Shipped 2026-05-01.** Extension of Pattern 2 — closes the gap between "what stage am I racing toward" (Pattern 2's goal block) and "what should I do right now to get there" (Pattern 3's activity list).

**Problem this solves:** Pattern 2 told the player `🎯 To advance: ◯ Frank trust 11/15  ◯ Bookkeeping 0/3` — abstract gates with progress. The player still had to ask: *Where do I do bookkeeping? Is it open right now? What else affects Frank's trust?*. The answer lived in canvas data the engine could see but never showed. Pattern 3 surfaces that data as a per-NPC activity panel.

**The fix:** below each Quests-page card, render a list of every unlocked canvas tagged to that NPC, with name + when (weekdays + time band) + where (location) + effects (`+1 Frank trust, +$8`) + what stage(s) it gates (`→ gates Frank Stage 1`). Same treatment for the player section (solo activities — shower / sleep / nap) and Story Goals section (rent / hygiene / energy hints get the contributing activities).

**Schema:** none. Pattern 3 reads existing canvas + helper data — no TOML changes required.

**Python build-time indexes** (`v1.py:_build_activity_to_gates_index`, `v1.py:_build_goal_activities_index`):

- `activity_gates_index: {canvas_id: [{helper_name, npc_slug, stage_value}, ...]}` — for each canvas, scan effects (choices[].effects + config.effects); for each positive trait-add or flag-set, find matching helpers (matching on `(subject, npc_id, trait_key)` triple — Frank-trust effects don't cross-pollute Ryan-trust helpers). Helper name → npc_slug + stage_value via `<bare>_stage_<N>` regex.
- `goal_activities_index: {template_index: [canvas_id, ...]}` — for each global hint template (no `npc_id`), inspect `condition.missing_flag` → find canvases that set that flag; inspect `condition.missing_trait` → find canvases that positive-add that trait. Template index keys the result so the QuestsPage can look up by `_g.goalKey`.

Both indexes ship as `setup.activity_gates_index` and `setup.goal_activities_index`.

**Engine renderer** (5 new JS functions in setup namespace):

- `setup.computeActivityList(sourceType, sourceId)` — main entry. `sourceType` ∈ `{"npc", "player", "goal"}`. Returns array of activity-row objects: `{id, name, location, schedules: [{weekdays, time, isNow}], effects, gates, isNow}`. Filters out: locked activities (conditions not met) + completed one-shots (`linked_flag` set OR present in `visited_nodes`). Schedule check NOT applied — we show other-weekday activities too.
- `setup._formatActivitySchedules(canvas)` — extends Pattern 2's `_formatCanvasSchedule` to handle multi-window canvases. Returns array of `{weekdays, time, isNow}` rather than single string. Computes `isNow` by reading current `time_state` and matching weekday + minute window.
- `setup._formatActivityEffect(effect)` — converts a TemplateChoiceEffect (or raw flagEffect dict) to a player-readable string. Uses Pattern 2's `setup.trait_labels` + `setup.flag_labels`. NPC-subject effects get NPC name prepended (`+1 Frank trust`). `+$8` shorthand for money.
- `setup._formatActivityGates(canvasId)` — looks up `setup.activity_gates_index[canvasId]`, formats each as `"<NPC name> Stage <N>"`.
- `setup._renderActivityList(activities, headerLabel)` — emits HTML. Each row gets `.activity-row` (or `.activity-row-now` if any schedule window is currently active) with name + meta (location · schedule) + detail (effects · gates).

**QuestsPage rewrite:** the per-NPC `<<set _next = setup.getNextActivity(_npcId)>>` block was replaced. New flow:

```twee
<<for _npcId, _npcData range _helpData.npcs>>
  <div class="npc-section">
    <h3>...</h3>
    <<set _slug = setup.npcSlugForId(_npcId)>>
    <<if _slug>>
      <<set _hint = setup.getStageHintForNPC(_slug)>>
      <<if _hint>><<renderStageHint _hint>><</if>>
    <</if>>
    <<set _acts = setup.computeActivityList("npc", _npcId)>>
    <<if _acts.length > 0>>
      <<print setup._renderActivityList(_acts, _npcData.name)>>
    <</if>>
  </div>
<</for>>
```

Same shape applied to player section + Story Goals section. The 9 conditional branches `getNextActivity` produced (`isStageHint` / `isStartingCanvas` / `isPhoneActivity` / `traitConditionsNotMet` / `flagConditionsNotMet` / `daysConditionsNotMet` / `conditionsNotMet` / `isLocked` / completed) are gone — the activity list is the single answer. Locked or unfired activities just don't appear.

**`getNextActivity` itself stays in code** — sidebar's `getSidebarHint` (line ~5969) still calls it. Sidebar's compact "next thing per source" presentation makes sense in tight space; QuestsPage gets the full list.

**`getGlobalHints` extended:** each match now includes `goalKey: ti` (the template's index in the templates array) so QuestsPage can look up activities for the right global hint via `setup.goal_activities_index[_g.goalKey]`.

**CSS** (~80 lines, alongside Pattern 2's stage-hint styles): `.activity-list`, `.activity-list-header`, `.activity-row`, `.activity-row-now` (green left-border for currently-active windows), `.activity-name`, `.activity-now-badge` (green inline badge), `.activity-meta`, `.activity-where`, `.activity-when` (mono font for time bands), `.activity-detail`, `.activity-effects`, `.activity-gates` (accent color for "→ gates X").

**Subject/NPC matching subtlety in gates index:** initial implementation matched on `trait_key` only — produced a 27-canvas index where any canvas adding any-NPC's trust appeared to gate every NPC's stage. Fixed by matching on `(subject, npc_id, trait_key)` triple. Result: 19 canvases in slice index, each correctly tied only to relevant helpers (`morning_kitchen` adds Frank trust → gates frank_stage_1 only, NOT ryan_stage_1).

**Slice impact:** Diana / Marge / Cookie sections — pre-Pattern-3 showed only `✓ All activities completed!` because `getNextActivity` couldn't find a "next" item. Pattern 3 surfaces every unlocked canvas tagged to them (Diana's `activity_help_diana_kitchen`, Marge/Cookie's diner shifts, etc.). Story Goals section (rent/hygiene/energy) now shows the contributing canvases (diner shifts under rent, shower under hygiene, sleep under energy) auto-discovered from canvas effects.

**Files modified for Pattern 3:**

| File | Change |
|---|---|
| `apps/game_generation/twee_comprehensive/generators/v1.py` | 2 new Python methods (`_build_activity_to_gates_index`, `_build_goal_activities_index`) ~250 lines; 2 new runtime dicts shipped (`setup.activity_gates_index`, `setup.goal_activities_index`); 5 new JS functions (`computeActivityList` + 4 helpers) ~280 lines; QuestsPage rewrite ~50 lines net (replaces ~100 lines of `getNextActivity` branching); ~80 lines CSS; `getGlobalHints` extended with `goalKey` field |
| `apps/projects/tests.py` | 5 new tests for index shipping + QuestsPage call sites; 2 existing tests updated (`test_quests_page_renders_stage_hint_directly`, `test_template_normalized_to_condition_items`) to reflect direct `setup.getStageHintForNPC` calls |

**Backwards compatibility:**
- `getNextActivity` function preserved — sidebar (`getSidebarHint`) still uses it
- Other games (TLS main, etc.) keep working — the new QuestsPage flow uses canvas data they already have
- Games without label registries (Pattern 2) still get readable activity rows — fallback to raw trait keys
- 124 existing tests + 5 new pass

**Verification:** Slice rebuild → `🎉 Package ready!`. `setup.activity_gates_index` has 19 canvases, each tied only to relevant NPC helpers. `setup.goal_activities_index` has 2 entries (template indices 9, 11) for the global hints with discoverable contributing activities. CSS classes + JS functions + `goalKey: ti` field all present in compiled HTML.

**What's deliberately out of scope:**
- Sidebar (TimeWidgets) — keeps using `getNextActivity` / `getSidebarHint`
- Per-activity sub-grouping ("Available now" / "Today" / "Tomorrow") — single list with weekday inline + green badge for currently-active. Easy to add later if playtest wants it.
- Tip-text linter rule (warn when tip duplicates auto-rendered effect data) — Q1 follow-up; activity list eliminates the main drift case for tip text, so this is lower priority now.

**Story-goal activity branch reverted (2026-05-01):** the goal-source activity list (rent / hygiene / energy under Story Goals) plus Fix A (op="set" trait_increasers), Fix B (`missing_flag` → costs+conditions tracing), and Fix D (`.story-goal-card` wrapper) were removed after a usability review. Hygiene → Shower and Energy → Sleep are single-activity lists where the canvas name duplicates the narrative line; Rent's seven-canvas money-earner list reads as a generic menu rather than focused guidance. Story Goals now render as narrative + 💡 tip cards only — same pattern as a Pattern-2 hint with no goal block. Per-NPC activity lists (the meat of Pattern 3) are unchanged. Code removed: `_build_goal_activities_index` Python method + `setup.goal_activities_index` runtime ship, `goal` arm of `setup.computeActivityList`, `goalKey` field on `getGlobalHints` matches, `.story-goal-card` CSS, QuestsPage Story Goals activity render block. Per-NPC `activity_gates_index` still ships and powers Frank/Ryan/Jake activity rows exactly as before.
- Comprehensive `11_Hint_Authoring_Guide.md` rewrite — still deferred. This doc + Pattern 2 §2.10 + Pattern 3 §2.11 cover the as-built design.

### §2.12 Narrative-priority picker (replaces Pattern 2 / Pattern 3)

**Shipped 2026-05-01** as the replacement architecture after Pattern 2 + Pattern 3 were reverted. The picker now resolves competing hint templates per the rule:

```
sort by (priority desc, condition_items.length desc, file-order asc)
```

**Schema change** (`apps/projects/services/template_import.py`): `TemplateHintTemplate` gains `priority: int = 0`. Loader reads `priority = N` from TOML (negatives clamp silently to 0); serializer ships it under the `"priority"` key in the runtime template JSON. The `auto_goal` field + `TemplateTraitLabel` / `TemplateFlagLabel` dataclasses + label-loader block + `create_project_from_template` registry writes were all removed in the same commit (Pattern 2 cleanup).

**Picker logic** (`apps/game_generation/twee_comprehensive/generators/v1.py`):

- `setup.getStageHintForNPC(npcSlug)` collects every matching template into a `candidates` array, sorts by the comparator above, and returns the top entry as `{text, npc_id, condition}`. (The `tip` field was dropped on 2026-05-01 — see §2.13 for where game-level mechanics live now.)
- `setup.getGlobalHints()` does the same with one extra step: groups candidates by **goal-key** = `condition.missing_flag || condition.missing_trait || ("__idx_" + ti)` so unrelated globals (rent / hygiene / energy) keep their own competition spaces. Within each group it picks the top entry; across groups it preserves first-seen file order so the visible card sequence stays predictable.

**Linter** (`_lint_hint_templates`): warns when two per-NPC templates share the **same** `npc_id + stage_value + priority + condition_items.length`. That's an undecidable tie — file order would silently win, which is exactly the silent contract the priority/specificity rule is built to kill. Author bumps priority on the variant that should fire first or adds a distinguishing condition.

**Slice usage:** Frank Stage 0 ships two templates (rent-pressure variant + baseline). The variant uses `priority = 10` AND has `missing_flag = "first_rent_paid"` — both signals point the same direction. While rent's unpaid the variant fires; once paid, baseline takes over. Other NPC stages use one template each — add variants when the narrative actually shifts on state.

**`<<renderStageHint>>` widget** simplified to render only `{text}` — narrative line in a `.stage-hint-card`. No goal block, no activity list, no tip, no schedule/location rows. Universal mechanics live on the Tips page (§2.13).

**QuestsPage** simplified: Story Goals section iterates `getGlobalHints()` and renders each as `<<renderStageHint>>`; per-NPC sections iterate help_data and render `<<renderStageHint setup.getStageHintForNPC(slug)>>`. The dedicated player section (shower/sleep/nap activity table) is gone — global hints (rent/hygiene/energy) cover those needs.

**Known limitation (carried over from PRD 03):** `missing_trait + gap_gte` doesn't normalize into `condition_items` (template_import.py:`_serialize_hint_template`), so global hygiene/energy templates all have 0 items — within their goal-key groups, priority is the only differentiator. Severe-state variants for those goals would need either a `priority` bump or a fix to the normalization path. Out of scope here.

**Files modified for §2.12:**

| File | Change |
|---|---|
| `apps/projects/services/template_import.py` | Drop `auto_goal` field + label dataclasses + label loader + Pattern 2 linter rules + project metadata writes; add `priority: int = 0` field + loader + serializer + tie-warning linter |
| `apps/game_generation/twee_comprehensive/generators/v1.py` | Drop `computeHintGoal` + helpers + `computeActivityList` + helpers + label registries + stage_setter_canvases + activity_gates_index + Pattern 2/3 CSS; rewrite `getStageHintForNPC` + `getGlobalHints` with priority/specificity sort + goal-key grouping; simplify `<<renderStageHint>>` widget to narrative + tip; simplify QuestsPage |
| `games/the_long_summer_test/toml_phases/4_story_arc.toml` + `7_final_game.toml` | Add Frank Stage 0 rent-pressure variant; strip `auto_goal = false` lines; rewrite header comment to describe picker rule |
| `games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml` + `7_final_game.toml` | Strip `[[traits.labels]]` + `[[flags.labels]]` blocks (no longer read) |
| `apps/projects/tests.py` | Remove Pattern 2/3 test classes; add `HintPriorityPickerTests` (5 tests covering field round-trip, picker shipping, goal-key dedupe, tie linter) |
| `28th_april_TLS_Phase2_Redesign/11_Hint_Authoring_Guide.md` | Mental model rewrite + new "Template ordering & narrative variants" section |

**Backwards compatibility:**
- Existing templates without `priority` default to 0 — file order remains the de-facto behavior for single-template-per-stage cases (the common case today).
- Other games (TLS main, etc.) keep working — they already had no Pattern 2/3 surface to lose.
- 122 tests pass (was 122; net change after removing 12 Pattern 2/3 tests + adding 5 picker tests).

### §2.13 Tips page (game-level mechanics surface)

**Shipped 2026-05-01** as the home for universal game mechanics, replacing the per-template `tip` field that was dropped the same day. Models RTS's Walkthrough page split — Quests journal stays pure narrative; mechanics (decay rates, time costs, what affects diner tips) live on a separate page authored once per game.

**Schema** (`apps/projects/services/template_import.py`):
```python
@dataclass
class TemplateTipsPage:
    title: str = "Tips"
    content: str = ""  # raw HTML, printed verbatim into :: TipsPage
```
New optional field on `GameTemplate`: `tips_page: Optional[TemplateTipsPage] = None`. Loader reads `data.get("ui", {}).get("tips_page")`; absent or content-empty → leaves `None` (graceful no-op). `create_project_from_template` writes `project.metadata["tips_page"] = {"title": ..., "content": ...}` when present.

**Runtime** (`apps/game_generation/twee_comprehensive/generators/v1.py`):
- `setup.tips_page = {json.dumps(self.tips_page or {})}` shipped alongside other setup objects.
- New `<<tipsButton>>` widget guards on `setup.tips_page && setup.tips_page.content` — body is empty otherwise. Invoked in StoryCaption right after `<<journalButton>>`.
- `<<journalButton>>` label renamed: "📖 Guide" → "📋 Quests" (the link always pointed at QuestsPage; old label was misleading).
- New `:: TipsPage` passage emits `<h2><<print _tp.title>></h2>` followed by a `<div class="npc-section">` card frame (same gradient + border treatment as QuestsPage cards) wrapping a `.tips-page-content` div with the author-supplied HTML. Content rendered as-is — pairs the Tips page visually with the Quests page so they read as the same family.
- `.tips-page-content` CSS — section `<h3>` headers mirror `.npc-name` from QuestsPage (border-bottom in `--theme-primary`, weight 600); `#tips-btn-widget` mirrors `#journal-btn-widget` (gradient `--journal-bg` → `--journal-bg-end` + journal-border) so Quests + Tips read as a paired sidebar cluster.
- `"TipsPage"` added to `info_pages_list` in the `InfoPageNav` script (built in `v1.py` near line 10535). Without this, the `:passagestart` handler overwrites `last_game_passage = "TipsPage"` whenever the page loads, and the back button loops on itself. Same trap every other info page (QuestsPage, StatsPage, SchedulePage, etc.) avoids by being in the same list.

**Slice usage:** `[ui.tips_page]` block in `1_metadata_and_locations.toml` + mirrored in `7_final_game.toml`. Seven `<h3>` sections: Time / Trust / Hygiene / Energy / Money / Corruption + Beauty / Reading the Quests page. Content consolidated from what used to be repeated as per-template `tip` text on every NPC card.

**Files modified for §2.13:**

| File | Change |
|---|---|
| `apps/projects/services/template_import.py` | Drop `tip` from `TemplateHintTemplate` + loader + serializer; add `TemplateTipsPage` dataclass + `tips_page` field on `GameTemplate` + loader + project metadata write |
| `apps/game_generation/twee_comprehensive/generators/v1.py` | Drop `tip` from picker return shapes + `<<renderStageHint>>` widget + `.stage-hint-tip` CSS; ship `setup.tips_page`; add `<<tipsButton>>` widget + invocations in StoryCaption; rename `<<journalButton>>` "📖 Guide" → "📋 Quests"; add `:: TipsPage` passage + `.tips-page-content` CSS |
| `games/the_long_summer_test/toml_phases/4_story_arc.toml` + `7_final_game.toml` | Drop all `tip = "..."` lines from 13 templates |
| `games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml` + `7_final_game.toml` | Add `[ui.tips_page]` block with 7 sections of consolidated game-level mechanics |
| `apps/projects/tests.py` | Drop tip assertions; add `TipsPageTests` (4 tests covering page emission, conditional widget, Quests rename) |
| `28th_april_TLS_Phase2_Redesign/11_Hint_Authoring_Guide.md` | Mental model rewrite (one piece, not two); new "Game-level mechanics: the Tips page" section |

**Backwards compatibility:**
- Games without `[ui.tips_page]` get no Tips button + no `:: TipsPage` passage rendered (graceful no-op).
- Quests button rename is unconditional — every game now reads "📋 Quests" instead of "📖 Guide".
- 132 tests pass (was 122; +4 new TipsPageTests, +5 already-shipped picker tests, +1 minor adjustment).

**Deliberately out of scope:**
- Markdown rendering — author writes raw HTML. Predictable formatting without a renderer.
- Per-NPC tips sub-blocks (`[ui.tips_page.npc_<slug>]`) — no consumer today.
- Linter rule for "did the author put game-mechanics-shaped text in `text`?" — too heuristic.

---

## §3 Test game audit (the_long_summer_test slice)

**Verified by reading slice TOML + grepping compiled output** (no hallucination):

| Feature | Used in slice? | How verified |
|---|---|---|
| E14 trait_checks | ✅ Yes | Frank Stage 0 transitionals A + B in `4_story_arc.toml` lines 35–47; compiled output shows 3 stacked condition_items per template |
| E15 global hints | ✅ Yes | Rent + hygiene + energy templates re-added to `4_story_arc.toml`; "Story Goals" section renders in QuestsPage |
| E16 visual split | ✅ Yes | All 13 templates use ` — 🎯 ` separator; widget renders 2-block layout |
| E17 cleared-but-not-triggered | Auto (engine) | No slice changes needed; engine wires for all 3 arc NPCs (Frank/Ryan/Jake) |
| E18 counter sidebar | Auto (engine) | 4 bars auto-emitted in compiled `setup.sidebar_items` JSON: Frank bookkeeping, Frank chore, Frank tease, Ryan help |
| E20 decay warnings | Auto (engine) | `trait_decay_warning` item emitted; snapshot logic confirmed in `advanceDay` |
| E21 cooldown opt-in | ❌ NOT used | No daily-cooldown solo activities to opt in. Schema available for future games. |
| E22 cross-NPC prereq | ❌ NOT used | No cross-NPC arc dependencies in current slice scope (Diana arc deferred per game design plan). Schema available. |
| E23 hint linter | Auto (build) | Runs at every `package_from_toml`; surfaces 2 known false positives (documented §2.1) |

**Net: 7 of 9 features actively demonstrated.** The 2 unused features (E21, E22) are because the slice's content scope doesn't have natural use cases — forcing demos would mean inventing fake mechanics. Better to leave the schema wired and ready, with example usage documented in this PRD.

---

## §4 Files modified

| File | Phases | LOC delta (approx) |
|---|---|---|
| `apps/projects/services/template_import.py` | A (linter) + B (E14/E22 schema) + D (E21 fields) | ~280 lines added |
| `apps/game_generation/twee_comprehensive/generators/v1.py` | C (E15/E17 render) + D (E18/E20/E21 sidebar+render) | ~310 lines added |
| `games/the_long_summer_test/toml_phases/4_story_arc.toml` | B (Frank transitionals) + C (backbone re-add) | ~30 lines added |
| `28th_april_TLS_Phase2_Redesign/11_Hint_Authoring_Guide.md` | post-batch — table flips + new sections | (see doc 11 for changes) |
| `28th_april_TLS_Phase2_Redesign/09_Future_Polish_Items.md` | post-batch — single subsection added | (see doc 09 for changes) |

No save-game shape changes. No tests deleted. Existing 111-test pytest suite passes throughout.

---

## §5 Verification

### Pytest

After every phase: `DJANGO_SETTINGS_MODULE=config.settings.testing pytest apps/projects/tests.py` → 111 passed.

### Slice rebuild

After every phase: concat phases → `package_from_toml --dev` → `🎉 Package ready!` with no validation errors. Linter warnings printed alongside (expected).

### Browser playtest checklist

Hard-refresh `games/the_long_summer_test/output/index.html` and verify:

**E15 — Story Goals section**
- Top of Quests/Guide page shows "Story Goals" section
- Rent hint visible on Day 1 (first_rent_paid is false)
- Hygiene/energy hints fire only when below threshold

**E16 — Visual split**
- Each NPC hint renders as italic flavor on top + green-tinted 🎯 goal block below
- 🎯 emoji is slightly larger than surrounding text
- Long goal text wraps cleanly within the card

**E17 — Cleared-but-not-triggered**
- Dev console: `State.variables.npcs[setup.npc_slug_map.npc_ryan].core_traits.trust = 12; State.variables.flags.group_settled_in = true;`
- Open Quests; Ryan section reads *"All gates cleared. — 🎯 Visit Back Yard to seal the moment."*

**E18 — Counter bars in sidebar**
- Right sidebar shows: Frank bookkeeping `0/3`, Frank chore `0/3`, Frank tease `0/3`, Ryan help `0/5`
- After doing a bookkeeping session, Frank bookkeeping bar fills to `1/3`
- After 3 sessions (gate cleared), bar disappears

**E20 — Decay warning**
- Dev console: `State.variables.npcs[setup.npc_slug_map.npc_ryan].core_traits.trust = 14`
- Sleep / advance one day (decay drops trust to 13.2)
- Sidebar shows amber banner: *"⚠ Ryan trust dropping (13.2 today, was 14.0 yesterday). Next gate at 15..."*

**E21 — Cooldown opt-in (no slice demo)**
- To test: edit any solo activity in TOML to add `show_when_blocked = true` + a daily flag condition. Use it once. Re-visit location. Expect grayed entry instead of disappearance.

**E22 — Cross-NPC prereq (no slice demo)**
- To test: add a hint with `prerequisite_npc_stage = "npc_frank >= 2"` to any NPC's templates. The hint will only fire once Frank reaches Stage 2.

**E23 — Hint linter (build-time, not browser)**
- Run `package_from_toml --dev`. Build console shows linter warnings inline with other ⚠️ output. False positives documented in §2.1.

---

## §6 Backwards compatibility

All schema additions are **optional fields with safe defaults** — existing games rebuild without changes:

- `TemplateHintCondition.trait_checks` defaults to `[]` (empty)
- `TemplateHintCondition.prerequisite_npc_stage` defaults to `None`
- `TemplateTrigger.show_when_blocked` defaults to `False`
- `TemplateTrigger.cooldown_message` defaults to `None`

Runtime State shape additions:
- `State.variables.last_day_snapshot` initialized to `{}` on first `advanceDay` after upgrade
- No save-game migration required

Engine functions added (`getGlobalHints`, `_getReadyHintForNPC`, `_findHelperTransitionLocation`, `getDecayWarnings`) — all new, no existing function signatures changed.

`getStageHintForNPC` modified to check ready-hint first, but **falls through** to existing template walk when no ready state — original behavior preserved for any state where ready check returns null.

**Tested:** TLS Phase 1 game (uses no PRD 09 schema fields) rebuilds unchanged.

---

## §7 Known limitations

### Linter (E23)
- **Branch-inside-shell transitions** not understood — when a stage transition fires from a scene's choice effects (not a helper), the linter's helper-comparison flags the hint as gate-count-mismatch even when the hint correctly references the scene's trigger gate
- **OR-logic helpers** not understood — when a helper has `logic="OR"` with multiple paths, the linter compares the hint against the first path only

Both produce false positive warnings (not failures). Future linter refinement can encode "branch-inside-shell" annotation on canvases and OR-aware helper traversal.

### E14 schema
- TOML inline tables (`condition = { ... }`) cannot span multiple lines per TOML 1.0 spec — `trait_checks` arrays must be authored on a single line, which gets long. Acceptable but ugly. Future ergonomics: standalone `[story_arc.hints.templates.condition]` tables that span lines naturally.

### E17 helper resolution
- Convention `<bare>_stage_<N+1>` is brittle — works for the TLS slice's naming but a game using non-conventional helper names won't get auto-detection. Future: explicit `[next_stage_helper = "..."]` field on templates.

### No live per-gate evaluation
- Hints are still string templates. The author writes them; the engine doesn't dynamically compose "trust 12/15, bookkeeping 1/3" inside the hint at render. E18 sidebar bars provide this visibility separately. A future enhancement could allow `{{trait:trust}}` placeholders inside hint text.

---

## §8 Cross-references

- **`08_Engine_PRD_Phase2_Additions.md`** — Phase 2 doctrine foundation (E1–E11 + arc_stages); this batch builds on it
- **`09_Future_Polish_Items.md`** — backlog of polish items; PRD 09 batch satisfies "hint system completeness" item; remaining items (StagesPage, NPC location sidebar, etc.) still pending
- **`10_Test_Slice_10Day_Plan.md`** — the test game design that surfaced the gaps this PRD closes
- **`11_Hint_Authoring_Guide.md`** — author-facing guide; updated post-batch to reflect shipped engine support and new conventions
- **Deferred future engine work:** E12 (bracket emitter), E19 (stage progress viz), E24 (advancement toast), E25 (completion markers), E26 (dev hint debug overlay), E27 (NPC sorting), E28 (cross-stage preview), E29 (click-to-navigate)

---

End of as-built record.
