"""
Audit a log of Andar Bahar rounds against the validated model (Phase 6, component 3).

The tests, thresholds and minimum sample are fixed here, before any live data exists,
so that nothing is chosen after looking at the results. They are the five families of
PHASE5_6_SIMULATION_AND_ARCHITECTURE.md:

  1 winner     first side's win share against 429/833, exact two-sided binomial test
  2 cards      number of cards dealt against the exact distribution, chi-square on the
               table's eight cards-dealt buckets; top buckets merged downward until every
               expected count is at least 5
  3 joker      joker rank against uniform over 13 ranks, chi-square
  4 sequence   independence of the winner sequence: Wald-Wolfowitz runs test and
               Ljung-Box on lags 1 to 5, Bonferroni-combined inside the family
  5 integrity  rule checks on every round: 52 distinct cards, the deal alternates from the
               stated first side, the round stops at the first card of the joker's rank,
               the declared winner is the side of that card, 1 <= n_cards <= 49.
               Any violation fails the family; it is not a statistical test.

Overall alpha 0.01, Bonferroni across the five families: each statistical family fails
at p < 0.002. No verdict is printed below 300 rounds.

A failed family means the log does not fit the model. It does not by itself mean
manipulation: a capture bug, a wrong table definition or a misread card produce the
same signal, and are checked first (Phase 7 step 3).

Usage:
  python tools/audit.py data/rounds.sqlite [--table "1x Andar Bahar"] [--json]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass

import numpy as np
from scipy import stats

from common import (CARD_BUCKETS, DIST, MAX_CARDS, P_FIRST_SIDE, TABLES, Round,
                    load_rounds, open_db, rank_name)

ALPHA_OVERALL = 0.01
N_FAMILIES = 5
ALPHA_FAMILY = ALPHA_OVERALL / N_FAMILIES
MIN_ROUNDS = 300
MIN_EXPECTED = 5.0
POWER = 0.9
LJUNG_BOX_LAGS = 5


@dataclass
class Result:
    family: str
    test: str
    statistic: str
    p_value: float | None
    verdict: str
    detail: str = ""
    rounds_to_resolve: int | None = None


# ---------------------------------------------------------------------------
# Rounds needed to resolve a borderline result
# ---------------------------------------------------------------------------

def rounds_for_chi2(n: int, stat: float, df: int, alpha: float = ALPHA_FAMILY) -> int | None:
    """Rounds at which an effect of the observed size would be detected with 90% power.

    The observed effect size is w^2 = (stat - df) / n (the expected excess over noise).
    Detection needs a noncentrality lambda with P(chi2_df(lambda) > critical) = POWER;
    rounds = lambda / w^2. None when the observed statistic is no larger than noise.
    """
    if stat <= df:
        return None
    w2 = (stat - df) / n
    crit = stats.chi2.ppf(1 - alpha, df)
    lo, hi = 0.0, 1e4
    for _ in range(100):
        mid = (lo + hi) / 2
        if stats.ncx2.sf(crit, df, mid) < POWER:
            lo = mid
        else:
            hi = mid
    return int(math.ceil(hi / w2))


def rounds_for_binomial(p0: float, p1: float, alpha: float = ALPHA_FAMILY) -> int | None:
    if p1 == p0:
        return None
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(POWER)
    num = (za * math.sqrt(p0 * (1 - p0)) + zb * math.sqrt(p1 * (1 - p1))) ** 2
    return int(math.ceil(num / (p1 - p0) ** 2))


def verdict(p: float) -> str:
    return "FAIL" if p < ALPHA_FAMILY else "pass"


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------

def test_winner(rounds: list[Round], first_side: str) -> Result:
    n = len(rounds)
    k = sum(r.winner == first_side for r in rounds)
    p0 = float(P_FIRST_SIDE)
    p = stats.binomtest(k, n, p0, alternative="two-sided").pvalue
    share = k / n
    need = rounds_for_binomial(p0, share) if p >= ALPHA_FAMILY else None
    return Result("1 winner", "exact binomial, two-sided",
                  f"{first_side} won {k}/{n} = {share:.4%} (model {p0:.4%})",
                  p, verdict(p), rounds_to_resolve=need)


def merged_buckets(n: int) -> list[tuple[int, int, float]]:
    """Table buckets with their model probability, top buckets merged until expected >= 5."""
    buckets = [(lo, hi, float(sum(DIST[k] for k in range(lo, hi + 1)))) for lo, hi in CARD_BUCKETS]
    while len(buckets) > 2 and buckets[-1][2] * n < MIN_EXPECTED:
        lo, _, p_prev = buckets[-2]
        _, hi, p_last = buckets[-1]
        buckets[-2:] = [(lo, hi, p_prev + p_last)]
    return buckets


def test_cards(rounds: list[Round]) -> Result:
    n = len(rounds)
    buckets = merged_buckets(n)
    obs = np.array([sum(lo <= r.n_cards <= hi for r in rounds) for lo, hi, _ in buckets], float)
    exp = np.array([p * n for *_, p in buckets])
    # Rounds outside 1..49 are integrity failures; keep the chi-square on the valid ones.
    exp *= obs.sum() / exp.sum()
    stat, p = stats.chisquare(obs, exp)
    df = len(buckets) - 1
    labels = ", ".join(f"{lo}-{hi}:{int(o)}/{e:.0f}" for (lo, hi, _), o, e in zip(buckets, obs, exp))
    need = rounds_for_chi2(n, stat, df) if p >= ALPHA_FAMILY else None
    return Result("2 cards", f"chi-square, {len(buckets)} buckets",
                  f"chi2 = {stat:.2f}, df = {df}", float(p), verdict(p),
                  detail="observed/expected " + labels, rounds_to_resolve=need)


def test_joker(rounds: list[Round]) -> Result:
    n = len(rounds)
    obs = np.array([sum(r.joker_rank == k for r in rounds) for k in range(1, 14)], float)
    stat, p = stats.chisquare(obs)
    need = rounds_for_chi2(n, stat, 12) if p >= ALPHA_FAMILY else None
    detail = " ".join(f"{rank_name(k)}:{int(o)}" for k, o in zip(range(1, 14), obs))
    return Result("3 joker", "chi-square, 13 ranks", f"chi2 = {stat:.2f}, df = 12",
                  float(p), verdict(p), detail=f"expected {n / 13:.1f} each; " + detail,
                  rounds_to_resolve=need)


def runs_test(x: np.ndarray) -> tuple[float, float]:
    n1 = int(x.sum())
    n0 = len(x) - n1
    if n0 == 0 or n1 == 0:
        return float("nan"), 0.0
    runs = 1 + int(np.count_nonzero(x[1:] != x[:-1]))
    n = n0 + n1
    mu = 2 * n0 * n1 / n + 1
    var = 2 * n0 * n1 * (2 * n0 * n1 - n) / (n * n * (n - 1))
    z = (runs - mu) / math.sqrt(var)
    return z, 2 * stats.norm.sf(abs(z))


def ljung_box(x: np.ndarray, lags: int) -> tuple[float, float, list[float]]:
    n = len(x)
    y = x - x.mean()
    denom = float(np.dot(y, y))
    acs = [float(np.dot(y[:-k], y[k:]) / denom) for k in range(1, lags + 1)]
    q = n * (n + 2) * sum(r * r / (n - k) for k, r in enumerate(acs, start=1))
    return q, float(stats.chi2.sf(q, lags)), acs


def test_sequence(rounds: list[Round], first_side: str) -> Result:
    x = np.array([r.winner == first_side for r in rounds], dtype=float)
    z, p_runs = runs_test(x)
    q, p_lb, acs = ljung_box(x, LJUNG_BOX_LAGS)
    p = min(1.0, 2 * min(p_runs, p_lb))
    ac_txt = ", ".join(f"lag{k} {a:+.3f}" for k, a in enumerate(acs, start=1))
    need = None
    if p >= ALPHA_FAMILY:
        need = rounds_for_chi2(len(x), q, LJUNG_BOX_LAGS, ALPHA_FAMILY / 2)
    return Result("4 sequence", "runs test + Ljung-Box lags 1-5",
                  f"runs z = {z:+.2f} (p {p_runs:.3g}); Q = {q:.2f} (p {p_lb:.3g})",
                  p, verdict(p), detail="autocorrelation " + ac_txt, rounds_to_resolve=need)


def integrity_problems(r: Round, first_side: str) -> list[str]:
    problems = []
    if not r.cards:
        return ["no cards dealt"]
    all_cards = [(r.joker_rank, r.joker_suit)] + [(c[1], c[2]) for c in r.cards]
    if len(set(all_cards)) != len(all_cards):
        problems.append("a card appears twice")
    if r.first_side != first_side or r.cards[0][0] != first_side:
        problems.append(f"first card to {r.cards[0][0]}, table deals first to {first_side}")
    if any(r.cards[i][0] == r.cards[i - 1][0] for i in range(1, len(r.cards))):
        problems.append("deal does not alternate")
    matches = [i for i, c in enumerate(r.cards) if c[1] == r.joker_rank]
    if not matches:
        problems.append("no card of the joker's rank was dealt")
    elif matches[0] != len(r.cards) - 1:
        problems.append("deal continued past the first matching card")
    if len(all_cards) and max(sum(c[0] == k for c in all_cards) for k in range(1, 14)) > 4:
        problems.append("a rank appears more than four times")
    if r.winner != r.cards[-1][0]:
        problems.append(f"declared winner {r.winner}, last card went to {r.cards[-1][0]}")
    if r.n_cards != len(r.cards) or not 1 <= r.n_cards <= MAX_CARDS:
        problems.append(f"n_cards {r.n_cards} with {len(r.cards)} cards logged")
    return problems


def test_integrity(rounds: list[Round], first_side: str) -> Result:
    bad = []
    for r in rounds:
        probs = integrity_problems(r, first_side)
        if probs:
            bad.append((r.round_id, probs))
    kinds: dict[str, int] = {}
    for _, probs in bad:
        for pr in probs:
            key = pr.split(",")[0] if pr.startswith("first card") else pr
            kinds[key] = kinds.get(key, 0) + 1
    detail = "; ".join(f"{k}: {v}" for k, v in sorted(kinds.items()))
    if bad:
        examples = ", ".join(rid for rid, _ in bad[:5])
        detail += f". First rounds affected: {examples}"
    return Result("5 integrity", "rule checks on every round",
                  f"{len(bad)} of {len(rounds)} rounds violate the rules",
                  None, "FAIL" if bad else "pass", detail=detail)


# ---------------------------------------------------------------------------

def audit(rounds: list[Round], table_name: str) -> list[Result]:
    first_side = TABLES[table_name].first_side
    return [
        test_winner(rounds, first_side),
        test_cards(rounds),
        test_joker(rounds),
        test_sequence(rounds, first_side),
        test_integrity(rounds, first_side),
    ]


def render(results: list[Result], n: int, table_name: str) -> str:
    lines = [f"Audit of {n} rounds, table '{table_name}'.",
             f"Overall alpha {ALPHA_OVERALL}, Bonferroni over {N_FAMILIES} families: "
             f"a statistical family fails at p < {ALPHA_FAMILY}.", ""]
    for r in results:
        p = "n/a (rule check)" if r.p_value is None else f"{r.p_value:.4g}"
        lines.append(f"[{r.verdict:>4}] {r.family:<12} {r.test}")
        lines.append(f"       {r.statistic}; p = {p}")
        if r.detail:
            lines.append(f"       {r.detail}")
        if r.rounds_to_resolve:
            lines.append(f"       an effect of the observed size would need about "
                         f"{r.rounds_to_resolve:,} rounds to detect with 90% power")
    failed = [r.family for r in results if r.verdict == "FAIL"]
    lines.append("")
    if failed:
        lines.append("RESULT: the log does not fit the model in " + ", ".join(failed) + ". "
                     "Check capture and table definition before reading this as a property of the game.")
    else:
        lines.append("RESULT: no family rejects the model. The log is consistent with a fair "
                     "single-deck deal under the published rules.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("db")
    ap.add_argument("--table", default="1x Andar Bahar", choices=sorted(TABLES))
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    a = ap.parse_args()

    rounds = load_rounds(open_db(a.db), a.table)
    if len(rounds) < MIN_ROUNDS:
        print(f"{len(rounds)} rounds logged for '{a.table}'. The audit reports nothing below "
              f"{MIN_ROUNDS} rounds (pre-registered). {MIN_ROUNDS - len(rounds)} more needed.")
        return 2
    results = audit(rounds, a.table)
    if a.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        print(render(results, len(rounds), a.table))
    return 1 if any(r.verdict == "FAIL" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
