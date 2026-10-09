"""Tiny TOML value writer for the first_term build generators (scratchpad only)."""
import json


def q(s):
    return json.dumps(str(s), ensure_ascii=False)


def v(x):
    """Inline TOML for a python value."""
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, (int, float)):
        return repr(x)
    if isinstance(x, str):
        return q(x)
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(v(i) for i in x) + "]"
    if isinstance(x, dict):
        return "{ " + ", ".join(f"{k} = {v(val)}" for k, val in x.items()) + " }"
    raise TypeError(type(x))


def vlist(items, indent="  "):
    """A multi-line array of inline tables."""
    if not items:
        return "[]"
    return "[\n" + "".join(f"{indent}{v(i)},\n" for i in items) + "]"


def cond(*items, logic="AND"):
    return {"version": "1.0", "logic": logic, "items": list(items)}


def ccond(*items, logic="AND"):
    """A conditions block written multi-line (items one per line)."""
    return ("{ version = \"1.0\", logic = " + q(logic) + ", items = [\n"
            + "".join(f"  {v(i)},\n" for i in items) + "] }")


# condition item helpers (canvas spelling)
def flag(k, on=True):
    return {"type": "flag", "subject": "player", "flag_key": k,
            "operator": "is_true" if on else "is_false"}


def trait(k, op, val):
    return {"type": "trait", "subject": "player", "trait_key": k, "operator": op, "value": val}


def ntrait(npc, k, op, val):
    return {"type": "trait", "subject": "npc", "npc_id": npc, "trait_key": k, "operator": op, "value": val}


def tod(a, b=None):
    d = {"type": "time_of_day", "start_time": a}
    if b:
        d["end_time"] = b
    return d


def wd(*days):
    return {"type": "weekday", "weekdays": list(days)}


def boost_off():
    return {"type": "modifier", "modifier_key": "drinks_boost", "operator": "is_inactive"}


# effect helpers
def add(k, n, clamp=True):
    d = {"targetType": "player", "trait": k, "op": "add", "value": n}
    if not clamp:
        d["clamp"] = False
    return d


def setv(k, n, clamp=None):
    d = {"targetType": "player", "trait": k, "op": "set", "value": n}
    if clamp is not None:
        d["clamp"] = clamp
    return d


def nadd(npc, k, n):
    return {"targetType": "npc", "npcId": npc, "trait": k, "op": "add", "value": n}


def fset(k):
    return {"targetType": "player", "flag": k, "op": "set"}


def funset(k):
    return {"targetType": "player", "flag": k, "op": "unset"}


DAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def days(names):
    return [DAYS[d[:3]] for d in names]
