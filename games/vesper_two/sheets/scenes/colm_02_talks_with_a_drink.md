# SCENE · Colm 2 — He talks with a drink in him  `[READY]`

`arc_colm_02` · `underworld_bar` · **21:00–23:59** · gate `colm_served` · sets `colm_talks` ·
**no sex**

## ⚠️ This step carries the informant function

Sol was cut from the cast; **his job lands here.** Bring Colm a name off the floor and he knows who
ran it and where the survivor turns up. That is the anchor's way *in* to everything else — which is
why the shortest arc in the game sits at the biggest location.

**A2's step, exactly**: it buys **when he is loose** (after nine, three drinks in) and **what he is
vulnerable about** (he cannot stop talking). Both are things the player then uses.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_talks` | After nine he will answer anything, and he does not remember afterwards which questions were the real ones. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Ask him a name." | `colm_talks` set · `relation` `add` `+3` | yes |
| "Let him talk himself out." | `colm_talks` set · `relation` `add` `+2` | yes |

⚠️ The name-asking row is **repeatable after the arc**, and it is the informant surface. It is a
`talk screen`, not an act rung — `the-surfaces.md` R2, a person is a hub.

## Media

`videos/locations/underworld_bar.jpg`.
