# SCENE · Colm 1 — Serve him  `[READY]`

`arc_colm_01` · `underworld_bar` · Mon-Sun 19:00–23:59 · gate `bar_rung gte 0` · sets `colm_served` ·
**no sex**

## ⚠️ Read before the rest of his sheets

**He does not climb.** He is cold and fast from the first beat, and the arc's job is to make
*sameness* into content rather than into filler. Step 4 is the one that does it.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_served` | A man at the end of the bar drinking through a delivery. He talks first, he talks too much, and that is the whole of him. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Keep his glass full." | `colm_served` set · `relation` `add` `+3` | yes |
| "Let him run dry." | `colm_served` set · `relation` `add` `+1` | yes |

## Media

`videos/locations/underworld_bar.jpg`.
