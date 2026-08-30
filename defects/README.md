# Open defects — author-game-v2

Defects in the **skill** (the instruction set at `.claude/skills/author-game-v2/`), not in any one
game. A game bug gets fixed in that game's TOML and logged in its `authoring_state.json` /
`v2_state.json`. A defect lands here when the answer to *"would a correct skill have prevented
this?"* is **yes** — because otherwise it ships again in the next game.

One file per defect. Each carries: what happened, the evidence with `file:line`, what it cost,
and the proposed fix. Nothing here is fixed until a dated line says so.

| # | defect | found | status |
|---|---|---|---|
| 001 | [No gate asks whether a canvas is reachable](001-no-reachability-gate.md) | 2026-08-30, `commuter` — **2nd occurrence**, `the_route` was 1st | **FIXED 2026-08-30** |
| 002 | [engine.md §30's band example fails on two of the three types](002-sidebar-band-example-wrong-type.md) | 2026-08-30, `commuter` | **FIXED 2026-08-30** |

⚠️ **Both of these files carried wrong `file:line` citations, and 002 carried a wrong diagnosis.**
Found on the fix pass, when every citation was re-read against source: five wrong in total, plus
four more stale ones in `engine.md` §30 that the defect file had not noticed. Corrections are marked
inline in each file rather than silently overwritten, because a defect file is read by the next
author and an uncorrected one hands the error forward.

**The lesson is now part of the convention:** a defect file's citations get verified on the way IN,
not only on the way out. A wrong `file:line` in a defect report is the same failure the report is
about — an assertion nobody checked.
