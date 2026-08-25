"""A room description that can change — `[[locations.description_variants]]`.

A location is the screen a player re-enters more than any other, and until this
existed the engine emitted its description as ONE static string: the same sentence
at 03:00 and at 18:00, on day one and on day ninety. `_resolve_at_references`
substitutes names and fields only, so there was no way to author a variant at all.

Measured across a 26-game field: 22% of rooms rotate their text and 17% vary by
hour, against 0% and 0% here. That gap is what this closes, and it is the engine
half of `games/mrs_vance/REVIEW.md` M1 — the half that could not be fixed by
writing, which is why the first attempt (nine one-time "arrival" canvases) was
reverted.

Two properties are load-bearing and both are asserted here:

  1. It is INERT without variants. Every existing game must emit byte-identical
     output, because this shipped into a repo with seven built games in it.
  2. It cannot FAIL OPEN. `setup.triggerConditionsSatisfied` returns TRUE for any
     conditions{} missing `version`, with no build error — so a variant without it
     would render forever and the location's own description would never be seen
     again. That is worse than having no variants, so the importer must refuse it.

⚠️ Targets **v2 explicitly**, for the reason test_media_pool_cycle.py gives: v1 is
deprecated and a v1-instantiating test can stay green while v2 is broken outright.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_location_description_variants.py -q
"""
import re
import types

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.template_import import (
    GameTemplate,
    TemplateLocation,
    TemplatePlayer,
    TemplateProject,
    TemplateTime,
    validate,
)


def _loc(description="Gravel between the house and the shop.", variants=None):
    """A location as the generator sees it — the model object, not the TOML."""
    return types.SimpleNamespace(
        name="Yard",
        description=description,
        properties={"description_variants": variants} if variants else {},
    )


NIGHT = {"version": "1.0", "logic": "AND",
         "items": [{"type": "time_window", "start": "22:00", "end": "05:00"}]}
FRIDAY = {"version": "1.0", "logic": "AND",
          "items": [{"type": "flag", "subject": "player",
                     "flag_key": "week_straight", "operator": "is_true"}]}


# ── 1. inert without variants ────────────────────────────────────────────────

def test_a_location_with_no_variants_emits_exactly_one_paragraph():
    """The whole installed base depends on this. Seven built games were hashed
    before and after this feature landed and every one was byte-identical."""
    g = TweeComprehensiveGeneratorV2()
    out = g._render_location_description(_loc())

    assert out == "<p>Gravel between the house and the shop.</p>"
    assert "<<if" not in out


def test_an_empty_description_still_falls_back_to_the_old_placeholder():
    g = TweeComprehensiveGeneratorV2()
    assert g._render_location_description(_loc(description="")) == \
        "<p>A location in your story.</p>"


# ── 2. the chain, and the base as its else ───────────────────────────────────

def test_variants_emit_a_first_match_chain_with_the_base_as_the_else():
    g = TweeComprehensiveGeneratorV2()
    out = g._render_location_description(_loc(variants=[
        {"conditions": NIGHT, "text": "The pole light is the only thing on."},
        {"conditions": FRIDAY, "text": "The week is straight and everybody knows it."},
    ]))

    assert out.startswith("<<if setup.triggerConditionsSatisfied(")
    assert "<<elseif setup.triggerConditionsSatisfied(" in out
    assert out.endswith("<<else>><p>Gravel between the house and the shop.</p><</if>>")
    # first match wins — one <<if>>, one <<elseif>>, one <<else>>, one close
    assert out.count("<<if ") == 1
    assert out.count("<<elseif ") == 1
    assert out.count("<<else>>") == 1
    assert out.count("<</if>>") == 1


def test_the_conditions_reach_the_runtime_verbatim():
    """No new primitive: this is the same helper the location passage already calls
    for entry_conditions a few lines above."""
    g = TweeComprehensiveGeneratorV2()
    out = g._render_location_description(_loc(variants=[{"conditions": NIGHT, "text": "Night."}]))

    assert '"version": "1.0"' in out
    assert '"time_window"' in out


def test_a_malformed_variant_is_skipped_rather_than_emitted_broken():
    """Defence in depth — the importer refuses these, but a hand-built model or a
    --use-db path must not produce a passage with a dangling <<if>>."""
    g = TweeComprehensiveGeneratorV2()
    out = g._render_location_description(_loc(variants=[
        {"text": "no conditions"}, {"conditions": NIGHT}, "not a dict",
    ]))

    assert out == "<p>Gravel between the house and the shop.</p>"


# ── 3. both emit paths use the one helper ────────────────────────────────────

def test_both_location_paths_call_the_same_helper():
    """The gated and ungated location emitters were byte-identical copies of each
    other, which is exactly how a change like this gets half-applied."""
    import inspect
    from apps.game_generation.twee_comprehensive.generators import v2 as mod

    src = inspect.getsource(mod)
    assert src.count("{self._render_location_description(location, location_id)}") == 2
    # and the old inline form is gone from both
    assert 'if location.description else "A location in your story."}</p>' not in src


# ── 4. it cannot fail open ───────────────────────────────────────────────────

def _template(variants, description="Gravel."):
    """The smallest GameTemplate `validate()` will walk — six required fields, and a
    single location carrying the variants under test."""
    return GameTemplate(
        schema_version="1.0",
        project=TemplateProject(slug="probe", title="Probe"),
        time=TemplateTime(),
        player=TemplatePlayer(),
        npcs=[],
        locations=[TemplateLocation(id="the_yard", name="Yard",
                                    description=description,
                                    description_variants=variants)],
    )


def _variant_errors(template):
    return [e for e in validate(template) if "description_variants" in e]


@pytest.mark.parametrize("bad, needle", [
    ([{"text": "Night.", "conditions": {"logic": "AND", "items": []}}], "version"),
    ([{"text": "Night.", "conditions": {}}], "no conditions"),
    ([{"conditions": NIGHT, "text": "   "}], "no text"),
    (["not a dict"], "must be a dict"),
])
def test_the_importer_refuses_a_variant_that_would_render_forever(bad, needle):
    errs = _variant_errors(_template(bad))
    assert [e for e in errs if needle in e], f"expected {needle!r}, got: {errs}"


def test_a_well_formed_variant_raises_no_description_variant_error():
    assert not _variant_errors(_template([{"conditions": NIGHT, "text": "The pole light."}]))


def test_a_variant_with_no_base_description_is_refused():
    """The chain's else is the base. Without one, no-match renders nothing at all."""
    errs = _variant_errors(_template([{"conditions": NIGHT, "text": "The pole light."}],
                                     description=""))
    assert [e for e in errs if "base `description`" in e]
