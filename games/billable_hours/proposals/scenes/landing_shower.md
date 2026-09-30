# [REVIEW] Scene — landing_shower (repeatable)

| row | answer |
|---|---|
| where · when | landing · always · repeatable |
| BRAKE (on the trigger) | `shower_today` day-cap flag, set on the choice, cleared overnight |
| bands | nerve 0–9 · 10–29 · 30 and up (`group` chain, mutually exclusive) |
| walk-in | substitution when Ethan is scheduled here and `ethan_stage` gte 1; chance 10% / 35% / 70% by band |
| clip | a cycling pool per band; `_t4` at 10–29, `_t5` at 30+ and on the walk-in |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| shower (band 0–9) | she wedges the door and washes fast, listening | no | "Towel off and go to your room." → her_room | nerve add +1 (stops at 5) · time 20 |
| shower (band 10–29) | **B3** below | **yes** | "Towel off." → her_room | nerve add +1 (stops at next rung) · time 20 |
| shower (band 30+) | **B4** below | **yes** | "Towel off." → her_room | nerve add +1 (stops at next rung) · time 20 |
| walk-in: Ethan | **B5** below | **yes** | "Keep washing." → her_room · "Shut the door on him." → her_room | nerve add +1 · sets `ethan_watched_shower` |

## Explicit beats (written by v2-prose; measured by `gates.py --beat`, re-run by the author on its own file)

**B3**

> The bathroom door won't latch, so you leave it open an inch. You stand under the hot water, naked. You soap your tits slowly and your nipples go hard under your palms. Your hand slides down to your clit. You rub small circles and listen for the landing. The stairs stay quiet, and part of you wants a creak. Your fingers keep rubbing, and your clit throbs against them.

*Measured: 69 words · 5 explicit (clit, naked, nipple, tits) · median 10 · last sentence on the body · no past claim.*

**B4**

> You leave the bathroom door wide open and turn to face it. Hot water runs down your tits. Two fingers push into your cunt, and your thumb rubs your clit hard. The landing is empty, and you want to hear a step on it. Your legs shake under the spray. You come with your eyes on the doorway, gasping, your cunt clenching tight around your fingers.

*Measured: 66 words · 4 explicit (clit, cunt, tits) · median 13 · last sentence on the body · no past claim.*

**B5**

> The bathroom door hangs open a hand's width. Ethan is on the landing, jeans open. He strokes his cock slowly, eyes on your tits. You keep washing. You soap your tits and let the water run down them. You turn and bend for the shampoo, your ass to the gap. His hand speeds up. His breath comes hard. "Don't stop." You run both hands down your ass. He jerks his cock faster and watches your hands.

*Measured: 76 words · 6 explicit (ass, cock, tits) · median 9 · last sentence on the body · ceiling: Ethan (cock, tits, ass).*
