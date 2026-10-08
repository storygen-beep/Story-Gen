# [READY] Person — Ryan

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the place sheets. Id `npc_ryan`.

| row | answer |
|---|---|
| age | 22 |
| role | step-brother |
| what she wants from him | the one person at home on her side |
| what he visibly wants, each visit | her, and he stops hiding it |
| what he keeps | want + warmth |
| where he sleeps | `home_ryan_room` |
| what he calls her | `@player.nickname` (her nickname, default El) |
| met | day 1, the hall, out of the shower |
| his line: towel | "Door's free, @player.nickname." His eyes drop and come back up. |
| his line: short skirt | "You're wearing that downstairs?" He doesn't look away from her ass. |
| his line: no bra | He talks to her face, hard, and fails. |
| his line: underwear only | "Jesus. Mom's home." He shuts his door, then opens it again. |

## Schedule grid (S5)

| place | days | from | to | why he is there |
|---|---|---|---|---|
| `home_bathroom` | Mon–Fri | 06:45 | 07:30 | he showers first (Laura's rule) |
| `home_ryan_room` | Mon, Tue, Thu, Fri, Sun | 18:00 | 22:00 | home from the yard |
| `home_ryan_room` | Sat, Sun | 07:30 | 18:00 | home from the yard |
| `home_ryan_room` | every day | 22:00 | 06:45 | home from the yard |
| `home_ryan_room` | Sat | 18:00 | 22:00 | home from the yard · only when `ryan_cancelled_kayla` · later (Ryan A 12) |

His night row ends 06:45, so it doesn't overlap his bathroom row (LO, 2026-10-08).

## Ladder — one guidance card per step (S10)

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 1 (Ryan A 1) | `ryan_01_hall_first_morning` | `home_hall` | the opening | none | want add +10 | "Knock next time." (parked) · the day-one final, below | Your first morning: out of the bathroom, Ryan waiting in the hall. |
| 2 (Ryan A 3) | `ryan_02_phone_on_the_sink` | `home_bathroom` | Mon–Fri 07:00–07:30 | Exhib. 20 · his Want 10 | want add +10 | "Leave it." (parked) | A weekday morning in the bathroom: Ryan's phone buzzes on the sink. |
| 3 (Ryan A 4) | `ryan_03_shirt_off` | `home_ryan_room` | Mon, Tue, Thu, Sun 18:00–22:00 | Corruption 20 · Exhib. 20 · his Want 20 | want add +10 · corruption add +1 | "Never mind." (parked) | Ryan's room, an evening he's home (not Wednesday or Friday): knock. |
| 4 (Ryan A 5) | `ryan_04_feet_in_his_lap` | `home_ryan_room` | Mon, Tue, Wed, Thu, Sun 22:00–00:00 | Corruption 20 · Exhib. 20 · his Want 30 | want add +10 | "Just saying goodnight." (parked) | Ryan's room, late at night (not Friday): two knocks. |
| 5 (Ryan A 6) | `ryan_05_thin_walls` | `home_ella_room` | Fri 22:00–00:00 | Corruption 20 · Exhib. 40 · his Want 40 | want add +10 · corruption add +1 | "Put your headphones in." · "Roll over. Sleep." (parked) | Friday night in your bed: Kayla is over, and the wall is thin. |
| 6 (Ryan A 7) | `ryan_06_after_the_shower` | `home_bathroom` | Sat 08:00–10:00 | Corruption 40 · Exhib. 40 · his Want 50 | want add +10 · exhibitionism add +3 | "Reach for the towel." (parked) | Saturday morning, the shower: Kayla is still in the house. |
| 7 (Ryan A 8) | `ryan_07_first_kiss` | `home_ryan_room` | Mon, Tue, Thu, Sun 18:00–22:00 | Corruption 40 · his Want 60 | want add +10 · corruption add +3 | "Goodnight, Ryan." (parked) · his: "I've got a girlfriend." | Ryan's room, an evening he's home: two knocks. |
| 8 (Ryan A 9) | `ryan_08_two_knocks` | `home_ryan_room` | Mon, Tue, Thu, Sun 18:00–22:00 | Corruption 40 · his Want 70 | want add +10 | final: "Your secret's safe. You're my brother, that's all. (ends his path)" | Ryan's room, an evening after the kiss: two knocks, and ask what you get. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

### Leak and promise (S5)

| n | the leak: his want, shown before | the promise: the line it ends on |
|---|---|---|
| 1 | none: step 1, and it says so | "First day of college, huh. Look at you." |
| 2 | his eyes go to her and away too fast | "Sneaking her in past Mom, huh?" |
| 3 | "Don't." He holds the look a beat longer | two knocks: the code |
| 4 | he opens on the second knock, every time | "Liar." |
| 5 | his hand on her ankle while he lies to Kayla | "I am. Thin walls." |
| 6 | "I heard you last night. All of it." | "Good. Now you've seen it too." |
| 7 | he leaves his door open a hand's width | "Ignore it." |
| 8 | his phone face-down when she knocks | "Two knocks. Any night that isn't Friday." |

**Final no:** on day one, "Don't ever look at me like that. (ends his path)"; later, "Your secret's safe. You're my brother, that's all. (ends his path)". Either closes his steps; he stays her brother, and cold.

**What the last 0.1 step turns into:** two knocks at his door, any night but Friday. The door this release ends on; step 9 shows locked, naming Hungry.

**After** (SP2, where the arc ends, past 0.1): the knocks go on around his girlfriend's nights, and Laura's knowing grows.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `ryan` | `knows_about_kayla` (step 2) | 1 day | 21:00–23:00 | his room, tonight: "two knocks?" · reminder: quest card | after step 8: every 2 days, 22:00–00:00, not Friday |

## Rows a gate needs

| row | gate |
|---|---|
| Want read by every step gate | the men's numbers are read |
| Warmth read: his lines with Laura and Jake | the men's numbers are read |
| the two knocks repeat | the door can be seen again |

## Why — the source of each key choice

| key choice | source |
|---|---|
| steps, lines and nos | SP2 · the arc ideas (Ryan A, 10-06) |
| renumbered 1–8, old names kept | LO, 2026-10-08 (call 1a) |
| the door | LO, 2026-10-07 (SP7) |
| his lines per clothing state | guess |
| the thread's timing | guess |
