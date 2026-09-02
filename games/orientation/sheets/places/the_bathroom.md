# PLACE · The Bathroom  `[READY]`

| | |
|---|---|
| **id** | `the_bathroom` · button `Bathroom` |
| **ENTERED FROM** | `the_hall` |
| **FILL** | 3,500 words |
| **cycling pool** | yes — `sex/bathroom_morning_t4`, pool 5 |

## What kind of place this is
Shared, one door, four people. The bolt works. **Whether she uses it is a decision the room asks her
every morning**, which is the whole design of the room.

## The list
| row | system |
|---|---|
| **Shower** | needs — `clean`, 25 min, free |
| **Talk to @wes** | cast — `npc_wes` hub, 07:00–08:00 |
| **Leave the bolt** | ascent — `nerve`. Day-capped |

## Walk-in
**Required, and NOT deferred** — gate `the walk-in floor`. She washes alone here and Wes is
scheduled here.

`walkin_bath_wes` fires on the `clean` restore inside his window. Two exits, and they are two
different beats, not one beat with a modifier (**A6b**): **cover** — her body decided — and
**do not** — she decided. Everything downstream differs: what she says, what he says, and whether it
counts as a rung.

**BRAKE:** the walk-in rides `trigger.max_triggers_per_day = 1`. ⚠️ This is a **located** canvas, so
it needs no flag — `max_triggers_per_day` is read off the trigger (`v2.py:11017`) and
`markCanvasTriggered` stamps the day key *before* `advanceTime` (`v2.py:4290`), so it is immune to
the midnight trap. Reach for the flag only when a rung is triggerless.

## Ways out
`the_hall`
