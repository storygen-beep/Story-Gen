"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    fails = []
    new_npcs = [n for n in game.get("npcs", []) if npc(base, n["id"]) is None]
    priya = next((n for n in new_npcs if "priya" in (n.get("name", "") + n["id"]).lower()), None)
    if not priya:
        return ["no new NPC named Priya"]
    if not any(s.get("location") == "firm" for s in priya.get("schedules", [])):
        fails.append("Priya has no schedule row at the firm")
    meets = [c for c in new_canvases(game, base)
             if priya["id"] in (c["trigger"].get("npc"), c["trigger"].get("requires_npc"))
             or "priya" in canvas_text(c).lower()]
    if not meets:
        fails.append("no new canvas for Priya's first meeting")
    elif not any("paralegal" in canvas_text(c).lower() for c in meets):
        fails.append("first meeting never says she is the paralegal (role before name, F7)")
    return fails
