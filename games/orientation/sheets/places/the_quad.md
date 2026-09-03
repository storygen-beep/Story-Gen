# PLACE · The Quad  `[READY]`   **🌳 ROOT · CAMPUS GROUND**

| | |
|---|---|
| **id** | `the_quad` · button `Quad` |
| **ENTERED FROM** | `the_avenue` — **and the crossing is priced on this location**: `costs = { time = 40, money = 2 }` |
| **FILL** | 5,000 words |
| **cycling pool** | yes — `ambient/quad_t3`, pool 5 |

⚠️ **CORRECTED AT BUILD.** This sheet said *"two roots, not one nested inside the other."* The
engine cannot do it — `template_import.py:4287` hard-fails a `navigation_order` entry whose
`entry_from` is not that location, and gate 11's adjacency is built from those two fields only, so a
canvas-only crossing strands this room and its three children. The bridge is the **travel cost on
this location**, which is `the-map.md`'s own mechanism, and the archetype is untouched: `two_hub` is
*"two strong hubs joined by a commute."* **The forty minutes and the two dollars are what make it a
commute rather than a corridor.**

## What kind of place this is
Open ground with the lecture buildings on three sides and the row of houses along the east edge. The
eight o'clock is here. **The row is visible from here and she cannot walk into it yet** — which is
the door v0.1 ends on.

⚠️ **The eight o'clock is a ROW here, not a room of its own.** A lecture hall with two hundred people
in it answers only *work*, thinly, and the count is derived from needs + work + people.

## The list
| row | system |
|---|---|
| **Sit through the eight o'clock** | work — attendance. **Shut when `rest lt 30`** |
| ~~**Buy the lab kit**~~ | **MOVED 2026-09-03** to `the_union_shop` — `sheets/places/the_union_shop.md` |
| ~~**Cross to the row**~~ | **DELETED 2026-09-02.** The row is a location now — `sheets/places/the_row.md`, DECISIONS.md A5b |
| **Sit on the wall (30m)** | ascent — `reputation`. The quiet outcome pays — **but only to 45; see below** |

## Sit on the wall — the dispatcher

⚠️ **THIS ROW IS SPENT FROM `reputation` 45 AND THE PLAYER IS NOT TOLD.** Its grant carries
`cap = 45`, so past that it costs 30 minutes and pays exactly nothing, while looking identical.
Its 30% walk-in also needs @halloran physically on the quad — Mon/Wed/Fri 08:00–09:30 only, ~4.5
hours a week — so outside that window the roll is 0%, not 30%. Both are `Cause 2` in the
2026-09-02 analysis (per-source caps violate `the-meters.md:955` M6, and the field gates a
dispatcher's hit on NPC presence in 0–5% of cases against our 6/6). **Out of scope for the map
restructure; not fixed here.** The quest card that used to point at this row for the 45→85 climb
now points at `act_pledge_upstairs`, which can actually move it.
**A7.** Most visits produce nothing, and the nothing is written **five ways**, returning 30 minutes
and a small `reputation` tick. A place where something always happens has no tension in the click.

**A6 — clothing moves the odds, not the outcome.** `worn_exposure` raises the floor of the roll.
Dressed ordinarily something happens ~36% of the time; dressed for it, ~71%. **Same scenes, twice as
much world.**

**A9 — the incidents here are different SETUPS, not different acts**, and their gates spread from
`nerve 5` to `reputation 85` so this one place still has something to give at the top of the game.

⚠️ **A8** — a pending arc step pre-empts the roll: it is a one-shot at this location priced above
the ambient, and entry-time auto-fire redirects before the location screen renders (`v2.py:4921`).

## Ways out
`the_row` · `halloran_office` · `the_counter` · `the_union_shop` · **bridge → `the_avenue`**

⚠️ **`the_pledge_house` moved one level down, onto `the_row`.** This game's own prose calls it
*"third house along the row"*, and the quad was standing in for three separate places its writing
names — the row, the lecture building, the union building. Two of the three are built now.
`act_quad_row` — the canvas that pretended the row was a button — is deleted. DECISIONS.md A5b.

⚠️ **The union building followed, 2026-09-03.** `act_quad_shop` was the same shape one layer down: a
canvas whose node was titled *The union shop*, standing on open ground, named after one of the three
things it sold. It is a location now. The lecture building is the only one of the three still
standing in.
