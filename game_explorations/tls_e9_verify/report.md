# tls_e9_verify — Exploration Report

Generated: 2026-05-16T12:26:14.475Z
Source URL: file:///tmp/tls_phase_e9/index.html

## Session Summary

- Sessions run: 1
- Total wall-clock: 9m 40s
- Total clicks: 0
- Total choices explored: 0
- Unique states seen: 27
- Unexplored frontier (queued for next session): 0
- Endings reached: 0 (use `live.js mark-ending <passage>` to record a terminal passage)

## Engine
Detected engine: **sugarcube** v(revive:eval),(function(){var e=this.prerelease?"-"+this.prerelease:"";return this.title+" (v"+this.major+"."+this.minor+"."+this.patch+e+")"})

## Variable schema (labeled at report time)

### player_stat (8)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `player.core_traits.energy` | number | -41..0 | 8 | high |
| `player.core_traits.fitness` | number | 0..0 | 0 | high |
| `player.core_traits.beauty` | number | 0..0 | 0 | high |
| `player.core_traits.corruption` | number | 0..24 | 10 | high |
| `player.core_traits.money` | number | 0..0 | 0 | high |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.corruption` | number | 0..9 | 5 | high |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.corruption` | number | 0..0 | 0 | high |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.corruption` | number | 0..4 | 2 | high |

### time (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `game_state.time_state.day` | number | 1..3 | 0 | high |

### flag (70)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `flags.prologue_at_bed` | boolean | false, true | 1 | high |
| `flags.prologue_saw_them` | boolean | false, true | 1 | high |
| `flags.prologue_crossed_line` | boolean | false, true | 1 | high |
| `flags.prologue_complete` | boolean | false, true | 1 | high |
| `flags.arrived_at_franks` | boolean | false, true | 1 | high |
| `flags.first_morning_kitchen_done` | boolean | false, true | 1 | high |
| `flags.slice_started` | boolean | false, true | 1 | high |
| `flags.hired_at_diner` | boolean | false | 0 | high |
| `flags.first_t0_shift_done` | boolean | false | 0 | high |
| `flags.group_settled_in` | boolean | false | 0 | high |
| `flags.first_sunday_passed` | boolean | false | 0 | high |
| `flags.first_rent_paid` | boolean | false | 0 | high |
| `flags.attended_church_this_week` | boolean | false | 0 | high |
| `flags.anon_dm_seen` | boolean | false, true | 1 | high |
| `flags.ryan_first_date_done` | boolean | false, true | 1 | high |
| `flags.jake_caught_drawing_done` | boolean | false, true | 1 | high |
| `flags.frank_caught` | boolean | false, true | 4 | high |
| `flags.frank_restrict_declared` | boolean | false, true | 1 | high |
| `flags.frank_cracked` | boolean | false, true | 4 | high |
| `flags.frank_keep_route_romantic` | boolean | false | 0 | high |
| `flags.frank_keep_route_arrangement` | boolean | false | 0 | high |
| `flags.frank_keep_route_rupture` | boolean | false | 0 | high |
| `flags.frank_keep_route_power_inverted` | boolean | false | 0 | high |
| `flags.frank_office_first_sex_done` | boolean | false | 0 | high |
| `flags.frank_invited_to_bedroom` | boolean | false | 0 | high |
| `flags.frank_bedroom_first_done` | boolean | false | 0 | high |
| `flags.frank_sleepover_done` | boolean | false, true | 1 | high |
| `flags.diana_confronted` | boolean | false, true | 1 | high |
| `flags.frank_branch_kicked_out` | boolean | false, true | 1 | high |
| `flags.frank_branch_brought_in` | boolean | false, true | 1 | high |
| `flags.ryan_help_tier_open` | boolean | false | 0 | high |
| `flags.ryan_partner_open` | boolean | false | 0 | high |
| `flags.ryan_big_deal_closed` | boolean | false | 0 | high |
| `flags.ryan_beach_proposal` | boolean | false | 0 | high |
| `flags.ryan_keep_route_yes_engaged` | boolean | false | 0 | high |
| `flags.ryan_keep_route_not_yet` | boolean | false | 0 | high |
| `flags.ryan_keep_route_no_withdrawn` | boolean | false | 0 | high |
| `flags.jake_first_glance_noticed` | boolean | false | 0 | high |
| `flags.jake_peek_draw_revealed` | boolean | false | 0 | high |
| `flags.jake_tease_open` | boolean | false | 0 | high |
| … | … | … | … | and 30 more |

### scalar (96)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `player.core_traits.hygiene` | number | 0..0 | 0 | low |
| `player.core_traits.calculation` | number | 0..0 | 0 | low |
| `player.core_traits.rep_church` | number | 0..0 | 0 | low |
| `player.core_traits.rep_road` | number | 0..0 | 0 | low |
| `player.core_traits.rep_college` | number | 0..0 | 0 | low |
| `player.core_traits.npc_ryan_stage` | number | 0..0 | 0 | low |
| `player.core_traits.npc_jake_stage` | number | 0..0 | 0 | low |
| `player.core_traits.ryan_help_count` | number | 0..0 | 0 | low |
| `player.core_traits.jake_peek_count` | number | 0..0 | 0 | low |
| `player.core_traits.lean_by_desk_count` | number | 0..0 | 0 | low |
| `player.core_traits.sex_stage` | number | 0..0 | 0 | low |
| `player.core_traits.sex_finisher_type` | number | 0..0 | 0 | low |
| `player.core_traits.sex_reactions` | number | 0..0 | 0 | low |
| `player.core_traits.anal_active` | number | 0..0 | 0 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.love` | number | 0..0 | 0 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.trust` | number | -10..0 | 2 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.arousal` | number | 0..19 | 8 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.love` | number | 0..6 | 2 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.trust` | number | 0..6 | 2 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.arousal` | number | 0..0 | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.love` | number | 0..0 | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.trust` | number | 0..0 | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.arousal` | number | 0..6 | 2 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.core_traits.awareness` | number | 0..9 | 6 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.core_traits.trust` | number | 0..0 | 0 | low |
| `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.core_traits.trust` | number | 0..0 | 0 | low |
| `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.core_traits.trust` | number | 0..0 | 0 | low |
| `game_state.time_state.current_hour` | number | 6..17 | 6 | low |
| `game_state.time_state.current_minute` | number | 0..55 | 13 | low |
| `game_state.time_state.current_week` | number | 1..1 | 0 | low |
| `game_state.rent_state.last_paid_week` | number | 1..1 | 0 | low |
| `game_state.rent_state.warnings` | number | 0..0 | 0 | low |
| `last_day_snapshot.player::hygiene` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:love` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:trust` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:arousal` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:515edc7f-8ac8-4870-918c-b29fbf209f22:love` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:515edc7f-8ac8-4870-918c-b29fbf209f22:trust` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:515edc7f-8ac8-4870-918c-b29fbf209f22:arousal` | number | 0..0 | 0 | low |
| `last_day_snapshot.npc:b89cca9a-be70-4592-8d47-007a222643ae:love` | number | 0..0 | 0 | low |
| … | … | … | … | and 56 more |

### string (48)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `last_game_passage` | string | `Start`, `StartingCanvas_event`, `Canvas_scene_livingr` | 22 | low |
| `player.name` | string | `Maya` | 0 | low |
| `player.portrait` | string | `maya.jpg` | 0 | low |
| `player.current_location` | string | `` | 0 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.name` | string | `Frank` | 0 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.portrait` | string | `frank.jpg` | 0 | low |
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.relationship` | string | `` | 0 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.name` | string | `Ryan` | 0 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.portrait` | string | `ryan.jpg` | 0 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.relationship` | string | `` | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.name` | string | `Jake` | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.portrait` | string | `jake.jpg` | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.relationship` | string | `` | 0 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.name` | string | `Diana` | 0 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.portrait` | string | `diana.jpg` | 0 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.relationship` | string | `` | 0 | low |
| `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.name` | string | `Marge` | 0 | low |
| `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.portrait` | string | `marge.jpg` | 0 | low |
| `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.relationship` | string | `` | 0 | low |
| `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.name` | string | `Cookie` | 0 | low |
| `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.portrait` | string | `cookie.jpg` | 0 | low |
| `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.relationship` | string | `` | 0 | low |
| `game_state.current_canvas` | string | ``, `2cbdbd7a-79d4-48bc-8`, `5f73424b-a48e-4a6e-9` | 20 | low |
| `game_state.time_state.current_day` | string | `Monday`, `Wednesday` | 0 | low |
| `game_state.trigger_history.2cbdbd7a-79d4-48bc-8e7c-26b2f59e0d8e.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.current_node` | string | `e49ad01a-b4b9-4a3c-b`, `e3ed1eb7-931e-4b93-a`, `5d97efdf-4938-477b-b` | 21 | low |
| `game_state.trigger_history.5f73424b-a48e-4a6e-937a-5767eacace27.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Living room — the catch.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.cd9ce6d1-24f1-41cf-ae8a-131c0a3cc353.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Hallway — Frank can't keep pretending.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.f9e7f84c-4a6e-421b-93b4-4f86d8883ebe.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Frank's bedroom — first night.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.b4e9d306-c29c-43bd-ab30-2ae5ca995d60.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Frank's bedroom — you stay the night.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.523fa7da-cc1c-4061-a99e-2893a0a94a17.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Living room — Diana knows.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.b3230183-9e5b-4eb6-b16b-3bcbb0007d75.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Kitchen — Frank passes the door while you're making tea.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.trigger_history.72fe67c5-4976-4507-811f-5c954c29fcc1.dayKey` | string | `1:Wednesday` | 0 | low |
| `game_state.activity_trigger_history.Maya's room — a DM from a stranger.dayKey` | string | `1:Wednesday` | 0 | low |
| … | … | … | … | and 8 more |

### misc (8)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.schedule` | object | — | 0 | low |
| `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.schedule` | object | — | 0 | low |
| `npcs.b89cca9a-be70-4592-8d47-007a222643ae.schedule` | object | — | 0 | low |
| `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.schedule` | object | — | 0 | low |
| `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.schedule` | object | — | 0 | low |
| `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.schedule` | object | — | 0 | low |
| `game_state.visited_locations` | object | — | 0 | low |
| `game_state.visited_nodes` | object | — | 0 | low |

## NPCs detected

_No NPCs detected yet._

## Body / appearance traits

_No body/appearance variables detected._

## Choice type distribution

_No choices classified yet._

## Economy

- Price-labeled choices observed: 0
- Money income events: 0
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **daykey** (23): `game_state.trigger_history.2cbdbd7a-79d4-48bc-8e7c-26b2f59e0d8e.dayKey`, `game_state.trigger_history.5f73424b-a48e-4a6e-937a-5767eacace27.dayKey`, `game_state.activity_trigger_history.Living room — the catch.dayKey`, `game_state.trigger_history.cd9ce6d1-24f1-41cf-ae8a-131c0a3cc353.dayKey`, `game_state.activity_trigger_history.Hallway — Frank can't keep pretending.dayKey`, `game_state.trigger_history.f9e7f84c-4a6e-421b-93b4-4f86d8883ebe.dayKey`, …
- **daycount** (23): `game_state.trigger_history.2cbdbd7a-79d4-48bc-8e7c-26b2f59e0d8e.dayCount`, `game_state.trigger_history.5f73424b-a48e-4a6e-937a-5767eacace27.dayCount`, `game_state.activity_trigger_history.Living room — the catch.dayCount`, `game_state.trigger_history.cd9ce6d1-24f1-41cf-ae8a-131c0a3cc353.dayCount`, `game_state.activity_trigger_history.Hallway — Frank can't keep pretending.dayCount`, `game_state.trigger_history.f9e7f84c-4a6e-421b-93b4-4f86d8883ebe.dayCount`, …
- **set** (19): `flags_meta.prologue_at_bed.set_day`, `flags_meta.prologue_saw_them.set_day`, `flags_meta.prologue_crossed_line.set_day`, `flags_meta.prologue_complete.set_day`, `flags_meta.arrived_at_franks.set_day`, `flags_meta.first_morning_kitchen_done.set_day`, …
- **frank** (16): `flags.frank_caught`, `flags.frank_restrict_declared`, `flags.frank_cracked`, `flags.frank_keep_route_romantic`, `flags.frank_keep_route_arrangement`, `flags.frank_keep_route_rupture`, …
- **total** (12): `game_state.trigger_history.2cbdbd7a-79d4-48bc-8e7c-26b2f59e0d8e.total`, `game_state.trigger_history.5f73424b-a48e-4a6e-937a-5767eacace27.total`, `game_state.trigger_history.cd9ce6d1-24f1-41cf-ae8a-131c0a3cc353.total`, `game_state.trigger_history.f9e7f84c-4a6e-421b-93b4-4f86d8883ebe.total`, `game_state.trigger_history.b4e9d306-c29c-43bd-ab30-2ae5ca995d60.total`, `game_state.trigger_history.523fa7da-cc1c-4061-a99e-2893a0a94a17.total`, …
- **npc** (11): `player.core_traits.npc_ryan_stage`, `player.core_traits.npc_jake_stage`, `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:love`, `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:trust`, `last_day_snapshot.npc:35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc:arousal`, `last_day_snapshot.npc:515edc7f-8ac8-4870-918c-b29fbf209f22:love`, …
- **jake** (11): `player.core_traits.jake_peek_count`, `flags.jake_caught_drawing_done`, `flags.jake_first_glance_noticed`, `flags.jake_peek_draw_revealed`, `flags.jake_tease_open`, `flags.jake_caught`, …
- **ryan** (9): `player.core_traits.ryan_help_count`, `flags.ryan_first_date_done`, `flags.ryan_help_tier_open`, `flags.ryan_partner_open`, `flags.ryan_big_deal_closed`, `flags.ryan_beach_proposal`, …
- **name** (7): `player.name`, `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.name`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.name`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.name`, `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.name`, `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.name`, …
- **portrait** (7): `player.portrait`, `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.portrait`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.portrait`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.portrait`, `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.portrait`, `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.portrait`, …
- **current** (7): `player.current_location`, `game_state.current_canvas`, `game_state.time_state.current_hour`, `game_state.time_state.current_minute`, `game_state.time_state.current_day`, `game_state.time_state.current_week`, …
- **trust** (6): `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.trust`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.trust`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.trust`, `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.core_traits.trust`, `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.core_traits.trust`, `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.core_traits.trust`
- **schedule** (6): `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.schedule`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.schedule`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.schedule`, `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.schedule`, `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.schedule`, `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.schedule`
- **relationship** (6): `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.relationship`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.relationship`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.relationship`, `npcs.b5943bf7-e300-480c-8c4d-b3b6cdc12107.relationship`, `npcs.5235a839-f585-4fec-8de9-2d3d0ebc188a.relationship`, `npcs.f7d3cce2-972d-4495-949c-766915c5c6f0.relationship`
- **talked** (5): `flags.talked_to_ryan_today`, `flags.talked_to_jake_today`, `flags.talked_to_diana_today`, `flags.talked_to_marge_today`, `flags.talked_to_cookie_today`
- **corruption** (4): `player.core_traits.corruption`, `npcs.35da86e0-e4f5-4c85-b8f1-fb7f3211fdcc.core_traits.corruption`, `npcs.515edc7f-8ac8-4870-918c-b29fbf209f22.core_traits.corruption`, `npcs.b89cca9a-be70-4592-8d47-007a222643ae.core_traits.corruption`
- **prologue** (4): `flags.prologue_at_bed`, `flags.prologue_saw_them`, `flags.prologue_crossed_line`, `flags.prologue_complete`
- **first** (4): `flags.first_morning_kitchen_done`, `flags.first_t0_shift_done`, `flags.first_sunday_passed`, `flags.first_rent_paid`
- **phase** (4): `flags.phase_2_bar_unlocked`, `flags.phase_2_fair_week_active`, `flags.phase_2_football_season_started`, `flags.phase_2_church_interior_unlocked`
- **rep** (3): `player.core_traits.rep_church`, `player.core_traits.rep_road`, `player.core_traits.rep_college`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-05-16T12:16:34.602Z | 9m 40s | 0 | 0 | 27 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **505**
- Observed edges during play: **0** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **0** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **0**.
- Coverage: **0.00%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 23

### Playable-content partition
- Passages defined in source: **267** (0 tagged `wip`, 0 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **267**.
- Distinct passages visited at least once: **17** — playable-passage coverage: **6.4%**.

### Static edge kinds
| kind | count |
|---|---|
| button | 198 |
| link | 179 |
| wiki | 126 |
| goto | 2 |

## See also
- `variable_profile.json` — raw statistical evidence, no labels
- `variable_schema.json` — variables with applied labels + confidence
- `mechanics.md` — design patterns observed
- `coverage.md` — frontier + explored counts
- `static_graph.json` — every navigation edge parsed from passage source (M2, written at startup as of M6.1)
- `choice_graph.json` — observed edges with per-edge effect aggregates (M2)
- `variable_index.json` — every game variable → passages/edges that `<<set>>`/`<<unset>>` it, with enclosing `<<if>>` gates (M6.1)
- `passage_catalog.json` — every passage with raw source + tags (M1)
- `scene_bodies.jsonl` — full rendered body per unique state (M1)
- `initial_state.json` — pristine pre-Phase-0a snapshot (M1)
- `state_timeline.jsonl` — per-observation state + full diff values (M1)
- `engine_config.json` — SugarCube Config/Setting/version/save-caps + State.history shape + Story IFID (M3)
- `sidebar_snapshots.jsonl` — sidebar panel text captures across Phase 0 probes + passive mid-game changes (M4)