"""`world size` (World and Systems PRD, Phase 6B, 2026-10-02): a REPORT row under `--ship` and a
`lint · world size` print. No threshold. Hook people are `want.cast` ids that are no thread's
person; the hub is the top of the house her room (`board.map.home_base`) is in, below the
street (leftovers L1, 2026-10-02); with no home base, the first `board.map.roots[]`. Fixtures only.
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


def _locs(*pairs):
    return {"locations": [{"id": i, "entry_from": p} if p else {"id": i} for i, p in pairs]}


def test_the_hub_is_the_house_not_the_street_two_roots():
    # billable_hours' shape: street -> Home -> Upstairs -> her room, and a second root downtown.
    game = _locs(("linden_street", None), ("house", "linden_street"), ("landing", "house"),
                 ("her_room", "landing"), ("downtown", None), ("firm", "downtown"))
    board = {"map": {"roots": ["linden_street", "downtown"], "exterior": "linden_street",
                     "home_base": "her_room"}}
    assert gates._world_hub(board, game) == "house"


def test_the_hub_single_root():
    game = _locs(("street", None), ("flat", "street"), ("her_room", "flat"))
    board = {"map": {"roots": ["street"], "exterior": "street", "home_base": "her_room"}}
    assert gates._world_hub(board, game) == "flat"
    # The house is the root itself (the street is not on her room's chain): the root.
    game = _locs(("house", None), ("her_room", "house"), ("street", None))
    board = {"map": {"roots": ["house", "street"], "exterior": "street", "home_base": "her_room"}}
    assert gates._world_hub(board, game) == "house"


def test_the_hub_is_the_house_itself_when_its_parent_is_outdoors():
    # members_only's shape: town -> cliff path (outdoors) -> the staff house, which is her home.
    game = _locs(("town", None), ("cliff_path", "town"), ("staff_house", "cliff_path"),
                 ("club", "cliff_path"))
    board = {"map": {"exterior": "town", "home_base": "staff_house"},
             "locations": [{"id": "town", "labels": ["outdoors"]},
                           {"id": "cliff_path", "labels": ["public", "outdoors"]},
                           {"id": "staff_house", "labels": ["private", "home_base"]}]}
    assert gates._world_hub(board, game) == "staff_house"
    # The same chain with an indoor stairwell (probation's shape) still climbs to it.
    board["locations"][1]["labels"] = ["public"]
    assert gates._world_hub(board, game) == "cliff_path"


def test_the_hub_without_a_home_base_is_the_first_root():
    assert gates._world_hub({"map": {"roots": ["room_a"]}}, _locs(("room_a", None))) == "room_a"
    assert gates._world_hub({}, None) is None


def test_world_size_counts_the_house_words():
    g, st = world()
    model, g2 = gates.build(g)
    st["board"]["map"] = {"roots": ["street"], "exterior": "street", "home_base": "room_a"}
    game = _locs(("street", None), ("room_a", "street"))
    assert "hub `room_a`" in gates._world_size(model, st, game)[0]
