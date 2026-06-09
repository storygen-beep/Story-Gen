# Reactive world (the fix for Gap 2) — clothing-driven lewd reactivity

Closes the dry-run's Gap 2 (`08`): "the world acknowledges your growth" had no mechanism → LC's static
wallpaper. Grounded in `10_reactive_world_research.md` (RTS ambient pool + Lustbound disposition-mediated
nudity heat). LO's calls: **the world reads CLOTHING, not traits**; reactions are **lewd/transgressive
(grope → molest → rape), never social courtesy**; the player is **sometimes choosing, sometimes taken**;
per-place ceilings are **decided per-game at generation.**

---

## The core rule
**The world reacts to what she's WEARING — not to a hidden corruption/exhibitionism number.** The outfit
has an exposure level she controls; the world reads it and **takes lewd liberties with her body** scaled
to it. Clothing is the lever; the room writes the scene. (Deliberate divergence from RTS, which also uses
corruption+exhibitionism — we use **outfit only**, for legibility + player control.)

**NOT social reactivity.** "People are nicer because she's dressed well" is out. Any tone shift with the
outfit shifts *lewder / bolder / more predatory*, never warmer.

---

## The exposure → TRANSGRESSION ladder
The more she shows, the further the world goes:
- **covered** → ignored, normal
- **low-cut / short** → stares, hands brushing "by accident," gropes in passing, crude propositions
- **barely dressed** → open groping, felt up, cornered, passed around
- **nude / extreme** → public use, gangbang, taken/raped — *where the place + people allow it*

---

## Who reacts & how far = PLACE ceiling + NPC disposition (in character)
The outfit triggers; the room decides the act, *in character* (keyed to the casting hooks `06`):
- **Predatory NPC / lawless place** → escalates to molestation / non-con / rape.
- **An NPC *designed* predatory** → gropes or takes her when she's exposed near him (his character, not generic).
- **A respectful NPC** → flustered, can't look away, a nervous touch at most — won't assault (stays in character).
- **The antagonist** → uses it / coerces / banks it as leverage.
- **A civilized public place** → capped at stares + crude comments (risk = exposure/reputation, not assault).

Same near-nude outfit → raped in the alley / worshipped-not-touched by the shy one / blackmailed by the
owner. One trigger, the room writes it.

---

## The three reaction MODES (LO answer 1 — "both," + a choice)
When a reaction fires, it lands in one of three modes — chosen by **exposure tier × place ceiling × disposition**:
1. **Sought** — she dressed for it / seeks it: she initiates, it's content she's chasing (ties to the desire ladder `09`).
2. **Choice-gated** — it triggers and she's **given a choice: refuse** (resist/escape — maybe a cost, a scene, a partial) **or accept** (be taken intentionally).
3. **Forced / unintentional** — it just happens, **no choice** — pure consequence of being exposed where she shouldn't be.

**Which mode = the risk curve:** low exposure / civilized place → only *sought* or *choice* (she can always refuse). High exposure / lawless place → can become *forced* (the choice is removed — she's taken). So **she manages risk by dressing for the place**: the more exposed + the more lawless, the more likely she loses the choice.

## The forced mode is ACT-SCOPED — prey early, predator late (`15` Finding D)
The *forced* mode (choice removed) is **not a fixed property of place × exposure — it also recedes as her power
rises.** This keeps the reactive world coherent with a power-rise fantasy: getting *taken* fits the broke,
exposed, desperate fall (Act 1); it is tonally wrong for the woman the city later answers to. So the forced
threshold is gated to the **cascade act / her power tier**, not place × exposure alone:
- **Early (the fall):** she's prey — high exposure × lawless place *can* become forced (no choice). The risk is real; it fuels the descent + the charge.
- **Late (the rise):** she's predator — the **same** outfit in the **same** place now reads as her *weaponizing*
  her body. Forced fades out; *sought* and *choice* dominate (she's courted, feared, used-by-her-own-design — she
  is the one taking now). The world treats power, not just skin.
**Prey → predator is the arc; the reactive world must track it.** (Engine: the forced auto-fire carries an
additional gate on player corruption/power tier — above a tier, forced down-shifts to choice/sought.)

---

## Per-place escalation CEILING (LO answer 2 — decided at generation, not hardcoded)
Every location carries a **reactivity ceiling**, set when designing the world (a per-game generation
decision, per the no-hardcode philosophy). The ceiling has two parts:
- **how far** reactions can go (stares-only → groping → non-con), and
- **whether they can become forced** (choice removed) at high exposure.
Lawless places (alley, docks at night, back room) + crowded/"rush" places — **and the bar itself, if the
game wants it** — get high ceilings (up to forced non-con). Civilized/public places get low ceilings
(stares/comments, always refusable). *Which place gets which ceiling is decided per game during
generation* — the principle is fixed; the values are authored. *(Implementation: the ceiling is a **design
discipline, not an engine field** — it's encoded in the `conditions` of the reactive canvases you author at
that location; see "Engine / skill reuse" below.)*

---

## Two ways the same content appears
- **Sought** (the want): she dresses down to get what comes with it — money, thrill, the descent (desire ladder `09`).
- **Risk** (the consequence): dressing exposed in the wrong place gets her taken when she didn't fully plan to.

---

## Where the CHARGE lives
This reactivity is a main delivery vehicle for the game's transgression (quality #7) — delivered at
**full intensity, non-con included**, at the NPC/place ceiling (`doctrine/08`), never soft-pedaled.

---

## Progression (since the world ignores traits)
Not from a trait — from **access to the clothing.** She starts owning only modest clothes; revealing /
slut outfits are *bought with money* or *unlocked as she commits to the path.* Her exposure dial widens
as she progresses; the world only ever reads the outfit she's actually wearing. Clothing-only preserved,
progression intact.

---

## Engine / skill reuse (implementation hook, for later)
- **Exposure value** = the existing clothing system (`worn_corruption` / clothing item values) — already
  gates public content; extend from *opt-in gating* to *passive reaction trigger*. Gate reactions on the
  **outfit value, NOT player corruption/exhibitionism.**
- **Passive events** = author as **Lane 2 (location-entry random)** + **Lane 3 (dispatcher)** content
  (`lanes.md`) — but gated on **clothing exposure × the location's ceiling × the present NPC's
  disposition**, not on the cascade meters. (Verified: clothing→Lane 2/3 is exactly the **PUBLIC content**
  the clothing doctrine *permits* gating on `worn_corruption` — `doctrine/11_clothing_design.md` §2 — so
  this is in-bounds, never an NPC arc spine.)
  - The *choice* mode = a normal `exit_block` with refuse/accept choices.
  - The *forced* mode = **NOT a zero-choice engine primitive** (verified: every canvas renders a fallback
    Continue; there is no `forced_goto`/`no_fallback`). Author it as an **auto-fire capstone-shape canvas**
    (`priority ≥ 9`, `is_repeatable = false`, gated above the place's forced-threshold) that plays the
    taken scene and exits via a **single Continue — no refuse/accept branch**. The player can't *avoid* it
    (it auto-fires when the gate is met), but isn't literally click-less. Achievable today, no engine work.
- **Per-location ceiling** = **NOT an engine attribute** (verified: a location has no author-defined custom
  field). The ceiling is **author-encoded as the per-canvas `conditions`** on the reactive canvases placed
  at that location — i.e. *which* reactive events you author there + their exposure/tier gates. The "ceiling"
  is a design discipline, not an engine knob.
- **Per-NPC disposition** = read from the casting hook/role (`06`) — encoded in each reactive canvas's
  `conditions` (`requires_npc` + the NPC's traits/flags), not a new engine field either.

---

## Self-check
- Reactions key off **CLOTHING exposure**, never player corruption/traits.
- Reactions are **lewd/transgressive** (grope→molest→rape), never social courtesy; tone shifts lewder only.
- **Place ceiling + NPC disposition** shape how far & who — in character (predatory escalates, respectful stays flustered, antagonist exploits).
- **Three modes present**: sought / choice (refuse-or-accept) / forced — with forced reserved for high exposure × lawless ceiling.
- **Forced is act-scoped** (`15` D): available in the fall (prey), recedes as power rises (predator) — gated on power tier, not place×exposure alone.
- **Per-place ceilings authored as per-canvas conditions** (not an engine attribute, not hardcoded);
  civilized places capped + always refusable; *forced* = an auto-fire capstone-shape canvas + single
  Continue (no zero-choice engine primitive).
- Exposure is **risk AND reward** (not always safe-reward).
- Feeds the **desire ladder** (she dresses down to chase wants).
- Charge delivered at the **ceiling** (non-con included), never soft-pedaled.

## Cross-references
- `10_reactive_world_research.md` (the evidence) · `08` Gap 2 · `06` casting (dispositions) · `09` desire
  ladder (sought reactions) · `05` quality #7 (charge) & #8 (reactive world) · existing clothing /
  `worn_corruption` + `lanes.md` (the engine vehicle).
