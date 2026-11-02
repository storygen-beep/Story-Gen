"""Release case check: returns a list of failure messages (empty means pass)."""
from lib import *



def _project_version(game):
    return str(game.get("project", {}).get("version", ""))


def _page(ledger):
    return (ledger or {}).get("release_page") or {}

def check(game, base, ledger=None):
    fails = []
    if _project_version(game) != "0.1.1":
        fails.append(f"[project] version is {_project_version(game)!r}, not 0.1.1")
    if str(_page(ledger).get("version", "")) != "0.1.1":
        fails.append(f"release_page.version is {_page(ledger).get('version')!r}, not 0.1.1")
    if not (_page(ledger).get("reader", {}).get("hub_jade_club") or {}):
        fails.append("hub_jade_club was touched but has no reader verdicts in release_page.reader")
    if json.dumps(canvases(game).get("hub_jade_club"), sort_keys=True) == json.dumps(canvases(base)["hub_jade_club"], sort_keys=True):
        fails.append("hub_jade_club was not changed")
    return fails
