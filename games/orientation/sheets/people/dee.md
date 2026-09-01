# PERSON · Dee  `[READY]`

| | |
|---|---|
| **id** | `npc_dee` · **fixed name** — not customizable, so prose may write *Dee* |
| **role** | her mother |
| **home** | `the_back_bedroom` |
| **meters** | `relation` only, **2 rungs** — and they gate the kitchen window |
| **met** | funnel screen 3 · flag `met_dee` |

**Why she is in the game:** not wanted — **she is the price tag.** Every hour Ray is alone with Josie
is an hour Dee is on shift, and that is the entire reason the taboo costs anything.

⚠️ **A character with no line here has no reason to exist. Hers is that line**, and it is a
*why-she-matters* rather than a *why-she-is-wanted* — stated in the open so nobody later mistakes
the gap for an oversight.

⚠️ **A character who gates nothing is not in the game yet.** `the_allowance` shipped two of five
characters with a full meter pair and **zero** gate sites on either. Dee's two rungs gate whether
the kitchen window is quiet or watched.

---

## The schedule grid

| # | location | start | end | weekdays | activity |
|---|---|---|---|---|---|
| 1 | `the_kitchen` | 17:00 | 21:00 | `[6,0,1,2,3]` Sun–Thu | eating standing up, then keys |
| 2 | `the_kitchen` | 09:00 | 13:00 | `[4,5]` Fri–Sat | home, and awake |
| — | *(offscreen)* | 22:00 | 06:00 | Sun–Thu | on shift — **absent, not scheduled** |

⚠️ **Her absence is a scheduled fact, not a missing row.** Rows 1 and 2 are complementary: she is in
the kitchen before her shift on the nights she works, and in the kitchen in the daytime on the two
days she does not. **Fri and Sat she is home at night, which is why Ray has no kitchen window then.**

⚠️ Read across this grid and Ray's: **no hour has both of them scheduled in the kitchen** except
17:00–21:00 Sun–Thu, where the row is hers and his window has not opened. That is the check S5
exists for.

---

## Ladder — 2 rungs, no arc

Deliberate. She is the pressure, not a route.

| rung | gate | what it does |
|---|---|---|
| *be good to him* | `met_dee` | states `home_face` in a person's mouth — the meter, before the meter |
| *the questions get sharper* | `home_face lt 40` | a `[group]` band that colours every kitchen visit |

## Crude ceiling

**NONE.** She is heard through a wall and never touched. **A deliberate ceiling, declared in the
open** — a ceiling described abstractly gets written around, and an undeclared absence reads as a
thing nobody decided.
