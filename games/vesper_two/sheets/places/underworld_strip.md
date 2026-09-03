# PLACE · The Strip  `[READY]`

| | |
|---|---|
| **id** | `underworld_strip` |
| **ENTERED FROM** | `the_street` |
| **WAYS OUT** | `underworld_bar` · `underworld_brothel` · `kess_berth` · `mercer_room` · `cain_lab` (locked) · back to `the_street` |
| **DOOR** | no |
| **LABELS** | `outdoors` · `public` · `zone:reach` |
| **fill** | 1,000 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

The Reach's open row and the busiest junction in the game — five of the fourteen rooms hang off it.
Nobody here cares what she is, which is the whole difference between this zone and the Spire.

## The list

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Pay the toll. (5 coin.)" | `TBD` | work | `coin` | first visit only | `coin` `add` `-5` | yes |
| 2–6 | the five ways on | `TBD` | exit | — | — | `time` `add` `+5` | yes |

⚠️ **The price is ON the label.** Vesper charged 5 coin for this exact toll with the amount written
nowhere — 3 of its 11 priced choices did the same. **Every game in the play corpus that charges
money puts the amount in the label**, because the player is budgeting against a date.

⚠️ **A price is spelled out.** 94% of the field's 654 priced labels use a symbol; vesper spelled the
unit out on 100% of twelve. An invented unit used consistently — *"5 coin"* — is the field's own
pattern and is not a defect. `board.economy.symbol` is `coin` and every button agrees with it.

## Ambient

`cover` read as one swapped clause: who calls after her crossing the row. The traversal layer is
most of the play minutes, and a non-erotic traversal layer wins by sheer occupancy — which is why
this cold-looking junction carries a pool.
