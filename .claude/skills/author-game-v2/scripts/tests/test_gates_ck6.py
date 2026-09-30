"""CK6 (PRD v2, 2026-09-30): `--beat` shows the joints.

Each beat, and ALL BEATS, print `but` and `and` per 1,000 words against FIELD_BUT_P10 and
FIELD_AND_MAX — printed, never judged — with "too short to judge" under JOINTS_MIN_WORDS.
The prose is written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def words(n, but=0, and_=0):
    """n words: `but` x but, `and` x and_, the rest filler."""
    return " ".join(["but"] * but + ["and"] * and_ + ["word"] * (n - but - and_)) + "."


def run(tmp_path, capsys, text):
    p = tmp_path / "beat.txt"
    p.write_text(text)
    rc = gates.beat_mode(str(p))
    return rc, [l for l in capsys.readouterr().out.splitlines() if "joints" in l]


def test_a_short_beat_prints_its_rates_and_the_note(tmp_path, capsys):
    rc, lines = run(tmp_path, capsys, words(100, but=1, and_=3))
    assert rc == 0 and len(lines) == 1
    assert "but 10.00/1k (field p10 2.88)" in lines[0]
    assert "and 30.0/1k (field max 41.11)" in lines[0]
    assert "too short to judge (under 500 words" in lines[0]


def test_a_long_beat_prints_no_note(tmp_path, capsys):
    rc, lines = run(tmp_path, capsys, words(600, but=3, and_=12))
    assert rc == 0
    assert "but 5.00/1k" in lines[0] and "and 20.0/1k" in lines[0]
    assert "too short" not in lines[0]


def test_all_beats_carries_the_joints_over_the_whole_text(tmp_path, capsys):
    rc, lines = run(tmp_path, capsys, words(300, but=3) + "\n\n" + words(300, and_=6))
    assert rc == 0 and len(lines) == 3                 # beat 1, beat 2, all beats
    assert "but 5.00/1k" in lines[2] and "and 10.0/1k" in lines[2]
    assert "too short" not in lines[2]
