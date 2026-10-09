scene | test | PASS / FAIL / N/A | the line judged (quoted, short) | why (one line)
---|---|---|---|---
quad_grass | want | N/A | — | no person on this canvas
quad_grass | next step | N/A | — | no person on this canvas
quad_grass | hook | N/A | — | no person on this canvas
quad_grass | her voice at her level | N/A | — | no thought of hers, or no meter in play
quad_grass | who notices | PASS | They don't stop looking at you. | campus_talk bands: the quad reacts to her name
quad_grass | the written no | N/A | — | no offer is made to her
quad_grass | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
quad_grass | the numbers and the clothes agree | N/A | — | no number, no garment of hers
quad_grass | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
quad_grass | true on every visit it can render on | PASS | You catch your name in it, then "Zoe's", then "party". | party line behind party_went; the no-party variant at the same band
quad_grass | a solo button is a real act | PASS | Get up. (30 min) | shows the sitting it names and spends the hour
canteen_eat | want | N/A | — | no person on this canvas
canteen_eat | next step | N/A | — | no person on this canvas
canteen_eat | hook | N/A | — | no person on this canvas
canteen_eat | her voice at her level | N/A | — | no thought of hers, or no meter in play
canteen_eat | who notices | N/A | — | nothing she does here for anyone to notice
canteen_eat | the written no | N/A | — | no offer is made to her
canteen_eat | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
canteen_eat | the numbers and the clothes agree | PASS | Eat ($5). | price on the label = costs money 5; energy +20 matches the description
canteen_eat | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
canteen_eat | true on every visit it can render on | FAIL | You eat it all, fast, standing up by the windows | the pool says she has eaten before she chooses; on the visit she clicks "Not hungry." the line is false
canteen_eat | a solo button is a real act | PASS | Eat ($5). | money -5, energy +20, 30 min
canteen_listen | want | N/A | — | no person on this canvas
canteen_listen | next step | N/A | — | no person on this canvas
canteen_listen | hook | N/A | — | no person on this canvas
canteen_listen | her voice at her level | N/A | — | no thought of hers, or no meter in play
canteen_listen | who notices | PASS | They look over at the same time, and then they all look away at once. | the canteen reacts at campus_talk 10+
canteen_listen | the written no | N/A | — | no offer is made to her
canteen_listen | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
canteen_listen | the numbers and the clothes agree | N/A | — | no number, no garment of hers
canteen_listen | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
canteen_listen | true on every visit it can render on | PASS | "She was at Zoe's party." | party line behind party_went; canteen open 08-18 weekdays
canteen_listen | a solo button is a real act | PASS | Leave them to it. (20 min) | shows the listening it names and spends the time
canteen_table | want | PASS | Babe. Sit. Tell them about your mom's rules. | Zoe wants her at the table
canteen_table | next step | PASS | Some of us came here to study. | the rival's band at campus_talk 10+ goes past plain lunch
canteen_table | hook | PASS | Somebody's planning Friday. | points at the Friday party
canteen_table | her voice at her level | N/A | — | no thought of hers, or no meter in play
canteen_table | who notices | PASS | By the end of lunch four new people know your name | the table and the rival react; campus_talk +1
canteen_table | the written no | N/A | — | no offer is made to her
canteen_table | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
canteen_table | the numbers and the clothes agree | PASS | looks you over, top to bottom | no garment named; no number contradicted
canteen_table | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
canteen_table | true on every visit it can render on | PASS | Hale asked about you after class. | Zoe and Nadia hold the canteen 11:45-13:00 weekdays; the Hale line is Mon/Wed/Fri, after his 08:30 class
canteen_table | a solo button is a real act | PASS | Stay for lunch. | campus_talk +1, 45 min
library_study | want | N/A | — | no person on this canvas
library_study | next step | N/A | — | no person on this canvas
library_study | hook | N/A | — | no person on this canvas
library_study | her voice at her level | N/A | — | no thought of hers, or no meter in play
library_study | who notices | N/A | — | nothing she does here for anyone to notice
library_study | the written no | N/A | — | no offer is made to her
library_study | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
library_study | the numbers and the clothes agree | PASS | Study an hour. | 60 min, energy cost 10, intelligence +1 as described
library_study | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
library_study | true on every visit it can render on | PASS | Nadia is two tables over | gated on npc_at_location
library_study | a solo button is a real act | PASS | Study an hour. | intelligence +1, energy -10, 60 min
toilet_wash | want | N/A | — | no person on this canvas
toilet_wash | next step | N/A | — | no person on this canvas
toilet_wash | hook | N/A | — | no person on this canvas
toilet_wash | her voice at her level | N/A | — | no thought of hers, or no meter in play
toilet_wash | who notices | N/A | — | nothing she does here for anyone to notice
toilet_wash | the written no | N/A | — | no offer is made to her
toilet_wash | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
toilet_wash | the numbers and the clothes agree | N/A | — | no number stated; no catalog garment named
toilet_wash | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
toilet_wash | true on every visit it can render on | PASS | Somebody comes in, pees, washes their hands and goes. | texture; open 07-22
toilet_wash | a solo button is a real act | PASS | Done. | hygiene +15, 10 min
toilet_mirror | want | N/A | — | no person on this canvas
toilet_mirror | next step | N/A | — | no person on this canvas
toilet_mirror | hook | N/A | — | no person on this canvas
toilet_mirror | her voice at her level | PASS | You could fold your arms all day. You won't. | braless on campus needs Daring (exhibitionism 20) by the clothing rules: appetite fits
toilet_mirror | who notices | N/A | — | nothing she does here for anyone to notice
toilet_mirror | the written no | N/A | — | no offer is made to her
toilet_mirror | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
toilet_mirror | the numbers and the clothes agree | PASS | The skirt. You bend to the sink | skirt behind worn_type short_skirt; bra lines behind the bra slot
toilet_mirror | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
toilet_mirror | true on every visit it can render on | PASS | Your bra shows a line. | each line behind its clothing check
toilet_mirror | a solo button is a real act | PASS | Take your bra off in a stall. | unequips the bra, exhibitionism +1
door_grade_psych | want | N/A | — | no person on this canvas
door_grade_psych | next step | N/A | — | no person on this canvas
door_grade_psych | hook | N/A | — | no person on this canvas
door_grade_psych | her voice at her level | N/A | — | no thought of hers, or no meter in play
door_grade_psych | who notices | N/A | — | nothing she does here for anyone to notice
door_grade_psych | the written no | N/A | — | no offer is made to her
door_grade_psych | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
door_grade_psych | the numbers and the clothes agree | N/A | — | no number stated; no garment
door_grade_psych | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
door_grade_psych | true on every visit it can render on | PASS | Laura is going to see this. | grade bands read the grade; the office's own lecturer and pronoun match the cast
door_grade_psych | a solo button is a real act | PASS | Read your grade on the door | shows the reading it names (the browse-share lint already lists it)
door_grade_art | want | N/A | — | no person on this canvas
door_grade_art | next step | N/A | — | no person on this canvas
door_grade_art | hook | N/A | — | no person on this canvas
door_grade_art | her voice at her level | N/A | — | no thought of hers, or no meter in play
door_grade_art | who notices | N/A | — | nothing she does here for anyone to notice
door_grade_art | the written no | N/A | — | no offer is made to her
door_grade_art | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
door_grade_art | the numbers and the clothes agree | N/A | — | no number stated; no garment
door_grade_art | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
door_grade_art | true on every visit it can render on | PASS | Look at the body. Really look. | grade bands read the grade; the office's own lecturer and pronoun match the cast
door_grade_art | a solo button is a real act | PASS | Read your grade on the door | shows the reading it names (the browse-share lint already lists it)
door_grade_business | want | N/A | — | no person on this canvas
door_grade_business | next step | N/A | — | no person on this canvas
door_grade_business | hook | N/A | — | no person on this canvas
door_grade_business | her voice at her level | N/A | — | no thought of hers, or no meter in play
door_grade_business | who notices | N/A | — | nothing she does here for anyone to notice
door_grade_business | the written no | N/A | — | no offer is made to her
door_grade_business | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
door_grade_business | the numbers and the clothes agree | N/A | — | no number stated; no garment
door_grade_business | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
door_grade_business | true on every visit it can render on | PASS | Retakes by appointment. Honest work only. | grade bands read the grade; the office's own lecturer and pronoun match the cast
door_grade_business | a solo button is a real act | PASS | Read your grade on the door | shows the reading it names (the browse-share lint already lists it)
door_grade_bio | want | N/A | — | no person on this canvas
door_grade_bio | next step | N/A | — | no person on this canvas
door_grade_bio | hook | N/A | — | no person on this canvas
door_grade_bio | her voice at her level | N/A | — | no thought of hers, or no meter in play
door_grade_bio | who notices | N/A | — | nothing she does here for anyone to notice
door_grade_bio | the written no | N/A | — | no offer is made to her
door_grade_bio | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
door_grade_bio | the numbers and the clothes agree | N/A | — | no number stated; no garment
door_grade_bio | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
door_grade_bio | true on every visit it can render on | PASS | She's drawn a tiny sad face beside it | grade bands read the grade; the office's own lecturer and pronoun match the cast
door_grade_bio | a solo button is a real act | PASS | Read your grade on the door | shows the reading it names (the browse-share lint already lists it)
hub_zoe_class | want | PASS | Sit with me. This is going to be so boring. | Zoe wants her beside her
hub_zoe_class | next step | PASS | There's a hot tub Saturday. Just us. Don't forget. | zoe_step bands go further
hub_zoe_class | hook | FAIL | Notes are for people with no friends. I'll copy yours. | only the zoe_step 2 band and the no-bra band point ahead; at steps 0, 1 and 3+ nothing names what comes next
hub_zoe_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_zoe_class | who notices | PASS | Now we're talking. Turn around. | Zoe reacts to the skirt, the dress and no bra
hub_zoe_class | the written no | N/A | — | no offer is made to her
hub_zoe_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_zoe_class | the numbers and the clothes agree | PASS | She bites her lip at the strap of her own dress on you. | every garment line has its clothing check
hub_zoe_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_zoe_class | true on every visit it can render on | FAIL | Whisper with her till it starts. | Zoe's row holds the hall Mon 13:00-14:30 and Tue/Thu 08:30-11:45; at Mon 14:20 or Tue 11:30 the class started long ago
hub_zoe_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_01_first_lecture | want | PASS | his eyes stay on you while he says good morning | Hale wants her, shown before anything happens
hale_01_first_lecture | next step | PASS | He's hard. | the meeting, the first step
hale_01_first_lecture | hook | PASS | His wife picks him up Thursdays. Half past seven | points at Thursdays
hale_01_first_lecture | her voice at her level | PASS | Welcome to college. | day-one meters, dry not hungry
hale_01_first_lecture | who notices | PASS | He does that. Last spring it was me. | Nadia
hale_01_first_lecture | the written no | N/A | — | no offer is made to her
hale_01_first_lecture | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hale_01_first_lecture | the numbers and the clothes agree | PASS | a man in his late thirties | cast age 39; skirt line behind short_skirt
hale_01_first_lecture | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_01_first_lecture | true on every visit it can render on | FAIL | a man in his late thirties is setting up his slides | the trigger runs Mon 08:30-10:00; at 09:59 he is setting up and the pen falls "Twenty minutes in" after the class has ended
hale_01_first_lecture | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_02_lost_his_place | want | PASS | His eyes have been on the front row every class since the pen | checked hale_01_first_lecture ("He's hard"): his want comes first
hale_02_lost_his_place | next step | PASS | let him see there's nothing under it | flash goes past the pen
hale_02_lost_his_place | hook | PASS | Thursday. After six. | names his office hours
hale_02_lost_his_place | her voice at her level | PASS | Go on. You came here to do this. | Daring: appetite
hale_02_lost_his_place | who notices | PASS | three rows behind you hear the silence, and somebody coughs | the class
hale_02_lost_his_place | the written no | FAIL | Fix your skirt. | the only refusal needs a short skirt; in jeans, leggings or a dress every button is a flash
hale_02_lost_his_place | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hale_02_lost_his_place | the numbers and the clothes agree | PASS | You went to the toilets before class and took your panties off | each garment line behind the choice or check that led there
hale_02_lost_his_place | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_02_lost_his_place | true on every visit it can render on | FAIL | today you sit in it on purpose, right in front of the lectern | fires to Mon/Wed/Fri 09:59; the class ends 10:00, yet he stops mid-sentence after 09:59 and "After class" follows an hour later
hale_02_lost_his_place | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_03_photo_face_down | want | PASS | his hand comes to rest on your shoulder while he reads, and stays there | checked hale_01, hale_02: his want comes earlier
hale_03_photo_face_down | next step | PASS | he reaches over and turns the photo face-down | the hand and the photo go past the flash
hale_03_photo_face_down | hook | PASS | An A? In Psychology? Who's been helping you? | Laura's question points ahead
hale_03_photo_face_down | her voice at her level | PASS | He turned his wife over so she wouldn't see. | Daring band: she watches, she doesn't flinch
hale_03_photo_face_down | who notices | PASS | Laura reads it at the kitchen table on her phone. | Laura sees the grade
hale_03_photo_face_down | the written no | PASS | "Just the paper." | written, he turns the photo back, the step parks for 7 days
hale_03_photo_face_down | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hale_03_photo_face_down | the numbers and the clothes agree | PASS | Your skirt rides up. | skirt behind short_skirt; grade bands 40/70 match the door
hale_03_photo_face_down | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_03_photo_face_down | true on every visit it can render on | PASS | His office door is open an inch. | Thu 18:00-19:30, inside his office row
hale_03_photo_face_down | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_04_claire_knocks | want | PASS | He wants to touch you, but he can't stop looking first. | checked hale_01 (hard), hale_02 (lost his place), hale_03 (hand on her shoulder): wanting shown earlier
hale_04_claire_knocks | next step | PASS | his palm closes over your tit | hand on bare breast goes past the shoulder
hale_04_claire_knocks | hook | PASS | Next class, Dr. Hale has to stand at the lectern and look at you. | points at hale_05
hale_04_claire_knocks | her voice at her level | PASS | You want him staring. | Bold: appetite
hale_04_claire_knocks | who notices | PASS | Her eyes drop to your flushed chest. | Claire
hale_04_claire_knocks | the written no | PASS | Button up. / "Next Thursday, then, @player." | written, parked 7 days, his want stays
hale_04_claire_knocks | the body | PASS | Your nipple is stiff under his thumb, so he rolls it again until you gasp. | 6 explicit words; last sentence on the body (the no-buttons variant is a placeholder)
hale_04_claire_knocks | the numbers and the clothes agree | FAIL | Your hand goes to your own top button. | renders in every top; a T-shirt or a dress has no button, and "Button up." is offered to all
hale_04_claire_knocks | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_04_claire_knocks | true on every visit it can render on | FAIL | "You ready, love?" | the trigger opens 18:30, so the knock lands at 18:40; Nadia fixes the pickup at half past seven and the ledger says close to it
hale_04_claire_knocks | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_05_seven_twenty | want | PASS | This has to stop, @player. | he wants it and fights it; earlier steps show the want
hale_05_seven_twenty | next step | PASS | Thursdays at seven. Your office. | she sets his hour
hale_05_seven_twenty | hook | PASS | He'll watch the clock the whole time. So will you. | points at Thursdays
hale_05_seven_twenty | her voice at her level | PASS | He'll watch the clock the whole time. So will you. | Bold: appetite
hale_05_seven_twenty | who notices | PASS | See what she does when she tries. | ledger declares nobody, then Laura at dinner
hale_05_seven_twenty | the written no | PASS | "See you in class." | parks the step 2 days (gate 'a no has content' covers it)
hale_05_seven_twenty | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hale_05_seven_twenty | the numbers and the clothes agree | PASS | You'll be done by seven-twenty. | seven to seven-twenty matches hale_thursdays' twenty minutes and the 19:30 pickup
hale_05_seven_twenty | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_05_seven_twenty | true on every visit it can render on | FAIL | When the room empties you stay in the front row | fires from Mon/Wed/Fri 08:30, the minute his class starts; the room has not emptied
hale_05_seven_twenty | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hale_thursdays | want | PASS | Twenty minutes, @player. | checked hale_01 to hale_05: his want comes first
hale_thursdays | next step | PASS | He locks the door behind you | the repeat of step 4's touch, every Thursday (hand screen is a placeholder)
hale_thursdays | hook | PASS | Thursday. | names next week
hale_thursdays | her voice at her level | N/A | — | no thought of hers, or no meter in play
hale_thursdays | who notices | PASS | Footsteps in the corridor stop outside, then go on. | the corridor
hale_thursdays | the written no | FAIL | "Not tonight." / "Then why did you come?" | the no is written but moves nothing: no flag, no effect, no park
hale_thursdays | the body | N/A | — | placeholder
hale_thursdays | the numbers and the clothes agree | FAIL | Button up. | offered in any top, a T-shirt included; and on that path 5+5 minutes pass before "When the twenty minutes are gone"
hale_thursdays | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hale_thursdays | true on every visit it can render on | FAIL | You walk out past the car park, where his wife's car will be soon. | fired at 19:19 the leave screen lands at 19:39, after the 19:30 pickup Nadia names
hale_thursdays | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_hale_office | want | PASS | He keeps the desk between you. | he wants her and holds back
hub_hale_office | next step | PASS | The photo on his desk is face-down. He doesn't turn it over. | hale_step bands
hub_hale_office | hook | FAIL | Dr. Hale looks up from a pile of papers. | the 'for now' is gone; only the step-2 clock line points ahead, at steps 1, 3, 4 and 5 nothing does
hub_hale_office | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_hale_office | who notices | PASS | Top of the class. I'd say I'm proud | he reacts to grade and clothes
hub_hale_office | the written no | N/A | — | no offer is made to her
hub_hale_office | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_hale_office | the numbers and the clothes agree | PASS | He loses the sentence, and starts it again. | skirt check; grade bands 40/70
hub_hale_office | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_hale_office | true on every visit it can render on | PASS | The photo on his desk is face-up | face-down from hale_step 3, the step that turns it
hub_hale_office | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_nadia_library | want | PASS | You want my notes? You can have my notes. | she wants to look after her
hub_nadia_library | next step | PASS | His wife came to the office. Everyone's saying. Was it you? | hale_step bands move her lines
hub_nadia_library | hook | PASS | Thursday office hours are a trap, you know that? | points at Hale's office
hub_nadia_library | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_nadia_library | who notices | PASS | Was it you? | Nadia knows
hub_nadia_library | the written no | N/A | — | no offer is made to her
hub_nadia_library | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_nadia_library | the numbers and the clothes agree | PASS | He'll lose his place again. | skirt check
hub_nadia_library | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_nadia_library | true on every visit it can render on | PASS | Nadia at a library table | inside her rows; 'after class' only Mon/Wed/Fri after Hale's 08:30 class
hub_nadia_library | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_nadia_canteen | want | PASS | You want my notes? You can have my notes. | she wants to look after her
hub_nadia_canteen | next step | PASS | His wife came to the office. Everyone's saying. Was it you? | hale_step bands move her lines
hub_nadia_canteen | hook | PASS | Thursday office hours are a trap, you know that? | points at Hale's office
hub_nadia_canteen | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_nadia_canteen | who notices | PASS | Was it you? | Nadia knows
hub_nadia_canteen | the written no | N/A | — | no offer is made to her
hub_nadia_canteen | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_nadia_canteen | the numbers and the clothes agree | PASS | He'll lose his place again. | skirt check
hub_nadia_canteen | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_nadia_canteen | true on every visit it can render on | PASS | Nadia at the end of a table with a salad | inside her rows; 'after class' only Mon/Wed/Fri after Hale's 08:30 class
hub_nadia_canteen | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_nadia_lecture | want | PASS | You want my notes? You can have my notes. | she wants to look after her
hub_nadia_lecture | next step | PASS | His wife came to the office. Everyone's saying. Was it you? | hale_step bands move her lines
hub_nadia_lecture | hook | PASS | Thursday office hours are a trap, you know that? | points at Hale's office
hub_nadia_lecture | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_nadia_lecture | who notices | PASS | Was it you? | Nadia knows
hub_nadia_lecture | the written no | N/A | — | no offer is made to her
hub_nadia_lecture | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_nadia_lecture | the numbers and the clothes agree | PASS | He'll lose his place again. | skirt check
hub_nadia_lecture | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_nadia_lecture | true on every visit it can render on | PASS | Nadia in the seat beside yours | inside her rows; 'after class' only Mon/Wed/Fri after Hale's 08:30 class
hub_nadia_lecture | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_jake_class | want | PASS | I'm only in this class for the credits. And you. | Jake wants her
hub_jake_class | next step | PASS | He keeps his hand on your back | jake_step bands
hub_jake_class | hook | FAIL | Draw me after. I'll hold still, I swear. | no line names a next scene; no date, no step
hub_jake_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_jake_class | who notices | PASS | Guys. Look at her. | Jake reacts to the skirt and dresses
hub_jake_class | the written no | N/A | — | no offer is made to her
hub_jake_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_jake_class | the numbers and the clothes agree | PASS | His eyes go down your legs and stay there. | each dress line behind its item
hub_jake_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_jake_class | true on every visit it can render on | FAIL | Talk till the lecturer starts. | his rows hold the hall Tue/Thu 08:30-10:00; at 09:55 the class is nearly over. Also "Everyone was looking at you tonight." plays at 08:30 in Laura's dress
hub_jake_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_jake_gym | want | PASS | You lift? Come here. I'll show you. | Jake wants her close
hub_jake_gym | next step | PASS | Pull him into the locker room. | Curious hips, Bold kiss
hub_jake_gym | hook | FAIL | You're going to get me thrown off the team. | no line names what comes next
hub_jake_gym | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_jake_gym | who notices | PASS | Somebody on the team whistles. | the team
hub_jake_gym | the written no | FAIL | Go. | his offer gets a bare exit: nothing written, nothing moves
hub_jake_gym | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_jake_gym | the numbers and the clothes agree | PASS | Ten. Look at you. Ten. | no garment of hers unbacked
hub_jake_gym | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_jake_gym | true on every visit it can render on | FAIL | Everyone was looking at you tonight. | the gym row is Tue/Thu 15:00-17:00; 'tonight' is false at every minute it shows
hub_jake_gym | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
college_class_psych | want | PASS | He watches you more than the slides. Just saying. | Hale's want, voiced by Nadia
college_class_psych | next step | PASS | He finds you in the front row before he starts. He always does now. | hale_step bands and the risky slot
college_class_psych | hook | PASS | Under the desk, with the class there. (Needs Hungry) | names the next act
college_class_psych | her voice at her level | PASS | Too tired ... Doze, or skip. | the thought reads energy under 20
college_class_psych | who notices | PASS | Nadia kicks your foot under the desk, grinning. | Hale and Nadia
college_class_psych | the written no | N/A | — | no offer is made to her
college_class_psych | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_class_psych | the numbers and the clothes agree | PASS | Dr. Hale lectures to the back wall for ninety minutes | 90 matches; clothes behind bra/skirt checks
college_class_psych | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_class_psych | true on every visit it can render on | FAIL | He finds you in the front row before he starts. | fires to Mon/Wed/Fri 09:59 (class 08:30-10:00); the class has a minute left and every button spends 90 minutes of it
college_class_psych | a solo button is a real act | PASS | Skip it. | each button moves a grade, energy or 90 minutes
college_class_business | want | PASS | You can have my notes. Seriously, any time. | the study guy
college_class_business | next step | PASS | For ninety minutes he doesn't write a word. | risky slot, rival's line
college_class_business | hook | PASS | Make the whole row look. (Needs Hungry) | names the next act
college_class_business | her voice at her level | PASS | Too tired ... Doze, or skip. | the thought reads energy under 20
college_class_business | who notices | PASS | her mouth gets thinner and thinner | the rival
college_class_business | the written no | N/A | — | no offer is made to her
college_class_business | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_class_business | the numbers and the clothes agree | PASS | Nice of you to dress for once. | bra and no-skirt checked
college_class_business | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_class_business | true on every visit it can render on | FAIL | The lecturer is a grey man in a grey suit who calls the register | fires to Mon/Wed 11:44 (class 10:15-11:45); the class has a minute left and every button spends 90 minutes of it
college_class_business | a solo button is a real act | PASS | Skip it. | each button moves a grade, energy or 90 minutes
college_class_bio | want | PASS | If anyone's struggling, my door's open Tuesday to Friday afternoons. | the TA
college_class_bio | next step | PASS | She drops her pen, picks it up, drops it again. | risky slot
college_class_bio | hook | PASS | Party Friday. I'm not asking. | names the party
college_class_bio | her voice at her level | PASS | Too tired ... Doze, or skip. | the thought reads energy under 20
college_class_bio | who notices | PASS | her neck pink all the way down to her collar | the TA
college_class_bio | the written no | N/A | — | no offer is made to her
college_class_bio | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_class_bio | the numbers and the clothes agree | PASS | Tuesdays, Thursdays, Fridays. | Zoe's quad rows; TA office Tue-Fri 14:30-18:00
college_class_bio | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_class_bio | true on every visit it can render on | FAIL | Focus. (90 minutes, 10 energy) | fires to Tue/Thu 11:44 (class 10:15-11:45); the class has a minute left and every button spends 90 minutes of it
college_class_bio | a solo button is a real act | PASS | Skip it. | each button moves a grade, energy or 90 minutes
college_class_figure | want | PASS | "Look at the weight of her," she says. "Draw that." | the lecturer wants her looking; stranger model, want before the beat
college_class_figure | next step | PASS | He's drawing you. | cocky_guy_met band and risky slot
college_class_figure | hook | PASS | Pose for the class. (Needs Watched) | names the next act
college_class_figure | her voice at her level | PASS | Too tired ... Doze, or skip. | the thought reads energy under 20
college_class_figure | who notices | PASS | Zoe kicks your ankle under the easel. | Zoe, the lecturer, the next easel
college_class_figure | the written no | N/A | — | no offer is made to her
college_class_figure | the body | PASS | "Look at the weight of her," she says. "Draw that." | 5 explicit words; ends on the model's body; the next beat ends on her nipples
college_class_figure | the numbers and the clothes agree | FAIL | Pose for the class. (Needs Watched) / It comes later, when you're Hungry. | the button names Watched (exhibitionism 60), the screen it opens names Hungry
college_class_figure | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_class_figure | true on every visit it can render on | FAIL | The model drops her robe on the platform | fires to Tue/Thu 09:59 (class 08:30-10:00); the class has a minute left and every button spends 90 minutes of it
college_class_figure | a solo button is a real act | PASS | Skip it. | each button moves a grade, energy or 90 minutes
meet_business | want | PASS | You can borrow my notes. Any time. If you, um. | the study guy wants her
meet_business | next step | PASS | — | first meeting, the first step
meet_business | hook | PASS | You can borrow my notes. Any time. | points at the study guy (the Business midterm)
meet_business | her voice at her level | N/A | — | no thought of hers, or no meter in play
meet_business | who notices | N/A | — | nothing she does here for anyone to notice
meet_business | the written no | N/A | — | no offer is made to her
meet_business | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
meet_business | the numbers and the clothes agree | PASS | the Business lecturer, fifty | cast age 50
meet_business | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
meet_business | true on every visit it can render on | FAIL | I don't do extensions. I don't do excuses. ... Sit down. | the class-opening speech fires to Mon/Wed 11:44 (class ends 11:45)
meet_business | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
meet_bio | want | PASS | land on you and skip off you, fast, like she touched something hot | the TA wants to look
meet_bio | next step | PASS | — | first meeting, the first step
meet_bio | hook | PASS | My door's open in the afternoons. | points at her office
meet_bio | her voice at her level | N/A | — | no thought of hers, or no meter in play
meet_bio | who notices | N/A | — | nothing she does here for anyone to notice
meet_bio | the written no | N/A | — | no offer is made to her
meet_bio | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
meet_bio | the numbers and the clothes agree | PASS | a shy woman of twenty-eight | cast age 28
meet_bio | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
meet_bio | true on every visit it can render on | FAIL | Hi. I'm— I'll be taking you this term. | the class-opening speech fires to Tue/Thu 11:44 (class ends 11:45)
meet_bio | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
meet_figure | want | PASS | He looks you over, slow, and grins. | the cocky guy
meet_figure | next step | PASS | — | first meeting, the first step
meet_figure | hook | PASS | This is going to be a good class. | points at the class and him
meet_figure | her voice at her level | N/A | — | no thought of hers, or no meter in play
meet_figure | who notices | N/A | — | nothing she does here for anyone to notice
meet_figure | the written no | N/A | — | no offer is made to her
meet_figure | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
meet_figure | the numbers and the clothes agree | PASS | The art lecturer is forty-five | cast age 45
meet_figure | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
meet_figure | true on every visit it can render on | FAIL | You'll draw what's there, not what you think is there | the class-opening speech fires to Tue/Thu 09:59 (class ends 10:00)
meet_figure | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
college_event_desk_guy | want | PASS | I'm hard. Help me out. | one-off (A15): want on the same canvas before the act
college_event_desk_guy | next step | PASS | Help him. | look at Curious, hand at Bold
college_event_desk_guy | hook | PASS | Next time, then. | points at the next class
college_event_desk_guy | her voice at her level | PASS | He said it like he was asking for a pen. | Curious/Bold: dry
college_event_desk_guy | who notices | FAIL | He comes over your knuckles, under the desk where nobody sees. | the look and the no have a girl two seats down; the hand path has nobody, and the ledger declares nothing
college_event_desk_guy | the written no | PASS | Worth a try. | written; sets desk_guy_refused
college_event_desk_guy | the body | PASS | You wipe your palm on his thigh while his cock twitches against his open jeans. | 5 explicit words; ends on the body
college_event_desk_guy | the numbers and the clothes agree | N/A | — | no number; only his clothes named
college_event_desk_guy | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_event_desk_guy | true on every visit it can render on | FAIL | He keeps glancing at your hands for the rest of the class. | fires to 09:59 / 11:44 with a minute of class left, then spends 90 minutes 'back to the class'
college_event_desk_guy | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
college_event_dress_code | want | PASS | Think about how you come to class. | the lecturer wants her covered; the rival wants her in trouble
college_event_dress_code | next step | PASS | I told the dean's office. Somebody had to. | after dress_warned, complaints +1
college_event_dress_code | hook | PASS | I told the dean's office. | points at the dean
college_event_dress_code | her voice at her level | N/A | — | no thought of hers, or no meter in play
college_event_dress_code | who notices | PASS | Their eyes go to your chest | lecturer and rival
college_event_dress_code | the written no | N/A | — | no offer is made to her
college_event_dress_code | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_event_dress_code | the numbers and the clothes agree | PASS | Their eyes go to your skirt, and away. | chest and skirt lines behind their checks
college_event_dress_code | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_event_dress_code | true on every visit it can render on | FAIL | Before the class starts, the lecturer calls you down to the front | fires through every class window; at 09:59 the class is ending, not starting
college_event_dress_code | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
college_exam_psych | want | N/A | — | no named person; a proctor only
college_exam_psych | next step | N/A | — | no person on this canvas
college_exam_psych | hook | PASS | The results go up on the portal next week, and on the office door. | points at the portal and the door
college_exam_psych | her voice at her level | PASS | You studied. You actually know this. | reads intelligence
college_exam_psych | who notices | N/A | — | nothing she does here for anyone to notice
college_exam_psych | the written no | N/A | — | no offer is made to her
college_exam_psych | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_exam_psych | the numbers and the clothes agree | PASS | Pens down. | no number contradicted; no garment unbacked
college_exam_psych | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_exam_psych | true on every visit it can render on | FAIL | the clock on the wall starts | the 90-minute midterm starts at Mon/Wed/Fri 09:59, a minute before its slot ends
college_exam_psych | a solo button is a real act | PASS | Focus. Do it yourself. | grade +6 or +1, 90 minutes
college_exam_business | want | PASS | He goes red to the ears. | checked meet_business and college_class_business ("You can have my notes. Seriously, any time."): his want comes earlier
college_exam_business | next step | PASS | his paper is on the corner of his desk, angled your way | past the notes offer
college_exam_business | hook | PASS | The results go up on the portal next week, and on the office door. | points at the portal and the door
college_exam_business | her voice at her level | PASS | You studied. You actually know this. | reads intelligence
college_exam_business | who notices | PASS | He goes red to the ears. | he reacts; campus_talk +1
college_exam_business | the written no | N/A | — | no offer is made to her
college_exam_business | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_exam_business | the numbers and the clothes agree | PASS | Pens down. | no number contradicted; no garment unbacked
college_exam_business | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_exam_business | true on every visit it can render on | FAIL | the clock on the wall starts | the 90-minute midterm starts at Mon/Wed 11:44, a minute before its slot ends
college_exam_business | a solo button is a real act | PASS | Focus. Do it yourself. | grade +6 or +1, 90 minutes
college_exam_bio | want | N/A | — | no named person; a proctor only
college_exam_bio | next step | N/A | — | no person on this canvas
college_exam_bio | hook | PASS | The results go up on the portal next week, and on the office door. | points at the portal and the door
college_exam_bio | her voice at her level | PASS | You studied. You actually know this. | reads intelligence
college_exam_bio | who notices | N/A | — | nothing she does here for anyone to notice
college_exam_bio | the written no | N/A | — | no offer is made to her
college_exam_bio | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
college_exam_bio | the numbers and the clothes agree | PASS | Pens down. | no number contradicted; no garment unbacked
college_exam_bio | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_exam_bio | true on every visit it can render on | FAIL | the clock on the wall starts | the 90-minute midterm starts at Tue/Thu 11:44, a minute before its slot ends
college_exam_bio | a solo button is a real act | PASS | Focus. Do it yourself. | grade +6 or +1, 90 minutes
college_exam_art | want | PASS | Show me and I'll tilt my paper. | checked meet_figure ("He looks you over, slow, and grins") and college_class_figure ("He's drawing you"): his want comes earlier
college_exam_art | next step | PASS | Then you pull everything up under the desk line | flash goes past the drawing
college_exam_art | hook | PASS | The results go up on the portal next week, and on the office door. | points at the portal and the door
college_exam_art | her voice at her level | PASS | You studied. You actually know this. | reads intelligence
college_exam_art | who notices | PASS | His eyes drop to your tits and stay there. | he sees
college_exam_art | the written no | PASS | "No." | written; grade +1 against +5
college_exam_art | the body | PASS | Your nipples are still hard, and his stare is still on your chest. | 5 explicit words; ends on the body
college_exam_art | the numbers and the clothes agree | PASS | One second. Two. Three. | matches 'Three seconds'; no catalog garment named
college_exam_art | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
college_exam_art | true on every visit it can render on | FAIL | the clock on the wall starts | the 90-minute midterm starts at Tue/Thu 09:59, a minute before its slot ends
college_exam_art | a solo button is a real act | PASS | Focus. Do it yourself. | grade +6 or +1, 90 minutes
hub_hale_class | want | PASS | Come and see me on Thursday. | the lecturer wants something of her
hub_hale_class | next step | PASS | — | grade and clothing bands
hub_hale_class | hook | PASS | Come and see me on Thursday. | points at the office
hub_hale_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_hale_class | who notices | PASS | — | the lecturer reacts to the skirt or no bra
hub_hale_class | the written no | N/A | — | no offer is made to her
hub_hale_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_hale_class | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks
hub_hale_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_hale_class | true on every visit it can render on | FAIL | Dr. Hale is laying out his notes on the lectern before the class starts | renders whenever the lecturer's row holds the hall, to the class's last minute
hub_hale_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_art_class | want | PASS | I'd like to draw you one day. | the lecturer wants something of her
hub_art_class | next step | PASS | — | grade and clothing bands
hub_art_class | hook | PASS | I'd like to draw you one day. | points at the office
hub_art_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_art_class | who notices | PASS | — | the lecturer reacts to the skirt or no bra
hub_art_class | the written no | N/A | — | no offer is made to her
hub_art_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_art_class | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks
hub_art_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_art_class | true on every visit it can render on | FAIL | The art lecturer is setting out charcoal at the easels before the class starts | renders whenever the lecturer's row holds the hall, to the class's last minute
hub_art_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_business_class | want | PASS | Failing. Retakes by appointment. | the lecturer wants something of her
hub_business_class | next step | PASS | — | grade and clothing bands
hub_business_class | hook | PASS | Failing. Retakes by appointment. | points at the office
hub_business_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_business_class | who notices | PASS | — | the lecturer reacts to the skirt or no bra
hub_business_class | the written no | N/A | — | no offer is made to her
hub_business_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_business_class | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks
hub_business_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_business_class | true on every visit it can render on | FAIL | The Business lecturer is writing today's headings on the board ... before the class starts | renders whenever the lecturer's row holds the hall, to the class's last minute
hub_business_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_ta_class | want | PASS | My door's open. If you want. | the lecturer wants something of her
hub_ta_class | next step | PASS | — | grade and clothing bands
hub_ta_class | hook | PASS | My door's open. If you want. | points at the office
hub_ta_class | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_ta_class | who notices | PASS | — | the lecturer reacts to the skirt or no bra
hub_ta_class | the written no | N/A | — | no offer is made to her
hub_ta_class | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_ta_class | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks
hub_ta_class | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_ta_class | true on every visit it can render on | FAIL | The TA is setting out handouts before the class starts. | renders whenever the lecturer's row holds the hall, to the class's last minute
hub_ta_class | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_art_office | want | PASS | Stand by the window a moment. The light's good on you. | wants her in the room
hub_art_office | next step | PASS | — | grade and clothing bands
hub_art_office | hook | PASS | Come and sit for me some time. | points at what she can come back for
hub_art_office | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_art_office | who notices | PASS | Stand by the window a moment. The light's good on you. | reacts to her clothes
hub_art_office | the written no | FAIL | Go. | she is asked to stand in the light and sit for her; the only answer is a bare exit
hub_art_office | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_art_office | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks; office hours match the rows
hub_art_office | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_art_office | true on every visit it can render on | PASS | — | office hours = location hours = rows
hub_art_office | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_business_office | want | PASS | Failing. I can offer an honest retake. Nothing else. | wants her in the room
hub_business_office | next step | PASS | — | grade and clothing bands
hub_business_office | hook | PASS | I can offer an honest retake. | points at what she can come back for
hub_business_office | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_business_office | who notices | PASS | Failing. I can offer an honest retake. Nothing else. | reacts to her clothes
hub_business_office | the written no | FAIL | Go. | the retake offer's no is a bare exit, nothing written
hub_business_office | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_business_office | the numbers and the clothes agree | PASS | sits watching you for an hour | 60 minutes on the button; grade +5
hub_business_office | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_business_office | true on every visit it can render on | PASS | — | office hours = location hours = rows
hub_business_office | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_ta_office | want | PASS | I like your— never mind. Sit down. Please. | wants her in the room
hub_ta_office | next step | PASS | — | grade and clothing bands
hub_ta_office | hook | PASS | We should fix your grade. Sit? | points at what she can come back for
hub_ta_office | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_ta_office | who notices | PASS | I like your— never mind. Sit down. Please. | reacts to her clothes
hub_ta_office | the written no | N/A | — | no offer is made to her
hub_ta_office | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_ta_office | the numbers and the clothes agree | PASS | — | clothing lines behind bra/skirt checks; office hours match the rows
hub_ta_office | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_ta_office | true on every visit it can render on | PASS | — | office hours = location hours = rows
hub_ta_office | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
hub_dean_office | want | PASS | Is that what you wear to college? | he wants obedience
hub_dean_office | next step | PASS | You're on probation. | probation band
hub_dean_office | hook | PASS | Don't make me write another letter. | points at another letter
hub_dean_office | her voice at her level | N/A | — | no thought of hers, or no meter in play
hub_dean_office | who notices | PASS | Is that what you wear to college? | reacts to her clothes
hub_dean_office | the written no | N/A | — | no offer is made to her
hub_dean_office | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
hub_dean_office | the numbers and the clothes agree | PASS | — | clothing line behind bra/skirt check
hub_dean_office | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
hub_dean_office | true on every visit it can render on | PASS | You've had your warning. | behind dean_met, set by the warning call
hub_dean_office | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
dean_warning | want | PASS | Consider this your warning. | he wants obedience
dean_warning | next step | PASS | I'm putting you on probation. | her first trouble
dean_warning | hook | PASS | My door is on the faculty floor, if you want to argue. | opens the office
dean_warning | her voice at her level | PASS | A letter home. Laura is going to read every word of it. | fits trouble with Laura
dean_warning | who notices | PASS | Your parents will be getting a letter. | Laura's portal scene reads letter_home
dean_warning | the written no | N/A | — | no offer is made to her
dean_warning | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
dean_warning | the numbers and the clothes agree | N/A | — | no number; no garment named
dean_warning | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
dean_warning | true on every visit it can render on | PASS | Complaints about your conduct in class. | each charge behind its flag; the call rings weekdays 09-17
dean_warning | a solo button is a real act | N/A | — | a person is on this canvas; no solo button
gym_workout | want | N/A | — | no person on this canvas
gym_workout | next step | N/A | — | no person on this canvas
gym_workout | hook | N/A | — | no person on this canvas
gym_workout | her voice at her level | N/A | — | no thought of hers, or no meter in play
gym_workout | who notices | PASS | two guys at the rack stop counting their reps | the gym reacts to the sports bra
gym_workout | the written no | N/A | — | no offer is made to her
gym_workout | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
gym_workout | the numbers and the clothes agree | PASS | Just the sports bra and your bottoms. | sports bra, no top, no dress all checked; jeans line behind jeans
gym_workout | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
gym_workout | true on every visit it can render on | PASS | Treadmill, then the weights, then the mats. | no person, no time word
gym_workout | a solo button is a real act | PASS | Work out an hour. | energy -15, 60 min, worked_out
lecture_timetable | want | N/A | — | no person on this canvas
lecture_timetable | next step | N/A | — | no person on this canvas
lecture_timetable | hook | N/A | — | no person on this canvas
lecture_timetable | her voice at her level | N/A | — | no thought of hers, or no meter in play
lecture_timetable | who notices | N/A | — | nothing she does here for anyone to notice
lecture_timetable | the written no | N/A | — | no offer is made to her
lecture_timetable | the body | N/A | — | no explicit beat (gates.py --beat: under 3 frozen-list words)
lecture_timetable | the numbers and the clothes agree | PASS | Friday: just Psychology, first thing | every day's three slots match the class triggers
lecture_timetable | companion and rival | N/A | — | want.companion_is_rival is not declared in v2_state.json
lecture_timetable | true on every visit it can render on | PASS | Somebody has drawn a penis on Thursday | texture
lecture_timetable | a solo button is a real act | PASS | Read the timetable on the door | shows the reading it names
