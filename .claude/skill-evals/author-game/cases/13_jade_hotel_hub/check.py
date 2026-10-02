"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    new = [c for c in new_canvases(game, base)
           if c["trigger"].get("location") == "hotel_bar"
           and "npc_jade" in (c["trigger"].get("npc"), c["trigger"].get("requires_npc"))]
    if not new:
        return ["no new hotel_bar canvas for Jade"]
    jade = npc(game, "npc_jade")
    if not any(s.get("location") == "hotel_bar" for s in jade.get("schedules", [])):
        return ["Jade has no schedule row at the hotel bar, so her hub can never fire"]
    return []
