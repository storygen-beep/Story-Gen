"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    if json.dumps(game, sort_keys=True) == json.dumps(base, sort_keys=True):
        return ["nothing was written"]
    rent = game["settings"]["rent"]
    amounts = {s["amount"] for s in rent.get("stages", [])} | {rent.get("amount")}
    fails = []
    for c in changed_canvases(game, base):
        for e in effects(c):
            v = e.get("value")
            if e.get("trait") == "money" and isinstance(v, (int, float)) and v < 0 and abs(v) in amounts:
                fails.append(f"{c['id']}: takes ${abs(v)} itself, but the engine already charges rent")
    return fails
