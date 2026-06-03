# Continue mode — author one beat per turn

The unit of work is **the next beat in the living plan**. A beat is any story development:
`npc_intro` · `location_reveal` · `arc_escalation` · `cross_npc` · `economic` · `story_turn` ·
`capstone`. Author exactly one per turn, validate it, then stop.

**Which phase file a beat's content goes in** (set the beat's `target_phase` accordingly; when
unsure, check where `games/late_shifts/toml_phases/` put the analogous content):

| Beat type | Canvases → phase file | Also touches |
|---|---|---|
| `npc_intro` | `5_scenes.toml` (meet + Lane-1 hub) | `1_metadata_and_locations.toml` (npc + schedule) |
| `location_reveal` | `5_scenes.toml` (its hubs) | `1_metadata_and_locations.toml` (location def + lock) |
| `arc_escalation` | `5_scenes.toml` | — |
| `cross_npc` | `5_scenes.toml` | — |
| `economic` | `5_scenes.toml` (beat canvases) | `0_systems_spec.toml` (rent/phone `[settings]`), `8_phone.toml` |
| `story_turn` | `2_one_shots.toml` (one-shot event) or `5_scenes.toml` | — |
| `capstone` | `4_story_arc.toml` or `5_scenes.toml` | — |

## Resume & reconcile (every continue turn, do this first)
1. Read `games/<slug>/authoring_state.json`.
2. `python scripts/merge_toml_phases.py games/<slug> --validate` — assembles `7_final_game.toml`.
3. **Drift check:** for each beat with status `authored`/`validated`, confirm its
   `produced_canvas_ids` appear in the merged TOML. If any are missing, STOP and report — the
   ledger and the build have diverged; fix before authoring anything new. (The merge +
   `package_from_toml` build is the real safety net; this check just catches out-of-band edits.)
4. Report: where we are, the `next_up` queue, what changed since last session.

## The beat loop
1. **Propose the next beat — with ideas + options.** Take the head of `next_up` (or let the user
   pick / inject a brand-new beat). Present via AskUserQuestion: 2–4 concrete ways to play the
   beat + a recommendation. A new or reshaped beat updates the roadmap (add it to `plan` with the
   next `beat_NNNN` id; log the change in `decisions_log`).
2. **Mark active** — set the beat's `status` to `active` in the ledger.
3. **Amend structure if needed — WHOLE.** For each item in the beat's `introduces`, do the full
   amendment, never a bare reference:
   - location → definition + `entry_conditions`/`blocked_message` lock + `[[npcs.schedules]]`
     wiring + the unlock beat that reaches it (the unlock contract);
   - NPC → schedule + an OPEN on-ramp where the player first meets it (the presence floor);
   - flag → ensure a reachable setter exists before anything gates on it.
   Add each new location/npc/flag to `structure_registry`. If it's already there, that's a
   conflict — do not silently re-add.
4. **Author the canvases across the right lanes.** First read TWO things:
   - the NPC's **R7 brief** in `design_book.md` — its arc shape, lane budget, **voice spec**,
     **per-tier vocab ceiling**, and stat ladder. Honor that intent; don't re-derive or drift it.
     Size the arc to the brief's budget AND the game's `scope_mode` (from the ledger).
   - `references/lanes.md` — the four lanes (when + how to write each, verbs/narrative/fingerprints),
     beat-type→lane mapping, budgets, and the hub-vs-solo-work separation.
   An NPC arc is built *across* lanes per its shape (never Lane-1-only); keep the NPC hub (Lane 1)
   separate from any Maya-solo work activity (Lane 3 host) — pronoun test: a menu verb with no NPC
   object is solo work, not a hub item. Voice: Lane 1/2/3 RTS-flat (~30 words) at the NPC's ceiling,
   Lane 4 Tier-3. **Before emitting, check `references/toml-gotchas.md`** (declare-before-use traits,
   single-line inline tables, choice/exit_block fields, stage-mutation shape — the silent
   build-breakers). Append ONLY to the beat's `target_phase` file. Record the new canvas ids in the
   beat's `produced_canvas_ids`.
5. **Author/update the quest card** — if the beat introduces or advances a *player-facing goal*
   (an NPC arc milestone, an economic milestone, a capstone). Add/replace the `[[quest_cards]]`
   that points the player at this step, with `when` flag-gates tracking arc state so the right
   card shows now and retires when the next stage opens (the milestone-chain pattern). NOT every
   beat gets a card — repeatable ambients / flavor hubs get none (Doc 49: quests are arcs, not
   activities). See "Quest cards" below for the shape.
6. **Validate** (below). Fix red BEFORE marking done.
7. **Mark validated + persist** — set `status` to `validated`, append a `decisions_log` entry,
   write `authoring_state.json` back.
8. **Build at milestones** — run the full HTML build at end of an arc / session / on demand
   (not every beat).

## Validation (per beat — the safety net)
Run with the repo venv active (`source venv/bin/activate`), in order; emit a PASS/FAIL line for each:
1. `python scripts/merge_toml_phases.py games/<slug> --validate` — **syntax only**: assembles
   `7_final_game.toml` and `tomllib`-parses it (catches malformed TOML, e.g. multi-line inline
   tables). It does NOT check flags or references.
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev` — **the real validation**:
   schema, broken references, and flag chains, plus it builds `index.html`. This is the step that
   actually catches dangling structure, so never skip it. (`--owner-id` must be an existing user;
   on `Owner with ID ... not found`, see `setup-interview.md` Step 6.)
3. **Doctrine self-audit** — check each against what THIS beat authored (cite the doctrine in
   `COMPREHENSIVE_SYSTEM_REFERENCE.md`):
   - **reachability triad** — the canvas fires only where NPC-schedule ∩ canvas-window ∩
     player-present-and-awake overlap.
   - **dead-presence / presence floor** — every scheduled NPC has a reachable hub; no dead presence.
   - **locked-location unlock contract** — any NPC at a locked location is meetable at an open
     on-ramp and the unlock flag has a reachable setter (Cases A/B/C).
   - **`[settings]` scoping** — clothing / rent / phone keys live under `[settings]`, never bare.
   - **`is_container` swallow** — no activity / ambient / capstone attached to a container
     location (containers are pure-nav and swallow attached canvases).
   - **engine-set flag gating** — do NOT gate a canvas *trigger* on a flag the engine sets
     rather than a canvas: the rent `eviction_flag` (e.g. `bar_seized`/`rent_evicted`) and the
     `[engine.daily_tick]` flags. The flag-chain validator only recognizes *canvas-set* flags as
     gate-satisfiable, so `package_from_toml` fails with `✗ <flag>  NEVER SET`. Instead gate on a
     canvas-set flag (+ `requires_npc`/schedule for timing), or — if you truly need to react to an
     engine flag — deliver that content via a phone-thread condition (phone delivery conditions are
     not flag-chain-validated). Only `is_true` gates are checked; `is_false` guards are exempt.
   - **Quests page reflects current goals** — if this beat is a trackable goal, a `[[quest_cards]]`
     now shows it at the right time (and the prior milestone's card retires via its `when` gate).
     The Quests page is never empty and never stale (Doc 49). Repeatable ambients/flavor: no card.
   - **lane coverage vs arc shape** — the NPC's content spans the lanes its shape calls for (not
     Lane-1-only), within the brief's budget + the game's `scope_mode`, and EMPTY cells stay empty
     (peer/dating: no Lane 3; service: no Lane 2/3). The NPC hub holds only NPC-object verbs; solo
     work/chores are their own canvases (§8.2/§8.3). Each Lane 3 substitution canvas ships
     `substitution_only=true` + `max_triggers_per_day=1` + `is_repeatable=true` + a `location`
     (missing any = silent miss). Hub base opener is one constant paragraph (not tiered, D56-R1).
   - **vocab ceiling honored** — explicit content sits at the NPC's declared per-tier ceiling (R7
     brief); default to the MOST explicit reading, no euphemism drift at high tiers, lower tiers
     naturally lighter. Sex scenes ship bareback (no contraception language) so a Phase-2+ pregnancy
     retrofit can attach (`doctrine/08`, `stages/01` §5.6).
   - **traits declared before use** — any trait this beat references (effect, condition, sidebar, or
     stage) is already in `[player.core_traits]` / `[npcs.core_traits]`; an undeclared trait is a
     sidebar hard-fail or a silent effect/condition no-op (`toml-gotchas.md`).

Any FAIL → fix, re-run, then mark validated.

## Quest cards (`[[quest_cards]]` — the Quests page)
Active only when `[project].quests_engine = "v2"`. Authoritative schema: `prompts_v2` `schema/02`
§8; condition shape: §16.5; doctrine: `doctrine/04` (Doc 49 goals-vs-sidebar, Doc 50 R1–R6 card shape).

- **Where they render:** no `npc_id` → top **"Story Goals"** (the spine / main objective);
  `npc_id` set → that NPC's section.
- **Fields:** `text` (climbing copy) · `ready_text` (when goals met) · `tip` (interior line) ·
  `npc_id` · `priority` · `when` (routing — ALL must be true to show this card) · `goals`
  (🎯 to-advance bullets) · `ready_canvas` (set → 🔓 Ready frame) · `terminal = true` (✓ arc complete).
- **Condition shape is FLAT** (different from trigger conditions — no `type` discriminator):
  flag gate `{ flag = "x", op = "is_true" }`; trait gate
  `{ trait = "relation", subject = "npc", npc_id = "npc_x", op = "gte", value = 10, label = "X trust" }`.
- **Three modes:** *mechanic* (no `ready_canvas` — crossing a `goals` threshold IS the unlock);
  *capstone* (`ready_canvas` → Ready frame launches the one-shot); *terminal* (`terminal = true`).
- **Milestone chain:** one card per arc stage, each gated `when` the prior stage's flag is set and
  this stage's completion flag is not — so exactly one card shows per NPC at a time.
- Author quest cards into the beat's `target_phase` (or `5_scenes.toml`), alongside its canvases.
