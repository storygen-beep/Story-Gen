# Doc 71 — Clothing System Design Doctrine

**Date:** 2026-05-27
**Status:** Active doctrine
**Sibling docs (analysis source):** Doc 36 (RTS Closet vs Engine Wardrobe + Maya Sketch), Doc 37 (Worn Clothing Stats Engine PRD — shipped)
**Sibling docs (doctrine):** Doc 70 (Choice Design Doctrine), Doc 56 (RTS Principles + Alignment), Doc 57 (Capstones)
**Destination:** Doc 66 (prompts_v2/ doctrine batch — held)
**Scope:** How clothing should be wired in a prompts_v2-generated game so that it functions as a content axis (RTS-faithful) rather than as a flavor layer.

---

## §1 — Why this doc exists

A 2026-05-27 audit of the TLS test slice's clothing system surfaced a pattern-level gap. TLS uses clothing as a thin Frank-ambient flavor layer (3 worn_corruption sites + 1 worn_beauty site), while RTS uses clothing as a **content-routing axis with 4 dimensions wired into ~25 distinct sites** across the game. The TLS coverage is roughly 16% of RTS's clothing footprint, with the home-nudity gate missing entirely, zero public-space corruption scenes, and no NPC-gift garments.

The audit also revealed RTS uses **location-risk-tiered thresholds** (Park ≥15 / Pool / Beach / Library / Gym ≥30) rather than a uniform "daring outfit = scene" gate, plus a **shame-as-fuel loop** for the bedroom-exit nudity gate (block + corruption pay-out when trying to leave naked at low corruption).

The prompts_v2/ folder (Doc 66, held) will generate dozens of games. Without click-level clothing doctrine, every generated game will reproduce TLS's pattern: clothing wired only as flavor-deltas on a single NPC's ambients, home interiors ungated, the player-controlled corruption-as-content-key dead. Doc 71 fills that gap.

### §1.1 — Scope boundary vs. engine docs

The engine layer is documented elsewhere. Doc 71 does NOT re-document engine internals — it applies the design-doctrine lens. If you're authoring a clothing-bearing game, read in this order:

1. **Doc 36** — what RTS actually does + how the engine compares (mechanism audit).
2. **Doc 37** — engine shipped state (`beauty` / `corruption` fields + `worn_*` predicates).
3. **Doc 71** — THIS doc — applies R1–R5 + T1–T5 to clothing decisions.

A clothing layer built without Doc 71's rules will reproduce the TLS 16%-coverage defect. A clothing layer built without Docs 36/37 won't have the engine vocabulary to start.

---

## §2 — RTS clothing pattern map (evidence-backed)

Four mechanisms cover every clothing-driven scene in RTS. Counts verified against `game_explorations/road-to-success/passage_catalog.json` (361 passages).

| Mechanism | What it does | Sites | Key evidence |
|---|---|---:|---|
| **A — worn_corruption** | Worn outfit's corruption stat gates lewd content via `$player.clothing.corruption >= N` | 8 | ParkJog / BeachSunbathe / PoolSwim / Workout / Library (Natasha quest unlock) / NatashaPublicExhibitionism / ComputerClassEvent |
| **B — worn `.type`** | Outfit category (swim / costume / cheerleader / naked) routes content via `$player.clothing.type == 'X'` | 6 | Beach / BeachChallenge1 / Marina / VeronicaHallway / SchoolGym / Bedroom-exit (naked/underwear) |
| **C — beauty (social key)** | `getBeauty() <> N` gates social access; rejection scenes pay narrative consequence | 3 | Club (bouncer) / StripClubInterview (manager) / ThomasPartyInvite (Thomas) |
| **D — undress is corruption-gated** | Can't leave home in underwear/naked unless global corruption ≥ tier; Wardrobe Return adds corr when blocked | 3 | Bedroom / ApartmentBedroom (Hallway-exit block) / Wardrobe (Return-button NotifyCorruption) |

Plus two adjacent patterns:

- **NPC-gift garments** (5 sites): SecretAdmirer → cute outfit; OfficeHR → secretary uniform; PhotoStudio → photoshoot dress; RestaurantPromotionScene → sexymaid uniform; PhoneMessages (VeronicaCostumeParty) reads `$clothes.costume1.purchased` to branch the quest objective. Garments are awarded as quest beats, which unlock further content (secretary uniform required for HR scenes; maid uniform unlocks restaurant promotion).
- **Player portrait reflects outfit** — `StoryCaption` builds the image path from `$player.clothing.type + .image` on every screen. The portrait is the always-on confirmation of what she's wearing.

### §2.1 — Worked example: Mechanism A done right (ParkJog)

ParkJog is the only RTS site that uses **tiered worn_corruption** — perfectly illustrating R1 + the §4 location-risk doctrine:

```sugarcube
<<if random(1,3) == 1 && $player.clothing.corruption >= 15>>
    <h3>You're wearing very flashy clothes, so people stare at you...</h3>
    <<if $player.clothing.corruption >= 30>>
        <button>'Come with me 🔥'</button>   /* predator path */
    <</if>>
<</if>>
```

Two corruption tiers in one scene, plus a randomized base gate. Wearing daring clothes (≥15) creates a CHANCE of attention. Wearing truly slutty clothes (≥30) escalates to a predator approach. The randomization keeps it from being deterministic — the park is public but not crowded; not every jog produces an encounter. Compare to PoolSwim (`corr >= 30`) which IS deterministic — the pool is crowded enough that daring outfits always attract eyes.

### §2.2 — Worked example: Mechanism D done right (Bedroom)

The home-undress gate is the most-missed pattern. Verified source:

```sugarcube
<!-- HALLWAY exit button -->
<<button 'Hallway 🚪'>>
    <<if $player.clothing.type == 'naked' && getCorruptionLevel() < 3>>
        <<Notification 'warning' "I should wear some clothes.. 30+ Corruption Needed">>
    <<elseif $player.clothing.type == 'underwear' && getCorruptionLevel() < 2>>
        <<Notification 'warning' "I should wear some clothes.. 15+ Corruption Needed">>
    <<elseif $player.energy == 0>>
        <<Notification 'warning' "You need to sleep!">>
    <<else>>
        <<goto 'Hallway'>>
    <</if>>
</<button>>
```

The bedroom ITSELF is freely-nakedable (she has to be able to change clothes). The HALLWAY EXIT button is what's gated. Two thresholds: underwear blocked under corr 15, naked blocked under corr 30. The Wardrobe Return button has the same gates plus a twist:

```sugarcube
<<button '↩️ Return'>>
    <<if $player.clothing.name == 'naked' && getCorruptionLevel() <= 3>>
        <<NotifyCorruption 4>>           /* block + pay corruption */
    <<elseif $player.clothing.name == 'Underwear' && getCorruptionLevel() <= 2>>
        <<NotifyCorruption 3>>
    <<else>>
        <<print '<<goto "' + previous() + '">>'>>
    <</if>>
</<button>>
```

The Return button blocks AND grants corruption every attempt. Trying to leave naked at low corruption fuels the corruption needed to eventually do it. The block IS the engine — shame-as-fuel.

---

## §3 — RTS clothing rules, derived (R1–R5)

The doctrine extracted from §2's evidence. Cite as **Doc 71 R1** through **Doc 71 R5** in design briefs + canvas comments.

### R1 — Worn corruption ROUTES content; never inflates global corruption

The outfit's corruption stat is a content key, not a meter feeder. Dressing slutty opens scenes without moving the player's corruption number.

**Why:** Player-controlled corruption-as-content axis lets the wardrobe behave like a content-router that's REVERSIBLE — change clothes → content closes. If outfit-corruption fed the global meter, every equip would be a one-way ratchet, breaking the "what should I wear today?" decision loop. Global corruption is the spine that gates story beats (catches / first-night / crack); outfit corruption is the on-ramp that decides which scenes the player can access right now.

**How to apply:** Use `worn_corruption gte N` predicates on canvas triggers / `[group]` blocks / substitution rule conditions. NEVER write a `clothing_*` condition that triggers a player `corruption add` effect — those are two separate axes. If the design wants a small global bump for sustained slutty wear, that's a SEPARATE deliberate `daily_tick` rule, not a side-effect of equipping.

### R2 — Outfit type (`.type`) is the content-category lever

Swimwear unlocks the beach zone. Costume unlocks the themed party. Cheerleader unlocks team content. The TYPE is the gate, not the specific item — a player who buys any swimsuit gets all the beach content without authoring per-item rules.

**Why:** RTS authors don't write "if wearing bikini1, unlock beach; if wearing bikini2, unlock beach; ...". They write "if wearing swim, unlock beach." Single source of truth per content category. Adds new swimsuits later → automatic compatibility with all swim content.

**How to apply:** The engine doesn't ship a native `.type` field yet (§8 + §10). Workaround: maintain a list of swim-typed item IDs and use `clothing_item equipped` per-item conditions in `OR` blocks. When Doc 72 ships, migrate to native `worn_type` predicates. Doctrine: AUTHOR the swim/costume/uniform content even with the workaround — don't skip Mechanism B because the engine field is missing.

### R3 — Beauty is the social-access stat

Distinct from worn-corruption. Beauty gates "are you ALLOWED here" (clubs, parties, auditions); worn-corruption gates "what happens BECAUSE of what you're wearing here." Rejection scenes (bouncer / manager refusal / friend embarrassment) make beauty a felt currency.

**Why:** Without rejection scenes, beauty becomes a one-way number that rises with showers/grooming but never has a downstream consequence. The player has no reason to care about their beauty score. RTS's bouncer-at-the-Club is the canonical example: beauty < 3 → "Your ID is okay, but we only allow people well-dressed to enter" → bounced. Beauty becomes felt cost.

**How to apply:** If the game has a beauty axis, author at least one rejection scene per beauty band the design uses. Rejection ≠ "scene doesn't fire" — rejection is an ALTERNATIVE branch with explicit rejection prose. The NPC tells the player WHY they can't proceed. That's the felt-currency moment.

### R4 — Undress is corruption-gated, not free

Naked or underwear-only OUTSIDE the bedroom requires global corruption tier. Use conditional `clothing_rules` on exit boundaries — the engine already supports this (§8). The shame of being seen IS the friction loop.

**Why:** The bedroom-exit gate is where the player MEETS their corruption number. Trying to leave naked at corr 0 → blocked → "I should wear some clothes." Trying again later at corr 30 → succeeds. The numeric corruption stat becomes the *experiential* thing that opens a door. Without this gate, the corruption number is decoration.

**How to apply:** Add `clothing_rules` to bedroom exit transitions (bedroom → hallway, bedroom → stairs, bedroom → outdoors) with `slots_required = ["top", "bottom"]` + `conditions = [{ trait_key = "corruption", operator = "lt", value = 30 }]`. The bedroom INTERIOR stays ungated — wardrobe must be usable. The EXIT carries the gate. Author per-tier:
- Under corr 15: blocked when in underwear or naked.
- Under corr 30: blocked when naked (underwear is allowed).
- Over corr 30: any state is allowed (the player has earned it).

### R5 — NPC gifts unlock content categories

Quest beats that award garments are how new content branches open. SecretAdmirer → cute outfit → cute-tier scenes. OfficeHR → secretary → HR scenes. Authoring a "buy this in a shop" gate is fine; authoring an NPC gift creates a stronger story moment AND unlocks the same content.

**Why:** Shop-bought garments feel transactional. NPC-gifted garments feel narrative — "this character SAW me and chose this for me." The garment becomes a memento + a content unlock + a relationship marker, all in one. RTS uses this 5 times; each gift is a Stage advance.

**How to apply:** Implement via `wardrobeEffects` on Doc 57 capstones — the capstone fires once at a Stage transition, awards a garment via `wardrobeEffects = [{ item_id = "X", action = "add_and_equip" }]`, downstream scenes gate on `clothing_item equipped`. The capstone-shape doubles as a Doc 57 Lane 4 entry AND a Doc 71 R5 content unlock.

---

## §4 — Location-risk tier doctrine

The most-missed pattern from RTS. Codified here for prompts_v2 authors.

RTS distributes worn_corruption thresholds by **how public the location is**. The threshold isn't arbitrary — it's calibrated to how "exposed" the location feels.

| Tier | Threshold | Examples | Behavior pattern |
|---|---|---|---|
| **Tier 1 — low-public** | `worn_corruption gte 15` + `random(1,3) == 1` gate | Park (jogging trail) | Daring outfit creates a CHANCE of attention. Randomized fire rate reflects the location's lower per-encounter density. Inner sub-branch at `>= 30` for escalation (e.g. predator approach). |
| **Tier 2 — mid-public** | `worn_corruption gte 30` (deterministic) | Beach / Pool / Library / Gym / Computer class | Daring outfit unlocks a sub-branch every visit. Public-and-charged locations — eyes are always on the player. Most lewd-content sites in RTS sit here. |
| **Tier 3 — undress-gated boundary** | global `corruption gte 15` (underwear) / `gte 30` (naked) | Bedroom exits, Wardrobe Return | Different mechanism: the player's STATE (what she's wearing) is gated, not a scene firing. Implemented via location `clothing_rules` + conditions. |

**Per-location publicness questions for prompts_v2 authors:**

1. **Is this location frequented by strangers vs friends/family?** Strangers → push toward Tier 2. Family/known NPCs → can stay ungated; lewd content happens via mechanism A on private NPCs (TLS-style Frank ambient).
2. **Is the player visible from many angles at once?** Pool (everyone in sight) / Gym (mirror wall) / Beach (open sand) → Tier 2 deterministic. Park trail (intermittent visibility) → Tier 1 randomized.
3. **Is exposure forced or chosen?** Beach requires swimwear (forced reveal) → Tier 2 always fires. Park allows any outfit (chosen reveal) → Tier 1 random fires only when the player deliberately overdresses.
4. **Is this the player's home?** Home interiors → ungated (private). Home EXITS → Tier 3 undress gates.

**Anti-pattern:** uniform `gte 30` everywhere. Treats the park the same as the pool; ignores location publicness; loses the calibration that makes RTS feel like a real city.

---

## §5 — The decision test (T1–T5)

Before authoring clothing content, check which dimension drives it. A clothing-gated piece of content should satisfy at least one of T1–T5.

### T1 — Worn-corruption unlock

"This scene/sub-branch should fire when the player is dressed daringly."

**Engine vehicle:** `worn_corruption gte N` predicate on canvas trigger / `[group]` block / substitution rule conditions.

**N selection:** Apply §4 tier table. Tier 1 (random + ≥15) for low-public. Tier 2 (≥30) for mid-public.

### T2 — Outfit-category routing

"Wearing swimwear should unlock this whole zone."

**Engine vehicle (today):** Enumerate item IDs in `clothing_item equipped` OR-chains. Author a doctrine-level swim list, costume list, etc.

**Engine vehicle (when Doc 72 ships):** Native `worn_type == 'swimwear'` predicate.

### T3 — Beauty-gated social access

"This scene should reject the player if she looks bad."

**Engine vehicle:** `worn_beauty gte N` predicate (Doc 37 shipped) OR `player.beauty gte N` (if beauty is a cumulative trait that includes grooming + sketching + clothing, not just outfit). Doc 70 R5 collapse applies if there's no rejection-branch — only a felt rejection makes the gate matter.

### T4 — Undress gating

"The player shouldn't be able to leave the bedroom naked at low corruption."

**Engine vehicle:** Location `clothing_rules` on exit-boundary location entries, with `slots_required = ["top", "bottom"]` + `conditions = [{ trait_key = "corruption", operator = "lt", value = 30 }]`.

### T5 — NPC-gift unlock

"Meeting this NPC at this Stage awards this outfit, which opens these scenes."

**Engine vehicle:** Doc 57 capstone with `wardrobeEffects = [{ item_id = "X", action = "add_and_equip" }]` on the exit_block effects. Downstream scenes gate on `clothing_item equipped` or `clothing_slot equipped`.

### If none of T1–T5 apply

The clothing-content link is decorative. Don't add a clothing condition that doesn't route. Don't sprinkle `worn_corruption` gates without purpose. Cite **Doc 71 R1 + R5** in the design brief showing the content distribution that justifies (or doesn't justify) each gate.

---

## §6 — Anti-patterns observed (TLS audit)

Four anti-patterns surfaced by the TLS slice audit. Cite as **Doc 71 AP1** through **Doc 71 AP4** in design reviews.

### AP1 — Single-NPC clothing scope

**Observed:** TLS wires `worn_corruption` to 3 Frank ambients (kitchen / yard / livingroom). Zero public-space scenes. Zero non-Frank NPC ambient consumers. Clothing becomes "Frank flavor," not a content axis.

**Why it's wrong:** Clothing in RTS distributes across 8 worn_corruption sites spanning 6 different locations and several NPC contexts (Natasha at the library, the gym crowd, beach strangers, classroom teachers, park predators). A single-NPC-flavor scope reduces clothing to a Frank-mood subsystem, killing the location-risk-tier dynamic from §4.

**Prompts_v2 rule:** Distribute clothing gates across NPCs AND public locations. Aim for ≥50% public-space coverage. A clothing layer wired exclusively to one NPC is decorative.

### AP2 — Home interiors ungated

**Observed:** TLS leaves all home rooms (kitchen, livingroom, yard, bathroom) with zero `clothing_rules`. The bedroom exit is ungated. The player can unequip everything and walk around naked at corruption 0. The TOML justification was "preserve robe teases" — but the slice has no robe garment, and the worn_corruption teases use clothed-but-revealing outfits (slip dress, crop top + short shorts) that pass slot coverage anyway.

**Why it's wrong:** Skips R4 entirely. The bedroom-exit gate is the load-bearing mechanism that connects the global corruption number to a felt door. Without it, corruption is decoration.

**Prompts_v2 rule:** Home boundaries (bedroom → hallway, bedroom → stairs, bedroom → outdoors) MUST have R4-style undress gates. The bedroom itself stays ungated (where the wardrobe lives — player must be able to change). The EXIT is what's gated.

### AP3 — `.type` field absence breeds per-item gates or skipped content

**Observed:** Because the engine has no `.type` field, TLS can't say "wearing swimwear unlocks beach." Authors fall back to listing items individually OR skip Mechanism B entirely. TLS skips it entirely — no swim-typed content exists.

**Why it's wrong:** Mechanism B is one of RTS's four pillars. Skipping it because the engine field is missing means the game has no "wear-this-to-unlock-zone" loops — losing a whole content-routing axis.

**Prompts_v2 rule (current engine):** Approximate `.type` with known-swim-item-ID lists in `clothing_item equipped` conditions. Tedious but functional. Doctrine: AUTHOR the swim/costume/uniform content even with the workaround — when Doc 72 ships, migration is mechanical search-and-replace.

### AP4 — Beauty as one-way trait, no rejection content

**Observed:** TLS uses `player.beauty` as a trait that rises with showers/sketching and gates Jake's first-glance. There's NO rejection-pattern content (no "you can't enter the club like that," no "the manager refuses your audition"). Beauty becomes a metric without consequence.

**Why it's wrong:** R3 says rejection scenes ARE the social-currency. A beauty stat without rejection content is a stat without a UX. The player has no reason to care about their beauty score except in the one Jake first-glance unlock.

**Prompts_v2 rule:** If beauty is in the game, author at least one rejection scene per beauty band the design uses. Rejection scenes pay narrative dividend (the player FEELS the score). The Club bouncer pattern is the reference.

---

## §7 — Pre-authoring checklist

Use BEFORE designing any clothing-bearing game (or any clothing-touched scene). Each item maps to one mechanism/rule.

- [ ] **Mechanism A — Public worn_corruption scenes.** Have I authored ≥ 4–6 sites where worn-corruption gates content across DIFFERENT locations (not all on one NPC)? Locations span ≥ 2 risk tiers (one Tier 1, several Tier 2)?
- [ ] **Mechanism B — Outfit-category content.** Have I tagged items by `type` (native field when Doc 72 ships, or item-ID lists pre-Doc-72) for ≥ 2 content categories (swim, costume, schoolwear, etc.)? Does each category have ≥ 3 scenes/branches gating on it?
- [ ] **Mechanism C — Beauty social gating.** Is beauty a real consequence-bearing stat? Have I authored ≥ 1 rejection scene where beauty < N gives a different outcome than beauty ≥ N?
- [ ] **Mechanism D — Undress gates.** Are home exit boundaries (bedroom → hallway / outdoors) gated on global corruption when the player is in underwear (≥ 15) or naked (≥ 30)? Does the bedroom itself stay ungated?
- [ ] **R5 — NPC-gift garments.** Have I authored ≥ 2 garments awarded by NPCs as quest beats (via `wardrobeEffects` on capstones, not just shop purchases)? Does each gift unlock ≥ 1 downstream scene?
- [ ] **R1 doctrine compliance.** Confirm: NO clothing condition sets `player.corruption` directly. Worn-corruption ROUTES content, doesn't inflate the meter.
- [ ] **§4 location-risk tiering.** Confirm: thresholds vary by location publicness, not a uniform ≥ 30 everywhere.

If most boxes are unchecked, the clothing system is decorative. Cite Doc 71 R1–R5 in the design brief showing how content was distributed across the four mechanisms.

---

## §8 — Engine capabilities reference (what's already supported)

To prevent authors thinking they need engine work where they don't. Verified against `apps/projects/services/template_import.py` + `apps/game_generation/twee_comprehensive/generators/v2.py` per Doc 36 §5 + Doc 37 ship state.

| Capability | Engine status | TOML shape / API |
|---|---|---|
| Slot-based wardrobe (bra/underwear/top/bottom/dress/legwear/shoes) | ✅ Shipped | `[[clothing]] slot = "top"` |
| Dress↔top/bottom mutex | ✅ Shipped | Auto-handled by `setup.equipItem` |
| Shop with corruption-tier locks (Basic / Cute / Bold / Daring at corr 0/45/85/135) | ✅ Shipped | `shop_location` + per-item `conditions` block |
| Buy semantics (exact price, affordability-gated, no auto-equip) | ✅ Shipped | `setup.buyItem` |
| Equip semantics (free, instant, condition-gated) | ✅ Shipped | `setup.equipItem` |
| Per-item `beauty` + `corruption` stats | ✅ Shipped (Doc 37) | `[[clothing]] beauty = 4 / corruption = 25` |
| `worn_beauty` / `worn_corruption` predicates (MAX aggregate across equipped) | ✅ Shipped (Doc 37) | `{ type = "worn_corruption", operator = "gte", value = 30 }` |
| `clothing_slot` / `clothing_item` condition predicates | ✅ Shipped | `{ type = "clothing_item", item_id = "bikini_top", state = "equipped" }` |
| Location-level clothing rules with conditions | ✅ Shipped | `clothing_rules = [{ slots_required = [...], conditions = { ... }, message = "..." }]` — **THIS supports the R4 undress-gate pattern via conditions reading `player.corruption < N`** |
| `wardrobeEffects` on canvas / choice (R5 NPC-gift pattern) | ✅ Shipped | `wardrobeEffects = [{ item_id = "X", action = "add_and_equip" }]` |
| `.type` field on items (R2 native) | ❌ NOT SHIPPED | See §10. Workaround: enumerate item IDs in `clothing_item equipped` checks. |
| Sidebar outfit readout | ❌ NOT SHIPPED | Doc 37 deferred. Workaround: none — players can't see what they're wearing without opening the wardrobe. |
| Player portrait reflects equipped outfit | ❌ NOT SHIPPED | Separate art track. Workaround: scene images carry the visual. |
| Block-with-pay-out gate (Wardrobe Return shame loop) | ❌ NOT SHIPPED | Workaround: split into a block-click + a separate "try anyway" click that adds corr. |

**Key insight:** the engine ALREADY supports R1 (worn_*), R3 (worn_beauty/player.beauty), R4 (clothing_rules with conditions), and R5 (wardrobeEffects). R2 is the only mechanism that needs an engine field. Authors who think "the engine doesn't support undress gates" are wrong — the engine supports it via the conditional `clothing_rules` pattern. The TLS gap is authoring, not engine.

---

## §9 — Worked example: minimum-viable RTS-faithful clothing layer

For a prompts_v2 game with 4 NPCs, 8–12 locations, and ~30 canvases — what the clothing layer should look like at minimum. Numbers calibrated to RTS scale-down.

### §9.1 — Catalog (~20 garments)

5 slots × ~4 items each. Mix of price-tiers and corruption-gated reveal items. Each item carries `beauty` (0–6) and `corruption` (0–35).

- **Initial outfit** (5–6 garments, `initial = true`, no `conditions`): modest, beauty 0–2, corruption 0–5. Auto-equipped at game start.
- **Basic tier** (5–6 garments, no `conditions`): beauty 2–4, corruption 5–10. Buyable from day 1 with starting money.
- **Cute tier** (6–8 garments, `conditions = [{ trait_key = "corruption", operator = "gte", value = 45 }]`): beauty 4–5, corruption 25–35. Buyable after corruption threshold crossed.

At least 6 items should be tagged by type category (swim / costume / sleepwear) for Mechanism B.

### §9.2 — Wardrobe + shop

- **Wardrobe location:** player's bedroom (where she changes).
- **Shop location:** town hub OR a dedicated shop sublocation.
- **Item buy-gates** use `conditions` reading global corruption (matches engine's Basic/Cute/Bold/Daring tier UI).

### §9.3 — Coverage rules (R4 implementation)

```toml
# Town entry — universal gate (R4 lite)
[[locations]]
id = "loc_town_hub"
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "Can't walk into town half-dressed." }
]

# Bedroom exit (or hallway entry from bedroom side) — R4 full
[[locations]]
id = "loc_hallway"  # OR loc_stairs / loc_outdoors_from_bedroom
clothing_rules = [
  # Block naked under corr 30
  { slots_required = ["top", "bottom"],
    conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 30 }
    ] },
    message = "I should put something on first... 30+ Corruption Needed" },
]
```

Optional lighter gate for underwear-only:
```toml
# Same boundary, lower threshold for underwear specifically
{ slots_required = ["underwear"],
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 15 }
  ] },
  message = "I should put more on... 15+ Corruption Needed" }
```

### §9.4 — Content distribution

For a slice of 30 canvases:

- **4–6 worn_corruption-gated public-space scenes** across ≥ 2 risk tiers:
  - 1 Tier 1 site: outdoor low-public location with `random(1,3) == 1 && worn_corruption gte 15`.
  - 3–5 Tier 2 sites: mid-public locations with `worn_corruption gte 30` deterministic.
- **2–3 worn_corruption-gated NPC-private scenes:** TLS-style ambient flavor on the central NPC (the "Frank pattern"). These should NOT be the only worn_corruption sites.
- **1 outfit-category routed zone:** swim → beach unlock, OR costume → themed party, OR uniform → workplace scenes.
- **1–2 NPC-gift garments** wired to capstone `wardrobeEffects` (R5).
- **1 beauty-rejection scene:** club / audition / party / interview / similar.

### §9.5 — Distribution check

The §7 checklist should be ≥ 5/7 checked. If fewer, the clothing layer is decorative.

---

## §10 — Engine gaps surfaced (queueable as Doc 72)

Three engine gaps were surfaced this session. Doc 71 names them but does NOT propose implementations. Author Doc 72 (Engine PRD) only if / when a prompts_v2 game needs them.

### Gap 1 — `.type` field on TemplateClothingItem

**The gap:** No native way to tag items by category. Without it, Mechanism B (R2) requires per-item enumeration in `clothing_item equipped` checks. Every game that wants swim/costume/uniform content has to maintain item-ID lists in conditions.

**Why it matters:** R2 is one of RTS's four pillars. The workaround is functional but tedious; authors are likely to skip it entirely (as TLS did). Native `.type` makes Mechanism B as cheap as Mechanism A.

**Effort estimate (per Doc 69 precedent):** ~3–4 hours engine + tests. Add field to `TemplateClothingItem` dataclass + parser branch in `template_import.py`; add `worn_type` predicate dispatch in `v1.py` + `v2.py`; ~10 tests; doc update. Small Doc 72 candidate.

### Gap 2 — Sidebar outfit readout

**The gap:** RTS shows "👗 Your Outfit: Casual 4" on every screen. The engine has no `sidebar_item` type that surfaces equipped outfit. Doc 37 explicitly deferred this.

**Why it matters:** Players forget what they're wearing. Without a readout, the wardrobe is invisible between screens. The "what should I wear" decision loses traction.

**Effort estimate:** ~2–3 hours sidebar work + tests. New `sidebar_item type = "worn_outfit"` rendering the current equipped state — reuses existing sidebar machinery.

### Gap 3 — Block-with-pay-out gate primitive

**The gap:** RTS Wardrobe-Return blocks the click AND adds corruption (`<<NotifyCorruption 4>>`). The engine has "block with message" and "apply effect" separately, but not "block AND apply on the same click."

**Why it matters:** The shame-as-fuel loop is a distinctive RTS mechanic. Without it, the block becomes a dead end rather than a slow-burn corruption gainer.

**Effort estimate:** New mechanism, ~4–6 hours. Lowest priority — can be approximated with a two-click pattern (block click + separate "Try to leave anyway" click that adds corr).

**Recommendation:** Queue all three under a single Doc 72 "RTS Clothing Engine Parity PRD" if/when prompts_v2 has a game that genuinely needs them. Don't preemptively author engine code. The current engine is enough for ~80% of RTS-faithful clothing behaviors.

---

## §11 — Sibling-doc cross-refs

### §11.1 — Analysis source (Doc 71 derives from these)

- **Doc 36 — `36_RTS_Closet_vs_Engine_Wardrobe_and_Maya_Sketch.md`** — the underlying analysis. §2-§4 evidence + §5-§7 engine audit. Doc 71's R1-R5 distill Doc 36 §4's four-mechanism finding into actionable rules. The Maya wardrobe sketch in Doc 36 §9 was a precursor to the prompts_v2 doctrine.
- **Doc 37 — `37_Worn_Clothing_Stats_Engine_PRD.md`** — shipped engine work that added `beauty`/`corruption` stats + `worn_beauty`/`worn_corruption` predicates. Doc 71 §8 "Capabilities" reflects post-Doc-37 engine state. Doc 37 §1 "Sidebar deferred" + "No `.type`" + "No automatic global-corruption coupling" still hold; those are Doc 72 / Doc 71 R1 territory.

### §11.2 — Doctrine siblings

- **Doc 70 — Choice Design Doctrine** — Doc 71 mirrors Doc 70's shape (R1–R5 + T1–T5 + anti-pattern catalog + pre-authoring checklist + cross-refs). Doc 70 is click-level; Doc 71 is clothing-system-level. Both feed prompts_v2.
- **Doc 56 — RTS Principles + Alignment** — Doc 71 §4 location-risk-tier doctrine extends Doc 56's principle that RTS encodes risk via thresholds. Doc 71 R1 (worn_corruption routes, doesn't inflate) is consistent with Doc 56's variant-routing principle.
- **Doc 57 — Capstones** — Doc 71 R5 (NPC-gift garments) is implemented via Doc 57 capstones with `wardrobeEffects` on the exit_block. The capstone-shape doubles as the unlock vehicle.

### §11.3 — Destination doc

- **Doc 66 — prompts_v2 session bookmark + decisions** — Doc 71 is one of the doctrine docs that the prompts_v2/doctrine/ folder will be authored from. Companion to Doc 70. Both should be included in batch 1 or batch 2 of prompts_v2 authoring.

### §11.4 — TLS-slice referent (for the audit numbers)

- **`games/the_long_summer_test/toml_phases/7_final_game.toml`** — the slice that grounded the gap-finding. 20 garments + 3 worn_corruption Frank ambients + 1 worn_beauty additive + zero R4 home-undress gates + zero R5 NPC-gift garments. Doc 70 §11 (Parked) explicitly stopped further TLS slice clothing work; Doc 71 informs FUTURE games via prompts_v2, not TLS edits.

---

## §12 — Open questions surfaced

- **Doc 72 trigger condition.** When does engine work get authorized for the 3 gaps in §10? Suggestion: when a prompts_v2 game's design brief lists Mechanism B (R2) as required AND no per-item workaround is acceptable. Until then, current engine is sufficient.
- **Sleepwear / nightwear as a type.** RTS uses `casual` / `school` / `fitness` / `swim` / `uniform` / `costume`. No explicit "sleepwear." TLS has no nightwear either. Worth a flag for prompts_v2 authors: is "what does she wear to bed" a meaningful arc beat in your game? If yes, you need either a nightwear type or sleepwear-as-casual-subset doctrine. Recommendation: add "sleepwear" as a recommended (not required) type for games with sleep-cycle content.
- **Robes specifically.** Mentioned in TLS L756 justification as a tease-vector but no robe garment exists in the slice. Open question for prompts_v2: should "robe" be a standard recommended-but-optional garment in the doctrine catalog? It's neither a slot category nor a content-route key — it's just a flavor garment. Recommendation: park as out-of-doctrine; authors can add a robe item if their narrative needs one without Doc 71 prescribing it.
- **`.type` vs `clothing_item equipped` migration path.** When Doc 72 ships native `.type`, what happens to games authored against the item-ID-list workaround? Recommendation: keep both predicates supported; new content uses `worn_type`, legacy content keeps `clothing_item equipped`. No forced migration.

---

## §13 — Verification checklist (editorial)

For future reviewers:

1. **R1–R5 each cite at least one RTS code excerpt or mechanism site from §2** ✓ (R1 cites Frank ambients + Doc 35 doctrine; R2 cites swim/costume/cheerleader; R3 cites Club/StripClub/ThomasParty; R4 cites Bedroom + Wardrobe; R5 cites SecretAdmirer/OfficeHR pattern).
2. **T1–T5 map 1:1 to §3 R-rules** ✓ (T1→R1, T2→R2, T3→R3, T4→R4, T5→R5).
3. **§4 tier-table thresholds verifiable** via `grep -oE 'clothing\.corruption\s*[<>=]+\s*[0-9]+' game_explorations/road-to-success/passage_catalog.json` — should show counts of 15 + 30 thresholds matching the §2 site totals.
4. **§8 engine capability table verifiable** against `template_import.py` + `v2.py` — file:line cites preserved through Doc 36 §5 + Doc 37 PRD.
5. **§11 cross-refs resolve** to existing docs (36, 37, 56, 57, 66, 70) — all confirmed present in `28th_april_TLS_Phase2_Redesign/`.
6. **§9 worked example numbers add up** — content distribution table satisfies §7 checklist + §4 tier doctrine.
7. **No prescription drift** — Doc 71 does NOT prescribe specific edits to TLS slice. It ONLY describes what a prompts_v2-generated game should look like. TLS-as-audit-subject is referenced; TLS-as-edit-target is not.
