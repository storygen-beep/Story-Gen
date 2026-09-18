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

    # 7 — no [[npcs.schedules]] row may point at the_cot: a row is unconditional and the nav badge is not
    #     canvas-gated, so it would park Bastien's face there in saves where he was never rescued.
    for npc in doc.get("npcs", []):
        for row in npc.get("schedules", []) or []:
            check(row.get("location") != "the_cot",
                  f"{npc.get('id')} has a schedule row at the_cot — badge leaks into every save")
        if npc.get("id") == "npc_loder":
            check(not (npc.get("schedules") or []),
                  "npc_loder must have ZERO schedule rows (he exists only inside a bunker that closes)")

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
          "and the route is not printed on the Quests page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
