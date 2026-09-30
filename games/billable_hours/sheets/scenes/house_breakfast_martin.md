# [READY] Scene — house_breakfast_martin (repeatable hub)

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| where · when | house · Mon–Fri 07:00–08:30 · repeatable, portrait (Martin) |
| BRAKE | `breakfast_today` |
| raises | martin_want add +1, stops at his next step's threshold (5, 10, 15) |
| lines | banded on martin_stage: 0 "Friday, Emma." · 1 "Your chair's free." · 2 "The jacket, Emma." Outfit: worn_corruption gte 2 swaps one line |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| table | he pours her coffee; his line by stage; Diane's line if office_talk gte 3 | no | "Drink it and go." → house | martin_want add +1 · `breakfast_today` set |
