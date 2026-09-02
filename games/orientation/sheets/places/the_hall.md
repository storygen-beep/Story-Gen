# PLACE · Hall  `[READY]`

| | |
|---|---|
| **id** | `the_hall` · button `Hall` |
| **ENTERED FROM** | `the_avenue` |
| **FILL** | 600 words |
| **cycling pool** | yes — `traffic/hall_landing_t4`, pool 4 |
| **DOOR** | **no.** R6c — shared circulation. Occupancy is a row *inside* the room, never a threshold in front of it |
| **LABELS** | *(none declared — `board.systems[]` has not been taken)* |

⚠️ **This room exists because the prose already contained it.** `the-map.md` R5 — *"three uses of
the same word is a place."* Before the 2026-09-02 restructure the writing named a **landing 7×**,
**stairs 6×** and a **corridor 3×**, and the map had none of them: all five house rooms hung off
`the_avenue`, so she walked out to the street to get from her bed to the bathroom. That is R3's
inverted map — *the home containing a bit of world* — and the avenue was carrying **2 things to do
against 6 ways out** where the field median for a place is 3 and 1.

⚠️ **NOT `is_container`.** A container swallows every canvas attached to it (`engine.md:770-772`),
which would put this room permanently in gate 1's *"declared locations with nothing placed"* list
and make it impossible to warm — and `traversal heat` is a ratio, so adding two cold rooms would
have taken the game from 7/10 = 70% to 7/12 = 58% and failed the 60% floor.

⚠️ **NO `[[npcs.schedules]]` ROW HERE, DELIBERATELY.** `the walk-in floor` (gate 30) qualifies any
location holding **both** a solo repeatable canvas **and** a scheduled body, and then owes it a
substitution rule. This room reports on the rooms *next* to it, which does not qualify it.

## What kind of place this is
The inside of the house that is not anybody's. Front door, stairs, the kitchen through the arch,
four doors off the landing and the one bathroom among them. **It is where she finds out who is in
before she decides which door to open** — the house's own state, read from the middle of it.

The corpus model is `zaras-school-life`'s living room and `corpo-life`'s kitchen: a home hub lists
the doors, keeps one or two things of its own, and its main content is a chain keyed on **who is
present right now**.

⚠️ **What the engine will not do, and what we do instead.** Zara's hub prints
`"Zara's mom is showering | [Join her]"` — a per-NPC activity line with a gated link.
`getNpcsPresentAtLocation` returns `{id, name, portrait}` and **discards the schedule's `activity`
string** (`v2.py:5025-5029`), and `[[locations]]` has no authorable row list at all
(`template_import.py:1899-1922` is the complete key set). So: the **destination cards already carry
a portrait badge** for whoever is scheduled in that room now, free (`v2.py:20338`), and this room's
`description_variants` write the sentence that goes with the face. Zara's beat minus the one-click
shortcut, on shipped features only.

## The list
| row | system |
|---|---|
| **Wait on the landing** | needs — `rest`. The wait for the one bathroom, and the traffic through it |

⚠️ **It pays a NEED, never an ascent tier.** The measured lesson from the corpus: Zara's park bench
restores **energy** on the quiet outcome and moves **corruption** only on the loud one. `act_quad_wall`
paid `reputation` for sitting still, which made it a climb rung, which correctly attracted a day-lock
and a `cap = 45` — and that is how it became a button that costs 30 minutes and returns nothing.

## What the room reports
Four `description_variants`, first-match, gated on `npc_at_location` — which is **cross-room**
(`v2.py:4368-4387`), so a condition evaluated here can ask about the bathroom:

| when | what the hall says |
|---|---|
| @wes in `the_bathroom` | the water going, the door shut, her mother's coat gone off the hook |
| @ray in `the_kitchen`, @dee absent | the light through the arch, the radio down to a shape |
| @dee in `the_kitchen` | her keys already down somewhere she will not find them |
| @wes in `wes_room` | the landing light off on its timer, a line under his door |

## Ways out
`her_room` · `the_kitchen` · `the_bathroom` · `the_back_bedroom` · `wes_room` · **back → `the_avenue`**
