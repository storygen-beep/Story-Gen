# [REVIEW] Scene — hale_05_seven_twenty

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 5 (Hale B 5) · his last step in 0.1 |
| where · when | the lecture hall, after class · Mon, Wed, Fri 08:30–10:00 |
| gate | Corruption 40 · the boost off |
| want (test 1) | since Claire's knock he can't start the lecture on time |
| next step (test 2) | she sets his hour, and he takes it |
| hook (test 3) | "You'll be done by seven-twenty." Thursdays are hers |
| what she wears here (test 8) | not named |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `stay` | she stays behind; his no: "This has to stop." | no | "What do you want?" → `hour` · "See you in class." → campus (parked) | none |
| `hour` | "Thursdays at seven. You'll be done by seven-twenty." | no | "Seven." → campus | Hale's step counter set 5 · `hale_hour_set` set |
| `midterm` | if the midterm is back: a B+; Laura: "See what she does when she tries." | no | — | reads the midterm flag; colour only |

## The repeat it turns into — Thursdays at seven (one sheet row)

| row | answer |
|---|---|
| where · when | his office, Thursday 18:30–19:20 |
| what happens | her hour: his hands on her, the photo face-down, Claire due at 7:30 |
| explicit? | at Bold: his hands above her waist, as in B 4 · step 6 later |
| BRAKE (S9) | once a week, Thursday, on the trigger |
| his thread | "Thursday. Seven." every Wednesday evening |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 5 (heat 10-06) |
| the midterm colours, never blocks | DIRECTION §5 · SYSTEMS §1 |
| Claire's 7:30 as a rule of the world | DIRECTION §6 · SP1 (the clock's exemptions) |
