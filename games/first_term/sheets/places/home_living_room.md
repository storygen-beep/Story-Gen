# [READY] Place — Living Room

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go with your recs, skip the play check"; DECISIONS 131, `sheets/READER_FAILS_A3.md`, Home): row 15: the couch's "Stay a while." (Daring, her underwear, Mark or Ryan passing) opens a short screen, `stay_mark` or `stay_ryan`: ten minutes later he comes back, looks, and holds back: "Not with your mother home." / "Not with Mom home, @player.nickname." while Laura is in the house, "Your mother'll be back." / "Mom'll be back, @player.nickname." while she is out. Same pay and once-a-day brake. Mark's hub in this room (row 1): channel 5 on the remote beside him shows only after his accident (`mark_saw_her`), like "Leave it on."; the towel's top band gets "Get dressed." (rows 5-6, below). Built in `home.py` (living_couch) and `mark.py`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_living_room`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | home_hall |
| labels — what kind of place | `zone:home`, `private` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget | 6,000 words (was 5,000): +1,000 for TV and the film (question 51) |
| door | no: a shared room. Who is inside is a row, not a door |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Mark: Sun–Fri 22:00–00:00, then Mon–Sat 00:00–02:00 | lie on the couch in what she's wearing | the hall |
|  | Laura: Saturday 22:00–00:00, waiting up in the dark |  |  |
|  | Ryan: Saturday and Sunday 14:00–18:00, TV and a film |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| Mark, late | person | Mark's ladder | Mark's Want read (colour) · Mark A 4 and 5 here | once a night, on the trigger | yes |
| Laura, waiting up | person | Laura's ladder | sees the front door (the shared step) | Saturday only | yes |
| lie on the couch | work | wardrobe | exhibitionism add +1 if Daring and someone passes | once a day, on the trigger | yes: who walks through, what they see |

## Everyday at home (system `home_life`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| TV | work | home_life · energy | 60 min · energy add +5 · alone plain · with Mark (late), Laura (Sat 22:00–00:00) or Ryan (Sat, Sun 14:00–18:00): +1, inside their hub | `watched_tv`, 12 h | yes: what's on, who's on the couch |
| TV: the remote (changed 2026-10-29, DECISIONS 85–86, signed by LO 2026-10-29) | work | the way up · home_life | alone (`living_tv`) and with Mark (his hub): 5 channels, each with its own clip. News, cooking, sports, old film: 30 min, energy add +5 once a day (`watched_tv`). Channel 5, the adult channel, any hour: "Keep watching." 30 min, corruption add +1, cap 19 at Good Girl, cap 39 at Curious · alone at Curious, "Touch yourself." corruption add +2, cap 39 · with Mark, his reaction by his step | none on the adult channel: it pays every time (LO, 2026-10-29); time is the limit | yes: `scenes/living_tv_channels.md` |
| a film (movie night) | person | home_life | 120 min · energy add +5 · with Laura (Sat 22:00–00:00) +2 · with Mark late +1 · with Ryan Sat, Sun 14:00–18:00 +1 | `movie_night`, 12 h | yes |
| a beer with Mark | person | home_life · Mark's ladder | 30 min · Mark's Want add +1 · `drinks_boost` on | `had_drink_home`, 12 h | yes |
| a random event | work | home_life | Mark asleep on the couch with the TV on (00:00–02:00, his row) | one a day | yes |

## Rows a gate needs

| row | gate |
|---|---|
| the couch at every hour | a destination is never open and exit-only |
| Mark's split night rows | standing surface (past midnight) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| Mark's late nights, split at midnight | LIVES §5 (fixed 10-06) |
| Laura waiting up on Saturday | LIVES §2 (lead's default, 10-06) |
| the couch row, read by her clothes | guess · the wardrobe sheet |
| the everyday rows | LO, 2026-10-08 (the everyday picks) · system `home_life` · times and numbers guess |
| Ryan's TV afternoons | LO, 2026-10-08 (question 55) |
