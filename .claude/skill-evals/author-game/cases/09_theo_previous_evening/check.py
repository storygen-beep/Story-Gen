"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("hub_theo_bar")
    if not c:
        return ["hub_theo_bar is gone"]
    if len(canvas_text(c)) <= len(canvas_text(canvases(base)["hub_theo_bar"])):
        return ["hub_theo_bar has no new text"]
    return []
