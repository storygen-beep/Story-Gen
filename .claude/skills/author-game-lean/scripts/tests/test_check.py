"""check.py and build.py: a clean tiny game is GREEN, and every planted bug turns its check red (or INCOMPLETE).
Each test builds a throwaway game in tmp_path and runs the repo's real merge script on it. Nothing in games/ is read."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import approve  # noqa: E402
import build  # noqa: E402
import check  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiny_game import canvas, make_game  # noqa: E402

@pytest.fixture
def game(tmp_path):
    return make_game(tmp_path)


def run(g, *flags, capsys=None):
    code = check.main([str(g), *flags])
    out = capsys.readouterr().out if capsys else ""
    return code, out


def results(g, release=False):
    return check.run_all(g, release)


def test_clean_game_is_green(game, capsys):
    code, out = run(game, capsys=capsys)
    assert code == 0 and out.startswith("GREEN")


def test_planted_broken_toml_is_red_merge(game):
    (game / "toml_phases" / "5_scenes.toml").write_text('[[canvases]]\nid = "start\n')
    r = results(game)
    assert r["merge"][0] == check.RED
    assert r["reach"][0] == check.INCOMPLETE and r["builds"][0] == check.INCOMPLETE  # never green on a skip


def test_planted_scene_nothing_opens_is_red_reach(game):
    p = game / "toml_phases" / "5_scenes.toml"
    p.write_text(p.read_text() + "\n" + canvas("peek", substitution_only="true"))
    (game / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start, kitchen, home, peek\n")
    approve.record_approval(game, "p1", "yes")  # a fixture card: not about the card check
    r = results(game)
    assert r["reach"][0] == check.RED and "`peek`" in r["reach"][1][0]


def test_planted_built_row_without_approval_is_red(game):
    (game / "approvals.json").unlink()
    r = results(game)
    assert r["approvals"][0] == check.RED and "no approval" in r["approvals"][1][0]


def test_planted_card_edited_after_yes_is_red(game):
    (game / "cards" / "p1.md").write_text("PIECE p1 · edited\nBuilds: start, kitchen\n")
    r = results(game)
    assert r["approvals"][0] == check.RED and "changed after the yes" in r["approvals"][1][0]


def test_planted_extra_canvas_next_to_approved_one_is_red_builds(game):
    p = game / "toml_phases" / "5_scenes.toml"
    p.write_text(p.read_text() + "\n" + canvas("kitchen_variant_b"))
    r = results(game)
    assert r["builds"] == (check.RED, ["canvas `kitchen_variant_b` is built but never approved "
                                       "(no approved card lists it in Builds:)"])


def test_planted_changed_card_covers_nothing(game):
    (game / "cards" / "p1.md").write_text("PIECE p1 · edited after the yes\nBuilds: start, kitchen\n")
    r = results(game)
    assert r["builds"][0] == check.RED
    assert {"`start`", "`kitchen`"} <= {row.split()[1] for row in r["builds"][1]}


def test_dev_canvases_are_skipped_by_builds(game):
    assert results(game)["builds"] == (check.GREEN, [])


def test_planted_dev_canvas_in_release_is_red(game):
    (game / "output").mkdir()
    (game / "output" / "index.html").write_text("<html>Dev jump: to the kitchen</html>")
    r = results(game, release=True)
    assert r["release"][0] == check.RED and "Dev jump: to the kitchen" in r["release"][1][0]


def test_release_with_clean_html_is_green(game):
    (game / "output").mkdir()
    (game / "output" / "index.html").write_text("<html>start kitchen</html>")
    assert results(game, release=True)["release"] == (check.GREEN, [])


def test_release_without_built_html_is_incomplete(game):
    assert results(game, release=True)["release"][0] == check.INCOMPLETE


def test_planted_no_state_is_incomplete_never_green(game, capsys):
    (game / "STATE.md").unlink()
    code, out = run(game, capsys=capsys)
    assert code == 2 and out.startswith("INCOMPLETE") and "GREEN" not in out


def test_every_red_prints_every_run_new_marks_only_new(game, capsys):
    p = game / "toml_phases" / "5_scenes.toml"
    p.write_text(p.read_text() + "\n" + canvas("extra_one"))
    code, out = run(game, capsys=capsys)
    assert code == 1 and "NEW RED [builds]" in out and "`extra_one`" in out
    code, out = run(game, capsys=capsys)
    assert code == 1 and "`extra_one`" in out and "NEW" not in out  # still printed, no longer NEW


def test_fixed_shows_once_then_no_change(game, capsys):
    p = game / "toml_phases" / "5_scenes.toml"
    clean = p.read_text()
    p.write_text(clean + "\n" + canvas("extra_one"))
    run(game, capsys=capsys)
    p.write_text(clean)
    code, out = run(game, capsys=capsys)
    assert code == 0 and "FIXED [builds]" in out
    code, out = run(game, capsys=capsys)
    assert code == 0 and "no change since last run" in out


def test_last_run_is_stored_per_mode(game, capsys):
    run(game, capsys=capsys)
    saved = json.loads((game / check.LAST).read_text())
    assert saved["dev"]["builds"][0] == check.GREEN


def test_build_refuses_an_unapproved_canvas_and_packages_nothing(game, capsys, monkeypatch):
    p = game / "toml_phases" / "5_scenes.toml"
    p.write_text(p.read_text() + "\n" + canvas("kitchen_variant_b"))
    called = []
    monkeypatch.setattr(build, "package", lambda g, release=False: called.append(g) or 0)
    assert build.main([str(game)]) == 1
    assert called == [] and "REFUSED" in capsys.readouterr().out


def test_build_packages_when_everything_is_approved(game, capsys, monkeypatch):
    called = []
    monkeypatch.setattr(build, "package", lambda g, release=False: called.append((g, release)) or 0)
    assert build.main([str(game)]) == 0 and called[0][1] is False
    # the mocked package writes no HTML, so the release check can't search it: INCOMPLETE (2), never GREEN
    assert build.main([str(game), "--release"]) == 2 and called[-1][1] is True


def test_every_build_writes_the_output_folder(game, monkeypatch):
    cmds = []
    monkeypatch.setattr(build.subprocess, "run", lambda cmd, cwd=None: cmds.append(cmd) or type("P", (), {"returncode": 0}))
    build.package(game)
    build.package(game, release=True)
    dev, rel = cmds
    assert dev[dev.index("--output") + 1].endswith("/output") and "--dev" in dev and "--debug" in dev
    assert rel[rel.index("--output") + 1].endswith("/output") and "--dev" not in rel and "--debug" not in rel


# ── change 6 (2026-11-20): places, people and sidebar items need an approved card too ──────────────────────

def add_phase(game, text):
    p = game / "toml_phases" / "1_metadata_and_locations.toml"
    p.write_text(p.read_text() + "\n" + text)


def test_planted_extra_place_is_red(game):
    add_phase(game, '[[locations]]\nid = "gym"\n')
    assert ("place `gym` is built but never approved (no approved card lists it in Builds:)"
            in results(game)["builds"][1])


def test_planted_extra_person_is_red(game):
    add_phase(game, '[[npcs]]\nid = "npc_x"\nname = "X"\n')
    assert any(r.startswith("person `npc_x`") for r in results(game)["builds"][1])


def test_planted_extra_sidebar_item_is_red(game):
    add_phase(game, '[[sidebar_items]]\ntype = "trait_bar"\ntrait = "energy"\nlabel = "Energy"\n')
    assert any(r.startswith("sidebar item `sidebar:energy`") for r in results(game)["builds"][1])


def test_a_card_that_lists_place_person_and_sidebar_is_green(game):
    add_phase(game, '[[locations]]\nid = "gym"\n\n[[npcs]]\nid = "npc_x"\nname = "X"\n\n'
                    '[[sidebar_items]]\ntype = "trait_bar"\ntrait = "energy"\n')
    (game / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start, kitchen, home, gym, npc_x, sidebar:energy\n")
    approve.record_approval(game, "p1", "yes")  # a fixture card: not about the card check
    assert results(game)["builds"] == (check.GREEN, [])


# ── the card check: check.py --card ─────────────────────────────────────────────────────────────────────────

@pytest.fixture
def skill(tmp_path):
    """A craft folder with one file whose must-read rows are C1 and L2."""
    s = tmp_path / "skill"
    (s / "craft").mkdir(parents=True)
    (s / "craft" / "people.md").write_text("# area\n\n## Must read\n\n| id | what |\n|---|---|\n| C1 | a |\n| L2 | b |\n\n"
                                         "## The shape\n\n| C9 | not a must-read row |\n")
    (s / "craft" / "media.md").write_text("## Must read\n\n| id | what |\n|---|---|\n| C3 | c |\n")
    return s


def card(game, craft, media=0, areas="people"):
    (game / "cards" / "c1.md").write_text(f"PIECE c1\nMedia: {media} spots\nBuilds: x\nAreas: {areas}\nCraft: {craft}\n")


def test_card_citing_or_skipping_every_must_read_is_green(game, skill):
    card(game, "craft/people.md · cites C1 · skip L2: no person in this piece")
    assert check.check_card(game, "c1", skill) == (check.GREEN, [])


def test_planted_card_missing_a_must_read_is_red(game, skill):
    card(game, "craft/people.md · cites C1")
    assert check.check_card(game, "c1", skill) == (
        check.RED, ["craft/people.md: must-read L2 is neither cited nor skipped with a reason"])


def test_planted_skip_without_a_reason_is_red(game, skill):
    card(game, "craft/people.md · cites C1 · skip L2: ")
    assert check.check_card(game, "c1", skill) == (check.RED, ["craft/people.md: `skip L2` gives no reason"])


def test_planted_media_spot_without_media_craft_is_red(game, skill):
    card(game, "craft/people.md · cites C1, L2", media=2)
    assert check.check_card(game, "c1", skill)[1] == [
        "the card has 2 media spot(s) and its Craft: line does not name craft/media.md"]


def test_planted_missing_craft_file_is_red(game, skill):
    card(game, "craft/people.md, craft/phone.md · cites C1, L2")
    assert check.check_card(game, "c1", skill)[1] == ["the Craft: line names craft/phone.md, which does not exist"]


def test_a_card_with_no_craft_line_is_red(game, skill):
    (game / "cards" / "c1.md").write_text("PIECE c1\nBuilds: x\nAreas: people\n")
    assert check.check_card(game, "c1", skill)[1] == [
        "the card has no Craft: line", "area `people`: the Craft: line does not name craft/people.md"]


def test_card_cli_exit_codes(game, skill, capsys, monkeypatch):
    monkeypatch.setattr(check, "SKILL", skill)
    card(game, "craft/people.md · cites C1, L2")
    assert check.main(["--card", str(game), "c1"]) == 0 and capsys.readouterr().out.startswith("GREEN")
    card(game, "craft/people.md · cites C1")
    assert check.main(["--card", str(game), "c1"]) == 1
    assert not (game / check.LAST).exists()  # the card check saves nothing


# ── the area line (LO, 2026-11-22): no piece in an area with no craft file ───────────────────────────────────

def test_planted_area_with_no_craft_file_is_red(game, skill):
    card(game, "craft/people.md · cites C1, L2", areas="people, clothes")
    assert check.check_card(game, "c1", skill)[1] == [
        "area `clothes` has no craft file yet: write craft/clothes.md first (piece.md step 1)"]


def test_area_with_its_craft_file_named_is_green(game, skill):
    (skill / "craft" / "clothes.md").write_text("## Must read\n\n| id | what |\n|---|---|\n| C5 | e |\n")
    card(game, "craft/people.md, craft/clothes.md · cites C1, L2, C5", areas="people, clothes")
    assert check.check_card(game, "c1", skill) == (check.GREEN, [])


def test_planted_area_whose_file_is_not_on_the_craft_line_is_red(game, skill):
    (skill / "craft" / "clothes.md").write_text("## Must read\n\n| id | what |\n|---|---|\n| C5 | e |\n")
    card(game, "craft/people.md · cites C1, L2", areas="people, clothes")
    assert check.check_card(game, "c1", skill)[1] == ["area `clothes`: the Craft: line does not name craft/clothes.md"]


def test_planted_card_with_no_areas_line_is_red(game, skill):
    (game / "cards" / "c1.md").write_text("PIECE c1\nBuilds: x\nCraft: craft/people.md · cites C1, L2\n")
    assert check.check_card(game, "c1", skill)[1] == ["the card has no Areas: line"]


def test_planted_empty_areas_line_is_red(game, skill):
    card(game, "craft/people.md · cites C1, L2", areas="")
    assert check.check_card(game, "c1", skill)[1] == ["the Areas: line names no area"]


def test_planted_unknown_area_is_red(game, skill):
    card(game, "craft/people.md · cites C1, L2", areas="people, romance")
    assert check.check_card(game, "c1", skill)[1] == ["Areas: `romance` is not an area (see SKILL.md, Where things live)"]


def test_first_hour_maps_to_the_opening_and_topics_to_their_files():
    assert check.area_file("first hour") == "craft/opening.md"
    assert check.area_file("body moments") == "craft/body-moments.md"
    for name in ("first hour", "media", "meters", "walk-ins", "body moments"):
        assert (check.SKILL / check.area_file(name)).is_file(), name


# ── --beat: explicit beats (C254, C249). The Watch beat is craft/heat.md's worked example. ─────────────────

WATCH = ("You stay behind the bush. He grabs her hips and fucks her harder. She moans into her own arm. "
         "He pulls out and cums across her ass in thick white strings. "
         "Your pussy is wet, and your thighs are pressed tight together.")


def beat_file(tmp_path, body):
    f = tmp_path / "card.md"
    f.write_text(f"PIECE P99 · test\n\nWhat the player sees:\n  [explicit] {body} [/explicit]\n  Choices: \"Leave\"\n")
    return f


def test_beat_watch_passes_with_five(tmp_path, capsys):
    words = check.explicit_words()
    assert len(words.findall(WATCH)) == 5
    assert check.main(["--beat", str(beat_file(tmp_path, WATCH))]) == 0
    assert capsys.readouterr().out.startswith("GREEN")


def test_planted_faded_beat_is_red(tmp_path):
    status, rows = check.check_beats(beat_file(tmp_path, "You stay behind the bush. You watch until it's over."))
    assert status == check.RED and any("needs 3" in r for r in rows)


def test_planted_pivoted_beat_is_red(tmp_path):
    pivot = WATCH + " You realise you'll never see the park the same way."
    status, rows = check.check_beats(beat_file(tmp_path, pivot))
    assert status == check.RED and len(rows) == 1 and "pivot" in rows[0]


def test_beat_runs_to_blank_line_and_strips_quotes(tmp_path):
    f = tmp_path / "beats.md"
    head, tail = WATCH.split(" She moans", 1)
    f.write_text(f"[explicit]\n> {head}\n> She moans{tail}\n\nYou realise nothing at all, ever.\n")
    assert check.check_beats(f)[0] == check.GREEN


def test_file_with_no_marked_beat_is_incomplete(tmp_path):
    f = tmp_path / "plain.md"
    f.write_text(WATCH + "\n")
    assert check.main(["--beat", str(f)]) == 2
