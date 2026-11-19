# [READY] Scene — laura_03_wine_in_the_kitchen

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 3 (Laura C 3) |
| where · when | the kitchen · Mon, Tue, Thu, Fri 20:00–22:00 (not Sunday: Mark is at the table) |
| gate | Corruption 20 · Exhibitionism 20 · her Want 20 · the boost off |
| want (test 1) | she keeps a glass poured for two after the catch |
| next step (test 2) | her secret: at 19 she snuck out in her mother's dress |
| hook (test 3) | "Like you get looked at." She wants to be looked at too |
| what she wears here (test 8) | not named |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `glass` | Laura with wine, her robe open at the collar: "Sit with me." | no | "Pour me one." → `story` · "I'm tired, Mom." → the hall (parked) | none |
| `story` | at 19 she snuck out in her own mother's dress, home at dawn (no clock hour) | no | "Mom!" → `mark` | none |
| `mark` | "Mark hasn't looked at my body like that since the wedding." | no | "He should." → the hall | Laura's Want add +10 · `laura_step` set 3 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 3 (heat 10-06) |
| Laura snuck out at 19 | DIRECTION §6 (kept, LO 10-06) |
| fix from the false-line sweep | sweep A2-05, A2-40 (2026-10-08) |
