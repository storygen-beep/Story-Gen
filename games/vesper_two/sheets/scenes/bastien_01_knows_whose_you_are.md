# SCENE · Bastien 1 — He already knows whose you are  `[READY]`

`arc_bastien_01` · `bastien_backroom` · Mon-Sun 20:00–23:59 · gate `service gte 10` ·
sets `bastien_caught` · **no sex**

## ⚠️ Read before the rest of his sheets

**His lever is curiosity, not desire, and a seduction ladder bounces off him.** There is no approach
ladder here and none should exist. What he has never permitted is being *read himself*; what she has
never permitted is being read at all. **That is the trade, and it is the whole character.**

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_caught` | He says whose she is, pleasantly, before she has decided what to tell him. Then he asks to see what she is carrying. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Show him." | `bastien_caught` set · `relation` `add` `+3` | yes |
| "Ask how he knows." | `bastien_caught` set · `relation` `add` `+2` | yes |

## Media

`videos/locations/bastien_backroom.jpg`.
