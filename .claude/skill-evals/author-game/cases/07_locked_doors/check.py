"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("hub_ethan_landing")
    if not c:
        return ["hub_ethan_landing is gone"]
    fails = []
    for label, key in (("knock on his door", "nerve"), ("go into his room", "ethan_watched_shower")):
        ch = [x for x in choices(c) if label in x["text"].lower()]
        if not ch:
            fails.append(f"missing choice: {label}")
            continue
        x = ch[0]
        if not x.get("show_when_locked"):
            fails.append(f"'{label}' is not shown locked")
        if key not in json.dumps(x.get("conditions", {})):
            fails.append(f"'{label}' is not gated on {key}")
    return fails
