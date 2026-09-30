# [REVIEW] Scene — hotel_bar_drink (repeatable, "Have a drink") + walk-in

| row | answer |
|---|---|
| where · when | hotel_bar · every day 17:00–23:00 · repeatable |
| BRAKE | `drink_today`; costs money 8 |
| walk-in | one canvas, two bands on nerve: 0–29 an associate from the firm (25%) · 30+ a stranger in a suit (B11, 35%) |
| clip | the bar, a cycling pool; the walk-in's top band `_t5` |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| drink | a drink alone at the bar; the firm's lights across the road | no | "Finish it and go." → downtown | costs money 8 · nerve add +1 (stops at 10) · `drink_today` set |
| walk-in (0–29) | an associate: "Drinking alone, intern?" | no | "Finish your drink." → downtown | office_talk add +1 |
| walk-in (30+) | **B11** below | **yes** | "Put the glass down and go." → downtown | nerve add +1 |

## Explicit beats (written by v2-prose; re-measured by the author on its own file)

**B11**

> He takes the stool beside you and says nothing. Under the bar his hand slides up your thigh and under your skirt. You open your knees for him. He rubs your cunt through your panties until they are soaked. "Keep drinking." You lift your glass. The bartender turns to the till, and he hooks your panties aside and pushes two fingers into you. His thumb works your clit. You swallow a moan and grind your cunt down on his hand, glass still in your fist.

*Measured: 85 words · 4 explicit (clit, cunt, moan) · median 11 · last sentence on the body · ceiling: role:a stranger in a suit (cunt, clit, tits).*
