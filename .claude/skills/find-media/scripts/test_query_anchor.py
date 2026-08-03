"""An NSFW query needs an ACT word, or it never reaches porn at all.

Measured 2026-08-01 on `vesper`, same query minus one token:

    riding cowgirl man in office chair gif  -> 83 urls, ZERO on a porn host
                                               (Tenor, BBC, Wikipedia, Billboard, NFL, Warhol)
    cowgirl riding fuck office chair gif    -> 73 urls, 69 on porn hosts (95%)

The validator PASSED the first one. `cowgirl` sits in SEXUAL_TERMS_FOR_SFW_CHECK, so
`has_sexual` was true and nothing fired. That set answers "is a sexual word leaking into an
SFW query?" — a different question from "will this land in porn?" — and for the second
question a position name is worse than useless, because `cowgirl` is also a ranch.

These are the first tests for these scripts. Run:
    python3 -m pytest .claude/skills/find-media/scripts/test_query_anchor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scene_semantics import ACT_ANCHORS, SEXUAL_TERMS_FOR_SFW_CHECK  # noqa: E402
from validate_queries import check_tier_alignment  # noqa: E402

ANCHOR_ISSUE = "no_act_anchor:position_or_setting_words_only"


def _issues(query, tier):
    _, issues = check_tier_alignment(query, tier)
    return issues


# ── the two measured cases, which are the whole reason this exists ──────────────────────

def test_the_real_failure_is_flagged():
    """The exact query that returned 0 of 83 on a porn host."""
    assert ANCHOR_ISSUE in _issues("riding cowgirl man in office chair gif", "t5")


def test_the_real_fix_passes():
    """Same query plus one act token — 69 of 73 on porn hosts."""
    assert ANCHOR_ISSUE not in _issues("cowgirl riding fuck office chair gif", "t5")


# ── the asymmetry that hid this bug for a whole session ─────────────────────────────────

def test_oral_anchors_a_query_by_itself():
    """`blowjob` is an act word, so every oral slot passed and the gap stayed invisible."""
    assert ANCHOR_ISSUE not in _issues("back alley blowjob gif amateur", "t5")


def test_position_names_alone_never_anchor():
    """The three ordinary-English position names, each on its own."""
    for position in ("cowgirl", "missionary", "doggy"):
        assert ANCHOR_ISSUE in _issues(f"{position} office gif", "t5"), position


# ── scope: who this check may and may not fire on ───────────────────────────────────────

def test_t4_is_exempt():
    """t4 is BORDERLINE. A tease beat must never be forced to carry a penetrative word."""
    assert ANCHOR_ISSUE not in _issues("downblouse leaning forward gif", "t4")


def test_sfw_tiers_are_exempt():
    """An SFW slot has no business carrying an act word; the check must not demand one."""
    assert ANCHOR_ISSUE not in _issues("empty kitchen morning light", "base")


def test_every_nsfw_tier_is_covered():
    for tier in ("t5", "t6", "t7", "t8"):
        assert ANCHOR_ISSUE in _issues("riding cowgirl chair gif", tier), tier


# ── no regression in the neighbouring checks ────────────────────────────────────────────

def test_sfw_sexual_term_check_still_fires():
    """SEXUAL_TERMS_FOR_SFW_CHECK keeps `cowgirl`; that is correct for ITS job."""
    assert "tier_mismatch:sfw_query_has_sexual_term" in _issues("cowgirl kitchen", "base")


def test_the_two_sets_are_deliberately_different():
    """Position names belong in one set and must stay out of the other."""
    for position in ("cowgirl", "missionary", "doggy"):
        assert position in SEXUAL_TERMS_FOR_SFW_CHECK, position
        assert position not in ACT_ANCHORS, position


# ── the word-boundary trap found while writing this ─────────────────────────────────────

def test_inflections_are_listed_not_prefix_matched():
    """`\\bfuck\\b` does not match "fucking", so inflections must be explicit members."""
    assert ANCHOR_ISSUE not in _issues("fucking her on the desk gif", "t5")


def test_sexy_is_not_an_act():
    """The reason prefix matching was rejected: `sex` would swallow "sexy", a mood."""
    assert ANCHOR_ISSUE in _issues("sexy secretary office chair gif", "t5")


# ── `bj`, added 2026-08-03 after the enforced rule flagged the BETTER query ──────────────

def test_bj_anchors_a_query():
    """The corpus's own abbreviation. It beat `blowjob` on two vesper slots — outdoors
    (real alleys vs indoor studio kneeling) and indoors (`bj chair`/`bj couch` are
    Sex.com's own tag names). Before this it was flagged `no_act_anchor`, i.e. the rule
    penalised the query that worked."""
    assert ANCHOR_ISSUE not in _issues("bar bj chair seated gif", "t5")
    assert ANCHOR_ISSUE not in _issues("public alley bj gif amateur", "t5")


def test_bj_does_not_match_inside_other_words():
    """A 2-letter anchor is the riskiest kind, so pin the substring case explicitly.
    `\\bbj\\b` cannot match "objects"/"subject" — the `b` there follows a word char."""
    for innocent in ("objects on the desk", "subject of the photo", "objection"):
        assert ANCHOR_ISSUE in _issues(innocent, "t5"), innocent
