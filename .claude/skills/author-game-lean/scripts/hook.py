"""Claude Code hooks for author-game-lean, so the state and the checks never depend on memory (C2083).

    hook.py session-start   print every lean game's STATE.md (a games/*/STATE.md ending in a `Next step:` line)
    hook.py after-bash      after a Bash call that ran merge_toml_phases or package_from_toml on a lean game,
                            run check.py on it; red or incomplete exits 2 so the session sees it

Wired in .claude/settings.json and run with "$CLAUDE_PROJECT_DIR"/venv/bin/python (check.py needs tomllib, 3.11+;
plain python3 on this machine is 3.10). Games are looked up under $CLAUDE_PROJECT_DIR. It never blocks a session
start or a command: it only shows things.
"""
import contextlib
import io
import json
import os
import re
import shlex
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

BUILD_TOOLS = re.compile(r"merge_toml_phases|package_from_toml")


def project_dir():
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or HERE.parents[3])


def is_lean_game(path):
    state = Path(path) / "STATE.md"
    if not (state.is_file() and (Path(path) / "toml_phases").is_dir()):
        return False
    lines = [l for l in state.read_text(encoding="utf-8").splitlines() if l.strip()]
    return bool(lines) and lines[-1].startswith("Next step:")


def session_start():
    for game in sorted((project_dir() / "games").glob("*")):
        if is_lean_game(game):
            print(f"## {game.name}: games/{game.name}/STATE.md\n")
            print((game / "STATE.md").read_text(encoding="utf-8"))
    return 0


def games_in(command, cwd):
    """Lean game folders a command names: each argument, or one of its parents, that holds STATE.md."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    found = []
    for tok in tokens:
        p = Path(tok) if os.path.isabs(tok) else Path(cwd) / tok
        for candidate in [p, *list(p.parents)[:3]]:
            if is_lean_game(candidate) and candidate.resolve() not in found:
                found.append(candidate.resolve())
                break
    return found


def after_bash(event):
    command = (event.get("tool_input") or {}).get("command") or ""
    if not BUILD_TOOLS.search(command) or "author-game-lean/scripts/build.py" in command:
        return 0  # not a build, or build.py, which runs check.py itself
    import check
    worst, report = 0, []
    for game in games_in(command, event.get("cwd") or project_dir()):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check.main([str(game)])
        worst = max(worst, code)
        report.append(f"check.py {game.name}: {out.getvalue().strip()}")
    if not report:
        return 0
    text = "\n".join(report)
    if worst:
        print(text, file=sys.stderr)
        return 2
    print(text)
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else ""
    if mode == "session-start":
        return session_start()
    if mode == "after-bash":
        try:
            event = json.load(sys.stdin)
        except ValueError:
            return 0
        return after_bash(event)
    print(f"usage: hook.py session-start | after-bash (got {mode!r})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
