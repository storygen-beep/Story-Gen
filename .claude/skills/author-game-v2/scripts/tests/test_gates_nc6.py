"""NC6 (PRD v2 phase 4 · D5 · J6, 2026-09-30): the men's numbers are read.

Every trait a man keeps is shown (EN7 `show_traits`) unless hidden or a ladder counter, and
every shown trait is read by a step gate AND a line branch.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}
TRUST = {"type": "trait", "subject": "npc", "npc_id": "npc_vic", "trait_key": "trust",
         "operator": "gte", "value": 20}


def game(kept=None, page=None, own=None, gate_read=True, line_read=True, labels=None):
    npc = {"id": "npc_vic", "name": "Vic", "core_traits": kept if kept is not None else {"trust": 0}}
    if own:
        npc["show_traits"] = own
    blocks = [{"type": "paragraph", "content": "He looks up."}]
    if line_read:
        blocks.append({"type": "group", "conditions": dict(V1, items=[TRUST]),
                       "blocks": [{"type": "paragraph", "content": "He smiles."}]})
    trig = {"location": "room", "is_repeatable": False}
    if gate_read:
        trig["conditions"] = dict(V1, items=[TRUST])
    g = {"npcs": [npc], "canvases": [{"id": "step", "trigger": trig,
                                      "nodes": [{"id": "n", "blocks": blocks}]}]}
    if page is not None:
        g["ui"] = {"cast_page": {"show_traits": page}}
    if labels:
        g["traits"] = {"labels": labels}
    return g


def row(g, state=None):
    return gates._mens_numbers(g, state)


def test_shown_and_read_both_ways_passes():
    ok, head, detail, _n = row(game(page=["trust"]))
    assert ok is True, detail


def test_shown_on_his_own_card_counts():
    assert row(game(own=["trust"]))[0] is True


def test_hidden_and_counters_are_exempt():
    g = game(kept={"trust": 0, "secret": 0, "vic_stage": 0, "steps": 0}, page=["trust"],
             labels=[{"key": "secret", "hidden": True}])
    state = {"board": {"characters": [{"id": "npc_vic", "ladder": {"counter": "steps"}}]}}
    assert row(g, state)[0] is True


def test_no_kept_traits_is_na():
    assert row(game(kept={}))[0] is None


def test_a_kept_trait_nothing_shows_fails():
    ok, _h, detail, _n = row(game())
    assert ok is False and detail[0].startswith("npc_vic: keeps `trust` and nothing shows it")


def test_a_shown_trait_no_gate_reads_fails():
    ok, _h, detail, _n = row(game(page=["trust"], gate_read=False))
    assert ok is False and "no step gate reads it" in detail[0]


def test_a_shown_trait_no_line_reads_fails():
    ok, _h, detail, _n = row(game(page=["trust"], line_read=False))
    assert ok is False and "no line branch reads it" in detail[0]
