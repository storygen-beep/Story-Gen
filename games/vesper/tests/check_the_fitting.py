#!/usr/bin/env python3
"""
0.2.5 — THE FITTING — static guard.

Reads the merged TOML and checks the chunk against games/vesper/design_the_fitting.md ("BLUEPRINT").
One section per beat.

Run from the repo root, after a merge:
    python games/vesper/tests/check_the_fitting.py [path/to/7_final_game.toml]
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

# The frozen explicit-word list, copied from author-game-v2/scripts/gates.py (EXPLICIT), as check_the_transfer does.
EXPLICIT = re.compile(
    r"\b(cock|dick|penis|cunt|puss|clit|tit(?:s|ty|ties)?\b|breast|nipple|ass(?:es)?\b|arse|anal|balls"
    r"|fuck|suck|blowjob|handjob|cum|semen|orgasm|moan|naked|nude|undress|horny"
    r"|arous|lust|lewd|slut|whore|thrust|penetrat|grop|erect|masturbat|vagina"
    r"|kiss|lick)", re.I)

LOOP_TRAITS = {"loop_npc_pleasure", "sex_stage", "sex_finisher_type", "anal_active", "sex_entry_origin", "cain_round"}


def check(cond, msg):
    if not cond:
        fails.append(msg)


def walk(o, out):
    """Every dict anywhere under o, depth first."""
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


def cascade_beats(n):
    for b in (n or {}).get("blocks", []):
        if b.get("type") == "cascade":
            return b["props"]["beats"]
    return []


with open(GAME, "rb") as f:
    t = tomllib.load(f)
cv = {c["id"]: c for c in t["canvases"]}
cards = t.get("quest_cards", [])
story = [c for c in cards if not c.get("npc_id")]
core = (t.get("player") or {}).get("core_traits") or {}
labels = {l["key"]: l for l in (t.get("traits") or {}).get("labels", [])}

# ── A tiny evaluator for the fitting's AND-only gates: trait gte/lt/eq, flag is_true/is_false, days_since_flag. ──
# st = {"traits": {...}, "flags": {...}, "days": {flag: days since it was set}}. A days_since_flag on a flag with no
# recorded day fails closed, as the engine does (v2.py days_since_flag).
def met(i, st):
    if "trait_key" in i or ("trait" in i and "flag" not in i):
        k = i.get("trait_key") or i.get("trait")
        v = st["traits"].get(k, 0); op = i.get("operator") or i.get("op"); x = i["value"]
        return {"gte": v >= x, "gt": v > x, "lt": v < x, "lte": v <= x, "eq": v == x}[op]
    if i.get("type") == "days_since_flag":
        d = st["days"].get(i["flag_key"])
        if d is None:
            return False
        return {"gte": d >= i["value"], "lt": d < i["value"]}[i["operator"]]
    k = i.get("flag_key") or i.get("flag")
    want = (i.get("operator") or i.get("op")) == "is_true"
    return bool(st["flags"].get(k)) == want


def live(conds, st):
    return all(met(i, st) for i in conds)


# ── 0252 — the numbers, card S (O converted in place, split into nine at beat_0262), Kess's two home cards ──
for k in ("parts_fitted", "parts_out", "parts_settled", "cain_nights", "cain_asked", "cain_round"):
    check(core.get(k) == 0, f"0252: {k} declared in core_traits at 0")
    check((labels.get(k) or {}).get("hidden") is True, f"0252: {k} hidden from the dump")
s_cards = [c for c in story if {"trait": "parts_fitted", "subject": "player", "op": "lt", "value": 3} in c.get("when", [])
           or any(w.get("trait") in ("parts_out", "parts_settled") for w in c.get("when", []))]
check(len(s_cards) == 9, f"0262: card S is nine cards, one per visit, got {len(s_cards)}")
for s in s_cards:
    check(not s.get("terminal"), "0252: card S is not terminal (O was converted, not left standing)")
    check({"flag": "cain_chosen", "op": "is_true"} in s["when"], "0252: card S needs cain_chosen")
    check(any(g.get("trait") == "parts_fitted" and g.get("value") == 3 for g in s.get("goals", [])), "0252: card S counts parts_fitted to 3")
    check("next release" not in s["text"] + s["tip"], "0252: card S does not say the build ends")
kess_home = [c for c in cards if c.get("npc_id") == "npc_kess" and {"flag": "back_in_body", "op": "is_true"} in c.get("when", [])]
check(len(kess_home) == 2, f"0252: Kess has two home cards (before / after the fitting), got {len(kess_home)}")
check(sorted(w["op"] for c in kess_home for w in c["when"] if w.get("trait") == "parts_fitted") == ["gte", "lt"],
      "0252: Kess's two home cards are exclusive on parts_fitted 3")

# ── 0253-0255, 0262 — the fitting: three visits per part, one a calendar day ──
VISITS = [("strength", "fit", 40), ("strength_settle", "settle", None), ("strength_proof", "proof", None),
          ("armour", "fit", 60), ("armour_settle", "settle", None), ("armour_proof", "proof", None),
          ("blade", "fit", 80), ("blade_settle", "settle", None), ("blade_proof", "proof", None)]
COUNTER = {"fit": "parts_out", "settle": "parts_settled", "proof": "parts_fitted"}
kf = cv.get("kess_fitting")
check(kf is not None, "0253: kess_fitting exists")
if kf:
    tr = kf["trigger"]
    check(tr.get("substitution_only") is True and tr.get("location") == "kess_berth", "0253: substitution-only at kess_berth (never a second Kess card)")
    check(not tr.get("npc") and not tr.get("requires_npc"), "0253: no npc on the trigger")
    its = items(tr.get("conditions"))
    check(has(its, flag_key="back_in_body", operator="is_true") and has(its, trait_key="parts_fitted", operator="lt", value=3),
          "0253: gated back_in_body + parts_fitted lt 3")
    base = node(kf, "base")
    ch = choices(base)
    step = [c for c in ch if c.get("targetType") == "node"]
    check(len(step) == 9, f"0262: nine visit choices, got {len(step)}")
    check(any(c.get("text") == "Not now." and c.get("targetType") == "location" for c in ch), "0253: 'Not now.' always there")
    for c in step:
        check({"targetType": "player", "flag": "fitting_day", "op": "set"} in (c.get("flagEffects") or []),
              f"0262: {c.get('nodeId')} sets fitting_day")
    # Walk the whole fitting the way a player would: one day per visit, and a same-day retry after each.
    st = {"traits": {"parts_fitted": 0, "parts_out": 0, "parts_settled": 0}, "flags": {"cain_chosen": True}, "days": {}}
    bands = [b for b in base["blocks"] if b.get("type") == "group"]
    check(all(base["blocks"][i].get("type") == "group" for i in range(len(bands))),
          "0262: the base bands are ONE chain (all groups, adjacent), so the same-day band wins")
    for nid, kind, price in VISITS:
        offered = [c for c in step if live(items(c.get("conditions")), st)]
        check(len(offered) == 1 and offered[0].get("nodeId") == f"kess_fitting.{nid}",
              f"0262: on the day of {nid}, exactly that visit is offered, got {[c.get('nodeId') for c in offered]}")
        first_band = next((b for b in bands if live(items(b["props"]["conditions"]), st)), None)
        check(first_band is not None and not has(items(first_band["props"]["conditions"]), type="days_since_flag"),
              f"0262: the day of {nid} paints a stage band, not the same-day band")
        if not offered:
            break
        c = offered[0]
        want_cost = [{"trait": "coin", "value": price}] if price else None
        check(c.get("costs") == want_cost, f"0262: {nid} costs {price or 'nothing'}")
        if price:
            check(c.get("text") == f"Pay him. ({price} coin.)", f"0262: {nid} label names {price}")
        check(c.get("effects") == [{"targetType": "player", "trait": COUNTER[kind], "op": "add", "value": 1, "clamp": True, "cap": 3}],
              f"0262: {nid} adds 1 to {COUNTER[kind]}, clamped, cap 3")
        if nid != "strength":
            check(has(items(c.get("conditions")), type="days_since_flag", flag_key="fitting_day", operator="gte", value=1),
                  f"0262: {nid} waits a calendar day")
        st["traits"][COUNTER[kind]] += 1
        st["days"]["fitting_day"] = 0
        st["flags"]["fitting_day"] = True
        same = [x for x in step if live(items(x.get("conditions")), st)]
        check(same == [], f"0262: after {nid}, nothing more the same day, got {[x.get('nodeId') for x in same]}")
        fb = next((b for b in bands if live(items(b["props"]["conditions"]), st)), None)
        check(fb is not None and has(items(fb["props"]["conditions"]), type="days_since_flag", operator="lt"),
              f"0262: after {nid}, the same-day band paints")
        live_s = [x for x in s_cards if live(x["when"], st)]
        check(len(live_s) == (1 if st["traits"]["parts_fitted"] < 3 else 0),
              f"0262: after {nid}, exactly one card S is live, got {len(live_s)}")
        st["days"]["fitting_day"] = 1
        n = node(kf, nid)
        check(n is not None, f"0262: node {nid}")
        if not n:
            continue
        cfg = (n.get("exit_block") or {}).get("config") or {}
        check(cfg.get("locationId") == "kess_berth" and cfg.get("time_progression_minutes") == 240, f"0262: {nid} is 240 min, back to the Berth")
        check(n["blocks"][-1].get("type") == "cascade", f"0262: {nid}'s cascade is its last block")
    check(st["traits"] == {"parts_fitted": 3, "parts_out": 3, "parts_settled": 3}, f"0262: the walk ends with all three proven, got {st['traits']}")
    for nid, media in (("strength_proof", "scenes/fitting_strength.jpg"), ("armour", "scenes/fitting_armour.jpg"), ("blade_proof", "scenes/fitting_blade.jpg")):
        files = [d["props"].get("file") for d in walk(node(kf, nid) or {}, []) if d.get("type") == "image"]
        check(files == [media], f"0262: {nid} carries exactly {media}")
    all_files = [d["props"].get("file") for d in walk(kf, []) if d.get("type") == "image"]
    check(len(all_files) == 3, f"0262: three images in the fitting, one asset one block, got {all_files}")
    arm = text_of(node(kf, "armour"))
    check("She never did that." in arm and "can't build" in arm, "0254: Kess says the pain line in the armour session")
    bl = text_of(node(kf, "blade"))
    check("It goes when you say" in bl, "0255: the blade goes when she says (no charge, LO)")
hub = cv["hub_kess_berth"]
fit = [c for c in choices(node(hub, "base")) if c.get("text") == "Get on his bench."]
check(len(fit) == 1 and fit[0].get("nodeId") == "kess_fitting.base", "0253: the hub carries 'Get on his bench.' into kess_fitting")
if fit:
    ci = items(fit[0].get("conditions"))
    check(has(ci, flag_key="back_in_body", operator="is_true") and has(ci, trait_key="parts_fitted", operator="lt", value=3),
          "0253: the hub choice is gated back_in_body + parts_fitted lt 3")

wr = cv["kess_the_wreck"]
wb = node(wr, "base")["blocks"]
img_groups = [b for b in wb if b.get("type") == "group" and any(d.get("type") == "image" for d in walk(b, []))]
check(len(img_groups) == 1 and has(items(img_groups[0]["props"]["conditions"]), trait_key="parts_out", operator="lt", value=3),
      "0255: the wreck's image (blade still in the arm) only while parts_out lt 3 (beat_0262: until the blade's fit)")
check("parts_fitted" not in str(wb), "0262: the wreck reads parts_out (what has come out of Vega), never parts_fitted")
check(not [b for b in wb if b.get("type") == "image"], "0255: no ungrouped image on the wreck card")
# Every chain is separated from the next by an ungrouped line (adjacent groups merge).
kinds = ["g" if b.get("type") == "group" else "x" for b in wb]
runs = re.findall(r"g+", "".join(kinds))
check([len(r) for r in runs] == [1, 3, 4], f"0255: the wreck card's three chains are 1 / 3 / 4 groups, got {[len(r) for r in runs]}")
check("perfect memory" not in text_of(wr), "0255: the wreck card no longer promises the perfect memory")
ct = cv["activity_cain_trains"]
first_group = next(b for b in node(ct, "base")["blocks"] if b.get("type") == "group")
fi = items(first_group["props"]["conditions"])
check(has(fi, trait_key="parts_fitted", operator="gte", value=3) and has(fi, flag_key="cain_chosen", operator="is_true"),
      "0255: Cain's first band is the blade-is-in band (his 'Kess is going to put that blade in you' is spent)")

# ── 0256 — the knife ──
kn = cv.get("cap_the_knife")
check(kn is not None, "0256: cap_the_knife exists")
if kn:
    tr = kn["trigger"]
    its = items(tr.get("conditions"))
    check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and tr.get("priority") == 11, "0256: one-shot at the Site, pri 11")
    check(has(its, trait_key="parts_fitted", operator="gte", value=2) and has(its, flag_key="knife_tested", operator="is_false"), "0256: gated armour in + not yet tested")
    check(has(its, type="npc_at_location", location_id="the_site", npc_id="npc_cain", operator="is_present"), "0256: Cain present (npc_at_location)")
    cfg = node(kn, "base")["exit_block"]["config"]
    check({"targetType": "player", "flag": "knife_tested", "op": "set"} in cfg.get("flagEffects", []), "0256: sets knife_tested")
    check("the way you'd test a hide" in text_of(kn), "0256: the stroke echoes cap_study_blade")

# ── 0257 — Cain's loop ──
trio = [c for c in choices(node(ct, "base")) if c.get("text") == "Lie down with him."]
check(len(trio) == 3, "0257: three 'Lie down with him.' choices")
step = 0
for c in trio:
    check(c.get("nodeId") == "loop_cain_site.intro", "0257: each goes into loop_cain_site.intro")
    ci = items(c.get("conditions"))
    check(has(ci, flag_key="cain_chosen", operator="is_true"), "0257: each needs cain_chosen")
    resets = {e["trait"] for e in c.get("effects", []) if e.get("op") == "set" and e.get("value") == 0}
    check(LOOP_TRAITS <= resets, f"0257: each entry resets every loop trait, missing {LOOP_TRAITS - resets}")
    adds = [e for e in c.get("effects", []) if e.get("trait") == "cain_nights"]
    if adds:
        step += 1
        check(adds == [{"targetType": "player", "trait": "cain_nights", "op": "add", "value": 1, "clamp": True, "cap": 4}], "0257: cain_nights +1, cap 4")
        check({"targetType": "player", "flag": "cain_lay", "op": "set"} in c.get("flagEffects", []), "0257: a stepping entry re-sets cain_lay")
check(step == 2, "0257: exactly two of the three step cain_nights (first night, later day); the same-day one does not")
dsf = sorted(i["operator"] for c in trio for i in items(c.get("conditions")) if i.get("type") == "days_since_flag")
check(dsf == ["gte", "lt"], "0257: the later-day and same-day entries are exact complements on days_since_flag cain_lay")
loop = cv.get("loop_cain_site")
fin = cv.get("loop_cain_site_finisher")
check(loop is not None and fin is not None, "0257: loop_cain_site + finisher exist")
if loop and fin:
    check("trigger" not in loop and "trigger" not in fin, "0257: loop and finisher are triggerless")
    allc = walk(loop, []) + walk(fin, [])
    stages = {e.get("value") for e in allc if e.get("trait") == "sex_stage" and e.get("op") == "set"}
    check(stages <= {0, 1}, f"0257: sex_stage only ever 0 or 1 (no anal slot), got {stages}")
    check(not [e for e in allc if e.get("trait") == "anal_active" and e.get("value") not in (0, None)], "0257: anal_active never set")
    fts = {e.get("value") for e in allc if e.get("trait") == "sex_finisher_type" and e.get("op") == "set"}
    check(fts <= {0, 1}, f"0257: finishes are her mouth (0) and inside her (1) only, got {fts}")
    words = text_of(loop) + " " + text_of(fin)
    check(not re.search(r"\b(ass|anal|arse)\b", words, re.I), "0257: no anal word anywhere in the loop (the signed row)")
    # On top waits for night 2 on every route in, except from inside on top itself, the ask (night 4) and the
    # second round (night 3), which can only be reached later than night 2.
    for nid in ("intro", "base_his_mouth", "base_her_mouth", "base_under_cain"):
        for c in choices(node(loop, nid)):
            if c.get("nodeId") == "base_on_top":
                check(has(items(c.get("conditions")), trait_key="cain_nights", operator="gte", value=2),
                      f"0257: '{c.get('text')}' from {nid} into on top waits for cain_nights 2")
    again = [c for c in choices(node(fin, "climax")) if c.get("text") == "Again."]
    check(len(again) == 1, "0257: the finisher offers 'Again.'")
    if again:
        ai = items(again[0].get("conditions"))
        check(has(ai, trait_key="cain_nights", operator="gte", value=3) and has(ai, trait_key="cain_round", operator="lt", value=1),
              "0257: 'Again.' opens at cain_nights 3, once a sitting")
        check({"targetType": "player", "trait": "cain_round", "op": "set", "value": 1, "clamp": False} in again[0].get("effects", []), "0257: 'Again.' sets cain_round")
    out = [c for c in choices(node(fin, "climax")) if c.get("targetType") == "location"]
    check(len(out) == 1 and out[0].get("locationId") == "the_site" and out[0].get("time_progression_minutes") == 120, "0257: the way out is 120 min to the Site")
    if out:
        resets = {e["trait"] for e in out[0].get("effects", []) if e.get("op") == "set" and e.get("value") == 0}
        check(LOOP_TRAITS <= resets, f"0257: the way out resets every loop trait, missing {LOOP_TRAITS - resets}")
    lines = text_of(loop) + text_of(fin)
    check("Kess made sure" not in lines and "stronger than me" not in lines,
          "0257: no loop line assumes the parts are in (the loop opens before the fitting)")

# ── 0258 — the ask ──
if loop:
    ask = [c for c in choices(node(loop, "intro")) if c.get("text") == "Ask him for it."]
    check(len(ask) == 1 and ask[0].get("nodeId") == "the_ask", "0258: the intro offers 'Ask him for it.'")
    if ask:
        ai = items(ask[0].get("conditions"))
        check(has(ai, trait_key="cain_nights", operator="gte", value=4) and has(ai, trait_key="cain_asked", operator="lt", value=1), "0258: the ask opens at night 4, once")
        check(ask[0].get("effects") == [{"targetType": "player", "trait": "cain_asked", "op": "set", "value": 1, "clamp": False}], "0258: the ask sets cain_asked")
    an = node(loop, "the_ask")
    vids = [d["props"] for d in walk(an, []) if d.get("type") == "video"]
    check([v.get("file") for v in vids] == ["sex/cain_asks_t5.webm"], "0258: the one-time ask is one file, not a pool")
    beats = cascade_beats(an)
    check(len(beats) >= 3, "0258: the ask is a cascade")
    if beats:
        last = text_of(beats[-1])
        before = text_of(beats[-2])
        check(len(EXPLICIT.findall(last)) < 3 and len(EXPLICIT.findall(before)) >= 3, "0258: the meaning beat comes after the body (the pivot rule)")
    first_band = next(b for b in node(loop, "intro")["blocks"] if b.get("type") == "group")
    check(has(items(first_band["props"]["conditions"]), trait_key="cain_asked", operator="gte", value=1), "0258: after the ask, the intro's first band is her asking")
cain_end = [c for c in cards if c.get("npc_id") == "npc_cain" and {"flag": "cain_chosen", "op": "is_true"} in c.get("when", [])]
check(len(cain_end) == 1 and "Lie down with him" in cain_end[0].get("tip", ""), "0258: Cain's card names the loop")

# ── 0259 — the hunt ──
u = cv.get("rand_units_street")
check(u is not None, "0259: rand_units_street exists")
if u:
    tr = u["trigger"]
    check(tr.get("location") == "underworld_strip" and tr.get("trigger_mode") == "random" and tr.get("chance") == 0.35
          and tr.get("max_triggers_per_day") == 1 and tr.get("is_repeatable") is True, "0259: random on the strip, 35%, once a day, repeatable")
    check(not tr.get("npc") and not tr.get("requires_npc"), "0259: no npc gate (they have no rows)")
    its = items(tr.get("conditions"))
    check(has(its, trait_key="parts_fitted", operator="gte", value=3), "0259: waits for all three parts")
    check(not [d for d in walk(u, []) if d.get("type") == "dialog" and (d.get("props") or {}).get("speaker") == "npc"
               and (d.get("props") or {}).get("npcId") != "npc_cain"], "0259: Lyra and Nova never speak (only Cain has a line, after)")
    check("npc_lyra" not in str(u) and "npc_nova" not in str(u) and "npc_vega" not in str(u), "0259: no NPC entries borrowed for the units")
    runs_ = choices(node(u, "base"))
    check([c.get("text") for c in runs_] == ["Run.", "Run."], "0259: the only choice is 'Run.'")
    ops = sorted(i["operator"] for c in runs_ for i in items(c.get("conditions")) if i.get("flag_key") == "units_first_loss")
    check(ops == ["is_false", "is_true"], "0259: the two Runs are exact complements on units_first_loss")
    rf = node(u, "run_first")["exit_block"]["config"]
    check(rf.get("locationId") == "the_site", "0259: the first loss goes to the Site (Cain carried her)")
    check({"targetType": "player", "trait": "vega_damage", "op": "add", "value": 60, "clamp": True} in rf.get("effects", []), "0259: first loss +60, clamped")
    check({"targetType": "player", "flag": "units_first_loss", "op": "set"} in rf.get("flagEffects", []), "0259: first loss sets units_first_loss")
    rl = node(u, "run")["exit_block"]["config"]
    check(rl.get("locationId") == "the_cot" and rl.get("time_progression_minutes") == 540, "0259: a later loss is the lost day home to the cot")
    check({"targetType": "player", "trait": "vega_damage", "op": "add", "value": 60, "clamp": True} in rl.get("effects", []), "0259: later losses +60, clamped")
    txt = text_of(u)
    check("Lyra and Nova" in txt and not re.search(r"\b(one of them alone|alone, one)\b", txt), "0259: always the two of them")
    check("Draw them out" not in str(t), "0259: no 'Draw them out' card anywhere (LO)")
t_card = [c for c in story if {"flag": "units_first_loss", "op": "is_false"} in c.get("when", [])]
check(len(t_card) == 1 and not t_card[0].get("terminal") and "run" in t_card[0].get("tip", ""), "0259: card T, live until the first loss, tells her to run")
twin = [c for c in choices(node(hub, "base")) if c.get("text") in ("Have him fix what she did.", "Have him fix what they did.")]
check(len(twin) == 2, "0259: the repair has its twin")
check(sorted(i["operator"] for c in twin for i in items(c.get("conditions")) if i.get("flag_key") == "units_first_loss") == ["is_false", "is_true"],
      "0259: 'she' and 'they' are exclusive on units_first_loss")
pu = node(cv["kess_patch_up"], "base")["blocks"]
g1 = next(b for b in pu if b.get("type") == "group")
check(has(items(g1["props"]["conditions"]), flag_key="units_first_loss", operator="is_true"), "0259: Kess's repair lines for the two of them come first")

# ── 0260 — the ending ──
mc = cv.get("cap_more_coming")
check(mc is not None, "0260: cap_more_coming exists")
if mc:
    tr = mc["trigger"]
    its = items(tr.get("conditions"))
    check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False, "0260: one-shot at the Site")
    check(has(its, flag_key="units_first_loss", operator="is_true") and has(its, flag_key="more_coming", operator="is_false"), "0260: after the first loss, once")
    check(not [i for i in its if i.get("type") == "npc_at_location"], "0260: no presence gate (he carried her in)")
    cfg = node(mc, "base")["exit_block"]["config"]
    check({"targetType": "player", "flag": "more_coming", "op": "set"} in cfg.get("flagEffects", []), "0260: sets more_coming")
    mt = text_of(mc)
    check("Bastien's men saw them" in mt and "can't make" in mt, "0260: why he came (Bastien's men in the stalls), and what she is that they can't make")
    check("Chairman" not in mt, "0260: the Chairman stays off screen (deferred)")
terms = [c for c in story if c.get("terminal")]
check(len(terms) == 1 and terms[0].get("when") == [{"flag": "more_coming", "op": "is_true"}], "0260: end card U is the only terminal story card")
if terms:
    check("'" not in terms[0].get("terminal_text", ""), "0260: no apostrophe in terminal_text")
# The story cards are exclusive across the chapter: exactly one live in each state.
def live_story(st):
    out = []
    for c in story:
        ok = True
        for w in c.get("when", []):
            if "flag" in w:
                ok = ok and (st.get(w["flag"], False) is (w["op"] == "is_true"))
            elif "trait" in w and w.get("subject") == "player":
                v = st.get(w["trait"], 0)
                ok = ok and {"lt": v < w["value"], "gte": v >= w["value"]}[w["op"]]
        if ok:
            out.append(c["text"][:30])
    return out
base = {k: True for k in ("cain_chosen", "back_in_body", "memory_whole", "dace_dead", "transferred", "memory_taken",
                          "rise_searched", "tower_planned", "units_fought", "last_night_held", "cradles_ready",
                          "study_blade", "study_signal", "study_method", "vega_taken", "vega_dismantled", "seam_known")}
ALL3 = {"parts_fitted": 3, "parts_out": 3, "parts_settled": 3}
for name, extra in (("fitting 0", {}), ("strength in, unsettled", {"parts_out": 1}),
                    ("strength settled, untested", {"parts_out": 1, "parts_settled": 1}),
                    ("fitting 2", {"parts_fitted": 2, "parts_out": 2, "parts_settled": 2}),
                    ("blade in, unsettled", {"parts_fitted": 2, "parts_out": 3, "parts_settled": 2}),
                    ("blade settled, untested", {"parts_fitted": 2, "parts_out": 3, "parts_settled": 3}),
                    ("hunted", ALL3),
                    ("after the first loss", {**ALL3, "units_first_loss": True, "more_coming": True})):
    got = live_story({**base, **extra})
    check(len(got) == 1, f"0260: exactly one story card live in '{name}', got {got}")

# ── 0261 — the dev jump ──
dj = cv.get("dev_jump_fitting_start")
check(dj is not None and "0.2.5: start" in dj.get("name", ""), "0261: dev jump '0.2.5: start (the end of 0.2.4)'")
if dj:
    ch = choices(node(dj, "seed"))[0]
    fe = {e["flag"]: e["op"] for e in ch.get("flagEffects", [])}
    for f_ in ("cain_chosen", "memory_whole", "back_in_body", "dace_dead"):
        check(fe.get(f_) == "set", f"0261: the jump sets {f_}")
    for f_ in ("in_vega", "knife_tested", "cain_lay", "units_first_loss", "more_coming", "fitting_day"):
        check(fe.get(f_) == "unset", f"0261: the jump unsets {f_}")
    te = {e["trait"]: e.get("value") for e in ch.get("effects", []) if e.get("op") == "set" and e.get("targetType") == "player"}
    check(te.get("parts_fitted") == 0 and te.get("coin", 0) >= 180, "0261: parts 0 and coin for all three fittings")
    check(te.get("parts_out") == 0 and te.get("parts_settled") == 0, "0262: the jump zeroes parts_out and parts_settled")
    check(ch.get("locationId") == "kess_berth", "0261: lands at the Berth")
for old in ("dev_jump_transfer_start", "dev_jump_in_vega"):
    ch = choices(node(cv[old], "seed"))[0]
    fe = {e["flag"]: e["op"] for e in ch.get("flagEffects", [])}
    check(fe.get("units_first_loss") == "unset", f"0261: {old} resets the 0.2.5 flags")

if fails:
    print("THE FITTING GUARD: FAILED")
    for f_ in fails:
        print("  - " + f_)
    sys.exit(1)
print("THE FITTING GUARD: OK")
