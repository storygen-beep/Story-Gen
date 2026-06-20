# Step 5 — the content roster: the checklist of every scene the game needs

The bridge between **Step 4** (the arcs — *who the characters are and how they escalate*) and **Step 6**
(authoring — *writing each scene + the code*). Step 5 turns the approved designs into a concrete **list of
scenes to write**, on paper, before a single canvas is authored. Without it you sit down at "2 empty Lane-2
slots for Sal" and improvise — the game comes out structurally correct but **thin**, and one whole content
*category* (the player/world feeders) never gets invented at all. That thinness is a big part of why LC
felt soulless.

**This re-homes the skill's existing `references/content-design.md`** into the Phase-3 pipeline and rewires
it to everything we've designed since (desire ladder `09`, double-lock `04`/`07`, reactive world `11`,
economy `13`, frontier `17`, run-mode `16`). The RTS-grounded core (the 9 archetypes, the tier ladder, the
feeder economy) is preserved — it was the good part. **Spec-on-paper; the skill file is reconciled at wiring
time, not now.**

---

## Position & inputs
**Pipeline:** 0 good-game · 1 setup · 2 top-level · 3 casting · 4 NPC arcs · **5 CONTENT ROSTER** · 6 authoring.
- **Inputs:** the casting table (`06`), each NPC's approved arc/brief (`07`), the world/locations (`01`), the
  **desire ladder** (`09`), the **per-place reactivity ceilings** (`11`), the **economy paths** (`13`).
- **Output:** a `## Content roster` table in `design_book.md` — one row per scene. Step 6 reads a row and
  builds it; the loop **never improvises a row** (`16`).
- The roster is a **hypothesis** (reorder / cut / add as authoring teaches you), but it exists *on paper
  before the first canvas.*

---

## The two content tracks — and the one the old skill was blind to
Lewd content splits in two. The skill modelled the first well and **omitted the second**:

- **NPC-arc track** — scenes tied to one character's escalation (hub rungs, ambients, walk-ins, capstones).
  The four-lane model (`lanes.md`), each rung **double-locked** (`07`): the player-corruption *door* + that
  NPC's own *lock*.
- **Player / world track** — lewd content **about the player, not any one NPC**. Two kinds now (the second
  is new since the original doc):
  1. **Self-corruption feeders** — solo self-acts, flashing, public dares, job-lewd. They raise the
     player's own `corruption`/`exhibitionism` odometers.
  2. **Reactive-world events** — the **clothing-triggered** lewd reactions (grope → molest → rape) from
     `11`, scaled by place ceiling × NPC disposition, in three modes (sought / choice / forced). New
     first-class roster content.

**Why the player track is load-bearing (the feeder economy).** The NPC double-lock has a player-corruption
**door** (`04`/`07`) — that's the **demand** side. The self-corruption feeders are the **supply** — they're
what opens the door. Rich NPC arcs with no feeder catalog → the door never opens → the arcs stall (the LC
starvation pattern). RTS balances this on purpose (~40 feeders across ~15 venues keep the odometer always
climbing). **Size the feeder supply to the doors it must open** — that balance is the whole point of doing
this on paper.

---

## Everything on the roster hangs on a WANT (the desire-ladder binding — `09` R1/R7)
This is the biggest rewire from the original doc. A roster row is **never** "an activity that raises a
meter." Every row is, in the fiction, the player **pursuing a want she currently holds** (`09`):
- ✗ "Flash at the bar (+1 corruption)."
- ✓ "Work the floor topless — the big tips get you the dress that turns the owner's head" (serves Want 2).

So the roster is authored **against the desire ladder**: for each rung/want on the ladder, *what scenes does
the player do while chasing it?* A row with no want it serves is the grind failure — cut or reframe it
(`09` R4).

---

## The archetype catalog (derived from RTS — `game_explorations/rts-align-verify/rts_scene_registry.json`)
RTS's content *is* a structured registry: 71 scenes / 27 venues, each `{location, title, chance, guide,
requirementsMC:{exhibitionism, corruption}}`. Mined from it, the nine archetypes — the ideation checklist.
Walk every location and every NPC against it.

| # | Archetype | Track | Shape | RTS tier (corr/exb) | RTS examples |
|---|---|---|---|---|---|
| 1 | **Solo self-act** | player | home/private, no NPC, no travel; pure odometer feeder | **ungated, corr 0** | Watch Porn, Camgirl, Masturbate |
| 2 | **Location flash** | player | base activity at a venue → flash event fires on it | **corr 15 + exb 10** | Gym/Mall/Club/Work Flash |
| 3 | **Location sex-escalation** | player | SAME venue, deeper rung — venues are 2–3-rung *columns* | **corr 30 → 45** | Gym Sex; Pool Sex; Jog Sex |
| 4 | **Job / service lewd ladder** | player+ | economic surface turns lewd; money × corruption (= the economy `13`) | **corr 15 → 45** | Restaurant→VIP, Strip Club, Gloryhole |
| 5 | **Public dare / challenge line** | player | a meta-app issues escalating public dares; deterministic track | **corr 30–45, ch 100** | Beach/Street/Park Challenge |
| 6 | **Household ambient grope/tease** | bridge | at-home chore; NPC gropes → feeds NPC arousal | corr 0, NPC-side | Bedroom/Study Grope |
| 7 | **Voyeur / peep** | bridge | catch an NPC mid-act; player feeder + NPC adjacency | corr 0–30 | Peep Sex, Spy Teacher |
| 8 | **Transit ambient** | player | low-tier feeders on a transit "location" | corr 0–30 | Bus Grope / Flash |
| 9 | **Story/condition special** | either | gated on NON-corruption state (followers, pregnancy, time, flag) | corr 0, other-gated | Photoshoot, Lactation, Kidnapped |
| **10** | **Reactive-world event** *(new — `11`)* | player | **clothing-exposure** triggers a lewd reaction, scaled by **place ceiling × NPC disposition**; modes sought/choice/forced | gated on **outfit**, not corruption | alley grope, back-room cornering, docks (forced) |

Archetypes 6–7 are the **bridge** where the player track meets the NPC-arc track. **Archetype 10 is the
reactive world** (`11`): unlike the others it keys on **clothing exposure**, and its *forced* mode is
**act-scoped** (`11`/`15` D — real in the fall, recedes as power rises). Pick archetypes that fit the
*premise + setting* — a bar has no gym, but it has a back room, a stockroom, a late shift, regulars to
flash, an alley out back. Honor each NPC's **vocab ceiling** (`doctrine/08`) when an archetype touches them.

---

## The tier ladder — populate EVERY tier so the climb never dead-ends (RTS, source-verified)
The player odometer is `+1` per charged act, hard cap 45; bands `<5 / 5–14 / 15–29 / 30–44 / ≥45`. The
feeder roster must populate **every tier**:
- **corr 0 (bootstrap)** — ungated self-acts + story/behaviour specials. *Gets her off zero.*
- **corr 15 + exb 10** — the **flash backbone**: one location-flash per public venue. The mid-game workhorse.
- **corr 30 (explicit)** — public sex, job promotions, gloryhole-class (= the first-sex *door* — the bulk).
- **corr 45 (cap)** — the **extreme-public** ceiling: strip/VIP/public-sex.
All-corr-30 capstones with no corr-0/15 feeders = the starvation pattern (she can't *reach* 30). **Seed the
low tiers first.** (The corruption odometer is the door's currency; clothing exposure is `11`'s separate
lever — both live in the player track but gate different things.)

---

## The economy is part of the roster (the `13` binding)
Archetype 4 (job/service lewd ladder) **is the corruption-ladder economy** (`13`): legit-low-pay → lewd-high
-pay, each paying scene *is* content (E4), multiple paths (E3), escalating tiers (E5). So the roster's
job-lewd rows are authored as the economy — and the **sinks** (rent/debt clock, the clothing dial that powers
archetype 10, the empire) are what keep her needing the next paying row. Income, content, and the reactive
world are the **same beats** (`13`).

---

## The roster artifact (a `## Content roster` table in `design_book.md`)
One master table, mirroring RTS's registry shape. Produced at Step 5; Step 6 reads a row and builds it.

| col | meaning |
|---|---|
| **want** | the desire-ladder rung this row serves (`09`) — *the row must have one* |
| **venue / host** | where it lives (a real location id) or the solo-activity it rides |
| **title** | short scene name (the registry `key`/`title`) |
| **track** | `NPC:<slug>` · `solo` · `public-dare` · `reactive` |
| **archetype** | 1–10 above |
| **lane / mode** | 1/2/3/4 (NPC track) · `solo` (player feeder) · sought/choice/forced (reactive, `11`) |
| **gate** | the **double lock** for NPC rows (player-corruption door + `<npc>` lock); **outfit tier × place ceiling** for reactive rows; player `corr/exb` tier for feeders; + flags/time |
| **fire** | `deterministic` (menu pick / chance-100 quest beat) or `random N%` (ambient on a base activity) |
| **hook** | the one-line concept — RTS's `guide` ("Order pizza naked", "Flash at the gym") |

---

## How the player track maps to the engine (it has no lane of its own)
Rides existing mechanisms — don't invent a new canvas type:
- **Self-act / flash (1–2, 8):** a **solo activity canvas** (Lane-3 *host* shape — `manual`, `is_repeatable`,
  `location`, no `npc`), gated on the **player** corr/exb tier, effect raises those odometers. The *base
  activity itself is lewd* (not an NPC walk-in).
- **Location sex-escalation (3):** the same host with higher-tier **locked-visible** rungs (`lanes.md`) — one
  canvas, a tiered column.
- **Job/service ladder (4):** the economic solo-work host (`lanes.md` Lane 3) — author its **lewd escalation
  rungs** as the economy (`13`), not just the earn.
- **Public dare line (5):** a deterministic chain (often a phone "app" thread / one-shot per rung).
- **Reactive-world events (10, `11`):** Lane-2 (location-entry) / Lane-3 events gated on **clothing exposure
  × place ceiling × NPC disposition** (the ceiling is author-encoded in each canvas's `conditions`, not an
  engine field), NOT on the cascade meters; *forced* mode = an **auto-fire capstone-shape canvas**
  (`priority ≥ 9`, single Continue, no refuse/accept branch — there is no zero-choice engine primitive)
  gated above the place's forced-threshold **and** below the power tier that retires it (`11`/`15` D);
  *choice* mode = a normal refuse/accept exit block.
- **Bridge (6–7):** ordinary Lane 2/3 NPC content — author on the NPC track.

---

## Method (the pass itself)
1. **NPC-arc track — per NPC:** walk its arc-shape rungs (R7 §3) × its lane budget → one row per scene, each
   tagged with the **want** it serves (`09`), its **double lock** (`07`), and — for any cross-wired rung —
   the **machine wire** it carries (the other arc's flag/stage it reads, from §8; `22`). Consolidates the
   whole cast into one table — and this is where the **machine is verified** (next), not just where
   cross-NPC gaps are caught by accident.
2. **Player track — per LOCATION × archetype:** walk each venue × the catalog (1–10) → "what self-act / flash
   / public / job-lewd / **reactive event** fits *here* at this premise + ceiling?" → a **tiered column per
   venue** (corr 0 → 15 → 30 → 45) + its **reactive ceiling** (`11`). This is the step that never happened.
3. **Balance the feeder economy:** count the player-corruption **doors** the NPC track demands (every
   seduction capstone's floor) vs the feeder **supply** across tiers. Too few low-tier feeders → doors
   unreachable → add feeders (or lower floors). Make supply/demand explicit.
4. **Bind to the desire ladder & frontier:** every row maps to a want (`09`); rows beyond the **current
   frontier** (`17`) are **deferred — telegraphed as locked-visible seeds**, never silent gaps (D72). The
   roster is **open-topped**: it covers up to the frontier and grows when the frontier is extended.

---

## Self-check before authoring against the roster
- **Both tracks present** — there IS a player/world feeder catalog (incl. reactive-world rows), not only NPC arcs. *(The blind-spot test.)*
- **Every row serves a want** (`09`) — no meter-exercise rows.
- **Tiers populated** — bootstrap (corr 0) + flash (corr 15) feeders exist, not just corr-30 capstones.
- **Economy balanced** — every NPC seduction door is reachable through ordinary feeder play.
- **The machine is verified** (`22` — a REAL check, not "≥1 cross-NPC link exists"):
  - **Core loop closed** — the conquest → money/access → next-conquest loop the machine designed (`22`) is
    present in the roster's rows (the income paths that fund reaching the next target are actually there).
  - **Every core NPC placed** — each core NPC's §8 wires (SETS/READS) appear as roster rows; no core NPC is
    an island.
  - **DAG (D2)** — trace the F1 cross-reads: they form a directed-acyclic graph, every arc cold-start-
    reachable, no two arcs mutually gating each other's depth. A cycle is a deadlock the build won't catch.
  - **No entry gated (D1)** — every cross-read gates a mid/late rung or capstone, never an arc's on-ramp.
  - **Every cross-gate telegraphed (D3)** — each cross-wired rung has a locked-visible row/telegraph naming
    the gating arc's state (`14` L7); no silent cross-lock.
- **Reactive rows present & ceiling-set** (`11`) — clothing-triggered events per place, with modes + the act-scoped forced rule.
- **Archetypes fit the premise** — no gym in a bar game; the venues are this game's real locations.
- **Ceiling honored** — player-track rows touching an NPC sit at that NPC's `doctrine/08` ceiling.
- **No silent caps** — rows beyond the frontier are telegraphed (locked-visible) + counted, never dropped (`17`/D72).
- **Scope = full game** (slice removed) — the venue columns are *filled*, not thinned to a spine.

---

## Run-mode (the `16` binding)
The roster is surfaced to the user as **Mode B** (a skimmable plain-language list — "here are the scenes this
game needs") before authoring; a genuine fork (e.g. "include archetype 5 public-dares or not?") is **Mode A**.
Then Step 6 authors **one row/scene at a time, building green** before the next (`16`). The roster is never
dumped into code in one pass.

## Cross-references
- `06` casting / `07` NPC arcs (inputs) · `09` desire ladder (every row a want) · `11` reactive world
  (archetype 10) · `13` economy (archetype 4) · `17` frontier (open-topped, deferred = seeds) · `16` run-mode ·
  `22` the machine (the roster self-check verifies it — core loop / every core NPC placed / DAG / telegraphs).
- Existing skill (reconcile at wiring): `references/content-design.md` (this re-homes it), `lanes.md`,
  `trait-design.md`, `sex-loop.md`, `doctrine/08`, `beat-authoring.md` (reads the roster each turn).
- Evidence: `game_explorations/rts-align-verify/rts_scene_registry.json`.
