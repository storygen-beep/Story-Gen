# PLACE · The Penthouse  `[READY]`

| | |
|---|---|
| **id** | `penthouse` |
| **ENTERED FROM** | `spire_plaza` |
| **WAYS OUT** | back to `spire_plaza` |
| **DOOR** | no — she has always been let in here, and that is the point |
| **LABELS** | `private` · `zone:spire` · `checks_cover` · `she_can_undress` |
| **fill** | 2,000 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

**Mercer's floor, and the softest bed in the game.** She is furniture here. It is the only room where
being used costs her nothing and gets her something — which is why it is the wrong answer, and why
the game has to make it comfortable enough that the player notices choosing it.

Two rooms hold Mercer and they are not the same room. Here he is still the man with an asset; at
`mercer_room` he is a man remembering he was. **His `relation` is nostalgia in both and it never
becomes desire**, because he is at his ceiling from the first beat and never learns anything, ever.

## The list — needs + people

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Sleep here." | `TBD` | need | `charge` | `relation gte N` | `charge` `set` `100` · `time` to 07:00 | yes |
| 2 | Mercer | `TBD` | hub | `service` | `trigger.npc` = `npc_mercer`, 08:00–23:00 | — | yes |

⚠️ **Row 1 is the second fill point for `charge` and it is FREE — which is the design, not a leak.**
It costs no coin and it costs the whole night in the Spire, out of reach of the Reach's windows.
`relation` gates it, so **the nostalgia meter buys hospitality access and never register**, exactly
as the shipped game's design said and never enforced.

⚠️ It does NOT fill `clean`. She wakes up in the Spire in what she arrived in.

## Walk-in — REQUIRED

He is scheduled, she sleeps here alone. Banded on `service`: who Mercer has over, and what he offers
them without asking her, because it costs him nothing.

## Media

`sex/mercer_serve_*_t5` (3) — the desk, the glass, the knees — plus the `mercer_finish_*` set shared
with the stall. `videos/locations/penthouse.jpg` on disk.

⚠️ **ONE ASSET, ONE BLOCK.** Never reuse a `file` or `pool_dir` across two blocks — review dedupes
by file and one verdict would silently cover two beats. The `mercer_finish_*` pools are shared
between two ROOMS, which is fine; what is not fine is two blocks in one room pointing at one pool.
