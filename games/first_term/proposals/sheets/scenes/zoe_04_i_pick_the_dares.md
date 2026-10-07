# [REVIEW] Scene — zoe_04_i_pick_the_dares

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 4 (Zoe A 4) · her last step in 0.1 |
| where · when | Zoe's couch · Mon–Sat 18:00–22:00, after the hot tub |
| gate | Corruption 40 · the boost off |
| want (test 1) | "Took you long enough." (A 3); she still won't ask |
| next step (test 2) | Zoe admits she dared instead of asking; @player takes the dares |
| hook (test 3) | "From now on, I pick the dares." Party nights are hers |
| what she wears here (test 8) | not named |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `couch` | Zoe: "You didn't need me in the hot tub. You were the dare." | no | → `asked` | none |
| `asked` | "I dared you so I wouldn't have to ask." | no | "From now on, I pick the dares." → `first` · "Okay." → the apartment (parked) | none |
| `first` | her first dare for Zoe; Zoe: "Not that one, babe." — then takes the next | no | "Next one, then." → the apartment | `zoe_step` set 4 · `picks_the_dares` set |

No "last night" in the lines: this step can come any evening after the hot tub (the truth rule).

## The repeat it turns into — party nights, her call (one sheet row)

| row | answer |
|---|---|
| where · when | Zoe's Friday party |
| what happens | the dare pool gains "Dare Zoe": @player sets the dares |
| explicit? | the dare screens are; `party_dare`'s sheet carries the beat |
| BRAKE (S9) | two dares a night, on the trigger |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 4 (heat 10-06) |
| "Not that one, babe." parked | SP2 (Zoe's no) |
| "Dare Zoe" in the pool | guess |
