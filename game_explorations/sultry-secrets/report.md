# sultry-secrets — Exploration Report

Generated: 2026-04-17T16:36:39.909Z
Source URL: https://mopoga.com/sultry-secrets

## Session Summary

- Sessions run: 1
- Total wall-clock: 10m 8s
- Total clicks: 21
- Total choices explored: 21
- Unique states seen: 22
- Unexplored frontier (queued for next session): 0
- Endings reached: 1 (Preserve your virgintiy for future)

## Engine
Detected engine: **sugarcube**

## Variable schema (labeled at report time)

### player_stat (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `corruption` | number | 1..2 | 2 | high |

### flag (41)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `havesex` | boolean | false, true | 2 | high |
| `day5_bath` | boolean | false | 0 | high |
| `gameStarted` | boolean | false | 0 | high |
| `gameOver` | boolean | false | 0 | high |
| `washroom_first_time` | boolean | false | 0 | high |
| `glory_event` | boolean | false | 0 | high |
| `day6_kitchen` | boolean | false | 0 | high |
| `day6_bathroom` | boolean | false | 0 | high |
| `day6_drink` | boolean | false | 0 | high |
| `day6_forest` | boolean | false | 0 | high |
| `day6_job` | boolean | false | 0 | high |
| `day6_class` | boolean | false | 0 | high |
| `day6_p` | boolean | false | 0 | high |
| `day7_kitchen` | boolean | false | 0 | high |
| `day7_living` | boolean | false | 0 | high |
| `day7_shower` | boolean | false | 0 | high |
| `day7_gwen` | boolean | false | 0 | high |
| `day7_shop` | boolean | false | 0 | high |
| `day7_virgin` | boolean | false | 0 | high |
| `day8_shop` | boolean | false | 0 | high |
| `day8_shower` | boolean | false | 0 | high |
| `day9_principal` | boolean | false | 0 | high |
| `day9_toilet` | boolean | false | 0 | high |
| `day10_class` | boolean | false | 0 | high |
| `day11_drop` | boolean | false | 0 | high |
| `cute_photo` | boolean | false | 0 | high |
| `bsd11` | boolean | false | 0 | high |
| `pd11` | boolean | false | 0 | high |
| `cfd11` | boolean | false | 0 | high |
| `scored` | boolean | false | 0 | high |
| `bsd14` | boolean | false | 0 | high |
| `pd14` | boolean | false | 0 | high |
| `blacksmith` | boolean | false | 0 | high |
| `lake` | boolean | false | 0 | high |
| `guards` | boolean | false | 0 | high |
| `m01_revenge` | boolean | false | 0 | high |
| `m01_princess_black` | boolean | false | 0 | high |
| `m01_thief` | boolean | false | 0 | high |
| `princess_pro` | boolean | false | 0 | high |
| `magistrate_m01` | boolean | false | 0 | high |
| … | … | … | … | and 1 more |

### scalar (10)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `david_relation` | number | 0..0 | 0 | low |
| `int` | number | 10..10 | 0 | low |
| `blowjob` | number | 2..3 | 1 | low |
| `rep` | number | 0..0 | 0 | low |
| `jack` | number | 0..0 | 0 | low |
| `day5` | number | 0..0 | 0 | low |
| `round` | number | 1..1 | 0 | low |
| `drunk` | number | 0..0 | 0 | low |
| `serve` | number | 0..0 | 0 | low |
| `m01_shift` | number | 0..0 | 0 | low |

### misc (1)

| name | type | range / samples | mutations | confidence |
|---|---|---|---|---|
| `players` | object | — | 0 | low |

## NPCs detected

_No NPCs detected yet._

## Body / appearance traits

_No body/appearance variables detected._

## Choice type distribution

| type | count |
|---|---|
| branch | 20 |

## Economy

- Price-labeled choices observed: 0
- Money income events: 0
- Money expense events: 0

## Variable prefix clusters

Variables sharing a leading token — candidate entity groups (verify manually).

- **day** (21): `day5`, `day5_bath`, `day6_kitchen`, `day6_bathroom`, `day6_drink`, `day6_forest`, …
- **bsd** (2): `bsd11`, `bsd14`
- **pd** (2): `pd11`, `pd14`

## Sessions

| # | started | duration | clicks | choices | new states | completed |
|---|---|---|---|---|---|---|
| 1 | 2026-04-17T16:26:32.028Z | 10m 8s | 21 | 21 | 22 | yes |

## Graph coverage (observed vs. static)

- Static-graph edges (every navigation parsed from passage source): **591**
- Observed edges during play: **21** unique `(from, clicked_text, to)` tuples.
- Static edges covered by at least one observation: **21** (a single observation covers every static edge with the same `(from, to)` pair — gated branches collapse to one observable move).
- Observed-only edges (no matching static edge, typically self-loop `<<link>>` wrappers that `<<replace>>` in-place): **0**.
- Coverage: **3.55%** of the static graph explored.
- Synthetic edges (Claude's out-of-band `eval`/`keys`/`restore`/`pop`): 1

### Playable-content partition
- Passages defined in source: **430** (0 tagged `wip`, 0 empty-body placeholder).
- Implied playable (non-WIP, non-empty): **430**.
- Distinct passages visited at least once: **22** — playable-passage coverage: **5.1%**.

### Static edge kinds
| kind | count |
|---|---|
| wiki | 586 |
| link | 4 |
| goto | 1 |

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