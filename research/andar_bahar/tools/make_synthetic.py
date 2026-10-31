"""
Generate Andar Bahar rounds from the rules, for testing audit.py (Phase 7).

Each round shuffles a real 52-card deck, draws the joker, and deals alternately starting
with the table's first side until the first card of the joker's rank. A fair run is
therefore the model itself, card by card, not a draw from the summary probabilities.

Optional faults, so the audit can be shown to catch them:

  --bias PP          shift the first side's win rate up by PP percentage points
                     (by re-dealing a fraction of second-side wins; the deck stays real)
  --order-error R    in a fraction R of rounds the first card goes to the wrong side,
                     as a dealer or a scanner would if it mixed up the deal order

Usage:
  python tools/make_synthetic.py --rounds 10000 --out data/fair.sqlite --seed 1
  python tools/make_synthetic.py --rounds 10000 --bias 3 --out data/bias3.sqlite
  python tools/make_synthetic.py --rounds 10000 --order-error 0.05 --out data/order.sqlite
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path

from common import (P_FIRST_SIDE, RANKS, SUITS, TABLES, Round, insert_round, open_db)


def other(side: str) -> str:
    return "A" if side == "B" else "B"


def deal_round(rng: random.Random, first_side: str) -> tuple[tuple[int, str], list[tuple[str, int, str]]]:
    deck = [(r, s) for r in RANKS for s in SUITS]
    rng.shuffle(deck)
    joker = deck[0]
    cards = []
    side = first_side
    for rank, suit in deck[1:]:
        cards.append((side, rank, suit))
        if rank == joker[0]:
            break
        side = other(side)
    return joker, cards


def generate(n_rounds: int, table_name: str = "1x Andar Bahar", seed: int | None = None,
             bias_pp: float = 0.0, order_error: float = 0.0) -> list[Round]:
    table = TABLES[table_name]
    rng = random.Random(seed)
    p0 = float(P_FIRST_SIDE)
    target = p0 + bias_pp / 100
    if not 0 < target < 1:
        raise ValueError("bias pushes the win rate outside (0, 1)")
    # Keep every first-side win; keep a second-side win with probability `keep`.
    # Then P(first side wins) = p0 / (p0 + (1 - p0) * keep) = target.
    keep = 1.0 if bias_pp <= 0 else p0 * (1 - target) / (target * (1 - p0))
    if bias_pp < 0:
        raise ValueError("negative bias not supported; swap the table's first side instead")

    rounds = []
    t = 1_700_000_000.0
    while len(rounds) < n_rounds:
        dealt_first = table.first_side
        if order_error and rng.random() < order_error:
            dealt_first = other(table.first_side)
        joker, cards = deal_round(rng, dealt_first)
        winner = cards[-1][0]
        if winner != table.first_side and keep < 1.0 and rng.random() > keep:
            continue  # re-deal: this is how the bias enters
        i = len(rounds)
        rounds.append(Round(
            round_id=f"syn{i:06d}", table_name=table_name,
            joker_rank=joker[0], joker_suit=joker[1], cards=cards,
            first_side=cards[0][0], winner=winner, n_cards=len(cards),
            source="synthetic", ts_start=t + 45 * i, ts_end=t + 45 * i + 30,
        ))
    return rounds


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rounds", type=int, default=10_000)
    ap.add_argument("--table", default="1x Andar Bahar", choices=sorted(TABLES))
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--bias", type=float, default=0.0, help="percentage points added to the first side's win rate")
    ap.add_argument("--order-error", type=float, default=0.0, help="fraction of rounds dealt from the wrong side")
    ap.add_argument("--out", required=True, help="SQLite file to write (replaced if it exists)")
    a = ap.parse_args()

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    conn = open_db(out)
    for r in generate(a.rounds, a.table, a.seed, a.bias, a.order_error):
        insert_round(conn, r)
    conn.commit()
    print(f"wrote {a.rounds} rounds to {out} (bias {a.bias} points, order error {a.order_error})")


if __name__ == "__main__":
    main()
