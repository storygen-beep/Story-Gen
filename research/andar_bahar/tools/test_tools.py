"""
Tests for the Phase 6 tools. Run from research/andar_bahar:

    .venv/bin/python -m pytest tools -q
"""
from __future__ import annotations

import ast
import http.server
import socket
import threading
from fractions import Fraction
from pathlib import Path

import pytest

import audit
import decide
from common import ONE_X_ANDAR_BAHAR, open_db, insert_round, load_rounds
from make_synthetic import generate

TOOLS = Path(__file__).resolve().parent
FAMILIES = ["1 winner", "2 cards", "3 joker", "4 sequence", "5 integrity"]


def verdicts(rounds):
    return {r.family: r.verdict for r in audit.audit(rounds, ONE_X_ANDAR_BAHAR.name)}


# ---------------------------------------------------------------------------
# capture.py has no path to any bet control
# ---------------------------------------------------------------------------

FORBIDDEN = {"click", "dblclick", "tap", "fill", "type", "press", "press_sequentially",
             "check", "uncheck", "select_option", "set_input_files", "drag_to", "dispatch_event",
             "mouse", "keyboard", "touchscreen", "hover", "focus"}


def test_capture_never_interacts():
    tree = ast.parse((TOOLS / "capture.py").read_text())
    used = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert not used & FORBIDDEN, f"capture.py uses {used & FORBIDDEN}"
    # No script evaluation that could click from inside the page either.
    src = (TOOLS / "capture.py").read_text()
    for needle in (".click(", "dispatchEvent", "MouseEvent", "PointerEvent"):
        assert needle not in src


# ---------------------------------------------------------------------------
# Synthetic data: the generator follows the rules and the audit behaves (Phase 7 steps 1-2)
# ---------------------------------------------------------------------------

def test_generator_obeys_rules():
    rounds = generate(2000, seed=7)
    assert all(not audit.integrity_problems(r, "B") for r in rounds)


def test_fair_data_passes():
    assert set(verdicts(generate(10_000, seed=1)).values()) == {"pass"}


def test_three_point_bias_caught():
    v = verdicts(generate(10_000, seed=2, bias_pp=3))
    assert v["1 winner"] == "FAIL"
    assert v["5 integrity"] == "pass"


def test_order_error_caught():
    v = verdicts(generate(10_000, seed=3, order_error=0.05))
    assert v["5 integrity"] == "FAIL"


def test_store_round_trip(tmp_path):
    conn = open_db(tmp_path / "t.sqlite")
    rounds = generate(50, seed=4)
    for r in rounds:
        insert_round(conn, r)
    conn.commit()
    back = load_rounds(conn)
    assert [r.round_id for r in back] == [r.round_id for r in rounds]
    assert back[0].cards == rounds[0].cards


def test_audit_refuses_small_samples(tmp_path, capsys):
    db = tmp_path / "small.sqlite"
    conn = open_db(db)
    for r in generate(299, seed=5):
        insert_round(conn, r)
    conn.commit()
    import sys
    sys.argv = ["audit.py", str(db)]
    assert audit.main() == 2
    assert "300" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# decide.py computes SKIP from the model, and the model matches Ezugi's published RTP
# ---------------------------------------------------------------------------

PUBLISHED_RTP = {"Andar": 96.99, "Bahar": 97.86, "cards 1-5": 94.86, "cards 6-10": 97.68,
                 "cards 11-15": 92.96, "cards 16-25": 98.10, "cards 26-30": 91.45,
                 "cards 31-35": 92.48, "cards 36-40": 94.97, "cards 41-49": 95.20}


def test_pricing_matches_published_rtp():
    for p in decide.price_from_model(ONE_X_ANDAR_BAHAR):
        assert abs((1 + p.ev) * 100 - PUBLISHED_RTP[p.bet.name]) < 0.14, p.bet.name


def test_model_says_skip():
    priced = decide.price_from_model(ONE_X_ANDAR_BAHAR)
    assert all(p.ev < 0 for p in priced)
    assert decide.recommend(priced, ONE_X_ANDAR_BAHAR).startswith("SKIP")


def test_skip_is_computed_not_hardcoded():
    # A paytable that overpays Bahar must flip the output, at the table minimum only.
    from dataclasses import replace
    generous = replace(ONE_X_ANDAR_BAHAR, bets=tuple(
        replace(b, payout=Fraction(1)) if b.name == "Bahar" else b for b in ONE_X_ANDAR_BAHAR.bets))
    out = decide.recommend(decide.price_from_model(generous), generous)
    assert out.startswith("REVIEW") and "₹100" in out


def test_use_audit_ignores_log_when_winner_passes():
    rounds = generate(1000, seed=6)
    priced, why = decide.pricing_for(ONE_X_ANDAR_BAHAR, rounds, use_audit=True)
    assert "passes" in why and all(p.source == "model" for p in priced)


# ---------------------------------------------------------------------------
# capture.py sees a WebSocket and the text inside a cross-origin iframe
# (the 1xBet page embeds the game from play.livetables.io the same way)
# ---------------------------------------------------------------------------

def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.mark.integration
def test_capture_reads_cross_origin_iframe(tmp_path):
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    from capture import Recorder

    http_port, ws_port = free_port(), free_port()
    site = tmp_path / "site"
    site.mkdir()
    # Top page on "localhost", game on "127.0.0.1": different sites, like 1xBet and livetables.
    (site / "top.html").write_text(
        f'<html><body>casino page<iframe src="http://127.0.0.1:{http_port}/game.html" '
        f'width="600" height="300"></iframe></body></html>')
    (site / "game.html").write_text(
        f'<html><body><div id="f">waiting</div><script>'
        f'const ws = new WebSocket("ws://127.0.0.1:{ws_port}");'
        f'ws.onmessage = e => {{ document.getElementById("f").innerText = "round #17392604276 " + e.data; }};'
        f'</script></body></html>')

    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(site), **k)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", http_port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    from websockets.sync.server import serve

    def ws_handler(conn):
        conn.send('{"joker":"9H","cards":["8D","3D"],"SessionId":"secret"}')
        conn.send(b"\x00\x01video")
        try:
            conn.recv(timeout=5)
        except Exception:
            pass

    ws_server = serve(ws_handler, "127.0.0.1", ws_port)
    threading.Thread(target=ws_server.serve_forever, daemon=True).start()

    rec = Recorder(tmp_path / "cap.sqlite", tmp_path / "shots", game_host="127.0.0.1", ws_host="127.0.0.1")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.on("websocket", rec.attach)
        page.goto(f"http://localhost:{http_port}/top.html")
        for _ in range(20):
            rec.poll(page)
            page.wait_for_timeout(250)
        browser.close()
    httpd.shutdown()
    ws_server.shutdown()

    frames = rec.conn.execute("SELECT url_host, direction, payload FROM ws_frames").fetchall()
    # Identity fields are stripped and binary frames are reduced to their length.
    assert ("127.0.0.1", "recv", '{"joker":"9H","cards":["8D","3D"]}') in frames
    assert ("127.0.0.1", "recv", "binary:7 bytes") in frames
    assert not any("secret" in p for *_, p in frames)
    texts = [t for (t,) in rec.conn.execute("SELECT text FROM dom_snapshots")]
    assert any("#17392604276" in t for t in texts)
    assert rec.round_ids == ["17392604276"]
    assert (tmp_path / "shots" / "17392604276.png").exists()


def test_capture_ignores_other_sockets_and_sent_frames(tmp_path):
    from capture import Recorder

    class FakeWS:
        def __init__(self, url):
            self.url, self.handlers = url, {}

        def on(self, event, fn):
            self.handlers[event] = fn

    rec = Recorder(tmp_path / "c.sqlite", tmp_path / "shots", "livetables")
    video = FakeWS("wss://muma-mdpz-e01.ezvds.net/x")
    game = FakeWS("wss://engine.livetables.io/x")
    rec.attach(video)
    rec.attach(game)
    assert video.handlers == {}
    assert set(game.handlers) == {"framereceived"}


# ---------------------------------------------------------------------------
# parse.py: one real round from the 2026-10-31 capture (round 17400256227, identity fields removed)
# ---------------------------------------------------------------------------

REAL_ROUND = [
    {"MessageType": "Card", "roundId": 17400256227, "CardHand": "Joker", "CardName": "6c"},
    *[{"MessageType": "Card", "roundId": 17400256227, "CardHand": h, "CardName": c}
      for h, c in [("Bahar", "9h"), ("Andar", "3c"), ("Bahar", "As"), ("Andar", "Kd"), ("Bahar", "3d"),
                   ("Andar", "Ah"), ("Bahar", "Th"), ("Andar", "Qh"), ("Bahar", "6d")]],
    {"MessageType": "GAME_RESULT", "roundId": 17400256227, "GameResults": {
        "RoundId": 17400256227, "WinningHand": "Bahar", "AndarCards": ["3c", "Kd", "Ah", "Qh"],
        "BaharCards": ["9h", "As", "3d", "Th", "6d"], "JokerCard": "6c"}},
]


def frames_db(tmp_path, messages):
    import json
    conn = open_db(tmp_path / "f.sqlite")
    for i, m in enumerate(messages):
        conn.execute("INSERT INTO ws_frames (ts, url_host, direction, payload) VALUES (?,?,?,?)",
                     (1000.0 + i, "engine.livetables.io", "recv", json.dumps(m)))
    return conn


def test_parse_real_round(tmp_path):
    import parse
    rounds, problems = parse.parse(frames_db(tmp_path, REAL_ROUND))
    assert problems == []
    (r,) = rounds
    assert (r.joker_rank, r.joker_suit, r.winner, r.n_cards, r.first_side) == (6, "C", "B", 9, "B")
    assert r.cards[0] == ("B", 9, "H") and r.cards[-1] == ("B", 6, "D")
    assert not audit.integrity_problems(r, "B")


def test_parse_rejects_partial_and_mismatched_rounds(tmp_path):
    import copy
    import parse
    joined_late = REAL_ROUND[3:]                       # missed the joker and two cards
    mismatch = copy.deepcopy(REAL_ROUND)
    mismatch[-1]["GameResults"]["BaharCards"][0] = "9d"
    for i, msgs in enumerate((joined_late, mismatch, REAL_ROUND[:-1])):
        case_dir = tmp_path / f"case{i}"
        case_dir.mkdir()
        rounds, problems = parse.parse(frames_db(case_dir, msgs))
        assert rounds == [] and len(problems) == 1
