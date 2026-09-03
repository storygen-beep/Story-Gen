# SYSTEM · charge — the body's clock  `[READY]`

| | |
|---|---|
| **kind** | `ambient` |
| **key** | `charge` (0–100) — **a declared need** (`board.needs[]`) |
| **fed at** | `kess_berth` — the feed line, and nowhere else |
| **labels** | `home_base` |
| **mechanism** (S8) | `[player.core_traits] charge` + `[player.trait_decay]`. Not rotation. |

Vesper's body is not a household's. It is `Power down` / `Charge up`, and this is the whole of it.

| need field | value |
|---|---|
| `falls` | 20 a day |
| `fills` | `kess_berth` · a night on the feed line · to 100 |
| `costs` | **10 coin a night, paid to Kess** — this need and the obligation are the same click |
| `shuts` | under 30 no drain fires, and every act rung costing charge stops rendering |

⚠️ **`shuts` is the load-bearing field** (M9, gate 29). A need that shuts nothing is a chore.

## READERS — written first

| # | reader | where |
|---|---|---|
| 1 | does a drain fire | every drain rung |
| 2 | do the act rungs that cost charge render | the `service` ladder |
| 3 | what Kess says when she arrives empty | `kess_berth` |
| 4 | ambient — how she moves at low charge | `the_street` and the three grounds |

## WRITERS

decay `-20/day` · the feed line `charge` · `op = "set"` · `100` · **`costs` = 10 `coin`**

⚠️ **This is the game's only charge channel.** `[settings.rent]` is NOT used: `due_day` takes
weekday names only and arms at 00:00 (`engine.md` §26, `v2.py:5615`), so the engine's system is
weekly and cannot express a nightly demand. No authored canvas narrates a payment the engine is
making — the measured failure shipped both, and the free duplicate was the one with the writing.
