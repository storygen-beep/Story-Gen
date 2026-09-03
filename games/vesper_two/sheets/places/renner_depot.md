# PLACE · Renner's Depot  `[READY]`

| | |
|---|---|
| **id** | `renner_depot` |
| **ENTERED FROM** | `the_waterfront` |
| **WAYS OUT** | back to `the_waterfront` |
| **DOOR** | no — she is hired here |
| **LABELS** | `private` · `zone:waterfront` |
| **fill** | 2,500 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

**The only graded on-ramp in the game, and the only one already paid for.** Renner is the sole
character with a real approach ladder on disk: `rung_renner_tease_t2` → `rung_renner_flash_t3` →
`rung_renner_grope_t4`, then the loops. Six characters have a loop; **two have any ladder at all.**

He hires her as cheap hands, ignores her, and cannot hold his discipline as she teases up. Every
rung is her doing it on purpose — which is the appetite stated at the smallest scale in the game.

## The list — work + people

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Haul. (4h.)" | `TBD` | work | `coin` | 09:00–18:00 | `coin` `add` `+12` · `charge` `add` `-15` · `time` `add` `+240` | yes |
| 2 | Renner | `TBD` | hub | `service` · `cover` | `trigger.npc` = `npc_renner`, 09:00–18:00 | — | yes |

**Two rows.** Work is its own surface and is never a rung inside his hub — *"Haul"* has no person as
the object of its verb.

⚠️ **The 4h cost is the throttle, and it is sized against his window** (M3 lever 2). A 10-minute
rung against an all-day hub is farmable ~144×/day; a 240-minute rung against an 09:00–18:00 window
is ~2/day, and advancing past the window makes him absent, which is what actually stops it.

⚠️ **The label states the duration and the engine does not tag activity time** (`v2.py:12733`), so
the button says `4h` itself. `the-clock.md` C4 — and a stated duration must be the real spend, or
gate `the label keeps its time` fails.

## Walk-in (R3) — REQUIRED, and the shape is already validated

⚠️ **This room's walk-in is the doctrine's own worked example, and it shipped in vesper.** Copy the
mechanism, not the world:

```toml
substitutions = [
  { target_canvas_id = "walkin_renner_depot", chance = 0.10, conditions = { … service lt 20 } },
  { target_canvas_id = "walkin_renner_depot", chance = 0.35, conditions = { … service gte 20, lt 40 } },
  { target_canvas_id = "walkin_renner_depot", chance = 0.70, conditions = { … service gte 40 } },
]
```

ONE canvas, `substitution_only = true`, three `[group]` bands on the trait the odds ride: watches
from the bottom of the ladder → finds reasons to touch her → backs her into the shelving. **Same
button. The world leans harder on it as he rots.**

⚠️ In vesper this rode `corruption`; here it rides `service`, because that is the tier this game
declares. The mechanism is what transfers.

## Media

`scenes/rung_renner_tease_t2` · `flash_t3` · `grope_t4` — the ladder, on disk.
`sex/renner_loop_*_t5` (4) · `sex/renner_finish_*_t5` (3) · `sex/renner_cheerup_*_t5` (2).
**9 pools + 3 rungs, all on disk.**
