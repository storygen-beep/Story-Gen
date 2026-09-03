# PERSON · Bastien  `[READY]`

| | |
|---|---|
| **id** | `npc_bastien` |
| **role** | `owns the room` |
| **home** | `bastien_backroom` |
| **meter** | `relation` — how much he has been allowed to read |
| **rungs** | 3 (`0 · 10 · 25`) |
| **why her** | He caught her. His lever is **curiosity, not desire** — he wants to read her. |

**No seduction ladder, because one would bounce off him.** What he has never permitted is being
read himself, and what she has never permitted is being read at all. That is the trade.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `bastien_backroom` | Mon-Sun | 20:00 | 23:59 | behind his own bar, taking numbers |

## The arc

**6 steps · first 3 carry no sex** (50%).

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | He already knows whose you are | `arc_bastien_01` | `bastien_backroom` | 20:00 | 23:59 | `service gte 10` | `bastien_caught` | no |
| 2 | He strips you at the door | `arc_bastien_02` | `bastien_backroom` | 20:00 | 23:59 | `bastien_caught` | `bastien_search` | no |
| 3 | He takes numbers | `arc_bastien_03` | `bastien_backroom` | 20:00 | 23:59 | `bastien_search` · `seated gte 1` | `bastien_reading` | no |
| 4 | Let him read something | `arc_bastien_04` | `bastien_backroom` | 20:00 | 23:59 | `bastien_reading` · `relation gte 10` | `bastien_first` | yes |
| 5 | Your body is the bag | `arc_bastien_05` | `bastien_backroom` | 20:00 | 23:59 | `bastien_first` · `seated gte 3` | `bastien_smuggled` | yes |
| 6 | **CONVERSION** | `arc_bastien_06` | `bastien_backroom` | 20:00 | 23:59 | `bastien_smuggled` · `relation gte 25` | `bastien_open` | yes |

⚠️ **Step 2 is the door, and the door is on the place sheet** — the threshold *is* the content, and
it is the only place in the game where `seated` is read against her before she has said anything.

⚠️ **Step 5 is the arc's own use for the sourced system.** Two things to get past him now, and her
body is where both are. That is why `seated` is fed in one room and read in seven.

## What step 6 converts into

`loop_bastien_backroom` — throttled on `arousal`. Ceiling stays **cell-scoped**: rough, and the
roughness is about being read, not wanted.
Media: `sex/bastien_loop_*_t5` (4, incl. `anal_hard`) · `sex/bastien_finish_*_t5` (3) ·
`sex/bastien_backroom_t4`. **8 pools, all on disk.**

## The refusal (A3)

Counted `bastien_refusals` · warned at 2 (*"the door search stops being a formality"*) · at 3 sets
`bastien_closed` and **the Undertow's back room shuts**, which costs her the fastest `service`
route and says so.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_bastien` | 33 | he writes something down before he looks at her again |
| stopping | `stop_bastien` | 28 | he is not offended. He is *interested*, which is worse |
| chickening out | `chicken_bastien` | 26 | what it costs to be a thing he could not finish reading |

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_bastien` | `bastien_backroom` | Mon-Sun | 20:00 | 23:59 | `met_bastien` | 145 | yes |

He already knows whose she is. He says so, pleasantly, and then asks to see what she is carrying.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 145 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`The back room` — a place and an hour.
