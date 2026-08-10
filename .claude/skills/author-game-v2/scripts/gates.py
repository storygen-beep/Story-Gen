#!/usr/bin/env python3
"""
gates.py — the author-game-v2 scoreboard.

Measures a built game against the ten ship gates. Every threshold in here was
derived from primary measurement of Degrees of Lewdity's own source across ten
snapshots spanning 2018-11 to 2026-07 (25 -> 61 locations, 1.7k -> 15.6k units,
254k -> 2.24M words). Nothing here is inherited opinion; see THRESHOLDS below for
the evidence behind each number.

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
ANCHOR_SHARE_PCT      = 25.0    # DoL seed: school = 35,218 / 116,540 = 30.2%
MEDIAN_LOCATION_WORDS = 3_000   # DoL seed median 3,154
MEAN_LOCATION_WORDS   = 4_500   # DoL seed mean 4,661

EXPLICIT_BEAT_FLOOR = 7.5
# Share of beats carrying 3+ explicit words. DoL held 7.5%-9.3% across eight
# years and 12x growth. Unlike raw sex-word share (which fell 3.00% -> 0.96% as
# systems and UI outgrew prose), this ratio is stable, so it is the usable floor.
# It is also robust to word-list choice: two different lists both put DoL at
# 8-10% and Vesper at ~2%.

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
                          nodes=c.get("nodes") or []))
    return model, game


# ─────────────────────────────────────────────────────────────────────────────
# Gates
# ─────────────────────────────────────────────────────────────────────────────
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

    fails = []
    if anchor_pct < ANCHOR_SHARE_PCT:
        fails.append(f"no anchor: deepest location {anchor_id} holds {anchor_pct:.1f}% "
                     f"of location prose (need {ANCHOR_SHARE_PCT:.0f}%) — the world has no centre")
    if median < MEDIAN_LOCATION_WORDS:
        fails.append(f"median location {median:,} words (need {MEDIAN_LOCATION_WORDS:,})")
    if mean < MEAN_LOCATION_WORDS:
        fails.append(f"mean location {mean:,.0f} words (need {MEAN_LOCATION_WORDS:,})")
    if empty:
        fails.append(f"{len(empty)} declared locations with nothing placed: {', '.join(empty[:12])}")
    gate("location fill", not fails,
         f"{n} locations · {total:,} words · mean {mean:,.0f} · median {median:,} · "
         f"anchor {anchor_id} {anchor_pct:.0f}%",
         fails)

    # G2 — explicit floor
    pct = 100 * len(expl) / max(len(all_beats), 1)
    gate("explicit floor", None if not all_beats else pct >= EXPLICIT_BEAT_FLOOR,
         f"{pct:.1f}% of {len(all_beats):,} beats carry 3+ explicit words (floor {EXPLICIT_BEAT_FLOOR}%)")

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
    gate("ascent tiers expand the world",
         None if not (expand or contract) else (bool(tiers) and not bad),
         f"[{source}] " + ", ".join(f"{k} ({expand[k]}+/{contract[k]}-)" for k in tiers)
         if tiers else "no gated meter found",
         [f"{k} closes more than it opens ({expand[k]} expanding / {contract[k]} contracting)"
          for k in bad] +
         [f"also ranked: {k} ({expand[k]}+/{contract[k]}-)" for k in ranked if k not in tiers])

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

    if "--json" in sys.argv:
        print(json.dumps([{k: v for k, v in r.items()} for r in results], indent=1, default=str))
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
    print(f"  {npass}/{judged} judged gates pass{na_note}\n")
    sys.exit(0 if judged and npass == judged else 1)


if __name__ == "__main__":
    main()
