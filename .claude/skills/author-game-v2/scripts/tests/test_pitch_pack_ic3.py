"""Fixtures for the pitch pack's RELATIONSHIPS section and --person (PRD_IDEAS_AND_CRAFT IC3 +
the "their side" fix, 2026-09-27).

The game is a minimal dict handed to `pitch_pack.pack` through a patched `gates._load`; the state
file is written to a temp dir; nothing in games/ is read or written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402


def flag_set(flag):
    return {"flagEffects": [{"flag": flag, "op": "set"}]}


def reads(flag):
    return {"version": "1.0", "logic": "AND", "items": [{"type": "flag", "flag_key": flag, "op": "is_true"}]}


def canvas(cid, sets=None, needs=None, npc=None, rep=False, text="He looks at you."):
    trig = {"location": "room_a", "is_repeatable": rep}
    if npc:
        trig["npc"] = npc
    if needs:
        trig["conditions"] = reads(needs)
    return {"id": cid, "trigger": trig,
            "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": text}],
                       "exit_block": {"config": flag_set(sets) if sets else {}}}]}


def game():
    return {
        "project": {"id": "fx", "title": "Fixture"},
        "player": {"core_traits": {"money": 10}},
        "locations": [{"id": "room_a"}],
        "npcs": [{"id": "npc_ray", "name": "Ray"}, {"id": "npc_ana", "name": "Ana"},
                 {"id": "npc_bo", "name": "Bo"}],
        "canvases": [
            # Ray: three steps found by id prefix, written out of order on purpose.
            canvas("ray_03", sets="ray_03", needs="ray_02", text="He says next time. You both hear it."),
            canvas("ray_01", sets="ray_01"),
            canvas("ray_02", sets="ray_02", needs="ray_01"),
            canvas("hub_ray", npc="npc_ray", rep=True),
            # Ana: one step found by binding; the flag it sets is read by nobody else.
            canvas("meet_ana", sets="ana_met", npc="npc_ana"),
            # Bo: one step found only through the declared ladder.
            canvas("porch_scene", sets="porch_done"),
            canvas("later", needs="porch_done"),
        ],
    }


def state():
    return {"board": {"characters": [{"id": "npc_bo", "ladder": {"counter": "bo_stage",
                                                                "steps": [{"n": 1, "canvas": "porch_scene"}]}}]},
            "promises": [{"text": "Ana owes her an answer about the flat", "made_in": "0.1", "paid_in": None}],
            "releases": []}


def run(tmp_path, monkeypatch, capsys, st, person=None):
    monkeypatch.setattr(pitch_pack.gates, "_load", lambda path: game())
    sp = tmp_path / "v2_state.json"
    sp.write_text(json.dumps(st), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    code = pitch_pack.pack("fx", "unused.toml", str(sp), person=person)
    return code, capsys.readouterr().out


def rels():
    g = game()
    model, _ = pitch_pack.gates.build(g)
    return {r["id"]: r for r in pitch_pack._relationships(g, model, state())}


def test_attribution_by_prefix_binding_and_ladder():
    r = rels()
    assert [s["how"] for s in r["npc_ray"]["steps"]] == ["id prefix"] * 3
    assert r["npc_ana"]["steps"][0]["how"] == "binds npc_ana"
    assert r["npc_bo"]["steps"][0]["how"] == "declared ladder"
    assert [x["id"] for x in r["npc_ray"]["surfaces"]] == ["hub_ray"]


def test_chain_order_follows_flags_not_file_order():
    assert [s["id"] for s in rels()["npc_ray"]["steps"]] == ["ray_01", "ray_02", "ray_03"]


def test_unread_setup_is_marked():
    r = rels()
    ray3 = dict(r["npc_ray"]["steps"][2]["flags"])
    assert ray3 == {"ray_03": False}                 # nothing after it reads ray_03
    assert dict(r["npc_bo"]["steps"][0]["flags"]) == {"porch_done": True}
    assert r["npc_ana"]["unread"] == 1


def test_promise_naming_the_person_is_counted_and_sorts_first():
    r = rels()
    assert r["npc_ana"]["promises"] == ["Ana owes her an answer about the flat"]
    g = game()
    model, _ = pitch_pack.gates.build(g)
    order = [x["id"] for x in pitch_pack._relationships(g, model, state())]
    assert order[0] == "npc_ana"                     # an open promise outranks unread set-ups


def test_section_prints_with_sort_keys_and_exit_zero(tmp_path, monkeypatch, capsys):
    code, out = run(tmp_path, monkeypatch, capsys, state())
    assert code == 0
    block = out[out.index("RELATIONSHIPS"):out.index("THE WANT")]
    assert "a sort, not a score" in block
    assert "ray_03 [id prefix]" in " ".join(block.split()) and "sets: ray_03 (NOT READ)" in block
    assert "SCENES ALREADY SHIPPED" in block


def test_person_prints_one_block(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, state(), person="npc_bo")
    block = out[out.index("RELATIONSHIPS"):out.index("THE WANT")]
    assert "npc_bo" in block and "npc_ray" not in block and "npc_ana" not in block
    _, out = run(tmp_path, monkeypatch, capsys, state(), person="npc_nobody")
    assert "unknown person `npc_nobody`" in out
