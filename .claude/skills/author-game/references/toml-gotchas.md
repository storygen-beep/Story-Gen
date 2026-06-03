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

When in doubt about a shape, read the authoritative table in `prompts_v2/schema/02_toml_schema.md`
and copy the analogous block from `games/late_shifts/toml_phases/`.
