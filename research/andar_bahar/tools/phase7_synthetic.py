"""
Phase 7, steps 1 and 2: how often the audit fails on fair data, and how often it catches
the two injected faults, at several sample sizes.

  fair         rounds dealt exactly by the rules
  bias +3      first side's win rate raised by 3 percentage points
  order 5%     5% of rounds dealt starting from the wrong side

Each cell is the share of independent replicates in which the audit's overall result
was FAIL (any family). On fair data that share is the false-alarm rate and should sit
at or below the 1% overall alpha.

Usage: python tools/phase7_synthetic.py [--reps 100]
"""
from __future__ import annotations

import argparse

import audit
from common import ONE_X_ANDAR_BAHAR
from make_synthetic import generate

SIZES = (300, 1000, 3000, 10_000)
CASES = {"fair": {}, "bias +3": {"bias_pp": 3.0}, "order 5%": {"order_error": 0.05}}


def fail_rate(n: int, kwargs: dict, reps: int, seed0: int) -> tuple[float, dict[str, float]]:
    any_fail = 0
    by_family: dict[str, int] = {}
    for rep in range(reps):
        results = audit.audit(generate(n, seed=seed0 + rep, **kwargs), ONE_X_ANDAR_BAHAR.name)
        failed = [r.family for r in results if r.verdict == "FAIL"]
        any_fail += bool(failed)
        for f in failed:
            by_family[f] = by_family.get(f, 0) + 1
    return any_fail / reps, {f: c / reps for f, c in sorted(by_family.items())}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=100)
    a = ap.parse_args()
    print(f"Share of {a.reps} replicates where the audit FAILS (overall alpha {audit.ALPHA_OVERALL})")
    print(f"{'case':<10}" + "".join(f"{n:>12,}" for n in SIZES))
    detail = []
    for ci, (case, kwargs) in enumerate(CASES.items()):
        row = f"{case:<10}"
        for n in SIZES:
            rate, fams = fail_rate(n, kwargs, a.reps, seed0=100_000 * (ci + 1) + n)
            row += f"{rate:>12.0%}"
            detail.append(f"  {case} at {n:,}: " + (", ".join(f"{f} {r:.0%}" for f, r in fams.items()) or "no family failed"))
        print(row)
    print("Families that failed:")
    print("\n".join(detail))


if __name__ == "__main__":
    main()
