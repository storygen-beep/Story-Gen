# reader — first_term, piece 4 (42 canvases asked; 36 in scope)

Scope: a canvas is read when it has a named person (trigger npc, requires_npc, or a dialog npcId) or an explicit beat (3+ frozen words, measured with `gates.py --beat`). Six canvases have neither and are not judged: cafe_coffee, party_drink_offer, park_walk, park_run, park_rest, park_selfie. (party_drink_offer names Zoe in a pool line but carries no npcId.)

Explicit beats measured: college_class_figure/class 7 · college_event_desk_guy/hand 5 · college_exam_*/flash 5 (same text in all four) · party_dare/flash 4 · party_hookup/oral 5, /sex 7 · park_watch_the_couple/run 7, /watch 11, /touch 9 · park_hidden/hidden 5 · touch_bed 6 · touch_shower 8 · touch_toilet 5. Under 3: zoe_park_dare/dare 0, party_dare/zoe 0, desk_guy/watch 0, figure/risky 1.

scene | test | verdict | the line judged | why
---|---|---|---|---
cafe_shift | want | PASS | Uniform's in the back, @player. Three hours. Smile. | Tom wants her behind the counter, smiling
cafe_shift | next step | PASS | Tom reties your apron on his way past | tom_step/want band and the tight-uniform/no-bra bands take it further
cafe_shift | hook | PASS | Booth four's going to tip big today. | points at booth four (Gary)
cafe_shift | her voice at her level | N/A | You'd drop a tray. Not today. | energy thought only; no meter voice
cafe_shift | who notices | PASS | every man who orders leans a little further over the counter | the room reacts to the uniform
cafe_shift | the written no | N/A | Not today. | a work row, not an offer
cafe_shift | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
cafe_shift | the numbers and the clothes agree | PASS | Clock out. (+$12) / (+$16) / (+$24, Friday tips) | $8+$4, $8+$8, Friday close doubles tips: job sheet rungs 1-3; tight uniform and no bra both gated
cafe_shift | companion and rival | N/A | — | want.companion_is_rival not declared
college_class_psych | want | PASS | He watches you more than the slides. Just saying. | Hale's want, voiced by Nadia; Hale's own lines on hale_step bands
college_class_psych | next step | PASS | He finds you in the front row before he says good morning. | hale_step 2/4 bands and the risky slot step past the plain lecture
college_class_psych | hook | PASS | Under the desk, with the class there. (Needs Hungry) | locked button names the next act
college_class_psych | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
college_class_psych | who notices | PASS | every time he forgets and looks down, his voice goes | Hale and Nadia react to the risky slot
college_class_psych | the written no | N/A | — | no offer on this screen
college_class_psych | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
college_class_psych | the numbers and the clothes agree | PASS | Hale lectures to the back wall for ninety minutes | 90 matches the 90-minute class; skirt line gated on short_skirt
college_class_psych | companion and rival | N/A | — | want.companion_is_rival not declared
college_class_business | want | PASS | You can have my notes. Seriously, any time. | the study guy wants her attention
college_class_business | next step | PASS | For ninety minutes he doesn't write a word. | risky slot (Daring) and the rival's dress_warned line go further
college_class_business | hook | PASS | Make the whole row look. (Needs Hungry) | locked button names the next act
college_class_business | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
college_class_business | who notices | PASS | her mouth gets thinner and thinner | the rival and the study guy react
college_class_business | the written no | N/A | — | no offer on this screen
college_class_business | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
college_class_business | the numbers and the clothes agree | PASS | For ninety minutes | matches the 90-minute slot; clothes line gated on bra/short_skirt
college_class_business | companion and rival | N/A | — | want.companion_is_rival not declared
college_class_bio | want | PASS | If anyone's struggling, my door's open in the afternoons. | the TA wants her in her office; Zoe wants her at the party
college_class_bio | next step | PASS | She drops her pen, picks it up, drops it again. | risky slot and zoe_met band go past the plain class
college_class_bio | hook | PASS | Party Friday. I'm not asking. | names Friday's party
college_class_bio | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
college_class_bio | who notices | PASS | her neck pink all the way down to her collar | the TA reacts
college_class_bio | the written no | N/A | — | no offer on this screen
college_class_bio | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
college_class_bio | the numbers and the clothes agree | PASS | Tuesdays, Thursdays, Fridays. | matches Zoe's quad rows (weekdays 1,3,4, 14:30-18:00)
college_class_bio | companion and rival | N/A | — | want.companion_is_rival not declared
college_class_figure | want | PASS | Look at the weight of her. Draw that. | the lecturer wants her looking; cocky guy band shows his want
college_class_figure | next step | PASS | He's drawing you. | cocky_guy_met band and the risky slot go further
college_class_figure | hook | PASS | Pose for the class. (Needs Watched) | locked button names the next act
college_class_figure | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
college_class_figure | who notices | PASS | Zoe kicks your ankle under the easel. | Zoe and the lecturer react (note: the Zoe line is not gated on zoe_met)
college_class_figure | the written no | N/A | — | no offer on this screen
college_class_figure | the body | PASS | but it's your nipples that ache. | last sentence on the body
college_class_figure | the numbers and the clothes agree | FAIL | Draw with your top button undone. / You undo a button | a buttoned top is named; the gate reads only bra-slot or short_skirt, nothing backs a button
college_class_figure | companion and rival | N/A | — | want.companion_is_rival not declared
meet_business | want | PASS | I'm doing study group Thursday. If you, um. If you want. | study guy wants her; lecturer wants honest work
meet_business | next step | PASS | Oh. You're in this one too. | first meeting, the first step
meet_business | hook | PASS | I'm doing study group Thursday. | names Thursday
meet_business | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
meet_business | who notices | N/A | — | a first meeting; she does nothing to notice
meet_business | the written no | N/A | If you want. | an invitation with no buttons; only 'Find a seat.'
meet_business | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
meet_business | the numbers and the clothes agree | PASS | the Business lecturer, fifty | matches cast age 50
meet_business | companion and rival | N/A | — | want.companion_is_rival not declared
meet_bio | want | PASS | land on you and skip off you, fast, like she touched something hot | the TA's look shows she wants to look
meet_bio | next step | PASS | Hi. I'm— I'll be taking you this term. | first meeting, the first step
meet_bio | hook | FAIL | like she touched something hot. | no line, promise or choice names what comes next; only 'Find a seat.'
meet_bio | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
meet_bio | who notices | N/A | — | a first meeting; she does nothing to notice
meet_bio | the written no | N/A | — | no offer on this screen
meet_bio | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
meet_bio | the numbers and the clothes agree | PASS | a shy woman of twenty-eight | matches cast age 28
meet_bio | companion and rival | N/A | — | want.companion_is_rival not declared
meet_figure | want | PASS | He looks you over, slow, and grins. | cocky guy's want shown at the first meeting
meet_figure | next step | PASS | This is going to be a good class. | first meeting, the first step
meet_figure | hook | PASS | This is going to be a good class. | points at the class and at him
meet_figure | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
meet_figure | who notices | N/A | — | a first meeting; she does nothing to notice
meet_figure | the written no | N/A | — | no offer on this screen
meet_figure | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
meet_figure | the numbers and the clothes agree | PASS | The art lecturer is forty-five | matches cast age 45
meet_figure | companion and rival | N/A | — | want.companion_is_rival not declared
college_event_desk_guy | want | PASS | I'm hard. Help me out. | one-off (A15): his want is on the same canvas before the act
college_event_desk_guy | next step | PASS | Help him. (corruption 40) | Look at Curious, her hand at Bold
college_event_desk_guy | hook | PASS | Next time, then. | points at the next class
college_event_desk_guy | her voice at her level | PASS | He said it like he was asking for a pen. | Curious/Bold band (20-59, warming up): dry, neither prim nor hungry
college_event_desk_guy | who notices | FAIL | He comes over your knuckles, under the desk where nobody sees. | no one beyond him reacts; neither the ledger nor the sheet says nobody notices
college_event_desk_guy | the written no | FAIL | Worth a try. | the 'Not here.' branch is written but moves nothing: no flag, no meter
college_event_desk_guy | the body | PASS | You wipe your palm on his thigh while his cock twitches against his open jeans. | last sentence on the body
college_event_desk_guy | the numbers and the clothes agree | N/A | — | no number; no garment of hers named
college_event_desk_guy | companion and rival | N/A | — | want.companion_is_rival not declared
college_event_dress_code | want | PASS | I told the dean's office. Somebody had to. | the rival wants her in trouble; the lecturer wants her covered
college_event_dress_code | next step | PASS | complaints +1 after dress_warned | the second visit turns the warning into a complaint
college_event_dress_code | hook | PASS | I told the dean's office. | points at the dean
college_event_dress_code | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
college_event_dress_code | who notices | PASS | Their eyes go to your chest | the lecturer and the rival react
college_event_dress_code | the written no | N/A | — | no offer on this screen
college_event_dress_code | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
college_event_dress_code | the numbers and the clothes agree | PASS | Their eyes go to your skirt, and away. | chest and skirt lines gated on bra-slot and short_skirt
college_event_dress_code | companion and rival | N/A | — | want.companion_is_rival not declared
college_exam_psych | want | PASS | Show me and I'll tilt my paper. | checked meet_figure ('He looks you over, slow, and grins') and college_class_figure ('He's drawing you'): his want comes earlier
college_exam_psych | next step | FAIL | One second. Two. Three. | the four midterms are word-for-word the same flash; whichever is played second goes no further
college_exam_psych | hook | PASS | Laura is going to see this. | points at Laura and the portal
college_exam_psych | her voice at her level | N/A | You studied. You actually know this. | intelligence thought, not her meter voice; flash has no thought
college_exam_psych | who notices | PASS | His eyes drop to your tits and stay there. | he sees; the grade goes home to Laura
college_exam_psych | the written no | PASS | "No." (grade +1 against +5) | refusal written and priced in the grade
college_exam_psych | the body | PASS | Your nipples are still hard, and his stare is still on your chest. | last sentence on the body
college_exam_psych | the numbers and the clothes agree | PASS | One second. Two. Three. | matches the node name 'Three seconds'; days 42-56 = weeks 7-8; 40/70 bands match the sheet
college_exam_psych | companion and rival | N/A | — | want.companion_is_rival not declared
college_exam_business | want | PASS | Show me and I'll tilt my paper. | checked meet_figure ('He looks you over, slow, and grins') and college_class_figure ('He's drawing you'): his want comes earlier
college_exam_business | next step | FAIL | One second. Two. Three. | the four midterms are word-for-word the same flash; whichever is played second goes no further
college_exam_business | hook | PASS | Laura is going to see this. | points at Laura and the portal
college_exam_business | her voice at her level | N/A | You studied. You actually know this. | intelligence thought, not her meter voice; flash has no thought
college_exam_business | who notices | PASS | His eyes drop to your tits and stay there. | he sees; the grade goes home to Laura
college_exam_business | the written no | PASS | "No." (grade +1 against +5) | refusal written and priced in the grade
college_exam_business | the body | PASS | Your nipples are still hard, and his stare is still on your chest. | last sentence on the body
college_exam_business | the numbers and the clothes agree | PASS | One second. Two. Three. | matches the node name 'Three seconds'; days 42-56 = weeks 7-8; 40/70 bands match the sheet
college_exam_business | companion and rival | N/A | — | want.companion_is_rival not declared
college_exam_bio | want | PASS | Show me and I'll tilt my paper. | checked meet_figure ('He looks you over, slow, and grins') and college_class_figure ('He's drawing you'): his want comes earlier
college_exam_bio | next step | FAIL | One second. Two. Three. | the four midterms are word-for-word the same flash; whichever is played second goes no further
college_exam_bio | hook | PASS | Laura is going to see this. | points at Laura and the portal
college_exam_bio | her voice at her level | N/A | You studied. You actually know this. | intelligence thought, not her meter voice; flash has no thought
college_exam_bio | who notices | PASS | His eyes drop to your tits and stay there. | he sees; the grade goes home to Laura
college_exam_bio | the written no | PASS | "No." (grade +1 against +5) | refusal written and priced in the grade
college_exam_bio | the body | PASS | Your nipples are still hard, and his stare is still on your chest. | last sentence on the body
college_exam_bio | the numbers and the clothes agree | PASS | One second. Two. Three. | matches the node name 'Three seconds'; days 42-56 = weeks 7-8; 40/70 bands match the sheet
college_exam_bio | companion and rival | N/A | — | want.companion_is_rival not declared
college_exam_art | want | PASS | Show me and I'll tilt my paper. | checked meet_figure ('He looks you over, slow, and grins') and college_class_figure ('He's drawing you'): his want comes earlier
college_exam_art | next step | FAIL | One second. Two. Three. | the four midterms are word-for-word the same flash; whichever is played second goes no further
college_exam_art | hook | PASS | Laura is going to see this. | points at Laura and the portal
college_exam_art | her voice at her level | N/A | You studied. You actually know this. | intelligence thought, not her meter voice; flash has no thought
college_exam_art | who notices | PASS | His eyes drop to your tits and stay there. | he sees; the grade goes home to Laura
college_exam_art | the written no | PASS | "No." (grade +1 against +5) | refusal written and priced in the grade
college_exam_art | the body | PASS | Your nipples are still hard, and his stare is still on your chest. | last sentence on the body
college_exam_art | the numbers and the clothes agree | PASS | One second. Two. Three. | matches the node name 'Three seconds'; days 42-56 = weeks 7-8; 40/70 bands match the sheet
college_exam_art | companion and rival | N/A | — | want.companion_is_rival not declared
hub_hale_class | want | PASS | the way he does when he's waiting to see who stays | Hale wants her to stay
hub_hale_class | next step | PASS | Come and see me on Thursday. | the failing band invites her to his office (the skirt line repeats the class verbatim)
hub_hale_class | hook | PASS | waiting to see who stays | points at staying behind
hub_hale_class | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_hale_class | who notices | PASS | He loses the sentence, and starts it again. | reacts to the short skirt
hub_hale_class | the written no | N/A | — | no choice is offered; only 'Go.'
hub_hale_class | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_hale_class | the numbers and the clothes agree | PASS | Come and see me on Thursday. | Hale's office is Thursday 17:00-19:30
hub_hale_class | companion and rival | N/A | — | want.companion_is_rival not declared
hub_art_class | want | PASS | I'd like to draw you one day. | she wants to draw her
hub_art_class | next step | PASS | That's a good line you're wearing today. | goes past the class: comments on her body
hub_art_class | hook | PASS | I'd like to draw you one day. | names posing (top band)
hub_art_class | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_art_class | who notices | PASS | I mean the shape, not the clothes. | reacts to what she wears
hub_art_class | the written no | N/A | — | no choice is offered; only 'Go.'
hub_art_class | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_art_class | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_art_class | companion and rival | N/A | — | want.companion_is_rival not declared
hub_business_class | want | PASS | This isn't a beach, @player. | he wants her covered and honest
hub_business_class | next step | FAIL | Adequate. | the class already says 'Retakes are by appointment'; nothing here goes further
hub_business_class | hook | PASS | Failing. Retakes by appointment. | points at the retake (failing band)
hub_business_class | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_business_class | who notices | PASS | This isn't a beach, @player. | reacts to what she wears
hub_business_class | the written no | N/A | — | no choice is offered; only 'Go.'
hub_business_class | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_business_class | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_business_class | companion and rival | N/A | — | want.companion_is_rival not declared
hub_ta_class | want | PASS | You look— sorry. Nothing. You look nice. | the TA wants to look
hub_ta_class | next step | PASS | You look nice. | she says what the class only shows
hub_ta_class | hook | PASS | My door's open. If you want. | points at her office (failing band)
hub_ta_class | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_ta_class | who notices | PASS | drops half of them | reacts to her
hub_ta_class | the written no | N/A | — | no choice is offered; only 'Go.'
hub_ta_class | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_ta_class | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_ta_class | companion and rival | N/A | — | want.companion_is_rival not declared
hub_art_office | want | PASS | Stand by the window a moment. The light's good on you. | she wants to look at her
hub_art_office | next step | PASS | Come and sit for me some time. | an ask to pose, past the class
hub_art_office | hook | PASS | Come and sit for me some time. | names posing
hub_art_office | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_art_office | who notices | PASS | The light's good on you. | reacts to what she wears
hub_art_office | the written no | N/A | — | no choice is offered; only 'Go.'
hub_art_office | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_art_office | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_art_office | companion and rival | N/A | — | want.companion_is_rival not declared
hub_business_office | want | PASS | Keep it honest. | he wants honest work
hub_business_office | next step | PASS | I'll take the retake. | the retake is a real step
hub_business_office | hook | PASS | I can offer an honest retake. Nothing else. | names the retake
hub_business_office | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_business_office | who notices | PASS | It won't change your grade. Nothing does. | reacts to what she wears
hub_business_office | the written no | N/A | Go. | the retake is a service row, not an offer
hub_business_office | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_business_office | the numbers and the clothes agree | PASS | Hand it in. (Business +5) | +5 on the label matches the effect; 'an hour' matches 60 minutes
hub_business_office | companion and rival | N/A | — | want.companion_is_rival not declared
hub_ta_office | want | PASS | Oh! Hi. Your grade. Um. We should fix your grade. Sit? | she wants her to stay
hub_ta_office | next step | PASS | I like your— never mind. Sit down. Please. | goes past the class: she nearly says it
hub_ta_office | hook | PASS | We should fix your grade. Sit? | points at help with the grade
hub_ta_office | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_ta_office | who notices | PASS | She jumps when you knock. | reacts to her
hub_ta_office | the written no | N/A | — | no choice is offered; only 'Go.'
hub_ta_office | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_ta_office | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_ta_office | companion and rival | N/A | — | want.companion_is_rival not declared
hub_dean_office | want | PASS | You're not in trouble. Yet. Keep it that way. | he wants obedience
hub_dean_office | next step | FAIL | Every grade, every complaint, crosses my desk now. | restates dean_warning; nothing goes further
hub_dean_office | hook | PASS | You're not in trouble. Yet. | points at trouble to come
hub_dean_office | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
hub_dean_office | who notices | PASS | Is that what you wore to class? | reacts to what she wears
hub_dean_office | the written no | N/A | — | no choice is offered; only 'Go.'
hub_dean_office | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
hub_dean_office | the numbers and the clothes agree | N/A | — | no number; no garment named
hub_dean_office | companion and rival | N/A | — | want.companion_is_rival not declared
dean_warning | want | PASS | Consider this your warning. | the dean wants her in line
dean_warning | next step | PASS | I'm putting you on probation. | her first trouble
dean_warning | hook | PASS | A letter home. Laura is going to read every word of it. | points at the letter at home
dean_warning | her voice at her level | N/A | A letter home. | thought present, but no corruption/exhibitionism meter in play
dean_warning | who notices | PASS | Your parents will be getting a letter. | the dean, then Laura
dean_warning | the written no | N/A | — | no offer on this screen
dean_warning | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
dean_warning | the numbers and the clothes agree | FAIL | Two complaints about your conduct in class. | shown at complaints gte 2, but a missed dean call adds +1 and later dress-code visits add more: at 3+ it still says two
dean_warning | companion and rival | N/A | — | want.companion_is_rival not declared
laura_reads_grade_psych | want | PASS | Do you want to explain this to me, sweetheart? | Laura wants her good girl back
laura_reads_grade_psych | next step | PASS | After the letter. After the dean wrote to us. | letter_home band and the curfew branch go further
laura_reads_grade_psych | hook | PASS | A week. No parties, no late shifts, no dates. | names the curfew week
laura_reads_grade_psych | her voice at her level | N/A | — | no thought of hers on screen
laura_reads_grade_psych | who notices | PASS | She turns the phone round so you can see it. | Laura reacts to the grade
laura_reads_grade_psych | the written no | N/A | — | no offer on this screen
laura_reads_grade_psych | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
laura_reads_grade_psych | the numbers and the clothes agree | PASS | A week. | curfew_days set 7; suspicion gte 45 +5 = the sheet's curfew at 50
laura_reads_grade_psych | companion and rival | N/A | — | want.companion_is_rival not declared
party_arrive | want | PASS | Not in that. Borrow mine. Bedroom. Go. | Zoe wants her dressed up and inside
party_arrive | next step | FAIL | Babe! Get in here. Now we're talking. | a fixed door line every Friday; no band reads her steps
party_arrive | hook | PASS | Borrow Zoe's dress first. | the choice names the next screen
party_arrive | her voice at her level | N/A | — | no thought of hers on screen; the only thoughts are needs (energy/curfew)
party_arrive | who notices | PASS | Not in that. | Zoe reacts to what she wears
party_arrive | the written no | N/A | Go home. | a door, not an offer
party_arrive | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
party_arrive | the numbers and the clothes agree | PASS | Go in. (15 energy) / The party is Friday nights, from seven. | 15 matches cost and the parties sheet; 19:00 matches the trigger
party_arrive | companion and rival | N/A | — | want.companion_is_rival not declared
party_chat | want | PASS | You're a hit, babe. Everyone's asking about you. | Zoe wants her a hit
party_chat | next step | FAIL | You're a hit, babe. Everyone's asking about you. | fixed line; campus_talk rises but nothing here reads it
party_chat | hook | PASS | the cocky one from Figure drawing, is leaning on the bathroom door. Watching you. | points at the hookup (when he is there)
party_chat | her voice at her level | N/A | — | no thought of hers on screen
party_chat | who notices | PASS | Everyone's asking about you. | Zoe and the room react
party_chat | the written no | N/A | — | no offer on this screen
party_chat | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
party_chat | the numbers and the clothes agree | N/A | — | no number that matters; no garment named
party_chat | companion and rival | N/A | — | want.companion_is_rival not declared
party_dare | want | PASS | Flash them, babe. Three seconds. | checked zoe_02 ('Bra off. Through the sleeve... That's the dare') and zoe_03 ('I want to see your tits'): her want comes earlier
party_dare | next step | PASS | Or dare me. Go on. You pick now. | after zoe_04 she can dare Zoe back
party_dare | hook | PASS | Next one's yours. / Or dare me. | points at the next dare
party_dare | her voice at her level | N/A | — | no thought of hers on screen
party_dare | who notices | PASS | Somebody whistles. | the circle reacts; campus_talk +1
party_dare | the written no | FAIL | Boo. Fine. Next one's yours. | refusal written but moves nothing; the parties sheet's party_cool_<npc> flag and one more push are not built
party_dare | the body | PASS | You hold them out a breath past the count, nipples stiff and aching, before you let everything drop. | last sentence on the body
party_dare | the numbers and the clothes agree | PASS | "One," ... "Two." ... "Three." | count matches 'Three seconds'; no garment named ('pull everything up')
party_dare | companion and rival | N/A | — | want.companion_is_rival not declared
party_hookup | want | PASS | He's been watching you all night. | checked meet_figure, college_class_figure and party_chat: his want comes earlier, and again on this canvas
party_hookup | next step | PASS | Get on your knees. / Pull him in. | oral or sex, past the exam flash
party_hookup | hook | PASS | By Monday half of campus will know. | points at campus talk
party_hookup | her voice at her level | PASS | You find you don't mind. | Bold stage, warming-up band (40-59): acceptance, not pushback, not hunger
party_hookup | who notices | PASS | In my bathroom? Babe. | Zoe sees them come out
party_hookup | the written no | FAIL | Your loss. | refusal written but moves nothing; once the door locks there is no way out
party_hookup | the body | PASS | You come clenching around his cock, your heels digging into his ass. | both beats end on the body (oral: 'then wipe your lip with your thumb')
party_hookup | the numbers and the clothes agree | N/A | — | no number; no garment of hers named
party_hookup | companion and rival | N/A | — | want.companion_is_rival not declared
park_watch_the_couple | want | PASS | He holds her hips from behind. | strangers (A15): the couple's want is on the same canvas
park_watch_the_couple | next step | PASS | Touch yourself while you watch. | run at stage 1, watch at Curious, touching herself after
park_watch_the_couple | hook | PASS | Touch yourself while you watch. | the choice names the next act
park_watch_the_couple | her voice at her level | PASS | You know exactly what that is. You could leave. You don't want to. | warming-up band: pushback and want together
park_watch_the_couple | who notices | FAIL | Neither of them looks toward the bush. | on the watch and touch paths nobody notices, and nothing declares it (only the run path has him look up)
park_watch_the_couple | the written no | N/A | Walk the other way. | no one makes her an offer
park_watch_the_couple | the body | PASS | your fingers keep working your clit through it. | run, watch and touch all end on the body
park_watch_the_couple | the numbers and the clothes agree | N/A | — | no number; no garment of hers named
park_watch_the_couple | companion and rival | N/A | — | want.companion_is_rival not declared
park_hidden | want | PASS | Come here. I know a place. | checked zoe_03 ('I want to see your tits') and zoe_04 ('She wanted you'): her want comes earlier
park_hidden | next step | PASS | Her hand slides down inside | in public, her fingers, past the hot-tub kiss
park_hidden | hook | FAIL | her mouth on yours to swallow every moan. | the yes path ends on 'Back to the path.'; nothing names what comes next
park_hidden | her voice at her level | N/A | — | no thought of hers on screen
park_hidden | who notices | FAIL | Footsteps crunch past, close enough to touch, but Zoe doesn't stop. | nobody notices and nothing declares it
park_hidden | the written no | FAIL | Your loss, babe. | refusal written but moves nothing
park_hidden | the body | PASS | Zoe pins you to the bark with her whole body, her mouth on yours to swallow every moan. | last sentence on the body
park_hidden | the numbers and the clothes agree | PASS | weekdays 5, 6 / 08:00-10:00 | matches Zoe's park row; no garment named
park_hidden | companion and rival | N/A | — | want.companion_is_rival not declared
zoe_park_dare | want | PASS | Flash me. Right here. Two seconds. | checked zoe_00 ('Wear something short', 'a beat too long'): her want comes earlier
zoe_park_dare | next step | PASS | pull everything up for one long second | a flash in public, past the quad meeting and the party dress
zoe_park_dare | hook | FAIL | Oh my god. I love you. Run! | nothing names what comes next
zoe_park_dare | her voice at her level | N/A | — | no thought of hers on screen
zoe_park_dare | who notices | PASS | The guy on the bench drops his coffee. | Zoe and a stranger react
zoe_park_dare | the written no | FAIL | Chicken. | refusal written but moves nothing
zoe_park_dare | the body | N/A | — | not explicit (0 frozen words)
zoe_park_dare | the numbers and the clothes agree | PASS | Two seconds. / one long second | her own choice to hold it shorter, not one span said two ways; trigger needs a top, no garment named
zoe_park_dare | companion and rival | N/A | — | want.companion_is_rival not declared
touch_bed | want | N/A | — | no person on the canvas
touch_bed | next step | N/A | — | no person on the canvas
touch_bed | hook | N/A | — | a solo loop, no person
touch_bed | her voice at her level | N/A | — | no thought bubble
touch_bed | who notices | N/A | — | private; nothing to notice
touch_bed | the written no | N/A | — | no offer on this screen
touch_bed | the body | PASS | You come with your thighs clamped on your wrist, legs shaking, fingers still pressed to your clit. | last sentence on the body
touch_bed | the numbers and the clothes agree | N/A | — | no garment of hers named
touch_bed | companion and rival | N/A | — | want.companion_is_rival not declared
touch_shower | want | N/A | — | no person on the canvas
touch_shower | next step | N/A | — | no person on the canvas
touch_shower | hook | N/A | — | a solo loop, no person
touch_shower | her voice at her level | N/A | — | no thought bubble
touch_shower | who notices | N/A | — | private; nothing to notice
touch_shower | the written no | N/A | — | no offer on this screen
touch_shower | the body | PASS | Your knees go weak, and you hold the tile while your clit throbs under your hand. | last sentence on the body
touch_shower | the numbers and the clothes agree | PASS | You lock the door and step naked under the hot water. | undressing inside the act
touch_shower | companion and rival | N/A | — | want.companion_is_rival not declared
touch_toilet | want | N/A | — | no person on the canvas
touch_toilet | next step | N/A | — | no person on the canvas
touch_toilet | hook | N/A | — | a solo loop, no person
touch_toilet | her voice at her level | N/A | — | no thought bubble
touch_toilet | who notices | N/A | — | private; nothing to notice
touch_toilet | the written no | N/A | — | no offer on this screen
touch_toilet | the body | PASS | The orgasm hits without a sound, and your thighs clamp shut on your hand. | last sentence on the body
touch_toilet | the numbers and the clothes agree | N/A | Get dressed. | no garment named (the exit says 'Get dressed' though nothing came off)
touch_toilet | companion and rival | N/A | — | want.companion_is_rival not declared
wardrobe_event_stairs | want | PASS | He looks up the stairs, straight up your skirt, and doesn't look away | Mark's want, Ryan's eyes, Laura's question
wardrobe_event_stairs | next step | FAIL | straight up your skirt, and doesn't look away until you're on the landing. | no band reads mark_step, ryan_step or a meter; the same look every time
wardrobe_event_stairs | hook | PASS | Is that for college or for a guy? | points at Laura's suspicion
wardrobe_event_stairs | her voice at her level | N/A | — | no thought of hers on screen
wardrobe_event_stairs | who notices | PASS | Is that for college or for a guy? | Mark, Ryan and Laura react
wardrobe_event_stairs | the written no | N/A | — | no offer on this screen
wardrobe_event_stairs | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
wardrobe_event_stairs | the numbers and the clothes agree | PASS | There's nothing under the skirt. | skirt backed by the trigger; nothing-under gated on underwear unequipped
wardrobe_event_stairs | companion and rival | N/A | — | want.companion_is_rival not declared
kitchen_uniform_home | want | PASS | Where's a waitress get twenties, wearing that? | Mark wants control; Laura wants her good girl
kitchen_uniform_home | next step | FAIL | Look at you. My working girl. | fixed lines; no step or meter band moves them
kitchen_uniform_home | hook | PASS | Where's a waitress get twenties, wearing that? | points at the money and what she does for it
kitchen_uniform_home | her voice at her level | N/A | — | no thought of hers on screen
kitchen_uniform_home | who notices | FAIL | You come in through the kitchen still in your café uniform | Laura with the tight uniform, Mark with the normal one, or Ryan in the kitchen: nobody reacts
kitchen_uniform_home | the written no | N/A | — | no offer on this screen
kitchen_uniform_home | the body | N/A | — | no explicit beat (gates --beat: under 3 frozen words)
kitchen_uniform_home | the numbers and the clothes agree | PASS | still in your café uniform, apron stuffed in your bag | backed by worn_type cafe_uniform; the sexy and normal lines are each item-gated
kitchen_uniform_home | companion and rival | N/A | — | want.companion_is_rival not declared

```json
{
 "cafe_shift": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_class_psych": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_class_business": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_class_bio": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_class_figure": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "PASS",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A"
 },
 "meet_business": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "meet_bio": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "meet_figure": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_event_desk_guy": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "FAIL",
  "the written no": "FAIL",
  "the body": "PASS",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "college_event_dress_code": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_exam_psych": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_exam_business": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_exam_bio": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "college_exam_art": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "hub_hale_class": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "hub_art_class": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "hub_business_class": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "hub_ta_class": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "hub_art_office": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "hub_business_office": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "hub_ta_office": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "hub_dean_office": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "dean_warning": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A"
 },
 "laura_reads_grade_psych": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "party_arrive": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "party_chat": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "party_dare": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "FAIL",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "party_hookup": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "FAIL",
  "the body": "PASS",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "park_watch_the_couple": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "FAIL",
  "the written no": "N/A",
  "the body": "PASS",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "park_hidden": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "FAIL",
  "the written no": "FAIL",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "zoe_park_dare": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "FAIL",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "touch_bed": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "PASS",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "touch_shower": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "touch_toilet": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "PASS",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A"
 },
 "wardrobe_event_stairs": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 },
 "kitchen_uniform_home": {
  "want": "PASS",
  "next step": "FAIL",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "FAIL",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A"
 }
}
```

## FAILs by test

**next step**
- college_exam_psych: "One second. Two. Three.": the four midterms are word-for-word the same flash; whichever is played second goes no further
- college_exam_business: "One second. Two. Three.": the four midterms are word-for-word the same flash; whichever is played second goes no further
- college_exam_bio: "One second. Two. Three.": the four midterms are word-for-word the same flash; whichever is played second goes no further
- college_exam_art: "One second. Two. Three.": the four midterms are word-for-word the same flash; whichever is played second goes no further
- hub_business_class: "Adequate.": the class already says 'Retakes are by appointment'; nothing here goes further
- hub_dean_office: "Every grade, every complaint, crosses my desk now.": restates dean_warning; nothing goes further
- party_arrive: "Babe! Get in here. Now we're talking.": a fixed door line every Friday; no band reads her steps
- party_chat: "You're a hit, babe. Everyone's asking about you.": fixed line; campus_talk rises but nothing here reads it
- wardrobe_event_stairs: "straight up your skirt, and doesn't look away until you're on the landing.": no band reads mark_step, ryan_step or a meter; the same look every time
- kitchen_uniform_home: "Look at you. My working girl.": fixed lines; no step or meter band moves them

**hook**
- meet_bio: "like she touched something hot.": no line, promise or choice names what comes next; only 'Find a seat.'
- park_hidden: "her mouth on yours to swallow every moan.": the yes path ends on 'Back to the path.'; nothing names what comes next
- zoe_park_dare: "Oh my god. I love you. Run!": nothing names what comes next

**who notices**
- college_event_desk_guy: "He comes over your knuckles, under the desk where nobody sees.": no one beyond him reacts; neither the ledger nor the sheet says nobody notices
- park_watch_the_couple: "Neither of them looks toward the bush.": on the watch and touch paths nobody notices, and nothing declares it (only the run path has him look up)
- park_hidden: "Footsteps crunch past, close enough to touch, but Zoe doesn't stop.": nobody notices and nothing declares it
- kitchen_uniform_home: "You come in through the kitchen still in your café uniform": Laura with the tight uniform, Mark with the normal one, or Ryan in the kitchen: nobody reacts

**the written no**
- college_event_desk_guy: "Worth a try.": the 'Not here.' branch is written but moves nothing: no flag, no meter
- party_dare: "Boo. Fine. Next one's yours.": refusal written but moves nothing; the parties sheet's party_cool_<npc> flag and one more push are not built
- party_hookup: "Your loss.": refusal written but moves nothing; once the door locks there is no way out
- park_hidden: "Your loss, babe.": refusal written but moves nothing
- zoe_park_dare: "Chicken.": refusal written but moves nothing

**the numbers and the clothes agree**
- college_class_figure: "Draw with your top button undone. / You undo a button": a buttoned top is named; the gate reads only bra-slot or short_skirt, nothing backs a button
- dean_warning: "Two complaints about your conduct in class.": shown at complaints gte 2, but a missed dean call adds +1 and later dress-code visits add more: at 3+ it still says two
