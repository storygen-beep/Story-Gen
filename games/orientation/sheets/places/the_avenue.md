# PLACE · The Avenue  `[READY]`   **🌳 ROOT · EXTERIOR**

| | |
|---|---|
| **id** | `the_avenue` · button `Avenue` |
| **ENTERED FROM** | **nothing. This is a root — no `entry_from`.** |
| **FILL** | 3,000 words |
| **cycling pool** | yes — `ambient/avenue_t3`, pool 4 |

⚠️ **`board.map.exterior`, and gate 28 reads `entry_from` to check it.** A game once declared an
exterior, priced it at 25 minutes, passed every gate — and its exterior hung off the kitchen, so
stepping outside meant stepping from one interior into a row of shops. **The world contains the
house; the house does not contain a scrap of world.**

## What kind of place this is
The street the Kessler house is on. A shelter at the stop, four other houses, the car in the drive.
This is the ground the house side sits on, and **the only renewable source of new people the
domestic half of this game has.**

## The list
| row | system |
|---|---|
| **Wait for the bus** | the bridge — 40 min, $2, always open |
| ~~**Ask @wes for a ride**~~ | cast — `npc_wes`, 07:15–07:50. **DECLARED, NOT BUILT.** No canvas exists |
| ~~**Ask @ray for a ride**~~ | cast — `npc_ray`, 08:00–08:30 and 18:00–18:30. **DECLARED, NOT BUILT** |
| **Wait out by the road (15m)** | ascent — `reputation`, and `worn_exposure` swaps the prose |

⚠️ **THE SECOND WAY ACROSS DOES NOT EXIST YET.** A ride from @wes or @ray — 15 minutes, no fare,
gated on `relation` — is declared in this sheet, in `v2_state.json` (`board.map.bridges[0].note`
and `r1_signoff`), in DECISIONS.md A5, and in `npc_wes.arc_stages`, which ships a stage literally
called **"The ride"**. **There is no canvas.** The avenue has three and none of them offers a
lift. Logged 2026-09-02 rather than inherited silently; the sheet no longer claims it is built.
Wes's window also disagrees with the build — this sheet said 07:10–07:45, the TOML says
07:15–07:50; the TOML is right and the row above now matches it.

⚠️ **Two ways across is the game's thesis on one screen: pay, or ask a man.** Travel friction is what
makes the schedule grid bite — a premise that says *ten minutes away* while arriving costs nothing
has written a fact the player never experiences. The cost sits on the **bridge**, never on every room.

## Ways out
`the_hall` · **bridge → `the_quad`**

⚠️ **This used to list all five house rooms.** The street was the hallway: she walked outside to
get from her bed to the bathroom, and the avenue carried 2 things to do against 6 ways out where
the field median for a place is 3 and 1. `the_hall` now holds them. Restructured 2026-09-02 —
DECISIONS.md A5.
