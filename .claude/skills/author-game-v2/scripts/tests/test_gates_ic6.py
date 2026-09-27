"""IC6 (PRD_IDEAS_AND_CRAFT, LO 2026-09-27): `prose has room` (the joints floor), the three
readable checks, the joints lint, and the token walk with its --ship BLOCK row."""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import readable  # noqa: E402

LOOSE = ("You want the job, but the money is bad. You take it because rent is due. "
         "He looks at you when you come in, so you look back. ") * 40
LISTY = ("You walk in and sit down and order and drink and pay and leave. " * 60)


def game(text, extra=None):
    g = {"project": {"id": "fx", "name": "fx", "starting_canvas": "c1"},
         "settings": {"narration_person": "second"},
         "player": {"core_traits": {"money": 10}},
         "locations": [{"id": "room_a", "name": "Room A"}],
         "npcs": [{"id": "npc_gil", "name": "Gil", "role": "step dad"}],
         "canvases": [{"id": "c1", "trigger": {"location": "room_a", "is_repeatable": False},
                       "nodes": [{"id": "n", "blocks": [{"type": "paragraph",
                                                         "content": text}]}]}]}
    g.update(extra or {})
    return g


def gate_result(g, name):
    model, g2 = gates.build(copy.deepcopy(g))
    results, _ = gates.score(model, g2)
    return next(r for r in results if r["gate"] == name)


# ── prose has room ───────────────────────────────────────────────────────────
def test_prose_with_its_joints_passes():
    r = gate_result(game(LOOSE), "prose has room")
    assert r["pass_"], r["headline"]


def test_a_list_of_ands_with_no_but_fails():
    r = gate_result(game(LISTY), "prose has room")
    assert not r["pass_"] and not r["na"]
    assert any("`but`" in d for d in r["detail"]) and any("`and`" in d for d in r["detail"])


def test_too_little_prose_is_na():
    assert gate_result(game("She stays. But not long."), "prose has room")["na"]


def test_sentence_length_prints_the_floor_it_does_not_judge():
    r = gate_result(game(LOOSE), "sentence length")
    assert f"p25 {gates.FIELD_SENTENCE_MEDIAN[0]}" in r["headline"] and "not judged" in r["headline"]


# ── readable ─────────────────────────────────────────────────────────────────
def test_a_pronoun_before_anyone_is_on_screen_is_listed():
    rows, note = readable.dangling(game("She left early."))
    assert note == "" and len(rows) == 1 and '"She"' in rows[0]


def test_a_role_on_screen_first_answers_it():
    rows, _ = readable.dangling(game("Your mum is in. She left early."))
    assert rows == []


def test_the_wrong_gender_does_not_answer():
    rows, _ = readable.dangling(game("Your mum doesn't know he paid."))
    assert len(rows) == 1 and '"he"' in rows[0]


def test_third_person_narration_is_not_run():
    g = game("She left early.", {"settings": {"narration_person": "third"}})
    rows, note = readable.dangling(g)
    assert rows == [] and note.startswith("not run")


def test_an_ungated_past_event_is_listed_and_a_flag_gate_clears_it():
    g = game("What happened last night?")
    assert len(readable.unearned_events(g)) == 1
    g["canvases"][0]["trigger"]["conditions"] = {"version": "1.0", "items": [
        {"type": "flag", "subject": "player", "flag_key": "went_out", "operator": "is_true"}]}
    assert readable.unearned_events(g) == []
    assert len(readable.unearned_events(g, universal={"went_out"})) == 1


def test_short_lines_without_a_verb_are_listed():
    rows, seen = readable.verbless(game("Ten dollars. Fast. You pay him."))
    assert seen == 3 and len(rows) == 2


def test_the_joints_lint_lists_the_shortest_screens():
    summary, rows = gates.lint_joints(game(LOOSE))
    assert "coordination ratio" in summary and rows and rows[0].startswith("c1: median sentence")


# ── tokens ───────────────────────────────────────────────────────────────────
def test_a_token_in_a_location_name_leaks():
    g = game("Hi.", {"locations": [{"id": "gil_room", "name": "@gil's Room"}]})
    _, player, _ = gates.lint_unresolved_tokens(g)
    assert len(player) == 1 and player[0].startswith("locations[].name")


def test_a_token_in_a_list_field_leaks():
    g = game("Hi.")
    g["npcs"][0]["tags"] = ["lives with @gil"]
    _, player, _ = gates.lint_unresolved_tokens(g)
    assert any(r.startswith("npcs[].tags[]") for r in player)


def test_a_token_in_block_content_is_fine():
    _, player, dev = gates.lint_unresolved_tokens(game("@gil is at the table."))
    assert player == [] and dev == []


def test_a_token_in_a_canvas_description_is_dev_only():
    g = game("Hi.")
    g["canvases"][0]["description"] = "@gil at the table"
    _, player, dev = gates.lint_unresolved_tokens(g)
    assert player == [] and len(dev) == 1


def test_ship_blocks_on_a_raw_token(tmp_path, monkeypatch, capsys):
    d = tmp_path / "games" / "fx"
    (d / "toml_phases").mkdir(parents=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps({}))
    live = game("Hi.", {"locations": [{"id": "gil_room", "name": "@gil's Room"}]})
    real_load = gates._load
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(live)
                        if str(p).endswith("7_final_game.toml") else real_load(p))
    monkeypatch.setattr(gates, "release_mode", lambda slug: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda slug: 0)
    block, _ = gates.ship_rows("fx", root=str(tmp_path))
    row = next(b for b in block if b[0] == "no raw token on screen")
    assert row[1] is False and "@gil" in row[3][0]
    real_rows = gates.ship_rows
    monkeypatch.setattr(gates, "ship_rows", lambda slug, root=None: real_rows(slug, str(tmp_path)))
    assert gates.ship_mode("fx") == 1
    assert "no raw token on screen" in capsys.readouterr().out
