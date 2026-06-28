#!/usr/bin/env python3
"""
validate_queries.py — deterministic query validator for find-media

Two input modes, same validation pipeline:

  --from-api-json <path>   (primary) Reads the missing_media array from a JSON
                            file produced by fetching the game-review API
                            endpoint. Handles all 5 media categories: canvas
                            blocks, locations, clothing, phone posts, dating
                            profiles. This is what the skill uses by default.

  --toml <path>             (fallback) Walks a TOML for search_queries. Misses
                            locations, clothing, and phone posts that don't have
                            a search_queries key. Only useful when the Django
                            server is unreachable.

Both modes feed the same validate_query() + check_format_alignment() pipeline,
applying rules from references/query_rewriting.md.

Usage:
    python validate_queries.py --from-api-json <path> [--item <substring>] [--json]
    python validate_queries.py --toml <path> [--item <substring>] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


BANNED_WORDS = {
    "passionate", "tender", "urgent", "loving", "intimate",
    "sensual", "seductive", "emotional", "forbidden",
    "beautiful", "gorgeous", "perfect", "amazing",
}

STORY_FILLERS = {"first time", "secret", "lazy"}

AUTO_REWRITES = {
    "hand job": "handjob",
    "manual stimulation": "__NEEDS_DIRECTION__",
    "oral": "__NEEDS_DIRECTION__",
    "manual": "__NEEDS_DIRECTION__",
}

SOLO_TRAP_ACTIONS = {
    "fingering": "men fingering girl",
    "cunnilingus": "guy eating out girl",
    "eating out": "guy eating out girl",
    "masturbation": "__UNUSABLE_FOR_MF__",
}

SEXUAL_TERMS_FOR_SFW_CHECK = {
    "sex", "fuck", "blowjob", "handjob", "fingering", "cunnilingus",
    "oral", "pussy", "cock", "cum", "creampie", "penetration",
    "missionary", "doggy", "cowgirl",
}

VANILLA_TERMS_FOR_NSFW_CHECK = {
    "romantic", "sweet", "tender", "loving",
}

SFW_TIERS = {"base", "t2", "t3", "location"}
BORDERLINE_TIERS = {"t4"}
NSFW_TIERS = {"t5", "t6", "t7", "t8"}

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
class ValidationResult:
    file: str
    tier: str
    original: str
    rewritten: str | None
    issues: list[str] = field(default_factory=list)
    rules_applied: list[str] = field(default_factory=list)
    tier_check_passed: bool = True
    needs_narrative_context: bool = False


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


def strip_banned(query: str) -> tuple[str, list[str]]:
    """Remove banned words and story fillers. Returns (cleaned, applied_rules)."""
    applied = []
    tokens = query.lower().split()
    kept = []
    for tok in tokens:
        stripped = re.sub(r"[^\w]", "", tok)
        if stripped in BANNED_WORDS:
            applied.append(f"stripped:{stripped}")
            continue
        kept.append(tok)
    # Multi-word fillers
    cleaned = " ".join(kept)
    for phrase in STORY_FILLERS:
        if phrase in cleaned:
            cleaned = cleaned.replace(phrase, "").strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            applied.append(f"stripped:{phrase}")
    return cleaned, applied


def check_gender_direction(query: str) -> tuple[str | None, list[str], bool]:
    """Rewrite solo-trap actions. Returns (rewritten_or_None, rules, needs_narrative)."""
    applied = []
    needs_narrative = False
    lower = query.lower()

    for trigger, replacement in SOLO_TRAP_ACTIONS.items():
        if re.search(rf"\b{re.escape(trigger)}\b", lower):
            if replacement == "__UNUSABLE_FOR_MF__":
                return None, [f"unusable:{trigger}_is_solo_only"], False
            if trigger in lower and replacement not in lower:
                query = re.sub(
                    rf"\b{re.escape(trigger)}\b", replacement, query, flags=re.IGNORECASE
                )
                applied.append(f"gender_direction:{trigger}→{replacement}")

    for trigger, replacement in AUTO_REWRITES.items():
        if re.search(rf"\b{re.escape(trigger)}\b", lower):
            if replacement == "__NEEDS_DIRECTION__":
                needs_narrative = True
                applied.append(f"needs_direction_from_narrative:{trigger}")
            else:
                query = re.sub(
                    rf"\b{re.escape(trigger)}\b", replacement, query, flags=re.IGNORECASE
                )
                applied.append(f"rewrote:{trigger}→{replacement}")

    return query, applied, needs_narrative


def check_tier_alignment(query: str, tier: str) -> tuple[bool, list[str]]:
    """Check query vocabulary against tier. Returns (passed, issues)."""
    issues = []
    lower = query.lower()
    has_sexual = any(re.search(rf"\b{re.escape(t)}\b", lower) for t in SEXUAL_TERMS_FOR_SFW_CHECK)
    has_vanilla = any(re.search(rf"\b{re.escape(t)}\b", lower) for t in VANILLA_TERMS_FOR_NSFW_CHECK)

    if tier in SFW_TIERS and has_sexual:
        issues.append(f"tier_mismatch:sfw_query_has_sexual_term")
    if tier in NSFW_TIERS and not has_sexual and has_vanilla:
        issues.append(f"tier_mismatch:nsfw_query_too_vanilla")

    return len(issues) == 0, issues


def validate_query(original: str, tier: str, file_path: str) -> ValidationResult:
    result = ValidationResult(file=file_path, tier=tier, original=original, rewritten=original)

    cleaned, banned_rules = strip_banned(original)
    result.rules_applied.extend(banned_rules)

    rewritten, gender_rules, needs_narrative = check_gender_direction(cleaned)
    result.rules_applied.extend(gender_rules)
    result.needs_narrative_context = needs_narrative

    if rewritten is None:
        result.rewritten = None
        result.issues.append("unusable_query")
        result.tier_check_passed = False
        return result

    tier_ok, tier_issues = check_tier_alignment(rewritten, tier)
    result.issues.extend(tier_issues)
    result.tier_check_passed = tier_ok

    result.rewritten = rewritten.strip()
    return result


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


def load_items_from_api_json(json_path: Path, item_filter: str | None = None) -> list[dict]:
    """Read missing_media from a JSON file produced by the game-review API.

    Accepts either a bare array [{...}, {...}] or a dict with a "missing_media"
    key (the full load-game response). Normalizes each entry to the internal
    {file, search_queries, description} shape used by the walker, preserving
    type/category/canvas_id as passthrough metadata for downstream consumers.
    """
    with json_path.open() as f:
        data = json.load(f)

    if isinstance(data, dict):
        entries = data.get("missing_media", [])
    elif isinstance(data, list):
        entries = data
    else:
        entries = []

    items = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        file_path = e.get("file") or e.get("image") or ""
        if not file_path:
            continue
        items.append({
            "file": file_path,
            "search_queries": e.get("search_queries") or [],
            "description": e.get("description") or "",
            "type": e.get("type"),
            "category": e.get("category"),
            "canvas_id": e.get("canvas_id"),
        })

    if item_filter:
        items = [i for i in items if item_filter in i["file"]]

    return items


def extract_queries_from_toml(toml_path: Path, item_filter: str | None = None) -> list[dict]:
    with toml_path.open("rb") as f:
        data = tomllib.load(f)

    items = []

    def walk(obj: Any, path_hint: str = ""):
        if isinstance(obj, dict):
            if "search_queries" in obj:
                # Support both "file" (scene blocks) and "image" (phone posts) as path key
                file_key = "file" if "file" in obj else ("image" if "image" in obj else None)
                if file_key:
                    items.append({
                        "file": obj[file_key],
                        "search_queries": obj["search_queries"],
                        "description": obj.get("description") or obj.get("alt") or obj.get("caption", ""),
                    })
                    return
            if "props" in obj and isinstance(obj["props"], dict) and "search_queries" in obj["props"]:
                items.append({
                    "file": obj["props"]["file"],
                    "search_queries": obj["props"]["search_queries"],
                    "description": obj["props"].get("description") or obj["props"].get("alt", ""),
                })
                return
            for v in obj.values():
                walk(v, path_hint)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, path_hint)

    walk(data)

    if item_filter:
        items = [i for i in items if item_filter in i["file"]]

    return items


def main() -> int:
    p = argparse.ArgumentParser()
    input_group = p.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--toml", type=Path, help="Walker mode: parse a TOML for search_queries (fallback; misses non-canvas categories)")
    input_group.add_argument("--from-api-json", type=Path, dest="from_api_json",
                             help="Primary mode: read missing_media from a JSON file produced by the game-review API")
    p.add_argument("--item", default=None, help="Filter to items containing this substring")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of human report")
    args = p.parse_args()

    if args.toml is not None:
        if not args.toml.exists():
            print(f"ERROR: TOML not found: {args.toml}", file=sys.stderr)
            return 2
        items = extract_queries_from_toml(args.toml, args.item)
        source_label = f"TOML {args.toml}"
    else:
        if not args.from_api_json.exists():
            print(f"ERROR: API JSON not found: {args.from_api_json}", file=sys.stderr)
            return 2
        items = load_items_from_api_json(args.from_api_json, args.item)
        source_label = f"API JSON {args.from_api_json}"

    if not items:
        print(f"No media items found in {source_label}.", file=sys.stderr)
        return 0

    all_results: list[ValidationResult] = []
    format_checks: list[FormatCheck] = []
    proposals: list[TagProposal] = []
    for item in items:
        tier, was_tagged = infer_tier_tagged(item["file"])
        for q in item["search_queries"]:
            all_results.append(validate_query(q, tier, item["file"]))
        format_checks.append(
            check_format_alignment(item["file"], item.get("description", ""), item["search_queries"])
        )
        signal, matched = classify_content_rating(item.get("description", ""), item["search_queries"])
        proposals.append(propose_tag(item["file"], tier, was_tagged, signal, matched, item.get("type")))

    flagged = [r for r in all_results if r.needs_narrative_context or r.rewritten is None]
    rewritten = [
        r for r in all_results
        if r.rules_applied and not r.needs_narrative_context and r.rewritten is not None
        and r.rewritten.lower() != r.original.lower()
    ]
    unchanged = [r for r in all_results if not r.rules_applied and r.tier_check_passed]
    tier_issues = [r for r in all_results if not r.tier_check_passed and r.rewritten]
    format_issues = [fc for fc in format_checks if not fc.passed]
    retag_auto = [p for p in proposals if p.action == "auto_retag"]
    retag_ask = [p for p in proposals if p.action == "ask"]

    if args.json:
        print(json.dumps({
            "queries": [asdict(r) for r in all_results],
            "format_checks": [asdict(fc) for fc in format_checks],
            "tag_proposals": [asdict(p) for p in proposals],
        }, indent=2))
        return 0

    print("=== Query Validation Report ===")
    print(f"Checked {len(all_results)} queries across {len(items)} items.\n")

    if flagged:
        print(f"⚠️  FLAGGED ({len(flagged)} queries need narrative-context rewrite):\n")
        for r in flagged:
            status = "UNUSABLE" if r.rewritten is None else "NEEDS NARRATIVE"
            print(f"  [{status}] {r.file} ({r.tier})")
            print(f"    Original: {r.original!r}")
            print(f"    Issues:   {', '.join(r.issues + r.rules_applied)}")
            print()

    if tier_issues:
        print(f"⚠️  TIER MISMATCH ({len(tier_issues)} queries):\n")
        for r in tier_issues:
            print(f"  [{r.tier}] {r.file}")
            print(f"    Query:    {r.rewritten!r}")
            print(f"    Issues:   {', '.join(r.issues)}")
            print()

    if rewritten:
        print(f"✅ AUTO-REWRITTEN ({len(rewritten)} queries):\n")
        for r in rewritten:
            print(f"  {r.file} ({r.tier})")
            print(f"    Original:  {r.original!r}")
            print(f"    Rewritten: {r.rewritten!r}")
            print(f"    Rules:     {', '.join(r.rules_applied)}")
            print()

    if format_issues:
        print(f"⚠️  FORMAT MISMATCH ({len(format_issues)} items — motion vs static):\n")
        for fc in format_issues:
            print(f"  {fc.file}")
            print(f"    Current:     {fc.current_extension}")
            print(f"    Detected:    {fc.detected_family} ({', '.join(fc.matched_keywords[:5])})")
            print(f"    Recommended: {fc.recommended_extension}")
            print(f"    {fc.message}")
            print()

    if retag_auto or retag_ask:
        print(f"⚠️  TIER RETAG ({len(retag_auto)} confident auto, {len(retag_ask)} need your call):\n")
        for p in retag_auto:
            print(f"  [AUTO → _{p.proposed_tag}] {p.file}")
            print(f"    {p.reason}")
        for p in retag_ask:
            print(f"  [ASK  → suggest _{p.proposed_tag}] {p.file}")
            print(f"    {p.reason}")
        print()

    print(f"✅ OK: {len(unchanged)} queries pass without changes.")
    print(f"   Format OK: {sum(1 for fc in format_checks if fc.passed)}/{len(format_checks)} items.")

    return 1 if flagged or tier_issues or format_issues or retag_auto or retag_ask else 0


if __name__ == "__main__":
    sys.exit(main())
