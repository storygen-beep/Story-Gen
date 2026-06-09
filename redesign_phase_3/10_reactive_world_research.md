# Reactive world — how the reference games do it (research for Gap 2)

Before designing Gap 2 (`08` — "the world acknowledges your growth," currently unowned), reference how
the sandbox games actually make the world react to the player. Source-read (RTS) + survey recall (others).
LO's hypothesis to test: *reactivity is largely LEWD and STATE-driven — e.g. fewer clothes → public/NPC
groping, varying by the NPC's arc/role.* Verdict: **confirmed, and it's the central mechanism.**

---

## The four mechanisms found (grounded)

**M1 — State-gated AMBIENT EVENT POOL (RTS's main one).**
Ordinary actions roll for lewd events whose **availability + intensity scale with player
corruption / exhibitionism / OUTFIT-corruption.** The more corrupt/underdressed you are, the more the
world "happens to" you.
- *Evidence (RTS source):* "Bus Grope — Ride the bus" (chance 33, corr 0) — do a neutral action, a grope
  fires by chance; clothing gates like "outfit with at least 30 corruption" (Sunbathe Lotion / Pool
  Flash need a 30+ corruption outfit); flash = 150 mentions, grope = 16. This is **passive** — the event
  comes to you because of your state, not because you picked "get groped."
- This directly IS LO's hypothesis: fewer/▾corrupt clothes → public groping/flashing fires.

**M2 — Clothing / nudity → reactions & consequences.**
Being underdressed/nude changes what happens — both *opt-in* public scenes (gated on outfit corruption)
AND *passive consequences*.
- *Evidence:* RTS outfit-corruption gates (above). **Lustbound `momHouse`**: Heat / CaughtCount /
  NudeStrike rise when you're nude in the house → confrontation/consequences, **mediated by the
  household's disposition** (Trust / Jealousy / Openness). The clearest "nudity → reaction" system, and
  it's *disposition-mediated* — exactly LO's "based on the NPC's arc/role."

**M3 — Per-NPC demeanor shifts (by relationship + your stats).**
NPCs treat you differently as their meters / your stats rise — reactive greetings, options, tone.
- *Evidence:* Become Someone — "girls react to you differently depending on your stats"; Back to Freedom —
  per-NPC love/lust changes their behavior. The *same hub*, a *different reception* by tier.

**M4 — Standing / reputation reflected.**
Your rise is acknowledged at the world level — your reputation/role changes who defers to you / engages you.
- *Evidence:* Gakko fame ladder ("Nobody → Recognition → Sensation"); RTS standing feeding reactions.

---

## The synthesis (what "the world reacts" actually means)
Two axes of reactivity, both **driven by player state and mediated by NPC disposition**:

1. **PASSIVE reactivity (the world acts ON you):** ambient lewd events + consequences fire on ordinary
   actions, scaled by your corruption/exhibitionism/**outfit** — and *who* reacts (and how) depends on
   the NPC/place's disposition. (M1 + M2.) ← *this is the part LO is pointing at, and it's the biggest.*
2. **PROSE/DEMEANOR reactivity (the world treats you differently):** baseline greetings, options, and
   tone shift as your state + the NPC's relationship rise; reputation is acknowledged. (M3 + M4.)

**The key refinement (LO's, and the games support it):** reaction is **PER-NPC-DISPOSITION, not
uniform.** Underdressed in front of a bold/corrupt NPC → he gropes; a respectful one → looks away,
flustered; an antagonist → uses it against you (Lustbound's disposition-mediated heat). This ties the
reactive world directly to the **casting HOOKS** (`06`) — each NPC reacts *in character*.

---

## Implications for the Gap-2 design (next)
- Reactivity should be **state-driven** (corruption / exhibitionism / **outfit-corruption / nudity**) —
  not a separate system, but the existing meters + clothing *read by the world*.
- It has **two surfaces**: passive ambient events/consequences (M1/M2) + reactive demeanor/prose (M3/M4).
- It must be **per-NPC-disposition**, keyed off each NPC's hook/role (`06`) and arc state — a corrupt
  NPC, a respectful NPC, and an antagonist react to the same outfit differently.
- It should be **legible** (the player learns "dressing like this gets this reaction") and feed the
  desire ladder (you dress down *because you want* the reaction that advances a want — `09` R1/R7).
- Engine note: clothing-corruption-gates-public-content is already in the skill (the clothing system /
  `worn_corruption`); Gap-2 design extends it from *opt-in gating* to *passive per-disposition reaction*.

## Cross-references
- `08` Gap 2 (this) · `06` casting hooks (the dispositions that mediate reaction) · `09` desire ladder
  (reactions you seek) · `05` quality #8 (reactive coherent world) · existing skill clothing /
  `worn_corruption` system (the engine hook).
