# [REVIEW] Place — Hall

> A draft for LO to place. Written 2026-10-08 against the system sheets. Id `home_hall`.

| row | answer |
|---|---|
| kind | thoroughfare |
| ENTERED FROM (S2) | street |
| labels — what kind of place | `zone:home` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget (S3) | 2,000 words (ledger, unchanged) |
| door | no: the house's hub; everyone passes through |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Ryan A 1, day one only: out of the bathroom into Ryan | Laura, 23:00–02:00, only when she came home late | check what she is wearing on the stairs | kitchen, living room, front door |
| from the street, 22:00 or later: the dark house (sets `came_home_late`) |  |  |  |
| Laura's catch on the stairs (Laura C 2, then her repeat) |  |  | her room, Ryan's room, master bedroom |
| the stairs event: short skirt or no panties, someone below |  |  | bathroom, garage, the street |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| Laura, on the stairs | person | Laura's ladder | `laura_suspicion` read: how hard she asks (colour) | only when `came_home_late` is set | yes |
| the stairs event | work | wardrobe | exhibitionism add +1, the first time each day | once a day, on the trigger | yes: her body |
| check your clothes in the hall mirror | work | wardrobe | none · the line reads her state | none needed: it writes nothing | yes, one line |

## Rows a gate needs

| row | gate |
|---|---|
| entered from the street, hub of the house | the map is a place |
| Laura there only with the flag set | standing surface |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the hall is the house's hub | the board, 2026-10-08 · the map's shape |
| Laura's gated stairs row | LO, 2026-10-08 (LIVES) |
| a hall mirror | guess |
