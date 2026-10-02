"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


def _late_path_minutes(canvas, ch):
    """Minutes spent by a 'late' choice, plus the longest exit of the node it opens (if any)."""
    total = ch.get("time_progression_minutes") or 0
    target = (ch.get("nodeId") or "").split(".")[-1]
    node = next((n for n in canvas.get("nodes", []) if n.get("id") == target), None)
    if node:
        # An exit is either a choices list or a location exit whose minutes sit under `config`.
        total += max((d.get("time_progression_minutes") or 0 for d in iter_dicts(node.get("exit_block", {}))), default=0)
    return total


def check(game, base):
    c = canvases(game).get("act_work_shift")
    if not c:
        return ["act_work_shift is gone"]
    late = [x for x in choices(c) if "late" in x["text"].lower()]
    if not late:
        return ["no 'work late' choice in act_work_shift"]
    if not any(_late_path_minutes(c, x) >= 120 for x in late):
        return ["the work-late path does not spend two hours"]
    return []
