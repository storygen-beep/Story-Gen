"""CK7 (PRD v2 phase 4 · I2 · D9a · D9c · H25, 2026-09-30): rooms and heat.

  - a destination is never open and exit-only (a 168-hour grid, judged from where the room
    first becomes reachable; thoroughfares exempt; joins `no empty rooms` on --ship, LO B);
  - traversal heat, redefined: a place holding a sex scene, phone scenes under his home;
  - the old clip-pool count, kept as `explicit pools by place`.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

EXIT = "a destination is never open and exit-only"
V1 = {"version": "1.0", "logic": "AND"}


def cond(*items):
    return dict(V1, items=list(items))


def canvas(cid, loc, blocks=None, **trig):
    t = {"location": loc, "is_repeatable": True}
    t.update(trig)
    return {"id": cid, "trigger": t,
            "nodes": [{"id": "n", "blocks": blocks or [{"type": "paragraph", "content": "x"}]}]}


def game(locations, canvases, npcs=None, **extra):
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": locations, "npcs": npcs or [], "canvases": canvases}
    g.update(extra)
    return g


def row(g, name=EXIT):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == name)


def evening(npc, loc):
    return {"id": npc, "name": npc, "schedules": [
        {"location": loc, "weekdays": [], "start_time": "18:00", "end_time": "20:00"}]}


# ── exit-only: pass ───────────────────────────────────────────────────────────

def test_an_ungated_thing_to_do_passes():
    r = row(game([{"id": "shop"}], [canvas("browse", "shop")]))
    assert r["pass_"] is True, r


def test_a_thoroughfare_is_exempt_and_only_thoroughfares_is_na():
    r = row(game([{"id": "hall", "kind": "thoroughfare"}], []))
    assert r["na"] is True, r


def test_a_room_closed_when_he_is_away_passes():
    g = game([{"id": "bar", "hours": [{"open": "18:00", "close": "20:00"}]}],
             [canvas("hub", "bar", npc="npc_a")], [evening("npc_a", "bar")])
    assert row(g)["pass_"] is True


def test_a_locked_room_is_judged_from_where_it_opens():
    # The room needs `has_key`; its canvas needs the same flag. Not exit-only for 168 h.
    g = game([{"id": "attic", "entry_conditions": cond(
        {"type": "flag", "subject": "player", "flag_key": "has_key", "operator": "is_true"})}],
        [canvas("rummage", "attic", conditions=cond(
            {"type": "flag", "subject": "player", "flag_key": "has_key", "operator": "is_true"}))])
    assert row(g)["pass_"] is True


def test_searching_his_room_while_he_is_out_counts():
    g = game([{"id": "his_room"}],
             [canvas("hub", "his_room", npc="npc_a"),
              canvas("search", "his_room", conditions=cond(
                  {"type": "npc_at_location", "npc_id": "npc_a", "location_id": "his_room",
                   "operator": "is_absent"}))],
             [evening("npc_a", "his_room")])
    assert row(g)["pass_"] is True


# ── exit-only: fail ───────────────────────────────────────────────────────────

def test_a_room_with_only_his_portrait_is_exit_only_when_he_is_away():
    g = game([{"id": "bar"}], [canvas("hub", "bar", npc="npc_a")], [evening("npc_a", "bar")])
    r = row(g)
    assert r["pass_"] is False
    assert r["detail"][0].startswith("bar: open with nothing to do (154 h) — Mon 00-18, 20-24")


def test_content_behind_a_later_flag_leaves_the_room_empty_until_then():
    g = game([{"id": "shop"}], [canvas("work", "shop", conditions=cond(
        {"type": "flag", "subject": "player", "flag_key": "has_job", "operator": "is_true"}))])
    g["canvases"].append({"id": "hire", "trigger": {"location": "elsewhere"}, "nodes": [
        {"id": "n", "blocks": [], "exit_block": {"config": {
            "flagEffects": [{"flag": "has_job", "op": "set"}]}}}]})
    r = row(g)
    assert r["pass_"] is False and "(168 h)" in r["detail"][0]


def test_a_random_event_is_not_something_to_do():
    r = row(game([{"id": "path"}], [canvas("wind", "path", trigger_mode="random")]))
    assert r["pass_"] is False


# ── heat ──────────────────────────────────────────────────────────────────────

HOT = "He fucks her against the wall, his cock deep in her cunt, her tits in his hands."


def test_heat_counts_an_explicit_beat_and_drops_thoroughfares():
    beds = [f"bed{i}" for i in range(5)]
    g = game([{"id": b} for b in beds] + [{"id": "hall", "kind": "thoroughfare"}],
             [canvas(f"sex{b}", b, [{"type": "paragraph", "content": HOT}]) for b in beds])
    r = row(g, "traversal heat")
    assert r["pass_"] is True and r["headline"].startswith("5/5 destinations"), r


def test_a_phone_scene_counts_under_his_home():
    g = game([{"id": "his_flat"}, {"id": "cafe"}],
             [{"id": "sext", "trigger": {"is_repeatable": True, "npc": "npc_a"},
               "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": HOT}]}]}],
             [evening("npc_a", "his_flat")])
    r = row(g, "traversal heat")
    assert "1/2 destinations" in r["headline"] and "cafe" in r["detail"][0]


def test_the_old_pool_count_is_its_own_row():
    g = game([{"id": "bed"}], [canvas("sex", "bed", [{"type": "paragraph", "content": HOT}])])
    assert row(g, "explicit pools by place")["pass_"] is False


# ── LO B on --ship ────────────────────────────────────────────────────────────

def ship_game():
    g = ws6.green_game()
    g["locations"].append({"id": "empty_room"})
    return g


def ship(tmp_path, monkeypatch, slug, state=None):
    import json
    d = tmp_path / "games" / slug
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(state or ws6.green_state()))
    monkeypatch.setattr(gates, "_load", lambda p: ship_game())
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, _ = gates.ship_rows(slug, root=str(tmp_path))
    return {n: (ok, h, det) for n, ok, h, det in block}["no empty rooms"]


def test_the_empty_room_blocks_a_new_game(tmp_path, monkeypatch):
    ok, head, detail = ship(tmp_path, monkeypatch, "brand_new")
    assert ok is False and EXIT in head
    assert any(d.startswith("empty_room: open with nothing to do") for d in detail)


def test_a_grandfathered_game_warns(tmp_path, monkeypatch):
    ok, head, _ = ship(tmp_path, monkeypatch, "probation")
    assert ok == "warn" and "exit_only" in head and "blocks from your next release" in head


# ── follow-ups: an unread condition shape is not live, and is listed ─────────

def test_a_clothing_gated_canvas_is_not_live_and_is_listed_not_judged():
    g = game([{"id": "shop"}], [canvas("try_on", "shop", conditions=cond(
        {"type": "clothing_slot", "slot": "top", "operator": "equipped"}))])
    r = row(g)
    assert r["pass_"] is False and "(168 h)" in r["detail"][0]
    assert any(d.startswith("not judged at shop: try_on (clothing_slot)") for d in r["detail"])
