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


# ── mood words, added 2026-08-05 after media_lab_f shelved romance on a facial slot ──────
#
# Measured: `tender intimate facial gif`-class queries built a 17% on-act shelf vs 50% for
# the act-first control (media_lab_h), 36% romance slugs, 45 Dreamstime stills vs 0. Google
# weights every token; the mood words have a vastly larger SFW cluster to fall into, so
# they outvote the act word. Two branches now cover it: `too_vanilla` (mood words, no act
# word) and `vanilla_dilution` (mood words BESIDE an act word — the case the old check
# waved through).

DILUTION_ISSUE = "vanilla_dilution:mood_words_pull_stock_results"
TOO_VANILLA_ISSUE = "tier_mismatch:nsfw_query_too_vanilla"


def test_the_query_that_passed_clean_now_flags():
    """media_lab_f ran `passionate real couple cumshot gif` — the old validator passed it
    with zero issues (`passionate` unlisted, `cumshot` anchoring) and the shelf went
    Dreamstime. The exact query must flag now."""
    assert DILUTION_ISSUE in _issues("passionate real couple cumshot gif", "t5")


def test_mood_beside_act_anchor_flags():
    """`gentle` joined the vanilla list, and `cumshot` (ACT_ANCHORS-only, absent from
    SEXUAL_TERMS_FOR_SFW_CHECK) now counts as act presence for the vanilla branches."""
    assert DILUTION_ISSUE in _issues("gentle loving cumshot gif", "t5")


def test_mood_beside_sexual_term_flags():
    """The original hole: with `blowjob` in SEXUAL_TERMS_FOR_SFW_CHECK, has_sexual was
    true and the old `not has_sexual` guard suppressed the vanilla check entirely."""
    assert DILUTION_ISSUE in _issues("tender loving blowjob gif", "t5")


def test_mood_without_act_word_is_still_too_vanilla():
    """`facial` is deliberately NOT an act anchor (it is a spa treatment), so f's
    `tender intimate facial gif` is the no-act case, not the dilution case."""
    issues = _issues("tender intimate facial gif", "t5")
    assert TOO_VANILLA_ISSUE in issues
    assert DILUTION_ISSUE not in issues


def test_old_too_vanilla_branch_is_intact():
    assert TOO_VANILLA_ISSUE in _issues("romantic bedroom couple", "t5")


def test_act_first_query_passes_both_mood_checks():
    """The shape the doctrine wants: act + position + anti-studio + gif."""
    issues = _issues("facial cumshot amateur gif", "t5")
    assert DILUTION_ISSUE not in issues
    assert TOO_VANILLA_ISSUE not in issues


def test_sfw_tiers_are_exempt_from_mood_checks():
    """`sweet` in a base-tier slot is a lifestyle word, not a leak."""
    issues = _issues("sweet couple morning kitchen", "base")
    assert DILUTION_ISSUE not in issues
    assert TOO_VANILLA_ISSUE not in issues
