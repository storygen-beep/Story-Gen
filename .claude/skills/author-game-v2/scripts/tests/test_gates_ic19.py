"""IC19: `--selfcheck` prints the running word total on every run (LO, 2026-09-28)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def test_selfcheck_prints_the_running_total(capsys):
    gates.selfcheck_mode()
    out = capsys.readouterr().out
    line = next(l for l in out.splitlines() if "running total" in l)
    assert f"/ {gates.WORD_REFERENCE:,} words" in line
