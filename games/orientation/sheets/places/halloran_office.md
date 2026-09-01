# PLACE · Halloran's Office  `[READY]`

| | |
|---|---|
| **id** | `halloran_office` · button `Halloran's Office` — owned interior, possessive |
| **ENTERED FROM** | `the_quad` |
| **FILL** | 4,000 words |
| **cycling pool** | yes — `sex/office_hours_t4`, pool 4 |

## What kind of place this is
Third floor, and the department empties at five. Office hours are 16:00–18:00, which means the last
hour of them is the only hour anyone is up there.

## The list
| row | system |
|---|---|
| **Office hours** | cast — `npc_halloran` hub, 16:00–18:00 |
| **The late lab** | work + arc — needs the lab kit bought at `the_quad` |
| **Ask about the reader's key** | start choice — `past_top` reaches this in week one |

⚠️ **`past_top` buys REACH here, and that is what a start choice is for.** Not flavour — the key gets
her into the building after the department has emptied, which is the top of this ladder's access.
**Additive only:** the original rung keeps its numbers and gains `past_top is_false`.

⚠️ **Separate the past-ladder from the existing `relation` band with a non-`group` block.** Adjacent
`[group]` blocks merge into one if/elseif chain and first match wins (`v2.py:14637`); the original
ladder would go dark with no error.

## Walk-in
**Required.** `walkin_latelab` — a colleague's door opens down the corridor while she is in there
after hours. Fires on the late lab, `max_triggers_per_day = 1` on the trigger.

⚠️ **Halloran ships CONVERTED — three rungs, no arc.** Logged as **arc debt owed at 0.3**.

## Ways out
`the_quad`
