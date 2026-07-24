# The clothing system — axes, the two-part rule, tiers, the coverage gate, enabling

Read this when the game uses the clothing/wardrobe system — declaring the catalog, gating a public event
on the outfit, wiring the exhibitionism meter, or stopping the player going out underdressed. It is the
DATA + DESIGN model for clothing; the trait facts it leans on (corruption, exhibitionism) live in
`references/trait-catalog.md`, and the one build-breaker (`clothing_rules` / `slots_required`) is owned by
`references/toml-gotchas.md` — this file cross-links rather than re-derives it.

**Every engine claim here is verified against live code** (`v2.py` = the comprehensive generator;
`template_import.py` = the importer/validator), cited `file:line`. Where the old corpus draft disagreed,
the **code wins** and the divergence is flagged inline with a `*(code-vs-lore note: …)*`.

## Contents
- §1 — The four axes and which gates what
- §2 — The load-bearing two-part rule (clothing gates PUBLIC, never an NPC arc)
- §3 — `worn_corruption`: the live public-event key (WEAN)
- §4 — `worn_beauty`: the social key (distinct from corruption)
- §5 — `exhibitionism`: the ratchet meter
- §6 — `worn_type`: outfit-category gate (bonus axis)
- §7 — Tiering & economy (the load-bearing going-out tier)
- §8 — The coverage gate ("can't go out underdressed")
- §9 — Enabling / scoping checklist

---

## §1 — The four axes and which gates what

Clothing is **two live outfit-derived keys (`worn_corruption`, `worn_beauty`), a stored `exhibitionism`
meter, and the global-`corruption` spine** — plus an optional fourth live outfit key, `worn_type` (§6).
Keep them separate; collapsing any pair is the most common design error. Every predicate below is a real
`type` the engine evaluates in `triggerConditionsSatisfied` (`v2.py:3747-3782`, the worn_* predicate block).

| Axis | What it is | How it reads | Gates | Predicate `type` |
|---|---|---|---|---|
| **`worn_corruption`** | how revealing the *currently equipped* outfit is | **live**, MAX over equipped items (`getWornStatMax`, `v2.py:1361-1380`); take the outfit off and the gate closes | PUBLIC / world events | `worn_corruption` |
| **`worn_beauty`** | how *good* the outfit looks | **live**, MAX over equipped items (same aggregate) | SOCIAL reception / venue access | `worn_beauty` |
| **`exhibitionism`** | a persistent "how shameless am I" meter | a stored `[player.core_traits]` trait — **ordinary trait, no decay**; you raise/gate it like any other | flash payoffs, combined with `corruption` | `trait` (`trait_key="exhibitionism"`) |
| **`corruption`** (the spine) | overall transgression | stored player trait | NPC arcs + the *right* to go out underdressed + buy-gating the revealing tier | `trait` / `corruption_level` |

The contract: **`worn_corruption` / `worn_beauty` are live keys you HOLD** (change clothes → the next render
re-reads them — `getWornStatMax` iterates `player.equipped` every call, `v2.py:1367-1378`).
**`exhibitionism` is a RATCHET** (acts raise it, it never falls). **`corruption` is the SPINE** everything
sits beside. Wearing a `corruption=30` outfit raises `worn_corruption` to 30 but leaves global `corruption`
untouched — the aggregate "ROUTE content; they never touch the global player.corruption trait" (engine
comment, `v2.py:1360`). They are different quantities and the engine treats them as such.

*(Code-vs-lore note: the old corpus called `worn_beauty` a "derived stat, don't store it." Correct — but
note there is **no `getBeauty()` engine macro**; the value comes from `setup.getWornBeauty()` =
`getWornStatMax('beauty')` (`v2.py:1381`). RTS-lore function names like `getBeauty`/`getExb`/`getCorruptionLevel`
quoted in the draft are RTS source, NOT this engine — don't cite them as ours.)*

---

## §2 — The load-bearing two-part rule (the single most important clothing rule)

**Clothing MAY gate PUBLIC/world content + the exhibitionism meter, AND may trigger ambient Lane 2/3
reactive-world events (a stranger groping/cornering/commenting). It must NEVER gate an NPC's escalation
spine / arc progression — that is the backwards on-ramp.**

The split:
- **PERMITTED — public surfaces.** Strangers, customers, passers-by, the reactive world. A street stare at
  `worn_corruption >= 15`; a bigger customer tip at `>= 25`; a Lane 2 ambient where a drunk corners her on a
  revealing-outfit `chance` roll. These ARE "public content" — the outfit routes *what the world does to her*.
- **FORBIDDEN — an NPC's arc.** A housemate's first-notice, his hub, his escalation rung, his sex scene.
  Those gate on **global `corruption` + `arousal` + `relation` + flags** — who she's *become*, never what she
  threw on this morning. Putting a `worn_*` predicate on a canvas whose `npc` / `requires_npc` field is set
  is the **backwards on-ramp** (`references/trait-design.md` — the arc's front door locked with a key found
  only by grinding a *different* system).

**The self-audit:** catch yourself writing a `worn_corruption` / `worn_beauty` predicate on a canvas that
names a tracked NPC → stop. Either the beat belongs on a public surface (no `npc`/`requires_npc`), or the
gate belongs on global `corruption`. (A reactive Lane 2 *ambient* is fine to outfit-gate — it's an
in-character world reaction, not the NPC's own arc rung. The distinction is arc-spine vs reactive-world.)

This is the one rule a clothing system most often gets *wired correctly and aimed wrong* — green build, dead
arc. Aim it at the world.

---

## §3 — `worn_corruption`: the live public-event key (WEAN)

**`worn_corruption` gates PUBLIC reactions — strangers, customers, passers-by — read live every render,
granting ZERO global corruption.**

- **MAX-aggregate, live** (`v2.py:3751-3761` → `getWornCorruption` → `getWornStatMax('corruption')`,
  `v2.py:1382`): returns the highest `corruption` among equipped items. `operator` defaults to `gte`,
  `value` defaults to 0 (`v2.py:3753-3754`). Change clothes, next render re-reads. A key you hold, not a
  level you bank.
- **WEAN — Wardrobe-Effect-Adds-Nothing.** A `worn_corruption` beat is prose/flavor only — it must NOT
  carry `effects` that raise global `corruption`. The outfit ROUTES content; corruption advances through the
  arc/economy, not through getting dressed. (Mirrors the engine's own contract — the worn aggregates "never
  touch the global player.corruption trait," `v2.py:1360`.)
- **Two-tier pattern:** a first-notice tier (`>= 15`) and an overt tier (`>= 25`–`30`) on the SAME public
  surface — glances/bigger tips low, open reaction high.
- **Where to host:** public surfaces with an implied audience — the town street, a park, a shop floor, a
  workplace with customers. Never a private room, never an NPC-arc canvas (§2).

Shape:
```toml
[canvases.trigger.conditions]
version = "1.0"
items = [ { type = "worn_corruption", operator = "gte", value = 15 } ]
```

---

## §4 — `worn_beauty`: the social key (distinct from corruption)

**`worn_beauty` gates SOCIAL reception and access — being treated well, being let in — NOT sexual content.**

Beauty and corruption are orthogonal: a put-together outfit can be high-beauty / low-corruption (a nice
dress), or the reverse (revealing but cheap). Same live MAX aggregate as §3 (`getWornStatMax('beauty')`,
`v2.py:1381`; predicate at `v2.py:3751-3761`). Use it for: warmer stranger reception, entry to a nicer venue,
a better tip class — "she looks good tonight, the room is kinder." Keep it OFF sexual gates; that's
corruption's job. Don't store beauty as a player trait — it's outfit-derived and would desync the moment she
changes.

---

## §5 — `exhibitionism`: the ratchet meter

**Exhibitionism is a stored player trait raised ONLY by public flash/expose ACTS, with NO decay; it then
gates payoff content combined with global corruption.**

- **No engine support needed** — it's an ordinary `[player.core_traits]` trait (`references/trait-catalog.md`
  §2: 0–100, default 0, no decay). Raise it with a normal effect
  (`{ targetType = "player", trait = "exhibitionism", op = "add", value = N }`); gate on it with a normal
  `{ type = "trait", subject = "player", trait_key = "exhibitionism", operator = "gte", value = N }`.
- **Monotonic — no daily decay.** Do NOT add it to `[engine.daily_tick].traitEffects` (there is no hardcoded
  passive — the tick only applies what you author, `v2.py:5255-5275`).
- **Raised ONLY by ACTS, never by wearing.** This is the one place a clothing-adjacent choice mutates a
  stat: a deliberate *flash/expose ACT* on a public canvas (usually itself gated `worn_corruption >= 25` so
  she's dressed for it) grants `+exhibitionism`. Merely wearing revealing clothes raises `worn_corruption`
  (live) but NOT exhibitionism — the ratchet only turns when she *acts*.
- **Payoffs combine the meter with the spine:** bolder public content gates `exhibitionism >= N` AND
  `corruption >= M` — a light payoff at `exb >= 10`, a bold one at `exb >= 30 && corruption >= 50`.

Declare exhibitionism only when the premise uses public/display content (`references/trait-catalog.md` §2 —
an axis that climbs but gates nothing is a dead meter). Surface it on a sidebar item if used.

---

## §6 — `worn_type`: outfit-category gate (bonus axis)

A fourth, optional live predicate. `worn_type` returns true when ANY equipped item declares a matching
`type` string (`getWornTypes` collects unique non-empty `type` tags across equipped items, `v2.py:1388-1407`;
predicate at `v2.py:3766-3782`). `operator` is `eq` (member) or `neq` (not member); empty value never matches.

- Tag a catalog item with `type = "swim"` (or any string), then gate a pool/beach scene on
  `{ type = "worn_type", operator = "eq", value = "swim" }`.
- **The `type` field is an open string, not a closed allowlist.** The importer warns (does NOT error) if a
  `worn_type` predicate names a value no catalog item declares (`template_import.py:1205-1209`), and emits an
  INFO note if the value is outside the soft `RECOMMENDED_CLOTHING_TYPES` set
  (`casual / swim / costume / schoolwear / fitness / uniform / sleepwear`, `template_import.py:163-165`). Use
  any string you like; the warning is a typo-catch, not a rule.
- This is the "right costume for the scene" gate — orthogonal to corruption/beauty. Optional; most games
  don't need it.
- **If the state-reactive player portrait is on, the same `type` tag also drives the portrait image.** Add
  a new outfit `type` and you must add a matching `[[player_portrait.outfits]]` rule + image, or wearing it
  silently shows the portrait's `default_image` (the importer warns at build). See
  `references/player-portrait.md` §4.

---

## §7 — Tiering & economy

**Rule: catalog tiers map to the corruption arc and are priced to the game's wage; the starting outfit
covers every slot so the player is NEVER naked/blocked.**

The seven slots are fixed: `bra / underwear / top / bottom / dress / legwear / shoes`
(`VALID_CLOTHING_SLOTS`, `template_import.py:158`). A `dress` occupies the `top`+`bottom` slots (equipping a
dress nulls both, `v2.py:1327-1330`; and a dress satisfies a `top`/`bottom` coverage requirement, §8).

| Tier | Buy-gate | beauty | corruption | price | purpose |
|---|---|---|---|---|---|
| **Starting outfit** | `initial = true` (free, pre-equipped) | 0–2 | 0–5 | 0 | full slot coverage so the player is never naked/blocked at game start |
| **Basic** | ungated | 2–4 | 5–12 | cheap (1–2 shifts' wage) | everyday nicer pieces |
| **Going-out** | **ungated** | ~4 | **15–20** | low-mid | **the load-bearing tier** — makes `worn_corruption >= 15` public events reachable EARLY |
| **Revealing** | buy-gated `corruption >= N` | 4–5 | 25–35 | mid-high (multi-shift save) | the overt tier; the buy-gate ties acquisition to the arc |

**Why the going-out tier is load-bearing.** Without an *ungated* item at `worn_corruption 15–20`, every
public clothing event (§3) is locked behind buying the revealing tier — which is itself locked behind global
corruption. That makes the clothing system **a backwards on-ramp on itself**: the player can't reach the
content that earns the corruption that unlocks the clothing that reaches the content. Always seed the
ungated going-out tier so the first `worn_corruption` events are reachable before she's ground much
corruption.

**`initial = true`** items go into BOTH the starting wardrobe and the starting equipped outfit, one per slot
(`v2.py:1014-1027`, the `initial_wardrobe`/`initial_equipped` build) — cover every slot or she starts under-equipped and the coverage gate (§8) can't be
satisfied from turn one.

**Pricing & the buy-gate.** Price the whole catalog against the game's income (a worked example: $60 start /
$45 a shift / $125 rent → basics affordable in 1–2 shifts, revealing tier a multi-shift save). The buy-gate
is the item's own `conditions` block, checked at purchase AND at equip:
- `buyItem` (`v2.py:1677-1704`) requires `money >= price` (`:1691`) AND `triggerConditionsSatisfied(item.conditions)`
  (`:1694`) before debiting money + adding to wardrobe; on a gate miss it toasts "Not yet — needs …".
- `equipItem` re-checks `item.conditions` (`v2.py:1324-1325`) — a buy-gate stays enforced even if equipped
  some other way.
- **Make the buy-gate a `corruption gte` condition specifically.** The shop UI reads the FIRST
  `trait_key="corruption", operator="gte"` value via `getCorruptionThreshold` (`v2.py:1609-1618`) to draw the
  "🔒 Corruption N+" badge (`v2.py:1805`). A buy-gate written any other way still *enforces* (it runs through
  the generic evaluator) but won't render a clean threshold badge.

  ```toml
  [[clothing]]
  id = "mini_dress"
  name = "Backless mini dress"
  slot = "dress"
  price = 90
  beauty = 5
  corruption = 30
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 } ] }
  ```

  *(Code-vs-lore note: the shop's section headers are hardcoded UI bands keyed off the item's gate THRESHOLD,
  not the player's corruption — `Basic 0 / Cute 45 / Bold 85 / Daring 135` (`v2.py:1721-1724`). So an item
  gated `corruption >= 25` files under the "Basic" header (25 < 45). These are cosmetic shop sections, not
  gates — don't design around them; design the gate value itself.)*

---

## §8 — The coverage gate ("can't go out underdressed")

**Rule: gate going-out on global corruption LEVEL via a SINGLE per-location `clothing_rule` whose
`conditions` block applies the cover-up requirement only BELOW a threshold.** Below the threshold she must
cover up; at/above it the condition fails, no rule is active, and `checkLocationClothing` returns null — she
leaves freely.

```toml
[[locations]]
id = "loc_town"
# ...
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "She can't head out half-dressed.", conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 50 } ] } },
]
```

How the engine resolves it (`checkLocationClothing`, `v2.py:1540-1580`): on entry it walks the location's
`clothing_rules` and picks the **first rule whose `conditions` are satisfied** (a rule with no/empty
conditions is auto-active, `v2.py:1557-1560`); for that rule it checks every slot in `slots_required` against
`player.equipped`, and a `dress` covers both `top` and `bottom` (`v2.py:1573`). Any missing slot → it returns
the rule's `message` and blocks the move; nothing missing → null (free). Above corruption 50 the `lt 50`
condition is false, no rule activates, `checkLocationClothing` returns null.

**The `slots_required` build-breaker — owned by `references/toml-gotchas.md`.** `slots_required` must be a
NON-EMPTY list of valid slots or the import HARD-FAILS (`template_import.py:3590-3597`:
`if not isinstance(slots, list) or not slots: errors.append("… missing slots_required")`, then each slot must
be in `VALID_CLOTHING_SLOTS` or "invalid slot"). So the coverage gate is **ONE conditional rule**, never an
empty-fallback pair — `{ slots_required = [], conditions = … }` fails validation. Full grep guard +
reject-line detail: `references/toml-gotchas.md` ("`clothing_rules` need a NON-EMPTY `slots_required`").

*(Code-vs-lore note: the old corpus cited the reject at `template_import.py:3460`. WRONG — the live check is
`template_import.py:3590-3597`, and it rejects both a missing AND an empty `[]` `slots_required`. The
`VALID_CLOTHING_SLOTS` set is at `:158`.)*

Gate the TOWN/exit location this way; leave home interiors ungated so robe/underdressed teases survive.

**A second, distinct enforcement path — `[settings.clothing_requirements]`.** Separate from the per-location
coverage gate above: `[settings.clothing_requirements].always_required = ["underwear", ...]` locks those slots
so the player can **never unequip them in the wardrobe UI** (the unequip button is suppressed —
`setup.canRemoveSlot` reads `req.always_required`, `v2.py:1491`/`:1496`, used at `:1477`). Use it for a hard
"she's never fully naked" floor. *(Caveat: the other two sub-fields, `body_coverage` and `conditional`/`until_flag`,
are parsed by the importer (`template_import.py:2266-2280`) but route only through `setup.validateClothing`,
which is **defined but never called** anywhere in the generator — so they're currently inert. Only
`always_required` is a live, consumed capability.)*

---

## §9 — Enabling / scoping checklist

The system is OFF until `[settings]` turns it on, and the switches are a **silent-failure trap** if
mis-scoped (a bare top-level key reads as disabled with no error).

- [ ] **`[settings]` table, NOT bare keys.** `clothing_enabled` / `wardrobe_location` / `shop_location` live
  under a `[settings]` header (read at `template_import.py:2241-2244`, `settings_raw = data.get("settings")`).
  Authored bare (e.g. right after a `[time]` block), they scope under the preceding table, `data["settings"]`
  is empty, and clothing reads **disabled with no error**. *(This is the same scoping trap that bites rent;
  see `references/systems.md`.)*
- [ ] **Items exist.** The catalog is the **top-level `[[clothing]]` array** (`data.get("clothing")`,
  `template_import.py:2247` — NOT under `[settings]`), parsed only when `clothing_enabled` is true. Enabled
  with zero items = empty wardrobe/shop + every `worn_*` reads 0 (`getWornStatMax` returns 0 when no equipped
  item matches). The importer does NOT warn — author the catalog (§7). **So never enable clothing before a
  garment exists, and never close a clothing beat "validated" with zero items:** the seven equipped slots
  stay null, `getUndressLevel()` returns `'naked'` **from turn 0 permanently**, and a `[player_portrait]`
  with a `naked_image` shows that as the marquee portrait forever, because nothing can ever be equipped to
  change it. (The importer validates each item but never asserts the list is non-empty — unlike the
  *adjacent* portrait check, which does error on "enabled but declares no images." Shipped exactly this way
  on The Inheritance, where a dead-rule warning got the portrait outfit rule deleted instead of the garment
  supplied.)
- [ ] **Full starting outfit** — every slot has an `initial = true` item (§7), so the player is never
  naked/blocked and the coverage gate (§8) is satisfiable from turn one.
- [ ] **Don't build a buy-canvas** — the shop and wardrobe UI are engine-auto-rendered from the `[[clothing]]`
  catalog. A clothing shop needs priced items and a `shop_location`, nothing else.
- [ ] **Wardrobe + shop locations exist and are navigable** — `wardrobe_location` / `shop_location` slugs
  must be real `[[locations]]` the player can reach (the engine injects the wardrobe/shop page there; a
  missing or unreachable slug = dead UI). The shop JS only emits when a `shop_location` is set
  (`v2.py:1607`).
- [ ] **Every `worn_*` consumer is on a PUBLIC surface** (§3) and is WEAN (no global-corruption effect);
  **zero `worn_*` predicates on NPC-arc canvases** (§2 — the load-bearing rule).
- [ ] **If exhibitionism is used:** the trait is declared in `[player.core_traits]`, has a sidebar item, and
  is NOT in the daily tick (§5).

Per-item fields the importer reads (`template_import.py:2250-2262`): `id`, `name`, `slot`, `image`,
`initial`, `conditions`, `price`, `beauty`, `corruption`, `type`. Slot must be in `VALID_CLOTHING_SLOTS` or
the catalog validation fails (`template_import.py:4273-4275`).

---

**Cross-references (in-skill only):**
- `references/toml-gotchas.md` — the `clothing_rules` / `slots_required` build-breaker (full grep guard);
  `version = "1.0"` on every `conditions` block (omit it and the gate FAILS OPEN); `itemEffects` camelCase.
- `references/trait-catalog.md` — `corruption` / `exhibitionism` ranges, defaults, no-decay, sidebar render;
  `getCorruptionLevel` tiers `[0,5,15,30,45]` (`v2.py:5624`).
- `references/trait-design.md` — the backwards-on-ramp anti-pattern; which axis drives which arc.
- `references/systems.md` — the optional-systems index (the Clothing row carries the two-part rule summary).
