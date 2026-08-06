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

Query dialect is SOURCE-SPECIFIC, so rewriting is gated behind --target:

  google (default)  Natural language and loose grammar are fine — a 7-token query
                    works. What breaks Google is CHARACTER/STORY words: they flip the
                    intent classifier and the whole query reclassifies as mainstream.
  pornhub           Compound queries dilute: rare words get silently dropped, and 4+
                    tokens can return literally 0 results. Flowery adjectives are dead
                    weight and get stripped.

The route-neutral half — what the scene IS (motion vs still, SFW vs NSFW, the _tN tag)
— lives in scene_semantics.py and is re-exported here for existing callers.

Usage:
    python validate_queries.py --from-api-json <path> [--target google|pornhub] [--item <substring>] [--json]
    python validate_queries.py --toml <path> [--target google|pornhub] [--item <substring>] [--json]

Exit codes:
    0  nothing needs attention
    1  something was flagged, rewritten, mis-formatted, or wants a retag (JSON mode too)
    2  invalid arguments / input file missing
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

# scene_semantics.py sits beside this file. Running by path already puts scripts/ on
# sys.path; importing validate_queries from anywhere else does not — so anchor it.
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Imported wholesale and RE-EXPORTED on purpose: SKILL.md, content_rating.md and
# apply_retags.py all reach for these through validate_queries, so the split must not
# move a name out from under an existing caller. Hence the unused-import waiver.
from scene_semantics import (  # noqa: E402,F401
    ACT_ANCHORS,
    ANIMATED_EXTENSIONS,
    ANIMATED_KEYWORDS,
    BORDERLINE_TIERS,
    NON_CANVAS_TYPES,
    NSFW_TIERS,
    RATING_BORDERLINE,
    RATING_HARD_NSFW,
    RATING_NUDITY,
    RATING_SFW,
    SEXUAL_TERMS_FOR_SFW_CHECK,
    SFW_TIERS,
    STATIC_EXTENSIONS,
    STATIC_KEYWORDS,
    FormatCheck,
    TagProposal,
    check_format_alignment,
    classify_content_family,
    classify_content_rating,
    infer_tier,
    infer_tier_tagged,
    propose_tag,
)

TARGETS = ("google", "pornhub")
DEFAULT_TARGET = "google"

# --- PornHub dialect ---------------------------------------------------------
# PornHub matches TAGS. A flowery adjective is a token that matches no tag, and every
# extra token narrows the result set — a 4+ token query can return literally 0.
BANNED_WORDS = {
    "passionate", "tender", "urgent", "loving", "intimate",
    "sensual", "seductive", "emotional", "forbidden",
    "beautiful", "gorgeous", "perfect", "amazing",
}

STORY_FILLERS = {"first time", "secret", "lazy"}

# --- Google dialect ----------------------------------------------------------
# Google does NOT mind adjectives or length; it minds INTENT. Measured: the query
# `back alley blowjob gif drunk guy night` came back Reddit movie stills, Facebook and
# TikTok — "drunk guy" alone reclassified a working porn query as mainstream. So the
# harmful tokens here are character-STATE words, the opposite of the PornHub list.
# Extrapolated from that one measurement, so kept to affect/state words that no porn
# taxonomy uses as a category name. `sleeping`, `asleep` and `unconscious` are
# DELIBERATELY absent: those ARE canonical category tags, so on Google they read as
# porn intent, not story intent — the exact opposite of "drunk guy".
GOOGLE_STORY_WORDS = {
    "drunk", "wasted", "tipsy", "hungover",
    "angry", "nervous", "scared", "crying", "sad", "shy", "embarrassed",
    "reluctant", "unwilling", "hesitant", "exhausted", "tired",
}
# Multi-word equivalents, stripped as phrases.
GOOGLE_STORY_PHRASES = {"passed out", "first time"}
# NOT stripped on Google: setting words. A dark alley or a grimy back room is often the
# only token carrying the beat's danger or squalor, and the user has rejected bright
# clips twice on exactly that ground. Anti-studio modifiers (amateur / real / voyeur /
# hidden cam) are ADDITIONS the author makes, not something to strip.

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

VANILLA_TERMS_FOR_NSFW_CHECK = {
    "romantic", "sweet", "tender", "loving",
    # media_lab_f 2026-08-05: these four rode along beside a hard act anchor and still
    # dragged the results to the romance/stock cluster (facial slot: 17% on-act vs the
    # act-first control's 50%, 45 Dreamstime stills vs 0).
    "gentle", "intimate", "passionate", "sensual",
}


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
    target: str = DEFAULT_TARGET  # which dialect the rewrite was made for


def _strip_words(query: str, words: set[str], phrases: set[str]) -> tuple[str, list[str]]:
    """Drop whole-token words and multi-word phrases. Returns (cleaned, applied_rules)."""
    applied = []
    kept = []
    for tok in query.lower().split():
        stripped = re.sub(r"[^\w]", "", tok)
        if stripped in words:
            applied.append(f"stripped:{stripped}")
            continue
        kept.append(tok)
    cleaned = " ".join(kept)
    for phrase in phrases:
        # Word-bounded, not a raw substring replace: `"secret"` in STORY_FILLERS used to
        # eat the middle of "secretary" and ship the query as "ary hand on man crotch".
        pattern = rf"\b{re.escape(phrase)}\b"
        if re.search(pattern, cleaned):
            cleaned = re.sub(r"\s+", " ", re.sub(pattern, "", cleaned)).strip()
            applied.append(f"stripped:{phrase}")
    return cleaned, applied


def strip_banned(query: str) -> tuple[str, list[str]]:
    """PornHub dialect: remove flowery adjectives and story fillers.

    Deliberately NOT applied on Google, where "passionate" costs nothing and the
    aggressive strip only threw away tokens that were doing no harm.
    """
    return _strip_words(query, BANNED_WORDS, STORY_FILLERS)


def strip_story_words(query: str) -> tuple[str, list[str]]:
    """Google dialect: remove character-STATE words that flip the intent classifier."""
    return _strip_words(query, GOOGLE_STORY_WORDS, GOOGLE_STORY_PHRASES)


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
    has_act_anchor = any(re.search(rf"\b{re.escape(t)}\b", lower) for t in ACT_ANCHORS)

    if tier in SFW_TIERS and has_sexual:
        issues.append("tier_mismatch:sfw_query_has_sexual_term")
    # For the vanilla branches, "has an act word" must consult BOTH lists: `cumshot`, `bj`,
    # `anal`, `deepthroat` live only in ACT_ANCHORS, so has_sexual alone calls a
    # cumshot query act-less. (has_sexual keeps its original narrow job in the SFW branch
    # above: `cowgirl` leaking into a t2 slot must still flag, and cowgirl is
    # deliberately not an anchor.)
    has_any_act = has_sexual or has_act_anchor

    if tier in NSFW_TIERS and not has_any_act and has_vanilla:
        issues.append("tier_mismatch:nsfw_query_too_vanilla")

    # A mood word BESIDE an act word is not saved by the act word — Google weights every
    # token, and the vanilla ones have a vastly larger SFW cluster to fall into. Measured
    # on media_lab_f (2026-08-05): `passionate real couple cumshot gif` passed this
    # validator clean and shelved romance couples at a 17% on-act rate (45 Dreamstime
    # stills; the act-first control ran 50%). Distinct issue string on purpose:
    # too_vanilla = no act word at all; dilution = act word present but outvoted.
    if tier in NSFW_TIERS and has_any_act and has_vanilla:
        issues.append("vanilla_dilution:mood_words_pull_stock_results")

    # An NSFW query with no ACT word does not reach porn at all — it gets classified as a
    # mainstream search and returns stock photography. Position names do not save it: they are
    # ordinary English, which is exactly why ACT_ANCHORS excludes them. Note this fires
    # INDEPENDENTLY of has_sexual, because has_sexual is true for `cowgirl` and that is the
    # case that went undetected (measured: 0 of 83 results on a porn host).
    # Deliberately NSFW_TIERS only — t4 is BORDERLINE and a tease beat must never be forced to
    # carry a penetrative word.
    if tier in NSFW_TIERS and not has_act_anchor:
        issues.append("no_act_anchor:position_or_setting_words_only")

    return len(issues) == 0, issues


def validate_query(original: str, tier: str, file_path: str,
                   target: str = DEFAULT_TARGET) -> ValidationResult:
    """Rewrite one query for one retrieval target.

    Only the WORD-STRIPPING half is target-dependent — the two surfaces punish opposite
    vocabularies. check_gender_direction runs on both: "fingering" and "cunnilingus"
    return solo-female results on any surface, and "oral"/"manual" are directionless
    on any surface, so those fixes are about the ACT, not the search engine.
    """
    result = ValidationResult(file=file_path, tier=tier, original=original,
                              rewritten=original, target=target)

    strip = strip_banned if target == "pornhub" else strip_story_words
    cleaned, strip_rules = strip(original)
    result.rules_applied.extend(strip_rules)

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
                props = obj["props"]
                # A POOL block declares `pool_dir` (a folder) and has NO `file` key at all.
                # This used to be a bare props["file"] lookup, which raised KeyError and killed
                # the whole --toml walk on the first pool it met — so a game that had converted
                # any slot to a pool could not be offline-validated at all. Precedence matches
                # apps/common/media_blocks.py: pool_dir > files > file.
                path = props.get("pool_dir") or props.get("file") or props.get("image")
                if not path:
                    files = props.get("files")
                    if isinstance(files, list) and files:
                        path = files[0]
                if not path:
                    return
                items.append({
                    "file": path,
                    "search_queries": props["search_queries"],
                    "description": props.get("description") or props.get("alt", ""),
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
    p.add_argument("--target", choices=TARGETS, default=DEFAULT_TARGET,
                   help=f"Retrieval surface the queries are written for (default: {DEFAULT_TARGET})")
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
            all_results.append(validate_query(q, tier, item["file"], args.target))
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

    # Computed ONCE, before the output branch. JSON mode used to hardcode `return 0`,
    # so any orchestration that checked the exit code got a green light no matter what
    # the payload said — the whole signal was discarded in the one mode a script reads.
    exit_code = 1 if flagged or tier_issues or format_issues or retag_auto or retag_ask else 0

    if args.json:
        print(json.dumps({
            "target": args.target,
            "exit_code": exit_code,
            "queries": [asdict(r) for r in all_results],
            "format_checks": [asdict(fc) for fc in format_checks],
            "tag_proposals": [asdict(p) for p in proposals],
        }, indent=2))
        return exit_code

    print("=== Query Validation Report ===")
    print(f"Checked {len(all_results)} queries across {len(items)} items "
          f"(target: {args.target}).\n")

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

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
