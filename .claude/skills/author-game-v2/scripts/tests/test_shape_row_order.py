"""`shape.py` reads schedule rows the way the engine does (skill pass 2026-10-08, B50, B51).

B50: the engine takes the FIRST matching row (v2.py:4289-4318). A row above the step's row can
take the person elsewhere though the union of rows covers the window. B51: an overnight row on
some weekdays loses its person after midnight, when the day reads as the next weekday.
Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import test_shape_ck5 as ck5  # noqa: E402

ROW = "the person is there at the step's hour"


def with_rows(rows):
    s = ck5.base()
    s["board"]["characters"][0]["schedule"] = rows
    return ck5.rows(s)[ROW]


def test_the_steps_row_first_passes_and_an_earlier_row_elsewhere_is_red():
    bar = {"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "21:00"}
    flat = {"where": "flat", "weekdays": ["Mon"], "from": "18:00", "to": "19:00"}
    assert with_rows([bar, flat])[0] is True
    ok, _h, detail = with_rows([flat, bar])
    assert ok is False and "an earlier row wins at Mon 18:00" in detail[0]


def test_an_overnight_row_on_some_days_needs_its_next_day_half():
    bar = {"where": "bar", "weekdays": ["Mon", "Wed"], "from": "17:00", "to": "21:00"}
    night = {"where": "flat", "weekdays": ["Fri"], "from": "22:00", "to": "06:00"}
    ok, _h, detail = with_rows([bar, night])
    assert ok is False and any("after midnight on Sat" in d for d in detail)
    morning = {"where": "flat", "weekdays": ["Sat"], "from": "00:00", "to": "06:00"}
    assert with_rows([bar, night, morning])[0] is True
