# TOML emission gotchas — the silent build-breakers

Check this before emitting any TOML. These are the rules that fail the build (or, worse, *silently*
no-op) and that an author hits constantly. All from `prompts_v2` `schema/01`/`schema/02`, verified
against the shipped `games/late_shifts/toml_phases/`.

## Hard build-breakers
- **Inline tables must be SINGLE-LINE.** A `{ ... }` inline table wrapped across newlines breaks
  `tomllib` and fails the merge parse — the single most common build-breaker. Keep every inline
  table on one line (arrays-of-tables `[[x]]` blocks can span lines; inline `{}` cannot).
- **Declare every trait BEFORE use.** Any trait referenced anywhere — an effect, a condition, a
  sidebar item, or a `<slug>_stage` — must already exist in `[player.core_traits]` or the NPC's
  `[npcs.core_traits]`. Undeclared trait → **sidebar = hard fail**, **effect/condition = silent
  no-op** (you won't see an error; the gate just never fires). New trait in a beat ⇒ add it to
  core_traits in the same turn (and register intent in the R7 brief).
- **No per-NPC sidebar bars.** `[[sidebar_items]]` of type `trait_bar`/`trait_words` resolve against
  the *player*; there is no npc-scoped sidebar bar (it hard-fails / mis-renders). NPC progression
  (relation/arousal/stage) goes on the **Quests page** (quest cards), not the sidebar.

## Right shapes (get these exact)
- **Choice (`exit_block.choices`) fields** (`schema/02` §7.4): `text`, `targetType`
  (`"trigger"`/`"location"`/`"node"`), `target`/`locationId`/`nodeId` (per targetType), `conditions`,
  `effects`, `flagEffects`, `time_progression_minutes`, and for the locked-visible ladder:
  `show_when_locked = true`, `locked_text`, `locked_text_threshold`.
- **Stage-trait mutation uses the PLAYER namespace** (`schema/01` §6.7): advance a stage with
  `{ targetType = "player", trait = "<slug>_stage", op = "set", value = N }` — NOT `targetType="npc"`.
  Predicate side: `{ type = "trait", subject = "player", trait_key = "<slug>_stage", operator = "gte", value = N }`.
- **Effect vs predicate field names differ** (`schema/02` §16.4): effects use
  `targetType` / `npcId` / `trait` / `flag` / `op`; predicates use
  `subject` / `npc_id` / `trait_key` / `flag_key` / `operator`. Don't cross them.
- **Two condition shapes** — trigger conditions are TYPED (`{type, subject, flag_key/trait_key,
  operator, value}`); quest-card `when`/`goals` are FLAT (`{flag, op}` / `{trait, subject, npc_id,
  op, value, label}`). `schema/02` §16.5.

## Trigger-field placement (silent if wrong)
- **`substitution_only`, `max_triggers_per_day`, `requires_npc`, `npc`, `chance`, `trigger_mode`,
  `schedules`, `substitutions` all live UNDER `[canvases.trigger]`** — NOT at the `[[canvases]]`
  top level. The importer reads them from the trigger; placed at canvas level they're silently
  ignored (e.g. a misplaced `substitution_only` → the canvas wrongly shows as a normal activity
  button). Live-verified 2026-06-03.

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
  id        = "loc_sal_place"
  name      = "Sal's place"
  description = "Sal's apartment across town. You've never been."
  offscreen = true
  ```
  Schedule an NPC's home/sleep/work block here to complete their 24h day without dead presence:
  ```toml
  [[npcs.schedules]]
  location = "loc_sal_place"
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
