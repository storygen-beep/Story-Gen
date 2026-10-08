# [READY] Scene — ryan_01_hall_first_morning

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The opening's capstone: the screen walk is on OPENING.md, rows 5–9.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 1 (Ryan A 1) |
| where · when | the hall, then the kitchen · the opening, Monday 07:15 |
| want (test 1) | her: he looks, and doesn't move from the wall |
| next step (test 2) | step 1, and it says so: the first look |
| hook (test 3) | Laura's rule puts him behind the bathroom door every morning |
| what she wears here (test 8) | a towel: the boot's shower node equips it (guess) |
| her stage here | Good Girl only: she starts at 0 |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `hall` | she steps out in the towel; Ryan on the wall: "Look at you." | no | four choices → the reaction nodes | none |
| `run` | she runs to her room, face hot; his eyes follow | no | "Get dressed." → `breakfast` | Ryan's Want add +10 · `ryan_hall_seen` set |
| `knock` | "Knock next time." · "Yeah. Sorry." | no | "Get dressed." → `breakfast` | `ryan_hall_knock` set · his next step waits 3 days |
| `talk` | she stops in the doorway; he asks about her first day | no | "Get dressed." → `breakfast` | Ryan's Warmth add +5 (guess) · `ryan_hall_talked` set |
| `final` | "Don't ever look at me like that. (ends his path)" | no | "Get dressed." → `breakfast` | `ryan_01_hall_first_morning_closed` set |
| `breakfast` | Laura, coffee; Mark at the counter with his keys | no | three start choices → `rule` | `rent_starts` set · one of `college_for_*` set |
| `rule` | Laura: "Ryan, you shower first from now on." | no | "Grab your bag." → `card` | `laura_rule_ryan_first` set |
| `card` | the opening card and the plain lines | no | "Keep hygiene on" / "Turn hygiene off" → the kitchen, 07:50 | `opening_done` set · `hygiene_off` set or not · `ryan_step` set 1 |

Laura calls up the stairs on every branch: *"@player, you'll be late on your first day!"* That is who notices.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, its lines and its four answers | IDEA §4 (LO picked it 2026-10-02) · SP2 |
| it carries breakfast and the card | the ledger's step 1 · OPENING.md (LO, 2026-10-08) |
| the towel is equipped in the boot | guess |
| Warmth +5 for talking | guess |
