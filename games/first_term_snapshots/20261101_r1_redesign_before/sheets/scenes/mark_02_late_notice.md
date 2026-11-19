# [READY] Scene — mark_02_late_notice

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 2 (Mark A 2) |
| where · when | the kitchen drawer, late · Sun–Fri 22:00–00:00, Mark next door |
| gate | his Want 10 |
| want (test 1) | his eyes on her hem at the first count |
| next step (test 2) | she learns his weak spot: the debt to Vance |
| hook (test 3) | "Put it back." Each of them now holds something |
| what she wears here (test 8) | not named |
| explicit? | no: info |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `drawer` | under the takeout menus, Vance's late notice | no | "Read it." → `phone` · "Shut the drawer." → the kitchen (parked) | none |
| `phone` | Mark in the doorway, on the phone: "Friday, Frank. I'll have it Friday." | no | "How late are we?" → `put` | `knows_mark_debt` set |
| `put` | "Put it back." | no | "Okay." → the kitchen | Mark's Want add +10 · `mark_step` set 2 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene; Frank is Vance | the arc ideas, Mark A 2 · DIRECTION §6 |
| `knows_mark_debt` as a key | guess |
