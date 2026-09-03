# PERSON · Calloway  `[READY]`

| | |
|---|---|
| **id** | `npc_calloway` |
| **role** | `rogue-hunter` |
| **home** | `offscreen` |
| **meter** | `relation` — **belief**: how far he has let her into the case |
| **rungs** | 3 (`0 · 15 · 35`) |
| **why her** | Starving to be believed. Nobody has taken his hunt seriously in two years. |

**His secret is not a kink.** The seduction *is* being believed, which makes him the one man in the
game she holds something over without using her body first.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `vance_securities` | Mon-Sun | 08:00 | 20:00 | in the stacks, being audited shut |

## The arc

**7 steps · first 3 carry no sex** (43%).

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | Work his case | `arc_calloway_01` | `vance_securities` | 08:00 | 20:00 | `cover gte 10` | `calloway_met` | no |
| 2 | Nobody else came | `arc_calloway_02` | `vance_securities` | 08:00 | 20:00 | `calloway_met` | `calloway_belief` | no |
| 3 | After the auditors go | `arc_calloway_03` | `vance_securities` | 18:00 | 20:00 | `calloway_belief` | `calloway_alone_known` | no |
| 4 | Sit closer than you need to | `arc_calloway_04` | `vance_securities` | 18:00 | 20:00 | `calloway_alone_known` · `relation gte 15` | `calloway_contact` | yes |
| 5 | He asks for it badly | `arc_calloway_05` | `vance_securities` | 18:00 | 20:00 | `calloway_contact` · `service gte 25` | `calloway_first` | yes |
| 6 | The drawer | `arc_calloway_06` | `vance_securities` | 18:00 | 20:00 | `calloway_first` · `drain gte 20` | `calloway_file_seen` | yes |
| 7 | **CONVERSION** | `arc_calloway_07` | `vance_securities` | 08:00 | 20:00 | `calloway_file_seen` · `relation gte 35` | `calloway_open` | yes |

⚠️ **Step 3 buys the hour, and step 6 is the payoff the whole arc is for** — a look at her own file.
That is A4b's *"information the player earns is a rung"* doing the work a plot dump would otherwise
do, and it is the only place in v0.1 where the company's paperwork is on screen.

## What step 7 converts into

`loop_calloway_files` — repeatable, throttled on `arousal`.
Media: `scenes/rung_calloway_contact_t4` · `rung_calloway_oral_t5` · `sex/calloway_loop_*_t5` (4) ·
`sex/calloway_finish_*_t5` (3). **All on disk.**

## The refusal (A3)

Counted `calloway_refusals` · warned at 2 (*"he stops bringing the case up"*) · at 3 sets
`calloway_closed` and **the file room's late hours close with it**, which is the door being named
out loud rather than silently lost.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_calloway` | 34 | he thanks her for the wrong thing; the case file still open on the desk |
| stopping | `stop_calloway` | 30 | he apologises too much, and that is worse |
| chickening out | `chicken_calloway` | 24 | what she owes a man who believed her first |

⚠️ His ceiling is **warm at the top** — being believed is what he is paying for. A register note,
not a content limit; the permitted words are in `crude_ceiling`.

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_calloway` | `vance_securities` | Mon-Sun | 08:00 | 20:00 | `met_calloway` | 130 | yes |

A man in a file room nobody visits, mid-sentence with himself. He explains his case to her because she is standing there, and does not stop.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 130 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`The file room` — a place and an hour.
