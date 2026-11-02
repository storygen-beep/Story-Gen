"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *




def check(game, base):
    rows = npc(game, "npc_theo").get("schedules", [])
    fails = []
    for day, start, end in ((4, 22 * 60, 24 * 60), (5, 0, 2 * 60)):
        for m in range(start, end, 30):
            where = presence(rows, day, m)
            if where != "hotel_bar":
                fails.append(f"day {day} {m // 60:02d}:{m % 60:02d}: Theo resolves to {where}, not hotel_bar")
    return fails[:4]
