# Phase 7 and Phase 8 results (1x Andar Bahar, live log, 2026-10-31 to 2026-11-01)

## What was captured

Six read-only capture runs on 1x Andar Bahar (Ezugi, game 63587, table 628000), with no bet
placed and no control clicked. Runs 2, 3, 4 and 6 produced rounds; run 1 was aborted and run 5
recorded nothing because 1xBet had logged the account out. `tools/parse.py` built 322 complete
rounds from the game's WebSocket `Card` messages, each one cross-checked against the table's own
`GAME_RESULT`; 39 rounds were left out (cut by a reload, a logout or the end of a run, or joined
part way through the deal). The log is `data/live.sqlite`, not committed because the same folder
holds the login profile.

## Phase 7 step 4: the audit on the live log

`python tools/audit.py data/live.sqlite`, 322 rounds, overall alpha 0.01 (each family fails at
p < 0.002):

| family | test | result | p |
|---|---|---|---|
| 1 winner | exact binomial | Bahar won 158 of 322 (49.07%; model 51.50%) | 0.403 |
| 2 cards | chi-square, 7 buckets | observed close to expected in every bucket | 0.748 |
| 3 joker | chi-square, 13 ranks | 19 to 36 per rank, expected 24.8 | 0.297 |
| 4 sequence | runs test and Ljung-Box lags 1-5 | no dependence between rounds | 0.594 |
| 5 integrity | rule check per round | 0 of 322 rounds break a dealing rule | n/a |

No family rejects the model: the log is consistent with a fair single-deck deal under the
published rules. That is not proof of fairness. With 322 rounds the audit can only catch large
departures; the synthetic runs (PHASE5_6, "Phase 7 steps 1 and 2") caught a 3-point bias in
the winner rate only 1% of the time at 300 rounds and 14% at 1,000. The deal-order check is
strong at any size. An anomaly in a later, larger log would still need to be ruled a capture
error before it is read as anything about the table.

Not done: Phase 7 step 3's comparison of logged rounds with the user's own iPhone screenshots.
None were supplied. The parser's cross-check compares two messages from the same server, so it
proves the capture is self-consistent, not that it matches the screen. The game-frame
screenshots in `data/shots/` are available for that check.

## Phase 8: decide.py on the live log

`python tools/decide.py --db data/live.sqlite --use-audit`. Because the winner family passes,
every bet is priced from the exact model, and the output for every logged round is SKIP:

| bet | pays | P(win) | EV per ₹1 |
|---|---|---|---|
| Andar | 1:1 | 48.50% | -3.00% |
| Bahar | 0.9:1 | 51.50% | -2.15% |
| cards 16-25 (best) | 3.5:1 | 21.80% | -1.90% |
| every other cards bet | 2.5:1 to 119:1 | | -2.33% to -8.52% |

No bet on this table has a positive expected value, so no bet is recommended at any stake.

## Answer to the original question

Can Rs 500 realistically become Rs 10,000? No. On a table the live log cannot tell apart from a
fair deal, the best possible way to play (computed in `tools/optimal_reach.py`) reaches
Rs 10,000 about 4.79% of the time and loses the whole Rs 500 about 95% of the time. No pattern
in the results changes that, and raising stakes after losses lowers it.
