# 0.0.1 — changes

First release. Everything is `[new]`; nothing is `[chg]` or `[gone]` because there is no previous
release to move anything from.

## Decisions signed

**Block A of [DECISIONS.md](../../DECISIONS.md) signed off by LO in chat, 2026-08-31** — narration person, who the player is, the title,
every id and slug, every meter scale. Those five cannot change once a build exists.

Blocks B and C remain changeable and were revised repeatedly during the session; the [decision file](../../DECISIONS.md)
carries the reasons inline.

## Reversals recorded during the session

Kept as a trail so nothing is re-derived:

| what | outcome |
|---|---|
| `nerve` as the player meter | **renamed** to `exhibitionism` — measured at **zero** stat uses across 28 field games |
| meter scale `0 → 24` | **wrong** — my error, conflating the scale with the rungs. Now 0 → 100, the field's modal ceiling and the engine's own clamp |
| the day as a skipped menu | **withdrawn the same day** — she picks her hours instead, and the hour became the difficulty dial |
| "written but thin" protagonist | **withdrawn** — LO's call. She is a written character |
| one need (`energy`) | **three** — energy, hunger, hygiene, each shutting a real door |
| five rooms | **seven** — the kitchen and the shared bathroom |
| the bathroom at the end of the corridor | **moved** behind the desk, to agree with the map |
| the camera monitor in the office | **moved** to the desk — it is the corruption on-ramp and cannot sit behind a door shut two nights in three |
| a day-menu, an invented rent bill | both **replaced** by things already in the fiction — hours she chooses, and the night audit |
| the opening as three beats in one canvas | **split** into boot + capstone, two canvases — `the-first-hour.md` F2 names collapsing them as the reason v2 openings run double v1's and still read thin |
| her name asked in a prose beat | **moved** to the engine's own `CustomizeCharacters` screen — see [decision 16](../../DECISIONS.md) |
| the opening's first screen | **it was never beat 1.** The age gate is screen 0 and always was (`engine.md` §12) |
| a funnel of pure narration | **the job, done once** — a guided first check-in with a choice that colours and refuses nothing |
| the 65-minute quiet stretch | **still open, but it moved** — it now falls after the funnel closes rather than inside it, and it is ~80 minutes |

## Promises made and not kept this release

- `Fix the sign` in [the lot](../../sheets/places/the_lot.md) opens nothing
- the face-down photograph in [room 6](../../sheets/places/room_6.md) opens nothing
- the bathroom walk-in is designed and unauthored
- both ladders ([del](../../sheets/people/del.md) · [marek](../../sheets/people/marek.md)) stop at rung 30 and 20 with everything above visible and locked

## What the screen walk found

The [opening sheet](../../sheets/OPENING.md) was rewritten on 2026-08-31 against a new review view,
and the view is the reason the findings exist. The old sheet specified three beats, a timeline and a
checklist — and passed all three of its own views while never saying **how many screens it was**,
**what was written on the button between them**, or **what the player saw before any of it.**

Four things the walk turned up that no other view could:

1. **The age gate is screen 0** and the old timeline opened on what is really screen 2.
2. **The engine has a character screen** — `CustomizeCharacters`, shipped by 7 of our 15 built
   games — and no sheet had ever had a row for a screen we do not author. Its text is hard-coded and
   one of the strings is a product-voice sentence sitting on the player's second screen.
3. **Boot and capstone were collapsed into one canvas**, which is the specific defect
   `the-first-hour.md` F2 was written against.
4. **The funnel had no verbs in it.** Everything up to 23:00 was narration and a name box.

**Measured before and after:** 175 words and an unstated screen count → **~830 words across 10
authored screens** (12 including the engine's two). Our v2 median is 402; our largest is
`the_allowance` at 535 across 5. The field's largest is Course of Temptation at 8,057 across 78.

## Signed off 2026-08-31 — the two open calls, both answered

**LO: "add the three explicit beats and keep the check-in."**

| the call | what was done |
|---|---|
| the explicit floor | three beats added — [`del_12`](../../sheets/scenes/del_12_reach_for_the_top_shelf.md) (tier 1), [`del_30`](../../sheets/scenes/del_30_behind_you_at_the_monitor.md) (tier 2), [`marek_20`](../../sheets/scenes/marek_20_dont_cover_up.md) (tier 2). All on repeatable surfaces, all at ceiling, all written out in full, **all three verified against `gates.py`'s regex.** ⚠️ **The floor still fails at 4.0%** — see below |
| the guided check-in | **kept.** Screens 9–11 of [the opening](../../sheets/OPENING.md) stay. It is the one piece of the funnel doctrine never asked for, and the only place she does the job instead of being told about it |

**One design consequence, recorded so it is not re-derived:** the game's first explicit beat moved
from corruption 20 (Marek, undressed) to corruption 12 (Del, fully dressed). Marek still owns the
first scene where she is not dressed. Reversible by moving that beat to `del_30`.

**One rule added to the format by this change:** every explicit beat is written out in full on its
sheet, even when the scene is not the release's voice sample. A label cannot carry a pivot test.

## ⚠️ The correction that came out of adding them

**Running the gate's word list instead of trusting the `[explicit]` label changed every number this
release had reported.**

The three beats the release already called explicit score **0, 0 and 1** against `gates.py:286`.
`hard` and `wet` are not on that list. So the release had **zero** countable explicit beats, not
three, and the figures given earlier today — 6.4%, then 4.2% — were both computed off labels.

**True history: 0% → 0% → 4.0%.** Three countable beats now exist and all three were added today.

**Two of the three new beats made the same mistake on their first write** and were rewritten before
they shipped — `del_12` swapped `hard` for `nipples`, `del_30` swapped `wet` for `cunt`. Both are
recorded inline on their sheets.

**One knock-on defect in [decision 15](../../DECISIONS.md):** Del's tier-1 ceiling is written
*tits, ass, hard*, and only two of those three count — so a Del tier-1 beat cannot clear the 3-word
floor without repeating a word or exceeding its own ceiling. Not fixed; it needs LO's call on the
wording.

**Open:** passing the floor needs the three mislabelled beats rewritten, which includes the release's
voice sample. Not done — it is prose LO has already read.