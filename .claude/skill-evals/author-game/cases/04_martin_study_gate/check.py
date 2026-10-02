"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("hub_martin_study")
    if not c:
        return ["hub_martin_study is gone"]
    fails = []
    ch = [x for x in choices(c) if "stay after he closes the door" in x["text"].lower()]
    if not ch:
        return ["no 'Stay after he closes the door.' choice in hub_martin_study"]
    gated = any(i.get("trait_key") == "martin_stage" and
                ((i.get("operator") == "gte" and i.get("value") == 3) or (i.get("operator") == "gt" and i.get("value") == 2))
                for x in ch for i in condition_items(x))
    if not gated:
        fails.append("the choice is not gated on martin_stage >= 3")
    for cv in changed_canvases(game, base):
        for cs in condition_sets(cv):
            if cs.get("version") != "1.0":
                fails.append(f"{cv['id']}: a conditions table has no version='1.0' (fails open)")
                break
    return fails
