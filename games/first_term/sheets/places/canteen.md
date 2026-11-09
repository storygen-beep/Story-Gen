# [READY] Place — Canteen
> Changed 2026-11-09 (DECISIONS 210, LO: "Go ahead"): showing off to get something, new section at the end. Signed by LO 2026-11-09 ("Sign them").
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. New section: what the heat proposal built here.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `canteen`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | campus |
| labels — what kind of place | `zone:campus`, `public`, `sells_food` |
| hours | Mon–Fri 08:00–18:00 |
| closed text | "The canteen is shut." |
| hidden until | no |
| fill — word budget | 2,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Zoe, Jake, Nadia: weekdays 11:45–13:00 | eat · listen to what they say | campus |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| eat | need | energy · money | energy add +20 · money add −5 (guess) · price on the label | once a day, on the trigger | yes, short |
| sit with the table | person | college · `campus_talk` | `campus_talk` add +1 (guess) · the rival may start trouble | once a day, lunch | yes |
| listen | work | college · `campus_talk` | none · what they say reads `campus_talk` | none needed: it writes nothing | yes |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Zoe | Eat ($5), Listen to what they say | Mon, Wed, Fri 11:45–12:00 | none: no meter | "Let it stay." Corruption +1, cap 39 |
| Jake | Eat ($5), Listen to what they say | Tue, Thu 11:45–12:00 | none: no meter | "Leave it." Exhibitionism +1, cap 19 |
| Nadia | Eat ($5), Listen to what they say | Mon, Tue, Wed, Thu, Fri 12:00–12:15 | none: no meter | a line only, no pay |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| Zoe under the table (A2) | her canteen hub, at lunch | "Let her." Hungry 60, Corruption +1, cap 79 · "Not here, Zo." pays 0 |

## Rows a gate needs

| row | gate |
|---|---|
| food costs money | money gates something · a price is on its label |
| `campus_talk` fed and read here | a meter is read |
| eat every weekday | a need can be met every day (with the bed) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| canteen food costs money; talk spreads | LO, chat 2026-10-07 (SYSTEMS §3, §9) |
| lunch for Zoe, Jake, Nadia | LIVES §3 |
| hours | LO took the guess, 2026-10-08 |
| the price and energy | guess |

## Zoe's crowd (2026-11-09, DECISIONS 210)

Row "Find someone for Zoe's party", weekdays 11:30-14:00, once a day: a guy eating alone at the end of the long table. Zoe texts once she has been to one of her parties and is Daring (Exhibitionism 20): bring her ten people (`phone.py` `zoe_crowd`; a no lets the text come back in a week, ignoring it costs her patience). After a yes, the quad, the gym and the canteen each have one ask a day, "Find someone for Zoe's party", until ten are coming (hidden count `zoe_crowd`). Asking plainly always gets a no and counts nothing. A show at her stage gets a yes: close (20, pays to 39); her panties under a short hem, or a stretch on the gym mats (40, pays to 59, campus talk +1); her bare tits for three seconds (60, pays to 79, campus talk +1). The screen after each yes says the count in that place's words. Source: `iterations/002/build_scripts/goals.py`.
