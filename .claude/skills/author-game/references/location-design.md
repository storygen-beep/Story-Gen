# Location design — the map as a designed system, not a backdrop

The skill's self-contained home for **how a game's world is laid out**: the spatial graph, the
naming, the locks, the travel friction, and the rule that every room must earn its place. Read this
before the **map-design step** (`step-2b-map-design.md`, which *uses* this) and before any beat that
adds or moves a location.

**Why this file exists.** A game's people (the cast), its economy, and its machine each get a
deliberate, reviewed design pass. The *map* used to be the one structural pillar nobody designed — it
got enumerated to hold scenes, then emitted by copying a reference game's shape. That is why a game
whose geography differs from the reference shipped incoherent and needed pass after pass to fix by
hand. The map is a **system you design**, with the same care as an arc.

The engine never checks any of this — a wrong, dead, or incoherent map builds GREEN and only reveals
itself in play. Treat this file as the design guide AND the pre-ship gate.

---

## §1 The two jobs + the engine model

A location author must get two things right, and both are silent failures:

1. **Geography** — the nav graph reads like a real place. Leaving the street should not drop you
   inside a private bedroom.
2. **Reachability** — every canvas attached to a location can actually *fire* there (§4).

**Three independent location fields — do not conflate them** (full `[[locations]]` field
reference: `references/engine-reference.md`):

| Field | What it controls | NOT |
|---|---|---|
| `entry_from` | **Navigation.** "You can reach me from here." The **"Leave X" link points to `X.entry_from`**, and a hub's child cards are every location whose `entry_from` points at it (ordered by `navigation_order`). | not hierarchy |
| `parent` | **Structure only** — canvas inheritance + visual grouping. A location's `parent` and `entry_from` may differ. | NOT used for nav links |
| `is_container` + `default_entry` | A **pure-nav wrapper** that auto-redirects into a child and holds no content. | NEVER hosts a canvas — a container **swallows** any attached canvas (it emits only child-nav). Attach canvases to a NON-container standing hub instead. **And always set `default_entry`:** a container with NO `default_entry` **double-prints** its child nav — once as choice links, once in the nav block (`v2.py:9213-9229` — container-no-`default_entry`: choice-links loop + `_generate_hierarchical_navigation`) — so set `default_entry` or use a non-container standing hub. |

The player walks the **`entry_from` chain**; `parent` is bookkeeping. A top-level location (no
`entry_from`) is a **root** — it emits no "Leave" link and is reached only via a walk-activity bridge
(§5) or by being the start. Deep nesting is supported (no engine depth cap); a 2–3-level nest is the
practical sweet spot.

---

## §2 The five topology archetypes — pick one to fit the premise

The genre floor is a **multi-zone town** (zone → venue → room), NOT a single building — a 3-level nest
is the observed sweet spot. The best games author a **small, data-driven map**, not a hand-grown room
tree. Choose the shape from the premise; don't default to "a house."

| Archetype | Shape | Fits | Example real game |
|---|---|---|---|
| **Nested-zones** *(default)* | district → venue → interior room; each hub lists its children | most life-sims: a town/campus + a home | Road to Success, new-life-project |
| **Two-hub free-roam** | 1–2 strong hubs (Home + Work) fanning to rooms, bridged by a commute | a premise anchored to 1–2 places (workplace + home, a base) | The Company |
| **Map-image hotspots** | a drawn city-map with clickable district hotspots + sidebar fast-travel; one component reused per level | a large (10+ zone), replay-heavy world | Become Someone |
| **Street-graph mesh** | named streets, each listing "go to" every adjacent street + its venues | a city that should feel real without a drawn map | Degrees of Lewdity |
| **Time-slot spine** *(the anti-map)* | NO geography — a fixed Morning→Work→Evening chain; places fade in/out with the script | heavily scripted content where a map would be friction | Emilie |

**The Inheritance lesson:** a residence + an attached hotel + a town is a textbook **nested-zones**
map — `Town (root) → Hotel (venue) → floors (sub-hubs) → rooms`. The engine builds multi-floor /
multi-building geometry with ordinary **named hubs + `entry_from`** (a "floor" is just a non-container
hub; there is no floor primitive and none is needed). Don't cap a world at "one floor / one unit" when
the premise is bigger — design the real geography. Do match the *size* to the cast: a tiny cast does
not need a sprawling city; add zones only where content lives — where "content" includes **ambient life** (§6),
not just a plot canvas.

**Sizing is TWO axes: scale AND aliveness.** Scale = how many zones (match the cast). Aliveness = how *lived-in*
the world feels: a **tight mission-slice** (only the locations a beat needs) at one end, a **living city** (extra
atmospheric zones carrying street events, NPC routines, self-care loops the player didn't trigger) at the other.
It's a **content-budget fork, not a quality dial** — every ambient zone is content you fund. A tight slice is
legitimate *when chosen on purpose*; the failure is **drifting** into a lifeless scene-holder because no one asked
"how alive?" (Vesper's first map shipped "utilitarian, not a living world" exactly this way — the anti-sprawl rule
followed off a cliff). Decide the point up front (`step-2b-map-design.md`), and for a sandbox **lean toward the
living end** — the genre runs on a world that breathes. **Depth over breadth:** a small, dense, genuinely-alive
slice beats a sprawling map of thin places. *(This ambient life is WORLD texture — street events, self-care,
routines you cross — NOT padding an NPC's arc-shape budget with fake relational beats; empty NPC arc cells stay
honest, `lanes.md`.)*

**Two roots, bridged by walk activities.** A home-exterior root and a town root are SEPARATE top-level
locations with no `entry_from`, connected by walk-activity canvases (`activity_walk_to_town` /
`activity_walk_home`), not by an `entry_from` link. Keep the private unit, the shared building it sits
in, and the town outside as distinct layers — household NPCs live inside the private unit; neighbors and
witnesses belong in the shared/public layer, never the private unit.

---

## §3 The naming contract

Names are a system too. The field's strongest games are remarkably consistent; match a contract and
hold it.

- **Public venues = bare plain nouns, no article**: `Gym`, `Mall`, `Bar`, `Bank`, `Night Club`,
  `Police Station`, `Adult Shop`. Clean and re-readable.
- **Private/owned interiors = possessive**: `Your Bedroom`, `Audrey's Room`, `Stepfather's Bedroom`.
- **Hierarchy rides the HEADER / nav-depth, NOT the label.** You already know your zone from the page
  you're on, so the venue label stays a clean bare noun (`Bar`, not `Hotel — Bar`). Reserve any
  ALL-CAPS / styled zone header for the parent.
- **Branded / punny flavor lives in BODY copy**, not the structural label (`The Underworld Lounge`
  reads in the description; the clickable label is `The Bar`).
- **Imperative-action labels** are fine where the link *is* the verb (`Go take a shower`).

**House style is allowed — consistency beats flattening.** An articled / em-dash-compound style
("The Residence", "The Hotel — Bar") is a *legitimate* old-money/boutique register (a real shipped game
uses `Company — Lab` throughout). It is **not** a bug to flatten. The only real defect is being
*inconsistent* — some children prefixed, some bare. Pick one register for a game and apply it evenly.

---

## §4 Reachability — every canvas must be able to fire

A canvas fires only where **NPC-present (per schedule) ∩ canvas time-window ∩ player-actually-there-
and-awake** all overlap. Empty intersection = a dead canvas the build won't flag. Anchor every NPC
ambient/capstone where the player *actually crosses that NPC during the daily loop*, not where the
fiction first imagines them. Three recurring traps:

- A `requires_npc` canvas whose location is **not** in that NPC's `[[npcs.schedules]]` never fires —
  schedule the NPC there, or drop `requires_npc` and time-gate the substitution target's own schedule.
- A **portrait hub** (`npc =` set) renders nothing unless that NPC is schedule-present at the hub.
- A window the player sleeps/works through is a dead zone (mind cross-midnight wraps).

Every schedule row resolves to exactly **one** of these three categories (the **Locked** unlock
contract is spelled out in §4.1 below):

| Category | Player can go? | Needs a hub? |
|---|---|---|
| **Reachable** | yes | **yes** — a presence-floor hub |
| **Locked** (`entry_conditions`) | not yet (visible-but-blocked) | deferred — see the unlock contract |
| **Offscreen** (`offscreen = true`) | no (non-navigable "away" label) | no |

### §4.1 The locked-location unlock contract — an NPC scheduled at a locked door

A schedule row at a **locked** location is a *deferred* hub promise. A locked location is a
`[[locations]]` with `entry_conditions` (a flag predicate) + `blocked_message`; the engine's lock is
**visible-but-blocked** — the room still shows on the nav as a greyed card with its `blocked_message`
printed in place (`v2.py:18254-18256` `location-card-locked` + `navDestBlockedReason`), and the passage-entry
guard re-checks on click (`v2.py:9257` `triggerConditionsSatisfied(entry_conditions)` re-check). It is legitimate **only** when the lock reads as "haven't met /
been invited yet" **and** the unlocking beat is reachable at an OPEN location. The lock represents the
social fact; the meeting is the key. There is **no native time-of-day location lock** — the only lock is
this flag gate, so don't invent a door field the engine lacks; put any time/exposure axis on the hub via
`trigger.schedules`, never on the door.

Every locked schedule row falls into exactly one case:

| Case | Shape | Verdict |
|---|---|---|
| **A — private place, the meeting unlocks it** | The locked location *is* the NPC's private space (his apartment); the player meets them at an **open** on-ramp, and that beat sets the unlock flag. | **OK.** Keep the locked row; the unlock beat sets the flag. Do **not** separately flag-gate the hub — the door already gates it (double-gating is the bug). |
| **B — a deeper room of an already-reachable NPC** | A secondary room the NPC routes into (his bedroom off the shared flat); they're meetable elsewhere meanwhile. | **Acceptable only if all three hold:** (1) the lock is **legible** — visible-but-blocked, reads as a closed door, not a disappearance; (2) **co-gated** (the door flag *is* the flag that gates the player's access to that window → zero dead window) **or off-hours + bracketing presence** (a later flag, but the window sits in hours the player doesn't routinely share AND the NPC has open-location presence bracketing it); (3) the locked row is **not** the NPC's only/primary presence. |
| **C — reachable ONLY via a locked location** | The NPC is *only ever* at locked location(s), **or** the unlock flag has no reachable setter — incl. chicken-and-egg: the door is gated on a flag only settable behind the door — **or the resource variant: a toll payable only in currency earnable *past* the toll** (floor-not-block it, §5). | **The bug — unreachable NPC.** Fix: open an on-ramp at a reachable OPEN location with a reachable flag-setter, or start the location unlocked and gate the *canvas/choices* instead of the door. |

**The legible-lock principle.** A present-but-unreachable place must read as a *closed/locked door* (via
`blocked_message`), distinct from **dead presence** (an NPC at a *reachable* location rendering nothing).
The failure to avoid is an NPC shunted into a locked room during a window the player **routinely shares**,
with no open fallback and/or an illegible gate → "where did they go?" And never leave an away/offscreen
block pointing at a reachable hub. Every condition block in `entry_conditions` needs `version = "1.0"` or
it **fails open** — the door silently unlocks (`v2.py:3534` `triggerConditionsSatisfied` version guard; same trap as §5).

*(code-vs-lore note: the Schedule page renders declared `[[npcs.schedules]]` rows regardless of the
door lock, so it will list the NPC at a locked location. With the visible-but-blocked model that's
tolerable, even flavorful — "the boss does the books in the office overnight." The engine has no
discovery/absent lock, only this flag gate.)*

### §4.2 The NAV-INVISIBLE INTERIOR — when a locked door is the wrong tool

A locked location is **visible-but-blocked**: a greyed card sits on the parent's nav grid with its
`blocked_message` showing. That is right when the lock *is* the story ("you haven't been invited yet").
It is **wrong** in two situations, and both come up often enough to name the shape:

- **The room must not be advertised before it exists in the fiction.** A greyed card announces a place —
  and its NPC — to a player who has no idea it is there, including one replaying an earlier act.
- **Getting in is a SCENE, and the scene must be unskippable.** If the door is a nav card, the moment the
  flag flips the player walks straight in and the scene you built as the gate never plays.

The shape for both: **a location with no `entry_from`, plus `auto_exit = false`.** Nothing links to it, so
it has no card anywhere and no NPC badge can render for anyone scheduled there; the only way in is a
canvas exit, and the only way out is a canvas exit you author.

⚠️ **BOTH HALVES OR IT DUMPS THE WHOLE MAP.** Dropping `entry_from` alone is half a job. A location's nav
grid is built from its **children** (locations whose `entry_from` points at it), so a childless, parentless
location renders an empty grid *and* no auto "Leave" link — and an empty nav list trips the
**list-every-location fallback**, which prints `All locations:` and the entire world. `auto_exit = false` is
the flag that tells the engine the emptiness is intentional (`v2.py _generate_hierarchical_navigation`:
`if not navigation_html and auto_exit`). See §5 of `engine-reference.md` for the field.

**Two ways to satisfy the engine, and they are not interchangeable.** A sealed room can instead be kept
quiet by giving it a **child** — a door location whose `entry_from` points back at it, locked on a flag
nothing ever sets. Use that when the door itself is content the player should see and rattle. Use
`auto_exit = false` when the player should not be shown a door at all.

**Checklist before shipping one:** the entering canvas exists and is reachable · the leaving exit is
authored (there is no safety net) · the built passage does **not** contain `All locations` · and, if an NPC
is scheduled there, no badge for them appears on any nav grid in the game.

---

## §5 The nav-learnings — authoring tools the engine now gives you

Four moves that make a map feel alive. Two are pure authoring; two are real engine knobs (v2):

- **Travel-friction (`costs`)** — a `[[locations]]` can charge a per-ENTRY cost:
  `costs = { time = 30, energy = 10 }`. `time` (minutes) advances the day clock; every other key
  deducts that player trait. This is what makes **NPC schedules bite** — if crossing town costs an hour,
  the player can't be everywhere, so *where someone is at a given hour matters*. Use it on the bridges
  between zones (the commute), not on every room. Empty = a free move. Pair it with a paid instant
  **fast-travel** (a walk/taxi/bus activity, unlocked once destinations are discovered) so friction
  never becomes tedium. Unaffordable destinations grey on the nav and bounce with the reason on click.
  **The refill-path exception (floor-not-block):** if a costed bridge/action is the **only** route to where its
  own resource refills or is earned, a *blocking* `costs` strands the player — so **floor the cost instead of
  gating it** (let the effect deduct and clamp at 0; don't make affordability a gate on that one move). A toll
  payable only in currency earnable *past* the toll needs a non-currency bootstrap (a fight/stealth/tool route)
  on the first crossing. This is the resource variant of §4 Case C.
- **Lock-as-prose** — a locked location (`entry_conditions` + `blocked_message`) now shows its
  `blocked_message` **inline on the greyed nav card**, not only on the blocked passage. So the lock
  reads as in-world prose at the point of choice ("The dining room's been dark since the staff went").
  **Every condition block needs `version = "1.0"`** or it fails OPEN (the door silently unlocks).
- **Presence-on-nav** *(already authorable)* — the nav cards already paint avatars of the NPCs
  scheduled at each destination (via `getNpcsPresentAtLocation`). The player sees *who's there* before
  spending time to travel. You get this for free by authoring schedules + hubs — surface it by keeping
  hubs where NPCs actually are.
- **Sidebar place+time locator** *(already authorable)* — a quest card's `ready_canvas` (pointing at a
  scene with `trigger.schedules`) makes the sidebar render 📍 place + 🕒 time-window, so "where is the
  live content" is answered, not hunted. Wire the active want's `ready_canvas` to the real beat.

---

## §6 The room-content floor + pre-ship location self-audit

**The room-content floor (the rule the old audit couldn't express):** *every navigable
(non-container, non-offscreen) location must host at least one canvas — an activity, ambient, hub, or
capstone — OR be a deliberately-locked deferred shell whose unlock beat is on the roadmap.* A
reachable, **empty-dead** room (no plot AND no ambient — the player walks in and bounces off) is the failure.
But "earns its keep" counts **ambient life, not only plot function**: a zone that hosts a solo activity (eat,
bathe, rest), a random **street/ambient event**, or an NPC routine you cross earns the click **even with no
mission attached** — that texture is what makes a world feel lived-in, and cutting it is how a map reads
"utilitarian, not a living world." Cut only a room with **neither** plot **nor** ambient life and no near-term
plan. ("A kitchen with nothing to do" is a dead end; "a kitchen where you make a meal and your housemate
sometimes walks in" is content.) This is distinct from the
activity-scoped "dead-bath" check: it quantifies over the *location set*, so it catches a room with no
NPC and no activity at all.

Run this before delivery — none of it is caught by the build:

- [ ] No canvas's `trigger.location` is an `is_container = true` location (§1).
- [ ] Topology matches a chosen archetype (§2); roots + layering are coherent (private-unit ≠
      shared-building ≠ town; two roots bridged by walk activities).
- [ ] Every `navigation_order` slug has `entry_from` pointing back here.
- [ ] Naming follows one consistent contract (§3) — no mixed prefixed/bare siblings.
- [ ] **Every navigable room earns its keep — a plot canvas OR authored ambient life (a solo activity / street
      event / NPC routine you cross) OR a deliberate locked shell with a roadmap setter (§6); only empty-dead
      rooms (neither plot nor ambient) are cut.**
- [ ] **Aliveness delivered (§2):** the map matches the declared point on the mission-slice ↔ living-city line —
      a "living city" carries ≥1 ambient/texture zone (a street hub, a place to just be) beyond the plot rooms.
- [ ] Reachability triad holds for every NPC ambient/capstone; portrait hubs are schedule-present (§4).
- [ ] Every schedule row is exactly one category — reachable (hub) / locked (unlock contract) /
      offscreen — and no away block points at a reachable location without a hub.
- [ ] **Every locked location's unlock flag has a real setter** — `entry_conditions` are **never scanned**
      by the flag-chain validator (it reads canvas triggers + choices only), so a room gated on a flag
      nothing sets builds green, reports "All flag chains valid," and is permanently unenterable. Grep the
      flag; find the canvas that sets it. Mechanism + the fail-open caveats: `references/toml-gotchas.md`.
      *(Shipped twice: v1's Dining Room, then again in the rebuild written to prevent it.)*
- [ ] **Every room with a declared job has a canvas LOCATED in it** — `grep 'trigger.location = "<id>"'`
      and confirm ≥1 hit. A job asserted in prose while the scene is authored in another room is a dead
      room wearing a promise: the room still renders and stays walkable, so the player arrives at a
      navigable nothing and nothing in the build warns you.
- [ ] Every locked location's `entry_conditions` carries `version = "1.0"` (else it fails open, §5).
- [ ] If travel-friction is used: the costed moves are the *bridges*, and a fast-travel release valve
      exists so friction isn't tedium (§5).

---

## Cross-references
`step-2b-map-design.md` (the generative step that uses this) · `content-framework.md §5` (the world
question set — §5A "what each place is FOR" is the room-content gate this audit enforces) · `lanes.md`
(what attaches where; presence-on-nav) · `toml-gotchas.md` (the `costs` / `entry_conditions` field
shapes + the `version="1.0"` trap) · `engine-reference.md` (the full `[[locations]]` field reference).
The locked-location unlock contract (§4.1) and the offscreen/three-category model (§4) live in this
file — it is the owner of both.
