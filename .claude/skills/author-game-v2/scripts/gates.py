#!/usr/bin/env python3
"""
gates.py — the author-game-v2 scoreboard.

Measures a built game against the ship gates. Nothing here is inherited opinion;
see THRESHOLDS below for the evidence behind each number.

Two measurement bases, and they are NOT interchangeable:

  1. Gates 1-10 were derived from Degrees of Lewdity's own source across ten
     snapshots, 2018-11 to 2026-07 (25 -> 61 locations, 1.7k -> 15.6k units,
     254k -> 2.24M words).
  2. Gates 11-19 (2026-08-12) were derived from a FIELD of 18 shipped browser
     sandboxes, ~62,000 passages, because a doctrine measured from one game
     cannot contain anything that game lacks. The game this skill built with
     basis (1) shipped 10/10 with no street, no guidance page, and an economy
     where money was unbounded — every one of those invisible to gates 1-10.

Usage:
    python3 gates.py <game-slug>            # resolves games/<slug>/toml_phases/7_final_game.toml
    python3 gates.py <path/to/game.toml>
    python3 gates.py <slug> --json          # machine-readable
    python3 gates.py --words <path>         # the vocabulary lint on ANY text file,
                                            #   for the WANT and BOARD phases, before
                                            #   a game exists to measure

Why a real TOML parser and not grep: an earlier grep-based pass on this same file
silently missed 24 `is_repeatable` lines (whitespace-aligned and unspaced variants)
and produced a 33%-repeatable figure when the truth is the majority. Parse, never grep.
"""

import sys
import os
import re
import json
import math
import collections

try:
    import tomllib as _toml          # py3.11+
    def _load(p): return _toml.load(open(p, "rb"))
except ImportError:
    import tomli as _toml            # py3.10 fallback
    def _load(p): return _toml.load(open(p, "rb"))


# ─────────────────────────────────────────────────────────────────────────────
# THRESHOLDS — each with the measurement it came from
# ─────────────────────────────────────────────────────────────────────────────
# ── Location fill: a DISTRIBUTION, not a floor ──────────────────────────────
# CORRECTED 2026-08-10. This gate first demanded >=10,000 words in EVERY location,
# from a "10,187 words per location" figure. That figure was wrong: the numerator
# included base-combat and base-system — engine code, not location prose. Measured
# on location prose only, DoL's seed is 116,540 words over 25 locations:
#   mean 4,661 · median 3,154 · min 302 (bus station) · max 35,218 (school)
#   -> 24 of its 25 locations are UNDER 10,000. The exemplar failed its own gate.
# The real shape is one or two deep ANCHORS plus many legitimately thin satellites:
# `school` alone held 30.2% of all location prose at seed.
#
# ⚠️ THESE THREE ARE A BACKSTOP, NOT THE CHECK — corrected 2026-08-15, study 6.
# When `v2_state.json` declares `board.locations[].fill`, gate 1 checks each location
# against ITS OWN declared budget and these constants are not consulted. They run only
# for a game with no ledger.
#
# Why: measured across all three v2 games, they were being treated as targets. Two of
# the three landed within FOUR WORDS of MEAN_LOCATION_WORDS (4,504 / 4,502 / 4,681), and
# all three shipped exactly 8 locations against a "6-8" range the doctrine had already
# flagged, in prose, as a judgement rather than evidence. A global constant can be
# satisfied by generating N things; a number checked against the author's own declaration
# cannot, because moving it means changing the design. See SKILL.md:107.
ANCHOR_SHARE_PCT      = 25.0    # DoL seed: school = 35,218 / 116,540 = 30.2%
MEDIAN_LOCATION_WORDS = 3_000   # DoL seed median 3,154
MEAN_LOCATION_WORDS   = 4_500   # DoL seed mean 4,661

DECLARED_FILL_TOLERANCE = 0.25
# ⚠️ THIS IS THE ONE INVENTED NUMBER IN THIS FILE. Say so plainly: it comes from no
# measurement, because none exists — nobody publishes their word budgets.
#
# It is defensible here for a reason that did NOT hold for the two thresholds this project
# had to demote (the-surfaces.md R5/R6): those had to discriminate BETWEEN GAMES, so an
# invented value scored noise and failed correct work. This one compares a game against
# ITSELF, so it only has to be loose enough not to police normal variance while still
# catching a room declared at 4,000 and delivered at 400. Any value in 0.2-0.4 does that job
# identically, which is the signature of a number that is not carrying the decision.
#
# If it ever starts failing games that look right, it is wrong and should be widened, not
# defended.

EXPLICIT_BEAT_FLOOR = 7.5
# Share of beats carrying 3+ explicit words. DoL held 7.5%-9.3% across eight
# years and 12x growth. Unlike raw sex-word share (which fell 3.00% -> 0.96% as
# systems and UI outgrew prose), this ratio is stable, so it is the usable floor.
# It is also robust to word-list choice: two different lists both put DoL at
# 8-10% and Vesper at ~2%.
#
# ⚠️ THIS IS A FLOOR. ITS UPPER COMPARISON IS MEANINGLESS. Do not read a game
# scoring far above it as "too hot" — that reading has now been wrong twice, and
# cost one game a dilution pass it never needed. Two independent reasons:
#
#   1. DIFFERENT DENOMINATORS. The 7.5-9.3% band is per DoL *unit* = a passage in
#      the whole source, combat/systems/UI included: its file carries 15,587
#      <tw-passagedata> entries, matching the "15.6k units" this header cites.
#      THIS gate counts beats in LOCATION PROSE ONLY. Not the same scale.
#   2. THE REFERENCE IS THE COLDEST GAME IN ITS OWN GENRE. Measured 2026-08-12
#      across 18 shipped sandboxes on this exact regex: field median 33.3% of
#      prose passages carry 3+, and DoL is LAST at 7.5%. The floor is a property
#      of DoL, not of the genre.
#
# Valid as a floor and still discriminating (the measured-cold game scores 4.7%).
# Invalid as anything resembling a target.

MENU_CEILING = 8
# Choices on a single repeatable, location-bound canvas. Measured 2026-08-12 across
# 18 shipped sandboxes, counting player-facing links per non-system screen:
#   median screen = 2 links · median p90 = 4 · ~2% of screens exceed 12
# So 8 is already double the field's ninetieth percentile.
#
# Big screens DO exist in real games — the reference game runs 2.9% of its screens
# above 20 links — but they are CATALOGUES: shops, wardrobes, character creation.
# A place the player returns to daily is not a catalogue. The game that prompted
# this put 23 choices on its front desk, 11 of them purchases, next to "Look up at
# the board", and scored 18/18 while doing it. references/the-surfaces.md.

SENTENCE_CEILING = 14
# Median sentence length, in words, across all authored beats. The first threshold
# here that measures WRITING rather than structure. Measured 2026-08-12 over 18
# shipped sandboxes: field median 10 words, DoL 9, and the game that prompted this
# ran 16 — third longest of the eighteen.
#
# ⚠️ TWO INSTRUMENTS, AND THE THRESHOLD SPANS THEM. The field figures come from
# parsing BUILT HTML (the only form a shipped game is available in). This gate reads
# AUTHORED BEAT TEXT from the TOML, which excludes the UI and system strings that
# survive HTML extraction. The same game measures 16 on the first instrument and 13
# on this one, so 14 is calibrated across a seam, not within one basis. It is
# therefore APPROXIMATE — it will catch prose drifting denser, but do not read a
# pass as "matches the field". Tightening it needs the field re-measured on TOML,
# which is not obtainable: we do not have anyone else's source.

EXPLICIT_IN_REPEATABLE = 50.0
# Explicit prose must live where the player returns. Measured failure case:
# 95% of Vesper's explicit beats sit in a sealed room with no exits, while all
# nine of its repeatable sex loops score zero.

EXPLICIT_BEAT_MEDIA_FLOOR = 50.0
# Share of EXPLICIT beats (3+ frozen-list words) that carry a media block OF THEIR
# OWN. Measured 2026-08-18 across 25 mopoga sandboxes, one rendered path per
# passage (branches collapsed — see the note under NARRATION_DIALOGUE_CEILING).
# Re-checked on all 27 parseable games 2026-08-24: the per-screen share moved UP and
# the words-per-clip figure held, so the floor stays generous. Unchanged:
#
#   a screen carrying explicit prose ......... 91% carry media, median 3 clips
#   one clip every ........................... 58 prose words (IQR 25-104, n=25,502)
#   an IN-PASSAGE REVEAL — the exact analogue
#   of one cascade beat ...................... 58% carry their own clip (n=3,005,
#                                              median 37 words per reveal)
#
# ⚠️ WHY THE BEAT AND NOT THE CANVAS. A cascade renders as nested <<linkreplace>>
# (v2.py:13952 — the beat's blocks are emitted INSIDE the linkreplace body), so
# every beat APPENDS below the last and nothing is ever removed. A clip at the top
# of a canvas is therefore a clip for beat 0 only; by the beat that is the act it
# has scrolled away. Node routing is the opposite — it resolves to a real passage
# at BUILD time (v2.py:13258) and SWAPS the screen, which is why the field's
# act-menu loops never go stale.
#
# Measured on our own games: media sits on NODES (20-54% of them) and essentially
# never on beats — vesper 16 of 389, and 0 of 169/623/938/516/39 in the five v2
# games — while v2 games moved nearly all content INTO beats (forty_miles: 938
# beats against 259 nodes).
#
# 50% is half the field's per-screen figure and below its per-reveal figure, so it
# is generous on both instruments. references/register.md.

NARRATION_DIALOGUE_CEILING = 5.0
# Whole-game narration words : dialogue words. Field median 2.93:1, and 10 of 27
# games sit at or under 2:1. 5.0 is above the median and above 18 of the 27, so it
# is slack rather than an invented line;
#
# ⚠️ DENOMINATOR ONLY. Re-checked 2026-08-24 against the two games that used to parse
# to zero: both are narration-heavy (college-daze 5.9:1, free-cities 9.7:1) and both
# sit ABOVE the ceiling, so neither count moved — 10 of 25 became 10 of 27 and 18 of
# 25 became 18 of 27. The median moves by +0.03 on a rebuilt instrument that does not
# reproduce the shipped absolutes and is used only for movement.
# the six games above it are the low-n and
# simulation-heavy outliers (new_life_project 103:1 is a location-description
# sandbox with almost no characters).
#
# ⚠️ THIS RULE WAS ONCE DELETED BY A BROKEN INSTRUMENT, AND THAT IS THE REASON THE
# CONSTANT CARRIES ITS OWN PROVENANCE. DOCTRINE_GAPS Study 4 measured the field by
# counting text inside "quote marks" and reported a median of 33:1 and a spread
# "too wide to threshold"; register.md then dropped v1's dialogue rule on that
# basis. But 20 of the 27 games render speech as a UI COMPONENT — <<speech>>,
# <<say>>, <<nm "Karlee" "...">>, <<chat portrait "...">>, <div class="npctextbox">,
# or one macro per character (<<Mc>>, <<AmyBd>>) — and a quote-counter sees none of
# it. Re-measured with each game's own convention read out of its source first:
#
#   game                 quotes only    + its own speech UI
#   corpo-life               584.9:1               0.30:1
#   sluttown-usa             762.0:1               0.63:1
#   family-business            >999:1               1.15:1
#   destroyer                 71.7:1               1.44:1
#   the-company              290.1:1               2.69:1
#   degrees-of-lewdity         3.6:1               3.62:1   <- unchanged
#   course-of-temptation       4.6:1               4.57:1   <- unchanged
#   patriarch                  2.9:1               2.93:1   <- unchanged
#   MEDIAN                    65.3:1               2.93:1
#   at <=2:1                        0             10 of 27
#
# The three that do not move are the three that punctuate speech with quote marks.
# The study did not find the two most dialogue-heavy games; it found the two whose
# dialogue its instrument could see. The "over 400:1" outlier that killed the rule
# is corpo-life, which is 70% spoken.

LOCATIONS_WITH_HEAT = 60.0
# Share of locations that must carry erotic content. NOT 100%: DoL's seed build
# had sexual passages in 17 of 25 locations (68%) — a police station and a museum
# are allowed to be cold. 60% is that measurement with a little slack.

ASCENT_TIERS = 3
# How many top-gated meters are judged as ascent. Measured in DoL's seed: it runs
# THREE ratcheting tiers, not one axis — promiscuity (22 raises / 1 lower, 206 gate
# sites), deviancy (20/0, 129), exhibitionism (12/1, 167) — each naming a different
# kind of going-further, each gating at 15/35/55/75, plus a `purity` counterweight.
# Volatile state (arousal: 277 sets, moves both ways) is NOT ascent and is expected
# to rank below them.
# ⚠️ n = 1, and the corpus does not repeat it (2026-08-19): of 27 parseable sandboxes,
# FIFTEEN have no player ascent tier at all and only two carry three or more.
# (Fourteen of 25 until the 2026-08-24 recheck: `college-daze` runs four meters PER
# CHARACTER and no player spine, `free-cities` carries `rep` at 17 rungs.) This
# constant is a fallback for guessing when `board.ascent_tiers` is absent — it is not
# a target, and 15/35/55/75 is one game's spacing, not a ladder to copy. Which meters
# a game should have at all is `the-meters.md` W1; gate 34 checks it against
# `board.who_climbs`.

# Engine fact, verified firsthand at:
#   apps/game_generation/twee_comprehensive/generators/v2.py:10937
#   apps/game_generation/twee_comprehensive/generators/v2.py:11010
#   apps/stories/models.py:355  (models.BooleanField(default=True))
# An ABSENT is_repeatable means REPEATABLE. Assuming false here is the single
# easiest way to mis-measure a game.
IS_REPEATABLE_DEFAULT = True

# Frozen explicit-word list. Frozen on purpose: the absolute share swings ~3x
# with list choice, so a floating list makes runs incomparable. Change it only
# with a version bump and a re-baseline of every game.
EXPLICIT = re.compile(
    r"\b(cock|dick|penis|cunt|puss|clit|tits?\b|breast|nipple|ass\b|arse|anal|balls"
    r"|fuck|suck|blowjob|handjob|cum|semen|orgasm|moan|naked|nude|undress|horny"
    r"|arous|lust|lewd|slut|whore|thrust|penetrat|grope|erect|masturbat|vagina"
    r"|kiss|lick)", re.I)

# The ladder a sexual scene climbs, lowest rung first. Used by a LINT ONLY, and
# deliberately: naming an act is not the same as depicting it, and no threshold on
# word-presence would survive contact. It exists to print WHERE a game's scenes sit,
# because both failure directions are real and they look nothing alike —
#   vesper       opens at vaginal-or-finish in 68% of its explicit canvases, median
#                4 rungs in ONE canvas: the whole ladder with no stairs to it
#   forty_miles  76% of 49 explicit canvases never pass hands or stripping: all
#                stairs and no ceiling
# Field, per screen: touch 13 · strip 15 · hands 11 · oral 14 · vaginal 28 · anal 5
# · finish 13 — spread evenly, because a field scene is ONE rung and the ladder is
# climbed across 3-4 chained screens. references/register.md.
RUNGS = (
    ("touch",   re.compile(r"\b(kiss(?:e[sd]|ing)?|caress|fondl|nuzzl|grope"
                           r"|touch(?:es|ed|ing)?)\b", re.I)),
    ("strip",   re.compile(r"\b(undress|strip(?:s|ped|ping)?|naked|nude|topless|bra\b"
                           r"|panties|knickers|unbutton|unzip)\b", re.I)),
    ("hands",   re.compile(r"\b(finger(?:s|ed|ing)?|handjob|hand job|jerk(?:s|ed|ing)?|wank"
                           r"|stroke[sd]? (?:his|her)|rub(?:s|bed|bing)?)\b", re.I)),
    ("oral",    re.compile(r"\b(suck(?:s|ed|ing)?|blowjob|blow job|lick(?:s|ed|ing)?"
                           r"|oral|deepthroat)\b", re.I)),
    ("vaginal", re.compile(r"\b(fuck(?:s|ed|ing)?|thrust|penetrat\w*|rides? (?:him|his)"
                           r"|inside her|in her cunt|in her puss\w*)\b", re.I)),
    ("anal",    re.compile(r"\b(anal|in the ass|her ass\b|your ass\b|butthole)\b", re.I)),
    ("finish",  re.compile(r"\b(cum(?:s|ming)?|came|orgasm\w*|climax\w*|creampie)\b", re.I)),
)
# ⚠️ THE RUNG IS AN ACT, NOT A BODY PART. `cunt` / `puss` / `tits` name anatomy and
# say nothing about what is happening to it — a first draft of this list had them in
# the `vaginal` rung and reported forty_miles as 71% opening at penetration when the
# measured figure is 9%. Every entry above is a verb or a verb phrase, and the field
# distribution quoted in the lint was produced by exactly this list.
RUNG_ORDER = [k for k, _ in RUNGS]

PROSE_BLOCKS = {"paragraph", "dialog", "thought_bubble", "quote", "note"}
MEDIA_BLOCKS = {"image", "video"}
EXPLICIT_MEDIA = re.compile(r"_t[45]\b|/sex/|^sex/", re.I)

# Parts of a building the prose can name. If the writing treats one as a place and
# the graph has no such location, either the location is missing or the sentence is
# wrong — both cheap to fix on the day, expensive twenty thousand words later.
# A LINT, never a gate: "he came through the hall" in a game that deliberately has
# no hall location is a judgement call, and a check that fires on correct work gets
# ignored. Measured trigger: one game referred to a hall six times, a front door
# twice, and the street once, with none of them in the map.
BUILDING_PARTS = ("hall", "hallway", "stairs", "staircase", "landing", "street",
                  "front door", "back door", "garden", "yard", "attic", "cellar",
                  "basement", "porch", "driveway", "corridor")

# Currency naming, used when the ledger does not declare one. Inference is a
# fallback so the economy gates still bite on a game authored before board.economy
# existed; a declaration always wins and the headline says which was used.
CURRENCY_HINT = re.compile(r"money|cash|funds?|wallet|credits?|coins?|gold", re.I)
# `coin` was missing until 2026-08-14, which made a whole currency invisible: vesper
# spends `coin` 18 times and `money` once, and every economy gate was judging `money`.


# ─────────────────────────────────────────────────────────────────────────────
# Model building
# ─────────────────────────────────────────────────────────────────────────────
class Beat:
    """One screen of text the player reads. The unit the floors are counted in.

    Group variants (blocks[].blocks[]) fold INTO their parent beat rather than
    splitting it, because a Twine passage likewise carries all its <<if>>
    branches inline — folding keeps our numbers comparable to the DoL baseline
    the thresholds came from. Cascade beats DO split, because each one is a
    separate screen the player advances through.
    """
    __slots__ = ("canvas", "node", "text", "media")

    def __init__(self, canvas, node):
        self.canvas, self.node = canvas, node
        self.text, self.media = [], []

    @property
    def words(self):
        return len(" ".join(self.text).split())

    @property
    def explicit(self):
        return len(EXPLICIT.findall(" ".join(self.text)))


def _collect(blocks, beat, out, canvas, node):
    """Walk a block list, filling `beat` and appending any cascade sub-beats to `out`."""
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        btype = b.get("type", "")
        props = b.get("props") or {}

        if props.get("beats"):                       # cascade: each beat is its own screen
            for cb in props["beats"]:
                sub = Beat(canvas, node)
                _collect(cb.get("blocks"), sub, out, canvas, node)
                if sub.text or sub.media:
                    out.append(sub)
            continue

        # Group (and block_pool): variants of ONE screen, folded into the parent beat.
        #
        # ⚠️ BOTH SHAPES. The importer accepts a group's children at the block's own
        # `blocks` key OR inside `props.blocks`, and normalises to the latter
        # (`template_import.py:6062-6086`); the generator then renders `props.blocks`
        # (`v2.py:13770`). Reading only the first shape made 158 groups across FOUR
        # games invisible to every beat-based gate in this file — their prose was not
        # counted as words, as explicit beats, as dialogue, or as sentences, while it
        # rendered perfectly well in the built game.
        inner = b.get("blocks") or props.get("blocks")
        if inner:
            _collect(inner, beat, out, canvas, node)

        if btype in PROSE_BLOCKS and b.get("content"):
            beat.text.append(str(b["content"]))
        elif b.get("content") and btype not in MEDIA_BLOCKS:
            beat.text.append(str(b["content"]))       # unknown text-ish type: still player-facing

        if btype in MEDIA_BLOCKS or props.get("file") or props.get("pool_dir") or props.get("files"):
            beat.media.append({
                "file": props.get("file"),
                "pool_dir": props.get("pool_dir"),
                "files": props.get("files"),
                "pool": props.get("pool"),
            })


def _conditions_of(obj):
    """Yield every condition item dict reachable from a trigger/choice/block."""
    conds = obj.get("conditions")
    if isinstance(conds, dict):
        for it in conds.get("items") or []:
            if isinstance(it, dict):
                yield it


def _effect_value_sign(val):
    """+1 / -1 / 0 for an effect `value`, which may be a number or a random range.

    The engine accepts `{type = "random", min = N, max = M}` as a value (v2.py:13525),
    so a sign test that only handles numbers silently reads every ranged grant as zero.
    """
    if isinstance(val, bool):
        return 0
    if isinstance(val, (int, float)):
        return 1 if val > 0 else (-1 if val < 0 else 0)
    if isinstance(val, dict) and val.get("type") == "random":
        hi = val.get("max", val.get("min"))
        if isinstance(hi, (int, float)):
            return 1 if hi > 0 else (-1 if hi < 0 else 0)
    return 0


def _currency_ops(obj, cur, out):
    """Collect every movement this structure performs on the currency trait, BY DIRECTION.

    Walks the whole nested shape rather than the known effect sites, because a
    grant can hang off an exit_block config, a choice, or a cascade beat, and a
    gate that only looks in one of those under-reports the economy.
    NOTE the key asymmetry the rest of this file already documents: an EFFECT
    names its trait `trait`, a CONDITION names it `trait_key`.

    ⚠️ DIRECTION, NOT OP NAME — and `op = "subtract"` IS NOT AN ENGINE OP.
    `applyTraitEffect` runs `add` and `set` and silently returns on anything else
    (v2.py:5742-5751), so the only way to take currency away in an effect is
    `op = "add"` with a NEGATIVE value. This function used to append the op string,
    which meant a real deduction written the only way that works counted as INCOME —
    measured on a game whose sink/source line flipped from 11:11 to 10:12 the moment
    its dead `subtract` effects were rewritten correctly. A `subtract` effect is
    counted as neither: it moves nothing, and gate 25 is what reports it.
    """
    if isinstance(obj, dict):
        if (obj.get("trait") or obj.get("trait_key")) == cur and obj.get("op") == "add":
            sign = _effect_value_sign(obj.get("value"))
            if sign:
                out.append("subtract" if sign < 0 else "add")
        # a `costs` entry is a spend even though it carries no op
        for cost in (obj.get("costs") or []):
            if isinstance(cost, dict) and cost.get("trait") == cur:
                out.append("subtract")
        for v in obj.values():
            _currency_ops(v, cur, out)
    elif isinstance(obj, list):
        for v in obj:
            _currency_ops(v, cur, out)


def _median(xs):
    """Same convention as gate 1 uses: the middle element of the sorted list."""
    s = sorted(xs)
    return s[len(s) // 2] if s else 0


def build(game):
    canvases = game.get("canvases") or []
    by_id = {c["id"]: c for c in canvases if "id" in c}

    # Which canvas does a link point into?  choices carry nodeId = "<canvas>.<node>"
    referrer = {}
    for c in canvases:
        for n in c.get("nodes") or []:
            eb = n.get("exit_block") or {}
            for ch in (eb.get("choices") or []):
                tgt = ch.get("nodeId") or ""
                if "." in tgt:
                    cid = tgt.split(".", 1)[0]
                    if cid != c["id"]:
                        referrer.setdefault(cid, c["id"])
            cfg = eb.get("config") or {}
            for ch in (cfg.get("choices") or []):
                tgt = ch.get("nodeId") or ""
                if "." in tgt:
                    cid = tgt.split(".", 1)[0]
                    if cid != c["id"]:
                        referrer.setdefault(cid, c["id"])
        for sub in ((c.get("trigger") or {}).get("substitutions") or []):
            if sub.get("target_canvas_id"):
                referrer.setdefault(sub["target_canvas_id"], c["id"])

    def resolve(cid, key, seen=None):
        """A triggerless link-target inherits location/repeatability from whatever links to it."""
        seen = seen or set()
        if cid in seen:
            return None
        seen.add(cid)
        c = by_id.get(cid)
        if not c:
            return None
        trig = c.get("trigger")
        if trig and key in trig:
            return trig[key]
        if trig and key == "is_repeatable":
            return IS_REPEATABLE_DEFAULT
        parent = referrer.get(cid)
        return resolve(parent, key, seen) if parent else None

    model = []
    for c in canvases:
        cid = c["id"]
        trig = c.get("trigger") or {}
        loc = trig.get("location") or resolve(cid, "location") or "(unplaced)"
        rep = trig.get("is_repeatable", IS_REPEATABLE_DEFAULT) if trig else resolve(cid, "is_repeatable")
        rep = IS_REPEATABLE_DEFAULT if rep is None else bool(rep)

        beats = []
        for n in c.get("nodes") or []:
            beat = Beat(cid, n.get("id"))
            _collect(n.get("blocks"), beat, beats, cid, n.get("id"))
            if beat.text or beat.media:
                beats.append(beat)

        sets, reads = set(), set()
        traits = []
        for it in _conditions_of(trig):
            (reads.add(it["flag_key"]) if it.get("flag_key") else None)
            if it.get("trait_key"):
                traits.append((it["trait_key"], it.get("operator"), it.get("value")))
        for it in _conditions_of(trig):
            if it.get("trait_key"):
                reads.add(it["trait_key"])          # a trait gate is a read, same as a flag gate
        for n in c.get("nodes") or []:
            eb = n.get("exit_block") or {}
            for holder in [eb.get("config") or {}] + list(eb.get("choices") or []):
                for fe in (holder.get("flagEffects") or []):
                    if fe.get("flag"):
                        sets.add(fe["flag"])
                # A canvas can also open content by MOVING A TRAIT past a gate, not only
                # by setting a flag — staged chains (repair_session, drains_done) do
                # exactly this. Treating trait writes as opens too, or the gate lies
                # about a legitimate pattern.
                # NOTE the key asymmetry, verified against the source: an EFFECT names
                # its trait `trait`, while a CONDITION names it `trait_key`. Reading
                # only `trait_key` here silently misses every trait write in the game.
                for ef in (holder.get("effects") or []):
                    key = ef.get("trait") or ef.get("trait_key")
                    if key:
                        sets.add(key)
                for it in _conditions_of(holder):
                    if it.get("flag_key"):
                        reads.add(it["flag_key"])
                    if it.get("trait_key"):
                        reads.add(it["trait_key"])
                        traits.append((it["trait_key"], it.get("operator"), it.get("value")))

        model.append(dict(id=cid, loc=loc, rep=rep, beats=beats,
                          sets=sets, reads=reads, traits=traits,
                          random=trig.get("trigger_mode") == "random",
                          npc=trig.get("npc"), requires_npc=trig.get("requires_npc"),
                          # The economy gates need to know whether a surface is
                          # rate-limited. `costs` is a real gate (the engine blocks
                          # on affordability); `effects` only deducts, so an income
                          # surface with neither a per-day cap nor a cost is a money
                          # printer and every other economy rule is void beside it.
                          perday=trig.get("max_triggers_per_day"),
                          costs=trig.get("costs") or [],
                          # The whole source canvas. Added 2026-08-18 for the needs /
                          # walk-in / label checks, which need `name`, `substitution_only`
                          # and `substitutions` — none of which the flattened record kept.
                          raw=c,
                          nodes=c.get("nodes") or []))
    return model, game


# ─────────────────────────────────────────────────────────────────────────────
# Lints — reported, never scored
# ─────────────────────────────────────────────────────────────────────────────
def _dialog_blocks(blocks, out):
    """Every dialog block reachable from a node, including inside cascades and groups."""
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        props = b.get("props") or {}
        if b.get("type") == "dialog":
            out.append(b)
        for cb in (props.get("beats") or []):
            _dialog_blocks(cb.get("blocks"), out)
        if b.get("blocks"):
            _dialog_blocks(b["blocks"], out)


def lint_dialogue_attribution(model):
    """Dialogue attributed to a character the canvas neither BINDS nor NAMES.

    The bug this catches shipped once: a walk-on character with no NPC record was
    written as a dialog block borrowing a declared NPC's id, which would have
    rendered the wrong name over her line. Declaring her instead is not the fix —
    that breaks the standing-surface gate, which wants every declared character
    findable and scheduled. One-scene characters are narrated, never declared.

    Deliberately narrow. The naive version of this check — flag dialogue on any
    canvas without an `npc` binding — returns 30 hits on a game with 2 real ones,
    because every triggerless rung is unbound by design and correctly carries its
    own character's voice. Naming the character in the canvas id is what tells
    them apart, and it is a convention the games already follow.
    """
    seen, hits = set(), []
    for c in model:
        bound = {c.get("npc"), c.get("requires_npc")} - {None}
        for n in c.get("nodes") or []:
            blocks = []
            _dialog_blocks(n.get("blocks"), blocks)
            for b in blocks:
                npc_id = ((b.get("props") or {}).get("npcId") or "").strip()
                if not npc_id or npc_id in bound:
                    continue
                # `npc_ray` is named by a canvas called `rung_ray_sit`.
                short = re.sub(r"^npc[_-]", "", npc_id)
                if short and short.lower() in c["id"].lower():
                    continue
                # ONE hit per canvas+speaker, not per line. A canvas where the
                # wrong name renders gets it wrong on every line it says, so the
                # per-line count measures how talkative the scene is, not how
                # many defects there are.
                key = (c["id"], npc_id)
                if key in seen:
                    continue
                seen.add(key)
                hits.append(dict(canvas=c["id"], node=n.get("id"), npc=npc_id,
                                 lines=1, line=str(b.get("content") or "")[:60]))
            for h in hits:
                if h["canvas"] == c["id"]:
                    h["lines"] = sum(
                        1 for b in blocks
                        if ((b.get("props") or {}).get("npcId") or "") == h["npc"])
    return hits


def lint_screen_shape(model, game):
    """The two `the-surfaces.md` rules whose thresholds are not yet establishable.

    R5 — ungated doors: how much of a location's menu is open on turn one.
    R6 — does the SCREEN move on re-entry, by any of the four mechanisms R6 names.

    ⚠️ R6's tally was rewritten 2026-08-16 and the old one counted the wrong thing.
    It reported "N/N standing menus never change their prose" — a conditional-OPENER
    count — while the paragraph it claimed to enforce says the opposite: measured on
    the reference game, the identity sentence is byte-identical on all six visits, and
    the incumbent skill calls tiering an opener "a known failure" (lanes.md:167). So
    the worst score it ever printed, 24/24 frozen, was reported against openers that
    were CORRECT. It now counts R6's four mechanisms per LOCATION and leads on how
    many locations carry none of them:

        1. a condition clause on the screen's own prose  (weather/crowd, not progress)
        2. a presence line — an NPC-bound canvas at that location
        3. the choice list itself — at least one gated choice
        4. an event replacing the whole screen — trigger_mode = "random"

    LINTS, deliberately. Both were built as gates first and neither threshold held up:
    R5's ceiling had to be invented, and R6 is not field-comparable because a compiled
    game's `<<if>>` covers engine plumbing as well as authored banding. Read the numbers,
    judge them; do not let a build pass or fail on them until the play study lands.
    """
    located = {x["id"] for x in (game.get("canvases") or [])
               if (x.get("trigger") or {}).get("location")}

    def varies(blocks):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            if ((b.get("props") or {}).get("conditions") or {}).get("items"):
                return True
            if (b.get("conditions") or {}).get("items"):
                return True
            inner = (b.get("blocks") or []) + [bb for cb in ((b.get("props") or {}).get("beats") or [])
                                               for bb in (cb.get("blocks") or [])]
            if inner and varies(inner):
                return True
        return False

    # R6's four mechanisms, tallied per LOCATION rather than per screen — the player
    # experiences a place, not a canvas, and mechanisms 2 and 4 live on sibling canvases
    # at the same location rather than on the hub itself.
    mech = collections.defaultdict(set)
    for x in (game.get("canvases") or []):
        trig = x.get("trigger") or {}
        loc = trig.get("location")
        if not loc:
            continue
        if trig.get("trigger_mode") == "random":
            mech[loc].add("event")
        if trig.get("npc") or trig.get("requires_npc"):
            mech[loc].add("presence")

    out, tot, opened, menus = [], 0, 0, 0
    rows = []
    for c in model:
        if not c["rep"] or c["id"] not in located:
            continue
        chs = [ch for n in c["nodes"] for ch in ((n.get("exit_block") or {}).get("choices") or [])]
        if not chs:
            continue
        n_open = sum(1 for ch in chs if not ((ch.get("conditions") or {}).get("items")))
        # ⚠️ ROWS ON SCREEN — the only number here the PLAYER can see, and the one that was
        # missing. A locked choice with `show_when_locked` still renders: greyed, but a line
        # on the list. Measured failure: a pass gated 57 room choices, moved "open on turn
        # one" from 126/166 to 70/166, and left show_when_locked on all of them — so 164 of
        # 166 rows still rendered and the game played exactly as wide as before. The author
        # optimised the number that was reported and never looked at the wall.
        n_rows = n_open + sum(1 for ch in chs
                              if (ch.get("conditions") or {}).get("items")
                              and ch.get("show_when_locked"))
        rows.append(n_rows)
        if n_rows >= 8:
            out.append(dict(kind="rows", id=c["id"], loc=c["loc"],
                            note=f"{n_rows} rows RENDER on turn one ({n_open} clickable, "
                                 f"{n_rows - n_open} greyed) out of {len(chs)} authored"))
        tot += len(chs)
        opened += n_open
        if len(chs) >= 2:
            menus += 1
        if any(varies(n.get("blocks")) for n in c["nodes"]):
            mech[c["loc"]].add("prose")
        if n_open < len(chs):
            mech[c["loc"]].add("choices")
        if n_open >= 8:
            out.append(dict(kind="open", id=c["id"], loc=c["loc"],
                            note=f"{n_open} of {len(chs)} choices open with no condition"))

    # R6 — how many places carry none of the four ways a screen can move on re-entry.
    all_locs = [l["id"] for l in (game.get("locations") or []) if l.get("id")]
    NAMES = {"prose": "a conditional clause", "presence": "an NPC canvas",
             "choices": "a gated choice", "event": "a random event"}
    still = sorted(l for l in all_locs if not mech.get(l))
    thin = sorted((l for l in all_locs if len(mech.get(l, ())) == 1),
                  key=lambda l: l)
    for l in still:
        out.append(dict(kind="still", id="—", loc=l,
                        note="renders identically on every visit — none of R6's four mechanisms"))
    for l in thin[:6]:
        out.append(dict(kind="thin", id="—", loc=l,
                        note=f"varies by one mechanism only ({NAMES[next(iter(mech[l]))]})"))
    n_event = sum(1 for l in all_locs if "event" in mech.get(l, ()))
    # Population labelled on purpose: the anchoring lint counts ROOM screens only, this one
    # counts every located repeatable screen. Two adjacent numbers over different populations
    # is the denominator trap, and naming it is cheaper than reconciling it.
    summary = (f"median {_median(rows)} ROWS render on a screen at turn one "
               f"(max {max(rows) if rows else 0}) · {opened}/{tot} location choices open · "
               f"{len(still)}/{len(all_locs)} locations render identically on every visit "
               f"· {n_event}/{len(all_locs)} carry a random event (R6 mechanism 4, "
               f"the one games drop)")
    return summary, out


def lint_world_prose(model, game):
    """Parts of a building the writing treats as real, that the map does not have.

    A LINT, not a gate. Crossing "the hall" in a game with no hall location may be
    perfectly deliberate — but the measured case was a game whose prose named a hall
    six times, a front door twice and the street once while its map had none of them,
    and whose shop was consequently reachable in one step from the living room.
    Either the location is missing or the sentence is wrong; both are cheap now.
    """
    locs = game.get("locations") or []
    known = " ".join(str(l.get("id", "")) + " " + str(l.get("name", "")) for l in locs).lower()
    prose = " ".join(t for c in model for b in c["beats"] for t in b.text).lower()
    hits = []
    for part in BUILDING_PARTS:
        if part in known:
            continue
        n = len(re.findall(rf"\b{re.escape(part)}\b", prose))
        if n >= 3:                      # once is a turn of phrase; three is a place
            m = re.search(rf"[^.]*\b{re.escape(part)}\b[^.]*\.", prose)
            hits.append(dict(part=part, count=n, line=(m.group(0).strip()[:70] if m else "")))
    return sorted(hits, key=lambda h: -h["count"])


# ─────────────────────────────────────────────────────────────────────────────
# Gates
# ─────────────────────────────────────────────────────────────────────────────
_OBJ_STOP = set("""
a an the and or but of to in on at for with from into over under by it its this that those these
you your yours she her hers he him his they them their is are was were be been being do does did
if then than so as up down out off back again more most some any all one two three four five six
seven eight nine ten what who whom which where when how why not no yes can will would could should
may might must let get got go goes going come comes take takes put puts make makes see sees look
looks keep keeps give gives run runs say says tell tells ask asks want wants need needs like just
now still yet only ever never own properly instead something somebody anybody nothing everything
there here whole half first last next again through past before after until while every each
another other same both few many much less least enough almost quite rather even also else
monday tuesday wednesday thursday friday saturday sunday weekend weekday morning evening night
eleven twelve twenty thirty forty fifty hundred
shift start minute hour day week month year time moment thing way point reason version sort kind
""".split())
# ⚠️ The second block was added after the under-declaration check reported choices "hanging off"
# objects called *there*, *before*, *whole*, *forty* and *friday*. Adverbs, ordinals, weekday
# names and bare numbers are never the thing a choice acts on, and they were drowning the real
# findings. Words that ARE objects in some game (a "morning" shift is not an object; a location
# genuinely named "The Weekend" would be) stay resolvable through the declared list itself.
# The third block is time spans and abstractions — *the shift*, *the start of it*, *the whole
# point*. They pass every lexical test for a noun and none of them is a thing in a room.


# An object is a thing a room HAS, and in English that is written with a determiner in front of
# it. This is the cheapest available noun test and it exists because the under-declaration check
# was reporting `sleep` (from the choice "Sleep.") as an object the board had failed to declare.
# Measured on a real game: without it, 16 findings of which 6 were verbs or bare abstractions;
# with it, 7 findings and every one a genuine thing in the room.
_NOUN_PHRASE = re.compile(
    r"\b(?:the|a|an|his|her|its|their|your|our|this|that|these|those|one|two|three|four|five|"
    r"six|seven|eight|nine|ten)\s+([a-z][a-z-]{2,})", re.I)


def _phrase_nouns(text):
    """Stemmed head-nouns that `text` names WITH a determiner, minus stopwords."""
    out = set()
    for w in _NOUN_PHRASE.findall(text or ""):
        st = _stem(w.lower())
        if st not in _OBJ_STOP and len(st) > 2:
            out.add(st)
    return out


def _stem(w):
    """Crude singular form. It only has to make the singular and the plural of the same word
    land on the same string.

    ⚠️ The first version stripped "es" from ANY word ending in it, so 'cages'->'cag' while
    'cage'->'cage' — 5 of 16 common pairs failed to meet, including cubicle/cubicles and
    table/tables, both of which occur in a real board declaration. English only adds "es"
    after a sibilant; everything else is a plain "s" on a word that already ends in "e".
    """
    if len(w) >= 5 and w.endswith(("ses", "xes", "zes", "ches", "shes")):
        return w[:-2]
    if len(w) >= 4 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w
    # Known and accepted: f->ves irregulars (shelf/shelves) still miss. Handling them costs
    # more than it buys — 'curves'->'curf' would be a new wrong answer — and both sides of a
    # real comparison are almost always the same number.


def _content_words(s):
    """Content words of a phrase — the vocabulary an object or a choice actually names.

    ⚠️ Stops are checked on BOTH the raw word and its stem. Filtering the raw form only let
    every inflection through — "gets" survived while "get" was stopped — which showed up as
    choices apparently hanging off objects called "get" and "start".
    """
    out = []
    for w in re.findall(r"[a-z]+", (s or "").lower()):
        if len(w) <= 2 or w in _OBJ_STOP:
            continue
        st = _stem(w)
        if st in _OBJ_STOP:
            continue
        out.append(st)
    return out


def _names_any(text, vocab):
    """Does `text` name anything in `vocab`? Both sides are stemmed, then matched exactly,
    with a SIX-character prefix fallback so 'curtain'/'curtained' and 'monitor'/'monitoring'
    connect.

    ⚠️ Six, not five. At five, 'count' matched 'counter' — so *"Count Bev's float"* was
    credited to the shop counter, which is a different object. A false PASS is the dangerous
    direction here: this gate exists to catch choices that name nothing, and one that
    silently forgives them is worse than none. Six excludes every 5-letter word from the
    fuzzy path, which costs a few true matches ('drain'/'drainage') and buys back precision.
    """
    for w in _content_words(text):
        if w in vocab:
            return w
        if len(w) >= 6:
            for v in vocab:
                if len(v) >= 6 and (v.startswith(w[:6]) or w.startswith(v[:6])):
                    return v
    return None


# ═════════════════════════════════════════════════════════════════════════════
# NEEDS + WALK-INS + LABELS — the 2026-08-18 pass. These replaced `objects`.
#
# The rule they enforce: a room's list is NEEDS + WORK + PEOPLE and nothing else
# (`the-surfaces.md` R2). The previous occupant of this space, gate 22, computed
# affordances from `exit_block.choices` and could not see a canvas at all — so
# "Get the washing in off the airer", an entire canvas about the airer, counted
# as ZERO, and the only way to go green was a second screen re-listing what was
# already there. It was green on all five games while manufacturing nine
# duplicate room screens. A check that cannot see the shape of the thing it
# judges does not measure quality; it manufactures whatever it CAN see.
# ═════════════════════════════════════════════════════════════════════════════

# Room-list labels that open on a determiner and name no verb: "The bench",
# "The counter, before midnight". A player cannot tell what clicking does.
# `the-voice.md` R1 — reported, never gated: three shipped games sit at 0% so the
# target is reachable, but any threshold in the 38%..84% gap would be invented,
# and this skill has demoted two rules for exactly that.
_DETERMINER = re.compile(r"^(the|a|an|your|his|her|their|my|our|this|that)\b", re.I)

# 84,009 action labels across the 27 parseable sandboxes, re-measured 2026-08-24:
#   ~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/
# A label here is every clickable form — [[…]], <<link>>, <<button>>, <a data-passage> —
# with ONE-WORD labels excluded ("Continue", "Next", "Back" are flow, not actions).
#
# ⚠️ THE LONG SHARE WAS WRONG AND IS CORRECTED HERE. It shipped as 0.10 against a stated
# basis of 64,594 labels on 25 games. Rebuilt on that same 25 the basis reproduces to
# 0.29% (64,781) and the median reproduces exactly at 3 — but the share at 6+ words is
# 16%, not 10%, and NO filter tested produces 10% while also producing a median of 3
# (all-labels gives 8.7% but a median of 2). The likeliest reading is that the median was
# taken on the 2+ set and the long share on the whole set. `findings_RECHECK.md` §1.
FIELD_LABEL_MEDIAN_WORDS = 3
FIELD_LABEL_LONG_SHARE   = 0.21      # share at 6+ words, 27 games (was 0.16 on 25)


def _room_list_labels(model, game):
    """The canvas names that RENDER in a location's solo-activity list.

    NOT choices inside a scene — those are exempt by `the-voice.md` R1, and the
    exemption leaking onto canvas names is what shipped "Come down in what you
    slept in" as a top-level button. Mirrors the runtime filter at v2.py:4514.
    """
    out = []
    for c in model:
        t = (c.get("raw") or {}).get("trigger") or {}
        if not t.get("location") or not t.get("is_repeatable"):
            continue
        if t.get("trigger_mode") == "random" or t.get("substitution_only"):
            continue
        if t.get("npc") or t.get("requires_npc"):
            continue                                   # a portrait, not a list row
        nm = (c.get("raw") or {}).get("name")
        if nm:
            out.append((c["id"], c["loc"], nm))
    return out


def lint_labels(model, game):
    """`the-voice.md` R1 as two numbers: noun-only share, and label length."""
    rows = _room_list_labels(model, game)
    if not rows:
        return "", []
    nouny = [(cid, loc, nm) for cid, loc, nm in rows if _DETERMINER.match(nm.strip())]
    words = [len(nm.split()) for _, _, nm in rows]
    longs = sum(1 for w in words if w >= 6)
    summary = (f"{len(nouny)}/{len(rows)} ({100*len(nouny)//max(len(rows),1)}%) room-list buttons "
               f"are bare noun phrases · median {_median(words)} words, "
               f"{100*longs//max(len(words),1)}% at 6+ "
               f"(field: {FIELD_LABEL_MEDIAN_WORDS} words, "
               f"{int(FIELD_LABEL_LONG_SHARE*100)}% at 6+)")
    out = [f"{loc}: \"{nm}\" names no verb — a player cannot tell what clicking does"
           for _, loc, nm in nouny[:8]]
    out += [f"{loc}: \"{nm}\" is {len(nm.split())} words"
            for _, loc, nm in sorted(rows, key=lambda r: -len(r[2].split()))[:3]
            if len(nm.split()) >= 8]
    return summary, out


def lint_browse_share(model, game):
    """Room canvases whose entire click changes nothing but the clock.

    A NUMBER, not a bar. Known noisy — a travel bridge legitimately scores as a
    browse (vesper's three "Take the car" rows), so read WHICH canvases it names
    rather than the percentage alone.
    """
    def changes(o):
        if isinstance(o, dict):
            if any(o.get(k) for k in ("effects", "flagEffects", "itemEffects",
                                      "questEffects", "costs")):
                return True
            return any(changes(v) for v in o.values())
        if isinstance(o, list):
            return any(changes(v) for v in o)
        return False

    rows = _room_list_labels(model, game)
    if not rows:
        return "", []
    by_id = {c["id"]: (c.get("raw") or {}) for c in model}
    inert = [(loc, nm) for cid, loc, nm in rows if not changes(by_id.get(cid) or {})]
    summary = (f"{len(inert)}/{len(rows)} "
               f"({100*len(inert)//max(len(rows),1)}%) room canvases change nothing but the clock")
    return summary, [f"{loc}: \"{nm}\" — no effect, no flag, no cost" for loc, nm in inert[:8]]


def _rule_bounds(rule):
    """{(subject, npc, key): (lower, upper, exact, flag)} for one substitution rule."""
    out = {}
    for it in ((rule.get("conditions") or {}).get("items") or []):
        key = (it.get("subject"), it.get("npc_id"),
               it.get("trait_key") or it.get("flag_key") or it.get("item_id"))
        lo, up, eq, fl = out.get(key, (None, None, None, None))
        op, val = str(it.get("operator") or ""), it.get("value")
        if op in ("gte", "gt") and isinstance(val, (int, float)):
            lo = val if lo is None else max(lo, val)
        elif op in ("lte", "lt") and isinstance(val, (int, float)):
            up = val if up is None else min(up, val)
        elif op == "eq":
            eq = val
        elif op in ("is_true", "is_false"):
            fl = (op == "is_true")
        out[key] = (lo, up, eq, fl)
    return out


def _rules_contradict(a, b):
    """Can these two substitution rules ever pass their conditions at the same time?"""
    ba, bb = _rule_bounds(a), _rule_bounds(b)
    for key in set(ba) & set(bb):
        (alo, aup, aeq, afl), (blo, bup, beq, bfl) = ba[key], bb[key]
        lows = [v for v in (alo, blo) if v is not None]
        ups = [v for v in (aup, bup) if v is not None]
        lo = max(lows) if lows else None
        up = min(ups) if ups else None
        if lo is not None and up is not None and lo >= up:
            return True                       # `x >= 20` and `x < 20` never hold together
        if aeq is not None and beq is not None and aeq != beq:
            return True
        if afl is not None and bfl is not None and afl != bfl:
            return True
    return False


def _dispatch_worst_case(rules):
    """The co-satisfiable set of independent rules that squeezes the HOST hardest.

    ⚠️ Not the largest set — the worst one. Picking by size makes the answer depend
    on the order the rules happen to be declared in: five rules where three bands are
    exclusive have several co-live triples, and `{band 0.30, 0.12, 0.10}` and
    `{band 0.80, 0.12, 0.10}` are both size three while leaving the host 55% and 16%
    of the time. A number that changes when an author reorders their TOML is not a
    measurement.

    Exact by brute force — a host with more than a dozen rules is not a thing anyone
    has authored, and the fallback keeps the lint honest if one ever is.
    """
    if len(rules) > 12:
        return rules
    best, best_surv = [], 1.0
    for mask in range(1 << len(rules)):
        pick = [rules[i] for i in range(len(rules)) if mask >> i & 1]
        if not pick:
            continue
        surv = 1.0
        for r in pick:
            surv *= (1.0 - float(r.get("chance") or 0))
        if surv >= best_surv:
            continue
        if all(not _rules_contradict(pick[i], pick[j])
               for i in range(len(pick)) for j in range(i + 1, len(pick))):
            best, best_surv = pick, surv
    return best


def lint_dispatch_depth(game):
    """How many DIFFERENT things one activity can turn into. `the-surfaces.md` R3.

    The walk-in floor GATE is an existence check — one substitution rule anywhere in
    a room and the room is covered (`_walkin_join`) — and it says so in its own
    comment: *one walk-in per qualifying room; the rest is the author's call*. But
    R3's content IS the branching (*"the richness is combinatorial, not authored"*),
    and until 2026-08-23 nothing printed how deep a dispatch goes.

    A NUMBER, never a gate. The field's unit is a passage and ours is a canvas, so no
    threshold transfers. What reads is the shape: DoL's `Bath` dispatches TWELVE
    outcomes from one activity; the deepest in this repo is vesper's `chat_the_floor`
    at four; and three v2 games run every host at exactly one — which is a coin flip
    between one branch and the base canvas, not a dispatch.

    The second half is the ENGINE, and it is invisible in the TOML. Rules without
    `exclusive_group` each roll their OWN dice (`v2.py:5382-5391`), so stacking them
    silently drives the host off the screen; rules sharing one share a single roll
    partitioned into buckets (`v2.py:5361-5379`), which is what a multi-outcome
    dispatch wants. This prints the host's own survival odds so the difference is not
    something an author has to compute.
    """
    hosts = []
    for c in (game.get("canvases") or []):
        rules = ((c.get("trigger") or {}).get("substitutions")) or []
        if not rules:
            continue
        targets = {r.get("target_canvas_id") for r in rules if r.get("target_canvas_id")}
        groups = {r.get("exclusive_group") for r in rules if r.get("exclusive_group")}
        solo = [r for r in rules if not r.get("exclusive_group")]
        # What is left for the base canvas, WORST CASE. Independent rules each roll,
        # so the ones that can be live together multiply; a group takes its slice off
        # the top once.
        #
        # ⚠️ "can be live together" is the whole difficulty and it is not decoration.
        # back_home stacks four `exposure >= 35/45/55` rules that are ALL true at the
        # top of its game — multiplying is right, and the activity renders 24% of the
        # time. off_season bands one walk-in `lt 20` / `gte 20 and lt 22` / `gte 22`,
        # where exactly one can ever pass — multiplying those would report 6% for a
        # canvas that actually renders 70% of the time early on. Same TOML shape, two
        # different mechanisms, so the contradictory pairs get found before anything
        # is multiplied.
        survives = 1.0
        for r in _dispatch_worst_case(solo):
            survives *= (1.0 - float(r.get("chance") or 0))
        for g in groups:
            survives *= max(0.0, 1.0 - sum(float(r.get("chance") or 0)
                                           for r in rules if r.get("exclusive_group") == g))
        hosts.append((str(c.get("id") or "?"),
                      str((c.get("trigger") or {}).get("location") or "—"),
                      len(rules), len(targets), sorted(g for g in groups if g), survives))
    if not hosts:
        return "", []
    depths = [h[3] for h in hosts]
    deepest = max(hosts, key=lambda h: h[3])
    summary = (f"{len(hosts)} dispatching activit{'y' if len(hosts) == 1 else 'ies'} · "
               f"{sum(h[2] for h in hosts)} rule(s) · outcomes per host "
               f"{depths if len(depths) <= 8 else str(sorted(depths, reverse=True)[:8]) + '…'} "
               f"· deepest {deepest[0]} at {deepest[3]} "
               f"· field: DoL's Bath dispatches 12 from one activity")
    findings = [f"{cid} @{loc}: {n} rule(s), ONE outcome — the roll decides whether the "
                f"branch or the host renders, not which branch"
                for cid, loc, n, d, _g, _s in hosts if d == 1]
    findings += [f"{cid} @{loc}: {n} independent rule(s), no exclusive_group — each rolls its "
                 f"own dice (v2.py:5382), so the host itself renders {100*surv:.0f}% of the time"
                 for cid, loc, n, d, g, surv in hosts if d > 1 and not g and surv < 0.5]
    return summary, findings



def _flat_blocks(blocks, out=None):
    """Every block in a node, groups and cascade beats flattened into one list."""
    out = [] if out is None else out
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        out.append(b)
        props = b.get("props") or {}
        for beat in (props.get("beats") or []):
            _flat_blocks(beat.get("blocks"), out)
        _flat_blocks(props.get("blocks") or b.get("blocks"), out)
    return out


def _speech_split(game):
    """(narration+thought words, spoken words) across every player-facing text block.

    Walks groups and cascade beats, because that is where v2 games keep their prose.
    `dialog` is the only block the engine renders as speech; `thought_bubble` is
    interiority and counts with narration, which is the point of the gate — in every
    v2 game the protagonist's inner monologue outweighs everything anyone says aloud
    (seventh_day 4.6 thought words per spoken word, forty_miles 3.1).
    """
    spoken = other = 0

    def walk(blocks):
        nonlocal spoken, other
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            btype = b.get("type")
            props = b.get("props") or {}
            if btype in PROSE_BLOCKS and b.get("content"):
                n = len(str(b["content"]).split())
                if btype == "dialog":
                    spoken += n
                else:
                    other += n
            for beat in (props.get("beats") or []):
                walk(beat.get("blocks"))
            walk(props.get("blocks") or b.get("blocks"))

    for c in (game.get("canvases") or []):
        for n in (c.get("nodes") or []):
            walk(n.get("blocks"))
    return other, spoken


def _canvas_text(c):
    """Every word of a model canvas's authored prose, in reading order."""
    return " ".join(t for b in c["beats"] for t in b.text)


def _rungs_of(text):
    """(first rung the text reaches, set of rungs present). None if it reaches none."""
    hits = {}
    for name, rx in RUNGS:
        m = rx.search(text)
        if m:
            hits[name] = m.start()
    if not hits:
        return None, set()
    return min(hits, key=hits.get), set(hits)


def lint_ladder(model, game):
    """Where each explicit canvas sits on the ladder, opening rung and ceiling.

    A NUMBER, never a bar. A canvas is not a field passage: the field's unit is one
    rung of a chain, ours is a whole scene, so no single threshold is comparable.
    What IS readable is the shape of the distribution, and both failure directions
    show up in it plainly.
    """
    rows = []
    for c in model:
        text = _canvas_text(c)
        if len(EXPLICIT.findall(text)) < 3:
            continue
        first, present = _rungs_of(text)
        if not first:
            continue
        rows.append((c["id"], c["loc"], first, present))
    if not rows:
        return "", []
    TOP = {"oral", "vaginal", "anal", "finish"}
    high = [r for r in rows if r[2] in ("vaginal", "anal", "finish")]
    stuck = [r for r in rows if not (r[3] & TOP)]
    summary = (f"{len(rows)} explicit canvases · {100*len(high)//len(rows)}% OPEN at "
               f"vaginal-or-above · {100*len(stuck)//len(rows)}% never reach oral "
               f"· field screens open at vaginal-or-above 46% of the time")
    findings = ([f"{cid} @{loc}: opens on {first} — no rung below it anywhere in the canvas"
                 for cid, loc, first, _ in high[:5]]
                + [f"{cid} @{loc}: never gets past {first} — {len(pres)} rung(s) total"
                   for cid, loc, first, pres in stuck[:5]])
    return summary, findings


def lint_talk_screens(model, game):
    """Screens whose job is a conversation. The genre's second largest content kind.

    Field: 15,774 of 54,630 screens (29%) are two-thirds spoken with one picture.
    Ours: the_allowance ships 216 spoken words in the entire game, seventh_day 410.
    """
    talk = []
    for c in model:
        text = _canvas_text(c)
        if not text.strip() or len(EXPLICIT.findall(text)) >= 3:
            continue
        _, spoken = _speech_split({"canvases": [{"nodes": c.get("nodes") or []}]})
        total = len(text.split())
        if total and spoken / total >= 0.40:
            talk.append((c["id"], c["loc"]))
    total_canvases = len(model)
    pct = 100 * len(talk) // max(total_canvases, 1)
    summary = (f"{len(talk)}/{total_canvases} canvases ({pct}%) are talk screens "
               f"— 40%+ spoken, no explicit load · field 29% of all screens")
    return summary, [f"{cid} @{loc}" for cid, loc in talk[:8]]


def _self_loop_nodes(canvas):
    """Node ids in this canvas that carry a choice routing back into themselves."""
    cid = canvas.get("id")
    out = set()
    for n in (canvas.get("nodes") or []):
        nid = n.get("id")
        eb = n.get("exit_block") or {}
        holders = list(eb.get("choices") or []) + list((eb.get("config") or {}).get("choices") or [])
        for ch in holders:
            if ch.get("targetType") != "node":
                continue
            tgt = str(ch.get("nodeId") or "")
            if tgt == nid or tgt == f"{cid}.{nid}":
                out.add(nid)
    return out


def lint_loop_shape(model, game):
    """Repeatable explicit surfaces: act-menu loop, or one-shot cascade?

    The loop is the field's own repeatable shape — destroyer's `ginablow` is one
    clip from a pool of eight, four words of text, and five exits (Keep blowing ·
    Pound her ass · Pound her pussy · Cum · Go back). Our engine builds it already:
    a triggerless canvas, one act node per rung, a self-loop that raises a hidden
    meter, switch links, and a finish gated on the meter (the-surfaces.md).

    A COUNT, never a target. Three loop shapes are offered as a choice; a game with
    one good loop is not worse than a game with four.
    """
    loops, oneshot = [], []
    for c in model:
        if not c["rep"]:
            continue
        if len(EXPLICIT.findall(_canvas_text(c))) < 3:
            continue
        (loops if _self_loop_nodes(c.get("raw") or {}) else oneshot).append((c["id"], c["loc"]))
    if not (loops or oneshot):
        return "", []
    summary = (f"{len(loops)} act-menu loop(s) and {len(oneshot)} one-shot cascade(s) "
               f"across {len(loops)+len(oneshot)} repeatable explicit surfaces")
    return summary, [f"{cid} @{loc}: repeatable, explicit, no act menu — one pass and it is spent"
                     for cid, loc in oneshot[:8]]


def _act_nodes(canvas):
    """The nodes a player is ON while the act is happening.

    The self-loop nodes (the act menu's own rungs) plus whatever the arousal-gated
    choice targets — the finisher. Entry and reset are deliberately NOT act nodes:
    one is the door and the other is afterwards, and both correctly score zero.
    """
    out = set(_self_loop_nodes(canvas))
    for n in (canvas.get("nodes") or []):
        eb = n.get("exit_block") or {}
        for ch in list(eb.get("choices") or []):
            items = ((ch.get("conditions") or {}).get("items") or [])
            if any(i.get("trait_key") == "arousal" for i in items):
                tgt = str(ch.get("nodeId") or "").split(".")[-1]
                if tgt:
                    out.add(tgt)

    # ⚠️ ONE HOP, when the act node is a pure menu. `the_long_summer_test` routes
    # base_ontop / base_doggystyle / base_missionary to result_* nodes and carries no
    # prose on the rungs themselves — measuring only the rungs read that game as
    # having no act beats at all, which is the blind spot, not the answer.
    byid = {str(n.get("id")): n for n in (canvas.get("nodes") or [])}
    for nid in list(out):
        node = byid.get(nid)
        if not node or _node_has_prose(node):
            continue
        eb = node.get("exit_block") or {}
        for ch in list(eb.get("choices") or []):
            if (ch.get("targetType") or "node") != "node":
                continue
            tgt = str(ch.get("nodeId") or "").split(".")[-1]
            if tgt and tgt in byid and tgt not in out:
                out.add(tgt)
    return out


def _node_has_prose(node):
    """Any block on this node that puts words on the screen."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "content" and isinstance(v, str) and v.strip():
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(node.get("blocks"))
    return bool(found)


def _band_texts(node):
    """One string per VARIANT this node can render, not per authored block.

    A `Beat` folds a node's [group] bands together, on purpose — a Twine passage
    carries all its `<<if>>` branches inline and the DoL baseline was counted that
    way. But a PLAYER sees exactly one band plus whatever sits outside the chain, and
    a finisher scoring six across three bands can put two body words on the screen.
    Measured live: every act node passed while nine finisher bands did not.
    """
    fixed, bands = [], []

    def walk(blocks, sink):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            props = b.get("props") or {}
            inner = b.get("blocks") or props.get("blocks")
            if b.get("type") == "group" and inner:
                acc = []
                walk(inner, acc)
                bands.append(" ".join(acc))
                continue
            if inner:
                walk(inner, sink)
            if b.get("content") and b.get("type") not in MEDIA_BLOCKS:
                sink.append(str(b["content"]))

    walk(node.get("blocks"), fixed)
    base = " ".join(fixed)
    return [f"{band} {base}".strip() for band in bands] if bands else ([base] if base else [])


def lint_act_nodes(model, game):
    """How crude is the beat the player is actually IN?

    `explicit floor` is a game-WIDE share, and a game can clear it while every act
    node is warm — which is exactly what the measured failure looked like: 95% of one
    game's crude prose sealed in a room with no exits, and all nine of its repeatable
    sex loops scoring zero. A percentage cannot see that. This reads the act nodes of
    every act-menu loop and its finisher, because that is the screen in front of the
    player while the thing is happening.

    A NUMBER, never a gate. **3 is not an invented threshold**: it is the same count
    `explicit floor` uses to call a beat explicit at all, so a row under 3 is an act
    beat that does not register as explicit anywhere else in the instrument either.

    `register.md`: an explicit beat stays on the body for its whole length. Read the
    beat's last sentence — if it is about what the moment MEANS rather than what is
    HAPPENING, the beat has pivoted, and a pivoted beat scores 0-1 here.
    """
    rows, vals = [], []
    for c in model:
        raw = c.get("raw") or {}
        if not c["rep"] or not _self_loop_nodes(raw):
            continue
        if len(EXPLICIT.findall(_canvas_text(c))) < 3:
            continue
        nodes = _act_nodes(raw)
        byid = {str(n.get("id")): n for n in (raw.get("nodes") or [])}
        beats = []
        for b in c["beats"]:
            if b.node not in nodes:
                continue
            # What a PLAYER can see, worst case: the thinnest band this node renders.
            bands = [len(EXPLICIT.findall(t)) for t in _band_texts(byid.get(b.node) or {})]
            beats.append((b.node, b.explicit, min(bands) if bands else b.explicit))
        if beats:
            rows.append((c["id"], beats))
            vals += [x for _, _, x in beats]
    if not vals:
        return "", []
    cold = sum(1 for x in vals if x < 3)
    summary = (f"{len(rows)} act-menu loop(s) · {len(vals)} act and finish beats · "
               f"median {_median(vals):.0f} explicit word(s) on the THINNEST band each "
               f"renders · {cold} of {len(vals)} under 3")
    findings = []
    for cid, beats in sorted(rows, key=lambda r: sum(1 for _, _, x in r[1] if x < 3), reverse=True):
        n = sum(1 for _, _, x in beats if x < 3)
        findings.append(
            f"{cid}: " + " ".join(f"{nd}={x}" + (f"(band {m})" if m != x else "")
                                  for nd, x, m in beats)
            + (f"  — {n} of {len(beats)} warm, not explicit" if n else "  — all explicit"))
    return summary, findings


def _declared_needs(state):
    """`board.needs[]` — the body's clock. the-meters.md M8."""
    return ((state or {}).get("board") or {}).get("needs") or []


def _traits_read_by_conditions(game):
    """Every trait key any condition anywhere in the game actually reads.

    Walks the WHOLE game object, not just triggers: a need is just as validly
    gated from a choice, a [group] block or a quest card as from a trigger.
    """
    seen = set()

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "trait" and o.get("trait_key"):
                seen.add(str(o["trait_key"]))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(game)
    return seen


# ═════════════════════════════════════════════════════════════════════════════
# METER OWNERSHIP — who owns the number, and whether anything reads it.
# `the-meters.md` W1-W6.  Measured 2026-08-19 over 25 mopoga sandboxes
# (~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/).
#
# ⚠️ INSTRUMENT NOTE, because it changes every field figure quoted below.
# `<<if $lust lt 0>>` is a CLAMP GUARD, not a content gate — corpo-life carries
# 2,889 of them on one variable. A first pass counted them and reported that
# meter at 3,235 gates when the real figure is 346. Every field number in this
# section counts only comparisons against a threshold strictly inside the
# meter's own range. Same failure family as the quote-only dialogue count that
# retired v1's Rule 4: an instrument that cannot tell a guard from a gate does
# not report a smaller number, it reports the wrong one.
# ═════════════════════════════════════════════════════════════════════════════

def _walk_paths(o, path=()):
    """Every dict in the game object, with the key-path that reached it."""
    if isinstance(o, dict):
        yield path, o
        for k, v in o.items():
            yield from _walk_paths(v, path + (k,))
    elif isinstance(o, list):
        for v in o:
            yield from _walk_paths(v, path + ("[]",))


def _traits_read_anywhere(game):
    """Every PLAYER trait key that any reader in the game consults → counts.

    Three readers, not one:

      · a `conditions` predicate     {type="trait", trait_key=…}
      · a `costs` entry              {trait=…, value=…}   ← gates AND deducts
      · a quest card `when`/`goals`  {trait=…, op="gte", value=…}

    G29 keeps the narrower `_traits_read_by_conditions` on purpose so its verdict
    does not shift under it. This one exists because a meter spent through `costs`
    IS read — the engine filters an unaffordable choice rather than letting it fail
    (engine.md §27) — and calling that dead would fail a game for using the engine's
    own resource gate.
    """
    seen = collections.Counter()
    for path, node in _walk_paths(game):
        if node.get("subject") == "npc":
            continue
        ps = "|".join(path)
        if node.get("type") == "trait" and node.get("trait_key"):
            seen[str(node["trait_key"])] += 1
        elif ps.endswith("costs|[]") and node.get("trait"):
            seen[str(node["trait"])] += 1
        elif "trait" in node and node.get("op") in ("gte", "gt", "lt", "lte"):
            seen[str(node["trait"])] += 1
    return seen


def _player_trait_raises(game):
    """Player traits written by an `effects` entry → {trait: [where, …]}.

    `where` is the canvas id when the effect sits inside one, else the top-level
    section that carried it (`engine`, `settings`, …), so a failure line can name
    the place to go and look rather than saying "somewhere".
    """
    out = collections.defaultdict(list)

    def scan(obj, where):
        for path, node in _walk_paths(obj):
            if not "|".join(path).endswith("effects|[]"):
                continue
            if "trait" in node and "op" in node and node.get("targetType", "player") == "player":
                out[str(node["trait"])].append(where)

    for c in (game.get("canvases") or []):
        scan(c, str(c.get("id") or "—"))
    for k, v in game.items():
        if k != "canvases":
            scan({k: v}, k)
    return out


def _engine_read_stage_traits(game):
    """`<npc>_stage` keys whose prefix names a DECLARED character.

    The ENGINE is their reader: `applyAndNotifyTrait` matches /^([a-z_]+)_stage$/
    and writes `game_state.stage_advancement_log[slug]` on an upward delta
    (v2.py:5549-5554, `author-game/references/trait-catalog.md` §3). A game that
    raises one and never gates on it is using the engine as designed, so G33
    exempts it.

    ⚠️ ONLY when the prefix is a real character. `sex_stage` is NOT exempt — no
    character is called `sex` — and vesper writes it 81 times against 0 reads,
    which is a genuine dead meter the carve-out must not hide.
    """
    ids = set()
    for n in (game.get("npcs") or []):
        nid = str(n.get("id") or "")
        if nid:
            ids.add(nid)
            ids.add(re.sub(r"^npc_", "", nid))
        nm = str(n.get("name") or "").split()
        if nm:
            ids.add(nm[0].lower())
    return {f"{i}_stage" for i in ids if i}


def _school_split(game, state):
    """Gate sites on DECLARED meters: player tiers vs per-character.

    The player side is whatever `board.ascent_tiers` NAMES, so no keyword
    classifier decides what counts as a meter — the author does. The character
    side is every `subject = "npc"` trait predicate.

    Quest-card reads are excluded on both sides: a guidance card describes
    progress, it does not gate access, and counting it would let the quest page
    decide which school the game is in.
    """
    tiers = set(((state or {}).get("board") or {}).get("ascent_tiers") or [])
    player, npc = collections.Counter(), collections.Counter()
    for path, node in _walk_paths(game):
        if "quest_cards" in "|".join(path) or node.get("type") != "trait":
            continue
        key = str(node.get("trait_key") or "")
        if node.get("subject") == "npc":
            npc[f"{node.get('npc_id') or '?'}.{key}"] += 1
        elif key in tiers:
            player[key] += 1
    return player, npc


# A meter runs 0-100, so a gate above 100 is a locked door declared in the open
# (`the-release.md` G9), not a rung of the climb. Counting one would credit a game
# for a step nothing can climb to.
METER_MAX = 100


def _meter_rungs(game):
    """{trait: sorted distinct thresholds} over real content gates.

    Conditions and `costs`, not quest cards — a quest card names the band the
    player is IN, and counting it would credit a game for describing a rung it
    never gates. Gates above `METER_MAX` are dropped for the same reason.
    """
    out = collections.defaultdict(set)
    for path, node in _walk_paths(game):
        ps = "|".join(path)
        if "quest_cards" in ps or node.get("subject") == "npc":
            continue
        v = node.get("value")
        if not isinstance(v, (int, float)) or not 0 < v <= METER_MAX:
            continue
        if node.get("type") == "trait" and node.get("trait_key"):
            out[str(node["trait_key"])].add(int(v))
        elif ps.endswith("costs|[]") and node.get("trait"):
            out[str(node["trait"])].add(int(v))
    return {k: sorted(v) for k, v in out.items()}


def _cast_meter_rungs(game):
    """{npc.trait: sorted distinct thresholds} over per-character content gates.

    The roster half of `_meter_rungs`. Same rule — conditions, not quest cards —
    read off `subject = "npc"` predicates instead of the declared player tiers,
    because a roster game spreads its climb across the cast and leaves
    `ascent_tiers` empty by definition (`the-meters.md` W1).
    """
    out = collections.defaultdict(set)
    for path, node in _walk_paths(game):
        if "quest_cards" in "|".join(path) or node.get("subject") != "npc":
            continue
        if node.get("type") != "trait" or not node.get("trait_key"):
            continue
        v = node.get("value")
        if not isinstance(v, (int, float)) or not 0 < v <= METER_MAX:
            continue
        out[f"{node.get('npc_id') or '?'}.{node['trait_key']}"].add(int(v))
    return {k: sorted(v) for k, v in out.items()}


# Field, live player ascent meters, content gates only (see the instrument note):
#   family-ties you.corr 17 rungs · free-cities rep 17 · corpo-life lust 11 ·
#   the-company horny 11 · DoL exhibitionism 11 · become-someone mc.dom 9 ·
#   friends-of-mine feminine 8.
# Lowest rung: 5, 1000, 10, 2, 15, 5, 5 — median 5.
#
# `free-cities` was added by the 2026-08-24 recheck and lands exactly on the existing
# maximum, so the 8-17 band and the median-5 first rung are both UNCHANGED. Its rungs
# run 1000..12000 because reputation there is priced in the arcology's own scale; the
# rung COUNT is what this constant reads, never the values.
FIELD_METER_RUNGS      = 8
FIELD_METER_FIRST_RUNG = 5

# ⚠️ THE 8-17 ABOVE IS A PLAYER-ASCENT NUMBER AND DOES NOT TRANSFER TO THE CAST.
# It was measured on the ONE meter that carries a game -- you.corr, feminine, lust,
# mc.dom -- and until 2026-08-24 lint_meter_ladder printed it on both sides of W1's
# fork, so a roster game was told it was six rungs short of a yardstick taken from a
# different kind of meter.
#
# MEASURED per-character, section E (findings_E_yes.md), pooled over 13 corpus games
# carrying a per-person willingness meter on 3+ people:
#     rungs per person   median 3   (p25 2, p75 6)
#     lowest rung        median 5   <- the SAME as the ascent number, so only the
#                                      rung-count half of the comparator was wrong
# Per game: become-someone `trust` 5 · patriarch `like` 6 · destroyer `relation` 3 ·
# zaras-school-life `relationship` 2 · the-hellfire-club `love` 5.
FIELD_CAST_METER_RUNGS_LO  = 2
FIELD_CAST_METER_RUNGS_MED = 3
FIELD_CAST_METER_RUNGS_HI  = 6


def lint_meter_ladder(game, state):
    """Per meter that carries the game: how many rungs, and where the lowest sits.

    Which meters those ARE follows `board.who_climbs`, because W1 makes that a
    declared fork: a ladder game's climb is the tiers it names, a roster game's
    is spread across the cast and leaves `ascent_tiers` empty. Reading only the
    named tiers measured the ladder games and printed NOTHING for the one roster
    game in the repo — half a fork is not an instrument.

    ⚠️ EACH BRANCH GETS ITS OWN FIELD NUMBER, since 2026-08-24. A declared tier is
    judged against player-ascent meters (8-17 rungs); a cast meter against the field's
    per-character willingness meters (2-6, median 3). Printing the ascent number beside
    a roster game told `off_season` its 5-rung cast meters were short of 8 when the
    field's per-character median is 3 -- it was already above it.

    A NUMBER, never a bar. A rung count is only comparable between meters on the
    same 0-100 scale, and a game is free to run a two-rung meter on purpose.
    What is worth seeing is that every meter in every v2 game so far reads
    15/35/55/75 — the DoL seed's spacing, promoted to a copyable example in
    `the-board.md` and reproduced across five games — all 16 declared tiers put
    their lowest rung at exactly 15.
    """
    board = (state or {}).get("board") or {}
    tiers = board.get("ascent_tiers") or []
    comparator = (f"field {FIELD_METER_RUNGS}-17 rungs, "
                  f"lowest at {FIELD_METER_FIRST_RUNG}")
    if tiers:
        rungs = _meter_rungs(game)
        rows = [(t, rungs.get(t) or []) for t in tiers]
        label, noun = "declared tiers", "tiers"
    elif str(board.get("who_climbs") or "").lower() == "cast":
        rows = sorted(_cast_meter_rungs(game).items())
        label, noun = "cast meters", "meters"
        comparator = (f"field {FIELD_CAST_METER_RUNGS_LO}-{FIELD_CAST_METER_RUNGS_HI} rungs "
                      f"(median {FIELD_CAST_METER_RUNGS_MED}), lowest at {FIELD_METER_FIRST_RUNG}")
    else:
        return "", []
    if not rows:
        return "", []
    late = [(t, r) for t, r in rows if r and r[0] > FIELD_METER_FIRST_RUNG]
    summary = (f"{len(rows)} {label} · median {_median([len(r) for _, r in rows]):.0f} rungs "
               f"· lowest rung {min([r[0] for _, r in rows if r] or [0])} "
               f"· {comparator}")
    findings = [f"{t}: {len(r)} rung(s) {r or '—'}" for t, r in rows]
    if late:
        findings.append(f"{len(late)} of {len(rows)} {noun} change nothing below "
                        f"{min(r[0] for _, r in late)} — that is the opening of the game "
                        f"with no feedback in it")
    return summary, findings


def lint_cast_meters(game, state):
    """Per character: which meters they own, and how many gates each carries.

    The field runs 285 per-character meters against 101 player-owned ones, and it
    SPLITS — 8 games put 65%+ of their character-gating on per-character meters,
    9 put 13% or less, and nothing sits between. A roster of identical
    `relation = 0` is a legitimate answer for a ladder game and the whole engine
    missing from a roster one; this prints which you built.
    """
    npcs = game.get("npcs") or []
    if not npcs:
        return "", []
    _, per_npc = _school_split(game, state)
    gates = collections.Counter()
    for k, v in per_npc.items():
        gates[k.split(".", 1)[0]] += v
    rows = []
    for n in npcs:
        nid = str(n.get("id") or "—")
        traits = sorted((n.get("core_traits") or {}).keys())
        rows.append((nid, traits, gates.get(nid, 0)))
    shapes = {tuple(t) for _, t, _ in rows}
    ungated = [nid for nid, _, g in rows if not g]
    summary = (f"{len(rows)} characters · {len(shapes)} distinct meter shape(s) "
               f"· {sum(g for _, _, g in rows)} per-character gate sites"
               + (f" · {len(ungated)} character(s) gate nothing" if ungated else ""))
    findings = [f"{nid}: {', '.join(t) or 'no meters'} — {g} gate site(s)" for nid, t, g in rows[:10]]
    return summary, findings


def lint_counterweight(game, state):
    """A player meter that runs DOWN: does it shut anything?

    One game in 25 ships a counterweight that gates (DoL `purity`, 84 gates).
    Four of our five v2 games ship one, and three of those gate almost nothing:
    `count` 0 reads, `standing` 2, `grace` 5.

    ⚠️ HEURISTIC, which is why this is a lint. Nothing in the TOML declares
    "counterweight", so it is inferred: a player trait starting at 50+ whose
    `add` effects are mostly negative. Declared needs are excluded — energy
    matches the same shape and is a different kind of meter entirely (M8).
    """
    core = ((game.get("player") or {}).get("core_traits") or {})
    needs = {str(n.get("key")) for n in _declared_needs(state)}
    decay = set((game.get("player") or {}).get("trait_decay") or {})
    up, down = collections.Counter(), collections.Counter()
    for path, node in _walk_paths(game):
        if not "|".join(path).endswith("effects|[]"):
            continue
        if node.get("op") != "add" or node.get("targetType", "player") != "player":
            continue
        v = node.get("value")
        if not isinstance(v, (int, float)):
            continue
        (up if v > 0 else down)[str(node.get("trait"))] += 1
    read = _traits_read_anywhere(game)
    rows = []
    for t, init in core.items():
        if t in needs or t in decay:
            continue
        if isinstance(init, (int, float)) and init >= 50 and down[t] > up[t]:
            rows.append((t, int(init), up[t], down[t], read.get(t, 0)))
    if not rows:
        return "", []
    summary = (f"{len(rows)} falling meter(s) · "
               + " · ".join(f"{t} {r} read(s)" for t, _, _, _, r in rows)
               + " · field: 1 game in 25 has one, at 84 gates")
    return summary, [f"{t}: starts at {init}, {d} drop(s) against {u} rise(s), read {r} time(s)"
                     + ("  — it costs her something and buys the player nothing" if r < 3 else "")
                     for t, init, u, d, r in rows]




# ─────────────────────────────────────────────────────────────────────────────
# The words the player has to already own
# ─────────────────────────────────────────────────────────────────────────────
# `scripts/genre_words.txt` is every lowercase word used by FOUR OR MORE of the 27
# parseable games in the mopoga corpus — 20,555 words out of 14.7M. It is data, not
# taste: a word missing from it is not banned, it is a word the genre does not reach
# for.
#
# ⚠️ IT WAS 18,043 WORDS FROM 25 GAMES UNTIL 2026-08-24. `college-daze` and
# `free-cities` parsed to zero, so a quarter of the corpus by volume was reported as
# vocabulary the genre does not use. Rebuilding on 27 added 1,976 words and dropped
# none — the file is a UNION with the old list, never a replacement.
GENRE_WORDS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "genre_words.txt")
_GENRE_WORDS_CACHE = None

_CALENDAR = set("""january february march april may june july august september october
november december monday tuesday wednesday thursday friday saturday sunday""".split())

# Number words, plain and compounded. A game that counts money in words writes
# `thirty-one` and `eighty-nine` constantly, and the genre — which writes `$31` —
# never does. That is a notation difference, not a vocabulary problem.
_NUM_UNIT = ("one two three four five six seven eight nine ten eleven twelve thirteen "
             "fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty "
             "fifty sixty seventy eighty ninety hundred thousand").split()
_NUM_WORD = re.compile(r"^(?:%s)(?:-(?:%s))*$" % ("|".join(_NUM_UNIT), "|".join(_NUM_UNIT)))

_WORD_TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]*")


# ⚠️ CURATED, and it has to be. A false friend is BY DEFINITION a common word — `vest`,
# `tea`, `bonnet` are all used by 4+ field games, so `genre_words.txt` is structurally
# blind to them. This is the half of the check that no corpus can supply, kept short on
# purpose: a lint that cries wolf gets ignored (see `_OBJ_STOP` above, same lesson).
# Only entries verified by reading real lines in our own games are listed.
#
# ⚠️ A WORD `register.md` NAMES AS A DEFECT BELONGS IN HERE. The four additions dated
#    2026-08-23 were all sitting in that file already and in none of this dict:
#    `meter` is the FIRST example in the section ("The words the player has to already
#    own"), and `pitch` and `float` are both in its required-swap list. A false friend is
#    by definition a common word, so `genre_words.txt` can never surface one — if this
#    dict does not carry it, nothing in the instrument does. Reconcile the two on every
#    edit to either.
#
# ⚠️ MEASURED AND REJECTED — do not re-propose without new evidence. Counts are uses in
#    player-visible text across the 20 built games (269,421 words), read line by line:
#      front  ×334  "the front door", "in front of" — noise
#      inside ×213  "inside the room" — noise
#      tip     ×44  only back_home's 3 ("the desk went to the tip") are the dump sense
#      boot     ×8  every use is footwear; not one car boot in the repo
#      bill     ×7  invoice and banknote are both common; no defect present
#      purse   ×10  a wrong picture, but it does not cost the scene; 5 of 10 correct
#    The bar is not "could be misread" — it is "misreads badly enough to cost the
#    reader the line, often enough to be worth the false positives."
_FALSE_FRIENDS = {
    "vest":    "an undershirt here, a waistcoat to most readers",
    "tea":     "the evening meal here, a hot drink to most readers",
    "bonnet":  "a car hood here, a hat to most readers",
    "jumper":  "a sweater here, a pinafore or someone jumping to most readers",
    "braces":  "suspenders here, teeth braces to most readers",
    "torch":   "a flashlight here, a burning brand to most readers",
    "biscuit": "a cookie here, a soft savoury roll to most readers",
    "dummy":   "a pacifier here, a mannequin to most readers",
    "fringe":  "a haircut here, an edge to most readers",
    # Added 2026-08-23. `meter` is the one that reached a player: LO hit the button
    # `Feed the meter ($3)` in the built off_season and could not read it — and it is
    # the first entry here whose clash is with OUR OWN UI rather than with a dialect.
    # In this genre a meter is a stat bar, and that game renders four in its sidebar.
    # Same exposure, unmeasured so far: board, card, flag, state, tier, rung.
    "meter":   "a coin-fed prepayment box here, a stat bar to most players",
    "float":   "the till's starting cash here, something buoyant to most readers",
    "pitch":   "the rent on a trading spot here, a sound or a throw to most readers",
    "chemist": "a pharmacy here, a scientist to most readers",
}
# `half seven` is 7:30 in Britain, 6:30 across much of Europe, and not a construction
# American English uses at all. Measured: 157 uses across six of our games against 4
# uses of the unambiguous `half past`.
_HALF_HOUR = re.compile(
    r"\bhalf\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b", re.I)

# This skill's OWN vocabulary, dropped only by `--words` (never by the game lint).
#
# A design document is not player-visible text: a Want legitimately says "tier" and
# "ratcheting" forty times, and a report where 41 of 46 rows are this skill talking to
# itself is a report the author skims. The count is always printed beside the summary,
# so the suppression is visible rather than silent.
#
# ⚠️ EVERY ENTRY HERE IS A WORD THE CHECK CAN NO LONGER SEE, so the bias is toward
# KEEPING words visible. This lint is a list a human reads: a false positive costs one
# skimmed row, a false negative costs a shipped word. Only unambiguous authoring jargon
# goes in.
#
# ⚠️ CONSIDERED AND REJECTED — each could name a real thing in a porn sandbox, which is
# the whole test:
#     odometer   a truck has one            slug       an animal
#     lint       comes out of a dryer       dispatcher a real job
#     rungs      a ladder has them          scoreboard a real object
#     downstream / fandom — not this skill's vocabulary in the first place
#
# Terms already in `genre_words.txt` (ascent, cascade, hub, meter, rung, surface,
# throttle, tier, canvas, gate, instrument, sandbox, repeatable) are omitted: they can
# never reach the list anyway, so naming them here would be decoration.
#
# `meter` is here for the FALSE-FRIEND half only. In game prose it is a real false
# friend — a coin-fed prepayment box to some readers, a stat bar to others — but in a
# design document it means the stat bar on purpose, so warning about it is the check
# arguing with the vocabulary it is written in.
_SKILL_META = frozenset("""
authoring canvases capstone corpus doctrine gating linted meter milestone milestones
ratcheting sandboxes schema taxonomy tiers toml verifier walkin
""".split())

def _genre_words():
    """The field's shared vocabulary. Empty set if the table is missing — the lint
    then reports nothing rather than reporting everything."""
    global _GENRE_WORDS_CACHE
    if _GENRE_WORDS_CACHE is None:
        try:
            with open(GENRE_WORDS_PATH) as fh:
                _GENRE_WORDS_CACHE = {ln.strip() for ln in fh
                                      if ln.strip() and not ln.startswith("#")}
        except OSError:
            _GENRE_WORDS_CACHE = set()
    return _GENRE_WORDS_CACHE


def _player_visible_text(model, game):
    """Every word the player actually reads: canvas prose, choice labels, room text.

    Labels are in scope even though `the-voice.md` owns their SHAPE, because a word
    the player cannot decode is undecodable on a button too — the measured trigger
    was `Buy a coin mech off the chandlery`, where both hard words are on the label
    and neither is anywhere in the prose behind it.
    """
    parts = [t for c in model for b in c["beats"] for t in b.text]
    for _path, node in _walk_paths(game):
        if isinstance(node.get("text"), str) and ("targetType" in node or "config" in node):
            parts.append(node["text"])
    for loc in (game.get("locations") or []):
        if loc.get("description"):
            parts.append(str(loc["description"]))
        if loc.get("name"):
            parts.append(str(loc["name"]))
    return "\n".join(parts)


def own_words_report(text, declared_names=(), suppress=frozenset(), shown=20):
    """Words in a body of text that the genre does not use — a LIST, not a score.

    Off Season scores 86.8 Flesch, easier than 24 of the 25 field games, and LO
    could not read it. Sentence length and syllable count both pass a game whose
    difficulty is REFERENTIAL: `immersion`, `airer`, `chandlery`, `forecourt` are
    short, common-looking words naming objects the reader must already own.

    ⚠️ A LIST AND NEVER A GATE. The rate does not discriminate: with names, months
    and number-words filtered out, `vesper` — which reads fine — runs 190 per 10k
    and off_season runs 254. What separates them is what the words ARE. `emitter`
    and `sternum` are built by the fiction; `immersion` and `airer` cannot be,
    because a real object either lands with the reader or it does not. That is a
    judgement, so the check hands over the words and the author makes it.
    `references/register.md`, "The words the player has to already own".

    ⚠️ This takes TEXT, not a parsed game, so the same instrument can run in the
    WANT phase — before a location has been named or a button written. It used to
    be reachable only from a built game, which is one phase too late: by then the
    vocabulary is already set into room names and labels and fixing it means
    renaming things. `the_season`'s Want shipped `rota` and `ledger` past a author
    who had committed, one message earlier, to avoiding exactly that class.

    `declared_names` — names the fiction teaches (a game's cast and places), which
    are never words the player had to arrive holding.
    `suppress` — terms to drop from the list. Used ONLY by `--words` for this
    skill's own vocabulary, which a design document legitimately contains; the
    count is always printed so nothing is hidden silently.
    `shown` — how many rows to print, or None for all. A whole game needs the cap;
    a one-page design document does not, and the cap hid the exact word this mode
    was built to catch — `rota` ×1 sorted into the tail behind twenty commoner ones.
    """
    genre = _genre_words()
    if not genre:
        return "", []

    # A proper noun is capitalised where a sentence does not force it. This finds the
    # game's own cast and places with no hand-maintained list, which is the point:
    # a name the fiction teaches is not a word the player had to arrive holding.
    mid, cap, uses = collections.Counter(), collections.Counter(), collections.Counter()
    for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
        toks = _WORD_TOKEN.findall(sent)
        for i, w in enumerate(toks):
            lw = w.lower()
            # A literal possessive only. `rstrip("'s")` strips ANY trailing s and
            # turned `goes` into `goe` and `this` into `thi` on the first run.
            if lw.endswith("'s"):
                lw = lw[:-2]
            elif lw.endswith("'"):
                lw = lw[:-1]
            if len(lw) < 3:
                continue
            uses[lw] += 1
            if i:                                    # not sentence-initial
                mid[lw] += 1
                if w[0].isupper():
                    cap[lw] += 1
    proper = {w for w in mid if mid[w] >= 2 and cap[w] / mid[w] > 0.6}
    # Plus every name the caller DECLARES. A cast member mentioned twice, both times
    # at the head of a sentence, is invisible to the capitalisation test.
    for name in declared_names:
        for w in _WORD_TOKEN.findall(str(name or "").replace("_", " ")):
            proper.add(w.lower())

    rare = {w: n for w, n in uses.items()
            if w not in genre and w not in proper and w not in _CALENDAR
            and not _NUM_WORD.match(w) and "-" not in w}
    # Counted BEFORE the drop, so the report can say how much it is not showing.
    muted = sorted(w for w in rare if w in suppress)
    for w in muted:
        del rare[w]
    total = sum(uses.values()) or 1
    if not rare:
        return (f"0 of {total:,} words sit outside the field's shared vocabulary"
                + (f" · {len(muted)} meta term(s) suppressed" if muted else ""), [])

    ranked = sorted(rare.items(), key=lambda kv: (-kv[1], kv[0]))
    SHOWN = len(ranked) if shown is None else shown
    findings = [f"{w} ×{n}" for w, n in ranked[:SHOWN]]
    # A list that hides two thirds of itself is not a list. off_season printed 20 rows
    # under a summary that said 67, and the 47 it swallowed included words already in
    # the player's face.
    if len(ranked) > SHOWN:
        rest = sum(n for _w, n in ranked[SHOWN:])
        findings.append(f"… and {len(ranked) - SHOWN} more word(s), {rest} use(s), not "
                        f"printed — re-run with --json for the full list")

    # The second half: words the corpus cannot flag because they are perfectly common.
    amb = len(_HALF_HOUR.findall(text))
    if amb:
        findings.append(f"[ambiguous] `half <hour>` ×{amb} — 7:30 here, 6:30 across much of "
                        f"Europe, and not used at all in American English. `half past` is the "
                        f"version that survives")
    # ⚠️ COUNT THE PLURAL TOO. `uses` is a bag of singular tokens, so the first version
    # of this read `vest` and never `vests` — and forty_miles carries both. Missed
    # `vests` ×2, `torches` ×2 and `biscuits` ×1 across the repo before this was added.
    def _ff_uses(w):
        return uses.get(w, 0) + uses.get(w + "s", 0) + uses.get(w + "es", 0)
    ff = [(w, _ff_uses(w)) for w in _FALSE_FRIENDS if _ff_uses(w) and w not in suppress]
    for w, n in sorted(ff, key=lambda kv: -kv[1]):
        findings.append(f"[false friend] {w} ×{n} — {_FALSE_FRIENDS[w]}")

    summary = (f"{len(ranked)} word(s) the 27-game field does not use, "
               f"{sum(rare.values())} use(s) across {total:,} words"
               + (f" · plus {amb} ambiguous and {len(ff)} false-friend term(s)" if (amb or ff) else "")
               + (f" · {len(muted)} meta term(s) suppressed" if muted else "")
               + " · read the list, do not read the number")
    return summary, findings


def lint_own_words(model, game):
    """`own_words_report` over everything the player actually reads in a built game.

    The names the fiction teaches come from the game's own declarations, so no
    hand-maintained cast list is needed.
    """
    names = [decl.get(field)
             for decl in list(game.get("npcs") or []) + list(game.get("locations") or [])
             for field in ("name", "id")]
    return own_words_report(_player_visible_text(model, game), names)

def _walkin_join(model, game):
    """The activity x schedule JOIN. `the-surfaces.md` R3.

    A location QUALIFIES when she does solo work there AND at least one character
    is scheduled there — then someone can walk in on her. Not a judgement: it is
    already true in the board. Returns (qualifying, covered, rows).
    """
    sched = collections.defaultdict(set)
    for npc in (game.get("npcs") or []):
        for r in (npc.get("schedules") or []):
            loc = r.get("location") or r.get("location_id")
            if loc:
                sched[loc].add(npc.get("id"))

    solo = collections.defaultdict(list)
    subs = collections.Counter()
    for c in model:
        t = (c.get("raw") or {}).get("trigger") or {}
        loc = t.get("location")
        if not loc or not t.get("is_repeatable"):
            continue
        if (t.get("trigger_mode") == "random" or t.get("npc")
                or t.get("requires_npc") or t.get("substitution_only")):
            continue
        solo[loc].append(c["id"])
        subs[loc] += len(t.get("substitutions") or [])

    qualifying = [l for l in solo if sched.get(l)]
    covered = [l for l in qualifying if subs[l] > 0]
    return qualifying, covered, (solo, sched, subs)


def _exit_holders(canvas_nodes):
    """Every place on a canvas that can carry effects/flagEffects/time."""
    out = []
    for n in canvas_nodes or []:
        eb = n.get("exit_block") or {}
        out.append(eb.get("config") or {})
        out.extend(eb.get("choices") or [])
    return out


def _tick_cleared(game):
    """Flags `[engine.daily_tick]` unsets on the day roll — the third part of a day cap."""
    out = set()
    for fe in (((game.get("engine") or {}).get("daily_tick") or {}).get("flagEffects") or []):
        if fe.get("op") in ("unset", "clear") and fe.get("flag"):
            out.add(fe["flag"])
    return out


def _holder_day_capped(holder, cleared):
    """Is this ONE choice self-capped to once a day?

    The three-part cap, all of it on the same choice: its `conditions` read a flag
    `is_false`, its own `flagEffects` set that flag, and `[engine.daily_tick]` clears it.
    Clicking it once shuts it until the day rolls.

    ⚠️ WHY THIS EXISTS. `_routes` already knows this pattern, but only for a choice that
    routes into ANOTHER CANVAS — it keys on `nodeId`. A walk-in's own exit choice targets
    a LOCATION, so it produces no route at all, `_is_free` fell through to the trigger,
    and the climb gate reported rungs as farmable that the engine will not serve twice in
    a day. Measured on `the_season`: `walkin_showers_wade` is guarded by
    `wade_rung_today is_false` and sets it, and the gate said "9 clicks, no cap."

    That is the family `_farmable`'s docstring above already documents twice, and
    `SKILL.md`'s rule — *a check that fails a game for obeying the doctrine is a bug in
    the check.* Both gates' own remediation text tells the author to do exactly this:
    "day-cap the rung with a flag cleared in [engine.daily_tick]."
    """
    if not cleared:
        return False
    sets = {fe.get("flag") for fe in (holder.get("flagEffects") or [])
            if fe.get("op") == "set" and fe.get("flag")}
    if not sets:
        return False
    for it in _conditions_of(holder):
        fk = it.get("flag_key")
        if fk and fk in sets and fk in cleared and it.get("operator") in ("is_false", "is_not_true"):
            return True
    return False


def _grants(canvas_nodes, cleared=frozenset()):
    """(subject, npcId, trait) -> total POSITIVE add on this canvas's exits, plus its time cost.

    Only `add` with a positive value counts as a grant. `set` is not a climb, and a
    negative add is a charge. Mirrors the engine's live-op list (engine.md §21b).

    A choice that day-caps ITSELF grants nothing farmable — see `_holder_day_capped`.
    """
    got, minutes = collections.Counter(), 0
    for h in _exit_holders(canvas_nodes):
        if _holder_day_capped(h, cleared):
            continue
        t = h.get("time_progression_minutes")
        if isinstance(t, (int, float)):
            minutes = max(minutes, int(t))
        for ef in (h.get("effects") or []):
            if ef.get("op") != "add":
                continue
            key = ef.get("trait") or ef.get("trait_key")
            if not key:
                continue
            sign = _effect_value_sign(ef.get("value"))
            if sign <= 0:
                continue
            val = ef.get("value")
            amt = val if isinstance(val, (int, float)) else (val or {}).get("max", 1)
            subject = "npc" if ef.get("npcId") else "player"
            got[(subject, ef.get("npcId"), key)] += float(amt)
    return got, minutes


def _is_dev(canvas):
    """A canvas the engine excludes from a shipped build.

    `dev_mode_enabled is_true` in the trigger conditions is a MARKER, not a gate — the
    generator tests for exactly this to strip dev shortcuts (`v2.py:8428-8452`), and the
    flag is set at StoryInit only in `--dev` builds (`v2.py:1080`). No canvas sets it and
    none should.
    """
    for it in _conditions_of(canvas.get("trigger") or {}):
        if it.get("flag_key") == "dev_mode_enabled" and it.get("operator") == "is_true":
            return True
    return False


def _farmable(canvas):
    """Can a player actually enter this more than once in a shipped build?

    ⚠️ THE CLASS THIS CLOSES, found by an author on 2026-08-17 and named in their game's
    ENGINE_NOTES: *gates.py was scoring canvases the engine cannot reach in a shipped
    build.* Two instances, both mine, both introduced with G26 the day before:

      * a ONE-SHOT canvas counted as farmable. The opening funnel — `is_repeatable =
        false`, no canvas linking into it, the game's own starting canvas — was reported as
        "14 clicks of canvas_opening" to reach cover 55. The only way to satisfy that gate
        was to put a `costs` block on the game's intro, charging the player energy to read
        it: a real defect introduced purely to please a check.
      * a DEV SHORTCUT counted as player-facing content, which cost the author a
        1-energy `costs` on every dev choice to silence it.

    Both are the failure SKILL.md already names — *a check that fails a game for obeying
    the doctrine is a bug in the check* — and this is its fourth and fifth measured
    instance. The file already knew how to read `is_repeatable` (see IS_REPEATABLE_DEFAULT
    and `build()`); the climb gate simply never consulted it.
    """
    trig = canvas.get("trigger") or {}
    if _is_dev(canvas):
        return False
    return bool(trig.get("is_repeatable", IS_REPEATABLE_DEFAULT)) if trig else IS_REPEATABLE_DEFAULT


def _routes(model, game):
    """canvas_id -> list of routes that reach it, each marked braked or free.

    A RUNG in this architecture is a triggerless canvas reached by a hub choice, so the
    brake almost never lives on the rung — it lives on the choice, or on a flag the rung
    sets and the choice reads. Gate 18 used to look only at `trigger.costs`, which is
    always empty for a triggerless rung, so every real brake in the game was invisible
    to it.

    A route is BRAKED when any of these hold:
      * the choice carries `costs`               — engine-enforced (engine.md §27)
      * the target canvas trigger has max_triggers_per_day  (engine.md §28)
      * the choice is gated on something the TARGET itself moves — the `_today` pattern:
        a flag the target sets, read `is_false`; or an `lt`/`lte` on a trait the target
        increments. That is self-limiting, which a plain tier gate is not.
    """
    by_id = {c["id"]: c for c in (game.get("canvases") or [])}
    sets_flag, bumps_trait = {}, {}
    for cid, c in by_id.items():
        f, t = set(), set()
        for h in _exit_holders(c.get("nodes")):
            for fe in (h.get("flagEffects") or []):
                if fe.get("flag"):
                    f.add(fe["flag"])
            for ef in (h.get("effects") or []):
                k = ef.get("trait") or ef.get("trait_key")
                if k:
                    t.add(k)
        sets_flag[cid], bumps_trait[cid] = f, t

    routes = collections.defaultdict(list)
    for c in (game.get("canvases") or []):
        for n in c.get("nodes") or []:
            eb = n.get("exit_block") or {}
            for ch in (eb.get("choices") or []):
                tgt = (ch.get("nodeId") or "").split(".", 1)[0]
                if not tgt or tgt == c["id"] or tgt not in by_id:
                    continue
                costs = ch.get("costs") or []
                if isinstance(costs, dict):
                    costs = [costs]
                perday = bool((by_id[tgt].get("trigger") or {}).get("max_triggers_per_day"))
                # The choice may day-cap ITSELF — guard on a flag it sets, cleared on the
                # tick. That is the shape §16 forces on a triggerless rung: the rung has
                # no location, so the flag CANNOT live on its exit and has to sit on the
                # hub choice instead. Without this the engine's own required pattern
                # reads as an unbraked route into every act loop in the repo.
                selflimit = _holder_day_capped(ch, _tick_cleared(game))
                for it in _conditions_of(ch):
                    fk, tk, op = it.get("flag_key"), it.get("trait_key"), it.get("operator")
                    if fk and fk in sets_flag.get(tgt, ()) and op in ("is_false", "is_not_true"):
                        selflimit = True
                    if tk and tk in bumps_trait.get(tgt, ()) and op in ("lt", "lte"):
                        selflimit = True
                # What this route demands of each trait, so a climb simulation cannot
                # spend a rung to reach the very threshold that rung is locked behind.
                reqs = {}
                for holder in (ch, by_id[tgt].get("trigger") or {}):
                    for it in _conditions_of(holder):
                        tk, op, v = it.get("trait_key"), it.get("operator"), it.get("value")
                        if tk and op in ("gte", "gt") and isinstance(v, (int, float)):
                            reqs[tk] = max(reqs.get(tk, 0.0), float(v))
                routes[tgt].append(dict(
                    src=c["id"], costs=bool(costs), perday=perday, selflimit=selflimit,
                    reqs=reqs, braked=bool(costs) or perday or selflimit))
    return routes


def _free_climb(top, grants, start=0.0):
    """Cheapest FREE climb from `start` to `top`, or None if the meter cannot be farmed there.

    grants: [(canvas_id, amount, minutes, requirement_on_this_same_trait)].

    Simulated one click at a time, because a rung locked at 15 legitimately becomes the
    fastest route once 15 is reached — and because the naive version of this check picked
    a +3 rung to explain reaching 55 when that rung was itself gated at 55.

    Two deliberate simplifications, both erring toward UNDER-reporting the grind:
      * only same-trait requirements are honoured. A rung also gated on a different
        meter, an NPC or a flag may not really be available this early, so the true
        click count can be higher than reported — never lower.
      * decay and clamping are ignored. Both make the real climb longer.
    """
    # A meter that already satisfies the gate at game start was never climbed, so it
    # cannot have been climbed for free. Without this, `energy` starting at 100 against
    # a gate at 25 reported "entirely for FREE — 0 clicks, 0m of game time" — which
    # describes no climb at all. Zero clicks is not farming; it is a starting value.
    if float(start) >= top:
        return None
    v, clicks, mins, used = float(start), 0, 0.0, collections.Counter()
    while v < top and clicks < 5000:
        avail = [g for g in grants if g[3] <= v]
        if not avail:
            return None
        cid, amt, m, _r = min(avail, key=lambda g: ((g[2] or 0) / g[1], -g[1]))
        v += amt
        mins += (m or 0)
        clicks += 1
        used[cid] += 1
    return None if v < top else (clicks, mins, used)


def _is_free(cid, routes, game):
    """A canvas is FREE when at least one way in has no brake on it.

    Min over routes, never max: one unbraked door makes the whole rung farmable, no
    matter how well priced the other doors are.
    """
    canvas = next((c for c in (game.get("canvases") or []) if c.get("id") == cid), None) or {}
    trig = canvas.get("trigger") or {}
    if trig.get("max_triggers_per_day") or trig.get("costs"):
        return False
    # The same three-part day cap, SPLIT: the guard on the trigger, the setter on a
    # choice inside. The canvas stops rendering the moment the flag is set, so it is
    # capped just as hard as if both halves sat on one choice — and this is the more
    # common shape, because a whole activity is usually what a day cap is for.
    cleared = _tick_cleared(game)
    if cleared:
        sets = {fe.get("flag") for h in _exit_holders(canvas.get("nodes"))
                for fe in (h.get("flagEffects") or [])
                if fe.get("op") == "set" and fe.get("flag")}
        for it in _conditions_of(trig):
            fk = it.get("flag_key")
            if fk and fk in sets and fk in cleared and it.get("operator") in ("is_false", "is_not_true"):
                return False
    rs = routes.get(cid)
    if not rs:                      # auto-firing / unreferenced: its own trigger is the only brake
        return not (trig.get("max_triggers_per_day") or trig.get("costs"))
    return any(not r["braked"] for r in rs)


def _hms(minutes):
    minutes = int(round(minutes))
    d, rem = divmod(minutes, 60 * 24)
    h, m = divmod(rem, 60)
    if d:
        return f"{d}d {h}h{m:02d}m"
    return f"{h}h{m:02d}m" if h else f"{m}m"


# ─────────────────────────────────────────────────────────────────────────────
# The first hour — the opening, the meetings, and the first visit
# Doctrine: references/the-first-hour.md.  Added 2026-08-22 after the first v2 game
# a human read end to end scored 31/32 and was unplayable for its first ten minutes.
# ─────────────────────────────────────────────────────────────────────────────
FUNNEL_DEFAULT_STEP = 3
# v2.py:13200 — `config.get('default_time_progression', 3)`. A node exit that does not
# declare `time_progression_minutes` still costs three minutes, so the handover clock is
# NEVER the starting hour. The game that prompted this landed at 07:36 from a 07:00 start
# without anyone computing it.


def _fh_blocks(blocks):
    """Every block on a node, descending into `group` and `cascade` containers."""
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        yield b
        yield from _fh_blocks(b.get("blocks"))
        for beat in ((b.get("props") or {}).get("beats") or []):
            yield from _fh_blocks(beat.get("blocks"))


def _fh_in_window(minute, start, end):
    """Is this clock minute inside a schedule row? Wraps past midnight.

    An unparseable window returns True — an instrument that cannot read a row must
    not convict on it.
    """
    def parse(t):
        try:
            h, m = str(t).split(":")[:2]
            return int(h) * 60 + int(m)
        except Exception:
            return None
    s, e = parse(start), parse(end)
    if s is None or e is None:
        return True
    m = minute % (24 * 60)
    return (s <= m < e) if s <= e else (m >= s or m < e)


def _fh_handovers(game):
    """Every (clock_minute, location_id) at which the opening can hand over.

    A BRANCHING walk, not a single spine: an opening with two exits passes if EITHER
    lands somewhere open. Returns ([], reason) when the chain cannot be walked, and the
    gate then reports n/a — an unresolvable walk is an instrument failure, not a defect.
    """
    start = (game.get("project") or {}).get("starting_canvas")
    base = int((game.get("time") or {}).get("starting_hour") or 8) * 60
    op = next((c for c in (game.get("canvases") or [])
               if c.get("id") == start or c.get("name") == start), None)
    if not op:
        return [], "no starting canvas is declared"
    nodes = {n.get("id"): n for n in (op.get("nodes") or []) if n.get("id")}
    first = ((op.get("nodes") or [None]) or [None])[0]
    if first is None:
        return [], "the opening canvas has no nodes"
    out, seen, stack = [], set(), [(first, base, 0)]
    while stack:
        node, clock, depth = stack.pop()
        key = (node.get("id"), clock)
        if key in seen or depth > 60:
            continue
        seen.add(key)
        eb = node.get("exit_block") or {}
        holders = list(eb.get("choices") or []) or [eb.get("config") or {}]
        for h in holders:
            if not isinstance(h, dict):
                continue
            cfg = h.get("config") or h
            step = cfg.get("time_progression_minutes")
            nxt = clock + (int(step) if isinstance(step, (int, float))
                           else FUNNEL_DEFAULT_STEP)
            nid = h.get("nodeId") or cfg.get("nodeId")
            if nid:
                if nid in nodes:
                    stack.append((nodes[nid], nxt, depth + 1))
                continue
            loc = cfg.get("locationId") or h.get("locationId")
            if loc:
                out.append((nxt, loc))
    return out, ("ok" if out else "the funnel never exits to a location")


def _fh_live_at(game, loc, minute):
    """Canvases at `loc` a player could actually reach at `minute`, on purpose.

    Excluded, and each for a reason the doctrine states:
      · `trigger_mode = "random"`  — rolls a chance; the first screen of the open
        world cannot be a coin flip
      · `substitution_only = true` — only ever appears inside another canvas's
        trigger (filtered in selectAutoFireCanvasForLocation, v2.py:4459)
      · the starting canvas itself — it is the thing that just ended
    """
    start = (game.get("project") or {}).get("starting_canvas")
    live = []
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        if t.get("location") != loc:
            continue
        if c.get("id") == start or c.get("name") == start:
            continue
        if t.get("substitution_only") or t.get("trigger_mode") == "random":
            continue
        if t.get("is_active") is False:
            continue
        sched = t.get("schedules") or []
        if sched and not any(_fh_in_window(minute, s.get("start_time"), s.get("end_time"))
                             for s in sched if isinstance(s, dict)):
            continue
        live.append(c.get("id"))
    return live


def _fh_meeting_setters(game):
    """flag -> the characters a NON-REPEATABLE canvas that sets it names.

    A canvas "names" a character when it binds them (`npc` / `requires_npc`) or when
    somebody speaks as them anywhere on it. A one-shot that mentions nobody sets no
    meeting: a flag is not an introduction.
    """
    out = collections.defaultdict(set)
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        if t.get("is_repeatable"):
            continue
        npcs = {t[k] for k in ("requires_npc", "npc") if t.get(k)}
        for n in (c.get("nodes") or []):
            for b in _fh_blocks(n.get("blocks")):
                nid = (b.get("props") or {}).get("npcId")
                if nid:
                    npcs.add(nid)
        if not npcs:
            continue
        for h in _exit_holders(c.get("nodes")):
            for fe in (h.get("flagEffects") or []):
                if fe.get("flag"):
                    out[fe["flag"]] |= npcs
    return out


def _fh_cast_met(game):
    """(met, cast, flag_owners, cold) — who is introduced before their hub opens.

    A character counts as MET when BOTH hold:

      (a) at least ONE of their portrait hubs is gated on a flag set by a
          non-repeatable canvas that names them, and that flag opens no other
          character's hub;
      (b) NONE of their portrait hubs is completely ungated.

    (a) is the introduction. (b) is the cold-spawn ban — a second hub for the same
    character at another location, with no conditions at all, puts their portrait on a
    screen before the meeting has fired, which is the defect however well the first hub
    is gated (`the_inheritance/hub_richard`, `vesper/hub_sol_undertow`).

    ⚠️ (a) is deliberately ANY hub and not EVERY hub. A later rung — a sex loop gated on
    `audrey_stage gte 3`, an arrangement gated on `marcus_drinks_done` — is gated on
    something downstream of the meeting, and requiring the meeting flag on it too would
    fail a game for obeying the doctrine. First implementation of this gate did exactly
    that and read the_inheritance as 3/5 when it is 4/5.

    The `flag_owners` half is the other whole rule: three v2 games gated their entire
    cast on ONE flag — `rota_running`, `doors_open`, `arrival_done` — which passes a
    casual look and is the cold-spawn hub wearing a coat.
    """
    setters = _fh_meeting_setters(game)
    hubs = [c for c in (game.get("canvases") or [])
            if (c.get("trigger") or {}).get("npc")
            and (c.get("trigger") or {}).get("is_repeatable")
            and not _is_dev(c)]
    per_char = collections.defaultdict(list)
    flag_owners = collections.defaultdict(set)
    for c in hubs:
        t = c["trigger"]
        npc = t["npc"]
        items = list(_conditions_of(t))
        flags = {it.get("flag_key") for it in items if it.get("flag_key")}
        hit = sorted(f for f in flags if npc in setters.get(f, set()))
        per_char[npc].append((c.get("id"), hit, bool(items)))
        for f in hit:
            flag_owners[f].add(npc)
    met, cold = [], []
    for npc in sorted(per_char):
        rows = per_char[npc]
        bare = [cid for cid, _hit, gated in rows if not gated]
        if bare:
            cold.append((npc, bare))
            continue
        flags = {f for _cid, hit, _g in rows for f in hit}
        owned = {f for f in flags if len(flag_owners[f]) == 1}
        if owned:
            met.append(npc)
    return met, sorted(per_char), flag_owners, cold


def _fh_declared_anchor(game, state):
    """The location the LEDGER calls the anchor — largest declared `fill`.

    Same declare-then-check discipline as gate `location fill`: the author's own number
    decides, and the built distribution is only the fallback. Returns (id, source).
    """
    rows = [l for l in (((state or {}).get("board") or {}).get("locations") or [])
            if (l.get("fill") or l.get("budget"))]
    if rows:
        best = max(rows, key=lambda l: (l.get("fill") or l.get("budget") or 0))
        if best.get("id"):
            return best["id"], "declared"
    return None, "no ledger"


def _fh_first_visits(game):
    """location_id -> the non-repeatable canvases bound to it (its first visit)."""
    start = (game.get("project") or {}).get("starting_canvas")
    out = collections.defaultdict(list)
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        loc = t.get("location")
        if not loc or t.get("is_repeatable"):
            continue
        if c.get("id") == start or c.get("name") == start:
            continue
        if t.get("substitution_only"):
            continue
        out[loc].append(c.get("id"))
    return out


def lint_named_before_met(model, game):
    """Names the player is asked to hold before the game has earned them — a LIST.

    Two halves, one rule (`the-first-hour.md`: the game does not use a name until it has
    earned it):

      · PEOPLE — a character named in the opening, or on a quest card, or in a location
        description, who has no meeting anywhere. The measured failure named six people
        in 278 words, put none of them on screen, and two of the six are not in the game.
      · PLACES — a location the prose or the map sends the player to that has no
        first-visit canvas. A place whose FUNCTION is only implied is an unglossed noun
        the size of a room; the anchor of the game that prompted this was never once
        described as the kind of business it is, and the first thing the human reader
        asked was what it is.

    ⚠️ A LIST AND NEVER A GATE. Whether a name has been earned is a reading, not a
    measurement — a character can be legitimately named in passing (an offstage boss, a
    dead parent) and a corridor legitimately needs no introduction. The check hands over
    the names; the author makes the call.
    """
    npcs = [n for n in (game.get("npcs") or []) if n.get("id")]
    if not npcs:
        return "", []
    # ONE definition of "met" in this file, and it is the gate's. Deriving a second,
    # looser one here read off_season as 0 characters named before a meeting, because
    # `canvas_first_borrow` names Ewan and sets a flag — a mid-arc milestone gated on
    # `npc_ewan.hold gte 18`, which fires long after the player has been using the hub.
    met, _cast, _owners, _cold = _fh_cast_met(game)
    has_meeting = set(met)

    start = (game.get("project") or {}).get("starting_canvas")
    opening = next((c for c in (game.get("canvases") or [])
                    if c.get("id") == start or c.get("name") == start), None)
    opening_text = ""
    if opening:
        parts = []
        for n in (opening.get("nodes") or []):
            for b in _fh_blocks(n.get("blocks")):
                if isinstance(b.get("content"), str):
                    parts.append(b["content"])
            eb = n.get("exit_block") or {}
            for h in [eb.get("config") or {}] + list(eb.get("choices") or []):
                if isinstance(h, dict) and isinstance(h.get("text"), str):
                    parts.append(h["text"])
        opening_text = "\n".join(parts)

    card_text = "\n".join(
        str(v) for card in (game.get("quest_cards") or [])
        for k, v in card.items() if isinstance(v, str) and k != "id")
    place_text = "\n".join(str(l.get("description") or "")
                           for l in (game.get("locations") or []))

    # The name the prose will actually use. Articles and titles are not it: "The
    # Collector" searched as "The" matched every sentence in last_call, and
    # "Mr. Halloway" searched as "Mr." matched nothing.
    def _searchable(name):
        skip = {"the", "a", "an", "mr", "mrs", "ms", "miss", "dr", "sir", "lady"}
        for tok in _WORD_TOKEN.findall(str(name or "")):
            if tok.lower() in skip or len(tok) < 3:
                continue
            return tok
        return ""

    findings = []
    for n in npcs:
        first = _searchable(n.get("name"))
        if not first:
            continue
        pat = re.compile(rf"\b{re.escape(first)}\b")
        where = [label for label, txt in (("the opening", opening_text),
                                          ("a quest card", card_text),
                                          ("a room description", place_text))
                 if pat.search(txt)]
        if not where:
            continue
        if n["id"] in has_meeting:
            continue
        findings.append(f"[person] {first} is named in {', '.join(where)} "
                        f"and has no meeting anywhere")

    # Places, heaviest first — a thin corridor legitimately needs no introduction and a
    # room carrying a third of the game's prose does not, so the order carries the
    # judgement the count cannot.
    visits = _fh_first_visits(game)
    weight = collections.Counter()
    for c in model:
        weight[c["loc"]] += sum(b.words for b in c["beats"])
    # A location with NO prose is a different defect and gate `location fill` owns it —
    # saying it also lacks an introduction is noise on top of a real finding.
    bare = [l for l in (game.get("locations") or [])
            if l.get("id") and not visits.get(l["id"]) and weight[l["id"]]]
    for l in sorted(bare, key=lambda l: -weight[l["id"]]):
        name = str(l.get("name") or l["id"])
        findings.append(f"[place] {name} has no first visit — {weight[l['id']]:,} words "
                        f"of prose and nothing that says what kind of place it is")

    if not findings:
        return ("every named character is met and every location introduces itself", [])
    people = sum(1 for f in findings if f.startswith("[person]"))
    places = len(findings) - people
    summary = (f"{people} character(s) named before any meeting · "
               f"{places} location(s) with no first visit — read the list, do not read "
               f"the number")
    return summary, findings


# ─────────────────────────────────────────────────────────────────────────────
# The clock — the time the game promises and the time the engine keeps
# Doctrine: references/the-clock.md.  Added 2026-08-22 after a shipped game offered
# "Work the counter till one (2h 30m)." on a canvas open 08:00–13:00, in an engine
# with no absolute-time advance at all.
# ─────────────────────────────────────────────────────────────────────────────
# There is NO way to send the clock to a named hour:
#   grep -E 'target_hour|advance_to|until_time|time_target' v2.py   ->   0 hits
# `advanceTime(minutes)` (v2.py:5400) adds minutes and rolls the day; that is the whole
# time API. So a label naming a clock time is a promise the engine cannot keep, and the
# only pinned reading in a game is `[time] starting_hour` on the first screen.

_CLK_WORDNUM = "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
# degrees-of-lewdity's cost tag — "(0:30)", "(£12 1:00)" — is a DURATION, not a clock.
# Stripping it first is what took a first draft of this instrument from 4,310 field
# "clock labels" down to the real 2.
_CLK_COSTTAG = re.compile(r"\([^)]{0,40}?\d{1,2}:\d{2}[^)]{0,40}?\)")
_CLK_NUMERIC = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b")
_CLK_AMPM = re.compile(r"\b(?:1[0-2]|0?[1-9])\s?[ap]\.?m\.?\b", re.I)
_CLK_OCLOCK = re.compile(r"\bo'?clock\b", re.I)
# `half nine` / `half past nine` is an HOUR and the bare wordnum list cannot see it.
# It is also on the own_words lint's AMBIGUOUS list (7:30 here, 6:30 across much of
# Europe), so the two instruments were looking at the same string and neither counted
# it as a clock.
_CLK_HALF = r"half(?:\s+past)?\s+(?:" + _CLK_WORDNUM + r"|\d{1,2})"
_CLK_PREP = re.compile(
    r"\b(?:at|till|until|by|before|after|past|from|gone)\s+"
    r"(?:" + _CLK_HALF + r"|" + _CLK_WORDNUM + r"|\d{1,2})\b([^\w]*)(\w+)?", re.I)
# An hour needs no preposition when a part of the day follows it — "Seven in the
# morning and the fryers have been off an hour" was invisible to the rule above.
_CLK_PARTOFDAY = re.compile(
    r"\b(?:" + _CLK_HALF + r"|" + _CLK_WORDNUM + r")\s+"
    r"(?:in the (?:morning|afternoon|evening)|at night)\b", re.I)
_CLK_QUARTER = re.compile(
    r"\bquarter\s+(?:past|to)\s+(?:" + _CLK_WORDNUM + r"|\d{1,2})\b", re.I)
# `half nine` needs no preposition and no part of day either — "Half nine and the
# flat is at twenty-four degrees" opens a sentence with a clock and was invisible to
# both rules above. Safe to match anywhere: `half` + an hour is only ever a time
# (`half a dozen` does not match, because a wordnum has to follow immediately).
# Checked against the 25-game corpus: one game moves, on a true positive
# ("gathered at half past six for drinks"), and the field median holds at 1.0.
_CLK_HALF_ANY = re.compile(r"\b" + _CLK_HALF + r"\b", re.I)

# "at one point", "one by one", "after ten minutes" are idiom, not the clock. A loose
# version of this rule was ~90% idiom across the 25-game corpus (312 hits of "at one
# point" alone), so a word-number hour only counts when a clause boundary or a
# time-marker follows it.
_CLK_OK_NEXT = {"o", "oclock", "sharp", "am", "pm", "in", "on", "tonight", "tomorrow",
                "today", "and", "or", "till", "until", "to", "when", "so", "but",
                "before", "after", "then", "she", "he", "they", "you", "i", "we",
                # "the" was in the STOPLIST until 2026-08-22, to kill "at one point".
                # It also killed every "by nine THE whole flat…" — the commonest shape
                # a clock reading takes in our own prose. The unit nouns below already
                # catch the idiom it was standing in for.
                "the", ""}
_CLK_BAD_NEXT = {"point", "of", "another", "one", "hand", "side", "end", "time",
                 "day", "days", "minute", "minutes", "hour", "hours", "week", "weeks",
                 "month", "months", "year", "years", "more", "others", "each", "last",
                 "as", "a", "an", "step", "steps", "stride", "strides",
                 "different", "separate", "distinct",
                 "elections", "women", "men", "large", "overly", "showing", "way"}


def _clk_refs(text):
    """Every clock-time reference in a piece of player-visible text.

    Deduped by SPAN: several patterns legitimately match the same phrase — "at half
    nine in the morning" hits both the preposition rule and the part-of-day rule — and
    counting it twice inflates the rate the lint reports.
    """
    t = _CLK_COSTTAG.sub(" ", str(text or ""))
    spans = []  # [start, end, text]

    def _add(m):
        for i, (a, b, _) in enumerate(spans):
            if m.start() < b and a < m.end():        # overlaps something already held
                if (m.end() - m.start()) > (b - a):  # keep the longer read
                    spans[i] = (m.start(), m.end(), m.group(0))
                return
        spans.append((m.start(), m.end(), m.group(0)))

    for rx in (_CLK_NUMERIC, _CLK_AMPM, _CLK_OCLOCK, _CLK_PARTOFDAY, _CLK_QUARTER,
               _CLK_HALF_ANY):
        for m in rx.finditer(t):
            _add(m)
    for m in _CLK_PREP.finditer(t):
        gap, nxt = (m.group(1) or ""), (m.group(2) or "").lower()
        boundary = any(ch in gap for ch in ".,;:!?)(\"'\n") or not nxt
        if not boundary:
            if nxt in _CLK_BAD_NEXT:
                continue
            if nxt not in _CLK_OK_NEXT and not re.fullmatch(r"\d+", nxt):
                continue
        seg = m.group(0)
        if _CLK_NUMERIC.search(seg) or _CLK_AMPM.search(seg) or _CLK_OCLOCK.search(seg):
            continue
        _add(m)
    return [x[2].strip() for x in sorted(spans)]


_CLK_DUR_HM = re.compile(r"(\d+)\s*(?:h|hr|hrs|hour|hours)\b"
                         r"(?:\s*(\d+)\s*(?:m|min|mins|minutes)\b)?", re.I)
_CLK_DUR_M = re.compile(r"(\d+)\s*(?:m|min|mins|minutes)\b", re.I)
_CLK_DUR_CLOCKFORM = re.compile(r"\b(\d{1,2}):([0-5]\d)\b")


def _clk_stated_minutes(label):
    """The duration a label PROMISES, in minutes, or None.

    Only what is inside brackets counts — that is the field's form ("(0:30)",
    "(£12 1:00)", "(2h 30m)") and it keeps prose like "a five minute walk" out of it.
    """
    for seg in re.findall(r"\(([^)]*)\)", str(label or "")):
        m = _CLK_DUR_CLOCKFORM.search(seg)
        if m:
            return int(m.group(1)) * 60 + int(m.group(2))
        m = _CLK_DUR_HM.search(seg)
        if m:
            return int(m.group(1)) * 60 + (int(m.group(2)) if m.group(2) else 0)
        m = _CLK_DUR_M.search(seg)
        if m:
            return int(m.group(1))
    return None


def _clk_node_index(game):
    """(canvas_id, node_id) -> node, so a choice's target can be resolved."""
    idx = {}
    for c in (game.get("canvases") or []):
        for n in (c.get("nodes") or []):
            idx[(c.get("id"), n.get("id"))] = n
    return idx


def _clk_spent_minutes(idx, canvas_id, choice):
    """Minutes this click actually costs, or None when it cannot be resolved.

    The duration is stated where the player DECIDES and charged where they LEAVE:
    off_season's "Work the counter (2h 30m)." targets `rung_arcade_take_am.base`, whose
    exit carries `time_progression_minutes = 150`. Reading only the choice would score
    every honest tag as unverifiable.
    """
    cfg = choice.get("config") or {}
    v = cfg.get("time_progression_minutes") or choice.get("time_progression_minutes")
    if v:
        return int(v)
    if (choice.get("targetType") or "") != "node":
        return None
    ref = str(choice.get("nodeId") or "")
    if not ref:
        return None
    cid, nid = ref.split(".", 1) if "." in ref else (canvas_id, ref)
    node = idx.get((cid, nid))
    if node is None:
        return None
    ecfg = (node.get("exit_block") or {}).get("config") or {}
    tv = ecfg.get("time_progression_minutes")
    return int(tv) if tv else None


def _clk_choices(model):
    """Every (canvas_record, choice, label) the player can read on a button."""
    for c in model:
        for n in c["nodes"]:
            for ch in ((n.get("exit_block") or {}).get("choices") or []):
                t = str(ch.get("text") or ch.get("label") or "")
                if t:
                    yield c, ch, t


def _clk_windows(canvas_raw):
    """Every schedule window on a canvas as (start, end, width_minutes)."""
    out = []
    for row in (((canvas_raw or {}).get("trigger") or {}).get("schedules") or []):
        s, e = row.get("start_time"), row.get("end_time")
        try:
            sh, sm = str(s).split(":")[:2]
            eh, em = str(e).split(":")[:2]
            a, b = int(sh) * 60 + int(sm), int(eh) * 60 + int(em)
        except Exception:
            continue
        out.append((s, e, ((b - a) % 1440) or 1440))
    return out


def lint_clock_in_prose(model, game):
    """Every hour a BEAT names, with the window it has to survive — a LIST.

    `the-clock.md` C2: a repeatable canvas fires at any minute of its window, and the
    windows in this repo run 149–540 minutes wide (five in the whole repo are an hour or
    less). So a sentence that reads as a clock is wrong for nearly the whole window it
    fires in — unless it is a RULE ("Nobody comes in before eleven in February"), which
    is true at every minute and is correct work.

    ⚠️ A LIST AND NEVER A GATE. Telling a rule from a reading is a reading, not a
    measurement, and a shift-driven world names hours as rules on purpose. A rate gate
    would fail seventh_day's kitchen board and steam's shift board for obeying the
    doctrine — SKILL.md's "a check that fails a game for obeying the doctrine is a bug
    in the check". The check hands over the lines and their windows; the author calls it.

    Field basis: median 0.8 clock references per 10,000 words across the 27 parseable
    sandboxes (14.7M words), p75 1.8.

    ⚠️ RE-BASELINED 2026-08-24 BY THE END-OF-STUDY RECHECK, from 1.1 / 2.1 on 25 games.
    `college-daze` and `free-cities` ship the Twine 1 <div id="store-area"> container and
    parsed to ZERO passages until section B taught the parser to read it. Both are
    clock-quiet — 0.25 and 0.27 references per 10k — so the median falls. This is the ONE
    field constant the recheck moved, and it moves AGAINST our games, not for them:
    off_season at 26.4 was 24x the field median and is now 33x. The old figure reproduced
    EXACTLY on the old 25 using this same `_clk_refs`, so the movement is the corpus and
    not the instrument (`findings_RECHECK.md` §2).

    Re-measured 2026-08-22 on the corrected `_clk_refs` (half-hours, part-of-day phrases,
    quarter-past, and `<hour> the`). The figure moved 1.0 -> 1.1 and p75 held at 2.1: ONE
    field game gained ONE reference, a true positive. The same correction moves our own
    games 25-50% -- off_season 20.1 -> 26.4 before repair, steam 29.2 -> 36.6, forty_miles
    22.6 -> 34.4. The blind spots were hiding our defects and almost none of the field's,
    because the constructions they missed are ones our authors reach for and the corpus
    does not.
    """
    FIELD_MEDIAN, FIELD_P75 = 0.8, 1.8
    words = 0
    rows = []
    for c in model:
        wins = _clk_windows(c.get("raw"))
        # A canvas with no schedule fires at ANY hour, so the claim has to survive the
        # whole day — 1440 is the honest width, and it sorts those to the top.
        widest = max((w for _s, _e, w in wins), default=1440)
        win_txt = (f"window {wins[0][0]}–{wins[0][1]}, {widest} min"
                   if wins else "no window — fires at any hour")
        for n in c["nodes"]:
            for b in _fh_blocks(n.get("blocks")):
                t = b.get("content")
                if not isinstance(t, str) or not t:
                    continue
                words += len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))
                for ref in _clk_refs(t):
                    i = t.find(ref)
                    frag = re.sub(r"\s+", " ", t[max(0, i - 46):i + 46]).strip()
                    rows.append((widest, f'{c["id"]}: "…{frag}…"  ({win_txt})'))
    if not words:
        return ("no beat prose to read", [])
    rate = len(rows) * 10000.0 / words
    band = ("inside the field's band" if rate <= FIELD_P75
            else f"{rate / FIELD_MEDIAN:.0f}x the field median")
    if not rows:
        return (f"no beat names a clock time ({words:,} words)", [])
    # Widest window first: the wider the window a line has to survive, the less
    # defensible the claim, and "no window" is the whole day.
    findings = [r for _w, r in sorted(rows, key=lambda x: (-x[0], x[1]))][:40]
    summary = (f"{rate:.1f} clock references per 10k words — {band} "
               f"(field median {FIELD_MEDIAN}, p75 {FIELD_P75}) · read the lines, not "
               f"the number: a rule is correct, a reading is not")
    return summary, findings


def lint_time_cost_on_button(model, game):
    """Clicks that move the clock a long way without saying so — a LIST.

    `the-clock.md` C4. The engine already tags TRAVEL time on a navigation card
    (`getLocationCostTag`, v2.py:4724, renders "20m") and tags ACTIVITY time nowhere —
    a choice's `time_progression_minutes` emits a bare advanceTime() at the bottom of
    the passage body (v2.py:12733). So the sidebar clock jumps and the player is not
    told why.

    ⚠️ A LIST AND NEVER A GATE. Duration-tagging is ONE game's convention, not a field
    norm: 4,219 of the corpus's 4,260 duration tags are degrees-of-lewdity's, and among
    the five field games with a minute-resolution clock only that one does it. Gating it
    would be the invented threshold G21 already refuses for stamina-type costs.
    """
    BIG = 60
    idx = _clk_node_index(game)
    big, silent = 0, []
    for c, ch, t in _clk_choices(model):
        spent = _clk_spent_minutes(idx, c["id"], ch)
        if not spent or spent < BIG:
            continue
        big += 1
        if _clk_stated_minutes(t) is None:
            silent.append(f'{c["id"]}: "{t[:52]}" spends {_hms(spent)}, '
                          f"label does not say so")
    if not big:
        return ("no click moves the clock an hour or more", [])
    if not silent:
        return (f"all {big} long clicks state their duration", [])
    return (f"{len(silent)} of {big} clicks that move the clock an hour or more say "
            f"nothing about it on the button", sorted(silent)[:40])


# ── The currency on the screen — the-economy.md R7 ───────────────────────────
# A shipped game wrote one click's price six ways and THREE of them were the
# engine's, not the author's (engine.md §33). The measurable part is the
# notation: a symbol, a currency code and a spelled-out unit all name a
# currency, and a game that uses two of them has two currencies on screen.
#
# A symbol and its own word are the SAME currency — "$" and "dollars" differ in
# form, not in unit — so the gate maps both onto one unit and never fails a game
# for saying "two dollars" beside "$2". Form is the lint's business.
_CUR_UNIT = {
    "$": "dollar", "£": "pound", "€": "euro", "¥": "yen",
    "usd": "dollar", "gbp": "pound", "eur": "euro", "jpy": "yen",
    "dollar": "dollar", "dollars": "dollar", "buck": "dollar", "bucks": "dollar",
    "pound": "pound", "pounds": "pound", "quid": "pound",
    "euro": "euro", "euros": "euro", "yen": "yen",
    # SUB-UNITS, added 2026-08-22. Without them a game that declared a neutral "$"
    # and then wrote "she is out by sixty pence" read as "no beat names a currency"
    # -- a false green that let a real regression sit for two batches. A sub-unit
    # names its parent currency exactly as the major unit does.
    "pence": "pound", "penny": "pound", "pennies": "pound",
    "cent": "dollar", "cents": "dollar",
    "centime": "euro", "centimes": "euro", "sen": "yen",
}
# ⚠️ "forty per cent" is not money. Measured before the sub-units went in: without
# this guard `steam`'s "the trade is down forty per cent" false-positives twice.
_CUR_PERCENT = re.compile(r"\bper\s*cents?\b", re.I)
_CUR_SYM = re.compile(r"([$£€¥])\s?\d")
_CUR_CODE = re.compile(r"\b(USD|GBP|EUR|JPY)\b", re.I)
_CUR_NUM = (r"\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
            r"fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand")
_CUR_WORD = re.compile(rf"\b(?:{_CUR_NUM})\s+([A-Za-z]+)\b", re.I)


def _cur_extra(currency, declared):
    """Words that name THIS game's currency but no other game's.

    An invented unit is legitimate and the field ships it — `apocalyptic-world`
    prices in caps, `vesper` in coin — but a fixed word list would guess. So the
    only invented words recognised are the ones the game itself declares: its
    currency trait name, and its declared symbol when that symbol is a word.
    """
    # `money`, `cash`, `funds` name the TRAIT, not a unit — nobody writes "50 money"
    # as a price, and a dev shortcut labelled "+50 money" is not one either.
    GENERIC = {"money", "cash", "funds", "fund", "wallet", "balance", "currency"}
    out = {}
    for src in (currency, declared):
        w = str(src or "").strip().lower()
        if w and w.isalpha() and w not in _CUR_UNIT and w not in GENERIC:
            out[w] = w
            out[w + "s"] = w
            out[w.rstrip("s")] = w
    return out


def _cur_units(text, extra):
    """Every currency named in one string as (unit, the form written, channel)."""
    out = []
    for m in _CUR_SYM.finditer(text):
        out.append((_CUR_UNIT[m.group(1)], m.group(1), "symbol"))
    for m in _CUR_CODE.finditer(text):
        out.append((_CUR_UNIT[m.group(1).lower()], m.group(1).upper(), "code"))
    for m in _CUR_WORD.finditer(text):
        w = m.group(1).lower()
        # "forty per cent" is a proportion, not a price.
        if w in ("cent", "cents") and _CUR_PERCENT.search(text[max(0, m.start() - 12):m.end()]):
            continue
        unit = _CUR_UNIT.get(w) or extra.get(w)
        if unit:
            out.append((unit, w, "word"))
    return out


def _cur_labels(model):
    """Every string the player reads on a button: canvas names + choice text.

    A canvas `name` is the room-list button (the-voice.md R1), so it is judged
    with the choices and not with the prose.
    """
    for c in model:
        raw = c.get("raw") or {}
        if _is_dev(raw):
            continue                                  # no player can reach a dev shortcut
        nm = str(raw.get("name") or "")
        if nm:
            yield c["id"], "name", nm
        for n in c["nodes"]:
            for ch in ((n.get("exit_block") or {}).get("choices") or []):
                t = str(ch.get("text") or ch.get("label") or "")
                if t:
                    yield c["id"], "choice", t


def _cur_setup(model, game, state):
    """(currency trait, declared symbol, engine symbol, extra-word map).

    Inference is by USAGE, matching gate 16 — a game can carry two currencies
    (`vesper` runs `money` alongside `coin`) and taking the first name match
    picks the wrong one, which would then not be recognised as a unit at all.
    """
    econ = (((state or {}).get("board") or {}).get("economy") or {})
    currency = econ.get("currency")
    if not currency:
        cands = [k for k in ((game.get("player") or {}).get("core_traits") or {})
                 if CURRENCY_HINT.search(k)]

        def _usage(trait):
            ops = []
            for c in model:
                _currency_ops(c, trait, ops)
            return len(ops) + sum(1 for c in model if trait in c["reads"])

        currency = max(cands, key=_usage) if cands else None
    declared = str(econ.get("symbol") or "").strip()
    rent = (game.get("settings") or {}).get("rent") or {}
    # v2.py:1190 — absent or empty, it is "$", and the rent pages print it.
    engine = (str(rent.get("currency_symbol") or "").strip() or "$") if rent.get("enabled") else ""
    return currency, declared, engine, _cur_extra(currency, declared)


_CUR_NUMTOK = frozenset(
    "one two three four five six seven eight nine ten eleven twelve fifteen twenty "
    "thirty forty fifty sixty seventy eighty ninety hundred thousand".split())


def _cur_exact_share(texts, extra):
    """Of every money-unit WORD, how many carry an exact amount beside them.

    Computed the same way the field figure was, so the two are comparable: a unit
    word counts as EXACT when a digit or a number word sits within two tokens
    before it. Field: 20%. Ours across ten games: 51%.
    """
    units = ({k for k in _CUR_UNIT if k.isalpha() and len(k) > 3}
             - {"usd", "gbp", "eur", "jpy"}) | set(extra)
    exact = total = 0
    for txt in texts:
        toks = re.findall(r"[A-Za-z0-9,]+", txt.lower())
        for i, w in enumerate(toks):
            if w not in units:
                continue
            total += 1
            if any(x[:1].isdigit() or x in _CUR_NUMTOK for x in toks[max(0, i - 2):i]):
                exact += 1
    return exact, total


def lint_currency_in_prose(model, game, state):
    """Where the prose names a currency other than the game's main one — a LIST.

    `the-economy.md` R7. Two field numbers, both from the 25-game corpus
    (11.0M words of passage prose):

      · a game's dominant notation carries a median 92% of its money references
        (minimum 56%); ours run at a median 82%
      · a money WORD carries an exact amount 20% of the time in the field and
        51% of the time in ours — we spell prices out, and a spelled-out price
        is the copy that goes stale when the number moves
        (v1 `author-game/references/prose-truth.md` §2)

    ⚠️ A LIST AND NEVER A GATE. `zaras-school-life` writes every price in words
    across 905k words and never varies; `apocalyptic-world` prices in caps. A
    rate gate would fail both for obeying the rule.
    """
    FIELD_DOM, FIELD_EXACT = 0.92, 0.20
    _cur, dec, eng, extra = _cur_setup(model, game, state)
    tally, rows, texts = collections.Counter(), [], []
    for c in model:
        for n in c["nodes"]:
            for b in _fh_blocks(n.get("blocks")):
                t = b.get("content")
                if not isinstance(t, str) or not t:
                    continue
                texts.append(t)
                for unit, form, _chan in _cur_units(t, extra):
                    tally[unit] += 1
                    i = t.lower().find(form.lower())
                    frag = re.sub(r"\s+", " ", t[max(0, i - 40):i + 44]).strip()
                    rows.append((unit, f'{c["id"]}: "…{frag}…"'))
    exact, words = _cur_exact_share(texts, extra)
    if not tally:
        return ("no beat names a currency", [])
    total = sum(tally.values())
    dom, dn = tally.most_common(1)[0]
    summary = (f"{total} money references · {dn/total*100:.0f}% in `{dom}` "
               f"(field median {FIELD_DOM*100:.0f}%)")
    if words:
        summary += (f" · {exact/words*100:.0f}% of the {words} money words carry an exact "
                    f"amount (field {FIELD_EXACT*100:.0f}%)")
    if len(tally) > 1:
        summary += " · " + ", ".join(f"`{u}` x{n}" for u, n in tally.most_common())
    # The engine prints its own symbol on the rent pages whether or not anyone declared
    # one, so prose that runs on a different unit contradicts a screen the author never
    # wrote. The gate cannot see this — it does not read prose — so it is said here.
    for label, sym in (("[settings.rent] currency_symbol", eng),
                       ("board.economy.symbol", dec)):
        if sym and _CUR_UNIT.get(sym.lower(), sym.lower()) != dom:
            summary += (f" · ⚠ the prose runs on `{dom}` and {label} is "
                        f'"{sym}" — engine.md §33')
    # The minority notations are the actionable list — the dominant one is the game.
    return summary, sorted({r for u, r in rows if u != dom})[:40]


def lint_price_spelled_out(model, game, state):
    """Priced buttons that do not use a symbol — a LIST.

    `the-economy.md` R7 part 3. Measured across 654 priced link labels in the
    25-game corpus: 94.0% use a SYMBOL, 5.2% spell the unit out, 0.8% use a
    currency code (five labels, all one game).

    ⚠️ A LIST AND NEVER A GATE. `vesper` prices ten labels `10 coin` and never
    varies, which is the same shape as the field's `Add 1000 caps`. Consistency
    is the gate's business; form is a house preference with a field behind it.
    """
    FIELD = (0.940, 0.052, 0.008)
    _cur, _dec, _eng, extra = _cur_setup(model, game, state)
    kinds, rows = collections.Counter(), []
    for cid, kind, text in _cur_labels(model):
        found = _cur_units(text, extra)
        if not found:
            continue
        chan = ("symbol" if any(f[2] == "symbol" for f in found)
                else "code" if any(f[2] == "code" for f in found) else "word")
        kinds[chan] += 1
        if chan != "symbol":
            rows.append(f'{cid} ({kind}): "{text[:58]}" — {chan}')
    n = sum(kinds.values())
    if not n:
        return ("no button states a price", [])
    summary = (f"{n} priced labels · symbol {kinds['symbol']/n*100:.0f}% · "
               f"spelled out {kinds['word']/n*100:.0f}% · code {kinds['code']/n*100:.0f}% "
               f"(field {FIELD[0]*100:.0f}% / {FIELD[1]*100:.0f}% / {FIELD[2]*100:.0f}%)")
    return summary, sorted(rows)[:40]


def run_gates(model, game, state=None):
    R = []

    def gate(name, ok, headline, detail=None):
        # ok is True / False / None. None means THERE WAS NOTHING TO JUDGE — reported
        # as n/a and excluded from the tally. A gate that "passes" on an empty game
        # flatters it: an absence is not a pass.
        R.append(dict(gate=name, pass_=(ok is True), na=(ok is None),
                      headline=headline, detail=detail or []))

    all_beats = [b for c in model for b in c["beats"]]
    expl = [b for b in all_beats if b.explicit >= 3]

    # Which routes reach each canvas, and which of them carry a brake. Needed by the
    # economy gates (18) and by G26; built once because it walks every choice in the game.
    routes = _routes(model, game)

    # G1 — location fill, judged as a distribution (see the constants block)
    wl = collections.Counter()
    for c in model:
        wl[c["loc"]] += sum(b.words for b in c["beats"])
    declared = {l["id"] for l in (game.get("locations") or [])}
    per_loc = sorted(wl.get(l, 0) for l in declared)          # includes empties as 0
    total = sum(per_loc)
    n = len(per_loc) or 1
    mean = total / n
    median = per_loc[n // 2] if n else 0
    anchor = max(per_loc) if per_loc else 0
    anchor_pct = 100 * anchor / total if total else 0
    anchor_id = max(declared, key=lambda l: wl.get(l, 0)) if declared else "—"
    empty = sorted(l for l in declared if not wl.get(l))

    # DECLARE-THEN-CHECK (2026-08-15, study 6). If the ledger declares a per-location
    # budget, each location is judged against ITS OWN number and the global constants are
    # not consulted. `fill` is canonical; `budget` is accepted because one shipped game
    # wrote that key. A 300-word corridor is not a defect if you declared a corridor —
    # which is what the-board.md has always said in prose and could not enforce.
    budgets = {}
    for l in ((state or {}).get("board") or {}).get("locations") or []:
        b = l.get("fill", l.get("budget"))
        if isinstance(b, (int, float)) and b > 0:
            budgets[l.get("id")] = float(b)

    fails = []
    if empty:
        fails.append(f"{len(empty)} declared locations with nothing placed: {', '.join(empty[:12])}")

    # ⚠️ A BUDGET THAT CANNOT BE WRONG IS NOT A BUDGET. Measured on all three v2 games:
    # every declared figure was an exact post-hoc word count — 9,607 / 4,936 / 10,295, not
    # one of twenty-four round to the nearest hundred — so delivered-vs-declared matched
    # 8/8 in all three and proved nothing. A plan is written in round numbers before the
    # prose; a record is written in arbitrary ones after it. If the declaration is a
    # record, say so and judge on the backstop instead of crediting a tautology.
    # ⚠️ 50, not 100. At 100 a legitimate 250-granularity plan (9,750 · 5,250 · 4,250 …) was
    # flagged as post-hoc — a false positive on exactly the careful author this is meant to
    # reward. 50 accepts every plan granularity anyone would actually use and still rejects
    # the measured real case, which scores 0 of 8 either way.
    planned = sum(1 for v in budgets.values() if v % 50 == 0)
    post_hoc = bool(budgets) and planned * 2 < len(budgets)

    if budgets and post_hoc:
        drift = [f"{lid}: declared {budgets[lid]:,.0f}, delivered {wl.get(lid, 0):,}"
                 for lid in sorted(budgets) if abs(wl.get(lid, 0) - budgets[lid]) > 1]
        fails.append(f"board.locations[].fill is a RECORD, not a plan — only {planned} of "
                     f"{len(budgets)} figures are round to 100, so the budget was written "
                     f"from the delivered word count and cannot fail")
        fails.append("declare the budget in round numbers at BOARD phase, before the prose; "
                     "the-board.md §1 — budget against the FINISHED total, not the current one")
        fails += drift[:4]
        if anchor_pct < ANCHOR_SHARE_PCT:
            fails.append(f"no anchor: {anchor_id} holds {anchor_pct:.1f}% of location prose "
                         f"(need {ANCHOR_SHARE_PCT:.0f}%) — the world has no centre")
        if median < MEDIAN_LOCATION_WORDS:
            fails.append(f"median location {median:,} words (need {MEDIAN_LOCATION_WORDS:,})")
        if mean < MEAN_LOCATION_WORDS:
            fails.append(f"mean location {mean:,.0f} words (need {MEAN_LOCATION_WORDS:,})")
        head = (f"{n} locations · {total:,} words · mean {mean:,.0f} · median {median:,} · "
                f"anchor {anchor_id} {anchor_pct:.0f}% · [declared budget is post-hoc — "
                f"judged on the backstop]")
    elif budgets:
        off = []
        for lid in sorted(declared):
            want_w = budgets.get(lid)
            if not want_w:
                off.append(f"{lid}: no fill declared in board.locations — nothing to check against")
                continue
            got = wl.get(lid, 0)
            drift = (got - want_w) / want_w
            if abs(drift) > DECLARED_FILL_TOLERANCE:
                off.append(f"{lid}: declared {want_w:,.0f} words, delivered {got:,} "
                           f"({drift:+.0%})")
        fails += off
        plan_total = sum(budgets.values())
        plan_anchor = max(budgets.values()) if budgets else 0
        plan_anchor_pct = 100 * plan_anchor / plan_total if plan_total else 0
        if plan_anchor_pct < ANCHOR_SHARE_PCT:
            fails.append(f"the PLAN has no centre: its deepest location is only "
                         f"{plan_anchor_pct:.0f}% of the declared total "
                         f"(need {ANCHOR_SHARE_PCT:.0f}%)")
        elif anchor_pct < ANCHOR_SHARE_PCT:
            fails.append(f"no anchor as built: {anchor_id} holds {anchor_pct:.1f}% of location "
                         f"prose (plan said {plan_anchor_pct:.0f}%) — the world has no centre")
        head = (f"{n} locations · {total:,} words vs {plan_total:,.0f} declared · "
                f"{len(declared) - len(off)}/{n} on their own budget · "
                f"anchor {anchor_id} {anchor_pct:.0f}%")
    else:
        # BACKSTOP ONLY — no ledger. See the constants block for why these are not the check.
        if anchor_pct < ANCHOR_SHARE_PCT:
            fails.append(f"no anchor: deepest location {anchor_id} holds {anchor_pct:.1f}% "
                         f"of location prose (need {ANCHOR_SHARE_PCT:.0f}%) — no centre")
        if median < MEDIAN_LOCATION_WORDS:
            fails.append(f"median location {median:,} words (need {MEDIAN_LOCATION_WORDS:,})")
        if mean < MEAN_LOCATION_WORDS:
            fails.append(f"mean location {mean:,.0f} words (need {MEAN_LOCATION_WORDS:,})")
        head = (f"{n} locations · {total:,} words · mean {mean:,.0f} · median {median:,} · "
                f"anchor {anchor_id} {anchor_pct:.0f}% · [backstop — no declared budgets]")

    gate("location fill", not fails, head, fails)

    # G2 — explicit floor.
    # ⚠️ A BARE PASS HERE MEANS ALMOST NOTHING, and the headline has to say so.
    # This floor is derived from the reference game's own 7.5-9.3% band — and that
    # game is the COLDEST of 18 shipped sandboxes measured on this same word list
    # (field median 33.3%). A game landing on 7.6% is inside the reference's historical
    # range and still four times colder than its genre. One did exactly that and the
    # gate said PASS. Until a field-comparable threshold exists (see the constant),
    # the honest thing is to print how marginal a marginal pass is.
    pct = 100 * len(expl) / max(len(all_beats), 1)
    marginal = EXPLICIT_BEAT_FLOOR <= pct < 12.0
    gate("explicit floor", None if not all_beats else pct >= EXPLICIT_BEAT_FLOOR,
         f"{pct:.1f}% of {len(all_beats):,} beats carry 3+ explicit words "
         f"(floor {EXPLICIT_BEAT_FLOOR}%)" + ("  ← BARE PASS" if marginal else ""),
         [f"{len(expl)} explicit beats in the whole game — the floor is the reference game's own "
          f"band, and that game is the coldest of 18 measured sandboxes",
          "clearing this floor is not evidence of heat; it is evidence of not being empty"]
         if marginal else [])

    # G3 — explicit content lives where the player returns
    rep_expl = sum(1 for c in model for b in c["beats"] if b.explicit >= 3 and c["rep"])
    share = 100 * rep_expl / max(len(expl), 1)
    worst = collections.Counter()
    for c in model:
        if not c["rep"]:
            worst[c["loc"]] += sum(1 for b in c["beats"] if b.explicit >= 3)
    gate("explicit in repeatable", None if not expl else share >= EXPLICIT_IN_REPEATABLE,
         f"{share:.1f}% of {len(expl)} explicit beats are re-enterable (floor {EXPLICIT_IN_REPEATABLE}%)",
         [f"once-only explicit at {l}: {n}" for l, n in worst.most_common(6) if n])

    # G4 — repeatable explicit media must cycle, never a fixed clip
    fixed, pooled = [], 0
    for c in model:
        if not c["rep"]:
            continue
        for b in c["beats"]:
            for m in b.media:
                path = m.get("file") or m.get("pool_dir") or ""
                if not EXPLICIT_MEDIA.search(str(path)):
                    continue
                if m.get("pool_dir") or m.get("files"):
                    pooled += 1
                else:
                    fixed.append(f"{c['id']}: {path}")
    gate("repeatable explicit media cycles", None if (pooled + len(fixed)) == 0 else not fixed,
         f"{pooled} pooled, {len(fixed)} fixed single-clip in repeatable content",
         fixed[:25])

    # ═════════════════════════════════════════════════════════════════════════
    # G31 — an explicit beat carries a clip. `register.md`.
    #
    # G4 above asks whether the clips CYCLE. This asks the prior question: is there
    # a clip on the screen the player is actually reading. A cascade appends
    # (v2.py:13952) — beat 2 renders BELOW beat 1 and beat 1's clip stays where it
    # was — so a canvas that hangs one video off its node lead has illustrated its
    # opening and nothing else. LO found this by playing: "it shows its media on
    # top and its content on the bottom … the third link is suck him, at that time
    # it doesn't show that media."
    #
    # Field, same unit: 58% of in-passage reveals carry their own clip (n=3,005),
    # and 91% of screens carrying explicit prose carry media at all.
    # ═════════════════════════════════════════════════════════════════════════
    expl_beats = [b for c in model for b in c["beats"] if b.explicit >= 3]
    clipped = [b for b in expl_beats if b.media]
    clip_pct = 100 * len(clipped) / max(len(expl_beats), 1)
    dry = collections.Counter()
    for b in expl_beats:
        if not b.media:
            dry[b.canvas] += 1
    gate("an explicit beat carries a clip",
         None if not expl_beats else clip_pct >= EXPLICIT_BEAT_MEDIA_FLOOR,
         (f"{len(clipped)}/{len(expl_beats)} explicit beats carry a clip of their own "
          f"({clip_pct:.0f}%, floor {EXPLICIT_BEAT_MEDIA_FLOOR:.0f}%) · field 91% of explicit "
          f"screens, 58% of in-passage reveals"
          if expl_beats else "no explicit beats authored — nothing to illustrate"),
         [f"{cid}: {n} explicit beat{'s' if n > 1 else ''} with no clip"
          for cid, n in dry.most_common(8)]
         + ([f"… and {len(dry)-8} more canvases"] if len(dry) > 8 else [])
         + (["a cascade APPENDS (nested <<linkreplace>>, v2.py:13952) — the clip on the node "
             "lead is the clip for beat 0 only; by the beat that is the act it has scrolled off",
             "the field puts one clip every ~58 words of explicit prose (IQR 25-104); ours run "
             "one every 178-435",
             "for a REPEATABLE act surface the fix is usually not more clips in the cascade but "
             "the other machine — node routing swaps the passage (v2.py:13258), so each act is "
             "its own screen with its own pool (the-surfaces.md)"]
            if expl_beats and clip_pct < EXPLICIT_BEAT_MEDIA_FLOOR else []))

    # ═════════════════════════════════════════════════════════════════════════
    # G32 — somebody speaks. `register.md`.
    #
    # Restores v1's Rule 4, which v2 dropped on a broken measurement — the whole
    # story is in the NARRATION_DIALOGUE_CEILING comment. The direction was right;
    # only the number (0.73:1, measured on one game) was too extreme.
    #
    # `thought_bubble` counts as narration on purpose. Every v2 game inverted the
    # two: seventh_day thinks 4.6 words for every word spoken aloud, forty_miles
    # 3.1 — and the bubble was for the NPC's interior in the first place.
    # ═════════════════════════════════════════════════════════════════════════
    narr_w, spoken_w = _speech_split(game)
    ratio = (narr_w / spoken_w) if spoken_w else float("inf")
    mute = sorted(
        ((sum(b.words for b in c["beats"]), c["id"]) for c in model
         if not any(bl.get("type") == "dialog"
                    for n in (c.get("nodes") or []) for bl in _flat_blocks(n.get("blocks")))
         and sum(b.words for b in c["beats"]) >= 60),
        reverse=True)
    gate("somebody speaks",
         None if not (narr_w + spoken_w) else ratio <= NARRATION_DIALOGUE_CEILING,
         (f"{ratio:.1f}:1 narration to dialogue — {spoken_w:,} spoken of {narr_w + spoken_w:,} "
          f"words (ceiling {NARRATION_DIALOGUE_CEILING:.0f}:1) · field median 2.93:1, 10 of 27 "
          f"games at or under 2:1"
          if spoken_w else
          f"NOBODY SPEAKS — {narr_w:,} words of prose and not one dialog block"),
         [f"{cid}: {w:,} words, no dialog block anywhere" for w, cid in mute[:8]]
         + ([f"… and {len(mute)-8} more silent canvases"] if len(mute) > 8 else [])
         + (["the talk screen is the genre's second largest content kind — 15,774 of 54,630 "
             "field screens, 55 words, two-thirds spoken, one picture",
             "prefer a line of speech to a sentence describing a line of speech; if a person is "
             "in the room, they talk (register.md)"]
            if ratio > NARRATION_DIALOGUE_CEILING else []))

    # G5 — traversal heat: the rooms players cross constantly must not be erotically blank
    hot_locs = set()
    for c in model:
        if not c["rep"]:
            continue
        for b in c["beats"]:
            for m in b.media:
                if (m.get("pool_dir") or m.get("files")) and EXPLICIT_MEDIA.search(str(m.get("pool_dir") or "")):
                    hot_locs.add(c["loc"])
    cold = sorted(declared - hot_locs)
    heat_pct = 100 * len(hot_locs) / max(len(declared), 1)
    gate("traversal heat", heat_pct >= LOCATIONS_WITH_HEAT,
         f"{len(hot_locs)}/{len(declared)} locations ({heat_pct:.0f}%) carry a cycling explicit pool "
         f"(floor {LOCATIONS_WITH_HEAT:.0f}%)",
         [", ".join(cold[:30])] if cold else [])

    # G6 — every character findable somewhere, at some hour
    npcs = game.get("npcs") or []
    bound = collections.Counter()
    for c in model:
        for key in (c.get("npc"), c.get("requires_npc")):
            if isinstance(key, str):
                bound[key] += 1
    missing = []
    for n in npcs:
        nid = n.get("id")
        sched = len(n.get("schedules") or [])
        if not bound.get(nid) or not sched:
            missing.append(f"{nid}: {bound.get(nid,0)} bound canvases, {sched} schedule rows")
    gate("standing surface", not missing,
         f"{len(npcs)-len(missing)}/{len(npcs)} characters are findable and scheduled", missing)

    # G7 — every milestone must open something standing, directly OR down a chain.
    # Transitive on purpose: an opening funnel legitimately runs one-shot -> one-shot,
    # and only the END of that chain has to land on standing content. Flagging every
    # link would punish a shape the genre uses everywhere.
    # Random ambients are excluded — a one-shot random scene is texture, not a milestone,
    # and is not supposed to open anything.
    reads_of = {c["id"]: c["reads"] for c in model}
    opens = {c["id"] for c in model if c["rep"]}          # standing content: the goal state
    changed = True
    while changed:                                        # closure: X opens if it feeds anything that opens
        changed = False
        for c in model:
            if c["id"] in opens or not c["sets"]:
                continue
            if any(c["sets"] & reads_of[o["id"]] for o in model if o["id"] in opens):
                opens.add(c["id"])
                changed = True

    milestones = [c for c in model
                  if not c["rep"] and c["beats"] and not c.get("random")]
    dead = []
    for c in milestones:
        if c["id"] in opens:
            continue
        # A canvas whose only writes are flags it reads back itself is a once-guard
        # ("fire this scene one time"), not a milestone. It promises nothing, so it
        # owes nothing.
        if c["sets"] and c["sets"] <= c["reads"]:
            continue
        if c["sets"]:
            dead.append(f"{c['id']} sets {sorted(c['sets'])[:3]} — chain never reaches standing content")
        else:
            dead.append(f"{c['id']} sets no flag — opens nothing")
    gate("milestones open something", None if not milestones else not dead,
         f"{len(milestones)-len(dead)} of {len(milestones)} milestones open standing content",
         dead[:25])

    # G8 — no meter may rise past the content it can buy.
    # A meter's PROMISED ceiling is the top band the player can see on the sidebar
    # (sidebar_items[].bands[]). A top band with no `max` is unbounded by design
    # and promises nothing, so it is skipped rather than guessed at.
    tops = collections.defaultdict(int)
    for c in model:
        for k, op, v in c["traits"]:
            if isinstance(v, (int, float)) and op in ("gte", "gt", "eq"):
                tops[k] = max(tops[k], int(v))
    over = []
    for item in (game.get("sidebar_items") or []):
        key = item.get("trait")
        bands = item.get("bands") or []
        if not key or not bands or key not in tops:
            continue
        # EVERY BAND BOUNDARY IS A PROMISE. A meter showing bands at 15/35/55/75 tells the
        # player there is something different at each of those. So the threshold that must be
        # bought is the TOP band's `min` — not the highest `max`, which is missing entirely
        # once the top band is (correctly) left unbounded.
        top_min = max((b["min"] for b in bands if isinstance(b.get("min"), (int, float))), default=None)
        if top_min is None or top_min == 0:
            continue
        if tops[key] < top_min:
            empty = [b["min"] for b in bands
                     if isinstance(b.get("min"), (int, float)) and b["min"] > tops[key]]
            over.append(f"{key}: bands promise something at {'/'.join(str(int(e)) for e in empty)}, "
                        f"but the highest authored gate is {tops[key]}")
    gate("meter ceiling", None if not tops else not over,
         f"{len(over)} visible meters rise past their content" if tops
         else "no authored trait gates yet — nothing to promise", over)

    # G9 — a release must end on a visible locked door
    #
    # ⚠️ `locked > 0` is an EXISTENCE check and it stays one — inventing a ratio ceiling
    # here is the mistake that demoted the-surfaces R5. What it must not do is report a
    # bare count: a game showing 18 locked doors passed this while running 78% of its
    # choices open on turn one, and the headline gave no way to see that. The verdict is
    # unchanged; the denominator now prints beside it.
    all_choices = [ch for c in model for n in c["nodes"]
                   for ch in ((n.get("exit_block") or {}).get("choices") or [])]
    locked = sum(1 for ch in all_choices if ch.get("show_when_locked"))
    gated = sum(1 for ch in all_choices if (ch.get("conditions") or {}).get("items"))
    n_ch = len(all_choices) or 1
    gate("ends on an opening", locked > 0,
         f"{locked} choices render visible-but-locked · "
         f"{gated}/{len(all_choices)} choices carry any gate at all "
         f"({100 * (len(all_choices) - gated) // n_ch}% open on turn one)")

    # G10 — the ASCENT meter must expand the world, never contract it.
    # Judged on the single most-gated meter only. A female-protagonist game runs one
    # global axis whose rise buys access ("as her corruption rises, the gameplay
    # expands"); skills and resources legitimately gate downward and are not the spine.
    expand, contract = collections.Counter(), collections.Counter()
    for c in model:
        for k, op, _v in c["traits"]:
            if op in ("gte", "gt"):
                expand[k] += 1
            elif op in ("lt", "lte"):
                contract[k] += 1
    ranked = sorted(set(expand) | set(contract), key=lambda k: -(expand[k] + contract[k]))[:6]
    # Judge what the author DECLARED as ascent, not what a heuristic guesses. Skills and
    # resources legitimately gate downward and are not the spine; only a declaration can
    # tell them apart. Falls back to the top-N heuristic when no ledger exists, and says so.
    declared = (state.get("board") or {}).get("ascent_tiers") if state else None
    tiers = list(declared) if declared else ranked[:ASCENT_TIERS]
    source = "declared" if declared else f"top-{ASCENT_TIERS} guess — no v2_state.json"
    bad = [k for k in tiers if expand[k] <= contract[k]]

    # ⚠️ DECLARING MUST NOT NARROW THE CHECK. Judging only what the board names means a
    # descent-shaped meter — the exact failure this gate exists to catch — disappears by not
    # being volunteered. Measured across the whole gate set: every gate that ITERATES a
    # declaration can be weakened by declaring less, and every gate that iterates the GAME and
    # looks a declaration up cannot. So the direction test now runs over every PLAYER trait in
    # the game, declared or not. It needs no threshold — "closes more than it opens" is a
    # direction, not a magnitude — and NPC-subject traits are excluded because a per-character
    # relation legitimately gates one way.
    p_expand, p_contract = collections.Counter(), collections.Counter()

    def _walk_player_traits(o):
        if isinstance(o, dict):
            if o.get("type") == "trait" and o.get("trait_key") and o.get("subject") == "player":
                op = o.get("operator")
                if op in ("gte", "gt"):
                    p_expand[o["trait_key"]] += 1
                elif op in ("lt", "lte"):
                    p_contract[o["trait_key"]] += 1
            for v in o.values():
                _walk_player_traits(v)
        elif isinstance(o, list):
            for v in o:
                _walk_player_traits(v)

    _walk_player_traits(game)
    # ⚠️ HIDDEN TRAITS ARE NOT METERS. the-economy.md R5 requires income loops to be
    # capped; on a TRIGGERLESS rung the author-side cap is a counter read with `lt`
    # (engine.md §28) — at which point this test called that counter "a meter that closes
    # more than it opens" and failed the game for obeying the doctrine. Third measured
    # instance of the class SKILL.md names. Excluding `hidden = true` keys keeps the
    # anti-narrowing property intact: marking a trait hidden also removes it from the
    # sidebar (engine.md §30), so it genuinely is not a meter the player can be lied to
    # by, which is the only thing this test exists to catch.
    _hidden = {l.get("key") for l in ((game.get("traits") or {}).get("labels") or [])
               if isinstance(l, dict) and l.get("hidden") and l.get("key")}
    descents = [k for k in sorted(set(p_expand) | set(p_contract))
                if p_contract[k] >= p_expand[k] and (p_expand[k] + p_contract[k])
                and k not in bad and k not in _hidden]

    gate("ascent tiers expand the world",
         None if not (expand or contract) else (bool(tiers) and not bad and not descents),
         f"[{source}] " + ", ".join(f"{k} ({expand[k]}+/{contract[k]}-)" for k in tiers)
         if tiers else "no gated meter found",
         [f"{k} closes more than it opens ({expand[k]} expanding / {contract[k]} contracting)"
          for k in bad] +
         [f"{k} is a player meter that closes more than it opens "
          f"({p_expand[k]}+/{p_contract[k]}-) and is NOT declared as an ascent tier — "
          f"a descent wearing an ascent's clothes is invisible to the declaration"
          for k in descents] +
         [f"also ranked: {k} ({expand[k]}+/{contract[k]}-)" for k in ranked if k not in tiers])

    # ─────────────────────────────────────────────────────────────────────────
    # G11-G19 — added 2026-08-12, derived from a FIELD of 18 shipped sandboxes
    # rather than from the single reference game. See the module docstring.
    #
    # Several of these judge the game against what the BOARD PHASE DECLARED,
    # because the property cannot be inferred from the TOML. That pattern held in
    # all four doctrine studies and is now the standard shape. Its n/a rule:
    #   no v2_state.json at all -> n/a, nothing was ever declared to check against
    #   ledger present, field missing -> FAIL, naming the missing key
    # ─────────────────────────────────────────────────────────────────────────
    board = ((state or {}).get("board") or {})
    locs = game.get("locations") or []
    loc_ids = {l["id"] for l in locs if l.get("id")}

    # G11 — every location reachable on foot from the start.
    # Movement is undirected: the engine generates the return link from entry_from,
    # so an edge in either field connects both ways.
    adj = collections.defaultdict(set)
    for l in locs:
        lid = l.get("id")
        if not lid:
            continue
        if l.get("entry_from"):
            adj[lid].add(l["entry_from"])
            adj[l["entry_from"]].add(lid)
        for child in (l.get("navigation_order") or []):
            adj[lid].add(child)
            adj[child].add(lid)
    start_canvas = (game.get("project") or {}).get("starting_canvas")
    start_loc = next((((c.get("trigger") or {}).get("location"))
                      for c in (game.get("canvases") or []) if c.get("id") == start_canvas), None)
    if not start_loc:
        start_loc = next((l["id"] for l in locs if not l.get("entry_from")), None)
    seen_locs, stack = set(), [start_loc] if start_loc else []
    while stack:
        cur_loc = stack.pop()
        if cur_loc in seen_locs:
            continue
        seen_locs.add(cur_loc)
        stack.extend(adj[cur_loc] - seen_locs)
    # `offscreen` is a schedule label with no nav card; `auto_exit = false` is a
    # deliberately sealed room entered only by a canvas exit. Neither is stranded.
    exempt = {l["id"] for l in locs if l.get("offscreen") or l.get("auto_exit") is False}
    stranded = sorted(loc_ids - seen_locs - exempt)
    gate("world reachable", None if not loc_ids else not stranded,
         f"{len(seen_locs & loc_ids)}/{len(loc_ids)} locations reachable on foot from "
         f"{start_loc or '(no start)'}",
         [f"{l} is not reachable and is not marked offscreen/sealed" for l in stranded])

    # G12 — everyone who lives here has somewhere to sleep.
    # Not inferable: a shopkeeper legitimately has no bed in the player's house and
    # a tenant on nights legitimately has no night schedule row. Only a declaration
    # separates "lives elsewhere" from "was never given a room".
    chars = board.get("characters") or []
    bmap = board.get("map") or {}
    homes = bmap.get("homes") or {}
    if state is None:
        gate("residents have homes", None, "no v2_state.json — nothing declared to check against")
    elif not bmap:
        gate("residents have homes", False, "board.map not declared",
             ["the board phase must record the map: archetype, shape, home_base, exterior, homes",
              "until it does, a cast with nowhere to sleep cannot be distinguished from one that lives out"])
    else:
        homeless = []
        for ch in chars:
            cid2 = ch.get("id")
            where = homes.get(cid2)
            if where is None:
                homeless.append(f"{cid2}: no home declared in board.map.homes")
            elif where not in loc_ids and where != "offscreen":
                homeless.append(f"{cid2}: home '{where}' is not a declared location")
        gate("residents have homes", None if not chars else not homeless,
             f"{len(chars)-len(homeless)}/{len(chars)} characters have a home that exists", homeless)

    # G13 — the guidance surface is authored, not just switched on.
    # `quests_engine = "v2"` lights up a sidebar entry and a page; without cards it
    # renders a heading and nothing. Measured genre failure: lostness is the dominant
    # player complaint at a 4.7% median share of comments, against grind's 0.9%.
    cards = game.get("quest_cards") or []
    tiers_owed = board.get("ascent_tiers") or []
    engine_on = ((game.get("project") or {}).get("quests_engine") == "v2"
                 or (game.get("settings") or {}).get("quests_engine") == "v2")
    def _card_mentions(card, key):
        blob = json.dumps(card)
        return f'"{key}"' in blob
    if not engine_on and not cards:
        gate("guidance exists", None, "quests engine not enabled — no guidance surface to author")
    elif not tiers_owed and not chars:
        # Cards exist but the ledger names no tiers and no characters, so there is
        # nothing to check them against. An absence is not a pass.
        gate("guidance exists", None,
             f"{len(cards)} quest cards, but board.ascent_tiers/characters undeclared — nothing to judge coverage against")
    else:
        # ⚠️ THE CAST COMES FROM THE GAME, NOT THE BOARD. Iterating board.characters let an
        # author owe fewer cards by naming fewer people: truncating the declared cast to one
        # reported "24 quest cards for 3 ascent tiers and 1 characters" and still passed. Every
        # [[npcs]] entry is a character the player can find — gate 6 already requires each to be
        # scheduled and reachable — so every one of them owes a card. The declaration may add
        # to what is checked; it may never subtract.
        game_npcs = [n for n in (game.get("npcs") or []) if n.get("id")]
        cast = {n["id"] for n in game_npcs} | {c.get("id") for c in chars if c.get("id")}

        gaps = []
        if not cards:
            gaps.append("0 [[quest_cards]] authored — the guidance page renders empty")
        else:
            for t in tiers_owed:
                if not any(_card_mentions(c, t) for c in cards if not c.get("npc_id")):
                    gaps.append(f"ascent tier '{t}' has no story-tier card — nothing tells the player its next rung")
            carded = {c.get("npc_id") for c in cards if c.get("npc_id")}
            for cid in sorted(cast):
                if cid not in carded:
                    gaps.append(f"{cid} has no quest card — their sidebar next-row renders blank")
        gate("guidance exists", not gaps,
             f"{len(cards)} quest cards for {len(tiers_owed)} ascent tiers and "
             f"{len(cast)} characters in the game",
             gaps)

    # ⚠️ THERE IS NO "walls state their key" GATE, AND THE ABSENCE IS DELIBERATE.
    # It was written, it fired on 7 of 8 doors in a real game, and it was WRONG:
    # `references/engine.md` §15 already rules on this and rules the other way —
    # omitting `locked_text` shows the greyed ACTION ("Ask him where the bench went"),
    # which is a want the player can name and is what sells the next release; setting
    # it replaces the want with a reason and is "weaker as a door". Preferring the want
    # is the documented default, verified live.
    # A locked choice showing its own action text is therefore NOT silent — it states
    # the want. What it does not state is the ROUTE, and that is `the-voice.md` R3's
    # job on the guidance card, already enforced by "guidance exists" below. A gate
    # here would fail a game for obeying the skill, and would duplicate that one.

    # G15 — no character's ladder ends in silence.
    # pickQuestsCard returns the single highest-priority match; when an arc's last
    # card retires with nothing behind it the whole section disappears from the page,
    # at the exact moment that character becomes permanent sandbox content. This bites
    # v2 harder than it bites a finite game, because a v2 product never ends.
    by_npc = collections.defaultdict(list)
    for c in cards:
        if c.get("npc_id"):
            by_npc[c["npc_id"]].append(c)
    silent_chains = []
    for npc_id, cs in sorted(by_npc.items()):
        forever = any(c.get("terminal") or (not c.get("goals") and not c.get("ready_text")) for c in cs)
        if not forever:
            silent_chains.append(f"{npc_id}: {len(cs)} cards, none terminal or end-of-content — "
                                 f"section vanishes when the arc closes")
    gate("no chain ends in silence", None if not by_npc else not silent_chains,
         f"{len(by_npc)-len(silent_chains)}/{len(by_npc)} character ladders keep a card after the last rung",
         silent_chains)

    # ── the economy gates ────────────────────────────────────────────────────
    # Measured over 18 shipped sandboxes, 2026-08-12:
    #   money gates content ....... median 67.3 conditions per 1,000 passages;
    #                               every sandbox in the set does it
    #   sinks outnumber sources ... median 2.2 : 1 (DoL 1.76 : 1)
    #   recurring obligation ...... 14 of 19 games carry one (DoL says "rent" 130x)
    econ = board.get("economy") or {}
    currency = econ.get("currency")
    cur_src = "declared"
    if not currency:
        # Pick by USAGE, not by declaration order. A game can carry more than one
        # real currency — vesper runs `money` (Credits, company-visible) alongside
        # `coin` (hers, hidden) — and taking the first name match judged the wrong
        # one. Same bug class already fixed once in the corpus extractor, where a
        # decoy `randomMoney` beat the real currency on name alone.
        cands = [k for k in ((game.get("player") or {}).get("core_traits") or {})
                 if CURRENCY_HINT.search(k)]

        def _usage(trait):
            ops = []
            for c in model:
                _currency_ops(c, trait, ops)
            return len(ops) + sum(1 for c in model if trait in c["reads"])

        if cands:
            ranked = sorted(cands, key=lambda t: (-_usage(t), cands.index(t)))
            currency = ranked[0]
            cur_src = "inferred — board.economy.currency not declared"
            if len(ranked) > 1:
                cur_src += (f"; chose `{currency}` ({_usage(currency)} uses) over "
                            + ", ".join(f"`{t}` ({_usage(t)})" for t in ranked[1:3]))

    if not currency:
        for nm in ("money gates something", "sinks >= sources", "no free uncapped income"):
            gate(nm, None, "no currency found — game declares none and none inferable")
    else:
        # A `costs` block IS a gate: the engine refuses the choice when the player
        # cannot afford it (v2.py:12556). `reads` is built from conditions only
        # (see _conditions_of above), so a game that prices its choices instead of
        # condition-gating them read as "nothing gates on money" — vesper spends
        # `coin` on seven choices and scored zero here.
        def _prices_currency(c):
            for n in c["nodes"]:
                for ch in ((n.get("exit_block") or {}).get("choices") or []):
                    cs = ch.get("costs") or []
                    if isinstance(cs, dict):
                        cs = [cs]
                    if any(isinstance(x, dict) and x.get("trait") == currency for x in cs):
                        return True
            return False

        reads_cur = sorted(c["id"] for c in model
                           if currency in c["reads"] or _prices_currency(c))
        gate("money gates something", bool(reads_cur),
             f"[{cur_src}] {len(reads_cur)} canvases gate on `{currency}` "
             f"(conditions or an affordability cost)",
             [] if reads_cur else
             [f"nothing in the game reads `{currency}` — every arc gated behind it is optional scenery",
              "field median is 67.3 money conditions per 1,000 passages; every measured sandbox gates on money"])

        sources, sinks = set(), set()
        for c in (game.get("canvases") or []):
            ops = []
            _currency_ops(c, currency, ops)
            if "add" in ops:
                sources.add(c["id"])
            if "subtract" in ops:
                sinks.add(c["id"])
        rent = (game.get("settings") or {}).get("rent") or {}
        if rent.get("enabled"):
            sinks.add("[settings.rent]")

        # ⚠️ COUNTING SINKS IS NOT ENOUGH — ASK WHERE THEY ARE.
        # The first version of this gate counted 21 sinks against 20 sources and passed
        # a game whose sinks were TWELVE PURCHASE BUTTONS ON ONE FRONT DESK. That is a
        # shop counter, not an economy: money leaves the player in one place, by one
        # gesture, and no other room is ever the reason she needs it.
        # This is the same error the explicit-in-repeatable gate already avoids for
        # heat — presence is not placement — and it was rebuilt here anyway.
        loc_of = {c["id"]: c["loc"] for c in model}
        sink_locs = collections.Counter(loc_of.get(s, "(engine)") for s in sinks
                                        if s != "[settings.rent]")
        top_loc, top_n = (sink_locs.most_common(1) or [("—", 0)])[0]
        concentrated = len(sinks) >= 5 and top_n > len(sinks) / 2

        fails = []
        if len(sinks) < len(sources):
            fails.append(f"more ways to earn `{currency}` than to spend it — "
                         f"the meter it feeds never has to rise")
            fails.append(f"sources: {', '.join(sorted(sources)[:8])}")
        if concentrated:
            fails.append(f"{top_n} of {len(sinks)} sinks are at ONE location ({top_loc}) — "
                         f"that is a shop counter, not an economy")
            fails.append("a sink belongs where the thing being bought lives, so the room it "
                         "improves is the reason she needs the money — references/the-economy.md")
        gate("sinks >= sources", None if not (sources or sinks) else not fails,
             f"{len(sinks)} sinks : {len(sources)} sources (field median 2.2 : 1)"
             + (f" · {top_n} at {top_loc}" if top_n else ""),
             fails)

        # Any repeatable surface granting currency with no brake on the way in is a
        # money printer, and every other economy rule is void beside it.
        #
        # ⚠️ REWRITTEN 2026-08-16, and the old version was wrong in two ways at once.
        #
        # 1. It read `c["costs"]`, which is `trigger.costs`. A triggerless RUNG has no
        #    trigger, so its real brake — `costs` on the hub choice that reaches it —
        #    was invisible. Every priced rung in every game read as unpriced.
        # 2. It then EXCUSED exactly those rungs, on the-economy.md R5's old footnote:
        #    "a triggerless rung behind a gated hub choice is not free, only farmable."
        #    Every rung in a v2 game is a triggerless rung behind a hub choice, so the
        #    footnote exempted the whole architecture. Measured: a rung paying £2 per
        #    25 minutes, uncapped, behind `standing >= 35`, against a £20 weekly
        #    obligation. This gate printed "4 gated rungs are uncapped too" and passed.
        #    A gate in front of a printer delays the printer. Footnote struck.
        #
        # Brakes are now resolved per ROUTE by _routes(): a costs block on the choice,
        # max_triggers_per_day on the target, or a self-limiting `_today` condition.
        # One unbraked door is enough to make a rung farmable, so _is_free is a min
        # over routes, not a max.
        printers = []
        by_id_all = {x["id"]: x for x in (game.get("canvases") or [])}
        for c in model:
            if not c["rep"] or not _is_free(c["id"], routes, game):
                continue
            if c["id"] in by_id_all and not _farmable(by_id_all[c["id"]]):
                continue                              # dev shortcut — no player can reach it
            ops = []
            _currency_ops({"nodes": c["nodes"]}, currency, ops)
            if "add" not in ops:
                continue
            _g, mins = _grants(c["nodes"], _tick_cleared(game))
            amt = sum(v for (subj, _n, t), v in _g.items() if subj == "player" and t == currency)
            if amt <= 0:
                continue          # every grant on it is day-capped — not a faucet
            printers.append(
                f"{c['id']} @{c['loc']}: grants +{amt:g} `{currency}` every {mins or 0} min "
                f"with no cost, no cap and no daily limit")
        gate("no free uncapped income", not printers,
             f"{len(printers)} repeatable surfaces print money without limit"
             if printers else "every income surface has a brake on every route in",
             printers[:8] + (["the-economy.md R5 — price the choice (`costs`), or day-cap the "
                              "rung with a flag cleared in [engine.daily_tick]. Being behind a "
                              "tier gate is not a cap: the tier is bought once, the rung repeats."]
                             if printers else []))

        # G21 — a price the player cannot see cannot be planned against.
        #
        # Measured by PLAYING (DOCTRINE_GAPS study 5, R3): every field game that
        # charges money names the amount on the label itself — "Buy coffee (0:02
        # £2)", "Paper - 80$ for a piece". The player is budgeting against a stated
        # obligation (DoL: "Bailey wants £100 on Sunday"), so a hidden price is a
        # plan they cannot make.
        #
        # This is money ONLY, deliberately. The field is split on stamina-type
        # costs — two corpus games label them, the reference game does not — and a
        # second rule there would be an invented threshold, which is the failure
        # that demoted the-surfaces R5 and R6. Non-currency costs are counted in
        # the headline and never judged.
        priced, silent, other_cost = 0, [], 0
        for c in model:
            for n in c["nodes"]:
                for ch in ((n.get("exit_block") or {}).get("choices") or []):
                    costs = ch.get("costs") or []
                    if isinstance(costs, dict):
                        costs = [costs]
                    amt = next((x.get("value") for x in costs
                                if isinstance(x, dict) and x.get("trait") == currency), None)
                    if amt is None:
                        other_cost += sum(1 for x in costs if isinstance(x, dict))
                        continue
                    priced += 1
                    if str(amt) not in (ch.get("text") or ""):
                        silent.append(f"{c['id']} @{c['loc']}: \"{(ch.get('text') or '')[:58]}\""
                                      f" costs {amt} {currency}, label does not say so")
        if priced:
            gate("a price is on its label", not silent,
                 f"{len(silent)} of {priced} choices spend `{currency}` without naming the amount"
                 + (f" · {other_cost} non-currency costs not judged" if other_cost else ""),
                 silent + (["field: every game in the play corpus that charges money puts the "
                            "amount in the label — the player is budgeting against a deadline"]
                           if silent else []))
        else:
            gate("a price is on its label", None,
                 f"no choice spends `{currency}` — nothing to judge"
                 + (f" ({other_cost} non-currency costs, not judged)" if other_cost else ""))

    # G37 — one currency, or the player cannot read a price.
    #
    # the-economy.md R7. Measured failure: a shipped game wrote the price of ONE
    # click six ways — "Feed the meter (GBP 3)" on the button, "Three pounds" in
    # the paragraph, "Requires 3 Money (you have 1)" when she was short (v2.py:4680),
    # "money: 12 / 100" in the sidebar (v2.py:16241) and "$90" on the rent card
    # (v2.py:1190, the default nobody declared). Three of the six were the engine's.
    #
    # Judged on UNIT, not on form: "$" and "dollars" are one currency written two
    # ways, and the field ships both in one game. Two units is two currencies.
    # The engine's own symbol is a channel like any other — it is what the rent
    # pages print, declared or not — and so is the ledger's declaration.
    _c0, cur_declared, cur_engine, _e0 = _cur_setup(model, game, state)
    cur_extra = _cur_extra(currency, cur_declared)
    cur_seen = {}

    def _cur_note(unit, where, form, shown):
        cur_seen.setdefault(unit, []).append(f"{where}: {shown}  [{form}]")

    for _cid, _kind, _text in _cur_labels(model):
        for _u, _form, _chan in _cur_units(_text, cur_extra):
            _cur_note(_u, f"{_cid} ({_kind})", _form, f'"{_text[:56]}"')
    if cur_declared:
        _cur_note(_CUR_UNIT.get(cur_declared.lower(), cur_declared.lower()),
                  "board.economy.symbol", cur_declared, f'declared "{cur_declared}"')
    if cur_engine:
        _cur_note(_CUR_UNIT.get(cur_engine.lower(), cur_engine.lower()),
                  "[settings.rent]", cur_engine,
                  f'currency_symbol "{cur_engine}"'
                  + ("" if ((game.get("settings") or {}).get("rent") or {}).get("currency_symbol")
                     else " — NOT DECLARED, this is the engine default (v2.py:1190)"))

    if not cur_seen:
        gate("the price is in one currency", None,
             "no button, ledger or rent setting names a currency — nothing to judge")
    else:
        _units = sorted(cur_seen, key=lambda u: (-len(cur_seen[u]), u))
        _hits = sum(len(v) for v in cur_seen.values())
        if len(_units) == 1:
            _extra_note = []
            if not cur_declared:
                _extra_note = ["declare it: `board.economy.symbol` in the ledger, so a re-price "
                               "or a new author cannot start a second one (the-economy.md R7)"]
            gate("the price is in one currency", True,
                 f"one currency (`{_units[0]}`) across {_hits} "
                 + ("place" if _hits == 1 else "places")
                 + (f" · declared `{cur_declared}`" if cur_declared
                    else " · not declared in the ledger"),
                 _extra_note)
        else:
            _detail = []
            for _u in _units:
                for _line in cur_seen[_u][:3]:
                    _detail.append(f"`{_u}` — {_line}")
                if len(cur_seen[_u]) > 3:
                    _detail.append(f"`{_u}` — and {len(cur_seen[_u]) - 3} more")
            gate("the price is in one currency", False,
                 f"{len(_units)} currencies on the screen: "
                 + " · ".join(f"`{u}` x{len(cur_seen[u])}" for u in _units),
                 _detail + ["the-economy.md R7 — declare `board.economy.symbol`, set "
                            "`[settings.rent] currency_symbol` to the same string, and write "
                            "that notation on every button. `engine.md` §33 lists the sixteen "
                            "places the engine prints money and the four the setting reaches"])

    # G20 — a place is not a catalogue.
    # The seam to split on is always available: one canvas per (who it is aimed at
    # x when). A hub that has grown past this is doing several jobs at once — almost
    # always a character hub with solo work dumped into it, or a shop merged into a
    # room. references/the-surfaces.md.
    #
    # ⚠️ THE HEADLINE REPORTS THE DISTRIBUTION, NOT THE VERDICT — added 2026-08-15, study 6.
    # "0 screens over 8" and "19 of 30 screens at exactly 8" are the same PASS and completely
    # different games, and the scoreboard could not tell them apart: the game this cap was
    # written to fail (23 on one desk, 214 choices over 22 screens) and the game that replaced
    # it (max 8, 213 choices over 29 screens) both read as solved. A ceiling makes "pass" and
    # "maximise" point the same way, so a ceiling gate that prints only a verdict teaches the
    # cap as the spec. Same discipline as G2's marginal-pass headline.
    #
    # ⚠️ ROOMS AND CHARACTER HUBS ARE COUNTED SEPARATELY, and the reason is the denominator
    # trap this project has now hit six times. R3 is about ROOMS. Character hubs are shaped by
    # a different rule (R1/R2's object test) and measured well: on the game that prompted this
    # they open a median of 3 choices, exactly the field figure. Averaging them together
    # reported "19/29 screens at the cap" when the rooms alone were 18 of 22 — the good screens
    # were diluting the bad ones in the number meant to expose them. The cap still applies to
    # both; only the reporting is split.
    npc_bound = {x["id"] for x in (game.get("canvases") or [])
                 if (x.get("trigger") or {}).get("npc")
                 or (x.get("trigger") or {}).get("requires_npc")}
    fat, per_screen, per_hub = [], [], []
    for c in model:
        if not c["rep"]:
            continue
        if not (c["id"] in {x["id"] for x in (game.get("canvases") or [])
                            if (x.get("trigger") or {}).get("location")}):
            continue                                  # rungs are link targets, not screens
        for n in c["nodes"]:
            # Count DECISIONS, not navigation. A choice that leaves for another
            # location is an exit; the field's big screens are mostly exits and
            # standing travel affordances, and only 1-6 things to actually do.
            # Today this excludes nothing — every choice we have ever authored is
            # targetType "node" — but the engine does support location targets
            # (v2.py:13252), so the count is made denominator-proof up front.
            choices = (n.get("exit_block") or {}).get("choices") or []
            decisions = [ch for ch in choices
                         if (ch.get("targetType") or "node") != "location"]
            if decisions:
                (per_hub if c["id"] in npc_bound else per_screen).append(len(decisions))
            if len(decisions) > MENU_CEILING:
                exits = len(choices) - len(decisions)
                fat.append(f"{c['id']} @{c['loc']}: {len(decisions)} decisions on one screen"
                           + (f" (+{exits} exits, not counted)" if exits else ""))
    at_cap = sum(1 for k in per_screen if k == MENU_CEILING)
    shape = (f"rooms median {_median(per_screen)} · {at_cap}/{len(per_screen)} at the cap"
             if per_screen else "no repeatable room screens")
    if per_hub:
        shape += (f" · character hubs median {_median(per_hub)} "
                  f"({sum(1 for k in per_hub if k == MENU_CEILING)}/{len(per_hub)} at the cap)")
    gate("a place is not a catalogue", not fat,
         f"{len(fat)} screens over {MENU_CEILING} · {shape}",
         fat + (["field, measured by PLAYING five games: a location screen carries 1-6 things to "
                 "actually do (median 3). Big screens in real games are wardrobes, rosters and "
                 "character builders — or they are mostly exits, which are not counted here"]
                if fat else [])
         + ([f"⚠️ {at_cap} of {len(per_screen)} screens sit ON the cap. {MENU_CEILING} is a "
             f"backstop for the pathological case, NOT the size of a normal room — the field "
             f"median is 3. A room's list is needs + work + people (the-surfaces.md R2) — a "
             f"CLOSED set that sizes itself, not an open one filled up to this number."]
            if per_screen and at_cap * 2 > len(per_screen) else []))

    # ⚠️ THE TWO SCREEN-SHAPE RULES ARE LINTS, NOT GATES — see lint_screen_shape().
    # `the-surfaces.md` R5 (ungated doors) and R6 (does the screen move) are real rules that a
    # real game ignored, and both were built here as gates before the thresholds were
    # checked. Neither survived the check:
    #   R5: the ceiling had to be invented — one game sits at exactly 50% and passes
    #       while another fails at 52%, which is noise, not a measurement.
    #   R6: not field-comparable AT ALL. In a compiled Twine file `<<if>>` covers engine
    #       plumbing — gated choices, media, presence — not just authored prose banding,
    #       and the two cannot be separated in someone else's build. Measured that way
    #       our games score 84% and 89% against a field median of 86%, which says
    #       nothing about whether the PROSE moves.
    # Whether a room's narrative actually changes on re-entry is a question only PLAY
    # answers. Reported as lints until the play study sets real numbers.

    # G24 — the declared obligation is actually charged.
    #
    # ⚠️ MEASURED FAILURE. A game declared "GBP 200 a week back, plus GBP 45 for the caravan",
    # printed "Have the two hundred and forty-five" on its quest card, and wrote the scene of
    # handing the money through a car window — and the settle-up canvas carried NO cost and NO
    # money effect. Played live with GBP 300: before 300, after 300, and repeatable without
    # limit. The whole game's money outflow was 11 optional purchases totalling GBP 90 against
    # GBP 70 a night of income.
    #
    # Gate 16 passed it, because nine OTHER canvases gate on money. That is the presence-gate
    # failure mode: "at least one exists" cannot see that the important one does not. This is
    # SKILL.md:107 applied to the field the economy is built on — the board declares a price,
    # so the gate checks the price is taken.
    ob = econ.get("obligation")
    ob_amt = econ.get("obligation_amount")
    has_ob = isinstance(ob, str) and ob.strip() and ob.strip().lower() not in ("none", "n/a")
    if not currency:
        gate("the obligation is charged", None, "no currency declared — nothing to price")
    elif not has_ob:
        gate("the obligation is charged", None,
             "no board.economy.obligation declared — nothing to check against",
             ["the-economy.md R3: a recurring obligation is near-universal in the field; "
              "declaring none is a choice, not an omission"])
    else:
        # `_currency_ops` collects operations, not amounts, and this gate needs the amount —
        # so it walks for values itself rather than widening a helper five other gates share.
        #
        # ⚠️ TWO CHANNELS, AND THE FIRST VERSION KNEW ONLY ONE.
        # (1) An authored charge — a `costs` entry, or an effect written `op = "add"` with a
        #     NEGATIVE value. NOT `op = "subtract"`: that is not an engine op and moves nothing
        #     (v2.py:5742-5751), so counting it here would credit a charge that never happens —
        #     which is the exact failure this gate exists to catch, rebuilt inside the gate.
        # (2) `[settings.rent]` — the engine's own recurring-demand system. It arms on the day
        #     rollover to `due_day`, intercepts the next `Location_*` entry, and really does
        #     charge (`$player.core_traits.money -= _rent`, v2.py:15918-15928; verified live).
        #     Measured: a game whose obligation IS charged, by that system, failed this gate
        #     because the walk only looked at canvases. A check that fails a game for obeying
        #     the doctrine is a bug in the check.
        outflows = []
        rent_cfg = (game.get("settings") or {}).get("rent") or {}
        rent_amt = rent_cfg.get("amount") if rent_cfg.get("enabled") else None
        rent_charges = isinstance(rent_amt, (int, float)) and rent_amt > 0

        def _outflows(o):
            if isinstance(o, dict):
                if ((o.get("trait") or o.get("trait_key")) == currency
                        and o.get("op") == "add"
                        and isinstance(o.get("value"), (int, float))
                        and o["value"] < 0):
                    outflows.append(-o["value"])
                for cost in (o.get("costs") or []):
                    if (isinstance(cost, dict) and cost.get("trait") == currency
                            and isinstance(cost.get("value"), (int, float))):
                        outflows.append(cost["value"])
                for v in o.values():
                    _outflows(v)
            elif isinstance(o, list):
                for v in o:
                    _outflows(v)

        _outflows(game.get("canvases") or [])
        biggest = max(outflows) if outflows else 0
        charged_by = None
        if rent_charges and rent_amt >= (ob_amt if isinstance(ob_amt, (int, float)) else 0):
            charged_by = f"[settings.rent] {rent_amt:g} every {rent_cfg.get('due_day', '?')}"
        elif isinstance(ob_amt, (int, float)) and biggest >= ob_amt:
            charged_by = f"an authored charge of {biggest:g}"

        gaps = []
        if not isinstance(ob_amt, (int, float)) or ob_amt <= 0:
            gaps.append("board.economy.obligation is declared but board.economy.obligation_amount "
                        "is not — an obligation with no price cannot be checked, and one that "
                        "cannot be checked is how a game shipped with its central charge missing")
        elif not charged_by:
            gaps.append(f"nothing takes {ob_amt:g} `{currency}` from the player: the largest "
                        f"authored outflow is {biggest:g}"
                        + (f" and [settings.rent] charges {rent_amt:g}" if rent_charges
                           else " and [settings.rent] is not enabled")
                        + " — the price is written in the ledger and the prose but never taken")
        gate("the obligation is charged", not gaps,
             f"[declared] {ob_amt if isinstance(ob_amt, (int, float)) else '?'} {currency}"
             + (f" · charged by {charged_by}" if charged_by else "")
             + f" · largest authored outflow {biggest:g} across {len(outflows)} charges",
             gaps)

    # G25 — every effect uses an op the engine actually runs.
    #
    # ⚠️ THE CHEAPEST GATE HERE, AND IT CATCHES THE MOST INVISIBLE CLASS OF BUG.
    # `applyTraitEffect` runs `add` and `set`, and on anything else falls through to
    # `// Unknown op; do nothing` and RETURNS (v2.py:5742-5751). Nothing normalises the
    # value: `subtract` appears nowhere in the generator or the importer. The importer
    # validates `op` for cheat-page grants (template_import.py:3755) and for nothing else,
    # so a dead effect is valid TOML, builds green, and emits verbatim into the HTML.
    #
    # Measured, on two v2 games authored from the same skill: 35 dead effects in one and
    # 70 in the other. In the first, a whole declared meter never moved for the entire game
    # — the counterweight that "only ever falls" was frozen at its starting value across 12
    # dead decrements — twenty activities never charged the energy they said they cost, and
    # the one NPC penalty in the game never applied. Every gate here passed it, and a live
    # play-through passed it too, because the number simply does not change and nothing says
    # why. `references/engine.md` §21 had discussed `op = "subtract"` as though it worked.
    #
    # SCOPED TO CANVASES AND THE ENGINE BLOCK on purpose: quest-card `goals`/`when` entries
    # legitimately carry `trait` + `op = "gte"|"lt"`, and they are comparisons, not effects.
    # Anything carrying `subject` or `operator` is a condition and is skipped for the same
    # reason.
    LIVE_OPS = {
        "trait": ({"add", "set"}, "v2.py:5742-5751"),
        "flag": ({"set", "unset", "toggle"}, "v2.py:5888"),
        "quest": ({"start", "update", "complete", "cancel"}, "v2.py:5914-5919"),
    }
    dead = collections.Counter()
    dead_where = collections.defaultdict(set)

    def _walk_ops(o, cid):
        if isinstance(o, dict):
            if "subject" not in o and "operator" not in o and isinstance(o.get("op"), str):
                kind = ("flag" if o.get("flag") else
                        "quest" if (o.get("quest_id") or o.get("questId") or o.get("quest")) else
                        "trait" if o.get("trait") else None)
                if kind and o["op"] not in LIVE_OPS[kind][0]:
                    dead[(kind, o["op"])] += 1
                    dead_where[(kind, o["op"])].add(cid)
            for v in o.values():
                _walk_ops(v, cid)
        elif isinstance(o, list):
            for v in o:
                _walk_ops(v, cid)

    for c in (game.get("canvases") or []):
        _walk_ops(c, c.get("id", "?"))
    _walk_ops(game.get("engine") or {}, "[engine]")

    detail = []
    for (kind, op), n in dead.most_common():
        live = ", ".join(sorted(LIVE_OPS[kind][0]))
        where = sorted(dead_where[(kind, op)])
        detail.append(f"{n} {kind} effects use op = \"{op}\", which the engine discards — "
                      f"the {kind} ops it runs are {live} ({LIVE_OPS[kind][1]})")
        detail.append(f"    in: {', '.join(where[:6])}"
                      + (f" … and {len(where) - 6} more canvases" if len(where) > 6 else ""))
    if dead:
        detail.append("to take something away, write op = \"add\" with a NEGATIVE value; "
                      "a quantity like money must also carry clamp = false (engine.md §21)")
    gate("effects use a live op", not dead,
         f"{sum(dead.values())} effects use an op the engine does not run"
         if dead else "every effect op is one the engine runs",
         detail)

    # ─────────────────────────────────────────────────────────────────────────
    # A DAY-CAP CLOSES.  the-meters.md M5 · engine.md §28.
    #
    # The day cap on a triggerless rung has THREE parts: set the flag, gate the
    # choice on it being false, clear it in [engine.daily_tick]. Two of three
    # validates and does nothing.
    #
    # Measured failure: a shipped game read four `*_talk_today` flags as is_false on
    # four hub choices and cleared all four in the tick, and NO canvas ever set them.
    # A flag nothing sets is permanently false, so every one of those gates fails
    # open and the four talk screens were re-clickable every twenty minutes — a
    # faster route to the cast meters than the day-capped rung they sit below.
    #
    # ⚠️ Nothing else in the toolchain can see it. The generator's flag-chain
    # validator checks `operator == "is_true"` only (`v2.py:11659`) — deliberately,
    # because an is_false read is a re-entry guard rather than a prerequisite — so a
    # never-set flag read as is_false is legal, silent, and green. The build passes,
    # `the climb is paid for` passes (energy is still a real cost on the route in),
    # and the throttle the whole climb was costed against does not exist.
    #
    # Fully mechanical: no threshold, no field measurement, nothing to judge. A cap
    # with no setter cannot close, whatever the author meant.
    # ─────────────────────────────────────────────────────────────────────────
    tick_cleared = set()
    for fe in (((game.get("engine") or {}).get("daily_tick") or {}).get("flagEffects") or []):
        if isinstance(fe, dict) and fe.get("op") == "unset" and fe.get("flag"):
            tick_cleared.add(str(fe["flag"]))

    cap_set, cap_read = collections.defaultdict(set), collections.defaultdict(set)

    def _walk_caps(o, cid):
        if isinstance(o, dict):
            for fe in (o.get("flagEffects") or []):
                if isinstance(fe, dict) and fe.get("op") == "set" and fe.get("flag"):
                    cap_set[str(fe["flag"])].add(cid)
            if o.get("type") == "flag" and o.get("operator") == "is_false" and o.get("flag_key"):
                cap_read[str(o["flag_key"])].add(cid)
            for v in o.values():
                _walk_caps(v, cid)
        elif isinstance(o, list):
            for v in o:
                _walk_caps(v, cid)

    for c in (game.get("canvases") or []):
        # A dev shortcut is stripped from a shipped build, so it is not a setter.
        if _is_dev(c):
            continue
        _walk_caps(c, c.get("id", "?"))

    open_caps = sorted(f for f in tick_cleared if cap_read.get(f) and not cap_set.get(f))
    detail = []
    for f in open_caps:
        where = sorted(cap_read[f])
        detail.append(f"`{f}` — read as is_false in {', '.join(where[:3])}"
                      + (f" (+{len(where) - 3} more)" if len(where) > 3 else "")
                      + " and cleared in [engine.daily_tick], but NO canvas sets it")
    if open_caps:
        detail.append("the-meters.md M5 — a day cap is three parts. Set the flag on the CHOICE "
                      "that opens the rung (a choice runs its flagEffects BEFORE advanceTime, "
                      "v2.py:12648-12733; a node exit runs them AFTER, v2.py:13085-13088, so an "
                      "exit-set flag on a midnight-crossing rung lands on the new day)")
    gate("a day-cap closes",
         None if not tick_cleared else not open_caps,
         (f"{len(open_caps)} day-cap flag(s) are read and cleared but never set"
          if open_caps else
          f"{len(tick_cleared)} day-cap flag(s) cleared in [engine.daily_tick], all of them set somewhere")
         if tick_cleared else "no [engine.daily_tick] flag clears — no day cap to check",
         detail)

    # ─────────────────────────────────────────────────────────────────────────
    # G37 — A SPENT DAY STILL HAS A DOOR.  the-surfaces.md R6 · the-meters.md M5.
    #
    # The other half of the gate above. `a day-cap closes` asks whether the cap has a
    # SETTER. This one asks what the screen looks like once the cap is SPENT — and a
    # day cap is spent every single day, by design, so this is not an edge state.
    #
    # Measured failure, 2026-08-23: the author of a shipped game walked into his own
    # NPC's hub, on a day he had already used that character's one rung and one talk,
    # and got a portrait, a paragraph, a line of dialogue and nothing to click. All TEN
    # hubs in that game did it, and three activity screens did the money-shaped version
    # of it. He could not tell whether the game was broken.
    #
    # ⚠️ THE CAP IS PER PERSON AND THE HUBS ARE PER ROOM. That game gave one character
    # three hubs — a yard, a harbour, an arcade counter — all reading one shared
    # `*_rung_today`. Spending it at the yard at 09:00 emptied the other two for the
    # rest of the day, and their whole list was that one flag.
    #
    # ⚠️ MIRROR THE ENGINE, DO NOT RE-INVENT IT. A choice is a DOOR only when it carries
    # neither `conditions` nor `costs` — that is precisely `has_unconditional_choice`
    # (v2.py:12827-12836), where a cost-bearing choice is registered as conditional
    # alongside a gated one. Get that wrong and the gate disagrees with the runtime.
    #
    # Two ways a choice is SHUT in a state the player reaches by ordinary play:
    #   · its AND-conditions read a day-cap flag `is_false` — spent, until tomorrow;
    #   · it spends `money` — and a player at $0 cannot earn any from inside the screen.
    # A node with no door, all of whose choices are shut, is a guaranteed dead screen.
    #
    # ⚠️ NOT EVERY ALL-CONDITIONAL NODE IS A DEAD END, and this gate must not say so.
    # Conditional ROUTING — `stealth gte 10` / `lt 10 + fighting` / `lt 10` catch-all —
    # is exhaustive by construction and cannot all-fail. Scoping to day caps and money
    # is what keeps it sound: measured across the ten built games, it finds 13 of 13 in
    # the game that shipped the defect and ZERO in the other nine, which between them
    # carry 29 all-conditional routing nodes.
    #
    # The fix is one choice, and every other game in the repo already ships it:
    # `{ text = "Leave him to it.", targetType = "location", locationId = <the hub's
    # own location> }` — no conditions, no costs, last in the list.
    # ─────────────────────────────────────────────────────────────────────────
    def _door(ch):
        """The engine's own test: free of BOTH gates (v2.py:12827-12836)."""
        return not ch.get("conditions") and not ch.get("costs")

    def _spent(ch):
        """Shut until tomorrow: reads a day-cap flag is_false."""
        cond = ch.get("conditions") or {}
        if str(cond.get("logic") or "AND").upper() != "AND":
            return False
        return any(it.get("type") == "flag" and it.get("operator") == "is_false"
                   and str(it.get("flag_key")) in tick_cleared
                   for it in (cond.get("items") or []))

    def _priced(ch):
        """Shut while broke, and no money is earnable from inside the screen."""
        return any(str(cst.get("trait")) == "money" for cst in (ch.get("costs") or []))

    shut_nodes = []
    for c in (game.get("canvases") or []):
        if _is_dev(c):
            continue
        for n in (c.get("nodes") or []):
            chs = (n.get("exit_block") or {}).get("choices") or []
            if not chs or any(_door(ch) for ch in chs):
                continue
            if not all(_spent(ch) or _priced(ch) for ch in chs):
                continue
            n_spent = sum(1 for ch in chs if _spent(ch))
            n_priced = len(chs) - n_spent
            why = ("all day-capped" if not n_priced else
                   "all priced" if not n_spent else
                   f"{n_spent} day-capped, {n_priced} priced")
            shut_nodes.append(f"{c.get('id')}.{n.get('id')} — {len(chs)} choice(s), "
                              f"{why}, none free of both conditions and costs")
    door_det = list(shut_nodes[:20])
    if shut_nodes:
        if len(shut_nodes) > 20:
            door_det.append(f"… and {len(shut_nodes) - 20} more")
        door_det.append('add one choice with neither `conditions` nor `costs`: '
                        '{ text = "Leave him to it.", targetType = "location", '
                        'locationId = <the node\'s own location> }')
    gate("a spent day still has a door",
         None if not tick_cleared else not shut_nodes,
         (f"{len(shut_nodes)} screen(s) empty once the day is spent"
          if shut_nodes else
          "every screen keeps one choice free of both conditions and costs")
         if tick_cleared else "no [engine.daily_tick] flag clears — no day cap to check",
         door_det)

    # ─────────────────────────────────────────────────────────────────────────
    # G26 — THE CLIMB IS PAID FOR.  the-meters.md M1.
    #
    # Every gate before this one asks whether a thing EXISTS. This one asks what it
    # COSTS, which is the question three shipped games passed without ever being
    # asked. Measured failure: a game with three correctly-declared ascent tiers,
    # gates at 15/35/55, every penetrative scene properly behind one — and a rung
    # granting +1 cover for 10 minutes, free, uncapped, repeatable forever. Live: 12
    # clicks took cover 4 -> 16 at no cost. Cover 0->55 is 55 clicks, nine hours of one
    # Monday. It scored 22/24.
    #
    # ⚠️ It walks the GAME, not a declaration. Every trait ANY condition reads is in
    # scope — the three declared tiers, the counterweight, and per-NPC relation, which
    # is where half of these games actually keep the lock. Same anti-narrowing property
    # gate 10 argues for: a gate that iterates a declaration can be weakened by
    # declaring less.
    #
    # ⚠️ It reports the RATE, not a verdict alone. A `costs` of 1 energy on a 10-minute
    # rung satisfies any boolean version of this check and changes nothing. Clicks and
    # in-game minutes to the top threshold are the numbers that cannot be faked, so
    # they print whether the gate passes or fails.
    thresholds = collections.defaultdict(float)      # (subject, trait) -> highest gate
    for c in (game.get("canvases") or []):
        for holder in [c.get("trigger") or {}] + _exit_holders(c.get("nodes")):
            for it in _conditions_of(holder):
                tk, op, v = it.get("trait_key"), it.get("operator"), it.get("value")
                if tk and op in ("gte", "gt") and isinstance(v, (int, float)):
                    thresholds[(it.get("subject") or "player", tk)] = max(
                        thresholds[(it.get("subject") or "player", tk)], float(v))

    grantors = collections.defaultdict(list)         # (subject, trait) -> [(cid, amt, min, req, free)]
    for c in (game.get("canvases") or []):
        if not _farmable(c):
            continue                                  # one-shots and dev shortcuts are not a grind
        got, minutes = _grants(c.get("nodes"), _tick_cleared(game))
        rs = routes.get(c["id"]) or []
        free_rs = [r for r in rs if not r["braked"]]
        free = _is_free(c["id"], routes, game)
        for (subject, _npc, trait), amt in got.items():
            if amt <= 0:
                continue
            # cheapest requirement across the FREE ways in — that is the value at which
            # this rung actually becomes farmable.
            req = min((r["reqs"].get(trait, 0.0) for r in free_rs), default=0.0) if free_rs else 0.0
            grantors[(subject, trait)].append((c["id"], amt, minutes, req, free))

    unpaid, priced_lines = [], []
    for key in sorted(thresholds, key=lambda k: (-thresholds[k], k[1])):
        subject, trait = key
        top = thresholds[key]
        gs = grantors.get(key) or []
        if not gs:
            continue                                  # nothing raises it — gate 7/10's problem, not this one
        free_gs = [(cid, amt, m, req) for cid, amt, m, req, fr in gs if fr]
        # Climb from the DECLARED starting value, not from zero — a counterweight that
        # starts at 70 is 5 points from a 75 gate, and saying "75 points of grind" there
        # would be the same denominator error this gate exists to catch.
        start = 0.0
        if subject == "player":
            sv = ((game.get("player") or {}).get("core_traits") or {}).get(trait)
            start = float(sv) if isinstance(sv, (int, float)) else 0.0
        climb = _free_climb(top, free_gs, start) if free_gs else None
        if climb:
            clicks, mins, used = climb
            route = " + ".join(f"{cid} ×{n}" for cid, n in used.most_common(2))
            unpaid.append(
                f"`{trait}` {int(start)} → gate at {int(top)}, entirely for FREE — "
                f"{clicks} clicks, {_hms(mins)} of game time, no cost, no cap ({route})")
        else:
            cheapest = min(gs, key=lambda g: ((g[2] or 0) / g[1], -g[1]))
            cid, amt, mins, _req, _fr = cheapest
            priced_lines.append(
                f"`{trait}` gates at {int(top)} · no free route to it · cheapest rung "
                f"{cid} +{amt:g} / {mins or 0} min")

    n_gated = len([k for k in thresholds if grantors.get(k)])
    gate("the climb is paid for", None if not n_gated else not unpaid,
         (f"{len(unpaid)} of {n_gated} gated meters can be raised for free"
          if unpaid else
          f"all {n_gated} gated meters carry a brake on every route in")
         if n_gated else "no trait gate has anything that raises it — nothing to price",
         unpaid + priced_lines[:4]
         + (["the-meters.md M3-M5 — spacing is never the brake; price the hub choice "
             "(`costs`), or day-cap it with a FLAG cleared in [engine.daily_tick]. "
             "`max_triggers_per_day` is read off a TRIGGER and a triggerless rung has none."]
            if unpaid else []))

    # ─────────────────────────────────────────────────────────────────────────
    # G27 — a banded meter is not also a number.  the-meters.md M7, engine.md §30.
    #
    # The sidebar prints a trait twice, from two places that do not know about each
    # other: the auto Traits dump (every declared core_trait, as a bare number) and
    # whatever [[sidebar_items]] you authored. Measured live: a game rendered
    # "Nothing under it" and `cover 55` stacked on top of each other for all four of
    # its meters, because none of them was declared in [[traits.labels]] at all.
    #
    # Deterministic — no threshold to invent, so unlike the-surfaces R5/R6 this one
    # can be a gate.
    labels = {l.get("key"): l for l in ((game.get("traits") or {}).get("labels") or [])
              if isinstance(l, dict) and l.get("key")}
    doubled = []
    for item in (game.get("sidebar_items") or []):
        if not isinstance(item, dict) or not item.get("bands"):
            continue
        if item.get("trait_owner") == "npc":
            continue                                  # per-NPC cards do not come from the player dump
        k = item.get("trait") or item.get("trait_key")
        if not k:
            continue
        if not (labels.get(k) or {}).get("hidden"):
            doubled.append(
                f"`{k}` is banded as {item.get('type', 'a sidebar item')} but "
                + ("is not declared in [[traits.labels]] at all"
                   if k not in labels else "is declared without hidden = true")
                + " — the band and the raw number both render")
    n_banded = sum(1 for i in (game.get("sidebar_items") or [])
                   if isinstance(i, dict) and i.get("bands") and i.get("trait_owner") != "npc")
    gate("a banded meter is not also a number", None if not n_banded else not doubled,
         f"{len(doubled)} of {n_banded} banded sidebar meters also print as a raw number"
         if n_banded else "no banded sidebar meters — nothing to judge",
         doubled + (["set hidden = true on the same key in [[traits.labels]] (engine.md §30)"]
                    if doubled else []))

    # ─────────────────────────────────────────────────────────────────────────
    # G28 — THE MAP IS A PLACE.  the-map.md R0 + R3.
    #
    # Measured failure, twice: a world that is one house with a token outside,
    # shipped green. The second time it scored 26/26 and was spotted from the
    # LOCATION LIST ALONE, by eye, as "the same mistake we made in back home."
    # Of the five v2 games, the only two whose map starts indoors are those two.
    #
    # The cause was the-map.md's own worked example — the FIRST game's map, with
    # its bugs patched out and its skeleton intact — which three games then
    # copied. An example outranks every rule beside it, so the example is gone
    # and the shape is now a declared choice with this check behind it.
    #
    # TWO tests, because a declaration alone is satisfied by typing a word:
    #   1. did you CHOOSE a shape (declared)
    #   2. is the outside actually the outside (mechanical, off entry_from)
    #
    # Test 2 is the half a parser can see, and it is the exact inversion that
    # shipped: an exterior declared, priced at 25 minutes, hanging off the
    # KITCHEN — so stepping outdoors meant stepping from one interior into a row
    # of shops. It cannot be talked out of in the ledger.
    ARCHETYPES = {"nested_zones", "two_hub", "map_hotspots", "street_mesh", "time_slot"}
    map_fails = []
    if state is None:
        gate("the map is a place", None, "no v2_state.json — nothing declared to check against")
    else:
        arch = bmap.get("archetype")
        if not bmap:
            map_fails.append("board.map not declared at all — the-map.md R0 and R3")
        elif not arch:
            map_fails.append(
                "board.map.archetype is missing — pick one of "
                + " / ".join(sorted(ARCHETYPES))
                + ". Deriving the count from where the cast goes is circular; the shape is the "
                  "input that breaks it (the-map.md R0)")
        elif arch not in ARCHETYPES:
            map_fails.append(f"board.map.archetype = '{arch}' is not one of "
                             + " / ".join(sorted(ARCHETYPES))
                             + " — add a sixth WITH its evidence rather than forcing a fit")
        ext = bmap.get("exterior")
        by_loc = {l.get("id"): l for l in (game.get("locations") or []) if l.get("id")}
        if bmap and arch != "time_slot":
            if not ext:
                map_fails.append("board.map.exterior is missing — a world with no exterior can only "
                                 "recycle its own interior (the-map.md R3)")
            elif ext not in by_loc:
                map_fails.append(f"board.map.exterior = '{ext}' is not a declared location")
            elif by_loc[ext].get("entry_from"):
                parent = by_loc[ext]["entry_from"]
                pname = (by_loc.get(parent) or {}).get("name", parent)
                map_fails.append(
                    f"the exterior '{ext}' HANGS OFF '{parent}' ({pname}) — it is a leaf, not the "
                    f"ground. Stepping outside means stepping from one interior into another. "
                    f"The exterior must be a root, with the home base among the things on it "
                    f"(the-map.md R3)")
    gate("the map is a place", None if state is None else not map_fails,
         (f"{len(map_fails)} map declarations missing or inverted"
          if map_fails else
          f"[{bmap.get('archetype', '—')}] the exterior is the ground everything else sits on"),
         map_fails)

    # ═════════════════════════════════════════════════════════════════════════
    # G29 — a need shuts a door. `the-meters.md` M9.
    #
    # DECLARE-THEN-CHECK against `board.needs[]`. Deterministic, no threshold to
    # invent: either some condition somewhere reads the key or nothing does.
    #
    # ⚠️ THE MEASURED FAILURE. the_allowance declares `[player.trait_decay]
    # hygiene = 10`, ships FOUR ways to wash, and has ZERO conditions reading
    # hygiene. A fully wired loop that costs the player time and buys nothing.
    # It scored 26/27 with that in it. Contrast vesper: 11 things drop hygiene
    # by 30, one restores it, `hygiene >= 40` gates "Take the car" — filthy means
    # she cannot leave.
    #
    # Reads the WHOLE game, not just triggers: a need is just as validly gated
    # from a choice, a [group] band or a quest card.
    # ═════════════════════════════════════════════════════════════════════════
    needs = _declared_needs(state)
    if state is None:
        gate("a need shuts a door", None, "no v2_state.json — nothing declared to check against")
    elif not needs:
        # Ledger present, field missing → FAIL, not n/a. Same convention as G28: a
        # declaration that was never made is a defect, not an absence of evidence.
        # A game with no declared needs has no body — there is no reason to be in
        # any room, which is the defect this gate exists for.
        gate("a need shuts a door", False,
             "no board.needs[] declared — this game has no body",
             ["declare the body's clock in v2_state.json: what falls, where it fills, "
              "what it costs, and WHAT IT SHUTS (references/the-meters.md M8)",
              "a room's list is needs + work + people (the-surfaces.md R2) — with no "
              "declared needs, a third of every room's menu cannot exist",
              "measured: a game whose anchor location is a kitchen shipped with zero "
              "eat / cook / meal / food / sleep canvases because nothing ever asked"])
    else:
        read = _traits_read_by_conditions(game)
        dead = [n for n in needs if str(n.get("key")) not in read]
        gate("a need shuts a door", not dead,
             f"{len(needs) - len(dead)}/{len(needs)} declared needs are read by a condition "
             f"somewhere in the game",
             [f"`{n.get('key')}` is declared a need"
              + (f" that \"{n.get('shuts')}\"" if n.get("shuts") else "")
              + " — but NO condition anywhere in the game reads it. A restore that gates "
                "nothing is a chore, not a need (the-meters.md M9)"
              for n in dead])

    # ═════════════════════════════════════════════════════════════════════════
    # G30 — the walk-in floor. `the-surfaces.md` R3.
    #
    # The join is the author's OWN board: she works alone here, someone is
    # scheduled here, so someone can interrupt her. Nothing is invented.
    #
    # ⚠️ FLOOR IS PER ROOM, NOT PER PAIR — deliberately. The raw cross-product is
    # 40 pairs for the_allowance and 49 for seventh_day; demanding those would
    # rebuild the wall of buttons one layer down, which is the objects mistake in
    # a new coat. One walk-in per qualifying room; the rest is the author's call.
    #
    # Measured before this gate was written: 10 substitution rules across 791
    # canvases in five v2 games, against the incumbent skill sizing the same
    # mechanism at ~47% of its densest arc shape.
    # ═════════════════════════════════════════════════════════════════════════
    qualifying, covered, (solo, sched, subs) = _walkin_join(model, game)
    missing = sorted(set(qualifying) - set(covered))
    gate("the walk-in floor", None if not qualifying else not missing,
         (f"{len(covered)}/{len(qualifying)} rooms where she works alone with someone "
          f"scheduled carry a walk-in"
          if qualifying else
          "no room has both solo work and a scheduled character — nothing to interrupt"),
         [f"{l}: {len(solo[l])} solo activit{'ies' if len(solo[l]) > 1 else 'y'} and "
          f"{len(sched[l])} scheduled character{'s' if len(sched[l]) > 1 else ''} "
          f"({', '.join(sorted(sched[l])[:3])}) — nobody ever walks in"
          for l in missing[:8]]
         + ([f"… and {len(missing)-8} more rooms"] if len(missing) > 8 else [])
         + (["the-surfaces.md R3 — ONE canvas, substitution_only = true, [group] bands on the "
             "axis the odds ride. Vesper's is 2.3 KB; DoL's are 458-473 bytes. Not a scene.",
             "⚠️ the target MUST declare a `location` — getCanvasById indexes only "
             "location-bound canvases (v2.py:3177), so a triggerless rung silently never fires",
             "one per ROOM, not one per pair — filling the cross-product is the wall of "
             "buttons one layer down"]
            if missing else []))

    # ═════════════════════════════════════════════════════════════════════════
    # G33 — A METER IS READ.  `the-meters.md` W3.
    #
    # Every player trait an `effects` entry raises must be read by SOMETHING —
    # a condition, a `costs` entry, or a quest goal. Deterministic: either a
    # reader exists or none does, and there is no threshold to invent.
    #
    # ⚠️ THE MEASURED FAILURE, and it lands on the field's hottest gate.
    #     arousal, across five v2 games:  232 raises  ·  4 reads
    #     seventh_day per-NPC lust 34 · 0   ·   forty_miles energy 28 · 0
    #     steam energy 50 · 0               ·   the_allowance hygiene 4 · 0
    # In the field a sexual-state meter is a real gate in 13 of 27 games, and
    # where it exists it is the #1 or #2 most-gated thing in the whole game
    # (corpo-life `lust`, DoL `arousal`, family-ties `you.arousal`,
    # friends-of-mine `excitement`). We raise it everywhere and read it nowhere.
    #
    # CAUSE, one line of this skill's own template: the volatile layer in
    # `templates/board.toml` was labelled "NEVER gate an arc on these" — correct
    # about the ODOMETER and silent about the THROTTLE, so five authors read it
    # as "never gate on it at all". The missing positive half is now W2: a
    # throttle gates the REPEATABLE act surface, and only that.
    #
    # ⚠️ CARVE-OUT. `<npc>_stage` is exempt when the prefix names a declared
    # character — the ENGINE reads those (v2.py:5549-5554). Written in advance
    # rather than after a bug report, because a gate that fails a game for
    # obeying the engine is a bug in the gate.
    # ═════════════════════════════════════════════════════════════════════════
    raises = _player_trait_raises(game)
    read_by = _traits_read_anywhere(game)
    exempt = _engine_read_stage_traits(game)
    dead = sorted(t for t in raises if t not in exempt and not read_by.get(t))
    core = ((game.get("player") or {}).get("core_traits") or {})
    inert = sorted(t for t in core
                   if t not in raises and t not in exempt and not read_by.get(t))
    detail = []
    for t in dead:
        where = collections.Counter(raises[t])
        top = " · ".join(f"{c}" for c, _ in where.most_common(3))
        detail.append(f"`{t}` is raised {len(raises[t])} time(s) across {len(where)} canvas(es) "
                      f"({top}{' …' if len(where) > 3 else ''}) and NO condition, cost or quest "
                      f"goal anywhere in the game reads it — that is not a meter, it is a number "
                      f"the player watches move (the-meters.md W3)")
    if inert:
        detail.append(f"declared but never touched at all: {', '.join(inert[:10])}"
                      + (" …" if len(inert) > 10 else ""))
    gate("a meter is read", None if not raises else not dead,
         f"{len(raises) - len(dead)}/{len(raises)} raised player meters are read by a condition, "
         f"a cost or a quest goal"
         + (f" · {len(exempt & set(raises))} `_stage` key(s) exempt (the engine reads those)"
            if (exempt & set(raises)) else ""),
         detail)

    # ═════════════════════════════════════════════════════════════════════════
    # G41 — THE WARDROBE IS READ.  `the-meters.md` W3, extended to the wardrobe.
    #
    # W3's law is "a number nothing reads is not a meter", and the gate above
    # enforces it for player traits an `effects` entry RAISES. It is structurally
    # blind to clothing: `worn_beauty` / `worn_corruption` are DERIVED from a
    # garment's own `beauty` / `corruption` declaration (template_import.py:218-219,
    # a MAX aggregate — engine.md §17), never raised by an effect, so a game can
    # ship a full catalog and the meter gate sees nothing at all.
    #
    # MEASURED across the 21 games carrying a merged final, 2026-08-24:
    #     102 garments in 10 games  ·  47 reads between them
    #     mothers_place 6 garments / 0 reads      seventh_day   8 / 0
    #     steam         8 garments / 0 reads      the_allowance 9 / 0
    # The field reads its wardrobe an order of magnitude harder: degrees-of-lewdity
    # reads its derived exposure ~900 times, the-hellfire-club its slot variables
    # 484, zaras-school-life `$PlayerClothes` 415. Our best is vesper at 21.
    #
    # ⚠️ THREE READER FAMILIES. Counting only the first is how this gate would fail
    #    a game for doing the most common thing in the field:
    #      · a condition predicate — worn_corruption / worn_beauty / worn_type /
    #        clothing_slot / clothing_item                        (engine.md §17)
    #      · a player_portrait outfit override — when = { worn_type = … } or
    #        { corruption = … }                          (template_import.py:744)
    #      · a location dress code — clothing_rules.slots_required
    #                                              (template_import.py:4227-4241)
    #    The portrait override is a DISPLAY reaction rather than a gate, and W7 is
    #    what says that is the field's dominant mode — DoL swaps the model's mouth
    #    on `V.exposed === 2`. vesper reads its wardrobe 19 times through
    #    `clothing_item` and twice through a portrait override; a first-family-only
    #    check would have failed the best reader we have.
    #
    # ⚠️ THE SAME FIG LEAF AS THE GATE ABOVE — one throwaway `worn_corruption gte 1`
    #    turns this green. No threshold is invented, because W7 measures the field's
    #    median gate share at 10% and demanding gates would be wrong. Instead the
    #    summary prints garments-against-reads, so a thin pass is visible on the
    #    report the way the meter-ladder lint makes a one-rung ladder visible.
    # ═════════════════════════════════════════════════════════════════════════
    _CLOTHING_PREDICATES = ("worn_corruption", "worn_beauty", "worn_type",
                            "clothing_slot", "clothing_item")
    garments = [c for c in (game.get("clothing") or []) if isinstance(c, dict)]
    wardrobe_reads = collections.Counter()
    for path, node in _walk_paths(game):
        ps = "|".join(path)
        if node.get("type") in _CLOTHING_PREDICATES:
            wardrobe_reads[str(node["type"])] += 1
        elif ps.endswith("player_portrait|outfits|[]"):
            when = node.get("when")
            if isinstance(when, dict):
                for k in ("worn_type", "corruption"):
                    if k in when:
                        wardrobe_reads["player_portrait when=" + k] += 1
        elif ps.endswith("locations|[]") and isinstance(node.get("clothing_rules"), list):
            wardrobe_reads["clothing_rules"] += len(node["clothing_rules"])
    _reads = sum(wardrobe_reads.values())
    detail = []
    if garments and not _reads:
        _slots = collections.Counter(str(c.get("slot") or "?") for c in garments)
        _names = ", ".join(f"`{c.get('id') or c.get('name') or '?'}`" for c in garments[:8])
        detail.append(f"{len(garments)} garment(s) across {len(_slots)} slot(s) "
                      f"({' · '.join(f'{k} x{v}' for k, v in _slots.most_common())}) "
                      f"and NOTHING reads the wardrobe — no worn_corruption / worn_beauty / "
                      f"worn_type / clothing_slot / clothing_item condition, no player_portrait "
                      f"outfit override, no location clothing_rules")
        detail.append(f"the catalog: {_names}" + (" …" if len(garments) > 8 else ""))
        detail.append("the player can dress and the world does not look. Either read it or cut it "
                      "(the-meters.md W3, W7)")
    gate("the wardrobe is read", None if not garments else bool(_reads),
         (f"{len(garments)} garment(s) · {_reads} read(s)"
          + (" · " + " · ".join(f"{k} x{v}" for k, v in wardrobe_reads.most_common(4))
             if wardrobe_reads else "")
          + (f" · field: DoL ~900, the-hellfire-club 484, zaras-school-life 415"
             if garments and _reads and _reads < 50 else ""))
         if garments else "no [[clothing]] catalog declared",
         detail)

    # ═════════════════════════════════════════════════════════════════════════
    # G42 — A LOCKED DOOR SAYS WHY.  `the-surfaces.md` R5c, `engine.md` §15.
    #
    # A choice with `show_when_locked = true` and no reason beside it renders the
    # ACTION LABEL, greyed, with nothing else — `escaped_locked = (locked_text or
    # choice_text)` at v2.py:13171, repeated into the title tooltip at :13219-13220.
    # The player sees "Kiss her" struck out and learns nothing.
    #
    # MEASURED, 26 shipped sandboxes, 2026-08-24 (findings_B_refusal.md):
    #   27,505 conditionals wrap an action; only 23% refuse anything (35% are
    #   variant selectors where every branch acts). Of the 16,167 that DO refuse:
    #       71% render nothing at all      the option is simply not there
    #       28% speak                      median 9 words, 60% naming a handle
    #   A visible, MUTE action label is 2.26% of 4,513 spoken refusals, and nearly
    #   all of that is settings and pagination chrome (OptionsWidget, Widgets
    #   Outfits "Previous"/"Next") rather than gated content. The field hides a
    #   refusal or it explains one. It does not show a dead label and stop.
    #   Ours, same day, by tomllib over every merged final: 144 of 176 shown-locked
    #   choices are mute — 82%, against the field's 2.26%.
    #
    # ⚠️ THIS GATE REVERSES WHAT THIS SKILL USED TO TEACH. engine.md §15 read
    #    "Prefer the want unless the gate is genuinely obscure" until 2026-08-24,
    #    so the 7% is doctrine, not sloppiness. §15 was rewritten in the same turn
    #    this gate landed; the two must not be allowed to drift apart again.
    #
    # ⚠️ THREE THINGS COUNT AS A REASON, and the third is why late_shifts passes:
    #      · locked_text            the reason replaces the label   (engine.md §15)
    #      · locked_text_threshold  the label becomes a <<button>> that fires
    #        setup.queueGatedNotification(...) on click (v2.py:13210-13217) — the
    #        field's click-then-refused shape minus the passage, so it counts
    #      · rejection_node         a live link to a real failure node (§36)
    #    A `costs` entry needs NO authoring at all: the exit-block cost rung appends
    #    setup.getCostBlockedMessage(...) by itself (v2.py:13159-13166), which is
    #    the field's dominant `priced` refusal for free. A cost-only choice is never
    #    counted against the game.
    #
    # NO INVENTED THRESHOLD. The check is categorical because the measurement is:
    # the field's mute share is ~2% and it is UI chrome. The summary prints
    # shown-locked against reasons given so a thin pass stays visible.
    # ═════════════════════════════════════════════════════════════════════════
    shown_locked, mute = [], []
    for path, node in _walk_paths(game):
        if not path or path[-1] != "[]" or "choices" not in path:
            continue
        if "text" not in node and "target" not in node:
            continue
        if not node.get("show_when_locked"):
            continue
        label = str(node.get("text") or node.get("target") or "?")
        shown_locked.append(label)
        has_reason = (
            str(node.get("locked_text") or "").strip()
            or str(node.get("locked_text_threshold") or "").strip()
            or node.get("rejection_node")
        )
        if has_reason:
            continue
        # A choice gated ONLY by costs explains itself — the engine writes the
        # message. Anything else is a condition, and a condition goes mute.
        if not node.get("conditions") and node.get("costs"):
            continue
        mute.append(label)
    detail = []
    if mute:
        _shown = ", ".join(f'"{m[:52]}"' for m in mute[:8])
        detail.append(f"{len(mute)} of {len(shown_locked)} shown-locked choice(s) render the "
                      f"action label greyed with no reason beside it — v2.py:13171 falls back "
                      f"to the label when `locked_text` is absent")
        detail.append(f"mute: {_shown}" + (" …" if len(mute) > 8 else ""))
        detail.append("give each one a `locked_text` (the reason), a `locked_text_threshold` "
                      "(the bar, on click), or a `rejection_node` (a real failure node). "
                      "The field hides a refusal or explains it — 2.26% show a dead label "
                      "(the-surfaces.md R5c, engine.md §15/§36)")
    gate("a locked door says why",
         None if not shown_locked else not mute,
         (f"{len(shown_locked)} shown-locked · {len(shown_locked) - len(mute)} with a reason"
          + (f" · {100 * len(mute) // len(shown_locked)}% mute (field 2%)" if mute else "")
          ) if shown_locked else "no `show_when_locked` choices authored",
         detail)

    # ═════════════════════════════════════════════════════════════════════════
    # G34 — THE CLIMB IS WHERE YOU SAID IT IS.  `the-meters.md` W1.
    #
    # DECLARE-THEN-CHECK against `board.who_climbs`. The field does NOT converge
    # on one answer — it splits, cleanly, into two schools with nothing between
    # them (share of character-meter gating carried by per-character meters):
    #
    #   ROSTER  zaras 100% · adam-and-gaia 100% · taxi 91% · become-someone 84%
    #           hellfire 80% · patriarch 79% · love-and-vice 73% · fam-bus 65%
    #   -------------------------------------------------------------------  (8)
    #   LADDER  new-lust 15% · friends 13% · corpo-life 12% · destroyer 12%
    #           DoL 10% · wasteland 5% · family-ties 0% · company 0% · slut 0%
    #                                                                       (9)
    #
    # Ours: 20% · 22% · 19% · 29% · 28%. All five inside a band no shipped game
    # occupies — not because the middle was chosen, but because the question was
    # never asked. v1 asks it (`content-framework.md`, "Who climbs?"); v2 dropped
    # it, and one template answered it five times by default.
    #
    # The cut points sit INSIDE the measured empty band (15%-65%), so they are
    # read off the distribution rather than invented. What is judged is the game
    # against its own declaration, never against a number this file picked.
    # ═════════════════════════════════════════════════════════════════════════
    board = (state or {}).get("board") or {}
    who = board.get("who_climbs")
    p_gates, n_gates = _school_split(game, state)
    p_tot, n_tot = sum(p_gates.values()), sum(n_gates.values())
    tot = p_tot + n_tot
    cast_pct = 100 * n_tot / tot if tot else 0
    shape = (f"{p_tot} gate site(s) on declared tiers, {n_tot} on per-character meters "
             f"— {cast_pct:.0f}% of the climb sits on the cast")
    if state is None:
        gate("the climb is where you said it is", None,
             "no v2_state.json — nothing declared to check against")
    elif not who:
        gate("the climb is where you said it is", None,
             f"board.who_climbs not declared — {shape}",
             ["declare it: \"player\" (one or two meters on her run everything), \"cast\" "
              "(the meters live on each character), or \"both\" — references/the-meters.md W1",
              "measured: the field splits 9 ladder / 8 roster with NOTHING between 15% and 65%, "
              "and all five v2 games sit at 19-29% without having chosen",
              "this reports n/a, which is NOT a pass — an absence is not evidence"])
    elif not tot:
        gate("the climb is where you said it is", None,
             "no meter gates anywhere in the game — nothing to place")
    else:
        want = {"player": ("at least 60% on her own tiers", cast_pct <= 40),
                "cast":   ("at least 60% on the cast",      cast_pct >= 60),
                "both":   ("at least 25% on each side",     25 <= cast_pct <= 75)}
        label, ok = want.get(str(who), (f"unknown who_climbs value {who!r}", False))
        gate("the climb is where you said it is", ok,
             f"declared `{who}` — {shape} (wants {label})",
             [] if ok else
             [f"the board says `{who}` and the game does not do it: {shape}",
              "either move the gating to where the declaration says it lives, or change the "
              "declaration — but do not leave it in the middle, which is where every v2 game "
              "so far has landed by default (the-meters.md W1)"])
    # G19 — sentence length. The first gate here that measures WRITING.
    sent_words = [len(s.split())
                  for c in model for b in c["beats"]
                  for s in re.split(r"(?<=[.!?])\s+", " ".join(b.text))
                  if 2 <= len(s.split()) <= 120]
    med_sent = _median(sent_words)
    # G23 — every speaking block names its speaker.
    #
    # ⚠️ THE LARGEST DEFECT EVER FOUND IN A v2 GAME, AND NOTHING WATCHED FOR IT. A shipped,
    # portal-listed build rendered "💭 Npc is thinking:" on 147 passages — every thought bubble
    # in the game — because `props.speaker` was omitted and the engine defaults the field to the
    # literal string "npc" (v2.py:14631), which then title-cases to "Npc" (v2.py:14657).
    # Measured afterwards across every v2 game: 147, 145 and 79 blocks missing it. Three for
    # three, because the v2 skill mentions `thought_bubble` once and never shows its shape.
    #
    # A GATE, not a lint: unlike a dialog speaker's IDENTITY — which needs a reader — the
    # PRESENCE of the field is pure consistency, always reachable, and there is no case where
    # omitting it is correct. The existing dialogue-attribution lint is a different question
    # (it asks whether the right name will render); this asks whether any name will.
    def _speaking_blocks(blocks, out):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") in ("dialog", "thought_bubble"):
                out.append(b)
            props = b.get("props") or {}
            for beat in (props.get("beats") or []):
                _speaking_blocks(beat.get("blocks"), out)
            _speaking_blocks(props.get("blocks") or b.get("blocks"), out)

    voiceless = collections.Counter()
    n_speaking = 0
    for c in (game.get("canvases") or []):
        for n in (c.get("nodes") or []):
            found = []
            _speaking_blocks(n.get("blocks"), found)
            for b in found:
                n_speaking += 1
                if not (b.get("props") or {}).get("speaker"):
                    voiceless[f"{c.get('id')}#{b.get('type')}"] += 1
    n_bad = sum(voiceless.values())
    gate("speakers are named", None if not n_speaking else not n_bad,
         f"{n_speaking - n_bad}/{n_speaking} dialog and thought_bubble blocks name their speaker"
         if n_speaking else "no dialog or thought_bubble blocks authored",
         [f"{k}: {v} block{'s' if v > 1 else ''} with no props.speaker"
          for k, v in voiceless.most_common(10)]
         + ([f"a missing speaker renders as the literal '{'Npc'}' (v2.py:14631, :14657) — it is "
             f"never a default, it is a bug",
             "props = { speaker = \"player\" } · { speaker = \"npc\", npcId = \"npc_x\" } · "
             "{ speaker = \"unknown\" } for a stranger (renders \"Someone\"), v2.py:14640"]
            if n_bad else []))

    # Ceiling gate — reports its MARGIN, for the reason in G20's header. A game sitting on
    # the ceiling and a game well under it must not print the same line.
    margin = SENTENCE_CEILING - med_sent
    gate("sentence length", None if not sent_words else med_sent <= SENTENCE_CEILING,
         f"median sentence {med_sent} words across {len(sent_words):,} sentences "
         f"(ceiling {SENTENCE_CEILING}, margin {margin:+d}) · field median 10",
         ([] if med_sent <= SENTENCE_CEILING else
          ["field median is 10 words; the reference game is 9",
           "escalate by adding beats, not by lengthening sentences"])
         + ([f"⚠️ sitting ON the ceiling. {SENTENCE_CEILING} is a backstop calibrated across "
             f"two extraction bases, not a target — the field runs 10 and the reference game 9."]
            if sent_words and margin <= 0 else []))

    # ─────────────────────────────────────────────────────────────────────────
    # THE FIRST HOUR — references/the-first-hour.md
    # Three gates added 2026-08-22, after the first v2 game a human read end to end
    # scored 31/32 and was unreadable for its first ten minutes. Nothing in the
    # existing 32 looked at the opening, the introductions, or the first visit.
    # ─────────────────────────────────────────────────────────────────────────

    # G33 — the opening hands over into an open door (the-first-hour.md F3)
    # A funnel that ends at a clock time when nothing at the landing location is open
    # makes the player's first free act pressing a wait button. v1 named this the
    # dead-window bug and v2 shipped it into the one place it costs most.
    hands, hand_why = _fh_handovers(game)
    if not hands:
        gate("the opening opens a door", None,
             f"the funnel could not be walked — {hand_why}",
             ["an unresolvable walk is an instrument failure, not a defect; "
              "the gate judges nothing here"])
    else:
        rows, any_open = [], False
        for minute, loc in sorted(set(hands)):
            live = _fh_live_at(game, loc, minute)
            any_open = any_open or bool(live)
            clock = f"{(minute // 60) % 24:02d}:{minute % 60:02d}"
            rows.append(f"hands over {clock} at {loc}: "
                        + (f"{len(live)} open — {', '.join(live[:4])}" if live
                           else "NOTHING open"))
        detail = rows
        if not any_open:
            first_min, first_loc = sorted(set(hands))[0]
            shut = []
            for c in (game.get("canvases") or []):
                t = c.get("trigger") or {}
                if t.get("location") != first_loc:
                    continue
                if t.get("substitution_only"):
                    shut.append(f"{c.get('id')}: substitution_only — never renders alone")
                elif t.get("trigger_mode") == "random":
                    shut.append(f"{c.get('id')}: trigger_mode = random — not guaranteed")
                elif t.get("schedules"):
                    w = ", ".join(f"{s.get('start_time')}-{s.get('end_time')}"
                                  for s in t["schedules"] if isinstance(s, dict))
                    shut.append(f"{c.get('id')}: schedule {w} — closed at "
                                f"{(first_min // 60) % 24:02d}:{first_min % 60:02d}")
            detail = rows + shut[:8] + [
                "move the handover, widen the window, or hand over somewhere else — "
                "a random ambient is not a door and neither is a walk-in"]
        gate("the opening opens a door", any_open,
             (f"{len(set(hands))} handover(s) · "
              + ("at least one lands on something open" if any_open
                 else "every handover lands on a closed room")),
             detail)

    # G34 — every hub is met first (the-first-hour.md F5 + F8)
    # The forbidden shape is a repeatable `npc=` hub whose base node IS the introduction.
    # All six v2 games shipped it for their whole cast; two v1 games are already at 100%,
    # so the bar is one shipped work has cleared rather than an invented number.
    met, cast, flag_owners, cold = _fh_cast_met(game)
    shared = {f: sorted(o) for f, o in flag_owners.items() if len(o) > 1}
    if not cast:
        gate("every hub is met first", None, "no portrait hubs authored")
    else:
        det = [f"{npc}: hub(s) {', '.join(cids)} carry no condition at all — "
               f"the portrait is live on turn one"
               for npc, cids in cold[:8]]
        det += [f"{npc}: gated, but on no flag a meeting with {npc} sets"
                for npc in cast
                if npc not in met and npc not in {n for n, _c in cold}][:6]
        det += [f"`{f}` opens hubs for {len(o)} characters ({', '.join(o)}) — "
                f"one flag per character" for f, o in sorted(shared.items())]
        if len(met) < len(cast):
            det.append("a meeting is a NON-repeatable canvas that names that character "
                       "and sets one flag the hub reads — the_inheritance/canvas_meet_audrey, "
                       "125 words and 4 dialog blocks, is the worked shape")
        gate("every hub is met first", len(met) == len(cast),
             f"{len(met)}/{len(cast)} characters are introduced before their hub opens",
             det)

    # G38 — a meeting fires where they are (the-first-hour.md F5).
    # The other half of G34. G34 asks whether a character is INTRODUCED before their
    # hub opens; this asks whether that introduction can only play in a room the
    # character is standing in.
    #
    # ⚠️ `requires_npc` DOES NOT DO THIS, and believing it does is the whole defect.
    #    Traced: selectAutoFireCanvasForLocation -> isCanvasValid (v2.py:4559) reads
    #    schedules, conditions and repeatability and NEVER reads requiresNpc.
    #    Repo-wide the field is consumed in exactly two functions —
    #    checkRandomEncounters (v2.py:5245, trigger_mode="random") and
    #    checkAndSubstituteCanvas (v2.py:5318, substitution_only) — which is why
    #    those two shapes are excluded below rather than judged.
    #
    # The failure this was written from: a game shipped five meetings with no window
    # and its introductions played to empty rooms — one at 06:10 on a Saturday with
    # the character out working, its prose saying "it's Monday". The skill had taught
    # the rule and shipped a worked template twelve hours before that game was
    # written; what it did not have was a check, and template_import.py's own comment
    # on the field said the opposite (corrected in the same change as this gate).
    #
    # SCOPED SO IT ONLY CONVICTS WHERE A WINDOW WAS AUTHORABLE. A canvas whose NPC
    # declares no rows at that location has nothing to copy, and saying so would be a
    # different, weaker finding wearing this one's clothes.
    #
    # Measured across every game in the repo the day it was written — 69 canvases in
    # scope, and ZERO carry a window that misses their character's own hours, so this
    # never nags a game that did the work:
    #   last_call 11/11 clean · off_season 8/8 · the_long_summer_test 1/1
    #   the_season 0/5 · the_inheritance 0/24 · vesper 0/13 · late_shifts 6/7
    npc_rows = collections.defaultdict(list)
    for _n in (game.get("npcs") or []):
        for _r in (_n.get("schedules") or []):
            _loc = _r.get("location") or _r.get("location_id")
            if _loc:
                npc_rows[(_n.get("id"), _loc)].append(_r)

    windowless, in_scope = [], 0
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        # the three shapes that DO gate on requiresNpc, and a repeatable hub, which
        # is G34's business and not this gate's
        if t.get("is_repeatable") or t.get("substitution_only"):
            continue
        if t.get("trigger_mode") == "random" or _is_dev(c):
            continue
        who = t.get("requires_npc")
        if not who:
            continue
        in_scope += 1
        if t.get("schedules"):
            continue
        theirs = npc_rows.get((who, t.get("location")))
        if not theirs:
            continue          # nothing to copy — not this gate's finding
        hours = " · ".join(f"{r.get('start_time')}-{r.get('end_time')}" for r in theirs[:3])
        windowless.append(f"{c.get('id')} @{t.get('location')}: no trigger.schedules, but "
                          f"{who} is only there {hours} — `requires_npc` alone does not "
                          f"gate this path (v2.py:4559)")
    gate("a meeting fires where they are",
         None if not in_scope else not windowless,
         f"{in_scope - len(windowless)}/{in_scope} one-shot canvases naming a character "
         f"can only fire in that character's own hours",
         windowless)

    # G35 — the anchor introduces itself (the-first-hour.md F9)
    # ⚠️ AN EXISTENCE CHECK, which SKILL.md warns is the weakest kind — it asks whether a
    # thing is there, not how much of it or what it cost. It is defensible here only
    # because the real question genuinely IS existence: the game that prompted this gave
    # first-visit canvases to five rooms and none to the anchor it had declared at 27% of
    # the whole word budget. The per-location coverage prints below so the distribution
    # stays visible and this does not quietly become a box to tick.
    anchor_id, anchor_src = _fh_declared_anchor(game, state)
    visits = _fh_first_visits(game)
    all_locs = [l.get("id") for l in (game.get("locations") or []) if l.get("id")]
    covered = [l for l in all_locs if visits.get(l)]
    if not anchor_id:
        gate("the anchor introduces itself", None,
             "no v2_state.json fill budget — the declared anchor is unknown",
             [f"{len(covered)}/{len(all_locs)} locations carry a first visit"]
             if all_locs else None)
    else:
        ok = bool(visits.get(anchor_id))
        det = []
        if not ok:
            det.append("the room the ledger budgeted largest is the one room nothing "
                       "introduces")
            det.append("a non-repeatable canvas bound to the location auto-fires once "
                       "(v2.py:4453) — no new primitive is needed")
        bare = sorted(set(all_locs) - set(covered))
        if bare:
            det.append(f"no first visit: {', '.join(bare[:8])}"
                       + (f" … and {len(bare) - 8} more" if len(bare) > 8 else ""))
        gate("the anchor introduces itself", ok,
             f"[{anchor_src}] anchor {anchor_id} "
             + (f"opens with {', '.join(visits[anchor_id][:3])}" if ok
                else "has no first-visit canvas")
             + f" · {len(covered)}/{len(all_locs)} locations carry one",
             det)

    # G36 — the label keeps its time (the-clock.md C3 + C4)
    # A label is a promise about what the click DOES. Two ways to break it:
    #
    #   1. naming a clock time. The engine has no absolute-time advance at all —
    #      grep -E 'target_hour|advance_to|until_time|time_target' v2.py -> 0 hits, and
    #      advanceTime(minutes) (v2.py:5400) is the whole API. "Work the counter till one
    #      (2h 30m)." on an 08:00–13:00 canvas lands at 10:30 from an 08:00 entry and at
    #      15:25 from a 12:55 one: right for ONE minute of a five-hour window.
    #   2. stating a duration that is not the real spend. Walked choice -> target node ->
    #      that node's exit, because the tag sits where the player decides and the charge
    #      sits where they leave.
    #
    # Field basis: of 92,226 link labels across 25 shipped sandboxes, TWO name a clock
    # time and both are explicit waits ("Wait until 21:00") — zero promise an hour as the
    # outcome of an action. Even lust-for-life, which HAS an absolute-time primitive and
    # calls it 270 times, labels those buttons "Back home" / "Leave" / "Go to the SPA".
    # All four v1 games here already pass, so this is a bar shipped work has cleared.
    _idx = _clk_node_index(game)
    lab_n, clk_bad, dur_n, dur_bad = 0, [], 0, []
    for _c, _ch, _t in _clk_choices(model):
        lab_n += 1
        _refs = _clk_refs(_t)
        if _refs:
            _shown = sorted({r.strip(" .,;:!?") for r in _refs})[:2]
            clk_bad.append(f'{_c["id"]}: "{_t[:54]}" — the engine cannot reach a clock '
                           f'time ({", ".join(_shown)})')
        _said = _clk_stated_minutes(_t)
        if _said is None:
            continue
        dur_n += 1
        _spent = _clk_spent_minutes(_idx, _c["id"], _ch)
        if _spent is not None and _spent != _said:
            dur_bad.append(f'{_c["id"]}: "{_t[:44]}" promises {_hms(_said)}, '
                           f"spends {_hms(_spent)}")
    if not lab_n:
        gate("the label keeps its time", None, "no choice labels authored")
    else:
        _det = clk_bad[:10] + dur_bad[:6]
        if clk_bad:
            _det.append("state the DURATION instead — \"Work the counter (2h 30m).\" is "
                        "true at every entry minute; the hour is not")
        gate("the label keeps its time", not (clk_bad or dur_bad),
             (f"{len(clk_bad)} label(s) name a clock time"
              + (f" · {len(dur_bad)} of {dur_n} stated durations do not match the spend"
                 if dur_bad else
                 (f" · {dur_n} stated duration(s) all match the spend" if dur_n else
                  " · no label states a duration"))),
             _det)


    return R


def _words_declared_names(path):
    """The names the fiction teaches, read off `v2_state.json` beside the file.

    Without this the cast tops its own report: a Want naming six people put five of
    them in the first six rows and pushed the one real finding off the printed tail.
    The ledger already declares them, so nothing here is guessed — same declare-then-
    check shape the gates use everywhere else.

    Returns `(names, ledger_path_or_None)`.
    """
    d = os.path.dirname(os.path.abspath(path))
    for _ in range(3):                       # the file may sit in games/<slug>/ or below
        cand = os.path.join(d, "v2_state.json")
        if os.path.exists(cand):
            break
        parent = os.path.dirname(d)
        if parent == d:
            return [], None
        d = parent
    else:
        return [], None

    try:
        with open(cand) as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        return [], None

    names, board = [], state.get("board") or {}
    # The protagonist. She is not in board.characters[] — she is the player — so
    # without this her own name tops her own report on every single run.
    names += [state.get("protagonist"), board.get("protagonist")]
    names += list((state.get("want") or {}).get("why_this_person") or {})
    names += list((state.get("want") or {}).get("crude_ceiling") or {})
    for key in ("characters", "locations"):
        for entry in board.get(key) or []:
            if isinstance(entry, dict):
                names += [entry.get("id"), entry.get("name")]
    names += list((board.get("map") or {}).get("homes") or {})
    # `npc_boyd` -> the tokeniser sees `npc` and `boyd`; both are then names the
    # fiction teaches, which is correct — neither is a word the player arrived with.
    return [n for n in names if n], cand


def words_mode(path):
    """The vocabulary lint on a plain text file — the WANT and BOARD phases.

    The game-phase lint runs on a BUILT game, which is one phase too late: by then
    every noun is already set into a room name, a button label and the prose behind
    it, and changing one means renaming things. This runs on the document where the
    nouns are being CHOSEN.

    Always exits 0. `references/register.md` is explicit that this is a list and never
    a score, so it must not be able to fail a build or block a phase.
    """
    try:
        with open(path) as fh:
            text = fh.read()
    except OSError as exc:
        print(f"cannot read {path}: {exc}")
        return 2

    names, ledger = _words_declared_names(path)
    summary, findings = own_words_report(text, names, suppress=_SKILL_META, shown=None)
    print(f"the words the player has to already own — {path}")
    if ledger:
        print(f"  names the fiction teaches, from {ledger}: {len(names)} declared")
    else:
        print("  no v2_state.json alongside — the cast's own names will appear in the "
              "list below (they are not defects)")
    print(f"  {summary}" if summary else
          "  genre_words.txt is missing — nothing measured (an absence is not a pass)")
    for f in findings:
        print(f"    · {f}")
    if findings:
        print("\n  Read the list, not the number. A word here is not automatically wrong —")
        print("  the question is whether a player arrives already holding it.")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "--words":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --words <path/to/file>")
            sys.exit(2)
        sys.exit(words_mode(sys.argv[2]))
    arg = sys.argv[1]
    path = arg if arg.endswith(".toml") else f"games/{arg}/toml_phases/7_final_game.toml"
    if not os.path.exists(path):
        print(f"not found: {path}")
        sys.exit(2)

    model, game = build(_load(path))
    # The ledger, when it exists, tells the gates what the author DECLARED.
    state_path = os.path.join(os.path.dirname(os.path.dirname(path)), 'v2_state.json')
    state = json.load(open(state_path)) if os.path.exists(state_path) else None
    results = run_gates(model, game, state)

    lints = lint_dialogue_attribution(model)
    world_lints = lint_world_prose(model, game)
    shape_summary, shape_lints = lint_screen_shape(model, game)
    label_summary, label_lints = lint_labels(model, game)
    browse_summary, browse_lints = lint_browse_share(model, game)
    disp_summary, disp_lints = lint_dispatch_depth(game)
    ladder_summary, ladder_lints = lint_ladder(model, game)
    talk_summary, talk_lints = lint_talk_screens(model, game)
    loop_summary, loop_lints = lint_loop_shape(model, game)
    act_summary, act_lints = lint_act_nodes(model, game)
    rung_summary, rung_lints = lint_meter_ladder(game, state)
    cast_summary, cast_lints = lint_cast_meters(game, state)
    cw_summary, cw_lints = lint_counterweight(game, state)
    words_summary, words_lints = lint_own_words(model, game)
    fh_summary, fh_lints = lint_named_before_met(model, game)
    clock_summary, clock_lints = lint_clock_in_prose(model, game)
    tcost_summary, tcost_lints = lint_time_cost_on_button(model, game)
    cur_summary, cur_lints = lint_currency_in_prose(model, game, state)
    price_summary, price_lints = lint_price_spelled_out(model, game, state)

    if "--json" in sys.argv:
        print(json.dumps({"gates": [dict(r) for r in results],
                          "lints": {"dialogue_attribution": lints,
                                    "world_prose": world_lints,
                                    "screen_shape": {"summary": shape_summary,
                                                     "findings": shape_lints},
                                    "labels": {"summary": label_summary,
                                               "findings": label_lints},
                                    "browse_share": {"summary": browse_summary,
                                                     "findings": browse_lints},
                                    "dispatch_depth": {"summary": disp_summary,
                                                       "findings": disp_lints},
                                    "ladder": {"summary": ladder_summary,
                                               "findings": ladder_lints},
                                    "talk_screens": {"summary": talk_summary,
                                                     "findings": talk_lints},
                                    "loop_shape": {"summary": loop_summary,
                                                   "findings": loop_lints},
                                    "act_nodes": {"summary": act_summary,
                                                  "findings": act_lints},
                                    "meter_ladder": {"summary": rung_summary,
                                                     "findings": rung_lints},
                                    "cast_meters": {"summary": cast_summary,
                                                    "findings": cast_lints},
                                    "counterweight": {"summary": cw_summary,
                                                      "findings": cw_lints},
                                    "own_words": {"summary": words_summary,
                                                  "findings": words_lints},
                                    "named_before_met": {"summary": fh_summary,
                                                         "findings": fh_lints},
                                    "clock_in_prose": {"summary": clock_summary,
                                                       "findings": clock_lints},
                                    "time_cost_on_button": {"summary": tcost_summary,
                                                            "findings": tcost_lints},
                                    "currency_in_prose": {"summary": cur_summary,
                                                          "findings": cur_lints},
                                    "price_spelled_out": {"summary": price_summary,
                                                          "findings": price_lints}}},
                         indent=1, default=str))
        return

    name = (game.get("project") or {}).get("name") or os.path.basename(path)
    npass = sum(1 for r in results if r["pass_"])
    nna   = sum(1 for r in results if r.get("na"))
    judged = len(results) - nna
    print(f"\n  author-game-v2 gates — {name}")
    print(f"  {path}")
    print(f"  {'─'*72}")
    for r in results:
        tag = "n/a " if r.get("na") else ("PASS" if r["pass_"] else "FAIL")
        print(f"  [{tag}]  {r['gate']:32s} {r['headline']}")
        for d in r["detail"][:12]:
            print(f"          · {d}")
        if len(r["detail"]) > 12:
            print(f"          · … and {len(r['detail'])-12} more")
    print(f"  {'─'*72}")
    na_note = f"  ({nna} n/a — nothing authored yet to judge)" if nna else ""
    print(f"  {npass}/{judged} judged gates pass{na_note}")

    # Lints sit BELOW the tally and never touch it. A warning that can change a
    # score is a gate, and a gate has to be re-derivable from a measurement.
    if lints:
        print(f"  {'─'*72}")
        print(f"  lint · dialogue attribution — {len(lints)} to eyeball")
        for h in lints[:12]:
            print(f"          · {h['canvas']}#{h['node']} speaks as {h['npc']}: {h['line']}…")
        if len(lints) > 12:
            print(f"          · … and {len(lints)-12} more")
        print("          (a canvas that neither binds nor names the speaker — check the"
              " name that will render)")

    if label_summary:
        print(f"  {'─'*72}")
        print(f"  lint · room-list labels — {label_summary}")
        for h in label_lints[:8]:
            print(f"          · {h}")
        if label_lints:
            print("          (the-voice.md R1 — a NUMBER, not a bar. last_call, late_shifts and"
                  " the_allowance sit at 0% noun-only, so it is reachable; any threshold in the"
                  " 38%..84% gap would be invented. The register lives in the paragraph the click"
                  " produces, never in the button)")

    if browse_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the browse share — {browse_summary}")
        for h in browse_lints[:8]:
            print(f"          · {h}")
        if browse_lints:
            print("          (a room's list is needs + work + people, the-surfaces.md R2."
                  " KNOWN NOISY: a travel bridge legitimately changes nothing, so read WHICH"
                  " canvases are named, not the percentage alone)")

    if disp_summary:
        print(f"  {'─'*72}")
        print(f"  lint · dispatch depth — {disp_summary}")
        for h in disp_lints[:8]:
            print(f"          · {h}")
        print("          (the-surfaces.md R3 — one activity DEEPENS, the room does not widen."
              " The walk-in floor gate only asks whether a room has a branch; this asks how many"
              " different things the branch can be. `exclusive_group` shares ONE roll across"
              " buckets (v2.py:5361-5379) — without it every rule rolls its own)")

    if ladder_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the ladder — {ladder_summary}")
        for h in ladder_lints[:8]:
            print(f"          · {h}")
        print("          (register.md — a field scene is ONE rung and the ladder is climbed across"
              " 3-4 chained screens. Opening at the top means there are no stairs to it; stopping"
              " below oral means the climb never arrives)")

    if talk_summary:
        print(f"  {'─'*72}")
        print(f"  lint · talk screens — {talk_summary}")
        for h in talk_lints[:8]:
            print(f"          · {h}")
        print("          (register.md — if a person is in the room, they speak. The `dialog`"
              " block already exists; this counts whether it was used)")

    if loop_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the act menu — {loop_summary}")
        for h in loop_lints[:8]:
            print(f"          · {h}")
        print("          (the-surfaces.md — a COUNT, never a target. One good loop beats four"
              " thin ones; a repeatable explicit surface with no act menu is a one-time scene"
              " the player is asked to re-read)")

    if act_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the act nodes — {act_summary}")
        for h in act_lints[:10]:
            print(f"          · {h}")
        print("          (register.md — the beat the player is IN while it is happening. `explicit"
              " floor` is a game-wide share and a game can clear it with every act node warm: the"
              " measured failure sealed 95% of its crude prose in one room and scored ZERO on all"
              " nine of its repeatable loops. 3 is the count `explicit floor` needs to call a beat"
              " explicit at all, not a new threshold)")

    if rung_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the meter ladder — {rung_summary}")
        for h in rung_lints[:8]:
            print(f"          · {h}")
        print("          (the-meters.md W4 — a NUMBER, never a bar. 15/35/55/75 is the DoL"
              " seed's spacing, and ALL 16 declared tiers across five v2 games put their"
              " lowest rung at exactly 15, because it shipped as a copyable example. The"
              " field runs 8-17 rungs, lowest at 5)")

    if cast_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the cast's meters — {cast_summary}")
        for h in cast_lints[:8]:
            print(f"          · {h}")
        print("          (the-meters.md W1/W6 — a roster of identical `relation = 0` is a fine"
              " answer for a ladder game and the whole engine missing from a roster one. Read it"
              " next to board.who_climbs)")

    if cw_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the counterweight — {cw_summary}")
        for h in cw_lints[:8]:
            print(f"          · {h}")
        print("          (the-meters.md W5 — HEURISTIC: a player trait starting at 50+ whose"
              " effects mostly fall, declared needs excluded. One field game in 25 ships one"
              " that gates; four of our five ship one and three gate almost nothing)")

    if shape_lints or shape_summary:
        print(f"  {'─'*72}")
        print(f"  lint · screen shape — {shape_summary}")
        TAGS = {"rows": "rows", "open": "wide open", "still": "never moves", "thin": "one lever"}
        for h in shape_lints[:10]:
            tag = TAGS.get(h["kind"], h["kind"])
            where = f"{h['id']} @{h['loc']}" if h["id"] != "—" else h["loc"]
            print(f"          · [{tag}] {where}: {h['note']}")
        if len(shape_lints) > 10:
            print(f"          · … and {len(shape_lints)-10} more")
        print("          (the-surfaces.md R5/R6 — thresholds not yet establishable; judge these,"
              " do not score them)")

    if words_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the words the player has to already own — {words_summary}")
        for h in words_lints:
            print(f"          · {h}")
        print("          (register.md — a LIST, never a score. Measured against the 25-game"
              " field's own vocabulary (scripts/genre_words.txt, words used by 4+ games).")
        print("           The field runs locale-locked nouns at 0.8 per 10k words; our v2 games"
              " run 9-96. Invented words are safe — the fiction builds them; real regional")
        print("           objects are the trap, because they look defined and are not. Gloss it"
              " in the sentence that first uses it, or use the plain word.")
        print("           [ambiguous] and [false friend] rows come from a CURATED list, not the"
              " corpus — a false friend is by definition a common word, so genre_words.txt")
        print("           is structurally blind to them. Expect false positives and read them:"
              " vesper's `torch` is a CUTTING torch, which is correct everywhere)")

    if fh_summary:
        print(f"  {'─'*72}")
        print(f"  lint · named before met — {fh_summary}")
        for h in fh_lints[:14]:
            print(f"          · {h}")
        if len(fh_lints) > 14:
            print(f"          · … and {len(fh_lints)-14} more")
        print("          (the-first-hour.md F7/F9 — a LIST, never a score. The game does not"
              " use a name until it has earned it: before the player has met a person or a")
        print("           place, say what it IS and where; after, say the name. A character"
              " named in passing and a corridor that needs no introduction are both fine —")
        print("           read the rows and make the call. degrees-of-lewdity swaps the"
              " description for the name on the meeting flag in 64 places)")

    if clock_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the clock in the prose — {clock_summary}")
        for h in clock_lints[:16]:
            print(f"          · {h}")
        if len(clock_lints) > 16:
            print(f"          · … and {len(clock_lints)-16} more")
        print("          (the-clock.md C2 — a LIST, never a score. Read each line at the LAST"
              " minute of the window beside it: a RULE is still true there and is correct")
        print("           work (\"Nobody comes in before eleven in February\"); a READING is"
              " not (\"Shutter up at eight\", true for 1 minute of 300). The turn is")
        print("           grammatical — the reading becomes a rule and the fact survives:"
              " \"The shutter goes up at eight\")")

    if tcost_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the time cost is not on the button — {tcost_summary}")
        for h in tcost_lints[:10]:
            print(f"          · {h}")
        if len(tcost_lints) > 10:
            print(f"          · … and {len(tcost_lints)-10} more")
        print("          (the-clock.md C4 — a LIST, never a score. The engine tags TRAVEL time"
              " for you on a nav card (v2.py:4724, \"20m\") and tags ACTIVITY time nowhere")
        print("           (v2.py:12733), so the sidebar clock jumps unexplained. Recommended,"
              " not required: 4,219 of the corpus's 4,260 duration tags are one game's)")

    if cur_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the currency in the prose — {cur_summary}")
        for h in cur_lints[:10]:
            print(f"          · {h}")
        if len(cur_lints) > 10:
            print(f"          · … and {len(cur_lints)-10} more")
        print("          (the-economy.md R7 — a LIST, never a score. The lines listed are the"
              " ones NOT in the game's main currency. Field: one notation carries a median 92%"
              " of a game's money references, and a money word carries an exact amount 20% of"
              " the time against our 51%)")

    if price_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the price is spelled out — {price_summary}")
        for h in price_lints[:10]:
            print(f"          · {h}")
        if len(price_lints) > 10:
            print(f"          · … and {len(price_lints)-10} more")
        print("          (the-economy.md R7 part 3 — a LIST. 94% of the field's 654 priced"
              " labels use a symbol, 5% spell the unit out, 0.8% use a currency code. An"
              " invented unit used consistently — \"10 coin\", \"1000 caps\" — is the field's"
              " own pattern and is not a defect)")

    if world_lints:
        print(f"  {'─'*72}")
        print(f"  lint · the prose names places the map does not have — {len(world_lints)} to eyeball")
        for h in world_lints[:10]:
            print(f"          · \"{h['part']}\" ×{h['count']}: {h['line']}…")
        print("          (either the location is missing, or the sentence is wrong)")
    print()
    sys.exit(0 if judged and npass == judged else 1)


if __name__ == "__main__":
    main()
