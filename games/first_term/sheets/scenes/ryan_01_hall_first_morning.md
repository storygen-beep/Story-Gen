# [REVIEW] Scene — ryan_01_hall_first_morning

> Changed 2026-11-04 to match the build; waits for LO's re-sign. `breakfast`: Mark has already left (Q10).

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The final no row is gone; the hall has three choices.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. Ryan's +10 sits on "Open the door."; the card's buttons and exit; the step row.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The opening's capstone: the screen walk is on OPENING.md, rows 5–9.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 1 (Ryan A 1) |
| where · when | the hall, then the kitchen · the opening, Monday 07:15 |
| want | her: he looks, and doesn't move from the wall |
| next step | step 1, and it says so: the first look |
| hook | Laura's rule puts him behind the bathroom door every morning |
| what she wears here | a towel: the boot's shower node equips it (guess) |
| her stage here | Good Girl only: she starts at 0 |
| explicit? | no |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** an accident at home that happens to her (Good Girl · Covered). Ryan's first; every chosen act with him comes after `ryan_hall_seen`.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Ryan sees her in the towel in the hall, and can't hide it | Ryan; Laura, calling down the hall | empty: step 1 is an accident | empty: step 1 is an accident | he waits at the bathroom door and doesn't move out of her way | not a sex act: a look | Laura's rule (Ryan showers first); his doorway tease can open; the rent starts |

Not on the map: the boot's `wake` and `problem` screens (Mark's rent, told the night before), and "Skip the opening", which sets step 1, his Want +10 and every opening flag and goes straight to the card.

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `shower` | the bathroom; Ryan rattles the handle: "Some of us have places to be." | no | "Open the door." → `hall` | Ryan's Want add +10 (the moment he sees her) |
| `hall` | she steps out in the towel; Ryan on the wall: "Look at you." He catches himself, towel low over his shorts | no | three choices → the reaction nodes | `ryan_hall_seen` set on all three |
| `run` | she runs to her room, face hot; his eyes follow | no | "Get dressed." → `breakfast` | `ryan_step` set 1 · nothing of his ("Run to your room." adds 0) |
| `knock` | "Knock next time." · "Yeah. Sorry." | no | "Get dressed." → `breakfast` | `ryan_hall_knock` set · `ryan_step` set 1 |
| `talk` | she stops in the doorway; he asks about her first day | no | "Get dressed." → `breakfast` | Ryan's Warmth add +5 · `ryan_hall_talked` set · `ryan_step` set 1 |
| `breakfast` | Laura, coffee; Mark has already gone to work, his envelope against the sugar bowl, and Laura says the rent for him (Q10) | no | three start choices → `rule` | `rent_starts` set · one of `college_for_*` set |
| `rule` | Laura: "Ryan, you shower first from now on." | no | "Grab your bag." → `card` | `laura_rule_ryan_first` set |
| `card` | the opening card and the plain lines | no | "Go to campus." · "Go to campus. (Turn hygiene off)" → the dean's office | `opening_done` set · `hygiene_off` set on the second |

Laura calls down the hall on every branch: *"@player, you'll be late on your first day!"* That is who notices.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, its lines and its answers | IDEA §4 (LO picked it 2026-10-02) · SP2 |
| it carries breakfast and the card | the ledger's step 1 · OPENING.md (LO, 2026-10-08) |
| the towel is equipped in the boot | guess |
| Want +10 on "Open the door.", 0 on her answer | LO, 2026-11-03 (DECISIONS 143) |
| Warmth +5 for talking | guess, as built |
