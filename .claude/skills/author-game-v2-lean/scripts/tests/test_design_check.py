"""design_check.py: dated goals, minors, phase order."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import design_check as dc  # noqa: E402


def test_dated_goal_patterns():
    for bad in ("by day 60", "within 98 days", "by the end of her second year", "week twelve", "a deadline"):
        assert dc.DATED.search(bad), bad
    for ok in ("save enough to move out", "make partner at the agency", "pay Marco back"):
        assert not dc.DATED.search(ok), ok


def test_minor_ages_and_section():
    md = "## 3. What she wants\nTo leave.\n\n## 5. The people and her life\nSam, a 16-year-old.\n"
    assert dc.MINOR_AGE.search(dc.section(md, 5))
    assert not dc.MINOR_AGE.search(dc.section(md, 3))


def test_phase_order():
    assert dc.at_least("idea", "want") and not dc.at_least("want", "idea") and not dc.at_least(None, "want")


def test_blank_signature_line_is_not_a_signature():
    assert not dc.SIGNED.search("> [REVIEW] · drafted 2026-10-04 · signed by LO: —")
    assert dc.SIGNED.search("> [READY] · drafted 2026-10-03 · signed by LO: LO, 2026-10-03")
