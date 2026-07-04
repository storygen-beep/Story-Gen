# Engine reference — every knob the engine actually has

Read this when you need to know **whether a field exists and what the engine does with it** — before
emitting any TOML field, trigger, condition, or effect. This is the skill's authoritative "what the engine
reads / renders" table. **Every row is verified against live code** — the importer
(`apps/projects/services/template_import.py`, "the importer") and the active generator
(`apps/game_generation/twee_comprehensive/generators/v2.py`, "v2"), cited `file:line`. If a field isn't
here, the engine almost certainly doesn't read it — **don't invent a knob.** Where this file and the older
corpus drafts disagree, **the code wins**; the divergence is flagged inline as *(code-vs-lore: …)*.

> **`file:line` cites are approximate — grep the named symbol, don't trust the number.** The generated engine
> (`v2.py`) is regenerated and RENUMBERS often — a citation drifts the moment code is inserted above it (one
> engine change shifted lines +5 near the top to +294 near the bottom, across 67 hunks). Every cite names its
> **symbol** (a function, a variable, a quoted string) precisely because that's what survives a renumber: if a
> line looks wrong, `grep -n` the symbol in the current engine file and use the line it reports. Number = hint,
> symbol = truth.

This file is the **field mechanics**. The DESIGN decisions — which trait spines an arc, which lane to
reach for, how a map is shaped, when to enable a system — live in the sibling references. Cross-links are
explicit; nothing is duplicated. For the silent build-breakers and grep guards, `references/toml-gotchas.md`
is the home — this file points there, never restates them.

The canonical in-repo worked example is a complete shipped game: `games/late_shifts/toml_phases/`. When in
doubt about a shape, copy the analogous block from there.

## Contents
- §1 — Built-in traits (the list; ranges live in `trait-catalog.md`)
- §2 — `[[canvases]]` + `[canvases.trigger]` field set + lane fingerprints
- §3 — `exit_block.choices` — the complete `TemplateChoice` table
- §4 — Effects vs predicates — the two field-name systems + the condition-type set + the version rule
- §5 — `[[locations]]` field set
- §6 — `[[npcs]]` field set
- §7 — `[settings]` homes — the enable-switch scoping map
- §8 — `[project]` / `[time]` / `[engine.daily_tick]` / `[[sidebar_items]]` (brief)
- §9 — Canonical worked-TOML skeleton

---

## §1 — Built-in traits

The engine has **no hardcoded trait list and no hardcoded defaults** — every trait is author-declared in
`[player.core_traits]` (read at `template_import.py:1537`) or each NPC's `[npcs.core_traits]` (`:1601`),
verbatim, with its initial integer. The "built-in set" below is the RTS-shape *convention*, not an engine
constant. **Declare every trait before use** or it's a silent no-op gate / hard sidebar fail
(`references/toml-gotchas.md`).

Canonical set: **player** — `corruption`, `arousal`, `energy`, `hygiene`, `money`, plus optional
`exhibitionism` / `fitness` / `intelligence`, plus one `<slug>_stage` per arc'd NPC. **NPC** — `relation`,
`corruption`, `arousal`.

For each trait's range / default / decay / which sidebar primitive renders it, and the throttle-vs-odometer
distinction → **`references/trait-catalog.md`**. Which trait spines which arc → `references/trait-design.md`.

> **Clamp trap — effects are UNBOUNDED by default; you opt IN to clamping.** The low-level
> `applyAndNotifyTrait` defaults `clamp = true` (`v2.py:5440-5442`, `next = window._traitClamp(next, 0, 100)`)
> — BUT the effect-application path overrides it: it calls with `eff.clamp || false` (`v2.py:2084`, also
> `:2001`), and job income hardcodes `false` (`:2674`). So a TOML effect that OMITS `clamp` — e.g.
> `{ trait = "money", op = "add", value = 45 }` — runs with `clamp = false` and applies the raw delta with
> **no 0–100 bound**. That's correct for `money` (it climbs past 100 freely — `trait-catalog.md`'s "no cap" is
> right). The flip side: a 0–100 stat (corruption, etc.) will ALSO exceed 100 if you over-add, because nothing
> auto-clamps it — and if a **banded** stat leaves its bands, its sidebar card silently vanishes
> (`trait-catalog.md` §4). To BOUND a stat, pass **`clamp = true`** (clamps 0–100) or **`cap = N`** (per-effect ceiling,
> `v2.py:5444-5450`). Spending via per-choice/canvas **`costs`** hardcodes `clamp = true` (`v2.py:4367`), so
> deductions floor at 0. Bottom line: in TOML, unbounded is the default — clamp/cap is something you add.

---

## §2 — `[[canvases]]` + `[canvases.trigger]`

Canvas dataclass `TemplateCanvas` at `template_import.py:689`. Trigger dataclass `TemplateTrigger` at
`template_import.py:459`; parsed at `template_import.py:1676-1748`.

### §2.1 — Canvas top-level

| Field | Type | Notes |
|---|---|---|
| `id` | str | unique slug |
| `name` | str | display |
| `description` | str | author-side only |
| `trigger` | table | the gate — §2.2 |
| `nodes` | list | body — `TemplateNode` at `:670` (`id`, `name`, `blocks`, `exit_block`, `loop_terminal`, `modifier_redirect`) |
| `connections` | list | graph-editor only; **runtime ignores** |
| `loop` | table | loop config (advanced) |

*(code-vs-lore: `guide` is documented in the corpus as a tolerated pending field — it is **not** on the
`TemplateCanvas` dataclass (`:689`) and is not parsed. Emitting it is harmless but does nothing. Don't rely
on it.)*

### §2.2 — `[canvases.trigger]` — the lane gate

**Every gating/scheduling field lives UNDER `[canvases.trigger]`, never at the `[[canvases]]` top level** —
placed at canvas level they are silently ignored (`references/toml-gotchas.md` "Trigger-field placement").

| Field | Type | Default | What it does |
|---|---|---|---|
| `location` | str | required | Where the canvas anchors. Read `:1677`. |
| `is_active` | bool | `true` | Soft on/off. `:1678`. |
| `is_repeatable` | bool | `true` | Lane 1/2/3 = `true`; Lane 4 capstone = `false`. `:1679`. |
| `max_triggers_per_day` | int? | — | Per-day cap. Lane 3 targets typically `1`. `:1680`. |
| `priority` | int | `0` | Lane 4 capstones use `≥ 9` — tie-break in auto-fire selection. `:1685`. |
| `conditions` | table | `{}` | `{version, logic, items}` gate — §4. `:1686`. |
| `schedules` | list | `[]` | Per-canvas `{weekdays, start_time, end_time}` windows. Dataclass `:452`; parsed `:1662-1675`. A hub renders only inside its OWN window. |
| `npc` | str? | — | **Portrait field** → sets `npcId`. `:1688`. Only a repeatable canvas with `npc` renders as an NPC portrait→menu. |
| `trigger_mode` | str | `"manual"` | `"manual"` (Lane 1/3/4) or `"random"` (Lane 2). `:1689`. |
| `chance` | float? | — | 0.0–1.0; **Lane 2 only** (random fire probability). `:1690`. |
| `costs` | list | `[]` | `[{trait, value}]` — **how you GATE a resource** on entry: affordability-checked, dims the button `(N Energy)`, deducts on entry. `:1695-1699`. Full model: `references/toml-gotchas.md` "Resource gating". |
| `show_when_blocked` | bool | `false` | Render a grayed entry on the Quests page when a daily cooldown blocks. `:1700`. |
| `cooldown_message` | str? | — | Blocked-entry text. `:1701`. |
| `entry_only_from` | list | `[]` | Lane 2 anti-toggle: fire only if the previous location matched. `:1705-1709`. |
| `substitutions` | list | `[]` | **Lane 3 dispatcher rules** — §2.4. `:1715-1735`. |
| `substitution_only` | bool | `false` | Excluded from portrait/solo/auto-fire grids; reachable ONLY via a substitution rule. `:1736`. |
| `requires_npc` | str? | — | **Presence gate only** (does NOT set `npcId`): ANDs `getNpcLocation(npc).location === location`. `:1740`. |
| `pre_substitution_effects` | list | `[]` | Effects that run unconditionally before the substitution check (`{targetType, npcId?, trait, op, value, clamp?, cap?}`). `:1744-1748`. |

> **`npc` ≠ `requires_npc` — separate fields; an NPC hub needs BOTH.** `npc` is the portrait (→`npcId`);
> `requires_npc` is presence only. A repeatable hub with `requires_npc` but no `npc` has no `npcId` and
> drops to the flat solo-activity bucket — no build error, only live-play shows it. Full trap (with the
> Lane 2 `trigger_mode="random"`+`chance` twin): `references/toml-gotchas.md`.

### §2.3 — Lane fingerprints (which combination = which lane)

| Lane | Diagnostic trigger fields | Design home |
|---|---|---|
| **1 — Hub button** | `trigger_mode="manual"` + `is_repeatable=true` + `npc` set + (`requires_npc` for presence) + `schedules` covering the NPC's window | `references/lanes.md` |
| **2 — Location-entry random** | `trigger_mode="random"` + `chance` + `is_repeatable=true` (often `requires_npc`) | `references/lanes.md` |
| **3 — Dispatcher (parent activity)** | `trigger_mode="manual"` + `is_repeatable=true` + `substitutions=[…]` (solo-clickable) | `references/lanes.md` |
| **3 — Substitution target** | `substitution_only=true` + `requires_npc` + `is_repeatable=true` + `max_triggers_per_day=1` | `references/lanes.md` |
| **4 — Capstone (auto-fire)** | `trigger_mode="manual"` + `priority ≥ 9` + `is_repeatable=false` + a flag-setter effect on exit | `references/beat-authoring.md` |

### §2.4 — `[[canvases.trigger.substitutions]]` (Lane 3)

Each rule is a free-form dict (parsed `:1715-1735`):

| Field | Type | Notes |
|---|---|---|
| `target_canvas_id` | str | slug of the target canvas (resolved to UUID at build) |
| `chance` | float | 0.0–1.0; for a Pattern-B group, the cumulative bucket size within the group |
| `conditions` | table? | extra `{version, items}` (ANDs with the target's own gates) |
| `exclusive_group` | str? | Pattern-B mutex group: rules sharing this string share ONE dice roll; a failed condition in the claimed slot falls to solo (not the next rule). `:1726-1731`. |

### §2.5 — `[[canvases.nodes]]` body blocks + `exit_block`

Block vocabulary (`canvases.nodes.blocks`, each `{type, …}`) — only these types are real: `paragraph`,
`dialog` (`{type="dialog", npcId, content}`), `thought_bubble`, `image`/`video` (`{props.file}`) / `clip`
(`{props.clipId}` — a DB asset, NOT a file; full media shapes + the `search_queries` craft in
`references/media.md`), `heading`, `group` (`{props.conditions, props.blocks}`), `block_pool`, `cascade`. A mistyped `type` does
**NOT** ship silently: the importer **HARD-FAILS the build** on an unrecognized content block type, with a
did-you-mean hint (`dialogue`→`dialog`, `speech`→`dialog`) — `_validate_content_block_types`,
`template_import.py:2805` (error appended ~`:2826`). The "silent `<p>` degrade that drops the speaker"
(`v2.py:13923-13936`) is only the GENERATOR's fallback for non-importer entry points (e.g. the editor), not
the build path. **Dialogue MUST be `type="dialog"`** — `type="dialogue"`/`"speech"` fail the build
(`references/toml-gotchas.md` for the grep guard).

`exit_block` (`TemplateExitBlock` at `:662`): `type` = `"location"` or `"choices"`.
- `type="location"` → single return button; `config = {destinationType, locationId, time_progression_minutes}`.
  `destinationType` must be `"trigger"`, `"specific"`, or `"node"` (validated `:3900`; default `"trigger"`,
  `v2.py:12567`).
- `type="choices"` → the menu (Lane 1 hub) — §3.

---

## §3 — `exit_block.choices` — the complete `TemplateChoice` table

Dataclass `TemplateChoice` at `template_import.py:620`; **parsed at `template_import.py:1955-1988`** — that
parse block is the source of truth for which keys the importer actually reads. (`references/toml-gotchas.md`
used to point here as "the full table"; this is it.)

| TOML key | Read at | Type / default | Notes |
|---|---|---|---|
| `text` | `:1957` | str `"Continue"` | button label |
| `targetType` | `:1958` | str `"trigger"` | `"trigger"` / `"location"` / `"node"` |
| `locationId` | `:1959` | str? | for `targetType="location"` |
| `nodeId` | `:1960` | str? | for `targetType="node"` — route within canvas, or `"canvas_id.node_id"` cross-canvas |
| `time_progression_minutes` | `:1961-1967` | int? | advances the clock on click |
| `effects` | `:1968` | list | trait effects — §4.1 |
| `flagEffects` | `:1969` | list | flag effects — §4.2 **(camelCase)** |
| `wardrobeEffects` | `:1970` | list | `[{op:"equip"\|"unequip", slot, item_id?}]` **(camelCase)** |
| `conditions` | `:1971` | table | per-choice gate `{version, items}` — §4. **Needs `version="1.0"` or fails OPEN.** |
| `show_when_locked` | `:1972` | bool `false` | render greyed when conditions fail |
| `locked_text` | `:1973` | str | the greyed reason |
| `locked_text_threshold` | `:1974` | str | **makes the locked rung a clickable toast-button** — OMIT for a plain greyed span |
| `rejection_node` | `:1975` | str? | route here on locked-click (Mode B) |
| `rejection_effects` | `:1976` | list | effects on rejection-click |
| `modifier_effects` | `:1977` | list | temporary trait offsets |
| `passEffects` | `:1909` | list | `[{pass_id}]` — stored as `pass_effects` **(camelCase in TOML)** |
| `itemEffects` | `:1915` | list | `[{item_id, action:"add"\|"remove", quantity}]` — stored as `item_effects` **(camelCase in TOML — snake `item_effects` is silently dropped)** |
| `questEffects` | `:1925` | list | `[{quest, op, step?}]` **(camelCase)** |
| `scheduleEffects` | `:1935` | list | `[{delayDays, action, flag?/quest?/conversation?}]` **(camelCase)** |
| `text_variants` | `:1946` | list | `[{text, conditions}]`; first match wins |
| `costs` | `:1983-1987` | list | `[{trait, value}]` — per-choice resource cost; a tier UNDER `conditions`; deducts on click |
| `inc` | `:1829` | list | shorthand: `["counter"]` or `[{counter, by}]` → expands to add-op effects |

> **The camelCase trap.** Choice-level effect *containers* are read from camelCase TOML keys: `flagEffects`,
> `wardrobeEffects`, `itemEffects`, `passEffects`, `questEffects`, `scheduleEffects`. Writing the snake form
> (`item_effects = […]`) means the importer never sees it — the buy choice still charges money/`costs` but
> grants nothing, with no build error. (The *inner* effect rows below still use their own field names — see
> §4.) Full trap + grep guard: `references/toml-gotchas.md` "Item grant on a choice uses `itemEffects`".

`costs` (resource gating) is the same `costs` semantic as the trigger (§2.2), at the choice level — for a
per-choice differential (e.g. −15 vs −28 energy). Full model: `references/toml-gotchas.md` "Resource gating".

---

## §4 — Effects vs predicates — the two field-name systems

⚠️ **Effects and predicates use DIFFERENT field names. Mixing them silently no-ops — no build error.** The
validators at `template_import.py:1093`/`:1114` catch *some* cases as warnings, not all.

| Concept | EFFECT field (mutation) | PREDICATE field (condition) |
|---|---|---|
| player vs npc | `targetType` | `subject` |
| npc identifier | `npcId` | `npc_id` |
| trait name | `trait` | `trait_key` |
| flag name | `flag` | `flag_key` |
| operation | `op` | `operator` |
| type tag | (dispatched by `trait` vs `flag` presence) | `type` (required) |

### §4.1 — Trait effect (mutation)

Dataclass `TemplateChoiceEffect` at `template_import.py:514`. Applied by `applyAndNotifyTrait`
(`v2.py:5539` → `applyTraitEffect` `v2.py:5395`).

```toml
{ targetType = "player", trait = "corruption", op = "add", value = 1 }
{ targetType = "player", trait = "arousal", op = "set", value = 0 }        # climax reset
{ targetType = "player", trait = "energy", op = "add", value = -10 }       # decay = negative add
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }
{ targetType = "player", trait = "money", op = "add", value = 90 }  # unbounded — clamp defaults false on effects
```

| Field | Required | Notes |
|---|---|---|
| `targetType` | yes | `"player"` / `"npc"` |
| `npcId` | when npc | NPC slug (NOT `npc_id`) |
| `trait` | yes | trait name (NOT `trait_key`) |
| `op` | yes | `"add"` or `"set"` — **there is NO `"sub"` op** (`v2.py:5430-5437`; unknown op = no-op). Negative `value` decays. |
| `value` | yes | integer |
| `clamp` | no | The effect path passes `eff.clamp \|\| false` (`v2.py:2084`), so an OMITTED `clamp` = **`false` = unbounded** (the low-level fn defaults `true`, but the effect path overrides it). Set **`clamp = true`** to bound a stat to 0–100. |
| `cap` | no | per-effect upper bound (`v2.py:5444-5450`) |
| `conditions` | no | gate this effect (used on `[engine.daily_tick]` entries) |

**Stage advancement** uses the **player** namespace: `{ targetType = "player", trait = "<slug>_stage",
op = "set", value = N }`. The engine special-cases `/^([a-z_]+)_stage$/` and logs an upward delta to
`stage_advancement_log` (`v2.py:5548-5554`). Never `targetType="npc"`. Predicate side: `{ type = "trait",
subject = "player", trait_key = "<slug>_stage", operator = "gte", value = N }`. (`references/toml-gotchas.md`,
`trait-catalog.md` §3.)

### §4.2 — Flag effect

Dataclass `TemplateFlagEffect` at `template_import.py:532`.

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "toggle" }
```

`op` = `"set"` / `"unset"` / `"toggle"`; flag name is `flag` (NOT `flag_key`); `npcId` when npc.

### §4.3 — Predicate (condition) — the typed `{version, logic, items}` block

Evaluated by `triggerConditionsSatisfied` (`v2.py:3530`). Used on `[canvases.trigger.conditions]`,
per-choice `conditions`, group-block `props.conditions`, substitution-rule `conditions`,
location `entry_conditions`, stage-helper `conditions`, and phone `trigger.conditions`.

> **⚠️ `version = "1.0"` IS MANDATORY — omit it and the gate FAILS OPEN.** The evaluator opens with
> `if (!conditions.version || conditions.version !== '1.0') return true;` (**`v2.py:3534`**). A block
> missing `version` is treated as satisfied — items never checked. No build error, no validator catch. The
> whole function ALSO fails open on any thrown exception (`v2.py:3873-3875`). *(code-vs-lore: the corpus +
> `toml-gotchas.md` cite this at `v2.py:3312` — the real line is **3534**. The rule is right; the line was
> stale. The behavior table here supersedes it.)* Grep guard + full trap: `references/toml-gotchas.md`.

```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
```

`logic` = `"AND"` (default) or `"OR"` (`v2.py:3537`, `:3871-3872`). `subject` = `"player"` or `"npc"` (npc
requires `npc_id`).

**The complete live condition `type` set (16 — verified `v2.py:3596-3864`).** Anything else → the item is
`false` (`v2.py:3866-3867`).

| `type` | Required fields | Operators / behavior | Code |
|---|---|---|---|
| `flag` | `subject`, `flag_key` | `is_true` / `is_false` (missing reads false) / `exists` | `:3596` |
| `modifier` | `modifier_key` | `is_active` (else negated) | `:3635` |
| `trait` | `subject`, `trait_key`, `operator`, `value` | `eq`/`ne`/`gt`/`gte`/`lt`/`lte` (numeric) · `in`/`not_in` · `contains`/`not_contains` · `exists`/`not_exists` | `:3644`, ops `:3553-3585` |
| `days_since_flag` | `subject`, `flag_key`, `operator`, `value` | numeric — days since the flag's `set_day` | `:3669` |
| `clothing_slot` | `slot`, `operator` | `equipped` / `unequipped` (clothing-enabled only) | `:3706` |
| `clothing_item` | `item_id`, `operator` | `equipped` / `unequipped` / `owned` / `not_owned` | `:3723` |
| `worn_beauty` | `operator`, `value` | numeric — MAX beauty across equipped | `:3751` |
| `worn_corruption` | `operator`, `value` | numeric — MAX corruption across equipped (content router; ≠ player.corruption) | `:3751` |
| `worn_type` | `operator`, `value` | `eq` / `neq` against an outfit category string | `:3766` |
| `pass` | `pass_id`, `operator` | `is_active` (else negated) | `:3785` |
| `item` | `item_id`, `operator`, `value` | numeric inventory count | `:3795` |
| `stage` | `helper`, `operator` | resolves a named `[[engine.stage_helpers]]`, recursively evaluates; `is_false` negates | `:3808` |
| `quest` | `quest_id`/`quest`, `operator` | `active` / `completed` / `step_gte` | `:3824` |
| `corruption_level` | `operator`, `value` | banded 0–4 from tiers `[0,5,15,30,45]` (override `[engine].corruption_tiers`); `gte`/`lt`/`eq` | `:3836`, tiers `v2.py:5622-5628` |
| `npc_at_location` | `location_id` (`npc_id` optional), `operator` | `is_present` / `is_absent`; with `npc_id` → that NPC at the location, without → any NPC (room occupied/empty) | `:3847` |

*(code-vs-lore: `npc_at_location` IS live (`:3847`) — older corpus drafts omit it entirely, and miss
`contains`/`not_contains` on `trait`. Treat this code-verified table as the set.)*

### §4.4 — Quest-card conditions are a DIFFERENT, flat shape

`[[quest_cards]]` `when` / `goals` use `QuestsCondition` (`template_import.py:848`) — **flat, no `type`
discriminator**: `{ flag, op }` or `{ trait, subject, npc_id?, op, value, label }`. Do NOT use the typed
`{type, …}` shape inside a quest card, and don't use the flat shape anywhere else. (`references/systems.md`
for the quest-card design model.)

```toml
{ flag = "frank_caught", op = "is_true" }
{ trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" }
```

---

## §5 — `[[locations]]` field set

Dataclass `TemplateLocation` at `template_import.py:135`; parsed at `template_import.py:1625-1642`.

| Field | Read at | Type | Notes |
|---|---|---|---|
| `id` / `name` / `description` / `image` | `1627-1630` | str | basics |
| `image_search_queries` | `1631` | list | Missing-Media page. NOTE the key-name trap: a **location** uses `image_search_queries`; a **content block** uses bare `search_queries`. Query craft in `references/media.md`. |
| `is_container` | `1632` | bool | **pure-nav wrapper — SWALLOWS attached canvases** (renders only the child menu). Never attach a canvas to a container. |
| `offscreen` | `1633` | bool | **non-navigable "away" label** — no nav card, no hub; NPCs schedule here for home/sleep/work; exempt from presence floor + reachability. The 3rd location category. |
| `parent` | `1634` | str | structural nesting only (canvas inheritance) — NOT navigation |
| `entry_from` | `1635` | str | navigation parent — "Leave X" links here |
| `default_entry` | `1636` | str | (containers) child to auto-redirect into |
| `navigation_order` | `1637` | list | ordered child slugs; each MUST have `entry_from` = this location, or the build rejects it (`:3581`) |
| `entry_conditions` | `1638` | table | `{version, items}` — deny entry when it fails. **Needs `version="1.0"` or it fails OPEN** (§4.3). Visible-but-blocked; no native time lock. Evaluated `v2.py:4457` (`navDestUnlocked` → `triggerConditionsSatisfied`). |
| `blocked_message` | `1639` | str | rendered inline on the greyed nav card AND the blocked passage (one source) |
| `costs` | `1640` | table | per-ENTRY travel friction: `time` (minutes, advances the clock) + any other key deducts that player trait. Empty = free. |
| `clothing_rules` | `1641` | list | per-location coverage gate; `slots_required` must be **non-empty** + every slot in `VALID_CLOTHING_SLOTS` or the import HARD-FAILS (validator `:3586-3597`; `VALID_CLOTHING_SLOTS` = `bra/underwear/top/bottom/dress/legwear/shoes`, `:158`) |

Design (map shape, layering, reachability triad, lock contract, travel friction) → `references/location-design.md`.
Clothing-rule mechanics + the conditional-coverage pattern → `references/toml-gotchas.md` /
`references/clothing.md`.

---

## §6 — `[[npcs]]` field set

Dataclass `TemplateNPC` at `template_import.py:107`; parsed at `template_import.py:1595-1610`.

| Field | Read at | Type | Notes |
|---|---|---|---|
| `id` / `name` / `description` / `portrait` | — | str | basics |
| `core_traits` | `1601` | table | per-NPC initial trait values (`relation` / `corruption` / `arousal`) — same declare-before-use rule |
| `flag_keys` | — | list | pre-declared NPC flags |
| `schedules` | `1603` | list | `[[npcs.schedules]]` — the NPC location source of truth |
| `customizable` | `1604` | bool | player renames + picks a relationship at start — **requires** `relationship` + `relationship_options`, default ∈ options, or the import HARD-FAILS (validator `:3420-3429`) |
| `relationship` | `1605` | str? | default relationship label |
| `relationship_options` | `1606` | list | picker choices |
| `arc_stages` | `1609` | list | display strings only (the integer lives at `player.core_traits.<slug>_stage`); length implies max stage = len−1 |
| `hidden_from_ui` | — | bool | omit from Guide / Stats / sidebar |
| `trait_decay` | — | table | per-NPC daily decay |

`[[npcs.schedules]]` (`TemplateNPCSchedule` `:94`): `location` (slug→UUID at build), `weekdays`
(0=Mon…6=Sun, empty=all), `start_time`/`end_time` (`HH:MM`), `activity` (author-side label). The NPC's
location is **derived** by `getNpcLocation` (`v2.py:3141`, returns `{location, activity}`) — there is no stored location field. Keep rows
non-overlapping. The **co-location / meta-location** model (an NPC scheduled at the exact canvas location vs
a shared meta-location) drives the `requires_npc` walk-in direction — design in `references/lanes.md` /
`references/location-design.md`.

Customization `@`-token output, schedule→hub presence-floor design, and which trait spines the arc →
`references/customization.md`, `references/location-design.md`, `references/trait-design.md`.

---

## §7 — `[settings]` homes — the enable-switch scoping map

**Each optional system is OFF unless a key in its OWN table turns it on.** Authoring an enable key *bare*
(directly after another table) scopes it under the wrong table, the read comes back empty, and the system
reads as disabled **with no error** — a silent failure that has shipped dead systems. The scoping:

| System | Enable key + home | Read at | Item/config tables |
|---|---|---|---|
| **Clothing** | `clothing_enabled` in `[settings]` (+ `wardrobe_location`, `shop_location`) | `template_import.py:2241-2244` | `[[clothing]]` items; `[settings.clothing_requirements]` (`:2268`); per-location `clothing_rules` |
| **Rent** | `enabled` in `[settings.rent]` | `:2399-2400` | `[settings.rent]`: `amount`/`due_day`/`collector_npc`/`grace_periods`/`start_after_flag`/`eviction_mode`/`eviction_flag`/`text` (`:2401-2408`) |
| **Phone** | `enabled` in **top-level `[phone]`** (defaults `true` when the table is present) | `:2411-2415` | `[[phone.apps]]`, `[[phone.conversations]]`, `[[phone.posts]]`, … |
| **Time** | `[time]` (`enabled`/`starting_hour`/`starting_day`/`starting_week`) | `:1481` | — |

*(code-vs-lore: there is **no** bare `phone_enabled`, `rent_enabled`, or `rent_amount` key — those forms are
dead config the importer never reads. Rent keys are `enabled`/`amount`, not `rent_enabled`/`rent_amount`.)*
The design model for each system (when to enable, the patterns) → `references/systems.md`,
`references/clothing.md`.

```toml
[settings]            # clothing
clothing_enabled = true
[settings.rent]       # rent
enabled = true
[phone]               # phone — top-level, NOT under [settings]
enabled = true
```

---

## §8 — `[project]` / `[time]` / daily tick / sidebar (brief)

- **`[project]`** (`TemplateProject` `:43`): TOML key is **`id`** (stored internally as `slug`, read
  `:1473`) — not `slug`. `title`, `description`, `quests_engine` (`"v2"` enables `[[quest_cards]]`).
- **`[engine.daily_tick]`** (`TemplateDailyTick` `:415`): `flagEffects` (clear daily-cooldown flags) +
  `traitEffects` (per-day deltas, each a §4.1 effect with optional per-entry `conditions`). This is where you
  author the arousal climb / hygiene decay — **the engine hardcodes no daily passive**. (`trait-catalog.md`.)
- **`[[sidebar_items]]`** — `{type, …}`; types validated at `template_import.py:3129`+. Live types include
  `trait_words`, `trait_bar`, `trait_status_text`, `trait_decay_warning`, `npc_panel` (rows validated
  against `("arousal","corruption","location","next")`, `:3373`), `passes`, `inventory`. Which primitive
  renders which stat + the doubling trap → **`trait-catalog.md` §5** and `references/hud.md`.
- **`[[engine.stage_helpers]]`** (`:429`): named composite gates (`name`, `conditions`, `dev_only`);
  referenced by a `{type="stage", helper=…}` predicate; helper→helper recursion rejected at validate-time.

---

## §9 — Canonical worked-TOML skeleton

A minimal end-to-end shape (project + location + NPC + one Lane-1 hub + one Lane-4 capstone). For a full,
shipped, multi-system game, read `games/late_shifts/toml_phases/` — that is the in-repo gold standard.

```toml
[project]
id = "test_game"            # TOML key is `id`, not `slug`
title = "Test Game"
quests_engine = "v2"

[time]
starting_hour = 8
starting_day = "Monday"

[player]
name = "Maya"
[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
frank_stage = 0

[[npcs]]
id = "npc_frank"
name = "Frank"
arc_stages = ["neutral", "caught", "cracked"]
[npcs.core_traits]
relation = 0
corruption = 0
arousal = 0
[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0,1,2,3,4]
start_time = "07:00"
end_time = "09:00"
activity = "Making coffee"

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
entry_from = "loc_house"

# ---- Lane 1 hub (clickable NPC portrait → menu) ----
[[canvases]]
id = "frank_kitchen_hub"
name = "Frank in the kitchen"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_frank"            # portrait field — sets npcId
requires_npc = "npc_frank"  # presence gate — BOTH needed
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4], start_time = "07:00", end_time = "09:00" }]
[[canvases.nodes]]
id = "hub"
name = "Hub"
blocks = [{ type = "dialog", npcId = "npc_frank", content = "Morning." }]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee"
effects = [{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 1 }]
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 10

# ---- Lane 4 capstone (auto-fires on entry, once) ----
[[canvases]]
id = "scene_catch"
name = "The catch"
[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = false
priority = 10
conditions = { version = "1.0", items = [          # version REQUIRED or fails open
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.nodes]]
id = "catch"
name = "The catch"
blocks = [{ type = "paragraph", content = "He's there before you hear him." }]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Lower your eyes."
flagEffects = [{ targetType = "player", flag = "frank_caught", op = "set" }]
effects = [{ targetType = "player", trait = "frank_stage", op = "set", value = 1 }]
targetType = "location"
locationId = "loc_living_room"
```

---

**That's the engine surface authoring touches.** Silent build-breakers + grep guards →
`references/toml-gotchas.md`. Trait data → `trait-catalog.md`. Lane/map/system DESIGN → `references/lanes.md`,
`references/location-design.md`, `references/systems.md`.
