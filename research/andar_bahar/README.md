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

All scripts above: `python3 <file>` from this folder. Only dependency is numpy.

### Phase 6 tools (`tools/`, built 2026-10-31)

Run with the folder's venv (`.venv`, Python 3.10: playwright 1.64.1, numpy, scipy, pytest,
websockets; Chromium installed by `playwright install chromium`). From `tools/`:
`../.venv/bin/python <file>`. Tests: `.venv/bin/python -m pytest tools -q` from this folder.

| file | what it is |
|---|---|
| `tools/common.py` | SQLite schema, the 1x Andar Bahar paytable and limits, model probabilities from `andar_bahar_model.py` |
| `tools/capture.py` | Playwright, persistent profile under `data/`, records every WebSocket frame verbatim, the game frame's text on change, one screenshot per round id. No click/type/key/mouse call anywhere (test-enforced) |
| `tools/audit.py` | Five pre-registered test families, Bonferroni at overall alpha 0.01, refuses to report below 300 rounds |
| `tools/decide.py` | EV of every bet from paytable and model; SKIP unless some EV > 0; stake output never above the table minimum |
| `tools/make_synthetic.py` | Deals real shuffled decks by the rules; optional injected win-rate bias and dealing-order error |
| `tools/phase7_synthetic.py` | Phase 7 steps 1–2: audit false-alarm and detection rates by sample size |
| `tools/optimal_reach.py` | Highest P(₹500 to ₹10,000) choosing among all bets on the table each round |
| `tools/parse.py` | Builds rounds from the game's `Card` messages in arrival order; writes a round only if it agrees with the table's own `GAME_RESULT`; leaves out rounds joined mid-deal |
| `tools/test_tools.py` | 15 tests, including capture of a WebSocket and text inside a cross-origin iframe on a local test page, and parsing of a real captured round |

`data/` is git-ignored: it holds the browser profile (with the casino login cookies), live logs,
screenshots and synthetic runs.

## State of the eight phases

| phase | status |
|---|---|
| 1 Game research | Done. P(first-card side) = 429/833 = 51.5006%. House edge 2.15% at 0.9:1, 3.00% at 1:1. |
| 2 Shuffle investigation | Done. All tables on the account: one physical deck, machine or dealer shuffle every round. No provably-fair scheme anywhere. |
| 3 Casino integrity | Done to the extent possible from outside. 1xBet: Curaçao licence to Caecus N.V.; user's domain is an unlisted mirror; long enforcement record; ED proceedings in India. Providers: Ezugi and Evolution verifiable; ElCasino not. Michigan orders document dealer manipulation at Evolution, caught by a regulator. |
| 4 Mathematical model | Done and validated: reproduces all ten of Ezugi's published RTP figures within 0.13 points. |
| 5 Simulation | Done. Corrected 2026-10-31: ceiling **4.79%** on 1x Andar Bahar, staking everything on cards-dealt "16-25" (3.5:1); bold play on Bahar 4.48%; every progression lower; Ultimate 2.70%. |
| 6 Architecture | Built 2026-10-31 in `tools/`, 15 tests pass. Round parser written against the first live frames. |
| 7 Controlled testing | Steps 1–2 passed on synthetic data (results in PHASE5_6 doc). Steps 3–4, live capture and screenshot check, next. |
| 8 Decision support | `decide.py` built; computes SKIP from the paytable (best bet "16-25", EV −1.90% per ₹1). Not run on live data until Phase 7 passes. |

## Decisions made by the user

- Platform: 1xBet (domain in use `1-x-bet-india.com`).
- Withdrawal mechanics out of scope by user instruction. Facts recorded: min ₹1,000, max ₹50,000, 72 h, bank transfer.
- No bets placed at any point. Operating rules from the original brief remain in force
  (never fabricate probabilities, never recommend chasing losses, never bet without explicit authorisation).

## Facts about the account's tables (from screenshots, 2026-10-30)

| table | provider | first card | 0.9:1 side | notes |
|---|---|---|---|---|
| 1x Andar Bahar (1xLIVE) | Ezugi dedicated | Bahar | Bahar | Published RTP Bahar 97.86%, Andar 96.99%. Sides 2.5/3.5/4.5/3.5/14/24/49/119. Limits ₹100–₹200,000. URL `casino-search?game=63587` |
| Andar Bahar | Ezugi | Bahar | Bahar | Standard table, same paytable |
| Ultimate Andar Bahar | Ezugi | Bahar | Bahar | 20% fee, virtual multiplier draw, RTP Bahar 97.82%, Andar 97.44%. Limits ₹100–₹200,000. URL `casino-search?game=67426` |
| OTT Andar Bahar | Ezugi | not read | | extra betting rounds, not captured |
| Super Andar Bahar | Evolution | Andar | Andar | 501 players seated; ten side bets with multipliers |
| Andar Bahar | ElCasino (TV Games) | Andar | Andar | Barcode scanner, shuffling machine, two betting rounds, 1st Andar 15:1, 1st Bahar 15.5:1, First 3 120/8/5, cards dealt 2 to 800:1; provider has no public footprint |
| M Andar Bahar | SA Gaming | not read | | |
| Andar Bahar | Playtech | not read | | |

## Open items

1. ~~Laptop~~ This Mac (macOS 15), confirmed 2026-10-31.
2. ~~Table to observe~~ Chosen 2026-10-31: **1x Andar Bahar**, `casino-search?game=63587`.
3. ~~Minimum stake~~ ₹100 (on-screen limits line, 2026-10-31). The ceiling does not move: bold play
   still reaches ₹10,000 with 4.48% (exact) / 4.50% (200,000-session simulation), because no
   bold-play stake from ₹500 ever falls below ₹100. (Superseded the same day: with all bets
   allowed the ceiling is 4.79%; see PHASE5_6.)
4. ~~Go-ahead~~ Given 2026-10-31; tools built.
5. First live capture (Phase 7 step 3), steps below.

## Page structure of the game (Claude in Chrome, read-only, 2026-10-31)

- The game client is a cross-origin iframe served from `play.livetables.io` inside the 1xBet page,
  on both game 63587 and game 67426. Scripts in the 1xBet page cannot read it, and the extension's
  network log showed only 1xBet's own requests. Claude in Chrome therefore sees the game only as
  screenshots; it is not a capture route. Playwright can attach to the iframe and its WebSocket
  traffic; whether round data travels as WebSocket messages is still unverified.
- Readable on screen: round id and countdown in the footer (e.g. `#17392604276`), result road of
  about 90 rounds, last seven joker ranks, and the road's own Andar/Bahar percentage summary.
- No control inside the game was clicked. Balance shown ₹0.00.

## Live capture (Phase 7 step 3), how to run it

From this folder, in Terminal:

    cd tools && ../.venv/bin/python capture.py --minutes 120

1. A Chromium window opens on game 63587. The first time, log in to 1xBet by hand in that
   window (the script never sees the password; the login stays in `data/chromium_profile/`).
   Open 1x Andar Bahar there if the page did not load it. Keep it in that first tab.
2. Leave it. Do not bet. The terminal prints frames, snapshots and round ids every 30 seconds.
3. During the two hours, take about 20 iPhone screenshots of the table at the moment a round
   ends, with the round id in the footer visible. Those are checked against the log.
4. Ctrl+C or the `--minutes` limit stops it. The log is `data/live.sqlite`, screenshots of the
   game frame per round in `data/shots/`.

After that, the frames are read and the round parser written; nothing is audited before the
parsed rounds match the screenshots.

## What the game client receives (first live captures, 2026-10-31)

- Two WebSockets open when the table loads. `engine.livetables.io` carries the game as JSON,
  one message per event: `SHUFFLE`, `PLACE_YOUR_BETS`, `NO_MORE_BETS`, one `Card` per card
  (`"CardHand":"Joker"|"Andar"|"Bahar"`, `"CardName":"6c"`) in dealing order, then
  `GAME_RESULT` with `JokerCard`, `AndarCards`, `BaharCards`, `WinningHand`. Table id `628000`.
  `*.ezvds.net` carries the video (`"stream":"ezugi_628000_hi"`), binary.
- First run (16:28) stalled after 20 seconds: the video frames were stored as base64 and the
  frames the browser sends carried the session token, session id and IP. Stopped; capture now
  records only frames received from the game host, strips identity fields, and stores binary
  frames as their length. The aborted file was scrubbed (no token, session id or IP remains)
  and kept as `data/capture_run1_aborted.sqlite`.
- Round 17400256227, as dealt: joker 6c; Bahar 9h, Andar 3c, Bahar As, Andar Kd, Bahar 3d,
  Andar Ah, Bahar Th, Andar Qh, Bahar 6d; Bahar wins. Bahar first, alternate deal, stop on the
  first matching rank: the published rules.
- `GAME_RESULT` also carries the table's last 100 winners and jokers. Those are the casino's own
  summary, not observed data, and are not used by the audit.
