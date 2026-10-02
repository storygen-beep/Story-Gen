"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *



def presence(npc_row_list, day, minute):
    """Where an NPC is, per v2.py:4149-4150: weekday matched against TODAY first, then the time
    window (which wraps past midnight, v2.py:4517). First matching row wins."""
    for s in npc_row_list:
        days = s.get("weekdays")
        if days not in (None, []) and day not in days:
            continue
        st, en = to_minutes(s["start_time"]), to_minutes(s.get("end_time") or s["start_time"])
        if not s.get("end_time"):
            en = st + 60
        ok = (minute >= st or minute < en) if en < st else (st <= minute < en)
        if ok:
            return s["location"]
    return None

def check(game, base):
    rows = npc(game, "npc_theo").get("schedules", [])
    fails = []
    for day, start, end in ((4, 22 * 60, 24 * 60), (5, 0, 2 * 60)):
        for m in range(start, end, 30):
            where = presence(rows, day, m)
            if where != "hotel_bar":
                fails.append(f"day {day} {m // 60:02d}:{m % 60:02d}: Theo resolves to {where}, not hotel_bar")
    return fails[:4]
