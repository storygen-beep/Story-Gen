# [CUT] Scene — mark_08_the_red_circle

> **CUT 2026-11-01** (DECISIONS 113): Mark's paid route is cut: no sex and no money for her body (`npc_mark.md`). Kept on disk as the record; not built in release 1.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 8 (Mark A 8) |
| where · when | the kitchen, the fridge calendar · Sunday 12:00–18:00 |
| gate | Corruption 40 · his Want 70 |
| want | he counts the twenties twice now |
| next step | she picks the hour: Laura's late Wednesday |
| hook | "You'll see." Step 9 pays it |
| what she wears here | not named |
| explicit? | no: info |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `calendar` | she circles Laura's late Wednesday in red | no | → `see` · "Never mind." → the kitchen (parked) | none |
| `see` | Mark at the table: "What's that for?" — "You'll see." | no | "Wednesday." → the hall | Mark's Want add +10 · `mark_step` set 8 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene | the arc ideas, Mark A 8 (fixed 10-06: Wednesday) |
