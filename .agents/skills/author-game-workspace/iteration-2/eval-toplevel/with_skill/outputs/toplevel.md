# The Hale House — Step 2: top-level design (World setup / engine)

*Second person. Female PC. Systems: clothing ON, phone ON, rent OFF. This is the rulebook for how the
nurse grows and how that growth makes the hotel answer to her — plain words, no TOML yet.*

**A seed note first.** The fantasy says "three grown children," but the locked cast names only two — Iris
and Tobin. I'm treating the third, absent heir as the **frontier's greyed next-hook** (§6): the estranged
child who's been away and comes home to contest, once the house is already hers. That turns the loose thread
in the premise into a deliberate clip-point instead of a hole. Everything below is designed to the four
locked people: Hale, Iris, Tobin, Vance.

---

## 0. Who climbs — the model call (the crucial fork)

**She climbs. This is the default cascade, not a still-point game.** You start as a broke, competent nurse
with nothing but your post — an outsider — and the whole fantasy is a *rise*: "works each of them until the
place answers to her." That arc lives on **you** changing, not only on the people you move. Second person
seals it: the prose puts the player inside the seducer, the aroused subject of every beat, not behind glass
watching a fixed professional operate.

I considered the still-point read (a cold operator who arrives already ruthless, the double lock sitting
entirely on the family). **Rejected on purpose.** Still-point usually pairs with third person and makes the
player *watch* the heat — a real cooling of the porn — and it throws away the best thing this premise has:
the line-crossing. The heat here is watching a *proper* nurse become the woman who reads the will, drugs the
dose, and lets a guest watch. That only lands if she had a line to cross. So she climbs.

**What "corruption" means in this game.** It isn't generic sluttiness. It's **how far past the line she'll
go — from caregiver to owner.** Every point is a professional/moral boundary crossed: skimming his scripts,
reading the will off his desk, letting the bar's drunks put hands on her for the tips, crossing the
nurse-patient line with the dying man himself. That's the master key.

---

## 1. The cascade + the double lock (the spine)

**You must cross your own lines before the family opens to you.** The lewd content on each Hale stays
locked behind the KIND of act you're depraved enough to attempt — but *befriending* them, *nursing* them,
*earning their trust* is never gated. You build the family's willingness in parallel while you build your own
nerve, and the two converge.

**Three acts:**
- **Fall + Build (Act 1).** Take the post, learn the house. Corrupt yourself through solo/semi-public
  feeders (skim the meds, work the bar floor in something you shouldn't, snoop the phone, the first
  half-clinical touch of Hale that isn't clinical) *and* in parallel warm every family member through
  ordinary talk — pour Tobin's drinks, out-argue Iris, fetch Vance his coffee. Befriending is not
  corruption-gated.
- **Reach (Act 2).** As your corruption crosses tiers, the lewd rungs *appear* on each Hale per the double
  lock. The people you invested in are already unlocked when the door opens.
- **Deepen (Act 3).** First-time capstones with each, then the repeatable loops — the house run as yours.

**The DOUBLE LOCK.** Every lewd scene with a family member needs BOTH:
1. **Your corruption ≥ the tier for that KIND of act** — the door ("am I far enough gone to try this?").
   Built by your own line-crossing feeders; opens for the whole cast at once.
2. **That person's own trait ≥ their threshold for this rung** — the individual lock ("is *he* far enough?").
   Built by working *him* specifically.

Non-lewd interaction (talk, tend, argue, do favors) is ungated — it's how you raise each person's lock in
Act 1 while you corrupt yourself. Engine-wise this rides the standard two-axis gate: player `corruption` floor
+ the NPC's own `relation`/`corruption`.

### The stat set (each leg gates real content — no dead stats)

- **corruption** *(built-in, always present)* — the line-crossing door / the cascade. Gates the *kind* of
  transgression on the table: low = you'll snoop and flirt; mid = you'll skim, blackmail, cross the
  patient line; high = you'll drug a dose, stage a will-signing, take the coercive rungs. **Named content it
  gates in the act we're building now:** the whole family's lewd ladder + the crooked-income paths.
- **money** *(built-in)* — you arrive broke; it's survival AND the fuel for every lever (the outfit that
  turns Vance's head, Tobin's bar debt paid off, gifts). **Rent is OFF**, so money is never a hard
  game-over; it's the sink pressure that keeps you hungry. Gates: buying into the reactive-world outfits and
  the arc-moving bribes/gifts.
- **energy** *(built-in)* — paces the day; nursing Hale, working a bar shift, and working a person each cost
  it; sleep restores. Gates: how many things you get done before the day rolls.

**Legs deliberately left OFF (named in, so none is half-wired):**
- **exhibitionism** — OFF. The being-seen content here is **clothing-driven** (§3) and gated on the worn
  outfit, not on a trained exhibition meter. There's no separate public-display ladder that needs its own
  trained stat, so adding one would be a dead leg. If play later reveals a real "she performs for the guests"
  domain that wants its own meter, it grows in then (a Step-2 lock is the meter set for *now*).
- **fitness / intelligence** — OFF. No body-training arc, no academic domain. Beauty is **not a leg** — it's
  read-only from the worn outfit (`worn_beauty`), owned by the clothing system.
- **Per NPC:** each person's lock is `relation` + their own `corruption` (their willingness), sketched in §7
  and set per character at Step 4.

**Hard vs soft gates, matched to the fiction:**
- **Vance** — *hard*. He's the *visiting* doctor; when you have no leverage and nothing to offer, he's simply
  not in the picture beyond signing a chart and leaving. His deeper content is absent until earned.
- **The east wing** — *hard*. Locked and dark until the house is yours; visible-but-blocked ("the key's on
  Hale's ring, and Iris keeps the ring").
- **Hale, Iris, Tobin** — *soft*. They're always in the house. Low corruption doesn't remove them; it just
  means the daughter's colder, the son's warier, the old man's touch stays clinical. Always reachable, low
  stat degrades the scene.

---

## 2. The desire ladder (the cascade, felt as named wants)

The spine the player reads on the Story-Goals card. Each rung is a concrete *want*, ends in a payoff scene,
and reveals the next. The meter is backstage; the want is onstage. (Kink areas named per rung for the
Step-4 ceiling pass; ceilings themselves declared per-arc there.)

1. **"Keep the post."** *(survival)* You're the hired help in a house that resents hired help — Iris would
   fire you on a whim. Nurse Hale well, take the wage, don't give her a reason. **Payoff:** you're in, a room
   of your own, the run of the ground floor. *Reveals:* the wage is nothing and the family's circling
   something bigger. *(Areas: none lewd yet — the setup rung.)*
2. **"Earn off the books."** You're broke and the wage won't cut it — so pour drinks at Tobin's bar in
   something the guests tip for, and start skimming Hale's scripts for the cash they're worth. The first
   time a drunk's hand lands on your hip and you don't move it, that's the first line gone. **Payoff:** real
   money + your first read on how easy Tobin is. *(Areas: clothing-reactive being-seen, petty crime, first
   forced-adjacent touch.)*
3. **"Turn the son."** Tobin's weak, indebted, and half in love by night three. Own him — the bar answers to
   you, his testimony against Iris is yours, and he'll do the thing you need done and thank you for it.
   **Ends on:** him on his knees in the stockroom, doing what you tell him and grateful. **Payoff:** bar
   income + a wedge against his sister. *(Areas: weak-man domination, transactional sex, blackmail-leverage.)*
4. **"Make the doctor sign."** Vance signs things — prescriptions, competency, eventually the papers that
   move an estate. He'll trade a signature for a favor, and the favors escalate. Work him from smug quid-pro-
   quo to a man who'll sign anything you slide across the desk. **Ends on:** him initialing a competency
   form with your knees under his desk. **Payoff:** the legal machinery starts turning — unlocks the "make it
   official" rungs. *(Areas: coercion/quid-pro-quo, older-man, seduction-as-weapon.)*
5. **"Become his whole world."** Hale is dying and dependent and there is no one left he trusts but the woman
   who tends him. Cross the caregiver line — the sponge bath that stops being clinical, the dose you control,
   the will he rewrites because you're the only kindness in the house. **Ends on:** him signing you into the
   will and weeping that he's glad. **Payoff:** power of attorney / named heir — `hold` climbs hard.
   *(Areas: caregiver-patient taboo, invalid/dependency, older-man — the sharpest charge in the game.)*
6. **"Break the daughter."** Iris is the one obstacle left and she has *seen* you the whole time, filing it
   away. With the son owned, the doctor bought, and the will signed, she's out of allies — so take her too,
   adversary to complicit to owned. **Ends on:** the sharp elder daughter locking her father's study door
   *for* you. **Payoff:** the last resistance in the house gone. *(Areas: adversary-conquest, a proud woman
   worn down, f/f.)*
7. **"Open the east wing."** *(frontier)* The house is yours. Hale's keyring is on your belt, the east wing's
   dust sheets come off, the guests and what's left of the staff answer to you. **Ends on:** you standing in
   the reopened wing that no one else was allowed into, running it. **Payoff / plateau:** the livable
   steady-state — the repeatable loops with each conquered person, the income, the reactive world, all still
   running. *Greyed seed:* the third heir has heard, and is coming home. *(Areas: the full menu, now as
   predator.)*

Every gain on this ladder is you *pursuing a want you hold right now*, never "raise corruption." The waitress
test: you flash for the bar tips **to afford the dress that makes Vance sign**, not to tick a meter.

---

## 3. The reactive world (clothing-driven)

The world reads **what you're wearing**, not a hidden number, and takes liberties scaled to the outfit's
exposure. Nurse's whites = invisible; the dress you bought for Vance = a different house. Every tone shift
goes **lewder/bolder/more predatory**, never warmer. Progression is **access to the clothing** (revealing
outfits are bought — a money sink), not a trait. Engine truth: gate these on **`worn_corruption`**, authored
as Lane 2 / Lane 3 canvases — this is the PUBLIC content clothing is allowed to gate, never an NPC's arc
spine. Per-place ceiling is author-encoded in each canvas's `conditions`, not a location attribute.

**Per-place ceiling × who's standing there:**
| Place | Ceiling | Who reacts, and how |
|---|---|---|
| **Hale's room** | intimate but feeble — a dying man's hunger, grateful and pathetic; no force | Hale: dependent, watches, is tended. High *transgression*, low physical ceiling. |
| **The bar (day)** | stares, comments, a hand "helping" you past | Tobin flustered; sober guests stare. |
| **The bar (after hours)** | groping, cornering — an **early prey window** | drunk guests predatory; Tobin too weak to stop it. Recedes as your power rises. |
| **The lobby** | stares from guests; Iris **banks it as leverage** ("dressing like that around my father — I'll remember") | Iris the schemer files it; guests gawk. |
| **The pier** | catcalls → gropes → cornered — the other **early prey window** (isolated, lawless) | fishermen/locals, crude; recedes with power. |
| **The town** | stares and comments — a **civilized cap**, nothing lands | shopkeepers, passersby; prude-heavy. |
| **The east wing** *(late)* | the transgression ceiling — but by the time it opens you're the **predator**, not prey | yours to run. |

**Three modes:** *sought* (you dressed for it) · *choice* (refuse-or-accept) · **forced** (no refuse/accept).
**Forced is act-scoped** — it lives in the early prey windows (bar-after-hours, the pier) while you're the
broke outsider, and **recedes as `hold` rises** and you become the one the house fears. Gate it on the power
tier, not on place×exposure alone. Engine: forced = an auto-fire capstone-shape canvas (priority ≥ 9, single
Continue, no branch) — there's no zero-choice primitive.

---

## 4. The economy (a corruption ladder, rent OFF)

**Earning and corrupting are the same act.** Income runs legit-low early → crooked-high as you fall, and the
better money is always further down the line-crossing path. One wallet, money is money.

- **The income ladder (multiple paths, anti-grind):**
  - *Legit-low:* the nursing wage — a pittance, paid for tending Hale.
  - *Grey:* work Tobin's bar floor in a revealing outfit for tips (a clothing-reactive scene, not a chore-
    click); skim and sell Hale's scripts.
  - *Crooked-high:* charge the hotel's guests for more than a room; run Vance's little pharmacy on the side;
    later, the estate's own money once you sign for it.
  Blocked on one (bar's dead tonight) → do another (snoop, skim, a guest).
- **Every paying activity IS a scene** — the bar floor is a reactive-world beat, guest work is a scene, the
  skim is a crossing. Never a button that only adds cash. The player **sees the deposit** — coin on the HUD,
  the quest goal's live `current / value` line ("Buy the green dress — $80 / $200").
- **Pressure without rent (the sinks + the clock):** the clothing shop (the reactive-world dial costs money);
  the bribes and gifts that move arcs (Vance's price, Tobin's bar debt, a gift for Iris); and the standing
  clock — **Hale is dying**, and the estate is bleeding money while the family fights, so every day you're
  not in the will is a day the pot shrinks and Iris gets closer to selling the place out from under you.
- **Pressure escalates across acts:** survival-broke early → Iris actively moving to sell / a creditor
  circling the failing hotel late. The *form* escalates; the pressure is constant. No rent meter — the
  decline clock and the broke-pressure do that job.

### What compounds — **the house**

The thing that grows and becomes yours is **the Hale House itself.** Not a dashboard — a set of **states**,
each unlocking a room / a person / a kind of scene. Built as a hidden `hold_stage` player trait, gated with
ordinary `gte` thresholds; surfaced to the player only as the Story-Goals rung it advances (no banded meter
in the sidebar).

| `hold_stage` | State | What the world does — content it opens |
|---|---|---|
| 0 | **Employee** | You have your room and the ground floor. |
| 1 | **Confidante** | Hale trusts only you; his room and his meds are yours to run; Tobin defers. |
| 2 | **Power of Attorney** | Vance signed; you sign *for* Hale; the office opens; the family has to route through you. |
| 3 | **Executor** | Named in the will; Iris and Tobin must deal with you as the heir; the will-fight turns your way. |
| 4 | **Owner** | The house is yours — the **east wing opens**, the guests/staff answer, the frontier plateau begins. |

Whoever joins the house is still an **arc**, never a slot. A *finished* arc becoming a standing resource
(Tobin's bar running itself as income) is form-3 wiring — **deferred (G6)**, not built at Step 2.

Engine reuse: one `money` trait, the bar/guest Lane-3 work hosts that earn, the clothing shop as sink. No
`[settings.rent]` block (rent OFF).

---

## 5. Legibility + pacing

- **Legibility rides the quest cards.** The top Story-Goals card always shows the current want **and the next
  concrete step — place + person + verb + window:** "Earn off the books — work the bar floor for tips,
  evenings 6pm–close" (not "make money"). Each family member's `next` block on their NPC panel names their
  step the same way. Telegraph the next rung locked-visible. **Cross-gates name the other arc:** at rung 6
  the card reads "Iris won't fold while Tobin's still hers — turn the son first," never a silent grey. A rung
  waiting on your corruption names the feeder that raises it. (Card mechanics owned by `quests.md`.)
- **Pacing = tension → release, escalating, then plateau.** Each want ends in a payoff; payoffs climb the
  ladder (a tip on your hip → the son on his knees → the will signed → the wing opened), then flatten into
  the wide livable plateau at the frontier. Alternate big beats (a capstone) with small (a bar shift, a
  snoop). Cap the gap — a near payoff always visible. Don't dump the will-signing early.
- **The endgame escalates in CONTENT, not management.** Owning the house is not a spreadsheet — it's the
  *hottest* beats: the reopened wing, each conquered person's repeatable loop, running the guests. Every
  "upgrade" (a `hold` state) unlocks new KINDS of scenes, never a +income widget.

---

## 6. The frontier (endless sandbox, not a finish line)

- **Local arc endings — KEPT.** Each family member's terminal capstone (you fully own Iris; Hale signs and
  passes) ends a *thread*, not the game. **Hale's death is a local ending** — the payoff of rung 5, not a
  game-over (see the fail-state below).
- **Hard game-ending — DROPPED.** No win-screen.
- **The FRONTIER — rung 7, "Open the east wing," does the three jobs:**
  1. *Payoff at the charge ceiling* — the house that shut you out is yours; you stand in the wing no one else
     was allowed into.
  2. *Livable steady-state* — the repeatable loops with Hale (while he lives), Iris, Tobin, Vance, the guest
     income, and the reactive world all keep running.
  3. *Greyed next-hook seed* — **the absent third heir is coming home** to contest the estate. That's the
     clip-point a later extension bolts onto (and when it's actually pitched, it goes through the five parts +
     heat test — a frontier seed is a promise of desire, not plot).
- **Endless ≠ aimless.** At the frontier the tracker says so honestly: "You own the Hale House. Run it —
  more is coming." Never a blank screen.

---

## 7. The machine (cross-wiring as the depth spine)

One machine, not four arcs sharing a wallet.

**The core loop (the spine).** Nurse Hale → his trust + your wage + house access → that access lets you work
each family member → working them yields the **levers** (Tobin's bar income + his testimony; Vance's
signatures; Iris's fold) → the levers convert Hale's dependency into **legal control** (POA → executor →
owner, the `hold` states) → each state reopens the house and deepens what you can do to everyone → the
reopened house (the wing, the guests) is new content + income. Conquest → access → the next conquest.

**Every core NPC's place in it:**
- **Hale** — the *source*. All authority flows from him; his dependency is what you convert into `hold`.
- **Tobin** — the *cold-start easy entry* + the bar economy + the wedge against Iris.
- **Vance** — the *gatekeeper of documents*; his signatures are what make `hold` legally real.
- **Iris** — the *obstacle/rival*; breaking her clears the last resistance and completes the takeover.

**The wires:**
- **Form 1 (arc→arc depth gate):**
  - *Vance's late rung* (signs the POA / competency papers) is gated on **Hale's stage** — you need his
    dependency high enough that his signature is plausible. Milestone → a shared **player flag** the Hale arc
    sets (`hale_dependent`); "how far along" → the `hale_stage` player trait. Telegraphed: "Vance won't put
    his name to it until the old man's clearly leaning on you."
  - *Iris's fold rung* is gated on **Tobin's stage** — with her brother owned and testifying, she's out of
    allies. Milestone flag `tobin_owned`. Telegraphed: "Iris holds while Tobin's still on her side — turn him
    first."
  - Never a raw cross-NPC trait read — mirror to the player namespace at the source arc.
- **Form 2 (arc↔economy circulation):**
  - *2a (load-bearing):* the **bar income from Tobin's arc funds the outfits and bribes** that reach Vance
    and pressure Iris. The economy is the connective tissue — money earned working the floor buys the dress
    that gets the signature.
  - *2b (flourish):* the guest/bar payout **banded by Tobin's relation** — authored as band-gated sibling
    choices (he skims less off the top as he's more owned).

**The three disciplines (firewalls):**
- **D1 — never gate an arc's ENTRY on another arc.** Every family member is cold-start enterable: Hale from
  hour one, Tobin at the bar, Vance on his visit days, Iris in the lobby. Only *mid/late* rungs cross-gate.
- **D2 — no dependency cycles (DAG).** Hale → Vance; Tobin → Iris. No arc waits on an arc that waits on it.
  (Finalized and checked at Step 5 / Step 6.)
- **D3 — every cross-gate is a locked-visible telegraph naming the other arc's state** (the §5 lines above).
  A silent cross-lock is a soft-lock.

No new ledger field — the machine lives in the design book's `## The machine` section (finalized at Step 5)
and is enforced by ordinary beat `deps` + the `cross_npc`/`economic` beat types.

---

## 8. The opening, the systems, and the fail-state

**The opening / cold start.** First screen: you step off the coast road into the **lobby** of the Hale
House — salt-stained wallpaper, half the lights off, a chandelier under a dust sheet. **Iris** meets you
cold, keys in hand: *"My father's nurse. Not family. Remember which one you are."* Your bag is at your feet;
the sidebar lights money near-zero, energy full; the phone buzzes once — a family group thread already
arguing about the will, so the fight is on-screen from frame one.

**The 2–3 things you can do immediately** (one nudges you down without grinding):
1. Go up to **Hale's room** and start his care — teaches the nursing day-job loop + the wage + the source of
   all power.
2. Find **your room**, drop the bag — teaches the map + the wardrobe (clothing system, at value-zero: nurse
   whites only, the shop greyed-and-named).
3. Go down to the **bar**, where **Tobin's** already drinking his own stock — teaches an NPC on-ramp + the
   crooked-money path (the nudge). Pour for him and the first tip-for-a-look is right there.

**First named want:** *"Keep the post."* **How the world teaches with no tutorial:** the empty grand hotel
tells you it's dying; Iris's line tells you you're an outsider who could be gotten rid of; the phone thread
tells you there's an estate worth fighting over; the greyed clothing shop and the greyed east-wing card tell
you there's a climb. **Ten-minute taste:** you tend a dying man, you're broke in a house full of money, the
heirs are at each other's throats, and there's an obvious crooked door (the bar, the skim) — the player knows
this is a slow-seduction takeover of a household from the inside.

**Speak-back / customization:** the player names the nurse (a `@player` name token — spoken back in prose,
the phone contact, and the quest cards, never baked into labels). No body/look customization and no NPC
relabeling — the four are fixed characters. Player portrait: OFF (not authored this game).

**The systems in play (named in or out):**
- **Clothing — ON.** The reactive-world dial; whites → bought revealing outfits as the money sink.
- **Phone — ON.** Carries the will-fight: the family group thread, Vance's after-hours texts, guest
  bookings, Iris scheming — gated threads that fire on flags + elapsed days only.
- **Rent/debt clock — OFF** (declared). Pressure comes from Hale's decline clock + being broke + Iris's move
  to sell, not a rent meter.
- **Customization — minimal** (the name token only, above).
- **Player portrait — OFF.**
- *Finer authored subsystems* (a "cover" for the skimming, a leverage/blackmail ledger, a guest-management
  loop) are **not forced now** — most emerge once the game is concrete and played; fold them in then.

**The cheat page's diegetic skin:** **Hale's master keyring** — the ring of hotel keys that ends up on your
belt; the page presents as "keys you shouldn't have yet." (The page itself is the standard cheat surface;
only the dressing is the design choice. `dev_mode_enabled` shortcuts stay separate.)

**The fail-state — failure EXISTS, three forms (this world has teeth):**
- **DEADLINE — Hale's decline.** He is dying on a clock. If you dawdle and he passes before you've secured
  the will / POA, the deadline **bites** — it forecloses the *clean-inheritance* route (rung 5's payoff is
  gone). It does **not** end the game: the sandbox continues and you must seize the house the hard way —
  through the children, through Vance's forgeable papers, through Iris. (This is the deliberate fix for the
  advertised-clock-that-never-bites gap: it lands, it costs, it doesn't win-screen.)
- **DECAY.** Neglect a family member for days and their `relation` cools (neglect-keyed per-NPC decay, skips
  anyone you saw that day, floors at 0). Neglect Hale's actual care and his health drops faster — **speeding
  the deadline.** A player-side decay keeps the pressure honest.
- **DANGER.** Push the crooked paths in the wrong place — caught skimming meds, caught reading the will,
  caught in the wrong bed — and an NPC *banks* it as leverage (Iris especially), costing you money, a rung,
  or standing. The place-specific outcomes are Step-4/5's job; here the negative axis is declared live.

Not a forward-only ratchet: the house can turn on you, the old man can die too soon, the daughter can catch
you. Safe would read as dead; this doesn't.

---

*Set `pipeline_phase = "map_design"` — Step 2b next designs the spatial graph (the hotel's lobby / bar /
Hale's room / nurse's room / closed east wing, the pier, the town) with per-location dramatic jobs, access,
and travel friction, before Step 3 casts the four people onto it.*
