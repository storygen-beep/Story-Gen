"""PRD v2 DC9e · H16: before the build, `gates.py <slug>` points at shape.py instead of a bare
"not found". Run in a temp dir; nothing in games/ is read or written."""
import json
import os
import subprocess
import sys

GATES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gates.py")


def run(cwd, slug):
    return subprocess.run([sys.executable, GATES, slug], cwd=cwd, capture_output=True, text=True)


def test_a_ledger_without_toml_points_at_shape(tmp_path):
    (tmp_path / "games" / "fx").mkdir(parents=True)
    (tmp_path / "games" / "fx" / "v2_state.json").write_text(json.dumps({"phase": "board"}))
    r = run(tmp_path, "fx")
    assert r.returncode == 2 and "no TOML yet: use shape.py fx" in r.stdout


def test_nothing_at_all_is_still_not_found(tmp_path):
    r = run(tmp_path, "nope")
    assert r.returncode == 2 and "not found:" in r.stdout
