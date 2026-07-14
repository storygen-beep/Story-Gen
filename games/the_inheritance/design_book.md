# The Inheritance — Design Book

> The user's review surface. This is **intent in plain language** — the engine/TOML is the faithful
> translation of what's written here. Grown one section per pipeline step.

> **Book revision 1** — the seed (Steps 0+1), 2026-07-14.
>
> **This is a re-author.** The v1 game is archived at `archive/the_inheritance_v1/` (book revision 72). Its
> premise, cast, map, machine and economy were **good** — the skill's own `location-design.md` cites its map
> by name as the canonical nested-zones example. What failed was everything from the **blueprint down**:
> 47% of canvases were one-shots, the whole game had **7 Lane-2 ambients** (Audrey, the densest arc, had
> zero), 8 Lane-3 walk-ins were re-registered 41× to look bigger, NPCs were scheduled into rooms with no
> canvases, and 88 of 102 nodes had no choice at all. A corridor of milestones.
>
> So: **Steps 0–4 borrow from v1 as raw material, re-run through every gate. Step 5 (blueprint) onward is
> generated fresh.** Importing v1's blueprint would import the corridor.

---

## World setup

**POV.** Female PC. Cascade-native: the player corrupts herself and her own resolve before she corrupts the
household. The estranged daughter is a vessel the player fills.

**Register — PERSON: `second`.** Locked at the seed, **immutable** (a change is a full-corpus rewrite).
Every `paragraph` and `thought_bubble` is "you"; `dialog` blocks are exempt. This is what Road to Success
does, what the skill's every rule and example is written in, and what v1 already wrote well:

> *"You draw the curtain and lie down in the room you grew up in. The hotel's quiet. Tomorrow there's the
> floor to work and the family to handle. You go under."*

Mirrored into the TOML as `[settings] narration_person = "second"` at authoring. (Person is the first of the
three register axes — `.claude/skills/author-game/references/rts-flat-prose.md` Rule 1. Not to be confused
with POV, which in this skill means the protagonist's *gender*.)

**The fantasy (clears the 3-part bar).**
> You left years ago, estranged and written off. A death drags you home to the family hotel for the reading
> of the will — and you intend to take it *all*: the estate, the dying hotel, and **every person under its
> roof**, one by one, until the family that underestimated you answers to you.

- **POV-fit** ✓ — a female-PC takeover-from-within; the closed family is hers to corrupt from the inside.
- **Sharp charge** ✓ — *power-reversal + taboo*. The overlooked, estranged daughter returns and methodically
  takes the family apart and remakes it around herself. Incest is the taboo charge; **conquest**
  (break-and-own) is the heat. Cold and deliberate — never romantic longing.
- **Built-in two-act shape** ✓ — **Act 1:** come home underestimated, read the players, find each one's
  weakness, take the failing hotel in hand as leverage. **Act 2:** pick them off — seduce, indebt, break —
  until the household and the estate are yours to own and arrange.

**Desire span (declared, not stumbled into) — MIXED, total-household conquest.**
Every adult under the roof is a target. The span carries **three distinct registers**, chosen deliberately
so the player is never ambushed by a tone they didn't sign up for:
1. **Cold sapphic conquest** — the women (Audrey, Margaret). The spine of the game.
2. **Humiliation / domination** — the arrogant parasite brother (Grayson). *Bring the prick to heel.*
3. **Widower seduction** — the grieving stepfather (Richard). Slow, dark; consoling-into-owning the broken
   man, becoming the new woman of the house. The heaviest tonal outlier — handle with care.

**Premise.** The matriarch — your mother **Eleanor**, who built the family's boutique hotel — has died. Her
will pulls you, the estranged eldest daughter, back to the building you walked out of years ago. Your
stepfather is too sunk in grief to run the hotel or keep the household afloat; your brother is a useless
parasite; the will is contested; and the family who expected to inherit everything is standing exactly where
you intend to stand.

**Why she left.** The break was with **Eleanor**. When Richard and the younger children became "the family,"
Eleanor chose them — she let Catherine, the firstborn from before, be written out of the hotel's future, and
never lifted a hand when Catherine walked out. **Eleanor's death is the trigger precisely because it
forecloses any reckoning:** the one person who could have made it right is gone. So Catherine returns not to
grieve and not to reconcile, but to take what she was written out of. The wound fuels the conquest; it never
softens it.

**Blood ties.** Audrey and Grayson are Catherine's **blood half-siblings** — all three share the dead mother
Eleanor, but the two younger ones are Eleanor + Richard's (Catherine is from Eleanor's earlier
relationship). **Margaret** is blood aunt (Eleanor's sister). **Richard** is the stepfather — Eleanor's
widower and father to the two younger siblings, **no blood relation to Catherine**.

**Player.** **Customizable** — the player sets her name (default **Catherine**) and her look at the opening.
The returning daughter is a role the player inhabits.

**Systems in use (scope only — wiring decided at authoring):**
- **Clothing** — YES. Wardrobe/closet; the worn outfit gates public reactions and exhibitionism. The
  reactive world (Step 2) rides on this.
- **Phone** — YES. Chat threads with the household; photos; leverage that lives on a screen.
- **Player portrait** — YES. A state-reactive sidebar image of her that swaps on undress / outfit /
  corruption **level**. For a game whose spine is *watch yourself become someone else*, this is the
  strongest feedback surface the engine has. (New since v1 — shipped 2026-07-06. Cost: ~15–30 consistent
  images, sourced at authoring.)
- **Money / economy** — YES, but **a CONTROL economy, never survival rent.** The boutique hotel is failing
  and Richard can't cover the staff or Audrey's tuition. If the player takes the hotel in hand, *saving it*
  becomes both her income and her leverage — paying a sister's fees or covering Richard's debts is a
  corruption hook, not charity. (Exact stat/loop is Step 2's job. Flagged here as: money matters, but as
  **control and dependence**, never as scraping rent.)

---

## Cast (names + roles only — Step 3 reshapes this into the cascade)

Naming set: **classic / old-money.** Deceased matriarch: **Eleanor** (the mother who built the hotel; never
on screen, drives everything). Player default name: **Catherine** (editable).

*Cold sapphic conquest (the spine):*
- **Audrey** — half-sister, in college, fees unpaid. The most vulnerable of the household; the way in.
- **Margaret** — the aunt (Eleanor's sister). Moved into the hotel to "help," and is angling to seize the
  hotel and the will. The apex female power in the house; the climactic conquest.

*Other registers:*
- **Grayson** — half-brother. A useless, hostile parasite and rival claimant who expects to coast into the
  inheritance. Register = **humiliation / domination**.
- **Richard** — the stepfather. Eleanor's widower, sunk in grief; nominally heads the household and the
  hotel he can no longer run. Register = **widower seduction** (console-into-own; slow, dark). Also the
  legal gatekeeper — the will, and the hotel's fate.

*Not a target:*
- **Lorna** — runs the hotel bar. The one straight dealer in the building; the ally and the on-ramp into how
  this world actually works.

> Step 3 (casting) derives the exact tiers and ordering the cascade needs, and may add or merge minor cast
> (hotel staff, the bank, a guest). Listed here as *people* — no arc shapes, voices, or stats yet.
>
> **Two holes v1 left that casting must close:** the money pressure had **no face** (its banker was three
> one-shot scenes and an empty room), and **Lorna died after four beats** despite being the mentor the whole
> corruption track hangs on.

---

## Locations (the map — ONE BUILDING)

It's **one building — the hotel** — not an estate with a hotel attached. Eleanor built the boutique hotel and
**raised the family in the residence above it**, so the player grew up here and the whole campaign plays out
inside (and just outside) this single building. The decline is literal: old money so broke the family lives
upstairs in the hotel it can barely keep.

- **The Hotel — Lobby (the root / arrival)** — where the player walks in. The public floor she works and
  remakes; the control-economy surface; a public stage for clothing/exhibitionism content.
  - **Bar · Guest Rooms** — the rest of the public floor (Lorna's bar; the let rooms, where a comped "favor"
    has somewhere to happen).
  - **🔒 Back Office** — the books, the money. Unlocks when she takes the hotel's purse in hand. Controlling
    it means controlling the roof everyone sleeps under.
  - **🔒 Private Floor** — the vice-house apex, the top of the building. Opened late; the dirtiest money and
    the best.
- **The Residence (the family floor, up the stairs behind the desk)** — where the family lives. The
  **bedrooms** (Audrey's, Margaret's, Richard's, Grayson's, and the player's old room) are the private
  interaction spaces; the **common rooms** (the drawing room where Margaret holds court, the study, the
  kitchen, the upstairs bath, the terrace) are the shared household space where presence and ambient
  reactions happen.
- **Town (out the front doors)** — the bank and the lawyer (the will), the boutique (clothes), a discreet
  adult shop (the tools), the college (offscreen).

> Shape: `hotel` (root) → bar · guest rooms · **residence** (→ bedrooms + common rooms) · back office 🔒 ·
> private floor 🔒 · town (→ bank · boutique · adult shop).
>
> Step 2b (map design) re-derives **each room's dramatic job and access** — that is where v1 failed, not
> here: it shipped **five dead rooms** and one permanently locked on a flag nothing ever set. The topology
> is sound and is borrowed near-verbatim; the per-room job is generated fresh.

---

## Top-level design — the engine, economy & machine (Step 2)

> Plain-words rulebook for how she grows and how that growth unlocks the household. No TOML yet.
>
> **Core loop:** work the floor → money → take the hotel in hand → the vice-house grows → its money and
> access buy leverage over the family → corrupt them → the family becomes part of the business → take the
> will → become the one the household answers to.

### 1. The cascade + the double lock

**You must corrupt YOURSELF before you can corrupt anyone else.** Your own corruption is the master key;
every *lewd* beat with the family stays locked until you've fallen far enough on your own hotel floor.

- **Self-corruption first (Act 1).** You fall *publicly*, working the failing hotel — hostessing in bolder
  clothes, weathering and then *enjoying* what guests try, crossing the first transactional line. That
  raises **corruption** (the door) and **exhibitionism** (the public register) *while it earns money*.
- **Befriending the family is NOT gated.** Talking, managing the hotel together, working old wounds — all
  ungated, all Act 1, raising each person's own lock in parallel.
- **The double lock on every family lewd rung** — BOTH must be true:
  1. **Your corruption ≥ the tier for that KIND of act.** The *door*. Opens for the whole household at once;
     built by your own feeders.
  2. **That person's own trait ≥ their threshold for that rung.** The *individual lock*. Built by working on
     them.

  They converge: by the time your corruption opens the door, the people you invested in are already unlocked.

### 2. The stat set (each leg gates real content — no dead stats)

| Stat | Kind | The content it gates |
|---|---|---|
| **corruption** | built-in | The lewd door — every family lewd rung's floor, and your own willingness on the floor. The cascade spine. |
| **money** | built-in | The leverage fund. Bolder clothes, hotel upgrades, and the family hooks (Audrey's fees, Richard's debts). |
| **energy** | built-in | Paces the day. Spent via `costs`, restored by sleep. |
| **exhibitionism** | built-in | How far the *public* content goes — the floor-work rungs and the hotel's public beats. |

- **`exhibitionism` vs the clothing's `worn_corruption` — NOT the same axis, and v1 never wrote this down.**
  **The outfit is a dial you can turn back; exhibitionism is a ratchet that only climbs.** What you're
  *wearing right now* (`worn_corruption`) decides how the room treats you *this minute* — take the dress
  off and the room goes quiet again. **Exhibitionism** is how far you're *willing* to go in public, it never
  falls, and it's what the floor-work rungs gate on. Two axes. Without this written down, exhibitionism
  reads as a duplicate and someone eventually cuts it.
- **No `renown` meter.** The hotel's turn from boutique to vice-house is **not** a bar. Which clientele and
  services exist is gated on money-bought upgrades + story flags + your corruption floor. Fewer dials, and
  the house grows out of the conquests that matter instead of a grind. *(v1 got this right and killed the
  meter at its own Step 5 — kept.)*
- **No `beauty` leg** (derived read-only from worn clothing). **No `fitness` / `intelligence` / `charisma`** —
  no domain needs them; the family arcs run on each person's own `relation` / `corruption`.

**Hard vs soft gates.** The private floor and its clientele = **hard** (they don't exist until the upgrades
and Richard's signed-over control open them). A family member's *presence* = **soft** — they live here; they
are always reachable from a cold start. Only the lewd rungs gate.

### 3. The desire ladder (the chain of named wants — the player-facing spine)

Backstage it's meters; onstage it's wants. Each rung = a concrete want + what clearing it opens.

- **Act 1 — Fall + Build**
  - *"Get your hands on this place."* → take floor shifts → first tips, first bolder outfit.
  - *"Make the hotel breathe again."* → comp a room for a "favor" → the first transactional line crossed.
  - *(parallel, ungated)* *"Get back inside this family."* → re-meet Audrey, Grayson, Richard, Margaret →
    find each one's weak point.
- **Act 2 — Reach**
  - *"Open the private floor."* (needs hotel control + the upgrade) → the vice-house emerges.
  - As corruption crosses tiers the family rungs *appear* (double lock). Per-person wants: **own Audrey**
    (the way in) → **bring Grayson to heel** → **console-and-own Richard** → **topple Margaret** (apex).
- **Act 3 — Deepen**
  - *"Make the family part of the business."* → each of them inducted; their hot capstones.
  - *"Take the will."* → the apex conquest of Margaret; the house is yours.
- **Frontier (open-topped)** → below, §7.

### 4. Pressure — a RACE, not a threat (the fail-state consequence)

**There is no fail-state (§8). So pressure cannot come from anything being taken — it comes from wanting.**

- **The decline is the OPPORTUNITY, not the countdown.** Richard can't run the hotel. That is not a clock —
  it is **a lever lying on the floor**, and you are the only one who will pick it up. v1 advertised a
  foreclosure that could never actually land; that threat is **cut**, not softened. The bank and the lawyer
  stay in the world as the *machinery of the will*, never as a doom timer.
- **You corrupt yourself for money because money buys LEVERAGE, and leverage buys PEOPLE.** The want was
  never "don't lose the hotel." It's *own them*. This is why the economy is a control economy and never
  survival rent — it was in the seed, and now the whole design agrees with it.
- **Margaret is a RACE you are currently losing — visibly.** She cannot take anything from you. But she is
  holding court in your mother's drawing room, the staff answer to her, and Grayson smirks behind her. You
  can't lose the race; you also can't win it until you break the men her power stands on. **The negative
  axis is STATUS, not confiscation** — a standing humiliation you want to erase. That's desire-pressure, and
  it's the right shape for a cold-conquest register.
- **Pressure escalates by raising the PRIZE, not the danger.** Act 1: the hotel is a lever. Act 2: Margaret
  and Grayson move on the will — the prize is now contested. Act 3: the house itself is the prize, and what
  it can *become*. What escalates is what you can win, never what you can lose.

### 5. The reactive world (clothing-driven)

The world reacts to **what you're WEARING** (`worn_corruption`), never to a hidden number — and the shift is
always *bolder / lewder*, never warmer.

- **Place ceilings (author-encoded per canvas):** the lobby and bar = civilized-public early (stares,
  comments, a hand in passing). The **private floor** = lawless (open liberties). The **residence** (family
  bedrooms + common rooms) = milder but charged — it's home, and that's what makes it worse.
- **Predatory dispositions:** certain guests escalate. **Grayson** takes liberties early — he's entitled and
  hostile and he doesn't think you'll do anything. Respectful staff just go flustered. **Margaret** takes
  what she sees and *banks it as leverage*.
- **Three modes:** *sought* (you dressed for it) · *choice* (refuse or accept) · **forced** (no branch — an
  auto-fire capstone-shape canvas; there is no zero-choice engine primitive).
- **FORCED is ACT-SCOPED, prey-early — and it is the floor of the whole reversal.** While you are
  underestimated and powerless (Act 1), a guest or Grayson can take a liberty **you cannot refuse**. It
  **recedes as you rise.** Things stop happening *to* you and start happening *because of* you. This is the
  best idea in v1's design and it is kept whole: the prey→predator reversal is the game, and the forced
  mode is what makes the "predator" half mean anything.
- Progression comes from **access to bolder clothing** (bought / unlocked), never from a trait.

### 6. The economy (a corruption ladder, anti-grind)

- **One wallet.** Money is money.
- **Income IS the corruption ladder:** legit hostessing (scraps) → flirty / comped "favors" → escort
  arrangements → private-floor cuts (the real money). **The better money is always further down the lewd
  path.** Making money and corrupting yourself are the same act.
- **Earning = content.** Every paying activity is a floor / reactive / escort scene. Never a chore-click
  that just adds cash.
- **Multiple paths (anti-grind):** blocked on one → do another. Floor work · comped favors · private-floor
  services · selling photos through the phone.
- **Sinks are WANTED buys** (this is what keeps pressure alive with no fail-state): bolder clothing (the
  reactive dial) · hotel upgrades (transform a room → unlock a new KIND of service) · **the family hooks**
  (Audrey's tuition, Richard's debts — paying is a corruption hook, never charity) · the legal costs of the
  will.

### 7. Pacing & the frontier

- **Pacing:** climb → plateau → climb. Every want ends in a payoff; alternate big and small beats; never
  dump the big content early. **The endgame escalates in CONTENT, never into management** — each family
  member's induction into the business is a *hot capstone*; the apex is the *hottest* beats. Never a
  +income dashboard.
- **The frontier (open-topped, no win-screen).** The top authored rung does three jobs:
  1. **Land the charge-ceiling payoff** — the household owned and serving; the will yours.
  2. **Drop into a livable steady-state** — run the house: the repeatable family loops, the private-floor
     income, and the reactive world all stay playable.
  3. **Leave a greyed next-hook seed** — *"a society rival across the city has heard what your house has
     become."*
- **Local arc endings are KEPT** (fully owning one person ends a *thread*). There is **no hard game-ending**.
  At the frontier the tracker says so honestly — *"you've reached the current peak; run your house"* — never
  a blank screen.

### 8. The declarations (opening · systems · fail-state · body-state)

**The opening / cold start.** You walk into the lobby of the hotel you grew up in, on the day of the will
reading, and the first thing you see is **Margaret standing behind the front desk giving orders to your
mother's staff.** That is the whole game in one frame: the house is being taken, and not by you. Three
things you can do immediately — **talk to Lorna at the bar** (who tells you how bad it really is, and is the
first person glad you're back), **go up to the family floor** (meet who's left), and **take a shift on the
floor** (the first money, the first bolder outfit, the first rung). The first named want is
***"Get your hands on this place."*** The customizable name and look are set here, and the world speaks it
back (`@player`) from the first scene. No tutorial — the hotel teaches you by needing you.

**Systems in play** — declared in and out, so nothing is half-wired:
- **ON:** clothing (wardrobe; the reactive-world dial) · phone (household chat, photos, leverage on a
  screen) · player portrait (state-reactive sidebar image: undress × outfit × corruption level) ·
  customization (name + look).
- **OFF:** the rent system. There is no rent and no survival clock — the economy is control, not survival
  (§4). *(Turning `[settings.rent]` on would smuggle the cut fail-state back in through the engine.)*
- Finer **authored** subsystems are deliberately NOT all chosen here — they emerge from play
  (`system-patterns.md`).

**Fail-state — NONE, BY DESIGN.** Declared, not defaulted. Nothing is ever confiscated: no surface closes,
no arc is lost, no deadline takes the hotel. Refusing a beat, neglecting a person, or being broke costs you
*progress and standing* — never property. The negative axis is **status** (§4): Margaret is winning, in your
mother's house, in front of you. That is the only thing that gets "worse," and erasing it is the want.
*(Consequence, held as law: no advertised threat that cannot land. If it can't bite, it doesn't get dressed
as a clock.)*

**Body-state — PREGNANCY IS IN, as a late / frontier axis.** Declared on purpose (v1 left it open for 72
revisions). It lands exactly where the charge already points, and there are two targets:
- **Grayson** — blood half-brother. The breeding taboo, straight.
- **Richard** — the widower. You don't just take the house; you **replace Eleanor in it**. "Becoming the new
  woman of the house" stops being a metaphor.

It rides the engine's existing pregnancy axis (the player portrait's `pregnancy_suffix`; a hidden trait) and
it is **always a payoff she chooses — never a punishment.** A punitive pregnancy would smuggle the cut
fail-state back in through the side door. Wiring is Step 4/5; declared here.

### 9. The machine (cross-wiring — the depth spine)

**One machine, not parallel arcs sharing a wallet.** This is the best structural idea v1 had and it is kept
whole. The core loop is fixed here; the full per-arc wiring is finalized at Step 5.

**The core loop:** floor work → **money** → take the hotel in hand → open the private floor → bigger money +
access → **fund the family hooks** → corrupt the family → the family joins the service (more money) → take
the will → apex.

**Every core node has a place in it:**
- **Audrey** — the entry conquest, the tuition hook, and the **gateway** to group content.
- **Grayson** — the obstacle → humiliated → bought out.
- **Richard** — gatekeeper of the will → seduced → signs control over.
- **Margaret** — the apex rival for the will and the house.

**The wires:**
- **Form 2a (economy as connective tissue).** Hotel money is the *gate* that advances family arcs: pay
  Audrey's tuition to deepen her dependence; cover Richard's debts to own him; out-spend and buy out
  Grayson. The economy is the tissue *between* arcs, not a shared wallet beside them.
- **Form 1 (arc→arc depth gates — mid/late rungs ONLY).** **Margaret's power is routed THROUGH the men.**
  Her late rungs are gated on player flags the other conquests set (`richard_signed`, `grayson_bought_out`)
  — so **breaking the men is what breaks her.** She isn't a fourth parallel arc; she is what the other three
  *add up to*. Audrey's late group capstones gate on `richard_stage` / `grayson_stage`. Grayson's
  humiliation gates on hotel control.

**The three disciplines:**
- **D1 — never gate an arc's ENTRY on another arc.** Everyone lives in this house; everyone is meetable from
  a cold start. Only mid/late rungs cross-gate.
- **D2 — the wires form a DAG.** No cycles. Checked at the blueprint and again at the feedback review.
- **D3 — every cross-gate is a locked-visible telegraph naming the other arc's state.** *"Margaret won't be
  moved while Richard still holds the deed"* — a silent cross-lock is a soft-lock.

**Milestone → a shared player FLAG. "How far along" → the `<npc>_stage` player TRAIT.** Never a raw
cross-NPC trait read.

---

## Spatial graph & location model (Step 2b)

### The archetype — nested-zones

**Town (root) → The Hotel (venue) → floors (sub-hubs) → rooms.** The skill cites this game by name as its
canonical nested-zones example, and the premise wants exactly this: one building she grew up in, with a
street outside it. A "floor" is just a named hub with `entry_from` — there is no floor primitive and none is
needed.

**Aliveness — dense and living, not a tight slice.** Chosen on purpose (this is a content-budget fork, not a
quality dial). **Depth over breadth: 21 rooms, and every one of them has a job.**

> **What went wrong in v1, measured.** Its map wasn't dead — it was **lopsided**, with three empty stages and
> one unreachable room. Audrey's Room had **19** canvases; **Grayson's had 1**, Richard's 3, and **Margaret's
> — the apex conquest — had 3.** The Private Floor, the endgame venue, had **1**. The Residence, The Grand
> Stair and Town had **zero** — and since v1 declared no containers, the player could walk into all three and
> find nothing there. The Dining Room was gated on `hotel_dining_reopened`, a flag **set exactly zero times in
> the entire game**: unreachable forever, and shipped anyway.
>
> The topology was never the problem. **Jobs** were.

### The graph

```
Town  (root)                                    ← the street; a DIFFERENT ceiling than the hotel
├── The Boutique                                 (shop UI + the mirror)
├── The Adult Shop                               (the tools)
├── Halloway & Sons                              (the lawyer — the will's machinery)
└── The College                                  [OFFSCREEN — Audrey's away-label]

The Hotel — Lobby   (entry_from Town)           ← the public stage. Costs TIME to cross from Town.
├── The Bar                                      (Lorna)
├── The Guest Rooms                              (where a comped favor has somewhere to happen)
├── 🔒 The Back Office                           (the books)
├── 🔒 The Private Floor                         (the vice-house apex)
└── The Grand Stair                              ← the threshold between your two selves
    └── The Residence  (the landing)             ← who's home; who's behind which door
        ├── The Drawing Room                     (Margaret holds court)
        ├── The Study                            (Richard; the deed)
        ├── The Kitchen                          (the neutral ground)
        ├── The Upstairs Bath                    (the shared private space)
        ├── Your Old Room                        (your base)
        ├── Audrey's Room
        ├── Grayson's Room
        ├── Richard's Room
        └── Margaret's Room
```

### Every room's job + access

**The room-content floor is a GATE: if you can't name what the player comes here to DO, the room doesn't
ship.** (v1 shipped four rooms that failed this and one that couldn't be entered.)

| Room | This exists so the player can… | Access |
|---|---|---|
| **The Hotel — Lobby** | Work the floor. The public stage where the fall happens in front of people — and where, on frame one, **Margaret is behind your mother's front desk giving orders to your mother's staff.** The reactive world bites hardest here early. | open |
| **The Bar** | Find Lorna — the one person glad you're back, and the only one who'll tell you how bad it really is. Loosen guests. Take the drink that makes the next thing easier. | open |
| **The Guest Rooms** | Cross the transactional line. A comped room is the first favor that has somewhere to happen. | open |
| **The Grand Stair** | **Collide with your two selves.** You come off a shift in a bold outfit and meet family coming down. She *is* the woman who works the floor below and the daughter who lives above; this is the one place those two meet. Charged crossings, both directions. | open |
| **🔒 The Back Office** | Take the hotel's purse in hand. The books, the accounts, the roof everyone sleeps under. **Unlock beat:** Richard hands you the ledger because he can no longer face it. | locked-visible |
| **🔒 The Private Floor** | Run the vice-house. The dirtiest money and the best. **Unlock beat:** hotel control + the upgrade bought. | locked-visible |
| **The Residence** (landing) | See who's home. Which doors are shut, who's behind them, who's in the bath. The presence surface the peep/caught/occupied content is built on. | open |
| **The Drawing Room** | Watch Margaret hold court **in your mother's chair.** The status humiliation stage — the thing you want to erase. | open |
| **The Study** | Find Richard where his grief lives, with the deed in the drawer beside him. | open |
| **The Kitchen** | Catch the family unarmored, at odd hours. **The one room where they're people instead of positions** — which is exactly what makes it usable. | open |
| **The Upstairs Bath** | Occupy, walk in on, be walked in on. The shared private space — the door is never locked and the schedule decides who's behind it. | open |
| **Your Old Room** | Sleep. Dress. Look at yourself. Use the phone. Do the things to yourself that open the door. | open |
| **Audrey's Room** | Work the sister who has the most to lose and the least power to refuse. | open |
| **Grayson's Room** | Work the brother. **v1 gave this room ONE scene for a core target — the single worst hole in the map.** | open |
| **Richard's Room** | Work the widower in private — as distinct from the Study, which is his grief in *public*. | open |
| **Margaret's Room** | Work the apex. **v1 gave the final conquest three scenes in her own bedroom.** | open |
| **Town** (the street) | Be seen outside the building — a *different* place ceiling. Same outfit, different room, different scene. | open |
| **The Boutique** | Buy the dial — and **turn it, in front of the mirror, with the door shut.** v1 bought the reactive dial and never once dramatized turning it; this is the first rung of the exhibitionism ratchet. | open |
| **The Adult Shop** | Buy the tools that unlock rungs (they gate content, locked-visible). | open |
| **Halloway & Sons** | Move the will. The lawyer's office is the machinery of the inheritance — **not** a doom clock (there is no fail-state; §8). | open |
| **The College** | — | **offscreen** (Audrey's away-label; never navigable) |

**Cut from v1, on purpose:**
- **The Dining Room** — locked behind a flag nothing set, zero content, and no job the Private Floor doesn't
  already do better. It is the purest specimen of the disease; it does not come back.
- **Out & About** — a vague catch-all with one scene. A room named "somewhere else" has no job.

### Naming contract

**Articled / old-money house style, applied evenly** — the register the building actually has ("The Bar",
"The Drawing Room", "The Grand Stair"), with **possessives for private interiors** ("Audrey's Room", "Your
Old Room"). Hierarchy rides the nav depth, never the label. The skill permits a house style; the only real
defect is *inconsistency*, so: every public room takes the article, every private room takes the possessive,
no exceptions.

### Travel friction

**Free inside the building. Time-costed to Town.**

Charging her to climb her own stairs is friction with no drama. But **going out costs time** — and that one
cost is what makes the household's schedules bite: *leaving the building means missing someone in it.*
Choosing to go shopping is choosing not to catch Richard alone in the study. The cost sits on the single
bridge that matters (Town ↔ Lobby, both directions), which is also the only bridge — so no fast-travel valve
is needed; the bridge *is* the valve.

---

## Casting (Step 3) — every NPC's role, hook & place in the machine

**The cast is small on purpose: four core targets, one ally, two props.** Every person under this roof is
either someone you take or someone who teaches you how. Nobody is scenery.

> **MAP AMENDMENT (bounced up from casting, done whole).** **Halloway & Sons is CUT** — 21 rooms → **20**.
> Halloway's only role in v1 was the foreclosure clock, and Step 2 cut the clock (no fail-state). A room whose
> only inhabitant is a prop has no job, and the room-content floor is a gate. The will now lives entirely
> under the roof: **read** in the Drawing Room (Margaret already in your mother's chair — the opening frame),
> **signed** in the Study (Richard, at his own desk, after you've hollowed him out), **contested** by Margaret
> in your face. This is *more* on-fantasy, not less: the premise is "every person under its roof," and the
> lawyer was the one person who wasn't.

### Structural coverage ✅

| Required role | Who fills it |
|---|---|
| **Pressure source** | **Margaret.** With no fail-state, pressure can't be a squeeze that takes things — it's a **rival who is beating you, visibly, in your mother's house.** Status, not confiscation. |
| **Corrupting on-ramp** | **Lorna** + the hotel floor itself. She hands you the first dirty idea and every bigger one after it. |
| **Core target(s)** | **Audrey · Grayson · Richard · Margaret** — the whole household. |
| **Late-act pressure** | **Margaret**, escalating: the prize gets bigger, never the danger. |
| **Gatekeeper** | **Richard** — he holds the deed. (Also a core target; one character can hold two roles.) |
| **Ally / enabler** | **Lorna.** |

### The cast

| NPC | Role(s) | Hook — dynamic · charge · want | Register | Depth | Arc-shape (budget) | Place in the machine |
|---|---|---|---|---|---|---|
| **Audrey** | Core target (entry) + **GATEWAY** | The baby sister who never stopped looking up to you — broke, terrified of losing her place at college, so hungry to be *taken care of* that gratitude curdles into something she won't name. **Want:** land the boy (Danny). **Charge:** corruption-as-mentorship — she wins *and* she's yours. | Vulnerable → groomed · cold sapphic | Core / gold | **family/ambient — DENSE (25–35)** | **Tuition hook** (Form 2a) + the **group-content gateway**. The first family unlock. |
| **Margaret** | Core target (**APEX**) + **pressure source** + late-act pressure | Eleanor's sister, moved in "to help" — sharp, patient, already counting the silver, and reading you as the only real threat in the building. **Want:** the will, the hotel, the family under her. **Charge:** conquest of the apex who came to conquer *you*. | Dominant antagonist → taken · cold sapphic | Core / gold | **family/ambient — DENSE (25–35)** ⚠️ **RE-SHAPED** | **Apex node.** Her late rungs gate on `richard_signed` + `grayson_bought_out` (Form 1) — **breaking the men is what breaks her.** She is also the standing humiliation (§4). |
| **Grayson** | Core target + obstacle + **the prey-phase predator** | Your brother — entitled, useless, certain the inheritance is his and you're beneath him. Certain enough to put his hands on you while you're still nobody. **Want:** the money without earning it; dominance over you. **Charge:** humiliation — break the arrogance, bring the prick to heel. | Arrogant rival → heeled · domination | Core | **family/ambient — DENSE (25–35)** ⚠️ **RE-SHAPED** — *density lives in **Lane 3** (the prey phase), not in a long seduction ladder* | **Obstacle → bought out.** He is the in-house face of the **forced/prey-early** mode; his subjugation sets `grayson_bought_out` (Form 1 → Margaret's apex gate). |
| **Richard** | Core target + **will gatekeeper** | Eleanor's widower, hollowed out, drifting through a hotel he can't run, holding the deed and forgetting why. **Want:** Eleanor back. Comfort. To hold the family together. **Charge:** console-into-own the broken king. | Tender-predatory / fill-the-void · widower seduction | Core | **slow-burn family (10–15)** *(v1 got this right)* | **Gatekeeper node.** Seduced → signs control over, setting `richard_signed` (Form 1 → Margaret's apex gate + hotel control). |
| **Lorna** | **Corrupting on-ramp** (structural) + ally/enabler + **the mirror** | The hotel's lifer bartender who's seen what this place was and what it could be after dark — worldly, unshockable, glad to teach the new owner how a room like this *really* turns a profit. **Want:** the hotel alive, and her cut. **Charge:** she hands you the first dirty idea. | Knowing mentor · transactional | **Light / peripheral** | **service (6–10)** | **On-ramp node.** She opens each rung of the income ladder: tips → comped favors → escort → the private floor. |
| **Danny** | Prop — Audrey's payoff | The ordinary college boy Audrey is hopeless over. Sweet, clueless, no idea what he's walked into. **Want:** Audrey. **Charge:** none of his own — he's *her* win, and the body in the group content. | — | Prop | — (2–3) | Audrey's payoff. **Relocated: he now visits the house** (v1 staged him in "Out & About", which is cut). |
| **Mr. Halloway** | **Prop — one scene** | Eleanor's executor. Starched, correct, reads the will and leaves. | — | Prop | — (1) | None. **Not a character** — the will reading needs a formal voice, not a person. *(Was v1's "deadline with a face"; the deadline is gone.)* |

### ⚠️ The casting error that sank v1 — named, so it can't repeat

**Margaret was not under-built. She was MIS-CAST — and then built correctly to the wrong budget.**

| | v1 built | cast as | that shape's budget |
|---|---|---|---|
| Audrey | 20 | family/ambient | 25–35 |
| Grayson | 14 | **antagonist** | 6–10 |
| Richard | 13 | slow-burn | 10–15 ✓ |
| **Margaret** | **8** | **antagonist** | **6–10 ✓ (in budget!)** |
| Lorna | 5 | service | 6–10 |

The author obeyed the matrix. **Margaret came in *inside* her budget.** The bug was upstream: *antagonist/witness*
is the shape for an obstacle who **never becomes a target** — and Margaret is the game's **apex conquest.** An
apex needs a climb, and 6–10 canvases cannot carry one. Same error on Grayson.

**Both are re-shaped to family/ambient (dense).** They live in this house, they are in front of you constantly,
and they are the last two things you take.

### The honest budget

Four core arcs at these shapes = **~93–133 NPC canvases**, plus the player track (floor work, the feeders, the
economy ladder, the hotel upgrades, the opening, the phone) at roughly **30–40**. Call it **~125–170 canvases**.

**v1 shipped 76.** This is close to double, and that is simply what *"own the whole household"* costs. Stated
here, at casting, so the blueprint cannot quietly shrink it back into a corridor.

### Rough sketches & cross-NPC threads

**Audrey — the gateway.** The load-bearing thread. She's the first one fully open, so her late content unlocks
the **group routes** (Danny, then Richard, then Grayson). The more you have Audrey (`audrey_stage`), the more
group content lights up. Her want (*land Danny*) is what makes her corruptible: you teach her how to get him,
and **the teaching is the corruption.**

**Richard ↔ Margaret — the will.** Richard nominally holds control; Margaret is prying it out of his grief.
Owning Richard first (he signs to *you*) strips Margaret's claim and detonates the apex. Both feed the will.

**Grayson — the early predator, the late grovel.** In the prey phase he's the in-house face of the liberties you
**can't refuse** (Step 2 §5). His arc is the inversion that pays that off: the man who put his hands on you when
you were nobody ends up bought and heeled. He bridges the reactive world and the humiliation arc — which is
exactly why his density lives in Lane 3.

**Lorna — the mirror.** *(Role unchanged from v1, on LO's call.)* She is the **one person you never take**, and
that's the point: everyone else in this house you own, and she's the one who's on your side by choice. She's
what you're **becoming, already arrived** — and the way that lands is the recurring beat v1 designed and then
**never built**: you catch **Lorna with a customer** (behind the bar after close, in the guest rooms). She
catches your eye, winks, doesn't stop. Voyeuristic only; never pull the player in.

> **The Lorna build correction (not a role change — a shape change).** v1 gave her 5 canvases and **4 of them
> fire exactly once**: meet her · take the books · the Grayson tip · the partnership. After a couple of hours
> she was a woman behind a bar with nothing left to say — and the **structural on-ramp died with her.** Same
> light budget; spent differently: her hub is **repeatable and TIERED**, escalating with the business — *"there's
> a guest in 12 who tips if you're friendly"* → *"comp him the room, he'll pay it back"* → *"I know girls who'd
> work a floor like this"* → *"the top floor's been empty a long time."* Plus the mirror beats, which are the
> thing that makes her a person instead of a menu. **Keep her light. Never gold-plate her. Never bed her.**
