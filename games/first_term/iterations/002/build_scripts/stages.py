"""A new stage is a moment (sheets/systems/meters.md Rule 7, DECISIONS 229; signed by LO 2026-11-11, "Sign them").

The model is Cupid's Way: one pop-up per stage, its name, two or three lines of who she has become, and what opens
(cupids-way.txt:19980-20010), fired on the morning check. Here: the first night after she crosses 20, 40 or 60, going
to bed plays this canvas in place of room_sleep (a substitution on it, like Ryan's step 5), and its morning screen is
the moment. It sleeps her exactly as room_sleep does and pays nothing more. 80 is the next release.
Her room is the wardrobe room, so nothing one-time may fire there on entry (gate `nothing one-time at the shop or
wardrobe`); a substitution_only target never does.
"""
from canv import *
from tomlw import tod

out = []
LATE_CLEAR = [funset(f) for f in ("came_home_late", "late_party", "late_shift", "late_date")]   # as home.py room_sleep
SLEEP_EFF = [setv("energy", 100)]
BUCKETS = [("19:00", "20:00", 690), ("20:00", "21:00", 630), ("21:00", "22:00", 570), ("22:00", "23:00", 510),
           ("23:00", "00:00", 450), ("00:00", "01:00", 390), ("01:00", "02:00", 330), ("02:00", "03:00", 270),
           ("03:00", "04:00", 210), ("04:00", "05:00", 150), ("05:00", "06:00", 90), ("06:00", "07:00", 30)]
BED_HOURS = [{"weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "19:00", "end_time": "07:00"}]   # room_sleep's window
IDS = []   # home.py puts these on room_sleep's substitutions, in this order

STAGES = [
    ("corruption", 20, "Curious",
     "You wake up thinking about it again: the couple in the park, a door left open at night. You used to look away. "
     "This morning you don't want to.",
     "Watching, touching yourself, a kiss, a dare."),
    ("corruption", 40, "Bold",
     "You lie with your hand flat on your stomach and you know it now. You'd let a hand stay. You'd put your mouth "
     "where you were asked to.",
     "Hands, mouths, a price for a look."),
    ("corruption", 60, "Hungry",
     "You wake up wet, and it isn't a dream. It's this house: your brother across the hall, Mark at the table "
     "downstairs. You want what you aren't allowed, and you want someone to see you take it.",
     "The taboo at home, strangers who can see, a room watching."),
    ("exhibitionism", 20, "Daring",
     "You pull on a top and leave the bra on the chair. Nobody told you to. You liked how they looked yesterday, and "
     "you want it again.",
     "No bra, a short skirt out of the house, bigger tips at the café."),
    ("exhibitionism", 40, "Showing",
     # her clothes are backed: the panties line only while she wears them (she sleeps in them, but a night can strip her)
     [G(cond({"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}),
        P("You stand at the mirror in your panties longer than you need to, and think about who you'd let see this. "
          "Then you think about taking the panties off too.")),
      G(cond({"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}),
        P("You stand at the mirror with nothing on, longer than you need to, and think about who you'd let see this. "
          "Then you think about letting them."))],
     "No panties out, naked for someone you know, your feed."),
    ("exhibitionism", 60, "Watched",
     "Being seen isn't enough now. You want to be watched: a room going quiet, a stranger who can't look away, and "
     "you not covering up.",
     "A room watching, a stranger."),
]

BED_LINE = {
    "Curious": "You get under the covers and lie in the dark with your eyes open, replaying what you saw today.",
    "Bold": "You get under the covers with your skin still buzzing, and you don't try to make it stop.",
    "Hungry": "You lie in the dark and listen to the house, every door in it, and you know who is behind each one.",
    "Daring": "You get into bed still feeling their eyes on you, warm, and you fall asleep smiling.",
    "Showing": "You kick the duvet off and lie on top of it in the warm dark, and you like being bare to the room.",
    "Watched": "You lie awake a long time, thinking about the faces that turned today, and how quiet they went.",
}

for meter, at, name, moment, opens in STAGES:
    cid = f"stage_{meter}_{at}"
    IDS.append(cid)
    seen = f"{cid}_seen"
    out.append({
        "id": cid, "name": "Go to bed",
        "description": f"Her {meter.capitalize()} reaches {at} ({name}): the next night's sleep, whose morning is one "
                       f"screen of who she is now and what opens (meters.md Rule 7). Sleeps her as room_sleep does.",
        "trigger": {"location": "home_ella_room", "is_repeatable": False, "priority": 1, "is_active": True,
                    "substitution_only": True, "schedules": BED_HOURS,
                    "conditions": cond(flag("opening_done"), trait(meter, "gte", at), flag(seen, False))},
        "nodes": [
            node("bed", "Your bed", [P(BED_LINE[name])],
                 [go("Sleep till morning.", node="wake", mins=m, cond_=cond(tod(a, b)), eff=SLEEP_EFF, flags=LATE_CLEAR)
                  for a, b, m in BUCKETS] + [go("Not yet. Get up.", loc="home_hall")]),
            node("wake", name, (moment if isinstance(moment, list) else [P(moment)])
                 + [P(f"New for you now: {opens}", not_speech=True)],
                 [go("Get up.", loc="home_ella_room", cond_=cond(flag("heavy_night", False)), flags=[fset(seen)]),
                  go("Get up, slowly.", loc="home_ella_room", cond_=cond(flag("heavy_night")),
                     eff=[add("energy", -30) | {"clamp": True}], flags=[funset("heavy_night"), fset(seen)])]),
        ],
    })

if __name__ == "__main__":
    text = ("# =============================================================================\n"
            "# First Term — 5 · scenes · HER STAGES (sheets/systems/meters.md Rule 7, DECISIONS 229)\n"
            "# One morning moment in her room per stage she crosses.\n"
            "# =============================================================================\n")
    text += "".join(emit(c) for c in out)
    open(__import__("sys").argv[1], "w").write(text)
    print("stages:", len(out), "canvases")
