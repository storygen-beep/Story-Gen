# The Long Summer — Test Slice (10-Day Engine-Validation Game)

> **Created 2026-04-30.**
> Sibling to `games/the_long_summer/`. Built per `28th_april_TLS_Phase2_Redesign/10_Test_Slice_10Day_Plan.md`.
> Engine-validation purpose. Not a player-facing game.

---

## What this is

A 10-in-game-day vertical slice of "The Long Summer" rebuilt against the Phase 2 doctrine (`28th_april_TLS_Phase2_Redesign/01_Repeatable_First_Doctrine.md` + `04_Scene_Cascade_Pattern.md`). Maya wakes in her bedroom on Day 1 morning of her stay at Frank's property — Prologue and arrival cinematic skipped via pre-seeded flags. Across 10 in-game days she can naturally advance Frank, Ryan, and Jake from Stage 0 → 1 → 2 of their respective arcs. Stage 3+ is force-advanceable via dev buttons for cascade verification.

The slice exists to *play* the doctrine end-to-end — to prove that hub-and-event architecture, single-node multi-group scene cascades, helper-driven stage advancement (E4), daily-tick resets (E5), maintenance-pressure decay (E2), stage-gated hint rotation (E10), stalled-stage detection (E9), and the `stage_label` sidebar (E11) all compose into a sandbox that reads differently each visit.

## What this is not

- Not a content rewrite of the existing TLS Phase 1 game. The slice is a **parallel build**; the existing `games/the_long_summer/toml_phases/` and `toml_phases_v2/` are not touched.
- Not the Prologue. Pre-seeded `prologue_complete = true` + `arrived_at_franks = true` + `first_morning_kitchen_done = true` (via the intro one-shot's exit flagEffects) skips the locked-correct novel-mode opening.
- Not a player-facing game. Hidden dev shortcuts (`dev_mode_enabled` flag) expose force-advance buttons, state snapshots, and day-skip controls that get stripped before any player slice.
- Not voice-polished. Doctrine density caps are honored (hub ≤ 300 chars body; activity 30–80 words/state; event 80–250 words; scene 80–400 words across all reveals); register polish is a follow-up pass.

## Validation surface

The §3 mechanism checklist in the plan doc is the test rubric. Twenty rows; each one a doctrine claim or shipped engine feature exercised in this slice. Pass criteria in plan §14. Exit criteria: all 20 rows pass + the natural-cadence walkthrough (plan §6) lands at end-state F2 R1 J2 within ±1 stage of expectation.

## File layout

```
games/the_long_summer_test/
├── concept.md                          (this file)
├── confabulation.md                    (registry of every invented background detail)
├── playtest_log.md                     (validation pass/fail per §3 row)
├── toml_phases/
│   ├── 0_systems_spec.toml             engine wiring (daily_tick + 7 stage_helpers) + design discipline comments
│   ├── 1_metadata_and_locations.toml   project/time/player (with stage traits)/6 NPCs/14 locations/sidebar items/rent
│   ├── 2_one_shots.toml                event_test_slice_intro (the seeding canvas)
│   ├── 3_activities.toml               11 activities (hub-launchable repeatables; image rotation, no block_pool)
│   ├── 4_story_arc.toml                [story_arc.hints] with 12 stage-gated templates (E10) + stall message (E9)
│   ├── 4b_stage_transitions.toml       transition canvases that explicitly write <slug>_stage (helper-derived advancement, see §12.1)
│   ├── 5_hubs_and_scenes.toml          10 hubs + 8 scenes (the heaviest authoring; cascades per Doc 04)
│   ├── 6_dev_shortcuts.toml            9 dev canvases (force-advance, force-catch, day-skip, snapshot)
│   └── 7_final_game.toml               concat of 0–6 (the file passed to package_from_toml)
└── output/
    └── index.html                      compiled output
```

## Build

```sh
cd /Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django
source venv/bin/activate
python manage.py package_from_toml \
  --file games/the_long_summer_test/toml_phases/7_final_game.toml \
  --owner-id <uuid> \
  --output games/the_long_summer_test/output \
  --dev \
  --video-folder games/the_long_summer/output/videos
```

`--dev` enables sidebar stat-adjustment controls (independent of the in-game `dev_mode_enabled` flag — both useful in playtest).
