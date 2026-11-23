# build — build, check, read, close

Build exactly what the approved card says, nothing more. Then three judges, in order: the scripts, the sheet and the guard, the reader. Then close the piece, and LO plays. (The rule pipeline, LO 2026-11-24.)

**Reads.** The approved card `games/<slug>/cards/<id>.md`, `games/<slug>/toml_phases/*.toml`, the rule list (`check.py --rules games/<slug> <id>`) and the craft rows it names.

**Writes.** `games/<slug>/toml_phases/*.toml`; rulings in `games/<slug>/NOTES.md` as `Ruling: what · why · cost if wrong`; `games/<slug>/reader/<id>.json` (through `reading.py --record`); `STATE.md` in the same turn.

## 1 · Build

`venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug>`. It refuses a piece with no approval, or whose card changed after the yes (`approvals.json`). It merges, packages the dev build (`--dev --debug`, into `output/`) and runs `check.py` itself. A small call the card didn't make goes in NOTES.md as a ruling, listed to LO at the end.

## 2 · The scripts (blocking)

`check.py games/<slug>` runs every check, and every red blocks. Its docstring says what each one checks, and `scenes.py`'s docstring says what each scene check can't see.

- **merge, reach, approvals, builds:** the build is whole, every kept scene can be reached, and everything built is on an approved card.
- **talk, length, presence, creation, saves, speakers, goals:** the measured scene checks.
- **sheet:** the card's `Sheet:` against the clock, place, who, clothes and flags worked out from the build, by meaning. A red row is never fixed by pasting `sheet.py`'s value. Per row, say which it is: (a) format only, (b) the story was wrong (fix the story, then the row), or (c) the script is wrong (stop and report). Record (b) and (c) in NOTES.md.
- **does:** the guard. What a script can see each screen do is named on its `Does:` line.

INCOMPLETE names what wasn't checked; it is never green. A card with an explicit beat also runs `check.py --beat`. Fix red in the card first, show LO the changed lines, take his yes, and rebuild. A red never goes away by editing the TOML past the card.

## 3 · The reader (blocking on its own rows)

Only once the scripts are green, on every scene piece:

1. `venv/bin/python .claude/skills/author-game-lean/scripts/reading.py games/<slug> <id>` prints the work list. On a card with `Does:` it is the rule list plus the 13 scene tests, per screen. The first pass asks every row. After that it asks only:
   - the rows on a changed screen that its triggers fire;
   - every FAIL;
   - every row whose rule changed;
   - rows never judged.
   Everything else is carried.
2. A fresh agent reads it, with `reader.md`, the game folder and the work list, and nothing else from this session. It returns verdicts as JSON, grouped by cause.
3. Record the pass: `reading.py --record games/<slug> <id> <the JSON>`. It refuses a verdict that wasn't asked, an item left out, and a FAIL with no cause.
4. Show LO the table, by cause.
   - **What blocks:** a FAIL on a `reader` or `script` row, a FAIL on a scene test, or a FAIL on the truth rule (C460, C461).
   - **What doesn't:** `note` rows are shown in their own section and never block.
   - **Each blocking cause** becomes one change to the card, shown to LO as before and after. A new yes means rebuild, back to 2.

There is no limit on passes. A piece's reading is done when `reading.py` prints an empty work list, or every FAIL left is one LO waived in NOTES.md, in his words. At release, read with `--all`.

## 4 · Close the piece

In the same turn:
- mark the piece built and checked in `STATE.md`;
- set a new `Next step:`;
- list this piece's rulings to LO.

## 5 · LO plays

Every few pieces LO plays the dev build in `output/`: "this should happen. Does it?" What he finds goes back into a card, and back through the loop.

**Commits.** LO decides when. A session commits only on his word, relayed or direct, and never pushes or merges unless he says so.

**Done when.**
- `build.py` ran, and `check.py games/<slug>` is green (not INCOMPLETE).
- On a scene piece, the reader's work list is empty, or every FAIL left is waived.
- `STATE.md` marks the piece built and checked, with a new `Next step:`.
- LO saw the reader's table and this piece's rulings.
