# Design Book — Bar Empire (`eval_bar_empire_wired`)

> The user's review surface. Intent in plain language. Grown one section per pipeline step.

---

## World setup

**POV — Female PC.** Chosen first (Step 0 gate 1). This is cascade-native: corrupt yourself, then
others. Every fantasy below is shaped *for* a woman climbing from the bottom of someone else's house to
the top of her own.

**The fantasy (clears the 3-part bar).**
> Broke waitress at a sleazy bar a man owns → seduce and corrupt *him* until you take the bar from
> under him → then build it into your own empire, recruiting and corrupting other women into your
> stable until you're the madam the city answers to.

- **POV-fit** ✓ — a woman weaponizing seduction to rise, not a man acquiring.
- **Sharp charge** ✓ — power *reversal* (powerless waitress → madam the city answers to) fused with
  seduction-as-weapon. The charge is the climb, not the having.
- **Built-in two acts** ✓ — Act 1 *take the man* (Sal), Act 2 *build the empire* (the stable). The
  cascade is inside the fantasy; nothing is stapled on.

**Desire span (declared, not stumbled into).**
- **Act 1 — the conquest of Sal.** One man. Flavor: transactional heat that *sharpens into conquest* —
  you start trading on his want, you end owning him. He is a target to break-and-own, not a romance.
- **Act 2 — the stable.** Multiple women (and the patrons who pay for them). Flavor: conquest +
  transactional — recruiting and *corrupting* other women into working for you. F/F seduction in the
  recruiting, F/M in the house economy the player now runs.
- **Genders of core targets:** male (Sal, Act 1) → female (recruits, Act 2). The player came for a
  power-climb fantasy; both registers serve the *same* climb, so neither ambushes the other.

**Premise / player.** The player is a broke waitress working the floor of the Velvet Rail, a sleazy
downtown bar Sal owns and runs into the ground. She starts with nothing but the shifts he gives her and
the way men look at her. The player is **named and fully customizable** (name + appearance) — she's the
self-insert at the center of a self-corruption climb, so the player owns her body.

**Systems in use (yes/no only — wiring is Step 6):**
- **Clothing — YES.** The reactive world rides clothing; "what she wears on the floor" is a live dial in
  a bar full of paying men. Non-negotiable for this fantasy.
- **Phone — YES.** A madam runs a *roster of contacts*. The recruiting/empire act needs a channel to
  reach women and clients off the floor.
- **Rent — NO.** The economic pressure here is *the bar's own debt and Sal's grip*, not a landlord. A
  rent meter would compete with the real money spine. Cut.

---

## Cast (names + roles only — arc shapes/voice/stats are Steps 3–4)

| Name | Role (as a person) |
|---|---|
| **Sal** | The owner. Sleazy, broke-but-proud, runs the Velvet Rail. The Act-1 target — the man you take the bar from. |
| **Dee** | The other waitress, been here longer. Tired, sharp, knows where the money goes. First possible recruit in Act 2. |
| **Marcus** | A regular at the bar. Money, a wandering eye, the kind of patron the house economy runs on. |
| **Rosa** | Runs the kitchen / back of house. Older, sees everything, owes Sal nothing. |
| **Vince** | Sal's loan-shark / the man Sal owes. The off-floor pressure squeezing the bar — a lever, not a lover. |

*(Casting in Step 3 will derive the roles the cascade actually needs and reshape this list. Here it is
just people.)*

---

## Locations (the map — creative geography only; locks/schedules are Step 6)

- **The Velvet Rail (main floor)** — the bar itself. The stage. Where shifts, patrons, and the floor
  economy live.
- **The back room** — behind the bar. Sal's office / the card-and-cash room. Where the real business and
  the real privacy happen.
- **The storeroom** — narrow, dark, between floor and kitchen. The first place things happen off-stage.
- **The player's apartment** — cramped, hers. Sleep, dress, the phone, the private climb.
- **The docks / the street outside** — the city beyond the bar. Where Vince's world and the wider empire
  eventually reach.

---

## Top-level design (the engine, economy, desire ladder, frontier)

### The cascade (the spine)
**Corrupt yourself before you can take the man, take the man before you can build the stable.** The
player's own `corruption` is the master key. Three acts:

- **Act 1 — Fall + Build.** She corrupts herself on the floor (solo/public feeders: dressing for tips,
  letting patrons touch, the storeroom favors) *and*, in parallel, builds Sal — befriending/working him
  is **not** corruption-gated. The two converge.
- **Act 2 — Reach (take the bar).** As her corruption crosses tiers, the conquest rungs on Sal *appear*
  (the double lock). She seduces, owns, and finally takes the Velvet Rail out from under him.
- **Act 3 — Deepen (the empire).** Now the owner, she recruits and corrupts women (Dee, then others)
  into the stable — each a full corruption arc — until she runs the house the city pays to enter.

**The DOUBLE LOCK (every lewd NPC scene needs BOTH):**
1. **MC `corruption` ≥ the tier for that KIND of act** — the door, opened by her own feeders.
2. **That NPC's own personal trait ≥ her rung threshold** — the individual lock, built by interacting
   with HER. *(Non-lewd talk/befriend/work is NEVER corruption-gated — it raises the NPC lock in Act 1.)*

### The stat set (each leg names the content it gates)
- **`corruption`** (built-in, always) — the lewd door / the cascade master key. Gates every escalation
  rung across the cast.
- **`money`** (built-in, always) — survival + the clothing/empire sinks + the *pressure* (Sal's/Vince's
  debt) that pulls her down the lewd path.
- **`energy`** (built-in, always) — paces the day; spent via `costs` on shifts/activities, restored by
  sleep.
- **`exhibitionism`** (built-in, optional, INCLUDED) — gates the public-floor exposure content: working
  the floor barely-dressed, flashing for tips, the eventual stage/show beats. Names real content → kept.
- **`influence`** (**Tier-3 CUSTOM trait** — NOT engine-native; declared in `[player.core_traits]`,
  gated with the ordinary `trait` predicate) — the *madam power* leg. Gates Act-2/3 content: who in the
  house answers to her, which recruits she can approach, the city-tier beats. Named content → kept.
- **NOT used:** `fitness`/`intelligence` (no body-arc or academic domain here — would be dead stats).
  **`beauty` is NOT a leg** — derived read-only from worn clothing (`worn_beauty`), owned by the
  clothing system.
- **Per-NPC personal trait** (the individual lock) — chosen per character in Step 4. Sal's is `relation`
  sharpening to a conquest meter; recruits get their own corruption/relation axis.

**Hard vs soft gates (match the fiction):** Sal is always present (soft — broke and around from turn 1).
The *stable* and the city-tier (Act 3) are **hard-gated** on `influence` — those people/places literally
aren't in the picture until she has power. The clothing-reactive floor is a soft dial (always on, scaled
by what she wears).

### The desire ladder (the cascade felt as named WANTS — the player-facing spine)
The meter is backstage; the want is onstage. Each rung is a concrete want whose pursuit raises the meters
that open the next. Surfaced later via quest cards (current want + next concrete action).

1. **"Make rent on tips tonight."** → pursue by working the floor; learn dressing-for-tips. *Unlocks:* the
   thrift rack (better outfits = better tips).
2. **"Turn Sal's head."** → dress up, work him, take the storeroom favors. Raises `corruption` +
   Sal-`relation`. *Unlocks:* Sal starts wanting you back — the conquest rungs appear.
3. **"Get into the back room."** → the private Sal beats; learn where the money and the debt live.
   *Unlocks:* the leverage to move on the bar.
4. **"Take the Velvet Rail."** → the Act-1 capstone: own Sal, then own the bar. *Unlocks:* `influence`,
   Act 3, the recruiting channel (phone).
5. **"Recruit your first girl (Dee)."** → seduce/corrupt Dee into the stable — a full arc. *Unlocks:* the
   house cut, the second recruit.
6. **"Run the house the city answers to."** → the frontier rung (see §frontier).

### The reactive world (clothing-driven, NOT social courtesy)
The world reacts to **what she's wearing** (gated on **`worn_corruption`**, the clothing exposure value —
never on player corruption). Every tone shift goes *lewder/bolder/more predatory*, never warmer.
- **Exposure → transgression:** covered → ignored; low-cut → stares & gropes-in-passing; barely-dressed →
  open groping / cornered; nude-ish → taken — *where place + people allow.*
- **Place ceiling × NPC disposition (author-encoded in each canvas's `conditions`, NOT an engine
  attribute):** the **floor** (public, civilized-ish) caps at stares/comments/passing-gropes; the
  **storeroom / back room** (private, lawless) escalates to cornered/forced; the **apartment** is safe.
  **Marcus is predatory** (escalates hardest); **Sal** is opportunistic; **Rosa** stays flustered/dry.
- **Authored as Lane 2 / Lane 3 canvases** — the PUBLIC content clothing is allowed to gate; NEVER an
  NPC's arc spine.
- **Three modes:** *sought* (she dressed for it) · *choice* (refuse/accept) · **forced** = an **auto-fire
  capstone-shape canvas** (`priority ≥ 9`, `is_repeatable=false`, single Continue, no refuse/accept). Forced
  is **ACT-SCOPED** — prey early (the fall, low `influence`), recedes as her power rises; gated on the
  power tier, not place×exposure alone.
- **Progression = access to clothing** (revealing outfits bought/unlocked at the thrift rack), not a trait.

### The economy (a corruption ladder, anti-grind)
**One wallet.** Income IS a corruption ladder — making money and corrupting herself are the same act.
- **Act 1 paths (legit-low → lewd-high):** plain floor shift (low) → revealing floor shift (more tips,
  needs the outfit + `exhibitionism`) → storeroom favors for patrons (lewd-high, needs `corruption`).
  Blocked on one → do another (anti-grind).
- **Act 3 paths:** the **house cut** (a % of what the stable earns — a byproduct of playing recruit
  content, never a dashboard) → city-tier beats (needs `influence`).
- **Earning = content** — every paying activity is a floor/reactive/Sal/recruit scene, never a chore-click.
- **Pressure via SINKS, not a tax:** Sal's bar-debt deadline (Act 1) → the clothing rack (the dial costs
  money) → recruiting/gifts (Act 3). **Pressure escalates across acts:** the bar's debt (survival) →
  **Vince's boss / a rival madam** (the bigger late threat that still costs money). Presence of pressure is
  constant; the *form* escalates.
- **Recruits are ARCS, not income widgets** — each is a full Step-4 NPC double-lock + capstone + loop.

### Pacing
Climb → plateau → climb. Every want ends in a **payoff** (no want without one); payoffs escalate up the
ladder. Alternate big beats (take-the-bar capstone) with small (a good tip night); always a near payoff
visible; don't dump the empire content early. **The endgame escalates in CONTENT, never management** — the
madam beats are the *hottest*, never a +income widget.

### The frontier (endless sandbox, not a finish line)
- **Local arc endings KEPT** — fully corrupting Rosa / a finished recruit ends a *thread*, not the game.
- **No hard game-ending / win-screen.**
- **The top rung ("Run the house the city answers to") does three jobs:** (1) lands the charge-ceiling
  payoff — she IS the madam, the house runs on her terms; (2) drops into a **livable steady-state** (the
  floor, the stable loops, the reactive world, the house cut all stay playable); (3) leaves a **greyed
  next-hook seed:** *"a rival madam across town has heard your name — and she runs a tighter house."* The
  clip-point a later extension bolts onto.
- The tracker says so **honestly** at the frontier ("you've reached the current peak — run your empire;
  more to come"), never a blank screen.

---

## Casting

The cascade generates the role slots; the seed's people are cast into them. Structural coverage checked:
**pressure source** = Vince (+ Sal's debt as the Act-1 squeeze); **corrupting on-ramp** = Sal (the boss
who gives the risqué shifts) + Marcus (the patron who pays for favors); **core target** = Sal (mandatory,
present). Late-act pressure = Vince's boss / the rival-madam seed (Step 2 frontier).

| NPC | role(s) | hook (dynamic + charge + want) | lane | depth | arc-shape | spine |
|---|---|---|---|---|---|---|
| **Sal** | corrupting on-ramp + **core target** + pressure source (his debt) | The bar owner who signs your shifts and barely covers his own debt — sleazy, proud, used to being the one with power. Charge: you start beneath him and end owning him (the reversal is the whole fantasy). Want: keep the bar afloat and keep you wanting his approval — until he's the one wanting. **Conquest flavor.** | forbidden / dominant-becoming-dominated | **CORE** | **Family / slow-burn** | `npc.corruption` odometer + `npc.arousal` throttle; player `corruption` floors the explicit beats (the expensive treatment — reserved for the central relationship) |
| **Dee** | **core target #2 (the first recruit)** + ally | The other waitress, here longer, tired and sharp — she clocked the game before you did. Charge: a peer you seduce-and-corrupt into working *for* you, the first proof you can run women. Want: survive, get a cut, maybe get out — until you give her a reason to stay and earn. **Conquest + transactional.** | forbidden peer → recruit | **CORE** (Act 3) | **Peer / dating** (recruit variant) | `npc.relation` milestones (the seduction) + her own corruption once recruited |
| **Marcus** | corrupting on-ramp + **peripheral target** + reactive-world host | The flush regular with a wandering eye who tips like the floor owes him a show. Charge: the patron you learn to *use* — first he pays for glimpses, later he's a client of your house. Want: access, a show, to feel like he's buying you. **Transactional heat (predatory edge).** | transactional / predatory | peripheral | **Service / transactional** | player `corruption` + `worn_corruption` (the floor exposure host); `npc.relation` light |
| **Rosa** | ally / enabler (back of house) | Runs the kitchen, owes Sal nothing, sees every dirty thing that crosses the floor. Charge: the one who *knows* and chooses to look the other way — or help you. Want: a quiet life and to not go down with Sal's ship. **Longing (slow, dry warmth) — local thread, not a conquest.** | nurturing / witness | peripheral | **Service** | `npc.relation` (trust) — a local arc ending, no escalation spine |
| **Vince** | **pressure source** + late-act antagonist | Sal's loan shark — the reason the bar bleeds and the reason Sal can be taken. Charge: the off-floor squeeze; later, his *boss* is the bigger threat your empire has to answer. Want: his money back, and a piece of whatever you build. **Conquest-against (a lever, never a lover).** | antagonist | peripheral | **Antagonist** | silent awareness/pressure accumulator (no arc_stages); drives the debt deadline |

**Rough sketches + cross-NPC threads:**
- **Sal** — opportunistic patron at first (lets you take the storeroom favors, takes a cut), warms as his
  `arousal` climbs, then the conquest flips: the back-room beats hand you the leverage, the capstone takes
  the bar. Thread: the day you own the Rail changes how **everyone** treats you (`influence` gate opens).
- **Dee** — Act-1 co-worker (commiserates, ungated talk raises her `relation`); becomes recruitable only
  *after* you own the bar (hard `influence` gate). Thread: **Dee already knows Rosa** — recruiting Dee
  warms Rosa toward you (a `cross_npc` ripple at authoring).
- **Marcus** — the live floor-reactivity host all game (his reactions scale with `worn_corruption`); in
  Act 3 he converts from "patron who pays for glimpses" to "client of the house." Thread: Marcus's money
  is part of the **house cut** once the stable exists.
- **Rosa** — a slow, dry trust arc with a single local ending (she helps you against Sal). No lewd spine.
- **Vince** — the debt deadline pressure (Act 1); his *boss* is the seeded late-act threat at the frontier.

*(Self-check: structural coverage ✓ pressure/on-ramp/core-target/late-act all present; every NPC has a
role + a hungry hook; variety spans forbidden-conquest / peer-recruit / predatory-transactional /
dry-nurturing / antagonist — five distinct lanes; desire span delivered — M conquest (Sal) → F
recruit/conquest (Dee) + F/M house (Marcus); Rosa is a deliberate non-conquest local thread.)*

---

## NPC arcs

> One R7 brief per NPC, one at a time. Sal (core) authored first — he IS Act 1. The rest
> (Dee/Marcus/Rosa/Vince) get briefs in subsequent increments before Step 5; this eval authors Sal in full
> as the structural proof.

### Sal — R7 brief (CORE · family/slow-burn · conquest)

**§1. End-state fantasy.** *(authored first — gates everything below)* The reversal completed: the man who
signed your shifts and let you keep his bar afloat now keeps *himself* afloat on your approval. By the end
of his arc Sal has gone from the owner who takes a cut of your storeroom favors → to the man who needs you
in the back room → to the man who signs the Velvet Rail over to you because he can't imagine the place, or
himself, without you running it. He doesn't lose the bar in a fight; he gives it to you because by then
wanting you *is* who he is. The charge is the slow flip of who owns whom — you end this arc owning the man
and the building, and he's grateful. *(Expands the casting hook: proud-broke-owner → dominated-devoted.)*

**§2. Voice spec.** Lane 1/2/3 = **RTS-flat** — Sal talks like a tired bar owner: clipped, transactional,
a little crude, always half-counting the till. Early he condescends ("Smile more, you'll make rent");
mid-arc the condescension cracks into want he's ashamed of; late he's plain hungry. **Tier-3 prose earned
ONLY in capstones** (the back-room night, the signing-over) — the once-only beats get the lush register;
the repeatable hub stays flat and re-readable.

**§3. Stat ladder + gating spine (the DOUBLE LOCK).** Core → the rich two-meter model.
- **Spine (the lock):** `npc_sal.corruption` (his **ODOMETER** — how far the arc has permanently come;
  gates rungs AND the one-shot capstones) + `npc_sal.arousal` (his **THROTTLE** — resets at climax; gates
  the **repeatable loop only**, never a capstone). Player `corruption` = the **secondary floor / the door**
  on the most explicit beats. *(family/slow-burn spine per trait-design.md — never default to relation,
  never make player corruption the universal spine.)*
- **Stage flags:** `sal_noticed` → `sal_storeroom_done` → `sal_backroom_done` → `sal_owned` (the
  Act-1 capstone flag). Hidden stage labels; flags are the legible milestones.
- **Per-rung double lock (door tier × his lock):**

  | Rung | Door (player `corruption`) | His lock (`npc_sal.corruption`) | Lewd? |
  |---|---|---|---|
  | Talk / work his shift / commiserate | — (UNGATED) | builds his lock | no |
  | Flirt across the bar | tier-1 (`≥ 15`) | `≥ 5` | mild |
  | Storeroom favor (he takes a cut) | tier-2 (`≥ 30`) | `≥ 10` | yes |
  | Back-room private beats | tier-2 (`≥ 30`) | `≥ 20` | yes |
  | Take the bar (capstone) | tier-3 (`≥ 45`) | `≥ 30` + `sal_backroom_done` | yes |

- **Vocab ceiling:** max-explicit (default) at the storeroom rung and above; flirt rung is suggestive.

**§4. Per-rung pretext shapes (the content menu).**
- *Flirt* — lean over the bar counting tips; let him catch you adjusting the outfit he "suggested."
- *Storeroom favor* — he sends you to fetch stock; the patron who paid follows; Sal takes his cut after.
- *Back room* — he invites you past the bar to "go over the books"; the books are an excuse.
- *Take the bar* — the night the debt comes due, you have the leverage and he has nothing left but wanting
  you; he signs.

**§5. Lane-by-lane map** *(family/slow-burn budget ≈ L1 2 · L2 1 · L3 1 · capstones 3 — per lanes.md)*:
- **Lane 1 (hubs):** `sal_bar_hub` (the floor, his shift) · `sal_backroom_hub` (opens at
  `sal_backroom_done`).
- **Lane 2 (ambient reactive):** floor groping/comments scaled by `worn_corruption` when Sal is present
  (opportunistic, not predatory — his disposition).
- **Lane 3 (walk-in):** Sal catches you with a patron in the storeroom and *joins/takes a cut* rather than
  stopping it (a slow-burn DOES get a walk-in).
- **Solo:** dressing-for-Sal at the apartment mirror (raises the lock-pretext).

**§6. Capstones (committed up front — odometer-gated, NEVER the throttle).**
- **C1 — Storeroom night (Type A linear).** Trigger: manual at `sal_bar_hub`. Gate: player `corruption ≥ 30`
  AND `npc_sal.corruption ≥ 10`. Writes `sal_storeroom_done`.
- **C2 — Back-room books (Type A).** Gate: `corruption ≥ 30` AND `npc_sal.corruption ≥ 20` AND
  `sal_storeroom_done`. Writes `sal_backroom_done`. Opens the back-room hub + the repeatable loop.
- **C3 — Take the Velvet Rail (Type B branching, Pattern F).** Gate: `corruption ≥ 45` AND
  `npc_sal.corruption ≥ 30` AND `sal_backroom_done` AND debt-due flag. Writes **`sal_owned` +
  `influence` unlock + `bar_owned`** (the Act-2 master flag the whole empire reads). Two branches: take it
  cold (he's discarded) / keep him as your first kept man (he stays, devoted).

**§7. Per-NPC anti-patterns.** Don't let player corruption become Sal's spine (his own corruption is the
odometer). Don't gate his arc on clothing (clothing gates the *floor reactivity* only — two-part rule).
Don't put the repeatable loop behind a capstone gate or behind his odometer — it's `arousal`-throttled.
Don't make him a yes-man: he takes a cut, he condescends, he resists giving up the bar until the leverage
is real.

**§8. Cross-arc writes / reads.**
- **Writes:** `sal_owned`, `bar_owned`, `influence`-unlock (read by **Dee** recruit gate, **Marcus**
  house-cut conversion, the city-tier beats, and the frontier).
- **Reads:** the debt-due flag from **Vince**'s pressure clock (C3 trigger); `worn_corruption` (Lane 2).

**§9. Cross-references.** `trait-design.md` (family/slow-burn spine, throttle/odometer split) ·
`lanes.md` (budget + locked-visible rungs + voice register) · `sex-loop.md` (the repeatable loop opened at
C2) · Step 2 §cascade (the double-lock door tiers) · casting row (hook + threads).

**§10. Acceptance criteria (the arc is "done" when):** the four stage flags chain reachably; every lewd
rung is double-locked and every non-lewd interaction is ungated; the three capstones are odometer-gated
(throttle off); the repeatable loop opens after C2 on `arousal`; `bar_owned`/`influence` are written and
read downstream; the voice flips condescension → hunger across the odometer; the 8 qualities hold
(legible locked-visible rungs, capstone payoffs land Tier-3, the conquest charge is honored at the peak).

*(Briefs for Dee/Marcus/Rosa/Vince follow in subsequent increments — abbreviated here for the structural
eval; each will carry the same 10 sections at its casting depth: Dee core/peer-recruit with a complete
self-contained late-act ladder, Marcus/Rosa peripheral-light single-odometer, Vince antagonist
accumulator.)*

---

## Content roster

> WHAT scenes exist, decided on paper before authoring HOW. **Both tracks present.** Short for the
> structural eval — tiers are seeded (corr 0/15/30/45) so the climb never dead-ends; Step-6 fills a row
> per beat, never improvises one.

**NPC-arc track**

| venue / host | title | track | arch | lane / mode | want | tier (door × lock) | fire | hook | gate |
|---|---|---|---|---|---|---|---|---|---|
| `loc_bar_floor` | Sal's shift | `NPC:sal` | — | 1 (hub) | "Turn Sal's head" | ungated talk | deterministic | work his floor, take the ribbing | none (non-lewd) |
| `loc_bar_floor` | Sal flirts back | `NPC:sal` | — | 1 (hub rung) | "Turn Sal's head" | corr 15 × sal.corr ≥ 5 | deterministic | lean over the till; he stares | double lock |
| `loc_storeroom` | The storeroom cut | `NPC:sal` | 6/7 | 2 (capstone C1) | "Get into the back room" | corr 30 × sal.corr ≥ 10 | deterministic | a patron follows; Sal takes his cut | double lock + flag |
| `loc_back_room` | Over the books | `NPC:sal` | — | 1 (capstone C2) | "Get into the back room" | corr 30 × sal.corr ≥ 20 + storeroom_done | deterministic | the books are an excuse | double lock + chain |
| `loc_back_room` | **Take the Velvet Rail** | `NPC:sal` | 9 | capstone C3 (Type B) | "Take the bar" | corr 45 × sal.corr ≥ 30 + backroom_done + debt_due | deterministic | the night the debt comes due | double lock + flags; writes `bar_owned`+`influence` |
| `loc_bar_floor` | Marcus pays for a glimpse | `NPC:marcus` | 4 | 4 (service) | "Make rent on tips" | corr 15 × marcus.rel ≥ 1 | deterministic | the regular tips for a show | player floor + light lock |

**Player / world track** (the feeder catalog — the load-bearing supply)

| venue / host | title | track | arch | mode | want | tier | fire | hook | gate |
|---|---|---|---|---|---|---|---|---|---|
| `loc_apartment` | Touch yourself before shift | solo | 1 | solo | (bootstrap) | corr 0 | deterministic | get off zero | ungated |
| `loc_bar_floor` | Flash for a bigger tip | solo | 2 | solo | "Make rent on tips" | corr 15 + exb 10 | random 40% on shift | flash the table that's tipping | player tier |
| `loc_bar_floor` | Floor groping (clothing-reactive) | reactive | 10 | choice | "Make rent on tips" | `worn_corruption` ≥ 1 × floor ceiling (stares/gropes) | random on shift | low-cut = hands in passing | outfit × place ceiling |
| `loc_storeroom` | Cornered in the storeroom | reactive | 10 | **forced** (act-scoped) | (the fall) | `worn_corruption` ≥ 2 × storeroom ceiling (lawless) × low `influence` | random, Act-1 only | barely-dressed in the dark room | auto-fire capstone-shape + single Continue; recedes as `influence` rises |
| `loc_bar_floor` | Work the floor revealing | solo+ | 4 | solo | "Make rent on tips" | corr 30 (lewd-high pay) | deterministic (work menu) | the better money is down the lewd path | player tier (economy ladder) |

**Economy balance (supply vs demand).** Floors the NPC track demands: corr 15 (flirt/Marcus), corr 30
(storeroom/back room/revealing work), corr 45 (take-the-bar). Feeder supply: corr-0 solo (bootstrap) →
corr-15 flash + reactive floor groping → corr-30 revealing work + storeroom escalation → corr-45 reached
via the cap-tier work + reactive ceiling. Every floor is reachable through ordinary shifts. *(Tiers
seeded; Step 6 deepens columns. Frontier rows — the stable/city-tier — logged as locked-visible seeds, not
silent gaps.)*

**Open-topped seeds (telegraphed, not silent):** the Dee-recruit column + the house-cut economy + the
city-tier `influence` beats live past the current authored frontier; they are locked-visible in the desire
ladder (rungs 5–6), authored in later increments.
