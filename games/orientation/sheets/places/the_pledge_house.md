# PLACE · The Pledge House  `[READY]`   **⭐ ANCHOR**

| | |
|---|---|
| **id** | `the_pledge_house` |
| **name on the button** | `Pledge House` — public venue, bare noun, no article |
| **ENTERED FROM** | `the_quad` |
| **FILL** | **11,500 words · 25.6% of the world** — declared before the prose |
| **cycling pool** | yes — `sex/pledge_upstairs_t5`, pool 6 |

⚠️ **The anchor is a RATIO.** 11,500 is its share of the **finished 45,000**, not of whatever is
written today. Put that share into every increment. One build watched its anchor fall 53% → 35%
without losing a word, going 9/10 → 8/10 while getting objectively better.

---

## What kind of place this is

Third house along the row on the east edge of campus. Twelve girls live in it, Simone runs it, and
there is a sign-in book on a table inside the door that everyone signs and nobody reads. Downstairs
is public. Upstairs on a party night is not.

**F9 — the description says the FUNCTION first.** A player who has never been here has to learn from
the room screen that this is *where you get taken in, and where you pay for it* — before it says
anything about the carpet. The measured failure declared its anchor at 27% of the word budget and
opened its description *"…and under them forty machines"*, and the first thing a human reader asked
was what the place is.

---

## The list — needs + work + people, and every row is a system

`the-surfaces.md` **R2 / R2c**. Six rows, and each one is a system from `SYSTEMS.md` surfacing here.
Nothing is invented from the fiction.

| row | system | notes |
|---|---|---|
| **Sign the book** | arc flags — `simone_01` | one-time. The meeting. Gone after it fires |
| **Talk to the woman who runs it** | cast — `npc_simone` hub | her ladder, one rung at a time |
| **Hand over the dues** | money — the obligation | Friday 17:00–19:00 only |
| **Shower here** | needs — `clean` | $2. The reason it costs is that it is not her house |
| **Go up** | ascent — `nerve` / `appetite` | party nights only. **The repeatable act surface** |
| **Sit where they can see you** | ascent — `reputation` | the quiet outcome pays: +time, and sometimes nothing |

⚠️ **Six rows because six systems live here**, not because six is a good number. The field median for
things-to-do-at-a-place is **3**; the cap of 8 is a backstop and not a target. A game built after
that cap put **19 of its 30 screens at exactly 8** and shipped the same 213 choices as the game the
cap was written to fail.

⚠️ **The object test, on the hub rows only.** *Talk to the woman who runs it* → a person is the
object ✓. *Hand over the dues* → **not a hub rung**; it is the obligation, its own surface. The
23-choice failure had a hub binding no NPC at all and every one of its choices was work wearing a
menu item's clothes.

---

## Go up — the repeatable act surface

This is **where the crudest writing in the game lives** (Want §7), and it is re-entered, not seen
once. Opened by `simone_07`, which is the last step of her arc — the surface is the **reward for
finishing the arc, not the starting position.**

**BRAKE** (S9 — on the way IN, on the trigger, never on an inner choice):

```
trigger.costs                 rest 15
day-cap flag                  went_up_today   ← SET ON THE CHOICE, cleared in [engine.daily_tick]
schedule window               Thu/Fri/Sat 21:00-02:00 only
```

⚠️ **The day-cap flag is set on the CHOICE, not on the rung's exit.** `advanceTime` rolls the day
inside itself (`v2.py:5411-5414`) and the tick clears `_today` flags there (`v2.py:5552`), so an
exit-set cap on a rung crossing midnight starts the new day already capped. A 21:00→02:00 window is
exactly that case. 40 caps in this repo sit on an exit and 35 of those are in two games written under
the old example.

⚠️ **One unbraked door makes the whole rung farmable no matter how well priced the other doors are.**
Three rounds of adding costs to inner choices once moved nothing; moving the same costs to the
triggers fixed five meters at once.

**Text varies on re-entry** — `block_pool` for undirected variety, stacked `group` bands for directed
variety on `nerve`. `block_pool` runs 46 times in `the_long_summer` and **zero times in every v2
game**; v1 had a numbered rule for it and v2 lost it. A repeatable surface written as one paragraph
is dead by the third visit.

**A10 — the act ends on a written beat.** ~32 words, no sex in it: how she is left, and the offer to
stay or go. **23 of 23 finish nodes across six v2 games have an empty `exit_block`.** This one does
not.

**A11 — a stop beat**, about *how Simone takes being stopped*, not about her exit.

---

## Sit where they can see you — the quiet outcome

**A7.** Most visits produce nothing, the nothing is written **five ways**, and it returns something
she wanted anyway — 30 minutes and a `reputation` tick. A place where something always happens has
no tension in the click.

Dispatch depth target: **5**. The deepest dispatching activity in this repo turns into 5 things; in
two games *every* dispatching activity has exactly one outcome, so the roll decides only whether the
branch fires and never which branch it is.

⚠️ **A8 — a pending arc beat pre-empts the dice.** Simone's next step, if its conditions hold, fires
as a one-shot at this location with a `priority` above the ambient. Entry-time auto-fire redirects
before the location screen renders (`v2.py:4921`) and takes the highest priority (`v2.py:4633-4634`).

---

## Walk-in

**Required — gate `the walk-in floor`.** She showers here and Simone is scheduled here. A room where
she works or washes alone with someone scheduled carries a walk-in, and **a sheet may not defer it**
(S6: a bathroom sheet once said *"named here so it is not forgotten"*, and the gate failed 0/5).

`walkin_shower_simone` — fires on `clean` restore when Simone's window is live. Two exits: cover, or
do not. **Do not cover** is a `nerve` rung and it is where `A6b`'s distinction lands — showing on
purpose is not showing by accident, and they are two beats, not one beat with a modifier.

---

## Ways out

`the_quad` (the only door). Reachable on foot, so gate *world reachable* holds.

## Media

| slot | kind | why |
|---|---|---|
| `sex/pledge_upstairs_t5` · pool 6 | **video pool** | repeatable explicit — **never** a single `file`. Gate 4 |
| `sex/pledge_shower_t4` · pool 4 | video pool | the walk-in, re-enterable |
| `locations/pledge_house.jpg` | image | the room plate |

⚠️ **`_t4` / `_t5` in the filename is how downstream tooling knows the slot is explicit.** An
untagged explicit slot is read as safe and mis-sourced.

⚠️ **An explicit beat carries a clip of its own** — on the beat the player is reading, not on the one
above it.
