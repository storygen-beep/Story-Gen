"""
Observe a live Andar Bahar table and record what the game client receives (Phase 6, component 1).

Read-only by construction. This file contains no call that clicks, types, presses a key,
moves the mouse or fills a field; tests/test_tools.py checks that on every run. It never
sees credentials: the first time, you log in by hand in the browser window it opens, and
the login persists in a profile folder under data/.

What it records, into one SQLite file:
  ws_frames      every text frame RECEIVED on the game's WebSocket (host containing
                 --ws-host, default engine.livetables.io). First capture, 2026-10-31: this
                 socket carries JSON per round ("MessageType", "roundId", ...).
                 Not recorded: frames the browser sends (they carry the session token,
                 session id and IP), and every other socket, including the video stream on
                 *.ezvds.net, whose binary frames swamped the first run. Identity fields
                 (see REDACT_KEYS) are removed from received JSON before it is stored.
  dom_snapshots  the visible text of the game frame whenever it changes (every 0.5 s poll),
                 the fallback when frames turn out not to carry round data.
  data/shots/    one screenshot of the game frame per round id seen in the footer, for
                 checking logged rounds against the screen (Phase 7 step 3).

The `rounds` table is filled by a parser written against the frames from the first
capture, not by guessing their format in advance.

Usage:
  python tools/capture.py                         # opens 1x Andar Bahar, runs until Ctrl+C
  python tools/capture.py --minutes 120 --db data/live.sqlite
  python tools/capture.py --channel chrome        # use installed Google Chrome, not Chromium
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Frame, Page, WebSocket, sync_playwright

from common import RESEARCH_DIR, open_db

DEFAULT_URL = "https://1-x-bet-india.com/en/casino-search?game=63587"
DEFAULT_GAME_HOST = "livetables"   # the game iframe is served from play.livetables.io
DEFAULT_WS_HOST = "engine.livetables.io"
# Fields that identify the player or the session. The audit needs none of them.
REDACT_KEYS = {"CurrentPlayerToken", "SessionId", "ClientIp", "ClientId", "Token", "token",
               "sessionId", "playerId", "PlayerId", "Nickname", "nickname", "UserName", "userName"}
ROUND_ID = re.compile(r"#(\d{8,})")
POLL_SECONDS = 0.5
DATA_DIR = RESEARCH_DIR / "data"


class Recorder:
    def __init__(self, db_path: Path, shots_dir: Path, game_host: str,
                 ws_host: str = DEFAULT_WS_HOST):
        self.conn = open_db(db_path)
        self.shots_dir = shots_dir
        self.shots_dir.mkdir(parents=True, exist_ok=True)
        self.game_host = game_host
        self.ws_host = ws_host
        self._shot_error_reported = False
        self.frames = 0
        self.snapshots = 0
        self.round_ids: list[str] = []
        self._last_text_hash = ""

    # -- WebSocket ---------------------------------------------------------

    def attach(self, ws: WebSocket) -> None:
        host = urlparse(ws.url).hostname or "?"
        if self.ws_host not in host:
            return  # video stream, chat, odds feeds: not round data
        print(f"websocket opened: {host}")
        ws.on("framereceived", lambda payload: self._frame(host, payload))

    def _frame(self, host: str, payload: str | bytes) -> None:
        if isinstance(payload, bytes):
            payload = f"binary:{len(payload)} bytes"
        else:
            payload = redact(payload)
        self.conn.execute("INSERT INTO ws_frames (ts, url_host, direction, payload) VALUES (?,?,?,?)",
                          (time.time(), host, "recv", payload))
        self.frames += 1

    # -- DOM fallback ------------------------------------------------------

    def game_frame(self, page: Page) -> Frame | None:
        for frame in page.frames:
            if self.game_host in (urlparse(frame.url).hostname or ""):
                return frame
        return None

    def poll(self, page: Page) -> None:
        frame = self.game_frame(page)
        if frame is None:
            return
        try:
            text = frame.evaluate("() => document.body ? document.body.innerText : ''")
        except Exception:
            return  # frame navigating or detached; next poll retries
        digest = hashlib.sha1(text.encode()).hexdigest()
        if digest == self._last_text_hash:
            return
        self._last_text_hash = digest
        shot = None
        ids = ROUND_ID.findall(text)
        if ids and (not self.round_ids or ids[-1] != self.round_ids[-1]):
            self.round_ids.append(ids[-1])
            shot = self._screenshot(page, ids[-1])
        self.conn.execute("INSERT INTO dom_snapshots (ts, frame_host, text, screenshot) VALUES (?,?,?,?)",
                          (time.time(), urlparse(frame.url).hostname or "?", text, shot))
        self.snapshots += 1

    def _screenshot(self, page: Page, round_id: str) -> str | None:
        path = self.shots_dir / f"{round_id}.png"
        try:
            # A clip of the page, not an element screenshot: an element screenshot waits for
            # the element to be "stable", which a frame playing video may never be.
            box = page.locator(f'iframe[src*="{self.game_host}"]').first.bounding_box(timeout=3000)
            if box is None:
                raise RuntimeError("game frame has no box (hidden or scrolled away)")
            page.screenshot(path=str(path), clip=box, timeout=10_000)
            return str(path)
        except Exception as exc:
            if not self._shot_error_reported:
                print(f"screenshot failed for #{round_id}: {exc!r} (further failures not printed)")
                self._shot_error_reported = True
            return None


def redact(payload: str) -> str:
    """Drop identity fields from a JSON frame; non-JSON text is kept as it is."""
    try:
        data = json.loads(payload)
    except ValueError:
        return payload

    def strip(x):
        if isinstance(x, dict):
            return {k: strip(v) for k, v in x.items() if k not in REDACT_KEYS}
        if isinstance(x, list):
            return [strip(v) for v in x]
        return x
    return json.dumps(strip(data), separators=(",", ":"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--db", default=str(DATA_DIR / "live.sqlite"))
    ap.add_argument("--profile", default=str(DATA_DIR / "chromium_profile"),
                    help="persistent browser profile; your login is kept here, not in this code")
    ap.add_argument("--game-host", default=DEFAULT_GAME_HOST, help="host of the game iframe (DOM poll)")
    ap.add_argument("--ws-host", default=DEFAULT_WS_HOST, help="only WebSockets to this host are recorded")
    ap.add_argument("--minutes", type=float, default=0, help="stop after this long (0 = until Ctrl+C)")
    ap.add_argument("--channel", default=None, help="'chrome' to use installed Google Chrome")
    a = ap.parse_args()

    db_path = Path(a.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    rec = Recorder(db_path, db_path.parent / "shots", a.game_host, a.ws_host)
    deadline = time.time() + a.minutes * 60 if a.minutes else None

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(a.profile, headless=False, channel=a.channel,
                                                    no_viewport=True)
        # Every tab of this browser is listened to, including ones opened after start; the DOM
        # poll follows the first tab, so keep the table in that tab.
        ctx.on("page", lambda p: p.on("websocket", rec.attach))
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for p in ctx.pages:
            p.on("websocket", rec.attach)
        page.goto(a.url)
        print("Browser open. If you are not logged in, log in by hand in that window and open the "
              "table; recording starts as soon as the game frame appears. Ctrl+C here to stop.")
        last_report = time.time()
        try:
            while deadline is None or time.time() < deadline:
                rec.poll(page)
                rec.conn.commit()
                if time.time() - last_report >= 30:
                    last = rec.round_ids[-1] if rec.round_ids else "none yet"
                    print(f"{time.strftime('%H:%M:%S')}  frames {rec.frames}  snapshots {rec.snapshots}  "
                          f"rounds seen {len(rec.round_ids)} (last #{last})")
                    last_report = time.time()
                page.wait_for_timeout(POLL_SECONDS * 1000)
        except KeyboardInterrupt:
            pass
        finally:
            rec.conn.commit()
            print(f"stopped. {rec.frames} frames, {rec.snapshots} snapshots, "
                  f"{len(rec.round_ids)} round ids, written to {db_path}")
            ctx.close()


if __name__ == "__main__":
    main()
