# Parked — 2026-09-19

**Audience: the agent. Not a sheet.** Nothing in this folder is in the game. `scripts/merge_toml_phases.py`
merges a fixed list of files from `toml_phases/`, and this folder is not one of them.

## Why

LO: *"yes, lets park them"* · *"go ahead take them out."* Between the content-complete build (`273f5ec`,
2026-09-15) and 2026-09-18 the game took 24 commits and no design round. `sheets/BASE.md` now decides the
game block by block, and the base can't be decided while scenes built ahead of it are live and arguing
for their own rows. Everything here was built from something LO asked for **in chat** — the ledger
decision in each row below quotes him — and none of it was designed on a sheet first.

## The rule for bringing anything back

**Nothing comes back by default.** Each item returns only when the round for its block in
`sheets/BASE.md` decides it, and then it is taken from here if it fits, rewritten if it half-fits, and
left here if it doesn't. Every canvas below is copied verbatim from `ff91336`, design comments included,
and was checked equal to the built canvas before removal.

## What's here

| file | scenes | from | ledger | block in BASE.md |
|---|---|---|---|---|
| `cards_front_room_and_tasha_room.toml` | `hub_nate_sofa`, `hub_tasha_room` · `sofa_hour` · `nate_sits_down` | `63df046` | 102 | 2 cards · *her alone* · 4 walking in |
| `tasha_ladder.toml` | `arc_tasha_01..03`, `loop_tasha_bath`, `hub_tasha_bath` · `owen_at_the_board` | `86cc9f1` | 103 | 5 Tasha's ladder · 4 walking in |
| ~~`gil_kitchen_card.toml`~~ | `hub_gil_kitchen` | `cd677e8` | 105 | **CONSUMED 2026-09-23 → `sheets/people/gil_cards.md`** |
| `stream_at_work.toml` | `stream_toilet` | `3233846` | 106 | 5 a going-live ladder |
| `television.toml` | `watch_tv` · `hub_gil_sofa`, `hub_lynn_sofa` | `0e829a1` | 108 | *her alone* · 2 cards |
| `garage_and_nate.toml` | `garage_gil`, `garage_nate`, `hub_nate_room`, `kitchen_nate` | `6801814` | 109 | 2 cards |
| `bathroom_door.toml` | `bath_break`, `bath_knock`, `bath_gil`, `bath_lynn`, `bath_nate`, `bath_tasha`, `nate_walks_in` | `972a27b` | 110 | 4 walking in |
| `house_happens_to_her.toml` | `tasha_caught` · `hub_gil_bed`, `hub_lynn_bed` | `2591a11` | 111 | 3 random events · 2 cards |
| `kitchen_and_her_mum.toml` | `cook`, `kettle` · `cook_with_mum`, `chores_with_mum`, `hub_lynn_kitchen`, `hub_tasha_kitchen` | `19fee19` | 112 | *her alone* · 2 cards |
| `as_built.toml` | `nate_door`, `master_bedroom`, `wash`, `dinner`, `friday_payment`, `the_schedule`, `tasha_walks_in` | many | 103–112 | the passes' versions of founding scenes |

***her alone*** is not a block yet. `BASE.md`'s map has nowhere for what she does on her own — cook, the
kettle, the television, the sofa hour — and that gap was put to LO on 2026-09-19, unanswered.

**`as_built.toml` is salvage only.** The build carries those seven scenes as they were at `63df046`,
with every prose fix. These are the versions the house passes left: `nate_door` as a dice roll with
three bands on @nate's arousal and two on her corruption, `master_bedroom` as a dice roll, `wash` with
the bathroom-lock substitutions, `dinner` reading `door_noticed`, and so on.

## What left with them and is not copied here

Pointers, not copies — take them from git when a round needs them.

- **Schedule rows.** 22 rows added and 7 changed, by six passes. The build is back to the founding 23 plus
  Owen's office row. Every row with the pass that made it: `git show ff91336:games/the_balance/toml_phases/1_metadata_and_locations.toml`.
- **Flags and counters** only these scenes used, and their resets in `[engine.daily_tick]`:
  `git show ff91336:games/the_balance/toml_phases/0_systems_spec.toml`.
- **The bathroom door's four "Open it anyway." options** on the location, and **the gym location** —
  `sheets/RELEASE.md` lists the gym under *"What waits"*: same `1_metadata_and_locations.toml` at `ff91336`.
- **`door_noticed`**, her door's tally of shutting it on a full house. `her_door` is kept, the tally is not.
- **Four walk routes**: `kitchen`, `afternoon`, `bathroom`, `ambients` — kept in `process/walks.py` under
  `PARKED_ROUTES`, not run by default. The lock route's full-house half is at `ff91336` in the same file.
- **Nine `presence.py` exemptions** for parked rows. Their written reasons are at `ff91336` in that file.

## The writing about it — parked the same day

LO: *"Go ahead takes the yes one out."* Once the scenes were out, the pages still described them. Taken
out too, as **whole-file copies of the versions that are gone** — not diffs:

| file here | what it is | the live file now |
|---|---|---|
| `sheets_as_built/people/the_cast.md` | +22 · Nate's age and year, the house roles | `sheets/people/the_cast.md` at `273f5ec` |
| `sheets_as_built/places/the_house.md` | +24 · the two kinds of work, cooking | `sheets/places/the_house.md` at `273f5ec` |
| `sheets_as_built/systems/the_house_day.md` | +232 · sleep, the television, her door, the week | `sheets/systems/the_house_day.md` at `273f5ec` |
| `sheets_as_built/systems/the_phone.md` | +20 · Go Live, the work toilet | `sheets/systems/the_phone.md` at `273f5ec` |
| `sheets_as_built/systems/the_week.md` | +1 · Nate "the year above" | `sheets/systems/the_week.md` at `273f5ec` |
| `sheets_as_built/systems/walking_in.md` | +16 · three doors on dice at home | `sheets/systems/walking_in.md` at `273f5ec` |
| `DECISIONS_as_built.md` | +117 · her mum's television and bathroom amendments, Gil out of the van | `DECISIONS.md` at `273f5ec` |

Lines added to the pages as they stood at `ff91336`: **315**. The 328 quoted elsewhere counts every
commit's additions, including lines a later pass rewrote.

⚠️ **One seam this leaves, on purpose.** The game keeps the role-label fix (`f1b2d59`), so @nate's
description in the build reads *"a year ahead of you at the same college"* while the restored cast
page reads *"a senior at her college"*. Round 3 of `sheets/BASE.md` (the household) settles which.

**Nothing in this folder is citable** under `process/README.md` §0a. It is what was built, not what LO decided.

---

## What block 2 took back for @gil — 2026-09-23

`sheets/people/gil_cards.md` is the round this folder's rule was waiting for: *"taken from here if
it fits, rewritten if it half-fits, and left here if it doesn't."* All five of his canvases were
read; three came back rewritten and two stayed.

| canvas | file | what happened |
|---|---|---|
| `hub_gil_kitchen` | `gil_kitchen_card.toml` | **back, rewritten.** The `requires_npc` shape, the two time bands and the `gil_today` cap all carried. Cut: every line naming the fridge list (gone since 2026-09-23) and the `relation >= 10` choice *"Ask what the semester actually cost"*, which is a climb. Retimed — the front room has his 06:45 hour now. |
| `garage_gil` | `garage_and_nate.toml` | **back, rewritten.** Its 17:00-18:00 window was from a week he no longer has; it now covers all four garage rows on `requires_npc` alone, and it is where the lift is bought. |
| `hub_gil_bed` | `house_happens_to_her.toml` | **back, rewritten.** Its ward-night 21:00-23:30 hours are dead — he is in the garage then. It is the *asleep* card now, on three schedules. |
| `hub_gil_sofa` | `television.toml` | **stays.** Evening front room. The page rules he does not sit there in the evening: he sits there at quarter to seven in the morning, and that is a different card. |
| `bath_gil` | `bathroom_door.toml` | **stays.** Three rungs on a walk-in. He has a bathroom row now, at 23:00, and the door is **locked** — the ladder behind it is block 5. |

⚠️ **His schedule rows did NOT come from here.** They are generated from `GIL_ROWS` in
`process/gen_week.py`, which is where round 3 put them and where block 2 changed them.

## What stayed, and why

- **The 43 founding scenes**, at `63df046`, with every prose fix.
- **Bus and walk** (6). `the_week.md`: *"The bus is forty minutes and $2 each way. Walking is free and takes an hour."*
- **`her_door`**. `RELEASE.md`: *"going live in her room with the door shut."*
- **Owen's office row**, 21:00–22:00. Without it `office_closer` never renders, `owen_standing` never
  moves, and `move_up_counter` never opens — the ending on `RELEASE.md` can't be reached. Probed live
  after the park: 7/7.
- **The Go Live launcher**, her room only. **Cara's messages.** The engine, and every sheet.

---

## The climbs — parked the same day

LO, after reading how Jules's dares and the cafe job climb: *"So they shouldn't climb. We are talking
about base here. Not more than that."* Then: *"Go ahead park all the climb."*

`sheets/BASE.md`'s own test decides what goes: *"If it changes because of what she's done, it belongs to
a ladder."* **This is different from the first park.** That one took out work nobody designed. This one
takes out work that **was** designed, on LO's signed pages: `RELEASE.md`, `the_dares.md`,
`the_move_up.md`, `the_cafe.md`, `the_two_doors.md` and `the_phone.md`. It's block 5, the ladders, and
it's parked so that the base can be decided without it pulling the rows. **Those pages are still the
citation** when a ladder brings it back. The TOML here is how it was built, not a new decision.

### The line

**Out (a climb):** anything that reads or moves a progress meter, or is a step in a chain. A chain's
first step goes too: dare one, "Take your top off.", @nate's door, the first customer.

- her three meters, `exposure` · `corruption` · `reputation`, and `followers`
- the cafe: `shifts_worked` · `owen_standing` · `move_up` · `cust_hand_done`
- the dares: `dare_chain` · `dare_cooldown` · `dare_1_pending` · `jacket_off` · `quiet_week` · `crowd_standing`
- going live: `stream_top_done` · `stream_naked_done` · `stream_touch_done`
- the doors: `nate_seen` · `nate_landing` · `saw_them`
- **every NPC `relation` and `arousal` write.** With Cara's later messages parked, nothing read them.

**Stays (base systems, not climbs):**
- needs: `rest`, `clean`
- money: `cash`, `debt_left`, the Friday $150, the chore, the bus
- attendance: `attend_1..4`
- Gil's rules: `home_after_ten`, `fridays_missed`
- the job itself: `has_job`
- the day caps and `door_locked`

`exposure`, `corruption` and `reputation` (with their sidebar words) and `followers` (with its visible
count) stay **declared**, but nothing moves them.

**A base scene that read a climb keeps exactly what a fresh save sees**, and nothing else. No prose was
written. **No schedule row moved.**

### What's here

| file in `climbs/` | what |
|---|---|
| `cafe.toml` | `shift_counter`, `cust_hand`, `cust_showing`, `office_closer`, `move_up_counter` |
| `dares.toml` | `dare_1_offer`, `dare_1_do`, `dare_2_offer` |
| `house_doors.toml` | `nate_door`, `master_bedroom`, `master_caught` |
| `cara_thread.toml` | `cara_rumour`, `cara_coffee`, `cara_cool`, `cara_last`: each is gated on her relation or on exposure |
| `systems.toml` | eight counters' declarations and labels, three `[engine.daily_tick]` pieces, the three dare quest cards. Not loadable as one file: each piece goes back into the table named above it |
| `before_the_strip.toml` | **the 25 base scenes and messages that had a climb cut out, whole, as they stood before the cut**: the stream, the floor shift, the board, Friday, the four picking-on ambients, the three listening scenes, the classroom door, Paige, Bree ×2, dinner, the opening, asking for the job, Cara ×2 at the union, Sam ×2, Tasha walking in, and Cara's first two messages |

Every canvas and message in these files was checked equal to the built one before it came out.

### What the base scenes lost

| scene | cut |
|---|---|
| `stream` | the three rungs and their nodes · followers, exposure, corruption · the 500 and 2,000 pay bands (the $8–25 band stays) · the landing week's line and lock |
| `shift_floor` | both customer swaps · `shifts_worked +1` · `move_up lt 2` |
| `canvas_ask_owen` | `move_up set 1` |
| `the_schedule` | the counter version of the board · the locked closing-shift choice |
| `friday_payment` | "Ask him for a bit more time." and its node |
| `picked_quad` / `_union` / `_lecture` / `_stop` | the `quiet_week` switch · the jacket and exposure 20/40 versions · "Say something back." |
| `listen_union` / `_quad` / `_before` | the exposure 15/40 versions |
| `classroom_door` | "Stay and watch properly." · "Let them see you there." · their nodes and `after` · corruption on the freeze |
| `paige_is_nice`, `bree_takes_it_home` | the after-a-dare lines · the crowd_standing / reputation choices |
| `bree_catches` | "Go over." |
| `dinner` | @nate's landing line |
| relation writes | the opening, Friday, dinner, Tasha walking in, Cara and Sam at the union, Sam in class, Cara catching her, Paige, Cara's first two messages |

### What this leaves, on purpose

- **No ending.** The closing shift was the last step of the cafe climb.
- **One explicit beat**, the classroom door's first screen.
- **Owen's office row stays and is DEAD.** Its only reason was `office_closer`; rows are block 1, and
  round 4 of `BASE.md` decides it. The "What stayed" entry above predates this.
- **Jules has no card.** Her rows stay, and `presence.py` lists them.
- **Cara's messages:** the first two stay (the opening, the job), without relation.
- `presence.py` now reports 13 DEAD rows. `walks.py` has five more `PARKED_ROUTES`: `cafe_climb`,
  `stream_climb`, `doors`, `dares`, `cara_thread`.
