# [READY] Scene — ryan_06_after_the_shower

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The explicit screen is written by `v2-prose` and measured.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 6 (Ryan A 7) |
| where · when | the bathroom · Saturday 08:00–10:00, seen from his room |
| gate | Corruption 40 · Exhibitionism 40 · his Want 50 · the boost off |
| want (test 1) | "...@player.nickname?" through the wall last night (step 5) |
| next step (test 2) | he sees her naked, by her choice, the door locked |
| hook (test 3) | Kayla calls "Ryan?"; he leaves wanting more (the kiss, step 7) |
| what she wears here (test 8) | naked: she has just showered; the towel is there and she leaves it |
| her voice | stage 3, confident |
| the crude-word ceiling | Ryan's middle column: ass, tits, cock, wet · not cunt, fuck, cum |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `door` | she steps out of the shower; the door swings open: Ryan | no | "Leave the towel." → `look` · "Reach for the towel." → parked | none |
| `look` | she stays naked, locks the door, lets him look | yes (6 words) | "Let him look." → `kayla` | exhibitionism add +3 · Ryan's Want add +10 |
| `kayla` | Kayla from the hall: "Ryan?" He unlocks the door and goes, hard | no | "Take your time drying off." → the hall | `ryan_step` set 6 |

"Reach for the towel." is the parked no: he backs out, red; the step waits a week.

## The explicit screen, written

**`look`** · 147 words · explicit words 6 (ass, cock, naked, nipple, tits) · median sentence 12 · act rungs: strip, hands · Ryan's middle column (SP2 crude table): ass, tits, cock, wet · not cunt, fuck, cum, pussy

> You step out of the shower just as the door swings open. Ryan, in nothing but his shorts. Water runs down your tits and drips off your nipples, hard in the cold air. The towel hangs right there on the rail. You stay naked and leave it. His cock is already hard, straining the front of his shorts, and he can't stop looking. "I heard you last night, @player.nickname. All of it." "Good. Now you've seen it too." You reach past him, close enough to feel the heat off his chest, and turn the lock. You turn slowly so he gets your ass, pink from the hot water. A line of water slides down your spine and between your cheeks. Behind you his breathing goes rough. You look back over your shoulder. His hands are fists at his sides, but his cock jerks against the thin cotton.

*The last sentence:* his fists, his cock against the cotton. On the body; not a pivot.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 7 (heat 10-06) |
| naked for someone she knows at Bold | SP2 §1 |
| no touching on this screen | SP2: showing at stage 3; his hands wait for step 7 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the parked towel no | guess |
| Kayla in the house on Saturday morning | LIVES (she stays Friday night) · LO, 2026-10-08 (question 70): she leaves Saturday by 10:00, so the step is true any Saturday 08:00–10:00 · sweep A2-10 |
