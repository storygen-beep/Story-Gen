"""`[settings] ambient_render` — what a random ambient does to the room it fires on.

Until this existed, an ambient took the WHOLE screen. `getStoryCanvasRedirect`
returned a story one-shot or a random encounter without distinguishing them and the
location passage <<goto>>'d either, so a player walking into the Yard could be moved
to an event having never seen the Yard: no title, no description, no NPC portraits,
no activities, no exits.

The field does something narrower. destroyer's room screens, read from source:

    <<if _scene is 0>>     <img …>  "…you noticed a black girl taking off her T-shirt."
    <<elseif _scene > 0>>  <img …>  "Your neighborhood. Quiet, sunny area…"
    <</if>>
    <div class="staff-bar"> … </div>      ← either way
    … exits …                              ← either way

The encounter replaces the DESCRIPTION. Everything else stands. That is what
"inline" does here, and a STORY one-shot keeps the redirect under both settings
because a story beat owning the screen is correct.

⚠️ Default is "redirect", and these tests exist mostly to prove that: seven built
games were in the repo when this landed and every authored passage in all of them
had to come out byte-identical.

    pytest apps/game_generation/tests/test_ambient_render_inline.py -q
"""
import inspect

import pytest

from apps.game_generation.twee_comprehensive.generators import v2 as v2mod
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


def _gen(mode=None):
    g = TweeComprehensiveGeneratorV2()
    if mode is not None:
        g.ambient_render = mode
    return g


# ── 1. the default changes nothing ───────────────────────────────────────────

def test_default_is_redirect_and_emits_exactly_what_it_always_did():
    g = _gen()   # attribute absent entirely — the getattr default must hold
    assert g._location_autofire_line("the_yard") == \
        '<<set _autoFire = setup.getStoryCanvasRedirect("the_yard")>>'


def test_redirect_leaves_the_description_slot_untouched():
    g = _gen("redirect")
    assert g._wrap_ambient_slot("<p>Gravel.</p>", "the_yard") == "<p>Gravel.</p>"


# ── 2. inline splits the one-shot from the ambient ───────────────────────────

def test_inline_redirects_only_story_one_shots():
    """A story beat still owns the screen. Only the ambient stops doing that."""
    g = _gen("inline")
    line = g._location_autofire_line("the_yard")

    assert line == '<<set _autoFire = setup.getStoryOneShotRedirect("the_yard")>>'
    assert "checkRandomEncounters" not in line


def test_inline_puts_the_ambient_in_the_description_slot():
    g = _gen("inline")
    out = g._wrap_ambient_slot("<p>Gravel.</p>", "the_yard")

    assert out == ('<<set _amb = setup.checkRandomEncounters("the_yard", true)>>'
                   '<<if _amb>><<include _amb>><<else>><p>Gravel.</p><</if>>')


def test_inline_passes_the_inline_only_flag():
    """Without it an ambient carrying Lane-3 substitutions would be included, and its
    injected <<goto>> would navigate away mid-render — taking the room with it."""
    g = _gen("inline")
    assert '"the_yard", true)' in g._wrap_ambient_slot("<p>x</p>", "the_yard")


def test_inline_composes_with_description_variants():
    """The two features share the slot; the ambient wraps the whole variant chain."""
    import types
    g = _gen("inline")
    loc = types.SimpleNamespace(
        name="Yard", description="Gravel.",
        properties={"description_variants": [{
            "conditions": {"version": "1.0", "logic": "AND", "items": []},
            "text": "Dark.",
        }]})
    out = g._render_location_description(loc, "the_yard")

    assert out.startswith('<<set _amb = setup.checkRandomEncounters("the_yard", true)>>')
    assert "<<if _amb>><<include _amb>><<else>>" in out
    assert out.endswith("<<else>><p>Gravel.</p><</if>><</if>>")


# ── 3. the room still renders around it ──────────────────────────────────────

def test_portraits_activities_and_navigation_sit_outside_the_ambient_wrapper():
    """The whole point. If these moved inside the <<if _amb>> we would have rebuilt
    the bug with extra steps."""
    src = inspect.getsource(v2mod)

    # both location paths: description slot, THEN the room's own furniture
    assert src.count("{self._render_location_description(location, location_id)}") == 2
    assert src.count('<<= setup.renderNpcPortraits("{location_id}")>>') == 2
    assert src.count('<<= setup.renderSoloActivities("{location_id}")>>') == 2
    # and the wrapper only ever encloses the description it is handed
    body = inspect.getsource(TweeComprehensiveGeneratorV2._wrap_ambient_slot)
    assert "renderNpcPortraits" not in body
    assert "location-navigation" not in body


def test_the_runtime_carries_the_substitution_guard():
    src = inspect.getsource(v2mod)
    assert "if (inlineOnly && (setup.canvasSubstitutions || {{}})[canvasList[i].id])" in src
    assert "setup.getStoryOneShotRedirect = function(locationId)" in src


# ── 4. a typo fails the build ────────────────────────────────────────────────

def _template(mode):
    t = GameTemplate(
        schema_version="1.0",
        project=TemplateProject(slug="probe", title="Probe"),
        time=TemplateTime(),
        player=TemplatePlayer(),
        npcs=[],
        locations=[TemplateLocation(id="the_yard", name="Yard", description="Gravel.")],
    )
    t.ambient_render = mode
    return t


@pytest.mark.parametrize("mode", ["inline", "redirect"])
def test_the_two_valid_modes_pass_validation(mode):
    assert not [e for e in validate(_template(mode)) if "ambient_render" in e]


def test_a_typo_fails_the_build_rather_than_silently_staying_on_redirect():
    """Silently falling back would leave the game doing the exact thing the author
    was turning off, with nothing on screen to say so."""
    errs = [e for e in validate(_template("inlined")) if "ambient_render" in e]
    assert errs and "not valid" in errs[0]
