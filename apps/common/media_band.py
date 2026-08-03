"""Shared content-band classifier for one media slot — SFW vs NSFW, and why.

**There is no band in the corpus.** A repo-wide scan finds zero `tier =` keys in any
game TOML; the tier lives only in a *filename convention* (`sex/renner_loop_oral_t5`).
So every band this module returns is DERIVED, and the caller is told which evidence
produced it via `band_source` — a filter that quietly guesses is worse than no filter,
because being mostly right is exactly what teaches you to trust it.

Bands, ordered hottest first:

    explicit    a sex act is depicted
    nudity      bare body, no act
    borderline  underwear, tease, suggestive — anything on the sexual ladder
    clean       everything else

`explicit`, `nudity` and `borderline` are all NSFW; only `clean` is SFW. The three-way
split above the line exists so a card can show what it actually is while the filter
still offers the two buckets a human asks for.

**A tease is never SFW** (LO, 2026-08-04). A tier suffix of any kind — t2 through t8 —
means the author placed that beat on the sexual ladder, so it lands in `borderline` at
the coolest. See the note on `TIER_BAND` for why this deliberately diverges from
find-media's `SFW_TIERS`.

**Evidence precedence**, strongest first — the first rule that fires wins:

    authored        an explicit `tier` on the block          (nothing uses this yet)
    tier_suffix     `_t5` in the declared path
    folder          the slot lives under `sex/`
    portrait_state  a player-portrait state key (`naked_image`)
    description     a cue word in the description or search queries
    default         clean

Path evidence outranks description evidence on purpose: a file under `sex/` is
explicit whatever its caption says, and captions are the weakest signal we have.

**Why the cue lists are short and phrase-heavy.** A first pass over vesper with a
loose word list produced two false positives that read as comedy but would have been
real mislabels: `kess_berth_intro` ("a **stripped** hull behind him") and
`salvage_waterfront_dawn` ("down on one **knee**"). Everything here is matched on word
boundaries for the same reason — `\bcock\b` must not fire on "leaning **cocky**", and
`\banal\b` must not fire on "junior-**analyst** kit", which is a real vesper cover story.

Measured against vesper's 216 slots, the rules below place all 22 that a naive
path-only rule sends to the SFW bucket — including the six `cell_*` captivity clips.
See `tests/test_media_band.py`, which pins those by name.
"""
import re
from typing import Any, Dict, Iterable, Optional, Tuple

# Hottest first. Also the tie-break order when two cue lists both match.
BANDS = ("explicit", "nudity", "borderline", "clean")
NSFW_BANDS = ("explicit", "nudity", "borderline")

# The tier vocabulary, mapped onto the bands above. A literal map rather than a numeric
# comparison so the non-numeric tiers ("base", "location") have somewhere to land.
#
# ⚠️ This DIVERGES from find-media's `SFW_TIERS`
# (.claude/skills/find-media/scripts/scene_semantics.py:28-30), which puts t2 and t3 in the
# SFW set. LO's ruling, 2026-08-04: **a tease is never SFW.** Any authored tier suffix means
# the author put the beat on the sexual ladder; only `base` / `location` / no suffix is clean.
#
# The skill's set was written as if SFW meant *wayfinding* — a location or establishing shot
# the player reads to know where they are. A t2 tease on a permanent hub rung is nothing like
# a room shot: vesper's `rung_renner_tease_t2` sits on a repeatable hub gated `corruption >= 0`
# with no upper bound, so it is clickable from the first minute to the last. Calling that SFW
# is what let it ship as a single unrotated clip.
#
# `scene_semantics.py` is the other half of this fix and is not yet updated — until it is,
# find-media will still route t2/t3 searches as SFW. See the plan's Part 3.
TIER_BAND = {
    "base": "clean", "location": "clean",
    "t2": "borderline", "t3": "borderline", "t4": "borderline",
    "t5": "explicit", "t6": "explicit", "t7": "explicit", "t8": "explicit",
}

# A tier suffix on the declared path: `sex/x_t5.webm`, or a pool dir ending AT the
# tier (`sex/brothel_oral_t5`) — hence the end-of-string alternative.
_TIER_SUFFIX_RE = re.compile(r"_t([2-8])(?:[._/]|$)")

# The folder that is explicit by construction, whatever any caption claims.
_EXPLICIT_ROOT = "sex"

# Player-portrait state keys. The engine already parses these (`naked_image`,
# `topless_image`, ...), so their band is structural, not a guess — no authoring
# needed. This also overrides game_review.py's standing comment that portraits are
# "always SFW regardless of how explicit the game is", which is false for any game
# whose player portrait undresses.
PORTRAIT_STATE_BAND = {
    "naked": "nudity", "nude": "nudity",
    "topless": "nudity", "bottomless": "nudity",
    "underwear": "borderline", "lingerie": "borderline",
}

# Phrases that mean a sex act with no innocent reading in this corpus. Multi-word
# entries are here because the single words they contain are NOT safe alone: "used"
# and "line" and "turn" all appear in ordinary industrial captions.
_EXPLICIT_CUES = (
    "fuck", "fucked", "fucking", "fucks", "blowjob", "handjob", "rimjob",
    "cunnilingus", "creampie", "gangbang", "bukkake",
    "cum", "cumshot", "cumming", "facial", "semen", "ejaculate", "ejaculating",
    "cock", "cunt", "pussy", "anal", "vaginal", "doggy", "missionary", "cowgirl",
    "penetration", "penetrated", "penetrating", "double penetration", "orgasm",
    "being used", "used by", "used from behind", "still being used",
    "used on the floor", "passed down the line", "line of men", "group of men",
    "her throat", "takes her ass", "legs held open", "strip on command",
    "waiting their turn", "pissed on", "from-behind",
)

# Bare body, no act.
_NUDITY_CUES = (
    "naked", "nude", "fully nude", "topless", "bottomless",
    "bare breasts", "bare tits", "undressed",
)

# Underwear and suggestive-but-clothed.
_BORDERLINE_CUES = (
    "lingerie", "underwear", "panties", "bra", "cleavage", "makeout", "straddling",
)


def _norm(path: str) -> str:
    """Declared paths appear both bare (`sex/x.webm`) and prefixed (`videos/sex/x.webm`).

    `file` is bare and `serve_path` is prefixed, and mixing the two forms in one test
    is a live footgun: a `"/sex/" in path` check silently misses every bare path.
    Normalise to the bare form before any structural test.
    """
    p = (path or "").replace("\\", "/").strip().lstrip("/")
    return p[len("videos/"):] if p.startswith("videos/") else p


def _cue_hit(text: str, cues: Iterable[str]) -> Optional[str]:
    """First cue present in `text` on word boundaries, else None.

    Word boundaries are load-bearing, not tidiness: `anal` inside "analyst" and `cock`
    inside "cocky" both occur in shipped vesper captions.
    """
    for cue in cues:
        if re.search(r"\b" + re.escape(cue) + r"\b", text):
            return cue
    return None


def band_for(
    path: str,
    *,
    tier: Optional[str] = None,
    description: str = "",
    search_queries: Iterable[str] = (),
    portrait_state: Optional[str] = None,
) -> Tuple[str, str]:
    """Classify one media slot. Returns ``(band, band_source)``.

    `band_source` names the evidence, so a UI can show that a `description`-derived
    band is weaker than an `authored` one instead of presenting both as fact.
    """
    if tier:
        mapped = TIER_BAND.get(str(tier).strip().lower())
        if mapped:
            return mapped, "authored"

    rel = _norm(path)

    m = _TIER_SUFFIX_RE.search(rel)
    if m:
        return TIER_BAND["t" + m.group(1)], "tier_suffix"

    if rel.split("/", 1)[0] == _EXPLICIT_ROOT:
        return "explicit", "folder"

    if portrait_state:
        mapped = PORTRAIT_STATE_BAND.get(str(portrait_state).strip().lower())
        if mapped:
            return mapped, "portrait_state"

    text = " ".join([description or ""] + [q for q in (search_queries or []) if q]).lower()
    if text:
        # Hottest-first: a caption naming both an act and nudity is explicit.
        if _cue_hit(text, _EXPLICIT_CUES):
            return "explicit", "description"
        if _cue_hit(text, _NUDITY_CUES):
            return "nudity", "description"
        if _cue_hit(text, _BORDERLINE_CUES):
            return "borderline", "description"

    return "clean", "default"


def band_for_entry(entry: Dict[str, Any]) -> Tuple[str, str]:
    """`band_for` over an enumerator entry, reading the fields it already carries."""
    return band_for(
        entry.get("file", ""),
        tier=entry.get("tier"),
        description=entry.get("description", ""),
        search_queries=entry.get("search_queries") or (),
        portrait_state=entry.get("portrait_state"),
    )


def is_nsfw(band: str) -> bool:
    return band in NSFW_BANDS
