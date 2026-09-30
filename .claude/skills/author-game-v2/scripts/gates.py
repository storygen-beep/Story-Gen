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
     cannot contain anything that game lacks. A game can score 10/10 on basis
     (1) with no street, no guidance page and unbounded money — every one of
     those invisible to gates 1-10.

Usage:
    python3 gates.py <game-slug>            # resolves games/<slug>/toml_phases/7_final_game.toml
    python3 gates.py <path/to/game.toml>
    python3 gates.py <slug> --json          # machine-readable
    python3 gates.py --words <path>         # the vocabulary lint on ANY text file,
                                            #   for the WANT and BOARD phases, before
                                            #   a game exists to measure
    python3 gates.py --release <slug>       # the ARTEFACT, not the source: is the build
                                            #   in games/<slug>/output/ shippable? Off for
                                            #   every ordinary run; exits non-zero on a red.
    python3 gates.py --beat <path>          # measure LOOSE PROSE the way the build measures
                                            #   a beat — explicit count, sentence length, dash
                                            #   rate, act rungs, and where the body words fall.
                                            #   The only mode that needs no game. Always exits 0.
    python3 gates.py --selfcheck            # does SKILL.md still document every gate and
                                            #   lint this script emits? No game needed.

Why a real TOML parser and not grep: grep misses whitespace-aligned and unspaced
`is_repeatable` variants and badly under-counts repeatables. Parse, never grep.
"""

import sys
import os
import re
import json
import math
import collections
import copy

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
#   mean 4,661 · median 3,154 · min 302 (bus station) · max 35,218 (the anchor)
#   -> 24 of its 25 locations are UNDER 10,000. The exemplar failed its own gate.
# The real shape is one or two deep ANCHORS plus many legitimately thin satellites:
# the anchor alone held 30.2% of all location prose at seed.
#
# ⚠️ THESE THREE ARE A BACKSTOP, NOT THE CHECK — corrected 2026-08-15, study 6.
# When `v2_state.json` declares `board.locations[].fill`, gate 1 checks each location
# against ITS OWN declared budget and these constants are not consulted. They run only
# for a game with no ledger.
#
# Why: a global constant can be
# satisfied by generating N things; a number checked against the author's own declaration
# cannot, because moving it means changing the design. See SKILL.md's operating rule
# "the BOARD DECLARES IT and the gate checks the game against its own declaration".
ANCHOR_SHARE_PCT      = 25.0    # DoL seed: anchor = 35,218 / 116,540 = 30.2%
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

# A share gate judged on fewer cases than this reports "too few to judge", not PASS
# (PRD IC21, LO 2026-09-27). LO decided. Five, not a derived number: the smallest sample
# on which 1 of 1 or 100% of 1 cannot pass.
FEW_CASES = 5
# Only a SHARE gate — a percentage that must reach a floor below 100% — can be "too few to
# judge": 100% of 1 says nothing about a 50% floor. An all-or-nothing gate (every item must
# be right) is judged on any n: 3/3 correct is a real PASS (LO, 2026-09-27).
SHARE_GATES = {"location fill", "explicit floor", "explicit in repeatable",
               "an explicit beat carries a clip", "traversal heat"}

EXPLICIT_BEAT_FLOOR = 7.5
# Share of beats carrying 3+ explicit words. DoL held 7.5%-9.3% across eight
# years and 12x growth. Unlike raw sex-word share (which fell 3.00% -> 0.96% as
# systems and UI outgrew prose), this ratio is stable, so it is the usable floor.
# It is also robust to word-list choice: two different lists both put DoL at
# 8-10%.
#
# ⚠️ THIS IS A FLOOR. ITS UPPER COMPARISON IS MEANINGLESS. Do not read a game
# scoring far above it as "too hot". Two independent reasons:
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
# Valid as a floor.
# Invalid as anything resembling a target.

MENU_CEILING = 8
# Choices on a single repeatable, location-bound canvas. Measured 2026-08-12 across
# 18 shipped sandboxes, counting player-facing links per non-system screen:
#   median screen = 2 links · median p90 = 4 · ~2% of screens exceed 12
# So 8 is already double the field's ninetieth percentile.
#
# Big screens DO exist in real games — the reference game runs 2.9% of its screens
# above 20 links — but they are CATALOGUES: shops, wardrobes, character creation.
# A place the player returns to daily is not a catalogue. references/the-surfaces.md.

SENTENCE_CEILING = 14
# Median sentence length, in words, across all authored beats. The first threshold
# here that measures WRITING rather than structure. Measured 2026-08-12 over 18
# shipped sandboxes: field median 10 words, DoL 9.
#
# ⚠️ TWO INSTRUMENTS, AND THE THRESHOLD SPANS THEM. The field figures come from
# parsing BUILT HTML (the only form a shipped game is available in). This gate reads
# AUTHORED BEAT TEXT from the TOML, which excludes the UI and system strings that
# survive HTML extraction. The same game measures shorter on the second instrument,
# so 14 is calibrated across a seam, not within one basis. It is
# therefore APPROXIMATE — it will catch prose drifting denser, but do not read a
# pass as "matches the field". Tightening it needs the field re-measured on TOML,
# which is not obtainable: we do not have anyone else's source.

# ── The field's joints, and the floor under the prose (PRD IC6, LO 2026-09-27) ────
# Every prose threshold above is a MAXIMUM, so compressed prose passes all of them.
# What separates it from the field is its JOINTS, not its sentence length, so the
# floor is on the joints. Measured 2026-09-27 over the 25 games of
# ~/Documents/Prose_Machine_Sound_Study_20260828/results.json ["field"], built HTML,
# `field_prose()` + `profile()` (after the prose study's measure.py:38): `but` per 1k min 2.46 · p10 2.88 · p25 3.76 · median 4.68 · max 8.44;
# `and` per 1k min 9.26 · p25 19.14 · median 22.77 · max 41.11; coordination ratio
# (and/then/or over because/so/since/though/…) p25 1.81 · median 2.08 · max 3.89.
# LO decided. p10 for `but`, not p25: at p25 the model beats in register.md (3.39, one
# `but` in 295 words) would fail.
FIELD_BUT_P10 = 2.88
FIELD_AND_MAX = 41.11
FIELD_JOINT_RATIO = (1.81, 2.08, 3.89)      # p25, median, max — printed, not judged
JOINTS_MIN_WORDS = 500                      # the field study's own inclusion filter
# Sentence length and verbless fragments, measured the same day over the 26 Round 1
# games (~/Documents/Process_Review_20260925/round1_evidence/dump.py, built HTML,
# G19's split, 2-120 words; fragments = 1-8-word sentences with no finite verb by
# scripts/readable.py's rule). PRINTED, NOT JUDGED: the loud voice runs short on purpose
# — the model beats' median is 7, under the field's p25 — so a sentence floor at p25
# would fail the register LO chose and pass the build it was meant to catch.
FIELD_SENTENCE_MEDIAN = (8.25, 10.5, 13.0)  # p25, median, p75 of per-game medians
FIELD_FRAGMENT_SHARE = (11.36, 15.16, 27.61)  # p25, median, p75, % of sentences

DASH_CEILING = 35.0
# Em and en dashes per 10,000 prose words. The SECOND threshold here that measures
# writing. Dash density is the marker readers most often name when they call prose
# machine-written, and nothing in this file looked at it.
#
# Measured 2026-08-27 over the 25-game mopoga corpus:
#   p50 0.99 · p75 4.21 · p90 17.46 · p95 25.72 · max 35.41 (apocalyptic-world)
#
# The ceiling is the corpus MAXIMUM on purpose. A shipped, heavily-commented game
# writes at 35, so a game at or under it cannot be called wrong without contradicting
# the field. This catches an author who has left the distribution, not one working at
# its edge.
#
# ⚠️ IT COUNTS SPEECH TOO, ON PURPOSE, AND THAT IS A KNOWN COST. An em-dash inside
# dialogue is how English writes an interruption — "Wait — no — I can't, if you
# keep —" is correct as written — so a game with a lot of broken speech scores worse
# without being worse. Narrowing the
# verdict to narration was investigated and REFUSED, because it needs a narration-only
# field baseline that cannot be built: 14 of the 25 corpus games put under 2% of their
# words inside quote marks (corpus median 1.3%), marking speech with italics, speaker
# prefixes, or nothing. Judging a narration-only measurement against an all-prose ceiling
# is exactly the seam error below. The gate reports the split instead and gates the whole.
#
# ⚠️ THIS CONSTANT DOES NOT SPAN THE SEAM THAT SENTENCE_CEILING DOES. The field
# figures come from built HTML and this gate reads authored TOML — the same two bases
# — but the metric was checked on BOTH for the same game and moved 7% between the
# two bases. A rate over word count is insensitive to how text is segmented,
# which is exactly what the seam distorts. Do not weaken this constant believing it
# inherits G19's approximation; it does not.

EXPLICIT_IN_REPEATABLE = 40.0
# Explicit prose must live where the player returns. Re-derived from the field
# 2026-09-28 (LO): 30 random explicit passages per passing game, each traced by hand to
# whether it can play again — Shady Deals 93%, Course of Temptation 76%, Cupid's Way 50%,
# In Her Own Hands 40%; pooled 65% (75/116). Each figure is roughly ±17 points at n = 30.
# The floor is the lowest passing game, so none of the four fails it. Field games carry no
# `is_repeatable`, so "can play again" is the closest faithful reading of this metric. An
# automatic proxy over 59 mopoga games (median 68.7%, p25 40%) misses the hand labels by up
# to 28 points and is not used. Plan: round5/SETTINGS_REDERIVE_PLAN.md.

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

# ── The field's OWN word list, and why this is not `EXPLICIT` above ───────────
# `EXPLICIT` is deliberately broad — it counts kiss, naked, arous, lust, breast —
# and that is correct for every gate that uses it, because those measure a share of
# a game's beats against its own beats: one list, one substrate.
#
# ⚠️ THIS LINT COMPARES A GAME AGAINST THE FIELD, so it must run the FIELD's list or the
# comparison is invalid by construction: mixing word lists across corpora voids every
# cross-comparison.
# This is verbatim `~/Documents/Sex_Loop_Study_20260829/shape.py:12`, which is where
# the field figures below come from.
FIELD_BODY = re.compile(r"\b(cock|dick|cunt|pussy|clit|tits|nipples?|balls|ass|arse|thrust|"
                        r"fuck\w*|cum\w*|orgasm\w*|moan\w*|suck\w*|lick\w*|penetrat\w*)\b", re.I)
FIELD_EXPLICIT_PER_KW = 1.24   # median, 25 mopoga sandboxes
FIELD_EXPLICIT_P25    = 0.95
FIELD_EXPLICIT_ABS    = 457    # median absolute explicit screens
FIELD_MIN_SCREENS     = 20     # shape.py's own inclusion filter: fewer and a game is not in the field

_TW_PASSAGE = re.compile(r'<tw-passagedata[^>]*\bname="([^"]*)"[^>]*>(.*?)</tw-passagedata>', re.S)
_CANVAS_NAME = re.compile(r'^(?:Starting)?Canvas_[A-Za-z0-9_]+?_Node_')

# The ladder a sexual scene climbs, lowest rung first. Used by a LINT ONLY, and
# deliberately: naming an act is not the same as depicting it, and no threshold on
# word-presence would survive contact. It exists to print WHERE a game's scenes sit,
# because both failure directions are real and they look nothing alike — a game can
# open at the top with no stairs to it, or climb forever with no ceiling.
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
                           r"|oral|deepthroat|face-?fuck\w*"
                           r"|fuck(?:s|ed|ing)? (?:your|her|my|his) (?:mouth|face|throat))\b", re.I)),
    ("vaginal", re.compile(r"\b((?<!face-)fuck(?:s|ed|ing)?(?! (?:your|her|my|his) (?:mouth|face|throat|ass))"
                           r"|thrust|penetrat\w*|rides? (?:him|his)"
                           r"|inside her|in her cunt|in her puss\w*)\b", re.I)),
    ("anal",    re.compile(r"\b(anal|in the ass|(?:in|up) (?:your|her|my) ass"
                           r"|fuck(?:s|ed|ing)? (?:your|her|my) ass|butthole)\b", re.I)),
    ("finish",  re.compile(r"\b(cum(?:s|ming)?|came|orgasm\w*|climax\w*|creampie)\b", re.I)),
)
# ⚠️ THE RUNG IS AN ACT, NOT A BODY PART. `cunt` / `puss` / `tits` name anatomy and
# say nothing about what is happening to it — a first draft of this list had them in
# the `vaginal` rung and over-counted penetration openings roughly eightfold. Every entry above is a verb or a verb phrase, and the field
# distribution quoted in the lint was produced by this list AS IT WAS BEFORE 2026-09-30.
#
# ⚠️ CHANGED 2026-09-30 (PRD v2 CK8a · I10), on the same principle: `her ass` / `your ass`
# alone is anatomy, not anal ("he grabs your ass"), and "fucks your mouth / face" is oral,
# not vaginal. Anal now needs an act on the ass (in / up / fucks). The field figures above
# and in `lint_ladder` were measured with the old list — RE-MEASURE PENDING.
RUNG_ORDER = [k for k, _ in RUNGS]

PROSE_BLOCKS = {"paragraph", "dialog", "thought_bubble", "quote", "note"}
MEDIA_BLOCKS = {"image", "video"}
EXPLICIT_MEDIA = re.compile(r"_t[45]\b|/sex/|^sex/", re.I)

# Parts of a building the prose can name. If the writing treats one as a place and
# the graph has no such location, either the location is missing or the sentence is
# wrong — both cheap to fix on the day, expensive twenty thousand words later.
# A LINT, never a gate: "he came through the hall" in a game that deliberately has
# no hall location is a judgement call, and a check that fires on correct work gets
# ignored.
BUILDING_PARTS = ("hall", "hallway", "stairs", "staircase", "landing", "street",
                  "front door", "back door", "garden", "yard", "attic", "cellar",
                  "basement", "porch", "driveway", "corridor")

# Currency naming, used when the ledger does not declare one. Inference is a
# fallback so the economy gates still bite on a game authored before board.economy
# existed; a declaration always wins and the headline says which was used.
CURRENCY_HINT = re.compile(r"money|cash|funds?|wallet|credits?|coins?|gold", re.I)
# `coin` was missing until 2026-08-14, which made a coin-denominated currency invisible
# to every economy gate.


# ─────────────────────────────────────────────────────────────────────────────
# Model building
# ─────────────────────────────────────────────────────────────────────────────
class Beat:
    """One screen of text the player reads. The unit the floors are counted in.

    Group variants (blocks[].blocks[]) fold INTO their parent beat rather than
    splitting it, because a Twine passage likewise carries all its <<if>>
    branches inline — folding keeps a game's numbers comparable to the DoL baseline
    the thresholds came from. Cascade beats DO split, because each one is a
    separate screen the player advances through.

    ⚠️ UNFOLDING `block_pool` WAS PROPOSED AND IS REFUSED (2026-08-27).
    ═══════════════════════════════════════════════════════════════════════════
    `~/Documents/Female_PC_Craft_Study_20260823/proposal_for_skill.md` opens with a
    **P0**, to ship "first, alone": count a pool as ONE representative variant for
    word-count purposes, because otherwise "the scoreboard will punish authors for
    using it." The observation underneath is TRUE — a pool renders one of N, so a
    game's counted words exceed what any single pass shows.

    THE CONCLUSION DOES NOT FOLLOW, and the fix would break a correct game.
    `the-board.md` §1 (`fill`) decides it: fill is "its word budget — in round numbers, written
    now, BEFORE THE PROSE." It is a plan for what the author will WRITE. Three pooled
    variants of 400 words ARE 1,200 words written. A one-variant count would fail an
    author for doing exactly what the doctrine asked — which is the Study 2 R4 failure
    the proposal itself cites two sections earlier: a check that fails a game for
    obeying the doctrine is a bug in the check.

    The field-baselined gates barely move either, because they are RATES and both
    halves move together.

    ⚠️ AND A SPLIT MODEL (each pool child its own beat) ORPHANS POOL CHILDREN FROM
    THE NODE'S SIBLING MEDIA, so `an explicit beat carries a clip` would read pooled
    explicit variants as dry when they sit under a clip on the shared node.

    So: no change. Gate 1 REPORTS the per-pass figure (see G1) and judges the budget.
    ═══════════════════════════════════════════════════════════════════════════
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


def _pool_pass_words(game):
    """(pool count, words one pass shows) — REPORTING ONLY, judged by nothing.

    A `block_pool` renders one of N (`v2.py:14572`), so a game's counted words and the
    words a single playthrough shows are two different quantities. Gate 1 judges the
    first, because `fill` is a budget for prose WRITTEN (`the-board.md` §1) — see the
    refusal recorded on `Beat`. It prints the second so the gap is visible rather than
    argued about, the way gates 19/20 print their distribution and G43 prints its split.

    Per pass = every variant's words replaced by the MEDIAN variant of its pool. Median,
    not first, so the figure does not swing on authoring order.
    """
    per_pool = []

    def walk(blocks):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            props = b.get("props") or {}
            kids = b.get("blocks") or props.get("blocks") or []
            if b.get("type") == "block_pool" and kids:
                sizes = []
                for k in kids:
                    beat = Beat("", "")
                    _collect([k], beat, [], "", "")
                    sizes.append(beat.words)
                if sizes:
                    per_pool.append((sum(sizes), sorted(sizes)[len(sizes) // 2]))
            walk(kids)
            for sub in props.get("beats") or []:
                walk(sub.get("blocks"))

    for c in game.get("canvases") or []:
        for n in c.get("nodes") or []:
            walk(n.get("blocks"))
    return len(per_pool), sum(written - shown for written, shown in per_pool)


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
    which meant a real deduction written the only way that works counted as INCOME.
    A `subtract` effect is
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

        # Reads INSIDE the story text: a `group` / `block_pool` gated on a flag. This is
        # how `register.md`'s truth rule gates a line about the past, and how a daily card
        # remembers a one-time step. Kept apart from `reads` on purpose: the economy gates
        # read `reads` as "this surface is gated on it", and a colouring read is not a gate.
        # G7 (milestones) is the one check that asks "does anything read what this set?",
        # and for that question a callback line is a real read. Added 2026-09-25, after the
        # `mum_sat_down` rewrite's correct first-time step failed G7 for a read it could not
        # see (`STYLE_REWRITE_MUM_SAT_DOWN.md`).
        text_reads = set()

        def _block_reads(blocks):
            for b in blocks or []:
                if not isinstance(b, dict):
                    continue
                props = b.get("props") or {}
                for holder in (b, props):
                    for it in _conditions_of(holder):
                        for k in ("flag_key", "trait_key"):
                            if it.get(k):
                                text_reads.add(it[k])
                _block_reads(b.get("blocks") or props.get("blocks"))
                for sub in props.get("beats") or []:
                    _block_reads(sub.get("blocks"))

        for n in c.get("nodes") or []:
            _block_reads(n.get("blocks"))

        # Keys this canvas reads ONLY as "not yet" (`is_false`). G7 asks whether anything
        # reads what a milestone set, and a read that shows content only while the flag
        # is OFF is not content the milestone opened — it is content the milestone shuts.
        # LO, 2026-09-26 (PRD WS4). Every other consumer keeps the plain `reads`.
        pos_keys, neg_keys = set(), set()
        for it in _pr_collect(c, lambda d: (d.get("flag_key"), d.get("operator"))
                              if isinstance(d.get("flag_key"), str) else None, set()):
            (neg_keys if it[1] in ("is_false", "is_not_true") else pos_keys).add(it[0])
        for it in _pr_collect(c, lambda d: d.get("trait_key")
                              if isinstance(d.get("trait_key"), str) else None, set()):
            pos_keys.add(it)
        neg_only = neg_keys - pos_keys

        model.append(dict(id=cid, loc=loc, rep=rep, beats=beats,
                          sets=sets, reads=reads, traits=traits, text_reads=text_reads,
                          neg_only_reads=neg_only,
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

    The bug this catches: a walk-on character with no NPC record was
    written as a dialog block borrowing a declared NPC's id, which would have
    rendered the wrong name over her line. Declaring her instead is not the fix —
    that breaks the standing-surface gate, which wants every declared character
    findable and scheduled. One-scene characters are narrated, never declared.

    Deliberately narrow. The naive version of this check — flag dialogue on any
    canvas without an `npc` binding — returns many false hits, because every
    triggerless rung is unbound by design and correctly carries its own character's
    voice. Naming the character in the canvas id is what tells them apart.
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
                # `npc_jo` is named by a canvas called `rung_jo_sit`.
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


def lint_ambient_presence(model, game):
    """A random ambient in which a character SPEAKS, with nothing saying he is there.

    The other half of G38. G38 asks whether a one-shot meeting can only play in a room
    its character is standing in, and is scoped to the auto-fire path — which does not
    read `requires_npc` at all (`v2.py:4559`). This asks the same question of the path
    that DOES read it: `trigger_mode = "random"` (`checkRandomEncounters`, `v2.py:5245`).

    Nothing was checking it, and the miss is the exact shape SKILL.md warns about — the
    doctrine was right, the instrument was aimed at the wrong path.

    The failure it catches passes a green build: an ambient puts a man in a room,
    speaking, with no gate of any kind. The navigation panel reads presence from the
    schedule and correctly shows him absent; the ambient then fires anyway and he is
    there. Once the panel is wrong once it stops being read, and the panel is how a
    sandbox is navigated.

    THREE OUTCOMES, and they are different jobs — the split is the point of the lint:

      · `gate it`      — the speaker has schedule rows at this location, so the window
                         exists and one line of `requires_npc` is the whole fix.
      · `or narrate`   — the speaker has NO row here, so a gate would strand the canvas
                         forever. The fix is prose: narrate the arrival, the way a
                         correct one already does ("He comes in through the back
                         door"). Do NOT gate these.
      · not reported   — already carries `requires_npc`, an `npc_at_location` condition,
                         or its own `trigger.schedules`.

    A LIST AND NEVER A GATE. An ambient may legitimately place a character who is
    off-schedule, and three ways of saying so are all correct: he is on the telephone,
    he is speaking through a door, he has arrived from somewhere the scene declines to
    name. Only the author can tell those from the defect, so the check hands over the
    rows and the windows and lets them call it.
    """
    npc_rows = collections.defaultdict(list)
    for n in (game.get("npcs") or []):
        for r in (n.get("schedules") or []):
            loc = r.get("location") or r.get("location_id")
            if loc:
                npc_rows[(n.get("id"), loc)].append(r)

    speaking, findings = 0, []
    for c in model:
        if not c.get("random"):
            continue
        trig = (c.get("raw") or {}).get("trigger") or {}
        speakers = []
        for n in c.get("nodes") or []:
            blocks = []
            _dialog_blocks(n.get("blocks"), blocks)
            for b in blocks:
                nid = ((b.get("props") or {}).get("npcId") or "").strip()
                if nid and nid not in speakers:
                    speakers.append(nid)
        if not speakers:
            continue                      # nobody to misplace
        speaking += 1
        if trig.get("requires_npc") or trig.get("schedules"):
            continue
        if any(it.get("type") == "npc_at_location"
               for it in ((trig.get("conditions") or {}).get("items") or [])):
            continue
        loc = c.get("loc")
        placed, stranded = [], []
        for sp in speakers:
            rows = npc_rows.get((sp, loc))
            short = re.sub(r"^npc[_-]", "", sp)
            if rows:
                hrs = " · ".join(f"{r.get('start_time')}-{r.get('end_time')}" for r in rows[:2])
                placed.append(f"{short} ({hrs})")
            else:
                stranded.append(short)
        verdict = (f"gate it on {placed[0].split()[0]}" if placed
                   else "or narrate the arrival — no row here to gate on")
        findings.append(
            f"{c['id']} @{loc}: {', '.join(speakers)} speak(s), no presence gate — "
            f"{verdict}"
            + (f"; {', '.join(stranded)} has no row at this location" if stranded and placed else ""))

    if not speaking:
        return ("", [])
    summary = (f"{len(findings)}/{speaking} ambients where somebody speaks carry no "
               f"presence gate")
    return (summary, sorted(findings))


def lint_badge_before_content(model, game):
    """A ✓ that lands at or before the last thing the player can unlock — and a goal
    threshold no content in the game reads.

    Two findings, one instrument, because they are the same mistake seen from either
    end: a number on a quest card that nothing else in the game agrees with.

    `engine.md` §23 already warns that `terminal` is NOT computed from progress —
    Frame 1 fires on `card.terminal === true` alone (`v2.py:15404`), ahead of the ready
    and goal frames, and nothing checks that anything was achieved. It then gives the
    rule that follows from it: terminal belongs on a card the player has to CLIMB TO.
    What no check asked is **climb to WHAT** — whether the threshold the badge sits on
    is above the last threshold any content reads.

    A terminal card can print ✓ at or before the click that opens its content, or ride
    a different meter from the one the door reads, so the badge can arrive at 0. A card
    can also ask the player to climb to a threshold no condition anywhere reads, hidden
    only because the terminal frame outranks the bullets that would have shown it.

    THE FIX THE FINDING POINTS AT is not a bigger number. A meter is the wrong thing to
    gate a badge on at all: put the ✓ on a FLAG the content sets on its way out, so it
    means "you have played this" instead of "you have ground past it". The v1 hint
    system had exactly that pairing (`arc_closure_flag` + `arc_complete`,
    `template_import.py:1017-1023`) and the v2 card schema dropped it.

    A LIST, NEVER A GATE. "Content" here means a canvas condition reading that same
    (character, trait), which is a proxy: an author may legitimately put a badge on a
    meter no canvas reads if the arc closes on something else. Read the rows.
    """
    cards = game.get("quest_cards") or []
    if not cards:
        return ("", [])

    # the highest `gte` threshold any CANVAS condition reads, per (npc, trait)
    ceiling, rungs = {}, collections.defaultdict(set)
    def scan(o):
        if isinstance(o, dict):
            key = o.get("trait_key") or o.get("trait")
            npc = o.get("npc_id")
            op = o.get("operator") or o.get("op")
            val = o.get("value")
            if key and npc and op in ("gte", "gt") and isinstance(val, (int, float)):
                k = (npc, key)
                ceiling[k] = max(ceiling.get(k, float("-inf")), float(val))
                rungs[k].add(float(val))
            for v in o.values():
                scan(v)
        elif isinstance(o, list):
            for v in o:
                scan(v)
    for c in model:
        scan(c.get("raw"))

    findings = []
    n_terminal = 0
    for card in cards:
        npc = card.get("npc_id")
        if not npc:
            continue
        short = re.sub(r"^npc[_-]", "", npc)
        # ── the badge
        if card.get("terminal"):
            n_terminal += 1
            gates = [i for i in (card.get("when") or [])
                     if i.get("trait") and i.get("op") in ("gte", "gt")
                     and isinstance(i.get("value"), (int, float))]
            if not gates:
                pass          # flag-gated or unconditional — this check has no opinion
            else:
                for g in gates:
                    top = ceiling.get((g.get("npc_id") or npc, g["trait"]))
                    if top is None:
                        continue
                    if float(g["value"]) <= top:
                        gap = ("lands ON the last content"
                               if float(g["value"]) == top
                               else f"lands {top - float(g['value']):.0f} EARLY")
                        findings.append(
                            f"[badge] {short}: terminal at {g['trait']} "
                            f"{g['op']} {g['value']:g}, but content reads "
                            f"{g['trait']} up to {top:g} — {gap}")
                # a badge gated on a meter the door does not read at all
                door_traits = {t for (n, t) in ceiling if n == npc}
                mine = {g["trait"] for g in gates}
                if door_traits and not (mine & door_traits):
                    findings.append(
                        f"[badge] {short}: terminal gated on {', '.join(sorted(mine))} "
                        f"while the content reads {', '.join(sorted(door_traits))} — "
                        f"a different meter, so the ✓ can arrive at zero")
        # ── the goal nothing pays
        for g in (card.get("goals") or []):
            if not (g.get("trait") and g.get("op") in ("gte", "gt")
                    and isinstance(g.get("value"), (int, float))):
                continue
            who = g.get("npc_id") or npc
            top = ceiling.get((who, g["trait"]))
            if top is None:
                continue          # no content reads this trait at all — nothing to compare
            if float(g["value"]) > top:
                findings.append(
                    f"[goal] {short}: card asks for {g['trait']} {g['op']} "
                    f"{g['value']:g}, but nothing in the game reads {g['trait']} "
                    f"above {top:g} — {float(g['value']) - top:.0f} points that buy nothing")
            elif float(g["value"]) not in rungs[(who, g["trait"])]:
                # A rung BELOW the ceiling that still opens nothing. Splits a real
                # climb into halves the player is told to hit and is not paid for.
                real = ", ".join(f"{v:g}" for v in sorted(rungs[(who, g["trait"])]))
                findings.append(
                    f"[rung] {short}: card asks for {g['trait']} {g['op']} "
                    f"{g['value']:g}, which no condition reads — the real rungs on "
                    f"{g['trait']} are {real}")

    if not n_terminal:
        return ("", [])
    summary = (f"{len(findings)} finding(s) across {n_terminal} terminal card(s) — "
               f"a ✓ at or before the last content, or a goal nothing reads")
    return (summary, sorted(set(findings)))


def lint_refusal_shape(model, game):
    """WHICH rows are shown locked, and whether the reason on them is a door or a label.

    `engine.md` §15 was reversed 2026-08-24 to *"set `locked_text` by default"*, and it is
    right — a visible mute row is 2.26% of the field and nearly all of that is settings
    chrome. But it answers only what a shown row must SAY. Nothing says how many rows to
    show; the missing half is this one.

    THE FIELD'S DEFAULT IS SILENCE (`findings_B_refusal.md` §2, 16,167 refusing chains):
    **71% render nothing at all**, and the per-game silent share runs a median of **79%**
    across a **22–100%** range. The study's own words: *"a house decision, not a genre
    norm"* — zaras-school-life speaks 78% of its refusals, corpo-life speaks two of 574,
    and both shipped. So this is a LIST and can never be a gate; a threshold here would be
    the invented number `gates.py` refuses elsewhere.

    THREE THINGS IT HANDS OVER, because they are three different calls:

    1. **In-scene.** A shown-locked choice routing to a node inside its OWN canvas is a
       greyed rung in the middle of a beat rather than a door on a room screen.
    2. **Self-moved.** Of those, the ones gated on a trait the same canvas's effects
       WRITE. That is the machinery narrating its own progress bar: the row opens by
       itself in a click or two, so the text hands the player nothing to act on. Contrast
       a row naming something the player goes elsewhere and fixes — a real handle.
    3. **Length.** A DOOR and a REFUSAL are different objects and the numbers say so. The
       field's spoken refusals are a flat mechanical UI label — n=4,540, **median 9
       words**, naming a price 37% of the time. A DOOR is in-fiction; nine words is
       right for "already done" and wrong for the ceiling of a release.
    """
    def _walk(o, f):
        if isinstance(o, dict):
            f(o)
            for v in o.values():
                _walk(v, f)
        elif isinstance(o, list):
            for v in o:
                _walk(v, f)

    shown, in_scene, self_moved, lens = 0, [], [], []
    for c in model:
        raw = c.get("raw") or {}
        cid = c.get("id")
        node_ids = {n.get("id") for n in (raw.get("nodes") or [])}
        writes = set()

        def _w(o):
            # ⚠️ `effects` is not always a list of dicts. Some games carry string
            # entries and an unguarded .get() there took the WHOLE SCOREBOARD down for
            # that game — a lint must never be able to do that. Guard every element.
            for e in (o.get("effects") or []):
                if not isinstance(e, dict):
                    continue
                k = e.get("trait")
                if k:
                    writes.add(("npc:" + e["npcId"] if e.get("npcId") else "player") + "." + k)
        _walk(raw, _w)

        hits = []

        def _f(o):
            if not o.get("show_when_locked"):
                return
            hits.append(o)
        _walk(raw, _f)


        for ch in hits:
            shown += 1
            lt = str(ch.get("locked_text") or "")
            if lt.strip():
                lens.append(len(re.findall(r"[A-Za-z][A-Za-z'\-]*", lt)))
            tgt = str(ch.get("nodeId") or "")
            inside = (ch.get("targetType") == "node" and
                      (tgt in node_ids or tgt.startswith(cid + ".")))
            if not inside:
                continue
            reads = set()
            for it in ((ch.get("conditions") or {}).get("items") or []):
                if not isinstance(it, dict):
                    continue
                k = it.get("trait_key") or it.get("trait")
                if k:
                    reads.add(("npc:" + it["npc_id"] if it.get("npc_id") else "player") + "." + k)
            label = (lt or str(ch.get("text") or ""))[:46]
            same = sorted(reads & writes)
            if same:
                self_moved.append(f'{cid}: "{label}" — gated on {", ".join(same)}, '
                                  f"which this canvas's own effects raise")
            else:
                in_scene.append(f'{cid}: "{label}" — in-scene, gated on '
                                f'{", ".join(sorted(reads)) or "a flag"}')

    if not shown:
        return ("", [])
    findings = sorted(self_moved) + sorted(in_scene)
    n_in = len(self_moved) + len(in_scene)
    bits = [f"{shown} shown-locked · {n_in} in-scene"]
    if self_moved:
        bits.append(f"{len(self_moved)} gated on a bar the scene itself moves")
    if lens:
        lens.sort()
        med = lens[len(lens) // 2]
        bits.append(f"reason length median {med}w (field refusal median 9)")
    return (" · ".join(bits), findings)


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
        # on the list. Gating room choices while leaving show_when_locked on all of them
        # moves "open on turn one" and leaves the game playing exactly as wide as before —
        # the number that was reported moves and the wall does not.
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


def lint_faceless_surfaces(game):
    """Repeatable person-bound canvases that render no portrait. A LIST, never a score.

    `trigger.npc` is what puts a character's face on a location screen AND what gates that
    surface on their declared [[npcs.schedules]] (v2.py:5176-5179). A repeatable canvas that
    names somebody via `requires_npc` but carries no `npc` renders instead as a plain
    activity button (v2.py:5259 skips only canvases that HAVE an npcId) with no presence
    check of any kind — `requires_npc` is read on exactly two paths, trigger_mode = "random"
    (v2.py:5343) and substitution_only (v2.py:5486), and this is neither.

    ⚠️ A LIST AND NOT A GATE, on purpose. The hard version of this failure — `npc` written
    one level too high, where the key is discarded outright — is convicted by the gate
    `no canvas key is discarded`, which cannot produce a false positive. THIS is the
    soft version, and it has legitimate instances: walk-ins and scenes that happen in a
    place while somebody is around, often already windowed by their own
    `trigger.schedules` — the correct alternative per the-first-hour.md F5b. A gate here
    would fail games for obeying the doctrine, which is the R4 error. Measure the
    artefact the check reads.
    """
    rows = []
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        if not _rep_of(t) or _is_dev(c):
            continue
        if t.get("npc"):
            continue
        who = t.get("requires_npc")
        if not who:
            continue
        # the two paths that DO read requires_npc — nothing is missing there
        if t.get("trigger_mode") == "random" or t.get("substitution_only"):
            continue
        # ⚠️ list(), not the bare call — _conditions_of is a GENERATOR and a generator is
        # always truthy, which read every unconditioned hub as "conditions only" once.
        gated = "windowed by trigger.schedules" if t.get("schedules") else (
            "conditions only, no window" if list(_conditions_of(t))
            else "NO window and NO conditions")
        rows.append(f"{c.get('id')} @{t.get('location')}: names {who}, renders as a link "
                    f"not a face — {gated}")
    if not rows:
        return "", []
    return (f"{len(rows)} repeatable canvas(es) name a character and render no portrait"), sorted(rows)


# Where the engine resolves an `@token` — every other string reaches the player raw.
# Taken from the generator's call sites (v2.py), re-read 2026-09-27; engine.md §43 carries
# the same table. Paths are normalised: every list index becomes "[]".
#   block content               _resolve_at_references at v2.py:15897 (def :15350)
#   choice / exit text          _resolve_at_references_expr at v2.py:13937
#   locations[].description     v2.py:10252 · description_variants[].text v2.py:10276
#   locations[].blocked_message v2.py:10127 — ⚠️ HALF: the copy in setup.locations
#                               (v2.py:1039) is raw and navDestBlockedReason prints it
#                               (v2.py:5241), so a token there leaks onto the nav card
#   door description / option text / locked_text   v2.py:10209, :12961, :12963
#   npcs[].role                 v2.py:15985
#   phone surfaces              setup.resolveAtRefs at runtime, v2.py:2239-2670
#   story_arc emotion ranges    v2.py:6826, :6838
_TOKEN_RESOLVED_EXACT = {"locations[].description", "locations[].description_variants[].text",
                         "npcs[].role"}


def _token_resolved(path):
    if path in _TOKEN_RESOLVED_EXACT:
        return True
    if path.startswith("canvases[].nodes[]"):
        if path.endswith(".content"):
            return True
        if path.endswith(".text") and ("choices[]" in path or "exit_block" in path):
            return True
    if path.startswith("locations[].properties.door"):
        return path.endswith((".description", ".text", ".locked_text"))
    if path.startswith("phone."):
        return path.endswith((".content", ".text", ".notify", ".player_message",
                              ".npc_response"))
    return path.startswith("story_arc.") and path.endswith(".description")


def _token_never_rendered(path, owner):
    """A key the generator never emits: a token there is untrue source, not a leak."""
    if path == "canvases[].description":
        return "dev surfaces only — CanvasReview_*, the --debug banner"
    # npcs[].description reaches only the CustomizeCharacters screen, and only for an
    # NPC with customizable = true; for everyone else it renders nowhere.
    if path == "npcs[].description" and not owner.get("customizable"):
        return f"{owner.get('id')} is not customizable, so its description never renders"
    return None


def lint_unresolved_tokens(game):
    """`@player` / `@npc` in a field the engine never resolves. Returns (summary,
    player_facing_rows, dev_rows); a player-facing row is the `--ship` BLOCK row
    "no raw token on screen".

    Walks the WHOLE game, every nested list included — the list this replaced checked
    eight top-level fields and skipped lists, which is where leaks hide (`npcs[].tags`,
    `relationship_options`). Scoped to references the engine
    WOULD resolve in prose — a declared npc slug or `player` — so an email address or a
    decorative `@` is not a finding. engine.md §43.
    """
    known = {"player"}
    for n in (game.get("npcs") or []):
        nid = str(n.get("id") or "")
        known.add(nid)
        if nid.startswith("npc_"):
            known.add(nid[4:])
    pat = re.compile(r"@(\w+(?:\.\w+)?)")
    player, dev = [], []

    def walk(node, path, owner):
        if isinstance(node, dict):
            if "customizable" in node or ("id" in node and "relationship_options" in node):
                owner = {"id": node.get("id"), "customizable": node.get("customizable")}
            where = (node.get("id") or node.get("key") or node.get("group")
                     or node.get("ready_canvas"))
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else key,
                     dict(owner, at=where or owner.get("at")))
        elif isinstance(node, list):
            for item in node:
                walk(item, f"{path}[]", owner)
        elif isinstance(node, str):
            hits = sorted({m.group(0) for m in pat.finditer(node)
                           if m.group(1).split(".")[0] in known})
            if not hits or _token_resolved(path):
                return
            row = f"{path} [{owner.get('at') or '?'}]: {' '.join(hits)}"
            why = _token_never_rendered(path, owner)
            if why:
                dev.append(f"{row} — {why}")
            else:
                player.append(f"{row} — prints raw")

    walk(game, "", {})
    if not player and not dev:
        return "", [], []
    bits = []
    if player:
        bits.append(f"{len(player)} player-facing")
    if dev:
        bits.append(f"{len(dev)} dev-only")
    return " · ".join(bits), sorted(player), sorted(dev)


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
# The load lints — register.md "The load rules"
# ─────────────────────────────────────────────────────────────────────────────
# Three LISTS, never scores. A threshold is refused: it would red games for the age
# of the doctrine, which is the R4 / study-6 / P0 failure this file has turned down
# four times. The fix is per-sentence, so the useful artefact is the sentences.
#
# Field figures, 27 corpus games / 14.5M prose words, quoted at each print site.

GLOSS_RE = re.compile(r",\s*(which|who)\s+(means|is|are|was|were)\b", re.I)

NEGATION_RE = re.compile(
    r"\b(not|never|no|nothing|nobody|neither|nor|without|cannot)\b"
    r"|n['’]t\b", re.I)
# ⚠️ THE CONTRACTION BRANCH IS SEPARATE, AND THE VERSION WITHOUT IT WAS WRONG FOR
# TWO DAYS. Until 2026-09-01 the alternation carried `n't` INSIDE the `\b(...)\b`
# group, and `\bn't\b` can never match inside a word: the `n` of `doesn't` is
# preceded by `e`, so there is no word boundary in front of it. `doesn't`, `don't`,
# `won't`, `isn't`, `can't` and `cannot` were ALL invisible to this rule. Fixture:
#   "She doesn't look up."  miss -> HIT      "She does not look up."   HIT (unchanged)
# It is not a symmetric error. Contracted negatives live in SPEECH, the field writes a
# lot of speech, and so the hole hid much of the field. The
# field's own rate roughly doubles once it is closed — see the re-based figures under
# `lint_negation`. Anything measured with the old pattern is void.

# The L2 field baseline, re-measured 2026-09-01 with the fixed regex above and with the
# field reduced to NARRATION — the register `_narration_by_canvas` reads on the game's side —
# by stripping `<<...>>` macro speech (20 of 27 corpus games mark speech that way) and
# quoted spans, then splitting with `_beat_sentences`. Same regex, same splitter, same
# register, both sides. 25 games, 784,591 sentences.
#
# ⚠️ THESE ARE LINT BOUNDS, NOT A GATE. Nothing fails on them and nothing should:
# a game over the max is a finding to read, not a build to break. The old values (7.59 / 13.56 / 20.22) were measured with the broken
# regex against an ALL-TEXT field and must not be restored.
FIELD_NEGATION_P50 = 12.06
FIELD_NEGATION_P90 = 16.38
FIELD_NEGATION_MAX = 25.76   # become-taxi-driver

# ⚠️ TIGHTENED, and the loose version is why. `since|years|moved|carried` scored
# "moved his hand" and "carried the tray" as history. This keeps TEMPORAL markers
# only and was checked against a 14-case fixture (7 real history lines, 7 action
# lines) at 0 errors before any figure was taken. It still
# over-counts a sentence that merely mentions a duration — read the list, not the
# number.
HISTORY_RE = re.compile(
    r"\b(used to"
    r"|\bago\b"
    r"|\bsince\b"
    r"|(has|have|had) been\b"
    r"|\b(ever since|these days|back then|any more|anymore)\b"
    r"|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s+"
    r"(days?|weeks?|months?|years?)\b"
    r")", re.I)


def _narration_by_canvas(game):
    """[(canvas_id, is_repeatable, [sentence, ...]), ...] — NARRATION ONLY.

    ⚠️ NOT built on `model`, and that is the point. `PROSE_BLOCKS` folds `dialog` in
    with `paragraph`, so a lint reading `Beat.text` scores speech — and the rule these
    three serve exempts speech in full ("The same rule for a phrase, not just a word":
    a character may talk however that person talks). The first cut of this lint flagged
    a character's own line, *"That's the county's arithmetic, not mine."*

    ⚠️ THE BASIS DIFFERS FROM THE FIELD FIGURE, deliberately, and in the field's
    favour. The corpus exists only as built HTML with speech inline, so the p50/p90/max
    quoted at each print site are ALL-TEXT and the field's narration-only rates would be
    higher than printed. Excluding speech raises a game's numbers, so the gap this
    reports is the conservative one. It can understate the drift; it cannot invent it.
    """
    out = []
    for c in game.get("canvases") or []:
        buf = []

        def walk(blocks):
            for b in blocks or []:
                if not isinstance(b, dict):
                    continue
                props = b.get("props") or {}
                if b.get("content") and b.get("type") != "dialog":
                    buf.extend(_beat_sentences(str(b["content"])))
                walk(b.get("blocks") or props.get("blocks"))
                for sub in props.get("beats") or []:
                    walk([sub])

        for nd in c.get("nodes") or []:
            walk(nd.get("blocks"))
        if buf:
            rep = _rep_of(c.get("trigger"))
            out.append((c.get("id", "—"), rep, buf))
    return out


def lint_gloss(game):
    """A fact, then an explanation of the fact, welded into the same sentence.

    `register.md` "The load rules" L1. The field's worst game writes 0.24 per 1,000
    words. A gloss is always more abstract than
    the thing it glosses, which is why it costs the reader rather than helping them.

    Returns (rate per 1,000 words, hits) — one hit per sentence, worst canvas first.
    """
    hits, words = [], 0
    for cid, _rep, sents in _narration_by_canvas(game):
        for s in sents:
            words += len(re.findall(r"[A-Za-z][A-Za-z']*", s))
            m = GLOSS_RE.search(s)
            if m:
                hits.append(dict(canvas=cid, line=s.strip()[:110], joint=m.group(0).strip()))
    rate = 1000.0 * len(hits) / words if words else 0.0
    return rate, sorted(hits, key=lambda h: h["canvas"])


def lint_negation(game):
    """Sentences whose claim is what did NOT happen.

    `register.md` "The load rules" L2. Behind almost every one is a positive fact that
    is shorter and more specific, so this is the rare subtraction that makes the prose
    MORE specific.

    ⚠️ RE-BASED 2026-09-01, and BOTH the regex and the field figure moved. The old
    field numbers (p50 7.59%, max 20.22%) were taken with the broken `\bn't\b` pattern
    above AND against an ALL-TEXT field baseline, while this function has always read
    NARRATION ONLY (`_narration_by_canvas` drops `dialog`).

    Re-measured with the fixed regex, the field reduced to narration the same way
    (macro speech and quoted spans stripped) and split with `_beat_sentences` — the
    same regex, splitter and register on both sides, 25 games, 784,591 sentences:

        field   p50 12.06%  ·  p90 16.38%  ·  p95 22.32%  ·  MAX 25.76%
                                                    (become-taxi-driver)

    ⚠️ MEASURE NARRATION, NOT BUILT HTML. A game's build carries thousands of words of
    engine-generated labels, room lists and sidebar with almost no negation in them,
    which dilutes exactly the quantity being measured. The authored narration is the
    register an author controls and the one this lint reads.

    Returns (share of sentences, total sentences, worst canvases) — a canvas is worth
    listing only once it is both above the field max and carrying real prose.
    """
    total = neg = 0
    per = []
    for cid, _rep, ss in _narration_by_canvas(game):
        n = sum(1 for s in ss if NEGATION_RE.search(s))
        total += len(ss)
        neg += n
        if len(ss) >= 8:
            per.append(dict(canvas=cid, share=100.0 * n / len(ss), n=n, of=len(ss),
                            line=next((s.strip()[:100] for s in ss if NEGATION_RE.search(s)), "")))
    share = 100.0 * neg / total if total else 0.0
    return share, total, sorted([p for p in per if p["share"] > FIELD_NEGATION_MAX],
                                key=lambda p: -p["share"])


def lint_history_repeatable(game):
    """Backstory on a screen the player re-enters dozens of times.

    `register.md` "The load rules" L3. Field max 5.41%.
    A repeatable canvas is the expensive place for history — the reader reconstructs a
    prior state of the world before the present one means anything, every visit.

    ⚠️ REPEATABLE ONLY, and that is the rule rather than a scoping convenience. The
    same sentence on a one-time canvas is where the doctrine says to PUT it, so a
    lint that flagged both would argue against its own fix.

    Not to be confused with `the-clock.md` C2, which owns clock time. This is elapsed
    time.
    """
    hits, total = [], 0
    for cid, rep, sents in _narration_by_canvas(game):
        if not rep:
            continue
        for s in sents:
            total += 1
            m = HISTORY_RE.search(s)
            if m:
                hits.append(dict(canvas=cid, line=s.strip()[:110], marker=m.group(0).strip()))
    share = 100.0 * len(hits) / total if total else 0.0
    return share, total, sorted(hits, key=lambda h: h["canvas"])


# ─────────────────────────────────────────────────────────────────────────────
# The loud voice's lints — added 2026-09-24 with `register.md` "The voice — say it
# loud" and "The truth rule", `the-first-hour.md` F1b and `the-meters.md` "What the
# player is shown". Source: PRD_SKILL_STYLE_AND_OPENING.md §5.5.
#
# ⚠️ ALL FIVE ARE LINTS, NOT GATES, on purpose. The PRD scoped the blocking overhaul
# out, and P0 applies: a gate on a brand-new doctrine measures the doctrine's age, not
# the games.
# ─────────────────────────────────────────────────────────────────────────────

# A claim about a past the player may not have had. Deliberately NOT folded into
# HISTORY_RE: that regex is the basis of L3's field comparison (p50 1.64%, max 5.41%),
# and widening it would silently re-base a figure measured on the old marker set.
PAST_CLAIM_RE = re.compile(
    r"\b(last night|last time|yesterday|this week|again|the other day|as usual|"
    r"like always)\b", re.I)
# ⚠️ "every time" was in the first cut and came out the same day: "every time" is habitual
# present tense ("every time he draws back"), not a claim about a past.
#
# ⚠️ A MARKER IS NOT A CLAIM (PRD v2 CK4 · H6 · I15 · I26, 2026-09-30). The bare marker
# fired on "Delgado reads this week's log aloud", on "the last night in May" about her
# sister, and on "he wants you again". A hit now counts only when the SAME CLAUSE also has
# the player's pronoun (subject or object, per `[settings] narration_person`) and a
# past-tense verb. LO Q1: "again" alone never fires; it fires only inside a past-tense
# clause about her ("you came again").
_PAST_VERB_RE = re.compile(
    r"\b(\w+ed|was|were|had|did|went|came|saw|said|told|took|gave|made|got|left|ate|slept)\b",
    re.I)
_CLAUSE_SPLIT_RE = re.compile(r"[,;:—–()]|\s(?:and|but)\s", re.I)


def _player_pronoun_re(game):
    """The player's own words for `[settings] narration_person` (default second, as
    `readable.py` reads it): you/your in second, I/me/my in first, and in third the
    protagonist's name plus she/her."""
    person = str((game.get("settings") or {}).get("narration_person") or "second")
    if person == "first":
        words = ["me", "my", "mine", "myself"]
    elif person == "third":
        name = str((game.get("player") or {}).get("name") or "")
        words = re.findall(r"[A-Za-z']+", name) + ["she", "her", "hers", "herself"]
    else:
        words = ["you", "your", "yours", "yourself"]
    pat = r"(?i:\b(?:" + "|".join(re.escape(w) for w in words) + r")\b)"
    # First person's "I" is matched as a capital only, so no stray lower-case "i" counts.
    return re.compile(pat + (r"|\bI\b" if person == "first" else ""))


def _past_claim_clause(sentence, pron_re):
    """The PAST_CLAIM_RE match in `sentence` whose clause also holds the player's pronoun
    and a past-tense verb, else None.

    A clause that holds ONLY the marker ("Last night, you came to his room." / "You were
    tired, again.") is judged joined to its neighbour clause on each side, because the
    comma cut the claim from its verb (LO, 2026-09-30, the CK4 comma hole). A marker
    joined to a clause about somebody else ("Last night, Delgado read the log.") still
    has no pronoun of hers, so it still does not fire.
    """
    clauses = [c or "" for c in _CLAUSE_SPLIT_RE.split(sentence)]

    def claims(text):
        return bool(pron_re.search(text) and _PAST_VERB_RE.search(text))

    for i, clause in enumerate(clauses):
        m = PAST_CLAIM_RE.search(clause)
        if not m:
            continue
        if claims(clause):
            return m
        if re.fullmatch(r"[\W_]*", clause[:m.start()] + clause[m.end():]):
            nearby = [clauses[j] for j in (i - 1, i + 1) if 0 <= j < len(clauses)]
            if any(claims(clause + " " + other) for other in nearby):
                return m
    return None

# `+Jo Respect`, `-2 Trust`, `−Relationship`, `(Trust +4)`: a sign, an optional number,
# then a Capitalised name — or a Capitalised name, then a signed number. The capital is
# what keeps "twenty-five" and "a - b" out; a dash between words has spaces round it.
PRINTED_STAT_RE = re.compile(
    r"(?:(?<![\w-])[+\-−]\s?\d*\s?([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2}))"
    r"|(?:\b([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2})\s[+\-−]\d+\b)")


def _canvas_npcs(c, npc_ids):
    """The people a canvas is bound to: `trigger.npc`, `requires_npc`, or a dialog speaker."""
    trig = c.get("trigger") or {}
    out = {v for v in (trig.get("npc"), trig.get("requires_npc"), c.get("requires_npc")) if v}
    for n in c.get("nodes") or []:
        for b in _flat_blocks(n.get("blocks")):
            if b.get("type") == "dialog":
                # `speaker = "npc"` + `npcId` is the house shape (engine.md, dialog block);
                # a bare npc id in `speaker` also renders; "unknown" is a stranger talking.
                props = b.get("props") or {}
                sp = props.get("npcId") or props.get("speaker")
                if sp in npc_ids:
                    out.add(sp)
                elif sp == "unknown":
                    out.add("a stranger")
    return out


def _speech_by_canvas(c):
    """(dialog words, thought_bubble words) on one canvas."""
    said = thought = 0
    for n in c.get("nodes") or []:
        for b in _flat_blocks(n.get("blocks")):
            if not b.get("content"):
                continue
            w = len(str(b["content"]).split())
            if b.get("type") == "dialog":
                said += w
            elif b.get("type") == "thought_bubble":
                thought += w
    return said, thought


def lint_one_time_speaks(game):
    """A one-time step bound to a person, with nobody saying anything.

    `register.md` "The voice — say it loud" rule 5 and L3: the one-time step is where
    the full loud version lives — the reveal, the CONVERSATION, the hook. A one-time
    canvas with a person on it and no `dialog` block has skipped the conversation.
    The PRD asked for this per one-time step because G32 `somebody speaks` is a
    whole-game ratio and cannot see one silent scene inside a talkative game.
    """
    npc_ids = {n.get("id") for n in game.get("npcs") or [] if n.get("id")}
    scope, mute = 0, []
    for c in game.get("canvases") or []:
        if _rep_of(c.get("trigger")):
            continue
        who = _canvas_npcs(c, npc_ids)
        if not who:
            continue
        scope += 1
        said, _ = _speech_by_canvas(c)
        if not said:
            mute.append(f"{c.get('id')} ({', '.join(sorted(who))}) — no dialog block")
    if not scope:
        return "", []
    return f"{len(mute)} of {scope} one-time canvases bound to a person have nobody speaking", mute


FIELD_LONGEST_CHAIN_MEDIAN = 15   # median of each game's longest step chain, 26 corpus games;
                                  # 12 of 26 have one of 15+ (numbers only — the corpus includes
                                  # failing games). SKILL_REVIEW, 2026-09-26.


def lint_arc_ladder(game, state=None):
    """Each person's arc as a chain: the one-time steps written, how many are switched off
    (`is_active = false`), and the longest run where each step's trigger reads a flag or a
    number the step before it sets. `the-arc.md` A1. A LIST, never a score.

    A step belongs to a person when it is bound to them (`trigger.npc` / `requires_npc`) or
    its id carries their short name (`arc_jo_02` is Jo's). Declared ladders
    (`board.characters[].ladder`) print their own step count beside it.
    """
    npcs = [n.get("id") for n in game.get("npcs") or [] if n.get("id")]
    model, _ = build(copy.deepcopy(game))
    sets = {c["id"]: {str(x) for x in (c.get("sets") or [])} for c in model}

    def reads(c):
        out = {str(x) for x in (next((m for m in model if m["id"] == c.get("id")), {}).get("reads") or [])}
        for it in _conditions_of(c.get("trigger") or {}):
            k = it.get("flag_key") or it.get("trait_key") or it.get("flag") or it.get("trait")
            if k:
                out.add(str(k))
        return out

    declared = {who: len(lad.get("steps") or []) for who, lad in _declared_ladders(state)}
    rows, best_all = [], (0, "")
    for npc in npcs:
        short = npc[4:] if npc.startswith("npc_") else npc
        pat = re.compile(rf"(^|_){re.escape(short)}(_|$)")
        steps = [c for c in game.get("canvases") or [] if not _rep_of(c.get("trigger"))
                 and (npc in ((c.get("trigger") or {}).get("npc"), (c.get("trigger") or {}).get("requires_npc"))
                      or pat.search(str(c.get("id") or "")))]
        if not steps:
            continue
        ids = [c.get("id") for c in steps]
        rd = {c.get("id"): reads(c) for c in steps}
        off = sum(1 for c in steps if (c.get("trigger") or {}).get("is_active") is False)

        def longest(s, seen):
            best = [s]
            for t in ids:
                if t not in seen and sets.get(s, set()) & rd[t]:
                    p = [s] + longest(t, seen | {t})
                    if len(p) > len(best):
                        best = p
            return best

        chain = max((longest(i, {i}) for i in ids), key=len)
        if len(chain) > best_all[0]:
            best_all = (len(chain), npc)
        row = (f"{npc}: {len(ids)} one-time step(s)"
               + (f", {off} switched off" if off else "")
               + f" · longest gated chain {len(chain)}"
               + (f" ({chain[0]} → {chain[-1]})" if len(chain) > 1 else ""))
        if npc in declared:
            row += f" · declared ladder {declared[npc]} step(s)"
        rows.append(row)
    if not rows:
        return "", []
    return (f"longest chain {best_all[0]} step(s) ({best_all[1]}) · field median of the longest "
            f"~{FIELD_LONGEST_CHAIN_MEDIAN}"), rows


def lint_scene_ends_on_nothing(game):
    """A one-time scene with a named person that hands the player straight back.

    `register.md` "What a scene contains", test 3 (hook). The scene's last node offers no
    choice — a bare exit — so the only place a hook can live is its last line, and nothing
    here can read a line. A LIST for `v2-reader`, never a verdict: a bare exit whose last
    line points forward is fine.
    """
    npc_ids = {n.get("id") for n in game.get("npcs") or [] if n.get("id")}
    scope, bare = 0, []
    for c in game.get("canvases") or []:
        if _rep_of(c.get("trigger")) or not _canvas_npcs(c, npc_ids):
            continue
        nodes = c.get("nodes") or []
        if not nodes:
            continue
        scope += 1
        if not any((n.get("exit_block") or {}).get("choices") for n in nodes):
            bare.append(f"{c.get('id')}: no node offers a choice; the hook has to be the last line")
    if not scope:
        return "", []
    return f"{len(bare)} of {scope} one-time scenes with a person offer no choice at all", bare


def lint_person_never_speaks(game):
    """A repeatable scene bound to a person — by `trigger.npc` or `requires_npc` — where that
    person never has a line.

    Not `lint_one_time_speaks` (one-time scenes, anyone speaking) and not `no chain ends in
    silence` (quest cards): this is the surface the player returns to, and the person on it
    stays mute. `register.md` "What a scene contains", test 1 (want).
    """
    npc_ids = {n.get("id") for n in game.get("npcs") or [] if n.get("id")}
    scope, mute = 0, []
    for c in game.get("canvases") or []:
        if not _rep_of(c.get("trigger")):
            continue
        trig = c.get("trigger") or {}
        bound = {v for v in (trig.get("npc"), trig.get("requires_npc"), c.get("requires_npc"))
                 if v in npc_ids}
        if not bound:
            continue
        scope += 1
        spoke = set()
        for n in c.get("nodes") or []:
            for b in _flat_blocks(n.get("blocks")):
                if b.get("type") == "dialog":
                    props = b.get("props") or {}
                    spoke.add(props.get("npcId") or props.get("speaker"))
        silent = sorted(bound - spoke)
        if silent:
            mute.append(f"{c.get('id')}: {', '.join(silent)} never speaks")
    if not scope:
        return "", []
    return f"{len(mute)} of {scope} repeatable scenes bound to a person where that person never speaks", mute


def lint_thoughts_over_speech(game):
    """A person is on the canvas, and she thinks more words than anyone says aloud.

    `register.md` rule 3: her thoughts go BESIDE the dialogue, never instead of it.
    G32 counts
    `thought_bubble` as narration game-wide (`_speech_split`); this is the per-canvas
    view of the same inversion, scoped to canvases where somebody could have talked.
    """
    npc_ids = {n.get("id") for n in game.get("npcs") or [] if n.get("id")}
    scope, over = 0, []
    for c in game.get("canvases") or []:
        if not _canvas_npcs(c, npc_ids):
            continue
        said, thought = _speech_by_canvas(c)
        if not (said or thought):
            continue
        scope += 1
        if thought > said:
            over.append(f"{c.get('id')}: {thought} thought words against {said} spoken")
    if not scope:
        return "", []
    return (f"{len(over)} of {scope} canvases with a person and any speech or thought think more "
            f"than they say"), over


def _declared_stat_names(game):
    """Every name a printed stat could honestly refer to, lower-cased: trait keys and
    labels, player and NPC core_traits, NPC flag_keys, and every flag any effect sets."""
    names = set()
    for lab in ((game.get("traits") or {}).get("labels") or []):
        for k in ("key", "label"):
            if lab.get(k):
                names.add(str(lab[k]).lower())
    for owner in [game.get("player") or {}] + list(game.get("npcs") or []):
        names.update(str(k).lower() for k in (owner.get("core_traits") or {}))
        names.update(str(k).lower() for k in (owner.get("flag_keys") or []))
    for _path, d in _walk_paths(game):
        for k in ("flag", "flag_key", "trait", "trait_key"):
            if isinstance(d.get(k), str):
                names.add(d[k].lower())
    return {n.replace("_", " ") for n in names} | names


def lint_printed_stat(game):
    """`+Jo Respect` on a button, or in the prose after it: a score printed on screen.

    `the-meters.md` "What the player is shown": numbers are shown and named (D1), and a `+X`
    for a stat that does not exist is wrong; `register.md` truth rule 4, a consequence printed on a
    button is real. A declared stat is still listed, as a note, until the lint is rebuilt (PRD v2
    phase 4, the printed-stat lint).
    Matches by the LAST words of the printed name, so "+Jo Respect" counts as declared if
    `respect` or `jo respect` is. A list, never a score.
    """
    declared = _declared_stat_names(game)
    hits = []

    def check(cid, text):
        for m in PRINTED_STAT_RE.finditer(text or ""):
            name = (m.group(1) or m.group(2) or "").strip()
            words = name.lower().split()
            if not words:
                continue
            tails = {" ".join(words[i:]) for i in range(len(words))}
            # Under D1 (`the-meters.md` "What the player is shown") a real stat may be shown;
            # it is still listed, marked as real, until phase 4 narrows this lint.
            if tails & declared or {t.replace(" ", "_") for t in tails} & declared:
                hits.append(f"{cid}: \"{m.group(0).strip()}\" prints a real stat (allowed; "
                            f"the engine's toast already shows it)")
            else:
                hits.append(f"{cid}: \"{m.group(0).strip()}\" names no declared trait or flag")

    for c in game.get("canvases") or []:
        for n in c.get("nodes") or []:
            for b in _flat_blocks(n.get("blocks")):
                if b.get("content"):
                    check(c.get("id"), str(b["content"]))
            for ch in _node_choices(n):
                check(c.get("id"), str(ch.get("text") or ""))
    return f"{len(hits)} printed stat label(s) on screen", hits


def lint_past_claim(game):
    """A repeatable screen claims a past the player may not have had.

    `register.md` truth rule 2 and L3: *last night*, *this week*, *again* on a canvas
    that also renders on the first visit is a lie on the first visit. Legal inside a
    `group` whose conditions read the flag or counter that records it, so any sentence
    under a conditioned group is skipped — which is LENIENT: it cannot tell whether the
    condition is the right one. Narration and speech both, because the rewrite this came
    from put the false past in a character's mouth ("Did you eat last night? You didn't").

    A marker counts only in a clause that also holds the player's pronoun and a
    past-tense verb (`_past_claim_clause`, PRD v2 CK4).
    """
    hits, scope = [], 0
    pron_re = _player_pronoun_re(game)

    def walk(cid, blocks, gated):
        nonlocal scope
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            props = b.get("props") or {}
            here = gated or (b.get("type") == "group" and bool(
                (props.get("conditions") or {}).get("items") or b.get("conditions")))
            if b.get("content") and b.get("type") in PROSE_BLOCKS:
                for s in _beat_sentences(str(b["content"])):
                    scope += 1
                    m = _past_claim_clause(s, pron_re)
                    if m and not here:
                        hits.append(f"{cid} [{m.group(0)}]: {s.strip()[:160]}")
            walk(cid, props.get("blocks") or b.get("blocks"), here)
            for beat in props.get("beats") or []:
                walk(cid, beat.get("blocks"), here)

    for c in game.get("canvases") or []:
        if not _rep_of(c.get("trigger")):
            continue
        for n in c.get("nodes") or []:
            walk(c.get("id"), n.get("blocks"), False)
    if not scope:
        return "", []
    return (f"{len(hits)} ungated sentence(s) on repeatable canvases claim a past "
            f"(of {scope} sentences)"), hits


def _opening_flags(game):
    """Every flag the opening sets, on any branch — the state at the handover.

    Reads the starting canvas and, since 2026-09-25, any capstone the funnel walks into
    (F2). Reading the starting canvas alone made `lint_opening_card` report "no quest
    card is visible" on a boot → capstone opening whose capstone set the flag.
    """
    start = (game.get("project") or {}).get("starting_canvas")
    op = next((c for c in game.get("canvases") or [] if c.get("id") == start), None)
    if not op:
        return None
    out = set()
    for path, d in _walk_paths(op):
        if "flagEffects" in path and isinstance(d.get("flag"), str) and d.get("op", "set") == "set":
            out.add(d["flag"])
    _h, walked, _r = _funnel_walk(game)
    return out | (walked or set())


def _card_visible(card, flags, start_traits):
    """Does this card show right after the opening? Unknown conditions count as NOT shown,
    so the lint can only under-report a card, never invent one."""
    for w in card.get("when") or []:
        if not isinstance(w, dict):
            return False
        opn = w.get("op") or w.get("operator")
        if w.get("flag"):
            on = w["flag"] in flags
            if (opn == "is_true" and not on) or (opn == "is_false" and on):
                return False
            if opn not in ("is_true", "is_false"):
                return False
        elif w.get("trait") and (w.get("subject") in (None, "player")):
            cur = start_traits.get(w["trait"], 0)
            val = w.get("value", 0)
            ok = {"lt": cur < val, "lte": cur <= val, "gt": cur > val, "gte": cur >= val,
                  "eq": cur == val, "ne": cur != val}.get(opn)
            if not ok:
                return False
        else:
            return False
    return True


def lint_opening_card(game):
    """The opening ends on a quest card with goal steps.

    `the-first-hour.md` F1b step 5: the first objective is a card with `goals`, so the
    guidance page prints what is done and what is next — 21 of 26 top games give "what
    next" text and it is the players' number-one comment topic (8.4% of all comments, 30 of 30 games).
    Visible = no `when`, or a `when` satisfied by the flags the starting canvas sets and
    the player's starting traits.
    """
    flags = _opening_flags(game)
    if flags is None:
        return "", []
    start_traits = dict(((game.get("player") or {}).get("core_traits")) or {})
    cards = game.get("quest_cards") or []
    shown = [c for c in cards if _card_visible(c, flags, start_traits)]
    with_goals = [c for c in shown if c.get("goals")]
    rows = [f"{c.get('id') or str(c.get('text') or '')[:40]}: "
            f"{'goals ' + str(len(c['goals'])) if c.get('goals') else 'NO goals'}"
            for c in shown]
    if not shown:
        rows = ["no quest card is visible once the opening hands over"]
    verdict = "arms a card with goals" if with_goals else "arms NO card with goals"
    return (f"the opening {verdict} — {len(with_goals)} of {len(shown)} visible card(s) "
            f"carry goals"), rows


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
# Without it, verbs and bare abstractions come through as findings.
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
# already there. It went green only by manufacturing duplicate room screens. A check that cannot see the shape of the thing it
# judges does not measure quality; it manufactures whatever it CAN see.
# ═════════════════════════════════════════════════════════════════════════════

# Room-list labels that open on a determiner and name no verb: "The bench",
# "The counter, before midnight". A player cannot tell what clicking does.
# `the-voice.md` R1 — reported, never gated: any threshold would be invented, and
# this skill has demoted two rules for exactly that.
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
        if not t.get("location") or not _rep_of(t):
            continue
        if t.get("trigger_mode") == "random" or t.get("substitution_only"):
            continue
        if t.get("npc") or t.get("requires_npc"):
            continue                                   # a portrait, not a list row
        nm = (c.get("raw") or {}).get("name")
        if nm:
            out.append((c["id"], c["loc"], nm))
    return out


def _cost_traits_of(canvas):
    """Every trait a canvas charges — trigger costs AND choice costs.

    Separate from the model's `reads` on purpose. `reads` is built from CONDITIONS,
    and a `costs` block is just as much a read: the engine refuses the choice when the
    player cannot afford it (v2.py:12556). The `money gates something` gate already
    makes exactly this correction for the currency; a check that counted only
    conditions would report a system read solely through a price as unread, which is
    the "an instrument that cannot see a thing reports its ABSENCE" failure.

    ⚠️ `costs` is a LIST of {trait, value}, never a dict. Read as a dict it matches
    nothing at all and the check goes quietly, wrongly green.
    """
    out = set()

    def take(cs):
        if isinstance(cs, dict):
            cs = [cs]
        for x in (cs or []):
            if isinstance(x, dict) and isinstance(x.get("trait"), str):
                out.add(x["trait"])

    take(((canvas.get("trigger") or {}).get("costs")))
    for n in (canvas.get("nodes") or []):
        eb = n.get("exit_block") or {}
        take(eb.get("costs"))
        for ch in (eb.get("choices") or []):
            take(ch.get("costs"))
    return out


def lint_labels_and_systems(model, game, state):
    """`the-systems.md` SY1-SY4 — do the declared systems and the room labels agree?

    DECLARE-THEN-CHECK against `board.systems[]` and `board.locations[].labels`, the
    same shape as the `a need shuts a door` gate. Three lists, and a verdict on none
    of them.

    ⚠️ A LINT AND NOT A GATE, and the direction is the whole reason it is safe to
    build. A count is satisfied by declaring more — that is why R2c shipped with no
    check at all, and why `objects` / gate 22 had to be deleted after it manufactured
    duplicate room screens. This one runs the other way:
    declaring another label makes the output WORSE, because an unread label is what it
    prints. Nothing here can be optimised into a pass.

    ⚠️ P0 — never build a check for a state nothing is in. A gate on a field nobody
    declares yet fails every game for the age of the doctrine rather than for anything
    in them. This
    reports "not declared" and moves on; it cannot fail anything.
    """
    if state is None:
        return "", []
    board = (state or {}).get("board") or {}
    systems = [s for s in (board.get("systems") or []) if isinstance(s, dict)]
    locs = [l for l in (board.get("locations") or []) if isinstance(l, dict)]
    room_labels = {str(l.get("id")): {str(x) for x in (l.get("labels") or [])}
                   for l in locs if l.get("id")}
    declared_labels = set().union(*room_labels.values()) if room_labels else set()

    if not systems and not declared_labels:
        return ("no board.systems[] and no room labels declared — the systems step has "
                "not been taken (the-systems.md SY1)"), []

    findings = []

    # 1 · a label on a room that no system names — dead weight.
    claimed = set()
    for s in systems:
        claimed |= {str(x) for x in (s.get("labels") or [])}
    for lid, labs in sorted(room_labels.items()):
        for lab in sorted(labs - claimed):
            findings.append(f"{lid}: label `{lab}` is claimed by no declared system")

    # 2 · a label a system names that no room carries — nowhere to live.
    for s in systems:
        for lab in sorted({str(x) for x in (s.get("labels") or [])} - declared_labels):
            findings.append(f"system `{s.get('id')}`: label `{lab}` is on no location")

    # 3 · a sourced system: fed where it says, and read somewhere else. SY2.
    by_loc = {}
    for c in model:
        by_loc.setdefault(c["loc"], []).append(c)
    for s in systems:
        if str(s.get("kind")) != "sourced":
            continue
        key, sid = str(s.get("key") or ""), s.get("id")
        if not key:
            findings.append(f"system `{sid}`: no `key` — nothing to check it against")
            continue
        fed = [str(x) for x in (s.get("fed_at") or [])]
        if not fed:
            findings.append(f"system `{sid}`: `sourced` with no `fed_at` — say where it is fed")
            continue
        written_at = [f for f in fed if any(key in c["sets"] for c in by_loc.get(f, []))]
        elsewhere = sorted({c["loc"] for c in model
                            if c["loc"] not in fed
                            and (key in c["reads"] or key in _cost_traits_of(c["raw"]))})
        if not written_at:
            findings.append(f"system `{sid}`: nothing at {', '.join(fed)} writes `{key}`")
        if not elsewhere:
            findings.append(f"system `{sid}`: `{key}` is read in no room outside {', '.join(fed)} "
                            f"— a source with no readers (SY2)")

    sourced = sum(1 for s in systems if str(s.get("kind")) == "sourced")
    summary = (f"{len(systems)} systems declared ({sourced} sourced) · "
               f"{len(declared_labels)} distinct labels over {len(room_labels)} rooms · "
               f"{len(findings)} to eyeball")
    return summary, findings


def lint_mute_cards(game):
    """Which guidance cards tell the player nothing, and whose page is silent entirely.

    `renderQuestsGoalBlock` has four frames and falls off the end: a card with no
    `goals` and no `ready_canvas`, not `terminal`, renders its flavour text and then
    RETURNS "" (v2.py:15974-15976). `evaluateGoals` reports `allMet` vacuously for an
    empty list (v2.py:15875-15877), so such a card can never show a 🎯 block at all.

    ⚠️ A LINT AND NOT A GATE, and the engine's own comment is why: that `return ""`
    is annotated "happens for transitional cards between capstones" — a legitimate
    authored shape. The withdrawn "walls state their key" gate fired on 7 of 8 doors in
    a game that was obeying the doctrine; failing every mute card would be the same
    error one surface over.

    What the list is for is the shape the corpus punishes hardest. `in-her-own-hands`
    ships 136 passages for one character and an 881-word hint page whose locked state
    reads "This hint is locked until you have completed another task", and its players
    quote it back — "What task do i do to unlock shauns third task" (13 likes), against
    a top-comment complaint of "Does corruption have to be at a certain level? What's
    needed?" (52). A character EVERY one of whose cards is mute has a section on the
    guidance page that never says anything, which is that failure exactly.
    """
    cards = game.get("quest_cards") or []
    if not cards:
        return "", []
    mute, by_owner = [], collections.defaultdict(list)
    for c in cards:
        owner = c.get("npc_id") or "story"
        silent = (not (c.get("goals") or [])
                  and not c.get("ready_canvas")
                  and not c.get("terminal"))
        by_owner[owner].append(silent)
        if silent:
            mute.append((owner, str(c.get("text") or "")[:60]))
    rows = []
    for owner in sorted(by_owner):
        flags = by_owner[owner]
        if flags and all(flags):
            rows.append(f"{owner}: ALL {len(flags)} cards render no requirement — "
                        f"their section of the page never says what to do")
    for owner, txt in mute[:10]:
        rows.append(f"{owner}: mute card — \"{txt}…\"")
    if not rows:
        return "", []
    return (f"{len(mute)}/{len(cards)} cards render flavour text and no requirement",
            rows)


def lint_doors(model, game):
    """`the-map.md` R6-R6c — every `[locations.door]`, and whether it opens onto anything.

    A DOOR is the threshold screen the player lands on instead of the room: click her
    room and get *knock* rather than walking straight in. Doc 73.

    ⚠️ PRINTS NOTHING when a game declares no door, and that is deliberate. R6 says a
    door is a handful per game — DoL carries SIX named doors in a 15,626-passage game —
    so a row on every doorless game would be noise, and this is a check on a feature,
    never a nudge toward one. The `print(f"  lint · …")` line still exists in the
    source, so `--selfcheck` finds the name either way.

    ⚠️ A LINT AND NOT A GATE, and the direction is why it is safe. Declaring another
    door makes findings 2-4 WORSE, never better — an unreachable door, a door with
    nothing on it, and a knock nobody can answer are what it prints. Nothing here can be
    optimised into a pass, which is the property `objects` / gate 22 lacked.
    """
    doors = [(l.get("id"), l.get("door")) for l in (game.get("locations") or [])
             if isinstance(l.get("door"), dict) and l.get("door")]
    if not doors:
        return "", []

    # Everything any canvas in the game opens — flags AND trait writes, both already
    # folded into the model's per-canvas `sets` (build(), and note the key asymmetry
    # recorded there: an effect names its trait `trait`, a condition `trait_key`).
    opened = set()
    for c in model:
        opened |= set(c["sets"])

    # Who is ever scheduled where. Same walk the walk-in and ambient checks use.
    sched = collections.defaultdict(set)
    for npc in (game.get("npcs") or []):
        for r in (npc.get("schedules") or []):
            loc = r.get("location") or r.get("location_id")
            if loc:
                sched[loc].add(npc.get("id"))

    findings = []
    n_options = 0
    for lid, door in sorted(doors, key=lambda x: str(x[0])):
        options = [o for o in (door.get("options") or []) if isinstance(o, dict)]
        n_options += len(options)

        # 1 · a door no option can ever open, or whose only option opens onto nothing.
        live = []
        for oi, o in enumerate(options):
            keys = [it.get("flag_key") or it.get("trait_key")
                    for it in _conditions_of(o)]
            keys = [k for k in keys if k]
            if not keys or any(k in opened for k in keys):
                live.append(oi)
            elif keys:
                findings.append(
                    f"{lid} options[{oi}] `{str(o.get('text') or '')[:28]}` is gated on "
                    f"{', '.join('`%s`' % k for k in keys if k not in opened)}, which no "
                    f"canvas ever sets — the door does not open onto this")
        if options and not live:
            findings.append(f"{lid}: no option on this door can EVER open (R6)")

        # 2 · a door whose only way through is `enter`. That is not a door, it is a
        #     room with an extra click — the two-click tax R6b is about.
        kinds = [str((o.get("goes_to") or {}).get("type") or "enter") for o in options]
        if kinds and set(kinds) == {"enter"} and len(kinds) == 1:
            findings.append(
                f"{lid}: the only option is `enter` — that is a room with an extra "
                f"click, not a door. Drop the door or give it something to say (R6b)")

        # 3 · a knock nobody can answer.
        for oi, o in enumerate(options):
            for it in _conditions_of(o):
                if it.get("type") != "npc_at_location" or it.get("operator") == "is_absent":
                    continue
                who = it.get("npc_id") or it.get("character_id")
                where = it.get("location_id") or it.get("location") or lid
                if who and who not in sched.get(where, set()):
                    findings.append(
                        f"{lid} options[{oi}] waits for `{who}` at `{where}`, where no "
                        f"schedule row ever puts them — a knock nobody can answer")

        # 4 · R6c. A door belongs to a PERSON'S home; a room the whole cast passes
        #     through is shared, and a shared room takes rows inside, not a threshold.
        #     Reported to eyeball: "shared" is a proxy and only the author can call it.
        if len(sched.get(lid, set())) > 1:
            findings.append(
                f"{lid} is scheduled for {len(sched[lid])} characters "
                f"({', '.join(sorted(sched[lid]))}) — a shared room takes occupancy-gated "
                f"ROWS, not a door (R6c)")

    n_locs = len([l for l in (game.get("locations") or []) if l.get("id")])
    summary = (f"{len(doors)} door(s) on {n_locs} locations · {n_options} option(s) · "
               f"{len(findings)} to eyeball")
    return summary, findings


def lint_unwritten_act(model, game):
    """`the-surfaces.md` R9 — the clicks that change her and show her nothing.

    A choice that targets a LOCATION and fires effects resolves whatever it named
    into a 2-second numeric toast (`v2.py:6239`) and puts the player back on the room
    screen. The approach is written, the outcome is a number, and the act between them
    was never authored.

    ⚠️ THIS IS A LIST AND CANNOT FAIL ANYTHING — LO's call, 2026-09-02, and the reason
    is this: at zero tolerance it reds nearly every game at once, and a scoreboard that
    reds everything stops telling a
    broken game from an unfinished one. The doctrine carries the absolute; this makes
    each game's debt visible.

    ⚠️ IT IS SAFE AS A LINT because authoring MORE of these makes the output worse and
    never better — the property `objects`/gate 22 lacked.

    The split it reports is the actionable one. On a SINGLE-NODE canvas the act is
    definitively unwritten: one screen of approach, then a button. On a multi-node
    canvas the click closes a chain that was written, so it is a departure — still
    time passing with nothing on it, but a different repair.
    """
    rows, single, multi = [], 0, 0
    for c in (game.get("canvases") or []):
        if _is_dev(c):
            continue                                  # dev shortcut — no player reaches it
        nodes = c.get("nodes") or []
        last = nodes[-1].get("id") if nodes else None
        for n in nodes:
            for ch in _node_choices(n):
                if (ch.get("targetType") or "node") != "location" or not _choice_acts(ch):
                    continue
                mins = ch.get("time_progression_minutes") or 0
                closes = len(nodes) > 1 and n.get("id") == last
                if closes:
                    multi += 1
                else:
                    single += 1
                what = []
                for e in (ch.get("effects") or []):
                    t = e.get("trait") or e.get("trait_key")
                    if not t:
                        continue
                    v = e.get("value")
                    # ⚠️ `value` is not always a number. The engine also takes a random
                    # RANGE — `value = { type = "random", min = 2, max = 4 }` — which
                    # games do use. Formatting it as a scalar
                    # raised TypeError and took the whole lint down with it.
                    if isinstance(v, dict):
                        what.append(f"+{v.get('min','?')}..{v.get('max','?')} {t}")
                    elif isinstance(v, (int, float)):
                        what.append(f"{'+' if v >= 0 else ''}{v:g} {t}")
                    else:
                        what.append(str(t))
                for fe in (ch.get("flagEffects") or []):
                    if fe.get("flag"):
                        what.append(str(fe["flag"]))
                rows.append((mins, closes,
                             f"{c.get('id')}.{n.get('id')} \"{str(ch.get('text',''))[:44]}\" — "
                             f"{mins}m, {' '.join(what[:4]) or 'costs only'}"
                             + (" (closes a written chain)" if closes else "")))
    if not rows:
        return "", []
    mins_total = sum(r[0] for r in rows)
    summary = (f"{len(rows)} choice(s) change her and show nothing — "
               f"{mins_total:,}m ({mins_total/60:.1f}h) of game time · "
               f"{single} on a single-screen canvas, {multi} closing a written chain")
    return summary, [r[2] for r in sorted(rows, key=lambda r: -r[0])]


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
    browse (a "Take the car" row), so read WHICH canvases it names
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

    A NUMBER, never a gate. The field's unit is a passage and this engine's is a canvas,
    so no threshold transfers. What reads is the shape: DoL's `Bath` dispatches TWELVE
    outcomes from one activity. A host at exactly one is a coin flip between one branch
    and the base canvas, not a dispatch.

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
        # Four stacked `exposure >= 35/45/55` rules can ALL be true at once — multiplying
        # is right. A walk-in banded `lt 20` / `gte 20 and lt 22` / `gte 22`, where
        # exactly one can ever pass, must not be multiplied — that would report a tiny
        # share for a canvas that renders most of the time. Same TOML shape, two
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
    interiority and counts with narration, which is the point of the gate.
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
    rung of a chain, a canvas is a whole scene, so no single threshold is comparable.
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
               f"· field screens open at vaginal-or-above 46% of the time "
               f"(old rung list — re-measure pending)")
    findings = ([f"{cid} @{loc}: opens on {first} — no rung below it anywhere in the canvas"
                 for cid, loc, first, _ in high[:5]]
                + [f"{cid} @{loc}: never gets past {first} — {len(pres)} rung(s) total"
                   for cid, loc, first, pres in stuck[:5]])
    return summary, findings


def lint_talk_screens(model, game):
    """Screens whose job is a conversation. The genre's second largest content kind.

    Field: 15,774 of 54,630 screens (29%) are two-thirds spoken with one picture.
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

    The loop is the field's own repeatable shape — one `destroyer` act screen (structure
    only; it fails the adults-only rule) is one clip from a pool of eight, four words of
    text, and five exits. Our engine builds it already:
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

    # ⚠️ ONE HOP, when the act node is a pure menu. An act menu can route its rungs to
    # result_* nodes with no prose on the rungs themselves — measuring only the rungs
    # reads that as having no act beats at all, which is the blind spot, not the answer.
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


def _expand_axes(fixed, axes, cap=64):
    """Every string this node can render: `fixed` plus one alternative per axis.

    An axis is a set of mutually exclusive alternatives — a `[group]` if/elseif
    chain, or a `block_pool`'s variants. A node can carry several, and what the
    player sees is one from each, so the renderable set is their cross product.
    Truncated at `cap` combinations: the callers take a MINIMUM over this list and
    a lint that walks 3^12 strings to find it is not worth the wall-clock.
    """
    out = [fixed]
    for axis in axes:
        if not axis:
            continue
        out = [f"{alt} {base}".strip() for base in out for alt in axis][:cap]
    return [x for x in out if x]


def _band_texts(node):
    """One string per VARIANT this node can render, not per authored block.

    A `Beat` folds a node's variants together, on purpose — a Twine passage carries
    all its `<<if>>` branches inline and the DoL baseline was counted that way. But a
    PLAYER sees exactly one, and a finisher scoring six across three bands can put two
    body words on the screen. Measured live: every act node passed while nine finisher
    bands did not.

    ⚠️ `block_pool` IS AN AXIS AND WAS NOT READ AS ONE UNTIL 2026-08-24. Only `group`
    was special-cased; a pool's variants fell through to the always-renders text and
    got concatenated, so a three-variant pool reported the SUM of all three as the
    thinnest thing the node can show. Nothing had used `block_pool` yet, so nothing had
    been wrong yet — this landed with the first pooled act node. It is the same failure
    the beat collector already carries a warning about at the top of this file, where
    whole groups were invisible for the same reason:
    a walker that knows one container type and meets another.

    Adjacent `[group]` blocks merge into ONE if/elseif chain (`engine.md` §35), so all
    the groups at one level are a single axis. Pools are independent of each other and
    of the chain, so each is its own.
    """
    def walk(blocks):
        """-> (always-renders text, [axis, …]); an axis is a list of alternatives."""
        fixed, group_bands, axes = [], [], []
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            props = b.get("props") or {}
            inner = b.get("blocks") or props.get("blocks")
            btype = b.get("type")
            if btype == "group" and inner:
                gf, gaxes = walk(inner)
                group_bands.extend(_expand_axes(gf, gaxes))
                continue
            if btype == "block_pool" and inner:
                variants = []
                for v in inner:
                    vf, vaxes = walk([v])
                    variants.extend(_expand_axes(vf, vaxes))
                if variants:
                    axes.append(variants)
                continue
            if inner:
                sf, saxes = walk(inner)
                if sf:
                    fixed.append(sf)
                axes.extend(saxes)
            if b.get("content") and btype not in MEDIA_BLOCKS:
                fixed.append(str(b["content"]))
        return " ".join(p for p in fixed if p), ([group_bands] if group_bands else []) + axes

    base, axes = walk(node.get("blocks"))
    return _expand_axes(base, axes)


def lint_explicit_volume(slug):
    """How much explicit content is actually IN this game, in absolute terms.

    Every other heat check here is a SHARE with a hand-picked denominator, so a game
    can clear all of them while being nearly empty. Nothing could see that.

    Field (2026-09-01): a median of 457 explicit screens, and 1.24 per 1,000 words.

    ⚠️ READS THE BUILT HTML, and that is deliberate here even though G43 forbids it for
    prose texture. The reason is the same one G43 gives: the engine's build carries UI
    blocks the field's passages do not, so anything computed PER SENTENCE or PER PASSAGE
    is not comparable across the two bases — but *a rate over word count is*. The field
    figures come from `<tw-passagedata>` bodies (`shape.py`), so the game's must too, or
    the bases differ and the comparison is void.

    ⚠️ TWO BASES ARE PRINTED ON PURPOSE, and the difference is the honesty.
      · ALL passages      — matched to how the field number was produced. The primary.
      · CANVAS passages   — the game's canvases only, excluding UI chrome. GENEROUS,
                            unmatched, and therefore an upper bound rather than a
                            fairer figure. A claim about the gap to the field holds on
                            the matched basis ONLY; stating it without the basis
                            overstates it.

    A LINT, never a gate. A gate here would fail games for obeying current doctrine —
    the failure that withdrew R4, study 6's anchoring check and P0. It prints the
    numbers and judges nothing.
    """
    build = os.path.join(os.getcwd(), "games", slug, "output", "index.html")
    if not os.path.exists(build):
        return "", []
    import html as _html
    text = _html.unescape(open(build, encoding="utf-8", errors="replace").read())
    parts = _TW_PASSAGE.findall(text)
    if not parts:
        return "", []

    def measure(keep):
        screens = words = 0
        for name, body in parts:
            if not keep(name):
                continue
            words += len(re.findall(r"[A-Za-z][a-z']+",
                                    re.sub(r"<<.*?>>|<[^>]*>|\[\[.*?\]\]", " ", body)))
            if len(FIELD_BODY.findall(body)) >= 3:
                screens += 1
        return screens, words, (screens / words * 1000 if words else 0.0)

    a_scr, a_wrd, a_rate = measure(lambda n: True)
    c_scr, _, c_rate = measure(lambda n: _CANVAS_NAME.match(n))

    summary = (f"{a_scr} explicit screen(s) over {a_wrd:,} words — {a_rate:.2f} per 1,000 "
               f"(field median {FIELD_EXPLICIT_PER_KW}, p25 {FIELD_EXPLICIT_P25}; "
               f"canvas-only basis {c_rate:.2f} from {c_scr})")
    findings = []
    if a_scr < FIELD_MIN_SCREENS:
        findings.append(f"{a_scr} explicit screens — under {FIELD_MIN_SCREENS}, which is the "
                        f"threshold below which `shape.py` drops a game from the field "
                        f"altogether. It is not in the distribution being compared to.")
    if a_rate < FIELD_EXPLICIT_P25 and c_rate < FIELD_EXPLICIT_P25:
        findings.append(f"below the field's p25 ({FIELD_EXPLICIT_P25}) on BOTH bases "
                        f"({a_rate:.2f} matched, {c_rate:.2f} generous) — the gap is not an "
                        f"artefact of UI chrome in the denominator")
    elif a_rate < FIELD_EXPLICIT_P25 <= c_rate:
        findings.append(f"below p25 on the matched basis ({a_rate:.2f}) but above it on the "
                        f"generous one ({c_rate:.2f}) — report the basis with the number")
    findings.append(f"field median is {FIELD_EXPLICIT_ABS} explicit screens in absolute terms; "
                    f"this game has {a_scr}")
    return summary, findings


def lint_act_nodes(model, game):
    """How crude is the beat the player is actually IN?

    `explicit floor` is a game-WIDE share, and a game can clear it while every act
    node is warm. A percentage cannot see that. This reads the act nodes of
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

    ⚠️ `[engine.daily_tick].traitEffects` IS A WRITER (PRD v2 CK1 · H1, 2026-09-30).
    The engine applies it on every day roll (v2.py:6276-6293; imported at
    template_import.py:3146). The key is camelCase, so the old `effects|[]` suffix
    test never matched it, and a meter the night adds to (`review_days +1`) read as
    one nothing raises. That is the only place the importer reads `traitEffects`,
    so it is matched there and nowhere else.
    """
    out = collections.defaultdict(list)

    def scan(obj, where):
        for path, node in _walk_paths(obj):
            if not ("|".join(path).endswith("effects|[]")
                    or path == ("engine", "daily_tick", "traitEffects", "[]")):
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
    character is called `sex` — so a `sex_stage` written and never read is a
    genuine dead meter the carve-out must not hide.
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
    # A `<npc>_stage` counter is a ladder counter: it records how far a step has come, not
    # how he feels about her (review J6, LO D5). It counts on NEITHER side (PRD v2 CK8b · I14,
    # LO 2026-09-30), even when it is named in `ascent_tiers`. `_ladder_counter_sites` counts
    # what was left out, so the FAIL can say so.
    stages = _engine_read_stage_traits(game)
    player, npc = collections.Counter(), collections.Counter()
    for path, node in _walk_paths(game):
        if "quest_cards" in "|".join(path) or node.get("type") != "trait":
            continue
        key = str(node.get("trait_key") or "")
        if key in stages:
            continue
        if node.get("subject") == "npc":
            npc[f"{node.get('npc_id') or '?'}.{key}"] += 1
        elif key in tiers:
            player[key] += 1
    return player, npc


def _ladder_counter_sites(game):
    """How many trait predicates read a `<npc>_stage` ladder counter (quest cards excluded,
    as in `_school_split`, which leaves these out)."""
    stages = _engine_read_stage_traits(game)
    return sum(1 for path, node in _walk_paths(game)
               if "quest_cards" not in "|".join(path) and node.get("type") == "trait"
               and str(node.get("trait_key") or "") in stages)


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
    named tiers measured the ladder games and printed NOTHING for a roster
    game — half a fork is not an instrument.

    ⚠️ EACH BRANCH GETS ITS OWN FIELD NUMBER, since 2026-08-24. A declared tier is
    judged against player-ascent meters (8-17 rungs); a cast meter against the field's
    per-character willingness meters (2-6, median 3). Printing the ascent number beside
    a roster game told a roster game its 5-rung cast meters were short of 8 when the
    field's per-character median is 3 -- it was already above it.

    A NUMBER, never a bar. A rung count is only comparable between meters on the
    same 0-100 scale, and a game is free to run a two-rung meter on purpose.
    15/35/55/75 is the DoL seed's spacing, one game's, not a ladder to copy.
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
# vocabulary the genre does not use. Rebuilding on 27 added 2,512 words — 18,043 to
# 20,555, of which 1,976 came from those two games — and dropped none: the file is a
# UNION with the old list, never a replacement. (This read "added 1,976" until
# 2026-08-24, which was the sub-figure, not the delta. Count the file.)
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
# Each entry is a common word that misreads badly for most readers.
#
# ⚠️ A WORD `register.md` NAMES AS A DEFECT BELONGS IN HERE. The four additions dated
#    2026-08-23 were all sitting in that file already and in none of this dict:
#    `meter` is the FIRST example in the section ("The words the player has to already
#    own"), and `pitch` and `float` are both in its required-swap list. A false friend is
#    by definition a common word, so `genre_words.txt` can never surface one — if this
#    dict does not carry it, nothing in the instrument does. Reconcile the two on every
#    edit to either.
#
# ⚠️ REJECTED — do not re-propose without new evidence: front, inside, tip, boot, bill,
#    purse — each misreads rarely enough that the false positives cost more than the
#    catch. The bar is not "could be misread" — it is "misreads badly enough to cost the
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
    # Added 2026-08-23. `meter` clashes with the genre's own UI rather than with a
    # dialect: in this genre a meter is a stat bar. Same exposure, unmeasured so far: board, card, flag, state, tier, rung.
    "meter":   "a coin-fed prepayment box here, a stat bar to most players",
    "float":   "the till's starting cash here, something buoyant to most readers",
    "pitch":   "the rent on a trading spot here, a sound or a throw to most readers",
    "chemist": "a pharmacy here, a scientist to most readers",
}
# `half seven` is 7:30 in Britain, 6:30 across much of Europe, and not a construction
# American English uses at all.
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

    Readability scores pass text a reader cannot follow: sentence length and
    syllable count both pass a game whose
    difficulty is REFERENTIAL: `immersion`, `airer`, `chandlery`, `forecourt` are
    short, common-looking words naming objects the reader must already own.

    ⚠️ A LIST AND NEVER A GATE. The rate does not discriminate: a game that reads
    fine and a game that does not can run at similar rates. What separates them is
    what the words ARE. `emitter`
    and `sternum` are built by the fiction; `immersion` and `airer` cannot be,
    because a real object either lands with the reader or it does not. That is a
    judgement, so the check hands over the words and the author makes it.
    `references/register.md`, "The words the player has to already own".

    ⚠️ This takes TEXT, not a parsed game, so the same instrument can run in the
    WANT phase — before a location has been named or a button written. It used to
    be reachable only from a built game, which is one phase too late: by then the
    vocabulary is already set into room names and labels and fixing it means
    renaming things. Run it at WANT/BOARD, before words set into room names.

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
    # A list that hides two thirds of itself is not a list.
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
    # ⚠️ COUNT THE PLURAL TOO. `uses` is a bag of singular tokens, so read `vest` and
    # `vests`.
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

def _hour_slots(rows):
    """{(day, hour)} touched by rows = [(weekdays or None for every day, start, end)].

    An hour counts when any part of it is inside a row; a row past midnight spills into
    the next day (`_ladder_spans`).
    """
    out = set()
    for weekdays, start, stop in rows:
        for d in (range(7) if not weekdays else weekdays):
            for sd, sa, sb in _ladder_spans(d, _pr_mins(start), _pr_end_mins(stop)):
                out |= {(sd, h) for h in range(24) if h * 60 < sb and sa < h * 60 + 60}
    return out


def _trigger_slots(trigger):
    """The hour slots a canvas's own schedule makes it live in; every slot when it has none."""
    scheds = (trigger or {}).get("schedules") or (
        [trigger["schedule"]] if (trigger or {}).get("schedule") else [])
    if not scheds:
        return {(d, h) for d in range(7) for h in range(24)}
    return _hour_slots([(s.get("weekdays"), s.get("start_time", "00:00"),
                         s.get("end_time", "23:59")) for s in scheds])


def _walkin_join(model, game):
    """The activity x schedule JOIN. `the-surfaces.md` R3.

    A location QUALIFIES when she does solo work there AND at least one character
    is scheduled there — then someone can walk in on her. Not a judgement: it is
    already true in the board. Returns (qualifying, covered, rows).

    ⚠️ ALONE MEANS ALONE AT THAT HOUR (PRD v2 CK8c · I11, 2026-09-30). A repeatable not
    bound to a person used to count as solo however full the room was. Now a solo canvas
    counts only if it is live in some hour when NOBODY is scheduled in the room — and the
    room must have somebody scheduled at another hour, or there is nobody to walk in.
    """
    sched = collections.defaultdict(set)
    rows_at = collections.defaultdict(list)
    for npc in (game.get("npcs") or []):
        for r in (npc.get("schedules") or []):
            loc = r.get("location") or r.get("location_id")
            if loc:
                sched[loc].add(npc.get("id"))
                rows_at[loc].append((r.get("weekdays"), r.get("start_time", "00:00"),
                                     r.get("end_time", "23:59")))
    occupied = {loc: _hour_slots(rows) for loc, rows in rows_at.items()}

    solo = collections.defaultdict(list)
    subs = collections.Counter()
    for c in model:
        t = (c.get("raw") or {}).get("trigger") or {}
        loc = t.get("location")
        if not loc or not _rep_of(t):
            continue
        if (t.get("trigger_mode") == "random" or t.get("npc")
                or t.get("requires_npc") or t.get("substitution_only")):
            continue
        if not (_trigger_slots(t) - occupied.get(loc, set())):
            continue                  # somebody is always there when this runs: not alone
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


def _node_choices(node):
    """Every choice on ONE node — `exit_block.choices` AND `exit_block.config.choices`.

    `_exit_holders` does this for a whole canvas; this is the per-node form, needed
    wherever a count is per-screen rather than per-canvas. The `config.choices`
    spelling is legal and rare — reading it just stops a per-node walker having a silent hole
    the canvas-level one does not.
    """
    eb = node.get("exit_block") or {}
    return list(eb.get("choices") or []) + list((eb.get("config") or {}).get("choices") or [])


def _choice_acts(ch):
    """Does this choice CHANGE anything? — the seam `the-surfaces.md` R9 draws.

    A location-target choice that fires nothing is a DOOR: R7's leave-link, written
    to close the beat, and it is navigation. One that grants a trait, sets a flag,
    moves an item, or charges a cost is an ACT that happens to end in a room, and it
    is a decision the player made.

    ⚠️ Both spellings of the item key are read because the generator reads both
    (`v2.py` — `itemEffects` and `item_effects`); authored TOML uses `itemEffects`
    4 times and `item_effects` never.
    """
    return any(ch.get(k) for k in ("effects", "flagEffects", "itemEffects", "item_effects",
                                   "questEffects", "wardrobeEffects", "costs"))


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
    a day: a walk-in guarded by `x_rung_today is_false` that sets it is day-capped, and
    the gate called it "9 clicks, no cap."

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


def _rep_of(trigger):
    """Is a canvas with this trigger repeatable, read the way the ENGINE reads it?

    ⚠️ ONE READING FOR THE WHOLE FILE (2026-09-26, PRD WS5). An absent `is_repeatable`
    means REPEATABLE (`IS_REPEATABLE_DEFAULT`, and `build()` already said so). Eleven
    helpers used to read it as `t.get("is_repeatable")`, which turns an absent key into
    one-time, so a lint and a gate could disagree about the same canvas. Every one of
    them now calls this.
    """
    return bool((trigger or {}).get("is_repeatable", IS_REPEATABLE_DEFAULT))


# ─────────────────────────────────────────────────────────────────────────────
# Presence: is anything in the room when the schedule puts somebody there?
#
# Ported 2026-09-26 (PRD WS5). `standing surface` can read PASS on a game where a face
# is on a bedroom door and the room behind it is empty. The exemptions are not a
# hand-kept table: they are a DECLARED ledger field, `board.characters[].occupancy_rows`,
# each row with its reason, so no game's data sits in this script.
# ─────────────────────────────────────────────────────────────────────────────
_PR_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _pr_mins(hhmm):
    h, _, m = str(hhmm).partition(":")
    try:
        return int(h or 0) * 60 + int(m or 0)
    except ValueError:
        return 0


def _pr_end_mins(hhmm):
    """An END time of "00:00" is midnight, 1440, not 0."""
    return 1440 if str(hhmm).strip() in ("00:00", "24:00") else _pr_mins(hhmm)


def _pr_live_days(row, canvas):
    """Which of the row's weekdays this canvas can appear on (day-precise on purpose:
    one Friday scene must not score a seven-evening row as backed)."""
    days = set(row["weekdays"])
    if not canvas["schedules"]:
        return days

    def spans(start, end):
        # A window that runs past midnight (23:00-08:00) is two spans on the clock.
        a, b = _pr_mins(start), _pr_end_mins(end)
        return [(a, b)] if a < b else [(a, 1440), (0, b)]

    row_spans = spans(row["start_time"], row["end_time"])
    live = set()
    for s in canvas["schedules"]:
        c_spans = spans(s.get("start_time", "00:00"), s.get("end_time", "23:59"))
        if any(ca < rb and ra < cb for ca, cb in c_spans for ra, rb in row_spans):
            live |= days & set(s.get("weekdays") or range(7))
    return live


def _pr_collect(node, test, found):
    if isinstance(node, dict):
        hit = test(node)
        if hit:
            found.add(hit)
        for v in node.values():
            _pr_collect(v, test, found)
    elif isinstance(node, list):
        for v in node:
            _pr_collect(v, test, found)
    return found


def _pr_canvas_facts(canvas):
    t = canvas.get("trigger") or {}
    scheds = t.get("schedules") or ([t["schedule"]] if t.get("schedule") else [])
    speakers = _pr_collect(canvas.get("nodes") or [],
                           lambda d: (d.get("props") or {}).get("npcId"), set())
    addressed = _pr_collect(canvas, lambda d: d.get("npc_id")
                            if (d.get("type") == "npc_at_location"
                                and d.get("operator") == "is_present") else None, set())
    return {
        "id": canvas.get("id"),
        "location": t.get("location") or canvas.get("location"),
        "npc": t.get("npc") or canvas.get("npc"),
        "repeatable": _rep_of(t),
        "random": (t.get("trigger_mode") or "manual") == "random",
        "sub": bool(t.get("substitution_only")),
        "active": t.get("is_active", True) is not False,
        "max_per_day": t.get("max_triggers_per_day"),
        "gated": bool(t.get("conditions")),
        "dev": _is_dev(canvas),
        "schedules": scheds,
        "speakers": speakers,
        "addressed": addressed,
    }


def _pr_twin_rows(scheds):
    """{index of an ungated fallback row: what it falls back from} — structural, so it
    cannot be gamed by naming."""
    out = {}
    for i, s in enumerate(scheds):
        if s.get("when"):
            continue
        window = (tuple(s.get("weekdays", [])), s.get("start_time"), s.get("end_time"))
        for earlier in scheds[:i]:
            if earlier.get("when") and (tuple(earlier.get("weekdays", [])),
                                        earlier.get("start_time"),
                                        earlier.get("end_time")) == window:
                out[i] = f"{earlier.get('location')} {earlier.get('start_time')}-{earlier.get('end_time')}"
                break
    return out


def _declared_occupancy(state):
    """{(npc_id, location, start_time): reason} from board.characters[].occupancy_rows.

    A row whose job is to put a body in a room (asleep, in the bath, blocking a door)
    is backed by that job, not by a canvas. It has to be DECLARED with its reason; an
    exemption the script worked out for itself would grow quietly.
    """
    out = {}
    for ch in (((state or {}).get("board") or {}).get("characters") or []):
        for r in (ch.get("occupancy_rows") or []):
            if ch.get("id") and r.get("location") and r.get("start_time"):
                out[(ch["id"], r["location"], r["start_time"])] = r.get("reason") or "(no reason given)"
    return out


def _schedule_rows_backed(game, state=None):
    """Every [[npcs.schedules]] row, classified per weekday, plus the portrait canvases
    that can never render. Returns a dict of lists: rows, dead, stranded, capped, ladder.

    A row is backed when, on each of its weekdays, standing in that room at those hours
    gives the player something that knows the person is there:
      portrait      a repeatable, non-random, non-substitution canvas bound to her here
      covered       she speaks on such a canvas here, or it asks `npc_at_location is_present`
      substitution  a substitution canvas bound to her here whose HOST is live in these hours
      occupancy     declared in the ledger with its reason, or a structural fallback twin
      DEAD          none of the above, on the weekdays named
    """
    raw = [c for c in (game.get("canvases") or [])]
    facts = [_pr_canvas_facts(c) for c in raw]
    facts = [f for f in facts if not f["dev"]]
    by_loc = collections.defaultdict(list)
    for f in facts:
        by_loc[f["location"]].append(f)
    hosts_of = collections.defaultdict(list)
    for c in raw:
        if _is_dev(c):
            continue
        host = _pr_canvas_facts(c)
        for rule in ((c.get("trigger") or {}).get("substitutions") or []):
            if rule.get("target_canvas_id"):
                hosts_of[rule["target_canvas_id"]].append(host)
    occupancy = _declared_occupancy(state)

    out = dict(rows=[], dead=[], stranded=[], capped=[], ladder=[])
    stands_at = {}
    for npc in game.get("npcs") or []:
        nid = npc.get("id")
        scheds = npc.get("schedules") or []
        stands_at[nid] = {s.get("location") for s in scheds}
        twins = _pr_twin_rows(scheds)
        for i, s in enumerate(scheds):
            row = {"location": s.get("location"),
                   "weekdays": s.get("weekdays", list(range(7))),
                   "start_time": s.get("start_time", "00:00"),
                   "end_time": s.get("end_time", "23:59")}
            key = (nid, row["location"], row["start_time"])
            if key in occupancy:
                verdict, detail, dead_days = "occupancy", occupancy[key], set()
            elif i in twins:
                verdict, detail, dead_days = "occupancy", f"falls back from {twins[i]}", set()
            else:
                want, backed, why, subs, portrait = set(row["weekdays"]), set(), [], [], False
                here = by_loc.get(row["location"], [])
                for c in here:
                    if not c["active"]:
                        continue
                    mine = c["npc"] == nid
                    if mine and c["sub"]:
                        subs.append(c)
                        continue
                    if not c["repeatable"] or c["random"]:
                        continue
                    speaks, asks = nid in c["speakers"], nid in c["addressed"]
                    if not (mine or speaks or asks):
                        continue
                    days = _pr_live_days(row, c)
                    if days:
                        backed |= days
                        why.append(c["id"] + ("" if mine else (" (speaks)" if speaks else " (asks for her)")))
                        portrait = portrait or mine
                if not want - backed:
                    verdict, detail, dead_days = ("portrait" if portrait else "covered"), ", ".join(why), set()
                elif subs and not backed:
                    live = [f"{c['id']} on {h['id']}" for c in subs
                            for h in hosts_of.get(c["id"], []) if _pr_live_days(row, h)]
                    if live:
                        verdict, detail, dead_days = "substitution", ", ".join(live[:3]), set()
                    else:
                        verdict, dead_days = "DEAD", want
                        detail = (f"{', '.join(c['id'] for c in subs)} is bound here but only runs "
                                  f"as a substitution on a host that is not live in these hours")
                else:
                    verdict, dead_days = "DEAD", want - backed
                    detail = (f"{len(here)} canvas(es) at {row['location']}"
                              + (f"; backed only by {', '.join(why)}" if why else ", none of them hers"))
            entry = dict(npc=nid, row=row, verdict=verdict, detail=detail, dead_days=dead_days)
            out["rows"].append(entry)
            if verdict == "DEAD":
                out["dead"].append(entry)

    for f in facts:
        if not (f["npc"] and f["repeatable"] and not f["sub"] and not f["random"]):
            continue
        if f["max_per_day"]:
            (out["ladder"] if (f["gated"] or f["schedules"]) else out["capped"]).append(f)
        if f["location"] not in stands_at.get(f["npc"], set()):
            out["stranded"].append(f)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Money a week can actually bring in (PRD WS5, `the obligation is charged`).
# ─────────────────────────────────────────────────────────────────────────────
def _value_mean_max(val):
    """(mean, max) of an effect value that may be a number or {type="random", min, max}."""
    if isinstance(val, bool):
        return 0.0, 0.0
    if isinstance(val, (int, float)):
        return float(val), float(val)
    if isinstance(val, dict) and val.get("type") == "random":
        lo, hi = val.get("min"), val.get("max", val.get("min"))
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            return (lo + hi) / 2.0, float(hi)
    return 0.0, 0.0


def _week_income(game, currency):
    """What one week can bring in, per source: (mean_total, max_total, rows, uncapped).

    An income source is a positive `add` to the currency on a canvas exit. How often it
    can fire in a week:
      one-time canvas                  once
      capped to once a day             7 × the cap. A cap is `max_triggers_per_day` on the
                                       trigger, or a choice that day-caps itself
                                       (`_holder_day_capped`), or a trigger condition on a
                                       flag the canvas sets and `[engine.daily_tick]` clears.
                                       A trigger schedule narrows it to its weekdays.
      repeatable with no cap           UNCAPPED. Listed, and left out of the totals:
                                       `no free uncapped income` is the gate that owns it.
    MEAN is the verdict because a random pay of 8–25 is not 25 every day. MAX is printed
    beside it. Neither is a promise the player can reach it — only that she cannot beat it.
    """
    cleared = _tick_cleared(game)
    mean_total = max_total = 0.0
    rows, uncapped = [], []
    for c in game.get("canvases") or []:
        if _is_dev(c):
            continue
        t = c.get("trigger") or {}
        # A `substitution_only` canvas only ever renders IN PLACE OF another canvas's visit
        # (v2.py checkAndSubstituteCanvas), so its pay replaces that visit's pay rather than
        # adding a visit. Counting it read one game's week as ~1,950 against 600
        # (PRD v2 CK8b · I9). Since-dated under LO B: `_legacy("sub_income")` is the old count.
        if t.get("substitution_only") and not _legacy("sub_income"):
            continue
        sets_on_canvas = {fe.get("flag") for n in c.get("nodes") or []
                          for h in _exit_holders([n]) for fe in (h.get("flagEffects") or [])
                          if fe.get("op", "set") == "set" and fe.get("flag")}
        # A daily flag anywhere on the canvas caps it: the entry choice reads
        # `streamed_today is_false`, the pay sits on a later node's exit, and that exit sets
        # the flag the day tick clears. Reading only the holder that
        # carries the pay called that stream uncapped. Canvas-wide on purpose: it can only
        # LOWER the ceiling, and a canvas mixing a capped branch with a free one is what
        # `no free uncapped income` is for.
        canvas_reads_false = {it.get("flag_key") for h in [t] + _exit_holders(c.get("nodes") or [])
                              for it in _conditions_of(h)
                              if it.get("operator") in ("is_false", "is_not_true")}
        trig_daily = bool(canvas_reads_false & sets_on_canvas & cleared)
        weekdays = set()
        for s in (t.get("schedules") or ([t["schedule"]] if t.get("schedule") else [])):
            weekdays |= set(s.get("weekdays") or range(7))
        days_per_week = len(weekdays) if weekdays else 7
        # One visit pays through ONE exit, so a capped or one-time canvas contributes its
        # best-paying exit per visit, not the sum of its alternatives (four `act_bar_work`
        # tip choices are four ways to end one shift, not four shifts).
        best_mean = best_max = 0.0
        free = False
        for h in _exit_holders(c.get("nodes") or []):
            pay_mean = pay_max = 0.0
            for ef in (h.get("effects") or []):
                if (ef.get("trait") or ef.get("trait_key")) != currency or ef.get("op") != "add":
                    continue
                mean, mx = _value_mean_max(ef.get("value"))
                if mx > 0:
                    pay_mean += mean
                    pay_max += mx
            if pay_max <= 0:
                continue
            capped = (not _rep_of(t) or t.get("max_triggers_per_day")
                      or _holder_day_capped(h, cleared) or trig_daily)
            if not capped:
                free = True
                uncapped.append(f"{c.get('id')}: +{pay_max:g} with no daily cap")
                continue
            best_mean, best_max = max(best_mean, pay_mean), max(best_max, pay_max)
        if best_max <= 0:
            continue
        if not _rep_of(t):
            times, how = 1, "once"
        else:
            cap = t.get("max_triggers_per_day") or 1
            times, how = days_per_week * cap, f"{cap}/day × {days_per_week} days"
        mean_total += best_mean * times
        max_total += best_max * times
        rows.append(f"{c.get('id')}: +{best_mean:g} (max {best_max:g}) × {times} ({how})"
                    + (" · also has an uncapped exit" if free else ""))
    return mean_total, max_total, rows, uncapped


# ─────────────────────────────────────────────────────────────────────────────
# Can a condition ever come true? (PRD WS5: the door, and the guidance cards)
# ─────────────────────────────────────────────────────────────────────────────
def _flags_ever_set(game):
    """Every flag some effect sets (op `set`), anywhere in the game."""
    out = set()
    for path, d in _walk_paths(game):
        if "flagEffects" in path and isinstance(d.get("flag"), str) and d.get("op", "set") == "set":
            out.add(d["flag"])
    return out


def _cond_parts(item):
    """(kind, key, op, value) for a condition item in either spelling (canvas or card)."""
    op = item.get("operator") or item.get("op")
    if item.get("flag_key") or item.get("flag"):
        return "flag", item.get("flag_key") or item.get("flag"), op, None
    if item.get("trait_key") or item.get("trait"):
        return "trait", item.get("trait_key") or item.get("trait"), op, item.get("value")
    return None, None, op, None


def _cmp(cur, op, val):
    if not isinstance(val, (int, float)):
        return None
    return {"lt": cur < val, "lte": cur <= val, "gt": cur > val, "gte": cur >= val,
            "eq": cur == val, "ne": cur != val}.get(op)


def _cond_state(item, start_flags, start_traits, ever_set, written):
    """('open'|'closed'|'never'|'unknown') for one condition item.

    open     true at the start state
    closed   false at the start, and something in the game can make it true
    never    false at the start, and nothing in the game can ever make it true
    unknown  a condition shape this check does not read (counts as satisfiable)
    """
    kind, key, op, val = _cond_parts(item)
    if kind == "flag":
        on = key in start_flags
        if op in ("is_true",):
            return "open" if on else ("closed" if key in ever_set else "never")
        if op in ("is_false", "is_not_true"):
            return "closed" if on else "open"
        return "unknown"
    if kind == "trait" and (item.get("subject") in (None, "player")):
        cur = start_traits.get(key, 0)
        ok = _cmp(cur, op, val)
        if ok is None:
            return "unknown"
        if ok:
            return "open"
        return "closed" if key in written else "never"
    return "unknown"


# ─────────────────────────────────────────────────────────────────────────────
# Ladders: does each declared step fire when it is unlocked, and can it be unlocked?
#
# Added 2026-09-26 (PRD WS4, `~/Documents/Process_Review_20260925/PRD_SKILL_CHANGES.md`).
# A release can add repeatables and no new step, and no check saw it: nothing here
# knew what a person's steps were. A ladder is now DECLARED in the ledger
# (`board.characters[].ladder`, `references/state.md`), and this compares every declared
# step with the canvas that is supposed to be it. The declaration is not trusted; the
# canvas is read, and any difference between the two is a failure (LO, 2026-09-26).
#
# Two halves, both static:
#   1. the step matches its canvas — place, hours, trigger conditions, the counter it
#      reads (true at N-1, false at N) and the counter it sets (N).
#   2. every unlock is earnable — for each gate item, some scene the player can reach
#      sets that flag or moves that meter, can get it to the value, and is open before
#      the step (its own counter conditions allow a value below N).
# The third half, "the step really fires in a built game", is `playtest.reach_step`,
# run by `--ship`.
# ─────────────────────────────────────────────────────────────────────────────
_LADDER_DAY_NAMES = {d.lower(): i for i, d in enumerate(_PR_DAYS)}


def _ladder_day(d):
    """0-6 (0 = Monday, as the engine and `_PR_DAYS` read it) from an int or a day name."""
    if isinstance(d, int) and not isinstance(d, bool) and 0 <= d <= 6:
        return d
    if isinstance(d, str) and d[:3].lower() in _LADDER_DAY_NAMES:
        return _LADDER_DAY_NAMES[d[:3].lower()]
    return None


def _declared_ladders(state):
    """[(who, ladder)] for every board.characters[] entry that declares a ladder."""
    out = []
    for ch in (((state or {}).get("board") or {}).get("characters") or []):
        lad = ch.get("ladder")
        if isinstance(lad, dict):
            out.append((ch.get("id") or ch.get("name") or "?", lad))
    return out


def _declared_door(state):
    """The door this release ends on: `release_page.door`, else `board.door`, else None.

    The release page is the newer source (PRD WS8) and wins when both exist; `--ship`
    already fails a build whose two copies differ ("the build matches the release page").
    Only a dict with both `canvas` and `choice` counts as declared.
    """
    for door in (((state or {}).get("release_page") or {}).get("door"),
                 ((state or {}).get("board") or {}).get("door")):
        if isinstance(door, dict) and door.get("canvas") and door.get("choice"):
            return door
    return None


def _door_choice(canvas, door):
    """The choice dict on `canvas` whose text is the declared door's, or None."""
    found = None
    for n in (canvas or {}).get("nodes") or []:
        if door.get("node") and n.get("id") != door["node"]:
            continue
        for ch in _node_choices(n):
            if str(ch.get("text") or "").strip() == str(door["choice"]).strip():
                found = ch
    return found


def _opening_canvas_ids(game):
    """Ids of every canvas the opening plays: the starting canvas and the capstones its
    funnel walks into (`_funnel_walk`). A ladder step marked `fires_from = "opening"`
    must be one of these."""
    walked = []
    _funnel_walk(game, walked=walked)
    return {c.get("id") for c in walked if isinstance(c, dict)}


_DAY_WORDS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
              "mon", "tue", "tues", "wed", "thu", "thurs", "fri", "sat", "sun")
_TIME_WORDS = ("weekday", "weekend", "every day", "daily", "each day", "morning",
               "afternoon", "evening", "night", "tonight", "lunch")


def _counter_values(when, counter, top):
    """The counter values 0..top at which a card's `when` can match, reading only the
    items on that counter (the other items are the step's own gate, judged elsewhere)."""
    ops = {"eq": lambda v, x: v == x, "gte": lambda v, x: v >= x, "gt": lambda v, x: v > x,
           "lte": lambda v, x: v <= x, "lt": lambda v, x: v < x}
    items = [w for w in when or [] if isinstance(w, dict) and w.get("trait") == counter
             and (w.get("subject") or "player") == "player"]
    if not items:
        return set()
    vals = set(range(top + 1))
    for w in items:
        f = ops.get(w.get("op"))
        try:
            x = float(w.get("value"))
        except (TypeError, ValueError):
            return set()
        vals = {v for v in vals if f and f(v, x)}
    return vals


def step_hint_problems(game, state):
    """(steps checked, problems) — does every declared ladder step have a quest card that
    is shown exactly while it is the next step, and does that card say where and when?
    None when no ladder is declared. `--ship` REPORT row; `the-voice.md` R2.

    A card matches step n when its counter items admit exactly {n-1} — `eq n-1`, or
    `gte n-1` + `lt n`. Place = the location's name or id in the tip or a goal label;
    time = a day word, a part of the day, or the window's from/to.
    """
    ladders = _declared_ladders(state)
    if not ladders:
        return None
    locs = {l.get("id"): str(l.get("name") or l.get("id")) for l in game.get("locations") or []}
    cards = [c for c in game.get("quest_cards") or [] if isinstance(c, dict)]
    checked, probs = 0, []
    for who, lad in ladders:
        counter = lad.get("counter")
        steps = sorted(lad.get("steps") or [], key=lambda st: st.get("n", 0))
        top = max([st.get("n", 0) for st in steps] + [0])
        for st in steps:
            n, checked = st.get("n"), checked + 1
            mine = [c for c in cards if c.get("npc_id") == who
                    and _counter_values(c.get("when"), counter, top) == {n - 1}]
            if not mine:
                probs.append(f"{who} step {n} ({st.get('canvas')}): no card is shown while it "
                             f"is the next step — generate one with guidance_from_ladder.py")
                continue
            blob = " ".join([str(c.get("tip") or "") for c in mine]
                            + [str(g.get("label") or "") for c in mine
                               for g in c.get("goals") or [] if isinstance(g, dict)]).lower()
            where = st.get("where") or ""
            when = st.get("when") or {}
            place_ok = bool(where) and (where.lower() in blob
                                        or locs.get(where, "\0").lower() in blob)
            # whole words, so "money" is not Monday and "sunset" is not Sunday
            time_ok = (bool(re.search(r"\b(" + "|".join(_TIME_WORDS + _DAY_WORDS) + r")s?\b",
                                      blob))
                       or any(str(when.get(k) or "\0") in blob for k in ("from", "to")))
            missing = [x for x, ok in (("the place", place_ok), ("the time", time_ok)) if not ok]
            if missing:
                probs.append(f"{who} step {n} ({st.get('canvas')}): its card does not name "
                             f"{' or '.join(missing)} (`{where}`, {when.get('from')}–{when.get('to')})")
    return checked, probs


def _ladder_cond_key(item):
    """A comparable key for a condition, in either the canvas spelling or the declared one."""
    kind, key, op, val = _cond_parts(item)
    if kind == "flag":
        return ("flag", key, op or "is_true")
    if kind == "trait":
        npc = item.get("npc_id") or item.get("npc")
        subject = "npc" if (npc or item.get("subject") == "npc") else "player"
        return ("trait", key, op, val, subject, npc)
    return ("other", json.dumps(item, sort_keys=True, default=str))


def _ladder_key_text(k):
    if k[0] == "flag":
        return f"flag {k[1]} {k[2]}"
    if k[0] == "trait":
        who = f"{k[5]}." if k[5] else ""
        return f"{who}{k[1]} {k[2]} {k[3]}"
    return f"condition {k[1]}"


def _ladder_spans(day, a, b):
    """[(day, start, end)] minutes; a window that runs past midnight is two spans."""
    return [(day, a, b)] if a < b else [(day, a, 1440), ((day + 1) % 7, 0, b)]


def _window_uncovered(days, frm, to, rows):
    """The days (0 = Monday) on which the window `frm`-`to` is NOT fully covered by the
    union of `rows` = [(weekdays or None for every day, start, end)].

    FULL cover, not overlap: a person at the place for ten minutes of a two-hour step is
    not there for the step. A window or row that runs past midnight is split into two
    spans (`_ladder_spans`), so "22:00-02:00" is covered by 21:00-23:59 plus 00:00-03:00.
    An end of "23:59" reads as midnight, or those two rows would leave a one-minute gap.
    Shared by `shape.py` (the person is there at the step's hour, PRD v2 CK5 · I13) and,
    from CK8b, the ladder check's person-present test.
    """
    def end(t):
        return 1440 if str(t).strip() == "23:59" else _pr_end_mins(t)

    covered = collections.defaultdict(list)
    for weekdays, start, stop in rows:
        for rd in (range(7) if weekdays is None else weekdays):
            for sd, sa, sb in _ladder_spans(rd, _pr_mins(start), end(stop)):
                covered[sd].append((sa, sb))
    missing = []
    for d in sorted(set(days)):
        for sd, sa, sb in _ladder_spans(d, _pr_mins(frm), end(to)):
            at = sa
            for ra, rb in sorted(covered[sd]):
                if ra <= at < rb:
                    at = rb
                if at >= sb:
                    break
            if at < sb:
                missing.append(d)
                break
    return missing


def _ladder_holders(canvas):
    """Every choice-like holder on a canvas: exit_block.config and each exit choice."""
    for n in canvas.get("nodes") or []:
        eb = n.get("exit_block") or {}
        for h in [eb.get("config") or {}] + list(eb.get("choices") or []):
            if isinstance(h, dict):
                yield h


def _ladder_counter_ok(conds, counter, n):
    """Do this trigger's counter conditions hold at N-1 and shut at N?"""
    cc = [it for it in conds if _ladder_cond_key(it)[:2] == ("trait", counter)
          and _ladder_cond_key(it)[4] == "player"]
    if not cc:
        return f"the trigger does not read the counter {counter} — nothing stops it firing out of order"
    at = lambda v: all(_cmp(v, it.get("operator"), it.get("value")) for it in cc)
    if not at(n - 1):
        return f"its counter conditions are not true at {counter} = {n-1}"
    if at(n):
        return f"its counter conditions are still true at {counter} = {n} — it does not shut after it fires"
    return None


def _ladder_open_below(canvas, counter, n, ever_set, start_flags, start_traits, written):
    """Is this canvas open at some counter value below N, and not shut forever?"""
    trig = canvas.get("trigger") or {}
    conds = list(_conditions_of(trig))
    cc = [it for it in conds if _ladder_cond_key(it)[:2] == ("trait", counter)
          and _ladder_cond_key(it)[4] == "player"]
    if cc and not any(all(_cmp(v, it.get("operator"), it.get("value")) for it in cc)
                      for v in range(0, n)):
        return False
    rest = [it for it in conds if it not in cc]
    return all(_cond_state(it, start_flags, start_traits, ever_set, written) != "never"
               for it in rest)


def _ladder_reachable(canvas, opening_ids=frozenset()):
    """Can the player walk into this canvas at all: not dev, active, and placed.

    A canvas the opening plays (`opening_ids`, from `_opening_canvas_ids`) is reached
    by starting a new game, so it counts although it has no place (PRD v2 CK1 · H3).
    """
    trig = canvas.get("trigger") or {}
    return (not _is_dev(canvas) and trig.get("is_active", True) is not False
            and (bool(trig.get("location") or trig.get("npc"))
                 or canvas.get("id") in opening_ids))


def _ladder_earnable(item, step_canvas_id, counter, n, game, ctx, opening_ids=frozenset()):
    """None if this gate item can be earned before step N, else why not."""
    kind, key, op, val = _cond_parts(item)
    npc = item.get("npc_id") or item.get("npc")
    start_flags, start_traits, ever_set, written = ctx
    open_setters = [c for c in game.get("canvases") or []
                    if c.get("id") != step_canvas_id and _ladder_reachable(c, opening_ids)
                    and _ladder_open_below(c, counter, n, ever_set, start_flags,
                                           start_traits, written)]

    def holders_ok(h):
        return all(_cond_state(it, start_flags, start_traits, ever_set, written) != "never"
                   for it in _conditions_of(h))

    if kind == "flag":
        op = op or "is_true"
        want_on = op not in ("is_false", "is_not_true")
        if (key in start_flags) == want_on:
            return None
        verb = "set" if want_on else "unset"
        for c in open_setters:
            for h in _ladder_holders(c):
                if not holders_ok(h):
                    continue
                for fe in h.get("flagEffects") or []:
                    if fe.get("flag") == key and (fe.get("op") or "set") == verb:
                        return None
        return (f"flag {key} {op}: no scene the player can reach before step {n} "
                f"{'sets' if want_on else 'clears'} it")

    if kind == "trait":
        if npc:
            start = (next((x for x in game.get("npcs") or [] if x.get("id") == npc), {})
                     .get("core_traits") or {}).get(key, 0)
        else:
            start = start_traits.get(key, 0)
        if not isinstance(val, (int, float)) or not isinstance(start, (int, float)):
            return f"{key} {op} {val}: not a number this check can read"
        if _cmp(start, op, val):
            return None
        rising = op in ("gte", "gt", "eq")
        once_total, farm, sets_ok = 0, False, False
        for c in open_setters:
            best = 0
            for h in _ladder_holders(c):
                if not holders_ok(h):
                    continue
                for ef in h.get("effects") or []:
                    if (ef.get("trait") or ef.get("trait_key")) != key:
                        continue
                    tgt = ef.get("targetType", "player")
                    if (npc and (tgt != "npc" or ef.get("npcId") != npc)) or (not npc and tgt != "player"):
                        continue
                    v = ef.get("value")
                    if isinstance(v, dict) and v.get("type") == "random":
                        v = v.get("max", v.get("min"))
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        continue
                    eop = ef.get("op") or "add"
                    if eop == "set":
                        sets_ok = sets_ok or bool(_cmp(v, op, val))
                    elif eop == "add" and ((v > 0) == rising) and v != 0:
                        cap = ef.get("cap")
                        if _farmable(c):
                            if cap is None or _cmp(cap, op, val):
                                farm = True
                        else:
                            best = max(best, abs(v))
            once_total += best
        # The day roll is a farm: `[engine.daily_tick].traitEffects` runs every night,
        # each effect only while its own `conditions` hold (v2.py:6276-6281). A counter
        # item there must be true at some value below N, and nothing else on it may be
        # "never" (PRD v2 CK1 · H1).
        for ef in (((game.get("engine") or {}).get("daily_tick") or {}).get("traitEffects") or []):
            if not isinstance(ef, dict) or (ef.get("trait") or ef.get("trait_key")) != key:
                continue
            tgt = ef.get("targetType", "player")
            if (npc and (tgt != "npc" or ef.get("npcId") != npc)) or (not npc and tgt != "player"):
                continue
            tick_conds = list(_conditions_of(ef))
            on_counter = [it for it in tick_conds if _ladder_cond_key(it)[:2] == ("trait", counter)
                          and _ladder_cond_key(it)[4] == "player"]
            if on_counter and not any(all(_cmp(v, it.get("operator"), it.get("value"))
                                          for it in on_counter) for v in range(0, n)):
                continue
            if any(_cond_state(it, start_flags, start_traits, ever_set, written) == "never"
                   for it in tick_conds if it not in on_counter):
                continue
            v = ef.get("value")
            if isinstance(v, dict) and v.get("type") == "random":
                v = v.get("max", v.get("min"))
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                continue
            eop = ef.get("op") or "add"
            if eop == "set":
                sets_ok = sets_ok or bool(_cmp(v, op, val))
            elif eop == "add" and v != 0 and (v > 0) == rising:
                cap = ef.get("cap")
                if cap is None or _cmp(cap, op, val):
                    farm = True
        if sets_ok or farm:
            return None
        reach = start + once_total if rising else start - once_total
        if _cmp(reach, op, val):
            return None
        return (f"{'npc ' + npc + ' ' if npc else ''}{key} {op} {val}: it starts at {start}, "
                f"and every scene open before step {n} together moves it only to {reach}")
    return f"a gate this check cannot read: {item}"


def ladder_problems(game, state, notes=None):
    """(ladders, steps_checked, problems). ladders == 0 means no ladder is declared.

    Two kinds of step are read differently (PRD v2 CK1, 2026-09-30):
      · THE DOOR STEP — the step whose canvas holds the declared door choice
        (`_declared_door`). The door opens next release by design, so its unlock is not
        judged earnable; the step is noted "the door — opens next release" in `notes`
        (a list the caller passes, appended to) and every other check still runs.
      · AN OPENING STEP — `fires_from = "opening"`. It fires at a new game, not in a
        room, so the place, the hours and the person-present checks are skipped, and
        so is the counter read (the opening plays once, with the counter at 0). It
        must be step 1 and its canvas must be one the opening plays.
    """
    ladders = _declared_ladders(state)
    if not ladders:
        return 0, 0, []
    door = _declared_door(state)
    door_canvas = door.get("canvas") if door else None
    opening_ids = frozenset(_opening_canvas_ids(game))
    canvases = {c.get("id"): c for c in game.get("canvases") or []}
    npcs = {n.get("id"): n for n in game.get("npcs") or []}
    ctx = (_opening_flags(game) or set(),
           dict(((game.get("player") or {}).get("core_traits")) or {}),
           _flags_ever_set(game), set(_player_trait_raises(game)))
    problems, checked = [], 0
    for who, lad in ladders:
        counter = lad.get("counter")
        steps = sorted(lad.get("steps") or [], key=lambda s: s.get("n", 0))
        if not counter:
            problems.append(f"{who}: the ladder names no counter")
            continue
        if not steps:
            problems.append(f"{who}: the ladder declares no steps")
            continue
        if [s.get("n") for s in steps] != list(range(1, len(steps) + 1)):
            problems.append(f"{who}: steps must be numbered 1..{len(steps)} with no gap, "
                            f"got {[s.get('n') for s in steps]}")
            continue
        start = ctx[1].get(counter, 0)
        if start != 0:
            problems.append(f"{who}: {counter} starts at {start}, not 0")
        for st in steps:
            checked += 1
            n, cid = st["n"], st.get("canvas")
            tag = f"{who} step {n} ({cid})"
            c = canvases.get(cid)
            if c is None:
                problems.append(f"{tag}: no canvas with that id")
                continue
            trig = c.get("trigger") or {}
            from_opening = st.get("fires_from") == "opening"
            if st.get("fires_from") not in (None, "opening"):
                problems.append(f"{tag}: fires_from = {st.get('fires_from')!r} — the only "
                                f"value is \"opening\"")
            if from_opening:
                if n != 1:
                    problems.append(f"{tag}: fires_from = \"opening\" on step {n} — the "
                                    f"opening plays once, at the start, so it can only be step 1")
                if cid not in opening_ids:
                    problems.append(f"{tag}: fires_from = \"opening\", but the opening never "
                                    f"plays {cid} — it is not the starting canvas or a "
                                    f"capstone the opening walks into")
            if _is_dev(c):
                problems.append(f"{tag}: it is a dev canvas — a shipped build strips it")
            if trig.get("is_active", True) is False:
                problems.append(f"{tag}: the trigger is not active")
            if not from_opening and trig.get("location") != st.get("where"):
                problems.append(f"{tag}: declared at {st.get('where')}, the canvas fires at "
                                f"{trig.get('location')}")
            # ── hours ──
            when = st.get("when") or {}
            days = [_ladder_day(d) for d in when.get("days") or []]
            frm, to = when.get("from"), when.get("to")
            scheds = trig.get("schedules") or ([trig["schedule"]] if trig.get("schedule") else [])
            if from_opening:
                pass                                   # no room, no clock: a new game
            elif not days or None in days or not frm or not to:
                problems.append(f"{tag}: `when` must be a window — days, from, to — got {when}")
            elif not scheds:
                problems.append(f"{tag}: declared {when}, but the canvas has no hours of its own — "
                                f"it fires at any time")
            else:
                c_days = set()
                bad = []
                for s in scheds:
                    c_days |= set(s.get("weekdays") or range(7))
                    if (s.get("start_time"), s.get("end_time")) != (frm, to):
                        bad.append(f"{s.get('start_time')}-{s.get('end_time')}")
                if bad:
                    problems.append(f"{tag}: declared {frm}-{to}, the canvas's hours are "
                                    f"{', '.join(bad)}")
                if c_days != set(days):
                    problems.append(f"{tag}: declared days {sorted(set(days))}, the canvas fires "
                                    f"on {sorted(c_days)} (0 = Monday)")
            # ── conditions ──
            conds_obj = trig.get("conditions")
            conds = list(_conditions_of(trig))
            if isinstance(conds_obj, dict):
                if str(conds_obj.get("version")) != "1.0":
                    problems.append(f"{tag}: trigger conditions have no version = \"1.0\" — "
                                    f"the engine lets them all through")
                if (conds_obj.get("logic") or "and").lower() not in ("and", "all"):
                    problems.append(f"{tag}: trigger conditions are joined by "
                                    f"{conds_obj.get('logic')}, a step's gate is AND")
            why = None if from_opening else _ladder_counter_ok(conds, counter, n)
            if why:
                problems.append(f"{tag}: {why}")
            actual = {_ladder_cond_key(it) for it in conds
                      if _ladder_cond_key(it)[:2] != ("trait", counter)
                      and not (it.get("flag_key") == "dev_mode_enabled")}
            declared_items = st.get("gate") or []
            declared = {_ladder_cond_key(it) for it in declared_items}
            for k in sorted(actual - declared, key=str):
                problems.append(f"{tag}: the canvas also needs {_ladder_key_text(k)}, "
                                f"which the ladder does not declare")
            for k in sorted(declared - actual, key=str):
                problems.append(f"{tag}: the ladder declares {_ladder_key_text(k)}, "
                                f"which the canvas does not check")
            # ── the counter moves ──
            moves = False
            for h in _ladder_holders(c):
                for ef in h.get("effects") or []:
                    if (ef.get("trait") == counter and ef.get("targetType", "player") == "player"
                            and ((ef.get("op") == "set" and ef.get("value") == n)
                                 or (ef.get("op", "add") == "add" and ef.get("value") == 1))):
                        moves = True
            if not moves:
                problems.append(f"{tag}: no exit sets {counter} to {n} — the ladder stops here")
            # ── the person is there ──
            npc_id = trig.get("npc") if isinstance(trig.get("npc"), str) else None
            if npc_id and days and None not in days and frm and to and not from_opening:
                rows = [r for r in (npcs.get(npc_id) or {}).get("schedules") or []
                        if r.get("location") == st.get("where")]
                if _legacy("full_cover"):
                    # The rule before 2026-09-30: any overlap on the day was enough.
                    a, b = _pr_mins(frm), _pr_end_mins(to)
                    absent = []
                    for d in sorted(set(days)):
                        win = _ladder_spans(d, a, b)
                        hit = False
                        for r in rows:
                            ra, rb = _pr_mins(r.get("start_time", "00:00")), _pr_end_mins(r.get("end_time", "23:59"))
                            for rd in r.get("weekdays") or range(7):
                                for sd, sa, sb in _ladder_spans(rd, ra, rb):
                                    if any(sd == wd and sa < wb and wa < sb for wd, wa, wb in win):
                                        hit = True
                        if not hit:
                            absent.append(_PR_DAYS[d])
                    if absent:
                        problems.append(f"{tag}: bound to {npc_id}, whose schedule does not put them at "
                                        f"{st.get('where')} in {frm}-{to} on {', '.join(absent)}")
                else:
                    # FULL cover (PRD v2 CK8b · H9): ten minutes of him in a two-hour window
                    # is not him being there for the step. `_window_uncovered` is the helper
                    # `shape.py` uses for the same question on the ledger. Since-dated
                    # under LO B (`SHIP_SINCE["full_cover"]`).
                    missing = _window_uncovered(
                        days, frm, to,
                        [(r.get("weekdays") or None, r.get("start_time", "00:00"),
                          r.get("end_time", "23:59")) for r in rows])
                    if missing:
                        problems.append(f"{tag}: bound to {npc_id}, whose schedule does not fully "
                                        f"cover {st.get('where')} {frm}-{to} on "
                                        f"{', '.join(_PR_DAYS[d] for d in missing)}")
            # ── every unlock is earnable ── (not the door's: it opens next release)
            if cid == door_canvas:
                if notes is not None:
                    notes.append(f"{tag}: the door — opens next release")
                continue
            for it in declared_items:
                why = _ladder_earnable(it, cid, counter, n, game, ctx, opening_ids)
                if why:
                    problems.append(f"{tag}: {why}")
    return len(ladders), checked, problems


RESETTING_NAME = re.compile(r"_(today|tonight|week|weekly|daily)$")


def lint_flag_never_resets(game, state):
    """A flag meant to reset — named `*_today` / `*_week` (or `_tonight`, `_daily`,
    `_weekly`), or listed in `board.resetting_flags` — that something sets and nothing
    anywhere unsets, including `[engine.daily_tick]`. Reported, never a gate.

    WHY. A `*_week` flag set on payment, read `is_false` to offer the payment and never
    cleared is paid once per SAVE, not once per week, and every screen that names the
    weekly payment is false from the second week on. The name promised a reset the game
    never runs.

    Walks every dict in the game for `flagEffects`, so a set or unset in a node exit, a
    choice, a cascade beat, a quest effect or the daily tick all count.
    """
    ops = collections.defaultdict(set)

    def walk(obj):
        if isinstance(obj, dict):
            for fe in obj.get("flagEffects") or []:
                if isinstance(fe, dict) and fe.get("flag"):
                    ops[fe["flag"]].add(str(fe.get("op") or "set"))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(game)
    declared = {str(f) for f in (((state or {}).get("board") or {}).get("resetting_flags") or [])}
    stuck = sorted(f for f, o in ops.items()
                   if (RESETTING_NAME.search(f) or f in declared)
                   and o & {"set", "toggle"} and not o & {"unset", "clear", "remove"})
    candidates = sorted(f for f in ops if RESETTING_NAME.search(f) or f in declared)
    if not candidates:
        return "", []
    if not stuck:
        return f"all {len(candidates)} resetting flag(s) are unset somewhere", []
    return (f"{len(stuck)} of {len(candidates)} resetting flag(s) are set and never unset — "
            f"not in any effect, not in [engine.daily_tick]", stuck)


_JOINT_COORD = ("and", "then", "or")
_JOINT_SUBORD = ("because", "so", "since", "though", "although", "while", "whereas",
                 "after", "before", "until", "when", "once")
_GLOSS = re.compile(r", (which (is|was|means)|and that is the|that is the)\b", re.I)


def _joint_prose(game, types=("paragraph", "dialog", "thought_bubble"), locations=True):
    """The prose the joint rates are counted over, on a game dict."""
    out = []

    def walk(blocks):
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") in types and isinstance(block.get("content"), str):
                out.append(block["content"])
            props = block.get("props") or {}
            for beat in props.get("beats") or []:
                walk(beat.get("blocks"))
            walk(props.get("blocks") or block.get("blocks"))

    for canvas in game.get("canvases") or []:
        for node in canvas.get("nodes") or []:
            walk(node.get("blocks"))
    if locations:
        for loc in game.get("locations") or []:
            if isinstance(loc.get("description"), str):
                out.append(loc["description"])
    return " ".join(out)


def _joint_count(text, word):
    return len(re.findall(r"(?<![\w])" + word + r"(?![\w])", text, re.I))


def _joint_profile(text):
    words = len(text.split())
    w = words or 1
    coord = sum(_joint_count(text, x) for x in _JOINT_COORD)
    sub = sum(_joint_count(text, x) for x in _JOINT_SUBORD)
    return {"words": words, "and_1k": _joint_count(text, "and") * 1000 / w,
            "but_1k": _joint_count(text, "but") * 1000 / w,
            "ratio": coord / max(sub, 1), "gloss": len(_GLOSS.findall(text))}


def lint_joints(game):
    """The joints beside the field, and the screens whose sentences run shortest.
    A LIST: `prose has room` judges `but` and `and`; this prints the rest."""
    jp = _joint_profile(_joint_prose(game))
    if jp["words"] < JOINTS_MIN_WORDS:
        return "", []
    lo, med, hi = FIELD_JOINT_RATIO
    summary = (f"coordination ratio {jp['ratio']:.2f} (field p25 {lo} · median {med} · max {hi})"
               f" · {jp['gloss']} `, which is` gloss(es)")
    rows = []
    for canvas in game.get("canvases") or []:
        text = _joint_prose({"canvases": [canvas]}, ("paragraph", "thought_bubble"), False)
        lens = [len(x.split()) for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]
        if len(lens) >= 3:
            rows.append((_median(lens), f"{canvas.get('id')}: median sentence {_median(lens)}"))
    return summary, [r for _, r in sorted(rows)[:5]]


def lint_readable(game):
    """The three checks in scripts/readable.py: (pronoun rows, note), event rows,
    (verbless rows, sentences seen)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import readable
    universal = (_opening_flags(game) or set()) - {
        f for f, ops in _flag_ops(game).items() if ops & {"unset", "clear", "remove"}}
    return readable.dangling(game), readable.unearned_events(game, universal), \
        readable.verbless(game)


def _flag_ops(game):
    ops = collections.defaultdict(set)

    def walk(obj):
        if isinstance(obj, dict):
            for fe in obj.get("flagEffects") or []:
                if isinstance(fe, dict) and fe.get("flag"):
                    ops[fe["flag"]].add(str(fe.get("op") or "set"))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(game)
    return ops


CHEAT_BASICS = (("money", "trait"), ("skip to morning", "next_day"),
                ("the next step now", "play"), ("ask again", "reopen"))


def lint_cheat_page(game):
    """`[ui.cheat_page]` — is there one, and are the four time-savers free? Reported,
    never a gate (`the-systems.md` SY7).

    WHY. The most-liked comment on 8 of the study's 13 core mopoga pages asks for a cheat
    or a code, and a phone player cannot open a console. A basic sold behind a code is
    listed because it is the one thing SY7 says to give away; a missing basic is listed
    because the author may have cut it on purpose ("ask again" in a game whose every "no"
    parks), so it is a list to read, not a failure.
    """
    page = (game.get("ui") or {}).get("cheat_page")
    if not isinstance(page, dict):
        return "none — the most-asked-for feature in the field (the-systems.md SY7)", []
    rows = [g for g in page.get("grants") or [] if isinstance(g, dict)]
    free = [g for g in rows if g.get("free") is True]
    coded = [g for g in rows if g.get("free") is not True]
    have = {g.get("kind") or "trait" for g in free}
    findings = [f"no free '{name}' row" for name, kind in CHEAT_BASICS if kind not in have]
    findings += [f"'{g.get('id')}' ({g.get('kind')}) is a time-saver sold behind a code"
                 for g in coded if (g.get("kind") or "trait") != "trait"]
    return (f"{len(free)} free row(s), {len(coded)} behind a code · "
            f"{4 - sum(1 for _, k in CHEAT_BASICS if k not in have)} of 4 basics free"), findings


def lint_toggles_declared(game, state):
    """`want.toggles` — the content toggles the author declared, and whether anything reads
    them (`the-surfaces.md` R5b.4). Reported, never a gate.

    A toggle is a start-choice flag: the engine has no settings screen, so a flag every
    canvas of that kind reads is the only route. A declared toggle that no canvas reads
    switches nothing, so it is listed. n/a when none is declared — a game may have none.
    """
    toggles = [t for t in ((((state or {}).get("want") or {}).get("toggles")) or [])
               if isinstance(t, dict) and t.get("flag")]
    if not toggles:
        return "n/a — none declared in want.toggles (the-surfaces.md R5b.4)", []
    wanted = {t["flag"] for t in toggles}
    readers = collections.defaultdict(set)

    def walk(obj, cid):
        if isinstance(obj, dict):
            for it in _conditions_of(obj):
                if it.get("flag_key") in wanted:
                    readers[it["flag_key"]].add(cid)
            for v in obj.values():
                walk(v, cid)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, cid)

    for c in (game.get("canvases") or []):
        walk(c, c.get("id") or "?")
    rows = []
    for t in toggles:
        n = len(readers[t["flag"]])
        rows.append(f"{t.get('id') or t['flag']} (`{t['flag']}`): read by {n} canvas(es)"
                    + (" — switches nothing" if not n else ""))
    live = sum(1 for t in toggles if readers[t["flag"]])
    return f"{len(toggles)} declared · {live} read by at least one canvas", rows


def lint_repeatables_without_step(model, state):
    """Repeatables added since the last release with no declared step added. Reported.

    Reads `releases[-1].repeatables` (canvas ids) and `releases[-1].ladder_steps` (a
    count), which a release writes when it ships. With no earlier release it prints the
    baseline, so the next release has something to compare against.
    """
    reps = sorted(c["id"] for c in model if c["rep"] and not c.get("random") and c["beats"])
    steps = sum(len(l.get("steps") or []) for _, l in _declared_ladders(state))
    rels = [r for r in ((state or {}).get("releases") or []) if isinstance(r, dict)]
    last = rels[-1] if rels else None
    if state is None:
        return "", []
    if not last or "repeatables" not in last:
        return (f"first release: {len(reps)} repeatables, {steps} declared steps — "
                f"nothing to compare", [])
    added = [r for r in reps if r not in set(last.get("repeatables") or [])]
    new_steps = steps - int(last.get("ladder_steps") or 0)
    if not added:
        return f"no repeatable added since {last.get('version', 'the last release')}", []
    if new_steps > 0:
        return (f"{len(added)} repeatables and {new_steps} steps added since "
                f"{last.get('version', 'the last release')}", [])
    return (f"{len(added)} repeatables added since {last.get('version', 'the last release')} "
            f"and no declared step", added)


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
      * the click costs at least the SOURCE canvas's own schedule window in time — a
        240-minute shift from a hub open 18:00-22:00 can run once per window (PRD v2
        CK8c · H13). The time is the choice's `time_progression_minutes`, else the
        target node's exit time. A source with no schedule has no window, so no brake.
    """
    by_id = {c["id"]: c for c in (game.get("canvases") or [])}

    def window_minutes(trigger):
        scheds = (trigger or {}).get("schedules") or (
            [trigger["schedule"]] if (trigger or {}).get("schedule") else [])
        spans = [(_pr_end_mins(s.get("end_time", "23:59")) - _pr_mins(s.get("start_time", "00:00")))
                 % 1440 or 1440 for s in scheds]
        return max(spans) if spans else None

    def click_minutes(ch, tgt):
        v = (ch.get("config") or {}).get("time_progression_minutes") or ch.get("time_progression_minutes")
        if v:
            return int(v)
        nid = (ch.get("nodeId") or "").split(".", 1)[1] if "." in (ch.get("nodeId") or "") else None
        for n in by_id[tgt].get("nodes") or []:
            if nid is None or n.get("id") == nid:
                tv = ((n.get("exit_block") or {}).get("config") or {}).get("time_progression_minutes")
                return int(tv) if tv else 0
        return 0
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
                # reads as an unbraked route into every act loop.
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
                win = window_minutes(c.get("trigger"))
                timecap = bool(win) and click_minutes(ch, tgt) >= win
                routes[tgt].append(dict(
                    src=c["id"], costs=bool(costs), perday=perday, selflimit=selflimit,
                    timecap=timecap, reqs=reqs,
                    braked=bool(costs) or perday or selflimit or timecap))
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
# Doctrine: references/the-first-hour.md.  Added 2026-08-22.
# ─────────────────────────────────────────────────────────────────────────────
FUNNEL_DEFAULT_STEP = 3
# v2.py:13200 — `config.get('default_time_progression', 3)`. A node exit that does not
# declare `time_progression_minutes` still costs three minutes, so the handover clock is
# NEVER the starting hour.


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


def _capstone_at(game, loc, minute, flags):
    """The one-time canvas the funnel lands in, if any: F2's boot → capstone.

    `the-first-hour.md` F2 splits the opening into a boot at the start location and a
    capstone at the next one, gated on a flag the boot sets. A walk that stops at the
    boot's location exit judges the boot's hop, not the real handover. So: a canvas at
    `loc` that is non-repeatable, not random, not substitution-only, whose trigger
    conditions are all flag tests the funnel's flags satisfy, and whose schedule window
    (if any) covers `minute`, is the capstone. The weekday is not checked: the opening is
    day one by construction.
    """
    for c in game.get("canvases") or []:
        t = c.get("trigger") or {}
        if t.get("location") != loc or t.get("is_repeatable", True) is not False:
            continue
        if t.get("trigger_mode") == "random" or t.get("substitution_only"):
            continue
        items = list(_conditions_of(t))
        ok = bool(items)
        for it in items:
            fk, opn = it.get("flag_key"), it.get("operator")
            if not fk or opn not in ("is_true", "is_false"):
                ok = False
                break
            if (opn == "is_true") != (fk in flags):
                ok = False
                break
        if not ok:
            continue
        wins = t.get("schedules") or []
        if wins:
            def _m(hhmm):
                h, m = str(hhmm).split(":")
                return int(h) * 60 + int(m)
            if not any(_m(w.get("start_time", "00:00")) <= minute % 1440 < _m(w.get("end_time", "24:00"))
                       for w in wins if isinstance(w, dict)):
                continue
        return c
    return None


def _funnel_walk(game, walked=None):
    """Walk the opening: the starting canvas, and on through any capstone it lands in.

    Returns (handovers, flags, reason). `handovers` is every (clock_minute, location_id)
    at which the funnel really lets go; `flags` is every flag set on any branch of it.
    A BRANCHING walk: an opening with two exits passes if EITHER lands somewhere open.

    Node ids may be bare (`"hall"`) or qualified (`"canvas_opening.hall"`); the engine
    keeps the last segment (`v2.py:13716`) and so does this walk. Before 2026-09-25 a
    qualified id was looked up as-is, found nothing, and the gate read "the funnel never
    exits to a location" on an opening that plainly did (`OPENING_DRAFT.md` §5).
    """
    start = (game.get("project") or {}).get("starting_canvas")
    base = int((game.get("time") or {}).get("starting_hour") or 8) * 60
    op = next((c for c in (game.get("canvases") or [])
               if c.get("id") == start or c.get("name") == start), None)
    if not op:
        return [], None, "no starting canvas is declared"
    if not (op.get("nodes") or []):
        return [], None, "the opening canvas has no nodes"

    out, all_flags = [], set()

    def _set_flags(holder, cfg):
        got = set()
        for h in (holder, cfg):
            for fe in (h.get("flagEffects") or []):
                if isinstance(fe, dict) and fe.get("flag") and fe.get("op", "set") == "set":
                    got.add(fe["flag"])
        return got

    def walk_canvas(canvas, clock0, flags0, visited):
        if walked is not None:
            walked.append(canvas)
        nodes = {n.get("id"): n for n in (canvas.get("nodes") or []) if n.get("id")}
        first = (canvas.get("nodes") or [None])[0]
        if first is None:
            return
        seen, stack = set(), [(first, clock0, frozenset(flags0), 0)]
        while stack:
            node, clock, flags, depth = stack.pop()
            key = (node.get("id"), clock, flags)
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
                if not isinstance(step, (int, float)):
                    step = h.get("time_progression_minutes")
                nxt = clock + (int(step) if isinstance(step, (int, float))
                               else FUNNEL_DEFAULT_STEP)
                now = set(flags) | _set_flags(h, cfg)
                all_flags.update(now)
                nid = str(h.get("nodeId") or cfg.get("nodeId") or "")
                if nid:
                    nid = nid.split(".")[-1]
                    if nid in nodes:
                        stack.append((nodes[nid], nxt, frozenset(now), depth + 1))
                    continue
                loc = cfg.get("locationId") or h.get("locationId")
                if loc:
                    cap = _capstone_at(game, loc, nxt, now)
                    if cap is not None and cap.get("id") not in visited and len(visited) < 6:
                        walk_canvas(cap, nxt, now, visited | {cap.get("id")})
                    else:
                        out.append((nxt, loc))

    walk_canvas(op, base, set(), {op.get("id")})
    return out, all_flags, ("ok" if out else "the funnel never exits to a location")


def _fh_handovers(game):
    """Every (clock_minute, location_id) at which the opening can hand over.

    Follows the boot into its capstone (F2), so the handover judged is the real one.
    Returns ([], reason) when the chain cannot be walked, and the gate then reports n/a:
    an unresolvable walk is an instrument failure, not a defect.
    """
    out, _flags, reason = _funnel_walk(game)
    return out, reason


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
        if _rep_of(t):
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


# ⚠️ NOT BUILT, ON PURPOSE — the self-gating meeting (corpo-life's shape).
#
# The 2026-09-02 field study found that a meeting need not be its own canvas: `corpo-life`
# (1,464 comments) opens *Mia Office Interaction* with `<<if $metmia is 0>>` and gates
# everything after on `$metkaren is 1` — one canvas, first visit is the meeting, every visit
# after is the hub. `become-taxi-driver` and `amore` do the same. F5 allows only the
# separate-canvas shape, so a game using this one reads as cold-spawning when it is not.
#
# A detector for it WAS built and REVERTED the same hour. The rule it used — "the canvas
# branches on a flag it also sets" — is satisfied by every day cap (`x_rung_today`) and by
# arc rungs, so it moved verdicts both ways. Semantically the check has to answer "is this the FIRST contact or the third rung",
# and nothing in the TOML distinguishes them: both read a flag `is_false`, both set it on the
# way out. A lenient version silently passes games that ARE cold-spawning, which is worse
# than under-reporting.
#
# So the second shape is recorded in `the-first-hour.md` F5 as legitimate and is NOT scored.
# An author who builds it should expect this gate to under-report and say so in the ledger.
# Study: ~/Documents/Opening_And_Introduction_Study_20260902/.


def _fh_opening_cast(game):
    """Characters every player meets by playing the opening — its FORCED part.

    The starting canvas and every capstone the funnel walks into (`_funnel_walk`). A
    character counts when a walked canvas binds them (`npc` / `requires_npc`) or when they
    speak on its FIRST node, the screen no branch can skip. A line on a later node is on
    a branch, and a branch is not forced.
    """
    walked = []
    _funnel_walk(game, walked)
    out = set()
    for c in walked:
        t = c.get("trigger") or {}
        out |= {t[k] for k in ("requires_npc", "npc") if t.get(k)}
        first = (c.get("nodes") or [None])[0] or {}
        for b in _fh_blocks(first.get("blocks")):
            nid = (b.get("props") or {}).get("npcId")
            if nid:
                out.add(nid)
    return out


def _fh_cast_met(game):
    """(met, cast, flag_owners, cold) — who is introduced before their hub opens.

    A character counts as MET when either holds:

      (a) at least ONE of their portrait hubs is gated on a flag set by a
          non-repeatable canvas that names them, and NONE of their hubs is completely
          ungated;
      (c) they are named in the forced opening (`_fh_opening_cast`) — every player has
          met them before any hub can open, so an ungated hub is not a cold spawn.

    (a) is the introduction plus the cold-spawn ban — a second hub for the same character
    at another location, with no conditions at all, puts their portrait on a screen
    before the meeting has fired, which is the defect however well the first hub is gated
    (`hub_x`).

    A GROUP meeting counts (LO, 2026-09-28): one non-repeatable scene that names three
    people and sets one flag meets all three. What stays out is a flag set by a scene that
    names nobody (`doors_open`): no character is among that flag's setters, so it opens
    hubs and meets no one. `flag_owners` still reports which flags open several hubs, as
    information.

    ⚠️ (a) is deliberately ANY hub and not EVERY hub. A later rung — a sex loop gated on
    `x_stage gte 3`, an arrangement gated on `y_drinks_done` — is gated on something
    downstream of the meeting, and requiring the meeting flag on it too would fail a
    game for obeying the doctrine.
    """
    setters = _fh_meeting_setters(game)
    hubs = [c for c in (game.get("canvases") or [])
            if (c.get("trigger") or {}).get("npc")
            and _rep_of(c.get("trigger"))
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
    opened = _fh_opening_cast(game) if per_char else set()
    met, cold = [], []
    for npc in sorted(per_char):
        if npc in opened:
            met.append(npc)
            continue
        rows = per_char[npc]
        bare = [cid for cid, _hit, gated in rows if not gated]
        if bare:
            cold.append((npc, bare))
            continue
        if any(hit for _cid, hit, _g in rows):
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
        if not loc or _rep_of(t):
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

    PEOPLE ONLY — a character named in the opening, or on a quest card, or in a
    location description, who has no meeting anywhere.

    ⚠️ There was a PLACES half here and it moved out on 2026-08-26. It asked whether a
    location had a first-visit canvas, which was the wrong question — the answer lives in
    the location's own description. `lint_place_function` below owns places now.

    ⚠️ A LIST AND NEVER A GATE. Whether a name has been earned is a reading, not a
    measurement — a character can be legitimately named in passing (an offstage boss, a
    dead parent) and a corridor legitimately needs no introduction. The check hands over
    the names; the author makes the call.
    """
    npcs = [n for n in (game.get("npcs") or []) if n.get("id")]
    if not npcs:
        return "", []
    # ONE definition of "met" in this file, and it is the gate's. Deriving a looser
    # second one misses a character named on a mid-arc milestone gated long after the
    # hub is in use.
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
    # Collector" searched as "The" matches every sentence, and
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

    if not findings:
        return ("every named character is met before the game uses their name", [])
    return (f"{len(findings)} character(s) named before any meeting — read the list, "
            f"do not read the number"), findings


_ROLE_STOP = {
    "your", "the", "a", "an", "and", "he", "she", "it", "is", "was", "has", "have",
    "who", "that", "his", "her", "you", "him", "them", "they", "of", "to", "in",
    "on", "at", "by", "with", "for", "not", "but", "one", "this", "there",
}


def lint_role_label(game):
    """`npcs[].role` — the label the engine prints under the name. A LIST, never a score.

    `the-first-hour.md` F10. Distinct from `lint_role_stays_attached` below, which measures
    the role ANCHORS IN PROSE and never looks at this field at all — which is why a game
    could carry zero labels and nothing said so.

    Absent is a legal choice (F10: empty renders no line), so this cannot fail anything. It
    exists because the field was invisible rather than declined: `templates/board.toml`
    carried neither `role` nor `relationship` until 2026-09-02, so every author who filled in the template got every
    field it listed and never saw this one.
    """
    npcs = [n for n in (game.get("npcs") or []) if isinstance(n, dict)]
    if not npcs:
        return "", []
    have = [n for n in npcs if (n.get("role") or "").strip()]
    rows = []
    for n in npcs:
        r = (n.get("role") or "").strip()
        if not r:
            rel = " ".join(str(n.get("relationship") or "").split())[:44]
            rows.append(f"{n.get('id')}: no role — the dialogue box prints the bare name"
                        + (f" (relationship: \"{rel}\")" if rel else ""))
    # ⚠️ A RENAMEABLE CHARACTER'S LABEL BELONGS TO THE PLAYER. `relationship_options`
    # renders a listbox: the player decides whether this man is her stepfather, her
    # father or her uncle. A hard-coded label there either contradicts the pick or has
    # to dodge it, which is not what the box is for. `role = "@<npc>.rel"` prints the
    # pick and follows it when they change it (engine.md §43).
    for n in have:
        if n.get("customizable") and (n.get("relationship_options") or []):
            r = n["role"].strip()
            if "@" not in r:
                short = str(n.get("id", "")).replace("npc_", "")
                rows.append(f"{n.get('id')}: role \"{r}\" is hard-coded, but the player picks "
                            f"this relation from {len(n['relationship_options'])} options — "
                            f"use `role = \"@{short}.rel\"` so the label says what they chose")
    # ⚠️ PRINT EVERY DECLARED LABEL, not just the missing ones. Whether a label answers
    # "who is this person" is a reading, not a measurement — no parser can tell `professor`
    # from `the nine-thirty`. Listing them is the only check available, and it costs one line.
    for n in have:
        rows.append(f"{n.get('id')}: \"{n['role'].strip()}\"")
    return f"{len(have)}/{len(npcs)} characters carry a label under the name", sorted(rows)


def lint_role_stays_attached(model, game):
    """After the meeting, do a character's own surfaces still say who he is? — a LIST.

    `the-first-hour.md` F10. F7 gets the role on screen at the meeting; F9 says a place
    keeps saying what it is on every visit. This is F9 for people, and it is the rule
    that was missing: "who is this" is a STANDING question, and a meeting answers it
    once before the player spends forty visits with a bare first name.

    ⚠️ THE INSTRUMENT IS THE POINT, because a version of this WAS TRIED AND REJECTED.
    F7 records it: a fixed KIN-WORD list run over MEETINGS fires wrongly on any cast that
    is not family. The cause is structural — kin words are never going to be there, and
    no amount of tuning a kin list fixes a game it does not describe.

    This one takes its vocabulary from the GAME: the anchors for each character are the
    content words of that character's own `npcs[].relationship` string. A cast of
    colleagues yields "boss" and "shift"; a cast of siblings yields "brother". A game
    that declares no relationships yields nothing and is skipped rather than failed.

    And it counts over that character's OWN canvases, not over meetings.

    ⚠️ A LIST AND NEVER A SCORE. There is no per-character field baseline to hold anyone
    to, and inventing one is what `gates.py` refuses everywhere else. The row speaks for
    itself: "2,594 words of his own, says who he is twice" needs no threshold beside it.
    """
    npcs = game.get("npcs") or []
    anchors = {}
    for n in npcs:
        nid, rel = n.get("id"), str(n.get("relationship") or "")
        if not nid or not rel.strip():
            continue
        head = rel.split(".")[0].lower()
        words = {w for w in re.findall(r"[a-z']+", head)
                 if w not in _ROLE_STOP and len(w) > 2}
        # the character's own NAME is not an anchor — it is the thing being anchored
        words -= {str(n.get("name") or "").lower()}
        if words:
            anchors[nid] = sorted(words)
    if not anchors:
        return "", []

    tally = {k: {"words": 0, "hits": 0, "canvases": 0, "which": collections.Counter()}
             for k in anchors}
    for c in model:
        raw = c.get("raw") or {}
        who = {c.get("npc"), c.get("requires_npc")}
        who |= set(re.findall(r'"npcId":\s*"([^"]+)"', json.dumps(raw)))
        text = _canvas_text(c).lower()
        wc = len(text.split())
        for k in (who & set(anchors)):
            tally[k]["words"] += wc
            tally[k]["canvases"] += 1
            for a in anchors[k]:
                hit = len(re.findall(r"\b" + re.escape(a) + r"\b", text))
                tally[k]["hits"] += hit
                tally[k]["which"][a] += hit

    rows = [(k, v) for k, v in tally.items() if v["words"] >= 200]
    if not rows:
        return "", []
    rows.sort(key=lambda kv: (kv[1]["hits"] / max(kv[1]["words"], 1)))
    by_id = {str(n.get("id")): str(n.get("name") or n.get("id")) for n in npcs}
    findings = []
    for k, v in rows:
        per = round(10000 * v["hits"] / max(v["words"], 1))
        which = ", ".join(f"{a}x{n}" for a, n in v["which"].most_common(3) if n) or "never"
        findings.append(f"{by_id.get(k, k)}: {v['words']:,} words across {v['canvases']} "
                        f"canvases of his own, says who he is {v['hits']}x "
                        f"({per} per 10k) — {which}")
    med = _median([10000 * v["hits"] / max(v["words"], 1) for _, v in rows])
    summary = (f"{len(rows)} character(s) · median {med:.0f} anchor(s) per 10k words in their "
               f"own surfaces · anchors taken from each character's own `relationship` line, "
               f"not from a kin list — read the thinnest row, there is no bar")
    return summary, findings


def lint_place_function(model, game):
    """Does a location's own description say what kind of place it is? — a LIST.

    `the-first-hour.md` F9. The description is the ONLY surface a player sees on every
    visit, so it is where a place has to say what it is and what happens in it.

    ⚠️ THIS REPLACED A GATE (2026-08-26). The gate required a non-repeatable canvas
    bound to the anchor — a first-visit scene. Counted across the 26-game corpus that
    device is ONE game: degrees-of-lewdity, 258 branches and 117 flags, against EIGHTEEN
    games with none at all, destroyer and become-someone and course-of-temptation among
    them. A green board should not depend on the outlier.

    ⚠️ A LIST AND NEVER A SCORE. Whether a description names its function is a reading.
    A thin corridor owes nothing; a room carrying a third of the game does. The order
    carries the judgement the count cannot: heaviest first, with the description's own
    length beside it, so a room where a great deal happens behind two lines of scene-set
    is visible on sight.
    """
    weight = collections.Counter()
    for c in model:
        weight[c["loc"]] += sum(b.words for b in c["beats"])
    visits = _fh_first_visits(game)
    rows = []
    for l in (game.get("locations") or []):
        lid = l.get("id")
        if not lid or not weight[lid]:
            continue          # `location fill` owns a room with no prose at all
        desc = str(l.get("description") or "")
        rows.append((lid, str(l.get("name") or lid), weight[lid],
                     len(desc.split()), bool(visits.get(lid))))
    if not rows:
        return "", []
    rows.sort(key=lambda r: -r[2])
    findings = [
        f"{name}: {w:,} words happen here, described in {d}"
        + (" · has a first visit too" if fv else "")
        for _, name, w, d, fv in rows]
    med = _median([r[3] for r in rows])
    summary = (f"{len(rows)} location(s) · median description {med:.0f} words · "
               f"field room prose per visit, median 82 — read whether each one NAMES "
               f"what the place is, not how long it is")
    return summary, findings


# ─────────────────────────────────────────────────────────────────────────────
# The clock — the time the game promises and the time the engine keeps
# Doctrine: references/the-clock.md.  Added 2026-08-22. The engine has no
# absolute-time advance at all.
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
# `to` is a SEPARATE branch and a narrower one, because bare `to` is a false-positive
# machine. Measured 2026-08-25 against 81,264 action labels from the 27-game corpus:
#   `to` in the shared alternation .......... +8 hits, ALL false  ("Change to 0",
#                                             "Update to 0.3" — sliders and version buttons)
#   `to` + a spelled-out hour ............... +1 false ("restrict myself to one?")
#   `to` + a spelled-out hour, NOT `one` .... +0
# `one` is the same idiom trap _CLK_BAD_NEXT was built for (312 corpus hits of "at one
# point"), and excluding it here loses no reading: `at one` and `till one` are still
# covered by the branch above. The narrow form catches real readings ("Twenty to eight",
# "Ten to six") the lint was missing.
_CLK_WORDNUM_NOT_ONE = "two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
_CLK_PREP = re.compile(
    r"\b(?:"
    r"(?:at|till|until|by|before|after|past|from|gone)\s+"
    r"(?:" + _CLK_HALF + r"|" + _CLK_WORDNUM + r"|\d{1,2})"
    r"|to\s+(?:" + _CLK_HALF + r"|" + _CLK_WORDNUM_NOT_ONE + r")"
    r")\b([^\w]*)(\w+)?", re.I)
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
                # a clock reading takes. The unit nouns below already
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
    a choice "Work the counter (2h 30m)." targets `rung_x.base`, whose exit carries `time_progression_minutes = 150`. Reading only the choice would score
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
    """Every (canvas_record, exit, label) the player can read on a button.

    ⚠️ A NODE'S EXIT COMES IN TWO SHAPES AND THIS READ ONLY ONE OF THEM UNTIL
    2026-08-25. Either the exit_block carries a `choices` array, or it IS the button —
    `{type: "location", text: "...", config: {...}}` with no choices at all. Reading
    only the first misses every button that IS the exit_block — labels invisible because
    nothing looked, not because the pattern was narrow.

    The single exit_block already carries `config.time_progression_minutes`, which is
    the first key `_clk_spent_minutes` reads, so yielding it makes C4's duration half
    work on these labels with no further change.

    The third field of each tuple is the label; the second is whatever object carries
    the spend, and callers must not assume it is a choice dict. The fourth names the
    shape — "choice" or "exit" — so a finding can say which half it came from.
    """
    for c in model:
        for n in c["nodes"]:
            eb = n.get("exit_block") or {}
            chs = eb.get("choices") or []
            for ch in chs:
                t = str(ch.get("text") or ch.get("label") or "")
                if t:
                    yield c, ch, t, "choice"
            if not chs:
                t = str(eb.get("text") or "")
                if t:
                    yield c, eb, t, "exit"


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
    windows typically run hours wide. So a sentence that reads as a clock is wrong for nearly the whole window it
    fires in — unless it is a RULE ("Nobody comes in before eleven in February"), which
    is true at every minute and is correct work.

    ⚠️ A LIST AND NEVER A GATE. Telling a rule from a reading is a reading, not a
    measurement, and a shift-driven world names hours as rules on purpose. A rate gate
    would fail a shift-driven world's rota for obeying the doctrine — SKILL.md's "a check that fails a game for obeying the doctrine is a bug
    in the check". The check hands over the lines and their windows; the author calls it.

    Field basis: median 0.8 clock references per 10,000 words across the 27 parseable
    sandboxes (14.7M words), p75 1.8.

    ⚠️ RE-BASELINED 2026-08-24 BY THE END-OF-STUDY RECHECK, from 1.1 / 2.1 on 25 games.
    `college-daze` and `free-cities` ship the Twine 1 <div id="store-area"> container and
    parsed to ZERO passages until section B taught the parser to read it. Both are
    clock-quiet — 0.25 and 0.27 references per 10k — so the median falls. This is the ONE
    field constant the recheck moved. The old figure reproduced
    EXACTLY on the old 25 using this same `_clk_refs`, so the movement is the corpus and
    not the instrument (`findings_RECHECK.md` §2).

    Re-measured 2026-08-22 on the corrected `_clk_refs` (half-hours, part-of-day phrases,
    quarter-past, and `<hour> the`). The figure moved 1.0 -> 1.1 and p75 held at 2.1: ONE
    field game gained ONE reference, a true positive.
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
    for c, ch, t, _shape in _clk_choices(model):
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
# One click's price can appear six ways and THREE of them are the engine's, not
# the author's (engine.md §33). The measurable part is the
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
    # -- a false green. A sub-unit
    # names its parent currency exactly as the major unit does.
    "pence": "pound", "penny": "pound", "pennies": "pound",
    "cent": "dollar", "cents": "dollar",
    "centime": "euro", "centimes": "euro", "sen": "yen",
}
# ⚠️ "forty per cent" is not money: "down forty per cent" false-positives without
# this guard.
_CUR_PERCENT = re.compile(r"\bper\s*cents?\b", re.I)
_CUR_SYM = re.compile(r"([$£€¥])\s?\d")
_CUR_CODE = re.compile(r"\b(USD|GBP|EUR|JPY)\b", re.I)
_CUR_NUM = (r"\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
            r"fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand")
_CUR_WORD = re.compile(rf"\b(?:{_CUR_NUM})\s+([A-Za-z]+)\b", re.I)


def _cur_extra(currency, declared):
    """Words that name THIS game's currency but no other game's.

    An invented unit is legitimate and the field ships it — `apocalyptic-world`
    prices in caps — but a fixed word list would guess. So the
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
    and taking the first name match
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
    before it. Field: 20%.
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
        (minimum 56%)
      · a money WORD carries an exact amount 20% of the time in the field — a
        spelled-out price is the copy that goes stale when the number moves
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


def _declared_currency(state):
    return (((state or {}).get("board") or {}).get("economy") or {}).get("currency")


def lint_money_channel(model, game, state):
    """HOW money is read — conditions vs prices. A LIST, never a score.

    Gate 16 passes on either channel and that is deliberate: a game that prices its
    choices instead of condition-gating them used to read as "nothing gates on money",
    and that false negative was fixed on 2026-08-14. But the two channels are not the
    same claim and the gate cannot tell them apart:

      · a CONDITION on the currency means content exists that money OPENS
      · a `costs` block means a thing can be BOUGHT

    A game can have zero money conditions and pass gate 16 on the price channel
    alone. The field median is 67.3
    money conditions per 1,000 passages and every measured sandbox has some
    (`the-economy.md` R1). A game at zero is not wrong about prices — it has simply
    never put anything behind the money.

    ⚠️ NOT A GATE, for the same reason the ratio below is not one: a floor cannot be
    defended from what has been measured, and inventing one at n=1 is exactly how the meter doctrine
    went wrong and had to be superseded on 2026-08-19. This prints, and the distribution
    accumulates until a floor can be read off it.
    """
    currency = _declared_currency(state)
    if not currency:
        return ("board.economy.currency not declared — channel not counted", [])

    cond_sites, price_sites = collections.Counter(), collections.Counter()

    def walk(obj, cid):
        if isinstance(obj, dict):
            for it in _conditions_of(obj):
                if it.get("trait_key") == currency:
                    cond_sites[cid] += 1
            for ch in ((obj.get("exit_block") or {}).get("choices") or []):
                cs = ch.get("costs") or []
                if isinstance(cs, dict):
                    cs = [cs]
                if any(isinstance(x, dict) and x.get("trait") == currency for x in cs):
                    price_sites[cid] += 1
            for v in obj.values():
                walk(v, cid)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, cid)

    for c in (game.get("canvases") or []):
        walk(c, c.get("id") or "?")

    n_cond, n_price = sum(cond_sites.values()), sum(price_sites.values())
    summary = (f"`{currency}` is read by {n_cond} condition(s) across "
               f"{len(cond_sites)} canvas(es) and priced by {n_price} choice(s) across "
               f"{len(price_sites)} canvas(es)")
    if not n_cond:
        summary += (" · ⚠ NOTHING is gated on money (warning only — a lint, never a gate) — "
                    "every purchase buys a number, "
                    "and gate 16 passes on the price channel alone")
    rows = [f"{cid}: {n} condition(s) read `{currency}`"
            for cid, n in cond_sites.most_common(12)]
    return summary, rows


def lint_obligation_vs_week(model, game, state):
    """The obligation against what a week actually earns — R3's arithmetic, printed.

    `the-economy.md` R3 has said *"price it against the income channels in both
    directions"* since the file existed. The ledger now has a field for the week —
    `board.economy.week_income` — and this prints the ratio.

    ⚠️ NEVER A GATE. Any threshold fails a game for obeying the doctrine — the error that got the
    anchoring check demoted (2026-08-15) and P0 refused (2026-08-27).
    ⚠️ An undeclared `week_income` reports as UNDECLARED, which is not a pass. An
    absence is not evidence — the same wording the climb and start-choice gates use.
    """
    econ = ((state or {}).get("board") or {}).get("economy") or {}
    amount, week = econ.get("obligation_amount"), econ.get("week_income")
    if not isinstance(amount, (int, float)) or not amount:
        return ("no obligation_amount declared — nothing to price", [])
    if not isinstance(week, (int, float)) or not week:
        return (f"obligation {amount:g} · board.economy.week_income NOT DECLARED — "
                "the ratio cannot be computed, which is not a pass",
                ["the-economy.md R3 — count what a week actually earns and write it "
                 "beside the amount."])
    share = amount / week
    summary = (f"obligation {amount:g} against a declared week of {week:g} — "
               f"{share*100:.0f}% of the week")
    rows = []
    # R3b — a declared moving obligation answers the low-ratio note before it is made.
    # `week_income` is the BASELINE week by definition, so a game whose obligation grows
    # with what the player buys will always read low here, and nagging it would be the
    # check failing a game for obeying the doctrine.
    moves = econ.get("obligation_moves")
    if isinstance(moves, str) and moves.strip():
        rows.append(f"the obligation MOVES (R3b): {moves.strip()}")
        rows.append("the ratio above is the BASELINE week by construction — a moving "
                    "obligation is priced against the week it starts in, not the week "
                    "it ends in")
    elif share < 0.30:
        rows.append("⚠ under a third of the week, and the obligation does not move — "
                    "board.economy.obligation_moves is not declared. Not a failure, but "
                    "the-economy.md R3 is explicit that an obligation trivially paid is "
                    "not pressure either, and R3b is the shape that fixes it without "
                    "raising the number: make it MOVE with what she buys.")
    return summary, rows


def lint_collector_is_target(model, game, state):
    """Is the person who enforces the hold also the person the porn is attached to?

    ⚠️ THE DEFECT THIS EXISTS FOR WAS NEVER WRITTEN IN ANY FILE. Asked for ten
    female-lead concepts, this skill produced ten where a man collects money and the
    sex is how the money gets settled. Grepping `references/`, `SKILL.md` and
    `templates/` for `prostitut|sex work|escort|paid sex|sex for money|instead of
    money` returns ZERO. It is emergent: `the-want.md` §1b used to ask for a
    collector, §4's first charge is "someone with power over her" - which the
    collector already is - and `the-surfaces.md` requires the repeatable surface be
    explicit. Three defensible rules compose into one architecture nobody chose.

    Measured, `~/Documents/Female_Hold_Study_20260904/probe_c.py`: across every field
    game with a bill and a named collector, the collector's share of the game's
    EXPLICIT passages is 0.4-3.8%, and he is never the top figure. `degrees-of-lewdity`
    (numbers only) is the case that settles it - its collector, the character that game is
    half built around, carries 6 of 415 explicit passages (1.4%) against another
    character's 61 (14.7%), who charges her nothing. The field builds the hold and the porn as two systems.

    ⚠️ A LINT, NEVER A GATE, and the reason is in that same sentence: DoL ships
    collector-as-target deliberately and it works. A gate here would fail a game for a
    legitimate design - the error that took R4, study 6's anchoring check and P0 back
    out (see `lint_obligation_vs_week`). So this prints a RANK and a count and invents
    no threshold.

    ⚠️ The unit here is SURFACES, not passages, so the percentage is not directly
    comparable to the field's 0.4-3.8%. The rank is: the field's collector is never #1.
    """
    want = (state or {}).get("want") or {}
    board_econ = ((state or {}).get("board") or {}).get("economy") or {}
    npcs = {n.get("id"): (n.get("name") or n.get("id"))
            for n in (game.get("npcs") or []) if n.get("id")}

    # ── who collects, in declaration order: the ledger, then the engine, then the prose
    collector, source, rows = want.get("hold_collector"), "want.hold_collector", []
    if not collector:
        rent = (game.get("settings") or {}).get("rent") or {}
        if rent.get("collector_npc"):
            collector, source = rent["collector_npc"], "[settings.rent] collector_npc"
    if not collector:
        # Last resort: a proper noun from the cast appearing in the declared hold.
        # A game often names its collector there ("paid to Jo"). An
        # ambiguous match is reported as ambiguous rather than resolved by guessing.
        prose = " ".join(str(x) for x in (want.get("obligation"),
                                          board_econ.get("obligation")) if x)
        named = [nid for nid, nm in npcs.items()
                 if nm and re.search(r"\b" + re.escape(nm) + r"\b", prose, re.I)]
        if len(named) == 1:
            collector, source = named[0], "named in the declared hold"
        elif len(named) > 1:
            rows.append(f"the declared hold names {len(named)} characters "
                        f"({', '.join(npcs[n] for n in named)}) — declare "
                        f"want.hold_collector to say which one enforces it")

    # ── what carries the crude writing: every REPEATABLE canvas that is explicit at
    # all, on the same >= 3 floor `explicit floor` and `lint_act_nodes` use.
    #
    # ⚠️ Deliberately NOT lint_act_nodes' selection, which also requires an act-menu
    # self-loop. That extra clause is right for asking "how crude is the beat the
    # player is standing in", and wrong here: it can select zero canvases in a game
    # full of explicit repeatable surfaces, so the lint returns empty and looks like a
    # pass. The question here
    # is which character the returnable porn is attached to, and a portrait hub with
    # no self-loop is exactly that.
    per_npc, total = collections.Counter(), 0
    for c in model:
        if not c["rep"] or len(EXPLICIT.findall(_canvas_text(c))) < 3:
            continue
        total += 1
        who = c.get("npc") or c.get("requires_npc")
        if not who:
            # Fall back to whoever is on screen: a portrait block's npcId.
            for n in (c.get("nodes") or []):
                blocks = []
                _dialog_blocks(n.get("blocks"), blocks)
                for b in blocks:
                    nid = ((b.get("props") or {}).get("npcId") or "").strip()
                    if nid:
                        who = who or nid
        if who:
            per_npc[who] += 1

    if not total:
        return "", []

    ranked = per_npc.most_common()
    top = ", ".join(f"{npcs.get(n, n)} {k}" for n, k in ranked[:4]) or "nobody"
    # Two denominators, and printing one of them alone reads as a much smaller share
    # than it is: many explicit repeatables (walk-ins, ambients) name no character at
    # all, so a rank is out of the ATTRIBUTED set and a share is out of the whole.
    attributed = sum(per_npc.values())
    basis = (f"{total} explicit repeatable surface(s), {attributed} attributed to a "
             f"character")

    if not collector:
        rows.append("the-want.md §4a — the field's collector carries 0.4–3.8% of the "
                    "explicit passages and is never the top figure. Nothing here can "
                    "check that until the collector is named.")
        return (f"collector NOT DECLARED, which is not a pass · {basis} · {top}", rows)

    mine = per_npc.get(collector, 0)
    rank = next((i + 1 for i, (n, _) in enumerate(ranked) if n == collector), None)
    who = npcs.get(collector, collector)
    summary = (f"collector {who} ({source}) holds {mine} of {attributed} attributed"
               + (f", rank {rank} of {len(ranked)}" if rank else ", carrying none")
               + f" · {basis} · {top}")

    rows.append("field reference: the collector's share of a game's explicit passages "
                "runs 0.4–3.8% and he is NEVER the top figure — degrees-of-lewdity's "
                "collector 6 of 415 (1.4%) against another character's 61 (14.7%), who "
                "charges her nothing")
    if rank == 1:
        rows.append("⚠ the collector is the game's LARGEST explicit surface owner. Not a "
                    "failure — DoL makes its collector both on purpose — but the-want.md §4a: if "
                    "settling the hold IS the repeatable surface, the game has one idea, "
                    "and its ceiling is however many ways she can pay. Check that somebody "
                    "who charges her nothing carries more of it than he does.")
    elif mine == 0:
        rows.append("the collector owns no explicit surface at all. Also a shape — but §4a "
                    "asks for a real character who CAN want her, not an absent one.")
    return summary, rows


def lint_paid_repeatable_deposits(model, game, state):
    """What a PAID repeatable leaves behind — a RATE, never a score.

    `the-economy.md` R1c. The 2026-07-24 field report said *"every repeatable should
    deposit into something"*. That phrasing is too broad to ship: counting every
    repeatable surface sweeps in ambient prose that fires for free, and an ambient is
    SUPPOSED to grant nothing. So this is narrowed to the choices the player actually
    pays for — money, energy, or half an hour or more.

    ⚠️ A pure sink is not a defect (R2 wants sinks). A game made only of pure sinks is.
    ⚠️ NEVER A GATE, and this is the fourth time this file has printed a distribution
    instead of inventing a floor: no threshold has been measured.
    """
    currency = _declared_currency(state)
    paid = deposits = 0
    empty = []

    def choices_of(obj, out):
        if isinstance(obj, dict):
            if isinstance(obj.get("choices"), list):
                out.extend(x for x in obj["choices"] if isinstance(x, dict))
            for v in obj.values():
                choices_of(v, out)
        elif isinstance(obj, list):
            for v in obj:
                choices_of(v, out)

    for c in (game.get("canvases") or []):
        if not _rep_of(c.get("trigger")):
            continue
        found = []
        choices_of(c, found)
        for ch in found:
            costs = ch.get("costs") or []
            if isinstance(costs, dict):
                costs = [costs]
            mins = ch.get("time_progression_minutes") or 0
            if not costs and mins < 30:
                continue
            paid += 1
            if (ch.get("effects") or ch.get("traitEffects")
                    or ch.get("flagEffects") or ch.get("itemEffects")):
                deposits += 1
            elif len(empty) < 12:
                price = next((f"{x.get('value')} {x.get('trait')}" for x in costs
                              if isinstance(x, dict)), f"{mins}m")
                empty.append(f"{c.get('id')}: \"{(ch.get('text') or '')[:44]}\" "
                             f"costs {price} and leaves nothing behind")
    if not paid:
        return ("no paid repeatable choices — nothing to weigh", [])
    rate = deposits / paid
    summary = (f"{deposits} of {paid} paid repeatable choices deposit something "
               f"({rate*100:.0f}%)")
    if not deposits:
        summary += " · ⚠ EVERY paid repeatable in this game is a pure sink"
    rows = empty
    if empty:
        rows.append("R1c — R2 asks whether money leaves; this asks whether anything "
                    "remembers that it left. A thing bought that stays bought is R1b.")
    if currency:
        rows.append(f"currency read as `{currency}`")
    return summary, rows


def lint_price_spelled_out(model, game, state):
    """Priced buttons that do not use a symbol — a LIST.

    `the-economy.md` R7 part 3. Measured across 654 priced link labels in the
    25-game corpus: 94.0% use a SYMBOL, 5.2% spell the unit out, 0.8% use a
    currency code (five labels, all one game).

    ⚠️ A LIST AND NEVER A GATE. An invented unit used consistently — the field's
    `Add 1000 caps` — is not a defect. Consistency
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


def _parked_files(game_dir, state):
    """Every parked TOML fragment for a game: `<game>/parked/**/*.toml` automatically,
    plus any paths or globs the ledger lists in `parked.files` (relative to the game).

    ⚠️ THE FOLDER IS READ WHETHER OR NOT THE LEDGER DECLARES IT (LO, 2026-09-27): a game
    that forgets to declare its parked folder must still be caught.
    """
    import glob as _glob
    if not game_dir:
        return []
    found = set(_glob.glob(os.path.join(game_dir, "parked", "**", "*.toml"), recursive=True))
    for pat in (((state or {}).get("parked") or {}).get("files") or []):
        found.update(_glob.glob(os.path.join(game_dir, str(pat)), recursive=True))
    return sorted(p for p in found if os.path.isfile(p))


def _merge_parked(game, files):
    """A COPY of the game with every parked fragment merged back in: list tables are
    appended, and an entry whose `id` matches a live one replaces it (a parked file may
    hold the fuller version of a live scene). Returns (merged, [(file, error)])."""
    import copy as _copy
    merged, errors = _copy.deepcopy(game), []
    for f in files:
        try:
            frag = _load(f)
        except Exception as exc:                  # a fragment that does not parse is reported
            errors.append((f, str(exc)[:120]))
            continue
        for key, val in frag.items():
            if not isinstance(val, list):
                continue
            live = merged.setdefault(key, [])
            if not isinstance(live, list):
                continue
            ids = {x.get("id"): i for i, x in enumerate(live) if isinstance(x, dict) and x.get("id")}
            for item in val:
                if isinstance(item, dict) and item.get("id") in ids:
                    live[ids[item["id"]]] = item
                else:
                    live.append(item)
    return merged, errors


def _switched_off(game):
    """Ids of the canvases that never play on their own: `is_active = false`, not a dev
    shortcut, and NOT the target of any substitution rule.

    ⚠️ `is_active = false` is not "unaddressable" (`engine.md` §46.3): a dispatcher still
    substitutes an inactive canvas in, so a substitution target is live content and is
    left alone.
    """
    canvases = game.get("canvases") or []
    targets = {sub.get("target_canvas_id") for c in canvases
               for sub in ((c.get("trigger") or {}).get("substitutions") or [])
               if isinstance(sub, dict)}
    return [c.get("id") for c in canvases
            if (c.get("trigger") or {}).get("is_active") is False
            and c.get("id") not in targets and not _is_dev(c)]


def _mark_switched_off(results, model, game, state, info):
    """Switched-off canvases in the tally (LO, 2026-09-28).

    Parked content is taken OUT of the TOML, so a gate cannot see it. A switched-off canvas
    stays IN, and most gates read it as if it plays. So the gates run twice more:
      · AS PLAYED — the switched-off canvases taken out. A gate that PASSES with them
        counted and does not pass as played is a FAIL, noted "passes only if switched-off
        canvases are counted" (`switched_off = "fail"`).
      · ALL ON — the switched-off canvases turned on, for the few gates that skip them. A
        gate that is n/a live and judged with them on is "switched off, not judged"
        (`switched_off = "na"`), counted as not passing, like parked.
    Both land in the tally's fail count, and the tally line prints how many are [off].
    """
    ids = _switched_off(game)
    info["switched_off"] = ids
    if not ids:
        return
    off = set(ids)
    played = copy.deepcopy(game)
    played["canvases"] = [c for c in (played.get("canvases") or []) if c.get("id") not in off]
    on = copy.deepcopy(game)
    for c in (on.get("canvases") or []):
        if c.get("id") in off:
            c.setdefault("trigger", {})["is_active"] = True
    try:
        as_played = {r["gate"]: r for r in run_gates(*build(played), state)}
        all_on = {r["gate"]: r for r in run_gates(*build(on), state)}
    except Exception as exc:
        info["errors"].append(("(switched-off canvases)", f"could not be re-gated — {str(exc)[:120]}"))
        return
    shown = ", ".join(ids[:6]) + (f" and {len(ids) - 6} more" if len(ids) > 6 else "")
    for r in results:
        if r.get("parked"):
            continue
        p, o = as_played.get(r["gate"]), all_on.get(r["gate"])
        if r["pass_"] and p is not None and not p["pass_"]:
            verdict = "n/a" if p["na"] else "too few" if p.get("few") else "FAIL"
            r.update(pass_=False, switched_off="fail",
                     headline=(f"[off] passes only if switched-off canvases are counted — "
                               f"as played: {verdict} · {p['headline']}"),
                     detail=[f"switched off: {shown}"] + list(p.get("detail") or [])[:8])
            info["marked_off"] += 1
        elif r["na"] and o is not None and not o["na"]:
            r.update(na=False, pass_=False, switched_off="na",
                     headline=(f"switched off, not judged — with them on: "
                               f"{'PASS' if o['pass_'] else 'TOO FEW' if o.get('few') else 'FAIL'} · "
                               f"{o['headline']}"),
                     detail=[f"switched off: {shown}"])
            info["marked_off"] += 1


def score(model, game, state=None, game_dir=None):
    """run_gates, plus PARKED, NOT JUDGED (PRD IC21).

    Parking content turned gates n/a, and an n/a leaves the denominator, so taking
    content out RAISED the score — parking can take gates to n/a. So the
    gates run twice: on the live game, and on a copy with the parked content merged
    back in. A gate that is n/a live and JUDGED with the parked content is marked
    parked: never a pass, counted in the denominator, printed with the files.
    Measured, never declared: a gate is only marked parked if the content actually
    judges it. Returns (results, parked_info).
    """
    results = run_gates(model, game, state)
    files = _parked_files(game_dir, state)
    info = dict(files=files, errors=[], marked=0, switched_off=[], marked_off=0)
    if not files:
        _mark_switched_off(results, model, game, state, info)
        return results, info
    merged, info["errors"] = _merge_parked(game, files)
    try:
        m_model, m_game = build(merged)
        with_parked = {r["gate"]: r for r in run_gates(m_model, m_game, state)}
    except Exception as exc:
        info["errors"].append(("(merged game)", f"could not be built — {str(exc)[:120]}"))
        _mark_switched_off(results, model, game, state, info)
        return results, info
    rel = [os.path.relpath(f, game_dir) for f in files]
    for r in results:
        p = with_parked.get(r["gate"])
        if r["na"] and p is not None and not p["na"]:
            r.update(na=False, pass_=False, parked=True,
                     headline=(f"parked, not judged — with the parked content: "
                               f"{'PASS' if p['pass_'] else 'TOO FEW' if p.get('few') else 'FAIL'} · "
                               f"{p['headline']}"),
                     detail=[f"parked content: {', '.join(rel[:6])}"
                             + (f" and {len(rel) - 6} more" if len(rel) > 6 else "")])
            info["marked"] += 1
    _mark_switched_off(results, model, game, state, info)
    return results, info


def tally_counts(results):
    """(passed, failed, parked, few, na, denominator). Parked and too-few count in the
    denominator as NOT passing (LO, 2026-09-27), so neither can ever raise the score.
    n/a stays out: nothing was ever authored to judge."""
    npass = sum(1 for r in results if r["pass_"])
    npark = sum(1 for r in results if r.get("parked"))
    nfew = sum(1 for r in results if r.get("few"))
    nna = sum(1 for r in results if r.get("na"))
    nfail = len(results) - npass - npark - nfew - nna
    return npass, nfail, npark, nfew, nna, len(results) - nna


def run_gates(model, game, state=None):
    R = []

    _N = {}                                        # gate name -> its share's denominator

    def gate(name, ok, headline, detail=None):
        # ok is True / False / None. None means THERE WAS NOTHING TO JUDGE — reported
        # as n/a and excluded from the tally. A gate that "passes" on an empty game
        # flatters it: an absence is not a pass.
        #
        # TOO FEW TO JUDGE (PRD IC21, LO 2026-09-27). A share gate records its
        # denominator in _N just before it is called. A PASS on fewer than FEW_CASES
        # cases is not a pass — `explicit in repeatable` passed "100% of 1" and
        # `milestones open something` 1 of 1. It reports "too few to judge" and counts
        # in the tally as not passing. A FAIL on few cases stays a FAIL: a miss is a miss.
        n = _N.get(name)
        few = name in SHARE_GATES and ok is True and isinstance(n, int) and n < FEW_CASES
        if isinstance(n, int) and f" of {n}" not in headline and f"/{n}" not in headline:
            headline = f"{headline} (n = {n})"
        if few:
            headline = f"too few to judge ({n} of {FEW_CASES}) — {headline}"
        R.append(dict(gate=name, pass_=(ok is True) and not few, na=(ok is None),
                      few=few, n=n, parked=False, headline=headline, detail=detail or []))

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
    # not consulted. `fill` is canonical; `budget` is accepted as an alias. A 300-word corridor is not a defect if you declared a corridor —
    # which is what the-board.md has always said in prose and could not enforce.
    budgets = {}
    for l in ((state or {}).get("board") or {}).get("locations") or []:
        b = l.get("fill", l.get("budget"))
        if isinstance(b, (int, float)) and b > 0:
            budgets[l.get("id")] = float(b)
    # THIS RELEASE'S PLACES (PRD v2 CK9 · H11, 2026-09-30). A place cut from the release
    # keeps its board fill, and summing it put a plan nobody is building into the total, the
    # anchor share and a drift line of its own. With `release_page.places` declared, the
    # budget is judged over those places only (the same read as shape.py row 1).
    rp_places = {p if isinstance(p, str) else (p or {}).get("id")
                 for p in (((state or {}).get("release_page") or {}).get("places") or [])
                 if isinstance(p, (str, dict))}
    cut = sorted(lid for lid in budgets if rp_places and lid not in rp_places)
    if rp_places:
        budgets = {lid: v for lid, v in budgets.items() if lid in rp_places}
    judged = sorted(declared & rp_places) if rp_places else sorted(declared)

    fails = []
    if empty:
        fails.append(f"{len(empty)} declared locations with nothing placed: {', '.join(empty[:12])}")

    # ⚠️ A BUDGET THAT CANNOT BE WRONG IS NOT A BUDGET. A declared figure that is an
    # exact post-hoc word count cannot be wrong, so delivered-vs-declared proves nothing.
    # A plan is written in round numbers before the
    # prose; a record is written in arbitrary ones after it. If the declaration is a
    # record, say so and judge on the backstop instead of crediting a tautology.
    # ⚠️ 50, not 100. At 100 a legitimate 250-granularity plan (9,750 · 5,250 · 4,250 …) was
    # flagged as post-hoc — a false positive on exactly the careful author this is meant to
    # reward. 50 accepts every plan granularity anyone would actually use.
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
        for lid in judged:
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
                f"{len(judged) - len(off)}/{len(judged)} on their own budget · "
                f"anchor {anchor_id} {anchor_pct:.0f}%"
                + (f" · {len(cut)} place(s) cut from this release ignored" if cut else ""))
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

    # ⚠️ REPORTING ONLY — appended to every branch's headline, and judged by NOTHING.
    # A pool renders one of N, so `total` above is words WRITTEN and this is words one
    # pass shows. Gate 1 judges the first on purpose (`the-board.md` §1); the refusal of
    # the proposal to judge the second is recorded on `Beat`. Printed because two numbers
    # that differ by 30% should not be invisible behind a single PASS.
    n_pools, pool_gap = _pool_pass_words(game)
    if n_pools:
        head += f" · {n_pools} pools, {total - pool_gap:,} words per pass"

    _N["location fill"] = len(declared)
    gate("location fill", not fails, head, fails)

    # G2 — explicit floor.
    # ⚠️ A BARE PASS HERE MEANS ALMOST NOTHING, and the headline has to say so.
    # This floor is derived from the reference game's own 7.5-9.3% band — and that
    # game is the COLDEST of 18 shipped sandboxes measured on this same word list
    # (field median 33.3%). A game landing on 7.6% is inside the reference's historical
    # range and still four times colder than its genre. Until a field-comparable threshold exists (see the constant),
    # the honest thing is to print how marginal a marginal pass is.
    # ⚠️ THE DENOMINATOR IS REPEATABLE BEATS, NOT EVERY BEAT. Changed 2026-08-31.
    # This gate used to divide by every beat in the game, which answers "what share of
    # this game's text is explicit?" The question worth asking is "when the player
    # RETURNS to a surface, is it hot?" — and the two diverge the moment a game contains
    # legitimately cold content, because the cold content lands in the denominator.
    #
    # The opening funnel is the largest such block and it is one the author is supposed
    # to build WELL. An opening funnel dilutes an all-beats share on identical prose. That
    # is a live incentive to shorten an opening to move a number, which is the worst
    # available response, and the old denominator rewarded it.
    #
    # ⚠️ The DIRECTION of the gap is the diagnostic, and it is worth reading off the
    # headline. A repeatable share ABOVE the all-beats share means the cold content is
    # in one-shots, where it belongs. BELOW means the heat is in one-shots and the loops
    # are cold — the shape this gate exists to catch.
    #
    # ⚠️ EXPLICIT_BEAT_FLOOR HAS NOT BEEN RE-BASELINED ON THIS DENOMINATOR, and the
    # honest consequence is that the floor is now LENIENT, not strict. The 7.5-9.3% band
    # was measured on the reference game over all its beats; a repeatable-only share is
    # >= an all-beats share for any game whose one-shots are colder than its loops.
    # Re-baselining needs the reference game segmented by repeatability and that has
    # never been done. Until it is, treat a pass here as "not empty", never as "hot" —
    # which is what the BARE PASS note already says.
    rep_beats = [b for c in model if c["rep"] for b in c["beats"]]
    rep_expl = [b for b in rep_beats if b.explicit >= 3]
    pct = 100 * len(rep_expl) / max(len(rep_beats), 1)
    all_pct = 100 * len(expl) / max(len(all_beats), 1)
    marginal = EXPLICIT_BEAT_FLOOR <= pct < 12.0
    _N["explicit floor"] = len(rep_beats)
    gate("explicit floor", None if not rep_beats else pct >= EXPLICIT_BEAT_FLOOR,
         f"{pct:.1f}% of {len(rep_beats):,} REPEATABLE beats carry 3+ explicit words "
         f"(floor {EXPLICIT_BEAT_FLOOR}%)"
         f" · {all_pct:.1f}% of all {len(all_beats):,} beats [reported, not judged]"
         + ("  ← BARE PASS" if marginal else ""),
         [f"{len(rep_expl)} explicit beats on re-enterable surfaces, {len(expl)} in the game — "
          f"the floor is the reference game's own band, and that game is the coldest of 18 "
          f"measured sandboxes",
          "clearing this floor is not evidence of heat; it is evidence of not being empty"]
         if marginal else [])

    # G3 — explicit content lives where the player returns
    rep_expl = sum(1 for c in model for b in c["beats"] if b.explicit >= 3 and c["rep"])
    share = 100 * rep_expl / max(len(expl), 1)
    worst = collections.Counter()
    for c in model:
        if not c["rep"]:
            worst[c["loc"]] += sum(1 for b in c["beats"] if b.explicit >= 3)
    _N["explicit in repeatable"] = len(expl)
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
    _N["repeatable explicit media cycles"] = pooled + len(fixed)
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
    _N["an explicit beat carries a clip"] = len(expl_beats)
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
             "the field puts one clip every ~58 words of explicit prose (IQR 25-104)",
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
    # `thought_bubble` counts as narration on purpose — the bubble was for the NPC's
    # interior in the first place.
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
    _N["traversal heat"] = len(declared)
    gate("traversal heat", heat_pct >= LOCATIONS_WITH_HEAT,
         f"{len(hot_locs)}/{len(declared)} locations ({heat_pct:.0f}%) carry a cycling explicit pool "
         f"(floor {LOCATIONS_WITH_HEAT:.0f}%)",
         [", ".join(cold[:30])] if cold else [])

    # G6 — every character is findable where and when the schedule puts her.
    #
    # ⚠️ REWRITTEN 2026-09-26 (PRD WS5). The old check asked two questions per character —
    # is ANY canvas bound to her anywhere, and does she have ANY schedule row — and never
    # asked whether the two are in the same room at the same time. It could read PASS on a
    # game where her face was on the bedroom door and the room behind it was empty,
    # passing her on a substitution-only canvas that can never render a portrait. The rule
    # below is a ported presence check: every schedule row is judged per weekday, and a portrait canvas bound to a
    # room its person never stands in, or capped per day on its trigger, is listed too.
    # Rows whose job is only to put a body in a room are declared, with the reason, in
    # board.characters[].occupancy_rows. See `_schedule_rows_backed`.
    npcs = game.get("npcs") or []
    if not npcs:
        gate("standing surface", None, "no [[npcs]] — nobody to find")
    else:
        pres = _schedule_rows_backed(game, state)
        bad = []
        for e in pres["dead"]:
            r = e["row"]
            bad.append(f"DEAD {e['npc']} @{r['location']} {r['start_time']}-{r['end_time']} "
                       f"on {' '.join(_PR_DAYS[d] for d in sorted(e['dead_days']) if 0 <= d < 7)}"
                       f" — {e['detail']}")
        for f in pres["stranded"]:
            bad.append(f"STRANDED {f['id']} @{f['location']}: {f['npc']} is never scheduled "
                       f"there, so this portrait cannot render")
        for f in pres["capped"]:
            bad.append(f"DAY-CAPPED {f['id']} @{f['location']}: max_triggers_per_day on the "
                       f"trigger deletes the person after one click — cap the choice instead "
                       f"(engine.md §28)")
        unsched = [n.get("id") for n in npcs if not (n.get("schedules") or [])]
        for nid in unsched:
            bad.append(f"{nid}: no schedule rows — she stands nowhere")
        n_rows = len(pres["rows"])
        _N["standing surface"] = n_rows
        gate("standing surface", not bad,
             f"{n_rows - len(pres['dead'])}/{n_rows} schedule rows have something in the room "
             f"on every weekday · {len(pres['stranded'])} stranded · "
             f"{len(pres['capped'])} day-capped portraits",
             bad)

    # G7 — every milestone must open something standing, directly OR down a chain.
    # Transitive on purpose: an opening funnel legitimately runs one-shot -> one-shot,
    # and only the END of that chain has to land on standing content. Flagging every
    # link would punish a shape the genre uses everywhere.
    # Random ambients are excluded — a one-shot random scene is texture, not a milestone,
    # and is not supposed to open anything.
    # A read inside the story text counts here (a callback line on the daily card is the
    # skill's own shape for a first-time step: `the-arc.md` A1, `register.md` L3).
    # A read that is only `is_false` does not count (LO, 2026-09-26, PRD WS4): a line that
    # shows while the flag is still off is not something the milestone opened.
    reads_of = {c["id"]: (c["reads"] | c.get("text_reads", set()))
                - c.get("neg_only_reads", set()) for c in model}
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
            dead.append(f"{c['id']} sets no flag — opens nothing. A first time on a card "
                        f"that already exists passes by setting a flag its daily card reads, "
                        f"e.g. a callback group")
    _N["milestones open something"] = len(milestones)
    gate("milestones open something", None if not milestones else not dead,
         f"{len(milestones)-len(dead)} of {len(milestones)} milestones open standing content",
         dead[:25])

    # G7b — every declared step matches its canvas, and every unlock can be earned.
    # n/a until a ladder is declared; `--ship` is where an undeclared ladder is red.
    # See `ladder_problems` (PRD WS4, 2026-09-26).
    lad_notes = []
    n_lad, n_steps, lad_probs = ladder_problems(game, state, notes=lad_notes)
    _N["ladders move forward"] = n_steps
    gate("ladders move forward", None if not n_lad else not lad_probs,
         (f"{n_steps} declared steps across {n_lad} ladder(s), {len(lad_probs)} problem(s)"
          + "".join(f" · {t}" for t in lad_notes)
          if n_lad else "no ladder declared in board.characters[].ladder"),
         lad_probs[:25])

    # G8 — no meter may rise past the content it can buy.
    # A meter's PROMISED ceiling is the top band the player can see on the sidebar
    # (sidebar_items[].bands[]).
    #
    # A FALLING METER IS NOT A CLIMB (PRD v2 CK3 · H5, 2026-09-30). A meter that starts
    # full and drains (`clean` at 100 with a "90+" band) failed "bands promise something
    # at 90": the player starts in that band, so nothing has to buy it. Two exemptions:
    # the band holding the meter's STARTING value is not a promise, and a meter declared
    # `falling = true` in [[traits.labels]] is not judged at all. `falling` is read here
    # only; the importer keeps just its own label keys (template_import.py:3324-3335).
    tops = collections.defaultdict(int)
    for c in model:
        for k, op, v in c["traits"]:
            if isinstance(v, (int, float)) and op in ("gte", "gt", "eq"):
                tops[k] = max(tops[k], int(v))
    falling = {l.get("key") for l in ((game.get("traits") or {}).get("labels") or [])
               if isinstance(l, dict) and l.get("falling") is True}
    npc_start = {n.get("id"): (n.get("core_traits") or {}) for n in (game.get("npcs") or [])}
    over = []
    for item in (game.get("sidebar_items") or []):
        key = item.get("trait")
        bands = item.get("bands") or []
        if not key or not bands or key not in tops or key in falling:
            continue
        start = (npc_start.get(item["npc_id"], {}) if item.get("npc_id")
                 else ((game.get("player") or {}).get("core_traits") or {})).get(key, 0)

        def holds_start(b):
            lo, hi = b.get("min"), b.get("max")
            return (isinstance(start, (int, float)) and isinstance(lo, (int, float))
                    and lo <= start and (hi is None or start <= hi))
        # EVERY BAND BOUNDARY IS A PROMISE — except the one she starts in. A meter showing
        # bands at 15/35/55/75 tells the player there is something different at each of
        # those. So the threshold that must be bought is the highest `min` left after the
        # starting band is dropped — not the highest `max`, which is missing entirely once
        # the top band is (correctly) left unbounded. A rising meter starting at 0 drops
        # only its bottom band, so it is still judged at its top band's `min`.
        promised = [b["min"] for b in bands
                    if isinstance(b.get("min"), (int, float)) and not holds_start(b)]
        top_min = max(promised, default=None)
        if top_min is None or top_min == 0:
            continue
        if tops[key] < top_min:
            empty = [m for m in promised if m > tops[key]]
            over.append(f"{key}: bands promise something at {'/'.join(str(int(e)) for e in empty)}, "
                        f"but the highest authored gate is {tops[key]}")
    _N["meter ceiling"] = len(tops)
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
    #
    # ⚠️ REWRITTEN 2026-09-26 (PRD WS5). "Any locked choice anywhere" passed a game whose
    # ending had been removed, on unrelated locked rows. The release names ITS door in the ledger — board.door =
    # {canvas, choice} (choice = the choice's text; optional `node`) — and the gate checks
    # that door: it exists outside dev, it renders locked, it is shut at the start, and
    # every condition on it can come true later. The declared-state rule applies: no
    # ledger -> n/a; a ledger with no door -> FAIL (LO, 2026-09-26: an undeclared
    # door is not a pass). The door is read by `_declared_door`: `release_page.door`,
    # else `board.door` (PRD v2 CK2 · H4, 2026-09-30). Before that a door declared only
    # on the release page read as "not declared".
    all_choices = [ch for c in model for n in c["nodes"]
                   for ch in ((n.get("exit_block") or {}).get("choices") or [])]
    locked = sum(1 for ch in all_choices if ch.get("show_when_locked"))
    gated = sum(1 for ch in all_choices if (ch.get("conditions") or {}).get("items"))
    n_ch = len(all_choices) or 1
    census = (f"{locked} choices render visible-but-locked · "
              f"{gated}/{len(all_choices)} choices carry any gate at all "
              f"({100 * (len(all_choices) - gated) // n_ch}% open on turn one)")
    door = _declared_door(state) if state is not None else None
    if state is None:
        gate("ends on an opening", None, "no v2_state.json — no declared door to check · " + census)
    elif door is None:
        gate("ends on an opening", False,
             "no door declared — name the door this release ends on in release_page.door "
             "(or board.door before the release page exists) · " + census,
             ["declare release_page.door = {canvas = <canvas id>, choice = <the choice's text>} "
              "in v2_state.json; `the-release.md`: every release ends on a visible locked door, "
              "and a count of locked choices cannot tell which one that is"])
    else:
        problems = []
        src = ("release_page.door" if door is ((state.get("release_page") or {}).get("door"))
               else "board.door")
        canvas = next((c for c in (game.get("canvases") or []) if c.get("id") == door["canvas"]), None)
        choice = None
        if canvas is None:
            problems.append(f"{src}.canvas '{door['canvas']}' is not a canvas in the game")
        else:
            if _is_dev(canvas):
                problems.append(f"'{door['canvas']}' is a dev canvas — a shipped build strips it")
            choice = _door_choice(canvas, door)
            if choice is None:
                problems.append(f"no choice with text '{door['choice']}' on '{door['canvas']}'")
        if choice is not None:
            if not choice.get("show_when_locked"):
                problems.append("the door does not render locked (no show_when_locked) — the "
                                "player never sees it")
            items = list(_conditions_of(choice))
            if not items:
                problems.append("the door has no conditions — it is open, not a door")
            start_flags = _opening_flags(game) or set()
            start_traits = dict(((game.get("player") or {}).get("core_traits")) or {})
            ever_set = _flags_ever_set(game)
            written = set(_player_trait_raises(game))
            states = [(it, _cond_state(it, start_flags, start_traits, ever_set, written))
                      for it in items]
            if items and all(s == "open" for _, s in states):
                problems.append("every condition on the door is already true at the start — "
                                "it opens on turn one")
            for it, s in states:
                if s == "never":
                    kind, key, op, val = _cond_parts(it)
                    problems.append(f"condition {key} {op} {val if val is not None else ''} can "
                                    f"never come true — nothing in the game sets or raises it")
        gate("ends on an opening", not problems,
             f"declared door ({src}): {door['canvas']} · \"{door['choice']}\" · " + census, problems)

    # G9b — the door can be seen again (PRD v2 CK1 · I24, 2026-09-30). A door is a
    # locked choice the player is meant to walk past now and come back to. On a
    # ONE-TIME canvas the first visit spends the canvas, so a player who reaches it
    # before the unlock never sees the door again. It passes when the door's canvas is
    # repeatable, or opted into EN1 (`consume_on = "exit"`) with the door choice itself
    # neither `consumes` nor `final`. A separate row from the ladder's on purpose: a
    # ladder can be sound and still end on a door shown once. n/a when there is no
    # door to read; "ends on an opening" reports a missing or broken one.
    d_door = _declared_door(state)
    d_canvas = next((c for c in (game.get("canvases") or [])
                     if d_door and c.get("id") == d_door["canvas"]), None)
    d_choice = _door_choice(d_canvas, d_door) if d_canvas else None
    if d_choice is None:
        gate("the door can be seen again", None,
             "no declared door found in the game — nothing to re-enter")
    else:
        d_trig = d_canvas.get("trigger") or {}
        opt_in = d_trig.get("consume_on") == "exit"
        spent = bool(d_choice.get("consumes") or d_choice.get("final"))
        again = _rep_of(d_trig) or (opt_in and not spent)
        why = ("the canvas is repeatable" if _rep_of(d_trig) else
               "consume_on = \"exit\" and the door choice does not consume it" if again else
               "consume_on = \"exit\", but the door choice is marked "
               + ("consumes" if d_choice.get("consumes") else "final") if opt_in else
               "the canvas is one-time (is_repeatable = false)")
        gate("the door can be seen again", again,
             f"{d_door['canvas']}: {why}",
             [] if again else
             [f"the door is seen once — {d_door['canvas']} spends itself on the first visit, "
              f"so a player who reaches it before the unlock never sees \"{d_door['choice']}\" "
              f"again. Make the canvas repeatable, or set consume_on = \"exit\" on its trigger "
              f"and leave the door choice without consumes/final"])

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
    ranked = sorted(set(expand) | set(contract), key=lambda k: (-(expand[k] + contract[k]), k))[:6]  # name breaks ties: stable output
    # Judge what the author DECLARED as ascent, not what a heuristic guesses. Skills and
    # resources legitimately gate downward and are not the spine; only a declaration can
    # tell them apart. Falls back to the top-N heuristic when no ledger exists, and says so.
    declared = (state.get("board") or {}).get("ascent_tiers") if state else None
    tiers = list(declared) if declared else ranked[:ASCENT_TIERS]
    source = "declared" if declared else f"top-{ASCENT_TIERS} guess — no v2_state.json"
    # A declared tier nothing reads YET is n/a for that tier, not a meter that closes as
    # much as it opens (0 <= 0 used to fail it; PRD v2 CK8b · H10). Its note says so.
    unread = [k for k in tiers if not expand[k] and not contract[k]] if declared else []
    bad = [k for k in tiers if expand[k] <= contract[k] and k not in unread]

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

    read_tiers = [k for k in tiers if k not in unread]
    gate("ascent tiers expand the world",
         None if not (expand or contract) or (declared and not read_tiers and not descents)
         else (bool(read_tiers) and not bad and not descents),
         f"[{source}] " + ", ".join(f"{k} ({expand[k]}+/{contract[k]}-)" for k in tiers)
         if tiers else "no gated meter found",
         [f"{k} closes more than it opens ({expand[k]} expanding / {contract[k]} contracting)"
          for k in bad] +
         [f"{k} is a player meter that closes more than it opens "
          f"({p_expand[k]}+/{p_contract[k]}-) and is NOT declared as an ascent tier — "
          f"a descent wearing an ascent's clothes is invisible to the declaration"
          for k in descents] +
         [f"`{k}`: declared, no gate reads it this release — n/a for this tier" for k in unread] +
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
    _N["world reachable"] = len(loc_ids)
    gate("world reachable", None if not loc_ids else not stranded,
         f"{len(seen_locs & loc_ids)}/{len(loc_ids)} locations reachable on foot from "
         f"{start_loc or '(no start)'}",
         [f"{l} is not reachable and is not marked offscreen/sealed" for l in stranded])

    # G11b — every authored node is reachable. `world reachable` one level down:
    # that gate asks whether a ROOM can be walked to, this asks whether a SCREEN can
    # be opened. Added 2026-09-02 (the-surfaces.md R9).
    #
    # ⚠️ A canvas can ship nodes nothing links: `base` falls through to the engine's
    # default `[[Continue->Location_…]]`, so authored nodes are built and unreachable.
    # Nothing here could see it, because the only other reachability check
    # (`release_mode`'s `every canvas is a passage`) deliberately
    # keys on the CANVAS and throws the node segment away — node ids are not portable
    # across generator eras, so it cannot look inside. This gate reads the SOURCE,
    # where node ids are exactly as authored, so that objection does not apply.
    #
    # ⚠️ WHY A GATE AND NOT A LINT. There is no band to argue about — a node nothing points at is not a style, it is content the player
    # can never open.
    #
    # ⚠️ QUALIFY BEFORE COMPARING. `nodeId` may be bare or `canvas.node`; `rejection_node`
    # and `config.destinationId` are authored BARE and same-canvas (game_graph.py:450-453,
    # :516). `base`, `act` and `dev` repeat across canvases corpus-wide, so an unqualified
    # target set lets one canvas's `base` mark every other canvas's `base` as reached and
    # the gate silently under-reports to zero.
    #
    # ⚠️ `[[canvases.connections]]` IS NOT AN EDGE. It parses and persists, and the
    # generator never reads it — `game_graph.py:390`: "NodeConnection is dead — never
    # read by the generator — skipped." Counting it would clear a node that is still
    # dead in the build. Zero games declare one; it is excluded on purpose, not by
    # oversight.
    #
    # A substitution targets a CANVAS, so it reaches that canvas's entry node, which is
    # already exempt — it buys nothing here and is not read.
    node_targets, orphans, node_total = set(), [], 0
    for c in (game.get("canvases") or []):
        if _is_dev(c):
            continue                                  # dev shortcut — stripped from a shipped build
        cid = c.get("id") or "?"
        for n in (c.get("nodes") or []):
            for ch in _node_choices(n):
                for raw in (ch.get("nodeId"), ch.get("rejection_node")):
                    raw = str(raw or "")
                    if raw:
                        node_targets.add(raw if "." in raw else f"{cid}.{raw}")
            dest = str(((n.get("exit_block") or {}).get("config") or {}).get("destinationId") or "")
            if dest:
                node_targets.add(dest if "." in dest else f"{cid}.{dest}")
    for c in (game.get("canvases") or []):
        if _is_dev(c):
            continue
        cid = c.get("id") or "?"
        nodes = c.get("nodes") or []
        node_total += len(nodes)
        # nodes[0] is the canvas entry — the build lands on it, so it needs no inbound edge.
        for n in nodes[1:]:
            key = f"{cid}.{n.get('id')}"
            if key not in node_targets:
                w = sum(len(b.split()) for b in _band_texts(n)) if _band_texts(n) else 0
                orphans.append(f"{key} — {w} words, and nothing in the game links to it")
    _N["every authored node is reachable"] = node_total
    gate("every authored node is reachable", None if not node_total else not orphans,
         f"{node_total - len(orphans)}/{node_total} authored nodes can be opened",
         orphans[:12] + ([f"… and {len(orphans) - 12} more"] if len(orphans) > 12 else [])
         + (["a node is reached by a `targetType = \"node\"` choice, a `rejection_node`, or an "
             "`exit_block.config.destinationId` — write the link in the same edit as the node "
             "(the-surfaces.md R9)"] if orphans else []))

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
        _N["residents have homes"] = len(chars)
        gate("residents have homes", None if not chars else not homeless,
             f"{len(chars)-len(homeless)}/{len(chars)} characters have a home that exists", homeless)

    # G13 — the guidance surface is authored, not just switched on.
    # `quests_engine = "v2"` lights up a sidebar entry and a page; without cards it
    # renders a heading and nothing. Measured genre failure: lostness is the dominant
    # player complaint at a 4.7% median share of comments, against grind's 0.9%.
    cards = game.get("quest_cards") or []
    tiers_owed = board.get("ascent_tiers") or []
    # ⚠️ CORRECTED 2026-09-26 (PRD WS5). This used to accept `quests_engine` from
    # [settings] too. The engine reads it ONLY from [project] (`template_import.py:1870`;
    # the [[quest_cards]] block is parsed only when that value is "v2", `:2767`), so a game
    # with it under [settings] ships with every card dropped (`setup.quests_cards = [];`)
    # while this gate passed. It now reads
    # [project] only, and a [settings] placement FAILS by name. It also lists cards that
    # render no words and cards whose `when` can never come true.
    engine_on = (game.get("project") or {}).get("quests_engine") == "v2"
    misplaced = (not engine_on
                 and (game.get("settings") or {}).get("quests_engine") == "v2")
    def _card_mentions(card, key):
        blob = json.dumps(card)
        return f'"{key}"' in blob
    if misplaced:
        gate("guidance exists", False,
             f"quests_engine is under [settings] — the engine reads it only from [project], "
             f"so none of the {len(cards)} quest cards render",
             ["move `quests_engine = \"v2\"` from [settings] to [project] "
              "(template_import.py:1870, :2767)"])
    elif not engine_on and not cards:
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
            # A card that exists but can never help: no words, or a `when` that can never
            # come true. Start state = the flags the opening leaves set, and starting traits.
            g_start_flags = _opening_flags(game) or set()
            g_start_traits = dict(((game.get("player") or {}).get("core_traits")) or {})
            g_ever_set = _flags_ever_set(game)
            g_written = set(_player_trait_raises(game))
            for c in cards:
                name = c.get("id") or c.get("npc_id") or "a card"
                if not str(c.get("text") or "").strip() and not str(c.get("title") or "").strip():
                    gaps.append(f"{name}: renders no words — text and title are empty")
                for w in c.get("when") or []:
                    if isinstance(w, dict) and _cond_state(w, g_start_flags, g_start_traits,
                                                           g_ever_set, g_written) == "never":
                        kind, key, op, val = _cond_parts(w)
                        gaps.append(f"{name}: its `when` reads {key} {op}"
                                    f"{' ' + str(val) if val is not None else ''}, which nothing "
                                    f"in the game can make true — the card never shows")
        _N["guidance exists"] = len(tiers_owed) + len(cast)
        gate("guidance exists", not gaps,
             f"{len(cards)} quest cards for {len(tiers_owed)} ascent tiers and "
             f"{len(cast)} characters in the game",
             gaps)

    # G13b — a goal bullet says what it wants, in words.
    # The goal renderer falls back `label -> trait -> flag -> ""` (v2.py:15962-15964),
    # so a goals item carrying no `label` prints its RAW KEY to the player: a bullet
    # reading "◯ x_05_done" under the 🎯 To advance header. The importer requires
    # `label` on trait and counter goals ONLY (template_import.py:5669-5673; the
    # dataclass says so itself at :1092-1095) — flag-shaped goals fall straight through.
    #
    # Trait goals are already safe and already print the number: the renderer appends
    # " — <current> / <target>" for them (v2.py:15966-15968). The engine does its half
    # correctly; the whole leak is flag goals.
    #
    # A GATE and not a lint, on two grounds. There is no legitimate version of showing
    # a player a snake_case flag key — unlike the mute-card shape below, which the
    # engine's own comment calls intentional. And it invents no threshold: it compares
    # a card against its own declared goals, so it cannot fail a game for obeying the
    # doctrine. n/a when no card declares a goal, because an absence is not a pass.
    unlabelled, goal_items = [], 0
    for c in cards:
        for g in (c.get("goals") or []):
            goal_items += 1
            if not str(g.get("label") or "").strip():
                key = g.get("flag") or g.get("trait") or "?"
                who = c.get("npc_id") or "story"
                unlabelled.append(
                    f"{who}: goal '{key}' has no label — the player reads the raw key")
    _N["a goal says what it wants"] = goal_items
    gate("a goal says what it wants",
         None if not goal_items else not unlabelled,
         f"{goal_items - len(unlabelled)}/{goal_items} goal bullets render words "
         f"rather than a raw key",
         unlabelled)

    # ⚠️ THERE IS NO "walls state their key" GATE, AND THE ABSENCE IS DELIBERATE.
    # It was written, it fired on nearly every door, and it was WRONG:
    # `references/engine.md` §15 already rules on this and rules the other way —
    # omitting `locked_text` shows the greyed ACTION ("Ask him where the bench went"),
    # which is a want the player can name and is what sells the next release; setting
    # it replaces the want with a reason and is "weaker as a door". Preferring the want
    # is the documented default, verified live.
    # A locked choice showing its own action text is therefore NOT silent — it states
    # the want. What it does not state is the ROUTE.
    # ⚠️ CORRECTED 2026-09-03. This comment used to end "and that is `the-voice.md`
    # R3's job on the guidance card, ALREADY ENFORCED BY 'guidance exists' below."
    # It is not. "guidance exists" checks that a card EXISTS per ascent tier and per
    # character and never reads what the card says. The route was therefore unchecked
    # on both surfaces at once. The two checks that now cover it are G13b above (a goal
    # renders words, not a raw key) and `lint · the guidance page says nothing` below
    # (a card that renders no requirement at all).

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
    _N["no chain ends in silence"] = len(by_npc)
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
        # real currency — a game can run a public currency alongside a hidden one —
        # and taking the first name match judged the wrong one. Same bug class already fixed once in the corpus extractor, where a
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
        # condition-gating them read as "nothing gates on money" — a game that spends
        # its currency on choices scored zero here.
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
        # Ties broken by name, so two runs print the same location (was set-order dependent).
        top_loc, top_n = (sorted(sink_locs.items(), key=lambda kv: (-kv[1], kv[0]))[:1] or [("—", 0)])[0]
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
        # obligation ("the rent is £100 on Sunday"), so a hidden price is a
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
            _N["a price is on its label"] = priced
            gate("a price is on its label", not silent,
                 f"{len(silent)} of {priced} choices spend `{currency}` without naming the amount"
                 + (f" · {other_cost} non-currency costs not judged" if other_cost else ""),
                 silent + (["field: every game in the play corpus that charges money puts the "
                            "amount in the label — the player is budgeting against a bill that comes back"]
                           if silent else []))
        else:
            gate("a price is on its label", None,
                 f"no choice spends `{currency}` — nothing to judge"
                 + (f" ({other_cost} non-currency costs, not judged)" if other_cost else ""))

    # G37 — one currency, or the player cannot read a price.
    #
    # the-economy.md R7. One click's price can render six ways: the button, the
    # paragraph, the engine's refusal "Requires 3 Money (you have 1)" (v2.py:4680),
    # "money: 12 / 100" in the sidebar (v2.py:16241) and the rent card's default "$90"
    # (v2.py:1190). Three of the six are the engine's.
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
    # different games, and the scoreboard could not tell them apart: a game with one desk far
    # over the cap and a game with every screen AT the cap both read as solved. A ceiling makes "pass" and
    # "maximise" point the same way, so a ceiling gate that prints only a verdict teaches the
    # cap as the spec. Same discipline as G2's marginal-pass headline.
    #
    # ⚠️ ROOMS AND CHARACTER HUBS ARE COUNTED SEPARATELY, and the reason is the denominator
    # trap this project has now hit six times. R3 is about ROOMS. Character hubs are shaped by
    # a different rule (R1/R2's object test). Averaging hubs with rooms dilutes the room
    # count — the good screens dilute the bad ones in the number meant to expose them. The
    # cap still applies to both; only the reporting is split.
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
            # Count DECISIONS, not navigation. The field's big screens are mostly
            # exits and standing travel affordances, and only 1-6 things to do.
            #
            # ⚠️ CORRECTED 2026-09-02 — THIS GATE HAD GONE BLIND, and the comment that
            # blinded it was the give-away. It read: "Today this excludes nothing —
            # every choice is targetType 'node'" (2026-08-13, d1dc430). That stopped
            # being true almost immediately. Excluding EVERY location target excluded
            # the acts as well as the doors, and the gate went blind.
            #
            # And this file already disagreed with itself: the `a spent day still has
            # a door` gate below PRESCRIBES a location-target leave-link as the fix it
            # wants authors to write, so the advice manufactured exactly the choices
            # this line then refused to see.
            #
            # The seam is not the target, it is whether the choice DOES anything
            # (`the-surfaces.md` R9). A location exit that fires nothing is R7's door
            # and stays uncounted; one that grants, flags or charges is an act that
            # happens to end in a room, and it is a decision.

            choices = _node_choices(n)
            decisions = [ch for ch in choices
                         if (ch.get("targetType") or "node") != "location"
                         or _choice_acts(ch)]
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
    # `the-surfaces.md` R5 (ungated doors) and R6 (does the screen move) are real rules, and
    # both were built here as gates before the thresholds were checked. Neither survived the
    # check:
    #   R5: the ceiling had to be invented — a game at exactly 50% passes while another
    #       fails at 52%, which is noise, not a measurement.
    #   R6: not field-comparable AT ALL. In a compiled Twine file `<<if>>` covers engine
    #       plumbing — gated choices, media, presence — not just authored prose banding,
    #       and the two cannot be separated in someone else's build. Measured that way
    #       the field median is 86%, which says nothing about whether the PROSE moves.
    # Whether a room's narrative actually changes on re-entry is a question only PLAY
    # answers. Reported as lints until the play study sets real numbers.

    # G24 — the declared obligation is actually charged.
    #
    # ⚠️ A game can declare an obligation, print it on a quest card and write the scene of
    # paying it — while the settle-up canvas carries NO cost and NO money effect and is
    # repeatable without limit.
    #
    # Gate 16 passes that when OTHER canvases gate on money. That is the presence-gate
    # failure mode: "at least one exists" cannot see that the important one does not. This is
    # SKILL.md's "the BOARD DECLARES IT" rule applied to the field the economy is built on — the board declares a price,
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
        # EN2b — a staged bill may omit `amount`; the importer then requires a stage from
        # total 0, and that stage is what the rent charges from the first week.
        _stages = rent_cfg.get("stages") if rent_cfg.get("enabled") else None
        if not rent_amt and isinstance(_stages, list) and _stages and isinstance(_stages[0], dict):
            rent_amt = _stages[0].get("amount")
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

        # ⚠️ CORRECTED 2026-09-26 (PRD WS5). Two holes closed.
        # (a) A charge only counts where the player meets it again: on a canvas that is NOT
        #     dev and IS recurring (repeatable), or through [settings.rent]. A one-time or
        #     dev-only charge anywhere used to satisfy it. If the ledger names the settle-up
        #     canvas (board.economy.settle_canvas), the charge must sit on that canvas.
        # (b) The week has to be able to pay it. `_week_income` measures what a week can
        #     bring in; the verdict uses its MEAN (a random 8–25 is not 25 every day) and
        #     prints the MAX and the declared week_income beside it. A declared week_income
        #     can go stale while the build pays far less, and nothing compared them.
        settle = econ.get("settle_canvas")
        for c in game.get("canvases") or []:
            if _is_dev(c) or not _rep_of(c.get("trigger") or {}):
                continue
            if settle and c.get("id") != settle:
                continue
            _outflows(c)
        biggest = max(outflows) if outflows else 0
        charged_by = None
        if rent_charges and rent_amt >= (ob_amt if isinstance(ob_amt, (int, float)) else 0):
            charged_by = f"[settings.rent] {rent_amt:g} every {rent_cfg.get('due_day', '?')}"
        elif isinstance(ob_amt, (int, float)) and biggest >= ob_amt:
            charged_by = (f"a recurring charge of {biggest:g}"
                          + (f" on {settle}" if settle else ""))
        wk_mean, wk_max, wk_rows, wk_uncapped = _week_income(game, currency)
        declared_week = econ.get("week_income")

        gaps = []
        if not isinstance(ob_amt, (int, float)) or ob_amt <= 0:
            gaps.append("board.economy.obligation is declared but board.economy.obligation_amount "
                        "is not — an obligation with no price cannot be checked")
        elif not charged_by:
            gaps.append(f"nothing takes {ob_amt:g} `{currency}` from the player: the largest "
                        f"authored outflow is {biggest:g}"
                        + (f" and [settings.rent] charges {rent_amt:g}" if rent_charges
                           else " and [settings.rent] is not enabled")
                        + " — the price is written in the ledger and the prose but never taken")
        if isinstance(ob_amt, (int, float)) and ob_amt > 0 and not wk_uncapped:
            moves = econ.get("obligation_moves")
            if wk_mean < ob_amt and not (isinstance(moves, str) and moves.strip()):
                gaps.append(f"a week can bring in about {wk_mean:g} {currency} on average "
                            f"(at most {wk_max:g}) against an obligation of {ob_amt:g} — "
                            f"the player cannot pay it, and board.economy.obligation_moves "
                            f"does not signpost when that changes")
        if isinstance(declared_week, (int, float)) and declared_week > wk_max and not wk_uncapped:
            gaps.append(f"board.economy.week_income says {declared_week:g}, but the build can "
                        f"bring in at most {wk_max:g} a week — the ledger is stale")
        gate("the obligation is charged", not gaps,
             f"[declared] {ob_amt if isinstance(ob_amt, (int, float)) else '?'} {currency}"
             + (f" · charged by {charged_by}" if charged_by else "")
             + f" · week income ~{wk_mean:g} (max {wk_max:g}"
             + (f", declared {declared_week:g}" if isinstance(declared_week, (int, float)) else "")
             + (f", {len(wk_uncapped)} uncapped sources" if wk_uncapped else "") + ")",
             gaps + [f"income: {r}" for r in wk_rows[:8]] + [f"uncapped: {u}" for u in wk_uncapped[:5]])

    # G25 — every effect uses an op the engine actually runs.
    #
    # ⚠️ THE CHEAPEST GATE HERE, AND IT CATCHES THE MOST INVISIBLE CLASS OF BUG.
    # `applyTraitEffect` runs `add` and `set`, and on anything else falls through to
    # `// Unknown op; do nothing` and RETURNS (v2.py:5742-5751). Nothing normalises the
    # value: `subtract` appears nowhere in the generator or the importer. The importer
    # validates `op` for cheat-page grants (template_import.py:3755) and for nothing else,
    # so a dead effect is valid TOML, builds green, and emits verbatim into the HTML.
    #
    # A dead effect builds green and changes nothing: a meter never moves, a cost is never
    # charged, and nothing says why — a live play-through passes it too, because the number
    # simply does not change. `references/engine.md` §21 had discussed `op = "subtract"` as though it worked.
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
    # A flag read `is_false` and cleared in the tick that no canvas sets is permanently
    # false, so every gate on it fails open — a talk screen guarded that way is
    # re-clickable without limit, a faster route to the cast meters than the day-capped
    # rung it sits below.
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
    # G37b — A SPENT DAY STILL HAS A DOOR.  the-surfaces.md R6 · the-meters.md M5.
    #
    # The other half of the gate above. `a day-cap closes` asks whether the cap has a
    # SETTER. This one asks what the screen looks like once the cap is SPENT — and a
    # day cap is spent every single day, by design, so this is not an edge state.
    #
    # A spent day cap can leave a hub with a portrait, a paragraph, a line of dialogue
    # and nothing to click, and the player cannot tell whether the game is broken. An
    # activity screen can do the money-shaped version of it.
    #
    # ⚠️ THE CAP IS PER PERSON AND THE HUBS ARE PER ROOM. One shared `*_rung_today`
    # spent at one hub empties the others for the rest of the day when their whole list
    # is that one flag.
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
    # keeps it from flagging exhaustive routing.
    #
    # The fix is one choice:
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
    # COSTS: a rung granting +1 for 10 minutes, free, uncapped and repeatable, makes a
    # correctly gated tier farmable.
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
    _N["the climb is paid for"] = n_gated
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
        # EN5 (2026-09-30): `in_dump = false` is the switch for this — it keeps the key out
        # of the dump only. `hidden = true` still passes (it removes the key everywhere),
        # but it is the secret-trait switch, and name-keyed: hiding the player's banded
        # `corruption` with it also hid every man's `corruption`.
        _lab = labels.get(k) or {}
        if not (_lab.get("in_dump") is False or _lab.get("hidden")):
            doubled.append(
                f"`{k}` is banded as {item.get('type', 'a sidebar item')} but "
                + ("is not declared in [[traits.labels]] at all"
                   if k not in labels else "is declared without in_dump = false")
                + " — the band and the raw number both render")
    n_banded = sum(1 for i in (game.get("sidebar_items") or [])
                   if isinstance(i, dict) and i.get("bands") and i.get("trait_owner") != "npc")
    _N["a banded meter is not also a number"] = n_banded
    gate("a banded meter is not also a number", None if not n_banded else not doubled,
         f"{len(doubled)} of {n_banded} banded sidebar meters also print as a raw number"
         if n_banded else "no banded sidebar meters — nothing to judge",
         doubled + (["set in_dump = false on the same key in [[traits.labels]] (engine.md §30)"]
                    if doubled else []))

    # ─────────────────────────────────────────────────────────────────────────
    # G28 — THE MAP IS A PLACE.  the-map.md R0 + R3.
    #
    # A world that is one house with a token outside passes a declaration alone.
    # The shape is a declared choice with this check behind it; a worked example
    # outranks every rule beside it, so none is given.
    #
    # TWO tests, because a declaration alone is satisfied by typing a word:
    #   1. did you CHOOSE a shape (declared)
    #   2. is the outside actually the outside (mechanical, off entry_from)
    #
    # Test 2 is the half a parser can see: an exterior declared, priced at 25
    # minutes, hanging off the KITCHEN — so stepping outdoors means stepping from
    # one interior into a row of shops. It cannot be talked out of in the ledger.
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
    # ⚠️ A need that decays, is restored four ways and gates nothing costs the
    # player time and buys nothing. The shape is a need that shuts a door
    # (`hygiene >= 40` gates leaving — filthy means she cannot leave).
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
              "declared needs, a third of every room's menu cannot exist"])
    else:
        read = _traits_read_by_conditions(game)
        dead = [n for n in needs if str(n.get("key")) not in read]
        _N["a need shuts a door"] = len(needs)
        gate("a need shuts a door", not dead,
             f"{len(needs) - len(dead)}/{len(needs)} declared needs are read by a condition "
             f"somewhere in the game",
             [f"`{n.get('key')}` is declared a need"
              + (f" that \"{n.get('shuts')}\"" if n.get("shuts") else "")
              + " — but NO condition anywhere in the game reads it. A restore that gates "
                "nothing is a chore, not a need (the-meters.md M9)"
              for n in dead])

    # G29b — a need can be met every day (PRD v2 CK8c · H12, 2026-09-30). G29 asks whether
    # a need gates anything; this asks whether she can FILL it on every weekday. A body that
    # needs food and a kitchen closed on Sundays is a Sunday with no way out. A source is a
    # canvas whose effects add a positive value to the need, or set it to one. It is live on its trigger's
    # weekdays (every day with no schedule), narrowed by its place's EN3 `hours` when the
    # place has them; a triggerless rung takes the days of the canvases that route into it.
    if state is None or not needs:
        gate("a need can be met every day", None,
             "no declared needs — nothing to fill" if state is not None
             else "no v2_state.json — nothing declared to check against")
    else:
        loc_hours = {l.get("id"): l.get("hours") for l in (game.get("locations") or [])
                     if isinstance(l.get("hours"), list) and l.get("hours")}

        def own_days(canvas):
            t = canvas.get("trigger") or {}
            live = _trigger_slots(t)
            hours = loc_hours.get(t.get("location"))
            if hours:
                live &= _hour_slots([(h.get("weekdays"), h.get("open", "00:00"),
                                      h.get("close", "23:59")) for h in hours])
            return {d for d, _h in live}

        by_id = {c.get("id"): c for c in (game.get("canvases") or [])}

        def live_days(canvas):
            t = canvas.get("trigger") or {}
            if t.get("location"):
                return own_days(canvas)
            days = set()
            for r in routes.get(canvas.get("id")) or []:
                src = by_id.get(r["src"])
                if src is not None and (src.get("trigger") or {}).get("location"):
                    days |= own_days(src)
            return days

        short = []
        for need in needs:
            key = str(need.get("key"))
            days = set()
            for c in (game.get("canvases") or []):
                if _is_dev(c) or (c.get("trigger") or {}).get("is_active", True) is False:
                    continue
                # A refill is an `add` of a positive value OR a `set` to one: the field's
                # restores are mostly "wash set 100", and reading `add` only called every
                # one of them unfillable.
                raises = any((ef.get("trait") or ef.get("trait_key")) == key
                             and ef.get("targetType", "player") == "player"
                             and (ef.get("op") or "add") in ("add", "set")
                             and _effect_value_sign(ef.get("value")) > 0
                             for h in _exit_holders(c.get("nodes")) for ef in (h.get("effects") or []))
                if raises:
                    days |= live_days(c)
            missing = [_PR_DAYS[d] for d in range(7) if d not in days]
            if missing:
                short.append(f"`{key}`: nothing that raises it is live on {', '.join(missing)}")
        gate("a need can be met every day", not short,
             f"{len(needs) - len(short)}/{len(needs)} declared needs can be filled on every weekday",
             short)

    # ═════════════════════════════════════════════════════════════════════════
    # G30 — the walk-in floor. `the-surfaces.md` R3.
    #
    # The join is the author's OWN board: she works alone here, someone is
    # scheduled here, so someone can interrupt her. Nothing is invented.
    #
    # ⚠️ FLOOR IS PER ROOM, NOT PER PAIR — deliberately. The raw cross-product runs
    # to dozens of pairs per game; demanding those would
    # rebuild the wall of buttons one layer down, which is the objects mistake in
    # a new coat. One walk-in per qualifying room; the rest is the author's call.
    # ═════════════════════════════════════════════════════════════════════════
    qualifying, covered, (solo, sched, subs) = _walkin_join(model, game)
    missing = sorted(set(qualifying) - set(covered))
    _N["the walk-in floor"] = len(qualifying)
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
             "axis the odds ride. DoL's are 458-473 bytes. Not a scene.",
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
    # ⚠️ It lands on the field's hottest gate. In the field a sexual-state meter is a real gate in 13 of 27 games, and
    # where it exists it is the #1 or #2 most-gated thing in the whole game
    # (corpo-life `lust`, DoL `arousal`, family-ties `you.arousal`,
    # friends-of-mine `excitement`).
    #
    # CAUSE, one line of this skill's own template: the volatile layer in
    # `templates/board.toml` was labelled "NEVER gate an arc on these" — correct
    # about the ODOMETER and silent about the THROTTLE, so an author reads it
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
    _N["a meter is read"] = len(raises)
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
    # The field reads its wardrobe hard: degrees-of-lewdity reads its derived
    # exposure ~900 times, the-hellfire-club its slot variables 484,
    # zaras-school-life `$PlayerClothes` 415.
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
    #    on `V.exposed === 2`. A game can read its wardrobe mostly through
    #    `clothing_item` plus a portrait override; a first-family-only check fails it.
    #
    # ⚠️ THE SAME FIG LEAF AS THE GATE ABOVE — one throwaway `worn_corruption gte 1`
    #    turns this green. No threshold is invented, because W7 measures the field's
    #    median gate share at 10% and demanding gates would be wrong. Instead the
    #    summary prints garments-against-reads, so a thin pass is visible on the
    #    report the way the meter-ladder lint makes a one-rung ladder visible.
    # ═════════════════════════════════════════════════════════════════════════
    # ⚠️ `worn_exposure` was missing here until 2026-09-03 while `engine.md` §17 listed it
    #    in the same reader family and the engine implemented it (v2.py:4255, :8117). It is
    #    the newest of the predicates and the only one that reads an EMPTY slot, so a game
    #    reading its wardrobe exclusively that way was reported as reading it not at all —
    #    the detail block would say "NOTHING reads the wardrobe" while conditions did.
    _CLOTHING_PREDICATES = ("worn_corruption", "worn_beauty", "worn_type",
                            "worn_exposure", "clothing_slot", "clothing_item")
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
    # G48 — A DECLARED GARMENT CAN BE GOT.  `the-meters.md` W3 · `engine.md` §17.
    #
    # G41 above asks whether the wardrobe is READ. This asks the prior question, the one
    # that makes the read moot: can the player ever OWN the thing? A garment with no route
    # into `sv.player.wardrobe` is a catalog entry, and every condition naming it is a door
    # with no key.
    #
    # WHAT THIS CATCHES, and it is not wardrobe hygiene. A garment with no `shop_location`
    # and no `wardrobeEffects` can never be obtained. An arc step that triggers on it
    # (`worn_type eq "going_out"`) dies there — live: `isCanvasValid` false with every
    # other prerequisite met — and everything downstream of the step is sealed.
    #
    # ⚠️ "A SHOP EXISTS" IS THE WRONG TEST. `renderShopPage` stocks only
    # `!initial && price > 0` (v2.py:2105-2107), so non-initial garments at `price = 0` are
    # invisible on the very page they sit beside. A check reading "there is a shop,
    # therefore buyable" misses them.
    #
    # ⚠️ `shop_location` IS NEVER VALIDATED. template_import.py:2536 takes the slug as a bare
    # string and v2.py:9935 compares it to each location's own slug; a typo is silent and the
    # whole catalog is unreachable with no error anywhere. Hence the `in _loc_ids` test.
    #
    # ⚠️ ZERO-BASED, like G44 and G45, and for the same reason: there is no threshold to
    # invent. Either a route exists or none does. A game declaring no [[clothing]] reports
    # n/a, which is NOT a pass.
    #
    # ⚠️ THIS DOES NOT ASK WHETHER A CONDITION IS SATISFIABLE. That needs the derived
    # worn_beauty / worn_corruption MAX aggregate modelled, and a check that cannot see the
    # shape of the thing it judges manufactures whatever it can see (the deleted gate 22,
    # `the-surfaces.md`). The exact question reaches the same defect from the side that can
    # be answered.
    # ═════════════════════════════════════════════════════════════════════════
    _settings = game.get("settings") or {}
    _loc_ids = {l.get("id") for l in (game.get("locations") or []) if isinstance(l, dict)}
    _shop_slug = str(_settings.get("shop_location") or "")
    _shop_live = bool(_settings.get("clothing_enabled")) and _shop_slug in _loc_ids
    _grantable = {c.get("id") for c in garments if c.get("initial")}
    if _shop_live:
        _grantable |= {c.get("id") for c in garments
                       if not c.get("initial") and (c.get("price") or 0) > 0}
    for _path, _wnode in _walk_paths(game):
        for _we in (_wnode.get("wardrobeEffects") or []):
            if isinstance(_we, dict) and _we.get("item_id"):
                _grantable.add(str(_we["item_id"]))
    _ungrantable = [c for c in garments if c.get("id") not in _grantable]
    _why_no_shop = ("no `shop_location` in [settings]" if not _shop_slug else
                    "clothing_enabled is false" if not _settings.get("clothing_enabled") else
                    f'`shop_location = "{_shop_slug}"` names no declared location')
    detail = []
    if _ungrantable:
        detail.append(
            f"{len(_ungrantable)} declared garment(s) with NO route into the wardrobe: "
            + ", ".join(f"`{c.get('id')}`"
                        + (" (price 0 — the shop stocks only price > 0, v2.py:2105)"
                           if _shop_live and not (c.get("price") or 0) else "")
                        for c in _ungrantable[:10])
            + (" …" if len(_ungrantable) > 10 else ""))
        if not _shop_live:
            detail.append(f"the shop is not live — {_why_no_shop} — and no `wardrobeEffects` "
                          f"grants them either (v2.py:14414, :14575)")
        detail.append("three routes exist and this game uses none of them for these: "
                      "`initial = true`, a shop purchase (`[settings] shop_location` + "
                      "`initial = false` + `price > 0`), or `wardrobeEffects = "
                      '[{ item_id = "…", action = "add" }]` on a choice or an '
                      "`exit_block.config` — `engine.md` §17")
        detail.append("a condition naming a garment nothing can grant is a door with no key. "
                      "Open a route or cut the garment (`the-meters.md` W3)")
    _N["a declared garment can be got"] = len(garments)
    gate("a declared garment can be got",
         None if not garments else not _ungrantable,
         (f"{len(garments) - len(_ungrantable)}/{len(garments)} declared garment(s) have a "
          f"route into the wardrobe"
          + (f" · shop @{_shop_slug}" if _shop_live else f" · no shop ({_why_no_shop})")
          + (f" · {len(_ungrantable)} unreachable" if _ungrantable else ""))
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
    #
    # ⚠️ THIS GATE REVERSES WHAT THIS SKILL USED TO TEACH. engine.md §15 read
    #    "Prefer the want unless the gate is genuinely obscure" until 2026-08-24,
    #    so a mute locked row is doctrine, not sloppiness. §15 was rewritten in the same turn
    #    this gate landed; the two must not be allowed to drift apart again.
    #
    # ⚠️ THREE THINGS COUNT AS A REASON:
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
    _N["a locked door says why"] = len(shown_locked)
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
    # No field game sits between 15% and 65%. A game lands there not because the
    # middle was chosen, but because the question was never asked. v1 asks it
    # (`content-framework.md`, "Who climbs?"); v2 dropped it.
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
              "measured: the field splits 9 ladder / 8 roster with NOTHING between 15% and 65%",
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
              "declaration — but do not leave it in the middle, where no field game sits "
              "(the-meters.md W1)"]
             + ([f"{_ladder_counter_sites(game)} gate(s) read a ladder counter and are not "
                 f"counted: a ladder counter is not his score; give him a meter of his own (D5)"]
                if _ladder_counter_sites(game) else []))
    # G44 — the start choice is read. `the-want.md` §1.
    #
    # WHAT THIS CATCHES: fake freedom — a start question whose answers share one target,
    # carry no effects and differ in no way. The game asks the player who she is and
    # then discards the answer.
    #
    # WHY IT IS WORTH GATING: `freedom` is the largest single thing the male-heavy top 30
    # is loved for (25.9% of top-30 engagement, reason (1) weighted by comment count). For
    # a female lead the premise matters too (the-want.md §0); the choosing still does.
    #
    # ⚠️ IT FAILS ONLY ON ZERO, AND THAT RESTRAINT IS THE POINT. A floor ("read at least
    # N times") cannot be defended with no distribution to read it off, and this
    # skill has already had to supersede a whole doctrine built at n = 1 (the-meters.md
    # W1, 2026-08-19). Declared-and-never-read needs no threshold — it is the defect by
    # definition. Everything else is REPORTED so a distribution accumulates and a future
    # floor can be read off it instead of invented.
    #
    # ⚠️ THE SET-SITE IS NOT CHECKED HERE. The flag-chain validator already hard-fails a
    # flag whose setter is triggerless (`template_import.py`), and two instruments on one
    # question is how gate 22 and the anchoring lint had to be split apart.
    # ═════════════════════════════════════════════════════════════════════════
    sc = (((state or {}).get("want") or {}).get("player") or {}).get("start_choice") or {}
    sc_flags = [f for f in (sc.get("flags") or []) if isinstance(f, str) and f.strip()]
    if state is None:
        gate("the start choice is read", None,
             "no v2_state.json — nothing declared to check against")
    elif not sc_flags:
        gate("the start choice is read", None,
             "no want.player.start_choice declared — the player chooses nothing about her",
             ["declare it: want.player.start_choice = { asked_at, flags } — the-want.md §1",
              "measured on the male-heavy top 30: `freedom` is 25.9% of engagement and the "
              "largest single bucket; for a female lead the premise matters too (the-want.md "
              "§0)",
              "a memory, not a slider — ask what the scene already asks and set a flag; do "
              "not build a stat screen",
              "this reports n/a, which is NOT a pass — an absence is not evidence"])
    else:
        # A READ is the flag appearing in ANY condition anywhere in the canvas tree —
        # a trigger, a choice, a [group] band. All three are how a start choice earns
        # its keep, so all three count; `_conditions_of` only reaches one object, so
        # this walks the whole structure the way the flag census does.
        sc_reads = collections.Counter()

        def _walk_conds(obj):
            if isinstance(obj, dict):
                for it in _conditions_of(obj):
                    key = it.get("flag_key")
                    if key in sc_flags:
                        sc_reads[key] += 1
                for v in obj.values():
                    _walk_conds(v)
            elif isinstance(obj, list):
                for v in obj:
                    _walk_conds(v)

        _walk_conds(game.get("canvases") or [])
        dead = [f for f in sc_flags if not sc_reads[f]]
        shape = " · ".join(f"{f} read {sc_reads[f]}x" for f in sc_flags)
        gate("the start choice is read", not dead,
             f"{len(sc_flags)} start-choice flag(s) — {shape}"
             + ("" if dead else "  (count reported, not judged — see the header)"),
             ([f"declared and NEVER READ: {', '.join(dead)}",
               "a choice the game does not read is the fake-freedom defect this gate exists "
               "for — the player is asked who she is and the answer is discarded",
               "either read it (a [group] band, a gated rung) or drop it from "
               "want.player.start_choice.flags"] if dead else []))

    # G45 — what money buys opens a door. `the-economy.md` R1b.
    #
    # WHAT THIS CATCHES: a purchase the game forgets — price, flag and shop built, and
    # the flag read nowhere, so the doors were never cut.
    #
    # WHY IT IS WORTH GATING: it is Study 7's fake-freedom defect in its economic form.
    # There the player was asked who she is and the answer was discarded; here she is
    # asked to pay and the purchase is discarded. Same shape, same zero-based test.
    # Measured, the field sells a THING in nine of 25 corpus games and in all four of the
    # most-engaged sandboxes — become-someone's company gates 114 condition sites,
    # become-taxi-driver's car 46, destroyer's five rooms 21/20/16/16/16.
    #
    # ⚠️ IT FAILS ONLY ON ZERO, for the reason G44 does: there is no distribution to read a
    # floor off. The counts print unjudged until there is.
    #
    # ⚠️ A GAME THAT SELLS NOTHING REPORTS n/a, NOT PASS. An absence is not evidence — the same wording the climb, start-choice and
    # obligation checks use.
    # ═════════════════════════════════════════════════════════════════════════
    _cur = _declared_currency(state)
    if not _cur:
        gate("what money buys opens a door", None,
             "board.economy.currency not declared — purchases cannot be identified")
    else:
        buys = {}                      # flag -> price paid for it
        _buy_choice = collections.defaultdict(set)   # flag -> id() of the choices that SET it
        _buy_canvas = collections.defaultdict(set)   # flag -> canvas ids holding those choices

        def _purchases(obj, cid):
            if isinstance(obj, dict):
                for ch in (obj.get("choices") or []):
                    if not isinstance(ch, dict):
                        continue
                    cs = ch.get("costs") or []
                    if isinstance(cs, dict):
                        cs = [cs]
                    price = next((x.get("value") for x in cs
                                  if isinstance(x, dict) and x.get("trait") == _cur), None)
                    if price is None:
                        continue
                    for e in (ch.get("flagEffects") or []):
                        if isinstance(e, dict) and e.get("op") == "set" and e.get("flag"):
                            buys.setdefault(e["flag"], (price, cid))
                            _buy_choice[e["flag"]].add(id(ch))
                            _buy_canvas[e["flag"]].add(cid)
                for v in obj.values():
                    _purchases(v, cid)
            elif isinstance(obj, list):
                for v in obj:
                    _purchases(v, cid)

        for c in (game.get("canvases") or []):
            _purchases(c, c.get("id") or "?")

        # A READ is the flag in ANY condition anywhere — trigger, choice or [group] band,
        # counted the way G44 counts a start choice rather than by reaching one object.
        #
        # ⚠️ EXCEPT THE TILL'S OWN GATE, WHICH IS NOT A DOOR. Two conditions exist only so
        # the same thing cannot be sold twice, and neither is content the money opened:
        #   · `<flag> is_false` on the BUYING CHOICE — stops re-selling it;
        #   · `<flag> is_false` on the TRIGGER of the canvas holding that choice — retires
        #     the whole row once it is owned.
        # Counting them handed every carefully-written purchase a free +1 and put this
        # gate's zero test out of reach: a purchase can pass on the choice form alone while
        # the garment is never received and no condition anywhere names it again.
        # The trigger form is excluded in advance: it is what
        # `<flag> is_false` on [canvases.trigger] produces, and an author writing it
        # would silently re-open the hole. Restricted to `is_false` — an `is_true` test on
        # the choice that SETS the flag can never fire, so it is dead either way.
        buy_reads = collections.Counter()

        def _walk_buy_conds(obj, cid=None, in_trigger=False):
            if isinstance(obj, dict):
                for it in _conditions_of(obj):
                    key = it.get("flag_key")
                    if key not in buys:
                        continue
                    if it.get("operator") == "is_false" and (
                            id(obj) in _buy_choice[key]
                            or (in_trigger and cid in _buy_canvas[key])):
                        continue                      # the till, not a door
                    buy_reads[key] += 1
                for k, v in obj.items():
                    _walk_buy_conds(v, cid, in_trigger or k == "trigger")
            elif isinstance(obj, list):
                for v in obj:
                    _walk_buy_conds(v, cid, in_trigger)

        for c in (game.get("canvases") or []):
            _walk_buy_conds(c, c.get("id") or "?")

        # A flag the daily tick wipes overnight is a DAY CAP, not a possession, and a day
        # cap priced in coins is a legitimate shape. They
        # are excluded here rather than failed — the same carve-out `_holder_day_capped`
        # makes for gate 18.
        _tick = ((game.get("engine") or {}).get("daily_tick") or {})
        _nightly = {e.get("flag") for e in (_tick.get("flagEffects") or [])
                    if isinstance(e, dict) and e.get("op") in ("clear", "unset", "reset")}
        kept = {f: v for f, v in buys.items() if f not in _nightly}

        if not kept:
            gate("what money buys opens a door", None,
                 f"nothing is bought with `{_cur}` that survives the night — "
                 "the game sells no possession",
                 ["the-economy.md R1b — nine of 25 corpus games sell the player a THING, "
                  "and all four of the most-engaged sandboxes do",
                  "a level ladder (a company at 20k/50k/100k), an instalment build (a "
                  "church, five payments of 50 wood), or a one-off possession (a room)",
                  "this reports n/a, which is NOT a pass — an absence is not evidence"])
        else:
            dead = [f for f in kept if not buy_reads[f]]
            shape = " · ".join(f"{f} ({kept[f][0]:g}) opens {buy_reads[f]}"
                               for f in sorted(kept, key=lambda k: -buy_reads[k]))
            shape += "  (the purchase's own `is_false` gate is not a door)"
            gate("what money buys opens a door", not dead, shape
                 + ("" if dead else "  (doors reported, not judged — see the header)"),
                 ([f"BOUGHT AND NEVER READ: "
                   + ", ".join(f"{f} for {kept[f][0]:g} at {kept[f][1]}" for f in dead),
                   "the player pays and the game never refers to it again — Study 7's "
                   "fake-freedom defect with a price on it",
                   "either read it (a [group] band, a gated rung, a wider block_pool — "
                   "the-surfaces.md R6) or stop charging for it"] if dead else []))

    # ═════════════════════════════════════════════════════════════════════════
    # G46 — she can say no. `the-surfaces.md` R5b, existence half. 2026-08-28.
    #
    # ⚠️ R5b WAS DELIBERATELY LEFT UNGATED AND THIS DOES NOT OVERTURN THAT. The reason on
    # record is that it rested on "four games read in source, which is an observation, not
    # a field", and that whether a decline is written at full length and PAID is a
    # judgement no parser makes. Both still hold, and the quality half stays ungated. What
    # this gates is strictly narrower and countable — is there a single choice in the whole
    # game that declines an offer — and it rests on the whole corpus, not on four games.
    #
    # WHAT THIS CATCHES: a game the player cannot decline anything in. An author can
    # write two hundred choices without ever noticing they never wrote a no.
    #
    # THE FIELD: 1,763 of 84,458 clickable labels across the 25 corpus games are a real
    # refusal — 2.09%, roughly one click in fifty. And they are NOT theatre, which was
    # checked before this gate was written: of 4,973 refusals sitting beside at least one
    # other option, 79% go somewhere the accepting link does not, the median destination
    # carries 262 words, and only 3% lead to a stub under 20. In the field, declining buys
    # content. Refusal is a content kind, not a courtesy.
    #
    # ⚠️ FAILS ONLY ON ZERO, on the precedent of G44 and G45. A rate floor cannot be
    # defended from here: the field's 2.09% is not the same measurement — field labels
    # include navigation, and this reads authored choice text. Zero needs no threshold. It is the defect by definition, and everything above
    # zero is reported so a distribution can accumulate and a future floor be READ off it
    # rather than invented. That restraint is what R4, study 6's anchoring check and P0
    # were withdrawn for missing.
    #
    # ⚠️ THE PATTERN IS NARROW ON PURPOSE, AND THE FIRST DRAFT WAS WRONG. A looser one
    # counted `leave` and `ignore`, which are navigation — "Leave the shop" declines
    # nothing, so it reads navigation as refusal. A refusal DECLINES AN OFFER; anything
    # that merely exits a room is not one. If this gate is ever loosened, re-check it
    # against games with known refusals first.
    # ═════════════════════════════════════════════════════════════════════════
    # CK8a (I3): a no written as her spoken line starts with a quote mark — skip it.
    _REFUSAL = re.compile(
        r"^[\s\"“'‘]*(no[,.!\s\"”'’]|no$|refuse|decline|say no|reject|resist|turn (him|her|it|them) down|"
        r"don't|do not|not (tonight|now|today|this)|push (him|her|them) (off|away)|"
        r"stop (him|her|them)|pull away|shake your head|tell (him|her|them) no|"
        r"back off|not interested|keep (them|it) on|refuse to)", re.I)
    _ch_texts = [ch.get("text") for c in (game.get("canvases") or [])
                 for n in (c.get("nodes") or [])
                 for ch in ((n.get("exit_block") or {}).get("choices") or [])
                 if isinstance(ch.get("text"), str)]
    _refusals = [t for t in _ch_texts if _REFUSAL.match(t.strip())]
    if not _ch_texts:
        gate("she can say no", None, "no authored choices to judge")
    else:
        _rate = len(_refusals) / len(_ch_texts) * 100
        gate("she can say no", len(_refusals) > 0,
             f"{len(_refusals)} refusal(s) in {len(_ch_texts):,} choices = {_rate:.1f}%"
             + ("  (rate reported, not judged — see the header)" if _refusals else "")
             + " · field 2.09% of labels",
             ([f"e.g. {t.strip()[:60]!r}" for t in _refusals[:3]] if _refusals else
              ["the player cannot decline ANYTHING in this game — every choice is a way of "
               "saying yes, and a choice she cannot refuse is not a choice",
               "the field puts a real refusal on roughly one click in fifty, and 79% of them "
               "lead somewhere the accepting link does not, median 262 words behind them",
               "write the no as content, not as a dead end: what she does instead is a scene",
               "⚠️ a refusal is not `Leave` — exiting a room declines nothing"]))

    # ═════════════════════════════════════════════════════════════════════════
    # G47 — what she picks is read. `the-want.md` §1, W1. 2026-08-29.
    #
    # WHAT THIS CATCHES: the creation screen that goes nowhere. A game asks the player
    # her name, her build and her look at minute zero and then never uses one of them.
    # This is G44's fake-freedom defect in the engine's OTHER start-choice mechanism —
    # G44 reads `want.player.start_choice.flags` and has no knowledge of
    # `[[player.customization_fields]]`, which is where the discarding is worst.
    #
    # WHY IT IS WORTH GATING: measured over the 13 top-30 games with a creation step,
    # the field reads each created field a median of FOUR times and the median game
    # leaves NONE of them unread.
    #
    # ⚠️ FAILS ONLY ON ZERO, on the precedent of G44, G45 and G46. No rate floor: the
    # field's median of 4 is a different measurement (their reads run through name widgets
    # and bare interpolation over whole games) and a threshold taken from it would
    # fail a game for obeying the doctrine. Zero is the defect by definition.
    #
    # ⚠️ A GAME DECLARING NO CUSTOMIZATION REPORTS n/a, NOT PASS — same wording as the
    # start-choice, climb and obligation checks. An absence is not evidence.
    #
    # ⚠️ TWO SYNTAXES, AND MISSING ONE PRODUCES A FALSE ZERO. The value lands at
    # `$player.<id>` (or `$player.name`), and the HOUSE form for reading it in prose is
    # the `@` token — `@player` for the name, `@player.<id>` for the rest. This study's
    # own instrument reported a false zero twice by knowing only one form: once by
    # missing `@player.<id>` entirely, once by excluding `@player.` at a sentence end,
    # which is the commonest way the name token appears. The name pattern below is
    # therefore "@player NOT followed by a dot and another declared field id".
    #
    # ⚠️ `sets_portrait = true` COUNTS AS A READ. An image_select field writes
    # `$player.portrait`, which the stats page renders. Without this exemption every
    # image_select field fails — a gate that fails a
    # game for using a feature correctly, which is exactly what took R4 back out.
    # ═════════════════════════════════════════════════════════════════════════
    _pl = game.get("player") or {}
    _cfs = [c for c in (_pl.get("customization_fields") or []) if isinstance(c, dict)]
    if not _cfs or not _pl.get("customizable"):
        gate("what she picks is read", None,
             "no customization declared — the player is handed a protagonist whole",
             ["that is a legitimate choice: half the corpus ships no creation step, "
              "including the second-ranked game, and across 22,614 comments the whole "
              "subject runs at 0.12% (lostness 4.7%, grind 0.9%)",
              "if you do add one: the-want.md §1 W1 — if you ask, print it back",
              "this reports n/a, which is NOT a pass — an absence is not evidence"])
    else:
        _blob = []

        def _strings(o):
            if isinstance(o, dict):
                for v in o.values():
                    _strings(v)
            elif isinstance(o, list):
                for v in o:
                    _strings(v)
            elif isinstance(o, str):
                _blob.append(o)

        _strings(game)
        _text = "\n".join(_blob)
        _ids = [str(c.get("id") or "") for c in _cfs]
        _other = [i for i in _ids if i and i != "name"]
        _nametok = (re.compile(r"@player(?!\.(?:" + "|".join(map(re.escape, _other)) + r")\b)")
                    if _other else re.compile(r"@player\b"))
        _counts, _dead = {}, []
        for _cf in _cfs:
            _fid = str(_cf.get("id") or "")
            if not _fid:
                continue
            if _fid == "name":
                _n = (len(re.findall(r"\$player\.name(?![A-Za-z0-9_])", _text))
                      + len(_nametok.findall(_text)))
            else:
                _n = (len(re.findall(r"\$player\." + re.escape(_fid) + r"(?![A-Za-z0-9_])", _text))
                      + len(re.findall(r"@player\." + re.escape(_fid) + r"(?![A-Za-z0-9_])", _text)))
            _counts[_fid] = _n
            if _n == 0 and not _cf.get("sets_portrait"):
                _dead.append(_fid)
        _shape = " · ".join(
            f"{k} {v}x" + (" (portrait)" if any(c.get("id") == k and c.get("sets_portrait")
                                                for c in _cfs) else "")
            for k, v in _counts.items())
        gate("what she picks is read", not _dead,
             f"{len(_counts)} field(s) — {_shape}"
             + ("" if _dead else "  (counts reported, not judged — see the header)")
             + " · field median 4 reads per field",
             ([f"declared and NEVER READ: {', '.join(_dead)}",
               "the player is asked who she is and the answer is discarded — the-want.md "
               "§1 W1. The field reads each created field a median of 4 times and the "
               "median game leaves none unread",
               "print it back: `@player` for her name, `@player.<field_id>` for the rest "
               "(or the raw `$player.<field_id>`) — the payload is a WORD, not a gate",
               "or drop the field. Refusing costs nothing: half the corpus ships no "
               "creation step at all"] if _dead else []))

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
    _N["speakers are named"] = n_speaking
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
         f"(ceiling {SENTENCE_CEILING}, margin {margin:+d}) · field median 10, p25 "
         f"{FIELD_SENTENCE_MEDIAN[0]} — the floor is printed, not judged (prose has room)",
         ([] if med_sent <= SENTENCE_CEILING else
          ["field median is 10 words; the reference game is 9",
           "escalate by adding beats, not by lengthening sentences"])
         + ([f"⚠️ sitting ON the ceiling. {SENTENCE_CEILING} is a backstop calibrated across "
             f"two extraction bases, not a target — the field runs 10 and the reference game 9."]
            if sent_words and margin <= 0 else []))

    # prose has room — the first FLOOR under the writing (PRD IC6). Every other prose
    # check is a ceiling; this one fails prose that has dropped its joints: too few `but`
    # (nothing is set against anything) or more `and` than any game in the field (a list
    # where there should be a relationship). Same base as the field figures: paragraph,
    # dialog and thought text, plus each location's description.
    jp = _joint_profile(_joint_prose(game))
    if jp["words"] < JOINTS_MIN_WORDS:
        gate("prose has room", None,
             f"{jp['words']} prose words — under {JOINTS_MIN_WORDS}, too little to judge a rate")
    else:
        low_but = jp["but_1k"] < FIELD_BUT_P10
        high_and = jp["and_1k"] > FIELD_AND_MAX
        gate("prose has room", not (low_but or high_and),
             f"`but` {jp['but_1k']:.2f}/1k (floor {FIELD_BUT_P10}, field p10) · `and` "
             f"{jp['and_1k']:.1f}/1k (field max {FIELD_AND_MAX}) · over {jp['words']:,} words",
             ([f"`but` is under the field's p10: the prose sets nothing against anything. "
               f"Name the relationship — but, because, so, until — or split (register.md, "
               f"\"Joints\")"] if low_but else [])
             + ([f"`and` is over every game in the field: a list where a relationship "
                 f"belongs"] if high_and else []))

    # G43 — prose texture. The SECOND gate here that measures writing.
    #
    # Added 2026-08-27. Of the 42 gates that existed, exactly one looked at the writing
    # (G19). Prose can be field-normal on the only axis measured and far off-field on one
    # that is not.
    #
    # ⚠️ THIS READS b.text AND MUST NEVER READ THE BUILT HTML. Built HTML carries UI list
    # blocks that never reach a full stop, so the splitter reads each as one enormous
    # comma-filled "sentence", and joints-per-sentence taken off HTML is an artifact. Read
    # authored beat text. That is the same family of error the SENTENCE_CEILING seam documents, hit a second time.
    # Anything computed PER SENTENCE is not comparable across the two bases. A rate over
    # word count, which is what this gate judges on, is.
    #
    # Only the dash carries a verdict. The three numbers reported under it gate nothing: no
    # threshold is invented for a marker whose field spread has not been shown to separate
    # a good game from a bad one.
    tex_words = tex_dashes = 0
    dash_by_canvas = {}
    for c in model:
        t = " ".join(x for b in c["beats"] for x in b.text)
        w = len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))
        d = len(re.findall(r"—|–", t))
        tex_words += w
        tex_dashes += d
        if d:
            dash_by_canvas[c["id"]] = (d, w)
    dash_rate = tex_dashes / tex_words * 10_000 if tex_words else 0.0

    tex_prose = " ".join(x for c in model for b in c["beats"] for x in b.text)
    tex_sents = [s for s in re.split(r"(?<=[.!?])\s+", tex_prose)
                 if 2 <= len(s.split()) <= 120]
    tex_joints = (sum(len(re.findall(r",|—|–|;|:", s)) for s in tex_sents)
                  / len(tex_sents)) if tex_sents else 0.0
    tex_tok = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]*", tex_prose)]
    tex_you = (sum(tex_tok.count(w) for w in ("you", "your", "yours"))
               / len(tex_tok) * 100) if tex_tok else 0.0
    tex_p2n = (len(re.findall(r"\b(?:he|him|his|she|her|hers|they|them|their)\b",
                              tex_prose, re.I))
               / max(len(re.findall(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", tex_prose)), 1))

    # Where the dashes actually live. An em-dash in narration is the appositive habit
    # register.md names; an em-dash in speech is how English writes an interruption, and
    # "Wait — no — I can't, if you keep —" is correct as written.
    #
    # ⚠️ REPORTED, NEVER GATED, and the verdict above deliberately still counts BOTH.
    # Moving the verdict to narration-only needs a narration-only FIELD baseline, and that
    # was investigated and cannot be had: 14 of the 25 corpus games put under 2% of their
    # words inside quote marks (corpus median 1.3%), marking speech with italics, speaker
    # prefixes or nothing at all. A narrowed measurement judged against an all-prose
    # ceiling is the seam error this gate's header exists to warn about.
    def _tex_split(blocks, spoken, narr):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            props = b.get("props") or {}
            if isinstance(b.get("content"), str):
                # thought_bubble is a person's voice too, and stammers for the same reasons
                (spoken if b.get("type") in ("dialog", "thought_bubble")
                 else narr).append(b["content"])
            for beat in (props.get("beats") or []):
                _tex_split(beat.get("blocks"), spoken, narr)
            _tex_split(props.get("blocks") or b.get("blocks"), spoken, narr)

    tex_spoken, tex_narr = [], []
    for c in (game.get("canvases") or []):
        for n in (c.get("nodes") or []):
            _tex_split(n.get("blocks"), tex_spoken, tex_narr)

    def _rate(parts):
        t = " ".join(parts)
        w = len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))
        return (len(re.findall(r"—|–", t)) / w * 10000 if w else 0.0), w

    spoken_rate, spoken_w = _rate(tex_spoken)
    narr_rate, narr_w = _rate(tex_narr)

    tex_detail = []
    if tex_words and dash_rate > DASH_CEILING:
        tex_detail += [f"{cid}: {d} in {w:,} words"
                       for cid, (d, w) in sorted(dash_by_canvas.items(),
                                                 key=lambda kv: -kv[1][0])[:6]]
        tex_detail += [
            "⚠️ do NOT fix this by swapping the dash for a comma. The joint survives the swap "
            "and nothing reads easier. Split the sentence, "
            "or cut the clause it was holding on.",
            "field p50 is 0.99/10k — half the corpus writes under one dash per 10,000 words",
        ]
    if tex_words and (spoken_w or narr_w):
        tex_detail.append(
            f"where they live — narration {narr_rate:.1f}/10k over {narr_w:,} words · "
            f"speech {spoken_rate:.1f}/10k over {spoken_w:,} words. A dash in speech is how "
            f"English writes an interruption and is usually correct; the narration figure is "
            f"the one register.md's \"Dashes stay rare\" is about. Verdict above counts both, "
            f"because the field cannot be split (see DASH_CEILING).")
    if tex_words:
        tex_detail += [
            f"reported, not gated, NO field figure — joints/sentence {tex_joints:.2f} · "
            f'"you" {tex_you:.1f}% of words · pronoun:name {tex_p2n:.2f}',
            "⚠️ these three compare a game with its own earlier builds and with nothing else. "
            "The corpus exists only as built HTML, whose UI strings and list blocks move all "
            "three. The dash rate above is quoted against the field because it is the one that "
            "survives the change of basis.",
        ]
    gate("prose texture", None if not tex_words else dash_rate <= DASH_CEILING,
         f"{tex_dashes} dash{'' if tex_dashes == 1 else 'es'} in {tex_words:,} prose words = "
         f"{dash_rate:.1f}/10k (ceiling {DASH_CEILING:.0f}) · field p50 0.99, p90 17.5, max 35.4"
         if tex_words else "no authored beat prose to measure",
         tex_detail)

    # ─────────────────────────────────────────────────────────────────────────
    # THE FIRST HOUR — references/the-first-hour.md
    # Three gates added 2026-08-22. Nothing in the existing 32 looked at the opening,
    # the introductions, or the first visit.
    # ─────────────────────────────────────────────────────────────────────────

    # G33b — the opening hands over into an open door (the-first-hour.md F3)
    # A funnel that ends at a clock time when nothing at the landing location is open
    # makes the player's first free act pressing a wait button. v1 named this the
    # dead-window bug; the opening is the one place it costs most.
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

    # G34b — every hub is met first (the-first-hour.md F5 + F8)
    # The forbidden shape is a repeatable `npc=` hub whose base node IS the introduction.
    # The bar is 100%, and it is a CHOICE backed by field evidence, not a universal law
    # (LO decided, 2026-09-28). Hand-read across the four passing games, 7-27 characters
    # each: three meet every character before their hub is reachable in spirit — Shady
    # Deals, Cupid's Way and In Her Own Hands, 100% each — but only 57-81% under a strict
    # one-flag-per-person reading, the gap being GROUP meetings on one shared flag (Shady
    # Deals' trio, Cupid's Way's office tour) and characters met in the forced opening.
    # So both count as met (`_fh_cast_met`). Course of Temptation does it differently: its
    # generic "Talk to" works on strangers (30% in spirit). Plan and samples:
    # round5/SETTINGS_REDERIVE_PLAN.md.
    met, cast, flag_owners, cold = _fh_cast_met(game)
    if not cast:
        gate("every hub is met first", None, "no portrait hubs authored")
    else:
        det = [f"{npc}: hub(s) {', '.join(cids)} carry no condition at all — "
               f"the portrait is live on turn one"
               for npc, cids in cold[:8]]
        det += [f"{npc}: gated, but on no flag a meeting with {npc} sets"
                for npc in cast
                if npc not in met and npc not in {n for n, _c in cold}][:6]
        if len(met) < len(cast):
            det.append("a meeting is a NON-repeatable canvas that names that character "
                       "and sets a flag the hub reads (a group scene naming several "
                       "people meets them all), or a line in the forced opening")
        _N["every hub is met first"] = len(cast)
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
    # The failure: a meeting with no window plays its introduction to an empty room —
    # at an hour the character is out, with prose naming the wrong day. A taught rule
    # and a worked template do not stop it; a check does. template_import.py's own
    # comment on the field said the opposite (corrected in the same change as this gate).
    #
    # SCOPED SO IT ONLY CONVICTS WHERE A WINDOW WAS AUTHORABLE. A canvas whose NPC
    # declares no rows at that location has nothing to copy, and saying so would be a
    # different, weaker finding wearing this one's clothes.
    #
    # Scoped so a game that did the work is never nagged.
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
        if _rep_of(t) or t.get("substitution_only"):
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
    _N["a meeting fires where they are"] = in_scope
    gate("a meeting fires where they are",
         None if not in_scope else not windowless,
         f"{in_scope - len(windowless)}/{in_scope} one-shot canvases naming a character "
         f"can only fire in that character's own hours",
         windowless)

    # G47b — no canvas key is discarded (the-first-hour.md F5b, engine.md §42)
    #
    # `TemplateCanvas` has seven fields — id, name, description, trigger, nodes, connections,
    # loop (template_import.py:906-913) — and it is built with named arguments only
    # (:2302-2310), so ANY other key on a [[canvases]] table is dropped: no error, no
    # warning, green build. `slug` is tolerated because the parser does read it, as a
    # fallback label in error context (:2033).
    #
    # The keys that get written up here are TRIGGER keys, and losing one is invisible in
    # exactly the way that hurts — the TOML still says what the author meant.
    #
    # ⚠️ THIS INVENTS NO THRESHOLD AND CANNOT PRODUCE A FALSE POSITIVE, which is why it is
    #    a gate where its softer sibling below is only a lint. A key outside the seven does
    #    nothing at all, on any path, in any shape of game. Writing one is never correct, so
    #    there is no game this can fail for obeying the doctrine — R4 is unreachable here.
    #
    # `npc` one level too high costs the whole cast its portraits and presence gate, and
    # the canvas title renders as the link label. `substitution_only` one level too high
    # turns every walk-in into a clickable activity instead of a dispatcher-only target.
    #
    # ⚠️ THE CLASS IS THE KEY PLACEMENT, NOT THE KEY: `npc` and `substitution_only` both get
    #    written one table too high in the same way, so a gate named for one key would pass
    #    the other.
    CANVAS_FIELDS = {"id", "name", "description", "trigger", "nodes", "connections",
                     "loop", "slug"}
    TRIGGER_FIELDS = {"location", "is_active", "is_repeatable", "max_triggers_per_day",
                      "priority", "conditions", "schedules", "npc", "trigger_mode",
                      "chance", "costs", "show_when_blocked", "cooldown_message",
                      "entry_only_from", "substitutions", "substitution_only",
                      "requires_npc", "pre_substitution_effects",
                      "consume_on", "retry_after_days"}  # EN1, 2026-09-30
    misplaced = []
    for c in (game.get("canvases") or []):
        t = c.get("trigger") or {}
        for k in sorted(set(c) - CANVAS_FIELDS):
            where = f" @{t['location']}" if t.get("location") else ""
            if k in TRIGGER_FIELDS:
                home = f"a [canvases.trigger] field — move it one level down"
                if k in t:
                    home += ", where this canvas already sets it (the top-level copy is dead)"
            else:
                home = "not a field the importer reads anywhere"
            misplaced.append(f"{c.get('id')}{where}: `{k}` on [[canvases]] is discarded — {home}")
    n_misplaced = len(misplaced)
    gate("no canvas key is discarded", not n_misplaced,
         f"{n_misplaced} canvas key(s) sit on [[canvases]] and are dropped by the importer"
         if n_misplaced else "every canvas key is one the importer reads",
         misplaced)

    # G35 was "the anchor introduces itself" and is GONE (2026-08-26).
    # It passed a game only if its anchor carried a non-repeatable canvas — a
    # first-visit scene. Counted across the 26-game corpus that device is ONE game
    # (degrees-of-lewdity, 258 branches / 117 flags; eighteen games have none), so the
    # gate made a green board depend on something most of the field declines to do,
    # and it sent one author to write nine arrivals that were reverted the next day.
    # What replaces it is `lint · the place says what it is` — a list, because whether
    # a description names its function is a reading and not a measurement.
    # the-first-hour.md F9 carries the numbers.

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
    # Field basis: of 84,009 action link labels across the 27 parseable sandboxes, 24 name
    # a clock time and NONE of them is a repeatable action — 6 explicit waits or alarms
    # ("Wait until 21:00"), 7 stated windows, 6 chapter markers in one linear game, 5
    # narration fragments used as a label. Even lust-for-life, which HAS an absolute-time
    # primitive and calls it 270 times, labels those buttons "Back home" / "Leave" /
    # "Go to the SPA".
    # ⚠️ THIS READ "2 in 92,226 across 25 sandboxes" UNTIL 2026-08-24. The 2026-08-24
    # recheck re-measured it into `the-clock.md` C2 and did not update this comment, so
    # the skill carried two numbers for one measurement for a day. Section K found it.
    # The load-bearing zero — no label promises a clock time as the OUTCOME of a
    # repeatable action — survived the re-measurement unchanged. `the-clock.md`, "What the scoreboard checks".
    _idx = _clk_node_index(game)
    lab_n, clk_bad, dur_n, dur_bad = 0, [], 0, []
    _from_exit = 0
    for _c, _ch, _t, _shape in _clk_choices(model):
        lab_n += 1
        _refs = _clk_refs(_t)
        if _refs:
            _shown = sorted({r.strip(" .,;:!?") for r in _refs})[:2]
            if _shape == "exit":
                _from_exit += 1
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
            if _from_exit:
                # Say where they came from. This check read only `exit_block.choices`
                # until 2026-08-25, which is most buttons; a count
                # that jumped without saying so would read as prose having changed.
                _det.append(f"{_from_exit} of these sit on a SINGLE-EXIT node "
                            "(exit_block.text, no choices array) — a surface this check "
                            "did not read before 2026-08-25")
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
    want = state.get("want") or {}
    names += list(want.get("why_this_person") or {})
    # A `role:<name>` key (a walk-on with no id, PRD v2 DC2b · H34) is not a name the
    # fiction teaches: "role:night man" would hide "night" and "man" from the report.
    names += [k for k in (want.get("crude_ceiling") or {}) if not str(k).startswith("role:")]
    # The Want's own people and places (DC2b · B7): the board does not exist yet in the
    # want phase, so without these the game's own place names top its own report.
    names += [c.get("id") for c in want.get("cast") or [] if isinstance(c, dict)]
    for p in want.get("places") or []:
        if isinstance(p, dict):
            names += [p.get("id"), p.get("name")]
    for key in ("characters", "locations"):
        for entry in board.get(key) or []:
            if isinstance(entry, dict):
                names += [entry.get("id"), entry.get("name")]
    names += list((board.get("map") or {}).get("homes") or {})
    # `npc_jo` -> the tokeniser sees `npc` and `jo`; both are then names the
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


# ─────────────────────────────────────────────────────────────────────────────
# --beat — the only mode that measures prose that is not in a game yet
# ─────────────────────────────────────────────────────────────────────────────
# Everything else here needs a built `7_final_game.toml`, which is one phase too
# late for the job it is wanted for. `references/agents.md` specifies the Prose
# Maker as "one beat, from a spec it cannot argue with, hitting one measurable
# target" — and no instrument in this skill could measure a loose paragraph. The
# explicit counter is a property on a `Beat` assembled out of parsed TOML blocks
# (`Beat.explicit`), and `--words` reports vocabulary and nothing else. So the
# agent's own spec named a target that did not exist, and it could not be told
# whether it had succeeded.
#
# ⚠️ EVERY NUMBER BELOW IS ALREADY IN THIS FILE. Nothing new is invented here, and
# that is deliberate: an instrument built for one agent, measuring on its own
# private scale, would let the Prose Maker optimise for something the build never
# checks. Same regexes, same constants, same reason.
#
#   3 explicit words     the count `explicit floor` uses to call a beat explicit
#                        at all. `lint_act_nodes` says it in as many words:
#                        "3 is not an invented threshold".
#   SENTENCE_CEILING 14  measured over 18 shipped sandboxes, field median 10.
#   DASH_CEILING 35.0    per 10,000 words, measured over the 25-game mopoga corpus.
#   model beats          `register.md` ## The model beats — the field runs 37 words per reveal beat (reference, not a rule).
#
# AND IT REPORTS, IT DOES NOT GRADE. Exit is always 0, like `--words`. A beat is
# not a game and a single paragraph outside its canvas cannot be failed: the same
# 25 words are correct as one rung of a four-beat cascade and thin as a capstone.
# The reader decides; this says what is on the page.


def _beat_sentences(text):
    """Sentence split, identical to G19's so the two never disagree."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def _print_beat_joints(text):
    """One `--beat` line: `but` and `and` per 1,000 words against the field figures the
    gate `prose has room` judges a whole game by (PRD v2 CK6 · H8). PRINTED, NOT JUDGED,
    like every `--beat` line. Under JOINTS_MIN_WORDS the gate itself calls a rate too little
    to judge, and the line says so."""
    jp = _joint_profile(text)
    short = (f" — too short to judge (under {JOINTS_MIN_WORDS} words; printed, not judged)"
             if jp["words"] < JOINTS_MIN_WORDS else "")
    print(f"    joints               but {jp['but_1k']:.2f}/1k (field p10 {FIELD_BUT_P10}) \u00b7 "
          f"and {jp['and_1k']:.1f}/1k (field max {FIELD_AND_MAX}){short}")


def beat_mode(path):
    """Measure loose prose the way the build measures a beat.

    Blank-line separated blocks are separate beats; a single paragraph is one beat.

    ⚠️ THE PIVOT IS REPORTED AS A SHAPE AND NEVER AS A VERDICT. `register.md`'s rule
    is a READING test — "read the beat's last sentence; if it is about what the moment
    MEANS rather than what is HAPPENING, the beat has pivoted" — and no regex decides
    what a sentence is about. What IS observable is where the body words fall, so the
    report prints the distribution across sentences and quotes the last sentence back.
    A beat whose explicit words all sit in the front half and whose final sentence
    carries none has the shape the rule describes. Whether it pivoted is the reader's
    call, and calling it automatically is how a check starts failing correct work.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"cannot read {path}: {exc}")
        return 2

    beats = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    if not beats:
        print(f"{path} is empty — nothing measured (an absence is not a pass)")
        return 0

    print()
    print(f"  the beat as the build would measure it — {path}")
    print("  " + "\u2500" * 68)
    print(f"  {len(beats)} beat(s). Every threshold below is one this script already "
          f"uses;")
    print("  none of them is new, and none of them can fail here — see --beat's header.")

    all_words, all_sents, all_expl = 0, [], 0
    for i, text in enumerate(beats, 1):
        words = text.split()
        sents = _beat_sentences(text)
        expl = EXPLICIT.findall(text)
        per_sent = [len(EXPLICIT.findall(s)) for s in sents]
        sent_lens = [len(s.split()) for s in sents if 2 <= len(s.split()) <= 120]
        med = _median(sent_lens) if sent_lens else 0
        dashes = text.count("\u2014") + text.count("\u2013")
        rate = 10000.0 * dashes / max(len(words), 1)
        rungs = [name for name, rx in RUNGS if rx.search(text)]

        all_words += len(words)
        all_sents += sent_lens
        all_expl += len(expl)

        print()
        print(f"  BEAT {i}")
        # ⚠️ NO VERDICT ON LENGTH, and the reason is a unit mismatch that would have
        # made this line lie. `register.md 'S1 · The clip rides the beat'` gives 37 words per reveal beat, where
        # a beat is ONE SCREEN. A canvas node that is not a cascade is a single `Beat`
        # to this script and can hold several screens' worth of prose, and calling it
        # "over the band" would report a defect that the doctrine's own unit does not
        # support. A beat count and a node count are different things. So: the number, the reference, and the
        # caveat, and the reader matches unit to unit.
        print(f"    words                {len(words):>4}   register.md 'S1 · The clip rides the beat' \u2014 the field runs "
              f"37 words per")
        print(f"{'':>32}reveal beat, where a beat is ONE SCREEN. Compare only")
        print(f"{'':>32}if this text is one screen.")
        print(f"    explicit words       {len(expl):>4}   "
              f"{'registers as explicit (3+)' if len(expl) >= 3 else 'does NOT register as explicit (needs 3+)'}")
        if expl:
            print(f"      {', '.join(sorted(set(w.lower() for w in expl)))}")
        print(f"    median sentence      {med:>4}   "
              f"ceiling {SENTENCE_CEILING}, field median 10, reference game 9")
        print(f"    dashes               {dashes:>4}   {rate:.0f}/10k "
              f"(ceiling {DASH_CEILING:.0f}, field p50 0.99)")
        print(f"    act rungs named      {', '.join(rungs) if rungs else 'none — anatomy without an act, or no act here'}")
        _print_beat_joints(text)

        # The pivot shape.
        if sents:
            print(f"    body words by sentence   "
                  f"{' '.join(str(n) for n in per_sent)}   ({len(sents)} sentences)")
            if len(expl) >= 3 and per_sent and per_sent[-1] == 0:
                print("    \u26a0 the last sentence carries no body word. `register.md`: an "
                      "explicit beat")
                print("      stays on the body for its whole length. Read it and decide "
                      "whether it is")
                print("      about what is HAPPENING or about what it MEANS \u2014 this is a "
                      "shape, not a verdict:")
                print(f"        \u201c{sents[-1][:110]}\u201d")

    if len(beats) > 1:
        print()
        print("  ALL BEATS")
        print(f"    words {all_words:,} \u00b7 explicit {all_expl} \u00b7 median sentence "
              f"{_median(all_sents) if all_sents else 0} \u00b7 "
              f"{sum(1 for b in beats if len(EXPLICIT.findall(b)) >= 3)}"
              f"/{len(beats)} register as explicit")
        _print_beat_joints(" ".join(beats))
    print()
    print("  A beat outside a band is not a defect. The same 25 words are right as one")
    print("  rung of a cascade and thin as a capstone \u2014 which is why this exits 0.")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# --release — the one mode that reads the ARTEFACT instead of the source
# ─────────────────────────────────────────────────────────────────────────────
# Everything above this line measures `7_final_game.toml`. That is the right
# target for authoring and it is structurally incapable of seeing a build, which
# is why the release boundary went unheld: LO's rule — dev mode and missing media
# block RELEASE, not testing — lived only as a hand-copied comment on a JS object
# literal (`games-data.js:44-49`), restated in nine of twenty-eight portal entries
# in three wordings. Nine hand-copies in three wordings is doctrine in the wrong file.
#
# ⚠️ FAILING ON A MARKER DOES NOT WORK. A review once proposed failing on an `[IMAGE MISSING]` / `[VIDEO POOL MISSING]` marker in the HTML.
# Those markers are --debug ONLY — v2.py:12404 `if not self.debug: return ''`,
# and again at :14753 and :14906 — so a CLEAN build renders silent gaps and a
# marker grep passes it. The grep measures the wrong thing.
#
# Two instruments survive a clean build, and both are read here instead:
#   1. the flags-init JSON the generator always writes — `debug_mode` from
#      v2.py:1077, `dev_mode_enabled` written only under --dev (v2.py:1081-1082).
#      That is the build's own record of the flags it was made with.
#   2. MissingMediaPage — v2.py:217, "always generated, but button only shows in
#      debug mode"; _generate_missing_media_page at v2.py:10332 prints a real count
#      in every build.
#
# ⚠️ The media count is a BUILD-TIME SNAPSHOT. Files added to disk after the build
# are not in it. That is the correct semantic for a release gate — it judges the
# artefact that ships, not the working tree — and it means the fix for a red here
# is a REBUILD, never a file copy.

_PORTAL_FILE = "games-data.js"


def _portal_entries(root, path=None):
    """Every entry in games-data.js as {slug: {...}}, or None if the file is absent.

    Not a JS parser. Entries are brace-blocks at two-space indent and the fields
    wanted here (`slug`, `dev`, `version`) are one-line literals; the only long
    field is `summary`, a template literal that never opens a two-space brace.
    """
    path = path or os.path.join(root, _PORTAL_FILE)
    if not os.path.exists(path):
        return None
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    starts = [m.start() for m in re.finditer(r'^  \{', text, re.M)]
    out = {}
    for i, s in enumerate(starts):
        chunk = text[s: starts[i + 1] if i + 1 < len(starts) else len(text)]
        m = re.search(r'^\s*slug:\s*"([^"]+)"', chunk, re.M)
        if not m:
            continue
        ver = re.search(r'^\s*version:\s*"([^"]+)"', chunk, re.M)
        dev = re.search(r'^\s*dev:\s*(true|false)', chunk, re.M)
        out[m.group(1)] = {"version": ver.group(1) if ver else None,
                           "dev": (dev.group(1) == "true") if dev else False,
                           "listed": True}
    return out


def _built_flags(text):
    """(debug, dev, missing) read off the built HTML.

    `text` is already html.unescape()d: the flags map and the missing-media page
    both live inside passage source, so in the file itself they read
    `&quot;debug_mode&quot;: true` and `Found &lt;strong&gt;50&lt;/strong&gt;`.
    """
    dbg = set(re.findall(r'"debug_mode":\s*(true|false)', text))
    dev = set(re.findall(r'"dev_mode_enabled":\s*(true|false)', text))
    m = re.search(r'Found <strong>(\d+)</strong> missing media', text)
    if m:
        missing = int(m.group(1))
    elif "No missing media files found" in text:
        missing = 0
    else:
        missing = None                      # the page is absent — not a pass
    return ("true" in dbg), ("true" in dev), missing


# A passage declaration, NOT a mention. Three things this regex has to get right:
#
#  1. It anchors on `<tw-passagedata … name="`. A canvas that is LINKED TO but never
#     emitted still has its name in the HTML, inside the link text of the passages
#     pointing at it — most raw matches can be link references rather than
#     declarations. A bare substring search therefore
#     returns a false PASS on a dangling link, which is the other half of this very
#     bug class.
#  2. It accepts the `StartingCanvas_` prefix. The opening canvas emits as
#     `StartingCanvas_<id>_Node_base`; without the prefix this false-fails every
#     game.
#  3. It keys on the CANVAS, never the node. Node ids are not portable across
#     generator eras — older generator builds emit `_Node_1`, current ones
#     `_Node_base` — so a node-level check raises false alarms on older builds.
_PASSAGE_DECL = re.compile(
    r'<tw-passagedata\b[^>]*\bname="(?:Starting)?Canvas_([A-Za-z0-9_]+?)_Node_[^"]*"')


def _built_passages(text):
    """The set of canvas ids that actually became passages in the built HTML.

    `text` is already html.unescape()d by the caller, which does not matter here —
    passage NAMES are attributes and are never entity-encoded — but the shared
    reader keeps this beside `_built_flags` on purpose: both answer "what is in the
    artefact", which no gate can see because every gate parses the source.
    """
    return set(_PASSAGE_DECL.findall(text))


def release_mode(slug):
    """Is this build shippable? The artefact, not the source.

    OFF for every ordinary run — `gates.py <slug>` never reaches here — so nothing
    about authoring changes. This is LO's rule expressed as code instead of as memory.

    Exits NON-ZERO on any red. `words_mode` above is documented as always exiting 0
    because it is a list and must never block a phase; this one is the opposite by
    design, because a release is the one moment something can reach a player.
    """
    import html as _html

    root = os.getcwd()
    game_dir = os.path.join(root, "games", slug)
    build = os.path.join(game_dir, "output", "index.html")

    R = []

    def check(name, ok, headline, detail=None):
        R.append((name, ok, headline, detail or []))

    print(f"\n  author-game-v2 release check — {slug}")
    print(f"  {os.path.relpath(build, root)}")
    print(f"  {'─'*72}")

    # ── the build itself ────────────────────────────────────────────────────
    if not os.path.exists(build):
        check("a build exists", False,
              "no games/%s/output/index.html — there is nothing to ship" % slug)
        text = None
    else:
        check("a build exists", True,
              f"{os.path.getsize(build)//1024} KB")
        text = _html.unescape(open(build, encoding="utf-8", errors="replace").read())

    if text is not None:
        debug, dev, missing = _built_flags(text)

        check("built without --debug", not debug,
              "no debug scaffolding in the shipped flags" if not debug else
              "debug_mode is TRUE — this build carries [IMAGE MISSING] placeholders "
              "and the debug branches with them",
              [] if not debug else
              ["rebuild without --debug: manage.py package_from_toml --file "
               f"games/{slug}/toml_phases/7_final_game.toml --output games/{slug}/output "
               "--gen-version v2"])

        check("built without --dev", not dev,
              "no dev shortcuts in the shipped flags" if not dev else
              "dev_mode_enabled is TRUE — the [DEV MODE] banner, the sidebar jump list "
              "and every dev-shortcut canvas are live for the player")

        if missing is None:
            check("no missing media", False,
                  "MissingMediaPage is absent from the build — nothing measured, "
                  "and an absence is not a pass")
        else:
            check("no missing media", missing == 0,
                  "0 missing at build time" if missing == 0 else
                  f"{missing} media files were missing when this was built",
                  [] if missing == 0 else
                  ["a build-time snapshot: harvesting the files is not enough, the "
                   "build has to be REDONE afterwards"])

        # ── every canvas is a passage ───────────────────────────────────────
        # Reachability is not a property of the source, so no gate above can see
        # it: it is what the generator DECIDED TO EMIT. A canvas can be written,
        # at its ceiling, and absent from the build while every source gate is
        # green, because they parse `7_final_game.toml` and count content.
        # defects/001.
        src_path = os.path.join(game_dir, "toml_phases", "7_final_game.toml")
        try:
            src_game = _load(src_path)
        except Exception:
            src_game = None

        if src_game is None:
            check("every canvas is a passage", None,
                  "7_final_game.toml is unreadable — nothing to compare the build against")
        else:
            built = _built_passages(text)
            src_canvases = src_game.get("canvases") or []
            gone = [c for c in src_canvases if c.get("id") not in built]

            # WHICH of the two causes, read off the canvas's own trigger. A canvas
            # carrying trigger.location is in the SEED set by construction
            # (v2.py:420-424 graph path, :447-451 ORM path) and cannot be pruned by
            # the closure — so if it is absent, the build simply predates it. One
            # with no location had to be pulled in by a targetType="node" choice or
            # a substitution target (_compute_included_canvases, v2.py:564-640, and
            # its no-DB twin at :642-691), and absence means nothing pulled it.
            #
            # ⚠️ Two discriminators were tested and are NOT used, because inventing
            # the wrong exemption is how R4, study 6 and P0 were all withdrawn:
            #   · dev-gated canvases need no exemption — they are built in a
            #     NON-dev build too.
            #   · file mtime discriminates nothing — a TOML is routinely newer than
            #     its build, because merge_toml_phases rewrites 7_final_game.toml.
            stale = [c["id"] for c in gone if (c.get("trigger") or {}).get("location")]
            pruned = [c["id"] for c in gone if not (c.get("trigger") or {}).get("location")]

            detail = []
            if pruned:
                detail.append(
                    f"NOTHING LINKS TO THESE, so the build dropped them: {', '.join(sorted(pruned)[:8])}"
                    + (f" … and {len(pruned)-8} more" if len(pruned) > 8 else ""))
                detail.append(
                    "a triggerless canvas is only built if a targetType=\"node\" choice or a "
                    "substitution target pulls it in — write the link in the same edit as the "
                    "canvas (engine.md §8)")
            if stale:
                detail.append(
                    f"these carry a location, so they are in the seed set and the BUILD PREDATES "
                    f"them: {', '.join(sorted(stale)[:8])}"
                    + (f" … and {len(stale)-8} more" if len(stale) > 8 else ""))
                detail.append(
                    "REBUILD — do not go hunting for a missing link: manage.py package_from_toml "
                    f"--file games/{slug}/toml_phases/7_final_game.toml --output games/{slug}/output "
                    "--gen-version v2")

            check("every canvas is a passage", not gone,
                  f"{len(src_canvases)}/{len(src_canvases)} canvases reached the build"
                  if not gone else
                  f"{len(src_canvases) - len(gone)}/{len(src_canvases)} canvases reached the build "
                  f"— {len(gone)} in the source "
                  f"{'is' if len(gone) == 1 else 'are'} not in the HTML",
                  detail)

    # ── how the portal presents it ──────────────────────────────────────────
    entries = _portal_entries(root)
    if entries is None:
        check("filed as published", None,
              f"{_PORTAL_FILE} not found from {root} — run this from the repo root")
        entry = None
    else:
        entry = entries.get(slug)
        if entry is None:
            check("filed as published", False,
                  f"no entry for `{slug}` in {_PORTAL_FILE} — a game nobody can reach "
                  "is not released")
        else:
            check("filed as published", not entry["dev"],
                  "not filed under Dev / test builds" if not entry["dev"] else
                  "`dev: true` still set — the portal files this under test builds, "
                  "and that line is what moves it into the main grid")

    # ── the version triangle ────────────────────────────────────────────────
    # Three places say what shipped and nothing ever compared them: the portal
    # (what the storefronts are told), [project] version (what the sidebar prints
    # to the player) and the archive (the build itself, kept). The three drift: the
    # portal can sit releases behind the number in the player's face.
    if entry is not None:
        portal_v = entry["version"]
        toml_path = os.path.join(game_dir, "toml_phases", "7_final_game.toml")
        project_v = None
        if os.path.exists(toml_path):
            try:
                project_v = ((_load(toml_path).get("project") or {}).get("version"))
            except Exception:
                project_v = None
        archive = os.path.join(game_dir, "releases", f"v{portal_v}.html") if portal_v else None
        have_archive = bool(archive and os.path.exists(archive))

        if entry["dev"] and portal_v:
            check("the version says what shipped", False,
                  f"`dev: true` AND `version: \"{portal_v}\"` on the same entry — "
                  "one says not published, the other says this is what is live")
        elif not portal_v:
            check("the version says what shipped", False,
                  "no `version` on the portal entry — nothing can say what is live at "
                  f"games/{slug}/output/",
                  [f"[project] version in the TOML reads {project_v!r}" if project_v else
                   "and the TOML declares none either"])
        else:
            agree = (project_v == portal_v) and have_archive
            check("the version says what shipped", agree,
                  f"{portal_v} — portal, [project] and archive agree" if agree else
                  f"portal {portal_v} · [project] "
                  f"{project_v if project_v else 'not declared'} · archive "
                  f"{'present' if have_archive else 'MISSING'}",
                  [] if agree else
                  [f"the sidebar prints [project] version to the player; the portal is "
                   f"what the storefronts are told",
                   f"archive expected at games/{slug}/releases/v{portal_v}.html"])

    for name, ok, headline, detail in R:
        tag = "n/a " if ok is None else ("PASS" if ok else "FAIL")
        print(f"  [{tag}]  {name:32s} {headline}")
        for d in detail:
            print(f"          · {d}")

    judged = [r for r in R if r[1] is not None]
    npass = sum(1 for r in judged if r[1])
    print(f"  {'─'*72}")
    print(f"  {npass}/{len(judged)} release checks pass")

    # ── printed, never judged ───────────────────────────────────────────────
    # ⚠️ The archive is NOT required to be byte-identical to output/. An archive and
    # output/ legitimately differ after a rebuild; a check here would fail the correct
    # case, which is how R4, study 6's anchoring check and P0 each ended.
    if entry is not None and entry.get("version") and text is not None:
        arch = os.path.join(game_dir, "releases", f"v{entry['version']}.html")
        if os.path.exists(arch):
            import hashlib
            def _h(p):
                return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
            a, b = _h(build), _h(arch)
            print(f"  {'─'*72}")
            print(f"  note · output/ vs releases/v{entry['version']}.html — "
                  + ("identical" if a == b else f"differ ({a} vs {b})"))
            print("          (reported, never judged — output/ is legitimately rebuilt after "
                  "archiving, so a correct release can differ)")
    print()
    return 0 if judged and npass == len(judged) else 1


# ─────────────────────────────────────────────────────────────────────────────
# --saves — the only check that reads TWO releases
# ─────────────────────────────────────────────────────────────────────────────
# Every other check in this file, `--release` included, reads ONE snapshot. A
# save-compatibility break does not exist in a snapshot: renaming a canvas id
# produces a game that is perfectly correct on its own terms and strands every
# player holding a save. It exists only in the DIFFERENCE between what shipped and
# what is about to.
#
# `references/the-returning-player.md` states the rules; this is the half a human
# cannot be trusted to do by eye, because it is four set-differences across a few
# hundred names. It compares the current build against the newest archived
# release — which is why `the-release.md` step 3 archives one, and why a game with
# no archive cannot be checked at all.
#
# ⚠️ ADDITIONS ARE NEVER A FAILURE, and that is the whole shape of the thing.
# `setup.backfillStateDefaults` (`engine.md` §40) reaches a new flag, meter, NPC or
# `$game_state` sub-map on the next passage. Only a name that DISAPPEARED breaks a
# save, and a rename reads here as a removal plus an addition — correctly, because
# that is exactly what it is to the save.
#
# ⚠️ What this CANNOT see, and no diff of two builds can: a rescaled stat whose key
# never moved, and a one-shot grant a carried save already burned. Both are real,
# both have shipped, and both stay human — `the-returning-player.md` §4 and §6.


def _join_keys(text):
    """The four things a save is joined on, read off a built game.

    `text` must already be html.unescape()d — passage source is stored escaped, so
    `<<set $flags = {&quot;a&quot;: true}>>` is what is in the file.
    Returns None for any part that could not be read, so an unreadable build is
    never mistaken for one that lost every key.
    """
    out = {"passages": None, "npcs": None, "flags": None,
           "player_traits": None, "npc_traits": None, "title": None,
           "schema": None}

    names = re.findall(r'<tw-passagedata[^>]*\bname="([^"]*)"', text)
    if names:
        out["passages"] = set(names)
    m = re.search(r'<tw-storydata[^>]*\bname="([^"]*)"', text)
    if m:
        out["title"] = m.group(1)
    m = re.search(r'Config\.saves\.version = (\d+)', text)
    if m:
        out["schema"] = m.group(1)

    def obj(var):
        head = "<<set $%s = " % var
        i = text.find(head)
        if i == -1:
            return None
        i = text.find("{", i)
        if i == -1:
            return None
        depth, j = 0, i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        else:
            return None
        try:
            return json.loads(text[i:j + 1])
        except ValueError:
            # A build whose init object is not valid JSON is a broken build, and
            # guessing its keys with a regex would report a confident wrong answer.
            return None

    flags = obj("flags")
    if flags is not None:
        out["flags"] = set(flags)
    player = obj("player")
    if player is not None:
        out["player_traits"] = set(player.get("core_traits") or {})
    npcs = obj("npcs")
    if npcs is not None:
        out["npcs"] = set(npcs)
        out["npc_traits"] = {
            "%s.%s" % (slug, t)
            for slug, rec in npcs.items()
            for t in (rec.get("core_traits") or {})
        }
    return out


def _newest_archive(game_dir):
    """The highest-versioned `releases/v*.html`, preferring the free build.

    Sorted numerically, not lexically: `v0.1.10` is newer than `v0.1.9`, and a
    string sort puts it earlier. A `-paid` file is the same game with a different
    content set, so it carries the same join keys — taken only when it is the one
    copy of that version.
    """
    d = os.path.join(game_dir, "releases")
    if not os.path.isdir(d):
        return None, None
    best = None
    for fn in os.listdir(d):
        m = re.fullmatch(r"v(.+?)(-paid)?\.html", fn)
        if not m:
            continue
        ver, paid = m.group(1), bool(m.group(2))
        try:
            key = tuple(int(p) for p in ver.split("."))
        except ValueError:
            continue                        # not a numeric version — skip, do not guess
        cand = (key, not paid, ver, fn)     # free sorts above paid at equal version
        if best is None or cand > best:
            best = cand
    if best is None:
        return None, None
    return os.path.join(d, best[3]), best[2]


def saves_mode(slug, against=None, now_version=None):
    """Would this build break the saves of the last release?

    Exits NON-ZERO on any red, like `--release` — a save break reaches a player
    who has already spent hours, which is the most expensive thing a release can
    break. Additions are counted and never judged.

        gates.py --saves <slug>                    output/ vs the newest archive
        gates.py --saves <slug> 0.1.3              output/ vs a chosen archive
        gates.py --saves <slug> 0.1.3 0.1.7        two archives, after the fact

    The third form is not decoration: it reads history — two archives, after the
    fact, show passages a save could be parked on that went missing.
    """
    import html as _html

    root = os.getcwd()
    game_dir = os.path.join(root, "games", slug)
    build_path = os.path.join(game_dir, "output", "index.html")
    if against:
        cand = os.path.join(game_dir, "releases", f"v{against}.html")
        arch_path, arch_ver = (cand, against) if os.path.exists(cand) else (None, None)
        if arch_path is None:
            print(f"\n  no games/{slug}/releases/v{against}.html\n")
            return 2
    else:
        arch_path, arch_ver = _newest_archive(game_dir)

    R = []

    def check(name, ok, headline, detail=None):
        R.append((name, ok, headline, detail or []))

    print(f"\n  author-game-v2 save-compatibility check — {slug}")
    print(f"  {'─'*72}")

    if now_version:
        # Audit: diff two ARCHIVED releases instead of output/. Same code path, so a
        # question asked about history and one asked before shipping cannot disagree.
        cand = os.path.join(game_dir, "releases", f"v{now_version}.html")
        if not os.path.exists(cand):
            print(f"\n  no games/{slug}/releases/v{now_version}.html\n")
            return 2
        build_path = cand
    if not os.path.exists(build_path):
        print(f"  no games/{slug}/output/index.html — build it first\n")
        return 2
    if arch_path is None:
        print(f"  no games/{slug}/releases/v*.html to compare against.")
        print("  Nothing shipped yet, or step 3 of the release loop was skipped —")
        print("  `the-release.md` § Shipping the build. Without an archive there is no")
        print("  previous release to diff, and this check cannot run at all.\n")
        return 2

    print(f"  {'later   ' if now_version else 'now     '} "
          f"{os.path.relpath(build_path, root)}")
    print(f"  {'earlier ' if now_version else 'shipped '} "
          f"{os.path.relpath(arch_path, root)}")
    print(f"  {'─'*72}")

    now = _join_keys(_html.unescape(
        open(build_path, encoding="utf-8", errors="replace").read()))
    was = _join_keys(_html.unescape(
        open(arch_path, encoding="utf-8", errors="replace").read()))

    added = {}

    def compare(name, key, what, why, sample=6):
        old, new = was[key], now[key]
        if old is None or new is None:
            side = "the shipped build" if old is None else "this build"
            check(name, None, f"could not read {what} from {side} — not measured")
            return
        gone = sorted(old - new)
        added[key] = len(new - old)
        check(name, not gone,
              f"{len(old)} shipped, {len(new)} now, +{len(new - old)} added"
              if not gone else
              f"{len(gone)} {what} present in v{arch_ver} and GONE from this build",
              [] if not gone else
              [", ".join(gone[:sample]) + (f" … and {len(gone) - sample} more"
                                           if len(gone) > sample else ""),
               why])

    compare("no passage disappeared", "passages", "passages",
            "a save stores the passage it is parked on BY NAME — renaming a canvas, "
            "node or location id lands the player nowhere. the-returning-player.md §2")
    compare("no NPC key disappeared", "npcs", "NPC keys",
            "$npcs is keyed by the TOML id; a renamed NPC takes her whole "
            "relationship history with her. §2")
    compare("no flag disappeared", "flags", "flags",
            "the flag name IS the join between the scene that set it and the gate "
            "that reads it — a rename re-locks an earned door. §3")
    compare("no player meter disappeared", "player_traits", "player meters",
            "a renamed meter reads as undefined and the player is back at zero. §3")
    compare("no NPC meter disappeared", "npc_traits", "NPC meters",
            "same rule, per character. §3")

    if was["title"] is None or now["title"] is None:
        check("the title is unchanged", None, "could not read the story title")
    else:
        same = was["title"] == now["title"]
        check("the title is unchanged", same,
              f"{now['title']!r}" if same else
              f"{was['title']!r} → {now['title']!r}",
              [] if same else
              ["SugarCube namespaces in-browser save slots by slugify(title), so "
               "every existing slot disappears from the player's list. §5"])

    for name, ok, headline, detail in R:
        tag = "n/a " if ok is None else ("PASS" if ok else "FAIL")
        print(f"  [{tag}]  {name:30s} {headline}")
        for d in detail:
            print(f"          · {d}")

    judged = [r for r in R if r[1] is not None]
    npass = sum(1 for r in judged if r[1])
    print(f"  {'─'*72}")
    print(f"  {npass}/{len(judged)} save-compatibility checks pass")

    # ── printed, never judged ───────────────────────────────────────────────
    # The schema stamp moves whenever the trait/flag key SURFACE moves, which
    # includes every legitimate addition. Judging it would fail a release for
    # adding a flag — the exact shape that took R4 and P0 back out.
    print(f"  {'─'*72}")
    print(f"  note · schema stamp {was['schema']} → {now['schema']}"
          + ("  (unchanged)" if was["schema"] == now["schema"] else
             "  (moved — expected whenever a flag or meter is added)"))
    total_added = sum(v for v in added.values() if v)
    print(f"  note · {total_added} names added since v{arch_ver}, none of which can "
          "break a save")
    print("          (setup.backfillStateDefaults reaches them on the next passage — "
          "engine.md §40)")
    print("  ⚠️  a rescaled stat and a burned one-shot grant are invisible here and "
          "stay human —")
    print("          the-returning-player.md §4 and §6")
    print()
    return 0 if judged and npass == len(judged) else 1


# ─────────────────────────────────────────────────────────────────────────────
# --selfcheck — does SKILL.md still document what this script runs?
# ─────────────────────────────────────────────────────────────────────────────
# SKILL.md's scoreboard table is what an author reads WHEN A GATE FAILS, and it
# says so in its own words: "When a gate fails, look it up here. Nine of these
# used to be documented nowhere but in the script's own comments, so an author
# who hit one had nothing to read."
#
# That was closed by the 2026-08-16 whole-skill audit — "nine gates were
# documented in zero reference files, now indexed in SKILL.md (23/23 findable)".
# It REOPENED within twelve days: on 2026-08-28 the script emitted 44 gates and
# 27 lint headlines against an index missing five gates, eight lints and both
# alternate modes. Nothing anywhere would have said so, because nothing compared
# the script to the file that documents it.
#
# Documenting the missing rows fixes that day. This kills the class.
#
# ⚠️ It invents NO threshold, which is why it is safe to build where R4, study 6's
# anchoring check and P0 were not: it is a set difference over strings, and every
# name is read out of this file's own source rather than guessed. Proved exact
# before it was written — the regex below recovers 44 of 44 gate names with
# nothing extra in either direction, checked against `--json`.
#
# ⚠️ The comparison is SUBSTRING against the whole file, never cell-equality.
# SKILL.md legitimately packs several gate names into one table cell
# ("guidance exists · no chain ends in silence"); a cell-wise diff reports
# fourteen false gaps, which is exactly what the first attempt did.


def _emitted_names(src):
    """(gates, lints) this script can emit, read out of its own source.

    Static rather than run against a game on purpose: a game that declares no
    economy reports n/a and still emits the row, but a game missing a whole
    subsystem would hide names from a runtime listing and the check would go
    quiet exactly where the index is most likely to be stale.
    """
    gates = sorted(set(re.findall(r'\bgate\(\s*"([^"]+)"', src)))
    lints = sorted({m.strip() for m in
                    re.findall(r'print\(f"  lint · ([^—"]+?) *(?:—|\{)', src)})
    return gates, lints


def _documented_gate_names(skill):
    """Gate names SKILL.md's scoreboard table claims exist — the other direction.

    Scoped to the ONE table whose header row is `| gate | …`. SKILL.md carries
    several other tables (the state model, the phases, the modes) and an unscoped
    sweep reads their first cells as gate names: 8 false positives, measured. One
    cell can hold several names joined by `·`, so each cell is split.
    """
    names, inside = [], False
    for line in skill.splitlines():
        if re.match(r"^\|\s*gate\s*\|", line):
            inside = True
            continue
        if not inside:
            continue
        if not line.startswith("|"):
            break                       # the table ended
        if set(line) <= set("|-: "):
            continue                    # the |---|---| rule
        for part in line.split("|")[1].split("·"):
            part = part.strip().strip("*").strip()
            if part:
                names.append(part)
    return names


_RULE_DEF = re.compile(r"^(?:#{1,6}\s+|\*\*)([A-Z]{1,2}\d+[a-z]?)\s*·")
# A qualified reference names its file, so it can be resolved exactly. Backticks and a
# `references/` prefix are both in live use — `the-surfaces.md` R3b, `references/the-economy.md` R7 —
# and a regex that misses them turns three correct cross-file pointers into false orphans.
_RULE_QUALIFIED = re.compile(
    r"`?(?:references/)?([a-z][a-z0-9-]*\.md)`?\s+`?([A-Z]{1,2}\d+[a-z]?)`?\b")


def _rule_definitions(skill_dir):
    """{file -> set of rule ids it DEFINES}.

    A rule is defined by `## R6 · …` (a heading) or `**W1 · …**` (a bold lead). Both
    forms are in use and the `·` is what separates a definition from a mention.
    """
    out = {}
    for root, _, files in os.walk(os.path.join(skill_dir, "references")):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            ids = set()
            with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    m = _RULE_DEF.match(line)
                    if m:
                        ids.add(m.group(1))
            if ids:
                out[f] = ids
    return out


def _orphan_rules(skill_dir, defs):
    """Rules that are POINTED AT and never written. Returns (broken, unwritten).

    This exists because of a defect nothing in the toolchain could see. `the-voice.md`
    R6 was recorded as shipped in two ledgers, cited by this script, and listed in the
    file's own checks table — while the file itself read "The five rules" and stopped at
    R5. `git log -S "R6 · "` returned nothing: no commit had ever contained it. The name
    reconciliation above cannot help, because it compares GATE names, and a rule cited by
    a reference file with no section defining it is outside what it reads.

    Two directions, and they are NOT equally certain, so they are not reported the same:

      broken    a QUALIFIED reference — `the-voice.md R6` — names its own file, so the
                lookup is exact and a miss is a fact. These FAIL.

    ⚠️ SCOPED TO `references/` IN BOTH DIRECTIONS, and that is not tidiness. The rules
    live there; `CHANGELOG.md`, `DOCTRINE_GAPS.md` and `STATUS.md` are dated ledgers that
    MENTION them, including ones since deleted. Scanning the ledgers reported three
    "broken" pointers at `the-surfaces.md` R2b — a rule superseded on 2026-08-18 and
    recorded as such — and 118 bare hits, most of them gate numbers in changelog prose.
    A check that fires on an accurate history entry is the R4 error with a new face.

      unwritten a BARE reference inside the file that owns that letter family. This is
                the direction that would have caught R6, and it is prose: `the-phone.md`
                says "P0 … was withdrawn" and `the-surfaces.md` discusses a deleted R2b,
                both correct, neither a broken pointer. So it is a LIST TO EYEBALL and
                never a failure — the same restraint this file's own docstring records
                for lints, and the same one that took R4, study 6's anchoring check and
                P0 back out for inventing a threshold that failed a correct file.
    """
    broken, unwritten = [], []
    for root, _, files in os.walk(os.path.join(skill_dir, "references")):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, skill_dir)
            own = defs.get(f, set())
            families = {i[0] for i in own}
            bare = re.compile(r"\b(%s)(\d+[a-z]?)\b" % "|".join(sorted(families))) \
                if families else None
            with open(path, encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    qualified = set()
                    for tgt, rid in _RULE_QUALIFIED.findall(line):
                        qualified.add(rid)
                        if tgt in defs and rid not in defs[tgt]:
                            broken.append((rel, n, f"{tgt} {rid}"))
                    # A definition line is not a reference to itself, and an id already
                    # resolved against the file that OWNS it is not an orphan here: three
                    # of the five first hits were `the-surfaces.md` R3b and its kin — real
                    # cross-file pointers, correct, and only "undefined" locally.
                    if bare and not _RULE_DEF.match(line):
                        for fam, num in bare.findall(line):
                            if fam + num not in own and fam + num not in qualified:
                                unwritten.append((rel, n, fam + num))
    return broken, unwritten


_TOML_HDR = re.compile(r'^\s*(\[\[?[A-Za-z][\w.]*\]?\])\s*$')
_TOML_FLD = re.compile(r'^\s*#?\s*([a-z_][a-z0-9_]*)\s*=')


def _toml_fields_by_table(text, count_commented):
    """{table -> set of field names}, with a sub-table counted as a field of its parent.

    `[canvases.trigger.conditions]` IS the `conditions` field of `[canvases.trigger]`
    written long. Without that equivalence the comparison below reports every sub-table
    in the skill as a missing field — six false positives, measured.
    """
    out, tables, cur = collections.defaultdict(set), set(), None
    for ln in text.split("\n"):
        h = _TOML_HDR.match(ln)
        if h:
            cur = h.group(1).strip("[]")
            tables.add(cur)
            continue
        if cur is None:
            continue
        if not count_commented and ln.lstrip().startswith("#"):
            continue
        m = _TOML_FLD.match(ln)
        if m:
            out[cur].add(m.group(1))
    for t in tables:
        if "." in t:
            parent, leaf = t.rsplit(".", 1)
            out[parent].add(leaf)
    return out


def _template_field_gap(skill_dir):
    """{table -> fields} a reference TEACHES and no template SHOWS.

    ⚠️ THE ASYMMETRY IS DELIBERATE. A commented line in a REFERENCE is commentary — F5b's
    own `# npc = "npc_theo"  ← WRONG` is an anti-example, and counting it reported the very
    field the template had just been fixed to carry. A commented line in a TEMPLATE is
    still on the author's screen, so it counts as shown.
    """
    taught = collections.defaultdict(set)
    ref = os.path.join(skill_dir, "references")
    for f in sorted(os.listdir(ref)) if os.path.isdir(ref) else []:
        if not f.endswith(".md"):
            continue
        with open(os.path.join(ref, f), encoding="utf-8", errors="replace") as fh:
            for blk in re.findall(r"```toml\n(.*?)```", fh.read(), re.S):
                for t, fs in _toml_fields_by_table(blk, False).items():
                    taught[t] |= fs
    shown = collections.defaultdict(set)
    tpl = os.path.join(skill_dir, "templates")
    for f in sorted(os.listdir(tpl)) if os.path.isdir(tpl) else []:
        if not f.endswith(".toml"):
            continue
        with open(os.path.join(tpl, f), encoding="utf-8", errors="replace") as fh:
            for t, fs in _toml_fields_by_table(fh.read(), True).items():
                shown[t] |= fs
    # only tables a template actually defines — a reference may teach whole subsystems
    # (the phone, quest cards, the cheat page) that no template is meant to scaffold
    return {t: sorted(taught[t] - shown[t]) for t in sorted(set(taught) & set(shown))
            if taught[t] - shown[t]}


WORD_REFERENCE = 149_283   # SKILL.md + references/ when the IC programme began; not a cap (LO)
_HAND_COUNT = re.compile(r"(?<![/\d,])(\d+)\s+(gates|lints)\b")
# Spelled out too (IC17): "fifty-five lints" went stale the same way. Ten and up only —
# "two gates" is usually a subset, not a claim about the scoreboard.
_TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
         "eighty": 80, "ninety": 90}
_TEENS = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
          "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
_ONES = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
         "nine": 9}
_HAND_WORD = re.compile(
    r"\b(" + "|".join(_TENS) + r")(?:-(" + "|".join(_ONES) + r"))?\b\s+(gates|lints)\b"
    r"|\b(" + "|".join(_TEENS) + r")\b\s+(gates|lints)\b", re.I)


def _hand_counts(skill_dir, n_gates, n_lints):
    """Hand-written scoreboard counts that disagree with the script (IC14, LO 2026-09-28).

    "46 gates, 28 lints" was written into three files and went stale in all three. A doc
    should point at `--selfcheck` instead of writing the number; this row catches one that
    does and is wrong. Only a line about THE SCOREBOARD is read — one naming both gates and
    lints, or `gates.py`, or the scoreboard — because "2,235 gates" in a field table counts
    conditions in other games, not ours. A tally such as `29/49 gates pass` is a format and
    is skipped by the `/` before it. Returns [(file, line, "46 gates")].
    """
    import glob
    paths = [os.path.join(skill_dir, "SKILL.md")]
    paths += sorted(glob.glob(os.path.join(skill_dir, "references", "*.md")))
    paths += sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(skill_dir)),
                                           "agents", "v2-*.md")))
    out = []
    for path in paths:
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            low = line.lower()
            if not (("gate" in low and "lint" in low) or "gates.py" in low or "scoreboard" in low):
                continue
            for num, kind in _HAND_COUNT.findall(line):
                if int(num) != (n_gates if kind == "gates" else n_lints):
                    out.append((os.path.relpath(path, skill_dir), i, f"{num} {kind}"))
            for m in _HAND_WORD.finditer(line):
                tens, ones, k1, teen, k2 = m.groups()
                if tens:
                    val, kind = _TENS[tens.lower()] + (_ONES[ones.lower()] if ones else 0), k1
                else:
                    val, kind = _TEENS[teen.lower()], k2
                if val != (n_gates if kind.lower() == "gates" else n_lints):
                    out.append((os.path.relpath(path, skill_dir), i, m.group(0)))
    return out


def selfcheck_mode():
    """Does SKILL.md still describe the checks this script actually runs?

    Both directions, because the one-directional version shipped 2026-08-28 and
    the audit two days later found what it cannot see:

      · script -> SKILL.md   a check with no row. An author who hits it has
                             nothing to read.
      · SKILL.md -> script   a row with no check. G35 `the anchor introduces
                             itself` was deleted 2026-08-26 and its row sat in
                             the table for two days, sending authors at a device
                             the doctrine that replaced it tells them to avoid.

    Needs no game and touches none. Exits non-zero on a gap, like `--release`
    and unlike `--words`.

    ⚠️ LINTS ARE CHECKED ONE WAY ONLY. They live in a wrapped prose paragraph
    with no exact extraction; gates have a table. A reverse check on prose would
    fire on how a sentence was broken, and a check that fires wrongly is what
    took R4, study 6's anchoring check and P0 back out.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    skill_path = os.path.join(os.path.dirname(here), "SKILL.md")
    try:
        skill = open(skill_path, encoding="utf-8").read()
    except OSError as exc:
        print(f"cannot read {skill_path}: {exc}")
        return 2
    src = open(os.path.abspath(__file__), encoding="utf-8").read()

    # Whitespace-collapsed, because SKILL.md is wrapped prose: a lint named across
    # a line break IS documented, and a check that says otherwise sends the author
    # to reflow a paragraph instead of writing the row that is actually missing.
    flat = re.sub(r"\s+", " ", skill)

    gates, lints = _emitted_names(src)
    modes = ["--words", "--beat", "--release", "--saves", "--selfcheck", "--ship"]
    documented = _documented_gate_names(skill)

    missing_g = [g for g in gates if g not in flat]
    missing_l = [l for l in lints if l not in flat]
    missing_m = [m for m in modes if m not in flat]
    stale_g = [d for d in documented if d not in set(gates)]

    print(f"\n  author-game-v2 self-check — is the index current?")
    print(f"  {os.path.relpath(skill_path, os.getcwd())}")
    print(f"  {'─'*72}")
    for label, found, missing in (
            ("gates", gates, missing_g),
            ("lints", lints, missing_l),
            ("modes", modes, missing_m)):
        tag = "PASS" if not missing else "FAIL"
        print(f"  [{tag}]  {label:32s} {len(found)-len(missing)}/{len(found)} documented")
        for m in missing:
            print(f"          · undocumented: {m}")
    tag = "PASS" if not stale_g else "FAIL"
    print(f"  [{tag}]  {'gate rows':32s} "
          f"{len(documented)-len(stale_g)}/{len(documented)} still checked")
    for s in stale_g:
        print(f"          · documented but NOT emitted: {s}")

    skill_dir = os.path.dirname(here)
    rule_defs = _rule_definitions(skill_dir)
    broken, unwritten = _orphan_rules(skill_dir, rule_defs)
    n_rules = sum(len(v) for v in rule_defs.values())
    tag = "PASS" if not broken else "FAIL"
    print(f"  [{tag}]  {'rule pointers':32s} "
          f"{n_rules} rules across {len(rule_defs)} files, "
          f"{len(broken)} pointing at nothing")
    for rel, n, what in broken:
        print(f"          · {rel}:{n} points at {what} — no section defines it")
    stale_counts = _hand_counts(skill_dir, len(gates), len(lints))
    tag = "PASS" if not stale_counts else "FAIL"
    print(f"  [{tag}]  {'hand-written counts':32s} "
          f"{len(stale_counts)} disagree with the script ({len(gates)} gates · {len(lints)} lints)")
    for rel, n, what in stale_counts:
        print(f"          · {rel}:{n} says {what} — point at `gates.py --selfcheck` instead")
    print(f"  {'─'*72}")

    if unwritten:
        # A LIST, never a score. See `_orphan_rules`.
        print(f"  rule · referenced and not defined in its own file — "
              f"{len(unwritten)} to eyeball")
        for rel, n, rid in unwritten[:12]:
            print(f"          · {rel}:{n} says {rid}")
        if len(unwritten) > 12:
            print(f"          · … and {len(unwritten)-12} more")
        print("          (a withdrawn or superseded rule discussed as history is fine;")
        print("           a rule the file relies on and never wrote is the R6 defect)")
        print(f"  {'─'*72}")

    gap = _template_field_gap(skill_dir)
    if gap:
        print(f"  field · taught in a reference, shown in no template — "
              f"{sum(len(v) for v in gap.values())} to eyeball")
        for tbl in sorted(gap):
            print(f"          · [{tbl}]  {', '.join(sorted(gap[tbl]))}")
        print("          (a field a reference teaches and no template shows is a field")
        print("           authors miss — the author fills in the template, not the reference.")
        print("           A LIST, never a score — a template is not meant to carry every")
        print("           advanced field, and this cannot tell an omission from a decision)")
        print(f"  {'─'*72}")

    # The running total (IC19, LO 2026-09-28): SKILL.md + references/*.md, against the
    # programme's starting size. Printed on every run, never judged — LO set no hard cap; the
    # number is here so growth is seen the day it happens, not measured after the fact.
    # ⚠️ Counted by `wc -w`, the command every CHANGELOG running total has used. Python's
    # split() differs by ~440 words here (macOS wc treats the ⚠️ sign as a word of its own in
    # some positions), and a total that disagrees with the ledger is worse than none.
    import glob
    import subprocess
    paths = [skill_path] + sorted(glob.glob(os.path.join(skill_dir, "references", "*.md")))
    try:
        blob = b"".join(open(p, "rb").read() for p in paths)
        words = int(subprocess.run(["wc", "-w"], input=blob, capture_output=True,
                                   check=True).stdout.split()[0])
        print(f"  running total — {words:,} / {WORD_REFERENCE:,} words (SKILL.md + references/, wc -w)")
    except (OSError, subprocess.CalledProcessError, ValueError, IndexError):
        print("  running total — wc -w unavailable here; count SKILL.md + references/ by hand")
    print(f"  {'─'*72}")

    total = (len(missing_g) + len(missing_l) + len(missing_m) + len(stale_g) + len(broken)
             + len(stale_counts))
    if total:
        if missing_g or missing_l or missing_m:
            print(f"  {len(missing_g)+len(missing_l)+len(missing_m)} name(s) the script emits "
                  f"and SKILL.md does not carry.")
            print("  An author who hits one has nothing to read. Add the row, or rename the "
                  "check — the two are the same fix.")
        if stale_g:
            print(f"  {len(stale_g)} row(s) SKILL.md documents and the script no longer runs.")
            print("  Worse than a missing row: it sends an author to build for a check that is")
            print("  gone, and the doctrine that replaced it may say the opposite. Delete the")
            print("  row wherever it appears — the templates included.")
    else:
        print("  the index is current")
    print()
    return 1 if total else 0


# ─────────────────────────────────────────────────────────────────────────────
# --ship — the one check that is allowed to stop a publish
# ─────────────────────────────────────────────────────────────────────────────
# Added 2026-09-26 (PRD WS6, `~/Documents/Process_Review_20260925/PRD_SKILL_CHANGES.md`).
# Until now nothing read this script's verdict: no hook, no release script. The Process
# Review found the finish line moved every few days because nothing held it.
#
# It BLOCKS only what makes a build broken, unfinishable or untrue (LO, 2026-09-26), and
# REPORTS everything else for LO to judge when he plays. The two lists are fixed here and
# in `the-release.md`; a row moves between them only at a release boundary.
#
# `--release` and `--saves` are CALLED, not re-implemented, and their own output is left
# exactly as it was: their exit codes are read, and their [FAIL] lines are quoted.

SHIP_REPORT_GATES = [
    "prose has room", "somebody speaks", "every hub is met first", "an explicit beat carries a clip",
    "explicit floor", "location fill", "the walk-in floor", "traversal heat",
    "sentence length",
]
SHIP_BLOCK_GATES = {
    "ends on an opening": "the declared door works",
    "the obligation is charged": "the pressure can be paid or is signposted",
    "standing surface": "no empty rooms",
}


# Named for what it proves, not more (LO, 2026-09-26): the static half proves each step
# matches its canvas and each unlock can be earned; the played half sets the place and
# the clock per step and applies the declared gate, but never the counter. That is not
# "plays end to end", and the row does not say so.
SHIP_LADDER_ROW = "each step fires when unlocked, and each unlock is earnable"

# ── NEW BLOCK RULES WARN FIRST (LO B, PRD v2 §0.9; `the-release.md`) ────────────────
# A rule that makes a `--ship` BLOCK row stricter carries a `since` date. A game whose
# v2_state.json existed before that date is GRANDFATHERED: where the row is red under the
# new rule and green under the old one, it prints [WARN] "… blocks from your next release"
# instead of blocking — until the game records a release with `shipped` on or after the
# date, from which point the row blocks. A game started after the date is blocked from
# the start. Ordinary gates are never grandfathered: they may go red, and never stop a
# commit.
SHIP_GRANDFATHERED = frozenset({"members_only", "orientation", "probation", "the_balance",
                                "vesper_two"})
SHIP_SINCE = {
    # CK8b · H9: a person must be at the step's place for the WHOLE window, not any overlap.
    "full_cover": ("2026-09-30", SHIP_LADDER_ROW),
    # CK8b · I9: a substitution_only canvas's pay is not income of its own.
    "sub_income": ("2026-09-30", SHIP_BLOCK_GATES["the obligation is charged"]),
}
# The rules running in their OLD form. Empty except while `ship_rows` re-runs one row to
# ask whether a grandfathered game would have passed before the rule changed.
_LEGACY_RULES = set()


def _legacy(rule_id):
    return rule_id in _LEGACY_RULES


def _grandfathered(slug, state, since):
    """Is this game still warned, not blocked, by a rule dated `since`?"""
    if slug not in SHIP_GRANDFATHERED:
        return False
    return not any(str((r or {}).get("shipped") or "") >= since
                   for r in ((state or {}).get("releases") or []) if isinstance(r, dict))


def _ship_ladders(root, slug, game, state, people, player=None):
    """(ok, headline, detail) for the ladder row. `player(build, game, ladder)` returns
    reach_step's list; it is `playtest.reach_step` in a fresh browser unless a test
    hands in another."""
    ladders = dict(_declared_ladders(state))
    missing = [p for p in people if p not in ladders]
    if missing:
        return False, f"{len(missing)} of {len(people)} people on the release page have no ladder", \
            [f"{p}: no board.characters[].ladder — nothing says what their steps are"
             for p in missing]
    # The sub-ledger keeps the declared door, so the door's step is read as the door
    # here too (PRD v2 CK1 · H2).
    sub = {"board": {"characters": [
        ch for ch in (((state or {}).get("board") or {}).get("characters") or [])
        if ch.get("id") in people], "door": _declared_door(state)}}
    _, checked, probs = ladder_problems(game, sub)
    if probs:
        return False, f"{len(probs)} static problem(s) in {checked} steps — not played yet", probs[:10]
    build_path = os.path.join(root, "games", slug, "output", "index.html")
    if not os.path.exists(build_path):
        return False, "no build to play", [os.path.relpath(build_path, root)]
    if player is None:
        def player(build, g, lad):
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import playtest
            with playtest.open_game(build) as (page, errors):
                res = playtest.reach_step(page, g, lad, len(lad.get("steps") or []))
                if errors:
                    res.append(dict(n="-", canvas="-", reached=False,
                                    why=f"page error: {errors[0]}"))
                return res
    # The door's step is not played (PRD v2 CK1 · H2, LO 2026-09-30): it opens next
    # release, so this release's build cannot climb it, nor any step after it. The
    # ladder handed to the player stops just before it.
    door_canvas = (_declared_door(state) or {}).get("canvas")
    bad, unplayed = [], []
    for p in people:
        lad = ladders[p]
        steps = sorted(lad.get("steps") or [], key=lambda s: s.get("n", 0))
        at_door = next((s.get("n") for s in steps if s.get("canvas") == door_canvas), None)
        if at_door is not None:
            lad = dict(lad, steps=[s for s in steps if s.get("n", 0) < at_door])
            unplayed.append(f"{p} step {at_door} ({door_canvas})")
        try:
            res = player(build_path, game, lad)
        except Exception as e:                      # a harness that cannot run is not a pass
            bad.append(f"{p}: could not be played — {type(e).__name__}: {e}")
            continue
        want = len(lad.get("steps") or [])
        got = sum(1 for r in res if r.get("reached"))
        if got < want or any(not r.get("reached") for r in res):
            miss = next((r for r in res if not r.get("reached")), {})
            bad.append(f"{p}: reached {got} of {want} steps — step {miss.get('n')} "
                       f"({miss.get('canvas')}): {miss.get('why')}")
    if bad:
        return False, f"{len(bad)} of {len(people)} ladders stop before the top", bad
    door_note = (f" · not played, the door — opens next release: {', '.join(unplayed)}"
                 if unplayed else "")
    return True, (f"{checked} steps across {len(people)} people: each matches its canvas, "
                  f"each unlock is earnable, and each fired in the build" + door_note), []


def _capture(fn, *args):
    """(return code, printed lines) of a mode function, without letting it print."""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*args)
    return rc, buf.getvalue().splitlines()


def _fail_lines(lines):
    return [l.strip() for l in lines if l.strip().startswith("[FAIL]")]


def ship_rows(slug, root=None):
    """(block_rows, report_rows) for a game, each row (name, ok, headline, detail).

    ok is True / False / None; None means n/a (for a BLOCK row only where the thing
    genuinely does not apply yet, such as saves before a first release).
    """
    root = root or os.getcwd()
    path = os.path.join(root, "games", slug, "toml_phases", "7_final_game.toml")
    block, report = [], []

    def B(name, ok, headline, detail=None):
        block.append((name, ok, headline, detail or []))

    if not os.path.exists(path):
        B("the game builds from source", False, f"no {os.path.relpath(path, root)}")
        return block, report

    model, game = build(_load(path))
    state_path = os.path.join(root, "games", slug, "v2_state.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else None
    scored, _ = score(model, game, state, os.path.join(root, "games", slug))
    results = {r["gate"]: r for r in scored}
    rp = (state or {}).get("release_page") or {}

    # ── the four untrue or silent screens (lints promoted for shipping) ──────
    _tok_s, _tok_player, _tok_dev = lint_unresolved_tokens(game)
    B("no raw token on screen", not _tok_player,
      f"{len(_tok_player)} @token(s) on a surface the engine never resolves"
      if _tok_player else "every @token sits where the engine resolves it", _tok_player[:10])
    s, hits = lint_past_claim(game)
    B("no past claim on a repeatable", not hits,
      s or "no repeatable screen to check", hits[:10])
    s, hits = lint_printed_stat(game)
    B("no printed stat labels", not hits, s, hits[:10])
    s, mute = lint_one_time_speaks(game)
    B("a one-time step with a person speaks", not mute,
      s or "no one-time step bound to a person", mute[:10])
    s, rows = lint_opening_card(game)
    B("the opening's card has goals", bool(s) and "arms NO card" not in s,
      s or "the opening could not be read — no starting canvas", rows[:10])

    # ── unfinishable ────────────────────────────────────────────────────────
    people = rp.get("people") or []
    if not people:
        B(SHIP_LADDER_ROW, None,
          "the release page names nobody — 'the build matches the release page' is red for that")
    else:
        ok, head, detail = _ship_ladders(root, slug, game, state, people)
        B(SHIP_LADDER_ROW, ok, head, detail)
    signed = rp.get("signed_by_lo") is True and bool(rp.get("signed_at"))
    B("LO signed the playtest", signed,
      f"signed {rp.get('signed_at')}" if signed else
      "release_page.signed_by_lo / signed_at not set — LO plays every person on the "
      "release page from a new game to the door, then signs")

    # ── broken ──────────────────────────────────────────────────────────────
    rc, lines = _capture(release_mode, slug)
    B("the build exists and is a release build", rc == 0,
      "every --release check passes" if rc == 0 else
      f"gates.py --release {slug} fails", _fail_lines(lines))
    rc, lines = _capture(saves_mode, slug)
    if rc == 2:
        B("last release's saves still load", None,
          "no archived release to compare against — a first release has no saves to break")
    else:
        B("last release's saves still load", rc == 0,
          "every --saves check passes" if rc == 0 else f"gates.py --saves {slug} fails",
          _fail_lines(lines))
    for gname, label in SHIP_BLOCK_GATES.items():
        B(label, *_block_gate_verdict(gname, results.get(gname)))

    # ── untrue: the build against the page it claims to be ───────────────────
    if not rp:
        B("the build matches the release page", False,
          "no release_page in v2_state.json — nothing says what this release is")
    else:
        npc_ids = {n.get("id") for n in game.get("npcs") or []}
        missing = [p for p in (rp.get("people") or []) if p not in npc_ids]
        door_rp, door_b = rp.get("door"), ((state or {}).get("board") or {}).get("door")
        probs = [f"release_page names {p}, who is not in the build" for p in missing]
        if not rp.get("people"):
            probs.append("release_page.people is empty — the page names nobody")
        if door_rp and door_b and door_rp != door_b:
            probs.append(f"release_page.door {door_rp} is not board.door {door_b}")
        B("the build matches the release page", not probs,
          f"{len(rp.get('people') or [])} people on the page"
          + (f", door {door_rp.get('canvas')}" if isinstance(door_rp, dict) else ""), probs)

    # ── REPORT: printed for LO, never blocking ─────────────────────────────────
    for gname in SHIP_REPORT_GATES:
        r = results.get(gname)
        if r is None:
            continue
        head = r["headline"]
        if gname == "explicit floor":
            head += (" · field: per paragraph the median game is 4.4% and 8 of 26 meet 7.5%; "
                     "per passage the median is 28–33% and DoL, the source of 7.5%, is lowest")
        report.append((gname, None if r["na"] else r["pass_"], head, []))
    hints = step_hint_problems(game, state)
    if hints is None:
        report.append(("a hint line with place and time per step", None,
                       "n/a — no ladder declared", []))
    else:
        h_checked, h_probs = hints
        report.append(("a hint line with place and time per step", not h_probs,
                       f"{h_checked - len(h_probs)}/{h_checked} steps have a card that says "
                       f"where and when", h_probs[:10]))
    # Checkpoint A (IC16): the spine's decisions, from the ledger alone — `scripts/shape.py`.
    # REPORT, not BLOCK: the BLOCK list moves only at a release boundary (the-release.md).
    import shape as _shape
    _srows, _sflags = _shape.check(state, _shape.is_strict(state))
    _sbad = [f"{n}: {h}" for n, ok, h, _d in _srows if ok is False]
    _sjudged = [r for r in _srows if r[1] is not None]
    report.append(("the spine holds together", None if not _sjudged else not _sbad,
                   f"{len(_sjudged) - len(_sbad)}/{len(_sjudged)} spine checks pass "
                   f"(scripts/shape.py)" if _sjudged else "n/a — nothing on the spine yet",
                   _sbad[:10]))
    shown = set(SHIP_REPORT_GATES) | set(SHIP_BLOCK_GATES)
    others = [r for g, r in results.items() if g not in shown]
    red = [g for g, r in results.items() if g not in shown and not r["na"] and not r["pass_"]]
    report.append(("every other gate", not red,
                   f"{sum(1 for r in others if r['pass_'])}/"
                   f"{sum(1 for r in others if not r['na'])} pass",
                   [f"FAIL {g}" for g in red]))

    # ── LO B: a row red only under a rule newer than a grandfathered game WARNS ──
    # Re-run just that row with the rule in its old form. Red then too: it stays a FAIL.
    labels = {label: gname for gname, label in SHIP_BLOCK_GATES.items()}
    for rule, (since, label) in SHIP_SINCE.items():
        i = next((k for k, row in enumerate(block) if row[0] == label), None)
        if i is None or block[i][1] is not False or not _grandfathered(slug, state, since):
            continue
        _LEGACY_RULES.add(rule)
        try:
            if label == SHIP_LADDER_ROW:
                old_ok = _ship_ladders(root, slug, game, state, people)[0]
            else:
                old_scored, _ = score(model, game, state, os.path.join(root, "games", slug))
                gname = labels[label]
                old_ok = _block_gate_verdict(
                    gname, next((r for r in old_scored if r["gate"] == gname), None))[0]
        finally:
            _LEGACY_RULES.discard(rule)
        if old_ok is not False:
            name, _ok, head, detail = block[i]
            block[i] = (name, "warn", f"{head} — new since {since} ({rule}); blocks from your "
                                      f"next release", detail)
    return block, report


def _block_gate_verdict(gname, r):
    """(ok, headline, detail) for a gate promoted to a `--ship` BLOCK row."""
    if r is None:
        return False, f"gate '{gname}' did not run", []
    if r.get("parked") or r.get("few"):
        # PRD IC21: a parked block is never read as green, and says why it is red.
        return False, f"{gname}: {r['headline']}", r["detail"][:10]
    if r["na"] and gname != "the obligation is charged":
        return False, f"{gname}: n/a — {r['headline']} (an absence is not a pass)", r["detail"][:10]
    return (None if r["na"] else r["pass_"]), f"{gname}: {r['headline']}", r["detail"][:10]


def ship_mode(slug):
    """May this build reach a player? Exits NON-ZERO on any red BLOCK row."""
    block, report = ship_rows(slug)
    print(f"\n  author-game-v2 ship check — {slug}")
    print(f"  {'─'*72}")
    print("  BLOCK — broken, unfinishable or untrue. Any red row stops the publish.")
    for name, ok, head, detail in block:
        tag = ("WARN" if ok == "warn" else "n/a " if ok is None else
               ("PASS" if ok else "FAIL"))
        print(f"  [{tag}]  {name:42s} {head}")
        for d in detail:
            print(f"          · {d}")
    print(f"  {'─'*72}")
    print("  REPORT — for LO to judge when he plays. Never blocks.")
    for name, ok, head, detail in report:
        tag = "n/a " if ok is None else ("ok  " if ok else "red ")
        print(f"  [{tag}]  {name:42s} {head}")
        for d in detail:
            print(f"          · {d}")
    red = [b for b in block if b[1] is False]
    print(f"  {'─'*72}")
    print(f"  {'SHIP: yes' if not red else f'SHIP: NO — {len(red)} BLOCK row(s) red'}\n")
    return 1 if red else 0


def ship_targets(paths, root=None, portal=None):
    """Which slugs must pass --ship for a commit touching these paths.

    Used by scripts/hooks/pre-commit. A slug is checked when its build or the portal
    changes, it is a v2 game (it has v2_state.json — v1 games are never
    caught), and its portal entry is NOT `dev: true` (a test build passes through).
    """
    root = root or os.getcwd()
    entries = _portal_entries(root, portal) or {}
    slugs = set()
    for p in paths:
        m = re.match(r"games/([^/]+)/output/index\.html$", p)
        if m:
            slugs.add(m.group(1))
        elif p == _PORTAL_FILE:
            slugs |= {s for s, e in entries.items() if not e.get("dev")}
    out = []
    for s in sorted(slugs):
        if not os.path.exists(os.path.join(root, "games", s, "v2_state.json")):
            continue
        e = entries.get(s)
        if e is None or e.get("dev"):
            continue
        out.append(s)
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "--words":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --words <path/to/file>")
            sys.exit(2)
        sys.exit(words_mode(sys.argv[2]))
    if sys.argv[1] == "--beat":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --beat <path/to/beat.txt>")
            sys.exit(2)
        sys.exit(beat_mode(sys.argv[2]))
    if sys.argv[1] == "--release":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --release <game-slug>")
            sys.exit(2)
        sys.exit(release_mode(sys.argv[2]))
    if sys.argv[1] == "--saves":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --saves <game-slug> "
                  "[<shipped-version> [<compare-version>]]")
            sys.exit(2)
        sys.exit(saves_mode(sys.argv[2],
                            sys.argv[3] if len(sys.argv) > 3 else None,
                            sys.argv[4] if len(sys.argv) > 4 else None))
    if sys.argv[1] == "--selfcheck":
        sys.exit(selfcheck_mode())
    if sys.argv[1] == "--ship":
        if len(sys.argv) < 3:
            print("usage: python3 gates.py --ship <game-slug>")
            sys.exit(2)
        sys.exit(ship_mode(sys.argv[2]))
    if sys.argv[1] == "--ship-targets":
        # Internal, for scripts/hooks/pre-commit: staged paths in, slugs to check out.
        args, portal = sys.argv[2:], None
        if args[:1] == ["--portal"] and len(args) > 1:
            portal, args = args[1], args[2:]
        print("\n".join(ship_targets(args, portal=portal)))
        sys.exit(0)
    arg = sys.argv[1]
    path = arg if arg.endswith(".toml") else f"games/{arg}/toml_phases/7_final_game.toml"
    if not os.path.exists(path):
        # Before the build there is no TOML, and the ledger is what can be checked (PRD v2
        # DC9e · H16): point at shape.py rather than a bare "not found".
        if not arg.endswith(".toml") and os.path.exists(f"games/{arg}/v2_state.json"):
            print(f"no TOML yet: use shape.py {arg} (checkpoint A reads the ledger alone)")
        else:
            print(f"not found: {path}")
        sys.exit(2)

    model, game = build(_load(path))
    # The ledger, when it exists, tells the gates what the author DECLARED.
    game_dir = os.path.dirname(os.path.dirname(path))
    state_path = os.path.join(game_dir, 'v2_state.json')
    state = json.load(open(state_path)) if os.path.exists(state_path) else None
    results, parked_info = score(model, game, state, game_dir)

    lints = lint_dialogue_attribution(model)
    amb_summary, amb_lints = lint_ambient_presence(model, game)
    badge_summary, badge_lints = lint_badge_before_content(model, game)
    refusal_summary, refusal_lints = lint_refusal_shape(model, game)
    world_lints = lint_world_prose(model, game)
    face_summary, face_lints = lint_faceless_surfaces(game)
    tok_summary, tok_player, tok_dev = lint_unresolved_tokens(game)
    shape_summary, shape_lints = lint_screen_shape(model, game)
    label_summary, label_lints = lint_labels(model, game)
    sys_summary, sys_lints = lint_labels_and_systems(model, game, state)
    door_summary, door_lints = lint_doors(model, game)
    mute_summary, mute_lints = lint_mute_cards(game)
    unwritten_summary, unwritten_lints = lint_unwritten_act(model, game)
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
    gloss_rate, gloss_lints = lint_gloss(game)
    neg_share, neg_total, neg_lints = lint_negation(game)
    hist_share, hist_total, hist_lints = lint_history_repeatable(game)
    past_summary, past_lints = lint_past_claim(game)
    stat_summary, stat_lints = lint_printed_stat(game)
    speaks_summary, speaks_lints = lint_one_time_speaks(game)
    ends_summary, ends_lints = lint_scene_ends_on_nothing(game)
    arc_summary, arc_lints = lint_arc_ladder(game, state)
    silent_summary, silent_lints = lint_person_never_speaks(game)
    thought_summary, thought_lints = lint_thoughts_over_speech(game)
    opcard_summary, opcard_lints = lint_opening_card(game)
    fh_summary, fh_lints = lint_named_before_met(model, game)
    place_summary, place_lints = lint_place_function(model, game)
    role_summary, role_lints = lint_role_stays_attached(model, game)
    label_sum, label_rows = lint_role_label(game)
    clock_summary, clock_lints = lint_clock_in_prose(model, game)
    tcost_summary, tcost_lints = lint_time_cost_on_button(model, game)
    cur_summary, cur_lints = lint_currency_in_prose(model, game, state)
    price_summary, price_lints = lint_price_spelled_out(model, game, state)
    chan_summary, chan_lints = lint_money_channel(model, game, state)
    oblig_summary, oblig_lints = lint_obligation_vs_week(model, game, state)
    coll_summary, coll_lints = lint_collector_is_target(model, game, state)
    dep_summary, dep_lints = lint_paid_repeatable_deposits(model, game, state)
    grow_summary, grow_lints = lint_repeatables_without_step(model, state)
    reset_summary, reset_lints = lint_flag_never_resets(game, state)
    cheat_summary, cheat_lints = lint_cheat_page(game)
    tog_summary, tog_lints = lint_toggles_declared(game, state)
    joint_summary, joint_lints = lint_joints(game)
    (pron_rows, pron_note), event_rows, (vl_rows, vl_seen) = lint_readable(game)
    # The slug, for the one lint that reads the ARTEFACT rather than the source.
    # A bare `<slug>` argument is the slug; a `.toml` path is two directories under it.
    _slug = (os.path.basename(os.path.dirname(os.path.dirname(path)))
             if arg.endswith(".toml") else arg)
    vol_summary, vol_lints = lint_explicit_volume(_slug)

    if "--json" in sys.argv:
        _tp, _tf, _tk, _tw, _tn, _td = tally_counts(results)
        print(json.dumps({"gates": [dict(r) for r in results],
                          "tally": {"pass": _tp, "fail": _tf, "parked": _tk, "few": _tw,
                                    "na": _tn, "denominator": _td,
                                    "parked_files": parked_info["files"],
                                    "parked_errors": parked_info["errors"],
                                    "switched_off": sum(1 for r in results if r.get("switched_off")),
                                    "switched_off_canvases": parked_info["switched_off"]},
                          "lints": {"dialogue_attribution": lints,
                                    "world_prose": world_lints,
                                    "screen_shape": {"summary": shape_summary,
                                                     "findings": shape_lints},
                                    "labels": {"summary": label_summary,
                                               "findings": label_lints},
                                    "labels_and_systems": {"summary": sys_summary,
                                                           "findings": sys_lints},
                                    "doors": {"summary": door_summary,
                                              "findings": door_lints},
                                    "mute_cards": {"summary": mute_summary,
                                                   "findings": mute_lints},
                                    "unwritten_act": {"summary": unwritten_summary,
                                                      "findings": unwritten_lints},
                                    "browse_share": {"summary": browse_summary,
                                                     "findings": browse_lints},
                                    "ambient_presence": {"summary": amb_summary,
                                                         "findings": amb_lints},
                                    "badge_before_content": {"summary": badge_summary,
                                                             "findings": badge_lints},
                                    "refusal_shape": {"summary": refusal_summary,
                                                      "findings": refusal_lints},
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
                                    "place_function": {"summary": place_summary,
                                                       "findings": place_lints},
                                    "role_stays_attached": {"summary": role_summary,
                                                            "findings": role_lints},
                                    "clock_in_prose": {"summary": clock_summary,
                                                       "findings": clock_lints},
                                    "time_cost_on_button": {"summary": tcost_summary,
                                                            "findings": tcost_lints},
                                    "currency_in_prose": {"summary": cur_summary,
                                                          "findings": cur_lints},
                                    "price_spelled_out": {"summary": price_summary,
                                                          "findings": price_lints},
                                    "money_channel": {"summary": chan_summary,
                                                      "findings": chan_lints},
                                    "paid_repeatable_deposits": {"summary": dep_summary,
                                                                "findings": dep_lints},
                                    "repeatables_without_step": {"summary": grow_summary,
                                                                 "findings": grow_lints},
                                    "flag_never_resets": {"summary": reset_summary,
                                                          "findings": reset_lints},
                                    "cheat_page": {"summary": cheat_summary,
                                                   "findings": cheat_lints},
                                    "toggles_declared": {"summary": tog_summary,
                                                         "findings": tog_lints},
                                    "joints": {"summary": joint_summary,
                                               "findings": joint_lints},
                                    "pronoun_nobody": {"note": pron_note,
                                                       "findings": pron_rows},
                                    "past_event_not_given": {"findings": event_rows},
                                    "short_lines_no_verb": {"sentences": vl_seen,
                                                            "findings": vl_rows},
                                    "obligation_vs_week": {"summary": oblig_summary,
                                                           "findings": oblig_lints},
                                    "collector_is_target": {"summary": coll_summary,
                                                            "findings": coll_lints},
                                    "past_claim": {"summary": past_summary,
                                                   "findings": past_lints},
                                    "printed_stat": {"summary": stat_summary,
                                                     "findings": stat_lints},
                                    "arc_ladder": {"summary": arc_summary, "findings": arc_lints},
                                    "scene_ends_on_nothing": {"summary": ends_summary,
                                                              "findings": ends_lints},
                                    "person_never_speaks": {"summary": silent_summary,
                                                            "findings": silent_lints},
                                    "one_time_speaks": {"summary": speaks_summary,
                                                        "findings": speaks_lints},
                                    "thoughts_over_speech": {"summary": thought_summary,
                                                             "findings": thought_lints},
                                    "opening_card": {"summary": opcard_summary,
                                                     "findings": opcard_lints}}},
                         indent=1, default=str))
        # ⚠️ 2026-09-26 (PRD WS5): this used to `return` and exit 0 whatever the gates said,
        # so a caller reading --json could never see a failure. Same code as the text mode.
        j_judged = sum(1 for r in results if not r.get("na"))
        j_pass = sum(1 for r in results if r.get("pass_"))
        sys.exit(0 if j_judged and j_pass == j_judged else 1)

    name = (game.get("project") or {}).get("name") or os.path.basename(path)
    npass, nfail, npark, nfew, nna, denom = tally_counts(results)
    print(f"\n  author-game-v2 gates — {name}")
    print(f"  {path}")
    print(f"  {'─'*72}")
    for r in results:
        tag = ("park" if r.get("parked") else "few " if r.get("few") else
               "off " if r.get("switched_off") == "na" else
               "n/a " if r.get("na") else ("PASS" if r["pass_"] else "FAIL"))
        print(f"  [{tag}]  {r['gate']:32s} {r['headline']}")
        for d in r["detail"][:12]:
            print(f"          · {d}")
        if len(r["detail"]) > 12:
            print(f"          · … and {len(r['detail'])-12} more")
    print(f"  {'─'*72}")
    for f, err in parked_info["errors"]:
        print(f"  parked: {os.path.relpath(f, game_dir) if os.path.isabs(f) or os.sep in f else f}"
              f" could not be merged — {err}")
    # PRD IC21 (LO, 2026-09-27): parked and too-few count in the denominator as NOT
    # passing, so neither can raise the score; n/a stays out.
    # Switched-off canvases (LO, 2026-09-28): a gate that passes only with them counted
    # is a FAIL, and the line says how many fails are [off] so the reason is visible.
    noff = sum(1 for r in results if r.get("switched_off"))
    off_note = (f" ({noff} [off] — switched-off canvases counted)" if noff else "")
    print(f"  {npass}/{denom} gates pass  ·  {nfail} fail{off_note}  ·  {npark} parked, not judged  ·  "
          f"{nfew} too few to judge  ·  {nna} n/a (nothing authored)")

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

    if refusal_summary:
        print(f"  {'─'*72}")
        print(f"  lint · which refusals are shown at all — {refusal_summary}")
        for h in refusal_lints[:14]:
            print(f"          · {h}")
        if len(refusal_lints) > 14:
            print(f"          · … and {len(refusal_lints)-14} more")
        print("          (engine.md §15 says what a shown row must SAY and nothing about how"
              " many to show. The field's default is silence — 71% of 16,167 refusals render")
        print("           nothing, per-game median 79% silent across a 22-100% range, which the"
              " study calls \"a house decision, not a genre norm\". A LIST, never a score.")
        print("           A row gated on a bar THIS SCENE moves is the machinery narrating its"
              " own progress bar; a row gated on something the player goes elsewhere and")
        print("           fixes is a real handle and worth speaking. Length: a refusal is a"
              " 9-word UI label; a DOOR is in-fiction)")

    if badge_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the badge arrives before the content — {badge_summary}")
        for h in badge_lints[:16]:
            print(f"          · {h}")
        if len(badge_lints) > 16:
            print(f"          · … and {len(badge_lints)-16} more")
        print("          (engine.md §23 — Frame 1 fires on `terminal === true` ALONE, ahead of"
              " ready and goals, and nothing checks achievement. A LIST, never a score:")
        print("           \"content\" here is a canvas condition reading the same (character,"
              " trait), which is a proxy. The fix a [badge] row points at is not a bigger")
        print("           number — a meter is the wrong thing to gate a badge on. Put the ✓ on"
              " a FLAG the content sets on its way out, so it means \"you played this\")")

    if amb_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the ambient puts him in the room — {amb_summary}")
        for h in amb_lints[:16]:
            print(f"          · {h}")
        if len(amb_lints) > 16:
            print(f"          · … and {len(amb_lints)-16} more")
        print("          (the OTHER half of G38, on the path that actually reads the field"
              " — checkRandomEncounters, v2.py:5245. A LIST, never a score: an ambient may")
        print("           legitimately place someone off-schedule, and the prose is where"
              " that is said. Two different fixes — `gate it` is one line of requires_npc;")
        print("           `or narrate` means no row exists here, so a gate would strand the"
              " canvas and the arrival belongs in the prose instead)")

    if unwritten_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the act between the click and the number — {unwritten_summary}")
        for h in unwritten_lints[:16]:
            print(f"          · {h}")
        if len(unwritten_lints) > 16:
            print(f"          · … and {len(unwritten_lints)-16} more")
        print("          (the-surfaces.md R9 — a LIST, never a score. A location exit"
              " that fires nothing is R7's door and is fine. One that fires effects is")
        print("           an ACT that happens to end in a room, and the engine shows it"
              " as a 2-second numeric toast: the approach is written, the outcome is a")
        print("           number, and the act between them was never authored. A WORK"
              " rung may resolve to a toast — nobody needs a paragraph about stacking")
        print("           shelves. A rung aimed at a PERSON, or at her own body, may"
              " not. The repair is one follow-up node, and several gated choices can")
        print("           share it — route them into one banded follow-up node."
              " ⚠️ Field range is 0-68%, so there is no threshold")
        print("           to set here that would not fail a game for obeying the"
              " doctrine — which is why this cannot fail anything)")

    if mute_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the guidance page says nothing — {mute_summary}")
        for h in mute_lints[:12]:
            print(f"          · {h}")
        if len(mute_lints) > 12:
            print(f"          · … and {len(mute_lints)-12} more")
        print("          (the-voice.md R3 — a LIST, never a score. A card with no"
              " `goals`, no `ready_canvas` and not `terminal` renders its flavour text")
        print("           and then nothing at all (v2.py:15974-15976), because"
              " evaluateGoals reports allMet vacuously for an empty list. The engine's")
        print("           own comment calls that shape intentional for transitional"
              " cards between capstones, so ONE mute card is fine and cannot be failed.")
        print("           The row worth reading is a character ALL of whose cards are"
              " mute: their section of the page never says what to do. That is the")
        print("           corpus's most-punished defect — in-her-own-hands ships 136"
              " passages for one character behind hints reading \"complete another")
        print("           task\", and its players quote it back. Trait goals already"
              " print the number themselves — label — current / target)")

    if door_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a door opens onto something — {door_summary}")
        for h in door_lints[:16]:
            print(f"          · {h}")
        if len(door_lints) > 16:
            print(f"          · … and {len(door_lints)-16} more")
        print("          (the-map.md R6-R6c — a LIST, never a score, and it cannot fail"
              " anything. A door is the threshold screen the player lands on INSTEAD of")
        print("           the room. It belongs to a PERSON'S HOME and it is rare: DoL"
              " carries six named doors in a 15,626-passage game. Presence is not")
        print("           the test. The"
              " field never SKIPS a threshold either (become-someone: 54 door screens,")
        print("           50 gating on occupancy, none skipped); what it makes"
              " conditional is whether the door exists at all. ⚠️ Declaring another door")
        print("           makes this output worse, not better, which is the only reason"
              " it is checked. Silent on a game that declares none, by design)")

    if sys_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the labels and the systems agree — {sys_summary}")
        for h in sys_lints[:16]:
            print(f"          · {h}")
        if len(sys_lints) > 16:
            print(f"          · … and {len(sys_lints)-16} more")
        print("          (the-systems.md SY1-SY3 — a LIST, never a score, and it cannot fail"
              " anything. `serves` is what happens in a room; `labels` is what KIND of place")
        print("           it is. An AMBIENT system is fed by nearly every room and so makes no"
              " room special; a SOURCED one is fed in one or two places and read all over —")
        print("           measured in family-ties, piercings 2 rooms → 117 read sites, clothes"
              " 1 → 53. A game of only ambient systems ships a duty list.")
        print("           ⚠️ Declaring MORE labels makes this output worse, not"
              " better — that direction is the only reason it is checked at all)")

    if label_summary:
        print(f"  {'─'*72}")
        print(f"  lint · room-list labels — {label_summary}")
        for h in label_lints[:8]:
            print(f"          · {h}")
        if label_lints:
            print("          (the-voice.md R1 — a NUMBER, not a bar; any threshold would be"
                  " invented. The register lives in the paragraph the click"
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
    # lint · she permits or she acts. Measured 2026-08-28, the corpus-verb study.
    #
    # The field puts the ACT on the button: across 113,134 clickable labels, `fuck` 1,349,
    # `cum` 1,073, `blowjob` 492, `missionary` and `doggy` 778 between them. `let` is 779
    # — 0.69% of all labels.
    #
    # A game can invert it: when `Let him…` concentrates inside the sex loops, outside the
    # bedroom she takes, asks, works and buys, and inside it she almost only permits. The
    # prose is explicit and the button is a permission, so the verb collapses at exactly
    # the moment the content is supposed to be hottest.
    #
    # ⚠️ REPORTED, NEVER JUDGED. `let` is a proxy for "this choice grants rather than does",
    # and a proxy is not a defect: a permission is the right button in a scene about being
    # used. No threshold is defensible from one marker, and the field figure is a
    # different measurement (field labels include navigation; this reads authored choice
    # text). It prints the share and stops.
    # computed here rather than reused from run_gates — different function, different scope
    _all_ch = [ch.get("text") for c in (game.get("canvases") or [])
               for n in (c.get("nodes") or [])
               for ch in ((n.get("exit_block") or {}).get("choices") or [])
               if isinstance(ch.get("text"), str)]
    permit = [t for t in _all_ch if re.match(r"^\s*let\b", t, re.I)]
    if _all_ch:
        loop_ids = {c.get("id") for c in (game.get("canvases") or [])
                    if re.search(r"loop|sex|fuck|serve|climax", str(c.get("id") or ""))}
        loop_ch = [ch.get("text") for c in (game.get("canvases") or []) if c.get("id") in loop_ids
                   for n in (c.get("nodes") or [])
                   for ch in ((n.get("exit_block") or {}).get("choices") or [])
                   if isinstance(ch.get("text"), str)]
        loop_let = [t for t in loop_ch if re.match(r"^\s*let\b", t, re.I)]
        bits = [f"{len(permit)}/{len(_all_ch)} choices open with `let` "
                f"({len(permit)/len(_all_ch)*100:.1f}%)"]
        if loop_ch:
            bits.append(f"inside sex loops {len(loop_let)}/{len(loop_ch)} "
                        f"({len(loop_let)/len(loop_ch)*100:.0f}%)")
        print(f"  lint · she permits or she acts — " + " · ".join(bits))
        for t in permit[:4]:
            print(f"          · {t.strip()[:70]!r}")
        print("          (reported, never judged. The field puts the act on the button — `fuck`"
              " 1,349, `cum` 1,073, `blowjob` 492 across 113,134 labels, against `let` at 0.69%."
              " A permission is the right button in a scene about being used; a game where it is"
              " the ONLY button has moved the act into the prose and left the player granting"
              " consent to a paragraph. the-voice.md R6 has the worked rewrites)")

        print(f"  lint · the act nodes — {act_summary}")
        for h in act_lints[:10]:
            print(f"          · {h}")
        print("          (register.md — the beat the player is IN while it is happening. `explicit"
              " floor` is a game-wide share and a game can clear it with every act node warm."
              " 3 is the count `explicit floor` needs to call a beat"
              " explicit at all, not a new threshold)")

    if rung_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the meter ladder — {rung_summary}")
        for h in rung_lints[:8]:
            print(f"          · {h}")
        print("          (the-meters.md W4 — a NUMBER, never a bar. 15/35/55/75 is the DoL"
              " seed's spacing, one game's, not a ladder to copy. The"
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
              " that gates)")

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
        print("           The field runs locale-locked nouns at 0.8 per 10k words."
              " Invented words are safe — the fiction builds them; real regional")
        print("           objects are the trap, because they look defined and are not. Gloss it"
              " in the sentence that first uses it, or use the plain word.")
        print("           [ambiguous] and [false friend] rows come from a CURATED list, not the"
              " corpus — a false friend is by definition a common word, so genre_words.txt")
        print("           is structurally blind to them. Expect false positives and read them:"
              " a `torch` that is a cutting torch is correct everywhere)")

    if gloss_lints:
        print(f"  {'─'*72}")
        print(f"  lint · the sentence explains itself — {len(gloss_lints)} gloss(es), "
              f"{gloss_rate:.2f} per 1,000 words")
        for h in gloss_lints[:10]:
            print(f"          · {h['canvas']}: …{h['line']}")
        if len(gloss_lints) > 10:
            print(f"          · … and {len(gloss_lints)-10} more")
        print("          (register.md 'The load rules' L1 — a LIST, never a score. A fact followed"
              " by an explanation of the fact, welded into one sentence.")
        print("           Field over 27 games: p50 0.06, p90 0.19, MAX 0.24 (destroyer).")
        print("           Delete the clause or make it its own"
              " sentence; deletion is the default, because the fact was")
        print("           usually already doing the work. A dash or a bracket is NOT the fix —"
              " the joint survives the swap)")

    if neg_lints or neg_share > FIELD_NEGATION_MAX:
        print(f"  {'─'*72}")
        print(f"  lint · what did not happen — {neg_share:.1f}% of {neg_total} sentences carry a "
              f"negation")
        for h in neg_lints[:8]:
            print(f"          · {h['canvas']}: {h['share']:.0f}% ({h['n']}/{h['of']}) — {h['line']}")
        if len(neg_lints) > 8:
            print(f"          · … and {len(neg_lints)-8} more canvases over the field max")
        print("          (register.md L2, RETIRED 2026-09-24 for the loud voice. Printed for"
              " reference only: a FIGURE and a LIST, never a score, and not a rule."
              f" Field, NARRATION ONLY, 25 games: p50 {FIELD_NEGATION_P50}%,")
        print(f"           p90 {FIELD_NEGATION_P90}%, MAX {FIELD_NEGATION_MAX}%"
              " (become-taxi-driver). Behind almost"
              " every negation is")
        print("           a positive fact that is shorter AND more specific — 'it takes you ninety'"
              " beats 'you have never once done it in forty-five'.")
        print("           Canvases listed are those over the field max with 8+ sentences. Baseline"
              " re-measured 2026-09-01: the old figures were taken")
        print("           with a regex blind to every contraction and against an ALL-TEXT field"
              " while this reads narration only — see NEGATION_RE)")

    if hist_lints:
        print(f"  {'─'*72}")
        print(f"  lint · history on a repeatable screen — {len(hist_lints)} of {hist_total} "
              f"sentences ({hist_share:.1f}%)")
        for h in hist_lints[:10]:
            print(f"          · {h['canvas']} [{h['marker']}]: {h['line']}")
        if len(hist_lints) > 10:
            print(f"          · … and {len(hist_lints)-10} more")
        print("          (register.md 'The load rules' L3 — a LIST, never a score. REPEATABLE"
              " canvases only: the same sentence on a one-time canvas is")
        print("           where the doctrine says to PUT it. Field over 27 games: p50 1.64%,"
              " p90 3.94%, MAX 5.41% (free-cities).")
        print("           The marker set is temporal (used to / ago / since /"
              " has been / N days-weeks-months-years) and it OVER-COUNTS a")
        print("           sentence that merely mentions a duration — read the lines, not the"
              " number. Clock time is a different rule and belongs to")
        print("           the-clock.md C2; this one is elapsed time)")

    if past_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a repeatable claims a past — {past_summary}")
        for h in past_lints[:10]:
            print(f"          · {h}")
        if len(past_lints) > 10:
            print(f"          · … and {len(past_lints)-10} more")
        print("          (register.md 'The truth rule' rule 2 and L3 — a LIST, never a score."
              " Legal inside a group gated on the flag that records the past;")
        print("           any conditioned group is skipped, so this under-reports. Speech"
              " counts too: a character can lie about a past the player never had)")

    if stat_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a printed stat is real — {stat_summary}")
        for h in stat_lints[:10]:
            print(f"          · {h}")
        print("          (the-meters.md 'What the player is shown' — numbers are shown and named;"
              " a +X for a stat that does not exist")
        print("           is the defect. A LIST, never a score)")

    if speaks_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a one-time step speaks — {speaks_summary}")
        for h in speaks_lints[:10]:
            print(f"          · {h}")
        if len(speaks_lints) > 10:
            print(f"          · … and {len(speaks_lints)-10} more")
        print("          (register.md 'The voice — say it loud' rule 5 and L3 — the one-time"
              " step carries the conversation. A LIST, never a score)")

    if arc_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the arc ladder — {arc_summary}")
        for h in arc_lints[:10]:
            print(f"          · {h}")
        print("          (the-arc.md A1 — one or two long chains for the central people. A LIST,"
              " never a score)")

    if ends_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a scene ends on nothing — {ends_summary}")
        for h in ends_lints[:8]:
            print(f"          · {h}")
        print("          (register.md 'What a scene contains', test 3 — the hook. A LIST for"
              " v2-reader, never a score: a last line that points forward is fine)")

    if silent_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a person who never speaks — {silent_summary}")
        for h in silent_lints[:8]:
            print(f"          · {h}")
        print("          (register.md 'What a scene contains', test 1 — the want. A LIST,"
              " never a score)")

    if thought_summary:
        print(f"  {'─'*72}")
        print(f"  lint · thoughts outweigh speech — {thought_summary}")
        for h in thought_lints[:10]:
            print(f"          · {h}")
        if len(thought_lints) > 10:
            print(f"          · … and {len(thought_lints)-10} more")
        print("          (register.md rule 3 and S3 — her thoughts go beside the dialogue,"
              " never instead of it. A LIST, never a score)")

    if opcard_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the opening arms a card with goals — {opcard_summary}")
        for h in opcard_lints[:10]:
            print(f"          · {h}")
        print("          (the-first-hour.md F1b step 5 — the first objective is a quest card"
              " with goal steps. A LIST, never a score)")

    if fh_summary:
        print(f"  {'─'*72}")
        print(f"  lint · named before met — {fh_summary}")
        for h in fh_lints[:14]:
            print(f"          · {h}")
        if len(fh_lints) > 14:
            print(f"          · … and {len(fh_lints)-14} more")
        print("          (the-first-hour.md F7 — a LIST, never a score. The game does not"
              " use a name until it has earned it: before the player has met somebody, say")
        print("           what they ARE and where; after, say the name. A character named in"
              " passing is fine — read the rows and make the call. degrees-of-lewdity swaps")
        print("           the description for the name on the meeting flag in 64 places)")

    if label_sum:
        print(f"  {'─'*72}")
        print(f"  lint · the label under the name — {label_sum}")
        for h in label_rows[:12]:
            print(f"          · {h}")
        if len(label_rows) > 12:
            print(f"          · … and {len(label_rows)-12} more")
        print("          (the-first-hour.md F10 — a LIST, never a score. `npcs[].role` is the"
              " 1-3 word label the engine prints under the name in EVERY dialogue box;"
              " `relationship` is the cast page's sentence and does NOT render there. Absent"
              " is legal and renders no line. READ THE"
              " LABELS: each must answer WHO THIS PERSON IS. `professor` and `mother`"
              " pass; `the nine-thirty` names an hour and `pays the rent` names a"
              " fact)")

    if role_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the role stays attached — {role_summary}")
        for h in role_lints[:12]:
            print(f"          · {h}")
        print("          (the-first-hour.md F10 — a LIST, never a score. F7 puts the role on"
              " screen at the meeting; this asks whether it is still there on the fortieth")
        print("           visit. Anchors come from each character's OWN relationship line, not"
              " from a kin list — a fixed kin list fires wrongly on any cast that")
        print("           is not family. Do not swap the"
              " NAME out for the relation: destroyer is the only game of 26 that does, and it")
        print("           has one of each relation. Both, at the point of use)")

    if place_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the place says what it is — {place_summary}")
        for h in place_lints[:14]:
            print(f"          · {h}")
        if len(place_lints) > 14:
            print(f"          · … and {len(place_lints)-14} more")
        print("          (the-first-hour.md F9 — a LIST, never a score. The description is"
              " the only surface a player sees on EVERY visit, so it is where a place says")
        print("           what it is. Read whether each one names the FUNCTION.")
        print("           This replaced a gate requiring a first-visit canvas: that"
              " device is 1 of 26 games (DoL 258 branches; 18 games have none))")

    if clock_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the clock in the prose — {clock_summary}")
        for h in clock_lints[:16]:
            print(f"          · {h}")
        if len(clock_lints) > 16:
            print(f"          · … and {len(clock_lints)-16} more")
        print("          (the-clock.md C2 — a LIST, never a score. Read each line at the LAST"
              " minute of the window beside it: a RULE is still true there and is correct")
        print("           work (\"Nobody comes in before eleven on a Monday\"); a READING is"
              " not (\"Doors open at nine\", true for 1 minute of 300). The turn is")
        print("           grammatical — the reading becomes a rule and the fact survives:"
              " \"The doors open at nine\")")

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
              " the time)")

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

    if chan_summary:
        print(f"  {'─'*72}")
        print(f"  lint · money gates content, or only prices it — {chan_summary}")
        for h in chan_lints[:10]:
            print(f"          · {h}")
        if len(chan_lints) > 10:
            print(f"          · … and {len(chan_lints)-10} more")
        print("          (the-economy.md R1 — a LIST, never a score. A CONDITION on the currency"
              " means content exists that money opens; a `costs` block means a thing can be"
              " bought. Gate 16 passes on either, deliberately — but the field runs a median"
              " 67.3 money conditions per 1,000 passages and every sandbox has some)")

    if oblig_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the obligation against the week — {oblig_summary}")
        for h in oblig_lints[:10]:
            print(f"          · {h}")
        print("          (the-economy.md R3 — a FIGURE, never a score: any threshold would"
              " fail a game for obeying the doctrine. Declare board.economy.week_income; an undeclared week is not a pass)")

    if coll_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the collector is also the target — {coll_summary}")
        for h in coll_lints[:6]:
            print(f"          · {h}")
        print("          (the-want.md §4a — a RANK, never a score. The field's collector is"
              " never the top explicit figure, but DoL makes its collector both deliberately, so a"
              " threshold here would fail a game for a legitimate design)")

    if dep_summary:
        print(f"  {'─'*72}")
        print(f"  lint · what a paid repeatable leaves behind — {dep_summary}")
        for h in dep_lints[:10]:
            print(f"          · {h}")
        if len(dep_lints) > 10:
            print(f"          · … and {len(dep_lints)-10} more")
        print("          (the-economy.md R1c — a RATE, never a score. A pure sink is not a"
              " defect; a game made only of pure sinks is. No threshold has been measured,"
              " so none is set)")

    if grow_summary:
        print(f"  {'─'*72}")
        print(f"  lint · repeatables without a step — {grow_summary}")
        for h in grow_lints[:10]:
            print(f"          · {h}")
        if len(grow_lints) > 10:
            print(f"          · … and {len(grow_lints)-10} more")
        print("          (PRD WS4 — a LIST, never a score. More to do at the same step is"
              " fine; a release that only adds repeatables has moved nobody on)")

    if reset_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a flag that never resets — {reset_summary}")
        for h in reset_lints[:10]:
            print(f"          · {h}")
        if reset_lints:
            print("          (a LIST, never a score. The name promises a reset the game never runs:"
                  " once set, it holds for the whole save. Clear it in [engine.daily_tick], or"
                  " rename it if it really is once-per-save — engine.md §28)")

    print(f"  {'─'*72}")
    print(f"  lint · a cheat page exists — {cheat_summary}")
    for h in cheat_lints[:10]:
        print(f"          · {h}")
    if cheat_lints:
        print("          (a LIST, never a score. Cut a basic on purpose if the game cannot use it;"
              " a time-saver behind a code is the one thing SY7 says to give away — engine.md §48)")

    print(f"  {'─'*72}")
    print(f"  lint · toggles declared — {tog_summary}")
    for h in tog_lints[:12]:
        print(f"          · {h}")
    if tog_lints:
        print("          (a LIST, never a score. A toggle is a start-choice flag every canvas of its"
              " kind reads; one no canvas reads switches nothing — the-surfaces.md R5b.4)")

    if joint_summary:
        print(f"  {'─'*72}")
        print(f"  lint · the joints — {joint_summary}")
        for h in joint_lints:
            print(f"          · {h}")
        print("          (a LIST, never a score. `prose has room` judges `but` and `and`; the"
              " ratio and the glosses are for reading — register.md, \"Joints\" and L1)")

    print(f"  {'─'*72}")
    print(f"  lint · a pronoun with nobody to point at — "
          f"{pron_note or f'{len(pron_rows)} screen(s) or place(s)'}")
    for h in pron_rows[:10]:
        print(f"          · {h}")
    if pron_rows:
        print("          (a LIST, never a score. Put the person on screen before the pronoun:"
              " a role, a name, or a token — register.md, \"A pronoun needs someone\")")

    if event_rows:
        print(f"  {'─'*72}")
        print(f"  lint · a past event the player was never given — {len(event_rows)} line(s)")
        for h in event_rows[:10]:
            print(f"          · {h}")
        print("          (a LIST, never a score. Gate the line on the flag that records it,"
              " or cut it — register.md, \"The truth rule\")")

    vl_share = 100 * len(vl_rows) / vl_seen if vl_seen else 0.0
    print(f"  {'─'*72}")
    print(f"  lint · short lines with no verb — {len(vl_rows)} of {vl_seen:,} sentences "
          f"({vl_share:.1f}%; field p25 {FIELD_FRAGMENT_SHARE[0]} · median "
          f"{FIELD_FRAGMENT_SHARE[1]} · p75 {FIELD_FRAGMENT_SHARE[2]})")
    for h in vl_rows[:8]:
        print(f"          · {h}")
    if vl_rows:
        print("          (a LIST, never a score, and approximate: a curated verb list, no tagger."
              " A fragment is a choice, not a defect — read them)")

    if vol_summary:
        print(f"  {'─'*72}")
        print(f"  lint · how much explicit content is in here — {vol_summary}")
        for h in vol_lints[:10]:
            print(f"          · {h}")
        print("          (a NUMBER, never a score. Every other heat check here is a share with"
              " a hand-picked denominator, so a game can pass every one of them nearly"
              " empty. Reads the BUILT html on the field's own word list; a rate"
              " over word count is the only figure comparable across the two bases)")

    if world_lints:
        print(f"  {'─'*72}")
        print(f"  lint · the prose names places the map does not have — {len(world_lints)} to eyeball")
        for h in world_lints[:10]:
            print(f"          · \"{h['part']}\" ×{h['count']}: {h['line']}…")
        print("          (either the location is missing, or the sentence is wrong)")

    if face_summary:
        print(f"  {'─'*72}")
        print(f"  lint · bound to a person, no face — {face_summary}")
        for h in face_lints[:10]:
            print(f"          · {h}")
        if len(face_lints) > 10:
            print(f"          · … and {len(face_lints)-10} more")
        print("          (the-first-hour.md F5b — a LIST, never a score. `trigger.npc` renders the"
              " portrait AND gates the surface on that character's own [[npcs.schedules]]."
              " `requires_npc` draws no face, but since 2026-09-03 it DOES gate the solo lane"
              " (setup._npcPresentForCanvas) as well as random ambients and substitution targets,"
              " so a row carrying it is at least hidden while that person is elsewhere — it is"
              " the FACE that is still missing. An activity that happens in a place while somebody"
              " is around is a legitimate shape. A surface ON that person wants the face, and when"
              " the face is already taken by a higher-priority canvas the surface is a NODE INSIDE"
              " that canvas, not a second one beside it — a node has no priority to lose (F5b)."
              " Walk-ins and windowed scenes are legitimate hits, which is why this cannot"
              " fail anything)")

    if tok_summary:
        print(f"  {'─'*72}")
        print(f"  lint · a token the engine never resolves — {tok_summary}")
        for h in tok_player[:10]:
            print(f"          · {h}")
        if len(tok_player) > 10:
            print(f"          · … and {len(tok_player)-10} more player-facing")
        for h in tok_dev[:3]:
            print(f"          · (dev) {h}")
        if len(tok_dev) > 3:
            print(f"          · (dev) … and {len(tok_dev)-3} more")
        print("          (engine.md §43 — a LIST, never a score. @-tokens are resolved in block"
              " content, a location's description and blocked_message, and choice text. Nowhere"
              " else. A canvas `name` becomes the link label on the room screen and the quest"
              " card's canvas_name; an npc `description` is the character-creation screen. Write"
              " the ROLE in these fields — \"his son\", \"Sit with him\" — and keep the token for"
              " prose)")
    print()
    # Parked and too-few are in `denom` and never passes, so either keeps this non-zero.
    sys.exit(0 if denom and npass == denom else 1)


if __name__ == "__main__":
    main()
