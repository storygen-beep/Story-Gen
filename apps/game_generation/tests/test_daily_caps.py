"""[engine.daily_caps] (first_term exhibition phase 1, LO 2026-11-08): parsed, and emitted for the runtime."""
import pytest

from apps.projects.services.template_import import _parse_daily_caps


def test_bands_are_parsed_and_sorted():
    out = _parse_daily_caps({"exhibitionism": {"bands": [{"below": 40, "cap": 2}, {"below": 20, "cap": 3}],
                                               "hold_band_while": ["drinks_boost"], "first_gain_message": "Hi"}})
    assert out["exhibitionism"]["bands"] == [{"below": 20.0, "cap": 3.0}, {"below": 40.0, "cap": 2.0}]
    assert out["exhibitionism"]["hold_band_while"] == ["drinks_boost"]


def test_an_unknown_key_is_refused():
    with pytest.raises(ValueError):
        _parse_daily_caps({"exhibitionism": {"bands": [], "capp": 3}})


def test_a_bad_band_is_refused():
    with pytest.raises(ValueError):
        _parse_daily_caps({"exhibitionism": {"bands": [{"below": 20}]}})


def test_nothing_declared_is_none():
    assert _parse_daily_caps(None) is None


def test_the_runtime_reads_the_cap(tmp_path):
    from pathlib import Path
    built = Path(__file__).resolve().parents[3] / "games" / "first_term" / "output" / "index.html"
    if not built.exists():
        pytest.skip("first_term not built")
    text = built.read_text(encoding="utf-8")
    assert "setup.dailyCapAllow = function" in text and '"exhibitionism": {"bands"' in text
