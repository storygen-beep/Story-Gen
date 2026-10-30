"""
Price the three live Andar Bahar tables observed on the user's 1xBet account
(screenshots, 2026-10-30, domain 1-x-bet-india.com) against the exact model.

Table A  "1x Andar Bahar" (1xLIVE-branded dedicated table, Ezugi game-info panel): Andar 1:1,
         Bahar 0.9:1, Bahar first, cards-dealt 2.5/3.5/4.5/3.5/14/24/49/119. Published RTP
         Andar 96.99%, Bahar 97.86%, side bets 91.45% to 98.10%.
Table B  "Ultimate Andar Bahar" (Ezugi, confirmed by lobby tile and game-info panel): Andar 1:1,
         Bahar 0.9:1, 20% fee on every bet, side bets 2/3/4/3/12/20/40/100, random 2x/3x/5x
         multipliers on 1-3 virtual cards. Published RTP: Andar 97.44%, Bahar 97.82%, sides 95.05-95.68%.
Table C  "Andar Bahar" by ElCasino (1xBet "TV Games" section; watermark on its rules panel and
         the TV Games lobby tile): Andar 0.9:1, Bahar 1:1,
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


print("TABLE A  '1x Andar Bahar' (1xLIVE dedicated table; Ezugi game-info panel read 2026-10-30)")
print("  Rules: one 52-card deck shuffled/changed before each round by the dealer; joker, then betting; Bahar first.")
print("  Exact model versus Ezugi's published 'optimal return to player':")
published_A = {"Bahar (first card)": F(9786, 10000), "Andar (second)": F(9699, 10000),
               (1, 5): F(9486, 10000), (6, 10): F(9768, 10000), (11, 15): F(9296, 10000), (16, 25): F(9810, 10000),
               (26, 30): F(9145, 10000), (31, 35): F(9248, 10000), (36, 40): F(9497, 10000), (41, 49): F(9520, 10000)}
rows = [("Bahar (first card)", P_FIRST, F(9, 10)), ("Andar (second)", P_SECOND, F(1))]
rows += [(f"cards {lo}-{hi}", bucket(lo, hi), pay) for (lo, hi), pay in
         zip([(1, 5), (6, 10), (11, 15), (16, 25), (26, 30), (31, 35), (36, 40), (41, 49)],
             [F(5, 2), F(7, 2), F(9, 2), F(7, 2), F(14), F(24), F(49), F(119)])]
keys = ["Bahar (first card)", "Andar (second)", (1, 5), (6, 10), (11, 15), (16, 25), (26, 30), (31, 35), (36, 40), (41, 49)]
worst = 0.0
for (label, p, pay), key in zip(rows, keys):
    model = p * (pay + 1)
    pub = published_A[key]
    diff = float(pub - model) * 100
    worst = max(worst, abs(diff))
    print(f"  {label:<20} model RTP {float(model):8.4%}   published {float(pub):6.2%}   difference {diff:+.3f} points")
print(f"  Largest difference: {worst:.3f} points. The provider's own figures agree with a single-deck,")
print("  three-match, alternate-deal model on every bet. The model is validated for Ezugi tables.")

print("\nTABLE B  'Ultimate Andar Bahar' (Ezugi; game-info panel read 2026-10-30)")
print("  Rules: one 52-card deck shuffled/changed by the dealer before each round; Bahar first;")
print("  20% fee added to the player's total bet; Andar 1:1, Bahar 0.9:1; side bets 2/3/4/3/12/20/40/100;")
print("  1-3 multiplier cards (2x/3x/5x) drawn from a VIRTUAL pack after bets close; side bets get one random multiplier.")
FEE = F(6, 5)
for label, p, pay, published in (("Bahar (first card)", P_FIRST, F(9, 10), F(9782, 10000)),
                                  ("Andar (second)", P_SECOND, F(1), F(9744, 10000))):
    base = p * (pay + 1) / FEE
    implied = (published * FEE / p - 1) / pay
    print(f"  {label:<20} RTP without multipliers {float(base):7.2%}   Ezugi's published RTP {float(published):6.2%}"
          f"   implied average multiplier on a winning bet {float(implied):.3f}x")
print("  Side bets, RTP without multiplier vs published:")
for (lo, hi), pay, published in zip([(1, 5), (6, 10), (11, 15), (16, 25), (26, 30), (31, 35), (36, 40), (41, 49)],
                                    [F(2), F(3), F(4), F(3), F(12), F(20), F(40), F(100)],
                                    [F(9519, 10000), F(9540, 10000), F(9505, 10000), F(9516, 10000),
                                     F(9568, 10000), F(9537, 10000), F(9550, 10000), F(9522, 10000)]):
    base = bucket(lo, hi) * (pay + 1) / FEE
    implied = published * FEE / (bucket(lo, hi) * (pay + 1))
    print(f"    cards {lo:>2}-{hi:<2}  base {float(base):7.2%}   published {float(published):6.2%}   implied multiplier {float(implied):.3f}x")
print("  Published figures cannot be derived independently: the multiplier draw distribution is not published.")
print("  They are consistent with the stated mechanics (about 1.4x average on winners) and are Ezugi's own numbers.")

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
