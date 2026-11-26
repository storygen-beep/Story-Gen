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


def test_a_place_cut_for_the_release_is_green():
    """LO 2026-11-27: the House Next Door hidden in release 1. Its flag is declared and nothing sets it."""
    places = [{"id": "next_door", "hidden_until": {"flag": "next_door_open"}}]
    game = planted(meets=(), places=places)
    game["player"] = {"flag_keys": ["next_door_open"]}
    assert pages.problems(game) == []


def test_an_undeclared_flag_nothing_sets_is_still_red():
    places = [{"id": "next_door", "hidden_until": {"flag": "next_door_opn"}}]
    rows = pages.problems(planted(meets=(), places=places))
    assert any("next_door" in r and "hidden" in r for r in rows)


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


# ── a person's start feelings, and the sidebar, as screens (P48, 2026-11-25; LO: "Go ahead"). Trait words are no
# screen: they are hidden, and the reader judges the fit on the scenes (LO, 2026-11-26: "Hide them dont show them") ──

SYSTEM = '''
[engine.people]
system = "cot"

[[npcs]]
id = "npc_tom"
name = "Tom"
gender = "male"
attracted = true
people_type = "worker"
traits = ["Pushy", "Kind"]
core_traits = { friendship = 300 }

[[sidebar_items]]
type = "trait_words"
trait = "exhibitionism"
label = "Exhibitionism"
bands = [{ min = 0, max = 99, text = "Level 0" }, { min = 100, max = 199, text = "Level 1" }]
'''


@pytest.fixture
def system_game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED + SYSTEM)
    (g / "cards" / "p1.md").write_text("PIECE p1\nWhat the player sees:\n  Screen 1: Mom.\n" + SHEET
                                       + "Does:\n  start.a | the opening\n  start.b | the opening\n"
                                       + "  sidebar.exhibitionism | a meter is shown or paid\n"
                                       + "Builds: start, home, engine:people, sidebar:exhibitionism\n")
    return g


def test_start_feelings_are_screens_and_trait_words_are_not(system_game):
    game = check.load_merged(system_game)
    entries = pages.people_entries(game)
    assert entries["npcs.npc_tom.feelings"].startswith("friendship 300, lust 0, control 0")
    assert not any(s.endswith(".traits") for s in entries)  # hidden: no player-facing screen (C2193)
    sc = reading.screens(game, {"engine:people"})
    assert "npcs.npc_tom.feelings" in sc and "npcs.npc_tom.traits" not in sc
    assert "npcs.npc_tom.feelings" in reading.screens(game, {"npcs:npc_tom"})
    assert "npcs.npc_tom.feelings" not in reading.screens(game, {"start"})


def test_no_switch_no_system_screens(system_game):
    game = check.load_merged(system_game)
    game["engine"] = {}
    assert not any(s.endswith((".traits", ".feelings")) for s in pages.people_entries(game))


def test_a_sidebar_item_is_a_screen_its_builds_line_covers(system_game):
    game = check.load_merged(system_game)
    assert "sidebar.exhibitionism" in reading.screens(game, {"sidebar:exhibitionism"})
    assert rules.seen(game)["sidebar.exhibitionism"] == {"a meter is shown or paid"}
    assert pages.is_page("sidebar.exhibitionism")


def test_a_card_of_only_page_screens_is_judged_and_needs_no_sheet(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED + SYSTEM)
    (g / "cards" / "p1.md").write_text("PIECE p1\nDoes:\n  sidebar.exhibitionism | a meter is shown or paid\n"
                                       "  npcs.npc_tom.feelings | a person is on screen\n"
                                       "Builds: engine:people, sidebar:exhibitionism\n")
    game = check.load_merged(g)
    assert not check.not_built_yet(rules.card_does((g / "cards" / "p1.md").read_text()), game)
    assert check.check_card(g, "p1")[0] == check.GREEN
    assert check.check_does(g, game) == (check.GREEN, [])


def test_a_card_need_not_name_its_sidebar_items_on_does(system_game):
    # P09 and P36 built Grades and Reputation before a sidebar item was a screen; the reader still reaches them.
    card = system_game / "cards" / "p1.md"
    card.write_text(card.read_text().replace("  sidebar.exhibitionism | a meter is shown or paid\n", ""))
    assert not any("sidebar." in r for r in check.check_does(system_game, check.load_merged(system_game))[1])
    rows = sorted({i["row"] for i in reading.work_list(system_game, "p1")["items"]})
    reading.record(system_game, "p1", {"verdicts": [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows],
                                       "causes": []})
    merged = system_game / "toml_phases" / "7_final_game.toml"
    merged.write_text(merged.read_text().replace('text = "Level 1"', 'text = "Bold"'))
    assert any(i["screen"] == "sidebar.exhibitionism" for i in reading.work_list(system_game, "p1")["items"])


@pytest.mark.parametrize("old,new,screen", [
    ("friendship = 300", "friendship = 100", "npcs.npc_tom.feelings"),
    ('text = "Level 1"', 'text = "Bold"', "sidebar.exhibitionism"),
])
def test_a_changed_start_value_or_band_reopens_its_rows(system_game, old, new, screen):
    rows = sorted({i["row"] for i in reading.work_list(system_game, "p1")["items"]})
    verdicts = [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows]
    reading.record(system_game, "p1", {"verdicts": verdicts, "causes": []})
    assert not [i for i in reading.work_list(system_game, "p1")["items"] if i["screen"] == screen]
    merged = system_game / "toml_phases" / "7_final_game.toml"
    merged.write_text(merged.read_text().replace(old, new))
    again = [i for i in reading.work_list(system_game, "p1")["items"] if i["screen"] == screen]
    assert again


ANN = '''
[[npcs]]
id = "npc_ann"
name = "Ann"
gender = "female"
attracted = false
people_type = "worker"
traits = ["Shy", "Kind"]
'''


def test_new_people_fields_after_a_reading_are_each_asked_without_does(system_game):
    # P48, 2026-11-25: the "most of a canvas is new" shortcut took all new npcs.* screens as one canvas `npcs`, and
    # with only sidebar lines on Does: it asked 0 people items.
    merged = system_game / "toml_phases" / "7_final_game.toml"
    full = merged.read_text()
    merged.write_text(full.replace('[engine.people]\nsystem = "cot"\n', ""))  # read once before the switch
    rows = sorted({i["row"] for i in reading.work_list(system_game, "p1")["items"]})
    reading.record(system_game, "p1", {"verdicts": [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows],
                                       "causes": []})
    merged.write_text(full + ANN)
    assert "npcs." not in (system_game / "cards" / "p1.md").read_text()
    items = reading.work_list(system_game, "p1")["items"]
    asked = {i["screen"] for i in items if i["screen"].startswith("npcs.")}
    every = {k for k in pages.people_entries(check.load_merged(system_game)) if k.endswith(".feelings")}
    assert {f"npcs.{n}.feelings" for n in ("npc_tom", "npc_ann")} <= every
    assert asked == every
    assert all(i["why"] == "screen is new" for i in items if i["screen"].startswith("npcs."))
    assert not any(i["why"].startswith("most of npcs") for i in items)


# ── one screen, one owning card; a page field asks only the rows that fire on it (2026-11-25) ─────────────────────

def test_the_people_page_card_does_not_own_traits_or_feelings(system_game):
    game = check.load_merged(system_game)
    game["ui"] = {"people_page": "cot"}
    game["npcs"][-1]["stranger_name"] = "guy behind the counter"
    sc = pages.screens_for(game, {"ui:people_page"})
    assert "npcs.npc_tom.stranger_name" in sc
    assert not any(s.endswith((".traits", ".feelings")) for s in sc)  # P48's, not P46's: 912 duplicate items
    assert "npcs.npc_tom.feelings" in pages.screens_for(game, {"engine:people"})


def test_a_card_without_does_asks_a_sidebar_item_only_the_rows_that_fire_on_it(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED + SYSTEM)
    card = g / "cards" / "p1.md"
    card.write_text("PIECE p1\nCraft: craft/meters.md · cites C285\nBuilds: start, home\n")
    rows = sorted({i["row"] for i in reading.work_list(g, "p1")["items"]})
    reading.record(g, "p1", {"verdicts": [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows], "causes": []})
    card.write_text(card.read_text().replace("Builds: start, home", "Builds: start, home, sidebar:exhibitionism"))
    items = reading.work_list(g, "p1")["items"]
    table = rules.table()
    on_item = {i["row"] for i in items if i["screen"] == "sidebar.exhibitionism"}
    assert on_item and len(on_item) < len(rows)  # P01: 459 items, every row on each of three items
    assert all({"always", "a meter is shown or paid"} & set(table[r]["when"]) for r in on_item)
    assert not any(i["why"] == "a screen of the scene changed" for i in items)  # P01: 127 "*" rows


def test_two_cards_owning_one_page_screen_is_red(system_game):
    (system_game / "cards" / "p2.md").write_text("PIECE p2\nDoes:\n  sidebar.exhibitionism | a meter is shown or paid\n"
                                                 "Builds: sidebar:exhibitionism\n")
    red = check.check_does(system_game, check.load_merged(system_game))[1]
    assert any("sidebar.exhibitionism" in r and "p1" in r and "p2" in r for r in red)


# ── the trait fit is judged on the scenes (C2194; LO, typed in main-lean 2026-11-26: "Hide them dont show them") ──

def test_a_changed_trait_word_asks_only_the_fit_row_on_that_persons_scenes(tmp_path):
    g = make_game(tmp_path)
    merged = g / "toml_phases" / "7_final_game.toml"
    merged.write_text(MERGED.replace('id = "npc_mom"\n', 'id = "npc_mom"\ntraits = ["Kind", "Cook"]\n'))
    (g / "cards" / "p1.md").write_text("PIECE p1\nCraft: craft/people.md · cites C660\nBuilds: start, home\n")
    rows = sorted({i["row"] for i in reading.work_list(g, "p1")["items"]})
    assert reading.TRAIT_FIT in rows
    reading.record(g, "p1", {"verdicts": [{"row": r, "screen": "*", "verdict": "PASS"} for r in rows], "causes": []})
    assert reading.work_list(g, "p1")["items"] == []
    merged.write_text(merged.read_text().replace('["Kind", "Cook"]', '["Cruel", "Cook"]'))
    items = reading.work_list(g, "p1")["items"]
    assert items and {i["row"] for i in items} == {reading.TRAIT_FIT}
    assert {i["screen"] for i in items} == {"start.a"}  # mom is on start.a only
    assert all(i["why"] == "a trait word of someone on it changed" for i in items)


# ── C2201: a description never changes with what she wears (LO, typed in main-lean 2026-11-27) ──

def _place(*variants):
    return {"id": "street", "description_variants": [{"conditions": {"version": "1.0", "logic": "AND",
                                                                      "items": list(v)}, "text": "x"} for v in variants]}


def test_a_description_that_reads_her_clothes_is_red():
    game = {"locations": [_place([{"type": "clothing_item", "item_id": "leggings", "operator": "equipped"}])]}
    rows = pages.problems(game)
    assert any("street" in r and "changes with what she wears" in r for r in rows)


def test_a_nested_clothing_condition_is_red_too():
    nested = {"type": "group", "logic": "OR", "items": [{"type": "worn_exposure", "operator": "gte", "value": 1}]}
    assert any("worn_exposure" in r for r in pages.problems({"locations": [_place([nested])]}))


def test_nobody_here_and_a_weekday_are_green():
    game = {"locations": [_place([{"type": "npc_at_location", "npc_id": "npc_mom", "location_id": "street",
                                   "operator": "is_absent"}], [{"type": "weekday", "weekdays": [6]}])]}
    assert pages.problems(game) == []
