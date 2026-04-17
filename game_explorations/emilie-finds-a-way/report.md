# emilie-finds-a-way — Exploration Report

Generated: 2026-04-17T11:10:53.335Z
Source URL: https://mopoga.com/embed/emilie-finds-a-way/

## Session Summary

- Sessions run: 1
- Total wall-clock: 15m 52s
- Total clicks: 67
- Total choices explored: 67
- Unique states seen: 56
- Unexplored frontier (queued for next session): 1
- Any ending reached: not yet

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (3)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `money` | number | 100..100 | 0 | high |
| `charisma` | number | 10..11 | 1 | high |
| `fitness` | number | 10..11 | 1 | high |

### flag (86)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `start` | boolean | false | 0 | high |
| `shower` | boolean | false, true | 1 | high |
| `tease1` | boolean | false, true | 1 | high |
| `daddyshower1` | boolean | false | 0 | high |
| `shopping1` | boolean | false | 0 | high |
| `undress` | boolean | true | 0 | high |
| `daddy` | boolean | false | 0 | high |
| `sport` | boolean | false | 0 | high |
| `gym1` | boolean | false | 0 | high |
| `gym2` | boolean | false | 0 | high |
| `gym3` | boolean | false | 0 | high |
| `gym4` | boolean | false | 0 | high |
| `gym5` | boolean | false | 0 | high |
| `run1` | boolean | false | 0 | high |
| `run2` | boolean | false | 0 | high |
| `run3` | boolean | false | 0 | high |
| `run4` | boolean | false | 0 | high |
| `run5` | boolean | false | 0 | high |
| `yoga1` | boolean | false | 0 | high |
| `yoga2` | boolean | false | 0 | high |
| `yoga3` | boolean | false | 0 | high |
| `yoga4` | boolean | false | 0 | high |
| `yoga5` | boolean | false | 0 | high |
| `analplug` | boolean | false | 0 | high |
| `dildo` | boolean | false | 0 | medium |
| `lube` | boolean | false | 0 | high |
| `selfie1` | boolean | true | 0 | high |
| `selfie2` | boolean | false | 0 | high |
| `selfie3` | boolean | false | 0 | high |
| `selfie4` | boolean | false | 0 | high |
| `selfie5` | boolean | false | 0 | high |
| `selfie6` | boolean | false | 0 | high |
| `selfie7` | boolean | false | 0 | high |
| `selfie8` | boolean | false | 0 | high |
| `selfie9` | boolean | false | 0 | high |
| `selfie10` | boolean | false | 0 | high |
| `selfie11` | boolean | false | 0 | high |
| `selfie12` | boolean | false | 0 | high |
| `selfie13` | boolean | false | 0 | high |
| `selfie14` | boolean | false | 0 | high |
| … | … | … | … | and 46 more |

### scalar (14)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `openminded` | number | 0..23 | 13 | low |
| `arousal` | number | 0..32 | 17 | low |
| `loveanal` | number | 0..3 | 2 | low |
| `loveoral` | number | 0..4 | 4 | low |
| `sharing` | number | 0..0 | 0 | low |
| `bobbyaddiction` | number | 0..17 | 7 | low |
| `ericaddiction` | number | 0..6 | 6 | low |
| `francoisaddiction` | number | 0..12 | 6 | low |
| `sophiaaddiction` | number | 3..10 | 1 | low |
| `gabriellaaddiction` | number | 0..0 | 0 | low |
| `marcaddiction` | number | 0..0 | 0 | low |
| `johnaddiction` | number | 0..0 | 0 | low |
| `coworkeraddiction` | number | 0..0 | 0 | low |
| `jonathanaddiction` | number | 0..0 | 0 | low |

## NPCs detected

_No NPCs detected yet._

## Body / appearance traits

_No body/appearance variables detected._

## Choice type distribution

| type | count |
|---|---|
| branch | 66 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 0
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **selfie** (22): `selfie1`, `selfie2`, `selfie3`, `selfie4`, `selfie5`, `selfie6`, …
- **tutoring** (6): `Tutoring`, `Tutoring1`, `Tutoring2`, `Tutoring3`, `Tutoring4`, `Tutoring5`
- **office** (6): `Office`, `Office1`, `Office2`, `Office3`, `Office4`, `Office5`
- **gym** (5): `gym1`, `gym2`, `gym3`, `gym4`, `gym5`
- **run** (5): `run1`, `run2`, `run3`, `run4`, `run5`
- **yoga** (5): `yoga1`, `yoga2`, `yoga3`, `yoga4`, `yoga5`
- **bus** (5): `bus1`, `bus2`, `bus3`, `bus4`, `bus5`
- **chill** (5): `Chill`, `Chill1`, `Chill2`, `Chill3`, `Chill4`
- **gab** (5): `Gab1`, `Gab2`, `Gab3`, `Gab4`, `Gab5`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-17T10:55:01.560Z | 15m 52s | 67 | 67 | 56 | no |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **1121**
- Observed edges during play: **67** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **51** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **19**.
- Coverage: **4.55%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 1

### Static edge kinds
| kind | count |
|---|---|
| wiki | 1101 |
| link | 20 |

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