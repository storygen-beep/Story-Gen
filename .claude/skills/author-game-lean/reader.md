# reader — judges a built scene piece before LO plays it

**Who runs it.** A fresh agent (the Agent tool, general-purpose), given this file, the game folder and the piece id, and nothing else from the session. It never saw the build: the one who checks is never the one who built. It reads. It never writes under `games/`, never fixes, never scores, never ranks.

**Input.** `games/<slug>`, a piece id whose `Builds:` names at least one canvas, and the work list: `venv/bin/python .claude/skills/author-game-lean/scripts/reading.py games/<slug> <id>` (the session runs it and hands over its JSON). Judge only the work list's items, each a row on a screen (`<canvas>.<node>`, or `*` for wherever the row applies). Everything else was judged before on the same text and is carried. At release, or when LO asks, the session runs it with `--all`. Why: every P13 pass, v5 to v11, judged everything again, and a row passed on one pass and failed on the next on unchanged text (LO, relayed 2026-11-24).

## Reads

- `games/<slug>/cards/<id>.md`: what the card promised, its `Builds:` and its `Craft:` lines.
- Every craft file the `Craft:` line names (`.claude/skills/author-game-lean/craft/*.md`), and the craft file for any area the piece touches that the card left out (`craft/opening.md` for the opening, `craft/meters.md` for a meter or an act that pays one, `craft/media.md` for any media spot, `craft/walk-ins.md` for a scene she walks into or someone walking in on her, `craft/body-moments.md` for a moment alone with her body). A craft file the card should have named and didn't is itself a FAIL, and so is an area the scene touches that the card's `Areas:` line doesn't name.
- `craft/voice.md` for the voice and "The truth rule", on every scene piece. The writer reads the same text (`piece.md` step 3).
- The canvases in `Builds:`, from `games/<slug>/toml_phases/7_final_game.toml`.
- `games/<slug>/PLAN.md` and `games/<slug>/NOTES.md`.
- Who is where: `venv/bin/python .claude/skills/author-game-lean/scripts/who_is_where.py games/<slug>`.

## The tests

**A · Craft.** Every must-read row of every craft file above, judged on the built scene, and every numbered step of each file's "The shape". One verdict per row and one per step, with the line it was judged on. Judge the row's or the step's own words, not whether the card cited it: a card can cite a row and still break it. A step the scene does thinly is a FAIL, not a PASS with a note (the first reading of P13 passed a one-sentence build-up this way, 2026-11-20).

How three rows are read (the false-red test on the old first_term opening, 2026-11-20):
- **Length (C519, C520):** a FAIL is a screen with more than one job, or over about 150 words. 34–57 is a target, not a FAIL.
- **C109 on a person's first scene:** there is no step before it, so the leak half is N/A; judge only the promise the scene ends on. His look, caught and covered, is judged at C601, not here.
- **C1604:** judge the objective cards showing at the hand-over, the ones that tell her what to do. A person's card on the people page is not one.

**B · The scene** (from `v2-reader`'s tests, plus test 13; `PLAN.md` stands in for WANT.md and the v2 ledger):

1. **want:** the person visibly wants something here. On a sexual step, an earlier canvas already showed him wanting it. Name the canvases you checked.
2. **next step:** something goes one step further than the last scene with this person.
3. **hook:** the scene points at what comes next: a line, a promise, a choice that names it.
4. **her voice at her level:** her reaction matches her meter: pushback at a low level, appetite at a high one, on her body and in what she says, never in an italic thought (`craft/voice.md`). At stage 0–1 she reacts; it never chooses an act her stage hasn't opened (L71).
5. **who notices:** someone reacts to what she does, or PLAN.md declares nobody does.
6. **the written no:** where she gets an offer, a refusal exists, is written and lands somewhere. A final no ("(ends his path)") on a main arc's first step, or in the opening, is a FAIL (C166).
7. **the body:** an explicit beat's last sentence is about what is happening, not what it means.
8. **the numbers and the clothes agree:** every number agrees with PLAN.md and the other cards; every garment the prose names is backed by a clothing condition or an equip before it.
9. **companion and rival:** only where PLAN.md declares the companion is the rival.
10. **true on every visit:** read each line at the first and last minute it can show, and on the second visit. Who it says is there is there (who_is_where). A past it names is behind its flag. A "first time" is behind a seen flag.
11. **a solo button is a real act:** it changes something she or the game can see, or shows the act it names.
12. **low heat is on the body:** a charged scene with no explicit beat names a part of her body, writes his reaction, and holds a "not yet" or a price (C311). Talk only is a FAIL (C314).
13. **a moment alone with her body is a body moment:** a shower, dressing or undressing, the towel, bed or the mirror stays on her body and has a picture of her. Written as a chore (no body, or no picture), or skipped ("Back in your room, dressed"), is a FAIL.

## Output

Two files in your scratchpad, both returned:

1. `reader_<slug>_<id>.json`, one verdict per work-list item, for `reading.py --record`:
   ```
   {"verdicts": [{"row": "C460", "screen": "opening.kitchen_ask", "verdict": "FAIL", "line": "<quoted, short>",
                  "why": "<one line>", "cause": "c1"}],
    "causes": [{"id": "c1", "what": "<the one thing that is wrong, in one line>"}]}
   ```
   An item asked on `*` may be answered on one or more screens. Verdicts are PASS, FAIL, N/A, or WAIVED for a FAIL LO waived in NOTES.md (quote his words in `why`). Every FAIL names a cause; one cause covers every row it breaks, so three rows broken by one line are one cause, not three.
2. `reader_<slug>_<id>.md`: the same verdicts as a table, `row | screen | verdict | the line judged | why`, then the FAILs grouped by cause, one head line per cause and its rows under it.

A FAIL you can't quote a line for is N/A, and you say why. No fixes, no severity, no score.

## After (the session, not the reader)

The session records the pass: `venv/bin/python .claude/skills/author-game-lean/scripts/reading.py --record games/<slug> <id> <the JSON>`. It refuses a verdict that wasn't asked, an item with no verdict, and a FAIL with no cause, and it writes `games/<slug>/reader/<id>.json`. Then it shows LO the table, by cause. Each cause becomes one change to the card, shown to LO as before and after. A new yes means rebuild, then `reading.py` again: it asks again every row on a changed screen, every FAIL, and every row whose rule text changed. The pass is over when the work list is empty. There is no limit on the number of passes. LO plays a piece only when its work list is empty, or every FAIL left is one he waived. A waiver goes in NOTES.md in his words.

What the work list can't see: a number in PLAN.md or another card, or what another canvas does to her clothes before a repeatable. Re-read with `--all` when one of those changes. Everything on the screen's sheet row (clock, place, who, wearing, flags) is in its hash, so a change there re-opens it.
