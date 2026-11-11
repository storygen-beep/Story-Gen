#!/usr/bin/env python3
"""Cut a merged game down to one release (LO + advisor, 2026-11-11; first_term DECISIONS 230).

    python3 scripts/release_filter.py games/<slug> --release 1     # the release-1 slice
    python3 scripts/release_filter.py games/<slug>                 # authoring: everything, tags stripped

Runs after scripts/merge_toml_phases.py and before package_from_toml, and rewrites
toml_phases/7_final_game.toml IN PLACE — the same way --no-dev drops 6_dev_shortcuts.toml —
so the gates and the packager read the slice with no change of their own.

WHY A SLICE AND NOT CONDITIONS. A player can read the HTML. Content hidden behind a condition
ships in the file, and one missed condition leaks it. So release N's build holds only release
N's content, and nothing is ever deleted from the sources: every canvas stays in toml_phases and
the build scripts, and the next release's build lets it back in.

What it does, repeated until nothing changes:

  1. TAGS. `release = N` keeps an item only when N <= target; `release_until = N` only when
     N >= target. Any table can carry them: a canvas, node, choice, block, location, npc,
     schedule row, quest card, phone item, clothing item, cheat grant, timetable row. Untagged
     means release 1. The keys are always stripped, because several importer tables reject an
     unknown key (timetable rows template_import.py:7279, conditions :1836).
  2. LADDER. v2_state.json board.characters[].ladder.steps[] carry `release`; a step above the
     target drops its canvas, and the person's counter is capped at the top kept step.
  3. METERS. v2_state.json release_page.meters freezes a meter: `{"cap": N}` (it can rise to N
     at most) or `{"hold": true}` (it stays at its start value); `"npc": true` applies it to
     every NPC's trait of that name. A frozen meter loses the effects that would move it past
     the freeze, and every condition on it is judged against the frozen range: an impossible
     choice, block, card, schedule row, phone item or canvas is dropped.
  4. DANGLING. Anything pointing at a dropped canvas, place or person is dropped with it
     (navigation_order entries, door options, substitutions, cheat `play` grants, schedule and
     timetable rows, phone items, quest cards), and labels nothing reads any more.
  5. REPORT. Every drop, by kind, plus the kept flag setters whose only reader was cut — a
     button that now leads nowhere (Laura's Tuesday invite was the first one found).

No runtime wrappers, no second game, no change to v2.py.
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import math
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover — py < 3.11
    import tomli as tomllib

MAX = math.inf
TAG_KEYS = ("release", "release_until")


# ─────────────────────────────────────────────────────────────────────────────
# A TOML writer, just enough for a game file (no new package).
# ─────────────────────────────────────────────────────────────────────────────
_BARE = re.compile(r"^[A-Za-z0-9_-]+$")


def _key(k):
    return k if _BARE.match(k) else json.dumps(k, ensure_ascii=False)


def _inline(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if math.isnan(v):
            return "nan"
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(_inline(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{_key(k)} = {_inline(x)}" for k, x in v.items()) + " }" if v else "{}"
    if hasattr(v, "isoformat"):
        return v.isoformat()
    raise TypeError(f"cannot write {type(v).__name__}")


def _is_aot(v):
    return isinstance(v, list) and bool(v) and all(isinstance(x, dict) for x in v)


def dumps(doc):
    """Write a parsed TOML document back out. Scalars and inline values first, then
    sub-tables, then arrays of tables, recursively — so a header never reopens a table."""
    out = []

    def table(path, d):
        later = []
        for k, v in d.items():
            if isinstance(v, dict) or _is_aot(v):
                later.append((k, v))
            else:
                out.append(f"{_key(k)} = {_inline(v)}")
        for k, v in later:
            p = path + [k]
            dotted = ".".join(_key(x) for x in p)
            if isinstance(v, dict):
                out.append(f"\n[{dotted}]")
                table(p, v)
            else:
                for item in v:
                    out.append(f"\n[[{dotted}]]")
                    table(p, item)

    table([], doc)
    return "\n".join(out).lstrip("\n") + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Frozen ranges and condition judging
# ─────────────────────────────────────────────────────────────────────────────
class Frozen:
    """What a release lets each frozen meter be: a closed range [lo, hi] per key.

    Keys are ("player", trait) or ("npc", npc_id, trait). A meter not named here is free and
    every condition on it is left alone."""

    def __init__(self):
        self.player = {}            # trait -> (lo, hi)
        self.npc = {}               # (npc_id, trait) -> (lo, hi)
        self.npc_any = {}           # trait -> rule, for NPCs read with no declared start
        self.player_rules = {}      # trait -> rule dict
        self.npc_rules = {}         # trait -> rule dict

    def range_of(self, subject, trait, npc_id=None):
        if subject == "npc":
            if (npc_id, trait) in self.npc:
                return self.npc[(npc_id, trait)]
            rule = self.npc_rules.get(trait)
            if rule is not None:
                # An NPC with no declared start for this trait starts at 0 (setup.stateDefaults).
                return (0.0, 0.0) if rule.get("hold") else (0.0, float(rule["cap"]))
            return None
        return self.player.get(trait)


def _cmp_possible(lo, hi, op, val):
    """(can it be true, can it be false) for `x op val` with x anywhere in [lo, hi]."""
    if op == "gte":
        return hi >= val, lo < val
    if op == "gt":
        return hi > val, lo <= val
    if op == "lte":
        return lo <= val, hi > val
    if op == "lt":
        return lo < val, hi >= val
    if op == "eq":
        return lo <= val <= hi, not (lo == hi == val)
    if op in ("neq", "ne"):
        return not (lo == hi == val), lo <= val <= hi
    return True, True


def judge_item(item, frozen, gone):
    """True (always), False (never) or None (can't tell) for one condition item.

    Handles the canvas shape ({type, trait_key, operator, value, subject, npc_id}) and the
    quest-card shape ({trait, op, value, subject, npc_id}); `gone` holds the ids of people,
    places and canvases this release dropped."""
    if not isinstance(item, dict):
        return None
    t = item.get("type")
    if t == "npc_at_location" and item.get("npc_id") in gone["npcs"]:
        return item.get("operator") == "is_absent"
    # A garment she can never get this release (locked on the rail and handed out by nothing): never worn or owned.
    if t == "clothing_item" and item.get("item_id") in (gone.get("no_clothes") or ()):
        op = item.get("operator")
        return {"equipped": False, "owned": False, "unequipped": True, "not_owned": True}.get(op)
    # A flag nothing in this release can set (rule 3, release builds only): read true it never holds; a
    # days/hours-since wait on it never opens either (both fail closed on an unset flag, v2.py:5212).
    never = gone.get("never_set") or ()
    flag = (item.get("flag_key") or item.get("flag")) if t in ("flag", "days_since_flag", "hours_since_flag") else (
        item.get("flag") if t is None and isinstance(item.get("flag"), str) else None)
    if flag and flag in never:
        op = item.get("operator") or item.get("op")
        if t in ("days_since_flag", "hours_since_flag"):
            return False
        if op == "is_true":
            return False
        if op == "is_false":
            return True
        return None
    if flag:
        return None
    # canvas items carry `trait_key`; quest-card items carry `trait` (with or without a type)
    trait = (item.get("trait_key") or item.get("trait")) if t in ("trait", None) else None
    if not trait:
        return None
    op = item.get("operator") or item.get("op")
    val = item.get("value")
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        return None
    subject = item.get("subject") or "player"
    rng = frozen.range_of(subject, trait, item.get("npc_id"))
    if rng is None:
        return None
    can_t, can_f = _cmp_possible(rng[0], rng[1], op, float(val))
    if can_t and not can_f:
        return True
    if can_f and not can_t:
        return False
    return None


def judge_block(cond, frozen, gone):
    """The same three-way verdict for a whole conditions table, or a bare list of items (AND)."""
    if isinstance(cond, list):
        items, logic = cond, "AND"
    elif isinstance(cond, dict):
        items, logic = cond.get("items") or [], str(cond.get("logic") or "AND").upper()
    else:
        return None
    verdicts = [judge_item(i, frozen, gone) for i in items]
    if not verdicts:
        return None
    if logic == "OR":
        if any(v is True for v in verdicts):
            return True
        if all(v is False for v in verdicts):
            return False
        return None
    if any(v is False for v in verdicts):
        return False
    if all(v is True for v in verdicts):
        return True
    return None


# ─────────────────────────────────────────────────────────────────────────────
# The filter
# ─────────────────────────────────────────────────────────────────────────────
class Report:
    def __init__(self):
        self.dropped = collections.defaultdict(list)
        self.notes = []

    def drop(self, kind, ident):
        self.dropped[kind].append(str(ident))

    def lines(self):
        out = []
        for kind in sorted(self.dropped):
            ids = self.dropped[kind]
            out.append(f"  dropped {len(ids)} {kind}: {', '.join(sorted(set(ids))[:40])}"
                       + (" …" if len(set(ids)) > 40 else ""))
        out.extend(f"  ⚠️  {n}" for n in self.notes)
        return out


def _tag_ok(d, target):
    r = d.get("release")
    u = d.get("release_until")
    if isinstance(r, (int, float)) and not isinstance(r, bool) and r > target:
        return False
    if isinstance(u, (int, float)) and not isinstance(u, bool) and u < target:
        return False
    return True


def _label(d):
    for k in ("id", "slug", "name", "text", "content", "key", "flag"):
        if isinstance(d.get(k), str) and d[k]:
            return d[k][:60]
    return "?"


def drop_tagged(node, target, rep, kind="item"):
    """Recursively remove every list element whose tags put it outside `target`, then strip the
    tags from what is left. A tagged dict that is a plain table value (not a list element)
    cannot be dropped by position, so its tags are only stripped and the case reported."""
    if isinstance(node, dict):
        for k in list(node):
            v = node[k]
            if isinstance(v, list):
                kept = []
                for x in v:
                    if isinstance(x, dict) and not _tag_ok(x, target):
                        rep.drop(f"tagged {k}", _label(x))
                        continue
                    kept.append(x)
                node[k] = kept
            if isinstance(node[k], (dict, list)):
                drop_tagged(node[k], target, rep, k)
        for t in TAG_KEYS:
            if t in node:
                if not _tag_ok(node, target):
                    rep.notes.append(f"a tagged `{kind}` table is not in a list, so it was kept: {_label(node)}")
                del node[t]
    elif isinstance(node, list):
        for x in node:
            drop_tagged(x, target, rep, kind)


def _ladder_steps(state):
    for ch in ((state.get("board") or {}).get("characters") or []):
        lad = ch.get("ladder")
        if isinstance(lad, dict):
            yield ch.get("id"), lad


def build_frozen(game, state, target):
    """The frozen ranges for this release: release_page.meters plus one counter per ladder."""
    fz = Frozen()
    if target == MAX:
        return fz, set()
    start = ((game.get("player") or {}).get("core_traits") or {})
    rp = state.get("release_page") or {}
    for trait, rule in (rp.get("meters") or {}).items():
        if not isinstance(rule, dict):
            continue
        if rule.get("npc"):
            fz.npc_rules[trait] = rule
            for n in game.get("npcs") or []:
                s = (n.get("core_traits") or {}).get(trait)
                if isinstance(s, (int, float)):
                    s = float(s)
                    fz.npc[(n.get("id"), trait)] = (s, s) if rule.get("hold") else (min(s, rule["cap"]), float(rule["cap"]))
        else:
            fz.player_rules[trait] = rule
            s = float(start.get(trait, 0) or 0)
            fz.player[trait] = (s, s) if rule.get("hold") else (min(s, rule["cap"]), float(rule["cap"]))
    cut_canvases = set()
    for who, lad in _ladder_steps(state):
        counter = lad.get("counter")
        steps = [s for s in lad.get("steps") or [] if isinstance(s, dict)]
        kept = [s for s in steps if (s.get("release") or 1) <= target]
        cut = [s for s in steps if (s.get("release") or 1) > target]
        top = max([s.get("n", 0) for s in kept] or [0])
        if counter:
            fz.player[counter] = (float(start.get(counter, 0) or 0), float(top))
            fz.player_rules[counter] = {"cap": top, "counter": True}
        kept_ids = {s.get("canvas") for s in kept}
        # A canvas shared by two ladders (zoe_01_first_party is Zoe 1 and Jake 1) goes only
        # when neither keeps it.
        cut_canvases |= {s.get("canvas") for s in cut if s.get("canvas")} - kept_ids
    for who, lad in _ladder_steps(state):
        cut_canvases -= {s.get("canvas") for s in lad.get("steps") or []
                         if isinstance(s, dict) and (s.get("release") or 1) <= target}
    return fz, cut_canvases


def _moves_frozen(eff, fz):
    """Should this effect go? A capped meter loses every rise (an add above 0, any set), a
    held one loses every change. Counters are never stripped — a kept step must still count."""
    if not isinstance(eff, dict) or "trait" not in eff or "op" not in eff:
        return False
    trait, op, val = eff.get("trait"), eff.get("op"), eff.get("value")
    tt = eff.get("targetType")
    rule = (fz.npc_rules.get(trait) if tt == "npc"
            else fz.player_rules.get(trait) if tt in (None, "player") else None)
    if not rule or rule.get("counter"):
        return False
    if rule.get("hold"):
        return True
    if op == "set":
        return not (isinstance(val, (int, float)) and val <= rule["cap"])
    if op == "add":
        # DECISIONS 231 (reader, release 1): a fall moves a frozen meter too (Tom's want -1 on an ignored text),
        # so any non-zero add goes; only a no-op add of 0 stays.
        return not (isinstance(val, (int, float)) and not isinstance(val, bool) and val == 0)
    return False


def strip_effects(node, fz, rep, where=""):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            # every list the engine applies as effects (DECISIONS 231: the reader found want raised by a
            # trigger's pre_substitution_effects, which the filter had not read)
            if k in ("effects", "income", "pre_substitution_effects", "traitEffects") and isinstance(v, list):
                kept = [e for e in v if not _moves_frozen(e, fz)]
                if len(kept) != len(v):
                    rep.drop("meter effects", f"{where}.{k}" if where else k)
                node[k] = kept
            elif k == "modifier_effects" and isinstance(v, list):
                # a timed boost to a frozen meter (DECISIONS 231: "Tipsy", Corruption and Exhibitionism +20 for 3h)
                kept = []
                for m in v:
                    if isinstance(m, dict) and isinstance(m.get("trait_offsets"), dict):
                        offs = {t: o for t, o in m["trait_offsets"].items() if not (fz.player_rules.get(t) and not fz.player_rules[t].get("counter"))}
                        if offs != m["trait_offsets"]:
                            rep.drop("meter effects", f"{where}.{k}" if where else k)
                        if not offs:
                            continue
                        m = dict(m, trait_offsets=offs)
                    kept.append(m)
                node[k] = kept
            elif isinstance(v, (dict, list)):
                strip_effects(v, fz, rep, node.get("id", where) if isinstance(node.get("id"), str) else where)
    elif isinstance(node, list):
        for x in node:
            strip_effects(x, fz, rep, where)


def strip_true_items(cond, fz, gone):
    """In an AND block, an item that always holds this release says nothing: drop it, so a read of a flag or
    meter this release can't move (zoe_met is_false) is not left in the file. An empty AND holds, as before."""
    if not gone.get("release_mode") or not isinstance(cond, dict):
        return cond
    if str(cond.get("logic") or "AND").upper() != "AND" or not isinstance(cond.get("items"), list):
        return cond
    kept = [i for i in cond["items"] if judge_item(i, fz, gone) is not True]
    # Never empty a block's items. In a group chain an empty group renders as the <<else>> (v2.py:18320,
    # _render_group_chain), so a band that always holds at the frozen values would drop to the END of the chain
    # and the top band would show instead (DECISIONS 231: the reader found Corruption-60 thoughts at 0). One
    # always-true item keeps it a condition, in its place in the chain.
    if not kept and cond["items"]:
        # keep the item least tied to cut content: a read of a flag nothing sets would look like a dead reader
        never = gone.get("never_set") or ()
        rank = lambda i: 1 if (i.get("flag_key") or i.get("flag")) in never else 0
        kept = [sorted(cond["items"], key=rank)[0]]
    if len(kept) != len(cond["items"]):
        cond = dict(cond, items=kept)
    return cond


def prune_blocks(blocks, fz, gone, rep, cid):
    """Blocks whose own conditions can never hold go; pools and groups left empty go too."""
    out = []
    for b in blocks or []:
        if not isinstance(b, dict):
            out.append(b)
            continue
        if b.get("conditions") is not None and judge_block(b["conditions"], fz, gone) is False:
            rep.drop("lines/blocks", cid)
            continue
        # a line spoken by someone this release does not ship (DECISIONS 231: the cocky guy in Figure drawing)
        if (b.get("props") or {}).get("npcId") in gone["npcs"]:
            rep.drop("lines by a cut person", cid)
            continue
        # canv.G's stand-alone group (a one-item block_pool around one group) that always holds this release is
        # not a choice: its blocks stand on their own in the node (DECISIONS 231). Unwrapped here, at the pool, so
        # its lines don't end up in a pool that would pick one of them. A group in a chain keeps a condition.
        inner = b.get("blocks") if b.get("type") == "block_pool" and not b.get("props") else None
        if (gone.get("release_mode") and isinstance(inner, list) and len(inner) == 1 and isinstance(inner[0], dict)
                and inner[0].get("type") == "group" and isinstance(inner[0].get("conditions"), dict)
                and judge_block(inner[0]["conditions"], fz, gone) is True):
            out.extend(prune_blocks(inner[0].get("blocks"), fz, gone, rep, cid))
            continue
        if b.get("type") == "group" and isinstance(b.get("conditions"), dict):
            b["conditions"] = strip_true_items(b["conditions"], fz, gone)
        if isinstance(b.get("blocks"), list):
            b["blocks"] = prune_blocks(b["blocks"], fz, gone, rep, cid)
            if not b["blocks"] and b.get("type") in ("group", "block_pool"):
                continue
        out.append(b)
    return out


def _cond_false(d, key, fz, gone):
    c = d.get(key)
    return c is not None and judge_block(c, fz, gone) is False


# The flags the engine sets itself, never through a flagEffect (the same list gates.py's `every kept thing can
# happen` allows): a final step's `<canvas>_closed` (v2.py:17222), a cheat row's `cheat_<id>` (v2.py:13741),
# the three seeded true at a new game (v2.py:1157-1163), and the rent's `rent_short` (v2.py:15992).
ENGINE_FLAGS = re.compile(r"^(?:.+_closed|cheat_.+|game_started|debug_mode|dev_mode_enabled)$")


def never_set_flags(game):
    """Every flag some reader asks for that no flagEffect in this build sets and the engine does not set.
    A `<canvas>_closed` flag is the engine's only while that canvas is in the build."""
    sets = set(flag_sets(game))
    if ((game.get("settings") or {}).get("rent") or {}).get("enabled"):
        sets.add("rent_short")
    canv = {c.get("id") for c in game.get("canvases") or []}
    out = set()
    for f in flag_reads(game):
        if f in sets:
            continue
        if f.endswith("_closed"):
            if f[:-len("_closed")] not in canv:
                out.add(f)
            continue
        if not ENGINE_FLAGS.match(f):
            out.add(f)
    return out


def unobtainable_clothing(game, fz, gone, unpriced_too=False):
    """Garments this release can't give her: not worn at the start, no wardrobe action hands them out, and their
    own conditions (the rail's lock) can never hold. Their equipped/owned checks are then always false."""
    granted = set()

    def walk(n):
        if isinstance(n, dict):
            if n.get("action") in ("add", "equip") and n.get("item_id"):
                granted.add(n["item_id"])
            for k, v in n.items():
                if k != "clothing":
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(game)
    out = set()
    for c in game.get("clothing") or []:
        if not isinstance(c, dict) or c.get("initial") or c.get("id") in granted:
            continue
        if c.get("conditions") is not None and judge_block(c["conditions"], fz, gone) is False:
            out.add(c.get("id"))
        elif unpriced_too and not c.get("price"):
            out.add(c.get("id"))      # not worn at the start, not sold, handed out by nothing kept
    return out


def one_pass(game, fz, gone, rep):
    """One sweep of rules 3 and 4. Returns True when anything changed."""
    changed = False
    if gone.get("release_mode"):
        gone["never_set"] = never_set_flags(game)
        gone["no_clothes"] = unobtainable_clothing(game, fz, gone)
    loc_ids = {l.get("id") for l in game.get("locations") or []}
    npc_ids = {n.get("id") for n in game.get("npcs") or []}

    # places: a sub-place whose parent went, goes too
    locs = []
    for l in game.get("locations") or []:
        if l.get("entry_from") and l["entry_from"] not in loc_ids:
            rep.drop("places", l.get("id"))
            gone["locations"].add(l.get("id"))
            changed = True
            continue
        locs.append(l)
    if len(locs) != len(game.get("locations") or []):
        game["locations"] = locs
    loc_ids = {l.get("id") for l in game.get("locations") or []}
    for l in game.get("locations") or []:
        no = l.get("navigation_order")
        if isinstance(no, list):
            kept = [x for x in no if x in loc_ids]
            if kept != no:
                l["navigation_order"] = kept
                changed = True
        dv = l.get("description_variants")
        if isinstance(dv, list):
            kept = [v for v in dv if not (isinstance(v, dict) and _cond_false(v, "conditions", fz, gone))]
            if len(kept) != len(dv):
                l["description_variants"] = kept
                changed = True

    # canvases
    canv_ids = {c.get("id") for c in game.get("canvases") or []}
    kept_c = []
    for c in game.get("canvases") or []:
        t = c.get("trigger") or {}
        cid = c.get("id")
        why = None
        if cid in gone["ladder"]:
            why = "ladder steps (a later release)"
        elif t.get("location") and t["location"] not in loc_ids:
            why = "canvases at a cut place"
        elif any(t.get(k) and t[k] not in npc_ids for k in ("npc", "requires_npc")):
            why = "canvases of a cut person"
        elif _cond_false(t, "conditions", fz, gone):
            why = "canvases that can't fire this release"
        if why:
            rep.drop(why, cid)
            gone["canvases"].add(cid)
            changed = True
            continue
        kept_c.append(c)
    game["canvases"] = kept_c
    canv_ids = {c.get("id") for c in kept_c}

    for c in kept_c:
        cid = c.get("id")
        t = c.get("trigger") or {}
        subs = t.get("substitutions")
        if isinstance(subs, list):
            kept = [s for s in subs if isinstance(s, dict) and s.get("target_canvas_id") in canv_ids
                    and not _cond_false(s, "conditions", fz, gone)]
            if len(kept) != len(subs):
                t["substitutions"] = kept
                changed = True
        for n in c.get("nodes") or []:
            before = json.dumps(n.get("blocks"), sort_keys=True)
            n["blocks"] = prune_blocks(n.get("blocks"), fz, gone, rep, cid)
            if json.dumps(n["blocks"], sort_keys=True) != before:
                changed = True
            eb = n.get("exit_block") or {}
            ch = eb.get("choices")
            if isinstance(ch, list):
                kept = []
                for x in ch:
                    if isinstance(x, dict):
                        if _cond_false(x, "conditions", fz, gone):
                            rep.drop("buttons", f"{cid}: {str(x.get('text'))[:40]}")
                            continue
                        if isinstance(x.get("conditions"), dict) and x["conditions"].get("items"):
                            stripped = strip_true_items(x["conditions"], fz, gone)
                            if stripped is not x["conditions"]:
                                if stripped.get("items"):
                                    x["conditions"] = stripped
                                else:
                                    del x["conditions"]
                                changed = True
                        if x.get("targetType") == "location" and x.get("locationId") and x["locationId"] not in loc_ids:
                            rep.drop("buttons to a cut place", f"{cid}: {str(x.get('text'))[:40]}")
                            continue
                        if x.get("targetType") == "canvas" and x.get("canvasId") and x["canvasId"] not in canv_ids:
                            rep.drop("buttons to a cut canvas", f"{cid}: {str(x.get('text'))[:40]}")
                            continue
                    kept.append(x)
                if len(kept) != len(ch):
                    eb["choices"] = kept
                    changed = True

    # screens no kept button reaches any more (a level-3 shift screen whose button went) go too: their text would
    # still be in the file. A canvas opens on its first node; another canvas can open one as "<canvas>.<node>".
    outside = collections.defaultdict(set)
    for c in kept_c:
        for n in c.get("nodes") or []:
            for x in ((n.get("exit_block") or {}).get("choices") or []):
                nid = x.get("nodeId") if isinstance(x, dict) else None
                if isinstance(nid, str) and "." in nid:
                    a, b = nid.split(".", 1)
                    outside[a].add(b)
    for c in kept_c:
        nodes = c.get("nodes") or []
        if not nodes:
            continue
        by_id = {n.get("id"): n for n in nodes}
        seen, todo = set(), [nodes[0].get("id")] + sorted(outside.get(c.get("id"), ()))
        while todo:
            nid = todo.pop()
            if nid in seen or nid not in by_id:
                continue
            seen.add(nid)
            for x in ((by_id[nid].get("exit_block") or {}).get("choices") or []):
                if isinstance(x, dict) and x.get("targetType") == "node" and isinstance(x.get("nodeId"), str):
                    todo.append(x["nodeId"])
        if len(seen) < len(nodes):
            for n in nodes:
                if n.get("id") not in seen:
                    rep.drop("screens no button reaches", f"{c.get('id')}.{n.get('id')}")
            c["nodes"] = [n for n in nodes if n.get("id") in seen]
            changed = True

    # door options, schedule rows, timetable, people's schedules
    for l in game.get("locations") or []:
        door = l.get("door")
        if isinstance(door, dict) and isinstance(door.get("description_variants"), list):
            dv = door["description_variants"]
            kept = [v for v in dv if not (isinstance(v, dict) and _cond_false(v, "conditions", fz, gone))]
            if len(kept) != len(dv):
                door["description_variants"] = kept
                changed = True
        if isinstance(door, dict) and isinstance(door.get("options"), list):
            kept = []
            for o in door["options"]:
                gt = (o.get("goes_to") or {}) if isinstance(o, dict) else {}
                cid = (o.get("canvas") if isinstance(o, dict) else None) or gt.get("canvas_id")
                if cid and cid not in canv_ids:
                    rep.drop("door options", f"{l.get('id')}: {cid}")
                    continue
                if isinstance(o, dict) and _cond_false(o, "conditions", fz, gone):
                    rep.drop("door options", f"{l.get('id')}: {o.get('text')}")
                    continue
                kept.append(o)
            if len(kept) != len(door["options"]):
                door["options"] = kept
                changed = True
    for n in game.get("npcs") or []:
        sch = n.get("schedules")
        if isinstance(sch, list):
            kept = [s for s in sch if isinstance(s, dict) and (not s.get("location") or s["location"] in loc_ids)
                    and not _cond_false(s, "when", fz, gone)]
            if len(kept) != len(sch):
                rep.drop("schedule rows", n.get("id"))
                n["schedules"] = kept
                changed = True
    st = game.get("settings") or {}
    wl = st.get("wardrobe_location")
    if isinstance(wl, list):
        kept = [x for x in wl if x in loc_ids]
        if kept != wl:
            st["wardrobe_location"] = kept
            changed = True
    elif isinstance(wl, str) and wl not in loc_ids:
        del st["wardrobe_location"]
        changed = True
    ui = game.get("ui") or {}
    tt = ui.get("timetable")
    if isinstance(tt, list):
        kept = [r for r in tt if not (isinstance(r, dict) and r.get("place") and r["place"] not in loc_ids)]
        if len(kept) != len(tt):
            ui["timetable"] = kept
            changed = True
    cp = ui.get("cheat_page") or {}
    if isinstance(cp.get("grants"), list):
        kept = [g for g in cp["grants"] if not (isinstance(g, dict) and g.get("kind") == "play"
                                                 and g.get("canvas") not in canv_ids)]
        if len(kept) != len(cp["grants"]):
            for g in cp["grants"]:
                if g not in kept:
                    rep.drop("cheat grants", g.get("id"))
            cp["grants"] = kept
            changed = True

    # quest cards: a card whose routing or a goal can never be met goes; so does one about a cut person
    cards = []
    for q in game.get("quest_cards") or []:
        if q.get("npc_id") and q["npc_id"] not in npc_ids:
            rep.drop("quest cards", f"{q['npc_id']}: {str(q.get('text'))[:40]}")
            changed = True
            continue
        if judge_block(q.get("when") or [], fz, gone) is False or any(
                judge_item(g, fz, gone) is False for g in q.get("goals") or []):
            rep.drop("quest cards", f"{q.get('npc_id') or q.get('group')}: {str(q.get('text'))[:40]}")
            changed = True
            continue
        if q.get("ready_canvas") and q["ready_canvas"] not in canv_ids:
            del q["ready_canvas"]
            changed = True
        cards.append(q)
    if "quest_cards" in game:
        game["quest_cards"] = cards

    # phone
    ph = game.get("phone") or {}
    for key, who in (("conversations", "npc"), ("posts", "npc"), ("calls", "caller"), ("profiles", "npc")):
        items = ph.get(key)
        if not isinstance(items, list):
            continue
        kept = []
        for it in items:
            if isinstance(it, dict):
                trig = it.get("trigger") or {}
                if it.get(who) and it[who] not in npc_ids:
                    rep.drop(f"phone {key}", it.get("id"))
                    continue
                if _cond_false(trig, "conditions", fz, gone) or _cond_false(it, "conditions", fz, gone):
                    rep.drop(f"phone {key}", it.get("id"))
                    continue
            kept.append(it)
        if len(kept) != len(items):
            ph[key] = kept
            changed = True
    return changed


def trim_bands(game, fz):
    """Sidebar and cast-page bands a frozen meter can never reach go, so their names
    (Bold, Hungry, Wants you) are not in the file."""
    for item in game.get("sidebar_items") or []:
        rng = fz.player.get(item.get("trait")) if isinstance(item, dict) else None
        if rng and isinstance(item.get("bands"), list):
            item["bands"] = [b for b in item["bands"] if not (isinstance(b, dict) and b.get("min", 0) > rng[1])]
    cast = ((game.get("ui") or {}).get("cast_page") or {})
    bands = cast.get("trait_bands")
    if isinstance(bands, dict):
        for trait, rows in bands.items():
            rule = fz.npc_rules.get(trait)
            if not rule or not isinstance(rows, list):
                continue
            ranges = [r for (_, t), r in fz.npc.items() if t == trait] or [(0.0, 0.0)]
            bottom, top = min(r[0] for r in ranges), max(r[1] for r in ranges)
            bands[trait] = [b for b in rows if not (isinstance(b, dict) and (
                b.get("min", -math.inf) > top or b.get("max", math.inf) < bottom))]


def prune_labels(game, rep):
    """A trait label or a starting trait nothing else in the file names any more goes."""
    def names(node, out, skip):
        if isinstance(node, dict):
            for k, v in node.items():
                if id(v) in skip:
                    continue
                out.add(k)
                names(v, out, skip)
        elif isinstance(node, list):
            for x in node:
                names(x, out, skip)
        elif isinstance(node, str):
            out.add(node)

    tr = (game.get("traits") or {})
    labels = tr.get("labels")
    player = game.get("player") or {}
    core = player.get("core_traits") or {}
    fkeys = player.get("flag_keys")
    skip = {id(labels), id(core), id(fkeys)}
    used = set()
    names(game, used, skip)
    keep = {"money", "energy", "hygiene", "corruption", "exhibitionism"}
    if isinstance(labels, list):
        kept = [l for l in labels if not isinstance(l, dict) or l.get("key") in used or l.get("key") in keep]
        for l in labels:
            if l not in kept:
                rep.drop("trait labels", l.get("key"))
        tr["labels"] = kept
    # her starting traits and the declared flag list name every counter and flag in the full game
    # (zoe_step, exam_art_done): only the ones the slice still uses stay
    for k in [k for k in core if k not in used and k not in keep]:
        rep.drop("starting traits", k)
        del core[k]
    if isinstance(fkeys, list):
        kept = [f for f in fkeys if f in used]
        rep.dropped["declared flags"].extend(f for f in fkeys if f not in used)
        player["flag_keys"] = kept


def trait_reads(game):
    """Every trait a condition, a quest goal or a page reads."""
    out = set()

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "trait" and n.get("trait_key"):
                out.add(n["trait_key"])
            if isinstance(n.get("trait"), str) and ("op" in n and str(n.get("op")) in
                                                    ("gte", "gt", "lt", "lte", "eq", "neq")):
                out.add(n["trait"])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(game)
    for item in game.get("sidebar_items") or []:
        if isinstance(item, dict) and item.get("trait"):
            out.add(item["trait"])
    return out


def prune_unread_upkeep(game, rep):
    """The daily tick resets and nudges every flag and counter in the full game (sauna_today, zoe_patience).
    Upkeep on something nothing in the slice reads goes, so its name is not in the file."""
    tick = ((game.get("engine") or {}).get("daily_tick") or {})
    fr, tr = flag_reads(game), trait_reads(game)
    for key, reads, field in (("flagEffects", fr, "flag"), ("traitEffects", tr, "trait"), ("effects", tr, "trait")):
        lst = tick.get(key)
        if isinstance(lst, list):
            kept = [e for e in lst if not (isinstance(e, dict) and e.get(field) and e[field] not in reads
                                           and e[field] not in ("money", "energy", "hygiene"))]
            if len(kept) != len(lst):
                rep.drop("daily upkeep", f"{len(lst) - len(kept)} {key}")
                tick[key] = kept


def flag_reads(game):
    out = set()

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") in ("flag", "days_since_flag", "hours_since_flag") and n.get("flag_key"):
                out.add(n["flag_key"])
            # a quest-card flag item ({flag, op: is_true}); a flag EFFECT ({flag, op: set}) is not a read
            if (isinstance(n.get("flag"), str) and str(n.get("op") or "").startswith("is_")
                    and "targetType" not in n):
                out.add(n["flag"])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(game)
    return out


def flag_sets(game):
    out = collections.defaultdict(set)

    def walk(n, cid):
        if isinstance(n, dict):
            if isinstance(n.get("id"), str) and "nodes" in n:
                cid = n["id"]
            for fe in n.get("flagEffects") or []:
                if isinstance(fe, dict) and fe.get("flag") and fe.get("op", "set") == "set":
                    out[fe["flag"]].add(cid)
            for v in n.values():
                walk(v, cid)
        elif isinstance(n, list):
            for v in n:
                walk(v, cid)
    walk(game, "?")
    return out


def filter_game(game, state, target, rep):
    # `[release_overrides.N]` swaps a value for release N only ("project.description" = "..."), for a table that
    # is not a list and so cannot carry its own copy; the table never ships. A list item is named by its id in
    # brackets: "locations[home_ryan_room].description".
    ov = game.pop("release_overrides", None) or {}
    for path, val in ((ov.get(str(int(target))) or {}) if target != MAX else {}).items():
        node, keys = game, path.split(".")
        for k in keys[:-1]:
            if k.endswith("]") and "[" in k:
                name, item = k[:-1].split("[", 1)
                node = next(x for x in node[name] if isinstance(x, dict) and x.get("id") == item)
            else:
                node = node.setdefault(k, {})
        node[keys[-1]] = val
        rep.drop("release overrides applied", path)
    full_reads = flag_reads(game)
    # taken BEFORE the tags drop anything, so a person or place cut by tag counts as gone
    loc_before = {l.get("id") for l in game.get("locations") or []}
    npc_before = {n.get("id") for n in game.get("npcs") or []}
    drop_tagged(game, target, rep)
    fz, ladder_cut = build_frozen(game, state, target)
    gone = {"npcs": set(), "locations": set(), "canvases": set(), "ladder": ladder_cut,
            "release_mode": target != MAX, "never_set": set()}
    strip_effects(game, fz, rep)
    for _ in range(40):
        gone["npcs"] = npc_before - {n.get("id") for n in game.get("npcs") or []}
        if not one_pass(game, fz, gone, rep):
            break
    gone["locations"] |= loc_before - {l.get("id") for l in game.get("locations") or []}
    trim_bands(game, fz)
    if gone["release_mode"]:
        gone["never_set"] = never_set_flags(game)
        nope = unobtainable_clothing(game, fz, gone, unpriced_too=True)
        cl = game.get("clothing") or []
        kept = [c for c in cl if not (isinstance(c, dict) and c.get("id") in nope and not c.get("price"))]
        for c in cl:
            if c not in kept:
                rep.drop("clothes she can't get this release", c.get("id"))
        if "clothing" in game:
            game["clothing"] = kept
        ids = {c.get("id") for c in kept if isinstance(c, dict)}

        def prune_wardrobe(n):
            # "take every garment off" lists name each one; a garment that is gone goes from them too
            if isinstance(n, dict):
                for k, v in n.items():
                    if k in ("wardrobeEffects", "wardrobe") and isinstance(v, list):
                        n[k] = [w for w in v if not (isinstance(w, dict) and w.get("item_id")
                                                     and w["item_id"] not in ids)]
                    else:
                        prune_wardrobe(v)
            elif isinstance(n, list):
                for v in n:
                    prune_wardrobe(v)
        prune_wardrobe(game.get("canvases") or [])
        prune_wardrobe(game.get("phone") or {})
    if gone["release_mode"]:
        prune_unread_upkeep(game, rep)
        types = {c.get("type") for c in game.get("clothing") or [] if isinstance(c, dict)}
        pp = game.get("player_portrait") or {}
        outs = pp.get("outfits")
        if isinstance(outs, list):
            pp["outfits"] = [o for o in outs if not (isinstance(o, dict) and isinstance(o.get("when"), dict)
                                                     and o["when"].get("worn_type")
                                                     and o["when"]["worn_type"] not in types)]
    prune_labels(game, rep)
    # kept setters whose only reader was cut
    slice_reads = flag_reads(game)
    orphans = {f: ids for f, ids in flag_sets(game).items() if f in full_reads and f not in slice_reads}
    for f, ids in sorted(orphans.items()):
        rep.notes.append(f"flag `{f}` is still set ({', '.join(sorted(ids))[:80]}) but its only readers were cut")
    for c in game.get("canvases") or []:
        for n in c.get("nodes") or []:
            eb = n.get("exit_block") or {}
            if eb.get("type") == "choices" and not eb.get("choices"):
                rep.notes.append(f"dead end: {c.get('id')} node {n.get('id')} has no button left")
    return game


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("game_dir", type=Path)
    ap.add_argument("--release", default="max", help="the release to cut to (an integer), or max")
    args = ap.parse_args(argv)
    target = MAX if str(args.release) == "max" else int(args.release)
    toml_path = args.game_dir / "toml_phases" / "7_final_game.toml"
    raw = toml_path.read_text()
    game = tomllib.loads(raw)
    state_path = args.game_dir / "v2_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    before = {"canvases": len(game.get("canvases") or []), "places": len(game.get("locations") or []),
              "people": len(game.get("npcs") or []), "cards": len(game.get("quest_cards") or [])}
    pristine = copy.deepcopy(game)
    rep = Report()
    filter_game(game, state, target, rep)
    if game == pristine:
        print(f"release filter ({args.release}): nothing tagged or frozen — {toml_path.name} left as merged")
        return 0
    toml_path.write_text(
        f"# 7_final_game.toml — merged, then cut by scripts/release_filter.py --release {args.release}\n"
        "# DO NOT EDIT THIS FILE BY HAND. Edit the phases and the build scripts, then rebuild.\n\n"
        + dumps(game))
    after = {"canvases": len(game.get("canvases") or []), "places": len(game.get("locations") or []),
             "people": len(game.get("npcs") or []), "cards": len(game.get("quest_cards") or [])}
    print(f"release filter ({args.release}): " + ", ".join(f"{k} {before[k]}→{after[k]}" for k in before))
    for line in rep.lines():
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
