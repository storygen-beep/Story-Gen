# Andar Bahar — Phase 1: Game Research and Exact Mathematics

Status: Phase 1 complete. Phases 2–3 (shuffle and platform integrity) need the
platform URL, its published rules and payout table before they can be done
against the real target rather than in general.

Every number below is produced by `andar_bahar_model.py` in this folder. Rerun it
to reproduce them. Where a statement comes from general knowledge rather than
from the model, it is marked **[unverified for your platform]**.

## 1. Rules of the standard online game

Verified by derivation from the rules; the rules themselves are the common
single-deck form. Confirm each against your platform's rule page.

- One 52-card deck, reshuffled for every round. Online RNG tables generate a fresh
  virtual deck per round; live-dealer tables shuffle a physical deck per round.
  **[unverified for your platform]** — a continuous shoe without reshuffle is the
  one rule variant that would change the mathematics, so this is the first thing to
  confirm.
- A first card, the joker, is drawn face up. 51 cards remain, exactly 3 of which
  share its rank.
- Cards are then dealt alternately to the two piles. On most online tables the
  first card always goes to Andar. On classic tables the joker's colour decides:
  black joker, first card to Andar; red joker, first card to Bahar.
- The first card matching the joker's rank ends the round. The pile it lands on wins.
- Main bets close before the first card is dealt. Some tables offer a second bet
  after two cards are dealt, at adjusted odds.
- Typical payouts: the first-dealt side pays 0.9:1, the second-dealt side pays 1:1.
  Some tables pay 1:1 on both. Your platform's payout table is required.
- Side bets on how many cards will be dealt are common. Their fair odds are in
  section 4.

## 2. Win probabilities (exact)

The three matching cards occupy a uniformly random 3-subset of the 51 positions.
The first match sits at position k with probability C(51−k, 2) / C(51, 3). The
first-dealt pile receives the odd positions, the second-dealt pile the even ones.

| outcome | exact | decimal |
|---|---|---|
| first-dealt side wins | 429/833 | 51.5006% |
| second-dealt side wins | 404/833 | 48.4994% |
| first-side advantage | 25/833 | 3.0012 percentage points |

The widely quoted "26/51 = 50.98%" figure is wrong for this game. 26/51 is the
answer when only one matching card exists; with three it is 429/833. The model
prints both so the difference is auditable.

The joker's rank carries no information: every rank has exactly three partners.
The joker's colour matters only on colour-decides-first-side tables, and then it
only tells you which side holds the 51.5%, which the payout already prices.

## 3. Expected value and house edge

Per 1 rupee staked. EV = P(win) × payout − P(lose).

| bet | payout | EV | house edge |
|---|---|---|---|
| first side | 1.00:1 | +0.0300 | player edge 3.00% (no real table pays this) |
| first side | 0.95:1 | +0.0043 | player edge 0.43% |
| first side | 0.90:1 | −0.0215 | 2.15% |
| first side | 0.85:1 | −0.0472 | 4.72% |
| second side | 1.00:1 | −0.0300 | 3.00% |
| second side | 0.95:1 | −0.0543 | 5.43% |
| second side | 0.90:1 | −0.0785 | 7.85% |

Consequences:

- On the standard 0.9:1 / 1:1 table, **the first-dealt side at 0.9:1 is the better
  bet** (2.15% edge versus 3.00%). The intuition "take the even-money side" is wrong.
- A table paying 1:1 on the first-dealt side would be a positive-expectation bet.
  No operator offers that knowingly. If a rule page claims it, assume a misprint,
  then verify with real rounds.
- Kelly fraction is negative for both standard bets. Kelly's answer is to bet zero.

## 4. Round length

| statistic | value |
|---|---|
| expected cards dealt after the joker | exactly 13 |
| maximum possible | 49 |
| match on the very first card | 1/17 = 5.88% |
| round over within 5 cards | 27.11% |
| round over within 13 cards | 59.49% |
| 26 or more cards | 12.49% |
| 41 or more cards | 0.79% |
| 45 or more cards | 0.17% |

Fair odds for the usual card-count side-bet buckets (compare against your
platform's payouts to measure the edge on each):

| bucket | probability | fair payout |
|---|---|---|
| 1–5 | 27.11% | 2.69:1 |
| 6–10 | 21.70% | 3.61:1 |
| 11–15 | 16.90% | 4.92:1 |
| 16–25 | 21.80% | 3.59:1 |
| 26–30 | 6.10% | 15.40:1 |
| 31–35 | 3.70% | 26.05:1 |
| 36–40 | 1.90% | 51.72:1 |
| 41–49 | 0.79% | 125.21:1 |

## 5. Does any observable information change the next outcome?

### Across rounds, with a reshuffle every round
No. Each round is an independent draw from the same distribution. The previous
joker, the previous winner, streak length, and the full card history carry zero
information about the next round. Any "pattern" signal built from them is noise.

### Across rounds, without a reshuffle (continuous shoe, hypothetical)
Then the count of the current joker's rank already removed matters. With n cards
left and m of the joker's rank among them:

| n | m | P(first side) |
|---|---|---|
| 51 | 3 | 51.50% |
| 40 | 3 | 51.92% |
| 20 | 3 | 53.95% |
| 10 | 3 | 58.33% |
| 40 | 2 | 51.28% |
| 20 | 2 | 52.63% |
| 40 | 1 | 50.00% |

The first side at 0.9:1 becomes positive-expectation only when P(first) exceeds
52.63%. That requires a deep shoe with all three partners still live, a state a
real operator never offers because every known online implementation reshuffles.
Test for it anyway: if the same card (rank and suit) ever appears twice within
what the table calls one shoe, the table reshuffles. Cheap and decisive.

### Within a round, before the main bet closes
Nothing is revealed except the joker, which carries no information (section 2).

### Within a round, at a second-bet window
After k non-matching cards are out, the next pile to receive a card wins with
probability rising from 51.50% (k=0) to 52.50% (k=20) and 57.58% (k=40). Tables
that offer a mid-round bet reprice it to keep their edge. Check the second-bet
payout against these numbers; if the operator misprices it, that is a genuine
edge and the only in-game one this analysis can find. It would still have to be
confirmed over many rounds before a rupee goes on it.

### Multi-deck variants
Decks increase the first-side advantage slightly: 51.75% with 2 decks, 51.94%
with 8. None of these reach the 52.63% break-even for 0.9:1.

## 6. What this already says about ₹500 to ₹10,000

This is the Phase 5 question, but the ceiling follows directly from the Phase 1
mathematics, so it belongs here.

- In a game with zero house edge, no strategy can reach ₹10,000 from ₹500 with
  probability above 500/10,000 = 5.00%. This is a theorem (optional stopping),
  not an estimate.
- In a subfair game the maximum is achieved by bold play: stake everything, or
  exactly what is needed to hit the target. Dubins and Savage, 1965. Solved
  exactly for this game:

| strategy | bet | P(reach ₹10,000) | P(lose everything) |
|---|---|---|---|
| bold play | first side 0.9:1 | 4.48% | 95.5% |
| bold play | second side 1:1 | 4.34% | 95.7% |
| flat ₹250 | second side 1:1 | 1.27% | 98.7% |
| flat ₹100 | second side 1:1 | 0.087% | 99.9% |
| flat ₹50 | second side 1:1 | 0.0005% | ~100% |
| flat ₹10 | second side 1:1 | 0.0000% | 100% |

Monte Carlo, 100,000 sessions per strategy, bet limits ₹10 to ₹10,000, base
stake ₹10, second side at 1:1:

| strategy | P ≥ ₹1,000 | P ≥ ₹2,500 | P ≥ ₹5,000 | P = ₹10,000 | ruin | median rounds |
|---|---|---|---|---|---|---|
| bold | 48.3% | 11.4% | 5.5% | 4.38% | 95.6% | 1 |
| martingale | 42.5% | 13.1% | 5.2% | 1.98% | 98.0% | 100 |
| fibonacci | 37.6% | 9.3% | 2.9% | 0.90% | 99.1% | 195 |
| d'Alembert | 37.8% | 9.0% | 2.3% | 0.45% | 99.6% | 98 |
| reverse martingale | 29.7% | 2.2% | 0.04% | 0.00% | 100% | 376 |
| flat ₹10 | 4.8% | 0.0% | 0.0% | 0.00% | 100% | 1,260 |

Reading the table:

- Every progression loses to bold play on the target question and every one of
  them has a higher ruin probability than bold play. Progressions reshape the
  path, they do not move the expectation. The smaller the bets, the more rounds
  the house edge is charged on, and the lower the chance of ever reaching the
  target.
- Martingale's 100-round median hides its failure mode: a run of 9 losses from a
  ₹10 base needs ₹5,110 in hand for the tenth bet, which ₹500 never has. It busts
  on the first long run, which arrives on average well inside 400 rounds.
- The 4.5% ceiling is a hard number. ₹500 at any Andar Bahar table is a roughly
  one-in-twenty-two shot at ₹10,000 and a roughly twenty-one-in-twenty-two shot
  at ₹0. No information, system, or stake-sizing changes that unless the table
  itself is broken (section 7).

## 7. What would have to be true for the picture to change

A positive-expectation bet needs one of:

1. A payout table more generous than 0.9:1 / 1:1. Measured in minutes from the
   rule page. Report it and the model prices it immediately.
2. A mispriced second-bet window (section 5).
3. A continuous shoe without reshuffle (section 5). Detectable with one repeated card.
4. A biased deal. The first side at 0.9:1 needs P(first) above 52.63%; the second
   side at 1:1 needs P(second) above 50%. Rounds needed to detect such a bias
   with 90% power at 5% significance, one-sided test:

| true P(second) | rounds to detect |
|---|---|
| 0.50 | ~9,500 |
| 0.52 | ~1,750 |
| 0.53 | ~1,050 |
| 0.55 | ~500 |

   At one round per 30 to 60 seconds that is 8 to 160 hours of observation
   before the first justified bet. The payoff if found is also small: even a
   P(win) of 0.55 lifts bold-play reach probability from 4.3% to 7.8%, and 0.60
   only to 11.6%. A platform biased in the player's favour by five points does
   not exist; the realistic sign of any bias is against the player.

Nothing on this list is available from ₹500 of play. All of it is observation
first, wagering never or later.

## 8. Items needed from you before Phase 2 and 3

1. The platform URL and the exact game variant name (provider name if shown,
   for example Ezugi, Evolution, Super Spade, or an in-house RNG table).
2. Screenshot or copy of the rules page and the full payout table, including side
   bets and any second-bet window.
3. Minimum and maximum stake on that table.
4. Whether it is a live-dealer stream or an animated RNG table.
5. Any fairness, certification, or "provably fair" link the page offers.
6. The round-history widget if one exists (a screenshot of 50 or more past
   results is enough to begin the independence checks).

## 9. Preview of Phase 2 and 3, flagged as general knowledge

These are the documented facts the next phases build on. They are from
general knowledge and will be checked against sources in Phase 2.
**[unverified for your platform]** applies to every line.

- Fisher–Yates with a cryptographically secure generator is the accepted
  shuffle. Known failure modes: using a non-cryptographic generator such as
  Mersenne Twister, whose 19,937-bit state can be recovered from 624 consecutive
  outputs; seeding from the clock; modulo bias when mapping random integers to
  card indices; and the off-by-one that makes some permutations impossible.
- The textbook real case: in 1999 Reliable Software Technologies showed that a
  commercial online poker shuffle seeded a 32-bit generator from the millisecond
  clock, leaving about 200,000 possible decks, and predicted the full deal after
  seeing five cards. That attack does not exist against a correctly seeded
  cryptographic generator, which is what certified providers state they use.
- "Provably fair" tables publish a server-seed hash before the round and reveal
  the seed after, so the player can recompute the deck. That proves the shuffle
  was fixed before bets closed. It does not prove the published odds are right,
  and no live-dealer or mainstream RNG casino table uses it.
- Independent certification (eCOGRA, GLI, iTech Labs, BMM) tests the generator
  and the game logic against the published payout table. The certificate
  belongs to the provider and the build, not to the site running it. A site can
  skin a certified game or run an uncertified clone under the same name.
- The practical integrity risk for a small account is rarely the shuffle. It is
  withdrawal: identity checks, bonus terms, limits, and refusal. An operator who
  wanted to take ₹500 does not need to bend a card.
- Regulatory context: India's Promotion and Regulation of Online Gaming Act,
  2025 prohibits offering online money games to Indian users. A rupee-denominated
  Andar Bahar table reachable from India is therefore offshore and unlicensed
  for India, which means no domestic regulator, audit obligation, or recourse.
  Confirm the current enforcement position; the point here is the absence of any
  enforceable fairness guarantee.

## 10. Phase 1 conclusion

- The game has a fixed, known house edge of 2.15% (first side, 0.9:1) or 3.00%
  (second side, 1:1) under the standard rules.
- No observable information changes the next outcome on a reshuffled table.
- The best achievable probability of turning ₹500 into ₹10,000 is about 4.5%,
  reached by staking everything in a handful of rounds. Every careful-looking
  system does worse. This is a ceiling, not a strategy recommendation; no
  betting recommendation is made at this phase, as agreed.
- The only routes to a positive-expectation bet are operator errors (payout
  misprint, mispriced second bet, no reshuffle, biased deal), and each must be
  observed over hundreds to thousands of rounds before it could justify a stake.
- Given the stated purpose, the decision-relevant number is this: ₹500 kept is
  5% of the rent with certainty; ₹500 played is about a 4.5% chance of the whole
  rent and a 95.5% chance of 0% of it. The expected contribution to the rent is
  about ₹450 to ₹485 if played, ₹500 if not.
