# [REVIEW] Scene — ryan_07_first_kiss

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 7 (Ryan A 8) |
| where · when | his room · Mon, Tue, Thu, Sun 18:00–22:00, after two knocks |
| gate | Corruption 40 · his Want 60 · the boost off |
| want (test 1) | since the shower he leaves his door open a hand's width |
| next step (test 2) | the first kiss, and she starts it |
| hook (test 3) | his no, "I've got a girlfriend", and what she gets instead (step 8) |
| what she wears here (test 8) | not named |
| explicit? | no: a kiss, his hands on her ass; under 3 list words |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `knocks` | two knocks; he opens; neither sits down | no | "Kiss him." → `kiss` · "Goodnight, Ryan." → the hall (parked) | none |
| `kiss` | she kisses him first; his hands go to her ass and pull her in | no | "Don't stop." → `text` | none |
| `text` | Kayla's text lights his phone; she turns it face-down | no | "Ignore it." → `his_no` | corruption add +3 · Ryan's Want add +10 |
| `his_no` | "@player.nickname — I've got a girlfriend." | no | "Then think about it." → the hall | `ryan_step` set 7 |

His no is parked: he still opens to two knocks, and the kiss waits a few nights.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, his no | the arc ideas, Ryan A 8 · SP2 (his no) |
| a kiss at Bold | SP2 §1 (LO, 2026-10-06) |
