# Build vs sheet — first_term 0.1, overnight build 2026-10-08/09

Every place the build does something other than a signed sheet says, and why. LO reviews this list.
Rules used (the batch prompt): a sheet against the skill → the sheet; two sheets → the later or more
specific; the engine can't → the closest version that works; a ledger change → made after a snapshot.

## Piece 1 — the world skeleton

| # | the sheet line | what I built instead | why |
|---|---|---|---|
| 1 | home_ella_room: sleep "the clock to 07:00" | sleep lands between 06:30 and 07:29 | the engine moves the clock by minutes only (`engine.md` §32.1); one choice per hour of bedtime, each sized to land near 07:00 |
| 2 | home_ella_room: sleep "energy set 100 · once a night" | `room_sleep` 19:00–06:00 sets energy 100; a separate `room_nap` 07:00–19:00, two hours, energy +30, once a day | a bed at noon needed an answer; the nap is the closest thing that keeps "once a night" true |
| 3 | needs: "at zero she falls asleep and wakes next morning" | not built: at 0 energy every energy-priced choice greys out with its need; she can still go to bed | no engine hook fires on a trait reaching 0 |
| 4 | cafe: open Mon–Sat 08:00–22:00, "after 22:00, only by staying for Tom" | the café's hours are 08:00–23:00; shifts stop at 22:00 (piece 4); 22:00–23:00 only Tom's close scenes | the engine shows the closed screen on any re-entry after closing, so Tom's 22:00–23:00 step could never fire inside a 22:00 close |
| 5 | wardrobe: "leaving a room in it needs Exhibitionism" (per state) | `clothing_rules` on every public place: a towel or the sleep shirt never goes out; a short skirt needs Daring; no bra needs Daring; no panties needs Showing; top and bottom always (underwear-only stays home) | the engine has no "leave the room" hook (`engine.md` §17); a destination's dress rule is the closest place to put the price. A towel/sleep-shirt block uses a slot nobody owns ("legwear") because a dress-slot garment satisfies top and bottom |
| 6 | the park: "Daring: a sports bra only" | the park's rule lets her out in a bra (any bra) with no top at Daring | `clothing_rules` checks slots, not garments |
| 7 | wardrobe sheet: change clothes "1–2 clicks" anywhere implied | `wardrobe_anywhere = false`; she changes in her room, the café's back room, the women's toilet, or Zoe's bedroom | with it on, every dress rule is one click from met (`engine.md` §17, "the loophole") |
| 8 | money in the sidebar | money shows in the sidebar's trait list as "Money N", not as a banded row | a banded money row cannot carry `clamp = false`, and money above 100 needs it (`engine.md` §21) |
| 9 | home_master_bedroom door: "Knock · Go in (when both are out)"; Laura or Mark answers | "Knock." (someone in) enters the room; "Go in." (nobody in) enters | a door option must point at a located canvas or `enter`; who answers is the room's own rows (Laura dressing, they're asleep) |
| 10 | the street's way home at 22:00 or later sets `came_home_late` (DECISIONS 35) | a door on the hall, seen only from the street: "Go in." 06:00–22:00, "Let yourself in." 22:00–06:00 plays a short screen and sets the flag | the only engine surface that knows she came from the street. "Leave Kitchen" and the other back-links skip it, so walking into the hall from inside never sets it |
| 11 | people sheets: four classmates with role "classmate" | roles made unique: "Psychology classmate" (Nadia), "the next desk", "rival classmate", "Business classmate"; Zoe's "her friend" became "college friend" | the importer refuses two people with the same role label |
| 12 | names "the art lecturer", "the guy beside her" etc. | capitalised for the name box ("The art lecturer"); "the guy beside her" printed as "The guy beside you" | the name prints at the start of a dialogue box; second person |
| 13 | LIVES §6: everyone but the family hidden until met | every non-family schedule row carries `when` on that person's met flag | LIVES is signed and the sheets say nothing against it |
| 14 | Ryan's Saturday 18:00–22:00 row (`ryan_cancelled_kayla`, "later, Ryan A 12") | not built | marked for a later release in the ledger |
| 15 | the corner shop, the men's toilet | not built | not in 0.1 (SP7) |
| 16 | her face (`[player_portrait]`) | slots declared with placeholder file names; no look chosen | DECISIONS 1: chosen with the media pass. No media was searched for |
| 17 | Jake's thread: "after step 4: every 7 days" | the date text repeats weekly from the first text | Jake's steps 3 and 4 both need a booked date, so the booking has to repeat before step 4 |
| 18 | the phone's texts naming an hour ("2:30", "8. the park", "kitchen. six") | kept as the sheets wrote them | a text is the world naming a rule of its own (`the-clock.md` C2 exemption) |
| 19 | OPENING.md: the start-choice flags `college_for_*`; the ledger's `want.player.start_choice` said `start_wants_*` | used the sheet's names; **ledger change**: `want.player.start_choice.flags` and `asked_at` updated (snapshot `20261008_build_piece2_before`) | two sources disagreed; the signed sheet is more specific |
| 20 | sleep shirt and towel `initial` in the wardrobe | given in the opening's first screen instead (`wardrobeEffects add`) | an `initial` dress-slot garment is worn over everything at the start (the engine equips one item per slot) |

## Piece 2 — the opening, the home, Ryan

| # | the sheet line | what I built instead | why |
|---|---|---|---|
| 21 | ryan_01 sheet: "Knock next time" — "his next step waits three days" | no wait | the ladder gate refuses any trigger condition the ledger doesn't declare; a wait would need a declared gate item |
| 22 | ryan_01: the final no sets `ryan_01_hall_first_morning_closed` | that, and `ryan_step` set to −1 | the step counter at −1 closes every later step without an undeclared condition (same for every person's final no) |
| 23 | ryan_08: exits "Two knocks." → the hall; the ledger door is the choice "Two knocks" | the open exit is "Go back to your room."; "Two knocks" is the locked door choice (Corruption 60, the engine prints the need) leading to an honest "next release" screen | two choices labelled almost the same on one screen would read as one; the door gate needs the exact label "Two knocks" |
| 24 | SP7: the locked button "naming Hungry" | it names "Corruption 60" (the engine's own suffix) | a pure number lock may not carry a `locked_text` (gate `a locked door says why`) |
| 25 | ryan_05: after the step, "Take the shower" → the bathroom, Sat 08:00 | "Wait your turn, then take the shower." lands between 08:00 and 09:00 | so Saturday's step 6 (08:00–10:00) can fire; the clock moves only by minutes |
| 26 | ryan_06 voice line "I heard you last night" | "I heard you through the wall" (re-measured: 148 words, 6 explicit, median 12) | the step can fire on a later Saturday (its own 7-day retry), so "last night" could be false (the reader) |
| 27 | ryan_02: "he has had twenty minutes" (my line) | "he's had the bathroom long enough" | the reader: it can be fifteen |

## Piece 3 — Laura, Mark, Tom, Zoe, Hale, Jake

| # | the sheet line | what I built instead | why |
|---|---|---|---|
| 28 | laura_01: node `kitchen` (Laura washing up: "Come upstairs") then the bedroom | the "Come upstairs" line and a "Follow her upstairs." choice live on Laura's kitchen hub on Tuesday evenings; the step canvas fires in the master bedroom | the ledger puts the step in `home_master_bedroom` and the ladder gate checks the place |
| 29 | the curfew: "read by days since set, 7" | a counter `curfew_days` (7 when set, −1 each night in the daily tick); the flag `curfew` is still set | a gate can't be "A and (curfew older than 7 days)" — no nested conditions (B70) |
| 30 | Laura's curfew call: "she is out after 23:00" | it rings 23:00–01:00 under the curfew when `came_home_late` isn't set; answering returns her to her room | the engine has no "player is out" condition |
| 31 | mark_01: "The thirty-five waits a week." | "The rest waits a week." | the short amount isn't known; a number that can be wrong breaks the truth rule |
| 32 | the money sheet: Mark's table counts the streak | the count runs on whichever Sunday scene plays first (his steps 1, 3, 7 or the table row), once per Sunday | so a step Sunday still counts; `sunday_counted_today` stops a double count |
| 33 | Ryan's cover "what she's short" | he gives a fixed $25 | the engine can't compute the shortfall |
| 34 | Vance's knock "the next evening, Monday" | any evening Monday–Saturday while `rent_carried` is set, at the front door | a carried week has to be reachable when she's home; once per carried week |
| 35 | the twist's offer: who makes it | Mark, at the kitchen table with every letter out, after `pays_her_own_way`; both answers park; "It's not my debt" also sets `debt_refused` | DIRECTION §2; "her answer stays parked until 0.2" |
| 36 | the café's two uniforms | both carry the garment type `cafe_uniform`; the tight one is named "Tight café uniform" | one type lets a scene check "in uniform"; a name must end on the garment (B72) |
| 37 | Tom's steps happen "on shift" | each Tom step opens in the back room, where she puts the uniform on | the truth rule: the uniform is named on his screens, so it must be worn first |
| 38 | Gary's "met: Tom B 4" | Gary speaks one line at the end of step 4 ("Thursday, sweetheart. Same booth.") | "every hub is met first" needs a meeting scene that names him; added to a signed screen's after-beat, not to the explicit one |
| 39 | hale_02: the flash, "she doesn't fix her skirt" | in a skirt she uncrosses her legs; in jeans or leggings she pulls her waistband down an inch; either way the panties come off first | the reader failed a skirt line in jeans; the step stays reachable in what she owns |
| 40 | hale_04: "There is nothing under them" | "Undo it." takes her bra off first | the signed prose claims it; now it is true |
| 41 | Jake's date | a pickup canvas at the front door, Saturday 19:00–21:00, booked by his text; it lands her back at the door after eleven where his steps and the goodnight play | the sheets have the door, not the date itself |
| 42 | the Thursday repeat's "seven-twenty" | "when the twenty minutes are gone" | the repeat window opens 18:30; the clock line could be false |
| 43 | every parked no | a short reply screen, then the parked exit | the reader's test 6 (B74) |
| 44 | Mark's hubs | split by room (the living room, the garage, the kitchen, asleep in bed) with their own leaks | the reader: one shared set of leaks was false in three rooms |

## Piece 4 — the pool and system scenes

| # | the sheet line | what I built instead | why |
|---|---|---|---|
| 45 | the class rows "once per class window" | once a day per subject (no subject has two windows in a day) | `max_triggers_per_day` is the engine's cap |
| 46 | the class "Skip" row | "Skip it." leaves to campus with the grade −2 | she is already in the room when the class shows |
| 47 | the lecturers met "at their first class" | a one-time first-class scene for Business, Biology and Figure drawing (the cocky guy and the model are met at Figure drawing); Hale and Nadia at Hale's step 1 | the class rows repeat, and a hub must be opened by a one-time meeting |
| 48 | the midterms "weeks 7–8, once per exam", result reads `intelligence` + grade | one-time scenes in each subject's slot from day 42 to 56; Focus adds +6 with intelligence 10+, +1 below; copying +5; the result bands read the grade | conditions can't add two traits |
| 49 | the failing chain: Laura reads the grade | one row per subject in her evening kitchen when that grade is under 40, once a week (cleared at the Sunday count); suspicion +5, the curfew at low Warmth or suspicion 45+ | no "any grade under 40" condition (no OR inside AND) |
| 50 | probation "a week after the result" and the dean | the dean's office calls (a complaint call after two complaints, a grades call a week after Laura saw a failing grade); the warning sets probation if failing and sends the letter home (suspicion +10) | the calls are the npc_dean sheet's "his office calls her in" |
| 51 | the party's "something short" | `worn_beauty` 2 or more (the short skirt, Zoe's dress, Laura's dress, the tight uniform) | one condition instead of three |
| 52 | the heavy night: "her Saturday bed scene" | sleep now ends on a morning screen; after a heavy night it reads the hangover and takes 30 energy | no canvas can auto-fire every time; sleep is where the morning is |
| 53 | the park's "strangers see her on purpose" locked button | "Let strangers see. (Needs Hungry)" on the walk | as the park sheet |
| 54 | the stairs event "a short skirt or no panties" | in a short skirt (no panties is a line inside it) | a trigger can't be OR plus another gate |
| 55 | `party_hookup` "once a night" | once a day (`hookup_today`, cleared at midnight) | the party crosses midnight; a night cap would need a party counter |
| 56 | the Figure drawing class "posing for the class: Needs Hungry" (SP7) | "Pose for the class. (Needs Watched)" | SP2 §1: posing for the class turns on how many see her: Watched |
