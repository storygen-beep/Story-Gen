"""Cheat page ([ui.cheat_page]) — emission, the free/paid split, and validation.

V2-only and no-DB, deliberately: the closest existing precedent (TipsPageTests in
apps/projects/tests.py) builds with V1, which carries a duplicate tips_page
implementation and its own local-var infoPages. Copying it would test a frozen
generator for a v2-only feature.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_cheat_page.py -q
"""
import copy
import re

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"

# A hint string that appears nowhere else, so "did paid-only copy leak into the free
# build" is a plain substring check over the whole output.
HINT = "ZZ_PAID_ONLY_HINT_SENTINEL"

BUILDS = {"free": {"label": "Free Build"}, "paid": {"label": "🎯 Beta Nut Build"}}

# awareness is given bands by _with_bands() below, so it exercises the cap rules.
# money is unbanded, so it exercises the clamp=false unbounded-resource path.
GRANTS = [
    {"label": "Money", "trait": "money", "value": 25, "clamp": False, "hint": HINT},
    {"label": "Awareness", "trait": "awareness", "value": 5, "cap": 40,
     "at_cap_text": "As far as this goes."},
    {"label": "Frank", "targetType": "npc", "npcId": "npc_frank", "trait": "trust",
     "value": 10, "cap": 50},
    {"label": "Energy", "trait": "energy", "op": "set", "value": 100},
]


def _raw():
    return parse_toml(FIXTURE)


def _with_bands(d):
    """Give `awareness` a banded sidebar item — that is what makes a cap mandatory."""
    d.setdefault("sidebar_items", []).append({
        "type": "trait_status_text",
        "trait": "awareness",
        "bands": [
            {"min": 0, "max": 19, "text": "Unaware"},
            {"min": 20, "max": 40, "text": "Suspicious"},
        ],
    })
    return d


def _authored(grants=None, builds=True, bands=True, page_extra=None):
    d = _raw()
    if bands:
        _with_bands(d)
    page = {"title": "The Ledger", "intro": "She keeps her own numbers.",
            "button_label": "Cheat", "button_icon": "🔓",
            "locked_note": "Supporters unlock these.",
            "grants": copy.deepcopy(GRANTS if grants is None else grants)}
    page.update(page_extra or {})
    d.setdefault("ui", {})["cheat_page"] = page
    if builds:
        d["builds"] = copy.deepcopy(BUILDS)
    return d


def _build(d, options=None):
    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(
        graph.project, dict(options or {}), graph=graph
    )


def _section(twee, name="CheatPage"):
    """The body of one passage, so a canvas's own macros don't pollute the check."""
    for chunk in twee.split("\n:: "):
        if chunk.startswith(name + "\n") or chunk == name:
            return chunk
    return ""


def _info_pages(twee):
    return twee.split("setup.infoPages = ")[1].split(";")[0]


def _errors(d):
    return [e for e in validate(normalize(d)) if "cheat_page" in e or "[builds]" in e]


# ── wiring ───────────────────────────────────────────────────────────────────

def test_importer_carries_the_block_all_the_way_to_metadata():
    """Guards the silent-no-op step: parse the TOML, forget the GameTemplate kwarg,
    and the whole feature vanishes with no error anywhere."""
    template = normalize(_authored())
    assert template.cheat_page is not None
    assert len(template.cheat_page.grants) == 4
    assert template.build_labels.paid == "🎯 Beta Nut Build"
    graph = build_game_graph(template)
    assert "cheat_page" in graph.project.metadata
    assert graph.project.metadata["build_labels"]["free"] == "Free Build"


def test_page_is_registered_in_info_pages():
    """Without this setup.commitMoment refuses to publish a moment on the page and
    every grant is lost on save/refresh."""
    assert '"CheatPage"' in _info_pages(_build(_authored()))


def test_no_cheat_page_means_no_registration_but_widget_still_defined():
    twee = _build(_raw())
    assert '"CheatPage"' not in _info_pages(twee)
    assert ":: CheatPage" not in twee
    # StoryCaption calls the widget unconditionally; SugarCube throws on a ghost.
    assert '<<widget "cheatButton">><</widget>>' in twee


def test_sidebar_button_is_wired_and_labelled():
    twee = _build(_authored())
    assert "<<cheatButton>>" in twee
    assert '<div id="cheat-btn-widget">' in twee
    assert '<<link "Cheat" "CheatPage">>' in twee
    assert "#cheat-btn-widget" in twee  # CSS pill styling, not just the markup


# ── the free/paid split ──────────────────────────────────────────────────────

def test_free_build_has_labels_and_padlocks_only():
    twee = _build(_authored())
    section = _section(twee)
    assert section.count("cheat-row is-locked") == 4
    assert "🔒" in section
    assert "Supporters unlock these." in section


def test_free_build_contains_nothing_executable():
    twee = _build(_authored())
    section = _section(twee)
    for token in ("setup.applyAndNotifyTrait", "<<script>>", "advanceTime", "cheat-hint"):
        assert token not in section, f"free build leaked {token}"


def test_free_build_does_not_leak_paid_only_copy():
    """The hint is the walkthrough. A free player must not learn a threshold from it."""
    assert HINT not in _build(_authored())


def test_paid_build_emits_one_grant_per_row():
    section = _section(_build(_authored(), {"build": "paid"}))
    assert section.count("setup.applyAndNotifyTrait(") == 4
    assert HINT in section


def test_paid_grant_call_shape_is_exact():
    section = _section(_build(_authored(), {"build": "paid"}))
    # Unbounded resource: clamp false, no cap, no guard.
    assert (
        'setup.applyAndNotifyTrait("player", null, "money", "add", 25, false, null)'
        in section
    )
    # Banded player trait: clamp true + cap.
    assert (
        'setup.applyAndNotifyTrait("player", null, "awareness", "add", 5, true, 40)'
        in section
    )
    # NPC trait routes through the npc target with its slug.
    assert (
        'setup.applyAndNotifyTrait("npc", "npc_frank", "trust", "add", 10, true, 50)'
        in section
    )


def test_paid_rows_carry_an_at_cap_guard():
    """Evaluated at render — which is why rows navigate to themselves. Without it a
    maxed row stays lit and silently does nothing."""
    section = _section(_build(_authored(), {"build": "paid"}))
    assert 'setup.getTraitValue("player", null, "awareness") lt 40' in section
    assert 'setup.getTraitValue("npc", "npc_frank", "trust") lt 50' in section
    # op="set" guards on inequality instead of a ceiling.
    assert 'setup.getTraitValue("player", null, "energy") isnot 100' in section
    assert "As far as this goes." in section


def test_page_never_costs_time_in_either_variant():
    for opts in ({}, {"build": "paid"}):
        assert "advanceTime" not in _section(_build(_authored(), opts))


def test_rows_navigate_to_themselves():
    section = _section(_build(_authored(), {"build": "paid"}))
    assert section.count('"CheatPage">>') == 4


# ── the build badge ──────────────────────────────────────────────────────────

def test_badge_names_the_variant():
    assert 'class="build-badge">Free Build<' in _build(_authored())
    assert 'class="build-badge">🎯 Beta Nut Build<' in _build(_authored(), {"build": "paid"})


def test_unknown_build_value_falls_back_to_free():
    """Defence in depth behind argparse choices: only the exact string "paid" opts in."""
    assert 'class="build-badge">Free Build<' in _build(_authored(), {"build": "bogus"})


def test_game_without_the_feature_is_byte_identical_across_variants():
    """The regression guard for every pre-existing game: --build must not perturb a
    game that authors no cheat page."""
    assert _build(_raw(), {}) == _build(_raw(), {"build": "paid"})
    # No badge MARKUP. (The `.build-badge` CSS rule ships unconditionally in the
    # stylesheet, so assert on the emitted span, not on the bare class name.)
    assert 'class="build-badge">' not in _build(_raw(), {})


def test_paid_build_is_reproducible():
    d = _authored()
    assert _build(d, {"build": "paid"}) == _build(d, {"build": "paid"})


# ── the integrity gate ───────────────────────────────────────────────────────

def _sabotage(d, options, hook):
    graph = build_game_graph(normalize(d))
    gen = TweeComprehensiveGeneratorV2()
    hook(gen)
    return gen.generate(graph.project, dict(options), graph=graph)


def test_integrity_gate_catches_a_free_build_emitting_live_rows():
    def emit_paid_rows_in_a_free_build(gen):
        original = gen._cheat_row_markup
        gen._cheat_row_markup = lambda g, is_paid: original(g, True)

    with pytest.raises(RuntimeError, match="FREE build contains"):
        _sabotage(_authored(), {}, emit_paid_rows_in_a_free_build)


def test_integrity_gate_catches_a_paid_build_with_a_dead_row():
    def drop_the_first_grant(gen):
        original = gen._cheat_row_markup
        seen = {"n": 0}

        def hook(g, is_paid):
            seen["n"] += 1
            return original(g, False) if seen["n"] == 1 else original(g, is_paid)

        gen._cheat_row_markup = hook

    with pytest.raises(RuntimeError, match="grant call"):
        _sabotage(_authored(), {"build": "paid"}, drop_the_first_grant)


# ── validation ───────────────────────────────────────────────────────────────

def test_valid_block_produces_no_errors():
    assert _errors(_authored()) == []


def test_banded_trait_requires_a_cap():
    d = _authored(grants=[{"label": "Awareness", "trait": "awareness", "value": 5}])
    assert any("declares no 'cap'" in e for e in _errors(d))


def test_cap_above_the_top_band_is_rejected():
    d = _authored(grants=[{"label": "A", "trait": "awareness", "value": 5, "cap": 90}])
    assert any("exceeds the top band max" in e for e in _errors(d))


def test_set_above_the_top_band_is_rejected():
    d = _authored(grants=[
        {"label": "A", "trait": "awareness", "op": "set", "value": 90, "cap": 40}
    ])
    assert any("above its top band max" in e for e in _errors(d))


def test_clamp_false_on_a_banded_trait_is_rejected():
    d = _authored(grants=[
        {"label": "A", "trait": "awareness", "value": 5, "cap": 40, "clamp": False}
    ])
    assert any("clamp = false is not allowed" in e for e in _errors(d))


def test_cap_over_100_with_clamp_on_is_rejected():
    """The engine clamps to 0-100 before applying the cap, so the cap is unreachable."""
    d = _authored(grants=[{"label": "M", "trait": "money", "value": 25, "cap": 500}])
    assert any("cap is unreachable" in e for e in _errors(d))


def test_stage_trait_cannot_be_granted():
    d = _authored(grants=[{"label": "Stage", "trait": "npc_frank_stage", "value": 1}])
    assert any("stage/arc counter" in e for e in _errors(d))


def test_causal_fields_are_rejected():
    for field, value in (("flag", "some_flag"), ("questEffects", [{"a": 1}]),
                         ("itemEffects", [{"item_id": "x"}]), ("nodeId", "n")):
        d = _authored(grants=[
            {"label": "M", "trait": "money", "value": 5, "clamp": False, field: value}
        ])
        assert any("not allowed on a cheat-page row" in e for e in _errors(d)), field


def test_undeclared_trait_is_rejected():
    d = _authored(grants=[{"label": "X", "trait": "not_a_real_trait", "value": 5}])
    assert any("not found in [player.core_traits]" in e for e in _errors(d))


def test_unknown_npc_is_rejected():
    d = _authored(grants=[
        {"label": "X", "targetType": "npc", "npcId": "npc_nobody",
         "trait": "trust", "value": 5}
    ])
    assert any("not found in NPC definitions" in e for e in _errors(d))


def test_missing_label_and_bad_op_are_rejected():
    d = _authored(grants=[{"label": "", "trait": "money", "value": 5, "clamp": False}])
    assert any("'label' is required" in e for e in _errors(d))
    d = _authored(grants=[
        {"label": "M", "trait": "money", "op": "mul", "value": 5, "clamp": False}
    ])
    assert any("must be 'add' or 'set'" in e for e in _errors(d))


def test_duplicate_rows_are_rejected():
    d = _authored(grants=[
        {"label": "A", "trait": "money", "value": 5, "clamp": False},
        {"label": "B", "trait": "money", "value": 9, "clamp": False},
    ])
    assert any("duplicate cheat row" in e for e in _errors(d))


def test_page_with_no_rows_is_rejected():
    assert any("declares no [[ui.cheat_page.grants]]" in e for e in _errors(_authored(grants=[])))


def test_missing_build_labels_are_rejected():
    assert any("[builds.free].label" in e for e in _errors(_authored(builds=False)))


def test_a_toml_side_variant_selector_is_rejected():
    """Two builds come from one commit, so a committed selector is necessarily false
    for one of them. The variant is a CLI argument."""
    for key in ("enabled", "cheat_grants", "paid"):
        d = _authored(page_extra={key: True})
        assert any("chosen at build time" in e for e in _errors(d)), key
    d = _authored()
    d["builds"]["variant"] = "paid"
    assert any("must not declare which variant is active" in e for e in _errors(d))


def test_cheat_page_requires_time_enabled():
    d = _authored()
    d.setdefault("time", {})["enabled"] = False
    assert any("requires [time] enabled" in e for e in _errors(d))
