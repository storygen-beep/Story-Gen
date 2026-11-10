"""Everyday random scenes at home, batch 1: Laura, Ryan, Mark (DECISIONS 221; LO, 2026-11-10: "Go ahead").

Why: the random-scenes studies (~/Documents/Great_Games_Study_20260926/playtest_study_20261109/
13_random_scenes_top.md, 14_random_scenes_ours.md). 69 of our 82 random scenes were sexual or about her body,
Ryan and Laura had no everyday scene and Mark one, and at almost every place only one scene could fire, so a
repeat was always the same. Course of Temptation, the model: each scene about one screen, a choice, the person
who is really there and what they want setting the tone (its hall bump: an apology, a grope or a shove),
about 4 in 10 moving a relationship, and a repeat that rests a day or goes one step further (its workers'
five-scene chain; IHOH's Shaun by visit count).

The shape here, with what the engine already has (v2.py checkRandomEncounters :6747-6879, canvasRollChance
:6327):
- a random-mode canvas at the person's place, bound to them (`requires_npc`) inside their own row's hours;
- one screen, then her answer's own short screen (the written no is one of the answers);
- each answer moves his or her meter, or records a flag that his hub reads the next day (HUB_READS);
- `<id>_today` (cleared at midnight) keeps each to once a day, `everyday_home_today` keeps the plain ones to one
  a day at home in all, and `seen_weight` makes one she has seen come up less often;
- MIXED scenes read his Want (Laura: her Love) and play as everyday low and as heat high;
- CHAINS count up a hidden trait: each rung opens only after the one before, at her stage, once a day.
Mark's ceiling this release is looks and brushes (DECISIONS 107); his chain stops at a brush.
"""
import sys
from canv import *
from tomlw import tod, wd
from home_items import CURIOUS, BOLD, DARING, here, since

R, L, M = "npc_ryan", "npc_laura", "npc_mark"
K, LR, HALL, GAR = "home_kitchen", "home_living_room", "home_hall", "home_garage"
BRAKE = "everyday_home_today"
DAILY_FLAGS = [BRAKE]       # every flag here that [engine.daily_tick] clears (0_systems_spec.toml)
COUNTERS = []               # every chain counter (hidden player traits, gen_world.py + 0_systems_spec.toml)
HUB_READS = {}              # hub id -> [group blocks]: the day after, his hub remembers
SUB_RULES = {}              # host canvas id -> [substitution rules] (attach_subs, called by the host's part)
out = []


def S(days, a, b):
    return [{"weekdays": list(days), "start_time": a, "end_time": b}]


def _remember(hub, rec, *blocks, lo=6, hi=30):
    """His hub remembers `rec` from `lo` hours after it was set (never the same visit; the scene's exit is his
    room) until `hi`. `rec` is the answer's own flag, so a line about the yes never follows the no (scene reader
    2026-11-10)."""
    HUB_READS.setdefault(hub, []).append(G(cond(flag(rec), since(rec, "gte", lo), since(rec, "lt", hi)), *blocks))


def scene(cid, name, loc, who, sched, conds, lead, answers, hook, chance=0.3, plain=True, bound=True, rest=None,
          sub_host=None, entry=()):
    """One everyday or mixed scene. answers: [(label, cond_items, eff, reply_blocks, extra_flags[, back])].
    The answer screen's exit returns to the room (or `back`); the record flag `cid` rides every answer. A band
    that a meter decides is split into separate answers with their own conditions, because the answer's raise
    lands before its screen is read (scene reader 2026-11-10)."""
    today = f"{cid}_today"
    DAILY_FLAGS.append(today)
    items = [flag("opening_done"), flag(today, False)] + ([flag(BRAKE, False)] if plain else []) \
        + ([flag(rest, False)] if rest else []) + list(conds)
    if sub_host:
        # a walk-in on one of her acts there (the café: gate `nothing one-time at the shop or wardrobe` keeps random
        # events out of the uniform room); the rule carries the hours, one rule per window
        trig = {"location": loc, "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "conditions": cond(*items)}
        for w in sched:
            SUB_RULES.setdefault(sub_host, []).append({"target_canvas_id": cid, "chance": chance, "conditions": cond(
                here(who, loc), wd(*w["weekdays"]), tod(w["start_time"], w["end_time"]))})
    else:
        trig = {"location": loc, "is_repeatable": True, "priority": 3, "is_active": True,
                "trigger_mode": "random", "chance": chance, "seen_weight": 0.4,
                "schedules": sched, "conditions": cond(*items)}
    if entry:
        trig["pre_substitution_effects"] = list(entry)   # his raise for what happened, on the way in (home.py event())
    if bound:
        trig["requires_npc"] = who
    choices, nodes = [], []
    for i, ans in enumerate(answers):
        label, citems, eff, reply, extra = ans[:5]
        back = ans[5] if len(ans) > 5 else loc
        nid = f"a{i}"
        flags = [fset(cid), fset(today)] + ([fset(BRAKE)] if plain else []) + ([fset(rest)] if rest else []) \
            + [fset(f) for f in extra]
        choices.append(go(label, node=nid, mins=5, cond_=cond(*citems) if citems else None, eff=eff or None, flags=flags))
        nodes.append(node(nid, label.strip('".').rstrip("."), list(reply) + [hook], [go("Go on.", loc=back, mins=5)]))
    c = {"id": cid, "name": name,
         "description": f"Everyday random scene at home (DECISIONS 221): {name}. Chance {chance}, once a day.",
         "trigger": trig, "nodes": [node("scene", name, list(lead), choices)] + nodes}
    out.append(c)
    return c


def chain(prefix, name, loc, who, sched, conds, rungs, hook):
    """An escalating chain: rung k opens when `<prefix>_n` is k-1 and its own gate holds; its "further" answer
    sets the counter to k and records `<prefix>_<k>_yes`. rungs: [(gate_items, lead, further(label, eff, reply[,
    cond_items]), other_answers)]."""
    counter = f"{prefix}_n"
    COUNTERS.append(counter)
    rest = f"{prefix}_today"      # one rung a day: the chain rests a day between steps (CoT's day cooldown)
    DAILY_FLAGS.append(rest)
    for k, (gate, lead, further, others) in enumerate(rungs, start=1):
        label, eff, reply = further[:3]
        fcond = further[3] if len(further) > 3 else []
        answers = [(label, fcond, list(eff) + [setv(counter, k)], reply, [f"{prefix}_{k}_yes"])] + list(others)
        scene(f"{prefix}_{k}", f"{name} ({k})", loc, who, sched, list(conds) + [trait(counter, "eq", k - 1)] + list(gate),
              lead, answers, hook, chance=0.3, plain=False, rest=rest)


def love(n):
    return nadd(L, "warmth", n)


def his(npc, key, n):
    return nadd(npc, key, n)


def her(meter, cap):
    return {"targetType": "player", "trait": meter, "op": "add", "value": 1, "cap": cap}


LAURA_COOKS = [0, 1, 3, 4, 6]          # her kitchen evenings, 18:00-21:30 (v2_state.json)
NO_DINNER_CROWD = [here(M, K, False), here(R, K, False)]

# ═════════════════════════════════════════════════════════════════════════════
# LAURA
# ═════════════════════════════════════════════════════════════════════════════
scene("ev_laura_did_you_eat", "Did you eat?", K, L, S(LAURA_COOKS, "19:00", "21:15"),
      [flag("ate_dinner", False)] + NO_DINNER_CROWD,
      [P("Laura's wiping down the counter. She looks you over, the way she does, top to toe."),
       D(L, "Did you eat today? Real food. Not crisps out of the bag."),
       ME("Define real."),
       D(L, "Something with a plate under it, sweetheart.")],
      [("\"Not really.\"", [], [love(2)],
        [P("She's already pulling a plate out of the oven, where she kept it warm. She sits you down and sits across from you and watches you eat every bite."),
         D(L, "Look at you. You're too thin for all those classes."), ME("I'm fine, Mom."), D(L, "You're fine when you've eaten.")], ["laura_fed_her"]),
       ("\"I had something at college.\"", [], [love(1)],
        [P("She narrows her eyes at you, but she lets it go."), D(L, "Then there's a plate in the oven for later. Don't let Ryan find it.")], []),
       ("\"I'm not hungry, Mom.\"", [], [],
        [D(L, "You never are."), P("She covers the plate with foil and puts it back in the oven anyway, and she pats your cheek on her way past."),
         D(L, "It'll be in there when you are.")], [])],
      P("She cooks most nights. There's always a plate."))
_remember("hub_laura_kitchen", "laura_fed_her", D(L, "You cleared that plate I kept for you. I'm making it again."))

scene("ev_laura_phone_call", "On the phone", K, L, S([0, 1, 2, 3, 4], "07:00", "07:50"),
      [here(M, K, False)],
      [P("Laura's at the counter in her work blouse with her phone clamped to her ear, toast burning under the grill behind her."),
       D(L, "No, I said Thursday. Thursday, Dennis. I sent it."),
       P("She sees the smoke, then you, and her eyes go wide over the phone: help.")],
      [("Rescue the toast.", [], [love(2)],
        [P("You whip the toast out and scrape the black off into the sink. She mouths thank you, and when she hangs up she kisses the top of your head."),
         D(L, "That man. I swear I'll strangle him with his own lanyard."), ME("You'll get him, Mom.")], ["laura_toast_saved"]),
       ("Mouth: you've got this.", [], [love(1)],
        [P("She rolls her eyes, but she stands up straighter, and her voice goes cool and sure."),
         D(L, "Dennis. It's in your inbox. Thursday. Goodbye."), P("She hangs up and laughs, a little shaky."), D(L, "Did I sound mean?"), ME("You sounded great.")], []),
       ("Leave her to it.", [], [],
        [P("You take your coffee to the far end of the counter and leave her to it. She's still saying Thursday, louder each time."),
         D(L, "Thursday!")], [])],
      P("She takes his calls at the counter most mornings before work."))
_remember("hub_laura_kitchen", "laura_toast_saved", D(L, "Dennis got the file. Thursday, like I told him. Thank you for the toast."))

scene("ev_laura_list", "The shopping list", K, L, S(LAURA_COOKS, "19:00", "21:15"),
      NO_DINNER_CROWD,
      [P("Laura's at the kitchen table with a pen and the back of an envelope, the shopping list half written."),
       D(L, "Anything you want this week? Speak now, or it's Ryan's cereal again.")],
      [("\"The good yoghurt. The Greek one.\"", [], [love(1)],
        [D(L, "Fancy."), P("She writes it down and underlines it twice."), D(L, "Don't tell Mark what it costs.")], []),
       ("\"Wine. For you.\"", [CURIOUS], [love(2)],
        [P("She laughs, surprised, and points the pen at you."), D(L, "For me. Of course."),
         P("She writes it down anyway, and her cheeks go pink, and she doesn't cross it out.")], ["laura_wine_listed"]),
       ("\"Whatever. I don't mind.\"", [], [],
        [D(L, "You'd mind if I bought the wrong shampoo."), ME("That's different."), D(L, "It always is."), P("She says it lightly, but she writes your shampoo down anyway.")], [])],
      P("She does the list at this table every week."))
_remember("hub_laura_kitchen", "ev_laura_list", D(L, "The list's on the fridge. Add anything I forgot."), lo=1)

# MIXED: her shoulders. Her Love sets it: tired mom, or her leaning back into you (her own want; the-heat-ladder H1)
scene("ev_laura_shoulders", "Her shoulders", K, L, S(LAURA_COOKS, "20:30", "21:15"),
      NO_DINNER_CROWD,
      [P("Laura's at the table with her shoes off and her feet on a chair, rolling her neck until it cracks."),
       D(L, "Don't get old, sweetheart. Everything hurts."),
       GC(cond(ntrait(L, "warmth", "lt", 60)), D(L, "Be an angel and rub my shoulders for one minute.")),
       GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), D(L, "Come here. Your hands. My shoulders. Please."),
          P("She's already undone the top two buttons of her blouse to give you room."))],
      [("Rub her shoulders.", [ntrait(L, "warmth", "lt", 60)], [love(2)],
        [P("You work your thumbs into the knots at the top of her back. She groans and drops her head forward."),
         D(L, "Oh, that's the spot. Who taught you that?"), ME("YouTube."), D(L, "Bless YouTube.")], ["laura_shoulders_rubbed"]),
       ("Rub her shoulders.", [ntrait(L, "warmth", "gte", 60)], [love(2)],
        [P("You work your thumbs into her shoulders, and she leans her head back against your stomach. Her blouse gapes open. From above you can see right down it to her tits, soft and heavy, rising when she breathes."),
         D(L, "Lower. God, that's good. A bit lower."),
         P("Your hands slide down onto her collarbones. She doesn't stop you. Her nipples have gone hard against the cotton, and she has to know you can see."),
         D(L, "That's enough. That's. Thank you, sweetheart.")], ["laura_shoulders_rubbed"]),
       ("\"Ask Mark.\"", [], [],
        [P("She snorts."), D(L, "Mark's hands are for engines."), ME("Fair."), P("She does her own neck, one-handed, and winces.")], [])],
      P("Her shoulders always hurt after work."))
_remember("hub_laura_kitchen", "laura_shoulders_rubbed", D(L, "My neck's still thanking you."))

# ═════════════════════════════════════════════════════════════════════════════
# RYAN
# ═════════════════════════════════════════════════════════════════════════════
RYAN_COUCH_EVE = S([0, 1, 3, 6], "19:00", "20:15") + S([2], "19:00", "20:45")
scene("ev_ryan_cover", "Cover for me", LR, R, RYAN_COUCH_EVE,
      [here(L, LR, False)],
      [P("Ryan pauses his game and twists round on the couch to look at you."),
       D(R, "If Mom asks about the noise Friday night, it was my game. The headset broke."),
       ME("Was it?"),
       D(R, "Does it matter? Just say you heard the game.")],
      [("\"Fine. You owe me.\"", [], [his(R, "warmth", 2)],
        [D(R, "I owe you. Write it down."), P("He unpauses the game, but he's grinning at the screen.")], ["ryan_owes_her"]),
       ("\"Where were you really?\"", [], [his(R, "warmth", 1)],
        [P("He looks at you for a long second."), D(R, "It wasn't the game. That's all you get."),
         GC(cond(flag("knows_about_kayla")), ME("Kayla?")), GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), ME("Who?")),
         D(R, "That's all you get, @player.nickname.")], []),
       ("\"Lie to her yourself.\"", [], [],
        [D(R, "Wow. Thanks. Family."), P("He unpauses the game and shoots something very hard.")], [])],
      P("He's on that couch most evenings after dinner."))
_remember("hub_ryan_living_room", "ryan_owes_her", D(R, "I still owe you. Don't think I forgot."))

scene("ev_ryan_shift", "His shift", LR, R, S([5, 6], "14:00", "17:45"),
      [here(L, LR, False)],
      [P("Ryan's on the couch with his phone, typing with both thumbs, his jaw tight."),
       D(R, "My boss wants me in next Sunday. Six a.m. Again."),
       D(R, "Help me say no without getting fired.")],
      [("Write it for him.", [], [his(R, "warmth", 2)],
        [P("You take his phone and type it: sorry, family thing, happy to do next week. You hit send before he can argue."),
         D(R, "You just sent that."), ME("You're welcome."), P("His phone buzzes. He reads it, and his whole face changes."),
         D(R, "He said fine. He said fine! You're a genius.")], ["ryan_shift_saved"]),
       ("\"Just go in. It's money.\"", [], [his(R, "warmth", 1)],
        [D(R, "Spoken like someone who's never been up at five."), P("But he types yes, sighing, and drops the phone on his chest.")], []),
       ("\"Not my problem.\"", [], [],
        [D(R, "Cold, @player.nickname."), P("He goes back to his phone, but he just types and deletes, types and deletes.")], [])],
      P("Weekends, the couch is his."))
_remember("hub_ryan_living_room", "ryan_shift_saved", D(R, "Still got my Sunday off. Because of you."), hi=168)

scene("ev_ryan_dinner_kick", "Under the table", K, R, S([0, 1, 3], "18:00", "18:45"),
      [here(L, K), here(M, K)],
      [P("Dinner. Laura is asking Ryan about money again, the yard, his savings, and he's running out of answers."),
       D(L, "So how much is in it? Roughly."),
       P("Under the table his foot finds yours and presses, twice. He's staring at his plate. Help.")],
      [("Change the subject.", [], [his(R, "warmth", 2)],
        [ME("Mom, did you get that promotion thing sorted?"), P("Laura lights up and talks for ten minutes. Mark grunts in the right places. Ryan eats fast."),
         P("When she gets up for the salt he leans over."), D(R, "I owe you. Again.")], ["ryan_owes_her"]),
       ("Kick him back. Hard.", [], [],
        [P("He jerks and bangs his knee on the table. Everybody looks at him."), D(M, "Something wrong with you?"), D(R, "Cramp."),
         P("Laura goes back to the savings. He glares at you across the potatoes.")], ["ryan_kicked"]),
       ("Let him squirm.", [], [],
        [P("You eat. He squirms. Laura gets a number out of him, a small one, and her mouth goes thin."), D(L, "We'll talk about it.")], [])],
      P("Laura asks about money at most dinners."))
_remember("hub_ryan_kitchen", "ryan_kicked", D(R, "My shin's still purple. Thanks for that."))

# MIXED: the hall at night. His Want sets it (the CoT bump): sorry under 40; at 40, he doesn't move.
scene("ev_ryan_hall_squeeze", "In the hall", HALL, R, S([0, 1, 2, 3, 6], "22:00", "23:45"),
      [here(R, "home_ryan_room"), here(L, HALL, False)],
      [P("Ryan's door opens as you pass, and he comes out in his shorts on his way to the bathroom. The hall's too narrow for two."),
       GC(cond(ntrait(R, "want", "lt", 40)), P("He backs up against the wall to let you by, his eyes on the ceiling."), D(R, "Sorry. Go. You first.")),
       GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}),
          P("He doesn't back up. He stops right in the middle, so you'd have to squeeze past with your tits against his chest."),
          D(R, "You first, @player.nickname."))],
      [("Slip past.", [ntrait(R, "want", "lt", 40)], [his(R, "want", 1)],
        [P("You slip past. Your shoulder brushes his arm, and he goes red to the ears."), D(R, "Night.")], []),
       ("Squeeze past him.", [ntrait(R, "want", "gte", 40), BOLD], [his(R, "want", 1)],
        [P("You turn side-on and squeeze past him. Your tits drag across his bare chest, slow, and your nipples go hard. He breathes in through his nose and holds it."),
         P("By the time you're past, his shorts are tenting. He doesn't hide it."), D(R, "Night, @player.nickname."),
         P("He goes into the bathroom and turns the lock. You stand in the dark hall with your nipples aching. Not tonight. Not in the hall.")], ["ryan_squeezed_hall"]),
       ("\"Move, Ryan.\"", [], [],
        [D(R, "Moving."), P("He flattens himself against the wall, grinning, and lets you by without touching."), ME("Thank you."), D(R, "Anytime.")], [])],
      P("He goes to the bathroom about now most nights."), bound=False)
_remember("hub_ryan_room", "ev_ryan_hall_squeeze", D(R, "That hall's too small. I'm not complaining."))

# CHAIN: the bet on his game. Each round one step further; rung 3 needs his step 3 and her Curious, rung 4 his
# step 4 and her Bold. Laura is never in the room (the couch screen's own rule, ryan.py LAURA_NOT_HERE).
RYAN_COUCH_ALL = RYAN_COUCH_EVE + S([5, 6], "14:00", "17:45")
chain("ev_ryan_bet", "The bet", LR, R, RYAN_COUCH_ALL, [here(L, LR, False), here(M, LR, False)], [
    ([],
     [P("Ryan holds out the second controller without looking away from the screen."),
      D(R, "One round. Loser makes the tea.")],
     ("Play.", [his(R, "warmth", 1)],
      [P("You lose in ninety seconds. He makes you make the tea anyway, and he drinks it like a king."),
       D(R, "Two sugars next time. Same bet tomorrow.")]),
     [("\"Make your own tea.\"", [], [], [D(R, "Coward."), P("He plays on alone, loudly winning.")], [])]),
    ([],
     [D(R, "New bet. Loser answers one question. Honestly."),
      P("He's already holding out the controller.")],
     ("Play.", [his(R, "warmth", 1), his(R, "want", 1)],
      [P("You lose. Of course you lose."), D(R, "First kiss. Who, where."),
       ME("Danny Price. Behind the gym. He tasted like crisps."),
       P("He laughs so hard he drops his controller. Then he stops laughing and looks at your mouth a second too long.")]),
     [("\"I'm not answering anything.\"", [], [], [D(R, "Then you can't lose. Boring."), P("He plays on.")], [])]),
    ([trait("ryan_step", "gte", 3), CURIOUS],
     [D(R, "Stakes. Loser takes something off. One thing."),
      P("He doesn't look at you when he says it. His ears have gone red.")],
     ("Play.", [his(R, "want", 2), her("corruption", 39)],
      [P("You lose. You take your top off and drop it on the floor, and play the next round in your bra with the controller in your lap."),
       P("He loses that one on purpose, staring at your tits instead of the screen. When it's over you pull your top back on, slow."), D(R, "Best of three?")],
      [{"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}]),
     [("\"Nice try.\"", [], [], [D(R, "Worth asking."), P("He goes back to the game, but his knee is bouncing.")], [])]),
    ([trait("ryan_step", "gte", 4), BOLD],
     [D(R, "Last bet. Loser plays the next round in the winner's lap."),
      P("He pats his thigh. He's not joking.")],
     ("Play.", [his(R, "want", 2), her("corruption", 59)],
      [P("You lose. You climb into his lap with your back to his chest and the controller in your hands, and he wraps his arms round you to hold his."),
       P("Every time you move, you grind on him, and he's rock hard against your ass through his shorts. You lose that round too. Neither of you looks at the score."),
       D(R, "Again. Same seat.")]),
     [("\"In your dreams.\"", [], [], [D(R, "Every night."), P("He says it to the screen, and he doesn't look round.")], [])]),
], P("He's on the couch most days, and he always wants a rematch."))
for _k, _l in ((1, "You still owe me two sugars."), (2, "Danny Price. Behind the gym. I can't stop laughing."),
               (3, "I'm still thinking about best of three."), (4, "Rematch. Same seat.")):
    _remember("hub_ryan_living_room", f"ev_ryan_bet_{_k}_yes", D(R, _l))

# ═════════════════════════════════════════════════════════════════════════════
# MARK (his meter is Power: hers to give or take; his ceiling this release is looks and brushes)
# ═════════════════════════════════════════════════════════════════════════════
scene("ev_mark_bills", "The bills", K, M, S([6], "10:00", "17:00"),
      [here(L, K, False)],
      [P("Mark's at the Sunday table with the bills spread out in front of him and a calculator older than you."),
       D(M, "Somebody in this house leaves every light on. Every light, @player."),
       P("He holds up the electric bill like evidence.")],
      [("\"Sorry. I'll turn them off.\"", [], [his(M, "power", 1)],
        [D(M, "That's all I ask."), P("He goes back to his sums, satisfied, and you feel about twelve.")], []),
       ("\"That's Ryan, not me.\"", [], [his(M, "power", -1)],
        [P("He looks at you over his glasses."), D(M, "Is it."), ME("He sleeps with his lamp on."),
         D(M, "Huh."), P("He writes RYAN on the bill and circles it.")], ["mark_blames_ryan"]),
       ("\"Not my bill, Mark.\"", [], [his(M, "power", -1)],
        [D(M, "Everything under this roof is your bill, @player."), P("He says it to the calculator, not to you.")], [])],
      P("Sundays he does the bills at this table."))
_remember("hub_mark_kitchen", "mark_blames_ryan", D(M, "I had a word with Ryan about that lamp of his."), lo=1)

scene("ev_mark_radio", "The garage radio", GAR, M, S([0, 1, 3, 4], "19:00", "21:45") + S([5], "09:00", "16:45"),
      [],
      [P("Mark's under the car on his back, only his legs sticking out. The radio on the bench is playing something from before you were born."),
       D(M, "Ten mill. On the bench. Pass it here."),
       P("A hand comes out from under the car, open, black with oil.")],
      [("Pass it, and stay.", [], [],
        [P("You put the wrench in his hand and sit on the upturned bucket. He talks from under the car, about the first car he ever had, a rust bucket he loved more than his first wife."),
         D(M, "Drove it into a lake once. Long story."), ME("Tell me."), D(M, "Another time."),
         P("But he's smiling. You can hear it.")], ["mark_told_car"]),
       ("Pass it.", [], [his(M, "power", 1)],
        [P("You put the wrench in his hand."), D(M, "Good."), P("The hand goes back under the car.")], []),
       ("\"Get it yourself.\"", [], [his(M, "power", -1)],
        [P("A long pause. Then he slides out on the creeper, gets the wrench himself, and slides back under without a word."),
         D(M, "Close the door on your way out.")], [])],
      P("He's out here most evenings with that radio."))
_remember("hub_mark_garage", "mark_told_car", D(M, "The lake. It was a Tuesday. I'll tell you sometime."), hi=96)

scene("ev_mark_chilli", "Wednesday chilli", K, M, S([2], "18:15", "21:30"),
      [],
      [P("Mark has every pan in the house out and the kitchen smells like it's on fire. He holds a spoon out to you over the pot."),
       D(M, "Taste. Tell me the truth.")],
      [("\"It's good. Really.\"", [], [his(M, "power", 1)],
        [P("It's good. It's very hot. Your eyes water."), D(M, "Told you."), P("He looks pleased in a way you don't see often, and he gives you a bowl to yourself.")], ["mark_fed_her"]),
       ("\"It needs salt.\"", [], [his(M, "power", -1)],
        [P("He tastes it himself. He frowns. He adds salt."), D(M, "Fine. It needed salt."), ME("You're welcome."),
         D(M, "Don't push it.")], []),
       ("\"I'll eat later.\"", [], [],
        [D(M, "Suit yourself. There won't be any."), P("He turns back to the pot, but he leaves a bowl out on the side.")], [])],
      P("Wednesdays, he cooks."))
_remember("hub_mark_kitchen", "mark_fed_her", D(M, "Chilli's better the second day. There's a pot in the fridge."), lo=8)

# MIXED: the creeper. His Want sets it: a plain hand-me-the-light, or he rolls out and looks before he speaks.
scene("ev_mark_creeper", "The creeper", GAR, M, S([0, 1, 3, 4], "19:00", "21:45") + S([5], "09:00", "16:45"),
      [flag("mark_saw_her")],
      [P("You're crossing the garage when Mark rolls out from under the car on the creeper, right at your feet."),
       GC(cond(ntrait(M, "want", "lt", 40)), P("He looks up at your face and holds out a hand."), D(M, "Light. Bench. Thanks.")),
       GC(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
          P("He doesn't look at your face first. From down there he looks straight up your skirt, up your bare thighs, and takes his time about it."),
          D(M, "Light's on the bench, @player.")),
       GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}),
          P("He lies there and looks up the length of you, slow, from your ankles to your tits, before he gets to your face."),
          D(M, "Light's on the bench, @player."))],
      [("Fetch the light.", [ntrait(M, "want", "lt", 40)], [],
        [P("You hand it down. He clicks it on and rolls back under."), D(M, "Cheers.")], ["mark_light_fetched"]),
       ("Fetch the light, side-on to him.", [ntrait(M, "want", "gte", 40)], [his(M, "want", 1)],
        [P("You get the light and hand it down without bending in front of him. His eyes go up you anyway, slow."),
         D(M, "Cheers."), P("He doesn't roll back under until you've gone.")], ["mark_light_fetched"]),
       ("Bend for it, your back to him.", [ntrait(M, "want", "gte", 40), BOLD], [his(M, "want", 1)],
        [P("You bend for the light with your back to him, and you know exactly what he can see from the floor. When you hand it down his fingers brush yours."),
         D(M, "Cheers."), P("He doesn't roll back under until you've gone.")], ["mark_light_fetched"]),
       ("Step over him.", [], [his(M, "power", -1)],
        [P("You step over him and keep walking."), D(M, "Watch the oil."), P("You hear the creeper roll back under.")], [])],
      P("He's under that car most evenings."))
_remember("hub_mark_garage", "mark_light_fetched", D(M, "Thanks for the light, the other day."), lo=12, hi=72)

# CHAIN: his late TV. Each night a step closer, and no further than a brush (his ceiling this release).
MARK_TV = S([6, 0, 1, 2, 3, 4], "22:00", "23:45") + S([0, 1, 2, 3, 4, 5], "00:00", "01:30")
chain("ev_mark_tv", "Late TV", LR, M, MARK_TV, [here(R, LR, False), here(L, LR, False), flag("mark_saw_her")], [
    ([],
     [P("Mark's on the couch with the late film and a beer. He shifts his feet off the cushion without being asked."),
      D(M, "Sit if you're sitting. It's nearly the good bit.")],
     ("Sit and watch.", [his(M, "power", 1)],
      [P("You sit at the other end. It's a war film. He knows every line and says half of them under his breath."),
       D(M, "Same time tomorrow, if you want the ending.")]),
     [("\"I'm off to bed.\"", [], [], [D(M, "Night."), P("He turns the volume up a notch as you go.")], [], HALL)]),
    ([],
     [P("Mark's on the couch again with the film on. He holds a second can out to you without taking his eyes off the screen."),
      D(M, "Don't tell your mother.")],
     ("Take the beer.", [his(M, "power", 1), his(M, "want", 1)],
      [P("You take it and sit closer than you did before, the middle cushion between you. He clinks his can on yours."),
       P("When you tuck your feet up he looks at your legs, once, and then at the film.")]),
     [("\"I don't drink.\"", [], [], [D(M, "Smart."), P("He drinks yours too.")], [])]),
    ([CURIOUS],
     [P("The film's on. Mark's arm is along the back of the couch, and he leaves it there."),
      D(M, "Sitting?")],
     ("Sit in the middle.", [his(M, "want", 2), her("corruption", 39)],
      [P("You sit in the middle, right under his arm on the back of the couch. It doesn't come down. His fingers hang an inch above your shoulder."),
       P("Neither of you watches the film. When you lean back, your hair brushes his wrist, and he goes very still.")]),
     [("Take the end seat.", [], [], [P("You take the end. His arm stays on the back of the couch, on nothing."), D(M, "Suit yourself.")], [])]),
    ([BOLD],
     [P("Mark's on the couch with the film. He pats the cushion right beside him."),
      D(M, "Here.")],
     ("Sit right beside him.", [his(M, "want", 2), her("corruption", 59)],
      [P("You sit close at his side. Halfway through the film his hand comes off his knee and rests on the cushion, an inch from your thigh."),
       P("When you shift, your leg brushes it, once. He doesn't move it, and he doesn't move closer. Your nipples are hard and he can see them, and the film goes on."),
       D(M, "Good film."), ME("Yeah.")]),
     [("Sit at the end.", [], [], [D(M, "Suit yourself."), P("He takes his hand back.")], [])]),
], P("He watches the late film most nights."))
for _k, _l in ((1, "They all die at the end, by the way."), (2, "Your mother found a can in the bin. I said it was mine."),
               (3, "Film's on again tonight."), (4, "Film's on again tonight. Same seat.")):
    _remember("hub_mark_living_room", f"ev_mark_tv_{_k}_yes", D(M, _l), lo=10)

# ═════════════════════════════════════════════════════════════════════════════
# BATCH 2, OUT (LO, 2026-11-10: "okay go ahead"): Zoe, Jake, Nadia, Tom. Zoe, Jake and Nadia keep no meter of
# their own, so their scenes move a flag their hub reads, or her own meter; Tom's Power. Their ladders already
# escalate (Zoe's dares, Jake's dates), so batch 2 has no chains. Tom stays strict this release (npc_tom.md).
# ═════════════════════════════════════════════════════════════════════════════
BRAKE_OUT = "everyday_out_today"
DAILY_FLAGS.append(BRAKE_OUT)
Z, J, N, T_ = "npc_zoe", "npc_jake", "npc_nadia", "npc_tom"
LUNCH = S([0, 1, 2, 3, 4], "11:45", "12:45")


MET_FLAG = {Z: "zoe_met", J: "jake_met", N: "nadia_met", T_: "tom_met"}


def out_scene(cid, name, loc, who, sched, conds, *a, **k):
    """An everyday scene away from home: once a day each, one a day away from home in all, and only once she
    has met the person (scene reader 2026-11-10: the rows alone are not the meeting)."""
    c = scene(cid, name, loc, who, sched, [flag(MET_FLAG[who])] + list(conds), *a, plain=False, rest=BRAKE_OUT, **k)
    c["description"] = c["description"].replace("at home", "away from home")
    return c


out_scene("ev_zoe_fries", "Your fries", "canteen", Z, S([0, 1, 2, 3], "11:45", "12:45"), [],
          [P("You've barely sat down when a hand comes over your shoulder and steals three of your fries."),
           D(Z, "Tax. You looked lonely."),
           P("Zoe drops onto the bench beside you with nothing on her own tray but a coffee.")],
          [("\"Get your own.\"", [], [],
            [D(Z, "Rude."), P("She says it, but she steals two more anyway, and you let her.")], []),
           ("Push the tray over.", [], [],
            [P("She grins and pulls the whole tray into the middle."), D(Z, "This is why I love you. Also, I'm broke till Friday."),
             ME("You're always broke till Friday."), D(Z, "And yet I always survive."),
             D(Z, "Friday. Party at mine. You're coming. That's the payment for the fries.")], ["zoe_fed"]),
           ("Steal her coffee back.", [], [],
            [P("You take her coffee and drink half of it while she watches, outraged."), D(Z, "That was my whole lunch!"), ME("Tax.")], ["zoe_coffee_stolen"])],
          P("She finds you at lunch most days."))
_remember("hub_zoe_canteen", "zoe_fed", D(Z, "I owe you fries. I'm keeping a list."), lo=12)
_remember("hub_zoe_canteen", "zoe_coffee_stolen", D(Z, "I'm guarding this coffee with my life."), lo=12)

out_scene("ev_zoe_mum", "Her mum", "quad", Z, S([1, 3, 4], "14:30", "17:45"), [],
          [P("Zoe's lying on the grass when her phone rings. She looks at the screen and groans."),
           D(Z, "It's my mum. If I don't answer she'll call the college."),
           P("She answers it with a face like she's swallowed a lemon.")],
          [("Lie down beside her.", [], [],
            [P("You lie down beside her on the grass while her mum talks and talks. Zoe says yes, Mum, no, Mum, and holds your hand the whole time without looking at you."),
             P("When she hangs up she lets out a long breath."), D(Z, "She says hi. She thinks you're a good influence."), ME("I am a good influence."), D(Z, "God help us all.")], ["zoe_mum_stayed"]),
           ("\"Want me to go?\"", [], [],
            [D(Z, "No. Stay. Make faces at me."), P("You make faces at her while she says yes, Mum, and she nearly laughs down the phone.")], []),
           ("Leave her to it.", [], [],
            [P("You wave and leave her to it. Behind you she's saying no, Mum, I am eating, I promise.")], [], "campus")],
          P("Her mum calls most weeks, always at the worst time."))
_remember("hub_zoe_quad", "zoe_mum_stayed", D(Z, "My mum asked about you again. You're her favourite now."), lo=12, hi=96)

out_scene("ev_zoe_smoothie", "The smoothie", "park", Z, S([5, 6], "08:00", "09:45"), [],
          [P("Zoe's on the bench by the gates with two smoothies, sweaty from her run, holding one out to you."),
           D(Z, "Kale and mango. Don't make that face. It's good for you.")],
          [("Drink it.", [], [],
            [P("It's awful. You drink all of it to make her happy, and she watches you like she knows."), D(Z, "Liar. You hate it."), ME("I love it."),
             D(Z, "Then next weekend you run the whole loop with me. No stopping. That's the deal.")], ["zoe_smoothie_drunk"]),
           ("\"What's actually in it?\"", [], [],
            [D(Z, "Kale. Mango. Love. Don't ask about the rest."), P("You sip it. You stop asking.")], []),
           ("\"I'll pass.\"", [], [],
            [D(Z, "More for me."), P("She drinks both, one in each hand, staring you down.")], [])],
          P("Weekend mornings she runs here."))
_remember("hub_zoe_park", "zoe_smoothie_drunk", D(Z, "You drank the whole kale one. I'm still proud of you."), lo=20, hi=200)

# MIXED: the sunscreen. Before they're together it's a friend's back; after, and Daring, her hands go under the
# strap on the open quad.
SUN_FRIEND = flag("zoe_together", False)
out_scene("ev_zoe_sunscreen", "Sunscreen", "quad", Z, S([1, 3, 4], "14:30", "17:45"), [],
          [P("Zoe's on her front on the grass with her top rolled up, holding a bottle of sunscreen over her shoulder."),
           D(Z, "Do my back? I'm turning into a lobster.")],
          [("Do her back.", [SUN_FRIEND], [],
            [P("You kneel and rub it into her shoulders and down her back. She sighs into her arms."), D(Z, "You're hired. Daily."), ME("I charge."), D(Z, "Put it on my tab.")], ["zoe_sunscreen_done"]),
           ("Do her back.", [flag("zoe_together")], [],
            [P("You kneel and rub it into her back, slow. She unhooks her bra with one hand without lifting her head, so you can do all of it, and the straps fall loose on the grass."),
             P("Two guys walking past slow right down. Zoe waves at them without looking up."), D(Z, "Don't stop. Let them look."),
             P("Your hands slide down her sides, and she lifts off the grass enough that your fingers brush the sides of her bare tits. Your face is hot, and you're wet."),
             D(Z, "That's enough for out here, babe. Later."), P("She hooks her bra back up without looking, grinning at the grass.")], ["zoe_sunscreen_done"]),
           ("\"Do it yourself.\"", [], [],
            [D(Z, "I literally can't reach."), P("She tries anyway, and gets most of it on her elbow.")], [])],
          P("She sunbathes here when it's warm."))
_remember("hub_zoe_quad", "zoe_sunscreen_done", D(Z, "No burn. You've got magic hands."), lo=12, hi=96)

# Jake: he wants a girlfriend he can show off (npc_jake.md)
out_scene("ev_jake_photo", "The team photo", "quad", J, S([0, 2, 4], "08:30", "11:30"), [],
          [P("Jake's at the edge of the team on the grass, holding his phone up at you."),
           GC(cond(flag("jake_photo_taken", False)), D(J, "Photo. For the team chat. They think I made you up.")),
           GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), D(J, "Another one. The last one's still the best thing in the team chat."))],
          [("Smile for it.", [], [],
            [P("You lean in beside him and smile. He takes about twenty."),
             GC(cond(trait("jake_step", "gte", 3)), D(J, "Perfect. Look at that. That's my girl.")),
             GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), D(J, "Perfect. Look at that. They'll lose their minds.")),
             P("The guys behind him whistle.")], ["jake_photo_taken"]),
           ("Sit on his knee for it.", [DARING], [her("exhibitionism", 39)],
            [P("You sit on his knee, and his arm goes round your waist, and his hand rests on your hip where everyone can see it. The guys go loud."),
             D(J, "Oh, that's the one. That's going everywhere."), P("Your face is hot, and you don't get up straight away.")], ["jake_photo_taken"]),
           ("\"No photos, Jake.\"", [], [],
            [D(J, "Come on. One."), ME("No."), GC(cond(flag("jake_photo_taken", False)), D(J, "Fine. They'll keep thinking I made you up.")), GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), D(J, "Fine. The last one'll have to do.")), P("He puts the phone away, sulking a little.")], [])],
          P("The team's here three mornings a week."))
_remember("hub_jake_quad", "jake_photo_taken", D(J, "That photo's the best thing in the team chat. Ever."), lo=6, hi=72)

out_scene("ev_jake_mum", "His mum", "canteen", J, LUNCH, [],
          [P("Jake's at the end of the table on the phone, one finger in his other ear."),
           D(J, "Yes, Mum. Yes. I'm eating. There's a girl, yeah."),
           P("He sees you and goes red, and he doesn't hang up.")],
          [("Sit down next to him.", [], [],
            [P("You sit down right beside him. He puts the phone on speaker without asking."), D(J, "Mum, say hi. She's here."),
             P("His mum says hi so warmly that you both go red."), ME("Hi, Mrs. Jake's mum.")], ["jake_mum_met"]),
           ("Sit across from him.", [], [],
            [P("You sit across from him and eat your lunch while he tries to hang up for five minutes."), D(J, "Bye, Mum. Love you. Bye."),
             D(J, "Sorry. She wants to meet you."), ME("Already?")], []),
           ("Leave him to it.", [], [],
            [P("You leave him to it. He's still on the phone when you go, telling his mum you're shy.")], [], "campus")],
          P("His mum calls at lunch most days."))
_remember("hub_jake_canteen", "jake_mum_met", D(J, "My mum hasn't stopped talking about you. She wants to meet you. One day."), lo=12, hi=168)

out_scene("ev_jake_knee", "His knee", "quad", J, S([0, 2, 4], "08:30", "11:30"), [],
          [P("Jake's sitting out at the edge of the grass with an ice pack strapped round his knee, scowling at the team."),
           D(J, "Coach benched me. One bad landing.")],
          [("Sit with him.", [], [],
            [P("You sit with him and hold the ice pack while he complains about the coach. He leans his head on your shoulder after a while."),
             D(J, "This is the best I've felt all morning. When this knee's better, I'm taking you out. Properly.")], ["jake_knee_kept"]),
           ("\"You'll live.\"", [], [],
            [D(J, "Harsh."), P("He scowls, but then he laughs, and he looks a bit less sorry for himself.")], []),
           ("Leave him to sulk.", [], [],
            [P("You leave him to sulk. He shouts after you that he's injured.")], [], "campus")],
          P("The team's here three mornings a week."))
_remember("hub_jake_quad", "jake_knee_kept", D(J, "Knee's fine. I'm telling coach you're the reason."), lo=12, hi=96)

# Nadia: she knows things
out_scene("ev_nadia_notes", "Her notes", "library", N, S([0, 1, 2, 4], "14:30", "17:45"), [],
          [P("Nadia slides her notebook across the desk to you without looking up."),
           D(N, "Psychology. In case you missed anything. You usually do.")],
          [("Copy them.", [], [add("grade_psych", 1, cap=69)],
            [P("You copy them out while she reads. They're better than the lecture."),
             G(cond(flag("hale_met")), P("In the margin she's drawn Hale with horns."), D(N, "Don't copy the horns.")),
             D(N, "Same deal next week. You buy the tea.")], ["nadia_notes_shared"]),
           ("Quiz her on them instead.", [], [add("grade_psych", 1, cap=69)],
            [P("You quiz her. She gets every one, then quizzes you back, and you get most. She looks pleased with you in a way that's almost a smile.")], ["nadia_notes_shared"]),
           ("\"I'll be fine.\"", [], [],
            [D(N, "You won't. But fine."), P("She takes the notebook back, but she leaves it open on the desk where you can see it.")], [])],
          P("She studies here most afternoons."))
_remember("hub_nadia_library", "nadia_notes_shared", D(N, "This week's notes are in my bag. Same deal."), lo=12, hi=168)

out_scene("ev_nadia_essay", "Her essay", "canteen", N, LUNCH, [],
          [P("Nadia has her laptop open on the lunch table and her head in her hands."),
           D(N, "Two thousand words. Due tomorrow. I've got four hundred, and two of them are my name.")],
          [("Help her with it.", [], [],
            [P("You talk it through with her over lunch, and halfway through she starts typing fast and doesn't stop."),
             D(N, "Okay. Okay. I can do this. I owe you."), ME("You owe me a tea.")], ["nadia_owes_her"]),
           ("\"You always do this.\"", [], [],
            [D(N, "I know. I always finish, too."), P("She cracks her knuckles and starts typing.")], []),
           ("Leave her to panic.", [], [],
            [P("You leave her to it. She doesn't notice you go.")], [], "campus")],
          P("She leaves every essay to the last day."))
_remember("hub_nadia_library", "nadia_owes_her", D(N, "I got a B plus. I owe you a tea. Don't let me forget."), lo=48, hi=168)

# MIXED by her stage: the guy two desks over (in a skirt she can let him look)
LIB_SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
out_scene("ev_nadia_watcher", "Two desks over", "library", N, S([0, 1, 2, 4], "14:30", "17:45"), [LIB_SKIRT],
          [P("Nadia leans over without taking her eyes off her book."),
           D(N, "Don't look. The guy two desks over has been staring at your legs for ten minutes."),
           P("You don't look. You can feel it anyway, on the backs of your bare thighs under the skirt.")],
          [("Tug your skirt down.", [], [],
            [P("You tug your skirt down as far as it goes. Nadia nods, approving."), D(N, "Men. Honestly.")], []),
           ("Cross your legs, slow.", [DARING], [her("exhibitionism", 39)],
            [P("You cross your legs, slow, so the hem rides up another inch. Two desks over a chair creaks."),
             P("Nadia's eyebrows go up behind her glasses."), D(N, "You did that on purpose."), ME("Did what?")], ["nadia_saw_legs"]),
           ("Ignore it.", [], [],
            [P("You go back to your reading. Nadia keeps glaring at him over her book until he leaves.")], [])],
          P("She notices everything in here."))
_remember("hub_nadia_library", "nadia_saw_legs", D(N, "Your fan came back today. Asked if you were coming in."), lo=20, hi=168)

# Tom: strict this release; his Power is his say over her shifts
CAFE = S([0, 1, 2, 3, 4, 5], "08:30", "21:45")
out_scene("ev_tom_machine", "The machine", "cafe", T_, CAFE, [],
          [P("The espresso machine hisses and dies. Tom hits it with the flat of his hand. It doesn't come back."),
           D(T_, "Not today. Not with a queue.")],
          [("Jiggle the steam valve.", [], [his(T_, "power", -1)],
            [P("You reach past him and jiggle the steam valve, on a hunch. The machine coughs and comes back."),
             P("Tom looks at you for a long second."), D(T_, "Fine. You can stay.")], ["tom_machine_fixed"]),
           ("\"Want me to take the queue?\"", [], [his(T_, "power", 1)],
            [D(T_, "Smile at them. Tell them five minutes."), P("You smile at the queue. He swears at the machine. Somehow it works.")], []),
           ("Keep out of his way.", [], [],
            [P("You keep well out of his way. He fixes it himself in ten minutes, and he's in a mood the whole time you're there.")], [])],
          P("That machine breaks most weeks."), sub_host="cafe_coffee", entry=[his(T_, "want", 1)])
_remember("hub_tom_cafe", "tom_machine_fixed", D(T_, "You and that steam valve. Don't let it go to your head."), lo=12, hi=168)

out_scene("ev_tom_sister", "His sister", "cafe", T_, CAFE, [],
          [P("Tom's in the back doorway with his phone, his voice low and tight."),
           D(T_, "I can't, Jen. I'm on my own here till close."),
           P("He sees you, covers the phone and looks at the counter, then at you.")],
          [("\"Go. I'll watch the counter.\"", [], [his(T_, "power", -1), add("money", 5, clamp=False)],
            [P("He's gone ten minutes. You sell two coffees and a muffin and nobody steals anything. When he comes back he puts a five on the counter."),
             D(T_, "For the ten minutes. Don't tell anyone I'm soft.")], ["tom_owes_her"]),
           ("Pretend you didn't hear.", [], [],
            [P("You look at the menu board very hard. He finishes the call and comes back out, jaw tight, and doesn't say anything.")], [])],
          P("His sister calls him at work. He always answers."), sub_host="cafe_coffee", entry=[his(T_, "want", 1)])
_remember("hub_tom_cafe", "tom_owes_her", D(T_, "Jen says thanks. So. Thanks."), lo=12, hi=168)

out_scene("ev_tom_pastries", "The leftovers", "cafe", T_, S([0, 1, 2, 3, 4, 5], "22:00", "22:45"), [],
          [P("The café's shut, the sign turned. Tom's boxing up what didn't sell and holds the box out to you."),
           D(T_, "Take these, or they go in the bin.")],
          [("Take them.", [], [],
            [P("You take the box. There's a cinnamon roll on top, the good one."), D(T_, "Don't say I never give you anything.")], ["tom_gave_pastries"]),
           ("\"I'm good, thanks.\"", [], [],
            [D(T_, "Suit yourself."), P("He tips the box into the bin without ceremony, but he saves the cinnamon roll and eats it himself.")], []),
           ("\"Give them to Gary.\"", [flag("gary_met")], [],
            [D(T_, "Gary doesn't need help eating."), P("He doesn't smile, but it's close. He puts the box on the counter for whoever wants it.")], [])],
          P("He boxes up the leftovers every night at close."), sub_host="cafe_coffee", entry=[his(T_, "want", 1)])
_remember("hub_tom_cafe", "tom_gave_pastries", D(T_, "Cinnamon rolls again tonight, if you're around at close."), lo=10, hi=48)

# ═════════════════════════════════════════════════════════════════════════════
# Readers for records nothing read (14_random_scenes_ours.md): the day after, his hub remembers.
# ═════════════════════════════════════════════════════════════════════════════
_remember("hub_ryan_kitchen", "ryan_saw_her_towel", P("Ryan doesn't look up from his plate at you once, and his ears are red the whole meal."))
_remember("hub_ryan_room", "ryan_walked_in_shower", D(R, "Lock the bathroom, @player.nickname. I mean it. Or don't."))
_remember("hub_ryan_room", "ryan_brushed_kitchen", D(R, "About the kitchen. That was an accident. Mostly."))
_remember("hub_ryan_living_room", "ryan_caught_ch5", D(R, "I'm checking what channel it's on before I sit down. Every time now."))
_remember("hub_mark_kitchen", "mark_brushed_reach", D(M, "You're always in front of the coffee, @player."))
_remember("hub_mark_kitchen", "mark_brushed_kitchen", D(M, "Coffee's on. I'll get my own cup this time."))
_remember("hub_mark_garage", "mark_walked_in_laundry", D(M, "I'll knock next time you're at the machine. Maybe."))
_remember("hub_mark_garage", "mark_walked_in_shower", D(M, "That lock needs fixing. I've been meaning to."))
_remember("hub_laura_kitchen", "laura_saw_ch5", D(L, "We're not going to talk about the TV, are we. Good."))


def attach_subs(canvases):
    """Put the everyday walk-in rules on their hosts (hosts not here are skipped)."""
    for c in canvases:
        for r in SUB_RULES.get(c.get("id"), []):
            c["trigger"].setdefault("substitutions", []).append(r)


def hub_read(canvases):
    """Put each hub's remember lines at the end of its first screen (hubs not here are skipped)."""
    for c in canvases:
        for blk in HUB_READS.get(c.get("id"), []):
            c["nodes"][0]["blocks"].append(blk)


if __name__ == "__main__":
    text = ("# =============================================================================\n"
            "# First Term — 5 · scenes · EVERYDAY AT HOME, batch 1 (everyday.py; DECISIONS 221)\n"
            "# =============================================================================\n")
    text += "".join(emit(c) for c in out)
    open(sys.argv[1], "w").write(text)
    print("everyday:", len(out), "canvases;", len(DAILY_FLAGS), "daily flags;", len(COUNTERS), "chain counters")
