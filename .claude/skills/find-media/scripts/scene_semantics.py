#!/usr/bin/env python3
"""
scene_semantics.py — what a scene IS, independent of where you search for it

Split out of validate_queries.py. Everything here answers a question about the SCENE,
never about a search engine's dialect:

  infer_tier_tagged / infer_tier   what heat the author declared (the _tN suffix)
  classify_content_family          motion or still
  check_format_alignment           does the declared extension match that
  classify_content_rating          SFW / borderline / NSFW
  propose_tag                      reconcile the author's tag against the content

That makes this the ROUTING module, not a lint pass. gif-vs-jpg decides which retrieval
surface can serve the slot at all, and SFW-vs-NSFW decides which query dialect and which
sources apply — so these five calls run before a single search does. The query-dialect
rewriting that DOES depend on the target lives in validate_queries.py.

No CLI — validate_queries.py is the entry point and re-exports every name here, so
`from validate_queries import infer_tier` still works.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SFW_TIERS = {"base", "t2", "t3", "location"}
BORDERLINE_TIERS = {"t4"}
NSFW_TIERS = {"t5", "t6", "t7", "t8"}

SEXUAL_TERMS_FOR_SFW_CHECK = {
    "sex", "fuck", "blowjob", "handjob", "fingering", "cunnilingus",
    "oral", "pussy", "cock", "cum", "creampie", "penetration",
    "missionary", "doggy", "cowgirl",
}

# Content-family classification — drives format (image vs animated) independent of tier.
# Tier gates explicitness (what can be shown). Family gates motion (how it should be shown).

STATIC_KEYWORDS = {
    "dinner", "lunch", "breakfast", "meal", "cooking", "cook", "eating",
    "chores", "cleaning", "dishes", "laundry", "tidying",
    "talking", "conversation", "chat", "sitting", "standing", "watching",
    "reading", "studying", "working",
    "greeting", "arrival", "departure", "goodbye",
    "kitchen", "bedroom", "office", "garage", "backyard", "porch",
    "coffee", "wine", "food",
}

ANIMATED_KEYWORDS = {
    # Kisses — motion = chemistry
    "kiss", "kissing", "makeout", "make out", "snog", "french kiss", "making out",
    # Teasing / flirting (physical)
    "tease", "teasing", "seduce", "seducing", "flirt",
    # Undressing / exposure
    "undress", "undressing", "strip", "stripping", "naked", "nude",
    "flash", "flashing", "expose", "exposing", "topless",
    # Bathing / washing (solo visible body)
    "bathe", "bathing", "bath", "shower", "showering", "washing",
    # Touch / intimate (erotic context)
    "grope", "fondle", "caress",
    # Core sex acts — prefer -ing forms where the bare verb has daily-life
    # meaning ("ride the bus", "5am grind") to avoid false positives on
    # fitness/lifestyle captions
    "sex", "fuck", "fucking", "thrusting",
    "riding", "grinding",
    "blowjob", "handjob", "fingering", "cunnilingus", "oral", "eating out",
    "missionary", "doggy", "cowgirl", "spooning", "bent over",
    "cum", "creampie", "orgasm", "climax",
}

# Content-RATING buckets — drive the SFW/NSFW routing decision (which pipeline).
# PURPOSE-BUILT and deliberately NOT the format ANIMATED_KEYWORDS set: format lumps
# "kiss"/"bath" with "fuck" because all three are motion; rating must keep them apart
# because a clothed kiss is stock-findable while a sex act is not. The routing question
# is "is there nudity or a sex act?" — not "is it motion?".
RATING_NUDITY = {
    "nude", "naked", "topless", "bottomless",
    "undress", "undressing", "strip", "stripping", "flash", "flashing",
}
# Stock genuinely can't serve these → confident NSFW.
RATING_HARD_NSFW = SEXUAL_TERMS_FOR_SFW_CHECK | RATING_NUDITY | {"anal", "deepthroat"}
# Clothed→explicit span; only the author knows the heat → default to ASK.
RATING_BORDERLINE = {
    "kiss", "kissing", "makeout", "make out", "making out", "snog", "french kiss",
    "tease", "teasing", "seduce", "seducing", "grind", "grinding",
    "caress", "grope", "fondle", "straddle", "in bed", "lingerie",
    "bathe", "bathing", "bath", "shower", "showering", "washing",
}
# Vanilla → stock is fine.
RATING_SFW = STATIC_KEYWORDS | {
    "flirt", "flirting", "hug", "hugging", "embrace", "holding hands", "hold hands",
    "cuddle", "cuddling", "smile", "date", "greet", "wave",
}

NON_CANVAS_TYPES = {"location_image", "clothing_image", "social_post_image", "dating_profile_photo"}

ANIMATED_EXTENSIONS = {".webm", ".mp4", ".gif"}
STATIC_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass
class FormatCheck:
    file: str
    current_extension: str
    detected_family: str  # "static" | "animated" | "ambiguous"
    matched_keywords: list[str]
    recommended_extension: str | None
    passed: bool
    message: str


@dataclass
class TagProposal:
    file: str
    current_tag: str
    was_tagged: bool
    content_signal: str  # "hard_nsfw" | "borderline" | "sfw" | "unknown"
    matched: list[str]
    proposed_tag: str | None  # the _tN to write (or suggested default for an ask); None for leave
    action: str  # "auto_retag" | "ask" | "leave"
    reason: str


def infer_tier_tagged(file_path: str) -> tuple[str, bool]:
    """Extract tier from a filename → (tier, was_tagged).

    breakfast_ethan_t5.webm → ("t5", True); couch_kiss_base.jpg → ("base", True);
    couch_kiss.webm → ("base", False). was_tagged distinguishes an untagged file
    (which silently defaults to base) from one deliberately tagged _base — the whole
    point of the audit, so a forgotten tag can be told apart from an intentional one.
    """
    stem = Path(file_path).stem
    m = re.search(r"_t([0-8])$", stem)
    if m:
        return f"t{m.group(1)}", True
    if stem.endswith("_base"):
        return "base", True
    return "base", False


def infer_tier(file_path: str) -> str:
    """Back-compat wrapper — tier only."""
    return infer_tier_tagged(file_path)[0]


def classify_content_family(description: str, search_queries: list[str]) -> tuple[str, list[str]]:
    """Return (family, matched_keywords) where family is 'static', 'animated', or 'ambiguous'.

    Any animated-keyword hit wins — kiss/tease/nudity/sex scenes need motion to land.
    Static scenes (domestic, conversational, location shots) only classify as static when
    they match static keywords AND don't match any animated keyword.
    """
    blob = " ".join([description] + list(search_queries)).lower()
    animated_hits = sorted({kw for kw in ANIMATED_KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", blob)})
    if animated_hits:
        return "animated", animated_hits
    static_hits = sorted({kw for kw in STATIC_KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", blob)})
    if static_hits:
        return "static", static_hits
    return "ambiguous", []


def check_format_alignment(file_path: str, description: str, search_queries: list[str]) -> FormatCheck:
    """Check that the file extension matches the content family.

    Kiss/tease/nudity/sex scenes written as .jpg → flagged (motion needed).
    Dinner/chores/location scenes written as .webm → flagged (static fine, animation overkill).
    """
    ext = Path(file_path).suffix.lower()
    family, keywords = classify_content_family(description, search_queries)

    if family == "animated" and ext in STATIC_EXTENSIONS:
        return FormatCheck(
            file=file_path,
            current_extension=ext,
            detected_family=family,
            matched_keywords=keywords,
            recommended_extension=".webm",
            passed=False,
            message=f"description/queries suggest motion ({', '.join(keywords[:3])}) but file is {ext} — use .webm or .gif",
        )

    if family == "static" and ext in ANIMATED_EXTENSIONS:
        return FormatCheck(
            file=file_path,
            current_extension=ext,
            detected_family=family,
            matched_keywords=keywords,
            recommended_extension=".jpg",
            passed=False,
            message=f"description suggests static scene ({', '.join(keywords[:3])}) but file is {ext} — use .jpg",
        )

    return FormatCheck(
        file=file_path,
        current_extension=ext,
        detected_family=family,
        matched_keywords=keywords,
        recommended_extension=None,
        passed=True,
        message="format matches content family" if family != "ambiguous" else "content family unclear — format accepted as-is",
    )


def classify_content_rating(description: str, search_queries: list[str]) -> tuple[str, list[str]]:
    """Suggest the SFW/NSFW rating from scene meaning. Returns (signal, matched).

    signal ∈ {hard_nsfw, borderline, sfw, unknown}. This is the ROUTING evidence
    (which pipeline) — separate from classify_content_family (the still-vs-animated
    FORMAT axis). hard_nsfw wins, then borderline, then sfw, else unknown.
    """
    blob = " ".join([description] + list(search_queries)).lower()

    def hits(words: set[str]) -> list[str]:
        return sorted({w for w in words if re.search(rf"\b{re.escape(w)}\b", blob)})

    hard = hits(RATING_HARD_NSFW)
    if hard:
        return "hard_nsfw", hard
    border = hits(RATING_BORDERLINE)
    if border:
        return "borderline", border
    sfw = hits(RATING_SFW)
    if sfw:
        return "sfw", sfw
    return "unknown", []


def propose_tag(file_path: str, tier: str, was_tagged: bool, signal: str,
                matched: list[str], item_type: str | None = None) -> TagProposal:
    """Reconcile the author's tag against the content signal → a retag proposal.

    Content leads the SFW/NSFW routing; the tag grades the heat. Up-grades on explicit
    content are confident (auto); down-grades and all borderline calls are asked (the
    author owns the heat grade). See references/content_rating.md for the full matrix.
    """
    def mk(proposed: str | None, action: str, reason: str) -> TagProposal:
        return TagProposal(file=file_path, current_tag=tier, was_tagged=was_tagged,
                           content_signal=signal, matched=matched,
                           proposed_tag=proposed, action=action, reason=reason)

    if item_type in NON_CANVAS_TYPES:
        return mk(None, "leave", "non-canvas type — always SFW, never retagged")

    cue = ", ".join(matched[:3])
    tag_is_sfw = tier in SFW_TIERS
    tag_is_nsfw = tier in BORDERLINE_TIERS or tier in NSFW_TIERS

    if not was_tagged:
        if signal == "hard_nsfw":
            return mk("t5", "auto_retag", f"untagged but description is explicit ({cue}) → NSFW")
        if signal == "borderline":
            return mk("t4", "ask", f"untagged borderline ({cue}) — confirm heat: t3 peck / t4 makeout / t5+ explicit")
        return mk(None, "leave", "untagged, reads SFW — default base is correct")

    if tag_is_sfw and signal == "hard_nsfw":
        return mk("t5", "auto_retag", f"tagged {tier} (SFW) but description is explicit ({cue}) → NSFW")
    if tag_is_sfw and signal == "borderline":
        return mk("t4", "ask", f"tagged {tier} (SFW) but borderline content ({cue}) — confirm")
    if tag_is_nsfw and signal == "sfw":
        return mk("base", "ask", f"tagged {tier} (NSFW) but content reads vanilla ({cue}) — confirm down-grade")
    return mk(None, "leave", "tag consistent with content")
