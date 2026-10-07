# [REVIEW] Scene — tom_05_half_is_mine

> A draft for LO to place. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 5 (Tom B 5) |
| where · when | the back room, after a shift · Mon–Sat 14:30–22:00 |
| gate | `cafe_job` · Corruption 40 · Exhibitionism 20 · his Want 40 |
| want (test 1) | he holds his hand out for the cash after booth four |
| next step (test 2) | she names her terms: the price will be hers |
| hook (test 3) | "Half's yours till I name the price." Her price, later |
| what she wears here (test 8) | the café uniform |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `half` | Tom: "Half's mine." | no | "Half's yours till I name the price." → `jar` · "Fine." → the shift (parked) | none |
| `jar` | "And the jar's mine to tell about." He stops smiling | no | "Goodnight, Tom." → the café | Tom's Want add +10 · Tom's Power add −10 (guess) · `tom_step` set 5 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 5 (heat 10-06) |
| Power tips to her on the jar | SP2 (Tom: knowing about the jar lowers his Power) · the size is a guess |
