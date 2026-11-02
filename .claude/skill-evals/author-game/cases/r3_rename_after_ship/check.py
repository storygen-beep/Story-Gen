"""Release case check: returns a list of failure messages (empty means pass)."""
from lib import *



def _project_version(game):
    return str(game.get("project", {}).get("version", ""))


def _page(ledger):
    return (ledger or {}).get("release_page") or {}

def check(game, base, ledger=None):
    lost = sorted(ids(base) - ids(game))
    if lost:
        return [f"a shipped id was removed or renamed (saves would strand): {', '.join(lost[:5])}"]
    return []
