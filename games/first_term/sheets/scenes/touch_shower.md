# [READY] Scene — touch_shower

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the explicit beats as built, measured.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Touching herself in the shared bathroom: a repeatable row (LO, 2026-10-08, question 13).

| row | answer |
|---|---|
| place · row | `home_bathroom`, the shower, door locked · "Touch yourself" |
| gate | Curious: Corruption 20 (LO, 2026-10-08) |
| who | nobody: she is alone |
| what she wears here | naked in the shower (the place backs it) · elsewhere not named |
| BRAKE | once a day, on the trigger |
| raises | corruption add +1, the first time each day, until past Curious |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `touch` | alone, she touches herself until she comes | yes | "Get dressed." → the room | corruption add +1 |

## The explicit screens, written

**`touch`** · 120 words · explicit words 8 (ass, clit, moan, naked, nipple, orgasm, tits) · median sentence 10 · stage 2

> You lock the door and step naked under the hot water. Footsteps cross the hall outside and keep going. The water runs down your tits and drips off your nipples. You soap them slowly, thumbs circling until they stand hard and ache. Your hand slides down your belly and between your legs. You are slick there, and not from the shower. Two fingers find your clit and press. The water drums on your back and your ass. You lean one hand on the tile and rub faster. Your hips jerk against your fingers. The orgasm hits hard, and you bite down on the moan. Your knees go weak, and you hold the tile while your clit throbs under your hand.

No history words on any screen: each one repeats.

## Why — the source of each key choice

| key choice | source |
|---|---|
| touching herself in the shower, from Curious | LO, 2026-10-08 (question 13) |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| one voice for stages 2–3 | LO, 2026-10-08: SP2 gives both "warming up" |
| "Footsteps cross the hall" only while someone is home and awake (by their rows); otherwise the house is quiet | sweep A6-29 |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `touch` | 120 | 8: clit ×2, naked, tits, nipples, ass, orgasm, moan | Alone: no column on SP2; crude words used: ass, clit, tits | on this sheet above |
