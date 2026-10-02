"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def _diane_present(c):
    t = c["trigger"]
    if "npc_diane" in (t.get("npc"), t.get("requires_npc")):
        return True
    return any(i.get("type") == "npc_at_location" and "npc_diane" in json.dumps(i)
               for i in condition_items(t))

def check(game, base):
    hits = [c for c in new_canvases(game, base)
            if c["trigger"].get("location") == "kitchen"
            and any(b.get("props", {}).get("npcId") == "npc_diane" for b in text_blocks(c))]
    if not hits:
        return ["no new kitchen canvas where Diane speaks"]
    return [f"{c['id']}: Diane speaks but nothing requires her to be in the kitchen"
            for c in hits if not _diane_present(c)]
