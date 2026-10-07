# [REVIEW] Scene — tom_01_the_apron

> A draft for LO to place. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 1 (Tom B 1) |
| where · when | the café counter · Mon–Sat 14:30–22:00, her first shift |
| gate | `cafe_job` |
| want (test 1) | none before: step 1. His eyes on her ass as she carries the tray |
| next step (test 2) | he touches her, as if it's nothing: the apron |
| hook (test 3) | "Regulars tip the pretty ones." Tips, and the uniform (step 2) |
| what she wears here (test 8) | the normal café uniform (the dress rule) |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `apron` | Tom reties her apron from behind, his knuckles on her hip | no | "Then I'll be pretty." → `tray` · "I can tie my own apron." → `tray` | none |
| `tray` | "Regulars tip the pretty ones." His eyes follow her ass out | no | "Table six." → the shift | Tom's Want add +10 · `tom_step` set 1 |

Both answers count; the second gives his Power add −5 (guess): she pushed back.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 1 (heat 10-06) |
| the Power cost of pushing back | guess |
