# PERSON · Marsh  `[READY]`

| | |
|---|---|
| **id** | `npc_marsh` |
| **role** | `dockside fixer` |
| **home** | `offscreen` |
| **meter** | `relation` — whether he books her by name instead of by slot |
| **rungs** | 2 (`0 · 15`) — the shortest in the game; field p25 is 2 |
| **why her** | He pays and does not care whose body is in the slot. |

**The honest version of what the company does to her**, and the first time she *chooses* a mark
rather than being pointed at one.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `underworld_brothel` | Sun | 20:00 | 23:59 | his standing hour, booked weeks out |

⚠️ **One day only.** That is the throttle — his window *is* his pacing, and no cost or cap is
needed on top of it. A rung that can only fire on a Sunday evening is capped at once a week by
the clock.

## The arc

**4 steps · first 1 carries no sex** (25% — short arc, and the setup is a purchase rather than a
conversation).

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | Buy the slot | `arc_marsh_01` | `underworld_brothel` | 20:00 | 23:59 | `coin gte 20` | `marsh_slot` | no |
| 2 | Take the hour | `arc_marsh_02` | `underworld_brothel` | 20:00 | 23:59 | `marsh_slot` · `clean gte 40` | `marsh_first` | yes |
| 3 | He books you by name | `arc_marsh_03` | `underworld_brothel` | 20:00 | 23:59 | `marsh_first` · `relation gte 15` | `marsh_named` | yes |
| 4 | **CONVERSION** | `arc_marsh_04` | `underworld_brothel` | 20:00 | 23:59 | `marsh_named` | `marsh_open` | yes |

⚠️ **Step 1 is A4b's third key: a preparation bought and endured.** Money buys the key to a rung,
not a stat — which is `the-economy.md` R1b arriving from the arc side. A shop that sells an arc's
prerequisite does more work than a shop that sells a meter point, and this is the game's only one.

⚠️ **Step 3 is the whole charge of him.** He starts as a man who does not care whose body it is and
ends as a man who asked for hers. Nothing about the act changes; the booking does.

## What step 4 converts into

`loop_marsh_sunday` — repeatable, **once a week by the clock**.
Media: `sex/marsh_*_t5` (7) — includes `marsh_finish_ass_paid_t5` and `marsh_finish_ass_nodrain_t5`,
which are the same act priced two ways. `sex/brothel_*_t5` (6) is the generic surface.

## The refusal (A3)

Counted `marsh_refusals` · warned at 2 (*"the slot goes back to whoever had it"*) · at 3 the
20 coin is **not refunded**, which is the sharpest refusal cost in the game because it is the only
one denominated in money.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_marsh` | 31 | he pays before he leaves and counts it out where she can see |
| stopping | `stop_marsh` | 28 | he asks, evenly, whether he is getting the hour he paid for |
| chickening out | `chicken_marsh` | 24 | the money on the side, and whether she takes it |

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_marsh` | `underworld_brothel` | Sun | 20:00 | 23:59 | `met_marsh` | 90 | yes |

He is waiting for the slot he booked and she is not the one he booked. He asks one question about the arrangement and none about her.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 90 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`Sunday's hour` — a place and a day.
