scene | test | PASS / FAIL / N/A | the line judged (quoted, short) | why (one line)
---|---|---|---|---
room_sleep | want | N/A | — | solo canvas, no person on screen
room_sleep | next step | N/A | — | solo canvas, no person on screen
room_sleep | hook | N/A | — | solo canvas, no person on screen
room_sleep | her voice at her level | N/A | — | solo canvas, no person on screen
room_sleep | who notices | N/A | — | solo canvas, no person on screen
room_sleep | the written no | N/A | — | solo canvas, no person on screen
room_sleep | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
room_sleep | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
room_sleep | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
room_sleep | true on every visit it can render on | PASS | Through the wall, Ryan's music thumps low. | gated on Ryan in his room and 19:00-00:00; his rows hold him there awake
room_sleep | a solo button is a real act | PASS | Sleep till morning. | energy set 100, clock to ~06:30-07:29, late flags cleared
room_nap | want | N/A | — | solo canvas, no person on screen
room_nap | next step | N/A | — | solo canvas, no person on screen
room_nap | hook | N/A | — | solo canvas, no person on screen
room_nap | her voice at her level | N/A | — | solo canvas, no person on screen
room_nap | who notices | N/A | — | solo canvas, no person on screen
room_nap | the written no | N/A | — | solo canvas, no person on screen
room_nap | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
room_nap | the numbers and the clothes agree | PASS | Sleep two hours. | button spends 120 min
room_nap | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
room_nap | true on every visit it can render on | PASS | The light through the curtains goes orange | 07:00-19:00 only; nothing time-bound false
room_nap | a solo button is a real act | PASS | Sleep two hours. | +30 energy, 120 min
room_study | want | N/A | — | solo canvas, no person on screen
room_study | next step | N/A | — | solo canvas, no person on screen
room_study | hook | N/A | — | solo canvas, no person on screen
room_study | her voice at her level | N/A | — | solo canvas, no person on screen
room_study | who notices | N/A | — | solo canvas, no person on screen
room_study | the written no | N/A | — | solo canvas, no person on screen
room_study | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
room_study | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
room_study | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
room_study | true on every visit it can render on | PASS | It's dull, but the exams read it. | no claim tied to time or people
room_study | a solo button is a real act | PASS | Psychology. | grade +1, energy -10, 60 min, studied_home
room_makeup | want | N/A | — | solo canvas, no person on screen
room_makeup | next step | N/A | — | solo canvas, no person on screen
room_makeup | hook | N/A | — | solo canvas, no person on screen
room_makeup | her voice at her level | PASS | You know exactly who you're doing it for: anybody who looks. | appetite line gated exhibitionism gte 20; nothing at low level
room_makeup | who notices | PASS | flag made_up | Laura reads made_up within 10 h (7_final_game.toml:7161)
room_makeup | the written no | N/A | — | solo canvas, no person on screen
room_makeup | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
room_makeup | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
room_makeup | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
room_makeup | true on every visit it can render on | PASS | Darker on the eyes than you'd wear for class. | no time or person claim
room_makeup | a solo button is a real act | PASS | Done. | 15 min, made_up + made_up_today set
room_tidy | want | N/A | — | solo canvas, no person on screen
room_tidy | next step | N/A | — | solo canvas, no person on screen
room_tidy | hook | N/A | — | solo canvas, no person on screen
room_tidy | her voice at her level | N/A | — | solo canvas, no person on screen
room_tidy | who notices | PASS | flag room_tidy | read at the Sunday table (7_final_game.toml:7586-7636)
room_tidy | the written no | N/A | — | solo canvas, no person on screen
room_tidy | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
room_tidy | the numbers and the clothes agree | PASS | It takes half an hour | button spends 30 min
room_tidy | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
room_tidy | true on every visit it can render on | PASS | the mugs carried down | no time or person claim
room_tidy | a solo button is a real act | PASS | Done. | 30 min, energy -5, room_tidy set
bathroom_shower | want | PASS | "Sorry," he says through the door, and doesn't move away from it for a long second. | Ryan's lingering shows his want; not a sexual step
bathroom_shower | next step | N/A | — | ambient reaction on a repeatable solo button, not a scene with Ryan
bathroom_shower | hook | N/A | — | ambient reaction on a repeatable solo button
bathroom_shower | her voice at her level | FAIL | Nobody can see, but you take your time like someone could. | exhibitionist appetite in a pool line with no meter gate; renders at exhibitionism 0
bathroom_shower | who notices | PASS | Laura's voice floats up the stairs. "Leave some hot water, sweetheart!" | Ryan, Mark and Laura each react when their rows put them home
bathroom_shower | the written no | N/A | — | solo canvas, no person on screen
bathroom_shower | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
bathroom_shower | the numbers and the clothes agree | PASS | For ten minutes the house can't get at you. | ten minutes under the water inside a 20-min button; no garment named, towel equipped on exit
bathroom_shower | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
bathroom_shower | true on every visit it can render on | PASS | Ryan's door opens across the hall. | gated on Ryan in his room; his rows there are not asleep
bathroom_shower | a solo button is a real act | PASS | Wrap up in a towel. | hygiene +50, 20 min, towel equipped
bathroom_mirror | want | N/A | — | solo canvas, no person on screen
bathroom_mirror | next step | N/A | — | solo canvas, no person on screen
bathroom_mirror | hook | N/A | — | solo canvas, no person on screen
bathroom_mirror | her voice at her level | N/A | — | solo canvas, no person on screen
bathroom_mirror | who notices | N/A | — | solo canvas, no person on screen
bathroom_mirror | the written no | N/A | — | solo canvas, no person on screen
bathroom_mirror | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
bathroom_mirror | the numbers and the clothes agree | PASS | the towel tucked over your tits | each garment line sits in a group on worn_type / clothing_slot / worn_exposure
bathroom_mirror | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
bathroom_mirror | true on every visit it can render on | PASS | Half dressed, half not. | fallback only reached when exposure > 0 and no earlier group holds
bathroom_mirror | a solo button is a real act | PASS | Look in the mirror | shows the act it names, one line by what she has on
hall_mirror | want | N/A | — | solo canvas, no person on screen
hall_mirror | next step | N/A | — | solo canvas, no person on screen
hall_mirror | hook | N/A | — | solo canvas, no person on screen
hall_mirror | her voice at her level | N/A | — | solo canvas, no person on screen
hall_mirror | who notices | N/A | — | solo canvas, no person on screen
hall_mirror | the written no | N/A | — | solo canvas, no person on screen
hall_mirror | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
hall_mirror | the numbers and the clothes agree | FAIL | No bra. Your nipples show through your top | group is bra unequipped + exposure 0, also true in a dress-slot item (Laura's blue dress, Zoe's party dress, cafe uniform): no top is worn
hall_mirror | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hall_mirror | true on every visit it can render on | FAIL | Covered, neat, nothing anyone could say a word about. You look like Laura's good girl. | exposure 0 is also Zoe's party dress (corruption 2), the Sheer blouse, the Tight cafe uniform
hall_mirror | a solo button is a real act | PASS | Check your clothes in the hall mirror | shows the act it names, one line by what she has on
kitchen_drawer | want | N/A | — | solo canvas, no person on screen
kitchen_drawer | next step | N/A | — | solo canvas, no person on screen
kitchen_drawer | hook | N/A | — | solo canvas, no person on screen
kitchen_drawer | her voice at her level | N/A | — | solo canvas, no person on screen
kitchen_drawer | who notices | N/A | — | solo canvas, no person on screen
kitchen_drawer | the written no | N/A | — | solo canvas, no person on screen
kitchen_drawer | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
kitchen_drawer | the numbers and the clothes agree | N/A | Three envelopes from Vance | no ledger figure for the count to agree or disagree with
kitchen_drawer | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
kitchen_drawer | true on every visit it can render on | FAIL | And one from the college, with your name on it, opened. Laura's read it. | letter_home is set when the dean says the letter WILL be sent (toml:19757); renders the same afternoon, before any arrival or Laura reading it
kitchen_drawer | a solo button is a real act | PASS | Look through the drawer | shows the act it names; 5 min, kitchen to hall
kitchen_breakfast | want | N/A | — | solo canvas, no person on screen
kitchen_breakfast | next step | N/A | — | solo canvas, no person on screen
kitchen_breakfast | hook | N/A | — | solo canvas, no person on screen
kitchen_breakfast | her voice at her level | N/A | — | solo canvas, no person on screen
kitchen_breakfast | who notices | N/A | — | solo canvas, no person on screen
kitchen_breakfast | the written no | N/A | — | solo canvas, no person on screen
kitchen_breakfast | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
kitchen_breakfast | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
kitchen_breakfast | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
kitchen_breakfast | true on every visit it can render on | FAIL | Nobody's in, but somebody left the radio on. | trigger checks only the kitchen; Sat 08:00 Ryan is in home_ryan_room (who_is_where), Sat 09:00 Mark in the garage
kitchen_breakfast | a solo button is a real act | PASS | Eat. | +10 energy, 15 min, ate_breakfast
kitchen_coffee | want | N/A | — | solo canvas, no person on screen
kitchen_coffee | next step | N/A | — | solo canvas, no person on screen
kitchen_coffee | hook | N/A | — | solo canvas, no person on screen
kitchen_coffee | her voice at her level | N/A | — | solo canvas, no person on screen
kitchen_coffee | who notices | N/A | — | solo canvas, no person on screen
kitchen_coffee | the written no | N/A | — | solo canvas, no person on screen
kitchen_coffee | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
kitchen_coffee | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
kitchen_coffee | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
kitchen_coffee | true on every visit it can render on | FAIL | You drink it at the window and watch the street wake up. | window runs to 11:00; at 10:59 the street woke hours ago
kitchen_coffee | a solo button is a real act | PASS | Drink it. | +5 energy, 10 min, had_coffee
kitchen_dinner | want | N/A | — | solo canvas, no person on screen
kitchen_dinner | next step | N/A | — | solo canvas, no person on screen
kitchen_dinner | hook | N/A | — | solo canvas, no person on screen
kitchen_dinner | her voice at her level | N/A | — | solo canvas, no person on screen
kitchen_dinner | who notices | N/A | — | solo canvas, no person on screen
kitchen_dinner | the written no | N/A | — | solo canvas, no person on screen
kitchen_dinner | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
kitchen_dinner | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
kitchen_dinner | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
kitchen_dinner | true on every visit it can render on | PASS | eaten at the empty table | gated nobody in the kitchen
kitchen_dinner | a solo button is a real act | PASS | Eat. | +15 energy, 30 min, ate_dinner
kitchen_dishes | want | N/A | — | solo canvas, no person on screen
kitchen_dishes | next step | N/A | — | solo canvas, no person on screen
kitchen_dishes | hook | N/A | — | solo canvas, no person on screen
kitchen_dishes | her voice at her level | N/A | — | solo canvas, no person on screen
kitchen_dishes | who notices | N/A | — | solo canvas, no person on screen
kitchen_dishes | the written no | N/A | — | solo canvas, no person on screen
kitchen_dishes | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
kitchen_dishes | the numbers and the clothes agree | PASS | it's done in twenty minutes | button spends 20 min
kitchen_dishes | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
kitchen_dishes | true on every visit it can render on | PASS | The sink's full again. | 'again' on a repeatable is allowed (register.md truth rule)
kitchen_dishes | a solo button is a real act | PASS | Done. | 20 min, energy -5, did_dishes
living_couch | want | PASS | He stands there drinking, looking down the length of you | Mark's want shown; not a sexual step
living_couch | next step | N/A | — | ambient reaction on a repeatable solo button, not a scene with Mark or Ryan
living_couch | hook | N/A | — | ambient reaction on a repeatable solo button
living_couch | her voice at her level | N/A | — | solo canvas, no person on screen
living_couch | who notices | PASS | "Jesus, @player.nickname." | Mark or Ryan reacts to her in underwear
living_couch | the written no | N/A | — | solo canvas, no person on screen
living_couch | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
living_couch | the numbers and the clothes agree | PASS | You're in your underwear. | underwear and skirt lines sit in clothing_slot / worn_type groups
living_couch | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
living_couch | true on every visit it can render on | PASS | Mark comes through from the kitchen with a beer | gated on Mark in the kitchen
living_couch | a solo button is a real act | PASS | Get up. | 10 min, couch to hall; 'Stay a while' +1 exhibitionism
living_tv | want | N/A | — | solo canvas, no person on screen
living_tv | next step | N/A | — | solo canvas, no person on screen
living_tv | hook | N/A | — | solo canvas, no person on screen
living_tv | her voice at her level | N/A | — | solo canvas, no person on screen
living_tv | who notices | N/A | — | solo canvas, no person on screen
living_tv | the written no | N/A | — | solo canvas, no person on screen
living_tv | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
living_tv | the numbers and the clothes agree | PASS | An hour goes by without asking | button spends 60 min
living_tv | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
living_tv | true on every visit it can render on | PASS | A cooking show, then an old film | no hour-bound claim false 07:00-02:00
living_tv | a solo button is a real act | PASS | Watch an hour. | +5 energy, 60 min, watched_tv
living_film | want | N/A | — | solo canvas, no person on screen
living_film | next step | N/A | — | solo canvas, no person on screen
living_film | hook | N/A | — | solo canvas, no person on screen
living_film | her voice at her level | N/A | — | solo canvas, no person on screen
living_film | who notices | N/A | — | solo canvas, no person on screen
living_film | the written no | N/A | — | solo canvas, no person on screen
living_film | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
living_film | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
living_film | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
living_film | true on every visit it can render on | PASS | turn the lights off | 19:00-00:00 only
living_film | a solo button is a real act | PASS | Watch it. | +5 energy, 120 min, movie_night
master_wardrobe | want | N/A | — | solo canvas, no person on screen
master_wardrobe | next step | N/A | — | solo canvas, no person on screen
master_wardrobe | hook | N/A | — | solo canvas, no person on screen
master_wardrobe | her voice at her level | N/A | — | solo canvas, no person on screen
master_wardrobe | who notices | N/A | — | solo canvas, no person on screen
master_wardrobe | the written no | N/A | — | solo canvas, no person on screen
master_wardrobe | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
master_wardrobe | the numbers and the clothes agree | PASS | the blue one | her dress named behind clothing_item laura_blue_dress owned
master_wardrobe | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
master_wardrobe | true on every visit it can render on | FAIL | There's the gap on the rail where the blue one hung. It's in your room now. | condition is clothing_item owned, which also holds while she is wearing the dress
master_wardrobe | a solo button is a real act | PASS | Put it all back. | shows the act it names; 20 min, bedroom to hall
master_asleep | want | N/A | — | both people asleep; door screen
master_asleep | next step | N/A | — | solo canvas, no person on screen
master_asleep | hook | PASS | Go to the bed. (Needs Hungry) | names the next step, shown locked
master_asleep | her voice at her level | N/A | — | solo canvas, no person on screen
master_asleep | who notices | N/A | — | solo canvas, no person on screen
master_asleep | the written no | N/A | — | solo canvas, no person on screen
master_asleep | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
master_asleep | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
master_asleep | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
master_asleep | true on every visit it can render on | PASS | Laura's asleep on her side | door option gated 22:00-07:00 + someone present; every row there is asleep (z)
master_asleep | a solo button is a real act | N/A | — | door screen with people on it, not a solo button
garage_things | want | N/A | — | solo canvas, no person on screen
garage_things | next step | N/A | — | solo canvas, no person on screen
garage_things | hook | N/A | — | solo canvas, no person on screen
garage_things | her voice at her level | N/A | — | solo canvas, no person on screen
garage_things | who notices | N/A | — | solo canvas, no person on screen
garage_things | the written no | N/A | — | solo canvas, no person on screen
garage_things | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
garage_things | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
garage_things | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
garage_things | true on every visit it can render on | PASS | the loan is named only after knows_mark_debt | past lines sit behind rent_carried / knows_mark_debt
garage_things | a solo button is a real act | PASS | Lock it up again. | shows the act it names; 15 min, garage to hall
garage_laundry | want | N/A | — | solo canvas, no person on screen
garage_laundry | next step | N/A | — | solo canvas, no person on screen
garage_laundry | hook | N/A | — | solo canvas, no person on screen
garage_laundry | her voice at her level | N/A | — | solo canvas, no person on screen
garage_laundry | who notices | N/A | — | solo canvas, no person on screen
garage_laundry | the written no | N/A | — | solo canvas, no person on screen
garage_laundry | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
garage_laundry | the numbers and the clothes agree | N/A | — | solo canvas, no person on screen
garage_laundry | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
garage_laundry | true on every visit it can render on | PASS | feed the old machine until it shudders and starts | gated Mark absent, 07:00-21:00
garage_laundry | a solo button is a real act | PASS | Load it. | 30 min, energy -5, did_laundry
garden_sun | want | PASS | once the radio goes quiet you know he's standing in the doorway | Mark's (and Ryan's 'His music stops.') want shown; no sexual step written
garden_sun | next step | N/A | — | placeholder: every further rung (sun_ryan_tease, sun_ryan_touch, sun_mark_tease, sun_mark_paid) is a PLACEHOLDER screen
garden_sun | hook | PASS | Play up to Mark in the garage door. | names the next rung
garden_sun | her voice at her level | PASS | Your skin is hot and it isn't only the sun. | appetite behind exhibitionism gte 20
garden_sun | who notices | PASS | Ryan's window is open above you. His music stops. | Mark and Ryan react when home
garden_sun | the written no | FAIL | Not today. | sun_mark offers 'Let him pay to look.'; the refusal returns to the garden and moves nothing
garden_sun | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
garden_sun | the numbers and the clothes agree | FAIL | In what you have on, sleeves pushed up, face to the sky. | catch-all group (exposure gte 0) also renders in the towel and the dresses: sleeves unbacked; also Ryan's rungs gate ryan_step gte 3 / gte 7 against the ledger's 'Ryan A 4' / 'Ryan A 8' (ryan_04 sets 4, ryan_08 sets 8), where Mark's use gte 3 / gte 7 for 'Mark A 3' / 'A 7'
garden_sun | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
garden_sun | true on every visit it can render on | FAIL | You drag the lounger into the one patch of sun | garden is open to 21:00 (closed_text 'It's dark out.'), no time gate on the canvas: false at 20:59
garden_sun | a solo button is a real act | PASS | Lie in the sun an hour. | +5 energy, 60 min, sunned
garden_washing | want | N/A | — | solo canvas, no person on screen
garden_washing | next step | N/A | — | solo canvas, no person on screen
garden_washing | hook | N/A | — | solo canvas, no person on screen
garden_washing | her voice at her level | N/A | — | solo canvas, no person on screen
garden_washing | who notices | N/A | — | solo canvas, no person on screen
garden_washing | the written no | N/A | — | solo canvas, no person on screen
garden_washing | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
garden_washing | the numbers and the clothes agree | N/A | jeans, towels, and your smalls | washing on the line, not what she wears
garden_washing | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
garden_washing | true on every visit it can render on | FAIL | but nobody's watching | no presence gate; Sat 09:00-17:00 Mark is in home_garage, whose door opens onto the garden
garden_washing | a solo button is a real act | PASS | Done. | 15 min, hung_washing
front_step | want | PASS | A guy walking his dog looks over, and keeps looking. | one-off strangers; want shown on the same canvas
front_step | next step | N/A | — | strangers and an ambient Vance line on a repeatable solo button
front_step | hook | N/A | — | repeatable solo button
front_step | her voice at her level | PASS | You could put your knees down. You don't, for a while. | only renders in the short skirt, itself gated on exhibitionism
front_step | who notices | PASS | Next door, Vance lowers his paper on the porch and watches you | reaction present
front_step | the written no | N/A | — | solo canvas, no person on screen
front_step | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
front_step | the numbers and the clothes agree | PASS | anyone passing can see your panties | skirt and panties lines behind worn_type + clothing_slot
front_step | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
front_step | true on every visit it can render on | PASS | The street is dark and quiet, the porch light on its timer. | day and night text split on time_of_day; Vance gated on vance_house 18-22
front_step | a solo button is a real act | PASS | Go back in. | shows the act it names; 20 min, step to hall
home_event_ryan_towel | want | FAIL | "Sorry." | Ryan only apologises; nothing he wants shows on the screen (checked: event + its two placeholder nodes)
home_event_ryan_towel | next step | N/A | — | placeholder: the further rung (ev_curious / ev_bold) is a PLACEHOLDER screen
home_event_ryan_towel | hook | PASS | Walk past slowly. | a choice names the next rung for a player at Curious
home_event_ryan_towel | her voice at her level | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_towel | who notices | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_towel | the written no | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_towel | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
home_event_ryan_towel | the numbers and the clothes agree | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_towel | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
home_event_ryan_towel | true on every visit it can render on | PASS | Ryan steps out in a towel | Mon-Fri 06:45-07:30 matches his bathroom row
home_event_ryan_towel | a solo button is a real act | N/A | — | random event with a person on it, no solo button
home_event_laura_robe | want | PASS | Don't look at me like that. It's early. | Laura wants not to be looked at
home_event_laura_robe | next step | N/A | — | placeholder: the further rung (ev_curious / ev_bold) is a PLACEHOLDER screen
home_event_laura_robe | hook | PASS | Don't look away. | a choice names the next rung for a player at Curious
home_event_laura_robe | her voice at her level | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_laura_robe | who notices | PASS | She ties it again fast, pink to the ears. | Laura reacts to Ella's look
home_event_laura_robe | the written no | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_laura_robe | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
home_event_laura_robe | the numbers and the clothes agree | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_laura_robe | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
home_event_laura_robe | true on every visit it can render on | PASS | It's early. | Mon-Fri 06:30-08:00, gated on Laura in the kitchen
home_event_laura_robe | a solo button is a real act | N/A | — | random event with a person on it, no solo button
home_event_mark_reach | want | PASS | his chest at your back for a second longer than the mug needs | Mark's want shown
home_event_mark_reach | next step | N/A | — | placeholder: the further rung (ev_curious / ev_bold) is a PLACEHOLDER screen
home_event_mark_reach | hook | PASS | Lean back into him. | a choice names the next rung for a player at Curious
home_event_mark_reach | her voice at her level | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_reach | who notices | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_reach | the written no | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_reach | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
home_event_mark_reach | the numbers and the clothes agree | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_reach | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
home_event_mark_reach | true on every visit it can render on | PASS | Mark reaches over you | Sun 08:00-22:00, Mark's Sunday-table row
home_event_mark_reach | a solo button is a real act | N/A | — | random event with a person on it, no solo button
home_event_mark_asleep | want | FAIL | Mark has fallen asleep on the couch | asleep, Mark shows no want
home_event_mark_asleep | next step | N/A | — | placeholder: the further rung (ev_curious / ev_bold) is a PLACEHOLDER screen
home_event_mark_asleep | hook | PASS | Take the beer out of his hand. | a choice names the next rung for a player at Curious
home_event_mark_asleep | her voice at her level | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_asleep | who notices | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_asleep | the written no | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_asleep | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
home_event_mark_asleep | the numbers and the clothes agree | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_mark_asleep | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
home_event_mark_asleep | true on every visit it can render on | FAIL | Mark has fallen asleep on the couch with the TV still on | who_is_where: Mon-Sat 00:00-02:00 his living-room row is 'up late with the TV on', not asleep (no z)
home_event_mark_asleep | a solo button is a real act | N/A | — | random event with a person on it, no solo button
home_event_ryan_door | want | PASS | Ryan's door is open a hand's width. Light under it, music low. | the open door behind ryan_step gte 7 is his invitation
home_event_ryan_door | next step | N/A | — | placeholder: the further rung (ev_curious / ev_bold) is a PLACEHOLDER screen
home_event_ryan_door | hook | PASS | Stop and look in. | a choice names the next rung for a player at Curious
home_event_ryan_door | her voice at her level | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_door | who notices | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_door | the written no | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_door | the body | N/A | — | no block reaches 3 frozen-list words (gates.py --beat on every block)
home_event_ryan_door | the numbers and the clothes agree | N/A | — | no thought, no act of hers to notice, no offer, no number or garment of hers
home_event_ryan_door | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
home_event_ryan_door | true on every visit it can render on | PASS | Light under it, music low. | 22:00-00:00, Ryan's room row every day
home_event_ryan_door | a solo button is a real act | N/A | — | random event with a person on it, no solo button
home_event_quiet_hall | want | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | next step | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | hook | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | her voice at her level | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | who notices | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | the written no | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | the body | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | the numbers and the clothes agree | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | companion and rival | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_hall | true on every visit it can render on | PASS | Nothing happens. | gated nobody in the room; no time or person claim
home_event_quiet_hall | a solo button is a real act | N/A | — | random event, not a button she chose
home_event_quiet_kitchen | want | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | next step | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | hook | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | her voice at her level | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | who notices | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | the written no | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | the body | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | the numbers and the clothes agree | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | companion and rival | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_kitchen | true on every visit it can render on | PASS | Nothing happens. | gated nobody in the room; no time or person claim
home_event_quiet_kitchen | a solo button is a real act | N/A | — | random event, not a button she chose
home_event_quiet_living_room | want | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | next step | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | hook | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | her voice at her level | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | who notices | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | the written no | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | the body | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | the numbers and the clothes agree | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | companion and rival | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_living_room | true on every visit it can render on | PASS | Nothing happens. | gated nobody in the room; no time or person claim
home_event_quiet_living_room | a solo button is a real act | N/A | — | random event, not a button she chose
home_event_quiet_bathroom | want | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | next step | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | hook | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | her voice at her level | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | who notices | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | the written no | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | the body | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | the numbers and the clothes agree | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | companion and rival | N/A | — | random quiet event, no person, nothing to notice
home_event_quiet_bathroom | true on every visit it can render on | PASS | Nothing happens. | gated nobody in the room; no time or person claim
home_event_quiet_bathroom | a solo button is a real act | N/A | — | random event, not a button she chose

## FAILs by test

### want
- home_event_ryan_towel: ""Sorry."" — Ryan only apologises; nothing he wants shows on the screen (checked: event + its two placeholder nodes)
- home_event_mark_asleep: "Mark has fallen asleep on the couch" — asleep, Mark shows no want
### her voice at her level
- bathroom_shower: "Nobody can see, but you take your time like someone could." — exhibitionist appetite in a pool line with no meter gate; renders at exhibitionism 0
### the written no
- garden_sun: "Not today." — sun_mark offers 'Let him pay to look.'; the refusal returns to the garden and moves nothing
### the numbers and the clothes agree
- hall_mirror: "No bra. Your nipples show through your top" — group is bra unequipped + exposure 0, also true in a dress-slot item (Laura's blue dress, Zoe's party dress, cafe uniform): no top is worn
- garden_sun: "In what you have on, sleeves pushed up, face to the sky." — catch-all group (exposure gte 0) also renders in the towel and the dresses: sleeves unbacked; also Ryan's rungs gate ryan_step gte 3 / gte 7 against the ledger's 'Ryan A 4' / 'Ryan A 8' (ryan_04 sets 4, ryan_08 sets 8), where Mark's use gte 3 / gte 7 for 'Mark A 3' / 'A 7'
### true on every visit it can render on
- hall_mirror: "Covered, neat, nothing anyone could say a word about. You look like Laura's good girl." — exposure 0 is also Zoe's party dress (corruption 2), the Sheer blouse, the Tight cafe uniform
- kitchen_drawer: "And one from the college, with your name on it, opened. Laura's read it." — letter_home is set when the dean says the letter WILL be sent (toml:19757); renders the same afternoon, before any arrival or Laura reading it
- kitchen_breakfast: "Nobody's in, but somebody left the radio on." — trigger checks only the kitchen; Sat 08:00 Ryan is in home_ryan_room (who_is_where), Sat 09:00 Mark in the garage
- kitchen_coffee: "You drink it at the window and watch the street wake up." — window runs to 11:00; at 10:59 the street woke hours ago
- master_wardrobe: "There's the gap on the rail where the blue one hung. It's in your room now." — condition is clothing_item owned, which also holds while she is wearing the dress
- garden_sun: "You drag the lounger into the one patch of sun" — garden is open to 21:00 (closed_text 'It's dark out.'), no time gate on the canvas: false at 20:59
- garden_washing: "but nobody's watching" — no presence gate; Sat 09:00-17:00 Mark is in home_garage, whose door opens onto the garden
- home_event_mark_asleep: "Mark has fallen asleep on the couch with the TV still on" — who_is_where: Mon-Sat 00:00-02:00 his living-room row is 'up late with the TV on', not asleep (no z)

```json
{
 "room_sleep": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "room_nap": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "room_study": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "room_makeup": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "room_tidy": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "bathroom_shower": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "FAIL",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "bathroom_mirror": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "hall_mirror": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "kitchen_drawer": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "kitchen_breakfast": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "kitchen_coffee": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "kitchen_dinner": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "kitchen_dishes": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "living_couch": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "living_tv": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "living_film": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "master_wardrobe": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "master_asleep": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "garage_things": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "garage_laundry": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "garden_sun": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "FAIL",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "garden_washing": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "PASS"
 },
 "front_step": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "home_event_ryan_towel": {
  "want": "FAIL",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_laura_robe": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_mark_reach": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_mark_asleep": {
  "want": "FAIL",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "home_event_ryan_door": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_quiet_hall": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_quiet_kitchen": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_quiet_living_room": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "home_event_quiet_bathroom": {
  "want": "N/A",
  "next step": "N/A",
  "hook": "N/A",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 }
}
```
