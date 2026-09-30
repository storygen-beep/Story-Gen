# [READY] Scene — her_room_touch (repeatable, "Touch yourself")

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| where · when | her_room · always · repeatable |
| BRAKE | `touch_today` day-cap flag |
| bands | nerve 0–9 (she stops herself) · 10–29 (B8) · 30+ (B9) |
| clip | a cycling pool per band, `_t4` / `_t5` |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| bed (0–9) | a hand on her stomach; a creak on the landing; she stops | no | "Sleep." → her_room | nerve add +1 (stops at 5) |
| bed (10–29) | **B8** below | **yes** | "Roll over and sleep." → her_room | nerve add +1 (stops at next rung) |
| bed (30+) | **B9** below | **yes** | "Lie there." → her_room | nerve add +1 (stops at next rung) |

## Explicit beats (written by v2-prose; measured by `gates.py --beat`, re-run by the author on its own file)

**B8**

> You push your hand up under your sleep shirt. Your tits are hot and heavy, and your nipples go hard under your fingers. You pinch one and bite your lip. The TV mutters downstairs. You slide your hand into your panties anyway. Your clit is swollen and slick, and you rub it in small, tight circles. Your hips lift into your hand, and you bite down on a moan.

*Measured: 69 words · 4 explicit (clit, moan, nipple, tits) · median 9 · last sentence on the body · no person named.*

**B9**

> You yank the sleep shirt off and flop back, knees up. Your nipples are already hard, tits bare to the ceiling. Two fingers slide into your cunt. Your thumb finds your clit. You work your fingers fast and you don't bother being quiet. The headboard knocks the wall. Your cunt clamps on your fingers and you come loud, hips off the sheet, thumb still grinding your clit.

*Measured: 67 words · 6 explicit (clit, cunt, nipple, tits) · median 10 · last sentence on the body · no person named.*
