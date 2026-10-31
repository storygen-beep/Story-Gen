"""
Turn the game client's WebSocket messages, as recorded by capture.py, into rounds.

Message format, from the first captures of 1x Andar Bahar (engine.livetables.io, 2026-10-31):

  {"MessageType":"Card", "roundId":..., "CardHand":"Joker"|"Andar"|"Bahar", "CardName":"6c", ...}
      one per card, in dealing order; the joker first
  {"MessageType":"GAME_RESULT", "roundId":..., "GameResults":{"WinningHand":"Bahar",
      "AndarCards":[...], "BaharCards":[...], "JokerCard":"6c"}, ...}
      the table's own summary at the end of the round

A round is built from the Card messages in the order they arrived, never reconstructed from
the GAME_RESULT lists: rebuilding the deal order from two lists would assume the alternation
the audit is meant to test. GAME_RESULT is the cross-check: the round is written only if its
joker, its Andar cards and its Bahar cards agree with the Card messages. Rounds joined part
way through, or whose messages disagree, are reported and left out.

The winner stored is the table's declared WinningHand, so the audit's integrity family can
compare it with the side the matching card actually went to.

Usage:
  python tools/parse.py data/live.sqlite            # parse, write rounds, print a summary
  python tools/parse.py data/live.sqlite --list     # also list every round for screenshot checks
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import dataclass, field

from common import Round, insert_round, open_db

RANKS = {"A": 1, "T": 10, "J": 11, "Q": 12, "K": 13, **{str(n): n for n in range(2, 10)}}
SUITS = {"s": "S", "h": "H", "d": "D", "c": "C"}
SIDES = {"Andar": "A", "Bahar": "B"}


def card(name: str) -> tuple[int, str]:
    """'6c' -> (6, 'C'); 'Th' -> (10, 'H')."""
    if len(name) != 2 or name[0] not in RANKS or name[1].lower() not in SUITS:
        raise ValueError(f"unrecognised card {name!r}")
    return RANKS[name[0]], SUITS[name[1].lower()]


@dataclass
class Pending:
    joker: str | None = None
    dealt: list[tuple[str, str]] = field(default_factory=list)  # (side, card name) in arrival order
    first_ts: float | None = None
    result: dict | None = None
    result_ts: float | None = None
    started_clean: bool = False   # saw the joker before any dealt card


def parse(conn: sqlite3.Connection, table_name: str = "1x Andar Bahar") -> tuple[list[Round], list[str]]:
    pending: dict[int, Pending] = {}
    for ts, payload in conn.execute("SELECT ts, payload FROM ws_frames WHERE direction = 'recv' ORDER BY id"):
        try:
            msg = json.loads(payload)
        except ValueError:
            continue
        rid = msg.get("roundId")
        kind = msg.get("MessageType")
        if rid is None or kind not in ("Card", "GAME_RESULT"):
            continue
        p = pending.setdefault(int(rid), Pending())
        if kind == "Card":
            hand = msg.get("CardHand")
            if hand == "Joker":
                p.joker = msg["CardName"]
                p.started_clean = not p.dealt
                p.first_ts = p.first_ts or ts
            elif hand in SIDES:
                p.dealt.append((SIDES[hand], msg["CardName"]))
                p.first_ts = p.first_ts or ts
        else:
            p.result = msg.get("GameResults") or {}
            p.result_ts = ts

    rounds, problems = [], []
    for rid, p in sorted(pending.items()):
        why = check(p)
        if why:
            problems.append(f"round {rid}: {why}")
            continue
        jr, js = card(p.joker)
        cards = [(side, *card(name)) for side, name in p.dealt]
        rounds.append(Round(
            round_id=str(rid), table_name=table_name, joker_rank=jr, joker_suit=js,
            cards=cards, first_side=cards[0][0], winner=SIDES[p.result["WinningHand"]],
            n_cards=len(cards), source="ws", ts_start=p.first_ts, ts_end=p.result_ts,
        ))
    return rounds, problems


def check(p: Pending) -> str | None:
    if p.result is None:
        return "no GAME_RESULT (capture ended mid-round, or the round was cancelled)"
    if p.joker is None or not p.started_clean:
        return "joined after the deal started; not all Card messages were seen"
    if not p.dealt:
        return "no dealt cards"
    r = p.result
    if r.get("JokerCard") != p.joker:
        return f"joker {p.joker} in Card messages, {r.get('JokerCard')} in GAME_RESULT"
    for side, key in (("A", "AndarCards"), ("B", "BaharCards")):
        seen = [name for s, name in p.dealt if s == side]
        if seen != list(r.get(key, [])):
            return f"{key} {r.get(key)} in GAME_RESULT, {seen} in Card messages"
    if r.get("WinningHand") not in SIDES:
        return f"unrecognised WinningHand {r.get('WinningHand')!r}"
    try:
        card(p.joker)
        for _, name in p.dealt:
            card(name)
    except ValueError as exc:
        return str(exc)
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("db")
    ap.add_argument("--table", default="1x Andar Bahar")
    ap.add_argument("--list", action="store_true", help="print every parsed round")
    a = ap.parse_args()

    conn = open_db(a.db)
    rounds, problems = parse(conn, a.table)
    for r in rounds:
        insert_round(conn, r)
    conn.commit()
    print(f"{len(rounds)} rounds parsed and written; {len(problems)} left out.")
    for line in problems:
        print("  left out: " + line)
    if a.list:
        names = {1: "A", 10: "T", 11: "J", 12: "Q", 13: "K"}
        for r in rounds:
            seq = " ".join(f"{s}:{names.get(k, k)}{u.lower()}" for s, k, u in r.cards)
            print(f"#{r.round_id}  joker {names.get(r.joker_rank, r.joker_rank)}{r.joker_suit.lower()}  "
                  f"winner {'Andar' if r.winner == 'A' else 'Bahar'}  {r.n_cards} cards  {seq}")


if __name__ == "__main__":
    main()
