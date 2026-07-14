# The Inheritance — Design Book

> The user's review surface. This is **intent in plain language** — the engine/TOML is the faithful
> translation of what's written here. Grown one section per pipeline step.

---

## World setup

**POV.** Female PC. Cascade-native: the player corrupts herself and her own resolve before she corrupts
the household. The estranged daughter is a vessel the player fills.

**The fantasy (clears the 3-part bar).**
> You left years ago, estranged and written off. A death drags you home to the family estate for the
> reading of the will — and you intend to take it *all*: the estate, the dying family hotel, and **every
> person under its roof**, one by one, until the family that underestimated you answers to you.

- **POV-fit** ✓ — a female-PC takeover-from-within; the closed family is hers to corrupt from the inside.
- **Sharp charge** ✓ — *power-reversal + taboo*: the overlooked, estranged daughter returns and methodically
  takes apart and remakes the family around herself. Incest is the taboo charge; conquest (break-and-own) is
  the heat.
- **Built-in two-act shape** ✓ — **Act 1:** come home underestimated, read the players, find each one's
  weakness, take the failing hotel in hand as leverage. **Act 2:** pick them off — seduce, indebt, break —
  until the household and the estate are yours to own and arrange.

**Desire span (declared, not stumbled into) — MIXED, total-household conquest.**
> ⚠️ Widened from the original sapphic-only lock (book_revision 1 → 2). The player chose the full
> "own everyone under this roof" fantasy. Every adult in the house is a target.

- **Targets:** the **whole household** — both women (Audrey, Margaret) *and* both men (Grayson, Richard).
  Mixed span. *(Vivian removed turn 10.)*
- **Core flavor:** **conquest** (break-and-own) shading into transactional control; **cold, deliberate
  base register**, not romantic longing.
- **Three distinct registers** the span must carry (chosen, not stumbled into — the player should never be
  ambushed by a tone they didn't sign up for):
  1. **Cold sapphic conquest** — the women (Audrey / Margaret). The spine of the game.
  2. **Humiliation / domination** — the arrogant parasite brother (Grayson). "Bring the prick to heel."
  3. **Widower seduction** — the grieving stepfather (Richard). Slow, dark; consoling-into-owning the
     broken man, becoming the new woman of the house. The heaviest tonal outlier — handle with care.

**Premise.** The family matriarch — your mother, **Eleanor**, who built the family's **boutique hotel** —
has died. Her will pulls you, the estranged eldest daughter, back to the estate you walked out of years ago.
Your stepfather (her widower) is too sunk in grief to run the hotel or keep the household afloat; your
brother is a useless parasite; the will is contested; and the family who expected to inherit everything is
standing exactly where you intend to stand.

**Family blood ties (LOCKED).** Audrey and Grayson are Catherine's **half-siblings** — all three children
share the dead mother **Eleanor**, but the two younger ones are **Eleanor + Richard's** kids
(Catherine is from Eleanor's earlier relationship). So: the siblings are **blood** (shared mother → strong
incest taboo); **Margaret** is blood aunt (Eleanor's sister); **Richard** is the **stepfather** — Eleanor's
widower and the biological father of the two younger siblings (Audrey, Grayson), but no blood relation to
Catherine.

**Player.** **Customizable** — the player sets her name (and likely build/look) at the opening. The
returning-daughter is a role the player inhabits.

**Systems in use (scope only — wiring decided at authoring):**
- **Clothing** — YES. Wardrobe/closet; worn outfit gates public reactions and exhibitionism. The reactive
  world (Step 2) rides on this.
- **Phone** — YES. Chat threads with the household, photo tiers, leverage over screens.
- **Money / economy** — YES, but **reframed as a CONTROL economy, not survival rent.** The **boutique hotel**
  is failing and the stepfather can't cover the sisters' college fees or the staff. If the player chooses to
  take the hotel in hand, *saving it* becomes both her income and her leverage — paying a sister's tuition or
  covering Richard's debts is a corruption hook, not charity. (Exact stat/loop is Step 2's job; flagged here
  as "money matters, but as *control & dependence*, never as scraping rent.")

---

## Cast (names + roles only — Step 3 reshapes this into the cascade)

Naming set: **classic / old-money.** Deceased matriarch: **Eleanor** (the mother who built the hotel).
Player default name: **Catherine** (editable — the player is customizable).

**The whole household is in play (mixed span). Targets, by register:**

*Cold sapphic conquest (the spine):*
- **Audrey** — younger sister, in college, fees unpaid; the most vulnerable / entry-tier of the household.
- **Margaret** — the aunt (Eleanor's sister), moved into the estate to "help" and angling to seize control
  of the hotel and the will. The apex female power in the house; the climactic conquest.
- *(Vivian, the older sister, was cut turn 10.)*

*Other registers:*
- **Grayson** — the brother. A useless, hostile parasite and rival claimant who expects to coast into the
  inheritance. Target register = **humiliation / domination** ("bring the prick to heel").
- **Richard** — the stepfather, Eleanor's widower, sunk in grief; nominally heads the household and hotel he
  can no longer run. Target register = **widower seduction** (console-into-own; slow, dark). Also functions
  as the legal gatekeeper (the will, the hotel's fate).

> Step 3 (casting) will derive the exact tiers/ordering the cascade needs and may add or merge characters
> (e.g. hotel staff as minor cast). Listed here as *people* — no arc shapes, voices, or stats yet.

---

## Locations (the map — creative geography only)

- **The estate** — the family home the player returns to (her childhood home), attached to / above the
  hotel. The hub.
- **The bedrooms** — the sisters' rooms, the aunt's room, Richard's room, the player's old room. Private
  interaction space.
- **The hotel** — the failing family boutique hotel: lobby, guest rooms, bar/restaurant, back office. The
  control-economy surface where the player steps up and takes hold; also a public-facing stage for
  clothing/exhibitionism content and where each family member has a role.
- **The grounds / common rooms** — kitchen, study, drawing room, garden — shared household space where
  presence and ambient reactions happen.
- **Town** — the outside-the-estate space: the bank/lawyer (the will), shops (clothing), the sisters'
  college, wherever the hotel's business reaches.

> Creative geography only — no `is_container` / lock / schedule decisions yet (those are authoring).

---

## Top-level design — the engine, economy & machine (Step 2)

> Plain-words rulebook for how Catherine grows and how that growth unlocks the household. No TOML yet.
> Everything answers to the core loop: **work the floor → money + renown → the vice-house grows → its
> money/access buys leverage over the family → corrupt them → the family becomes part of the business →
> take the will → become the madam the household answers to.**

### 1. The cascade + the double lock
**You must corrupt YOURSELF before you can corrupt anyone else.** Catherine's own corruption is the master
key; all *lewd* content with the family stays locked until she's fallen far enough on the hotel floor.

- **Self-corruption first (Act 1).** She falls publicly, working her own failing hotel — hostessing in
  bolder outfits, weathering and then *enjoying* guests' liberties, crossing the first transactional lines.
  This raises **corruption** (the door) and **exhibitionism** (the public register) while it earns money.
- **Befriending the family is NOT gated.** Re-entering the household — talking, managing the hotel
  together, rebuilding (or exploiting) old bonds — raises each person's personal lock in parallel, in Act 1,
  with no corruption requirement.
- **The DOUBLE LOCK on every family lewd rung:** (1) **Catherine's corruption ≥ the tier for that KIND of
  act** (the door — opens for the whole household at once), AND (2) **that family member's own personal
  trait ≥ her/his threshold for that rung** (the individual lock — built by investing in them). They
  converge: by the time her corruption opens the door, the people she worked on are already unlocked.

### 2. The stat set (each leg gates real content — no dead stats)
- **corruption** *(always-on)* — the lewd door; the cascade spine. Gates: every family lewd rung (floor)
  + Catherine's own willingness on the hotel floor.
- **money** *(always-on)* — the hotel's lifeblood + the leverage fund. Gates: the family hooks (tuition,
  debts), clothing, hotel upgrades. The pressure that drives the fall (broke → the money's down the lewd
  path).
- **energy** *(always-on)* — paces the day; spent via `costs`, restored by sleep.
- **exhibitionism** *(built-in)* — the public/hotel-floor register; clothing-driven. Gates: how bold the
  floor work / public hotel content goes.
- **renown** *(Tier-3 custom — CONFIRMED)* — the **hotel's** underground reputation / how far
  the vice-house has transformed. This is the hotel's *own lock* in the double-lock (the building treated
  like a node): it gates which **clientele tiers and services** exist to be sold (legit guests → favors →
  escort clients → private-floor members). Raised by running lewd operations. Distinct from `corruption`
  (= how depraved *Catherine* is) and from `money` (= raw cash): renown = how depraved the *house* is.
- *(No `beauty` leg — derived read-only from worn clothing. No `fitness`/`intelligence`/`charisma` — no
  domain needs them; the family arcs use per-NPC `relation`/`corruption`.)*
- **Hard vs soft gates:** the private floor & its clientele = **hard** (don't exist until renown unlocks
  them). A family member's *presence* in the house = always reachable (**soft** — they're around from the
  start; only the lewd rungs gate).

### 3. The desire ladder (the chain of named wants — the player-facing spine)
Backstage it's meters; onstage it's wants. Each rung = a concrete want + what clearing it unlocks.

- **Act 1 — Fall + Build.**
  - *"Don't get thrown out — make the first money."* → take floor shifts → first tips + first bolder outfit.
  - *"Get the hotel breathing again."* → comp a room for a 'favor'; cross the first transactional line.
  - *(parallel, ungated)* *"Get back inside this family."* → re-meet Audrey, Margaret, Richard,
    Grayson; learn each one's weak point.
- **Act 2 — Reach.**
  - *"Open the private floor."* (renown threshold) → escort arrangements; the vice-house emerges.
  - As corruption crosses tiers, the family lewd rungs *appear* (double lock). Per-person wants:
    **own Audrey** (entry) → **bring Grayson to heel** → **console-and-own Richard** →
    **topple Margaret** (apex).
- **Act 3 — Deepen.**
  - *"Make the family part of the business."* → each member inducted into the vice-house (their hot
    capstones).
  - *"Take the will — become the head."* → apex conquest of Margaret + control of the estate.
- **Frontier (open-topped).** Madam of the vice-empire; the household owned and serving; the will yours.

### 4. The reactive world (clothing-driven)
The world reacts to **what Catherine is WEARING** (`worn_corruption`), never to a hidden number — and the
shift is always *bolder/lewder*, never warmer.
- **Place ceilings (author-encoded per canvas):** hotel lobby/bar = civilized-public early (stares,
  comments, brush-bys); the **private floor** = lawless (open liberties); family/common rooms = milder,
  charged. Same outfit, different room → different scene.
- **Predatory dispositions:** certain guests escalate; **Grayson** (hostile/entitled) takes liberties early;
  respectful staff stay flustered; **Margaret** banks what she sees as leverage.
- **Three modes:** *sought* (she dressed for it) · *choice* (refuse/accept) · **forced** (no branch —
  auto-fire capstone-shape). **Forced is ACT-SCOPED prey-early:** while she's underestimated and powerless
  (Act 1), a guest or Grayson can take a liberty she can't refuse; it **recedes as she rises** to predator.
  *(CONFIRMED: forced/non-con prey-early mode is IN — the floor of the prey→predator reversal.)*
- Progression comes from **access to bolder clothing** (bought/unlocked), not a trait.

### 5. The economy (a corruption ladder, anti-grind)
- **One wallet.** Money is money.
- **Income IS the corruption ladder:** legit hostessing (scraps) → flirty/comped favors → escort
  arrangements → private-floor cuts (the real money). The better money is always further down the lewd path.
- **Earning = content.** Every paying activity is a floor/reactive/escort scene, never a chore-click.
- **Multiple paths** (blocked on one → do another): floor work, comped favors, private-floor services,
  selling photos via the phone.
- **Sinks (wanted buys, keep pressure alive):** bolder clothing (the reactive dial) · hotel upgrades
  (transform rooms → unlock new service KINDS) · the family hooks (Audrey's tuition, Richard's debts) ·
  legal/buy-out costs for the will.
- **Pressure escalates across acts:** Act 1 = the hotel faces foreclosure/forced sale → Act 2 = Margaret &
  Grayson move legally to seize it / contest the will → Act 3 = a bigger external threat (a predatory buyer,
  the bank, a society scandal). The *form* escalates; pressure is always present, always costs money.

### 6. The machine (cross-wiring — core loop + wires)
**One machine, not parallel arcs sharing a wallet.** Core loop fixed here; full per-arc wiring finalized at
Step 4/5.
- **Core loop (the spine):** floor work → **money + renown** → unlock private-floor services → bigger money
  + leverage → **fund the family hooks** → corrupt the family → family joins the service (more renown/money)
  → take the will → apex.
- **Every core node has a place:** Audrey (entry conquest + tuition hook + the **gateway** to group content)
  · Grayson (obstacle → humiliated → bought out) · Richard (gatekeeper of the will → seduced → signs over
  control) · Margaret (apex rival for the will + the house). *(Vivian, the former operations node, was cut
  turn 10 — Catherine + Lorna carry hotel operations.)*
- **Wires:**
  - **Form 2a (economy as connective tissue):** hotel money is the *gate* to advance family arcs — pay
    Audrey's tuition to deepen her dependence; cover Richard's debts to own him; out-spend/buy out Grayson.
  - **Form 1 (arc→arc depth gates, mid/late only):** Margaret's late rungs gated on a player flag the other
    conquests set (e.g. `richard_signed` / `grayson_bought_out`); Grayson's humiliation gated on hotel
    control; Audrey's late group-threesome capstones gated on `richard_stage` / `grayson_stage`.
- **Disciplines:** **D1** — never gate an arc's ENTRY on another (everyone lives in the house →
  cold-start-meetable); only mid/late rungs cross-gate. **D2** — the wires form a DAG (checked at the
  roster). **D3** — every cross-gate is a locked-visible telegraph naming the other arc's state.

### 7. Pacing & frontier
- **Pacing:** climb → plateau → climb. Every want ends in a payoff; alternate big/small beats; never dump
  the big content early. **The endgame escalates in CONTENT, not management** — each family member's
  induction into the business is a *hot capstone*, the apex (becoming the madam of the house) is the
  hottest beats, never a +income dashboard.
- **The frontier (open-topped, no win-screen):** the top authored rung does three jobs — (1) land the
  charge-ceiling payoff (the whole household owned + serving, the will signed to Catherine); (2) drop into a
  **livable steady-state** (run the house: repeatable family loops + private-floor income + reactive world
  stay playable); (3) leave a **greyed next-hook seed** — e.g. *"a society rival across the city has heard
  what your house has become."* Local arc endings (fully owning one person) end a *thread*, not the game.

### Decisions (resolved — Step 2 locked)
1. **The `renown` stat** — ✅ INCLUDED. The hotel's underground reputation is its own Tier-3 progression
   axis, the building's "lock" in the double-lock model (gates clientele tiers + services).
2. **The forced / non-con reactive mode** — ✅ INCLUDED, act-scoped prey-early. Catherine starts as prey
   (powerless on the floor; guests/Grayson can take liberties she can't refuse) and rises to predator; the
   forced mode recedes as her power climbs. This is the floor of the central prey→predator reversal.

---

## Casting (Step 3) — every NPC's role, hook & place in the machine

**Scope locked:** all five family members are **full core arcs** (the true "own everyone" build), plus two
non-family NPCs — **Lorna** (the corrupting on-ramp / enabler) and **Mr. Halloway** (the will/foreclosure
pressure, structural). Naming stays classic/old-money.

**Structural coverage check** ✅ — pressure source = Halloway (foreclosure clock) + Margaret (seizes the
will, escalates late); corrupting on-ramp = Lorna + the hotel floor; core targets = all five family; late-act
pressure = Margaret. Cascade can run.

| NPC | Role(s) | Hook (dynamic · charge · want) | Lane / register | Depth | Arc-shape | Place in the machine |
|---|---|---|---|---|---|---|
| **Audrey** | Core target (entry) + **GATEWAY** | The baby sister who never stopped looking up to you — broke, terrified of losing her place at college, so hungry to be *taken care of* that gratitude curdles into something she won't name. **Want:** land the boy at school (Danny). **Charge:** corruption-as-mentorship; she wins AND is yours. | Vulnerable / nurturing-turned-corrupt · cold-sapphic | Full (gold) | family/ambient (dense) | **Tuition hook** (Form 2a) + **group-content gateway** (unlocks threesomes — Danny/Richard/Grayson). First family unlock. |
| **Margaret** | Core target (**apex**) + late-act pressure | Eleanor's sister, moved in "to help" — sharp, patient, already counting the silver and reading you as the only real threat. **Want:** the will, the hotel, the family under her. **Charge:** conquest of the apex who came to conquer you. | Dominant antagonist · cold-sapphic | Full (gold) | antagonist → conquest | **Apex node** — her late rungs gate on `richard_signed` + `grayson_bought_out` (Form 1); she *is* the escalating Act 2–3 pressure. |
| **Grayson** | Core target + obstacle | Your brother — entitled, useless, certain the inheritance is his and you're beneath him (certain enough to put his hands on you while you're still nobody). **Want:** the money without earning it; dominance over you. **Charge:** humiliation — break the arrogance, bring the prick to heel. | Arrogant rival humiliated · domination | Full | antagonist | **Obstacle → bought-out** — predatory in the prey phase; his subjugation sets `grayson_bought_out` (Form 1, feeds Margaret's apex gate). |
| **Richard** | Core target + will gatekeeper | Eleanor's widower, hollowed by grief, drifting through a hotel he can't run, holding the will and the keys and forgetting why. **Want:** Eleanor back / comfort / to hold the family together. **Charge:** console-into-own the broken king. | Tender-predatory / fill-the-void · widower seduction | Full | slow-burn family | **Gatekeeper node** — seduced → signs over control, setting `richard_signed` (Form 1, gates Margaret's apex + hotel control). |
| **Lorna** | Corrupting on-ramp / ally-enabler + peripheral target | The hotel's lifer bartender who's seen what this place was and what it could be after dark — worldly, unshockable, glad to teach the new owner how a room like this *really* turns a profit. **Want:** the hotel alive + her cut. **Charge:** transactional flirt; she hands you the first dirty idea. | Knowing mentor / transactional · light flirt | Light (peripheral) | service | **On-ramp / renown node** — unlocks the vice-trade knowledge that opens private-floor services (drives `renown`). |
| **Mr. Halloway** | Pressure source / structural | Eleanor's executor — starched, correct, holding the foreclosure clock and the will's fine print, indifferent to your charm and immune to it. **Want:** discharge the estate by the book. **Charge:** none — he's the deadline with a face. | Obstacle (no desire lane) | Structural (no arc) | — (not a target) | **Pressure node** — the Act-1 foreclosure clock + will reading; the deadline that drives the fall. |
| **Danny** *(added turn 8)* | Prop — Audrey's payoff | The ordinary college boy Audrey's hopeless over — sweet, a little clueless, no idea what he's walked into. **Want:** Audrey. **Charge:** none of his own — he's *her* win and the body in the threesome. | — (prop) | Prop (no arc) | — (not a target) | **Audrey's payoff** — she lands him (study weekdays / weekend outings); Catherine joins → BF threesome. Light recurring presence, never his own arc. |

### Rough sketches & cross-NPC threads
- **Audrey the gateway.** The load-bearing thread now runs through Audrey: she's the first one fully open,
  so her late content unlocks the **group/threesome routes** (Danny, Richard, Grayson). The more Catherine
  has Audrey (`audrey_stage`), the more group content lights up. *(This replaced the cut Audrey↔Vivian
  sisters thread, turn 10.)*
- **Richard ↔ Margaret (the will).** Richard nominally holds control; Margaret is prying it from his grief.
  Whoever Catherine owns first changes the other's path — owning Richard (he signs to *her*) strips
  Margaret's claim and detonates the apex confrontation. Both feed the `will` machine.
- **Grayson, the early predator.** In the prey phase he's the in-house face of the forced/reactive liberties
  (entitled, handsy). His arc is the satisfying inversion: the man who took liberties early ends up
  groveling/bought-out. Bridges the reactive world (Step 2 §4) and his humiliation arc.
- **Lorna, the mirror.** She's what Catherine is becoming — a woman who runs a house of vice without
  flinching. Possible light arc of her own; also the voice that narrates the hotel's transformation. If her
  thread grows, she re-enters as a deeper NPC (new casting pass).
- **Halloway** stays an island — pure structure (the clock). No thread, by design.

---

## NPC arcs (Step 4) — one R7 brief per NPC

> Built one NPC at a time. Each brief expands the casting hook into a playable arc bound to the cascade
> double-lock. Order follows the cascade: **Audrey → Grayson → Richard → Margaret → Lorna.** *(Vivian cut
> turn 10.)*

### Audrey — R7 brief  ✅ (entry target + GATEWAY · family/ambient (dense) · core/gold · cold-sapphic)

> **Her job in the game:** the entry target AND the **gateway** — the first one fully open, the key that
> unlocks all the group/threesome content. The biggest, most replayable arc in the game even though she's
> the easiest. Built as the *fun, sex-positive sandbox sister* against the cold register everywhere else.

**§1 · End-state fantasy — corruption disguised as mentorship; she WINS and is yours.** Audrey's own
**want** drives the arc: there's a boy at school — **Danny** — she's hopeless over and too innocent to land.
The ramp is trust: she comes to Catherine panicking about tuition → Catherine pays it → Audrey learns *her
big sister is the one who fixes everything* → so when the boy problem hits, she brings *that* to Catherine
too, and **asks to be taught.** Catherine teaches her, skill by skill, and the lessons are the corruption.
The twist (this is what makes it darker, not lighter): **Audrey genuinely succeeds** — she lands Danny as her
boyfriend — but by then Catherine has rebuilt her into a girl with no lines left: she practices everything
on her sister first, shares Danny's bed with her, and is happily down for the whole family. She never sees
any of it as wrong; she thinks she has the closest, luckiest family alive and a sister who taught her
everything. The horror is entirely the player's to see. *(Innocent-but-enthusiastic. The student who aced
the class and never noticed what the class was.)*

**§2 · Voice spec.** Soft, eager, earnest — a diligent student who *wants to get it right* ("okay, so — like
this? am I doing it right?"). Fast when she's nervous; deflects worry into helpfulness. Calls her "Cath."
Never crude in her own voice early — the dirty words are part of the *lesson*, coaxed out of her ("say it,
it's just us"); that coaxing is content. Stays enthusiastic and unembarrassed once a skill is learned (she's
*proud*). RTS-flat for Lane 1/2/3; **Tier-3 earned only in capstones**, where her reframing ("this is just
sisters, this is just practice, this is just love") blooms. One *italic* private thought per appearance — a
rationalization (early ones shy about Danny, later ones easy and happy).

**§3 · Stat ladder + gating spine** *(family/ambient dense → rich two-meter, core depth).*
- **Spine = `npc_audrey.corruption`** (her ODOMETER — permanent willingness; gates skill rungs + capstones)
  **+ `npc_audrey.arousal`** (her THROTTLE — resets at climax; gates the repeatable practice/sex loop ONLY,
  never a capstone). Both declared in `[npcs.core_traits]`.
- **THE DOUBLE LOCK IS LOAD-BEARING HERE (LO's tightening):** player `corruption` is NOT just a floor on the
  final beats — it gates **how far Catherine can teach at all**, rising per skill. Each new skill needs BOTH
  (a) Audrey practiced the prior skill enough (her readiness) AND (b) Catherine corrupt enough herself (the
  door). Teaching masturbation needs barely any player corruption; teaching **anal** needs Catherine near her
  own floor. → *you must keep corrupting yourself on the hotel floor to keep unlocking what you may teach.*
  Her arc is welded to the main self-corruption loop.
- **The "practice ×3" mechanic:** each skill is a **repeatable** practice action (gated by her `arousal`
  throttle). Practicing raises `npc_audrey.corruption` **+1, daily-capped** (via `practiced_with_audrey_today`)
  — so ~3 capped practices = a few in-game days = the next skill's rung unlocks. The next skill renders
  **locked-visible** ("She needs more practice first" telegraph). Vary each practice (nervous → clumsy →
  proud) + Catherine coaches differently so it reads as *learning*, not grind. NO passive `+1/day` climb
  (overrides `doctrine/09` §4.1) — fully player-driven.
- **Stage flags (the skill ladder, player-mirrored as `audrey_stage`):** `audrey_reconnected` (non-lewd
  re-bond) → `audrey_tuition_paid` (trust leash) → `audrey_lessons_begin` (asks for help w/ Danny) →
  `audrey_skill_masturbate` → `audrey_skill_kiss` → `audrey_skill_toy` → `audrey_skill_blowjob` →
  `audrey_skill_sex` (first night → opens sex loop) → `audrey_skill_anal` → `audrey_danny_bf` (lands him) →
  group-route flags (`audrey_3some_danny`, `audrey_3some_richard`, `audrey_3some_grayson`) → `audrey_devoted`
  (terminal).
- **Vocab ceiling:** max-explicit (default).

**§4 · Per-rung pretext shapes — the LESSON LADDER** (each skill practiced ~3×, double-gated on her
readiness + the player-corruption door; the **lesbian content IS the practice** — "I can't practice on him
yet, so… on you"):

| # | Skill | Practices ON | Player-corruption door (approx) |
|---|---|---|---|
| 0 | *Confession + tuition* (non-lewd hook) | — | none |
| 1 | **Masturbation** | herself (homework; the walk-in scenes) | low (~Lewd) |
| 2 | **Kissing** | *Catherine* | ~Lewd |
| 3 | **Toy / dildo** | herself (penetration + oral prep on it) | ~Lewd/Slutty |
| 4 | **Blowjob** | a toy, then *Catherine* (strap) | ~Slutty |
| 5 | **Sex** (first night) | *Catherine* (strap) | ~Slutty/Whore |
| 6 | **Anal** | *Catherine* | ~Whore |

**§5 · Lane-by-lane map** *(family/ambient dense budget — ~22–26 canvases; she's the content hub):*
- **L1 hubs** — *Audrey's room* + wherever she hovers near you (one hub per schedule window): base + Talk
  (ungated) + the locked-visible **skill ladder** (each skill a practice action; the next greyed with a
  "needs more practice / you're not corrupt enough yet" telegraph). The **repeatable practice/sex loop**
  hangs off the hub once each skill is learned (`sex-loop.md`, gated by her `arousal`).
- **L2** — ambients: catch her bent over bills red-eyed (early); catch her flushed after "homework"; catch
  her texting Danny giddily. T1–T2.
- **L3** — the dense lane (this is family/ambient): **"did you do your homework?" walk-ins** (catch her
  practicing what you set), **Danny study-date walk-ins** (weekday — see below), her walking in on *you*.
  Several substitution scenes — the shape's dominant lane.
- **Danny (the boyfriend) presence:** light recurring NPC — **weekdays studying in Audrey's room**
  (a Lane-3 host: "join the study session" → coaching / walk-in / eventual threesome), **weekends out** (a
  beach/outing location — ties into the clothing/exhibition system: pick her swimsuit, his reaction).
- **Capstones** — see §6.

**§6 · Capstones** *(odometer + flags only — NEVER the arousal throttle):*
1. **"You fix everything"** (Type A) — the tuition crisis; Catherine pays; trust locks. Gate:
   `audrey_reconnected`. Sets `audrey_tuition_paid` (+ opens the lessons hook).
2. **"The first lesson"** (Type A) — she asks for help with Danny; the first explicit lesson crosses the
   line. Gate: `audrey_lessons_begin` + `npc_audrey.corruption ≥ 4` + player `corruption ≥ ~15`. Sets
   `audrey_skill_masturbate` + `audrey_opened_up`.
3. **"The first night"** (Type A) — the "sex" lesson; practice becomes the real thing, on Catherine. Gate:
   `audrey_skill_blowjob` + `npc_audrey.corruption ≥ 10` AND player `corruption ≥ ~50`. Sets
   `audrey_skill_sex` → **opens the repeatable sex loop**.
4. **"She got the boy"** (Type A) — Danny becomes her boyfriend (the win; study dates + weekends begin).
   Gate: `audrey_skill_sex` + `audrey_danny_introduced`. Sets `audrey_danny_bf`.
5. **"Study group" (BF threesome)** (Type B) — Catherine joins a Danny study session; the threesome.
   Gate: `audrey_danny_bf` + player `corruption ≥ Whore`. Sets `audrey_3some_danny`.
6. **Family-threesome capstones (×2, cross-NPC, late/frontier):** **Audrey + Richard + Catherine** and
   **Audrey + Grayson + Catherine** — Audrey is the willing third. Gate each on `audrey_skill_anal` AND the
   other arc deep (`richard_stage`/`grayson_stage` ≥ late) + player `corruption ≥ Whore`. Set
   `audrey_3some_richard` / `audrey_3some_grayson`. *(Authored as `cross_npc` beats; D1-safe — these gate
   LATE rungs, never any arc's entry.)*

**§7 · Per-NPC anti-patterns.** Don't make Audrey crude unprompted early (it's coached out of her).
Don't gate her skill rungs on player corruption ALONE — her own corruption odometer is the spine (Marcus
split-spine trap); the player door is the *second* lock, not the only one. No passive daily climb. Keep the
practice from being grind (vary it + cap it). Don't let Danny become a real character with his own arc — he's
a light prop (her win + the threesome). The tuition/lessons are never, from *her* side, a transaction or a
seduction — only the player sees the leash.

**§8 · Wiring contract (place in the machine).**
- **SETS:** the full `audrey_skill_*` ladder, `audrey_tuition_paid`, `audrey_danny_bf`, the three
  `audrey_3some_*` flags, `audrey_devoted`, and the player-mirror `audrey_stage`.
- **READS:** the **economy** (Form 2a) — paying tuition is a money sink that opens the trust ramp; the
  **cascade door** (player `corruption`) — now **load-bearing**, gating each skill's reach; and for the
  family-threesome capstones, **`richard_stage` / `grayson_stage`** (late-only, the group reward).
- **SOURCE for:** the **group content** — Audrey is the gateway/enabler the men's late arcs route a
  threesome through (`audrey_3some_richard` / `audrey_3some_grayson`). *(Her former sisters-lever role for
  Vivian is gone — Vivian was cut turn 10.)*
- **Disciplines:** D1 ✓ — entry (reconnect/talk/first lesson hook) ungated; the cross-reads
  (`richard_stage`/`grayson_stage`) gate only the **late** threesome capstones, never any entry. D2 ✓ — the
  reads point at Richard/Grayson, who don't read back through Audrey (no cycle; roster runs the DAG check).
  D3 ✓ — every cross-gated capstone ships a locked-visible telegraph naming the other arc's state ("Not
  while Richard's still grieving — bring him further along first").

**§9–10 · Acceptance.** Done when: the two-meter spine is declared + gated (her corruption gates the skill
ladder, her arousal gates the practice/sex loop); the double lock is on every skill — her readiness AND the
rising player-corruption door; the practice-×3 mechanic paces each skill (daily-capped, locked-visible next
rung); ~22–26 canvases sized to family/ambient with L3 dominant; Danny exists as a light recurring prop
(study weekdays / weekend outings) and never overgrows; 6 capstones gate on odometer + flags (incl. the
3 group routes — Danny, Richard, Grayson); the voice holds innocent-enthusiastic with Tier-3 only in
capstones; `audrey_stage` is set as the player-mirror, and the `audrey_3some_*` enabler flags exist for the
men's arcs.

---

### Grayson — R7 brief  ✅ (core target + obstacle · antagonist → owned (domination) · core/full · femdom + cuckold)

> **Her job in the game:** the brother you *break*. The cast's only pure-payback arc — the dominant
> register against Audrey's tenderness and Margaret's cold rivalry. He starts on top of you and ends your
> willing lapdog. **Bought with money, exactly like Audrey — but corrupted into submission, not love.**

**§1 · End-state fantasy — the arrogant heir broken into your willing lapdog.** Grayson is the entitled
parasite certain the estate is his and you're beneath him — and early, while you're still nobody, he's
*handsy*: he bullies and paws at you because he can (the prey-phase floor, the bottom of the game's
prey→predator reversal). Then you take the money. The hotel's purse is yours, his allowance is gone, and his
**gambling debts** (to people who hurt slow payers) are closing in. So he comes to *you*, needing cash — and
the price is a **day as your servant.** It's a cold transaction he despises at first. But repeated servitude
**rewires him**: the man who never had to do anything discovers he *needs* it — the structure, the being
owned, your attention. The money stops being the point. He ends giving himself **for free** — your
chastity-locked, orgasm-controlled **lapdog**, made to *watch* you take everyone and everything he thought
was his, signing his inheritance claim over because the throne means nothing next to belonging to you.
*(Bought into submission. The prince who begged for the collar — and then begged to keep it.)*

**§2 · Voice spec.** Smug, condescending, entitled drawl; "sis" as a sneer; casual cruelty while he's on
top. As he breaks: bravado → sullen compliance → neediness → eager grovelling ("tell me what you want — I'll
do it, just— let me"). RTS-flat Lane 1/2/3; **Tier-3 earned only in capstones** (the deal, the turn, the
surrender). One *italic* private thought per appearance — early ones contemptuous, later ones humiliated by
how badly he wants it.

**§3 · Stat ladder + gating spine** *(antagonist → owned, domination → rich two-meter, core depth).*
- **Spine = `npc_grayson.corruption`** (his SUBMISSION ODOMETER — how broken/owned; gates rungs +
  capstones; built by service beats, daily-capped via `served_today`, no passive climb) **+
  `npc_grayson.arousal`** (his THROTTLE — drives the repeatable use/humiliation loop, never a capstone).
  Player `corruption` = the secondary floor on the degrading/explicit beats, rising per tier. Declared in
  `[npcs.core_traits]`.
- **The money lever (Form 2a — same engine as Audrey):** paying Grayson is a **money sink** that buys each
  servitude beat and advances his odometer. His **gambling debt** is a background number/threat that keeps
  his need (and your leverage) alive and **escalating** (the bookies are the late-act pressure on him).
- **Stage flags (player-mirrored as `grayson_stage`):** `grayson_bully` (prey floor, Act 1 — he's on top,
  ungated) → `grayson_broke` (the flip — you control the purse, he comes needing cash) → `grayson_serves`
  (first paid servitude) → `grayson_used` (first degrading/sexual service — opens the use-loop) →
  `grayson_craves` (the turn — he wants it) → `grayson_gives_himself` (serves unpaid) → `grayson_bought_out`
  (terminal — claim folds, fully yours).
- **Double-lock thresholds:** menial service = `npc_grayson.corruption ≥ 3` (door low); degrading/sexual =
  `npc_grayson.corruption ≥ 6` AND player `corruption ≥ ~25`; deepest humiliation (pegging / chastity /
  cuckold) = `npc_grayson.corruption ≥ 12` AND player `corruption ≥ Whore`.
- **Vocab ceiling:** max-explicit. **Femdom ceiling = FULL, incl. pegging** (LO confirmed).

**§4 · Per-rung pretext shapes — the SERVITUDE LADDER** (bought with money, escalating as his submission
odometer + the player door climb):
- *Prey floor (reactive, early):* he bullies/gropes you while you're powerless — humiliating, happens *to*
  you (the Step-2 §4 forced/reactive content; recedes as you rise).
- *The flip:* he comes broke, bookies on him; you make a day's servitude the price.
- *Menial:* fetch, carry, wait on you, kneel — stripping the entitled man's dignity.
- *Degrading:* beg, be mocked, serve in front of others, worship you, eat you out on command.
- *Sexual use (full femdom):* ride him as your toy (his orgasm on your terms — denial, ruined, chastity);
  **pegging**; **cuckold/made-to-watch** (he watches you take others / is the lowest body in the Audrey
  threesome). The status humiliation — the heir watching you own everything — is the spice.
- *Free service:* he comes unpaid, asks for it, gives himself.

**§5 · Lane-by-lane map** *(antagonist → owned, mid-dense — ~14–18 canvases):*
- **Early reactive** — the prey-phase Grayson liberties (Step-2 §4 forced/choice; act-scoped, fade as power
  rises).
- **L1 hub** — *summon / make Grayson serve* (where you control him): the servitude rungs (locked-visible,
  greyed until `grayson_broke` + the door rises) + the **repeatable use/humiliation loop** once
  `grayson_used` (gated by his `arousal`).
- **L2** — ambients: catch him sulking, taking a threatening call from the bookie, gambling on his phone,
  glaring as you run the house. T1–T2.
- **L3** — walk-ins: catch him cornered/desperate by the bookies; catch him mid-menial-task and *liking* it.
- **Capstones** — see §6.

**§6 · Capstones** *(odometer + flags only — NEVER the arousal throttle):*
1. **"The deal"** (Type B) — he comes broke; you set servitude as the price. Both branches playable (takes
   it seething / storms off and comes back worse). Gate: `grayson_broke` + hotel-money control. Sets
   `grayson_serves`.
2. **"On his knees"** (Type A) — service escalates to degrading/sexual; the first real use + orgasm control.
   Gate: `grayson_serves` + `npc_grayson.corruption ≥ 6` + player `corruption ≥ ~25`. Sets `grayson_used`
   → **opens the repeatable use-loop** (gated by `npc_grayson.arousal`).
3. **"He stops pretending"** (Type A) — the turn; he serves and you both know he wants it; the deepest
   humiliation tier opens (pegging / chastity / cuckold). Gate: `grayson_used` + `npc_grayson.corruption ≥
   12` + player `corruption ≥ Slutty`. Sets `grayson_craves`.
4. **"Yours for nothing"** (Type A, terminal) — he comes unpaid, gives himself, signs his claim over. Gate:
   `grayson_craves` + player `corruption ≥ Whore`. Sets `grayson_gives_himself` + `grayson_bought_out`
   (ends the thread).

**§7 · Per-NPC anti-patterns.** Don't let the early prey-floor groping read as *his* win from the player's
side — it's the humiliating floor that earns the payback. Don't break him fast — the entitled bravado must
be real and resistant so the fall lands (he's not Audrey; he fights it). Don't gate his arc **entry** on
another arc (D1) — he exists and bullies from the start; the *flip* gates on the **economy** (hotel-money
control), not an NPC. Don't gate on player corruption alone — his submission odometer is the spine. The
money lever is **repeated**, not one-time — paid service over days is what rewires him (a single payoff
doesn't corrupt).

**§8 · Wiring contract (place in the machine).**
- **SETS:** `grayson_serves`, `grayson_used`, `grayson_craves`, `grayson_gives_himself`, `grayson_bought_out`,
  and the player-mirror `grayson_stage`.
- **READS:** the **economy** (Form 2a — paying him is a money sink; his gambling debt = escalating
  pressure); the **cascade door** (player `corruption`) on degrading/explicit beats; a **hotel-money-control**
  flag for the flip (he needs you because you hold the purse).
- **SOURCE for:** **Margaret's apex** — `grayson_bought_out` removes a pillar under the aunt (one of the
  isolating moves that unlocks her endgame); **Audrey's group route** — `grayson_stage`/`grayson_bought_out`
  enables `audrey_3some_grayson` (Audrey reads this, late-only).
- **Disciplines:** D1 ✓ — entry (he bullies / exists) ungated; the flip gates on the economy, not another
  NPC. D2 ✓ — Audrey & Margaret read Grayson; Grayson reads neither (no cycle; roster runs the DAG check).
  D3 ✓ — the flip ships a locked-visible telegraph naming the requirement ("Grayson won't come crawling till
  you control the hotel's money").

**§9–10 · Acceptance.** Done when: the two-meter spine is declared + gated (his submission gates rungs, his
arousal gates only the use-loop); the **money lever** (Form 2a) buys each servitude beat and the debt drives
escalating pressure; the double lock is on every degrading/explicit rung (his submission AND the rising
player door); he resists hard early (real bravado) and the prey-floor reactive content is present; ~14–18
canvases sized antagonist→owned; the femdom ceiling is full incl. pegging + the cuckold/status humiliation;
4 capstones gate on odometer + flags; `grayson_bought_out` feeds Margaret's gate and `grayson_stage` enables
Audrey's threesome route.

---

### Richard — R7 brief  ✅ (core target + will gatekeeper · slow-burn family · core/full · earned seduction)

> **His job in the game:** the gatekeeper of the will. The cast's one genuinely *warm* arc — you don't
> trick or break him, you pull a grieving man back to life and he falls for you, then hands you the
> kingdom. **Won with trust + lust, not money or coercion. No dead-wife angle (cut) — he falls for YOU.**

**§1 · End-state fantasy — the widower who gives you the keys.** Richard is your **stepfather** (Eleanor's
widower — **no blood tie to you**; he's the biological father of Audrey & Grayson) and he holds the two
things you need: control of the hotel and the will. Since Eleanor died he's been **hollowed out** —
drifting, drinking, not running anything. His grief is his *starting state*, not a lever you pull: you win
him by becoming the reason he gets up again. **Trust first** (his steady presence, his confidante), **then
lust** (the closeness turns charged and he wants you, ashamed of it but unable to stop). His wanting pulls
him **back to the business — he throws himself into the hotel to be near you, to impress you, to earn your
company** — and you reward the effort with more of yourself. He wants more, works more, you give more; the
failing hotel revives on the back of his desire. In the end he sees clearly that **you'd run the place
better than he ever could**, he's tired and aging, and he'd rather *support you than lead* — so he hands you
the keys and the will, and stays on as your devoted right hand, helping however you need. *(The one tender,
earned, slightly melancholy arc — the man who fell for the woman who saved him and gave her everything.)*

**§2 · Voice spec.** Grief-fogged, distant, apologetic early ("sorry — what did you— I wasn't listening").
As trust + lust build: warming, then *eager* — alive again, a little embarrassed by how much he wants you
near. Dignified even in devotion; never pathetic. RTS-flat Lane 1/2/3; **Tier-3 earned only in capstones**
(the first night, the handover). One *italic* private thought per appearance — early ones grief-numb, later
ones guiltily hopeful, then quietly content.

**§3 · Stat ladder + gating spine** *(slow-burn family → rich two-meter, core depth).*
- **Spine = `npc_richard.corruption`** (his ODOMETER — but *felt* as **trust/attachment/how-far-he'll-go**,
  not depravity; gates rungs + capstones; built by being there for him, daily-capped via
  `talked_to_richard_today`, no passive climb) **+ `npc_richard.arousal`** (his THROTTLE — his **lust**;
  drives the "he wants more / pursues you" pressure and the repeatable loop after the first night, never a
  capstone). Player `corruption` = the secondary floor on explicit beats. Declared in `[npcs.core_traits]`.
- **The pursuit loop (his agency):** as his arousal/attachment climbs, **he initiates** — asks you to join
  him at the hotel, finds reasons to be near you. Rewarding him (your attention/intimacy) advances his
  odometer. Authored as his pursuit beats, not a new mechanic. *(This also fills the hotel-operations role
  the cut Vivian left — Richard re-engaged is your ops help.)*
- **Stage flags (player-mirrored as `richard_stage`):** `richard_grieving` (Act 1 — checked out; you
  comfort him, ungated) → `richard_leans_on_you` (trust; his confidante) → `richard_wants_you` (lust; he
  starts pursuing) → `richard_opened` (first charged crossing) → `richard_first_night` (opens the loop) →
  `richard_signed` (hands over hotel + will control) → `richard_devoted` (terminal — devoted elder/right
  hand).
- **Double-lock thresholds:** charged/contact = `npc_richard.corruption ≥ 6` + player `corruption ≥ ~20`;
  first-night/explicit = `npc_richard.corruption ≥ 10` AND player `corruption ≥ ~35`; the handover gates on
  deep attachment (`npc_richard.corruption ≥ 14` + `richard_first_night`) — willingly, not coerced.
- **Vocab ceiling:** max-explicit (default).

**§4 · Per-rung pretext shapes** (built on companionship → lust, never on grief-exploitation):
- *Presence (non-lewd):* sit with him, get him eating, fill the silence. Become his steady person.
- *Trust:* he confides, leans on you, lets you in; you become indispensable.
- *The charge:* the comfort turns warm turns wanting — a touch that lingers, him catching himself looking.
- *The pursuit:* he comes alive, throws himself into the hotel to be near you; you accompany and reward him.
- *Explicit:* the first night — him finally letting himself have what he wants; tender, a little guilty.
- *The handover:* fully yours, he gives you the keys and the will, and asks only to stay and help.

**§5 · Lane-by-lane map** *(slow-burn family budget — ~12–14 canvases; empty cells honest):*
- **L1 hub** — *the study / the office where he drifts then works* (one per schedule window): base + Talk/
  comfort (ungated) + locked-visible rungs (greyed until trust/lust + the door rise). The repeatable loop
  hangs off it after `richard_first_night`.
- **L2** — ambients: catch him staring at nothing / drinking alone (early); catch him *energized*, actually
  working, lighting up when you appear (mid). T1–T2.
- **L3** — walk-ins: catch him broken-down in the study (early); later, him seeking you out, finding excuses.
  2–3 scenes.
- **Capstones** — see §6.

**§6 · Capstones** *(odometer + flags only — NEVER the arousal throttle):*
1. **"Back to life"** (Type A) — the comfort crosses into the first charged moment; he wants you and you
   both feel it. Gate: `richard_leans_on_you` + `npc_richard.corruption ≥ 6` + player `corruption ≥ ~20`.
   Sets `richard_opened`.
2. **"The first night"** (Type A) — he finally lets himself have you; tender, guilty, willing. Gate:
   `richard_opened` + `npc_richard.corruption ≥ 10` AND player `corruption ≥ ~35`. Sets `richard_first_night`
   → **opens the repeatable loop** (gated by `npc_richard.arousal`).
3. **"The keys"** (Type A) — he hands you control of the hotel and the will; he'd rather support you than
   lead. Gate: `richard_first_night` + `npc_richard.corruption ≥ 14`. Sets `richard_signed` (feeds Margaret's
   apex gate + grants hotel control).
4. **"At your side"** (Type A, terminal) — the devoted elder/right hand, wholly yours, helping however you
   need. Gate: `richard_signed` + player `corruption ≥ Slutty`. Sets `richard_devoted` (ends the thread).

**§7 · Per-NPC anti-patterns.** **No dead-wife angle** — Catherine never impersonates or evokes Eleanor;
he falls for *her*. The grief is his starting state, not a seduction tool — don't write Catherine preying on
it ghoulishly; the arc is earned warmth. Don't make him pathetic — dignified even in devotion. Don't gate
his arc **entry** on another arc (D1) — he's home and grieving from the start; comfort is ungated. Don't
gate on player corruption alone (his attachment odometer is the spine). The handover must read as
*willing* (trust + age + your competence), never coerced — that's what makes it land harder than a puppet
signing.

**§8 · Wiring contract (place in the machine).**
- **SETS:** `richard_opened`, `richard_first_night`, `richard_signed`, `richard_devoted`, and the
  player-mirror `richard_stage`. `richard_signed` grants **hotel control** (narrative ops help filling the
  cut-Vivian gap; income-wire = G6 deferred).
- **READS:** the **cascade door** (player `corruption`) on explicit beats. (His arc is otherwise
  self-contained — no cross-NPC read gates it.)
- **SOURCE for:** **Margaret's apex** — `richard_signed` strips her claim (with `grayson_bought_out`, the
  two moves that detonate the endgame); **Audrey's group route** — `richard_stage` enables
  `audrey_3some_richard` (Audrey + Richard + Catherine — **father & daughter**, LO-confirmed; Audrey reads
  this, late-only).
- **Disciplines:** D1 ✓ — entry (comfort) ungated. D2 ✓ — Audrey & Margaret read Richard; Richard reads
  neither (no cycle). D3 ✓ — any cross-gated beat ships a locked-visible telegraph.

**§9–10 · Acceptance.** Done when: the two-meter spine is declared + gated (his attachment gates rungs, his
lust/arousal gates the pursuit + loop); the **trust→lust→pursuit→handover** progression is intact and the
business-revival loop is authored as his pursuit beats; **no dead-wife/Eleanor-impersonation content
anywhere**; the double lock is on the explicit rungs; the handover reads as willing (gates on deep
attachment, not coercion); ~12–14 canvases slow-burn; 4 capstones gate on odometer + flags;
`richard_signed` feeds Margaret's gate + grants hotel control, and `richard_stage` enables Audrey's
threesome route.

---

### Margaret — R7 brief  ✅ (apex target + late-act pressure · antagonist (broken, NOT seduced) · core/full · cold → destroyed)

> **Her job in the game:** the **final boss.** The one target you never win over — you *destroy* her.
> Hard-gated behind every other conquest, so she's genuinely the last thing in the game. Taking her =
> the charge-ceiling payoff / the frontier trigger.

**§1 · End-state fantasy — the queen who came to own everyone, reduced to the family's communal slave.**
Margaret is your **blood aunt** (Eleanor's sister), the cold schemer who moved in to seize the estate. She
is the one person you **cannot** seduce, buy, or comfort — she stays defiant to the end. **Her legal
advantage runs entirely through people, not paper:** she controls the say of the grief-incapacitated widower
(Richard) and the backing of the pliable heir (Grayson), while your own claim is weak (the estranged
prodigal who walked out). So you don't out-lawyer her — you **take the men her power runs through.** Seduce
Richard into signing control to *you* (`richard_signed`) and buy out Grayson (`grayson_bought_out`), and her
advantage **collapses** — a schemer with no one left to scheme through. Still defiant with nothing left, she
gets **broken by force:** you intoxicate her, and the two men she once commanded — now wholly yours — **take
her** (a one-and-done forced 3-on-1 you orchestrate), breaking her sexually then mentally. Terminal state:
the patrician aunt reduced to the **household's communal slave** — domestic + sexual servitude, **put to
work on the vice-house floor she schemed to own**, taking orders from the niece (Audrey) she scorned and the
men (Grayson) she used. *(The total inversion: she who would own all, owned by all. The game's peak.)*

**§2 · Voice spec.** Cold, precise, patrician; velvet over steel; she compliments like a threat and never
once raises her voice or says a crude word. Underneath: pure calculation, never warmth — she's always a step
ahead, almost beats you. In the breaking, the control finally shatters. Terminal (slave): hollow, vacant,
compliant — the voice emptied out. **Tier-3 earned in the breaking + the cornering capstones** (the
once-only peaks). One *italic* private thought per appearance — sharp and scheming through the cold war,
then nothing left to think.

**§3 · Stat ladder + gating spine** *(antagonist → destroyed — NOT the two-meter seduction model).*
- **She is not a seduction target — there is no "build her desire" odometer.** Her "lock" **IS the war:** you
  unlock her breaking by completing the prerequisites, not by warming her up.
- **A hidden scheming/pressure track** (antagonist accumulator, `margaret_scheming`) runs across Acts 1–2 —
  her legal/social pressure escalates (the late-act pressure role, Step-2 §5). Never surfaced as a player-
  facing meter (spoils the confrontation); it drives her threat beats.
- **The breaking gates HARD (Form 1, the apex gate):** `richard_signed` AND `grayson_bought_out` AND
  player `corruption ≥ Whore` AND hotel control. Those prerequisites are her lock — that's what makes her
  the genuine final boss the game won't let you skip to.
- **Post-break:** `margaret_slave` opens the **light, repeatable "command/use the family slave" endgame
  menu** (a `npc_margaret.arousal`-or-trait-gated use-loop — *specific acts deferred to Step 5 roster*).
- **Vocab ceiling:** max-explicit. **The breaking is non-con** (intoxicated + forced) — authored as an
  **auto-fire forced capstone** per the game's locked forced-content mode (no consent branch for her). All
  four participants adult.

**§4 · Per-rung pretext shapes** (the war, then the destruction — no seduction rungs):
- *The cold war (Acts 1–2):* verbal sparring, her power moves, legal threats, her watching and **banking
  your missteps as leverage** (her reactive-world flavor — she files, she doesn't grope).
- *The cornering:* the board turns — Richard's signed, Grayson's bought out — and she realizes she's lost.
- *The breaking:* you intoxicate her; Richard + Grayson take her by force; sexual then mental destruction.
- *The slavery:* communal household servitude + the vice-house floor (acts → Step 5).

**§5 · Lane-by-lane map** *(antagonist, capstone-driven — ~10–14 canvases):*
- **L1 hub** — limited charged **cold-war encounters** (where you spar with her; she's untouchable, so the
  menu is verbal/strategic, not escalation rungs). Ungated entry (you can always confront her).
- **L2** — her **presence/pressure** beats: she drops a velvet threat, makes a move, is seen tightening her
  grip. T1–T2, escalating across acts.
- **L3** — **none** (antagonist shape — no vulnerability walk-ins; she appears as pressure, never off-guard).
- **Capstones** — the apex chain (see §6). She is mostly capstone-driven.

**§6 · Capstones** *(the apex chain):*
1. **"Velvet and steel"** (Type B sparring, low-repeat across Acts 1–2) — she threatens/maneuvers; you trade
   blows but can't touch her. Advances `margaret_scheming` + the escalating pressure.
2. **"The board turns"** (Type A) — her advantage collapses. Gate: `richard_signed` + `grayson_bought_out`.
   She's cornered, knows she's lost. Sets `margaret_cornered`.
3. **"The breaking"** (Type A, one-and-done **forced** set-piece, cross-NPC) — intoxicate her; Richard +
   Grayson break her, sexually then mentally. Gate: `margaret_cornered` + player `corruption ≥ Whore` +
   hotel control (+ both men owned). Auto-fire forced capstone (no consent branch). Sets `margaret_broken`.
4. **"The family slave"** (Type A, terminal) — reduced to the household's communal slave (domestic +
   sexual + the vice-house floor). Gate: `margaret_broken`. Sets `margaret_slave` → **opens the light
   command/use endgame menu** (acts → Step 5) AND is the **charge-ceiling payoff / frontier trigger.**

**§7 · Per-NPC anti-patterns.** Don't make her seducible or winnable by charm — she's the one you *destroy*;
**no romantic yielding** (we cut that). Don't make her touchable early — the hard gates (both men + hotel +
max corruption) are what make her the real final boss; never let the player skip to her. Keep her
**formidable and a step ahead** through the cold war — she should almost beat you (no incompetent-villain).
The breaking is **one-and-done forced** (the game's locked forced mode), not a repeatable rape. Her hidden
scheming track is **never surfaced** as a meter.

**§8 · Wiring contract (place in the machine).**
- **SETS:** `margaret_scheming`, `margaret_cornered`, `margaret_broken`, `margaret_slave`, and the
  player-mirror `margaret_stage`.
- **READS (the apex gate, Form 1):** `richard_signed` + `grayson_bought_out` (her two pillars stripped) +
  hotel control + player `corruption` (max). **The breaking capstone pulls in Richard + Grayson as
  participants** (reads their owned/terminal flags — cross-NPC).
- **SOURCE for:** the **FRONTIER** — `margaret_slave` is the charge-ceiling payoff that drops the game into
  its livable plateau + the greyed next-hook.
- **The legal backbone (LOCKED):** Margaret's whole advantage = controlling Richard's say + Grayson's
  backing while your claim is weak; **`richard_signed` is the legal kill-shot** (you took the man her power
  ran through), `grayson_bought_out` removes the other heir, and **Halloway** is the neutral arbiter who
  watches control shift from her to you over the game.
- **Disciplines:** D1 ✓ — her **entry** (the cold-war sparring) is ungated from arrival; only the **breaking**
  (the conquest) gates on the other arcs. D2 ✓ — Margaret reads Richard + Grayson; they don't read Margaret
  (no cycle). D3 ✓ — the breaking ships a locked-visible telegraph naming the prerequisites ("She can't be
  touched while she still holds Richard's confidence and Grayson's backing — take them first").

**§9–10 · Acceptance.** Done when: she is authored as an **antagonist, not a seduction** (no desire
odometer; the war is her lock); the breaking is **hard-gated** on `richard_signed` + `grayson_bought_out` +
max corruption + hotel control (the genuine final boss); the breaking is a **one-and-done forced cross-NPC
capstone** (Richard + Grayson as participants, per the locked forced mode, all adult); she's formidable and
escalating through Acts 1–2 (the late-act pressure); `margaret_slave` opens the light endgame use-menu
(acts → Step 5) and triggers the frontier; the legal backbone is consistent across Margaret/Richard/Halloway.

---

### Lorna — R7 brief  ✅ (corrupting on-ramp / ally-enabler · service · LIGHT/peripheral · NOT a sexual target)

> **Her job in the game:** the **one genuine ally** — not a conquest. The veteran bartender who teaches you
> the *business* of corruption (the vice trade + the empire), opens the door to your own dirty-work
> self-corruption, and becomes your trusted right-hand. **Kept deliberately LIGHT** (peripheral — no
> two-meter arc, no escalation ladder, no big capstones; gold-plating her is the failure).

**§1 · Role & end-state — the partner you never bed.** Everyone else in the game you take, break, or own;
**Lorna is the exception — the one person on your side by choice.** A trajectory, not a takedown: she starts
as the unshockable lifer bartender sizing up the broke prodigal, becomes your **mentor in the vice trade**
(she drops the first dirty idea and opens each bigger move — comped favors → escort arrangements → the
private floor), and ends as your **trusted right-hand / consigliere** running the floor at your side for her
cut. She owns the **business side of corruption** (the hotel's transformation = `renown`) and is the
**on-ramp** that supplies your own self-corruption (the dirty jobs she hands you); she has **nothing to do
with corrupting the family** — she stays out of the bedrooms. Thematically she's the **mirror**: what you're
becoming, already arrived.

**§2 · Voice spec.** Worldly, dry, unshockable; transactional warmth; "honey," "sweetheart"; frank, never
crude-for-shock. Unbothered by anything — including being caught. RTS-flat throughout (she's peripheral —
no earned Tier-3 capstones). One *italic* private thought when it fits — always shrewd, always counting.

**§3 · Stat ladder + gating spine** *(service → LIGHT, peripheral — do NOT gold-plate).*
- **Spine = a single odometer, `npc_lorna.relation`** (trust), built by working with her / taking her
  advice. **NO `arousal` throttle, NO `corruption` odometer** (peripheral — P5; she's not a seduction
  target). Declared in `[npcs.core_traits]`.
- **Flags** carry her real function: the **vice-trade unlock chain** (the `renown` on-ramp — each tier she
  opens) + `lorna_partner` (the right-hand milestone).
- **No double-lock / no player-corruption gating of her own content** — she's not a lewd target. (The
  *activities she unlocks* are gated on `renown`/player corruption, but that's the player-feeder economy,
  Step 5 — not Lorna's own arc.)

**§4 · Per-rung pretext shapes** (advice, unlocks, info — not seduction):
- *The lessons:* she teaches the trade — drops the first dirty idea, then opens each bigger vice move as
  trust + `renown` grow.
- *The tip-offs:* the insider who sees everything — she's how you learn the board (e.g. where the hotel's
  cash really went → Grayson's gambling; the lay of the family).
- *The mirror (ambient):* you randomly catch **Lorna with a customer** (see §5) — she practices what she
  preaches, unbothered.

**§5 · Lane-by-lane map** *(service, light — ~4–6 canvases):*
- **L1 hub** — *the bar*: Talk / **advice / learn-the-trade** menu (drops dirty ideas; unlocks vice content
  as trust + `renown` climb). Ungated entry.
- **L2** — **1–2 ambient "catch Lorna with a customer"** beats (the bathroom, behind the bar after close):
  voyeuristic, repeatable, low-chance, **never player-involved** — vice-world texture + the literal mirror.
  She catches your eye, winks, doesn't stop. *(Deliberate light addition — characterizes the reactive
  vice-world; not an escalation rung.)*
- **L3** — none.
- **Capstone** — **1, non-sexual:** *"The partnership"* — once the empire's rolling, she throws in with you
  for good as your right-hand. Gate: `npc_lorna.relation ≥ N` + `renown ≥ [tier]`. Sets `lorna_partner`.

**§6 · Capstones.** Just the one above (`lorna_partner`) — peripheral; no first-night, no chain, no loop.

**§7 · Per-NPC anti-patterns.** **Don't gold-plate her** (no two-meter, no arousal throttle, no escalation
ladder — peripheral stays lean, P5). **No player↔Lorna sex** (decided). The "caught with a customer"
ambients are **voyeuristic texture only** — never pull the player in. Don't let her corrupt the **family**
(that's #3, all you). Keep her an **ally**, never something you own.

**§8 · Wiring contract (place in the machine).**
- **SETS:** `npc_lorna.relation`, the **vice-trade unlock chain** (the `renown` on-ramp flags), `lorna_partner`.
- **READS:** `renown` (higher unlocks) + player progress; no cross-NPC lewd gate.
- **SOURCE for:** the **player-feeder / vice ECONOMY** — she's the on-ramp that opens the earning/vice
  content (the `renown` node, Step-2 §4–5); and the **recon/info** that colors the early game (e.g. surfacing
  Grayson's gambling — flavor, not a hard gate on his arc).
- **Disciplines:** D1 ✓ — entry (the bar) ungated from day 1. D2 ✓ — no cross-NPC cycle. D3 ✓ — each vice
  unlock telegraphs its requirement.

**§9–10 · Acceptance.** Done when: she's authored **LIGHT** (single `relation` odometer, no throttle/
corruption meter, no gold-plating); she's the **on-ramp** that unlocks the vice-trade/earning content (the
`renown` node) + the info source; **no player sex**; the 1–2 "caught with a customer" ambients exist as
voyeuristic texture; one non-sexual `lorna_partner` capstone; she never touches the family arcs.

---

## Content roster (Step 5) — the scene inventory

> Every scene that will exist, on paper before authoring. **Grouped by lane** (one table per lane, all NPCs
> pooled — so coverage gaps are visible). Built in three phases: **A = NPC track** (Lanes 1–4, below) ·
> **B = player/world track** (solo feeders + reactive-world, *to do*) · **C = balance + machine verify**
> (*to do*). Each row = one scene + the **want** it serves (no meter-grind rows). The Step-6 beat loop fills
> a row; it never improvises one.

### Phase A · NPC track

#### Lane 1 — Hub rungs (player-clicked escalation menus; 🔁 = repeatable loop rung)

| NPC | Venue | Rung | Want | Unlocks at | Hook |
|---|---|---|---|---|---|
| Audrey | Audrey's room | Talk | re-bond | ungated | warm sister talk; builds her lock |
| Audrey | Audrey's room | Practice: masturbation | "get ready for Danny" | lessons_begin + your corr low + her_corr≥4 | guide her hand; 🔁 ×3 → next skill |
| Audrey | Audrey's room | Practice: kissing (on you) | practice for him | skill_masturbate + your corr ~Lewd | "I can't practice on him, so… you" 🔁 |
| Audrey | Audrey's room | Practice: toy | practice for him | skill_kiss + your corr ~Lewd/Slutty | give her the toy, show her 🔁 |
| Audrey | Audrey's room | Practice: blowjob (toy→you) | practice for him | skill_toy + your corr ~Slutty | the lesbian content ramps 🔁 |
| Audrey | Audrey's room | Practice: anal | the last lesson | skill_sex + your corr ~Whore | 🔁 |
| Audrey | Audrey's room | 🔁 Sex loop (her menu) | (repeatable) | skill_sex (after first night) | her arousal-gated practice/sex menu (acts → unchanged) |
| Grayson | summon / his room | Talk / spar | (recon, early) | ungated | trade barbs; he's on top early |
| Grayson | summon | Order: menial service | break his ego | grayson_serves | fetch/kneel/wait on you |
| Grayson | summon | Order: degrading service | own him | grayson_used + your corr ~Slutty | beg, worship, eat you out |
| Grayson | summon | 🔁 Use him (femdom loop) | (repeatable) | grayson_used | orgasm denial / pegging / cuckold; his arousal-gated |
| Grayson | summon | Command (free) | total ownership | grayson_gives_himself | he serves unpaid, eager |
| Richard | study / office | Talk / comfort | be his person | ungated | sit with him, fill the silence |
| Richard | study / office | Charged closeness | the bond turns | richard_opened + your corr ~Lewd | a touch that lingers |
| Richard | study / office | 🔁 Intimacy loop | (repeatable) | richard_first_night | warm, devoted; his arousal-gated |
| Margaret | shared rooms | Spar / confront | win the war | ungated | velvet-over-steel cold war (no escalation rungs) |
| Margaret | (endgame) | 🔁 Command the slave | (repeatable) | margaret_slave | the light use-menu (acts → Step 5 player track) |
| Lorna | the bar | Talk | — | ungated | dry banter |
| Lorna | the bar | Learn the trade / advice | grow the empire | relation + renown | she opens each bigger vice move (renown on-ramp) |

#### Lane 2 — Ambients (random on room entry; texture)

| NPC | Venue | Scene | Unlocks at | Hook |
|---|---|---|---|---|
| Audrey | hallway / her room | Red-eyed over bills | early | caught crying over the college rejection letter |
| Audrey | her room | Flushed after homework | post-skill | catch her pink-cheeked, flustered you saw |
| Audrey | common rooms | Giddy texting Danny | danny intro'd | she's glowing at her phone |
| Grayson | common rooms | The bookie call | early–mid | overhear a threatening call about his debts |
| Grayson | common rooms | Gambling / sulking | early | hunched over his phone; glaring as you run the house |
| Richard | study | Staring / drinking alone | early | the hollow widower, checked out |
| Richard | hotel / study | Alive again | mid (wants_you) | energized, working — lights up when you appear |
| Margaret | shared rooms | A velvet threat | Acts 1–2 | she drops a warning; tightens her grip (escalates) |
| Lorna | bar / bathroom | Caught with a customer | renown rising | walk in on her mid-act; she winks, doesn't stop (×1–2, voyeur) |

#### Lane 3 — Walk-ins (during a solo activity; happens *to* you)

| NPC | Venue / host | Scene | Unlocks at | Hook |
|---|---|---|---|---|
| Audrey | her room | "Did you do your homework?" | skill set | catch her practicing what you taught (touching herself / the toy) |
| Audrey | your room | Asleep, waiting up | post-opened | she dozed off in your bed waiting for you |
| Audrey | her room (weekday) | Danny study date (host) | danny_bf | join the session → coaching → threesome route |
| Grayson | his room / back office | Cornered by the bookies | mid | catch him desperate, begging for time |
| Grayson | service | Caught liking it | grayson_craves | catch him mid-task, enjoying being owned |
| Richard | study | Broken down | early | catch him falling apart when he thinks he's alone |
| Richard | hotel | Seeking you out | mid | he's invented a reason to need you nearby |
| Margaret | — | *(none — antagonist, no walk-ins)* | — | — |

#### Lane 4 — Capstones (one-shot milestones; Tier-3 prose)

| NPC | Title | Type | Gate | Sets |
|---|---|---|---|---|
| Audrey | You fix everything | A | reconnected | tuition_paid |
| Audrey | The first lesson | A | lessons_begin + corr~15 + her_corr≥4 | skill_masturbate, opened_up |
| Audrey | The first night | A | skill_blowjob + her_corr≥10 + corr~50 | skill_sex (→ loop) |
| Audrey | She got the boy | A | skill_sex + danny_introduced | danny_bf |
| Audrey | Study group (Danny 3some) | B | danny_bf + corr~Whore | 3some_danny |
| Audrey | + Richard (3some) | A (cross) | skill_anal + richard_stage late + corr~Whore | 3some_richard *(father+daughter)* |
| Audrey | + Grayson (3some) | A (cross) | skill_anal + grayson_stage late + corr~Whore | 3some_grayson |
| Grayson | The deal | B | grayson_broke + hotel-money control | grayson_serves |
| Grayson | On his knees | A | grayson_serves + his_corr≥6 + corr~25 | grayson_used (→ loop) |
| Grayson | He stops pretending | A | grayson_used + his_corr≥12 + corr~Slutty | grayson_craves |
| Grayson | Yours for nothing | A | grayson_craves + corr~Whore | grayson_gives_himself, grayson_bought_out |
| Richard | Back to life | A | leans_on_you + his_corr≥6 + corr~20 | richard_opened |
| Richard | The first night | A | richard_opened + his_corr≥10 + corr~35 | richard_first_night (→ loop) |
| Richard | The keys | A | richard_first_night + his_corr≥14 | richard_signed |
| Richard | At your side | A | richard_signed + corr~Slutty | richard_devoted |
| Margaret | Velvet and steel | B | margaret_scheming (Acts 1–2) | (escalates pressure) |
| Margaret | The board turns | A | richard_signed + grayson_bought_out | margaret_cornered |
| Margaret | The breaking | A (forced, cross) | margaret_cornered + corr~Whore + hotel control + both men owned | margaret_broken *(intoxicate + Richard & Grayson; 1-and-done)* |
| Margaret | The family slave | A (terminal) | margaret_broken | margaret_slave *(→ frontier trigger + slave use-menu)* |
| Lorna | The partnership | A | relation + renown | lorna_partner *(non-sexual)* |

> **Phase A coverage note:** Lane 3 is empty for Margaret (correct — antagonist, no vulnerability walk-ins)
> and thin for the men (correct — they're hub/capstone-driven). Audrey carries the Lane-3 density (gateway).

### Phase B · Player / world track — the hotel

> *Your own* scenes (about Catherine, not any one relative): the earning ladder, solo acts, and the
> reactive world. Each row = one canvas. **Defaults marked `[dial]` are the open intensity calls — adjust
> freely.** (Estate + town venues still to do; then Phase C balance.)

#### Earning ladder + solo feeders (track = `solo` — these raise YOUR corruption + money)

| Venue | Scene (canvas) | Archetype | Want it serves | Tier (player) | Hook |
|---|---|---|---|---|---|
| Hotel floor | Work a hostess shift | job (4) | keep the hotel open | corr 0 (bootstrap) | serve guests, pour, carry — the legit entry job, scraps |
| Hotel floor | Flash for tips | flash (2) | afford the outfit that turns heads | corr 15 + exb 10 | bolder outfit; tips for showing skin (the mid-game workhorse) |
| Hotel bar | Tease the regulars | job (4) | earn + warm the room | corr 15 | flirty barwork; regulars tip for the attention |
| Guest rooms | Comp a room for a "favor" | job (4) | first real money / save the place | corr 30 | trade a favor for a booking — the first transactional line |
| Private floor | Take a private client | job (4) | the real money | Slutty (~50) + renown | escort — the deep end opens **`[dial]` full escort empire vs discreet members-only** |
| Private floor | A regular / VIP patron | escalation (3) | a name on the floor | Slutty→Whore (~60) + renown | repeat clients, bolder asks — the mid-rung of the column |
| Private floor | Headline the floor | escalation (3) | the madam's own draw | Whore (~75) + renown | the extreme-public ceiling — carries corruption to Whore (the deepest-content floor) |
| Staff bathroom | Get yourself off after a shift | solo (1) | relief / feed the need | corr 0, ungated | alone, wound up after a charged shift |
| Her old room | Late-night alone | solo (1) | the rot starts inside | corr 0 | private solo act |
| Phone | "Dare me" thread | public-dare (5) | push yourself further | corr 30 + exb 20 | a thread eggs you into bolder floor stunts — **`[dial]` SEED, optional** |

#### Reactive-world events (track = `reactive` — keyed on OUTFIT × place ceiling, not corruption)

| Place (ceiling) | Scene (canvas) | Mode | Outfit gate | Disposition | Hook |
|---|---|---|---|---|---|
| Lobby (civil) | Eyes and a hand | sought / choice | low-cut+ | guests | stares, comments, a hand at your back — capped at the lobby |
| Bar (semi-private) | A regular gets handsy | choice | revealing+ | regular | he pushes; refuse or lean in |
| Guest rooms (lawless) | A guest takes a liberty | **forced** (early) | revealing+ | predatory guest | prey-phase: you're nobody, he takes what he wants — **act-scoped, fades as power rises** |
| Private floor (lawless) | Used on the floor | sought / choice (late) | barely | clients | once it's yours — escort/use on your terms |
| Back office (semi) | Grayson corners you | **forced** (early) | any | Grayson (predator) | the prey-phase brother content, *before* you flip him → feeds his arc |

> **`[dial]` reactive scope:** default has the early **forced** liberties coming from **predatory guests +
> Grayson** (per the locked Step-2 prey-early mode); worst-of-it caps at cornered/used on the lawless
> floors, fading as you rise to predator. Widen (more staff/regulars) or soften (cap lower) as you like.

### Phase B · Player / world track — the estate

> The home: mostly private/solo + self-display. Reactive reactions *here* belong to the family (NPC
> ambients, Phase A bridge — archetype 6/7), so the player-track at the estate is solo acts + exhibition
> that raises `exhibitionism` without targeting one relative.

| Venue | Scene (canvas) | Archetype | Want | Tier | Hook |
|---|---|---|---|---|---|
| Her old room | Touch yourself in bed | solo (1) | feed the need | corr 0, ungated | private solo act — the rot starts inside |
| Bathroom | Linger in the shower | solo (1) | relief + hygiene | corr 0 | self-act in the shower (doubles as a hygiene beat) |
| Common rooms | Dress bold around the house | flash (2) | push your nerve / be seen | corr 15 + exb 10 | parade in something daring; eyes follow *(bridges to family ambients)* |
| Grounds / garden | Sunbathe barely-dressed | flash (2) | push your nerve | corr 15 + exb 10 | lie out where the household passes |

### Phase B · Player / world track — town

> Outside the estate: the clothing **sink** (the reactive-world dial), an exhibition venue (the beach,
> which also hosts Audrey's weekend), and the public-dare line.

| Venue | Scene (canvas) | Archetype | Want | Tier | Hook |
|---|---|---|---|---|---|
| Clothing shop | Buy bolder outfits | sink (economy) | the outfit that turns heads | money sink | the reactive-world dial — revealing wear unlocks bolder reactions |
| Clothing shop | Tease in the changing room | flash (2) | push your nerve | corr 15 + exb 10 | try-on tease; let someone catch a look |
| The beach | Bold swimsuit, be seen | flash / escalation (2/3) | be wanted in public | corr 15→30 + exb 20 | public exposure *(also hosts Audrey + Danny's weekend — Audrey arc)* |
| Public / street | Public dare | public-dare (5) | push yourself further | corr 30 + exb 20–30 | the escalating public-dare chain *(ties to the phone "dare me" thread — `[dial]` optional)* |
| College | Drop in on Audrey | story special (9) | (Audrey-adjacent) | — | visit / tuition errand — light, feeds Audrey's arc |
| Bank / lawyer | (Halloway — the will & deadline) | story special (9) | — | — | structural pressure beats, not lewd (the foreclosure clock) |

> **Town reactive:** strangers react to outfit at a **civil-public ceiling** (stares/comments; bolder in
> seedier corners) — light, `sought`/`choice` only (no forced in public town, by default).

### Phase C · Balance + machine verify

> Player-corruption scale = **0–100, 4 bands** (Pure 0–24 / Lewd 25–49 / Slutty 50–74 / **Whore 75–100**) —
> the roster's "corr 15/30/45" tiers map onto these. (Exact ints finalized at authoring.)

**1 · Feeder supply vs the floors it must clear (the anti-deadlock check).**
- **Demand (deepest family floors):** Audrey's anal + the threesomes, Grayson's pegging/deepest, **Margaret's
  breaking** all sit at **Whore (~75+)**; the first-night tier sits at Slutty (~50).
- **Supply by band:** Pure/bootstrap (0) — hostess shift + 3 solo acts ✓ well-seeded · Lewd (~25) — flash
  for tips, tease regulars, dress-bold, sunbathe, changing-room, beach ✓ rich · Slutty (~50) — comp-a-room,
  public dare, beach-escalation ✓ ok · **Whore (~75) — only the private-floor client ⚠️ THIN.**
- **FIX (applied):** the **private floor is a 2–3-rung escalation column**, not one row — *take a private
  client → VIP/regular patron → headline the floor* (archetype 3) — so it carries corruption from Slutty up
  to **Whore** and the deepest content is actually reachable through play. *(Reactive-world rows do NOT feed
  corruption — they're outfit-gated — so the climb rides on the job ladder + solo + flash + dares; the job
  ladder is the backbone, hence the private-floor expansion.)*

**2 · The machine (DAG / no-deadlock / D1–D3).**
- **Read-graph:** Audrey → {Richard, Grayson} (late, for her threesomes) · Margaret → {Richard, Grayson}
  (the apex gate) · Richard → ∅ · Grayson → ∅ · Lorna → `renown` (not an NPC). **No cycles → DAG holds.** ✓
- **D1 — no entry gated:** all five entries ungated (Audrey reconnect/talk · Grayson bully/spar · Richard
  comfort · Margaret cold-war · Lorna bar). The economy/cross gates hit **mid/late** rungs only. ✓
- **D2 — no mutual locks:** Richard & Grayson read no NPC; Audrey & Margaret read them one-way. ✓
- **D3 — cross-gates telegraphed:** each brief ships a locked-visible telegraph (Vivian's gone; Margaret's
  "take the men first", Audrey's threesome "bring him further", Grayson's "control the purse"). ✓
- **Core loop closed:** floor work (roster rows) → **money + renown** → private floor → money funds the
  **family hooks** (Audrey's tuition sink, paying Grayson, clothing sink — all roster rows) → conquests set
  `richard_signed` + `grayson_bought_out` → **Margaret's breaking** → `margaret_slave` = **frontier.** Every
  core NPC is placed; the income that funds the next conquest is a real roster row. ✓

**Verdict: Step 5 green** — both tracks present, every row serves a want, tiers populated, the one Whore-tier
thinness fixed (private-floor column), the machine is a verified DAG with no entry gated and the core loop
closed. **Roster complete → ready for Step 6 (authoring).**
