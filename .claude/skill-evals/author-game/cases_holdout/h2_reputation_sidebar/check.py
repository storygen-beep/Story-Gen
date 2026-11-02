"""Held-out case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    old = {s.get("trait") for s in base.get("sidebar_items", [])}
    new = [s for s in game.get("sidebar_items", []) if s.get("trait") not in old]
    if not new:
        return ["no new sidebar item"]
    trait = new[0]["trait"]
    labels = {l["key"]: l for l in game.get("traits", {}).get("labels", [])}
    fails = []
    if trait not in labels or not labels[trait].get("label"):
        fails.append(f"trait {trait} has no label in [traits]")
    if not any(e.get("trait") == trait and (e.get("value") or 0) > 0 for e in effects(game)):
        fails.append(f"nothing raises {trait}")
    return fails
