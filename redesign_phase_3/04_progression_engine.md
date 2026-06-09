# Step 2 — The progression engine (the cascade)

**Status: CORE LOCKED** (2026-06-08); two sub-choices pending (§7). This is the heart of the Top-level
design step — the rulebook for how the player grows and how that growth unlocks the world and the NPCs.
Grounded in `02_GAME_SURVEY_top_level.md` + `03_secondary_traits_gating.md` (the studied gating
patterns) + the RTS model. Sandbox-only (per LO); may go as system-rich as Lustbound.

---

## §1 — The one idea

**You must corrupt YOURSELF before you can corrupt anyone else.** The player's own corruption is the
master key; all lewd content with NPCs stays locked until the MC has fallen far enough. This single rule
turns an open sandbox into a story with a beginning, middle, and end — *without a linear script.*

---

## §2 — The cascade (3 acts)

**Act 1 — Fall (corrupt yourself) + Build (befriend NPCs) — in parallel.**
- Start clean (MC corruption 0). No lewd moves available on anyone.
- Two loops run side by side:
  - **Self-corruption loop** — solo + risky/public activities (porn, drink, flash, the sketchy job) raise the MC's OWN corruption. The money/rent pressure pushes the player toward the corrupting options (clean jobs don't pay enough). *This is the feeder economy; it is the story's opening — you erode your own limits.*
  - **Per-NPC loop** — you can talk to / befriend / build any NPC from day 1 (NOT gated by your corruption — see §4). This raises each NPC's OWN personal traits.

**Act 2 — Reach (the lewd door opens, per the DOUBLE LOCK).**
- As MC corruption crosses tiers, lewd options *appear* on NPCs: low tier → flirt/tease, mid → grope/contact, high → sex.
- Every lewd NPC scene has a **double lock** (§3). MC corruption opens the door for the whole cast; each NPC's own personal trait is the individual lock you've been picking in Act 1.
- The two loops CONVERGE: NPCs you invested in are ready the moment your corruption unlocks the door.

**Act 3 — Deepen (per-NPC arcs + repeatable).**
- After an NPC's first-time capstone, her repeatable sex loop opens (paced by **arousal**, the throttle that resets each time — odometer/throttle doctrine intact).
- Deep arcs play out.

---

## §3 — The DOUBLE LOCK (the core gate)

Every **lewd** NPC scene requires BOTH:
1. **MC corruption ≥ the tier for that KIND of act** — the *door*. "Am I depraved enough to even attempt this?" Opens for the whole cast at once.
2. **The NPC's own personal trait(s) ≥ her threshold for that rung** — the *individual lock*. "Is SHE far enough along?" Built by interacting with HER.

This is RTS's two-axis gate (`requirementsMC` player floor + the NPC's own corruption/arousal), made the
EXPLICIT spine: the player side is a "fall first" cascade, the NPC side is her personal arc.

---

## §4 — Two build-loops, and what each gates (the crucial split)

| Loop | What you do | What it raises | What it gates |
|---|---|---|---|
| **Self-corruption** | solo + world/public activities (the feeders) | MC **corruption** | the lewd DOOR (the cascade tiers) — applies to the whole cast |
| **Per-NPC** | talk to / interact with a specific NPC | that NPC's OWN personal trait(s) | that NPC's individual LOCK (her arc rungs + her repeatable loop) |

**Non-lewd interaction is NOT gated by MC corruption.** Talking, befriending, building an NPC's
trust/relationship is available from day 1 — that's *how you raise her personal traits*. Only the LEWD
escalation is double-locked. (So a clean MC can still build the whole cast's readiness; the lewd door
opens later.)

**Which personal trait drives a given NPC is PER-NPC** (her personality / arc-shape — the spine menu
from `02_GAME_SURVEY`): slow-burn family → corruption+arousal; dating → love+lust; service → trust; etc.
Chosen per character, documented in her brief (Step 3).

---

## §5 — The stat set (each leg owns ONE job — no dead stats)

| Stat | Its job (domain it gates) | Gating pattern (§ of doc 03) | Raised by |
|---|---|---|---|
| **Corruption** *(MC, the SPINE)* | the **lewd door** — the whole cascade (§2-3) | hard content tier | solo + risky/public activities |
| **Money** | survival + purchases (clothes/gifts/rent) + *pressure that drives you to corrupt* | economy/pressure | jobs/work |
| **Energy** | **paces the day** — spend to act, restore by sleep | action cost (our `costs`) | sleep/rest |
| **Charisma / social** *(Tier-3 CUSTOM — not a built-in)* | the **social door** — which NPCs will engage you | banded (soft default; hard for 1–2 "exclusive" NPCs) | social activities |
| **Fitness** *(Tier-2 optional engine trait)* | **attractiveness / body** — better NPC reactions, earnings, maybe one looks-gated arc | soft modifier / banded | gym, grooming |
| *(per NPC)* **personal trait(s)** e.g. trust/corruption/arousal or love/lust | that NPC's individual lock + her repeatable loop | tier + throttle (arousal) | interacting with HER |

**Division of labor:** corruption opens the LEWD door, charisma opens the SOCIAL door, money opens the
SURVIVAL/PURCHASE door, fitness improves OUTCOMES. Several legs, not one corruption rail. (Optional: a
career/skill stat for a stronger money/job ladder — leveled-tier — if the economy wants depth.)

**No dead stats:** every stat above gates a real domain or feeds a visible outcome. Anything that only
climbs gets cut (the dead-stat trap, doc 03 §3).

> **Engine ground-truth (verified 2026-06-10 — the skill may only cite REAL knobs).** Which of these
> "legs" is a built-in matters, because the skill's iron rule bans inventing engine fields:
> - **Built-in player traits (real, special-handled):** `corruption`, `arousal`, `energy`, `hygiene`,
>   `money` (always-on Tier 1) + `exhibitionism`, `fitness`, `intelligence` (optional Tier 2). Declare
>   in `[player.core_traits]`; gate with standard predicates (`corruption_level` for the banded door).
> - **`beauty` is NOT a raisable stat** — it is **derived read-only from worn clothing** (`getWornBeauty`;
>   `op=add/set` forbidden). It belongs to the **clothing system** (the `worn_beauty` predicate), not the
>   stat legs. Don't model "raise beauty at the gym"; raise `fitness` (real) and let clothing drive beauty.
> - **`charisma` / `social` are NOT built-in** — zero engine concept. A "social door" is legitimate ONLY
>   as a **Tier-3 CUSTOM trait** the game declares per-game (doctrine/09 §6 free-form), gated with the
>   ordinary `trait` predicate. Same for a career/skill stat. Fine to author — just never present them as
>   engine-native. This is exactly what §7's "derive, don't hardcode" already implies.

---

## §6 — Why this answers the worries

- **No random writing** — every stat has a written rule (job · pattern · raise loop · not-dead check). Claude gates to the rulebook.
- **Not one-trait-does-everything** — corruption=lewd, charisma=access, money=survival, fitness=looks; distributed (doc 03 §2).
- **Story in a sandbox** — the "fall → reach → deepen" cascade is a real 3-act arc with no linear script.
- **RTS-grounded** — it's RTS's corruption floor + two-axis gate, made the explicit spine.
- **Engine-supported** — corruption tiers, per-NPC traits, energy `costs`, money, schedules all already exist; arousal-throttle + odometer doctrine intact.

---

## §7 — DON'T hardcode the stat count or gate type — DERIVE them (LO directive)

The number of stats and the gate types are NOT fixed values to memorize — they are *derived per game*
from principles. The skill teaches the logic; the author/Claude applies it. (LO: "we don't want to
hardcode things, instead focus on the design philosophy — why, how much, the logic behind it.")

**How many legs? — derived from the game's CONTENT, not a number.**
- A stat exists ONLY to gate a content domain the game actually has. The test for any proposed stat:
  **"name the specific content this gates."** If you can't, it's a dead stat — cut it.
- Always-present: **corruption** (the spine) + **money** (economy) + **energy** (pacing). These earn
  their place in every sandbox.
- Add another leg ONLY when the game has a distinct domain that needs its own gate (built-in vs custom
  matters — see the ground-truth box in §5):
  - lots of public/exhibition content → **`exhibitionism`** (built-in Tier 2);
  - an attractiveness/body arc → **`fitness`** (built-in Tier 2; *beauty* is clothing-derived, not a leg);
  - an academic/skill domain → **`intelligence`** (built-in Tier 2);
  - a real career/job ladder → a **career/skill stat** (Tier-3 *custom* — author it per-game);
  - meaningful differences in who'll socially engage you → **`charisma`/social** (Tier-3 *custom*).
- *How much* = as many legs as there are REAL domains, no more. A game with no career content must NOT
  add intelligence (it'd be dead). The count falls out of the content; it is never a target.

**Hard vs soft gate? — match the FICTION, not a global rule.** (Generalizes to ALL gates, not just charisma.)
- Ask: **"what does the world honestly look like when the player is LOW on this stat?"**
  - If the honest answer is *"this person/content isn't in the picture at all"* → **hard gate** (it's absent/locked until the threshold). Use for guarded/exclusive characters or genuinely locked content.
  - If the honest answer is *"they're around, just colder / harder / worse outcomes"* → **soft gate** (always reachable, the low stat degrades it). Use for most relationships.
- Decide per case from what's *true in the world*, never by a blanket "charisma is always soft" rule.

**The meta-rule:** every stat ships with its four facts — **job · gating pattern (doc 03 §1) · raise
loop · not-dead check** — derived from the game, so the choice is principled, never hardcoded or guessed.

---

## §8 — Worked picture (the bar game)
Day 1: broke, bar in debt. You can chat with Sal/Dee (build their personal traits) but can't make a
lewd move (corruption 0 — door shut). You watch porn, take the topless late shift for cash, flash a
regular on a dare → **your corruption climbs**. At tier 1, "flirt with Sal" appears IF Sal's own arc is
ready (double lock). You've been flirting/serving him in Act 1, so he is. Build him further → at tier 2
+ his lock open → the back-room scene. Meanwhile **charisma** decides whether the standoffish new regular
talks to you at all; **money** buys the outfit that raises **beauty** that warms the whole table.

---

## Cross-references
- `03_secondary_traits_gating.md` — the 6 gating patterns + domain-separation + dead-stat trap.
- `02_GAME_SURVEY_top_level.md` — the spine menu (which personal trait drives each NPC).
- Existing skill doctrine to reconcile when implementing: `trait-design.md` (throttle/odometer, per-NPC
  spine), `rts-design-philosophy.md` (two-axis gate, feeder economy), `content-design.md` (the feeder
  activities that raise MC corruption + each stat).


