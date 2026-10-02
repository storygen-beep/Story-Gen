"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def _evening_only(conds):
    for i in condition_items(conds):
        if i.get("type") == "time_of_day" and to_minutes(i.get("start_time", "00:00")) >= 17 * 60:
            return True
    return False

def check(game, base):
    c = canvases(game).get("hub_diane_home")
    if not c:
        return ["hub_diane_home is gone"]
    ch = [x for x in choices(c) if "tonight" in x["text"].lower()]
    if not ch:
        return ["no 'tonight' choice in hub_diane_home"]
    # Diane is in the kitchen at breakfast (07:00-08:30) too, so the choice needs its own evening gate.
    if not (_evening_only(ch[0].get("conditions", {})) or _evening_only(c["trigger"].get("conditions", {}))):
        return ["the 'tonight' choice can show at breakfast: no evening time_of_day gate"]
    return []
