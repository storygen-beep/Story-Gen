# [READY] System — office talk

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| kind | sourced: fed only at the firm |
| the key it keeps | `office_talk`, 0–10 |
| fed at | firm (the walk-in, the copier, staying late) |
| room labels it attaches to | public |
| what reads it | who at home has heard what |

## Where it surfaces

| room | row label | reads (op, value) | what the player sees |
|---|---|---|---|
| house | Dinner | office_talk gte 3 | Diane: "Someone said you were at the copier with Ethan till nine." |
| study | Martin, Friday | office_talk gte 3 | "Callahan's associates talk about you. I'd rather they didn't." |
| firm | Work a shift | office_talk gte 5 | two associates stop talking when she walks past |

Raises: +1 per walk-in, +1 per late night at the firm. Never falls in v0.1.
