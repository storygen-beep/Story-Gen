> Copied into the game on 2026-11-03 (third alignment pass) from `~/Documents/Great_Games_Study_20260926/round12_tease/copy_fixes_A.md`, unchanged below this note. Signed by LO 2026-11-02 with the a2 sheets (DECISIONS 125: "they go in as drafted").

Draft for LO, 2026-11-02: replacement copy for group A (home and family), from `first_term_reader/reader_first_term_heat_A.md` row 12. Nothing is built or edited. Gates, effects and button destinations are unchanged.

Scope: every row-12 verdict with "talk only", "no body part" or "no body", "no reaction", "no not-yet or price", or "leak not physical". Rules: `the-heat-ladder.md` H4 and H7, `register.md` "The voice" and "The truth rule". Crude words come from `spine/SP2_ladders.md` §6. Early columns: Ryan "ass, tits", Mark "legs, ass", Laura "body, chest". Laura's middle column, "tits, nipples", is used once, at her step 3.

Sources. Most text is in `games/first_term/iterations/002/build_scripts/*.py`. Mark's tease screens and his reach event are the writer's files in `games/first_term/iterations/002/placeholders/NN_*.txt`, which `writer.py` puts into the build. The hot repeatables come from `sheets/scenes/ryan_hot_repeatables.md`, read by `sheetbeats.py`. TOML lines are `toml_phases/7_final_game.toml` as built 2026-11-01 20:22.

Measured: each new Ryan, Laura and Mark line that is not a one-line addition was run through `gates.py --beat`. None of them counts as explicit (1–2 frozen words each, needs 3). Median sentence is 5–14, under the ceiling of 14.

## Index

| # | canvas · node | verdict fixed | musts added |
|---|---|---|---|
| A1 | ryan_02_phone_on_the_sink · sink | no body part | body named, his reaction, leak on his body |
| A2 | hub_ryan_room · hot1 "Lean in his doorway." | no not-yet or price | already rewritten on the sheet. Rebuild only, no new copy |
| A3 | bathroom_shower · shower (Ryan group) | leak not physical | leak on his body, seen by her; body named |
| A4 | home_event_ryan_towel · event | no body part; no reaction | body named, his reaction, leak on his body (stage 1 cover) |
| A5 | garden_sun · sun_seen ("Show off for whoever's looking.") | no reaction; no not-yet or price | his reaction and leak, a not-yet or price, a hook, one branch per watcher |
| A6 | laura_06_take_me_with_you · bed | leak not physical (talk only) | her want on her body; a Ryan-present branch |
| A7 | home_event_laura_robe · ev_curious "Don't look away." | talk only / no body (PLACEHOLDER) | full screen: body, her reaction, not yet, hook |
| A8 | hub_mark_living_room · hl_beer_tease "Curl up on the couch." | no not-yet or price | not yet, hook |
| A9 | hub_mark_garage · hl_laundry_tease "Leave your basket on top." | no not-yet or price | not yet, hook |
| A10 | hub_mark_kitchen · hl_breakfast_tease "Let him look." | no not-yet or price | not yet, hook |
| A11 | hub_mark_kitchen · hl_dinner_tease "Eat slowly for him." | no not-yet or price | not yet, hook |
| A12 | hub_mark_kitchen · hl_cook_tease "Reach past him for the pan." | no not-yet or price | not yet, his reaction, hook |
| A13 | hub_mark_kitchen · hl_dishes_tease "Bend to the dishwasher." | no not-yet or price | not yet (a price: "ask"), hook |
| A14 | home_event_mark_reach · ev_curious "Lean back into him." | no not-yet or price | not yet, hook |
| A15 | garden_sun · sun_mark_tease "Stretch out for him." | no not-yet or price | not yet, risk sentence, hook (+ a truth fix) |
| A16 | wardrobe_event_stairs · stairs (Mark group) "Keep climbing." | no body part; no not-yet or price | body named, his reaction on his body, not yet |
| A17 | living_couch · couch (Mark and Ryan groups) "Stay a while." | no body part | body named, his reaction, leak on his body (Ryan) |
| A18 | vance_knock · knock (Power 60+ group) "Maybe one evening." | no body part | body named, his reaction |

---

## A1 · ryan_02_phone_on_the_sink · node `sink`
- **Where:** `build_scripts/ryan.py:24` (first two sentences of the paragraph) · TOML `7_final_game.toml:4065`
- **Current:** "His eyes find you in the mirror through the steam, and go away again too fast."
- **New:** "His eyes find you in the mirror through the steam. They drop down your back to your ass and stay there. Then he catches himself, looks at the tiles, and turns to face the wall, fast, so you can't see the front of him." The paragraph goes on unchanged: "Then his phone buzzes on the edge of the sink…"
- **Musts added:** body named (ass) · his reaction · leak on his body (H7 stage 1: he looks, catches himself, looks away, turns the bulge from her). The hook is already there (the phone, "Read it.").
- **Truth note:** no garment is named, so the line is true in any outfit, towel included. She has her back to him, so "down your back" works. The thin_top group at `ryan.py:26-27` stays as it is. "the front of him" is right because he is naked in the shower.

## A2 · hub_ryan_room · hot1 "Lean in his doorway."
- **Where:** the pool text comes from `sheets/scenes/ryan_hot_repeatables.md:39-49` (1a/1b/1c), read by `sheetbeats.pool` at `ryan.py:327`/`hot_node`. TOML `7_final_game.toml:5520` (stale).
- **Current (built):** "…\"Then why are you staring at my legs?\" He doesn't answer. His eyes climb your legs, slow, and stop at your mouth…"
- **New:** no new copy. The sheet was already rewritten after the build (sheet saved 2026-11-02 00:02, TOML 2026-11-01 20:22, DECISIONS 124). Each entry names her body (1a "Your tits lift", 1b "the front of your thigh", 1c "your ass"), hides and fails to hide his bulge (pillow, chair turned, sock in his lap), and ends on "Not tonight… tomorrow".
- **Musts:** body, reaction, leak, not yet and hook are all on the sheet already.
- **Truth note:** the three entries name no garment, so they are true in any outfit. "Ask me nicely tomorrow" fits a canvas that runs Mon, Tue, Thu and Sun evenings and can be seen again. Run the build so 7_final_game.toml takes the sheet text.

## A3 · bathroom_shower · node `shower`, group `npc_ryan is_present home_ryan_room`
- **Where:** `build_scripts/home.py:133` · TOML `7_final_game.toml:25675`
- **Current:** "Ryan's door opens across the hall. His steps stop outside the bathroom. The handle turns, catches on the lock, and lets go. \"Sorry,\" he says through the door, and doesn't move away from it for a long second."
- **New:** "Ryan's door opens across the hall. The bathroom handle turns, and the sticky lock gives an inch before it catches. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He looks at the floor and turns side-on, one hand in front of his shorts. \"Sorry.\" He doesn't move away from the door for a long second."
- **Optional variant** (group `npc_ryan.want gte 40`, after the line): "This time he doesn't look at the floor until the door clicks shut."
- **Musts added:** leak on his body, seen by her (H7 stage 1: he looks, looks away, hides the front of his shorts) · body named (tits). This is an accident. Her way out is the existing "Wrap up in a towel.", and it pays nothing new.
- **Truth note:** the beat above says "the lock sticks halfway like always", so the inch of gap is backed. The same beat says "your eyes shut", which is why the new line opens her eyes before she sees him. "his shorts" are his own clothes, not hers, so the clothes gate does not apply. The group still needs Ryan in his room. The shower never plays while he is in the bathroom (`home.py:142`).

## A4 · home_event_ryan_towel · node `event`
- **Where:** `build_scripts/home.py:603` · TOML `7_final_game.toml:27624`. The sheet's direction is at `sheets/people/npc_ryan.md:219`.
- **Current:** "The bathroom door opens as you pass and Ryan steps out in a towel, wet, steam behind him. You nearly walk into his chest." then Ryan "Sorry." and her "Sorry."
- **New:** keep the first paragraph as it is. After it, add one chain of groups, then the two "Sorry." lines as now:
  - `worn_type eq towel`: "You're in your towel too. His eyes drop to the knot over your tits. They go down to your bare thighs and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel."
  - `worn_type eq sleep_shirt`: "His eyes drop down your sleep shirt to your bare legs and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel."
  - else (`worn_exposure gte 0`, the writer's ANY): "His eyes drop to your tits and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel."
- **Musts added:** body named · his reaction · leak on his body (stage 1 cover: looks, catches himself, turns the tent away). The way out ("Step round him.") and the hooks ("Walk past slowly.", "Let him look.") are already there.
- **Truth note:** the event runs Mon–Fri 06:45–07:30, which allows a towel, a sleep shirt or day clothes. Each branch names only what that branch backs. In the else branch "tits" is true in any outfit. Adjacent groups merge into one if/elseif chain, so exactly one shows. Pays as now: Ryan Want +1, nothing to her (H5).

## A5 · garden_sun · node `sun_seen` (choice "Show off for whoever's looking.")
- **Where:** `build_scripts/home.py:528` (the node). Its two choices are at `home.py:517` (Mark in the garage) and `home.py:520` (Ryan in his room, Mark not in the garage). TOML `7_final_game.toml:27341`
- **Current:** "You stay exactly as you are and let whoever's looking look. Your skin is hot and it isn't only the sun."
- **New:** replace it with two groups, one per watcher:
  - group `npc_mark is_present home_garage`: "You stay on your front and push up on your elbows, slow, so from the garage door he gets your bare back and the curve of your ass. The radio stays off. When you look round, Mark is holding his beer low, in front of his jeans." Mark: "Fence is low, @player." Her: "I'm not turning over, Mark. Not today."
  - group `npc_ryan is_present home_ryan_room` + `npc_mark is_absent home_garage`: "You roll onto your back, and your tits are bare to the sky and to his window. His music doesn't come back on. Ryan stands at the glass, then steps back fast, red to the ears." Her: "Want a better look, Ryan? Come down and ask me." Then: "He doesn't come down. Not today."
- **Musts added:** his reaction · leak on his body (Mark's beer held over his jeans; Ryan steps back) · a not yet (Mark) or a price (Ryan: "come down and ask") · hook: turning over for Mark, and for Ryan the sun-lotion rung ("Call him down with the sun lotion.", Bold, already on `sun_ryan`).
- **Truth note:** both choices need TOPLESS (top, dress and bra off). The sun node already prints "Topless, on your front", so "stay on your front" and "roll onto your back" both follow from it. Her bottoms are not named, so "your ass" is true. No "sun" claim, because the garden is open until 21:00, after the sun. Mark's early column has no "tits", so his branch shows her back and her ass only. The pays stay as they are.

## A6 · laura_06_take_me_with_you ("All dressed up") · node `bed`
- **Where:** `build_scripts/laura.py:173-175` · TOML `7_final_game.toml:7380`. The sheet's intent is at `sheets/people/npc_laura.md` §seven columns, row 3.
- **Current:** "She sits down on the end of the bed in her good dress, her heels in her hand. Her lipstick is perfect. She has nowhere to go." then Laura: "Do I still look like someone you'd look at?"
- **New:** keep the paragraph, then add:
  - always: "She pulls her shoulders back for the mirror, and her chest lifts in the dress. She's looking at herself the way she wants somebody to look at her."
  - group `npc_ryan is_present home_living_room`: "Downstairs Ryan laughs at something on the TV. Her hands stop in her lap. She looks at the door, not at you, and her nipples go hard through the dress."
  - then her line and the thought, as now.
- **Musts added:** her want on her body, seen by Ella (her chest; her nipples when Ryan is heard) · the Ryan sign the audit's row 1 asks for before laura_04's "Ryan." The not-yet ("Liar.") and the hook ("her bedroom door doesn't quite close") are already in the nodes after.
- **Truth note:** the step runs Sat 17:00–18:30. Ryan's row puts him on the couch Sat 14:00–18:00 only (`npc_ryan.md:41`). The sheet's "Ryan's laugh comes up the stairs" is therefore a lie from 18:00 to 18:30, so it needs the group. Mark has already left for the bar (`zipped` node). "the dress" is Laura's good dress, named in prose; Ella's clothes are not named. "nipples" is Laura's middle column. For the early column, use "and her chest rises and falls fast in the dress" instead.

## A7 · home_event_laura_robe · node `ev_curious` ("Don't look away.") · PLACEHOLDER
- **Where:** `build_scripts/home.py:613` (placeholder via `event()`, `home.py:589-597`). Signed line: `sheets/places/home_hall.md:45` "@player doesn't look away." TOML `7_final_game.toml:27792`
- **Current:** "PLACEHOLDER — sheets/places/home_hall.md:45 (Laura's robe: curious)."
- **New:**
  > You don't look away. Laura's fingers are still on the knot, and your eyes are still on her chest, where the robe sat open a second ago. She sees where you're looking. The pink goes down her neck and into the robe.
  > Laura: "Eyes up, sweetheart."
  > You: "You look good, Mom."
  > She laughs, short, and pulls the robe tighter. It doesn't help. The knot sits tight across her chest now, and you both know you're looking at it.
  > Laura: "Not before my coffee. Go on."
  >
  > *She didn't tell you to stop. She told you not yet.*
- **Optional hook variant** (group `flag:laura_lonely is_true`, after the last beat): "Tonight her bedroom door won't quite close. She knows you know it."
- **Musts:** her body named (chest; early column "body, chest") · Laura's reaction (the flush, the laugh, the tighter knot) · a not yet said out loud ("Not before my coffee.") · hook (the thought, plus the optional door line). The exit stays "Go on." Pays as now: Laura Warmth +1.
- **Truth note:** the event runs in the kitchen Mon–Fri 06:30–08:00 with Laura there, so "coffee" fits the hour. Ella's clothes are not named. "Eyes up" replaces any mention of cereal, because she may not be eating. The optional line is true only behind `laura_lonely`, which step 3 sets with "On weeknights now, her bedroom door doesn't quite close." The event is weekday-only, so "tonight" is Mon–Fri, inside the gap's Sun–Fri.

## A8 · hub_mark_living_room · node `hl_beer_tease` ("Curl up on the couch.")
- **Where:** `placeholders/21_hub_mark_living_room_hl_beer_tease.txt:13-18`, wired at `mark.py:495`. TOML `7_final_game.toml:11295`
- **Current:** ends "Then keep sitting like that." / "*He's counting every inch of your legs. Let him count.*"
- **New:** after "Then keep sitting like that." add: "You slide your foot along the cushion until it touches his thigh. He lifts it off with one hand, slow, and his hand stays round your ankle a second too long." Mark: "Not that close, @player." Replace the thought with: "*He said not that close. He didn't say not ever.*"
- **Musts added:** not yet said out loud · his reaction, on his hand · hook (the thought points at the next rung).
- **Truth note:** "your foot" names no shoe, so it is true in any outfit. The sleep-shirt variant (#21 variant 1) still goes after sentence 1. Mark's line is a limit, not an order to cover up, so it still fits his Power under 40 ("He doesn't give you orders any more").

## A9 · hub_mark_garage · node `hl_laundry_tease` ("Leave your basket on top.")
- **Where:** `placeholders/23_hub_mark_garage_hl_laundry_tease.txt:13-18`, wired at `mark.py:551`. TOML `7_final_game.toml:11996`
- **Current:** "He doesn't. When you bend to the machine, he looks at your ass instead." / "*He held them like he had every right to. You let him, because you wanted to see if he would.*"
- **New:** after "…he looks at your ass instead." add: You: "You could fold them for me, Mark." Mark: "Not today, @player." Then: "He goes back to his bench the long way, past the basket." Keep the thought.
- **Musts added:** not yet said out loud · hook (folding them is the withheld rung).
- **Truth note:** the panties stay "in the basket" and are never "your panties", as #23's facts say. "Not today" names no date, so no future scene has to be built for it. LO: "Let him fold them." is cut this release (`m_paid` returns None, `mark.py:393-394`). The not-yet points at a rung a later release would write.

## A10 · hub_mark_kitchen · node `hl_breakfast_tease` ("Let him look.")
- **Where:** `placeholders/25_hub_mark_kitchen_hl_breakfast_tease.txt:13-18`, wired at `mark.py:565`. TOML `7_final_game.toml:12290`
- **Current:** "He grunts. He turns a page, but he's still looking at your legs." / "*He's not reading a word of that paper. Let him look.*"
- **New:** after "…still looking at your legs." add: "You let one knee fall open toward him. He folds the paper shut." Mark: "Feet down, @player. Not at my table." Replace the thought with: "*Not at his table. So somewhere else.*"
- **Musts added:** not yet said out loud · his reaction (the paper shut) · hook.
- **Truth note:** beat 1 already puts her "knees up onto the chair, heels on the seat", so the knee is backed. "my table" is Mark's own phrase from his sheet ("That's what you wear to my table?"). Sunday breakfast 08:00–11:00. The sleep-shirt variant replaces only the quotation lines of beat 1, so put the new lines after the "He grunts." line.

## A11 · hub_mark_kitchen · node `hl_dinner_tease` ("Eat slowly for him.")
- **Where:** `placeholders/27_hub_mark_kitchen_hl_dinner_tease.txt:12-16`, wired at `mark.py:572`. TOML `7_final_game.toml:12376`
- **Current:** "So you go slower. Sauce runs down your thumb, and you lick it off while he watches your mouth. He puts his knife down and doesn't pick it up again." / "*He's telling you how to eat. And you're doing it.*"
- **New:** after "…doesn't pick it up again." add: Mark, low: "That's enough, @player. Not here." Replace the thought with: "*Not here, he said. You're going to make him say where.*"
- **Musts added:** not yet said out loud · hook.
- **Truth note:** with Laura at the table (#27 variant 1), "low" is why she doesn't hear. Without her it still reads right. No clothes are named. The beat's explicit count stays at 1 ("lick").

## A12 · hub_mark_kitchen · node `hl_cook_tease` ("Reach past him for the pan.")
- **Where:** `placeholders/28_hub_mark_kitchen_hl_cook_tease.txt:12-18`, wired at `mark.py:576`. TOML `7_final_game.toml:12439`, `:12453`
- **Current:** ends "*He made you touch him. Now he can say he didn't touch you.*" / "\"Salt.\" He holds his hand out without looking at you."
- **New:** after the "Salt." line add: Mark: "And not while I'm cooking, @player." Then: "His knuckles are white on the spoon."
- **Musts added:** not yet said out loud ("not while I'm cooking" holds the act back to some other time) · his reaction, on his body · hook.
- **Truth note:** the canvas runs Wed 18:00–19:00 only, while he cooks, so "while I'm cooking" is true every time it shows. No clothes are named.

## A13 · hub_mark_kitchen · node `hl_dishes_tease` ("Bend to the dishwasher.")
- **Where:** `placeholders/29_hub_mark_kitchen_hl_dishes_tease.txt:12-16`, wired at `mark.py:581`. TOML `7_final_game.toml:12519`
- **Current:** "You reach for it without standing up." / "*He could hand it to you. He wants you to reach.*"
- **New:** after "…without standing up." add: "He lifts the plate up out of your reach." Mark: "Not like that, @player. Stand up and ask me for it." Replace the thought with: "*He wants you to ask. You don't. Not yet.*"
- **Musts added:** a price on the yes ("ask me for it") · not yet · hook.
- **Truth note:** he is drying (hl_dishes, Wed and Sun 19:00–21:00), so he is holding plates. The short-skirt variant (#29 variant 1) is unchanged.

## A14 · home_event_mark_reach · node `ev_curious` ("Lean back into him.")
- **Where:** `placeholders/41_home_event_mark_reach_ev_curious.txt:12-16`, wired at `home.py:618`. TOML `7_final_game.toml:27855`, `:27864`
- **Current:** beat 2: "\"Excuse me, @player.\"" / "His voice is rough, and he still doesn't move." / "*He could have asked you to pass it. He didn't want to.*"
- **New:** beat 2: Mark: "Excuse me, @player." Then: "His voice is rough. Then he steps back and puts the mug down hard." Mark: "Not here." Thought: "*Not here, he said. He didn't say no.*"
- **Musts added:** not yet said out loud · hook. Beat 1 already names her body ("ass") and his leak ("get hard against your ass").
- **Truth note:** the event runs in the kitchen on Sunday 08:00–22:00, with Mark there. No clothes are named. The new lines sit in beat 2, so beat 1's explicit count stays at 2.

## A15 · garden_sun · node `sun_mark_tease` ("Stretch out for him.")
- **Where:** `placeholders/36_garden_sun_sun_mark_tease.txt:13-18`, node built at `home.py:546`. TOML `7_final_game.toml:27479`
- **Current:** "He takes a long pull on the beer and keeps looking." / "*His radio's still on in there. He isn't going back to it.*"
- **New:** after "…keeps looking." add: "You hook one thumb under your bra strap." Mark: "Leave that where it is, @player. Fence is low." Replace the thought with: "*Leave it, he said. For now.*"
- **Musts added:** not yet said out loud · the risk as a sentence ("Fence is low") · hook.
- **Truth note:** the bra is backed by the choice (BRA_ONLY). The sun node says "The fence is low", which backs the risk. ⚠️ The existing line has a truth defect the audit missed. "That how you spend a Saturday, @player?" (#36:14) can show on Mon, Tue, Thu and Fri 19:00–21:00, because MARK_SEES is only `npc_mark is_present home_garage` and his garage row covers those evenings (`npc_mark.md` schedule). Wrap it in a Saturday group and add a fallback for the other days: "That how you spend an evening, @player?"

## A16 · wardrobe_event_stairs · node `stairs`, Mark group ("Keep climbing.")
- **Where:** `build_scripts/pools.py:345` · TOML `7_final_game.toml:24880`
- **Current:** "Mark comes out of the living room into the hall below just as you reach the top. He stops. He looks up the stairs, straight up your skirt, and doesn't look away until you're on the landing."
- **New:** "Mark comes out of the living room into the hall below just as you reach the top. He stops. He looks up the stairs, straight up your skirt to your ass, and doesn't look away until you're on the landing. His hand has gone white on the banister." Mark: "That skirt doesn't go up stairs in my house, @player." Then: "You don't come down, and you don't go any slower. Not for him. Not yet."
- **Musts added:** body named (ass, Mark's early column) · his reaction on his body (the white hand) · not yet · hook.
- **Truth note:** the trigger needs `worn_type eq short_skirt`, so "skirt" is backed. "ass" is true with or without panties. The existing no-panties group (`pools.py:350`) still adds "gets everything". The line is a variant of Mark's short-skirt line on his sheet. Mark's group needs him in the living room (his late rows, 22:00–02:00). The audit's "no accident first (Mark)" is a gate question and is not handled here.

## A17 · living_couch · node `couch`, the two passer groups ("Stay a while.")
- **Where:** `build_scripts/home.py:241` (Mark), `home.py:242` (Ryan) · TOML `7_final_game.toml:26106`, `:26112`
- **Current (Mark):** "Mark comes through from the kitchen with a beer and stops behind the couch. You're in your underwear. He doesn't say cover up. He stands there drinking, looking down the length of you, and then he goes, slowly."
- **New (Mark):** "Mark comes through from the kitchen with a beer and stops behind the couch. You're in your underwear. He doesn't say cover up. He looks down the length of you, at your legs, at your ass in your panties. The beer stops halfway to his mouth. Then he goes, slowly."
- **Current (Ryan):** "Ryan comes down for a drink and sees you and stops on the last stair. \"Jesus, @player.nickname.\" He goes to the kitchen without looking again. He takes a long time getting that drink."
- **New (Ryan):** "Ryan comes down for a drink and stops on the last stair. His eyes go straight to your tits in your bra. Then they go up to the ceiling. \"Jesus, @player.nickname.\" He goes to the kitchen without looking again. He takes a long time getting that drink. On the way back up he holds the can in front of his shorts."
- **Optional Ryan variant** (a second group with `npc_ryan.want gte 40`, and `want lt 40` on the line above): "His eyes go down you, your tits, your panties, and come back up slow. He doesn't pretend he wasn't looking."
- **Musts added:** body named (Mark: legs, ass; Ryan: tits) · his reaction · leak on his body (Ryan, the stage-1 cover). The hook is the existing "Stay a while." This is the wear-at-home kind, so his line climbs and hers doesn't.
- **Truth note:** both groups need UNDIES (bra and underwear on; top, bottom and dress off), so "bra" and "panties" are backed. The Ryan base is his under-40 behaviour (`npc_ryan.md:205`). At Want 70 he "doesn't pretend", so the optional variant keeps the line true across his bands.

## A18 · vance_knock · node `knock`, group `npc_vance.power gte 60`
- **Where:** `build_scripts/mark.py:364` · TOML `7_final_game.toml:10952`
- **Current:** "He looks past you into the hall, then back at you, slow, all the way down and up."
- **New:** "He looks past you into the hall, then back at you, slow: your legs, your chest, all the way down and up. He wets his lips."
- **Musts added:** body named · his reaction. The price ("We'll talk about what's owed.") and the hook ("\"Maybe one evening.\"") are already in the group.
- **Truth note:** the front door, Monday 18:00–19:00, in any outfit. No garment is named. Vance has no crude-word column: SP2 §6 leaves him out and `npc_vance.md` has none. Plain, uncrude words are used until LO sets one.

---

## Skipped, and why

- **Rows whose only verdict is "too early" or "no accident first"** (gates handled elsewhere): ryan_04, ryan_07, ryan_08, ryan_two_knocks, hub_ryan_room hot4, hub_ryan_living_room hot2/hot6, home_event_ryan_towel "Walk past slowly.", ryan_door_ajar, laura_shower_gap, laura_alone_in_bed, master_door_saturday_night, mark_03, hub_mark_living_room/kitchen "Let it slip."/"Drop it.", Mark channel 5, living_tv "Keep watching.", front_step, jake_saturday_date, ryan_01 "Skip the opening".
- **Explicit beats** (3+ frozen words): out of scope by the brief.
- **hub_mark_kitchen "Reach past him for the pan." and home_event_mark_reach "Lean back into him."** also carry "too early". Only their not-yet copy is drafted here (A12, A14). Moving the gate to Bold stays with the gate work.
- **hub_ryan_room hot1 (A2)**: no new copy, because the sheet already holds a rewrite that meets H4. It needs a rebuild only.
- **ok rows**: not touched.

## Found against the audit

1. **hub_ryan_room hot1**: the audit's "no not-yet or price" reads the stale build. `sheets/scenes/ryan_hot_repeatables.md:39-49` was rewritten after it (DECISIONS 124) and already has body, leak, "Not tonight" and "tomorrow".
2. **laura_06**: the sheet's planned fix ("Ryan's laugh comes up the stairs from the couch", `npc_laura.md` row 3) is false 18:00–18:30. The step runs Sat 17:00–18:30 and Ryan's couch row ends at 18:00. It needs the presence group in A6.
3. **garden_sun sun_mark_tease**: "That how you spend a Saturday, @player?" can show on weekday evenings. Mark's garage row is Mon/Tue/Thu/Fri 19:00–22:00 as well as Saturday, and the garden is open until 21:00. The audit marked the row only "no not-yet". It is also a truth-rule defect (A15).
4. **Mark's tease screens** live in `iterations/002/placeholders/*.txt` (read by `writer.py`), not in `build_scripts/*.py`. The edits go there.
5. **Vance** has no crude-word column anywhere. LO should set one before his arc heats up.
