# [READY] Scene — tom_02_uniform_rule

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 2 (Tom B 2) |
| where · when | the café floor · Mon–Sat 14:30–22:00 |
| gate | `cafe_job` · Exhibitionism 20 · his Want 10 |
| want (test 1) | his eyes on her apron strings every shift |
| next step (test 2) | his uniform rule: tight top, top button open |
| hook (test 3) | Gary lowers his paper; her tips double. Gary is introduced |
| what she wears here (test 8) | the sexy uniform: the scene adds and equips it |
| explicit? | no: a dress rule |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `rule` | Tom hands her a tight black top: "Top button stays open." | no | "Is this the uniform, or your idea?" → `both` · "No." → the shift (parked) | none |
| `both` | "Both." | no | "Fine." → `gary` | `cafe_uniform_sexy` added and worn · `uniform_sexy` set |
| `gary` | she leans to pour; Gary in booth four lowers his paper | no | "Back to work." → the shift | Tom's Want add +10 · exhibitionism add +3 · `tom_step` set 2 |

From here her tips are $8 a shift, not $4. Her "No." is parked: tips stay low; Tom asks again next week.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 2 (heat 10-06) |
| $8 tips in the sexy uniform | LO, 2026-10-07 (SP4) |
| Gary's introduction here | LO, 2026-10-08 (the job sheet) |
