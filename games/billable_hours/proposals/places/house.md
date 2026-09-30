# [REVIEW] Place — the house (the kitchen) · ANCHOR

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | linden_street |
| labels | zone:suburb · private |
| hours | always |
| hidden until | no |
| fill — word budget | 7,500 |
| door | no (a shared room) |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Friday: the rent page (the engine's) | Martin, Diane, Ethan · Mon–Fri 07:00–08:30; Martin, Diane 18:00–19:00; weekends | Eat something | her room · the landing · the study (Fri 19–22) · Linden Street |

## Rows

| row | kind | system | cost and effect, with op | BRAKE | lands on a screen? |
|---|---|---|---|---|---|
| Eat something (15m) | need | energy | energy add +10 | once a meal window | yes: a short beat |
| the walk-in: Ethan (late) | person | outfit · who is home | substitution on Eat, 21:00–23:30, chance 20% / 40% by nerve band | chance | yes: he leans on the counter; reads worn_exposure (sleep shirt) |
| Martin (breakfast) | person | who is home · outfit | martin_want add +1, stops at his next step | `breakfast_today` | yes: his hub |
| Your mother | person | office talk | reads office_talk | — | yes: her hub |
| Ethan (breakfast) | person | office talk | sets ethan memory flags only | — | yes: his hub |
| Dinner (Mon–Fri 18:00) | person | office talk · who is home | reads office_talk, martin_friday_sat | once a day | yes: the table, everyone |

WALK-IN: Eat runs at hours when nobody is scheduled here and the family is scheduled at others, so the walk-in gate counts this room. Ethan's late walk-in covers it.

Friday: the engine's rent page is Martin at the table. No authored scene takes the money.
