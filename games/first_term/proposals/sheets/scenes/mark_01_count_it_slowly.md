# [REVIEW] Scene — mark_01_count_it_slowly

> A draft for LO to place. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 1 (Mark A 1) |
| where · when | the kitchen table · her first Sunday, 08:00–12:00 |
| gate | `rent_starts` (set at breakfast, day 1) |
| want (test 1) | none before: step 1. His eyes go to her bare legs and stay |
| next step (test 2) | the count itself: he counts slower when she's short |
| hook (test 3) | "The thirty-five waits a week." Next time: "Not the shirt." |
| what she wears here (test 8) | her sleep shirt: only in a group on her worn state (guess) |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: he only looks |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `table` | she comes down; Mark at the table: "Count it out." | no | "Here." → `count` · "Let me get dressed first." → `dressed` (parked) | none |
| `count` | his thumb on a bill; he counts slower; she's short | no | "Can you just — count it?" → `short` | none |
| `short` | "I am counting." The short goes on the tab | no | "Fine." → the hall | Mark's Want add +10 · `mark_step` set 1 |
| `dressed` | "Suit yourself." He counts when she's back; the short waits a week | no | → the hall | the step counts; no Want |

Who notices: Ryan, in the doorway. A full count (she isn't short) plays the same scene in her version: "Count it slowly."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Mark A 1 (heat 10-06) |
| "she knows, and she's still short" | LO, 2026-10-07 (SYSTEMS, decided item 2) |
| the Power edge at 50 | guess |
