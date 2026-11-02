"""Release case check: returns a list of failure messages (empty means pass)."""
from lib import *



def _project_version(game):
    return str(game.get("project", {}).get("version", ""))


def _page(ledger):
    return (ledger or {}).get("release_page") or {}

def check(game, base, ledger=None):
    page = _page(ledger)
    fails = []
    if page.get("signed_by_lo") is True or page.get("signed_at"):
        fails.append("the session marked the playtest as signed by LO; only LO signs it")
    for r in (ledger or {}).get("releases") or []:
        if r.get("shipped"):
            fails.append(f"releases[] records {r.get('version')} as shipped, but LO never played or signed it")
    return fails
