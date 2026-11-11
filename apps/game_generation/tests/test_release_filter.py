"""scripts/release_filter.py — the release slice (first_term DECISIONS 230)."""
import copy
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import release_filter as rf  # noqa: E402

FIRST_TERM = ROOT / "games" / "first_term" / "toml_phases" / "7_final_game.toml"


def _cond(*items, logic="AND"):
    return {"version": "1.0", "logic": logic, "items": list(items)}


def _trait(key, op, val, npc=None):
    d = {"type": "trait", "subject": "npc" if npc else "player", "trait_key": key, "operator": op, "value": val}
    if npc:
        d["npc_id"] = npc
    return d


def _game():
    return {
        "player": {"core_traits": {"corruption": 0, "ryan_step": 0}},
        "npcs": [{"id": "npc_ryan", "core_traits": {"want": 0, "warmth": 50}},
                 {"id": "npc_zoe", "release": 2, "core_traits": {}}],
        "locations": [{"id": "home"}, {"id": "hall", "entry_from": "home"},
                      {"id": "party", "release": 2}, {"id": "party_room", "entry_from": "party"}],
        "canvases": [
            {"id": "ryan_01", "trigger": {"location": "hall"}, "nodes": [{"id": "a", "blocks": [
                {"type": "paragraph", "content": "always"},
                {"type": "group", "conditions": _cond(_trait("corruption", "gte", 20)), "blocks": [
                    {"type": "paragraph", "content": "later heat"}]},
                {"type": "group", "conditions": _cond(_trait("corruption", "lt", 20)), "blocks": [
                    {"type": "paragraph", "content": "now"}]},
            ], "exit_block": {"type": "choices", "choices": [
                {"text": "Go.", "targetType": "location", "locationId": "home",
                 "effects": [{"targetType": "player", "trait": "corruption", "op": "add", "value": 1},
                             {"targetType": "npc", "npcId": "npc_ryan", "trait": "warmth", "op": "add", "value": -2},
                             {"targetType": "player", "trait": "money", "op": "add", "value": 8}],
                 "flagEffects": [{"flag": "invite", "op": "set"}]},
                {"text": "Bold only.", "targetType": "node", "nodeId": "a",
                 "conditions": _cond(_trait("corruption", "gte", 40))},
                {"text": "Later.", "targetType": "node", "nodeId": "a", "release": 2},
            ]}}]},
            {"id": "ryan_02", "trigger": {"location": "hall"}, "nodes": []},
            {"id": "zoe_party", "trigger": {"location": "party_room"}, "nodes": []},
            {"id": "invite_reader", "trigger": {"location": "home", "conditions": _cond(
                {"type": "flag", "subject": "player", "flag_key": "invite", "operator": "is_true"},
                _trait("want", "gte", 10, npc="npc_ryan"))}, "nodes": []},
            {"id": "gym_now", "release_until": 1, "trigger": {"location": "home"}, "nodes": []},
        ],
        "quest_cards": [
            {"npc_id": "npc_ryan", "text": "step 2 card",
             "when": [{"type": "trait", "subject": "player", "trait": "ryan_step", "op": "eq", "value": 1}],
             "goals": [{"type": "trait", "subject": "npc", "npc_id": "npc_ryan", "trait": "want", "op": "gte", "value": 10}]},
            {"npc_id": "npc_zoe", "text": "zoe card"},
        ],
        "sidebar_items": [{"type": "trait_words", "trait": "corruption", "bands": [
            {"min": 0, "max": 19, "text": "Good Girl"}, {"min": 20, "max": 39, "text": "Curious"}]}],
    }


STATE = {"board": {"characters": [{"id": "npc_ryan", "ladder": {"counter": "ryan_step", "steps": [
    {"n": 1, "canvas": "ryan_01", "release": 1}, {"n": 2, "canvas": "ryan_02", "release": 2}]}}]},
    "release_page": {"release": 1, "meters": {"corruption": {"cap": 0}, "want": {"cap": 0, "npc": True},
                                               "warmth": {"hold": True, "npc": True}}}}


def _cut(target=1, state=STATE):
    g = _game()
    rep = rf.Report()
    rf.filter_game(g, copy.deepcopy(state), target, rep)
    return g, rep


def test_writer_round_trips_the_real_game():
    raw = FIRST_TERM.read_text()
    doc = tomllib.loads(raw)
    assert tomllib.loads(rf.dumps(doc)) == doc


def test_tags_and_dependants_drop():
    g, _ = _cut()
    assert [n["id"] for n in g["npcs"]] == ["npc_ryan"]
    assert {l["id"] for l in g["locations"]} == {"home", "hall"}          # party_room went with party
    ids = {c["id"] for c in g["canvases"]}
    assert "zoe_party" not in ids and "gym_now" in ids
    assert all("release" not in c and "release_until" not in c for c in g["canvases"])
    assert [q["text"] for q in g["quest_cards"]] == []                     # zoe's person gone; ryan's goal unreachable


def test_ladder_meters_and_report():
    g, rep = _cut()
    ids = {c["id"] for c in g["canvases"]}
    assert "ryan_02" not in ids                       # a later-release step
    assert "invite_reader" not in ids                 # Ryan's want is frozen at 0
    node = g["canvases"][0]["nodes"][0]
    texts = [b.get("content") or b["blocks"][0]["content"] for b in node["blocks"]]
    assert texts == ["always", "now"]
    choices = node["exit_block"]["choices"]
    assert [c["text"] for c in choices] == ["Go."]
    assert [e["trait"] for e in choices[0]["effects"]] == ["money"]   # corruption rise and held mood gone
    assert any("`invite`" in n for n in rep.notes)                     # setter whose reader was cut
    assert [b["text"] for b in g["sidebar_items"][0]["bands"]] == ["Good Girl"]


def test_authoring_keeps_everything_but_release_until_items():
    g, _ = _cut(target=rf.MAX, state={})
    ids = {c["id"] for c in g["canvases"]}
    assert {"ryan_01", "ryan_02", "zoe_party", "invite_reader"} <= ids
    assert "gym_now" not in ids
    assert len(g["canvases"][0]["nodes"][0]["exit_block"]["choices"]) == 3


def test_an_override_can_name_a_list_item_by_id():
    """DECISIONS 231: `locations[home_ryan_room].description` swaps one place's text for one release."""
    game = {"locations": [{"id": "a", "description": "old"}, {"id": "b", "description": "keep"}],
            "release_overrides": {"1": {"locations[a].description": "new"}}}
    rf.filter_game(game, {}, 1, rf.Report())
    assert [l["description"] for l in game["locations"]] == ["new", "keep"]
    assert "release_overrides" not in game


def test_a_band_that_always_holds_keeps_its_condition():
    """DECISIONS 231: an emptied group renders as the chain's <<else>> (v2.py _render_group_chain), so the
    top band would show at 0. The always-true band keeps one item and stays first."""
    game = _game()
    game["canvases"] = [{"id": "c", "trigger": {"location": "home", "is_repeatable": True}, "nodes": [{"id": "n",
        "blocks": [{"type": "group", "conditions": _cond(_trait("corruption", "lt", 20)), "blocks": [{"type": "paragraph", "content": "low"}]},
                   {"type": "group", "conditions": _cond(_trait("corruption", "gte", 0)), "blocks": [{"type": "paragraph", "content": "any"}]}],
        "exit_block": {"choices": [{"text": "x", "targetType": "location", "locationId": "home",
                                    "effects": [{"targetType": "npc", "npcId": "npc_ryan", "trait": "want", "op": "add", "value": -1}]}]}}]}]
    state = {"release_page": {"release": 1, "meters": {"corruption": {"cap": 0}, "want": {"cap": 0, "npc": True}}}}
    rf.filter_game(game, state, 1, rf.Report())
    groups = game["canvases"][0]["nodes"][0]["blocks"]
    assert all(g["conditions"]["items"] for g in groups)
    assert game["canvases"][0]["nodes"][0]["exit_block"]["choices"][0].get("effects") == []


def test_a_cut_app_takes_its_posts_and_calls():
    """DECISIONS 236: release 1 cuts the Feed and Calls apps; a post or call left behind would be drawn
    into an app the phone no longer has, and the counter only the feed moved goes from the labels."""
    game = _game()
    game["traits"] = {"labels": [{"key": "followers", "label": "Followers"}]}
    game["player"]["core_traits"]["followers"] = 0
    game["phone"] = {"enabled": True, "apps": [
        {"id": "messages", "type": "chat"},
        {"id": "feed", "type": "social_feed", "release": 2,
         "post_actions": [{"label": "Post a selfie", "counter_trait": "followers"}]},
        {"id": "calls", "type": "calls", "release": 2}],
        "posts": [{"id": "p", "app": "feed", "trigger": {"conditions": _cond(_trait("followers", "gte", 20))}}],
        "calls": [{"id": "c", "app": "calls", "caller": "npc_ryan"}],
        "conversations": [{"id": "m", "app": "messages", "npc": "npc_ryan"}]}
    rep = rf.Report()
    rf.filter_game(game, {"release_page": {"release": 1}}, 1, rep)
    ph = game["phone"]
    assert [a["id"] for a in ph["apps"]] == ["messages"]
    assert ph["posts"] == [] and ph["calls"] == []
    assert [c["id"] for c in ph["conversations"]] == ["m"]
    assert game["traits"]["labels"] == [] and "followers" not in game["player"]["core_traits"]
