"""Gate `every kept scene can be reached` and scripts/reach.py (LO, 2026-11-18): a scene no door opens, one that
waits on a garment type she can never wear, one whose clothing no wearable outfit meets inside the room's dress
code, a media spot only such scenes or groups carry, and a portrait outfit she can never wear. Minimal game
dicts; nothing in games/ is read."""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import reach  # noqa: E402


def _cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def _slot(slot, on):
    return {"type": "clothing_slot", "slot": slot, "operator": "equipped" if on else "unequipped"}


def _scene(cid, loc="home", cond=None, nodes=None, **trig):
    t = {"location": loc, "is_active": True}
    if cond:
        t["conditions"] = cond
    t.update(trig)
    return {"id": cid, "trigger": t, "nodes": nodes or [{"id": "a", "blocks": [], "exit_block": {"choices": []}}]}


def _pic(name, cond=None):
    b = {"type": "image", "props": {"file": name}}
    return {"type": "group", "conditions": cond, "blocks": [b]} if cond else b


def _game(*canvases, raise_exh=False, **extra):
    wear = lambda i, slot, typ, **kw: dict(id=i, slot=slot, type=typ, **kw)  # noqa: E731
    street_rules = [  # the last rule always applies: at Exhibitionism 0 she goes out fully dressed
        {"slots_required": ["top", "bottom"], "conditions": _cond(
            {"type": "trait", "subject": "player", "trait_key": "exhibitionism", "operator": "gte", "value": 20})},
        {"slots_required": ["bra", "underwear", "top", "bottom"]}]
    g = {
        "project": {"starting_canvas": canvases[0]["id"] if canvases else None},
        "player": {"core_traits": {"exhibitionism": 0}},
        "npcs": [],
        "clothing": [wear("plain_bra", "bra", "bra", initial=True), wear("panties", "underwear", "panties", initial=True),
                     wear("tshirt", "top", "tshirt", initial=True), wear("jeans", "bottom", "jeans", initial=True),
                     wear("skirt", "bottom", "short_skirt", price=30, conditions=_cond(
                         {"type": "trait", "subject": "player", "trait_key": "exhibitionism", "operator": "gte",
                          "value": 20}))],
        "locations": [{"id": "home"}, {"id": "street", "clothing_rules": street_rules}],
        "canvases": list(canvases),
    }
    if raise_exh:
        g["canvases"].append(_scene("trainer", nodes=[{"id": "a", "exit_block": {"choices": [
            {"text": "x", "effects": [{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1}]}]}}]))
    g.update(extra)
    return g


def test_a_garment_type_she_can_never_wear_shuts_the_scene():
    g = _game(_scene("start"), _scene("wind", "street", _cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"})))
    r = reach.check(g)
    assert list(r["scenes"]) == ["wind"] and "short_skirt" in r["scenes"]["wind"][0]
    # once something can raise Exhibitionism, the skirt can be bought and worn, and the street lets her out in it
    assert reach.check(_game(*copy.deepcopy(g["canvases"]), raise_exh=True))["scenes"] == {}


def test_a_scene_nothing_opens():
    lone = _scene("peek", substitution_only=True)
    assert "nothing opens it" in reach.check(_game(_scene("start"), lone))["scenes"]["peek"][0]
    # a substitution from a live scene, a door option, or a phone call's accept is a door
    sub = _scene("start", substitutions=[{"target_canvas_id": "peek"}])
    assert reach.check(_game(sub, copy.deepcopy(lone)))["scenes"] == {}
    door = _game(_scene("start"), copy.deepcopy(lone))
    door["locations"][0]["door"] = {"options": [{"text": "Peek.", "goes_to": {"type": "canvas", "canvas_id": "peek"}}]}
    assert reach.check(door)["scenes"] == {}
    call = _game(_scene("start"), copy.deepcopy(lone), phone={"calls": [{"id": "c", "accept": "peek"}]})
    assert reach.check(call)["scenes"] == {}


def test_a_dress_code_that_never_lets_her_stand_there_dressed_that_way():
    nobra = _cond(_slot("bra", False))
    g = _game(_scene("start"), _scene("seen", "street", nobra), _scene("mirror", "home", copy.deepcopy(nobra)))
    r = reach.check(g)
    assert list(r["scenes"]) == ["seen"] and "dress code" in r["scenes"]["seen"][0]   # home has no code
    # an Exhibitionism rise opens the first rule (top and bottom only), so no bra on the street can happen
    assert reach.check(_game(*copy.deepcopy(g["canvases"][:3]), raise_exh=True))["scenes"] == {}


def test_media_is_dead_only_when_every_placement_is():
    run = _scene("run", "street", nodes=[{"id": "a", "blocks": [
        _pic("look/run_nobra_t4", _cond(_slot("bra", False))), _pic("look/run_t0")], "exit_block": {"choices": []}}])
    r = reach.check(_game(_scene("start"), run))
    assert list(r["spots"]) == ["look/run_nobra_t4"] and r["scenes"] == {}
    # the same picture also shown somewhere she can be keeps it
    elsewhere = _scene("start", nodes=[{"id": "a", "blocks": [_pic("look/run_nobra_t4")], "exit_block": {"choices": []}}])
    assert reach.check(_game(elsewhere, copy.deepcopy(run)))["spots"] == {}


def test_a_portrait_outfit_she_can_never_wear():
    g = _game(_scene("start"), player_portrait={"outfits": [
        {"image": "portraits/her_skirt.jpg", "when": {"wearing": "skirt"}},
        {"image": "portraits/her_jeans.jpg", "when": {"worn_type": "jeans"}}]})
    assert list(reach.check(g)["portraits"]) == ["portraits/her_skirt.jpg"]


def test_the_gate():
    ok, head, rows = gates._every_kept_scene_reached(_game(_scene("start"), _scene("peek", substitution_only=True)))
    assert ok is False and "1 kept scene(s) can never open" in head and "`peek`" in rows[0]
    ok, head, rows = gates._every_kept_scene_reached(_game(_scene("start")))
    assert ok is True and rows == []
    assert gates._every_kept_scene_reached({"canvases": []})[0] is None
