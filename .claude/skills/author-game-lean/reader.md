# reader — judges a built scene piece before LO plays it

**Who runs it.** A fresh agent (the Agent tool, general-purpose), given this file, the game folder and the piece id, and nothing else from the session. It never saw the build: the one who checks is never the one who built. It reads. It never writes under `games/`, never fixes, never scores, never ranks.

**Input.** `games/<slug>` and a piece id whose `Builds:` names at least one canvas.

## Reads

- `games/<slug>/cards/<id>.md`: what the card promised, its `Builds:` and its `Craft:` lines.
- Every craft file the `Craft:` line names (`.claude/skills/author-game-lean/craft/*.md`), and the craft file for any area the piece touches that the card left out (`craft/opening.md` for the opening, `craft/meters.md` for a meter or an act that pays one, `craft/media.md` for any media spot, `craft/walk-ins.md` for a scene she walks into or someone walking in on her, `craft/body-moments.md` for a moment alone with her body). A craft file the card should have named and didn't is itself a FAIL.
- `.claude/skills/author-game-v2/references/register.md`, "The voice — say it loud" and "The truth rule". CLAUDE.md names it the register for every game until `craft/voice.md` exists (`LATER.md`).
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
4. **her voice at her level:** her thought matches her meter: pushback at a low level, appetite at a high one. At stage 0–1 her thought reacts; it never chooses an act her stage hasn't opened (L71).
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

One table, written to your scratchpad as `reader_<slug>_<id>.md` and returned:

```
test | PASS / FAIL / N/A | the line judged (quoted, short) | why (one line)
```

Then one line per FAIL, grouped by test. A FAIL you can't quote a line for is N/A, and you say why. No fixes, no severity, no score.

## After (the session, not the reader)

The session shows LO the whole table. Each FAIL becomes a change to the card, shown to LO as before and after. A new yes means rebuild, then the reader again. LO plays a piece only when its reader table has no FAIL he hasn't waived. A waiver goes in NOTES.md in his words.
