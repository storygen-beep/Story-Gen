"""The phone (8_phone.toml), iteration 002 part 6: the seven threads message by message, the selfie on
Exhibitionism, the feed behind its flags. The calls (Laura's curfew call, the dean's office) are kept
verbatim in phone_calls.toml (fixed in parts 3 and 4) and appended.

Sources: each person sheet's "Phone thread" row and "Messages, per reply" table (LO's note, 2026-10-08:
each follow-up waits for her reply with `after_round`, one answer per reply with `after_choice`; `round`
on a message does nothing, the-phone.md P3); wardrobe.md "On the phone" (the selfie rungs, LO Q66); the
feed row (a party post only after `party_went`).
Usage: python3 phone.py <path to 8_phone.toml>
"""
import os
import sys
from tomlw import q, v

HERE = os.path.dirname(os.path.abspath(__file__))
L = []
w = L.append


def npc_eff(npc, trait, n):
    d = {"targetType": "npc", "npcId": npc, "trait": trait, "op": "add", "value": n, "clamp": True}
    if n < 0:
        d["clamp"] = True   # a phone effect is unclamped by default (v2.py applyPhoneEffectSet); a cost stops at 0
    return d


def setf(f):
    return {"targetType": "player", "flag": f, "op": "set"}


def trigger(*items):
    w("[phone.conversations.trigger]")
    w("conditions = { version = \"1.0\", logic = \"AND\", items = [")
    for it in items:
        w(f"  {v(it)},")
    w("] }")


def F(f, on=True):
    return {"type": "flag", "subject": "player", "flag_key": f, "operator": "is_true" if on else "is_false"}


def SINCE(f, days):
    return {"type": "days_since_flag", "subject": "player", "flag_key": f, "operator": "gte", "value": days}


def DAYS(*d):
    return {"type": "weekday", "weekdays": list(d)}


def HOURS(a, b):
    return {"type": "time_of_day", "start_time": a, "end_time": b}


def SINCE_H(f, hours):
    return {"type": "hours_since_flag", "subject": "player", "flag_key": f, "operator": "gte", "value": hours}


def unsetf(f):
    return {"targetType": "player", "flag": f, "op": "unset"}


def TRAIT_GTE(t, n):
    return {"type": "trait", "subject": "player", "trait_key": t, "operator": "gte", "value": n}


# LO, 2026-11-04 (Q5): a no-show, or an invite left unanswered, pushes that person's next invite back a few days,
# and they say so in a text. The wait is a hidden patience meter: full at ZOE_WAIT / JAKE_WAIT, emptied by the
# no-show or the ignore, one back each midnight ([engine.daily_tick] in 0_systems_spec.toml); an invite waits for
# it to be full. Zoe asks once a week (Thursday, Friday), so hers is 6 days and skips the next ask; Jake asks twice
# (Mon/Tue, Thu/Fri), so his 3 days skip the next one.
ZOE_WAIT, JAKE_WAIT = 6, 3


def pl_eff(trait, n):
    d = {"targetType": "player", "trait": trait, "op": "add", "value": n, "clamp": True}
    if n < 0:
        d["clamp"] = True
    return d


def noshow(cid, npc, notify, key, hours, opener, replies, cost, extra=(), comment=None):
    """She said yes and never came (DECISIONS 87). Arrives once `key` is still set `hours` after the yes;
    every reply, and ignoring it for a day, applies `cost` once and clears the booking. Showing up clears
    the booking first (canv.clear_on_leave / booked_split), so this never arrives after she came."""
    done = {"effects": list(cost.get("effects", [])), "flagEffects": list(cost.get("flagEffects", [])) + [unsetf(key)]}
    thread(cid, npc, notify, [F(key), SINCE_H(key, hours), *extra], opener,
           [(t, done, a) for t, a in replies], repeat=1, ignore=(1, done), comment=comment)


def thread(cid, npc, notify, trig, opener, replies, repeat=None, comment=None, round2=None, ignore=None):
    """opener: the messages before she answers. replies: [(her text, {effects/flagEffects}, his answer)].
    round2: (after_choice index in round 1, [(her text, extras, his answer)]).
    ignore: (days, {effects/flagEffects}): no reply that many days after it arrived applies the set once
    (the engine's on_ignore, E3b). Ignoring costs more than a no (CoT, round9a cot_phone.md §1)."""
    w("")
    if comment:
        w(f"# ── {comment} ──")
    w("[[phone.conversations]]")
    w(f"id     = {q(cid)}")
    w('app    = "messages"')
    w(f"npc    = {q(npc)}")
    w(f"notify = {q(notify)}")
    if repeat:
        w(f"repeat_after_days = {repeat}")
    if ignore:
        w(f"ignore_after_days = {ignore[0]}")
        w(f"on_ignore = {v(ignore[1])}")
    trigger(*trig)
    for m in opener:
        w("[[phone.conversations.blocks]]")
        w('type = "message"')
        w('sender = "npc"')
        w(f"content = {q(m)}")
    w("[[phone.conversations.blocks]]")
    w('type = "reply"')
    w("round = 1")
    w("choices = [")
    for text, extras, _ in replies:
        w(f"  {v(dict({'text': text}, **extras))},")
    w("]")
    for i, (_, _, answer) in enumerate(replies):
        if not answer:
            continue
        w("[[phone.conversations.blocks]]")
        w('type = "message"')
        w('sender = "npc"')
        w("after_round = 1")
        w(f"after_choice = {i}")
        w(f"content = {q(answer)}")
    if round2:
        on_choice, r2 = round2
        w("[[phone.conversations.blocks]]")
        w('type = "reply"')
        w("round = 2")
        w("after_round = 1")
        w(f"after_choice = {on_choice}")
        w("choices = [")
        for text, extras, _ in r2:
            w(f"  {v(dict({'text': text}, **extras))},")
        w("]")
        for i, (_, _, answer) in enumerate(r2):
            w("[[phone.conversations.blocks]]")
            w('type = "message"')
            w('sender = "npc"')
            w("after_round = 2")
            w(f"after_choice = {i}")
            w(f"content = {q(answer)}")


w('''# =============================================================================
# First Term — 8 · the phone (a channel, not a system: the-phone.md)
#
# Generated by iterations/002/build_scripts/phone.py (iteration 002, part 6). Never hand-edit:
# edit phone.py (the threads, the feed) or phone_calls.toml (the calls).
#
# One thread per person she is involved with (each person sheet's "Phone thread" row): Ryan, Laura,
# Mark, Tom, Zoe, Dr. Hale (his college email), Jake. Every text is caused by a flag a scene sets,
# with a delay and an hour window (P4). Each follow-up waits for her reply (after_round) and answers
# only the reply she sent (after_choice).
# =============================================================================

[phone]
enabled = true

[[phone.apps]]
id    = "messages"
type  = "chat"
label = "Messages"

# The selfie lives on the phone only (wardrobe.md "On the phone", LO Q66): three rungs on Exhibitionism
# (Covered 0, Daring 20, Showing 40), each label naming the act; a post moves only `followers`; once a
# day each (the engine's daily cap). The engine reads only one meter for a post, not her clothes.
[[phone.apps]]
id    = "feed"
type  = "social_feed"
label = "Feed"
release = 2   # DECISIONS 236 (LO, 2026-11-12): release 1 has Messages only; followers start next release
post_actions = [
  { label = "Post a selfie", followers_min = 3, followers_max = 8, counter_trait = "followers", daily_cap = 1 },
  { label = "Post one in your bra", followers_min = 10, followers_max = 25, counter_trait = "followers", daily_cap = 1, corruption_min = 20, gate_trait = "exhibitionism" },
  { label = "Post one topless", followers_min = 40, followers_max = 90, counter_trait = "followers", daily_cap = 1, corruption_min = 40, gate_trait = "exhibitionism" },
]

# ── the feed looks back at her, each post behind the flag that makes it true (wardrobe.md feed row) ──
# A party post only after she has been to Zoe's Friday party (`party_went`: party_arrive, Zoe A 1).
[[phone.posts]]
id          = "feed_party_tag"
app         = "feed"
poster_name = "@campus_nights"
caption     = "friday at zoe's. who's the new girl 👀"
likes       = 212
image       = "phone/feed_party_tag.jpg"
search_queries = ["college house party crowd phone photo"]
[phone.posts.trigger]
conditions = { version = "1.0", logic = "AND", items = [ { type = "flag", subject = "player", flag_key = "party_went", operator = "is_true" }, { type = "trait", subject = "player", trait_key = "campus_talk", operator = "gte", value = 10 } ] }

# gossip (DECISIONS 207): the feed says what campus says, one post a level, each behind the flag that makes it true
# (CoT's six reputation posts on its feed, cot_20:6311-6350). No DECISIONS 41 words from strangers.
[[phone.posts]]
id          = "feed_talk_named"
app         = "feed"
poster_name = "@quad_watch"
caption     = "lecture hall got a show again 👀 row behind the new girl, you know what you saw"
likes       = 388
image       = "phone/feed_talk_named.jpg"
search_queries = ["college lecture hall students phone photo from behind"]
[phone.posts.trigger]
conditions = { version = "1.0", logic = "AND", items = [ { type = "flag", subject = "player", flag_key = "talk_class", operator = "is_true" }, { type = "trait", subject = "player", trait_key = "campus_talk", operator = "gte", value = 25 } ] }

[[phone.posts]]
id          = "feed_talk_slut"
app         = "feed"
poster_name = "@quad_watch"
caption     = "everybody's heard about the new girl by now. slut or legend? comments open 🔥"
likes       = 612
image       = "phone/feed_talk_slut.jpg"
search_queries = ["college campus girl walking phone photo candid"]
[phone.posts.trigger]
conditions = { version = "1.0", logic = "AND", items = [ { type = "trait", subject = "player", trait_key = "campus_talk", operator = "gte", value = 40 } ] }

[[phone.posts]]
id          = "feed_talk_rate"
app         = "feed"
poster_name = "@campus_nights"
caption     = "friday at zoe's: guess who took the dare again. rate her 1-10 👇"
likes       = 905
image       = "phone/feed_talk_rate.jpg"
search_queries = ["house party kitchen crowd cheering phone photo"]
[phone.posts.trigger]
conditions = { version = "1.0", logic = "AND", items = [ { type = "flag", subject = "player", flag_key = "talk_party", operator = "is_true" }, { type = "trait", subject = "player", trait_key = "zoe_dares_done", operator = "gte", value = 1 }, { type = "trait", subject = "player", trait_key = "campus_talk", operator = "gte", value = 60 } ] }

# Followers come only from her own posts, so a mirror pic exists once there are twenty of them.
[[phone.posts]]
id          = "feed_followers_dm"
app         = "feed"
poster_name = "@quad_watch"
caption     = "mirror pic of the week. that ass, those legs. you know who you are 🔥 dm us the rest"
likes       = 340
image       = "phone/feed_followers_dm.jpg"
search_queries = ["girl mirror selfie bedroom phone"]
[phone.posts.trigger]
conditions = { version = "1.0", logic = "AND", items = [ { type = "trait", subject = "player", trait_key = "followers", operator = "gte", value = 20 } ] }''')

R, LA, M, T, Z, H, J = "npc_ryan", "npc_laura", "npc_mark", "npc_tom", "npc_zoe", "npc_hale", "npc_jake"

# ── 1 · Ryan (npc_ryan.md: knows_about_kayla, a day later, 21:00-23:00). A day or more after the
# bathroom, so never "this morning". ──
thread("ryan_kayla", R, "📱 Ryan", [F("knows_about_kayla"), SINCE("knows_about_kayla", 1), HOURS("21:00", "23:00")],
       ["about the phone thing", "don't tell mom"],
       [("your secret's safe", {"effects": [npc_eff(R, "warmth", 2)]}, "owe you one. two knocks?"),
        ("what's it worth?", {"effects": [npc_eff(R, "want", 1)]}, "come find out. two knocks"),
        ("who's kayla?", {}, "friday. you'll hear her")],
       # (pass 3 F60) leaving him on read after he trusted her with it costs more than any answer
       ignore=(1, {"effects": [npc_eff(R, "warmth", -1)]}),
       comment="Ryan: caused by knows_about_kayla (his step 2)")
# his repeat after step 8: every 2 days, 22:00-00:00, not Friday (Kayla's night); he's in his room, awake
thread("ryan_two_knocks_text", R, "📱 Ryan",
       [F("ryan_08_done"), SINCE("ryan_08_done", 1), DAYS(0, 1, 2, 3, 5, 6), HOURS("22:00", "00:00")],
       ["you still up?", "two knocks. door's open."],
       [("coming", {"effects": [npc_eff(R, "warmth", 1)], "flagEffects": [setf("ryan_knock_booked")]}, None),
        ("not tonight", {}, None)],
       repeat=2, ignore=(1, {"effects": [npc_eff(R, "warmth", -1)]}),
       comment="Ryan's repeat invite, after his step 8 (the door this release ends on)")
noshow("ryan_knock_noshow", R, "📱 Ryan", "ryan_knock_booked", 3,
       ["you said coming.", "door was open all night."],
       [("fell asleep. sorry", "sure. sleep tight then."), ("tomorrow. promise", "we'll see about that.")],
       {"effects": [npc_eff(R, "warmth", -2)]}, extra=[HOURS("00:30", "04:00")],
       comment="Ryan: she said coming and never knocked (DECISIONS 87)")

# ── 2 · Laura (npc_laura.md: laura_01_done, a day later; the days she cooks, 16:00-17:30, so "six"
# is still ahead; every 7 days) ──
thread("laura_dinner", LA, "📱 Mom",
       [F("laura_01_done"), SINCE("laura_01_done", 1), DAYS(0, 1, 3, 4, 6), HOURS("16:00", "17:30")],
       ["home for dinner sweetheart?"],
       [("yes, starving", {"effects": [npc_eff(LA, "warmth", 1)], "flagEffects": [setf("dinner_promised")]},
         "six. kitchen. don't be late"),
        ("eating out tonight", {"flagEffects": [setf("said_eating_out")]}, "ok. text me when you're coming"),
        ("is mark cooking?", {}, "god no. it's me")],
       repeat=7, ignore=(1, {"effects": [npc_eff(LA, "warmth", -1)]}),
       comment="Laura: caused by laura_01_done (the blue dress). The yes books dinner (laura.py DINNER_DONE).")
# Dinner runs 18:00-20:00; the yes comes 16:00-17:30, so 4 hours after it dinner is over.
noshow("laura_dinner_noshow", LA, "📱 Mom", "dinner_promised", 4,
       ["i kept you a plate.", "you said six."],
       [("sorry. lost track of time", "it's in the fridge."), ("something came up", "it always does.")],
       {"effects": [npc_eff(LA, "warmth", -2), pl_eff("laura_suspicion", 2)]}, extra=[HOURS("20:00", "23:00")],
       comment="Laura: she said yes to dinner and never sat down (DECISIONS 87)")

# ── 3 · Mark (npc_mark.md: rent_starts, five days on: Saturday 18:00-21:00, the night before each count;
# every 7 days) ──
thread("mark_rent", M, "📱 Mark",
       [F("rent_starts"), SINCE("rent_starts", 5), DAYS(5), HOURS("18:00", "21:00")],
       ["rent. tomorrow. kitchen."],   # pass 4 F75: no hand-typed price; the engine re-prices to 90 and 100 (settings.rent stages)
       [("i'll have it", {}, "good."),
        ("i might be short", {"effects": [npc_eff(M, "want", 1)]}, "then we talk tomorrow."),
        ("what if i'm not", {}, "you will be. kitchen. eight.")],
       # (pass 3 F60) no answer to the man she owes: his Dominance +1, so his terms come sooner at the table
       repeat=6, ignore=(1, {"effects": [{"targetType": "npc", "npcId": M, "trait": "power", "op": "add", "value": 1, "cap": 100}]}),
       comment="Mark: caused by rent_starts (breakfast, day 1); Saturday, every week")

# ── 4 · Tom (npc_tom.md: cafe_job, a day later, 10:00-14:00; no clock time: "after class") ──
thread("tom_shift", T, "📱 Tom",
       [F("cafe_job"), SINCE("cafe_job", 1), DAYS(0, 1, 2, 3, 4, 5), HOURS("10:00", "14:00")],
       ["shift after class?"],
       [("on my way after", {"flagEffects": [setf("tom_shift_booked")]}, "apron's on the hook."),
        ("not today", {}, "your loss. tips were good."),
        ("what's it pay", {}, "eight and tips. be on time.")],   # release 1: strict, and the right pay (tom_01_the_apron.md)
       ignore=(1, {"effects": [npc_eff(T, "want", -1)]}),
       comment="Tom: caused by cafe_job. The yes books today's first shift (cafe.py).")
# The last shift starts by 19:00; the yes comes 10:00-14:00, so 9 hours after it the day's shifts are gone.
noshow("tom_shift_noshow", T, "📱 Tom", "tom_shift_booked", 9,
       ["no show today? really?", "i covered your tables."],
       [("sorry, class ran late", "tell it to the tip jar."), ("something came up", "don't make it a habit.")],
       {"effects": [npc_eff(T, "want", -1)]}, extra=[HOURS("19:00", "23:00")],
       comment="Tom: she said on my way and never clocked in (DECISIONS 87)")
# (release 1: Tom's after-close loop waits with his step 6, a later release; tom_close and tom_close_noshow are not built)

# ── 5 · Zoe (npc_zoe.md: zoe_met. The party, Thursday 18:00-22:00; the run, Friday 18:00-22:00; weekly) ──
thread("zoe_party", Z, "📱 Zoe",
       [F("zoe_met"), SINCE("zoe_met", 1), TRAIT_GTE("zoe_patience", ZOE_WAIT), DAYS(3), HOURS("18:00", "22:00")],
       ["party tmrw. wear something short"],
       [("obviously", {"flagEffects": [setf("zoe_party_promised")]}, "that's my girl 😈"),
        ("what counts as short", {}, "come by tonight. i'll lend you one"),
        ("can't. my mom", {}, "sneak out. kidding. kinda")],
       repeat=6, ignore=(1, {"effects": [pl_eff("zoe_patience", -ZOE_WAIT)], "flagEffects": [setf("zoe_ignored")]}),
       comment="Zoe: the party (Thursday; she's home till midnight, so 'tonight' holds)")
# DECISIONS 210 (goals.py): Zoe's crowd. After her first party, at Daring; a no lets it come back in a week.
thread("zoe_crowd", Z, "📱 Zoe",
       [F("zoe_met"), F("party_went"), F("zoe_crowd_on", False), TRAIT_GTE("zoe_step", 1), TRAIT_GTE("exhibitionism", 20),
        SINCE("party_went", 2), HOURS("12:00", "22:00")],
       ["throwing a big one", "need bodies. bring me ten", "i'll make it worth it"],
       [("ten? easy", {"flagEffects": [setf("zoe_crowd_on")]}, "quad, gym, canteen. go get them 😈"),
        ("how do i get ten people", {"flagEffects": [setf("zoe_crowd_on")]}, "smile. show a little. you know how"),
        ("not my thing", {}, "it will be. ask me next week")],
       repeat=7, ignore=(2, {"effects": [pl_eff("zoe_patience", -ZOE_WAIT)], "flagEffects": [setf("zoe_ignored")]}),
       comment="Zoe: her crowd (DECISIONS 210). A yes sets zoe_crowd_on; the asks are in goals.py")
# (pass 3 F60, F61) a bail costs. Since Q5 (LO, 2026-11-04) it costs a few days, not every run: `zoe_bailed` only
# colours her park line (zoe.py hub_zoe_park), and the wait is her patience. Ignoring the text counts as a bail;
# "too early" costs nothing.
thread("zoe_run", Z, "📱 Zoe",
       [F("zoe_met"), SINCE("zoe_met", 2), TRAIT_GTE("zoe_patience", ZOE_WAIT), DAYS(4), HOURS("18:00", "22:00")],
       ["run tmrw? 8. the park"],
       [("i'm in", {"flagEffects": [setf("zoe_run_booked")]}, "wear the sports bra 😏"),
        ("too early", {}, "lazy. next week then")],
       repeat=6, ignore=(1, {"effects": [pl_eff("zoe_patience", -ZOE_WAIT)], "flagEffects": [setf("zoe_bailed"), setf("zoe_ignored")]}),
       comment="Zoe: the run (Friday; her park row is weekend mornings 08:00-10:00). The yes books it (zoe.py).")
# Saturday's run ends 10:00; the yes comes Friday 18:00-22:00, so 16 hours after it she ran alone.
# The cost is her patience (Q5): no invite from her for six days, and she says so; `zoe_bailed` is read by her next
# park line (zoe.py).
noshow("zoe_run_noshow", Z, "📱 Zoe", "zoe_run_booked", 16,
       ["you bailed on me 🙄", "i ran alone like a loser", "no invites for you this week"],
       [("sorry!! next week", "you're buying coffee."), ("overslept", "obviously. lazy bones.")],
       {"effects": [pl_eff("zoe_patience", -ZOE_WAIT)], "flagEffects": [setf("zoe_bailed")]}, extra=[HOURS("10:00", "20:00")],
       comment="Zoe: she said i'm in and never came to the park (DECISIONS 87)")

# ── 6 · Dr. Hale, his college email (npc_hale.md: hale_02_done, a day later, 09:00-17:00; whole sentences) ──
thread("hale_office_hours", H, "📧 College email: Dr. Hale",
       [F("hale_02_done"), SINCE("hale_02_done", 1), DAYS(0, 1, 2, 3, 4), HOURS("09:00", "17:00")],
       ["Thursday, six, my office. Bring the essay."],
       [("I'll be there.", {"flagEffects": [setf("hale_office_booked")]}, "Good. — H."),
        ("I can't this Thursday.", {}, "Then next Thursday. — H.")],
       ignore=(1, {"effects": [pl_eff("grade_psych", -1)]}),   # (pass 3 F60) an unanswered email from your lecturer is marked
       comment="Dr. Hale (his college email): caused by hale_02_done. The yes books step 3 (hale.py).")
# His step 3 is Thursday 18:00-19:30. On Friday, a day after the yes, a booking still open with the
# step not done means she never came.
noshow("hale_office_noshow", H, "📧 College email: Dr. Hale", "hale_office_booked", 24,
       ["I waited until half past seven."],
       [("I'm sorry. Something came up.", "Your essay grade reflects it. — H."),
        ("It won't happen again.", "See that it doesn't. — H.")],
       {"effects": [pl_eff("grade_psych", -2)]},
       extra=[DAYS(4), HOURS("09:00", "17:00"),
              {"type": "trait", "subject": "player", "trait_key": "hale_step", "operator": "eq", "value": 2}],
       comment="Hale: she said she'd come to office hours and didn't (DECISIONS 87)")
# LO, 2026-11-10 ("1 yes add it"; DECISIONS 219): after his step 4, the booked hour. The evening before a weekday
# that isn't Thursday he emails; her yes puts him in his office 10:00-12:00 the next morning (people_data latch 18 h).
thread("hale_office_text", H, "📧 College email: Dr. Hale",
       [F("hale_04_done"), SINCE("hale_04_done", 1), F("hale_booked", False), DAYS(6, 0, 1, 3), HOURS("19:00", "22:00")],
       ["Tomorrow, ten. My office.", "Lock the door behind you. — H."],
       [("I'll be there.", {"flagEffects": [setf("hale_booked")]}, "Good. — H."),
        ("I can't tomorrow.", {}, "Then office hours. — H.")],
       repeat=2, ignore=(1, {"effects": [pl_eff("grade_psych", -1)]}),   # an unanswered email from your lecturer is marked (as hale_office_hours)
       comment="Dr. Hale: the booked morning hour, after his step 4")
thread("hale_thursday", H, "📧 College email: Dr. Hale",
       [F("hale_04_done"), SINCE("hale_04_done", 1), DAYS(2), HOURS("09:00", "17:00")],
       ["Thursday, my office. Half past six."],
       [("Half past six.", {"flagEffects": [setf("hale_thursday_booked")]}, None),
        ("Not this week.", {}, None)],
       repeat=6, ignore=(1, {"effects": [pl_eff("grade_psych", -1)]}),   # (pass 3 F60)
       comment="Hale's repeat, after his step 4 (release 1): Wednesday, \"Thursday. Half past six.\" The yes books it (hale.py).")
noshow("hale_thursday_noshow", H, "📧 College email: Dr. Hale", "hale_thursday_booked", 24,
       ["Half past six. My door was unlocked."],   # pass 4 B48: "half past", and 7 words a bubble
       [("I couldn't get away.", "Then don't promise. — H."), ("Next week.", "We will see. — H.")],
       {"effects": [pl_eff("grade_psych", -1)]},
       extra=[DAYS(4), HOURS("09:00", "17:00")],
       comment="Hale: she said seven and didn't come (DECISIONS 87)")

# ── 7 · Jake (npc_jake.md: jake_number, a day later, 18:00-22:00). The date is booked only by her yes;
# nothing names a pickup before it. Weekly while unbooked. ──
BOOK = {"flagEffects": [setf("jake_date_booked")]}
# W8 (LO 2026-11-03): two dates a week, Wednesday and Saturday. The Saturday ask comes Thursday or Friday, the
# Wednesday ask Monday or Tuesday; one booking at a time.
thread("jake_date", J, "📱 Jake",
       [F("jake_number"), SINCE("jake_number", 1), F("jake_date_booked", False), TRAIT_GTE("jake_patience", JAKE_WAIT),
        DAYS(3, 4), HOURS("18:00", "22:00")],
       ["saturday? i'll pick you up"],
       [("yes", BOOK, "front door. eight. wear something"),
        ("not this week", {}, "next week then. i'm patient"),
        ("where are we going", {}, "surprise. yes or no?")],
       repeat=6, ignore=(1, {"effects": [pl_eff("jake_patience", -JAKE_WAIT)], "flagEffects": [setf("jake_ignored")]}),
       comment="Jake: caused by jake_number (Zoe's first party). The date is booked here.",
       round2=(2, [("yes", BOOK, "front door. eight."), ("no", {}, "next week then")]))
# (alignment pass 2, 2026-11-03) a missed date left jake_date_booked set for good: the pickup reads it only for 168
# hours and both invites need it false, so Jake never asked again. The no-show text clears it (DECISIONS 87, S10).
# The latest pickup is 51 hours after the latest ask, so 72 hours after the yes the date is missed. Jake has no
# meter of his own; the cost is the flag his hub line reads.
noshow("jake_date_noshow", J, "📱 Jake", "jake_date_booked", 72,
       ["sat outside your house twenty minutes", "you ok?", "asking again in a few days"],
       [("sorry. i fell asleep", "next time text me. ok?"), ("something came up", "fine. you owe me one.")],
       {"effects": [pl_eff("jake_patience", -JAKE_WAIT)], "flagEffects": [setf("jake_stood_up")]}, extra=[HOURS("10:00", "22:00")],   # (pass 3 F58) the hour window, P4
       comment="Jake: she said yes to a date and wasn't at the door (DECISIONS 87)")
# (pass 3 F61) standing him up costs the midweek date: while `jake_stood_up` holds he asks only for Saturday (his hub
# line: "You still owe me a date, you know. Saturday?"), until a date clears it (jake.py jake_date_pickup).
thread("jake_date_wed", J, "📱 Jake",
       [F("jake_number"), SINCE("jake_number", 1), F("jake_date_booked", False), F("jake_stood_up", False),
        TRAIT_GTE("jake_patience", JAKE_WAIT), DAYS(0, 1), HOURS("18:00", "22:00")],
       ["wednesday? i'll pick you up"],
       [("yes", BOOK, "front door. eight."),
        ("not this week", {}, "saturday then. maybe"),
        ("again?", {}, "again. yes or no?")],
       repeat=6, ignore=(1, {"effects": [pl_eff("jake_patience", -JAKE_WAIT)], "flagEffects": [setf("jake_ignored")]}),
       comment="Jake (W8, LO 2026-11-03): the midweek date, booked here.",
       round2=(2, [("yes", BOOK, "front door. eight."), ("no", {}, "saturday then")]))

# Reach audit 2026-11-09 (LO "Go ahead" on Zoe and Jake): after his step 4, on the nights with no date, Jake's booty
# call (Course of Temptation's shape, REPORT.md section 2). Her yes puts him at her door 22:00-00:00 (jake.py jake_booty_call).
thread("jake_booty_text", J, "📱 Jake",
       [F("jake_04_done"), SINCE("jake_04_done", 1), F("jake_coming", False), DAYS(0, 1, 3, 6), HOURS("21:00", "22:30")],
       ["you up? 😏", "i can be at yours in twenty"],
       [("door's unlocked", {"flagEffects": [setf("jake_coming")]}, "on my way"),
        ("not tonight", {}, "your loss gorgeous")],
       repeat=2, ignore=(1, {"effects": [pl_eff("jake_patience", -JAKE_WAIT)], "flagEffects": [setf("jake_ignored")]}),   # gate: ignoring costs more than a no
       comment="Jake's booty call, after his step 4 (the nights with no date)")

# Q5 (LO, 2026-11-04): an invite left unanswered gets one short text the day it closes, saying the next one
# waits. Fired by the ignore's own flag, which clears at midnight ([engine.daily_tick]); the replies change nothing
# (the wait is already paid). The met flag is the scene that caused the invite.
thread("zoe_ignored_text", Z, "📱 Zoe",
       [F("zoe_met"), SINCE("zoe_met", 1), F("zoe_ignored"), HOURS("08:00", "23:00")],
       ["wow ok. left on read", "fine. no invites this week 🙄"],
       [("sorry zo", {}, "mm. you'd better be"), ("i was busy", {}, "busy. sure.")],
       repeat=1, comment="Zoe: after she ignored an invite (Q5)")
thread("jake_ignored_text", J, "📱 Jake",
       [F("jake_number"), SINCE("jake_number", 1), F("jake_ignored"), HOURS("08:00", "22:00")],
       ["guess that's a no", "i'll ask again in a few days"],
       [("sorry, i missed it", {}, "it's ok. i'll ask again"), ("ok", {}, "ok.")],
       repeat=1, comment="Jake: after she ignored a date ask (Q5)")

w("")
w(open(os.path.join(HERE, "phone_calls.toml")).read().rstrip("\n"))
open(sys.argv[1], "w").write("\n".join(L) + "\n")
print("phone: 13 conversations, 2 posts, the calls")
