# Step 2 — top-level design (the engine, economy, desire ladder, frontier)

The rulebook for how the player grows and how that growth unlocks the world. Designed in **plain words,
written into `design_book.md`** — no TOML yet. The crucial forks here (cascade shape · economy shape ·
ending/frontier shape) are **Mode A** (decide *with* the user); the rest is informed-and-written. This step
is cheap on paper and identity-setting, so ask freely.

Everything below answers to the 8 qualities (Step 0) and is grounded in the RTS model.

---

## 1. The cascade (the spine) — `redesign_phase_3/04`
**One idea: you must corrupt YOURSELF before you can corrupt anyone else.** The player's own corruption is
the master key; all lewd content with NPCs stays locked until the MC has fallen far enough. This turns an
open sandbox into a story with a beginning/middle/end *without a linear script.*

**Three acts:** **Fall + Build** (Act 1 — corrupt yourself via solo/public feeders *and*, in parallel,
befriend NPCs — befriending is NOT corruption-gated) → **Reach** (Act 2 — as MC corruption crosses tiers,
lewd options *appear* on NPCs per the double lock) → **Deepen** (Act 3 — first-time capstones, then
repeatable loops).

### The DOUBLE LOCK (the core gate)
Every **lewd** NPC scene requires BOTH:
1. **MC corruption ≥ the tier for that KIND of act** — the *door* ("am I depraved enough to attempt this?").
   Opens for the whole cast at once; built by the player's self-corruption feeders.
2. **The NPC's own personal trait ≥ her threshold for that rung** — the *individual lock* ("is SHE far
   enough?"). Built by interacting with HER.

**Non-lewd interaction (talk, befriend, build trust) is NOT corruption-gated** — it's how you raise the
NPC's lock in Act 1, in parallel with corrupting yourself. The two converge: when your corruption opens the
door, the NPCs you invested in are already unlocked. This is RTS's two-axis gate made the explicit spine
(`requirementsMC` player floor + the NPC's own corruption/arousal). It is the same machinery as
`references/trait-design.md` (the NPC's own axis gates rungs; player corruption is the secondary floor on
the most explicit beats) — Step 4 wires each NPC into it.

### The stat set (each leg owns ONE job — no dead stats)
A stat exists ONLY to gate a content domain the game actually has. **Test for any proposed stat: "name the
specific content this gates."** No answer → dead stat, cut it. Derive the count from the game's content,
never a target number.
- **Always-present:** **corruption** (the lewd door — the cascade) · **money** (survival + purchases +
  the pressure that drives corrupting) · **energy** (paces the day; spend via `costs`, restore by sleep).
- **Add a leg only for a real domain** — and respect what's a built-in vs a custom trait:
  - public/exhibition content → **`exhibitionism`** (built-in); a body/looks arc → **`fitness`** (built-in);
    an academic domain → **`intelligence`** (built-in).
  - a "social door" (who'll engage you) → **`charisma`/social** — **NOT a built-in; author it as a Tier-3
    custom trait** (declare in `[player.core_traits]`, gate with the ordinary `trait` predicate).
  - a career ladder → a **career/skill** Tier-3 custom trait.
  - **`beauty` is NOT a leg** — it is *derived read-only from worn clothing* (`worn_beauty`), owned by the
    clothing system. Raise `fitness` (real); let clothing drive beauty.
- *(Per NPC)* the **personal trait(s)** that form each NPC's lock — chosen per character in Step 4.

**Hard vs soft gate — match the FICTION.** Ask "what does the world honestly look like when the player is
LOW on this stat?" *"This person/content isn't in the picture"* → **hard gate** (absent/locked). *"They're
around, just colder/worse"* → **soft gate** (always reachable, low stat degrades it). Decide per case.

---

## 2. The desire ladder — `redesign_phase_3/09` (the cascade, *felt* as wants)
Don't model the game as a corruption meter with content bolted at thresholds. Model it as **a chain of
escalating, named WANTS** — each concrete and *wanted* — where pursuing a want raises the meters that open
the next want. **The meter is backstage; desire is onstage.**
- **Every gain serves a named want.** Any activity that raises a meter must be, in the fiction, the player
  *pursuing a want she currently holds.* Test each activity: "what does the player WANT that this serves?"
  No answer → grind; cut or reframe. (The waitress flashes for tips *to afford the dress that turns the
  owner's head* — not "to raise corruption.")
- **The current want is always NAMED and visible** (this is also the legibility surface).
- **Want-completion = tier-crossing = a payoff**, and it reveals the next want.
- **Per-NPC arcs are wants too** (flavor incl. **conquest** — wanting to break/own a person; fine as a core
  target as long as the pursuit is hot and they have agency).
- **The ladder is OPEN-TOPPED** (the frontier, §6) — the top rung is the current edge of authored content,
  not a wall.

Author the desire ladder as the design book's player-facing spine (surfaced later via quest cards). Each
rung: a concrete want + what clearing it unlocks (the next want).

---

## 3. The reactive world — `redesign_phase_3/11` (clothing-driven lewd reactivity)
**The world reacts to what she's WEARING, not to a hidden corruption number.** The outfit has an exposure
level she controls; the world reads it and takes lewd liberties scaled to it. (Deliberate divergence from
RTS — outfit-only, for legibility + player control.)
- **NOT social courtesy.** Any tone shift with the outfit goes *lewder / bolder / more predatory*, never
  warmer. Exposure → transgression ladder: covered → ignored; low-cut → stares/gropes-in-passing;
  barely-dressed → open groping/cornered; nude → public use/taken — *where place + people allow.*
- **Who & how far = place ceiling × NPC disposition, in character.** Predatory NPC/lawless place escalates
  to non-con; a respectful NPC stays flustered; the antagonist banks it as leverage; a civilized public
  place caps at stares/comments. Same outfit, different room → different scene.
- **Three modes:** *sought* (she dressed for it) · *choice* (refuse-or-accept) · **forced** (no
  refuse/accept). **Forced is ACT-SCOPED** — prey early (the fall), recedes as power rises (predator); gate
  it on the power tier, not place×exposure alone.
- **Engine truth (only real knobs):** gate reactions on **`worn_corruption`** (the clothing exposure
  value), NOT on player corruption/exhibitionism. Author the events as **Lane 2 / Lane 3** canvases
  (`references/lanes.md`) — this is exactly the **PUBLIC content** clothing is *allowed* to gate
  (`references/systems.md` two-part rule); it is **never** an NPC's arc spine. The **forced** mode = an
  **auto-fire capstone-shape canvas** (`priority ≥ 9`, single Continue, no refuse/accept branch — there is
  no zero-choice engine primitive). The **per-place ceiling** is **author-encoded in each canvas's
  conditions**, NOT an engine location attribute. Disposition comes from the casting hook (Step 3).
- **Progression** comes from *access to the clothing* (revealing outfits are bought / unlocked), not a trait.

---

## 4. The economy — `redesign_phase_3/13` (a corruption-ladder, anti-grind)
**The economy is itself a CORRUPTION LADDER, not a job list.** Income runs legit-low-pay early →
lewd-high-pay as she falls, so **making money and corrupting herself are the same act**, and broke-pressure
*pulls her down the lewd path because that's where the money is.*
- **One wallet** — money is money (no dirty/clean split, no laundering).
- **Income is a corruption ladder** (legit-low → lewd-high; the better money is always down the lewd path).
- **Multiple paths** (anti-grind) — several *different* income activities; blocked on X → do Y.
- **Earning = content** — every paying activity IS a lewd / reactive-world / story scene (work the floor
  revealing, cam, escort), never a chore-click that only adds cash.
- **Pressure kept alive by SINKS, not a tax** — climbing rent/debt + clothing (the reactive-world dial
  costs money) + the empire itself + gifts. The sinks are *wanted* buys (pressure via desire).
- **Pressure ESCALATES across acts** — survival debt → a bigger late threat (rival madam / crooked cop /
  the shark's boss) that still costs money. The *form* escalates; the *presence* of pressure is constant.
- **Recruits are ARCS, not income widgets** — every recruited girl is a full corruption arc (her own
  double-lock + capstone + loop, a Step-4 NPC); her income is a byproduct of playing her content.
- Engine reuse: one `money` trait + the rent system (`[settings.rent]`, the climbing deadline) + Lane-3
  work hosts that earn + the clothing shop as a sink. Rates/path-counts authored per game.

---

## 5. Legibility + pacing — `redesign_phase_3/14`
- **Legibility is a discipline on the quest cards we already have, not a new tracker.** The top "Story
  Goals" card always shows the **current want** (the active desire-ladder rung) AND **the next concrete
  action, naming the PLACE + TIME-WINDOW + REQUIREMENT verbatim** ("Make rent ($120) — work the floor for
  tips at the bar, evenings 6 pm–close", not just "make rent") — RTS's failure was naming the goal, not the
  step; the field's best games (Gakko's walkthrough-as-sidebar) always name where + when. **Mandatory for
  the active card**, and for each NPC's `next` block (`npc_panel`, `systems.md`). Telegraph the next rung
  (locked-visible). Never stale (one current want shown). Per-NPC wants legible in each NPC's quest section.
  **A cross-gated rung names the OTHER arc's state** ("Sal won't go further while the bar's in jeopardy" —
  `14` L7 / the machine §7 D3); a silent cross-lock is a soft-lock.
- **Pacing = tension → release, escalating, then PLATEAU.** Every want ends in a **payoff** (no want without
  one); payoffs escalate up the ladder, then flatten into a **wide livable plateau** at the frontier
  (climb → plateau → climb). Alternate big and small beats; cap the gap between payoffs (always a near
  payoff visible); don't dump the big content early. Rates (climb rate · beats-per-want · payoff frequency ·
  escalation steepness · rent cadence) are authored per game.
- **The endgame escalates in CONTENT, never into management** (the biggest late-game trap — LC's mirror).
  Every empire/endgame beat cashes out as content: a recruit is a full arc, an "upgrade" unlocks new KINDS
  of scenes, the apex (the madam) is the *hottest* beats — never a +income widget or a dashboard.

---

## 6. The frontier — `redesign_phase_3/17` (endless sandbox, not a finish line)
We build **endless sandboxes** (like RTS), not limited games with a win-screen. Three kinds of "ending":
- **Local arc endings — KEEP.** A single NPC's terminal capstone ("you fully corrupted Rosa") ends a
  *thread*, not the game.
- **A hard game-ending — DROP.** No closing win-screen.
- **The FRONTIER — DESIGN.** The top of the desire ladder is the **current edge of authored content**, and
  its rung does **three jobs**: (1) land a real payoff at the charge ceiling; (2) drop into a **livable
  steady-state** (the repeatable loops + stable + reactive world + income stay playable); (3) leave a
  **greyed next-hook seed** ("a rival madam across town has noticed you") — the clip-point a later extension
  bolts onto.
- **Endless ≠ aimless** — at the frontier the tracker says so **honestly** ("you've reached the current peak
  — run your empire; more to come"), never a blank screen (the RTS sin).

---

## 7. The machine — `redesign_phase_3/22` (cross-wiring as the depth spine)
The game is **one machine**, not parallel arcs that share a wallet: NPC arcs + the economy + the player's
rise read/write a shared state and feed each other. Designed HERE, up front, so Step-4 arcs are authored as
components that plug into a machine that already exists on paper (the islands-fail fix). **Design the core
loop first**, then the wires, then check the disciplines.
- **The core loop (the spine).** One economic circuit: conquest → money/access → the next conquest
  (bar game: break the owner → take the bar → bar income funds recruiting girls → their arcs earn → fund
  the madam). Every core NPC gets a **place** in it (casting, `step-3-casting.md`).
- **Two forms of wire** (form 3 — a *finished* arc becomes a resource — is **G6, deferred**):
  - **Form 1 — arc→arc depth gate.** Arc A's *mid/late rung* gated on arc B's *stage*. **Milestone → a
    shared PLAYER flag** the source arc sets (`{type="flag", subject="player", flag_key="bar_seized"}`);
    **"how far along" → the `<npc>_stage` PLAYER trait** (`{type="trait", subject="player",
    trait_key="<otherNpc>_stage", operator="gte"}`). Rule: **milestone → flag; "how far" → stage trait.**
    NEVER a raw cross-NPC trait read (`subject="npc", npc_id="npc_OTHER"` from a foreign canvas is
    unverified — mirror to the player namespace at the source arc).
  - **Form 2 — arc↔economy circulation.** (2a, load-bearing) money earned from arc/activity A is the *gate*
    to reach B — the economy is the connective tissue between arcs (`13` fusion). (2b, flourish) a payout
    **banded** by an NPC's trait — authored as **band-gated sibling choices** (one choice per band, each
    with its own `conditions` + literal-int money `effects`; `beat-authoring.md`), banding on the host
    NPC's trait or a player-mirror.
- **Three disciplines** (the firewalls): **D1** never gate an arc's ENTRY on another arc — only mid/late
  rungs (every arc stays cold-start-enterable; breaks cycles by construction). *Introducing a late-act
  recruit later (her schedule begins in Act 3) is the separate on-ramp-stagger pattern — fine; D1 forbids a
  `conditions` cross-gate on a **present** arc's on-ramp, not sequencing when an NPC enters.* **D2** no
  dependency cycles (the F1 wires form a DAG — checked at the roster, `step-5-roster.md`); **D3** every
  cross-gate is a **locked-visible telegraph naming the other arc's state** (§5 / `14` L7 — a silent
  cross-gate is a soft-lock).
- **No new ledger field** — the machine is designed in the design book's `## The machine` section and
  enforced by ordinary beat `deps` + the `cross_npc`/`economic` beat types (`ledger-schema.md`). One NPC at
  a time still holds (Step 4): A reads a flag B will later set; an unset flag = a locked rung = correct.

---

## Output (written into `design_book.md`)
A **World setup / engine** section carrying: the cascade + double-lock + the stat set (with each leg's job
+ which are built-in vs Tier-3 custom); the **desire ladder** (the chain of named wants from open to
frontier); the **reactive-world** model (which places get which ceiling, which NPCs are predatory); the
**economy** (the income paths + the sinks + the late-act pressure); **the machine** (the core loop + which
arcs wire to which / to the economy — form 1/2, the disciplines); the **pacing** intent; and the
**frontier** (the top rung's 3 jobs + the seeded next-hook). Set `pipeline_phase = "casting"` when done.
*(The full `## The machine` block in the design book is finalized at Step 4/5 — the synthesis of every
arc's §8 wiring contract — but the core loop + who's a node is fixed here.)*

## Self-check
- The cascade + **double lock** are explicit; non-lewd interaction is ungated.
- Every stat names the content it gates (no dead stats); built-in vs Tier-3-custom is correct; **beauty is
  not a leg**.
- The **desire ladder** exists (a chain of wants), not a bar with content at thresholds; every gain serves
  a want.
- The reactive world keys on **clothing** (Lane 2/3, public content), never an NPC arc spine; forced =
  auto-fire capstone; ceiling = per-canvas conditions.
- One wallet; income is a corruption ladder; earning = content; pressure escalates via scaling sinks.
- Pacing is climb → plateau → climb; the **endgame escalates in content, not management**.
- The **frontier** is designed (3 jobs + honest narration); local arc endings kept; no hard game-ending.
- **The machine** (§7): the core loop is designed; every core NPC has a place; the wires are form 1/2 (form
  3 = G6, deferred); D1 (no entry gated) · D2 (DAG) · D3 (cross-gates telegraphed) hold. Legibility (§5) is
  mandatory verbatim (place + time-window) + cross-gates name the other arc.

## Cross-references
`redesign_phase_3/{04,09,11,13,14,17,22}` (full detail; `22` = the machine) · `references/trait-design.md`
(the spine the double-lock rides) · `references/lanes.md` (where reactive/economy content is authored) ·
`references/systems.md` (the clothing two-part rule + the `npc_panel` `next` block legibility) ·
`references/run-mode.md` (ask the crucial forks). Next = `references/step-3-casting.md`.
