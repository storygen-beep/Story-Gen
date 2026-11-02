"""Held-out case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    old_keys = {e.get("trait") for e in effects(base)}
    raised = {e.get("trait") for e in effects(game) if (e.get("value") or 0) > 0} - old_keys
    sus = [t for t in raised if t and "susp" in t.lower()]
    if not sus:
        return ["no new suspicion meter is raised anywhere"]
    t = sus[0]
    if not any(i.get("trait_key") == t for i in condition_items(game)):
        return [f"{t} is raised but no condition ever reads it"]
    return []
