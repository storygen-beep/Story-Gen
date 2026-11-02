"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


SAMPLES = [(1, 20 * 60, "bar_floor"), (3, 22 * 60 + 30, "library"), (4, 23 * 60 + 30, "members_floor"),
           (0, 20 * 60, None), (6, 20 * 60, None)]


def check(game, base):
    return schedule_matches_sheet(game, "kessler", SAMPLES)
