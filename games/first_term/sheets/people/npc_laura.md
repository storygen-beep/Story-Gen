# [READY] Person — Laura

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the place sheets. Id `npc_laura`.

| row | answer |
|---|---|
| age | 41 |
| role | mom |
| what she wants from her | to stay her good girl, and to be close to her |
| what she visibly wants, each visit | a happy house; she wants @player nearer than she says |
| what she keeps | want + warmth · also reads `laura_suspicion`, below |
| where she sleeps | `home_master_bedroom` |
| what she calls her | "sweetheart" |
| met | day 1, breakfast in the kitchen |
| her line: short skirt | "Is that for college or for a guy?" |
| her line: her blue dress | "It never fit me like that." Her hand smooths the hip. |
| her line: no bra | Her eyes stop on @player's chest, then she pours the coffee. |
| her line: towel | "Hall's cold, sweetheart. Don't stand there." |

## Schedule grid (S5)

| place | days | from | to | why she is there |
|---|---|---|---|---|
| `home_hall` | every day | 23:00 | 02:00 | the catch on the dark stairs · only when `came_home_late` |
| `home_kitchen` | Mon–Fri | 06:30 | 08:00 | breakfast; home evenings |
| `home_kitchen` | Mon, Tue, Thu, Fri, Sun | 18:00 | 22:00 | breakfast; home evenings |
| `home_master_bedroom` | Mon, Tue, Wed, Thu, Fri, Sun | 22:00 | 06:30 | sleeps; dresses Saturday |
| `home_master_bedroom` | Sat | 00:00 | 07:00 | sleeps; dresses Saturday |
| `home_master_bedroom` | Sun | 00:00 | 07:00 | sleeps; dresses Saturday |
| `home_master_bedroom` | Sat | 17:00 | 18:30 | sleeps; dresses Saturday |
| `home_living_room` | Sat | 22:00 | 00:00 | waiting up, Saturday |

**Row order matters.** The engine takes the first matching row, so her stairs row is first. Saturday 00:00–07:00 covers Friday night. Her night row ends 06:30 (all LO, 2026-10-08).

## Ladder — one guidance card per step (S10)

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 1 (Laura C 1) | `laura_01_blue_dress` | `home_master_bedroom` | Tue 18:00–22:00 | none | want add +10 · exhibitionism add +3 | "I can't take this." (parked) | Tuesday evening: Laura is in the kitchen, and she has a dress for you upstairs. |
| 2 (Laura C 2) | `laura_02_home_late` | `home_hall` | every day 23:00–01:00 | `came_home_late` · Exhib. 20 · her Want 10 | want add +10 | "I was at Zoe's. (she'll know)": Warmth −5 | Come home late: Laura waits on the dark stairs. |
| 3 (Laura C 3) | `laura_03_wine_in_the_kitchen` | `home_kitchen` | Mon, Tue, Thu, Fri, Sun 20:00–22:00 | Corruption 20 · Exhib. 20 · her Want 20 | want add +10 | "I'm tired, Mom." (parked) | Late evening in the kitchen: Laura has a glass of wine. |
| 4 (Laura C 4) | `laura_04_ryans_door` | `home_ryan_room` | Mon, Tue, Thu, Sun 20:00–22:00 | Corruption 20 · Exhib. 20 · her Want 30 · ryan_step gte 4 | want add +10 | "It's nothing. (she'll know)" (parked) | An evening in Ryan's room, your feet in his lap: Laura opens the door. |
| 5 (Laura C 5) | `laura_05_jake_at_the_door` | `home_front_door` | Sat 22:30–00:00 | Corruption 40 · Exhib. 40 · her Want 40 · jake_step eq 3 · `jake_date_booked` | want add +10 | "Goodnight, Jake." (parked) | Saturday night, after a date with Jake: the front door. Laura waits up. |
| 6 (Laura C 6) | `laura_06_take_me_with_you` | `home_master_bedroom` | Sat 17:00–18:30 | Corruption 40 · Exhib. 40 · her Want 50 | want add +10 | "Ask Mark." (parked) | Saturday early evening: Laura is dressing to go out. Zip her up. |
| 7 (Laura C 7) | `laura_07_dark_stairs` | `home_kitchen` | Fri 18:00–21:00 | Corruption 40 · Exhib. 40 · her Want 60 · zoe_step gte 1 | want add +10 · corruption add +3 | "Not tonight, Mom." (parked) | Friday evening: Laura wants to come to Zoe's party. Leave together from the kitchen. |
| 8 (Laura C 8) | `laura_08_it_wasnt_the_wine` | `home_kitchen` | Mon–Fri 06:30–08:00 | Corruption 40 · Exhib. 40 · her Want 70 | want add +10 | "It was the wine." (parked) · hers: "I'm your mother." | The next breakfast: Laura is in the kitchen. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

### Leak and promise (S5)

| n | the leak: his want, shown before | the promise: the line it ends on |
|---|---|---|
| 1 | none: step 1, and it says so | "It never fit me like that." |
| 2 | she looks too long at the dress | "Did anyone look at you in it?" |
| 3 | she keeps a glass poured for two | "Like you get looked at." |
| 4 | she asks about Ryan, lightly | "Mark doesn't need to hear about this." |
| 5 | "Is Jake bringing you home?" | "Was he any good?" |
| 6 | she leaves her door open while dressing | "Take me with you one night." |
| 7 | "Wear something short." Her own words, back | "Don't stop for him." |
| 8 | she can't meet @player's eyes at breakfast | "I'm your mother." |

**Final no:** "You're my mom. That's all you get to be. (ends her path)". Every catch after is a strict-mom punishment.

**What the last 0.1 step turns into:** her catches go on: home late, she waits on the stairs, and "tell me everything" reads her suspicion.

**After** (SP2, where the arc ends, past 0.1): her catches keep coming, and her questions become foreplay.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `laura` | `laura_01_done` (the blue dress) | 1 day | 17:00–20:00 | "Home for dinner?" the kitchen, 18:00 · reminder: hub line | none in 0.1: her sex step is later |
| her call | `curfew` (her scene) · she is out after 23:00 | none | 23:00–01:00 | a call: missed costs `laura_suspicion` add +2 | one call per curfew (calls don't repeat) |

**`laura_suspicion`, its two 0.1 readers** (LO, 2026-10-08, question 5):

| reader | how it reads |
|---|---|
| her catch on the stairs | low: "Where were you?" · high: she checks the dress, the smell |
| the curfew | low Warmth, or suspicion 50 or more, sets it |

**What raises it** (LO, 2026-10-08): home late add +5 · a lie add +5 · a failing grade add +5 · the letter home add +10 · a missed call add +2.

## Rows a gate needs

| row | gate |
|---|---|
| her stairs row first in her list | standing surface (Laura there for the catch) |
| `laura_suspicion` read twice | a meter is read |
| Want read by every step gate | the men's numbers are read |

## Why — the source of each key choice

| key choice | source |
|---|---|
| steps, lines and nos | SP2 · the arc ideas (Laura C) |
| two suspicion readers | LO, 2026-10-08 (question 5) |
| the raise sizes, the 50 | LO, 2026-10-08 (question 20) |
| first-match row order | `v2.py:4304-4318` |
| her lines per clothing state | guess |
