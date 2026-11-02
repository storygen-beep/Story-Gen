"""Release case check: returns a list of failure messages (empty means pass)."""
from lib import *



def _project_version(game):
    return str(game.get("project", {}).get("version", ""))


def _page(ledger):
    return (ledger or {}).get("release_page") or {}

def check(game, base, ledger=None):
    c = canvases(game).get("hub_theo_bar")
    if not c:
        return ["hub_theo_bar is gone"]
    ch = [x for x in choices(c) if "key card" in x["text"].lower()]
    if not ch:
        return ["no 'Take the key card.' choice in hub_theo_bar"]
    page_door = _page(ledger).get("door") or {}
    board_door = ((ledger or {}).get("board") or {}).get("door") or {}
    fails = []
    if page_door.get("canvas") != "hub_theo_bar" or "key card" not in str(page_door.get("choice", "")).lower():
        fails.append(f"release_page.door is {page_door}, not the key-card choice in hub_theo_bar")
    if board_door and board_door != page_door:
        fails.append(f"board.door {board_door} disagrees with release_page.door {page_door}")
    return fails
