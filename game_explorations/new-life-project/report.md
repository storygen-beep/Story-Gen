# new-life-project — Exploration Report

Generated: 2026-04-19T07:33:53.043Z
Source URL: https://mopoga.com/new-life-project

## Session Summary

- Sessions run: 2
- Total wall-clock: 30m 17s
- Total clicks: 220
- Total choices explored: 220
- Unique states seen: 214
- Unexplored frontier (queued for next session): 0
- Endings reached: 0 (use `live.js mark-ending <passage>` to record a terminal passage)

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `money` | number | 0..508 | 22 | high |
| `strength` | number | 0..0 | 0 | high |

### npc_stat (6)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `chloeLove` | number | 0..0 | 0 | high |
| `lilyLove` | number | 0..0 | 0 | high |
| `broLove` | number | 0..0 | 0 | high |
| `dadLove` | number | 0..0 | 0 | high |
| `zackLove` | number | 0..0 | 0 | high |
| `caineLove` | number | 0..0 | 0 | high |

### body (4)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `discard` | object | — | 0 | medium |
| `makeupDone` | number | 0..0 | 0 | medium |
| `hairDone` | number | 0..0 | 0 | medium |
| `makeupAmount` | number | 5..5 | 0 | medium |

### time (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `day` | number | 1..8 | 7 | high |

### flag (89)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `sanity` | boolean | true | 0 | high |
| `kidnapQuest` | boolean | false | 0 | high |
| `facilityQuest` | boolean | false | 0 | high |
| `mansion` | boolean | false | 0 | high |
| `mansionFresh` | boolean | false | 0 | high |
| `morrisTalk` | boolean | false | 0 | high |
| `constantin` | boolean | false | 0 | high |
| `lilyRoom` | boolean | false | 0 | high |
| `id` | boolean | false | 0 | high |
| `alley` | boolean | false, true | 1 | high |
| `cottage` | boolean | false | 0 | high |
| `coffeeDrunk` | boolean | false, true | 2 | high |
| `lake` | boolean | false | 0 | high |
| `cult` | boolean | false | 0 | high |
| `tent` | boolean | false | 0 | high |
| `turnDownLily` | boolean | false | 0 | high |
| `apt401Key` | boolean | false, true | 1 | high |
| `aptKeyLux` | boolean | false | 0 | high |
| `oldphone` | boolean | false, true | 1 | high |
| `phone` | boolean | false | 0 | high |
| `laptop` | boolean | false | 0 | high |
| `cam` | boolean | false | 0 | high |
| `digiGPS` | boolean | false | 0 | high |
| `zackSex` | boolean | false | 0 | high |
| `lilySex` | boolean | false | 0 | high |
| `lilyNude` | boolean | false | 0 | high |
| `textDad` | boolean | false | 0 | high |
| `dadSeen` | boolean | false | 0 | high |
| `dadRape` | boolean | false | 0 | high |
| `brotherMissing` | boolean | false | 0 | high |
| `constantinCorrupt` | boolean | false | 0 | high |
| `beautySeen` | boolean | false | 0 | high |
| `legsCheck` | boolean | false | 0 | high |
| `pussyCheck` | boolean | false | 0 | high |
| `hairCheck` | boolean | false | 0 | high |
| `makeupCheck` | boolean | false | 0 | high |
| `libBook` | boolean | false | 0 | high |
| `dildo` | boolean | false | 0 | medium |
| `tail` | boolean | false | 0 | high |
| `buttplug` | boolean | false | 0 | high |
| … | … | … | … | and 49 more |

### scalar (132)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `deckCount` | number | 8..8 | 0 | low |
| `chips` | number | 0..0 | 0 | low |
| `bet` | number | 0..0 | 0 | low |
| `luckyCasino` | number | 0.49..0.49 | 0 | low |
| `casinoSus` | number | 0..0 | 0 | low |
| `pot` | number | 0..0 | 0 | low |
| `winAmount` | number | 0..0 | 0 | low |
| `totalWinAmount` | number | 0..0 | 0 | low |
| `totalBetAmount` | number | 0..0 | 0 | low |
| `pMiss` | number | 0..0 | 0 | low |
| `dCheat` | number | 0..0 | 0 | low |
| `vibeLevel` | number | 0.07500000000000001..0.3 | 2 | low |
| `countperiods` | number | 0..85 | 35 | low |
| `questDays` | number | 0..8 | 7 | low |
| `mansionCook` | number | 0..0 | 0 | low |
| `cellarClean` | number | 0..0 | 0 | low |
| `intoxic` | number | 0..0 | 0 | low |
| `allure` | number | 0..30 | 3 | low |
| `inhib` | number | 100..117 | 1 | low |
| `corrupt` | number | -20..0 | 8 | low |
| `arousal` | number | 0..30 | 2 | low |
| `trauma` | number | 0..0 | 0 | low |
| `groceries` | number | 0..10 | 1 | low |
| `kitchenClean` | number | -175..0 | 7 | low |
| `zackClean` | number | -175..0 | 7 | low |
| `rngesus` | number | 0..21 | 46 | low |
| `rent` | number | 0..7 | 8 | low |
| `bum` | number | 0..0 | 0 | low |
| `PIProg` | number | 0..0 | 0 | low |
| `PIDays` | number | 0..0 | 0 | low |
| `birdwatch` | number | 0..0 | 0 | low |
| `jogger` | number | 0..1 | 1 | low |
| `cardio` | number | 0..0 | 0 | low |
| `yoga` | number | 0..0 | 0 | low |
| `mood.Lively` | number | 0..0 | 0 | low |
| `mood.Empty` | number | 0..0 | 0 | low |
| `mood.Dominant` | number | 0..0 | 0 | low |
| `mood.Submissive` | number | 0..0 | 0 | low |
| `mood.Sensual` | number | 0..0 | 0 | low |
| `mood.Romantic` | number | 0..0 | 0 | low |
| … | … | … | … | and 92 more |

### string (50)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `charPron.gender` | string | `non-binary`, `male` | 1 | low |
| `charPron.subject` | string | `they`, `he` | 1 | low |
| `charPron.object` | string | `them`, `him` | 1 | low |
| `charPron.possessive` | string | `their`, `his` | 1 | low |
| `charPron.reflexive` | string | `themself`, `himself` | 1 | low |
| `charPron.determiner` | string | `their`, `his` | 1 | low |
| `charPron.contraction` | string | `they're`, `he's` | 1 | low |
| `charPron.noun` | string | `person`, `man` | 1 | low |
| `charPron.partner` | string | `enbyfriend`, `boyfriend` | 1 | low |
| `partner` | string | `boyfriend` | 0 | low |
| `questLetter1` | string | `unopened` | 0 | low |
| `questLetter2` | string | `unopened` | 0 | low |
| `home` | string | `none`, `zackApt` | 1 | low |
| `name` | string | `Josephine` | 0 | low |
| `job` | string | `No job`, `cafe` | 1 | low |
| `oldphonePIN` | string | `6969` | 0 | low |
| `dating` | string | `single` | 0 | low |
| `pet.name` | string | `` | 0 | low |
| `pet.race` | object,string | `Sphynx` | 1 | low |
| `pet.gender` | object,string | `male` | 1 | low |
| `pet.attribute` | object,string | `an adventurous` | 1 | low |
| `return` | string | `Beginning`, `Street`, `Cafe` | 157 | low |
| `gender` | string | `Girl` | 0 | low |
| `upbring` | string | `chrisvirg` | 0 | low |
| `partnerPro1` | string | `he` | 0 | low |
| `partnerPro2` | string | `him` | 0 | low |
| `partnerPro3` | string | `his` | 0 | low |
| `garage.street.name` | string | `Street Parking` | 0 | low |
| `garage.city.name` | string | `City Parking` | 0 | low |
| `garage.mansion.name` | string | `Mansion Parking` | 0 | low |
| `garage.luxapt.name` | string | `Luxury Parking` | 0 | low |
| `car.honda.name` | string | `Honda EV` | 0 | low |
| `car.honda.condition` | string | `good` | 0 | low |
| `car.honda.location` | string | `dealership` | 0 | low |
| `car.toyota.name` | string | `Toyota Hybrid` | 0 | low |
| `car.toyota.condition` | string | `good` | 0 | low |
| `car.toyota.location` | string | `dealership` | 0 | low |
| `car.audi.name` | string | `Audi` | 0 | low |
| `car.audi.condition` | string | `good` | 0 | low |
| `car.audi.location` | string | `dealership` | 0 | low |
| … | … | … | … | and 10 more |

### misc (7)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `deck` | object | — | 0 | low |
| `player` | object | — | 0 | low |
| `dealer` | object | — | 0 | low |
| `questmap` | object | — | 0 | low |
| `cats` | object | — | 0 | low |
| `catGend` | object | — | 0 | low |
| `catAtt` | object | — | 0 | low |

## NPCs detected

| npc | stats observed | var count |
|---|---|---|
| chloe | love | 1 |
| lily | love | 1 |
| bro | love | 1 |
| dad | love | 1 |
| zack | love | 1 |
| caine | love | 1 |

## Body / appearance traits

- `discard`
- `makeupDone`
- `hairDone`
- `makeupAmount`


## Choice type distribution

| type | count |
|---|---|
| branch | 166 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 17
- Money expense events: 5

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **name** (12): `name`, `pet.name`, `garage.street.name`, `garage.city.name`, `garage.mansion.name`, `garage.luxapt.name`, …
- **price** (10): `garage.street.price`, `garage.city.price`, `garage.mansion.price`, `garage.luxapt.price`, `car.honda.price`, `car.toyota.price`, …
- **condition** (6): `car.honda.condition`, `car.toyota.condition`, `car.audi.condition`, `car.hyundai.condition`, `car.bmw.condition`, `car.urus.condition`
- **owned** (6): `car.honda.owned`, `car.toyota.owned`, `car.audi.owned`, `car.hyundai.owned`, `car.bmw.owned`, `car.urus.owned`
- **location** (6): `car.honda.location`, `car.toyota.location`, `car.audi.location`, `car.hyundai.location`, `car.bmw.location`, `car.urus.location`
- **maxspots** (4): `garage.street.maxSpots`, `garage.city.maxSpots`, `garage.mansion.maxSpots`, `garage.luxapt.maxSpots`
- **filledspots** (4): `garage.street.filledSpots`, `garage.city.filledSpots`, `garage.mansion.filledSpots`, `garage.luxapt.filledSpots`
- **gender** (3): `charPron.gender`, `pet.gender`, `gender`
- **partnerpro** (3): `partnerPro1`, `partnerPro2`, `partnerPro3`
- **partner** (2): `charPron.partner`, `partner`
- **questletter** (2): `questLetter1`, `questLetter2`
- **job** (2): `job`, `lilyQ.job`
- **temp** (2): `mood.temp1`, `mood.temp2`
- **cafe** (2): `eggLocations.cafe`, `exLoc.cafe`
- **park** (2): `eggLocations.park`, `exLoc.park`
- **hospital** (2): `eggLocations.hospital`, `exLoc.hospital`
- **outskirts** (2): `eggLocations.outskirts`, `exLoc.outskirts`
- **downtown** (2): `eggLocations.downtown`, `exLoc.downtown`
- **uptown** (2): `eggLocations.uptown`, `exLoc.uptown`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-19T07:02:14.826Z | 12m 51s | 53 | 53 | 52 | no |
| 2 | 2026-04-19T07:16:26.685Z | 17m 26s | 167 | 167 | 162 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **3586**
- Observed edges during play: **123** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **141** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **9**.
- Coverage: **3.93%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 5

### Playable-content partition
- Passages defined in source: **1636** (0 tagged `wip`, 9 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **1627**.
- Distinct passages visited at least once: **49** — playable-passage coverage: **3.0%**.

### Static edge kinds
| kind | count |
|---|---|
| wiki | 3207 |
| include | 202 |
| link | 128 |
| goto | 49 |

### Unresolved static targets (35)
Targets that appear in passage source but don't resolve to a known passage — typically dynamic expressions like `` <<goto `func()`>> `` or referenced-but-never-defined passages.

- `Anyone online??? [NEW`
- `Contests [NEW`
- `LINK DESTINATION`
- `M4F 18 [NEW`
- `M4F tonight M21 [NEW`
- `M4M 34 [NEW`
- `M64 looking to suck some dick [NEW`
- `RE: Montgomery`
- `Selling credit cards [NEW`
- `Site rules, News & Announcements [NEW`
- `Who's Montgomery? [NEW`
- `_args[4`
- `https://discord.gg/rPSPtFhzAv`
- `https://f95zone.to/threads/new-life-project-v0-4-1a-nota-bao.158423/`
- `https://ko-fi.com/notabao`
- `https://www.patreon.com/NotaBao`
- `https://www.tfgames.site/index.php?module=viewgame&id=3041`
- `need weed? [NEW`
- `policeDowntownAlley`
- `policeDowntownCar`
- … and 15 more

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