"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    new = [c for c in new_canvases(game, base)
           if "npc_ethan" in (c["trigger"].get("npc"), c["trigger"].get("requires_npc")) or "ethan" in c["id"]]
    if not new:
        return ["no new Ethan canvas"]
    if not any(len(choices(c)) >= 2 for c in new):
        return ["Ethan's step 3 offers no real choice"]
    return []
