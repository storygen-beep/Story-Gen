# [READY] Scene — jake_02_kiss_on_the_quad

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_jake` · 2 (Jake B 2) |
| where · when | the quad · Mon, Wed, Fri 10:15–11:45, with his team |
| gate | Corruption 20 · Exhibitionism 20 · the boost off |
| want (test 1) | "Wasn't planning to stop." (B 1); his number in her phone |
| next step (test 2) | a kiss in public, and he shows her off |
| hook (test 3) | "Saturday. Pick me up at the door." |
| what she wears here (test 8) | not named |
| explicit? | no: a kiss |
| crude words | Jake's early column: ass (stage 2) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `team` | Jake with his team on the grass: "Guys, this is @player." | no | "Hi." → `kiss` · "Not tonight." → the quad (parked) | none |
| `kiss` | he kisses her in front of them, his hand low: "Again. They missed it." | no | "Again." → `ask` | exhibitionism add +3 |
| `ask` | she kisses him longer: "Saturday. Pick me up at the door." | no | "Saturday." → the quad | `jake_step` set 2 · `jake_date_booked` set |
| `dawn` | cut: Ryan has no way to know yet; he meets Jake at the door (Jake B 3) | — | — | — |

"Who's Jake?" moves to the night Ryan sees Jake at the front door (Jake B 3); it plays once, and Ryan's Warmth add −5 goes with it.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Jake B 2 (heat 10-06) |
| the first date is booked here | LO, 2026-10-07 (dates on his thread) · guess: this ask books it |
| Ryan's Warmth −5 | SP2 (lowered by choosing Jake) · the size is a guess |
| fix from the false-line sweep | sweep A2-13 (2026-10-08) |
