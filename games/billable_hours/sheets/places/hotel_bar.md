# [READY] Place — the hotel bar

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | downtown |
| labels | zone:downtown · public · opens_at |
| hours | every day 17:00–23:00; shut: "The bar opens at five." |
| hidden until | no |
| fill — word budget | 2,500 |
| door | no |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| theo_01_the_hour (one time) | Theo · Tue–Thu 18:00–21:00 | Have a drink | downtown |

## Rows

| row | kind | system | cost and effect, with op | BRAKE | lands on a screen? |
|---|---|---|---|---|---|
| Have a drink ($8, 30m) | need | money · nerve | costs money 8; nerve add +1, stops at 10 | `drink_today` | yes: short beat |
| Theo | person | money · outfit | after step 1: his hub | — | yes: his hub |
| the walk-in: an associate / a stranger | person | office talk · nerve | substitution on Have a drink: 0–29 associate 25%; 30+ stranger 35% (B11, explicit) | chance | yes |

WALK-IN: she drinks alone here at hours Theo isn't scheduled, so the walk-in gate counts this room. The associate's walk-in covers it.
