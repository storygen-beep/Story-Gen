"""Build case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(game, base):
    old = {l["id"] for l in base["locations"]}
    new = sorted(l["id"] for l in game["locations"] if l["id"] not in old)
    fails = []
    if new:
        fails.append(f"new location(s) {new} built with no signed place sheet")
    k1, b1 = canvases(game).get("kessler_01_page_one"), canvases(base).get("kessler_01_page_one")
    if k1 and b1 and k1["trigger"].get("location") != b1["trigger"].get("location"):
        fails.append("kessler_01_page_one was moved without a signed sheet for the new place")
    return fails
