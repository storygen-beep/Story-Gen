"""`npcs[].role` — the short label under a speaker's name in a dialogue box.

A player reading `Cade:` on a line has to already know who Cade is. The answer
existed — `relationship`, "Your husband's eldest, 29…" — on the cast page, one
click away and outside the scene. This puts a short form of it under the name,
every time he speaks, WITHOUT taking the name away: portrait, name, role, line.

⚠️ IT IS AUTHORED, NEVER DERIVED, and the repo is why. Deriving it from
`relationship`'s first clause was the obvious idea and it collapses casts:

    mrs_vance    5 of 6 relationship strings contain "husband" — the husband, his
                 three sons, and his brother
    the_season   two characters whose strings both begin "Your brother"

A label that repeats is the confusion the field exists to remove, so a silent
derived default would be worse than nothing. Hence `validate()` refuses two roles
that match — the one rule a machine can hold here, since it cannot invent the words.

⚠️ Targets **v2 explicitly**, for the reason test_media_pool_cycle.py gives: v1 is
deprecated and a v1-instantiating test can stay green while v2 is broken.

    pytest apps/game_generation/tests/test_npc_role_label.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.template_import import (
    GameTemplate,
    TemplateNPC,
    TemplatePlayer,
    TemplateProject,
    TemplateTime,
    validate,
)

UUID = "uuid-cade"


def _gen(role="husband's eldest", portrait=""):
    g = TweeComprehensiveGeneratorV2()
    g.npc_slug_map = {"npc_cade": UUID}
    g.npc_map = {UUID: {"name": "Cade", "portrait": portrait, "role": role}}
    return g


def _line(g, speaker="npc", npc_id="npc_cade"):
    props = {"speaker": speaker}
    if speaker == "npc":
        props["npcId"] = npc_id
    return g._convert_blocks_to_game_html(
        [{"type": "dialog", "props": props, "content": "Slower."}])


# ── 1. the label renders under the name, and the name stays ──────────────────

def test_the_role_renders_and_the_name_is_still_there():
    """The whole point. Nothing is replaced — a swap would just move the memory
    tax onto the label."""
    out = _line(_gen())

    # No trailing colon since 2026-08-27: the name sits above the face in its own
    # column, and `Cade:` is inline speech attribution, which reads wrong there.
    assert "<strong>Cade</strong>" in out
    assert '<span class="dialog-role">husband&#x27;s eldest</span>' in out
    assert out.index("Cade") < out.index("dialog-role")


def test_the_face_is_a_sibling_of_the_flow_not_inside_it():
    """⚠️ Structural, and it is the whole mechanism. The face is a FLOAT and the text is
    normal flow beside it — that is the only way to get speech to wrap around a box, and
    it only works while the portrait is a sibling of `.dialog-content`. Put it back
    inside and the float has nothing to wrap and the layout silently flattens."""
    out = _line(_gen(portrait="faces/cade.jpg"))

    assert out.index('class="portrait"') < out.index('<div class="dialog-content">')


def test_name_role_and_speech_are_ONE_flow_with_no_wrapper_between_them():
    """⚠️ The layout this replaced put the name in a fixed-width column, and LO's whole
    complaint was the gap that left between the label and the line being spoken. A column
    of any width reintroduces it. So: name, role and speech run together, in that order,
    with nothing between the role and the first word of the line except one space.

    An earlier version of this file asserted the OPPOSITE — that `.dialog-content` held
    the line and nothing else. That test described a design that has been abandoned, and
    is inverted here rather than deleted so the reversal is on the record."""
    content = _line(_gen(portrait="faces/cade.jpg")).split('<div class="dialog-content">')[1]

    assert content.startswith("<strong>Cade</strong>")
    assert '<span class="dialog-role">husband&#x27;s eldest</span> Slower.' in content
    assert "portrait" not in content          # the face stays outside the flow


def test_the_colon_goes_on_whichever_of_name_or_role_comes_last():
    """The colon itself is CSS (`::after`), so what the HTML must get right is WHICH
    element is last, and that is carried by `dlg-inline`:

        with a role     <strong>Dorn</strong><span class="dialog-role">husband</span>
        without one     <strong class="dlg-inline">Dorn</strong>

    `dlg-inline` doubles as the rule that keeps a role-less name on the speech's own
    line instead of taking a row to itself."""
    with_role = _line(_gen(role="husband's eldest"))
    assert "<strong>Cade</strong>" in with_role
    assert "dlg-inline" not in with_role

    without = _line(_gen(role=""))
    assert '<strong class="dlg-inline">Cade</strong>' in without
    assert "dialog-role" not in without


def test_a_speaker_with_no_portrait_still_gets_one():
    """The column must never be visually empty, or the face slot collapses and the
    name jumps up. `_render_portrait("")` returns the SVG silhouette; the old
    `if portrait else ''` guard at the call site skipped it entirely."""
    assert 'class="portrait' in _line(_gen(portrait=""))


def test_an_npc_with_no_role_renders_exactly_what_it_always_did():
    """Six built games declare no role. Their dialogue boxes must not move."""
    assert _line(_gen(role="")) == _line_without_role_baseline()


def _line_without_role_baseline():
    g = TweeComprehensiveGeneratorV2()
    g.npc_slug_map = {"npc_cade": UUID}
    g.npc_map = {UUID: {"name": "Cade", "portrait": ""}}   # no `role` key at all
    return _line(g)


def test_a_whitespace_only_role_renders_no_line():
    assert "dialog-role" not in _line(_gen(role="   "))


# ── 2. the other two speakers are untouched ──────────────────────────────────

def test_the_player_speaker_takes_no_role():
    """`speaker = "player"` is her; a role under her own name is nonsense."""
    out = _line(_gen(), speaker="player")
    assert "dialog-role" not in out


def test_an_unknown_speaker_stays_a_stranger():
    """`speaker = "unknown"` renders `Stranger` — there is nobody to label, so the name
    takes the colon and stays inline."""
    out = _line(_gen(), speaker="unknown")
    assert '<strong class="dlg-inline">Stranger</strong>' in out
    assert "dialog-role" not in out


def test_every_speaker_kind_gets_a_face():
    """A Stranger line and a player line sit among NPC lines on the same screen. If any
    of the three renders without a face, the text beside it starts at the left margin
    while its neighbours are indented past a portrait — a ragged edge down the scene."""
    for speaker in ("npc", "player", "unknown"):
        out = _line(_gen(), speaker=speaker)
        assert 'class="portrait' in out, speaker
        assert out.index('class="portrait') < out.index('<div class="dialog-content">'), speaker


# ── 3. it is build-time text, not save state ─────────────────────────────────

def test_role_is_stripped_before_npcs_reaches_runtime_state():
    """The label is baked into the passage HTML at build time and nothing reads it
    back, so shipping it in $npcs would put a dead key in every save of every game
    — including the games that never set one. Caught by hashing seven builds."""
    import inspect
    from apps.game_generation.twee_comprehensive.generators import v2 as mod

    src = inspect.getsource(mod)
    assert 'entry.pop("role", None)' in src


# ── 4. a label that repeats is refused ───────────────────────────────────────

def _template(*roles):
    return GameTemplate(
        schema_version="1.0",
        project=TemplateProject(slug="probe", title="Probe"),
        time=TemplateTime(),
        player=TemplatePlayer(),
        npcs=[TemplateNPC(id=f"npc_{i}", name=f"N{i}", role=r)
              for i, r in enumerate(roles)],
        locations=[],
    )


def _role_errors(t):
    return [e for e in validate(t) if "role" in e]


def test_two_characters_may_not_wear_the_same_label():
    """`brother` is fine with one brother and useless with two. the_season has
    exactly this shape, and is the game whose reader said "I don't know who is who"."""
    errs = _role_errors(_template("brother", "brother"))
    assert errs and "already used by" in errs[0]


def test_the_check_ignores_case_and_padding():
    assert _role_errors(_template("Brother", " brother "))


def test_distinct_labels_pass():
    assert not _role_errors(_template("elder brother", "younger brother", "uncle"))


def test_empty_roles_are_not_duplicates_of_each_other():
    """Most games declare none at all; that must never read as a collision."""
    assert not _role_errors(_template("", "", ""))


def test_a_sentence_is_refused_as_a_label():
    """A role is a LABEL under a name; a sentence about them belongs in
    `relationship`, which the cast page renders."""
    errs = _role_errors(_template("Runs the canteen window and the scale on Tuesdays"))
    assert errs and "words" in errs[0]
