"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    kitchen_new = [c for c in new_canvases(game, base) if c["trigger"].get("location") == "kitchen"]
    old = canvases(base)
    added_choices = 0
    for c in changed_canvases(game, base):
        if c["trigger"].get("location") == "kitchen" and c["id"] in old:
            added_choices += max(0, len(choices(c)) - len(choices(old[c["id"]])))
    if len(kitchen_new) + added_choices < 4:
        return [f"only {len(kitchen_new)} new kitchen canvases and {added_choices} new choices"]
    return []
