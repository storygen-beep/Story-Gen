# media_lab_b — arm B of the Q2 A/B

Not a game. The **second arm** of an experiment about whether find-media's *ranking* step is
worth anything.

- **Arm A** = `games/media_lab/`, filled by **`find-media`** — gates + strip, then HEAT /
  SETTING / CRAFT scoring picks the install.
- **Arm B** = this game, filled by **`find-media-b`** — gates + strip only. **No scoring.**
  The install is simply the *first* candidate that passes correctness. No taste applied.

Ten identical beats, identical descriptions, identical `search_queries`, and — deliberately —
**the identical candidate shelf** (`.find-media/media_options.json` was copied from arm A, so
neither arm benefits from a luckier Google day). The judging rule is the only variable.

The question it answers: **does ranking beat not-ranking?** LO compares the two install sets
directly. It is not blind and it is n=10 with one judge, so a close result means nothing —
only a lopsided one does.

## Rules

- **⚠️ Never run `scripts/merge_toml_phases.py` here.** Its `OUTPUT_FILENAME` is
  `7_final_game.toml`, so a merge would overwrite this hand-written file with an empty one
  built from phase files that do not exist. Same trap as arm A.
- **Never edit the slots, descriptions or `search_queries`** unless the identical edit lands in
  arm A in the same commit. They are the experiment's constants. That includes the three
  old-doctrine control queries — they stay, for parity.
- The study key (which three slots carry the old-style queries, and what each slot probes)
  lives in `games/media_lab/STUDY_KEY_do_not_read_before_hunting.md`. Not duplicated here.

Arm A's findings and per-slot reasoning: `games/media_lab/.find-media/FINDINGS.md`.
