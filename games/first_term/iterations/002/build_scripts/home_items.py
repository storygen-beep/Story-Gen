"""Shared pieces for life at home (sheets/systems/home_life.md), iteration 002, part 2.

- brake(): once a day, cleared at midnight (LO, 2026-10-09, DECISIONS 77, replacing Q60's 12 hours).
  The item's flag is read `is_false` and set on use; every key in DAILY is unset in
  [engine.daily_tick] (0_systems_spec.toml), so the gates see the cap (the-meters.md M3-M5).
- placeholder(): a marked hole where a signed sheet line belongs that this build does not write
  (LO, 2026-10-09: the tease / touch / paid-look lines between her and Laura, Mark or Ryan). The
  block's text starts with PLACEHOLDER and names the sheet file:line; list_placeholders.py reads
  them back out of the built TOML for BUILD_LOG.md.
- item(): one home_life item inside a person's hub: a hub choice into a node; the node's exits are
  the plain finish, and by stage the tease, the touch, and "(Needs Hungry)" locked (home_life.md
  "The rule for every item").
"""
import copy
from canv import *
from tomlw import tod, wd

HOURS = 12
CURIOUS = trait("corruption", "gte", 20)
BOLD = trait("corruption", "gte", 40)
HUNGRY = trait("corruption", "gte", 60)
DARING = trait("exhibitionism", "gte", 20)
SHOWING = trait("exhibitionism", "gte", 40)


def here(npc, loc, on=True):
    return {"type": "npc_at_location", "location_id": loc, "npc_id": npc,
            "operator": "is_present" if on else "is_absent"}


def nobody(loc):
    return {"type": "npc_at_location", "location_id": loc, "operator": "is_absent"}


def since(key, op, hours=HOURS):
    return {"type": "hours_since_flag", "subject": "player", "flag_key": key, "operator": op, "value": hours}


# Every brake flag a home item sets; each one is unset in [engine.daily_tick] (0_systems_spec.toml).
DAILY = ["ate_breakfast", "had_coffee", "ate_dinner", "helped_cook", "did_dishes", "had_drink_home",
         "watched_tv", "movie_night", "did_laundry", "sunned", "studied_home", "made_up_today",
         "hung_washing", "home_event", "couch_seen", "mark_paid_look"]


def _with(c, extra):
    base = (c or {}).get("items", []) if isinstance(c, dict) else []
    return cond(*(list(base) + list(extra)))


def brake(choice, key):
    """A choice open once a day: its flag unset (cleared at midnight). A list, for splatting."""
    assert key in DAILY, key
    c = copy.deepcopy(choice)
    c["conditions"] = _with(c.get("conditions"), [flag(key, False)])
    return [c]


def brake_canvas(canvas, key):
    """A solo canvas open once a day (its flag unset). A list, for splatting."""
    assert key in DAILY, key
    c = copy.deepcopy(canvas)
    c["trigger"]["conditions"] = _with(c["trigger"].get("conditions"), [flag(key, False)])
    return [c]


def placeholder(ref, what):
    """A marked hole: the sheet line this build does not write."""
    return P(f"PLACEHOLDER — {ref} ({what}). This line is on the signed sheet and is not written in this build.")


def fx(*effects):
    return [e for e in effects if e]


def npc_add(npc, key, n):
    return {"targetType": "npc", "npcId": npc, "trait": key, "op": "add", "value": n, "cap": 100}


def item(prefix, label, when, key, back, plain_blocks, plain_eff, mins,
         tease=None, touch=None, hungry=None, done_exits=None, plain_costs=None):
    """One home_life item in a hub.

    when: condition items for the hub choice (hours, weekday, who's there).
    tease / touch: dicts {label, ref, gate (items), eff, what, brake (optional extra flag)} or None;
      their screens are placeholders (the signed line is not written in this build).
    done_exits: replaces the plain "Done." (each must set `key` itself).
    Returns (hub_choices, nodes)."""
    nid = f"hl_{prefix}"
    hub = brake(go(label, node=nid, cond_=cond(*when)), key)
    exits = done_exits if done_exits is not None else [
        go("Done.", loc=back, mins=mins, eff=plain_eff, flags=[fset(key)], costs=plain_costs)]
    exits = list(exits)
    nodes = []
    for kind, spec in (("tease", tease), ("touch", touch)):
        if not spec:
            continue
        sub = f"{nid}_{kind}"
        flags_ = [fset(key)] + ([fset(spec["brake"])] if spec.get("brake") else [])
        c = go(spec["label"], node=sub, cond_=cond(*spec["gate"]), eff=spec.get("eff"), flags=flags_)
        exits += brake(c, spec["brake"]) if spec.get("brake") else [c]
        nodes.append(node(sub, spec.get("name", kind.title()),
                          [placeholder(spec["ref"], spec.get("what", kind))],
                          [go("Done.", loc=back, mins=mins)]))
    if hungry:
        exits.append(go(hungry, node="hl_hungry", swl=True, cond_=cond(HUNGRY)))
    # One way out free of every cap and cost (gate: a spent day still has a door, the-surfaces.md R7).
    exits.append(go("Not now.", loc="home_hall"))
    for c in exits:
        if any(f.get("flag") == key for f in c.get("flagEffects", [])):
            c["conditions"] = _with(c.get("conditions"), [flag(key, False)])
    nodes.insert(0, node(nid, label.rstrip("."), list(plain_blocks), exits))
    return hub, nodes


def warm(npc, n=1):
    return npc_add(npc, "warmth", n)


def want(npc, n=1):
    return npc_add(npc, "want", n)


def energy(n):
    return {"targetType": "player", "trait": "energy", "op": "add", "value": n, "cap": 100}


CORR1 = {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}
EXH1 = {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}
PAY20 = {"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}
DRINK = [{"key": "drinks_boost", "name": "Tipsy", "duration_hours": 3,
          "trait_offsets": {"corruption": 20, "exhibitionism": 20}}]
MADE_UP = [flag("made_up"), since("made_up", "lt", 10)]
NORMAL_ON = {"type": "clothing_item", "item_id": "cafe_uniform_normal", "operator": "equipped"}
SEXY_ON = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}


def hungry_node(back):
    """The screen behind every "(Needs Hungry)" choice, as the college classes have it."""
    return node("hl_hungry", "Further", [
        P("That's further than you go in this release of First Term. It comes later, when you're Hungry."),
    ], [go("Back.", loc=back)])
