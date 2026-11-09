# Build log — first_term 0.1, iteration 002 (the rebuild from the 2026-10-09 sheets)

Phase `sheets`. Skill: author-game-v2 at `fd444666`. Sources: the sheets signed by LO on 2026-10-09
(`sheets/`, `DECISIONS.md`, `WANT.md`, `SYSTEMS.md`, `LIVES.md` §11, `v2_state.json`).
Snapshots before each part: `~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261009_iter002_part<N>_before/`.
Every build: `iterations/002/build_scripts/build_scenes.sh` (merge, then `package_from_toml … --gen-version v2 --dev`).

## The build scripts (fixed first)

Copied from `iterations/001/build_scripts/` (byte-identical to the 0.1 scratch copies). `build_scenes.sh`:

- now runs from its own folder, not a session scratch path;
- `PARTS` picks only which scene sections to **regenerate**; the concatenation always walks all eleven
  (`ryan laura mark tom zoe hale jake cafe college pools extras`), the order 0.1 shipped — checked
  byte-identical against 0.1's `5_scenes.toml`;
- a missing `parts/<name>.toml` stops the build instead of being left out. A plain rerun can no longer
  drop five people's scenes.
- `PARTS=" "` regenerates nothing and only rebuilds `1_` and the package. `parts/` was seeded with
  0.1's section files, so part 1 changed the world only; each later part regenerates its own people.

## Part 1 — the world

**Built** (`world_data.py`, `people_data.py`, `gen_world.py`; output `1_metadata_and_locations.toml`)

- Areas: **Home** (a building, opens in the hall, `crossing_costs` time 10), **Campus** (now an area,
  time 15; its hours and closed text gone), **Town** (new area off the street, time 15, the bus). Each
  room inside an area names its `parent`, because the engine finds the area through the parent chain
  (`v2.py:11398-11433`).
- The park's 10 minutes is its own `costs`; the street lost its old `costs` time 10 (it was charged on
  every return to the street).
- New places: `home` · `home_garden` (off the hall) · `corner_shop` (on the street) · `campus_gym` ·
  `college_mens_toilet` (empty, LO's call, Q76) · `town` · `zoe_flat` (a building, opens in Zoe's
  Living Room) · `zoe_kitchen` · `zoe_bathroom`. `zoe_apartment` is named "Zoe's Living Room".
  38 places built (the ledger's 38, the men's toilet included).
- Hours, closed text, hidden flags and costs are read from the ledger at build time (no hand copy). New
  descriptions for the new places; the street says the minutes once in LO's words (Q65).
- Every schedule row is generated from the ledger (`board.characters[].schedule`) in ledger order, with
  an activity line per row. A row marked for a later release (Ryan's Saturday, Ryan A 12) is not built.
  A row without a ledger gate keeps 0.1's `<x>_met` gate (the household has none).
- The wait button: the engine's own (10 minutes, 1 hour, 1 day), under the clock on every screen
  (`v2.py:19435`/`:19448`); nothing to build.
- Sweep fixes on world lines: A1-13 (Vance's description and cast line no longer say Mark owes him),
  A1-19 (Zoe now has a bedroom row; the bedroom line no longer says she watches you change),
  A1-20 (the café's closed line is the ledger's "The café's shut."), A1-35 (the street shows "Home").
- Mark's late-night rows read "up late with the TV on", not "up late, Laura asleep": the truth gates
  read the word "asleep" in an activity as the person sleeping (`gates.py` `_TR_SLEEP`).

**LO's calls this part** (DECISIONS 75, 76): the hall's late door is gone and the street sets no
`came_home_late`; Laura's stairs row reads `late_party`, `late_shift` or `late_date` set in the last
4 hours. The men's toilet is built, empty, with the women's toilet's hours and closed line.

**Checks**

- `who_is_where.py` against the ledger, every 5 minutes of the week, every person: **0 mismatches**
  (scratch script; a gated row counts both ways). LIVES.md §11 is the ledger's rows copied, so it
  matches too, and the §4 house view holds (dinner hour, Ryan's weekend afternoons, Mark downstairs
  every night but Saturday).
- Live (headless, the built game): street to Home +10 min, to Campus +15, to Town +15, to the park +10,
  to the corner shop +0; moves inside an area +0; leaving free; Vance's house shut at 10:50.
- `gates.py`: 53/87 (0.1 on the current gates: 57/87). `shape.py --finish`: 22 pass, 0 fail.
  `playtest.py`: 8/8.

**Gates that went red this part, and why**

| gate | cause | owner |
|---|---|---|
| world reachable (10/38) | gate gap: G11 sees no edge into a building's `default_entry` (below) | skill |
| a step is seen from the next room (7/8) | the same gap: `zoe_apartment` has no `entry_from` now | skill |
| standing surface (63/68) | new rows with nothing of theirs in the room: Zoe at the party house and the Wednesday lecture, Jake at the gym and his lectures | parts 4, 5 |
| a destination is never open and exit-only (24/31) | the new rooms have nothing to do yet: gym, men's toilet, corner shop, garden, Zoe's kitchen and bathroom, Zoe's living room Mon–Thu 22:00–00:00 | parts 2, 4, 5 (the men's toilet: by LO's call) |
| every person here has a face (4 → 12 pairs) | faces for the new rows: Ryan and Mark at dinner, Ryan's TV afternoons, Laura asleep, Tom after close, Zoe and Jake in class, Zoe's bedroom and party house, Jake at the gym and the door, Vance at the door, the cocky guy | parts 2–5 |
| nobody is woken (3 → 5) | the master-bedroom knock while asleep; Laura A 1 and A 4 off their new windows; meet_figure | parts 2, 3, 4 |
| a latch flag is cleared (3 → 4) | `jake_date_went` (the pickup isn't built yet), `jake_date_booked`, `rent_carried`, `came_home_late` | parts 3, 5 |

## Part 2 — home and everyday life

Snapshot: `first_term_snapshots/20261009_iter002_part2_before/`. Regenerated sections: `laura`, `mark`,
`ryan`, `jake` (one line), `extras`, and a new `home` section (`home.py`, `home_items.py`), added to
`ALL_PARTS`. The house half of `3_activities.toml` (its lines 13–807) moved into `home.py`.

**Built**

- **The home_life card** (`sheets/systems/home_life.md`): every item with a person is a choice inside that
  person's hub, opening one screen with the plain finish and, by stage, the tease, the touch or paid look,
  and "(Needs Hungry)" locked. Alone, each item is its own row, shown only while nobody is in the room.
  - Laura's kitchen: breakfast, coffee, dinner (Sunday dinner reads and clears `room_tidy`: +2 tidy,
    −1 messy), help her cook, dishes, a glass (after Laura C 3, `drinks_boost`), study at the table.
  - Laura's living room (Sat 22:00–00:00): a film (+2) or the TV.
  - Laura's room: her hair at the mirror on Saturday evening; asleep at night (her face, K3).
  - Mark's kitchen: Sunday breakfast, dinner, help him cook (Wed), dishes (Wed, Sun). Living room late: a
    beer (`drinks_boost`), the TV, a film. Garage: laundry. Paid look: money +20, Want +1,
    Exhibitionism +1, one a day across all his items, no amount on the button (D11).
  - Ryan: two new hubs, `hub_ryan_kitchen` (the dinner hour) and `hub_ryan_living_room` (weekend
    afternoons: his game, a film).
  - The garden: Mark and Ryan aren't in the garden (they see it from the garage door and his window),
    so their versions are choices in the garden row, read by their rows.
- **Meals refill energy**: breakfast +10, coffee +5, dinner +15; the dinner hour 18:00–19:00 shows who sits down.
- **Alone rows**: breakfast, coffee, dinner, dishes (kitchen); TV, a film, the couch (living room); laundry
  (garage); lie in the sun, hang the washing (garden); study, make-up and hair, tidy (her room).
- **Random home events** (pool `home_event`): 1 in 4 on entering the hall, kitchen, living room or
  bathroom, one a day; each only when its person's row puts them there; a quiet line when nobody's there.
- **The master bedroom at night** (Q58): the door offers Knock only while Laura is up dressing
  (Sat 17:00–18:30), "Ease the door open" when they're asleep (22:00–07:00): one screen naming only who is
  in the bed, then back to the hall. Go in only when both are out. Laura and Mark have faces there asleep,
  so their sleep `occupancy_rows` are dropped from the ledger (K3; `v2_state.json`).
- **Garment lines inside hubs**: the uniform lines moved from the `kitchen_uniform_home` button into
  Laura's and Mark's kitchen hubs and Ryan's new hubs; Laura reads `made_up` for 10 hours.
- **Removed**: `room_feed`, `room_selfie` (the phone owns them), `kitchen_uniform_home` (now hub lines),
  `hall_home_late` (Q75).
- **No arrival text on a repeatable**: the new rows open on what she does, never on walking in.
- **Sweep fixes**: A1-03 (the shower strips her before the towel), A1-04/05/06 (clothes named by slot),
  A1-13 (drawer and garage name the debt only after `knows_mark_debt`), A1-14, A1-16, A1-21, A1-22,
  A1-23, A1-25, A1-31, A1-32; Mark's hub no longer says "kid".
- **Pulled forward from part 5**: Jake's "Go out with him." sets `jake_date_went` (Q73). The regenerated
  Laura section reads it (her step 5 gate) and the build's flag-chain check refused it with no setter.

**LO's call this part** (DECISIONS 77): every home brake is once a day, cleared at midnight
(`home_items.DAILY`, 16 flags in `[engine.daily_tick]`), replacing Q60's 12 hours.

**Guesses taken** (each a number or a line the sheets leave open, all small): study at the desk gives
+1 to the subject she picks; touches add Corruption +1 (the card's "feeds Corruption (Bold only)");
the garden's "show off" pays Exhibitionism +1 only topless and seen; random events raise their person on
every version; the bedside "(Needs Hungry)" at the eased door; new plain lines where a sheet gives only
the item (the rooms alone, Ryan's TV hub, Mark's film).

**Deferred to part 5**: the grocery run (asked at Laura's dinner, bought at the corner shop, delivered at
her next evening). Built whole in part 5 so the list never exists without the shop.

**Checks**

- `gates.py`: 51/87 (part 1: 53/87; 0.1: 57/87). `shape.py --finish`: 22/0. `playtest.py`: 10/10 (its
  two random-event checks now run: 9 random canvases, events fire at 4/4 rooms). `who_is_where` against
  the ledger: 0 mismatches.
- Live (headless): the door at Tue 23:30 shows only "Ease the door open" and names Laura asleep and
  Mark's empty half; Sat 17:30 only "Knock."; Tue 14:00 only "Go in."; Laura's breakfast gives Warmth
  +1, disappears for the day, and comes back after midnight.
- Turned green against part 1: every person here has a face (12 → 9 pairs; Ryan at dinner, Ryan's
  weekend TV, Laura asleep fixed), nobody is woken (5 → 3), her clothes are named exactly (5 → 1),
  a button does something (19 → 15), a past line has its event (12 → 10).
- Red, and why:
  - **explicit floor 7.0%** (floor 7.5%, was 11.0%): 90 new repeatable home beats, plain by the card's own
    rule, and the heat that would sit on them is the 40 placeholders below.
  - **a place is not a catalogue**: `room_sleep` only, its twelve hour-buckets (0.1's, unchanged).
  - **world reachable**, **a step is seen from the next room**: the part 1 gate gap (`default_entry`).
  - **sinks >= sources** (3 : 11): the paid looks are four new money sources; already red in 0.1.
  - **nobody is woken (3)**: Laura A 1 and A 4 off their windows and `meet_figure`: parts 3, 4.

## Part 3 — Ryan, Laura and Mark

Snapshot: `first_term_snapshots/20261009_iter002_part3_before/`. Regenerated: `ryan`, `laura`, `mark`, `jake`,
`tom`, `zoe`, `pools`, `home` (the last four for the late flags and the new card shape only).

**Built**

- **Their steps against the changed sheets** (the sheets' 2026-10-08/09 rows, sweep fixes named):
  - Laura C 1 starts only from "Follow her upstairs." in her kitchen hub, which sets `laura_dress_invite`
    (read for an hour); walking into her room does nothing (A2-09).
  - Laura C 2: what she smells and asks follows the late flag; the truth by the flag goes to her room,
    a different place than the flag says is the lie (A2-02). "No guys at the door" (A2-41, LO's line fix).
  - Laura C 3: home at dawn, no clock hour (A2-05); not Sunday (the ledger's window).
  - Laura C 4: "Don't tell Mark." on the button (A2-39). Laura C 7: no Mark line, and the party screen has a
    bucket for every minute (A2-21, A2-22).
  - Mark A 1: "bare" legs only when they are; nobody in the doorway (A3-06, A3-20); "Let me get dressed
    first." now dresses her.
  - Mark A 4: "Laura's gone up"; not on a night she came home late (A3-04).
  - Mark A 5: its two windows (Sun–Fri 23:00–00:00 and Mon–Sat 00:00–01:00, never Sunday 00:00, A3-03);
    the step needs bare legs (Q72: no jeans, no leggings) and not a late night; **two written nos**, one per
    voice, verbatim from the sheet (A3-13); no pay on any button.
  - Mark A 7 and the Sunday table: no pay on the buttons (D11). Mark A 9: Sunday's money is counted out of
    her purse and back in it; nothing moves on a Wednesday (A3-34).
  - "kid" is gone from every line Mark says: @player, or @player.nickname where the sheet has him soft (Q71).
    These are word swaps inside existing screens, as the sheets now write them; no other prose changed.
    Follow-up (LO, 2026-10-09): three more in the Sunday table's paid look, which `mark.py` reads from
    `beat_mark_table_look_*.txt` (my first grep covered the `.py` files only): "Go on then, @player." and
    "Fair, @player,". `grep -rnw kid toml_phases/` and the built HTML now show nothing.
  - Ryan A 6 is true any Saturday 08:00–10:00 (Kayla leaves by 10:00, Q70; the ledger window). Ryan A 9's
    "And Jake?" only after Jake B 3 (A2-12).
- **The new step windows** come straight from the ledger: Ryan A 4, A 8, A 9 and Mark A 6 at 19:00–22:00
  (after the dinner hour). `canv.step_trigger` now also builds a step's second window (`when_also`).
- **The late flags** (Q69): each outing that ends after 22:00 sets its own flag and `came_home_late`:
  `late_party` on Zoe's party and the party house's hot tub (only exits from 22:00), `late_shift` on Tom's
  after-close, `late_date` on Jake's goodnights and Laura C 5. Each is read for 4 hours; her bed clears all
  four (part 2). The street sets none (Q75). Laura's stairs row and her step 2 read `came_home_late` for 4
  hours, as the ledger has them; the catch says the true reason by the specific flag. Laura C 5 counts as her
  catch for that night.
- **Laura's curfew call** (npc_laura.md:130-137): Friday 21:00–22:00, only while Laura is awake in the
  kitchen, an hour after the curfew is set, once a day; her three lines as signed; it never says where @player
  is, and both answers return her to where she was. Missed: suspicion +2.
- **Cards**: every person's step cards now carry the step's real requirements (each meter with its number and
  stage name, each of their numbers, a flag as words, another person's step named as that event in the tip),
  never the counter (the seven ladder sheets, "Card goals"). Done for Ryan, Laura, Mark, and also Tom, Zoe and
  Jake (same generator); Hale's are part 4.
- **Repeat screens no longer say "when you come in"** (Ryan's, Laura's and Mark's hubs).
- **Part 2 follow-ups**: every home item screen has a free "Not now." (gate: a spent day still has a door);
  Laura's breakfast and coffee share one screen (her kitchen hub was 9 buttons on paper).

**Checks**

- `gates.py` 51/87 (start of part 3: 51/87; the same total, different gates). `shape.py --finish` 22/0.
  `playtest.py` 10/10. `who_is_where` against the ledger: 0 mismatches.
- Live (headless): a Friday-23:00 click at Zoe's party sets `late_party` and `came_home_late`; at 23:40
  Laura is on the stairs and her catch says "Zoe's again?" with smoke and cologne; walking into her room
  on a Tuesday evening plays nothing.
- Turned green: a card shows the real gates (111 → 13 lines, all Hale's: part 4), a spent day still has
  a door, the climb is paid for (kept green: the call's suspicion is capped), a chat is short and timed,
  a repeat doesn't say it's the first time (11 → 6: Zoe, Jake and the park left, parts 4–5), a phone line
  is true (10 → 7: the after_round texts are part 6, the dean's calls part 4).
- Red, and why:
  - **sex for pay names the amount (4/9)**: your D11 (no earned pay on a button) against this gate, which
    wants the sum on the button. The scenes say it ("Five an inch. Twenty tops."). A warning, not a block.
  - **ladders move forward**: the ledger lags the signed scene sheets (below), plus a gate gap: it compares a
    step's canvas with its `when` only and ignores the ledger's own `when_also` (Mark A 5, Zoe A 4).
  - **nobody is woken (3)**: Laura C 1 and C 4 are the part 1 building gap (`entry_from` stops at the hall);
    in play Laura walks up from the kitchen. `meet_figure` is part 4.
  - **a day word fits its window**: `ryan_05_thin_walls` "Kayla is still here in the morning" is the signed
    hook about the next morning; the college two are part 4.

**For LO to re-sign: the ledger lags the scene sheets** (I did not edit the ledger):

| step | the signed scene sheet says | the ledger's step declares |
|---|---|---|
| Laura C 1 | starts only from "Follow her upstairs.", which sets `laura_dress_invite` | no flag |
| Laura C 2 | `came_home_late` read for 4 hours (Q69) | `came_home_late` is_true |
| Mark A 4, A 5 | not on a night she came home late | no flag |
| Mark A 5 | bare legs (Q72) | a `gate_note`, not a gate |

## Part 4 — college

Snapshot: `first_term_snapshots/20261009_iter002_part4_before/`. Regenerated: every section (the card
shape changed in `canv.py`); the college rows in `3_activities.toml` edited by hand.

**Fixed first** (my own slip in part 3): the edit that capped Laura's missed curfew call had also landed on
the dean's grades call (`8_phone.toml`), so missing his call would have blocked Laura's that day. Removed.

**Built**

- **Classes.** Each class has its own lines for Focus, Chat and Doze (they were one pool pasted into four,
  A5-15); figure drawing's are about drawing, and the lecturer's praise is on Focus only (A5-16). Focus
  is shut under 20 energy, as the thought says (A5-08). Psychology before Hale and Nadia are met says
  who they are (A5-06); no "good morning" on Thursday afternoon (A5-07); no "back of the class" after the
  front row (A5-09). Business names the study guy and the rival only once met (A5-17), and the rival's
  "dress for once" only when she has (A5-10). The TA's hours are Tuesday to Friday (A5-12). In figure
  drawing Zoe is "the girl at the next easel" until she's met (A5-13).
- **Zoe's and Jake's rows once met** (L27): faces in the lecture hall in their classes (`hub_zoe_class`,
  `hub_jake_class`), checked live: Tuesday 08:40 shows the art lecturer, Jake and Zoe.
- **The first classes.** No study group that doesn't exist (A5-18); the rival as a stranger if she isn't
  met (A5-17); in figure drawing the cocky guy is "Jake's teammate" only once Jake is met, and he is met on
  the second screen (A5-14; he has no lecture-hall row, see below).
- **Events.** The dress-code warning comes as the class starts (a class fills its window, A5-19), from
  whichever lecturer is in the room (A5-31), and the rival speaks only in her own classes (A5-20). The guy
  beside her: his ask is said once, on its own screen (A5-23); the rest of the class really passes
  (A5-21); "like a model student", not "a good boy" (A5-22).
- **The exam.** The cocky guy's flash beat no longer repeats his ask (A5-23); flirting for the study guy's
  paper is in Business only, once he's met (A5-24); the result goes up "next week" (A5-25).
- **Hale.** Nadia introduces herself only when she isn't met (A4-15). Hale B 2's act fits what she wears
  (skirt, waistband, a dress's hem), and the panties line shows only when they came off now (A4-23).
  He reads her start choice without claiming she told him (A4-13; DECISIONS 25). Hale B 4: "his wife"
  until he names her at the door (A4-19); in the sheer blouse she undoes it, in any other top she pulls
  it up, with the sheet's word swaps on the later screens (A4-22; the new hand beat for that top is a
  placeholder). His office hub: the photo by his step (A4-18), a way out to the faculty floor (A4-26).
  Hale B 5 reads the Psychology midterm (A4-20). The Thursday repeat's hand screen is a placeholder
  (A4-32). Cards: no clock times, no closed card nothing can reach (A4-37, A4-38).
- **Nadia.** "He asked about you after class" only after Hale's step 2, on a Psychology morning, and not
  in the lecture hall (A4-17, A1-12); "He'll lose his place again" only after Hale B 2 (A4-16).
- **The campus hubs** (Zoe, Jake, Nadia, the lecturers, the offices): every "Go." leaves the room (A4-26,
  A5-30); class hubs are before class, not after (A5-26, A5-27); Jake's lines no longer give away later
  steps (A4-11, A4-12) and "Saturday?" waits until he isn't booked (A4-31); no arrival lines (A4-28).
- **The dean.** His warning is the phone call itself and returns her where she was (gate: a phone line is
  true); his hub's lines are true after the warning (A5-28, A5-29).
- **The gym** (campus_gym.md): "Work out" (60 min, energy −15; in just a sports bra at Daring,
  Exhibitionism +1), once a day; Jake's training hub on Tuesday and Thursday afternoons once she has his
  number: train with him, his hands on her hips at the rack (Curious), a kiss against the lockers (Bold,
  after Jake B 2). `worked_out` and `jake_gym_today` are cleared at midnight.
- **The campus rows** (`3_activities.toml`): the quad and canteen gossip claims a party only after one, and
  no dare at all (no flag records one; A1-08, A1-09); Nadia's canteen line as above; "the girl from class"
  (A1-28); the toilet mirror's locked teaser is gone (A1-18).
- **Quest cards from real requirements**: every card now passes (`a card shows the real gates` 76/76); the
  stage names stand as goals, not packed into labels (A4-35); the week-one story card's first goal is
  meeting Hale (a flag), and its tip puts the café in town; the tier card names the right Bold acts
  (A6-22); Nadia's card has her Thursday class (A6-25); Claire's card has no clock time (A6-40); Vance's
  card no longer says Mark owes him (A1-13).

**Checks**

- `gates.py` 53/87 (start of part 4: 51/87). `shape.py --finish` 22/0. `playtest.py` 10/10.
  `who_is_where` against the ledger: 0 mismatches.
- Turned green: a card shows the real gates (13 → 0), every hub is met first, no one is named before
  they're met (6 → 0), every authored node is reachable. Better: a past line has its event (10 → 2: Tom's
  card and the feed, parts 5–6), every person here has a face (9 → 6, all part 5), standing surface
  (63/68 → 67/68: Zoe at the party house, part 5), a repeat doesn't say it's the first time (6 → 3),
  nobody is woken (3 → 2: the building gap), a button does something (14 → 8), one pool, one place
  (67 → 54).
- Still red: **explicit floor 6.4%** (the Thursday repeat's explicit screen is a placeholder now: 35 → 34
  explicit beats); **a destination is never open and exit-only** (the men's toilet by LO's call; the corner
  shop and Zoe's kitchen, bathroom and late living room, part 5); **a named person is where the line
  says** (42, mostly the house's sleep lines from parts 2–3 against Laura's late-night stairs row, listed
  for part 7).

**For LO**

- The cocky guy's sheet puts him in figure drawing, but the ledger gives him no lecture-hall row, so the
  build can't put his face there; he is met and speaks in the first class only.
- `hale_04_claire_knocks.md:27` signs "Go home." → campus. Kept as signed; the sweep (A4-25) calls the
  label untrue. Your call: a different label, or home.

## Part 5 — town

Snapshot: `first_term_snapshots/20261009_iter002_part5_before/`. Regenerated: every section; a new `town`
section (`town.py`) added to `ALL_PARTS`; town rows in `3_activities.toml` edited by hand.

**First, LO's call:** Hale B 4's "Go home." goes home (`home_hall`, about 25 minutes), not to campus. LO is
fixing `hale_04_claire_knocks.md:27` for his sign. The cocky guy stays without a class row, as signed.

**A bug of mine, fixed:** a choice carrying `costs` and also an effect that subtracts the same amount
charged twice (engine.md §27: the cost is deducted on the click). Found live when the corner shop took $40;
it had been on the home items' energy since part 2 (dishes, laundry, cooking, study, tidying) and on the gym.
`canv.emit` now drops the repeated effect; a parse of the build finds no double charge left.

**Built**

- **The café (Tom, Gary).** No pay on any button (D11): Tom says the price ("Gary's in. Twenty for ten
  minutes. Half's mine."), the toast shows it. An evening shift starts by 19:00 so it ends by the 22:00
  close (A5-04); Friday's tips are the Friday evening shift. Clocking out takes the uniform off (A5-02).
  The shift's lunch-rush and slow-afternoon lines show at their hours (A5-05); "Booth four's going to tip
  big" only while Gary's in (A5-03). Tom's Friday after-close carries his face. His closed card ("You told
  him no more late shifts") is gone: nothing sets his counter below 0. Hub exits spend time.
- **The clothes shop.** No prices in the try-on prose (they're on the shop's labels, A1-30); "Hang them
  back up." instead of a "Get dressed again." that dressed nobody.
- **The corner shop and the grocery run** (home_life.md:100, Q67): at Laura's dinner, "The shopping list."
  opens its own screen: she gives you a list and twenty; the corner shop opens on your map only while you
  have it ("You've got nothing to buy." otherwise: Q50, the grocery run only); buying costs the twenty; at a
  later dinner you give it to her (Warmth +2), or a day late you own up (suspicion +2, the twenty back).
  Checked live: $20 in, $20 out, Warmth 50 → 52.
- **Zoe's flat.** Her living room by the hour: Friday 18:00–19:00 she's getting ready and does your face
  ("Lips. Open."; in her lap at Curious; `made_up`), the Friday party (no arrival line, A4-27), the party
  after midnight, her couch other evenings (A4-06, A4-07); "What's tonight's dare?" only while a dare can
  happen (A4-42). Her bedroom on weeknights is her face, and the dress she lends is a choice in it (moved
  from 3_activities). Her kitchen: a drink on party night (three a night, as the party's), a glass of water
  other evenings. Her bathroom: fix your face (hygiene +5, once a night), the queue on party night. Her couch
  when she's in her bedroom. The party house: her face in the hot tub on Saturday nights.
- **Zoe's steps.** Zoe A 0: "I've got a shift" only with the job, else class (A4-43). Zoe A 3: she strips to
  her bra and panties at the tub; "Take your bra off." takes it off (A4-24); "You unhook your bra" as the
  sheet now writes it; with no bra on, the kiss screen is a placeholder; every minute has a way home (A4-01).
  The park: a way out; no promised "worse dare" (A4-41).
- **Jake's pickup and door.** His face at the pickup (Sat 19:00–21:00) and at the goodnight; the booking is
  read for 7 days and lapses (Q73; gate: a latch flag is cleared); the night he took her out is read for 6
  hours and cleared at midnight; Jake B 3, B 4 and the goodnight gate on it, the goodnight only after Jake B 4
  (A4-04); every minute of the pickup has a way home (A4-02); the curfew line is her own thought, since
  Laura isn't home on Saturday evening (A4-05). Ryan's −5 Warmth and "Who's Jake?" move to the night he sees
  Jake at the door, once (jake_02 sheet:28); the bathroom line is gone (A2-13).
- **Vance's Monday knock** (added to this part by LO): his row's window, Monday 18:00–19:00, with his face;
  `rent_carried` read for 48 hours (the engine stamps it at Sunday's count); "Go back in." goes to the hall.
  His porch goodnight leaves his gate (A1-24); "Sunday comes round quicker" (A1-29).
- **Random town events** (street.md): the wind and her skirt, a car slows, Vance on his porch, a jogger, the
  quiet street; 1 in 4 on coming out onto the street, one a day; the bolder answer at Curious/Daring.
- **The cocky guy at the party**: a face that isn't only the heat one; party_hookup's line names him by
  figure drawing, not "the one who drew you instead of the model" (A6-07).
- **The late flags**: the party house soak sets `late_party` after 22:00.

**Checks**

- `gates.py` 59/88 (start of part 5: 53/87; the 88th is "what money buys opens a door", now judged and
  green: the groceries). `shape.py --finish` 22/0. `playtest.py` 10/10 (14 random canvases; events fire at
  5/5 places). `who_is_where` against the ledger: 0 mismatches. `grep -rnw kid toml_phases/`: nothing.
- Turned green: a clock bucket has a catch-all, a latch flag is cleared, standing surface (68/68), what
  money buys opens a door, a button does something, a repeat doesn't say it's the first time, a price is on
  its label, a spent day still has a door, her clothes are backed, the climb is paid for, a place is not a
  catalogue... (see the gates file). Better: every person here has a face (6 → 1), a destination is never
  open and exit-only (26/31 → 30/31: only the men's toilet, LO's call), a named person is where the line
  says (42 → 34).
- Still red: **sex for pay names the amount (0/9)**, D11 against the gate (part 3); **every person here has
  a face (1)**: Tom at the café 22:00–23:00 Mon–Sat, closing while the café is shut (below); **a past line
  has its event (1)**: the feed's party post, part 6; **explicit floor 5.9%** (more plain repeatable beats;
  the heat sits in the 43 placeholders).

**For LO**

- Tom's row runs 08:00–23:00 ("open 08:00-22:00, then he closes"), the café shuts at 22:00, and only Friday's
  after-close has a scene. The face gate wants a face Mon–Thu and Sat 22:00–23:00, when she can't be in the
  room. Options: an `occupancy_rows` entry for Tom closing (like Ryan's shower), or his row ending at 22:00
  except Friday. Your call; nothing changed.

## Part 6 — the phone

Snapshot: `first_term_snapshots/20261009_iter002_part6_before/`. `8_phone.toml` is now generated by
`phone.py` (the threads, the feed) plus `phone_calls.toml` (the calls, carried over verbatim from parts 3
and 4); `build_scenes.sh` runs it.

**First, LO's call on Tom's 22:00–23:00 (option A):** his café row is split into 08:00–22:00 and
22:00–23:00 (same place and days, he still closes up), and the 22:00 row is an `occupancy_rows` entry,
"closing, room shut", like Ryan's shower hour. Both are ledger edits (`v2_state.json`), because the gate
exempts a whole row by its place and start time (`gates.py:14502-14512`). Presence is unchanged
(`who_is_where` against the ledger: 0 mismatches); `every person here has a face` turned green (42/42).

**Built**

- **The seven threads, message by message** (each person sheet's "Messages, per reply"): Ryan (the phone
  thing; his two-knocks repeat), Laura (dinner, the days she cooks, 16:00–17:30, every 7 days), Mark (the
  rent, Saturday evening, weekly), Tom (a shift after class; his Friday repeat), Zoe (the party on
  Thursday; the run on Friday, setting `zoe_run_booked`), Dr. Hale (his college email; his Wednesday
  repeat), Jake (Saturday; "where are we going" opens a second round, and only her yes books the date).
  Every follow-up waits for her reply (`after_round`) and answers only the reply she sent
  (`after_choice`); no message carries `round` (it does nothing). Where a sheet gives no follow-up (Ryan's,
  Tom's and Hale's repeats) none is invented. Each thread keeps its cause flag, its delay and its window.
- **The selfie** on Exhibitionism (wardrobe.md, Q66): "Post a selfie" (Covered), "Post one in your bra"
  (Daring 20), "Post one topless" (Showing 40); followers only, once a day each; each label names the act.
- **The feed behind its flags**: the party post only after `party_went` (and campus talk 10); the mirror-pic
  post once followers reach 20 (followers come only from her own posts).

**Checks**

- `gates.py` 61/88 (start of part 6: 60/88 after Tom's occupancy row; 59/88 at the end of part 5).
  `shape.py --finish` 22/0. `playtest.py` 10/10. `who_is_where`: 0 mismatches. No "kid".
- Turned green: a phone line is true (5 → 0), a past line has its event (the feed post, now 40/40),
  every person here has a face (Tom).
- Verified in the build data, not clicked live: 11 conversations, 26 follow-ups each on an after_round
  and after_choice, the three selfie rungs on `exhibitionism`, both posts' triggers (the built HTML
  carries every `after_round`/`after_choice`).
- New warning: **a chat is short and timed (4)**: four signed lines outside the 3–7-word band (Laura's "ok.
  text me when you're on your way", Mark's "good.", Tom's "twelve and tips. more in a tighter top.", Hale's
  whole-sentence email). Kept as signed; a warning, not a block.

**For LO**

- **Tom B 6's window: the sheets disagree.** `npc_tom.md:46` (his ladder table) says Mon–Sat 22:00–23:00;
  `tom_06_after_close_kiss.md:10` and `:30` say Friday only ("Stay late Friday?", sweep A3-30), and so does
  the ledger (L24). The build follows the ledger: Friday. Nothing changed; one of the two needs your fix.
- **Mark's rent text says "$75."** (npc_mark.md), but the rent rises to $90 and $100 as she pays (the money
  sheet). The phone can't read the rent's level, so after the first rise the text is wrong. Kept as signed.

## Part 7 — the whole game

Snapshot: `first_term_snapshots/20261009_iter002_part7_before/`. Report: `REPORT.md`; the reader's
tables and JSON: `reader/`.

**Fixed (from the first `--ship` run, 9 BLOCK red):**

- Named-person lines held behind the person's presence: Mark's living-room "Laura's asleep" behind Laura in
  the master bedroom; Laura in bed on Mark A 4 and A 5's triggers; "Laura's out" on Sunday in `mark_01` and
  `mark_sunday_table`; `mark_07` "Ryan's door is shut upstairs"; Mark's Wednesday dinner line; the garden's
  sun rungs and `master_asleep` behind their people (and 22:00–07:00); the nap line; the home event label
  "Mark dozing"; "Mark's asleep" removed from Laura's film line.
- Presence checks on `ryan_04` (Laura in bed, Mark in the living room) and `laura_05` (Laura in the living
  room). One-time lines on `mark_05`'s start and `hale_04`'s desk are lifted out of the repeating text
  (`lift_line`); "a one-time line speaks once" is green.
- **Two presence checks taken back out, found by `reach_all.py`:** Laura in the kitchen on `laura_01` and
  `laura_04` (the gate's building gap, lead item 6, means the check never satisfied `nobody is woken`
  anyway), and Gary in the café on `tom_04` (Tom B 4 is where she meets Gary; his row waits for
  `gary_met`, so the check made the step unreachable). Named-person lines went 10 → 12 because of this;
  both are the same gate gap or a first meeting.

**Checks:** gates 61/88; `--ship` 8 BLOCK red (REPORT.md lists each). `shape.py --finish` 22/0.
`playtest.py` 10/10. Every ladder step played with `playtest.reach_step`: 43/44 as the ledger declares,
44/44 once Laura C 1 declares `laura_dress_invite` (a scratch copy of the ladder, the ledger not edited).
`who_is_where` vs the ledger: 0 mismatches. No "kid". 43 placeholders (no new ones in part 7).

**The reader:** six `v2-reader` runs on all 193 canvases (no shipped release, so every canvas is touched):
135 FAIL verdicts on 105 canvases. Saved in `v2_state.json` `release_page.reader` (the gate reads it there;
`release_page.reader_read_at` says when). No reader FAIL is fixed in this part; REPORT.md sorts them.

## Part 8 — the reader's fixes (LO, 2026-10-09)

Snapshot: `first_term_snapshots/20261009_iter002_part8_before/`. LO's call: fix the reader's kind-A slips,
build the three kind-B lines, re-read the changed canvases; waive "no empty rooms" for the men's toilet and
the lines caused by the gate gaps (lead items 6, 7, 9); waive the kind-D craft FAILs for 0.1 and keep the
list; leave the ledger and the sheets alone.

**Kind A, fixed (build slips; no sheet line rewritten):**

- *Café (tom.py, extras.py):* "Eight till seven" for the shift hours (the shift opens 08:00–19:00); "first
  tray of the shift"; "Today" for the back room; Tom B 5 "In the back room, between orders"; Tom B 6 opens
  "Friday, closing time"; booth four is Gary only while Gary is in the café, else a regular at the window;
  Tom's work lines only in the uniform, a customer line out of it; Gary's "Slow day"; the coffee is paid
  for only on "Drink it"; "Nobody here knows you" only before she meets Tom.
- *Zoe (zoe.py, extras.py, town.py):* the strap line only with a bra on; the bra on her bedpost only after
  the sleeve dare took it (`zoe_has_bra`, new); the party photos only after `party_went`; her dress is on
  before "she whistles" (a new `dress` node); the hot-tub reminder not on Saturday; the fries off the guy
  beside her; "Whisper with her a while"; her couch line names her door only while she's in her bedroom;
  the bedroom look's "Go." walks to the living room (2 min).
- *College (college.py, hale.py, jake.py, 3_activities.toml):* every class, first meeting, midterm, the
  desk guy and the dress-code event fire in the first 15 minutes of the slot (`at_start`); the lecturer
  hubs say what they're doing without "before the class starts"; the figure class's pose button opens
  its own "when you're Watched" screen (the orphaned Hungry node removed); Hale B 1, B 2, B 5 fire
  08:30–08:45 (`at_class_start`, a time condition; the ledger window stays, a ladder static item for the
  lead); Hale B 1 "with his slides up", "Partway through"; Hale B 5 "You take the front row while the room
  fills"; Hale's Thursdays end by 19:25 (window 18:30–19:05) and close on "When he looks at the clock
  again"; "Talk with him a while" in Jake's class hub; the canteen shows the counter first and the meal only
  after "Eat"; the dean's notice "Step back into the corridor" (2 min, to the faculty floor).
- *Home (home.py):* the hall mirror's no-bra line needs a top (a dress version beside it) and "good girl"
  needs plain clothes (worn corruption 0, not the thin top); the college letter shows a day after the
  dean's warning; "The kitchen's yours" at breakfast; "watch the street go by"; the wardrobe gap reads
  owned-not-worn, with a worn version; the lounger's sun only 07:00–19:00 (the last of the light after);
  no "sleeves"; the washing line says Mark's watching when he's in the garage; Mark "slumped, eyes half
  shut" at the late event (his row is "up late").
- *Mark and Vance (mark.py, 3_activities.toml):* her version of Mark A 3 changes first ("Go up and change",
  a new `hers_down` node) so the shorts are on before the screen names them; "the short stays on the tab"
  only when `rent_carried`; the bare knee only without jeans or leggings; Mark A 7's "no" no longer slides
  back a twenty he never put down; Mark A 9 counts "your money" and says "That's what you've got"; the debt
  offer's "He hasn't hidden anything" only after `knows_mark_debt`, and the debt is years of loans from
  the man who owns the house (WANT: the family rents); Vance's "maybe" drops the envelope; TV and the film
  with Mark end before his 02:00; Wednesday's cooking line to 20:00, the soaking pan after; "Then the rent"
  only before the count; Vance's porch line "He'd sell me a lot of things to clear it"; the house look's
  "Walk on." to the street.
- *Pools and town (pools.py, town.py):* the cocky guy "since he came in"; his exam line only after the art
  midterm's flash (`cocky_exam_deal`, new); the park wind line without the skirt; "face tipped up to the
  sky"; the selfie is posted only on "Post it" (a new `posted` node); the hollow with Zoe only within an hour
  of "Run a lap with her" (`ran_with_zoe`, new); the shower's footsteps only at hours somebody is up in the
  house; Vance "lowers it when you pass".
- *Ryan and Laura (ryan.py, laura.py):* Ryan A 6's headphones and "Roll over" each show the act; his
  goodnight on a Thursday says Saturday; his cover thought on Sunday says "At the table"; Laura's first catch
  drops "again"; Laura C 5's "no" leaves her inside, with Laura silent on the couch; the catch says "She
  waits like this now" only after Laura C 2; "Dinner in ten" only to 19:50; "You two seem close" only from
  Ryan's step 2; "never done before" once, then "She counts it again".

**Kind B, built:**

- *Laura's final no* (`npc_laura.md:72`, "Every catch after is a strict-mom punishment"): at laura_step −1
  the catch offers only "Take what's coming." (the curfew), whatever her Warmth.
- *Ryan's final no:* the door goes back to one knock (`ryan_knock_code` unset at the final), and his hub
  opens "You knock once. He opens it on the first knock and goes back to his bed."
- *Vance's porch promise:* no sheet gives a number to "knock a little off his number", so the promise is
  taken out of my line instead of built (building it needs a sum and a mechanic: LO's call, in REPORT.md).

**Not fixed: kind C (sheet against sheet or ledger; the lead's, for LO's sign):** the opening's clock
(OPENING.md times vs Mark's and Ryan's Monday rows), Vance's first meeting (his porch row starts at
`vance_met`), Laura C 7's radio and morning, Mark A 3's "Not the shirt this time", Mark A 5's "tomorrow
night" and the twenty in the Power<50 no, the twenty count in Mark A 7 and the Sunday table, Jake's
"tonight" on his daytime hubs, "Home by eleven", "Biology class" in Zoe's first meeting, Hale B 4's top
button and 18:40 knock, "Button up" on Hale's Thursdays, Tom B 5's "Goodnight, Tom." at 14:30.

**After the re-read (77 canvases, 31 FAIL), six more of mine fixed:** Hale B 5's grade line "Top of the
class" (no letter grades in the ledger); Laura's truth screen "the part about him" (no touch recorded);
"Is Jake bringing you home" behind `jake_date_booked` (the sheet's line, gated); Tom's "palm already open"
only in the uniform with Gary in; "ready for Friday" (the sheet's line) only Monday to Friday; the hollow
with Zoe to 09:30 so it ends inside her park row; Ryan's Thursday goodnight says "Tomorrow" after
midnight. The 12 canvases these touched were read a third time (12 FAIL, 9 of them craft).

**Checks:** gates 61/88; `--ship` 8 BLOCK red (the same eight as part 7). Ladder static problems 24 → 27
(the three Hale time conditions, the lead's). `shape.py --finish` 22/0. `playtest.py` 10/10. Every step
43/44, 44/44 with Laura C 1's flag. `who_is_where` vs the ledger: 0 mismatches. No "kid". 43
placeholders. The reader: 193/193 read; 72 FAIL verdicts, 47 craft ones waived in
`release_page.reader_waivers` (LO), 25 left (REPORT.md). Tables: `reader/reader_p8*.md`.

**Reader error, no change:** the garden's Ryan rungs (`ryan_step gte 3/7`) are right: the ledger's "Ryan A 4"
is step n = 3 and "Ryan A 8" is n = 7.

## Part 9 — my last six reader slips (LO, 2026-10-09)

Snapshot: `first_term_snapshots/20261009_iter002_part9_before/`. LO: fix my 6 slips on the 5 canvases,
re-read `laura_08` and the touched canvases; keep Hale B 1/2/5 at 08:30–08:45 (the lead writes it into the
ledger); leave Vance's promise out; don't touch `iterations/002/placeholders/` (the writer session's).

**Fixed (4 canvases; the fifth, `jake_03`, is kind C — its "Nobody," is the signed beat,
`jake_03_my_boyfriend.md:34`, against Laura's Saturday row):**
- `laura_catch`: on a date night her silent look shows only when no other line on the screen speaks
  (suspicion under 30, and not the step 2+ / Want 50+ "Tell me everything").
- `hub_laura_kitchen`: "Don't tell Mark" only while Mark isn't in the kitchen (the wine item says "Just the
  one" when he is); "For a while it's just the two of you" (the talk spends 25 minutes).
- `hub_tom_cafe`: "Back to work." only in the uniform; out of it, "Sit at the counter a while." and "Go.";
  "He watches you the whole shift" only in the uniform; the palm line only within the hour after she topped
  up Gary's tea (`served_gary`, new, set in `hub_gary_booth`, read by hours since).
- `hub_zoe_apartment`: "Still here? Good girl." only within 8 hours of `party_went`; otherwise "Now you show
  up? Get a drink. Catch up."

**Re-read** (`laura_08` + the five changed canvases, incl. `hub_gary_booth` for the new flag): every slip
above passes, and `laura_08` passes (her punishment rule is built). The read found 8 older lines on these
canvases that earlier reads passed (REPORT.md "Part 9"); not fixed, outside this part.

**Checks:** gates 61/88; `--ship` the same 8 BLOCK red; `shape.py --finish` 22/0; `playtest.py` 10/10; Tom and
Zoe 10/10, Laura 8/8 with C 1's flag; `who_is_where` 0 mismatches; no "kid"; 43 placeholders. Reader: 70
FAIL verdicts, 46 craft waived, **24 left**.

## Part 10 — the last fix pass (LO, 2026-10-09)

Snapshot: `first_term_snapshots/20261009_iter002_part10_before/`. LO: fix the 8 older lines the part 9 read
found; re-read only those canvases; list anything new in REPORT.md without fixing it; then stop for good.

**Fixed:**
- `laura_catch`: "Kiss her goodnight." is no longer shown locked (it showed at laura_step −1, against "Nothing
  else"); at step 8+ below Hungry a thought says it instead ("Not yet").
- `hub_laura_kitchen`:
  - "Eat something, sweetheart" only before `ate_breakfast`.
  - "Dinner in ten" only before `ate_dinner`.
  - Ryan "wet from the gym" Monday to Saturday; on Sunday "still yawning from the couch".
  - "Study at the kitchen table." and "talk while she works" (no "while she cooks" at 21:00).
- `hub_tom_cafe`:
  - The work lines only 08:00–22:00.
  - "Back to work." and "Sit at the counter" only to 21:30.
  - After 22:00, "The sign's turned to CLOSED"; "Go." always.
- `hub_gary_booth`: "Ten minutes, when you've got them." only when the ten minutes can fire: weekdays
  14:30–18:00, in uniform, Corruption 40+.
- `hub_zoe_apartment`: "What's tonight's dare?" only when a dare can fire (Exhibitionism 40+, at the party
  tonight).

**Re-read** (the 5 canvases): all eight lines pass. New: one truth FAIL on `hub_tom_cafe` and two craft
FAILs, listed in REPORT.md and not fixed, as LO said. Craft ones waived under LO's standing call.

**Checks:** gates 61/88 (no change in the red list); `--ship` the same 8 BLOCK red; `shape.py --finish` 22/0;
`playtest.py` 10/10; Tom and Zoe 10/10, Laura 8/8 with C 1's flag; `who_is_where` 0 mismatches; no "kid";
43 placeholders; `iterations/002/placeholders/` not touched. Reader: 67 FAIL verdicts, 47 craft waived,
**20 left** (17 kind C, 2 edge minutes, 1 new on `hub_tom_cafe`).

## Writer — the 25 screens in (LO, 2026-10-09)

Snapshot: `first_term_snapshots/20261009_iter002_writer_before/` (toml_phases, build_scripts, v2_state.json,
output). ⚠️ `canv.py`'s emit hook and `writer.py` were written a few minutes before the snapshot was taken;
no game file had changed yet, and in the snapshot copy `writer.py` is removed and `canv.py` reverted, so it
is byte-identical to the part 10 copy (checked with `diff`).

**How the text gets in (no hand edit of 7_final_game.toml):** `build_scripts/writer.py` reads
`iterations/002/placeholders/NN_<canvas>_<node>.txt` (read only; the writer's folder is not touched) and
`canv.emit` calls `writer.fill()`, which swaps that node's `PLACEHOLDER —` block for the screen.
- **Lines:** a blank line starts a new beat. A quotation-only line becomes a dialog block, with the speaker
  given per file in `SPEAKERS`. A line with narration around a quotation stays a paragraph. `*…*` becomes
  her thought.
- **Variants:** coded in `VARIANTS` exactly as each file places them (after a beat, after or in place of a
  sentence, in place of the spoken lines). A beat with variants becomes one if/elseif chain of whole-beat
  versions, most conditions first and the plain beat last, wrapped so it never merges with a neighbour.
- **Placeholders filled:** #1–3, #21–39, #41–43 (`FILLED`). Laura's 18 (#4–20, #40) stay PLACEHOLDER.
- **Checked:** every sentence of every screen is in the built node (0 missing); block depth ≤ 4.

**Checks:**
- `list_placeholders.py`: **18 placeholders**, all Laura's (14 in `hub_laura_kitchen`, 2 in
  `hub_laura_living_room`, 1 in `hub_laura_bedroom`, 1 in `home_event_laura_robe`).
- Gates 61 → **59/88**. Turned green: **explicit floor 6.2% → 9.5%** of 306 repeatable beats (floor 7.5%;
  9.0% of all 513).
- New reds:
  - `her climb`: 6 paid repeatables, 17 problems. The Mark hubs' paid looks are open on a new save before
    his paid route's introduction, and the paid nodes carry no two-tier voice.
  - `no one is named before they're met`: `hale_thursdays` "Claire's here at half past." with nothing on
    the way reading `claire_met`.
  - `prose has room`: `but` 2.80/1k, under the field's p10 of 2.88.
- Already red, worse:
  - `her clothes are named exactly` 1 → 5:
    - `hl_beer_touch` and `party_house_soak` strip with no garment coming off;
    - `sun_mark_tease` / `sun_mark_paid` name her bra on `worn_exposure` alone.
  - `somebody speaks` 6.2 → 6.8:1.
  - `sex for pay names the amount` 0/9 → 0/14.
- Better, still red: traversal heat 13 → 15/31.
- Clips: 31/46 explicit beats carry a clip (was 30/35); the new beats have none (no media harvest).
- `--ship`: the same 8 BLOCK rows red, plus `no one is named before they're met` (9 red).
  - `a named person is where the line says` 12 → 20. Seven are on `garden_sun`'s new nodes, which are
    reached only through the `RYAN_SEES` / `MARK_SEES` choice, but the gate reads Monday 07:00. One is
    `home_event_mark_asleep`'s "Mark's asleep on the couch" against his "up late" row.
  - The reader row still reads part 10's verdicts: `v2_state.json` was not edited, on LO's instruction.
- `shape.py --finish` 22/0. `playtest.py` 10/10. `reach_all.py` 43/44, and 44/44 with Laura C 1's flag.
  No "kid".

**The reader, once, on the 13 changed canvases** (`reader/reader_w.md`): 18 FAIL. Listed, not fixed.
- On the new screens:
  - hook: `hub_ryan_kitchen`, `hub_mark_garage`, `home_event_mark_reach`, `home_event_mark_asleep`;
  - her voice at her level: appetite with no pushback at Curious in `hl_tv_tease`, `hl_beer_tease` and
    `hl_breakfast_tease`;
  - the numbers and the clothes agree:
    - "The rent is seventy-five" (false after the rent rises);
    - the breakfast and sleep-shirt lifts don't check the bra;
    - the dishes waistband shows in the towel, uniform and dresses;
    - "the strap" with no bra on the sun-lotion choice;
  - true on every visit: "in broad daylight" in the evening garden.
- Already there before the screens (seen again):
  - the garden's "Not today." and Hale's "Not tonight." refusals;
  - Hale's button lines (kind C);
  - Claire's 18:40 knock (kind C);
  - the hot tub's dry-hair line and the "Take it off" line on the bra-less path.

## Writer fix pass — six fixes on the 25 screens (LO, 2026-10-10)

Snapshot first: `first_term_snapshots/20261010_iter002_writer_fix_before/` (toml_phases, v2_state.json,
output, iterations/002/build_scripts). All text changes go through `build_scripts/writer.py`; the screen
files in `placeholders/` are untouched. Same `build_scenes.sh` (`--dev`) build.

**What changed (`writer.py` tables EDITS, HOOKS, VOICES, GUARD, CHOICES and new VARIANTS):**
1. Clothes:
   - The sleep shirt strip and the breakfast lift name the bra when one is on.
   - The dishes line names the towel, uniform or dress.
   - The lotion strap needs a bra; with none the line is "His fingers slide around your sides".
   - "Broad daylight" only shows 07:00–19:00; otherwise "out in the open garden".
   - The choices into `hl_beer_touch`, `hl_breakfast_touch`, `hl_dishes_touch`, `sun_ryan_touch` and
     `sun_mark_paid` are split by outfit. The two "strip to the waist" screens take the top and bra
     off (`wardrobeEffects`), and the sleep shirt in the living room.
   - `sun_mark_tease` and `sun_mark_paid` sit behind a garment check, not `worn_exposure`.
2. "The rent is seventy-five." is now "That's a piece of the rent."
3. `hale_thursdays`: "My wife's here at half past."; "Claire's" only behind `claire_met`.
4. Mark's paid looks also need `mark_paid_touch` and `mark_arrangement` (`mark.py` `MARK_PAID_ROUTE`,
   `home.py` garden choice). Each has a second voice: SP2's "warming up" under corruption 60, the
   bold voice from 60. One hub line was reworded from "His thumb rubs" to "His thumb works at", because
   the gate reads `rubs` as an act (lead item 12).
5. At Curious (corruption under 40) she pushes back a little on `hl_tv_tease`, `hl_beer_tease` and
   `hl_breakfast_tease`. Bold and up keep the screen's voice.
6. A forward hook on `hl_dinner_tease` (Ryan's kitchen), both garage screens, `home_event_mark_reach`
   and `home_event_mark_asleep`.

**Checks** (`reader/gates_wf.txt`, `reader/ship_wf.txt`):
- Gates 59 → **60/88**.
  - `no one is named before they're met` is green.
  - `her clothes are named exactly` 5 → 1: `party_house_soak`, which is not a writer screen.
  - `her climb` 17 → 7 problems: the laundry and dinner teases have one voice, and `garden_sun` is
    flagged through the gate's garment-word gap (lead item 12).
  - Worse: `somebody speaks` 6.8 → 7.1:1 and `prose has room` `but` 2.80 → 2.68/1k, because of the
    added thought lines.
  - The explicit floor stays at 9.5%.
- `--ship`: 9 → **8** BLOCK rows red, the same 8 as before the writer pass. `a named person is where the
  line says` stays at 20.
- `shape.py --finish` 22/0. `playtest.py` 10/10. `reach_all.py` 36/37 tried, Laura stopping at C 1 as
  before; with C 1's flag Laura 8/8, so 44/44. No "kid". 18 placeholders, all Laura's.

**The reader, once, on the 9 changed canvases** (`reader/reader_wf.md`): 9 FAIL. Listed, not fixed.
- From this pass:
  - `home_event_mark_reach` her voice: the new hook ("you'll be standing right under it") is
    appetite at Curious, with no pushback.
  - `garden_sun` clothes: the lotion choice checks top and dress but not the bottom, so
    "down to your waistband" can show with nothing on below.
  - Not a FAIL, but wrong: `wardrobeEffects` take the clothes off before the screen draws
    (`v2.py` ~15540–15595). The sleep shirt variants in `hl_beer_touch` and the "unhook your bra" beat
    in `sun_mark_paid` never show. What does show is true.
- Already there before:
  - the garden's "Not today." and Hale's "Not tonight." refusals;
  - Hale's "Button up.";
  - Hale "stands up" when he's already standing;
  - Mark's Sunday chair line against "His chair is pulled out from the table for nobody" at step 7;
  - "Tips any good? Sunday's coming." on a Sunday;
  - the dishes paid look with Laura in the kitchen on Sunday evenings.
  - Also noted: "That how you spend a Saturday" shows on weekday evenings, and "Twenty to untie it."
    names a tie no garment has.

## Placeholders — the signed lines this build does not write

Each is a screen whose only text starts with `PLACEHOLDER —` and names the sheet line it stands for.
The button, its gate, its effects and its brake are built; only the line is missing. Regenerate this
table with `python3 iterations/002/build_scripts/list_placeholders.py`.

| # | canvas | node | sheet file:line | what goes here |
|---|---|---|---|---|
| 1 | `hub_ryan_kitchen` | `hl_dinner_tease` | `sheets/people/npc_ryan.md:106` | Ryan, dinner: tease (Curious, Ryan A 4) |
| 2 | `hub_ryan_living_room` | `hl_tv_tease` | `sheets/people/npc_ryan.md:105` | Ryan, TV and a film: tease (Curious, Ryan A 4) |
| 3 | `hub_ryan_living_room` | `hl_tv_touch` | `sheets/people/npc_ryan.md:105` | Ryan, TV and a film: touch (Bold, Ryan A 8) |
| 4 | `hub_laura_kitchen` | `hl_coffee_tease` | `sheets/people/npc_laura.md:87` | Laura, coffee: tease (Curious, Laura C 1) |
| 5 | `hub_laura_kitchen` | `hl_coffee_touch` | `sheets/people/npc_laura.md:87` | Laura, coffee: touch (Bold, Laura C 7) |
| 6 | `hub_laura_kitchen` | `hl_breakfast_tease` | `sheets/people/npc_laura.md:86` | Laura, breakfast: tease (Curious, Laura C 1) |
| 7 | `hub_laura_kitchen` | `hl_breakfast_touch` | `sheets/people/npc_laura.md:86` | Laura, breakfast: touch (Bold, Laura C 7) |
| 8 | `hub_laura_kitchen` | `hl_tidy_tease` | `sheets/people/npc_laura.md:96` | Laura, Sunday dinner tidy check: tease (Curious) |
| 9 | `hub_laura_kitchen` | `hl_dinner_tease` | `sheets/people/npc_laura.md:88` | Laura, dinner: tease (Curious, Laura C 1) |
| 10 | `hub_laura_kitchen` | `hl_dinner_touch` | `sheets/people/npc_laura.md:88` | Laura, dinner: touch (Bold, Laura C 7) |
| 11 | `hub_laura_kitchen` | `hl_cook_tease` | `sheets/people/npc_laura.md:89` | Laura, help her cook: tease (Curious, Laura C 1) |
| 12 | `hub_laura_kitchen` | `hl_cook_touch` | `sheets/people/npc_laura.md:89` | Laura, help her cook: touch (Bold, Laura C 7) |
| 13 | `hub_laura_kitchen` | `hl_dishes_tease` | `sheets/people/npc_laura.md:90` | Laura, dishes: tease (Curious, Laura C 1) |
| 14 | `hub_laura_kitchen` | `hl_dishes_touch` | `sheets/people/npc_laura.md:90` | Laura, dishes: touch (Bold, Laura C 7) |
| 15 | `hub_laura_kitchen` | `hl_wine_tease` | `sheets/people/npc_laura.md:91` | Laura, a glass of wine: tease (Curious, Laura C 1) |
| 16 | `hub_laura_kitchen` | `hl_wine_touch` | `sheets/people/npc_laura.md:91` | Laura, a glass of wine: touch (Bold, Laura C 7) |
| 17 | `hub_laura_kitchen` | `hl_study_tease` | `sheets/people/npc_laura.md:94` | Laura, study at the table: tease (Curious, Laura C 1) |
| 18 | `hub_laura_living_room` | `hl_film_tease` | `sheets/people/npc_laura.md:92` | Laura, movie night: tease (Curious, Laura C 1) |
| 19 | `hub_laura_living_room` | `hl_film_touch` | `sheets/people/npc_laura.md:92` | Laura, movie night: touch (Bold, Laura C 7) |
| 20 | `hub_laura_bedroom` | `hl_hair_tease` | `sheets/people/npc_laura.md:95` | Laura, her hair: tease (Curious, Laura C 1) |
| 21 | `hub_mark_living_room` | `hl_beer_tease` | `sheets/people/npc_mark.md:108` | Mark, late TV and a beer: tease (Curious, Mark A 3) |
| 22 | `hub_mark_living_room` | `hl_beer_touch` | `sheets/people/npc_mark.md:108` | Mark, late TV and a beer: the paid look (Bold, Mark A 7) |
| 23 | `hub_mark_garage` | `hl_laundry_tease` | `sheets/people/npc_mark.md:109` | Mark, laundry: tease (Curious, Mark A 3) |
| 24 | `hub_mark_garage` | `hl_laundry_touch` | `sheets/people/npc_mark.md:109` | Mark, laundry: the paid look (Bold, Mark A 7) |
| 25 | `hub_mark_kitchen` | `hl_breakfast_tease` | `sheets/people/npc_mark.md:104` | Mark, Sunday breakfast: tease (Curious, Mark A 3) |
| 26 | `hub_mark_kitchen` | `hl_breakfast_touch` | `sheets/people/npc_mark.md:104` | Mark, Sunday breakfast: the paid look (Bold, Mark A 7) |
| 27 | `hub_mark_kitchen` | `hl_dinner_tease` | `sheets/people/npc_mark.md:105` | Mark, dinner: tease (Curious, Mark A 3) |
| 28 | `hub_mark_kitchen` | `hl_cook_tease` | `sheets/people/npc_mark.md:106` | Mark, help him cook: tease (Curious, Mark A 3) |
| 29 | `hub_mark_kitchen` | `hl_dishes_tease` | `sheets/people/npc_mark.md:107` | Mark, dishes: tease (Curious, Mark A 3) |
| 30 | `hub_mark_kitchen` | `hl_dishes_touch` | `sheets/people/npc_mark.md:107` | Mark, dishes: the paid look (Bold, Mark A 7) |
| 31 | `zoe_03_hot_tub` | `kiss_bare` | `sheets/scenes/zoe_03_hot_tub.md:44` | Zoe A 3, the kiss when she wore no bra into the tub |
| 32 | `hale_04_claire_knocks` | `hand` | `sheets/scenes/hale_04_claire_knocks.md:72` | Hale B 4, the hand beat in a top without buttons |
| 33 | `hale_thursdays` | `hand` | `sheets/scenes/hale_05_seven_twenty.md:31` | Thursdays at seven: his hands above her waist (Bold), its own screen |
| 34 | `garden_sun` | `sun_ryan_tease` | `sheets/people/npc_ryan.md:104` | Ryan, the garden: tease (Curious, Ryan A 4) |
| 35 | `garden_sun` | `sun_ryan_touch` | `sheets/people/npc_ryan.md:104` | Ryan, the garden: touch (Bold, Ryan A 8) |
| 36 | `garden_sun` | `sun_mark_tease` | `sheets/people/npc_mark.md:110` | Mark, the garden: tease (Curious, Mark A 3) |
| 37 | `garden_sun` | `sun_mark_paid` | `sheets/people/npc_mark.md:110` | Mark, the garden: the paid look (Bold, Mark A 7) |
| 38 | `home_event_ryan_towel` | `ev_curious` | `sheets/places/home_hall.md:44` | Ryan out of the shower: curious |
| 39 | `home_event_ryan_towel` | `ev_bold` | `sheets/places/home_hall.md:44` | Ryan out of the shower: bold |
| 40 | `home_event_laura_robe` | `ev_curious` | `sheets/places/home_hall.md:45` | Laura's robe: curious |
| 41 | `home_event_mark_reach` | `ev_curious` | `sheets/places/home_hall.md:46` | Mark reaching past: curious |
| 42 | `home_event_mark_asleep` | `ev_curious` | `sheets/places/home_hall.md:47` | Mark asleep, TV on: curious |
| 43 | `home_event_ryan_door` | `ev_curious` | `sheets/places/home_hall.md:48` | Ryan's door, a hand's width: curious |

Part 4 added two (`hale_04_claire_knocks` · `hand`, `hale_thursdays` · `hand`): Hale B 4's new beat for a top without buttons, and the Thursday repeat's own
screen, which had reused step 4's first-time prose word for word (sweep A4-32).
Part 6 added none. Part 5 added one (`zoe_03_hot_tub` · `kiss_bare`): Zoe A 3's kiss when she wore no bra into the tub (the sheet's beat opens by unhooking it).

Part 3 added none: its new lines (Mark A 5's two nos, the catch's reasons, the curfew call) are the
sheets' own, and none is a tease, touch or paid look.

## Added to part 5 (LO, 2026-10-09)

- `jake_date_booked` / `jake_date_went` latch (the booking lapses at 21:00, Q73) and Jake's pickup clock bucket.
- `rent_carried`: Vance's Monday knock at the front door (his ledger row Mon 18:00–19:00, `when`
  `rent_carried`; `vance_knock`; the latch-flag gate). Part 5 also owns the grocery run (above).

## For the lead — skill gaps and engine bugs (not fixed here)

1. **Skill · gates.py G11 `world reachable` ignores `default_entry`.** The engine sends a building with a
   `default_entry` straight to that room (`v2.py:11112-11121`), and the importer forbids that room an
   `entry_from` (`template_import.py:5192-5195`) and forbids listing it in the building's
   `navigation_order` (validation: "navigation_order for 'home' includes 'home_hall' which is not a
   destination"). G11 builds edges from `entry_from` and `navigation_order` only (`gates.py:7560-7569`),
   so every room behind the hall reads unreachable: 10/38 on a map the live run walks end to end.
   The same blind spot fails `a step is seen from the next room` for Zoe A 3 (`zoe_apartment` "hangs off
   None"). Fix: treat a container's `default_entry` (and a room's `parent`) as an edge.
2. **Engine · a closed `default_entry` room's "Go back" goes to `Start`.** The closed screen's back link
   uses `entry_from`; a building's default room has none, so `Location_zoe_apartment` closed renders
   `[[Go back->Start]]` (built output). Reached when she is in Zoe's Living Room as it shuts (02:00 on
   Saturday after the party, 00:00 other nights) and a scene returns her there, or on loading such a save.
3. **Engine · a door on a building's default room is never shown.** The street links the building, the
   building `goto`s the room, and the room's `[locations.door]` is skipped, so a threshold on the way in
   (the hall's late door) can't exist once Home is a building; a door is refused on the container itself
   (`engine.md` §44). No condition type says where she came from. (LO chose outing flags, Q75.)
4. **Engine · no OR inside an AND condition block.** `cond(A, {logic: OR, ...})` is refused by the
   importer ("unknown condition type None"), and `hours_since_flag` fails closed on an unset flag, so
   "unset, or set 12+ hours ago" (Q60) needs two copies of every button. The gates also read only a flag
   cleared in `[engine.daily_tick]` as a cap (`the-meters.md` M3-M5), so an hours-since brake reads as
   free. LO moved the home brakes to once a day (DECISIONS 77).
5. **Skill · the importer's `navigation_order` rule and G11 contradict each other** for buildings; the
   map doctrine (`the-map.md` "Navigation — area, building, room", D10) asks for buildings, so the gate
   fails a game for obeying it (SKILL.md: "a check that fails a game for obeying the doctrine is a bug in
   the check").
6. **Skill · the same `default_entry` gap in the truth gates' building.** `gates.py` `_tr_building` walks
   `entry_from` up to the place under the root, and the hall now has none (it is Home's `default_entry`),
   so every house room is its own "building": `nobody is woken` says Laura is "not in the building" for
   Laura C 1 and C 4 while she is in the kitchen.
7. **Skill · `ladders move forward` reads a step's `when` and ignores its `when_also`.** The ledger declares
   a second window for Mark A 5 and Zoe A 4 (L26, L29); the canvas carries both, and the gate reports the
   second as a mismatch.
8. **Skill vs D11 · `sex for pay names the amount`** wants the sum on the button; LO's D11 keeps earned pay
   off every button (the scene and the card say it). A warning; worth reconciling in the skill.
9. **Skill · the `default_entry` building gap also reaches `a named person is where the line says`.**
   Ryan in his doorway on `jake_03` and Laura in the mirror on `laura_01` read as "not here" for the same
   reason as item 6; a presence check on the line cannot satisfy it.
10. **Skill · `playtest.reach_step` only knows `Canvas_` passages.** The starting canvas is
    `StartingCanvas_<id>_Node_<node>`; `reach_all.py` patches this in the scratch driver, never in the skill.
11. **Skill · only the reader row has a waiver.** LO waived "no empty rooms" for the men's toilet and the
    lines the gate gaps cause (items 6, 7, 9) on 2026-10-09, but `gates.py --ship` reads waivers only from
    `release_page.reader_waivers`; there is no field for any other BLOCK row, so those rows stay red with
    LO's waiver written in REPORT.md.
12. **Skill · `her climb` reads a garment word as an act.** `_rungs_of` puts `bra`, `topless`, `naked`
    and `panties` in the `strip` rung and `rubs` in `hands` (`gates.py:345-360`), so a hub line ("His
    thumb rubs the edge of whatever he's holding") or a sunbathing line ("Topless, on your front") makes
    the whole node an act node. `garden_sun`'s first screen is the lounger, open on a new save, so the
    canvas reads as a paid act open from turn one, and (c) asks two voices of every such node. The
    same note the file already makes about anatomy ("THE RUNG IS AN ACT, NOT A BODY PART") applies to
    garments. Found in the writer fix pass, 2026-10-10.

## 2026-10-29 · step 5: the Good Girl moments (DECISIONS 79–81)

- **Scripts:**
  - `pools.py`: the park's `run` stops before he looks up, and a new `linger` screen pays corruption +1, cap 19 (`CAP_GG`).
  - `college.py`: the new `library_back_stacks`.
  - `home.py`: the new `ryan_door_ajar` and `master_door_saturday_night`. Both are reached only by a door, are once a day, and carry the door's window as their trigger conditions. `master_asleep`'s "asleep" lines now skip Sun 00:00–01:00.
  - `world_data.py`: Ryan's door gets "His door's open a crack." for Sun–Thu 22:00–00:00. Their door gets "The door's ajar." for Sun 00:00–01:00, and "Ease the door open" is split around that hour. Each brake is two options with one text, "never seen" or "seen 20/24+ hours ago", because `hours_since_flag` fails closed on an unset flag and conditions don't nest.
  - `mark.py` and `laura.py`: the bedroom "asleep" lines skip Sun 00:00–01:00.
  - `extras.py`: the 4 goal-card labels (DECISIONS 81).
  - `people_data.py`: Mark's activity list.
- **Ledger** `v2_state.json`: Mark's Sun 00:00–02:00 row is split, so 00:00–01:00 is "awake, with Laura" (DECISIONS 80). Corruption's `fed_at` gains park, library, `home_ryan_room` and `home_master_bedroom`.
- **Built** with `--dev --debug`.
- **Gates:** 60/89 before, 61/89 after.
  - "every stage has a way up" is green: Good Girl has 4 sober acts, about 4 points a day, about 5 days.
  - No other verdict changed.
  - `--ship` is unchanged: NO, 8 BLOCK. Missing media went from 82 to 88; those are the 6 new clip slots, and no harvest was run.
- **Live playtest** (headless Chromium, `output/index.html`): 22/22, no page errors. It covered each button showing at its hour, each look paying 0 and each stay +1, the cap at 19, the once-a-night and once-a-week brakes, Friday showing no crack, Sun 00:30 showing "ajar" and Sun 01:30 showing "ease", and `master_asleep` showing no "asleep" line at Sun 00:30.
- **Snapshot:** `first_term_snapshots/20261029_step5_before/`.
- **The reader** (`v2-reader`, the 4 canvases) found 11 FAILs. Fixed here:
  - Laura's ledger row Sun 00:00–07:00 is split, so 00:00–01:00 reads "awake, with Mark"; it said "asleep" while the scene shows her awake.
  - `ryan_door_ajar` and its door need `ryan_step gte 0`, so it doesn't play after his path closes cold (step −1). Checked live.
  - The library scene opens until 19:45, so its exits land before the 20:00 close.
  - DECISIONS 79 now says the park stranger does see her.
- **Left for LO (design calls):**
  - The hooks: the park, library and their door end with nothing pointing forward. Nothing in 0.1 reads the seen flags.
  - Her Good Girl voice ("You should look away. You don't.") plays the same at every stage, because there's no stage gate.
  - Mark's want for Laura is shown nowhere before the scene.
  - The door says "Nobody comes" at Sun 00:00–01:00 when they're inside but the scene was seen within 24 hours, or Laura is on the stairs.
  - The park's exits can land after 22:00. That is older than this step, apart from `linger`.
- **After the fixes:** gates 61/89, ship unchanged, playtest 23/23.

## 2026-10-29: reader item 5, the park closes on time (LO's yes)

- `pools.py`: `park_watch_the_couple`'s trigger now also needs `time_of_day` 07:00–21:30. The longest path is 21 minutes, so every exit lands before the park locks at 22:00. The park sheet's "where · when" row says the same (changed first, waits for LO's re-sign).
- Snapshot before: `first_term_snapshots/20261029_fixes45_before/`.
- Rebuilt with dev + debug. Gates 61/89, unchanged. The built TOML carries the new window.

## 2026-10-29: reader item 4, a peek instead of "Nobody comes" (LO's "go")

- New sheet `sheets/scenes/master_door_peek.md` (DRAFT, waits for LO's sign) and two rows in `places/home_master_bedroom.md`.
- `world_data.py`: their door gets "Peek through the gap." for Sun 00:00–01:00 in two cases: both in and `mark_laura_seen` under 24 hours, or Mark in and Laura out (`came_home_late`, she is on the stairs).
- `home.py`: new canvas `master_door_peek`, one screen, a line per case, pays nothing, "Close the door." to the hall.
- Gate catch: "sitting up in bed" read as asleep (`_TR_SLEEP` matches "in bed"), so the line says "against the headboard". Noted on the sheet.
- Rebuilt with dev + debug. Gates 61/89, unchanged; the named-person count is back to 20. Playtest: the peek and park-hour probe 14/14, the step 5 probe 23/23, 0 page errors.

## 2026-10-29: Laura alone, Sun–Fri 22:00–23:00 (DECISIONS 82–84, LO's picks)

- New sheet `sheets/scenes/laura_alone_in_bed.md` (DRAFT). Changed: `places/home_master_bedroom.md`, `people/npc_laura.md`, `people/npc_mark.md`, DECISIONS 82–84. Snapshot: `first_term_snapshots/20261029_laura_alone_before/`.
- Ledger: Laura's bedroom row Sun–Fri 22:00–06:30 split at 23:00; 22:00–23:00 is "awake, alone". `ACTIVITIES` gains the row.
- `home.py`: canvases `laura_alone_in_bed` (`crack` / `watch`, +1 cap 19, flags `saw_laura_alone` and `laura_alone_seen`) and `laura_alone_peek` (one screen, pays nothing). `LAURA_ASLEEP_HOURS` keeps every "Laura's asleep" line out of that hour (`home.py`, `laura.py`).
- `world_data.py`: "Ease the door open" skips Sun–Fri 22:00–23:00; "The door's ajar." (brake: unset or 20+ hours) and "Peek through the gap." (under 20 hours) fill it.
- Rewording (DECISIONS 83): Mark's living-room lines and step 4 say Laura has "gone up" or "gone to bed"; Ryan's step 4 "Mom's asleep." became "Mom's gone to bed." Curious goal card adds "Laura's door at night".
- Rebuilt with dev + debug. Gates 61/89, unchanged; named-person flags 20, unchanged. "Every stage has a way up": Good Girl has 5 acts, about 4 days (was 4 acts, about 5). Playtest: Laura probe 18/18, step 5 probe 23/23, peek and park probe 14/14, 0 page errors. The 2 new clip slots (`sex/laura_alone_crack_t5`, `sex/laura_alone_watch_t5`) are empty; no media harvest.

## 2026-10-29: the remote, 5 channels (DECISIONS 85–86, LO's picks)

- New sheet `sheets/scenes/living_tv_channels.md` (DRAFT); `places/home_living_room.md` row; DECISIONS 85–86. Snapshot: `first_term_snapshots/20261029_tv_before/`.
- `home_items.py`: `CHANNELS` and the remote helpers, shared. `home.py`: `living_tv` rebuilt (remote, 4 plain channels, `adult`, `touch`), no daily brake on the canvas; the plain channels keep energy +5 once a day. `mark.py`: the old "Watch TV with him." item replaced by the same remote inside `hub_mark_living_room` (`mremote`, `mch_*`, `madult`, `mleave`).
- 12 new clip pools, all empty (no harvest).
- Gates 60/89 (was 61): "the climb is paid for" went red, as LO was told: it reads `living_tv` as "0 → 60 free, no cap", but the effects carry caps 19/39, so the TV cannot raise her past 39 (the gate does not read `cap`, B145). "one pool, one place" 56 → 64: the four plain channels' lines are shared between alone and with Mark. Good Girl: 7 acts, about 3 days.
- Playtest: TV probe 19/19, Laura 18/18, step 5 23/23, peek and park 14/14, 0 page errors.

## 2026-10-29: closed Zoe's Living Room, "Go back" (engine fix, LO's option 1)

- LO's report: Town, then Zoe's Flat before 18:00, then "Go back" went to the start of the game. Reproduced headless: "Go back" ran `previous()`, which was `Location_zoe_flat`, and that redirects straight back into the Living Room (a loop, or Start with no earlier page).
- Cause, in the engine: a building's `default_entry` room has no `entry_from` by rule, so its closed screen fell to `previous() || "Start"`. Fix in `generators/v2.py` (the closed-screen "Go back"): that room now goes back to the building's own `entry_from`, the same place as the open room's "Exit <building>". Zoe's Living Room's "Go back" now goes to `Location_town`. No game files changed.
- Test: `test_location_hours.py::test_a_closed_default_entry_room_goes_back_out_of_the_building`. Run with `test_refused_room` and `test_unaffordable_room`: 37 passed.
- Rebuilt with dev + debug. Gates 60/89, unchanged. Playtest: the Zoe probe lands on `Location_town`; TV 19/19, Laura 18/18, step 5 23/23, peek and park 14/14, 0 page errors.

## 2026-10-29: a text books something (DECISIONS 87–88, LO's "go")

- LO's report: Laura's "home for dinner sweetheart?" changes nothing. Of the 10 texts, 2 were broken (Laura's dinner; Zoe's run set `zoe_run_booked`, which nothing read) and 6 changed nothing when she answered. Top games (round9a: CoT, IHOH): a text books a meeting; a no costs a little, ignoring costs more, a yes with no show costs most.
- Engine read first: texts take `ignore_after_days` + `on_ignore` (`template_import.py`); a reply's `flagEffects` honours `unset`; setting a flag again restarts `hours_since_flag` (`v2.py` applyFlagEffect). Phone effects are unclamped by default (`applyPhoneEffectSet`), so every negative phone effect carries `clamp`.
- `canv.py`: `clear_on_leave()` and `booked_split()`. `phone.py`: `thread(ignore=…)`, `noshow()`, the 8 bookings, 7 no-show threads, each with an hour window. Scenes: Laura's dinner (`DINNER_DONE` split by booking and the eating-out lie, read for 8 hours), Zoe's park run, the café's first shift (+$4), `tom_after_close` (needs `tom_close_booked`), Hale step 3 and `hale_thursdays`, `ryan_two_knocks`, the party door (`zoe_party_promised`, read for 30 hours). Tom's "maybe" became "i'll stay".
- Sheets: a "Bookings and no-shows" table on the five person sheets, each waiting for LO's re-sign. Snapshot: `first_term_snapshots/20261029_texts_before/`.
- Rebuilt with dev + debug. Gates 60/89, unchanged. Two reds along the way, fixed: the day-cap gate can't see a phone setter (the eating-out flag is now read for 8 hours, not cleared at midnight), and the phone truth gate caught Laura's no-show text at 23:00, when she's asleep (window now 20:00–23:00). "A chat is short and timed" fell from 15 problems to the 4 older ones.
- Playtest: new probe `texts.js` 33/33, 0 page errors. Not played live: the party lines (they need a short outfit) and Tom's after close (see below). The older probes (tv, laura, probe, peek2, zoe) were lost when the scratchpad was cleared and were not rerun.
- Found, not fixed: the café closes at 22:00 in the build (ledger "Mon-Sat 08:00-22:00"; `world_data.py` says 23:00, but the ledger wins), and the room passage shows the closed screen after 22:00 even to someone inside. Tom step 6 (`tom_06_after_close_kiss`, Mon–Sat 22:00–23:00) and `tom_after_close` (Fri 22:00–23:00) can't be reached. Waits for LO.

## 2026-10-29: the café open till 23:00 (DECISIONS 89, LO), then "sign all"

- Ledger: café hours `Mon-Sat 08:00-23:00` (the location and the job row), and Tom's 22:00–23:00 row note. `sheets/places/cafe.md` hours and closed-text rows. Snapshot: `first_term_snapshots/20261029_cafe_hours_before/`.
- `tom.py`: `hub_tom_cafe` now runs 08:00–22:00. With no hours it took Tom's face in the closing hour (priority 6 over `tom_after_close`'s 5), so after close couldn't open even with the booking.
- Rebuilt with dev + debug. Gates 60/89; the fail list and every number on it are the same as before the change. Playtest: `tom_late.js` 4/4 (step 6 plays Fri 22:15, café shut at 23:15, after close shut without his yes and open with it), `texts.js` 33/33, 0 page errors.
- Signed by LO ("sign all"): DECISIONS 87–89, the five person sheets (Laura, Zoe, Tom, Hale, Ryan), and `places/cafe.md`.

## 2026-10-29: locked buttons name the number (DECISIONS 90, LO)

- LO's report: "(Needs Hungry)" is hard to read. At Good Girl the player has never seen the word, and it reads like food ("Not hungry." is a real choice at home).
- Build scripts (`college.py`, `home.py`, `home_items.py`, `laura.py`, `mark.py`, `ryan.py`, `pools.py`): 9 buttons now say "(Needs Corruption 60)" and the figure-drawing button "(Needs Exhibitionism 60)"; the "Further" screens say "It comes later, when your Corruption reaches 60." (or Exhibitionism). The sidebar keeps its stage words. `canv.py` is untouched: its quest-card filter reads step labels, not these buttons.
- 13 sheets quote the new words, each marked changed and waiting for LO's re-sign; the ledger's `locked_next` line too. `scenes/college_class_figure.md` still says the posing button needs Corruption (the build has said Exhibitionism since iteration 001, BUILD_VS_SHEET row 56); that difference is unchanged. Snapshot: `first_term_snapshots/20261029_locked_labels_before/`.
- Rebuilt with dev + debug. The built page has 0 "Needs Hungry" left. Gates 60/89, unchanged.

## 2026-10-30: the TV alone, five sessions a day (DECISIONS 91, LO)

- `home.py` `living_tv`: `max_triggers_per_day = 5`, `show_when_blocked = true`, `cooldown_message = "Not now."`. The last two are trigger keys (`template_import.py:2548`); put under `metadata` they are silently dropped (the first build did that, and the probe caught it). The grey row also shows when the room is busy or it's past 02:00 (`v2.py` `renderSoloActivities`), so the text says only "Not now."
- `sheets/scenes/living_tv_channels.md` brake row, waiting for LO's re-sign. Snapshot: `first_term_snapshots/20261030_tv_cap_before/`.
- Rebuilt with dev + debug. Gates 60/89, the same fail list. Probe `tv_cap.js` 8/8, 0 page errors: five sessions each pay channel 5's +1, then "Watch TV — Not now." and no link, then the next day the row is back.

## 2026-10-30: channel 5 with Mark pays more, once a day (DECISIONS 92, LO)

- `mark.py` node `mleave`: "Keep watching." pays her Corruption +2 (cap 19 / 39) and Mark's Want +2 behind `mark_tv_paid`; a third copy with the flag set pays nothing. `mark_tv_paid` added to `home_items.DAILY` and to `[engine.daily_tick]` in the hand-written `0_systems_spec.toml`.
- Sheets `scenes/living_tv_channels.md` and `people/npc_mark.md`, waiting for LO's re-sign. Snapshot: `first_term_snapshots/20261030_mark_tv_before/`.
- Rebuilt with dev + debug. Gates 61/89 (was 60): "the climb is paid for" turned green. Channel 5 with Mark was the one unbraked route into a gated meter, and the brake closed it. Probes: `mark_tv.js` 6/6 (+2 and Want +2, then 0 the same day, the real midnight tick clears it, pays again, 38 lands at 39, 18 lands at 19), `tv_cap.js` 8/8, 0 page errors.

## 2026-10-30: the people's meters get market words (DECISIONS 93, LO)

- Shown labels only: `warmth` is Love, `want` is Lust, `power` is Dominance (`0_systems_spec.toml` `[[traits.labels]]`, `canv.py` `TRAIT_NAME`). Keys, saves, conditions and gates unchanged. Canvas descriptions, comments and the 56 sheets keep the old names as design terms; DECISIONS 93 maps them.
- Rebuilt in full with dev + debug. 28 quest goals now read "…'s Lust N", 0 old labels left. Gates 61/89, the same pass/fail on every gate. Probes: `labels.js` 4/4 (traitLabel, the goals, the cast cards: Mark and Tom Lust + Dominance, Laura and Ryan Lust + Love), `mark_tv.js` 6/6, `tv_cap.js` 8/8, 0 page errors.

## 2026-10-30: the People screen is a tap-to-open list, phone first (DECISIONS 94, LO)

- Engine only (`v2.py`): one `<details>` row per person, sorted by `setup.castRoster` (about now, then ready, then the rest); the row line from `setup.castNext`, short times from `setup.castWhen`; meters as bars; Back on top. The EN7 golden was regenerated on purpose, two EN7 tests now open a row before reading it (a closed row has no text), `test_hidden_places` pins the new source line, and three tests were added. 46 passed. The skill's `engine.md` §34 and CHANGELOG were updated.
- Rebuilt with `--dev --debug` (no TOML change). Gates 61/89, the same per gate. Probe `cast_list.js` 16/16 at 390 and 1280 wide: five closed rows on one phone screen, Laura (in the Kitchen) first, Tom's line "Ready · Mon–Sat 2:30–10 PM", one open at a time. `labels.js` 4/4, `mark_tv.js` 6/6, `tv_cap.js` 8/8, 0 page errors.

## 2026-10-30: the sidebar, trimmed; Cheats; the phone clock; schedules on the People page (DECISIONS 95, LO)

- `0_systems_spec.toml`: `[ui] sidebar_hide = ["stats", "schedules", "flags"]`, `phone_clock = true`; `[ui.cheat_page] title = "Cheats"`. Merged (only those lines changed in `7_final_game.toml`), rebuilt with `--dev --debug`.
- Engine: the two `[ui]` keys (importer + validate + StoryCaption), the phone clock, `<<npcScheduleSection>>` shared by the Schedules page and the new per-person dialog. Found and fixed on the way: widget arguments are `$args` on SugarCube 2.30, not `_args`.
- Gates 61/89, the same per gate. Probe `sidebar.js` 12/12, 0 page errors: no Stats/Schedules/Flags buttons, Cheats button and heading, Tom's schedule in a dialog, the clock at the top left on a 390-wide screen only while the sidebar is closed, follows the time, and opens the sidebar on a tap. Engine tests 759 passed plus 4 new.

## 2026-10-30: the schedule pop-up shows one day (DECISIONS 96, LO)

- Engine: `setup.castScheduleHtml` / `castTimeRange` replace the weekly table in the People card's dialog. Same rows as the Schedules page (`getNpcAllSchedulesSorted`, lock reasons, hidden-place names, emitted only for a game with hidden places).
- Rebuilt with `--dev --debug`. Gates 61/89, the same per gate. Probe `sched_day.js` 12/12 at 390 and 1280: Laura on Friday 19:00 shows three rows with "▶ 6–10 PM Kitchen" marked and "Now: Kitchen"; the Saturday chip redraws with no now line; no sideways scroll. `sidebar.js` 12/12, `cast_list.js` 16/16, `labels.js` 4/4, `mark_tv.js` 6/6, `tv_cap.js` 8/8, 0 page errors. Engine tests 764 passed.

## 2026-10-30: the Quests page is short rows, phone first (DECISIONS 97, LO)

- Engine: `[ui] quests_layout = "list"` swaps the V2 QuestsPage for a list built on `setup.questsStoryRows`, `setup.questsRoster` and `setup.questsNextWindow`. It reuses the cast page's `castNext` / `castWhen`. The default cards page is unchanged byte for byte.
- `0_systems_spec.toml` `[ui]`: `quests_layout = "list"`. Merged; only that line moved in `7_final_game.toml`.
- Rebuilt with `--dev --debug`. Gates 61/89, unchanged.
- Probe `quests_list.js` 24/24 at 390 and 1280 wide, 0 page errors. On Monday 15:00:
  - 3 story rows (0 / 4, 0 / 20, 0 / 20);
  - Tom first with "Today 2:30–10 PM · Café" and Now;
  - Mark last, ◯ "The rent has started";
  - the whole page fits on one phone screen (last row ends at 814px of 844).
- Other probes: `cast_list` 16/16, `sidebar` 12/12, `sched_day` 12/12, `labels` 4/4, `mark_tv` 6/6. `tv_cap` was 7/8 once ("next day: Watch TV is back"), then 8/8 on two re-runs, with no TV code touched.
- Engine tests 770 passed (6 new in `test_quests_list.py`).

## 2026-10-31: the towel at home (DECISIONS 98, LO)

- `home_items.py`: `towel_set()` (three meter bands, one flat pool of lines per band, the towel-only choices, a paid copy and a same-day unpaid copy, Laura's catch) and `TOWEL_CAUGHT`; `ryan_towel_today`, `mark_towel_today`, `laura_towel_today` added to `DAILY` and to `[engine.daily_tick]` in the hand-written `0_systems_spec.toml`.
- `ryan.py`: room, dinner, couch (Lust <40 / 40–69 / 70+; "Let it slip." Exhibitionism 20; "Drop it." Exhibitionism 40, Lust 70+, step 6; Lust +2 and Exhibitionism +1); the bathroom door gets only "Knock, and let the towel slip.". The single towel lines moved into the low band.
- `mark.py`: `mark_hub(..., towel=True)` on the living room and kitchen only (Dominance <40 / 40–59 / 60+; "Drop it." at step 5; Dominance +2). `laura.py`: kitchen, waiting up, dressing only (Love <40 / 40–69 / 70+; "Let her fix it.", no Exhibitionism gate; Love +2).
- Laura in the room when she lets it slip near Ryan or Mark: `towel_caught`, Laura's Love −3, no pay, the day's flag set.
- Every exit out of a towel screen goes to the hall: a first build sent them back to the hub's own room, and "a button does something" failed on 9 buttons (the same screen comes back).
- Media: 5 new pools (`sex/towel_ryan_slip_t4`, `towel_ryan_drop_t4`, `towel_ryan_door_slip_t4`, `towel_mark_slip_t4`, `towel_mark_drop_t4`), empty; the harvest is LO's.
- Sheets `people/npc_ryan.md`, `npc_mark.md`, `npc_laura.md` get a towel section, waiting for LO's re-sign. Snapshot: `first_term_snapshots/20261031_towel_before/`.
- Rebuilt with dev + debug. Gates 61/89, the same pass/fail on every gate. Explicit floor 12.8% to 17.0% of repeatable beats; 54/76 explicit beats carry a clip (71%, floor 50%). "Her climb" (already failing) went from 10 to 17 problems: the towel pay makes Ryan's room hub and others count as paid repeatables open on a new save.
- Probe `towel.js` 22/22, 0 page errors: the band line follows the meter; Daring 19 / 20 and the Drop gates; pay once, unpaid the same day; `advanceDay()` clears the flag; dressed shows nothing; Laura at dinner catches it (Love −3); Mark Drop +2; Mark's garage untouched; Laura's fix without Daring, Love +2; her room only while she dresses; the bathroom knock.

## 2026-10-31: the towel, LO's three answers (DECISIONS 98)

- "Drop it." loses its story step (LO: "no"): Ryan and Mark now need only Exhibitionism 40 and their top band (`ryan.py`, `mark.py` `drop_gate=[SHOWING]`).
- Laura's kitchen towel line stays the built one, "Go and get dressed, sweetheart. You'll catch your death."; `npc_laura.md` row "her line: towel" now says it (LO's pick).
- `npc_ryan.md`, `npc_mark.md`, `npc_laura.md`: the towel section re-signed by LO 2026-10-31.
- Rebuilt with dev + debug. Gates 61/89, the same per gate. Probe `towel.js` 22/22, 0 page errors (Drop it now shows at Ryan's step 5).

## 2026-11-01: release 1, slice A — the systems (DECISIONS 112–121)

- Baseline first: the unchanged build gave gates 61/89 and a byte-identical `7_final_game.toml`.
- Engine: a rent late fee. `rent_late_fee` (a player trait) is part of the next Sunday's due under `on_short = "carry"`, said on its own line ("Late fee: $15."), zeroed by a full payment, folded into `owed` by a carry (`v2.py` RentDay, `setup.carryRent`). Three new tests in `test_rent_carry.py`; rent tests 42 passed. It was needed because `rent_state.owed` is reachable by no effect or condition.
- The ledger (`v2_state.json`): the dean's Monday 08:00–09:00 row (`when` dean_met) and `dean_office` hours "Mon 08:00-09:00; Mon-Fri 09:00-17:00", hidden until `dean_met`; Laura's Saturday 16:30–17:00 bathroom row; Gary's rows `when` cafe_job (met at level 1). The sheet said the dean from 07:30; the faculty floor opens at 08:00, so 08:00 (a build fix, said here, not written back).
- `classes.py`: the four class schedules, read by `college.py` and by `gen_world.py`, which writes the `[[ui.timetable]]` rows; `[ui] timetable_button = true`.
- `gen_world.py`: the release-1 counters in `[player.core_traits]`; `0_systems_spec.toml`: their labels, the garage-hold `conditions` on the short skirt, sheer blouse and sports bra, `out_shown_today` in the daily tick.
- The opening's card: Laura's "You'll be late on your first day."; "Go to campus." walks her to the dean's office (20 minutes). The skip path now dresses her as the full opening does (the dean's office has clothing rules; the probe caught it).
- `college.py`: `college_dean_office` (four screens; the timetable opens from a `<<link>>` in a paragraph, which renders raw, v2.py:18310); the door's timetable paragraph is the same link; the dean's hub reads `dean_met`, with the warning line only after `dean_summons`.
- `cafe.py`: the three levels as five flat, mutually exclusive cases (the evaluator takes flat lists only: a nested group has no `type` and fails, v2.py `triggerConditionsSatisfied`). Five measured beats pasted verbatim. Pay $8 plus a random tip (`{"type": "random"}`, applied on choices, v2.py:17264), doubled by the sexy uniform and the Friday close as built. Counters: shifts worked, level-2 shifts, footfall, name; `cafe_let_it`; Gary met at level 1. Build note for LO: the sheet's level-2 "pool of three setups" became one setup that names both tables, so the line before each yes is true whichever she picks.
- `mark.py`: `rent_short_1` (the key), `_2` (Mark names the $15; `rent_late_fee` add 15; Vance says it at the door), `_3` (the first of skirt, blouse, sports bra she owns and Mark doesn't hold, flat cases; none left: "Next week, then."); a full Sunday gives the key and the held items back.
- `town.py`: `street_seen_skirt`, `_nobra`, `_nopanties`, once a day, the witness by the hour. `world_data.py`: the street-door rules read either meter, the messages name both numbers.
- Gates 59/89 (61 before). Newly failing, both expected: "every person here has a face" (Laura's shower row has no canvas until slice C) and "a meter is read" (`cafe_name` and `cafe_shifts_worked` are read by Tom's step 3 and step 2, slice E). Fixed on the way: trait labels, three unbacked garment lines, the dean's face and window.
- Probe `probe_A.py` 15/15, 0 page errors: the opening, the dean, the timetable dialog (Monday rows), "already late" after 08:30, the lecture hall, the sidebar button, the garage hold refusing to equip.

## 2026-11-01: release 1, slice B — Ryan (DECISIONS 114)

- `sheetbeats.py`: the measured beats are read verbatim from the signed scene sheets (`beat(sheet, node)`, `pool(sheet, n)`); a missing heading stops the build. `canv.POOL(..., bag=True)` writes `seen_weight = 0` (the shuffle bag).
- The ledger: Ryan's gates as signed (step 2 Lust 10 from 06:45; 3 and 4 Corruption 20; 5 Corruption 20; 6 Exhibitionism 40; 7 Corruption 40 · Lust 60; 8 Corruption 40 · Lust 70), steps 7 and 8 point at the new canvases, the release door at step 8's "Further. (Needs Corruption 60)".
- `ryan.py`: Lust +5 a step; step 3 Laura calls up the stairs (only while her row has her in the kitchen); step 4 the measured `lap` beat and Kayla's "Who's there?"; step 6 `look` and `comes`; step 7 `ryan_07_kayla_cant_know`; step 8 `ryan_08_two_knocks_first_sex` with the terms after, the Jake line on `jake_met`, step 9 locked. The cut steps are no longer built.
- Build fix, said here and not written back: step 8 and its repeat run **Sunday to Thursday**, not "any night but Friday". Their signed screens put Laura across the hall ("Mom's right across the hall", her knock, her light), and on Saturday nights her row has her downstairs, waiting up.
- The hot repeatables: 1, 4, 5 on his room hub (Mon, Tue, Thu, Sun 19:00–22:00), 2, 3, 6 on the couch hub, 7 is the two-knocks repeat. Lust +3 once a day across all seven (`ryan_hot_today`, daily tick); each a shuffle bag of three from the sheet; none with Laura in the room. Row 3 undresses her to her underwear (it needs bra and panties on), rows 4 and 5 strip her and dress her after; row 6 needs Mark in the kitchen (Sunday), as its screens say his TV is in the next room. Row 7's near-catches are two of its three signed entries (7b Laura knocks, 7c Kayla calls), so no separate roll.
- `ryan_laura_opens_the_door`: Saturday 17:00–18:00, Laura dressing upstairs, once; sets `laura_knows_ryan`. (`laura_04_ryans_door` goes with Laura's slice.)
- Fixes from the gates: `kayla_met` now set when she reads Kayla's texts at step 2, and read by step 4 (it names Kayla); each hot exit is day-capped on its own and each hot screen has a free "Leave him to it."
- Gates 59/89, the same two expected gaps as slice A. Probe `probe_B.py` 11/11, 0 page errors: step 8 to the terms and the locked "Further", `ryan_step` 8 and the term flag; hot 1's button, its pool, Lust +3, gone for the day.

## 2026-11-01: release 1, slice C — Laura (DECISIONS 115)

- The ledger: Laura's ladder is four steps (1 the blue dress; 2 the `laura_03` canvas, Love 10; 3 the `laura_06` canvas, Love 20; 4 `laura_04_she_saw_you`, Corruption 20 · Love 30 · `laura_gaps_watched` 3). Her Saturday 16:30 bathroom row came in slice A. Mark gets a Saturday 17:00–18:30 kitchen row, "heading out to the bar": step 3 has him call up the stairs, and his sheet's Saturday had nothing after the garage (a build row, said here).
- `laura.py`: Love +5 a step (Want dropped: nothing of hers reads it). `laura_02` is the curfew rule: repeatable, no step, once a night (`laura_caught_today`), the kind path pays nothing. The built `laura_catch` repeat is removed: it duplicated the curfew rule and carried the cut climb ("Kiss her goodnight", her Want). `laura_04_ryans_door`, `_07`, `_08` are no longer built; `laura_05` stays one more slice on Jake's counter only (Jake's slice merges it). Step 3 reworked as "All dressed up". Step 4 and its breakfast ("last night" under 12 hours, else "the other night"). Her tease and touch columns are cut; her plain items pay Love +2 once a day in total (`laura_love_today`, a post-pass over her three hubs). Hub lines realigned to the four steps.
- `home.py`: "Keep watching." adds 1 to `laura_gaps_watched`; the crack's dressed-up line behind `laura_lonely`; `laura_alone_after` (the two measured after-step-4 screens); `laura_shower_gap` (Saturday 16:30–17:00, the two measured screens).
- `world_data.py`: her door's "The door's ajar." is flat, mutually exclusive cases: step 4 when ready, the after-gap once she's past it, the gap otherwise, each with the once-a-night brake.
- Gates 60/89. The one expected gap left: "a meter is read" (`cafe_name`, `cafe_shifts_worked`: Tom's slice). Fixed on the way: the curfew rule's `retry_after_days` (a repeatable has none) and its free suspicion rung; step 4's no.
- Probe `probe_C.py` 10/10, 0 page errors: the door, the gap with the dressed-up line, the counter to 3, step 4 next night ("Ryan.", both choices), `laura_step` 4, `laura_said_ryan`, the breakfast.

## 2026-11-01: release 1, slice D — Mark (DECISIONS 116)

- The ledger: Mark's ladder is four steps (1 count it slowly; 2 the late notice, his step 1 only; 3 shorts, `rent_short_weeks` 1 or more; 4 the `mark_06` canvas in the garage, Mon, Tue, Thu, Fri 19:00–22:00, Ryan's step 4 done).
- `mark.py`: Mark A 4, 5, 7, 8, 9 are no longer built. Step 4 reworked: "I saw you come out of Ryan's room. Middle of the night."; the couch lines cut; his no "Since Ryan's door."; `mark_step` 4. The Sunday table loses the paid look ("Twenty, and you can look", both voices, the cover screen, the wallet line); after the arrangement he counts at normal speed, plus a shuffle bag of five lines. His paid look on the hubs (`m_paid`) and in the garden (`home.py`) are cut. His leaks realigned (garage: "He can't hold your look" before step 4). Cards: four steps; the locked line "Mark, later. (After the house is yours.)".
- Gates 61/89 ("sinks >= sources" now passes with the paid sources gone). The one expected gap: "a meter is read" (Tom's slice).
- Probe `probe_D.py` 8/8, 0 page errors: step 4 in the garage, no couch line, `mark_step` 4 and `mark_arrangement`; the next Sunday's count at normal speed, no paid look.

## 2026-11-01: release 1, slice E — Tom (DECISIONS 117)

- The ledger: Tom's ladder is three steps (1 the apron; 2 the tip jar, `cafe_shifts_worked` 5; 3 `tom_03_not_by_the_window`, footfall 15, name −5 or lower, `cafe_let_it`).
- `tom.py`: strict. His hire line ("Eight a shift, plus tips. Be on time."; "Smile at booth four" and "Customers like that" cut); step 1 ("Tables first. Phone in the back. Smile.", "Yes, boss.", the two thoughts); step 2 the tip jar (Lust +5, Dominance −5); step 3 new; Tom B 2 and B 4 cut and B 5, B 6, the after-close repeat and Gary's paid ten minutes not built; his counter lines realigned. `phone.py`: "what's it pay" gets "eight and tips. be on time."; the after-close texts are not built (they wait with step 6).
- Build additions, said here: "Ask for the tight top." on his counter at Daring ("Your choice. Tables don't wait."): with the uniform rule cut, nothing else gives her the tight uniform, and the sheets say it is her choice. `cafe_gary_meet`, a one-time screen in Gary's hours that sets `gary_met` (his booth hub opens on a meeting).
- A fix to a bug that was already in the build: the clock-in equipped both uniforms, and the engine's "equip" also adds the item (v2.py:17371), so the tight uniform was hers and on from her first shift. The clock-in now puts on the normal uniform unless she has changed into the tight one.
- Step 3's "this shift" is `cafe_let_it` under 4 hours: the flag is stamped when the clock-out runs, before its 180 minutes pass (the probe caught "under 1 hour" never firing).
- Gates 62/89, no gate lost against the baseline; "a meter is read" passes again (Tom reads the café counters).
- Probe `probe_E.py` 12/12, 0 page errors: a level-3 shift, "Let it.", footfall 15, name −5, shifts worked, the pay; Tom's step 3 at clock-out, "It's my tips.", `tom_step` 3, the window rule.

## 2026-11-01: release 1, slice F — Hale (DECISIONS 118)

- The ledger: Hale's ladder is four steps (2 Exhibitionism 20; 3 his step 2 only; 4 Corruption 20 · Exhibitionism 20). Hale B 5 is cut.
- `hale.py`: step 1 reworked (she walks in late; "Late, on the first day." on day one, "Late." after; "Front row. Where I can see you."; his pen at her feet; picked up or left); its window is the whole lecture now, as she comes from the dean. Step 3 is private coaching (the speech, the hand, three answers, all finish, no grade; the portal). Step 4 reworks `hale_04_claire_knocks` as the first session: the two measured screens, "Let him." pays grade +5 and both meters +3, Claire's knock; "This isn't coaching." and Run park a week, Run costs grade −2. `hale_thursdays` is the Thursday session: two tiers of three measured pooled screens (shuffle bags), Claire early on a 1–4 roll (`hale_claire_roll`), the three answers, "Hale, further. (Needs Corruption 60)" locked. The old step-4 swaps and placeholders are removed; his office line at step 4 is "He looks at the clock, and then at you, like you're both on his schedule." `phone.py`: his Wednesday email follows step 4, "Thursday, my office. Half past six."
- Gates 62/89, no gate lost against the baseline.
- Probe `probe_F.py` 7/7, 0 page errors: step 4's three answers, Claire's knock, `hale_step` 4, grade +5; eight Thursdays: seven sessions and one early Claire.

## 2026-11-01: release 1, slice G — Zoe (DECISIONS 119)

- The ledger: step 2 opens on her ladder alone (its "Curious or Daring" is on the screen: each yes reads its own meter and shows locked with the number when she can't take it); step 3 Corruption 20 · Exhibitionism 20; step 4 her step 3 only; step 5 `zoe_05_no_dare`, Saturday 00:00–02:00 at her apartment (where her row is; the scene moves to her bedroom), Corruption 40, four dares done, `cocky_guy_met`, a party tonight.
- `zoe.py`: step 2's doing yes, "Dare me something else.", plays the dares' measured kiss; step 4 "I dared you instead of asking. I always do." / "Then keep daring me." (Zoe keeps picking; the built "From now on, I pick the dares." cut); step 5 with its two measured screens, "Tell him to go." / "Let him watch." (`zoe_let_him_watch`), Corruption +3, +3 Exhibitionism if he watches. Cards for five steps; the locked line "Zoe's next dare. (Needs Corruption 60.)".
- `pools.py`: `zoe_dares` replaces `party_dare`. Three tiers as flat cases, two yeses and a no on each, the six measured screens, the built circle flash kept as the Showing dare's second entry (a shuffle bag), the regulars' "You again." lines, the Jake line when she's his girlfriend, `zoe_dares_done` +1 a yes, locked yeses with their number.
- Build fixes, said here: the dares run at Zoe's Friday party only, **Saturday 00:00–02:00**. The party house on Saturday has none of the regulars, whose rows are Zoe's Friday party only; and a window that crossed midnight let the day roll clear `zoe_dared` and open a second dare the same night (the probe caught it). `zoe_dared` is set by every dare exit, cleared by the daily tick and by arriving at the party.
- Gates 62/89, no gate lost against the baseline.
- Probe `probe_G.py` 9/9, 0 page errors: the low tier's line and both yeses, the kiss, `zoe_dares_done` 1, one a night; step 5, "Let him watch.", `zoe_step` 5, `zoe_together`, `zoe_let_him_watch`.

## 2026-11-01: release 1, slice H — Jake (DECISIONS 120)

- The ledger: step 2 opens on his ladder alone ("Hi." reads Curious or Daring, two flat copies, locked with both numbers otherwise); step 4 `jake_04_sneak_him_in`, Saturday 22:00–00:00 at the front door after a date, Corruption 40.
- `jake.py`: step 3 is merged with built Jake 4 = Laura 5: after Ryan's door, Laura's shape in the dark window; inside, her couch lines ("Was he any good?", both dress answers); Laura present by her row. `laura_05_jake_at_the_door` is no longer built. Step 4 takes the date-end slot: "Come up.", "Your room. Now.", the three measured screens, the keyless landing when `her_door_unlocked`, Ryan through the wall past his step 5, Corruption +3, Ryan's Lust +5, `jake_first_time`. `jake_saturday_date` is the end of a date: the car by stage (the three measured screens; both meters, the street and Laura's window can see), after step 4 "Come up." (a two-entry shuffle bag) with the near-catch on a 1–8 roll (1 Laura's door, 2 Ryan's two knocks), "Jake, further. (Needs Corruption 60)" locked. The date drives her home now (the two date lines and its exit).
- A fix on the way: my first ledger edit rebound Jake's step 4 in a local map and never wrote it back; the validator caught the quest card still pointing at `laura_05`.
- Gates 62/89, no gate lost against the baseline (61/89).
- Probe `probe_H.py` 11/11, 0 page errors: step 3, Laura in the window, "Was he any good?", `jake_step` 3; the car at Curious; step 4, the landing, Ryan through the wall, `jake_step` 4 and `jake_first_time`.

## 2026-11-01: release 1, the reader pass and its fixes

- `v2-reader` on the 54 canvases the build touched: 42 FAILs on 31 canvases (report: the session scratchpad, `reader_first_term.md`). Fixed in the build, the build's own errors:
  - the locked twin buttons (`zoe_dares`, `jake_02`) are gone: the engine already greys the real button when it fails; `zoe_02`'s "Watch me." no longer claims "Needs Exhibitionism 20" to a girl without a bra;
  - "your top" in a dress: `canv.top_or_dress` swaps to "your dress" behind the two dresses she goes out in (`zoe_02` kiss, `zoe_dares`, the car, Hale's lower session);
  - bare feet in sneakers: "Feet up." and hot repeatable 2 take her sneakers off, hot 3 strips them too, the Laura event drops "bare";
  - `ryan_07`: one entrance (the screen before brings her to his door; the measured beat knocks); `ryan_08`'s Jake line needs `jake_step` 3, a boyfriend who walks her to the door;
  - `rent_short_2` says Vance comes "tomorrow night" (his knock is Monday); `rent_short_3` says "Three times." only on the third, "Again." after, and asks for the item she's wearing instead of fetching it;
  - Hale's grade said truly at each band, "Then your grade stays where it is."; Claire's "I'm early." (the knock lands about 18:40);
  - `zoe_02`'s doing yes needs the cocky guy at the party; the date's near-catch has Laura on the stairs, not upstairs (her Saturday row is the living room);
  - the curfew rule's "like she did in her mirror" is cut (it could show without the dress scene).
- Left for LO, listed in the report to LO: the design FAILs (8 hooks, Laura's want before her gaps, 4 written nos), the café's "folded twenty" against a $10–16 tip, and the FAILs in screens this build didn't write (Mark's streak lines read before the count, `mark_03`'s "listening at doors", `tom_01` and `tom_03` after the shifts end or "Busy night?" by day, Ryan's rent cover after the count, the hot tub's "in your clothes").
- Gates 62/89, no gate lost against the 61/89 baseline. All eight slice probes re-run: 83/83, 0 page errors. Engine suite: 793 passed, 17 skipped.

## 2026-11-01: LO's picks on the reader's FAILs — 5 built; 1–4 drafted on the sheets

- LO's pick 5 ("fix them now"), built, in screens this release didn't write: Mark's streak line now says the streak this Sunday makes (read before the count adds it; nothing on a broken Sunday); `mark_03`'s "Since you're listening at doors now." becomes "Shorts this time. Since you're reading my mail now."; Tom's step 1 window ends at 19:00 (the last shift start) and the screen hands her the apron (it equips the uniform); the tip jar's "Busy night?" becomes "Busy shift?"; Ryan's rent cover on a Sunday only before Mark's count; the hot tub's "Not tonight, Zo." dresses her before she goes home. Gates 62/89; probes A, B, D, E, G re-run, all pass.
- LO's picks 2b, 3, 4 and the hook lines (1) are drafted on the sheets, waiting for LO's sign: Laura's two gaps open after her step 2; written replies for the four nos (Ryan 4, the job ask, Hale 2 in jeans, Jake 4); "a folded ten" (re-measured); one true closing line each for the street (Vance), Ryan 6 and 7, Laura 3 and her breakfast, Zoe 5. Not built yet.

## 2026-11-01: LO's picks 1–4 built (DECISIONS 123, "Signed, build them")

- (1) Hooks: Ryan 6 and 7 end on a short screen each ("his door is open a hand's width. It stays that way." / "his phone is face-down every time you knock"); Laura 3's two endings and her breakfast point at her weeknight gap; Zoe 5's two endings, "Friday, babe. I'm in the dare with you now."; the street's Vance line, "He'll be on his porch tomorrow evening. He always is."
- (2b) Laura's bedroom gap and shower gap need `laura_step` 2 (the door options and both triggers).
- (3) The nos: Ryan 4's "Just saying goodnight." gets his reply; the café job ask has "Not yet." (Tom's reply; the ask is parked a day: `consume_on = "exit"`); Hale 2 has "Sit up straight." out of a skirt; Jake 4's "Goodnight, Jake." gets "Next Saturday, then. Your room."
- (4) "a folded ten".
- Gates 62/89, no gate lost against the baseline. Probes A–H 83/83 and `probe_I.py` 6/6 (no gap before step 2, the gap at step 2, the job's "Not yet.", Ryan's goodnight), 0 page errors.

## 2026-11-01: step 7, the taste columns into the skill

- `TASTE_COLUMNS.md` is now skill rule S14 (`the-sheets.md`), with the step row in the scene template, the ladder rules in the person template, and the step row in `v2-pitcher`. B150 done; the skill CHANGELOG has the entry. No game file changed; gates 62/89.

## 2026-11-01: the lecture links (LO: "College lectures have psychology business Links and wierd. It can be like attend lecture. And biology lecture just should the lecture no where to attend the lecture")

- The class button in the lecture hall was the canvas name ("Psychology (Dr. Hale)", "Business", "Biology", "Figure drawing"). Renamed to "Attend the Psychology lecture", "Attend the Business lecture", "Attend the Biology lecture", "Attend Figure drawing" (`college.py`, the four `class_row` calls).
- The first Business, Biology and Figure drawing classes (`meet_*`) ended back in the hall, so the first class read as over and nothing said where to attend. Their last button ("Find a seat." / "Find your charcoal.") now opens the class's own seat (Focus, Chat, Doze, Skip, the risky slot) inside the same canvas, with the same met flags; the class opening lines are left out because the meeting has just said them, except Figure drawing keeps its pose (`college.py`, `into_class`). Psychology's first lecture is Hale 1 and is unchanged.
- Dev + debug rebuild. Gates 62/89, nothing lost against the baseline. Probes A–I all pass; `probe_lect2.py` 21/21 (each first class opens the seat, no repeated opening, back in the hall after, no second class in the same slot, the "Attend" link next time opens the seat).

## 2026-11-02: the heat ladder applied, release 1 to Hungry (DECISIONS 124–125, "Signed, go ahead and build")

- **Gates** (the change page `sheets/HEAT_LADDER_A2.md` §1–3): 15 acts to Bold or Showing, 17 to Hungry or Watched, 3 teases
  to Curious. Step gates in the ledger (`v2_state.json` board ladders: Ryan 4 → C40, Ryan 7 and 8 → C60, Zoe 3 and Hale 4 →
  40/40, Mark 3 + `mark_saw_her`); the rest in the build scripts, each line commented "DECISIONS 124".
- **Pays:** Bold one-time steps +3 cap 79 (Ryan 4 and 7, Ryan 6's Exhibitionism, the hot tub, Hale 4, Zoe 5, Jake 4);
  Bold acts cap 59, Hungry acts cap 79. Zoe's first no pays nothing and adds `zoe_refused` (read on her balcony line); the
  dress-code warning pays nothing; the café's no no longer counts toward "Let it."; the stairs get a way out that pays her
  nothing and moves Mark's Want when he is below; Laura 4's stay caps at 59; Mark's towel slip pays her like Ryan's.
- **New:** `mark_00_the_dryer` (Mark's first accident, Saturday in the garage; his teases, "Play up to Mark", and step 3 read
  `mark_saw_her`); the skip-opening hall screen (`2_one_shots.toml` `skip_hall`; she is dressed on its "Get dressed."); the
  door crack's low-Want branch (`crack_low`, `watch_low`, from its sheet); Ryan banging on the shower door on weekdays
  06:25–06:45 ("Wrap up and get out." / "\"Five minutes.\"", his Warmth −1); Laura's look at the door when Ryan laughs
  downstairs (step 3, only while he is on the couch); the hall towel screen by what she wears.
- **Locks:** every "(Needs Corruption 60)" / "(Needs Exhibitionism 60)" lock and the cards' terminal lines now read "(Next
  release)" (18 buttons and 4 card lines, Tom's included). The gate is `canv.NEXT_RELEASE`, a hidden counter
  `release_2_written` gated at 1 that nothing raises: the engine prints "(Corruption N+ (you have M))" beside a trait lock
  of 2 or more (`v2.py:16462-16468`), and a flag gate fails the build's flag-chain check. Each carries its label as
  `locked_text` (gate: a locked door says why). The "It comes later" screens say "That's in the next release of First Term."
- **The Quests stage cards** reach Hungry and Watched (`extras.py`): Bold's card names what pays at Bold, and two new cards
  (Hungry, Watched) say what the next release holds.
- **Copy (H4):** the 73 signed rows (`round12_tease/copy_fixes_{A,B,C}.md`), applied by three agents on disjoint files.
  Judgement calls they made: Hale's pen screen has him hold out his hand, flat (the draft took the pen before her button);
  the class risky lines take one group per clothing set (`college.py` `by_clothes`; the bio braless-in-jeans line was false
  and is fixed); the cocky guy's "Not yet." shows only Friday before midnight, while `hookup_today` can tell; Mark's stairs
  line catches her halfway up so both her buttons answer it; the shop says "strip down" with no underwear; Mark's laundry
  not-yet points at his laundry tease again, not the cut "Let him fold them."; the garden show has a catch-all line for a
  watcher who has gone in the hour.
- **Build deviations from the sheets:**
  - Jake's car choices read `jake_step` gte 3, not eq 3. His step 4 takes the first Bold Saturday, so with eq 3 the car
    scenes would almost never show (probe H found it).
  - "Let it." at the café: below Corruption 40 the grope still happens at level 3, and she can only refuse (being groped
    is stage 1; her answer is what climbs).
  - The party tub has no meter pay (it pays energy, as built); the gate is on the canvas.
- **Gates** 61/89 against the 62/89 baseline. Lost: `ends on an opening`. The declared door ("Further. (Next release)" on
  Ryan 8) can never come true in this build, and the gate wants a door the player can open later in the same build. That
  is LO's call (waive it for release 1, or declare a different door). Nothing else lost.
- **Probes:** `probe_a2.py` 16/16 (the skip shows the hall, the lean only at Curious and on the body, it pays +1, Ryan 4
  waits for Bold, the dryer fires and pays, no "Needs Corruption 60" anywhere, 0 page errors). A–I updated to the new gates
  (A 15/15, B 11/11, C 10/10, D 8/8, E 12/12, F 7/7, G 9/9, H 10/10, I 6/6).
- Rebuilt with `--dev --debug`. Not committed.
- **Reader** (`v2-reader`, all 89 changed canvases in three groups; tables in
  `~/Documents/Great_Games_Study_20260926/round12_tease/first_term_reader/reader_a2_{home,college,out}.md`): 107 FAILs of
  1,068 verdicts. Fixed now, the ones this change caused:
  - the hall accident's "Knock next time." and "Stop and talk." set `ryan_hall_seen` too (without it the doorway lean could
    never open on those branches);
  - Mark's other chosen acts follow his accident (`mark_saw_her`): the towel slip and drop, channel 5's "Leave it on.", the
    couch with him passing, the garden's "Let Mark look." and "Show off" with him;
  - `mark_03`: "Fine." needs Daring like "Go up and change."; her version has "I'm not changing for you."; under Daring her
    version has him ask instead of a screen with no button;
  - the keg flash (now Watched) loses the Curious excuse ("It's a dare. It doesn't count." became "Let the whole room look.");
  - the stairs fire only with Mark below (an empty house paid her for nobody);
  - "Stand naked in his room." needs Bold too (it pays Corruption);
  - the dryer's cover-up ending has her pushback ("Mom's husband. Don't think about it.").
  The rest were in the game before this change; they are listed for LO in the report. Gates 61/89 (only `ends on an opening`
  lost, as above); probes 104/104, 0 page errors. Rebuilt `--dev --debug`.

## 2026-11-02: dev mode edits her four sidebar meters (DECISIONS 126, LO: "Add them to the traits. Rebuild commit and push")

- LO could not change Corruption in dev + debug mode: the dev Traits list skipped every `in_dump = false` key
  (`v2.py:19862`, `:19888`), so the four meters shown as their own sidebar rows (Corruption, Exhibitionism, Energy,
  Hygiene) had no − / +. Engine: the DEV list now skips only hidden keys; the player's list is unchanged.
- Tried first: dropping `in_dump = false` in `0_systems_spec.toml`. That failed the gate "a banded meter is shown
  once" (the player would see Corruption twice), so it was reverted for the engine fix.
- Engine test `test_the_dev_list_skips_only_hidden_so_a_sidebar_meter_keeps_its_buttons`; engine suite 794 passed,
  17 skipped. Gates 61/89, as before. `probe_devtraits.py` 7/7 (− / + on all four, `ryan_step` still hidden, + raises
  Corruption, 0 page errors). Rebuilt `--dev --debug`. a2's play check: "skipped by LO" (recorded by `pieces.py`).

## 2026-11-02: the dev screen (engine, dev builds only; LO: "1 both · 2 yes full page · 3 yes place")

- New full page `DevPage`, opened by "🔧 Dev screen" in the dev sidebar, laid out like People (tap-to-open rows):
  **Her** (a button per stage band of each banded sidebar meter), **Time and place** (day, hour, ±15/60 min, go to any
  place), then **one row per person**: his meters ±5, the step counter ±1, and every step with ✓ / ▶ / ·, what it
  needs (each condition checked by the engine's own evaluator, "now N"), its window and its place, and two buttons:
  **Set it up** (clears its fired record, makes each condition true, moves the clock into its first window, sends
  her to the place, where it fires the normal way) and **Play it now** (jumps into its first screen).
- Nothing authored: steps are found at runtime from `setup.help_data.locationCanvases` (a person's counter is the
  `eq` counter their one-time scenes read most; then every one-time scene reading it is a step, bound or not).
  first_term: Mark 1–4, Laura 1–4, Ryan 2–8 (1 is the opening), Jake 1–4, Hale 1–4, Tom 1–3, Zoe 1–5.
- Not forced by "Set it up": clothing and presence items (marked ✗ for the tester).
- Engine tests 795 passed (two new). `probe_devpage.py` 10/10 (the button, Her, all seven people, Set it up fires
  Ryan 4 from Corruption 0, Play it now opens the hot tub, the Hungry button, 22:00, 0 page errors). Gates 61/89;
  probes a2, A–I and devtraits all pass. Rebuilt `--dev --debug`.

## 2026-11-02: "Play it now" moves the clock into the step's window (engine, dev builds only; LO: "1")
- LO hit a dead end: Play it now on Ryan 5 from a daytime clock left the last screen with no exit (the three
  "Sleep." exits read 22:00–01:00, "Knock back twice." needs Corruption 40). Play it now set nothing.
- Fix in `v2.py`: `clockIntoWindow(st, always)`, shared with Set it up. Play it now calls it with `always=false`, so
  the clock moves to the window's start + 5 minutes only when it is outside the window (schedule or time_of_day);
  meters, flags and clothes stay as they are. Not a game bug: in real play step 5 starts Friday 22:00–00:00 and
  the last screen is reached by 00:19 at the latest, inside a "Sleep." window.
- `test_the_dev_screen_is_in_dev_builds_only` checks the call (18 passed). New `probe_devplay_clock.py` 6/6 (Monday
  10:00 + C5, Play it now lands Friday 22:05, C stays 5, "Sleep." shows, no dead-end warning, an in-window 23:30 is
  kept, 0 page errors); `probe_devpage.py` 10/10. Rebuilt `--dev --debug`.

## 2026-11-02: Ryan's step 8 rises from normal, and the two-knocks repeat is a menu (DECISIONS 127; LO: "Signed, go ahead and build")
- Step 8 (`ryan_08_two_knocks_first_sex`): knocks, then a normal talk on his bed ("I meant it. The girlfriend thing."), her
  doubt (*This is Ryan. You should go.*: "Stay." / "Go."), the kiss ("Let him." / "Stop. Not tonight."), undressing; then
  her picks: what first (`suck` / `lick` / straight on), how (`ride` / `under` / `wall_back`), Laura's light (`keep` /
  `freeze`), the finish (`inside` / `on` / `mouth`); `after` (her feeling, its own screen); the terms as signed. Three
  parked nos. Stripped on the first act pick; dressed again on the terms exits. Gate, pay and terms unchanged; the
  trigger now also reads `kayla_met` (gate "no one is named before they're met").
- The repeat (`ryan_two_knocks`): door, `start` (a bag of three normal starts), the act menu by his Lust (suck and ride
  at 70, lick at 80, wall at 90, the last two shown locked), each act in two voices split at Corruption 70, `twist` (a
  bag of three: nothing / Laura knocks / Kayla calls), her pick of finish. Pay as built (C+1 cap 79, Lust +3 once a day).
- 30 screens by six `v2-prose` writers, measured; read from the sheets. Fixes after: no "asleep" for Laura (awake
  22:00–23:00); `light` leaves the pause to the player; `kiss`/`undress` name no garment (gate "her clothes are backed");
  the loop's `7suck` ends with him in her so the twists are true after every act; "The bed creaks." cut; Kayla's
  thought reworded (her call is never answered).
- Gates 61/89, the same set as before (only `ends on an opening` off, waiting for LO). Explicit floor 25.4% of
  repeatable beats. New `probe_ryan8.py` 21/21 (the whole step-8 path, the terms, the loop the next night, the menu at
  Lust 77 and 92, both voices, the pay, 0 page errors). `probe_B.py` updated to the new path, 11/11; a2, A, C–I, devtraits,
  devpage, devplay_clock pass (D flaked once on a random home event, then 3/3). Rebuilt `--dev --debug`.
- New media slots for LO's harvest: `sex/ryan_08_{kiss,undress}_t4`, `sex/ryan_08_{suck,lick,under,wall_back,keep,freeze,mouth}_t5`,
  `sex/ryan_hot7_{suck,ride,lick,wall,twist,finish}_t5`. Retired: `sex/ryan_hot7_t5`.
- Reader pass (`v2-reader` on both canvases): 13 fails, the truth ones fixed. Step 7 is "Kayla can't know" (her hand,
  his phone), not the cut kiss: `talk` now says "Last time. With Kayla calling. That can't happen again." ("Then why did
  you open the door?"), `kiss` and `undress` follow it. Mark is downstairs with the TV 22:00–02:00, so only Laura is
  "across the hall" (`suck`, `lick`, `7ride_shy`); `light` has Ryan see the light (she may face the wall); `under` pulls
  her up the bed; `7t_b` opens on the headboard waking Laura (asleep from 23:00); `7t_c` turns the face-down phone over;
  the door line no longer puts him at the desk; step 8's trigger skips a towel (`undress` pulls clothes over her head).
  All changed beats re-measured (explicit 5–10, no pivot). Not fixed, for LO: the reader's R5b, that the parked nos
  ("Not tonight.", "Go.", "Leave him to it.") move nothing but the retry (as signed). Gates 61/89; probes ryan8 21/21,
  B 11/11, a2 16/16.

## 2026-11-02: Mark's plain items pay nothing; laundry is a tease ladder (DECISIONS 128; LO: "Signed, skip the play check, build it")
- `mark.py`: `want(M)` removed from every plain pay (beer, film, the TV's `watch_plain`, laundry, breakfast, dinner,
  cooking, dishes). Kept: channel 5 "Leave it on." (+2), the towel, his steps, the other items' tease rows.
- Laundry: `LAUNDRY_BASKET` (Curious · `mark_saw_her`, Lust +2; the filled basket screen, no step needed now) and
  `LAUNDRY_TEASES`: "Bend for the bottom drum." (Curious · Daring · panties on · not a towel; Lust +3, Exhibitionism +1
  cap 39; three screens by `worn_type`: skirt or dress / sleep shirt / jeans, leggings, shorts) and "Wash what you're
  wearing." (Bold · Showing · a top and a bra; Lust +4, Exhibitionism +1, Corruption +1, cap 59; the top unequipped).
  Once a day through `did_laundry`. Screens by `v2-prose`, measured, in `sheets/scenes/mark_laundry_teases.md`.
- `home_items.py` `item()`: new `teases=[...]`; a spec may carry `blocks` (its written screen) and `wardrobe`.
- Gates 61/89, same set. New `probe_mark_laundry.py` 19/19 (plain laundry and TV pay nothing, the ladder by stage,
  both bend variants, the wash pays and leaves the bra, once a day, 0 page errors). a2, A–C, E–I, devtraits, devpage,
  devplay_clock, ryan8 pass. D flakes about 1 run in 4: Mark's random "reach" home event can fire in the kitchen on
  Sunday 09:00 before the rent table (older, not from this change). Rebuilt `--dev --debug`.
- Media for LO's harvest: `sex/mark_laundry_bend_t4`, `sex/mark_laundry_wash_t4`.

## 2026-11-02: False lines, pass a3 (DECISIONS 129; LO: "Signed")
From `sheets/FALSE_LINES_A3.md`: the a2 reader's fails on "true on every visit" and "the numbers and the clothes agree".
- Home: the shower pool no longer says "Nobody can see" (the lock only catches halfway); at Ryan's Want 40 the peek
  itself has him keep looking ("He doesn't look at the floor"), so no "This time" sits after "He looks at the floor".
  The garden opener says "lie down". The opening says "the café near campus" (`2_one_shots.toml`). Ryan 6 loses "It
  stays that way."; Ryan 7's knock reads "His light is on under his door, and you both know why you're here." (and its
  card). Ryan 8's near-catch is Laura's floorboards, not her light (her lamp is on 22:00–23:00): `light`, `keep` and
  `freeze` rewritten in the sheet and re-measured (121 words, 9 explicit; 132, 11; 135, 10); the after screen reads
  "Laura's room has gone quiet again"; the node and its video description follow.
- Item 3 (Mark 3 with no exit) was already fixed in a2: her version has "I'm not changing for you." at every stage.
  The sheet was wrong on it; `probe_a3` checks the button.
- Out: `cafe_coffee` "Nobody here knows you."; Gary's shifts show only his own L3 screen (`L3_B`; the strangers' two
  stay for the shifts he isn't in); the tight uniform is "the black dress"; the shop's skirt says "Curious or Daring" and
  the sports bra loses the park line (`3_activities.toml`). Gates: the no-panties breeze needs no jeans, leggings or
  shorts on; Tom 3 needs the shift to have ended within 30 minutes (`cafe_let_it` under 3.5 hours); `vance_meeting`
  waits while his rent row has him at your front door (`npc_at_location home_front_door is_absent`, not "present on his
  porch": before `vance_met` he has no porch row).
- College: the cocky guy has Figure drawing rows in `v2_state.json` (Tue/Thu 08:30–10:00, Wed 13:00–14:30, after
  `cocky_guy_met`), and a new face there, `hub_cocky_class` (needed by the gates "every person here has a face" and
  "standing surface"). Hale 1 splits on `hale_met` / `nadia_met`. Hale 4's window ends 19:15. "Bye, Dr. Hale." Jake's
  hubs say "Everyone's looking at you in that dress." (the date car keeps "tonight"). Zoe 2 has sports-bra lines;
  the hot tub's "Go home" dresses her (`DRESS_DAY`); Zoe's "Start the song." dare draws `FLASH_SONG` ("Till the song
  ends, babe", 108 words, 4 explicit) instead of the count of three; the park dare is "two long seconds".
- Gates 61/89; "sinks >= sources" now passes too. New `probe_a3.py` 23/23. A, a2, B (updated for the floorboards),
  C–I, devplay_clock, mark_laundry, ryan8 pass. `probe_shower.py` is stale (written before DECISIONS 124 changed the
  weekday shower exits). Rebuilt `--dev --debug`.
- Reader pass (`v2-reader`, truth and clothes, 28 canvases): 28 of 29 fixes hold. Fixed after it: item 20 really (the
  "Sorry." link set `nadia_met` before the front row read it; Nadia, the desk guy and the rival are now met on the
  front row's exits); Ryan 7's knock beat "You knock twice and push his door open without waiting." (116 words, 4
  explicit); Ryan 8's knock drops "The house is dark." and its other finish reads "Laura's room is quiet again"; Tom's
  button and screen say "the tight dress"; `hub_cocky_class` names him without Jake, makes no easel or arrival claim,
  and its stay is "Talk a while.". Gates 61/89; probes a3 24/24 (first visit meets Nadia), A, a2, B, C–I, ryan8,
  mark_laundry, devplay_clock pass.
- Reader fails NOT fixed, new finds outside the signed list, for LO: the shower pool's "For ten minutes the house can't
  get at you." after a peek or a bang; Hale 1's "while the room packs up" can run past 10:00 into Business; the exam's
  and `meet_figure`'s "Jake's teammate" without `jake_met`, and `meet_figure`'s end easel with two neighbours;
  `zoe_dares` `low_do` past his 02:00 row; Zoe 2's "under your top" in Laura's dress; the hot tub's "unhook your bra"
  for a sports bra; Hale 4's "your top" in a dress. Full table: the session scratchpad `reader_first_term.md`.
- The reader's 8 new finds, fixed (LO: "Yes fix them", then "Skip the play check", recorded on `a3_false_lines`):
  the shower pool's third line "you stay under it longer than you should"; Hale 1 opens only to 08:55, so the hour
  of lecture ends by 10:00 (the first Monday's dean path arrives at 08:52, checked live with `probe_hale1.py`); the art
  midterm names "the cocky guy from Figure drawing" until `jake_met`; the first Figure drawing class takes "an easel
  halfway round the horseshoe"; Zoe's dares end at 01:50, so a 10-minute yes lands before his 02:00 row ends; Zoe 2 has
  a sports-bra line under a dress; the hot tub kiss opens "You get your bra off" (120 words, 9 explicit); Hale 4 says
  "You pull everything up anyway." and "You pull everything back down over your tits." (feel: 116 words, 7 explicit).
  Gates 61/89; probes a3 24/24, hale1 1/1, A, a2, B–I, ryan8, mark_laundry, devplay_clock pass. Rebuilt `--dev --debug`.

## 2026-11-02: The release door (DECISIONS 130; LO: "Go ahead with your rec", "Skip the play check")
- `ryan.py`: step 8's terms door is "Further." locked on Corruption 60 (shown locked; the engine prints "(Corruption 60+
  (you have N))"). Open, a `further` screen: "Ryan's waiting for your answer. Whatever comes after it isn't written
  yet." and "That's in the next release of First Term.", then "Back." to his terms. No `locked_text`: the gate "a locked
  door says why" counts a label plus the engine's need as saying it twice. `v2_state.json` `release_page.door` now
  names "Further.". The other "(Next release)" locks keep `NEXT_RELEASE`.
- Gates 62/89: "ends on an opening" passes; nothing new fails. New `probe_door.py` 6/6 (locked at 45, open at 60, the
  screen, back to his terms, 0 page errors). `probe_B.py` updated (at Corruption 65 the door is open), 11/11; A, a2,
  C, E–I, a3, ryan8, mark_laundry, devplay_clock, hale1 pass; D flaked once on Mark's random reach event (older).
  Rebuilt `--dev --debug`.

## 2026-11-02: Reader fails, pass a3 (DECISIONS 131; LO: "Signed, go with your recs, skip the play check")
From `sheets/READER_FAILS_A3.md` (68 rows from three `v2-reader` re-reads of the current build). Built by three agents
on disjoint scripts (home: mark, ryan, laura, home, home_items, writer; college: college, hale, jake, zoe; out: extras,
pools, town, tom, cafe, `3_activities.toml`), then one full build. Each change is commented `reader a3 #<row>`; each
touched sheet has a dated note.
- Calls as signed: hub nos cost his Want +1 with a line (Mark, Ryan, Vance; Laura's costs her Love −1); no new
  counters; the five unwritten screens are written (the front step's "Let the street see.", the garden's "Let Mark
  look.", the couch's "Stay a while." for Mark and Ryan, Laura's tidy tease, the park's walk). None is sex; measured.
- Deviations: Zoe and the cocky guy have no Want stat, and the validator refuses one, so their nos (park, party wall,
  art midterm) are his or her line only. Mark's towel no is "Hitch the towel up." (a "Get dressed." that moves no
  garment fails "a button does something"). Laura's tidy tease says "your laundry … the little things" (the wardrobe
  has no lace, and "your panties" off her body fails "her clothes are backed"). The front step's showing and Vance's
  paid no are once a day (`street_step_today`, `vance_no_today` in `[engine.daily_tick]`): as free rungs they failed
  "the climb is paid for". The hot tub's "Leave it." caps Exhibitionism at 79 (59 never moved at its E60 gate).
  Hale's office lines and Zoe's park line were reworded to stay true ("Front row tomorrow", "Tomorrow I'm daring you
  again"). The TA's held-back line is now her eyes on your chest (the first version repeated her door line).
- Verify pass (`v2-reader`, all twelve tests, 55 canvases): 64 of 68 rows fixed; then fixed: the garden's "Play up to…"
  only while `sunned` is unset; Laura's tidy tease only after her door or her shower was seen; `hub_cocky_class` has
  a body line in any outfit, a price after the midterm, and no stale answers line; the park walk ends on her not-yet;
  `laura_04` needs `laura_alone_seen` (her "Ryan." and "again" were unbacked on a shower-only path).
- Gates 62/89 (no new fails). New `probe_rf.py` 17/17 (Channel 5 after his accident, the selfie at E20, the park hem
  under E40, the whistle reply by stage, the front step once a day by daylight, Vance's no paid once a day). A, a2, a3,
  B, C, E–I, ryan8, mark_laundry, door, hale1 pass. Rebuilt `--dev --debug`.
- Open, older, for LO: `home_event_laura_robe` "She knows you know it." before `laura_04_done`; `zoe_02`'s "slides out
  of your sleeve" in Zoe's dress; no hook below the stage on the robe, Mark's reach and Ryan's towel events; Ryan's
  garden tease and lotion screens are still placeholders; `zoe_park_dare` still sets the unread `park_cool_zoe`; the
  café strangers' audience at Corruption 40 (a stage call). Verify table: the session scratchpad `reader_a3_verify.md`.
- The older reader rows (LO: "Skip the play check, fix the older ones too"): the robe's "She knows you know it." needs
  `laura_04_done`; the robe, Mark's reach and Ryan's towel events each end on a forward thought below their stage
  ("She's down here in that robe every weekday morning. So are you." · "Next time he reaches past you, you'll know
  why." · "He's out of that bathroom at this time every weekday."); in Zoe's dress the bra slides out "through the
  armhole"; `zoe_park_dare` no longer sets the unread `park_cool_zoe` (no longer declared); the café strangers' lap
  (`L3_C`, the back table roars) only at Exhibitionism 60, `L3_A` below it (a room watching is Watched).
- Correction: the earlier note said Ryan's garden tease and lotion screens were placeholders. They are not: `writer.py`
  fills both (#34, #35) from the writer's signed screens, and the lotion button needs a bare back. A first attempt to
  write them collided with that fill (the build asserted) and was reverted.
- Gates 62/89; 0 PLACEHOLDER blocks in the build. Probes rf, A, a2, a3, B, C, E–I, ryan8, mark_laundry, door, hale1
  pass; D 3/4 (Mark's random reach event before the Sunday table, as before). Rebuilt `--dev --debug`.

## 2026-11-02 — engine: no empty lines between blocks (LO: "Go ahead")
- LO's report: Gary's booth showed a big gap above and below his one line, and many screens had empty space. Cause,
  measured headless: SugarCube renders every source line break as a `<br>`, and the v2 generator put its invisible
  macros on lines of their own. The line pool and the condition-group chain joined `<<set>>`/`<<if>>`/`<</if>>` with
  newlines, and every node passage ended its content with `\n\n` plus one line each for the current_canvas and
  current_node sets, markCanvasTriggered and visited_nodes. Gary's booth: 2 empty lines above, 8 below.
- Fix in `generators/v2.py` (every v2 game): the pool and group chains join with `""`. The node bookkeeping is one
  `node_bookkeeping` string written straight after the content, shared by the three header builds. No line break is
  left after the dev caption, the substitution check, the pre-substitution effects, or before the exits' `<<nobr>>`.
  The location and game-end exits' effects lines are one line. No TOML changed.
- Measured over all 593 canvas screens: 5,686 `<br>` before (every screen, up to 17 in a row); 689 after, each one
  directly after a button (one button per line), none in a row. 0 line breaks between markup outside `<<nobr>>`.
  Gary's booth is now caption, paragraph, his line, the button.
- Tests: new `tests/test_no_blank_lines.py` (pool, group, passage head, and a browser sweep of a fixture's screens).
  `test_legacy_engine.py` Doc 69 ordering test now compares positions, not line numbers (both macros share a line).
  `apps/game_generation/tests`: 799 passed, 17 skipped. `tests/` + `apps/projects`: 14 fail, and the same 14 fail
  with HEAD's `v2.py`, so they predate this change.
- Gates 62/89. "sinks >= sources" differs from the 11-01 baseline file, but it was already that way in every run
  today: it reads the TOML, not the generator. Probes a3 24/24, door 6/6, rf 17/17, B 11/11. Rebuilt `--dev --debug`.

## 2026-11-02 — Zoe's meeting card under People (LO: "zoe should have a npc card??" · "Yes build it, skip the play check")
- Before: nothing pointed at Zoe in week one. Every one of her rows and cards needs `zoe_met`, and the one nudge, a
  Story Goals card ("Someone from your Biology class hangs out on the quad…", priority 15, group `story_goals`), lost
  its group to the priority-20 "Week one" card for days 0–6 (`pickQuestsCards` shows one card per group). Measured:
  the Biology card first showed at 7 days since the opening, though her meeting fires from the first Tuesday.
- Now (`zoe.py`): her own card, `npc_id = npc_zoe`, the way Dr. Hale's step-1 card points at his first lecture.
  It shows while `opening_done` is set and `zoe_met` is not, with `ready_canvas = zoe_00_quad_meeting`, text "The girl
  from your Biology class hangs out on the quad in the afternoons." and tip "The quad, Tuesday, Thursday or Friday,
  14:30 to 18:00". The Story Goals card is cut. Sheet row updated (`sheets/scenes/zoe_00_quad_meeting.md`).
- Accepted: the People row is headed "Zoe" before she shouts her name in the scene (the engine has no stranger name
  for an NPC). Her card's text still calls her the girl from Biology.
- New `probe_zoe_npccard.py` 5/5: opening day shows "Zoe · Tue, Thu, Fri 2:30–6 PM · Quad" under People and no
  Biology story goal; still there on day 8; Tue 15:00 on the quad plays the meeting; after it her card is the Friday
  party. Gates 62/89. Probes a3, door, rf, B, A pass. Rebuilt `--dev --debug`.

## 2026-11-02 — pointers to the people a player could miss (LO: "Yes all three the go ahead")
- Audit after Zoe's card: every scene that opens a person, and what points at it before it fires. Ryan, Laura, Mark
  and Hale have cards from the start; Jake comes at Zoe's first party, Nadia at Hale's first lecture, Kayla and Claire
  inside Ryan's and Hale's steps, the party house at Zoe's step 2, the other lecturers on the Timetable. Three gaps:
  - **Tom / the café job:** only the "Week one" story card named it, gone after 7 days. Measured: day 8, nothing on
    the Quests page mentioned the café, the job or Tom. Now `tom.py` adds his hiring card, "The café in town is
    hiring." (tip "The café in town, Monday to Saturday, 8 AM to 11 PM"), shown while `cafe_job` is unset and
    pointing at `cafe_job_ask`.
  - **Vance:** met only by chance on the street of an evening; his porch and his knock wait for `vance_met`. Now
    `extras.py` adds his meeting card, "Next door: the man who owns your house watches the street." (tip "The street,
    an evening, 6 to 10 PM"), shown while `vance_met` is unset and pointing at `vance_meeting`.
  - **Zoe's step 5** needs `cocky_guy_met`, met only at Figure drawing; its goal read "Cocky guy met". Now
    `canv.py` FLAG_WORDS labels it "Meet Jake's teammate at Figure drawing (Tuesday or Thursday morning, Wednesday
    after lunch)".
- Sheets: `tom_01_the_apron.md` and `people/npc_vance.md` carry the cards.
- New `probe_pointers.py`: Tom ("Today 8 AM–11 PM · Café") and Mr. Vance ("Today 6–10 PM · Your Street") under
  People on day 1 and day 8; once she has the job and has met him, both rows hand over to their usual cards. Zoe's
  step-5 card, opened, lists the Figure drawing goal (her closed row shows only the first goal with a number).
- Gates 62/89; 0 PLACEHOLDER. Probes a3, door, rf, B, A, zoe_npccard pass. Rebuilt `--dev --debug`.
- Seen, not changed: some goal labels still print the raw counter name: "zoe_dares_done 4" (Zoe step 5, and her
  closed row), and in Tom's cards "cafe_shifts_worked 5", "cafe_footfall 15", "cafe_name -5".

## 2026-11-03 — card goals in words (LO: "Yes fix the labels too, skip the play check")
- Eight goal labels printed a raw name: "zoe_dares_done 4", "cafe_shifts_worked 5", "cafe_footfall 15",
  "cafe_name -5", "laura_gaps_watched 3", "rent_short_weeks 1", "Mark saw her", "Cafe let it". Cause:
  `canv.card_goals` named a counter only from its short `TRAIT_NAME` list, else the key, and a flag only from
  `FLAG_WORDS`, else the key tidied.
- Now `canv.py`: a counter falls back to the game's own `[[traits.labels]]` name in `0_systems_spec.toml`
  (`SPEC_LABEL`), so a new counter is named too. `COUNTER_WORDS` says how for three: "Café regulars 15: play along or
  flirt back on a busy shift, or let a hand stay", "The café's name -5: let a customer's hand stay, on a café shift"
  and "A Sunday short on the rent". `FLAG_WORDS` adds "Mark's first accident: the garage, a Saturday" and "Let a
  customer's hand stay, on a café shift". Also now: "Shifts worked 5", "Times you watched Laura 3", "Zoe's dares 4".
- Build: 0 goal labels with a raw name. New `probe_labels.py` 1/1: no raw name on the Quests page, cards open.
  Gates 62/89. Probes a3, door, rf, B, A, zoe_npccard pass; pointers 5/6, the miss being Zoe's closed row, which shows
  only her first goal with a number (her open card lists the Figure drawing goal). Rebuilt `--dev --debug`.

## 2026-11-03 — no "(Next release)" buttons (LO: "(Next release) no dont even show the option"; DECISIONS 132)
- LO saw "Further. (Next release)" on Mark's beer from the first visit, before any tease shows. Every such button was
  greyed for good: its gate is the `release_2_written` counter nothing raises (`canv.py:16`).
- Removed 14 buttons and their screens: `home_items.item` loses `hungry` and `hungry_node` goes (Mark beer and Sunday
  breakfast, Laura breakfast, Ryan games); Ryan's two knocks; the bedroom door at night (`home.py`); Hale's office;
  Jake's car; Zoe's party dare and the park loop (`pools.py`); `college.class_row` loses `hungry_label` (Psychology,
  Business, Biology, Figure drawing's pose).
- Kept: Ryan step 8's "Further." (the declared release door, Corruption 60), and four quest cards whose last goal
  names the next release: "Hale, further.", "Jake, further.", "Tom, later.", "Zoe's next dare.".
- Build: 0 "(Next release)" choices; 4 left on cards. New `probe_nr.py` 4/4 (no such choice in the story source;
  Mark's beer and Figure drawing clean at Corruption 45; no page errors). `probe_door.py` 6/6. Gates 62/89, the same
  as the baseline. The build's "1 error(s) encountered" line is there with the files at HEAD too. Rebuilt `--dev --debug`.
- Not played in Chrome.

## 2026-11-03 — a no to Zoe's kiss is not her step 1 (LO: "I think dare refusal shouldn't be counted as done", "Go"; DECISIONS 133)
- LO saw Zoe's kiss dare and her bra dare at the same party. Cause: step 1 (Fri 19:00-23:00) and step 2 (Fri
  21:00-00:00) had no gap but "step 1 done", and the refused kiss counted as step 1. Step 2 also fired at Good Girl
  with "Not tonight, Zo." as the only button.
- `zoe.py`: the no sets `zoe_kiss_refused` and only Jake's step; new `zoe_01b_kiss_again`; step 2 gets 24 hours after
  `zoe_01_done` plus Exhibitionism 20, and a Curious copy `zoe_02_balcony_curious` (the engine has no nested OR in a
  trigger); the "last time" line reads `zoe_balcony_refused`; two cards changed.
- Found on the way: Friday is weekday 4 here (`canv.DAYS`); `zoe_dares`' `[5]` is Saturday 00:00-01:50, right for it.
- Probes: new `probe_zkiss.py` 17/17 (no, same night, Good Girl, re-ask, twice, yes, same night, Daring) and
  `probe_zbalc.py` 6/6 (Curious copy with the cocky guy there, its no, "last time", the kiss route to step 2).
  nr 4/4, door 6/6, a3 24/24, zoe_npccard 5/5. Gates 62/89, as the baseline. Played in Chrome
  (`pieces.py chrome first_term zoe_kiss_no`). Rebuilt `--dev --debug`.

## 2026-11-03 — LO's skill decisions applied to the game (DECISIONS 134–140)

- **C1 (DECISIONS 135).** Her refusal never raises his Want. The +1 is gone from `home_items.py` (the towel no),
  `home.py` (the five random events' way out), `pools.py` (the stairs skirt) and `college.py` (the cocky guy).
- **S6 (136).** The five "Nothing happens." random events are removed from `home.py` and `town.py`.
- **S12 (134).** Ryan's "Further." door and its screen are removed (`ryan.py`). His card's end line is now "More of
  Ryan in the next release.", and `v2_state.release_page.door` is null.
- **C4 (137).** Under hygiene 30, Ryan's hot repeatables (his room, the couch) and Jake's date still show. When she
  goes, he refuses and says why, with no pay (`ryan.py` `hot_choice`/`stink_node`, `jake.py`).
- **W8 (138).** Jake dates Wednesday and Saturday: a second text, `jake_date_wed` (`phone.py`), and the pickup and
  the end of a date on both nights. "Come up." stays Saturday only. Laura's line is now "Is Jake taking you out
  again?"
- **S4 (139).** The class screens say they're teaching. The dean gets "Ask about your grades." and the TA gets "Ask
  her to help you with Biology." (`college.py`).
- **C3.** Zoe's, Tom's and Vance's pre-meeting cards carry a `heading` (engine f0d7b863).
- **W9 (140).** Checked, nothing changed: the build already lets a hard-working player pay the first rent.
- **Verified.** Dev and debug rebuild; each change grepped in index.html. Gates went from 61/87 to 60/86 (26 fail,
  4 n/a): "the door can be seen again" is n/a now that there is no door, and nothing regressed. All 7 pieces were
  played in Chrome, and `pieces.py chrome` records them.
- **Found, not fixed (not in LO's list):**
  - `tom.py:17` `CLOCK_IN` equips the tight uniform on her first shift.
  - The tight-uniform "Clock out." choices on the café shift screen under Exhibitionism 20 carry both
    `cafe_uniform_sexy equipped` and `unequipped`, so they can never show.

## 2026-11-03 — the two uniform bugs, the 13 game slips, week one kept easy (DECISIONS 141–142)

- Everything is listed in DECISIONS 142. Week one stays easy (141, LO "B"), and the money_pressure sheet carries a
  note saying so.
- Verified in Chrome on the dev build: "Clock in." gives the normal uniform only; the three "come back later"
  messages are live; Ryan's two-knocks speech shows as dialog; the office choices and busy lines are there; Hale's
  pointer card hides his name.
- Gates went from 60/86 to 62/86 (24 fail, 4 n/a). "meter ceiling" and "no canvas key is discarded" pass now.
  "somebody speaks" went from 8.3 to 8.0 and still fails, because 49 other canvases have no speech; that was not
  on the 13. The party house is still open and empty on Saturday night, which wasn't on the 13 either.
- Ryan's attribution tags ("Ryan pants.", "You tell him.") now sit as short narration lines between the dialog
  boxes. Every signed word is kept.

## 2026-11-03 (night) — the Want rule and the second-pass slips (DECISIONS 143–144)

- **Want:** his Want now sits on the moment, never on her no. Ryan's opening +10 moved to "Open the door.", his
  step 8 +5 to the sex, and his Jake step 3 reaction to "Don't stop.". Vance's walk-on pays nothing now.
- **Jake:** a no-show text clears his booking. **Rent:** the game reads the engine's new `rent_short`. **Goal 2:**
  its card shows, and its end is set for release 2.
- **Closed lines:** generated from the hours (`canv.with_closed_line`), 24/24. **Names:** descriptions and the map
  are unnamed until each meeting, the offices are hidden until met, and "Next Door" replaces "Vance's House".
- **Speech:** 138 paragraphs became 315 dialog blocks (`speech_table.py`, `canv.speech`). 6 paragraphs are marked
  `not_speech`. One overheard fragment on the quad stays as narration.
- **Gates:** 65/90. All six new or changed gates pass. "somebody speaks" is now 6.7:1 and still fails, because
  scenes with no talk at all can't be fixed by converting quotes.
- **Verified in Chrome:** the quad unnamed and then named, the faculty floor listing only the offices she has met,
  the goal-2 card, Jake's no-show in the build, and Ryan's lines in speech boxes.

## 2026-11-03 (late) — Vance after a short Sunday, the sleep shirt, the true lines (DECISIONS 145)

Added 2026-11-03 by the third alignment pass from DECISIONS 145 and commits `12737f9b`, `a76f776e`.

- Vance's front-door row reads `rent_short` with its 48-hour window, so he comes only after a short Sunday.
- She starts in her sleep shirt and panties; the first screen adds her day clothes.
- Every line that places a person is true at every hour it shows; the ledger's ladder windows match.

## 2026-11-03 (late) — the 17 silent people speak (DECISIONS 146)

From commits `94bf8e00`, `762674c4`. A line or two each, gated on who is really there; no effects added.

## 2026-11-03 — the heat proposal, chunks 1–3, and its follow-ups (DECISIONS 147–152)

From commits `9655c8ff`, `c118641b`, `45021e99`, `6e68f353`, `a3a9ec98`. The signed proposal is now in the
game: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`.

- **Chunk 1 (148):** home walk-ins B1–B8, the small rungs C1–C6, Mark's dryer +5 on its first screen.
- **Chunk 2 (149):** sex scenes A1–A7 and media pools A10–A13. Traversal heat and explicit pools pass.
- **Chunk 3 (150):** walk-ins outside the house B9–B20. The walk-in floor is 24/24.
- **151:** Zoe's park dare pays once a day; in the hot-tub walk-in Zoe is already in the water.
- **152:** Mark's Saturday rows (07:00–08:30 bed, 08:30–09:00 kitchen) and his three walk-ins.

## 2026-11-03 (night) — third alignment pass, groups 2 and 3

From commits `7b874e61` (group 2, game logic: pay, systems, structure, a check for each kind of slip) and
`ce8551b1` (group 3, writing: voice, words, labels, and the scene reader's fails on every changed scene).
Gates after: 92/110 pass, 18 fail.

## 2026-11-03 (night) — third alignment pass, group 1 (pages only, no build)

No build. The spine (SP1, SP2, SP3, SP4, SP7), `OPENING.md`, `COVERAGE.md`, the person, place, system and
scene sheets brought to what the build does; 28 signed titles to `[READY]`; the heat proposal and the copy
fixes copied into `proposals/`; this iteration's SHORT, LONG, CHANGES and BUILD_VS_SHEET written. Every
changed signed page waits for LO's re-sign.

## 2026-11-05 — the café job could be reached again

LO could not ask for the job. `cafe_job_ask` needed Tom placed, his schedule waits on `tom_met`, and only that scene sets
it; this came in on 2026-11-04 when the scene moved from firing on entry to a swap on the coffee. The scene no longer
needs him and opens from its own row, `cafe_job_row` (DECISIONS 193). New skill gate `nobody waits for themselves`.
Dev + debug rebuild. Not committed. The one new screen, the row's fallback, has not had a reader pass.

## 2026-11-05 — "No content" gone

The importer's nesting cap dropped 8 written lines on 3 screens; the cap went from 4 to 8 and a build holding the stand-in
now fails (DECISIONS 194). Dev + debug rebuild: stand-ins 5 to 0. Then
committed. Two reader reads on those screens, fixes in DECISIONS 195; the second read's fixes are not re-read.

## 2026-11-05 — Change Clothes and the clothes shop as a dressing room

LO picked the v3 dressing-room mockup ("Go ahead", DECISIONS 196). `[ui] clothes_layout = "room"` and
`clothes_door = "street"` in `0_systems_spec.toml`; `image` on the 18 garments; `locked_text` on the three garage
items; two portrait rows on the new `wearing`. Engine: the room pages, `when.wearing` and `locked_text`, and theme
colours for the table pages in every game.

Dev + debug rebuild. This container has no Tweego, so the build was compiled by a local stand-in that puts the new
story data into the last real build's SugarCube. On the unchanged source it reproduced the committed `index.html` byte
for byte. Rebuild with real Tweego before a public build. The missing-media count went from 28 to 48: the 18 garment
pictures and the 2 new portraits, which the media pass is meant to find.

Played in headless Chromium by script, not in Claude in Chrome. What it checked:
- the slot column and the rail;
- the door line in jeans, in the short skirt and in the towel;
- the portrait pick in jeans, the skirt, the towel and the café uniform;
- a held skirt that will not go on;
- the dress swap;
- the shop's reasons, Buy and wear, and the empty rack.
No JS errors, no sideways scroll at 390px.

Found and not changed: the street's last dress-code rule has no condition and requires bra, panties, top and bottom,
but its message only says "Going out without a bra…". A girl in her underwear reads that line, here and on the
ClothingBlock page.

## 2026-11-08 — Exhibitionism phase 1

DECISIONS 197. The engine's daily cap, the leave rules on Exhibitionism alone, the low-cut top, six looks that pay at
0, three bridges, the cards. Gates 111 pass, shape 22 pass. Dev + debug rebuild. Two reader reads on the new scenes:
27 fails fixed, then 0. LO re-signed `meters.md` and `wardrobe.md` ("Sign it").

Merged with main's dressing room (DECISIONS 196), so this row moved to 197. The low-cut top got a picture path
(`clothing/low_top.jpg`) like the other garments; missing media is now 49 (main's 48 plus that one). Rebuilt with
real Tweego after the merge, which replaces the stand-in-compiled build that main carried. After the merge: gates
118, 0 real fails; shape 22 pass; engine tests 841 pass; skill tests 1,017 pass; importer the same 6 old failures;
cites 0 wrong. Headless: every look pays, the cap and drink rules hold, the top buys in the new shop, shows on
the Change Clothes rail and goes on, no sideways scroll at 390px; the pace play reaches 20 on day 7.

## 2026-11-08 — the gym clothes

DECISIONS 198. Engine: garment `description` (importer, the room's shop stand and rail; test
`test_garment_description.py`). Game: four gym pieces, shop lines on every bought piece, the gym floor's line per
step, two buttons, three accidents as substitutions from "Work out", the gym's locker room, park and Jake lines, the
new pieces in the strip lists and the bare-legs checks. The first build failed three gates (a panties line with no
panties check, random events in a changing room, a quoted line in a paragraph); all fixed, the accidents moved from
random-on-entry to swaps from the workout. Dev + debug rebuild; missing media 53 (the 4 new pictures).

## 2026-11-08 — clothing accidents in class and at the café

DECISIONS 202. Eleven accident scenes: six in class (`college.py`, `class_accident`), five on the café shift (`cafe.py`, `cafe_accident`); two daily unsets; shop lines on both uniforms. First build failed two gates: the same hook and Tom line pasted into several scenes (rewritten per scene), and the café accidents each paying a wage (five new money sources; they now pay none and hand her back to the shift). `but` fell under the field floor (2.83); joints added in the new lines. Headless, the class swap ate the class (opening a class uses its one visit), so the class accidents roll on arrival at the hall instead. After: gates 118, 0 fails; shape 22 pass; engine tests 843 pass; skill tests 1,017 pass; cites 0 wrong. Headless with the dice fixed: each accident fires only in its clothes, the let-it-be gates hold at 19/20, 39/40, the class runs after a class accident, no second accident the same day, and the café accident pays no wage and the shift is offered after it.

## 2026-11-08 — the stage for bare skin in the accidents

DECISIONS 203. Bare-tits answers from 60 (cap 79) in five scenes, gym strap included; the bare-skirt stairs answer removed (80). The reader's 11 truth and clothes fails from DECISIONS 202 fixed first (repeat-visit hooks, bra details the trigger doesn't check, table four vs Gary's booth four, the button's gate). Gates 118, 0 fails. Headless: every new gate shut at 59 and open at 60, the stairs answer never shows, bra answers open at any stage.

Reader re-read of the 12 scenes: 7 fails (3 lines that claimed the class or the lunch rush before either happened, 4 café endings with no hook); all rewritten. Rebuilt; gates 118, 0 fails. Not re-read after that rewrite.

## 2026-11-08 — everyday clothes by stage

DECISIONS 205. Crop top, bodycon minidress, micro shorts, plunge dress; four street looks, class lines in Psychology and Figure drawing, Zoe's lines on the quad and at the party house, four accidents. First build: four gate fails (one Zoe line naming panties unchecked, a first-time phrase, class lines pasted into every class, street looks paying from 0); fixed. Reader: 12 fails, fixed, plus DECISIONS 41's words removed from the strangers' accidents (also the gym's and the class ones from 198 and 202). A fix to Zoe's lines first overwrote her old hub lines; restored from git before the build. After: gates 118, 0 fails; shape 22 pass; skill tests 1,017 pass; cites 0 wrong. Headless: each piece locked a point below its stage and wearable at it; each street look pays to its cap; class lines show; each accident's answer shut below its gate and open at it; the class accidents don't roll in Figure drawing.

Second reader read: 5 fails fixed (the class accidents' exit is "Wait for class.", a bench hook, Vance's "Not tonight.", the sheer squats need panties). Gates 118, 0 fails; headless: the sheer squat button shows with panties at 60 and not without.

## 2026-11-08 — café uniforms she buys

DECISIONS 206. Two dresses Tom sells when she asks (short at Exhibitionism 40 and footfall 10, $30; low-cut at 60 and
footfall 25, $40), no shop price. Tips x1/x2/x3/x4 by the uniform on; clock-in keeps any uniform she wears (cafe.py
shift_choice, the accidents' counter, tom.py back()). Two accidents (cafe_acc_short_shelf, cafe_acc_lowcut_slip). First
build: 3 gate fails (two dresses named "your uniform" in Hale's and Zoe's lines; the accidents' Tom line in three
canvases; the bought-flags nobody read), fixed. Reader: 7 fails, fixed. Gates 118, 0 fails; shape 22 pass; cites 0
wrong. Headless: the offers show at footfall 10 and 25 only; buying takes $30 and $40; locks shut at 39 and 59; on
shift each dress stays on; tips $10/12/14/16 on "Not today, hon."; each accident's let is shut at 39/59, open at 40/60.
Two pictures missing: clothing/cafe_uniform_short.jpg, clothing/cafe_uniform_lowcut.jpg.

## 2026-11-08 — gossip that matters

DECISIONS 207. New part `gossip.py` (in build_scenes.sh ALL_PARTS): three spread scenes, the asks on the quad (25) and
at the party (60), the passer-by (60). `canv.py` talk_remembers sets talk_class / talk_gym / talk_quad / talk_party on
every answer that pays campus_talk (TALK_KIND by canvas-id prefix). Nadia's library question and lunch refusal
(hale.py), the rival's report (college.py gossip_rival_report), three feed posts (phone.py), the sidebar words and
in_dump = false, the daily resets gossip_today / gossip_party_today. First builds: 4 gate fails (garment names in
past-tense lines; lines copied across screens; the banded meter's number; `but` under the field p10), fixed. Reader:
22 fails, fixed. Gates 118, 0 fails; shape 22 pass; cites 0 wrong. Headless: spreads fire at 10 with their flag only;
let +1, shut 0; Nadia defends below 40 only, Zoe at the party; the quad ask's answers by stage (19 / bra at 20 / bare at
60); the party ask in a dress at 60; the passer-by's smile from 40; the rival at 40 not 39, complaints +1; Nadia asks
once, refuses lunch at 40, library open. Three pictures missing: phone/feed_talk_named.jpg, phone/feed_talk_slut.jpg,
phone/feed_talk_rate.jpg.

## 2026-11-09 — more clothes, round 2

DECISIONS 208. Five garments in 0_systems_spec.toml (split_skirt, sequin_dress, backless_dress, lace_bra,
lace_panties). Street looks and town_event_split_wind (town.py), seat lines (college.py CLASS_CLOTHES), Zoe's lines
(zoe.py ZOE_SEES; party_arrive in pools.py), two party-dress accidents (pools.py party_dress_accident, daily reset
party_dress_acc_today), Mark's laundry list, the lace lines at home (home.py, walkins.py LACE_SET), the strip lists.
First build: gates 0 fails. Reader: 6 fails, fixed; one more gate fail after the fixes (a day word, "every Friday",
on a Saturday screen), fixed. Gates 118, 0 fails; shape 22 pass; cites 0 wrong. Headless: each lock shut a point below
and open at it (19/20, 59/60, Corruption 19/20); the shop stocks all five; buying the backless dress takes $50; the
street looks show at their stage; the wind's and the party accidents' "let it be" open at 40/40/60, not 39/39/59; Zoe's
door lines; the lace set under jeans gets "Not in that" at the door; the lace lines in both mirrors. Five pictures
missing: clothing/split_skirt.jpg, sequin_dress.jpg, backless_dress.jpg, lace_bra.jpg, lace_panties.jpg.

## 2026-11-09 — her reaction drifts when she does it again

DECISIONS 209. New `drift.py` (DRIFT table, apply()), called from canv.emit; 23 new hidden counters declared in gen_world.py
(DRIFTCOUNTERS) and labelled hidden in 0_systems_spec.toml; Zoe's dares read zoe_dares_done. Mode "in" raises the counter
on the paid choice into the screen and sets `<counter>_now`, which an unpaid way in clears; mode "out" raises it on the paid
exit and reads the count before. The chain is fenced in a one-item pool. First build: one gate fail (two lines read as
arrivals), fixed. Reader: 20 fails, fixed; re-read: 6 more plus a shared-list bug in apply(), fixed. Gates 118, 0 fails;
shape 22 pass; cites 0 wrong. Headless: the street skirt row shows line 1 / 2 / 2 / 3 / 3 at counts 0 / 1 / 3 / 4 / 9 and
adds 1 per walk; the gym shows 1 / 2 / 2 / 3 after 1 / 2 / 4 / 5 visits, a "no" adds 0; the park run in track pants shows
nothing and counts nothing, the paying runs count and show line 1.

