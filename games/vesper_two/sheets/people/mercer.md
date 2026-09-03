# PERSON · Mercer  `[READY]`

| | |
|---|---|
| **id** | `npc_mercer` |
| **role** | `former owner` |
| **home** | `mercer_room` |
| **meter** | `relation` — **nostalgia**: how much of his old life is back in the room |
| **rungs** | 3 (`0 · 10 · 30`) |
| **why her** | He owns her and it costs him nothing. The top of the leash and the last door. |

## ⚠️ This is a NON-SEDUCTION arc, and that is the design

He is **at his ceiling from the first beat** and **never learns anything, ever**. There is no climb
in him and no crack in him. What his meter buys is **hospitality access, never register** — the
shipped game's design said exactly this and never enforced it.

`the-arc.md` A1's line is that **zero arcs is what is not defensible**, not that every arc is a
seduction. His is a numbered ladder in which *she* changes position and *he* does not notice.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `penthouse` | Mon-Sun | 08:00 | 23:00 | his floor, his hours, her in the corner of it |
| `mercer_room` | Mon-Sun | 23:00 | 08:00 | the stall, under a flat new name |

⚠️ **Two rows, one character, no overlap** — 23:00 is the boundary and it is exclusive. The
overnight row is a single row **only because `weekdays` covers all seven days**: `isCurrentTimeSlot`
handles the wrap (`v2.py:3784`) but the weekday check runs first against *today* (`v2.py:3596`).

## The arc

**5 steps · first 2 carry no sex** (40%).

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | He is delighted | `arc_mercer_01` | `mercer_room` | 23:00 | 08:00 | — | `mercer_found` | no |
| 2 | His chores, like always | `arc_mercer_02` | `mercer_room` | 23:00 | 08:00 | `mercer_found` | `mercer_chores` | no |
| 3 | Serve | `arc_mercer_03` | `mercer_room` | 23:00 | 08:00 | `mercer_chores` | `mercer_served` | yes |
| 4 | He keeps you around | `arc_mercer_04` | `penthouse` | 08:00 | 23:00 | `mercer_served` · `relation gte 10` | `mercer_kept` | yes |
| 5 | **CONVERSION** | `arc_mercer_05` | `penthouse` | 08:00 | 23:00 | `mercer_kept` · `relation gte 30` | `mercer_open` | yes |

⚠️ **Step 3 is explicit at step 3 of 5 and that is correct for him alone.** He is the one man she is
already used by when the game opens, so his arc is not an escalation — it is her *position* moving
while the act stays exactly where it always was. Every other arc here earns its first act later.

⚠️ **Step 4 crosses rooms**, and it is the only arc step that does. It is reachable because the
penthouse row covers 08:00–23:00; the checker verifies that rather than trusting it.

## What step 5 converts into

`loop_mercer_penthouse` and the stall's own surface — **hospitality access**: the penthouse `Sleep
here` row unlocks, which is the game's second `charge` fill point and its only free one.

Media: `sex/mercer_lockup_*_t5` (7) · `mercer_print_*_t5` (6) · `mercer_serve_*_t5` (3) ·
`mercer_finish_*_t5` (3). **16 pools — the deepest set in the game.**

⚠️ Sixteen pools is **not** sixteen rungs. He is at his ceiling, so his use-scenes differentiate by
**what each violates**, never by pose.

## The refusal (A3)

⚠️ **He is the one character who cannot be refused, and the sheet says so out loud.** He does not
ask. A3's counter is absent here by design, and that absence is the character — but the *player*
still gets A11's stop and chicken-out exits, because those are hers and not his.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_mercer` | 35 | he is fond of her, out loud, and it is the worst line in the game |
| stopping | `stop_mercer` | 30 | mild surprise, and he waits, because she has never done that |
| chickening out | `chicken_mercer` | 26 | he does not even register it as a refusal |

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_mercer` | `penthouse` | Mon-Sun | 08:00 | 23:00 | `met_mercer` | 115 | yes |

He is delighted. He says her name before she says anything, and he is fond of her the way a man is fond of a good tool.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 115 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`The stall` — a place and an hour.
