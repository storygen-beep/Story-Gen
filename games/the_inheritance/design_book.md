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
└── Stairs                                       ← the threshold between your two selves
    └── The Residence  (the landing)             ← who's home; who's behind which door
        ├── The Drawing Room                     (Margaret holds court)
        ├── The Study                            (Richard; the deed)
        ├── The Kitchen                          (the neutral ground)
        ├── Bathroom                             (the shared private space)
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
| **Stairs** | **Collide with your two selves.** You come off a shift in a bold outfit and meet family coming down. She *is* the woman who works the floor below and the daughter who lives above; this is the one place those two meet. Charged crossings, both directions. | open |
| **🔒 The Back Office** | Take the hotel's purse in hand. The books, the accounts, the roof everyone sleeps under. **Unlock beat:** Richard hands you the ledger because he can no longer face it. | locked-visible |
| **🔒 The Private Floor** | Run the vice-house. The dirtiest money and the best. **Unlock beat:** hotel control + the upgrade bought. | locked-visible |
| **The Residence** (landing) | See who's home. Which doors are shut, who's behind them, who's in the bath. The presence surface the peep/caught/occupied content is built on. | open |
| **The Drawing Room** | Watch Margaret hold court **in your mother's chair.** The status humiliation stage — the thing you want to erase. | open |
| **The Study** | Find Richard where his grief lives, with the deed in the drawer beside him. | open |
| **The Kitchen** | Catch the family unarmored, at odd hours. **The one room where they're people instead of positions** — which is exactly what makes it usable. | open |
| **Bathroom** | Occupy, walk in on, be walked in on. The shared private space — the door is never locked and the schedule decides who's behind it. | open |
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

---

## Story design (Step 4) — the story, one subject at a time

> **STORY ONLY.** No lanes, no thresholds, no flags, no placement — those are the Blueprint's (Step 5).
> Here: what happens to these people, and what it feels like.
>
> ⚠️ **v1 never wrote this pass at all.** Its Step 4 was NPC briefs and nothing else — no player thread, no
> world, no reactivity. That is the root of the starved player track and the dead rooms: the *supply* was
> never designed before the *demand* leaned on it.

### The player thread (Step 4 · §2)

#### She uses it, and then she wants it

The cascade says she must corrupt herself before she can corrupt anyone. The register says she is cold,
deliberate, and here for conquest — not longing. **Both are true, and the tension between them IS her arc.**

- **Act 1 — "it works."** She isn't seduced into anything. She does this because it *pays*: the tips are
  better in the lower-cut thing, the guest signs when she leans in, Richard talks when she sits close. Sex is
  a **tool**, and she is holding it. She'd tell you she's in complete control, and in Act 1 she mostly is.
- **Act 2 — "…I wanted that."** The gap opens. Somewhere between doing what it takes and doing it again
  when she didn't have to, she catches herself. **The cold is armor, not a personality**, and this is the
  sound of it cracking.
- **Act 3 — "I want it."** The armor is gone and what's underneath is worse than anything in this house.
  She is no longer using the thing. It's hers.

**What cracks her is the one thing she doesn't control: the liberties she can't refuse.** While she's still
nobody — broke, underestimated, working her own floor — a guest's hand, or Grayson in her doorway, takes
something. She can't stop it. That's the prey phase, and it is precisely what a woman who thinks she's
holding the weapon cannot account for. *(This is the floor of the prey→predator reversal; it recedes as she
rises.)*

#### §2A — The bootstrap: getting off zero, with no one watching

**Night one.** She's alone in the room she grew up in, in the house that wrote her out, and she is not
aroused — she is **furious and wide awake at 3 a.m.** The old set still pulls the channels nobody admits to.
She watches, and she gets herself off in the bed she was a child in.

**It isn't appetite. It's spite, and relief.** And it's the first crack — she notices, afterwards, that she
still wants something, and it isn't relief. It's the rooms down the hall.

**Off-zero without a solo act:** she can be *looked at* before she's chosen anything. The lobby has eyes from
the first hour — guests, staff, Grayson — and being seen costs her nothing and moves her anyway.

#### §2B — The exhibition backbone: being SEEN

The ratchet runs **mirror → floor → room**, and what she *wants* out of it changes underneath her:

| Stage | Where | What she wants out of it |
|---|---|---|
| **The mirror** | the boutique, door shut; her own room | to see it. Nobody else yet. |
| **The floor** | the lobby, the bar | **tips.** The bolder thing simply earns more, and that's the whole reason. |
| **The floor, again** | the lobby, the bar | **a specific head turned** — Grayson watching his sister hostess; a guest who'll sign. |
| **The room** | the guest rooms, the private floor | **the fact that she can.** Being looked at stops being a means. |

What she's wearing is a dial she can turn back. How far she's *willing* to be seen only ever climbs.

#### §2C — Earning IS corrupting: her money story, broke to rich

**The ladder is the fall.** Every rung pays better and costs more of her, and the better money is *always*
further down:

1. **Hostess the floor** — the lowest respectable money. Scraps. Her mother's hotel, her mother's staff, and
   she's carrying drinks in it.
2. **Work it bolder** — the same shift in the lower-cut thing. The stares are worth money. This is the first
   time being looked at has a price on it, and the price is good.
3. **Comp a room for a "favor."** Lorna's first dirty idea. The first line that can't be uncrossed — and the
   hotel makes more from one comped room than a week of scraps.
4. **Escort arrangements.** Not the hotel's money now. Hers.
5. **The private floor.** The dirtiest and the best.

**A second path so it's never a grind:** she sells photographs off the phone. Real scenes, not a button — who
she sells to, and what they ask for next.

**The sinks that keep her hungry even once she's rich** *(there is no fail-state — pressure is want, not
threat)*: bolder clothes (the dial costs money) · the hotel's rooms coming back to life · and **the family
hooks — Audrey's tuition, Richard's debts.** Paying is never charity. It's a hook, and she knows it while
she's writing the cheque.

**The key things money buys that aren't clothes:** a toy she teaches with · something to loosen a target ·
a photograph she doesn't delete.

#### §2D — Her ceiling, and what else she climbs

**The top of her own depravity — public, about HER, unthinkable on night one:** she doesn't just *run* the
private floor. **She works it.** The headline slot, in her mother's hotel, with the household serving
downstairs — the woman who was written out of this building's future, on top of it and being paid.

**Other ladders:** none. No skill track, no rank, no fame. Her climb is corruption and exhibition, and the
house's transformation runs on the conquests, not on a bar. **The hotel coming back to life is the only other
thing that grows**, and it grows because of who she's broken.

**Her livable top:** when the climb is done the floor still runs, the private floor still pays, the household
still serves, and the loops she likes are all still there. Never a blank screen.

#### The daily routines — where the world walks in *(the fused unit)*

**This is the pass v1 skipped, and why its kitchen and bath shipped dead.** Every repeated chore is ONE
moment doing three jobs at once: the thing she came for, the thing she does alone, and **the door someone
opens.**

| The routine | What she came for | What she does alone | Who walks in — and what it feels like |
|---|---|---|---|
| **Sleep** — your old room | the day ends | the channel nobody admits to; the phone; her own hand | **Grayson**, who does not knock. He doesn't even pretend it was a mistake. |
| **The bath** — the upstairs bath | to be clean | her hands, in the water, quietly | **Grayson** ("door was open") · **Richard** (mortified, and slower to leave than he should be) · **Margaret** (looks, says nothing, **banks it**) |
| **Eating** — the kitchen | energy, at an odd hour | — | whoever else is up: Richard drinking alone, Audrey with a book she isn't reading, Grayson at the fridge. **The one room where they're people instead of positions** — which is exactly what makes them reachable. |
| **The floor shift** — the lobby, the bar | money | dressing bolder and taking the stares | guests take a liberty · **Grayson watches his sister hostess**, and hates it, and can't stop |
| **The mirror** — the boutique | the dial | trying it on. Turning. Looking. | the shop girl who's seen it before; a stranger who hasn't |

#### The day, walked across *(breadth — is there more than one thread?)*

A representative mid-game day has: **her own self-care** (the bath, the bed) · **being seen** (a shift in the
bolder thing) · **a second economy** (the phone) · **the house waking up** (a room coming back) · **whatever
walks in on her** · and **four people to work.** The day is never only the grind.

**Supply before demand:** the deepest thing the family will ever ask of her is further down than anything she
can reach on night one — and every rung between here and there is a scene she *wants* to play, not a number
she has to farm. If any band of her climb ends up with nothing real in it, the blueprint has failed, not her.

---

### Audrey — story brief
*entry target + **GATEWAY** · family/ambient, DENSE (25–35) · core/gold · cold sapphic*

> **Her job in the game:** the entry target AND the **gateway** — the first one fully open, and the key that
> unlocks the group content everywhere else. The biggest, most replayable arc in the game *even though she's
> the easiest.* Written as the warm, eager sister against the cold register of everything around her.

**§1 · End-state — corruption disguised as mentorship. She WINS, and she's yours.**

Her own **want** drives the arc: there's a boy — **Danny** — she's hopeless over and too innocent to land.

The ramp is trust. She comes to you panicking about tuition; you pay it; she learns that **her big sister is
the one who fixes things.** So when the boy problem hits, she brings *that* to you too — and **asks to be
taught.** You teach her, skill by skill, and **the lessons are the corruption.**

The twist — and it's what makes this darker rather than lighter: **Audrey genuinely succeeds.** She lands
Danny. She gets exactly what she wanted. But by then you have rebuilt her into a girl with no lines left: she
practices everything on her sister first, shares Danny's bed with you, and is happily down for the whole
family. **She never once sees any of it as wrong.** She thinks she has the closest, luckiest family alive and
a sister who taught her everything.

**The horror is entirely the player's to see.** She aced the class and never noticed what the class was.

**§2 · Voice.** Soft, eager, earnest — a diligent student who *wants to get it right*: "Okay, so — like this?
Am I doing it right?" Fast when she's nervous; deflects worry into helpfulness. Calls you **Cath**.

**Never crude in her own voice early.** The dirty words are part of the *lesson*, coaxed out of her — *"say
it, it's just us"* — and **that coaxing is the content.** Once a skill is learned she's unembarrassed about
it; she's **proud**. One private thought per appearance: a rationalization. The early ones are shy and about
Danny. The later ones are easy, and happy.

RTS-flat for the everyday; the once-only peaks are where her reframing blooms — *this is just sisters, this
is just practice, this is just love.*

**§3 · The arc, as moments.**
Cold-warm at the start — she's just glad you're back, and has no idea what you are. → **The tuition panic**
(she has nowhere else to go). → **You fix it.** → She starts bringing you things instead of waiting. → **The
boy problem.** → *"Can you teach me?"* → The first lesson is innocent; the second one isn't. → **"I can't
practice on him yet, so… on you."** → The practice stops being practice. → **She gets the boy** — and brings
him home to show you. → She shares him with you, and finds it the most natural thing in the world. → She is
the willing third everywhere else in the house.

**§4 · The pretext — THE LESSON LADDER.** The entire sapphic arc is smuggled inside a pretext *she believes*:
*I can't practice on him yet, so I'll practice on you.*

| Lesson | She practices on |
|---|---|
| the tuition confession *(non-lewd — the hook)* | — |
| **touching herself** | herself — her "homework" |
| **kissing** | **you** |
| **the toy** | herself |
| **going down** | a toy, then **you** |
| **the first time** | **you** |
| **the last thing** | **you** |

**§5 · The big nights** (once-only peaks — what each is, and what it sets in motion):
1. **"You fix everything."** The tuition crisis; you pay it. The trust that opens every door after it.
2. **"The first lesson."** She asks for help landing Danny. The line moves and she doesn't notice.
3. **"The first night."** The practice becomes the real thing. In her head it is *still a lesson, still love.*
4. **"She got the boy."** Her own goal genuinely comes true. **Let it be a real win** — that is the knife.
5. **"Study group."** She shares Danny with you, cheerfully, and it doesn't occur to her to mind.
6. **The family nights** — Audrey + Richard (father and daughter; **LO-confirmed, carried forward**), and
   Audrey + Grayson. The gateway paying off.

**§6 · What changes after.** *(v1 never wrote this section — which is exactly why she read as a menu.)*
- After **the tuition**: she seeks you out instead of waiting to be found.
- After **the first lesson**: she starts closing the door *behind* you, not in front of you.
- After **the first night**: she stops calling it practice.
- After **Danny**: **she brings him home.** The boy is in the house now, at the kitchen table, and she wants
  you to like him.
- After **the family nights**: there is nothing you can ask her for that she will find strange.

**§7 · Her ambient life.** *(The other thing v1 missed: she had 19 canvases and **zero** ambient scenes —
19 things you DID to her, and not one moment of her simply existing.)* She lives here. You catch her:
studying at the kitchen table with a book she isn't reading · on the phone to Danny, going quiet when you
walk in · coming out of the bath · doing her "homework" behind a door that isn't quite shut — and later, one
that is deliberately open. **This is what a dense arc is actually made of.**

**§8 · Anti-patterns.** Don't make her crude unprompted early — the words are **coached** out of her. Don't
let the practice read as a chore: vary it (nervous → clumsy → proud) so it feels like *learning*, not
repetition. Don't let **Danny** become a real character with an arc — he's her win and a body. And the
load-bearing one: **from her side this is never a transaction and never a seduction.** It is care, and
sisterly help, and family. **Only the player sees the leash.**

**§9 · Acceptance (story).** Done when: the **hook is visible** (the eager-student voice, the real want, and
genuine agency — she chases Danny herself and never notices the chase was hijacked); the **fall is
believable** (comfort → trust → "teach me" → the redirect onto you, each moment following the last with no
jump); the **"devotion, not corruption" framing holds** the whole way (she never names it); and the **peak is
earned** — she wins the boy *and* is wholly yours. The sweetest surface over the darkest core.

> **Danny — relocated.** v1 staged him in "Out & About" (cut at Step 2b). He now **visits the house**: the
> kitchen table, Audrey's room. Better — the boy is inside your world, on your stages, where you can reach him.

---

### Grayson — story brief
*core target + obstacle + **the prey-phase predator** · family/ambient, DENSE (25–35) — **density lives in Lane 3** · core · domination / femdom*

> **His job in the game:** the brother you *break*. The cast's only pure-payback arc — the dominant register
> against Audrey's tenderness and Margaret's cold rivalry. He starts on top of you and ends your willing
> lapdog. **Bought with money, exactly like Audrey — but corrupted into submission, not love.**
>
> He is also **load-bearing in two directions at once**: the man who takes liberties from you before you're
> anybody, *and* the man you bring to heel. The reversal only lands if the early half genuinely stings.

**§1 · End-state — the arrogant heir broken into your willing lapdog.**

He's the entitled parasite, certain the estate is his and you're beneath him — and **early, while you're
still nobody, he's handsy.** He bullies and paws at you *because he can.* That is the floor of the game's
whole prey→predator reversal, and it has to actually sting.

Then you take the money. The hotel's purse is yours, his allowance is gone, and his **gambling debts** — to
people who hurt slow payers — are closing in. So he comes to **you**, needing cash. And the price is **a day
as your servant.**

It's a cold transaction and he despises it. But repeated servitude **rewires him.** The man who never had to
do anything in his life discovers he *needs* it — the structure, the being-owned, your attention. The money
stops being the point. He ends giving himself **for free**: your chastity-locked, orgasm-controlled lapdog,
made to *watch* you take everything he thought was his, and signing his claim over — because the throne means
nothing next to belonging to you.

*(Bought into submission. The prince who begged for the collar, and then begged to keep it.)*

**§2 · Voice.** Smug, condescending, entitled drawl. **"Sis"** as a sneer. Casual cruelty while he's on top.
As he breaks: bravado → sullen compliance → neediness → eager grovelling (*"Tell me what you want — I'll do
it, just— let me"*). RTS-flat everyday; Tier-3 earned only at the once-only peaks (the deal, the turn, the
surrender). One private thought per appearance — early ones contemptuous, later ones **humiliated by how
badly he wants it.**

**§3 · The arc, as moments.**
He's on top of you, and enjoying it. → **He takes something you can't stop.** → You take the purse. → His
allowance dies. → **He comes to you needing money** — and hates it. → The price is a day of service. → He
does it seething. → He does it again. → **He stops needing to be paid.** → He asks. → He gives himself, signs
everything away, and is grateful.

**§4 · The pretext — THE SERVITUDE LADDER** (bought with money, exactly like Audrey; each step strips more
of him off):
- **The prey floor (early).** He gropes and bullies you while you're powerless. It happens *to* you, and you
  can't refuse. **It recedes as you rise** — and the recession *is* the point.
- **The flip.** He comes broke, bookies on him. You name the price.
- **Menial.** Fetch, carry, wait on you, kneel. Strip the dignity off a man who never earned any.
- **Degrading.** Beg. Be mocked. Serve in front of others. Worship you.
- **Use (full femdom).** He's a toy — his orgasm on your terms (denial, ruined, chastity). Pegging.
  **Cuckold / made-to-watch** — he watches you take others; the lowest body in the room.
- **Free service.** He comes unpaid. He asks for it. He gives himself.

**§5 · The big nights.**
1. **"The deal."** He comes broke; you set servitude as the price; he takes it seething (or storms off and
   comes back worse). The cold transaction that starts the unmaking.
2. **"On his knees."** Service becomes use — you take control of his body.
3. **"He stops pretending."** The turn: he serves, and you both know he *wants* it now. The deepest
   humiliations open.
4. **"Yours for nothing."** He comes unpaid, gives himself, and signs his claim over. Belonging to you
   matters more than the throne he was promised.

**§6 · What changes after.** *(v1 never wrote this.)*
- After **the prey floor**: *nothing changes* — and that's the horror. He does it again.
- After **the deal**: he can't meet your eyes in front of Margaret.
- After **on his knees**: he starts *finding reasons* to be wherever you are.
- After **the turn**: the sneer is gone from "sis," and what's left underneath is worse for him.
- After **free service**: he watches you take his father, his aunt, and his sister — **and he holds your coat.**

**§7 · His ambient life.** *(Where his density actually lives — he is cast Lane-3-dominant.)* He is
*everywhere* in this house, and that IS the texture of Act 1: sprawled in the drawing room with his feet on
your mother's furniture · at the fridge at 2 a.m. · on the phone to someone he owes, voice low, hanging up
when you walk in · at the bar nursing a drink, **watching his sister hostess** — hating it, unable to stop.
**And in your doorway. Not knocking.**

**§8 · Anti-patterns.** **Don't let the early groping read as *his* win** — it is the humiliating floor that
*earns* the payback, not fan service for him. **Don't break him fast:** he is not Audrey, he *fights*; the
bravado must be real and resistant or the fall is worthless. The unmaking is **repeated** — day after day of
paid service rewiring him, never a single beat. Keep the **status humiliation** present throughout (the heir
watching you take everything is the spice).

**§9 · Acceptance (story).** Done when: the **hook is visible** (the smug entitled voice, and the way it
cracks into need); the **reversal is believable** (prey → bought → craving → freely given, breaking by
degrees with no quick fold); he stays **formidable early** (he genuinely fights); and the **peak is earned** —
the heir who pawed at you when you were nobody ends a willing lapdog who signs everything away and is
grateful to.

> **How you get the weapon: Lorna tells you.** The gambling debts come to you through the bartender — her
> "eyes and ears" job (Step 3). The knife you put into Grayson was handed to you by **the one person in this
> building who is on your side by choice.**

---

### Richard — story brief
*core target + **will gatekeeper** · slow-burn family (10–15) · core · earned seduction*

> **His job in the game:** the gatekeeper of the will. The cast's one genuinely *warm* arc — you don't trick
> him and you don't break him. You pull a grieving man back to life, he falls for you, and he hands you the
> kingdom. **Won with trust and lust, never money or coercion.**
>
> **And he is where the armor thins.** Everyone else in this house is a transaction she executes cleanly. He
> is the one where the technique doesn't entirely *stay* technique — she sits with him because it works, and
> then she sits with him a little longer than it works. She would never admit that. Not to him. Not to
> herself. **He genuinely falls. She takes everything anyway.** That is not romance; it is the horror of
> finding out you're capable of meaning it and doing it regardless — the player's own crack (§2), applied to
> a person instead of an act.

**§1 · End-state — the widower who gives you the keys.**

Richard is your **stepfather** — Eleanor's widower, **no blood tie to you**, father to Audrey and Grayson. He
holds the two things you need: control of the hotel, and the will. Since Eleanor died he has been **hollowed
out** — drifting, drinking, running nothing. **His grief is his starting state, not a lever you pull.**

You win him by **becoming the reason he gets up again.** Trust first (his steady presence, his confidante).
Then the closeness turns charged, and he wants you — ashamed of it, and unable to stop. **His wanting pulls
him back to the business:** he throws himself into the hotel to be near you, to impress you, to earn your
company — and you reward the effort with more of yourself. He wants more, works more, you give more, and
**the failing hotel revives on the back of his desire.**

In the end he sees clearly that you would run this place better than he ever could. He's tired. He would
rather **support you than lead**. So he hands you the keys and the will, and stays on as your devoted right
hand. *(The one tender, earned, slightly melancholy arc — the man who fell for the woman who saved him, and
gave her everything.)*

**§2 · Voice.** Grief-fogged, distant, apologetic early — *"Sorry — what did you— I wasn't listening."* As
trust and lust build: warming, then **eager** — alive again, and a little embarrassed by how much he wants you
near. **Dignified even in devotion; never pathetic.** RTS-flat everyday; Tier-3 earned only at the once-only
peaks (the first night, the handover). One private thought per appearance — early ones grief-numb, later ones
guiltily hopeful, then quietly content.

**§3 · The arc, as moments.**
He barely registers that you're back. → You sit with him. You get him eating. → He starts talking. → He
starts *waiting* for you. → The comfort turns warm, turns wanting. → **He catches himself looking, and hates
himself for it.** → He stops hating himself for it. → **The first night.** → He throws himself at the hotel
to deserve you. → **The keys.** → He asks only to stay.

**§4 · The pretext** (built on companionship → lust; **never** on grief-exploitation):
- *Presence (non-lewd):* sit with him, get him eating, fill the silence. Become his steady person.
- *Trust:* he confides, leans on you, lets you in. You become indispensable.
- *The charge:* the comfort turns warm turns wanting — a touch that lingers; him catching himself looking.
- *The pursuit:* he comes alive and throws himself into the hotel to be near you; you accompany, and reward.
- *Explicit:* the first night — him finally letting himself have what he wants. Tender, and a little guilty.
- *The handover:* fully yours, he gives you the keys and the will, and asks only to stay and help.

**§5 · The big nights.**
1. **"Back to life."** The comfort crosses into the first charged moment. He wants you, and you both feel it.
2. **"The first night."** He finally lets himself have you. Tender, guilty, willing.
3. **"The keys."** He hands you control of the hotel and the will — he'd rather support you than lead.
   ***(The move that strips Margaret's claim.)***
4. **"At your side."** The devoted right hand, wholly yours.

**§6 · What changes after.**
- After you **sit with him**: he starts eating.
- After the **first charge**: he shaves.
- After the **first night**: **he goes to work.** The man runs a hotel again, because of you.
- After the **keys**: he brings you the books unasked.
- After the **child** (below): he is *radiant* — and that is the most frightening thing in this game.

**§7 · His ambient life.** In the study with the lamp on at 3 a.m. Standing in the kitchen holding a glass he
hasn't drunk from. Asleep in a chair. Looking at a door he doesn't open. **Later:** down on the floor in his
shirtsleeves, actually working — and looking up when you pass.

**§8 · The child — SUPPLANTING, not impersonation.** *(Folds in the Step-2 pregnancy declaration, which this
brief predates.)*

There is an apparent contradiction here and it must be held precisely, because the arc lives in the gap:

- **BANNED — impersonation.** She never wears the dead woman. Never evokes her, never mimics her, never uses
  the ghost as bait. That would make him a mark being conned, and it is cheap.
- **THE POINT — supplanting.** She takes Eleanor's place **by being better at it**, and the child is the seal
  on that. *She did not become Eleanor. She ended her.*

The anti-pattern survives, scoped to **method**. The pregnancy is the **outcome**. And per Step 2's law, it is
always a payoff she **chooses** — never a punishment.

**§9 · Anti-patterns.** **No Eleanor-impersonation content anywhere** (see §8). The grief is his starting
state, **not** a seduction tool — don't write her preying on it ghoulishly; the arc is earned warmth.
**Never pathetic** — dignified even in devotion. And **the handover must read as WILLING** (trust + age + her
competence), never coerced: a puppet signing is worth nothing, and a man handing it over with his eyes open is
the entire point.

**§10 · Acceptance (story).** Done when: the **hook is visible** (the hollowed widower warming back to life;
the guilty eagerness as he falls for *her*); the **fall is believable** (grief → trust → lust → pursuit → the
willing handover, each step earned); **no impersonation anywhere**; the **handover reads as willing**; and the
**peak is earned** — the one tender, melancholy arc, the man who gives away everything because belonging to
her is worth more than the kingdom.

---

### Margaret — story brief
*apex target + **pressure source** + late-act pressure · family/ambient, **DENSE (25–35)** · core/gold · cold sapphic · **antagonist — destroyed, NOT seduced***

> **Her job in the game:** the **final boss.** The one target you never win over — you *destroy* her.
> Untouchable until you have taken everything else, so she is genuinely the last thing in the game.
>
> ⚠️ **WHY V1 FAILED HER — and it was not laziness.** v1 cast her *antagonist/witness* (budget 6–10) and
> built 8 canvases: **inside budget.** But her v1 *story* was `cold war → the cornering → the breaking → the
> slavery` — **four big nights and some sparring, with no rungs in between.** She wasn't under-built; **the
> story genuinely had no climb in it**, so the shape matched the writing and the writing was the problem.
> Re-shaping her to DENSE is therefore not a budget edit — **it is a demand for new story.** That story is §4
> below: *the war, fought with what she sees.*

**§1 · End-state — the queen who came to own everyone, reduced to the family's communal slave.**

Margaret is your **blood aunt** (Eleanor's sister), the cold schemer who moved in to seize the estate. She is
the one person you **cannot** seduce, buy, or comfort. She stays defiant to the end.

**Her advantage runs entirely through PEOPLE, not paper:** she holds the say of the grief-wrecked widower and
the backing of the pliable heir, while your own claim is weak — the estranged prodigal who walked out. So you
do not out-lawyer her. **You take the men her power runs through.** Seduce Richard into signing control to
*you*; buy out Grayson. Her advantage **collapses** — a schemer with no one left to scheme through.

Still defiant with nothing left, she is **broken by force**: you intoxicate her, and the two men she once
commanded — now wholly yours — **take her**. A one-and-done set-piece you orchestrate; sexual destruction,
then mental. **Terminal state:** the patrician aunt reduced to the household's **communal slave** — domestic
and sexual servitude, **put to work on the vice-house floor she schemed to own**, taking orders from the niece
she scorned and the men she used.

*(The total inversion: she who would own all, owned by all. The game's peak.)*

**§2 · Voice.** Cold, precise, patrician. Velvet over steel. **She compliments like a threat**, never raises
her voice, and never says a crude word. Underneath: pure calculation, never warmth — always a step ahead,
almost beating you. Tier-3 earned only at the once-only peaks. One private thought per appearance: sharp and
scheming through the war — then nothing left to think.

**The shatter is PLAYED, not narrated** (Rule 4 at the apex — the game's biggest beat cannot be a narrated
summary of her voice). At "The breaking," the control cracks in a *spoken* line — the first unguarded thing
she has ever said to you: the precision failing mid-sentence, an order that curdles into a plea she'd have
died rather than speak — *"You don't— you can't— "* → *(and then, smaller)* *"…tell them to stop. Tell
them—"* → the voice going, not gone. **Then** the terminal "family slave" floor is where the voice is
*emptied out* — hollow, vacant, compliant, wordless — because by then the wordlessness is the point. Don't
spend the silence early; earn it by playing the shatter first.

**§3 · The arc, as moments.**
She is already behind your mother's desk when you walk in. → **She catches you at something, and says
nothing.** → And again. → You realise she is *keeping* them. → **She spends one.** → You lose ground. → She
offers you money to leave, politely, like a favour. → You claw back. → **She watches you too long, once, and
you both notice.** → Richard signs. → Grayson kneels. → **She has no one left to scheme through.** → The
breaking. → The floor.

**§4 · The pretext — THE WAR, FOUGHT WITH WHAT SHE SEES.** *(The new story. Her weapon was always "she
banks your missteps — she files, she doesn't grope"; v1 wrote that line and never built it. It is the arc.)*

- **Act 1 — she is AHEAD of you. She catches you, and she files it.** On the floor in the bolder thing.
  Coming out of a guest room. With Audrey. Coming out of the bath. **She says nothing.** She looks, and she
  keeps it, and the noose tightens. *(This is Step 2's status pressure made concrete — she is winning,
  visibly, in your mother's house, and nothing is being taken from you but ground.)*
- **Act 2 — she SPENDS what she banked.** Each file becomes a move, and each move is a scene where you lose
  ground and must claw it back: she takes it to Richard · she works on Audrey · she offers you money to leave
  · she has your things moved out of your mother's room · she turns the staff.
- **The turn — she watches too long.** The one thing she cannot file. She despises what you are doing and she
  **cannot stop looking at it.** She never yields, never softens, never admits it — but the temperature rises,
  and it makes what is coming **worse**: you will eventually give her, by force, the thing she would not have
  admitted she wanted.
- **The cornering.** The board turns — Richard has signed, Grayson is bought — and she understands she has
  lost.
- **The breaking.** You intoxicate her; her own two pillars take her. Sexual, then mental.
- **The floor.** Communal household servitude; put to work on the vice-house floor she schemed to own.

**§5 · The big nights.**
1. **"Velvet and steel."** The cold war — she threatens, manoeuvres, and files. You trade blows and cannot
   touch her. The rising menace that drives the back half.
2. **"The board turns."** Her advantage collapses. The schemer with nobody left to scheme through.
3. **"The breaking."** The one-and-done forced set-piece: intoxicated, taken by the two men she once
   commanded — **her own pillars, turned against her.** *(Non-con, forced. All adult.)*
4. **"The family slave."** Reduced to the household's communal slave, working the floor she schemed to own,
   taking orders from the niece she scorned. **The game's peak.**

**§6 · What changes after.**
- After **the first catch**: nothing. And that is what frightens you.
- After **she spends a file**: the staff stop meeting your eye.
- After **she watches too long**: she is *colder* to you — overcorrecting, and you can see it.
- After **Richard signs**: she comes to your room. At midnight. To talk. It does not go the way she planned.
- After **Grayson kneels**: she notices he cannot look at her, and she understands what that means before he
  does.
- After **the breaking**: there is nothing left to change. That is the point.

**§7 · Her ambient life.** She is **in your mother's chair.** Holding court in the drawing room. Counting the
silver — literally, with a list. On the phone to a lawyer, and unhurried about hanging up when you come in.
Behind the front desk, giving your mother's staff their instructions. **Watching you from across the lobby,
over the rim of a glass, saying nothing.**

**§8 · Anti-patterns.** **Do not make her seducible or winnable by charm** — no romantic yielding, ever.
She is the one you *destroy*. **Untouchable until you've taken everything else** — never let the player reach
her early; that is what makes her a real final boss instead of a fourth door. **Keep her formidable and a
step ahead** through the whole war — she should very nearly beat you (no incompetent villain, no early fold).
**The breaking is ONE-AND-DONE**, not a repeatable rape. Her scheming stays hidden until it detonates. And
**the watching is never a softening** — it is contempt with a hot edge, and she would deny it under oath.

**§9 · Acceptance (story).** Done when: she reads as an **antagonist, not a seduction** (the war is the
through-line, never a warming-up); she stays **formidable to the very end**; the **war has real rungs** (she
catches, she banks, she spends — and you lose ground and claw it back, over and over) rather than four
set-pieces with sparring between them; the **breaking lands as the forced, one-and-done destruction it is** —
her own two pillars turned against her; and the **peak is earned** — the queen who came to own everyone ends
owned by everyone.

---

### Lorna — story brief
*corrupting on-ramp (STRUCTURAL) + ally/enabler + **the mirror** · service (6–10) · **LIGHT / peripheral** · **NOT a sexual target***

> **Her job in the game:** the **one genuine ally** — not a conquest. The veteran bartender who teaches you
> the *business* of corruption, hands you every next dirty idea, and ends as your right hand.
> **Kept deliberately LIGHT. Gold-plating her is the failure.** *(Role carried forward from v1 unchanged, on
> LO's call.)*

**§1 · End-state — the partner you never bed.** Everyone else in this game you take, break, or own.
**Lorna is the exception: the one person on your side by choice.** A trajectory, not a takedown. She starts
as the unshockable lifer sizing up the broke prodigal, becomes your **teacher in the trade** (she drops the
first dirty idea, then opens each bigger one as you rise), and ends as your **right hand**, running the floor
beside you for her cut. She owns the *business* of corruption; she has **nothing to do with corrupting the
family** — she stays out of the bedrooms. **She is the mirror: what you are becoming, already arrived.**

**§2 · Voice.** Worldly, dry, unshockable. Transactional warmth — "honey," "sweetheart." Frank, never
crude-for-shock. **Unbothered by anything, including being caught.** RTS-flat throughout (peripheral — she has
no earned Tier-3 peaks). One private thought when it fits: always shrewd, always counting.

**§3 · The arc, as moments.**
She sizes you up and isn't impressed. → She tells you how bad it really is, because nobody else will. → **She
gives you the first dirty idea**, lightly, like it's nothing. → It works. → She gives you the next one. → She
starts telling you things you didn't ask for (**Grayson's debts**). → You catch her with a customer, and she
winks. → She stops calling you the owner's daughter. → **She throws in with you for good.**

**§4 · The pretext** (advice, unlocks, information — **never seduction**):
- **The lessons.** She teaches the trade, and the ladder is hers to open: *"there's a guest in 12 who tips if
  you're friendly"* → *"comp him the room, he'll pay it back twice"* → *"I know girls who'd work a floor like
  this"* → *"that top floor's been empty a long time."*
- **The tip-offs.** She sees everything, and she's the reason you know where the hotel's money actually went
  — **Grayson's gambling.** *The knife you put into your brother was handed to you by the one person in this
  building who is on your side.*
- **The mirror** *(recurring — and the thing v1 designed and never built)*: you catch **Lorna with a
  customer** — behind the bar after close, in a guest room with the door not quite shut. **She catches your
  eye, winks, and doesn't stop.** She practises what she preaches. **Voyeuristic only — never pull the player
  in.**

**§5 · The big night** (peripheral — she gets exactly ONE, and it isn't sexual):
- **"The partnership."** Once the house is running, she throws in with you for good: the lifer stops being
  staff and becomes your right hand. No first night. No chain. She's the ally, not a conquest.

**§6 · What changes after.** After the first idea works: she starts offering them unprompted. After the
debts: she tells you things without being asked. After you catch her with a customer: **nothing changes at
all** — and *that* is the lesson. After the partnership: she calls the floor "ours."

**§7 · Anti-patterns.** **Keep her light** — a vivid flavour, not a central figure; do not inflate her. **No
player↔Lorna sex, ever.** The caught-with-a-customer beats are **voyeuristic only.** Don't let her corrupt the
**family** — that's yours alone. And keep her an **ally**, never something you own.

**§8 · The build correction (not a role change — a SHAPE change).** *(This is the actual v1 failure, and it
is the whole reason she's being re-written.)*

v1 gave her 5 canvases and **4 of them fire exactly once**: meet her · take the books · the Grayson tip · the
partnership. After a couple of hours she was a woman standing behind a bar with nothing left to say — and
**the structural on-ramp died with her.** The two things that would have made her a person (the escalating
lessons, and the mirror) were **never built at all.**

Same light budget. Spent differently:
- her hub is **repeatable and TIERED**, escalating with the business — she always has the *next* idea;
- the **mirror beats** exist, recurring, through the whole game;
- she is still there, and still saying things, in Act 3.

**§9 · Acceptance (story).** Done when: she is the **one genuine ally** (a partner you respect, never own,
never bed); her function reads clearly (**she teaches you the trade**, and she is your eyes and ears); **the
mirror lands** (you catch what you're becoming, already arrived, and she isn't ashamed); and she stays
**light** — a flavour, not an arc — while remaining **alive to the last day of the game.**

---

### The world (Step 4 · §5)

> The stage already exists (Step 2b: 20 rooms, each with a job). This pass gives each place its **story** —
> the feel of its public, its clock, its ceiling, and who can be seen through which door.

**§5A · What each place is FOR — and which track lives there.**
The room-content gate was passed at 2b. What matters here is the **split**: the work she does **alone** and
the person she works **on** share rooms in this house, and they stay **separate things to do** — never blurred
into one menu.

| Kind of place | Which |
|---|---|
| **The earning / being-seen stage** | the Lobby · the Bar · (later) the Private Floor |
| **The private room where one person opens up** | each bedroom · the Study (Richard) · the Drawing Room (Margaret) |
| **The lawless deep end** | the Private Floor |
| **The shop where money goes to die** | the Boutique · the Adult Shop |
| **The shared hub everyone passes through** | the Residence landing · the Kitchen · **the Grand Stair** |

*(All five kinds exist. None missing.)*

**§5B · The ceiling — how far each place lets the world go.** *(Owner of where forced content is allowed.)*

| Place | The worst/hottest thing that can happen here | Forced (can't-refuse) allowed? |
|---|---|---|
| **The Lobby** | stares · comments · a hand on the small of the back in passing | **early only** — a guest's hand, and you're staff, and you swallow it |
| **The Bar** | a liberty *offered* — refuse or accept | **early only** |
| **The Guest Rooms** | anything, behind a closed door — this is where a favour has somewhere to happen | yes, act-scoped |
| **The Residence** (family floor) | **milder, and worse for it.** It's home. That's what makes it land | **Grayson, early** — the doorway, the bath |
| **The Upstairs Bath** | walked in on · walking in · caught | **yes, early** (§5H) |
| **The Private Floor** | **lawless.** The ceiling is whatever she'll sell | no — by the time it's open, **she is not prey** |
| **Town / the street** | a look, a word, a follow — a *different* ceiling: strangers, not staff | no |

**The forced mode is ACT-SCOPED and it RECEDES.** Early, while she's nobody, the world takes what it wants.
As she rises, it stops — and the stopping is the payoff. **The Private Floor never allows it**, because by the
time she owns that floor nothing in this building takes anything from her.

**§5C · The reactive public — who else is looking.** Beyond the named cast: **the guests** (the ones who tip,
the one who signs, the one who assumes), **the staff** (who watched her grow up and now watch her carry
drinks), and **the street**. Dispositions are *not* one flat "everyone gropes her":
- **The predator** — the regular who reads a comped room as a transaction and is right.
- **The prude** — the old staffer who goes red and looks away, and whose disappointment costs her something.
- **The opportunist** — the guest who won't start anything but won't refuse it either.

**One outfit, three rooms:** in the **Lobby** it earns her tips and a comment. In the **Kitchen** at midnight
it makes Richard look at the floor and Grayson look too long. On the **Grand Stair** it catches her between
her two selves and someone's coming down. *Same dress. Three different scenes.* If it isn't three different
scenes, the ceiling model is broken.

**What goes wrong:** she can be **seen by the wrong person** — and in this house the wrong person is
**Margaret**, who says nothing and **files it** (§4). That is the real downside of exposure here: not a fine,
not a robbery — **leverage**, accumulating quietly in someone else's hands.

**§5D · The clock — who's here, and when.** Everyone lives in this building, so *"is he home right now"* is a
real fact her routines roll against — never décor, never an offscreen label. **Richard** haunts the Study late
and the Kitchen at odd hours. **Margaret** holds the Drawing Room by day and is *behind the desk* in the
mornings. **Grayson** is nocturnal, useless, and everywhere he shouldn't be. **Audrey** studies, and is out at
college by day — the one person with a real "away." **Lorna** is at the Bar every evening until close.

**§5E · Cadence & pressure.** The climb is measured in **days and small steps**; nobody is maxed out in an
afternoon. **The pressure is not a clock** — there is no fail-state (§8). What makes the days urgent is that
**Margaret is winning them.** She holds court, she gives your mother's staff their orders, and every day you
don't move is a day she does. *Pressure by wanting, not by threat.*

**§5F · The phone & the sidebar.** The phone carries what lives nowhere else: **chat threads that change tone
as people fall** (Audrey's get eager; Grayson's get desperate; Richard's get shy), the **photo-sale economy**
(her second income), and **leverage that lives on a screen** — a picture she doesn't delete. The sidebar
carries the portrait, the money, the day, and each person's **named next step with its place and time-window**.
**Hidden:** Margaret's scheming track. The player must never see a bar labelled "how much she's banked" —
finding out is the scene.

**§5G · Access.** Day one she can walk into the whole hotel, the whole residence, and the street. **Two doors
are shut and she can SEE they're shut:** the Back Office (until Richard hands over the ledger) and the Private
Floor (until she controls the hotel and pays for it). Both say *why* on the door. Nothing in this game
silently appears.

**§5H · Shared private space — CONFIRMED per place (Mode A, LO).**

**All four are in play.**

- **The Upstairs Bath — all three directions.** One door, and it has never locked.
  - *You walk in on them* — **Richard** (mortified, and slower to leave than he should be) · **Grayson** (who
    doesn't care, and says so) · **Audrey** (unbothered — it's just her sister).
  - *You find it occupied* — the room itself tells you who's behind the door.
  - *You are caught in there yourself* — **early, that's a liberty you can't refuse** (Grayson: *"door was
    open"*). **Late, you left it open on purpose.**
- **Audrey's room — the "homework."** Her door isn't quite shut and she's practising what you taught her. You
  hear it before you see it. Early it's an accident. Later **she leaves the door open**, and neither of you
  says so. *(Her lesson ladder, bleeding out of the scenes and into the house.)*
- **Your own room — Grayson doesn't knock.** You are the one walked in on. No knock, no apology, and early
  **nothing you can do about it** — the prey floor, in the one room that should be yours. It recedes as you
  rise, and by the end **he stands in the doorway waiting to be told he may come in.**
- **The guest rooms — you catch Lorna.** A door not quite shut after close. She catches your eye, **winks, and
  doesn't stop.** Voyeuristic only — you are never pulled in. Nothing changes afterwards, and *that is the
  lesson.*

---

### Reactivity as experience (Step 4 · §4)

> What becomes *different* when something changes — named as felt moments, so the Blueprint has something to
> wire. (The flags, deps and the DAG are Step 5's.)

**When SHE crosses a band.** The world doesn't announce it — **it stops flinching.** The comment that would
have made her go still last week gets an answer. The dress she couldn't have worn is just what she's wearing.
And the thing she notices, quietly, is that **she chose it this time**, and she can't pretend otherwise.
*(Her portrait in the sidebar changes. Nobody mentions it. That's the point.)*

**When SHE is seen.** Exposure is never free in this house, and it isn't a fine — **it's evidence.**
Margaret sees, and says nothing, and **keeps it.** The player should feel the file thickening long before it's
opened.

**When AUDREY falls.** The greeting changes first — she stops waiting to be found. Then the door starts
closing *behind* you instead of in front of you. Then she stops calling it practice. And once **Danny is in the
house**, the whole board changes: the group content opens, and Audrey is the one who suggests it, cheerfully,
because *why wouldn't we.*

**When GRAYSON breaks.** The doorway stops being a threat and becomes a place he *waits*. He can't meet
Margaret's eyes. And when you take his father, his aunt, and his sister — **he holds your coat.**

**When RICHARD falls.** He eats. He shaves. **He goes to work** — the hotel physically comes back to life
because a man wants to impress you, and you can *see it in the rooms.* Then he brings you the books unasked.
Then he hands you the keys — and **the moment he signs, Margaret's ground disappears from under her**, and she
knows it before anyone tells her.

**When the men fall, MARGARET feels it — before she's told.** This is the machine, felt: she notices Grayson
can't look at her. She notices Richard is *working*. She comes to your room at midnight to talk, and it does
not go the way she planned. **The apex isn't gated behind the men as a mechanism — it's gated behind them as a
story:** breaking them is what leaves her with nobody to scheme through.

**When SHE takes someone, who else reacts.** This house is small. Audrey thinks the family has never been
closer. Grayson watches. Lorna knows and says nothing, except once, with her eyes. **Margaret files it.**

**When she LOSES ground.** *(§4F — the fail-state declaration, carried down from Step 2.)* **Failure does not
exist, by design.** Nothing is ever confiscated: no room closes, no arc is lost, no deadline takes the hotel.
Neglect a person and they cool. Neglect the house and **Margaret gains a step** — and you watch her take it.
**The negative axis is STATUS, never property.** The only thing that gets worse is how far ahead she is, and
erasing that is the want that drives the entire game.

**At the top.** The floor still runs. The private floor still pays. The household still serves. Her favourite
loops all still work, and the tracker says so honestly — *you've reached the current peak; run your house* —
and somewhere across the city, a rival has heard what this place has become.

---

## Blueprint (Step 5) — the gated, placed, ordered scene list

> **Generated FRESH from the Step-4 story.** v1's scene list is NOT consulted — it is the corridor we're
> replacing (47% one-shots · 7 Lane-2 ambients total · 88/102 nodes choiceless). The budget set at casting —
> **~125–170 canvases** — is held here so the structure can't shrink back into that corridor.
>
> STRUCTURE only. No prose, no TOML (those are Step 7).

### Player blueprint (Step 5 · §2) — the self-corruption track + the feeder economy

#### The spine — the meters and their bands

- **`corruption` (0–100, the DOOR)** — how far she'll go. **Never falls.** Four bands, each opening a KIND of
  act for her AND the whole household at once (the door half of the double lock):
  | Band | Range | The kind of act this door opens |
  |---|---|---|
  | **Pure** | 0–24 | non-lewd warmth; the first *charged* line — a held look, a coached "say it" |
  | **Lewd** | 25–49 | heavy petting, oral, the first transactional favour; clothes-off display |
  | **Slutty** | 50–74 | full sex; escort work; taking a family member to bed |
  | **Whore** | 75–100 | anal, group/threesome, the private-floor headline acts, the forced apex |
- **`exhibitionism` (built-in, clothing-read)** — the RATCHET; only climbs. Read off `worn_corruption`; gates
  floor/public content + what paid floor work she can take. **Never gates a family arc** (clothing two-part
  rule).
- **`arousal` (0–10, LIGHT throttle)** — is she worked up right now. Gates in-the-moment repeatable acts
  (get herself off; warm into a loop pose); **resets to 0 at climax** (author-emitted). **Never** unlocks a
  tier — that's `corruption` alone.
- **`money` + `energy`** — the leverage fund + the daily clock. **No `renown`** (the house's growth is gated
  on upgrades + flags + corruption, not a meter).

> **Clamp discipline (the vanishing-HUD lint).** Every `op=add` on a banded body-need/resource stat
> (`energy`, `money`) **clamps into its declared range** — an unbounded value leaves its bands and the sidebar
> card silently disappears (reads as a *missing* HUD element, not a wrong number). **The only body-need stats
> are `energy` (0–100) and `money`; there is no `hygiene` stat** (see the fused hosts — the bath restores
> energy).

#### The scene list — lane · what it is · gate · place · pays

**Bootstrap (Pure — night one):**
| Handle | Lane | What it is | Gate | Place |
|---|---|---|---|---|
| `p_solo_channel` | solo feeder | the channel nobody admits to (TV / phone) | corr 0 · +arousal | your room |
| `p_solo_mirror` | solo feeder | try the bolder thing on, look | corr 0 · +exhib | boutique · your room |
| `p_solo_off` | solo feeder | get herself off | **arousal ≥ 4** · resets arousal | your room |

**The daily-routine hosts — FUSED UNITS** (chore + solo feeder + walk-in are ONE canvas; the walk-in `chance`
climbs by corruption band):
| Host | Restore | Solo feeder branch | Walk-in (Lane 3, `requires_npc` + banded chance) |
|---|---|---|---|
| `p_sleep` | energy (rolls the day) | the channel · the phone · her hand | **Grayson** — doesn't knock (chance rises Pure→Slutty, then he's *invited*) |
| `p_bath` | energy *(no `hygiene` stat — it gated nothing; energy is the restore)* | her hands, in the water | **Grayson** ("door was open") · **Richard** (mortified) · **Margaret** (files it) |
| `p_eat` | energy | — | whoever's up, unarmored (Richard / Audrey / Grayson) |

**The income ladder — the fall made literal** (better money always further down; each rung a real scene):
| Handle | Lane | What it is | Gate | Place | Pays |
|---|---|---|---|---|---|
| `p_floor_hostess` | earn (repeatable) | a plain hostess shift | corr 0 | lobby · bar | ~$15 |
| `p_floor_bold` | earn / exhib rung | the shift in the lower-cut thing; stares → tips | corr ≥ 15 · bold outfit | lobby · bar | ~$40 + tips |
| `p_floor_display` | earn / exhib rung (Slutty escalation of `p_floor_bold`) | not just dressed bold — *put on display*: a guest's table, a lap, the bar top; she's the show now | corr ≥ Slutty · barely-outfit | lobby · bar | ~$120 + tips |
| **`p_take_purse`** ⭐ | **the hinge scene** | you take the hotel's books in hand — Lorna shows you where the money went, and you stop asking Richard and start deciding. **SETS `hotel_in_hand`** (the flag Richard's "keys" + Grayson's "deal" both read) | `lorna_books` (Lorna showed you the books) · money floor (you can cover a week of staff) | back office door / the bar | — |
| `p_floor_favor` | earn (transactional) | comp a guest a room for a "favour" — the first line crossed | corr ≥ Lewd · Lorna's idea (flag) | guest rooms | ~$150 |
| `p_floor_escort` | earn (transactional) | a paid escort arrangement | corr ≥ Slutty · escort upgrade | guest rooms · private | ~$400 |
| `p_floor_private` | earn (ceiling — 3 sub-rungs: client → regular → **headline**) | private-floor service; the dirtiest, best-paying thing she does; **her ceiling** (anal/group, *earned*) | corr ≥ Whore · `richard_signed` · private-floor upgrade | private floor | $800 / $1.5k / $3k |
| `p_phone_photos` | earn (alt path, anti-grind) | sell photos off the phone; tiers scale with corruption/exhib | corr ≥ 25 (t1) / 50 (t2) / 75 (t3) | anywhere (phone) | $20 / $50 / $120 |

**Reactive-world ambients** (`worn_corruption` × place ceiling; Lane 2 — the PUBLIC content clothing is
allowed to gate):
| Handle | Place ceiling | What it is |
|---|---|---|
| `p_react_lobby` | civil-public | stares, comments, a hand in passing |
| `p_react_bar` | semi-permissive | a liberty *offered* — refuse or accept |
| `p_react_rooms` | lawless | open liberties (guest rooms / private floor) |

#### Pacing the repeatables (never free + instant — the Vesper-Renner break)

- **Floor work** is throttled by **`energy` `costs`** — each shift spends energy, restored by sleep → ~a loop
  a day, not a spam button. Corruption gain per shift is small and **band thresholds are spaced ~×2.5**
  (Pure→Lewd is quick; Slutty→Whore is the long climb) so the fall is measured in days, not an afternoon.
- **Solo `p_solo_off`** is throttled by the **`arousal` gate** (must be worked up) + arousal resets at climax.
- **Photo tiers** are throttled by a **daily cap** (`max_triggers_per_day`) + the corruption gate.

#### The economy made real — sinks + key items

**One wallet.** Income is the corruption ladder above. **Pressure is WANT, not a clock** (no fail-state):

- **Clothing** (the reactive dial) — ~$50–300 per bolder piece. Access to the outfit *is* the exhibition
  progression.
- **Hotel upgrades** — ~$500–2,000; each transforms a room and unlocks a new KIND of service (discreet rooms
  → escort; the private-floor build → the headline slot).
- **The family hooks** (a corruption hook, never charity): **Audrey's tuition** (~$800, the arc's opening
  move) · **Richard's debts** (scaling, covering-him-is-owning-him) · **buying out Grayson** (clears his
  bookies, sets the servitude flip).
- **Key items** (adult shop; each gates content, locked-visible — LO's picks):
  | Item | Cost | Unlocks |
  |---|---|---|
  | **The toy** (+ later a **strap**) | ~$60 / $120 | Audrey's lesson-ladder "toy" rungs; the things she practices on you |
  | **The intoxicant** | ~$200 | Margaret's **breaking** (you intoxicate her); eases other hard-gated beats. *(Drug, on the shelf — not liquor, not under-the-counter.)* |
  | **A gift** | varies | deepens a hook materially (a thing for Audrey / Richard) |

#### Feeder count — band by band (§2E, the anti-starvation seed — LO: 2–3 live per band, EVERY band)

| Band | Her own live feeders | count |
|---|---|---|
| **Pure** | the channel · the mirror · hostess shift | **3** |
| **Lewd** | bold floor · comp-a-favour · photos t1 · the bath feeder | **4** |
| **Slutty** | escort · photos t2 · **`p_floor_display`** (put on display — a real handle now) | **3** |
| **Whore** | private floor (×3 sub-rungs) · photos t3 · **her ceiling (the headline slot)** | **3+** |

**No band dead-ends.** Her fall is a full arc you could play with the family barely touched — which is what
makes the double-lock converge *honestly* (her corruption opens the family doors having got there through her
OWN content, no grinding). *(Closed for real at the end of Pass 2, against the deepest NPC floors.)*

#### Day-breadth (§2F — is a mid-game day more than one thread?)

A representative Act-2 day has, live and non-grind: **self-care** (the bath, the bed) · **being seen** (a bold
shift) · **a second economy** (the phone) · **the house changing** (a room coming back) · **whatever walks in
on her** · and **four people to work.** **≥2–3 non-grind threads, comfortably.** The day is never only the
grind.

### Audrey blueprint (Step 5 · §3) — entry target + gateway · family/ambient, dense · ~28 scenes

**Spine:** `audrey_corruption` odometer (the individual lock) + `audrey_arousal` throttle (re-warm per
session). **Double lock** on every lewd rung: your `corruption` band (the door) + `audrey_corruption ≥` the
rung (built by the lessons). **Non-lewd on-ramp is UNGATED** (trust is Act-1 parallel work).
**Lane mix:** L1 7 · L2 5 · L3 13 (**~46%, the dominant lane**) · L4 5 = **30**, sex-loop menu after.

#### Lane 1 — the lesson hub (escalation rungs she clicks)
| Scene | Gate (double lock unless noted) | Place |
|---|---|---|
| `aud_hub` (base talk — presence floor) | **ungated** | wherever she is |
| `aud_tuition` (the confession — non-lewd hook; SETS `audrey_tuition_paid`) | **ungated** (money sink, not corruption) | your room · kitchen |
| `aud_lesson_kiss` (kissing — on you) | corr ≥ Lewd · `aud_c ≥ 2` | her room |
| `aud_lesson_toy` (the toy — needs the **toy** item) | corr ≥ Lewd · `aud_c ≥ 4` · owns toy | her room |
| `aud_lesson_down` (going down — toy then you) | corr ≥ Slutty · `aud_c ≥ 6` | her room |
| `aud_coax_1/2` (the "say it" rungs — the crude word coaxed out; the coaxing IS the content) | interleaved w/ lessons | her room |

#### Lane 2 — ambients (re-readable, fire across the arc)
`aud_amb_study` (the book she isn't reading) · `aud_amb_phone` (Danny call, goes quiet) · `aud_amb_bath`
(coming out) · `aud_amb_morning` (the greeting, warming by tier) · `aud_amb_kitchen` (unarmored, late).
*(This is the band v1 gave her ZERO of. It is not optional — it is the arc-shape.)*

#### Lane 3 — the "homework" (the DOMINANT lane, ~13) — walk-ins + the fused hosts hijacked
- **Her practicing** (the door not quite shut → later deliberately open): a banded chain — corr-gated
  `chance` climbs; early = accident/embarrassed, late = she wants you to see. (~5 tiers)
- **The bath host** (`p_bath` hijacked by Audrey): walk in on her; she's unbothered — it's just her sister.
- **Her room** at escalating tiers (the "homework" hijack of the sleep/solo loop). (~4)
- **Caught doing it in a shared space** once corruption's high — she doesn't stop. (~2)

#### Lane 4 — the big nights (capstones)
| # | Capstone | Trigger | Sets |
|---|---|---|---|
| 1 | **"You fix everything"** (tuition) | `audrey_tuition_paid` | `aud_trust` |
| 2 | **"The first lesson"** | corr ≥ Lewd · `aud_c ≥ 2` · `aud_trust` | `aud_lessons_open` |
| 3 | **"The first night"** | corr ≥ Slutty · `aud_c ≥ 8` | **`audrey_stage ≥ surrendered`** |
| 4 | **"She got the boy"** (Danny lands — her genuine win; Danny now visits the house) | `aud_lessons_open` + days | `danny_here` |
| 5 | **"Study group"** (Wave-1 threesome: you + Audrey + Danny) | `audrey_stage` + `danny_here` | `group_open` |

#### The gateway — TWO WAVES (LO: staged)
- **Wave 1 — needs Audrey ONLY.** She lands Danny → *"Study group"* (you + Audrey + Danny). Her arc pays
  off on its own terms; the group content's first taste needs no one else.
- **Wave 2 — needs Audrey AND the man** (Form 1 cross-wire, respects D1 — can't fire before he's broken):
  - `audrey_stage` **+** `richard_stage ≥ open` → **Audrey + Richard + you** *(father & daughter; LO-confirmed)*
  - `audrey_stage` **+** `grayson_stage ≥ heeled` → **Audrey + Grayson + you** (he's the lowest body in it)

#### Wiring (§8)
- **SETS:** `audrey_tuition_paid` · `aud_trust` · `aud_lessons_open` · `audrey_stage` · `danny_here` ·
  `group_open`.
- **READS (cross-gate, telegraphed — D3):** `richard_stage`, `grayson_stage` for the Wave-2 threesomes
  (*"Audrey's happy to share — but Richard has to be yours first"*).
- **D1** ✓ entry (`aud_hub`/`aud_tuition`) ungated. **D2** ✓ she only READS the men (never a mutual lock).
- **Media:** establishing — her at the kitchen table; the hot beats — the lesson clips (image-first).
- **Sex-loop menu** opens post-"first night": the repeatable explicit layer (poses at her `audrey_corruption`
  tier + `audrey_arousal` throttle).

#### Per-NPC self-check
Spine fits family/ambient (odometer + throttle, no dead meter) ✓ · double lock on every lewd rung ✓ ·
Lane 3 is dominant (~46%, the fix for v1's zero) ✓ · the gateway respects D1 (Wave 2 can't precede the men) ✓
· depth matches casting (dense, not gold-plated — she's *supposed* to be the biggest) ✓.

### Grayson blueprint (Step 5 · §3) — core target + prey-phase predator · family/ambient, dense · ~27 scenes

**Spine:** `grayson_sub` odometer (his brokenness — built by repeated servitude) + `arousal` throttle for the
repeatable use. **The reversal is mechanized:** the prey-floor scenes do NOT gate on his meter — they gate on
YOUR low power, and recede as you rise. **Double lock** on the servitude/use rungs: your `corruption` band +
`grayson_sub ≥` the rung. **Lane mix:** L1 7 · L2 5 · L3 11 (**~41%, dominant**) · L4 4 = **27**, sex-loop
(femdom) after. *(His ambient life is Lane-2 atmosphere — enumerated below in its own section, not double-counted inside Lane 3.)*

#### THE HINGE — a hard flip at "The deal" (LO)
```
PREY PHASE  ── forced liberties; chance ALREADY fading as corruption/power rises
     │
 "THE DEAL" (capstone) ── he comes broke, bookies on him; you name servitude as the price
     │  SETS grayson_flipped
     ▼
SERVITUDE   ── grayson_prey OFF forever (no forced liberty ever again); the ladder begins
```
**One clean turning point:** the last time he touches you without permission is the scene *right before* he's
on his knees. The reversal lands because it has a moment.

#### Lane 2 — his ambient life (re-readable atmosphere; runs the whole game, ~5)
`gray_amb_furniture` (feet on your mother's furniture in the drawing room) · `gray_amb_fridge` (the 2 a.m.
fridge) · `gray_amb_phone` (the low phone call he cuts off when you enter) · `gray_amb_watch` (**watching his
sister hostess** from the bar, hating it) · `gray_amb_sprawl` (post-flip: underfoot, finding reasons to be
where you are). *(Location-entry ambient — you walk in and he's there; distinct from the Lane-3 walk-ins,
which fire on YOUR activity.)*

#### Lane 3 — the prey floor + servitude walk-ins (the DOMINANT lane, ~11) — fire on YOUR activity
- **Forced liberties (prey — act-scoped, auto-fire, no refuse; chance fades with your power, HARD-OFF at
  `grayson_flipped`):** the doorway walk-in (doesn't knock, on your sleep/solo host) · the bath ("door was
  open") · a hand on the floor in passing · cornered on the Grand Stair · the boldest, once (the scene right
  before the flip). (~6)
- **Post-flip servitude walk-ins** (he interrupts your routines to serve, at escalating `grayson_sub` tiers):
  he brings you things · kneels while you work · is used on command mid-chore · the cuckold walk-in (you're
  with someone, he holds your coat). (~5)

#### Lane 1 — the servitude hub (post-flip rungs she clicks)
menial (fetch/carry/kneel) → degrading (beg/mocked/serve-in-front-of-others) → **use** (denial, ruined,
chastity; **pegging** — needs the strap; **cuckold/made-to-watch**) → free service. Gated: `grayson_flipped`
+ your `corruption` band + `grayson_sub ≥` rung.

#### Lane 4 — the capstones
| # | Capstone | Trigger | Sets |
|---|---|---|---|
| 1 | **"The deal"** | broke (`grayson_debt_known` via Lorna) · **`hotel_in_hand`** · your power floor | **`grayson_flipped`** (prey OFF) |
| 2 | **"On his knees"** | `grayson_flipped` · corr ≥ Slutty · `grayson_sub ≥ 4` | first use · **`grayson_stage = heeled`** (opens Audrey Wave-2) |
| 3 | **"He stops pretending"** | `grayson_sub ≥ 7` | deepest humiliations open |
| 4 | **"Yours for nothing"** | `grayson_sub ≥ 10` (freely given) | **`grayson_bought_out`** (feeds Margaret's apex gate) |

#### Wiring (§8)
- **SETS:** `grayson_flipped` · **`grayson_stage = heeled`** (at "On his knees" — for Audrey's Wave-2
  threesome) · **`grayson_bought_out`** (→ Margaret's apex).
- **READS (telegraphed — D3):** `grayson_debt_known` (Lorna's tip) · **`hotel_in_hand`** (the flip needs you
  holding the money — set by `p_take_purse`). Cuckold/watch scenes READ the other arcs' stages (he's made to
  watch you take them).
- **D1** ✓ his entry is his *ambient presence* (ungated — he's in the house from hour one; the prey liberties
  are act-scoped, not an on-ramp gate). **D2** ✓ he only READS the debt flag + others' stages.
- **Media:** establishing — feet on the furniture, the sneer; hot beats — the femdom/servitude clips.

#### Per-NPC self-check
Density in Lane 3 (~48%, correct for his shape) ✓ · the reversal has a hard felt moment (`grayson_flipped`)
✓ · forced content is act-scoped and hard-recedes (never a permanent no-refuse) ✓ · "don't break him fast" —
the ladder is repeated servitude (`grayson_sub` odometer), not a one-beat fold ✓ · the early groping never
reads as HIS win (it's the floor that earns the payback) ✓.

### Richard blueprint (Step 5 · §3) — core target + will gatekeeper · slow-burn family, SPARSE · ~13 scenes

**Spine:** `richard_want` odometer (his guilty wanting) + `arousal` throttle. **Double lock** on lewd rungs:
your `corruption` band + `richard_want ≥` rung. Non-lewd companionship (sit with him, get him eating) is
**ungated** — that's the whole on-ramp. **KEEP HIM TIGHT** (10–15; sparse-and-concentrated is the shape — do
NOT pad him to match the dense arcs). **Lane mix:** L1 4 · L2 2 · L3 3 · L4 4 = **13**, gentle loop after.

#### Lane 1 — the companionship→wanting hub
`ric_sit` (sit with him — **ungated**, gets him eating, the on-ramp) → `ric_confide` (he leans on you;
non-lewd trust) → `ric_charge` (the comfort turns warm — the lingering touch) → `ric_pursue` (he throws
himself at the hotel to earn your company; each visit warmer). Gated: player band + `richard_want`.

#### Lane 2 — ambients (2, sparse)
`ric_amb_study` (the lamp on at 3 a.m.; later — in shirtsleeves, working, looking up when you pass) ·
`ric_amb_kitchen` (the glass he hasn't drunk from).

#### Lane 3 — discrete revelations (3, walk-ins that reveal, not routine)
the bath (mortified, slower to leave than he should be) · the study (the deed in the open drawer — you *see*
what he holds) · asleep in a chair (you cover him; the tenderness that's also the leash).

#### Lane 4 — the capstones
| # | Capstone | Trigger | Sets |
|---|---|---|---|
| 1 | **"Back to life"** | corr ≥ Lewd · `richard_want ≥ 3` · trust | first charge |
| 2 | **"The first night"** | corr ≥ Slutty · `richard_want ≥ 6` | **`richard_stage ≥ open`** (Audrey Wave-2) |
| 3 | **"The keys"** | `richard_want ≥ 8` · **`hotel_in_hand`** (set by `p_take_purse`) | **`richard_signed`** ⭐ (Margaret apex + private floor + back office) |
| 4 | **"At your side"** → **"The child"** *(terminal; the supplanting payoff)* | `richard_signed` · Whore-era · **player chooses** | `richard_pregnant` (portrait suffix; the pregnancy system, Pass 3) |

#### Wiring (§8) — the machine's keystone
- **SETS:** `richard_stage` (Audrey Wave-2) · **`richard_signed`** — the single most load-bearing flag in the
  game: it strips Margaret's claim (her apex gate), unlocks the **private floor** + the **back office**, and
  is the hinge of the core loop.
- **READS:** the hotel-taken-in-hand flag (the keys need you already running the floor). D3-telegraphed
  (*"he trusts you with the hotel before he trusts you with the deed"*).
- **D1** ✓ entry (`ric_sit`) ungated. **D2** ✓ he SETS the keystone, READS only the hotel flag — no cycle.
- **Media:** establishing — the 3 a.m. lamp; hot beats — tender, the handover.

#### Per-NPC self-check
Spine fits slow-burn (odometer + throttle) ✓ · **SPARSE, not padded** (13, capstone-heavy — the shape,
respected) ✓ · the handover reads as WILLING (earned by `richard_want`, never coerced) ✓ · no
Eleanor-impersonation anywhere (the child is *supplanting*, method-clean) ✓ · his register stays tender,
never pathetic ✓.

### Margaret blueprint (Step 5 · §3) — APEX + pressure source · family/ambient, dense · ~26 scenes · destroyed, NOT seduced

**Spine (SPECIAL — no seduction meter).** There is no "seduce Margaret" odometer. Two mechanisms instead:
- **`margaret_leverage` — HIDDEN** (§5F: the player must NEVER see it; finding out is the scene). Rises when
  she catches you; spent on her Act-2 moves.
- **The breaking's "individual lock" is the MEN, not her willingness:** the apex gate is
  **`richard_signed` + `grayson_bought_out`**. *Breaking the men IS the lock on Margaret.* She is
  **untouchable until everything else is taken** — that's what makes her the real final boss.

**Lane mix:** L2 4 · L3 11 (she-catches-you + her ambient life, **~42% dominant**) · Act-2 moves 6 · L4 5 =
**26**. **No sex-loop menu** — her only sexual content is the one-and-done breaking + the terminal slave loop.

#### Lane 3 — SHE catches YOU + her ambient life (the dominant lane, ~11)
- **She catches you** (inverted Lane 3 — `requires_npc` Margaret present ∩ you in a compromising state; each
  RAISES the hidden `margaret_leverage`, and she says *nothing*): on the floor in the bold thing · coming out
  of a guest room · with Audrey · coming out of the bath. **She looks, and keeps it.** (~6)
- **Her ambient life:** in your mother's chair · holding court in the drawing room · counting the silver with
  a list · on the phone to a lawyer, unhurried about hanging up · behind the front desk giving your mother's
  staff their orders · watching you across the lobby over a glass. (~5)

#### The Act-2 offense — she SPENDS what she banked (~6; LO: soft temporary setbacks, nothing taken)
Each move **FIRES on a staggered `margaret_leverage` threshold** (this is the spend side of the meter — she
can't move until she's banked enough on you; that's why catching you *matters*). Each sets a **temporary
condition flag** (NOT an odometer decrement — engine-honest, and the clawback is content):
| Her move | Fires at | The soft setback (a knot you untie) | Cleared by |
|---|---|---|---|
| takes it to Richard | `margaret_leverage ≥ 2` | `richard_cooled` — his warm content gates OFF | a re-warm scene (content) |
| turns the staff | `margaret_leverage ≥ 3` | `staff_cold` — floor tips dip | a win-them-back floor scene |
| works Audrey | `margaret_leverage ≥ 4` | `audrey_skittish` — Audrey wary a few days | reassure her (content) |
| has your things moved out of your mother's room | `margaret_leverage ≥ 5` | a status jab — you move back in | a reclaim beat |
**Nothing is ever GONE. Everything is HARDER, briefly.** You feel her winning; you never lose the game.
*(The catch→bank→SPEND loop is now closed: catches raise the meter, thresholds fire the moves.)*

#### Lane 2 — the cold war presence (4)
velvet-over-steel exchanges — she compliments like a threat, never crude, always a step ahead. Re-readable;
the rising menace.

#### Lane 4 — the apex chain
| # | Capstone | Trigger | Sets |
|---|---|---|---|
| — | **"She watches too long"** (the turn — once; contempt with a hot edge, she'd deny it) | mid-war, high `margaret_leverage` | flavor → makes the breaking worse |
| 1 | **"Velvet and steel"** (the war's peak threat) | Act-2 mid | — |
| 2 | **"The board turns"** (her advantage collapses — she feels it before she's told) | **`richard_signed` + `grayson_bought_out`** | `margaret_cornered` |
| 3 | **"The breaking"** (ONE-AND-DONE forced 3-on-1: intoxicate her; the two men she commanded — now yours — take her) — **carriage: PLAYED** (see §2: the shatter gets a spoken line, *not* narrated summary — Rule 4 at the apex) | `margaret_cornered` · **intoxicant item** · corr ≥ Whore | `margaret_broken` |
| 4 | **"The family slave"** (terminal: communal servitude; put to work on the vice-floor she schemed to own) — the emptied-out silence lives HERE, where wordlessness is the point | `margaret_broken` | frontier |

#### Wiring (§8) — the machine's payoff
- **SETS:** `margaret_leverage` (hidden) · the Act-2 setback flags · `margaret_cornered` · `margaret_broken`
  (a frontier trigger).
- **READS (the apex gate — D3-telegraphed loud):** `richard_signed` **AND** `grayson_bought_out`
  (*"Margaret won't be moved while Richard holds the deed and Grayson still has a spine"*). **The Act-2 moves
  READ `margaret_leverage`** (staggered thresholds — the spend side of the meter). The catches READ your
  missteps (the compromising-state).
- **D1** ✓ her entry is her ambient presence (ungated — she's behind the desk on frame one; the WAR is her
  on-ramp, and it's cold-start-available). **D2** ✓ she READS the men's flags; the men never read hers → no
  cycle. **The apex gate is the machine's keystone dependency** — checked acyclic at Pass 4.
- **Media:** establishing — Margaret in your mother's chair; the breaking — the forced 3-on-1 (all adult).

#### Per-NPC self-check
Reads as ANTAGONIST not seduction (the war is the through-line — the fix for v1's climb-less arc) ✓ · the war
has REAL RUNGS (catch → bank → spend → claw back, over and over) ✓ · she stays formidable to the end (the
apex gate means she can't be reached early) ✓ · the breaking is ONE-AND-DONE (never a repeatable rape) ✓ ·
her scheme track is HIDDEN (§5F) ✓ · dense budget met by the WAR, not padded seduction ✓.

### Lorna blueprint (Step 5 · §3) — corrupting on-ramp + ally + mirror · service, LIGHT · ~9 scenes

**No spine odometer** (peripheral — she isn't seduced; `relation` flavor only). The whole fix vs v1 is
**SHAPE: her hub is REPEATABLE and TIERED, not four one-shots.** **Lane mix:** service has no Lane 2/3 ladder;
her content is a tiered hub + the recurring mirror + the structural scenes. **~9**, and she's alive to the
last day.

#### The tiered hub (ONE repeatable canvas that swaps its offer as the business grows)
She always has the **next idea** — the offer tiers on story flags, never a dead end:
| Tier | Her line | Unlocks / gates on |
|---|---|---|
| 0 | *"There's a guest in 12 who tips if you're friendly."* | corr 0 (the on-ramp) |
| 1 | *"Comp him the room, he'll pay it back twice."* | → **`lorna_favor_idea`** (opens `p_floor_favor`) |
| 2 | *"I know girls who'd work a floor like this."* | escort upgrade era |
| 3 | *"That top floor's been empty a long time."* | `richard_signed` (the private floor) |

#### The mirror (recurring — voyeuristic ONLY; the thing v1 designed and never built)
`lorna_mirror` — you catch her with a customer (behind the bar after close · a guest room, door not quite
shut). She catches your eye, **winks, and doesn't stop.** Fires a few times across the game; **nothing
changes afterward, and that IS the lesson.** Never pulls the player in.

#### The structural scenes
`lorna_meet` (she sizes you up — the intro) · `lorna_books` (she shows you where the hotel's money went →
SETS `lorna_books` = true, the prerequisite for the player's `p_take_purse` scene that SETS `hotel_in_hand`) · **`lorna_debt_tip`** (Grayson's gambling — SETS `grayson_debt_known`; *the knife
handed to you by the one person on your side*) · **"The partnership"** (the ONE big night — non-sexual; she
throws in as your right hand; SETS `lorna_partner`).

#### Wiring (§8)
- **SETS:** `lorna_favor_idea` (→ the comp-a-favor income rung) · **`grayson_debt_known`** (→ Grayson's flip)
  · **`lorna_books`** (→ the player's `p_take_purse` → `hotel_in_hand`) · `lorna_partner`.
- **D1** ✓ ungated on-ramp (Tier 0 from corr 0). **D2** ✓ she only SETS (never gated on another arc).
- **Media:** establishing — Lorna behind the bar; the mirror — the wink.

#### Per-NPC self-check
LIGHT, not gold-plated (~9, no odometer, no capstone chain — the shape, respected) ✓ · the on-ramp is
REPEATABLE/TIERED so it stays alive to Act 3 (the fix for v1's died-after-4-beats) ✓ · the mirror EXISTS
(v1's ghost, built) ✓ · never bedded, never corrupts the family ✓.

### World blueprint (Step 5 · §5) — schedules, ceilings, systems, quests, the shared-private builds

#### §5B — Per-place ceilings (author-encoded in each canvas's `conditions` — NOT a location attribute)
| Place | Ceiling | Forced allowed? |
|---|---|---|
| Lobby / Bar | stares → a hand in passing | **early only**, chance fades w/ power |
| Guest Rooms | anything behind a closed door | yes, act-scoped |
| Residence / bedrooms | milder, charged | **Grayson early** (prey floor) |
| Upstairs Bath | walk-in / occupied / caught | **early** (§5H) |
| **Private Floor** | lawless — whatever she'll sell | **never** (by the time it opens she's not prey) |
| Town / street | strangers, not staff — a different ceiling | never |

#### §5D — Schedules (who's where, when — reachable presence, never an offscreen blink-out except Audrey's college)
| NPC | Schedule (location · window) | Notes |
|---|---|---|
| **Richard** | Study 20:00–23:59 **+** 00:00–02:00 (wraps midnight → **two rows**) · Kitchen odd hours · *(post-arc)* the floor daytime | the 3 a.m. lamp; two-row past-midnight (known gotcha) |
| **Margaret** | Front desk 08:00–11:00 · Drawing Room 11:00–18:00 · her room evenings | behind your mother's desk on frame one |
| **Grayson** | Drawing Room daytime (feet up) · the Bar evenings (watching Audrey) · Kitchen 01:00–03:00 · his room | nocturnal, everywhere he shouldn't be |
| **Audrey** | **College 09:00–16:00 [OFFSCREEN away-label]** · her room / Kitchen evenings | the one real "away" |
| **Lorna** | the Bar 18:00–close | alive every evening |

#### §5F — Systems
- **Clothing** — outfit tiers covered → daring → bold → barely (each a `worn_corruption` band; the exhibition
  progression is *access to the outfit*, bought). Wardrobe at Your Old Room; shop = the Boutique.
- **Phone** — threads fire on **flags + elapsed days only** (never place/time/roll): Audrey's get eager,
  Grayson's get desperate (post-flip), Richard's get shy. **+ the photo-sale economy** (`p_phone_photos`,
  her 2nd income). Leverage-on-a-screen carried here.
- **Player portrait** — her image, one dominant axis + generic undress: **undress** (dressed → underwear →
  topless → bottomless → naked) · **outfit-type** (`work` / `going-out`) · **corruption LEVEL 0–4** ·
  **`pregnancy_suffix`**. Needs `clothing_enabled` (on).
- **THE PREGNANCY SYSTEM** (cross-cutting — Richard + Grayson; speced here, not buried in one arc):
  a **hidden trait `pregnant`** (0 = none · 1 = Richard's · 2 = Grayson's), set ONLY by the player-chosen
  terminal capstone, drives the portrait `pregnancy_suffix` (dressed images only) + late scene variants +
  NPC-reaction beats (Richard *radiant*; Grayson the darker note). **Always a chosen payoff, never a
  punishment** (Step 2 law). Frontier-tier.
- **Sidebar `npc_panel`** — each NPC's row shows the named next step + place + time-window. **HIDDEN meters:**
  `margaret_leverage`, every `*_stage`/`*_want` internal odometer, the `pregnant` trait (`[[traits.labels]]
  hidden=true`).

#### §5F.1 — The Quests page (the WHOLE surface, laid out as one thing)
- **Story-Goals spine** (from the desire ladder): *Get your hands on this place* → *Make the hotel breathe* →
  *Open the private floor* → *Take the will* → **frontier card** (*"you've reached the current peak — run
  your house"*; the greyed next-hook: a society rival across the city).
- **Per-NPC sections:**
  | NPC | Ladder shape | Why |
  |---|---|---|
  | **Audrey** | **stepped trait-band** (bands on `audrey_corruption`) | a smooth graded climb — the lessons |
  | **Grayson** | milestone-chain | discrete beats (prey → the deal → on his knees → yours for nothing) |
  | **Richard** | milestone-chain | discrete (sit → first night → **the keys** → the child) |
  | **Margaret** | milestone-chain, **WAR-framed** | shows the *war state* (she's watching / cornered), **never a seduction bar** (her leverage is hidden) |
  | **Lorna** | milestone-chain | her tiers |
- Every card **non-stale** (no Frame-3-blank dead end) + parity-matched to its `npc_panel` `next` row.

#### §5G — Access & travel
Day one: the whole hotel, residence, and street are open. **Two locked-visible doors say WHY on the card:**
the **Back Office** (*"the books are Richard's — until he trusts you with them"* → `richard_signed`) and the
**Private Floor** (*"empty, and it stays empty until you own this place and pay to open it"* → `richard_signed`
+ upgrade). Travel: **free inside the building; TIME-costed on the Town↔Lobby bridge** (`costs = {time=N}` on
that bridge only; the bridge is its own fast-travel valve). Locks are lock-as-prose (`entry_conditions` +
`blocked_message`, `version="1.0"`).

#### §5H — The four shared-private spaces (built the CORRECTED way — enterable, occupancy-gated activities)
All four: keep the room **enterable** (never hard-lock → no dead-end), give it a **dynamic occupant
description**, gate the ACTIVITIES by occupancy (`npc_at_location`).
- **The Upstairs Bath** — your self-care shows `is_absent`; the **peek lives on the room canvas** gated
  `is_present` (occupant resolves who: Richard mortified / Grayson doesn't-care / Audrey unbothered);
  **caught** = catch-then-react on your own bath (chance × who's-home, not a clock; early = can't-refuse,
  Grayson).
- **Audrey's room** — the "homework": `is_present` peek (door not quite shut → later open); banded chance.
- **Your Old Room** — you're the one caught: Grayson's no-knock walk-in on your sleep/solo host (chance fades
  with power; post-flip he waits to be invited).
- **The Guest Rooms** — the Lorna mirror: `is_present` catch after close; voyeuristic only.

#### §5A.1 — Private-bedroom placement (closing the dead-room gap the Step-6 review caught)
The map (2b) gave every private bedroom a job; the per-NPC blueprints must **land located canvases there**, or
they repeat v1's "job asserted, canvas never arrives" defect — the review flagged it landing on Grayson's Room
(the very room this game brags about fixing). Pinned:
- **Grayson's Room** (`loc_grayson_room`) — hosts the **servitude hub base** (`gray_amb_sprawl` + the private
  use rungs that aren't "in front of others") and the post-flip walk-ins where he waits to be invited. His
  room is where the *owned* Grayson lives, as distinct from the public humiliations.
- **Richard's Room** (`loc_richard_room`) — hosts **"The first night"** and **"The child"** (the private,
  tender peaks), as distinct from the Study (his grief in public + the deed).
- **Margaret's Room** (`loc_margaret_room`) — hosts **"The breaking"** and the terminal **"family slave"**
  loop's private beats, as distinct from the Drawing Room (her public court). Also `marg_amb` — her at her own
  vanity, the patrician armour off, the one place you see her uncomposed before the end.
- **The Back Office** (`loc_hotel_back_office`) — **disposition: an unlock-beat + a light function, not a dead
  shell.** Post-`richard_signed` it hosts the books-as-control (a repeatable "run the numbers" beat that gates
  the hotel upgrades) — so the room the player fought to open has a reason to be entered, not just a door that
  turned green.

### Wiring, order & opening (Step 5 · Pass 4) — the holistic pass

> Invents no new scenes. Orders and wires the whole inventory; seeds the plan.

#### The machine — the dependency map (verified acyclic)
```
  Lorna ──favor_idea──▶ income: comp-a-favour
  Lorna ──debt_known──▶ Grayson: "The deal" ──▶ grayson_bought_out ─┐
  floor work ─▶ money ─▶ hotel-in-hand ─▶ Richard: "The keys"       │
                                              │                      │
                                     richard_signed ────────────────┤
                                       │        │                    │
                              private floor  back office             ▼
                                       │                    Margaret: "The board turns"
  Audrey ◀── richard_stage, grayson_stage (Wave-2 threesomes)  ──▶ cornered ─▶ breaking
                                                                          │
                                                                    ▶ FRONTIER
```
- **D1 — no arc entry is gated.** Every on-ramp cold-start-enterable: Audrey (`aud_hub`/tuition), Grayson
  (ambient presence + the prey floor, act-scoped not a gate), Richard (`ric_sit`), Margaret (the war/ambient),
  Lorna (tier 0 @ corr 0). ✓
- **D2 — acyclic.** Verified by DFS: **no cycles.** Lorna is a source; Margaret is the sink (reads
  `richard_signed` + `grayson_bought_out`, sets only the frontier). ✓
- **D3 — every cross-gate telegraphed.** Audrey Wave-2 (*"Richard has to be yours first"*), Margaret's apex
  (*"she won't be moved while Richard holds the deed and Grayson still has a spine"*), the two locked doors. ✓
- **Every gate has a reachable setter** (verified): the favor idea, the debt tip, `richard_signed`,
  `grayson_bought_out`, the stages, `margaret_cornered`, hotel-in-hand, the intoxicant. ✓
- **The core money→access→conquest loop CLOSES** (money is the connective tissue — Form 2a). ✓

#### The opening — concrete scenes (the linear funnel; `onboarding.md`)
1. **Boot / customization** — set her name (default Catherine) + look. *(The world speaks `@player` back from
   scene one.)*
2. **The cold open — the Lobby.** You walk in on the day of the will reading, and **Margaret is behind your
   mother's front desk, giving your mother's staff their orders.** The whole game in one frame.
3. **The 2–3 things doable at zero:** **talk to Lorna** (the bar — she tells you how bad it is, and is glad
   you're back) · **go up to the family floor** (meet who's left — every arc's cold-start on-ramp is a room
   away) · **take a shift on the floor** (the first tip, the first ask for a bolder outfit — the first rung).
4. **The first named want:** ***"Get your hands on this place."***
5. **Each live system surfaced once, in fiction:** the shift teaches **clothing** + **the reactive world**
   (the first stare) + **money** (the first tip); a first text lights the **phone**; the sidebar shows the
   **portrait** at value-zero. No tutorial — the hotel teaches by needing you.
6. **The 10-minute taste:** a new player comes away knowing the charge — *the house is being taken, and not
   by you; you're here to take it back, and everyone in it.*

#### The fail-state ripple (§4F)
**No failure, by design** (Step 2, re-confirmed). Nothing confiscated; the negative axis is Margaret's
*status* lead, cleared by content. The rent system stays OFF.

#### Supply-vs-demand — closed
The deepest NPC floor (the Whore-band capstones — the private floor, the apex breaking) is reachable through
the player's OWN feeder economy (2–3 live per band, every band) without grinding: her corruption opens the
family doors having climbed through her own content. ✓

#### Scene total
Player track ~34 + NPC 106 + world/systems/opening ~12 = **~152 canvases** (v1: 76). Inside the 125–170
target. **The blueprint did not shrink into a corridor.**
