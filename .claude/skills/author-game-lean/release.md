# release — check, read, play, media, ship

Stub. Filled in during Phase 3.

**What it is.** Close a release once every piece in it is checked, in this order:

1. `venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug> --release` (merges with `--no-dev`, `scripts/merge_toml_phases.py:80`), then `venv/bin/python .claude/skills/author-game-lean/scripts/check.py games/<slug> --release`, which is red if any canvas from `6_dev_shortcuts.toml` is in the release output;
2. the reader on this release's scenes;
3. LO plays the whole release;
4. the media search, only after LO says "release ready";
5. ship.

**Reads.** `games/<slug>/STATE.md`, `games/<slug>/approvals.json`, the built game in `games/<slug>/output/`.

**Writes.** The reader's verdicts; one `STATE.md` line for the shipped release (what shipped, the date, the commit LO made); `NOTES.md` lines for LO's calls.

**Done when.** LO has played the release and said it ships, LO has committed it, and `STATE.md` has the release line and `Next step: plan — release <n+1>`.
