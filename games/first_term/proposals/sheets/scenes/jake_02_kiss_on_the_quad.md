# [REVIEW] Scene — jake_02_kiss_on_the_quad

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_jake` · 2 (Jake B 2) |
| where · when | the quad · Mon, Wed, Fri 10:15–11:45, with his team |
| gate | Corruption 20 · Exhibitionism 20 · the boost off |
| want (test 1) | "Wasn't planning to stop." (B 1); his number in her phone |
| next step (test 2) | a kiss in public, and he shows her off |
| hook (test 3) | "Saturday. Pick me up at the door." Ryan: "Who's Jake?" |
| what she wears here (test 8) | not named |
| explicit? | no: a kiss |
| crude words | Jake's early column: ass (stage 2) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `team` | Jake with his team on the grass: "Guys, this is @player." | no | "Hi." → `kiss` · "Not tonight." → the quad (parked) | none |
| `kiss` | he kisses her in front of them, his hand low: "Again. They missed it." | no | "Again." → `ask` | exhibitionism add +3 |
| `ask` | she kisses him longer: "Saturday. Pick me up at the door." | no | "Saturday." → the quad | `jake_step` set 2 · `jake_date_booked` set |
| `dawn` | next morning, Ryan at the bathroom door: "Who's Jake?" | no | — | Ryan's Warmth add −5 (choosing Jake, guess) |

"Who's Jake?" is Ryan's line on his next morning hub, gated on `jake_step` 2: the promise this step ends on.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Jake B 2 (heat 10-06) |
| the first date is booked here | LO, 2026-10-07 (dates on his thread) · guess: this ask books it |
| Ryan's Warmth −5 | SP2 (lowered by choosing Jake) · the size is a guess |
