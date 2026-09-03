# DECISIONS — Vesper: Undertow  `[READY]`

> **GENERATED from `v2_state.json` by `scripts/render_decisions.py`. Do not edit by hand.**
> `the-sheets.md` S7 — the decision sheet and the ledger are one document written twice, so
> here they are one document generated twice. Edit the ledger, re-run the script.
> As of 2026-09-03 · phase `sheets`.

## The map — THIS IS THE PART THAT NEEDS YOUR SIGNATURE

**Shape.** One street at ground level. Three districts hang off it: the Spire uphill behind glass, the Waterfront along the dock road, and the Reach down under it. Everything else is a room inside one of those three.

- archetype `nested_zones` · exterior **`the_street`** (a ROOT — nothing is its parent)
- home base `kess_berth`

| character | sleeps at |
|---|---|
| npc_mercer | `mercer_room` |
| npc_kess | `kess_berth` |
| npc_bastien | `bastien_backroom` |
| npc_renner | `offscreen` |
| npc_calloway | `offscreen` |
| npc_colm | `offscreen` |
| npc_marsh | `offscreen` |

- bridges: `the_street` → `spire_plaza` (20m) · `the_street` → `the_waterfront` (20m) · `the_street` → `underworld_strip` (20m)

**`r1_signoff`:** SIGNED by LO, 2026-09-03. Drawn by ENI the same day; the-map.md is explicit that the author of a map cannot sign it, so this waited for him. He read the shape sentence, the exterior root and the three zone grounds, and signed.

> `the-map.md`: *"A sign-off written by the author of the map is not a sign-off."*
> The one question it has to answer: **could someone who has never seen the game draw
> this place from the graph?** That is the half gate 28 cannot see.

## Blocked by reversibility

### A · locked forever once v0.1 ships

- `narration_person` = **second** — changing it rewrites every line
- the story title **Vesper: Undertow** — in-browser saves namespace off `Util.slugify(title)`
- every canvas id, flag key, trait key and stat scale — renaming one strands every save

### B · expensive

- the map shape (`nested_zones`) and which room is the anchor
- the cast (7 people) — media is keyed to them
- which systems exist, and which are `sourced`

### C · cheap

- every number: rung spacing, fill budgets, prices, decay rates
- all prose, all media, every display name

## The board, as the gates read it

**`who_climbs`** = `both` — gate 34 wants ≥60% of meter-gating on her own tiers.

### Ascent tiers

| tier | ceiling |
|---|---|
| `cover` | 100 |
| `service` | 100 |
| `drain` | 100 |

### Systems

| system | kind | key | fed at | labels |
|---|---|---|---|---|
| `seated` | sourced | `seated` | `kess_berth` | `has_bench` |
| `cover` | sourced | `cover` | `kess_berth` | `checks_cover`, `outdoors` |
| `service` | ambient | `service` | `underworld_bar`, `bastien_backroom`, `underworld_brothel`, `mercer_room`, `penthouse`, `renner_depot`, `vance_securities` | `private`, `she_can_undress` |
| `drain` | ambient | `drain` | — | — |
| `charge` | ambient | `charge` | `kess_berth` | `home_base` |
| `clean` | ambient | `clean` | `underworld_bar_bathroom`, `kess_berth` | `she_can_undress` |
| `coin` | ambient | `coin` | `underworld_bar` | — |
| `arousal` | ambient | `arousal` | — | — |

### Locations

`[INTENT]` **14 locations · 29,600 words budgeted · anchor `underworld_bar` at 30.4%** (floor 25%). Every figure below is a BUDGET written before the prose, not a count of prose that exists — gate 1 refuses to credit a set that is mostly non-round.

| location | fill |  | heat | labels | job |
|---|---|---|---|---|---|
| `the_street` | 600 |  | cold | `outdoors`, `public` | The ground the three districts sit on. Everything she walks between, she walks here. |
| `spire_plaza` | 800 |  | cold | `outdoors`, `public`, `zone:spire`, `checks_cover` | The glass front of the company. Where the cover gets tested before she is even inside. |
| `vance_securities` | 1500 |  | yes | `private`, `zone:spire`, `checks_cover` | Calloway's file room, being audited shut. The one place her own file might be. |
| `penthouse` | 2000 |  | yes | `private`, `zone:spire`, `checks_cover`, `she_can_undress` | Mercer's floor. She is furniture here and it is the softest bed in the game. |
| `the_waterfront` | 800 |  | cold | `outdoors`, `public`, `zone:waterfront` | The dock road. The Spire is behind you and the Reach is below. |
| `renner_depot` | 2500 |  | yes | `private`, `zone:waterfront` | Renner's gutted supply yard. He hires cheap hands and does not look up. |
| `underworld_strip` | 1000 |  | yes | `outdoors`, `public`, `zone:reach` | The Reach's open row. Nobody here cares what she is. |
| `underworld_bar` | 9000 | **ANCHOR** | yes | `public`, `zone:reach`, `checks_cover` | The floor she works. Where men come to her instead of the other way round. |
| `underworld_bar_bathroom` | 600 |  | yes | `private`, `zone:reach`, `she_can_undress` | Two sinks and a lock that does not. Where she gets clean enough to go back out. |
| `bastien_backroom` | 2500 |  | yes | `private`, `zone:reach`, `she_can_undress` | Behind his own bar. He strips her at the door every time, and he is not looking for a weapon. |
| `underworld_brothel` | 2500 |  | yes | `private`, `zone:reach`, `she_can_undress` | The House. A booked hour, and Sunday belongs to Marsh. |
| `kess_berth` | 3000 |  | yes | `private`, `zone:reach`, `home_base`, `has_bench`, `she_can_undress` | His bench, her charger, her bed. The only place anything gets put inside her on purpose. |
| `mercer_room` | 2500 |  | yes | `private`, `zone:reach`, `she_can_undress` | The stall he runs under a flat new name. He is delighted every single time. |
| `cain_lab` | 300 |  | cold | `zone:reach` | Dark, and the door does not open. The company says he is what she is for. |

### Characters

| character | surfaces | sched rows | meters | why she wants them |
|---|---|---|---|---|
| `npc_mercer` | 2 | 2 | `relation` | He owns her and it costs him nothing. The top of the leash and the last door. |
| `npc_renner` | 2 | 1 | `relation` | Cold, mean, clawing at a gutted business. He ignores her and then he cannot. |
| `npc_bastien` | 2 | 1 | `relation` | He caught her, he strips her at the door, and his lever is curiosity rather than desire. |
| `npc_calloway` | 2 | 1 | `relation` | Starving to be believed. She takes his hunt seriously and that is the whole seduction. |
| `npc_colm` | 2 | 1 | `relation` | Cold and fast and nothing else. The rung where the act stops being an event. Carries the informant function cut with Sol: bring him a name off the floor and he knows who ran it. |
| `npc_marsh` | 1 | 1 | `relation` | He pays and does not care whose body is in the slot. The first time she chooses a mark. Carries the slot obstacle cut with Rue: the Sunday hour is bought off someone, and the coin is the obstacle. |
| `npc_kess` | 2 | 1 | `relation` | He reads bodies as hardware and hers as an interesting problem. Landlord, charge and repair. |

### Needs

| need | falls | fills | costs | shuts (gate 29 reads this) |
|---|---|---|---|---|
| `charge` | 20 a day | kess_berth · a night on the feed line · to 100 | 10 coin a night, paid to Kess | **under 30 no drain fires and every act rung that costs charge stops rendering** |
| `clean` | 30 per finish, 10 a day | underworld_bar_bathroom · Wash · 20 min · free · or the berth | free at the bathroom; a berth night covers it | **under 40 the cover doors at spire_plaza, vance_securities and penthouse refuse her, and the bar floor pays half** |

### Economy

- currency `coin` · written as **coin** · `[settings.rent] currency_symbol` must match
- obligation: The feed line — 10 coin a night, paid to Kess at the berth, which is also the only thing that refills her charge. Seventy across a week.
- `[INTENT]` **10 per charge** against `week_income` **210**
- it MOVES: Kess raises the nightly rate as he seats more in her — the more he has put inside her, the more a night on the line costs. The demand rides the `seated` system rather than a second mechanic.
- sinks: the feed line · cover garments · Kess's parts and repairs · the toll at the Reach gate · buying Sunday's slot off the girl who holds it

## Guidance — one card per tier (S10)

`quests_engine = "v2"` lights a sidebar entry and a page, and with no cards it renders a heading and nothing. No sheet in the format mentioned a quest card; nine were written from scratch after the first gate run on the game this format came from. Lostness is the genre's dominant complaint at a **4.7% median share** of player comments against grind's 0.9%.

| card | canvas | says |
|---|---|---|
| `cover` | `TBD` — written in pass D | names a place and an hour, never a number |
| `service` | `TBD` — written in pass D | names a place and an hour, never a number |
| `drain` | `TBD` — written in pass D | names a place and an hour, never a number |
| the obligation | `TBD` — written in pass D | when it is due and who takes it |

## Gate reconciliation (S6)

> *"Nothing a gate requires may be deferred by a sheet."* The incident: a bathroom sheet said *"not authored this release, named here so it is not forgotten"* — honest, deliberate, signed off, and `the walk-in floor` is a GATE, which then failed 0/5. **A deferral is not a pass.**

`[INTENT]` **48 of 49 gates have their sheet on disk** (1 n/a). Every `NOT YET` below is a KNOWN red, never a silent one. The column is computed from the filesystem, so this table cannot claim a sheet that has not been written.

| gate | discharged by | sheet on disk? |
|---|---|---|
| `location fill` | places/* | yes |
| `explicit floor` | scenes/* | yes |
| `explicit in repeatable` | scenes/* | yes |
| `repeatable explicit media cycles` | places/* | yes |
| `an explicit beat carries a clip` | scenes/* | yes |
| `somebody speaks` | scenes/* | yes |
| `traversal heat` | places/* | yes |
| `standing surface` | people/* | yes |
| `milestones open something` | people/* | yes |
| `meter ceiling` | DECISIONS | yes |
| `ends on an opening` | DECISIONS | yes |
| `ascent tiers expand the world` | systems/cover,service,drain | yes |
| `world reachable` | DECISIONS | yes |
| `every authored node is reachable` | scenes/* | yes |
| `residents have homes` | DECISIONS | yes |
| `guidance exists` | DECISIONS | yes |
| `no chain ends in silence` | people/* | yes |
| `money gates something` | systems/coin | yes |
| `sinks >= sources` | systems/coin | yes |
| `no free uncapped income` | systems/coin | yes |
| `a price is on its label` | places/* | yes |
| `the price is in one currency` | DECISIONS | yes |
| `a place is not a catalogue` | places/* | yes |
| `the obligation is charged` | systems/charge | yes |
| `effects use a live op` | FORMAT | yes |
| `a day-cap closes` | places/* | yes |
| `a spent day still has a door` | places/* | yes |
| `the climb is paid for` | systems/cover,service,drain | yes |
| `a banded meter is not also a number` | DECISIONS | yes |
| `the map is a place` | DECISIONS | yes |
| `a need shuts a door` | systems/charge,clean | yes |
| `the walk-in floor` | places/* | yes |
| `a meter is read` | systems/* | yes |
| `the wardrobe is read` | systems/cover | yes |
| `a declared garment can be got` | systems/cover | yes |
| `a locked door says why` | places/* | yes |
| `the climb is where you said it is` | DECISIONS | yes |
| `the start choice is read` | OPENING | yes |
| `what money buys opens a door` | systems/coin | yes |
| `she can say no` | people/* | yes |
| `what she picks is read` | n/a -- no customization declared | n/a |
| `speakers are named` | scenes/* | yes |
| `sentence length` | scenes/* | yes |
| `prose texture` | scenes/* | yes |
| `the opening opens a door` | OPENING | yes |
| `every hub is met first` | OPENING | yes |
| `a meeting fires where they are` | people/* | yes |
| `no canvas key is discarded` | FORMAT | yes |
| `the label keeps its time` | places/* | yes |

## Decisions log

- **0.1** — The ascent is INVERTED from the shipped game's. games/vesper declared her axis as 'the awakening: chip fragments + the accumulating glitch-dread' (design_book.md:595) and started her pre-maxed — 'she starts at the bottom of herself' (:563). That is a plot ladder, and it produced the whole failure set on gates.py vesper (17 PASS / 22 FAIL / 11 n/a): explicit floor 4.3%, heat sealed one-time in captive_room, ascent tiers reading case_progress / names_known, and 17 of 18 gated meters raisable for free because there was no climb to brake. WHAT REPLACES IT: three access tiers — cover, service, drain — each already media-complete on disk. The cost is that Wren no longer starts at her sexual ceiling, so the shipped game's captivity material has no home here.
- **0.1** — Cast cut from 17 to 8, driven by media already paid for. KEPT: Mercer (16 act pools), Renner (9, and the only graded on-ramp on disk — tease_t2 / flash_t3 / grope_t4), Bastien (8), Marsh (7), Calloway (7), Colm (7), Kess (no acts; he is the obligation's collector), Cain (no acts; the locked door). CUT: Sol, Rue, Vane, Enns, Voss, Reyes, Marr, Grier, Sabin. Grier and Sabin have neither face nor acts and would start from zero media. The cost is that Sol's informant function and Rue's brothel-slot obstacle both need re-homing if the Undertow keeps its shape.
- **0.1** — Story title is 'Vesper: Undertow', NOT 'Vesper'. In-browser save slots namespace off Util.slugify(title) (the-returning-player.md:129, engine.md:2338), so an identical title would collide with the live vesper v0.2.0 in a returning player's browser. Exported .save files survive a title change; in-browser slots do not.
- **0.1** — definition = 'written' chosen AGAINST the field, which runs 19 blank to 10 written with blank holding 80.4% of top-30 engagement (the-want.md:58). Reason: eight Wren portrait states, six complete act ladders and a wardrobe are already keyed to a named woman. What blank buys is bought instead by the start choice — past_field / past_house / past_floor, read as bands on the standing surfaces rather than as a stat screen.
- **0.1** — OPEN — 'grays' (the company uniform) is flagged by gates.py --words as a noun none of the 27 field games use. It is already on disk as videos/clothing/company_grays.jpg, so it is no longer a soft noun; renaming costs a media rename. Recorded rather than silently kept. Decide before the board phase names garments.
- **0.1** — Charge channel: the feed line is a `costs` entry on the berth rung, NOT `[settings.rent]`. `due_day` takes weekday names only and the demand arms at 00:00 on that day (engine.md 26, v2.py:5615), so the engine's system is weekly and cannot express a nightly charge. obligation_amount is therefore declared as 10 — the amount ONE charge takes, which is what gate 24 compares against the largest authored outflow (gates.py:5901) — with the weekly 70 carried in the obligation prose. ONE channel only: no authored canvas narrates a payment the engine is making, because the measured failure shipped both and the free duplicate was the one with the writing in it.
- **0.1** — board.systems was missing `service` and `drain`. Both are declared ascent tiers, and the-systems.md:39 is explicit that a meter is one kind of system — so a tier absent from board.systems is a thing the game keeps track of that the systems list does not know about. Found while writing the system sheets, which is what the sheets phase is for. Both declared `ambient`: they are fed at every act surface, which is most rooms. Ambient-fed is not thinly-read — DoL raises promiscuity in 22 places and gates on it in 206.
- **0.1** — Mercer holds TWO rooms and the first draft made them contradictory: the penthouse sheet had him owning a Spire floor 08:00-23:00 while the stall sheet had him 'blown and hiding under a flat new name'. Those are two states of the same character from the shipped game's timeline, declared as simultaneous. Resolved: he is not hiding, he is SLIDING — the penthouse by day because his position still just holds, the stall by night because it does not. Found by writing his arc, not by reading the place sheets, which is the sheets phase working as intended.
- **0.1** — kess_berth's 'The wardrobe.' row was DELETED. Declaring wardrobe_location renders [[Change Clothes->WardrobePage]] on that location's screen unconditionally (v2.py:9814), above the portrait row, on every visit. An authored canvas beside it is a second door and is the one that does not work — orientation shipped exactly that. The room now has 3 rows, which is the field median.
- **0.1** — `grays` CLOSED — LO's call 2026-09-03: it stays. gates.py --words flags it as a noun none of the 27 field games use, and it was logged as open because videos/clothing/company_grays.jpg already exists so a rename would cost a media rename. LO kept the noun; no rename, and the lint entry is now an accepted cost rather than an open question.
- **0.1** — board.who_climbs corrected `player` -> `both`. It was declared in the board phase before a single arc existed, and gate 34 now measures 19 gate sites on the declared tiers against 18 on per-character meters — 49%, against the 60% a `player` declaration wants. That split is not a defect: every arc in this game is spined on `relation`, and the three tiers are the floor under them. the-meters.md W1 describes `both` as exactly that — 'a player tier as the FLOOR under per-character arcs' — and asks for >=25% each. The declaration was wrong, not the content.

## Promises outstanding

- Cain — named, seen once and unreachable. v0.1 closes on his door. *(made 0.1, unpaid)*
