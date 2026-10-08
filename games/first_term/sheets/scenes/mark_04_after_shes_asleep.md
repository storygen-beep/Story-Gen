# [READY] Scene — mark_04_after_shes_asleep

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 4 (Mark A 4) |
| where · when | the living room · Sun–Fri 22:00–00:00, Laura asleep |
| gate | Corruption 40 · Exhibitionism 20 · his Want 30 |
| want (test 1) | he stays up after Laura sleeps, the TV low |
| next step (test 2) | the ask: a price is named for the first time |
| hook (test 3) | "What's the difference worth?" Step 5 answers |
| what she wears here (test 8) | not named |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: an ask |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `m` | M: "Come down after your mother's asleep." | no | "What for?" → `price` · "I'll pay it Sunday like everyone else." → parked | none |
| `e` | E: she sits on the arm of the couch: "What's the difference worth, Mark?" | no | → `price` | none |
| `price` | he looks at the ceiling, then at her legs; he doesn't answer yet | no | "Think about it." → the hall | Mark's Want add +10 · `mark_step` set 4 |

This is the introduction of his paid route (her climb): the price is raised before the first time.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, both versions | the arc ideas, Mark A 4 (fixed 10-06: at Bold) |
| the ask as the introduction | `the-arc.md` A15 |
