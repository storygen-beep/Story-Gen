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
4. **Author the canvases** per the doctrine in `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` for
   the beat `type` (lanes, hubs, schedules, locks, settings, capstone shape). Append ONLY to the
   beat's `target_phase` file. Record the new canvas ids in the beat's `produced_canvas_ids`.
5. **Validate** (below). Fix red BEFORE marking done.
6. **Mark validated + persist** — set `status` to `validated`, append a `decisions_log` entry,
   write `authoring_state.json` back.
7. **Build at milestones** — run the full HTML build at end of an arc / session / on demand
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

Any FAIL → fix, re-run, then mark validated.
