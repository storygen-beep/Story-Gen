# Step 3 — casting (roles + hooks + rough sketch): every NPC earns its place

The step between the world (Step 2's engine + Step 2b's designed map) and the per-NPC arcs (Step 4) — the
stages already exist, so cast people onto them. The answer to "just randomly adding NPCs isn't good."
**Before anyone designs an NPC's arc, that NPC must have a ROLE in the story/cascade and a HOOK that makes
them desirable.** No role → cut or merge. Both *generative* (derive the roles the game
needs, cast people into them) and a *filter* (reject roleless/off-fantasy NPCs). Answers to the 8 qualities
(Step 0): coherence, desirable characters, the fantasy.

Output: a `## Casting` section in `design_book.md`. Set `pipeline_phase =
"deep_design"` when done.

---

## The principle
Like a novelist casting a story — characters aren't added at random; each serves the plot/theme. The **core
fantasy + the cascade GENERATE the role slots the game needs**; you cast the seed's named people into those
slots, give each a hook, and cut anyone who doesn't fit. Every NPC answers **"what am I FOR in this game?"**
before getting an arc. Casting may **amend the cast** — ADD an NPC to fill a missing required role; CUT or
MERGE a roleless one.

## The role taxonomy (derive which you need — don't hardcode the set)
**A. Structural — the cascade won't run without these:**
- **Pressure source** — creates the money/survival squeeze that drives Act 1 (the loan shark, the
  landlord). Without it nothing pushes the player to corrupt herself. *(Near-mandatory.)*
- **Corrupting on-ramp** — supplies the self-corruption opportunities (the boss who offers the risqué job).
  Fuels the self-corruption loop. *(Near-mandatory; can be the same character as a target or pressure source.)*

**B. Desire — the point of the game (the fantasy lives here):**
- **Core target(s)** — the 1–3 deep NPCs who ARE the fantasy's centerpiece; full two-meter arcs (the gold
  NPCs). *At least one is mandatory.*
- **Peripheral target(s)** — lighter NPCs adding breadth (a flirt, a fling); light model.
- **Gatekeeper** — a target locked behind a *secondary* stat, which gives that stat a real job + an
  aspirational prize. *(Include only if a secondary stat needs the job.)*

**C. Optional drama — add only if the fantasy calls for them:** ally/enabler, rival, witness/antagonist.

*One character can hold more than one role* (the boss = corrupting on-ramp AND a core target). Count falls
out of the fantasy + cascade, never a fixed number. Also carry a **late-act pressure role** (rival/cop/boss)
so the squeeze escalates and never dies (Step 2 §4).

## The HOOK (what makes a character desirable — quality #5)
Every cast NPC gets a one-line **hook** = **a specific charged dynamic + a WANT**. It must carry:
- **the dynamic** (who they are to the player — boss / step-sis / jaded regular / landlord),
- **the charge** (what's forbidden/hot about them),
- **their want** (what *they* are after — so they have agency, can resist/scheme, aren't a yes-man),
- **their fantasy lane** (so the cast spans VARIETY — nurturing vs forbidden vs dominant vs reluctant),
- **the desire FLAVOR** (longing / transactional heat / **conquest** — wanting to take/break/own them; a
  conquest-target is legitimate as a core target as long as the pursuit is hot and they have agency).

A hook is "the strict bar-owner's wife you want to break, who's bored and craves danger" — NOT "Family
arc-shape #3." If you can't write the hook in one hungry line, the character isn't ready. The cast as a
whole must deliver the **desire span declared at Step 0**. The hook is also what the NPC's **first encounter**
must land on the page — casting's want becomes the meeting's first voiced line (`references/npc-intro.md`).

## The rough sketch (where each NPC roughly goes — and where cross-NPC lives)
Alongside role + hook, give each NPC a **rough sketch** — a loose few lines of where the character *roughly*
heads (not the full arc; that's Step 4). The sketch is the home for the game's **cross-NPC connections**,
kept deliberately light: *"she's got a friend who could become her own arc," "if she ends up pregnant it
changes how Sal treats you," "she and Dee already know each other."* These are **ideas, not a format** —
organic threads (RTS: a brother's pregnancy rippling to the others; a sister's friend opening into an arc).
**Optional, not every NPC** (islands are fine).

Why it earns its place:
- You sketch the **whole cast in one sitting** → you *see the connections* while everyone's in front of you
  (the only "look at the forest" moment the one-at-a-time Step 4 can't give). No separate weave step.
- **Step 4 is never authored in a vacuum** — the sketch + threads are already there when you go deep.
- Clean **three-level zoom**: hook (one line) → rough sketch (casting) → full arc brief (Step 4); the sketch
  seeds the brief's §1 end-state.
- When a thread grows up: a friend-who-becomes-playable is a **new NPC** back through casting; a ripple is a
  **`cross_npc` beat** at authoring. No system, no diagram.

## What casting assigns per NPC (the bridge to Step 4)
For each cast member, record: **role(s) · hook · fantasy lane · depth (core vs peripheral) · arc-shape**
(which implies the personal trait that will drive them — the spine menu, `references/trait-design.md`) **·
place in the machine** (core NPCs — below) **· rough sketch.** Step 4 details each one's locks/scenes;
casting just sets *who they are and what they're for.*

**Place in the machine (core NPCs — `step-2-toplevel.md` §7).** Step 2 designed the
**core loop** (conquest → money/access → next conquest). Give each *core* NPC one phrase for its **node** in
it — what it feeds, what feeds it: *"the boss = income node — corrupting him raises the floor wage that funds
reaching Sal"* (form 2), or *"Rosa's deep rungs open only once the bar is seized"* (form 1). The rough-sketch
threads are the seed; a load-bearing thread (it gates a rung or routes income) becomes a real place here and
a wire in Step 4 §8. Peripherals/islands get none — the machine is the core's spine, not a quota. Disciplines
(`step-2-toplevel.md` §7) bound it: a wire constrains an arc's *depth ordering*, never its *availability* (D1).

## The output artifact (a `## Casting` section in `design_book.md`)
| NPC | role(s) | hook (dynamic + charge + want) | lane | depth | arc-shape | place in machine (core) | rough sketch (+ cross-NPC threads) |
|---|---|---|---|---|---|---|---|
One row per NPC; the rough sketch is a loose few lines (write it under the table if it needs room).
**Place in machine** = one phrase for each core NPC's node in the core loop (`step-2-toplevel.md` §7); blank for peripherals.

## Casting self-check (run before locking the cast)
- **Structural coverage:** a pressure source? a corrupting on-ramp? at least ONE core target? *(dead cascade
  without all three.)* And a **late-act pressure** role so the squeeze escalates.
- **Every NPC has a role AND a hook** — no roleless character (cut/merge), no shapeless one (no hook → not ready).
- **Coherence:** every NPC serves the core fantasy — no off-theme character.
- **Cover holds (infiltration premises):** if a target sits behind a disguise/cover, would he **see through** it —
  recognize what she really is? An insider who'd clock her breaks the honeypot; recast him as a deniable outsider
  or change the cover (`references/content-framework.md` §1A — the premise pressure-test).
- **Variety:** the cast spans different fantasy lanes/dynamics — not five of the same; each core target a *distinct* desire.
- **Desire span delivered:** the cast covers the genders + flavors declared at Step 0; any conquest-target
  reads as wanted-as-conquest, not a cold instrument.
- **No redundancy:** two NPCs with the same role + hook → merge or differentiate.
- **Machine placed** (`step-2-toplevel.md` §7): the core loop is named and **every core NPC has a place in it** — the cast isn't
  a set of islands. (The DAG is built at the blueprint + checked at the feedback review, `step-6-feedback.md`;
  here it's just "is each core NPC wired in at all?")
- **The 3-question test:** say the fantasy in one sentence? name what the player wants next? name *each*
  NPC's hook? If any NPC fails the third, fix or cut it.
- **Not every NPC is a climb.** Most hooks imply a rising arc, but an owner/spouse/regular you *already have* is
  the **static** shape (no climb) and an infiltration mark is the **honeypot** shape (the climb is on HIM, not the
  player) — both are rows in `trait-design.md`'s arc-shape table. Don't force a static/honeypot NPC onto a climb row.

## Cross-references
`references/step-2-toplevel.md` §7 (the machine —
the "place in the machine" each core NPC gets) · `references/trait-design.md` (the arc-shape → spine menu each
hook implies) · `references/lanes.md` (per-arc-shape budgets) · Step 4 = `references/step-4-deep-design.md`
(Pass 2 designs the per-NPC story on each cast row) · Step 5 = `references/step-5-blueprint.md` (structures it
into the scene list, incl. the §8 wiring contract).
