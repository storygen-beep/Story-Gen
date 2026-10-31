"""
Highest probability of turning ₹500 into ₹10,000 on a table, choosing freely among ALL its
bets each round (one bet per round), with the table's real minimum stake.

Phase 5 solved bold play on the 0.9:1 main bet only. On 1x Andar Bahar the cards-dealt bet
"16-25" has a smaller house edge (1.90%) than Bahar (2.15%) and pays 3.5:1, so it has to be
in the optimisation. This script solves it exactly as a Markov decision problem by value
iteration, on a ₹10 grid (bankrolls and stakes in ₹10 steps; winnings rounded down to the
grid, which can only understate the probability slightly).

Limits of the model: one bet per round (combinations of cards-dealt bets in the same
round are not searched); stakes on a ₹10 grid; no table maximum is reached from ₹500.

Usage: python tools/optimal_reach.py [--bankroll 500] [--target 10000]
"""
from __future__ import annotations

import argparse

import numpy as np

from common import TABLES

GRID = 10


def solve(table, allowed: list[str], target: int) -> np.ndarray:
    """v[i] = max P(reach target) from bankroll i * GRID."""
    n = target // GRID
    min_units = table.min_stake // GRID
    bets = [(float(table.p_win(b)), float(b.payout)) for b in table.bets if b.name in allowed]
    xs = np.arange(n + 1)
    v = np.zeros(n + 1)
    v[n] = 1.0
    for _ in range(1000):
        best = v.copy()
        for p, pay in bets:
            for s in range(min_units, n):
                x = xs[s:n]
                up = np.minimum(n, x + int(np.floor(s * pay)))
                best[s:n] = np.maximum(best[s:n], p * v[up] + (1 - p) * v[x - s])
        if np.max(np.abs(best - v)) < 1e-13:
            return best
        v = best
    return v


def best_action(table, v: np.ndarray, bankroll: int, target: int) -> tuple[str, int, float]:
    n, xu = target // GRID, bankroll // GRID
    best = (-1.0, "", 0)
    for b in table.bets:
        p, pay = float(table.p_win(b)), float(b.payout)
        for s in range(table.min_stake // GRID, xu + 1):
            val = p * v[min(n, xu + int(np.floor(s * pay)))] + (1 - p) * v[xu - s]
            if val > best[0] + 1e-12:
                best = (val, b.name, s * GRID)
    return best[1], best[2], best[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", default="1x Andar Bahar", choices=sorted(TABLES))
    ap.add_argument("--bankroll", type=int, default=500)
    ap.add_argument("--target", type=int, default=10_000)
    a = ap.parse_args()
    table = TABLES[a.table]
    names = [b.name for b in table.bets]
    i = a.bankroll // GRID

    print(f"{table.name}: P(₹{a.bankroll} reaches ₹{a.target:,}), minimum stake ₹{table.min_stake}, ₹{GRID} grid")
    for name in names:
        print(f"  only {name:<12} {solve(table, [name], a.target)[i]:8.4%}")
    v = solve(table, names, a.target)
    print(f"  any bet, best each round {v[i]:8.4%}")
    print("Optimal first bets along the way:")
    for x in (a.bankroll, 2 * a.bankroll, 2250, 5000, 9000):
        if x < a.target:
            name, stake, val = best_action(table, v, x, a.target)
            print(f"  bankroll ₹{x:>6,}: {name:<12} stake ₹{stake:>6,}  P(reach) {val:.4%}")


if __name__ == "__main__":
    main()
