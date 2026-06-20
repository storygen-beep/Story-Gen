# Step 5 — content roster: decide WHAT scenes exist (before authoring HOW)

The bridge from arcs (Step 4) to authoring (Step 6). The rest of the skill tells you **how** to build a
canvas and gives each NPC a **budget of empty slots** — nothing decides **what fills them**. Without this
step you sit down at "2 empty Lane-2 slots for Sal" and improvise; the game comes out structurally correct
but thin, and one whole content *category* (the player/world track) never gets invented at all. This is the
missing creative-direction pass: **generate the content roster first, then author against it.**

Run it after cast + briefs exist; the Step-6 beat loop fills a roster row, never improvises one. The roster
is a hypothesis like the desire ladder — reorder, cut, add — but it exists *on paper before the first
canvas.* Source: `redesign_phase_3/18` (which re-homes the former `content-design.md`). Output: a `## Content
roster` section in `design_book.md`. Set `pipeline_phase = "authoring"` when done.

---

## Two content tracks — and the one the lane model is blind to
- **NPC-arc track** — scenes tied to one character's escalation (hub rungs, ambients, walk-ins, capstones).
  The four-lane model (`references/lanes.md`), gated on the **double lock** (Step 2 / `step-4-npc-arcs.md`).
- **Player / world track** — lewd activities **about the player, not any one NPC**: solo self-acts,
  location flashing/exhibitionism, public dares, job-lewd, AND the **reactive-world events** (archetype 10).
  These feed the player's *own* `corruption` + `exhibitionism` odometers. The lane model has no home for
  them, so nothing prompts you to invent this category — **why a game starves its player-corruption
  odometer** (the Last Call finding).

**The feeder economy (why the player track is load-bearing).** NPC seduction content gates on a
player-corruption FLOOR (the double-lock door). That floor is the **demand**. The player-track activities
are the **supply** — what raises the odometer. Author rich NPC arcs with no feeder catalog and the odometer
barely moves, the floors never clear, the arcs stall. RTS keeps ~40 feeders across ~15 venues so the floors
are reachable through ordinary play. **Size the feeder supply to the floors it must clear** — that balance
is the whole point of doing this on paper.

**Every row hangs on a WANT** (the desire ladder — `redesign_phase_3/09`). A roster row whose only
justification is "raises corruption" is the grind failure; reframe it under a want or cut it.

## The archetype catalog (RTS-derived — your ideation checklist)
Walk every location and every NPC against it. (Evidence: `game_explorations/rts-align-verify/rts_scene_registry.json`.)

| # | Archetype | Track | Shape | tier (corr/exb) |
|---|---|---|---|---|
| 1 | **Solo self-act** | player | home/private, no NPC, no travel; pure odometer feeder | ungated, corr 0 |
| 2 | **Location flash** | player | base activity at a venue → flash event fires on it | corr 15 + exb 10 |
| 3 | **Location sex-escalation** | player | SAME venue, deeper rung — venues are 2–3-rung *columns* | corr 30 → 45 |
| 4 | **Job / service lewd ladder** | player+ | economic surface turns lewd; money × corruption (= the economy, `redesign_phase_3/13`) | corr 15 → 45 |
| 5 | **Public dare / challenge line** | player | a chain of escalating public dares; deterministic quest track | corr 30–45 + exb 20–30 |
| 6 | **Household ambient grope/tease** | bridge | at-home chore → family member gropes; feeds NPC arousal | corr 0, NPC-side |
| 7 | **Voyeur / peep** | bridge | catch an NPC mid-act; player feeder + NPC adjacency | corr 0–30 |
| 8 | **Transit ambient** | player | low-tier feeders on a transit "location" | corr 0–30 |
| 9 | **Story/condition special** | either | gated on NON-corruption state (followers, pregnancy, time, flag) | corr 0, other-gated |
| **10** | **Reactive-world event** *(new — `redesign_phase_3/11`)* | player | **clothing exposure** triggers a lewd reaction (grope→molest→rape), scaled by **place ceiling × NPC disposition**; modes sought / choice / forced | gated on **outfit (`worn_corruption`)**, not corruption |

Archetypes 6–7 are the **bridge** where the player track meets the NPC-arc track (author them on the NPC
track). **Archetype 10 is the reactive world**: unlike the others it keys on **clothing exposure**, its
*forced* mode is an **auto-fire capstone-shape canvas + single Continue** (no zero-choice primitive), and
its per-place ceiling is **author-encoded in the canvas conditions** (not an engine attribute). Pick
archetypes that fit the *premise* — a bar game has no gym, but it has a back room, a stockroom, a late
shift, regulars to flash, an alley out back. Honor each NPC's **vocab ceiling** (`doctrine/08`) when an
archetype touches that NPC.

## The player-corruption tier ladder (populate EVERY tier so the climb never dead-ends)
The odometer is `+1` per charged act, cap ~45; the feeder roster should populate every tier:
- **corr 0 (bootstrap)** — ungated self-acts + story/behavior-gated specials. *Gets the player off zero.*
- **corr 15 + exb 10** — the **flash backbone**: one location-flash per public venue. The mid-game workhorse.
- **corr 30** — the **explicit tier**: public sex, job promotions (= first-sex floor; the bulk).
- **corr 45 (cap)** — the **extreme-public** ceiling: strip/VIP/public-sex.
A roster that's all corr-30 NPC capstones with no corr-0/15 feeders is the starvation pattern — seed the
low tiers first.

## The roster artifact (a `## Content roster` table in `design_book.md`)
| col | meaning |
|---|---|
| **venue / host** | where it lives (a real location id) or the solo-activity it rides |
| **title** | short scene name |
| **track** | `NPC:<slug>` · `solo` · `public-dare` · `reactive` |
| **archetype** | 1–10 above |
| **lane / mode** | 1/2/3/4 (NPC track) · `solo` (player feeder) · sought/choice/forced (reactive, `11`) |
| **want** | the desire-ladder rung this row serves (`09` — no meter-exercise rows) |
| **tier** | player floor (`corr N` / `exb N`) **+** any NPC odometer (`<npc>.relation ≥ N`) |
| **fire** | `deterministic` (a menu pick) or `random Nx%` (ambient on a base activity) |
| **hook** | the one-line concept ("Order pizza naked", "Flash at the gym") |
| **gate** | the **double lock** for NPC rows (player-corruption door + `<npc>` lock); **outfit tier × place ceiling** for reactive rows; player `corr/exb` tier for feeders; + flags/time |

**Open-topped:** rows past the current frontier are logged as **telegraphed locked-visible seeds**
(`redesign_phase_3/17`), never silent gaps.

## How the player track maps to the engine (no new canvas type)
- **Solo self-act / location flash (1–2, 8):** a **solo activity canvas** (Lane-3 *host* shape — `manual`,
  `is_repeatable`, `location`, no `npc`/`requires_npc`), gated on the **player** corruption/exhibitionism
  tier, raising those odometers. It is the *base activity itself being lewd*, NOT an NPC walk-in.
- **Location sex-escalation (3):** the same host with higher-tier rungs as **locked-visible** choices.
- **Job/service ladder (4):** the **economic** beat's solo work host — author its *lewd* escalation rungs,
  not just the earn.
- **Public dare line (5):** a deterministic chain (often a phone "app" thread / one-shot per rung).
- **Reactive-world events (10):** **Lane-2 / Lane-3** canvases gated on **`worn_corruption` × place ceiling
  (per-canvas conditions) × NPC disposition**, NOT cascade meters; *forced* = the auto-fire capstone-shape
  canvas + single Continue; *choice* = a normal refuse/accept exit block. This is the **PUBLIC content**
  clothing is allowed to gate (`references/systems.md`), never an NPC arc spine.
- **Bridge (6–7):** ordinary Lane 2/3 NPC content — author on the NPC track.

## Method (the pass itself)
1. **NPC-arc track — per NPC:** walk its arc-shape rungs (R7 §3 ladder) × its lane budget → one roster row
   per scene (consolidates R7 §4/§5 across the cast; catches cross-NPC gaps).
2. **Player track — per LOCATION:** walk each venue × the archetype catalog → "what self-act / flash /
   public / job-lewd / **reactive event** fits *here* at this premise + ceiling?" → a **tiered column per
   venue** (corr 0 → 15 → 30 → 45) + its **reactive ceiling**. This is the step that never happened.
3. **Balance the economy:** count the player-corruption FLOORS the NPC track demands vs the feeder SUPPLY
   across tiers. Too few low-tier feeders → floors unreachable → add feeders (or lower floors). Make
   supply/demand explicit.
4. **Verify the machine** (`redesign_phase_3/22`): from each arc's §8 wiring contract, list the F1 cross-reads
   (arc A's rung reads arc B's flag/stage) + the F2a circulatory steps (income that gates reaching the next
   target). Trace them: the **core loop is closed** (the income that funds the next conquest is actually a
   roster row), **every core NPC is placed** (no island), the F1 wires form a **DAG** (no cycle, every arc
   cold-start-reachable), **no entry is gated** (cross-reads hit mid/late rungs only), and **every cross-gate
   has a telegraph** (a locked-visible row naming the gating arc — `14` L7).

## Self-check before authoring against the roster
- **Both tracks present** — there IS a player/world feeder catalog (incl. reactive-world rows), not only
  NPC arcs. *(The blind-spot test.)*
- **Every row serves a WANT** (`09`) — no meter-exercise rows.
- **Tiers populated** — bootstrap (corr 0) + flash (corr 15) feeders exist, not just corr-30 capstones.
- **Economy balanced** — every NPC seduction floor is reachable from the feeder supply through ordinary play.
- **The machine is verified** (`22` — a REAL check, not "≥1 cross-NPC link"): core loop closed · every core
  NPC placed · F1 wires form a **DAG** (no cycle, all cold-start-reachable, D2) · no arc ENTRY gated (D1) ·
  every cross-gate telegraphed naming the gating arc (D3 / `14` L7). A cycle is a deadlock the build won't catch.
- **Reactive rows present & ceiling-set** — clothing-triggered events per place, with modes + the
  act-scoped forced rule; forced = auto-fire capstone + single Continue.
- **Archetypes fit the premise** — the venues are this game's real locations.
- **Ceiling honored** — player-track rows touching an NPC sit at that NPC's `doctrine/08` ceiling.
- **No silent caps** — deferred rows are telegraphed (locked-visible) seeds, counted, logged.

## Cross-references
`redesign_phase_3/18` (full detail) · `references/lanes.md` (the four lanes + the Lane-3 player-lewd-event
amendment) · `references/trait-design.md` / `rts-design-philosophy.md` (the double-lock + why the feeder
economy is load-bearing) · `references/sex-loop.md` (the deep surface a corr-30+ column terminates in) ·
`doctrine/08` (vocab ceiling) · Step 6 = `references/beat-authoring.md` (fills a roster row per beat).
