"""sheet_check.py: reading days, hours, places and signatures off a sheet."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sheet_check as sc  # noqa: E402

LOCS = [{"id": "bar_floor", "name": "Bar"}, {"id": "members_floor", "name": "Upstairs"},
        {"id": "staff_house", "name": "Staff House"}, {"id": "pool_terrace", "name": "Terrace"}]


def test_days():
    assert sc.days_in("Tue–Sat") == [1, 2, 3, 4, 5]
    assert sc.days_in("Thursday 22:00–23:00") == [3]
    assert sc.days_in("Sat–Mon") == [5, 6, 0]


def test_midpoint_wraps_midnight():
    assert sc.midpoint("09:00–16:30") == 12 * 60 + 45
    assert sc.midpoint("23:00–01:00") == 0


def test_place_names():
    assert sc.place_id("Bar, his table", LOCS) == "bar_floor"
    assert sc.place_id("his room, Upstairs", LOCS) == "members_floor"
    assert sc.place_id("Terrace · Saturday 22:00–23:59", LOCS) == "pool_terrace"
    assert sc.place_id("the moon", LOCS) is None


def test_signed_needs_ready_and_signature(tmp_path):
    ok = tmp_path / "a.md"; ok.write_text("# [READY] Scene\n> Signed by LO 2026-09-29\n")
    draft = tmp_path / "b.md"; draft.write_text("# [REVIEW] Scene\n")
    unsigned = tmp_path / "c.md"; unsigned.write_text("# [READY] Scene\n")
    assert sc.read_sheet(ok)["signed"] and not sc.read_sheet(draft)["signed"] and not sc.read_sheet(unsigned)["signed"]


def test_person_grid_mismatch(tmp_path):
    sheet = tmp_path / "noor.md"
    sheet.write_text("# [READY] Person\n\n| place | Mon | Tue–Fri |\n|---|---|---|\n"
                     "| Staff House | 09:00–16:30 | — |\n| Bar | — | 18:00–22:00 |\n")
    npc = {"id": "noor", "schedules": [{"location": "staff_house", "weekdays": [0], "start_time": "09:00", "end_time": "17:00"},
                                       {"location": "bar_floor", "weekdays": [1, 2, 3], "start_time": "18:00", "end_time": "22:00"}]}
    problems = sc.check_person(sc.read_sheet(sheet), npc, LOCS)
    assert problems == ["person noor: Fri 20:00 the grid says bar_floor, the schedule puts them at None"]
