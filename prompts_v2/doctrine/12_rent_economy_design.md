# Doctrine 12 — Rent & Economic-Pressure Design

**Sources:** Engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (rent state `:1126`, due trigger in `advanceDay` `:4811`, render intercept `:13849`, `RentDay` / `RentDay_Paid` / `RentDay_Short` passages `:14242–14379`) + `apps/projects/services/template_import.py` (read `:2382`, validator `:4167`); TLS gold-standard `[settings.rent]` (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml:634`) + its hybrid first-Sunday capstone; Late Shifts rent build (2026-06-01 — Vince the landlord, the first prompts_v2 game to ship rent correctly scoped); Phase-2 design docs (`28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §"economic engine", `10_Test_Slice_10Day_Plan.md` slice math, `11_Hint_Authoring_Guide.md` rent-crisis hint).
**Authority:** Doctrine. WHEN to use rent, how to aim it, and how to tune it. Schema lives in `schema/02_toml_schema.md` §14; this file is the design model.
**Purpose:** Rent is the simplest engine for the RTS "I Need Money" drive — but it's easy to wire it so it never fires (the scoping trap), fires too early (onboarding eviction), ends the game when you wanted leverage (wrong eviction mode), or asks for money the player can't earn yet (untuned budget). Late Shifts shipped rent mis-scoped and silently OFF for a full session. This file encodes the verified model so the next game gets it right.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[settings.rent]` enable switch), §14 (field tables + runtime flow); `schema/03_example_toml.md` §13 (verbatim worked block); `doctrine/11_clothing_design.md` §8 (the same `[settings]` scoping trap); `doctrine/01_rts_principles.md` (the money drive); `stages/02_toml_generation_prompt.md` Step 1 (`[settings.rent]` emission).

---

## §1 — Rent is the economic spine (the player's drive)

**Rule: use rent when you want a recurring, dateable money obligation that FORCES engagement with the income arcs — it is the "I Need Money" opener made mechanical.**

RTS opens every run with money pressure: the player needs cash, so they go out and engage the world. TLS adopted this directly — *"Rent is due monthly. Maya must find money OR have someone pay her rent OR leave town. This is the player drive."* (`30_TLS_Test_Redesign_PRD.md` §"economic engine"). Rent converts a soft suggestion ("you could work") into a hard clock ("Friday, $125, or else"). That clock is what makes the income channels — jobs, NPC favors, the corruption economy — matter.

Use rent when the game has: a place to live, a way to earn, and a reason the player can't just ignore money. Skip it for games with no economy or where money isn't the drive (a pure relationship sandbox). Rent is one expression of economic pressure; a game can instead lean on savings goals, debts, or purchase-gated progression — but when the drive is "keep a roof over your head," rent is the built-in system.

---

## §2 — What the engine gives you for free

The engine ships the entire rent loop; you author config + prose, not logic. (Full schema: `schema/02` §14.)

- **The clock.** On each day rollover, when the in-game weekday hits `due_day` and `start_after_flag` (if set) is satisfied, rent comes due (once/week). *As of 2026-06-01 the engine respects `due_day`* — earlier it ignored it and always fired Monday. Set `due_day` to a real day and frame the prose around it.
- **The intercept.** While rent is due, the player is redirected to the `RentDay` passage before they can do anything else — money pressure you can't click past.
- **The branch.** `RentDay` → pay (`RentDay_Paid`) or short (`RentDay_Short`). Short within grace = a warning and the week is survived; short past grace = eviction.
- **The collector.** If `collector_npc` is set, RentDay shows that NPC's name + portrait (§6).
- **The prose.** Every beat has an author override via `[settings.rent.text]` (§14.3) — use it; the defaults are generic.

What the engine does NOT give you: a "first rent paid" flag, a quest card, or any first-time framing. Those are authoring (§7).

---

## §3 — The arm-after pattern (`start_after_flag`)

**Rule: arm rent only AFTER the player has a way to pay — set `start_after_flag` to an income flag so onboarding is rent-free.**

A fresh player has the starting balance and no income yet. If rent arms on the first due day, you can evict someone before they've had a chance to earn — a frustration, not a drive. `start_after_flag` defers the entire cycle until that flag is set:

- **Late Shifts:** `start_after_flag = "hired_at_diner"`. Rent is dormant until Maya gets the job; the first Friday after hire is the first due date. Onboarding (find the diner, get hired) happens with no rent clock ticking.
- **TLS:** `start_after_flag = "first_sunday_passed"`, set by a scripted first-Sunday capstone (§7).

Leave `start_after_flag` empty only if the player can pay from turn one (rare). The flag must actually get set somewhere reachable — an income/onboarding flag the player will hit naturally.

---

## §4 — `eviction_mode`: game_end vs flag_set (the decision rule)

**Rule: choose the eviction mode by what failure should MEAN in your game. `game_end` = the run is over. `flag_set` = the world changes and play continues. Both are first-class; pick deliberately.**

| Mode | What happens | Use when | Cost |
|---|---|---|---|
| `game_end` | GAME OVER screen + restart | failure is terminal — a roguelike/survival framing where losing the roof ends the story | a hard wall; the player loses progress |
| `flag_set` | sets `eviction_flag` (e.g. `rent_evicted`), play continues | failure should have *narrative* consequence, not a wall — the landlord's leverage, a downgrade, a debt, a different arrangement | you must author what the flag DOES downstream (fail-forward) |

`flag_set` is the richer choice for an arc-driven adult game: missing rent doesn't kick the player out, it hands the collector leverage. The engine supports this with **`_soft` text variants** (`eviction_scene_soft` / `_response_soft` / `_closing_soft`) that play instead of the hard-eviction prose — write them to open the consequence, not close the game. Late Shifts uses `flag_set` so Vince's missed-rent beat becomes *"Money's one way to keep a roof. There's others."* — a leverage hook the arc can pick up. TLS likewise uses `flag_set` (`rent_evicted`).

If you pick `flag_set`, the `eviction_flag` is a real promise: author at least one downstream beat that reads it, or eviction is a dead end dressed as a consequence.

---

## §5 — Budget math: price rent to the wage

**Rule: `amount` must be clearable by the first post-arm due date with margin — tune it against the income channels, not in a vacuum.**

Rent that can't be paid isn't pressure, it's a scripted loss. Before setting `amount`, count: starting balance, income per channel, and how many earning opportunities fall between the arm flag and the first due date.

- **Late Shifts:** $60 start, +$45/diner shift, rent $125 due Friday, armed at hire. Between a Monday hire and Friday there are ~3–4 shifts (135–180) — clears 125 with margin; `grace_periods = 1` is the backstop for a bad week.
- **TLS (`10_Test_Slice_10Day_Plan.md`):** $60-equivalent weekly rent against two income channels + a comfortable starting buffer, explicitly checked so "rent fires correctly" without being a wall.

`grace_periods` is the tension dial: 0 = a single miss evicts (brutal); 1–2 = a bad week is recoverable, a pattern is not. Higher grace softens the clock. Tune `amount` and `grace_periods` together against the wage; verify the first due date is winnable in a live-play.

---

## §6 — `collector_npc`: give rent a face

**Rule: route rent through an NPC (`collector_npc`) so the obligation has a person behind it — and, under `flag_set`, a relationship that can be leveraged.**

A faceless "the landlord" works, but a named collector turns a number into a scene. RTS, TLS (Frank — rent collector AND romance arc), and Late Shifts (Vince — the building landlord) all put a person at the door. The collector's voice carries the pressure (`[settings.rent.text]` in their register), and under `flag_set` the missed-rent leverage flows naturally into their arc — Frank's rent terms feed his arc; Vince's "there's others" opens one.

`collector_npc` is an NPC slug that **must exist in `[[npcs]]`** (validator, `template_import.py:4174`). The collector does not need a schedule for RentDay to work (the passage looks them up by slug for name + portrait), but giving them light presence (a schedule window where the player can meet them) makes the rent knock land as a known face rather than a stranger — Late Shifts schedules Vince out front mornings for exactly this.

---

## §7 — The hybrid first-period pattern + surfacing the pressure

**Rule: when the first rent payment carries plot weight, hand-author it as a one-shot capstone that also sets `start_after_flag`; let the engine handle every recurring week after.**

The engine's recurring rent is uniform by design — same RentDay scene weekly. The *first* time often deserves more: an establishing beat, a choice, a flag set for downstream content. The hybrid pattern (TLS):

1. A one-shot capstone (`canvas_first_sunday_morning`) delivers the first rent narratively and sets `first_sunday_passed`.
2. `start_after_flag = "first_sunday_passed"` arms the engine — so recurring rent begins the *next* week.
3. The capstone can also set a `first_rent_paid` flag (the engine won't) for hints/branches.

Skip the hybrid (arm on a plain income flag, like Late Shifts' `hired_at_diner`) when the first payment is just the first of many.

**Surface the pressure.** Rent off-screen is weak pressure. Make it visible: a money sidebar band ("Making rent"), and — for the V2 quests engine — a rent-crisis hint that fires while rent is unpaid and softens once it's cleared (`11_Hint_Authoring_Guide.md`: a global/no-`npc_id` hint gated on `missing_flag = "first_rent_paid"` renders in the Story-Goals section). The player should always know the clock is running.

---

## §8 — Enabling checklist + the scoping trap

Rent is OFF until `[settings.rent]` turns it on, and the switch is a **silent-failure trap** if mis-scoped (the same trap as clothing, `doctrine/11` §8).

- [ ] **`[settings.rent]` table, NOT bare keys.** `enabled` / `amount` / etc. live under a `[settings.rent]` header (read at `template_import.py:2382`). Authored bare (e.g. right after `[time]` as `rent_enabled = true`), they scope under the preceding table, `data["settings"]["rent"]` is empty, and rent reads as **disabled with no error**. This silently shipped a dead rent system in Late Shifts. (`schema/02` §1.3.)
- [ ] **Correct key names.** `enabled` / `amount` / `due_day` / `grace_periods` — NOT `rent_enabled` / `rent_amount` / `rent_due_day`. A verbatim move of the bare keys still fails; rename them.
- [ ] **`amount > 0`** and **`due_day`** is a full weekday name (validator).
- [ ] **`collector_npc` exists** in `[[npcs]]` if set (§6, validator).
- [ ] **`start_after_flag` is reachable** — armed by a flag the player will actually set (§3); empty only if payable from turn one.
- [ ] **`eviction_mode` chosen deliberately** (§4); if `flag_set`, the `eviction_flag` has at least one downstream consumer (and `_soft` text authored).
- [ ] **`[settings.rent.text]` authored** as a SUB-table (not a multi-line inline table — breaks `tomllib`), using the real keys (`schema/02` §14.3).
- [ ] **Budget tuned** — first post-arm due date is clearable with margin against the income channels (§5); verified in a live-play.

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[settings.rent]` enable switch (the scoping fix).
- `schema/02_toml_schema.md` §14 — `[settings.rent]` field tables + runtime flow + `[settings.rent.text]` keys.
- `schema/03_example_toml.md` §13 — verbatim rent excerpt (`[settings.rent]` + `[settings.rent.text]` + the hybrid pattern).
- `doctrine/11_clothing_design.md` §8 — the identical `[settings]` scoping trap.
- `doctrine/01_rts_principles.md` — the "I Need Money" money drive rent serves.
- `stages/02_toml_generation_prompt.md` Step 1 — `[settings.rent]` emission.
- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §"economic engine"; `10_Test_Slice_10Day_Plan.md` (slice math, F4 rent test); `11_Hint_Authoring_Guide.md` (rent-crisis hint).

---

**End of file.** A rent system that passes §8 is enabled correctly and aimed correctly: it gives the player a dateable money clock (§1–§2), holds off until they can pay (§3), fails in the way the story needs (§4), asks for an amount they can earn (§5), wears a face (§6), and stays visible on screen (§7).
