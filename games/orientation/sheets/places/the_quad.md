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
| **The eight o'clock** | work — attendance. **Shut when `rest lt 30`** |
| **Buy the lab kit** | money — a purchase that **stays bought** and opens the late lab (R1b) |
| **Cross to the row** | ends-on-a-door — `show_when_locked`, `reputation 85` |
| **Sit on the wall** | ascent — `reputation`. The quiet outcome pays |

## Sit on the wall — the dispatcher
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
`the_pledge_house` · `halloran_office` · `the_counter` · **bridge → `the_avenue`**
