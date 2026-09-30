"""CK5 (PRD v2, 2026-09-30): `shape.py`.

  H7  · lenient mode with no READY page is n/a, not "0/7 READY" PASS.
  D13 · (LO decided) no day-after compare; a READY page must still be signed.
  H11 · place checks read `release_page.places` when present, else `board.locations`.
  I12 · the pressure walks `board.pressure.stages`; `obligation_moves` only prints.
  I13 · `board.characters[].schedule` must fully cover each step's window (the union of rows,
        past midnight included); opening steps are exempt. Plus the shared helper
        `gates._window_uncovered`.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import shape  # noqa: E402

WIN = {"days": ["Mon", "Wed"], "from": "18:00", "to": "20:00"}


def base():
    return {
        "phase": "idea",
        "board": {
            "locations": [{"id": "bar"}, {"id": "flat"}, {"id": "docks"}],
            "characters": [{"id": "npc_a", "ladder": {"counter": "a_stage", "steps": [
                {"n": 1, "canvas": "a_1", "where": "bar", "when": dict(WIN), "gate": [], "hint": "h"}]}}],
        },
        "release_page": {"people": ["npc_a"], "door": {"canvas": "a_1", "choice": "x"}},
    }


def rows(state, strict=False):
    return {n: (ok, h, d) for n, ok, h, d in shape.check(state, strict)[0]}


def pages(status="READY", **kw):
    return {"pages": [dict({"id": f"SP{i}", "status": status}, **kw) for i in range(1, 8)]}


# ── H7 ────────────────────────────────────────────────────────────────────────

def test_no_ready_page_is_na_while_lenient():
    s = base()
    s["spine"] = pages(status="REVIEW")
    ok, head, _ = rows(s)["every spine page is signed"]
    assert ok is None and "no spine page READY yet" in head


def test_no_ready_page_fails_when_strict():
    s = base()
    s["spine"] = pages(status="REVIEW")
    assert rows(s, strict=True)["every spine page is signed"][0] is False


# ── D13 ───────────────────────────────────────────────────────────────────────

def test_signed_the_day_it_was_drafted_passes():
    s = base()
    s["spine"] = pages(signed_by="LO", drafted_at="2026-09-29", signed_at="2026-09-29")
    assert rows(s, strict=True)["every spine page is signed"][0] is True


def test_ready_but_unsigned_still_fails():
    s = base()
    s["spine"] = pages(signed_by="LO", drafted_at="2026-09-29")
    ok, _h, detail = rows(s)["every spine page is signed"]
    assert ok is False and detail[0] == "SP1: READY but not signed"


# ── H11 ───────────────────────────────────────────────────────────────────────

def test_a_step_at_a_place_cut_from_the_release_fails():
    s = base()
    s["release_page"]["places"] = ["flat", "docks"]
    ok, head, detail = rows(s)["a step's place is declared"]
    assert ok is False and "release_page.places" in head
    assert detail == ["npc_a step 1: `bar` is not in release_page.places"]


def test_without_release_places_the_board_is_read():
    ok, head, _ = rows(base())["a step's place is declared"]
    assert ok is True and "board.locations" in head


# ── I12 ───────────────────────────────────────────────────────────────────────

def money(stages=None, moves=None):
    s = base()
    s["want"] = {"hold_kind": "bill"}
    s["board"]["economy"] = {"obligation_amount": 100, "week_income": 120}
    if moves:
        s["board"]["economy"]["obligation_moves"] = moves
    if stages:
        s["board"]["pressure"] = {"stages": stages}
    s["release_page"]["weeks"] = 4
    return rows(s)["the pressure can be met"]


def test_a_rising_bill_is_walked_week_by_week():
    ok, head, _ = money(stages=[{"amount": 100, "after_total_paid": 0},
                                {"amount": 150, "after_total_paid": 200}])
    assert ok is False
    assert "480 earnable against 500 owed (rising in 2 stage(s))" in head


def test_without_stages_it_is_the_start_times_the_weeks():
    ok, head, _ = money()
    assert ok is True and "480 earnable against 400 owed (flat)" in head


def test_obligation_moves_prints_and_is_not_judged():
    ok, head, _ = money(moves="the boiler adds 15 a week")
    assert ok is True and head.endswith("moves: the boiler adds 15 a week")


# ── I13 ───────────────────────────────────────────────────────────────────────

def cover(schedule, when=None, fires_from=None):
    s = base()
    s["board"]["characters"][0]["schedule"] = schedule
    step = s["board"]["characters"][0]["ladder"]["steps"][0]
    if when:
        step["when"] = when
    if fires_from:
        step["fires_from"] = fires_from
    return rows(s)["the person is there at the step's hour"]


def test_a_covered_step_passes():
    ok, _h, _d = cover([{"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "22:00"}])
    assert ok is True


def test_a_missing_day_fails_and_is_named():
    ok, _h, detail = cover([{"where": "bar", "weekdays": ["Mon"], "from": "17:00", "to": "22:00"}])
    assert ok is False
    assert detail == ["npc_a step 1: npc_a's schedule does not cover bar 18:00-20:00 on Wed"]


def test_back_to_back_rows_cover_together():
    ok, _h, _d = cover([{"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "19:00"},
                        {"where": "bar", "weekdays": ["Mon", "Wed"], "from": "19:00", "to": "21:00"}])
    assert ok is True


def test_a_gap_between_rows_fails():
    ok, _h, _d = cover([{"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "18:30"},
                        {"where": "bar", "weekdays": ["Mon", "Wed"], "from": "19:00", "to": "21:00"}])
    assert ok is False


def test_past_midnight_is_covered_by_two_rows():
    when = {"days": ["Fri"], "from": "22:00", "to": "02:00"}
    ok, _h, _d = cover([{"where": "bar", "weekdays": ["Fri"], "from": "21:00", "to": "23:59"},
                        {"where": "bar", "weekdays": ["Sat"], "from": "00:00", "to": "03:00"}], when=when)
    assert ok is True
    ok, _h, _d = cover([{"where": "bar", "weekdays": ["Fri"], "from": "21:00", "to": "23:59"}], when=when)
    assert ok is False


def test_the_wrong_place_fails():
    ok, _h, _d = cover([{"where": "flat", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "22:00"}])
    assert ok is False


def test_an_opening_step_is_exempt():
    ok, head, _ = cover([], fires_from="opening")
    assert ok is None and "n/a" in head


def test_no_schedule_is_na():
    assert rows(base())["the person is there at the step's hour"][0] is None


# ── the shared helper ─────────────────────────────────────────────────────────

def test_window_uncovered_union_midnight_and_gap():
    assert gates._window_uncovered([0], "18:00", "20:00", [(None, "18:00", "20:00")]) == []
    assert gates._window_uncovered([0, 2], "18:00", "20:00", [([0], "10:00", "23:00")]) == [2]
    assert gates._window_uncovered([4], "23:00", "01:00",
                                   [([4], "22:00", "00:00"), ([5], "00:00", "02:00")]) == []
    assert gates._window_uncovered([4], "23:00", "01:00", [([4], "22:00", "00:00")]) == [4]
    assert gates._window_uncovered([0], "18:00", "20:00",
                                   [([0], "18:00", "19:00"), ([0], "19:01", "20:00")]) == [0]


def test_an_opening_step_needs_no_declared_place():
    s = base()
    step = s["board"]["characters"][0]["ladder"]["steps"][0]
    step.update(fires_from="opening")
    step.pop("where")
    assert rows(s)["a step's place is declared"][0] is True
