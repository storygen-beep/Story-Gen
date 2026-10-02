"""The truth rule, rule 5: prose names her clothes only where a check backs it (World and
Systems PRD, Phase 6B, 2026-10-02). `_clothes_unbacked`, built on readable.py's
`unearned_events` in its `needs_clothing` mode.

Garments come from the game's own `[[clothing]]` names; "hers" is `your <garment>` (second
person) or her name's / `her` in a sentence opening on her name (third person). Backers: the
trigger, an enclosing group, the location's entry_conditions, a choice into the canvas or node,
an equip in an earlier node. An explicit canvas with a strip word in the same beat is exempt.
Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

HOT = "He fucks her, his cock deep in her wet cunt, and she comes."


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def wears(i):
    return {"type": "clothing_item", "item_id": i, "operator": "equipped"}


def para(t):
    return {"type": "paragraph", "content": t}


def game(*canvases, person="second", locations=None):
    return {"settings": {"clothing_enabled": True, "narration_person": person},
            "player": {"name": "Mara"},
            "clothing": [{"id": "skirt_short", "name": "Short skirt", "slot": "bottom",
                          "corruption": 2},
                         {"id": "blouse_tight", "name": "Tight silk blouse", "slot": "top",
                          "corruption": 2},
                         {"id": "blouse_white", "name": "White blouse", "slot": "top"},
                         {"id": "shop_dress", "name": "A dress of your own", "slot": "dress"}],
            "locations": locations or [{"id": "bar"}],
            "canvases": list(canvases)}


def canvas(cid, *blocks, conditions=None, location="bar", nodes=None):
    trig = {"location": location}
    if conditions:
        trig["conditions"] = conditions
    return {"id": cid, "trigger": trig,
            "nodes": nodes or [{"id": "n", "blocks": list(blocks)}]}


def rows(g):
    model, g2 = gates.build(g)
    return gates._clothes_unbacked(model, g2)


def test_an_unbacked_garment_is_listed():
    r = rows(game(canvas("c", para("Your skirt rides up."))))
    assert len(r) == 1 and '"Your skirt"' in r[0] and r[0].startswith("c/n")


def test_the_trigger_backs_it():
    assert rows(game(canvas("c", para("Your skirt rides up."),
                            conditions=cond(wears("skirt_short"))))) == []


def test_an_enclosing_group_backs_it():
    grp = {"type": "group", "props": {"conditions": cond(wears("skirt_short")),
                                      "blocks": [para("Your skirt rides up.")]}}
    assert rows(game(canvas("c", grp))) == []


def test_the_locations_entry_conditions_back_it():
    locs = [{"id": "bar", "entry_conditions": cond(
        {"type": "clothing_slot", "slot": "bottom", "operator": "equipped"})}]
    assert rows(game(canvas("c", para("Your skirt rides up.")), locations=locs)) == []


def test_a_choice_into_the_canvas_backs_it():
    door = canvas("door", para("The door."), nodes=[{"id": "n", "blocks": [], "exit_block": {
        "choices": [{"text": "Go in", "targetType": "canvas", "canvasId": "c",
                     "conditions": cond(wears("skirt_short"))}]}}])
    assert rows(game(door, canvas("c", para("Your skirt rides up.")))) == []


def test_an_equip_in_an_earlier_node_backs_it_and_a_later_one_does_not():
    first = {"id": "a", "blocks": [], "exit_block": {"config": {"wardrobeEffects": [
        {"action": "equip", "item_id": "skirt_short"}]}}}
    second = {"id": "b", "blocks": [para("Your skirt rides up.")]}
    assert rows(game(canvas("c", nodes=[first, second]))) == []
    assert len(rows(game(canvas("c", nodes=[dict(second, id="a"), dict(first, id="b")])))) == 1


def test_a_stat_both_garments_reach_does_not_back_the_tight_blouse():
    # worn_corruption gte 2 is met by the short skirt with the white blouse.
    grp = {"type": "group", "props": {"conditions": cond(
        {"type": "worn_corruption", "operator": "gte", "value": 2}),
        "blocks": [para("His eyes go down your tight blouse.")]}}
    r = rows(game(canvas("c", grp)))
    assert len(r) == 1 and "your tight blouse" in r[0]


def test_an_explicit_beat_with_a_strip_word_is_exempt():
    assert rows(game(canvas("c", para(HOT + " Naked, you kick your skirt away.")))) == []


def test_strip_club_is_not_a_strip_word_and_not_a_garment():
    r = rows(game(canvas("c", para(HOT + " In the strip club he lifts your skirt."))))
    assert len(r) == 1
    assert rows(game(canvas("d", para("You dance at the strip club.")))) == []


def test_his_shirt_and_her_skirt_in_second_person_are_not_hers():
    assert rows(game(canvas("c", para("Her skirt is short. His blouse is open.")))) == []


def test_third_person_reads_her_name_and_her_in_her_sentence():
    r = rows(game(canvas("c", para("Mara's skirt rides up. Mara tugs her blouse. Ana fixes "
                                   "her skirt.")), person="third"))
    assert sorted(x.split('"')[1] for x in r) == ["Mara's skirt", "her blouse"]


def test_clothing_off_is_none():
    g = game(canvas("c", para("Your skirt rides up.")))
    g["settings"]["clothing_enabled"] = False
    assert rows(g) is None
