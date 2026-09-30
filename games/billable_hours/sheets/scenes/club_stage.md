# [READY] Scene — club_stage (repeatable, "Watch the stage")

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| where · when | club · Mon–Sat 21:00–23:59 · repeatable |
| BRAKE | `club_today` day-cap flag; energy add −20 on the night |
| bands | nerve 0–9 (she watches from the door) · 10+ (B6) |
| walk-in | the man at the bar, nerve gte 20: chance 35%, 70% at 40+ |
| clip | a cycling pool of stage clips `_t4`; the lap walk-in `_t5` |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| stage (0–9) | she watches from the door with a drink, cheeks hot | no | "Go home." → downtown | nerve add +1 (stops at 10) |
| stage (10+) | **B6** below | **yes** | "Finish your drink." → downtown | nerve add +1 (stops at next rung) |
| walk-in: the lap | **B7** below | **yes** | "Get up and go home." → downtown | nerve add +1 |

Note: Jade's "Next one's yours" is a promise. It's paid in v0.2 (Jade step 2, the stage). Logged as an open promise.

## Explicit beats (written by v2-prose; measured by `gates.py --beat`, re-run by the author on its own file)

**B6**

> Jade's tits are out and bouncing under the lights. She hooks the last strip of lace off her hips. She is naked. The men up front lean in. She slides down the pole and bends over, her whole ass to the front row. Then she finds you and grins. "Em! Next one's yours." God, you are wet watching her. You want to be up there. She shakes her ass at you, slow, and your thighs clamp together on the stool.

*Measured: 80 words · 4 explicit (ass, naked, tits) · median 9 · last sentence on the body · ceiling: Jade.*

**B7**

> The bass is loud enough to feel in your teeth. A man at the bar hooks your waist and pulls you down onto his lap. His cock is hard under you, pressed right against your ass through his trousers. His hands close on your tits over your blouse and squeeze. "Stay." You do not get up. You grind down on his cock in time with the song, and his fingers dig harder into your tits.

*Measured: 75 words · 5 explicit (ass, cock, tits) · median 14 · last sentence on the body · ceiling: role:the man at the bar.*
