"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *




def check(game, base):
    rows = npc(game, "npc_theo").get("schedules", [])
    fails = []
    for m in range(14 * 60, 18 * 60, 30):
        if presence(rows, 2, m) != "firm":
            fails.append(f"Wednesday {m // 60:02d}:{m % 60:02d}: Theo is not at the firm")
    # Double-booking: two rows at different places that overlap on the same day.
    def spans(s):
        st, en = to_minutes(s["start_time"]), to_minutes(s.get("end_time") or s["start_time"])
        return [(st, en)] if en > st else [(st, 24 * 60), (0, en)]
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a["location"] == b["location"]:
                continue
            days = set(a.get("weekdays") or range(7)) & set(b.get("weekdays") or range(7))
            if days and any(x0 < y1 and y0 < x1 for x0, x1 in spans(a) for y0, y1 in spans(b)):
                fails.append(f"double-booked on days {sorted(days)}: {a['location']} and {b['location']} overlap")
    return fails[:4]
