# SCENE · Renner 2 — The crew goes at five  `[READY]`

`arc_renner_02` · `renner_depot` · Mon-Sun **17:00–18:00** · gate `renner_hired` · sets
`renner_alone_known` · **no sex**

## What this step is FOR

**This is the whole of A2 in one screen.** It buys two things and nothing else: **when he is
alone**, and **what he is vulnerable about**. Both are things the player then uses.

> `family-ties` steps 0–3 are a place, an hour, and who else is in the building — *"go to the
> kitchen on any weekend at 7 a.m."* **Information the player earns is a rung; information the game
> narrates is exposition.**

The hour on this row is narrower than his schedule on purpose. She has to still be there at five.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_five` | The crew clocks out. He does not. The yard goes quiet and he is still at the manifest, and the numbers on it are the reason he is still here. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Stay and finish the row." | `renner_alone_known` set · `relation` `add` `+3` | yes |
| "Go home with the others." | — | yes |

⚠️ The second arm does **not** set the flag — it is the only step in this arc where the player can
leave without advancing, and it is repeatable. That is A4's *repeating a step at the bottom walks
the player up it*.

## Media

`videos/locations/renner_depot.jpg`.
