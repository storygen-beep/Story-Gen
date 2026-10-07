# [REVIEW] Person — Jake

> A draft for LO to place. Written 2026-10-08 against the place sheets. Id `npc_jake`.

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
| his line: Laura's dress | "Everyone was looking at you tonight." |

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
| `home_front_door` | Sat | 22:00 | 00:00 | brings her home after a date · only when `jake_date_booked` |

## Ladder — one guidance card per step (S10)

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 1 (Jake B 1) | `zoe_01_first_party` | `zoe_apartment` | Fri 19:00–23:00 | zoe_step eq 0 | the counter only | "Not tonight." (parked) | Friday evening at Zoe's party: a guy across the room won't stop looking. |
| 2 (Jake B 2) | `jake_02_kiss_on_the_quad` | `quad` | Mon, Wed, Fri 10:15–11:45 | Corruption 20 · Exhib. 20 | exhibitionism add +3 | "Not tonight." (parked) | A Monday, Wednesday or Friday morning on the quad: Jake and his team. |
| 3 (Jake B 3) | `jake_03_my_boyfriend` | `home_front_door` | Sat 23:00–00:00 | Corruption 20 · Exhib. 20 · `jake_date_booked` | the counter only | "Not tonight." (parked) | Saturday night: Jake at the front door, Ryan due home from Kayla's. |
| 4 (Jake B 4) | `laura_05_jake_at_the_door` | `home_front_door` | Sat 22:30–00:00 | Corruption 40 · Exhib. 40 · Laura's Want 40 · laura_step eq 4 · `jake_date_booked` | the counter only | "Goodnight, Jake." (parked) | Saturday night, after your date: kiss Jake goodnight at the front door, in Laura's dress. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

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
