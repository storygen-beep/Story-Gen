# [READY] Scene — laura_01_blue_dress

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 1 (Laura C 1) |
| where · when | the kitchen, then the master bedroom · Tuesday 18:00–22:00, day 2 |
| gate | none: step 1, day 2 |
| want (test 1) | none before it: step 1, and it says so |
| next step (test 2) | she dresses her daughter, and lingers |
| hook (test 3) | the dress is hers now; it comes home late (step 2) |
| what she wears here (test 8) | Laura's blue dress: the scene adds and equips it |
| her stage here | Good Girl: shy choices only (SP2) |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `kitchen` | Laura, washing up: "Come upstairs. I have something for you." | no | "Follow her." → `mirror` | none |
| `mirror` | the blue dress, tight across her chest; Laura smooths it over her hips | no | "Is that bad?" → `no` · "I can't take this." → `give` (parked) | `laura_blue_dress` added and worn |
| `no` | "It never fit me like that." — "No." | no | "Thank you, Mom." → her room | Laura's Want add +10 · exhibitionism add +3 · `laura_step` set 1 · `laura_01_done` set |
| `give` | "Keep it. Wear it somewhere." Laura doesn't take it back | no | "Okay." → her room | `laura_blue_dress` kept · the step counts, warmer |

Who notices: Laura, behind her in the mirror.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 1 (heat 10-06) |
| day 2, shy choices only | SP2 §6 (kept) |
| the dress is equipped by the scene | the truth rule · guess for the mechanism |
