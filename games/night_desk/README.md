# Night Desk

An experiment in **reviewing a game before it is built**. The sheets were written and signed off
first; the TOML and the build came after. The point is the review loop, not the game.

**Status: BUILT, 2026-08-31.** 39 of 40 gates green, 35/35 canvases reached the build. The one red is
`location fill` — this is 4,590 words against a seed of 116,540, and it is not fixable by editing.

⚠️ **The output of the experiment is [`iterations/001/BUILD_VS_SHEET.md`](iterations/001/BUILD_VS_SHEET.md)** — ten format gaps that
were only visible once something ran. That file is what gets promoted into the skill.

## Read in this order

| file | what it is | status |
|---|---|---|
| `iterations/001/SHORT.md` | 30 seconds. What this is and what is wrong with it | [REVIEW] |
| `iterations/001/LONG.md` | 2 minutes, plain words | [REVIEW] |
| [`DECISIONS_LONG.md`](DECISIONS_LONG.md) | the sixteen decisions, plainly | [READY] |
| [`DECISIONS.md`](DECISIONS.md) | the same, with the evidence | [READY] — Block A signed |
| [`FORMAT.md`](FORMAT.md) | how these sheets work, and why | locked |
| [`iterations/001/BUILD_VS_SHEET.md`](iterations/001/BUILD_VS_SHEET.md) | **the experiment's output** — sheet vs build, ten format gaps | [READY] |
| [`iterations/001/BUILD_LOG.md`](iterations/001/BUILD_LOG.md) | every red in the order it appeared | — |
| [`SKILL_CHANGES_OWED.md`](SKILL_CHANGES_OWED.md) | what this experiment owes `author-game-v2` | 1 of 12 applied |

## The sheets

**Living — always current, overwritten each release.**

<pre>
sheets/<a href="sheets/OPENING.md">OPENING.md</a>              the first night — 12 screens, with a screen walk,
                               a timeline and a checklist
sheets/places/                 7 — <a href="sheets/places/the_desk.md">the_desk</a> (anchor) · <a href="sheets/places/the_bathroom.md">the_bathroom</a> · <a href="sheets/places/the_corridor.md">the_corridor</a>
                               <a href="sheets/places/the_lot.md">the_lot</a> · <a href="sheets/places/the_kitchen.md">the_kitchen</a> · <a href="sheets/places/the_office.md">the_office</a> · <a href="sheets/places/room_6.md">room_6</a>
sheets/people/                 2 — <a href="sheets/people/del.md">del</a> · <a href="sheets/people/marek.md">marek</a>
sheets/scenes/                 11 — 9 rungs and 2 refusals
</pre>

**Frozen — what each release did.**

<pre>
iterations/001/                SHORT · LONG · CHANGES · <a href="iterations/001/BUILD_VS_SHEET.md">BUILD_VS_SHEET</a> · <a href="iterations/001/BUILD_LOG.md">BUILD_LOG</a>
toml_phases/                   6 phase files → 7_final_game.toml (152 KB)
output/index.html              the built game, 1141 KB
</pre>

## The workflow

<pre>
[REVIEW]  →  LO reads and edits  →  [READY]  →  built  →  [GAME-READY]
</pre>

Copied from the reference game's own Writer's Workflow: the document is argued over first, and
whoever implements it is not whoever wrote it.
