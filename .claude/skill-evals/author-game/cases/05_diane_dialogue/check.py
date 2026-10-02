"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


KNOWN = {"paragraph", "dialog", "group", "block_pool", "thought_bubble", "image", "video", "choices"}

def _diane_lines(c):
    return sum(1 for b in iter_dicts(c) if b.get("type") == "dialog" and b.get("props", {}).get("npcId") == "npc_diane")

def check(game, base):
    c, b = canvases(game).get("hub_diane_home"), canvases(base)["hub_diane_home"]
    if not c:
        return ["hub_diane_home is gone"]
    fails = []
    if _diane_lines(c) - _diane_lines(b) < 2:
        fails.append("fewer than 2 new dialog blocks attributed to npc_diane")
    bad = {d.get("type") for d in iter_dicts(c) if "content" in d and d.get("type") not in KNOWN}
    if bad:
        fails.append(f"unknown block type(s) {sorted(bad)} render as anonymous prose")
    return fails
