#!/usr/bin/env python3
"""
THE WAY DOWN (0.2.2) — route-consistency guard.

⚠️ WHY THIS EXISTS. Renner's drain payload (renner_route_canvas) is a DESCRIPTION of the node graph in
bunker_route. They are two separate pieces of TOML written at different times. Change one and forget the
other and the game lies to the player with a completely green build — the prose-truth failure. The route
is also deliberately not printed on the Quests page, so a player who follows Renner's directions and ends
up in a guard room has no way to tell whether they misremembered or the game is wrong.

Run from the repo root, after a merge:
    python games/vesper/tests/check_bunker_route.py
Exits 0 on pass, 1 on any failure.
"""
import re
import sys
import os

try:
    import tomllib
except ModuleNotFoundError:                      # py<3.11
    import tomli as tomllib                      # type: ignore

GAME = os.path.join(os.path.dirname(__file__), "..", "toml_phases", "7_final_game.toml")

# The route, as the answer key. Each row: turn node, the CORRECT choice's target, the guard room the
# wrong doors lead to, and a word that must appear in Renner's mouth for that turn.
ROUTE = [
    ("base", "t1", "g1", "stair"),
    ("t1",   "t2", "g2", "pump"),
    ("t2",   "t3", "g3", "ring"),
    ("t3",   "t4", "g4", "far gate"),
    ("t4",   "t5", "g5", "conduit"),
]
# Where a caught room's free stealth back-out must return her to (the junction she just left).
BACKOUT = {"g1": "bunker_route.base", "g2": "bunker_route.t1", "g3": "bunker_route.t2",
           "g4": "bunker_route.t3",   "g5": "bunker_route.t4"}

fails: list[str] = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def main() -> int:
    with open(GAME, "rb") as fh:
        doc = tomllib.load(fh)

    canvases = {c["id"]: c for c in doc.get("canvases", [])}
    for cid in ("bunker_route", "bunker_guards", "bunker_descent",
                "renner_route_canvas", "bunker_bastien", "cap_the_extraction"):
        check(cid in canvases, f"canvas missing: {cid}")
    if fails:
        return report()

    nodes = {c: {n["id"]: n for n in canvases[c].get("nodes", [])} for c in canvases}

    def choices(canvas, node):
        nd = nodes[canvas].get(node)
        if not nd:
            return []
        eb = nd.get("exit_block") or {}
        return eb.get("choices") or []

    def targets(canvas, node):
        out = []
        for ch in choices(canvas, node):
            if ch.get("targetType") == "node" and ch.get("nodeId"):
                nid = ch["nodeId"]
                out.append(nid if "." in nid else f"{canvas}.{nid}")
            elif ch.get("targetType") == "location":
                out.append(f"@{ch.get('locationId')}")
        return out

    # 1 — the correct path is walkable end to end, and each wrong door lands in that turn's own room.
    for turn, nxt, guard, _ in ROUTE:
        t = targets("bunker_route", turn)
        check(f"bunker_route.{nxt}" in t,
              f"route: {turn} has no correct exit to {nxt} (targets={t})")
        check(f"bunker_guards.{guard}" in t,
              f"route: {turn} has no wrong-turn exit to bunker_guards.{guard} (targets={t})")
        for tgt in t:
            if tgt.startswith("bunker_guards."):
                check(tgt == f"bunker_guards.{guard}",
                      f"route: {turn} leaks into {tgt}; every wrong door at this turn must land in {guard}")

    # 2 — every caught room offers exactly the four documented ways out.
    for _, _, guard, _ in ROUTE:
        t = targets("bunker_guards", guard)
        check(BACKOUT[guard] in t, f"{guard}: stealth back-out must return to {BACKOUT[guard]} (targets={t})")
        check(f"bunker_guards.{guard}_down" in t, f"{guard}: no fight branch to {guard}_down")
        check(f"bunker_guards.{guard}_taken" in t, f"{guard}: no emitter branch to {guard}_taken")
        check("@facility_ruins" in t, f"{guard}: no flee exit to facility_ruins")

        # the emitter must SPEND a shot via `costs` (engine-enforced affordability), not a bare condition
        emit = [c for c in choices("bunker_guards", guard) if c.get("nodeId") == f"{guard}_taken"]
        check(bool(emit), f"{guard}: emitter choice not found")
        if emit:
            costs = emit[0].get("costs") or []
            check(any(c.get("trait") == "arousal_charge" and c.get("value") == 1 for c in costs),
                  f"{guard}: emitter choice must cost 1 arousal_charge (got {costs})")

        # the free back-out must be budgeted by bunker_stealth_used, or it is free every room
        back = [c for c in choices("bunker_guards", guard) if c.get("nodeId") == BACKOUT[guard]]
        if back:
            raw = str(back[0].get("conditions", ""))
            check("bunker_stealth_used" in raw,
                  f"{guard}: back-out is not gated on bunker_stealth_used — it would be free every room")

        # the caught scene must carry its own pool, and pools must not be shared
        taken = nodes["bunker_guards"].get(f"{guard}_taken")
        check(taken is not None, f"{guard}_taken node missing")

    # 3 — one asset, one block: every bunker pool_dir is unique
    pools = re.findall(r'pool_dir = "(sex/bunker_[^"]+)"', open(GAME, encoding="utf-8").read())
    check(len(pools) == len(set(pools)), f"pool_dir reused across blocks: {pools}")
    check(len(pools) == 5, f"expected 5 bunker pools, found {len(pools)}")

    # 4 - PROSE TRUTH, CHECKED ON THE MNEMONIC LINE, NOT ON THE WHOLE SPEECH.
    #
    # WARNING: the first cut of this check was useless and a negative test caught it. It asked whether each
    # tell appeared ANYWHERE in the node. Deleting "conduit" from the sentence that actually gives turn five
    # still passed, because the word also appears in the surrounding description. A guard that cannot fail
    # is not a guard. What matters is the closing summary - the five clauses the player writes down - so
    # that line is located explicitly and every tell must appear IN IT, IN ORDER. Both the drain payload
    # and the re-ask carry their own copy, and the two must not drift apart either.
    def mnemonic(canvas, node):
        blob = str(nodes[canvas][node])
        best = None
        for line in re.findall(r"'([^']{40,})'", blob) + re.findall(r'"([^"]{40,})"', blob):
            low = line.lower()
            if "stair" in low and "ramp" in low:
                if best is None or len(line) < len(best):
                    best = low
        return best

    for canvas, node, label in (("renner_route_canvas", "base", "the drain payload"),
                                ("renner_control_canvas", "route_recall", "the re-ask")):
        line = mnemonic(canvas, node)
        check(line is not None,
              "prose-truth: " + label + " has no summary line naming both the stair and the ramp")
        if line:
            pos = -1
            for _, _, _, tell in ROUTE:
                idx = line.find(tell)
                check(idx != -1,
                      "prose-truth: " + label + " route line never says '" + tell + "' - it is not this route")
                if idx != -1:
                    check(idx > pos, "prose-truth: " + label + " gives '" + tell + "' out of order")
                    pos = idx

    # 5 — the route must NOT be on the Quests page; printing it deletes the mechanic.
    for card in doc.get("quest_cards", []):
        blob = f"{card.get('text','')} {card.get('tip','')}".lower()
        hits = sum(t in blob for t in ("left at the pump", "right at the ring", "the far gate", "conduit turns into"))
        check(hits < 2, f"a quest card prints the route ({hits} clauses): {blob[:90]}")

    # 6 — the door's full on-ramp gate, and that it closes for good after the rescue.
    raw_gate = str(canvases["bunker_descent"].get("trigger", {}).get("conditions", ""))
    for flag in ("rescue_agreed", "route_learned", "link_built", "bastien_rescued"):
        check(flag in raw_gate, f"bunker_descent is not gated on {flag}")

    # 7 - BASTIEN AT THE COT, BY SCHEDULE, WITHOUT THE LEAK (rev 225).
    #
    # Until 2026-09-18 this section forbade any row at the_cot: a row carried no conditions and the nav badge
    # is schedule-driven, so a row there parked Bastien's face on the cot's card in every 1b+ save, rescued or
    # not. The engine now reads an optional `when` on a row (tests/test_npc_schedule_when.py). So the rule is
    # now the positive one LO asked for - his portrait at the cot - plus the gate that keeps it honest:
    #   - a row at the_cot exists (a portrait card renders ONLY for an NPC a live row places there,
    #     renderNpcPortraits), and it is gated bastien_at_cot is_true with version "1.0" (versionless fails
    #     OPEN, which would be the old leak with extra steps);
    #   - the back-room row is gated raid_done is_false, so it stops existing once the room does and the
    #     Schedules page stops listing him in a building nobody can enter;
    #   - ANY row, anyone's, at the_cot carries a versioned `when` - the cot is reachable in every save;
    #   - amb_bastien_cot is his portrait hub (npc + requires_npc), not a solo link.
    def gated(row, flag, want_true):
        w = row.get("when") or {}
        if str(w.get("version") or "") != "1.0":
            return False
        return any(isinstance(it, dict) and it.get("type") == "flag" and it.get("flag_key") == flag
                   and it.get("operator") == ("is_true" if want_true else "is_false")
                   for it in w.get("items") or [])

    bastien = next((n for n in doc.get("npcs", []) if n.get("id") == "npc_bastien"), {})
    brows = bastien.get("schedules") or []
    cot_rows = [r for r in brows if r.get("location") == "the_cot"]
    check(cot_rows, "npc_bastien has no schedule row at the_cot - his portrait card cannot render there")
    for r in cot_rows:
        check(gated(r, "bastien_at_cot", True),
              "npc_bastien's the_cot row is not gated `bastien_at_cot is_true` (version 1.0) - "
              "his face would park on the cot's nav card in every save, rescued or not")
    for r in [r for r in brows if r.get("location") == "bastien_backroom"]:
        check(gated(r, "raid_done", False),
              "npc_bastien's bastien_backroom row is not gated `raid_done is_false` - it outlives the room")
    for npc in doc.get("npcs", []):
        for row in npc.get("schedules", []) or []:
            if row.get("location") == "the_cot":
                check(str((row.get("when") or {}).get("version") or "") == "1.0",
                      f"{npc.get('id')} has an UNGATED schedule row at the_cot - badge leaks into every save")
        if npc.get("id") == "npc_loder":
            check(not (npc.get("schedules") or []),
                  "npc_loder must have ZERO schedule rows (he exists only inside a bunker that closes)")
    amb = (canvases.get("amb_bastien_cot") or {}).get("trigger") or {}
    check(amb.get("npc") == "npc_bastien" and amb.get("requires_npc") == "npc_bastien",
          "amb_bastien_cot is not Bastien's portrait hub (needs npc + requires_npc = npc_bastien)")


    # 8 - THE DEV JUMPS MUST START WHERE 0.2.1 ENDS.
    #
    # WARNING: this shipped broken at beat_0188. Both jumps copied their seed from dev_jump_whose_hand_end,
    # which lands at 0.2.1 beat 13 and deliberately UNSETS the release's ending flags. The seed was read by
    # flag NAME without its op, so "two_men_done is in the list" was mistaken for "two_men_done is set".
    # Clicking "0.2.2: Cain brings the news" then showed 0.2.1's card A (activity_say_yes) instead of the
    # news, because cap_bastien_alive needs two_men_done. The check below replays each jump's flagEffects in
    # order (last write wins) and evaluates the real trigger conditions against the result.
    END_OF_021 = ["third_located", "capstone_failed", "vesper_named",
                  "cain_absent_confirmed", "cain_came_along", "two_men_done"]

    def seeded_flags(jump_id):
        state = {}
        for node in canvases[jump_id].get("nodes", []):
            for ch in (node.get("exit_block") or {}).get("choices", []) or []:
                for fe in ch.get("flagEffects", []) or []:
                    state[fe["flag"]] = (fe.get("op") == "set")
        return state

    def flag_items_hold(canvas_id, state):
        conds = (canvases[canvas_id].get("trigger") or {}).get("conditions") or {}
        for it in conds.get("items", []):
            if it.get("type") != "flag":
                continue
            want = it.get("operator") == "is_true"
            if state.get(it["flag_key"], False) != want:
                return False, it["flag_key"]
        return True, None

    for jump in ("dev_jump_way_down_start", "dev_jump_way_down_door"):
        check(jump in canvases, f"dev jump missing: {jump}")
        if jump not in canvases:
            continue
        st = seeded_flags(jump)
        for f in END_OF_021:
            check(st.get(f) is True, f"{jump}: leaves 0.2.1's '{f}' unset - it starts mid-0.2.1, not at its end")
        ok, _ = flag_items_hold("activity_say_yes", st)
        check(not ok, f"{jump}: 0.2.1's card A (activity_say_yes) is still live in the seeded state")

    if "dev_jump_way_down_start" in canvases:
        st = seeded_flags("dev_jump_way_down_start")
        ok, bad = flag_items_hold("cap_bastien_alive", st)
        check(ok, f"dev_jump_way_down_start: cap_bastien_alive cannot fire from the seeded state (fails on {bad})")

    # 9 - THE DEV JUMPS MUST CARRY THE WARDROBE A REAL PLAYER HAS BY THE END OF 0.2.1.
    #
    # WARNING: this shipped broken too, and LO found it in play: "I dont see the Dock cover at all in the
    # change cloths menu." A dev jump starts from a fresh StoryInit, so canvas_opening_morning's
    # `add cover_dockhand` never runs, and both 0.2.2 jumps carried flags and traits but NO wardrobeEffects.
    # She owned only the four initial garments; hub_depot_floor then substitutes the no-cover squint, so the
    # drain, route_learned and everything after beat 2 could not be reached from the jump.
    # The required set is DERIVED, not listed: every garment any non-dev canvas grants with `add`. Nothing in
    # this game ever removes a garment, so a real end-of-0.2.1 player owns every one of them. A garment
    # added in a later release joins this set automatically and the jumps must follow it.
    def is_dev(c):
        return "dev_mode_enabled" in str((c.get("trigger") or {}).get("conditions", ""))

    def adds_in(c):
        out = set()
        for node in c.get("nodes", []):
            eb = node.get("exit_block") or {}
            pools = [eb.get("config") or {}] + list(eb.get("choices") or [])
            for holder in pools:
                for we in holder.get("wardrobeEffects", []) or []:
                    if we.get("action") == "add":
                        out.add(we.get("item_id"))
        return out

    def wardrobe_ops(c):
        ops = []
        for node in c.get("nodes", []):
            for ch in (node.get("exit_block") or {}).get("choices", []) or []:
                ops += [(we.get("action"), we.get("item_id")) for we in ch.get("wardrobeEffects", []) or []]
        return ops

    initial = {i["id"] for i in doc.get("clothing", []) if i.get("initial")}
    granted_in_play = set()
    for c in canvases.values():
        if not is_dev(c):
            granted_in_play |= adds_in(c)
    check("cover_dockhand" in granted_in_play, "sanity: nothing in play grants cover_dockhand")

    for jump in ("dev_jump_way_down_start", "dev_jump_way_down_door"):
        if jump not in canvases:
            continue
        ops = wardrobe_ops(canvases[jump])
        owned = initial | {i for a, i in ops if a == "add"}
        for item in sorted(granted_in_play - owned):
            check(False, f"{jump}: never grants '{item}' - a real end-of-0.2.1 player owns it"
                         + (" (the coveralls: Renner's whole hub gates on it)" if item == "cover_dockhand" else ""))
        for a, i in ops:
            if a == "equip":
                check(i in owned, f"{jump}: equips '{i}' without owning it")

    # 10 - NO EARLIER RELEASE'S ONE-SHOT MAY STILL BE ARMED IN A JUMP, AT ANY PLACE 0.2.2 SENDS THE PLAYER,
    #      AND THE 0.2.2 PATH ITSELF MUST BE OPEN.
    #
    # WARNING: the third seed defect, and the widest. 0.2.1 never went back to Renner or the burned yard, so
    # dev_jump_whose_hand_end never carried their Act-1 state - and 0.2.2 sends the player straight back to
    # both. Measured in the built game: renner_hired false (his hub cannot open), npc_renner corruption 0
    # (no office loop), drains_done 0 (the finisher would replay the ACT-1 first extraction, not .again),
    # yard_depth 3 with finds 1-3 unset (the Act-1 finds would replay), emitter never found or repaired.
    # This replays each jump's effects the way the engine does and evaluates real trigger conditions.
    NEW_0_2_2 = {"cap_bastien_alive", "activity_go_after_him", "cap_back_into_cover", "renner_route_canvas",
                 "yard_find_4", "kess_makes_the_link", "bunker_descent", "bunker_route", "bunker_guards",
                 "bunker_sides", "bunker_bastien", "cap_the_extraction", "cap_bastien_at_the_cot",
                 "amb_bastien_cot"}
    PLACES = {"the_cot", "renner_depot", "the_anchor", "renner_burned_yard", "kess_berth",
              "facility_ruins", "the_waterfront"}
    init_p = dict((doc.get("player") or {}).get("core_traits", {}))
    npc0 = {n["id"]: dict(n.get("core_traits", {})) for n in doc.get("npcs", [])}

    def replay(jump_id):
        fl, tr, nt = {}, dict(init_p), {k: dict(v) for k, v in npc0.items()}
        for node in canvases[jump_id].get("nodes", []):
            for ch in (node.get("exit_block") or {}).get("choices", []) or []:
                for fe in ch.get("flagEffects", []) or []:
                    fl[fe["flag"]] = (fe.get("op") == "set")
                for e in ch.get("effects", []) or []:
                    tgt = tr if e.get("targetType") == "player" else nt.setdefault(e.get("npcId"), {})
                    v = e.get("value") if isinstance(e.get("value"), (int, float)) else 0
                    tgt[e["trait"]] = v if e.get("op") == "set" else tgt.get(e["trait"], 0) + v
        return fl, tr, nt

    def holds(conds, st):
        fl, tr, nt = st
        for it in (conds or {}).get("items", []):
            t = it.get("type")
            if t == "flag" and fl.get(it["flag_key"], False) != (it["operator"] == "is_true"):
                return False
            if t == "trait":
                src = tr if it.get("subject") == "player" else nt.get(it.get("npc_id"), {})
                val, x, op = src.get(it["trait_key"], 0), it.get("value", 0), it["operator"]
                if not {"gte": val >= x, "gt": val > x, "lt": val < x, "lte": val <= x,
                        "eq": val == x, "neq": val != x}.get(op, True):
                    return False
        return True     # clothing / presence / time are not modelled; they only ever make this stricter

    def path_gate(canvas_id, node_id, target):
        for ch in (nodes[canvas_id][node_id].get("exit_block") or {}).get("choices", []) or []:
            if ch.get("nodeId") == target:
                return ch.get("conditions")
        return None

    for jump in ("dev_jump_way_down_start", "dev_jump_way_down_door"):
        if jump not in canvases:
            continue
        st = replay(jump)
        for cid, c in canvases.items():
            trg = c.get("trigger") or {}
            if cid in NEW_0_2_2 or trg.get("location") not in PLACES:
                continue
            if trg.get("is_repeatable", True) or trg.get("substitution_only") or is_dev(c):
                continue
            check(not holds(trg.get("conditions"), st),
                  f"{jump}: an earlier release's one-shot '{cid}' is still armed at {trg.get('location')}")

    # the 0.2.2 Renner path must be open from the NEWS jump: hub -> office loop -> anal -> .again
    st = replay("dev_jump_way_down_start")
    fl, tr, nt = st
    check(holds((canvases["hub_depot_floor"].get("trigger") or {}).get("conditions"), st),
          "dev_jump_way_down_start: hub_depot_floor cannot open (renner_hired)")
    check(holds(path_gate("hub_depot_floor", "base", "loop_renner_office_sex.intro"), st),
          "dev_jump_way_down_start: the office loop is shut (office/oral/corruption>=40)")
    check(nt.get("npc_renner", {}).get("corruption", 0) >= 50,
          "dev_jump_way_down_start: Renner's corruption is under 50, so the ass finish that IS the drain is locked")
    check(tr.get("drains_done", 0) >= 1,
          "dev_jump_way_down_start: drains_done < 1 routes the drain to Act 1's .intro, not .again (the 0.2.2 ask)")
    check(fl.get("arousal_weapon_ready") and fl.get("has_arousal_weapon"),
          "dev_jump_way_down_start: the emitter was never found or repaired, so no caught-beat can be reached")

    return report()


def report() -> int:
    if fails:
        print("BUNKER-ROUTE GUARD: FAILED")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("BUNKER-ROUTE GUARD: OK — five turns walkable, every wrong door lands in its own room, "
          "the emitter spends a shot, the back-out is budgeted, Renner's directions match the rooms, "
          "the mnemonic names all five turns in order in both the drain and the re-ask, "
          "the route is not printed on the Quests page, and both dev jumps start at the end of 0.2.1 "
          "with the wardrobe a real player has by then.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
