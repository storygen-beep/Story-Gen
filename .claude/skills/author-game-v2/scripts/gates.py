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

Why a real TOML parser and not grep: an earlier grep-based pass on this same file
silently missed 24 `is_repeatable` lines (whitespace-aligned and unspaced variants)
and produced a 33%-repeatable figure when the truth is the majority. Parse, never grep.
"""

import sys
import os
import re
import json
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

        if b.get("blocks"):                          # group: variants of ONE screen -> fold in
            _collect(b["blocks"], beat, out, canvas, node)

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


def _currency_ops(obj, cur, out):
    """Collect every 'add'/'subtract' this structure performs on the currency trait.

    Walks the whole nested shape rather than the known effect sites, because a
    grant can hang off an exit_block config, a choice, or a cascade beat, and a
    gate that only looks in one of those under-reports the economy.
    NOTE the key asymmetry the rest of this file already documents: an EFFECT
    names its trait `trait`, a CONDITION names it `trait_key`.
    """
    if isinstance(obj, dict):
        if (obj.get("trait") or obj.get("trait_key")) == cur and obj.get("op") in ("add", "subtract"):
            out.append(obj["op"])
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
    R6 — frozen openers: a standing menu whose authored prose carries no conditional
         block at all, so it reads identically on day 1 and day 40.

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

    out, tot, opened, menus, frozen = [], 0, 0, 0, 0
    for c in model:
        if not c["rep"] or c["id"] not in located:
            continue
        chs = [ch for n in c["nodes"] for ch in ((n.get("exit_block") or {}).get("choices") or [])]
        if not chs:
            continue
        n_open = sum(1 for ch in chs if not ((ch.get("conditions") or {}).get("items")))
        tot += len(chs)
        opened += n_open
        if len(chs) >= 2:
            menus += 1
            if c["beats"] and not any(varies(n.get("blocks")) for n in c["nodes"]):
                frozen += 1
                out.append(dict(kind="frozen", id=c["id"], loc=c["loc"],
                                note=f"{len(chs)} choices, no conditional block — same prose every visit"))
        if n_open >= 8:
            out.append(dict(kind="open", id=c["id"], loc=c["loc"],
                            note=f"{n_open} of {len(chs)} choices open with no condition"))
    # Population labelled on purpose: the anchoring lint counts ROOM screens only, this one
    # counts every located repeatable screen. Two adjacent numbers over different populations
    # is the denominator trap, and naming it is cheaper than reconciling it.
    summary = (f"{opened}/{tot} location choices open on turn one · "
               f"{frozen}/{menus} standing menus never change their prose "
               f"(rooms AND character hubs)")
    return summary, out


def lint_choice_anchoring(model, game, state=None):
    """`the-surfaces.md` R2b, as a MEASURED PERCENTAGE rather than a verdict.

    A LINT, and the third rule in this file to end up here after being built as a gate. The
    reason is in `_room_objects`: a word-match is a proxy for a semantic rule, and run
    against the skill's own worked example it fails "Mirror" under a paragraph about a
    wardrobe. A check that fails correct work gets ignored — R5 and R6 taught that already.

    What to do with the number: compare it, do not clear it. Measured on the game that
    prompted this, 55% of room choices name something their own screen said, against a
    ceiling of ~74% for the same game measured against the whole room's prose. A screen
    contributing several floating choices is where to look — not the total.
    """
    decl = _room_objects(model, game, state)
    if decl is None or not decl["choices"]:
        return None, []
    pct = 100 * decl["anchored"] / decl["choices"]
    summary = (f"{decl['anchored']}/{decl['choices']} ({pct:.0f}%) of room choices name "
               f"something their own screen's prose put in the room")
    return summary, decl["floats"]


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
""".split())
# ⚠️ The second block was added after the under-declaration check reported choices "hanging off"
# objects called *there*, *before*, *whole*, *forty* and *friday*. Adverbs, ordinals, weekday
# names and bare numbers are never the thing a choice acts on, and they were drowning the real
# findings. Words that ARE objects in some game (a "morning" shift is not an object; a location
# genuinely named "The Weekend" would be) stay resolvable through the declared list itself.


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


_ROOM_OBJECTS_CACHE = {}


def _room_objects(model, game, state):
    """Shared analysis behind gate 22 and the choice-anchoring lint.

    Memoised on the identity of its inputs: the gate and the lint both need the full walk,
    and computing it twice is not just wasted work — it is two places that could drift if
    only one call site is ever edited.

    Returns None when no `board.locations[].objects` are declared anywhere — an absence is
    never a pass. Otherwise a dict carrying both the DECLARATION checks (which are gated,
    because they are pure consistency and reachable) and the ANCHORING count (which is a
    lint, because it is a lexical proxy for a semantic rule — see the note below).

    ⚠️ WHY ANCHORING IS A LINT AND NOT A GATE. Run against this skill's own worked example
    in `the-surfaces.md` — the one measured from a shipped game to show what CORRECT looks
    like — a strict word-match fails "Mirror" under *"Your clothes are kept in the creaky
    wardrobe."* The mirror belongs to the cluster that paragraph sets up; a human sees it and
    a word-match cannot. One in four of that example's real decisions fails. On a real game
    the ceiling is ~74% even matching against the whole room's prose. A gate demanding zero
    failures could therefore never be passed, and this project has already learned twice what
    happens to a check that fails correct work: it gets ignored. The percentage is genuinely
    useful; the pass/fail line was not.
    """
    key = (id(model), id(game), id(state))
    if key in _ROOM_OBJECTS_CACHE:
        return _ROOM_OBJECTS_CACHE[key]

    board_locs = ((state or {}).get("board") or {}).get("locations") or []
    objs = {l.get("id"): (l.get("objects") or []) for l in board_locs if l.get("objects")}
    if not objs:
        _ROOM_OBJECTS_CACHE[key] = None
        return None

    real_locs = {l.get("id") for l in (game.get("locations") or [])}
    loc_desc = {l.get("id"): (l.get("description") or "") for l in (game.get("locations") or [])}

    # A canvas bound to a person is judged by the object test (R1/R2), not by room objects.
    # BOTH keys matter: `requires_npc` and `npc` are separate fields and a hub may set only
    # one — checking `npc` alone would judge a character's hub as if it were a room.
    npc_hubs = {x["id"] for x in (game.get("canvases") or [])
                if (x.get("trigger") or {}).get("npc")
                or (x.get("trigger") or {}).get("requires_npc")}

    named = collections.defaultdict(set)
    afforded = collections.defaultdict(set)
    floats, rooms_seen = [], set()
    undeclared_hooks = collections.defaultdict(collections.Counter)
    n_choices = n_anchored = 0

    # The location's own description renders on the way in, so it is prose the room has said.
    # Seeded OUTSIDE the canvas loop on purpose: a location whose only canvases bind an NPC
    # would otherwise never have its description read, and every object there would be
    # reported "never written".
    for loc, os_ in objs.items():
        for i, o in enumerate(os_):
            if _names_any(loc_desc.get(loc, ""), set(_content_words(o))):
                named[loc].add(i)

    for c in model:
        if not c["rep"] or c["id"] in npc_hubs or not c["loc"]:
            continue
        rooms_seen.add(c["loc"])
        os_ = objs.get(c["loc"])
        if not os_:
            continue
        obj_words = {w for o in os_ for w in _content_words(o)}
        for n in c["nodes"]:
            prose = " ".join([loc_desc.get(c["loc"], "")]
                             + [b.get("content") or "" for b in (n.get("blocks") or [])
                                if isinstance(b, dict)])
            for i, o in enumerate(os_):
                if _names_any(prose, set(_content_words(o))):
                    named[c["loc"]].add(i)
            # This screen's own prose — NOT the room's whole declared list, which would
            # accept almost anything from a room declaring seventeen things.
            screen_vocab = set(_content_words(prose))
            for ch in ((n.get("exit_block") or {}).get("choices") or []):
                if (ch.get("targetType") or "node") == "location":
                    continue                                  # an exit is not a decision
                n_choices += 1
                txt = ch.get("text") or ""
                # Separate question from anchoring — record unconditionally, or one defect
                # gets reported twice (floating choice AND unusable object).
                for i, o in enumerate(os_):
                    if _names_any(txt, set(_content_words(o))):
                        afforded[c["loc"]].add(i)
                if _names_any(txt, screen_vocab):
                    n_anchored += 1
                    # ⚠️ UNDER-DECLARATION, computed from the GAME rather than the board, so
                    # it cannot be answered by shrinking the board. This choice hangs off
                    # something its screen really did name — so if no declared object covers
                    # that word, the board left a real affordance out. Without this, gate 22
                    # was passable by declaring one safe object per room and touching nothing
                    # else: measured, that scored 20/21 with the game byte-identical.
                    # Compare with the SAME fuzzy matcher the rest of the file uses. Exact
                    # membership reported "padlock" as undeclared against a declared "the
                    # padlocked door".
                    hooks = [w for w in _content_words(txt) if w in screen_vocab]
                    if hooks and not any(_names_any(w, obj_words) for w in hooks):
                        undeclared_hooks[c["loc"]][hooks[0]] += 1
                else:
                    floats.append(f"{c['id']} @{c['loc']}: \"{txt[:52]}\" names nothing "
                                  f"the room has")

    unknown = [f"board declares objects for \"{loc}\", which is not a location in the game"
               for loc in objs if loc not in real_locs]
    # Closes the room-level hole: without this, declaring objects for one easy room and
    # leaving the rest blank shrinks what the checks look at until they are trivial.
    undeclared = [f"{loc} has room screens but declares no objects — nothing to check it against"
                  for loc in sorted(rooms_seen - set(objs))]
    # Closes the object-level hole — see the note at the call site above.
    missing = [f"{loc}: choices hang off \"{w}\", which the board never declared "
               f"({n} choice{'s' if n > 1 else ''})"
               for loc, ws in sorted(undeclared_hooks.items())
               for w, n in ws.most_common()]
    unnamed, unused, roomless = [], [], []
    for loc, os_ in objs.items():
        if loc in real_locs and loc not in rooms_seen:
            # No repeatable room screen at all. Reporting every object as "affords no choice"
            # would be seven misleading lines for one fact — and the fact is the board's own:
            # "what she can do there repeatedly — if nothing, it is not a location yet."
            roomless.append(f"{loc}: declares {len(os_)} objects but has no repeatable room "
                            f"screen — nothing there can afford anything")
            continue
        for i, o in enumerate(os_):
            if i not in named.get(loc, set()):
                unnamed.append(f"{loc}: declared \"{o}\" but no prose names it")
            elif i not in afforded.get(loc, set()):
                unused.append(f"{loc}: \"{o}\" is in the prose but affords no choice")

    result = dict(objs=objs, unknown=unknown, undeclared=undeclared, roomless=roomless,
                  missing=missing, unnamed=unnamed, unused=unused, floats=floats,
                  anchored=n_anchored, choices=n_choices)
    _ROOM_OBJECTS_CACHE[key] = result
    return result


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
    locked = sum(1 for c in model for n in c["nodes"]
                 for ch in ((n.get("exit_block") or {}).get("choices") or [])
                 if ch.get("show_when_locked"))
    gate("ends on an opening", locked > 0,
         f"{locked} choices render visible-but-locked")

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
    descents = [k for k in sorted(set(p_expand) | set(p_contract))
                if p_contract[k] >= p_expand[k] and (p_expand[k] + p_contract[k])
                and k not in bad]

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
    # a lodger on nights legitimately has no night schedule row. Only a declaration
    # separates "lives elsewhere" from "was never given a room".
    chars = board.get("characters") or []
    bmap = board.get("map") or {}
    homes = bmap.get("homes") or {}
    if state is None:
        gate("residents have homes", None, "no v2_state.json — nothing declared to check against")
    elif not bmap:
        gate("residents have homes", False, "board.map not declared",
             ["the board phase must record the map: shape, dwelling, exterior, homes",
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

        # A STANDING surface — one with its own trigger.location, that the player can
        # simply click — granting currency with neither a per-day cap nor a costs block
        # is a money printer, and every other economy rule is void beside it.
        # A triggerless RUNG is held to a weaker standard on purpose: it is reached
        # through a hub choice that carries the meter gate, so it is not free, only
        # farmable. Those are reported, not failed — the sinks:sources gate above is
        # what judges whether the game has too many ways to earn.
        own_trigger = {c["id"] for c in (game.get("canvases") or [])
                       if (c.get("trigger") or {}).get("location")}
        printers, farmable = [], []
        for c in model:
            if not c["rep"] or c["perday"] or c["costs"]:
                continue
            ops = []
            _currency_ops({"nodes": c["nodes"]}, currency, ops)
            if "add" not in ops:
                continue
            (printers if c["id"] in own_trigger else farmable).append(
                f"{c['id']} @{c['loc']}: grants `{currency}`, no per-day cap, no costs block")
        gate("no free uncapped income", not printers,
             f"{len(printers)} standing surfaces print money without limit"
             + (f" · {len(farmable)} gated rungs are uncapped too" if farmable else ""),
             printers + ([f"(gated, not failed) {x}" for x in farmable[:6]] if printers else []))

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
             f"median is 3. A room's choice count should fall out of what its prose names "
             f"(the-surfaces.md R2b, gate 22), not be filled up to this number."]
            if per_screen and at_cap * 2 > len(per_screen) else []))

    # G22 — choices hang off the room. `the-surfaces.md` R2b, made checkable.
    #
    # DECLARE-THEN-CHECK, per SKILL.md:107. `board.locations[].objects` is the author's
    # own list of what each room's prose names; this compares the game against it and
    # invents no number of its own.
    #
    # Why it exists (study 6): gate 20 caps a MAGNITUDE, and a game can satisfy a cap by
    # generating choices up to it — measured, one did, at exactly 8 on 19 of 30 screens,
    # with the same 213 total choices as the game the cap was written to fail. R2b is the
    # causal half of the same rule and was the half nothing checked; it drifted to 41%.
    #
    # SCOPED TO LOCATION-ONLY HUBS. On an NPC-bound hub the anchor is the PERSON, not a
    # room object — R1/R2's object test. Measured: the handover hub scores 0% here and is
    # correct, because all eight of its choices take the character as the object of the
    # verb. Including NPC hubs would fail exactly the screens that are right.
    decl = _room_objects(model, game, state)
    if decl is None:
        gate("declared objects are real", None,
             "no board.locations[].objects declared — nothing to check against",
             ["declare what each room's prose names and she can act on, per location",
              "references/the-surfaces.md R2b"])
    else:
        bad = (decl["unknown"] + decl["undeclared"] + decl["roomless"]
               + decl["unnamed"] + decl["unused"] + decl["missing"])
        n_obj = sum(len(v) for v in decl["objs"].values())
        gate("declared objects are real", not bad,
             f"{n_obj} declared objects across {len(decl['objs'])} rooms · "
             f"{len(decl['unnamed'])} never written · {len(decl['unused'])} unusable · "
             f"{len(decl['missing'])} affordances undeclared"
             + (f" · {len(decl['undeclared'])} rooms undeclared" if decl["undeclared"] else ""),
             bad + (["references/the-surfaces.md R2b — a declared object must appear in the "
                     "room's prose AND afford at least one choice, and every thing the choices "
                     "act on must be declared",
                     "an object nobody can act on is texture: put it in the prose, not in "
                     "board.locations[].objects"]
                    if bad else []))

    # ⚠️ THE TWO SCREEN-SHAPE RULES ARE LINTS, NOT GATES — see lint_screen_shape().
    # `the-surfaces.md` R5 (ungated doors) and R6 (frozen openers) are real rules that a
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
        outflows = []

        def _outflows(o):
            if isinstance(o, dict):
                if ((o.get("trait") or o.get("trait_key")) == currency
                        and o.get("op") == "subtract"
                        and isinstance(o.get("value"), (int, float))):
                    outflows.append(o["value"])
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
        gaps = []
        if not isinstance(ob_amt, (int, float)) or ob_amt <= 0:
            gaps.append("board.economy.obligation is declared but board.economy.obligation_amount "
                        "is not — an obligation with no price cannot be checked, and one that "
                        "cannot be checked is how a game shipped with its central charge missing")
        elif biggest < ob_amt:
            gaps.append(f"the largest single `{currency}` outflow in the game is {biggest:g}, "
                        f"below the declared obligation of {ob_amt:g} — the price is written in "
                        f"the ledger and the prose but never taken from the player")
        gate("the obligation is charged", not gaps,
             f"[declared] {ob_amt if isinstance(ob_amt, (int, float)) else '?'} "
             f"{currency} · largest single outflow {biggest:g} across {len(outflows)} charges",
             gaps)

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

    return R


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
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
    anchor_summary, anchor_lints = lint_choice_anchoring(model, game, state)

    if "--json" in sys.argv:
        print(json.dumps({"gates": [dict(r) for r in results],
                          "lints": {"dialogue_attribution": lints,
                                    "world_prose": world_lints,
                                    "screen_shape": {"summary": shape_summary,
                                                     "findings": shape_lints},
                                    "choice_anchoring": {"summary": anchor_summary,
                                                         "findings": anchor_lints}}},
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

    if anchor_summary:
        print(f"  {'─'*72}")
        print(f"  lint · choices hang off the room — {anchor_summary}")
        by_screen = collections.Counter(h.split(" @")[0] for h in anchor_lints)
        for sid, n in by_screen.most_common(8):
            print(f"          · {sid}: {n} choice{'s' if n > 1 else ''} naming nothing the screen said")
        if len(by_screen) > 8:
            print(f"          · … and {len(by_screen)-8} more screens")
        if anchor_lints:
            print("          (the-surfaces.md R2b — a PERCENTAGE to compare, not a bar to clear:"
                  " a word-match cannot see that a mirror belongs to a paragraph about a wardrobe."
                  " ROOM screens only; character hubs are judged by the object test instead)")

    if shape_lints or shape_summary:
        print(f"  {'─'*72}")
        print(f"  lint · screen shape — {shape_summary}")
        for h in shape_lints[:10]:
            tag = "frozen" if h["kind"] == "frozen" else "wide open"
            print(f"          · [{tag}] {h['id']} @{h['loc']}: {h['note']}")
        if len(shape_lints) > 10:
            print(f"          · … and {len(shape_lints)-10} more")
        print("          (the-surfaces.md R5/R6 — thresholds not yet establishable; judge these,"
              " do not score them)")

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
