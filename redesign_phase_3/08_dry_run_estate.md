# Dry-run — "The Estate" through the pipeline + brutal critique

A paper test of the designed front-end (Step 0→4) on ONE fresh game, then an honest critique against
the good-game qualities (`05`). Premise chosen deliberately NOT the bar (the bar is hand-fitted in the
docs — a fresh premise is a real test). Goal: does the design compose into a *good* game, or another
correct-but-soulless LC? What gaps does it expose?

---

## The run

### Step 0 — Good-game (fantasy + desire curve)
- **Core fantasy (one hungry sentence):** *"Inherit your estranged father's debt-strangled estate and
  turn the women who came with it — his trophy widow, her bratty daughter, the housekeeper who keeps
  every secret — into your own, becoming the master of the house that was never meant to be yours."*
  → A fantasy, not a setting (it's *own the household + take his place*). ✓
- **Desire curve:** the visible prize = **Vivian**, the elegant widow who looks down on you — you can
  see her, can't touch her, climb toward her. The clock = **Harlan's debt deadline** (lose the estate
  if unpaid). Payoffs drip up from the easy wins (Cassie's provocations, Marta's complicity) to the
  widow. Endings: save + claim the house (win) / lose it (lose) / branches per who you took.

### Step 1 — Setup (bare seed)
- Player: broke, estranged 20-something son who just inherited.
- Cast (names+roles only): **Vivian** (widow), **Cassie** (her daughter), **Marta** (housekeeper), **Harlan** (creditor).
- World: the estate (manor rooms + grounds) + the nearby town/bank.
- Systems: clothing (the women's wardrobe matters), debt/rent (the estate's mortgage = the pressure), phone (optional).

### Step 2 — Engine/cascade (the part we've designed)
- **Cascade:** Act 1 — broke grieving-intruder in a house that resents you; corrupt yourself (the
  father's cellar/secrets, the town's seedy money) + build the women (help, share grief) in parallel.
  Act 2 — your corruption opens lewd moves, each also gated by that woman's own lock. Act 3 — deep arcs
  + save/claim the estate.
- **Stats (each a job):** corruption = lewd door; money = save the estate (the pressure); energy =
  pacing; **standing/charisma** = whether Vivian & Harlan's world take you seriously (you start a
  nobody). Test: each names content it gates → no dead stat. ✓

### Step 3 — Casting (roles + hooks)
- **Harlan** — *pressure source*. Hook: "the smiling creditor who'll seize the estate — or accept other arrangements." Want: the estate / leverage.
- **Marta** — *corrupting on-ramp* + peripheral target. Hook: "the housekeeper who kept your father's secrets and will keep yours — pragmatic, knows where the bodies are." Enables your self-corruption (cellar, the father's vices). Want: keep her place.
- **Vivian** — *core target* (+ standing-gated). Hook: "your father's trophy widow — elegant, grieving, secretly broke and trapped, who looks down on you but has no one else left." Want: security; she resents needing you. Slow-burn.
- **Cassie** — *peripheral target*. Hook: "the bratty stepsister your own age who wants the intruder gone — but she's bored, and provokable." Want: you out; secretly craves friction.
- Variety: forbidden-elegant / bratty-antagonist / complicit-pragmatic / antagonist-pressure. ✓ Coherent (all serve "own the house"). ✓

### Step 4 — NPC arcs
- **Vivian (core, slow-burn):** rich two-meter (her corruption + arousal). End-state expands the hook
  (contempt → need → devotion as co-mistress). Lewd rungs **double-locked** (MC corruption tier + her
  own corruption, built by intimacy/shared grief); non-lewd talk ungated (builds her lock Act 1). Early
  engagement also **standing-gated** (she won't entertain a broke loser). First-night capstone
  (odometer+flags); repeatable loop after.
- **Cassie (peripheral):** light — `relation` (antagonism→flirt) + player-corruption floor; provocation
  escalates; one capstone, no loop.
- **Marta (peripheral + on-ramp):** light — trust/complicity; enables self-corruption; service-target.
- **Harlan (antagonist):** flags + money/leverage + the deadline; confrontation capstone (pay / lose / arrangement).

---

## Brutal critique

### What it PASSES (and why it's already better than LC)
- **Fantasy in one sentence** ✓ (LC fails this — "a bar with NPCs").
- **Desirable characters** ✓✓ — each has a hook + a *want* + agency (Vivian resents needing you; Cassie
  wants you gone; Marta trades secrets; Harlan circles). This is the single biggest upgrade over LC's
  interchangeable arc-shapes — these create *desire*.
- **Coherence** ✓ — everything serves "own the house"; the casting filter would cut a roleless NPC.
- **Paced gating structure** ✓ — the cascade + double-lock give a tension structure.
- **The anti-LC test** ✓ — say the fantasy / name what you want next (Vivian, the deadline) / name each hook.

**Verdict: the front-end is genuinely stronger than LC.** The hooks + fantasy + double-lock are real.

### What it EXPOSES (the gaps the dry-run found — the valuable part)

**GAP 1 — the cascade risks BEING the grind unless DESIRE drives it. (deepest)**
The cascade is a *gating* structure (raise corruption → unlock tier). But "raise corruption to unlock"
is one keystroke away from the #1 enemy: **grind a bar to unlock content.** The thing that makes it
*good* instead is that every corruption gain is *motivated by a want* — you flash for cash because you
want to impress Vivian; you snoop the cellar because you're chasing her. **Nothing in our design yet
forces the cascade to be experienced as pursuit-of-desire rather than meter-filling.** This is THE
make-or-break, and it's currently implicit. → Needs an explicit principle: *every progression gain is
hung on a desire/goal the player feels*, never "do activities to fill the bar."

**GAP 2 — the reactive world (quality #8) has NO designed mechanism.**
We assert "the world acknowledges your growth" (intruder → master; the house improves; the women's
baseline demeanor shifts). But no step *produces* this. Without it, you get LC's static wallpaper. →
The remaining Step-2 design needs an **acknowledgement layer**: standing/state visibly changes baseline
prose, the world (the house, the town) reflects your rise, NPCs' default demeanor moves with the odometer.

**GAP 3 — legibility (the goal-thread) has no owner.**
RTS's #1 complaint. We have locked-visible rungs (per-NPC), but no GAME-level "you always know the
current objective + next step" spine. → Step 2 needs a **progression-legibility / objective thread**
(the roadmap as the player-facing goal line: "pay the debt by X; win over Vivian"), so the player is
never lost.

**GAP 4 — the desire CURVE / pacing is asserted, not designed.**
"Earned escalation, tension→release" — but nothing shapes the *curve*: how fast corruption climbs, when
payoffs land, the rhythm. Pacing is make-or-break (LC's flat grind). The numbers that make it feel good
vs grindy are undesigned. → Needs a **pacing design** (the rate/curve), probably in Step 2 or as a
cross-cutting principle.

**GAP 5 — the economy could be a grind-wall.**
The cascade leans on money pressure; if there's one repetitive income job, that's classic grind. →
The economy design must bake in **multiple income paths** (anti-grind: blocked on X → progress on Y).

---

## Conclusion
The designed front-end **holds and is clearly better than LC** — the fantasy + hooks + double-lock
produce desire and coherence LC never had. But the dry-run found that **"good" isn't fully secured yet**:
the cascade must be made *desire-driven not meter-driven* (Gap 1, the deepest), and three qualities we
*named* in `05` have **no step that produces them** — reactivity (#8), legibility (#2), pacing (#4-#6).
These map almost entirely to **the still-undesigned rest of Step 2** (world / economy / story-spine /
pacing) plus **one new cross-cutting principle** (desire-driven progression).

**So the dry-run did its job:** it validated the foundation AND told us exactly what the rest of Step 2
must contain — not "story/world/economy/endings" generically, but specifically: a **desire-driven-progression
principle**, an **acknowledgement/reactivity layer**, a **legible objective thread**, a **pacing curve**,
and an **anti-grind multi-path economy.** Design those and the front-end should produce a good game.
