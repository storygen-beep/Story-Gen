"""
Shared pieces for the Phase 6 tools: the SQLite store, the observed table's paytable,
and the exact model probabilities every tool tests or prices against.

Nothing here talks to the casino. The paytable values come from the game screen of
"1x Andar Bahar" (game 63587), read 2026-10-31, and match Table A in
PHASE2_PROVIDERS_REPORT.md section 10.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

# The model lives one folder up; reuse it rather than copying its mathematics.
RESEARCH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RESEARCH_DIR))

from andar_bahar_model import first_match_distribution, side_probabilities  # noqa: E402

# ---------------------------------------------------------------------------
# Exact model
# ---------------------------------------------------------------------------

# DIST[k] = P(the first card matching the joker is the k-th card dealt), k = 1..49.
# Positions 50 and 51 have probability 0: three matches cannot all sit after position 49.
DIST: list[Fraction] = first_match_distribution(51, 3)
MAX_CARDS = 49
P_FIRST_SIDE, P_SECOND_SIDE = side_probabilities(51, 3)  # 429/833, 404/833

RANKS = range(1, 14)  # 1 = A, 11 = J, 12 = Q, 13 = K
SUITS = "SHDC"
RANK_NAMES = {1: "A", 11: "J", 12: "Q", 13: "K"}


def rank_name(rank: int) -> str:
    return RANK_NAMES.get(rank, str(rank))


# ---------------------------------------------------------------------------
# Table definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Bet:
    name: str
    payout: Fraction          # net units paid per unit staked on a win
    win_cards: tuple[int, int] | None = None  # inclusive n_cards range for cards-dealt bets
    side: str | None = None   # "A" or "B" for main bets


@dataclass(frozen=True)
class Table:
    name: str
    first_side: str           # side that receives the first card after the joker
    min_stake: int
    max_stake: int
    bets: tuple[Bet, ...]

    def p_win(self, bet: Bet) -> Fraction:
        """Model probability that `bet` wins on a fair round of this table."""
        if bet.side is not None:
            return P_FIRST_SIDE if bet.side == self.first_side else P_SECOND_SIDE
        lo, hi = bet.win_cards
        return sum(DIST[k] for k in range(lo, hi + 1))


ONE_X_ANDAR_BAHAR = Table(
    name="1x Andar Bahar",
    first_side="B",
    min_stake=100,
    max_stake=200_000,
    bets=(
        Bet("Andar", Fraction(1), side="A"),
        Bet("Bahar", Fraction(9, 10), side="B"),
        Bet("cards 1-5", Fraction(5, 2), win_cards=(1, 5)),
        Bet("cards 6-10", Fraction(7, 2), win_cards=(6, 10)),
        Bet("cards 11-15", Fraction(9, 2), win_cards=(11, 15)),
        Bet("cards 16-25", Fraction(7, 2), win_cards=(16, 25)),
        Bet("cards 26-30", Fraction(14), win_cards=(26, 30)),
        Bet("cards 31-35", Fraction(24), win_cards=(31, 35)),
        Bet("cards 36-40", Fraction(49), win_cards=(36, 40)),
        Bet("cards 41-49", Fraction(119), win_cards=(41, 49)),
    ),
)

TABLES = {"1x Andar Bahar": ONE_X_ANDAR_BAHAR}

# Card-count buckets the audit tests, taken from the table's own cards-dealt bets.
CARD_BUCKETS = [b.win_cards for b in ONE_X_ANDAR_BAHAR.bets if b.win_cards]

# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS rounds (
    round_id    TEXT NOT NULL,
    table_name  TEXT NOT NULL,
    ts_start    REAL,
    ts_end      REAL,
    joker_rank  INTEGER NOT NULL,
    joker_suit  TEXT NOT NULL,
    cards_json  TEXT NOT NULL,   -- ordered [[side, rank, suit], ...] dealt after the joker
    first_side  TEXT NOT NULL,   -- side that received the first dealt card
    winner      TEXT NOT NULL,   -- side the table declared the winner
    n_cards     INTEGER NOT NULL,
    source      TEXT NOT NULL,   -- 'ws', 'dom', 'manual' or 'synthetic'
    PRIMARY KEY (table_name, round_id)
);
-- Raw WebSocket frames from the game client, kept verbatim so the round parser can be
-- written (and re-run) against what the client actually received.
CREATE TABLE IF NOT EXISTS ws_frames (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         REAL NOT NULL,
    url_host   TEXT NOT NULL,
    direction  TEXT NOT NULL,    -- 'recv' or 'sent'
    payload    TEXT NOT NULL
);
-- DOM fallback: text of the game frame each time it changes, plus the screenshot taken then.
CREATE TABLE IF NOT EXISTS dom_snapshots (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         REAL NOT NULL,
    frame_host TEXT NOT NULL,
    text       TEXT NOT NULL,
    screenshot TEXT
);
"""


def open_db(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.executescript(SCHEMA)
    return conn


@dataclass
class Round:
    round_id: str
    table_name: str
    joker_rank: int
    joker_suit: str
    cards: list[tuple[str, int, str]]
    first_side: str
    winner: str
    n_cards: int
    source: str
    ts_start: float | None = None
    ts_end: float | None = None


def insert_round(conn: sqlite3.Connection, r: Round) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO rounds VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (r.round_id, r.table_name, r.ts_start, r.ts_end, r.joker_rank, r.joker_suit,
         json.dumps(r.cards), r.first_side, r.winner, r.n_cards, r.source),
    )


def load_rounds(conn: sqlite3.Connection, table_name: str | None = None) -> list[Round]:
    sql = ("SELECT round_id, table_name, joker_rank, joker_suit, cards_json, first_side, winner,"
           " n_cards, source, ts_start, ts_end FROM rounds")
    args: tuple = ()
    if table_name:
        sql += " WHERE table_name = ?"
        args = (table_name,)
    # Order by start time when known, else by insertion order: the independence tests
    # depend on the sequence being the order the rounds were played.
    sql += " ORDER BY COALESCE(ts_start, 0), rowid"
    out = []
    for row in conn.execute(sql, args):
        out.append(Round(row[0], row[1], row[2], row[3],
                         [tuple(c) for c in json.loads(row[4])],
                         row[5], row[6], row[7], row[8], row[9], row[10]))
    return out
