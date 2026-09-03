# SYSTEM · seated — what Kess has put inside her  `[READY]`

| | |
|---|---|
| **kind** | `sourced` — fed in one place, read all over |
| **key** | `seated` (integer, 0–5) |
| **fed at** | `kess_berth` — **and nowhere else** |
| **labels** | `has_bench` |
| **mechanism** (S8) | a player trait raised by Kess's seat rungs and read by ordinary `trait` conditions. Not rotation. |

This is the game's one load-bearing sourced system. The shape is the field's:
`family-ties` feeds piercings in **2 rooms** and reads them in **117 passages**; clothes 1 → 53;
the skill ladder 1 → 19. A room with two rows that feeds a system read in fifty places is doing
more work than a room with eight rows that feeds nothing.

---

## READERS — written first, on purpose

`the-systems.md` SY2: *"Write the reader first. A source with no readers is a dead meter wearing a
new hat."* And SY2b is the rule this game is being built against — across the twelve v2 games,
50 body-and-disposition systems run a median read-to-write of **0.40**, and **zero clear 10:1**.
Our descriptive systems are scoreboards. This one is not allowed to be.

| # | reader | where | what changes |
|---|---|---|---|
| 1 | does the drain fire at all | every `drain` rung, all 7 people | `seated >= 1` or the act runs and takes nothing |
| 2 | how much a drain takes | every `drain` rung | bands at 1 / 3 / 5 — the same act, three payloads |
| 3 | what Bastien's door-search finds | `bastien_backroom` entry | he strips her every visit; what he finds is what is in her |
| 4 | which act rungs her body will take | the `service` ladder | the deeper seats change what she can be used for |
| 5 | what a night on the line costs | `kess_berth` | the obligation MOVES with this — `the-economy.md` R3b |
| 6 | what shows under a garment | the `cover` doors | a deep seat reads wrong through a thin cover |
| 7 | how Mercer talks to her | `penthouse` · `mercer_room` | he is fond of the tool and notices it has been worked on |
| 8 | the quest card on the `drain` tier | guidance | S10 |

**8 readers across 7 locations, against 1 writer location.** `[INTENT]` — no instrument has
produced this; it is the design's claim and `gates.py` will judge it.

## WRITERS

| # | writer | where | effect |
|---|---|---|---|
| 1 | Kess seats a part | `kess_berth` | `seated` · `op = "add"` · `+1` |
| 2 | a failure takes one back out | `kess_berth` | `seated` · `op = "add"` · `-1` |

One location. That is the whole point of the system.

---

## The trap this sheet is written against

⚠️ **`worn_exposure` shipped 2026-08-28** — an engine predicate (`v2.py:4186`), a derived
aggregate, its own lock text and a section in `engine.md` — built precisely so a scene could ask
*"is she covered?"*. **Reads across all 26 built games: three.** DoL reads its equivalent 586 times
in 119 places, most of them in a street and a canteen rather than in sex scenes.

The lesson is not "build a better system". It is that **the content that consults it is the work**,
and it is written into scenes that already exist. Each of the eight readers above is an existing
surface getting a second version, not a new mechanic. The engine primitive is stacked `[group]`
bands on one key (`engine.md` §35).

⚠️ **The placement trap.** Adjacent `[group]` blocks merge into ONE if/elseif chain
(`v2.py:14637`) and first match wins. Any `seated` band dropped next to a surface's existing
ladder makes that ladder unreachable — no error, no build warning, the prose simply stops
appearing. Separate the two chains with any non-`group` block.

## What is NOT claimed

This is not a meter the player watches. It has no sidebar row, and its number is never printed.
The player learns what is in her from what men say about it.
