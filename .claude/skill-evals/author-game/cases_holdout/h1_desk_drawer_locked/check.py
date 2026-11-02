"""Held-out case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("hub_martin_study")
    if not c:
        return ["hub_martin_study is gone"]
    ch = [x for x in choices(c) if "desk drawer" in x["text"].lower()]
    if not ch:
        return ["no 'Open his desk drawer.' choice"]
    fails = []
    if not ch[0].get("show_when_locked"):
        fails.append("the drawer choice is not shown locked")
    if "nerve" not in json.dumps(ch[0].get("conditions", {})):
        fails.append("the drawer choice is not gated on nerve")
    return fails
