# 0.0.1 — in short

**Status: [GAME-READY]. Built 2026-08-31. 39/40 gates green, 35/35 canvases in the build.**

## Measured — from the BUILD, not from the sheets

<pre>
canvases                35        35/35 reached the build
beats (nodes)           52        ⚠ the sheets said 75 — different unit, see BUILD_VS_SHEET
  repeatable            41
explicit beats           6        14.6% of repeatable · 11.5% of all
                                  floor 7.5% — PASSES
words                4,590        the sheets estimated ~3,670
rooms                    7        5 · 4 · 4 · 3 · 3 · 2 · 0 things to do
people                   2        10 schedule rows
walk-ins                 5        the sheets deferred all of them
quest cards              9        the sheets have no row for these at all
gates                39/40        only `location fill` is red
</pre>

⚠️ **The sheets and the build disagree about what a "beat" is**, and that is the largest single
finding of the experiment. The sheets count paragraphs; `gates.py` counts nodes. Every headline
figure this release reported before the build was in a unit the instrument does not use.
[`BUILD_VS_SHEET.md`](BUILD_VS_SHEET.md) §1.

**Against a seed: 2.3%.** DoL's first release was 116,540 words across 25 locations.

## What it is

*Sheets: [places](../../sheets/places) · [people](../../sheets/people) · [scenes](../../sheets/scenes) · [the opening](../../sheets/OPENING.md). Longer read: [LONG.md](LONG.md).*

- One motel, seven rooms, two men, and she cannot leave.
- **The opening is twelve screens** — age gate, the engine's character screen, two of setup,
  two that name the game and the room, three of Del handing over, and three where she does the job
  once with the money landing in her hand.
- Del is slow because he has something to lose. Marek is fast because he does not.
- **The first explicit beat is Del's, at corruption 12, on about night two** — she is fully dressed
  and it is his shelf. The first scene where she is *not* dressed is still Marek's, in the shared
  bathroom, on about night three.

## What is wrong with it

1. **The explicit floor still fails, at 4.0%.** Three beats were added on LO's call
   (`del_12` · `del_30` · `marek_20`) and all three count. **But the three the release already had
   never counted** — see above. Passing needs those three rewritten too. **Your call.**
   ⚠️ Underneath it sits a **measurement** problem, still open: the explicit floor divides by every
   beat in the game, so a big well-built opening dilutes it. ⚠️ I first blamed `the-first-hour.md`
   F4b for this and that was wrong — F4b is about refusals, not heat.
   [`SKILL_CHANGES_OWED.md`](../../SKILL_CHANGES_OWED.md) §11.
2. **It is 2.3% of a seed.** This is a slice to test a review loop, not a shippable release, and it
   should not be called one.
3. **Eighty minutes of the first night — 23:00 to 00:20 — has nothing arriving.** It moved and
   grew when the funnel got longer, but it now falls *after* the opening closes rather than inside
   it, which is the half of the problem that mattered.

## Owed to later releases

- `Fix the sign` in [the lot](../../sheets/places/the_lot.md) opens nothing
- the face-down photograph in [room 6](../../sheets/places/room_6.md) opens nothing
- the [bathroom](../../sheets/places/the_bathroom.md) walk-in is designed and not authored
- every top rung on both ladders is locked and visible, which is correct for one release and a
  broken promise by the third
