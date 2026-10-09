# [READY] Place — Garage

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_garage`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | home_hall |
| labels — what kind of place | `zone:home`, `private` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget (S3) | 2,000 words (was 1,500): +500 for laundry |
| door | no: Mark's workshop, not a bedroom |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Mark: Mon, Tue, Thu, Fri 19:00–22:00 · Saturday 09:00–17:00 | go through Mark's things while he's out | the hall |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| Mark | person | Mark's ladder | Mark A 6 here · his Power read (colour) | once per window, on the trigger | yes |
| his things | work | money and rent | the debt papers: reads `rent_carried` · the loan with Vance is named only after `knows_mark_debt` (Mark A 2) | once a day, when he's out | yes |

## Everyday at home (system `home_life`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| laundry, the washer | work | home_life | 30 min · energy add −5 · alone plain · with Mark here (Mon, Tue, Thu, Fri 19:00–22:00 · Sat 09:00–17:00): his Want +1, inside his hub | `did_laundry`, 12 h | yes |

## Rows a gate needs

| row | gate |
|---|---|
| his things while he's out | a destination is never open and exit-only |

## Why — the source of each key choice

| key choice | source |
|---|---|
| Mark's evenings in the garage | LIVES §2 |
| his things while he's out | LIVES §4 |
| the debt papers | guess |
| the everyday rows | LO, 2026-10-08 (the everyday picks) · system `home_life` · times and numbers guess |
| the dinner hour, 18:00–19:00 | LO, 2026-10-08 (question 54) |
| fix from the false-line sweep | sweep A1-13 (2026-10-08) |
