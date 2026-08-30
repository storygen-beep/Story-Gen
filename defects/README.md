# Open defects — author-game-v2

Defects in the **skill** (the instruction set at `.claude/skills/author-game-v2/`), not in any one
game. A game bug gets fixed in that game's TOML and logged in its `authoring_state.json` /
`v2_state.json`. A defect lands here when the answer to *"would a correct skill have prevented
this?"* is **yes** — because otherwise it ships again in the next game.

One file per defect. Each carries: what happened, the evidence with `file:line`, what it cost,
and the proposed fix. Nothing here is fixed until a dated line says so.

| # | defect | found | status |
|---|---|---|---|
| 001 | [No gate asks whether a canvas is reachable](001-no-reachability-gate.md) | 2026-08-30, `commuter` — **2nd occurrence**, `the_route` was 1st | OPEN |
| 002 | [engine.md §30's band example fails on two of the three types](002-sidebar-band-example-wrong-type.md) | 2026-08-30, `commuter` | OPEN |
