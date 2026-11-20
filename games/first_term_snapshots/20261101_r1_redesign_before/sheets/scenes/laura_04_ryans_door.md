# [READY] Scene — laura_04_ryans_door

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 4 (Laura C 4) |
| where · when | Ryan's room, then her room · Mon, Tue, Thu, Sun 20:00–22:00 |
| gate | Corruption 20 · Exhibitionism 20 · her Want 30 · Ryan's step 4 |
| want (test 1) | she asks about Ryan, lightly, at breakfast |
| next step (test 2) | the second catch: with Ryan, and she keeps the secret |
| hook (test 3) | "Mark doesn't need to hear about this." A secret between them |
| what she wears here (test 8) | not named; her bare feet |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `door` | Laura opens Ryan's door: her bare feet in his lap, his hand on her calf | no | "Mom—" → `room` | none |
| `room` | in her room Laura sits close, her knee against hers | no | "Don't tell Mark." → `secret` · "It's nothing. (she'll know)" → `lie` | none |
| `secret` | "Mark doesn't need to hear about this." | no | "Goodnight, Mom." → her room | Laura's Want add +10 · `laura_step` set 4 |
| `lie` | "Don't." Laura leaves without the secret | no | → her room | Warmth add −5 · `laura_suspicion` add +5 · parked |

Who notices: Laura, seeing her with Ryan. Ryan's line next time reads it.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 4 (fixed 10-06) |
| it waits for Ryan's step 4 | SP3 (LO, 2026-10-07) |
| a lie parks the step | guess |
| fix from the false-line sweep | sweep A2-39: Mark is named on the button, so "him" has someone to point at (2026-10-08) |
