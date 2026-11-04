# [REVIEW] Scene — touch_bed

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The TV mutters down the hall (Q7). The build does not read this sheet's beat.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the explicit beats as built, measured.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Touching herself in her room: a repeatable row (LO, 2026-10-08, question 13).

| row | answer |
|---|---|
| place · row | `home_ella_room`, her bed · "Touch yourself" |
| gate | Curious: Corruption 20 (LO, 2026-10-08) |
| who | nobody: she is alone |
| what she wears here | not named |
| BRAKE | once a day, on the trigger |
| raises | corruption add +1, the first time each day, until past Curious |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `touch` | alone, she touches herself until she comes | yes | "Lie still." → the room | corruption add +1 |

## The explicit screens, written

**`touch`** · 117 words · explicit words 6 (ass, clit, nipple, tits) · median sentence 13 · stage 2

> Your door is shut, but someone's TV mutters down the hall. Under the sheet, you slide a hand up and squeeze your tits. You pinch a nipple until it goes hard between your fingers, and the jolt runs straight down to your clit. So you follow it down. You're wet already, and you want to know how much more you can take. Two fingers circle your clit, slow, until your hips start to lift. Then faster. Your heels dig in, your ass comes off the mattress, chasing your hand. The walls are thin, so you bite your lip hard to keep quiet. You come with your thighs clamped on your wrist, legs shaking, fingers still pressed to your clit.

No history words on any screen: each one repeats.

## Why — the source of each key choice

| key choice | source |
|---|---|
| touching herself in her bed, from Curious | LO, 2026-10-08 (question 13) |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| one voice for stages 2–3 | LO, 2026-10-08: SP2 gives both "warming up" |
| "someone's TV mutters down the hall" only while Mark is in the living room (his rows, 22:00–02:00); in an empty house the line is the quiet | sweep A6-28 |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `touch` | 121 | 6: clit ×3, tits, nipple, ass | Alone: no column on SP2; crude words used: ass, clit, tits | on this sheet above |
