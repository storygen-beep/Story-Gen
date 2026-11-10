"""Zoe — her meeting, steps 1-4 (Zoe A 1-4; step 1 = Jake B 1), her hubs, the meeting nudge.
Source: sheets/scenes/zoe_0*.md, people/npc_zoe.md. Explicit screens pasted as signed."""
from canv import *
import doors   # DECISIONS 224: a scene with a person opens from their portrait
from tomlw import tod, wd
from home_items import placeholder
from sheetbeats import beat

Z = "npc_zoe"
J = "npc_jake"
out = []

def done(n):
    return fset(f"zoe_0{n}_done")

PARTY_DRESS = {"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "equipped"}
PLAIN_BRA = {"type": "clothing_item", "item_id": "plain_bra", "operator": "equipped"}
SPORTS_BRA = {"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}
CURIOUS = trait("corruption", "gte", 20)


def by_level(meter, **lines):
    """Her line by band (register.md "One event, several levels"): keys good_girl, curious, bold, hungry. Write only the
    bands the scene can reach; the lowest one written also catches anything under it, so the screen is never silent."""
    bands = {"good_girl": (None, 20), "curious": (20, 40), "bold": (40, 60), "hungry": (60, None)}
    written = [k for k in bands if k in lines]
    rows = []
    for k in written:
        lo, hi = bands[k]
        items = ([trait(meter, "gte", lo)] if lo is not None and k != written[0] else []) + ([trait(meter, "lt", hi)] if hi is not None else [])
        rows.append(G(cond(*items), lines[k]))
    return rows


# ── her meeting on the quad ──
out.append({
    "id": "zoe_00_quad_meeting", "name": "The girl from Biology",
    "description": "Meets Zoe on the quad, the first time she's there in Zoe's hours. Sets zoe_met (opens her apartment) and zoe_number. Both answers meet her.",
    "trigger": {"location": "quad", "requires_npc": Z, "is_repeatable": False, "priority": 10, "is_active": True,
                "schedules": [{"weekdays": [1, 3, 4], "start_time": "14:30", "end_time": "18:00"}],
                "conditions": cond(flag("opening_done"), flag("zoe_met", False))},
    "nodes": [
        node("wave", "On the grass", [
            IMG("scenes/zoe_00_quad.jpg", "a laughing college girl lying on the grass of a campus quad waving someone over, sunglasses, afternoon",
                "college girl lying on grass quad waving", "girl on campus lawn sunglasses laughing"),
            # reader batch 5 (pass 3): "your Biology class" only once she has sat one (meet_bio sets bio_ta_met)
            G(cond(flag("bio_ta_met")),
              P("The girl from your Biology class, the one who whispers through the slides, is lying on the grass on her elbows with her sunglasses pushed up in her hair. She sees you and waves both arms over her head like you're a plane she's landing."),
              WHO("Hey. You. Biology. Sit.")),
            G(cond(flag("bio_ta_met", False)),
              P("A girl is lying on the grass on her elbows with her sunglasses pushed up in her hair. She sees you and waves both arms over her head like you're a plane she's landing."),
              WHO("Hey. You. You're on my Biology list and you never come. Sit.")),
        ], [
            go("Sit with her.", node="zoe", mins=5),
            go("\"Can't, I've got a shift.\"", node="later", mins=2, cond_=cond(flag("cafe_job"))),
            go("\"Can't, I've got class.\"", node="later", mins=2, cond_=cond(flag("cafe_job", False))),
        ]),
        node("zoe", "Zoe", [
            P("You sit. She rolls over and puts her head straight in your lap like you've known each other for years, and looks up at you upside down."),
            G(cond(flag("bio_ta_met")), D(Z, "Zoe. You're the one who sits at the back and pretends not to know the answers. I like you. Do you party?")),
            G(cond(flag("bio_ta_met", False)), D(Z, "Zoe. You're the one who signed up for Biology and never shows. I like you. Do you party?")),
            P("She talks fast, about everything, Biology and the TA who blushes and a guy on the team with an ass you could bounce coins off. She looks at you a beat too long while she says it, and laughs."),
            G(cond(flag("college_for_fun")), D(Z, "You look like fun. You look like you've been waiting for someone to ask.")),
        ], [go("\"Party?\"", node="friday", mins=10, flags=[fset("zoe_met")])]),
        node("friday", "Friday", [
            D(Z, "Friday. My place. Wear something short."),
            P("She takes your phone out of your hand without asking and types her number into it, and her address, and a row of devil emojis."),
            D(Z, "Or don't, and I'll lend you something shorter."),
            T("You've known her ten minutes. You're going."),
        ], [go("\"Friday.\"", loc="quad", mins=5, flags=[fset("zoe_number")])]),
        node("later", "Run, then", [
            D(Z, "Fine, run! Friday, my place!"),
            P("She shouts the address after you across the whole quad. Three people turn round, but she doesn't care. You've got her name by the time you reach the gate, because she shouted that too: Zoe."),
        ], [go("Wave without looking back.", loc="campus", mins=2, flags=[fset("zoe_met"), fset("zoe_number")])]),   # pass 3 D39 (R7)
    ]})

# ── step 1 · Zoe A 1 = Jake B 1 · the first party (one canvas, both counters) ──
DARE_NO = ["Not tonight, Zo."]
out.append({
    "id": "zoe_01_first_party", "name": "Your first party",
    "description": "Zoe step 1 = Jake step 1 (one canvas, it sets both). Zoe's dress, her first dare, and a guy who picks her out: Jake. Sets party_went, jake_met, jake_number.",
    "trigger": step_trigger(Z, 1),
    "nodes": [
        node("dress", "Zoe's bedroom", [
            P("Zoe drags you straight past the music into her bedroom and shuts the door. She pulls a black dress off the back of it, short, tight, straps like string."),
            D(Z, "Put it on. No, here. I want to see."),
        # scene reader 2026-11-04 (the written no): her no to changing in front of Zoe. Both ways she wears it; neither pays.
        ], [go("Change in front of her.", node="change", mins=2), go("\"Turn around, Zo.\"", node="change_no", mins=2)]),
        node("change", "In front of her", [
            P("You change in front of her. She sits on the bed with her chin in her hands and doesn't look away once, not while you strip, not when you wriggle the dress down over your hips."),
            D(Z, "Turn around. Let me see."),
            *by_level("exhibitionism",
                      good_girl=T("Nobody at home would know you in this. You want to pull the hem down."),
                      curious=T("She really is looking. You wonder what she sees."),
                      bold=T("Let her look. You turn around slowly, so she gets all of it."),
                      hungry=T("You want more eyes than hers on you in this. You want the whole party looking at your ass.")),
        ], [go("\"Zoe! Eyes up here.\"", node="party", mins=8,
               wardrobe=[{"action": "add", "item_id": "zoe_party_dress"}, {"action": "equip", "item_id": "zoe_party_dress"}])]),
        node("change_no", "Turn around", [
            ME("Turn around, Zo. I mean it."),
            D(Z, "Boo. Fine. My eyes are shut."),
            P("They aren't. You turn your back on her and change facing the wall, fast, and pull the dress down over your hips before she can say anything."),
            D(Z, "Prude. You still look great, babe."),
        ], [go("\"You looked.\"", node="party", mins=8,
               wardrobe=[{"action": "add", "item_id": "zoe_party_dress"}, {"action": "equip", "item_id": "zoe_party_dress"}])]),
        node("party", "The party", [
            IMG("scenes/zoe_01_party.jpg", "a crowded apartment party, fairy lights, red cups, a girl in a short black dress being pulled through the crowd by her friend",
                "apartment party fairy lights crowd college", "girl in short black dress house party"),
            P("The flat is packed: half of campus, the bass coming up through the floor, red cups on every surface. Zoe walks you through it with her arm round your waist like she's showing you off, and people look. At the dress. At you in it."),
            G(cond(flag("college_for_grades")), D(Z, "Grades, you told your mom? Babe. Tonight you're majoring in this.")),
            G(cond(flag("college_for_fun")), D(Z, "You said fun. This is fun. Drink.")),
            G(cond(flag("college_for_freedom")), D(Z, "Freedom, babe. No mom, no step-dad, no rules. Breathe it in.")),
            P("She puts her head on your shoulder on the couch and says it into your ear, like a secret:"),
            D(Z, "Kiss someone. Or don't, and I'll keep asking."),
        ], [
            # a no pays her nothing (H5, DECISIONS 124), and it is not her step 1 (LO 2026-11-03, DECISIONS 133):
            # it still meets Jake; she asks again on a later Friday (zoe_01b_kiss_again)
            go("\"Not tonight, Zo.\"", node="no_dare", mins=5, flags=[fset("party_went"), fset("zoe_kiss_refused")], eff=[add("zoe_refused", 1, clamp=False)]),
            # a kiss on the couch with the party whooping: the doing pays Corruption (it is gated on it) and being seen
            # pays Exhibitionism (the-heat-ladder.md "Two meters, one act"; DECISIONS 103; pass 3 A48)
            go("Kiss Zoe.", node="kiss_zoe", mins=5, cond_=cond(CURIOUS), flags=[fset("party_went")], eff=[add("corruption", 3, cap=39), add("exhibitionism", 3, cap=79)]),
            go("Kiss the guy who's staring.", node="jake", mins=5, cond_=cond(CURIOUS), flags=[fset("party_went"), fset("jake_kissed")], eff=[add("corruption", 3, cap=39), add("exhibitionism", 3, cap=79)]),
        ]),
        node("no_dare", "Not tonight", [D(Z, "Boring. Fine. I'll keep asking."), P("She steals your drink instead and dances off into the crowd. Across the room a guy in a team jacket is watching you. Not Zoe. You.")],
             [go("Look back at him.", node="jake", mins=15)]),
        node("kiss_zoe", "Zoe", [
            P("You turn your head and kiss her, right there on the couch. She makes a surprised little sound against your mouth, then kisses you back, harder, one hand in your hair and the other on your thigh, under the hem of her own dress. Somebody whoops. Her hand stops there, and she pulls back with her eyes huge."),
            D(Z, "Oh. Okay. Okay. Not on the couch, babe. Not yet."),
            P("Across the room a guy in a team jacket is watching you. Not Zoe. You."),
        ], [go("Look back at him.", node="jake", mins=5)]),
        node("jake", "Across the room", [
            P("He's been watching you since you came in: tall, a team jacket, a beer he isn't drinking, standing with three guys who are all talking to each other while he looks at you. When he sees you see him, he doesn't look away. He comes over."),
            G(cond(flag("jake_kissed")), P("You meet him halfway and kiss him before he can say anything. He tastes of beer. His hand goes to the small of your back like it belongs there.")),
            ME("You've been staring since I came in."),
            D(J, "Wasn't planning to stop. I'm Jake."),
            G(cond(PARTY_DRESS), P("His eyes go down your legs in Zoe's dress and stay there.")),
            P("Zoe sits on the arm of the couch watching the two of you with her drink and an unreadable face."),
        ], [
            go("\"Here's my number.\"", loc="zoe_apartment", mins=30, consumes=True, cond_=cond(flag("zoe_kiss_refused", False)),
               eff=[setv("zoe_step", 1), setv("jake_step", 1)], flags=[done(1), fset("jake_met"), fset("jake_number")]),
            go("\"Here's my number.\"", loc="zoe_apartment", mins=30, consumes=True, cond_=cond(flag("zoe_kiss_refused")),
               eff=[setv("jake_step", 1)], flags=[fset("jake_met"), fset("jake_number")]),
            go("\"Not tonight.\"", node="jake_no", mins=2),
        ]),
        node("jake_no", "Not tonight", [D(J, "Wasn't planning to give up."), P("He grins and goes back to his team, but he looks over every time you laugh.")],
             [go("Back to the party.", loc="zoe_apartment", mins=20, consumes=True, cond_=cond(flag("zoe_kiss_refused", False)),
                 eff=[setv("zoe_step", 1), setv("jake_step", 1)], flags=[done(1), fset("jake_met")]),
              go("Back to the party.", loc="zoe_apartment", mins=20, consumes=True, cond_=cond(flag("zoe_kiss_refused")),
                 eff=[setv("jake_step", 1)], flags=[fset("jake_met")])]),
    ]})

# ── step 1 again · her kiss dare, a later Friday, after a no (LO 2026-11-03: "I think dare refusal shouldn't be
#    counted as done"; DECISIONS 133). Only from Curious: the kiss is Curious, so below it every yes is hidden. ──
AT_PARTY_Z = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}
KISS_DONE = dict(eff=[setv("zoe_step", 1)], flags=[done(1)])
out.append({
    "id": "zoe_01b_kiss_again", "name": "Same dare",
    "description": "Zoe step 1 after a no at her first party: a later Friday party, from Curious, she asks the kiss again. A yes is her step 1; a no parks it a week.",
    "trigger": {"location": "zoe_apartment", "npc": Z, "requires_npc": Z, "is_repeatable": False, "priority": 10, "is_active": True,
                "consume_on": "exit", "retry_after_days": 7,
                "schedules": [{"weekdays": [DAYS["Fri"]], "start_time": "19:00", "end_time": "23:00"}],
                "conditions": cond(trait("zoe_step", "eq", 0), flag("zoe_kiss_refused"), CURIOUS, AT_PARTY_Z,
                                   {"type": "hours_since_flag", "subject": "player", "flag_key": "zoe_kiss_refused", "operator": "gte", "value": 24})},
    "nodes": [
        node("ask", "Same dare", [
            P("Zoe finds you on the couch, drops into your lap sideways and hooks an arm round your neck."),
            D(Z, "You chickened out on me last time. Same dare. Kiss someone. I told you I'd keep asking."),
            # zoe_refused counts her nos; at the second no to the kiss Zoe says she's counting (true: only kiss nos come before
            # step 1). Exactly 2: at 3 and up "twice" is a miscount (scene reader, 2026-11-04)
            G(cond(trait("zoe_refused", "eq", 2)), D(Z, "That's twice you've said no, babe. I'm counting.")),
        ], [
            go("Kiss Zoe.", node="kiss_zoe", mins=5, eff=[add("corruption", 3, cap=39), add("exhibitionism", 3, cap=79)]),   # pass 3 A48: both meters
            go("Kiss the guy by the speakers.", node="kiss_guy", mins=5, eff=[add("corruption", 3, cap=39), add("exhibitionism", 3, cap=79)]),
            go("\"Not tonight, Zo.\"", node="no", mins=2),
        ]),
        node("kiss_zoe", "Zoe", [
            P("You turn in her lap and kiss her. She's ready for it this time. Her mouth opens under yours, her tongue finds yours, and her hand goes straight up the inside of your thigh, high, and stays there. Somebody whoops. She pulls back first, breathing hard, her eyes on your mouth."),
            D(Z, "Okay. Okay. Worth the wait, babe."),
            # scene reader 2026-11-04 (hook, low heat): the not-yet, and her next dare, Friday (zoe_02)
            P("You reach for her again, and she catches your wrist and puts your hand back on your own knee."),
            D(Z, "Not yet. That's all you get tonight. Next Friday I've got a worse one."),
        ], [go("Back to the party.", loc="zoe_apartment", mins=15, consumes=True, **KISS_DONE)]),
        node("kiss_guy", "The guy by the speakers", [
            P("You get up, cross the room to a guy by the speakers you've never seen before, and kiss him. He's surprised for half a second. Then his hands are on your hips, pulling you into him, his tongue's in your mouth, and one hand slides down onto your ass and squeezes. Somebody whoops. When you let him go he just stares at you."),
            D(Z, "Babe! Okay! Told you I'd keep asking."),
            # scene reader 2026-11-04 (hook, low heat): the same not-yet, from his side
            P("She pulls you off him by the wrist before his hand gets any further."),
            D(Z, "That's enough of your ass for one guy. Next Friday I'm picking something harder."),
        ], [go("Back to the party.", loc="zoe_apartment", mins=15, consumes=True, **KISS_DONE)]),
        no_node("no", [D(Z, "Boo. Next Friday, then. I'm not giving up on you."), P("She slides off your lap and goes to dance.")],
                "zoe_apartment", 7, eff=[add("zoe_refused", 1, clamp=False)], label="Let her go and dance."),   # pass 3 D39 (R7)
    ]})

# ── step 2 · Zoe A 2 · bra through the sleeve ──
# One pool, one place (2026-11-04): zoe_dares keeps low_do; each copy of this balcony has its own kiss on the zoe_02 sheet,
# worded by what she has on top (pools.dare_by_top is the shape; chain_by_sentence prints shared sentences once).
_TOP_ONLY = {"type": "clothing_slot", "slot": "top", "operator": "equipped"}
_NO_TOP = {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}
_NO_DRESS = {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}


def kiss_by_top(key, on_top, on_bra, on_skin):
    text = beat("zoe_02_bra_through_the_sleeve", key)
    assert on_top in text, key
    return chain_by_sentence([
        (cond(_TOP_ONLY, _NO_DRESS), text),
        *[(cond({"type": "clothing_item", "item_id": d, "operator": "equipped"}), text.replace("your top", "your dress")) for d in DRESSES],
        (cond(_NO_TOP, _NO_DRESS, {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), text.replace(on_top, on_bra)),
        (cond(_NO_TOP, _NO_DRESS, {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), text.replace(on_top, on_skin)),
        (cond({"type": "clothing_slot", "slot": "dress", "operator": "equipped"}), text.replace("your top", "your clothes"))])   # any other dress-slot item


out.append({
    "id": "zoe_02_bra_through_the_sleeve", "name": "Through the sleeve",
    "description": "Zoe step 2 (Zoe A 2): a dress dare on the balcony, the room behind the glass. Her bra comes off. Sets party_house_invite (opens the party house).",
    "trigger": step_trigger(Z, 2, retry_days=7),
    "nodes": [
        node("balcony", "The balcony", [
            # her no on this balcony is remembered (DECISIONS 133; step 1's no has its own re-ask, zoe_01b_kiss_again)
            G(cond(flag("zoe_balcony_refused")), D(Z, "You chickened out on me last time. Not tonight, babe.")),
            # Iteration 002, part 8 (reader): the strap only when there is one.
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}),
              P("Zoe pulls you out onto the balcony, away from the noise. The glass door is behind you and the whole party is on the other side of it. She leans on the rail and looks at the strap on your shoulder and doesn't look anywhere else.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
              P("Zoe pulls you out onto the balcony, away from the noise. The glass door is behind you and the whole party is on the other side of it. She leans on the rail and looks at your shoulder and doesn't look anywhere else.")),
            D(Z, "Bra off. Don't take anything else off. That's the dare."),
        ], [
            go("\"Watch me.\"", node="sleeve", mins=5,
               cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, trait("exhibitionism", "gte", 20))),
            go("\"I'm not wearing one, Zo.\"", node="already", mins=2,
               cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, trait("exhibitionism", "gte", 20))),
            go("\"Dare me something else.\"", node="kiss", mins=2,
               cond_=cond(trait("corruption", "gte", 20), flag("cocky_guy_met"),
                          {"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": "npc_cocky_guy", "operator": "is_present"})),
            go("\"Not tonight, Zo.\"", node="no", mins=2),
        ]),
        node("sleeve", "Through the sleeve", [
            # false lines a3 #27 (DECISIONS 129): a sports bra doesn't unhook, so it gets its own line
            G(cond(PARTY_DRESS, PLAIN_BRA), P("You reach up under Zoe's dress and unhook it at the back, and work one strap down your arm and through the armhole of the dress, then the other.")),
            # scene reader b03 (2026-11-03): a sleeve only when there is a top or a dress; in a bra and nothing over it, no sleeve
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}, PLAIN_BRA, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}), P("You reach up the back and unhook it, and work one strap down your arm and out through your sleeve, then the other.")),
            G(cond({"type": "clothing_slot", "slot": "dress", "operator": "equipped"}, {"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}, PLAIN_BRA), P("You reach up the back and unhook it, and work one strap down your arm and out through the armhole, then the other.")),
            G(cond({"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}, PLAIN_BRA), P("There's no sleeve to work it through. You reach back, unhook it in one go, and peel it off your tits with the whole party on the other side of the glass.")),
            # scene reader 2026-11-04: a sports bra doesn't unhook
            G(cond({"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}, SPORTS_BRA), P("There's no sleeve to work it through. You drag the sports bra up over your head and off your tits, with the whole party on the other side of the glass.")),
            G(cond(PARTY_DRESS, SPORTS_BRA), P("You reach up under Zoe's dress and drag the sports bra up, and work it off one arm at a time through the armholes of the dress.")),
            G(cond({"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, SPORTS_BRA), P("You drag the sports bra up off your tits under your top, and work it off one arm at a time, out through your sleeves.")),
            G(cond({"type": "clothing_slot", "slot": "dress", "operator": "equipped"}, {"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}, SPORTS_BRA), P("You reach up under the dress and drag the sports bra up off your tits, and work it off one arm at a time through the armholes.")),
            # reader a3 older: Zoe's dress has armholes, not sleeves
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}), P("It takes forever. Zoe watches every second. When it slides out of your sleeve your nipples are hard in the cold air, two points anyone could see, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.")),
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}), P("It takes forever. Zoe watches every second. When it slides out through the armhole your nipples are hard in the cold air, two points anyone could see through the cloth, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.")),
            G(cond({"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}), P("Your tits are bare on the balcony, your nipples hard in the cold air, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.")),
            G(cond(PARTY_DRESS), P("It takes forever. Zoe watches every second. When it slides out through the armhole your nipples are hard in the cold air, two points anyone could see under her dress, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles.")),
            # pass 3 B4: the balcony talks
            D(Z, "Slower. Make the window wait for it."), ME("Zo, that guy is staring right at me."), D(Z, "I know. Isn't it the best?"),
        # reader a3, seen by the readers (DECISIONS 131): Zoe doesn't have it yet when the button shows
        # pass 4 E94: the guy at the window whistles, so the party talks (campus_talk, like the party's dares)
        ], [go("Ask for it back.", node="mine", mins=3, eff=[add("exhibitionism", 3, cap=79), add("campus_talk", 1, clamp=False)], flags=[fset("zoe_has_bra")],
               wardrobe=[{"action": "unequip", "item_id": "plain_bra"}, {"action": "unequip", "item_id": "sports_bra"}])]),
        node("already", "Already", [D(Z, "You're— oh my god. All night? Babe."), P("She looks at your chest for a long second, then laughs and leans on the rail next to you, close, her shoulder on your bare arm.")],
             [go("Laugh with her.", node="mine2", mins=3, eff=[add("exhibitionism", 3, cap=79)])]),
        node("mine2", "Saturday", [D(Z, "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people."), ME("Some people?"), D(Z, "Some. Bring nothing to wear."), T("She keeps looking at your chest. She keeps not asking.")],
             [go("\"Saturday.\"", loc="zoe_apartment", mins=5, consumes=True, eff=[setv("zoe_step", 2)], flags=[done(2), fset("party_house_invite")])]),
        no_node("no", [D(Z, "Boo. Fine. Next Friday I'm daring you again."), P("She goes back inside and leaves the balcony door open behind her.")], "zoe_apartment", 7,
                label="Stay out on the balcony a minute.",
                eff=[add("zoe_refused", 1, clamp=False)], flags=[fset("zoe_balcony_refused")]),
        node("kiss", "Kiss him", [
            D(Z, "Fine. Kiss the cocky guy. Properly."),
            # scene reader b03 (2026-11-03): worded by what she has on top
            *kiss_by_top("kiss", "Your nipples harden against your top, and he groans when he feels them.",
                         "Your nipples harden through your bra, and he groans when he feels them.",
                         "Your bare nipples harden against his shirt, and he groans when he feels them."),
            # pass 3 B37: its own asset, not zoe_dares' low_do pool (one asset, one block)
            VID("a girl kissing a guy hard at a party, his hands on her ass, people cheering", "girl kisses guy at party dare", "dare kiss party hands on ass", pool_dir="sex/zoe_02_kiss_t3"),
            D("npc_cocky_guy", "Zoe. I owe you one."), D(Z, "You owe her, not me. Hands off now."),
            # scene reader 2026-11-04 (her voice): "Just a dare" is pushback, so it stops at Bold. Out of the beat, into its own thought.
            *by_level("corruption",
                      curious=T("Just a dare, you tell yourself."),
                      bold=T("Just a dare, you tell yourself. You don't believe it."),
                      hungry=T("Just a dare? You'd have kissed him without one, and you're wet to prove it.")),
        # pass 4 E94: the whole corner whoops at the kiss, so the party talks (campus_talk)
        ], [go("\"What's next, Zo?\"", node="saturday", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 3, "cap": 39},
                                                              add("campus_talk", 1, clamp=False)])]),
        node("saturday", "Saturday", [
            P("Zoe pulls you back out onto the balcony, flushed."),
            D(Z, "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people."),
            ME("Is he one of the people?"), D(Z, "Only if you want him to be, babe."),
        ], [go("\"Saturday.\"", loc="zoe_apartment", mins=5, consumes=True,
               eff=[setv("zoe_step", 2)], flags=[done(2), fset("party_house_invite")])]),
        node("mine", "Mine now", [
            P("Zoe takes it out of your hand and tucks it in her back pocket."),
            D(Z, "Nope. Mine now."),
            P("Then she leans on the rail next to you, close, her shoulder against your bare arm, and says it quieter."),
            D(Z, "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people."),
            ME("And my bra?"), D(Z, "Stays with me. You won't need it Saturday."),
            T("She keeps looking at your chest. She keeps not asking."),
        ], [go("\"Saturday.\"", loc="zoe_apartment", mins=5, consumes=True,
               eff=[setv("zoe_step", 2)], flags=[done(2), fset("party_house_invite")])]),
    ]})

# ── step 3 · Zoe A 3 · the hot tub (the voice sample; every screen as signed) ──
HOME_AT_3 = [(("20:00", "21:00"), 400), (("21:00", "22:00"), 340), (("22:00", "23:00"), 280), (("23:00", "00:00"), 220),
             (("00:00", "20:00"), 160)]   # past midnight: the catch-all (sweep A4-01)
# truth pass (2026-11-03): the scene runs 28 minutes to "Across the bubbles, Zoe is still looking at you", and her
# party-house row ends at midnight, so the step opens to 23:30 (the ledger says so too since 2026-11-03)
_t3 = step_trigger(Z, 3, bind_npc=False, retry_days=7)
assert [(s_["start_time"], s_["end_time"]) for s_ in _t3["schedules"]] == [("20:00", "23:30")]
out.append({
    "id": "zoe_03_hot_tub", "name": "The hot tub",
    "description": "Zoe step 3 (Zoe A 3), the voice sample: the party house hot tub, her friends go in first; topless for Zoe alone and she kisses her. Home at three; Ryan at his door.",
    "trigger": _t3,
    "nodes": [
        node("tub", "The hot tub", [
            P("Zoe drags you into the hot tub on the back deck, laughing. Steam rolls off the water. Music thumps through the glass. Three of her friends are already in, drinks on the rim. \"Make room, babe's here.\" She doesn't need room. She sits right against you, her knee pressed to yours under the water. When you talk, she watches your mouth. All term she has dared you instead of asking, but you know what she wants. \"Your tits are floating, babe,\" she says, grinning. Your face goes hot, and it isn't the water. One of her friends stands up, restless. \"Going in for more drinks.\""),
        ], [go("Stay in the water.", node="alone", mins=15,
               wardrobe=[REMEMBER] + [{"action": "unequip", "item_id": g} for g in ("tshirt", "thin_top", "low_top", "gym_tank", "jeans", "leggings", "track_pants", "gym_shorts", "sheer_leggings", "sleep_shorts",
                                                                       "short_skirt", "zoe_party_dress", "laura_blue_dress", "sneakers", "crop_top", "bodycon_dress", "micro_shorts", "plunge_dress",
                                                                       "split_skirt", "sequin_dress", "backless_dress")])]),
        node("alone", "Just us", [
            # scene reader 2026-11-04: "Take it off" only with a bra on (Zoe may have kept it, zoe_has_bra); "I want to see
            # your tits" not after walkin_tub_zoe, when she has already sat naked against her (zoe_in_the_tub)
            P("The door slides shut behind her friends. Now it is just the two of you in the steam. Zoe goes quiet, and Zoe is never quiet."),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), P("\"Take it off, babe,\" she says, low.")),
            P("\"Just for me. Nobody else is here.\" Her eyes drop to your chest and stay there. She bites her lip. Her breath comes short across the water."),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, flag("zoe_in_the_tub", False)), P("\"Everything on you is wet anyway. I can see your nipples, babe. I want to see your tits.\"")),
            P("Your heart pounds, because you want her to keep looking. Your hands drift up and stop. She waits for your answer."),
            *by_level("exhibitionism",
                      bold=T("She wants this. Make her wait one second longer."),
                      hungry=T("You want your tits out for her. You want it so badly your hands are shaking.")),
        ], [
            go("Take your bra off.", node="kiss", mins=3, cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}),
               wardrobe=[{"action": "unequip", "item_id": "plain_bra"}, {"action": "unequip", "item_id": "sports_bra"}]),
            go("Let her look.", node="kiss_bare", mins=3, cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"})),
            go("\"Not tonight, Zo.\"", node="home_no", mins=60, wardrobe=DRESS_BACK),
        ]),
        node("kiss", "Topless", [
            P("You get your bra off and toss it on the deck. The steam rolls over your bare tits. The night air is cold on them, so your nipples go hard above the water. Zoe stares at them. \"Babe,\" she breathes. \"Look at you.\" You grab the back of her neck and pull her in. You kiss her hard, open-mouthed, until she moans into you. Her tits press flat against yours. Her nipples drag across your nipples, hard and wet. Her thigh slides between your thighs under the water. It presses up, slow and firm. Her breath catches. Your hands run down her slick back to her ass. You grab it with both hands and pull her tits tight against yours."),
            VID("two topless girls kissing in a steaming hot tub at night, breasts pressed together", "two girls topless kissing hot tub night", "lesbian kiss hot tub steam topless", file="sex/zoe_03_kiss_t5.webm"),
        ], [go("Hold her.", node="asked", mins=10, eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 3, "cap": 79}, {"targetType": "player", "trait": "corruption", "op": "add", "value": 3, "cap": 79}])]),
        # No bra to take off: the sheet's beat names unhooking it, so this screen is a placeholder (iteration 002).
        node("kiss_bare", "Topless", [placeholder("sheets/scenes/zoe_03_hot_tub.md:44", "Zoe A 3, the kiss when she wore no bra into the tub")],
             [go("Hold her.", node="asked", mins=10, eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 3, "cap": 79}, {"targetType": "player", "trait": "corruption", "op": "add", "value": 3, "cap": 79}])]),
        node("asked", "You could've asked", [
            P("Zoe pulls back, flushed and breathless, and laughs. \"Took you long enough, babe.\" \"You could've asked,\" you tell her. She goes quiet. She opens her mouth, but she doesn't answer that. Not yet. All term she dared you instead of asking for this. You liked every single dare. The sliding door bangs open. Her friends spill back out, shrieking. You sink to your shoulders in the hot water. Across the bubbles, Zoe is still looking at you. Next time you two are alone, somebody has to ask first."),
        ], [go("Go home.", node="home", mins=m, cond_=cond(tod(a, b)), consumes=True, wardrobe=DRESS_BACK,   # false lines a3 #28: dressed for the walk home
               eff=[setv("zoe_step", 3)], flags=[done(3)]) for (a, b), m in HOME_AT_3]),
        node("home_no", "Home", [D(Z, "Next Saturday, then. I'll ask again."), P("She doesn't sound annoyed. She sounds like she's counting. You climb out and get dressed and go home with dry hair, the chlorine still on your skin, and Ryan's door is shut.")],
             [go("Go to bed.", loc="home_ella_room", mins=5, retry=7)]),
        node("home", "Home at three", [
            P("You let yourself in. The house is dark, and your hair drips on the mat. You smell of chlorine, and Zoe's lipstick is still on your neck. Down the hall, Ryan's door is open a crack. He is awake. He sees you in the hall. His eyes stop on your wet hair, then drop to your neck and stay there. \"@player.nickname. Where've you been?\" \"Zoe's.\" You say nothing else, because you want him to wonder. Your face goes hot under his stare, but you hold it. Ryan's jaw tightens. He looks a beat too long, then his door closes slowly."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, retry=7, eff=[nadd("npc_ryan", "want", 5)])]),
    ]})

# ── step 4 · Zoe A 4 · I pick the dares ──
out.append({
    "id": "zoe_04_i_pick_the_dares", "name": "I pick the dares",
    "description": "Zoe step 4 (Zoe A 4), her couch any evening after the hot tub: she admits she dared instead of asking. Sets picks_the_dares (party nights are hers).",
    "trigger": step_trigger(Z, 4),
    "nodes": [
        node("couch", "Her couch", [
            P("Zoe's on her couch in a big T-shirt with her bare legs tucked under her, eating cereal out of the box. She doesn't offer you any. She doesn't look at you either, which for Zoe is the same as shouting."),
            D(Z, "You didn't need me in the hot tub. You were the dare."),
        ], [go("Sit down next to her.", node="asked", mins=5)]),
        node("asked", "So I wouldn't have to ask", [
            D(Z, "I dared you instead of asking. I always do. That's all the dares were. Pathetic, right?"),
            P("She says it to the cereal box. Her ears are red."),
            ME("Not pathetic. A bit stupid, maybe."), D(Z, "Wow. Thanks, babe. Really."),
            # scene reader 2026-11-04 (low heat): a named part of her, Zoe's reaction, the not-yet
            P("She looks up at last, and her eyes go straight to your chest and stay there. Her bare knee is against your thigh, and it doesn't move. Your nipples go tight, and she sees it. She swallows and looks back at the box. Not yet."),
            T("All term. Every dare. She wanted you and she made it a game so she'd never have to say it."),
        ], [
            go("\"Then keep daring me.\"", node="keep", mins=5),
            go("\"Okay.\"", node="okay", mins=1),   # scene reader 2026-11-04 (the written no): her reply, and it says it's parked
        ]),
        node("keep", "Every party", [
            P("She looks at you properly for the first time tonight. Then she grins, slow."),
            *by_level("corruption",
                      bold=ME("Worse ones, Zo. I can take it."),
                      hungry=ME("Make them filthy, Zo. I'll do every single one.")),
            D(Z, "Friday, then. Every party."),
        ], [go("\"Every party.\"", loc="zoe_apartment", mins=10, consumes=True,
               eff=[setv("zoe_step", 4)], flags=[done(4), fset("picks_the_dares")])]),
        no_node("okay", [D(Z, "Okay? I say all that, and I get okay? Wow."),
                         P("She puts her hand back in the cereal, but her ears are still red."),
                         D(Z, "Go on. Come back when you've got more than that, babe.")],
                "zoe_apartment", 3, label="Leave her to her cereal.", mins=4),
    ]})

# ── step 5 · No dare (zoe_05_no_dare.md, signed 2026-11-01), the top step: after a Friday party, past midnight, at
#    her apartment where her row is; she takes her to her bedroom. Her late column (signed). ──
_t5 = step_trigger(Z, 5, retry_days=7)
# truth pass (2026-11-03): "The cocky guy stands there" is 15 minutes in, and his row (and Zoe's) at the flat ends at
# 02:00, so the step opens to 01:45 (the ledger's window is 00:00-02:00)
assert [(s_["start_time"], s_["end_time"]) for s_ in _t5["schedules"]] == [("00:00", "01:45")]   # the ledger says so since 2026-11-03
_t5["conditions"]["items"].append({"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8})
STEP5 = dict(eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 3, "cap": 79}, setv("zoe_step", 5)],
             flags=[done(5), fset("zoe_together")])
out.append({
    "id": "zoe_05_no_dare", "name": "No dare",
    "description": "Zoe step 5, the top step (release 1): after the party, her bedroom: \"No dare. I'm asking.\" The cocky guy at the door: \"Tell him to go.\" or \"Let him watch.\" Sets zoe_together.",
    "trigger": _t5,
    "nodes": [
        node("asking", "I'm asking", [
            P("Zoe pulls you into her bedroom and shuts the door on the party. The music thumps through it. She leans back against the door and, for once, she isn't grinning."),
            D(Z, "No dare. I'm asking."),
            *by_level("corruption",
                      bold=T("You want her to dare you something worse, but she isn't going to."),
                      hungry=T("You don't need a dare. You want her mouth on your cunt, and you want to say so.")),
        ], [
            go("\"Yes.\"", node="down", mins=5),
            go("\"Ask me again.\"", node="again", mins=2),
        ]),
        node("down", "Her bed", [P(beat("zoe_05_no_dare", "down")),
            VID("a girl going down on her friend on a bed, party lights under the door", "girl eats out her friend on bed", "lesbian oral bed party", pool_dir="sex/zoe_05_down_t5"),
            # reader pass 3 b00: Zoe's mouth is on her, so the begging is Ella's, and Zoe's line is about her own mouth
            ME("Oh fuck. Right there, Zo. Don't you dare stop."),
            D(Z, "I've wanted my mouth on your cunt all term, babe."),
            P("She says it against your clit, and her tongue goes straight back to work.")],
            [go("Don't stop.", node="comes", mins=10)]),
        node("comes", "The door", [P(beat("zoe_05_no_dare", "comes")),
            VID("a girl coming with her hand over her mouth, her friend between her thighs, a guy in the doorway", "girl orgasm hand over mouth door opens", "lesbian caught by guy at door", pool_dir="sex/zoe_05_comes_t5")],
            [go("\"Tell him to go.\"", node="out", mins=1),
             go("\"Let him watch.\"", node="watch", mins=1, cond_=cond(trait("exhibitionism", "gte", 60)))]),   # a watcher: Watched (DECISIONS 124)
        node("out", "Out", [
            D(Z, "Out."),
            P("The door clicks shut. The music goes muffled again. Zoe crawls up the bed and kisses you, and you taste yourself on her."),
            D(Z, "Friday, babe. I'm in the dare with you now."),
        ], [go("Stay with her.", loc="zoe_apartment", mins=30, consumes=True, **STEP5)]),
        node("watch", "Stay. Watch.", [
            D(Z, "Stay. Watch."),
            P("He stays. He leans in the doorway with his beer and doesn't say a word. Zoe crawls up the bed and kisses you slowly, so he can see all of it."),
            D(Z, "Friday, babe. I'm in the dare with you now."),
        ], [go("Stay with her.", loc="zoe_apartment", mins=30, consumes=True,
               eff=STEP5["eff"] + [{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 3, "cap": 79}],   # Watched (DECISIONS 124)
               flags=STEP5["flags"] + [fset("zoe_let_him_watch")])]),
        node("again", "Next Friday", [
            ME("Ask me again."),
            P("Zoe laughs, and something in her face lets go."),
            D(Z, "Next Friday, then. I'll ask again."),
        ], [go("Go back to the party.", loc="zoe_apartment", mins=2, retry=7)]),
    ]})

# ── her hubs ──
# reader a3 #36-41 (DECISIONS 131): the skirt line goes on her body, with a not-yet. In public it's "Not here"; in her
# own flat and bedroom "Later" (zoe_05 and her dares make "not yet" false once they've happened).
# One pool, one place (2026-11-04): each hub says these its own way, for that room and that hour. The canteen, where she
# is every weekday, keeps the first words. Gates stay in zoe_state / zoe_leaks, one place. Rows: canteen Mon-Fri lunch;
# quad Tue/Thu/Fri afternoon, her head in her lap; class Mon-Thu; apartment evenings and the Friday party; bedroom Mon-Thu
# 22:00-00:00; party house Saturday night, in the tub ("tits" and "tub" can't show there: both read not-Saturday).
ZOE_HUB_LINES = {
    "canteen": {
        "skirt": ("Her eyes go down your bare legs to the hem, and she bites her lip.", "Now we're talking. Not here, babe."),
        "tits": ("Her eyes drop to your tits and stay there. She bites her lip.", "Oh, you're ready for Friday. Keep them in for now, babe."),
        "dress": ("She bites her lip at the strap of her own dress on you.", "Nope. Eyes stay."),
        "strap": "Her eyes keep going to your bra strap.",
        "tub": "There's a hot tub Saturday. You, me, and some people. Don't forget.",
        "last": "You didn't need me last time, babe.",
    },
    "quad": {
        "skirt": ("She's lying right under your hem, looking straight up your bare thighs, and she licks her lip.", "Best view on campus. Not out here, babe."),
        "tits": ("She looks straight up at your tits from your lap, and her mouth falls open.", "No bra on the quad? Save those for my party, babe."),
        "dress": ("She squints up at her own black dress on you and tugs the string strap with one finger.", "My dress, on the grass? Nope. I'm behaving. For now."),
        "strap": "Upside down in your lap, she's looking at your bra strap.",
        "tub": "Saturday. Hot tub. Me, you, my friends. Say you remember.",
        "last": "That hot tub, babe. You didn't need me at all, did you?",
    },
    "class": {
        "skirt": ("She drops her pen under the desk on purpose, and on the way back up her eyes run along your bare thigh to the hem.", "That's worth coming to class for. Not in here, babe."),
        "tits": ("She stops chewing her pen. She's staring at your tits, and she's quit pretending to take notes.", "You wore that to class? Keep them covered till Friday, babe."),
        "dress": ("She takes the pen out of her mouth and points it at the strap of her own dress on your shoulder.", "In class? In my dress? I'm going to fail this, babe."),
        "strap": "She's supposed to be writing. She's looking at your bra strap.",
        "tub": "Psst. Saturday, the hot tub, you and me and some friends. Write that down.",
        "last": "Psst. You didn't need me in that tub, babe. I can't stop thinking about it.",
    },
    "apartment": {
        "skirt": ("She takes in the skirt from across the room, all that bare leg, and whistles through her teeth.", "Look at you in my living room. Later, babe."),
        "tits": ("Her eyes land on your tits and she stops talking, and for Zoe that takes something.", "No bra at my place? Hold that thought, babe."),
        "dress": ("She looks at her own dress on you, at the string on your shoulder, and pulls at her bottom lip.", "I'm keeping my hands to myself. For now."),
        "strap": "She's talking to you, but she's looking at your bra strap.",
        "tub": "Hot tub, Saturday, the party house. My friends will be there. Bring your nerve, babe.",
        "last": "You didn't need my dare in that tub, babe. I noticed.",
    },
    "bedroom": {
        "skirt": ("She rolls over on her bed to get a better look, up your bare legs to the hem, and hums.", "Now I'm awake. Later, babe."),
        "tits": ("She props her chin on her hand and looks at your tits, then your face, then your tits.", "No bra, in my bedroom? Go home, babe, before I stop behaving."),
        "dress": ("She reaches off the bed and twangs the strap of her own dress on your shoulder, but only once.", "Nope. Hands stay."),
    },
    "party_house": {
        "skirt": ("She looks over the rim of the tub, up your bare legs to the hem, and sinks down slowly in the water.", "That skirt's getting wet if you come any closer. Not in front of the girls, babe."),
        "tits": ("She looks at your tits from the water and blows steam at them.", "Get them in here sometime, babe. Not with the girls here."),
        "dress": ("She looks up at her own black dress on you and flicks water at the strap.", "Not in my tub, you don't. That dress stays dry."),
        "strap": "She's up to her neck in the water, and her eyes are on your bra strap.",
        "tub": "This tub, Saturday. You, me, the girls. Don't forget.",
        "last": "Same tub, babe. You didn't need me in it last time.",
    },
}


ZOE_SEES = {   # two places, so each line lives on one screen (gate `one pool, one place`)
    "quad": {   # she's lying with her head in your lap here; each line keeps a "not out here"
        "crop_top": ("Zoe, with her head in your lap, pokes your bare belly under the crop top and grins up at the hem.", "One reach for the top shelf and the whole library gets underboob, babe. Not out here, though. Too many people."),
        "bodycon_dress": ("Zoe looks up at you from your lap, all the way up the bodycon dress, and whistles.", "Painted on. Keep your knees together out here, babe. Save the rest for my party."),
        "micro_shorts": ("Zoe turns her head in your lap and bites the bare skin of your thigh where the micro shorts stop.", "Half your ass is out on the quad, babe. I love it. Not here, though. Everyone's watching."),
        "plunge_dress": ("Zoe looks straight up the open front of the plunge dress, from your lap, at your bare tits inside it.", "To class? In that? One wrong move and they're out. Not out here, babe. Save it for a party."),
        # more clothes, round 2 (DECISIONS 208)
        "split_skirt": ("Zoe runs a finger up your bare leg from your knee to where the slit in your skirt stops, at your hip.", "This slit is criminal. Not here, babe. Save it for my party."),
        "sequin_dress": ("Zoe squints up at you from your lap like you're too bright to look at, and laughs.", "Sequins on the quad? You're a disco ball. Save it for my party, babe."),
        "backless_dress": ("Zoe slides a hand up your bare back from your lap, all the way up, and doesn't find a strap.", "Nothing under it. On the quad. Babe. Not out here, though. Save it for my party."),
    },
    "party_house": {
        "crop_top": ("Zoe hooks a finger in the bottom of your crop top and tugs it an inch higher.", "There. Now you're dressed for my parties."),
        "bodycon_dress": ("Zoe runs her eyes down the bodycon dress to where it stops on your thighs.", "Sit on the edge of this tub in that and I'll see everything from here. Just saying."),
        "micro_shorts": ("Zoe leans on the rim of the tub to look at the backs of your micro shorts, and laughs.", "Wear those to the party. Every guy there will look at your ass twice. I'll count."),
        "plunge_dress": ("Zoe takes in the plunge dress, the open neck, your bare tits loose inside it, and her eyebrows go up.", "Dance in that at my party and you'll fall out of it. Please dance in that."),
        "split_skirt": ("Zoe pulls the slit of your skirt open with one finger, all the way to your hip, and lets it fall.", "Sit on the edge of the tub in that and the slit does all the work."),
        "sequin_dress": ("Zoe looks the sequin dress up and down and puts a hand over her heart.", "My kind of dress. Wear it to every party I throw, babe, I mean it."),
        "backless_dress": ("Zoe makes you turn round at the rim of the tub to see the back of the dress, the bare skin down to the base of your spine.", "Nothing under it at all? Babe. Everyone at the party is going to want to put a hand there."),
    },
}


def zoe_state(where):
    say = ZOE_HUB_LINES[where]
    return [
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P(say["skirt"][0]), D(Z, say["skirt"][1])),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}, {"type": "weekday", "weekdays": [0, 1, 2, 3, 4]}),
          P(say["tits"][0]), D(Z, say["tits"][1])),
        G(cond(PARTY_DRESS), P(say["dress"][0]), D(Z, say["dress"][1])),
        # everyday clothes by stage (DECISIONS 205): Zoe sees each piece
        *[G(cond({"type": "worn_type", "operator": "eq", "value": t}, *([{"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}] if t in ("plunge_dress", "backless_dress") else [])),
            P(a), D(Z, b)) for t, (a, b) in ZOE_SEES.get(where, {}).items()],
    ]


def zoe_leaks(where):
    say = ZOE_HUB_LINES[where]
    return [
        G(cond(trait("zoe_step", "eq", 1), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), P(say["strap"])),
        # not on Saturday: that night she is in the tub (iteration 002, part 8, reader)
        G(cond(trait("zoe_step", "eq", 2), {"type": "weekday", "weekdays": [0, 1, 2, 3, 4, 6]}), D(Z, say["tub"])),   # scene reader b02: her friends are in the tub (zoe_03)
        G(cond(trait("zoe_step", "eq", 3)), D(Z, say["last"])),
    ]


out.append({
    "id": "hub_zoe_quad", "name": "Zoe, on the grass",
    "description": "Zoe's hub on the quad: her want shown first, her head in her lap.",
    "trigger": {"location": "quad", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("grass", "The grass", [
        P("Zoe's on the grass with her shoes off. She doesn't say hello. She just puts her head in your lap and looks up at you, and when people look over, she says, \"Let them.\""),
        POOL(D(Z, "Tell me something bad you did."), D(Z, "That guy's staring at your legs. Want me to make him stare harder?"), D(Z, "Friday. You're coming. I'm not asking."),
             D(Z, "Best friend I've made at this whole college, and you're wasted on Psychology."),   # pass 3 C45 (the-first-hour.md F10): who she is, in the pool
             pid="zoe_quad_lines"),
        ME("Hey, Zo."), D(Z, "Hey yourself. Stay still, you're my pillow now."),   # pass 3 B4
        *zoe_state("quad"), *zoe_leaks("quad"),
    ], [go("Lie back with her a while.", loc="quad", mins=30), go("Leave her to the sun.", loc="campus")])]})

out.append({
    "id": "hub_zoe_canteen", "name": "Zoe, at lunch",
    "description": "Zoe at lunch in the canteen.",
    "trigger": {"location": "canteen", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("lunch", "Lunch", [
        P("Zoe steals fries off the tray of the guy beside her, one at a time, and eats them looking straight at you."),
        *zoe_leaks("canteen"),
        G(cond(wd(3, 4)), D(Z, "Friday. Mine. Don't make me come and get you.")),
        # reader a3 #20 (DECISIONS 131): Mon-Wed points ahead too. Her Friday party runs every Friday (hub_zoe_apartment)
        G(cond(wd(0, 1, 2)), D(Z, "Friday's coming, babe. Start planning.")),
        POOL(D(Z, "Babe. You will not believe what the TA said to me."), D(Z, "Sit. You're with me."), D(Z, "Who's the guy? Don't say no guy. There's a guy."),
             D(Z, "What are friends for? Give me your fries."),   # pass 3 C45 (F10)
             pid="zoe_lunch_lines"),
        ME("Hi, Zo."), D(Z, "Hi, babe. You're buying dessert."),   # pass 3 B4
        *zoe_state("canteen"),
    ], [go("Stay for lunch with her.", loc="canteen", mins=30), go("Leave her your fries.", loc="campus")])]})

# ── her face in class: Biology and figure drawing, once met (ledger L27; sweep A5-11) ──
out.append({
    "id": "hub_zoe_class", "name": "Zoe, in class",
    "description": "Zoe beside her in Biology and figure drawing (her lecture-hall rows, once met).",
    "trigger": {"location": "lecture_hall", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("seat", "Zoe, beside you", [
        P("Zoe's in the seat beside yours with her bag on her knee and her pen in her mouth."),
        POOL(D(Z, "Notes are for people with no friends. I'll copy yours."), D(Z, "Sit with me. This is going to be so boring."),
             D(Z, "Don't let me fall asleep. Actually, do."),
             D(Z, "Party's Friday. You're coming."),   # reader a3 #21 (DECISIONS 131): a forward line; her class rows are Mon-Thu
             D(Z, "You're my only friend in this class who takes notes. Guard them with your life."),   # pass 3 C45 (F10)
             pid="zoe_class_lines"),
        *zoe_state("class"), *zoe_leaks("class"),
    ], [go("Whisper with her a while.", loc="lecture_hall", mins=10), go("Leave her to doodle.", loc="campus")])]})

PRE_PARTY = [wd(4), tod("18:00", "19:00")]
PARTY_ON = cond(wd(4), tod("19:00", "00:00"))
PARTY_LATE = cond(wd(5), tod("00:00", "02:00"))
COUCH = [{"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}, tod("18:00", "00:00")]   # her row runs to midnight
out.append({
    "id": "hub_zoe_apartment", "name": "Zoe, at home",
    "description": "Zoe in her living room: getting ready on Friday before the party (she does your face), the Friday party, her couch other evenings.",
    "trigger": {"location": "zoe_apartment", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("couch", "Zoe", [
        G(cond(wd(5), tod("22:00", "23:59")), P("Zoe's flat out on the couch with her shoes off and the music turned low. She lifts her feet so you can sit."),   # pass 5 D5: her row runs to midnight
          D(Z, "Sit. Saturday's not over till I say so.")),
        G(cond(*PRE_PARTY), P("Zoe's at the mirror by the balcony door in her underwear, make-up tipped out across the table, music already up."),
          D(Z, "Sit. You're next. Lips first.")),
        G(PARTY_ON, P("The flat is loud and full. Zoe's in the middle of it with a drink in each hand, and she hands you one."),
          D(Z, "Drink. Dance. Don't be boring.")),
        # "Still here?" only if she was at the party tonight (part 9, reader)
        G(cond(*PARTY_LATE["items"], {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}),
          P("The party's thinner now, the music lower. Zoe's on the arm of the couch with her shoes off, holding court."),
          D(Z, "Still here? Good girl.")),
        G(cond(*PARTY_LATE["items"], flag("party_went", False)),
          P("The party's thinner now, the music lower. Zoe's on the arm of the couch with her shoes off, holding court."),
          D(Z, "Now you show up? Get a drink. Catch up.")),
        G(cond(*PARTY_LATE["items"], flag("party_went"), {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "gte", "value": 8}),
          P("The party's thinner now, the music lower. Zoe's on the arm of the couch with her shoes off, holding court."),
          D(Z, "Now you show up? Get a drink. Catch up.")),
        G(cond(*COUCH), P("Zoe's on the couch in a big T-shirt with the TV on and her feet up. She shoves her feet off the cushion for you."),
          POOL(D(Z, "Stay. Watch trash with me."), D(Z, "Paint my nails. You've got steadier hands."), D(Z, "I'm bored. Dare me something."),
               D(Z, "You're my favorite friend at that whole college. Don't tell the others."), pid="zoe_home_lines"),
          ME("Budge up, then."), D(Z, "Only if you rub my feet.")),   # pass 3 B4
        G(cond(flag("picks_the_dares"), wd(4), tod("23:00", "00:00"), trait("exhibitionism", "gte", 40), {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}), D(Z, "After midnight I pick your dare. Don't go anywhere.")),
        # reader 2026-11-10 (DECISIONS 224): "Take Zoe's dare" opens here, and Zoe names the dare herself
        G(cond(flag("picks_the_dares"), *PARTY_LATE["items"], trait("exhibitionism", "gte", 40), flag("zoe_dared", False), flag("cocky_guy_met"), tod("00:00", "01:50"), {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}), D(Z, "It's past midnight. I've picked your dare. Ask me.")),   # the door closes at 01:50
        *zoe_state("apartment"), *zoe_leaks("apartment"),   # reader a3 #36 (DECISIONS 131): her own flat
    ], [
        go("Let her do your face.", node="face", mins=20, cond_=cond(*PRE_PARTY, flag("made_up_today", False)),
           flags=[fset("made_up"), fset("made_up_today")]),
        go("Let her do your face in her lap.", node="face_lap", mins=20, cond_=cond(*PRE_PARTY, flag("made_up_today", False), CURIOUS),
           # in her lap with nobody else watching is a thing she does, not shows: Corruption, the meter it is gated on,
           # capped at the top of Curious (pass 3 A48, G8)
           flags=[fset("made_up"), fset("made_up_today")], eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 39}]),
        # reader batch 5 (pass 3): her "Lips first." gets a written no
        go("\"I'll do my own face.\"", node="face_no", mins=0, cond_=cond(*PRE_PARTY, flag("made_up_today", False))),
        go("Stay a while.", loc="zoe_apartment", mins=45),
        go("Leave her to it.", loc="town"),
    ]),
    node("face_no", "Your own face", [
        D(Z, "Your loss, babe. Don't come crying to me when nobody looks at you."),
        P("She turns back to the mirror in her underwear and does her own lips, slow, watching you in the glass the whole time."),
    ], [go("Wait for the party.", loc="zoe_apartment", mins=60)]),
    node("face", "Lips. Open.", [
        P("She sits you on the arm of the couch and tips your chin up with two fingers and does your whole face, eyes and skin and lips, close enough that you can feel her breathing."),
        D(Z, "Lips. Open. There. Now you look like trouble."),
    ], [go("Look in the mirror.", loc="zoe_apartment", mins=5)]),
    node("face_lap", "In her lap", [
        P("She pulls you into her lap on the couch to do it, your knees either side of hers, and does your eyes with her face an inch from yours. She takes longer than she needs to, but neither of you mentions it."),
        D(Z, "Lips. Open. Don't move. I said don't move."),
    ], [go("Look in the mirror.", loc="zoe_apartment", mins=5)]),
]})

# ── her bedroom, Mon-Thu 22:00-00:00 (her row; Q48, Q52): she's going to bed, and she lends the dress ──
# Moved here from 3_activities' zoe_borrow_dress: an item with a person is a choice in her hub, and her face is here.
out.append({
    "id": "hub_zoe_bedroom", "name": "Zoe, going to bed",
    "description": "Zoe in her bedroom on weeknights and Sunday nights, going to bed: her wardrobe, and the dress she lends (zoe_party_dress).",
    "trigger": {"location": "zoe_bedroom", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [
        node("bed", "Her bedroom", [
            P("Zoe's on her bed on her stomach in a big T-shirt, chin in her hands, half ready for sleep and nowhere near it."),
            D(Z, "Raid the wardrobe. Half of it still has the tags on."),
            *zoe_state("bedroom"),   # reader a3 #37 (DECISIONS 131): her own bedroom
        ], [go("Go through her clothes.", node="wardrobe", mins=5), go("Leave her to sleep.", loc="zoe_apartment", mins=2)]),
        node("wardrobe", "Zoe's wardrobe", [
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "not_owned"}),
              P("She points with her foot at a black dress on the back of the door, short and tight, with straps like string."),
              D(Z, "That one. Put it on. No, here. I want to see.")),
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "owned"}),
              D(Z, "You've got my dress. You've got the best one. What else do you want, my underwear?"),
              P("She laughs. Then she doesn't, and she watches you hold a top up against yourself in her mirror, and she bites her lip.")),
        ], [
            go("Put it on for her.", node="dress", mins=5,
               cond_=cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "not_owned"}),
               wardrobe=[{"action": "add", "item_id": "zoe_party_dress"}, {"action": "equip", "item_id": "zoe_party_dress"}]),
            go("Hang it all back up.", loc="zoe_apartment", mins=15),
        ]),
        # Iteration 002, part 8 (reader): the dress is on her before the screen says so.
        node("dress", "Her dress", [
            P("You change in front of her. She doesn't look away once, not while you strip, not when you tug the dress down over your ass. When it's on she whistles, low, and hooks one finger under the strap on your shoulder, and stops there."),
            D(Z, "Keep it. If I fix that strap I won't stop. Wear it Friday."),
        ], [go("Keep it.", loc="zoe_apartment", mins=10)]),
    ]})

# ── the party house, Saturday 20:00-00:00 (her row, sweep A4-08): the hot tub on the deck ──
out.append({
    "id": "hub_zoe_party_house", "name": "Zoe, in the hot tub",
    "description": "Zoe at the party house on Saturday night, in the hot tub with her friends (her face there; Zoe A 3 fires here).",
    "trigger": {"location": "party_house", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("deck", "The deck", [
        P("Zoe's in the hot tub on the back deck with two of her friends, hair piled up, a drink on the rim, steam all round her."),
        POOL(D(Z, "Get in. The water's perfect."), D(Z, "There she is. Make room, girls."),
             D(Z, "Girls, this is my friend from college. Be nice. Or don't."), pid="zoe_party_house_lines"),
        # reader batch 4 (pass 3): a forward line that can show here (her Friday party at her flat, PARTY_ON)
        D(Z, "And Friday you're at mine. Don't you dare miss it."),
        *zoe_state("party_house"), *zoe_leaks("party_house"),
    ], [go("Sit on the edge with your feet in.", node="edge", mins=0), go("Leave her to the tub.", loc="town")]),
        # reader batch 4 (pass 3): her "Get in." answered on the screen it lands on
        node("edge", "Feet in", [
            P("You sit on the edge of the tub and put your feet in the water."),
            D(Z, "Coward. Feet only? Fine. For now."),
            P("She splashes your knees and laughs, and her eyes run up your wet legs and stay there."),
        ], [go("Watch the steam a while.", loc="party_house", mins=20)])]})

out.append({
    "id": "hub_zoe_park", "name": "Zoe, running",
    "description": "Zoe on her weekend run in the park: a lap with her, her eyes on your ass. Her flash dare (zoe_park_dare) and the hollow off the path (park_hidden) open from her first screen (doors.py, DECISIONS 224).",
    "trigger": {"location": "park", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [
        node("path", "The path", [
            P("Zoe jogs up the path in tiny shorts and a sports top, earbuds in, cheeks pink. She runs on the spot in front of you and pulls one earbud out."),
            D(Z, "Run with me. Or don't, and stand there looking cute."),
            G(cond({"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}),
              D(Z, "Just the sports bra? Babe. Half the park's going to fall in the pond.")),
            # her run text (phone.py zoe_run, DECISIONS 87): the yes books it; a no-show sets zoe_bailed
            G(cond(flag("zoe_run_booked")), D(Z, "You actually came! Okay. I owe you a coffee.")),
            G(cond(flag("zoe_run_booked", False), flag("zoe_bailed")), D(Z, "Oh, look who remembered mornings exist.")),
        ], [
            # pass 3 D44 (the-surfaces.md R9): the lap with her lands on a screen of it, not a toast
            *booked_split(go("Run a lap with her.", node="lap", mins=30, costs=[{"trait": "energy", "value": 10}],
                             flags=[fset("ran_with_zoe"), funset("zoe_bailed")]), "zoe_run_booked"),
            go("Let her run on.", loc="street"),
        ]),
        node("lap", "A lap with her", [
            P("She sets the pace and doesn't let up, and by the far end of the pond your lungs are burning and sweat is running down between your tits. Zoe drops back on the last stretch to run behind you."),
            D(Z, "Just enjoying the view, babe. Keep going."),
            # scene reader b03 (2026-11-03): the not-yet, and the hook by her run row (Sat and Sun 08:00-10:00)
            P("She stays two strides behind you all the way to the gates, her eyes on your ass, and she never closes the gap. Not yet."),
            G(cond(wd(5)), D(Z, "Same loop tomorrow. Eight sharp, babe.")),
            G(cond(wd(6)), D(Z, "Same loop next Saturday. Eight sharp, babe.")),
        ], [go("Walk it off.", loc="street")]),
    ]})

# reader a3 #23 (DECISIONS 131): each branch points at her next dare. She runs Sat and Sun 08:00-10:00, and the dare
# repeats once a day, so Saturday's is tomorrow and Sunday's is next weekend. "Again", not "worse": no worse park
# dare is built in this release.
PARK_NEXT = [G(cond(wd(5)), D(Z, "Tomorrow I'm daring you again.")),
             G(cond(wd(6)), D(Z, "Next weekend I'm daring you again."))]
out.append({
    "id": "zoe_park_dare", "name": "\"Dare me, Zo.\"",
    "description": "Zoe's dare on her run (the park sheet, Curious): a flash on the path. Exhibitionism +1, once a day.",
    # DECISIONS 224 (LO, 2026-11-10): a button in her park hub, not its own link; its gate lives in doors.py
    "trigger": {"location": "park", "requires_npc": Z, "is_repeatable": True, "priority": 4, "is_active": True, **doors.trigger("zoe_park_dare")},
    "nodes": [
        node("ask", "Her dare", [D(Z, "Flash me. Right here. Two seconds. There's a guy on the bench, so make it count."),
            *by_level("exhibitionism",
                      good_girl=T("A guy on a bench, in broad daylight. Your face burns just hearing it."),
                      curious=T("Two seconds. You wonder what his face would do."),
                      bold=T("Two seconds. You're nearly brave enough, and you hate how much you want to be."),
                      hungry=T("Two seconds isn't enough. You want him to drop that coffee."))],
             [go("Do it.", node="dare", mins=1, cond_=cond(trait("exhibitionism", "gte", 60))), go("\"Not here, Zo.\"", node="no", mins=1)]),   # a stranger watching: Watched (DECISIONS 124)
        node("dare", "Her dare", [
            P("You check the path both ways and pull your top up, and everything under it, for two long seconds. Your tits are out in the open air. Zoe shrieks. The guy on the bench drops his coffee and doesn't look away."),
            D(Z, "Oh my god. Two seconds, that's all he gets. Run!"),
            *PARK_NEXT,
        # (2026-11-03) the walk-in B13 opens this node directly, past the canvas's own daily cap, so the pay carries
        # its own: once a day through zoe_park_dare_today (cleared in the daily tick)
        ], [go("Run.", loc="park", mins=10, cond_=cond(flag("zoe_park_dare_today", False)), flags=[fset("zoe_park_dare_today")],
               eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 79}]),
            go("Run.", loc="park", mins=10, cond_=cond(flag("zoe_park_dare_today")))]),
        node("no", "Not here", [D(Z, "Chicken."), P("She laughs and sprints off up the path, and you have to run to catch her."), *PARK_NEXT], [go("Run after her.", loc="park", mins=10)]),   # reader a3 older: park_cool_zoe was read by nothing
    ]})

cards = step_cards(Z, {
    1: ("Zoe's party, Friday, at her place. She has a dress for you.", "Friday evening: Zoe's party at her apartment"),
    2: ("Her eyes keep going to your bra strap. She has a dare.", "A Friday party at Zoe's, out on the balcony (Curious or Daring)"),
    3: ("\"There's a hot tub Saturday. You, me, and some people.\"", "Saturday night: the hot tub at the party house (Curious, Daring)"),
    4: ("\"You didn't need me in the hot tub.\" She still won't ask.", "An evening at Zoe's apartment, on her couch"),
    5: ("Party nights are hers. Four dares, and she stops daring.", "After a Friday party, past midnight (Bold)"),
}, met_flag="zoe_met", terminal_text=("Her dares, every Friday: she joins in now.", "Zoe's next dare. (Next release)"))

# Her meeting card, on her own row under People from the day the opening ends (LO 2026-11-02: "zoe should have
# a npc card"), the way Dr. Hale's step-1 card points at his first lecture. It was a Story Goals card in group
# story_goals, where the priority-20 "Week one" card won the group for days 0-6: nothing pointed at her in week
# one, though her meeting fires from the first Tuesday.
# C3 (LO 2026-11-03): the heading stands in for her name until she has met her (engine f0d7b863)
cards.insert(0, {"npc_id": Z, "priority": 10, "heading": "A girl from Biology", "text": "The girl from your Biology class hangs out on the quad in the afternoons.",
                 "tip": "The quad, Tuesday, Thursday or Friday, 14:30 to 18:00",
                 "when": [{"flag": "opening_done", "op": "is_true"}, {"flag": "zoe_met", "op": "is_false"}],
                 "ready_canvas": "zoe_00_quad_meeting"})
story = []

# Step 2 (DECISIONS 133): not the night of step 1 (24 hours after zoe_01_done), and only when a yes shows:
# Daring takes the bra dare; Curious under Daring takes "Dare me something else." when the cocky guy is there.
# The engine has no nested OR in a trigger, so the Curious case is its own copy of the balcony with the kiss route.
import copy
_s2 = next(c for c in out if c["id"] == "zoe_02_bra_through_the_sleeve")
_s2["trigger"]["conditions"]["items"].append({"type": "hours_since_flag", "subject": "player", "flag_key": "zoe_01_done", "operator": "gte", "value": 24})
_s2c = copy.deepcopy(_s2)
_s2["trigger"]["conditions"]["items"].append(trait("exhibitionism", "gte", 20))
_s2c["id"] = "zoe_02_balcony_curious"
_s2c["description"] = "Zoe step 2, Curious under Daring: the balcony dare when only \"Dare me something else.\" can be a yes (the cocky guy is at the party). Same screens as zoe_02_bra_through_the_sleeve."
_s2c["trigger"]["conditions"]["items"] += [trait("exhibitionism", "lt", 20), CURIOUS, flag("cocky_guy_met"),
    {"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": "npc_cocky_guy", "operator": "is_present"}]
_s2c["nodes"] = [n for n in _s2c["nodes"] if n["id"] in ("balcony", "kiss", "saturday", "no")]
own_media(_s2c["nodes"], "curious")   # pass 3 B37: the copy's kiss clip is its own asset

_s2c["nodes"][0]["choices"] = [c for c in _s2c["nodes"][0]["choices"] if c.get("nodeId") not in ("sleeve", "already")]   # Daring-only
# scene reader b02 (2026-11-03): in this copy "I'm not wearing one" is cut, so with no bra on she has already
# beaten the bra dare and Zoe says so; the dare line itself only while there is a bra to take off
_BRA_DARE = D(Z, "Bra off. Don't take anything else off. That's the dare.")
_NO_BRA_ITEM = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
_NO_BRA_LINE = D(Z, "No bra under that? Babe. You've beaten my bra dare before I've said it. So what do I dare you instead?")
_i = _s2c["nodes"][0]["blocks"].index(_BRA_DARE)
_s2c["nodes"][0]["blocks"][_i:_i + 1] = [
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), _BRA_DARE),
    # scene reader 2026-11-04: "under that" only with a top or a dress on (conditions don't nest, so one group each)
    G(cond(_NO_BRA_ITEM, _TOP_ONLY), _NO_BRA_LINE),
    G(cond(_NO_BRA_ITEM, _NO_TOP, {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}), _NO_BRA_LINE),
    G(cond(_NO_BRA_ITEM, _NO_TOP, _NO_DRESS), D(Z, "Nothing on top at all? Babe. That's my bra dare beaten before I've opened my mouth. Now what?"))]
# One pool, one place (2026-11-04): this copy's words are its own; zoe_02_bra_through_the_sleeve keeps the first ones.
_s2_voice = {
    "You chickened out on me last time. Not tonight, babe.": "You bailed on this balcony once already, babe. Not this time.",
    "Zoe pulls you out onto the balcony, away from the noise. The glass door is behind you and the whole party is on the other side of it. She leans on the rail and looks at the strap on your shoulder and doesn't look anywhere else.":
        "Zoe hauls you through the crowd and out onto the balcony, and shuts the glass door with her foot. It's cold out here, and every face at the party is right there through the glass. She hooks a finger under the strap on your shoulder and lets it snap back, grinning.",
    "Zoe pulls you out onto the balcony, away from the noise. The glass door is behind you and the whole party is on the other side of it. She leans on the rail and looks at your shoulder and doesn't look anywhere else.":
        "Zoe hauls you through the crowd and out onto the balcony, and shuts the glass door with her foot. It's cold out here, and every face at the party is right there through the glass. She looks at your shoulder, right where a strap should be, and raises her eyebrows.",
    "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people.":
        "Saturday night. The party house has a hot tub on the deck. You and me, babe. Okay, you, me and a few people.",
}


def _reword(blocks):
    for b in blocks:
        if b.get("content") in _s2_voice:
            b["content"] = _s2_voice[b["content"]]
        _reword(b.get("blocks") or [])


for _n in _s2c["nodes"]:
    _reword(_n["blocks"])
_kiss = next(n for n in _s2c["nodes"] if n["id"] == "kiss")
_kiss["blocks"] = _kiss["blocks"][:-3]   # the three "Just a dare" thoughts stay on the bra canvas: its beat, not this copy's
_vid = next(i for i, b in enumerate(_kiss["blocks"]) if b.get("type") == "video")
_kiss["blocks"][1:_vid] = kiss_by_top("kiss_curious", "Your nipples tighten under your top, and he feels them and laughs into your mouth.",
                                      "Your nipples tighten through your bra, and he feels them and laughs into your mouth.",
                                      "Your bare nipples tighten against his shirt, and he feels them and laughs into your mouth.")
# Her line beside the dare. The bra canvas reads Exhibitionism (20+ by its trigger, the moment is being seen); this copy
# reads Corruption (20+), because she is here for what she will do, not for what she will show.
_s2["nodes"][0]["blocks"] += by_level("exhibitionism",
    curious=T("The whole party is right behind that glass. You wonder who'd look first."),
    bold=T("The whole party is right behind that glass. Good. Let one of them turn around."),
    hungry=T("You want that glass full of faces, and every one of them looking at you."))
_s2c["nodes"][0]["blocks"] += by_level("corruption",
    curious=T("Not with that glass there. Your face burns just thinking about it, but you wonder what else she'd dare you to do."),
    bold=T("Show the whole party? No. But you'd do nearly anything else she asks, and you want her to know it."),
    hungry=T("Not through that glass. Put a guy in front of you instead. You want something you can get your mouth on."))
out.insert(out.index(_s2) + 1, _s2c)
_c1 = next(c for c in cards if c.get("ready_canvas") == "zoe_01_first_party")
_c1["when"].append({"flag": "zoe_kiss_refused", "op": "is_false"})
cards.insert(cards.index(_c1) + 1, {"npc_id": Z, "priority": 10,
    "text": "You said no to her kiss dare. She said she'd keep asking.",
    "tip": "A Friday party at Zoe's, 7 to 11 PM",
    "when": [{"type": "trait", "subject": "player", "trait": "zoe_step", "op": "eq", "value": 0},
             {"flag": "zoe_kiss_refused", "op": "is_true"}, {"flag": "zoe_met", "op": "is_true"}],   # pass 3 C38: every card after the meeting carries it
    "goals": [{"type": "trait", "subject": "player", "trait": "corruption", "op": "gte", "value": 20,
               "label": "Not yet: Zoe's kiss dare waits until you're more curious (your Corruption)"}],   # study 2026-11-09: the need last, in words
    "ready_canvas": "zoe_01b_kiss_again"})
_c2 = next(c for c in cards if c.get("ready_canvas") == "zoe_02_bra_through_the_sleeve")
_c2["tip"] += "; Daring, or Curious when a guy from Figure drawing is at the party"   # playtest 2026-11-09: no unmet name
_c2.setdefault("goals", []).append({"type": "trait", "subject": "player", "trait": "exhibitionism", "op": "gte", "value": 20,
    "label": "Reach Daring (Exhibitionism 20), or Curious (Corruption 20) with a guy from Figure drawing at the party"})

# heat proposal A2 (the canteen) and A5 (her bedroom), DECISIONS 147 chunk 2: screens inside her hubs (heat_a.py)
import heat_a
heat_a.attach_zoe(out)

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · ZOE (sheets/scenes/zoe_0*.md, people/npc_zoe.md)\n"
        "# Her meeting, steps 1-4 (step 1 is also Jake's step 1), her hubs, her cards, the meeting nudge.\n"
        "# =============================================================================\n")
# Iteration 002, part 3: leaving this outing after 22:00 sets late_party and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
for _c in out:
    if _c["id"] in ['zoe_01_first_party', 'zoe_01b_kiss_again', 'zoe_02_bra_through_the_sleeve', 'zoe_02_balcony_curious', 'zoe_03_hot_tub']:
        mark_late(_c, 'late_party', split=True)

# pass 4 E95: the one-time sex step takes energy and hygiene like the repeatable acts (board.needs)
sex_takes_needs(out, "zoe_05_no_dare", "down", "Don't stop.")
import everyday   # DECISIONS 222: the day after an everyday scene, the hub remembers it
everyday.hub_read(out)
doors.apply(out)   # DECISIONS 224: seal the door-only scenes here, open the doors in the hubs here
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards + story)
open(__import__("sys").argv[1], "w").write(text)
print("zoe:", len(out), "canvases,", len(cards) + len(story), "cards")
