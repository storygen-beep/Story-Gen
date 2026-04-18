# shady-deals — Exploration Report

Generated: 2026-04-18T09:36:11.759Z
Source URL: https://mopoga.com/shady-deals

## Session Summary

- Sessions run: 2
- Total wall-clock: 26m 11s
- Total clicks: 30
- Total choices explored: 30
- Unique states seen: 148
- Unexplored frontier (queued for next session): 0
- Endings reached: 0 (use `live.js mark-ending <passage>` to record a terminal passage)

## Engine
Detected engine: **sugarcube** v(revive:eval),(function(){var prerelease=this.prerelease?"-".concat(this.prerelease):"";return"".concat(this.title," (v").concat(this.major,".").concat(this.minor,".").concat(this.patch).concat(prerelease,")")})

## Variable schema (labeled at report time)

### player_stat (5)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `energy` | number | 6..6 | 0 | high |
| `money` | number,object | 0..1000 | 4 | high |
| `reputation` | number | -34..0 | 1 | high |
| `enemy_1.hp` | number | 10..24 | 3 | high |
| `target.hp` | number | 10..19 | 2 | high |

### body (7)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `discard` | object | — | 0 | medium |
| `body_1` | string | `1` | 0 | medium |
| `body_2` | string | `2` | 0 | medium |
| `body_3` | string | `3` | 0 | medium |
| `hair_page` | number | 0..0 | 0 | medium |
| `boobs_grab_yapping` | object | — | 0 | medium |
| `pc_haircolor` | string | `brunette`, `redhead` | 2 | medium |

### item (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `enemy_1.photo` | string | `img/photos/gangers/1` | 0 | medium |
| `target.photo` | string | `img/photos/gangers/1` | 0 | medium |

### flag (290)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `lvlup` | boolean | false | 0 | high |
| `pc_lips_piercing` | boolean | false | 0 | high |
| `pc_nipple_piercing` | boolean | false | 0 | high |
| `pc_navel_piercing` | boolean | false | 0 | high |
| `gold_digger_tools` | boolean | false | 0 | high |
| `gangs_base` | boolean | false | 0 | high |
| `gangs_met` | number | 0..0 | 0 | medium |
| `mafia_base` | boolean | false | 0 | high |
| `mafia_met` | number | 0..0 | 0 | medium |
| `cartel_base` | boolean | false | 0 | high |
| `cartel_met` | number | 0..0 | 0 | medium |
| `bikers_met` | number | 0..0 | 0 | medium |
| `hackers_met` | number | 0..0 | 0 | medium |
| `strange_note_1` | boolean | false, true | 1 | high |
| `strange_note_2` | boolean | false | 0 | high |
| `strange_note_3` | boolean | false | 0 | high |
| `strange_note_4` | boolean | false | 0 | high |
| `met_mechanic` | number | 0..0 | 0 | medium |
| `ring_information` | boolean | false | 0 | high |
| `autoshop_information` | boolean | false | 0 | high |
| `hackers_crypto_note` | boolean | false | 0 | high |
| `outskirts_checkpoint_known` | boolean | false | 0 | high |
| `gangers_accomplices_tutorial` | boolean | false | 0 | high |
| `gangers_hiring_end` | boolean | false | 0 | high |
| `do_it_anyway` | boolean | false | 0 | high |
| `dm_cap_too_much` | boolean | false | 0 | high |
| `bar_moonshine_sold` | boolean | false | 0 | high |
| `outskirts_trade` | boolean | false | 0 | high |
| `downtown_bribe` | boolean | false, true | 2 | high |
| `suburbs_bribe` | boolean | false | 0 | high |
| `race_active` | boolean | true | 0 | high |
| `mafia_blackjack` | boolean | true | 0 | high |
| `police_connections` | boolean | false | 0 | high |
| `harbor_gangbang` | boolean | false | 0 | high |
| `distributor_standoff` | boolean | false | 0 | high |
| `distributor_lewd` | boolean | false | 0 | high |
| `distributor_daily_sex` | boolean | false | 0 | high |
| `gangs_leaders_daily_sex` | boolean | false | 0 | high |
| `news_milestone_1` | boolean | false | 0 | high |
| `news_milestone_2` | boolean | false | 0 | high |
| … | … | … | … | and 250 more |

### scalar (585)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `deckCount` | number | 1..1 | 0 | low |
| `bet` | number | 0..0 | 0 | low |
| `pot` | number | 0..0 | 0 | low |
| `autosave_cd_setting` | number | 3..3 | 0 | low |
| `autosave_cd` | number | 2..3 | 1 | low |
| `pc_photo_index` | number | 0..0 | 0 | low |
| `daily_heal` | number | 8..8 | 0 | low |
| `cun_base` | number | 3..6 | 1 | low |
| `cun_mod_boss` | number | 0..0 | 0 | low |
| `cun_scout_mod` | number | 0..0 | 0 | low |
| `cun_arousal_mod` | number | 0..0 | 0 | low |
| `cun` | number | 3..6 | 1 | low |
| `bonus_charm_style` | number | 0..0 | 0 | low |
| `bonus_charm_slut` | number | 0..0 | 0 | low |
| `charm_mod_boss` | number | 0..0 | 0 | low |
| `charm_arousal_mod` | number | 0..0 | 0 | low |
| `charm_sex_buff` | number | 0..0 | 0 | low |
| `charm_base` | number | 3..3 | 0 | low |
| `charm` | number | 3..3 | 0 | low |
| `base_energy` | number | 6..6 | 0 | low |
| `energy_mod_boss` | number | 0..0 | 0 | low |
| `energy_mod_car` | number | 0..0 | 0 | low |
| `stam` | number | 0..6 | 3 | low |
| `combat_base` | number | 3..4 | 1 | low |
| `combat_mod_boss` | number | 0..0 | 0 | low |
| `combat_mod_training` | number | 0..0 | 0 | low |
| `combat_arousal_mod` | number | 0..0 | 0 | low |
| `combat` | number | 3..4 | 1 | low |
| `health_base` | number | 30..30 | 0 | low |
| `health_traits_mod` | number | 0..0 | 0 | low |
| `health_training_mod` | number | 0..0 | 0 | low |
| `p_hp_max` | number | 30..30 | 0 | low |
| `p_hp` | number | 0..30 | 5 | low |
| `combat_stamina_base` | number | 100..100 | 0 | low |
| `combat_stamina` | number | 100..100 | 0 | low |
| `stream_stamina` | number | 120..120 | 0 | low |
| `arousal` | number | 0..0 | 0 | low |
| `p_depravity` | number | 5..5 | 0 | low |
| `heat` | number | 0..0 | 0 | low |
| `gangs_heat` | number | 0..0 | 0 | low |
| … | … | … | … | and 545 more |

### string (119)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `heat_difficulty` | string | `Default` | 0 | low |
| `hotkey_home` | string | `` | 0 | low |
| `hotkey_old_downtown` | string | `` | 0 | low |
| `hotkey_suburbs` | string | `` | 0 | low |
| `hotkey_city_center` | string | `` | 0 | low |
| `hotkey_harbor` | string | `` | 0 | low |
| `hotkey_outskirts` | string | `` | 0 | low |
| `arousal_effects_setting` | string | `On` | 0 | low |
| `arousal_text_setting` | string | `On` | 0 | low |
| `boss_name` | string | `Boss` | 0 | low |
| `adolesence` | string | ``, `Bully` | 1 | low |
| `first_crime` | string | ``, `Robbery`, `Theft` | 3 | low |
| `last_crime` | string | ``, `Burglary` | 1 | low |
| `dt_indoors` | string | `playful` | 0 | low |
| `dt_outdoors` | string | `playful` | 0 | low |
| `dt_group` | string | `playful` | 0 | low |
| `dt_lesbian` | string | `playful` | 0 | low |
| `dt_prostitution` | string | `playful` | 0 | low |
| `player_text` | string | `player_pink` | 0 | low |
| `rough_sex_attitude` | string | `ok` | 0 | low |
| `weapon_equipped` | string | `Nothing` | 0 | low |
| `city_name` | string | `Default Name`, `Kickback Keys` | 1 | low |
| `nc_name` | string | `Swaying Bazongas` | 0 | low |
| `boss_type` | string | `Bandit Boss` | 0 | low |
| `band_name` | string | `Band`, `Ring`, `Just Another Gang` | 2 | low |
| `original_band_name` | string | `Band` | 0 | low |
| `band_type` | string | `Street Gang` | 0 | low |
| `right_hand.name` | string | `` | 0 | low |
| `right_hand.nickname` | string | `` | 0 | low |
| `chauffeur_name` | string | `` | 0 | low |
| `chauffeur_nickname` | string | `` | 0 | low |
| `sabo_type` | string | `` | 0 | low |
| `heist_type` | string | `` | 0 | low |
| `equip.top.item` | string | `Black T-shirt` | 0 | low |
| `equip.top.slot` | string | `top` | 0 | low |
| `equip.top.pic` | string | `<img src=img/clothes` | 0 | low |
| `equip.bottom.item` | string | `Jeans` | 0 | low |
| `equip.bottom.slot` | string | `bottom` | 0 | low |
| `equip.bottom.pic` | string | `<img src=img/clothes` | 0 | low |
| `equip.feet.item` | string | `Sneakers` | 0 | low |
| … | … | … | … | and 79 more |

### misc (189)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `deck` | object | — | 0 | low |
| `player` | object | — | 0 | low |
| `dealer` | object | — | 0 | low |
| `gameDate` | object | — | 0 | low |
| `drugs_shipment` | object | — | 0 | low |
| `steroids_shipment` | object | — | 0 | low |
| `aphrodisiac_shipment` | object | — | 0 | low |
| `stolen_goods_shipment` | object | — | 0 | low |
| `stolen_goods_shipment_x3` | object | — | 0 | low |
| `stolen_goods_shipment_x5` | object | — | 0 | low |
| `jewelry_shipment` | object | — | 0 | low |
| `jewelry_shipment_x3` | object | — | 0 | low |
| `jewelry_shipment_x5` | object | — | 0 | low |
| `electronic_shipment` | object | — | 0 | low |
| `moonshine_shipment` | object | — | 0 | low |
| `weapons_shipment` | object | — | 0 | low |
| `weapons_shipment_x3` | object | — | 0 | low |
| `weapons_shipment_x5` | object | — | 0 | low |
| `improvised_weapons_shipment` | object | — | 0 | low |
| `improvised_weapons_shipment_x3` | object | — | 0 | low |
| `improvised_weapons_shipment_x5` | object | — | 0 | low |
| `melee_shipment` | object | — | 0 | low |
| `melee_shipment_x3` | object | — | 0 | low |
| `melee_shipment_x5` | object | — | 0 | low |
| `p_traits` | object | — | 0 | low |
| `p_inv` | object | — | 0 | low |
| `garage_inv` | object | — | 0 | low |
| `stash` | object | — | 0 | low |
| `p_range` | object | — | 0 | low |
| `p_melee` | object | — | 0 | low |
| `p_craft` | object | — | 0 | low |
| `warehouse_upgrades` | object | — | 0 | low |
| `warehouse_inv` | object | — | 0 | low |
| `band_events` | object | — | 0 | low |
| `p_wardrobe` | object | — | 0 | low |
| `trait_rich` | object | — | 0 | low |
| `job_rich` | object | — | 0 | low |
| `job_fem_rich` | object | — | 0 | low |
| `trait_downtown` | object | — | 0 | low |
| `job_downtown` | object | — | 0 | low |
| … | … | … | … | and 149 more |

## NPCs detected

_No NPCs detected yet._

## Body / appearance traits

- `discard`
- `body_1`
- `body_2`
- `body_3`
- `hair_page`
- `boobs_grab_yapping`
- `pc_haircolor`

Transitions observed: 2
- `pc_haircolor`: `"brunette"` → `"redhead"` at `CharGen`
- `pc_haircolor`: `"redhead"` → `"brunette"` at `QuickStart Menu`

## Choice type distribution

| type | count |
|---|---|
| branch | 1 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 2
- Money expense events: 2

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **nc** (45): `nc_striptease_cd`, `nc_name`, `nc_tax`, `nc_tax_upgrades`, `nc_pop`, `nc_pop_raise`, …
- **gig** (40): `gig_rep_scale`, `gig_rep_scale_second`, `gig_needed_item`, `gig_item_amount`, `gig_item_reward`, `gig_item_type`, …
- **stat** (33): `stat_money`, `stat_money_used`, `stat_dmoney`, `stat_dmoney_used`, `stat_heat`, `stat_burglary`, …
- **brothel** (29): `brothel`, `brothel_sluts_max`, `brothel_sluts`, `brothel_pop`, `brothel_clients_amount`, `brothel_quality_mods`, …
- **band** (23): `band_strength`, `band_strength_bonus`, `band_war_progress`, `band_war_needed_progress`, `band_war_max_progress`, `band_war_progress_speed`, …
- **bleach** (21): `bleach_cd`, `bleach_combat`, `bleach_cun`, `bleach_charm`, `bleach_pickpocket`, `bleach_burglary`, …
- **crypto** (19): `crypto_trait_progress`, `crypto_cvc`, `crypto_ctc`, `crypto_gbt`, `crypto_ksh`, `crypto_rfc`, …
- **moonshine** (18): `moonshine_shipment`, `moonshine_trailer`, `moonshine_mats`, `moonshine_farmers`, `moonshine_farmers_max`, `moonshine_prod_upgrade_1`, …
- **downtown** (17): `downtown_bribe`, `downtown_rep`, `downtown_landlord`, `downtown_arousal_event`, `downtown_duo_cd`, `downtown_loot`, …
- **bikers** (16): `bikers_heat`, `bikers_met`, `bikers_heat_event`, `bikers_weapons_refresh`, `bikers_gunparts`, `bikers_handguns`, …
- **enemy** (16): `enemy_sabo`, `combat_cooldowns.enemy_1`, `combat_cooldowns.enemy_2`, `combat_cooldowns.enemy_3`, `enemy_1`, `enemy_2`, …
- **heat** (15): `heat_difficulty`, `heat`, `heat_first`, `heat_cw_block`, `heat_racket_block`, `heat_gangs_entrance`, …
- **mafia** (15): `mafia_heat`, `mafia_base`, `mafia_met`, `mafia_blackjack`, `mafia_heat_event`, `mafia_wreck`, …
- **suburbs** (15): `suburbs_bribe`, `suburbs_duo_cd`, `suburbs_burglary_comments`, `suburbs_duo_stole_something`, `suburbs`, `suburbs_cars`, …
- **gangs** (14): `gangs_heat`, `gangs_base`, `gangs_met`, `gangs_leaders_daily_sex`, `gangs_heat_event`, `gangs_racketeer`, …
- **harbor** (13): `harbor_gangbang`, `harbor_stealing_from_cartel`, `harbor`, `harbor_spot_captured`, `harbor_spot_grace`, `harbor_spot_attacked`, …
- **gold** (12): `gold_digger_tools`, `gold_digger`, `gold_digger_cd`, `gold_digger_sold`, `gold_rep_mod`, `gold_gd_price`, …
- **outskirts** (12): `outskirts_checkpoint_known`, `outskirts_trade`, `outskirts_roadblock`, `outskirts_cars`, `outskirts_checkpoint_captured`, `outskirts_checkpoint_grace`, …
- **gd** (12): `gd_weapon_bought`, `gd_shipment_bought`, `gd_shipment_type`, `gd_shipment_amount`, `gd_shipment_price`, `gd_weapon_type`, …
- **scrap** (12): `scrap_shack`, `scrap_hands_amount`, `scrap_hand_productivity`, `scrap_shack_gunsmith`, `scrap_shack_gun_workbench_upgrade`, `scrap_shack_gunparts_upgrade_1`, …

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-18T08:07:45.496Z | 11m 45s | 8 | 8 | 28 | no |
| 2 | 2026-04-18T09:21:45.301Z | 14m 26s | 22 | 22 | 120 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **2120**
- Observed edges during play: **22** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **39** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **5**.
- Coverage: **1.84%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 127

### Playable-content partition
- Passages defined in source: **680** (0 tagged `wip`, 3 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **677**.
- Distinct passages visited at least once: **111** — playable-passage coverage: **16.4%**.

### Static edge kinds
| kind | count |
|---|---|
| link | 1582 |
| goto | 314 |
| include | 181 |
| button | 41 |
| wiki | 2 |

### Unresolved static targets (9)
Targets that appear in passage source but don't resolve to a known passage — typically dynamic expressions like `` <<goto `func()`>> `` or referenced-but-never-defined passages.

- `Adolesence info " + State.variables.adolesence + "`
- `Crime info " + State.variables.first_crime + "`
- `Display Carrots`
- `Downtown Tenants Search`
- `Hair Color " + State.variables.pc_haircolor + "`
- `Harborr`
- `Last Crime info " + State.variables.last_crime + "`
- `Residential Complex`
- `Tenant`

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