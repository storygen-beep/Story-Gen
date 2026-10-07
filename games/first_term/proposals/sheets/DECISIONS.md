# [REVIEW] Decisions — First Term

> A draft for LO to place (it lives at the game's root once placed). Written 2026-10-08, phase board.
> This sheet and the ledger say the same thing. Where they differ, it is listed below, and nothing
> was changed in the ledger.

## Open questions for LO — first

| # | question | recommendation | why it matters |
|---|---|---|---|
| 36 | Ledger change 3: name `laura_suspicion`'s 0.1 readers. | LO: when he signs Laura's sheet. | Waiting on that sign-off. |
| 37 | WANT.md still says the park is on her walk to campus. | LO: fix it at the next WANT.md re-sign. | SYSTEMS §14 says it isn't. |
| 39 | SYSTEMS.md:498 says `came_home_late` is set at the front door. | LO: fix it at the next SYSTEMS re-sign. | Question 35 moved it to the street's way home. |
| 40 | `party_hookup`: who is it with, and how far does it go? | LO holds it: a heat call not made yet. | It is the party's Bold repeat; no scene sheet until then. |

## Answered (LO, 2026-10-08)

| # | question | LO's answer |
|---|---|---|
| 1 | Her face | Later: it is needed for the media before the build, not the sheets. |
| 2 | Tom's last step | The kiss after close repeats on Friday nights. |
| 3 | Tom B 7–9 | After 0.1. |
| 4 | Hygiene, colour only | Keep it. LO's call holds over the skill rule. |
| 5 | `laura_suspicion` has no reader | Laura's sheet adds two readers. |
| 6 | Zoe A 3 and SP2's group rule | Stays at stage 3; her friends leave the tub first, so only Zoe sees. |
| 7 | Nobody in the park | Zoe runs there weekend mornings. Ryan and Jake joining her wait for later. |
| 8 | The first explicit scene | The park couple: she walks into them, sees, and runs. |
| 9 | Small pools | Accept the warning for 0.1. |
| 10 | `party_hookup` and `park_hidden` | Add both. |
| 11 | The counts | The ledger is right: 37 rows, 110,500 words. |
| 12 | Which rooms get a door | Ryan's room and the master bedroom. |
| 13 | Touching herself alone | Yes, from Curious: her bed, the shower, the college toilet. |
| 14 | Alone in an office | Her grade posted on the door; open in their person's hours. |
| 15 | The party house hours | Saturday 20:00 to Sunday 03:00: Zoe A 3 has her home at 3 a.m. |
| 16 | Hours for the other places | The guesses on the sheets. |
| 17 | Readers for `campus_talk` and `followers` | The quad and canteen overhear; her room's feed. |
| 18 | Hale B 2, no panties at Daring | Yes, for that step only; the wardrobe rule stays at Showing. |
| 19 | Vance's numbers | Porch line at Want 30 and 60; at Power 60 he asks for her. |
| 20 | `laura_suspicion` | Late +5, a lie +5, failing +5, the letter +10; curfew at 50. |
| 21 | Phone threads | Seven; Hale's a college email; Laura's curfew call. |
| 22 | Guessed names and flags | Taken as guesses. |
| 23 | Mark at Monday breakfast | Yes, leaving for work at 07:40, in the opening only. |
| 24 | The hygiene choice | On the last opening screen. |
| 25 | The start choice's readers | Laura at dinner, Zoe at the first party, Hale in his office. |
| 26 | The opening card | First class 08:30 · ask the café for a job · $75 by Sunday. |
| 27 | Where the skip lands | On the last screen, every flag set. |
| 28 | The crude-word columns | Early: stages 1–2 · middle: stage 3 · late: stages 4–5. |
| 29 | Ryan's repeat in 0.1 | A kiss and his hands. |
| 30 | Step 5 into Saturday dawn | One canvas. |
| 31 | Second person | Yes: `narration_person = "second"` in the ledger. |
| 32 | Crude words for Tom, Zoe, Hale, Jake | A row on each person sheet, before their scenes. |
| 33 | "Twenty, and you can look" at the repeat table | Yes, from Bold, the price on the button. |
| 34 | The proposed crude words | Taken as proposed. |
| — | Mark A 5's `stop` screen, last sentence | Kept: on her body, not a pivot. |
| 35 | The front door as the way in | B: keep the tree. Only the street's way home, at 22:00 or later, sets `came_home_late`. |
| 38 | Drop `laura_suspicion` from the money card's feeds | Yes. |
| — | Tom B 4's `ten` screen, last sentence | Kept: on the body. |
| 41 | Crude words for strangers, extras, her alone | Taken: tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy. |
| — | A second voice for touching herself | No: stages 2–3 share "warming up"; the bold voice starts at stage 4. |

**Question 6 keeps SP2 as signed.** Only Zoe sees her, which is Bold: naked by choice for someone she knows.
The step's hint and who-notices line in the ledger still name the friends (ledger change 11).

**Question 8, the beat.** She walks the path, walks into a couple in the bushes, sees them, and runs: an
accident, allowed at Good Girl. Curious adds "Stay and watch". Day one reaches it.

## Clashes: a skill rule against a signed page (S12)

| | the skill says | the signed page says | LO's answer |
|---|---|---|---|
| hygiene | *"A restore with no gate behind it is a button that maintains a number."* | *"Colour only, never a story lock."* | the page holds (2026-10-08) |

## Settled

| locked forever | expensive to change | cheap to change |
|---|---|---|
| every id: places, people, canvases | the map tree, street as the ground | each room's word budget |
| every trait and flag key | the anchor: the kitchen | shop hours and prices |
| her two meters run 0–100 | her stage edges: 20, 40, 60, 80 | energy costs and refills |
| the name tokens: `@player`, `@player.nickname` | rent: $75, rising to $90 and $100 | raise sizes on small acts |
| everyone's age, all 18 or older | the door: Ryan's two knocks | pool contents and their order |
| the title, First Term | who climbs: both | guidance card wording |

## The ledger keys

| ledger key | value |
|---|---|
| `board.map.archetype` · `exterior` | `nested_zones` · `street`, the only root |
| `board.map.home_base` | `home_ella_room` |
| `board.map.homes` | Ryan, his room · Laura and Mark, theirs · Zoe, hers · Vance, `vance_house` |
| `board.who_climbs` | `both` |
| `board.ascent_tiers` | `corruption`, `exhibitionism` · ceilings 100 each · start 0 |
| `board.economy` | `$` · a top week pays $232 · rent $75, Sunday 00:00, to Mark |
| obligation moves | $90 after $300 paid · $100 after $900 · then flat |
| `board.economy.sinks` | rent · canteen food · the clothes shop |
| `board.needs` | `energy`: spent, a real lock · `hygiene`: colour only, with an off switch |
| the anchor | `home_kitchen`: 28,000 of 110,500 words, 25.3%. It reaches 25%, barely. |
| places | 31 declared; 29 in 0.1 (no corner shop, no men's toilet) |
| people | 21; 7 with ladders, 44 steps |
| `release_page.door` | `ryan_08_two_knocks` · "Two knocks" · step 9 locked, naming Hungry |

**The anchor is tight.** Other rooms can grow by about 1,500 words in total before the kitchen drops under
25%. Past that, every 1,000 words elsewhere needs about 330 more in the kitchen.

## Where the sheets and the ledger differ

| # | what | the ledger | the signed page or sheet |
|---|---|---|---|
| 1 | coverage rows | 37 | LO: the ledger is right |
| 2 | total word budget | 110,500 | LO: the ledger is right |
| 3 | college card acts | fixed: marked 0.2 | — |
| 4 | college card acts | fixed: the guy beside her added | — |
| 5 | `laura_suspicion` readers | "Ryan A 13" | a later step; nothing in 0.1 |
| 6 | the park's people | fixed: Zoe only, weekend mornings | — |
| 7 | key items | fixed: the slutty uniform dropped for now | — |
| 8 | `intelligence` fed at | fixed: the lecture hall added | — |
| 9 | Ryan steps 3 and 5 | fixed: Corruption +1 | — |
| 10 | the park | its own place | WANT.md still says she walks through it to campus |
| 11 | Tom's last step | 6 | SP5 fixed to step 6; it waits for your re-sign |

Row 10 is an older signed page behind a newer one. The newer page holds; WANT.md's line needs your
edit when you next re-sign it.

## Ledger changes

**Written 2026-10-08 with LO's yes** (backup: `first_term_snapshots/20261008_sheets_ledger_before/`):

| # | change |
|---|---|
| 1 | College card: the art lecturer, TA and dean acts marked "0.2" |
| 2 | College card: the guy beside her added at rungs 2 and 3 |
| 4 | Park `leads_to`: `npc_zoe` added |
| 5 | Zoe: a park row, Saturday and Sunday 08:00–10:00 |
| 6 | `cafe_uniform_slutty` dropped from key items until its release |
| 7 | `park_hidden` and `party_hookup` added to their pools |
| 8 | Ryan steps 3 and 5: Corruption +1, not +3 |
| 9 | `intelligence` fed in the lecture hall too |
| 10 | Park `people`: Zoe only; Ryan and Jake noted as later |
| 11 | Zoe A 3's hint and who-notices: Zoe alone |
| 12 | Job card: Tom's kiss repeats on Friday close |
| — | SP5 set to REVIEW in the ledger, with the page |


**Written 2026-10-08 with LO's yes, batch 2** (backup: `first_term_snapshots/20261008_places_ledger_before/`):

| # | change |
|---|---|
| 13 | `hours` and `closed_text` on 18 places; the rest always open or not in 0.1 |
| 14 | an `alone` row on every destination |
| 15 | `hidden_until`: `zoe_met` (apartment, bedroom), `party_house_invite`, `dean_summons` |
| 16 | park `serves.people`: `npc_zoe` |
| 17 | energy `fills`: the party house soak |
| 18 | a `door` on Ryan's room and the master bedroom |

**Written 2026-10-08 with LO's yes, batch 3** (backup: `first_term_snapshots/20261008_people_ledger_before/`):

| # | change |
|---|---|
| 19 | Laura's stairs row moved to the top of her list |
| 20 | Laura: master bedroom, Saturday 00:00–07:00 |
| 21 | Ryan's night row ends 06:45; Laura's ends 06:30 |
| 22 | Vance: `read_by` and `raised_by` on his Want and Power |

**Written 2026-10-08 with LO's yes, batch 5** (backup: `first_term_snapshots/20261008_narration_ledger_before/`):

| # | change |
|---|---|
| 23 | top-level `"narration_person": "second"` |

**Written 2026-10-08, batch 5** (backup: `first_term_snapshots/20261008_money_feeds_before/`):

| # | change |
|---|---|
| 25 | `money_pressure.feeds`: `laura_suspicion` dropped |

**Not a ledger change:** the ledger keeps no "entered from" per place. The sheets take it from the map's
shape line, and the build writes it as `entry_from`.

## Rows a gate needs (S6)

Nothing on these sheets is deferred. These rows hold up a gate:

| row | sheet | gate |
|---|---|---|
| the map: street is the only root | this one | the map is a place · world reachable |
| homes for every resident | this one | residents have homes |
| the kitchen at 25.3% | this one | location fill |
| energy locks a shift, Focus and the party | this one, college, job, parties | a need shuts a door |
| a bed, every day | this one | a need can be met every day |
| rent $75, Sunday, carried when short | money and rent | the obligation is charged · money gates something |
| shop prices on the label | wardrobe | a price is on its label · one currency |
| Gary's $20, half to Tom | job | sex for pay names the amount · her climb |
| six cards, each filled | all six system sheets | every system has a card (blocks a ship) |
| each card leads to a person | all six | leads to a person or a sex scene (blocks a ship) |
| seven states and the key items, read three times | wardrobe | every clothing state is read three times (blocks a ship) |
| `sports_bra` sold at the shop | wardrobe, park | a declared garment can be got |
| every meter has a reader in 0.1 | college, park, parties | a meter is read |
| the door repeats | this one | ends on an opening · the door can be seen again |
| no topic unknown | coverage | no unknown topic |

**At risk now:** `laura_suspicion` (readers on Laura's sheet). `followers` and `campus_talk` get 0.1 readers on the
place sheets (question 17). **Traversal heat** is a report row, not a ship block; question 13 raises it.

## Why — the source of each key choice

| key choice | source |
|---|---|
| nested zones, street as the ground | `the-map.md` R0, R3 · the board, 2026-10-08 |
| Vance sleeps at his house | LO, 2026-10-08 (LIVES.md:261) |
| who climbs: both | SP2 · `the-meters.md` W1 |
| stage edges 20/40/60/80 | LO, 2026-10-08 (SP2 §1) |
| every money number | LO, 2026-10-07 (SP4) |
| energy is a lock, hygiene colour only | LO, chat 2026-10-06 (SYSTEMS §5–6) |
| the anchor at 25% | `the-release.md` § The first release |
| Tom to step 6 | LO, 2026-10-08 (SP7) |
| the door | LO, 2026-10-07 (SP7) |
| the park couple as the first explicit beat | LO, 2026-10-08 · `the-arc.md` A15 |
| Zoe in the park at weekend mornings | LO, 2026-10-08 (08:00–10:00 is a guess) |
| a pool canvas for each Bold act | LO, 2026-10-08 |
| the eleven answers | LO, 2026-10-08 |
| questions 12–17 | LO, 2026-10-08 |
| questions 18–22 | LO, 2026-10-08 |
| questions 23–27 | LO, 2026-10-08 |
| questions 28–30 | LO, 2026-10-08 |
| questions 31–32 | LO, 2026-10-08 |
| questions 33–34 | LO, 2026-10-08 |
| questions 35, 38 | LO, 2026-10-08 |
| the seen_from rule | `gates.py:12998-13020` |
| `narration_person` | `state.md` schema · engine default `second` |
| the engine takes the first matching row | `v2.py:4304-4318` |
