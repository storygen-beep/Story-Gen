"""Fixtures for the pitch pack's NAMING section and per-person scene list (LO, 2026-09-27: the
pitchers kept restaging shipped scenes, writing "Mum" in a "your mother" game, and breaking the
cast's term-of-address rule). Nothing in games/ is read or written.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402


def game():
    return {
        "project": {"id": "fx", "title": "Fixture"},
        "player": {"core_traits": {"money": 10}},
        "locations": [{"id": "room_a"}],
        "npcs": [{"id": "npc_ray", "name": "Ray", "customizable": True},
                 {"id": "npc_ana", "name": "Ana"}],
        "canvases": [
            {"id": "ray_01", "name": "The first night", "description": "Arc step 1. The kitchen after ten.",
             "trigger": {"location": "room_a", "is_repeatable": False},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph",
                 "content": "Your mother is on until six. Your mother does not ask."}]}]},
        ],
    }


def run(tmp_path, monkeypatch, capsys, st, toml_text="", person=None):
    monkeypatch.setattr(pitch_pack.gates, "_load", lambda path: game())
    tp = tmp_path / "7_final_game.toml"
    tp.write_text(toml_text, encoding="utf-8")
    sp = tmp_path / "v2_state.json"
    sp.write_text(json.dumps(st), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert pitch_pack.pack("fx", str(tp), str(sp), person=person) == 0
    out = capsys.readouterr().out
    out = " ".join(out.split())
    return out[out.index("NAMING —"):out.index("THE WANT")], out


def test_kin_words_counted_and_unused_forms_named(tmp_path, monkeypatch, capsys):
    block, _ = run(tmp_path, monkeypatch, capsys, {})
    assert '"your mother" ×2' in block
    assert '"mum"' in block.split("never:")[1]


def test_renameable_person_gets_the_token_rule(tmp_path, monkeypatch, capsys):
    block, out = run(tmp_path, monkeypatch, capsys, {})
    assert "npc_ray → @ray" in block and "npc_ana →" not in block
    assert "prose writes @ray, never a typed name" in out


def test_declared_address_wins_over_the_comment(tmp_path, monkeypatch, capsys):
    st = {"board": {"characters": [{"id": "npc_ray", "address": "\"love\""}]}}
    block, out = run(tmp_path, monkeypatch, capsys, st,
                     toml_text="# the cast: ONE term of address each — Ray says \"pet\".\n")
    assert 'npc_ray calls her: "love"' in block
    assert "COMMENT" not in block
    assert 'calls her: "love"' in out


def test_comment_is_quoted_whole_paragraph_when_nothing_declared(tmp_path, monkeypatch, capsys):
    toml = ("# unrelated heading\n#\n# The register note: one subject per person, and ONE\n"
            "# term of address each — Ray says \"love\", Ana says nothing.\n#\n# Other stuff.\n")
    block, _ = run(tmp_path, monkeypatch, capsys, {}, toml_text=toml)
    assert "from a COMMENT" in block
    assert "The register note: one subject per person, and ONE term of address each" in block
    assert "Other stuff" not in block and "unrelated heading" not in block


def test_shipped_scene_listed_with_its_own_words(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, {}, person="npc_ray")
    assert "SCENES ALREADY SHIPPED" in out
    assert "ray_01 [id prefix] “The first night” — Arc step 1. The kitchen after ten." in out
