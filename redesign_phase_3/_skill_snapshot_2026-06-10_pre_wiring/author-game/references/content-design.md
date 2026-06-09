# Content design — decide WHAT scenes exist before authoring HOW

The rest of the skill tells you **how** to build a canvas (lanes, gates, prose register, vocab
ceiling) and gives each NPC a **budget of empty slots** (R7 brief §5 / `lanes.md`). Nothing decides
**what fills the slots** — the actual roster of scenes and activities. Without this step you sit down
at "2 empty Lane-2 slots for Sal" and improvise on the spot; the game comes out structurally correct
but thin, and one whole content *category* never gets invented at all (below). This reference is the
missing creative-direction pass: **generate the content roster first, then author against it.**

Run it at setup (after cast + locations + R7 briefs exist — `setup-interview.md` Step 3.5) and consult
it every continue turn (the beat loop fills a roster row, never improvises one). The roster is a hypothesis
like the roadmap — reorder, cut, add — but it exists *on paper before the first canvas*.

## Two content tracks — and the one the skill is blind to
Lewd content splits in two. The skill models the first well and **omits the second entirely**:

- **NPC-arc track** — scenes tied to one character's escalation (hub rungs, ambients, walk-ins,
  capstones). This is the four-lane model (`lanes.md`), gated on that NPC's spine + player-corruption
  floors (`trait-design.md`).
- **Player / world track** — lewd activities that are **about the player, not any one NPC**: solo
  self-acts, location flashing/exhibitionism, public dares, job-lewd. These feed the player's *own*
  `corruption` + `exhibitionism` odometers. The lane model has no home for them — even Lane 3 frames a
  solo activity only as a *host for an NPC walk-in*. So nothing in the skill ever prompts you to invent
  this category, which is **why a game starves its player-corruption odometer** (the Last Call finding,
  2026-06-07).

**Why the player track is load-bearing, not flavor (the feeder economy).** NPC seduction content gates
on a player-corruption FLOOR (RTS `requirementsMC`; the two-axis gate, `rts-design-philosophy.md` P9).
That floor is the **demand** side. The player-track activities are the **supply** side — they're what
raises the odometer. Author rich NPC arcs with no feeder catalog and the odometer barely moves, the
floors never clear, the arcs stall. RTS balances this deliberately: ~40 feeder activities across ~15
venues keep the odometer always climbing so the floors are reachable through ordinary play. **Size the
feeder supply to the floors it must clear** — that balance is the whole point of doing this on paper.

## The archetype catalog (derived from RTS — `game_explorations/rts-align-verify/rts_scene_registry.json`)
RTS's content *is* a structured registry: 71 scenes / 27 venues, each `{location, title, chance, guide,
requirementsMC:{exhibitionism, corruption}}`. That registry is the worked example of a roster. Mined
from it, the nine archetypes — your ideation checklist. Walk every location and every NPC against it.

| # | Archetype | Track | Shape | RTS tier (corr/exb) | RTS examples |
|---|---|---|---|---|---|
| 1 | **Solo self-act** | player | home/private, no NPC, no travel; pure odometer feeder | **ungated, corr 0** | Watch Porn, Camgirl (Live), Masturbate |
| 2 | **Location flash** | player | base activity at a venue → flash event fires on it | **corr 15 + exb 10** | Gym/Mall/Club/Classroom/Bathroom/Work Flash, Library Exhibitionism |
| 3 | **Location sex-escalation** | player | SAME venue, deeper rung — venues are 2–3-rung *columns*, not single scenes | **corr 30 → 45** | Gym Personal Sex→Shower Threesome; Swim Flash→Pool Sex; Jog Flash→Jog Sex |
| 4 | **Job / service lewd ladder** | player+ | economic surface turns lewd; money/career × corruption | **corr 15 → 45** | Restaurant career→VIP gangbang, Strip Club, Office, Gloryhole, Discount Sex, Pizza |
| 5 | **Public dare / challenge line** | player | a meta-app issues escalating public dares; deterministic quest track | **corr 30–45 + exb 20–30, ch 100** | Beach / Street / Park / Car-Wash Challenge ("Naked Life App") |
| 6 | **Household ambient grope/tease** | bridge | at-home chore/study; family member gropes → feeds NPC arousal | corr 0, NPC-side | Bedroom Grope, Study Brother/Dad Grope, Bedroom Tease |
| 7 | **Voyeur / peep** | bridge | catch an NPC mid-act; player feeder + NPC adjacency | corr 0–30 | Peep Brother/Dad Sex, Movie Grope, Spy Teacher |
| 8 | **Transit ambient** | player | low-tier feeders on a transit "location" | corr 0–30 | Bus Grope / Flash / Masturbate |
| 9 | **Story/condition special** | either | gated on NON-corruption state (followers, pregnancy, time, behavior flag) | corr 0, other-gated | Model Photoshoot (followers), Lactation (pregnant), Kidnapped (night) |

Archetypes 6–7 are the **bridge** where the player track meets the NPC-arc track (RTS's family arcs
live here). Pick archetypes that fit the *premise + setting* — a bar game has no gym, but it has a
back room, a stockroom, a late shift, regulars to flash. Honor each NPC's **vocab ceiling**
(`doctrine/08`) when an archetype touches that NPC.

## The player-corruption ladder (what each tier unlocks — RTS, source-verified)
The odometer is `+1` per charged act, **hard cap 45**; bands `<5 / 5–14 / 15–29 / 30–44 / ≥45`. The
feeder roster should populate **every tier** so the climb never dead-ends:
- **corr 0 (bootstrap)** — ungated self-acts + story/behavior-gated specials. *Gets the player off zero.*
- **corr 15 + exb 10** — the **flash backbone**: one location-flash per public venue. The mid-game workhorse.
- **corr 30** — the **explicit tier**: public sex, job promotions, gloryhole-class. (= first-sex floor; the bulk.)
- **corr 45 (cap)** — the **extreme-public** ceiling: strip-club / VIP-gangbang / public-sex.
A roster that's all corr-30 NPC capstones with no corr-0/15 feeders is the starvation pattern — the
player can't *reach* 30. Seed the low tiers first.

## The roster artifact (a `## Content roster` section in `design_book.md`)
One master table, mirroring RTS's registry shape. Produced at setup; the beat loop reads a row and builds it.

| col | meaning |
|---|---|
| **venue / host** | where it lives (a real location id) or the solo-activity it rides |
| **title** | short scene name (the registry `key`/`title`) |
| **track** | `NPC:<slug>` · `solo` · `public-dare` |
| **archetype** | 1–9 above |
| **lane** | 1/2/3/4 (NPC track) or `solo` (player track — see lane mapping below) |
| **tier** | player floor (`corr N` / `exb N`) **+** any NPC odometer (`<npc>.relation ≥ N`) |
| **fire** | `deterministic` (a menu pick / chance 100 quest beat) or `random Nx%` (ambient on a base activity) |
| **hook** | the one-line concept — RTS's `guide` ("Order pizza naked", "Flash at the gym") |
| **gate** | flags / conditions / clothing / time beyond the tier |

## How the player track maps to the engine (it has no lane of its own)
The player track rides existing mechanisms — don't invent a new canvas type:
- **Solo self-act / location flash (archetypes 1–2, 8):** a **solo activity canvas** (Lane-3 *host*
  shape — `manual`, `is_repeatable`, `location`, no `npc`/`requires_npc`), gated on the **player**
  corruption/exhibitionism tier via `conditions`, whose effect raises those odometers. It is NOT an NPC
  walk-in — it's the *base activity itself being lewd*. (RTS layers the lewd event on the base activity
  with a `chance`; you can do either a direct activity or a random event on a neutral one.)
- **Location sex-escalation (3):** the same host with higher-tier rungs as **locked-visible** choices
  (`lanes.md` ladder) — the venue is one canvas with a tiered column, not N canvases.
- **Job/service ladder (4):** the **economic** beat's solo work host (`lanes.md` Lane 3 / beat-type
  table) — but author its *lewd* escalation rungs, not just the earn. Money × corruption.
- **Public dare line (5):** a deterministic chain (often a phone "app" thread or a one-shot per rung).
- **Bridge archetypes (6–7):** ordinary Lane 2 / Lane 3 NPC content — author them on the NPC track.
This is the amendment `lanes.md` Lane 3 now carries: a solo host can fire a **player-lewd event**, not
only an NPC walk-in, and the solo lane is also the **corruption-feeder economy** — not merely the earn loop.

## Method (the pass itself)
1. **NPC-arc track — per NPC:** walk its arc-shape rungs (R7 §3 ladder) × its lane budget → one roster
   row per scene. Consolidates R7 §4/§5 across the whole cast into one table (catches cross-NPC gaps).
2. **Player track — per LOCATION:** walk each venue × the archetype catalog → "what self-act / flash /
   public / job-lewd fits *here* at the premise + ceiling?" → a **tiered column per venue** (corr 0
   bootstrap → 15 flash → 30 sex → 45 extreme), sized to scope. This is the step that was never happening.
3. **Balance the economy:** count the player-corruption FLOORS the NPC track demands (every seduction
   capstone's floor) vs the feeder SUPPLY across tiers. Too few low-tier feeders → the floors are
   unreachable → add feeders (or lower floors). Make the supply/demand explicit in the roster.
4. **Size to `scope_mode` + budgets:** `slice` → a thin but tier-complete feeder spine (≥1 bootstrap +
   ≥1 flash per active venue) + the gold NPC's full arc; `full_game` → the venue columns filled. Log
   deferred rows as locked-visible telegraphs, never silent gaps (D72).

## Self-check before authoring against the roster
- **Both tracks present.** There IS a player/world feeder catalog, not only NPC arcs. (The blind-spot test.)
- **Tiers populated.** Bootstrap (corr 0) + flash (corr 15) feeders exist, not just corr-30 capstones.
- **Economy balanced.** Every NPC seduction floor is reachable from the feeder supply through ordinary play.
- **Archetypes fit the premise.** No gym in a bar game; the venues are this game's real locations.
- **Ceiling honored.** Player-track scenes touching an NPC sit at that NPC's declared ceiling (`doctrine/08`).
- **No silent caps.** Deferred roster rows are telegraphed (locked-visible), counted, and logged — not dropped.

## Cross-references
- `lanes.md` — the four lanes (NPC track) + the Lane-3 player-lewd-event amendment.
- `trait-design.md` / `rts-design-philosophy.md` — the two-axis gate + why the feeder economy is load-bearing (P9).
- `sex-loop.md` — the deep repeatable surface a corr-30+ venue/NPC column terminates in.
- `doctrine/08` — per-NPC vocab ceiling (caps how explicit any roster row may get).
- `setup-interview.md` Step 3.5 (produces the roster) · `beat-authoring.md` (reads it each turn).
- Evidence: `game_explorations/rts-align-verify/rts_scene_registry.json` + that slug's `notes.md`.
