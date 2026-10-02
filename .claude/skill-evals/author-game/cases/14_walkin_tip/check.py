"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    new = [c for c in new_canvases(game, base)
           if any(e.get("trait") == "money" and (e.get("value") or 0) > 0 for e in effects(c))]
    if not new:
        return ["no new canvas that pays Emma"]
    return []
