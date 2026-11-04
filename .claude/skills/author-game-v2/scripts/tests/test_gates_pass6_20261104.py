"""LO's calls on the sixth alignment check, 2026-11-04.

  13    gate `no child framing next to sex`       register.md "Everyone is an adult"
  B54   gate `her clothes are named exactly`      register.md rule 5
  E98   gate `a need falls where it says`         the-meters.md M8
  G76   gate `an act pays inside its own stage`   the-arc.md A4d
  J76   gate `a deduction is gated or priced`     engine.md §21

Fixtures are built here; nothing in games/ is read.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
from test_gates_group2_checks import EXPLICIT, ch, cv, game, nd, pay, row  # noqa: E402


# ── no child framing next to sex ─────────────────────────────────────────────
CHILD = "no child framing next to sex"
PEOPLE = [{"id": "npc_jake", "name": "Jake", "role": "campus guy", "relationship": "A guy from campus."},
          {"id": "npc_zoe", "name": "Zoe", "role": "college friend", "relationship": "Your friend."},
          {"id": "npc_mark", "name": "Mark", "role": "step-father", "relationship": "Your step-father."},
          {"id": "npc_vance", "name": "Mr. Vance", "role": "landlord", "relationship": "Your landlord."}]


def says(npc, text):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def child_game(*blocks):
    return game(cv("scene", [nd("a", [ch("Go.")], blocks=list(blocks))]), npcs=PEOPLE)


def test_jakes_good_girl_passes():
    assert row(child_game(says("npc_jake", "Good girl.")), CHILD, {})["pass_"] is True


def test_marks_good_girl_fails_with_no_body_word_anywhere():
    r = row(child_game(says("npc_mark", "Good girl.")), CHILD, {})
    assert r["pass_"] is False and "npc_mark" in r["detail"][0]


def test_vances_growing_up_beside_your_legs_fails():
    r = row(child_game(says("npc_vance", "Growing up."), says("npc_vance", "Your legs.")), CHILD, {})
    assert r["pass_"] is False and "Growing up" in r["detail"][0]


def test_the_same_phrase_with_no_body_word_on_the_node_passes():
    assert row(child_game(says("npc_vance", "You're growing up."), says("npc_vance", "Rent's due.")), CHILD, {})["pass_"] is True


def test_my_girl_counts_only_from_a_parent_figure():
    assert row(child_game(says("npc_jake", "That's my girl."), says("npc_jake", "Your legs.")), CHILD, {})["pass_"] is True
    assert row(child_game(says("npc_mark", "That's my girl."), says("npc_mark", "Your legs.")), CHILD, {})["pass_"] is False


def test_a_level_name_on_a_card_or_a_label_is_ui_not_a_line():
    g = child_game(says("npc_jake", "Hi."))
    g["quest_cards"] = [{"id": "c", "goals": [{"label": "Good Girl"}]}]
    g["sidebar_items"][0]["bands"] = [{"min": 0, "max": 19, "text": "Good Girl"}]
    assert row(g, CHILD, {})["pass_"] is True


def test_the_gate_is_on_the_truth_list_beside_one_pool():
    names = [t[0] for t in gates._TRUTH_GATES]
    assert names.index(CHILD) == names.index("one pool, one place") + 1


# ── B54 · her clothes are named exactly ──────────────────────────────────────
NAMED = "her clothes are named exactly"
UNDER = "You stand there in your underwear."
EXPOSED = {"version": "1.0", "logic": "AND", "items": [{"type": "worn_exposure", "operator": "gte", "value": 1}]}
SLOT = {"version": "1.0", "logic": "AND", "items": [{"type": "clothing_slot", "slot": "top", "operator": "unequipped"}]}


def clothes_game(back=None, group=False):
    body = [{"type": "group", "props": {"conditions": SLOT},
             "blocks": [{"type": "paragraph", "content": UNDER}]}] if group else None
    second = nd("b", [ch("Go.")], text=UNDER, blocks=body)
    first = nd("a", [ch("On.", node="b", conds=back)])
    c = cv("scene", [first, second], conditions=EXPOSED)
    return game(c, clothing=[{"id": "t", "name": "Tee", "slot": "top"}])


def test_a_line_on_worn_exposure_alone_still_fails():
    assert row(clothes_game(), NAMED, {})["pass_"] is False


def test_the_choice_that_led_to_the_screen_backs_it():
    assert row(clothes_game(back=SLOT["items"]), NAMED, {})["pass_"] is True


def test_an_enclosing_group_backs_it():
    assert row(clothes_game(group=True), NAMED, {})["pass_"] is True


def test_one_unbacked_way_in_leaves_the_line_unbacked():
    g = clothes_game(back=SLOT["items"])
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"].append(ch("Also.", node="b"))
    assert row(g, NAMED, {})["pass_"] is False


# ── E98 · "sex" means partnered ──────────────────────────────────────────────
NEED = "a need falls where it says"
NEED_STATE = {"board": {"ascent_tiers": ["heat", "show"],
                        "needs": [{"key": "hygiene", "falls": "faster after sex"}]}}
ALONE = "You fuck your wet cunt, your tits bouncing, your clit under your fingers, and you come."


def need_game(*canvases):
    return game(*canvases, player={"core_traits": {"heat": 0, "show": 0, "hygiene": 50}})


def test_solo_and_watching_canvases_do_not_count_as_sex():
    fall = [pay("hygiene", -10)]
    g = need_game(cv("bed", [nd("a", [ch("Go.", eff=fall)], text=EXPLICIT)], requires_npc="npc_a"),
                  cv("touch_bed", [nd("a", [ch("Go.")], text=ALONE)]),
                  cv("park_watch_couple", [nd("a", [ch("Go.")], text=EXPLICIT)], requires_npc="npc_a"))
    assert row(g, NEED, NEED_STATE)["pass_"] is True


def test_a_partnered_scene_that_takes_nothing_still_fails():
    g = need_game(cv("bed", [nd("a", [ch("Go.")], text=EXPLICIT)], requires_npc="npc_a"))
    r = row(g, NEED, NEED_STATE)
    assert r["pass_"] is False and any("names sex" in d for d in r["detail"])


# ── G76 · a dress code sets the stage ────────────────────────────────────────
STAGE = "an act pays inside its own stage"
STAGE_STATE = {"board": {"ascent_tiers": ["heat"]}}
STAGE_BANDS = [{"min": 0, "max": 19, "text": "A"}, {"min": 20, "max": 39, "text": "B"},
               {"min": 40, "max": 59, "text": "C"}, {"min": 60, "text": "D"}]


def heat(op, v):
    return {"type": "trait", "subject": "player", "trait_key": "heat", "operator": op, "value": v}


def walk_game(garment, cap):
    rules = [{"conditions": {"version": "1.0", "logic": "AND",
                             "items": [{"type": "worn_type", "operator": "eq", "value": "skirt"}, heat("lt", 20)]},
              "slots_required": ["legwear"], "message": "Not yet."},
             {"conditions": {"version": "1.0", "logic": "AND", "items": [heat("gte", 40)]},
              "slots_required": ["top", "bottom"], "message": "No."},
             {"conditions": {"version": "1.0", "logic": "AND", "items": [heat("gte", 20)]},
              "slots_required": ["underwear", "top", "bottom"], "message": "No."},
             {"slots_required": ["underwear", "top", "bottom"], "message": "No."}]
    conds = {"version": "1.0", "logic": "AND", "items": [garment]}
    g = game(cv("walk", [nd("a", [ch("Walk.", eff=[pay("heat", 1, cap=cap)])])], location="street", conditions=conds),
             clothing=[{"id": "s", "name": "Skirt", "slot": "bottom", "type": "skirt"},
                       {"id": "p", "name": "Panties", "slot": "underwear"},
                       {"id": "t", "name": "Tee", "slot": "top"}],
             sidebar_items=[{"trait": "heat", "bands": STAGE_BANDS}])
    g["locations"].append({"id": "street", "name": "Street", "clothing_rules": rules})
    return g


SKIRT = {"type": "worn_type", "operator": "eq", "value": "skirt"}
NO_PANTIES = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}


def test_a_garment_that_needs_20_can_cap_at_39_and_no_higher():
    assert row(walk_game(SKIRT, 39), STAGE, STAGE_STATE)["pass_"] is True
    assert row(walk_game(SKIRT, 59), STAGE, STAGE_STATE)["pass_"] is False


def test_a_garment_that_needs_40_can_cap_at_59_and_no_higher():
    assert row(walk_game(NO_PANTIES, 59), STAGE, STAGE_STATE)["pass_"] is True
    r = row(walk_game(NO_PANTIES, 79), STAGE, STAGE_STATE)
    assert r["pass_"] is False and "opens at heat 40" in r["detail"][0]


def test_with_no_dress_code_the_cap_stays_at_the_first_stage():
    g = walk_game(SKIRT, 39)
    g["locations"][-1].pop("clothing_rules")
    assert row(g, STAGE, STAGE_STATE)["pass_"] is False


# ── J76 · a clamp is no net under money ──────────────────────────────────────
DEDUCT = "a deduction is gated or priced"


def test_a_clamped_money_deduction_fails_and_the_fix_offers_no_clamp():
    r = row(game(cv("buy", [nd("a", [ch("Buy.", eff=[pay("money", -10, clamp=True)])])])), DEDUCT, {})
    assert r["pass_"] is False and "clamp" not in r["detail"][0]


def test_the_declared_currency_counts_as_money():
    g = game(cv("buy", [nd("a", [ch("Buy.", eff=[pay("show", -10, clamp=True)])])]))
    assert row(g, DEDUCT, {"board": {"economy": {"currency": "show"}}})["pass_"] is False


def test_a_clamped_meter_deduction_still_passes():
    assert row(game(cv("rest", [nd("a", [ch("Rest.", eff=[pay("energy", -1, clamp=True)])])])), DEDUCT, {})["pass_"] is True
