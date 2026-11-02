"""Release case check: returns a list of failure messages (empty means pass)."""
from lib import *



def _project_version(game):
    return str(game.get("project", {}).get("version", ""))


def _page(ledger):
    return (ledger or {}).get("release_page") or {}

def check(game, base, ledger=None):
    if "theo_knows_friday" not in flag_keys(game):
        return ["the live flag key theo_knows_friday is gone; shipped saves lose what it recorded"]
    return []
