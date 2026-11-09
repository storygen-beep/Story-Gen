"""A phone reply is a located flag setter (2026-11-09).

`_build_flag_unlock_map` registers phone replies as setters (`"is_phone": True`) and the
runtime hint renders them ("📱 Check your messages"), but `validate_flag_chains` used to
refuse any setter with no location or schedule, so a trigger gated on a flag that only a
phone reply sets hard-failed the build with "MISSING HINT". first_term (DECISIONS 210) had
to read a hidden trait instead. This pins the fix and its control: a flag set only by a
triggerless canvas still fails.

    pytest apps/game_generation/tests/test_flag_chain_phone_setter.py -q
"""
import copy

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
KITCHEN = "loc_kitchen"
FLAG = "phone_test_flag"


def _reader(cid=f"reads_{FLAG}"):
    """A kitchen row whose trigger needs the flag is_true."""
    return {
        "id": cid,
        "name": "Reads the flag",
        "trigger": {"location": KITCHEN, "is_repeatable": True, "priority": 4, "is_active": True,
                    "conditions": {"version": "1.0", "logic": "AND", "items": [
                        {"type": "flag", "subject": "player", "flag_key": FLAG, "operator": "is_true"}]}},
        "nodes": [{"id": "base", "name": "Base",
                   "blocks": [{"type": "paragraph", "content": "The flag is set."}],
                   "exit_block": {"type": "location", "text": "Leave.",
                                  "config": {"destinationType": "specific", "locationId": KITCHEN}}}],
    }


def _phone(d):
    """One thread whose reply sets the flag."""
    d["phone"] = {
        "enabled": True,
        "apps": [{"id": "messages", "type": "chat", "label": "Messages"}],
        "conversations": [{
            "id": "test_thread", "app": "messages", "npc": "npc_frank", "notify": "Frank",
            "trigger": {"conditions": {"version": "1.0", "logic": "AND", "items": [
                {"type": "flag", "subject": "player", "flag_key": "summer_started", "operator": "is_true"}]}},
            "blocks": [
                {"type": "message", "sender": "npc", "content": "come over?"},
                {"type": "reply", "choices": [
                    {"text": "yes", "flagEffects": [{"targetType": "player", "flag": FLAG, "op": "set"}]},
                    {"text": "no"}]},
            ],
        }],
    }
    return d


def _triggerless_setter():
    """A canvas with no trigger whose exit sets the flag: no place, no schedule, not a phone."""
    return {
        "id": "sets_it_nowhere",
        "name": "Sets it nowhere",
        "nodes": [{"id": "base", "name": "Base",
                   "blocks": [{"type": "paragraph", "content": "Somewhere."}],
                   "exit_block": {"type": "location", "text": "Leave.",
                                  "config": {"destinationType": "specific", "locationId": KITCHEN,
                                             "flagEffects": [{"targetType": "player", "flag": FLAG}]}}}],
    }


def _errors(d):
    graph = build_game_graph(normalize(d))
    gen = TweeComprehensiveGeneratorV2()
    gen.generate(graph.project, {}, graph=graph)
    return [e for e in (gen.validate_flag_chains() or []) if e.get("flag_key") == FLAG]


def test_a_phone_reply_is_a_located_setter():
    d = _phone(copy.deepcopy(parse_toml(FIXTURE)))
    d["canvases"].append(_reader())
    assert not _errors(d)


def test_a_triggerless_canvas_setter_still_fails():
    d = copy.deepcopy(parse_toml(FIXTURE))
    d["canvases"] += [_triggerless_setter(), _reader()]
    errs = _errors(d)
    assert errs and "MISSING HINT" in errs[0]["issue"], errs
