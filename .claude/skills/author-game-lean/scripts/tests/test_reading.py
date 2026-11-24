"""reading.py: the reader's memory. Built on the tiny game in a temp folder; nothing in games/ is read or written."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import reading  # noqa: E402
from tiny_game import make_game  # noqa: E402

MERGED = """
[[npcs]]
id = "npc_mom"
name = "Laura"
role = "Mom"
[[npcs.schedules]]
location = "home"
start_time = "07:00"
end_time = "09:00"

[[npcs]]
id = "npc_dad"
name = "Frank"
[[npcs.schedules]]
location = "home"
start_time = "18:00"

[[canvases]]
id = "start"
[canvases.trigger]
location = "home"
[[canvases.nodes]]
id = "a"
blocks = [{ type = "paragraph", content = "Mom is at the stove." }]
[[canvases.nodes]]
id = "b"
blocks = [{ type = "paragraph", content = "You eat alone." }]
"""


@pytest.fixture
def game(tmp_path):
    g = make_game(tmp_path)
    (g / "toml_phases" / "7_final_game.toml").write_text(MERGED)
    (g / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start\nCraft: craft/voice.md · cites C442\n")
    return g


def first_pass(game, verdict="PASS"):
    work = reading.work_list(game, "p1")
    out = {"verdicts": [{"row": i["row"], "screen": "start.a", "verdict": verdict, "line": "Mom is at the stove.",
                         "cause": "c1" if verdict == "FAIL" else None} for i in work["items"]],
           "causes": [{"id": "c1", "what": "Mom's line"}] if verdict == "FAIL" else []}
    return reading.record(game, "p1", out)


def edit(game, old, new):
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace(old, new))


def test_first_pass_asks_every_row_once(game):
    work = reading.work_list(game, "p1")
    rows = {i["row"] for i in work["items"]}
    assert {"B1", "B13", "C442", "voice#1"} <= rows and all(i["screen"] == "*" for i in work["items"])


def test_unchanged_screens_give_no_rows(game):
    first_pass(game)
    work = reading.work_list(game, "p1")
    assert work["items"] == [] and work["carried"] and all(v["carried"] for v in work["carried"])


def test_one_changed_screen_gives_only_its_rows(game):
    first_pass(game)
    edit(game, "You eat alone.", "You eat alone, fast.")
    work = reading.work_list(game, "p1")
    assert work["items"] and {i["screen"] for i in work["items"]} == {"start.b"}


def test_a_carried_pass_never_flips_without_a_text_change(game):
    first_pass(game)
    for _ in range(3):
        assert reading.work_list(game, "p1")["items"] == []
        rec = reading.record(game, "p1", {"verdicts": [], "causes": []})
        assert all(v["verdict"] == "PASS" for v in rec["verdicts"])


def test_a_fail_comes_back_until_it_passes(game):
    first_pass(game, verdict="FAIL")
    work = reading.work_list(game, "p1")
    assert work["items"] and all(i["why"] == "failed last pass" for i in work["items"])


def test_a_moved_schedule_row_reopens_the_screens_naming_that_person(game):
    first_pass(game)
    edit(game, 'end_time = "09:00"', 'end_time = "08:00"')
    work = reading.work_list(game, "p1")
    assert {i["screen"] for i in work["items"]} == {"start.a"}  # b doesn't name Mom


def test_another_persons_row_reopens_nothing(game):
    first_pass(game)
    edit(game, 'start_time = "18:00"', 'start_time = "19:00"')
    assert reading.work_list(game, "p1")["items"] == []


def test_all_asks_everything_again(game):
    first_pass(game)
    assert reading.work_list(game, "p1", everything=True)["items"]


def test_a_fail_without_a_cause_or_off_the_list_is_refused(game):
    work = reading.work_list(game, "p1")
    item = work["items"][0]
    with pytest.raises(ValueError, match="cause"):
        reading.record(game, "p1", {"verdicts": [dict(item, verdict="FAIL")], "causes": []})
    first_pass(game)
    with pytest.raises(ValueError, match="work list"):
        reading.record(game, "p1", {"verdicts": [{"row": "B1", "screen": "start.a", "verdict": "PASS"}]})


def test_fails_are_grouped_by_cause(game):
    rec = first_pass(game, verdict="FAIL")
    lines = reading.by_cause(rec)
    assert lines[0].startswith("c1 · Mom's line") and len(lines) == 1 + len(rec["verdicts"])


def test_record_is_written_under_reader(game):
    first_pass(game)
    rec = json.loads((game / "reader" / "p1.json").read_text())
    assert rec["pass"] == 1 and rec["screens"]["start.a"]


def test_an_old_format_card_mostly_rewritten_is_asked_on_star(game):
    # the card has no Does: line (P06, P42); both of start's two screens change text
    first_pass(game)
    edit(game, "Mom is at the stove.", "Mom is at the stove, humming.")
    edit(game, "You eat alone.", "You eat alone, fast.")
    items = reading.work_list(game, "p1")["items"]
    assert items and all(i["screen"] == "*" for i in items)
    assert len(items) == len({i["row"] for i in items})
    assert any(i["why"].startswith("most of start changed (2 of 2") for i in items)


def test_an_old_format_card_with_half_changed_still_asks_per_screen(game):
    first_pass(game)
    edit(game, "You eat alone.", "You eat alone, fast.")
    assert {i["screen"] for i in reading.work_list(game, "p1")["items"]} == {"start.b"}


def test_an_old_format_fail_stays_on_its_screen_when_rewritten(game):
    first_pass(game, verdict="FAIL")
    edit(game, "Mom is at the stove.", "Mom is at the stove, humming.")
    edit(game, "You eat alone.", "You eat alone, fast.")
    items = reading.work_list(game, "p1")["items"]
    assert any(i["screen"] == "start.a" and i["why"] == "failed last pass" for i in items)
