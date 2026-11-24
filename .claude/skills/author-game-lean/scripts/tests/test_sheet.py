"""sheet.py and check.py's `sheet`: a clean card is green, a planted wrong fact is red. Tiny game in a temp folder."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import reading  # noqa: E402
import sheet  # noqa: E402
import scenes  # noqa: E402
from tiny_game import make_game  # noqa: E402

MERGED = """
[project]
starting_canvas = "start"

[time]
starting_hour = 7
starting_day = "Monday"

[[locations]]
id = "home"
[[locations]]
id = "hall"

[[clothing]]
id = "pyjamas"
slot = "top"
initial = true
[[clothing]]
id = "jeans"
slot = "bottom"

[[npcs]]
id = "npc_mom"
name = "Laura"
role = "Mom"
[[npcs.schedules]]
location = "home"
start_time = "07:00"
end_time = "07:10"

[[canvases]]
id = "start"
[[canvases.nodes]]
id = "a"
blocks = [{ type = "paragraph", content = "Mom is at the stove." }]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Go up"
targetType = "node"
nodeId = "b"
time_progression_minutes = 5
flagEffects = [{ flag = "met_mom", op = "set" }]
wardrobeEffects = [{ action = "equip", item_id = "jeans" }]
[[canvases.nodes]]
id = "b"
blocks = [{ type = "paragraph", content = "You pull your jeans on." }]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Go out"
targetType = "location"
locationId = "hall"
time_progression_minutes = 10
"""

SHEET = """Sheet:
  start.a | 07:00–07:05 | home | npc_mom | pyjamas | none
  start.b | 07:05–07:15 | hall | nobody | jeans, pyjamas | met_mom
"""


@pytest.fixture
def game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED)
    return g


def card(game, sheet_text=SHEET, screens=True):
    body = "PIECE p1\n" + ("What the player sees:\n  Screen 1: Mom.\n" if screens else "") + sheet_text
    (game / "cards" / "p1.md").write_text(body + "Builds: start, home\n")


def red_rows(game):
    return check.check_sheet(game, check.load_merged(game))


def test_computed_sheet_for_the_opening(game):
    rows = sheet.compute(check.load_merged(game), {"start"}, {"start.a": "home", "start.b": "hall"})
    assert sheet.line("start.a", rows["start.a"]) == "start.a | 07:00–07:05 | home (card) | npc_mom | pyjamas | none"
    assert rows["start.b"]["who"] == "nobody" and rows["start.b"]["wearing"] == "jeans, pyjamas"


def test_a_card_that_matches_is_green(game):
    card(game)
    assert red_rows(game) == ("green", [])


@pytest.mark.parametrize("old,new,col", [
    ("start.a | 07:00–07:05", "start.a | 07:00–07:10", "clock"),       # a planted wrong time
    ("start.b | 07:05–07:15 | hall | nobody", "start.b | 07:05–07:15 | hall | npc_mom", "who"),  # not there
    ("home | npc_mom | pyjamas |", "home | npc_mom | jeans, pyjamas |", "wearing"),  # not on yet
    ("jeans, pyjamas | met_mom", "jeans, pyjamas | none", "flags"),
])
def test_a_planted_wrong_fact_is_red(game, old, new, col):
    card(game, SHEET.replace(old, new))
    status, rows = red_rows(game)
    assert status == "red" and any(f"· {col}:" in r for r in rows)


def test_mom_is_judged_at_the_cards_place_and_time(game):
    card(game, SHEET.replace("start.a | 07:00–07:05 | home | npc_mom", "start.a | 07:00–07:05 | hall | npc_mom"))
    status, rows = red_rows(game)
    assert status == "red" and any("start.a · who" in r and "nobody" in r for r in rows)


def test_a_screen_missing_from_the_sheet_or_not_built_is_red(game):
    card(game, SHEET.replace("  start.b | 07:05–07:15 | hall | nobody | jeans, pyjamas | met_mom\n",
                             "  start.c | 07:05–07:15 | hall | nobody | jeans | met_mom\n"))
    status, rows = red_rows(game)
    assert status == "red" and any("start.b is built" in r for r in rows) and any("start.c is on" in r for r in rows)


def test_a_screen_with_no_place_is_incomplete_never_green(game):
    card(game, "Sheet:\n  start.a | 07:00–07:05 | ? | npc_mom | pyjamas | none\n"
               "  start.b | 07:05–07:15 | hall | nobody | jeans, pyjamas | met_mom\n")
    status, rows = red_rows(game)
    assert status == "incomplete" and any("start.a · who" in r for r in rows)


def test_an_old_card_with_no_sheet_is_not_compared(game):
    card(game, "", screens=True)
    assert red_rows(game) == ("green", [])


def test_card_check_asks_a_new_card_with_screens_for_a_sheet(game):
    card(game, "")
    assert any("no Sheet: block" in r for r in check.check_card(game, "p1")[1])
    card(game)
    assert not any("no Sheet: block" in r for r in check.check_card(game, "p1")[1])


def test_an_upstream_equip_change_reopens_the_later_screen(game):
    card(game)
    work = reading.work_list(game, "p1")
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="start.a", verdict="PASS") for i in work["items"]]})
    assert reading.work_list(game, "p1")["items"] == []
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace('wardrobeEffects = [{ action = "equip", item_id = "jeans" }]', ""))
    screens = {i["screen"] for i in reading.work_list(game, "p1")["items"]}
    assert "start.b" in screens  # b's own text didn't change; what she wears there did


def test_order_in_a_set_column_does_not_matter(game):
    card(game, SHEET.replace("jeans, pyjamas | met_mom", "pyjamas, jeans | met_mom"))
    assert red_rows(game) == ("green", [])


# ── a card row written by hand, before any build, compares by meaning (ENI for LO, 2026-11-24) ──

BUILD = "10:00–20:55 +5 · Mon Tue Wed Thu Fri Sat"


@pytest.mark.parametrize("hand", ["Mon–Sat 10:05–21:00", "Mon-Sat 10:05-21:00, any minute", "mon tue wed thu fri sat 10:00–20:55 +5",
                                  "weekdays and Sat 10:05–21:00"])
def test_a_hand_written_clock_that_means_the_same_is_equal(hand):
    assert sheet.norm("clock", hand) == sheet.norm("clock", BUILD)


@pytest.mark.parametrize("hand", ["Mon–Sun 10:05–21:00", "Mon–Sat 10:00–21:00", "weekdays 10:05–21:00", "Mon–Sat 10:05–21:00 +5"])
def test_a_hand_written_clock_that_means_something_else_differs(hand):
    assert sheet.norm("clock", hand) != sheet.norm("clock", BUILD)


def test_weekdays_and_a_range_mean_the_same():
    assert sheet.norm("clock", "weekdays 14:00–15:00") == sheet.norm("clock", "14:00–15:00 +0 · Mon Tue Wed Thu Fri")


def test_the_opening_clock_is_exact_and_hand_times_may_drop_the_zero(game):
    card(game, SHEET.replace("start.a | 07:00–07:05", "start.a | 7:00–7:05"))
    assert red_rows(game) == ("green", [])
    card(game, SHEET.replace("start.a | 07:00–07:05", "start.a | 7:00–7:06"))
    assert red_rows(game)[0] == "red"


# ── a choice's own clock condition narrows the screens after it (P34: rent inside Mark's menu, 2026-11-24) ──

def menu_game(choices):
    """A kitchen menu open all week; each choice leads to `rent` with its own conditions."""
    return {
        "npcs": [{"id": "npc_mark", "name": "Mark", "schedules": [{"location": "kitchen", "start_time": "00:00",
                                                                    "end_time": "23:55"}]}],
        "canvases": [{"id": "menu", "trigger": {"location": "kitchen", "is_repeatable": True},
                      "nodes": [{"id": "hub", "blocks": [], "exit_block": {"type": "choices", "choices": [
                          {"text": f"Pay ({i})", "targetType": "node", "nodeId": "rent",
                           "time_progression_minutes": 5, "conditions": cond} for i, cond in enumerate(choices)]}},
                                {"id": "rent", "blocks": [{"type": "dialog", "content": "Seventy-five.",
                                                           "props": {"speaker": "npc", "npcId": "npc_mark"}}]}]}],
    }


SUNDAY_MORNING = {"version": "1.0", "items": [{"type": "weekday", "weekdays": [6]},
                                              {"type": "time_of_day", "start_time": "08:00", "end_time": "12:00"}]}
SATURDAY = {"version": "1.0", "items": [{"type": "weekday", "weekdays": [5]},
                                        {"type": "time_of_day", "start_time": "08:00", "end_time": "12:00"}]}


def test_a_sunday_only_choice_gives_its_screen_a_sunday_row():
    rows = sheet.compute(menu_game([SUNDAY_MORNING]), {"menu"})
    assert rows["menu.hub"]["clock"] == "any +0"
    assert rows["menu.rent"]["clock"] == "08:05–12:05 · Sun"
    assert sheet.norm("clock", "Sun 08:05–12:05") == sheet.norm("clock", rows["menu.rent"]["clock"])


def test_two_choices_into_one_screen_give_the_union():
    clock = sheet.compute(menu_game([SUNDAY_MORNING, SATURDAY]), {"menu"})["menu.rent"]["clock"]
    want = sheet.norm("clock", "Sat Sun 08:05–12:05")
    assert sheet.norm("clock", clock) == want
    assert sheet.norm("clock", "Sun 08:05–12:05") != want


def test_presence_narrows_by_the_choice_too():
    g = menu_game([SUNDAY_MORNING])
    g["npcs"][0]["schedules"] = [{"location": "kitchen", "weekdays": [6], "start_time": "07:00", "end_time": "13:00"}]
    assert scenes.check_presence(g) == ("green", [])  # Mark is only there Sunday mornings: the rent line is true
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["conditions"] = {}
    assert scenes.check_presence(g)[0] == "red"  # with no choice condition the line could show any day
