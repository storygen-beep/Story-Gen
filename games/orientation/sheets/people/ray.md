# PERSON · @ray  `[READY]`

| | |
|---|---|
| **id** | `npc_ray` · renameable by the player, so **prose uses `@ray`, never a typed name** |
| **role** | her step-father — **role before name** (F7), and the role stays attached after (F10) |
| **home** | `the_back_bedroom` |
| **meters** | `relation` (access) + `lust` (willingness) — the rich pair, because he carries an arc |
| **met** | funnel screen 2 · flag `met_ray` |
| **`relationship_options`** | stepfather · mom's husband · father · uncle → `@ray.rel` |

**Why he is wanted:** the first adult who looks at her like the room changed when she walked in, and
the one person she cannot afford to lose.

**What he owns** (R8 — a person owns a corner of the world): the house, the money, the car. Nobody
else in the cast touches any of the three.

---

## The schedule grid — place × hours × days

**0 = Monday**, 6 = Sunday (`v2.py:3906`). An empty list means every day.

| # | location | start | end | weekdays | activity |
|---|---|---|---|---|---|
| 1 | `the_avenue` | 08:00 | 08:30 | `[0,1,2,3,4]` Mon–Fri | putting the case in the car |
| 2 | `the_avenue` | 18:00 | 18:30 | `[0,1,2,3,4]` Mon–Fri | back, and not going in yet |
| 3 | `the_kitchen` | 22:00 | 23:59 | `[6,0,1,2,3]` Sun–Thu | up on his own |
| 4 | `the_kitchen` | 00:00 | 01:00 | `[0,1,2,3,4]` Mon–Fri | still up |
| — | `the_back_bedroom` | 01:00 | 06:00 | — | asleep, home only |

⚠️ **Rows 3 and 4 are ONE window split in two, and the split is mandatory.** The weekday check runs
**first and against today** (`v2.py:3596`), then the time check (`v2.py:3597`). `isCurrentTimeSlot`
handles the midnight wrap correctly — but a **day-specific** overnight row puts him on site on Sunday
night and **deletes him at midnight**, because `todayIndex` is now Monday. An all-days row would be
one row; this one is not all-days, so it is two.

⚠️ **He is never in two places at one hour.** That is what this grid is for — the incident behind S5
was one character declared 22:00–02:00 at a desk on one sheet and 22:00–02:00 in an office on
another, with nothing in the format reading across them.

⚠️ **Fri and Sat nights he has no kitchen window, because Dee is home.** The absence is the design,
not a gap: the counterweight has two nights a week where it cannot be spent.

---

## The arc — 9 steps, direction **HERS**

`the-arc.md` A5b: what climbs is **her willingness**, and the question the arc asks is *how far will
she go*. The refusals therefore belong to her.

**A2 — the first third has no sex in it.** Steps 1–3 buy the player two things and nothing else:
**when he is alone**, and **what he is vulnerable about**. Both are things the player then uses.
Information she earns is a rung; information the game narrates is exposition.

| # | step | gate | what it teaches or takes |
|---|---|---|---|
| 1 | the first Sunday she is still up when Dee has gone | `met_ray` | **when he is alone** — the window itself |
| 2 | he says what the house was like before | `ray_01` · relation 8 | **what he is vulnerable about** |
| 3 | she asks him for the dues before she is short | `ray_02` | **R5e — the OFFER.** Not gated on scarcity |
| 4 | **the refusal** — she stops it, and the game says where to come back | `ray_03` | **A3b: PARKED**, free and reversible |
| 5 | the first thing that is not deniable | `ray_04` · `home_face lt 60` | the counterweight starts paying |
| 6 | he asks her to do it again, in the same chair | `ray_05` · lust 15 | |
| 7 | she asks first | `ray_06` · appetite 30 | the direction flips inside the arc |
| 8 | the night Dee's shift is cancelled and it happens anyway | `ray_07` · `home_face lt 40` | |
| 9 | **conversion** — the kitchen row appears | `ray_08` | sets `ray_open` |

**Step 3 is the ignition and it is the one two other games got wrong.** Both wired the same offer
behind a *lack* — `money lt 260`, `prep lt 30` — making it near-unreachable, and neither author was
careless: the doctrine had nothing for a choice offered **before she needs it**. Three of the four
corpus games with an obligation let her volunteer for a bigger one and **not one gates it on
scarcity**. Test: **can she take this when she doesn't need to?**

**Step 4 is PARKED, not counted.** Free, reversible, and the game prints the place and the hour:
*if she changes her mind, the kitchen, after her mother has gone.* The counted-and-closed shape is
for when the closing is itself content, and this is not that. **The one thing neither shape does is
stay silent about which it is.**

**A4 — each step grants the meter that opens the step after it, capped at the next threshold**, so
replaying step 5 at the bottom walks her up to step 6 and then stops feeding it.

⚠️ **Separate the grant band from the hub's existing `relation` ladder with a non-`group` block.**

---

## The converted surface — `the_kitchen` · *Sit up with him*

Opened by `ray_09`. **The repeatable surface is the reward for finishing the arc, not the starting
position** — which is the thing this repo has never once built: zero arcs across twelve games and
1,396 canvases, every act loop authored in its converted state on day one.

**BRAKE:** `trigger.costs rest 12` · day-cap `kitchen_late_today` **set on the choice** · his window.

**A10 — the aftermath**, ~32 words, written for him and no one else: how he leaves, what she is left
holding, and the offer to stay or go. **A11 — the stop beat**, about how *he* takes being stopped.

## Crude ceiling

| tier 1 | tier 2 | tier 3 |
|---|---|---|
| tits · ass · hard · his cock through the seam of his jeans | cock · cunt · wet · suck · fuck | full — cunt, cock, cum, throat, fuck, come in her |

A ceiling, never a floor. Writing under it is a defect.
