#!/usr/bin/env python3
"""
0.2.4 — THE TRANSFER — static guard.

Reads the merged TOML and checks the chunk against games/vesper/design_the_transfer.md ("BLUEPRINT").
One section per beat; each beat adds its own section in the same turn it is built.

Run from the repo root, after a merge:
    python games/vesper/tests/check_the_transfer.py
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
GAME = os.path.join(HERE, "..", "toml_phases", "7_final_game.toml")

fails = []

# The frozen explicit-word list, VERSION 2, copied from author-game-v2/scripts/gates.py (EXPLICIT) so this guard
# measures an explicit beat the way the build's own register gate does.
EXPLICIT = re.compile(
    r"\b(cock|dick|penis|cunt|puss|clit|tit(?:s|ty|ties)?\b|breast|nipple|ass(?:es)?\b|arse|anal|balls"
    r"|fuck|suck|blowjob|handjob|cum|semen|orgasm|moan|naked|nude|undress|horny"
    r"|arous|lust|lewd|slut|whore|thrust|penetrat|grop|erect|masturbat|vagina"
    r"|kiss|lick)", re.I)


def check(cond, msg):
    if not cond:
        fails.append(msg)


def walk_blocks(blocks, out):
    """Every block, recursing into groups and cascade beats."""
    for b in blocks or []:
        out.append(b)
        props = b.get("props") or {}
        walk_blocks(b.get("blocks"), out)
        for beat in props.get("beats", []) or []:
            walk_blocks(beat.get("blocks"), out)
    return out


def all_blocks(nodes):
    out = []
    for n in nodes or []:
        walk_blocks(n.get("blocks"), out)
    return out


def text_of(canvas):
    return " ".join(str(b.get("content", "")) for b in all_blocks(canvas.get("nodes", [])))


def cond_items(conditions):
    return (conditions or {}).get("items", []) if isinstance(conditions, dict) else []


def has_flag(items, key, op):
    return any(i.get("type") == "flag" and i.get("flag_key") == key and i.get("operator") == op for i in items)


def node(canvas, node_id):
    return next((n for n in canvas.get("nodes", []) if n.get("id") == node_id), None)


def study_night_checks(canvases, cards, cid, tag, prev_flag, sets, image, must_say):
    """A study night: one-shot auto-fire at the Site, Kess AND Cain present as conditions, gated on the night
    before (or cradles_ready) and on its own flag is_false, sets its flag, 360 minutes out, one image, and its
    flag is a goal on card M."""
    c = canvases.get(cid)
    check(c is not None, f"{tag}: {cid} is missing")
    if not c:
        return
    tr = c.get("trigger") or {}
    check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and tr.get("priority") == 11,
          f"{tag}: {cid} is a one-shot auto-fire at the_site, pri 11")
    its = cond_items(tr.get("conditions"))
    check((tr.get("conditions") or {}).get("version") == "1.0", f"{tag}: {cid} conditions need version 1.0")
    check(has_flag(its, prev_flag, "is_true") and has_flag(its, sets, "is_false"), f"{tag}: gated {prev_flag} + {sets} is_false")
    for who in ("npc_kess", "npc_cain"):
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == who and i.get("location_id") == "the_site"
                  and i.get("operator") == "is_present" for i in its), f"{tag}: {cid} needs {who} present at the_site")
    cfg = (((c.get("nodes") or [{}])[0].get("exit_block")) or {}).get("config") or {}
    check(cfg.get("locationId") == "the_site" and cfg.get("time_progression_minutes") == 360, f"{tag}: exits to the_site after 360 min")
    check({"targetType": "player", "flag": sets, "op": "set"} in (cfg.get("flagEffects") or []), f"{tag}: sets {sets}")
    imgs = [(b.get("props") or {}).get("file") for b in all_blocks(c.get("nodes")) if b.get("type") == "image"]
    check(imgs == [image], f"{tag}: one image {image}, found {imgs}")
    txt = text_of(c).lower()
    for w in must_say:
        check(w in txt, f"{tag}: {cid} never says '{w}'")
    m = [k for k in cards if not k.get("npc_id") and {"flag": "cradles_ready", "op": "is_true"} in k.get("when", [])]
    check(m and any(g.get("flag") == sets and g.get("op") == "is_true" for g in m[0].get("goals", [])),
          f"{tag}: card M lists {sets} as a goal")


def run_link_checks(canvases, cid, tag, prev_flag, sets, minutes, images, must_say, presence=False,
                    where="the_site", exit_to="the_site", needs=()):
    """A link of THE RUN: one-shot auto-fire at the Site, pri 11, gated prev_flag + its own flag is_false, exits to
    the_site with the stated minutes, sets its flag, carries exactly its images. Presence gates only on link 1."""
    c = canvases.get(cid)
    check(c is not None, f"{tag}: {cid} is missing")
    if not c:
        return None
    tr = c.get("trigger") or {}
    check(tr.get("location") == where and tr.get("is_repeatable") is False and tr.get("priority") == 11,
          f"{tag}: {cid} is a one-shot auto-fire at {where}, pri 11 (got {tr.get('location')})")
    its = cond_items(tr.get("conditions"))
    check((tr.get("conditions") or {}).get("version") == "1.0", f"{tag}: {cid} conditions need version 1.0")
    check(has_flag(its, prev_flag, "is_true") and has_flag(its, sets, "is_false"), f"{tag}: gated {prev_flag} + {sets} is_false")
    for f in needs:
        check(has_flag(its, f, "is_true"), f"{tag}: {cid} also needs {f}")
    pres = [i for i in its if i.get("type") == "npc_at_location"]
    if presence is None:
        pass            # the caller checks its own presence gate (e.g. Sabin's look)
    elif presence:
        for who in ("npc_kess", "npc_cain"):
            check(any(i.get("npc_id") == who and i.get("operator") == "is_present" for i in pres), f"{tag}: {cid} needs {who} present")
    else:
        check(not pres, f"{tag}: {cid} is a later link of the run and must carry NO presence gate (the beat_0222 pattern)")
    cfg = (((c.get("nodes") or [{}])[-1].get("exit_block")) or {}).get("config") or {}
    check(cfg.get("locationId") == exit_to and cfg.get("time_progression_minutes") == minutes,
          f"{tag}: exits to {exit_to} after {minutes} min, got {cfg.get('locationId')} / {cfg.get('time_progression_minutes')}")
    check({"targetType": "player", "flag": sets, "op": "set"} in (cfg.get("flagEffects") or []), f"{tag}: sets {sets}")
    imgs = sorted((b.get("props") or {}).get("file") for b in all_blocks(c.get("nodes")) if b.get("type") in ("image", "video"))
    check(imgs == sorted(images), f"{tag}: media should be {sorted(images)}, found {imgs}")
    txt = text_of(c).lower()
    for w in must_say:
        check(w.lower() in txt, f"{tag}: {cid} never says '{w}'")
    return c


def cascade_beats(canvas):
    """Every cascade beat in the canvas, as (advance_text, blocks)."""
    out = []
    for b in all_blocks(canvas.get("nodes", [])):
        for beat in ((b.get("props") or {}).get("beats") or []) if b.get("type") == "cascade" else []:
            out.append((beat.get("advance_text", ""), beat.get("blocks") or []))
    return out


def beat_text(blocks):
    return " ".join(str(b.get("content", "")) for b in walk_blocks(blocks, []))


def explicit_scene_checks(canvas, tag, clips, min_explicit_beats):
    """Explicit scene: every beat carrying a clip has 3+ frozen-list words; at least N explicit beats; every clip is
    a single file (one-time screen); no anal anywhere (the signed ceiling holds it out)."""
    beats = cascade_beats(canvas)
    vids = []
    n_explicit = 0
    for adv, blocks in beats:
        txt = beat_text(blocks)
        k = len(EXPLICIT.findall(txt))
        has_clip = any(b.get("type") == "video" for b in blocks)
        if k >= 3:
            n_explicit += 1
        if has_clip:
            check(k >= 3, f"{tag}: the clip beat '{adv}' carries only {k} frozen-list words (needs 3+)")
        for b in blocks:
            if b.get("type") == "video":
                pr = b.get("props") or {}
                vids.append(pr.get("file"))
                check(pr.get("file") and not pr.get("pool_dir"), f"{tag}: a one-time explicit beat carries one file, not a pool")
    check(sorted(v for v in vids if v) == sorted(clips), f"{tag}: clips should be {sorted(clips)}, found {sorted(v for v in vids if v)}")
    check(n_explicit >= min_explicit_beats, f"{tag}: needs {min_explicit_beats}+ explicit beats (3+ words), has {n_explicit}")
    alltxt = text_of(canvas).lower()
    check(not re.search(r"\banal\b|\bin her ass\b|\bher ass open", alltxt), f"{tag}: anal is held out by the signed ceiling")
    return beats


# ── THE VEGA MAP — what is true in every save while Wren wears Vega (beat_0248). ──────────────────────────────
# Flags known true / false once the transfer has happened. Anything not listed is UNKNOWN and treated as possibly
# true, so the walk below over-approximates what Vega can reach and what can render there: it can only fail loud.
VEGA_TRUE = {"in_vega", "rise_door", "transferred", "cradles_ready", "vega_dismantled", "vega_taken", "vega_plan",
             "crew_back", "study_blade", "study_signal", "study_method", "last_night_held", "marrow_known", "site_offered",
             "the_site_open", "archive_1a_done", "rise_named", "salvage_entered", "salvage_relaunched", "sabin_met",
             "sabin_consulted", "seam_known", "opening_done", "wall_understood", "face_bought",
             # beat_0250: the strip is on Vega's map now. The 0.2.3 ambush on it (cap_the_ambush) sets site_ambushed, and
             # the hunt that ends in cradles_ready comes after it, so every save that reaches the transfer has it.
             "site_ambushed"}
VEGA_FALSE = {"face_worn", "back_in_body", "memory_whole", "cain_chosen", "dev_mode_enabled"}
VEGA_TRAITS = {"vega_records": 9}
# Surfaces that are written for Vega without an in_vega gate (their own flags only exist in Vega), or that are
# body-neutral. Each one is read by a human; adding to this list is a claim that the prose is true for Vega.
VEGA_OK = {"activity_leave_the_rise": "the lift and the desk, no body named",
           "activity_leave_the_lab": "the way out of the lab, no body named",
           "cap_lyra_and_nova": "memory_taken only ever sets in Vega",
           "cap_dace_falls": "units_fought only ever sets in Vega",
           "cap_back_in_body": "the homecoming, written for leaving Vega"}


def may_pass(conditions):
    """Can these v1.0 conditions be true while Wren is in Vega? False only when a KNOWN state contradicts them."""
    if not conditions or conditions.get("version") != "1.0":
        return True
    items = conditions.get("items", [])
    def one(i):
        if i.get("type") == "flag":
            k, op = i.get("flag_key"), i.get("operator")
            if k in VEGA_TRUE:
                return op == "is_true"
            if k in VEGA_FALSE:
                return op == "is_false"
            return True
        if i.get("type") == "trait" and i.get("trait_key") in VEGA_TRAITS:
            v, op, x = VEGA_TRAITS[i["trait_key"]], i.get("operator"), i.get("value")
            return {"gte": v >= x, "gt": v > x, "lt": v < x, "lte": v <= x, "eq": v == x, "ne": v != x}.get(op, True)
        return True
    res = [one(i) for i in items]
    return any(res) if conditions.get("logic") == "OR" else all(res)


def vega_gated(trigger):
    return any(i.get("type") == "flag" and i.get("flag_key") == "in_vega" for i in cond_items(trigger.get("conditions")))


def vega_reach(t):
    """Locations Vega can stand in: nav (parent <-> child, navigation_order) through locks that may pass, plus every
    teleport (choice locationId, exit config locationId) on a card that may render at a reached place."""
    locs = {l["id"]: l for l in t.get("locations", [])}
    nbr = {k: set() for k in locs}
    for k, l in locs.items():
        par = l.get("entry_from") or l.get("parent")
        if par in locs:
            nbr[k].add(par); nbr[par].add(k)
        for c in l.get("navigation_order", []) or []:
            if c in locs:
                nbr[k].add(c)
    by_loc = {}
    for c in t.get("canvases", []):
        tr = c.get("trigger") or {}
        by_loc.setdefault(tr.get("location"), []).append(c)
    seen, todo = set(), ["the_site"]
    while todo:
        k = todo.pop()
        if k in seen:
            continue
        seen.add(k)
        for n in nbr.get(k, ()):
            if n not in seen and may_pass(locs[n].get("entry_conditions")):
                todo.append(n)
        for c in by_loc.get(k, []):
            if c["id"].startswith("dev_jump") or not may_pass((c.get("trigger") or {}).get("conditions")):
                continue
            for nd in c.get("nodes", []):
                eb = nd.get("exit_block") or {}
                tgts = [ch.get("locationId") for ch in eb.get("choices", []) if may_pass(ch.get("conditions"))]
                tgts.append((eb.get("config") or {}).get("locationId"))
                for x in tgts:
                    if x in locs and x not in seen:
                        todo.append(x)
    return seen, by_loc


def main():
    t = tomllib.load(open(GAME, "rb"))
    core = (t.get("player") or {}).get("core_traits") or {}
    labels = {l.get("key"): l for l in (t.get("traits") or {}).get("labels", [])}
    npcs = {n["id"]: n for n in t.get("npcs", [])}
    canvases = {c["id"]: c for c in t.get("canvases", [])}
    cards = t.get("quest_cards", [])

    # ── beat_0224 — the numbers, Kess's Site row, activity_read_vega, card M ──────────────────────────
    # 1. vega_records is declared at 0 (the cross-release backfill initialises core_traits, so a 0.2.3 save
    #    loads it as 0 rather than undefined, and every gte on an undefined trait is false) and hidden.
    check(core.get("vega_records") == 0, f"0224: vega_records must be declared in core_traits at 0, got {core.get('vega_records')!r}")
    check(labels.get("vega_records", {}).get("hidden") is True, "0224: vega_records must be hidden from the traits dump")

    # 2. Kess's Site row: 22:00-23:59 (after his berth row, never across midnight), gated v1.0 on cradles_ready
    #    + back_in_body is_false. The berth row is unchanged.
    rows = (npcs.get("npc_kess") or {}).get("schedules", [])
    berth = [r for r in rows if r.get("location") == "kess_berth"]
    site = [r for r in rows if r.get("location") == "the_site"]
    check(len(berth) == 1 and berth[0].get("start_time") == "10:00" and berth[0].get("end_time") == "22:00",
          "0224: Kess's berth row must stay 10:00-22:00")
    check(len(site) == 1, f"0224: Kess needs exactly one the_site row, has {len(site)}")
    if site:
        r = site[0]
        check(r.get("start_time") == "22:00" and r.get("end_time") == "23:59", "0224: Kess's Site row is 22:00-23:59")
        w = r.get("when") or {}
        check(w.get("version") == "1.0", "0224: Kess's Site row `when` needs version 1.0 or it fails OPEN")
        check(has_flag(cond_items(w), "cradles_ready", "is_true") and has_flag(cond_items(w), "back_in_body", "is_false"),
              "0224: Kess's Site row gated cradles_ready + back_in_body is_false")

    # 3. activity_read_vega: solo, repeatable, twice a day, gated cradles_ready + transferred is_false; the read
    #    costs 15 Charge, adds 1 capped at 9, is offered only under 9; the result exits to the Site with 60 min;
    #    unlock screens at exactly 3, 6 and 9.
    a = canvases.get("activity_read_vega")
    check(a is not None, "0224: activity_read_vega is missing")
    if a:
        tr = a.get("trigger") or {}
        check(tr.get("location") == "the_site" and tr.get("is_repeatable") is True, "0224: read card is a repeatable card at the_site")
        check(not tr.get("npc") and not tr.get("requires_npc"), "0224: read card is Wren-solo (Cain's card here is activity_cain_trains)")
        check(tr.get("max_triggers_per_day") == 2, "0224: read card is capped at 2 a day")
        its = cond_items(tr.get("conditions"))
        check((tr.get("conditions") or {}).get("version") == "1.0", "0224: read card conditions need version 1.0")
        check(has_flag(its, "cradles_ready", "is_true") and has_flag(its, "transferred", "is_false"),
              "0224: read card gated cradles_ready + transferred is_false")
        base = node(a, "base")
        chs = ((base or {}).get("exit_block") or {}).get("choices", [])
        read = [c for c in chs if c.get("nodeId") == "activity_read_vega.read"]
        check(len(read) == 1, "0224: one 'read' choice on the base node")
        if read:
            c = read[0]
            check({"trait": "energy", "value": 15} in (c.get("costs") or []), "0224: a read costs 15 Charge (gated + deducted)")
            eff = [e for e in c.get("effects", []) if e.get("trait") == "vega_records"]
            check(eff and eff[0].get("op") == "add" and eff[0].get("value") == 1 and eff[0].get("cap") == 9 and eff[0].get("clamp") is True,
                  "0224: a read adds 1 to vega_records, clamped at 9")
            ci = cond_items(c.get("conditions"))
            check(any(i.get("trait_key") == "vega_records" and i.get("operator") == "lt" and i.get("value") == 9 for i in ci),
                  "0224: the read is offered only while vega_records < 9")
        check(any(c.get("targetType") == "location" and c.get("locationId") == "the_site" for c in chs),
              "0224: the base node has a way out")
        rn = node(a, "read")
        check(rn is not None, "0224: the read result node is missing")
        if rn:
            cfg = ((rn.get("exit_block") or {}).get("config")) or {}
            check(cfg.get("locationId") == "the_site" and cfg.get("time_progression_minutes") == 60,
                  "0224: the read exits to the_site after 60 minutes")
            eqs = sorted(i.get("value") for b in walk_blocks(rn.get("blocks"), []) if b.get("type") == "group"
                         for i in cond_items((b.get("props") or {}).get("conditions"))
                         if i.get("trait_key") == "vega_records" and i.get("operator") == "eq")
            check(eqs == [3, 6, 9], f"0224: unlock screens at exactly 3, 6 and 9, found {eqs}")
        imgs = [(b.get("props") or {}).get("file") for b in all_blocks(a.get("nodes")) if b.get("type") == "image"]
        check(imgs == ["scenes/vega_records.jpg"], f"0224: one image, scenes/vega_records.jpg, found {imgs}")

    # 4. Card M (the study) is the live cradles_ready Story-Goals card, NOT terminal, gated last_night_held is_false,
    #    and carries the records goal at 9.
    m = [c for c in cards if not c.get("npc_id") and {"flag": "cradles_ready", "op": "is_true"} in c.get("when", [])]
    check(len(m) == 1, f"0224: one Story-Goals card on cradles_ready (M), found {len(m)}")
    if m:
        m = m[0]
        check(not m.get("terminal"), "0224: card M is not terminal")
        check({"flag": "last_night_held", "op": "is_false"} in m.get("when", []), "0224: card M closes at last_night_held")
        check(any(g.get("trait") == "vega_records" and g.get("op") == "gte" and g.get("value") == 9 for g in m.get("goals", [])),
              "0224: card M has the records goal at 9")

    # ── beat_0225 — cap_study_blade (study night 1) ─────────────────────────────────────────────────────
    study_night_checks(canvases, cards, "cap_study_blade", "0225", prev_flag="cradles_ready", sets="study_blade",
                       image="scenes/study_the_blade.jpg", must_say=["blade", "knife"])

    # ── beat_0226 — cap_study_signal (study night 2) ────────────────────────────────────────────────────
    study_night_checks(canvases, cards, "cap_study_signal", "0226", prev_flag="study_blade", sets="study_signal",
                       image="scenes/study_the_signal.jpg", must_say=["calling home", "not long if you fight"])

    # ── beat_0227 — cap_study_method (study night 3) + card M's ready_text ──────────────────────────────
    study_night_checks(canvases, cards, "cap_study_method", "0227", prev_flag="study_signal", sets="study_method",
                       image="scenes/study_the_method.jpg", must_say=["neck", "count"])
    sm = canvases.get("cap_study_method")
    if sm:
        # The making has no faces: the scene may not name Cain or Marrow as one of the people in it.
        txt = text_of(sm).lower()
        for bad in ("marrow did this", "cain did", "it was cain", "it was you"):
            check(bad not in txt, f"0227: the method scene gives away the third piece ('{bad}')")
    m = [k for k in cards if not k.get("npc_id") and {"flag": "cradles_ready", "op": "is_true"} in k.get("when", [])]
    if m:
        check(bool(m[0].get("ready_text")), "0227: card M carries a ready_text (the engine hides goals once all are met)")
        check(len(m[0].get("goals", [])) == 4, f"0227: card M has four goals (records + three nights), has {len(m[0].get('goals', []))}")

    # ── beat_0228 — cap_last_night ──────────────────────────────────────────────────────────────────────
    ln = canvases.get("cap_last_night")
    check(ln is not None, "0228: cap_last_night is missing")
    if ln:
        tr = ln.get("trigger") or {}
        its = cond_items(tr.get("conditions"))
        check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and tr.get("priority") == 11,
              "0228: one-shot auto-fire at the_site, pri 11")
        check(has_flag(its, "study_method", "is_true") and has_flag(its, "last_night_held", "is_false"),
              "0228: gated study_method + last_night_held is_false")
        check(any(i.get("trait_key") == "vega_records" and i.get("operator") == "gte" and i.get("value") == 9 for i in its),
              "0228: gated vega_records gte 9")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_cain" and i.get("operator") == "is_present" for i in its),
              "0228: Cain present")
        check(not any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_kess" for i in its),
              "0228: Kess is NOT gated (the scene sends him to sleep)")
        cfg = (((ln.get("nodes") or [{}])[0].get("exit_block")) or {}).get("config") or {}
        check(cfg.get("time_progression_minutes") == 540 and cfg.get("locationId") == "the_site", "0228: 540 min, back to the_site")
        check({"targetType": "player", "flag": "last_night_held", "op": "set"} in (cfg.get("flagEffects") or []), "0228: sets last_night_held")
        txt = text_of(ln).lower()
        check("scared" in txt, "0228: she says she is afraid")
        for w in ("cock", "cunt", "fuck", "naked", "kiss"):
            check(w not in txt, f"0228: no sex on the last night (found '{w}')")
        imgs = [(b.get("props") or {}).get("file") for b in all_blocks(ln.get("nodes")) if b.get("type") == "image"]
        check(imgs == ["scenes/last_night_cain.jpg"], f"0228: one image scenes/last_night_cain.jpg, found {imgs}")

    # ── beat_0229 — cap_the_transfer (the run, link 1) ──────────────────────────────────────────────────
    tf = run_link_checks(canvases, "cap_the_transfer", "0229", "last_night_held", "transferred", 480,
                         ["scenes/the_transfer.jpg", "scenes/wren_wakes_in_vega.jpg"],
                         ["neck", "blade", "still scared", "vega's voice"], presence=True)
    if tf:
        for w in ("cock", "cunt", "fuck me harder", "naked"):
            check(w not in text_of(tf).lower(), f"0229: no sex in Vega's body (found '{w}')")
    # The read card and the cradles card close or stay out of the way once she is in Vega: the read card is gated
    # transferred is_false (checked at §0224); the run's links outrank the solo cards (pri 11 over 3).

    # ── beat_0240-0246 — THE PLAYER PLAYS VEGA (LO 2026-10-13). The Rise as player cards, the rest re-hosted. ──
    # The transfer drops into free play as Vega.
    if tf:
        cfg = (((tf.get("nodes") or [{}])[-1].get("exit_block")) or {}).get("config") or {}
        fl = {f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}
        check(fl.get("in_vega") == "set" and fl.get("rise_door") == "set" and fl.get("face_worn") == "unset",
              "0240: the transfer sets in_vega + rise_door and takes the bought face off")
        eff = {e.get("trait"): (e.get("op"), e.get("value")) for e in cfg.get("effects", [])}
        check(eff.get("vega_cell") == ("set", 100), "0240: the transfer fills Vega's cell")
    lab = canvases.get("activity_vega_lab")
    check(lab is not None, "0243: activity_vega_lab is missing")
    if lab:
        tr = lab.get("trigger") or {}
        its = cond_items(tr.get("conditions"))
        check(tr.get("location") == "the_rise_floor" and tr.get("is_repeatable") is True, "0243: the lab card is a repeatable card on the Rise floor")
        check(has_flag(its, "in_vega", "is_true") and has_flag(its, "rise_slip", "is_false"), "0243: lab card gated in_vega + rise_slip is_false")
        up = [c for c in ((node(lab, "base") or {}).get("exit_block") or {}).get("choices", []) if c.get("nodeId") == "activity_vega_lab.lab"]
        check(up and up[0].get("show_when_locked") and any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_sabin"
              and i.get("location_id") == "the_rise_floor" and i.get("operator") == "is_present" for i in cond_items(up[0].get("conditions"))),
              "0243: up to the lab only while Sabin is downstairs on the floor, shown locked otherwise")
        ln = node(lab, "lab") or {}
        cfg = (ln.get("exit_block") or {}).get("config") or {}
        check({"targetType": "player", "flag": "rise_slip", "op": "set"} in (cfg.get("flagEffects") or []), "0243: the lab sets rise_slip")
        check("until eleven" in text_of(lab) and "Vance Tower" in text_of(lab), "0243: the lab says why it is empty and where the slip points")
    top = canvases.get("activity_vega_top_floors")
    check(top is not None, "0243: activity_vega_top_floors is missing")
    if top:
        ch = [c for c in ((node(top, "base") or {}).get("exit_block") or {}).get("choices", []) if c.get("nodeId") == "activity_vega_top_floors.top"]
        check(ch and {"trait": "vega_cell", "value": 10} in (ch[0].get("costs") or []), "0243: the top floors cost 10 of Vega's cell")
        cfg = ((node(top, "top") or {}).get("exit_block") or {}).get("config") or {}
        check({"targetType": "player", "flag": "rise_line_seen", "op": "set"} in (cfg.get("flagEffects") or []), "0243: the top floors set rise_line_seen")
        check("eleven thousand" in text_of(top), "0243: the line is Sabin's eleven thousand")
    sn = run_link_checks(canvases, "cap_sabin_notices", "0243", "rise_line_seen", "rise_searched", 10,
                         ["scenes/sabin_looks.jpg"], ["never look at anybody", "make a note"],
                         where="the_rise_floor", exit_to="spire_plaza", needs=("in_vega", "rise_slip"), presence=None)
    if sn:
        its = cond_items((sn.get("trigger") or {}).get("conditions"))
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_sabin" and i.get("operator") == "is_present" for i in its),
              "0243: Sabin's look needs him present on the floor")
        for bad in ("transfer works", "it's wren", "you're wren"):
            check(bad not in text_of(sn).lower(), f"0243: Sabin must not learn the transfer works ('{bad}')")
    check("cap_the_rise" not in canvases, "0243: the old auto-fire cap_the_rise is gone (the Rise is played, not watched)")
    tp = run_link_checks(canvases, "cap_tower_plan", "0244", "rise_searched", "tower_planned", 60,
                         ["scenes/the_tower_plan.jpg"], ["Waterfront", "vault", "eleven thousand"], presence=True, needs=("in_vega",))
    if tp:
        txt = text_of(tp).lower()
        for bad in ("if you're late", "if you are late", "call us", "we'll come in", "signal us", "by three"):
            check(bad not in txt, f"0244: the plan sets no hour and no rescue pact ('{bad}')")
    vt = run_link_checks(canvases, "cap_the_vault", "0245", "tower_planned", "memory_taken", 30,
                         ["scenes/the_blade_in_the_tower.jpg", "scenes/vance_tower_vault.jpg"],
                         ["no number on the panel", "alarm", "blade", "Don't open it"], where="chairmans_floor", exit_to="spire_plaza", needs=("in_vega",))
    if vt:
        base_ch = [c.get("nodeId") or c.get("locationId") for c in ((node(vt, "base") or {}).get("exit_block") or {}).get("choices", [])]
        check(sorted(base_ch) == ["atrium", "cap_the_vault.blade", "cap_the_vault.wait"], f"0245: the door: blade / wait / go back down, found {base_ch}")
        wait_ch = [c.get("nodeId") or c.get("locationId") for c in ((node(vt, "wait") or {}).get("exit_block") or {}).get("choices", [])]
        check(sorted(wait_ch) == ["atrium", "cap_the_vault.blade"], f"0245: waiting ends at the blade or back down, found {wait_ch}")
        for nid in ("base", "wait"):
            bl = [c for c in ((node(vt, nid) or {}).get("exit_block") or {}).get("choices", []) if c.get("nodeId") == "cap_the_vault.blade"]
            check(bl and {"trait": "vega_cell", "value": 30} in (bl[0].get("costs") or []) and bl[0].get("show_when_locked"),
                  f"0245: the blade at .{nid} costs 30 of the cell and shows locked when she can't afford it")
        txt = text_of(vt)
        check("npc_chairman" not in txt and "the chairman says" not in txt.lower(), "0245: the Chairman is never on screen")
        check("At midnight" not in txt and "by three" not in txt, "0245: no clock hour the player's own timing can make false")
    ln5 = run_link_checks(canvases, "cap_lyra_and_nova", "0246", "memory_taken", "units_fought", 120,
                          ["scenes/lyra_and_nova.jpg", "scenes/vega_breaking.jpg"],
                          ["Lyra and Nova", "signal off", "no pain", "Waterfront"], where="spire_plaza", exit_to="spire_plaza")
    if ln5:
        check(not any(n in npcs for n in ("npc_lyra", "npc_nova")), "0246: Lyra and Nova have no NPC entries")
        check(not [b for b in all_blocks(ln5.get("nodes")) if b.get("type") == "dialog"], "0246: Lyra and Nova do not speak")
        check("three o'clock" not in text_of(ln5).lower(), "0246: no clock hour in the fight")
    df = run_link_checks(canvases, "cap_dace_falls", "0246", "units_fought", "dace_dead", 210,
                         ["scenes/the_seam_again.jpg", "scenes/dace_falls.jpg"],
                         ["seam", "Nobody called them", "Let them go", "coffins"], where="spire_plaza", exit_to="the_site")
    if df:
        spk = {(b.get("props") or {}).get("npcId") for b in all_blocks(df.get("nodes")) if b.get("type") == "dialog"}
        check({"npc_dace", "npc_cain", "npc_bastien"} <= spk, f"0246: Dace, Cain and Bastien all speak, found {spk}")
    # Truth sweep: the cot hub's band chain gets a dace_dead band AFTER the face band and BEFORE the cradles band
    # (first match wins), and no Bastien line after dace_dead speaks of Dace in the present tense.
    cot = canvases.get("amb_bastien_cot")
    if cot:
        groups = [b for b in (node(cot, "base") or {}).get("blocks", []) if b.get("type") == "group"]
        keys = []
        for g in groups:
            its = cond_items((g.get("props") or {}).get("conditions"))
            keys.append(its[0].get("flag_key") if its else None)
        check("dace_dead" in keys, "0234: amb_bastien_cot has a dace_dead band")
        if "dace_dead" in keys and "cradles_ready" in keys:
            check(keys.index("face_worn") < keys.index("dace_dead") < keys.index("cradles_ready"),
                  f"0234: band order face_worn < dace_dead < cradles_ready, found {keys[:4]}")
            dd = groups[keys.index("dace_dead")]
            check("Dace is very good" not in " ".join(str(b.get("content", "")) for b in walk_blocks(dd.get("blocks"), [])),
                  "0234: the dace_dead band does not call Dace good in the present tense")
    b27 = [c for c in cards if c.get("npc_id") == "npc_bastien" and {"flag": "dace_dead", "op": "is_true"} in c.get("when", [])]
    check(len(b27) == 1 and b27[0].get("terminal") is True and b27[0].get("priority", 0) > 26,
          "0234: Bastien card 27 on dace_dead, terminal, above card 26")
    if b27:
        check("'" not in (b27[0].get("terminal_text") or ""), "0234: no apostrophe in terminal_text")

    # ── beat_0235 — cap_back_in_body (the run, link 7) ──────────────────────────────────────────────────
    bb = run_link_checks(canvases, "cap_back_in_body", "0235", "dace_dead", "back_in_body", 30,
                         ["scenes/back_in_her_body.jpg"], ["my own hands", "seats it"])
    if bb:
        txt = text_of(bb)
        # LO's order: back into her body FIRST, then the memory goes in.
        check(txt.find("my own hands") < txt.find("seats it"), "0235: she is back in her body before the memory is seated (LO's order)")
        for w in ("cock", "cunt", "fuck me", "naked"):
            check(w not in txt.lower(), f"0235: no sex in the homecoming (found '{w}')")

    # ── beat_0236 — cap_the_whole_memory (the run, link 8, THE FLASHBACK, explicit) ────────────────────
    wm = canvases.get("cap_the_whole_memory")
    check(wm is not None, "0236: cap_the_whole_memory is missing")
    if wm:
        tr = wm.get("trigger") or {}
        its = cond_items(tr.get("conditions"))
        check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and tr.get("priority") == 11, "0236: one-shot auto-fire at the_site, pri 11")
        check(has_flag(its, "back_in_body", "is_true") and has_flag(its, "memory_whole", "is_false"), "0236: gated back_in_body + memory_whole is_false")
        check(not [i for i in its if i.get("type") == "npc_at_location"], "0236: no presence gate (the run)")
        cfg = (((wm.get("nodes") or [{}])[0].get("exit_block")) or {}).get("config") or {}
        check({"targetType": "player", "flag": "memory_whole", "op": "set"} in (cfg.get("flagEffects") or []), "0236: sets memory_whole")
        beats = explicit_scene_checks(wm, "0236", ["sex/flashback_cain_kiss_t4.webm", "sex/flashback_cain_blowjob_t5.webm",
                                                   "sex/flashback_cain_fuck_t5.webm"], 6)
        txt = text_of(wm)
        check("twenty-four" in txt, "0236: she is an adult on the page (twenty-four)")
        for w in ("Vesper", "her father", "Cain's hands holding her down", "None of us can be left"):
            check(w.lower() in txt.lower(), f"0236: the memory must give back '{w}'")
        # THE SEX IS THE LOVE, NEVER THE LAB: no beat carries both a lab word and 3+ explicit words.
        for adv, blocks in beats:
            bt = beat_text(blocks).lower()
            if len(EXPLICIT.findall(bt)) >= 3:
                for lab in ("cradle", "the lab", "lines are in her neck", "counting", "opening her"):
                    check(lab not in bt, f"0236: explicit beat '{adv}' mentions the making ('{lab}')")
        spk = {(b.get("props") or {}).get("speaker") for b in all_blocks(wm.get("nodes")) if b.get("type") == "dialog"}
        check("unknown" not in spk, "0236: Marrow is quoted in narration, never a 'Stranger:' line")

    # ── beat_0237 — cap_cain_for_real (the run, last link, explicit) + end card O ──────────────────────
    cf = canvases.get("cap_cain_for_real")
    check(cf is not None, "0237: cap_cain_for_real is missing")
    if cf:
        tr = cf.get("trigger") or {}
        its = cond_items(tr.get("conditions"))
        check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and tr.get("priority") == 11, "0237: one-shot auto-fire at the_site, pri 11")
        check(has_flag(its, "memory_whole", "is_true") and has_flag(its, "cain_chosen", "is_false"), "0237: gated memory_whole + cain_chosen is_false")
        check(not [i for i in its if i.get("type") == "npc_at_location"], "0237: no presence gate (the run)")
        cfg = (((cf.get("nodes") or [{}])[0].get("exit_block")) or {}).get("config") or {}
        check(cfg.get("time_progression_minutes") == 540 and cfg.get("locationId") == "the_site", "0237: 540 min, back to the_site")
        check({"targetType": "player", "flag": "cain_chosen", "op": "set"} in (cfg.get("flagEffects") or []), "0237: sets cain_chosen")
        explicit_scene_checks(cf, "0237", ["sex/cain_for_real_kiss_t4.webm", "sex/cain_for_real_fuck_t5.webm",
                                           "sex/cain_for_real_finish_t5.webm"], 6)
        txt = text_of(cf)
        check("I'm choosing you anyway" in txt, "0237: the choice is said in dialogue (legible)")
        check("nine years" not in txt, "0237: no year count (Grier's nine and Bastien's eleven do not agree)")
        beats = cascade_beats(cf)
        last = beat_text(beats[-1][1]) if beats else ""
        check(len(EXPLICIT.findall(last)) < 3, "0237: the meaning beat comes after the body, not folded into it (the pivot rule)")
    o = [c for c in cards if not c.get("npc_id") and c.get("terminal") and {"flag": "cain_chosen", "op": "is_true"} in c.get("when", [])]
    check(len(o) == 1, "0237: one terminal end card O on cain_chosen")
    terms = [c for c in cards if not c.get("npc_id") and c.get("terminal")]
    check(len(terms) == 1, f"0237: exactly one terminal Story-Goals card in the game, found {len(terms)}")
    if o:
        check("'" not in (o[0].get("terminal_text") or ""), "0237: no apostrophe in terminal_text")
        check("That is where this build ends" in (o[0].get("tip") or ""), "0237: the end card says where the build ends")

    # ── beat_0238 — what stands after: site_the_cradles bands, Cain's band, Kess's Site card, the wreck ─────
    sc = canvases.get("site_the_cradles")
    if sc:
        blocks = (node(sc, "base") or {}).get("blocks", [])
        kinds = ["G" if b.get("type") == "group" else "x" for b in blocks]
        check("".join(kinds) == "GGxGGGG", f"0238: site_the_cradles is two chains split by one ungrouped line, found {''.join(kinds)}")
        g = [b for b in blocks if b.get("type") == "group"]
        firsts = [cond_items((x.get("props") or {}).get("conditions")) for x in g]
        check(has_flag(firsts[0], "back_in_body", "is_false") and has_flag(firsts[1], "back_in_body", "is_true"),
              "0238: chain 1 is the shell (until back_in_body) then the empty cradle")
        imgs = [(b.get("props") or {}).get("file") for b in walk_blocks(g[0].get("blocks"), []) if b.get("type") == "image"]
        check(imgs == ["scenes/the_shell_in_the_cradle.jpg"], "0238: the shell image shows only while the shell is there")
        check(sum(1 for f in firsts if has_flag(f, "cain_chosen", "is_true")) == 2, "0238: two cain_chosen bands (present / absent)")
        txt = text_of(sc)
        check("Kess took what was left of Vega" in txt, "0238: the after band says where the shell went")
    ct = canvases.get("activity_cain_trains")
    if ct:
        g = [b for b in (node(ct, "base") or {}).get("blocks", []) if b.get("type") == "group"]
        first = cond_items((g[0].get("props") or {}).get("conditions")) if g else []
        check(has_flag(first, "cain_chosen", "is_true"), "0238: Cain's card opens its chain on cain_chosen (first match wins)")
    ks = canvases.get("activity_kess_site")
    check(ks is not None, "0238: activity_kess_site (Kess's face at the Site) is missing")
    if ks:
        tr = ks.get("trigger") or {}
        check(tr.get("npc") == "npc_kess" and tr.get("requires_npc") == "npc_kess" and tr.get("location") == "the_site"
              and tr.get("is_repeatable") is True, "0238: Kess's Site card is his portrait hub at the_site")
        its = cond_items(tr.get("conditions"))
        check(has_flag(its, "cradles_ready", "is_true") and has_flag(its, "back_in_body", "is_false"), "0238: it lives exactly as long as his Site row")
    kw = canvases.get("kess_the_wreck")
    check(kw is not None, "0238: kess_the_wreck is missing")
    if kw:
        tr = kw.get("trigger") or {}
        check(tr.get("location") == "kess_berth" and tr.get("is_repeatable") is True and not tr.get("npc") and not tr.get("requires_npc"),
              "0238: the wreck is a solo repeatable card at kess_berth (hub_kess_berth is his card there)")
        check(has_flag(cond_items(tr.get("conditions")), "back_in_body", "is_true"), "0238: the wreck is there from back_in_body")
        imgs = [(b.get("props") or {}).get("file") for b in all_blocks(kw.get("nodes")) if b.get("type") == "image"]
        check(imgs == ["scenes/the_wreck_on_the_table.jpg"], "0238: one image, the wreck on the table")
        for bad in ("next release", "0.2.5", "tomorrow"):
            check(bad not in text_of(kw).lower(), f"0238: the wreck card promises no date ('{bad}')")

    # ── beat_0239 — dev_jump_transfer_start (LO: "click on the end of 0.2.3 and start this new release") ──
    dj = canvases.get("dev_jump_transfer_start")
    check(dj is not None, "0239: dev_jump_transfer_start is missing")
    if dj:
        check(has_flag(cond_items((dj.get("trigger") or {}).get("conditions")), "dev_mode_enabled", "is_true"), "0239: the jump is dev-only")
        ch = ((dj.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        check(ch[0].get("locationId") == "the_site", "0239: the jump lands at the Site")
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("vega_taken", "vega_dismantled", "vega_plan", "crew_back", "cradles_ready"):
            check(fl.get(f) == "set", f"0239: the jump SETS {f} (the end of 0.2.3)")
        for f in ("study_blade", "study_signal", "study_method", "last_night_held", "transferred", "rise_searched",
                  "tower_planned", "memory_taken", "units_fought", "dace_dead", "back_in_body", "memory_whole", "cain_chosen"):
            check(fl.get(f) == "unset", f"0239: the jump UNSETS {f}")
        eff = {e.get("trait"): e.get("value") for e in ch[0].get("effects", [])}
        check(eff.get("vega_records") == 0 and eff.get("vega_damage") == 0, "0239: records 0, damage 0")
    # Every older 0.2.3 jump clears the 0.2.4 state too, so a jump taken after playing 0.2.4 lands before it.
    for jid in ("dev_jump_hunt_start", "dev_jump_hunt_on", "dev_jump_hunt_crew", "dev_jump_hunt_take", "dev_jump_hunt_table"):
        j = canvases.get(jid)
        if j:
            ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
            fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
            check(fl.get("transferred") == "unset" and fl.get("cain_chosen") == "unset", f"0239: {jid} clears the 0.2.4 flags")

    # ── beat_0248 — THE VEGA MAP: doors, meters, portrait, Vega's cards, and the leak walk ───────────────────
    locs = {l["id"]: l for l in t.get("locations", [])}
    st = locs.get("underworld_strip") or {}
    # beat_0250 (LO: "No different route for vega"): the strip is OPEN to Vega and the lock is on its six Wren rooms,
    # each with a Vega refusal in blocked_messages, so a room that already had its own lock still says the true reason.
    check(not has_flag(cond_items(st.get("entry_conditions")), "in_vega", "is_false"), "0250: the strip is open to Vega (she walks Wren's route)")
    vbm = [(st.get("description_variants") or [{}])[0].get("conditions")]
    check(has_flag(cond_items(vbm[0]), "in_vega", "is_true"), "0250: the strip describes itself for Vega (description_variants)")
    for rid in ("underworld_bar", "underworld_brothel", "underworld_pit", "underworld_market", "kess_berth", "crew_den"):
        r = locs.get(rid) or {}
        ec = r.get("entry_conditions") or {}
        bms = r.get("blocked_messages") or []
        check(has_flag(cond_items(ec), "in_vega", "is_false") and ec.get("version") == "1.0", f"0250: {rid} is shut to Vega's body")
        check(bool(bms) and has_flag(cond_items(bms[0].get("conditions")), "in_vega", "is_true") and bms[0].get("text", "").startswith("Not in this body."),
              f"0250: {rid} tells Vega why (blocked_messages)")
    cf = locs.get("chairmans_floor") or {}
    ci = cond_items(cf.get("entry_conditions"))
    check(cf.get("entry_from") == "atrium" and "chairmans_floor" in (locs.get("atrium") or {}).get("navigation_order", []),
          "0241: the Chairman's floor hangs off the Atrium")
    check(has_flag(ci, "in_vega", "is_true") and has_flag(ci, "tower_planned", "is_true") and has_flag(ci, "memory_taken", "is_false")
          and any(i.get("type") == "time_of_day" for i in ci), "0241: the Chairman's floor: Vega, after the plan, before the memory, at night")
    rd = cond_items((locs.get("the_rise_floor") or {}).get("entry_conditions"))
    check(has_flag(rd, "rise_named", "is_true") and has_flag(rd, "rise_door", "is_true") and not has_flag(rd, "face_worn", "is_true"),
          "0241: the Rise's door reads rise_door (face or Vega)")
    face = canvases.get("activity_the_face") or {}
    fch = ((node(face, "base") or {}).get("exit_block") or {}).get("choices", [])
    ops = {(f.get("flag"), f.get("op")) for c in fch for f in c.get("flagEffects", [])}
    check(("rise_door", "set") in ops and ("rise_door", "unset") in ops, "0241: the face card sets and clears rise_door with the face")
    check("heal_rise_door" in canvases, "0241: old saves with the face on are healed once (heal_rise_door)")
    rows = t.get("sidebar_items", [])
    cell = [r for r in rows if r.get("trait") == "vega_cell"]
    check(len(cell) == 1 and has_flag(cond_items(cell[0].get("show_when")), "in_vega", "is_true"), "0240: one Vega's cell row, shown only in Vega")
    for r in rows:
        if r.get("trait") != "vega_cell":
            check(has_flag(cond_items(r.get("show_when")), "in_vega", "is_false"), f"0240: Wren's {r.get('trait')} row hides while she is in Vega")
    outs = ((t.get("player_portrait") or {}).get("outfits") or [{}])
    check(outs[0].get("when") == {"flag": "in_vega"}, "0240: the in_vega portrait rule is FIRST (first match wins)")
    check(core.get("vega_cell") == 0 and labels.get("vega_cell", {}).get("hidden") is True, "0240: vega_cell declared at 0 and hidden")
    for cid, loc in (("activity_vega_site", "the_site"), ("activity_vega_gate", "underworld_gate"), ("activity_vega_car", "spire_plaza"),
                     ("activity_vega_gate_car", "underworld_gate"), ("activity_vega_strip_exit", "underworld_strip")):
        c = canvases.get(cid) or {}
        tr = c.get("trigger") or {}
        check(tr.get("location") == loc and has_flag(cond_items(tr.get("conditions")), "in_vega", "is_true"), f"0242: {cid} is Vega's card at {loc}")
    # beat_0250: Vega's twins carry Wren's own labels, and Wren's cards are untouched (LO: no change to her route).
    def labels_of(cid):
        return [ch.get("text") for nd in (canvases.get(cid) or {}).get("nodes", []) for ch in ((nd.get("exit_block") or {}).get("choices") or [])] + \
               [(nd.get("exit_block") or {}).get("text") for nd in (canvases.get(cid) or {}).get("nodes", [])]
    check("Ride down to the Underworld." in labels_of("activity_vega_car") and "Ride down to the Underworld." in labels_of("activity_travel_to_reach"),
          "0250: the plaza car's label is Wren's for Vega too")
    check("Ride up to the Spire." in labels_of("activity_vega_gate_car") and "Ride up to the Spire." in labels_of("activity_travel_from_gate"),
          "0250: the gate car's label is Wren's for Vega too")
    check("Out to the gate." in labels_of("activity_vega_strip_exit") and "Out to the gate." in labels_of("underworld_strip_hub"),
          "0250: Exit Underworld is the same for Vega")
    check(not any(nd.get("id") == "out" for nd in (canvases.get("activity_vega_site") or {}).get("nodes", [])),
          "0250: the Site's separate way out for Vega is gone")
    for cid in ("activity_travel_to_reach", "activity_travel_from_gate", "underworld_gate_check", "underworld_strip_hub"):
        check(has_flag(cond_items((canvases.get(cid) or {}).get("trigger", {}).get("conditions")), "in_vega", "is_false"), f"0250: Wren's {cid} stays hers")
    bb2 = canvases.get("cap_back_in_body") or {}
    cfg = (((bb2.get("nodes") or [{}])[-1].get("exit_block")) or {}).get("config") or {}
    fl = {f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}
    check(fl.get("in_vega") == "unset" and fl.get("rise_door") == "unset", "0246: the homecoming takes her out of Vega (in_vega, rise_door unset)")
    # THE LEAK WALK. Every place Vega can reach, and every card that may render there, must be Vega's (in_vega gate),
    # closed to Vega, impossible under the known Vega state, or on the read-by-a-human list above.
    reach, by_loc = vega_reach(t)
    # sabin_lab is NOT in this set: Vega's lab is a node of activity_vega_lab, and she never stands in the location.
    want = {"the_site", "underworld_strip", "underworld_gate", "spire_plaza", "atrium", "the_rise_floor", "chairmans_floor"}
    check(want <= reach, f"0248: Vega must be able to reach {sorted(want - reach)}")
    check(not (reach - want), f"0248: Vega can reach places written for Wren: {sorted(reach - want)}")
    for k in reach:
        for c in by_loc.get(k, []):
            tr = c.get("trigger") or {}
            if c["id"].startswith("dev_jump") or c["id"] in VEGA_OK or vega_gated(tr):
                continue
            if may_pass(tr.get("conditions")):
                fails.append(f"0248: {c['id']} @{k} can render while Wren is in Vega and is not written for her (gate it in_vega is_false, or band it)")

    # ── beat_0249 — the Quests page: character cards hide in Vega; finished arcs under "Finished" (LO 2026-10-13) ──
    npc_cards = [c for c in cards if c.get("npc_id")]
    # beat_0251: Kess and Cain each have ONE card written for Vega (in_vega is_true) that names only the Site.
    vega_cards = [c for c in npc_cards if {"flag": "in_vega", "op": "is_true"} in c.get("when", [])]
    check(sorted(c["npc_id"] for c in vega_cards) == ["npc_cain", "npc_kess"], f"0251: Kess and Cain each have one Vega card, got {[c['npc_id'] for c in vega_cards]}")
    for c in vega_cards:
        check("Berth" not in c.get("tip", "") and "Site" in c.get("tip", ""), f"0251: {c['npc_id']}'s Vega card names only the Site")
    ungated = [(c.get("npc_id"), c.get("priority")) for c in npc_cards if c not in vega_cards and {"flag": "in_vega", "op": "is_false"} not in c.get("when", [])]
    check(not ungated, f"0249: every other character card hides while she is in Vega (their tips name Wren's places); ungated: {ungated}")
    # beat_0251: one live Kess card and one live Cain card in every state of the chapter (the NPC tier shows one).
    def live(npc, st):
        out = []
        for c in npc_cards:
            if c.get("npc_id") != npc:
                continue
            ok_ = all((st.get(w["flag"], False) is (w["op"] == "is_true")) for w in c.get("when", []) if "flag" in w)
            if ok_:
                out.append(c["text"][:30])
        return out
    STATES = {
        "study": {"cradles_ready": True},
        "after the last night": {"cradles_ready": True, "last_night_held": True},
        "in Vega": {"cradles_ready": True, "last_night_held": True, "transferred": True, "in_vega": True},
        "home": {"cradles_ready": True, "last_night_held": True, "transferred": True, "back_in_body": True},
    }
    for name, st_ in STATES.items():
        for npc in ("npc_kess", "npc_cain"):
            got = live(npc, st_)
            check(len(got) == 1, f"0251: exactly one {npc} card in '{name}', got {got}")
    check((t.get("project") or {}).get("quests_finished_collapsed") is True, "0249: Vesper opts into the collapsed Finished section")

    if fails:
        print("THE TRANSFER GUARD: FAILED")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print("THE TRANSFER GUARD: OK")


if __name__ == "__main__":
    main()
