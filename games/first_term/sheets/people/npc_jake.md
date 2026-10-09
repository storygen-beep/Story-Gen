# [READY] Person — Jake

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the place sheets. Id `npc_jake`.

| row | answer |
|---|---|
| age | 20 |
| role | campus guy |
| what she wants from him | a normal boyfriend |
| what he visibly wants, each visit | a girlfriend he can show off |
| what he keeps | step counter + memory flags |
| where he sleeps | offscreen |
| what he calls her | "@player" |
| met | Zoe's first party (Zoe A 1) |
| his line: short skirt | "Guys. Look at her." He says it to the team. |
| his line: Zoe's dress | His eyes go down her legs and stay there. |
| his line: Laura's dress | "Everyone was looking at you tonight." (at the door after a date only) · campus: "Is that your mom's?" |

## Crude words, by stage (SP2: "on their sheets")

| column | words |
|---|---|
| early (stages 1–2) | ass |
| middle (stage 3) | ass, tits, cock |
| late (stages 4–5) | cock, fuck, cum |

A ceiling, never a floor. LO took these, 2026-10-08.

## Schedule grid (S5)

| place | days | from | to | why he is there |
|---|---|---|---|---|
| `quad` | Mon, Wed, Fri | 08:30 | 11:45 | with the team |
| `zoe_apartment` | Fri | 19:00 | 00:00 | the Friday party, till midnight |
| `canteen` | Mon–Fri | 11:45 | 13:00 | lunch |
| `campus_gym` | Tue, Thu | 15:00 | 17:00 | team training · only when `jake_number` (met at Zoe's) |
| `home_front_door` | Sat | 19:00 | 21:00 | picks her up · only when `jake_date_booked` (question 73) |
| `home_front_door` | Sat | 22:00 | 00:00 | brings her home after a date · only when `jake_date_went` (she left with him tonight) |

## Ladder — one guidance card per step (S10)

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 1 (Jake B 1) | `zoe_01_first_party` | `zoe_apartment` | Fri 19:00–23:00 | zoe_step eq 0 | the counter only | "Not tonight." (parked) | Friday evening at Zoe's party: a guy across the room won't stop looking. |
| 2 (Jake B 2) | `jake_02_kiss_on_the_quad` | `quad` | Mon, Wed, Fri 10:15–11:45 | Corruption 20 · Exhib. 20 | exhibitionism add +3 | "Not tonight." (parked) | A Monday, Wednesday or Friday morning on the quad: Jake and his team. |
| 3 (Jake B 3) | `jake_03_my_boyfriend` | `home_front_door` | Sat 23:00–00:00 | Corruption 20 · Exhib. 20 · `jake_date_booked` | the counter only | "Not tonight." (parked) | Saturday night: Jake at the front door after your date; Ryan is home by then. |
| 4 (Jake B 4) | `laura_05_jake_at_the_door` | `home_front_door` | Sat 22:30–00:00 | Corruption 40 · Exhib. 40 · Laura's Want 40 · laura_step eq 4 · `jake_date_booked` | the counter only | "Goodnight, Jake." (parked) | Saturday night, after your date: kiss Jake goodnight at the front door, in Laura's dress. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

## Card goals (LO's play note, 2026-10-08)

Each guidance card's goals are the step's real requirements: the meters, flags, place and hour in its
row above. Never the step counter (no "1 / 2"). A requirement on another person's ladder is named as
the event, e.g. "after Ryan's feet-in-his-lap night".


### Leak and promise (S5)

| n | the leak: his want, shown before | the promise: the line it ends on |
|---|---|---|
| 1 | he watches her across the room, not Zoe | "Wasn't planning to stop." |
| 2 | his hand low on her back on the quad | "Saturday. Pick me up at the door." |
| 3 | "Your brother hates me." | "Ryan, this is Jake. My boyfriend." |
| 4 | "Is your mom up?" | "Higher. Don't stop." |

**Final no:** "Don't come to the door again. (ends his path)", offered only at his step 6, after 0.1. In 0.1 his nos are parked.

**What the last 0.1 step turns into:** the Saturday dates repeat, booked on his thread, ending at the front door.

**After** (SP2, where the arc ends, past 0.1): the dates repeat, booked on his phone thread, and the house and campus treat him as hers.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `jake` | `jake_number` (Zoe A 1) | 1 day | 18:00–22:00 | "Saturday? I'll pick you up." sets `jake_date_booked` · reminder: quest card, hub line | after step 4: every 7 days, Thursday 18:00–22:00 |

**Jake B 4 is Laura C 5**: one canvas, read by both counters. It waits for Laura C 4 too.

### Messages, per reply (LO's note, 2026-10-08)

Each follow-up waits for her reply (`after_round`), and a different answer follows each reply where it matters (`after_choice`). Texts are lowercase, 3–7 words. Lines are samples (guess). The date is booked only by her yes; nothing names a pickup before it.

| round | Jake | her reply | after that reply |
|---|---|---|---|
| 1 | "saturday? i'll pick you up" | "yes" | "front door. eight. wear something" · sets `jake_date_booked` |
| | | "not this week" | "next week then. i'm patient" |
| | | "where are we going" | "surprise. yes or no?" (round 2) |
| 2 (after "where") | — | "yes" | "front door. eight." · sets `jake_date_booked` |
| | | "no" | "next week then" |

## Rows a gate needs

| row | gate |
|---|---|
| the step counter read by every gate | ladders move forward |
| `jake_date_booked` set by the thread, cleared by the door | a flag that never resets (lint) |
| the booking shown on a card | the phone: a booking she can see |

## Why — the source of each key choice

| key choice | source |
|---|---|
| steps and nos | SP2 · the arc ideas (Jake B) |
| dates booked on his thread | LO, 2026-10-07 |
| the shared step | LO, 2026-10-08 (SP3) |
| the thread's timing | guess |
| messages per reply | LO's play note, 2026-10-08 (chats wait for her reply) · lines guess |
| the pickup only after her yes | sweep A6-19, A6-20 |
| his gym rows | LO, 2026-10-08 (question 64) |
| fix from the false-line sweep | sweep A4-03, A4-10, A4-40 (2026-10-08) |
| card goals are the step's real requirements | LO's play note, 2026-10-08 · sweep K8 and its 38 more cards |
