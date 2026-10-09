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
