# Doctrine 11 — Clothing Design + Worn-State Predicates

**Sources:** Road-to-Success source extraction (364 passages, `game_explorations/road_to_success/passage_catalog.json`, verified June 2026 — clothing-gate conditions quoted verbatim below); Late Shifts clothing build (2026-05-31 / 06-01 — first prompts_v2 game to ship the system); TLS gold-standard catalog (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml:616–`); engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (`getWornStatMax`:1227, `checkLocationClothing`:1407) + `apps/projects/services/template_import.py` (settings read :2224, clothing items :2230).
**Authority:** Doctrine. What the clothing/wardrobe system should GATE, and how the three worn-state axes relate to global corruption. Schema lives in `schema/02_toml_schema.md` §12; this file is the design model.
**Purpose:** A game can wire clothing perfectly and still aim it at the wrong target. RTS uses clothing to drive PUBLIC/world content + a social gate + an exhibitionism meter — and NEVER to gate NPC arcs. Late Shifts initially gated an NPC's arc on the worn outfit (the backwards-on-ramp anti-pattern) and had to be re-aimed. This file encodes the verified RTS model so the next game gets it right the first time.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[settings]` enable switches), §12 (clothing items + requirements + `clothing_rules`); `doctrine/02_three_lanes_plus_capstone.md` §8.12 (backwards on-ramp); `doctrine/09_trait_catalog.md` (beauty + exhibitionism as distinct axes); `stages/02_toml_generation_prompt.md` Step 1 (`[settings]`) + Step 8 (clothing emission).

---

## §1 — The three worn-state axes (none feeds another)

Clothing in the RTS model is three independent stats plus the global-corruption spine. Keep them separate; collapsing any pair is the most common design error.

| Axis | What it is | Reads | Gates | RTS evidence |
|---|---|---|---|---|
| **worn corruption** | how revealing the *currently equipped* outfit is | live, MAX across equipped items (`getWornStatMax`, `v2.py:1227`); WEAN — never touches `player.corruption` | PUBLIC / world events | `ParkJog` `$player.clothing.corruption >= 15` (then `>= 30`); `BeachSunbathe` `> 30`; `Workout`/`PoolSwim` `>= 30`; `Library`/`NatashaPublicExhibitionism` `>= 30` |
| **beauty** | how *good* the outfit looks | live, MAX across equipped items | SOCIAL access / reception | `Club` `getBeauty() < 3` → bouncer refuses; `StripClubInterview` `getBeauty() == 0` → rejected; `ThomasPartyInvite` `getBeauty() >= 3` |
| **exhibitionism** | a persistent "how shameless am I" meter | a stored player trait, NO decay (monotonic) | flash payoffs, combined with corruption | `getExb()` raised by `<<AddExb>>` in flash acts; `StreetChallenge1` `getCorruptionLevel() >= 4 && getExb() >= 30`; `DiscountSex`/`BusRandomEvent` `getExb() >= 10` |
| **global corruption** (the spine) | the player's overall transgression | stored player trait | NPC arcs + the *right* to go out underdressed | `BrotherBedroom` sex `getCorruptionLevel() >= 3`; `Bedroom` "can't leave naked unless `getCorruptionLevel() >= 3`" |

**The rule:** worn corruption is a *live key* (take the outfit off, the door closes). Exhibitionism is a *ratchet* (acts raise it, it never falls). Global corruption is the *spine* everything else sits beside. Wearing a corruption-30 outfit raises `worn_corruption` to 30 but leaves global corruption untouched — verified live in RTS (the `Bedroom` guard treats `clothing.corruption` and `getCorruptionLevel()` as different quantities on the same line).

---

## §2 — Clothing gates PUBLIC content, NEVER NPC arcs (the load-bearing rule)

**Rule: an NPC's arc (notice / hub / escalation / sex) gates on global corruption + arousal + relationship + flags — never on what the player is wearing.**

RTS is unambiguous. Every family/romance hub gates sex with zero clothing checks:

- `MarcusBedroom`: `<<if isBoyfriend("Marcus")>>` … `<<if $player.arousal > 0>>`
- `BrotherBedroom`: `<<if getCorruptionLevel() >= 3>>` `<<if getArousal() > 0>>` `<<if $npc.Brother.relation >= 10>>`
- `DadBedroom` / `GrandpaBedroom`: `getCorruptionLevel() >= 3` / `>= 4`

None read `$player.clothing.*`. The outfit drives what happens *out in the world*; the people in your life respond to who you've *become* (corruption), not what you threw on this morning.

**Anti-pattern (the mistake Late Shifts made, then corrected):** gating an NPC's first-notice or hub on `worn_corruption` — e.g. a housemate who won't register the player until she's bought and worn provocative clothing. That is a **backwards on-ramp** (`doctrine/02` §8.12): the arc's front door is locked with a key found only by progressing a *different* system. Late Shifts' Ben B1a originally required `worn_corruption >= 15`; it was re-gated to `corruption >= 15` (global). If you catch yourself putting a `worn_*` predicate on a canvas whose `requires_npc`/`npc` field is set, stop — that beat belongs on a public surface, or the gate belongs on global corruption.

---

## §3 — `worn_corruption`: the live public-event key

**Rule: `worn_corruption` gates PUBLIC reactions — strangers, customers, passers-by — read live every render, granting zero global corruption (WEAN).**

- **MAX-aggregate, live:** the predicate returns the highest `corruption` among equipped items (`getWornStatMax`). Change clothes and the next render re-reads it. This is a *key you hold*, not a level you bank.
- **WEAN (Wardrobe-Effect-Adds-Nothing):** a `worn_corruption` beat is prose/flavor only — it must NOT carry `effects` that raise global corruption. The outfit routes content; corruption advances through the arc/economy, not through getting dressed.
- **Two-tier pattern (RTS `ParkJog`):** a first-notice tier (`>= 15`) and an overt tier (`>= 30`, Late-Shifts-scaled `>= 25`) on the same surface — glances/bigger tips at the low tier, open reaction at the high tier.
- **Where to host:** PUBLIC surfaces with an implied audience — the town street, a park, a shop, a workplace floor with customers. Never a private room, never an NPC arc canvas (§2).

Late Shifts consumers (worked example): diner-customer beat (15/30), town-street stares (25), park jogger (15), convenience-store clerk (25) — all `rts_public_clothing_*` in `5_scenes.toml`, all WEAN.

---

## §4 — `beauty`: the social key (distinct from corruption)

**Rule: `worn_beauty` gates SOCIAL reception and access — being treated well, being let in — not sexual content.**

Beauty and corruption are orthogonal: a put-together outfit can be high-beauty / low-corruption (a nice dress) or the reverse (something revealing but cheap). RTS gates *venues and welcome* on beauty (`Club`, `StripClubInterview`, `ThomasPartyInvite` all `getBeauty() >= 3`), and *exposure content* on corruption. Use beauty for: warmer NPC-stranger reception, entry to a nicer venue, a better tip class — the "she looks good tonight, the room is kinder" beat. Keep it off sexual gates; that's corruption's job.

Cross-ref `doctrine/09_trait_catalog.md`: beauty is outfit-derived (the `worn_beauty` predicate), not a stored trait — don't store it, or it desyncs when the player changes clothes.

---

## §5 — `exhibitionism`: the persistent meter

**Rule: exhibitionism is a stored player trait raised ONLY by public flash/expose ACTS, with NO decay; it then gates payoff content combined with global corruption.**

- **It needs no engine support** — it's an ordinary `[player.core_traits]` trait (declare it in `stages/02` Step 2). Raise it with a normal effect (`{ targetType = "player", trait = "exhibitionism", op = "add", value = N }`); gate on it with a normal `{ type = "trait", … trait_key = "exhibitionism" }` condition.
- **Monotonic — no daily decay.** RTS `getExb` only climbs (`<<AddExb>>`). Do NOT add it to `[engine.daily_tick]`.
- **Raised ONLY by acts, never by wearing.** This is the one place a clothing-adjacent choice mutates a stat: a *flash/expose ACT* (a deliberate choice on a public canvas, usually itself gated `worn_corruption >= 25` so she's dressed for it) grants `+exhibitionism`. Merely wearing revealing clothes raises `worn_corruption` (live) but NOT exhibitionism — the ratchet only turns when she *acts*.
- **Payoffs combine the meter with the spine (RTS `StreetChallenge1`):** bolder public content gates on `exhibitionism >= N AND corruption >= M`. A light payoff at `exb >= 10`, a bold one at `exb >= 30 && corruption >= 50`.

Late Shifts worked example: 2 flash acts (park bench, diner-3am; require `worn_corruption >= 25`, grant `+10 exhibitionism`) + 2 payoffs (`exb >= 10` recognition; `exb >= 30 && corruption >= 50` dare, `+15`).

Cross-ref `doctrine/09_trait_catalog.md` §5.3 — exhibitionism is already catalogued as a distinct axis from corruption (high-corruption + low-exhibitionism = sexually active but private; the reverse = loves being seen, not yet active).

---

## §6 — Coverage gate: conditional on global corruption, not pure slots

**Rule: "can't go out underdressed" gates on global corruption LEVEL — once corrupt enough she leaves without shame (RTS `Bedroom` parallel) — not on a flat slot requirement.**

RTS blocks leaving home naked/underwear only below a corruption level (`Bedroom`: naked needs `getCorruptionLevel() >= 3`, underwear `>= 2`). Mirror this with a **single** per-location `clothing_rule` carrying a `conditions` block that applies the cover-up requirement *only below* a threshold:

```toml
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "She can't head out half-dressed.", conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 50 },
    ] } },
]
```

Below 50 the rule applies (must cover up); at 50+ its condition fails, `checkLocationClothing` finds no active rule and returns null (she leaves freely).

**Validator gotcha:** `slots_required` must be NON-EMPTY (`template_import.py:3460` rejects `[]`). Do NOT express this as a two-rule empty-fallback (`{ slots_required = [], conditions = … }` + a cover-up rule) — the empty list fails validation. The single conditional rule above is the correct form. A `dress` satisfies both `top` and `bottom`. Gate the TOWN entry this way; leave home interiors ungated so robe/underdressed teases survive.

---

## §7 — Tiering & economy

**Rule: catalog tiers map to the corruption arc and are priced to the game's wage; the starting outfit covers every slot.**

| Tier | Gate | beauty | corruption | price | purpose |
|---|---|---|---|---|---|
| Starting outfit | `initial = true`, free | 0–2 | 0–5 | 0 | full slot coverage so the player is NEVER naked/blocked at game start |
| Basic | ungated | 2–4 | 5–12 | cheap (1–2 shifts' wage) | everyday nicer pieces |
| Going-out | ungated | ~4 | **15–20** | low-mid | the load-bearing tier: makes `worn_corruption >= 15` public events reachable EARLY, before the player has ground much global corruption |
| Revealing | buy-gated on global `corruption >= N` | 4–5 | 25–35 | mid-high (multi-shift save) | the overt tier; the buy-gate ties acquisition to the arc |

The going-out tier is what TLS lacked and Late Shifts added: without an *ungated* item at `worn_corruption 15–20`, every public clothing event is locked behind buying the gated tier, which is itself locked behind corruption — a soft backwards-on-ramp on the clothing system itself. Always seed it. Price the whole catalog against the game's income (Late Shifts: $60 start, $45/shift, $125 rent → basics affordable in 1–2 shifts, revealing tier a multi-shift save). The buy-gate uses item `conditions` (global corruption), distinct from the live `worn_*` predicates that gate content.

Late Shifts worked example: 20 items — 6 starting (free, full coverage) / 6 basic / 3 going-out (worn_corruption 15–20, ungated) / 5 revealing (buy-gated `corruption >= 25`).

---

## §8 — Enabling checklist + the scoping trap

The system is OFF until `[settings]` turns it on, and the switches are a **silent-failure trap** if mis-scoped.

- [ ] **`[settings]` table, NOT bare keys.** `clothing_enabled` / `wardrobe_location` / `shop_location` live under a `[settings]` header (read at `template_import.py:2224`). Authored bare (e.g. right after `[time]`), they scope under the preceding table, `data["settings"]` is empty, and clothing reads as **disabled with no error**. This silently shipped a dead clothing system in Late Shifts for a full session. (`schema/02` §1.3.)
- [ ] **Items exist.** `clothing_enabled = true` with zero `[[clothing]]` items = empty wardrobe/shop pages + all `worn_*` read 0. The importer does NOT warn. Author the catalog (§7).
- [ ] **Full starting outfit** — every slot has an `initial = true` item, so the player is never naked/blocked and the coverage gate (§6) is satisfiable from turn one.
- [ ] **Wardrobe + shop locations exist and are player-navigable** — `wardrobe_location` / `shop_location` slugs must be real `[[locations]]` (the engine injects the wardrobe/shop page there; a non-navigable or missing location = dead UI).
- [ ] **Every `worn_*` consumer is on a PUBLIC surface** (§3) and is WEAN (no global-corruption effect); zero `worn_*` predicates on NPC-arc canvases (§2).
- [ ] **`clothing_requirements` + `clothing_rules`** under `[settings]` / per-location respectively (§6); coverage gate conditional on corruption, non-empty `slots_required`.
- [ ] If exhibitionism is used: the trait is declared in `[player.core_traits]`, has a sidebar item, and is NOT in the daily tick (§5).

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[settings]` enable switches (the scoping fix).
- `schema/02_toml_schema.md` §12 — `[[clothing]]` items, `[settings.clothing_requirements]`, per-location `clothing_rules`.
- `schema/03_example_toml.md` — verbatim clothing excerpt (enabling `[settings]` + catalog + public event + flash act).
- `doctrine/02_three_lanes_plus_capstone.md` §8.12 — backwards on-ramp (the NPC-gated-on-outfit anti-pattern).
- `doctrine/09_trait_catalog.md` — beauty (outfit-derived) + exhibitionism (distinct from corruption).
- `stages/02_toml_generation_prompt.md` Step 1 (`[settings]`) + Step 8 (clothing emission).
- `reference/04_rts_hud_world_model.md` — RTS Outfit string + beauty/exhibitionism HUD bars.

---

**End of file.** A clothing system that passes §8 is enabled correctly and aimed correctly: it drives the world and the player's public reputation (§3–§5), gates going-out on who she's become (§6), and leaves the people in her life responding to corruption + arousal + relationship — never to what she's wearing (§2).
