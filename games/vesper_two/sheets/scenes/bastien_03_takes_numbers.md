# SCENE · Bastien 3 — He takes numbers  `[READY]`

`arc_bastien_03` · `bastien_backroom` · 20:00–23:59 · gate `bastien_search` · `seated gte 1` ·
sets `bastien_reading` · **no sex**

**A2's step in his register.** It buys the two things an arc opening buys — when he is alone and
what he is vulnerable about — and for him the second answer is that **he wants to know**, which is
the only appetite he has that she can feed.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_numbers` | He writes down what came off the search. He is more interested in the numbers than in her, and it is the first time in the game a man in a room with her is thinking about something else. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Let him write it down." | `bastien_reading` set · `relation` `add` `+4` | yes |
| "Ask what the numbers are for." | `bastien_reading` set · `relation` `add` `+2` | yes |

## Media

`videos/locations/bastien_backroom.jpg`.
