"""Content routing — scene_semantics.py.

    python3 -m pytest .claude/skills/find-media/scripts/test_scene_semantics.py

Run by explicit path: the repo's pytest sets `testpaths = ["tests"]` and never reaches the
skills tree.

Three groups carry the weight, and every string in the first two is a REAL vesper caption
rather than a constructed one — the same discipline as `tests/test_media_band.py`, whose
`test_cocky_is_not_a_cock` pins a shipped caption.

⚠ `test_an_avoid_clause_is_not_content` and friends pin the 2026-09-08 defect: the classifier
  scored a beat's `Avoid:` directives as if they described the beat. Four vesper tease rungs
  were retagged _t5 by an UNATTENDED `auto_retag` because of it. If these go red, find-media
  starts hunting hardcore for clothed teases again.

⚠ `test_the_lowest_authored_tiers_are_never_demoted` and `test_a_tease_tier_is_still_checked`
  pin the two traps in the tier-set move. The second one is the important one: it is the test
  that fails if t2/t3 fall out of every branch of check_tier_alignment, which looks like
  "nothing to report" rather than like a bug.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from scene_semantics import (  # noqa: E402
    BORDERLINE_TIERS,
    LOWEST_AUTHORED_TIERS,
    NSFW_TIERS,
    SFW_TIERS,
    check_format_alignment,
    classify_content_family,
    classify_content_rating,
    propose_tag,
)
from validate_queries import check_tier_alignment  # noqa: E402

# ── Real corpus strings ────────────────────────────────────────────────────────────────
# games/vesper/toml_phases/5_scenes.toml, the four rungs the defect actually retagged.
GRIER_TEASE = (
    "A woman in an open-necked blouse bending down out of her chair toward the floor in a "
    "dim filthy workshop, the front of her blouse hanging open, a heavy older seated man "
    "watching from an armchair with a glass. Must show: downblouse cleavage, her clothed "
    "and bending, him seated and looking. Avoid: nudity, avoid: sex, avoid: a clean or "
    "bright room, avoid: a young man."
)
GRIER_FLASH_QUERIES = ["cleavage flash leaning over man in armchair dim room gif"]
GRIER_FLASH = (
    "A woman in an open blouse leaning over the arm of a chair to pour a drink for a heavy "
    "older seated man in a dim filthy room, her front on show, him looking. Must show: her "
    "leaning over him clothed but open, him seated and looking. Avoid: nudity, avoid: sex."
)
# The must-show clause is the ONLY place a hard word appears in this one.
MERCER_KNEES = (
    "A woman kneeling in front of a seated man in a bare concrete room. Must show: her on "
    "her knees, his cock in her mouth, his hand at her hair setting the pace."
)
# The avoid clause names acts the beat must NOT contain.
MERCER_ASS = (
    "A heavy older man in shirtsleeves standing behind a naked younger woman in a bare "
    "concrete room, both hands full of her ass. Must show: her naked and standing, him "
    "clothed and behind her. Avoid: penetration of any kind, anal, her bent over or "
    "kneeling, spanking or striking."
)


# ── Group 1: an avoid clause is a directive, not content ───────────────────────────────

def test_an_avoid_clause_is_not_content():
    """The 2026-09-08 defect, exactly. `avoid: sex` scored as `sex`."""
    signal, matched = classify_content_rating(GRIER_TEASE, [])
    assert signal == "borderline", f"avoid-clause scored as content: {matched}"
    assert "sex" not in matched


def test_the_defect_produced_an_unattended_retag():
    """Not merely a wrong label — `auto_retag` is taken without asking."""
    signal, matched = classify_content_rating(GRIER_TEASE, [])
    proposal = propose_tag("scenes/rung_grier_tease_t2", "t2", True, signal, matched)
    assert proposal.action != "auto_retag"


def test_a_must_show_clause_is_still_counted():
    """`Must show:` is POSITIVE evidence. 12 of 40 supply the only hard word they have."""
    signal, matched = classify_content_rating(MERCER_KNEES, [])
    assert signal == "hard_nsfw"
    assert "cock" in matched


def test_an_avoid_clause_does_not_pollute_the_evidence():
    """The signal was already right here; the `matched` list was not — and it is printed
    to the human in the proposal's reason string."""
    signal, matched = classify_content_rating(MERCER_ASS, [])
    assert signal == "hard_nsfw"          # correct, from "her naked and standing"
    assert "anal" not in matched          # lifted from "Avoid: ... anal" before the fix
    assert "penetration" not in matched


def test_search_queries_are_never_truncated():
    """119 corpus blocks have euphemistic prose and are rated entirely by their queries."""
    signal, _ = classify_content_rating(
        "A woman kneeling at a desk in a penthouse office while a man keeps working.",
        ["office blowjob desk penthouse"],
    )
    assert signal == "hard_nsfw"


def test_the_format_axis_reads_through_the_same_filter():
    """A still portrait saying `avoid: kissing` was being told to become a .webm."""
    desc = "A still portrait of a man at a desk. Avoid: kissing, avoid: undressing."
    assert classify_content_family(desc, [])[0] == "ambiguous"
    assert check_format_alignment("scenes/x.jpg", desc, []).passed


# ── Group 2: `flash` is a homograph ────────────────────────────────────────────────────

def test_a_cleavage_flash_is_not_nudity():
    """Every bare `flash` in the corpus is a clothed tease. This one arrives via a QUERY,
    so the avoid-clause fix alone does not catch it."""
    signal, matched = classify_content_rating(GRIER_FLASH, GRIER_FLASH_QUERIES)
    assert signal == "borderline", f"bare 'flash' read as nudity: {matched}"


def test_flashing_is_still_nudity():
    """The inflected form is the genuine one — 'woman flashing tits bending over'."""
    assert classify_content_rating("A woman flashing tits bending over.", [])[0] == "hard_nsfw"


def test_a_skirt_flash_tease_stays_borderline():
    """games/vesper — rung_renner_tease_t2, the other real bare-`flash` caption."""
    signal, _ = classify_content_rating(
        "In a cramped office a woman teases close — lifting her skirt to flash the underwear "
        "beneath while a seated man tries not to look, stays clothed, withheld.",
        ["office tease skirt flash underwear"],
    )
    assert signal == "borderline"


# ── Group 3: the tier sets, and the two traps in moving them ───────────────────────────

def test_a_tease_tier_is_never_sfw():
    """LO's ruling 2026-08-04. Mirrors TIER_BAND in apps/common/media_band.py."""
    for tier in ("t2", "t3", "t4"):
        assert tier not in SFW_TIERS
        assert tier in BORDERLINE_TIERS
    assert SFW_TIERS == {"base", "location"}


@pytest.mark.parametrize("tier", ["t2", "t3"])
@pytest.mark.parametrize("signal", ["hard_nsfw", "borderline", "sfw", "unknown"])
def test_an_authored_tease_tier_is_left_alone(tier, signal):
    """The author put it on the ladder; nothing here second-guesses which rung."""
    assert propose_tag("x", tier, True, signal, ["w"]).action == "leave"


def test_the_lowest_authored_tiers_are_never_demoted():
    """TRAP B. Moving t2/t3 to the NSFW side switches on the down-grade branch, which
    proposes `base` — 'not on the sexual ladder at all', the one thing an authored suffix
    rules out."""
    assert propose_tag("x", "t2", True, "sfw", ["hug"]).proposed_tag != "base"
    assert LOWEST_AUTHORED_TIERS == {"t2", "t3"}


@pytest.mark.parametrize("tier", ["t4", "t5"])
def test_the_higher_tiers_keep_their_down_grade(tier):
    """The exemption is narrow — t4+ still asks."""
    p = propose_tag("x", tier, True, "sfw", ["hug"])
    assert (p.action, p.proposed_tag) == ("ask", "base")


def test_an_untagged_explicit_slot_is_still_caught():
    """The genuine catch this module exists for must survive the move."""
    p = propose_tag("scenes/x.webm", "base", False, "hard_nsfw", ["fuck"])
    assert (p.action, p.proposed_tag) == ("auto_retag", "t5")


@pytest.mark.parametrize("tier", ["t2", "t3"])
def test_a_tease_tier_is_still_checked(tier):
    """TRAP A — the one that fails silently.

    check_tier_alignment's first rule is SFW_TIERS-only and every later rule is
    NSFW_TIERS-only. Moving t2/t3 between them drops them out of EVERY branch, so a t2
    slot carrying `blowjob gif` reports no issues at all — indistinguishable from a clean
    query. This test is what makes that visible.
    """
    passed, issues = check_tier_alignment("blowjob gif", tier)
    assert not passed
    assert "tier_mismatch:tease_query_has_hard_act_word" in issues


@pytest.mark.parametrize("tier", ["t2", "t3"])
def test_tease_vocabulary_passes_on_a_tease_tier(tier):
    """A tease beat is never REQUIRED to carry a hard act word — which is why the NSFW
    `no_act_anchor` rule stays NSFW-only."""
    assert check_tier_alignment("downblouse tease amateur gif", tier)[0]


def test_t4_keeps_its_exemption():
    """The trap inside TRAP A's fix.

    Scoping the new tease rule to all of BORDERLINE_TIERS flags t4, and t4 is the
    makeout/ORAL band where a hard act word is correct — vesper's `sex/grier_room_oral_t4`
    legitimately queries a kneeling blowjob. The first run of that branch flagged it twice.
    t4's exemption predates this rule; keep it.
    """
    assert check_tier_alignment(
        "kneeling slow blowjob older man in armchair amateur gif", "t4"
    )[0]


def test_a_sexual_term_still_flags_on_a_genuinely_sfw_tier():
    """Regression: `cowgirl` leaking into a clean slot must still fire."""
    passed, issues = check_tier_alignment("cowgirl kitchen", "base")
    assert not passed
    assert "tier_mismatch:sfw_query_has_sexual_term" in issues


def test_the_nsfw_anchor_rule_is_untouched():
    """Regression: the measured cowgirl case, 0 of 83 results on a porn host."""
    passed, issues = check_tier_alignment("cowgirl riding man in office chair gif", "t5")
    assert not passed
    assert "no_act_anchor:position_or_setting_words_only" in issues


def test_the_tier_sets_stay_disjoint():
    assert not (SFW_TIERS & BORDERLINE_TIERS)
    assert not (BORDERLINE_TIERS & NSFW_TIERS)
    assert not (SFW_TIERS & NSFW_TIERS)
