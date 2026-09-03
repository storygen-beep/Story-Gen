# SCENE · Calloway 3 — After the auditors go  `[READY]`

`arc_calloway_03` · `vance_securities` · **18:00–20:00** · gate `calloway_belief` ·
sets `calloway_alone_known` · **no sex**

**A2's hour.** The window is narrower than his schedule on purpose — this step buys **when he is
alone**, and the player then uses it. *"Go to the kitchen on any weekend at 7 a.m."* is the field's
version of the same row.

## Nodes

| # | node | what is on it | exit |
|---|---|---|---|
| 1 | `n_alone` | The auditors leave at six and he does not. The stacks are his again for two hours a day and he spends them the same way every time. | choices |

## Exits

| label | effect | screen |
|---|---|---|
| "Stay past six." | `calloway_alone_known` set · `relation` `add` `+4` | yes |
| "Leave with the auditors." | — | yes |

⚠️ The second arm does not advance and is repeatable — A4's *repeating a step at the bottom walks
the player up it.*

## Media

`videos/locations/vance_securities.jpg`.
