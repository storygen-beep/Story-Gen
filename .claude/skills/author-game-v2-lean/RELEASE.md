# Prepare and ship a release

`R` is `.claude/skills/author-game-v2/references/`. `RCHECK` is
`python3 .claude/skills/author-game-v2-lean/scripts/release_check.py`. `CHECK` is the edit check from
[CHANGE.md](CHANGE.md).

A release has two halves. **Preparing** it is yours. **Shipping** it waits for LO: LO plays it and
signs, and only then is it built and published. You stop at the line between them.

## Prepare

**1 · Snapshot.** Run `RCHECK <slug> --start` and `CHECK <slug> --start`.
Done when both print `START`.

**2 · Know what the release is.**
- If LO named the content, that is the release.
- If not, run the pitch: three `v2-pitcher` agents in one message, two on the most-owed relationships
  and one on a thread of her life (`R/the-release.md` "The loop", step 2). Show LO the three and **stop
  until LO picks one.**

Name the line of the Want the release serves.
Done when the content and the Want line are both stated.

**3 · Write it.** Follow [CHANGE.md](CHANGE.md) steps 2–4 for the content.
Done when `CHECK <slug>` prints `CLEAN`.

**4 · Fill the release page** in `v2_state.json` `release_page` (`R/state.md`, `release_page`):
- `version`: the new version. Bump the third number for a fix or a small addition (0.1 → 0.1.1) and
  the second for a new step or person (0.1 → 0.2). Set the same value in `[project] version` in the
  TOML.
- `people`: every person this release moves, as NPC ids.
- `door`: `{ canvas, choice }`, the locked choice the release ends on. If `board.door` is also set,
  make it the same value.
- `her_moment`: the step this release pays, when it has one.

Done when all four are written.

**5 · Read every touched canvas.** Run the `v2-reader` agent on each canvas this release changed
that has a named person or an explicit beat (`R/the-release.md` step 6b). Save its verdicts under
`release_page.reader`. Fix a FAIL in the scene. A FAIL that should stand goes to LO, who decides
whether to waive it (`release_page.reader_waivers`); you never write a waiver yourself.
Done when every touched canvas has fresh verdicts and every FAIL is fixed or with LO.

**6 · Check.** Run `RCHECK <slug>`.
Done when it prints `READY FOR LO`. On `RED`, fix each line at its cause and run it again.

**7 · Hand over.** Tell LO the release is ready to play: the version, the people, the door, and the
`RCHECK` to-do lines. **Stop.**

## Ship — only after LO has played it and signed

LO signs by setting `release_page.signed_by_lo` and `signed_at`. If LO tells you they have played
and approved it, you may record that for them. Then follow `R/the-release.md` "Ship" steps 1–8 in
order:
1. Rebuild without `--dev` or `--debug`.
2. Archive the build to `releases/v<version>.html`.
3. Set the portal `version` and drop `dev: true` in the same commit.
4. Run `gates.py --ship <slug>` until it exits 0.
5. Log the release in `releases[]`: `version`, `subject`, `want_line`, `moment_kind`, `her_moment`,
   `added`, `opened` (never empty), `shipped`, `commit`, `repeatables` and `ladder_steps`
   (`R/state.md`, `releases[]`).

## Footguns

- **Ids are permanent once a version has shipped.** A canvas, location, NPC, clothing, quest or job id
  never changes; change its `name` or its prose instead. Deleting a node inside a canvas is safe.
  If LO asks for a rename on a shipped game, explain this and keep the id. (`R/the-returning-player.md` §2)
- **Flag and trait keys are permanent too.** To retire one, leave it where it is and add the new key
  beside it ("deprecate and add"). (`R/the-returning-player.md` §3)
- **Never sign for LO**, never mark a release `shipped`, and never write a reader waiver. Those are
  LO's.
- **The version lives in three places** that must agree: `[project] version`, `release_page.version`,
  and at ship time the portal entry and the archive name. (`R/the-release.md` "The three places that
  say what shipped")
- **The door hangs on a meter rung this release can't reach**, not on a flag that nothing sets yet:
  the build refuses a choice gated `is_true` on a flag with no setter (`package_from_toml.py:562`,
  `v2.py:12793-12801`).
- **A stale reader verdict is not a verdict.** A canvas you touched gets read again.
