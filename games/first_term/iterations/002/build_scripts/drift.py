"""Her reaction drifts when she does it again (DECISIONS 209; LO, 2026-11-09, "Go ahead").

The studied pattern (exhibition_study/C_other_games.md:223, 314, 360): the same request at each visit, and her
reaction moves by visit count: "hesitantly", then quickly but still embarrassed, then not embarrassed. Ours: one
hidden counter per loop, raised by the answer that pays her, and one paragraph on the paid screen that reads it:
the first time (1), the next few (2-4), once it's a habit (5 and up). The paragraph is about her body's habit and
the watchers' habit, never shame against pride, so it is true at every stage the screen can show at; her stage
thought, where a screen has one, stays as it is.

mode "in":  the counter is raised by the choices INTO the paid screen, so the screen reads it after: 1 / 2-4 / 5+.
mode "out": the screen pays on its way OUT (the street, the café, the dares), so it reads it before: 0 / 1-3 / 4+.
"""

# canvas id -> (counter, [paid node ids], mode, (first, again, habit))
DRIFT = {
    # ── the street, once a day (town.py STREET_CASES, street_seen_lowtop) ──
    "street_seen_skirt": ("rep_street_skirt", ["seen"], "out", (
        "Your hands keep going to the hem, tugging it down, every few steps.",
        "Your hands only go to the hem once now, at the gate, and then you leave it alone.",
        "You don't touch the hem at all any more. You walk, and let the street have your legs.")),
    "street_seen_nobra": ("rep_street_nobra", ["seen"], "out", (
        "You walk with your arms half up, ready to fold them over your chest, and you feel every step in your tits.",
        "Your arms stay down now. Your tits move loose under your clothes, and you let them.",
        "You walk with your shoulders back. No bra is just how you go out now, and the street has learned it.")),
    "street_seen_nopanties": ("rep_street_nopanties", ["seen"], "out", (
        "You walk stiff, your thighs pressed together, sure the whole street can tell there's nothing under your clothes.",
        "You walk normally now, almost. Only when the air moves do you remember, and your face goes hot.",
        "You don't think about it any more until a breeze comes. Then you slow down for it.")),
    "street_seen_lowtop": ("rep_street_lowtop", ["walked"], "in", (
        "You keep feeling the neckline sit low, every step, and your hand stays down.",
        "Your hand doesn't even twitch toward the neckline any more. You let the top sit low and the cleavage show.",
        "You walk in the low top like it's nothing, arms down, and the man at the bus stop looks like it's everything.")),
    "street_seen_crop": ("rep_street_crop", ["seen"], "out", (
        "You keep pulling the crop top down over your belly, and it keeps riding back up.",
        "You've stopped pulling it down. It rides up, and your belly's bare, and you let it.",
        "You lift your arms to fix your hair on the corner, on purpose, and the top rides up to the bottom of your tits.")),
    "street_seen_bodycon": ("rep_street_bodycon", ["seen"], "out", (
        "Small steps, so the bodycon dress won't ride up. It rides up anyway.",
        "You walk at your normal pace now and tug the hem down once at the corner, not every few steps.",
        "You let the bodycon dress ride up as far as it wants. You fix it when you get where you're going.")),
    "street_seen_micro": ("rep_street_micro", ["seen"], "out", (
        "You keep reaching back to tug the micro shorts down over your cheeks, and there's nothing to tug.",
        "You've stopped reaching back. Your ass is half out with every step, and your hands stay at your sides.",
        "You walk slower than you need to in the micro shorts, so the people behind you get longer to look.")),
    "street_seen_plunge": ("rep_street_plunge", ["seen"], "out", (
        "You hold one hand flat on your chest the whole way, ready to catch the plunge if it swings open.",
        "Your hand only comes up when you step off the curb. The rest of the way you let the neckline move.",
        "Your hands stay down. The plunge swings with every step, your bare tits loose inside it, and you've stopped caring who sees how much.")),
    "street_seen_split": ("rep_street_split", ["seen"], "out", (
        "You hold the slit shut with your fingers for half the street before you make yourself let go.",
        "You let the slit fall open now. Your bare leg comes out to the hip with every step, and your fingers stay away.",
        "You take long steps in the split skirt, longer than you need to, so it opens all the way every time.")),
    "street_seen_sequin": ("rep_street_sequin", ["seen"], "out", (
        "Every head turns at the sequins, and you want to cross your arms over all of it.",
        "In the sequin dress you walk like you've got somewhere to be. The heads still turn, but you've stopped counting them.",
        "The sequin dress catches every eye on the street, and you've stopped pretending you didn't wear it for that.")),
    "street_seen_backless": ("rep_street_backless", ["seen"], "out", (
        "You can feel the air on your whole bare back, and you keep your arms tight to your sides so the open sides don't swing.",
        "Your arms swing loose now. The open side of the dress swings with them, and you let it.",
        "You walk with your arms loose and your back bare to the whole street, and you know exactly what the open sides show.")),
    # ── campus ──
    "gym_workout": ("rep_gym", ["looked", "mats", "set", "sheer"], "in", {"mats": (
        "Every stretch, you check the mirror wall to see who's watching. Someone always is.",
        "You stretch without checking the mirror now. You know who's at the rack, and which way you're facing.",
        "The guys at the rack are there before you are now, waiting. You lie back on the mat and give them the view."), "*": (
        "Every rep, you check the mirror wall to see who's watching. Someone always is.",
        "You don't need to check the mirror now to know who's at the rack, or where their eyes are.",
        "The guys at the rack are there before you are now, waiting. You don't even look at them. You start your set.")}),
    "college_class_psych": ("rep_class_psych", ["risky"], "in", (
        "Your heart is going so hard in the front row you can hear it over the lecture.",
        "You take the front-row seat without stopping to think now. Your heart still kicks the first time he looks down.",
        "The front-row seat is yours now. Nobody else sits in it, and Dr. Hale knows exactly where to look.")),
    "college_class_business": ("rep_class_business", ["risky"], "in", (
        "You lean back so slowly the guy behind you must think you're stuck.",
        "You don't wait for the right moment now. The guy behind you is ready for it before you've started.",
        "The guy behind you saves his seat for this class now. You don't make him wait long.")),
    "college_class_bio": ("rep_class_bio", ["risky", "risky_mild"], "in", {"risky_mild": (
        "Your face is hot the whole time she's turned away. You can't tell if she saw.",
        "She saw. She turns to the board a little faster every class now.",
        "The TA can't look at the second row at all now. She teaches the whole class to the other side of the room."), "*": (
        "You look the TA in the eye while you do it. Your pulse is going so hard you can feel it in your nipples.",
        "You don't wait for her to look over now. You do it, and then you look up to watch her face go red.",
        "The TA comes down to the second row first every class now. She doesn't even pretend it's to check your work.")}),
    "college_class_figure": ("rep_class_figure", ["risky"], "in", (
        "You lean into the easel so carefully you nearly knock it over.",
        "You lean into the easel without thinking now, and the guy who draws you is already looking.",
        "The guy who draws you has stopped drawing the model in this class. He draws you, every time.")),
    # ── her own loops ──
    "park_run": ("rep_park_run", ["run"], "in", (
        "You run the first lap with your eyes on the path, not on who's watching.",
        "You look up on the second lap now, at the benches, and the regulars are already looking back.",
        "The bench by the pond is never empty when you run any more. You know which faces will be there before you get to it.")),
    "living_stretch": ("rep_stretch", ["held"], "in", (
        "You hold the stretch and count your breaths, and feel exactly where his eyes are.",
        "You hold the stretch with your eyes open now, but you don't look round at him.",
        "You hold the stretch and look straight at whoever's watching, and wait for him to look away first.")),
    "garden_sun": ("rep_garden", ["sun_seen"], "in", (
        "You lie stiff on the lounger, too aware of every window that faces the garden.",
        "You lie loose on the lounger now. You know which windows face the garden, and you lie where they can see you.",
        "You don't pretend it's for the sun any more. You lie out for the windows, and you know who's behind them.")),
    "bathroom_shower": ("rep_shower_door", ["unlocked"], "in", (
        "You reach for the lock twice before you leave it.",
        "You don't reach for the lock any more. You leave the door off the latch and step in.",
        "You leave the door open a crack before you've even turned the water on.")),
    # ── the café (pays as she clocks out) ──
    "cafe_shift": ("rep_cafe_show", ["l1_table", "l2_flirt", "l2_play", "l3_let"], "out", (
        "You do it with your face burning, sure the whole café saw.",
        "You don't stop to think before you do it now, and the regulars grin at you like it's a joke you're all in on.",
        "The regulars sit where they can see you do it now. Tom's noticed which tables fill up first.")),
    # ── people ──
    "zoe_dares": ("zoe_dares_done", ["low_show", "low_do", "high_show", "high_do", "z_show", "z_do"], "out", (
        "Your heart slams the whole time. Half the room doesn't believe you'll do it. Zoe does.",
        "Your heart doesn't slam as much now. Half the room still doesn't believe it until you do it.",
        "The room knows Zoe's dares end with you doing them. They're watching before she's finished saying it.")),
    "hub_mark_garage": ("rep_mark_laundry", ["hl_laundry_tease2", "hl_laundry_tease3"], "in", {"hl_laundry_tease3": (
        "Your heart's going hard when you take hold of the hem of your top. The machine's too loud to hear him breathe.",
        "You pull your top off over your head in one go now, and stand there in your bra while the machine fills.",
        "You don't wait for the machine any more. Your top's off before the drum's loaded, and Mark's already watching."), "*": (
        "You can feel your heartbeat in your face the whole time you're bent over the drum.",
        "You bend over the drum without looking round first now. You know he's watching, and you know where.",
        "Mark's hands stop on the bench the second you bend now.")}),
    "home_event_ryan_door": ("rep_ryan_door", ["ev_curious"], "in", (
        "You stop at his door with your heart in your throat, ready to run if the floor creaks.",
        "You stop at his door without thinking about it now. Your feet know the boards that don't creak.",
        "You stop at his door like it's on the way. Some nights you think he leaves it open for you.")),
}


def counters():
    return sorted({v[0] for v in DRIFT.values()})


def apply(canvas):
    """Adds the counter's +1 and the three-way paragraph to one canvas, if it is in DRIFT."""
    from tomlw import cond, trait, add, flag, fset, funset
    from canv import G, GC, P
    spec = DRIFT.get(canvas["id"])
    if not spec:
        return
    key, nodes, mode, lines = spec
    lo = 1 if mode == "in" else 0     # the first visit's reading
    now = key + "_now"                # mode "in": this visit paid (an unpaid way into the same screen clears it)
    paid = lambda ch: any(e.get("trait") in ("exhibitionism", "corruption") and e.get("op") == "add" for e in ch.get("effects") or [])
    found = set()
    for n in canvas["nodes"]:
        if n["id"] in nodes:
            first, again, habit = lines.get(n["id"], lines.get("*")) if isinstance(lines, dict) else lines
            chain = [GC(cond(trait(key, "lt", lo + 1)), P(first)),
                     GC(cond(trait(key, "lt", lo + 4)), P(again)),
                     GC(cond(trait(key, "gte", lo + 4)), P(habit))]
            # reader (DECISIONS 209): groups back to back join one if/elseif chain (v2.py:18686-18691), so the drift is
            # fenced in its own one-item pool; it would otherwise be the else of the screen's last group
            gate = [flag(now)] if mode == "in" else [{"type": "worn_exposure", "operator": "gte", "value": 0}]
            n["blocks"] = list(n["blocks"]) + [G(cond(*gate), *chain)]
            found.add(n["id"])
            if mode == "out" and key != "zoe_dares_done":   # the dares already count themselves (pools.py)
                for ch in n["choices"]:
                    if paid(ch):
                        ch["effects"] = list(ch.get("effects") or []) + [add(key, 1, clamp=False)]
        if mode == "in":
            for ch in n["choices"]:
                if ch.get("targetType") == "node" and ch.get("nodeId") in nodes:
                    fl = ch["flagEffects"] = list(ch.get("flagEffects") or [])   # choices can share one list (reader)
                    if paid(ch):
                        ch["effects"] = list(ch.get("effects") or []) + [add(key, 1, clamp=False)]
                        fl.append(fset(now))
                    else:
                        fl.append(funset(now))
    assert found == set(nodes), (canvas["id"], set(nodes) - found)
