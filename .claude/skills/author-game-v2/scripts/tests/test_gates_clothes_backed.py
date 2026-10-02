"""The truth rule, rule 5: prose names her clothes only where a check backs it (World and
Systems PRD, Phase 6B, 2026-10-02). `_clothes_unbacked`, built on readable.py's
`unearned_events` in its `needs_clothing` mode.

Garments come from the game's own `[[clothing]]` names; "hers" is `your <garment>` (second
person) or her name's / `her` in a sentence opening on her name (third person). Backers: the
trigger, an enclosing group, the location's entry_conditions, a choice into the canvas or node,
an equip in an earlier node. An explicit canvas with a strip word in the same beat is exempt.
Promoted to a `--ship` BLOCK row (n/a passes; LO B as the other rows). Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
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


# ── promoted to a `--ship` BLOCK (K4 commit 2): the two false-positive kinds ──────

def test_a_name_with_of_takes_the_garment_before_it():
    assert rows(game(canvas("c", para("You did it on your own.")))) == []
    assert len(rows(game(canvas("c", para("Your dress is new."))))) == 1


def test_an_undressing_phrase_in_an_explicit_beat_is_exempt():
    for line in ("He yanks your skirt down.", "He pops your blouse open.",
                 "\"Your skirt.\" You slide them down your legs."):
        assert rows(game(canvas("c", para(HOT + " " + line)))) == [], line


def test_pushing_his_hands_off_is_not_undressing():
    assert len(rows(game(canvas("c", para(HOT + " You shove his hands off your blouse."))))) == 1


def test_the_gate_is_na_with_clothing_off_and_red_with_a_line():
    model, g = gates.build(game(canvas("c", para("Your skirt rides up."))))
    ok, head, detail = gates._her_clothes_are_backed(model, g)
    assert ok is False and head.startswith("1 line(s)") and detail
    g["settings"]["clothing_enabled"] = False
    assert gates._her_clothes_are_backed(model, g)[0] is None
    gates._LEGACY_RULES.add("clothes_backed")
    try:
        assert gates._her_clothes_are_backed(model, game())[0] is True
    finally:
        gates._LEGACY_RULES.discard("clothes_backed")


def test_the_ship_row_warns_grandfathered_blocks_billable_and_na_passes(tmp_path, monkeypatch):
    import test_gates_wardrobe_reads as wr
    import test_gates_ws6 as ws6
    g = wr.dressed_game()
    g["clothing"][0]["name"] = "Short skirt"
    g["canvases"][2]["nodes"][0]["blocks"].append(para("Your skirt rides up."))
    row = "her clothes are backed"
    assert wr.ship(tmp_path, monkeypatch, "members_only", g, ws6.green_state())[row] == "warn"
    assert wr.ship(tmp_path, monkeypatch, "billable_hours", g, ws6.green_state())[row] is False
    st = ws6.green_state()
    st["releases"] = [{"version": "0.2", "shipped": "2026-10-02"}]
    assert wr.ship(tmp_path, monkeypatch, "members_only", g, st)[row] is False
    g["settings"]["clothing_enabled"] = False
    assert wr.ship(tmp_path, monkeypatch, "billable_hours", g, ws6.green_state())[row] is None
