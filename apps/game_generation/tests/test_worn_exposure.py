"""The engine could not tell a naked player from a dressed one.

Measured 2026-08-28: `setup.getWornStatMax` — which backs both `worn_beauty` and
`worn_corruption` — SKIPS a slot with nothing in it (`if (!id) continue;`) and starts at
zero. So a player wearing nothing returned 0, and a player in a plain bra and cotton
briefs (both declared 0/0 in `late_shifts`) also returned 0. Every condition in every game
this project has shipped was blind to nakedness, and across ten games with a wardrobe
exactly ONE choice was ever gated on clothing at all.

The field builds its clothing games on precisely the value we could not compute.
`degrees-of-lewdity`'s `$exposed` is the most-read variable in that game — 654 tests of
`gte 1` and 307 of `gte 2`, against 54 reads of any per-slot `.exposed` — and 71% of its
407 world gates ask how much skin is showing, in streets, an arcade, a canteen and a park.

So: `exposure` on a garment, `setup.getWornExposure()` deriving 0/1/2, and a
`worn_exposure` predicate. These tests pin the one property that makes it worth having —
that an EMPTY slot is louder than a modest garment — plus the three-evaluator seam this
engine has bitten us on before.

    pytest apps/game_generation/tests/test_worn_exposure.py -q
"""
from pathlib import Path

import pytest

from apps.projects.services.template_import import TemplateClothingItem

V2 = Path("apps/game_generation/twee_comprehensive/generators/v2.py").read_text(
    encoding="utf-8"
)


# --- the schema carries it ------------------------------------------------------


def test_garment_declares_exposure_and_defaults_to_covered():
    assert TemplateClothingItem(id="x", name="X", slot="top").exposure == 0
    assert TemplateClothingItem(id="x", name="X", slot="top", exposure=2).exposure == 2


def test_exposure_is_parsed_and_serialized():
    src = Path("apps/projects/services/template_import.py").read_text(encoding="utf-8")
    assert 'exposure=_require_int(c_raw, "exposure", 0)' in src, "not parsed from TOML"
    assert '"exposure": ci.exposure' in src, "not serialized into setup.clothing_data"


# --- the aggregate reads EMPTY slots, which is the whole point -------------------


def test_aggregate_exists_and_reads_empty_slots():
    fn = V2.split("setup.getWornExposure = function()")[1][:2200]
    # the two core regions, each asking whether the slot is FILLED rather than skipping it
    assert "filled('top')" in fn and "filled('bottom')" in fn
    assert "filled('bra')" in fn and "filled('underwear')" in fn
    assert "filled('dress')" in fn or "dress" in fn
    # bare beats underwear-level
    assert "? 1 : 2" in fn, "an empty core slot must read 2 unless underwear covers it"


def test_the_old_aggregate_still_skips_empty_slots():
    """getWornStatMax is deliberately NOT changed — worn_beauty and worn_corruption keep
    their meaning, and a game that reads them is unaffected by this feature."""
    fn = V2.split("setup.getWornStatMax = function(field)")[1][:900]
    assert "if (!id) continue;" in fn


def test_a_worn_garment_can_still_declare_exposure():
    """A mesh top fills the slot and does not cover her, so a filled slot is not the end
    of the question — the aggregate takes the max of regions and declared values."""
    fn = V2.split("setup.getWornExposure = function()")[1][:2200]
    assert "cdata[i].exposure" in fn


# --- the three-evaluator seam ---------------------------------------------------


def test_predicate_reaches_the_evaluator():
    ev = V2.split("setup.triggerConditionsSatisfied = function(conditions)")[1][:14000]
    assert "type === 'worn_exposure'" in ev


def test_predicate_reaches_the_requirement_text():
    """A choice locked on exposure must be able to say why — `a locked door says why`."""
    fm = V2.split("setup.formatCanvasConditions = function(conditions)")[1][:12000]
    assert 'item.type === "worn_exposure"' in fm


def test_predicate_is_guarded_on_clothing_enabled():
    """Every worn_* predicate short-circuits before touching an aggregate that only exists
    in clothing-enabled builds. Regression guard on a documented trap."""
    ev = V2.split("type === 'worn_exposure'")[1][:400]
    assert "clothing_enabled" in ev


@pytest.mark.parametrize("other", ["describeUnmetConditions", "_renderGoalGate"])
def test_known_gap_is_unchanged_and_equal_for_every_worn_predicate(other):
    """⚠️ NOT a bug this feature introduced. These two display helpers handle no `worn_*`
    predicate at all — not corruption, not beauty, not type, not exposure. Pinned so the
    day someone teaches them one, they teach them all four."""
    body = V2.split(f"setup.{other} = function")[1][:9000]
    assert "worn_corruption" not in body
    assert "worn_exposure" not in body
