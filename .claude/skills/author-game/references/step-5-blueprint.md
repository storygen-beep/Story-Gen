# Step 5 — blueprint: turn the STORY into the exact, gated, placed, ordered scene list (one subject at a time)

Step 4 imagined **what happens** — the lived story, the voice, the descent as a run of moments. Step 5
**decides the structure**: it takes that loose story and turns it into the discrete, named, lane-tagged,
ordered, gated, placed **scene list** — the thing Step 7 (authoring) translates straight into TOML without
re-deciding anything. Step 6 (feedback) then grades this blueprint.

**Why this step exists.** Without it, the story jumps straight to TOML and all the real choices (which lane,
what gate, where it fires, the flag wiring, the order, the opening) get made fast and half-hidden inside
authoring. That is the exact spot where the work "moved too fast." Pulling those choices into their own step
**makes the skill's core promise true**: the user reviews *intent* in the design book, and authoring is a
faithful translation of a design that was already seen and okayed — because by the time authoring runs, there
is nothing left to decide.

**Because this is the step that slows the structuring down, its working style is PROPOSE-FIRST.** It does not
quietly decide the structure and write it — for each subject it **proposes the plan, explains it in plain
words, brainstorms the real choices with the user, and only then writes.** It never commits structure to the
page silently. Writing first and reporting after is the exact failure this step was built to fix — see
**Interaction** below; this is not optional polish, it is how the step runs.

**What this step is, in one line.** It is the **mechanism half of the old Step 4** — the design brief's stat
ladder (§3), lane map (§5), capstone triggers (§6), and wiring contract (§8); the player track's thresholds
and feeder count (§2D/§2E); the world's ceilings, schedules, systems, and locks (§5B/§5D/§5F/§5G); all of the
reactivity wiring (§4) — **plus** the plan-seeding that used to be rushed at the top of authoring — pulled
out so STORY (Step 4) and STRUCTURE (Step 5) are never decided in the same breath.

---

## Inputs
The finished **STORY** layer from Step 4 (`design_book.md`: the player thread, each NPC's story brief, the
world's dramatic jobs, the reactivity-as-experience) · Step 2's cascade / economy / desire-ladder / frontier /
machine-core · the cast (Step 3) · **`content-framework.md`** — the question set this step writes content to
*align with* (Step 6 grades against the same set) · the reused mechanism library: `trait-design.md` (the
spine), `lanes.md` (lanes + budgets + telegraph), `sex-loop.md` (the repeatable menu), `systems.md` (phone /
clothing / rent / sidebar).

## The ordering rule (enforced by the ledger)
Blueprint runs **subject by subject, mirroring Step 4's supply→demand→stage order**, then a holistic pass.
The ledger `blueprint` block tracks `{ player, npcs, world, wiring }`; same gating as `deep_design` — don't
start `npcs` until `player == "done"`, and `wiring` is **last** (it can only wire scenes that already exist).
*Why:* the player's feeder count is fixed before the NPC floors that gate on it (the same anti-starvation
order Step 4 used, now with real numbers).

---

## Pass 1 — the PLAYER track: list it, lane it, gate it, place it (§2 mechanism)
Take Step 4's player story and decide its structure. Output: a **`### Player blueprint`** block in
`design_book.md` (a scene list + a gate/placement table).
- **List the scenes** — bootstrap solo acts, **self-care / daily-routine hosts (shower, bath, eat, sleep,
  work)**, exhibition rungs per venue, income-ladder scenes, the ceiling scene, any non-corruption ladder.
  Each gets a name.
- **Lane + budget** — tag each solo-host (Lane-3 player-lewd shape) vs ambient; size to `lanes.md`.
- **Wire the hosts as fused units** — for each self-care / daily-routine host, decide its three jobs: the
  restore/earn (the chore), the solo-lewd branch (the feeder, gated on player tier), and which NPC walks in
  (the Lane 3 substitution, `requires_npc` + a corruption-banded `chance` that climbs — `references/lanes.md`).
  A host at a co-presence location with no walk-in and no feeder is the dead-bath gap — catch it now.
- **Gate** — the actual `corruption`/`exhibitionism` value each rung needs (§2D thresholds); the resource
  `costs`; the locked-visible telegraph text. **The trait-spine decision lives here** — odometer vs throttle,
  which trait drives, per `trait-design.md`.
- **Economy made real** — the income-ladder values, the wanted sinks, the key-item costs + what each unlocks,
  the pressure clock **and whether it bites** (the fail-state — wire it or write the one-line "no failure").
- **Seed the feeder count** (§2E) — start the band-by-band tally; close it at the end of Pass 2.
- **Ledger:** `blueprint.player = "done"`.

## Pass 2 — each NPC: the descent list, lane-tagged, gated, placed (§3 mechanism) — ONE at a time
Take one NPC's Step-4 story and compile it. This is the **mechanism half of the design brief**.
- **The descent list (job A)** — turn each story turning-point into a named, ordered scene. Read it down the
  page as the fall: does each step follow believably from the last? A jump is a gap — bounce it UP to Step 4
  for a missing moment; do not invent a new beat here (this step *structures* the story, never *extends* it).
- **Lane + budget** — assign each scene a lane (1 hub-rung / 2 ambient / 3 walk-in / 4 capstone / solo-host);
  size to the arc-shape budget (`references/lanes.md`). Empty cells stay empty (peer → no Lane 3;
  service → no Lane 2/3).
- **Gate** — the stat ladder + spine (`trait-design.md`); the **double lock** on every lewd rung (the
  player-corruption door + the NPC's own trait lock; non-lewd stays ungated); the capstone triggers +
  thresholds + flags (odometer, never the `arousal` throttle); the costs; the locked-visible telegraph.
- **Place** — give each scene a location + time-window + the NPC's schedule (the lane-by-lane map compiled to
  slots); check the reachability triad (NPC present ∩ window ∩ player there & awake) and the presence floor.
  *Provisional here* — the world schedule isn't final until Pass 3, so Pass 4 reconciles placement whole-map.
- **Media** — name each placed scene's intended visual (the establishing shot; for a hot beat, the act clip),
  one line per scene. These games are image-first, so what the picture is is a design decision, not a Step-7
  afterthought (`references/media.md`).
- **Wire** — the §8 contract: every flag this arc SETS and READS, bound by D1 (entry never gated) / D2 (no
  mutual lock) / D3 (every cross-gate telegraphed naming the other arc).
- **The repeatable menu** — for a core NPC, spec the sex-loop menu (`sex-loop.md`); peripheral/service get none.
- **Per-NPC self-check** — spine fits the shape (no dead/split meter); double-lock present; late-act target
  carries its own complete ladder; depth matches casting (no gold-plating); wiring written; traits named.
- **Ledger:** when the cast is done, **close the feeder count** (every NPC floor reachable from the player
  supply through ordinary play) and set `blueprint.npcs = "done"`.

## Pass 3 — the WORLD: place mechanism (§5 mechanism)
Compile the world's structural half ONTO the spatial graph **already designed at Step 2b** (the topology,
roots, layering, naming, and travel-friction live there + in `structure_registry.locations`). This pass
places mechanism — schedules, locks, ceilings — onto that map and reconciles it; it does NOT re-decide
geography. Output: a **`### World blueprint`** block; updates the `structure_registry` preview.
- **5B ceilings** — the per-place limit on how far content goes, author-encoded in canvas `conditions`
  (there is no location attribute for it) + how it act-scopes out as she gains power.
- **5D schedules** — who's where, when; tag each row reachable / locked / **offscreen**.
- **5F systems** — phone threads (fire on flags + elapsed days only), the clothing catalog, the rent schedule,
  the sidebar `npc_panel` rows + the quest-card chain, customization fields (`systems.md`).
- **5G access** — locks + travel + the locked-visible map; confirm the Step-2b travel-friction (`costs` on
  the zone bridges) + its fast-travel valve, and that locks are lock-as-prose (`entry_conditions` +
  `blocked_message`, `version="1.0"`) — `location-design.md` §5.
- **5H shared-private perception** — for each shared private space CONFIRMED in play (Step 4 §5H / Mode A),
  build it the corrected way (design rationale): keep the room **enterable** (do NOT hard-lock — a
  hard `entry_conditions` lock makes its screen a dead-end), give it a **dynamic occupant description**, and
  gate the ACTIVITIES by occupancy — the player's self-care shows `is_absent`, the **peek lives ON the room
  canvas** gated `is_present`. Caught = catch-then-react on the player's shower (chance, gated who's-home,
  not a clock). Register: RTS-flat (~30w base, scheme in a `thought_bubble`), density only at the once-per-arc
  tier. Never author a place that wasn't confirmed.
- **Ledger:** `blueprint.world = "done"`.

## Pass 4 — the holistic wiring / order / opening pass (§4 mechanism) — LAST
Invents no new scenes. It **orders and wires the whole inventory**, and seeds the plan.
- **The dependency map (DAG)** — lay every cross-read flat: D1 no entry gated · D2 no cycle (every arc
  cold-start-reachable) · D3 every cross-gate telegraphed · the core money→access→conquest loop **closes** ·
  every gate has a reachable setter. Wire the §4 reactivity ("when she falls the sister gets easier") as
  ordinary `cross_npc`/`economic` deps.
- **The opening as concrete scenes** — the boot, the start location, the 2–3 things doable at zero, the first
  named want, the 10-minute taste, and every arc's ungated cold-start on-ramp.
- **The fail-state ripple** (§4F) — confirm the pressure clock bites on expiry, or record the one-line "no
  failure by design."
- **Close supply-vs-demand** (§2E) — the final whole-game feeders-vs-floors count.
- **Reconcile placement** — confirm every Pass-2 provisional slot against the now-final world schedule.
- **Seed the ledger `plan`** — turn the whole inventory into ordered beats: one beat per desire-ladder want /
  scene, `id = beat_NNNN`, `status = planned`, `target_phase`, `introduces`, `next_up` order. *(This is the
  plan-seeding moved up from authoring-entry; authoring now only emits the scaffold TOML and proves green.)*
- **Ledger:** `blueprint.wiring = "done"`, then **`pipeline_phase = "feedback"`**.

---

## The output artifact
The **blueprint** goes into `design_book.md` as plain-language prose + tables — the scene lists, the
gate/lane/placement tables, the dependency map, and the plan preview — and it seeds the ledger `plan`. It is
**never TOML** (that's Step 7) and never the scene's actual prose (also Step 7). Bump `book_revision` as each
subject-pass lands. The blueprint is what Step 6 grades and Step 7 builds from.

## Interaction — propose, don't just write (the heart of this step)
Blueprint's default is **NOT** "decide it and write." It is **propose → explain → brainstorm → write**, and it
**never commits structure to the page silently.** Run that four-beat rhythm **once per SUBJECT** (the player,
then each NPC, then the world), not per scene:

1. **Propose** — lay out the plan for this subject: e.g. "the sister's fall in eight scenes — which she clicks,
   which ambush her, the order, where the locks sit."
2. **Explain in plain words** — *why* each call is what it is, in everyday language. No wall of lane/gate
   jargon; the user reviews *intent*, so the proposal has to be readable (the simple-language rule, `run-mode.md`).
3. **Brainstorm** — surface the few real forks and settle them together: "does the fall jump here? should this
   be a click or a walk-in? where should the first lock land?"
4. **Write** — only once the shape is agreed, write the full scene list / tables into the design book.

**The guardrail — propose per SUBJECT, not per scene** (or this tips into death-by-questions, the failure
`run-mode.md` bans). Go deep on the genuine forks (the descent curve, a lane judgment call, the gate philosophy
— once per arc-shape) and breeze past the obvious ("this hello scene is just a click at the kitchen — nothing
to debate"). **What varies is how much you brainstorm; what never varies is that you propose before you
write.** A silent write is one failure; a question per scene is the other — this rhythm is the line between
them. At each subject boundary, propose the next subject from the `blueprint` ledger block.

## Self-check before feedback
- **Every story moment has a structured home** — no orphan scene from Step 4 left un-placed.
- **Every lewd rung is double-locked; non-lewd interaction is ungated.**
- **Every arc is lane-tagged and placed** — reachability triad holds, presence floor met, empty cells empty.
- **The DAG is acyclic**, every arc entry is cold-start-enterable, every cross-gate is telegraphed.
- **The feeder count is closed** — the deepest NPC floor is reachable through ordinary player play.
- **The opening is concrete scenes**, not just the Step-2 declaration.
- **The `plan` is seeded and ordered.**
- **No TOML, no scene prose written** — both belong to Step 7.

## Worked example (bar game)
Step 4's Sal story (threshold-free): *"your late partner's loyal best friend, wanted you for years, hates
himself for it; slow-burn to the night he stops resisting."* Blueprint **compiles that same story**: Sal's
descent = 6 named scenes across Lane 1 (talk/serve → tease → first touch), one Lane 2 ambient, and the
first-night capstone; spine = `npc_sal.corruption` odometer + `npc_sal.arousal` throttle; the tease rung gates
`npc_sal.corruption ≥ 3` + flags; the first-night capstone **double-locks** `npc_sal.corruption ≥ 5` AND
player `corruption ≥ 30`; all placed at the bar, evenings; SETS `sal_opened_up`; the repeatable loop opens
after. The diff between Step 4's threshold-free Sal and this one is the whole teaching point: *story there,
structure here.*

## Cross-references
`step-4-deep-design.md` (the STORY this structures) · `content-framework.md` (the questions it aligns to) ·
`trait-design.md` / `lanes.md` / `sex-loop.md` / `systems.md` (the mechanism library) · `step-6-feedback.md`
(grades this) · `beat-authoring.md` (Step 7 — translates this; the plan-seeding now lives here) · `run-mode.md`
(the rhythm + the documented relaxation) · `ledger-schema.md` (the `blueprint` block). Set
`pipeline_phase = "feedback"` when all four passes are `done`.
