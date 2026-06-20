# Economy (the fix for Gap 5) — a corruption-ladder, anti-grind income

Closes the dry-run's Gap 5 (`08` — the economy could be a grind-wall). Money is the Act-1 pressure that
*drives the cascade* (`04`); if income is one repetitive job, the heart of the game becomes the worst
grind. Grounded in `12_economy_research.md` (RTS + survey). LO calls: **one wallet — money is money (no
dirty/clean split, no laundering)**; pressure kept alive by **sinks, not a tax.**

---

## The core idea
**The economy is itself a CORRUPTION LADDER, not a job list.** Income runs legit-low-pay early →
lewd-high-pay as she falls, so **making money and corrupting herself are the same act**, and the money
pressure *pulls her down the lewd path because that's where the money is.* Earning *is* playing the
fantasy. The economy drives the cascade instead of sitting beside it.

---

## The rules
- **E1 — One wallet.** Money is money. No dirty/clean split, no laundering (dropped per LO). One number.
- **E2 — Income is a corruption ladder.** Legit-low-pay (safe, early) → lewd-high-pay (gated on
  corruption/exposure, late). The better money is always *down* the lewd path — so the broke pressure
  *is* the temptation. (RTS: legit gigs 45→110; sex work pays far more.)
- **E3 — Multiple paths** (anti-grind, quality #3): several *different* income activities, so she's never
  forced to repeat one. Blocked or bored on X → do Y. (Game-design fix: multiple forms of progression.)
- **E4 — Earning = content** (= `09` R7): every paying activity IS a lewd / reactive-world / story scene
  (work the floor revealing, cam, escort) — never a chore-click that only adds cash. No "work shift (+$20)".
- **E5 — Tiered pay (a curve, not a flat repeat):** each tier opens better-paying, dirtier work — so
  income escalates instead of grinding one rate.
- **E6 — Pressure kept alive by SINKS, not a tax.** Drop laundering's job onto *wanted* spending, so even
  when she earns well she's spending toward the fantasy (pressure via DESIRE, not friction):
  - **rent/debt that climbs** — the deadline scales as she rises (the Act-1 driver never fully dies);
  - **clothing access** — the revealing outfits (the reactive-world dial, `11`) cost money → always a wanted buy;
  - **the empire itself** — taking the bar, fixing it, recruiting girls all cost money;
  - **gifts** if an NPC arc uses them.
- **E7 — No-hardcode:** the *number* of income paths / sinks and the *pay rates* are decided per game at
  generation (the principle is fixed; the values are authored — like the per-place reactivity ceilings `11`).
- **E8 — The PRESSURE escalates across acts; it never dies** (`15` Finding E). Act-1's motor is *broke-pressure*
  (rent/debt/the shark). But once the empire earns, that squeeze vanishes — and a pressureless late game goes
  limp. So **swap the pressure, don't lose it:** the survival debt gives way to a *bigger* late threat — a rival
  madam, a crooked cop, the shark's boss, the city — that still costs money to fend off and still gives money a
  wanted use. The *form* escalates (survive → defend/grow the empire); the *presence* of pressure is constant to
  the end. (Casting carries a late-act pressure role, `06`.)
- **E9 — Recruits are ARCS, not income widgets** (`15` Finding C). When the stable earns, it is tempting to model
  a recruited girl as "+$X/day." **Don't.** Every recruit is a *full corruption arc* (her own double-lock, rungs,
  capstone, loop — a `07` core/peripheral NPC), and her "income" is a *byproduct* of playing her content. The
  empire's money comes from **content you author**, never from a passive number. (This is the economy half of the
  endgame-stays-carnal rule — see `14` P7.)

---

## Why this is anti-grind by construction
Three properties at once (each from the research): **multiple paths** (E3) + **the paths ARE content**
(E4) + **they escalate** (E5). You never "grind for money"; you pursue wanted content that happens to
pay, choosing among paths by what you want and dare. Money is a *byproduct* of playing the fantasy.

---

## How it fuses with the rest (the beautiful part)
Income, pressure, content, and desire become the **same beats**:
- the **cascade** (`04`): the money pressure is what pushes her to corrupt herself;
- the **desire ladder** (`09`): she earns *while chasing a want* (rent, the dress, the bar), never to fill a bar;
- the **reactive world** (`11`): the lewd income paths (work the floor revealing, cam, escort) ARE the
  clothing-triggered content — earning + reactivity + scene are one;
- the **machine** (`22`, form 2a): money is the **connective tissue BETWEEN arcs** — what you earn from one
  arc/activity is the *gate* to reach the next person. `13` says "earning = corrupting yourself"; the
  machine adds "earning = the thing that lets you reach the NEXT target" (work the floor / break the boss →
  *afford* the dress that turns the owner's head). So the economy isn't a meter beside the arcs; it's the
  circuit that wires them together. *(Form 2b — a payout **banded** by an NPC's trait, so corrupting him
  also pays better — is the same fusion at choice level; `22`. The output end — a *finished* arc that
  **produces** income/capability — is **G6**, deferred; reserve `E10` for it.)*
- **sinks** point money back at *wanted* purchases (clothing dial, the empire) → pressure via desire.

---

## Engine / skill reuse (implementation hook, later)
- **One `money` trait** + the existing **rent system** (`[settings.rent]`, `eviction_flag` — the climbing
  deadline = E6 pressure).
- **Income activities** = author as **Lane 3 solo-work hosts that earn** (`lanes.md` — work a shift earns
  money + is the natural Lane 3 host), gated by tier (corruption) + **clothing exposure** (`11`) for the
  lewd ones, so the paying scene *is* the reactive-world content.
- **Sinks** = rent (exists) + the clothing shop (exists, clothing system) + property/empire upgrades + gifts.
- Drop any dirty-money/laundering scaffolding — single wallet only.

---

## Worked example (bar→empire)
- **Early (legit-low):** waitress wage + modest tips — barely covers the climbing rent. Pressure is real.
- **Mid (lewd opens, pays more):** buy the low-cut top → work the floor for big tips (= the groping
  content `11` + income + advances "make rent"); a back-room gig; hustle a regular. Several paths, each a
  scene. The rent keeps climbing + the next outfit costs money → she keeps needing more → keeps falling.
- **Late (empire):** take the bar; now recruiting/corrupting girls and upgrading the place are the big
  money sinks; the stable earns. Income scaled up, sinks scaled up — pressure intact to the end.
She never grinds a shift button; she chooses which hot/story money path to chase, pushed by sinks she *wants*.

---

## Self-check
- **One wallet** (no dirty/clean, no laundering).
- Income is a **corruption ladder** (legit-low → lewd-high; better money is down the lewd path).
- **Multiple income paths**, each a *different* activity (anti-grind).
- **Every paying activity is content** (lewd/reactive/story) — no chore-clicks.
- **Tiered pay** (escalating curve, not one flat rate).
- **Pressure kept alive by scaling sinks** (rent/debt + clothing + empire + gifts), not a tax — and the sinks are *wanted* (desire, not friction).
- **Pressure escalates across acts** (E8): survival debt → late empire-threat; the squeeze never fully dies.
- **Recruits are arcs, not income widgets** (E9): empire money is a byproduct of authored content, never a passive number.
- **The economy is the machine's connective tissue** (`22` form 2a): earning from one arc/activity gates
  reaching the next — the income paths wire the arcs together, they don't just sit beside them.
- Counts/rates **authored per game**, not hardcoded.

## Cross-references
- `12_economy_research.md` (evidence) · `08` Gap 5 · `04` cascade (pressure) · `09` desire ladder (earn
  while chasing wants) · `11` reactive world (lewd income = the content) · `05` quality #3 (no grind) ·
  `22` the machine (the economy as connective tissue between arcs — form 2a/2b; finished-arc-as-income = G6).
- Engine reuse: existing `money` + rent system + clothing system + `lanes.md` Lane 3 work hosts.
