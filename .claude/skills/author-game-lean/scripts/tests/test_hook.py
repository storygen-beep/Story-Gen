"""hook.py, run exactly as Claude Code runs it: the command string from .claude/settings.json, through a shell,
with CLAUDE_PROJECT_DIR set. The project dir is a throwaway root that links the real venv and the real skill and
holds one tiny game; nothing in games/ is read or written."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parents[3]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiny_game import canvas, make_game  # noqa: E402

SETTINGS = json.loads((REPO / ".claude" / "settings.json").read_text())


def hook_command(event):
    [entry] = SETTINGS["hooks"][event]
    [h] = entry["hooks"]
    return entry.get("matcher"), h["command"]


@pytest.fixture
def root(tmp_path):
    """A project dir: venv and the skill linked from the real repo, the tiny game under games/."""
    r = tmp_path / "project"
    (r / ".claude" / "skills").mkdir(parents=True)
    (r / "venv").symlink_to(REPO / "venv")
    (r / ".claude" / "skills" / "author-game-lean").symlink_to(SCRIPTS.parent)
    (r / "games").mkdir()
    make_game(r / "games")
    return r


def run_hook(root, event, stdin=""):
    _, cmd = hook_command(event)
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
    return subprocess.run(["/bin/sh", "-c", cmd], input=stdin, capture_output=True, text=True, env=env, cwd=root)


def bash_event(root, command):
    return json.dumps({"hook_event_name": "PostToolUse", "tool_name": "Bash", "cwd": str(root),
                       "tool_input": {"command": command}})


def test_settings_run_the_venv_python():
    for event in ("SessionStart", "PostToolUse"):
        assert hook_command(event)[1].startswith('"$CLAUDE_PROJECT_DIR"/venv/bin/python ')
    assert hook_command("PostToolUse")[0] == "Bash"


def test_session_start_prints_a_lean_games_state(root):
    p = run_hook(root, "SessionStart")
    assert p.returncode == 0 and "games/tiny/STATE.md" in p.stdout and "Next step: build — p1" in p.stdout


def test_session_start_skips_a_game_without_a_lean_state(root):
    (root / "games" / "tiny" / "STATE.md").write_text("# not a lean state\n")
    p = run_hook(root, "SessionStart")
    assert p.returncode == 0 and p.stdout == ""


def test_after_a_clean_merge_check_runs_and_is_green(root):
    p = run_hook(root, "PostToolUse", bash_event(root, "venv/bin/python scripts/merge_toml_phases.py games/tiny"))
    assert p.returncode == 0 and "check.py tiny: GREEN" in p.stdout


def test_planted_unapproved_canvas_after_package_exits_2_with_the_red(root):
    phase = root / "games" / "tiny" / "toml_phases" / "5_scenes.toml"
    phase.write_text(phase.read_text() + "\n" + canvas("kitchen_variant_b"))
    cmd = "venv/bin/python manage.py package_from_toml --file games/tiny/toml_phases/7_final_game.toml --output x"
    p = run_hook(root, "PostToolUse", bash_event(root, cmd))
    assert p.returncode == 2 and "RED" in p.stderr and "`kitchen_variant_b`" in p.stderr


def test_build_py_is_skipped_because_it_checks_itself(root):
    cmd = "venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/tiny"
    p = run_hook(root, "PostToolUse", bash_event(root, cmd))
    assert p.returncode == 0 and p.stdout == "" and p.stderr == ""


def test_an_unrelated_command_does_nothing(root):
    p = run_hook(root, "PostToolUse", bash_event(root, "ls games/tiny"))
    assert p.returncode == 0 and p.stdout == "" and p.stderr == ""
