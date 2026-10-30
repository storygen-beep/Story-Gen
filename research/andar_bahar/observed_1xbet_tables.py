"""
Price the three live Andar Bahar tables observed on the user's 1xBet account
(screenshots, 2026-10-30, domain 1-x-bet-india.com) against the exact model.

Table A  "1x Andar Bahar" (1xLIVE-branded): Andar 1:1, Bahar 0.9:1,
         cards-dealt 2.5/3.5/4.5/3.5/14/24/49/119 for 1-5/6-10/11-15/16-25/26-30/31-35/36-40/41-49.
         Paytable identical to Ezugi's studio table. First card to Bahar implied by the 0.9:1.
Table B  "Ultimate Andar Bahar": Andar 1:1, Bahar 0.9:1, side bets shown with the round's
         random multipliers already applied (base 2/3/4/3/12/20/40/100 per review sites).
Table C  "Andar Bahar" (1st Andar / First 3 / 1st Bahar layout): Andar 0.9:1, Bahar 1:1,
         1st Andar 15:1, 1st Bahar 15.5:1, First 3 = 120/8/5, cards-dealt
         2/3/4/5/8/12/20/40/110/800 for ten 5-card buckets. Rules panel: one 52-card deck,
         certified shuffling machine, deck reshuffled after every game, first card to Andar,
         two betting rounds (before and after the joker is revealed).

Run: python3 observed_1xbet_tables.py
"""
from fractions import Fraction as F
from math import comb

from andar_bahar_model import first_match_distribution, side_probabilities

DIST = first_match_distribution(51, 3)
P_FIRST, P_SECOND = side_probabilities(51, 3)


def bucket(lo, hi):
    return sum(DIST[k] for k in range(lo, min(hi, 49) + 1))


def line(label, p, pay):
    rtp = p * (pay + 1)
    return f"  {label:<26} P={float(p):8.4%}  pays {float(pay):>6.2f}:1  RTP {float(rtp):8.4%}  edge {float(1-rtp):+8.4%}"


def first3_given_joker_rank(rank: int) -> F:
    """RTP of First 3 given the joker's rank (1=A .. 13=K), ace high or low, as the rules state.

    Two more cards come from the remaining 51. A straight needs the other two ranks of a
    3-rank window containing the joker's rank: 16 suit combinations per window, one of
    which is a straight flush. A flush needs both in the joker's suit: C(12,2) = 66 pairs.
    """
    windows = 0
    for start in range(1, 13):               # A23 (1..3) through QKA (12,13,1)
        ranks = {((start - 1 + i) % 13) + 1 for i in range(3)}
        if rank in ranks:
            windows += 1
    pairs = comb(51, 2)
    sf = windows
    straight = windows * 15
    flush = 66 - windows                      # exclude the straight-flush pairs
    return F(sf * 121 + straight * 9 + flush * 6, pairs)


print("TABLE A  '1x Andar Bahar'  (Ezugi-pattern paytable; Bahar receives the first card)")
print(line("Bahar (first card)", P_FIRST, F(9, 10)))
print(line("Andar (second)", P_SECOND, F(1)))
for (lo, hi), pay in zip([(1, 5), (6, 10), (11, 15), (16, 25), (26, 30), (31, 35), (36, 40), (41, 49)],
                         [F(5, 2), F(7, 2), F(9, 2), F(7, 2), F(14), F(24), F(49), F(119)]):
    print(line(f"cards {lo}-{hi}", bucket(lo, hi), pay))

print("\nTABLE B  'Ultimate Andar Bahar'  (Bahar receives the first card; multipliers on side bets)")
print(line("Bahar (first card)", P_FIRST, F(9, 10)))
print(line("Andar (second)", P_SECOND, F(1)))
print("  Side bets: base table unverified on-screen (multipliers were applied in the shot).")
print("  Review sites report a 20% fee on every bet on this table. If true, a Bahar bet at 0.9:1")
print("  costs 1.2 to win 0.9 unless multipliers hit: RTP before multipliers =", end=" ")
print(f"{float(P_FIRST * F(9,10) + P_FIRST) / 1.2:.4%}. Rules panel needed.")

print("\nTABLE C  'Andar Bahar' with 1st Andar / First 3 / 1st Bahar  (Andar receives the first card)")
print(line("Andar (first card)", P_FIRST, F(9, 10)))
print(line("Bahar (second)", P_SECOND, F(1)))
print(line("1st Andar", F(3, 51), F(15)))
print(line("1st Bahar", F(48, 51) * F(3, 50), F(31, 2)))
for (lo, hi), pay in zip([(1, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 35), (36, 40), (41, 45), (46, 49)],
                         [F(2), F(3), F(4), F(5), F(8), F(12), F(20), F(40), F(110), F(800)]):
    print(line(f"cards {lo}-{hi}", bucket(lo, hi), pay))
total = comb(52, 3)
unconditional = F(48 * 121 + 720 * 9 + 1096 * 6, total)
print(f"  First 3, bet before joker shown:            RTP {float(unconditional):8.4%}  edge {float(1-unconditional):+8.4%}")
print("  First 3, bet AFTER the joker is shown (second betting round), by joker rank:")
names = {1: "A", 11: "J", 12: "Q", 13: "K"}
for r in range(1, 14):
    rtp = first3_given_joker_rank(r)
    print(f"    joker {names.get(r, str(r)):>2}: RTP {float(rtp):8.4%}  edge {float(1-rtp):+8.4%}")
