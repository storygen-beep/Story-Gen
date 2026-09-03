# PLACE · The Undertow — Bathroom  `[READY]`

| | |
|---|---|
| **id** | `underworld_bar_bathroom` |
| **ENTERED FROM** | `underworld_bar` |
| **WAYS OUT** | back to `underworld_bar` |
| **DOOR** | no — **a shared room gets no door** (`the-map.md` R6c). A locked bathroom is a sentence, not a screen. |
| **LABELS** | `private` · `zone:reach` · `she_can_undress` |
| **fill** | 600 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

**It is the only free fill point for `clean`,** which is what stops it being scenery. Two sinks and
a lock that does not work.

⚠️ **This room exists because a need shuts a door, not because bathrooms exist.** `board.needs[]`
declares `clean`, gate 29 reads its `shuts`, and the three `checks_cover` doors refuse her under 40.
A restore that gates nothing is a chore, and a chore is not a reason to build a screen.

## The list — one need

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Wash. (20 min.)" | `TBD` | need | `clean` | — | `clean` `set` `100` · `time` `add` `+20` | yes |
| 2 | "Back out to the floor." | `TBD` | exit | — | — | — | yes |

**One row and a way back.** A 300-word bus station is not a defect; it is a corridor, provided it
was declared as one. This one is declared as one.

⚠️ **A spent day still has a door** (gate 31). Row 1 carries no `conditions` and no `costs`, so this
screen can never render empty.

## The mirror line

The room's own reader of `clean`: what she sees, banded. Three bands on one key, which is directed
variety — `block_pool` is for undirected. **Zero v2 games use either**, and `block_pool` runs 46
times in `the_long_summer` and 6 in vesper.

## Walk-in

⚠️ Nobody is scheduled here, so the gate does not read this room — but the bar's traffic does. A
low-chance substitution off row 1, banded on `cover`: who comes in while she is at the sink.
