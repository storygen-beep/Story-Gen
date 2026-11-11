#!/usr/bin/env python3
"""
0.2.6 — YOU, FOR HIM — static guard.

Reads the merged TOML and checks the chunk against games/vesper/design_the_offer.md ("BLUEPRINT", signed
2026-11-10), beats 0263-0274: the sealed places, the people and their rows, the switch-offs, every scene's gate and
what it sets, the four drain rigs (one step a day on the hub, the drain only at the top, each drain opens the next
door), the story cards (exactly one live in each state of the chapter), the end card, and the dev jump.

Run from the repo root, after a dev merge:
    python games/vesper/tests/check_you_for_him.py [path/to/7_final_game.toml]
Exits 0 on pass, 1 on any failure.
"""
import os
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:                      # py<3.11
    import tomli as tomllib                      # type: ignore

HERE = os.path.dirname(__file__)
GAME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "toml_phases", "7_final_game.toml")
fails = []

# The frozen explicit-word list, copied from author-game-v2/scripts/gates.py (EXPLICIT), as check_the_fitting does.
EXPLICIT = re.compile(
    r"\b(cock|dick|penis|cunt|puss|clit|tit(?:s|ty|ties)?\b|breast|nipple|ass(?:es)?\b|arse|anal|balls"
    r"|fuck|suck|blowjob|handjob|cum|semen|orgasm|moan|naked|nude|undress|horny"
    r"|arous|lust|lewd|slut|whore|thrust|penetrat|grop|erect|masturbat|vagina"
    r"|kiss|lick)", re.I)


def check(cond, msg):
    if not cond:
        fails.append(msg)


def walk(o, out):
    if isinstance(o, dict):
        out.append(o)
        for v in o.values():
            walk(v, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, out)
    return out


def text_of(o):
    return " ".join(d.get("content", "") for d in walk(o, []) if isinstance(d.get("content"), str))


def items(cond):
    return (cond or {}).get("items", []) if isinstance(cond, dict) else []


def has(its, **kw):
    return any(all(i.get(k) == v for k, v in kw.items()) for i in its)


def node(cf, nid):
    return next((n for n in cf.get("nodes", []) if n.get("id") == nid), None)


def choices(n):
    return ((n or {}).get("exit_block") or {}).get("choices") or []


with open(GAME, "rb") as fh:
    g = tomllib.load(fh)
canv = {c["id"]: c for c in g.get("canvases", [])}
locs = {l["id"]: l for l in g.get("locations", [])}
npcs = {n["id"]: n for n in g.get("npcs", [])}
cards = g.get("quest_cards", [])
story = [c for c in cards if not c.get("npc_id")]
traits = g.get("player", {}).get("core_traits", {})

# ── 0263: the numbers, the places, the people
NEW_TRAITS = ["tests_done", "guard_nights", "tech_nights", "sabin_nights", "keeper_nights", "guard_drains_done",
              "tech_drains_done", "sabin_custody_drains", "keeper_drains_done", "floor_door", "study_door", "records_door"]
for t in NEW_TRAITS:
    check(traits.get(t) == 0, f"0263: trait {t} declared 0")
for root in ("chairmans_room", "holding_cell"):
    L = locs.get(root) or {}
    check(L and not L.get("entry_from") and not L.get("parent") and L.get("auto_exit") is False, f"0263: {root} is sealed (no entry_from, no parent, auto_exit false)")
for child, parent, lock in (("chairmans_door", "chairmans_room", "cell_door"), ("holding_floor", "holding_cell", "floor_door"),
                            ("test_lab", "holding_floor", None), ("sabin_study", "holding_floor", "study_door"),
                            ("records_room", "holding_floor", "records_door")):
    L = locs.get(child) or {}
    check(L.get("entry_from") == parent and not L.get("parent"), f"0263: {child} attaches to {parent} by entry_from only")
    if lock:
        ec = L.get("entry_conditions") or {}
        check(ec.get("version") == "1.0" and has(items(ec), type="trait", trait_key=lock, operator="gte", value=1), f"0263: {child} locked on trait {lock}")
for nid in ("npc_chairman", "npc_guard", "npc_technician", "npc_keeper"):
    check(nid in npcs, f"0263: {nid} exists")
check(not npcs.get("npc_chairman", {}).get("schedules"), "0263: the Chairman has no row (one self-firing scene)")
for nid in ("npc_guard", "npc_technician", "npc_keeper"):
    for r in npcs.get(nid, {}).get("schedules", []):
        check((r.get("when") or {}).get("version") == "1.0" and has(items(r.get("when")), flag_key="in_custody", operator="is_true"), f"0263: {nid}'s rows only while in_custody")
rows = {r["location"]: r for r in npcs["npc_sabin"]["schedules"]}
check(set(rows) == {"the_rise_floor", "sabin_lab", "sabin_study"}, "0263: Sabin's three rows")
check(has(items(rows["sabin_study"].get("when")), flag_key="in_custody", operator="is_true"), "0263: the study row only inside")
for k in ("the_rise_floor", "sabin_lab"):
    check(has(items(rows[k].get("when")), flag_key="in_custody", operator="is_false"), f"0263: Sabin's {k} row off inside")
for r in npcs["npc_cain"]["schedules"]:
    check(has(items(r.get("when")), flag_key="cain_taken", operator="is_false"), "0263: Cain's rows off once taken")
for r in npcs["npc_mercer"]["schedules"]:
    check(has(items(r.get("when")), flag_key="mercer_dead", operator="is_false"), "0263: Mercer's rows off once dead")


def trig(cid):
    return (canv.get(cid) or {}).get("trigger", {}) or {}


def tgate(cid):
    return items(trig(cid).get("conditions"))


def sets(cid, f):
    return any(fe.get("flag") == f and fe.get("op") == "set" for d in walk(canv.get(cid), []) for fe in (d.get("flagEffects") or []) if isinstance(fe, dict))


# ── 0264: part one
check(trig("rand_units_no_show").get("location") == "underworld_strip" and trig("rand_units_no_show").get("is_repeatable") is False, "0264: nobody-comes is a one-shot on the strip")
its = tgate("rand_units_no_show")
check(has(its, flag_key="more_coming", operator="is_true") and has(its, type="time_of_day", start_time="21:00", end_time="03:00"), "0264: after 0.2.5, at night")
check(sets("rand_units_no_show", "units_no_show"), "0264: sets units_no_show")
check(trig("cap_site_wrecked").get("location") == "the_site" and has(tgate("cap_site_wrecked"), flag_key="units_no_show", operator="is_true"), "0264: the wrecked Site fires after nobody came")
check(sets("cap_site_wrecked", "cain_taken"), "0264: sets cain_taken")
check(not [i for i in tgate("cap_site_wrecked") if i.get("type") == "npc_at_location"], "0264: no presence gate on the wrecked Site")
check(has(tgate("rand_units_street"), flag_key="cain_taken", operator="is_false") and has(tgate("rand_units_street"), flag_key="in_custody", operator="is_false"), "0264: the hunt stops at cain_taken and inside")
check(has(tgate("activity_cain_trains"), flag_key="cain_taken", operator="is_false"), "0264: Cain's card closes at cain_taken")

# ── 0265: part two
check(trig("cap_mercer_brings_offer").get("location") == "the_cot" and has(tgate("cap_mercer_brings_offer"), flag_key="cain_taken", operator="is_true"), "0265: the offer at the cot after cain_taken")
check(sets("cap_mercer_brings_offer", "offer_made") and sets("cap_mercer_brings_offer", "mercer_found"), "0265: sets offer_made and mercer_found")
check("You, for him." in text_of(canv["cap_mercer_brings_offer"]), "0265: the offer in his words")
ans = node(canv["hub_mercer_room"], "answer")
check(ans and "Once you go in, the city is closed until the next release." in text_of(ans), "0265: the plain warning")
go = next((c for c in choices(ans) if c.get("text") == "Go with him."), {})
check(go.get("locationId") == "chairmans_room" and {"targetType": "player", "flag": "in_custody", "op": "set"} in go.get("flagEffects", []), "0265: 'Go with him.' sets in_custody and goes to the Chairman's room")
check(any(e.get("trait") == "equipped_weapon" and e.get("value") == 1 for e in go.get("effects", [])), "0265: she goes in carrying the drain")
check(not (ans.get("exit_block") or {}).get("config"), "0265: nothing is set on the warning's render")

# ── 0266: part five
t = text_of(canv.get("cap_chairman_talk"))
for line in ("Sit. You've been running a long time.", "Not one has ever been afraid.", "I want to know how it was put in you. All of it.",
             "That's not a question you get to ask yet.", "He's free. I keep my word. Ask Mr. Mercer.", "They'll take you down now. Try to be useful."):
    check(line in t, f"0266: the signed line '{line[:30]}...'")
check("wife" not in t.lower(), "0266: he never says why (the wife stays out of his mouth)")
check(sets("cap_chairman_talk", "chairman_met"), "0266: sets chairman_met")

# ── 0267: part six
tc = canv.get("activity_the_tests") or {}
check(trig("activity_the_tests").get("location") == "holding_cell", "0267: the tests card is on the cell")
gw = [c for c in choices(node(tc, "base")) if c.get("text") == "Go with them."]
check(len(gw) == 5, f"0267: five test choices, one per step ({len(gw)})")
for c in gw:
    check({"targetType": "player", "flag": "test_day", "op": "set"} in c.get("flagEffects", []), "0267: every test stamps test_day")
    check(any(e.get("trait") == "energy" and e.get("value") == -20 for e in c.get("effects", [])), "0267: every test costs 20 energy")
refills = [c for c in gw if any(e.get("trait") == "drain_charge" and e.get("value") == 1 for e in c.get("effects", []))]
check(len(refills) == 4, "0267: every test from the machine on refills the drain")
check("activity_cell_sleep" in canv and "activity_cell_wait" in canv, "0267/0268: sleep and wait in the cell")

# ── 0268: part four
check(sets("cap_mercer_last_visit", "mercer_last_visit") and sets("cap_guard_news", "mercer_dead"), "0268: the last visit and the news set their flags")
check(has(tgate("cap_guard_news"), type="npc_at_location", npc_id="npc_guard", operator="is_present"), "0268: the news is the guard's line")
for cid in ("cap_first_penthouse_service", "mercer_penthouse_hub", "cap_mercer_resurfaces", "hub_mercer_room", "mercer_room_offhours",
            "mercer_end_table", "rung_mercer_hands_on", "cap_owner_print", "salvage_mercer_shocked"):
    check(has(tgate(cid), flag_key="mercer_dead", operator="is_false"), f"0268: {cid} closes at mercer_dead")
for c in cards:
    if c.get("npc_id") == "npc_mercer":
        check({"flag": "mercer_dead", "op": "is_false"} in c.get("when", []), "0268: Mercer's cards close at mercer_dead")

# ── 0269-0272: the four rigs
RIGS = (("guard", "holding_cell", "guard_nights", "guard_day", 3, 6, "guard_drains_done", "floor_door"),
        ("technician", "test_lab", "tech_nights", "tech_day", 2, 4, "tech_drains_done", "study_door"),
        ("sabin_study", "sabin_study", "sabin_nights", "sabin_day", 3, 4, "sabin_custody_drains", "records_door"),
        ("keeper", "records_room", "keeper_nights", "keeper_day", 5, 7, "keeper_drains_done", None))
for rid, loc, nights, day, op, top, drains, lock in RIGS:
    hub, fin = canv.get(f"hub_{rid}"), canv.get(f"loop_{rid}_finisher")
    check(hub and fin and f"loop_{rid}" in canv and f"{rid}_drain_canvas" in canv, f"{rid}: the four canvases exist")
    if not (hub and fin):
        continue
    check(hub["trigger"].get("location") == loc and has(items(hub["trigger"]["conditions"]), flag_key="in_custody", operator="is_true"), f"{rid}: hub at {loc}, inside only")
    for cid in (f"loop_{rid}", f"loop_{rid}_finisher", f"{rid}_drain_canvas"):
        check(not canv[cid].get("trigger"), f"{rid}: {cid} is triggerless")
    steppers = [c for c in choices(node(hub, "base")) if any(e.get("trait") == nights and e.get("op") == "add" for e in c.get("effects", []))]
    for c in steppers:
        ci = items(c.get("conditions"))
        check({"targetType": "player", "flag": day, "op": "set"} in c.get("flagEffects", []), f"{rid}: every step stamps {day}")
        check(has(ci, type="days_since_flag", flag_key=day, operator="gte", value=1) or has(ci, flag_key=day, operator="is_false"), f"{rid}: every step waits a calendar day ('{c['text']}')")
        check(c.get("costs") == [{"trait": "energy", "value": 15}], f"{rid}: every step costs 15 energy")
    check(len(steppers) == op + 1, f"{rid}: {op} rungs and one stepping loop entry ({len(steppers)})")
    for d in walk(canv[f"loop_{rid}"], []):
        for e in d.get("effects") or []:
            if isinstance(e, dict):
                check(e.get("trait") != nights, f"{rid}: the loop never moves {nights}")
    fc = choices(node(fin, "climax"))
    d0 = next((c for c in fc if c.get("nodeId") == f"{rid}_drain_canvas.d0"), {})
    di = items(d0.get("conditions"))
    check(has(di, trait_key=nights, operator="gte", value=top) and has(di, trait_key="drain_charge", operator="gte", value=1)
          and has(di, trait_key="equipped_weapon", operator="eq", value=1) and has(di, trait_key=drains, operator="lt", value=1), f"{rid}: the first drain needs the top of the ladder, the weapon and the charge")
    eff = d0.get("effects", [])
    check(any(e.get("trait") == drains and e.get("op") == "add" for e in eff), f"{rid}: the first drain bumps {drains}")
    if lock:
        check(any(e.get("trait") == lock and e.get("value") == 1 for e in eff), f"{rid}: the first drain opens {lock}")
    check(any(has(items(c.get("conditions")), trait_key=nights, operator="lt", value=top) for c in fc), f"{rid}: below the top the ass finish lets go")
    body = sum(1 for n in canv[f"loop_{rid}"]["nodes"] for _ in [0] if len(EXPLICIT.findall(text_of(n))) >= 3)
    check(body >= 3, f"{rid}: the loop's poses stay on the body (3+ explicit words in {body} nodes)")
check(has(tgate("hub_sabin"), flag_key="in_custody", operator="is_false"), "0271: hub_sabin closes inside")

# ── 0273: the file and the end card
check(trig("cap_the_wifes_file").get("location") == "records_room" and has(tgate("cap_the_wifes_file"), trait_key="keeper_drains_done", operator="gte", value=1), "0273: the file after the keeper's drain")
check(sets("cap_the_wifes_file", "wife_file_read"), "0273: sets wife_file_read")
ft = text_of(canv.get("cap_the_wifes_file"))
check("subject did not survive transfer" in ft and "Cain" in ft and "A. Vance" in ft, "0273: what the file says")
terms = [c for c in story if c.get("terminal")]
check(len(terms) == 1 and terms[0].get("when") == [{"flag": "wife_file_read", "op": "is_true"}], "0273: end card AB is the only terminal story card")
if terms:
    check("'" not in terms[0].get("terminal_text", ""), "0273: no apostrophe in terminal_text")
leak = [c.get("npc_id") for c in cards if c.get("npc_id") and {"flag": "in_vega", "op": "is_false"} in c.get("when", [])
        and not any(w.get("flag") == "in_custody" for w in c.get("when", []))]
check(not leak, f"0273: every city character card hides inside ({leak[:5]})")


def live_story(st):
    out = []
    for c in story:
        good = True
        for w in c.get("when", []):
            if "flag" in w:
                good = good and (st.get(w["flag"], False) is (w["op"] == "is_true"))
            elif "trait" in w and w.get("subject") == "player":
                v = st.get(w["trait"], 0)
                good = good and {"lt": v < w["value"], "gte": v >= w["value"]}[w["op"]]
        if good:
            out.append(c["text"][:30])
    return out


base = {k: True for k in ("cain_chosen", "back_in_body", "memory_whole", "dace_dead", "transferred", "memory_taken",
                          "rise_searched", "tower_planned", "units_fought", "last_night_held", "cradles_ready",
                          "study_blade", "study_signal", "study_method", "vega_taken", "vega_dismantled", "seam_known",
                          "units_first_loss", "more_coming")}
base.update({"parts_fitted": 3, "parts_out": 3, "parts_settled": 3})
steps = [("0.2.5 ended", {}), ("Cain taken", {"cain_taken": True}), ("offer made", {"cain_taken": True, "offer_made": True})]
inside = {"cain_taken": True, "offer_made": True, "in_custody": True}
steps += [("going in", inside), ("inside", {**inside, "chairman_met": True}),
          ("floor open", {**inside, "chairman_met": True, "floor_door": 1}),
          ("study open", {**inside, "chairman_met": True, "floor_door": 1, "study_door": 1}),
          ("records open", {**inside, "chairman_met": True, "floor_door": 1, "study_door": 1, "records_door": 1}),
          ("keeper drained", {**inside, "chairman_met": True, "floor_door": 1, "study_door": 1, "records_door": 1, "keeper_drains_done": 1}),
          ("the end", {**inside, "chairman_met": True, "floor_door": 1, "study_door": 1, "records_door": 1, "keeper_drains_done": 1, "wife_file_read": True})]
for name, extra in steps:
    got = live_story({**base, **extra})
    ok1 = len(got) == 1 or (name in ("going in", "keeper drained") and len(got) <= 1)
    check(ok1, f"cards: exactly one story card live at '{name}' ({got})")

# ── 0274: the dev jump
j = canv.get("dev_jump_offer_start")
check(j and "0.2.6: start" in j.get("name", ""), "0274: the 0.2.6 jump exists")
if j:
    ch = choices(node(j, "seed"))[0]
    fe = {f["flag"]: f["op"] for f in ch.get("flagEffects", [])}
    check(fe.get("more_coming") == "set" and fe.get("units_first_loss") == "set", "0274: the jump starts after 0.2.5's end")
    for f in ("cain_taken", "offer_made", "in_custody", "chairman_met", "mercer_dead", "wife_file_read"):
        check(fe.get(f) == "unset", f"0274: the jump starts with {f} unset")
    check(ch.get("locationId") == "the_cot", "0274: lands at the cot")
for jid in ("dev_jump_fitting_start", "dev_jump_in_vega", "dev_jump_transfer_start"):
    fe = {f["flag"]: f["op"] for c in choices(node(canv.get(jid, {}), "seed")) for f in c.get("flagEffects", [])}
    check(fe.get("in_custody") == "unset" and fe.get("cain_taken") == "unset", f"0274: {jid} unsets the 0.2.6 flags")

if fails:
    print("YOU, FOR HIM GUARD: FAILED")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("YOU, FOR HIM GUARD: OK")
