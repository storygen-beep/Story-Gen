# PLACE · Wes's Room  `[READY]`

| | |
|---|---|
| **id** | `wes_room` · button `Wes's Room` |
| **ENTERED FROM** | `the_hall` |
| **FILL** | 3,000 words |
| **cycling pool** | yes — `sex/wes_room_t4`, pool 4 |

## Why this room exists
**R2.** Wes lives here — a junior who never moved out. `board.map.homes.npc_wes = "wes_room"`. Only
a declaration separates *lives elsewhere* from *was never given a room*, and declaring the
step-brother offscreen would have hollowed out the taboo to save a room.

## What kind of place this is
The door is usually open, which is a fact about him rather than about the door.

## The list
| row | system | lands on a screen? |
|---|---|---|
| **Talk to @wes** | cast — `npc_wes` hub, 19:00–23:00 | yes — `hub_wes_room.base` |
| ├ *Ask him about the campus.* | cast — his eight exchanges, `hub_wes_room.talk` | yes |
| **Borrow something of his** | arc flags — the ride ladder | yes |

⚠️ **The talk pool is a BRANCH of the hub, not a row.** Folded 2026-09-03 (`the-surfaces.md` R9,
`the-first-hour.md` F5b). It shipped as its own canvas carrying `requires_npc` and no `trigger.npc`,
which puts a canvas in the SOLO lane — the one that holds Sleep and Shower, where no row carries a
name. It could not simply be given `npc`: the portrait renders ONE canvas per character, highest
priority (`v2.py:4735`), and this hub already owns that slot. A second surface for the same person
in the same room is a **node inside the first**.

⚠️ **Wes ships CONVERTED — three rungs, no arc.** Logged as **arc debt owed at 0.2** in
`v2_state.decisions`. `the-arc.md`'s closing rule is to name which of A1–A12 a release built and
which it skipped, with the reason; this is that entry.

## Ways out
`the_hall`
