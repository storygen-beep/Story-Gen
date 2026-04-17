# new-life-project — Exploration Report

Generated: 2026-04-17T05:36:17.680Z
Source URL: https://mopoga.com/new-life-project

## Session Summary

- Sessions run: 1
- Total wall-clock: 6m 47s
- Total clicks: 49
- Total choices explored: 49
- Unique states seen: 52
- Unexplored frontier (queued for next session): 0
- Any ending reached: not yet

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (2)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `money` | number | 0..49 | 2 | high |
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

### body (3)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `discard` | object | — | 0 | medium |
| `makeupDone` | number | 0..0 | 0 | medium |
| `hairDone` | number | 0..0 | 0 | medium |

### time (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `day` | number | 1..2 | 1 | high |

### flag (72)

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
| `coffeeDrunk` | boolean | false | 0 | high |
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
| … | … | … | … | and 32 more |

### scalar (125)

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
| `vibeLevel` | number | 0.05..0.3 | 2 | low |
| `countperiods` | number | 0..13 | 6 | low |
| `questDays` | number | 0..2 | 1 | low |
| `mansionCook` | number | 0..0 | 0 | low |
| `cellarClean` | number | 0..0 | 0 | low |
| `intoxic` | number | 0..0 | 0 | low |
| `allure` | number | 15..30 | 1 | low |
| `inhib` | number | 100..125 | 2 | low |
| `corrupt` | number | -25..0 | 3 | low |
| `arousal` | number | 0..5 | 1 | low |
| `trauma` | number | 0..0 | 0 | low |
| `groceries` | number | 0..0 | 0 | low |
| `kitchenClean` | number | -25..0 | 1 | low |
| `zackClean` | number | -25..0 | 1 | low |
| `rngesus` | number | 0..21 | 21 | low |
| `rent` | number | 0..1 | 1 | low |
| `bum` | number | 0..0 | 0 | low |
| `PIProg` | number | 0..0 | 0 | low |
| `PIDays` | number | 0..0 | 0 | low |
| `birdwatch` | number | 0..0 | 0 | low |
| `jogger` | number | 0..0 | 0 | low |
| `cardio` | number | 0..0 | 0 | low |
| `yoga` | number | 0..0 | 0 | low |
| `mood.Lively` | number | 0..0 | 0 | low |
| `mood.Empty` | number | 0..0 | 0 | low |
| `mood.Dominant` | number | 0..0 | 0 | low |
| `mood.Submissive` | number | 0..0 | 0 | low |
| `mood.Sensual` | number | 0..0 | 0 | low |
| `mood.Romantic` | number | 0..0 | 0 | low |
| … | … | … | … | and 85 more |

### string (46)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `charPron.gender` | string | `non-binary` | 0 | low |
| `charPron.subject` | string | `they` | 0 | low |
| `charPron.object` | string | `them` | 0 | low |
| `charPron.possessive` | string | `their` | 0 | low |
| `charPron.reflexive` | string | `themself` | 0 | low |
| `charPron.determiner` | string | `their` | 0 | low |
| `charPron.contraction` | string | `they're` | 0 | low |
| `charPron.noun` | string | `person` | 0 | low |
| `charPron.partner` | string | `enbyfriend` | 0 | low |
| `partner` | string | `boyfriend` | 0 | low |
| `questLetter1` | string | `unopened` | 0 | low |
| `questLetter2` | string | `unopened` | 0 | low |
| `home` | string | `none` | 0 | low |
| `name` | string | `Josephine` | 0 | low |
| `job` | string | `No job`, `cafe` | 1 | low |
| `oldphonePIN` | string | `6969` | 0 | low |
| `dating` | string | `single` | 0 | low |
| `pet.name` | string | `` | 0 | low |
| `return` | string | `Beginning`, `characterCreation`, `playGirl` | 49 | low |
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
| `car.hyundai.name` | string | `Hyundai` | 0 | low |
| `car.hyundai.condition` | string | `good` | 0 | low |
| `car.hyundai.location` | string | `dealership` | 0 | low |
| … | … | … | … | and 6 more |

### misc (10)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `deck` | object | — | 0 | low |
| `player` | object | — | 0 | low |
| `dealer` | object | — | 0 | low |
| `questmap` | object | — | 0 | low |
| `cats` | object | — | 0 | low |
| `catGend` | object | — | 0 | low |
| `catAtt` | object | — | 0 | low |
| `pet.race` | object | — | 0 | low |
| `pet.gender` | object | — | 0 | low |
| `pet.attribute` | object | — | 0 | low |

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


## Choice type distribution

| type | count |
|---|---|
| branch | 49 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 2
- Money expense events: 0

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
- **temp** (2): `mood.temp1`, `mood.temp2`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-17T05:29:30.208Z | 6m 47s | 49 | 49 | 50 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **3586**
- Observed edges during play: **47** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **57** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **2**.
- Coverage: **1.59%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 0

### Static edge kinds
| kind | count |
|---|---|
| wiki | 3207 |
| include | 202 |
| goto | 90 |
| link | 87 |

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