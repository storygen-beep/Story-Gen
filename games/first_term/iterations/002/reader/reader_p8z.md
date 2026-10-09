# reader_p8z: first_term, 12 canvases (iteration 002, no shipped release, so every canvas is touched)

Read first: register.md "What a scene contains" + "The truth rule"; gates.py first_term (61/88; red lines for these canvases left alone: ryan_two_knocks "Take it further." gated on own corruption; hub_laura_kitchen "Further. (Needs Hungry)" and the pasted "That's further than you go..." paragraph; hub_tom_cafe "Booth four's going to tip big today." pasted pool and "He used to tell you." [used to] lint; hale_05 Laura speaking unbound; park_hidden / ryan_two_knocks bound to a person with no face; hub_laura_kitchen "Done." 30m leaves nothing); who_is_where.py (weekday 0 = Monday); v2_state.json ladders (want.companion is npc_zoe, companion_is_rival not declared).
Beats measured with gates.py --beat: park_hidden hollow = 5 frozen words (explicit); ryan_two_knocks hands paragraph = 0, its pool lines 0-2 each (not explicit).

scene | test | verdict | the line judged | why
---|---|---|---|---
ryan_two_knocks | want | PASS | "He kisses like he's been waiting all day, because he has." | Ryan visibly wants her; not a sexual step by measure (no beat reaches 3 words), earlier wanting is also on ryan_07_first_kiss and ryan_08_two_knocks
ryan_two_knocks | next step | PASS | "When he pulls you against him you can feel how hard he is" | goes past ryan_08 (terms, one neck kiss) to making out on his bed, his hands over her clothes
ryan_two_knocks | hook | PASS | "This is as far as he'll let himself go. For now." | points at what comes next; "Take it further." shows locked; goodnight sets the next night
ryan_two_knocks | her voice at her level | PASS | "This is as far as he'll let himself go. For now." | appetite, and the step needs corruption 40+
ryan_two_knocks | who notices | PASS | "Mark's TV drones up through the floor." | the ledger says only she knows (step 8); Mark downstairs is the risk
ryan_two_knocks | the written no | PASS | "You give him one kiss at the door, slow, and stop his hands with yours" | the no is written and moves warmth without corruption
ryan_two_knocks | the body | N/A | - | no beat measures explicit
ryan_two_knocks | the numbers and the clothes agree | PASS | "Saturday. Two knocks. Promise me." | Thursday-night line skips Friday, which the trigger leaves out; no garment of hers named
ryan_two_knocks | companion and rival | N/A | - | companion_is_rival not declared
ryan_two_knocks | true on every visit it can render on | PASS | "If Mom hears us, it's your call." | Laura upstairs 22-24, Mark line gated on his presence, weekday/time groups on goodnight agree
ryan_two_knocks | a solo button is a real act | N/A | - | no solo button
laura_catch | want | PASS | "Tell me where you were. Don't lie to me." | she wants the account
laura_catch | next step | PASS | "Her knee is bare where the robe has fallen open, and she doesn't fix it." | escalates by laura_step and want
laura_catch | hook | PASS | "Kiss her goodnight." (show_when_locked) | names the next rung; grounding names "A week"
laura_catch | her voice at her level | N/A | "A week. She means every second of it." | the only thought is about Laura's sentence and is not tied to a level
laura_catch | who notices | PASS | "She smells it from the step." | Laura reacts to where she was
laura_catch | the written no | PASS | "You think I don't know that face? I invented that face." | lying is written and priced (suspicion +10, warmth -5)
laura_catch | the body | N/A | - | not explicit
laura_catch | the numbers and the clothes agree | PASS | "That's it. A week." | curfew_days set 7; her dress gated on laura_blue_dress equipped
laura_catch | companion and rival | N/A | - | not declared
laura_catch | true on every visit it can render on | FAIL | "She doesn't ask. She just looks at you, at your mouth, at your hair." | on a late_date visit with laura_suspicion 30+ the same screen also shows "Tell me where you were. Don't lie to me." (and at step 2+ / want 50+ "Tell me everything"), so she asks and "doesn't ask" on one screen
laura_catch | a solo button is a real act | N/A | - | no solo button
hub_laura_kitchen | want | PASS | "Eat something, sweetheart. You're not going to class on nothing." | she wants her fed, talking, home
hub_laura_kitchen | next step | PASS | "She's started leaving her bedroom door open when she dresses." | a different line at each laura_step
hub_laura_kitchen | hook | PASS | "Come upstairs after. I have something for you." | Tuesday at step 0, plus the locked "Further. (Needs Hungry)"
hub_laura_kitchen | her voice at her level | N/A | - | no thought on the canvas (sub-screens are placeholders)
hub_laura_kitchen | who notices | PASS | "You did your face. Who's that for?" | reacts to clothes, make-up, hygiene
hub_laura_kitchen | the written no | FAIL | "Come upstairs after. I have something for you." | the offer has a yes ("Follow her upstairs.") but the only other way out is the bare "Leave her to it.", which shows nothing and leaves the menu as it was
hub_laura_kitchen | the body | N/A | - | not explicit
hub_laura_kitchen | the numbers and the clothes agree | FAIL | "For ten minutes it's just the two of you and it's easy." | "Talk to her." spends 20 minutes and "Go." 5 more, so 25 minutes pass, not ten
hub_laura_kitchen | companion and rival | N/A | - | not declared
hub_laura_kitchen | true on every visit it can render on | FAIL | "Pour me another, would you? Don't tell Mark." | shows 18:00-22:00 whenever Laura is in the kitchen; who_is_where puts Mark in home_kitchen Sun 08-22 and Mon/Tue/Thu/Fri 18-19 (e.g. Sun 20:00). The same goes for hl_wine's "One glass. Don't tell Mark." (open Sun 20-22)
hub_laura_kitchen | a solo button is a real act | N/A | - | no solo button
hub_tom_cafe | want | PASS | "keeping an eye on the room and an eye on you" | he wants her working and looked at
hub_tom_cafe | next step | PASS | "Gary asks about you, you know. Every day." | a line for each tom_step
hub_tom_cafe | hook | PASS | "Stay late Friday?" | points at tom_06 (Fri 22-23); other steps point at the next one
hub_tom_cafe | her voice at her level | N/A | - | no thought
hub_tom_cafe | who notices | PASS | "Smile. It's worth money." | Tom reacts to her uniform
hub_tom_cafe | the written no | N/A | - | no button offer; "Stay late Friday?" has no answer button on this canvas
hub_tom_cafe | the body | N/A | - | not explicit
hub_tom_cafe | the numbers and the clothes agree | PASS | "Top button stays open. House rule." | every uniform line is gated on worn_type/equipped; "Friday" matches tom_06's window
hub_tom_cafe | companion and rival | N/A | - | not declared
hub_tom_cafe | true on every visit it can render on | FAIL | "Back to work." | the only exit, shown on a day-off visit (not in uniform) where Tom has just said "Day off? Then you're a customer."; the want 50+ line "He watches you the whole shift." shows on that visit too. Also "His palm is already open on the counter when you come out of booth four." shows at step 4 whenever Gary is present, even when she has not been in booth four
hub_tom_cafe | a solo button is a real act | N/A | - | no solo button
hub_zoe_quad | want | PASS | "She just puts her head in your lap and looks up at you" | Zoe wants her close, in public
hub_zoe_quad | next step | PASS | "Her eyes keep going to your bra strap." | a line for each zoe_step
hub_zoe_quad | hook | PASS | "Friday. You're coming. I'm not asking." | names Friday
hub_zoe_quad | her voice at her level | N/A | - | no thought
hub_zoe_quad | who notices | PASS | "when people look over, she says, \"Let them.\"" | the quad watches
hub_zoe_quad | the written no | N/A | - | banter, no offer with buttons
hub_zoe_quad | the body | N/A | - | not explicit
hub_zoe_quad | the numbers and the clothes agree | PASS | "Her eyes keep going to your bra strap." | gated on bra equipped; skirt line on worn_type short_skirt
hub_zoe_quad | companion and rival | N/A | - | not declared
hub_zoe_quad | true on every visit it can render on | PASS | "There's a hot tub Saturday." | Zoe on the quad Tue/Thu/Fri 15-18; the Saturday line is kept off Saturday
hub_zoe_quad | a solo button is a real act | N/A | - | no solo button
hub_zoe_canteen | want | PASS | "Sit. You're with me." | she wants her at her table
hub_zoe_canteen | next step | PASS | "Her eyes keep going to your bra strap." | a line for each step
hub_zoe_canteen | hook | FAIL | "Babe. You will not believe what the TA said to me." | Mon-Wed at zoe_step 0, 1, 3 or 4 (bra on), no line names what comes next; the one forward line ("Friday. Mine.") is gated to Thu/Fri
hub_zoe_canteen | her voice at her level | N/A | - | no thought
hub_zoe_canteen | who notices | PASS | "Now we're talking. Turn around." | Zoe reacts to her clothes
hub_zoe_canteen | the written no | N/A | - | no offer
hub_zoe_canteen | the body | N/A | - | not explicit
hub_zoe_canteen | the numbers and the clothes agree | PASS | "She bites her lip at the strap of her own dress on you." | gated on zoe_party_dress equipped
hub_zoe_canteen | companion and rival | N/A | - | not declared
hub_zoe_canteen | true on every visit it can render on | PASS | "Friday. Mine. Don't make me come and get you." | Thu/Fri only; Zoe in the canteen 11/12-13 on weekdays
hub_zoe_canteen | a solo button is a real act | N/A | - | no solo button
hub_zoe_class | want | PASS | "Sit with me. This is going to be so boring." | she wants her beside her
hub_zoe_class | next step | PASS | "There's a hot tub Saturday. Just us." | a line for each step
hub_zoe_class | hook | FAIL | "Sit with me. This is going to be so boring." | at zoe_step 0, 1, 3 or 4 with a bra on, no line on the screen points at anything coming
hub_zoe_class | her voice at her level | N/A | - | no thought
hub_zoe_class | who notices | PASS | "Now we're talking. Turn around." | Zoe reacts to clothes
hub_zoe_class | the written no | N/A | - | no offer
hub_zoe_class | the body | N/A | - | not explicit
hub_zoe_class | the numbers and the clothes agree | PASS | "Her eyes keep going to your bra strap." | gated on bra equipped
hub_zoe_class | companion and rival | N/A | - | not declared
hub_zoe_class | true on every visit it can render on | PASS | "Zoe drops into the seat beside yours" | Zoe's lecture-hall rows Mon/Wed 13-14, Tue/Thu 09-11
hub_zoe_class | a solo button is a real act | N/A | - | no solo button
hub_zoe_apartment | want | PASS | "Sit. You're next. Lips first." | she wants to do her face, to dare her
hub_zoe_apartment | next step | PASS | "She pulls you into her lap on the couch to do it" | face_lap goes past the plain face
hub_zoe_apartment | hook | PASS | "I'm bored. Dare me something." | points at the dares and the party
hub_zoe_apartment | her voice at her level | N/A | - | no thought
hub_zoe_apartment | who notices | PASS | "She takes longer than she needs to. Neither of you mentions it." | Zoe reacts; made_up is read by Laura's hub
hub_zoe_apartment | the written no | FAIL | "Sit. You're next. Lips first." | the offer (face / face in her lap) has no written no: the only alternatives are "Stay a while." and "Go.", bare exits that show nothing
hub_zoe_apartment | the body | N/A | - | not explicit
hub_zoe_apartment | the numbers and the clothes agree | PASS | "She bites her lip at the strap of her own dress on you." | gated; Zoe's own underwear is hers
hub_zoe_apartment | companion and rival | N/A | - | not declared
hub_zoe_apartment | true on every visit it can render on | FAIL | "Still here? Good girl." | shows Sat 00:00-02:00 with no check that she was at the party (no party_went read); the flat is open then, so on a visit where she has just walked in at 00:30 "still here" is false
hub_zoe_apartment | a solo button is a real act | N/A | - | no solo button
hub_zoe_bedroom | want | PASS | "That one. Put it on. No, here. I want to see." | Zoe wants to watch her change
hub_zoe_bedroom | next step | PASS | "You change in front of her. She doesn't look away once." | lending the dress, then watching her in the mirror once it's hers
hub_zoe_bedroom | hook | PASS | "What else do you want, my underwear?" | names a next step on the owned visit; the not-owned visit offers the dress
hub_zoe_bedroom | her voice at her level | N/A | - | no thought
hub_zoe_bedroom | who notices | PASS | "She doesn't look away once." | Zoe watches
hub_zoe_bedroom | the written no | FAIL | "That one. Put it on. No, here. I want to see." | the no is "Hang it all back up.": 15 minutes, back to the flat, nothing written, nothing changed
hub_zoe_bedroom | the body | N/A | - | not explicit
hub_zoe_bedroom | the numbers and the clothes agree | PASS | "You change in front of her." | backed by the wardrobeEffects equip of zoe_party_dress on the choice
hub_zoe_bedroom | companion and rival | N/A | - | not declared
hub_zoe_bedroom | true on every visit it can render on | PASS | "half ready for sleep and nowhere near it" | Zoe in zoe_bedroom Mon-Thu 22-24
hub_zoe_bedroom | a solo button is a real act | N/A | - | no solo button
hub_zoe_party_house | want | PASS | "Get in. The water's perfect." | she wants her in the tub
hub_zoe_party_house | next step | PASS | "You didn't need me last time, babe." | a step-3 line after the hot tub; zoe_03 fires here first
hub_zoe_party_house | hook | PASS | "Get in. The water's perfect." | points at the tub
hub_zoe_party_house | her voice at her level | N/A | - | no thought
hub_zoe_party_house | who notices | PASS | "There she is. Make room, girls." | Zoe and friends react
hub_zoe_party_house | the written no | FAIL | "Get in. The water's perfect." | there is no yes on the canvas; the answers are "Sit on the edge with your feet in." (20 minutes, back to the same place, nothing shown) and "Go.", neither written, neither moving anything
hub_zoe_party_house | the body | N/A | - | not explicit
hub_zoe_party_house | the numbers and the clothes agree | PASS | "Her eyes keep going to your bra strap." | gated on bra equipped
hub_zoe_party_house | companion and rival | N/A | - | not declared
hub_zoe_party_house | true on every visit it can render on | PASS | "Zoe's in the hot tub on the back deck with two of her friends" | Zoe at party_house Sat 20-24; weekday groups for Friday/Saturday lines are kept off Saturday
hub_zoe_party_house | a solo button is a real act | N/A | - | no solo button
hale_05_seven_twenty | want | PASS | "He doesn't answer, because the answer is you." | opens hale_thursdays (sexual); his earlier wanting is shown on hale_02_lost_his_place (loses his sentence at her legs), hale_03_photo_face_down (hand stays on her shoulder, turns the photo down) and hale_04_claire_knocks ("He wants to touch you")
hale_05_seven_twenty | next step | PASS | "Thursdays at seven. Your office." | turns the one-off into a standing hour
hale_05_seven_twenty | hook | PASS | "Thursdays at seven. Your office. You'll be done by seven-twenty." | names the next scene
hale_05_seven_twenty | her voice at her level | PASS | "He'll watch the clock the whole time. So will you." | appetite at corruption 40+
hale_05_seven_twenty | who notices | PASS | "At dinner that week Laura reads your Psychology midterm" | the ledger says nobody, then Laura reads the midterm
hale_05_seven_twenty | the written no | FAIL | "\"See you in class.\"" | the refusal goes straight to campus with no screen; only a 2-day retry moves
hale_05_seven_twenty | the body | N/A | - | not explicit
hale_05_seven_twenty | the numbers and the clothes agree | PASS | "You'll be done by seven-twenty." | agrees with hale_thursdays "Twenty minutes" and hale_01's "Half past seven" pickup
hale_05_seven_twenty | companion and rival | N/A | - | not declared
hale_05_seven_twenty | true on every visit it can render on | PASS | "He hasn't been able to since the knock." | gated on hale_step 4 (after hale_04); Hale in the lecture hall Mon/Wed/Fri 08:30-10
hale_05_seven_twenty | a solo button is a real act | N/A | - | no solo button
park_hidden | want | PASS | "Come here. I know a place." | sexual step; Zoe's earlier wanting is shown on zoe_03_hot_tub ("Take it off, babe ... Just for me", her eyes on her chest, the kiss), which zoe_step 3+ comes after
park_hidden | next step | PASS | "Her fingers go fast, deep, until your hips buck into her hand." | past zoe_03's kiss to fingering to orgasm
park_hidden | hook | PASS | "Same time next weekend. Don't be late." | names the next time
park_hidden | her voice at her level | N/A | - | no thought
park_hidden | who notices | PASS | "A man walking his dog slows on the path above the hollow, looks your way, and walks on." | a stranger reacts
park_hidden | the written no | PASS | "Your loss, babe." | "Not here, Zo." is written and sets park_cool_zoe
park_hidden | the body | PASS | "Zoe pins you to the bark with her whole body, her mouth on yours to swallow every moan." | last sentence stays on the body (5 frozen words)
park_hidden | the numbers and the clothes agree | N/A | - | no number and no garment of hers named
park_hidden | companion and rival | N/A | - | not declared
park_hidden | true on every visit it can render on | PASS | "Zoe jogs to a stop beside you, pink and breathless" | Zoe in the park Sat/Sun 08-10; trigger 08:00-09:30 plus at most 22 minutes; ran_with_zoe under an hour old
park_hidden | a solo button is a real act | N/A | - | no solo button
