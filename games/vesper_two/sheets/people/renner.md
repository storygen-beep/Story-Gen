# PERSON · Renner  `[READY]`

| | |
|---|---|
| **id** | `npc_renner` |
| **role** (the 1–3 words the engine prints under his name in EVERY dialogue box) | `depot owner` |
| **home** | `offscreen` |
| **meter** | `relation` — how far up from cheap hands she has climbed |
| **rungs** | 3 (`0 · 12 · 30`) — field per-character median is **3**, p25 2, p75 6 |
| **why her** | Cold, mean, clawing at a gutted business. He ignores her and then he cannot. |

**The only graded on-ramp in the game, and the only one already paid for.** He is where the arc
doctrine is easiest to satisfy because the media already assumes it: `tease_t2 → flash_t3 →
grope_t4` exist on disk. Six characters have a loop; two have a ladder.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `renner_depot` | Mon-Sun | 09:00 | 18:00 | working the yard, not looking up |

## The arc

**7 steps · first 2 carry no sex** (A2 — they buy *when he is alone* and *what he is vulnerable
about*, and both are things the player then uses).

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | Cheap hands | `arc_renner_01` | `renner_depot` | 09:00 | 18:00 | — | `renner_hired` | no |
| 2 | The crew goes at five | `arc_renner_02` | `renner_depot` | 17:00 | 18:00 | `renner_hired` | `renner_alone_known` | no |
| 3 | Work where he can see | `arc_renner_03` | `renner_depot` | 09:00 | 18:00 | `renner_alone_known` · `cover gte 10` | `renner_teased` | yes |
| 4 | Commando | `arc_renner_04` | `renner_depot` | 09:00 | 18:00 | `renner_teased` · `cover gte 20` | `renner_flashed` | yes |
| 5 | He finds a reason | `arc_renner_05` | `renner_depot` | 09:00 | 18:00 | `renner_flashed` · `relation gte 12` | `renner_touched` | yes |
| 6 | Cheer him up | `arc_renner_06` | `renner_depot` | 09:00 | 18:00 | `renner_touched` · `service gte 15` | `renner_first` | yes |
| 7 | **CONVERSION** | `arc_renner_07` | `renner_depot` | 09:00 | 18:00 | `renner_first` · `relation gte 30` | `renner_open` | yes |

⚠️ **Step 2 is the whole of A2 in one row.** It is a place, an hour, and who else is in the
building — the same shape as *"go to the kitchen on any weekend at 7 a.m."* **Information the player
earns is a rung; information the game narrates is exposition.**

⚠️ **Each step grants the meter the NEXT one reads, capped at that threshold** (A4), so repeating a
step at the bottom walks her up. Two buttons per page — one step further, or leave — and **the
number is printed on the one she cannot take**: `Requires relation 12`.

## What step 7 converts into

`loop_renner_depot` — the repeatable surface, and the reward for finishing the arc rather than the
starting position. Act menu **2 options** (field median 2, span 1), throttled on `arousal` and
nothing else.

Media on disk: `sex/renner_loop_*_t5` (4) · `sex/renner_finish_*_t5` (3) · `sex/renner_cheerup_*_t5` (2).

## The refusal (A3)

| part | what it does |
|---|---|
| counted | `renner_refusals` `add` `+1` — free and in character, written at full length |
| warned | at 2: *"He stops asking. The depot stays work."* — names what closes, in plain words |
| routed | at 3: `renner_closed`, and **Colm's on-ramp opens three days later** |

⚠️ Default is **parked, not closed** (A3b) — refusing once names where to come back to.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_renner` | 32 | he goes back to the ledger without a word; what she is holding; stay or go |
| stopping | `stop_renner` | 30 | **how he takes being stopped** — not her exit |
| chickening out | `chicken_renner` | 25 | after she already said yes, and what that costs |

⚠️ **23 of 23 finish nodes across six v2 games have an empty `exit_block`.** This one does not.

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_renner` | `renner_depot` | Mon-Sun | 09:00 | 18:00 | `met_renner` | 110 | yes |

He is hiring hands and does not look at the one he hires. The only thing he says is what the work is and what it pays.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 110 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`Work the depot` — names the place and the hour, never a number.
