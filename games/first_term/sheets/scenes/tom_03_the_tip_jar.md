# [READY] Scene — tom_03_the_tip_jar

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 3 (Tom B 3) |
| where · when | the back room · Mon–Sat 14:30–22:00 |
| gate | `cafe_job` · Exhibitionism 20 · his Want 20 |
| want (test 1) | he counts the jar when she's near |
| next step (test 2) | she catches him stealing: leverage |
| hook (test 3) | "Not a word." She holds his secret for step 5 |
| what she wears here (test 8) | the café uniform |
| explicit? | no: info |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `jar` | she sees Tom fold twenties from the tip jar into his apron | no | "Busy night?" → `seen` · walk past → the shift (parked) | none |
| `seen` | he sees her see it: "Not a word." | no | "Not a word." → the shift | Tom's Want add +10 · `tom_step` set 3 · `knows_tip_jar` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 3 · DIRECTION §6 (the tip jar, kept) |
