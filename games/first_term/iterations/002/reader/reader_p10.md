# Reader — first_term, iteration 002, batch p10 (laura_catch, hub_laura_kitchen, hub_tom_cafe, hub_gary_booth, hub_zoe_apartment)

No shipped release, so every canvas counts as touched. I ran gates.py first. Lines it already reports are left alone: "Booth four's going to tip big today." duplicated across canvases, the hl_hungry paragraph pasted in many places, "Further. (Needs Hungry)" gated on a bar the canvas raises, the cafe uniforms both in the `dress` slot, laura_01 "nobody is woken", the "He used to tell you." lint, and the "Done." screens that leave nothing behind.
Weekday 0 = Mon (Zoe's Friday prep is [4], and who_is_where.py puts her at zoe_apartment Fri 18-24). Counter values: laura_step and tom_step equal the ladder n; laura_08's final sets laura_step to -1.

scene | test | verdict | the line judged | why
---|---|---|---|---
laura_catch | want | PASS | "Sit down. Tell me everything. All of it, sweetheart." | She wants to know everything. Not a sexual step (the kiss node is a release door, not explicit).
laura_catch | next step | PASS | "Her knee is bare where the robe has fallen open, and she doesn't fix it." | Variants rise with laura_step/want: grounding, a bare knee, a kiss at step 8 + Corruption 60.
laura_catch | hook | PASS | "Go to bed. Before I ask you anything else." | Names what she is holding back. Grounded names "A week". The kiss names the next release.
laura_catch | her voice at her level | PASS | "You want to kiss her goodnight, right here on the stairs. Not yet." | Appetite held back at Bold (step 8 needs Corruption 40, line is gated under 60).
laura_catch | who notices | PASS | "Smoke in your hair, somebody's cologne on your neck. She smells it from the step." | Laura reads where she has been.
laura_catch | the written no | PASS | "Lie. (she'll know)" → "You think I don't know that face? I invented that face." | The refusal of her "tell me" is written and moves suspicion +10 and warmth -5. At step -1 only "Take what's coming." remains, which matches laura_08's final.
laura_catch | the body | N/A | "You lean down and kiss her, there on the stairs" | Not explicit: --beat gives 0 explicit words for this kind of line.
laura_catch | the numbers and the clothes agree | PASS | "That's it. A week." / "She looks at her dress on you" | curfew_days set to 7, ticked -1 daily. The dress line is behind clothing_item laura_blue_dress equipped.
laura_catch | companion and rival | N/A | — | want.companion_is_rival not set
laura_catch | true on every visit it can render on | PASS | "Laura is on the stairs in her robe, waiting." | Laura is at home_hall 23:00-02:00 (requires_npc). "She waits like this now." is behind laura_02_done. Each truth paragraph is behind its late_* flag, and every came_home_late setter also sets one of those flags. laura_caught_today is cleared at midnight.
laura_catch | a solo button is a real act | N/A | — | no solo button (npc-bound)
hub_laura_kitchen | want | PASS | "Her eyes go to you and stay a second too long. She keeps a second glass on the counter now." | Her want leaks on her hub.
hub_laura_kitchen | next step | PASS | "She's started leaving her bedroom door open when she dresses." | One leak per laura_step 0-7.
hub_laura_kitchen | hook | PASS | "Come upstairs after. I have something for you." | Points at laura_01 (Tue 18-22).
hub_laura_kitchen | her voice at her level | N/A | — | no thought_bubble on this canvas
hub_laura_kitchen | who notices | PASS | "Is that for college or for a guy?" | Laura reacts to her skirt, uniform, make-up, bra and hygiene.
hub_laura_kitchen | the written no | FAIL | "Come upstairs after. I have something for you." | Laura's offer has a yes ("Follow her upstairs."). The only no is "Leave her to it.", a bare link to home_hall that is unwritten and moves nothing. Same for "Could you get these? Here's twenty.": its only answer is "Pocket it."
hub_laura_kitchen | the body | N/A | — | the tease/touch nodes are placeholders. No explicit beat.
hub_laura_kitchen | the numbers and the clothes agree | PASS | "Could you get these? Here's twenty." | money +20, and hl_forgot takes -20. Every garment line is behind a worn_type, clothing_item or clothing_slot check.
hub_laura_kitchen | companion and rival | N/A | — | not set
hub_laura_kitchen | true on every visit it can render on | PASS | "Laura is in her work blouse, buttering toast" (06:30-08:00) / "Ryan slides in next to you, still yawning from the couch." (Sun) | Each button window matches her rows: breakfast Mon-Fri, dinner Mon/Tue/Thu/Fri/Sun, no Wed or Sat evening. Mark and Ryan lines are behind npc_at_location. "She counts it, which she has never done before." is behind laura_counted_twenty. Brakes are cleared in daily_tick.
hub_laura_kitchen | a solo button is a real act | N/A | — | npc-bound hub
hub_tom_cafe | want | PASS | "keeping an eye on the room and an eye on you" | His want shows (Want 50+: "He doesn't even pretend to watch the room.").
hub_tom_cafe | next step | PASS | "His palm is already open on the counter when you come out of booth four." | One leak per tom_step 1-5.
hub_tom_cafe | hook | PASS | "Stay late Friday?" | Names tom_06.
hub_tom_cafe | her voice at her level | N/A | — | no thought on this canvas
hub_tom_cafe | who notices | PASS | "Top button stays open. House rule." | Tom reads her uniform.
hub_tom_cafe | the written no | N/A | "Stay late Friday?" | No answer button on this canvas. The offer is answered in tom_06.
hub_tom_cafe | the body | N/A | — | not explicit
hub_tom_cafe | the numbers and the clothes agree | PASS | "He reties your apron from behind on his way past." | Behind clothing_item cafe_uniform_normal. "Two lattes for six" is a table, not a price.
hub_tom_cafe | companion and rival | N/A | — | not set
hub_tom_cafe | true on every visit it can render on | FAIL | "Tom's behind the counter with a cloth over his shoulder, keeping an eye on the room" + "The sign's turned to CLOSED. Tom's putting the chairs up on the tables." | The café closes at 22:00 and "Back to work." (window to 21:30, +30m) lands her there at 22:00. Both lines then render together: he is behind the counter watching the room and putting chairs up in a closed café. Out of uniform she also gets "Day off? Then you're a customer. Sit where I can see you." under the CLOSED sign.
hub_tom_cafe | a solo button is a real act | N/A | — | npc-bound
hub_gary_booth | want | PASS | "You look lovely today. You always look lovely." | His want is on screen. He is not on a ladder.
hub_gary_booth | next step | PASS | "He pats the seat beside him in the booth and leaves his hand there, palm up." | Escalates once gary_ten_minutes_open + Corruption 40 + uniform.
hub_gary_booth | hook | PASS | "Ten minutes, when you've got them." | Names cafe_gary_ten_minutes.
hub_gary_booth | her voice at her level | N/A | — | no thought
hub_gary_booth | who notices | PASS | "He lowers the paper when you come near, an inch at a time." | He reacts to her approach.
hub_gary_booth | the written no | N/A | "Ten minutes, when you've got them." | No answer on this canvas. The yes and the written "\"No.\"" are in cafe_gary_ten_minutes.
hub_gary_booth | the body | N/A | — | not explicit
hub_gary_booth | the numbers and the clothes agree | PASS | "Ten minutes" | cafe_gary_ten_minutes "Time." spends 10m. No garment named.
hub_gary_booth | companion and rival | N/A | — | not set
hub_gary_booth | true on every visit it can render on | PASS | "Gary in booth four with his paper and his pot of black tea." | Gary is at the café Mon-Fri 14/15-18 and Fri 20-22. The ten-minute line is limited to weekdays 14:30-18:00. gary_met is set at tom_04.
hub_gary_booth | a solo button is a real act | N/A | — | npc-bound
hub_zoe_apartment | want | PASS | "Her eyes keep going to your bra strap." | Her want is on her hub.
hub_zoe_apartment | next step | PASS | "There's a hot tub Saturday. Just us. Don't forget." | One leak per zoe_step 1-3. The lap make-up opens at Corruption 20.
hub_zoe_apartment | hook | PASS | "There's a hot tub Saturday. Just us. Don't forget." | Names zoe_03.
hub_zoe_apartment | her voice at her level | N/A | — | no thought
hub_zoe_apartment | who notices | PASS | "Now we're talking. Turn around." | Zoe reacts to her skirt, bra and dress.
hub_zoe_apartment | the written no | FAIL | "Sit. You're next. Lips first." | Zoe's offer has two yeses (face / face in her lap). The no is "Stay a while." or "Go.", both bare exits that are unwritten and move nothing. "Paint my nails. You've got steadier hands." and "I'm bored. Dare me something." are offers with no answer at all on the canvas.
hub_zoe_apartment | the body | N/A | — | face_lap measured 0 explicit words
hub_zoe_apartment | the numbers and the clothes agree | PASS | "She bites her lip at the strap of her own dress on you." | Behind zoe_party_dress equipped. Bra lines are behind clothing_slot bra. Skirt is behind worn_type short_skirt.
hub_zoe_apartment | companion and rival | N/A | — | want.companion = npc_zoe, but companion_is_rival is not set
hub_zoe_apartment | true on every visit it can render on | PASS | "The party's thinner now, the music lower." (Sat 00-02) | Every clock bucket sits inside Zoe's zoe_apartment rows (Mon-Thu 18-22, Fri 18-24, Sat 00-02 and 18-20). Sunday is excluded. Party lines are split on party_went and its hours.
hub_zoe_apartment | a solo button is a real act | N/A | — | npc-bound

## FAILs by test

**the written no**
- hub_laura_kitchen — "Come upstairs after. I have something for you.": the only no is "Leave her to it.", which is unwritten and moves nothing. "Here's twenty." has only "Pocket it.".
- hub_zoe_apartment — "Sit. You're next. Lips first.": the no is a bare "Stay a while." or "Go.". "Paint my nails." and "Dare me something." have no answer at all.

**true on every visit it can render on**
- hub_tom_cafe — at 22:00 (café closed, reached via "Back to work." 21:30 + 30m), "Tom's behind the counter ... keeping an eye on the room" renders next to "The sign's turned to CLOSED. Tom's putting the chairs up". Out of uniform she also gets "Day off? Then you're a customer."
