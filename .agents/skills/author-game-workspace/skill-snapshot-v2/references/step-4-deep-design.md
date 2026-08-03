# Step 4 — design: imagine the STORY of each subject (one subject at a time)

Step 4 designs the **STORY** — what each subject DOES, sounds like, wants, and becomes — by answering the
*story* half of `content-framework.md`, **one subject at a time**, in a fixed order:

**PLAYER (§2) → each NPC (§3, one each) → WORLD (§5) → REACTIVITY as experience (§4).**

The order is **supply → demand → stage**: the player's own thread is imagined before the NPC arcs that lean on
it, and the world before the reactivity that ties it together. This is the heart of incremental authoring —
**never imagine the whole game in one pass.** Step 5 (`step-5-blueprint.md`) then **structures** this story into
the exact gated, placed, ordered scene list; Step 6 (`step-6-feedback.md`) reviews it.

**Step 4 is now STORY-ONLY.** Every mechanism decision — lanes, gates, thresholds, placement, flag wiring,
scene order — moved down to the Blueprint step, so story and structure are never decided in the same breath.
The four words **lane, threshold, flag, placement** do not belong in a Step-4 brief: name the *moment* and what
it *feels* like; Blueprint turns it into the gated, placed scene.

## Inputs
The **cascade + economy + desire ladder + frontier** (Step 2 / framework §1), the **cast** (Step 3 — role ·
hook · lane · depth · arc-shape · sketch · place in the machine), the **8 qualities** (Step 0), and
**`content-framework.md`** — the question set this step answers as *story* (§2 for Pass 1, §3 for Pass 2, §5
for Pass 3, §4 for Pass 4).

## The ordering rule (enforced by the ledger)
The ledger's `deep_design` block tracks `{ player, npcs, world, reactivity }`. **Don't start `npcs` until
`player == "done"`; don't start `reactivity` until `npcs` and `world` are both done.** *Why:* you imagine the
player's own thread first so each NPC's story can build on a protagonist who is already going somewhere, and
reactivity is last because it describes how finished arcs change each other.

---

## Pass 1 — the PLAYER subject (§2 YOU) — FIRST, before any NPC
Answer **`content-framework.md` §2** as story. Output: a **`### The player thread (Step 4 · §2)`** block in
`design_book.md`.
- **2A bootstrap** — the off-zero solo acts + any behavior/story moment that nudges her open, and *why*
  (boredom, the rot starting, relief) — the experience, not the gate. **If her top-level drive is
  reactive** (revenge / escape / reclaiming — set by a thing that already happened), decide that cause
  here and make sure it's stated in the opening; an unmotivated reactive want reads as arbitrary. Pure
  appetite (the sandbox where wanting more is itself the engine) needs no wound — don't invent one.
  Name which it is so Blueprint and the opening beat carry the cause when there is one.
- **2B exhibition backbone** — the being-seen ladder per venue/stage, and what she WANTS out of being seen
  (tips, the thrill, proving her nerve, turning a head).
- **2C the economy as STORY** — her money story broke→rich: the lowest respectable earning at the start, the
  dirtiest best-paying thing by the end (better money always further down the lewd path), the buys she stays
  hungry for, the key items she covets. *(The income VALUES, item costs, and the feeder count are Blueprint's;
  here name the scenes and the want.)*
- **2D the ceiling** — the most extreme, most public thing she does that's about HER, the top of her own
  depravity, unthinkable on night one; plus any non-corruption ladder (job rank / fame / faction / skill) and
  what it's for.

- **The daily-routine moment (where the world walks in)** — which of her repeated routines (a shower, the
  dishes, a work shift, a quiet hour) is the world allowed to intrude on, and what does that feel like — the
  surprise, the line she lets cross because she was *just doing a chore*? Each routine is both a feeder she
  runs alone AND the host an NPC walks in on — the same moment, two outcomes (`content-framework.md` §2E
  roster; `references/lanes.md` Lane 3). Name them here as story, before any NPC arc claims them.

**Every feeder hangs on a WANT** (the desire ladder), never "raises corruption." **Ledger:** set
`deep_design.player = "done"` when the player story is complete.

---

## Pass 2 — each NPC (§3 THEM) — ONE NPC at a time
Takes one **cast row** and answers **`content-framework.md` §3** as story: the **story brief** below. **One NPC
per increment** — surface the brief (Mode A for *core*, Mode B for *peripheral*), get it okayed, then the
next. Never imagine the whole cast's arcs in one pass — this is the per-increment quality gate a one-shot can't
have. The **§3H "web between them"** is answered ONCE for the cast.

### The output per NPC = the STORY brief (the kept half of the old design brief)
The mechanism half of the old design brief — the stat ladder & spine, the lane-by-lane map, the capstone triggers,
the wiring contract — now lives in the Blueprint step. Step 4 writes the **story**:

1. **End-state fantasy** (one paragraph) — the complete arc's destination. **= EXPAND THE HOOK.** Author it
   FIRST; everything downstream grows from it.
2. **Voice spec** — how this NPC sounds (from the hook): diction, tells, what they call you, the private
   thought you glimpse, and how the voice shifts as they fall. RTS-flat for the everyday content; Tier-3 prose
   is earned only at the once-only peaks.
3. **The arc as a sequence of moments** — walk the road from cold start to the end-state as named turning
   points: the first warmth, the first crossing of a line, the first time, the surrender. The *moments*, in
   order — as experience, NOT as gated rungs (Blueprint sizes and gates them).
4. **Per-moment pretext shapes** — the in-fiction setup for each escalation: the believable reason the scene
   happens, the fiction that makes the move land.
5. **The big nights** — the once-only scripted peaks (first kiss, first time, surrender, breaking) as
   *moments* — what each one is and what it sets in motion. (Blueprint commits their triggers/thresholds.)
6. **What changes after** — once a turning point lands, how THIS SAME person behaves differently: greeting,
   voice, new things possible, old moments retired. *(Whether anyone ELSE reacts is Pass 4.)*
7. **Per-NPC anti-patterns** — what NOT to do for this NPC (e.g. a peer/dating NPC chasing her in private; a
   service NPC given a corruption arc).
8. **Acceptance** — the arc's "done" check, in story terms: the hook is visible (voice + want + real agency),
   legible pull (the player can feel the climb ahead), the payoff lands, the ceiling is honored.

The genuinely-new story bindings Pass 2 adds:
- **Hook → arc.** The hook seeds §1 + §3, and the NPC's **want** gives them **agency** — they pursue, resist,
  scheme, set conditions; NOT a yes-man whose only state is your meters (quality #5).
- **Depth is an INPUT from casting** — core → a full, central figure; peripheral → a lighter flavor. Don't
  re-litigate it, and don't gold-plate a peripheral with a central arc's depth.
- **Late-act target** — a target introduced late carries a **complete, self-contained burn** (its own
  cold-to-surrender road), because it can't borrow pacing from a protagonist who's already maxed.
- **Hold each NPC to the 8 qualities** — legible pull, payoff, the charge, a reactive world.

### Per-NPC self-check (story)
- **The hook is visible** (voice + want + real agency). · **The arc reads as a believable fall** — each moment
  follows from the last, no jump. · **Depth matches casting** (core rich / peripheral light). · **Anti-patterns
  respected.** · **The peak is earned** and the ceiling honored.

### Worked example (bar game, story-only)
**Sal — core.** Hook: *"your late partner's loyal best friend who's wanted you for years and hates himself for
it."* End-state: the night he stops resisting and lets himself have you, then keeps coming back. Voice: gruff,
clipped, guilty; softens as he falls. The arc: you talk and serve him (ordinary, warm) → he catches himself
watching → the first time he doesn't look away → the night he stops pretending → he's yours. A slow burn — the
charge is the guilt breaking. *(Blueprint will turn these moments into gated, placed scenes — not here.)*
**Marcus — peripheral.** dating, light: a flirt who could become a fling; one good night, no deep arc.

---

## Pass 3 — the WORLD subject (§5) — the stage
Answer **`content-framework.md` §5** as story. Output: a **`### The world (Step 4 · §5)`** block. **The stage
already EXISTS** — Step 2b designed the spatial graph + each place's dramatic job + access category. Don't
re-decide geography here; imagine each place's *story* (the feel of its public, its clock, its shared-private
moments) ON that map.
- **5A** confirm/deepen each place's dramatic JOB from the Step-2b map as *story* (the room-content floor was
  already gated there) + which track lives there.
- **5C** the reactive public — who notices her besides the named cast, the predator-vs-prude dispositions, and
  what goes WRONG when she pushes too far (caught, robbed, taken) — as *story consequence*, not condition gates.
- **5E** the felt cadence + the pressure clock — how urgent the days feel, the deadline hanging over it.
- **5H** the shared private spaces — for each place where someone does something private and the player's
  next door (the one bathroom, a bedroom), is it a walk-in / peep / occupied / caught spot? **Surface each
  candidate and CONFIRM it with the user per-place (`run-mode.md` Mode A) before it's in play** — grounded in
  the place + person + hour, never a blanket toggle (`content-framework.md` §5H).

*(The per-place ceilings, the schedules, the phone/sidebar wiring, and the locks are Blueprint's — here give
each place its dramatic JOB and the feel of its public and clock.)*

---

## Pass 4 — REACTIVITY as experience (§4) — LAST
Answer **`content-framework.md` §4** as story. Name, for each state-change, **what becomes different** — as a
felt moment: when she crosses a depravity band, what's suddenly possible; when an NPC falls, how the next
visit reads; when she takes someone, who else reacts; when she loses ground (§4F), whether the world bites.
*(The actual flag deps, the dependency map, and the D1/D2/D3 wiring are Blueprint's — here name the
consequence so Blueprint has something to wire.)* The §4F fail-state gets its one-line declaration here (does
failure exist at all); Blueprint decides whether and how it bites.

**Ledger:** set `deep_design.reactivity = "done"`, then **set `pipeline_phase = "blueprint"`.**

---

## Navigation (which subject / NPC next)
At each pass boundary, **propose the next move with options** (`run-mode.md` → "Navigation at junctions"). The
four-pass ORDER is fixed (supply→demand→stage), but *within* Pass 2 "which NPC next" and *at* boundaries "ready
to move from the player to the NPCs?" are real junctions — propose from the `deep_design` ledger block.

## Cross-references
`references/content-framework.md` (the question set this step answers) · `references/lanes.md` /
`trait-design.md` / `sex-loop.md` / `systems.md` (the mechanism library — used at **Blueprint**, not here) ·
Step 2 = `references/step-2-toplevel.md` (framework §1 + the inputs) · Step 5 = `references/step-5-blueprint.md`
(structures this story into the scene list) · Step 6 = `references/step-6-feedback.md` (reviews it). Set
`pipeline_phase = "blueprint"` when all four passes are `done`.
