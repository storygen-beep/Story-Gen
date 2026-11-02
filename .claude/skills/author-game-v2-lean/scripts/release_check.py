"""Check that a release is prepared for LO's playtest.

    python3 .claude/skills/author-game-v2-lean/scripts/release_check.py <slug> --start   # before the release work
    python3 .claude/skills/author-game-v2-lean/scripts/release_check.py <slug>           # when the release is prepared

It runs author-game-v2's own `--ship` BLOCK rows (gates.py `ship_rows`) with the three parts that need
a built game stubbed out — the release build, the saves archive and the live ladder climb — the same
way v2's own tests do (`scripts/tests/test_gates_ws6.py`). Those three, and LO's signature, are listed
as still to do, never as passed. On top it checks what the rows do not:

- `[project] version` and `release_page.version` say the same version, and it is not one already shipped;
- no save-visible id or live flag key that existed at `--start` is gone (the-returning-player.md §2, §3).

Prints READY FOR LO and exits 0 when everything a session can do is done; otherwise RED and exit 1.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import tomllib as _toml            # py3.11+
except ModuleNotFoundError:            # py3.10, same fallback as gates.py
    import tomli as _toml

ROOT = Path(__file__).resolve().parents[4]
V2_SCRIPTS = ROOT / ".claude/skills/author-game-v2/scripts"
MERGE_PY = ROOT / "scripts/merge_toml_phases.py"

NEEDS_BUILD = ("each step fires when unlocked, and each unlock is earnable",
               "the build exists and is a release build", "last release's saves still load")
LO_ROW = "LO signed the playtest"
SAVE_IDS = ("canvases", "locations", "npcs", "clothing", "quests", "fast_jobs")


def game_dir(slug: str) -> Path:
    return ROOT / "games" / slug


def load_toml(slug: str) -> dict:
    with open(game_dir(slug) / "toml_phases" / "7_final_game.toml", "rb") as fh:
        return _toml.load(fh)


def load_ledger(slug: str) -> dict:
    p = game_dir(slug) / "v2_state.json"
    return json.loads(p.read_text()) if p.exists() else {}


def merge(slug: str) -> None:
    proc = subprocess.run([sys.executable, str(MERGE_PY), "--validate", str(game_dir(slug))],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"RED  the phase files do not merge or parse:\n{proc.stdout}{proc.stderr}")


def ship_rows(slug: str) -> list[tuple]:
    sys.path.insert(0, str(V2_SCRIPTS))
    spec = importlib.util.spec_from_file_location("v2_gates", V2_SCRIPTS / "gates.py")
    gates = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gates)
    gates.release_mode = lambda slug: 0
    gates.saves_mode = lambda slug, *a, **k: 2
    gates._ship_ladders = lambda *a, **k: (None, "needs the build", [])
    block, _report = gates.ship_rows(slug, root=str(ROOT))
    return block


def save_ids(game: dict) -> set[str]:
    """Ids a save stores (the-returning-player.md §2). Nodes are out: deleting one is safe."""
    return {f"{k}:{x['id']}" for k in SAVE_IDS for x in (game.get(k) or []) if x.get("id")}


def flag_keys(game: dict) -> set[str]:
    keys = set()

    def walk(o):
        if isinstance(o, dict):
            for k in ("flag", "flag_key"):
                if isinstance(o.get(k), str):
                    keys.add(o[k])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(game)
    return keys


def snapshot_path(slug: str) -> Path:
    key = hashlib.sha1(str(game_dir(slug).resolve()).encode()).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"release_check_{slug}_{key}.json"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    slug = sys.argv[1]
    merge(slug)
    game, ledger = load_toml(slug), load_ledger(slug)

    if "--start" in sys.argv[2:]:
        snapshot_path(slug).write_text(json.dumps({"ids": sorted(save_ids(game)), "flags": sorted(flag_keys(game))}))
        print(f"START  {slug}: snapshot of {len(save_ids(game))} ids and {len(flag_keys(game))} flag keys.")
        return 0

    reds, todo = [], []
    for name, ok, headline, detail in ship_rows(slug):
        if name in NEEDS_BUILD:
            todo.append(f"at ship time: {name}")
        elif name == LO_ROW:
            if ok is not True:
                todo.append("LO: play every person on the release page from a new game to the door, then sign "
                            "(release_page.signed_by_lo, signed_at). A session never signs.")
        elif ok is False:
            reds.append(f"--ship BLOCK: {name} — {headline}")
            reds += [f"    {d}" for d in (detail or [])[:3]]

    page = ledger.get("release_page") or {}
    project_v = str(game.get("project", {}).get("version", ""))
    page_v = str(page.get("version", ""))
    if project_v != page_v:
        reds.append(f"version: [project] says {project_v!r}, release_page says {page_v!r}; they must agree")
    shipped = {str(r.get("version")) for r in ledger.get("releases") or [] if r.get("shipped")}
    if project_v in shipped:
        reds.append(f"version {project_v} has already shipped; a new release needs a new version")

    snap = snapshot_path(slug)
    if snap.exists():
        before = json.loads(snap.read_text())
        gone_ids = sorted(set(before["ids"]) - save_ids(game))
        gone_flags = sorted(set(before["flags"]) - flag_keys(game))
        if gone_ids:
            reds.append("ids removed or renamed (a save parked on one lands nowhere; change the name, "
                        f"never the id): {', '.join(gone_ids[:6])}")
        if gone_flags:
            reds.append("flag keys removed or renamed (a shipped save loses what they recorded; "
                        f"deprecate and add): {', '.join(gone_flags[:6])}")
    else:
        todo.append(f"no --start snapshot, so removed ids and flags were not checked; run `{slug} --start` first next time")

    if reds:
        print(f"RED  {slug} {project_v}: {len([r for r in reds if not r.startswith('    ')])} problem(s).")
        for r in reds:
            print(r if r.startswith("    ") else f"  - {r}")
        return 1
    print(f"READY FOR LO  {slug} {project_v}: every check a session can run passes.")
    for t in todo:
        print(f"  - {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
