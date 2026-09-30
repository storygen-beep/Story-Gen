"""PRD v2 DC2a · B2: shape.py's "every person is an adult". Ages live in `want.cast[]`; a person with no
age, a non-number age or an age under 18 FAILS in lenient and strict mode alike (LO, 2026-09-30), and a
board character missing from `want.cast` has no age."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

ROW = "every person is an adult"


def verdict(state, strict=False):
    for name, ok, head, detail in shape.check(state, strict)[0]:
        if name == ROW:
            return ok, detail
    raise AssertionError("row missing")


def ledger(cast, board_ids=()):
    return {"phase": "idea", "want": {"cast": cast},
            "board": {"characters": [{"id": i} for i in board_ids]}}


def test_adults_pass():
    ok, detail = verdict(ledger([{"id": "npc_a", "age": 18}, {"id": "npc_b", "age": 41}], ["npc_a"]))
    assert ok is True and detail == []


def test_missing_age_fails_lenient_and_strict():
    st = ledger([{"id": "npc_a", "keeps": "want + warmth"}])
    for strict in (False, True):
        ok, detail = verdict(st, strict)
        assert ok is False and "no age" in detail[0]


def test_under_18_fails():
    ok, detail = verdict(ledger([{"id": "npc_a", "age": 17}]))
    assert ok is False and "under 18" in detail[0]


def test_string_age_fails():
    ok, detail = verdict(ledger([{"id": "npc_a", "age": "19"}]))
    assert ok is False and "must be a number" in detail[0]


def test_board_person_without_cast_entry_fails():
    ok, detail = verdict(ledger([{"id": "npc_a", "age": 30}], ["npc_a", "npc_b"]))
    assert ok is False and detail == ["npc_b: on the board but not in want.cast — no age declared"]


def test_nobody_declared_is_na():
    assert verdict({"phase": "idea"})[0] is None
