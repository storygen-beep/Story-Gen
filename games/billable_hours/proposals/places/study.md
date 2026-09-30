# [REVIEW] Place — Martin's study

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | house |
| labels | zone:suburb · private |
| hours | Friday 19:00–22:00; shut otherwise: "Martin's study. The door is shut." |
| hidden until | no |
| fill — word budget | 3,000 |
| door | yes: Martin's. It is only open on Friday evenings |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| martin_01 · martin_02 (one time, Fridays) | Martin · Mon–Fri 19:00–23:00 | Look at the shelves while he reads (a beat inside his hub) | the kitchen |

## Rows

| row | kind | system | cost and effect, with op | BRAKE | lands on a screen? |
|---|---|---|---|---|---|
| Martin | person | nerve · office talk | martin_want add +1 per Friday visit, stops at his next step | once a week (Friday) | yes: his hub |
| Go up to the study (the door) | person | — | locked: martin_want gte 15, shown with his line | — | yes: step 3, v0.2 |
