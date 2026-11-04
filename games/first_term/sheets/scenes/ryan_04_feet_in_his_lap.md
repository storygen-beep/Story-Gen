# [REVIEW] Scene — ryan_04_feet_in_his_lap

> Changed 2026-11-04 to match the build; waits for LO's re-sign. "Go to bed." lands in her room.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the step pays Corruption +3 on "Liar."; the no's own screen; the step row. the explicit beats as built, measured.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the no gets his reply.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: his move, he takes her foot and presses it onto his cock himself; Kayla hears something, "Who's there?", the ladder's one cut-off; gate Corruption 20 · his Want 30; Want +5. The `lap` screen is now explicit (his middle column).

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 4 (Ryan A 5) |
| where · when | his room · Sun–Thu 22:00–00:00, after two knocks |
| gate | Corruption 40 (was 20: DECISIONS 124) · his Want 30 · the boost off · pays Corruption +3, cap 79 |
| want | he opens on the second knock, every time, and leaves room on the bed |
| next step | a touch he makes: he presses her foot onto his cock while Kayla is on the phone |
| hook | "Liar." And Laura can open this door ("Laura opens the door" on his sheet reads this step) |
| what she wears here | not named; her bare feet only |
| explicit? | yes, `lap`: her foot on his cock (Curious) · the crude-word ceiling: Ryan's middle column, ass, tits, cock, wet · not cunt, fuck, cum |
| her_line_low · her_line_high | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** private sexual contact with someone she knows (Bold · Showing 40): her foot on his cock.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| her foot on his cock while Kayla is on the phone | Kayla, on the phone, hears something | Kayla hearing her | "Feet up." | he presses her foot onto his cock and holds it there | the ladder's one cut-off: Kayla's "Who's there?" | the feet-in-his-lap repeatable; Laura can walk in on them |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `knocks` | two knocks; he opens; a game on, low | no | "Feet up." → `lap` · "Just saying goodnight." → `night` (parked) | none |
| `night` | Ryan: "Yeah. Night." He doesn't shut his door until she's in her room | no | "Go to bed." → her room | none |
| `lap` | her bare feet in his lap; Kayla calls; "Yeah, babe. I'm alone." He takes her foot and presses it onto his cock, hard under his shorts, and holds it there | yes | "Keep your toes moving." → `liar` | none |
| `liar` | Kayla: "Who's there?" He lets go of her foot: "No one. The TV." It stops there: the one cut-off | no | "Liar." → the hall | Ryan's Want add +5 · corruption add +3, cap 79 · `ryan_step` set 4 |

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
| `knocks` | "Just saying goodnight." | Ryan: "Yeah. Night, @player.nickname." · "He stays in his doorway with his hand on the frame, and his eyes stay on your ass all the way out into the hall." The step waits a night, as before. |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `lap` | 129 | 4: cock ×2, thrust, balls | Ryan's middle column | on this sheet above |
