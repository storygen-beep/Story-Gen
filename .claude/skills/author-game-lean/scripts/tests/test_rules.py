"""rules.py, check.py --rules / --card / `does`, and reading.py's per-screen rows. Tiny game in a temp folder."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import reading  # noqa: E402
import rules  # noqa: E402
from test_sheet import MERGED, SHEET  # noqa: E402
from tiny_game import make_game  # noqa: E402

DOES = """Does:
  start.a | the opening, the first screen, a one-time step, a person is on screen, the clock moves, a first meeting, she dresses or undresses
  start.b | the opening, the hand-over, a one-time step, the clock moves, a garment is named, a place is entered, a scene's last screen
"""


@pytest.fixture
def game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(
        MERGED.replace('text = "Go up"', 'text = "Go up (5 min)"').replace('text = "Go out"', 'text = "Go out (10 min)"')
        .replace('[[clothing]]\nid = "jeans"', '[[clothing]]\nid = "jeans"\nname = "Jeans"'))
    return g


def card(game, does=DOES, sheet=SHEET):
    (game / "cards" / "p1.md").write_text("PIECE p1\nWhat the player sees:\n  Screen 1: Mom.\n" + sheet + does
                                          + "Builds: start, home\n")


def test_the_rule_list_is_always_rows_plus_the_screens_triggers():
    rows = rules.table()
    lst = rules.rule_list({"x.a": ["a media spot"]}, rows=rows)
    assert "C460" in lst and "C1261" in lst  # always, and a media spot
    assert "C1003" not in lst  # the plan
    assert all(r in lst for r, v in rows.items() if "always" in v["when"])


def test_pointer_rows_are_not_in_the_table():
    assert rules.table()["C448"]["home"] == "craft/people.md"  # voice.md's C448 is a pointer


def test_plan_rows_are_their_own_list():
    plan = rules.plan_rows()
    assert "C1003" in plan and "C460" not in plan


@pytest.mark.parametrize("line,why", [("start.a | sometimes", "not in SKILL.md"), ("start.a | always", "not written per screen"),
                                      ("start.a | the plan", "not written per screen"), ("start.a |", "names no trigger")])
def test_planted_bad_does_line_is_red_on_the_card(game, line, why):
    card(game, f"Does:\n  {line}\n  start.b | the opening\n")
    assert any(why in r for r in check.check_card(game, "p1")[1])


def test_does_and_sheet_must_name_the_same_screens(game):
    card(game, "Does:\n  start.a | the opening\n")
    assert any("different screens" in r for r in check.check_card(game, "p1")[1])


def test_a_card_with_does_needs_no_areas_or_craft_line(game):
    card(game)
    assert check.check_card(game, "p1") == ("green", [])


def test_a_new_card_with_screens_and_no_does_is_red(game):
    card(game, "")
    assert any("no Does: block" in r for r in check.check_card(game, "p1")[1])


def test_an_old_card_without_screens_or_does_is_not_asked(game):
    (game / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start, home\n")
    assert not any("Does:" in r for r in check.check_card(game, "p1")[1])
    assert check.check_does(game, check.load_merged(game)) == ("green", [])


def test_the_guard_is_green_when_does_names_what_the_build_does(game):
    card(game)
    assert check.check_does(game, check.load_merged(game)) == ("green", [])


@pytest.mark.parametrize("drop", ["the first screen", "the hand-over", "a person is on screen", "the clock moves", "she dresses or undresses",
                                  "a garment is named", "a place is entered", "a scene's last screen", "a one-time step"])
def test_planted_missing_trigger_is_red_by_the_guard(game, drop):
    card(game, DOES.replace(f", {drop}", "").replace(f"| {drop}, ", "| "))
    status, rows = check.check_does(game, check.load_merged(game))
    assert status == "red" and any(f"`{drop}`" in r for r in rows)


def test_a_first_meeting_may_sit_on_either_screen(game):
    card(game, DOES.replace(", a first meeting", "").replace("a garment is named,", "a garment is named, a first meeting,"))
    # start.a sets met_mom leaving it; naming the meeting on start.b, the screen it leads to, is enough
    assert check.check_does(game, check.load_merged(game)) == ("green", [])
    card(game, DOES.replace(", a first meeting", ""))
    status, rows = check.check_does(game, check.load_merged(game))
    assert status == "red" and any("met_mom" in r for r in rows)


def test_rules_cli_prints_the_list(game, capsys):
    card(game)
    assert check.main(["--rules", str(game), "p1"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("p1: ") and "reader (" in out and "C460" in out


def test_a_changed_screen_asks_only_the_rows_its_triggers_fire(game):
    card(game)
    work = reading.work_list(game, "p1")
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="start.a", verdict="PASS") for i in work["items"]]})
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("You pull your jeans on.", "You pull your jeans on, fast."))
    asked = {i["row"] for i in reading.work_list(game, "p1")["items"]}
    on_b = set(rules.rule_list(rules.card_does(DOES + "\n")).keys())
    b_only = {r for r, on in rules.rule_list(rules.card_does(DOES)).items() if on == ["start.b"]}
    a_only = {r for r, on in rules.rule_list(rules.card_does(DOES)).items() if on == ["start.a"]}
    assert asked and b_only <= asked and not (a_only & asked) and asked <= on_b | set(reading.scene_tests())


# ── "*" verdicts after one screen changes (P13 live trial, 2026-11-24: one changed line re-asked 229 of 260) ──

def scene_wide_pass(game):
    card(game)
    work = reading.work_list(game, "p1")
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="*", verdict="PASS") for i in work["items"]]})
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("You pull your jeans on.", "You pull your jeans on, fast."))
    return reading.work_list(game, "p1")


def test_a_star_pass_is_asked_again_only_on_the_changed_screen(game):
    work = scene_wide_pass(game)
    lst = rules.rule_list(rules.card_does(DOES))
    on_b = {r for r, on in lst.items() if "start.b" in on} | set(reading.scene_tests())
    rows_b = {i["row"] for i in work["items"] if i["screen"] == "start.b"}
    assert rows_b == on_b - set(reading.SCENE_WIDE)
    assert not any(i["screen"] == "start.a" for i in work["items"])
    a_only = {r for r, on in lst.items() if on == ["start.a"]}
    assert a_only and a_only <= {v["row"] for v in work["carried"]}  # carried, not asked


def test_only_the_scene_wide_tests_go_back_on_star(game):
    work = scene_wide_pass(game)
    assert {i["row"] for i in work["items"] if i["screen"] == "*"} == set(reading.SCENE_WIDE)


def test_a_star_pass_survives_a_new_verdict_on_one_screen(game):
    work = scene_wide_pass(game)
    rec = reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen=i["screen"], verdict="PASS")
                                                   for i in work["items"]]})
    stars = {v["row"] for v in rec["verdicts"] if v["screen"] == "*"}
    assert "C460" in stars and reading.work_list(game, "p1")["items"] == []


def test_a_star_fail_is_refused(game):
    card(game)
    item = reading.work_list(game, "p1")["items"][0]
    with pytest.raises(ValueError, match="never"):
        reading.record(game, "p1", {"verdicts": [dict(item, verdict="FAIL", cause="c1")],
                                    "causes": [{"id": "c1", "what": "x"}]})
