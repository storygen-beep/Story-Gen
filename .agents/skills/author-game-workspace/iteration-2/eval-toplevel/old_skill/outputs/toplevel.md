# Step 2 — Top-level design: *The Hale Hotel* (working title)

> **Seed (locked, not re-opened):** A broke live-in nurse takes a private post at a decaying seaside hotel
> owned by a dying man and his three grown children. She nurses him by day and, as the family fights over the
> will, works each of them until the place answers to her.
> **Person:** second. **Systems on:** clothing, phone. **Rent:** off.
> **Cast:** Mr. Hale (dying owner) · Iris (sharp elder daughter) · Tobin (weak son, runs the bar) ·
> Dr. Vance (visiting doctor who signs things).
> **Map:** the hotel (lobby, bar, Hale's room, the nurse's room, the closed east wing), the pier, the town.

This is the rulebook: how you grow, and how that growth makes the hotel answer to you. Plain words only — no
TOML yet.

---

## 1. The cascade (the spine) + the stat set

### Which model — and why NOT the still point
This is the **default climbing cascade**, not the still-point/owned-weapon variant. You arrive **broke and
proper** — a professional caregiver who has never crossed a line — and the game is you *crossing it*. You are
the erotic subject who **falls and rises**, not a pre-maxed honeypot who watches. That matches the second-person
register we locked (the still point pairs with third person and cools the porn — we are not paying that cost
here). So player `corruption` is a **live, climbing axis**, and the double lock runs in full.

### The double lock
Every **lewd** beat with a family member needs **both**:
1. **Your corruption ≥ the tier for that KIND of act** — the *door*. "Am I willing to do this?" One door for
   the whole house; you build it by crossing your own lines (below).
2. **That person's own trait ≥ the rung's threshold** — the *individual lock*. "Is *he/she* far enough?" You
   build each person's lock by working **them**.

**Nursing, talking, softening, doing favors, gathering leverage — none of it is corruption-gated.** That is how
you raise each person's lock in Act 1 while, in parallel, you corrupt yourself. The two converge: by the time
your corruption opens the door, the people you invested in are already unlocked.

### What raises YOUR corruption (self-corruption feeders — each a want, never grind)
Every feeder is you pursuing something you *want*, not "farming a bar":
- The first time you **work Tobin** instead of just serving his drink.
- The first **revealing outfit** worn down in the bar / out on the pier (the reactive world, §4).
- **Skimming the till**, palming a guest's cash, the first small theft.
- Every **leverage play** — reading the east-wing records, holding a secret over a child.
Each crosses a caregiver's line, so each is honestly self-corrupting.

### The stat set — three legs, each with one job (no dead stats)
- **corruption** *(built-in)* — the lewd door; the cascade. Gates the explicit rungs across the whole cast.
- **money** *(built-in)* — you are broke. The wage barely covers you; the good money is always further down the
  lewd path (§5). Gates: revealing clothing, gifts that soften a child, bribes that keep Dr. Vance. This is the
  pressure that pulls you down.
- **energy** *(built-in)* — paces the day: nurse by day, work them by night. Spent via `costs` on moves/
  activities, restored by sleep in the nurse's room.

**No exhibitionism leg.** This is a chamber piece about four named people, not a flash-for-tips economy; the
public bar/pier/town reactivity keys on the clothing value (`worn_corruption`), which needs no exhibitionism
trait. **No `beauty` leg** — beauty is derived read-only from worn clothing (`worn_beauty`); the wardrobe drives
it.

**No "control/standing" core meter — on purpose.** "The place answers to you" is genuinely the point, but a
control meter would gate *nothing* in Act 1 (you have no control yet) and only pay off late — a dead stat now.
So "the place answers to you" is modeled as **milestone flags** (`bar_taken`, `wing_open`, `vance_signed`,
`iris_folded`) and per-NPC `<npc>_stage` traits (the machine, §7), telegraphed on the Story-Goals card. It reads
as one rising "standing" to the player without a fake meter.

### Hard vs soft gates (match the fiction)
- **Hale's decline / the will** → **hard**: a real clock (§9 fail-state) that can foreclose the top rung.
- **The east wing** → **hard**: locked location, `entry_conditions` + `blocked_message` ("the family keeps it
  shut"), unlocked by a milestone.
- **A neglected child** → **soft**: Tobin/Iris/Vance are always *there*; ignore one and that thread turns colder
  and more transactional, never gone.
- **The reactive world** → **soft**, keyed on your outfit: covered = ignored, exposed = liberties taken.

---

## 2. The desire ladder (the cascade felt as named wants)

Second person, one current want always shown. Each rung: a concrete want → what clearing it unlocks.

1. **"Keep this post."** Nurse Hale through the first day, don't get dismissed, take your first small wage.
   *Unlocks:* the run of the house, and the money loop. *(Teaches nursing, money, energy, the phone.)*
2. **"Make the son yours."** Work Tobin behind the bar; he's weak and drunk and easy. *Unlocks:* bar income +
   the skim — your first real money, and a base that's yours.
3. **"Buy the dress that turns heads."** Afford the first revealing outfit off the phone catalog. *Unlocks:* the
   reactive world (bar, pier, town) and a self-corruption feeder.
4. **"Get into the east wing."** Find what the family shut away — the old will, the ledgers, the dirt.
   *Unlocks:* leverage plays as a currency.
5. **"Turn the doctor."** Work Dr. Vance until he'll sign what *you* want, not what Iris wants. *(Cross-gated on
   standing — you need the house behind you first, §7.)*
6. **"Break Iris."** The hard conquest: isolate the elder daughter and fold her. *(Cross-gated on Tobin taken +
   leverage in hand, §7.)*
7. **"The will names you."** Hale signs the estate to you; the place answers to you. *The frontier payoff (§6).*

The ladder is **open-topped** — rung 7 is the current edge of authored content, not a wall. This becomes the
Story-Goals column of the Quests page (laid out at Step 5).

---

## 3. The reactive world (clothing-driven)

The world reacts to **what you're wearing**, not to a hidden number. You control an exposure level; each place
reads it and takes liberties scaled to it — always **lewder/bolder/more predatory**, never warmer.

- **Nurse's uniform (covered)** → ignored everywhere. This is your day armor.
- **The bar (Tobin's, decaying, semi-lawless)** → exposed = stares, gropes-in-passing from patrons; the more the
  place has slid, the bolder they get.
- **The pier at night (drunks, fishermen, no eyes on you)** → the **highest** ceiling; exposed here escalates to
  cornered/taken. This is where **forced** mode lives early.
- **The town (civilized public)** → caps at stares and comments, whatever you wear.
- **Hale's room (private, his frailty)** → tender/taboo ceiling, capped by who he is.

**Three modes:** *sought* (you dressed for it) · *choice* (refuse-or-accept) · **forced** (no branch). **Forced
is act-scoped** — early you are prey (broke, powerless): a pier or back-bar cornering can be forced. As your
power rises it **recedes** — you become the predator. Gate forced on the **power tier**, not on outfit×place
alone.

**Engine truth:** these are **Lane 2 / Lane 3** canvases gated on **`worn_corruption`** (never on player
corruption/exhibitionism) — exactly the PUBLIC content clothing is allowed to gate; **never** a named NPC's arc
spine. The **forced** event = an **auto-fire capstone-shape canvas** (`priority ≥ 9`, single Continue, no
refuse/accept — there is no zero-choice engine primitive). The **per-place ceiling is author-encoded in each
canvas's `conditions`**, not a location attribute. Progression comes from **buying** revealing clothing, not a
trait.

The four named cast each read your outfit *in character* (dispositions set at Step 3): Iris banks it as leverage
(cold), Tobin flusters (weak), Vance is transactional, Hale is tender.

---

## 4. The economy (a corruption ladder — no rent)

**Rent is off** by seed. The pressure engine is not a rent clock but **Hale's decline + the will** (§9): the
prize and the deadline are the same object. Money is still tight from day one and the wage is thin, so the pull
downward is constant.

- **One wallet.** Money is money — no clean/dirty split.
- **Income is a corruption ladder:**
  - *Legit-low:* the nursing **wage** (a small stipend against the estate). Barely covers you.
  - *Lewd-mid:* the **bar** with Tobin — tips while exposed, then **skimming the till** once he's yours.
    Softening a child for gifts/cash.
  - *Lewd-high:* **leverage payouts** — Iris paying to keep you quiet, Vance's kickback for a favorable
    signature, dictating the accounts once the place answers to you.
- **Multiple paths (anti-grind):** bar closed / Tobin sulking → gather leverage in the wing → hit Iris for a hush
  payment → run the pier. Blocked on one, do another.
- **Earning = content.** Every paying activity is a lewd or reactive-world or leverage scene — never a
  chore-click that only adds a number.
- **Sinks (wanted buys, pressure via desire):** revealing clothing (the reactive-world dial, phone catalog) ·
  gifts to soften each child · **bribes to keep Dr. Vance signing your way**.
- **Pressure escalates across acts:** survival-broke early → the **estate contest** late (Iris counter-buys
  Vance; you must out-bid/out-leverage her to hold the will). The form escalates; the presence of pressure is
  constant.

Engine reuse: one `money` trait + Lane-3 work hosts (the bar, the pier) + the clothing shop as a sink. **No rent
system** (off by seed).

---

## 5. Legibility + pacing

- **Legibility rides the quest cards we already have.** The Story-Goals card always shows the **current want**
  and **the next concrete action naming PLACE + TIME-WINDOW + REQUIREMENT verbatim** — e.g. *"Make the son yours
  — work the bar while he's drinking, the bar, evenings"*, not "win over Tobin." Each NPC's `next` block
  (`npc_panel`) does the same. Telegraph the next rung (locked-visible). One current want, never stale.
- **Cross-gated rungs name the OTHER arc's state** (the machine, §7 D3): *"Vance won't sign while Iris still
  holds the accounts"*, *"Iris won't fold while the bar's still hers to lean on."* A silent cross-lock is a
  soft-lock — forbidden.
- **Pacing = tension → release, escalating, then plateau.** Every want ends in a payoff; payoffs escalate up the
  ladder (first kiss with Tobin → the bar is yours → the wing opens → Vance signs → Iris folds → the will names
  you), then flatten into a **wide livable plateau** at the frontier. Alternate big and small beats; always keep
  a near payoff visible; don't dump the big content early.
- **The endgame escalates in CONTENT, not management.** "The place answers to you" cashes out as the **hottest,
  most-owned** repeatable scenes with all four — never a dashboard, never a +income widget.

---

## 6. The frontier (endless sandbox, not a finish line)

- **Local arc endings — kept.** Fully folding Iris, or Hale signing the will, ends a *thread*, not the game.
- **Hard game-ending — dropped.** No win-screen.
- **The frontier — designed.** Rung 7 ("the will names you / the place answers to you") does three jobs:
  1. **Payoff at the ceiling:** the hotel is yours; all four are in your pocket; the owned-repeatable scenes are
     the hottest in the game.
  2. **Livable steady-state:** the repeatable loops with each conquered person + the reactive world + the bar/
     leverage income all stay playable.
  3. **Greyed next-hook seed:** *"A buyer from the mainland has heard the Hale hotel changed hands."* — the
     clip-point a later extension bolts onto.
- **Endless ≠ aimless:** at the frontier the tracker says so honestly — *"You own the Hale. Run it. More
  coming."* — never a blank screen.

---

## 7. The machine (cross-wiring — the depth spine)

One machine, not four arcs sharing a wallet.

### The core loop
**Nurse Hale (day) → trust + the run of the house → work each child + Vance (seduction/leverage) → each
conquest yields money + access + a leverage flag → leverage compounds (bar money funds the gifts that turn the
others; the turned doctor signs the will) → the will names you / the place answers to you → run the hotel.**

Every core person has a **place** in the loop (Step 3 casts them onto it):
- **Hale** — the **keystone**. Nursing him is the loop's entry and his dependence is the will. His lock is
  `relation` (trust/dependence); his arc is tender/taboo caregiver intimacy, and his payoff is the signature.
- **Tobin** — the **income node** and the **first conquest** (easiest, drink-softened). Lock: `relation` +
  `arousal`. Taking him sets **`bar_taken`**.
- **Dr. Vance** — the **legal lever**: he signs the will / the certificate. Lock: `relation` + a leverage flag.
  Turning him sets **`vance_signed`**.
- **Iris** — the **hardest conquest** and the rival for control. Lock: her own `corruption` (breaking the proper
  controller). Folding her sets **`iris_folded`**.

### The wires (form 1 + form 2)
- **F1 — arc→arc depth gates** (milestone → **player flag**; "how far" → **`<npc>_stage` player trait**):
  - **Vance's late rung** (signs *your* way) gated on **standing** — a `house_runs` player flag set once
    `bar_taken` **and** Hale's dependence milestone hold. *(Telegraph: "He won't cross Iris for a nurse with no
    standing.")*
  - **Iris's late rung** (she folds) gated on **`bar_taken`** (once the son is yours she's isolated) **and**
    **`wing_open`** (leverage in hand). *(Telegraph: "Iris won't fold while the bar's still hers to lean on.")*
  - **Hale's will-naming** (rung 7) gated on **`vance_signed`** and **`iris_folded`**.
  - All player-namespace flags/traits — **no raw cross-NPC trait reads**; each source arc mirrors its milestone
    to the player namespace.
- **F2 — arc↔economy circulation:**
  - **(2a, load-bearing)** Tobin's **bar income** is the gate to reach the others — bar money buys the clothing
    and gifts that turn Iris and Vance. The economy is the connective tissue.
  - **(2b, flourish)** **Iris's hush payout banded by her `corruption`/`relation`** — band-gated sibling choices
    (one per band, each its own `conditions` + literal-int money `effects`), authored at Step 5/7.

### The three disciplines (firewalls)
- **D1 — no arc's ENTRY is cross-gated.** Tobin, Iris, Vance, and Hale each have an open, cold-start on-ramp;
  cross-gates sit only on **mid/late** rungs.
- **D2 — no cycles.** The F1 wires form a DAG: `Hale-dependence + bar_taken → house_runs → vance_signed`;
  `bar_taken + wing_open → iris_folded`; `vance_signed + iris_folded → will_named`. No back-edge. (Checked at the
  feedback review.)
- **D3 — every cross-gate is a locked-visible telegraph naming the other arc's state** (the §5 lines above).

No new ledger field — the machine lives in `design_book.md`'s `## The machine` section (finalized at Step 5) and
is enforced by ordinary beat `deps` + `cross_npc`/`economic` beat types. One NPC at a time still holds: an unset
flag is a locked rung, and that is correct.

---

## 8. The §8 declarations (opening · systems · fail-state)

### The opening / cold start
- **First screen:** you step into the lobby of a hotel that's sliding into the sea — suitcase in hand, last
  cash in your pocket. The family is mid-fight over a dying man: Iris meets you cold at the desk, Tobin is
  already drunk at the bar, Hale is failing upstairs.
- **2–3 things you can do immediately:** (1) **go up and nurse Hale** — the job, teaches the nursing loop + the
  wage; (2) **go to the bar and meet Tobin** — the easy on-ramp, the nudge downward; (3) **check your phone** —
  teaches the phone: a clothing catalog and a first text.
- **First named want:** *"Keep this post."*
- **Teaches with no tutorial:** the sidebar lights **money near-zero** and **energy full**; the nursing loop
  pays the first wage; the **east wing shows locked** with its reason on the card ("the family keeps it shut" —
  the why-locked surfaces); you're shown in the uniform (clothing live at value zero).
- **10-minute taste:** a new player comes away knowing this is a **seduce-and-conquer-the-family-for-the-estate**
  game — you will work four people until the place is yours — not merely "nurse a sick man."
- **Customization / speak-back:** the PC is a broke live-in nurse (female). If her name is customizable, it flows
  through dialogue as `@player` (never baked into labels) and the game speaks it back. *(Confirm the exact
  customization surface at Step 3/onboarding.)*

### The systems in play
- **ON — clothing:** wardrobe (uniform vs revealing); `worn_corruption` drives the reactive world (§3);
  `worn_beauty` drives beauty (no beauty leg).
- **ON — phone:** the clothing catalog (a shop thread + sink), Dr. Vance's visit/appointment thread, and the
  family will-fight surfacing as async messages/updates.
- **OFF — rent** (by seed; the will/decline clock is the pressure engine instead).
- **OFF for now — customization beyond a name, and the player portrait.** Named out so nothing is half-wired.
- *Authored subsystems left to EMERGE through play* (not forced at the seed): a **leverage/dirt track** (the
  east-wing records as a second currency) is the likeliest to grow in — we'll fold it via the run-mode "systems
  grow through iteration" loop if play asks for it, rather than committing its full shape now.

### The fail-state
**Failure exists — on purpose — but there is no hard game-over** (§6):
- **Hale's decline is a real clock.** Neglect him for too long and he worsens; Dr. Vance flags the neglect and
  your **standing/post is threatened** — a real closing-off, not a game-over.
- **The will can be signed AWAY.** If you don't reach standing before the contest milestone, **Iris gets Vance to
  sign the estate to the children** — this **forecloses** rung 7 as a clean win and forces the harder
  leverage/break-Iris path to claw it back. This clock is built to **actually bite** (it cools a thread and
  raises the price), unlike an advertised-but-toothless deadline.
- **Neglecting a child** cools that thread (soft): colder, more transactional, never gone.

Forward stays possible throughout, but the price rises when you let a clock run — a chosen negative axis, not a
forward-only ratchet by default.

---

## Advance
When this section is written into `design_book.md`, set `pipeline_phase = "map_design"` — Step 2b lays out the
hotel's spatial graph (lobby / bar / Hale's room / nurse's room / closed east wing / pier / town, with the
locked wing, travel friction on the bridges, and per-location dramatic jobs) before Step 3 casts Hale, Iris,
Tobin, and Vance onto it.
