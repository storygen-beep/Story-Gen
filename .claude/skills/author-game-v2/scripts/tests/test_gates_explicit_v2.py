"""EXPLICIT list version 2 (2026-10-02): the inflections the frozen list missed.

"groping" failed because the stem was `grope`; "titties" and "asses" failed on a trailing `\\b`.
Version 2 adds `grop`, `tit(?:s|ty|ties)?` and `ass(?:es)?`. Everything version 1 counted it
still counts, and "come" stays out. Fixtures are written here; nothing in games/ is read.
"""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


@pytest.mark.parametrize("word", ["groping", "gropes", "grope", "titties", "titty", "tits", "tit",
                                  "asses", "ass"])
def test_version_2_counts_the_inflected_form(word):
    assert len(gates.EXPLICIT.findall(f"He keeps {word} there.")) == 1


@pytest.mark.parametrize("word", ["title", "assume", "assistant", "come"])
def test_version_2_does_not_widen_to_other_words(word):
    assert gates.EXPLICIT.findall(f"A {word} here.") == []
