"""Build a game built with author-game-lean, refusing anything LO hasn't approved.

    python3 build.py games/<slug> [--release]

1. Merge (dev form, or --no-dev under --release: scripts/merge_toml_phases.py:80).
2. Refuse, and package nothing, if any canvas is on no approved card's Builds: line, or any STATE.md piece
   marked built has no current approval (check.py's `builds` and `approvals` checks).
3. Package with package_from_toml (no database by default, package_from_toml.py:218): a dev build goes to
   output/ with --dev, a release to output/ without it. Both go to output/, the folder LO plays from (LO, 2026-11-23).
4. Run check.py, so the checks never depend on memory.
Exit 0 when built and green, non-zero otherwise.
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check  # noqa: E402


def refusals(game_dir):
    """Rows that stop the build: unapproved canvases and built pieces with no current approval."""
    game = check.load_merged(game_dir)
    if game is None:
        return ["the merged TOML did not parse"]
    rows = []
    for status, found in (check.check_builds(game_dir, game), check.check_approvals(game_dir)):
        if status == check.RED:
            rows += found
    return rows


def package(game_dir, release=False):
    """Every build goes to games/<slug>/output/, the folder LO plays from on his phone (LO, 2026-11-23:
    builds kept going to output_dev/, which he doesn't play). A dev build adds --dev (package_from_toml.py:151)."""
    game_dir = Path(game_dir).resolve()
    cmd = [sys.executable, str(check.REPO / "manage.py"), "package_from_toml",
           "--file", str(game_dir / "toml_phases" / check.MERGED),
           "--output", str(game_dir / "output"), "--gen-version", "v2"]
    if not release:
        cmd.append("--dev")
    return subprocess.run(cmd, cwd=check.REPO).returncode


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge, refuse unapproved canvases, package, then check.")
    ap.add_argument("game_dir")
    ap.add_argument("--release", action="store_true")
    args = ap.parse_args(argv)
    game_dir = Path(args.game_dir)

    status, rows = check.merge(game_dir, args.release)
    if status != check.GREEN:
        print("REFUSED: " + "; ".join(rows))
        return 1
    stop = refusals(game_dir)
    if stop:
        print("REFUSED: nothing was packaged")
        print("\n".join(f"  {r}" for r in stop))
        return 1
    if package(game_dir, args.release) != 0:
        print("BUILD FAILED: package_from_toml exited non-zero")
        return 1
    return check.main([str(game_dir)] + (["--release"] if args.release else []))


if __name__ == "__main__":
    sys.exit(main())
