"""One check command for a game built with author-game-lean.

    python3 check.py games/<slug> [--release]

Checks:
  merge      scripts/merge_toml_phases.py runs and the merged TOML parses (--no-dev under --release)
  reach      reach.py finds no scene, media spot or portrait that can never show
  approvals  every STATE.md piece with a built date has a current approval (approve.status == approved)
  builds     every canvas in the merged TOML is listed in the Builds: line of an APPROVED card
             (a changed card covers nothing; canvases from 6_dev_shortcuts.toml are skipped)
  release    --release only: no dev canvas id or name is left in the merged TOML or the built HTML

Output: one verdict line (GREEN, RED <n>, or INCOMPLETE: <reason>), then every red, with NEW on the ones
that weren't red last run, then what was fixed since last run. It never says GREEN when a check was skipped.
Exit 0 green, 1 red, 2 incomplete. The last run is kept in games/<slug>/.check_last.json (git-ignored).
"""
import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]  # scripts -> author-game-lean -> skills -> .claude -> repo
MERGE = REPO / "scripts" / "merge_toml_phases.py"
MERGED = "7_final_game.toml"
DEV_PHASE = "6_dev_shortcuts.toml"  # scripts/merge_toml_phases.py:62
LAST = ".check_last.json"

sys.path.insert(0, str(HERE))
import approve  # noqa: E402
import reach  # noqa: E402

GREEN, RED, INCOMPLETE = "green", "red", "incomplete"


# ── inputs ────────────────────────────────────────────────────────────────────────────────────────────────

def merge(game_dir, release=False):
    """Run the repo's merge script. Returns (status, rows)."""
    if not MERGE.is_file():
        return INCOMPLETE, [f"merge script not found at {MERGE}"]
    cmd = [sys.executable, str(MERGE), str(game_dir), "--validate"] + (["--no-dev"] if release else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        last = (p.stderr.strip() or p.stdout.strip() or f"exit {p.returncode}").splitlines()[-1]
        return RED, [f"merge failed: {last}"]
    return GREEN, []


def load_merged(game_dir):
    path = Path(game_dir) / "toml_phases" / MERGED
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def dev_canvases(game_dir):
    """{id: name} for the canvases in 6_dev_shortcuts.toml, or None when there is no such file."""
    path = Path(game_dir) / "toml_phases" / DEV_PHASE
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return {}
    return {c["id"]: c.get("name", "") for c in data.get("canvases", []) if c.get("id")}


def state_pieces(game_dir):
    """Rows of STATE.md's piece table as dicts, or None when there is no STATE.md or no table."""
    path = Path(game_dir) / "STATE.md"
    if not path.is_file():
        return None
    head, rows = None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            if head is not None and rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            if cells and cells[0] == "piece":
                head = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(head, cells))
        if row.get("piece") and not row["piece"].startswith("<"):
            rows.append(row)
    return rows if head is not None else None


def filled(cell):
    return bool(cell) and not cell.startswith("<")


def card_builds(game_dir):
    """{card id: set of canvas ids} from every card's Builds: line."""
    out = {}
    for path in sorted((Path(game_dir) / "cards").glob("*.md")):
        m = re.search(r"^Builds:\s*(.*)$", path.read_text(encoding="utf-8"), re.M)
        ids = {x.strip(" `") for x in (m.group(1).split(",") if m else [])}
        out[path.stem] = {x for x in ids if x and x.lower() != "none" and not x.startswith("<")}
    return out


# ── checks ────────────────────────────────────────────────────────────────────────────────────────────────

def check_reach(game):
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    rows = reach.rows(reach.check(game))
    return (RED, rows) if rows else (GREEN, [])


def check_approvals(game_dir):
    pieces = state_pieces(game_dir)
    if pieces is None:
        return INCOMPLETE, ["no STATE.md piece table"]
    rows = []
    for p in pieces:
        if filled(p.get("built", "")):
            s = approve.status(game_dir, p["piece"])
            if s != "approved":
                why = "its card changed after the yes" if s == "changed" else "no approval for its card"
                rows.append(f"piece `{p['piece']}` is built but {why}")
    return (RED, rows) if rows else (GREEN, [])


def check_builds(game_dir, game):
    """Every non-dev canvas must be listed by an approved card. A changed card covers nothing."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    dev = dev_canvases(game_dir) or {}
    covered = set()
    for cid, ids in card_builds(game_dir).items():
        if approve.status(game_dir, cid) == "approved":
            covered |= ids
    rows = [f"canvas `{c['id']}` is built but never approved (no approved card lists it in Builds:)"
            for c in game.get("canvases", []) if c.get("id") not in dev and c.get("id") not in covered]
    return (RED, rows) if rows else (GREEN, [])


def check_release(game_dir, game):
    """After a --no-dev merge, no dev canvas may survive in the TOML or in the built HTML."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    dev = dev_canvases(game_dir)
    if dev is None:
        return GREEN, []  # no dev file: nothing can leak from it
    rows = [f"dev canvas `{c['id']}` is in the release merge" for c in game.get("canvases", []) if c.get("id") in dev]
    html = sorted((Path(game_dir) / "output").rglob("*.html"))
    if not html:
        return (RED, rows) if rows else (INCOMPLETE, ["no built HTML in output/ to search for dev canvases"])
    for path in html:
        text = path.read_text(encoding="utf-8", errors="replace")
        for cid, name in dev.items():
            for s in filter(None, (cid, name)):
                if s in text:
                    rows.append(f"dev canvas {'id' if s == cid else 'name'} `{s}` is in {path.name}")
    return (RED, rows) if rows else (GREEN, [])


def run_all(game_dir, release=False):
    results = {"merge": merge(game_dir, release)}
    game = load_merged(game_dir) if results["merge"][0] == GREEN else None
    results["reach"] = check_reach(game)
    results["approvals"] = check_approvals(game_dir)
    results["builds"] = check_builds(game_dir, game)
    if release:
        results["release"] = check_release(game_dir, game)
    return results


# ── report ────────────────────────────────────────────────────────────────────────────────────────────────

def report(results, last):
    """Lines to print and the exit code. Every red is printed; NEW marks reds absent last run."""
    reds = [(k, r) for k, (s, rows) in results.items() if s == RED for r in rows]
    incomplete = [(k, r) for k, (s, rows) in results.items() if s == INCOMPLETE for r in rows]
    last_reds = {(k, r) for k, v in last.items() if v[0] == RED for r in v[1]}
    last_inc = {k for k, v in last.items() if v[0] == INCOMPLETE}
    if reds:
        head = f"RED {len(reds)}" + (f" · INCOMPLETE: {'; '.join(r for _, r in incomplete)}" if incomplete else "")
        code = 1
    elif incomplete:
        head, code = f"INCOMPLETE: {'; '.join(f'{k}: {r}' for k, r in incomplete)}", 2
    else:
        head, code = "GREEN", 0
    lines = [head]
    lines += [f"  {'NEW ' if (k, r) not in last_reds else ''}RED [{k}] {r}" for k, r in reds]
    now_reds = set(reds)
    lines += [f"  FIXED [{k}] {r}" for k, r in sorted(last_reds - now_reds)]
    lines += [f"  NOW INCOMPLETE [{k}] {r}" for k, r in incomplete if k not in last_inc]
    lines += [f"  CHECKED AGAIN [{k}]" for k in sorted(last_inc) if k in results and results[k][0] != INCOMPLETE]
    changed = [l for l in lines[1:] if l.lstrip().startswith(("NEW", "FIXED", "NOW INCOMPLETE", "CHECKED AGAIN"))]
    if last and not changed:
        lines.append("  no change since last run")
    return lines, code


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a game built with author-game-lean.")
    ap.add_argument("game_dir")
    ap.add_argument("--release", action="store_true")
    args = ap.parse_args(argv)
    game_dir = Path(args.game_dir)
    store = game_dir / LAST
    try:
        saved = json.loads(store.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        saved = {}
    mode = "release" if args.release else "dev"
    results = run_all(game_dir, args.release)
    lines, code = report(results, {k: tuple(v) for k, v in saved.get(mode, {}).items()})
    print("\n".join(lines))
    saved[mode] = {k: [s, rows] for k, (s, rows) in results.items()}
    store.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
