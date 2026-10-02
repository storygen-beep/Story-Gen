"""RUNGS inflections (2026-10-01): the act-rung readout sees inflected stems.

The Billable Hours test found `--beat`'s act-rung readout blind to "gropes", "fondles" and
"nuzzles": the stems sat before a word boundary, so only the bare stem matched. Every stem
now takes its inflections. Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


@pytest.mark.parametrize("text, rung", [
    ("He gropes her.", "touch"), ("He was groping her.", "touch"), ("He fondles her.", "touch"),
    ("He nuzzles her neck.", "touch"), ("She caresses him.", "touch"),
    ("She undresses.", "strip"), ("He unbuttons her blouse.", "strip"),
    ("He unzips her dress.", "strip"), ("He thrusts.", "vaginal"), ("He keeps thrusting.", "vaginal"),
])
def test_an_inflected_stem_finds_its_rung(text, rung):
    first, present = gates._rungs_of(text)
    assert first == rung and present == {rung}
