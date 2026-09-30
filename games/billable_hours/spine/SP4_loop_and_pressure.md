# SP4 · Loop and pressure — Billable Hours

> [READY] · drafted 2026-09-30 · signed by LO: LO, 2026-09-30
> The rules: `references/the-spine.md` SP4 · `the-economy.md` R3, R3b, R3c, R3d, R7 · `engine.md` §26.

| decision | answer |
|---|---|
| the hold | `bill`: Martin, every Friday |
| the currency | `$`; `[settings.rent] currency_symbol = "$"` |
| a full week of the income rungs pays | **$600**: the firm shift, $70 × 5 days = $350, plus Theo's hour at its best answer, $250 × 1 (from week 2). Amended 2026-09-30 from $550 (LO) |
| the obligation, its amount and day | $250, Friday, `collector_npc = "npc_martin"`, `start_after_flag = "firm_day1_done"` (armed once she has earned) |
| does it move? | `stages = [{250, after 0}, {300, after 500}, {350, after 1400}]`, then flat (R3d: ratchet through the ignition, then plateau). `stage_lines`: Martin at breakfast: *"Your mother's card was in your name too. Three hundred from Friday."* / *"Three-fifty. That's the last number, Emma."* |
| income rises with it (R3c) | Theo's hour pays $200 at `theo_stage` 1, $300 from stage 2: the same band as the bill |
| a short week | `on_short = "carry"`: owed next week, no game over (D8d) |
| clean work alone | $350 − the bill. Covers stage 1 with $100 to spare; at stage 2 it's $50; at stage 3 it's $0. Any sink (the firm's dress code, a blouse at $80) breaks it. The transgressive route is open and well paid from week 2 (R3d) |

**Decided by LO, 2026-09-30** (the engine and the signed pages disagreed, S12; findings F4):

1. **He collects at breakfast.** The engine arms the payment at 00:00 Friday and it intercepts on her next location screen (`engine.md` §26), so the rent page is Martin at the breakfast table. WANT §2 amended.
2. **Step 1 is about the stub, not the envelope.** The money is already his; after dinner he asks for her pay stub. IDEA §4 line 2 amended.
3. **The bill rises in stages**, $250 then $300 then $350, then stays flat. WANT §2 amended.

Record in `board.economy`, `board.pressure` and `[settings.rent]`.
