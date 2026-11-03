"""The café job — the shift (sheets/systems/job.md). Tom's steps, the Friday repeat and Gary's
ten minutes are in tom.py."""
from canv import *
from tomlw import tod, wd

TM = "npc_tom"
out = []
# Clocking out: the uniform off, her own top and jeans back on (iteration 002: sweep A5-02).
CLOCK_OUT = [{"action": "unequip", "item_id": "cafe_uniform_normal"}, {"action": "unequip", "item_id": "cafe_uniform_sexy"}, {"action": "equip", "item_id": "tshirt"}, {"action": "equip", "item_id": "jeans"}]
# (release 1 fix) "equip" also ADDS the item (v2.py:17371, setup.addToWardrobe + equipItem), so equipping both uniforms
# gave her the tight one on her first shift and put it on every time. Clock-in puts on the normal uniform, unless she
# has changed into the tight one herself (her choice, job.md).
CLOCK_IN = [{"action": "equip", "item_id": "cafe_uniform_normal"}]
SEXY_ON = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}
SEXY_OFF = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "unequipped"}
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
PARTS = {"L1": [[E_LO, SEXY_OFF]],
         "L2": [[E_LO, SEXY_ON], [E_HI, C_LO], [E_HI, C_HI, trait("cafe_l2_shifts", "lt", 3)]],
         "L3": [[E_HI, C_HI, trait("cafe_l2_shifts", "gte", 3)]]}

def at_level(lv, *blocks, extra=()):
    """The blocks, once per flat case of the level (only one case is ever true)."""
    return [G(cond(*items, *extra), *blocks) for items in PARTS[lv]]

def go_level(lv, text, node_, extra=()):
    return [go(text, node=node_, mins=0, cond_=cond(*items, *extra)) for items in PARTS[lv]]

L1_LINES = ["You bend to wipe a table and the conversation at the next one stops. When you straighten up it starts again, lower.",
            "Two men at the counter watch you walk to the kitchen and back. One of them says something. The other one laughs.",
            "A man in a suit doesn't look at his menu once. He looks at you the whole time you take his order, and over-tips."]
# pass 3 B4: what the room says beside each look (a stranger, speaker "unknown")
L1_SAID = ["Don't mind us, honey. Carry on.", "Nice legs on the new girl. Turn around, baby, let's see the rest.",
           "Whatever you're having. Surprise me. I'll be back tomorrow, same table."]
# One setup for both yeses, so the line before each beat is true whichever she picks (a build note to LO:
# the sheet's pool of three setups would let a setup and the other yes's beat disagree).
L2_SETUP = ("In the back booth, one of three guys asks, \"Are you on the menu?\" and the table laughs. "
            "All three of them are looking at your tits. "
            "At the counter, a guy on his own asks what time you get off, and his eyes drop to your ass when you turn.")
L3_SETUP = ("The slow hours are the ones where somebody always tries it. All shift, men's eyes have been on your ass "
            "every time you bend to a table. Today one of them does more than look.")
L2_PLAY = "You don't tell them off. You smile and bring the check over slow. You lean across their table, much lower than you need to. They can see right down the front of your uniform. Your tits hang there for them, and your nipples are hard against the cloth. It scares you, and you like it more than it scares you. \"Ten,\" the one by the wall says, loud enough for the counter to hear. Tom watches from behind it and says nothing. You take your time with the cups, one at a time. Your ass is pushed out at the next booth the whole while. The bills on the check come to more than the meal. You stay bent over their table, your tits close enough for them to touch."
L2_FLIRT = "You lean on the counter across from him, close. \"I get off when you stop staring at my tits.\" Your voice shakes on the last word, but you say it. He doesn't stop. His eyes stay right there, and your nipples go hard under your uniform. You walk two fingers up his arm, slow, from his wrist to his elbow. He swallows. You scoop whipped cream off a mug with your thumb and lick it clean, slowly. He watches your mouth the whole time. \"I'll think about it,\" you tell him. His face goes red and he shifts on his stool. At the coffee machine, Tom watches and says nothing. You turn away, and the guy's eyes drop to your ass. He tips double, eyes on your tits, while your nipples press hard against your apron."
L3_A = "His hand lands on your ass as you lean in with the plate. You don't move. He squeezes, slow, a full handful through your uniform. You set the knife down. Then the fork, slower. His friend across the booth stops chewing and watches. The hand slides lower, onto the back of your bare thigh. His palm is warm and in no hurry. Your tits feel heavy, your nipples hard under your uniform, and his friend can see them. You're wet. You can't believe it. You still don't move. At the counter Tom has stopped wiping. His eyes follow the hand up your thigh. He says nothing. The man tucks a folded ten into your apron. Then his fingers go back to your thigh and squeeze, high, right under your ass."
L3_B = "Gary holds out his cup without looking up from his paper. You lean in to pour. His free hand slides up the back of your thigh, under the hem of your uniform, and onto your ass. It stays there, warm and heavy. \"Doll,\" he says. He turns a page with his other hand. You keep pouring, very slowly. His thumb strokes the curve of your ass, back and forth. Your nipples go tight against your uniform. You're wet, and your thighs press together. At the counter Tom sees it, but he doesn't stop it. Gary spreads his fingers and squeezes. The coffee climbs toward the rim. His palm stays on your ass until the cup is full."
L3_C = "You let it. You drop onto his knee and the back table roars. His arm locks round your waist and pulls you tight against his chest. His big hand settles on your thigh and squeezes. Under your ass, through his trousers, his cock goes hard and thick. You feel it press up into you as he shifts. His other hand slides up your side and brushes the curve of your tit. Your nipples tighten under your uniform. You count to ten, slowly, and you do not move. Then you stand and smooth your apron flat. Tom watches from the counter and says nothing. The men slap bills onto the table, each tip bigger than the last. The one whose knee you sat on stays seated, his cock still tenting his trousers, his eyes on your ass."
L2_NO = "You smile and keep walking. \"Not today, hon.\" The table groans. The tip is small."
L3_PULL = "You step out from under his hand and put the plate down. \"Your food's here, sir.\" He laughs like it was a joke between you."
L3_SLAP = "You slap his hand off you, loud. The café goes quiet. He throws his napkin on the table and leaves without paying the tip."
GARY_L1 = "In booth four an older man with a folded newspaper lowers it when you pass. His eyes stay on your ass all the way down the aisle, and the paper goes back up the second you look round. Gary, the regular."
GARY_L2 = "You've got a lovely way of pouring, doll."
GARY_AFTER = "Same booth, doll. Same time."

# the pay: $8 a shift plus the tip; the sexy uniform and the Friday evening close each double it (as built:
# 12 / 16 / 24, cafe.py before 2026-11-01; LO kept the Friday close, DECISIONS 121)
PAY_WHEN = [(cond(SEXY_OFF, {"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), 1),
            (cond(SEXY_OFF, wd(4), tod("08:00", "18:00")), 1),
            (cond(SEXY_OFF, *FRI), 2),
            (cond(SEXY_ON, {"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), 2),
            (cond(SEXY_ON, wd(4), tod("08:00", "18:00")), 2),
            (cond(SEXY_ON, *FRI), 4)]
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

def level1_exits():
    """Level 1, no choice: the room looks. $2-4 tips; meeting Gary sets gary_met (npc_gary.md)."""
    out_ = []
    # (bug fix 2026-11-03) level 1 is the normal uniform only (PARTS["L1"]); the tight-uniform rows of PAY_WHEN
    # here could never show (both equipped and unequipped). The tight one at E_LO pays on level 2's exits.
    for when, m in [(w, m) for w, m in PAY_WHEN if SEXY_ON not in w["items"]]:
        for gary in (True, False):
            out_.append(go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT,
                           cond_=cond(*when["items"], *PARTS["L1"][0], GARY_IN if gary else GARY_OUT),
                           eff=[pay(2, 4, m), WORKED, SHIFT_SWEAT], flags=[fset("gary_met")] if gary else None))
    return out_

def money(n):
    return {"targetType": "player", "trait": "money", "op": "add", "value": n, "clamp": False}

def shift_choice(label, k, extra=(), sexy=False):
    prev = [flag(f"cafe_shift_{i}_today") for i in range(1, k)]
    return go(label, node="shift", mins=0, costs=[{"trait": "energy", "value": 20}],
              cond_=cond(*prev, flag(f"cafe_shift_{k}_today", False), *extra, SEXY_ON if sexy else SEXY_OFF),
              flags=[fset(f"cafe_shift_{k}_today")], wardrobe=None if sexy else CLOCK_IN)

# the evening shift is shut under the curfew (job sheet: "the evening shift says why")
DAY = tod("08:00", "18:00")
EVE = tod("18:00", "19:00")   # an evening shift starts by 19:00 and is done by 22:00, an hour before the 23:00 close (A5-04)
# Tom's text (phone.py tom_shift, DECISIONS 87): "on my way after" books the day's first shift, which pays
# $4 more and clears it (else his no-show text arrives).
BOOKED_PAY = [{"targetType": "player", "trait": "money", "op": "add", "value": 4, "clamp": False}]
choices = []
for k in (1, 2, 3):
    for extra in ([DAY], [EVE, NO_CURFEW_ITEM]):
        for sexy in (False, True):
            c = shift_choice("Work a shift (3 hours, 20 energy).", k, extra, sexy)
            choices += booked_split(c, "tom_shift_booked", eff=BOOKED_PAY) if k == 1 else [c]

out.append({
    "id": "cafe_shift", "name": "Work a shift",
    "description": "The café shift: 3 hours, 20 energy, $8 plus tips ($4 in the normal uniform, $8 in the tight one at Daring; Friday's close doubles tips). Up to three a day, Monday to Saturday; the evening shift is shut under the curfew.",
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
            D(TM, "Uniform's in the back, @player. Three hours. Smile."),
            G(cond(flag("tom_shift_booked")), D(TM, "You came. Good. Four extra for showing up.")),
            G(cond(trait("energy", "lt", 20)), T("You'd drop a tray. Not today.")),
            G(CURFEW_ON, G(cond(EVE), P("Mom's curfew. No evening shifts this week. Tom shrugs like it's your problem, because it is."))),
        ], choices + [go("Not today.", loc="cafe", mins=1)]),
        node("shift", "Three hours", [
            G(cond(tod("11:00", "14:00")), P("The lunch rush hits all at once: twelve coffees, a birthday, a baby that screams through all of it. You carry plates until your arms burn. A man at table two watches you bend over to set his plate down, and stops, eyes on your ass."),
              WHO("You've got a pretty smile, honey. That's my number on the napkin, under the tip. Use it.")),   # reader a3 #57 (DECISIONS 131)
            G(cond(tod("14:00", "18:00")), P("Slow afternoon. You wipe tables that are clean and refill sugar that's full, and the regulars at the counter watch your ass every time you bend over to do it. One of them pretends to read his phone the whole time, upside down."), WHO("Another coffee when you get a minute, love. No rush. Take your time bending.")),
            POOL(
                # pass 3 B4: somebody in the room talks (a stranger with no NPC: WHO, speaker "unknown")
                GC({"version": "1.0", "logic": "AND", "items": []}, P("A table of guys from the team come in and order nothing but coffee for an hour so they can watch you walk back and forth. Tom lets them. They tip like they're trying to impress each other."),
                   WHO("Same again, honey. And walk slower this time, we're paying for the view.")),
                GC({"version": "1.0", "logic": "AND", "items": []}, P("Two women in gym clothes, a businessman on a call, a pensioner who wants the crusts cut off his toast. Your feet hurt, but you're good at this. You can feel it in the tips."),
                   WHO("Crusts off, I said. Thank you, dear. You're the only one here who listens.")),
                pid="cafe_shift_lines"),
            G(cond(SEXY_ON), P("In the tight uniform with the top button open, every man who orders leans a little further over the counter. Every one of them tips more."),
              WHO("Whatever you recommend. Keep the change, honey. Buy yourself a smaller shirt.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
              P("No bra under the uniform, and your nipples show through it. Every time you lean to pour, somebody stops talking and looks at your tits."),
              WHO("Cold in here today, is it?")),
            # (cut 2026-11-01: Tom's "Booth four's going to tip big today." Tom is strict, DECISIONS 117)
            G(cond(trait("tom_step", "gte", 1), ntrait(TM, "want", "gte", 30)), P("Tom reties your apron on his way past, both times you go by."), D(TM, "Hold still. It's slipping again. Can't have you coming apart in front of the customers.")),
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
           + go_level("L2", "Play along.", "l2_play", extra=[trait("exhibitionism", "gte", 60)])   # a table and the counter watch: Watched (DECISIONS 124)
           + go_level("L2", "Flirt back.", "l2_flirt", extra=[C_HI])
           + go_level("L2", "\"Not today, hon.\"", "l2_no")
           + go_level("L3", "Let it.", "l3_let", extra=[trait("corruption", "gte", 40)])   # his hand on her, let: Bold; below it the grope still happens, and she refuses (DECISIONS 124)
           + go_level("L3", "\"Your food's here, sir.\"", "l3_pull")
           + go_level("L3", "Slap it away.", "l3_slap")),
        node("l2_play", "Play along", [P(L2_PLAY),
            VID("a waitress leaning low over a booth table, men looking down her uniform", "waitress leaning over table men staring cleavage", "waitress bends over booth customers look", pool_dir="sex/cafe_l2_play_t3")],
             outcome_exits("l2_play", 6, 10, eff=[capped_e("exhibitionism", 1, 79), add("cafe_footfall", 1), add("cafe_l2_shifts", 1)])),
        node("l2_flirt", "Flirt back", [P(L2_FLIRT),
            VID("a waitress flirting across a cafe counter with a customer, licking cream off her thumb", "waitress flirting counter customer", "flirty waitress licks cream finger customer stares", pool_dir="sex/cafe_l2_flirt_t3")],
             outcome_exits("l2_flirt", 6, 10, eff=[capped_e("corruption", 1, 39), add("cafe_footfall", 1), add("cafe_l2_shifts", 1)])),
        node("l2_no", "Not today", [P(L2_NO), WHO("Worth a try. Bring us the check, then, killjoy.")], outcome_exits("l2_no", 2, 4)),   # her no never opens "Let it." (H5, DECISIONS 124)
        node("l3_let", "Let it", [
            G(cond(GARY_IN), P(L3_B)),   # false lines a3 #10 (DECISIONS 129): gary_let_it is set on his clock-out, so his shift shows his touch
            # reader a3 older (heat ladder: a room watching is Watched, E60): the back table's lap only at Exhibitionism 60
            G(cond(GARY_OUT, trait("exhibitionism", "lt", 60)), P(L3_A)),
            G(cond(GARY_OUT, trait("exhibitionism", "gte", 60)), POOL(P(L3_A), P(L3_C), pid="cafe_l3_strangers", bag=True)),
            VID("a waitress letting a customer's hand stay on her as she serves, the manager watching from the counter", "customer grabs waitress ass she lets him", "waitress groped at table lets it happen", pool_dir="sex/cafe_l3_let_t4")],
             # L3 needs Corruption 40 but only Exhibitionism 20, so each meter stops at its own stage's top (pass 3 G8)
             outcome_exits("l3_let", 10, 16, eff=[capped_e("corruption", 1, 59), capped_e("exhibitionism", 1, 39),
                                                  add("cafe_footfall", 1), add("cafe_name", -1, clamp=False)],   # Tom 3 reads cafe_name lte -5: a clamp would floor it at 0 (pass 4 E96)
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
        P(GARY_L1),
        D(GY, "Top me up when you've got a minute, doll."),
    ], [go("\"Coming.\"", loc="cafe", mins=5, flags=[fset("gary_met")])])]})

text = "# ── the café shift (sheets/systems/job.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("cafe:", len(out), "canvases")
