# SYSTEM · coin — the only thing that can say no  `[READY]`

| | |
|---|---|
| **kind** | `ambient` |
| **key** | `coin` — declared `board.economy.currency`, symbol written `coin` |
| **fed at** | `underworld_bar` (the floor) · `underworld_brothel` (a booked hour) · `renner_depot` (hauling) |
| **labels** | — |
| **mechanism** (S8) | `[player.core_traits] coin` + `costs` on choices. Not rotation. |

## READERS — written first

| # | reader | where | what |
|---|---|---|---|
| 1 | the feed line | `kess_berth` | **10 a night** — the obligation |
| 2 | garments | wardrobe / shop rungs | each is a `cover` rung |
| 3 | Kess's parts | `kess_berth` | each is a `seated` rung |
| 4 | the toll at the gate | `underworld_strip` | reach |
| 5 | buying Sunday's slot | `underworld_brothel` | the way to Marsh |

**Five sinks, and they are at four different places.** Vesper ran 10 sinks to 5 sources with **6 of
the 10 at one shop counter** — that is a shop, not an economy. A sink belongs where the thing being
bought lives.

## WRITERS

| source | rate | brake |
|---|---|---|
| the floor at the bar | 15 a shift | `trigger.costs` time, sized to Colm's 19:00–23:59 window |
| a booked hour | by act | day-capped flag cleared in `[engine.daily_tick]` |
| hauling at the depot | by load | Renner's 09:00–18:00 window |

⚠️ **NO FREE UNCAPPED INCOME.** Vesper shipped three repeatable surfaces printing money with no
cost, no cap and no daily limit — `+30`, `+28`, `+60` every 120 minutes. Being behind a tier gate is
not a cap: the tier is bought once, the rung repeats.

⚠️ **A price is on its label.** Every priced button names its amount. Vesper had 3 of 11 that did
not, and the field puts the amount on the label every time — the player is budgeting against a date.

`[INTENT]` `week_income` **210** against an obligation of **10 a night / 70 a week** = 33%.
`forty_miles` runs 70% and `back_home` 25%, so this sits inside the field's range. The obligation
also **MOVES** — Kess raises the nightly rate as `seated` climbs (R3b).
