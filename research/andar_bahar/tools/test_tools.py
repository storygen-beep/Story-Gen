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
        conn.send('{"joker":"9H","cards":["8D","3D"]}')
        try:
            conn.recv(timeout=5)
        except Exception:
            pass

    ws_server = serve(ws_handler, "127.0.0.1", ws_port)
    threading.Thread(target=ws_server.serve_forever, daemon=True).start()

    rec = Recorder(tmp_path / "cap.sqlite", tmp_path / "shots", game_host="127.0.0.1")
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
    assert ("127.0.0.1", "recv", '{"joker":"9H","cards":["8D","3D"]}') in frames
    texts = [t for (t,) in rec.conn.execute("SELECT text FROM dom_snapshots")]
    assert any("#17392604276" in t for t in texts)
    assert rec.round_ids == ["17392604276"]
    assert (tmp_path / "shots" / "17392604276.png").exists()
