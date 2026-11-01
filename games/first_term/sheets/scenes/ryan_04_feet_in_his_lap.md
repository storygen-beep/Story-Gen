# [READY] Scene — ryan_04_feet_in_his_lap

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the no gets his reply.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: his move, he takes her foot and presses it onto his cock himself; Kayla hears something, "Who's there?", the ladder's one cut-off; gate Corruption 20 · his Want 30; Want +5. The `lap` screen is now explicit (his middle column).

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 4 (Ryan A 5) |
| where · when | his room · Sun–Thu 22:00–00:00, after two knocks |
| gate | Corruption 20 · his Want 30 · the boost off |
| want (test 1) | he opens on the second knock, every time, and leaves room on the bed |
| next step (test 2) | a touch he makes: he presses her foot onto his cock while Kayla is on the phone |
| hook (test 3) | "Liar." And Laura can open this door ("Laura opens the door" on his sheet reads this step) |
| what she wears here (test 8) | not named; her bare feet only |
| explicit? | yes, `lap`: her foot on his cock (Curious) · the crude-word ceiling: Ryan's middle column, ass, tits, cock, wet · not cunt, fuck, cum |
| her_line_low · her_line_high (rule 7) | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `knocks` | two knocks; he opens; a game on, low | no | "Feet up." → `lap` · "Just saying goodnight." → the hall (parked) | none |
| `lap` | her bare feet in his lap; Kayla calls; "Yeah, babe. I'm alone." He takes her foot and presses it onto his cock, hard under his shorts, and holds it there | yes | "Keep your toes moving." → `liar` | none |
| `liar` | Kayla: "Who's there?" He lets go of her foot: "No one. The TV." It stops there: the one cut-off | no | "Liar." → the hall | Ryan's Want add +5 · `ryan_step` set 4 |

Who notices: Kayla, on the phone, hearing something and asking. The screen `lap` is written by `v2-prose` at his middle column and measured before the build.

## The explicit screen, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: Ryan's name for her is `@player.nickname`, not "Ella". The tool lists `vaginal` where his spoken "fuck" or a "thrust" matches its regex; no vaginal act is on these screens (a known false reading of `gates.py`'s rung check).

**`lap`** · 129 words · explicit words 4 · median sentence 7 · act rungs: vaginal · Ryan's middle column: ass, tits, cock, wet · not cunt, fuck, cum

> The game murmurs low on the TV. Your bare feet rest in Ryan's lap. His phone buzzes on the sheet, and he answers it. "Yeah, babe. I'm alone." He doesn't look at you. His free hand closes around your ankle. He drags your foot up his thigh and presses your sole flat onto his cock. He's hard under his shorts, thick and hot, pinned under your arch. *This is Ryan. You should go.* You don't go. Your toes curl and keep moving along the length of him. His hips thrust up once, slow, into your foot. Kayla's voice buzzes small from the phone. "Mm-hm," he tells her. His grip tightens on your ankle. He grinds your heel down against his balls and holds your sole hard on his cock.

*The last sentence:* his hand grinding her heel down and holding her sole on his cock, Kayla still on the line. On the body; it stops before "Who's there?".

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 5 (heat 10-06) |
| a non-sexual touch at stage 2 | LO, 2026-10-04 (the two rules for fixes) |
| Laura C 4 waits for this step | SP3 (LO, 2026-10-07) |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| node | the no | the reply (mine, signed by LO 2026-11-01) |
|---|---|---|
| `knocks` | "Just saying goodnight." | Ryan: "Yeah. Night, @player.nickname." · "He doesn't shut his door until you're in your room." The step waits a night, as before. |
