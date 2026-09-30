# [REVIEW] Person — Martin

| row | answer |
|---|---|
| age | 52 |
| what she wants from him | to find out if his patience is restraint or waiting |
| what he visibly wants, each visit | her, grateful and on time; his eyes stay a beat too long |
| what he keeps | want + power (`martin_want`, `martin_power`, 0–100) |
| where he sleeps | house |
| what he calls her | Emma |
| role (under his name) | stepfather · partner |

## Schedule grid

| place | days | from | to | why he is there |
|---|---|---|---|---|
| house | Mon–Fri | 07:00 | 08:30 | breakfast; Fridays, the rent page |
| firm | Mon–Fri | 09:00 | 17:00 | partner |
| house | Mon–Fri | 18:00 | 19:00 | dinner |
| study | Mon–Fri | 19:00 | 23:00 | work, whisky, the door shut |
| house | Sat, Sun | 09:00 | 22:00 | home |

## Ladder

| n | canvas | where | when | gate | raises | the no | the leak (before) | the promise (after) | guidance card line |
|---|---|---|---|---|---|---|---|---|---|
| 1 | martin_01_first_friday | study | Fri 19–22 | — | martin_want +5 | parked; final "(ends his path)" | "Friday, Emma." at breakfast | "Callahan will ask me about you." | Friday after dinner: Martin's study. |
| 2 | martin_02_nobody_knocks | study | Fri 19–22 | martin_friday_sat | martin_want +5 | parked | "Your chair's free." | "Leave the jacket downstairs." | Friday after dinner: nobody knocks now. |
| 3 | martin_03_jacket_downstairs | study | Fri 19–22 | martin_want gte 15 | — | — | the jacket line | v0.2 | locked: "Leave the jacket downstairs." |

Breakfast hub raises martin_want +1 a day (`breakfast_today`), stopping at his next step.
