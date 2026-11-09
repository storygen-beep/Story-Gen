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
from home_items import CURIOUS, BOLD, here, since

R, L, M = "npc_ryan", "npc_laura", "npc_mark"
K, LR, HALL, GAR = "home_kitchen", "home_living_room", "home_hall", "home_garage"
BRAKE = "everyday_home_today"
DAILY_FLAGS = [BRAKE]       # every flag here that [engine.daily_tick] clears (0_systems_spec.toml)
COUNTERS = []               # every chain counter (hidden player traits, gen_world.py + 0_systems_spec.toml)
HUB_READS = {}              # hub id -> [group blocks]: the day after, his hub remembers
out = []


def S(days, a, b):
    return [{"weekdays": list(days), "start_time": a, "end_time": b}]


def _remember(hub, rec, *blocks, lo=6, hi=30):
    """His hub remembers `rec` from `lo` hours after it was set (never the same visit; the scene's exit is his
    room) until `hi`. `rec` is the answer's own flag, so a line about the yes never follows the no (scene reader
    2026-11-10)."""
    HUB_READS.setdefault(hub, []).append(G(cond(flag(rec), since(rec, "gte", lo), since(rec, "lt", hi)), *blocks))


def scene(cid, name, loc, who, sched, conds, lead, answers, hook, chance=0.3, plain=True, bound=True, rest=None):
    """One everyday or mixed scene. answers: [(label, cond_items, eff, reply_blocks, extra_flags[, back])].
    The answer screen's exit returns to the room (or `back`); the record flag `cid` rides every answer. A band
    that a meter decides is split into separate answers with their own conditions, because the answer's raise
    lands before its screen is read (scene reader 2026-11-10)."""
    today = f"{cid}_today"
    DAILY_FLAGS.append(today)
    items = [flag("opening_done"), flag(today, False)] + ([flag(BRAKE, False)] if plain else []) \
        + ([flag(rest, False)] if rest else []) + list(conds)
    trig = {"location": loc, "is_repeatable": True, "priority": 3, "is_active": True,
            "trigger_mode": "random", "chance": chance, "seen_weight": 0.4,
            "schedules": sched, "conditions": cond(*items)}
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
