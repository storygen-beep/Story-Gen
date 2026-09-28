"""Switched-off canvases in the tally (LO, 2026-09-28): a gate that passes only because
`is_active = false` content is counted is a FAIL marked [off]; a gate n/a only because they are
off is "switched off, not judged"; a dispatcher's substitution target is live and left alone.
Nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

EXPLICIT = "His cock is in her mouth and she sucks his cock hard, cum on her tits and her cunt wet."


def game(active=True, dispatched=False):
    loops = [{"id": f"loop_{i}",
              "trigger": {"location": "room_a", "is_repeatable": True, "is_active": active},
              "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": EXPLICIT}]}]}
             for i in range(5)]
    canvases = list(loops)
    if dispatched:
        canvases.append({"id": "dispatch", "trigger": {
            "location": "room_a", "is_repeatable": True,
            "substitutions": [{"target_canvas_id": c["id"]} for c in loops]},
            "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "You wait."}]}]})
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"money": 10}},
            "locations": [{"id": "room_a"}], "canvases": canvases}


def scored(g):
    model, g2 = gates.build(copy.deepcopy(g))
    return gates.score(model, g2)


def row(results, name):
    return next(r for r in results if r["gate"] == name)


def test_a_pass_that_needs_switched_off_content_is_a_fail_marked_off():
    results, info = scored(game(active=False))
    r = row(results, "explicit in repeatable")
    assert not r["pass_"] and not r["na"] and r["switched_off"] == "fail"
    assert r["headline"].startswith("[off] passes only if switched-off canvases are counted")
    assert info["switched_off"] == [f"loop_{i}" for i in range(5)]


def test_a_game_with_nothing_switched_off_is_unchanged():
    results, info = scored(game(active=True))
    r = row(results, "explicit in repeatable")
    assert r["pass_"] and not r.get("switched_off") and info["switched_off"] == []


def test_a_substitution_target_is_live_and_left_alone():
    results, info = scored(game(active=False, dispatched=True))
    assert info["switched_off"] == []
    assert not any(r.get("switched_off") for r in results)


def test_na_only_because_switched_off_is_not_judged(monkeypatch):
    def fake_run_gates(model, g, state=None):
        off = any((c.get("trigger") or {}).get("is_active") is False for c in g.get("canvases") or [])
        return [dict(gate="g", pass_=not off, na=off, few=False, n=None, parked=False,
                     headline="judged", detail=[])]
    monkeypatch.setattr(gates, "run_gates", fake_run_gates)
    results, info = scored(game(active=False))
    r = results[0]
    assert r["switched_off"] == "na" and not r["pass_"] and not r["na"]
    assert r["headline"].startswith("switched off, not judged — with them on: PASS")


def test_the_tally_counts_off_rows_as_not_passing():
    results, _ = scored(game(active=False))
    npass, nfail, _npark, _nfew, _nna, denom = gates.tally_counts(results)
    off = sum(1 for r in results if r.get("switched_off"))
    assert off >= 1 and npass + nfail + _npark + _nfew == denom
