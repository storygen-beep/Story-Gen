"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


SAMPLES = [(0, 12 * 60, "staff_house"), (2, 17 * 60 + 30, "dressing_room"), (4, 20 * 60, "bar_floor"),
           (5, 23 * 60, "pool_terrace"), (6, 20 * 60, None), (0, 20 * 60, None)]


def check(game, base):
    return schedule_matches_sheet(game, "noor", SAMPLES)
