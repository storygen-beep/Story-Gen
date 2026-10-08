# [READY] Scene — ryan_08_two_knocks

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The door this release ends on.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 8 (Ryan A 9) · the release's door |
| where · when | his room · Mon, Tue, Thu, Sun 18:00–22:00, after the kiss |
| gate | Corruption 40 · his Want 70 · the boost off |
| want (test 1) | his phone face-down every time she knocks now |
| next step (test 2) | she sets the terms: what they are, and Kayla's place in it |
| hook (test 3) | "Two knocks. Any night that isn't Friday." Step 9 shows locked |
| what she wears here (test 8) | not named |
| explicit? | no: a talk step |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `ask` | after the kiss: "Kayla gets Fridays. What do I get?" | no | → `terms` | none |
| `terms` | Ryan: "Two knocks. Any night that isn't Friday." · if Jake: "And Jake?" | no | three answers, the final no → below | none |
| `keep` | "Keep Kayla. I like being the secret." | no | "Two knocks." → the hall | `ryan_terms_keep_kayla` set · `ryan_step` set 8 |
| `end` | "End it with her." | no | "Two knocks." → the hall | `ryan_terms_end_kayla` set · `ryan_step` set 8 |
| `mom` | "Mom finds out when I want." | no | "Two knocks." → the hall | `ryan_terms_mine` set · `ryan_step` set 8 |
| `final` | "Your secret's safe. You're my brother, that's all. (ends his path)" | no | → the hall | `ryan_08_two_knocks_closed` set |

**The door:** the choice "Two knocks" stays on his room's door after this step. Step 9's button shows
locked: *"Needs Hungry."*

## The repeat it turns into — `ryan_two_knocks` (one sheet row, not its own step)

| row | answer |
|---|---|
| where · when | his room, 22:00–00:00, any night but Friday |
| what happens | two knocks, he opens; they kiss on his bed, his hands on her |
| by her stage | Bold: kissing, his hands over her clothes · Hungry: locked, named on the button |
| explicit? | no in 0.1: his sex step is later (Ryan A 10) |
| effects | corruption add +1, the first time each night, until she is past Bold |
| BRAKE (S9) | once a night, on the trigger |
| his thread | after step 8: "two knocks?" every 2 days, 22:00–00:00, not Friday |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the talk and her three answers | the arc ideas, Ryan A 9 (fixed 10-06) |
| the door canvas and choice | LO, 2026-10-07 (SP7) |
| the repeat stays a kiss in 0.1 | LO, 2026-10-08 (question 29) |
| the term flag names, `ryan_two_knocks` | guess |
