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


def test_an_old_format_card_rewritten_after_its_first_reading_asks_only_truth_rows(game):
    # LO's stop rule (2026-11-24): both of start's screens change text after pass 1; a card without Does: (P06, P42)
    first_pass(game)
    edit(game, "Mom is at the stove.", "Mom is at the stove, humming.")
    edit(game, "You eat alone.", "You eat alone, fast.")
    items = reading.work_list(game, "p1")["items"]
    assert items and {i["row"] for i in items} <= set(reading.TRUTH_ROWS)
    assert {i["screen"] for i in items} == {"start.a", "start.b"}


def test_an_old_format_card_with_one_screen_changed_asks_only_there(game):
    first_pass(game)
    edit(game, "You eat alone.", "You eat alone, fast.")
    items = reading.work_list(game, "p1")["items"]
    assert {i["screen"] for i in items} == {"start.b"} and {i["row"] for i in items} <= set(reading.TRUTH_ROWS)


def test_an_old_format_fail_stays_on_its_screen_when_rewritten(game):
    first_pass(game, verdict="FAIL")
    edit(game, "Mom is at the stove.", "Mom is at the stove, humming.")
    edit(game, "You eat alone.", "You eat alone, fast.")
    items = reading.work_list(game, "p1")["items"]
    assert any(i["screen"] == "start.a" and i["why"] == "failed last pass" for i in items)


def test_a_retired_canvas_has_no_rows_on_the_work_list(game):
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace('[canvases.trigger]\nlocation = "home"', '[canvases.trigger]\nlocation = "home"\nis_active = false', 1))
    assert reading.current(game, "p1")[0] == {"*": reading.whole_hash({})}
    p.write_text(p.read_text().replace("is_active = false\n", "", 1))
    assert "start.a" in reading.current(game, "p1")[0]


def test_a_note_fail_on_an_old_format_card_is_recorded_without_a_cause_and_carried(game):
    # P06: an old-format card (no Does:) with FAILs on C1313 and C1434, both `note` in craft/systems.md
    (game / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start\nCraft: craft/voice.md, craft/systems.md · cites C442\n")
    work = reading.work_list(game, "p1")
    assert {"C1313", "C1434"} <= {i["row"] for i in work["items"]}
    out = [dict(row=i["row"], screen="start.a", verdict="FAIL" if i["row"] in ("C1313", "C1434") else "PASS")
           for i in work["items"]]
    rec = reading.record(game, "p1", {"verdicts": out})  # no causes given: notes need none
    assert all(v["cause"] is None and v["note"] for v in rec["verdicts"] if v["row"] in ("C1313", "C1434"))
    assert reading.work_list(game, "p1")["items"] == []  # carried, not asked again
    with pytest.raises(ValueError, match="cause"):  # a reader row's FAIL still needs a cause
        reading.record(game, "p1", {"verdicts": [{"row": "C442", "screen": "start.a", "verdict": "FAIL"}]})


def test_a_reworded_activity_reopens_nothing(game):
    # P07 and others, 2026-11-24: six schedule activities reworded, no hour or place moved
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace('end_time = "09:00"', 'end_time = "09:00"\nactivity = "at the stove"'))
    first_pass(game)
    p.write_text(p.read_text().replace('activity = "at the stove"', 'activity = "making eggs"'))
    assert reading.work_list(game, "p1")["items"] == []
    p.write_text(p.read_text().replace('end_time = "09:00"', 'end_time = "08:00"'))  # a real move still counts
    assert reading.work_list(game, "p1")["items"]


def test_an_old_format_card_fact_change_asks_only_fact_rows(game):
    first_pass(game)
    edit(game, 'end_time = "09:00"', 'end_time = "08:00"')  # Mom's row moves; the text doesn't
    items = reading.work_list(game, "p1")["items"]
    assert items and all(reading.reads_facts(i["row"], reading.rules.table()) for i in items)
    assert all(i["why"] == "a fact changed" for i in items)


def test_a_record_from_before_facts2_reads_as_unchanged_once(game):
    first_pass(game)
    path = reading.record_path(game, "p1")
    rec = json.loads(path.read_text())
    for v in rec["screens"].values():
        if isinstance(v, dict):
            v.pop("facts2", None)
    path.write_text(json.dumps(rec))
    edit(game, 'end_time = "09:00"', 'end_time = "08:00"')
    assert reading.work_list(game, "p1")["items"] == []
