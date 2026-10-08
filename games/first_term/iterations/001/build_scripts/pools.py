"""The pool and system scenes: parties (arrival, drinks, chat, the dare, the hookup), the park
(walk, run, rest, selfie, the couple, hidden with Zoe), touching herself (bed, shower, toilet), the
stairs event. Sources: sheets/systems/parties.md, park.md, wardrobe.md; scenes party_*.md,
park_*.md, touch_*.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

Z, J, C = "npc_zoe", "npc_jake", "npc_cocky_guy"
R, L, M = "npc_ryan", "npc_laura", "npc_mark"
out = []
CAP_CUR, CAP_BOLD = 39, 59
CURIOUS, BOLD = trait("corruption", "gte", 20), trait("corruption", "gte", 40)
NO_CURFEW = cond(NO_CURFEW_ITEM)
AT_PARTY = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}
PARTY_SCHED = [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}, {"weekdays": [5], "start_time": "00:00", "end_time": "02:00"}]
LATE_PARTY = [{"weekdays": [4], "start_time": "23:00", "end_time": "00:00"}, {"weekdays": [5], "start_time": "00:00", "end_time": "02:00"}]
SHORT = {"type": "worn_beauty", "operator": "gte", "value": 2}   # a short skirt or a dress for going out
NOT_SHORT = {"type": "worn_beauty", "operator": "lt", "value": 2}

def capped(k, n, cap):
    return {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": cap}

# ═════════════ PARTIES ═════════════
out.append({
    "id": "party_arrive", "name": "Go in to Zoe's party",
    "description": "The Friday party at Zoe's (the parties sheet): the curfew, under 20 energy and something short each say why at the door. Arriving costs 15 energy; sets party_went and drinks_tonight 0.",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 5, "is_active": True,
                "schedules": [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}],
                "conditions": cond(flag("zoe_met"), trait("zoe_step", "gte", 1),
                                   {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "gte", "value": 24}),
                "metadata": {"show_when_blocked": True, "cooldown_message": "The party is Friday nights, from seven."}},
    "nodes": [node("door", "Zoe's door", [
        P("You can hear it from the stairwell: bass through the walls, somebody shrieking with laughter, the door propped open with a crate of beer."),
        G(CURFEW_ON, T("Laura said no. Not this Friday.")),
        G(cond(trait("energy", "lt", 20)), T("You're asleep on your feet. The party runs late. You could go home and sleep and come back.")),
        G(cond(NOT_SHORT), D(Z, "Not in that. Borrow mine. Bedroom. Go.")),
        G(cond(SHORT), D(Z, "Babe! Get in here. Now we're talking.")),
    ], [
        go("Go in. (15 energy)", loc="zoe_apartment", mins=10, costs=[{"trait": "energy", "value": 15}],
           cond_=cond(SHORT, NO_CURFEW_ITEM), flags=[fset("party_went")], eff=[setv("drinks_tonight", 0)]),
        go("Borrow Zoe's dress first.", loc="zoe_bedroom", mins=2),
        go("Go home.", loc="street", mins=2),
    ])]})

out.append({
    "id": "party_chat", "name": "Work the room",
    "description": "Party chat: who's here tonight and what they say; campus_talk +1 (capped by the arrival once a night).",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 2,
                "schedules": PARTY_SCHED, "conditions": cond(AT_PARTY)},
    "nodes": [node("room", "The party", [
        POOL(
            P("A girl from your Biology class grabs you and screams the lyrics of a song in your face, then hugs you like you're old friends. Maybe you are now."),
            P("Two guys from the team argue about whether you're Zoe's girlfriend. You don't correct them. Neither does Zoe."),
            P("Somebody's playing a drinking game on the kitchen floor. Somebody else is crying in the hall. A guy you've never met tells you you're famous, but he won't say why."),
            P("You end up on the balcony with three people you don't know, sharing a cigarette none of you smoke, laughing at nothing."),
            pid="party_chat_lines"),
        G(cond({"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": J, "operator": "is_present"}), P("Jake's by the kitchen. He raises his beer at you across the room.")),
        G(cond({"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": C, "operator": "is_present"}), P("Jake's teammate, the cocky one from Figure drawing, is leaning on the bathroom door. Watching you.")),
        D(Z, "You're a hit, babe. Everyone's asking about you."),
    ], [go("Keep going.", loc="zoe_apartment", mins=40, eff=[add("campus_talk", 1, clamp=False)]), go("Get some air.", loc="zoe_apartment", mins=10)])]})

DRINK_MOD = [{"key": "drinks_boost", "name": "Tipsy", "duration_hours": 3, "trait_offsets": {"corruption": 20, "exhibitionism": 20}}]
out.append({
    "id": "party_drink_offer", "name": "Somebody hands you a drink",
    "description": "A drink (the parties sheet): drinks_tonight +1 and the drinks boost for 3 hours (one stage up on both meters, for choices only; steps ignore it). The third drink sets heavy_night. A no always works.",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 4, "is_active": True,
                "schedules": PARTY_SCHED, "conditions": cond(AT_PARTY, trait("drinks_tonight", "lt", 3))},
    "nodes": [node("cup", "A red cup", [
        POOL(P("Someone pushes a red cup into your hand. Vodka and something orange. It's strong."),
             P("Zoe appears with two shots and holds one to your lips."), P("A guy from the team pours you something from a bottle with no label and winks.")),
        G(cond(trait("drinks_tonight", "eq", 2)), T("That'd be three. You'll feel it tomorrow.")),
    ], [
        go("Drink it.", loc="zoe_apartment", mins=15, cond_=cond(trait("drinks_tonight", "lt", 2)), mods=DRINK_MOD, eff=[add("drinks_tonight", 1)]),
        go("Drink it. (your third)", loc="zoe_apartment", mins=15, cond_=cond(trait("drinks_tonight", "eq", 2)), mods=DRINK_MOD,
           eff=[add("drinks_tonight", 1)], flags=[fset("heavy_night")]),
        go("\"I'm good, thanks.\"", node="no", mins=2),
    ]), node("no", "No thanks", [P("They shrug and drink it themselves. They look disappointed, but nobody pushes. At Zoe's, a no always works.")], [go("Go.", loc="zoe_apartment", mins=2)])]})

FLASH = ("\"Flash them, babe. Three seconds,\" Zoe says. The circle goes quiet. You pull everything up to your chin, and your tits drop out into the warm air, bare to people you sit next to in class. Your nipples go hard at once, tight and dark, while every eye lands on them. \"One,\" Zoe calls. Somebody whistles. A guy on the couch forgets the drink halfway to his mouth. \"Two.\" Your chest heaves, so your tits bounce with it. \"Three.\" You hold them out a breath past the count, nipples stiff and aching, before you let everything drop.")
out.append({
    "id": "party_dare", "name": "Zoe's dare",
    "description": "Zoe's dare after 23:00 (party_dare): at Showing, flash the circle (explicit). After Zoe A 4 she can dare Zoe back. A no costs nothing. Two a night.",
    "trigger": {"location": "zoe_apartment", "requires_npc": Z, "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 2,
                "schedules": LATE_PARTY, "conditions": cond(AT_PARTY, trait("exhibitionism", "gte", 40))},
    "nodes": [
        node("dare", "The circle", [
            P("Somebody's started truth or dare on the living-room floor, and Zoe pulls you down into the circle and puts her chin on your shoulder."),
            D(Z, "Flash them, babe. Three seconds."),
            G(cond(flag("picks_the_dares")), D(Z, "Or dare me. Go on. You pick now.")),
        ], [
            go("Do it.", node="flash", mins=2),
            go("Dare Zoe instead.", node="zoe", mins=2, cond_=cond(flag("picks_the_dares"))),
            go("\"Not tonight, Zo.\"", node="no", mins=1),
        ]),
        node("flash", "Three seconds", [P(FLASH),
            VID("a girl at a house party lifting her top to flash a circle of friends, fairy lights, cups", "girl flashing tits at house party circle", "truth or dare flash party", pool_dir="sex/party_dare_flash_t4")],
            [go("Back to the party.", loc="zoe_apartment", mins=20, eff=[capped("exhibitionism", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        node("zoe", "Dare Zoe", [
            ME("Kiss the TA's favourite. No, kiss me. Here. In front of them."),
            P("Zoe stares at you, and the circle goes \"ooooh\", and she climbs into your lap and does it, slow, both hands in your hair, until somebody throws a cushion at you both."),
            D(Z, "Happy?"),
        ], [go("Very.", loc="zoe_apartment", mins=20, eff=[capped("exhibitionism", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        node("no", "Not tonight", [D(Z, "Boo. Fine. Next one's yours."), P("She dares the guy on the couch to drink something from the sink instead. He does.")],
             [go("Go.", loc="zoe_apartment", mins=10, flags=[fset("party_cool_zoe")])]),
    ]})

ORAL = ("Zoe's bathroom door is locked, and the party thumps through the wall. You sink to your knees on the cold tiles. Jake's teammate leans on the sink and grins down at you. You open his jeans and pull his cock out, already hard. You lick the head slowly, so he has to watch. Then you take him in your mouth. His hand fists in your hair. He groans and pulls you into a rhythm, deeper with each stroke. You suck him hard while your hand works the base. His balls tighten against your fingers. His hips jerk, and he comes in your mouth, hot and thick. You swallow all of it, his cock still twitching on your tongue, then wipe your lip with your thumb.")
SEX = ("He locks Zoe's bathroom door and lifts you onto the sink. The party thumps through the wall. You yank his jeans open and his cock springs out, hard and thick. He pushes into you slowly, and you feel every inch stretch you. Then he starts slamming in hard. Your legs lock round his hips. His mouth finds your tits, and he sucks one nipple, then the other. You grab his ass and pull him deeper. The mirror fogs behind you. Somebody bangs on the door. You both keep going, faster. He groans into your neck and comes inside you. You come clenching around his cock, your heels digging into his ass.")
out.append({
    "id": "party_hookup", "name": "Jake's teammate",
    "description": "The party hookup (heat call A): the cocky guy, after 23:00, Zoe's locked bathroom; oral or sex at Bold. Not while Jake is there. Once a night.",
    "trigger": {"location": "zoe_apartment", "npc": C, "requires_npc": C, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(AT_PARTY, BOLD, flag("cocky_guy_met"),
                                   {"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": J, "operator": "is_absent"},
                                   flag("hookup_today", False))},
    "nodes": [
        node("ask", "Bathroom's free", [
            P("Jake's teammate, the one who drew you instead of the model, is leaning on the wall by Zoe's bathroom with a beer he's barely touched. He's been watching you all night. When you pass, he pushes off the wall."),
            D(C, "Bathroom's free. Just saying."),
            G(cond(flag("exam_psych_done")), D(C, "You still owe me for that exam. Or I owe you. Can't remember which.")),
        ], [
            go("\"Lead the way.\"", node="door", mins=2, flags=[fset("hookup_today")]),
            go("\"Not tonight.\"", node="no", mins=1),
        ]),
        node("door", "Locked", [
            P("Zoe's bathroom: fairy lights round the mirror, her makeup all over the sink. He locks the door. The party is right there through the wall, and he's looking at you like he's already decided."),
        ], [go("Get on your knees.", node="oral", mins=2), go("Pull him in.", node="sex", mins=2), go("Unlock the door.", node="no", mins=1)]),
        node("oral", "On your knees", [P(ORAL),
            VID("a girl on her knees on a bathroom floor at a party sucking a guy's cock as he leans on the sink", "blowjob party bathroom on knees", "girl sucks cock locked bathroom party", pool_dir="sex/party_hookup_oral_t5")],
            [go("Back to the party.", node="out", mins=15, eff=[capped("corruption", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        node("sex", "On the sink", [P(SEX),
            VID("a couple having sex on a bathroom sink at a party, her legs locked round him, the mirror fogged", "sex on bathroom sink party", "fucking on the sink at a house party", pool_dir="sex/party_hookup_sex_t5")],
            [go("Back to the party.", node="out", mins=20, eff=[capped("corruption", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        node("out", "Back out", [
            P("You come out first, fixing your hair. Zoe's in the hall with a drink in each hand. She looks at you, and at the bathroom door, and at him coming out behind you, and her mouth opens."),
            D(Z, "In my bathroom? Babe."),
            T("By Monday half of campus will know. You find you don't mind."),
        ], [go("Go back to the party.", loc="zoe_apartment", mins=5)]),
        node("no", "Not tonight", [D(C, "Your loss."), P("He goes back to his wall and his beer, grinning, still watching you.")], [go("Go.", loc="zoe_apartment", mins=2, flags=[fset("party_cool_cocky_guy")])]),
    ]})

# ═════════════ THE PARK ═════════════
SPORTS_ONLY = cond({"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"})
DARING_RUN = cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                  {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, logic="OR")

out.append({
    "id": "park_walk", "name": "Walk the path",
    "description": "A walk in the park: who she passes, what they see. Once a day. The next locked act is shown, naming Hungry.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("path", "The path", [
        POOL(P("You walk the loop round the pond. Ducks, dog walkers, a man on a bench with a newspaper. He's reading it, but he lowers it as you pass."),
             P("The wind comes off the water and goes straight up whatever you're wearing. A jogger turns his head to watch you hold it down, and nearly runs into a bin."),
             P("Two guys playing frisbee stop playing frisbee while you walk past. One of them says something. The other one laughs."), pid="park_walk_lines"),
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("The skirt is a problem in this wind. You let it be a problem.")),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), P("No bra, and the air is cool. Every man on the path finds a reason to look at your chest.")),
    ], [go("Finish the loop.", loc="park", mins=30), go("Let strangers see. (Needs Hungry)", node="wall", swl=True, cond_=cond(trait("corruption", "gte", 60)))]),
        node("wall", "Further", [P("That's further than you go in this release of First Term.")], [go("Back.", loc="park")])]})

out.append({
    "id": "park_run", "name": "Run",
    "description": "A run: energy 10. What she runs in decides who looks; Daring clothes (no bra, or a bra and no top): Exhibitionism +1. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("run", "A run", [
        G(cond({"type": "worn_type", "operator": "eq", "value": "leggings"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}),
          P("Leggings and a top, the normal way. You run the loop twice and your lungs burn and nobody looks twice, except the old man on the bench who looks at everybody.")),
        G(cond(*SPORTS_ONLY["items"], {"type": "worn_type", "operator": "eq", "value": "leggings"}), P("Just the sports bra and your leggings, and it's like you've set off an alarm. Heads turn on the whole loop. A guy doing push-ups stops at the top of one and stays there.")),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}),
          P("No bra under your top, and every stride shows it. A cyclist wobbles. A man walking his dog lets the dog walk him into a hedge.")),
        POOL(P("You finish at the gates with your hands on your knees, sweating, buzzing."), P("Your legs are jelly by the end. Your face is red and not only from running.")),
    ], [
        go("Cool down. (10 energy)", loc="park", mins=40, costs=[{"trait": "energy", "value": 10}], cond_=DARING_RUN, eff=[capped("exhibitionism", 1, CAP_BOLD)]),
        go("Cool down. (10 energy)", loc="park", mins=40, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"})),
        go("Walk it instead.", loc="park", mins=20),
    ])]})

out.append({
    "id": "park_rest", "name": "Rest on a bench",
    "description": "A bench in the sun: energy +5, once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("bench", "A bench", [POOL(
        P("You sit on a bench by the pond with your face tipped up to the sun and your eyes shut. Your shoulders come down from round your ears for the first time today."),
        P("You lie along a bench with your knees up and watch the clouds. A man walks past slowly, twice."))],
        [go("Get up.", loc="park", mins=30, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}])])]})

out.append({
    "id": "park_selfie", "name": "Take a selfie on the path",
    "description": "A photo on the path for her feed: followers +2, Exhibitionism +1. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("photo", "A selfie", [
        P("You find the good light by the willow and take twenty photos to get one. A man on a bench watches you do it, every angle."),
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("You take the one where the wind has the skirt. You post that one.")),
        G(SPORTS_ONLY, P("Sports bra, sweat, the pond behind you. The likes start before you've got your breath back.")),
    ], [go("Post it.", loc="park", mins=15, eff=[add("followers", 2, clamp=False), capped("exhibitionism", 1, CAP_BOLD)]), go("Delete them all.", loc="park", mins=5)])]})

RUN_SEEN = ("A sound comes from behind the bushes, low and wet and steady. You step off the path to look, straight into them. A man and a woman, both naked from the waist down, and they don't see you. She is bent over a fallen log, palms flat on the bark. He holds her hips from behind. His cock slides out of her, slick, then drives back in. Her tits swing under her with every thrust. His hand comes down on her ass and stays there, squeezing hard. She moans, loud, mouth open. You stare a second too long, and your face goes hot. Then he looks up, straight at you, still buried in her. You run, heart slamming, legs shaking, her moan still going behind you.")
WATCH = ("You crouch behind the rhododendron and part the leaves. A man has a woman bent against a tree, her palms flat on the bark. His cock slides out of her, slick and shining, then thrusts back in to the root. Every thrust makes a wet slap you can hear from here. He fills his hands with her tits and pinches her nipples hard. She moans loud, bites her lip, but can't hold the next one in. Her face is red, eyes shut, mouth hanging open. You stare at his cock. Your nipples go tight, and heat floods between your thighs. You press your hand flat on your stomach and keep it there. He drags her ass back onto his cock, faster, until her moans break into short, wet gasps.")
TOUCH = ("Behind the rhododendron, you can see everything. The man has the woman pinned to the tree, a hand full of each of her tits. His cock drives into her, hard and steady, and she moans on every stroke. Your hand slides down your belly and inside. Your fingers find your clit, and you are already wet. You match him. Each time he thrusts, you rub, fast and tight. Her nipples stand stiff between his fingers while her ass slaps the bark. You bite your lip so no sound gets out. Neither of them looks toward the bush. He groans and buries his cock deep, and you come with him. Your knees buckle, and your free hand grips a branch while your fingers keep working your clit through it.")
out.append({
    "id": "park_watch_the_couple", "name": "Walk the far path",
    "description": "The first explicit scene (LO, question 8): a couple in the bushes, strangers. Good Girl: she walks into them and runs. Curious: she watches, then touches herself. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("sound", "The far path", [
            P("The far path behind the rhododendrons is empty and quiet. Then it isn't: a sound off to the left, through the leaves, low and rhythmic."),
            G(cond(CURIOUS), T("You know exactly what that is. You could leave. You don't want to.")),
        ], [
            go("Step off the path to look.", node="run", mins=3, cond_=cond(trait("corruption", "lt", 20))),
            go("Stay and watch.", node="watch", mins=5, cond_=cond(CURIOUS)),
            go("Walk the other way.", node="away", mins=2),
        ]),
        node("run", "Run", [P(RUN_SEEN),
            VID("a couple having sex against a log in the bushes of a park, the man looks up", "couple fucking in park bushes caught", "outdoor sex in park man looks up", pool_dir="sex/park_couple_run_t5")],
            [go("Keep walking.", loc="park", mins=15, flags=[fset("saw_the_couple")])]),
        node("watch", "Watch", [P("Behind you on the path a jogger thuds past. You hold your breath until he's gone."), P(WATCH),
            VID("seen through leaves, a man fucking a woman bent against a tree in a park", "voyeur watching couple fuck in park", "hidden in bushes watching outdoor sex", pool_dir="sex/park_couple_watch_t5")],
            [go("Leave before they see.", loc="park", mins=10, eff=[capped("corruption", 1, CAP_CUR)], flags=[fset("saw_the_couple")]),
             go("Touch yourself while you watch.", node="touch", mins=5)]),
        node("touch", "With him", [P("A dog barks somewhere along the path, and you freeze with your hand on your belly. Nobody comes."), P(TOUCH),
            VID("a girl hidden in bushes touching herself while watching a couple have sex against a tree", "girl masturbating watching couple outdoors", "voyeur girl fingers herself in park", pool_dir="sex/park_couple_touch_t5")],
            [go("Slip away.", loc="park", mins=10, eff=[capped("corruption", 2, CAP_CUR)], flags=[fset("saw_the_couple")])]),
        node("away", "The other way", [P("You turn round and walk the other way, fast, and don't look back. Your face is burning anyway.")], [go("Back to the pond.", loc="park", mins=10)]),
    ]})

HIDDEN = ("Zoe drags you off the path into the hollow behind the rhododendrons. Joggers pound past a few metres away. She shoves you against a tree and kisses you hard, both of you still panting from the run. \"Quiet, babe,\" she breathes. Her hand slides down inside, flat on your skin, and finds you wet. Her fingers start slow. You grab her ass and pull her in. Her thumb finds your nipple and rubs. Footsteps crunch past, close enough to touch, but Zoe doesn't stop. Her fingers go fast, deep, until your hips buck into her hand. Your orgasm hits and your knees give out. Zoe pins you to the bark with her whole body, her mouth on yours to swallow every moan.")
out.append({
    "id": "park_hidden", "name": "Off the path with Zoe",
    "description": "After the run with Zoe, weekend mornings (park_hidden): a hollow off the path, Zoe's hand, nobody sees. Bold, after Zoe A 3. Once a day.",
    "trigger": {"location": "park", "requires_npc": Z, "is_repeatable": True, "priority": 5, "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [5, 6], "start_time": "08:00", "end_time": "10:00"}],
                "conditions": cond(BOLD, trait("zoe_step", "gte", 3))},
    "nodes": [
        node("pull", "After the run", [P("Zoe jogs to a stop beside you, pink and breathless, and grabs your wrist."), D(Z, "Come here. I know a place.")],
             [go("Follow her.", node="hidden", mins=5), go("\"Not here, Zo.\"", node="no", mins=1)]),
        node("hidden", "The hollow", [P("A man walking his dog slows on the path above the hollow, looks your way, and walks on."), P(HIDDEN),
            VID("two girls in running clothes hidden in bushes, one with her hand down the other's leggings, kissing against a tree", "girl fingers girlfriend in park bushes", "lesbian hidden in park hand down leggings", pool_dir="sex/park_hidden_t5")],
            [go("Back to the path.", node="after", mins=15, eff=[capped("corruption", 1, CAP_BOLD)])]),
        node("after", "Back on the path", [D(Z, "Same time next weekend. Don't be late."), P("She jogs off backwards, grinning, and doesn't fix her hair.")], [go("Go.", loc="park", mins=2)]),
        node("no", "Not here", [D(Z, "Your loss, babe."), P("She laughs and runs off ahead, looking back over her shoulder every few strides.")], [go("Go.", loc="park", mins=5, flags=[fset("park_cool_zoe")])]),
    ]})

# ═════════════ TOUCHING HERSELF (from Curious; DECISIONS 13) ═════════════
BED = ("Your door is shut, but someone's TV mutters downstairs. Under the sheet, you slide a hand up and squeeze your tits. You pinch a nipple until it goes hard between your fingers, and the jolt runs straight down to your clit. So you follow it down. You're wet already, and you want to know how much more you can take. Two fingers circle your clit, slow, until your hips start to lift. Then faster. Your heels dig in, your ass comes off the mattress, chasing your hand. The walls are thin, so you bite your lip hard to keep quiet. You come with your thighs clamped on your wrist, legs shaking, fingers still pressed to your clit.")
SHOWER = ("You lock the door and step naked under the hot water. Footsteps cross the hall outside and keep going. The water runs down your tits and drips off your nipples. You soap them slowly, thumbs circling until they stand hard and ache. Your hand slides down your belly and between your legs. You are slick there, and not from the shower. Two fingers find your clit and press. The water drums on your back and your ass. You lean one hand on the tile and rub faster. Your hips jerk against your fingers. The orgasm hits hard, and you bite down on the moan. Your knees go weak, and you hold the tile while your clit throbs under your hand.")
TOILET = ("You lock the stall and lean back against the cold wall. Your hand slides inside, and you are already wet. Two fingers find your clit and press. Your other hand clamps over your mouth. A tap runs a metre away. A girl laughs at the mirror. You rock your hips against your fingers, slow, so the latch doesn't rattle. Your nipples go hard and tight. The door bangs, and you freeze with your fingers on your clit. Nobody knocks. So you keep going, faster, while the hand dryer roars. The moan stays trapped under your palm. The orgasm hits without a sound, and your thighs clamp shut on your hand.")
for cid, loc, name, text, back, extra in [
        ("touch_bed", "home_ella_room", "Touch yourself", BED, "Lie still.", []),
        ("touch_shower", "home_bathroom", "Touch yourself in the shower", SHOWER, "Get dressed.", [{"type": "npc_at_location", "location_id": "home_bathroom", "npc_id": R, "operator": "is_absent"}]),
        ("touch_toilet", "college_womens_toilet", "Touch yourself in a stall", TOILET, "Get dressed.", [])]:
    out.append({
        "id": cid, "name": name,
        "description": f"Touching herself ({loc}): from Curious, once a day; Corruption +1 until past Curious.",
        "trigger": {"location": loc, "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1,
                    "conditions": cond(CURIOUS, *extra)},
        "nodes": [node("touch", name, [P(text),
            VID(f"a girl touching herself alone ({loc.replace('_', ' ')})", "girl masturbating alone", f"solo girl {loc.split('_')[-1]} orgasm", pool_dir=f"sex/{cid}_t5")],
            [go(back, loc=loc, mins=20, eff=[capped("corruption", 1, CAP_CUR)])])]})

# ═════════════ THE STAIRS (wardrobe event): a short skirt or no panties, someone below ═════════════
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NO_PANTIES = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}
out.append({
    "id": "wardrobe_event_stairs", "name": "Take the stairs slowly",
    "description": "The stairs event (wardrobe pool): a short skirt or no panties, and someone below. Exhibitionism +1, once a day.",
    "trigger": {"location": "home_hall", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1,
                "conditions": cond(SKIRT, trait("exhibitionism", "gte", 20))},
    "nodes": [node("stairs", "The stairs", [
        P("You go up the stairs slowly, one hand on the rail."),
        G(cond({"type": "npc_at_location", "location_id": "home_living_room", "npc_id": M, "operator": "is_present"}),
          P("Mark comes out of the living room into the hall below just as you reach the top. He stops. He looks up the stairs, straight up your skirt, and doesn't look away until you're on the landing.")),
        G(cond({"type": "npc_at_location", "location_id": "home_ryan_room", "npc_id": R, "operator": "is_present"}),
          P("Ryan is coming down as you go up. You pass on the narrow stairs, and he has to flatten himself to the wall, and his eyes go down your legs on the way past.")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": L, "operator": "is_present"}),
          D(L, "Is that for college or for a guy?")),
        G(cond(SKIRT, NO_PANTIES), P("There's nothing under the skirt. Anyone at the bottom of these stairs gets everything, and you climb slower.")),
    ], [go("Keep climbing.", loc="home_hall", mins=2, eff=[capped("exhibitionism", 1, CAP_BOLD)])])]})

text = "# ── the pool and system scenes: parties, the park, touching herself, the stairs ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("pools:", len(out), "canvases")
