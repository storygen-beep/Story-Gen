"""IC16: `shape.py`, checkpoint A. A full spine passes; each check fails on its own defect; an
empty ledger is n/a while the spine is being written and FAILS once the game finishes it (LO)."""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

WIN = {"days": ["Mon", "Wed"], "from": "18:00", "to": "20:00"}


def full():
    return {
        "phase": "idea",
        "want": {"hold_kind": "bill", "promise": {"goal": "her own flat", "date": "week 6"},
                 "cast": [{"id": "npc_a", "age": 34}, {"id": "npc_b", "age": 22}]},
        "spine": {"pages": [{"id": f"SP{i}", "status": "READY", "signed_by": "LO",
                             "drafted_at": "2026-09-27", "signed_at": "2026-09-28"}
                            for i in range(1, 8)]},
        "dependencies": [{"from": {"npc": "npc_b", "step": 1}, "needs": {"npc": "npc_a", "step": 2}}],
        "board": {
            "ascent_tiers": ["nerve"],
            "locations": [{"id": "bar"}, {"id": "flat"}],
            "economy": {"currency": "money", "obligation_amount": 100, "week_income": 150},
            "characters": [
                {"id": "npc_a", "meters": {"trust": "access"},
                 "schedule": [{"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "21:00"},
                              {"where": "flat", "weekdays": ["Mon", "Wed"], "from": "18:00", "to": "23:00"}],
                 "ladder": {"counter": "a_stage", "steps": [
                    {"n": 1, "canvas": "a_1", "where": "bar", "when": dict(WIN),
                     "gate": [{"trait": "nerve", "op": "gte", "value": 10}], "hint": "He is at the bar."},
                    {"n": 2, "canvas": "a_2", "where": "flat", "when": dict(WIN),
                     "gate": [{"flag": "met_a"}], "hint": "He asked you up."}]}},
                {"id": "npc_b",
                 "schedule": [{"where": "bar", "weekdays": ["Mon", "Wed"], "from": "18:00", "to": "20:00"}],
                 "ladder": {"counter": "b_stage", "steps": [
                    {"n": 1, "canvas": "b_1", "where": "bar", "when": dict(WIN),
                     "gate": [{"trait": "trust", "op": "gte", "value": 5}], "hint": "She waits after close."}]}},
            ],
        },
        "release_page": {"people": ["npc_a", "npc_b"], "door": {"canvas": "a_2", "choice": "Go up"},
                         "weeks": 4, "promise_alive": "the landlord names a date"},
    }


def rows(state, strict=True):
    return {n: (ok, h, d) for n, ok, h, d in shape.check(state, strict)[0]}


def failing(state, strict=True):
    return [n for n, (ok, _h, _d) in rows(state, strict).items() if ok is False]


def test_a_full_spine_passes_every_check():
    r = rows(full())
    assert failing(full()) == []
    assert all(ok is True for ok, _h, _d in r.values())
    assert shape.check(full(), True)[1] == ["met_a"]          # flags listed, not judged


def test_an_empty_ledger_finishing_the_spine_fails():
    assert shape.is_strict({"phase": "idea"}, finish=True)
    bad = failing({"phase": "idea"}, strict=True)
    assert {"everyone on the release page has a ladder", "every step has a guidance line",
            "the door is a declared step", "the promise has a beat this release",
            "every spine page is signed"} <= set(bad)


def test_an_empty_ledger_while_the_spine_is_written_is_na():
    assert not shape.is_strict({"phase": "idea"})
    assert failing({"phase": "idea"}, strict=False) == []


def test_past_the_spine_is_strict():
    assert all(shape.is_strict({"phase": p}) for p in ("spine", "board", "sheets", "release"))


def broken(edit):
    s = full()
    edit(s)
    return failing(s)


def test_each_check_fails_on_its_defect():
    ch = lambda s: s["board"]["characters"]
    cases = {
        "a step's place is declared": lambda s: (ch(s)[0]["ladder"]["steps"][0].update(where="roof"),
                                                 ch(s)[0]["schedule"].append(dict(ch(s)[0]["schedule"][0],
                                                                                  where="roof"))),
        "a step's hours are a window": lambda s: ch(s)[0]["ladder"]["steps"][0].update(when={"days": ["Mon"]}),
        "a step's variables are declared": lambda s: ch(s)[0]["ladder"]["steps"][0].update(
            gate=[{"trait": "lust", "op": "gte", "value": 1}]),
        "dependencies resolve": lambda s: s["dependencies"].append(
            {"from": {"npc": "npc_a", "step": 2}, "needs": {"npc": "npc_b", "step": 1}}),
        "the pressure can be met": lambda s: s["board"]["economy"].update(week_income=50),
        "everyone on the release page has a ladder": lambda s: s["release_page"]["people"].append("npc_c"),
        "every step has a guidance line": lambda s: ch(s)[1]["ladder"]["steps"][0].pop("hint"),
        "the door is a declared step": lambda s: s["release_page"]["door"].update(canvas="nowhere"),
        "the promise has a beat this release": lambda s: s["release_page"].pop("promise_alive"),
        "every spine page is signed": lambda s: s["spine"]["pages"][0].pop("signed_at"),   # D13: unsigned, not same-day
        "the person is there at the step's hour": lambda s: ch(s)[1]["schedule"][0].update(weekdays=["Mon"]),
    }
    for name, edit in cases.items():
        assert broken(edit) == [name], name


def test_a_shortfall_on_purpose_passes():
    s = full()
    s["board"]["economy"].update(week_income=50, shortfall="she is meant to fall behind and ask")
    assert failing(s) == []
