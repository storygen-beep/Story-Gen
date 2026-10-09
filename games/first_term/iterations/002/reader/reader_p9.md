# Reader — first_term, part 9 (6 canvases; iteration 002, no shipped release so every canvas is touched)

Read first: gates.py first_term (61/88; its red lines are left alone: laura_01 "nobody is woken", "Booth four's going to tip big today." duplicated, "He used to tell you." [used to], "Further. (Needs Hungry)" lint, the café uniform double-equip, the "Done." sinks), who_is_where.py first_term, v2_state.json ladders (npc_laura n 1-8, npc_tom n 1-6, npc_zoe n 1-4). There is no `want.companion_is_rival`, so test 9 is N/A everywhere. No canvas here carries an explicit beat (none has 3+ frozen-list words), so test 7 is N/A everywhere. Every button sits on a person's canvas, so test 11 is N/A everywhere.

scene | test | verdict | the line judged | why
---|---|---|---|---
laura_08_it_wasnt_the_wine | want | PASS | "She isn't saying no, either." | Laura's want shows (shaking hand, no refusal). Not an explicit step. Earlier sign checked: laura_07_dark_stairs ("She wants you. She isn't hiding it.", the stairs kiss), and the gate laura_step eq 7 comes after it
laura_08_it_wasnt_the_wine | next step | PASS | "I'm your mother." | the kiss is named out loud for the first time, one step past laura_07's silence
laura_08_it_wasnt_the_wine | hook | PASS | "\"Okay. For now.\"" | "for now" points at what comes next; it opens "Kiss her goodnight." in laura_catch at step 8
laura_08_it_wasnt_the_wine | her voice at her level | PASS | "She didn't say it was wrong. She said who she is." | appetite at a gate of corruption 40+
laura_08_it_wasnt_the_wine | who notices | PASS | "She doesn't turn round when you come in. She can't." | Laura reacts to her
laura_08_it_wasnt_the_wine | the written no | PASS | "You're my mom. That's all you get to be." | the no is written, ends the path (laura_step -1) and moves the catch to punishment only
laura_08_it_wasnt_the_wine | the body | N/A | — | no explicit beat
laura_08_it_wasnt_the_wine | the numbers and the clothes agree | N/A | — | no number, and none of her garments is named (the blouse is Laura's)
laura_08_it_wasnt_the_wine | companion and rival | N/A | — | no companion_is_rival
laura_08_it_wasnt_the_wine | true on every visit it can render on | PASS | "That was the wine. On the stairs." | weekdays 06:30-08:00 match Laura's kitchen row; gated on laura_step 7; the retry ("It was the wine.") re-renders true on the next weekday
laura_08_it_wasnt_the_wine | a solo button is a real act | N/A | — | no solo button
laura_catch | want | PASS | "Sit down. Tell me everything. All of it, sweetheart." | Laura wants to know. The kiss row comes after laura_08 (laura_step >= 8); earlier sign checked: laura_07_dark_stairs, laura_08_it_wasnt_the_wine
laura_catch | next step | PASS | "Her knee is bare where the robe has fallen open, and she doesn't fix it." | the catch grows with laura_step and want (step 2+ robe, step 8 the kiss)
laura_catch | hook | PASS | "Kiss her goodnight." | shown locked, so it names the next thing
laura_catch | her voice at her level | N/A | "A week. She means every second of it." | the thought is not tied to any of her meters
laura_catch | who notices | PASS | "She smells it from the step." | Laura reads where she has been
laura_catch | the written no | PASS | "You think I don't know that face? I invented that face." | Laura offers "tell me everything"; the Lie is written and moves suspicion +10 and warmth -5
laura_catch | the body | N/A | — | the "wall" kiss node is not explicit
laura_catch | the numbers and the clothes agree | PASS | "That's it. A week." | curfew_days is set to 7 and drops by 1 a day; "her dress on you" is backed by the laura_blue_dress equipped check
laura_catch | companion and rival | N/A | — | no companion_is_rival
laura_catch | true on every visit it can render on | FAIL | "Kiss her goodnight." | at laura_step -1 (after laura_08's "From now on, when she catches you, she punishes you. Nothing else.") this row still shows locked (show_when_locked, needs laura_step >= 8, which -1 can never reach). It is a door that can never open, and it contradicts "Nothing else."
laura_catch | a solo button is a real act | N/A | — | no solo button
hub_laura_kitchen | want | PASS | "Her eyes go to you and stay a second too long." | Laura's want leaks by step; no explicit step on this hub
hub_laura_kitchen | next step | PASS | "She's started leaving her bedroom door open when she dresses." | a leak line for each laura_step 1-7, and more choices at step 1 and step 7
hub_laura_kitchen | hook | PASS | "Come upstairs after. I have something for you." | names laura_01
hub_laura_kitchen | her voice at her level | N/A | — | no thought of hers on the hub
hub_laura_kitchen | who notices | PASS | "Is that the uniform, or Tom's idea?" | Laura reacts to clothes, make-up and hygiene
hub_laura_kitchen | the written no | PASS | "Come upstairs after." | the offer's written no lives in laura_01 ("I can't take this."); the shopping ask's no is "Never mind."
hub_laura_kitchen | the body | N/A | — | no explicit beat; the tease and touch nodes are placeholders
hub_laura_kitchen | the numbers and the clothes agree | PASS | "Could you get these? Here's twenty." | money +20 and the "forgot" path takes 20 back; every garment line is behind a worn_type, clothing_item or clothing_slot check
hub_laura_kitchen | companion and rival | N/A | — | no companion_is_rival
hub_laura_kitchen | true on every visit it can render on | FAIL | "Eat something, sweetheart. You're not going to class on nothing." | the 06:30-08:00 group has no ate_breakfast check. After "Eat." (ate_breakfast set, 15m, lands back in home_kitchen) it renders again at about 06:45-08:00 to a girl who has just eaten
hub_laura_kitchen | true on every visit it can render on | FAIL | "Dinner in ten. Set the table?" | gated on 18:00-19:50 only. After "Sit down to dinner." then "Done." (30m, ate_dinner set) the hub re-renders at 18:30+ and promises a dinner already eaten
hub_laura_kitchen | true on every visit it can render on | FAIL | "Ryan slides in next to you with his hair still wet from the gym." | Sun 18:00: who_is_where has Ryan in home_living_room 14-18 (TV), with no gym that day
hub_laura_kitchen | true on every visit it can render on | FAIL | "Study at the table while she cooks." / "You sit on the counter and talk while she cooks." | Study is open until 22:00 and Talk has no time gate. At 21:00-21:59 dinner (18-20) and the dishes are done, so she isn't cooking (and at 07:00 Talk says she "chops")
hub_laura_kitchen | a solo button is a real act | N/A | — | every button is with Laura
hub_tom_cafe | want | PASS | "keeping an eye on the room and an eye on you" | Tom's want shows
hub_tom_cafe | next step | PASS | "His palm is already open on the counter when you come out of booth four." | a leak line for each tom_step 1-5
hub_tom_cafe | hook | PASS | "Stay late Friday?" | names tom_06
hub_tom_cafe | her voice at her level | N/A | — | no thought
hub_tom_cafe | who notices | PASS | "Top button stays open. House rule." | Tom reads the uniform
hub_tom_cafe | the written no | PASS | "Stay late Friday?" | the no is written in tom_06_after_close_kiss ("Night, Tom.")
hub_tom_cafe | the body | N/A | — | no explicit beat
hub_tom_cafe | the numbers and the clothes agree | PASS | "He reties your apron from behind on his way past." | behind cafe_uniform_normal equipped; the top button is behind cafe_uniform_sexy
hub_tom_cafe | companion and rival | N/A | — | no companion_is_rival
hub_tom_cafe | true on every visit it can render on | FAIL | "Back to work." | at 21:59 (the café closes 22:00 and "Shifts end when the café shuts") it spends 30 minutes of work into the shut room. Tom's 22:00-23:00 closing row keeps the hub up, so "Table three wants you" re-renders at 22:29
hub_tom_cafe | a solo button is a real act | N/A | — | the buttons are with Tom
hub_gary_booth | want | PASS | "He lowers the paper when you come near, an inch at a time." | Gary's want shows on this canvas (no ladder)
hub_gary_booth | next step | PASS | "He pats the seat beside him in the booth and leaves his hand there, palm up." | after tom_04 he moves from looking to asking
hub_gary_booth | hook | PASS | "Ten minutes, when you've got them." | names cafe_gary_ten_minutes
hub_gary_booth | her voice at her level | N/A | — | no thought
hub_gary_booth | who notices | PASS | "You look lovely today. You always look lovely." | Gary reacts to her
hub_gary_booth | the written no | PASS | "Ten minutes, when you've got them." | the no is written in cafe_gary_ten_minutes ("\"No.\"")
hub_gary_booth | the body | N/A | — | no explicit beat
hub_gary_booth | the numbers and the clothes agree | PASS | "Ten minutes" | agrees with "Twenty for ten minutes" in cafe_gary_ten_minutes
hub_gary_booth | companion and rival | N/A | — | no companion_is_rival
hub_gary_booth | true on every visit it can render on | FAIL | "Ten minutes, when you've got them." | Fri 20:00-22:00 (Gary's café row) and any visit out of uniform, under corruption 40 or after the day's one trigger: cafe_gary_ten_minutes runs only on weekdays 14:30-18:00, in uniform, corruption 40+, once a day, so the offer cannot be taken
hub_gary_booth | a solo button is a real act | N/A | — | "Top up his tea." is with Gary
hub_zoe_apartment | want | PASS | "She takes longer than she needs to. Neither of you mentions it." | Zoe's want shows; no explicit step
hub_zoe_apartment | next step | PASS | "Her eyes keep going to your bra strap." | leak lines for zoe_step 1-3, the lap version at corruption 20, the dare lines after zoe_04
hub_zoe_apartment | hook | PASS | "There's a hot tub Saturday. Just us. Don't forget." | names zoe_03
hub_zoe_apartment | her voice at her level | N/A | — | no thought
hub_zoe_apartment | who notices | PASS | "She bites her lip at the strap of her own dress on you." | Zoe reacts to clothes
hub_zoe_apartment | the written no | FAIL | "I'm bored. Dare me something." | Mon-Thu and Sat 18:00-22:00 Zoe asks for a dare. The screen's only buttons are "Stay a while." and "Go."; nothing answers her and no refusal is written
hub_zoe_apartment | the body | N/A | — | face_lap is not explicit
hub_zoe_apartment | the numbers and the clothes agree | PASS | "Now we're talking. Turn around." | short_skirt, zoe_party_dress and the bra lines are each behind their checks; no numbers
hub_zoe_apartment | companion and rival | N/A | — | no companion_is_rival
hub_zoe_apartment | true on every visit it can render on | FAIL | "Go on, then. What's tonight's dare?" | Fri 23:00 with exhibitionism < 40, or Sat 00:00-02:00 with party_went unset (the hub's own "Now you show up?" branch): party_dare needs exhibitionism 40+ and party_went within 8h, so no dare can happen on any screen that night
hub_zoe_apartment | a solo button is a real act | N/A | — | the buttons are with Zoe
