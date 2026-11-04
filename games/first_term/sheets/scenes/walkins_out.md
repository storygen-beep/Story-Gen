# [REVIEW] Scenes — the walk-ins outside the house (B9-B20)

> Changed 2026-11-04 to match the build; waits for LO's re-sign. B14: "Strip and get in."; "Let her." needs Exhibitionism 60, pays both meters, costs Energy 10 and Hygiene 10.

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The built-differently items are confirmed, DECISIONS 170.

> New 2026-11-03 (third alignment pass), written from the build; waits for LO's sign. The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`, part B (signed by LO 2026-11-03, DECISIONS 147; built in DECISIONS 150-151).

How every walk-in works in the build: she does something alone; on entry the host rolls the odds; on a hit this screen shows instead. Screen 1 is the moment and pays his meter where he has one; screen 2 is her answer. The odds rise with her stage (0.25, 0.35, 0.45). Each walker comes once a day (a `_today` flag cleared at midnight).

Built differently from the proposal (DECISIONS 150), confirmed, DECISIONS 170: B10-B13 and B15 fire in the first 15 minutes of the walker's row; B11 is split by weekday; B16 Hale comes in at the start of his own lecture; B20 Hale in his office hours; B19 needs bare legs.

## B9 · `walkin_cafe_gary`

| row | answer |
|---|---|
| host · who | `cafe_coffee` · Gary |
| when | Mon/Tue/Wed/Thu/Fri 14:30-18:00; Fri 20:00-22:00 · odds 0.25, 0.35, 0.45 |
| want | he sits on the stool next to hers: "Off the clock, doll?" |
| next step | his knee on hers; from Curious, his hand on her thigh |
| hook | his booth line reads `gary_sat_with_her` for 48 hours |
| the no | "Move your knee." pays 0 |

**`walkin_cafe_gary`** — Café · needs `opening_done` · not `walkin_cafe_gary_today` · Gary in Café · `gary_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You take the stool at the end of the counter with your coffee, off the clock … | no | "His knee finds yours." → `answer` | `walkin_cafe_gary_today` set · `gary_sat_with_her` set |
| `answer` | Under the counter his knee presses against yours, warm and heavy, and stays there. | no | "Move your knee." → `g_move` | — |
|  |  |  | "Leave it." (Corruption under 20) → `g_leave` | Corruption +1 (cap 19) |
|  |  |  | "Let his hand rest on your thigh." (Corruption 20+) → `g_hand` | Corruption +1 (cap 39) |
| `g_move` | You shift your knee away from his and pick up your cup with both hands. | no | "Finish your coffee." → Café | — |
| `g_leave` | You leave it. | no | "Leave him to his paper." → Café | — |
| `g_hand` | His hand comes off the paper and settles on your thigh, high up, big and warm. | no | "Leave him to his paper." → Café | — |

## B10 · `walkin_gym_team`

| row | answer |
|---|---|
| host · who | `gym_workout` · Jake's team (Jake at the front, once she knows him) |
| when | Tue/Thu 15:00-15:15 · odds 0.25, 0.35, 0.45 |
| want | a dozen of them stop and look at her on the bench |
| next step | "Finish your set." in her sports bra (Daring) |
| hook | none in the build: nothing reads `team_saw_gym` |
| the no | "Grab your things and go." pays 0 |

**`walkin_gym_team`** — Gym · needs `opening_done` · not `walkin_gym_team_today` · Tue/Thu · 15:00-15:15 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're flat on your back on the bench with the bar over your chest, alone in … | no | "They've seen you." → `answer` | `walkin_gym_team_today` set · `team_saw_gym` set |
| `answer` | The noise stops. | no | "Grab your things and go." → `t_go` | — |
|  |  |  | "Finish your set." (wearing sports bra · no top · no dress · Exhibitionism 20+ · Exhibitionism under 40) → `t_set` | Exhibitionism +1 (cap 39) · costs Energy 10 |
| `t_go` | You rack the bar, grab your bag off the floor and hug it to your sports … | no | "Keep walking." → Campus | — |
| `t_set` | You don't get up. | yes | "Leave them staring." → Campus | `worked_out` set |

## B11 · `walkin_canteen_zoe`

| row | answer |
|---|---|
| host · who | `canteen_eat`, `canteen_listen` · Zoe |
| when | Mon/Wed/Fri 11:45-12:00 · odds 0.25, 0.35, 0.45 |
| want | her hand on Ella's knee under the table |
| next step | "Let it stay." (Curious): her hand up her thigh |
| hook | none in the build: nothing reads `zoe_canteen_knee` |
| the no | "Move her hand." pays 0 |

**`walkin_canteen_zoe`** — Canteen · needs `opening_done` · not `walkin_canteen_zoe_today` · Zoe in Canteen · `zoe_met` · Mon/Wed/Fri · 11:45-12:00 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You've got a table by the windows to yourself, the lunch line building. | no | "Her hand finds your knee." → `answer` | `walkin_canteen_zoe_today` set · `zoe_canteen_knee` set |
| `answer` | Under the table her hand lands on your knee like it lives there, and squeezes. | no | "Move her hand." → `z_move` | — |
|  |  |  | "Let it stay." (Corruption 20+) → `z_stay` | Corruption +1 (cap 39) |
| `z_move` | You pick her hand up off your leg and put it back on her own. | no | "Leave her your drink." → Canteen | — |
| `z_stay` | You let it stay. | yes | "Leave her to her fries." → Canteen | — |

## B11 · `walkin_canteen_jake`

| row | answer |
|---|---|
| host · who | `canteen_eat`, `canteen_listen` · Jake and two of the team |
| when | Tue/Thu 11:45-12:00 · odds 0.25, 0.35, 0.45 |
| want | "Guys. Look at her." at her skirt |
| next step | "Leave it." (Covered); "Training's at three. Come and watch." |
| hook | none in the build: nothing reads `team_saw_canteen` |
| the no | "Pull your skirt down." pays 0 |

**`walkin_canteen_jake`** — Canteen · needs `opening_done` · not `walkin_canteen_jake_today` · Jake in Canteen · `jake_met` · Tue/Thu · 11:45-12:00 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You've got a table by the windows to yourself, the lunch line building. | no | "They sit down." → `answer` | `walkin_canteen_jake_today` set · `team_saw_canteen` set |
| `answer` | Your skirt has ridden up your thighs on the plastic chair. | no | "Pull your skirt down." (in short skirt) → `j_down` | — |
|  |  |  | "Eat your lunch." (not in short skirt) → `j_eat` | — |
|  |  |  | "Leave it." (in short skirt · Exhibitionism under 20) → `j_leave` | Exhibitionism +1 (cap 19) |
| `j_down` | You tug your skirt down your thighs, as far as it goes. | no | "Leave them to their trays." → Canteen | — |
| `j_eat` | You eat. | no | "Leave them to their trays." → Canteen | — |
| `j_leave` | You leave it. | no | "Leave them to their trays." → Canteen | — |

## B11 · `walkin_canteen_nadia`

| row | answer |
|---|---|
| host · who | `canteen_eat`, `canteen_listen` · Nadia |
| when | Mon/Tue/Wed/Thu/Fri 12:00-12:15 · odds 0.25 |
| want | none: she warns her about Hale |
| next step | none: one screen, no answer |
| hook | Hale's Thursdays, from someone who knows |
| the no | none: "Eat with her." only |

**`walkin_canteen_nadia`** — Canteen · needs `opening_done` · not `walkin_canteen_nadia_today` · Nadia in Canteen · `nadia_met` · `hale_met` · Mon/Tue/Wed/Thu/Fri · 12:00-12:15 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You've got a table by the windows to yourself. | no | "She leans in." → `answer` | `walkin_canteen_nadia_today` set · `nadia_canteen_hale` set |
| `answer` | She stabs a tomato and doesn't look up. | no | "Eat with her." → Canteen | — |

## B12 · `walkin_library_nadia`

| row | answer |
|---|---|
| host · who | `library_study` · Nadia |
| when | Mon/Tue/Wed/Fri 14:30-14:45 · odds 0.25 |
| want | none: she takes the desk with the plug |
| next step | none: one screen |
| hook | `nadia_knows_stacks` if she saw the stacks couple; nothing reads it |
| the no | none: "Get back to work." only |

**`walkin_library_nadia`** — Library · needs `opening_done` · not `walkin_library_nadia_today` · Nadia in Library · `nadia_met` · Mon/Tue/Wed/Fri · 14:30-14:45 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You've got a desk under a green lamp and the Psychology reader open. | no | "She leans over." → `answer` | `walkin_library_nadia_today` set |
| `answer` | She sees you glance at the back stacks, and her eyebrows go up. | no | "Get back to work." — 2 versions, by flags → Library | — · varies: `nadia_knows_stacks` set |

## B13 · `walkin_run_zoe`

| row | answer |
|---|---|
| host · who | `park_run` · Zoe |
| when | Sat/Sun 08:00-08:15 · odds 0.25 |
| want | she slaps Ella's ass at the park gates: "Race you." |
| next step | "Run with her." or "Dare me, Zo." (her park dare) |
| hook | her park run and dare |
| the no | "Let her run on." pays 0; Zoe answers it on `z_on` |

**`walkin_run_zoe`** — Park · needs `opening_done` · not `walkin_run_zoe_today` · not `walkin_rest_zoe_today` · Zoe in Park · `zoe_met` · Sat/Sun · 08:00-08:15 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're stretching against the park gates, bent over your knees, when somebody comes up behind you … | no | "You spin round." → `answer` | `walkin_run_zoe_today` set · `walkin_rest_zoe_today` set · `zoe_caught_up` set |
| `answer` | Zoe, in tiny shorts and a sports top, bouncing on her toes, grinning. | no | "Let her run on." → `z_on` | — |
|  |  |  | "Run with her." (10 Energy) → `hub_zoe_park` `lap` | `ran_with_zoe` set · `zoe_bailed` cleared · `zoe_run_booked` cleared |
|  |  |  | "Dare me, Zo." (top on) → `zoe_park_dare` `ask` | — |
| `z_on` | "Go on without me, Zo." · Zoe: "Your loss. You're still buying the coffee." She slaps her ass again and runs off | no | "Watch her go." → Park | — |

## B13 · `walkin_rest_zoe`

| row | answer |
|---|---|
| host · who | `park_rest` · Zoe |
| when | Sat/Sun 08:00-08:15 · odds 0.25 |
| want | her head in Ella's lap on the bench, her hand on her hip |
| next step | "Run with her." or "Dare me, Zo." |
| hook | her park run and dare |
| the no | "Let her run on." pays 0; Zoe answers it on `z_on` |

**`walkin_rest_zoe`** — Park · needs `opening_done` · not `walkin_rest_zoe_today` · not `walkin_run_zoe_today` · Zoe in Park · `zoe_met` · Sat/Sun · 08:00-08:15 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're stretched out on a bench by the pond with your eyes shut when somebody drops … | no | "A head lands in your lap." → `answer` | `walkin_rest_zoe_today` set · `walkin_run_zoe_today` set · `zoe_caught_up` set |
| `answer` | Zoe, in tiny shorts and a sports top, her ponytail spread across your thighs, her face … | no | "Let her run on." → `z_on` | — |
|  |  |  | "Run with her." (10 Energy) → `hub_zoe_park` `lap` | `ran_with_zoe` set · `zoe_bailed` cleared · `zoe_run_booked` cleared |
|  |  |  | "Dare me, Zo." (top on) → `zoe_park_dare` `ask` | — |
| `z_on` | "I'm not running, Zo. Go." · Zoe: "Lazy. Fine. Keep my pillow warm." She pats her thigh and jogs off | no | "Watch her go." → Park | — |

## B14 · `walkin_tub_zoe`

| row | answer |
|---|---|
| host · who | `party_house_soak` · Zoe, the deck watching |
| when | Sat 23:30-23:45 (pass 4: every screen lands before Zoe leaves at midnight) · odds 0.25, 0.35, 0.45 |
| want | under the water her fingers brush Ella's pussy |
| next step | "Let her." (after `zoe_together`, Hungry, Exhibitionism 60) |
| hook | none in the build: nothing reads `zoe_in_the_tub` |
| the no | "Not here, Zo." or "Get out, dripping." |

**`walkin_tub_zoe`** — The Party House · needs `opening_done` · not `walkin_tub_zoe_today` · Zoe in The Party House · `zoe_met` · Sat · 23:30-23:45 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | The hot tub steams on the back deck. | yes | "Strip and get in." → `answer` | `walkin_tub_zoe_today` set · `zoe_in_the_tub` set |
| `answer` | You strip on the cold deck and get in. | no | "Not here, Zo." (`zoe_together`) → `tub_no` | — |
|  |  |  | "Get out, dripping." (not `zoe_together`) → The Party House | Energy +5 (cap 100) · `late_party` set · `came_home_late` set |
|  |  |  | "Let her." (`zoe_together` · Corruption 60+ · Exhibitionism 60+) → `tub_let` | Corruption +1 (cap 79) · Exhibitionism +1 (cap 79) · Hygiene -10 · costs Energy 10 |
| `tub_no` | You catch her wrist under the water and put her hand back on her own thigh. | no | "Get out, dripping." → The Party House | Energy +5 (cap 100) · `late_party` set · `came_home_late` set |
| `tub_let` | You let her. | yes | "Get out, dripping." → The Party House | Energy +5 (cap 100) · `late_party` set · `came_home_late` set |

## B15 · `walkin_quad_team`

| row | answer |
|---|---|
| host · who | `quad_grass` · Jake and the team |
| when | Mon/Wed/Fri 08:30-08:45 · odds 0.25, 0.35, 0.45 |
| want | six of them look up her skirt on the slope |
| next step | "Leave it." (Covered) |
| hook | none in the build: nothing reads `team_saw_grass` |
| the no | "Fix your skirt." pays 0 |

**`walkin_quad_team`** — Quad · needs `opening_done` · not `walkin_quad_team_today` · Jake in Quad · `jake_met` · in short skirt · Mon/Wed/Fri · 08:30-08:45 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're lying back on the grass with your bag under your head and your eyes shut. | no | "They've stopped." → `answer` | `walkin_quad_team_today` set · `team_saw_grass` set |
| `answer` | You open your eyes. | no | "Fix your skirt." → `q_fix` | — |
|  |  |  | "Leave it." → `q_leave` | Exhibitionism +1 (cap 19) |
| `q_fix` | You sit up fast and yank your skirt down over your thighs. | no | "Get up." → Quad | — |
| `q_leave` | You don't fix it. | no | "Get up." → Quad | — |

## B15 · `walkin_quad_zoe`

| row | answer |
|---|---|
| host · who | `quad_grass` · Zoe |
| when | Tue/Thu/Fri 14:30-14:45 · odds 0.25, 0.35, 0.45 |
| want | her head in Ella's lap, an inch from her crotch |
| next step | "Leave her there." · Curious: "Let her hand slide up your thigh." |
| hook | none in the build: nothing reads `zoe_lap_quad` |
| the no | "Sit up. 'Get your own lap.'" pays 0 |

**`walkin_quad_zoe`** — Quad · needs `opening_done` · not `walkin_quad_zoe_today` · Zoe in Quad · `zoe_met` · Tue/Thu/Fri · 14:30-14:45 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're sitting on the grass with your knees out and your notes on your lap. | no | "Her head's in your lap." → `answer` | `walkin_quad_zoe_today` set · `zoe_lap_quad` set |
| `answer` | She turns her face in against your thigh and looks up at you, upside down, her … | no | "Sit up. "Get your own lap." → `qz_up` | — |
|  |  |  | "Leave her there." (Corruption under 20) → `qz_leave` | Corruption +1 (cap 19) |
|  |  |  | "Let her hand slide up your thigh." (Corruption 20+) → `qz_hand` | Corruption +1 (cap 39) |
| `qz_up` | Zoe rolls off you onto the grass, laughing. | no | "Get up." → Quad | — |
| `qz_leave` | You leave her there. | no | "Get up." → Quad | — |
| `qz_hand` | Her hand slides from the outside of your thigh to the inside, slow, and keeps going, … | no | "Get up." → Quad | — |

## B16 · `walkin_hall_hale`

| row | answer |
|---|---|
| host · who | `lecture_timetable` · Dr. Hale |
| when | Mon/Wed/Fri 08:30-08:45; Thu 13:00-13:15 · odds 0.25, 0.35, 0.45 |
| want | his eyes on her legs, a second too long |
| next step | "Sit on the front desk while he sets up." (Daring) |
| hook | her thought on both answers: his office hours, Thursday at five, with the door shut (reader pass 4, 2026-11-04) |
| the no | "Take a seat." pays 0 |

**`walkin_hall_hale`** — Lecture Hall · needs `opening_done` · not `walkin_hall_hale_today` · Dr. Hale in Lecture Hall · `hale_met` · `hale_01_done` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're at the door reading the timetable when Dr. Hale comes in for his lecture with … | no | "He stops beside you." → `answer` | `walkin_hall_hale_today` set · `hale_early_look` set |
| `answer` | He looks at you, and then his eyes go down, to your legs, and stay there … | no | "Take a seat." → `h_seat` | — |
|  |  |  | "Sit on the front desk while he sets up." (Exhibitionism 20+ · Exhibitionism under 40) → `h_desk` | Exhibitionism +1 (cap 39) |
| `h_seat` | You go and sit in the third row while the seats fill up round you. | no | "Take notes." → Lecture Hall | — |
| `h_desk` | You hop up onto the front desk, right beside his lectern, and cross your legs. | no | "Take notes." → Lecture Hall | — |

## B17 · `walkin_couch_zoe`

| row | answer |
|---|---|
| host · who | `zoe_couch_alone` · Zoe |
| when | Mon/Tue/Wed/Thu 22:00-23:30 · odds 0.25, 0.35, 0.45 |
| want | in her sleep shirt, looking at Ella's mouth |
| next step | "Pull her down onto the couch." (Curious) |
| hook | after `zoe_together`: "Go to bed with her." (A5) |
| the no | "Say goodnight." pays 0 |

**`walkin_couch_zoe`** — Zoe's Living Room · needs `opening_done` · not `walkin_couch_zoe_today` · Zoe in Zoe's Bedroom · `zoe_met` · Mon/Tue/Wed/Thu · 22:00-23:30 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're on Zoe's couch under the fairy lights. | no | "She drops down next to you." → `answer` | `walkin_couch_zoe_today` set · `zoe_couch_night` set |
| `answer` | She curls up against your side with her bare legs over your lap. | no | "Say goodnight." → `c_night` | — |
|  |  |  | "Pull her down onto the couch." (Corruption 20+) → `c_pull` | Corruption +1 (cap 39) |
|  |  |  | "Go to bed with her." (`zoe_together` · Corruption 40+ · not `zoe_bed_today` · 22:00-23:45) → `hub_zoe_bedroom` `a5_offer` | — |
| `c_night` | She kisses your cheek, slow, near your mouth, and pads back down the hall. | no | "Sit a while." → Zoe's Living Room | — |
| `c_pull` | You pull her down on top of you. | no | "Sit a while." → Zoe's Living Room | — |

## B18 · `walkin_bedroom_zoe`

| row | answer |
|---|---|
| host · who | `zoe_bedroom_look` · Zoe |
| when | Mon/Tue/Wed/Thu 21:45-22:00 · odds 0.25, 0.35, 0.45 |
| want | she strips in front of Ella and catches her looking |
| next step | "Watch her change." (Good Girl, cap 19) |
| hook | none in the build: nothing reads `zoe_changed_in_front` |
| the no | "Look away." pays 0 |

**`walkin_bedroom_zoe`** — Zoe's Bedroom · needs `opening_done` · not `walkin_bedroom_zoe_today` · Zoe in Zoe's Living Room · `zoe_met` · Mon/Tue/Wed/Thu · 21:45-22:00 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're looking at the polaroids round Zoe's mirror when she comes in behind you and kicks … | no | "She starts undressing." → `answer` | `walkin_bedroom_zoe_today` set · `zoe_changed_in_front` set |
| `answer` | She pulls her top over her head and drops it on the floor. | no | "Look away." → `b_away` | — |
|  |  |  | "Watch her change." → `b_watch` | Corruption +1 (cap 19) |
| `b_away` | You look at the polaroids. | no | "Leave her to sleep." → Zoe's Living Room | — |
| `b_watch` | You watch. | yes | "Leave her to sleep." → Zoe's Living Room | — |

## B19 · `walkin_house_vance`

| row | answer |
|---|---|
| host · who | `vance_house_look` · Mr. Vance |
| when | 18:00-18:15 · odds 0.25, 0.35, 0.45 |
| want | he looks up her bare legs from the porch |
| next step | "Stay where he can see your legs." (Daring) |
| hook | his Want +2 on the moment, once a day |
| the no | "Walk on." pays 0 |

**`walkin_house_vance`** — Next Door · needs `opening_done` · not `walkin_house_vance_today` · Mr. Vance in Next Door · `vance_met` · not wearing jeans · not wearing leggings · 18:00-18:15 · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `moment` | You're on the sidewalk looking up at the house next door when the front door opens. | no | "He looks at your legs." → `answer` | Mr. Vance's Want +2 (cap 100) · `walkin_house_vance_today` set · `vance_porch_look` set |
| `answer` | He doesn't open the paper. | no | "Walk on." → `v_walk` | — |
|  |  |  | "Stay where he can see your legs." (Exhibitionism 20+) → `v_stay` | Exhibitionism +1 (cap 39) |
| `v_walk` | You walk on, and behind you the rocking chair starts up again, slow. | no | "Keep walking." → Your Street | — |
| `v_stay` | You stay. | no | "Walk on." → Your Street | — |

## B20 · `walkin_door_art`

| row | answer |
|---|---|
| host · who | `door_grade_art` · the art lecturer |
| when | in the walker's own hours · odds 0.25 |
| want | she looks at Ella as she looks at the model: measuring |
| next step | "Hold that. Don't move. Hm. Another time." |
| hook | her office hub reads `art_door_seen` |
| the no | one screen: "Step back." |

**`walkin_door_art`** — Art Lecturer's Office · needs `opening_done` · not `walkin_door_art_today` · The art lecturer in Art Lecturer's Office · `art_lecturer_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | You're reading your grade when the door opens under your finger. | no | "Step back." → Art Lecturer's Office | `walkin_door_art_today` set · `art_door_seen` set |

## B20 · `walkin_door_ta`

| row | answer |
|---|---|
| host · who | `door_grade_bio` · the Biology TA |
| when | in the walker's own hours · odds 0.25 |
| want | her eyes go down Ella and snap back up |
| next step | "The kettle's just boiled. You can come in, if you want." (her office, where "Step back." lands in her hours) |
| hook | her office hub reads `ta_door_seen` |
| the no | one screen: "Step back." |

**`walkin_door_ta`** — TA's Office · needs `opening_done` · not `walkin_door_ta_today` · The Biology TA in TA's Office · `bio_ta_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | The half-open door swings wide. | no | "Step back." → TA's Office | `walkin_door_ta_today` set · `ta_door_seen` set |

## B20 · `walkin_door_dean`

| row | answer |
|---|---|
| host · who | `door_dean_notice` · the dean |
| when | in the walker's own hours · odds 0.25 |
| want | "Is that what you wore to class?" |
| next step | none: one screen |
| hook | his office hub reads `dean_door_seen` |
| the no | one screen |

**`walkin_door_dean`** — Dean's Office · needs `opening_done` · not `walkin_door_dean_today` · The dean in Dean's Office · `dean_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | The heavy door opens while you're reading the notice. | no | "Step back out onto the faculty floor." → Faculty Floor | `walkin_door_dean_today` set · `dean_door_seen` set |

## B20 · `walkin_door_hale`

| row | answer |
|---|---|
| host · who | `door_grade_psych` · Dr. Hale |
| when | in the walker's own hours · odds 0.25 |
| want | his eyes down her legs: "Checking up on me?" |
| next step | "Come in or don't." His office hours |
| hook | his office hub reads `hale_door_seen` |
| the no | "Step back." lands on `no`: before his step 3 he watches her legs go; from his step 3, "Suit yourself. You know where I am on Thursdays." and he shuts the door |

**`walkin_door_hale`** — Dr. Hale's Office · needs `opening_done` · not `walkin_door_hale_today` · Dr. Hale in Dr. Hale's Office · `hale_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | You've got your finger on your grade when Dr. Hale opens his door. | no | "Step back." → `no` | — |
| `no` | You step back. He watches your legs go, and lets the door swing shut. (before his step 3) · You take a step back from his door. (from his step 3) | no | "Walk away." → Faculty Floor | `walkin_door_hale_today` set · `hale_door_seen` set |

## B20 · `walkin_door_business`

| row | answer |
|---|---|
| host · who | `door_grade_business` · the Business lecturer |
| when | in the walker's own hours · odds 0.25 |
| want | none: he looks at the grade, not at her |
| next step | none: one screen |
| hook | his office hub reads `business_door_seen` |
| the no | one screen: "Step back." |

**`walkin_door_business`** — Business Lecturer's Office · needs `opening_done` · not `walkin_door_business_today` · The Business lecturer in Business Lecturer's Office · `business_lecturer_met` · repeatable · walk-in only

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | The door opens. | no | "Step back." → Business Lecturer's Office | `walkin_door_business_today` set · `business_door_seen` set |

## Explicit beats on this page

Not written out here (see the build); the build counts these screens as explicit: `walkin_bedroom_zoe` `b_watch`, `walkin_canteen_zoe` `z_stay`, `walkin_gym_team` `t_set`, `walkin_tub_zoe` `moment`, `walkin_tub_zoe` `tub_let`.

