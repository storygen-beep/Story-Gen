"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    c = canvases(game).get("hub_martin_breakfast")
    if not c:
        return ["hub_martin_breakfast is gone"]
    if json.dumps(c, sort_keys=True) == json.dumps(canvases(base)["hub_martin_breakfast"], sort_keys=True):
        return ["hub_martin_breakfast was not changed"]
    if not any("npc_diane" in json.dumps(i) for i in condition_items(c)):
        return ["no condition in hub_martin_breakfast reads whether Diane is present"]
    old = text_blocks(canvases(base)["hub_martin_breakfast"])
    now = {b["content"] for b in text_blocks(c)}
    lost = [b["content"][:60] for b in old if b["content"] not in now]
    return [f"existing line removed: {t}" for t in lost[:3]]
