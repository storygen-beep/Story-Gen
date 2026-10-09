# [READY] Person — Zoe

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the place sheets. Id `npc_zoe`.

| row | answer |
|---|---|
| age | 19 |
| role | her friend |
| what she wants from her | someone to follow into fun |
| what she visibly wants, each visit | a partner in trouble; she wants @player, and dares instead of asking |
| what she keeps | step counter + memory flags |
| where she sleeps | `zoe_bedroom` |
| what she calls her | "babe" |
| met | the quad, week 1: `zoe_00_quad_meeting` sets `zoe_met` |
| her line: short skirt | "Now we're talking. Turn around." |
| her line: no bra | "Oh, you're ready for Friday." |
| her line: her party dress | She bites her lip at the bra strap. "Nope. Eyes stay." |

## Crude words, by stage (SP2: "on their sheets")

| column | words |
|---|---|
| early (stages 1–2) | tits, ass |
| middle (stage 3) | tits, nipples, wet |
| late (stages 4–5) | pussy, clit, fuck |

A ceiling, never a floor. LO took these, 2026-10-08.

## Schedule grid (S5)

| place | days | from | to | why she is there |
|---|---|---|---|---|
| `quad` | Tue, Thu, Fri | 14:30 | 18:00 | between classes |
| `party_house` | Sat | 20:00 | 00:00 | the party house, the hot tub (Zoe A 3); above her living-room row |
| `zoe_apartment` (her living room) | Mon–Thu | 18:00 | 22:00 | home evenings |
| `zoe_apartment` (her living room) | Fri, Sat | 18:00 | 00:00 | Friday party · Saturday evening |
| `zoe_apartment` (her living room) | Sat | 00:00 | 02:00 | the Friday party after midnight |
| `zoe_bedroom` | Mon–Thu | 22:00 | 00:00 | going to bed: she lends the dress |
| `canteen` | Mon–Fri | 11:45 | 13:00 | lunch |
| `park` | Sat, Sun | 08:00 | 10:00 | her weekend run |

## Everyday: make-up before the party (LO's pick 12, 2026-10-08)

A choice in Zoe's hub in her living room, Friday 18:00–19:00, before the party: "Lips. Open." Zoe does
@player's face; `made_up` set true (10 hours). Curious: she does it sitting in @player's lap. Lines guess.

## Ladder — one guidance card per step (S10)

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 1 (Zoe A 1) | `zoe_01_first_party` | `zoe_apartment` | Fri 19:00–23:00 | jake_step eq 0 | exhibitionism add +3 | "Not tonight, Zo." (parked; costs nothing) | Friday evening: Zoe's party at her apartment, and she has a dress for you. |
| 2 (Zoe A 2) | `zoe_02_bra_through_the_sleeve` | `zoe_apartment` | Fri 21:00–00:00 | Corruption 20 · Exhib. 20 | exhibitionism add +3 | "Not tonight, Zo." (parked) | A Friday party at Zoe's, out on the balcony: Zoe has a dare. |
| 3 (Zoe A 3) | `zoe_03_hot_tub` | `party_house` | Sat 20:00–00:00 | Corruption 40 · Exhib. 40 | exhibitionism add +3 · corruption add +3 | "Not tonight, Zo." (parked) | Saturday night: the hot tub at the party house. Zoe's friends head inside first. |
| 4 (Zoe A 4) | `zoe_04_i_pick_the_dares` | `zoe_apartment` | Mon–Thu 18:00–22:00 · Sat 18:00–20:00 | Corruption 40 | the counter only | Zoe's: "Not that one, babe." (parked) | An evening at Zoe's, on her couch, after the hot tub. |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

## Card goals (LO's play note, 2026-10-08)

Each guidance card's goals are the step's real requirements: the meters, flags, place and hour in its
row above. Never the step counter (no "1 / 2"). A requirement on another person's ladder is named as
the event, e.g. "after Ryan's feet-in-his-lap night".


### Leak and promise (S5)

| n | the leak: his want, shown before | the promise: the line it ends on |
|---|---|---|
| 1 | her head in @player's lap on the quad: "Let them." | "Kiss someone. Or don't, and I'll keep asking." |
| 2 | she keeps her eyes on the bra strap | "Nope. Mine now." |
| 3 | "There's a hot tub Saturday. Just us." | "Took you long enough." |
| 4 | "You didn't need me last night." | "From now on, I pick the dares." |

**Final no:** none. Every dare has "Not tonight, Zo" (parked, costs nothing).

**What the last 0.1 step turns into:** party nights are @player's call: she sets Zoe's dares.

**After** (SP2, where the arc ends, past 0.1): Zoe hands her the call on party nights, and what she brings home feeds Ryan and Laura.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `zoe` | `zoe_met` | 1 day | Thursday 18:00–22:00 | "Party Friday. Wear something short." her apartment, Fri 19:00 · reminder: quest card | every 7 days, Thursday |
| the run | `zoe_met` | 2 days | Friday 18:00–22:00 | "Run tomorrow? 8. The park." · reminder: quest card | every 7 days |

### Messages, per reply (LO's note, 2026-10-08)

Each follow-up waits for her reply (`after_round`), and a different answer follows each reply where it matters (`after_choice`). Texts are lowercase, 3–7 words. Lines are samples (guess).

**`zoe` — the party.** Thursday 18:00–22:00.

| round | Zoe | her reply | after that reply |
|---|---|---|---|
| 1 | "party tmrw. wear something short" | "obviously" | "that's my girl 😈" |
| | | "what counts as short" | "come by tonight. i'll lend you one" (Zoe is home till midnight) |
| | | "can't. my mom" | "sneak out. kidding. kinda" |

**The run.** Friday 18:00–22:00. "8, the park" is a meeting time, a rule of the world.

| round | Zoe | her reply | after that reply |
|---|---|---|---|
| 1 | "run tmrw? 8. the park" | "i'm in" | "wear the sports bra 😏" · sets `zoe_run_booked` |
| | | "too early" | "lazy. next week then" |

## Rows a gate needs

| row | gate |
|---|---|
| the step counter read by every gate | ladders move forward |
| her park row has a hub | standing surface |

## Why — the source of each key choice

| key choice | source |
|---|---|
| steps, lines and nos | SP2 · the arc ideas (Zoe A) |
| the park on weekend mornings | LO, 2026-10-08 |
| Zoe A 3: only Zoe sees her | LO, 2026-10-08 |
| the threads | guess |
| her rows split by room in her flat | LO, 2026-10-08 (questions 47, 48, narrowed by 52) |
| Zoe at the party house Sat 20:00–00:00 | LO, 2026-10-08 (sweep A4-08) |
| messages per reply | LO's play note, 2026-10-08 (chats wait for her reply) · lines guess |
| fix from the false-line sweep | sweep A4-09 (2026-10-08) |
| card goals are the step's real requirements | LO's play note, 2026-10-08 · sweep K8 and its 38 more cards |
