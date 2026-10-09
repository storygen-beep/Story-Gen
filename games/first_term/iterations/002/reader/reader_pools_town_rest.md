scene | test | PASS / FAIL / N/A | the line judged (quoted, short) | why (one line)
---|---|---|---|---
door_dean_notice | want | N/A |  | no person; a notice
door_dean_notice | next step | N/A |  | no person
door_dean_notice | hook | PASS | Your name isn't on it. Not yet. | names the list she is heading for
door_dean_notice | her voice at her level | N/A |  | 
door_dean_notice | who notices | PASS | Somebody has been talking about what you wear to class. | the complaints are the reaction
door_dean_notice | the written no | N/A |  | 
door_dean_notice | the body | N/A |  | 
door_dean_notice | the numbers and the clothes agree | N/A |  | no number, no garment named
door_dean_notice | companion and rival | N/A |  | want.companion_is_rival not set
door_dean_notice | true on every visit it can render on | PASS | Yours is on it. PROBATION | each line behind on_probation/complaints; office Mon-Fri 09-17
door_dean_notice | a solo button is a real act | FAIL | "Step back." | only describes; exit lands at dean_office where she stood, no time, no effect (description: 'Writes nothing')
party_arrive | want | PASS | Babe! Get in here. | Zoe wants her in
party_arrive | next step | N/A |  | repeatable door, no step
party_arrive | hook | PASS | Get in here. Now we're talking. | points into the party
party_arrive | her voice at her level | N/A | Laura said no. Not this Friday. | no meter-level thought
party_arrive | who notices | PASS | Not in that. Borrow mine. | Zoe reacts to the outfit
party_arrive | the written no | N/A |  | no offer; the door itself
party_arrive | the body | N/A |  | 
party_arrive | the numbers and the clothes agree | PASS | Go in. (15 energy) | costs 15; cooldown 'Friday nights, from seven' = schedule Fri 19:00
party_arrive | companion and rival | N/A |  | want.companion_is_rival not set
party_arrive | true on every visit it can render on | PASS | You can hear it from the stairwell | true Fri 19:00-23:59; Zoe present 18-24
party_arrive | a solo button is a real act | PASS | Go in. (15 energy) | energy, party_went, drinks_tonight
party_chat | want | PASS | You're a hit, babe. Everyone's asking about you. | Zoe pushes her into the room
party_chat | next step | N/A |  | repeatable, no person step
party_chat | hook | N/A |  | repeatable ambient, no arc to point at
party_chat | her voice at her level | N/A |  | 
party_chat | who notices | PASS | A guy you've never met tells you you're famous | the room reacts
party_chat | the written no | N/A |  | 
party_chat | the body | N/A |  | 
party_chat | the numbers and the clothes agree | N/A |  | counts are in-scene only; no garment
party_chat | companion and rival | N/A |  | want.companion_is_rival not set
party_chat | true on every visit it can render on | PASS | Jake's teammate, the cocky one from Figure drawing | behind npc presence; his rows are gated on cocky_guy_met
party_chat | a solo button is a real act | PASS | Keep going. | campus_talk +1, 40 min
party_drink_offer | want | PASS | A guy from the team pours you something ... and winks. | someone wants her drinking
party_drink_offer | next step | N/A |  | repeatable, no person step
party_drink_offer | hook | N/A |  | repeatable ambient
party_drink_offer | her voice at her level | N/A | That'd be three. You'll feel it tomorrow. | no meter in play
party_drink_offer | who notices | PASS | They look disappointed, but nobody pushes. | the refusal is seen
party_drink_offer | the written no | FAIL | "I'm good, thanks." / They shrug and drink it themselves. | written, but moves nothing: no flag, no meter, 2 min, back to the same room
party_drink_offer | the body | N/A |  | 
party_drink_offer | the numbers and the clothes agree | PASS | Drink it. (your third) | shows at drinks_tonight == 2; heavy_night read next morning
party_drink_offer | companion and rival | N/A |  | want.companion_is_rival not set
party_drink_offer | true on every visit it can render on | PASS | Zoe appears with two shots | Zoe present Fri 18-24, Sat 00-02
party_drink_offer | a solo button is a real act | PASS | Drink it. | drinks_tonight +1, Tipsy modifier
party_dare | want | PASS | Flash them, babe. Three seconds. | checked earlier: zoe_01_first_party ('Put it on. No, here. I want to see.'), zoe_02_bra_through_the_sleeve (looks at the strap and nowhere else)
party_dare | next step | PASS | bare to people you sit next to in class | public flash for the circle, past zoe_02's balcony dare
party_dare | hook | PASS | Boo. Fine. Next one's yours. | promises the next dare; 'You pick now' behind picks_the_dares
party_dare | her voice at her level | N/A |  | no thought
party_dare | who notices | PASS | Somebody whistles. A guy on the couch forgets the drink | circle reacts
party_dare | the written no | PASS | "Not tonight, Zo." | written; sets party_cool_zoe
party_dare | the body | PASS | before you let everything drop. | ends on the act; 4 frozen words
party_dare | the numbers and the clothes agree | N/A |  | no garment named ('pull everything up'); count is in-scene
party_dare | companion and rival | N/A |  | want.companion_is_rival not set
party_dare | true on every visit it can render on | PASS | Zoe pulls you down into the circle | Zoe present Fri 23-24 / Sat 00-02, requires_npc
party_dare | a solo button is a real act | N/A |  | person-bound
party_hookup | want | PASS | He's been watching you all night. ... Bathroom's free. | one-off (ledger: 'keeps: none'); same canvas shows his want before the act; also college_class_figure 'looks you over, slow, and grins'
party_hookup | next step | PASS | Get on your knees. / Pull him in. | sex, past hub_cocky_party's talk
party_hookup | hook | PASS | By Monday half of campus will know. | names what follows
party_hookup | her voice at her level | PASS | You find you don't mind. | appetite at corruption 40+
party_hookup | who notices | PASS | In my bathroom? Babe. | Zoe reacts (her presence line is already on the scoreboard)
party_hookup | the written no | PASS | "Not tonight." / Your loss. | written; sets party_cool_cocky_guy
party_hookup | the body | PASS | your heels digging into his ass. | oral ends 'wipe your lip with your thumb'; both on the body
party_hookup | the numbers and the clothes agree | N/A |  | only his jeans named; no number
party_hookup | companion and rival | N/A |  | want.companion_is_rival not set
party_hookup | true on every visit it can render on | FAIL | He's been watching you all night. | false at Fri 23:00: his only rows start 23:00, he has just arrived
party_hookup | a solo button is a real act | N/A |  | person-bound
party_hookup | true on every visit it can render on | FAIL | You still owe me for that exam. Or I owe you. | gated on exam_psych_done, but college_exam_psych has no cocky guy and no deal (Focus only); the past it names never happened
park_walk | want | PASS | The skirt is a problem in this wind. You let it be a problem. | her want shows
park_walk | next step | N/A |  | no person
park_walk | hook | PASS | Let strangers see. (Needs Hungry) | the locked act is named
park_walk | her voice at her level | PASS | You let it be a problem. | appetite; the skirt outside needs Daring
park_walk | who notices | PASS | A jogger turns his head to watch you | men look
park_walk | the written no | N/A |  | 
park_walk | the body | N/A |  | 
park_walk | the numbers and the clothes agree | PASS | The skirt is a problem | skirt behind worn_type short_skirt; no bra behind clothing_slot
park_walk | companion and rival | N/A |  | want.companion_is_rival not set
park_walk | true on every visit it can render on | FAIL | The wind ... goes straight up whatever you're wearing. A jogger turns his head to watch you hold it down | pool line not gated on a skirt; false in jeans or leggings, which the park allows
park_walk | a solo button is a real act | PASS | Finish the loop. | 30 min
park_run | want | PASS | Your face is red and not only from running. | her want
park_run | next step | N/A |  | no person
park_run | hook | N/A |  | person-less repeatable
park_run | her voice at her level | N/A |  | no thought
park_run | who notices | PASS | A cyclist wobbles. | onlookers react
park_run | the written no | N/A |  | 
park_run | the body | N/A |  | 
park_run | the numbers and the clothes agree | PASS | Cool down. (10 energy) | costs 10; leggings/top/sports bra each behind a clothing check
park_run | companion and rival | N/A |  | want.companion_is_rival not set
park_run | true on every visit it can render on | PASS | You run the loop twice | true at any park hour 07-22
park_run | a solo button is a real act | PASS | Cool down. (10 energy) | energy, hour, Exhibitionism
park_rest | want | N/A |  | utility rest
park_rest | next step | N/A |  | no person
park_rest | hook | N/A |  | utility rest
park_rest | her voice at her level | N/A |  | 
park_rest | who notices | N/A |  | nothing to notice
park_rest | the written no | N/A |  | 
park_rest | the body | N/A |  | 
park_rest | the numbers and the clothes agree | N/A |  | 
park_rest | companion and rival | N/A |  | want.companion_is_rival not set
park_rest | true on every visit it can render on | FAIL | your face tipped up to the sun | park open to 22:00, no time gate; no sun at 21:00-21:59
park_rest | a solo button is a real act | PASS | Get up. | energy +5, 30 min
park_selfie | want | N/A |  | no person
park_selfie | next step | N/A |  | no person
park_selfie | hook | N/A |  | person-less repeatable
park_selfie | her voice at her level | N/A |  | 
park_selfie | who notices | PASS | A man on a bench watches you do it, every angle. | seen
park_selfie | the written no | N/A |  | 
park_selfie | the body | N/A |  | 
park_selfie | the numbers and the clothes agree | PASS | the wind has the skirt | skirt and sports bra each behind a clothing check
park_selfie | companion and rival | N/A |  | want.companion_is_rival not set
park_selfie | true on every visit it can render on | FAIL | You post that one. / The likes start | narrated as posted before the choice; false on 'Delete them all.' (also 'the good light' at 21:45, park open to 22:00)
park_selfie | a solo button is a real act | PASS | Post it. | followers +2, Exhibitionism +1
park_watch_the_couple | want | PASS | You could leave. You don't want to. | strangers, one-off; her want and theirs shown before the act
park_watch_the_couple | next step | N/A |  | strangers, no ladder
park_watch_the_couple | hook | N/A |  | person-less repeatable
park_watch_the_couple | her voice at her level | PASS | You know exactly what that is. | appetite gated corruption 20+; below it she walks into them and runs
park_watch_the_couple | who notices | PASS | Then he looks up, straight at you | seen on the run path; 'Neither of them looks toward the bush' declared on touch
park_watch_the_couple | the written no | N/A |  | 
park_watch_the_couple | the body | PASS | your fingers keep working your clit through it. | all three beats end on the body (7/11/9 frozen words)
park_watch_the_couple | the numbers and the clothes agree | N/A |  | 
park_watch_the_couple | companion and rival | N/A |  | want.companion_is_rival not set
park_watch_the_couple | true on every visit it can render on | PASS | Behind you on the path a jogger thuds past. | park 07-22; no named person
park_watch_the_couple | a solo button is a real act | PASS | Touch yourself while you watch. | shows the act; corruption, saw_the_couple
park_hidden | want | PASS | Come here. I know a place. | checked earlier: zoe_03_hot_tub ('I want to see your tits'), zoe_02_bra_through_the_sleeve
park_hidden | next step | PASS | Her hand slides down inside ... and finds you wet. | her hand, past zoe_03's kiss
park_hidden | hook | PASS | Same time next weekend. Don't be late. | names the next one
park_hidden | her voice at her level | N/A |  | no thought
park_hidden | who notices | PASS | A man walking his dog slows ... looks your way | seen
park_hidden | the written no | PASS | "Not here, Zo." | written; sets park_cool_zoe
park_hidden | the body | PASS | her mouth on yours to swallow every moan. | on the body; 5 frozen words
park_hidden | the numbers and the clothes agree | N/A |  | no garment of hers named
park_hidden | companion and rival | N/A |  | want.companion_is_rival not set
park_hidden | true on every visit it can render on | FAIL | both of you still panting from the run | no run is required: a sibling link to hub_zoe_park's 'Run a lap with her'; false when she walks in from the street at Sat 08:00
park_hidden | a solo button is a real act | N/A |  | person-bound
touch_bed | want | N/A |  | solo, no other person
touch_bed | next step | N/A |  | no person
touch_bed | hook | N/A |  | solo repeatable
touch_bed | her voice at her level | PASS | you want to know how much more you can take | appetite at corruption 20+
touch_bed | who notices | N/A |  | private act
touch_bed | the written no | N/A |  | 
touch_bed | the body | PASS | fingers still pressed to your clit. | on the body; 6 frozen words
touch_bed | the numbers and the clothes agree | N/A |  | no garment of hers
touch_bed | companion and rival | N/A |  | want.companion_is_rival not set
touch_bed | true on every visit it can render on | PASS | The walls are thin | the TV line is already on the scoreboard; left alone
touch_bed | a solo button is a real act | PASS | Lie still. | shows the act; corruption +1
touch_shower | want | N/A |  | solo
touch_shower | next step | N/A |  | no person
touch_shower | hook | N/A |  | solo repeatable
touch_shower | her voice at her level | N/A |  | no thought
touch_shower | who notices | N/A |  | private act
touch_shower | the written no | N/A |  | 
touch_shower | the body | PASS | while your clit throbs under your hand. | on the body; 8 frozen words
touch_shower | the numbers and the clothes agree | PASS | step naked under the hot water | undressing inside the act
touch_shower | companion and rival | N/A |  | want.companion_is_rival not set
touch_shower | true on every visit it can render on | FAIL | Footsteps cross the hall outside and keep going. | false Mon 10:00 (Ryan, Laura, Mark all out 08-18) and at 03:00 (all in bed)
touch_shower | a solo button is a real act | PASS | Done. | shows the act; corruption +1
touch_toilet | want | N/A |  | solo
touch_toilet | next step | N/A |  | no person
touch_toilet | hook | N/A |  | solo repeatable
touch_toilet | her voice at her level | N/A |  | no thought
touch_toilet | who notices | N/A | Nobody knocks. | declared; private
touch_toilet | the written no | N/A |  | 
touch_toilet | the body | PASS | your thighs clamp shut on your hand. | on the body; 5 frozen words
touch_toilet | the numbers and the clothes agree | N/A |  | no garment
touch_toilet | companion and rival | N/A |  | want.companion_is_rival not set
touch_toilet | true on every visit it can render on | PASS | A girl laughs at the mirror. | strangers, toilet open 07-22
touch_toilet | a solo button is a real act | PASS | Done. | shows the act; corruption +1
wardrobe_event_stairs | want | PASS | straight up your skirt, and doesn't look away | Mark's want, when present
wardrobe_event_stairs | next step | N/A |  | person-less event
wardrobe_event_stairs | hook | N/A |  | person-less event
wardrobe_event_stairs | her voice at her level | PASS | you climb slower | appetite at Exhibitionism 20+
wardrobe_event_stairs | who notices | FAIL | You go up the stairs slowly, one hand on the rail. | with nobody home (Mon 10:00) this is the whole screen and Exhibitionism still +1; nobody reacts, none declared
wardrobe_event_stairs | the written no | N/A |  | 
wardrobe_event_stairs | the body | N/A |  | 
wardrobe_event_stairs | the numbers and the clothes agree | PASS | There's nothing under the skirt. | skirt behind the trigger, bare behind clothing_slot underwear
wardrobe_event_stairs | companion and rival | N/A |  | want.companion_is_rival not set
wardrobe_event_stairs | true on every visit it can render on | PASS | Mark comes out of the living room | each person behind npc_at_location
wardrobe_event_stairs | a solo button is a real act | PASS | Keep climbing. | Exhibitionism +1
town_event_wind | want | N/A |  | stranger event
town_event_wind | next step | N/A |  | no person
town_event_wind | hook | N/A |  | random event
town_event_wind | her voice at her level | N/A |  | 
town_event_wind | who notices | PASS | the man across the road walks into a bin | seen on the bold path
town_event_wind | the written no | N/A |  | 
town_event_wind | the body | N/A |  | 
town_event_wind | the numbers and the clothes agree | PASS | gets right under your skirt | short_skirt on the trigger
town_event_wind | companion and rival | N/A |  | want.companion_is_rival not set
town_event_wind | true on every visit it can render on | PASS | A gust comes down the street | 07-22
town_event_wind | a solo button is a real act | N/A |  | random event, no button
town_event_whistle | want | N/A |  | stranger event
town_event_whistle | next step | N/A |  | no person
town_event_whistle | hook | N/A |  | random event
town_event_whistle | her voice at her level | N/A |  | 
town_event_whistle | who notices | PASS | whistles, long, at your chest | seen
town_event_whistle | the written no | N/A |  | 
town_event_whistle | the body | N/A |  | 
town_event_whistle | the numbers and the clothes agree | N/A |  | no garment named; bra unequipped on trigger
town_event_whistle | companion and rival | N/A |  | want.companion_is_rival not set
town_event_whistle | true on every visit it can render on | PASS | A car slows down beside you. | 07-22
town_event_whistle | a solo button is a real act | N/A |  | random event, no button
town_event_vance | want | PASS | He watches you all the way past his gate. | Vance's want
town_event_vance | next step | N/A |  | repeatable ambient, not a step
town_event_vance | hook | N/A |  | random event
town_event_vance | her voice at her level | N/A |  | 
town_event_vance | who notices | PASS | He lowers it | seen
town_event_vance | the written no | N/A |  | 
town_event_vance | the body | N/A |  | 
town_event_vance | the numbers and the clothes agree | N/A |  | 
town_event_vance | companion and rival | N/A |  | want.companion_is_rival not set
town_event_vance | true on every visit it can render on | FAIL | He lowers it when you come out. | street is a thoroughfare reached from park, shop, campus, town; false when she arrives from campus at 19:00 and has not come out of the house
town_event_vance | a solo button is a real act | N/A |  | random event, no button
town_event_jogger | want | N/A |  | stranger event
town_event_jogger | next step | N/A |  | no person
town_event_jogger | hook | N/A |  | random event
town_event_jogger | her voice at her level | N/A |  | 
town_event_jogger | who notices | PASS | looks back over his shoulder at you, twice | seen
town_event_jogger | the written no | N/A |  | 
town_event_jogger | the body | N/A |  | 
town_event_jogger | the numbers and the clothes agree | N/A |  | 
town_event_jogger | companion and rival | N/A |  | want.companion_is_rival not set
town_event_jogger | true on every visit it can render on | PASS | A jogger goes past | 07-10
town_event_jogger | a solo button is a real act | N/A |  | random event, no button
town_event_quiet | want | N/A |  | nothing happens by design
town_event_quiet | next step | N/A |  | 
town_event_quiet | hook | N/A |  | 
town_event_quiet | her voice at her level | N/A |  | 
town_event_quiet | who notices | N/A |  | nothing to notice
town_event_quiet | the written no | N/A |  | 
town_event_quiet | the body | N/A |  | 
town_event_quiet | the numbers and the clothes agree | N/A |  | 
town_event_quiet | companion and rival | N/A |  | want.companion_is_rival not set
town_event_quiet | true on every visit it can render on | PASS | A dog barks two gardens down. | true at any hour
town_event_quiet | a solo button is a real act | N/A |  | random event, no button
corner_shop_list | want | N/A |  | errand
corner_shop_list | next step | N/A |  | no person
corner_shop_list | hook | N/A |  | errand
corner_shop_list | her voice at her level | N/A |  | 
corner_shop_list | who notices | N/A | without looking up from his phone | nobody notices, said outright
corner_shop_list | the written no | N/A |  | 
corner_shop_list | the body | N/A |  | 
corner_shop_list | the numbers and the clothes agree | PASS | Pay with Laura's twenty ($20). | costs 20; hub_laura_kitchen's ask adds money +20
corner_shop_list | companion and rival | N/A |  | want.companion_is_rival not set
corner_shop_list | true on every visit it can render on | PASS | Bread, milk, eggs, the wine Laura likes | shop 07-22
corner_shop_list | a solo button is a real act | PASS | Pay with Laura's twenty ($20). | money -20, groceries_bought, 15 min, to the street
hub_cocky_party | want | PASS | There she is. Sit with me. I don't bite. Much. | his want
hub_cocky_party | next step | FAIL | Talk with him a while. | 20 minutes back to the same room; no flag, no meter, nothing further than the last scene
hub_cocky_party | hook | PASS | I don't bite. Much. | points at what he wants, by the bathroom
hub_cocky_party | her voice at her level | N/A |  | no thought
hub_cocky_party | who notices | N/A |  | nothing she does
hub_cocky_party | the written no | FAIL | Walk past him. | the no is a bare link to zoe_kitchen; no written refusal
hub_cocky_party | the body | N/A |  | 
hub_cocky_party | the numbers and the clothes agree | N/A |  | no number, no garment
hub_cocky_party | companion and rival | N/A |  | want.companion_is_rival not set
hub_cocky_party | true on every visit it can render on | PASS | The cocky guy from figure drawing | behind cocky_guy_met; present Fri 23 - Sat 02
hub_cocky_party | a solo button is a real act | N/A |  | person-bound

```json
{"door_dean_notice": {"want": "N/A", "next step": "N/A", "hook": "PASS", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "FAIL"}, "party_arrive": {"want": "PASS", "next step": "N/A", "hook": "PASS", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "party_chat": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "party_drink_offer": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "FAIL", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "party_dare": {"want": "PASS", "next step": "PASS", "hook": "PASS", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "PASS", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}, "party_hookup": {"want": "PASS", "next step": "PASS", "hook": "PASS", "her voice at her level": "PASS", "who notices": "PASS", "the written no": "PASS", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "N/A"}, "park_walk": {"want": "PASS", "next step": "N/A", "hook": "PASS", "her voice at her level": "PASS", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "PASS"}, "park_run": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "park_rest": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "PASS"}, "park_selfie": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "PASS"}, "park_watch_the_couple": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "PASS", "who notices": "PASS", "the written no": "N/A", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "park_hidden": {"want": "PASS", "next step": "PASS", "hook": "PASS", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "PASS", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "N/A"}, "touch_bed": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "PASS", "who notices": "N/A", "the written no": "N/A", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "touch_shower": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "N/A", "the body": "PASS", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "PASS"}, "touch_toilet": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "N/A", "the body": "PASS", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "wardrobe_event_stairs": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "PASS", "who notices": "FAIL", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "town_event_wind": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}, "town_event_whistle": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}, "town_event_vance": {"want": "PASS", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "FAIL", "a solo button is a real act": "N/A"}, "town_event_jogger": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "PASS", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}, "town_event_quiet": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}, "corner_shop_list": {"want": "N/A", "next step": "N/A", "hook": "N/A", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "N/A", "the body": "N/A", "the numbers and the clothes agree": "PASS", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "PASS"}, "hub_cocky_party": {"want": "PASS", "next step": "FAIL", "hook": "PASS", "her voice at her level": "N/A", "who notices": "N/A", "the written no": "FAIL", "the body": "N/A", "the numbers and the clothes agree": "N/A", "companion and rival": "N/A", "true on every visit it can render on": "PASS", "a solo button is a real act": "N/A"}}
```

## FAILs by test

**next step**
- hub_cocky_party: "Talk with him a while." — 20 minutes back to the same room; no flag, no meter, nothing further than the last scene

**who notices**
- wardrobe_event_stairs: "You go up the stairs slowly, one hand on the rail." — with nobody home (Mon 10:00) this is the whole screen and Exhibitionism still +1; nobody reacts, none declared

**the written no**
- party_drink_offer: ""I'm good, thanks." / They shrug and drink it themselves." — written, but moves nothing: no flag, no meter, 2 min, back to the same room
- hub_cocky_party: "Walk past him." — the no is a bare link to zoe_kitchen; no written refusal

**true on every visit it can render on**
- party_hookup: "He's been watching you all night." — false at Fri 23:00: his only rows start 23:00, he has just arrived
- party_hookup: "You still owe me for that exam. Or I owe you." — gated on exam_psych_done, but college_exam_psych has no cocky guy and no deal (Focus only); the past it names never happened
- park_walk: "The wind ... goes straight up whatever you're wearing. A jogger turns his head to watch you hold it down" — pool line not gated on a skirt; false in jeans or leggings, which the park allows
- park_rest: "your face tipped up to the sun" — park open to 22:00, no time gate; no sun at 21:00-21:59
- park_selfie: "You post that one. / The likes start" — narrated as posted before the choice; false on 'Delete them all.' (also 'the good light' at 21:45, park open to 22:00)
- park_hidden: "both of you still panting from the run" — no run is required: a sibling link to hub_zoe_park's 'Run a lap with her'; false when she walks in from the street at Sat 08:00
- touch_shower: "Footsteps cross the hall outside and keep going." — false Mon 10:00 (Ryan, Laura, Mark all out 08-18) and at 03:00 (all in bed)
- town_event_vance: "He lowers it when you come out." — street is a thoroughfare reached from park, shop, campus, town; false when she arrives from campus at 19:00 and has not come out of the house

**a solo button is a real act**
- door_dean_notice: ""Step back."" — only describes; exit lands at dean_office where she stood, no time, no effect (description: 'Writes nothing')
