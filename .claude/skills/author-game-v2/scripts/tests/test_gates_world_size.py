"""`world size` (World and Systems PRD, Phase 6B, 2026-10-02): a REPORT row under `--ship` and a
`lint · world size` print. No threshold. Hook people are `want.cast` ids that are no thread's
person; the hub is the first `board.map.roots[]`. Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402


def world():
    g = ws6.green_game()
    g["npcs"].append({"id": "npc_b", "name": "B"})
    g["canvases"][2]["trigger"]["conditions"] = ws6.cond(
        {"type": "flag", "flag_key": "met_a", "operator": "is_true"})      # A's hub reads met_a
    # A thread canvas (B) that sets a flag the hook canvas (A's hub) reads.
    g["canvases"].append({"id": "b_job", "trigger": {"location": "work", "npc": "npc_b"},
                          "nodes": [{"id": "n", "blocks": [
                              {"type": "dialog", "content": "Shift starts now, okay?",
                               "props": {"speaker": "npc", "npcId": "npc_b"}}],
                              "exit_block": {"config": {"flagEffects": [{"flag": "met_a"}]}}}]})
    st = ws6.green_state()
    st["want"] = {"cast": [{"id": "npc_a", "age": 30}, {"id": "npc_b", "age": 25}],
                  "threads": [{"id": "job", "person": "npc_b"}, {"id": "gym", "person": "npc_z"}]}
    st["board"]["map"] = {"roots": ["room_a"]}
    st["board"]["locations"] = [{"id": "room_a", "labels": ["zone:home"]},
                                {"id": "work", "labels": ["zone:town", "public"]}]
    return g, st


def test_the_world_is_measured():
    g, st = world()
    model, g2 = gates.build(g)
    summary, rows = gates._world_size(model, st)
    assert "1 hook people, hub `room_a`" in summary
    assert "threads 2 declared, 1 built" in summary and "2 speaking NPCs" in summary
    assert "1 links" in summary and "2 zones" in summary
    assert rows[0] == "threads not built yet: gym" and rows[1] == "links: b_job"


def test_no_ledger_still_reports_a_size():
    model, _ = gates.build(ws6.green_game())
    assert "threads 0 declared" in gates._world_size(model, None)[0]


def test_it_is_a_ship_report_row_never_a_block(tmp_path, monkeypatch):
    import copy, json
    g, st = world()
    d = tmp_path / "games" / "fx"
    (d / "toml_phases").mkdir(parents=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(st))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(g))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, report = gates.ship_rows("fx", root=str(tmp_path))
    row = next(r for r in report if r[0] == "world size")
    assert row[1] is None and "a size, never a score" in row[2]
    assert "world size" not in {r[0] for r in block}
