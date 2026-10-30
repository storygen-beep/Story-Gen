"""
Price every Andar Bahar payout table collected in Phase 2 against the exact model.

Each table below is as published or as reported by review sites (trust level noted in
PHASE2_PROVIDERS_REPORT.md). Pricing assumes the standard deal: one 52-card deck,
joker drawn, 51 remain with 3 matches, alternate dealing starting with the side that
pays 0.9:1. RTP = sum over outcomes of P(outcome) x (payout + 1). House edge = 1 - RTP.

Run:  python3 research/andar_bahar/provider_tables.py
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb

from andar_bahar_model import first_match_distribution, side_probabilities

DIST = first_match_distribution(51, 3)
P_FIRST, P_SECOND = side_probabilities(51, 3)


def bucket_prob(lo: int, hi: int) -> F:
    return sum(DIST[k] for k in range(lo, min(hi, 49) + 1))


def rtp_line(label: str, p: F, payout: F) -> str:
    rtp = p * (payout + 1)
    return f"  {label:<28} P = {float(p):8.4%}   pays {float(payout):>6.2f}:1   RTP {float(rtp):8.4%}   house edge {float(1 - rtp):+8.4%}"


def main_bets(first_payout: F, second_payout: F, first_name: str, second_name: str) -> None:
    print(rtp_line(f"{first_name} (first card)", P_FIRST, first_payout))
    print(rtp_line(f"{second_name} (second)", P_SECOND, second_payout))


def card_count_table(buckets: list[tuple[int, int, F]]) -> None:
    for lo, hi, pay in buckets:
        print(rtp_line(f"cards {lo}-{hi}", bucket_prob(lo, hi), pay))


def first_three_poker() -> None:
    """Pragmatic Play 'First Three': joker + first Andar card + first Bahar card as a 3-card poker hand.

    Counted exactly over all C(52,3) = 22,100 three-card sets. Straights counted with
    ace high or low (A-2-3 and Q-K-A both count): 12 rank windows. If the table counts
    only one of them the straight line drops by 1/12.
    """
    total = comb(52, 3)
    ranks = list(range(13))  # 0 = A ... 12 = K
    windows = [set(((s + i) % 13) for i in range(3)) for s in range(12)]  # A23 .. QKA, excluding KA2
    sf = straight = flush = 0
    cards = [(r, s) for r in ranks for s in range(4)]
    for trio in combinations(cards, 3):
        rs = {c[0] for c in trio}
        same_suit = len({c[1] for c in trio}) == 1
        is_straight = len(rs) == 3 and any(rs == w for w in windows)
        if is_straight and same_suit:
            sf += 1
        elif is_straight:
            straight += 1
        elif same_suit:
            flush += 1
    for label, n, pay in (("straight flush", sf, 120), ("straight", straight, 8), ("flush", flush, 5)):
        print(rtp_line(f"first three: {label}", F(n, total), F(pay)))
    rtp = F(sf * 121 + straight * 9 + flush * 6, total)
    print(f"  {'first three: whole bet':<28} RTP {float(rtp):8.4%}   house edge {float(1 - rtp):+8.4%}")


def main() -> None:
    print("=" * 96)
    print("STANDARD LIVE TABLE  (Ezugi studio, Evolution Super Andar Bahar, Pragmatic Play Live): Andar 0.9:1, Bahar 1:1")
    print("Reported by: Wizard of Odds (independent), review sites for each provider. Provider pages publish no RTP.")
    print("=" * 96)
    main_bets(F(9, 10), F(1), "Andar", "Bahar")

    print("\n-- Ezugi studio table, card-count side bet (review sites; matches Wizard of Odds table) --")
    card_count_table([(1, 5, F(5, 2)), (6, 10, F(7, 2)), (11, 15, F(9, 2)), (16, 25, F(7, 2)),
                      (26, 30, F(14)), (31, 35, F(24)), (36, 40, F(49)), (41, 49, F(119))])
    print("  Ezugi's own OTT page snippet claims 'main bet RTP 94.85%'. Not derivable from 0.9:1 / 1:1. Unresolved.")

    print("\n-- Pragmatic Play Live side bets (review sites; no provider paytable found) --")
    card_count_table([(1, 5, F(5, 2)), (6, 10, F(7, 2)), (11, 15, F(9, 2)), (16, 25, F(7, 2)),
                      (26, 30, F(29, 2)), (31, 35, F(49, 2)), (36, 40, F(49)), (41, 49, F(119))])
    print(rtp_line("first on Andar", F(3, 51), F(15)))
    print(rtp_line("first on Bahar", F(48, 51) * F(3, 50), F(31, 2)))
    first_three_poker()

    print("\n-- Evolution Super Andar Bahar side bets, BASE payouts before random multipliers (review sites) --")
    card_count_table([(1, 5, F(2)), (6, 10, F(3)), (11, 15, F(4)), (16, 20, F(5)), (21, 25, F(8)),
                      (26, 30, F(12)), (31, 35, F(20)), (36, 40, F(40)), (41, 45, F(110)), (46, 49, F(800))])
    print("  Review sites quote 96% side-bet RTP. The base table above is far below that, so the random")
    print("  multipliers carry the difference. Their frequency and size are not published anywhere found.")

    print("\n" + "=" * 96)
    print("1xBET IN-HOUSE RNG 'ANDAR BAHAR' (1xGames) as stated on indian.1xbet.com/en/games/andar-bahar")
    print("=" * 96)
    print("Round 1, bets on the joker itself:")
    print(rtp_line("suit match", F(1, 4), F(27, 10)))      # 3.7x total return = 2.7:1
    print(rtp_line("value 2-7", F(6, 13), F(1)))           # 2x total return = 1:1
    print(rtp_line("value 9-A", F(6, 13), F(1)))
    print(rtp_line("value 8", F(1, 13), F(11)))            # 12x total return = 11:1
    print("Round 2, as stated: 'distribution always starts with Andar', Andar 2x, Bahar 2.1x, +20 pays 4x:")
    print(rtp_line("Andar (first card)", P_FIRST, F(1)))
    print(rtp_line("Bahar (second)", P_SECOND, F(11, 10)))
    print(rtp_line("+20 (21 or more cards)", bucket_prob(21, 49), F(3)))
    print("  Both main bets price POSITIVE for the player under the standard deal. No house ships that.")
    print("  Either the page's payouts are wrong, or the game is not dealing a simulated deck with")
    print("  standard alternation. The in-game info panel must settle it before anything else.")


if __name__ == "__main__":
    main()
