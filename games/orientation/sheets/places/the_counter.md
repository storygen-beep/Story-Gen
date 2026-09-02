# PLACE · The Counter  `[READY]`

| | |
|---|---|
| **id** | `the_counter` · button `Counter` |
| **ENTERED FROM** | `the_quad` |
| **FILL** | 3,500 words |
| **cycling pool** | yes — `sex/counter_backroom_t5`, pool 5 |

## What kind of place this is
The coffee counter on the ground floor of the union building. **The only place money comes from**,
and the back room behind it is one of the five surfaces the crude register lives on.

## The list
| row | system |
|---|---|
| **Take a shift** | work — the only income channel |
| **Eat on shift** | needs — `fed`, $4, 15 min |
| **Go in the back room** | ascent — `nerve`. **The repeatable act surface** |

## The shift — income, and the brake on it
Gate *no free uncapped income*: **every income surface has a brake on every route in.**

```
trigger.costs           rest 20
day-cap flag            shift_today   ← SET ON THE CHOICE
window                  Mon-Sat 10:00-16:00
pays                    $42-58 a shift  ->  ~$260 a week at six shifts
```

⚠️ **$260 is the honest maximum against a $120 obligation — 46%.** Measured across every game we have
built, **eight of ten clear the whole week's obligation in under one day of the best job**, median
0.48 days. The instruction to price it in both directions existed for months with **no field to
write the arithmetic in**; `board.economy.week_income` is that field.

⚠️ **R3c — if the demand rises, the income has to rise with it.** *"Here u still grind for nothing"*
is the corpus's single most-punished design. When a commitment adds weekly upkeep, a better-paying
variant of this shift unlocks on the same flag, with the original kept behind the flag's `is_false`.

## The back room
**BRAKE:** `trigger.costs rest 10` · day-cap `backroom_today` **on the choice** · shift window only.

**A12 — the reason she is there is a SYSTEM, not a sentence.** Two routes in, and they are not one
scene with two openings: **a price somebody paid** (a regular who tips in a way that is a number) and
**an accident she did not intend** (the stockroom door and who else has a key). Each brings its own
negotiation, its own refusal and its own aftermath.

## Walk-in
**Required.** `walkin_backroom` — the shift bell goes while she is in there.

## Ways out
`the_quad`
