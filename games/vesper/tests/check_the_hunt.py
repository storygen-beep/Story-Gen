#!/usr/bin/env python3
"""
0.2.3 — HER FATHER'S HOUSE and THE HUNT — static guard.

Reads the merged TOML and checks the chunk against games/vesper/design_the_hunt.md ("BLUEPRINT").
One section per beat; each beat adds its own section in the same turn it is built, written red first.

Run from the repo root, after a merge:
    python games/vesper/tests/check_the_hunt.py
Exits 0 on pass, 1 on any failure.
"""
import os
import sys

try:
    import tomllib
except ModuleNotFoundError:                      # py<3.11
    import tomli as tomllib                      # type: ignore

HERE = os.path.dirname(__file__)
GAME = os.path.join(HERE, "..", "toml_phases", "7_final_game.toml")

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def main():
    t = tomllib.load(open(GAME, "rb"))
    core = (t.get("player") or {}).get("core_traits") or {}
    labels = {l.get("key"): l for l in (t.get("traits") or {}).get("labels", [])}
    npcs = {n["id"]: n for n in t.get("npcs", [])}
    canvases = {c["id"]: c for c in t.get("canvases", [])}

    # ── beat_0206 — state + seams ────────────────────────────────────────────────────────────────────
    # 1. The three new traits are declared in core_traits at 0. core_traits is what the cross-release
    #    backfill initialises, so a 0.2.2 save loads them as 0 rather than undefined (every lt/gte on an
    #    undefined trait returns false).
    for key in ("vega_damage", "vega_habits", "undertow_build"):
        check(core.get(key) == 0, f"0206: {key} must be declared in [player.core_traits] at 0, got {core.get(key)!r}")
        check(labels.get(key, {}).get("hidden") is True, f"0206: {key} must be hidden from the traits dump")

    # 2. Damage is the one number the player sees, as a banded sidebar row that is ABSENT at 0 (bands start
    #    at 1) and whose top band has no max (an unset max survives any value).
    rows = [s for s in t.get("sidebar_items", [])
            if s.get("type") == "trait_status_text" and s.get("trait") == "vega_damage"]
    check(len(rows) == 1, f"0206: expected one trait_status_text row for vega_damage, found {len(rows)}")
    if rows:
        bands = rows[0].get("bands") or []
        check(bands and min(b.get("min", 0) for b in bands) == 1,
              "0206: vega_damage bands must start at 1 so the row is absent at 0")
        check(bands and "max" not in max(bands, key=lambda b: b.get("min", 0)),
              "0206: vega_damage's top band must carry no max")
        check(len(bands) == 3, f"0206: vega_damage wants three bands (Fine / Hurt / Badly hurt), has {len(bands)}")

    # 3. The two new people exist, with portraits — and NO schedule rows yet. A row parks a badge on a
    #    nav card in every save; each row lands with the scene that makes it true (Dace at beat_0213).
    for nid in ("npc_vega", "npc_dace"):
        n = npcs.get(nid)
        check(n is not None, f"0206: {nid} is not declared")
        if n:
            check(bool(n.get("portrait")), f"0206: {nid} needs a portrait")
            if nid == "npc_vega":
                check(not n.get("schedules"), "0206: npc_vega never gets a schedule row (she appears only in her own scenes)")

    # 4. Nobody's schedule moved. Inserting an [[npcs]] between an NPC and its [[npcs.schedules]]
    #    re-parents the rows with a green build (1_metadata_and_locations.toml:799, the Kess/Marsh bug).
    expected_rows = {
        "npc_grier": {"grier_room"},
        "npc_sabin": {"the_rise_floor", "sabin_lab"},
        "npc_kess": {"kess_berth"},
        "npc_bastien": {"bastien_backroom", "the_cot"},
        "npc_sol": {"underworld_bar"},
    }
    for nid, locs in expected_rows.items():
        got = {s.get("location") for s in (npcs.get(nid) or {}).get("schedules", [])}
        check(got == locs, f"0206: {nid}'s schedule rows changed: {sorted(got)} (expected {sorted(locs)})")
    # Cain's rows landed at beat_0211 with his training (§0211 checks them); before that he had none.
    check(not (npcs.get("npc_loder") or {}).get("schedules"), "0206: npc_loder must keep zero rows")

    # 5. The dev jump starts at the true end of 0.2.2: every Count flag set, the new state at rest.
    j = canvases.get("dev_jump_hunt_start")
    check(j is not None, "0206: dev_jump_hunt_start is missing")
    if j:
        conds = str((j.get("trigger") or {}).get("conditions"))
        check("dev_mode_enabled" in conds, "0206: the dev jump must be gated on dev_mode_enabled")
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or []
        check(len(ch) == 1 and ch[0].get("locationId") == "the_cot", "0206: the dev jump must land at the cot")
        if ch:
            flags = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
            for f in ("bastien_himself", "bastien_note", "house_answered", "bastien_back"):
                check(flags.get(f) == "set", f"0206: the dev jump must SET {f} (end of 0.2.2)")
            effs = {(e.get("trait"), e.get("npcId")): e.get("value") for e in ch[0].get("effects", [])}
            check(effs.get(("bastien_mend", None)) == 3, "0206: bastien_mend must be 3 (he stopped counting)")
            for key in ("vega_damage", "vega_habits", "undertow_build"):
                check(effs.get((key, None)) == 0, f"0206: the dev jump must put {key} at 0")

    # ── beat_0207 — cap_cain_comes, card H's seam, card I ──────────────────────────────────────────
    def items(cv):
        return (((cv or {}).get("trigger") or {}).get("conditions") or {}).get("items") or []

    def has_flag(its, key, op):
        return any(i.get("type") == "flag" and i.get("flag_key") == key and i.get("operator") == op for i in its)

    def dialog_speakers(cv):
        out = set()

        def walk(o):
            if isinstance(o, dict):
                if o.get("type") == "dialog":
                    p = o.get("props") or {}
                    out.add(p.get("npcId") or p.get("speaker"))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk((cv or {}).get("nodes", []))
        return out

    cc = canvases.get("cap_cain_comes")
    check(cc is not None, "0207: cap_cain_comes is missing")
    if cc:
        tr = cc.get("trigger") or {}
        its = items(cc)
        check(tr.get("location") == "the_cot", "0207: cap_cain_comes must fire at the_cot")
        check(tr.get("is_repeatable") is False, "0207: cap_cain_comes must be a one-shot")
        check((tr.get("priority") or 0) >= 10, "0207: cap_cain_comes needs priority >= 10 (auto-fire)")
        check((tr.get("conditions") or {}).get("version") == "1.0", "0207: conditions need version 1.0 or they fail OPEN")
        check(has_flag(its, "bastien_back", "is_true"), "0207: gated bastien_back is_true (the end of 0.2.2)")
        check(has_flag(its, "site_offered", "is_false"), "0207: gated site_offered is_false (fires once)")
        check(has_flag(its, "face_worn", "is_false"), "0207: gated face_worn is_false (every cot scene waits for the face to be off)")
        # A later day than The Count's last scene, or finishing The Count in the morning fires this in the same breath.
        check(any(i.get("type") == "days_since_flag" and i.get("flag_key") == "bastien_back"
                  and i.get("operator") == "gte" and i.get("value") == 1 for i in its),
              "0207: needs days_since_flag bastien_back gte 1 (never in the same breath as Counting again)")
        check(any(i.get("type") == "time_of_day" for i in its), "0207: gated on the morning (time_of_day)")
        spk = dialog_speakers(cc)
        check({"npc_cain", "npc_bastien", "player"} <= spk, f"0207: Cain, Bastien and Wren all speak (got {sorted(map(str, spk))})")
        ex = ((cc.get("nodes") or [{}])[-1].get("exit_block") or {})
        cfg = ex.get("config") or {}
        check(ex.get("type") == "location" and cfg.get("locationId") == "the_site", "0207: the exit goes to the_site")
        fl = {f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}
        check(fl.get("site_offered") == "set" and fl.get("the_site_open") == "set",
              "0207: the exit sets site_offered and the_site_open")

    site = next((l for l in t.get("locations", []) if l["id"] == "the_site"), {})
    check("have it yet" not in (site.get("description") or ""),
          "0207: the_site's description still says she doesn't have it yet; it is open from cap_cain_comes on")

    cards = t.get("quest_cards", [])
    check(not any("That is where this build ends" in (c.get("tip") or "") for c in cards if not c.get("terminal")),
          "0207: a non-terminal card still says 'That is where this build ends'")
    h = [c for c in cards if (c.get("text") or "").startswith("He counted it out on your blanket")]
    check(len(h) == 1, "0207: card H (He counted it out on your blanket) not found exactly once")
    if h:
        h = h[0]
        check(not h.get("terminal") and not h.get("terminal_text"), "0207: card H must lose terminal and terminal_text")
        check({"flag": "site_offered", "op": "is_false"} in h.get("when", []), "0207: card H must close on site_offered")
    ci = [c for c in cards if {"flag": "site_offered", "op": "is_true"} in c.get("when", [])
          and {"flag": "marrow_known", "op": "is_false"} in c.get("when", [])]
    check(len(ci) == 1, f"0207: expected one card I (site_offered + marrow_known is_false), found {len(ci)}")
    if ci:
        check(any(g.get("flag") == "marrow_known" for g in ci[0].get("goals", [])), "0207: card I's goal is marrow_known")
        check("Site" in (ci[0].get("tip") or ""), "0207: card I's tip must name the Site")

    j = canvases.get("dev_jump_hunt_start")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("site_offered", "the_site_open"):
            check(fl.get(f) == "unset", f"0207: the dev jump must UNSET {f}, or a jump taken mid-chunk skips Cain")

    # ── beat_0208 — cap_the_site (Tier-3) ─────────────────────────────────────────────────────────────
    def all_blocks(o, out):
        if isinstance(o, dict):
            if "type" in o and ("content" in o or o.get("type") in ("image", "video")):
                out.append(o)
            for v in o.values():
                all_blocks(v, out)
        elif isinstance(o, list):
            for v in o:
                all_blocks(v, out)
        return out

    cs = canvases.get("cap_the_site")
    check(cs is not None, "0208: cap_the_site is missing")
    if cs:
        tr = cs.get("trigger") or {}
        its = items(cs)
        check(tr.get("location") == "the_site" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 10,
              "0208: cap_the_site must be a located one-shot auto-fire at the_site")
        check(has_flag(its, "site_offered", "is_true") and has_flag(its, "marrow_known", "is_false"),
              "0208: gated site_offered is_true + marrow_known is_false")
        casc = [b for n in cs.get("nodes", []) for b in n.get("blocks", []) if b.get("type") == "cascade"]
        beats = casc[0]["props"]["beats"] if casc else []
        check(10 <= len(beats) <= 20, f"0208: Tier-3 wants 10-20 beats, has {len(beats)}")
        lead = [b for b in cs["nodes"][0]["blocks"] if b.get("type") != "cascade"]
        units = [lead] + [bt.get("blocks", []) for bt in beats]
        for i, u in enumerate(units):
            w = sum(len((b.get("content") or "").split()) for b in u)
            check(w <= 55, f"0208: beat {i} is {w} words; over ~50 it wanted to be two beats")
        blocks = all_blocks(cs.get("nodes", []), [])
        text = " ".join(b.get("content") or "" for b in blocks)
        # The memory, quoted as it shipped in Whose Hand (5_scenes, "She tells Cain"), with his face in it now.
        for must in ("Vesper, you have got all afternoon", "the seam that is not there yet", "Marrow", "father",
                     "I killed him", "asked me"):
            check(must in text, f"0208: the scene must contain {must!r}")
        for banned in ("Undertow", "Vega"):
            check(banned not in text, f"0208: {banned!r} does not belong in this scene")
        nar = sum(len((b.get("content") or "").split()) for b in blocks if b.get("type") in ("paragraph", "thought_bubble"))
        dia = sum(len((b.get("content") or "").split()) for b in blocks if b.get("type") == "dialog")
        check(dia and nar / dia <= 2.14, f"0208: narration:dialogue {nar}/{dia} is over the 2.14 standing target")
        check(any((b.get("props") or {}).get("npcId") == "npc_cain" for b in blocks if b.get("type") == "dialog"),
              "0208: Cain speaks")
        imgs = [b for b in blocks if b.get("type") == "image"]
        files = {(b.get("props") or {}).get("file") for b in imgs}
        check({"scenes/the_site_lab.jpg", "scenes/marrow_photo.jpg"} <= files, f"0208: the two media slots (got {files})")
        for b in imgs:
            pr = b.get("props") or {}
            check(pr.get("description") and pr.get("search_queries"), f"0208: {pr.get('file')} needs description + search_queries")
        # The photo rides the beat it depicts, never the node's lead (media.md §6a, the clip-rides-the-beat rule).
        check(not any((b.get("props") or {}).get("file") == "scenes/marrow_photo.jpg" for b in lead),
              "0208: the photo belongs in its own beat, not the node's lead")
        ex = (cs["nodes"][-1].get("exit_block") or {})
        fl = {f.get("flag"): f.get("op") for f in (ex.get("config") or {}).get("flagEffects", [])}
        check(fl.get("marrow_known") == "set", "0208: the exit sets marrow_known")

    # ── beat_0209 — the ambush, the seam, and the repair ──────────────────────────────────────────────
    def exit_cfg(cv, node=-1):
        return (((cv or {}).get("nodes") or [{}])[node].get("exit_block") or {})

    def effs_of(holder):
        return {(e.get("trait"), e.get("op")): (e.get("value"), e.get("clamp")) for e in holder.get("effects", [])}

    am = canvases.get("cap_the_ambush")
    check(am is not None, "0209: cap_the_ambush is missing")
    if am:
        tr = am.get("trigger") or {}
        its = items(am)
        # LOCATED, not chained triggerless: site_ambushed is read by triggers (cap_kess_seam, rand_vega_street),
        # and the flag-chain validator hard-fails a flag whose only setter is triggerless.
        check(tr.get("location") == "underworld_strip" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 11,
              "0209: cap_the_ambush must be a located one-shot auto-fire on underworld_strip, priority 11+")
        check(has_flag(its, "marrow_known", "is_true") and has_flag(its, "site_ambushed", "is_false"),
              "0209: gated marrow_known is_true + site_ambushed is_false")
        spk = dialog_speakers(am)
        check({"npc_vega", "npc_cain", "player"} <= spk, f"0209: Vega, Cain and Wren all speak (got {sorted(map(str, spk))})")
        ex = exit_cfg(am)
        cfg = ex.get("config") or {}
        check(cfg.get("locationId") == "kess_berth", "0209: the ambush ends at Kess's berth")
        check(effs_of(cfg).get(("vega_damage", "set"), (None,))[0] == 60, "0209: the ambush sets vega_damage to 60")
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("site_ambushed") == "set",
              "0209: the ambush sets site_ambushed")
        text = " ".join(b.get("content") or "" for b in all_blocks(am.get("nodes", []), []))
        check("Undertow" not in text, "0209: no Undertow in the ambush")
        imgs = [b for b in all_blocks(am.get("nodes", []), []) if b.get("type") == "image"]
        check(any((b.get("props") or {}).get("file") == "scenes/vega_ambush.jpg" for b in imgs), "0209: scenes/vega_ambush.jpg")

    ks = canvases.get("cap_kess_seam")
    check(ks is not None, "0209: cap_kess_seam is missing")
    if ks:
        tr = ks.get("trigger") or {}
        its = items(ks)
        check(tr.get("location") == "kess_berth" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 10,
              "0209: cap_kess_seam must be a located one-shot auto-fire at kess_berth")
        check(has_flag(its, "site_ambushed", "is_true") and has_flag(its, "seam_known", "is_false"),
              "0209: gated site_ambushed is_true + seam_known is_false")
        # Kess keeps yard hours; a pri-11 one-shot without this plays to an empty dock (the beat_0068 lesson).
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_kess" for i in its),
              "0209: cap_kess_seam needs npc_at_location npc_kess is_present")
        cfg = exit_cfg(ks).get("config") or {}
        e = effs_of(cfg).get(("vega_damage", "add"))
        check(e == (-25, True), f"0209: the first repair is free: vega_damage add -25 with clamp = true (got {e})")
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("seam_known") == "set",
              "0209: cap_kess_seam sets seam_known")
        text = " ".join(b.get("content") or "" for b in all_blocks(ks.get("nodes", []), []))
        check("seam" in text and "every one" in text.lower(), "0209: Kess shows her the seam, and that every one of them has it")

    hub = canvases.get("hub_kess_berth") or {}
    rep = [c for c in exit_cfg(hub, 0).get("choices", []) if c.get("nodeId") == "kess_patch_up.base"]
    check(len(rep) == 1, "0209: hub_kess_berth needs one choice into kess_patch_up.base")
    if rep:
        cond = rep[0].get("conditions") or {}
        check(cond.get("version") == "1.0" and any(i.get("trait_key") == "vega_damage" and i.get("operator") == "gte"
                                                   for i in cond.get("items", [])),
              "0209: the repair choice shows only when vega_damage gte 1")
    pu = canvases.get("kess_patch_up")
    check(pu is not None, "0209: kess_patch_up is missing")
    if pu:
        tr = pu.get("trigger") or {}
        check(tr.get("location") == "kess_berth" and tr.get("substitution_only") is True and tr.get("is_repeatable") is True,
              "0209: kess_patch_up keeps a located, substitution_only, repeatable trigger (the kess_makes_the_brace shape)")
        pay = [c for c in exit_cfg(pu, 0).get("choices", []) if any(x.get("trait") == "coin" for x in c.get("costs", []))]
        check(len(pay) == 1, "0209: kess_patch_up's base has one paying choice")
        if pay:
            check(pay[0]["costs"] == [{"trait": "coin", "value": 10}], f"0209: a repair costs 10 coin (got {pay[0]['costs']})")
            check(effs_of(pay[0]).get(("vega_damage", "add")) == (-25, True), "0209: a repair is vega_damage add -25, clamp = true")
        # Every band of the repeat screen must exist, so every visit says something true about how hurt she is.
        grp = [b for b in pu["nodes"][0].get("blocks", []) if b.get("type") == "group"]
        check(len(grp) == 3, f"0209: kess_patch_up's base wants three damage bands, has {len(grp)}")

    j0 = [c for c in cards if {"flag": "site_ambushed", "op": "is_true"} in c.get("when", [])
          and {"flag": "seam_known", "op": "is_false"} in c.get("when", [])]
    check(len(j0) == 1, "0209: one card live between the ambush and Kess (site_ambushed + seam_known is_false)")

    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("marrow_known", "site_ambushed", "seam_known"):
            check(fl.get(f) == "unset", f"0209: the dev jump must UNSET {f}")

    # ── beat_0210 — Vega on the streets + card J ──────────────────────────────────────────────────────
    def band_values(blocks, key):
        """Return the list of (op, value) tuples of every group on `key`, in order."""
        out = []
        for b in blocks:
            if b.get("type") != "group":
                continue
            its_ = (((b.get("props") or {}).get("conditions") or {}).get("items") or [])
            out.append(tuple((i.get("operator"), i.get("value")) for i in its_ if i.get("trait_key") == key))
        return out

    rv = canvases.get("rand_vega_street")
    check(rv is not None, "0210: rand_vega_street is missing")
    if rv:
        tr = rv.get("trigger") or {}
        check(tr.get("location") == "underworld_strip" and tr.get("trigger_mode") == "random"
              and tr.get("is_repeatable") is True and tr.get("chance") == 0.35 and tr.get("max_triggers_per_day") == 1,
              "0210: rand_vega_street must be Lane-2 random on underworld_strip, chance 0.35, once a day, repeatable")
        check(not tr.get("npc") and not tr.get("requires_npc"),
              "0210: no npc / requires_npc — Vega has no schedule, so a presence gate would never pass")
        its = items(rv)
        check(has_flag(its, "seam_known", "is_true") and has_flag(its, "vega_taken", "is_false"),
              "0210: gated seam_known is_true (after Kess) + vega_taken is_false (closes at the take)")
        nodes_ = {n["id"]: n for n in rv.get("nodes", [])}
        check(set(nodes_) == {"base", "run"}, f"0210: two screens, base and run (got {sorted(nodes_)})")
        for nid in ("base", "run"):
            bands = [bv for bv in band_values(nodes_.get(nid, {}).get("blocks", []), "vega_habits") if bv]
            check(bands == [(("gte", 4),), (("gte", 3), ("lt", 4)), (("gte", 2), ("lt", 3)), (("gte", 1), ("lt", 2)), (("lt", 1),)],
                  f"0210: {nid} needs five exclusive vega_habits bands 4 / 3 / 2 / 1 / 0 in that order, got {bands}")
        # The damage overlay must not merge into the band chain: adjacent groups form ONE if/elseif chain.
        bb = nodes_.get("base", {}).get("blocks", [])
        gi = [k for k, b in enumerate(bb) if b.get("type") == "group"]
        check(gi and bb[gi[0] + 1].get("type") != "group",
              "0210: an ungrouped block must separate the damage overlay from the habit bands")
        cfg = (nodes_.get("run", {}).get("exit_block") or {}).get("config") or {}
        check(cfg.get("locationId") == "the_cot" and cfg.get("time_progression_minutes") == 540,
              "0210: the escape loses the day (540 minutes) and ends at the cot")
        effs = {e.get("trait"): e for e in cfg.get("effects", [])}
        dmg, hab = effs.get("vega_damage") or {}, effs.get("vega_habits") or {}
        check(dmg.get("op") == "add" and dmg.get("value") == 35 and dmg.get("clamp") is True, "0210: vega_damage add 35, clamp = true")
        check(hab.get("op") == "add" and hab.get("value") == 1 and hab.get("clamp") is True and hab.get("cap") == 4,
              "0210: vega_habits add 1, clamp = true, cap = 4")
        text = " ".join(b.get("content") or "" for b in all_blocks(rv.get("nodes", []), []))
        check("Undertow" not in text, "0210: no Undertow on the street")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(rv.get("nodes", []), []) if b.get("type") == "image"}
        check({f"scenes/vega_street_t{k}.jpg" for k in (1, 2, 3, 4, 5)} <= imgs, f"0210: the five street media slots, one per band (got {imgs})")

    jj = [c for c in cards if {"flag": "seam_known", "op": "is_true"} in c.get("when", [])
          and {"flag": "vega_taken", "op": "is_false"} in c.get("when", [])]
    check(len(jj) == 1, f"0210: one card J for the hunt (seam_known + vega_taken is_false), found {len(jj)}")
    if jj:
        gl = {(g.get("trait") or g.get("flag"), g.get("op"), g.get("value")) for g in jj[0].get("goals", [])}
        for need in (("vega_habits", "gte", 4), ("fighting", "gte", 85), ("vega_damage", "lt", 30)):
            check(need in gl, f"0210: card J needs the goal {need}")

    # ── beat_0211 — Cain trains her at the Site + his schedule rows ────────────────────────────────────
    rows = (npcs.get("npc_cain") or {}).get("schedules") or []
    spans = sorted((r.get("location"), r.get("start_time"), r.get("end_time")) for r in rows)
    check(spans == [("the_site", "00:00", "03:00"), ("the_site", "21:00", "23:59")],
          f"0211: Cain's two rows are the_site 21:00-23:59 and 00:00-03:00 (got {spans})")
    for r in rows:
        w = r.get("when") or {}
        check(w.get("version") == "1.0" and any(i.get("flag_key") == "the_site_open" and i.get("operator") == "is_true"
                                                for i in w.get("items", [])),
              "0211: each Cain row needs when = the_site_open is_true (version 1.0, or it fails OPEN)")
        check(sorted(r.get("weekdays") or []) == [0, 1, 2, 3, 4, 5, 6], "0211: Cain's rows run every day")
    check("no schedule" not in ((npcs.get("npc_cain") or {}).get("description") or "").lower(),
          "0211: Cain's description still says he has no schedule")
    ct = canvases.get("activity_cain_trains")
    check(ct is not None, "0211: activity_cain_trains is missing")
    if ct:
        tr = ct.get("trigger") or {}
        check(tr.get("location") == "the_site" and tr.get("npc") == "npc_cain" and tr.get("requires_npc") == "npc_cain"
              and tr.get("is_repeatable") is True and tr.get("trigger_mode", "manual") == "manual",
              "0211: a Lane-1 portrait hub: npc AND requires_npc = npc_cain, repeatable, manual, at the_site")
        its = items(ct)
        check(has_flag(its, "marrow_known", "is_true"), "0211: the hub opens after the Site scene (marrow_known)")
        nodes_ = {n["id"]: n for n in ct.get("nodes", [])}
        bands = [bv for bv in band_values(nodes_.get("base", {}).get("blocks", []), "fighting") if bv]
        check(bands == [(("gte", 85),), (("gte", 70), ("lt", 85)), (("lt", 70),)],
              f"0211: base needs three fighting bands 85+ / 70-84 / under 70, got {bands}")
        fg = [b for b in nodes_.get("base", {}).get("blocks", []) if b.get("type") == "group"]
        check(fg and has_flag(((fg[0].get("props") or {}).get("conditions") or {}).get("items") or [], "vega_taken", "is_true"),
              "0216: Cain's base opens with the after-the-take band (vega_taken), ahead of the fighting bands")
        ch = (nodes_.get("base", {}).get("exit_block") or {}).get("choices") or []
        trains = [c for c in ch if c.get("text") == "Train with him."]
        check(len(trains) == 2, f"0211: two same-label 'Train with him.' choices (first session / later), got {len(trains)}")
        for c in trains:
            ci = (c.get("conditions") or {}).get("items") or []
            check(any(i.get("trait_key") == "fighting" and i.get("operator") == "gte" and i.get("value") == 70 for i in ci)
                  and any(i.get("trait_key") == "fighting" and i.get("operator") == "lt" and i.get("value") == 85 for i in ci),
                  "0211: each training choice needs fighting gte 70 and lt 85")
            check(c.get("costs") == [{"trait": "energy", "value": 15}], f"0211: a session costs 15 energy (got {c.get('costs')})")
            e = {x.get("trait"): x for x in c.get("effects", [])}.get("fighting") or {}
            check(e.get("op") == "add" and e.get("value") == 1 and e.get("cap") == 85 and e.get("clamp") is True,
                  "0211: a session is fighting add 1, cap 85, clamp = true")
        firsts = [c for c in trains if any(i.get("flag_key") == "cain_rule_heard" and i.get("operator") == "is_false"
                                           for i in (c.get("conditions") or {}).get("items", []))]
        check(len(firsts) == 1 and firsts[0].get("nodeId") == "activity_cain_trains.first",
              "0211: the first-session choice (cain_rule_heard is_false) goes to .first")
        first_text = " ".join(b.get("content") or "" for b in all_blocks(nodes_.get("first", {}).get("blocks", []), []))
        check("She'll always do the right thing. You have to do the wrong one." in first_text, "0211: the rule, in his words")
        fcfg = (nodes_.get("first", {}).get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in fcfg.get("flagEffects", [])}.get("cain_rule_heard") == "set",
              "0211: .first sets cain_rule_heard")
        for nid in ("first", "session"):
            cfg = (nodes_.get(nid, {}).get("exit_block") or {}).get("config") or {}
            check(cfg.get("time_progression_minutes") == 120 and cfg.get("locationId") == "the_site",
                  f"0211: .{nid} takes 120 minutes and returns to the_site")
        sb = [bv for bv in band_values(nodes_.get("session", {}).get("blocks", []), "fighting") if bv]
        check(sb == [(("gte", 85),), (("gte", 80), ("lt", 85)), (("gte", 75), ("lt", 80)), (("lt", 75),)],
              f"0211: .session needs four post-increment bands 85 / 80-84 / 75-79 / under 75, got {sb}")
        text = " ".join(b.get("content") or "" for b in all_blocks(ct.get("nodes", []), []))
        check("Undertow" not in text, "0211: no Undertow at the Site")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(ct.get("nodes", []), []) if b.get("type") == "image"}
        check("scenes/cain_training.jpg" in imgs, "0211: scenes/cain_training.jpg")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        check(fl.get("cain_rule_heard") == "unset", "0211: the dev jump must UNSET cain_rule_heard")

    # ── beat_0212 — B1 (Bastien asks) + B2 (the rebuild) + every Undertow surface kept true ────────────
    def cond_items(holder):
        return ((holder or {}).get("conditions") or {}).get("items") or []

    def node(cv, nid):
        return next((n for n in (cv or {}).get("nodes", []) if n["id"] == nid), {})

    amb = canvases.get("amb_bastien_cot") or {}
    vch = [c for c in (node(amb, "base").get("exit_block") or {}).get("choices", []) if c.get("text") == "Tell him about Vega."]
    check(len(vch) == 1, "0212: amb_bastien_cot needs one 'Tell him about Vega.' choice")
    if vch:
        ci = cond_items(vch[0])
        check(has_flag(ci, "site_ambushed", "is_true") and has_flag(ci, "crew_asked", "is_false") and has_flag(ci, "face_worn", "is_false"),
              "0212: the choice is gated site_ambushed + crew_asked is_false + face_worn is_false")
        check(vch[0].get("nodeId") in ("vega", "amb_bastien_cot.vega"), "0212: the choice goes to amb_bastien_cot.vega")
    vn = node(amb, "vega")
    vcfg = (vn.get("exit_block") or {}).get("config") or {}
    check({f.get("flag"): f.get("op") for f in vcfg.get("flagEffects", [])}.get("crew_asked") == "set", "0212: .vega sets crew_asked")
    vtext = " ".join(b.get("content") or "" for b in all_blocks(vn.get("blocks", []), []))
    check("Sol" in vtext and "Undertow" in vtext, "0212: Bastien names the Undertow and Sol")
    check("strip" in vtext, "0212: his men died on the strip (cap_the_raid shows no body in the bar)")

    rb = canvases.get("activity_rebuild_undertow")
    check(rb is not None, "0212: activity_rebuild_undertow is missing")
    if rb:
        tr = rb.get("trigger") or {}
        check(tr.get("location") == "underworld_bar" and tr.get("is_repeatable") is True and not tr.get("npc")
              and not tr.get("requires_npc"), "0212: a repeatable solo card at underworld_bar (never a second Sol card)")
        its = items(rb)
        check(has_flag(its, "crew_asked", "is_true"), "0212: gated crew_asked")
        check(any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" and i.get("value") == 3 for i in its),
              "0212: gated undertow_build lt 3 (closes when the bar is open)")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_sol" and i.get("operator") == "is_present" for i in its),
              "0212: Sol takes the coin, so he must be there (npc_at_location, not requires_npc)")
        pays = [c for c in (node(rb, "base").get("exit_block") or {}).get("choices", []) if c.get("costs")]
        got = sorted((c["costs"][0]["value"], [i.get("value") for i in cond_items(c) if i.get("trait_key") == "undertow_build"])
                     for c in pays)
        check([g[0] for g in got] == [40, 60, 80], f"0212: three paid stages 40 / 60 / 80 coin (got {got})")
        for c in pays:
            e = {x.get("trait"): x for x in c.get("effects", [])}.get("undertow_build") or {}
            check(e.get("op") == "add" and e.get("value") == 1 and e.get("cap") == 3 and e.get("clamp") is True,
                  "0212: each stage is undertow_build add 1, cap 3, clamp = true")
        last = [c for c in pays if c["costs"][0]["value"] == 80]
        check(last and {f.get("flag"): f.get("op") for f in last[0].get("flagEffects", [])}.get("undertow_open") == "set",
              "0212: the third stage sets undertow_open")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(rb.get("nodes", []), []) if b.get("type") == "image"}
        check({"scenes/undertow_rebuild_1.jpg", "scenes/undertow_rebuild_2.jpg", "scenes/undertow_rebuild_3.jpg"} <= imgs,
              f"0212: the three rebuild media slots (got {imgs})")

    # Every surface that describes the burned bar must stop at the stage that makes it false.
    sift = canvases.get("activity_sift_the_ruin") or {}
    check(any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" and i.get("value") == 1 for i in items(sift)),
          "0212: the ruin crawl closes when the clearing starts (undertow_build lt 1)")
    sol = canvases.get("hub_sol_undertow") or {}
    sbands = band_values(node(sol, "base").get("blocks", []), "undertow_build")
    check(sum(1 for b in sbands if b) == 4, f"0212: Sol's base needs four undertow_build bands (ruin / cleared / rebuilt / open), got {sbands}")
    askb = [c for c in (node(sol, "base").get("exit_block") or {}).get("choices", []) if c.get("text") == "Ask what they did with Bastien."]
    check(askb and any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" for i in cond_items(askb[0])),
          "0212: 'Ask what they did with Bastien.' closes once Sol knows it is Bastien's money")
    colm = canvases.get("hub_colm_undertow") or {}
    cb = [b for b in node(colm, "base").get("blocks", []) if b.get("type") == "group"
          and any(i.get("flag_key") == "raid_done" and i.get("operator") == "is_true"
                  for i in (((b.get("props") or {}).get("conditions") or {}).get("items") or []))]
    ruin = [b for b in cb if any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" and i.get("value") == 3
                                 for i in b["props"]["conditions"]["items"])]
    opened = [b for b in cb if any(i.get("trait_key") == "undertow_build" and i.get("operator") == "gte" and i.get("value") == 3
                                   for i in b["props"]["conditions"]["items"])]
    check(len(ruin) == 3 and len(opened) == 3, f"0212: Colm's post-raid base needs 3 ruin bands (lt 3) + 3 open bands (gte 3), got {len(ruin)}/{len(opened)}")
    cch = (node(colm, "base").get("exit_block") or {}).get("choices", [])
    tape = [c for c in cch if c.get("text") == "Take him through the tape."]
    check(tape and any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" and i.get("value") == 3
                       for i in cond_items(tape[0])), "0212: 'through the tape' closes when the back wall is rebuilt")
    back_open = [c for c in cch if c.get("text") == "Take him in the back."
                 and has_flag(cond_items(c), "raid_done", "is_true")]
    check(len(back_open) == 1 and any(i.get("trait_key") == "undertow_build" and i.get("operator") == "gte" and i.get("value") == 3
                                      for i in cond_items(back_open[0])),
          "0212: a post-rebuild 'Take him in the back.' (raid_done is_true + undertow_build gte 3)")
    lc = canvases.get("loop_colm_backroom") or {}
    lb = [b for b in node(lc, "intro").get("blocks", []) if b.get("type") == "group"]
    lruin = [b for b in lb if any(i.get("trait_key") == "undertow_build" and i.get("operator") == "lt" for i in b["props"]["conditions"]["items"])]
    lopen = [b for b in lb if any(i.get("trait_key") == "undertow_build" and i.get("operator") == "gte" for i in b["props"]["conditions"]["items"])]
    check(len(lruin) == 1 and len(lopen) == 1, "0212: Colm's loop intro needs a ruin band (lt 3) and a rebuilt band (gte 3)")

    bcards = [c for c in cards if c.get("npc_id") == "npc_bastien"]
    c19 = [c for c in bcards if {"flag": "bastien_back", "op": "is_true"} in c.get("when", [])]
    check(any({"flag": "site_ambushed", "op": "is_false"} in c.get("when", []) for c in c19),
          "0212: Bastien's 0.2.2 end card closes at the ambush")
    c20 = [c for c in bcards if {"flag": "site_ambushed", "op": "is_true"} in c.get("when", [])
           and {"flag": "crew_asked", "op": "is_false"} in c.get("when", [])]
    c21 = [c for c in bcards if {"flag": "crew_asked", "op": "is_true"} in c.get("when", [])
           and {"flag": "undertow_open", "op": "is_false"} in c.get("when", [])]
    check(len(c20) == 1 and len(c21) == 1, f"0212: Bastien cards 20 (tell him) and 21 (the bar) — got {len(c20)}/{len(c21)}")
    if c21:
        check(any(g.get("trait") == "undertow_build" and g.get("value") == 3 for g in c21[0].get("goals", [])),
              "0212: card 21's goal is undertow_build 3")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("crew_asked", "undertow_open"):
            check(fl.get(f) == "unset", f"0212: the dev jump must UNSET {f}")

    # ── beat_0213 — B3 the refusal, B4 Dace, Dace's pit row, Bastien cards 22/23 ───────────────────────
    drows = (npcs.get("npc_dace") or {}).get("schedules") or []
    check([(r.get("location"), r.get("start_time"), r.get("end_time")) for r in drows] == [("underworld_pit", "18:00", "23:59")],
          f"0213: Dace's one row is underworld_pit 18:00-23:59 (got {[(r.get('location'), r.get('start_time'), r.get('end_time')) for r in drows]})")
    for r in drows:
        w = r.get("when") or {}
        check(w.get("version") == "1.0" and any(i.get("flag_key") == "crew_refused" and i.get("operator") == "is_true"
                                                for i in w.get("items", [])),
              "0213: Dace's row needs when = crew_refused is_true (version 1.0) — he is not on the map before the men send her to him")
        check(any(i.get("flag_key") == "dace_met" and i.get("operator") == "is_false" for i in w.get("items", [])),
              "0214: Dace's row ends at his scene (dace_met is_false) — nothing of his is at the pit after it")
    cr = canvases.get("cap_crew_refuses")
    check(cr is not None, "0213: cap_crew_refuses is missing")
    if cr:
        tr = cr.get("trigger") or {}
        its = items(cr)
        check(tr.get("location") == "underworld_bar" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 11,
              "0213: cap_crew_refuses is a located one-shot auto-fire at underworld_bar, pri 11+")
        check(has_flag(its, "undertow_open", "is_true") and has_flag(its, "crew_refused", "is_false"),
              "0213: gated undertow_open + crew_refused is_false")
        # beat_0219 (LO): the men come because Bastien called them, through Rue — a day after she delivered his list.
        check(has_flag(its, "crew_called", "is_true"), "0219: the men come only after Bastien's call (crew_called)")
        check(any(i.get("type") == "days_since_flag" and i.get("flag_key") == "crew_called" and i.get("operator") == "gte"
                  and i.get("value") == 1 for i in its), "0219: the evening AFTER Rue puts the word out (days_since_flag crew_called gte 1)")
        check(any(i.get("type") == "time_of_day" for i in its), "0213: in the evening (time_of_day)")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_sol" for i in its), "0213: Sol is behind the bar")
        text = " ".join(b.get("content") or "" for b in all_blocks(cr.get("nodes", []), []))
        check("strip" in text and "Dace" in text, "0213: they died on the strip; they send her to Dace")
        # LO, 2026-10-04: "Who tells her dace is at the pit after 6pm??" — the men do, in the scene, where and when
        # (his row is 18:00-23:59 at underworld_pit), not only the quest card's tip.
        check("pit every night from six" in text, "0213: the men tell her where AND when Dace drinks (the pit, from six)")
        check(not any((b.get("props") or {}).get("npcId") == "npc_bastien" for b in all_blocks(cr.get("nodes", []), [])),
              "0213: Bastien does not appear at the bar (none of them will know where he is)")
        cfg = (cr["nodes"][-1].get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("crew_refused") == "set", "0213: sets crew_refused")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(cr.get("nodes", []), []) if b.get("type") == "image"}
        check("scenes/undertow_reopened.jpg" in imgs, "0213: scenes/undertow_reopened.jpg")
    dp = canvases.get("cap_dace_price")
    check(dp is not None, "0213: cap_dace_price is missing")
    if dp:
        tr = dp.get("trigger") or {}
        its = items(dp)
        check(tr.get("location") == "underworld_pit" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 11,
              "0213: cap_dace_price is a located one-shot auto-fire at underworld_pit, pri 11+")
        check(has_flag(its, "crew_refused", "is_true") and has_flag(its, "dace_met", "is_false"), "0213: gated crew_refused + dace_met is_false")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_dace" for i in its), "0213: Dace present (his pit row)")
        spk = dialog_speakers(dp)
        check({"npc_dace", "player"} <= spk, "0213: Dace and Wren speak")
        text = " ".join(b.get("content") or "" for b in all_blocks(dp.get("nodes", []), []))
        check("ten" in text and "all" in text, "0213: about ten men, all at once")
        cfg = (dp["nodes"][-1].get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("dace_met") == "set", "0213: sets dace_met")
    bc = [c for c in cards if c.get("npc_id") == "npc_bastien"]
    c22 = [c for c in bc if {"flag": "crew_called", "op": "is_true"} in c.get("when", []) and {"flag": "crew_refused", "op": "is_false"} in c.get("when", [])]
    c23 = [c for c in bc if {"flag": "crew_refused", "op": "is_true"} in c.get("when", []) and {"flag": "dace_met", "op": "is_false"} in c.get("when", [])]
    check(len(c22) == 1 and len(c23) == 1, f"0213: Bastien cards 22 (the men) and 23 (Dace), got {len(c22)}/{len(c23)}")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("crew_refused", "dace_met"):
            check(fl.get(f) == "unset", f"0213: the dev jump must UNSET {f}")

    # ── beat_0219 — LO's amendment: Bastien hears the bar is open and calls his men, through Rue ─────────
    amb_ = canvases.get("amb_bastien_cot") or {}
    bo = [c for c in (node(amb_, "base").get("exit_block") or {}).get("choices", []) if c.get("text") == "Tell him the bar is open."]
    check(len(bo) == 1, "0219: amb_bastien_cot needs one 'Tell him the bar is open.' choice")
    if bo:
        ci = cond_items(bo[0])
        check(has_flag(ci, "undertow_open", "is_true") and has_flag(ci, "crew_list_held", "is_false") and has_flag(ci, "face_worn", "is_false"),
              "0219: gated undertow_open + crew_list_held is_false + face_worn is_false")
    bn = node(amb_, "bar_open")
    bcfg = (bn.get("exit_block") or {}).get("config") or {}
    check({f.get("flag"): f.get("op") for f in bcfg.get("flagEffects", [])}.get("crew_list_held") == "set", "0219: .bar_open sets crew_list_held")
    btext = " ".join(b.get("content") or "" for b in all_blocks(bn.get("blocks", []), []))
    check("Rue" in btext and "names" in btext, "0219: Bastien writes the names, for Rue")
    rl = canvases.get("cap_rue_takes_the_list")
    check(rl is not None, "0219: cap_rue_takes_the_list is missing")
    if rl:
        tr = rl.get("trigger") or {}
        its = items(rl)
        check(tr.get("location") == "underworld_brothel" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 10,
              "0219: a located one-shot auto-fire at the House")
        check(has_flag(its, "crew_list_held", "is_true") and has_flag(its, "crew_called", "is_false") and has_flag(its, "rue_introduced", "is_true"),
              "0219: gated crew_list_held + crew_called is_false + rue_introduced")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_rue" for i in its), "0219: Rue present (08:00-03:00)")
        check({"npc_rue", "player"} <= dialog_speakers(rl), "0219: Rue and Wren speak")
        rcfg = (rl["nodes"][-1].get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in rcfg.get("flagEffects", [])}.get("crew_called") == "set", "0219: sets crew_called")
    crf = canvases.get("cap_crew_refuses") or {}
    crtext = " ".join(b.get("content") or "" for b in all_blocks(crf.get("nodes", []), []))
    check("Rue said" in crtext, "0219: the men answer Rue's word ('Rue said ...')")
    c22a = [c for c in bc if {"flag": "undertow_open", "op": "is_true"} in c.get("when", []) and {"flag": "crew_list_held", "op": "is_false"} in c.get("when", [])]
    c22b = [c for c in bc if {"flag": "crew_list_held", "op": "is_true"} in c.get("when", []) and {"flag": "crew_called", "op": "is_false"} in c.get("when", [])]
    check(len(c22a) == 1 and len(c22b) == 1, f"0219: Bastien cards 'tell him' and 'take the list to Rue' (got {len(c22a)}/{len(c22b)})")
    for jid, want in (("dev_jump_hunt_start", "unset"), ("dev_jump_hunt_on", "unset"), ("dev_jump_hunt_crew", "set"),
                      ("dev_jump_hunt_take", "set"), ("dev_jump_hunt_table", "set")):
        jj_ = canvases.get(jid)
        if jj_:
            ch = ((jj_.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
            fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
            for f in ("crew_list_held", "crew_called"):
                check(fl.get(f) == want, f"0219: {jid} must {want.upper()} {f}")

    # ── beat_0214 — B5 the crew night (Tier-3, the release's explicit capstone) + card 24 + J's crew goal ──
    import re
    # The scoreboard's frozen explicit list, VERSION 2, copied verbatim from author-game-v2/scripts/gates.py:311 so
    # this guard measures with the instrument the build is judged by.
    EXPLICIT = re.compile(
        r"\b(cock|dick|penis|cunt|puss|clit|tit(?:s|ty|ties)?\b|breast|nipple|ass(?:es)?\b|arse|anal|balls"
        r"|fuck|suck|blowjob|handjob|cum|semen|orgasm|moan|naked|nude|undress|horny"
        r"|arous|lust|lewd|slut|whore|thrust|penetrat|grop|erect|masturbat|vagina"
        r"|kiss|lick)", re.I)
    cn = canvases.get("cap_the_crew_night")
    check(cn is not None, "0214: cap_the_crew_night is missing")
    if cn:
        tr = cn.get("trigger") or {}
        its = items(cn)
        check(tr.get("location") == "underworld_bar" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 11,
              "0214: a located one-shot auto-fire at underworld_bar, pri 11+")
        check(has_flag(its, "dace_met", "is_true") and has_flag(its, "crew_back", "is_false") and has_flag(its, "undertow_open", "is_true"),
              "0214: gated dace_met + undertow_open + crew_back is_false")
        check(any(i.get("type") == "days_since_flag" and i.get("flag_key") == "dace_met" and i.get("operator") == "gte"
                  and i.get("value") == 1 for i in its), "0214: the night AFTER Dace's yes ('Tomorrow night')")
        check(any(i.get("type") == "time_of_day" and i.get("start_time") == "22:00" for i in its), "0214: after Sol shuts (22:00 on)")
        casc = [b for n in cn.get("nodes", []) for b in n.get("blocks", []) if b.get("type") == "cascade"]
        beats = casc[0]["props"]["beats"] if casc else []
        check(10 <= len(beats) <= 20, f"0214: Tier-3 wants 10-20 beats, has {len(beats)}")
        units = [[b for b in cn["nodes"][0]["blocks"] if b.get("type") != "cascade"]] + [bt.get("blocks", []) for bt in beats]
        explicit_beats = 0
        for i, u in enumerate(units):
            narr = " ".join(b.get("content") or "" for b in u if b.get("type") in ("paragraph",))
            w = sum(len((b.get("content") or "").split()) for b in u)
            check(w <= 60, f"0214: beat {i} is {w} words")
            if len(EXPLICIT.findall(narr)) >= 3:
                explicit_beats += 1
                # THE PIVOT RULE: an explicit beat's last narrated sentence stays on the body.
                last = [b for b in u if b.get("type") == "paragraph"][-1]["content"]
                check(len(EXPLICIT.findall(last)) >= 1 or any(k in last for k in ("floor", "boards", "counter", "mouth", "hips", "knees")),
                      f"0214: explicit beat {i} ends off the body: {last[-80:]!r}")
                check(not any(b.get("type") == "thought_bubble" for b in u), f"0214: explicit beat {i} folds interiority into the act")
        check(explicit_beats >= 7, f"0214: the capstone needs at least 7 explicit beats (3+ frozen words), has {explicit_beats}")
        text = " ".join(b.get("content") or "" for b in all_blocks(cn.get("nodes", []), []))
        check(not re.search(r"\banal\b|\bin her ass\b|\bup her ass\b|arse", text, re.I),
              "0214: no anal — the anal finish fires her weapon (The Count's rule, held)")
        check(not any((b.get("props") or {}).get("npcId") == "npc_bastien" for b in all_blocks(cn.get("nodes", []), [])),
              "0214: Bastien is not in the bar")
        vids = [b for b in all_blocks(cn.get("nodes", []), []) if b.get("type") == "video"]
        check(len(vids) == 1 and (vids[0].get("props") or {}).get("file") == "sex/crew_night_t5.webm"
              and (vids[0].get("props") or {}).get("description") and (vids[0].get("props") or {}).get("search_queries"),
              "0214: one clip, sex/crew_night_t5.webm (a one-time screen takes one file), with description + queries")
        check(not any(b.get("type") == "video" for b in units[0]), "0214: the clip rides its beat, never the node's lead")
        cfg = (cn["nodes"][-1].get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("crew_back") == "set", "0214: sets crew_back")
    bc = [c for c in cards if c.get("npc_id") == "npc_bastien"]
    c24 = [c for c in bc if {"flag": "dace_met", "op": "is_true"} in c.get("when", []) and {"flag": "crew_back", "op": "is_false"} in c.get("when", [])]
    check(len(c24) == 1, "0214: Bastien card 24 (the night)")
    if jj:
        check(any(g.get("flag") == "crew_back" and g.get("op") == "is_true" for g in jj[0].get("goals", [])),
              "0214: card J gains the crew goal now that crew_back has a setter")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        check(fl.get("crew_back") == "unset", "0214: the dev jump must UNSET crew_back")

    # ── beat_0215 — B6, the owner band on loop_bastien_cot ────────────────────────────────────────────
    lb = canvases.get("loop_bastien_cot") or {}
    for nid in ("intro", "base_oral_bastien", "base_ride_bastien", "base_under_bastien"):
        nd = node(lb, nid)
        gs = [b for b in nd.get("blocks", []) if b.get("type") == "group"]
        first = (((gs[0].get("props") or {}).get("conditions") or {}).get("items") or []) if gs else []
        # FIRST, so it wins the if/elseif chain once his men are back — and it carries bastien_himself too, so
        # check_the_count.py §7 ("the FIRST band must be HIMSELF") stays true.
        check(has_flag(first, "crew_back", "is_true") and has_flag(first, "bastien_himself", "is_true"),
              f"0215: {nid}'s FIRST band must be the owner band (crew_back + bastien_himself)")
        if gs:
            prose = " ".join(b.get("content") or "" for b in all_blocks(gs[0], []) if b.get("type") == "paragraph")
            if nid != "intro":
                check(len(EXPLICIT.findall(prose)) >= 3, f"0215: {nid}'s owner band is an act screen — 3+ frozen words in its narration")
            check(not re.search(r"\banal\b|in her ass|up her ass|arse", prose, re.I), f"0215: {nid} — no anal in this loop (the drain)")
            dia = sum(len((b.get("content") or "").split()) for b in all_blocks(gs[0], []) if b.get("type") == "dialog")
            nar = sum(len((b.get("content") or "").split()) for b in all_blocks(gs[0], []) if b.get("type") in ("paragraph", "thought_bubble"))
            check(nar / max(dia, 1) <= 2.14, f"0215: {nid}'s owner band narration:dialogue {nar}/{dia}")
    iv = [b for b in all_blocks(node(lb, "intro").get("blocks", []), []) if b.get("type") == "video"]
    check([ (b.get("props") or {}).get("file") for b in iv] == ["sex/bastien_cot_owner_t5.webm"],
          "0215: the owner band's clip is ONE file on the intro (it plays once a session — the pool-per-screen rule)")
    if iv:
        check((iv[0].get("props") or {}).get("description") and (iv[0].get("props") or {}).get("search_queries"),
              "0215: the clip needs description + search_queries")

    # ── beat_0216 — the take ─────────────────────────────────────────────────────────────────────────
    # BUILT AS ITS OWN CARD, not a choice on underworld_strip_hub as blueprinted: that canvas is the single-exit
    # "Exit Underworld" card (a location exit, no choices). The take is a node of this card, which is LOCATED, so
    # vega_taken (read by triggers: rand_vega_street, cap_the_table) has a legal setter.
    for key, want in (("vega_damage", "Damage"), ("vega_habits", "Vega's habits learned")):
        check(labels.get(key, {}).get("label") == want,
              f"0216: {key} needs label '{want}' — the engine prints it in the locked choice's bracket (setup.traitLabel)")
    dv = canvases.get("activity_draw_her_out")
    check(dv is not None, "0216: activity_draw_her_out is missing")
    if dv:
        tr = dv.get("trigger") or {}
        check(tr.get("location") == "underworld_strip" and tr.get("is_repeatable") is True and not tr.get("npc")
              and not tr.get("requires_npc") and tr.get("trigger_mode", "manual") == "manual",
              "0216: a repeatable solo card on underworld_strip")
        its = items(dv)
        check(has_flag(its, "seam_known", "is_true") and has_flag(its, "vega_taken", "is_false"),
              "0216: visible from Kess's seam until the take (seam_known + vega_taken is_false)")
        ch = [c for c in (node(dv, "base").get("exit_block") or {}).get("choices", []) if c.get("text") == "Draw her out."]
        check(len(ch) == 1, "0216: one 'Draw her out.' choice")
        if ch:
            c = ch[0]
            ci = cond_items(c)
            need = {("fighting", "gte", 85), ("vega_habits", "gte", 4), ("vega_damage", "lt", 30)}
            got = {(i.get("trait_key"), i.get("operator"), i.get("value")) for i in ci if i.get("trait_key")}
            check(need <= got, f"0216: the take needs fighting gte 85, vega_habits gte 4, vega_damage lt 30 (got {got})")
            check(has_flag(ci, "crew_back", "is_true"), "0216: the take needs crew_back")
            check((c.get("conditions") or {}).get("version") == "1.0", "0216: conditions need version 1.0 (or fail OPEN)")
            check(c.get("show_when_locked") is True and c.get("locked_text"), "0216: show_when_locked with a voiced locked_text")
            check(not re.search(r"\d", c.get("locked_text") or ""), "0216: locked_text carries no number — the engine appends it")
            check((c.get("locked_text") or "").startswith("Draw her out"),
                  "0216: locked_text must name the action — a greyed choice renders locked_text, never its label")
            check(c.get("nodeId") in ("take", "activity_draw_her_out.take"), "0216: the choice plays .take")
        tk = node(dv, "take")
        casc = [b for b in tk.get("blocks", []) if b.get("type") == "cascade"]
        beats = casc[0]["props"]["beats"] if casc else []
        check(10 <= len(beats) <= 20, f"0216: the take is Tier-3, 10-20 beats (has {len(beats)})")
        text = " ".join(b.get("content") or "" for b in all_blocks(tk.get("blocks", []), []))
        for must in ("the wrong", "seam", "bag"):
            check(must in text, f"0216: the take must contain {must!r}")
        check(re.search(r"\b(dead|died|dies|killed)\b", text), "0216: some of the men die (LO: yes)")
        spk = dialog_speakers({"nodes": [tk]})
        check({"npc_vega", "npc_dace", "player"} <= spk, f"0216: Vega, Dace and Wren speak (got {sorted(map(str, spk))})")
        cfg = (tk.get("exit_block") or {}).get("config") or {}
        check(cfg.get("locationId") == "kess_berth", "0216: the take ends at Kess's berth (the table is next)")
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("vega_taken") == "set", "0216: sets vega_taken")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(dv.get("nodes", []), []) if b.get("type") == "image"}
        check({"scenes/the_take.jpg", "scenes/vega_in_the_room.jpg"} <= imgs, f"0216: the two take media slots (got {imgs})")
    c25 = [c for c in cards if c.get("npc_id") == "npc_bastien" and {"flag": "crew_back", "op": "is_true"} in c.get("when", [])
           and {"flag": "vega_taken", "op": "is_false"} in c.get("when", [])]
    check(len(c25) == 1, "0216: Bastien card 25 (his men are behind you)")
    rj = canvases.get("dev_jump_hunt_take")
    check(rj is not None, "0216: dev_jump_hunt_take (ready for the take) is missing")
    if rj:
        ch = ((rj.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        for f in ("site_offered", "the_site_open", "marrow_known", "site_ambushed", "seam_known", "cain_rule_heard",
                  "crew_asked", "undertow_open", "crew_refused", "dace_met", "crew_back"):
            check(fl.get(f) == "set", f"0216: the take jump must SET {f}")
        check(fl.get("vega_taken") == "unset", "0216: the take jump must UNSET vega_taken")
        ef = {e.get("trait"): e.get("value") for e in ch[0].get("effects", [])}
        check(ef.get("fighting") == 85 and ef.get("vega_habits") == 4 and ef.get("vega_damage") == 0 and ef.get("undertow_build") == 3,
              f"0216: the take jump seeds fighting 85, habits 4, damage 0, the bar built (got {[ef.get(k) for k in ('fighting','vega_habits','vega_damage','undertow_build')]})")
        check(ch[0].get("locationId") == "kess_berth", "0216: the take jump lands at the berth (the strip would roll a street fight)")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        check(fl.get("vega_taken") == "unset", "0216: the start jump must UNSET vega_taken")

    # ── beat_0217 — the table, card K, the end card, Bastien's section end ──────────────────────────────
    tb = canvases.get("cap_the_table")
    check(tb is not None, "0217: cap_the_table is missing")
    if tb:
        tr = tb.get("trigger") or {}
        its = items(tb)
        check(tr.get("location") == "kess_berth" and tr.get("is_repeatable") is False and (tr.get("priority") or 0) >= 11,
              "0217: a located one-shot auto-fire at kess_berth, pri 11+")
        check(has_flag(its, "vega_taken", "is_true") and has_flag(its, "vega_dismantled", "is_false"),
              "0217: gated vega_taken + vega_dismantled is_false")
        check(any(i.get("type") == "npc_at_location" and i.get("npc_id") == "npc_kess" for i in its), "0217: Kess present")
        spk = dialog_speakers(tb)
        check({"npc_kess", "npc_cain", "player"} <= spk, f"0217: Kess, Cain and Wren speak (got {sorted(map(str, spk))})")
        text = " ".join(b.get("content") or "" for b in all_blocks(tb.get("nodes", []), []))
        for must in ("Sabin", "cradle", "father", "hands"):
            check(must in text, f"0217: Cain's plan names {must!r} (the method, the equipment, the hands)")
        check("Undertow" not in text, "0217: no Undertow at Kess's")
        cfg = (tb["nodes"][-1].get("exit_block") or {}).get("config") or {}
        check({f.get("flag"): f.get("op") for f in cfg.get("flagEffects", [])}.get("vega_dismantled") == "set", "0217: sets vega_dismantled")
        e = {x.get("trait"): x for x in cfg.get("effects", [])}.get("vega_damage") or {}
        check(e.get("op") == "set" and e.get("value") == 0, "0217: Kess sees to her too (vega_damage set 0)")
        imgs = {(b.get("props") or {}).get("file") for b in all_blocks(tb.get("nodes", []), []) if b.get("type") == "image"}
        check("scenes/kess_table_vega.jpg" in imgs, "0217: scenes/kess_table_vega.jpg")
    ck = [c for c in cards if not c.get("npc_id") and {"flag": "vega_taken", "op": "is_true"} in c.get("when", [])
          and {"flag": "vega_dismantled", "op": "is_false"} in c.get("when", [])]
    check(len(ck) == 1, "0217: one story card K (vega_taken + vega_dismantled is_false)")
    cl = [c for c in cards if not c.get("npc_id") and {"flag": "vega_dismantled", "op": "is_true"} in c.get("when", [])]
    check(len(cl) == 1, "0217: one story end card L (vega_dismantled)")
    if cl:
        check(cl[0].get("terminal") is True and cl[0].get("terminal_text"), "0217: card L is terminal, with terminal_text")
        check("'" not in (cl[0].get("terminal_text") or ""), "0217: no apostrophe in terminal_text (SugarCube source-byte escaping)")
        check("That is where this build ends" in (cl[0].get("tip") or ""), "0217: the end card says where the build ends")
    terms = [c for c in cards if not c.get("npc_id") and c.get("terminal")]
    check(len(terms) == 1, f"0217: exactly one terminal Story-Goals card in the game, found {len(terms)}")
    b26 = [c for c in cards if c.get("npc_id") == "npc_bastien" and {"flag": "vega_taken", "op": "is_true"} in c.get("when", [])]
    check(len(b26) == 1 and b26[0].get("terminal") is True, "0217: Bastien's section ends on a terminal card at vega_taken")
    if j:
        ch = ((j.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        check(fl.get("vega_dismantled") == "unset", "0217: the start jump must UNSET vega_dismantled")
    if rj:
        ch = ((rj.get("nodes") or [{}])[0].get("exit_block") or {}).get("choices") or [{}]
        fl = {f.get("flag"): f.get("op") for f in ch[0].get("flagEffects", [])}
        check(fl.get("vega_dismantled") == "unset", "0217: the take jump must UNSET vega_dismantled")

    # ── every beat — narration : dialogue, PER VISIT, on every spoken screen of the chunk ──────────────────
    # The game's standing target is 2.14:1 (design_book "Register debt"); the skill's hard fail is 3:1. Measured
    # here so it is checked every build. PER VISIT: a node's top-level groups are exclusive bands, so each band is
    # measured with the node's ungrouped blocks, never summed with the others. A node with no NPC line is SOLO
    # (nobody there to speak — the skill's exemption) and is skipped. beat_0209's first ambush measured 3.29.
    CHUNK = ("cap_cain_comes", "cap_the_site", "cap_the_ambush", "cap_kess_seam", "kess_patch_up",
             "rand_vega_street", "activity_cain_trains", "activity_rebuild_undertow", "cap_crew_refuses", "cap_dace_price", "cap_the_crew_night", "activity_draw_her_out", "cap_the_table", "cap_rue_takes_the_list")

    def screens(node):
        """Every screen a visit can paint. Adjacent groups form ONE if/elseif chain (one of them renders);
        an ungrouped block between groups starts a new, independent chain. A screen is the ungrouped blocks
        plus one group from each chain, so every combination is measured."""
        import itertools
        bl = node.get("blocks", [])
        common = [b for b in bl if b.get("type") != "group"]
        chains, cur = [], []
        for b in bl:
            if b.get("type") == "group":
                cur.append(b)
            elif cur:
                chains.append(cur)
                cur = []
        if cur:
            chains.append(cur)
        if not chains:
            return [all_blocks(common, [])]
        return [all_blocks(common, []) + [x for g in combo for x in all_blocks(g, [])]
                for combo in itertools.product(*chains)]

    for cid in CHUNK:
        cv = canvases.get(cid)
        if not cv:
            continue
        for nd_ in cv.get("nodes", []):
            for k, bl in enumerate(screens(nd_)):
                if not any(b.get("type") == "dialog" and (b.get("props") or {}).get("npcId") for b in bl):
                    continue
                nar = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") in ("paragraph", "thought_bubble"))
                dia = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") == "dialog")
                check(nar / max(dia, 1) <= 2.14,
                      f"ratio: {cid}.{nd_['id']} screen {k} narration:dialogue {nar}/{dia} = {nar / max(dia, 1):.2f}, over 2.14")

    # The chunk's additions INSIDE shipped canvases: measure only what 0.2.3 wrote (a node of ours, or a band gated
    # on a 0.2.3 key), never the shipped screens around it — those are their own releases' responsibility.
    OURS_KEYS = ("undertow_build", "crew_asked", "undertow_open", "crew_refused", "dace_met", "crew_back", "vega_taken")

    def ours(group):
        return any((i.get("trait_key") or i.get("flag_key")) in OURS_KEYS and i.get("operator") in ("gte", "is_true")
                   for i in (((group.get("props") or {}).get("conditions") or {}).get("items") or []))

    for cid, nid in (("amb_bastien_cot", "vega"),):
        bl = all_blocks(node(canvases.get(cid), nid).get("blocks", []), [])
        nar = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") in ("paragraph", "thought_bubble"))
        dia = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") == "dialog")
        check(bl and nar / max(dia, 1) <= 2.14, f"ratio: {cid}.{nid} narration:dialogue {nar}/{dia}, over 2.14")
    for cid, nid in (("hub_sol_undertow", "base"), ("hub_colm_undertow", "base"), ("loop_colm_backroom", "intro")):
        nd = node(canvases.get(cid), nid)
        common = [b for b in nd.get("blocks", []) if b.get("type") != "group"]
        for g in [b for b in nd.get("blocks", []) if b.get("type") == "group" and ours(b)]:
            bl = all_blocks(common, []) + all_blocks(g, [])
            nar = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") in ("paragraph", "thought_bubble"))
            dia = sum(len((b.get("content") or "").split()) for b in bl if b.get("type") == "dialog")
            first = (all_blocks(g, []) or [{}])[0].get("content", "")[:40]
            check(nar / max(dia, 1) <= 2.14, f"ratio: {cid}.{nid} 0.2.3 band '{first}' {nar}/{dia}, over 2.14")

    if fails:
        print("THE HUNT GUARD: FAILED")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print("THE HUNT GUARD: OK")


if __name__ == "__main__":
    main()
