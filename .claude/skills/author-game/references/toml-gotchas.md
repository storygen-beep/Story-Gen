# TOML emission gotchas — the silent build-breakers

Check this before emitting any TOML. These are the rules that fail the build (or, worse, *silently*
no-op) and that an author hits constantly. All from `prompts_v2` `schema/01`/`schema/02`, verified
against the shipped `games/late_shifts/toml_phases/`.

## Hard build-breakers
- **Inline tables must be SINGLE-LINE.** A `{ ... }` inline table wrapped across newlines breaks
  `tomllib` and fails the merge parse — the single most common build-breaker. Keep every inline
  table on one line (arrays-of-tables `[[x]]` blocks can span lines; inline `{}` cannot).
- **Every `conditions` block needs `version = "1.0"` or it FAILS OPEN.** The engine evaluator
  (`triggerConditionsSatisfied`, v2.py:3312) opens with `if (!conditions.version || conditions.version
  !== '1.0') return true;` — a `conditions` object lacking `version = "1.0"` is treated as
  **satisfied** (always-pass), the items never checked. **No build error, no validator catch.** This
  bites *choice-level* gates most (authors write `conditions = { items = [...] }`): the gate silently
  never fires, so locked rungs, daily caps, and capstone-gated choices all show from the start. Applies
  to EVERY condition block — `[canvases.trigger.conditions]`, per-choice `conditions`, group-block
  `props.conditions`, substitution-rule `conditions`, `entry_conditions`, stage-helper `conditions`.
  Always write `conditions = { version = "1.0", items = [ ... ] }`. Grep guard before build:
  `grep 'conditions = { items = \['` must return ZERO. (A real game shipped 17 fail-open choice gates
  this way — incl. its ending fork — before this was caught.)
- **Declare every trait BEFORE use.** Any trait referenced anywhere — an effect, a condition, a
  sidebar item, or a `<slug>_stage` — must already exist in `[player.core_traits]` or the NPC's
  `[npcs.core_traits]`. Undeclared trait → **sidebar = hard fail**, **effect/condition = silent
  no-op** (you won't see an error; the gate just never fires). New trait in a beat ⇒ add it to
  core_traits in the same turn (and register intent in the R7 brief).
- **Per-NPC sidebar items ARE supported** (the old "hard-fails" note is stale). `trait_bar`/`trait_words`/
  `trait_status_text` accept `trait_owner = "npc"` + `npc_id` (renders that NPC's trait). For the RTS
  House-card use **`type = "npc_panel"`** (`npc_id` + `rows = ["arousal","corruption","location","next"]`):
  arousal → band glyph, corruption → number, location → `getNpcLocation` (same schedule source as the
  Schedule page), `next` → the Quests-page goal block (🎯 To advance + progress while climbing, 🔓 Ready
  / 📍 / 🕒 when ready), reusing `renderQuestsGoalBlock` for exact parity. `stage`/`awareness` still
  never surface; relation/corruption milestones can also go on the Quests page — either is fine.

## Right shapes (get these exact)
- **Choice (`exit_block.choices`) field set** — see `schema/02` §7.4 for the full `TemplateChoice`
  table (`targetType` + `locationId`/`nodeId`, `conditions`, `effects`, `flagEffects`,
  `time_progression_minutes`, locked-visible fields). **Locked-render trap (looks wrong if backwards):**
  `locked_text_threshold` makes the locked rung a clickable **button** that toasts the gate value —
  OMIT it (and `locked_text`) for a plain greyed span showing the action text (the TLS look; `lanes.md`).
- **Stage-trait mutation uses the PLAYER namespace** (`schema/01` §6.7): advance a stage with
  `{ targetType = "player", trait = "<slug>_stage", op = "set", value = N }` — NOT `targetType="npc"`.
  Predicate side: `{ type = "trait", subject = "player", trait_key = "<slug>_stage", operator = "gte", value = N }`.
- **Effect vs predicate field names differ — never cross them** (silent no-op if you do): effects use
  `targetType`/`trait`/`op`; predicates use `subject`/`trait_key`/`operator`. Full card: `schema/02` §16.4.
- **Two condition shapes** — trigger conditions are TYPED (`{type, subject, flag_key/trait_key,
  operator, value}`); quest-card `when`/`goals` are FLAT (`{flag, op}` / `{trait, subject, npc_id,
  op, value, label}`). `schema/02` §16.5.

## Trigger-field placement (silent if wrong)
- **`substitution_only`, `max_triggers_per_day`, `requires_npc`, `npc`, `chance`, `trigger_mode`,
  `schedules`, `substitutions` all live UNDER `[canvases.trigger]`** — NOT at the `[[canvases]]`
  top level. The importer reads them from the trigger; placed at canvas level they're silently
  ignored (e.g. a misplaced `substitution_only` → the canvas wrongly shows as a normal activity
  button). Live-verified 2026-06-03.

## Resource gating — `costs`, not `effects` (the cosmetic-energy trap)
- **Spending energy/hygiene with `effects { op = "add", value = -N }` deducts but NEVER gates.**
  An effect just moves the number — there is **no affordability check**, it can drive the trait
  negative, and it blocks nothing. A game whose only energy "spend" is effects has a **cosmetic**
  energy bar: the player works/acts forever at 0, and the Sleep restore is pointless. No build error,
  no validator catch. (Live-caught in Last Call: every energy change was an effect → energy gated
  nothing; `grep trait_key="energy"` and `grep 'costs = ['` both returned zero.)
- **Use `costs` to gate a resource — it works at BOTH the canvas and the choice level:**
  - **Single-exit activity → trigger `costs`.** Put `costs = [{ trait = "energy", value = N }]` under
    `[canvases.trigger]` (NOT at canvas top level — same placement rule as the trigger fields above).
    The engine checks it (`checkCostsAffordable`), **auto-dims the menu button with a "(N Energy)"
    tag**, and on click shows **"Requires N Energy (you have M)" + Back** without spending anything
    (Node-1 cost guard). It also **deducts on entry** (`deductCosts`) — so this is the spend too.
  - **Multi-intensity choice exit → per-choice `costs`.** A canvas-level `costs` is one value, so it
    can't carry a per-choice differential (a −15 single vs a −28 double). Put `costs` on EACH
    `exit_block.choices` entry instead: `costs = [{ trait = "energy", value = N }]`. The engine renders
    it as a **tier UNDER the choice's `conditions`** (the main lock): when affordable → live link;
    when not → a **plain greyed `locked-choice` rung** showing "Requires N Energy (you have M)" (no
    button). It deducts on click. This is the right tool for "main lock, then resource cost" — e.g.
    "Work the floor in less" gated on a revealing outfit (`conditions`) with an energy `costs` tier
    under it: outfit off → "needs revealing outfit"; outfit on but tired → the energy message.
- **Do NOT gate a resource with `conditions` + `locked_text_threshold`.** That makes the locked rung a
  clickable **blue toast-button** (the RTS NotifyCorruption look), not the plain greyed text, and a
  flat `conditions` AND can't show a per-tier reason (one static label). Use `costs` (above) and keep
  `conditions` for the qualitative main lock only.
- **Double-charge trap:** `costs` deducts (on entry for canvas-level, on click for choice-level) — if
  you ALSO leave an `effects` energy deduction for the same spend, the player pays **twice**. Energy
  lives in `costs` OR `effects`, never both. When converting, DELETE the `effects` energy line AND any
  energy clause you put in `conditions`.
- **Restores stay effects.** `costs` only models a positive spend; a Sleep/Shower energy *gain* is a
  normal `effects { op = "add", value = +N }`. And a gate is only meaningful if there's a restore to
  earn back through — wire the day-cycle Sleep restore (see "Day System shapes" above) alongside any
  energy gate, or the player dead-ends.

## Minor / FYI
- **`[project]` key is `id`** (the shipped LS form: `id = "late_shifts"`), not `slug`.
- **Quest cards** support a `group` key (Story-Goals crisis-variant collapse) — available if needed.
- **`guide` field** (per-canvas progression hint) is a pending schema field; set it on capstones if
  a tracker system is `include`d (see setup Phase 2+ mechanization).

## Day System shapes (day-cycle + offscreen)
- **Offscreen location** (`schema/02` §4, `doctrine/10` §5.5) — an NPC "away" label the player can't
  visit. Set `offscreen = true`, give NO `entry_from`, and put it in NO `navigation_order`. It emits
  no nav card and no portrait/hub, is exempt from the presence floor + reachability, but still
  resolves its name on the Schedule page (`getNpcLocation`):
  ```toml
  [[locations]]
  id        = "loc_npc_home"
  name      = "Across town"
  description = "The NPC's place across town. You've never been."
  offscreen = true
  ```
  Schedule an NPC's home/sleep/work block here to complete their 24h day without dead presence:
  ```toml
  [[npcs.schedules]]
  location = "loc_npc_home"
  weekdays = [0,1,2,3,4,5,6]
  start_time = "02:00"
  end_time = "17:00"
  activity = "home, off the clock"
  ```
- **Day-advance (sleep) activity** (`doctrine/04` §10.1) — the shipped shape is LS `activity_sleep`
  (`games/late_shifts/toml_phases/3_activities.toml`): a SOLO canvas (no `npc`, no `requires_npc`) at
  the player's home, `is_repeatable = true`, with a `[[canvases.trigger.schedules]]` block gating the
  sleep window (LS: 07:00–14:00, the night-shift wake cycle), and the forward jump on the EXIT block —
  `exit_block.config.time_progression_minutes = 420` (≈7h to wake) + `effects` (energy +80, hygiene
  −10). It's the router that carries the player across the clock so daytime / off-hours windows are
  reachable; without it, non-starting-phase content is dead. The clock auto-rolls the day at midnight
  (`advanceTime` → `advanceDay`) — sleep just jumps the hours within the cycle.
  - **`schedule` IS correct here** because you WANT the button only in the sleep window. The
    `lanes.md` "solo activity → no `schedule`" gotcha is the opposite case: an activity that should be
    available *whenever* its location is reachable (there a `schedule` wrongly suppresses the button).
    Sleep is window-gated by design, so it carries the schedule block.

When in doubt about a shape, read the authoritative table in `prompts_v2/schema/02_toml_schema.md`
and copy the analogous block from `games/late_shifts/toml_phases/`.
