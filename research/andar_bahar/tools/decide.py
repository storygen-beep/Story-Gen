"""
Decision support (Phase 6, component 4): expected value of every bet, computed per round.

For each bet on the table: win probability, payout, EV per ₹1 staked. The recommendation
is SKIP unless some bet has EV > 0. It is computed every time, never hard-coded, so the
day an input changes the output changes with it.

Where the win probability comes from:
  * By default, the exact model (andar_bahar_model.py), validated against the provider's
    published RTP. Under it every bet on this table has negative EV, so the output is SKIP.
  * With --use-audit, and ONLY if audit.py's winner family has failed on the log, the main
    bets are priced from the log instead: a Beta(1 + wins, 1 + losses) posterior, read at
    its conservative 0.5% / 99.5% bound, not its mean. Cards-dealt bets stay on the model.
    A failed audit is far more likely to be a capture error than an edge (see audit.py),
    so even then a positive EV is flagged for review, not acted on.

What this tool never does: size a stake above the table minimum, raise a stake after a
loss, or treat a run of results as making the next one more likely. Its stake output,
when there is one, is the table minimum. It has no connection to the casino.

Usage:
  python tools/decide.py                                   # EV table, no log needed
  python tools/decide.py --db data/live.sqlite             # one line per logged round
  python tools/decide.py --db data/live.sqlite --follow    # wait for new rounds
  python tools/decide.py --db data/live.sqlite --use-audit
"""
from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from fractions import Fraction

from scipy import stats

import audit as audit_mod
from common import TABLES, Bet, Table, load_rounds, open_db

CONSERVATIVE_Q = 0.005


@dataclass
class Priced:
    bet: Bet
    p_win: float
    ev: float          # per ₹1 staked
    source: str


def price_from_model(table: Table) -> list[Priced]:
    out = []
    for bet in table.bets:
        p = table.p_win(bet)
        ev = p * bet.payout - (1 - p)
        out.append(Priced(bet, float(p), float(ev), "model"))
    return out


def price_from_log(table: Table, rounds) -> list[Priced]:
    """Main bets from a conservative bound on the log's posterior; side bets from the model."""
    n = len(rounds)
    wins_first = sum(r.winner == table.first_side for r in rounds)
    a, b = 1 + wins_first, 1 + n - wins_first
    out = []
    for pr in price_from_model(table):
        if pr.bet.side is None:
            out.append(pr)
            continue
        if pr.bet.side == table.first_side:
            p = float(stats.beta.ppf(CONSERVATIVE_Q, a, b))
        else:
            p = 1 - float(stats.beta.ppf(1 - CONSERVATIVE_Q, a, b))
        ev = p * float(pr.bet.payout) - (1 - p)
        out.append(Priced(pr.bet, p, ev, f"log, {n} rounds, {CONSERVATIVE_Q:.1%} bound"))
    return out


def recommend(priced: list[Priced], table: Table) -> str:
    best = max(priced, key=lambda x: x.ev)
    if best.ev <= 0:
        return f"SKIP  (best bet {best.bet.name}, EV {best.ev:+.2%} per ₹1; no bet has positive EV)"
    return (f"REVIEW  {best.bet.name} shows EV {best.ev:+.2%} per ₹1 ({best.source}). "
            f"Do not bet on this output alone: re-check capture against screenshots first. "
            f"Stake, if ever, the table minimum ₹{table.min_stake}.")


def ev_table(priced: list[Priced]) -> str:
    rows = [f"  {'bet':<13}{'pays':>8}{'P(win)':>10}{'EV per ₹1':>11}{'RTP':>9}  source"]
    for p in priced:
        rows.append(f"  {p.bet.name:<13}{float(p.bet.payout):>7.2f}:1{p.p_win:>10.4%}"
                    f"{p.ev:>+11.2%}{1 + p.ev:>9.2%}  {p.source}")
    return "\n".join(rows)


def pricing_for(table: Table, rounds, use_audit: bool) -> tuple[list[Priced], str]:
    if use_audit and len(rounds) >= audit_mod.MIN_ROUNDS:
        winner = audit_mod.test_winner(rounds, table.first_side)
        if winner.verdict == "FAIL":
            return price_from_log(table, rounds), "audit winner family FAILED; main bets priced from the log"
        return price_from_model(table), "audit winner family passes; model pricing"
    if use_audit:
        return price_from_model(table), f"fewer than {audit_mod.MIN_ROUNDS} rounds; model pricing"
    return price_from_model(table), "model pricing"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", default="1x Andar Bahar", choices=sorted(TABLES))
    ap.add_argument("--db", help="SQLite log from capture.py")
    ap.add_argument("--follow", action="store_true", help="keep polling the log for new rounds")
    ap.add_argument("--use-audit", action="store_true")
    ap.add_argument("--last", type=int, default=20, help="rounds to show when not following")
    a = ap.parse_args()
    table = TABLES[a.table]

    if not a.db:
        priced, why = pricing_for(table, [], False)
        print(f"{table.name}: first card to {table.first_side}, stakes ₹{table.min_stake}–₹{table.max_stake:,}. {why}.")
        print(ev_table(priced))
        print(recommend(priced, table))
        return

    conn = open_db(a.db)
    seen: set[str] = set()
    first_pass = True
    while True:
        rounds = load_rounds(conn, table.name)
        new = [r for r in rounds if r.round_id not in seen]
        if first_pass and not a.follow:
            new = new[-a.last:]
        if new:
            priced, why = pricing_for(table, rounds, a.use_audit)
            if first_pass:
                print(f"{table.name}: {why}.")
                print(ev_table(priced))
            for r in new:
                seen.add(r.round_id)
                # The decision for the NEXT round is made from what was known after this one.
                print(f"after round {r.round_id} (winner {r.winner}, {r.n_cards} cards): next round "
                      + recommend(priced, table))
        elif first_pass:
            print(f"{table.name}: no rounds logged yet.")
        first_pass = False
        if not a.follow:
            break
        seen.update(r.round_id for r in rounds)
        time.sleep(2)


if __name__ == "__main__":
    main()
