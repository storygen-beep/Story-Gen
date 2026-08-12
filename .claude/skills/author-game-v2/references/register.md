# Register — how to write an explicit beat

This file exists because the same failure happened three times in three consecutive increments,
authored by the person who wrote the doctrine against it. The skill said **where** the crude
register lives and **which words** were permitted, and nothing at all about **how to write the
beat**. That gap is what this closes.

It is short on purpose. Everything here came from a measured failure.

---

## The rule

> **An explicit beat stays on the body for its whole length.**

Not "contains a crude word". Not "is about sex". **Stays on it** — from the first sentence to the
last, the beat is describing what is physically happening to whose body.

---

## The diagnostic that catches it while writing

> **Read the beat's last sentence. If it is about what the moment MEANS rather than what is
> HAPPENING, the beat has pivoted and it will score 0–1.**

Every single failed beat did this. The shape is always identical: name one body part, then leave
the body for the rest of the beat.

**The three pivot targets, named so they are catchable:**

1. **He knows.** *"…and he does not stop, and it is you who steps back, and it is you whose face
   is burning."*
2. **She is ashamed.** *"…and you lie there afterwards deciding not to have noticed what did it."*
3. **What this says about her.** *"…and the arithmetic does not come out the way it is supposed
   to."*

All three are good sentences. All three belong in the game. **None of them belongs at the end of
an explicit beat.**

---

## Where the interiority goes instead

Its own beat, *after*. A `thought_bubble` following the act is correct and is the register
working. The same thought folded into the act is the defect.

```
beat 1   the body, start to finish, three-plus named            ← explicit
beat 2   what it meant, what she is going to do about it        ← interiority
```

Splitting them costs nothing — cascade beats are free — and it fixes the score without
sacrificing a single line of the psychology, which is the part that makes the game good.

---

## What the fix is NOT

**Not word-stuffing.** Eleven rewrites moved a game from 7.5% to 9.4% without adding one
gratuitous noun. The words arrived because the camera stayed on the body long enough to need
them, not because they were sprinkled in.

**Not loosening the wordlist.** `come` was excluded from the frozen list because it matches "come
downstairs" everywhere. When prose scores low, the prose is what is wrong. The list has been
challenged twice and was right both times.

---

## The measured targets

| | |
|---|---|
| per explicit beat | **3+ words from the frozen list** |
| across the whole game | **7.5–9.3% of beats carry 3+** |

The band is the reference game's, held across eight years and twelve-fold growth.

> ⚠️ **It is a FLOOR. Its upper comparison is meaningless — do not read a game scoring far above it
> as "too hot."** That reading has been wrong twice and cost one game a dilution pass it never
> needed. Two independent reasons, both measured 2026-08-12:
>
> - **Different denominators.** The 7.5–9.3% band counts whole-source *passages* — combat, systems
>   and UI included, 15,587 of them. `gates.py` counts beats in **location prose only**. Not the
>   same scale, so the two numbers were never comparable.
> - **The reference is the coldest game in its own genre.** Across 18 shipped sandboxes scored on
>   this exact word list, the field median is **33.3%** of prose passages carrying 3+ — and the
>   reference game is **last, at 7.5%**. The floor is a property of that one game, not of the genre.
>
> Clear it. Do not aim at it, and never dilute to approach it from above.

---

## Sweeping backwards: drive it off the MEASUREMENT, never off a category

The first backward application of this rule moved a game **10.8% → 15.9%** by rewriting "the three
repeatable sex loops". That worked, and it left the job half done: four canvases in the
protagonist's own bedroom — the solo surface, the wall, the door, the wardrobe — were written the
day before the rule existed, were never in the named category, and sat under the floor through two
further increments while the headline number went up.

Measured a fortnight later, every beat in that room scored **0, 1 or 2**. The only sex surface in
the game she initiates alone scored **1 · 1 · 0**.

> **A category name is not a sweep. Score every beat, sort ascending, and fix everything under 3.**

The instrument already prints per-beat scores; there is no reason to select by intuition.

**One thing the per-beat numbers will show you that looks wrong and is not:** the interiority beat
*after* an explicit one scores 0, correctly and by design. Do not "fix" it. What you are hunting is
the beat that scores **1 or 2** — that is a beat trying to be explicit and pivoting off the body
partway, which is exactly the defect. A 0 next to a 4 is the rule working.

---

## The habit this is fighting

The pivot is not carelessness. It is a *literary* instinct — the trained move of ending a
paragraph on significance — and it is correct almost everywhere else in writing. Here it is the
single most reliable way to produce a game that is explicit and cold at the same time.

It reasserts itself the moment it is not being actively fought. Assume you are doing it, and
check the gate.

---
---

# The other ninety percent

Everything above is about the explicit beat. Most of a game is not one. These rules cover the rest,
and they are measured across 18 shipped sandboxes rather than asserted — corpus and limits in
`DOCTRINE_GAPS.md` Appendix C.

*(This file governs what the player reads **after** a click. The room names, button labels, guidance
cards and locked-door text are a different job with a different rule — `references/the-voice.md`.)*

## Sentences run short

| | median sentence |
|---|---|
| field, 17 games | **10 words** |
| the reference game | **9 words** |
| a game of ours, measured | **16 words** — third longest of eighteen |

**Escalate by adding beats, never by lengthening sentences.** This is the same rule as the
beat-count one, one level down: a longer sentence buys density, and density is what rots on the
third re-read of a surface the player returns to fifty times.

Gate 19 puts the ceiling at 14 — deliberately generous, and calibrated across two extraction bases,
so treat a pass as "not drifting" rather than as "matches the field." The constant in `gates.py`
carries the full caveat.

## Second person is the genre standard

**13 of 17 games are second-person dominant.** Third person is a minority position held by three.
Our own most-second-person game runs 94% *you / your*.

`[settings] narration_person = "second"` is the default for a reason, and the field confirms it.
It stays **immutable once a release ships** — a person swap invalidates every line already written.

## Dialogue: a direction, not a threshold

The field spread runs from 2.7:1 narration-to-dialogue to over 400:1, which is far too wide to
threshold and is not gated. What the corpus does show: **the two most prose-dense games in it are
the two most dialogue-heavy.** Writing that is spoken rather than narrated scales; writing that
narrates at the reader does not.

Prefer a line of speech to a sentence describing a line of speech. That is the direction, and there
is deliberately no number attached to it.

## What is not measured here

Whether the writing is any good, and whether it arouses. Neither is countable, both are the job.
`gates.py` measures shape. It cannot tell you the scene works.

