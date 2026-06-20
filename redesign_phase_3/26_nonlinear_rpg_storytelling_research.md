# 26 — Non-Linear Adult-RPG Storytelling: Field Research + Skill Gap Analysis

How do you *write* a non-linear adult RPG story — and how far is the `author-game` skill from teaching it?
This doc answers both. It pairs a thorough internet survey of the established design theory (and the
sandbox-adult canon) with a file-checked gap analysis of the current skill, then states honestly where the
skill stands and where it should go.

**Position:** a research + analysis doc, **review-only — no skill files were edited and nothing here is
implemented.** It is the future-lookup reference for an eventual redesign; the redesign is a separate
decision LO makes *from* this doc, one task at a time. Produced 2026-06-17 by a 12-agent workflow (6 internet
research angles + 6 file-grounded skill reads → a 6-dimension synthesize→**adversarially-verify**→merge,
where every claimed gap was re-checked against the real files; inflated claims were downgraded, nothing was
hallucinated). Provenance + the raw research dump in §10.

---

## §1 — The reframe: name what an RTS-shape sandbox actually IS

The most load-bearing finding is a vocabulary one. Per Emily Short and Sam Kabo Ashwell, an RTS-shape adult
sandbox is **not a branching tree and not a "scene list."** It is a **Quality-Based Narrative (QBN) /
storylet system wearing an Open-Map skin, with a Loop-and-Grow day cycle for momentum.**

- **QBN / storylets** (Failbetter's *Fallen London* / StoryNexus is the shipped exemplar): content is a pool
  of atomic vignettes, each with a **prerequisite** (a query over qualities — flags, corruption tier,
  presence, time) and an **effect** (mutates those qualities). Order is *emergent*, not authored by
  next-scene pointers. Short's worked proof: discovering three facts in any order needs six branching paths
  ("ugly repetition") but only **four** storylets in QBN — qualities control availability, so authoring cost
  doesn't explode combinatorially.
- **Open Map** (Ashwell) is the spatial container — but he warns it goes "slower-paced and less directed"
  and "requires extensive state-tracking." That is the dead-sandbox failure: explorable but going nowhere.
- **Loop-and-Grow** (Ashwell) is the fix for that: a central thread that "loops repeatedly; state-tracking
  unlocks new options and closes others each cycle." Our day-cycle IS this.
- **Corruption tier** is a branch-and-bottleneck *quality* — a monotonic gate that bottlenecks the iconic
  beats (the capstones) behind a value the player raises through many small choices.

**The lanes map cleanly onto the field's QBN-vs-salience control axis** — *who chooses the next content,
the player or the system:*

| Lane | Field term | Who picks |
|---|---|---|
| **1 — hub** | player-chosen QBN storylet | player (navigates + clicks) |
| **4 — capstone** | player-chosen QBN storylet (high-consequence) | player (reaches the threshold + enters) |
| **2 — ambient** | **salience** content | the SYSTEM serves the most-applicable |
| **3 — walk-in** | **salience** content | the SYSTEM serves it inside a chore |

So the architecture is **correct** — it is exactly the architecture the theory prescribes for this genre.
The skill simply never *names* it (zero corpus hits for QBN / salience / storylet / Ashwell / Short), which
is why "non-linearity" reads as under-theorized even though it is structurally present.

---

## §2 — What the field knows (the six research angles, distilled)

**(A) Choice-structure theory** (Ashwell 2015 *Standard Patterns in Choice-Based Games*; Emily Short 2016
*Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures*; Failbetter QBN):
genuine non-linearity = content gated by **world state**, not by links from a previous scene. Salience
content needs a **most-applicable** selector (best-match + random tie-break + per-day cap), or everything
qualified fires at once. Defend against grind with **interdependent** qualities (one storylet's effect is
another's prerequisite — emergent sidequests), not parallel independent meters. Ashwell's explicit warning:
under-authored "floating modules" **drift to linearity and stat-grinding** — the exact risk of an
under-built lane catalog.

**(B) Sandbox-adult canon** (DoL, Lab Rats 2/Vren, Lilith's Throne, Free Cities, CoC/CoC2, Summertime Saga,
Karryn's Prison, Girl Life/New Life): tier stats **bidirectionally** — high state opens content AND closes
"pure" content (CoC: corrupt past a threshold and the pure NPC variant *leaves*; corruption is "a
double-edged blade"). Solve grind-vs-gate with a **meet-your-tier-to-progress** loop where lower acts still
pay a smaller currency (DoL Control: mild acts become *ineffectual* as you climb). Make gains **permanent /
ratcheting**, never decaying (Lab Rats 2 revamp). Separate the **repeatable pool** (most volume) from
**one-shot sequences** (the rare arcs) — which is exactly Lanes 1-3 vs Lane 4. Interleave concurrent arcs by
gating each on a **different axis** (Summertime Saga: rotate routes; one stat-gated, one time-gated, one
gated on another NPC's completion). Use a **few orthogonal axes**, not one master "lewdness" number (DoL's 8
stats; Karryn's parallel tracks). **Integrate** the corruption loop with the other loops — a corruption
meter that feeds nothing else is the documented Lab Rats 2 failure.

**(C) Living world** (The Sims / Matt Brown GDC 2018; Radiant AI; RimWorld storytellers; Stardew; immersive
sims; DoL): **"seem intelligent, don't BE intelligent"** ("Big A, little i") — complexity the player can't
read is noise; an ambient needs **local coherence** (makes sense given this place/time/tier/who's present)
and the player projects the long arc. Routine is the content pipe **because it's autonomous of the player**
(RDR2/KCD "lived-in" feeling = NPCs with their own jobs/homes). Someone has to **choose which emergent event
fires** (RimWorld's Cassandra vs Randy = a pacing director); flat per-tick random is the Dwarf Fortress end
(alive but shapeless). **The same routine slot yields different content as state advances** (Stardew: heart
events, friendlier dialogue, "post-marriage they almost never say what they did before") — the direct answer
to "how does the world acknowledge the player changing." The **dead-checklist** diagnosis (Ubisoft critique):
content feels dead when it doesn't react to state, doesn't cohere with before/after, and can't be projected
onto — the fix is not MORE nodes, it's state-reactive existing nodes.

**(D) Observe / peep / caught** (DoL; WickedWhims voyeurism devlog; RTS passages; stealth design): an observe
event and a be-observed event are the **same machine** (vantage, occupancy, visibility, consequence) pointed
in opposite directions. **Occupancy** turns a location into a scene — derived from NPC schedules, not
hand-placed (our shipped `npc_at_location` predicate). **Visibility is asymmetric and separate from access**
(a locked door can still leak sight/sound). The **caught roll is a timed/probabilistic race**, not a binary
— the near-miss IS the content (DoL's hidden 20-turn classroom timer). **Consequence must branch on the
catcher's disposition** — caught is *not* uniformly punitive: hostile→punish, opportunist→**blackmail**,
attracted→escalate, and it can *corrupt the catcher* (the single most-repeated finding). **Escalation runs on
a persistent count** (habituation): a peep must change meaning as it repeats (DoL exhibitionism tiers; RTS
`timesWatched`). **Frequency is capped per day** AND counted long-term.

**(E) Wayfinding** (Short on salience; Fallen London UX; Witcher 3 "Ladies of the Wood"; Game Developer
*The Unreliable Gamemaster*; DoL Feats/Journal; breadcrumbing/soft-gating): at scale the bottleneck stops
being "what content is available" and becomes "how does the player **see** what's available." Fallen London
needed author **ranking / pinning / color-coding** because a flat list of everything open is itself a failure
state. The legibility-vs-freedom paradox: over-marking collapses a world into a checklist ("more freedom can
make players feel *less* free"). Witcher 3's marker pre-solving the breadcrumb quest is the lesson — guidance
should orient toward a **place/person/pressure + time window** ("Maria opens the bar at 8"), never the
click-by-click. Carry "next" through **in-world voice** (an NPC saying "come by tonight") with the quest page
as a **soft, self-clearing journal**, not an exhaustive directive checklist. Keep **one or two frontier edges
lit**; let completed threads dismiss.

**(F) Player agency & corruption arcs** (Brice Morrison *Meaningful Choice*; Choice of Games *5 Rules*;
Alexis Kennedy choice/complicity/consequence; DoL Willpower/Control; CoC endings): a choice is **meaningful**
only with **Awareness + Gameplay-Consequence + Reminders + Permanence** (Morrison) — a reskin (same outcome,
different prose) is cosmetic. A transformation feels **authored**, not grinded, when corruption is a
**ratchet** (each concession makes reversal harder until the option is cut off) plus temptation — not
threshold arithmetic. Kennedy's triad: **complicity** is "what you feel in the moment when you are making
that choice... the fulcrum of having agency" — which a stat-grind destroys; he advocates **limited** choices
(3-5, "two opposed and one a bit of both"). **Refusal is content** (DoL: Willpower is a buildable resource;
"no" has its own systems). **Player-identity branches** (dom/sub, willing/coerced, pure/corrupt) multiply
non-linearity **cheaply when they are EXPRESSION axes that re-skin/re-gate shared content** rather than
parallel content trees (Choice of Games Rule 4: identity-expression choices; devs warn full parallel paths
are expensive, so most ship "flavors that converge"). CoC validates **route-keyed endings** ("multiple
primary endings... validating the player's agency").

---

## §3 — Where the skill stands today (verified strengths)

The skill has **won the structure war and the corruption-engine war.** These survived adversarial
verification (file-checked, not flattery):

- **Non-linearity is real and machinery-backed:** the double-lock gate (`step-2-toplevel.md:22-34`), the
  cross-wired "machine" (`step-2 §7:158-188` — Form-1 arc→arc stage gates, Form-2 arc↔economy circulation)
  protected by the **D1/D2/D3 disciplines** (cold-start-enterable, acyclic DAG, telegraphed cross-gates) that
  keep a many-order sandbox deadlock-free. This IS designed emergence, not an authored branch tree.
- **The four-lane model is coherent and correctly grounded** on the who-picks-it control axis
  (`doctrine/02 §1`; `lanes.md:13-18`); Lane-1-leads + "one threshold crossing lights up content across all
  lanes" is genuine emergence-via-interdependence.
- **The skill already fights the stat-grind failure on its own terms:** the desire ladder bans "a corruption
  meter with content bolted at thresholds" and tests every activity "what does she WANT that this serves? No
  answer → grind, cut" (`step-2-toplevel.md:58-69`) — the named floating-modules failure is addressed even
  without the vocabulary.
- **Pattern-F branching forks are taught in real depth** (`doctrine/02 §5.4-5.5`, F1-F5): both arms playable
  in good faith, diverging in *downstream effect* not just text — genuine outcome-divergence craft, **scoped
  to Lane-4 capstones.**
- **The corruption engine is deep:** odometer vs throttle, the two-axis gate, per-NPC odometers, and the
  non-naive P5 "reserve the rich model for the core" (`rts-design-philosophy.md`).
- **The shared-space model is a unified primitive,** not four bolted features (occupancy × access ×
  visibility + vantage; player-always-a-party; `redesign_phase_3/25`); **catch-then-react is fully taught and
  buildable today.**
- **Story/character-first + agency:** `content-framework.md` organizes by subject; `step-4-deep-design.md:13-16`
  bans lane/threshold/flag/placement from the story brief; NPCs are enforced as non-yes-men (pursue / resist /
  scheme / set terms). Dialogue-MODE (played vs narrated) is carried and graded.
- **Wayfinding/pacing/frontier is well-folded into the steps an author runs** (`step-2 §5-6`): the
  next-action-as-PLACE+TIME-WINDOW+REQUIREMENT rule, the cross-gate telegraph, the open-topped frontier with
  honest "you've reached the current peak" narration. The skill correctly rejects "build a tracker" and
  prescribes a usage discipline.

**Do not relitigate the architecture — it is sound.** The original instinct that there is a "structural
hole" was wrong; the adversarial pass downgraded it.

---

## §4 — The gaps, prioritized (file-checked)

| # | Gap | Sev | Evidence (file:line) | Fix |
|---|---|---|---|---|
| 1 | **No player-identity axis** — every player walks one monotonic corruption spine to the same destination | **critical** | player axes = corruption/exhibitionism/money only (`trait-design.md:171-178`); `doctrine/09` has no orthogonal deviancy/promiscuity split; the only dom/sub mention is NPC *cast* variety (`step-3-casting.md:46`) | ONE Step-2 flag (willing/coerced or dom/sub) that **re-gates/re-skins SHARED lanes**, not duplicated content. See §5. |
| 2 | **Intra-arc forks + complicity rule** — arcs are one ordered descent to a single end-state; tier-crossings are stat-driven, never a fulcrum choice | notable | arc = "a sequence of moments... in order" to a singular end-state (`step-4-deep-design.md:73-75`); compiled as one descent list (`step-5-blueprint.md:65-69`); Pattern F locked to L4 capstones | a small per-arc fork budget keyed to the identity flag + a rule distinguishing a **texture milestone** (auto-fire OK) from an **identity-crossing milestone** (staged 2-3-option complicity choice at the fulcrum) |
| 3 | **Caught has no disposition-branch table** — only the "into-her" branch | notable | `redesign_phase_3/25 §6.3` = one disposition (home + into her → flash/cover-up); zero hits for disposition/blackmail/punish | a (catcher disposition × player stat) → **punish \| blackmail \| escalate \| corrupt** fork, reusing the disposition table already at `redesign_phase_3/11:33-36`; feeds the corruption-feeder economy |
| 4 | **Parallel-arc layer is unmanaged** — no salience among live wants; no cross-arc pacing | notable | per-NPC `next` cards render independently, no cross-panel ranking (`systems.md:14`); `priority` taught only as auto-fire tie-break (`beat-authoring.md:295`); grep for stagger/peak-at-once/gate-on-different-axis = EMPTY | a recommend-a-next discipline (rank the spine above ambient pursuits) + a cross-arc rule to **stagger capstone thresholds and gate concurrent arcs on different axes** (Summertime-Saga rotation) |
| 5 | **Lane 2 is the thin lane** — first-match + a 3-visit cooldown, no most-applicable selector | notable | `doctrine/02 §3.1:186` (first-match substitute) + `§3.4:208-212` (only the cooldown; doctrine concedes "may feel too quiet"); Lane 3 got the full Pattern A/B/C + `§4.11` saturation curve | extend the proven Lane-3 banded-chance/ordering to Lane 2; promote `exclusive_group` as default for competing ambients; add a recency weight |
| 6 | **Refusal is a retry mechanic, not content** | notable | Refuse path is "a SHORTER scene" / fails to set the chain flag (`doctrine/02 §5.4:654`, `lanes.md:178`); no willpower track, no "held the line" arc | a Refuse may set its **own** distinct flag opening a resistance/abstinence track + an optional need-state-modulated willpower check (low energy / high arousal lowers the bar) |
| 7 | **Plan/ledger can't represent mutually-exclusive (XOR) routes** | notable (latent) | `ledger-schema.md:51` deps = "must exist first" (prerequisite DAG only); no fork/exclusive/mutex beat type or field | an optional `excludes`/`mutex_group` field on the plan object + a Step-6 DAG check that the player can't reach both arms (load-bearing once forks land) |
| 8 | Architecture unnamed (QBN/salience/storylet — zero corpus hits) | minor | grep across skill + doctrine returns ZERO | a short framing note naming QBN + salience + open-map + loop-and-grow, citing the floating-modules failure the gating discipline exists to prevent |
| 9 | **Escalation is purely additive** — no bidirectional deprecation of tame/pure content | minor | desire ladder open-topped/additive (`step-2:58-71`); forward-only legitimate-by-declaration (`:205-208`); deprecation IS taught as fiction-reactivity (`content-framework.md:128/178`) but never as the player-facing TRADE | optional pattern: as corruption rises, tame rungs render muted / stop paying feeder currency, and pure NPC variants retire on a threshold — framed as the **cost** of tiering up |
| 10 | **No callback-to-manner** — reactivity keys on current STATE, never HOW a fork was taken | minor (downstream of #1) | the whole `§4` reactivity web keys on tier/flag/outfit/wallet (`content-framework.md:157-196`); nothing references willing-vs-coerced | once an identity/manner fork exists, add a reactivity question asking whether later content references HOW a crossing was taken |
| 11 | **No route-keyed ending** — every player lands at the same open frontier | minor (downstream of #1) | frontier's three jobs are payoff/steady-state/next-hook (`redesign_phase_3/17`); per-NPC terminals differ by *which* NPC, not *how the arc was run* | a per-NPC terminal capstone may differentiate by route using the divergent flags Type-B already sets |
| 12 | **Voice-SHIFT exemplar absent at the point of writing** — the skill's highest craft promise is demonstrated nowhere | minor | spec'd (`step-4-deep-design.md:70-72`, `content-framework.md:142`) but the only example (Sal) is arc-summary with zero dialogue; `doctrine/05 §8` rewrites are flat-vs-literary, NOT same-NPC tier-1-vs-tier-4 | inline ONE same-NPC greeting pair (tier 1 vs tier 4) in `beat-authoring.md` (or a short `voice.md`) — cheapest high-leverage fix |
| 13 | **Warmer/demeanor reactivity (M3/M4) billed but not built** | minor | quality #8 bills it + `content-framework §4A/§4B` prompt it, but `11_reactive_world_design.md:16-18` rules social reactivity OUT; no buildable treatment parallel to doc 11 | build the M3/M4 demeanor+reputation pattern as a buildable treatment, OR downgrade quality #8 to "prompted, author-built" |
| 14 | **Observe-count habituation** — a peep means the same thing day 1 and day 10 | minor | zero hits for `times_peeped`/`times_caught`/habituation; only stat-tier escalation taught (`25:178`) | a per-act cumulative counter, banded with the existing `§4.11` saturation technique |
| 15 | Discoverability hygiene | minor | `systems.md:8-14` indexes only clothing/rent/phone/customization/HUD — omits day-cycle/offscreen, sex-loop, costs (well-taught at `toml-gotchas.md:57-76`, `sex-loop.md`); RTS 9-archetype catalog (`redesign_phase_3/18` + `rts_scene_registry.json`) not pointed to from the skill; visibility-matches-door self-check (`25:226`) not surfaced into Step-6; overhear (`hear`) ships no worked TOML | add see-also rows + a references pointer + hoist the visibility check into Step-6 + a 3-line overhear stub |

**The pattern across nearly every fix:** the **machinery already exists, uncomposed.** Permanent flags,
Type-B Pattern-F forks, orthogonal axes (corruption-vs-exhibitionism already proves multi-axis works,
`doctrine/09:678`/§5.3), the disposition table (`doctrine/11`), the `§4.11` banded saturation curve, the
`§4` reactivity web — all present, just never wired for the higher-order move. **This is doctrine work, not
engine work** — an unusually cheap backlog (compose existing pieces, don't invent systems).

---

## §5 — The one critical gap, in depth: the player-identity axis

The skill teaches the player's transformation as **a single monotonic corruption climb that every player
runs the same way to the same destination.** The only question the game ever asks is *"how far did you go?"*
It never asks *"who did you become?"* There is no axis for player identity — no dom/sub, no willing/coerced,
no corrupt-her-vs-redeem-her. This was the **one gap that survived adversarial verification as critical.**

It is **load-bearing**: it is *why* gaps #2 (complicity at the fulcrum), #10 (callback-to-manner), #11
(route-keyed ending), and #7 (mutex routes) cannot exist — all four are downstream of an identity fork the
skill never teaches you to author. You cannot call back to, end differently on, or branch around a choice
about who the player is, if that choice was never authorable.

**The genre is defined as much by "what kind of person did this run make me" as by "how far did I get."** The
skill currently models only the second. The field (Choice of Games Rule 4, CoC's route-keyed endings, DoL's
Willpower) models both — and does it **cheaply**, because identity is an **expression axis that re-skins and
re-gates SHARED content**, not a second parallel game. One flag; the existing scenes bend around it; a
dominant player and a submissive player experience the same kitchen/NPC/bathroom moment differently.

**The cheapest, highest-leverage single change in the whole report** is therefore: a Step-2 question that
introduces ONE identity flag re-gating shared lanes (touch-points: `step-2-toplevel.md` + `trait-design.md`,
with one worked example). If exactly one thing is ever done from this doc, make the player a **variable**,
not a **constant.**

---

## §6 — The other genuinely-non-linear blind spot: the parallel-arc layer

Besides identity, the second real hole (gap #4) is that the skill is excellent at **single-arc** legibility
and pacing but does not manage the **multi-arc** layer that makes a sandbox *feel* non-linear rather than a
stack of linear arcs running in lockstep:

- **No player-facing salience among live wants.** `redesign_phase_3/14:31` shows exactly one current want on
  the main ladder, but the per-NPC `next` cards (`systems.md:14`) can be many at once with **no ranking /
  recommended-next**. The player is oriented per-arc yet can be paralyzed by parallel choice. Fallen London
  needed author ranking/pinning precisely for this; the `priority` field exists but is taught only as an
  auto-fire tie-break, never as player-facing salience.
- **No cross-arc pacing.** Pacing rates (`14` P4/P6) are stated **whole-game / single-arc only**; nothing
  staggers capstone thresholds or gates concurrent arcs on different axes (the Summertime-Saga rotation),
  so nothing prevents every open arc peaking at once — or a dead stretch where every live arc is mid-buildup.

Both are net-new and authorable today over existing machinery (the `priority` field, the gate-type variety
the canon recommends).

---

## §7 — "Did we miss any mechanic?" — the full inventory beyond lanes + peep/caught

The original framing listed only lanes 1-4 + door/peep/caught. The skill also teaches, and a redesign must
hold, all of:

- **Clothing/wardrobe** (`doctrine/11`) — `worn_corruption` (gates public content) + derived beauty + the
  exhibitionism ratchet; clothing may gate public/world content + Lane 2/3 reactive events but **never an
  NPC's arc spine** (the backwards on-ramp anti-pattern).
- **Rent / economic pressure** (`doctrine/12`, `[settings.rent]`) — the "I need money" opener made
  mechanical; arm it AFTER income via `start_after_flag`.
- **The economy AS a corruption ladder** (`step-2 §4`) — legit-low-pay → lewd-high-pay, so earning and
  corrupting are the same act; EARNING = CONTENT; pressure via sinks, not a tax.
- **Phone / apps** (`doctrine/13`, `[phone]`) — a purchased second-world layer; triggers support NO
  day/time/location/random (use `days_since_flag`).
- **Customization** (`doctrine/14`) — player + per-NPC rename/relationship-label; must emit `@player` /
  `@<npc>` tokens, never bake a customizable name into a label.
- **Day-cycle + offscreen** — `offscreen=true` as a 3rd location category + the sleep/day-advance router
  carrying the player across the clock.
- **Schedules / presence + the reachability triad** (`doctrine/10`) — a canvas fires only when
  NPC-schedule ∩ canvas-window ∩ player-present-awake overlap; engine is strict co-location (loose Lane-3
  presence is faked via a meta-location).
- **Sidebar / HUD as the world model** (`systems.md` row 5) — `npc_panel` cards so the player can plan
  Lane 3; player stats banded by type.
- **The sex-loop** (`sex-loop.md`) — the triggerless node-routed repeatable menu after the once-only
  capstone; state must be numeric traits, reset on entry AND exit.
- **Resource gating via costs** (`toml-gotchas.md`) — energy/hygiene gate ONLY through `costs`, never
  `effects` (effects = a cosmetic meter).
- **Fail-state declaration** (`step-2 §8`) — you must declare on purpose whether failure exists at all.
- **The frontier / endless model** (`redesign_phase_3/17`) — no win-screen; open-topped ladder; the frontier
  rung lands a payoff, drops to a livable steady-state, and seeds a greyed next-hook.

Door/peep/caught itself is mostly **shipped and taught**; the only genuinely-pending piece is **config-2
(observing two NPCs together)** — an engine limit (one-portrait-per-NPC renderer, single-valued `npcId`),
honestly flagged at `content-framework.md:243` / `redesign_phase_3/25:117-119`.

---

## §8 — The honest synthesis

The skill has **quietly solved the hard structural problem and left the interesting one untouched.** Gating
+ cross-wiring + the four-lane control axis + the open-topped frontier genuinely produce a non-linear
sandbox, and the corpus cites itself line-for-line to prove it. What the skill delivers is **order-freedom
over arcs + combinatorial situational divergence** (outfit × place × NPC). What it does **not** deliver is
**outcome divergence** — who the player becomes. Every player runs the same climb to the same destination.

That single absence is the whole frontier for this skill. The secondary theme worth naming: the skill
repeatedly **knows** a concept (deprecation-as-recede, disposition branches, salience) but teaches it in only
one place and never composes it where it's needed (onto Lane-1 rungs, onto Caught, onto Lane 2). So the
backlog is "compose existing pieces," not "invent new systems" — which makes it cheap to burn down.

**If exactly one thing is ever done from this doc: make the player a variable, not a constant** (§5). The
next two: refusal-as-content (#6) and the complicity rule (#2). The parallel-arc layer (#4) is the other
genuinely-non-linear win. Everything else is craft refinement and discoverability hygiene — real, worth
doing, secondary.

---

## §9 — Research caveats (read honestly)

- Several sources returned **HTTP 403** to direct fetch (DoL Miraheze, Patreon, Grokipedia, TV Tropes), so
  some DoL/CoC/Lab-Rats specifics come from **search-result summaries, not full-page reads**. They are
  self-consistent and cross-corroborated where possible, but treat exact numbers (e.g. DoL stat ranges,
  timer lengths) as indicative.
- **"Waveform narrative" was not confirmed as Emily Short's term** — she uses *salience-based* and
  *waypoint*. The prompt's "waveform" is unverified; do not cite it as hers.
- **Road to Success itself could not be verified from a primary dev source** — no public design doc exists;
  our RTS knowledge rests on our own `game_explorations/` exploration (`rts-align-verify/`,
  `road_to_success/`), which is direct-observation but not dev-confirmed intent.
- **No source addresses adult/erotic sandbox design *theory* specifically** — all cited theory is
  genre-neutral non-linear-narrative theory applied here. Adult-specific corruption-pacing is extrapolation.
- **The 4-lanes ↔ QBN/salience mapping is the analysis's synthesis** (a well-grounded one), not a published
  claim about *our* engine.
- **A stale-memory nuance:** a verifier flagged the memory line "catch-then-react BUILD still open" as
  stale because the *skill* teaches catch-then-react as buildable (true). But that memory line tracks a
  *game-build task* (The Inheritance's `aud/gray_bath_walkin` interstitial rework), which may genuinely
  still be open. Two different things — verify before "fixing" the memory.

---

## §10 — Provenance + sources

- **Workflow:** run `wf_82f1b243-768` (resumed once after 3 transient socket failures on the verify stage;
  all 6 dimensions ultimately file-verified). Merged result + per-dimension verdicts in the task output.
- **Raw research dump** (all 6 angles' principles + applicability + uncertainties):
  `tool-results/bk3v5zvyp.txt` in the session transcript dir.
- **Memory:** `[[nonlinear-rpg-skill-research]]` (index in `MEMORY.md`).
- **Key sources** (verifiable): Sam Kabo Ashwell, *Standard Patterns in Choice-Based Games* (2015);
  Emily Short, *Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures* (2016) +
  *Storylets: You Want Them*; Failbetter Games — *Fallen London* / StoryNexus; Choice of Games, *5 Rules for
  Writing Interesting Choices*; Brice Morrison, *Meaningful Choice in Games* (Awareness/Consequence/Reminders/
  Permanence); Alexis Kennedy — choice/complicity/consequence + the "fulcrum of agency"; *Degrees of Lewdity*
  (Vrelnir); *Corruption of Champions* / CoC2 (Fenoxo); *Lab Rats 2* (Vren); *Summertime Saga*;
  *Karryn's Prison*; *Girl Life* / *New Life* (Willpower); The Sims — Matt Brown, GDC 2018 *Emergent
  Storytelling Techniques in The Sims* ("Big A, little i"); Bethesda Radiant AI; RimWorld AI storytellers;
  Stardew Valley schedules; WickedWhims (TURBODRIVER) *Voyeurism / Window Peeping* devlog; Witcher 3 *Ladies
  of the Wood* (over-marking critique); Game Developer, *The Unreliable Gamemaster*.

---

## Status
**Analysis only — no skill files edited, nothing implemented.** This is the future-lookup reference. The
redesign is a separate decision; LO drives one task at a time. Recommended starting point when it begins:
gap #1 (the player-identity axis, §5). Sibling docs: `21_field_survey_and_skill_review.md` (the prior
skill review), `25_shared_space_visibility_model.md` (the peep/caught family), `18_step5_content_roster.md`
(the archetype catalog this doc says to surface). Related anti-grind/desire theory already in the corpus:
`09_desire_driven_progression.md`, `14_legibility_and_pacing.md`, `17_frontier_endless_model.md`,
`22_the_machine_interconnection.md`.
