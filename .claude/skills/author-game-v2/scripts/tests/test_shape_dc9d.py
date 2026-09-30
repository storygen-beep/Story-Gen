"""PRD v2 DC9d · H29: a person's meter is `{type, min, max}`; a bare description string WARNS (it
still declares the name for row 3) and never FAILS."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

ROW = "a person's meter has a type and range"


def verdict(meters):
    state = {"phase": "idea", "board": {"characters": [{"id": "npc_a", "meters": meters}]}}
    for name, ok, head, detail in shape.check(state, True)[0]:
        if name == ROW:
            return ok, detail
    raise AssertionError("row missing")


def test_typed_meter_passes():
    assert verdict({"want": {"type": "opens his step", "min": 0, "max": 100}})[0] is True


def test_bare_string_warns_not_fails():
    ok, detail = verdict({"want": "how far he will go"})
    assert ok == "warn" and "npc_a.want" in detail[0]


def test_a_warn_does_not_fail_the_run(capsys):
    import json
    import tempfile
    state = {"phase": "idea", "board": {"characters": [{"id": "npc_a", "meters": {"want": "x"}}]},
             "want": {"cast": [{"id": "npc_a", "age": 30}]}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(state, fh)
    assert shape.main([fh.name]) == 0
    assert "[WARN]" in capsys.readouterr().out


def test_no_meters_is_na():
    assert verdict({})[0] is None
