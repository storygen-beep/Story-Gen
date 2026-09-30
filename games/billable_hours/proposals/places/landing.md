# [REVIEW] Place — the landing

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | house |
| labels | zone:suburb · private · has_shower · she_can_undress |
| hours | always |
| hidden until | no |
| fill — word budget | 3,500 |
| door | yes: Ethan's door. Knock (after ethan_stage 1), gated on Ethan being home |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| ethan_01_red_ink (step 1, one time) | Ethan · Mon–Thu, Sun 21:00–23:30 | Take a shower | her room · the kitchen |

## Rows

| row | kind | system | cost and effect, with op | BRAKE | lands on a screen? |
|---|---|---|---|---|---|
| Take a shower (20m) | her body | nerve · who is home | nerve add +1, stops at the next rung | `shower_today` | yes: three bands on nerve, explicit at the top two |
| the walk-in: Ethan | person | who is home | substitution when Ethan is here and ethan_stage gte 1 | chance by nerve band | yes: he watches, or walks off |
| Ethan's door | person | outfit | reads worn_exposure | — | yes: his hub |

WALK-IN: she washes alone and Ethan is scheduled here, so the walk-in is required, not optional.
