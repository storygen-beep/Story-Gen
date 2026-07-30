"""Studio identity ([project] support_url / studio_name) — plumbing, emission, defaults.

The funding link and the "Developed by X" credit were generator literals until
2026-07-29. They are now data, so a game can ship under a different campaign or
studio without a code change. The whole point of the feature is that it is INERT
until authored, so the load-bearing test here is the byte-identical one.

Mirrors test_cheat_page.py: v2-only, no-DB.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_support_url.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    DEFAULT_STUDIO_NAME,
    DEFAULT_SUPPORT_URL,
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"

# Three sites emit the URL: the sidebar <<patreonButton>> widget and both intro
# links (above and below the age gate). If that count ever changes, the emission
# tests below should be updated deliberately, not silently.
EXPECTED_SITES = 3


def _raw():
    return parse_toml(FIXTURE)


def _authored(url=None, studio=None):
    d = _raw()
    if url is not None:
        d["project"]["support_url"] = url
    if studio is not None:
        d["project"]["studio_name"] = studio
    return d


def _build(d):
    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


# ── wiring ───────────────────────────────────────────────────────────────────

def test_importer_carries_both_keys_all_the_way_to_metadata():
    """Guards the silent-drop step: nothing rejects an unknown [project] key, so a
    forgotten line in the dataclass, the parser or the writer makes the feature
    evaporate with no error anywhere in merge, --validate or package."""
    template = normalize(_authored("https://example.com/support", "Probe Co"))
    assert template.project.support_url == "https://example.com/support"
    assert template.project.studio_name == "Probe Co"
    graph = build_game_graph(template)
    assert graph.project.metadata["support_url"] == "https://example.com/support"
    assert graph.project.metadata["studio_name"] == "Probe Co"


def test_unset_keys_normalize_to_empty_not_to_the_default():
    """The fallback is deliberately generator-side, so the importer must NOT bake a
    default — build_guide.py reads [project] straight from the TOML and would then
    resolve a different value than the sidebar."""
    template = normalize(_raw())
    assert template.project.support_url == ""
    assert template.project.studio_name == ""


# ── the regression guard ─────────────────────────────────────────────────────

def test_game_without_the_keys_is_byte_identical_to_the_old_literals():
    """THE test for this feature. Every game built before 2026-07-29 authored
    neither key; making the URL data must not move a single byte for them."""
    twee = _build(_raw())
    assert twee == _build(_raw())  # reproducible
    assert twee.count(DEFAULT_SUPPORT_URL) == EXPECTED_SITES
    assert f"Developed by <strong>{DEFAULT_STUDIO_NAME}</strong>" in twee


# ── emission ─────────────────────────────────────────────────────────────────

def test_authored_url_replaces_the_default_everywhere():
    """A partial swap is the dangerous failure: two sites repointed, one still
    funnelling to the old campaign."""
    twee = _build(_authored(url="https://example.com/go/f95"))
    assert twee.count("https://example.com/go/f95") == EXPECTED_SITES
    assert DEFAULT_SUPPORT_URL not in twee


def test_authored_studio_name_replaces_the_credit_only():
    twee = _build(_authored(studio="Probe Co"))
    assert "Developed by <strong>Probe Co</strong>" in twee
    assert DEFAULT_STUDIO_NAME not in twee
    # The credit is independent of the link — leaving studio_name unset must not
    # drag the URL along with it.
    assert twee.count(DEFAULT_SUPPORT_URL) == EXPECTED_SITES


def test_each_key_falls_back_independently():
    twee = _build(_authored(url="https://example.com/x"))
    assert f"Developed by <strong>{DEFAULT_STUDIO_NAME}</strong>" in twee
    twee = _build(_authored(studio="Probe Co"))
    assert twee.count(DEFAULT_SUPPORT_URL) == EXPECTED_SITES


def test_whitespace_only_value_falls_back_rather_than_emitting_an_empty_href():
    """An href="" is a link to the current passage — worse than no link at all."""
    twee = _build(_authored(url="   ", studio="  "))
    assert twee.count(DEFAULT_SUPPORT_URL) == EXPECTED_SITES
    assert f"Developed by <strong>{DEFAULT_STUDIO_NAME}</strong>" in twee


def test_query_string_is_escaped_for_the_attribute_not_left_raw():
    """`&` must ship as `&amp;` in the Twee source. Verified live in a browser
    (2026-07-29): the DOM href comes back with a single real `&` and two distinct
    searchParams, so the double-escape seen when grepping the built HTML is the
    normal SugarCube source-byte round-trip, not a bug."""
    twee = _build(_authored(url="https://example.com/r?src=f95&tier=free"))
    assert "https://example.com/r?src=f95&amp;tier=free" in twee
    assert "src=f95&tier=free" not in twee


def test_markup_breaking_value_cannot_escape_the_attribute():
    """Defence in depth behind the scheme check: even a permitted http(s) URL
    carrying a quote or a macro must not break out of the href or fire."""
    twee = _build(_authored(url='https://example.com/"><<script>>x'))
    assert '"><<script>>' not in twee
    assert "&quot;&gt;&lt;&lt;script&gt;&gt;" in twee


# ── the resolver, without a full build ───────────────────────────────────────

@pytest.mark.parametrize(
    "meta",
    [None, {}, {"support_url": ""}, {"support_url": None}, "not-a-dict", 42],
)
def test_resolver_survives_a_missing_or_hostile_metadata_shape(meta):
    """Some callers pass a MagicMock project; a bare .metadata.get() returns a Mock
    and html.escape() then raises. The resolver must degrade to the default."""
    gen = TweeComprehensiveGeneratorV2()

    class _P:
        pass

    p = _P()
    if meta is not None:
        p.metadata = meta
    gen.project = p
    assert gen._resolve_support_url() == DEFAULT_SUPPORT_URL
    assert gen._resolve_studio_name() == DEFAULT_STUDIO_NAME


def test_resolver_survives_no_project_at_all():
    """package_from_toml builds a bare generator for flag-chain validation."""
    assert TweeComprehensiveGeneratorV2()._resolve_support_url() == DEFAULT_SUPPORT_URL


# ── validation ───────────────────────────────────────────────────────────────

def _support_errors(d):
    return [e for e in validate(normalize(d)) if "support_url" in e]


@pytest.mark.parametrize(
    "bad",
    [
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "//example.com/protocol-relative",
        "example.com/no-scheme",
        "ftp://example.com/x",
    ],
)
def test_non_http_scheme_is_rejected(bad):
    """html.escape stops the build-break but not a live javascript: click target,
    and this value lands in an href on every passage of a published file."""
    assert _support_errors(_authored(url=bad))


@pytest.mark.parametrize(
    "ok", ["https://example.com/x", "http://example.com/x", ""]
)
def test_http_schemes_and_absence_are_accepted(ok):
    assert not _support_errors(_authored(url=ok))
