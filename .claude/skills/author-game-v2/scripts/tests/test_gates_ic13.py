"""IC13: `lint · toggles declared` — n/a when none is declared, and a toggle no canvas reads is listed."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def reader(cid, flag):
    return {"id": cid, "trigger": {"location": "room", "is_repeatable": True, "conditions": {
        "version": "1.0", "logic": "AND",
        "items": [{"type": "flag", "subject": "player", "flag_key": flag, "operator": "is_true"}]}},
        "nodes": [{"id": "a", "blocks": []}]}


def state(*flags):
    return {"want": {"toggles": [{"id": f, "flag": f, "turns_off": "x"} for f in flags]}}


def test_no_toggles_is_na():
    s, rows = gates.lint_toggles_declared({"canvases": []}, None)
    assert s.startswith("n/a") and rows == []
    s, rows = gates.lint_toggles_declared({"canvases": []}, {"want": {}})
    assert s.startswith("n/a") and rows == []


def test_a_read_toggle_is_counted_per_canvas():
    g = {"canvases": [reader("c1", "t_anal"), reader("c2", "t_anal")]}
    s, rows = gates.lint_toggles_declared(g, state("t_anal"))
    assert s == "1 declared · 1 read by at least one canvas"
    assert rows == ["t_anal (`t_anal`): read by 2 canvas(es)"]


def test_a_toggle_nothing_reads_switches_nothing():
    g = {"canvases": [reader("c1", "t_anal")]}
    s, rows = gates.lint_toggles_declared(g, state("t_anal", "t_public"))
    assert s == "2 declared · 1 read by at least one canvas"
    assert rows[1] == "t_public (`t_public`): read by 0 canvas(es) — switches nothing"
