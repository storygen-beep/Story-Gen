# [CUT] Scene — hale_05_seven_twenty

> **CUT 2026-11-01** (DECISIONS 113): Her power over him goes against "Hale the jerk" (`npc_hale.md`). Kept on disk as the record; not built in release 1.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 5 (Hale B 5) · his last step in 0.1 |
| where · when | the lecture hall, after class · Mon, Wed, Fri 08:30–10:00 |
| gate | Corruption 40 · the boost off |
| want | since Claire's knock he can't start the lecture on time |
| next step | she sets his hour, and he takes it |
| hook | "You'll be done by seven-twenty." Thursdays are hers |
| what she wears here | not named |
| explicit? | no: a talk |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
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
| BRAKE | once a week, Thursday, on the trigger |
| his thread | "Thursday. Seven." every Wednesday evening |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 5 (heat 10-06) |
| the midterm colours, never blocks | DIRECTION §5 · SYSTEMS §1 |
| Claire's 7:30 as a rule of the world | DIRECTION §6 · SP1 (the clock's exemptions) |
