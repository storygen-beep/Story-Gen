# False lines, pass a3 — signed 2026-11-02 (LO: "Signed")

> **Written 2026-11-02** (LO: "1", fix the old reader fails, false lines first). Source: the a2 reader pass,
> `~/Documents/Great_Games_Study_20260926/round12_tease/first_term_reader/reader_a2_{home,college,out}.md`, tests
> "true on every visit it can render on" and "the numbers and the clothes agree". 30 fails; each quoted line was
> grepped against the build of 2026-11-02 (`toml_phases/7_final_game.toml`) and 29 are still in it. The loop's
> "Ryan? Are you up?" was already rewritten today (the headboard wakes Laura); its 22:00–23:00 twin is item 8.
> The other reader tests (want, the written no, low heat: about 60) are not in this pass.

**Kind:** prose = a line's words change · gate = a trigger or button condition · row = a schedule row · clothes = a
wardrobe effect.

## Home (8)

| # | canvas | the line | why it's false | the fix | kind |
|---|---|---|---|---|---|
| 1 | `bathroom_shower` | "You soap yourself slowly, all of you, because the door's locked. Nobody can see" · "This time he doesn't look at the floor" | on a visit where Ryan's peek group shows (Sat 10:00, Ryan in his room), the pool says nobody can see right after he looked; "This time" sits right after "He looks at the floor" | both lines hide on the visit the peek group shows (that group's gate, negated) | gate |
| 2 | `garden_sun` | "lie back with your eyes shut" then "Topless, on your front" | the topless visit puts her on her back, then on her front | the opener says "lie down with your eyes shut" | prose |
| 3 | `mark_03_shorts` | "Sunday. Mark's at the table with the envelope ... You don't wait to be asked." | at Mark's Power under 50 and her Exhibitionism under 20 no button shows (the only one needs E20): no exit | add the parked no "Not today." (the step comes back next Sunday) | gate |
| 4 | `ryan_01_hall_first_morning` | "A café on your street with a sign in the window." | the café is in Town, 15 minutes from your street; WANT.md calls it "the café near campus" | "A café near campus with a sign in the window." | prose |
| 5 | `ryan_01_hall_first_morning` | "The café on your street is hiring." | as 4 | "The café near campus is hiring." | prose |
| 6 | `ryan_06_after_the_shower` | "It stays that way." | a promise his door stays open; the built door is "A strip of light under it" and only knocks | cut it; the line before ends the screen ("He doesn't shut it all the way.") | prose |
| 7 | `ryan_07_kayla_cant_know` | "It's been open a hand's width every evening since the shower, and you both know why." | no surface shows his door open after step 6 | "His light is on under his door, and you both know why you're here." | prose |
| 8 | `ryan_08_two_knocks_first_sex` (`light`, `keep`, `freeze`) | "Across the hall, a line of light comes on under Laura's door." | 22:00–23:00 Laura is awake alone with her lamp on: there's no light to come on | the near-catch is a sound: her floorboards creak across the hall; `keep` ("the creak stops at her door") and `freeze` ("her steps go back") follow it. Three explicit beats edited and re-measured | prose |

## Out (8)

| # | canvas | the line | why it's false | the fix | kind |
|---|---|---|---|---|---|
| 9 | `cafe_coffee` | "Nobody here knows you when you're not in the apron. It's strange how much that changes." | shown only before she's met Tom: she's never worn the apron | "Nobody here knows you." | prose |
| 10 | `cafe_shift` | Gary: "Same booth, sweetheart. Same time." | `gary_let_it` is set on every L3 clock-out with Gary there, but his pool also draws the strangers' screens ("You drop onto his knee and the back table roars."): he claims a touch that didn't happen | with Gary in, the L3 screen is his (`L3_B` only); the strangers' two stay for the shifts he isn't there. Costs variety: his shifts show one L3 screen | gate |
| 11 | `hub_tom_cafe` | "the black top, tighter than the dress and cut for your tits" | the tight uniform is a dress-slot garment | "the black dress, tighter than the other one and cut for your tits" | prose |
| 12 | `shop_try_on` | "But you'd need to be Daring to walk out the door in it." | the street opens the skirt at Corruption 20 or Exhibitionism 20 | "But you'd need to be Curious or Daring to walk out the door in it." | prose |
| 13 | `shop_try_on` | "In the park, at Daring, you could run in just this with leggings. Everybody on the path would get a show." | not built: the street needs a top, so she can't get to the park in a sports bra | cut the line | prose |
| 14 | `street_seen_nopanties` | "A breeze comes down the street as you pass his gate, and there's nothing under your clothes to stop it." | the trigger is no panties in any bottom; in jeans or leggings no breeze reaches her and Vance sees nothing | the trigger also needs a skirt or a dress | gate |
| 15 | `tom_03_not_by_the_window` | "When you come off the floor Tom is in the back room" | a morning shift's "Let it." fires this at 14:30 when she walks in from town, not off the floor | the trigger also needs a clocked-out shift within the last 30 minutes | gate |
| 16 | `vance_meeting` | "Next door, on his porch, the man who owns your house: Mr. Vance." | Monday 18:00–19:00 after a carried rent his row puts him at your front door, yet this fires with him on his porch | the trigger also needs him present on his porch | gate |

## College (13)

| # | canvas | the line | why it's false | the fix | kind |
|---|---|---|---|---|---|
| 17 | `college_class_figure` | "At the next easel, the cocky guy isn't drawing the model. He's drawing you." | the cocky guy's only rows are Zoe's flat, Fri 23:00–Sat 02:00 | give `npc_cocky_guy` rows in the lecture hall at Jake's class times (Tue/Thu 08:00–10:00, Wed 13:00–15:00); the prose stays | row |
| 18 | `college_exam_art` | "Jake's teammate is at the next desk with his paper finished" · "Show me and I'll tilt my paper." | as 17 | as 17 | row |
| 19 | `meet_figure` | "The guy at the next easel is in a team jacket: Jake's teammate, the cocky one." | as 17 | as 17 | row |
| 20 | `hale_01_first_lecture` | "beside a girl with big glasses ... 'Sit here. I'm Nadia.'" · "At the lectern a man in a tweed jacket" | a Wednesday Psychology class can meet both first; this screen then introduces them as strangers | the two intros split on `nadia_met` / `hale_met`: met, "Nadia waves you over to the free seat beside her." and "Dr. Hale is at the lectern" | prose + gate |
| 21 | `hale_04_claire_knocks` | "You ready, love? I'm early." | the trigger runs to 19:30 and the knock comes 10 minutes in, so from 19:20 she's at or after the 19:30 pickup: not early | the trigger ends at 19:15 | gate |
| 22 | `hub_hale_office` | "Goodnight, Dr. Hale." | his office opens Thursday 17:00 | "Bye, Dr. Hale." | prose |
| 23–26 | `hub_jake_canteen`, `hub_jake_class`, `hub_jake_gym`, `hub_jake_quad` | "Everyone was looking at you tonight." | behind Laura's blue dress, at his daytime rows (08:30, noon, 15:00) | "Everyone's looking at you in that dress." | prose |
| 27 | `zoe_02_bra_through_the_sleeve` | "You reach up the back and unhook it" | "Watch me." reads only a bra on; a sports bra doesn't unhook | in a sports bra: "You drag the sports bra up and off through the sleeve." (a clothing group on `sports_bra`) | prose + gate |
| 28 | `zoe_03_hot_tub` | "You let yourself in. The house is dark, and your hair drips on the mat." | "Go home" equips nothing: she walks home in panties while the prose has her dressed | "Go home" puts her clothes back on | clothes |
| 29 | `zoe_dares` | "topless in the kitchen till the song ends" · "Flash them, babe. Three seconds," | one dare, two lengths | one length, the song: "Till the song ends, babe." | prose |
| 30 | `zoe_park_dare` | "Two seconds" · "for one long second" · "Two seconds, that's all he gets." | one second in her prose, two in Zoe's mouth | "for two long seconds" | prose |

(30 rows: items 4–5 are one canvas and 23–26 one line on four hubs, so 29 distinct fixes.)

## After the sign
Sheet first: each prose fix goes in the scene sheet the line is read from, or the build script if the line lives only
in code. Explicit beats re-measured with `gates.py --beat`. Then the build, gates against the baseline, a `v2-reader`
pass on these canvases (truth and clothes only), and a probe for the gate fixes (14, 15, 16, 21, 17, 28, 3).
