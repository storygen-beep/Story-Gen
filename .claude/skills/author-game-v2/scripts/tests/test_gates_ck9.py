"""CK9 (PRD v2, 2026-09-30): "location fill" reads this release's places.

With `release_page.places` declared, a place cut from the release is left out of the
budget: no drift line, not in the plan total or the plan's anchor share. Without it,
nothing changes. The fixture is written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def words(n):
    return " ".join(["word"] * (n - 1)) + " end."


def game():
    """bar ~2000 words, flat ~500, docks is in the game with nothing placed yet."""
    def canvas(cid, loc, n):
        return {"id": cid, "trigger": {"location": loc, "is_repeatable": True},
                "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": words(n)}]}]}
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "bar"}, {"id": "flat"}, {"id": "docks"}],
            "canvases": [canvas("b", "bar", 2000), canvas("f", "flat", 500)]}


def state(places=None, docks_fill=3000):
    s = {"board": {"locations": [{"id": "bar", "fill": 2000}, {"id": "flat", "fill": 500},
                                 {"id": "docks", "fill": docks_fill}]}}
    if places is not None:
        s["release_page"] = {"places": places}
    return s


def fill_row(st):
    model, g2 = gates.build(copy.deepcopy(game()))
    return next(r for r in gates.run_gates(model, g2, st) if r["gate"] == "location fill")


def test_a_cut_place_is_ignored():
    r = fill_row(state(places=["bar", "flat"]))
    assert not any(d.startswith("docks: declared") for d in r["detail"]), r["detail"]
    assert "vs 2,500 declared" in r["headline"]
    assert "2/2 on their own budget" in r["headline"]
    assert "1 place(s) cut from this release ignored" in r["headline"]


def test_without_release_places_the_cut_place_is_judged():
    r = fill_row(state())
    assert any(d.startswith("docks: declared 3,000 words, delivered 0") for d in r["detail"]), r["detail"]
    assert "vs 5,500 declared" in r["headline"]


def test_cut_fills_do_not_dilute_the_plan_anchor():
    # Six cut places at 2,000 each make bar 2,000 of 14,500 (14%): no centre. Cut, bar is 80%.
    def st(places=None):
        s = state(places=places)
        s["board"]["locations"] += [{"id": f"cut_{i}", "fill": 2000} for i in range(6)]
        return s
    assert any("the PLAN has no centre" in d for d in fill_row(st())["detail"])
    assert not any("the PLAN has no centre" in d
                   for d in fill_row(st(places=["bar", "flat"]))["detail"])


def test_place_ids_may_be_dicts():
    r = fill_row(state(places=[{"id": "bar"}, {"id": "flat"}]))
    assert "vs 2,500 declared" in r["headline"]
