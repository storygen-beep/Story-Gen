# Handoff prompt

Paste everything below the line into a fresh Claude Code session opened in this repository
on branch `claude/andar-bahar-research-go3zs3`.

---

Continue the Andar Bahar research project in `research/andar_bahar/`. Read `README.md` there
first; it indexes every file and states where each of the eight phases stands. Then read
`PHASE1_REPORT.md`, `PHASE2_PROVIDERS_REPORT.md` (especially section 10) and
`PHASE5_6_SIMULATION_AND_ARCHITECTURE.md` before doing anything else. Run
`python3 observed_1xbet_tables.py` from that folder to confirm the environment works.

Context you need and must not re-derive:

- Goal as originally stated: investigate whether ₹500 can realistically become ₹10,000 at
  online Andar Bahar, with full mathematical modelling, shuffle and integrity investigation,
  simulation, and a real-time observation system. The user's operating rules: never
  fabricate probabilities; separate verified facts, assumptions and hypotheses; never claim a
  pattern guarantees a win; never recommend increasing bets to recover losses; never treat a
  losing streak as a win being due; account for limits and house edge; flag platform-integrity
  issues; never claim to have analysed data not received; never place bets or move money
  without explicit authorisation; prioritise capital preservation; do not confuse anomalies
  with manipulation; state model limitations.
- Platform chosen by the user: 1xBet, accessed at `1-x-bet-india.com`, a mirror domain not
  on 1xBet's Curaçao licence certificate. The user has said withdrawal mechanics are out of
  scope; do not raise them beyond the facts already recorded.
- Phases 1 to 5 are complete. The exact model reproduces Ezugi's own published RTP for its
  Andar Bahar table on all ten bets within 0.13 percentage points. The best achievable
  probability of reaching ₹10,000 from ₹500 is 4.48%, by bold play on the 0.9:1 side (corrected 2026-10-31: 4.79% on 1x Andar Bahar using the cards-dealt "16-25" bet; see PHASE5_6)
  (Bahar on the Ezugi tables, Andar on Evolution Super Andar Bahar). Every betting
  progression does worse. No observable information changes the next round's probability on
  any table on the account. Under the validated model, a decision-support layer's correct
  output is "skip" on every round; it is to be built so the answer is computed, not asserted.
- Nine live Andar Bahar tables exist on the account (table in README.md). Ezugi and
  Evolution tables are the verifiable ones. Ezugi Ultimate carries a 20% fee and is worse
  for the target (2.70%). ElCasino has no public footprint. Side bets are worse than the
  main bet except on the Ezugi 1x table, where cards-dealt "16-25" (98.10%) and "6-10" (97.67%)
  beat Bahar (97.85%); all bets have negative EV.
- The user supplies screenshots from an iPhone. Nothing has been bet. No account access
  exists in this session.

What is next, in order:

1. Ask the user, in one message, for the open items in README.md: laptop and OS, which
   table to observe, the minimum stake on that table, and a go-ahead to build the tools.
2. On go-ahead, build Phase 6 as specified in `PHASE5_6_SIMULATION_AND_ARCHITECTURE.md`:
   `capture.py` (Playwright, persistent Chromium profile, WebSocket frame listener on the
   game client with a DOM poll fallback, SQLite store, no code path to any bet control),
   `audit.py` (pre-registered tests with Bonferroni correction and a 300-round minimum),
   `decide.py` (EV per bet from the paytable and the model, outputs skip unless EV > 0),
   and `make_synthetic.py` (generate rounds from the model, with optional injected bias, for
   Phase 7). Put them in `research/andar_bahar/tools/`. Reuse `andar_bahar_model.py`.
3. Phase 7: run the audit on synthetic data first; it must pass on fair data and catch an
   injected 3-point bias and a dealing-order error. Then guide the user through a two-hour
   live capture without betting and verify logged rounds against screenshots.
4. Phase 8 only after Phase 7 passes, and only as the computed per-round output of
   `decide.py` on the user's live log.

Keep every claim about code or the game tied to a file, a run, or a screenshot. Keep the
reports in this folder current, in normal prose, and commit to the same branch after each
step. Do not create a pull request unless asked.
