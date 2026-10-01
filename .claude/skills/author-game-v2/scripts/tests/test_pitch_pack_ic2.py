"""Fixtures for the pitch pack's her-moment sections (PRD_IDEAS_AND_CRAFT IC2, 2026-09-27).

The game is a minimal dict handed to `pitch_pack.pack` through a patched `gates._load`,
the state file and the moment library are written to a temp dir, and nothing in games/
is read or written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402

SECTIONS = ["THE PROMISE", "LAST LISTEN", "MOMENT KINDS ALREADY SHIPPED",
            "THE MOMENT LIBRARY", "CLIPS ON THE SHELF", "THE WANT", "PLACES", "PEOPLE"]

LIBRARY = """# The Moment Library

## firsts · her firsts

- **A — first** (`[p1]`) · "first quote"

## being_seen · being seen

- **B — seen one** (`[p2]`) · "seen quote one"
- **B — seen two** (`[p3]`) · "seen quote two"

## taboo_at_home · taboo at home

- **C — home** (`[p4]`) · "home quote"
"""


def game():
    return {
        "project": {"id": "fx", "title": "Fixture"},
        "player": {"core_traits": {"money": 10}},
        "locations": [{"id": "room_a"}],
        "npcs": [{"id": "npc_a", "name": "A"}],
        "canvases": [
            {"id": "c1", "trigger": {"location": "room_a", "npc": "npc_a",
                                     "is_repeatable": True},
             "nodes": [{"id": "n", "blocks": [
                 {"type": "video", "props": {"pool_dir": "sex/a_t5", "pool": 3}}]}]},
        ],
    }


def run(tmp_path, monkeypatch, capsys, state, kind=None):
    monkeypatch.setattr(pitch_pack.gates, "_load", lambda path: game())
    lib = tmp_path / "moment-library.md"
    lib.write_text(LIBRARY, encoding="utf-8")
    monkeypatch.setattr(pitch_pack, "LIBRARY_PATH", str(lib))
    sp = tmp_path / "v2_state.json"
    sp.write_text(json.dumps(state), encoding="utf-8")
    monkeypatch.chdir(tmp_path)          # no games/fx/output here, so no media on disk
    code = pitch_pack.pack("fx", "unused.toml", str(sp), kind=kind)
    return code, capsys.readouterr().out


def test_new_sections_print_first_and_in_order(tmp_path, monkeypatch, capsys):
    code, out = run(tmp_path, monkeypatch, capsys, {"want": {"appetite": "x"}})
    assert code == 0
    pos = [out.index(s) for s in SECTIONS]
    assert pos == sorted(pos), pos


def test_undeclared_fantasy_prints_not_declared(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, {"want": {}})
    block = out[out.index("THE PROMISE"):out.index("LAST LISTEN")]
    assert block.count("not declared") == 8          # IC14: + face, companion, pressure; W5: + threads


def test_declared_fantasy_prints_verbatim(tmp_path, monkeypatch, capsys):
    st = {"want": {"fantasy_shape": "mystery",
                   "promise": {"goal": "find her sister", "date": "day 30"}}}
    _, out = run(tmp_path, monkeypatch, capsys, st)
    block = out[out.index("THE PROMISE"):out.index("LAST LISTEN")]
    assert "mystery" in block and "goal: find her sister" in block
    assert block.count("not declared") == 6          # IC14: + face, companion, pressure; W5: + threads


def test_kinds_shipped_counts_and_three_least_used(tmp_path, monkeypatch, capsys):
    d = "2026-09-01"
    st = {"releases": [{"moment_kind": "firsts", "shipped": d}, {"moment_kind": "firsts", "shipped": d},
                       {"moment_kind": "being_seen", "shipped": d},
                       {"moment_kind": "consequence", "shipped": d},
                       {"subject": "old release, no kind", "shipped": d}]}
    counts, unrec, least = pitch_pack._kinds_shipped(st["releases"])
    assert counts["firsts"] == 2 and counts["being_seen"] == 1 and unrec == 1
    assert least == ["body_as_payment", "taboo_at_home", "being_seen"]
    _, out = run(tmp_path, monkeypatch, capsys, st)
    assert "unrecorded" in out
    assert "three least used: body_as_payment, taboo_at_home, being_seen" in out


def test_kind_prints_only_that_slice(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, {}, kind="being_seen")
    block = out[out.index("THE MOMENT LIBRARY"):out.index("CLIPS ON THE SHELF")]
    assert "seen quote one" in block and "seen quote two" in block
    assert "first quote" not in block and "home quote" not in block


def test_no_kind_and_unknown_kind_say_so(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, {})
    assert "no kind given" in out
    _, out = run(tmp_path, monkeypatch, capsys, {}, kind="bogus")
    assert "unknown kind `bogus`" in out


def test_clips_are_counted_per_person_and_zero_without_media(tmp_path, monkeypatch, capsys):
    _, out = run(tmp_path, monkeypatch, capsys, {})
    block = out[out.index("CLIPS ON THE SHELF"):out.index("THE WANT")]
    assert "no media on disk" in block
    assert "npc_a: sex/a_t5 0" in block
    # and with a media folder on disk
    d = tmp_path / "games" / "fx" / "output" / "media" / "sex" / "a_t5"
    d.mkdir(parents=True)
    for i in range(3):
        (d / f"{i}.webm").write_text("x")
    _, out = run(tmp_path, monkeypatch, capsys, {})
    block = out[out.index("CLIPS ON THE SHELF"):out.index("THE WANT")]
    assert "npc_a: sex/a_t5 3" in block
