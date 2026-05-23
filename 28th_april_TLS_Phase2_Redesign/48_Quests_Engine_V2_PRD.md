# 48 — Quests Engine V2 PRD

**Session date:** 2026-05-23
**Status:** PRD — ready for implementation planning
**Inherits from:** Doc 47 (Quests Page Unified Card Design — analysis)
**One-line summary:** Replace the five-path Quests rendering engine with a single-path engine driven by author-on-template `goals` arrays. Ship in `twee_comprehensive` behind a per-game opt-in flag (`quests_engine = "v2"`). TLS migrates; other games stay on the existing engine until they opt in.

---

## §1 Context

Doc 47 traced the current Quests engine end-to-end and concluded that the unified card design (one card shape, picker-swap as state-change signal, engine-rendered goal block) maps onto five accumulated rendering paths in `computeHintGoal` — `arc_closure_flag` set / unset / `arc_complete` / `auto_goal=false` suppression / helper-driven Path E — none of which were designed together. The accumulated indirection (stage helpers, transition canvases, label registries, closure-flag setter searches) exists because the design was discovered iteratively, not because the player-facing surface requires that complexity.

Adding the one missing piece (live progress bullets without a stage helper) to the current engine means adding a sixth path. This PRD chooses the cleanup instead: replace the engine with a single-path version that supports every card variant in doc 47 §6 directly. The new engine ships alongside the old; TLS opts in; other games stay on the old engine until ready.

The intended end state for TLS:

- Every arc NPC (Frank/Ryan/Jake) has a Quests card from Day 1 to arc terminal, swapping cards via the picker as state crosses.
- The bullet gap closes — pre-catch Frank shows `🎯 To advance + ◯ Maya's corruption — *X* / 25` instead of nothing.
- Stage helpers, stage integer variables, label registries, and the sidebar hint mechanism are deleted from TLS.
- The old engine remains untouched in `twee_comprehensive` for the other games that depend on it (`under_one_roof`, `two_weeks`, `new_in_town`).

---

## §2 Scope and goals

### In scope

- New SugarCube runtime code in `apps/game_generation/twee_comprehensive/generators/v2.py` implementing the V2 Quests engine (functions + widget + QuestsPage variant).
- Per-game opt-in flag (`quests_engine = "v2"`) in the project metadata block of TLS's TOML.
- New TOML schema (`[[quests.cards]]`) parsed by a new normalizer + validator + serializer in `apps/projects/services/template_import.py`.
- TLS migration: rewrite all 12 existing `[[story_arc.hints.templates]]` entries as `[[quests.cards]]`, author 6–8 new Frank pre-catch / post-catch / post-first-night / post-Diana cards, delete `[[engine.stage_helpers]]` + `[[traits.labels]]` + `[[flags.labels]]` + stage integer variables + sidebar `hint`-type entries.
- Test coverage at three layers: Python unit tests, SugarCube smoke game, TLS end-to-end manual walkthrough.

### Out of scope

- The sidebar hint mechanism is **removed entirely** from the V2 engine surface. `getSidebarHint`, `getNextActivity`'s sidebar-feeding role, `formatFlagHint`, `formatActivityHint`, `formatCanvasConditions`, and the `hint` type in `[[sidebar_items]]` are not implemented in V2. (They remain in the old engine for non-migrated games.)
- The old engine code in `v2.py` is **not touched**. All of `getStageHintForNPC`, `getGlobalHints`, `computeHintGoal`, `_isHintReady`, `_findFlagSetterCanvas`, `_findStageSetterCanvas`, `_renderGoalGate`, `_renderGoalPath`, `_labelForFlag`, `_labelForTrait`, the `renderStageHint` widget, the old QuestsPage variant — all stay as-is.
- Frontend / Next.js / React changes — none. This is a SugarCube-runtime + TOML-schema + Python-build-pipeline change.
- Migration tooling for other games. Their TOMLs stay as-is. They opt in by setting `quests_engine = "v2"` on their own schedule and converting their templates by hand (or via a future automated migration if needed).
- Engine V3 plans or further consolidation past the V2 design.

### Goals

1. **One rendering path.** The new `renderQuestsGoalBlock` has three exclusive frames (`✓ terminal`, `🔓 Ready+📍+🕒`, `🎯 bullets`). No suppression flags, no helper-vs-canvas fallbacks, no auto_goal switch.
2. **Author-on-template.** Each `[[quests.cards]]` entry carries everything the renderer needs: routing (`when`), narrative (`text` / `ready_text` / `tip`), progress (`goals` with labels), Ready target (`ready_canvas`), and terminal marker (`terminal`). No external lookups.
3. **Same schema for NPC arcs and Story Goals.** Distinction is purely presence/absence of `npc_id`.
4. **Coexistence with old engine.** Per-game flag selects which engine emits at build time. Both engines can ship in the same generator. Other games unaffected.
5. **All six player situations from doc 47 §6 expressible without special cases.**

### Non-goals

- No new player-facing UX. Same card visual shape, same Quests page layout.
- No performance optimization claims. Big-O is the same as the current engine (linear template scan).
- No backward-compat layer in V2. V2 reads only the new schema. Games that haven't migrated their TOML must stay on V1.

---

## §3 TOML schema (`[[quests.cards]]`)

### Field reference

| Field | Type | Required? | Semantics |
|---|---|---|---|
| `text` | string | yes | Maya-voice narrative line. Renders as `.quests-flavor` |
| `ready_text` | string | no | Replaces `text` when all `goals` evaluate to met. The "moment is on her" line |
| `tip` | string | no | Optional 💡 line below the goal block |
| `npc_id` | string | no | Present → card routes to that NPC's section. Absent → routes to "Story Goals" top section |
| `priority` | int | no (default `0`) | Higher wins picker tie. Used for crisis variants beating ambient lines |
| `group` | string | no | Story Goal only. Cards sharing a `group` value collapse to one (highest-priority match); cards without `group` are independent. Lets multiple crisis variants share a slot |
| `when` | array of condition items | yes | Routing conditions. ALL must match for this card to win the picker. Cannot be empty (use `[]` rejected by validator) |
| `goals` | array of condition items with `label` | no | The 🎯 bullets. If absent or empty → no bullets shown. If present → bullets render with live progress |
| `ready_canvas` | string (canvas slug) | no | When all `goals` are met (or `goals` is empty) AND this field is set, renderer shows 🔓 Ready + 📍 + 🕒 pulled from the named canvas's metadata |
| `terminal` | bool | no (default `false`) | If `true` AND all `when` match → renders ✓ Arc complete frame. Overrides goals/ready_canvas |

### Condition item shape

Used in both `when` (routing) and `goals` (bullets):

```toml
# Trait gate (player subject)
{ trait = "corruption", subject = "player", op = "gte", value = 25,
  label = "Maya's corruption" }

# Trait gate (NPC subject)
{ trait = "trust", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10,
  label = "Ryan trust" }

# Flag gate
{ flag = "frank_caught", op = "is_true" }

# Counter gate (counters live as traits today, same shape)
{ trait = "ryan_help_count", subject = "player", op = "gte", value = 3,
  label = "Yard help sessions" }
```

Field requirements:
- Trait/counter items: `trait` (key), `subject` (`"player"` or `"npc"`), `op` (`"gte"` / `"lte"` / `"eq"` / `"gt"` / `"lt"`), `value` (number). When `subject = "npc"`, also requires `npc_id`. `label` required when item appears in `goals`, ignored in `when`.
- Flag items: `flag` (key), `op` (`"is_true"` / `"is_false"`). `label` optional in `goals` (default to flag key if absent — but bullets render badly without one, so validator warns).
- Future: `days_since_flag` shape if needed. Not in V2 initial release.

### Card-shape coverage (cross-reference doc 47 §6)

| Doc 47 situation | Card pattern |
|---|---|
| 1. Climbing toward capstone | `when` = routing flags, `goals` = trait bullets, `ready_canvas` = capstone scene |
| 2. Capstone gates met | Same card as 1. `goalState.allMet` flips → ready_text + Ready frame |
| 3. Capstone fired, arc terminal | `terminal = true`, `when` = post-capstone flag is_true |
| 4. Pure-mechanic climbing | `when` = routing, `goals` = trait bullets, **no `ready_canvas`** |
| 5. Pure-mechanic tier just crossed | New template with `when` matching the new state. Picker swaps automatically |
| 6. Capstone fired → mechanic next | Card with `goals` for next mechanic threshold, no `ready_canvas` |

### Worked authoring examples

**Frank pre-catch climbing (situation 1):**

```toml
[[quests.cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25,
    label = "Maya's corruption" },
]
ready_canvas = "scene_livingroom_catch"
```

**Frank post-cracked pre-first-night (situation 2 without bullets):**

```toml
[[quests.cards]]
text         = "Upstairs now. The office stays for the books."
ready_text   = "He'll be in his bedroom tonight."
tip          = "Diana down the hall. Quiet."
npc_id       = "npc_frank"
when = [
  { flag = "frank_cracked",            op = "is_true" },
  { flag = "frank_bedroom_first_done", op = "is_false" },
]
ready_canvas = "scene_franks_bedroom_evening"
```

**Ryan pure-mechanic climbing (situation 4):**

```toml
[[quests.cards]]
text       = "Ryan's out in the yard most days. Maybe I should help him."
ready_text = "Ryan treats me like family now."
npc_id     = "npc_ryan"
when = [
  { trait = "trust", subject = "npc", npc_id = "npc_ryan", op = "lt", value = 10 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10,
    label = "Ryan trust" },
]
```

**Story Goal — rent:**

```toml
[[quests.cards]]
text  = "Rent's coming due and I've got next to nothing. No money, no roof — I need work, fast."
tip   = "Odd jobs, anyone who'll pay — start asking around."
group = "rent"
when = [
  { flag = "first_rent_paid", op = "is_false" },
]
```

**Frank arc terminal (situation 3):**

```toml
[[quests.cards]]
text     = "He moved the line. The bedroom is the venue now."
tip      = "Diana down the hall. Quiet."
npc_id   = "npc_frank"
priority = 1
when = [
  { flag = "frank_bedroom_first_done", op = "is_true" },
]
terminal = true
```

### Schema constraints (validator enforces)

1. `text` is non-empty.
2. `when` is non-empty (every card must have at least one routing condition; "always show" cards are deliberate authoring choices, not the default).
3. Every item in `goals` that targets a trait/counter has a non-empty `label`.
4. `ready_canvas`, when present, references an existing canvas slug in the game.
5. `terminal = true` AND `ready_canvas` present → validator warns (terminal overrides ready_canvas; both shouldn't be set).
6. `npc_id`, when present, references an existing NPC slug.
7. `priority` must be an integer.
8. Condition items use the new flat shape (no `type`/`flag_key`/`trait_key`/`operator` fields — those belong to the old schema).
9. `group` is only meaningful on Story Goal cards (no `npc_id`); validator warns if set on NPC cards.

---

## §4 Engine (SugarCube runtime)

Five functions + one widget + one passage. Total estimated surface: ~250 lines of JS.

### `setup.pickQuestsCard(npcSlug)` — NPC arc picker

```
function pickQuestsCard(npcSlug):
    cards = (setup.quests_cards || [])
    matches = []
    for each card in cards:
        if card.npc_id !== npcSlug: continue
        if not all(card.when): continue   # checkQuestsCondition on each item
        matches.push({ card, fileIndex: i })
    if matches empty: return null
    sort by (priority desc, when.length desc, fileIndex asc)
    return matches[0].card
```

### `setup.pickQuestsCards("story_goals")` — Story Goals picker

```
function pickQuestsCards():
    cards = (setup.quests_cards || [])
    matches = []
    for each card in cards:
        if card.npc_id is set: continue
        if not all(card.when): continue
        matches.push({ card, fileIndex: i })
    if matches empty: return []
    # Group by 'group' field (cards without group are unique singletons)
    groups = {}
    for each m in matches:
        key = m.card.group || ("__idx_" + m.fileIndex)
        groups[key].push(m)
    # Within each group, pick winner by sort order
    winners = []
    for each group:
        sort by (priority desc, when.length desc, fileIndex asc)
        winners.push(group[0])
    # Return in file order of the FIRST seen member of each group
    sort winners by fileIndex asc
    return winners.map(m => m.card)
```

### `setup.evaluateGoals(card)` — goal evaluator

```
function evaluateGoals(card):
    if not card.goals or card.goals.length === 0:
        return { allMet: true, items: [] }
    items = []
    allMet = true
    for each goal in card.goals:
        met = checkQuestsCondition(goal)
        current = readCurrentValue(goal)   # null for flags, number for traits
        items.push({ goal, currentValue: current, met })
        if not met: allMet = false
    return { allMet, items }
```

`readCurrentValue(goal)` extracts the live trait/counter value from `State.variables.player.core_traits` or `State.variables.npcs[uuid].core_traits` based on `subject` + `npc_id`. Returns `null` for flag goals.

### `setup.checkQuestsCondition(item)` — gate evaluator

```
function checkQuestsCondition(item):
    if item.flag is set:
        value = State.variables.flags[item.flag] === true
        if item.op === "is_true": return value
        if item.op === "is_false": return !value
        return false
    if item.trait is set:
        if item.subject === "player":
            current = State.variables.player.core_traits[item.trait] ?? 0
        else if item.subject === "npc":
            uuid = setup.npc_slug_map[item.npc_id] || item.npc_id
            current = State.variables.npcs[uuid].core_traits[item.trait] ?? 0
        else: return false
        return compare(current, item.op, item.value)
    return false
```

`compare(a, op, b)` is the standard `gte`/`lte`/`gt`/`lt`/`eq` numeric comparison.

### `setup.renderQuestsGoalBlock(card, goalState)` — one-path renderer

```
function renderQuestsGoalBlock(card, goalState):
    # Frame 1: ✓ Arc complete
    if card.terminal === true:
        return '<div class="quests-goal">
                  <div class="quests-goal-header quests-terminal">
                    <span>✓</span> Arc complete
                  </div>
                </div>'

    # Frame 2: 🔓 Ready
    if goalState.allMet and card.ready_canvas:
        found = lookupCanvasBySlug(card.ready_canvas)
        if not found: return ''   # silent fail; validator should have caught
        locName = _locNameFromUuid(found.locUuid)
        schedStr = _formatCanvasSchedule(found.canvas)
        html = '<div class="quests-goal">
                  <div class="quests-goal-header quests-ready">
                    <span>🔓</span> Ready
                  </div>'
        if locName: html += '<div class="quests-where">📍 ' + locName + '</div>'
        if schedStr: html += '<div class="quests-where">🕒 ' + schedStr + '</div>'
        html += '</div>'
        return html

    # Frame 3: 🎯 To advance
    if goalState.items.length > 0 and not goalState.allMet:
        html = '<div class="quests-goal">
                  <div class="quests-goal-header">
                    <span>🎯</span> To advance:
                  </div>
                  <ul>'
        for each item in goalState.items:
            marker = item.met ? '✓' : '◯'
            label = item.goal.label or fallbackLabel(item.goal)
            if item.goal.trait and typeof item.currentValue === 'number':
                label += ' — ' + item.currentValue + ' / ' + item.goal.value
            html += '<li>' + marker + ' ' + label + '</li>'
        html += '</ul></div>'
        return html

    # No frame (narrative text only — happens for cards whose only gates are
    # routing flags handled by `when`, not climbing toward a Ready target)
    return ''
```

### Widget — `<<renderQuestsCard>>`

```
<<widget "renderQuestsCard">>
<<set _card to $args[0]>>
<<set _goalState to setup.evaluateGoals(_card)>>
<<set _flavor to (_goalState.allMet && _card.ready_text) ? _card.ready_text : _card.text>>
<<set _goalBlock to setup.renderQuestsGoalBlock(_card, _goalState)>>
<div class="quests-card">
  <div class="quests-flavor"><<print _flavor>></div>
  <<if _goalBlock>><<print _goalBlock>><</if>>
  <<if _card.tip>><div class="quests-tip">💡 <<print _card.tip>></div><</if>>
</div>
<</widget>>
```

### QuestsPage passage

```
:: QuestsPage
<<nobr>>
<h2>What's Next</h2>

<<set _goals = setup.pickQuestsCards("story_goals")>>
<<if _goals.length > 0>>
  <div class="quests-section">
    <h3>Story Goals</h3>
    <<for _g range _goals>><<renderQuestsCard _g>><</for>>
  </div>
<</if>>

<<set _helpData = setup.help_data || {}>>
<<if _helpData.npcs>>
  <<for _npcId, _npcData range _helpData.npcs>>
    <<set _slug = setup.npcSlugForId(_npcId)>>
    <<set _card = _slug ? setup.pickQuestsCard(_slug) : null>>
    <<if _card>>
      <div class="quests-section">
        <h3><<print ($npcs[_npcId] && $npcs[_npcId].name) || _npcData.name>></h3>
        <<renderQuestsCard _card>>
      </div>
    <</if>>
  <</for>>
<</if>>

<<if !_goals.length && (!_helpData.npcs || !Object.keys(_helpData.npcs).length)>>
  <div class="no-quests">No active quests.</div>
<</if>>
<</nobr>>
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>
```

### New utility — `setup.lookupCanvasBySlug(slug)`

```
function lookupCanvasBySlug(slug):
    locCanvases = (setup.help_data || {}).locationCanvases || {}
    for each locUuid in locCanvases:
        for each canvas in locCanvases[locUuid]:
            if canvas.id === slug:
                return { canvas, locUuid }
    return null
```

~15 lines. Extracted from logic currently buried inside `_findFlagSetterCanvas`.

### Reused utilities (untouched)

- `setup._formatCanvasSchedule(canvas)` — `v2.py:6190-6205`
- `setup._locNameFromUuid(uuid)` — `v2.py:6208-6214`
- `setup.npcSlugForId(npcId)` — existing helper

### CSS classes used

Same naming convention as the old `.stage-hint-*` classes but namespaced under `.quests-*`:

- `.quests-card` (was `.stage-hint-card`)
- `.quests-flavor` (was `.stage-hint-flavor`)
- `.quests-tip` (was `.stage-hint-tip`)
- `.quests-goal` (was `.stage-hint-goal`)
- `.quests-goal-header` (was `.stage-hint-goal-header`)
- `.quests-where` (was `.stage-hint-where`)
- `.quests-ready` (was `.stage-hint-ready`)
- `.quests-terminal` (was `.stage-hint-arc-complete`)
- `.quests-section` (new — wraps NPC name + cards under a header)
- `.no-quests` (unchanged)

Stylesheet for these added to the V2 QuestsPage emission. Old stylesheet untouched.

---

## §5 Build-time integration (`template_import.py` + generator)

### Project metadata flag

New optional field on the `[project]` block:

```toml
[project]
title         = "The Long Summer — Test Slice"
quests_engine = "v2"   # opt-in; absent or "v1" → old engine
```

Plumbed through:
1. `Project` model — add `quests_engine` field (string, default `"v1"`)
2. `create_project_from_template` — reads the flag from TOML, stores on project
3. Generator — reads `project.quests_engine` to decide which engine to emit

### New normalizer

In `apps/projects/services/template_import.py`:

```python
@dataclass
class QuestsCondition:
    # flat shape — flag OR trait/counter, not both
    flag: Optional[str] = None
    trait: Optional[str] = None
    subject: Optional[str] = None    # "player" | "npc"
    npc_id: Optional[str] = None
    op: str = ""
    value: Optional[float] = None
    label: Optional[str] = None

@dataclass
class QuestsCard:
    text: str = ""
    ready_text: Optional[str] = None
    tip: Optional[str] = None
    npc_id: Optional[str] = None
    priority: int = 0
    group: Optional[str] = None
    when: List[QuestsCondition] = field(default_factory=list)
    goals: List[QuestsCondition] = field(default_factory=list)
    ready_canvas: Optional[str] = None
    terminal: bool = False
```

`_normalize_quests_cards(raw_data)` parses `quests.cards` table from raw TOML into `List[QuestsCard]`. Lives next to the existing `_normalize_hint_templates` function — both modules coexist.

### New validator

`_validate_quests_cards(cards, canvases, npcs)`:

1. Every card has non-empty `text` and non-empty `when` — else error
2. Every `goals` item targeting a trait/counter has a non-empty `label` — else error
3. Every `ready_canvas` reference resolves to an existing canvas slug — else error
4. Every `npc_id` reference resolves to an existing NPC slug — else error
5. `terminal = true` AND `ready_canvas` set → warning
6. Condition items use new flat shape (no `type` / `flag_key` / `trait_key` / `operator` fields) — else error
7. `group` set on a card with `npc_id` — warning (group is Story Goal only)
8. `priority` is integer — else error

Validator runs only when project metadata has `quests_engine = "v2"`. Old templates lint with the existing validator unchanged.

### Build pipeline dispatch

In the generator's `package_game` flow:

```python
if project.quests_engine == "v2":
    # Parse [[quests.cards]] via new normalizer
    quests_cards = _normalize_quests_cards(raw_data)
    _validate_quests_cards(quests_cards, canvases, npcs)
    # Emit V2 functions + widget + QuestsPage variant
    game_js += _emit_v2_quests_engine(quests_cards)
else:
    # Default — existing path unchanged
    hint_templates = _normalize_hint_templates(raw_data)
    _validate_hint_templates(hint_templates, ...)
    game_js += _emit_v1_quests_engine(hint_templates)
```

V1 path is byte-identical to today for non-migrated games.

### New serializer

`_serialize_quests_card(card)` → dict ready for embedding in `setup.quests_cards = [...]` JSON. Emits all fields with consistent naming (snake_case → camelCase if convention requires, otherwise matches TOML). Each card serializes to ~10–15 lines of JSON.

The runtime then sees `setup.quests_cards = [...]` as a top-level array — what the pickers walk.

---

## §6 TLS migration (TOML changes)

Concrete changes in `games/the_long_summer_test/toml_phases/`:

### A. `1_metadata_and_locations.toml`

Add to `[project]`:
```toml
quests_engine = "v2"
```

### B. `7_final_game.toml`

#### B1. Replace `[[story_arc.hints.templates]]` with `[[quests.cards]]`

Rewrite all 12 existing templates (`:2604-2707`) using field-mapping table in §3.

Direct mappings:
- Frank's 2 existing templates → 2 new cards (`ready_canvas` derived from old `arc_closure_flag`)
- Ryan's 3 stage-gated templates → 3 new cards (`goals` populated from old stage helper conditions; `when` updated to use trait checks directly)
- Jake's 3 stage-gated templates → 3 new cards (same pattern)
- 5 Story Goal templates (rent, settled-in, church, hygiene, energy) → 5 new cards (no `npc_id`; `group` field on rent/settled-in/church if multiple variants exist)

Plus 6–8 new Frank pre-catch / post-catch climbing / post-first-night / pre-Diana / Diana-ready / post-Diana terminal cards per doc 47 §7 walkthrough. Exact count and copy is authoring work in the implementation phase.

#### B2. Delete `[[engine.stage_helpers]]` block

Lines `:114-145`. Three entries (`ryan_stage_1`, `ryan_stage_2`, `jake_stage_2`).

**Pre-deletion verification:** grep TLS TOMLs for `ryan_stage_1`, `ryan_stage_2`, `jake_stage_2` to confirm no canvas trigger / choice gate / dev shortcut references them. (Expected: zero hits outside the deleted block, since helpers were only ever consumed by the hint renderer's Path E.)

#### B3. Delete `[[traits.labels]]` + `[[flags.labels]]` registries

Lines `:162-234`. All trait labels (`trust`, `arousal`, `corruption`, `beauty`, `ryan_help_count`) and flag labels (`frank_caught`, `frank_restrict_declared`, `group_settled_in`, `ryan_partner_open`, `jake_first_glance_noticed`, `jake_peek_draw_revealed`, `frank_office_first_sex_done`).

Labels move onto `goals` items directly.

#### B4. Delete stage integer variables (with verification)

In `[player.core_traits]` (declared per comment at `:249-252`):
- `npc_ryan_stage` — delete if grep shows no other consumer
- `npc_jake_stage` — delete if grep shows no other consumer

The 2026-05-11 RTS-shape conversion already deleted `npc_frank_stage`; this completes the parallel cleanup.

**Pre-deletion verification:** grep TLS TOMLs for `npc_ryan_stage` and `npc_jake_stage`. Expected hits only inside dev shortcuts that write the variable (e.g. `dev_advance_ryan_to_2`). If any production canvas reads them as gates, deletion blocks until those gates are converted to flag-based gates.

#### B5. Convert transition canvases

`transition_ryan_to_1`, `transition_jake_to_1_via_beauty`, `transition_jake_to_1_via_glance`, `transition_group_settled_in` (and similar).

For each:
1. **Keep** the canvas — its narrative prose and flag-setting role are still useful
2. **Strip** the `npc_<slug>_stage = N` write from its effects (the variable is gone)
3. **Keep** any closure flag write (`group_settled_in`, etc.)
4. **Verify** the trigger conditions don't reference the deleted stage variable

#### B6. Delete sidebar `hint`-type entries

In `2_sidebar_settings_etc.toml` (or wherever `[[sidebar_items]]` lives):
- Delete any entry of `type = "hint"`
- Other sidebar item types (`countdown`, `trait_bar`, decay warnings) untouched

The sidebar widget's `<<elseif _item.type is "hint">>` branch in `v2.py:13865-13871` is **not deleted** from the engine source — it stays available for other games. TLS's TOML just doesn't trigger that branch.

### Migration order

Sequential commits, each independently revertable:

1. Land new V2 engine code in `v2.py` (functions + widget + QuestsPage variant). Feature-flagged off by default. No game uses it yet.
2. Land new normalizer + validator + serializer in `template_import.py`. Feature-flagged off by default.
3. Land `quests_engine` flag plumbing in `Project` model + `create_project_from_template`.
4. Convert TLS's `7_final_game.toml` per B1. Build TLS with `quests_engine = "v2"` → verify Quests page renders.
5. Delete B2–B5 (helpers, labels, stage variables, transition stage writes) one PR each. Rebuild + smoke between.
6. Delete B6 (sidebar hint entries). Verify sidebar still works.
7. Add tests per §7.

Rolling back at any point: revert the metadata flag → TLS falls back to old engine. Old behavior restored (with the small caveat that the original `[[story_arc.hints.templates]]` block has been deleted, so a full roll-back also restores that block from git).

---

## §7 Verification

### Layer 1: Python unit tests

Add to `apps/projects/tests.py` (or new `tests/test_quests_v2.py`):

**Normalizer:**
- `[[quests.cards]]` with all fields populated → parses correctly
- Card without `npc_id` → routed as Story Goal
- Card with `terminal = true` and no `goals` → parses, no validation error
- Condition item in new flat shape → parses
- Condition item in old shape mixed in → validator catches

**Validator:**
- Missing `text` → error
- Empty `when` → error
- `goals` item targeting trait without `label` → error
- `ready_canvas` referencing nonexistent slug → error
- `npc_id` referencing nonexistent NPC → error
- `terminal = true` + `ready_canvas` set → warning
- `group` set on card with `npc_id` → warning

**Build dispatch:**
- Project with `quests_engine = "v2"` → generator emits V2 functions + widget + passage
- Project without flag (default) → generator emits V1 code byte-identical to today
- Both run in same test session without cross-contamination

**Serializer:**
- `QuestsCard` round-trip through `_serialize_quests_card` → JSON that runtime reads
- Field defaults present (`priority = 0`, `terminal = false`)

### Layer 2: SugarCube runtime smoke

A minimal test game at `games/quests_v2_smoke/` with 4 hand-crafted cards covering each frame variant. Build via `package_from_toml`, open HTML in headless browser via playwright skill. Assert:

- Card with `goals` not all met → `.quests-goal-header` contains `🎯 To advance` + `<ul>` with bullets
- Card with `goals` all met + `ready_canvas` → `🔓 Ready` + `<div class="quests-where">📍 ...` + `<div class="quests-where">🕒 ...`
- Card with `terminal = true` → `✓ Arc complete`
- Card with `ready_text` and all goals met → `.quests-flavor` div contains ready_text (not text)
- Story Goals section with 3 matching cards → all 3 render in file order
- Card with `priority = 1` beats card with `priority = 0` when both match

### Layer 3: TLS end-to-end manual walkthrough

Build TLS with `quests_engine = "v2"`. Use `twine-game-explorer` skill or playwright to drive through states using dev shortcuts. Confirm:

| State | Expected |
|---|---|
| Day 1 fresh start | Story Goals: rent + settled-in (+ hygiene/energy/church if applicable). Frank: pre-catch climbing card, `🎯 Maya's corruption — 0 / 25`. Ryan: stage 0 climbing, `🎯 Ryan trust — 5 / 10`. Jake: stage 0 card. |
| Bump corruption to 25 | Frank flavor swaps to ready_text. Goal block: `🔓 Ready + 📍 Living room + 🕒 Mon–Fri 20:00–22:30`. |
| Fire catch (`dev_force_catch`) | Frank swaps to post-catch / pre-declaration card with corruption bullet 25→35. |
| Bump corruption to 35 + fire declaration | Frank swaps to post-declaration card. `ready_canvas = scene_franks_bedroom_evening`. `🔓 Ready + 📍 Frank's bedroom + 🕒 Mon–Fri 21:00–23:00`. |
| Play first-night | Frank swaps to post-first-night card. |
| Force terminal | Frank shows `✓ Arc complete`. |
| Ryan: trust ≥ 10 via dev | Ryan card swaps from stage 0 to stage 1. |
| Pay rent | Rent card disappears from Story Goals section. |
| Sidebar | No hint surface visible. Other sidebar items (time, traits, decay warnings) render. |

### Layer 4: Regression on other games

Build a non-TLS game (e.g. `under_one_roof`) via `package_from_toml` after V2 lands. Confirm:

- Generated HTML diff vs pre-V2: no changes in QuestsPage section, no changes in old engine functions
- Existing pytest tests E9 / E10 / E11 / E15 / E17 / E20 pass unchanged
- Sidebar hint still works in the non-migrated game
- No new JS errors at build or runtime

### Success criteria

The PRD is complete when:

1. All Layer 1 pytest tests green
2. Layer 2 smoke game renders all four frame variants correctly
3. TLS Layer 3 walkthrough confirms every state-row renders as designed
4. Layer 4 regression check shows zero diff in non-migrated games' emitted code
5. Doc 47 §9 engine-support matrix can be rewritten with all ✅ across the two climbing rows (the gap closed)

---

## §8 Files this PRD will modify

### Created

- `apps/game_generation/twee_comprehensive/tests/test_quests_v2.py` (or merge into existing test file) — Layer 1 tests
- `games/quests_v2_smoke/` (minimal test game) — Layer 2 smoke target
- (Optional) `28th_april_TLS_Phase2_Redesign/49_*` follow-up implementation log

### Modified

- `apps/game_generation/twee_comprehensive/generators/v2.py` — new functions + widget + V2 QuestsPage variant + build dispatch
- `apps/projects/services/template_import.py` — new normalizer + validator + serializer + dispatch
- `apps/projects/models.py` (or wherever `Project` lives) — add `quests_engine` field
- `apps/projects/tests.py` — Layer 1 tests (or in the new test file above)
- `games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml` — add `quests_engine = "v2"`
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — full migration per §6
- `games/the_long_summer_test/toml_phases/2_sidebar_settings_etc.toml` — delete `hint`-type sidebar items

### Not touched

- All old V1 engine code in `v2.py`
- All other games' TOMLs
- Any frontend / Next.js / React code
- All non-Quests parts of `template_import.py` and the build pipeline

---

## §9 Open items the PRD doesn't decide

These belong in the implementation plan or future PRDs:

1. **Final authored card copy.** §3 examples are illustrative. Real Maya-voice copy for the 6–8 new Frank cards (and the Ryan/Jake/Story-Goal rewrites) is authoring work in the implementation phase.
2. **Exact `group` keys for Story Goals.** Whether rent has a `"rent"` group with ambient + crisis variants, or whether a single rent card with `priority` swap suffices. Authoring decision.
3. **Whether stage integer variables stay deleted long-term** or come back for a future feature (e.g. an arc-progress widget elsewhere in the UI). Currently deleted; resurrection is a future PRD if needed.
4. **CSS polish** — the `.quests-*` classes inherit visual styling from current `.stage-hint-*` definitions. Whether to add new visual treatment (animations on swap, color changes per frame state) is a follow-up.
5. **Migration helper for other games.** Optional CLI tool to convert old `[[story_arc.hints.templates]]` → new `[[quests.cards]]` automatically. Not built in V2; opt-in games hand-migrate.

---

## §10 References

### Source paths

- `apps/game_generation/twee_comprehensive/generators/v2.py:5648` — old `getStageHintForNPC`
- `:5777` — old `getGlobalHints`
- `:6106` — old `_isHintReady`
- `:6190-6205` — `_formatCanvasSchedule` (reused)
- `:6208-6214` — `_locNameFromUuid` (reused)
- `:6233-6438` — old `computeHintGoal`
- `:7055-7085` — old `getSidebarHint` (not implemented in V2)
- `:13760-13810` — old `renderStageHint` widget
- `:13865-13871` — old sidebar `hint` type branch (not implemented in V2)
- `:16067-16101` — old `:: QuestsPage` passage
- `apps/projects/services/template_import.py:769` — `auto_goal: bool = True` default
- `:1535,4004` — old serializer passthrough
- `games/the_long_summer_test/toml_phases/7_final_game.toml:107-110` — Frank stage helper retirement comment
- `:114-145` — current stage helpers block (to be deleted)
- `:162-234` — current label registries (to be deleted)
- `:249-252` — stage variable declaration comment
- `:2604-2707` — current `[[story_arc.hints.templates]]` (to be rewritten)
- `:6032-6100` — `scene_livingroom_catch` (Catch capstone — referenced by Frank pre-catch card's `ready_canvas`)

### Project docs

- `28th_april_TLS_Phase2_Redesign/47_Quests_Page_Unified_Card_Design.md` — analysis input
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — Frank progression spec
- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` — slice E-track
- `28th_april_TLS_Phase2_Redesign/34_TLS_Engine_PRD_Phase_E_Additions.md` — Phase E engine work
- `28th_april_TLS_Phase2_Redesign/11_Hint_Authoring_Guide.md` — old authoring reference (superseded for V2 games)

### Memory entries

- `frank_rts_shape_pass1` — the 2026-05-11 conversion that retired `npc_frank_stage`
- `feedback_hint_narrative_no_time_or_location` — voice doctrine for card text
- `feedback_rts_objective_quest_doctrine` — Story Goals authoring shape
- `phase_e_slice_redesign` — the "3-quest journal" Phase E promise
