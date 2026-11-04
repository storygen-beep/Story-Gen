"""cite_check.py: a cite off an anchor found in several places is wrong, not a warning (J80, 2026-11-04)."""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cite_check  # noqa: E402

ENGINE = "engine.py"
# A cite needs a line number of two digits or more (cite_check.CITE), so the code starts at line 21.
SOURCE = ["// filler"] * 20 + [
    "setup.other = 1;",                         # 21
    "setup.equipItem(a);",                      # 22  a call
    "setup.other = 2;",                         # 23
    "setup.equipItem = function(itemId) {",     # 24  the definition
    "  var inside = 1;",                        # 25
    "};",                                       # 26
    "setup.equipItem(b);",                      # 27  a call
    "pair_of_things(1);",                       # 28
    "pair_of_things(2);",                       # 29
]


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A tiny repo with one engine file and a skill whose reference file holds the cites."""
    skill = tmp_path / "skill"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# skill\n")
    (tmp_path / ENGINE).write_text("\n".join(SOURCE) + "\n")
    for args in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"],
                 ["add", "."], ["commit", "-qm", "base"]):
        subprocess.run(["git", *args], cwd=tmp_path, check=True)
    monkeypatch.setattr(cite_check, "SKILL", str(skill))
    monkeypatch.setattr(cite_check, "REPO", str(tmp_path))
    monkeypatch.setattr(cite_check, "TARGETS", {ENGINE: ENGINE})
    return tmp_path


def _run(repo, doc, *flags):
    """Run main() on a reference file holding `doc`. Returns (exit code, doc after, printed)."""
    path = repo / "skill" / "references" / "r.md"
    path.write_text(doc)
    old = sys.argv
    sys.argv = ["cite_check.py", *flags]
    try:
        code = cite_check.main()
    finally:
        sys.argv = old
    return code, path.read_text()


def _shift_engine(repo, n=3):
    """An uncommitted engine edit: n new lines at the top."""
    (repo / ENGINE).write_text("\n".join(["// new"] * n + SOURCE) + "\n")


def test_off_every_hit_counts_as_wrong_and_fails_strict(repo, capsys):
    # the name comes straight before the cite; line 21 holds none of its hits
    code, _ = _run(repo, "See `setup.equipItem` (`engine.py:21`).\n", "--strict")
    out = capsys.readouterr().out
    assert code == 1
    assert "1 citation(s) point at the wrong line" in out
    assert "of 1 live cites: 0 confirmed right, 1 wrong, 0 can't be checked" in out


def test_on_one_of_the_hits_is_right(repo, capsys):
    code, _ = _run(repo, "See `setup.equipItem` (`engine.py:27`).\n", "--strict")
    assert code == 0
    assert "1 confirmed right, 0 wrong" in capsys.readouterr().out


def test_a_line_inside_the_named_function_is_right(repo):
    code, _ = _run(repo, "See `setup.equipItem` (`engine.py:25`).\n", "--strict")
    assert code == 0


def test_a_name_that_only_sits_nearby_is_uncheckable_not_wrong(repo, capsys):
    code, _ = _run(repo, "The predicate (`engine.py:21`) and `setup.equipItem` agree.\n", "--strict")
    assert code == 0
    assert "0 confirmed right, 0 wrong, 1 can't be checked" in capsys.readouterr().out


def test_fix_follows_the_uncommitted_diff(repo):
    doc = "A call: `pair_of_things` (`engine.py:28`).\n"
    _run(repo, doc)
    _shift_engine(repo)
    _, after = _run(repo, doc, "--fix")
    assert "`engine.py:31`" in after     # the same call, not its twin on the next line


def test_fix_falls_back_on_the_one_definition(repo):
    _, after = _run(repo, "See `setup.equipItem` (`engine.py:21`).\n", "--fix")
    assert "`engine.py:24`" in after


def test_fix_leaves_and_lists_what_it_cannot_place(repo, capsys):
    # two hits, neither a definition, and no engine edit to follow
    doc = "See `pair_of_things` (`engine.py:21`).\n"
    code, after = _run(repo, doc, "--fix", "--verbose")
    assert after == doc
    assert "references/r.md:1  engine.py:21" in capsys.readouterr().out


def test_fix_never_moves_a_range(repo):
    doc = "See `setup.equipItem` (`engine.py:21-21`).\n"
    _, after = _run(repo, doc, "--fix")
    assert after == doc


def test_fix_does_not_collapse_two_cites_on_one_line(repo):
    doc = "`setup.equipItem` (`engine.py:21`) and `setup.equipItem` (`engine.py:23`).\n"
    _, after = _run(repo, doc, "--fix")
    assert after == doc


def test_fix_twice_changes_nothing_the_second_time(repo):
    doc = "A call: `pair_of_things` (`engine.py:28`).\n"
    _run(repo, doc)
    _shift_engine(repo)
    _, once = _run(repo, doc, "--fix")
    _, twice = _run(repo, once, "--fix")
    assert "`engine.py:31`" in once
    assert once == twice


def test_fix_carries_a_range_with_the_diff(repo):
    doc = "See `pair_of_things` (`engine.py:28-29`).\n"
    _run(repo, doc)
    _shift_engine(repo)
    _, after = _run(repo, doc, "--fix")
    assert "`engine.py:31-32`" in after


def test_fix_carries_a_cite_whose_name_is_only_in_a_string(repo):
    more = ['if kind == "the_kind":', "the_kind(1)", "the_kind(2)"]   # line 30 is the string
    (repo / ENGINE).write_text("\n".join(SOURCE + more) + "\n")
    subprocess.run(["git", "commit", "-qam", "more"], cwd=repo, check=True)
    doc = "See `the_kind` (`engine.py:30`).\n"
    code, _ = _run(repo, doc, "--strict")
    assert code == 0
    (repo / ENGINE).write_text("\n".join(["// new"] * 5 + SOURCE + more) + "\n")
    _, after = _run(repo, doc, "--fix")
    assert "`engine.py:35`" in after


def test_a_cite_with_no_anchor_is_never_moved(repo):
    doc = "Something happens at engine.py:27 for reasons.\n"
    _run(repo, doc)
    _shift_engine(repo)
    _, after = _run(repo, doc, "--fix")
    assert after == doc


def test_carry_line_returns_none_when_the_line_was_rewritten():
    assert cite_check.carry_line(10, [(10, 1, 10, 1)]) is None
    assert cite_check.carry_line(5, [(10, 1, 10, 1)]) == 5
    assert cite_check.carry_line(20, [(10, 0, 11, 3)]) == 23
