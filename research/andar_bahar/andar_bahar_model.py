"""
Andar Bahar — exact probability model and bankroll simulation.

Phase 1 (game mathematics) and the parts of Phase 4/5 that follow directly from it.
Every number in PHASE1_REPORT.md is produced by this file. Run:

    python3 research/andar_bahar/andar_bahar_model.py

Model assumptions (standard single-deck online Andar Bahar):
  * 52-card deck, freshly shuffled every round.
  * One card (the "joker") is drawn and shown. 51 cards remain; exactly 3 of them
    share the joker's rank.
  * Cards are then dealt alternately to two piles, starting with the FIRST side
    (Andar on most online tables; on classic tables the joker's colour picks it).
  * The first card matching the joker's rank ends the round; its pile wins.
  * Main bets close before the first card is dealt.

Everything below is derived from those rules, not from any platform's claims.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, erf, sqrt

import numpy as np

# ----------------------------------------------------------------------------
# 1. Exact round model
# ----------------------------------------------------------------------------

def first_match_distribution(n_remaining: int, n_matching: int) -> list[Fraction]:
    """P(first matching card sits at position k), k = 1..n_remaining.

    The n_matching matching cards occupy a uniformly random 3-subset (in general an
    m-subset) of the n positions. The first match is at position k iff position k is
    a match and the remaining m-1 matches sit among the n-k positions after it.
    """
    total = comb(n_remaining, n_matching)
    dist = [Fraction(0)]  # index 0 unused
    for k in range(1, n_remaining + 1):
        ways = comb(n_remaining - k, n_matching - 1)
        dist.append(Fraction(ways, total))
    return dist


def side_probabilities(n_remaining: int = 51, n_matching: int = 3) -> tuple[Fraction, Fraction]:
    """(P first-dealt side wins, P second-dealt side wins)."""
    dist = first_match_distribution(n_remaining, n_matching)
    p_first = sum(dist[k] for k in range(1, n_remaining + 1) if k % 2 == 1)
    p_second = sum(dist[k] for k in range(1, n_remaining + 1) if k % 2 == 0)
    return p_first, p_second


def expected_value(p_win: Fraction, payout: Fraction) -> Fraction:
    """EV per 1 unit staked: win pays `payout` units net, loss costs 1 unit."""
    return p_win * payout - (1 - p_win)


def expected_cards(dist: list[Fraction]) -> Fraction:
    return sum(k * dist[k] for k in range(1, len(dist)))


def cdf_tail(dist: list[Fraction], at_least: int) -> Fraction:
    return sum(dist[k] for k in range(at_least, len(dist)))


# ----------------------------------------------------------------------------
# 2. Sample size needed to detect an exploitable bias
# ----------------------------------------------------------------------------

def rounds_to_detect_bias(p0: float, p1: float, alpha: float = 0.05, power: float = 0.9) -> int:
    """Rounds of observation to tell p1 from p0 (one-sided z-test, normal approx)."""
    # z-values for alpha (one-sided) and power
    def z(q: float) -> float:
        # inverse normal CDF via bisection on erf — fine for these purposes
        lo, hi = -10.0, 10.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if 0.5 * (1 + erf(mid / sqrt(2))) < q:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    za, zb = z(1 - alpha), z(power)
    num = (za * sqrt(p0 * (1 - p0)) + zb * sqrt(p1 * (1 - p1))) ** 2
    return int(np.ceil(num / (p1 - p0) ** 2))


# ----------------------------------------------------------------------------
# 3. Bankroll: exact reach probabilities
# ----------------------------------------------------------------------------

def flat_bet_reach_probability(bankroll: int, target: int, unit: int, p: float, payout: float = 1.0) -> float:
    """P(reach target before ruin) betting `unit` every round.

    Solved as an absorbing Markov chain on rupee states (vectorised value iteration).
    """
    win_gain = int(round(unit * payout))
    v = np.zeros(target + 1)
    v[target] = 1.0
    xs = np.arange(unit, target)
    up = np.minimum(target, xs + win_gain)
    down = xs - unit
    for _ in range(2_000_000):
        new = v.copy()
        new[xs] = p * v[up] + (1 - p) * v[down]
        if np.max(np.abs(new - v)) < 1e-13:
            v = new
            break
        v = new
    return float(v[bankroll])


def bold_play_reach_probability(bankroll: int, target: int, p: float, payout: float = 1.0) -> float:
    """Bold play: each round stake the whole bankroll, or just enough to hit the target.

    Dubins & Savage (1965) prove this maximises P(reach target) for a subfair
    even-money game; for payout 0.9 it is near-optimal. Solved on the reachable
    state graph by value iteration.
    """
    def stake(x: int) -> int:
        # stake s so that a win lands exactly on target when possible
        need = target - x
        s_for_target = int(np.ceil(need / payout))
        return min(x, s_for_target)

    reach: dict[int, float] = {}
    frontier = [bankroll]
    graph: dict[int, tuple[int, int]] = {}
    while frontier:
        x = frontier.pop()
        if x in graph or x <= 0 or x >= target:
            continue
        s = stake(x)
        up = min(target, x + int(np.floor(s * payout)))
        down = x - s
        graph[x] = (up, down)
        frontier.extend([up, down])
    v = {x: 0.0 for x in graph}
    for _ in range(100_000):
        delta = 0.0
        for x, (up, down) in graph.items():
            vu = 1.0 if up >= target else v.get(up, 0.0)
            vd = 0.0 if down <= 0 else v.get(down, 0.0)
            new = p * vu + (1 - p) * vd
            delta = max(delta, abs(new - v[x]))
            v[x] = new
        if delta < 1e-14:
            break
    return v[bankroll], len(graph)


# ----------------------------------------------------------------------------
# 4. Monte Carlo of betting progressions (vectorised across sessions)
# ----------------------------------------------------------------------------

def simulate(strategy: str, p: float, payout: float, bankroll: int = 500, target: int = 10_000,
             base: int = 10, min_bet: int = 10, max_bet: int = 10_000, sessions: int = 100_000,
             max_rounds: int = 50_000, seed: int = 20261030) -> dict:
    """Simulate `sessions` independent sessions of one strategy.

    Returns reach probabilities for 1000/2500/5000/10000, ruin probability, median
    rounds, and mean maximum drawdown. A session ends on reaching target, on
    having less than min_bet, or at max_rounds (reported as 'unresolved').
    """
    rng = np.random.default_rng(seed)
    bank = np.full(sessions, float(bankroll))
    peak = bank.copy()
    max_dd = np.zeros(sessions)
    alive = np.ones(sessions, dtype=bool)
    rounds = np.zeros(sessions, dtype=np.int64)
    reached = {m: np.zeros(sessions, dtype=bool) for m in (1000, 2500, 5000, 10_000)}
    # progression state
    level = np.zeros(sessions, dtype=np.int64)          # martingale / fibonacci index
    dalembert_units = np.ones(sessions, dtype=np.int64)
    fib = [1, 1]
    while fib[-1] * base < max_bet * 4:
        fib.append(fib[-1] + fib[-2])
    fib = np.array(fib)

    for _ in range(max_rounds):
        if not alive.any():
            break
        idx = np.flatnonzero(alive)
        b = bank[idx]
        if strategy == "flat":
            stake = np.full(idx.size, float(base))
        elif strategy == "bold":
            need = np.ceil((target - b) / payout)
            stake = np.minimum(b, need)
        elif strategy == "martingale":
            stake = base * (2.0 ** level[idx])
        elif strategy == "reverse_martingale":
            stake = base * (2.0 ** level[idx])
        elif strategy == "fibonacci":
            stake = base * fib[np.minimum(level[idx], fib.size - 1)].astype(float)
        elif strategy == "dalembert":
            stake = base * dalembert_units[idx].astype(float)
        else:
            raise ValueError(strategy)
        stake = np.minimum(stake, max_bet)
        stake = np.minimum(stake, b)                     # cannot bet more than you have
        bust_now = stake < min_bet
        win = rng.random(idx.size) < p
        delta = np.where(win, np.floor(stake * payout), -stake)
        delta[bust_now] = 0.0
        nb = b + delta
        bank[idx] = nb
        rounds[idx] += 1
        # drawdown
        peak[idx] = np.maximum(peak[idx], nb)
        max_dd[idx] = np.maximum(max_dd[idx], (peak[idx] - nb) / peak[idx])
        # progression updates
        if strategy == "martingale":
            level[idx] = np.where(win, 0, level[idx] + 1)
        elif strategy == "reverse_martingale":
            # press winnings; reset after a loss or after 3 straight wins
            level[idx] = np.where(win, np.where(level[idx] >= 3, 0, level[idx] + 1), 0)
        elif strategy == "fibonacci":
            level[idx] = np.where(win, np.maximum(level[idx] - 2, 0), level[idx] + 1)
        elif strategy == "dalembert":
            dalembert_units[idx] = np.where(win, np.maximum(dalembert_units[idx] - 1, 1),
                                            dalembert_units[idx] + 1)
        for m in reached:
            reached[m][idx] |= nb >= m
        done = (nb >= target) | (nb < min_bet) | bust_now
        alive[idx[done]] = False

    final = bank
    return {
        "strategy": strategy,
        "p_reach": {m: float(reached[m].mean()) for m in reached},
        "p_ruin": float((final < min_bet).mean()),
        "p_unresolved": float(alive.mean()),
        "median_rounds": float(np.median(rounds)),
        "mean_rounds": float(rounds.mean()),
        "mean_max_drawdown": float(max_dd.mean()),
        "mean_final": float(final.mean()),
    }


# ----------------------------------------------------------------------------
# 5. Report
# ----------------------------------------------------------------------------

def pct(x) -> str:
    return f"{float(x) * 100:.4f}%"


def main() -> None:
    print("=" * 78)
    print("ANDAR BAHAR — EXACT MODEL (single deck, reshuffled every round)")
    print("=" * 78)

    dist = first_match_distribution(51, 3)
    p_first, p_second = side_probabilities()
    print(f"P(first-dealt side wins)  = {p_first} = {pct(p_first)}")
    print(f"P(second-dealt side wins) = {p_second} = {pct(p_second)}")
    print(f"Edge of first side over second = {p_first - p_second} = {pct(p_first - p_second)}")

    print("\n-- Round length (cards dealt after the joker) --")
    ec = expected_cards(dist)
    print(f"Expected cards dealt = {ec} = {float(ec):.4f}")
    print(f"Maximum cards dealt  = {max(k for k in range(1, 52) if dist[k] > 0)}")
    print(f"P(match on card 1)   = {dist[1]} = {pct(dist[1])}")
    print(f"P(round ends within 5 cards)  = {pct(1 - cdf_tail(dist, 6))}")
    print(f"P(round ends within 13 cards) = {pct(1 - cdf_tail(dist, 14))}")
    print(f"P(>= 26 cards) = {pct(cdf_tail(dist, 26))}")
    print(f"P(>= 41 cards) = {pct(cdf_tail(dist, 41))}")
    print(f"P(>= 45 cards) = {pct(cdf_tail(dist, 45))}")
    print("Range buckets used by common side bets:")
    for lo, hi in [(1, 5), (6, 10), (11, 15), (16, 25), (26, 30), (31, 35), (36, 40), (41, 49)]:
        pr = sum(dist[k] for k in range(lo, hi + 1))
        fair = (1 - pr) / pr
        print(f"  {lo:>2}-{hi:<2} cards: P = {pct(pr):>9}   fair payout = {float(fair):.2f}:1")

    print("\n-- Expected value and house edge per 1 unit staked --")
    for label, pwin in (("first side ", p_first), ("second side", p_second)):
        for payout in (Fraction(1), Fraction(19, 20), Fraction(9, 10), Fraction(17, 20)):
            ev = expected_value(pwin, payout)
            print(f"  {label} pays {float(payout):.2f}:1  EV = {float(ev):+.5f}  house edge = {pct(-ev)}")

    print("\n-- Does the joker's rank matter? --")
    print("  Single deck: every rank has exactly 3 other cards -> identical distribution for")
    print("  every joker rank. The rank carries zero information about Andar vs Bahar.")
    print("  Joker colour matters only on tables where colour picks the first-dealt side,")
    print("  and then it only tells you WHICH side has the 26/51 — a fact already priced in.")

    print("\n-- Multi-deck variants: P(first side) with d decks --")
    for d in (1, 2, 4, 6, 8):
        pf, ps = side_probabilities(52 * d - 1, 4 * d - 1)
        print(f"  {d} deck(s): first = {pct(pf)}  second = {pct(ps)}  (first-side edge {pct(pf - ps)})")

    print("\n-- Card removal WITHOUT reshuffle (continuous shoe, hypothetical) --")
    print("  If a platform did NOT reshuffle between rounds, the count of the joker's rank")
    print("  already gone would change the odds. Single deck, n cards left, m matching left:")
    for n, m in ((51, 3), (40, 3), (30, 3), (20, 3), (10, 3), (40, 2), (30, 2), (20, 2), (10, 2), (40, 1), (20, 1), (9, 1)):
        pf, ps = side_probabilities(n, m)
        print(f"  n={n:>2} m={m}: first = {pct(pf):>9}  second = {pct(ps):>9}")
    print("  (m=1 gives exactly (n+1)/(2n) for odd n: that is where the folk '26/51' comes from.)")

    print("\n-- In-round conditional odds (relevant only to tables with a second bet) --")
    print("  After k non-matching cards dealt, P(the NEXT pile to receive a card wins):")
    for k in (0, 2, 4, 10, 20, 30, 40):
        pf, ps = side_probabilities(51 - k, 3)
        print(f"  k={k:>2}: next pile {pct(pf):>9}, other pile {pct(ps):>9}")

    print("\n-- Bias needed for a +EV bet, and rounds needed to detect it --")
    p_be_first = 1 / 1.9
    print(f"  First side at 0.9:1 is +EV only if P(first) > {p_be_first:.4%} (true value {float(p_first):.4%}).")
    print(f"  Second side at 1:1 is +EV only if P(second) > 50% (true value {float(p_second):.4%}).")
    for p1 in (0.50, 0.52, 0.53, 0.55):
        n = rounds_to_detect_bias(float(p_second), p1)
        print(f"  Detect P(second) = {p1:.2f} vs fair {float(p_second):.4f} at alpha 5%, power 90%: ~{n:,} rounds")

    print("\n" + "=" * 78)
    print("REACH PROBABILITIES: Rs 500 -> Rs 10,000")
    print("=" * 78)
    pf, ps = float(p_first), float(p_second)
    print(f"Fair-game ceiling (zero house edge, any strategy): 500/10000 = {pct(0.05)}")
    for label, p, payout in ((f"second side 1:1 (house edge {pct(-expected_value(p_second, Fraction(1)))})", ps, 1.0),
                             (f"first side 0.9:1 (house edge {pct(-expected_value(p_first, Fraction(9, 10)))})", pf, 0.9),
                             ("first side 1:1 (if a table paid it)", pf, 1.0)):
        pb, nstates = bold_play_reach_probability(500, 10_000, p, payout)
        print(f"Bold play, {label}: {pct(pb)}  ({nstates} reachable bankroll states)")
    for unit in (10, 50, 100, 250):
        pr = flat_bet_reach_probability(500, 10_000, unit, ps, 1.0)
        print(f"Flat Rs {unit:>3} on second side at 1:1: {pct(pr)}")

    print("\n-- Monte Carlo, 100,000 sessions per strategy, bet limits Rs 10 .. Rs 10,000 --")
    print(f"Second side at 1:1, P(win) = {p_second}:")
    header = f"{'strategy':<20}{'P>=1000':>10}{'P>=2500':>10}{'P>=5000':>10}{'P=10000':>10}{'ruin':>9}{'unres':>8}{'med rounds':>12}{'avg maxDD':>11}"
    print(header)
    for s in ("flat", "bold", "martingale", "reverse_martingale", "fibonacci", "dalembert"):
        r = simulate(s, ps, 1.0, base=10)
        pr = r["p_reach"]
        print(f"{s:<20}{pr[1000]:>10.4f}{pr[2500]:>10.4f}{pr[5000]:>10.4f}{pr[10000]:>10.4f}"
              f"{r['p_ruin']:>9.4f}{r['p_unresolved']:>8.4f}{r['median_rounds']:>12.0f}{r['mean_max_drawdown']:>11.3f}")
    print(f"\nFirst side at 0.9:1, P(win) = {p_first}:")
    print(header)
    for s in ("flat", "bold", "martingale", "fibonacci", "dalembert"):
        r = simulate(s, pf, 0.9, base=10)
        pr = r["p_reach"]
        print(f"{s:<20}{pr[1000]:>10.4f}{pr[2500]:>10.4f}{pr[5000]:>10.4f}{pr[10000]:>10.4f}"
              f"{r['p_ruin']:>9.4f}{r['p_unresolved']:>8.4f}{r['median_rounds']:>12.0f}{r['mean_max_drawdown']:>11.3f}")

    print("\n-- Sensitivity: bold play on second side at 1:1 under a hypothetical bias --")
    for p in (ps, 0.50, 0.51, 0.52, 0.55, 0.60):
        pb, _ = bold_play_reach_probability(500, 10_000, p, 1.0)
        print(f"  P(win) = {p:.4f}: reach = {pct(pb)}")

    print("\n-- Kelly criterion --")
    for label, p, payout in (("second side 1:1", ps, 1.0), ("first side 0.9:1", pf, 0.9)):
        f = (p * payout - (1 - p)) / payout
        print(f"  {label}: f* = (p*b - q)/b = {f:+.5f}  -> negative, Kelly says bet nothing.")


if __name__ == "__main__":
    main()
