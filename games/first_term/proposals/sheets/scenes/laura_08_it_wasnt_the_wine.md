# [REVIEW] Scene — laura_08_it_wasnt_the_wine

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 8 (Laura C 8) · her last step in 0.1 |
| where · when | the kitchen · the next weekday breakfast, 06:30–08:00 |
| gate | Corruption 40 · Exhibitionism 40 · her Want 70 · the boost off |
| want (test 1) | she can't meet her eyes at breakfast |
| next step (test 2) | they name the kiss, and Laura shuts the door on it, for now |
| hook (test 3) | "I'm your mother." The door is locked, not shut: step 9 is later |
| what she wears here (test 8) | not named |
| explicit? | no: a talk |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `coffee` | Laura, not looking up: "That was the wine." | no | "It wasn't the wine." → `mother` · "It was the wine." → the hall (parked) | none |
| `mother` | "I'm your mother." Her hand shakes on the cup | no | "Okay. For now." → the hall · the final no → `final` | Laura's Want add +10 · `laura_step` set 8 |
| `final` | "You're my mom. That's all you get to be. (ends her path)" | no | → the hall | `laura_08_it_wasnt_the_wine_closed` set |

## The repeat it turns into — her catches (`laura_catch`, one sheet row)

| row | answer |
|---|---|
| where · when | the dark stairs, 23:00–02:00, when she comes home late |
| what happens | Laura waits up; her questions read her Warmth and suspicion |
| by her Want | high: "Tell me everything." Her questions get closer |
| explicit? | no in 0.1; her step 9 shows locked: "Needs Hungry" |
| BRAKE (S9) | once a night, on the trigger |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 8 (heat 10-06) |
| her final no | SP2 |
| her repeat is the catches | SP2 (After: her catches keep coming) |
| `laura_catch` as an id | guess |
