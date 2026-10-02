"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("act_drink")
    if not c:
        return ["act_drink is gone"]
    fails = []
    ops = {e.get("op") for e in effects(game)}
    if "subtract" in ops:
        fails.append("an effect uses op='subtract', which the engine never applies")
    blob = json.dumps(c)
    if "15" not in blob:
        fails.append("act_drink shows no $15 price anywhere")
    energy = [e for e in effects(c) if e.get("trait") == "energy"]
    costs = [d for d in iter_dicts(c) if isinstance(d.get("costs"), (dict, list)) and "energy" in json.dumps(d["costs"])]
    if not energy and not costs:
        fails.append("act_drink does not touch energy")
    return fails
