"""Can every kept scene be reached, and can every media spot show?

author-game-lean copy. Copied from author-game-v2/scripts/reach.py (frozen at ea8f6465) on 2026-11-19, with one
fix (LO, 2026-11-19): a live screen's exit_block.config effects (flagEffects, effects, wardrobeEffects) now count,
whatever the exit type, as the engine applies them (v2.py:17951-17971, v2.py:18054). v2 walked only
exit_block.choices, so a flag set on a one-way "location" exit read as "nothing sets it" (the exam fixture
billable_hours showed 49 false reds from `opening_boot`). v2's frozen copy still has this bug; first_term has no
such exits, so its result stands.

A built game (a release slice or the full game) can keep a scene that no player can ever open: it waits on a
garment she can never wear, its only door was cut, or the room's dress code never lets her stand there dressed
the way the scene asks. Nothing errors. The scene just never fires, and its media is still asked for.

This module answers that by playing the build's rules forward, not by trusting whatever cut it:

  * every door into a scene: its own trigger, another scene's substitution, a jump into one of its screens
    ("<canvas>.<node>"), a room's door option, a phone item that opens it (`accept`), a cheat-page grant, and
    the starting canvas;
  * what this build can cause: the flags something live sets, the highest and lowest value each trait can
    reach, and the garments she can get and put on. A flag, a trait rise or a garment that only a dead place
    gives does not count, so the answer is a fixed point;
  * every outfit she can wear, tried against each room's dress code (the engine checks it before any room is
    entered, `v2.py` `Config.navigation.override`, and the first matching rule wins, `clothingCheckForLocation`).

It only calls a thing unreachable when it can prove it. Anything it cannot judge (a time of day, who is where,
money) counts as possible. Read-only: it never changes the game it is given.

    from reach import check
    result = check(game)          # {"scenes": {cid: [why]}, "spots": {name: why}, "portraits": {image: why}}
"""
import itertools
import json
import math
import re
from collections import defaultdict

ENGINE_FLAGS = re.compile(r"^(?:.+_closed|cheat_.+|game_started|debug_mode|dev_mode_enabled)$")
CLOTH = {"clothing_slot", "clothing_item", "worn_type", "worn_exposure", "worn_beauty", "worn_corruption"}
MEDIA = {"image", "video"}
RISE_OPS = {"add", "+", "set", "subtract", "sub", "-"}


def _walk(x, f):
    if isinstance(x, dict):
        f(x)
        for v in x.values():
            _walk(v, f)
    elif isinstance(x, list):
        for v in x:
            _walk(v, f)


def _cmp(op, a, b):
    try:
        return {"eq": a == b, "ne": a != b, "neq": a != b, "gt": a > b, "gte": a >= b,
                "lt": a < b, "lte": a <= b}.get(op, False)
    except TypeError:
        return False


class _World:
    """What a set of live places lets happen."""

    def __init__(self, game, live_place):
        self.g = game
        clothes = {c.get("id"): c for c in game.get("clothing") or [] if isinstance(c, dict)}
        self.clothes = clothes
        rises, falls = defaultdict(list), defaultdict(bool)
        self.flags = set()
        granted = set()

        def eff(d):
            if isinstance(d.get("flag"), str) and d.get("op", "set") in ("set", "toggle") and "operator" not in d:
                self.flags.add(d["flag"])
            if d.get("action") in ("add", "equip") and d.get("item_id"):
                granted.add(d["item_id"])
            if isinstance(d.get("trait"), str) and d.get("op") in RISE_OPS and "operator" not in d:
                key = ("npc", d.get("npcId") or d.get("npc_id") or d.get("targetId"), d["trait"]) \
                    if d.get("targetType") == "npc" else ("player", d["trait"])
                op, v = d["op"], d.get("value")
                if op == "set":
                    rises[key].append(v if isinstance(v, (int, float)) and not isinstance(v, bool)
                                      else (v.get("max", math.inf) if isinstance(v, dict) else math.inf))
                    falls[key] = True
                elif op in ("add", "+"):
                    if isinstance(v, dict) or (isinstance(v, (int, float)) and v > 0):
                        rises[key].append(d["cap"] if isinstance(d.get("cap"), (int, float)) else math.inf)
                    elif isinstance(v, (int, float)) and v < 0:
                        falls[key] = True
                else:
                    falls[key] = True
            if isinstance(d.get("trait_offsets"), dict):
                for t, o in d["trait_offsets"].items():
                    if isinstance(o, (int, float)) and o > 0:
                        rises[("player", t)].append(math.inf)
                    else:
                        falls[("player", t)] = True
            if isinstance(d.get("counter_trait"), str):     # a phone post pays its counter
                rises[("player", d["counter_trait"])].append(math.inf)

        for c in game.get("canvases") or []:
            cid = c.get("id")
            if not live_place(cid, None, None):
                continue
            _walk(c.get("trigger"), eff)
            for n in c.get("nodes") or []:
                if not live_place(cid, n.get("id"), None):
                    continue
                _walk(n.get("blocks"), eff)
                # The engine applies a screen's exit_block.config effects whatever the exit type: flagEffects and
                # effects (v2.py:17951-17971, _get_flag_effects_for_node), wardrobeEffects (v2.py:18054).
                _walk((n.get("exit_block") or {}).get("config"), eff)
                for i, ch in enumerate((n.get("exit_block") or {}).get("choices") or []):
                    if live_place(cid, n.get("id"), i):
                        _walk(ch, eff)
        for k, v in game.items():
            if k != "canvases":
                _walk(v, eff)

        rent = ((game.get("settings") or {}).get("rent") or {}).get("enabled")
        if rent:
            self.flags.add("rent_short")
        self.engine_traits = {"money", "energy", "hygiene"} | (
            {"rent_short_weeks", "rent_late_fee", "paid_full_streak"} if rent else set())
        decay = set(((game.get("player") or {}).get("trait_decay") or {}).keys())
        start = (game.get("player") or {}).get("core_traits") or {}
        self.rng = {}
        for t, s in start.items():
            if t in self.engine_traits or not isinstance(s, (int, float)):
                continue
            k = ("player", t)
            self.rng[k] = (-math.inf if falls[k] or t in decay else s, max([s] + rises[k]))
        for n in game.get("npcs") or []:
            for t, s in (n.get("core_traits") or {}).items():
                if isinstance(s, (int, float)) and not isinstance(s, bool):
                    k, anyk = ("npc", n.get("id"), t), ("npc", None, t)
                    self.rng[k] = (-math.inf if falls[k] or falls[anyk] else s, max([s] + rises[k] + rises[anyk]))
        self.canvas_ids = {c.get("id") for c in game.get("canvases") or []}
        self.npc_ids = {n.get("id") for n in game.get("npcs") or []}
        self.loc_ids = {l.get("id") for l in game.get("locations") or []}

        # garments she can wear: start owned, handed out by a live place, or sold (priced, not initial) — and
        # their own conditions (the shop's and the wardrobe's lock, v2.py equipItem / buy) can hold
        def can_hold(c):
            return c.get("conditions") is None or self.block(c["conditions"]) is not False
        self.wear = {i for i, c in clothes.items()
                     if (c.get("initial") or i in granted or (c.get("price") or 0) > 0) and can_hold(c)}
        self.types = {clothes[i].get("type") for i in self.wear}

    # ---- conditions with no outfit in hand ----
    def item(self, it, depth=0):
        """(False, why) when this item can never hold; (None, None) otherwise."""
        if not isinstance(it, dict):
            return None, None
        t, op = it.get("type"), it.get("operator") or it.get("op")
        if t == "group":
            # a nested group (v2.py:5405-5413): its items under its own logic; empty or deeper than 3 never holds
            items = [i for i in it.get("items") or [] if isinstance(i, dict)]
            if depth + 1 > 3 or not items:
                return False, "an empty group, or one nested deeper than 3"
            got = [self.item(i, depth + 1) for i in items]
            dead = [w for v, w in got if v is False]
            if str(it.get("logic") or "AND").upper() == "OR":
                return (False, " and ".join(dead)) if len(dead) == len(got) else (None, None)
            return (False, dead[0]) if dead else (None, None)
        if t in ("flag", "days_since_flag", "hours_since_flag"):
            f = it.get("flag_key") or it.get("flag")
            if f and f not in self.flags and not (ENGINE_FLAGS.match(f) and not (
                    f.endswith("_closed") and f[:-7] not in self.canvas_ids)):
                if t != "flag" or op == "is_true":
                    return False, f"flag `{f}`, which nothing in this build sets"
            return None, None
        if t == "trait":
            k, v = it.get("trait_key"), it.get("value")
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                return None, None
            key = ("npc", it.get("npc_id"), k) if it.get("subject") == "npc" else ("player", k)
            r = self.rng.get(key)
            if r is None:
                return None, None
            lo, hi = r
            can = {"gte": hi >= v, "gt": hi > v, "lte": lo <= v, "lt": lo < v, "eq": lo <= v <= hi}.get(op)
            if can is False:
                who = "her" if key[0] == "player" else key[1]
                return False, f"{who} `{k}` {op} {v:g}, and this build keeps it at {lo:g}..{hi:g}"
            return None, None
        if t == "worn_type" and op in (None, "eq"):
            if it.get("value") not in self.types:
                return False, f"wearing a `{it.get('value')}`, and nothing she can wear in this build is one"
        if t == "clothing_item" and op == "equipped" and it.get("item_id") not in self.wear:
            return False, f"`{it.get('item_id')}` on, which she can never wear in this build"
        if t == "npc_at_location" and op == "is_present":
            if it.get("npc_id") and it["npc_id"] not in self.npc_ids:
                return False, f"`{it['npc_id']}` somewhere, who is not in this build"
        return None, None

    def block(self, cond):
        if not isinstance(cond, dict) or cond.get("version") != "1.0" or not cond.get("items"):
            return None      # the engine treats a versionless or empty table as satisfied
        vs = [self.item(i)[0] for i in cond["items"]]
        if str(cond.get("logic") or "AND").upper() == "OR":
            return False if all(v is False for v in vs) else None
        return False if any(v is False for v in vs) else None

    def why(self, cond):
        return [w for v, w in (self.item(i) for i in (cond or {}).get("items") or []) if v is False]


# ---- outfits and dress codes ----
def _outfits(w):
    by_slot = defaultdict(list)
    for i in w.wear:
        by_slot[w.clothes[i].get("slot")].append(i)
    slots = sorted(s for s in by_slot if s)
    out = []
    for combo in itertools.product(*[[None] + sorted(by_slot[s]) for s in slots]):
        eq = dict(zip(slots, combo))
        if eq.get("dress") and (eq.get("top") or eq.get("bottom")):
            continue   # a dress clears top and bottom when put on
        out.append(eq)
    return out


def _exposure(w, eq):
    dress = bool(eq.get("dress"))
    up = 0 if dress or eq.get("top") else (1 if eq.get("bra") else 2)
    low = 0 if dress or eq.get("bottom") else (1 if eq.get("underwear") else 2)
    return max([up, low] + [w.clothes[i].get("exposure") or 0 for i in eq.values() if i])


def _cloth(w, it, eq):
    """True/False for a clothing item in this outfit; None when the outfit does not decide it."""
    t, op = it.get("type"), it.get("operator")
    worn = [i for i in eq.values() if i]
    if t == "clothing_slot":
        return bool(eq.get(it.get("slot"))) if op == "equipped" else (
            not eq.get(it.get("slot")) if op == "unequipped" else False)
    if t == "clothing_item":
        return {"equipped": it.get("item_id") in worn, "unequipped": it.get("item_id") not in worn}.get(op)
    if t == "worn_type":
        types = {w.clothes[i].get("type") for i in worn}
        v = it.get("value") or ""
        return False if not v else (v in types if op in (None, "eq") else v not in types if op == "neq" else False)
    if t == "worn_exposure":
        return _cmp(op or "gte", _exposure(w, eq), it.get("value") or 0)
    if t in ("worn_beauty", "worn_corruption"):
        k = "beauty" if t == "worn_beauty" else "corruption"
        return _cmp(op or "gte", max([w.clothes[i].get(k) or 0 for i in worn] or [0]), it.get("value") or 0)
    return None


def _pinned(w, it):
    """A trait item when this build pins the trait to one value, else None."""
    if it.get("type") != "trait":
        return None
    key = ("npc", it.get("npc_id"), it.get("trait_key")) if it.get("subject") == "npc" else ("player", it.get("trait_key"))
    r = w.rng.get(key)
    return _cmp(it.get("operator"), r[0], it.get("value")) if r and r[0] == r[1] else None


def _room_lets_her_in(w, loc, eq):
    """True / False / None (a rule reads something this build does not pin)."""
    for r in loc.get("clothing_rules") or []:
        items = (r.get("conditions") or {}).get("items") or []
        match = True
        for it in items:
            v = _cloth(w, it, eq) if it.get("type") in CLOTH else _pinned(w, it)
            if v is None:
                return None
            if not v:
                match = False
                break
        if match:
            need = [s for s in r.get("slots_required") or []
                    if not (s in ("top", "bottom") and eq.get("dress")) and not eq.get(s)]
            return not need
    return True


def _holds(w, cond, eq):
    if not isinstance(cond, dict) or cond.get("version") != "1.0" or not cond.get("items"):
        return True
    vs = []
    for it in cond["items"]:
        if it.get("type") == "group":
            sub = {"version": "1.0", "logic": it.get("logic") or "AND", "items": it.get("items") or []}
            vs.append(bool(it.get("items")) and _holds(w, sub, eq))
            continue
        if it.get("type") in CLOTH:
            v = _cloth(w, it, eq)
            vs.append(True if v is None else v)
        else:
            vs.append(w.item(it)[0] is not False)
    return any(vs) if str(cond.get("logic") or "AND").upper() == "OR" else all(vs)


def _has_cloth(cond):
    return isinstance(cond, dict) and any(isinstance(i, dict) and (i.get("type") in CLOTH or (
        i.get("type") == "group" and _has_cloth(i))) for i in cond.get("items") or [])


def _dress_possible(w, outfits, loc, conds):
    """Is there an outfit the room lets her stand in for which all of these can hold? False only when proven."""
    if loc is None:
        return True
    for eq in outfits:
        if _room_lets_her_in(w, loc, eq) is False:
            continue
        if all(_holds(w, c, eq) for c in conds):
            return True
    return False


# ---- doors and liveness ----
def _doors(game):
    """[(target canvas, from_place or None, conditions)] for every way into a canvas other than its own trigger."""
    out = [(((game.get("project") or {}).get("starting_canvas")), None, None)]
    for c in game.get("canvases") or []:
        cid = c.get("id")
        for s in (c.get("trigger") or {}).get("substitutions") or []:
            if isinstance(s, dict):
                out.append((s.get("target_canvas_id"), (cid, None, None), s.get("conditions")))
        for n in c.get("nodes") or []:
            for i, ch in enumerate((n.get("exit_block") or {}).get("choices") or []):
                nid = ch.get("nodeId") if isinstance(ch, dict) else None
                if isinstance(nid, str) and "." in nid:
                    out.append((nid.split(".", 1)[0], (cid, n.get("id"), i), ch.get("conditions")))
                if isinstance(ch, dict) and ch.get("targetType") == "canvas":
                    out.append((ch.get("canvasId"), (cid, n.get("id"), i), ch.get("conditions")))

    def loc_door(d):
        gt = d.get("goes_to")
        if isinstance(gt, dict) and gt.get("type") == "canvas":
            out.append((gt.get("canvas_id"), None, d.get("conditions")))
        elif isinstance(d.get("canvas"), str) and "text" in d:
            out.append((d["canvas"], None, d.get("conditions")))
    _walk(game.get("locations"), loc_door)

    def phone_door(d):
        for k in ("accept", "canvas", "canvas_id", "opens"):
            if isinstance(d.get(k), str):
                cond = (d.get("trigger") or {}).get("conditions") if isinstance(d.get("trigger"), dict) else d.get("conditions")
                out.append((d[k], None, cond))
    _walk(game.get("phone"), phone_door)
    for g in (((game.get("ui") or {}).get("cheat_page") or {}).get("grants") or []):
        if isinstance(g, dict) and g.get("canvas"):
            out.append((g["canvas"], None, None))
    return out


def check(game):
    canv = {c.get("id"): c for c in game.get("canvases") or [] if isinstance(c, dict)}
    locs = {l.get("id"): l for l in game.get("locations") or [] if isinstance(l, dict)}
    doors = _doors(game)
    live = None
    prev = None
    for _round in range(25):
        w = _World(game, live or (lambda c, n, i: True))
        outfits = _outfits(w)
        live_c, live_n, live_ch, dead = set(), set(), set(), {}

        def enterable(cid, own):
            c = canv[cid]
            t = c.get("trigger") or {}
            loc = locs.get(t.get("location"))
            if t.get("location") and loc is None:
                return [f"its place `{t.get('location')}` is not in this build"]
            for k in ("npc", "requires_npc"):
                if t.get(k) and t[k] not in w.npc_ids:
                    return [f"it needs `{t[k]}`, who is not in this build"]
            if loc and not loc.get("door") and w.block(loc.get("entry_conditions")) is False:
                return [f"its place `{loc.get('id')}` can never be entered: " + "; ".join(w.why(loc.get("entry_conditions")))]
            if w.block(t.get("conditions")) is False:
                return w.why(t.get("conditions"))
            if _has_cloth(t.get("conditions")) and not _dress_possible(w, outfits, loc, [t["conditions"]]):
                return [f"no outfit she can wear meets it that `{t.get('location')}`'s dress code lets her stand in"]
            if own and (t.get("substitution_only") or t.get("is_active") is False):
                return ["nothing opens it: no trigger of its own, and no substitution, jump, door option, phone "
                        "item, cheat grant or start in this build points at it"]
            return []

        frontier = []
        for cid in canv:
            why = enterable(cid, True)
            if why:
                dead[cid] = why
            else:
                live_c.add(cid)
                frontier.append(cid)

        def place_live(p):
            if p is None:
                return True
            c, n, i = p
            return c in live_c and (n is None or ((c, n) in live_n and (i is None or (c, n, i) in live_ch)))

        changed = True
        while changed:
            changed = False
            # screens and buttons inside the live scenes
            for cid in list(live_c):
                nodes = canv[cid].get("nodes") or []
                if not nodes:
                    continue
                byid = {n.get("id"): n for n in nodes}
                todo = [nodes[0].get("id")] + [t.split(".", 1)[1] for t, p, cnd in
                                               [(ch.get("nodeId"), (oc, on.get("id"), oi), ch.get("conditions"))
                                                for oc in live_c for on in canv[oc].get("nodes") or []
                                                for oi, ch in enumerate((on.get("exit_block") or {}).get("choices") or [])
                                                if isinstance(ch, dict) and isinstance(ch.get("nodeId"), str)
                                                and ch["nodeId"].startswith(cid + ".")]
                                               if place_live(p) and w.block(cnd) is not False]
                seen = set()
                while todo:
                    nid = todo.pop()
                    if nid in seen or nid not in byid:
                        continue
                    seen.add(nid)
                    if (cid, nid) not in live_n:
                        live_n.add((cid, nid))
                        changed = True
                    for i, ch in enumerate((byid[nid].get("exit_block") or {}).get("choices") or []):
                        if not isinstance(ch, dict) or w.block(ch.get("conditions")) is False:
                            continue
                        if (cid, nid, i) not in live_ch:
                            live_ch.add((cid, nid, i))
                            changed = True
                        if ch.get("targetType") == "node" and isinstance(ch.get("nodeId"), str) and "." not in ch["nodeId"]:
                            todo.append(ch["nodeId"])
            # other doors, from live places
            for tgt, frm, cond in doors:
                if tgt in canv and tgt not in live_c and place_live(frm) and w.block(cond) is not False:
                    why = enterable(tgt, False)
                    if why:
                        dead.setdefault(tgt, why)
                    else:
                        live_c.add(tgt)
                        dead.pop(tgt, None)
                        changed = True

        state = (frozenset(live_c), frozenset(live_n), frozenset(live_ch))
        if state == prev:
            break
        prev = state
        def make_live(lc, ln, lch):
            def is_live(c, n, i):
                return c in lc and (n is None or ((c, n) in ln and (i is None or (c, n, i) in lch)))
            return is_live
        live = make_live(live_c, live_n, live_ch)

    # media: every image/video block, live only where its scene, screen and every group around it can be
    placements = defaultdict(list)

    def media(blocks, cid, alive, why, loc, conds, judge_dress):
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            a, wy, cc = alive, why, conds
            cond = b.get("conditions")
            if a and cond is not None:
                if w.block(cond) is False:
                    a, wy = False, "; ".join(w.why(cond))
                elif judge_dress and _has_cloth(cond):
                    cc = conds + [cond]
                    if not _dress_possible(w, outfits, loc, cc):
                        a, wy = False, f"it needs an outfit `{(loc or {}).get('id')}`'s dress code never lets her stand in"
            if b.get("type") in MEDIA:
                p = b.get("props") or {}
                name = p.get("pool_dir") or p.get("file") or (",".join(p.get("files")) if p.get("files") else None)
                if name:
                    placements[name].append((a, wy or f"its scene `{cid}` can never open"))
            media(b.get("blocks"), cid, a, wy, loc, cc, judge_dress)
            media((b.get("props") or {}).get("blocks"), cid, a, wy, loc, cc, judge_dress)

    for cid, c in canv.items():
        t = c.get("trigger") or {}
        loc = locs.get(t.get("location"))
        # a scene that changes her clothes part-way: its groups are not judged against the room's dress code
        judge = '"wardrobeEffects"' not in json.dumps(c)
        base = [t["conditions"]] if _has_cloth(t.get("conditions")) else []
        for n in c.get("nodes") or []:
            alive = cid in live_c and (cid, n.get("id")) in live_n
            why = "; ".join(dead.get(cid, [])) if cid not in live_c else (
                None if alive else "no live button reaches its screen")
            media(n.get("blocks"), cid, alive, why, loc, base, judge)
    spots = {k: next(wy for _a, wy in v) for k, v in placements.items() if not any(a for a, _ in v)}

    portraits = {}
    for o in ((game.get("player_portrait") or {}).get("outfits") or []):
        wh = o.get("when") or {}
        if wh.get("wearing") and wh["wearing"] not in w.wear:
            portraits[o.get("image")] = f"it shows only while she wears `{wh['wearing']}`, which she can never wear here"
        elif wh.get("worn_type") and wh["worn_type"] not in w.types:
            portraits[o.get("image")] = f"it shows only while she wears a `{wh['worn_type']}`, and nothing she can wear here is one"
    return {"scenes": {k: dead[k] for k in sorted(dead)}, "spots": dict(sorted(spots.items())), "portraits": portraits}


# ── Loopholes (LO, 2026-11-18): a dress code is only as good as its rules. first_term's street let her out with no
# panties at Exhibitionism 0 — its own message said that needs 40 — because "Not in just the sports bra" asked for a
# top and a dress counts as one. The cut and the checks above follow the rules as written, so they kept the scene.
# These three put such a hole in front of the author instead of treating it as a way in.

_COVER = ("bra", "underwear", "top", "bottom", "dress")


def _seen(eq):
    """An outfit as a dress code sees it: what fills the five covering slots (shoes and the like don't count)."""
    return tuple((k, eq.get(k)) for k in _COVER if eq.get(k))


def narrow_ways(game, limit=3):
    """Every kept scene her clothes decide that only a few outfits can open: [(scene, place, [outfits])]. A real way
    in is usually many outfits; one or two is often a hole in a dress rule. A LIST to read, never a verdict."""
    canv = {c.get("id"): c for c in game.get("canvases") or [] if isinstance(c, dict)}
    locs = {l.get("id"): l for l in game.get("locations") or [] if isinstance(l, dict)}
    w = _World(game, lambda c, n, i: True)
    outfits = _outfits(w)
    dead = check(game)["scenes"]
    out = []
    for cid, c in canv.items():
        t = c.get("trigger") or {}
        cond = t.get("conditions")
        if cid in dead or not _has_cloth(cond):
            continue
        loc = locs.get(t.get("location"))
        ways = sorted({_seen(eq) for eq in outfits
                       if (loc is None or _room_lets_her_in(w, loc, eq) is not False) and _holds(w, cond, eq)})
        if 0 < len(ways) <= limit:
            out.append((cid, t.get("location"), [", ".join(f"{k} {v}" for k, v in o) or "nothing on" for o in ways]))
    return out


_NEEDS = re.compile(r"needs\s+(?P<trait>[A-Za-z_ ]+?)\s+(?P<n>\d+)", re.I)
# What a refusal message says she can't go out without, by the words it uses.
_CLAIMS = [(re.compile(r"\b(no|without( your| any)?) (panties|knickers|underwear)\b", re.I), "underwear"),
           (re.compile(r"\b(no|without( a| your)?) bra\b", re.I), "bra"),
           (re.compile(r"\b(topless|(no|without( a| your)?) top)\b", re.I), "top"),
           (re.compile(r"\b(bottomless|(no|without( a| your)?) (bottoms?|trousers|skirt))\b", re.I), "bottom")]


def dress_rule_holes(game):
    """A refusal that says what she can't go out without, and from what number ("No panties out of the house needs
    Exhibitionism 40"), must hold at every value of that trait under the number: no outfit without that garment gets
    out. [(place, the message, the value, the outfit let out, the message of the rule that let it out, or "no rule")].
    A rule is matched the way the engine matches it: the first whose conditions hold decides (v2.py
    clothingCheckForLocation), and a dress fills top and bottom."""
    w = _World(game, lambda c, n, i: True)
    outfits = _outfits(w)
    start = (game.get("player") or {}).get("core_traits") or {}
    labels = {str(l.get("label")).lower(): l.get("key")
              for l in (game.get("traits") or {}).get("labels") or [] if isinstance(l, dict)}
    out, seen = [], set()
    for loc in game.get("locations") or []:
        rules = loc.get("clothing_rules") or []
        for r in rules:
            msg = str(r.get("message") or "")
            m = _NEEDS.search(msg)
            claim = next((slot for rx, slot in _CLAIMS if rx.search(msg)), None)
            if not m or not claim:
                continue
            name = m.group("trait").strip().lower()
            trait, n = labels.get(name, name.replace(" ", "_")), int(m.group("n"))
            cuts = {it.get("value") for q in rules for it in ((q.get("conditions") or {}).get("items") or [])
                    if it.get("type") == "trait" and it.get("trait_key") == trait and isinstance(it.get("value"), (int, float))}
            values = sorted({0, n - 1} | {c - 1 for c in cuts if 0 < c < n} | {c for c in cuts if c < n})

            for v in values:
                def match(rule, eq):
                    for it in ((rule.get("conditions") or {}).get("items") or []):
                        if it.get("type") in CLOTH:
                            ok = _cloth(w, it, eq)
                        elif it.get("type") == "trait" and (it.get("subject") or "player") == "player":
                            ok = _cmp(it.get("operator"), v if it.get("trait_key") == trait else start.get(it.get("trait_key"), 0),
                                      it.get("value"))
                        else:
                            return None
                        if not ok:
                            return False
                    return True

                for eq in outfits:
                    if eq.get(claim) or (claim in ("top", "bottom") and eq.get("dress")):
                        continue                  # she has it on: the claim is not about this outfit
                    first = next((q for q in rules if match(q, eq)), None)
                    if any(match(q, eq) is None for q in rules[:rules.index(first) + 1 if first else len(rules)]):
                        continue                  # a rule above reads something this check can't pin: not judged
                    if first is None or not [x for x in first.get("slots_required") or []
                                             if not (x in ("top", "bottom") and eq.get("dress")) and not eq.get(x)]:
                        row = (loc.get("id"), msg, v, ", ".join(f"{k} {x}" for k, x in _seen(eq)) or "nothing on",
                               first.get("message") if first else "no rule")
                        if row not in seen:
                            seen.add(row)
                            out.append(row)
    return out


def dress_exception_rows(game):
    """A rule that lets one garment stand in for a missing top or bottom ("just the sports bra") must say no dress
    too: a dress fills top and bottom, so without it the exception also matches her in a dress with that slot
    empty. [(place, rule message)]."""
    out = []
    for loc in game.get("locations") or []:
        for r in loc.get("clothing_rules") or []:
            items = (r.get("conditions") or {}).get("items") or []
            frees = {i.get("slot") for i in items if i.get("type") == "clothing_slot" and i.get("operator") == "unequipped"}
            names_item = any(i.get("type") == "clothing_item" and i.get("operator") == "equipped" for i in items)
            if names_item and frees & {"top", "bottom"} and "dress" not in frees:
                out.append((loc.get("id"), r.get("message")))
    return out


def rows(result):
    """One line per finding, for a gate or a build log."""
    out = [f"scene `{c}` can never open: {'; '.join(w)}" for c, w in result["scenes"].items()]
    out += [f"media `{k}` can never show: {w}" for k, w in result["spots"].items()]
    out += [f"her portrait `{k}` can never show: {w}" for k, w in result["portraits"].items()]
    return out


if __name__ == "__main__":
    import sys
    import tomllib
    game = tomllib.load(open(sys.argv[1], "rb"))
    r = rows(check(game))
    print("\n".join(r) if r else "every kept scene has a way in, and every media spot can show")
    sys.exit(1 if r else 0)
