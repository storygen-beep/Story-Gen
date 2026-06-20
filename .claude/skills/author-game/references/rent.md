# Rent & economic-pressure design — the recurring money clock

Read this when the game's drive is "keep a roof over your head" and you want a **dateable, recurring
money obligation** that forces the player into the income arcs — or when you're wiring `[settings.rent]`
and need the exact key set + the traps. Rent is the simplest mechanical engine for the "I Need Money"
opener: it converts "you could work" into "Friday, $125, or else."

**Every engine claim here is verified against live code** (`v2.py` = the comprehensive generator;
`template_import.py` = the importer/validator) and the shipped `games/late_shifts/`, cited `file:line`.
Where the engine and the old corpus draft disagree, **code/shipped-game wins** and the divergence is
flagged inline `*(code-vs-lore note: …)*`.

## Contents
- §1 — When to use rent (and when not)
- §2 — What the engine ships for free (the RentDay flow)
- §3 — The `[settings.rent]` key set (verified)
- §4 — The `[settings.rent.text]` prose keys (verified — the corpus once listed fictional ones)
- §5 — `eviction_mode`: `game_end` vs `flag_set`
- §6 — `collector_npc`: give rent a face
- §7 — `start_after_flag`: arm rent AFTER income
- §8 — Budget math: price rent to the wage
- §9 — The scoping trap + enabling checklist
- §10 — Pointers (don't duplicate)

---

## §1 — When to use rent (and when not)

**Rule: use rent when the game has (a) a place to live, (b) a way to earn, and (c) a reason the player
can't just ignore money.** Skip it for a pure relationship sandbox or any game where money isn't the
drive.

RTS opens every run with money pressure — the player needs cash, so they go out and engage the world.
Rent makes that mechanical: a hard weekly clock the player can't click past (§2). That clock is what
makes the income channels — jobs, NPC favors, the corruption economy — *matter*. Rent is one expression
of economic pressure; a game can instead lean on a savings goal, a debt, or purchase-gated progression.
But when the drive is "make rent," the engine ships the whole loop and you author only config + prose.

---

## §2 — What the engine ships for free (the RentDay flow)

You author config + prose; the engine owns the logic. The full loop, traced through the code:

| Beat | What happens | Where (`file:line`) |
|---|---|---|
| **The clock** | On each day rollover, `advanceDay()` advances the weekday; when the new day matches `due_day` (and `start_after_flag` is satisfied, if set), it sets `rent_state.is_due = true`. Once per week. | `v2.py:4991` (`advanceDay`), due-trigger at `:5008-5015` |
| **The intercept** | While `rent_state.is_due`, entering any `Location_*` passage or `Navigation` redirects to `RentDay` before the player can act. Saves the current passage to return to. | `v2.py:14176-14187` (redirect block) |
| **The branch** | `RentDay` → **pay** (`RentDay_Paid`, if money ≥ amount) or **short** (`RentDay_Short`). | `v2.py:14617-14660` (RentDay), `:14662` / `:14690` |
| **Grace** | In `RentDay_Short`, if `warnings < grace_periods` → a warning beat, `warnings += 1`, `is_due = false`, week survived. Else → eviction (§5). | `v2.py:14702-14753` |
| **The collector** | If `collector_npc` is set, RentDay looks the NPC up by slug for **name + portrait**; otherwise prints "the landlord". | `v2.py:14624-14631` |
| **The prose** | Every printed line has an author override via `[settings.rent.text]`; the engine defaults are generic placeholders (§4). | `v2.py:14633-14747` |

**The due-trigger logic (the Monday-bug fix).** `advanceDay` does
`var dueDay = setup.rent_due_day || "Monday"; if (days[nextIndex] === dueDay && setup.rent_enabled) {…}`
(`v2.py:5008-5009`). It compares the **new weekday against the configured `due_day`** — it does NOT
assume Monday. *(Code-vs-lore note: an earlier engine ignored `due_day` and always fired Monday; the
fix shipped 2026-06-01 and is the current behavior — confirmed at `v2.py:5008`. Set `due_day` to a real
day and frame the prose around it.)*

**State lives in `$game_state.rent_state`** — `{ last_paid_week, warnings, is_due }`, seeded at init
(`v2.py:1131-1140`). Pay resets `last_paid_week` + zeroes `warnings`; a warning increments `warnings`.

**What the engine does NOT give you:** a "first rent paid" flag, a quest card, or any first-time
framing. Those are authoring (§7 hybrid pattern). The engine sets only `eviction_flag`, and only under
`flag_set` (§5).

---

## §3 — The `[settings.rent]` key set (verified)

Read whole at `template_import.py:2399-2408` (`rent_raw = settings_raw.get("rent", {})`). Every key is
**bare under the `[settings.rent]` header** — there is no `rent_` prefix in the TOML (the `rent_*` names
are the importer's internal dataclass fields, `template_import.py:324-332`; don't write them in TOML).

| TOML key (under `[settings.rent]`) | Type | Default | Read at | Notes |
|---|---|---|---|---|
| `enabled` | bool | `false` | `:2400` | The on switch. Off (or mis-scoped, §9) = rent silently absent, no error. |
| `amount` | int | `0` | `:2401` | Weekly rent. Validator: must be `> 0` if enabled (`:4307`). |
| `due_day` | str | `"Monday"` | `:2402` | A **capitalized full weekday name** in `VALID_DAYS` (`template_import.py:2705-2713`: Monday…Sunday). Respected — don't assume Monday (§2). Validated `:4309`. |
| `collector_npc` | str (slug) | `""` | `:2403` | NPC slug; **must exist in `[[npcs]]`** if set (validator `:4313-4318`). §6. |
| `grace_periods` | int | `1` | `:2404` | Misses survivable before eviction. `0` = one miss evicts. Must be `>= 0` (`:4319`). The tension dial (§8). |
| `start_after_flag` | str | `""` | `:2405` | Arm rent only after this flag is set. Empty = armed from turn one. §7. |
| `eviction_mode` | str | `"game_end"` | `:2407` | `"game_end"` or `"flag_set"` (validator `:4321`). §5. |
| `eviction_flag` | str (slug) | `"rent_evicted"` | `:2408` | The flag set under `flag_set`. Must be lowercase snake_case if `flag_set` (`:4327`). §5. |
| `text` | sub-table | `{}` | `:2406` | The prose overrides — its own `[settings.rent.text]` header. §4. |

*(Code-vs-lore note: the corpus draft cited the collector validator at `template_import.py:4174`; the
real validation block is `:4306-4331`.)*

---

## §4 — The `[settings.rent.text]` prose keys (verified)

**Rule: author every printed line — the engine defaults are generic. Use the EXACT keys below; the
corpus once listed fictional ones.**

These are the complete set of `_rt.<key>` reads across the RentDay passages (`v2.py:14633-14747`,
extracted live). Authored as a **`[settings.rent.text]` sub-table** (a header, not a multi-line inline
table — inline `{…}` across newlines breaks `tomllib`, see `toml-gotchas.md`). The importer reads the
whole table verbatim (`template_import.py:2406`).

| Key | Where it prints | Engine default (placeholder) |
|---|---|---|
| `title` | RentDay `<h2>` (before " — Rent Day") | "Monday Morning" |
| `scene` | RentDay opening narration | a generic knock-at-the-door |
| `greeting` | collector's demand line | "Rent. $N. You know how this works." |
| `cant_pay` | the "can't pay" choice label | "Tell them you can't pay" |
| `paid_scene` | RentDay_Paid narration | hands over cash, nods, leaves |
| `paid_response` | collector's paid line | "Same time next week." |
| `paid_closing` | RentDay_Paid closing | "Another week secured." |
| `warning_scene` | RentDay_Short, within grace | you explain you're short |
| `warning_response` | collector's warning line | "Next Monday. Don't make me ask twice." |
| `warning_closing` | warning closing | "You have one week to find the money." |
| `eviction_scene` | RentDay_Short, past grace — **hard** (`game_end`) | collector doesn't wait for excuses |
| `eviction_response` | hard eviction collector line | "Locks are getting changed today." |
| `eviction_closing` | hard eviction closing (above GAME OVER) | "No negotiation. You had your chance." |
| `eviction_scene_soft` | past grace — **soft** (`flag_set`), falls back to `eviction_scene` | something shifts in how they look at you |
| `eviction_response_soft` | soft eviction collector line, falls back to `eviction_response` | "a different conversation from here on out" |
| `eviction_closing_soft` | soft eviction closing, falls back to `eviction_closing` | "the terms have changed" |

**Fallback chain (verified `v2.py:14726-14734`):** under `flag_set`, each soft line is
`_rt.X_soft || _rt.X || <default>`. So a `flag_set` game authors only the `_soft` trio; a `game_end`
game authors only the plain `eviction_*` trio. The shipped `games/late_shifts/toml_phases/0_systems_spec.toml:65-78`
is the gold-standard block — `flag_set`, so it writes the three `_soft` variants and omits the hard
ones.

*(Code-vs-lore note: an older corpus listed eviction keys as `{paid, late, evicted}` — those are
fictional; they never existed in the engine. The real keys are the 16 above.)*

---

## §5 — `eviction_mode`: `game_end` vs `flag_set`

**Rule: choose by what failure should MEAN. `game_end` = the run is over. `flag_set` = the world
changes and play continues. Both are first-class.**

| Mode | What the engine does | Use when |
|---|---|---|
| `game_end` | Prints the hard `eviction_*` prose + "GAME OVER" + a "Start Over" → `Engine.restart()` link (`v2.py:14738-14752`). | Failure is terminal — a roguelike/survival framing where losing the roof ends the story. A hard wall; the player loses progress. |
| `flag_set` | Sets `eviction_flag` via `applyAndNotifyFlag` (`v2.py:14721-14724`), zeroes `warnings`/`is_due`, plays the `_soft` prose, and offers a "Continue" link back into the game. | Failure should have *narrative* consequence, not a wall — the collector's leverage, a downgrade, a debt, a different arrangement. |

`flag_set` is the richer choice for an arc-driven adult game: a missed payment doesn't kick the player
out, it hands the collector leverage. **`eviction_flag` is a real promise** — author at least one
downstream consumer (a canvas/phone thread that reads it) or eviction is a dead end dressed as a
consequence. Late Shifts (`flag_set`, flag `rent_evicted`) wires a phone thread `vince_evicted` gated
on it (`games/late_shifts/toml_phases/8_phone.toml:288-312`) so the missed-rent beat opens a leverage
path: *"Money's one way to keep a roof. There's others."*

---

## §6 — `collector_npc`: give rent a face

**Rule: route rent through an NPC so the obligation has a person behind it — and, under `flag_set`, a
relationship that can be leveraged.**

A faceless "the landlord" works (it's the engine fallback), but a named collector turns a number into a
scene. `collector_npc` is an NPC slug that **must exist in `[[npcs]]`** (validator `:4313-4318`). The
RentDay passages look the NPC up by slug for **name + portrait** (`v2.py:14624-14631`); the
`[settings.rent.text]` lines carry that NPC's voice.

**The collector does NOT need a schedule.** RentDay resolves the NPC by slug, not by presence — the
weekly engine intercept delivers them. Late Shifts ships Vince as a **functional collector with NO
`[[npcs.schedules]]`**: he has a name, portrait, and a `relation` trait, met only via the Friday
RentDay intercept + his phone threads (`games/late_shifts/toml_phases/1_metadata_and_locations.toml:378-395`,
the file's own comment: *"a functional collector with NO physical `[[npcs.schedules]]`… He is met via
the weekly RentDay engine intercept on Friday + his phone threads, not standing presence."*).

*(Code-vs-lore note: the corpus draft claimed "Late Shifts schedules Vince out front mornings." It does
NOT — Vince has zero schedules in the shipped game. Giving a collector light presence is a valid choice
if you also want them as a standing hub, but a schedule row is a promise of a Lane 1 hub the player can
reach; don't add one unless you'll honor it.)*

---

## §7 — `start_after_flag`: arm rent AFTER income

**Rule: arm rent only after the player has a way to pay — set `start_after_flag` to an income/onboarding
flag so the opening is rent-free.**

A fresh player has the starting balance and no income yet. If rent arms on the first due day, you can
evict someone before they've earned a dollar — a frustration, not a drive. The due-trigger gates on the
flag: `var flagOk = !setup.rent_start_after_flag || State.variables.flags[setup.rent_start_after_flag]`
(`v2.py:5011-5012`) — the whole cycle stays dormant until that flag is set.

- **Late Shifts:** `start_after_flag = "hired_at_diner"`. Rent is dormant until Maya gets the job; the
  first Friday after hire is the first due date (`0_systems_spec.toml:59`).
- Leave `start_after_flag` empty only if the player can pay from turn one (rare). The flag must
  actually get set somewhere reachable — an income/onboarding flag the player hits naturally.

**Hybrid first-period pattern.** When the *first* payment carries plot weight (an establishing beat, a
choice, a flag for downstream content), hand-author a one-shot capstone that delivers the first rent
narratively AND sets `start_after_flag` — then the engine handles every recurring week after. The
capstone can also set a `first_rent_paid` flag (the engine won't) for hints/branches. Skip the hybrid
(arm on a plain income flag, like `hired_at_diner`) when the first payment is just the first of many.

**Surface the pressure.** Rent off-screen is weak pressure. Make it visible: an OPTIONAL passive
`trait_status_text` status line banded on `money` ("Making rent" — Late Shifts, `0_systems_spec.toml:278`,
money block `:271-280`). This is a status *line*, separate from the numeric money readout — the money figure
still shows as a number elsewhere (so it doesn't conflict with `trait-catalog.md` §5's "don't band the money
number"). The player should always know the clock is running.

---

## §8 — Budget math: price rent to the wage

**Rule: `amount` must be clearable by the first post-arm due date with margin — tune it against the
income channels, not in a vacuum.**

Rent that can't be paid isn't pressure, it's a scripted loss. Before setting `amount`, count: starting
balance, income per channel, and how many earning opportunities fall between the arm flag and the first
due date.

- **Late Shifts:** $60 start, +$45/diner shift, rent **$125** due Friday, armed at hire. Between a
  Monday hire and Friday there are ~3–4 shifts ($135–180) — clears $125 with margin; `grace_periods = 1`
  is the backstop for a bad week. (`0_systems_spec.toml:48-61`.)

`grace_periods` is the tension dial: `0` = a single miss evicts (brutal); `1–2` = a bad week is
recoverable, a pattern is not. Tune `amount` and `grace_periods` together against the wage; verify the
first post-arm due date is winnable in a live-play. *(Note: the flag-chain validator already treats
rent as a money **debit** context — `MONEY_DEBIT_CONTEXT` includes `"rent"`/`"due"`/`"pay"`/`"owe"`,
`template_import.py:4831` — so it won't flag rent as an unfunded payout; it only checks income flags.)*

---

## §9 — The scoping trap + enabling checklist

Rent is OFF until `[settings.rent]` turns it on, and the switch is a **silent-failure trap** if
mis-scoped — the same class as the clothing `[settings]` trap (`references/clothing.md`).

**The trap.** The importer reads `settings_raw.get("rent", {})` where `settings_raw = data.get("settings", {})`
(`template_import.py:2399`, `:2241`). The keys must live under a **`[settings.rent]` header**. Authored
as **bare top-level keys** (e.g. `rent_enabled = true` right after `[time]`), they scope under the
preceding table, `settings.rent` is empty, and rent reads as **disabled with no error**. This silently
shipped a dead rent system in Late Shifts for a full session before it was caught (`0_systems_spec.toml:24`:
*"rent was mis-scoped here as bare keys → silently OFF; fixed"*). And the TOML keys are **bare**
(`enabled`/`amount`/`due_day`) — NOT `rent_enabled`/`rent_amount` (those are the importer's internal
field names, §3). A verbatim move of bare prefixed keys still fails; use the unprefixed names under the
header.

**Enabling checklist:**
- [ ] **`[settings.rent]` table header, NOT bare keys** (the scoping trap above).
- [ ] **Unprefixed key names** — `enabled` / `amount` / `due_day` / `grace_periods` etc. (§3), never `rent_*`.
- [ ] **`amount > 0`** and **`due_day`** a capitalized full weekday in `VALID_DAYS` (validator `:4307`, `:4309`).
- [ ] **`collector_npc` exists** in `[[npcs]]` if set (§6, validator `:4313-4318`).
- [ ] **`start_after_flag` is reachable** — armed by a flag the player will actually set (§7); empty only if payable from turn one.
- [ ] **`eviction_mode` chosen deliberately** (§5); if `flag_set`, the `eviction_flag` has ≥1 downstream consumer and the `_soft` text is authored.
- [ ] **`[settings.rent.text]` authored** as a SUB-table (header, not a multi-line inline table), using the real keys (§4).
- [ ] **Budget tuned** — first post-arm due date clearable with margin against the income channels (§8); verified live.

---

## §10 — Pointers (don't duplicate)

- **The scoping-trap class + the `tomllib` inline-table rule:** `references/toml-gotchas.md`.
- **The money trait (range, sidebar render, "money stays a NUMBER — don't band it"):** `references/trait-catalog.md` §2.
- **Clothing — the sibling `[settings]` scoping trap + the income/exhibitionism economy:** `references/clothing.md`.
- **The one-line operative rule + the systems index row:** `references/systems.md` (Rent / economy row).
- **Verbatim shipped block to copy:** `games/late_shifts/toml_phases/0_systems_spec.toml:47-78`.

---

**End.** A rent system that passes §9 is enabled and aimed correctly: it gives the player a dateable
money clock (§2), holds off until they can pay (§7), fails in the way the story needs (§5), asks for an
amount they can earn (§8), and wears a face (§6) — all from `[settings.rent]` config + `[settings.rent.text]`
prose, no logic authored.
