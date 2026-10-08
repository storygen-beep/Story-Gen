# v2-reader — first_term, Laura + Mark canvases (29), 2026-10-08

Source: games/first_term/toml_phases/7_final_game.toml (5_scenes.toml). Ledger v2_state.json. Sheets read: people/npc_laura.md, people/npc_mark.md, scenes/mark_07.
Scoreboard (`gates.py first_term`) read first; anything it prints (dead groups in laura_02, laura_catch, hub_laura_kitchen groups 3-6, mark_01 short, mark_07 count, mark_sunday_table table, vance_knock; "Your legs stay open"; history-on-repeatable lines in the Mark hubs; laura_05 unreachable through jake_step/jake_date_booked) is left alone, and dead lines are not used as evidence.
Explicit beats measured with `gates.py --beat` (3+ words): laura_05 kiss (both), laura_07 stairs + door, mark_05 climb/half/stop, mark_07 look, mark_sunday_table look_his + look_hers (all four bands).
Voice tiers: shy <20, warming up 20-59, bold 60+ (corruption/exhibitionism). Weekday 0 = Monday.

scene | test | verdict | the line judged | why
---|---|---|---|---
laura_01_blue_dress | want | PASS | "Somebody should look at you in it." | Laura wants her seen in the dress
laura_01_blue_dress | next step | PASS | "keeps her hands there a second longer than she needs to" | step 1, first touch
laura_01_blue_dress | hook | PASS | "Keep it. Wear it somewhere." | points at wearing it out (the "no" branch ends without one)
laura_01_blue_dress | her voice | N/A | "You don't hate it." | no meter gate on the trigger
laura_01_blue_dress | who notices | PASS | "Her eyes in the mirror aren't on the dress." | Laura reacts
laura_01_blue_dress | written no | PASS | "I can't take this. It's yours." | written node, Warmth +3
laura_01_blue_dress | body | N/A | - | not explicit
laura_01_blue_dress | numbers+clothes | PASS | "Try it on." (equip laura_blue_dress) | dress equipped before the mirror names it
laura_01_blue_dress | companion/rival | N/A | - | not declared
laura_02_home_late | want | PASS | "Did anyone look at you?" | she wants to hear it
laura_02_home_late | next step | PASS | "She pats the step beside her" | catch replaces the dress scene
laura_02_home_late | hook | PASS | "Did anyone look at you in it?" | signed promise
laura_02_home_late | her voice | PASS | "A week. She means every second of it." | warming up (exh 20+), neutral
laura_02_home_late | who notices | PASS | "Smoke. Somebody's cologne." | Laura reads it off her
laura_02_home_late | written no | N/A | - | no offer; a catch
laura_02_home_late | body | N/A | - | not explicit
laura_02_home_late | numbers+clothes | PASS | "You're grounded. A week." | ledger: curfew ends after a week; call reads days_since < 7
laura_02_home_late | companion/rival | N/A | - | -
laura_03_wine_in_the_kitchen | want | PASS | "Sit with me. Just for a bit." | -
laura_03_wine_in_the_kitchen | next step | PASS | "Mark hasn't looked at my body like that since the wedding." | her secret
laura_03_wine_in_the_kitchen | hook | PASS | "She wants somebody to look at her. She's telling you." | -
laura_03_wine_in_the_kitchen | her voice | PASS | same | warming up, mixed
laura_03_wine_in_the_kitchen | who notices | PASS | "Like you get looked at." | -
laura_03_wine_in_the_kitchen | written no | FAIL | "I'm tired, Mom." | button only: no reply, nothing moves
laura_03_wine_in_the_kitchen | body | N/A | - | -
laura_03_wine_in_the_kitchen | numbers+clothes | PASS | "When I was nineteen" | Laura 41, fits
laura_03_wine_in_the_kitchen | companion/rival | N/A | - | -
laura_04_ryans_door | want | PASS | "She's asking like she wants the real answer." | Laura; Ryan's hand on her calf
laura_04_ryans_door | next step | PASS | "It's the first secret you've ever had with her" | -
laura_04_ryans_door | hook | PASS | "Mark doesn't need to hear about this." | -
laura_04_ryans_door | her voice | PASS | "She isn't shouting." | warming up
laura_04_ryans_door | who notices | PASS | "She looks at his hand on your leg." | -
laura_04_ryans_door | written no | N/A | - | no offer made to her
laura_04_ryans_door | body | N/A | - | -
laura_04_ryans_door | numbers+clothes | N/A | - | no garment, no number
laura_04_ryans_door | companion/rival | N/A | - | -
laura_05_jake_at_the_door | want | PASS | "Everyone was looking at you tonight." | earlier: zoe_01_first_party (Jake: "His eyes go down your legs"), laura_01/03 (Laura's look)
laura_05_jake_at_the_door | next step | PASS | "she doesn't pretend she wasn't watching" | -
laura_05_jake_at_the_door | hook | PASS | "Was he any good?" | -
laura_05_jake_at_the_door | her voice | PASS | "She is. She's watching. He doesn't know." | bold/showing gate, appetite
laura_05_jake_at_the_door | who notices | PASS | "Laura's shape stands still, her hand at her own throat." | -
laura_05_jake_at_the_door | written no | FAIL | "Goodnight, Jake." | button only, no written reply
laura_05_jake_at_the_door | body | PASS | "his cock grinds into your hips." | on the body
laura_05_jake_at_the_door | numbers+clothes | PASS | "under the hem of your mother's dress" | inside the dress-equipped group
laura_05_jake_at_the_door | companion/rival | N/A | - | -
laura_06_take_me_with_you | want | PASS | "Take me with you one night." | -
laura_06_take_me_with_you | next step | PASS | "She leans back into your hands" | -
laura_06_take_me_with_you | hook | PASS | "Friday." | -
laura_06_take_me_with_you | her voice | N/A | - | no thought
laura_06_take_me_with_you | who notices | PASS | "In the mirror her cheeks are pink." | -
laura_06_take_me_with_you | written no | FAIL | "Ask Mark." | button only, nothing moves
laura_06_take_me_with_you | body | N/A | - | -
laura_06_take_me_with_you | numbers+clothes | N/A | - | only Laura's dress
laura_06_take_me_with_you | companion/rival | N/A | - | -
laura_07_dark_stairs | want | PASS | "Take me with you tonight. Please." | earlier: laura_06 (her hands), laura_03 (looks at your mouth)
laura_07_dark_stairs | next step | PASS | "she kisses you" | -
laura_07_dark_stairs | hook | PASS | "she'll have to look at you." | -
laura_07_dark_stairs | her voice | PASS | "You want her to do it again." | bold/showing, appetite
laura_07_dark_stairs | who notices | PASS | "Babe. Your mom." / Ryan in the doorway | -
laura_07_dark_stairs | written no | FAIL | "Not tonight, Mom." | button only, nothing moves; no exit at the kiss
laura_07_dark_stairs | body | PASS | "his cock is tenting his shorts." | both beats on the body
laura_07_dark_stairs | numbers+clothes | N/A | - | none of her garments named
laura_07_dark_stairs | companion/rival | N/A | - | -
laura_08_it_wasnt_the_wine | want | PASS | "I'm your mother." | -
laura_08_it_wasnt_the_wine | next step | PASS | "They name the kiss" | -
laura_08_it_wasnt_the_wine | hook | PASS | "Okay. For now." | -
laura_08_it_wasnt_the_wine | her voice | PASS | "She didn't say it was wrong." | -
laura_08_it_wasnt_the_wine | who notices | PASS | "Her hand shakes on the cup" | -
laura_08_it_wasnt_the_wine | written no | PASS | "You're my mom. That's all you get to be." | written, laura_step -1
laura_08_it_wasnt_the_wine | body | N/A | - | -
laura_08_it_wasnt_the_wine | numbers+clothes | N/A | - | Laura's blouse only
laura_08_it_wasnt_the_wine | companion/rival | N/A | - | -
laura_catch | want | PASS | "Tell me where you were. Don't lie to me." | -
laura_catch | next step | PASS | "Kiss her goodnight." | corruption 60 rung
laura_catch | hook | PASS | "Go to bed. Before I ask you anything else." | -
laura_catch | her voice | N/A | "A week. She means every second of it." | no meter gate
laura_catch | who notices | PASS | "She smells it." | -
laura_catch | written no | N/A | - | no offer
laura_catch | body | N/A | - | -
laura_catch | numbers+clothes | PASS | "A week." | matches the ledger
laura_catch | companion/rival | N/A | - | -
hub_laura_kitchen | want | PASS | "Pour me another, would you? Don't tell Mark." | -
hub_laura_kitchen | next step | FAIL | "How's Ryan? You two seem close lately." | the step lines never render (see FAILs)
hub_laura_kitchen | hook | FAIL | "Is Jake bringing you home on Saturday?" | never renders, same chain
hub_laura_kitchen | her voice | N/A | - | no thought
hub_laura_kitchen | who notices | PASS | "Morning. Is that what you're wearing?" | -
hub_laura_kitchen | written no | N/A | - | hub, no offer
hub_laura_kitchen | body | N/A | - | -
hub_laura_kitchen | numbers+clothes | N/A | - | her garment lines never render
hub_laura_kitchen | companion/rival | N/A | - | -
hub_laura_living_room | want | PASS | "Come and sit with me. It's nice in the dark." | -
hub_laura_living_room | next step | PASS | "I saw you, you know. On the step." | -
hub_laura_living_room | hook | PASS | "Who's bringing you home tonight?" | -
hub_laura_living_room | her voice | N/A | - | -
hub_laura_living_room | who notices | PASS | "I didn't look away." | -
hub_laura_living_room | written no | N/A | - | hub
hub_laura_living_room | body | N/A | - | -
hub_laura_living_room | numbers+clothes | N/A | - | -
hub_laura_living_room | companion/rival | N/A | - | -
hub_laura_bedroom | want | PASS | "Black or green? Mark won't notice either way." | -
hub_laura_bedroom | next step | PASS | "She leaves the zip undone and turns her back to you" | -
hub_laura_bedroom | hook | FAIL | "Do I look old in this?" | nothing points forward below step 6
hub_laura_bedroom | her voice | N/A | - | -
hub_laura_bedroom | who notices | N/A | - | she does nothing here
hub_laura_bedroom | written no | N/A | - | hub
hub_laura_bedroom | body | N/A | - | -
hub_laura_bedroom | numbers+clothes | N/A | - | Laura's slip only
hub_laura_bedroom | companion/rival | N/A | - | -
laura_curfew_call | want | PASS | "Then open your door. I'm coming to look." | -
laura_curfew_call | next step | FAIL | "looking at you for longer than she has to" | the same call at every rung
laura_curfew_call | hook | FAIL | "before she says goodnight." | points at nothing
laura_curfew_call | her voice | N/A | - | -
laura_curfew_call | who notices | PASS | "I'm coming to look." | -
laura_curfew_call | written no | N/A | - | -
laura_curfew_call | body | N/A | - | -
laura_curfew_call | numbers+clothes | N/A | - | -
laura_curfew_call | companion/rival | N/A | - | -
mark_01_count_it_slowly | want | PASS | "his eyes go straight to your bare legs, and stay." | step 1, says so
mark_01_count_it_slowly | next step | PASS | "Seventy-five, I said." | first count
mark_01_count_it_slowly | hook | PASS | "The rest waits a week. Vance doesn't." | -
mark_01_count_it_slowly | her voice | N/A | "He counted you as much as the money." | no meter gate
mark_01_count_it_slowly | who notices | PASS | "Ryan leans in the doorway ... watching his father watch you." | -
mark_01_count_it_slowly | written no | PASS | "Let me get dressed first." | written node, no Want +10
mark_01_count_it_slowly | body | N/A | - | -
mark_01_count_it_slowly | numbers+clothes | FAIL | "Not the shirt, next time." | gated on rent only, not on the sleep shirt
mark_01_count_it_slowly | companion/rival | N/A | - | -
mark_02_late_notice | want | PASS | "Put it back." | -
mark_02_late_notice | next step | PASS | "LATE NOTICE" | she learns the debt
mark_02_late_notice | hook | PASS | "You've got something on him now." | -
mark_02_late_notice | her voice | N/A | - | no meter gate
mark_02_late_notice | who notices | PASS | "He sees what's in your hand." | -
mark_02_late_notice | written no | N/A | - | no offer
mark_02_late_notice | body | N/A | - | -
mark_02_late_notice | numbers+clothes | N/A | "a number with a lot of zeros" | no number stated
mark_02_late_notice | companion/rival | N/A | - | -
mark_03_shorts | want | PASS | "Every Sunday. Like that." | earlier: mark_01 (eyes on legs)
mark_03_shorts | next step | PASS | "Not the shirt this time. Shorts." | dress rule
mark_03_shorts | hook | PASS | "Every Sunday. Like that." | -
mark_03_shorts | her voice | N/A | - | no thought
mark_03_shorts | who notices | PASS | "He loses his place twice." | -
mark_03_shorts | written no | FAIL | "I'm not changing for you." | button only, nothing moves
mark_03_shorts | body | N/A | - | -
mark_03_shorts | numbers+clothes | FAIL | "You come down already in your shortest pair of sleep shorts" | the equip is on the next choice
mark_03_shorts | companion/rival | N/A | - | -
mark_04_after_shes_asleep | want | PASS | "he looks at your legs ... from your ankles up." | earlier: mark_01, mark_03
mark_04_after_shes_asleep | next step | PASS | "You know what you're asking me, kid." | -
mark_04_after_shes_asleep | hook | PASS | "He's going to name a number." | -
mark_04_after_shes_asleep | her voice | PASS | "You want to hear it." | warming up
mark_04_after_shes_asleep | who notices | PASS | "He looks at the ceiling, where Laura's asleep." | -
mark_04_after_shes_asleep | written no | FAIL | "I'll pay it Sunday like everyone else." | button only, nothing moves
mark_04_after_shes_asleep | body | N/A | - | -
mark_04_after_shes_asleep | numbers+clothes | N/A | - | no garment named
mark_04_after_shes_asleep | companion/rival | N/A | - | -
mark_05_a_bill_an_inch | want | PASS | "He stares at your legs like a starving man." | earlier: mark_01, mark_03, mark_04
mark_05_a_bill_an_inch | next step | PASS | "Five for every inch" | first paid touch
mark_05_a_bill_an_inch | hook | PASS | "you already want to know what he'll ask for next." | -
mark_05_a_bill_an_inch | her voice | PASS | "Your heart is pounding, but your leg stays put." | warming up
mark_05_a_bill_an_inch | who notices | PASS | "Upstairs, a floorboard creaks. Your mother." | -
mark_05_a_bill_an_inch | written no | PASS | "That's far enough." ($10) | written, half pay
mark_05_a_bill_an_inch | body | PASS | "His cock jerks against the cotton." | all three beats end on the body
mark_05_a_bill_an_inch | numbers+clothes | PASS | "four fives" / "two fives" | $5 an inch, $20 top, matches the ledger
mark_05_a_bill_an_inch | companion/rival | N/A | - | -
mark_06_our_arrangement | want | PASS | "We understand each other." | -
mark_06_our_arrangement | next step | PASS | "So we each keep one." | -
mark_06_our_arrangement | hook | PASS | "He thinks it's even. It isn't." | -
mark_06_our_arrangement | her voice | PASS | same | -
mark_06_our_arrangement | who notices | PASS | "then he nods. Just once." | -
mark_06_our_arrangement | written no | FAIL | "There's no arrangement." | button only, nothing moves
mark_06_our_arrangement | body | N/A | - | -
mark_06_our_arrangement | numbers+clothes | N/A | - | -
mark_06_our_arrangement | companion/rival | N/A | - | -
mark_07_twenty_and_you_can_look | want | PASS | "Mark counts the twenties twice." | earlier: mark_05 (paid touch), mark_04
mark_07_twenty_and_you_can_look | next step | PASS | "Twenty, and you can look." | -
mark_07_twenty_and_you_can_look | hook | FAIL | "He looks as long as the twenty buys" | nothing points at the calendar or Wednesday
mark_07_twenty_and_you_can_look | her voice | N/A | - | no thought
mark_07_twenty_and_you_can_look | who notices | PASS | "His breath goes short." | -
mark_07_twenty_and_you_can_look | written no | FAIL | "Just the rent." | button only
mark_07_twenty_and_you_can_look | body | PASS | "your nipples aching in the cold while his eyes stay on them." | -
mark_07_twenty_and_you_can_look | numbers+clothes | FAIL | "You lay one more twenty on top of it yourself." | she puts down a twenty, yet the button gives +$20
mark_07_twenty_and_you_can_look | companion/rival | N/A | - | -
mark_08_the_red_circle | want | PASS | "His chair's pulled out beside him for nobody." | -
mark_08_the_red_circle | next step | PASS | "Circle Wednesday." | -
mark_08_the_red_circle | hook | PASS | "You'll see." | -
mark_08_the_red_circle | her voice | PASS | "Just him, and his chair." | -
mark_08_the_red_circle | who notices | PASS | "What's that for?" | -
mark_08_the_red_circle | written no | N/A | - | no offer
mark_08_the_red_circle | body | N/A | - | -
mark_08_the_red_circle | numbers+clothes | PASS | "WORK LATE on Wednesday" | matches mark_09 weekday 2
mark_08_the_red_circle | companion/rival | N/A | - | -
mark_09_his_chair | want | PASS | "He's hard in his jeans" | -
mark_09_his_chair | next step | PASS | "He counts it standing up" | -
mark_09_his_chair | hook | PASS | "His lap is right there, waiting" | -
mark_09_his_chair | her voice | PASS | "you're not ready to give him that. Not yet." | -
mark_09_his_chair | who notices | PASS | "stops dead." | -
mark_09_his_chair | written no | FAIL | "No. I count." | button only, nothing moves
mark_09_his_chair | body | N/A | - | -
mark_09_his_chair | numbers+clothes | FAIL | "put this week's rent in front of you" | rent is taken Sunday 00:00, no money moves Wednesday
mark_09_his_chair | companion/rival | N/A | - | -
debt_offer | want | PASS | "So you get to see what your way pays into." | -
debt_offer | next step | PASS | "It's the house." | -
debt_offer | hook | PASS | "he's asking you something without asking." | -
debt_offer | her voice | N/A | - | no meter gate
debt_offer | who notices | PASS | "You pay your way now." | -
debt_offer | written no | FAIL | "It's not my debt, Mark." | button only, same flag as yes
debt_offer | body | N/A | - | -
debt_offer | numbers+clothes | FAIL | "Your seventy-five a week" | the ledger rent is $90 after $300 paid
debt_offer | companion/rival | N/A | - | -
mark_sunday_table | want | PASS | "Sit. Watch me count." | earlier: mark_07
mark_sunday_table | next step | PASS | "Nipples first. Then the rest." | Bold band
mark_sunday_table | hook | FAIL | "Morning. Go on, then." | nothing points forward
mark_sunday_table | her voice | N/A | - | no thought
mark_sunday_table | who notices | PASS | "His eyes go exactly where you send them." | -
mark_sunday_table | written no | FAIL | "Cover up. Give him his twenty back." | button only, nothing moves
mark_sunday_table | body | PASS | "while his eyes stay locked on your nipples." | all four bands end on the body
mark_sunday_table | numbers+clothes | FAIL | "You lay one more twenty on top yourself." | same money contradiction as mark_07
mark_sunday_table | companion/rival | N/A | - | -
vance_knock | want | PASS | "His fingers stay on it a second after yours close." | one-off knock
vance_knock | next step | PASS | "I didn't come for Mark. I came for you, Miss." | Power 60
vance_knock | hook | PASS | "Come and see me one evening." | -
vance_knock | her voice | N/A | - | no meter gate
vance_knock | who notices | PASS | "You're the one who pays in that house now" | -
vance_knock | written no | FAIL | "Close the door." | one button for the offer
vance_knock | body | N/A | - | -
vance_knock | numbers+clothes | PASS | "about Sunday" | matches rent_carried
vance_knock | companion/rival | N/A | - | -
hub_mark_living_room | want | PASS | "Can't sleep, kid?" | -
hub_mark_living_room | next step | PASS | "There's a folded bill on the arm of the couch" | -
hub_mark_living_room | hook | PASS | same | -
hub_mark_living_room | her voice | PASS | "He wants you. He's stopped trying to hide it" | -
hub_mark_living_room | who notices | PASS | "His eyes are on the hem of your sleep shirt." | gated
hub_mark_living_room | written no | N/A | - | hub
hub_mark_living_room | body | N/A | - | -
hub_mark_living_room | numbers+clothes | PASS | "your sleep shirt" | worn_type gate
hub_mark_living_room | companion/rival | N/A | - | -
hub_mark_bedroom | want | FAIL | "His eyes are on the hem of your sleep shirt." | he is asleep
hub_mark_bedroom | next step | PASS | "He keeps looking at the fridge." | -
hub_mark_bedroom | hook | PASS | "There's a folded bill ... Waiting." | -
hub_mark_bedroom | her voice | PASS | "He wants you." | -
hub_mark_bedroom | who notices | FAIL | "That's what you wear in my house?" | a sleeping man reacts
hub_mark_bedroom | written no | N/A | - | hub
hub_mark_bedroom | body | N/A | - | -
hub_mark_bedroom | numbers+clothes | PASS | "your sleep shirt" | gated
hub_mark_bedroom | companion/rival | N/A | - | -
hub_mark_garage | want | PASS | "What do you want? I'm busy." | -
hub_mark_garage | next step | PASS | step lines | -
hub_mark_garage | hook | PASS | "His chair is pulled out from the table for nobody." | -
hub_mark_garage | her voice | PASS | "He wants you." | -
hub_mark_garage | who notices | PASS | "That's what you wear in my house?" | -
hub_mark_garage | written no | N/A | - | hub
hub_mark_garage | body | N/A | - | -
hub_mark_garage | numbers+clothes | PASS | "your sleep shirt" | gated
hub_mark_garage | companion/rival | N/A | - | -
hub_mark_kitchen | want | FAIL | "Morning." | only the weekday line renders
hub_mark_kitchen | next step | FAIL | "There's a folded bill on the arm of the couch" | never renders
hub_mark_kitchen | hook | FAIL | "He keeps looking at the fridge. At the red circle." | never renders
hub_mark_kitchen | her voice | N/A | - | thought never renders
hub_mark_kitchen | who notices | N/A | - | nothing renders to notice
hub_mark_kitchen | written no | N/A | - | hub
hub_mark_kitchen | body | N/A | - | -
hub_mark_kitchen | numbers+clothes | PASS | "Wednesday." / "Sunday." | match his schedule
hub_mark_kitchen | companion/rival | N/A | - | -

## JSON

```json
{"laura_01_blue_dress":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"PASS","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"laura_02_home_late":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"laura_03_wine_in_the_kitchen":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"laura_04_ryans_door":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"laura_05_jake_at_the_door":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"PASS","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"laura_06_take_me_with_you":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"laura_07_dark_stairs":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"PASS","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"laura_08_it_wasnt_the_wine":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"PASS","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"laura_catch":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"hub_laura_kitchen":{"want":"PASS","next step":"FAIL","hook":"FAIL","her voice at her level":"N/A","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"hub_laura_living_room":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"hub_laura_bedroom":{"want":"PASS","next step":"PASS","hook":"FAIL","her voice at her level":"N/A","who notices":"N/A","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"laura_curfew_call":{"want":"PASS","next step":"FAIL","hook":"FAIL","her voice at her level":"N/A","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"mark_01_count_it_slowly":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"PASS","the body":"N/A","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"mark_02_late_notice":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"mark_03_shorts":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"mark_04_after_shes_asleep":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"mark_05_a_bill_an_inch":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"PASS","the body":"PASS","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"mark_06_our_arrangement":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"N/A","companion and rival":"N/A"},"mark_07_twenty_and_you_can_look":{"want":"PASS","next step":"PASS","hook":"FAIL","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"PASS","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"mark_08_the_red_circle":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"mark_09_his_chair":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"debt_offer":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"mark_sunday_table":{"want":"PASS","next step":"PASS","hook":"FAIL","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"PASS","the numbers and the clothes agree":"FAIL","companion and rival":"N/A"},"vance_knock":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"N/A","who notices":"PASS","the written no":"FAIL","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"hub_mark_living_room":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"hub_mark_bedroom":{"want":"FAIL","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"FAIL","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"hub_mark_garage":{"want":"PASS","next step":"PASS","hook":"PASS","her voice at her level":"PASS","who notices":"PASS","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"},"hub_mark_kitchen":{"want":"FAIL","next step":"FAIL","hook":"FAIL","her voice at her level":"N/A","who notices":"N/A","the written no":"N/A","the body":"N/A","the numbers and the clothes agree":"PASS","companion and rival":"N/A"}}
```

## FAILs by test (30)

**want (2)**
- hub_mark_bedroom: "His eyes are on the hem of your sleep shirt." The opening line says "Mark is asleep ... snoring", and his schedule has him in this room only to sleep.
- hub_mark_kitchen: only "Morning." or "It's chilli." renders. The weekday groups head a 15-group chain, and Mark is in the kitchen only on Wednesday and Sunday, so every want, leak and clothes line after them is dead.

**next step (3)**
- hub_laura_kitchen: "How's Ryan? You two seem close lately." never renders. Groups 1-2 (06:30-08:00, 18:00-22:00) are exactly Laura's kitchen hours, so groups 7-19 (all the step leaks) are dead too. The scoreboard prints only groups 3-6.
- laura_curfew_call: "looking at you for longer than she has to" is the same call at every rung of her ladder.
- hub_mark_kitchen: "There's a folded bill on the arm of the couch" never renders (same chain).

**hook (6)**
- hub_laura_kitchen: "Is Jake bringing you home on Saturday?" never renders (same chain).
- hub_laura_bedroom: "Do I look old in this?" Below step 6 nothing points forward.
- laura_curfew_call: "before she says goodnight." It points at nothing.
- mark_07_twenty_and_you_can_look: the scene ends on "He looks as long as the twenty buys". The sheet's hook (the fridge calendar, Wednesday) is not on the canvas.
- mark_sunday_table: "Morning. Go on, then." Nothing points forward, and the look nodes end on the act.
- hub_mark_kitchen: "He keeps looking at the fridge. At the red circle." never renders.

**who notices (1)**
- hub_mark_bedroom: "That's what you wear in my house?" A sleeping man reacts to her clothes.

**the written no (12)**
- laura_03 "I'm tired, Mom." · laura_05 "Goodnight, Jake." · laura_06 "Ask Mark." · laura_07 "Not tonight, Mom." (and the kiss on the stairs has no way out) · mark_03 "I'm not changing for you." · mark_04 "I'll pay it Sunday like everyone else." · mark_06 "There's no arrangement." · mark_07 "Just the rent." (the sheet's "Keep your twenty." is not built) · mark_09 "No. I count." · debt_offer "It's not my debt, Mark." (sets the same flag as yes) · mark_sunday_table "Cover up. Give him his twenty back." · vance_knock "Close the door." (the only answer to "Come and see me one evening"). In every one the refusal is a button with no written reply, and nothing moves except a parked retry.

**the numbers and the clothes agree (6)**
- mark_01_count_it_slowly: "Not the shirt, next time." The group checks rent_carried only. Nothing checks that she is wearing the sleep shirt.
- mark_03_shorts (Power under 50): "You come down already in your shortest pair of sleep shorts". The shorts are equipped only by the next choice.
- mark_07_twenty_and_you_can_look: "You lay one more twenty on top of it yourself." She puts down her own twenty, Mark slides his across, and "Time's up." gives her +$20.
- mark_sunday_table: "You lay one more twenty on top yourself." / "tuck it under the rent". Same money flow against +$20.
- mark_09_his_chair: "put this week's rent in front of you, in a neat pile". The ledger says the engine takes the rent Sunday 00:00. This is Wednesday, and no money moves.
- debt_offer: "Your seventy-five a week is a drop in that." Ledger stages put the rent at $90 after $300 paid. The streak route to pays_her_own_way gets there with exactly $300 paid.

## Seen while reading, outside the nine tests (not verdicts)
- The four Mark hubs share one set of leaks, and each is true in one room only. "folded bill on the arm of the couch" appears in the garage, bedroom and kitchen. "back to the TV" appears in the garage. "Laura's been asleep an hour" appears in the garage at 18:00-22:00. "His chair is pulled out from the table" and "looking at the fridge" appear in the living room.
- laura_catch: "Kiss her goodnight." is gated only on corruption 60. It is open at laura_step 0 and after the final no (step -1).
- mark_sunday_table: the look path sets sunday_counted_today but never touches paid_full_streak, ryan_covered or the streak, so that Sunday's count is skipped. mark_07 handles it.
- mark_05 `no`: "His hand jerks off your thigh". His hand was never on her thigh on either route, and on the Power-under-50 route he holds no bill to fold.
- mark_02 has no requires_npc, but the prose puts Mark next door and then in the doorway.
- Two spans can be false on early play: mark_06 says "off with you at dinner all week" (it can fire the next day), and mark_07 says "every Sunday since the couch" (it can be the first Sunday).
