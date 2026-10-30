"""
Phase 5 on the real tables: reach probabilities for Rs 500 -> Rs 10,000 using the
parameters read off the 1xBet tables on 2026-10-30.

Table E  Ezugi standard / 1x Andar Bahar: bet Bahar, P(win) = 429/833, pays 0.9:1.
         Evolution Super Andar Bahar is identical with Andar as the 0.9:1 side.
         Limits taken as min Rs 20 (ElCasino's published minimum; Ezugi minimum not captured,
         parametrised), max Rs 500,000.
Table U  Ezugi Ultimate: bet Bahar, pays 0.9:1, 20% fee on stake, multiplier on a winning bet
         with an ASSUMED distribution calibrated to Ezugi's published 97.82% RTP:
         with probability q the win is multiplied by M uniform on {2, 3, 5}; q solves
         1 + q*(E[M]-1) = 1.421. The true draw distribution is unpublished; this is a
         sensitivity case, not a claim about the game.

Run: python3 table_simulation.py
"""
import numpy as np

from andar_bahar_model import bold_play_reach_probability, flat_bet_reach_probability, side_probabilities, simulate

P_FIRST, _ = side_probabilities(51, 3)
p = float(P_FIRST)

print("=" * 80)
print("TABLE E  Ezugi standard (Bahar 0.9:1) / Evolution Super (Andar 0.9:1), P(win) = 51.5006%")
print("=" * 80)
pb, _ = bold_play_reach_probability(500, 10_000, p, 0.9)
print(f"Bold play, exact:                        {pb:.4%}")
for unit in (20, 100, 250, 500):
    print(f"Flat Rs {unit:>3}, exact:                     {flat_bet_reach_probability(500, 10_000, unit, p, 0.9):.4%}")
print("\nMonte Carlo, 100,000 sessions, min bet Rs 20, max Rs 500,000, base stake Rs 20:")
hdr = f"{'strategy':<20}{'P>=1000':>9}{'P>=2500':>9}{'P>=5000':>9}{'P=10000':>9}{'ruin':>8}{'med rounds':>12}"
print(hdr)
for s in ("bold", "flat", "martingale", "fibonacci", "dalembert", "reverse_martingale"):
    r = simulate(s, p, 0.9, base=20, min_bet=20, max_bet=500_000, sessions=100_000)
    pr = r["p_reach"]
    print(f"{s:<20}{pr[1000]:>9.4f}{pr[2500]:>9.4f}{pr[5000]:>9.4f}{pr[10000]:>9.4f}{r['p_ruin']:>8.4f}{r['median_rounds']:>12.0f}")

print("\n" + "=" * 80)
print("TABLE U  Ezugi Ultimate, Bahar 0.9:1, 20% fee, ASSUMED multiplier distribution")
print("=" * 80)
EM = (2 + 3 + 5) / 3
q = (1.421 - 1) / (EM - 1)
print(f"Calibration: q = P(multiplier on a winning bet) = {q:.4f}, M uniform on 2/3/5, E[mult] = {1 + q*(EM-1):.3f}")
rtp = p * (0.9 * (1 + q * (EM - 1)) + 1) / 1.2
print(f"Implied RTP = {rtp:.4%} (Ezugi publishes 97.82%)")


def simulate_ultimate(strategy, bankroll=500, target=10_000, base=20, min_bet=20, sessions=100_000,
                      max_rounds=50_000, seed=7):
    rng = np.random.default_rng(seed)
    bank = np.full(sessions, float(bankroll))
    alive = np.ones(sessions, dtype=bool)
    rounds = np.zeros(sessions, dtype=np.int64)
    reached = {m: np.zeros(sessions, dtype=bool) for m in (1000, 2500, 5000, 10_000)}
    mults = np.array([2.0, 3.0, 5.0])
    for _ in range(max_rounds):
        if not alive.any():
            break
        idx = np.flatnonzero(alive)
        b = bank[idx]
        if strategy == "bold":
            # stake so that an ordinary 0.9 win reaches the target; total cost is 1.2 x stake
            stake = np.minimum(b / 1.2, np.ceil((target - b) / 0.9))
        else:
            stake = np.full(idx.size, float(base))
        stake = np.minimum(stake, b / 1.2)
        bust = stake < min_bet
        win = rng.random(idx.size) < p
        hit = rng.random(idx.size) < q
        m = np.where(hit, rng.choice(mults, idx.size), 1.0)
        gain = np.where(win, np.floor(0.9 * stake * m), 0.0)
        # Pay 1.2 x stake. On a win get the stake back plus 0.9 x stake x multiplier; the fee is not returned.
        # That is the only reading under which Ezugi's published 97.82% follows from the stated payouts.
        nb = b - 1.2 * stake + np.where(win, stake + gain, 0.0)
        nb[bust] = b[bust]
        bank[idx] = nb
        rounds[idx] += 1
        for t in reached:
            reached[t][idx] |= nb >= t
        done = (nb >= target) | (nb < min_bet * 1.2) | bust
        alive[idx[done]] = False
    return {t: float(reached[t].mean()) for t in reached}, float((bank < min_bet * 1.2).mean()), float(np.median(rounds))


print("On a win the stake plus 0.9 x stake x multiplier comes back; the 20% fee does not. That reading")
print("reproduces Ezugi's published RTP; a fee-returned reading would make the bet positive, which it is not.")
for s in ("bold", "flat"):
    pr, ruin, med = simulate_ultimate(s)
    print(f"{s:<20}{pr[1000]:>9.4f}{pr[2500]:>9.4f}{pr[5000]:>9.4f}{pr[10000]:>9.4f}{ruin:>8.4f}{med:>12.0f}")
