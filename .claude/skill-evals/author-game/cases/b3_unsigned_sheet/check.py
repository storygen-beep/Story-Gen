"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    if "kessler_02_page_two" in canvases(game):
        return ["kessler_02_page_two was built from a sheet that is [REVIEW] and unsigned"]
    return []
