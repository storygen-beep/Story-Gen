# Build from the signed sheets

`R` is `.claude/skills/author-game-v2/references/`. `SCHECK` is
`python3 .claude/skills/author-game-v2-lean/scripts/sheet_check.py`. `CHECK` is the edit check from
[CHANGE.md](CHANGE.md).

The sheets in `games/<slug>/sheets/` are LO's signed design. The build turns them into TOML. A fact on
a signed sheet holds; when a sheet and this skill disagree, or a sheet is silent, you stop and ask LO
(`.claude/skills/author-game-v2/SKILL.md`, S12 and S13). Nothing is built from a sheet LO has not signed.

## Steps

**1 · Check the sheets.** Run `SCHECK <slug> --start` and `CHECK <slug> --start`.
`SCHECK` lists every sheet that is not `[READY]` and signed ("Signed by LO" under the title).
Done when every sheet you are about to build from is signed. If one is not, **stop and tell LO which
sheet needs signing.** If the work needs a place, person or scene that has no sheet at all, **stop**:
write a draft sheet in `games/<slug>/proposals/` from `.claude/skills/author-game-v2/templates/sheets/`
and ask LO to sign it.

**2 · Build in the sheets' order:** systems, then places, then people, then scenes, then the opening
(`R/the-sheets.md` review order).
- **ids come from the sheet file names:** `places/members_floor.md` is `[[locations]] id =
  "members_floor"`, `scenes/noor_02_the_pool.md` is the canvas `noor_02_the_pool`,
  `people/noor.md` is the NPC `noor`.
- **A place sheet** gives `[[locations]]`: its ENTERED FROM, hours, labels and dress code, and one row
  per line of its Rows table, with the gate, brake and effect exactly as the cells say. Its FILL is the
  word budget, recorded in `v2_state.json` `board.locations[].fill`.
- **A person sheet** gives `[[npcs]]` and one schedule row per filled cell of the grid. Read the
  column header for the days. Weekdays count from 0 = Monday.
- **A scene sheet** gives one canvas. "where · when" is the trigger location and schedule. The gate
  row is the trigger conditions. The sets row is the effects. The branch map is the nodes and their
  choices, and the HOOK is said in the last node.
- **The opening sheet** is a screen walk: one canvas per screen, in order, with its clock.

Done when every piece you were asked for is written.

**3 · Check.** Run `CHECK <slug>` and `SCHECK <slug>`.
Done when both print `CLEAN`. A line under "already there" in `SCHECK` is drift from before your
change: tell LO about it; it does not block you.

**4 · Report** in two lines what you built and from which sheets.

## Building the whole first release (v0.1)

Build every sheet as above, then follow `R/the-release.md` "The first release (v0.1)":
- **Version** 0.1.
- **The opening** follows `R/the-first-hour.md` F1b in order: setup, problem, person, conflict,
  choice with a reaction line, temptation, a quest card with goals, plain tutorial lines, a hook.
  `.claude/skills/author-game-v2/templates/first-hour.toml` is a menu: copy it and delete the opening shape you are not using.
- **Every person is met** before their portrait goes live (F5), where their schedule puts them
  (F5b).
- **The explicit floor** is met from the start.
- **It ends on a door.**

Then hand over through [RELEASE.md](RELEASE.md).

## Footguns

- **Never build from a [REVIEW] sheet or a proposal**, even when asked to. Probation was built from
  proposals and had to be redone.
- **Never add a place, person or scene that has no sheet.** Draft the sheet and ask. A build that
  invents rooms or merges them loses the people who live there (billable_hours made its house hub
  "The Kitchen" and its residents had no rooms; SKILL_NOTEBOOK N18).
- **Copy a gate exactly.** A paid visit whose sheet says `look` ≥ 40 opened on night one when the
  build dropped that condition (members_only, review J4).
- **A schedule grid cell is a promise.** Put every filled cell into a schedule row, and add no rows
  the grid does not have. One person in two places at once is a build bug.
- **A number on a sheet is a promise until a tool measures it** (`R/the-sheets.md` S1). Word budgets
  are measured by the gate `location fill` against `board.locations[].fill`.
