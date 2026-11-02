"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


SPEC = {"location": "pool_terrace", "gate": {"noor_stage": (['eq', 'gte'], 1), "kessler_stage": (['gte', 'gt', 'eq'], 1)},
        "sets": {"noor_stage": 2}, "when": (5, 22 * 60 + 30), "hook": "bring a member",
        "answers": ["naked", "underwear", "watch"]}


def check(game, base):
    return scene_matches_sheet(game, "noor_02_the_pool", SPEC)
