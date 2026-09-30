# [REVIEW] System — outfit

| row | answer |
|---|---|
| kind | sourced: set in one place, read everywhere |
| the keys it keeps | how the outfit reads (`worn_corruption`) · how much shows (`worn_exposure`, 0 covered · 1 underwear · 2 bare) |
| fed at | her_room (the wardrobe) |
| room labels it attaches to | has_wardrobe |
| what reads it | the firm's dress code, and what the men say about her clothes |

## Where it surfaces

| room | row label | reads (op, value) | what the player sees |
|---|---|---|---|
| firm | the dress code at the door | top, bottom, shoes required | turned away: "Callahan Reed dress code. Go home and change." |
| house | Breakfast with Martin | worn_corruption gte 2 | his eyes stay longer; his line changes |
| hotel_bar | Theo's hour | worn_corruption gte 2 | "You dressed for me. That costs extra." |
| landing | Ethan's door | worn_exposure gte 1 | his door opens an inch |

v0.1 wardrobe: the interview suit (corruption 0, starting), a tight office skirt and blouse (corruption 2, starting), a sleep shirt (exposure 1). No shop in v0.1.
