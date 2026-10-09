scene | test | PASS / FAIL / N/A | the line judged (quoted, short) | why (one line)
---|---|---|---|---
vance_meeting | want | PASS | His eyes go down you and come back up without hurrying. | his want is on screen
vance_meeting | next step | PASS | You'll be Mark's girl. The student. | first meeting; nothing before it
vance_meeting | hook | FAIL | You tell your stepfather I said good evening. | no line names the porch, the rent or a next visit
vance_meeting | her voice at her level | N/A | — | no thought, no meter
vance_meeting | who notices | PASS | He tells me you're paying your way now. | he knows and says it
vance_meeting | the written no | N/A | — | no offer
vance_meeting | the body | N/A | — | not explicit
vance_meeting | the numbers and the clothes agree | N/A | — | no number, no garment
vance_meeting | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
vance_meeting | true on every visit it can render on | FAIL | Next door, on his porch, the man who owns your house: Mr. Vance. | fires with vance_met false; Vance's vance_house row is `when vance_met`, so he is nowhere then, and Mon 18:00-19:00 his row can be home_front_door
vance_meeting | a solo button is a real act | N/A | — | one-time meeting, not a solo button
hub_vance_porch | want | PASS | I'll knock a little off his number. | asks for her company, eyes on her legs
hub_vance_porch | next step | PASS | Vance is standing before you reach his gate. | three Want tiers escalate (30, 60)
hub_vance_porch | hook | PASS | You come and sit out here one evening | names the next visit
hub_vance_porch | her voice at her level | N/A | — | no thought on screen
hub_vance_porch | who notices | PASS | That's a skirt and a half. Does your mother know | reacts to what she wears
hub_vance_porch | the written no | FAIL | "Goodnight, Mr. Vance." | the offer to sit has a refusal, but neither it nor the yes (steps node) changes anything
hub_vance_porch | the body | N/A | — | not explicit
hub_vance_porch | the numbers and the clothes agree | PASS | That's a skirt and a half. | skirt line is behind worn_type short_skirt
hub_vance_porch | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hub_vance_porch | true on every visit it can render on | FAIL | He'd sell me the house back for less. | Vance owns the house and the family rents (WANT §2, npc_vance); also "I'll knock a little off his number" is a promise the steps node never builds (no effect)
hub_vance_porch | a solo button is a real act | N/A | — | person canvas
vance_walk_past | want | PASS | The paper lowers. He wets his lips. | his want shows when she dresses for it
vance_walk_past | next step | N/A | — | repeatable loop; the step is carried by the hub tiers
vance_walk_past | hook | FAIL | you feel him watch you all the way to the corner. | neither branch names what comes next
vance_walk_past | her voice at her level | N/A | — | no thought
vance_walk_past | who notices | PASS | to him you're scenery. | he reads what she wears, both ways
vance_walk_past | the written no | N/A | — | no offer
vance_walk_past | the body | N/A | — | not explicit
vance_walk_past | the numbers and the clothes agree | N/A | — | no garment named; branches gated on skirt/bra
vance_walk_past | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
vance_walk_past | true on every visit it can render on | PASS | A nod from the rocking chair. | requires_npc hides it unless he is at vance_house; once a day
vance_walk_past | a solo button is a real act | PASS | Keep walking, hips loose. | moves her to the street and raises his Want
mark_01_count_it_slowly | want | PASS | his eyes go straight to your bare legs, and stay. | control and her, both on screen
mark_01_count_it_slowly | next step | PASS | Sit. I count it in front of you. | his first step
mark_01_count_it_slowly | hook | PASS | The rest waits a week. Vance doesn't. | names the next Sunday/Vance (paid branch: "Same again Sunday.")
mark_01_count_it_slowly | her voice at her level | N/A | He counted you as much as the money. | no meter of hers gates the canvas
mark_01_count_it_slowly | who notices | PASS | He notices. He doesn't like noticing. | Mark reacts to the count and the streak
mark_01_count_it_slowly | the written no | PASS | "Let me get dressed first." | written; skips his Want +10
mark_01_count_it_slowly | the body | N/A | — | not explicit
mark_01_count_it_slowly | the numbers and the clothes agree | PASS | Seventy-five, I said. | $75 matches WANT; sleep shirt and legs lines are clothing-gated; dressing is a wardrobeEffects equip
mark_01_count_it_slowly | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_01_count_it_slowly | true on every visit it can render on | PASS | Laura's out shopping. | Sun 08-12: Laura away, Mark in kitchen
mark_01_count_it_slowly | a solo button is a real act | N/A | — | person canvas
mark_02_late_notice | want | PASS | Put it back. | he wants the letter back and her quiet
mark_02_late_notice | next step | PASS | LATE NOTICE, it says. | she learns the debt
mark_02_late_notice | hook | PASS | You've got something on him now. | points at leverage she will use
mark_02_late_notice | her voice at her level | N/A | You've got something on him now. | no meter of hers in play
mark_02_late_notice | who notices | PASS | He sees you. He sees what's in your hand. | Mark catches her
mark_02_late_notice | the written no | N/A | — | no offer
mark_02_late_notice | the body | N/A | — | not explicit
mark_02_late_notice | the numbers and the clothes agree | N/A | — | no figure stated ("a lot of zeros"), no garment
mark_02_late_notice | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_02_late_notice | true on every visit it can render on | PASS | Through the wall you can hear Mark in the living room | Sun-Fri 22-24 his row is home_living_room
mark_02_late_notice | a solo button is a real act | N/A | — | one-time step
mark_03_shorts | want | PASS | you feel his eyes go down the curve of your ass and stay there. | on screen
mark_03_shorts | next step | PASS | Every Sunday. Like that. | the dress rule
mark_03_shorts | hook | PASS | Every Sunday. Like that. | names every Sunday to come
mark_03_shorts | her voice at her level | N/A | — | no thought bubble
mark_03_shorts | who notices | PASS | His count goes slow. He loses his place twice. | Mark reacts
mark_03_shorts | the written no | PASS | "I'm not changing for you." | written; Power -2, short stays on tab, retry 7
mark_03_shorts | the body | N/A | — | not explicit (1 frozen word)
mark_03_shorts | the numbers and the clothes agree | FAIL | You come down in the shortest thing you own to sleep in | Power<50 start node names her sleep shorts before any check: the equip is on the NEXT click
mark_03_shorts | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_03_shorts | true on every visit it can render on | FAIL | Not the shirt this time. Shorts. | claims she wore the sleep shirt last Sunday; no flag records it. Also no node: "Then the short stays on the tab" shows when rent_carried is false
mark_03_shorts | a solo button is a real act | N/A | — | one-time step
mark_04_after_shes_asleep | want | PASS | Then he looks at your legs, for a long time, slowly | shown; earlier mark_01/mark_03 showed it too
mark_04_after_shes_asleep | next step | PASS | Come down after your mother's asleep. Some night. We'll talk about the rent. | the ask
mark_04_after_shes_asleep | hook | PASS | He's going to name a number. You want to hear it. | names the price to come
mark_04_after_shes_asleep | her voice at her level | PASS | You want to hear it. | appetite at corruption 40+
mark_04_after_shes_asleep | who notices | PASS | he turns the TV down further. | Mark reacts
mark_04_after_shes_asleep | the written no | PASS | "I'll pay it Sunday like everyone else." | written; Power -2, retry 3
mark_04_after_shes_asleep | the body | N/A | — | not explicit
mark_04_after_shes_asleep | the numbers and the clothes agree | FAIL | your bare knee by his shoulder. | no clothing condition on trigger, group or choice; false in jeans or leggings
mark_04_after_shes_asleep | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_04_after_shes_asleep | true on every visit it can render on | PASS | Laura's gone up. | gated on Laura present in master bedroom; Mark 22-24 living room
mark_04_after_shes_asleep | a solo button is a real act | N/A | — | one-time step
mark_05_a_bill_an_inch | want | PASS | He stares at your legs like a starving man. | earlier: mark_01 (eyes on legs), mark_03 (eyes on her ass), mark_04 (looks at her legs, thinks about a price)
mark_05_a_bill_an_inch | next step | PASS | Five for every inch my hand climbs your bare thigh. | first paid touch
mark_05_a_bill_an_inch | hook | PASS | you already want to know what he'll ask for next. | names the next ask
mark_05_a_bill_an_inch | her voice at her level | PASS | It was the easiest twenty you ever made. | appetite at corruption 40+
mark_05_a_bill_an_inch | who notices | PASS | Upstairs, a floorboard creaks. Your mother. | Mark and the house react
mark_05_a_bill_an_inch | the written no | PASS | "Hands off, Mark." / "Not tonight." | written; costs the twenty, retry 3
mark_05_a_bill_an_inch | the body | PASS | Your legs stay open, and your thigh still burns where his hand was. | climb, stop, half each end on the body
mark_05_a_bill_an_inch | the numbers and the clothes agree | PASS | Ten, not twenty. | $10/$20 match the effects; bare legs backed by jeans/leggings unequipped on the trigger
mark_05_a_bill_an_inch | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_05_a_bill_an_inch | true on every visit it can render on | FAIL | he'll be on this couch tomorrow night. | shown Sat 00:00-01:00 (weekday 5 row): Saturday night 22-24 Mark's row is home_master_bedroom. Same node: "He folds the twenty back into his pocket" — the Power<50 branch never showed a twenty
mark_05_a_bill_an_inch | a solo button is a real act | N/A | — | one-time step
mark_06_our_arrangement | want | PASS | Our arrangement. Your mother has enough to worry about. | he wants the secret kept
mark_06_our_arrangement | next step | PASS | So we each keep one. | mutual secret
mark_06_our_arrangement | hook | FAIL | Your secret for his. He thinks it's even. It isn't. | nothing names the next ask, Sunday, or what comes
mark_06_our_arrangement | her voice at her level | PASS | It isn't. | her upper hand at corruption 40+
mark_06_our_arrangement | who notices | PASS | He's been off with you at dinner since the couch | Mark reacts
mark_06_our_arrangement | the written no | PASS | "There's no arrangement." | written; Power +2, retry 3
mark_06_our_arrangement | the body | N/A | — | not explicit
mark_06_our_arrangement | the numbers and the clothes agree | N/A | — | no number, no garment
mark_06_our_arrangement | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_06_our_arrangement | true on every visit it can render on | PASS | Mark's at his workbench with the radio on | Mon/Tue/Thu/Fri 19-22 his row is home_garage; couch is behind mark_step 5
mark_06_our_arrangement | a solo button is a real act | N/A | — | one-time step
mark_07_twenty_and_you_can_look | want | PASS | His breath goes short. | earlier: mark_05 (hand on her thigh, cock hard), mark_04, mark_03
mark_07_twenty_and_you_can_look | next step | PASS | You bare your tits for him under the kitchen light | past the thigh touch
mark_07_twenty_and_you_can_look | hook | PASS | Wednesday says WORK LATE in blue. | points at mark_08/09
mark_07_twenty_and_you_can_look | her voice at her level | N/A | — | no thought
mark_07_twenty_and_you_can_look | who notices | PASS | Mark counts the twenties twice. He does that now. | Mark reacts
mark_07_twenty_and_you_can_look | the written no | PASS | "Just the rent." | written; Want +2, retry 7
mark_07_twenty_and_you_can_look | the body | PASS | your nipples aching in the cold while his eyes stay on them. | ends on the body
mark_07_twenty_and_you_can_look | the numbers and the clothes agree | FAIL | You lay one more twenty on top of it yourself. | she lays her own twenty and he slides his; the toast pays +20 net. No node: "He slides his twenty back across the table to you anyway" pays nothing
mark_07_twenty_and_you_can_look | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_07_twenty_and_you_can_look | true on every visit it can render on | PASS | Laura's out shopping. Ryan's door is shut upstairs. | Sun 08-12: Laura away, Ryan in his room
mark_07_twenty_and_you_can_look | a solo button is a real act | N/A | — | one-time step
mark_08_the_red_circle | want | PASS | Mark is at the table with his paper, watching you over the top of it. | watching her
mark_08_the_red_circle | next step | PASS | You draw a slow red circle round Wednesday evening. | she sets the date
mark_08_the_red_circle | hook | PASS | You'll see. | names Wednesday
mark_08_the_red_circle | her voice at her level | PASS | Laura late. Ryan out. Just him, and his chair. | appetite at corruption 40+
mark_08_the_red_circle | who notices | PASS | What's that for? | Mark reacts
mark_08_the_red_circle | the written no | N/A | — | no offer; she acts
mark_08_the_red_circle | the body | N/A | — | not explicit
mark_08_the_red_circle | the numbers and the clothes agree | N/A | — | no number, no garment
mark_08_the_red_circle | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_08_the_red_circle | true on every visit it can render on | PASS | Laura late. Ryan out. | Wed: Laura and Ryan away to 22:00 (Ryan's league line is a gate red line, left alone)
mark_08_the_red_circle | a solo button is a real act | N/A | — | one-time step
mark_09_his_chair | want | PASS | He's hard in his jeans | on screen
mark_09_his_chair | next step | PASS | You sit down in his chair at the head of the table | she takes his chair
mark_09_his_chair | hook | PASS | His lap is right there, waiting | names the next step
mark_09_his_chair | her voice at her level | PASS | you're not ready to give him that. Not yet. | owns the room at 40+, holds the line
mark_09_his_chair | who notices | PASS | He turns round with the spatula in his hand and stops dead. | Mark reacts
mark_09_his_chair | the written no | PASS | "No. I count." | written; Power +3, retry 7
mark_09_his_chair | the body | N/A | — | not explicit (under 3 frozen words)
mark_09_his_chair | the numbers and the clothes agree | FAIL | count Sunday's rent out of your purse onto the table | no `money` condition: she can reach this with less than $75
mark_09_his_chair | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_09_his_chair | true on every visit it can render on | PASS | He's cooking, Wednesday, his back to you. | Wed 18-22 Mark in kitchen; Laura and Ryan away
mark_09_his_chair | a solo button is a real act | N/A | — | one-time step
debt_offer | want | PASS | he's asking you something without asking. | his ask is on screen
debt_offer | next step | PASS | It isn't the rent. It's the house. | the twist
debt_offer | hook | PASS | "Let me think about it." | the parked answer
debt_offer | her voice at her level | N/A | Your rent every week is a drop in that. | no meter of hers in play
debt_offer | who notices | PASS | You pay your way now. | Mark reacts to her goal
debt_offer | the written no | PASS | "It's not my debt, Mark." | written; sets debt_refused, Power +3
debt_offer | the body | N/A | — | not explicit
debt_offer | the numbers and the clothes agree | N/A | — | no stated figure, no garment
debt_offer | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
debt_offer | true on every visit it can render on | FAIL | He hasn't hidden anything from you for a while. | pays_her_own_way can be set by mark_sunday_table at mark_step 1, before mark_02 (knows_mark_debt). Also "Mark borrowed against it years ago": WANT says the family rents the house from Vance
debt_offer | a solo button is a real act | N/A | — | one-time step
mark_sunday_table | want | PASS | He counts it twice anyway, because he wants to sit here longer. | the look branch is after mark_07, which showed it first
mark_sunday_table | next step | PASS | His eyes go to you and stay. He counts the twenties in his wallet | the step-7+ branch carries the paid look
mark_sunday_table | hook | PASS | Next Sunday. Same table. | names the next visit
mark_sunday_table | her voice at her level | N/A | — | no thought
mark_sunday_table | who notices | PASS | That's not what I asked you to wear to my table. | Mark reads her clothes
mark_sunday_table | the written no | PASS | Cover up. Give him his twenty back. | written; costs the $20
mark_sunday_table | the body | PASS | while his eyes crawl over your nipples. | all four look beats end on the body
mark_sunday_table | the numbers and the clothes agree | FAIL | You lay one more twenty on top of it yourself. | look_his and look_hers (corruption<50) put her own twenty down too; the toast pays +20
mark_sunday_table | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
mark_sunday_table | true on every visit it can render on | PASS | Your mother's out. | Sun 08-12 Laura away; shorts line gated on worn_type shorts
mark_sunday_table | a solo button is a real act | PASS | Sit down at the table | faceless link; it does the count (streak, flags)
vance_knock | want | PASS | I came for you, Miss. | rent, then her
vance_knock | next step | PASS | Come and see me one evening. We'll talk about what's owed. | Power 60 tier asks for her
vance_knock | hook | PASS | Tell him I came by about Sunday. He'll know. | names the debt and the visit
vance_knock | her voice at her level | N/A | A short week, and it comes to the door. | no meter of hers in play
vance_knock | who notices | PASS | Is your stepfather in? | Vance reacts to the short Sunday
vance_knock | the written no | PASS | "Mark will pay." Close the door. | written; withholds Want +3
vance_knock | the body | N/A | — | not explicit
vance_knock | the numbers and the clothes agree | N/A | — | no number, no garment
vance_knock | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
vance_knock | true on every visit it can render on | FAIL | The envelope in your hand is warm from his fingers. | "maybe" needs Power 60+; he hands her the envelope only in the Power<60 group
vance_knock | a solo button is a real act | N/A | — | person canvas
hub_mark_living_room | want | PASS | His eyes are on the hem of your sleep shirt. | clothing and step lines show it
hub_mark_living_room | next step | PASS | He looks at you like you're one more thing in this house that's his. | Power/Want/step tiers
hub_mark_living_room | hook | PASS | Further. (Needs Hungry) | folded bill (step 4) and the locked button name what's next
hub_mark_living_room | her voice at her level | FAIL | He wants you. He's stopped trying to hide it from you, only from her. | one thought, gated on his Want only, shown the same at every level of her corruption
hub_mark_living_room | who notices | PASS | That's what you wear in my house? | reads her clothes
hub_mark_living_room | the written no | N/A | — | no offer from him; paid buttons are hers and lead to placeholders
hub_mark_living_room | the body | N/A | — | not explicit; placeholder screens
hub_mark_living_room | the numbers and the clothes agree | PASS | You're in your underwear. | every garment line is behind a slot/item/type check
hub_mark_living_room | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hub_mark_living_room | true on every visit it can render on | FAIL | an hour goes by like that. | from 01:30, hl_tv runs past 02:00 when Mark's row is home_master_bedroom; hl_film (120 min): "He falls asleep in the second half" on the couch, same
hub_mark_living_room | a solo button is a real act | N/A | — | person canvas
hub_mark_bedroom | want | FAIL | Mark is asleep on his back on his side of the bed, snoring | nothing wanted; the description promises Want/Power and clothing lines, none built
hub_mark_bedroom | next step | N/A | — | repeatable with one fixed line
hub_mark_bedroom | hook | FAIL | Even asleep he takes up most of it. | nothing points ahead
hub_mark_bedroom | her voice at her level | N/A | — | no thought
hub_mark_bedroom | who notices | N/A | — | he is asleep; nothing to notice
hub_mark_bedroom | the written no | N/A | — | no offer
hub_mark_bedroom | the body | N/A | — | not explicit
hub_mark_bedroom | the numbers and the clothes agree | N/A | — | no number, no garment
hub_mark_bedroom | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hub_mark_bedroom | true on every visit it can render on | PASS | Mark is asleep | every master-bedroom row of his is a sleep row
hub_mark_bedroom | a solo button is a real act | N/A | — | person canvas
hub_mark_garage | want | PASS | His eyes are on the hem of your sleep shirt. | clothing and step lines show it
hub_mark_garage | next step | PASS | He looks at you like you're one more thing in this house that's his. | Power/Want/step tiers
hub_mark_garage | hook | FAIL | What do you want? I'm busy. | no line or shown button names a next step
hub_mark_garage | her voice at her level | FAIL | He wants you. He's stopped trying to hide it from you, only from her. | one thought, gated on his Want only, shown the same at every level of her corruption
hub_mark_garage | who notices | PASS | That's what you wear in my house? | reads her clothes
hub_mark_garage | the written no | N/A | — | no offer from him; paid buttons are hers and lead to placeholders
hub_mark_garage | the body | N/A | — | not explicit; placeholder screens
hub_mark_garage | the numbers and the clothes agree | PASS | You're in your underwear. | every garment line is behind a slot/item/type check
hub_mark_garage | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hub_mark_garage | true on every visit it can render on | PASS | He hasn't been able to since the couch. | behind mark_step 5; Mark's garage rows hold
hub_mark_garage | a solo button is a real act | N/A | — | person canvas
hub_mark_kitchen | want | PASS | His eyes are on the hem of your sleep shirt. | clothing and step lines show it
hub_mark_kitchen | next step | PASS | He looks at you like you're one more thing in this house that's his. | Power/Want/step tiers
hub_mark_kitchen | hook | PASS | He keeps looking at the fridge. At the red circle. | step lines and "Further" point ahead
hub_mark_kitchen | her voice at her level | FAIL | He wants you. He's stopped trying to hide it from you, only from her. | one thought, gated on his Want only, shown the same at every level of her corruption
hub_mark_kitchen | who notices | PASS | That's what you wear in my house? | reads her clothes
hub_mark_kitchen | the written no | N/A | — | no offer from him; paid buttons are hers and lead to placeholders
hub_mark_kitchen | the body | N/A | — | not explicit; placeholder screens
hub_mark_kitchen | the numbers and the clothes agree | PASS | You're in your underwear. | every garment line is behind a slot/item/type check
hub_mark_kitchen | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
hub_mark_kitchen | true on every visit it can render on | FAIL | Eat, @player. Then the rent. | no sunday_counted_today or rent_starts check: false after the count, or before rent starts. Also Wed "Mark's cooking" shows to 21:59 while the hub's own dishes run 19-21
hub_mark_kitchen | a solo button is a real act | N/A | — | person canvas
vance_house_look | want | N/A | — | no person on screen
vance_house_look | next step | N/A | — | no person
vance_house_look | hook | N/A | — | no person
vance_house_look | her voice at her level | N/A | Somewhere in those cabinets is a folder with Mark's name on it. | no meter in play
vance_house_look | who notices | N/A | — | nothing to notice
vance_house_look | the written no | N/A | — | no offer
vance_house_look | the body | N/A | — | not explicit
vance_house_look | the numbers and the clothes agree | N/A | — | no number, no garment
vance_house_look | companion and rival | N/A | — | want.companion_is_rival not declared in v2_state.json
vance_house_look | true on every visit it can render on | PASS | Vance's house is bigger than yours and better kept | no person, time or past claim; thought behind knows_mark_debt
vance_house_look | a solo button is a real act | FAIL | "Go." -> vance_house | describes only, no time, no effect, and lands where she stood

```json
{
 "vance_meeting": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "hub_vance_porch": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "FAIL",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "vance_walk_past": {
  "want": "PASS",
  "next step": "N/A",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "mark_01_count_it_slowly": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "mark_02_late_notice": {
  "want": "PASS",
  "next step": "PASS",
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
 "mark_03_shorts": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "mark_04_after_shes_asleep": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "mark_05_a_bill_an_inch": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "mark_06_our_arrangement": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "mark_07_twenty_and_you_can_look": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "mark_08_the_red_circle": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "mark_09_his_chair": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "PASS",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "debt_offer": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "mark_sunday_table": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "PASS",
  "the numbers and the clothes agree": "FAIL",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "PASS"
 },
 "vance_knock": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "N/A",
  "who notices": "PASS",
  "the written no": "PASS",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "hub_mark_living_room": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "FAIL",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "hub_mark_bedroom": {
  "want": "FAIL",
  "next step": "N/A",
  "hook": "FAIL",
  "her voice at her level": "N/A",
  "who notices": "N/A",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "N/A",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "hub_mark_garage": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "FAIL",
  "her voice at her level": "FAIL",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "PASS",
  "a solo button is a real act": "N/A"
 },
 "hub_mark_kitchen": {
  "want": "PASS",
  "next step": "PASS",
  "hook": "PASS",
  "her voice at her level": "FAIL",
  "who notices": "PASS",
  "the written no": "N/A",
  "the body": "N/A",
  "the numbers and the clothes agree": "PASS",
  "companion and rival": "N/A",
  "true on every visit it can render on": "FAIL",
  "a solo button is a real act": "N/A"
 },
 "vance_house_look": {
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
  "a solo button is a real act": "FAIL"
 }
}
```

## FAILs by test

### want
- hub_mark_bedroom: "Mark is asleep on his back on his side of the bed, snoring" — nothing wanted; the description promises Want/Power and clothing lines, none built

### hook
- vance_meeting: "You tell your stepfather I said good evening." — no line names the porch, the rent or a next visit
- vance_walk_past: "you feel him watch you all the way to the corner." — neither branch names what comes next
- mark_06_our_arrangement: "Your secret for his. He thinks it's even. It isn't." — nothing names the next ask, Sunday, or what comes
- hub_mark_bedroom: "Even asleep he takes up most of it." — nothing points ahead
- hub_mark_garage: "What do you want? I'm busy." — no line or shown button names a next step

### her voice at her level
- hub_mark_living_room: "He wants you. He's stopped trying to hide it from you, only from her." — one thought, gated on his Want only, shown the same at every level of her corruption
- hub_mark_garage: "He wants you. He's stopped trying to hide it from you, only from her." — one thought, gated on his Want only, shown the same at every level of her corruption
- hub_mark_kitchen: "He wants you. He's stopped trying to hide it from you, only from her." — one thought, gated on his Want only, shown the same at every level of her corruption

### the written no
- hub_vance_porch: ""Goodnight, Mr. Vance."" — the offer to sit has a refusal, but neither it nor the yes (steps node) changes anything

### the numbers and the clothes agree
- mark_03_shorts: "You come down in the shortest thing you own to sleep in" — Power<50 start node names her sleep shorts before any check: the equip is on the NEXT click
- mark_04_after_shes_asleep: "your bare knee by his shoulder." — no clothing condition on trigger, group or choice; false in jeans or leggings
- mark_07_twenty_and_you_can_look: "You lay one more twenty on top of it yourself." — she lays her own twenty and he slides his; the toast pays +20 net. No node: "He slides his twenty back across the table to you anyway" pays nothing
- mark_09_his_chair: "count Sunday's rent out of your purse onto the table" — no `money` condition: she can reach this with less than $75
- mark_sunday_table: "You lay one more twenty on top of it yourself." — look_his and look_hers (corruption<50) put her own twenty down too; the toast pays +20

### true on every visit it can render on
- vance_meeting: "Next door, on his porch, the man who owns your house: Mr. Vance." — fires with vance_met false; Vance's vance_house row is `when vance_met`, so he is nowhere then, and Mon 18:00-19:00 his row can be home_front_door
- hub_vance_porch: "He'd sell me the house back for less." — Vance owns the house and the family rents (WANT §2, npc_vance); also "I'll knock a little off his number" is a promise the steps node never builds (no effect)
- mark_03_shorts: "Not the shirt this time. Shorts." — claims she wore the sleep shirt last Sunday; no flag records it. Also no node: "Then the short stays on the tab" shows when rent_carried is false
- mark_05_a_bill_an_inch: "he'll be on this couch tomorrow night." — shown Sat 00:00-01:00 (weekday 5 row): Saturday night 22-24 Mark's row is home_master_bedroom. Same node: "He folds the twenty back into his pocket" — the Power<50 branch never showed a twenty
- debt_offer: "He hasn't hidden anything from you for a while." — pays_her_own_way can be set by mark_sunday_table at mark_step 1, before mark_02 (knows_mark_debt). Also "Mark borrowed against it years ago": WANT says the family rents the house from Vance
- vance_knock: "The envelope in your hand is warm from his fingers." — "maybe" needs Power 60+; he hands her the envelope only in the Power<60 group
- hub_mark_living_room: "an hour goes by like that." — from 01:30, hl_tv runs past 02:00 when Mark's row is home_master_bedroom; hl_film (120 min): "He falls asleep in the second half" on the couch, same
- hub_mark_kitchen: "Eat, @player. Then the rent." — no sunday_counted_today or rent_starts check: false after the count, or before rent starts. Also Wed "Mark's cooking" shows to 21:59 while the hub's own dishes run 19-21

### a solo button is a real act
- vance_house_look: ""Go." -> vance_house" — describes only, no time, no effect, and lands where she stood
