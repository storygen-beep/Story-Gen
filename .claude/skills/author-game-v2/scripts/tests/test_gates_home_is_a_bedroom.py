"""Gate 12 `residents have homes`: a home is a bedroom (the-map.md R2).

Red when a home is a thoroughfare, a container or a hub (another location's `entry_from` points
at it), or when two people share it undeclared in `board.map.shared_homes`. A game in
SHIP_GRANDFATHERED gets the new reasons as warnings (the gate still passes) until it ships on or
after HOME_IS_A_BEDROOM_SINCE; billable_hours is not grandfathered. n/a policy unchanged: no
ledger, or no characters.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def house():
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [
                {"id": "street"},
                {"id": "hall", "entry_from": "street", "kind": "thoroughfare"},
                {"id": "kitchen", "entry_from": "hall"},
                {"id": "upstairs", "entry_from": "hall", "kind": "thoroughfare"},
                {"id": "his_room", "entry_from": "upstairs"},
                {"id": "parents_room", "entry_from": "upstairs"},
                {"id": "wardrobe", "entry_from": "parents_room", "is_container": True},
            ],
            "canvases": [{"id": "c", "trigger": {"location": "kitchen"},
                          "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}]}


def ledger(homes, shared=None, slug="billable_hours", releases=None):
    m = {"archetype": "nested_zones", "homes": homes}
    if shared is not None:
        m["shared_homes"] = shared
    st = {"slug": slug, "board": {"map": m, "characters": [{"id": i} for i in homes]}}
    if releases:
        st["releases"] = releases
    return st


def row(state, game=None):
    model, g2 = gates.build(copy.deepcopy(game or house()))
    return next(r for r in gates.run_gates(model, g2, state) if r["gate"] == "residents have homes")


COUPLE = {"npc_son": "his_room", "npc_mum": "parents_room", "npc_dad": "parents_room"}


def test_one_bedroom_each_and_a_declared_couple_pass():
    r = row(ledger(COUPLE, shared=[["npc_mum", "npc_dad"]]))
    assert r["pass_"] is True and r["detail"] == [], r


def test_an_undeclared_share_fails_both_people():
    r = row(ledger(COUPLE))
    assert r["pass_"] is False
    assert sum("shares 'parents_room'" in d for d in r["detail"]) == 2
    assert r["headline"].startswith("1/3"), r["headline"]


def test_a_home_that_is_the_hub_fails():
    r = row(ledger({"npc_son": "kitchen", "npc_x": "parents_room"}))
    assert r["pass_"] is True    # nothing opens off the kitchen; the wardrobe off the bedroom is a container
    r = row(ledger({"npc_son": "street"}))
    assert r["pass_"] is False and "is a hub" in r["detail"][0]


def test_a_thoroughfare_home_fails():
    r = row(ledger({"npc_son": "upstairs"}))
    assert r["pass_"] is False
    assert any("thoroughfare" in d for d in r["detail"]) and any("hub" in d for d in r["detail"])


def test_a_container_home_fails():
    r = row(ledger({"npc_son": "wardrobe"}))
    assert r["pass_"] is False and "container" in r["detail"][0]


def test_offscreen_still_passes():
    assert row(ledger({"npc_son": "offscreen"}))["pass_"] is True


def test_a_grandfathered_game_warns_and_passes():
    r = row(ledger(COUPLE, slug="members_only"))
    assert r["pass_"] is True
    assert all(d.startswith("warn (grandfathered") for d in r["detail"]) and len(r["detail"]) == 2


def test_a_grandfathered_game_that_shipped_since_fails():
    r = row(ledger(COUPLE, slug="members_only",
                   releases=[{"version": "0.3", "shipped": gates.HOME_IS_A_BEDROOM_SINCE}]))
    assert r["pass_"] is False


def test_the_old_reasons_are_never_grandfathered():
    r = row(ledger({"npc_son": "attic"}, slug="members_only"))
    assert r["pass_"] is False and "not a declared location" in r["detail"][0]


def test_na_policy_is_unchanged():
    assert row(None)["na"] is True
    assert row(ledger({}))["na"] is True
