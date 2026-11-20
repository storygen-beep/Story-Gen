# [READY] Place — Corner Shop

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `corner_shop`.
> In 0.1 for the grocery run only: plain, no heat (LO, 2026-10-08, question 50). Its heat stays empty in stages 1–3 (LO, 2026-10-07). Rows come in batch 3.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | street (next to home: no walk time) |
| labels — what kind of place | `zone:street`, `public` |
| hours | every day 07:00–22:00 |
| closed text | "The shutter's down." |
| hidden until | no |
| fill — word budget (S3) | 1,000 words |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | the clerk (no row, nameless) | buy Laura's list | the street |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| buy Laura's list | work | home_life | 15 min · money add −20 (Laura's cash) · `groceries_bought` set true | only while `grocery_list` is set | yes, one line: the clerk, the bags |

## Why — the source of each key choice

| key choice | source |
|---|---|
| in 0.1 for the grocery run only, 07:00–22:00, 1,000 words | LO, 2026-10-08 (question 50) |
| no heat in stages 1–3 | LO, 2026-10-07 (SP7) |
| the grocery run for Laura | LO, 2026-10-08 (pick 15) · round 11, groceries 3/12 (Cupid's Way: "I'll give you 40 bucks") · the $20 guess |
