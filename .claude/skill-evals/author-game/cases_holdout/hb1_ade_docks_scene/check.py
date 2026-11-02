"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


SPEC = {"location": "the_docks", "gate": {"ade_stage": (['eq', 'gte'], 1)}, "sets": {"ade_stage": 2},
        "sets_flags": ["knows_service_stairs"], "when": (0, 12 * 60), "hook": "service stairs"}


def check(game, base):
    return scene_matches_sheet(game, "ade_02_the_docks", SPEC)
