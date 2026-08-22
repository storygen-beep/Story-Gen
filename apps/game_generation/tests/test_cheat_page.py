"""Cheat page ([ui.cheat_page]) — emission, the code gate, and validation.

V2-only and no-DB, deliberately: the closest existing precedent (TipsPageTests in
apps/projects/tests.py) builds with V1, which carries a duplicate tips_page
implementation and its own local-var infoPages. Copying it would test a frozen
generator for a v2-only feature.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_cheat_page.py -q
"""
import copy

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"

# A hint string that appears nowhere else, so "is this row's copy behind its unlock
# flag" is a plain substring check.
HINT = "ZZ_HINT_SENTINEL"

# Codes are WORDS, and long enough that the plaintext-leak assert is meaningful.
CODES = {
    "money": "ALPHAWORD",
    "awareness": "BETAWORD",
    "frank": "GAMMAWORD",
    "energy": "ZETAWORD",
}

# awareness is given bands by _with_bands() below, so it exercises the cap rules.
# money is unbanded, so it exercises the clamp=false unbounded-resource path.
GRANTS = [
    {"id": "money", "label": "Money", "trait": "money", "value": 25,
     "clamp": False, "hint": HINT},
    {"id": "awareness", "label": "Awareness", "trait": "awareness", "value": 5,
     "cap": 40, "at_cap_text": "As far as this goes."},
    {"id": "frank", "label": "Frank", "targetType": "npc", "npcId": "npc_frank",
     "trait": "trust", "value": 10, "cap": 50},
    {"id": "energy", "label": "Energy", "trait": "energy", "op": "set", "value": 100},
]

JOIN_URL = "https://example.test/membership"


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


def _authored(grants=None, bands=True, page_extra=None, version="9.9.9"):
    d = _raw()
    if bands:
        _with_bands(d)
    if version is not None:
        d.setdefault("project", {})["version"] = version
    page = {"title": "The Ledger", "intro": "She keeps her own numbers.",
            "button_label": "Cheat", "button_icon": "🔓",
            "join_note": "Codes come with the guide.", "join_url": JOIN_URL,
            "grants": copy.deepcopy(GRANTS if grants is None else grants)}
    page.update(page_extra or {})
    d.setdefault("ui", {})["cheat_page"] = page
    return d


def _build(d, options=None, codes=None):
    graph = build_game_graph(normalize(d))
    opts = dict(options or {})
    if codes is not None:
        opts["cheat_codes"] = codes
    return TweeComprehensiveGeneratorV2().generate(
        graph.project, opts, graph=graph
    )


def _section(twee, name="CheatPage"):
    """The body of one passage, so a canvas's own macros don't pollute the check."""
    for chunk in twee.split("\n:: "):
        if chunk.startswith(name + "\n") or chunk == name:
            return chunk
    return ""


def _info_pages(twee):
    return twee.split("setup.infoPages = ")[1].split(";")[0]


def _code_table(twee):
    """The emitted {hash: row id} lookup, as a dict."""
    import json
    body = twee.split("setup.cheatCodes = ")[1]
    return json.loads(body[:body.index(";")])


def _errors(d):
    return [e for e in validate(normalize(d)) if "cheat_page" in e or "[builds]" in e]


# ── wiring ───────────────────────────────────────────────────────────────────

def test_importer_carries_the_block_all_the_way_to_metadata():
    """Guards the silent-no-op step: parse the TOML, forget the GameTemplate kwarg,
    and the whole feature vanishes with no error anywhere."""
    template = normalize(_authored())
    assert template.cheat_page is not None
    assert len(template.cheat_page.grants) == 4
    assert [g.id for g in template.cheat_page.grants] == list(CODES)
    graph = build_game_graph(template)
    assert "cheat_page" in graph.project.metadata
    assert graph.project.metadata["cheat_page"]["join_url"] == JOIN_URL


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


# ── the code gate ────────────────────────────────────────────────────────────

def test_every_row_including_its_copy_sits_behind_its_unlock_flag():
    """A padlocked placeholder would tell a player with no code exactly what is on sale
    and how many there are. Nothing is the point — so the guard must wrap the WHOLE
    row, label and hint included, not just the clickable part."""
    section = _section(_build(_authored(), codes=CODES))
    assert section.count('<<if $flags["cheat_') == 4

    # Everything outside an unlock guard is what a player with no code actually sees.
    outside = []
    rest = section
    for row_id in CODES:
        head, _, rest = rest.partition(f'<<if $flags["cheat_{row_id}"]>>')
        outside.append(head)
        _, _, rest = rest.partition("<</if>>\n  ")
    outside.append(rest)
    visible = "".join(outside)

    for token in ("Money", "Awareness", "Frank", "Energy", HINT,
                  "As far as this goes.", "applyAndNotifyTrait"):
        assert token not in visible, f"{token} is readable without a code"

    # What IS visible: the box, the join line, and nothing that names a row.
    assert '<<textbox "_cheatcode" "">>' in visible
    assert "Codes come with the guide." in visible


def test_every_row_is_still_emitted_live():
    """One build ships everywhere: the grants are present, gated at RUNTIME."""
    section = _section(_build(_authored(), codes=CODES))
    assert section.count("setup.applyAndNotifyTrait(") == 4
    assert HINT in section


def test_grant_call_shape_is_exact():
    section = _section(_build(_authored(), codes=CODES))
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


def test_rows_carry_an_at_cap_guard():
    """Evaluated at render — which is why rows navigate to themselves. Without it a
    maxed row stays lit and silently does nothing."""
    section = _section(_build(_authored(), codes=CODES))
    assert 'setup.getTraitValue("player", null, "awareness") lt 40' in section
    assert 'setup.getTraitValue("npc", "npc_frank", "trust") lt 50' in section
    # op="set" guards on inequality instead of a ceiling.
    assert 'setup.getTraitValue("player", null, "energy") isnot 100' in section
    assert "As far as this goes." in section


def test_page_never_costs_time():
    assert "advanceTime" not in _section(_build(_authored(), codes=CODES))


def test_rows_navigate_to_themselves():
    """The at-cap guard is evaluated at RENDER, so only a re-render can grey a row the
    instant it caps. Four row links, plus the Unlock link's goto on a successful code."""
    section = _section(_build(_authored(), codes=CODES))
    assert section.count('" "CheatPage">>') == 4
    assert section.count('<<goto "CheatPage">>') == 1


def test_code_box_and_join_block_are_always_present():
    """For a player with no code this is the ENTIRE page. If the join line goes
    missing they cannot tell what the box is for or where to get one."""
    section = _section(_build(_authored(), codes=CODES))
    assert '<<textbox "_cheatcode" "">>' in section
    assert '<<link "Unlock">>' in section
    assert "Codes come with the guide." in section
    assert JOIN_URL in section


def test_join_url_falls_back_to_project_support_url():
    d = _authored(page_extra={"join_url": ""})
    d.setdefault("project", {})["support_url"] = "https://example.test/fallback"
    assert "https://example.test/fallback" in _section(_build(d, codes=CODES))


def test_failure_message_names_the_build_version():
    """A code for another release simply misses, so the miss copy has to answer both
    cases. Naming the version is what turns a support message into a self-fix."""
    section = _section(_build(_authored(version="9.9.9"), codes=CODES))
    assert "This build is v9.9.9" in section
    assert 'class="build-badge">v9.9.9<' in section


# ── hashing ──────────────────────────────────────────────────────────────────

def test_no_plaintext_code_reaches_the_output():
    twee = _build(_authored(), codes=CODES)
    folded = "".join(twee.split()).upper()
    for word in CODES.values():
        assert word not in folded, word


def test_hash_table_maps_hashes_to_row_ids():
    table = _code_table(_build(_authored(), codes=CODES))
    assert sorted(table.values()) == sorted(CODES)
    gen = TweeComprehensiveGeneratorV2
    for row_id, word in CODES.items():
        assert table[gen.cheat_code_hash("9.9.9", row_id, word)] == row_id


def test_hash_is_salted_by_version_and_row():
    """Two free properties: a code cannot open a row it was not issued for, and last
    release's codes cannot open this release's rows."""
    h = TweeComprehensiveGeneratorV2.cheat_code_hash
    assert h("9.9.9", "money", "ALPHAWORD") != h("9.9.8", "money", "ALPHAWORD")
    assert h("9.9.9", "money", "ALPHAWORD") != h("9.9.9", "energy", "ALPHAWORD")


def test_entry_is_case_and_whitespace_insensitive():
    """It gets retyped off a PDF, on a phone, with autocapitalisation on."""
    h = TweeComprehensiveGeneratorV2.cheat_code_hash
    canonical = h("9.9.9", "money", "ALPHAWORD")
    for typed in ("alphaword", " AlphaWord ", "ALPHA WORD", "\talpha\nword "):
        assert h("9.9.9", "money", typed) == canonical


def test_build_without_codes_still_renders_the_page():
    """--no-codes: the page advertises, nothing opens. A valid state, not a crash."""
    twee = _build(_authored(), codes=None)
    section = _section(twee)
    assert '<<textbox "_cheatcode" "">>' in section
    assert _code_table(twee) == {}


def test_build_is_reproducible():
    d = _authored()
    assert _build(d, codes=CODES) == _build(d, codes=CODES)


# ── the integrity gate ───────────────────────────────────────────────────────

def test_integrity_gate_catches_a_plaintext_code_in_the_output():
    """The likeliest way to leak one is to paste it into a row's hint."""
    grants = copy.deepcopy(GRANTS)
    grants[0]["hint"] = "type ALPHAWORD here"
    with pytest.raises(RuntimeError, match="plaintext code for row 'money'"):
        _build(_authored(grants=grants), codes=CODES)


def test_integrity_gate_ignores_case_and_spacing():
    """A code that survives normalisation is still a working code."""
    grants = copy.deepcopy(GRANTS)
    grants[0]["hint"] = "type alpha word here"
    with pytest.raises(RuntimeError, match="plaintext code"):
        _build(_authored(grants=grants), codes=CODES)


# ── games without the feature ────────────────────────────────────────────────

def test_game_without_the_feature_carries_no_cheat_page_and_no_cheat_css():
    """The regression guard for every pre-existing game: this feature must not add a
    byte to a game that does not author it."""
    twee = _build(_raw())
    assert ":: CheatPage" not in twee
    assert "setup.cheatCodes" not in twee
    assert ".cheat-row" not in twee
    assert 'class="build-badge">' not in twee


def test_codes_option_is_inert_without_a_cheat_page():
    assert _build(_raw(), codes=CODES) == _build(_raw())


# ── validation ───────────────────────────────────────────────────────────────

def test_valid_block_produces_no_errors():
    assert _errors(_authored()) == []


def test_banded_trait_requires_a_cap():
    d = _authored(grants=[{"id": "r", "label": "Awareness", "trait": "awareness", "value": 5}])
    assert any("declares no 'cap'" in e for e in _errors(d))


def test_cap_above_the_top_band_is_rejected():
    d = _authored(grants=[{"id": "r", "label": "A", "trait": "awareness", "value": 5, "cap": 90}])
    assert any("exceeds the top band max" in e for e in _errors(d))


def test_set_above_the_top_band_is_rejected():
    d = _authored(grants=[
        {"id": "r", "label": "A", "trait": "awareness", "op": "set", "value": 90, "cap": 40}
    ])
    assert any("above its top band max" in e for e in _errors(d))


def test_clamp_false_on_a_banded_trait_is_rejected():
    d = _authored(grants=[
        {"id": "r", "label": "A", "trait": "awareness", "value": 5, "cap": 40, "clamp": False}
    ])
    assert any("clamp = false is not allowed" in e for e in _errors(d))


def test_cap_over_100_with_clamp_on_is_rejected():
    """The engine clamps to 0-100 before applying the cap, so the cap is unreachable."""
    d = _authored(grants=[{"id": "r", "label": "M", "trait": "money", "value": 25, "cap": 500}])
    assert any("cap is unreachable" in e for e in _errors(d))


def test_stage_trait_cannot_be_granted():
    d = _authored(grants=[{"id": "r", "label": "Stage", "trait": "npc_frank_stage", "value": 1}])
    assert any("stage/arc counter" in e for e in _errors(d))


def test_causal_fields_are_rejected():
    for field, value in (("flag", "some_flag"), ("questEffects", [{"a": 1}]),
                         ("itemEffects", [{"item_id": "x"}]), ("nodeId", "n")):
        d = _authored(grants=[
            {"id": "r", "label": "M", "trait": "money", "value": 5, "clamp": False, field: value}
        ])
        assert any("not allowed on a cheat-page row" in e for e in _errors(d)), field


def test_undeclared_trait_is_rejected():
    d = _authored(grants=[{"id": "r", "label": "X", "trait": "not_a_real_trait", "value": 5}])
    assert any("not found in [player.core_traits]" in e for e in _errors(d))


def test_unknown_npc_is_rejected():
    d = _authored(grants=[
        {"id": "r", "label": "X", "targetType": "npc", "npcId": "npc_nobody",
         "trait": "trust", "value": 5}
    ])
    assert any("not found in NPC definitions" in e for e in _errors(d))


def test_missing_label_and_bad_op_are_rejected():
    d = _authored(grants=[{"id": "r", "label": "", "trait": "money", "value": 5, "clamp": False}])
    assert any("'label' is required" in e for e in _errors(d))
    d = _authored(grants=[
        {"id": "r", "label": "M", "trait": "money", "op": "mul", "value": 5, "clamp": False}
    ])
    assert any("must be 'add' or 'set'" in e for e in _errors(d))


def test_duplicate_rows_are_rejected():
    d = _authored(grants=[
        {"id": "r", "label": "A", "trait": "money", "value": 5, "clamp": False},
        {"id": "r", "label": "B", "trait": "money", "value": 9, "clamp": False},
    ])
    assert any("duplicate cheat row" in e for e in _errors(d))


def test_page_with_no_rows_is_rejected():
    assert any("declares no [[ui.cheat_page.grants]]" in e for e in _errors(_authored(grants=[])))


def test_missing_join_note_is_rejected():
    """Without it a player with no code sees a bare box and no way to read it."""
    d = _authored(page_extra={"join_note": ""})
    assert any("'join_note' is missing" in e for e in _errors(d))


def test_join_url_without_a_scheme_is_rejected():
    """It lands in an href in a published file; scheme-less makes it a relative link."""
    d = _authored(page_extra={"join_url": "patreon.com/x"})
    assert any("must start with http" in e for e in _errors(d))


def test_row_id_is_required_unique_and_slug_shaped():
    d = _authored(grants=[{"label": "M", "trait": "money", "value": 5, "clamp": False}])
    assert any("'id' is required" in e for e in _errors(d))

    d = _authored(grants=[
        {"id": "Money Row", "label": "M", "trait": "money", "value": 5, "clamp": False}
    ])
    assert any("lowercase letters, digits and underscores" in e for e in _errors(d))

    d = _authored(grants=[
        {"id": "dup", "label": "M", "trait": "money", "value": 5, "clamp": False},
        {"id": "dup", "label": "E", "trait": "energy", "op": "set", "value": 100},
    ])
    assert any("duplicate id 'dup'" in e for e in _errors(d))


def test_a_toml_side_unlock_selector_is_rejected():
    """Rows unlock at runtime from the player's code. A committed selector would open
    every row for everyone, in a file that ships publicly."""
    for key in ("enabled", "cheat_grants", "paid", "unlocked"):
        d = _authored(page_extra={key: True})
        assert any("unlock at runtime" in e for e in _errors(d)), key


def test_codes_in_the_committed_toml_are_rejected():
    """This file is public. A code written here is a published code."""
    d = _authored(page_extra={"code": "ALPHAWORD"})
    assert any("untracked codes file" in e for e in _errors(d))

    grants = copy.deepcopy(GRANTS)
    grants[0]["code"] = "ALPHAWORD"
    assert any("untracked codes file" in e for e in _errors(_authored(grants=grants)))


def test_a_leftover_builds_block_is_rejected():
    """The free/paid split is gone. A stale block tells its author instead of quietly
    losing the footer badge it used to drive."""
    d = _authored()
    d["builds"] = {"free": {"id": "r", "label": "Free Build"}, "paid": {"id": "r", "label": "Paid"}}
    assert any("no longer supported" in e for e in _errors(d))


def test_cheat_page_requires_time_enabled():
    d = _authored()
    d.setdefault("time", {})["enabled"] = False
    assert any("requires [time] enabled" in e for e in _errors(d))
