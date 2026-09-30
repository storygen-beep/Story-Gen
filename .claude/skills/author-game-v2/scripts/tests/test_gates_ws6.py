"""The ship check (PRD WS6, 2026-09-26): which rows block, which only report, and the
pre-commit hook that holds a publish. Minimal fixtures built here; nothing in games/ is
read or written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import copy
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def green_game():
    """A small v0.1 that passes every BLOCK row. The ladder row is stubbed green in `rows()`;
    its real behaviour is tested in test_gates_ws4.py (PRD WS4)."""
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "opening",
                    "quests_engine": "v2"},
        "player": {"core_traits": {"money": 10}},
        "locations": [{"id": "room_a"}, {"id": "work"}],
        # Five rows, not one: a share on fewer than 5 cases is "too few to judge" and a
        # too-few BLOCK row is red (PRD IC21), so a green fixture needs a real sample.
        "npcs": [{"id": "npc_a", "name": "A",
                  "schedules": [{"location": "room_a", "weekdays": days,
                                 "start_time": "18:00", "end_time": "20:00"}
                                for days in ([0], [1], [2], [3], [4, 5, 6])]}],
        "canvases": [
            {"id": "opening", "trigger": {"location": "room_a", "is_repeatable": False},
             "nodes": [{"id": "n", "blocks": [], "exit_block": {"config": {
                 "flagEffects": [{"flag": "opening_done", "op": "set"}]}}}]},
            {"id": "meet_a", "trigger": {"location": "room_a", "npc": "npc_a",
                                          "is_repeatable": False},
             "nodes": [{"id": "n", "blocks": [
                 {"type": "dialog", "content": "You made it.",
                  "props": {"speaker": "npc", "npcId": "npc_a"}}],
                 "exit_block": {"config": {"flagEffects": [{"flag": "met_a", "op": "set"}]}}}]},
            {"id": "a_hub", "trigger": {"location": "room_a", "npc": "npc_a",
                                         "is_repeatable": True},
             "nodes": [{"id": "n", "blocks": [
                 {"type": "paragraph", "content": "She is at the table with her book."}]}]},
            {"id": "office", "trigger": {"location": "work", "is_repeatable": True},
             "nodes": [{"id": "n", "blocks": [], "exit_block": {"choices": [
                 {"text": "Take the closing shift", "show_when_locked": True,
                  "conditions": cond({"type": "flag", "flag_key": "met_a",
                                      "operator": "is_true"})}]}}]},
        ],
        "quest_cards": [{"id": "card", "text": "Find A.", "goals": [
            {"flag": "met_a", "label": "Meet A"}],
            "when": [{"flag": "opening_done", "op": "is_true"}]}],
    }


def green_state():
    return {"board": {"door": {"canvas": "office", "choice": "Take the closing shift"}},
            "release_page": {"version": "0.1", "people": ["npc_a"],
                             "door": {"canvas": "office", "choice": "Take the closing shift"},
                             "signed_by_lo": True, "signed_at": "2026-09-26"}}


def rows(tmp_path, monkeypatch, game=None, state=None, release_rc=0, saves_rc=2,
         ladder=(True, "stub: the ladder row is tested in test_gates_ws4.py", [])):
    game = game if game is not None else green_game()
    state = state if state is not None else green_state()
    d = tmp_path / "games" / "fx"
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(state))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(game))
    monkeypatch.setattr(gates, "release_mode", lambda slug: (print("[FAIL] x") or release_rc))
    monkeypatch.setattr(gates, "saves_mode", lambda slug: saves_rc)
    if ladder is not None:
        monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: ladder)
    block, report = gates.ship_rows("fx", root=str(tmp_path))
    return {n: ok for n, ok, h, d in block}, block, report


def test_green_fixture_ships(tmp_path, monkeypatch):
    b, block, report = rows(tmp_path, monkeypatch)
    red = [n for n, ok in b.items() if ok is False]
    assert red == [], red
    assert b["last release's saves still load"] is None       # first release: n/a


def flips(tmp_path, monkeypatch, row, game=None, state=None, **kw):
    b, *_ = rows(tmp_path, monkeypatch, game, state, **kw)
    assert b[row] is False, (row, b)


def test_past_claim_blocks(tmp_path, monkeypatch):
    # A past-tense clause about her (CK4): a bare marker no longer blocks on its own.
    g = green_game()
    g["canvases"][2]["nodes"][0]["blocks"][0]["content"] = "You came to the table last night."
    flips(tmp_path, monkeypatch, "no past claim on a repeatable", game=g)


def test_printed_stat_blocks(tmp_path, monkeypatch):
    g = green_game()
    g["canvases"][2]["nodes"][0]["blocks"][0]["content"] = "She smiles. (+5 Trust)"
    flips(tmp_path, monkeypatch, "no printed stat labels", game=g)


def test_mute_one_time_step_blocks(tmp_path, monkeypatch):
    g = green_game()
    g["canvases"][1]["nodes"][0]["blocks"] = [{"type": "paragraph", "content": "She nods."}]
    flips(tmp_path, monkeypatch, "a one-time step with a person speaks", game=g)


def test_no_goal_card_blocks(tmp_path, monkeypatch):
    g = green_game()
    del g["quest_cards"][0]["goals"]
    flips(tmp_path, monkeypatch, "the opening's card has goals", game=g)


def test_unsigned_blocks(tmp_path, monkeypatch):
    st = green_state()
    st["release_page"]["signed_by_lo"] = False
    flips(tmp_path, monkeypatch, "LO signed the playtest", state=st)


def test_bad_build_blocks(tmp_path, monkeypatch):
    flips(tmp_path, monkeypatch, "the build exists and is a release build", release_rc=1)


def test_broken_saves_block(tmp_path, monkeypatch):
    flips(tmp_path, monkeypatch, "last release's saves still load", saves_rc=1)


def test_undeclared_door_blocks(tmp_path, monkeypatch):
    # Undeclared means neither copy: since CK2 the release page's door alone counts.
    st = green_state()
    del st["board"]["door"]
    del st["release_page"]["door"]
    flips(tmp_path, monkeypatch, "the declared door works", state=st)


def test_unpayable_pressure_blocks(tmp_path, monkeypatch):
    g = green_game()
    g["canvases"].append({"id": "friday", "trigger": {"location": "work", "is_repeatable": True,
                                                       "max_triggers_per_day": 1},
                          "nodes": [{"id": "n", "blocks": [], "exit_block": {"config": {
                              "effects": [{"trait": "money", "op": "add", "value": -150}]}}}]})
    st = green_state()
    st["board"]["economy"] = {"currency": "money", "obligation": "rent",
                              "obligation_amount": 150}
    flips(tmp_path, monkeypatch, "the pressure can be paid or is signposted", game=g, state=st)


def test_dead_row_blocks(tmp_path, monkeypatch):
    g = green_game()
    g["canvases"][2]["trigger"]["location"] = "work"
    flips(tmp_path, monkeypatch, "no empty rooms", game=g)


def test_page_naming_a_missing_person_blocks(tmp_path, monkeypatch):
    st = green_state()
    st["release_page"]["people"] = ["npc_a", "npc_nobody"]
    flips(tmp_path, monkeypatch, "the build matches the release page", state=st)


def test_no_release_page_blocks(tmp_path, monkeypatch):
    st = green_state()
    del st["release_page"]
    flips(tmp_path, monkeypatch, "the build matches the release page", state=st)


def test_report_rows_never_change_the_verdict(tmp_path, monkeypatch):
    g = green_game()
    # all narration, no dialogue anywhere repeatable: `somebody speaks` goes red
    g["canvases"][2]["nodes"][0]["blocks"][0]["content"] = " ".join(["She reads."] * 80)
    b, block, report = rows(tmp_path, monkeypatch, game=g)
    assert [n for n, ok in b.items() if ok is False] == []
    assert any(n == "somebody speaks" for n, *_ in report)


# ── the hook's target list ───────────────────────────────────────────────────
PORTAL = """window.GAMES = [
  {
    slug: "live",
    version: "0.1",
  },
  {
    slug: "testbuild",
    dev: true,
  },
  {
    slug: "oldgame",
    version: "0.2.2",
  },
];
"""


def hook_root(tmp_path):
    (tmp_path / "games-data.js").write_text(PORTAL)
    for s, v2 in (("live", True), ("testbuild", True), ("oldgame", False)):
        (tmp_path / "games" / s).mkdir(parents=True)
        if v2:
            (tmp_path / "games" / s / "v2_state.json").write_text("{}")
    return str(tmp_path)


def test_targets_skip_dev_and_v1(tmp_path):
    root = hook_root(tmp_path)
    paths = ["games/live/output/index.html", "games/testbuild/output/index.html",
             "games/oldgame/output/index.html"]
    assert gates.ship_targets(paths, root=root) == ["live"]


def test_targets_portal_change_checks_every_published_v2_game(tmp_path):
    root = hook_root(tmp_path)
    assert gates.ship_targets(["games-data.js"], root=root) == ["live"]


def test_targets_read_the_staged_portal_file(tmp_path):
    root = hook_root(tmp_path)
    staged = tmp_path / "staged.js"
    staged.write_text(PORTAL.replace("slug: \"testbuild\",\n    dev: true,",
                                     "slug: \"testbuild\",\n    version: \"0.1\","))
    assert gates.ship_targets(["games-data.js"], root=root, portal=str(staged)) == \
        ["live", "testbuild"]


# ── the hook itself, in a throwaway git repo ────────────────────────────────
def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def _hook_repo(tmp_path, dev):
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")
    skill = r / ".claude" / "skills" / "author-game-v2" / "scripts"
    skill.mkdir(parents=True)
    # a stand-in gates.py: real --ship-targets, and a --ship that always fails
    (skill / "gates.py").write_text(
        "import sys, os\n"
        f"sys.path.insert(0, {os.path.dirname(HERE)!r})\n"
        "import gates as real\n"
        "if sys.argv[1] == '--ship-targets':\n"
        "    a = sys.argv[2:]; p = None\n"
        "    if a[:1] == ['--portal']: p, a = a[1], a[2:]\n"
        "    print('\\n'.join(real.ship_targets(a, portal=p))); sys.exit(0)\n"
        "print('ship check: FAIL (stand-in)'); sys.exit(1)\n")
    (r / "games" / "fx" / "output").mkdir(parents=True)
    (r / "games" / "fx" / "v2_state.json").write_text("{}")
    (r / "games-data.js").write_text(
        "window.GAMES = [\n  {\n    slug: \"fx\",\n" + ("    dev: true,\n" if dev else
                                                        "    version: \"0.1\",\n") + "  },\n];\n")
    (r / "games" / "fx" / "output" / "index.html").write_text("<html></html>")
    hooks = r / ".git" / "hooks"
    shutil.copy(os.path.join(REPO, "scripts", "hooks", "pre-commit"), hooks / "pre-commit")
    os.chmod(hooks / "pre-commit", 0o755)
    _git(r, "add", "-A")
    return r


def test_hook_blocks_a_published_v2_build(tmp_path):
    r = _hook_repo(tmp_path, dev=False)
    res = _git(r, "commit", "-q", "-m", "publish")
    assert res.returncode != 0 and "ship check failed" in (res.stdout + res.stderr)


def test_hook_lets_a_dev_build_through(tmp_path):
    r = _hook_repo(tmp_path, dev=True)
    assert _git(r, "commit", "-q", "-m", "test build").returncode == 0


# ── release_upload.py refuses at the ship step ───────────────────────────────
def test_release_upload_check_ship(tmp_path, monkeypatch):
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import release_upload as ru
    monkeypatch.setattr(ru, "REPO_ROOT", tmp_path)
    (tmp_path / "games" / "v2game").mkdir(parents=True)
    (tmp_path / "games" / "v2game" / "v2_state.json").write_text("{}")
    (tmp_path / "games" / "v1game").mkdir(parents=True)
    calls = []

    class R:
        def __init__(self, rc):
            self.returncode = rc

    monkeypatch.setattr(ru.subprocess, "run", lambda cmd, cwd=None: calls.append(cmd) or R(1))
    import pytest
    with pytest.raises(ru.ReleaseError):
        ru.check_ship("v2game")
    assert "--ship" in calls[0]
    ru.check_ship("v1game")                 # not a v2 game: skipped, no call
    assert len(calls) == 1
