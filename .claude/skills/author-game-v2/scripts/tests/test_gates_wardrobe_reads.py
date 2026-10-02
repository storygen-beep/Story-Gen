"""`every clothing state is read three times` (World and Systems PRD, Phase 6B, 2026-10-02).

A `--ship` BLOCK row: every state and key item declared in board.wardrobe is read in at least
three places. A reader is a condition on a canvas trigger, in a `group`, in a location's
`entry_conditions` or a dress code's `conditions`, or a dress code's `slots_required`. It
matches a state on the same predicate (and slot) with overlapping values. n/a (clothing off)
passes; clothing on with nothing declared is red. LO B as the other rows. Fixtures only.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

ROW = "every clothing state is read three times"


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def exp(op, v):
    return {"type": "worn_exposure", "operator": op, "value": v}


def item(i, op="equipped"):
    return {"type": "clothing_item", "item_id": i, "operator": op}


def dressed_game(readers=(), dress_code=None, clothing=True):
    """green_game with a catalog; each reader lands in a different kind of place."""
    g = ws6.green_game()
    g["settings"] = {"clothing_enabled": clothing}
    g["clothing"] = [{"id": "skirt", "slot": "bottom", "type": "skirt", "initial": True},
                     {"id": "blouse", "slot": "top", "initial": True}]
    for n, r in enumerate(readers):
        where = n % 3
        if where == 0:
            g["canvases"].append({"id": f"t{n}", "trigger": {"location": "work",
                                                            "conditions": cond(r)},
                                  "nodes": [{"id": "n", "blocks": []}]})
        elif where == 1:
            g["canvases"][2]["nodes"][0]["blocks"].append(
                {"type": "group", "props": {"conditions": cond(r), "blocks": []}})
        else:
            g["locations"].append({"id": f"room{n}", "entry_from": "work",
                                   "entry_conditions": cond(r)})
    if dress_code:
        g["locations"][1]["clothing_rules"] = [dress_code]
    return g


def wardrobe(states=(), items=()):
    st = ws6.green_state()
    st["board"]["wardrobe"] = {"states": [{"id": f"s{n}", "condition": c}
                                          for n, c in enumerate(states)],
                               "key_items": list(items)}
    return st


def run(game, st):
    return gates._wardrobe_is_read(game, st)


def test_a_state_read_three_times_passes():
    g = dressed_game([exp("gte", 1), exp("gte", 2), exp("eq", 2)])
    ok, head, detail = run(g, wardrobe([exp("gte", 1)]))
    assert ok is True and "1/1" in head, detail


def test_a_reader_whose_values_do_not_overlap_does_not_count():
    g = dressed_game([exp("gte", 1), exp("gte", 2), exp("lt", 1)])
    ok, _, detail = run(g, wardrobe([exp("gte", 1)]))
    assert ok is False and "read 2 time(s)" in detail[0], detail


def test_a_dress_code_reads_the_slots_it_names():
    no_top = {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}
    g = dressed_game([no_top, no_top], dress_code={"slots_required": ["top", "bottom"],
                                                   "message": "Dress code."})
    assert run(g, wardrobe([no_top]))[0] is True
    no_shoes = dict(no_top, slot="shoes")
    assert "read 0 time(s)" in run(g, wardrobe([no_shoes]))[2][0]


def test_worn_type_eq_and_neq():
    skirt = {"type": "worn_type", "operator": "eq", "value": "skirt"}
    not_jeans = {"type": "worn_type", "operator": "neq", "value": "jeans"}
    not_skirt = {"type": "worn_type", "operator": "neq", "value": "skirt"}
    g = dressed_game([skirt, not_jeans, not_skirt])
    _, _, detail = run(g, wardrobe([skirt]))
    assert "read 2 time(s)" in detail[0], detail


def test_a_key_item_counts_clothing_item_readers_only_not_choices():
    g = dressed_game([item("skirt"), item("skirt", "owned"), item("skirt")])
    assert run(g, wardrobe(items=["skirt"]))[0] is True
    g = dressed_game([item("skirt"), item("skirt")])
    g["canvases"][3]["nodes"][0]["exit_block"]["choices"][0]["conditions"] = cond(item("skirt"))
    ok, _, detail = run(g, wardrobe(items=["skirt"]))
    assert ok is False and "read 2 time(s)" in detail[0], detail


def test_a_key_item_not_in_the_catalog_is_red():
    ok, _, detail = run(dressed_game(), wardrobe(items=["gown"]))
    assert ok is False and "not a [[clothing]] id" in detail[0]


def test_a_state_that_is_not_a_clothing_predicate_is_red():
    ok, _, detail = run(dressed_game(), wardrobe([{"type": "trait", "trait_key": "nerve"}]))
    assert ok is False and "is not a clothing state" in detail[0]


def test_clothing_off_is_na():
    assert run(dressed_game(clothing=False), wardrobe())[0] is None


def test_clothing_on_with_nothing_declared_is_red():
    ok, head, _ = run(dressed_game(), ws6.green_state())
    assert ok is False and "declares no state or key item" in head


def test_the_legacy_form_passes():
    gates._LEGACY_RULES.add("wardrobe_reads")
    try:
        assert run(dressed_game(), ws6.green_state())[0] is True
    finally:
        gates._LEGACY_RULES.discard("wardrobe_reads")


# ── on `ship_rows` ────────────────────────────────────────────────────────────

def ship(tmp_path, monkeypatch, slug, game, state):
    d = tmp_path / "games" / slug
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(state))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(game))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, _ = gates.ship_rows(slug, root=str(tmp_path))
    return {n: ok for n, ok, h, _d in block}


def test_clothing_off_passes_the_ship_row_as_na(tmp_path, monkeypatch):
    b = ship(tmp_path, monkeypatch, "new_game", dressed_game(clothing=False), ws6.green_state())
    assert b[ROW] is None


def test_red_blocks_billable_and_warns_a_grandfathered_game(tmp_path, monkeypatch):
    g, st = dressed_game(), wardrobe([exp("gte", 1)])
    assert ship(tmp_path, monkeypatch, "billable_hours", g, st)[ROW] is False
    assert ship(tmp_path, monkeypatch, "the_balance", g, st)[ROW] == "warn"
    st["releases"] = [{"version": "0.3", "shipped": "2026-10-02"}]
    assert ship(tmp_path, monkeypatch, "the_balance", g, st)[ROW] is False
    assert gates._LEGACY_RULES == set()
