# 25 — Shared-Space Visibility Model

Peeping, locked doors, "the bathroom's occupied," walk-ins, and getting caught are **one family of
mechanics, not separate features**. Authored case-by-case they become a pile of contradictory special
cases — the "everything can be done" trap. This doc fixes the format: one model, and every situation is a
*combination* of a few room states.

**Position:** a design spec. It defines the model and the minimal engine primitives the model requires —
**named, not built**. The engine build is a separate decision made *from* this spec. This is *above RTS*
(RTS does walk-ins and catches; it does **not** do occupancy-contention or locked-door peeping), so the
vocabulary is kept minimal and the build is sequenced deliberately. The model **extends the existing lock
contract** (`doctrine/10` §5.4/§5.5); it does not invent a parallel system.

---

## §1 — The problem: a family, not features

"Can we do peeping?" is the wrong question. So are "locked-door peeping?", "open-door peeping?", "can the
bathroom be busy?". Answered one at a time they drift apart and contradict each other at the edges. Answered
*together* they are one small state machine: a room has a few independent properties, the player stands
somewhere relative to it, and the combination affords exactly one action. Define the properties once; every
"feature" is then a row in a table, not a bespoke build.

---

## §2 — The model: three room axes + the player's vantage

Every shared-space situation is a combination of **three independent properties of a room R** plus **where
the player is standing**.

### §2.1 — Occupancy — *who is in R right now*
`empty` / `one NPC` / `two NPCs` (plus the player, when the player is the one inside). This is the
foundational fact everything else reads. It is **not** the player's location — it is "who else is in that
room," which the engine cannot currently ask across rooms (§5).

### §2.2 — Access — *can the player enter R*
`open` / `closed-unlocked` / `locked`. This already exists: a locked room is a `[[locations]]` with
`entry_conditions` + `blocked_message`, visible-but-blocked (`doctrine/10` §5.4). The model reuses it as-is.

### §2.3 — Visibility — *can a party perceive into R without entering*
`none` / `see` (open door, full sightline) / `peep` (keyhole, gap, door ajar — partial sight) / `hear`
(thin wall or a closed door — **audio only**, no sight). Visibility is a property of the **door / wall
between two places**, not of the room alone.

### §2.4 — Vantage — *where the player stands relative to R*
`inside R` / `adjacent` (at the door / sharing a wall, with a sightline or audio line) / `elsewhere`
(no line at all).

> **The load-bearing rule: Access ⊥ Visibility.** They are *independent* axes. A **locked** door can still
> be `peep` or `hear` (the keyhole, the thin wall) — you perceive without entering. An **open** door is
> `see` *and* enterable. Collapsing them ("locked = you get nothing") is the exact misread this model
> exists to prevent.

---

## §3 — The player-always-a-party rule

A shared-space scene is valid **only if the player is the observer, the observed, or a participant.** Four
configurations:

| # | Observer | Observed | Example |
|---|---|---|---|
| 1 | **Player** | 1 NPC | peep on him in the shower |
| 2 | **Player** | 2 NPCs | catch two housemates together |
| 3 | 1 NPC | **Player** (solo) | an NPC catches her masturbating |
| 4 | 1 NPC | **Player + NPC** | an NPC catches her having sex with another NPC |

- **Invalid: NPC → NPC** with the player absent. If the player is neither watching, watched, nor
  participating, there is no scene — do not author it.
- Configs 1 and 3 are mirror images across the same door (she watches him / he watches her); the model
  treats "who is the observer" as just *which side of the visibility line the player is on*.

---

## §4 — The combination table (the law)

Each `(vantage × occupancy × access × visibility)` resolves to exactly one afforded action. Author to this
table; do not invent edge behaviour outside it.

| Player vantage | Occupancy of R | Access | Visibility | → Afforded action | Status |
|---|---|---|---|---|---|
| inside R | an NPC enters R | — | — | **walk-in on you** (he arrives mid-activity) | **works today** (co-location) |
| adjacent | 1 NPC | open | see | **peep freely**, or step in and **catch them** | needs occupancy |
| adjacent | 1 NPC | locked / closed | peep | **peep only — can't enter** | needs occupancy + visibility |
| adjacent | 1–2 NPCs | locked / closed | hear | **overhear through the wall** (audio, no sight) | needs occupancy + visibility |
| at the room | 1 NPC | **enterable** (default) | — | **enter → the peek option + a dynamic "X is in the shower" line** (the room is NOT hard-locked; the bath hides, the peek shows — occupancy gates the *activities*, §6.1) | **shipped** |
| at the room | 1 NPC | **sealed** (hard `entry_conditions`) | none | **blocked: dead-end** (`blocked_message` + Go-back, no actions) — reserve for rooms you genuinely can't enter | exists |
| adjacent | 2 NPCs | open / peep | see / peep | **catch two of them together** (config 2) | needs occupancy + co-presence (§5) |
| inside R (solo or with an NPC) | a 2nd/3rd NPC arrives with a sightline | — | see | **you get caught** (configs 3–4) | needs occupancy |

**Reading the table:** the *first three axes pick the situation*; visibility *picks how much gets through*
(see → full scene, peep → partial/charged, hear → audio tease, none → blocked). "Caught" is just the table
read **from the NPC's vantage** — the player is `inside R`, an NPC reaches `adjacent` with a sightline.

Every row must map to a fantasy someone actually wants. A row that doesn't is cut — the model is the minimum
that covers walk-in / peep / locked-peep / overhear / occupied / catch / caught, and no more.

---

## §5 — Engine vs authoring (what each axis costs)

| Axis | Status today | What it needs |
|---|---|---|
| **Access** | **EXISTS** | `entry_conditions` + `blocked_message` (`template_import.py:147-148`, `v2.py:8946-8986`). Reused as-is. |
| **Occupancy** | **SHIPPED (2026-06-17)** | The `npc_at_location` condition type (operator `is_present`/`is_absent`, optional `npc_id`) in `triggerConditionsSatisfied` (`v2.py`). Backs peep / occupied-block / caught. |
| **Visibility** | **AUTHORING — not engine** | Expressed by *which* canvas you write and *where* you place it (the canvas's location is the vantage; see/peep/hear is prose). The engine never needs a "this door is peepable" field. |
| **The scenes** | **AUTHORING** | peep / overhear / blocked / catch / caught canvases, gated on the above once they ship. |

### The engine primitives
1. **Occupancy query — SHIPPED (2026-06-17).** ONE condition type `npc_at_location` with `operator =
   "is_present" | "is_absent"` and optional `npc_id` (omitted = any NPC → room occupied/empty), backed by
   `setup.getNpcLocation` + a new `setup.getNpcsAtLocation` helper, added to `triggerConditionsSatisfied`
   — the single canonical evaluator, so it works in canvas, choice, substitution, AND `entry_conditions`. No
   import-schema change (condition types are permissive). This is the foundation; everything else stands on it.
2. **Visibility — AUTHORING, not engine** (decided during the build). See/peep/hear is the canvas you write
   and where you place it, gated on occupancy. No door/visibility field is built.
3. *(Config 2 only)* **Multi-NPC co-presence — STILL PENDING.** "Two NPCs in R having sex, player observes"
   leans on the separate co-presence gap (the renderer is one-portrait-per-NPC; `npcId`/`requires_npc` are
   single-valued). Referenced here, **not solved here**.

### Build status
**Occupancy — SHIPPED.** It alone unlocks peep, overhear, occupied-block, and caught (configs 1, 3, 4) — all
authorable now. **Visibility — authoring** (no build). **Co-presence (config 2) — pending**, and only if that
case is wanted.

---

## §6 — Authoring patterns (corrected against the live build + RTS, 2026-06-17)

The first draft of this section was wrong in two ways the live build (The Inheritance bathroom) and RTS both
corrected: it put the peek **at a hallway** and **hard-locked** the occupied room. Use what's below instead.

### §6.0 — Two layers + the RTS register split
RTS runs every shared room as **two layers**, and the writing register is split between them:
- **The repeatable layer** — the room hub, the player's shower/self-care, the peek, the "someone caught you"
  interstitial — is **RTS-flat and short** (RTS: shower 116w, caught interstitial 107w, kitchen-eat 34w). These
  fire daily; each is a ~30-word caption with the image/video carrying the body + one specific tell, and the
  player's *read* in **one `thought_bubble`** — **no interior monologue, no aphorisms** (the most common drift,
  `doctrine/05` Rule 5 / §4.3).
- **The capstone it routes into** — the once-per-arc payoff — is where the long, explicit, dialog-dense prose
  lives (RTS: 550–790w), gated `is_repeatable = false` / once-per-arc flag. Tier-3 density is **earned only
  here** (`doctrine/01` P8; `doctrine/05` §3.3).
Never let a daily peek or a max-1/day caught carry capstone-length prose.

### §6.1 — The occupied room stays ENTERABLE; occupancy gates the ACTIVITIES, not the door
A hard `entry_conditions` lock turns an "occupied" room into a **dead-end** — the engine renders only the
`blocked_message` + a Go-back link, **no activities** (live-confirmed). So the peek can't live there. **For a
shared private room you want interactive while occupied (a bathroom): do NOT hard-lock it.** Instead:
1. Keep it enterable (no `entry_conditions`).
2. Make the **description dynamic** — name the occupant when there is one:
```toml
description = "The shared bath, clawfoot tub, a lock that never quite catches.<<set _occ to setup.getNpcsPresentAtLocation('loc_bathroom')>><<if _occ.length>> The water's running — <<print _occ[0].name>>'s in the shower.<</if>>"
```
3. Gate the **activities** by occupancy on each canvas's own `conditions`:
   - the player's **shower/self-care** → `npc_at_location(loc_bathroom, is_absent)` (shows only when empty);
   - the **peek** → `npc_at_location(npc_X, loc_bathroom, is_present)`, and it lives **ON the bathroom canvas**, not a hallway.

`setup.getNpcsPresentAtLocation` is now schedule-based — the SAME source the door/occupancy predicate reads —
so the room's listed occupant, the dynamic description, and every gate name the same person. **Never fake
presence with a flag.** Reserve hard `entry_conditions` for **genuinely SEALED** rooms (a locked office you
earn a key to) where the dead-end IS the intent.

### §6.2 — Peek (player catches a showering NPC) — RTS-flat
A solo-link **on the bathroom canvas**, gated on the NPC present; `max_triggers_per_day = 1`. For several
housemates, the engine shows whichever one is actually in there (each peek gates on its own NPC).
```toml
[[canvases]]
id = "peek_frank_shower"
[canvases.trigger]
location             = "loc_bathroom"
is_repeatable        = true
max_triggers_per_day = 1
conditions = { version = "1.0", items = [
  { type = "npc_at_location", npc_id = "npc_frank", location_id = "loc_bathroom", operator = "is_present" },
] }
```
Base beat ≈ **30 flat words** (the image carries it); the player's read is **one `thought_bubble`**, not woven
into the paragraph. Escalate by stat tier — only the **deepest, once-per-arc tier** earns a dialog line + density.

### §6.3 — Caught (an NPC catches the showering player) — catch-then-react (the RTS shape)
RTS does **not** make the player pre-choose to "leave the door open." The shower is one terse activity; getting
caught is **automatic by chance**, gated on a housemate being **home + into her** (`IsNpcAtHome && arousal>0 &&
corruption>0`) — **never a fixed time-of-day window** — and routes to a **short interstitial** that gives the
agency *as a reaction*: a corruption-gated **flash/show vs cover-up/shut-it** choice. Only the bold branch
routes into the longer payoff.
- **Mechanism:** the caught is a `substitution_only` target on the shower's trigger (rolls on entry), gated on
  a `chance` + the NPC's arc + **"who's home now"** — gate on the NPC's current location being a residence room
  (their schedule puts them home), **not** a clock window, so morning catches the morning-home housemates and
  evening the evening ones, for free.
- **Register:** the interstitial is the short flat beat + the reaction choice; the explicit payoff (the bold
  branch) is the capstone where density lives. `max_triggers_per_day = 1` is the re-fire guard (RTS uses a
  `previous()` guard for the same reason).

### §6.4 — Overhear / co-presence
Overhear = the same occupancy gate, authored audio-only (no image). Two-NPC observe (config 2) still needs the
co-presence engine work — deferred.

---

## §7 — Disciplines & cautions

- **Minimal vocabulary.** Only rows in §4 that map to a real fantasy. If a combination has no scene someone
  wants, it has no behaviour — it is not a feature.
- **Player-always-a-party (§3).** Never author NPC→NPC observation.
- **Access ⊥ Visibility (§2).** Don't fuse them; a locked door can still leak sight or sound.
- **Don't author ahead of the engine.** No peep / occupancy / overhear content ships until the primitives in
  §5 land — same rule as `doctrine/04` §10.5. The walk-in-on-you row (and only that row) is buildable today.
- **It's above RTS.** Size the build to the fantasies actually wanted; occupancy is the one primitive that
  earns its keep first.

---

## Cross-references
- `doctrine/10` §5.4 (locked-location unlock contract) + §5.5 (the three location categories) — the **Access**
  axis; this model adds **Visibility** beside it.
- `doctrine/02` §4.8 (loose vs strict presence; the engine has only strict co-location) — why **Occupancy** is
  absent today.
- `doctrine/04` §10.5 (the daily loop is a content host) — the engine-follow-up note that names the occupancy
  primitive this spec formalizes.
- `redesign_phase_3/22` (the machine) — cross-NPC flag wiring, for the "caught" configs' downstream effects.
- The **multi-NPC co-presence** gap (cohabitation audit) — the dependency for config 2 only.

## Self-check (for any game authored to this model once §5 ships)
- Every peep / overhear / occupied / catch canvas gates on the **occupancy** predicate (`npc_at_location`,
  `is_present`/`is_absent`), never on a flag faking presence.
- Every visibility scene matches its door's `visibility` value (no "see" content behind a `hear`-only wall).
- The player is a party in **every** shared-space scene (§3); no NPC→NPC observation exists.
- Locked rooms that are meant to leak carry a visibility value; locked rooms that are sealed carry `none`
  (and the try-enter prints a `blocked_message`, not silence).
- No peep/occupancy content shipped while the §5 primitives are still unbuilt.
