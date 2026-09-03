# SCENE · Mercer 2 — His chores, like always  `[READY]`

`arc_mercer_02` · `mercer_room` · 23:00–08:00 · gate `mercer_found` · sets `mercer_chores` ·
**no sex**

**A2's step, in his register.** It buys the two things an arc opening buys — when he is alone, and
what he is vulnerable about — and for him both answers are the same: he is alone at the stall
because nobody comes to it, and what he is vulnerable about is that he used to have staff.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_chores` | He hands her the count sheet without discussing it, the way he did when she was an asset on a company floor. She does it. He watches her do it and is happy. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Do the count." | `mercer_chores` set · `relation` `add` `+3` | yes |
| "Do it badly." | `mercer_chores` set · `relation` `add` `+1` | yes |

## Media

`videos/locations/mercer_room.jpg`.
