"""The café job — the shift (sheets/systems/job.md). Tom's steps, the Friday repeat and Gary's
ten minutes are in tom.py."""
from canv import *
from tomlw import tod, wd

TM = "npc_tom"
out = []
# Clocking out: the uniform off, her own top and jeans back on (iteration 002: sweep A5-02).
CLOCK_OUT = [{"action": "unequip", "item_id": "cafe_uniform_normal"}, {"action": "unequip", "item_id": "cafe_uniform_sexy"}, {"action": "unequip", "item_id": "cafe_uniform_short"}, {"action": "unequip", "item_id": "cafe_uniform_lowcut"}, {"action": "equip", "item_id": "tshirt"}, {"action": "equip", "item_id": "jeans"}]
# (release 1 fix) "equip" also ADDS the item (v2.py:17371, setup.addToWardrobe + equipItem), so equipping both uniforms
# gave her the tight one on her first shift and put it on every time. Clock-in puts on the normal uniform, unless she
# has changed into the tight one herself (her choice, job.md).
CLOCK_IN = [{"action": "equip", "item_id": "cafe_uniform_normal"}]
SEXY_ON = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}
SEXY_OFF = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "unequipped"}
# DECISIONS 206 (LO, 2026-11-08: "She will buy. Completely her decision"): two more uniforms she buys from Tom, the
# short dress (Exhibitionism 40) and the low-cut dress (60). Clock-in keeps whichever uniform she has on.
SHORT_ON = {"type": "clothing_item", "item_id": "cafe_uniform_short", "operator": "equipped"}
SHORT_OFF = {"type": "clothing_item", "item_id": "cafe_uniform_short", "operator": "unequipped"}
LOW_ON = {"type": "clothing_item", "item_id": "cafe_uniform_lowcut", "operator": "equipped"}
LOW_OFF = {"type": "clothing_item", "item_id": "cafe_uniform_lowcut", "operator": "unequipped"}
SHOWY_OFF = [SEXY_OFF, SHORT_OFF, LOW_OFF]   # the normal uniform, or her own clothes before clock-in
NORMAL_ON = {"type": "clothing_item", "item_id": "cafe_uniform_normal", "operator": "equipped"}
IN_UNIFORM = {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}
NOT_IN_UNIFORM = {"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
PANTIES_OFF = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}
NO_CURFEW = cond(NO_CURFEW_ITEM)
FRI = [wd(4), tod("18:00", "19:00")]   # the Friday evening shift, as it starts (iteration 002: A5-04)


# ── the three levels (cafe_shift_scene.md, signed 2026-11-01, DECISIONS 121; job.md) ──
GY = "npc_gary"
GARY_IN = {"type": "npc_at_location", "location_id": "cafe", "npc_id": GY, "operator": "is_present"}
GARY_OUT = {"type": "npc_at_location", "location_id": "cafe", "npc_id": GY, "operator": "is_absent"}
# The evaluator takes flat lists only (v2.py triggerConditionsSatisfied: a nested group has no `type`
# and fails), so the three levels are five flat, mutually exclusive cases:
E_LO, E_HI = trait("exhibitionism", "lt", 20), trait("exhibitionism", "gte", 20)
C_LO, C_HI = trait("corruption", "lt", 20), trait("corruption", "gte", 20)
PARTS = {"L1": [[E_LO, *SHOWY_OFF]],
         "L2": [[E_LO, SEXY_ON], [E_LO, SHORT_ON], [E_LO, LOW_ON], [E_HI, C_LO], [E_HI, C_HI, trait("cafe_l2_shifts", "lt", 3)]],
         "L3": [[E_HI, C_HI, trait("cafe_l2_shifts", "gte", 3)]]}

def at_level(lv, *blocks, extra=()):
    """The blocks, once per flat case of the level (only one case is ever true)."""
    return [G(cond(*items, *extra), *blocks) for items in PARTS[lv]]

def go_level(lv, text, node_, extra=()):
    return [go(text, node=node_, mins=0, cond_=cond(*items, *extra)) for items in PARTS[lv]]

# reader 2026-11-05: "Nobody" is that table only, because Tom and Gary can already have touched her; each moment reads
# a different part of her, so the screen doesn't say "watch your ass" three times; the second now has a price.
L1_LINES = ["You lean across to clear a table and the conversation at the next one stops: every man at it is looking at your tits. When you straighten up it starts again, lower. Nobody at that table touches you. Not yet.",
            "Two men at the counter watch your legs all the way to the kitchen and back. One of them says something. The other one laughs and pushes a dollar under his saucer for you.",
            "A man in a suit doesn't look at his menu once. He looks at your tits the whole time you take his order, and over-tips."]
# pass 3 B4: what the room says beside each look (a stranger, speaker "unknown")
L1_SAID = ["Don't mind us, sweetheart. Carry on.", "Nice legs on you. Turn around, baby, let's see the rest.",
           "Whatever you're having. Surprise me. I'll be back, same table."]
# One setup for both yeses, so the line before each beat is true whichever she picks (a build note to LO:
# the sheet's pool of three setups would let a setup and the other yes's beat disagree).
L2_SETUP = ("In the back booth, one of three guys asks, \"Are you on the menu?\" and the table laughs. "
            "All three of them are looking at your tits. "
            "At the counter, a guy on his own asks what time you get off, and his eyes drop to your ass when you turn.")
L3_SETUP = ("Sooner or later, somebody always tries it. All shift, men's eyes have been on your ass "
            "every time you bend to a table. Today one of them does more than look.")
L2_PLAY = "You don't tell them off. You smile and bring the check over slow. You lean across their table, much lower than you need to. They can see right down the front of your uniform. Your tits hang there for them, and your nipples are hard against the cloth. It scares you, and you like it more than it scares you. \"Ten,\" the one by the wall says, loud enough for the counter to hear. Tom watches from behind it and says nothing. You take your time with the cups, one at a time. Your ass is pushed out at the next booth the whole while. The bills on the check come to more than the meal. You stay bent over their table, your tits close enough for them to touch."
L2_FLIRT = "You lean on the counter across from him, close. \"I get off when you stop staring at my tits.\" Your voice shakes on the last word, but you say it. He doesn't stop. His eyes stay right there, and your nipples go hard under your uniform. You walk two fingers up his arm, slow, from his wrist to his elbow. He swallows. You scoop whipped cream off a mug with your thumb and lick it clean, slowly. He watches your mouth the whole time. \"I'll think about it,\" you tell him. His face goes red and he shifts on his stool. At the coffee machine, Tom watches and says nothing. You turn away, and the guy's eyes drop to your ass. He tips double, eyes on your tits, while your nipples press hard against your apron."
L3_A = "His hand lands on your ass as you lean in with the plate. You don't move. He squeezes, slow, a full handful through your uniform. You set the knife down. Then the fork, slower. His friend across the booth stops chewing and watches. The hand slides lower, onto the back of your bare thigh. His palm is warm and in no hurry. Your tits feel heavy, your nipples hard under your uniform, and his friend can see them. You're wet. You can't believe it. You still don't move. At the counter Tom has stopped wiping. His eyes follow the hand up your thigh. He says nothing. The man tucks a folded ten into your apron. Then his fingers go back to your thigh and squeeze, high, right under your ass."
L3_B = "Gary holds out his cup without looking up from his paper. You lean in to pour. His free hand slides up the back of your thigh, under the hem of your uniform, and onto your ass. It stays there, warm and heavy. \"Doll,\" he says. He turns a page with his other hand. You keep pouring, very slowly. His thumb strokes the curve of your ass, back and forth. Your nipples go tight against your uniform. You're wet, and your thighs press together. At the counter Tom sees it, but he doesn't stop it. Gary spreads his fingers and squeezes. The coffee climbs toward the rim. His palm stays on your ass until the cup is full."
L3_C = "You let it. You drop onto his knee and the back table roars. His arm locks round your waist and pulls you tight against his chest. His big hand settles on your thigh and squeezes. Under your ass, through his trousers, his cock goes hard and thick. You feel it press up into you as he shifts. His other hand slides up your side and brushes the curve of your tit. Your nipples tighten under your uniform. You count to ten, slowly, and you do not move. Then you stand and smooth your apron flat. Tom watches from the counter and says nothing. The men slap bills onto the table, each tip bigger than the last. The one whose knee you sat on stays seated, his cock still tenting his trousers, his eyes on your ass."
L2_NO = "You smile and keep walking. \"Not today, hon.\" The table groans. The tip is small."
L3_PULL = "You step out from under his hand and put the plate down. \"Your food's here, sir.\" He laughs like it was a joke between you."
L3_SLAP = "You slap his hand off you, loud. The café goes quiet. He throws his napkin on the table and leaves without paying the tip."
GARY_L1 = "In booth four an older man with a folded newspaper lowers it when you pass. His eyes follow your hips all the way down the aisle, and the paper goes back up the second you look round. Gary, the regular."
GARY_L2 = "You've got a lovely way of pouring, doll."
GARY_AFTER = "Same booth, doll. Same time."

# the pay: $8 a shift plus the tip; the sexy uniform and the Friday evening close each double it (as built:
# 12 / 16 / 24, cafe.py before 2026-11-01; LO kept the Friday close, DECISIONS 121)
# DECISIONS 206: tips step with the uniform she has on: normal x1, tight x2, short x3, low-cut x4 (CoT's skimpier
# uniforms draw more custom, guide_course-of-temptation_userjs.js:813-890). The normal rows carry SHOWY_OFF.
TIP_TIERS = [(SHOWY_OFF, 1), ([SEXY_ON], 2), ([SHORT_ON], 3), ([LOW_ON], 4)]
PAY_WHEN = [row for on, m in TIP_TIERS for row in (
    (cond(*on, {"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), m),
    (cond(*on, wd(4), tod("08:00", "18:00")), m),
    (cond(*on, *FRI), 2 * m))]
WORKED = add("cafe_shifts_worked", 1, clamp=False)   # pass 4 J4: a count is never clamped (the-meters.md)
# three hours on her feet lower her hygiene (board.needs: hygiene "falls faster after work"; pass 3 E95)
SHIFT_SWEAT = {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}

def pay(lo, hi, m):
    return {"targetType": "player", "trait": "money", "op": "add", "clamp": False,
            "value": 8 + lo * m if lo == hi else {"type": "random", "min": 8 + lo * m, "max": 8 + hi * m}}

def capped_e(k, n, cap):
    return {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": cap}

def _and(c1, c2):
    return cond(*c1["items"], *c2["items"])

def outcome_exits(tag, lo, hi, eff=(), flags=(), gary_flag=False):
    out_ = []
    for when, m in PAY_WHEN:
        e = [pay(lo, hi, m), WORKED, SHIFT_SWEAT, *eff]
        if gary_flag:
            out_.append(go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=_and(when, cond(GARY_IN)),
                           eff=e + [{"targetType": "player", "trait": "money", "op": "add", "value": 4 * m, "clamp": False}],
                           flags=list(flags) + [fset("gary_met"), fset("gary_let_it")]))
            out_.append(go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=_and(when, cond(GARY_OUT)),
                           eff=e, flags=list(flags)))
        else:
            out_.append(go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=when, eff=e, flags=list(flags) or None))
    return out_

def level1_exits(extra_eff=()):
    """Level 1, no choice: the room looks. $2-4 tips; meeting Gary sets gary_met (npc_gary.md)."""
    out_ = []
    # (bug fix 2026-11-03) level 1 is the normal uniform only (PARTS["L1"]); the tight-uniform rows of PAY_WHEN
    # here could never show (both equipped and unequipped). The tight one at E_LO pays on level 2's exits.
    for when, m in [(w, m) for w, m in PAY_WHEN if SHORT_OFF in w["items"]]:   # the normal-uniform rows
        for gary in (True, False):
            out_.append(go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT,
                           cond_=cond(*when["items"], *PARTS["L1"][0], GARY_IN if gary else GARY_OUT),
                           eff=[pay(2, 4, m), WORKED, SHIFT_SWEAT, *extra_eff], flags=[fset("gary_met")] if gary else None))
    return out_

def money(n):
    return {"targetType": "player", "trait": "money", "op": "add", "value": n, "clamp": False}

def shift_choice(label, k, extra=(), dressed=False):
    """dressed: she has one of her four uniforms on already and keeps it; otherwise clock-in puts the normal one on."""
    prev = [flag(f"cafe_shift_{i}_today") for i in range(1, k)]
    return go(label, node="shift", mins=0, costs=[{"trait": "energy", "value": 20}],
              cond_=cond(*prev, flag(f"cafe_shift_{k}_today", False), *extra, IN_UNIFORM if dressed else NOT_IN_UNIFORM),
              flags=[fset(f"cafe_shift_{k}_today")], wardrobe=None if dressed else CLOCK_IN)

# the evening shift is shut under the curfew (job sheet: "the evening shift says why")
DAY = tod("08:00", "18:00")
EVE = tod("18:00", "19:00")   # an evening shift starts by 19:00 and is done by 22:00, an hour before the 23:00 close (A5-04)
# Tom's text (phone.py tom_shift, DECISIONS 87): "on my way after" books the day's first shift, which pays
# $4 more and clears it (else his no-show text arrives).
BOOKED_PAY = [{"targetType": "player", "trait": "money", "op": "add", "value": 4, "clamp": False}]
choices = []
for k in (1, 2, 3):
    for extra in ([DAY], [EVE, NO_CURFEW_ITEM]):
        for dressed in (False, True):
            c = shift_choice("Work a shift (3 hours, 20 energy).", k, extra, dressed)
            choices += booked_split(c, "tom_shift_booked", eff=BOOKED_PAY) if k == 1 else [c]

out.append({
    "id": "cafe_shift", "name": "Work a shift",
    "description": "The café shift: 3 hours, 20 energy, $8 plus tips ($4 in the normal uniform, x2 in the tight one, x3 in the short dress, x4 in the low-cut dress; Friday's close doubles tips). Up to three a day, Monday to Saturday; the evening shift is shut under the curfew.",
    "trigger": {"location": "cafe", "is_repeatable": True, "priority": 4, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "08:00", "end_time": "19:00"}],
                "conditions": cond(flag("cafe_job"), flag("cafe_shift_3_today", False)),
                # Q2 (LO, 2026-11-04): the café's one-time scenes open from the shift, not on entry, so the
                # wardrobe link always shows; each target keeps its own window and gates (canv.on_activity)
                "substitutions": [on_activity("tom_01_the_apron", flag("cafe_job")),
                                  on_activity("tom_03_the_tip_jar", flag("cafe_job")),
                                  on_activity("cafe_gary_meet", flag("cafe_job"))],
                "show_when_blocked": True, "cooldown_message": "Mon-Sat, 8 AM-7 PM, three shifts a day"},   # pass 3 H31: the hours, a bare phrase (the-clock.md C5)
    "nodes": [
        node("counter", "The counter", [
            # reader 2026-11-05: his order shows only where a shift can start (the hours, no curfew, the energy), and
            # "Uniform's in the back" only while she isn't already wearing one
            *[G(cond(*when, trait("energy", "gte", 20), NOT_IN_UNIFORM),
                D(TM, "Uniform's in the back, @player. Three hours. Smile.")) for when in ([DAY], [EVE, NO_CURFEW_ITEM])],
            *[G(cond(*when, trait("energy", "gte", 20), {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}),
                D(TM, "You're dressed, @player. Three hours. Smile.")) for when in ([DAY], [EVE, NO_CURFEW_ITEM])],
            # scene reader 2026-11-04: as BOOKED_PAY, the day's first shift only, and only where its button is open: 20 energy, not the curfew evening
            G(cond(flag("tom_shift_booked"), flag("cafe_shift_1_today", False), trait("energy", "gte", 20), DAY), D(TM, "Said you'd be here, and you are. Good. Four extra for showing up.")),
            G(cond(flag("tom_shift_booked"), flag("cafe_shift_1_today", False), trait("energy", "gte", 20), EVE, NO_CURFEW_ITEM), D(TM, "Said you'd be here, and you are. Good. Four extra for showing up.")),
            G(cond(trait("energy", "lt", 20)), T("You'd drop a tray. Not today.")),
            G(CURFEW_ON, G(cond(EVE), P("Mom's curfew. No evening shifts this week. Tom shrugs like it's your problem, because it is."))),
        ], choices + [go("Not today.", node="not_today")]),
        # the written no: his "Three hours. Smile." gets an answer; it costs nothing and moves nothing
        # reader 2026-11-05: "Your call." only when a shift button is there; under the curfew or too tired it isn't her call
        node("not_today", "Not today", [
            G(cond(trait("energy", "gte", 20), DAY), D(TM, "Your call. Sit where I can see you or clear the floor. I've got tables.")),
            G(cond(trait("energy", "gte", 20), EVE, NO_CURFEW_ITEM), D(TM, "Your call. Sit where I can see you or clear the floor. I've got tables.")),
            G(cond(trait("energy", "lt", 20), DAY), D(TM, "You're no use to me like that. Sit where I can see you or clear the floor. I've got tables.")),
            G(cond(trait("energy", "lt", 20), EVE, NO_CURFEW_ITEM), D(TM, "You're no use to me like that. Sit where I can see you or clear the floor. I've got tables.")),
            G(CURFEW_ON, G(cond(EVE), D(TM, "Your mother's curfew, not mine. Sit where I can see you or clear the floor. I've got tables."))),
            P("He flicks the cloth over his shoulder and goes back to the till. His eyes go to your ass as you walk away from the counter, but he doesn't call you back."),
        ], [go("Leave him to the till.", loc="cafe", mins=1)]),
        node("shift", "Three hours", [
            G(cond(tod("11:00", "14:00")), P("The lunch rush hits all at once: twelve coffees, a birthday, a baby that screams through all of it. You carry plates until your arms burn. A man at table two watches you bend over to set his plate down, and stops, eyes on your ass."),
              WHO("You've got a pretty smile, honey. That's my number on the napkin, under the tip. Use it.")),   # reader a3 #57 (DECISIONS 131)
            G(cond(tod("14:00", "18:00")), P("Slow afternoon. You wipe tables that are clean and refill sugar that's full, and the regulars at the counter watch your ass every time you bend over to do it. One of them pretends to read his phone the whole time, upside down."), WHO("Another coffee when you get a minute, love. No rush. Take your time bending.")),
            POOL(
                # pass 3 B4: somebody in the room talks (a stranger with no NPC: WHO, speaker "unknown")
                GC({"version": "1.0", "logic": "AND", "items": []}, P("A table of guys from the team come in and order nothing but coffee for an hour so they can watch you walk back and forth. Tom lets them. They tip like they're trying to impress each other."),
                   WHO("Same again, darling. And walk slower this time, we're paying for the view.")),
                GC({"version": "1.0", "logic": "AND", "items": []}, P("Two women in gym clothes, a businessman on a call, a pensioner who wants the crusts cut off his toast. Your feet hurt, but you're good at this. You can feel it in the tips."),
                   WHO("Crusts off, I said. Thank you, dear. You're the only one here who listens.")),
                pid="cafe_shift_lines"),
            G(cond(SEXY_ON), P("In the tight uniform with the top button open, every man who orders leans a little further over the counter. Every one of them tips more."),
              WHO("Whatever you recommend. Keep the change, sugar. Buy yourself a smaller shirt.")),
            # DECISIONS 206: the two dresses she bought, each read on the shift
            G(cond(SHORT_ON, PANTIES_ON), P("In the short dress you can't bend for anything. Every time you set a plate down, the hem rides up the backs of your thighs, and the booth behind you gets your panties. You could bend from the knees. You don't, and the tips come folded bigger."),
              WHO("Drop something, love. Go on. We'll wait.")),
            G(cond(SHORT_ON, PANTIES_OFF), P("Nothing under the short dress. Every time you bend over a table you keep one hand flat on the hem behind you, and the men at the counter watch that hand all shift, waiting for it to slip. It never does."),
              T("One slip and the whole booth sees everything.")),
            G(cond(LOW_ON, BRA_OFF), P("The low-cut dress is cut in a V most of the way to your belt, and with no bra under it your tits move in it every step. Pour a coffee and the counter sees nearly all of them. A nipple edges over the cut once, but you tuck it back before table three can say a word. Table three saw anyway."),
              WHO("Same again, sweetheart. Pour it slow.")),
            G(cond(LOW_ON, BRA_ON), P("The low-cut dress wasn't cut for a bra. Its cups show in the V every time you lean, but the men at the counter look at them like you meant it."),
              WHO("Lose the bra, love. It's spoiling the dress.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, LOW_OFF),
              P("No bra under the uniform, and your nipples show through it. Every time you lean to pour, a man's eyes drop to your tits."),
              WHO("Cold in here today, is it?")),
            # (cut 2026-11-01: Tom's "Booth four's going to tip big today." Tom is strict, DECISIONS 117)
            G(cond(trait("tom_step", "gte", 1), ntrait(TM, "want", "gte", 15)), P("Tom reties your apron on his way past, both times you go by."), D(TM, "Hold still. It's slipping again. Can't have you coming apart in front of the customers.")),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)), P("A woman at table three wrinkles her nose when you lean in. Her tip is coins."), WHO("Busy day, was it, dear? You might want a shower before the next one.")),
            # ── the drawn customer scene, one a shift (cafe_shift_scene.md, signed 2026-11-01, DECISIONS 121) ──
            *at_level("L1", POOL(*[GC({"version": "1.0", "logic": "AND", "items": []}, P(t), WHO(w)) for t, w in zip(L1_LINES, L1_SAID)], pid="cafe_l1_lines")),
            *at_level("L1", P(GARY_L1), extra=[GARY_IN]),
            *at_level("L2", P(L2_SETUP)),
            *at_level("L2", D(GY, GARY_L2), extra=[GARY_IN]),
            *at_level("L3", P(L3_SETUP)),
            # Tom's step 3 converts into the shift (the-arc.md A1; cafe_shift_scene.md "the window rule"): the
            # level-3 touch now reads tom_window_rule, so the top step changes the repeatable it sits on.
            *at_level("L3", P("Tom's rule since the back room: nothing by the window. Whatever happens now happens where the street can't see it."),
                      extra=[flag("tom_window_rule")]),
            *at_level("L3", D(GY, GARY_AFTER), extra=[GARY_IN, flag("gary_let_it")]),
        ], level1_exits()
           # exhibition phase 1 (LO, 2026-11-08): at level 1 a customer's look happens to her; her choice is to let it go on
           + [go("Take your time with the table.", node="l1_table", mins=0, cond_=cond(*PARTS["L1"][0]))]
           + go_level("L2", "Play along.", "l2_play", extra=[trait("exhibitionism", "gte", 60)])   # a table and the counter watch: Watched (DECISIONS 124)
           + go_level("L2", "Flirt back.", "l2_flirt", extra=[C_HI])
           + go_level("L2", "\"Not today, hon.\"", "l2_no")
           + go_level("L3", "Let it.", "l3_let", extra=[trait("corruption", "gte", 40)])   # his hand on her, let: Bold; below it the grope still happens, and she refuses (DECISIONS 124)
           + go_level("L3", "\"Your food's here, sir.\"", "l3_pull")
           + go_level("L3", "Slap it away.", "l3_slap")),
        node("l1_table", "Table six", [
            P("You bend low over table six to wipe it, and the man there stops talking halfway through a sentence. His eyes are down the front of your uniform."),
            P("You take your time. You wipe it twice, slow, and you don't straighten up until you're done."),
            P("He leaves an extra dollar tucked under his plate and won't look you in the face on his way out."),
            GC(cond(trait("exhibitionism", "lt", 5)), T("He was looking anyway. You just didn't stop him.")),
            GC(cond(trait("exhibitionism", "lt", 10)), T("A dollar for a look. You let him have it.")),
            GC(cond(trait("exhibitionism", "lt", 15)), T("He looked the whole time, and you let him.")),
            GC(cond(trait("exhibitionism", "lt", 20)), T("You'd do table six like that every shift.")),
        ], level1_exits(extra_eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}, {"targetType": "player", "trait": "money", "op": "add", "value": 1, "clamp": False}])),
        node("l2_play", "Play along", [P(L2_PLAY),
            VID("a waitress leaning low over a booth table, men looking down her uniform", "waitress leaning over table men staring cleavage", "waitress bends over booth customers look", pool_dir="sex/cafe_l2_play_t3")],
             outcome_exits("l2_play", 6, 10, eff=[capped_e("exhibitionism", 1, 79), add("cafe_footfall", 1, clamp=False), add("cafe_l2_shifts", 1, clamp=False)])),
        node("l2_flirt", "Flirt back", [P(L2_FLIRT),
            VID("a waitress flirting across a cafe counter with a customer, licking cream off her thumb", "waitress flirting counter customer", "flirty waitress licks cream finger customer stares", pool_dir="sex/cafe_l2_flirt_t3")],
             outcome_exits("l2_flirt", 6, 10, eff=[capped_e("corruption", 1, 39), add("cafe_footfall", 1, clamp=False), add("cafe_l2_shifts", 1, clamp=False)])),
        node("l2_no", "Not today", [P(L2_NO), WHO("Worth a try. Bring us the check, then, killjoy.")], outcome_exits("l2_no", 2, 4)),   # her no never opens "Let it." (H5, DECISIONS 124)
        node("l3_let", "Let it", [
            G(cond(GARY_IN), P(L3_B)),   # false lines a3 #10 (DECISIONS 129): gary_let_it is set on his clock-out, so his shift shows his touch
            # reader a3 older (heat ladder: a room watching is Watched, E60): the back table's lap only at Exhibitionism 60
            G(cond(GARY_OUT, trait("exhibitionism", "lt", 60)), P(L3_A)),
            G(cond(GARY_OUT, trait("exhibitionism", "gte", 60)), POOL(P(L3_A), P(L3_C), pid="cafe_l3_strangers", bag=True)),
            VID("a waitress letting a customer's hand stay on her as she serves, the manager watching from the counter", "customer grabs waitress ass she lets him", "waitress groped at table lets it happen", pool_dir="sex/cafe_l3_let_t4")],
             # L3 needs Corruption 40 but only Exhibitionism 20, so each meter stops at its own stage's top (pass 3 G8)
             outcome_exits("l3_let", 10, 16, eff=[capped_e("corruption", 1, 59), capped_e("exhibitionism", 1, 39),
                                                  add("cafe_footfall", 1, clamp=False), add("cafe_name", -1, clamp=False)],   # Tom 3 reads cafe_name lte -5: a clamp would floor it at 0 (pass 4 E96)
                           flags=[fset("cafe_let_it")], gary_flag=True)),
        node("l3_pull", "Your food's here", [P(L3_PULL), WHO("Feisty. I like feisty. Same table next week, love.")], outcome_exits("l3_pull", 4, 8)),
        node("l3_slap", "Slap it away", [P(L3_SLAP), ME("Hands to yourself. Next time I'll call the police."), D(TM, "Back to work, @player. Table six is waiting.")], outcome_exits("l3_slap", 0, 0)),
    ]})

# ── meeting Gary (npc_gary.md, re-signed 2026-11-01): level 1, her first shift he's in. A one-time screen that names
#    him and sets gary_met, so his booth hub opens on a meeting (gates: every hub is met first). ──
out.append({
    "id": "cafe_gary_meet", "name": "Booth four",
    "description": "The first time Gary is in during her job: the regular in booth four lowers his paper. Sets gary_met.",
    "trigger": {"location": "cafe", "npc": GY, "requires_npc": GY, "is_repeatable": False, "priority": 7, "is_active": True,
                "substitution_only": True,   # Q2 (LO, 2026-11-04): opens from "Work a shift" (cafe_shift above)
                "schedules": [{"weekdays": [0, 1, 2, 3, 4], "start_time": "14:30", "end_time": "18:00"},
                              {"weekdays": [4], "start_time": "20:00", "end_time": "22:00"}],   # his rows (npc_gary.md)
                "conditions": cond(flag("cafe_job"), flag("gary_met", False))},
    "nodes": [node("booth", "Booth four", [
        # his meeting has its own words; GARY_L1 stays on the repeat shift (one pool, one place)
        P("An older man in booth four has a folded newspaper and a pot of tea, but he brings the paper down an inch when you go by, and his eyes drop to your ass and follow it to the end of the aisle. The paper's back up before you can catch him. Tom calls him Gary. He's the regular."),
        D(GY, "Top me up when you've got a minute, doll."),
    ], [go("\"Coming.\"", loc="cafe", mins=5, flags=[fset("gary_met")])])]})

# ═════════════ ACCIDENTS ON THE SHIFT (cafe_shift_scene.md "Accidents", DECISIONS 202) ═════════════
# The uniform goes wrong as she comes on shift: a spilt jug soaks it see-through, the tight one's top button pops,
# the normal one's hem rides up (CoT's malfunction marks, A_cot.md:224, and water, :227; Curse of the Abyss's first
# tavern shift is the tap spraying her, C_other_games.md:219). 1 in 4, one a day, daytime only, opened from "Work a
# shift" (cafe_shift's substitutions) where a shift could start. It pays no wage: both answers send her back to the
# counter, in uniform, and the shift itself still pays (the shift stays the café's one way to earn; gate
# `sinks >= sources`). The room seeing it pays the café's footfall +1 (H5: an accident pays whoever saw it);
# letting it be pays her +1 Exhibitionism to the top of the stage it shows, gated there.
CAFE_ACC = "cafe_accident_today"
SEEN = add("cafe_footfall", 1, clamp=False)


def cafe_accident(cid, name, conds, blocks, fix, fix_text, let, let_gate, cap, let_text, hook, dressed=False, table="Table nine's waiting."):
    """dressed: she came in the tight uniform already; otherwise she changes into the normal one first."""
    # plain (not dressed): in her own clothes she changes into the normal uniform; in the normal one she goes straight out
    first = ([go("Get to the tables.", node="event", mins=0)] if dressed
             else [go("Get changed.", node="event", mins=5, wardrobe=CLOCK_IN, cond_=cond(NOT_IN_UNIFORM)),
                   go("Get to the tables.", node="event", mins=0, cond_=cond(NORMAL_ON))])
    done = [go("Back to the counter.", loc="cafe", mins=10)]
    return {"id": cid, "name": name,
            "description": f"Random shift accident (cafe_shift_scene.md, DECISIONS 202): {name}. 1 in 4, one a day, day shifts, as she comes on; no wage (the shift after it pays); footfall +1 on both answers, letting it be +1 Exhibitionism to cap {cap}.",
            "trigger": {"location": "cafe", "is_repeatable": True, "priority": 4, "is_active": True, "substitution_only": True,
                        "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "08:00", "end_time": "18:00"}],
                        "conditions": cond(flag("cafe_job"), flag("cafe_shift_3_today", False), flag(CAFE_ACC, False),
                                           trait("energy", "gte", 20), *conds)},
            "nodes": [
                node("counter", "The counter", [D(TM, "You're on, @player. The counter's yours. Go.")] if dressed
                     else [G(cond(NOT_IN_UNIFORM), D(TM, f"Uniform's in the back, @player. {table} Go.")),
                           G(cond(NORMAL_ON), D(TM, f"You're dressed, @player. {table} Go."))], first),
                node("event", name, blocks, [go(fix, node="fix", mins=0, eff=[SEEN], flags=[fset(CAFE_ACC)]),
                                             go(let, node="let", mins=0, eff=[SEEN, capped_e("exhibitionism", 1, cap)], flags=[fset(CAFE_ACC)],
                                                cond_=cond(*let_gate) if let_gate else None)]),
                node("fix", fix.rstrip("."), [*fix_text, P(hook)], done),
                node("let", let.rstrip("."), [*let_text, P(hook)], done),
            ]}


JUG = "Your first table of the shift, and the man at table nine swings round to wave at somebody and takes the water jug right out of your hand. The whole jug goes down your front."
out.append(cafe_accident("cafe_acc_spill_bra", "The jug goes over", [*SHOWY_OFF, BRA_ON],
    [P(JUG + " The uniform is soaked through in a second and goes see-through. It clings to you. Your bra shows through it, the shape of your tits in it and all."),
     WHO("Oh God, sorry, love. Sorry. Hell of a view, though.")],
    "Run for the back room.",
    [P("You fold your arms over your chest and run for the back room, but the whole café saw. You wring the front out in the sink until it's only damp, then go back out. Tom watches you come out and says nothing."),
     T("Three hours to go, and everyone remembers.")],
    "Finish the table.", [], 19,
    [P("You don't run. You finish the table soaking wet, your bra showing through the uniform, and you go on serving in it till it dries. Every table you go to looks. At the counter Tom watches and says nothing. Table nine says sorry three times and doesn't mean it once."),
     GC(cond(trait("exhibitionism", "lt", 10)), T("It's only water. It'll dry.")),
     GC(cond(trait("exhibitionism", "lt", 20)), T("They looked, and you let them.")),
     GC(cond(trait("exhibitionism", "gte", 20)), T("You could have run. You didn't want to."))],
    "He's a stranger, and he leaves with his eyes still on your chest. Three hours of shift to go, and every table in here saw it."))

out.append(cafe_accident("cafe_acc_spill_bare", "The jug goes over", [*SHOWY_OFF, BRA_OFF],
    [P(JUG + " The uniform is soaked through in a second and goes see-through, and there's no bra under it. It clings to your bare tits. Your nipples are hard from the cold water, dark through the wet cloth, for the whole room."),
     WHO("Jesus. Sorry, love. Sorry. Christ.")],
    "Run for the back room.",
    [P("You cross your arms over your tits and run for the back room with the whole café watching you go. You stand in front of the hand dryer until the front stops showing everything, and you go back out with a tray held against your chest. Tom says nothing."),
     T("No bra. Of course today.")],
    "Finish the table.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You don't run. You finish the table soaking wet, your bare tits and your hard nipples right there through the uniform, and you keep serving in it. Every man in the place orders another coffee. At the counter Tom watches and says nothing."),
     T("Everyone can see them. You don't want it to dry.")],
    "He's a stranger, and he can't look at your face when he pays. The whole shift is still ahead of you, in a uniform that won't dry.", table="Table nine wants water."))

out.append(cafe_accident("cafe_acc_button_bra", "The top button goes", [SEXY_ON, BRA_ON],
    [P("You're leaning over the counter with a man's change when the top button of the tight uniform gives up and pings off the coffee machine. The front falls open to your bra. He gets a long look at your tits pushed up in it."),
     WHO("Well. Thank you, sweetheart.")],
    "Hold it shut.",
    [P("You grab the front together with one hand, but it gapes every time you move, so you hold it like that, fixing it every time you lean. Tom finds a safety pin in the till and hands it over without a word."),
     T("A size smaller wasn't a great idea.")],
    "Leave it open.", [], 19,
    [P("You leave it. You go back to the tables with the uniform open to your bra, and you lean over every one a little further than you need to. Tom watches from the till and says nothing.")],
    "He takes his change without counting it. Three hours to go, and that button isn't coming back.", dressed=True))

out.append(cafe_accident("cafe_acc_button_bare", "The top button goes", [SEXY_ON, BRA_OFF],
    [P("You're leaning over the counter with a man's change when the top button of the tight uniform gives up and pings off the coffee machine. There's no bra under it. The front falls open and your bare tits are right there, a nipple out of the gap, a foot from his face."),
     WHO("Oh. Oh, sweetheart.")],
    "Hold it shut.",
    [P("You clutch the front shut and turn away, face burning, and go back out with one hand at your chest. Tom finds a safety pin in the till and hands it over without a word."),
     T("No bra and a tight uniform. Great plan.")],
    "Leave it open.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You leave it. The uniform hangs open, and every time you lean to pour, your bare tits swing in the gap, nipples and all. Tom watches from the till and says nothing. Men you've never seen before stay for a second coffee.")],
    "He forgets his change on the counter. The men at the window seats saw it all, and they're staying for the rest of your shift.", dressed=True))

out.append(cafe_accident("cafe_acc_hem", "Under the table", [*SHOWY_OFF, PANTIES_ON],
    [P("A man in booth two knocks his fork off the table. You bend all the way over to get it from under the seat, and the uniform's hem rides right up over your ass. The whole booth behind you sees your panties, stretched tight between your legs from behind."),
     WHO("Take your time down there.")],
    "Pull the hem down.",
    [P("You come up with the fork, yank the hem down and walk off quick, face red, but the booth is already laughing. Tom watches from the counter and says nothing."),
     T("Next time he can get his own fork.")],
    "Take your time down there.", [trait("exhibitionism", "gte", 40)], 59,
    [P("You take your time. You stay bent over, feeling under the seat for a fork you already found, your uniform up over your ass and your panties out to the whole booth. Then you stand, smooth it down and hand him a clean one. Tom watches from the counter and says nothing. The booth can't stop grinning at each other.")],
    "The booth comes in on the same day every week. Somebody's going to drop a fork again.", table="Booth two's waiting."))

# DECISIONS 206: the two dresses she bought go wrong too (a moment each; no public topless, DECISIONS 204)
out.append(cafe_accident("cafe_acc_short_shelf", "The top shelf", [SHORT_ON, PANTIES_ON],
    [P("Table nine wants the honey, and the honey lives on the top shelf behind the counter. You go up on your toes for it, and the short dress comes up with you, right off your ass. The two men on the counter stools get your panties at eye level, the whole back of them."),
     WHO("Higher shelf next time, Tom.")],
    "Pull the dress down.",
    [P("You grab the hem and come down off your toes fast, the honey in your other hand and your face hot. The two on the stools suddenly find their coffee very interesting. Tom wipes the same spot on the counter and doesn't look up."),
     T("Thirty dollars for a dress that does that.")],
    "Stay up there.", [trait("exhibitionism", "gte", 40)], 59,
    [P("You stay up on your toes. You take your time choosing between two jars that are both honey, the dress up over your ass and your panties out to the counter, and you only come down once you've picked. Tom has stopped wiping. The two men order another coffee they don't want."),
     GC(cond(trait("exhibitionism", "lt", 50)), T("They saw. You let them.")),
     GC(cond(trait("exhibitionism", "gte", 50)), T("You'd reach for that shelf all day."))],
    "They're on the same stools every week. They'll ask for something off the top shelf again.", dressed=True))

out.append(cafe_accident("cafe_acc_lowcut_slip", "The cut gives", [LOW_ON, BRA_OFF],
    [P("You lean in to pour for a man at the corner table at the back, and the low-cut dress gives up on the left side. Your nipple slides right out over the edge of the cut, bare and hard, a foot from his cup."),
     WHO("Careful, love. You'll spill.")],
    "Tug it back.",
    [P("You set the pot down and tug the dress back over it, fast, with both hands, but he's already seen everything. Your face burns all the way back to the counter, where Tom is very busy with the till."),
     T("No bra fits under it. You knew that when you paid for it.")],
    "Finish pouring.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You don't tug it back. You finish pouring, slow, your nipple out over the cut and tight in the air, and you top up his friend's cup too before you straighten up and tuck it away. The corner table goes silent. Tom stares at the till like it owes him money."),
     T("The whole corner saw it. You liked that they did.")],
    "The corner table stays for the rest of your shift and watches the cut of your dress every time you pour.", dressed=True))

CAFE_ACC_IDS = [c["id"] for c in out if c["id"].startswith("cafe_acc_")]
_shift = next(c for c in out if c["id"] == "cafe_shift")
_shift["trigger"]["substitutions"] += [{"target_canvas_id": a, "chance": 0.25, "conditions": cond(flag(CAFE_ACC, False))}
                                       for a in CAFE_ACC_IDS]

text = "# ── the café shift (sheets/systems/job.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("cafe:", len(out), "canvases")
