# [REVIEW] Scene — ryan_06_after_the_shower

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the pay sits on a new last screen, `after6`; the step row. the explicit beats as built, measured.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): `comes` ends on what comes next.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: gate Exhibitionism 40 · his Want 50 (Corruption 40 dropped); the ending: he stays in the doorway, pulls his cock out and jerks off while she watches, and comes as Kayla calls "Babe?"; Want +5. `look` is rewritten and `comes` is new, both by `v2-prose`; the column confirmed by LO 2026-11-01 ("Continue").

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The explicit screen is written by `v2-prose` and measured.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 6 (Ryan A 7) |
| where · when | the bathroom · Saturday 08:00–10:00, seen from his room |
| gate | Exhibitionism 40 · his Want 50 · the boost off |
| want | "...@player.nickname?" through the wall last night (step 5) |
| next step | he sees her naked, by her choice, and doesn't stop: he jerks off in the doorway while she watches |
| hook | he comes as Kayla calls "Babe?"; he can't look at Kayla at breakfast; his door stays open a hand's width (step 7) |
| what she wears here | naked: she has just showered; the towel is there and she leaves it |
| her voice | stage 3, confident |
| the crude-word ceiling | his late column for "cum" (cunt, fuck, cum) · signed today at the middle column (ass, tits, cock, wet) · confirmed by LO 2026-11-01 ("Continue") |
| her_line_low · her_line_high | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** naked by choice for someone she knows (Bold · Showing 40).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she leaves the towel, and he jerks off in the doorway while she watches | Ryan; Kayla calls "Babe?" from the hall | Kayla in the house, steps away | "Leave the towel." | he stays in the doorway and pulls his cock out | yes: he comes | his door open a hand's width; step 7; his bed and room repeatables |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `door` | she steps out of the shower; the door swings open: Ryan | no | "Leave the towel." → `look` · "Reach for the towel." → parked | none |
| `look` | she stays naked and leaves the towel; he stays in the doorway, pulls his cock out and strokes it while she watches | yes | "Watch him." → `comes` | exhibitionism add +3 · corruption add +1 (shown by choice, `meters.md` rule 3) |
| `comes` | he comes, and Kayla calls "Babe?" from the hall as he does; he can't answer her | yes | "Take your time drying off." → `after6` | none |
| `after6` | his door is open a hand's width when she comes out | no | "Go to your room." → the hall | Ryan's Want add +5 · `ryan_step` set 6 · `kayla_met` set |

"Reach for the towel." is the parked no: he backs out, red; the step waits a week.

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: Ryan's name for her is `@player.nickname`, not "Ella". One truth fix after: "I heard you last night" became "I heard you through the wall" (step 6 can fire any Saturday after step 5; `ryan_heard_her` backs it).

**`look`** · 145 words · explicit words 8 · median sentence 9 · act rungs: strip, hands · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> You step out of the shower and the door swings open. Ryan, in his shorts, hair flat from sleep. The towel hangs on the rail. You leave it there and stay naked. His eyes drop straight to your tits, then down to your cunt. This time he stays. "I heard you through the wall, @player.nickname." He leans in the doorway and pulls his cock out of his shorts. It's already hard, thick and dark at the head. He wraps his fist around it and jerks it, slow. *Kayla is in this house. Let him look anyway.* You stand there dripping and let him see all of it. Water runs down your tits and off your hard nipples. Your cunt is wet, and not from the shower. He strokes faster, eyes on it. His fist slides up and down his cock, and you watch every stroke.

*The last sentence:* his fist on his cock, her watching every stroke. On the body; he hasn't come.

**`comes`** · 108 words · explicit words 8 · median sentence 9 · act rungs: strip, hands, finish · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> His fist speeds up on his cock. You stand there naked, still wet from the shower, hands at your sides. His eyes go from your tits to your cunt. His breathing turns ragged. His hips jerk. He comes in thick ropes, spurting over his knuckles onto the tiles. "Babe?" Kayla calls from the hall. He can't answer her. His mouth opens on a choked breath. His cock pulses in his hand, again and again. *She's right there.* Cum drips off his fingers onto the floor between you. You stay exactly where you are, nipples hard, and watch the last of it leak from the head of his cock.

*The last sentence:* her nipples hard, the last of it leaking from his cock. On the body; not a pivot.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 7 (heat 10-06) |
| naked for someone she knows at Bold | SP2 §1 |
| no touching on this screen | SP2: showing at stage 3; his hands wait for step 7 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the parked towel no | guess |
| Kayla in the house on Saturday morning | LIVES (she stays Friday night) · LO, 2026-10-08 (question 70): she leaves Saturday by 10:00, so the step is true any Saturday 08:00–10:00 · sweep A2-10 |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| node | the closing line (mine, signed) | what it points at |
|---|---|---|
| `comes` | "When you come out, his door is open a hand's width." | false lines a3 #6 (DECISIONS 129): "It stays that way." cut; no screen shows his door open after this one |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `look` | 159 | 9: tits ×2, cunt ×2, cock ×2, naked, nipples, fuck | Ryan's late column; also nipples | on this sheet above |
| `comes` | 108 | 8: cock ×3, naked, tits, cunt, cum, nipples | Ryan's late column; also nipples | on this sheet above |
