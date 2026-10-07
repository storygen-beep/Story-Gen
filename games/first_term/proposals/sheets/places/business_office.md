# [REVIEW] Place — Business Lecturer's Office

> A draft for LO to place. Written 2026-10-08 against the system sheets. Id `business_office`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | faculty_floor |
| labels — what kind of place | `zone:campus`, `private` |
| hours | Mon, Wed, Thu, Fri 14:30–18:00 |
| closed text | "The office is locked. Office hours are on the door." |
| hidden until | no |
| fill — word budget (S3) | 500 words (ledger, unchanged) |
| door | no: an office, open in office hours |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | the Business lecturer: Mon, Wed, Thu, Fri 14:30–18:00 | read her grade, posted on the door | the faculty floor |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| the Business lecturer, the talk hub | person | college | one line on her grade, one on her clothes | once a day, on the trigger | yes |
| read your grade on the door | work | college | none · reads that subject's grade | none needed: it writes nothing | yes, one line |
| the honest retake | work | college | `grade_business` add +5 (guess) · `office_business_<term>_used` set | once per exam | yes |

## Rows a gate needs

| row | gate |
|---|---|
| the posted grade, every open hour | a destination is never open and exit-only |
| the Business lecturer's row has a hub | standing surface |

## Why — the source of each key choice

| key choice | source |
|---|---|
| every office a small talk hub first | kept (LO, 2026-10-07) (SYSTEMS §1) |
| their acts wait for 0.2 | LO, 2026-10-07 (SP5) |
| the grade posted on the door | LO, 2026-10-08 |
| the retake, once per exam | kept (LO, 2026-10-07) |
