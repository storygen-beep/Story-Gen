"""NC1 (PRD v2 phase 4 · D12, 2026-09-30): the reader passed — a `--ship` BLOCK row.

Every touched canvas (B81, 2026-10-08: faceless and solo ones too) needs a `release_page.reader`
entry; a FAIL blocks unless `release_page.reader_waivers` holds {canvas_id, test, why}.
N/A is not a failure. Grandfathered games WARN (LO B).

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

ROW = gates.SHIP_READER_ROW


def game():
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "room"}], "npcs": [{"id": "npc_a", "name": "A"}],
            "canvases": [
                {"id": "hub_a", "trigger": {"location": "room", "npc": "npc_a"},
                 "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "A waits."}]}]},
                {"id": "chores", "trigger": {"location": "room"},
                 "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Dishes."}]}]}]}


def reader_row(state, g=None, root="/nonexistent", slug="fx"):
    g = g or game()
    model, g2 = gates.build(copy.deepcopy(g))
    return gates._ship_reader(root, slug, model, g2, state)


def page(reader=None, waivers=None):
    rp = {}
    if reader is not None:
        rp["reader"] = reader
    if waivers is not None:
        rp["reader_waivers"] = waivers
    return {"release_page": rp}


# ── pass ──────────────────────────────────────────────────────────────────────

def test_pass_and_na_verdicts_pass():
    ok, head, _ = reader_row(page({"hub_a": {"want": "PASS", "the body": "N/A"},
                                   "chores": {"a solo button is a real act": "PASS"}}))
    assert ok is True and head.startswith("2/2 touched canvases read"), head


def test_a_waived_fail_passes():
    ok, head, _ = reader_row(page({"hub_a": {"want": "FAIL"}, "chores": {"want": "N/A"}},
                                  [{"canvas_id": "hub_a", "test": "want", "why": "LO: fine"}]))
    assert ok is True and "1 waived" in head


def test_a_solo_canvas_needs_an_entry_too():
    # B81: the faceless bed and couch buttons are where most of first_term's false lines sat.
    _ok, _h, detail = reader_row(page({}))
    assert any(d.startswith("chores: not read (a surface)") for d in detail)


# ── fail ──────────────────────────────────────────────────────────────────────

def test_an_unread_canvas_blocks():
    ok, _h, detail = reader_row(page({}))
    assert ok is False and detail[0].startswith("hub_a: not read (a named person)")


def test_a_fail_without_a_waiver_blocks():
    ok, _h, detail = reader_row(page({"hub_a": {"want": "PASS", "next step": "FAIL"}}))
    assert ok is False and 'hub_a: FAIL on "next step" with no waiver' in detail


def test_a_waiver_without_a_reason_does_not_count():
    ok, _h, _d = reader_row(page({"hub_a": {"want": "FAIL"}},
                                 [{"canvas_id": "hub_a", "test": "want"}]))
    assert ok is False


# ── touched ───────────────────────────────────────────────────────────────────

def _git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_touched_is_a_diff_against_the_release_commit(tmp_path):
    g = game()
    g["canvases"].append({"id": "hub_b", "trigger": {"location": "room", "npc": "npc_a"},
                          "nodes": [{"id": "n", "blocks": [{"type": "paragraph",
                                                            "content": "B waits."}]}]})
    toml_dir = tmp_path / "games" / "fx" / "toml_phases"
    toml_dir.mkdir(parents=True)
    # The shipped build had hub_a and chores exactly as now, and hub_b with other text.
    (toml_dir / "7_final_game.toml").write_text(
        '[[canvases]]\nid = "chores"\n[canvases.trigger]\nlocation = "room"\n'
        '[[canvases.nodes]]\nid = "n"\nblocks = [{type = "paragraph", content = "Dishes."}]\n'
        '[[canvases]]\nid = "hub_a"\n[canvases.trigger]\nlocation = "room"\nnpc = "npc_a"\n'
        '[[canvases.nodes]]\nid = "n"\nblocks = [{type = "paragraph", content = "A waits."}]\n'
        '[[canvases]]\nid = "hub_b"\n[canvases.trigger]\nlocation = "room"\nnpc = "npc_a"\n'
        '[[canvases.nodes]]\nid = "n"\nblocks = [{type = "paragraph", content = "Old."}]\n')
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "-c", "user.email=x@x", "-c", "user.name=x", "add", ".")
    _git(tmp_path, "-c", "user.email=x@x", "-c", "user.name=x", "commit", "-qm", "ship")
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True,
                         text=True).stdout.strip()
    state = page({})
    state["releases"] = [{"version": "0.1", "shipped": "2026-10-01", "commit": sha}]
    ok, head, detail = reader_row(state, g, root=str(tmp_path))
    assert ok is False and head.startswith("0/1 touched"), head
    assert detail[0].startswith("hub_b: not read")


# ── LO B ──────────────────────────────────────────────────────────────────────

def ship(tmp_path, monkeypatch, slug, reader):
    st = ws6.green_state()
    st["release_page"]["reader"] = reader
    d = tmp_path / "games" / slug
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(st))
    monkeypatch.setattr(gates, "_load", lambda p: ws6.green_game())
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, _ = gates.ship_rows(slug, root=str(tmp_path))
    return {n: (ok, h) for n, ok, h, _d in block}[ROW]


def test_the_green_fixture_ships_with_its_reader_saved(tmp_path, monkeypatch):
    ok, _h = ship(tmp_path, monkeypatch, "brand_new",
                  {"meet_a": {"want": "PASS"}, "a_hub": {"want": "N/A"},
                   "opening": {"want": "N/A"}, "office": {"want": "N/A"}})
    assert ok is True


def test_a_new_game_blocks_and_a_grandfathered_one_warns(tmp_path, monkeypatch):
    assert ship(tmp_path, monkeypatch, "brand_new", {})[0] is False
    ok, head = ship(tmp_path, monkeypatch, "vesper_two", {})
    assert ok == "warn" and "(reader)" in head


def test_an_empty_table_or_an_unknown_verdict_is_not_read():
    for entry in ({}, {"want": "MAYBE"}, {"want": ""}):
        ok, _h, detail = reader_row(page({"hub_a": entry}))
        assert ok is False and "empty or holds something other" in detail[0], entry
