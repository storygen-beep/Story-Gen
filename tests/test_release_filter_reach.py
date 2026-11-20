"""scripts/release_filter.py, 2026-11-18 (LO: "yes go ahead with filter fix and checker"): a release slice drops a
scene that waits on a garment type she can never wear, a `substitution_only` scene nothing opens any more, a scene
or block whose clothing the room's dress code never allows at the frozen meters, and a portrait outfit she can
never wear — and the reach check stops the build on anything it still keeps that can never open.

    pytest tests/test_release_filter_reach.py -q
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import release_filter as rf  # noqa: E402


def _cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def _scene(cid, loc="home", cond=None, blocks=None, **trig):
    t = {"location": loc, "is_active": True}
    if cond:
        t["conditions"] = cond
    t.update(trig)
    return {"id": cid, "trigger": t, "nodes": [{"id": "a", "blocks": blocks or [], "exit_block": {"choices": []}}]}


EXH20 = {"type": "trait", "subject": "player", "trait_key": "exhibitionism", "operator": "gte", "value": 20}
NOBRA = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
STATE = {"release_page": {"release": 1, "meters": {"exhibitionism": {"cap": 0}}}}


def _game(*canvases, **extra):
    g = {
        "project": {"starting_canvas": "start"},
        "player": {"core_traits": {"exhibitionism": 0}},
        "npcs": [],
        "clothing": [
            {"id": "plain_bra", "slot": "bra", "type": "bra", "initial": True},
            {"id": "panties", "slot": "underwear", "type": "panties", "initial": True},
            {"id": "tshirt", "slot": "top", "type": "tshirt", "initial": True},
            {"id": "jeans", "slot": "bottom", "type": "jeans", "initial": True},
            {"id": "skirt", "slot": "bottom", "type": "short_skirt", "price": 30, "conditions": _cond(EXH20)},
        ],
        "locations": [{"id": "home"}, {"id": "street", "clothing_rules": [
            {"slots_required": ["top", "bottom"], "conditions": _cond(EXH20)},
            {"slots_required": ["bra", "underwear", "top", "bottom"]}]}],
        "canvases": [_scene("start")] + list(canvases),
    }
    g.update(extra)
    return g


def _cut(game):
    rep = rf.Report()
    rf.filter_game(game, copy.deepcopy(STATE), 1, rep)
    return {c["id"] for c in game["canvases"]}, rep


def test_a_garment_type_she_can_never_wear():
    kept, _ = _cut(_game(_scene("wind", "street", _cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}))))
    assert kept == {"start"}
    assert rf.judge_item({"type": "worn_type", "operator": "neq", "value": "short_skirt"}, rf.Frozen(),
                         {"worn_types": {"jeans"}}) is True


def test_a_scene_nothing_opens_any_more():
    door = {"door": {"options": [{"text": "Peek.", "goes_to": {"type": "canvas", "canvas_id": "peek"},
                                  "conditions": _cond(EXH20)}]}}
    g = _game(_scene("peek", substitution_only=True))
    g["locations"][0].update(door)
    kept, rep = _cut(g)
    assert kept == {"start"}            # its door waits on Exhibitionism 20, so the door goes, then the scene
    g2 = _game(_scene("peek", substitution_only=True))
    g2["canvases"][0]["trigger"]["substitutions"] = [{"target_canvas_id": "peek"}]
    assert _cut(g2)[0] == {"start", "peek"}


def test_the_dress_code_at_frozen_meters():
    run = _scene("run", "street", blocks=[
        {"type": "group", "conditions": _cond(NOBRA), "blocks": [{"type": "image", "props": {"file": "sex/run_nobra_t4"}}]},
        {"type": "image", "props": {"file": "life/run_t0"}}])
    g = _game(_scene("seen", "street", _cond(NOBRA)), _scene("mirror", "home", _cond(NOBRA)), run)
    kept, _ = _cut(g)
    assert kept == {"start", "mirror", "run"}          # home has no dress code; the street needs a bra at 0
    blocks = next(c for c in g["canvases"] if c["id"] == "run")["nodes"][0]["blocks"]
    assert [b["props"]["file"] for b in blocks] == ["life/run_t0"]


def test_portrait_outfits_she_can_never_wear():
    g = _game(player_portrait={"outfits": [{"image": "p/skirt.jpg", "when": {"wearing": "skirt"}},
                                           {"image": "p/jeans.jpg", "when": {"worn_type": "jeans"}}]})
    _cut(g)
    assert [o["image"] for o in g["player_portrait"]["outfits"]] == ["p/jeans.jpg"]


def test_the_reach_check_stops_the_build(tmp_path, capsys):
    """Two door-only scenes that open each other and nothing else: the filter keeps them (each is the other's
    door), the reach check sees neither can ever open, and the slice fails by name."""
    a = _scene("loop_a", substitution_only=True, substitutions=[{"target_canvas_id": "loop_b"}])
    b = _scene("loop_b", substitution_only=True, substitutions=[{"target_canvas_id": "loop_a"}])
    game_dir = tmp_path / "g"
    (game_dir / "toml_phases").mkdir(parents=True)
    (game_dir / "toml_phases" / "7_final_game.toml").write_text(rf.dumps(_game(a, b)))
    (game_dir / "v2_state.json").write_text(json.dumps(STATE))
    assert rf.main([str(game_dir), "--release", "1"]) == 1
    out = capsys.readouterr().out
    assert "the build stops" in out and "`loop_a`" in out and "`loop_b`" in out
    # a clean slice passes
    clean = tmp_path / "c"
    (clean / "toml_phases").mkdir(parents=True)
    (clean / "toml_phases" / "7_final_game.toml").write_text(rf.dumps(_game()))
    (clean / "v2_state.json").write_text(json.dumps(STATE))
    assert rf.main([str(clean), "--release", "1"]) == 0


def test_a_meter_nothing_kept_raises_any_more():
    """complaints rose only in a scene the dress code cut; the line that waits on a complaint goes too."""
    raiser = _scene("raiser", "street", _cond(NOBRA), blocks=[])
    raiser["nodes"][0]["exit_block"]["choices"] = [{"text": "x", "effects": [
        {"targetType": "player", "trait": "complaints", "op": "add", "value": 1}]}]
    notice = _scene("notice", blocks=[
        {"type": "group", "conditions": _cond({"type": "trait", "subject": "player", "trait_key": "complaints",
                                                "operator": "gte", "value": 1}),
         "blocks": [{"type": "paragraph", "content": "COMPLAINT"}]},
        {"type": "paragraph", "content": "Your name isn't on it."}])
    g = _game(raiser, notice)
    g["player"]["core_traits"]["complaints"] = 0
    kept, _ = _cut(g)
    assert kept == {"start", "notice"}
    blocks = next(c for c in g["canvases"] if c["id"] == "notice")["nodes"][0]["blocks"]
    assert [b.get("content") for b in blocks] == ["Your name isn't on it."]
