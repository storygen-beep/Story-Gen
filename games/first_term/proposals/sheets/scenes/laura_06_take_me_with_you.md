# [REVIEW] Scene — laura_06_take_me_with_you

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 6 (Laura C 6) |
| where · when | the master bedroom · Saturday 17:00–18:30, Laura dressing |
| gate | Corruption 40 · Exhibitionism 40 · her Want 50 · the boost off |
| want (test 1) | she leaves her door open while she dresses |
| next step (test 2) | she asks for something: to come out with her daughter |
| hook (test 3) | "Wear something short." Step 7 pays it |
| what she wears here (test 8) | not named |
| explicit? | no: an ask |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `zip` | "Zip me up?" @player's knuckles slide up Laura's bare back | no | "Hold still." → `lean` · "Ask Mark." → the hall (parked) | none |
| `lean` | Laura leans back into her hands, her fingers on Laura's ribs | no | → `ask` | none |
| `ask` | "Take me with you one night." — "Wear something short." | no | "Friday." → the hall | Laura's Want add +10 · `laura_step` set 6 · `laura_asked_to_come` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 6 (heat 10-06) |
| the "Ask Mark." no | guess |
