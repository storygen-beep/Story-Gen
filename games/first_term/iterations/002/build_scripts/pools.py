"""The pool and system scenes: parties (arrival, drinks, chat, the dare, the hookup), the park
(walk, run, rest, selfie, the couple, hidden with Zoe), touching herself (bed, shower, toilet), the
stairs event. Sources: sheets/systems/parties.md, park.md, wardrobe.md; scenes party_*.md,
park_*.md, touch_*.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

Z, J, C = "npc_zoe", "npc_jake", "npc_cocky_guy"
R, L, M = "npc_ryan", "npc_laura", "npc_mark"
out = []
CAP_GG, CAP_CUR, CAP_BOLD = 19, 39, 59   # CAP_GG: a Good Girl act stops paying at 19 (DECISIONS 78)
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
PROMISED_SHORT = [flag("zoe_party_promised"), {"type": "hours_since_flag", "subject": "player",
                                              "flag_key": "zoe_party_promised", "operator": "lt", "value": 30}]
out.append({
    "id": "party_arrive", "name": "Go in to Zoe's party",
    "description": "The Friday party at Zoe's (the parties sheet): the curfew, under 20 energy and something short each say why at the door. Arriving costs 15 energy; sets party_went and drinks_tonight 0.",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 5, "is_active": True,
                "schedules": [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}],
                "conditions": cond(flag("zoe_met"), trait("zoe_step", "gte", 1),
                                   {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "gte", "value": 24}),
                "show_when_blocked": True, "cooldown_message": "Fri, 7 PM-midnight"},   # pass 3 H31: a bare phrase (C5)
    "nodes": [node("door", "Zoe's door", [
        P("You can hear it from the stairwell: bass through the walls, somebody shrieking with laughter, the door propped open with a crate of beer."),
        G(CURFEW_ON, T("Laura said no. Not this Friday.")),
        G(cond(trait("energy", "lt", 20)), T("You're asleep on your feet. The party runs late. You could go home and sleep and come back.")),
        G(cond(NOT_SHORT), D(Z, "Not in that. Borrow mine. Bedroom. Go.")),
        G(cond(SHORT), D(Z, "Babe! Get in here. Now we're talking.")),
        # her "obviously" to Thursday's text (phone.py zoe_party, DECISIONS 87), read for the next 30 hours
        G(cond(*PROMISED_SHORT, SHORT), D(Z, "Told you. Short. Good girl.")),
        G(cond(*PROMISED_SHORT, NOT_SHORT), D(Z, "\"Obviously\", she said. That's not short, babe.")),
    ], [
        go("Go in. (15 energy)", loc="zoe_apartment", mins=10, costs=[{"trait": "energy", "value": 15}],
           cond_=cond(SHORT, NO_CURFEW_ITEM), flags=[fset("party_went"), funset("zoe_party_promised"), funset("zoe_dared")],
           # pass 4 E95: a party night takes hygiene (board.needs "faster after ... parties"), once a night with the door
           eff=[setv("drinks_tonight", 0), add("hygiene", -10)]),
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
    "id": "party_drink_offer", "event": True, "name": "Somebody hands you a drink",
    "description": "A drink (the parties sheet): drinks_tonight +1 and the drinks boost for 3 hours (one stage up on both meters, for choices only; steps ignore it). The third drink sets heavy_night. A no always works.",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 4, "is_active": True,
                "schedules": PARTY_SCHED, "conditions": cond(AT_PARTY, trait("drinks_tonight", "lt", 3))},
    "nodes": [node("cup", "A red cup", [
        # LO 2026-11-03: the one who hands it over says something. Each entry is a group so the pool stays one type.
        POOL(GC(cond(AT_PARTY), P("Someone pushes a red cup into your hand. Vodka and something orange. It's strong."), WHO("Drink up. It's a party.")),
             GC(cond(AT_PARTY), P("Zoe appears with two shots and holds one to your lips."), D(Z, "Open up, babe. One for you, one for me.")),
             GC(cond(AT_PARTY), P("A guy from the team pours you something from a bottle with no label and winks."), WHO("Don't ask what's in it. Just drink."))),
        G(cond(trait("drinks_tonight", "eq", 2)), T("That'd be three. You'll feel it tomorrow.")),
    ], [
        # pass 3 D44 (the-surfaces.md R9): the drink lands on her body, not a toast (drinks_tonight is already counted)
        go("Drink it.", node="drunk", mins=15, cond_=cond(trait("drinks_tonight", "lt", 2)), mods=DRINK_MOD, eff=[add("drinks_tonight", 1)]),
        go("Drink it. (your third)", node="drunk", mins=15, cond_=cond(trait("drinks_tonight", "eq", 2)), mods=DRINK_MOD,
           eff=[add("drinks_tonight", 1)], flags=[fset("heavy_night")]),
        go("\"I'm good, thanks.\"", node="no", mins=2),
    ]), node("no", "No thanks", [P("They shrug and drink it themselves. They look disappointed, but nobody pushes. At Zoe's, a no always works.")], [go("Leave them to it.", loc="zoe_apartment", mins=2)]),
        node("drunk", "Down in one", [
            G(cond(trait("drinks_tonight", "lt", 3)), P("You knock it back in one. It burns all the way down, and a cheer goes up from whoever's nearest. A minute later the room is warmer, the music is louder, and your cheeks are hot.")),
            G(cond(trait("drinks_tonight", "gte", 3)), P("Three. The room tips when you turn your head, your lips have gone numb, and somebody's hand is on the small of your back keeping you upright, and you let it stay.")),
        ], [go("Find Zoe.", loc="zoe_apartment")])]})

FLASH = ("\"Flash them, babe. Three seconds,\" Zoe says. The circle goes quiet. You pull everything up to your chin, and your tits drop out into the warm air, bare to people you sit next to in class. Your nipples go hard at once, tight and dark, while every eye lands on them. \"One,\" Zoe calls. Somebody whistles. A guy on the couch forgets the drink halfway to his mouth. \"Two.\" Your chest heaves, so your tits bounce with it. \"Three.\" You hold them out a breath past the count, nipples stiff and aching, before you let everything drop.")
# false lines a3 #29 (DECISIONS 129): the dare is "till the song ends", so its second entry runs on the song, not a count of three
FLASH_SONG = ("\"Till the song ends, babe,\" Zoe says, and turns the music up. The kitchen goes quiet under it. You pull everything up to your chin, and your tits drop out into the warm air, bare to people you sit next to in class. Your nipples go hard at once, tight and dark, while every eye lands on them. Somebody whistles. A guy at the counter forgets the drink halfway to his mouth. The chorus comes round again. Your chest heaves, so your tits bounce with it. The last note goes, and you hold them out a breath past it, nipples stiff and aching, before you let everything drop.")
# ── Zoe's dares (zoe_dares.md, signed 2026-11-01): her hot repeatable after her step 4, replacing party_dare. One a
#    party night, Zoe picks; a showing yes, a doing yes, the no; three tiers, flat cases. At Zoe's Friday party, late,
#    where the regulars are (the cocky guy's rows: Friday 23:00 to 02:00); the party-house Saturday has none of them. ──
from sheetbeats import beat
D_ = lambda key: beat("zoe_dares", key)
TOGETHER, APART = flag("zoe_together"), flag("zoe_together", False)
# DECISIONS 124: the room watches every dare but the kiss, and a watched act is Watched (Exhibitionism 60).
TIER = {"low": [[trait("exhibitionism", "lt", 60)]],
        "high": [[APART, trait("exhibitionism", "gte", 60)]],
        "z": [[TOGETHER, trait("exhibitionism", "gte", 60)]]}
ZOE_LINE = {"low": "Kiss the cocky guy. Properly. Tongue, hands, the lot.",
            "high": "Flash the guy at the keg. Or topless in the kitchen till the song ends. Or the cocky guy's lap, till he's hard. Make him beg.",
            "z": "Kiss me where they can see. Or let me watch you with him."}
# pass 4 (A68 rule, LO 2026-11-04): an act a group watches needs both meters at stage 4, Corruption 60 and
# Exhibitionism 60 (the tier holds the Exhibitionism 60). Every dare but the kiss is watched (DECISIONS 124), so each
# watched yes reads Corruption 60 too, and it pays inside stage 4 (cap 79, PAY below).
WATCHED = [trait("corruption", "gte", 60)]
YESES = {"low": [("\"Watch this.\"", "low_do", [trait("corruption", "gte", 20)], "Needs Corruption 20", "cocky")],
         "high": [("\"Watch me.\"", "low_show", WATCHED, "Needs Corruption 60", "keg"),
                  ("\"Start the song.\"", "high_show", WATCHED, "Needs Corruption 60", "keg"),
                  ("\"Easy.\"", "high_do", WATCHED, "Needs Corruption 60", "cocky")],
         "z": [("\"Here?\"", "z_show", WATCHED, "Needs Corruption 60", "cocky"),
               ("\"Watch, then.\"", "z_do", WATCHED, "Needs Corruption 60", "cocky")]}
# pass 4 D18: a doing dare is a sex rung, so it costs energy like the other acts (heat_a ACT_COSTS): greyed
# "Requires 10 Energy" when she is spent (the-surfaces.md R3c)
DARE_COSTS = {"high_do": [{"trait": "energy", "value": 10}], "z_do": [{"trait": "energy", "value": 10}]}
PAY = {"low_show": [capped("exhibitionism", 1, 79)],
       "low_do": [capped("corruption", 1, CAP_CUR), capped("exhibitionism", 1, CAP_CUR)],
       "high_show": [capped("exhibitionism", 1, 79), capped("corruption", 1, 79)],
       "high_do": [capped("corruption", 1, 79), capped("exhibitionism", 1, 79)],
       "z_show": [capped("corruption", 1, 79), capped("exhibitionism", 1, 79)],
       "z_do": [capped("corruption", 1, 79), capped("exhibitionism", 1, 79)]}
MEDIA = {"low_show": VID("a girl flashing her breasts at a guy by a keg at a house party", "girl flashes guy at keg party", "party flash dare keg", pool_dir="sex/zoe_dare_low_show_t4"),
         "low_do": VID("a girl kissing a guy hard at a party, his hands on her ass, people cheering", "girl kisses guy at party dare", "dare kiss party hands on ass", pool_dir="sex/zoe_dare_low_do_t3"),
         "high_show": VID("a topless girl in a crowded party kitchen, everyone staring", "topless girl party kitchen", "topless dare at party", pool_dir="sex/zoe_dare_high_show_t4"),
         "high_do": VID("a girl grinding in a guy's lap on a party couch, him begging", "lap grind party couch dare", "girl grinds on guy's lap party", pool_dir="sex/zoe_dare_high_do_t4"),
         "z_show": VID("two girls making out in the middle of a house party, the room staring", "girls kissing at party everyone watching", "lesbian kiss party dare", pool_dir="sex/zoe_dare_z_show_t4"),
         "z_do": VID("a girl making out in a guy's lap on a party couch while her girlfriend watches and directs", "girl makes out with guy while girlfriend watches", "party couch girlfriend watching", pool_dir="sex/zoe_dare_z_do_t4")}
JAKE_LINE = {"cocky": "He's Jake's teammate. He'll tell Jake, or he won't.", "keg": "Half this party knows Jake."}
REGULAR_FLAG = {"cocky": "cocky_guy_dared", "keg": "keg_guy_dared"}
# pass 3 B4: the room talks after each dare (the keg guy has no NPC: WHO, speaker "unknown")
DARE_SAID = {"low_show": [WHO("Holy shit. Again. Do it again."), D(Z, "That's my girl. His drinks are yours now.")],
             "low_do": [D(C, "Fuck. Zoe should dare you more often."), D(Z, "Okay, okay, break it up before he proposes.")],
             "high_show": [WHO("Zoe, your friends are the best thing about this party."), D(Z, "Covered or not, babe, nobody here is forgetting those.")],
             "high_do": [D(C, "Please. Fuck. Please, okay? I'm begging."), D(Z, "You heard him. He begged. Dare done.")],
             "z_show": [D(Z, "Mm. You taste good. Again."), ME("Everyone's watching us."), D(Z, "That's the point, babe.")],
             "z_do": [D(Z, "Slower. Make him wait for it."), D(C, "Jesus Christ, you two are going to kill me.")]}
# scene reader 2026-11-04 (her voice): "It doesn't count" is pushback, and at Hungry she isn't pushing back. The kiss
# opens at Corruption 20, so three bands. Moved out of the low_do beat (zoe_dares.md) so the beat stays on the body.
LOW_DO_THOUGHT = [G(cond(trait("corruption", "lt", 40)), T("It's a dare. It doesn't count.")),
                  G(cond(trait("corruption", "gte", 40), trait("corruption", "lt", 60)), T("It's a dare. So why do you want to go back for more?")),
                  G(cond(trait("corruption", "gte", 60)), T("Dare, my ass. You wanted his tongue in your mouth before she said a word."))]
# scene reader b03 (2026-11-03): a dare beat that says "your top" is true only in a top. canv.top_or_dress keys on the
# two going-out dresses being off, so in a cafe uniform, or in only a bra, it named a top she wasn't wearing. Here each
# beat is worded for what is on: a top, a dress-slot item (the two dresses, the uniforms), a bra and nothing over it, bare.
UNIFORMS = ("cafe_uniform_normal", "cafe_uniform_sexy", "cafe_uniform_short", "cafe_uniform_lowcut")
def slot(s, on=True): return {"type": "clothing_slot", "slot": s, "operator": "equipped" if on else "unequipped"}
NO_TOP_BRA = {   # (old, new) per beat: a bra and nothing over it
    "low_show": [("You grab your top and everything under it and yank it all up to your chin.", "You grab your bra and yank it up to your chin."),
                 ("You pull your top down over your hard nipples, and your tits still tingle under it.", "You pull your bra back down over your hard nipples, and your tits still tingle under it.")],
    "low_do": [("Your nipples go hard under your top, and he feels them.", "Your nipples go hard through your bra, and he feels them.")],
    "high_do": [("Your nipples are tight against your top, and you're wet.", "Your nipples are tight against your bra, and you're wet.")],
    "z_do": [("His hands slide up under your top, shove aside whatever's in the way, and close on your bare tits.", "His hands push up under your bra and close on your bare tits.")]}
NO_TOP_BARE = {   # nothing on top at all
    "low_show": [("You grab your top and everything under it and yank it all up to your chin. Your tits are bare to him", "You're already bare on top, and you push your tits right out at him. They're bare to him"),
                 ("You pull your top down over your hard nipples, and your tits still tingle under it.", "You cross your arms over your hard nipples, and your tits still tingle under them.")],
    "low_do": [("Your nipples go hard under your top, and he feels them.", "Your bare nipples go hard against his shirt, and he feels them.")],
    "high_do": [("Your nipples are tight against your top, and you're wet.", "Your bare nipples are tight in the open air, and you're wet.")],
    "z_do": [("His hands slide up under your top, shove aside whatever's in the way, and close on your bare tits.", "His hands slide up your stomach and close on your bare tits.")]}


def _swap(text, pairs):
    for a, b in pairs:
        assert a in text, (a, text[:60])
        text = text.replace(a, b)
    return text


def dare_by_top(key, text):
    """The beat as one chain of groups by what she has on top (see NO_TOP_BRA)."""
    if "your top" not in text:
        return [P(text)]
    # fix_g3c: one beat, only the differing sentences chained (canv.chain_by_sentence); the else is the dress slot
    # itself (an exact check, not worn_exposure): every case not above has some other dress-slot item on
    return chain_by_sentence([(cond(slot("top"), slot("dress", False)), text)]
            + [(cond({"type": "clothing_item", "item_id": d, "operator": "equipped"}), text.replace("your top", "your dress")) for d in DRESSES]
            + [(cond({"type": "clothing_item", "item_id": u, "operator": "equipped"}), text.replace("your top", "your dress" if u in ("cafe_uniform_short", "cafe_uniform_lowcut") else "your uniform")) for u in UNIFORMS]
            + [(cond(slot("top", False), slot("dress", False), slot("bra")), _swap(text, NO_TOP_BRA[key])),
               (cond(slot("top", False), slot("dress", False), slot("bra", False)), _swap(text, NO_TOP_BARE[key])),
               (cond(slot("dress")), text.replace("your top", "your clothes"))])   # any other dress-slot item


dare_choices, dare_nodes = [], []
for tier, cases in TIER.items():
    for nm, key, gate, locked, who in YESES[tier]:
        for items in cases:
            dare_choices.append(go(nm, node=key, mins=10, cond_=cond(*items, *gate), costs=DARE_COSTS.get(key)))
for key in PAY:
    blocks = dare_by_top(key, D_(key)) if key != "high_show" else [POOL(P(D_(key)), P(FLASH_SONG), pid="zoe_dare_high_show", bag=True)]
    who = "keg" if key in ("low_show", "high_show") else "cocky"
    blocks += [MEDIA[key], *DARE_SAID[key], *(LOW_DO_THOUGHT if key == "low_do" else []), G(cond(trait("jake_step", "gte", 3)), T(JAKE_LINE[who]))]
    dare_nodes.append(node(key, "The dare", blocks, [
        go("Back to the party.", loc="zoe_apartment", mins=20, cond_=cond(flag("zoe_dared", False)),
           eff=PAY[key] + [add("zoe_dares_done", 1, clamp=False), add("campus_talk", 1, clamp=False)],
           flags=[fset(REGULAR_FLAG[who])]),
        go("Back to the party.", loc="zoe_apartment", mins=20, cond_=cond(flag("zoe_dared")))]))
out.append({
    "id": "zoe_dares", "name": "Take Zoe's dare",   # pass 4 H33: a room-list label says what the click does
    "description": "Zoe's dares (release 1): after her step 4, one a party night at her Friday party, late. Zoe picks; a showing yes and a doing yes by her stage, the no; three tiers. Each yes counts toward her step 5. Corruption 60 locked.",
    "trigger": {"location": "zoe_apartment", "requires_npc": Z, "is_repeatable": True, "priority": 4, "is_active": True,
                # after midnight, so the day roll (which clears zoe_dared) can't open a second dare the same party night
                "schedules": [{"weekdays": [5], "start_time": "00:00", "end_time": "01:50"}],   # false lines a3: a yes is 10 minutes, the cocky guy leaves at 02:00
                "conditions": cond(AT_PARTY, flag("picks_the_dares"), flag("zoe_dared", False), flag("cocky_guy_met"))},
    "nodes": [
        node("dare", "Zoe's dare", [
            P("Zoe finds you in the crush, hooks her chin over your shoulder, and looks round the room like she's shopping."),
            *[G(cond(*items), D(Z, ZOE_LINE[t])) for t, cs in TIER.items() for items in cs],
            G(cond(flag("keg_guy_dared")), P("The guy at the keg sees you and grins."), WHO("You again. Back for more?")),
            G(cond(flag("cocky_guy_dared"), {"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": C, "operator": "is_present"}),
              D(C, "You again. Come here.")),
        ], dare_choices + [
            go("\"Not tonight.\"", node="no", mins=1),
        ]),
        *dare_nodes,
        node("no", "Boo", [ME("Not tonight, Zoe."), D(Z, "Boo. Next Friday, then."), P("She goes and dares the guy on the couch to drink something from the sink instead. He does.")],
             [go("Let her have her dare.", loc="zoe_apartment", mins=10, flags=[fset("party_cool_zoe")])]),   # pass 3 D39 (R7)
    ]})
# one a party night: the dare's choices set zoe_dared; arriving at the party clears it
for _n in out[-1]["nodes"]:
    for _c in _n["choices"]:
        if _c.get("targetType") == "location":
            _c["flagEffects"] = list(_c.get("flagEffects") or []) + [fset("zoe_dared")]

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
            P("Jake's teammate, the cocky one from figure drawing, is leaning on the wall by Zoe's bathroom with a beer he's barely touched. He's been watching you since he came in. When you pass, he pushes off the wall."),
            D(C, "Bathroom's free. Just saying."),
            G(cond(flag("cocky_exam_deal")), D(C, "You still owe me for that exam. Or I owe you. Can't remember which.")),
        ], [
            go("\"Lead the way.\"", node="door", mins=2, flags=[fset("hookup_today")]),
            go("\"Not tonight.\"", node="no", mins=1),
        ]),
        node("door", "Locked", [
            P("Zoe's bathroom: fairy lights round the mirror, her makeup all over the sink. He locks the door. The party is right there through the wall, and he's looking at you like he's already decided."),
        # pass 3 E95: sex costs her 10 energy (greyed "Requires 10 Energy" when spent) and lowers hygiene (board.needs)
        ], [go("Get on your knees.", node="oral", mins=2, costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]), go("Pull him in.", node="sex", mins=2, costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]), go("Unlock the door.", node="no", mins=1)]),
        node("oral", "On your knees", [P(ORAL),
            VID("a girl on her knees on a bathroom floor at a party sucking a guy's cock as he leans on the sink", "blowjob party bathroom on knees", "girl sucks cock locked bathroom party", pool_dir="sex/party_hookup_oral_t5"),
            # pass 3 G23: the act ends on his aftermath line, before the exit
            P("He sags back against the sink with his cock still wet from your mouth and fumbles his jeans shut."),
            D(C, "Fuck. Does Jake have any idea what he's missing?")],
            [go("Back to the party.", node="out", mins=15, eff=[capped("corruption", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        node("sex", "On the sink", [P(SEX),
            VID("a couple having sex on a bathroom sink at a party, her legs locked round him, the mirror fogged", "sex on bathroom sink party", "fucking on the sink at a house party", pool_dir="sex/party_hookup_sex_t5"),
            P("He stays buried in you, panting, then lifts you down off the sink. His cum runs down the inside of your thigh."),
            D(C, "Fix your hair. They're all going to know anyway.")],
            [go("Back to the party.", node="out", mins=20, eff=[capped("corruption", 1, CAP_BOLD), add("campus_talk", 1, clamp=False)])]),
        # truth pass (2026-11-03): 15-20 minutes on, Zoe's Friday-night row may be over (it ends 02:00): her lines
        # only while she is still at the flat
        node("out", "Back out", [
          *pin_blocks([
            P("You come out first, fixing your hair. Zoe's in the hall with a drink in each hand. She looks at you, and at the bathroom door, and at him coming out behind you, and her mouth opens."),
            D(Z, "In my bathroom? Babe."),
          ], here_at(Z, "zoe_apartment")),
            T("By Monday half of campus will know. You find you don't mind."),
        ], [go("Go back to the party.", loc="zoe_apartment", mins=5)]),
        node("no", "Not tonight", [D(C, "Your loss."), P("He goes back to his wall and his beer, grinning, still watching you.")], [go("Leave him to his wall.", loc="zoe_apartment", mins=2, flags=[fset("party_cool_cocky_guy")])]),
    ]})

# ═════════════ THE PARK ═════════════
SPORTS_ONLY = cond({"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"})
DARING_RUN = cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                  {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, logic="OR")

out.append({
    "id": "park_walk", "name": "Walk the path",
    "description": "A walk in the park: who she passes, what they see. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("path", "The path", [
        POOL(P("You walk the loop round the pond. Ducks, dog walkers, a man on a bench with a newspaper. He's reading it, but he lowers it as you pass."),
             P("The wind comes off the water, cold enough to make you hug yourself. A jogger turns his head to watch you go by, and nearly runs into a bin."),
             P("Two guys playing frisbee stop playing frisbee while you walk past. One of them says something. The other one laughs."), pid="park_walk_lines"),
        # reader a3 #62 (DECISIONS 131): letting a stranger see her ass is her choice at Showing, as town_event_wind's
        # "Let it blow." (E40); under it the same gust is an accident and she grabs the hem.
        GC(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}, trait("exhibitionism", "lt", 40)),
           P("The skirt is a problem in this wind. It flips up over your ass, and a dog walker stops dead on the path to stare. You grab the hem in both fists and hold it down the rest of the loop, your face burning.")),
        GC(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}, trait("exhibitionism", "gte", 40)),
           P("The skirt is a problem in this wind. It flips up over your ass, and a dog walker stops dead on the path to stare. You let it be a problem.")),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), P("No bra, and the air is cool. Every man on the path finds a reason to look at your chest.")),
    ], [go("Finish the loop.", loc="park", mins=30)])]})

out.append({
    "id": "park_run", "name": "Run",
    "description": "A run (energy 10) or a walk. What she runs in decides who looks; Daring clothes (no bra, or a bra and no top): Exhibitionism +1. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1},
    # reader a3 #67 (DECISIONS 131): the run is shown only after she picks it; "Walk it instead." gets its own screen.
    "nodes": [node("gates", "The gates", [
        P("You stretch against the park gates. The loop round the pond is two laps if you mean it."),
        # writing pass: her voice at her level
        GC(cond(trait("exhibitionism", "lt", 20)), T("Head down, two laps. Nobody needs to look at you.")),
        GC(cond(trait("exhibitionism", "lt", 40)), T("Somebody on that loop is going to look. You wonder who.")),
        GC(cond(trait("exhibitionism", "lt", 60)), T("Take it past the benches. Let them look.")),
        GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), T("You want every man on that loop turning his head.")),
    ], [
        go("Run the loop. (10 energy)", node="run", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), eff=[capped("exhibitionism", 1, CAP_CUR)]),   # LO, 2026-11-04: a dress-code act pays to the top of the stage its dress code needs (a meter at 20)
        go("Run the loop. (10 energy)", node="run", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}), eff=[capped("exhibitionism", 1, CAP_CUR)]),
        go("Run the loop. (10 energy)", node="run", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "equipped"})),   # a dress empties the top slot, so it is not "no top": no dress code, no pay
        # exhibition phase 1 (LO, 2026-11-08): dressed in leggings under Daring, the run has its own screen, so the third
        # lap is the only pay on that way through (gate `a visit pays a meter once`)
        go("Run the loop. (10 energy)", node="run_plain", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "leggings"}, trait("exhibitionism", "lt", 20))),
        go("Run the loop. (10 energy)", node="run", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "worn_type", "operator": "neq", "value": "leggings"})),
        go("Run the loop. (10 energy)", node="run", mins=35, costs=[{"trait": "energy", "value": 10}], cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "leggings"}, trait("exhibitionism", "gte", 20))),
        go("Walk it instead.", node="walk", mins=20),
    ]),
        node("run", "A run", [
        G(cond({"type": "worn_type", "operator": "eq", "value": "leggings"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_item", "item_id": "gym_tank", "operator": "unequipped"}),
          P("Leggings and a top, the normal way. You run the loop twice and your lungs burn and nobody looks twice, except the old man on the bench who looks at everybody.")),
        G(cond(*SPORTS_ONLY["items"], {"type": "worn_type", "operator": "eq", "value": "leggings"}), P("Just the sports bra and your leggings, and it's like you've set off an alarm. Heads turn on the whole loop. A guy doing push-ups stops at the top of one and stays there, his eyes on your tits bouncing in the bra. He doesn't call anything after you. Not yet.")),   # scene reader b03: the not-yet (H4.3)
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}),
          P("No bra under your top, and every stride shows it: your tits bounce, your nipples hard against the cloth. A cyclist wobbles. A man walking his dog lets the dog walk him into a hedge. One of them calls something after you, but you don't slow down.")),
        # the gym clothes (DECISIONS 198; GYM_CLOTHES_PLAN.md §6): the park reads each step too. Lines only; the park's pay is unchanged.
        G(cond({"type": "worn_type", "operator": "eq", "value": "track_pants"}, {"type": "clothing_item", "item_id": "tshirt", "operator": "equipped"}, {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}),
          P("Track pants and a T-shirt. You run the loop twice and nobody looks at you once, which is what track pants are for.")),
        G(cond({"type": "clothing_item", "item_id": "gym_tank", "operator": "equipped"}, {"type": "worn_type", "operator": "neq", "value": "gym_shorts"}),
          P("The fitted gym tank shows every bounce. Two guys on the benches by the pond stop talking as you go past, both laps, and watch you all the way round.")),
        G(cond({"type": "worn_type", "operator": "eq", "value": "gym_shorts"}, *SPORTS_ONLY["items"]),
          P("Just the sports bra and the tiny shorts. The shorts are up your ass by the first bend and stay there. The whole loop watches you run it: a cyclist, two dog walkers, the guys at the pull-up bars. Somebody whistles, and you don't look round.")),
        G(cond({"type": "worn_type", "operator": "eq", "value": "gym_shorts"}, {"type": "clothing_slot", "slot": "top", "operator": "equipped"}),
          P("The tiny shorts ride up your ass with every stride, and you leave them there. The men on the benches turn their heads to watch you all the way round.")),
        G(cond({"type": "clothing_item", "item_id": "plain_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}, {"type": "worn_type", "operator": "neq", "value": "leggings"}),
          P("Just your bra on top. Every man on the loop looks at your tits bouncing in it, both laps, and a guy at the pull-up bars drops off the bar to watch.")),
        G(cond(*SPORTS_ONLY["items"], {"type": "worn_type", "operator": "eq", "value": "track_pants"}),
          P("Just the sports bra over your track pants. Your tits bounce in it on every stride, and the men on the benches by the pond watch you both laps.")),
        G(cond({"type": "worn_type", "operator": "eq", "value": "sheer_leggings"}, {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}),
          P("In the sun the sheer leggings go see-through. Your panties show on every stride, and somebody behind you can't keep quiet about it."), WHO("Oh my God.")),
        G(cond({"type": "worn_type", "operator": "eq", "value": "sheer_leggings"}, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}),
          P("In the sun the sheer leggings go see-through, and there's nothing under them. Your ass and your pussy show on every stride. A man on a bench stands up to watch you go round.")),
        POOL(P("You finish at the gates with your hands on your knees, sweating, buzzing."), P("Your legs are jelly by the end. Your face is red and not only from running.")),
        # reader a3 #44 (DECISIONS 131): the hook. Zoe's park row is Saturday and Sunday 08:00-10:00 once met
        # (people_data.py); when she's out on the loop right now, the line says so.
        G(cond(flag("zoe_met"), here_at(Z, "park")), P("Zoe's still out on the loop somewhere. She'd make you go further.")),
        G(cond(flag("zoe_met"), {"type": "npc_at_location", "location_id": "park", "npc_id": Z, "operator": "is_absent"}),
          P("Zoe runs here weekends. She'd make you go further.")),
        G(cond(flag("zoe_met", False)), P("Same time tomorrow.")),
    ], [go("Cool down.", loc="park", mins=5)]),
        # exhibition phase 1 (LO, 2026-11-08): in leggings and a top, under Daring, the man on the bench looks; she runs past him again
        node("run_plain", "A run", [
            P("Two laps in your leggings, and your lungs burn. The man on the bench by the pond watches your ass the whole way round, both times."),
        ], [go("Run past his bench again.", node="lap3", mins=10,
               eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}]),
            go("Cool down where he can't see.", node="cool_plain", mins=5)]),
        node("cool_plain", "The gates", [
            P("You stretch out at the gates with your back to his bench. When you look round, he's gone back to his paper. He's there most mornings."),
        ], [go("Back to the park.", loc="park", mins=1)]),
        node("lap3", "A third lap", [
            P("He doesn't pretend otherwise when you come round again. You take a third lap, right past him. He lowers his paper and opens his mouth to say something, then doesn't. Not today. You don't look back, and your cheeks burn anyway."),
            GC(cond(trait("exhibitionism", "lt", 5)), T("It's a public park. Anyone can look.")),
            GC(cond(trait("exhibitionism", "lt", 10)), T("You went round again for him.")),
            GC(cond(trait("exhibitionism", "lt", 15)), T("You slowed down past his bench.")),
            GC(cond(trait("exhibitionism", "lt", 20)), T("Next time, something he can see more of.")),
            P("He's on that bench most mornings."),
        ], [go("Cool down.", loc="park", mins=5)]),
        node("walk", "A walk", [
            P("You walk the loop instead, slow, and let the runners go past you both ways, red-faced and blowing. A man on the bench by the pond watches you all the way round. His eyes go down your legs and back up to your tits, but he doesn't look away when you catch him."),
            # reader a3 verify (DECISIONS 131): her not-yet; scene reader 2026-11-04: the middle bands only
            G(cond(trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 60)), T("Let him look. That's all he gets.")),
            # scene reader 2026-11-04: the other bands get theirs on the body too
            G(cond(trait("exhibitionism", "lt", 20)), P("You cross your arms over your chest and walk faster. Your face is hot, and he doesn't get another look.")),
            G(cond(trait("exhibitionism", "gte", 60)), P("You slow down right in front of him and roll your shoulders back, so your tits lift, and you keep walking. His mouth opens. Not today.")),
        ], [go("Back to the gates.", loc="park", mins=2)]),
    ]})

out.append({
    "id": "park_rest", "name": "Rest on a bench",
    "description": "A bench in the sun: energy +5, once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("bench", "A bench", [POOL(
        P("You sit on a bench by the pond with your face tipped up to the sky and your eyes shut. Your shoulders come down from round your ears."),
        P("You lie along a bench with your knees up and watch the clouds. A man walks past slowly, twice."))],
        [go("Get up.", loc="park", mins=30, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}])])]})

out.append({
    "id": "park_selfie", "name": "Take a selfie on the path",
    "description": "Photos on the path, a man on a bench watching her pose: Exhibitionism +1. Once a day. Posting is the phone's (pass 3 F64): followers move only on the Feed.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("photo", "A selfie", [
        # Iteration 002, part 8 (reader): nothing is posted until she posts it.
        P("You find a spot by the willow and take twenty photos to get one. A man on a bench watches you do it, every angle, his eyes on your ass each time you bend for the shot. He folds his paper into his lap. Whatever you post stays up for anyone to see."),
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("The best one is the one where the wind has the skirt, and your ass is half out of it. Post that, and everyone who follows you sees it, for good.")),
        G(SPORTS_ONLY, P("Sports bra, sweat, the pond behind you.")),
        # reader a3 #61 (DECISIONS 131): a photo of her on show pays from Daring (SP2 stage 2); under it, a not-yet
        G(cond(trait("exhibitionism", "lt", 20)), T("Put yourself up where anyone can look? Not yet.")),
    ], [  # DECISIONS 124: the skirt photo on her feed is a flash for a group, Watched
        # (pass 3 F64, the-phone.md P6 "the phone owns posting") she keeps the shot here; the Feed posts it
        go("Keep the best one.", node="posted", mins=10, cond_=cond({"type": "worn_type", "operator": "neq", "value": "short_skirt"}, trait("exhibitionism", "gte", 20)), eff=[capped("exhibitionism", 1, CAP_CUR)]),   # a Daring post stops at Daring's top (pass 3 G8)
        go("Keep the best one.", node="posted", mins=10, cond_=cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}, trait("exhibitionism", "gte", 60)), eff=[capped("exhibitionism", 1, 79)]),
        go("Delete them all.", loc="park", mins=5)]),
        node("posted", "Kept", [
            P("You keep the best one. It's on your phone now, one tap from your feed, and the man on the bench is still staring at you."),
        ], [go("Put the phone away.", loc="park", mins=5)])]})

# Step 4 (DECISIONS 79): `run` stops before he looks up; her choice to stay is `linger`, which pays.
RUN_SEEN = ("A sound comes from behind the bushes, low and wet and steady. You step off the path to look, straight into them. A man and a woman, both naked from the waist down, and they don't see you. She is bent over a fallen log, palms flat on the bark. He holds her hips from behind. His cock slides out of her, slick, then drives back in. Her tits swing under her with every thrust. His hand comes down on her ass and stays there, squeezing hard. You stare a second too long, and your face goes hot. She moans, loud, mouth open, his cock still driving into her.")
LINGER = ("You stay. You make yourself look. The man is naked from the waist down, and his cock is thick and shining wet. He pulls almost all the way out of her, then drives back in. The woman is bent over the log with her tits swinging under her. She moans every time he hits bottom. His hands grip her ass hard enough to leave marks. Your nipples go tight and ache. Heat pours down your belly, and you are wet, so wet it shocks you. Then the man looks up. He stares straight at you, still buried deep inside her. You run. Your legs shake under you. Your heart slams against your ribs. Your thighs slide together, slick, with every step.")
WATCH = ("You crouch behind the rhododendron and part the leaves. A man has a woman bent against a tree, her palms flat on the bark. His cock slides out of her, slick and shining, then thrusts back in to the root. Every thrust makes a wet slap you can hear from here. He fills his hands with her tits and pinches her nipples hard. She moans loud, bites her lip, but can't hold the next one in. Her face is red, eyes shut, mouth hanging open. You stare at his cock. Your nipples go tight, and heat floods between your thighs. You press your hand flat on your stomach and keep it there. He drags her ass back onto his cock, faster, until her moans break into short, wet gasps.")
TOUCH = ("Behind the rhododendron, you can see everything. The man has the woman pinned to the tree, a hand full of each of her tits. His cock drives into her, hard and steady, and she moans on every stroke. Your hand slides down your belly and inside. Your fingers find your clit, and you are already wet. You match him. Each time he thrusts, you rub, fast and tight. Her nipples stand stiff between his fingers while her ass slaps the bark. You bite your lip so no sound gets out. Neither of them looks toward the bush. He groans and buries his cock deep, and you come with him. Your knees buckle, and your free hand grips a branch while your fingers keep working your clit through it.")
out.append({
    "id": "park_watch_the_couple", "name": "Walk the far path",
    "description": "The first explicit scene (LO, question 8): a couple in the bushes, strangers. Good Girl: she walks into them and runs. Curious: she watches, then touches herself. Once a day.",
    "trigger": {"location": "park", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                # starts by 21:30: the longest path is 21 minutes, so every exit lands before the 22:00 lock (reader item 5)
                "conditions": cond(flag("opening_done"), tod("07:00", "21:30")),
                # pass 3 H64: a walk she chooses, windowed by a condition, so it says its hours when shut (C5)
                "show_when_blocked": True, "cooldown_message": "Every day, 7 AM-9:30 PM, once a day"},
    "nodes": [
        node("sound", "The far path", [
            P("The far path behind the rhododendrons is empty and quiet. Then it isn't: a sound off to the left, through the leaves, low and rhythmic. Your face goes hot, and your nipples go tight."),
            WHO("Hold still. Hold still for me."),   # writing pass: low heat (H4), the man, through the leaves
            G(cond(CURIOUS), T("You know exactly what that is. You could leave, but you don't want to.")),
            # writing pass: the price; scene reader 2026-11-04: from visit 2 she has already seen
            G(cond(trait("corruption", "lt", 20), flag("saw_the_couple", False)), T("One step off this path and you can't say you didn't see.")),
            G(cond(trait("corruption", "lt", 20), flag("saw_the_couple")), T("You know what's behind those leaves. You saw it last time. Your face burns.")),
        ], [
            go("Step off the path to look.", node="run", mins=3, cond_=cond(trait("corruption", "lt", 20))),
            go("Stay and watch.", node="watch", mins=5, cond_=cond(CURIOUS)),
            go("Walk the other way.", node="away", mins=2),
        ]),
        node("run", "Run", [P(RUN_SEEN), WHO("Oh God. Harder. Don't you dare stop."), WHO("Fuck, you're so wet. Somebody's going to hear you.")],   # LO 2026-11-03: the woman
            [go("Look a second longer.", node="linger", mins=3, flags=[fset("saw_the_couple")]),
             go("Run.", loc="park", mins=15, flags=[fset("saw_the_couple")])]),
        node("linger", "A second longer", [P(LINGER), P("Behind you, the man laughs."), WHO("Come back! She likes being watched!"), WHO("Don't, Dan. Oh God, don't stop."),
            VID("a couple having sex against a log in the bushes of a park, the man looks up", "couple fucking in park bushes caught", "outdoor sex in park man looks up", pool_dir="sex/park_couple_run_t5")],
            [go("Keep walking.", loc="park", mins=15, eff=[capped("corruption", 1, CAP_GG)], flags=[fset("saw_the_couple")])]),
        node("watch", "Watch", [P("Behind you on the path a jogger thuds past. You hold your breath until he's gone."), P(WATCH),
            WHO("Look at you, taking all of my cock. Moan for me."),   # LO 2026-11-03: the man
            WHO("Yes. Yes. Fuck me harder, right there, right there."),
            VID("seen through leaves, a man fucking a woman bent against a tree in a park", "voyeur watching couple fuck in park", "hidden in bushes watching outdoor sex", pool_dir="sex/park_couple_watch_t5")],
            [go("Leave before they see.", loc="park", mins=10, eff=[capped("corruption", 1, CAP_CUR)], flags=[fset("saw_the_couple")]),
             go("Touch yourself while you watch.", node="touch", mins=5)]),
        node("touch", "With him", [P("A dog barks somewhere along the path, and you freeze with your hand on your belly, but nobody comes."), P(TOUCH),
            WHO("Take it. Take all of it."), WHO("I'm coming. Oh God, I'm coming."),
            VID("a girl hidden in bushes touching herself while watching a couple have sex against a tree", "girl masturbating watching couple outdoors", "voyeur girl fingers herself in park", pool_dir="sex/park_couple_touch_t5")],
            [go("Slip away.", loc="park", mins=10, eff=[capped("corruption", 1, CAP_CUR)], flags=[fset("saw_the_couple")])]),
        node("away", "The other way", [P("You turn round and walk the other way, fast, and don't look back, but your face is burning and your nipples are still tight. You can hear them all the way to the pond. Not today.")], [go("Back to the pond.", loc="park", mins=10)]),
    ]})

HIDDEN = ("Zoe drags you off the path into the hollow behind the rhododendrons. Joggers pound past a few yards away. She shoves you against a tree and kisses you hard, both of you still panting from the run. \"Quiet, babe,\" she breathes. Her hand slides down inside, flat on your skin, and finds you wet. Her fingers start slow. You grab her ass and pull her in. Her thumb finds your nipple and rubs. Footsteps crunch past, close enough to touch, but Zoe doesn't stop. Her fingers go fast, deep, until your hips buck into her hand. Your orgasm hits and your knees give out. Zoe pins you to the bark with her whole body, her mouth on yours to swallow every moan.")
out.append({
    "id": "park_hidden", "name": "Let Zoe finger you off the path",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "After the run with Zoe, weekend mornings (park_hidden): a hollow off the path, Zoe's hand, nobody sees. Bold, after Zoe A 3. Once a day.",
    "trigger": {"location": "park", "requires_npc": Z, "is_repeatable": True, "priority": 5, "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [5, 6], "start_time": "08:00", "end_time": "09:30"}],   # done before her park row ends at 10:00
                # after a run with her (the "Run a lap with her" button, within the hour): park_hidden.md (part 8, reader)
                "conditions": cond(trait("corruption", "gte", 60), trait("zoe_step", "gte", 3), flag("ran_with_zoe"),   # strangers able to see: Hungry (DECISIONS 124)
                                   {"type": "hours_since_flag", "subject": "player", "flag_key": "ran_with_zoe", "operator": "lt", "value": 1})},
    "nodes": [
        node("pull", "After the run", [P("Zoe jogs to a stop beside you, pink and breathless, and grabs your wrist."), D(Z, "Come here. I know a place.")],
             [go("Follow her.", node="hidden", mins=5, costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]), go("\"Not here, Zo.\"", node="no", mins=1)]),   # pass 3 E95
        node("hidden", "The hollow", [P("A man walking his dog slows on the path above the hollow, looks your way, and walks on."), P(HIDDEN),
            VID("two girls in running clothes hidden in bushes, one with her hand down the other's leggings, kissing against a tree", "girl fingers girlfriend in park bushes", "lesbian hidden in park hand down leggings", pool_dir="sex/park_hidden_t5")],
            [go("Back to the path.", node="after", mins=15, eff=[capped("corruption", 1, 79)])]),
        node("after", "Back on the path", [D(Z, "Same time next weekend. Don't be late."), P("She jogs off backwards, grinning, and doesn't fix her hair.")], [go("\"Don't you be late.\"", loc="park", mins=2)]),
        node("no", "Not here", [D(Z, "Your loss, babe."), P("She laughs and runs off ahead, looking back over her shoulder every few strides.")], [go("Let her run on.", loc="park", mins=5)]),   # reader a3 #53 (DECISIONS 131): park_cool_zoe was read by nothing; Zoe has no Want to cost (validator), so the no is her line
    ]})

# ═════════════ TOUCHING HERSELF (from Curious; DECISIONS 13) ═════════════
BED = ("Your door is shut, but someone's TV mutters down the hall. Under the sheet, you slide a hand up and squeeze your tits. You pinch a nipple until it goes hard between your fingers, and the jolt runs straight down to your clit. So you follow it down. You're wet already, and you want to know how much more you can take. Two fingers circle your clit, slow, until your hips start to lift. Then faster. Your heels dig in, your ass comes off the mattress, chasing your hand. The walls are thin, so you bite your lip hard to keep quiet. You come with your thighs clamped on your wrist, legs shaking, fingers still pressed to your clit.")
SHOWER = ("You lock the door and step naked under the hot water. Footsteps cross the hall outside and keep going. The water runs down your tits and drips off your nipples. You soap them slowly, thumbs circling until they stand hard and ache. Your hand slides down your belly and between your legs. You are slick there, and not from the shower. Two fingers find your clit and press. The water drums on your back and your ass. You lean one hand on the tile and rub faster. Your hips jerk against your fingers. The orgasm hits hard, and you bite down on the moan. Your knees go weak, and you hold the tile while your clit throbs under your hand.")
TOILET = ("You lock the stall and lean back against the cold wall. Your hand slides inside, and you are already wet. Two fingers find your clit and press. Your other hand clamps over your mouth. A faucet runs three feet away. A girl laughs at the mirror. You rock your hips against your fingers, slow, so the latch doesn't rattle. Your nipples go hard and tight. The door bangs, and you freeze with your fingers on your clit. Nobody knocks. So you keep going, faster, while the hand dryer roars. The moan stays trapped under your palm. The orgasm hits without a sound, and your thighs clamp shut on your hand.")
# "Footsteps cross the hall" (touch_shower.md): only at hours somebody is up in the house, by their rows
# (who_is_where: weeknights and Sunday 18-24, Mark up to 02:00, Mark in the garage Saturday 09-17,
# Laura up on Saturday 22-24). Iteration 002, part 8 (reader).
TOUCH_SHOWER_HOURS = [{"weekdays": [0, 1, 2, 3, 4, 6], "start_time": "18:00", "end_time": "00:00"},
                      {"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "00:00", "end_time": "02:00"},
                      {"weekdays": [5], "start_time": "09:00", "end_time": "17:00"},
                      {"weekdays": [5], "start_time": "22:00", "end_time": "00:00"}]
# truth pass (2026-11-03): "someone's TV mutters downstairs" only while someone is in the living room (the any-NPC
# presence item, v2.py:5244-5256); with nobody down there the sentence keeps its first clause. touch_bed has no hours.
BED_TV = "Your door is shut, but someone's TV mutters down the hall."
assert BED.startswith(BED_TV + " ")
BED_OPEN = [GC(cond({"type": "npc_at_location", "location_id": "home_living_room", "operator": "is_present"}), P(BED_TV)),
            GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), P("Your door is shut.")),
            P(BED[len(BED_TV) + 1:])]
for cid, loc, name, text, back, extra in [
        ("touch_bed", "home_ella_room", "Touch yourself", BED, "Lie still.", []),
        ("touch_shower", "home_bathroom", "Touch yourself in the shower", SHOWER, "Done.", [{"type": "npc_at_location", "location_id": "home_bathroom", "npc_id": R, "operator": "is_absent"}]),   # hours when someone is up in the house: TOUCH_SHOWER_HOURS
        ("touch_toilet", "college_womens_toilet", "Touch yourself in a stall", TOILET, "Done.", [])]:
    out.append({
        "id": cid, "name": name,
        "description": f"Touching herself ({loc}): from Curious, once a day; Corruption +1 until past Curious.",
        "trigger": {"location": loc, "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1,
                    "conditions": cond(CURIOUS, *extra), **({"schedules": TOUCH_SHOWER_HOURS} if cid == "touch_shower" else {})},
        "nodes": [node("touch", name, [*(BED_OPEN if cid == "touch_bed" else [P(text)]),
            VID(f"a girl touching herself alone ({loc.replace('_', ' ')})", "girl masturbating alone", f"solo girl {loc.split('_')[-1]} orgasm", pool_dir=f"sex/{cid}_t5")],
            [go(back, loc=loc, mins=20, eff=[capped("corruption", 1, CAP_CUR)])])]})

# ═════════════ THE STAIRS (wardrobe event): a short skirt or no panties, someone below ═════════════
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NO_PANTIES = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}
MARK_BELOW = {"type": "npc_at_location", "location_id": "home_living_room", "npc_id": M, "operator": "is_present"}
MARK_NOT_BELOW = {"type": "npc_at_location", "location_id": "home_living_room", "npc_id": M, "operator": "is_absent"}
out.append({
    "id": "wardrobe_event_stairs", "name": "Bend for your bag in the hall",
    "description": "The hall event (wardrobe pool; was the stairs, Q7 one hall, LO 2026-11-04): a short skirt or no panties, and someone behind her. Exhibitionism +1, once a day.",
    "trigger": {"location": "home_hall", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1,
                # (DECISIONS 124) only with Mark below to see it (reader: an empty house paid her for nobody);
                # the evaluator takes flat lists, so one watcher is the trigger and the others are extra lines
                "conditions": cond(SKIRT, trait("exhibitionism", "gte", 20), MARK_BELOW)},
    "nodes": [node("stairs", "The hall", [
        P("Your bag strap slips off your shoulder in the hall, and you bend to catch it, slowly."),
        G(cond({"type": "npc_at_location", "location_id": "home_living_room", "npc_id": M, "operator": "is_present"}),
          # copy fixes A16 + C34 merged (DECISIONS 125): mid-bend, so both exits below ("Hold your skirt down." /
          # "Take your time getting up.") still answer him
          P("Mark comes out of the living room into the hall behind you while you're bent over. He stops. He looks straight up your skirt to your ass, and he doesn't look away. His hand has gone white on the door frame."),
          D(M, "That skirt doesn't bend over in my house, @player."),
          P("He stays in the living-room doorway and waits to see what you do.")),
        G(cond({"type": "npc_at_location", "location_id": "home_ryan_room", "npc_id": R, "operator": "is_present"}),
          P("Ryan comes out of his room while you're still bent over. He has to flatten himself to the wall to pass you in the narrow hall, and his eyes go down your legs on the way past.")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": L, "operator": "is_present"}),
          D(L, "Who are you dressed up for?")),
        G(cond(SKIRT, NO_PANTIES), P("There's nothing under the skirt. Anyone behind you in this hall gets your bare ass and your pussy."),
          # heat proposal A12 (DECISIONS 147): a _t4 pool on the no-panties screen (media only)
          VID("a girl in a short skirt and no panties bending over in a hallway, a man behind her looking straight up it",
              "upskirt bending over no panties hallway", "girl bends over short skirt man behind looks", pool_dir="sex/stairs_skirt_t4")),
    ], [  # DECISIONS 124 (H5): a way out that pays her nothing; the watcher's look moves his meter; only her going slower pays her
        go("Hold your skirt down.", node="down", mins=2),   # C1 (LO 2026-11-03): her no never raises his Want; reader batch 4 (pass 3): he answers it
        # pass 3 D44 (the-surfaces.md R9): going slower for him lands on his look, not a toast (Mark is below: the trigger)
        # reader batch 4 (pass 3): her chosen tease for Mark follows his accident, as his towel acts do (H2, DECISIONS 124)
        go("Take your time getting up.", node="slower", mins=3, cond_=cond({"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}, flag("mark_saw_her")),
           eff=[capped("exhibitionism", 1, CAP_CUR)]),
        go("Take your time getting up.", node="slower", mins=3, cond_=cond(NO_PANTIES, trait("exhibitionism", "gte", 40), flag("mark_saw_her")),
           eff=[capped("exhibitionism", 1, CAP_BOLD)]),
    ]),
        node("slower", "Slower", [
            G(cond(MARK_BELOW, {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}),
              P("You take your time with the strap, hips swaying, the skirt riding up as you reach for it. In the doorway Mark doesn't move. He watches your ass and your panties the whole time.")),
            G(cond(MARK_BELOW, NO_PANTIES),
              P("You don't straighten up. You stay bent forward, legs straight, for one long breath. From the doorway Mark gets your bare ass and your pussy, and his breath goes out of him loud enough to hear.")),
            G(cond(MARK_BELOW), D(M, "Christ, @player.")),
            G(cond(MARK_NOT_BELOW), P("You straighten up slow anyway. When you look round the hall is empty, and your face is hot.")),
            P("Mark's in that living room most nights. This hall will still be here."),   # reader batch 4 (pass 3): the hook
        ], [go("Go on.", loc="home_hall")]),
        # reader batch 4 (pass 3): the written no, his answer on the screen it lands on (Mark is below: the trigger)
        node("down", "Skirt down", [
            P("You clamp your skirt to the backs of your thighs with one hand, straighten up and get down the hall fast."),
            G(cond(MARK_BELOW), D(M, "Better."),
              P("He's still in the doorway when you reach the far end of the hall, still looking at your legs.")),   # pass 4 reader: "Go on." lands in the hall, not her room
            P("Mark's in that living room most nights. This hall will still be here."),
        ], [go("Go on.", loc="home_hall")])]})

# Iteration 002, part 3: leaving this outing after 22:00 sets late_party and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
for _c in out:
    if _c["id"] in ['party_arrive', 'party_chat', 'party_dare', 'party_drink_offer', 'party_hookup']:
        mark_late(_c, 'late_party', split=True)

# heat proposal B13 (Zoe in the park), DECISIONS 147 chunk 3
import walkins_out
_done = walkins_out.attach(out)
assert _done == {"park_run", "park_rest"}, _done

text = "# ── the pool and system scenes: parties, the park, touching herself, the stairs ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("pools:", len(out), "canvases")
