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
    (game / "cards" / "p1.md").write_text("PIECE p1\nBuilds: start, kitchen, peek\n")
    approve.approve(game, "p1", "yes")
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


def test_dev_build_never_writes_the_public_output_folder(game, monkeypatch):
    cmds = []
    monkeypatch.setattr(build.subprocess, "run", lambda cmd, cwd=None: cmds.append(cmd) or type("P", (), {"returncode": 0}))
    build.package(game)
    build.package(game, release=True)
    dev, rel = cmds
    assert dev[dev.index("--output") + 1].endswith("output_dev") and "--dev" in dev
    assert rel[rel.index("--output") + 1].endswith("/output") and "--dev" not in rel
