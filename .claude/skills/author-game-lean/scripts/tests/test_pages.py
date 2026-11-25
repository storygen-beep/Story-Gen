"""pages.py: the Hints page as screens, and the `pages` check (first meetings, hidden places, hint flags, the People
dialog keys). Planted games; nothing in games/ is read. LO, typed in main-lean 2026-11-25: "Go ahead"."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import pages  # noqa: E402
import reading  # noqa: E402
import rules  # noqa: E402
from test_sheet import MERGED, SHEET  # noqa: E402
from tiny_game import make_game  # noqa: E402


def choice(*flags):
    return {"text": "Go", "flagEffects": [{"flag": f, "op": "set"} for f in flags]}


def planted(hints=(), walk=(), meets=("met_tom",), opening=(), places=(), npcs=(), people_page=None):
    canvases = [{"id": "start", "nodes": [{"id": "a", "exit_block": {"choices": [choice(*opening)]}}]},
                {"id": "cafe_meet", "nodes": [{"id": "a", "exit_block": {"choices": [choice(*meets)]}}]}]
    ui = {"quests_layout": "hints"}
    if people_page:
        ui["people_page"] = people_page
    return {"project": {"starting_canvas": "start"}, "ui": ui, "canvases": canvases, "story_hints": list(hints),
            "walkthroughs": list(walk), "locations": list(places), "npcs": list(npcs)}


def hint(title, *flags):
    steps = [{"when": [], "text": "Ask at the café, Monday to Saturday from 10am."}]
    steps += [{"when": [{"flag": f, "op": "is_true"}], "text": "end"} for f in flags]
    return {"title": title, "category": "Employment 💼", "description": "Hiring.", "hints": steps}


def test_an_unpointed_first_meeting_is_red():
    assert any("met_tom" in r for r in pages.problems(planted()))


def test_a_meeting_on_a_hint_ladder_is_green():
    assert pages.problems(planted(hints=[hint("The Café Job", "met_tom")])) == []


def test_a_walkthrough_step_points_too():
    walk = [{"id": "wt", "title": "Job", "steps": [{"when": [{"flag": "met_tom", "op": "is_true"}],
                                                    "done_text": "Met.", "todo_text": "Meet Tom."}]}]
    assert pages.problems(planted(walk=walk)) == []


def test_the_opening_meets_people_without_a_hint():
    assert pages.problems(planted(meets=(), opening=("met_mom",))) == []


def test_a_place_hidden_behind_an_unpointed_flag_is_red():
    places = [{"id": "offices", "hidden_until": {"flag": "offices_known"}}]
    rows = pages.problems(planted(meets=("offices_known",), places=places))
    assert any("offices" in r and "hidden" in r for r in rows)


def test_a_hidden_place_set_beside_a_pointed_meeting_is_green():
    places = [{"id": "zoes", "hidden_until": {"flag": "zoe_place_known"}}]
    game = planted(meets=("met_zoe", "zoe_place_known"), places=places, hints=[hint("Zoe", "met_zoe")])
    assert pages.problems(game) == []


def test_a_hint_flag_no_canvas_sets_is_red():
    rows = pages.problems(planted(hints=[hint("Job", "met_tom", "never_set")]))
    assert any("never_set" in r and "no canvas sets" in r for r in rows)


def test_the_cot_people_page_needs_both_keys():
    npcs = [{"id": "npc_tom", "stranger_name": "guy behind the counter"}]
    rows = pages.problems(planted(hints=[hint("Job", "met_tom")], npcs=npcs, people_page="cot"))
    assert any("npc_tom" in r and "people_tab" in r for r in rows)


def test_no_hints_layout_no_pointer_check():
    game = planted()
    game["ui"] = {}
    assert pages.problems(game) == []


def test_each_entry_is_a_goal_card_screen():
    game = planted(hints=[hint("The Café Job", "met_tom")])
    seen = rules.seen(game)
    assert seen["story_hints.the_cafe_job"] >= {"a goal card is shown", "the clock moves"}


# ── on a card ───────────────────────────────────────────────────────────────────────────────────────────────────

HINTS = '''
[ui]
quests_layout = "hints"

[[story_hints]]
title = "The Café Job"
category = "Employment"
description = "Hiring."
hints = [ { when = [], text = "Ask at the café." } ]
'''


@pytest.fixture
def game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED + HINTS)
    return g


def card(game, does):
    (game / "cards" / "p1.md").write_text("PIECE p1\nWhat the player sees:\n  Screen 1: Mom.\n" + SHEET + does
                                          + "Builds: start, home, story_hints\n")


def test_a_card_building_the_hints_page_names_its_screens(game):
    card(game, "Does:\n  start.a | the opening\n  start.b | the opening\n")
    red = check.check_does(game, check.load_merged(game))[1]
    assert any("story_hints.the_cafe_job is built by this card" in r for r in red)


def test_a_page_screen_needs_no_sheet_row_and_gets_no_scene_tests(game):
    card(game, "Does:\n  start.a | the opening\n  start.b | the opening\n  story_hints.the_cafe_job | a goal card is shown\n")
    assert not any("different screens" in r for r in check.check_card(game, "p1")[1])
    where = reading.row_screens(game, "p1")
    assert "story_hints.the_cafe_job" not in where["B3"]
    assert any("story_hints.the_cafe_job" in on for on in where.values())  # the goal-card rules reach it
    assert "story_hints.the_cafe_job" in reading.screens(check.load_merged(game), {"story_hints"})


# ── the People dialog's fields as screens, and the re-ask (fix 7) ────────────────────────────────────────────────

PEOPLE = '''
[ui]
people_page = "cot"

[[npcs]]
id = "npc_tom"
name = "Tom"
stranger_name = "guy behind the counter"
people_tab = "coworkers"
'''


@pytest.fixture
def people_game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED + PEOPLE)
    (g / "cards" / "p1.md").write_text("PIECE p1\nWhat the player sees:\n  Screen 1: Mom.\n" + SHEET
                                       + "Does:\n  start.a | the opening\n  start.b | the opening\n"
                                       + "Builds: start, home, ui:people_page\n")
    return g


def test_a_persons_dialog_fields_are_screens(people_game):
    sc = reading.screens(check.load_merged(people_game), {"ui:people_page"})
    assert {"npcs.npc_tom.stranger_name", "npcs.npc_tom.people_tab"} <= set(sc)


def test_a_passed_stranger_name_is_asked_again_when_it_changes(people_game):
    first = reading.work_list(people_game, "p1")["items"]
    rows = sorted({i["row"] for i in first})
    verdicts = [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows]
    verdicts.append({"row": rows[0], "screen": "npcs.npc_tom.stranger_name", "verdict": "PASS"})  # as P46 was read
    reading.record(people_game, "p1", {"verdicts": verdicts, "causes": []})
    assert not [i for i in reading.work_list(people_game, "p1")["items"] if i["screen"].startswith("npcs.")]
    merged = people_game / "toml_phases" / "7_final_game.toml"
    merged.write_text(merged.read_text().replace("guy behind the counter", "man at the till"))
    again = reading.work_list(people_game, "p1")["items"]
    assert any(i["screen"] == "npcs.npc_tom.stranger_name" for i in again)


def test_a_card_need_not_list_people_fields_on_does(people_game):
    red = check.check_does(people_game, check.load_merged(people_game))[1]
    assert not any("npcs." in r for r in red)


def test_a_stranger_name_judged_only_on_star_is_asked_again(people_game):
    rows = sorted({i["row"] for i in reading.work_list(people_game, "p1")["items"]})
    reading.record(people_game, "p1", {"verdicts": [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows],
                                       "causes": []})
    merged = people_game / "toml_phases" / "7_final_game.toml"
    merged.write_text(merged.read_text().replace("guy behind the counter", "man at the till"))
    again = [i for i in reading.work_list(people_game, "p1")["items"] if i["screen"] == "npcs.npc_tom.stranger_name"]
    assert again and all(i["row"] in reading.rules.table() for i in again)
