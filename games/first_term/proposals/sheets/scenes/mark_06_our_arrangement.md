# [REVIEW] Scene — mark_06_our_arrangement

> A draft for LO to place. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 6 (Mark A 6) |
| where · when | the garage · Mon, Tue, Thu, Fri 18:00–22:00 |
| gate | Corruption 40 · his Want 50 |
| want (test 1) | he can't hold her look at dinner since the couch |
| next step (test 2) | it becomes a deal: each holds the other's secret |
| hook (test 3) | "So we each keep one." The table is hers to take |
| what she wears here (test 8) | not named |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `m` | M: "Our arrangement. Your mother has enough to worry about." | no | "Vance's letter is in the drawer." → `keep` · "There's no arrangement." → parked | none |
| `e` | E: "Vance's letter is in the drawer. So we each keep one." | no | → `keep` | none |
| `keep` | he wipes his hands on a rag and nods | no | "Deal." → the hall | Mark's Want add +10 · `mark_step` set 6 · `mark_arrangement` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, both versions | the arc ideas, Mark A 6 |
| `mark_arrangement` as a key | guess |
