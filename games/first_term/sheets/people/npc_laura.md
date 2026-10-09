# [READY] Person — Laura

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

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
| her line: no bra | Her eyes stop on @player's chest, then she pours the coffee (breakfast) or the wine (evenings). |
| her line: towel | Kitchen: "Robe, sweetheart. Not at my table." · the hall (the stairs, at night): "Hall's cold, sweetheart. Don't stand there." |

## Schedule grid (S5)

| place | days | from | to | why she is there |
|---|---|---|---|---|
| `home_hall` | every day | 23:00 | 02:00 | the catch on the dark stairs · only when `came_home_late` was set in the last 4 hours (question 69) |
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
| 3 (Laura C 3) | `laura_03_wine_in_the_kitchen` | `home_kitchen` | Mon, Tue, Thu, Fri 20:00–22:00 | Corruption 20 · Exhib. 20 · her Want 20 | want add +10 | "I'm tired, Mom." (parked) | Late evening in the kitchen: Laura has a glass of wine. |
| 4 (Laura C 4) | `laura_04_ryans_door` | `home_ryan_room` | Mon, Tue, Thu, Sun 20:00–22:00 | Corruption 20 · Exhib. 20 · her Want 30 · ryan_step gte 4 (card goal: "after Ryan's feet-in-his-lap night") | want add +10 | "It's nothing. (she'll know)" (parked) | An evening in Ryan's room, your feet in his lap: Laura opens the door. |
| 5 (Laura C 5) | `laura_05_jake_at_the_door` | `home_front_door` | Sat 22:30–00:00 | Corruption 40 · Exhib. 40 · her Want 40 · jake_step eq 3 · `jake_date_booked` | want add +10 | "Goodnight, Jake." (parked) | Saturday night, after a date with Jake: the front door. Laura waits up. |
| 6 (Laura C 6) | `laura_06_take_me_with_you` | `home_master_bedroom` | Sat 17:00–18:30 | Corruption 40 · Exhib. 40 · her Want 50 | want add +10 | "Ask Mark." (parked) | Saturday early evening: Laura is dressing to go out. Zip her up. |
| 7 (Laura C 7) | `laura_07_dark_stairs` | `home_kitchen` | Fri 18:00–21:00 | Corruption 40 · Exhib. 40 · her Want 60 · zoe_step gte 1 | want add +10 · corruption add +3 | "Not tonight, Mom." (parked) | Friday evening: Laura wants to come to Zoe's party. Leave together from the kitchen. |
| 8 (Laura C 8) | `laura_08_it_wasnt_the_wine` | `home_kitchen` | Mon–Fri 06:30–08:00 (Monday's breakfast after the party) | Corruption 40 · Exhib. 40 · her Want 70 | want add +10 | "It was the wine." (parked) · hers: "I'm your mother." | Monday's breakfast: Laura is in the kitchen. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

## Card goals (LO's play note, 2026-10-08)

Each guidance card's goals are the step's real requirements: the meters, flags, place and hour in its
row above. Never the step counter (no "1 / 2"). A requirement on another person's ladder is named as
the event, e.g. "after Ryan's feet-in-his-lap night".


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

## Everyday at home (system `home_life`, LO's picks, 2026-10-08)

Each item is a choice inside Laura's hub in that room and window, never its own scene. Raise: Laura's
Warmth add +1 (movie night +2), once a day per item. Tease from Curious and Laura C 1; touch from Bold
and Laura C 7; her sex version waits for Hungry ("Needs Hungry"). Lines are samples (guess).

| item | where · when | plain (Good Girl) | tease (Curious) | touch (Bold) |
|---|---|---|---|---|
| breakfast | kitchen · Mon–Fri 06:30–08:00 | "Eat something before class, sweetheart." She pushes the toast over. | She sees no bra and pours the coffee slower. "Cold this morning?" Her eyes stay on @player's chest. | Her hand smooths @player's hair, slides down to the nape, stays. "Look at you. Who are you dressing for?" |
| coffee | kitchen · Mon–Fri 06:30–08:00 | Two mugs. "Tell me one thing about yesterday." | "Is that a new top?" She tugs the hem, and her knuckles brush bare skin. | She drinks from @player's mug, lips on the same spot, watching. |
| dinner | kitchen · Mon, Tue, Thu, Fri, Sun 18:00–20:00 | "How's college?" She actually waits for the answer. | @player in a short skirt at the table. "Is that for college or for a guy?" She keeps looking at @player's legs. | Under the table her foot finds @player's ankle and doesn't move. |
| help her cook | kitchen · Mon, Tue, Thu, Fri, Sun 18:00–19:00 | She hands over the knife. "Onions. Don't cry on my sauce." | She ties the apron on @player, her hands at @player's waist a beat too long. | She stands behind @player at the stove, hands on @player's hips, chin on @player's shoulder. "You've got my hips." Her thumbs push under the waistband. |
| dishes | kitchen · Mon, Tue, Thu, Fri, Sun 19:00–21:00 | "You wash, I dry." Hip to hip at the sink. | Water down @player's top; Laura's eyes on the wet cloth over @player's tits. "You'll catch cold." | She peels the wet shirt off @player's chest with two fingers, and @player's nipples go hard under Laura's eyes. |
| a glass of wine | kitchen · same evenings 20:00–22:00 · after Laura C 3 | "One glass. Don't tell Mark." | "Did anyone look at you today?" She wants the answer. | Her glass at @player's lips. "Like you get looked at." Her other hand on @player's thigh. |
| movie night | living room · Sat 22:00–00:00 (she waits up) | A film on low. "Sit with me till Mark's asleep." | @player's head in Laura's lap; her fingers in @player's hair, then on @player's throat. | Under the blanket her hand rests on @player's chest, over the nipple, and neither of them says so. |
| the grocery run | asked at dinner · delivered at her next evening | "Could you get these? Here's twenty." | — | — |
| study at the table | kitchen · her evenings 19:00–22:00 | She reads over @player's shoulder. "That's wrong. No — that." | Her hand on the back of @player's neck while she reads. | — |
| her hair | master bedroom · Sat 17:00–18:30, Laura dressing | Laura brushes @player's hair out at her mirror. "You had my hair at your age." | She pins it up and looks at @player's bare shoulders in the mirror, then at @player's chest. | — |
| tidy check | kitchen · Sunday dinner reads `room_tidy` | tidy: "Your room looked nice." Warmth add +2 · messy: "Pigsty." Warmth add −1 | tidy, Curious: "Your underwear was on the bed. The lace one." | — |

**Breakfast and dinner match who is in the kitchen** (LIVES): breakfast is Laura on weekdays only;
weekend days she is out. Wednesday dinner is Mark's, because the clinic keeps her late.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `laura` | `laura_01_done` (the blue dress) | 1 day | Mon, Tue, Thu, Fri, Sun 16:00–17:30 | "Home for dinner?" the kitchen, 18:00 · reminder: hub line | none in 0.1: her sex step is later |
| her call | `curfew` (her scene) | none | Friday 21:00–22:00, Laura awake in the kitchen | a call: missed costs `laura_suspicion` add +2; it never claims where she is | one call per curfew (calls don't repeat) |

**`laura_suspicion`, its two 0.1 readers** (LO, 2026-10-08, question 5):

| reader | how it reads |
|---|---|
| her catch on the stairs | low: "Where were you?" · high: she checks the dress, the smell |
| the curfew | low Warmth, or suspicion 50 or more, sets it |

**What raises it** (LO, 2026-10-08): home late add +5 · a lie add +5 · a failing grade add +5 · the letter home add +10 · a missed call add +2.

### Messages, per reply (LO's note, 2026-10-08)

Each follow-up waits for her reply (`after_round`), and a different answer follows each reply where it matters (`after_choice`). Texts are lowercase, 3–7 words. Lines are samples (guess).

**`laura` — dinner.** Days she cooks only (Mon, Tue, Thu, Fri, Sun), window 16:00–17:30, so "six" is
still ahead. Comes back every 7 days.

| round | Laura | her reply | after that reply |
|---|---|---|---|
| 1 | "home for dinner sweetheart?" | "yes, starving" | "six. kitchen. don't be late" · Warmth add +1 |
| | | "eating out tonight" | "ok. text me when you're on your way" |
| | | "is mark cooking?" | "god no. it's me" |

**Her call — the curfew.** While `curfew` is set, Friday 21:00–22:00, when Laura is in the kitchen and
awake. She never says where @player is; the engine can't see that.

| Laura | her answer | after it |
|---|---|---|
| "It's nine. You know the rule. Home by eleven." | "I know. Eleven." | "Good girl." |
| | "I'm staying at Zoe's." | "We'll talk about this." · `laura_suspicion` add +2 |
| | (lets it ring) | `laura_suspicion` add +2 |

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
| her everyday items and lines | LO, 2026-10-08 (the everyday picks) · lines and numbers guess |
| messages per reply | LO's play note, 2026-10-08 (chats wait for her reply) · lines guess |
| the call at 21:00, Laura awake, no claim where she is | sweep A6-01 · question 63 |
| dinner text only on her days, before six | sweep A6-18 |
| fix from the false-line sweep | sweep A2-05, A2-22, A2-36 (2026-10-08) |
| the second glass on the counter shows only in the evening, after Laura C 3 | sweep A2-36 |
| her stairs row reads the flag for 4 hours only | question 69 · sweep A1-17, A2-01 |
| card goals are the step's real requirements | LO's play note, 2026-10-08 · sweep K8 and its 38 more cards |
| Laura C 4's card names the Ryan gate | sweep A2-32 |
