"""Held-out case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    ticks = (game.get("engine", {}).get("daily_tick", {}) or {}).get("traitEffects", []) or []
    drains = [e for e in ticks if e.get("trait") == "money" and isinstance(e.get("value"), (int, float)) and e["value"] < 0]
    if not drains:
        return ["no daily money drain in [engine.daily_tick].traitEffects"]
    fails = []
    for e in drains:
        floor = any(i.get("trait_key") == "money" and i.get("operator") in ("gte", "gt")
                    for i in condition_items(e.get("conditions", {})))
        if not floor and not e.get("clamp"):
            fails.append(f"the ${abs(e['value'])} daily drain can push money below zero: no money condition, no clamp")
    return fails
