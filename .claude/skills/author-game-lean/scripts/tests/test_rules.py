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


def test_a_changed_screen_asks_only_its_truth_rows_after_the_first_reading(game):
    card(game)
    work = reading.work_list(game, "p1")
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="start.a", verdict="PASS") for i in work["items"]]})
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("You pull your jeans on.", "You pull your jeans on, fast."))
    items = reading.work_list(game, "p1")["items"]
    table = rules.table()
    assert items and all(i["screen"] == "start.b" and reading.reads_truth(i["row"], table) for i in items)
    assert {"C460", "B10"} <= {i["row"] for i in items}

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
    table = rules.table()
    assert work["items"] and all(i["screen"] == "start.b" and reading.reads_truth(i["row"], table)
                                 for i in work["items"])
    lst = rules.rule_list(rules.card_does(DOES))
    a_only = {r for r, on in lst.items() if on == ["start.a"]}
    assert a_only and a_only <= {v["row"] for v in work["carried"]}  # carried, not asked

def test_a_changed_screen_sends_nothing_back_on_star(game):
    work = scene_wide_pass(game)
    assert not any(i["screen"] == "*" for i in work["items"])  # B1, B2, B9 carry unless a screen is new

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


# ── a one-time step she can say no to fires on arrival (P21's card, 2026-11-24) ──

AUTOFIRE = MERGED + """
[[canvases]]
id = "hire"
[canvases.trigger]
location = "home"
is_repeatable = false
[[canvases.nodes]]
id = "ask"
blocks = [{ type = "paragraph", content = "Mom looks up from the counter." }]
"""


def autofire_game(game, conditions=""):
    (game / "toml_phases" / "7_final_game.toml").write_text(AUTOFIRE + conditions)
    return check.load_merged(game)


def test_a_one_time_step_with_a_no_and_no_presence_gate_is_red(game):
    g = autofire_game(game)
    rows = rules.guard({"hire.ask": ["a person's arc step", "a no is possible"]}, g)
    assert any("fires by itself on arrival" in r for r in rows)


def test_a_presence_gate_or_a_repeatable_row_is_not_red(game):
    g = autofire_game(game, """[canvases.trigger.conditions]
version = "1.0"
items = [{ type = "npc_at_location", npc_id = "npc_mom", location_id = "home", operator = "is_present" }]
""")
    rows = rules.guard({"hire.ask": ["a person's arc step", "a no is possible"]}, g)
    assert not any("fires by itself" in r for r in rows)
    g = autofire_game(game)
    rows = rules.guard({"hire.ask": ["a person's arc step"]}, g)  # no "no" here: an arrival scene she can't refuse
    assert not any("fires by itself" in r for r in rows)


# ── a note's FAIL carries; a fact-only change asks only the rows that read facts (P10, P21 pass B, 2026-11-24) ──

def _passed(game, verdict_for=lambda r: "PASS"):
    card(game)
    work = reading.work_list(game, "p1")
    out = {"verdicts": [], "causes": [{"id": "c1", "what": "x"}]}
    for i in work["items"]:
        v = verdict_for(i["row"])
        out["verdicts"].append(dict(row=i["row"], screen="start.a" if v == "FAIL" else "*", verdict=v,
                                    cause="c1" if v == "FAIL" else None))
    return reading.record(game, "p1", out)


def _rows_on_a(judge):
    table = rules.table()
    lst = rules.rule_list(rules.card_does(DOES), rows=table)
    return [r for r, on in lst.items() if "start.a" in on and table[r]["judge"] == judge and not reading.reads_facts(r, table)]


def test_a_note_fail_carries_and_a_reader_fail_comes_back(game):
    note, reader = _rows_on_a("note")[0], _rows_on_a("reader")[0]
    _passed(game, lambda r: "FAIL" if r in (note, reader) else "PASS")
    items = {(i["row"], i["why"]) for i in reading.work_list(game, "p1")["items"]}
    assert (reader, "failed last pass") in items and not any(r == note for r, _ in items)
    rec = reading.load_record(game, "p1")
    assert [v["cause"] for v in rec["verdicts"] if v["row"] == note] == [None]  # kept out of causes
    assert any("notes, shown" in line for line in reading.by_cause(rec))


def test_a_note_fail_reopens_when_its_screen_changes(game):
    note = _rows_on_a("note")[0]
    _passed(game, lambda r: "FAIL" if r == note else "PASS")
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("Mom is at the stove.", "Mom is at the stove, humming."))
    assert any(i["row"] == note and i["screen"] == "start.a" for i in reading.work_list(game, "p1")["items"])


def test_a_fact_only_change_asks_only_the_rows_that_read_facts(game):
    _passed(game)
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace('end_time = "07:10"', 'end_time = "07:20"'))  # Mom's row moves
    items = reading.work_list(game, "p1")["items"]
    table = rules.table()
    assert items and all(i["why"] == "a fact changed" for i in items)
    assert all(reading.reads_facts(i["row"], table) for i in items)
    assert {"C460", "B10"} <= {i["row"] for i in items}


# ── a partial batch (a reader pass that dies mid-way can be saved in parts, 2026-11-24) ──

def test_a_partial_record_keeps_the_unanswered_items_on_the_next_list(game):
    card(game)
    items = reading.work_list(game, "p1")["items"]
    half = items[: len(items) // 2]
    rec = reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="*", verdict="PASS") for i in half]})
    assert rec["answered"] == len(half) and len(rec["pending"]) == len(items) - len(half) and rec["pass"] == 1
    nxt = reading.work_list(game, "p1")["items"]
    assert {(i["row"], i["screen"]) for i in nxt} == {(i["row"], i["screen"]) for i in items[len(half):]}
    assert all(i["why"].startswith("still to ask") or i["why"] == "never judged" for i in nxt)
    rec = reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="*", verdict="PASS") for i in nxt]})
    assert rec["pending"] == [] and rec["pass"] == 1  # the same pass, finished in two batches
    assert reading.work_list(game, "p1")["items"] == []


def test_a_pending_changed_screen_row_survives_the_new_hashes(game):
    _passed(game)
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("You pull your jeans on.", "You pull your jeans on, fast."))
    items = reading.work_list(game, "p1")["items"]
    first, rest = items[:1], items[1:]
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen=i["screen"], verdict="PASS") for i in first]})
    assert {(i["row"], i["screen"]) for i in reading.work_list(game, "p1")["items"]} == {(i["row"], i["screen"]) for i in rest}


def test_an_unanswered_fail_stays_a_fail(game):
    reader = _rows_on_a("reader")[0]
    _passed(game, lambda r: "FAIL" if r == reader else "PASS")
    reading.record(game, "p1", {"verdicts": []})  # an empty batch
    rec = reading.load_record(game, "p1")
    assert any(v["row"] == reader and v["verdict"] == "FAIL" for v in rec["verdicts"])
    assert any(i["row"] == reader for i in reading.work_list(game, "p1")["items"])


def test_a_partial_batch_still_refuses_a_star_fail_and_an_off_list_verdict(game):
    card(game)
    item = reading.work_list(game, "p1")["items"][0]
    with pytest.raises(ValueError, match="never"):
        reading.record(game, "p1", {"verdicts": [dict(item, verdict="FAIL", cause="c1")], "causes": [{"id": "c1"}]})
    with pytest.raises(ValueError, match="work list"):
        reading.record(game, "p1", {"verdicts": [{"row": "C99999", "screen": "start.a", "verdict": "PASS"}]})


def test_a_card_not_built_yet_is_not_judged_by_sheet_or_does(game):
    # the overlap rule: the next piece is carded and approved while the reader runs, and built later
    (game / "cards" / "p2.md").write_text("PIECE p2\nSheet:\n  later.a | 09:00–09:05 | home | nobody | any | none\n"
                                          "Does:\n  later.a | the clock moves\nBuilds: later\n")
    g = check.load_merged(game)
    assert not any(r.startswith("p2:") for r in check.check_sheet(game, g)[1] + check.check_does(game, g)[1])


def test_a_partly_built_card_is_judged_and_its_missing_screen_is_red(game):
    card(game, DOES + "  start.c | the clock moves\n",
         SHEET + "  start.c | 07:15–07:20 | hall | nobody | jeans, pyjamas | met_mom\n")
    g = check.load_merged(game)
    assert any("start.c is on the card's Sheet: but not built" in r for r in check.check_sheet(game, g)[1])
    assert any("start.c is not built" in r for r in check.check_does(game, g)[1])


# ── a mostly rewritten canvas is asked on "*" once (P34, 2026-11-24: 1,986 items after talk lines on 22 screens) ──

def ten_screens(game):
    nodes = "".join(f'\n[[canvases.nodes]]\nid = "s{i}"\nblocks = [{{ type = "paragraph", content = "Line {i}." }}]\n'
                    for i in range(10))
    (game / "toml_phases" / "7_final_game.toml").write_text(
        '[[locations]]\nid = "home"\n\n[[canvases]]\nid = "big"\n[canvases.trigger]\nlocation = "home"\n' + nodes)
    does = "Does:\n" + "".join(f"  big.s{i} | a repeatable, the clock moves\n" for i in range(10))
    (game / "cards" / "p1.md").write_text("PIECE p1\n" + does + "Builds: big, home\n")
    work = reading.work_list(game, "p1")
    reading.record(game, "p1", {"verdicts": [dict(row=i["row"], screen="*", verdict="PASS") for i in work["items"]]})


def rewrite(game, n):
    p = game / "toml_phases" / "7_final_game.toml"
    t = p.read_text()
    for i in range(n):
        t = t.replace(f"Line {i}.", f"Line {i}, rewritten.")
    p.write_text(t)


def test_one_changed_screen_of_ten_still_asks_per_screen(game):
    ten_screens(game)
    rewrite(game, 1)
    items = reading.work_list(game, "p1")["items"]
    assert items and {i["screen"] for i in items} <= {"big.s0", "*"}
    assert any(i["screen"] == "big.s0" for i in items)
    assert all(i["screen"] != "*" or i["row"] in reading.SCENE_WIDE for i in items)


def test_a_canvas_of_mostly_new_screens_asks_on_star_once(game):
    ten_screens(game)
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text() + "".join(f'\n[[canvases.nodes]]\nid = "n{i}"\nblocks = [{{ type = "paragraph", content = "New {i}." }}]\n'
                                         for i in range(11)))
    does = "Does:\n" + "".join(f"  big.s{i} | a repeatable, the clock moves\n" for i in range(10)) + \
        "".join(f"  big.n{i} | a repeatable, the clock moves\n" for i in range(11))
    (game / "cards" / "p1.md").write_text("PIECE p1\n" + does + "Builds: big, home\n")
    items = reading.work_list(game, "p1")["items"]
    assert items and all(i["screen"] == "*" for i in items)
    assert len(items) == len({i["row"] for i in items})
    assert any(i["why"].startswith("most of big is new (11 of 21") for i in items)

def test_a_fail_on_a_changed_screen_stays_per_screen_either_way(game):
    ten_screens(game)
    work = reading.work_list(game, "p1")
    rec = reading.load_record(game, "p1")
    rec["verdicts"] = [dict(v, verdict="FAIL", screen="big.s1", cause="c1") if v["row"] == "C460" else v
                       for v in rec["verdicts"]]
    rec["causes"] = [{"id": "c1", "what": "x"}]
    reading.record_path(game, "p1").write_text(__import__("json").dumps(rec))
    for n in (1, 8):
        rewrite(game, n)
        items = reading.work_list(game, "p1")["items"]
        assert any(i["row"] == "C460" and i["screen"] == "big.s1" for i in items), n


# ── disjoint batches of one pass, recorded in any order (P34, 2026-11-24) ──

@pytest.mark.parametrize("order", [(0, 1, 2), (2, 0, 1), (1, 2, 0)])
def test_three_disjoint_batches_land_in_any_order_and_a_late_fail_is_kept(game, order):
    card(game)
    rows = [i["row"] for i in reading.work_list(game, "p1")["items"]]
    x, y = rows[0], rows[1]
    batches = [
        [dict(row=x, screen="start.a", verdict="PASS")] + [dict(row=r, screen="*", verdict="PASS") for r in rows[2::3]],
        [dict(row=x, screen="start.b", verdict="PASS")] + [dict(row=r, screen="*", verdict="PASS") for r in rows[3::3]],
        [dict(row=y, screen="start.b", verdict="FAIL", cause="c1")] + [dict(row=r, screen="*", verdict="PASS")
                                                                       for r in rows[4::3]],
    ]
    for i in order:
        rec = reading.record(game, "p1", {"verdicts": batches[i], "causes": [{"id": "c1", "what": "y"}]})
    got = {(v["row"], v["screen"]): v["verdict"] for v in rec["verdicts"]}
    assert got[(x, "start.a")] == "PASS" and got[(x, "start.b")] == "PASS"
    assert got[(y, "start.b")] == "FAIL"
    assert rec["pending"] == [] and rec["pass"] == 1


def test_a_fail_no_longer_owed_is_kept_and_reported(game):
    _passed(game)  # a full pass: nothing is owed now
    reader = _rows_on_a("reader")[0]
    rec = reading.record(game, "p1", {"verdicts": [dict(row=reader, screen="start.a", verdict="FAIL", cause="c1")],
                                      "causes": [{"id": "c1", "what": "late"}]})
    assert [reader, "start.a"] in rec["unowed"]
    assert any(v["row"] == reader and v["verdict"] == "FAIL" for v in rec["verdicts"])
    other = _rows_on_a("reader")[1]
    with pytest.raises(ValueError, match="work list"):  # a PASS no longer owed is still refused
        reading.record(game, "p1", {"verdicts": [dict(row=other, screen="start.a", verdict="PASS")]})


# ── LO's stop rule (2026-11-24): after the first reading, a fix re-asks its FAILs and the truth rows, not every row ──

def test_after_pass_one_a_one_line_change_asks_only_its_fails_and_truth_rows(game):
    reader = _rows_on_a("reader")[0]
    _passed(game, lambda r: "FAIL" if r == reader else "PASS")
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("Mom is at the stove.", "Mom is at the stove, humming."))
    items = reading.work_list(game, "p1")["items"]
    table = rules.table()
    assert (reader, "start.a") in {(i["row"], i["screen"]) for i in items}  # the FAIL, to verify the fix
    assert all(i["row"] == reader or reading.reads_truth(i["row"], table) for i in items)
    assert len(items) < len(rules.rule_list(rules.card_does(DOES)))


def test_a_new_screen_is_asked_in_full(game):
    _passed(game)
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text() + '\n[[canvases.nodes]]\nid = "c"\nblocks = [{ type = "paragraph", content = "New." }]\n')
    (game / "cards" / "p1.md").write_text("PIECE p1\nWhat the player sees:\n  Screen 1: Mom.\n" + SHEET +
                                          DOES + "  start.c | the opening, a one-time step, the clock moves\n" +
                                          "Builds: start, home\n")
    on_c = {r for r, on in rules.rule_list(rules.card_does(DOES + "  start.c | the opening, a one-time step, "
                                                                  "the clock moves\n")).items() if "start.c" in on}
    asked_c = {i["row"] for i in reading.work_list(game, "p1")["items"] if i["screen"] == "start.c"}
    assert on_c and on_c <= asked_c


def test_all_still_asks_everything(game):
    _passed(game)
    every = reading.work_list(game, "p1", everything=True)["items"]
    assert {i["row"] for i in every} == set(reading.work_list(game, "p1", everything=True)["rows"])


def test_pending_items_saved_before_the_stop_rule_are_rejudged_by_it(game):
    _passed(game)
    rec = reading.load_record(game, "p1")
    table = rules.table()
    non_truth = next(r for r in rules.rule_list(rules.card_does(DOES)) if not reading.reads_truth(r, table))
    rec["pending"] = [{"row": non_truth, "screen": "start.a", "why": "screen changed"},
                      {"row": "C460", "screen": "start.a", "why": "screen changed"},
                      {"row": non_truth, "screen": "start.b", "why": "screen is new"}]
    reading.record_path(game, "p1").write_text(__import__("json").dumps(rec))
    asked = {(i["row"], i["screen"]) for i in reading.work_list(game, "p1")["items"]}
    assert (non_truth, "start.a") not in asked  # owed only because the text changed: carries now
    assert ("C460", "start.a") in asked and (non_truth, "start.b") in asked


# ── --waive: a held FAIL waived in LO's words (P07, 2026-11-24) ──

WORDS = "hotter will stay locked in for the release one"


def _held_fail(game):
    reader = _rows_on_a("reader")[0]
    _passed(game, lambda r: "FAIL" if r == reader else "PASS")
    return reader


def test_waive_turns_a_held_fail_into_waived_and_it_carries(game):
    reader = _held_fail(game)
    reading.waive(game, "p1", reader, "start.a", WORDS, "main-lean session, 2026-11-24")
    v = next(v for v in reading.load_record(game, "p1")["verdicts"] if v["row"] == reader)
    assert v["verdict"] == "WAIVED" and v["waived_words"] == WORDS and "2026-11-24" in v["waived_source"]
    assert not any(i["row"] == reader for i in reading.work_list(game, "p1")["items"])


def test_waive_refuses_a_row_that_is_not_a_held_fail_and_empty_words(game):
    reader = _held_fail(game)
    other = _rows_on_a("reader")[1]
    with pytest.raises(ValueError, match="held FAIL"):
        reading.waive(game, "p1", other, "start.a", WORDS, "chat")
    with pytest.raises(ValueError, match="own words"):
        reading.waive(game, "p1", reader, "start.a", "  ", "chat")
    with pytest.raises(ValueError, match="where and when"):
        reading.waive(game, "p1", reader, "start.a", WORDS, "")


def test_a_waived_row_reopens_when_its_screen_changes(game):
    reader = _held_fail(game)
    reading.waive(game, "p1", reader, "start.a", WORDS, "chat, 2026-11-24")
    p = game / "toml_phases" / "7_final_game.toml"
    p.write_text(p.read_text().replace("Mom is at the stove.", "Mom is at the stove, humming."))
    assert any(i["row"] == reader and i["why"] == "waived, its screen changed"
               for i in reading.work_list(game, "p1")["items"])


def test_waive_cli(game, capsys):
    reader = _held_fail(game)
    assert reading.main([str(game), "p1", "--waive", reader, "start.a", "--words", WORDS, "--source", "chat"]) == 0
    assert "NOTES.md: Waived:" in capsys.readouterr().out
