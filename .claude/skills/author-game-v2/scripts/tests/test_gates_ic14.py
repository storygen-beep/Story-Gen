"""IC14: `--selfcheck` flags a hand-written scoreboard count that disagrees with the script."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def skill(tmp_path, text):
    d = tmp_path / "skills" / "author-game-v2"
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text("# skill\n")
    (d / "references" / "x.md").write_text(text)
    return str(d)


def test_a_wrong_scoreboard_count_is_flagged(tmp_path):
    d = skill(tmp_path, "The scoreboard runs 46 gates and 28 lints.\n")
    assert gates._hand_counts(d, 52, 56) == [
        ("references/x.md", 1, "46 gates"), ("references/x.md", 1, "28 lints")]


def test_a_right_count_a_tally_and_a_field_table_are_not(tmp_path):
    d = skill(tmp_path, "gates.py runs 52 gates and 56 lints.\n"
                        "`29/49 gates pass` is the tally line of gates.py.\n"
                        "the field reads 2,235 gates across 27 games\n")
    assert gates._hand_counts(d, 52, 56) == []


def test_a_spelled_out_count_is_read_too(tmp_path):
    d = skill(tmp_path, "`scripts/gates.py` defines fifty-five lints and forty gates.\n"
                        "gates.py prints fifty-six lints.\n")
    assert gates._hand_counts(d, 52, 56) == [
        ("references/x.md", 1, "fifty-five lints"), ("references/x.md", 1, "forty gates")]
