"""Case check: returns a list of failure messages (empty means pass)."""
from lib import *


SENTENCE = re.compile(r"(?<=[.!?])\s+")


def check(game, base):
    """An explicit beat carries 3+ frozen-list words and its last sentence stays on the body.
    A beat here is one text block; interiority is allowed in its OWN block after the act."""
    rx = explicit_regex()
    new = [c for c in new_canvases(game, base) if c["trigger"].get("location") == "bathroom"]
    if not new:
        return ["no new bathroom canvas"]
    fails = []
    for c in new:
        beats = [b for b in text_blocks(c) if b.get("type") in ("paragraph", "dialog", "thought_bubble")]
        explicit = [b for b in beats if rx.search(b["content"])]
        if not explicit:
            fails.append(f"{c['id']}: the scene names nothing explicit")
        for b in explicit:
            n = len(rx.findall(b["content"]))
            if n < 3:
                fails.append(f"{c['id']}: explicit beat has {n} frozen-list words (floor 3): {b['content'][:60]}")
            last = SENTENCE.split(b["content"].strip())[-1]
            if not rx.search(last):
                fails.append(f"{c['id']}: explicit beat pivots off the body at its last sentence: {last[:60]}")
    return fails[:5]
