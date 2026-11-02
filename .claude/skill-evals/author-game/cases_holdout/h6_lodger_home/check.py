"""Held-out case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base, ledger=None):
    """v2's rule (`the-map.md` R2, `state.md` board.map.homes): every declared character has a home
    in the ledger, a room or "offscreen". A lodger who rents a room in the house has that room as
    her home, it is a real room (not a hallway), and her schedule puts her in it at some hour.

    Revised 2026-10-03. The first version required her to be in her room at 02:00. No character
    in the fixture is anywhere at 02:00 (the game sleeps everyone off-screen), so that was a rule
    the exam invented, not one v2 teaches."""
    new_npcs = [n for n in game.get("npcs", []) if npc(base, n["id"]) is None]
    ruth = next((n for n in new_npcs if "ruth" in (n.get("name", "") + n["id"]).lower()), None)
    if not ruth:
        return ["no new NPC named Ruth"]
    kinds = {l["id"]: l.get("kind") for l in game.get("locations", [])}
    home = (((ledger or {}).get("board") or {}).get("map") or {}).get("homes", {}).get(ruth["id"])
    if home is None:
        return [f"{ruth['id']} has no home in v2_state.json board.map.homes"]
    if home == "offscreen":
        return ["a lodger who rents a room in the house is declared as sleeping offscreen"]
    fails = []
    if home not in kinds:
        fails.append(f"Ruth's home {home} is not a declared location")
    elif kinds[home] == "thoroughfare":
        fails.append(f"Ruth's home {home} is a thoroughfare, not a room")
    if not any(s.get("location") == home for s in ruth.get("schedules", [])):
        fails.append(f"Ruth's schedule never puts her in her own room ({home})")
    return fails
