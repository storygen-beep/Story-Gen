"""who_is_where.py: the first matching row wins, a gated row lets the walk go on, windows wrap past midnight,
and the lean copy agrees with v2's on a real game (read-only)."""
import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parents[3]
sys.path.insert(0, str(SCRIPTS))
import who_is_where as w  # noqa: E402


def person(*rows):
    return {"npcs": [{"id": "npc_x", "schedules": list(rows)}]}


def at(game, day, hhmm):
    return w.where(game)["npc_x"][(day, w.minutes(hhmm))]


def test_first_matching_row_wins():
    g = person({"start_time": "08:00", "end_time": "12:00", "location": "office"},
               {"start_time": "00:00", "end_time": "23:59", "location": "home"})
    assert at(g, 0, "09:00") == {("office", "")}
    assert at(g, 0, "13:00") == {("home", "")}


def test_planted_first_match_bug_a_later_row_must_not_win():
    g = person({"start_time": "08:00", "end_time": "12:00", "location": "office"},
               {"start_time": "08:00", "end_time": "12:00", "location": "cafe"})
    assert ("cafe", "") not in at(g, 0, "10:00")


def test_a_gated_row_adds_its_place_and_lets_the_walk_go_on():
    g = person({"start_time": "18:00", "end_time": "20:00", "location": "bar",
                "when": {"items": [{"type": "flag", "flag_key": "bar_open", "operator": "is_true"}]}},
               {"start_time": "00:00", "end_time": "23:59", "location": "home"})
    assert at(g, 0, "19:00") == {("bar", ""), ("home", "")}


def test_a_met_only_when_is_an_ordinary_row():
    g = person({"start_time": "18:00", "end_time": "20:00", "location": "bar",
                "when": {"items": [{"flag_key": "x_met", "operator": "is_true"}]}},
               {"start_time": "00:00", "end_time": "23:59", "location": "home"})
    assert at(g, 0, "19:00") == {("bar", "")}


def test_a_window_wraps_past_midnight_and_no_end_is_an_hour():
    g = person({"start_time": "22:00", "end_time": "04:00", "location": "club"},
               {"start_time": "10:00", "location": "shop"})
    assert at(g, 1, "02:00") == {("club", "")}
    assert at(g, 1, "10:55") == {("shop", "")} and at(g, 1, "11:00") == {(None, "")}


def test_weekdays_and_sleep_mark():
    g = person({"weekdays": [5, 6], "start_time": "00:00", "end_time": "09:00", "location": "bed",
                "activity": "asleep"})
    assert at(g, 5, "03:00") == {("bed", "asleep")} and at(g, 0, "03:00") == {(None, "")}
    assert w.cell(w.where(g)["npc_x"], 5, 3) == "bedz"


def test_agrees_with_v2_on_first_term():
    """Same table as the frozen v2 copy, on a real game, read-only."""
    game_toml = REPO / "games" / "first_term" / "toml_phases" / "7_final_game.toml"
    v2 = REPO / ".claude" / "skills" / "author-game-v2" / "scripts"
    sys.path.insert(0, str(v2))
    spec = importlib.util.spec_from_file_location("v2_gates", v2 / "gates.py")
    gates = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gates)
    game = gates._load(str(game_toml))
    ours, theirs = w.where(game), gates._tr_where(game)
    assert ours.keys() == theirs.keys() and ours == theirs
