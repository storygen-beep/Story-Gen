# Andar Bahar — Phase 5 on the real tables, and Phase 6 architecture

Date: 2026-10-30. Inputs: the table parameters read from the 1xBet account in Phase 2 Task 4.
Numbers from `table_simulation.py` in this folder.

## Phase 5: ₹500 to ₹10,000 on the tables actually available

### Ezugi standard table (Bahar 0.9:1) and Evolution Super Andar Bahar (Andar 0.9:1)

Both have P(win) = 51.5006% on the 0.9:1 side. Minimum stake taken as ₹20, maximum ₹500,000.

Update 2026-10-31: the chosen table, 1x Andar Bahar, has limits ₹100 to ₹200,000. Rerun with
those limits (`simulate`, 200,000 sessions): bold play unchanged at 4.50% (exact 4.48%), because
every bold-play stake from ₹500 is at least ₹100; martingale from a ₹100 base 3.13%. Bold play
remains the ceiling.

| strategy | P ≥ ₹1,000 | P ≥ ₹2,500 | P ≥ ₹5,000 | P = ₹10,000 | ruin | median rounds |
|---|---|---|---|---|---|---|
| bold play (exact) | 26.4% | 13.6% | 7.0% | **4.48%** | 95.5% | 2 |
| martingale from ₹20 | 44.3% | 14.5% | 6.1% | 2.44% | 97.6% | 68 |
| fibonacci from ₹20 | 40.2% | 11.1% | 3.8% | 1.13% | 98.9% | 145 |
| d'Alembert from ₹20 | 42.1% | 12.2% | 4.0% | 0.93% | 99.1% | 68 |
| flat ₹500 (exact) | | | | 1.88% | | |
| flat ₹250 (exact) | | | | 1.29% | | |
| flat ₹100 (exact) | | | | 0.20% | | |
| flat ₹20 | 22.5% | 0.6% | 0.0% | 0.00% | 100% | 627 |
| reverse martingale | 39.5% | 9.5% | 1.7% | 0.06% | 99.9% | 137 |

Nothing has moved since Phase 1. The validated model, the real paytable and the real limits
give the same ceiling: about 4.5% by staking everything, less by any other method.

### Ezugi Ultimate (Bahar 0.9:1, 20% fee, multipliers)

The multiplier draw distribution is unpublished, so this is a sensitivity case: a winning bet
is multiplied with probability 18% by 2x, 3x or 5x equally, calibrated so the return matches
Ezugi's published 97.82%. The fee is paid on every bet and is not returned on a win; that is
the only reading under which the published return follows from the stated payouts.

| strategy | P ≥ ₹1,000 | P ≥ ₹2,500 | P ≥ ₹5,000 | P = ₹10,000 | ruin |
|---|---|---|---|---|---|
| bold play | 31.0% | 11.8% | 5.9% | **2.70%** | 96.5% |
| flat ₹20 | 30.7% | 2.6% | 0.1% | 0.00% | 100% |

Ultimate is worse for the target than the plain table, 2.7% against 4.5%, even though its
published return is almost the same. Reason: bold play needs ordinary wins to compound, and
on Ultimate an ordinary win returns 0.9 on 1.2 paid. The multipliers restore the average but
not the path. Rule out Ultimate.

### Side bets

Every side bet on every table prices worse than the main bet (Phase 2 section 10). None
belong in any plan.

Correction 2026-10-31: on 1x Andar Bahar (Ezugi) two cards-dealt bets beat the main bet. "16-25" at 3.5:1 returns 98.10% (Ezugi's published figure, model 98.103%) against Bahar's 97.85%, and "6-10" returns 97.67%. The earlier statement that every side bet is worse holds for ElCasino (Table C), not for this table. All bets still have negative EV. See "Corrected ceiling" below.

### Phase 5 conclusion

- Best table for the target: Ezugi standard or 1x Andar Bahar betting Bahar, or Evolution
  Super Andar Bahar betting Andar. Identical mathematics.
- (Corrected below to 4.79% on 1x Andar Bahar.) Best achievable probability: 4.48%, by betting the whole bankroll until it reaches ₹10,000
  or ₹0. Expected number of rounds: about two.
- Every progression system lowers that number and raises the ruin probability.
- Minimum withdrawal on the account is ₹1,000, so no outcome under ₹1,000 is collectable.
  Bold play from ₹500 passes ₹1,000 on the first win or never.

## Phase 6: observation and audit architecture

### What the system can and cannot be

Phase 1 proved no observable information changes the next round's probability on a
reshuffled table. Phase 2 confirmed every table on the account reshuffles every round.
A "real-time decision support" layer therefore has exactly one honest output per round:
**skip**, because no bet has positive expectation. It will be built, and it will say skip.

What the system can usefully do is **audit**: log every round of a chosen table from the
live stream, without betting, and test the log against the validated model. That answers
"does the physical deal match the published rules" with data instead of trust. If the
audit ever showed an exploitable bias at pre-registered significance, the decision layer
would change its answer. Phase 1 sized that: 1,000 to 9,500 rounds, and even then the gain
is small.

### Components

1. **Capture** (local laptop, Chromium via Playwright, persistent profile).
   - You log in once by hand in the Playwright-controlled browser; the script never handles
     credentials and never places bets. It has no code path to the bet buttons.
   - It opens the chosen table and listens to the game client's WebSocket frames
     (`page.on("websocket")`). Ezugi's and Evolution's clients receive round state as
     structured messages: round id, joker, each dealt card with its side, winner. That is
     the primary source: exact, sub-second, no image processing.
   - Fallback: a DOM poll every 500 ms of the joker panel, the ANDAR and BAHAR card slots
     and the result road, de-duplicated by the round id shown in the header.
   - Everything is read from your own browser session. Nothing is sent to the operator
     beyond what the page sends on its own.

2. **Store** (SQLite, one file).
   `rounds(round_id, table_name, ts_start, ts_end, joker_rank, joker_suit, cards_json,
   first_side, winner, n_cards, source)`. `cards_json` is the ordered list of
   (side, rank, suit). No bet columns are needed until a bet is ever justified.

3. **Audit** (`audit.py`, runs on the SQLite file, pre-registered tests).
   - Winner frequency against 51.5006% for the first-card side, exact binomial.
   - Card-count distribution against the exact bucket probabilities, chi-square, 8 buckets.
   - Joker rank uniformity, chi-square, 13 ranks.
   - Independence: runs test on the winner sequence; autocorrelation at lags 1 to 5.
   - Integrity: no card repeated within a round, no rank more than four times in a round,
     first card always to the stated side, n_cards between 1 and 49.
   - Multiple testing: Bonferroni across the five families; nothing reported before 300
     rounds; alpha 0.01.
   - Output: one table per test with statistic, p-value, verdict, and the rounds needed to
     resolve any borderline result.

4. **Decision layer** (`decide.py`).
   For each round: current paytable, P(win) from the model or from the audit's posterior if
   a bias were established, EV per bet, recommendation. Under the validated model its output
   is "skip" on every bet. It exists so that the recommendation is computed, not asserted.

5. **Reporting to this session.** Export the SQLite file or a CSV; run `audit.py` locally
   and paste its output. No live link is needed because nothing in the loop is time-critical.

### Latency

WebSocket frames arrive as the dealer deals. The DOM fallback is half a second behind.
Neither matters: the decision is settled before the joker is drawn.

### Phase 7: controlled test, before any live use

1. Generate 10,000 rounds from the model, run `audit.py`, confirm every test passes.
2. Inject a 3-point bias and a dealing-order error into the generated data, confirm the
   audit catches both at the stated sample sizes.
3. Run capture on the live stream for two hours without betting. Compare 20 logged rounds
   against screenshots taken at the same time. Any mismatch is a capture bug to fix first.
4. Only then run the audit on real data.

### What is needed to build it

- A laptop or desktop (macOS, Windows or Linux) with Chrome or Chromium. A phone cannot run
  Playwright; iOS Safari exposes nothing. Without a computer the alternative is screen
  recording on the phone and offline frame reading, which is slower and less reliable.
- The table to observe. Recommended: the Ezugi "Andar Bahar" or "1x Andar Bahar" table, or
  Evolution Super Andar Bahar. Both have a provider-published paytable the model reproduces.

## Corrected ceiling: all bets on 1x Andar Bahar (2026-10-31)

Phase 5 searched one bet. `tools/optimal_reach.py` searches every bet on the table each round as a
Markov decision problem (value iteration, ₹10 grid, minimum stake ₹100, one bet per round).

| allowed bets | P(₹500 reaches ₹10,000) |
|---|---|
| Andar only | 4.34% |
| Bahar only | 4.46% (exact solver without grid: 4.48%) |
| cards 6-10 only | 4.74% |
| cards 16-25 only | 4.79% |
| cards 41-49 only | 3.90% |
| any bet, best each round | **4.79%** |

The optimum at ₹500 is the whole bankroll on cards-dealt "16-25" (3.5:1, wins 21.80% of rounds,
house edge 1.90%). A win leaves ₹2,250. Ruin probability stays near 95%. The gain over Bahar,
0.33 points, comes from the smaller edge and from needing fewer wins at 3.5:1.

Limits: combinations of several cards-dealt bets in one round were not searched; the ₹10 grid
rounds winnings down. Neither can turn a negative-EV game positive, so `decide.py`'s per-round
output is unchanged: SKIP.

## Phase 7 steps 1 and 2: audit on synthetic data (2026-10-31)

`tools/phase7_synthetic.py --reps 100`: share of 100 independent synthetic logs per cell on which
the audit's overall result was FAIL.

| case | 300 rounds | 1,000 | 3,000 | 10,000 |
|---|---|---|---|---|
| fair deal | 1% | 0% | 2% | 1% |
| first side's win rate +3 points | 1% | 14% | 59% | 100% |
| 5% of rounds dealt from the wrong side | 100% | 100% | 100% | 100% |

- Fair data: false alarms at the 1% design rate (2/100 at 3,000 is within sampling noise of 1%).
- Injected 3-point bias: caught in every replicate at 10,000 rounds, the size the plan states;
  not reliably below about 3,000. A two-hour capture (a few hundred rounds) **cannot** detect a
  bias of this size. Its purpose is to prove the capture is correct, not to test the game.
- Dealing-order error: caught by the integrity family in every replicate at every size.

Steps 1 and 2 pass. The tests in `tools/test_tools.py` repeat one replicate of each case.
