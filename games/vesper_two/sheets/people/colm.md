# PERSON · Colm  `[READY]`

| | |
|---|---|
| **id** | `npc_colm` |
| **role** | `courier` |
| **home** | `offscreen` |
| **meter** | `relation` — how readily he talks with a drink in him |
| **rungs** | 3 (`0 · 8 · 20`) |
| **why her** | Cold and fast and nothing else. The rung where the act stops being an event. |

**He also carries the informant function** that was cut with Sol: bring him a name off the floor and
he knows who ran it. That is the anchor's way *in* to everything else, and it is why the shortest
arc in the game sits at the biggest location.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `underworld_bar` | Mon-Sun | 19:00 | 23:59 | at the end of the bar, drinking through a delivery |

## The arc

**5 steps · first 2 carry no sex** (40%). Short on purpose — he is the easy one, and the arc's job
is to make *easy* legible rather than to make it long.

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | Serve him | `arc_colm_01` | `underworld_bar` | 19:00 | 23:59 | `bar_rung gte 0` | `colm_served` | no |
| 2 | He talks with a drink in him | `arc_colm_02` | `underworld_bar` | 21:00 | 23:59 | `colm_served` | `colm_talks` | no |
| 3 | The back of the room | `arc_colm_03` | `underworld_bar` | 21:00 | 23:59 | `colm_talks` · `service gte 10` | `colm_first` | yes |
| 4 | He does not remember last time | `arc_colm_04` | `underworld_bar` | 21:00 | 23:59 | `colm_first` · `relation gte 8` | `colm_again` | yes |
| 5 | **CONVERSION** | `arc_colm_05` | `underworld_bar` | 19:00 | 23:59 | `colm_again` · `relation gte 20` | `colm_open` | yes |

⚠️ **Step 4 is the point of him.** The second time is written as *the same thing again* — that is
what makes him the rung where the act stops being an event, and it is a thing an arc can say that a
loop authored on day one cannot.

## What step 5 converts into

`loop_colm_backroom` — throttled on `arousal`.
Media: `sex/colm_loop_*_t5` (3) · `sex/colm_finish_*_t5` (3) · `sex/colm_backroom_t4`.

⚠️ **`sex/colm_ruin_t4` is EMPTY on disk** — the one media slot in this arc that needs a find-media
run. It is also the pool that ships media-blank in the live vesper 0.2.0.

## The refusal (A3)

Counted `colm_refusals` · warned at 2 (*"he takes his deliveries to the other bar"*) · at 3 sets
`colm_closed`, and **the informant route closes with him**, which is the expensive half — the
warning has to name that, not just the sex.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_colm` | 30 | he is already back on his stool and the glass is refilled |
| stopping | `stop_colm` | 27 | he shrugs. It genuinely does not matter to him, and she notices that |
| chickening out | `chicken_colm` | 22 | the one time he looks at her properly |

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_colm` | `underworld_bar` | Mon-Sun | 19:00 | 23:59 | `met_colm` | 95 | yes |

A man at the end of the bar with a delivery he is drinking through. He talks first, and he talks too much, and that is the whole of him.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 95 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`The end of the bar` — a place and an hour.
