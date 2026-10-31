# Andar Bahar research — index and state

Project: can ₹500 become ₹10,000 playing online Andar Bahar on 1xBet, and is the game
as implemented trustworthy. Started 2026-10-30. Branch: `claude/andar-bahar-research-go3zs3`.

## Files

| file | what it is |
|---|---|
| `PHASE1_REPORT.md` | Rules, exact probabilities, house edge, round length, reach-probability ceiling |
| `PHASE2_PROVIDERS_REPORT.md` | Ezugi / Evolution / Pragmatic / Vivo research, 1xBet licensing and enforcement, comparison matrix, the tables actually on the account (section 10), model validation against Ezugi's published RTP |
| `PHASE5_6_SIMULATION_AND_ARCHITECTURE.md` | Reach probabilities on the real tables, Ultimate sensitivity, observation and audit architecture, Phase 7 test plan |
| `HANDOFF_PROMPT.md` | Prompt to resume this work in a fresh session |
| `andar_bahar_model.py` | Exact model: first-match distribution, side probabilities, EV, bold-play and flat-bet solvers, vectorised Monte Carlo of progressions |
| `provider_tables.py` | Prices every paytable collected from research sources |
| `observed_1xbet_tables.py` | Prices the three tables read off the account, validates against Ezugi's published RTP, First 3 conditional on joker rank |
| `table_simulation.py` | Phase 5 on the real tables, including the Ultimate fee-and-multiplier sensitivity case |

All scripts: `python3 <file>` from this folder. Only dependency is numpy.

## State of the eight phases

| phase | status |
|---|---|
| 1 Game research | Done. P(first-card side) = 429/833 = 51.5006%. House edge 2.15% at 0.9:1, 3.00% at 1:1. |
| 2 Shuffle investigation | Done. All tables on the account: one physical deck, machine or dealer shuffle every round. No provably-fair scheme anywhere. |
| 3 Casino integrity | Done to the extent possible from outside. 1xBet: Curaçao licence to Caecus N.V.; user's domain is an unlisted mirror; long enforcement record; ED proceedings in India. Providers: Ezugi and Evolution verifiable; ElCasino not. Michigan orders document dealer manipulation at Evolution, caught by a regulator. |
| 4 Mathematical model | Done and validated: reproduces all ten of Ezugi's published RTP figures within 0.13 points. |
| 5 Simulation | Done. Ceiling 4.48% by bold play on the 0.9:1 side; every progression lower; Ultimate 2.70%. |
| 6 Architecture | Designed, not built. Awaiting a laptop and a go-ahead. |
| 7 Controlled testing | Not started. Plan written. |
| 8 Decision support | Not started. Under the validated model its output is "skip" every round. |

## Decisions made by the user

- Platform: 1xBet (domain in use `1-x-bet-india.com`).
- Withdrawal mechanics out of scope by user instruction. Facts recorded: min ₹1,000, max ₹50,000, 72 h, bank transfer.
- No bets placed at any point. Operating rules from the original brief remain in force
  (never fabricate probabilities, never recommend chasing losses, never bet without explicit authorisation).

## Facts about the account's tables (from screenshots, 2026-10-30)

| table | provider | first card | 0.9:1 side | notes |
|---|---|---|---|---|
| 1x Andar Bahar (1xLIVE) | Ezugi dedicated | Bahar | Bahar | Published RTP Bahar 97.86%, Andar 96.99%. Sides 2.5/3.5/4.5/3.5/14/24/49/119 |
| Andar Bahar | Ezugi | Bahar | Bahar | Standard table, same paytable |
| Ultimate Andar Bahar | Ezugi | Bahar | Bahar | 20% fee, virtual multiplier draw, RTP Bahar 97.82%, Andar 97.44% |
| OTT Andar Bahar | Ezugi | not read | | extra betting rounds, not captured |
| Super Andar Bahar | Evolution | Andar | Andar | 501 players seated; ten side bets with multipliers |
| Andar Bahar | ElCasino (TV Games) | Andar | Andar | Barcode scanner, shuffling machine, two betting rounds, 1st Andar 15:1, 1st Bahar 15.5:1, First 3 120/8/5, cards dealt 2 to 800:1; provider has no public footprint |
| M Andar Bahar | SA Gaming | not read | | |
| Andar Bahar | Playtech | not read | | |

## Open items

1. Laptop availability and OS for the Playwright capture tool.
2. Table to observe (recommended: Ezugi standard / 1x Andar Bahar, or Evolution Super).
3. Minimum stake on the chosen Ezugi table (the ₹20 in the simulation is ElCasino's minimum).
4. Go-ahead to write `capture.py`, `audit.py`, `decide.py` per the Phase 6 design.
