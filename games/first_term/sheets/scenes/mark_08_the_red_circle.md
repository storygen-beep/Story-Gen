# [READY] Scene — mark_08_the_red_circle

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 8 (Mark A 8) |
| where · when | the kitchen, the fridge calendar · Sunday 12:00–18:00 |
| gate | Corruption 40 · his Want 70 |
| want (test 1) | he counts the twenties twice now |
| next step (test 2) | she picks the hour: Laura's late Wednesday |
| hook (test 3) | "You'll see." Step 9 pays it |
| what she wears here (test 8) | not named |
| explicit? | no: info |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `calendar` | she circles Laura's late Wednesday in red | no | → `see` · "Never mind." → the kitchen (parked) | none |
| `see` | Mark at the table: "What's that for?" — "You'll see." | no | "Wednesday." → the hall | Mark's Want add +10 · `mark_step` set 8 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene | the arc ideas, Mark A 8 (fixed 10-06: Wednesday) |
