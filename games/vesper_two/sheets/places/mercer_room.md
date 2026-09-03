# PLACE · Mercer's Stall  `[READY]`

| | |
|---|---|
| **id** | `mercer_room` |
| **ENTERED FROM** | `underworld_strip` |
| **WAYS OUT** | back to `underworld_strip` |
| **DOOR** | **YES** — his place, and she is the visitor |
| **LABELS** | `private` · `zone:reach` · `she_can_undress` |
| **fill** | 2,500 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

⚠️ **CORRECTED 2026-09-03 — this sheet contradicted the penthouse sheet and the person sheet.** It
said Mercer was *"blown and hiding under a flat new name"*, which cannot be true of a man who also
holds a Spire penthouse 08:00–23:00. Two states of the same character from the shipped game's
timeline, declared as if they were simultaneous. Caught by writing his arc, which is what the
sheets phase is for.

**The resolution: he is not hiding, he is SLIDING, and the two rooms are the slide.** The penthouse
by day, because his position still just about holds. The stall by night, in Spire paper, because it
does not. He runs it under a flat name and everyone in the Reach knows exactly whose name it is.

He is **delighted** to see her, because she is proof he was once a man with an asset. He remembers
owning her fondly.

**He is the top of the leash and he never notices her change.** That is the design: no arc, no
climb, at his ceiling from the first beat. His `relation` is **nostalgia** — how much of his old
life is back in the room — and it buys **hospitality access, never register**.

## The list

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Knock." | `TBD` | door | `service` | 23:00–08:00 | — | yes |
| 2 | Mercer | `TBD` | hub | `service` | `trigger.npc` = `npc_mercer`, 23:00–08:00 | — | yes |

⚠️ **The overnight window is ONE row, not two** — but only because `weekdays` covers all seven days.
`isCurrentTimeSlot` handles the wrap (`v2.py:3784`), and the weekday check runs first against
**today** (`v2.py:3596`). A day-specific overnight window would need two rows and this one does not.

## Walk-in

⚠️ Required — he is scheduled and she has solo rows here. Banded on `service`: who else is at the
stall at four in the morning, and what he lets them do because it costs him nothing.

## Media

`sex/mercer_lockup_*_t5` (7) · `sex/mercer_print_*_t5` (6) · `sex/mercer_serve_*_t5` (3) ·
`sex/mercer_finish_*_t5` (3) — **16 pools, the deepest set in the game, all on disk.**

⚠️ **He is at his ceiling from beat one, so his use-scenes differentiate by WHAT EACH VIOLATES, not
by pose.** Sixteen pools is not sixteen rungs; it is sixteen different things being taken.
