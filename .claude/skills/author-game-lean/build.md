# build — build, check, close

Stub. Filled in during Phase 3.

**What it is.** Build exactly what the approved card says, nothing more, then check it and close the piece.

**Reads.** The approved card `games/<slug>/cards/<id>.md`, `games/<slug>/toml_phases/*.toml`.

**Writes.** `games/<slug>/toml_phases/*.toml`; rulings in `games/<slug>/NOTES.md` as `Ruling: what · why · cost if wrong`; `STATE.md` in the same turn.

**Done when.** `venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug>` ran, `venv/bin/python .claude/skills/author-game-lean/scripts/check.py games/<slug>` is green (not INCOMPLETE), `STATE.md` marks the piece built and checked with a new `Next step:`, and this piece's rulings were listed to LO.
