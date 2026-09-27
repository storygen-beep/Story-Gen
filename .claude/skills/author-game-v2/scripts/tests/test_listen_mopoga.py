"""Fixtures for listen_mopoga.py (PRD_IDEAS_AND_CRAFT IC3, loop step 8). The network is never
touched: `fetch` is patched with a thread shaped like the study's saved mopoga JSON. Nothing in
games/ is written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import listen_mopoga  # noqa: E402

JAN_2026 = 1767225600.0          # 2026-01-01 UTC
THREAD = {"id": None, "total_replies": 3, "replies": [
    {"id": "1", "created": str(JAN_2026 - 86400), "likes": "50", "text": "<p>old: where is the cheat code?</p>",
     "replies": []},
    {"id": "2", "created": str(JAN_2026 + 86400), "likes": "3", "text": "<p>I love this game, please add more</p>",
     "replies": [{"id": "3", "created": str(JAN_2026 + 2 * 86400), "likes": "9",
                  "text": "<p>how do I get the kitchen scene? I&#39;m stuck</p>", "replies": []}]},
]}


def setup_game(tmp_path, sources):
    os.makedirs(tmp_path / "games" / "fx")
    (tmp_path / "games" / "fx" / "v2_state.json").write_text(
        json.dumps({"listen_sources": sources} if sources is not None else {}), encoding="utf-8")


def test_no_page_declared_says_so_and_exits_zero(tmp_path, monkeypatch, capsys):
    setup_game(tmp_path, None)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(listen_mopoga, "fetch", lambda p: (_ for _ in ()).throw(AssertionError("fetched")))
    assert listen_mopoga.main(["fx", "--since", "2026-01-01"]) == 0
    assert "no mopoga page declared" in capsys.readouterr().out


def test_since_filter_likes_order_and_buckets(tmp_path, monkeypatch, capsys):
    setup_game(tmp_path, {"mopoga": "fx-game"})
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(listen_mopoga, "fetch", lambda page: THREAD)
    dump = tmp_path / "scratch" / "out.json"
    os.makedirs(dump.parent)
    assert listen_mopoga.main(["fx", "--since", "2026-01-01", "--out", str(dump)]) == 0
    out = capsys.readouterr().out
    assert "2 of 3 comment(s)" in out
    assert out.index("mopoga#3") < out.index("mopoga#2")          # 9 likes before 3 likes
    assert "mopoga#1" not in out                                  # before --since
    data = json.loads(dump.read_text())
    assert [c["id"] for c in data["comments"]] == ["3", "2"]
    counts = listen_mopoga.buckets(data["comments"])
    assert counts["how / where / stuck"] == 1 and counts["praise"] == 1 and counts["request"] == 1
    assert counts["cheat / code"] == 0
    assert os.listdir(tmp_path / "games" / "fx") == ["v2_state.json"]   # nothing written in games/


def test_refuses_to_write_under_games(tmp_path, monkeypatch, capsys):
    setup_game(tmp_path, {"mopoga": "fx-game"})
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(listen_mopoga, "fetch", lambda page: THREAD)
    assert listen_mopoga.main(["fx", "--since", "2026-01-01", "--out", "games/fx/dump.json"]) == 0
    assert "refusing to write under games/" in capsys.readouterr().out
    assert not os.path.exists(tmp_path / "games" / "fx" / "dump.json")


def test_network_error_is_reported_not_raised(tmp_path, monkeypatch, capsys):
    setup_game(tmp_path, {"mopoga": "fx-game"})
    monkeypatch.chdir(tmp_path)

    def boom(page):
        raise OSError("no route to host")
    monkeypatch.setattr(listen_mopoga, "fetch", boom)
    assert listen_mopoga.main(["fx", "--since", "2026-01-01"]) == 0
    assert "fetch failed: no route to host" in capsys.readouterr().out
