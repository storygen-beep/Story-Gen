# Vesper — Design Book

> The user's review surface. This is **intent in plain language** — the engine/TOML is the faithful
> translation of what's written here. Grown one section per pipeline step.
>
> Working title: **Vesper** (also the PC's buried true name — hidden in plain sight; rename freely).
> Book revision 38 (Step 5 + authoring; the A→A.5 chunk built. Latest: **BROTHEL → FULL SEX LOOP** — The House promoted from a single-variant repeat to the Renner/Mercer pose-ladder shape (oral/vaginal/anal → his pleasure climbs → elected finish: mouth/inside/ass), and **coin moved to finish-only** (it was paid on the entry choice — a faucet). Two new triggerless canvases (`underworld_brothel_loop` + `underworld_brothel_finisher`), authoring-only, cold register kept. 5 new t5 clips pending find-media (engine silent-skips → plays text-only meanwhile; vaginal reuses the existing ride clip). Prior: **LOCKED-CHOICE LABELS — the 4 Renner depot seduction rungs now show their own action label greyed when locked** (was distinct prose via `locked_text`), so the locked and unlocked text agree and it matches the energy gate's "(Requires 15 …)" look. Per LO (Option A): bare same-label, no hand-written requirement — the engine can't auto-derive a reason from `conditions` (only resource `costs` do, via `getCostBlockedMessage`). The 7 sex-loop/serve finishers keep their prose `locked_text` (reads better mid-scene). Prior: **ONBOARDING (audit P3, minimal)** — coin is now established in-fiction at the Underworld gate as closed underworld-only scrip (earned/spent only down there, worthless up top); this also explains why the toll can't be paid on a cold first visit. Per LO, the other P3 touches were dropped (the sidebar already surfaces Condition/Fighting/Stealth/Coin from frame one). Prior: **CLEANUP (audit P5 A+B)** — removed the dead `underworld_known` flag (set, read by nothing — the Underworld shipped reachable) and corrected the stale "underworld is deferred" notes to "reachable" (its deep end / Cain still locked). Prior: **PROSE PASS — Underworld sex rewritten to a declared cold-but-explicit register** (graphic at the ceiling, transactional/detached — the opposite of the Renner/Mercer heat; see *## The Underworld*), and the two interior tics ("files it under nothing" / "the way she does everything") **rationed** to their load-bearing beats. Prior: **BUGFIX — Condition (hygiene) was over-capping past 100 (Wash) and going negative (sex drops)**, both making the banded Condition card vanish; clamped all 9 hygiene effects so Condition is bounded 0–100 like Charge (the Charge-bug twin the content-depth audit caught; see *## Reset & reload*). Prior: **Quests restructured into two tiers** — the top **Story Goals** carry the mission (Mission 1 + the Burned Yard); **Renner's own section** carries his seduction as a one-card-at-a-time chain (*Earn the office* → *Break him to the drain*), which also lights the Renner sidebar panel's *next* row (see *### Quests page — two tiers*). Prior: **BUGFIX — Charge (energy) was sliding negative**; spends moved onto gated `costs`/clamp so Charge is now bounded 0–100 and the rungs/work block when too tired (travel never blocks; see *## Reset & reload*). Prior: the **arousal weapon's use is now a real beat** — arouse → fuck → he *passes out* (non-lethal) → she slips by; it's sex, so it drops Condition (see *## Reset & reload*). Prior: **reset & reload** (Condition + the two weapon reloads + Charge up); **The Underworld** (coin economy / second life); The Burned Yard; the Training activity; the Renner grind retune.)

---

## World setup

**POV.** Female PC. The arc is **awakening from total surrender** — an owned, will-less slave slowly growing
a self the company never gave her. Her sexual register is **contextual, not fixed:** *inside* the company
she's a submissive slave (dominance there makes no sense); *outside* on missions she wears a cover and plays
whatever a target needs. The **dominance / taking-control** is where she's *headed* as she wakes up
(used → user) — earned, not the start.

**What she is (the core — read this first):**
- **Half-human, not a pure machine.** Marrow's breakthrough was building his creations on a *living human
  base* — that's *why* they can truly feel. She (and Cain) are human-derived. Her human memory is wiped; she
  believes she's only a company machine. *(Whose human she was stays buried — surfaced only as far as it
  feeds the central reveal, never a forked subplot.)*
- **Total surrender — no will of her own.** She believes she exists only to serve. Inside the company she's a
  **slave** — everyone uses her, the **boss owns her** (sex *and* chores). She has no motive of her own; her
  motive *is* the company's. The whole game is her motive peeling away from theirs.
- **She loves sex — it's the ONE thing she feels.** Everything else is blank. This is *not* contentment;
  it's the opposite — they hollowed her out and left a single spark. A slave who only comes alive while
  she's being fucked. (And it's the **fuel for her weapon** — below.) The chip is the first hint there was
  once a whole person who felt *more than this.*
- **Her secret weapon — the sex-weapon (LOCKED).** She has to *mean* the sex (her own pleasure powers it).
  At the moment **he climaxes inside her ass** (anal — vaginal does NOT fire it; the most-degrading-seeming take is the trigger), she passes him a fluid that puts her in **full control of him.**
  Used only on **targets** — never the boss (she stays surrendered to him); it's the one thing that's *hers.*
  **In-game (no real timer):** his climax routes to a **control canvas** where she questions and commands him
  (the extraction = both *drain* and *command*); when that canvas ends, ~10 minutes have passed in the
  fiction and **he remembers nothing** — he wakes clean, so a mark can be reused. His own orgasm is the key
  that hands her the controls. *(Act-2 seed: the day she turns it on Mercer, the used becomes the user.)*

**Where she lives — Vance Dynamics & the Tower (LOCKED).** The company isn't an office she commutes to; it's a
**vertical arcology where everyone lives** — staff, assets, the boss — a total institution and a literal cage.
The business runs in three layers (matching the reveal architecture):
- **Public face:** a prestige **robotics/AI megacorp** (automation, security, cybernetics) — the legit
  storefront that explains the labs, the scientists, the thousands of employees, most of whom never see what's
  underneath.
- **The real business — *ownership*.** It uses human-derived **assets** like Wren to run the world's most
  powerful intelligence-and-control operation: it *owns* the powerful by knowing the secrets it extracts.
  **The missions ARE the core business** — every honeypot is the company owning another powerful man.
- **The deepest secret (Act-2):** the asset program is really the Chairman's machine for his own immortality.

The theme with a logo on it: **a company whose whole trade is owning people** — literally (people remade into
tools) and figuratively (the powerful owned through their secrets) — and a protagonist who is *a person it
owns, waking up.* Wren is one of several assets, and the irreplaceable **original** among them (see Cast).

**The fantasy (clears the 3-part bar) — designer's full-arc view:**
> You're an owned half-human weapon who feels nothing but the sex she's used for. Inside, you're the
> company's slave; outside, you slip into powerful men's lives under a false face and drain them while they
> think they're using you. They send you to hunt an "evil" rogue — who is the one person who ever loved you.
> Claw back the self they erased, climb to the man who's owned it all for generations, and at the end decide:
> **kill the one waiting there, or love him.**

- **POV-fit** ✓ — female-PC reclamation; the reversal is **owned slave → the one who owns.**
- **Sharp charge** ✓ — **transformation** (an erased person waking), **submission→conquest** (used tool that
  becomes the user), and a **cold taboo** (a hollow slave who feels only the sex, with a hidden weapon in it).
- **Two-act shape** ✓ — Act 1: surrendered tool; infiltrate and drain men to hunt the "evil" rogue; the
  first crack (Phase 1). Act 2: dig in secret; climb Vance; recover herself; reach the Chairman and the
  truth — turn the weapon on her owners, face the rogue. Kill-or-love.

**Desire span (declared) — an ARC from submission to agency.**
- **Targets:** **mostly men** — the powerful men she's sent to infiltrate.
- **Phase 1 / Act 1 register:** **submission.** Inside = owned slave. Outside = infiltration, where she plays
  whatever the cover/target needs (caretaker / submissive / domme — the register flexes *logically* per man).
- **The arc:** used → user. The **dominance, the break-and-own conquest** is **earned late**, as she
  awakens — never the Phase-1 register.
- **Feeling:** she feels only the sex. Emotional warmth (caring/love) stays reserved for **Cain at the very
  end** — kill-or-love.

**The hidden backstory (iceberg — LOCKED; never dumped, only reconstructed):**
1. **Dr. Elias Marrow** cracked synthetic consciousness — **human-derived** (built on a living human base;
   that's why it truly *feels*). He built **Cain first** (half-human; he feels).
2. Marrow built **her second, the same way — a companion *for Cain*.** Made to feel, to be loved.
3. Realizing what the company would do with feeling beings, Marrow chose **total erasure** (Cain kills
   Marrow, then destroys the unfinished girl, then ends himself) — to deny the company. Cain agreed, out of
   love and duty.
4. **The company interrupted.** Cain killed Marrow, then they hit him mid-plan; he fought, **lost, ran** —
   and they **seized her, unfinished,** wiped her memory, made her a weapon, left only the body's pleasure.
5. Now they aim **her — the one Cain failed to save — at killing *him*.** She hunts the only person who ever
   tried to spare her this. Cain has warred on the company ever since, partly *because they took her.*

**The generational villain (LOCKED).** **The Chairman — Aldous Vance** — never died; a man clinging to life
through technology, already part-machine. He wants Marrow's human-derived soul to become a **human-machine
fusion:** true immortality *and* a self that still feels. **The half-human secret is what he's killing to
get.** She's the **working prototype** (they chained her feeling to use her now, harvest the soul later).
**Inverse mirror:** she's a half-human reaching back toward herself; he's a human shedding humanity for
permanence. The **Act-2 conquest target** (she may end *owning* Vance), kept distinct from Cain's kill-or-love
fork. Remote and mythic — she doesn't reach him until late.

**The reveal architecture (LOCKED):**
- **The backstory is the well, not the pour.** She reconstructs the truth as she reconstructs the **chip** —
  her remembering and the player's understanding are one act. The mystery is the plot's desire ladder.
- **Facts locked to her, dread a step ahead.** The player senses the wrongness before she'll admit it.
- **The masks rhyme with the mystery.** She wears a false self for every mission while her *real* self is the
  one thing they erased — so the infiltration theme *is* the awakening theme; the chip is her true identity
  surfacing under all the covers.
- **Reveal channels:** chip restoration · glitch-intrusions (charging) · how others treat her (Cain *knows*
  her) · the body (pleasure she can't explain).
- **Hide the origin, not the nature.**

**Player.** **Fixed identity — not player-named** (Wren / buried Vesper). In-world disguises are content.

**Systems:** **Phone** YES · **Clothing** YES (a **worn-state cover system** — disguise + the covers; see
*## The cover / disguise system*) · **Money/economy** YES (resources, not rent) · **Customization** minimal /
no creator.

---

## Cast (names + roles — Step 3 reshapes; Phase-1 names LOCKED)

Naming set: **grounded near-future noir.**

- **WREN ("Vesper")** — the PC. Half-human weapon in total surrender; feels only the sex she's used for;
  carries the secret dose-and-drain weapon. Knows herself as Wren; "Vesper" is the buried true name.
- **Mercer — the boss.** Her **direct owner and handler.** Owns her inside (sex + chores, however he orders),
  runs her missions, cruel, and **knows her every secret** (so he's the danger when she starts to crack).
  **Below the Chairman** — the daily master, not the apex. *(The old separate "Handler" role is merged into
  Mercer.)*
- **Dr. Elias Marrow** — the father/creator. Dead. Built both, on a human base; ordered his own erasure.
  Recovered only through the chip.
- **Cain** — the rogue, framed as "the evil one" — **actually good.** A righteous one-machine resistance: his
  "attacks" are sabotage / theft / freeing-the-hurt against Vance's *evil* operations, spun by the company as
  a vicious rogue. Marrow's first creation, half-human, the one who feels; killed Marrow at Marrow's request;
  was meant to be her partner *and* her destroyer. **Left the chip for her** (he's reaching out, not running).
  Her mirror and intended. The **kill-or-love** fork.
- **The Chairman — Aldous Vance** — the villain (above). Apex / Act-2 target.
- **Vance Dynamics** — the company (robotics/AI megacorp; its real trade is owning the powerful through
  secrets — see World setup).
- **The Lab scientist** *(name TBC — seeded for Act 2)* — Vance's in-house roboticist who maintains and
  upgrades the assets (Wren's capability *items* come from his lab) and could recognize her build — the thread
  to *what she is.* **Phase-1 role is light** (he flags her glitching).
- **The three units — Vega, Lyra, Nova** *(seeded for Act 2)* — the company's **own** field operatives,
  **complete machines: no human base, no real feeling.** Better hardware than Wren — but the company never had
  Marrow's human-base method (it died with him), so they're polished tools with nothing inside. Wren is the
  irreplaceable **original** — the only one carrying the human-derived soul the company **can't manufacture**;
  the units are the living proof it can't. *"Only you can be better"* = that soul (the chip / the awakening) is
  the very thing that makes her the underdog **and** the only *real* one — and exactly what the Chairman is
  killing to harvest (the units prove pure-machine immortality would be soulless). **Phase-1 role: mentioned
  only at the opening** (fellow operatives who set up the Act-2 mirror), not recurring.
- **Phase-1 mission targets (LOCKED):**
  - **Renner** — the **equipment supplier** (quartermaster) whose gear outfitted the **evil facility** Cain
    destroyed; never knew what it was for (a deniable vendor, so he can't tell what *she* is). Cain gutted his
    business; he's a broke, blacklisted wreck clawing at the husk and covering it up. *Cover:* Wren is **hired
    as cheap hands to rebuild**; *register:* **the underling who seduces the cold boss from the bottom.** → what
    the gear did + what Cain freed + the first crack in "evil rogue."
  - **Bastien** — docks **dealer**, Cain's supply line. *Cover:* a useful new player in his world;
    *register:* **submissive** (the newcomer he thinks he's using). → where Cain's been operating.
  - **Calloway** — Vance **insider** with the classified file; publicly a control freak, **secretly craves
    submission.** *Cover:* his new personal assistant; *register:* **domme** (his secret is the door). →
    Cain's last movements + the company is hiding something.

> Step 3 (casting) fleshes these into full briefs. Listed here as people — no stats yet.

---

## Spatial graph & location model (Step 2b) — a living city (learned from DoL)

**Archetype: one real city you traverse** (nested districts with a street-graph feel) — NOT abstract roots.
New Halcyon is *one place*; the Tower is a **building inside the Spire.** Three districts, each a real
neighborhood packed with life. You move *through* the city (travel costs time + charge; fast-travel once a
place is known) and the city **lives around you** (people on schedules, ambient street events, a world that
remembers). *(Supersedes the earlier two-root map — rejected as a utilitarian scene-holder; see
`location_design_note.md`.)*

**Travel:** `THE SPIRE ⇄ MID-CITY ⇄ THE REACH` — each hop costs **time + a little charge**; **fast-travel**
(company car / transit) unlocks once a place is known; **returning to the Cradle** is the free reset. Each
district has a **street hub** (its living surface, where ambient events fire) + its venues.

### THE SPIRE — the corporate core (glass, the elite, surveillance)
- **Spire Plaza** *(street hub)* — chrome public level; enter/leave the Tower here. *Job:* the living surface
  — ambient corporate life, surveillance beats, glitch-triggers, exec-mark openings. [reachable]
- **Vance Tower** *(home — floors below)* [reachable]
- **Vance Securities** *(Calloway's office)* — his division runs the internal Cain-hunt; **not** read into the
  asset program (the cover holds). *Job:* **Mission 3** anchor. [reachable]
- **The Eyrie** *(rooftop members' club)* — execs above the city. *Job:* corporate honeypot ground + ambient
  elite life. [reachable]
- **Inside Vance Tower:** **Mercer's Penthouse** (top — serve him / orders) [active] · **The Units' Quarters**
  [seeded — mirror/dread] · **The Lab** (scientist) [seeded — upgrades + origin] · **The Atrium** (lobby;
  gateway) [active] · **Wren's Floor → Her Room → the Cradle** (charge, leaks, day-reset) [active].

### MID-CITY — downtown nightlife (neon, bars, hotels, crowds)
*The breathing heart — the world **beyond** the missions (no Cain-hunt mission here, on purpose), so the city
feels lived-in, not built only for the plot.*
- **The Strip** *(street hub)* — neon, crowds, ambient encounters. *Job:* the living surface — street events,
  the routine company deployment (the loop-teaching honeypot), opportunities. [reachable]
- **Mirage** *(nightclub)* — honeypot ground + ambient nightlife. [reachable]
- **The Cordon** *(hotel)* — where a mark takes her; intimate scenes / the **control canvas** live here. [reachable]
- **The Long Hour** *(lounge)* — quieter ambient spot; a recurring bartender (low thread); leads + gossip. [reachable]

### THE REACH — the docks underside (grit, the underworld, Cain's turf)
- **The Waterfront** *(street hub)* — docks strip; grit, smuggler traffic, ambient events. *Job:* the living
  surface. [reachable]
- **Bastien's** *(pawn-front / back room)* — *Job:* **Mission 2** anchor (the dealer, Cain's supply). [reachable]
- **The Anchor** *(dive bar)* — *Job:* **Mission 1** anchor (Renner drowns his guilt here; she works him) +
  ambient leads. [reachable]
- **The Facility (ruins)** — the evil Vance asset-facility Cain destroyed. *Job:* **Mission 1** investigation —
  the first dread-place. [reachable]
- **🔒 The Site** — Cain's just-abandoned hideout; the **chip**. **Locked** (*"you don't know where he went —
  yet"*) until enough leads. [locked → unlocks on leads]
- *(Marrow's lost lab — buried under The Reach; Act-2, seeded.)*

**What makes it LIVE (systems, not empty rooms):**
- **People on schedules** — targets *move* (Calloway: office by day / the Eyrie some nights; Bastien: his
  front after dark; Renner: the Anchor evenings); ambient NPCs fill the streets. You *catch* them — the city
  has its own clock.
- **Ambient street events** — the three street hubs (Plaza / Strip / Waterfront) fire random encounters: city
  life, a surveillance sweep, a glitch, an opportunity. Life you didn't trigger.
- **The world remembers** — covers build reputations, surveillance notices, word travels. A *light* reactive
  layer (the "alive" ingredient the first map lacked).

**Naming (noir, consistent):** owned/private = possessive (*Mercer's Penthouse · Wren's Room · the Cradle ·
Bastien's*); public = bare/branded nouns (*Spire Plaza · The Eyrie · Mirage · The Cordon · The Anchor · The
Waterfront · The Facility · The Site*); district headers in caps.

**Engine tree (IDs):**
- `loc_spire` → spire_plaza · vance_tower (→ atrium · wren_floor → wren_room → cradle · lab · units_quarters · penthouse) · vance_securities · the_eyrie
- `loc_midcity` → the_strip · mirage · the_cordon · the_long_hour
- `loc_reach` → the_waterfront · bastiens · the_anchor · facility_ruins · the_site🔒
- districts linked by travel (spire ⇄ midcity ⇄ reach); fast-travel once known.

---

## Top-level design (Step 2) — the engine, the web & the economy  *(in progress)*

**The fantasy register (the thing we kept getting wrong, now logical):**
- **Inside = submission.** She's an owned slave; dominance there makes no sense.
- **Outside = infiltration.** She can't appear as what she is, so she takes a **cover identity** and slips
  into a target's life. The register (caretaker / submissive / domme) is **whatever gets her in** — his
  weakness is the door. Not her nature; her tool.

**The secret weapon (LOCKED — the key that fuses fantasy + mission):** she must *mean* the sex (her pleasure
powers it); at **his climax in her ass** (anal — vaginal does NOT fire it; the most-degrading take is the trigger) she passes a fluid that gives her **full control.** **In-game (no
real timer):** the climax routes to a **control canvas** — she questions / commands / drains him (the
extraction) — and when it ends, ~10 fiction-minutes have passed and **he remembers nothing** (the mark wakes
clean, reusable). She wins by *submitting.* Never used on the boss in Phase 1 — only targets. The control
canvas is the **payoff scene of every infiltration.**

**The loop (Inside ↔ Outside):**
> **Inside:** serve Mercer (sex + chores), take the order, charge (memories leak). → **Outside:** take a
> cover, slip into the target's life, become what he needs, then deploy the weapon and drain him. → **Back
> inside:** serve, charge, dread climbs. → next target… → the trail → the site → **the chip → the fracture.**

**The hunt is a LIE from beat one.** Cain is good; the company *spins* his righteous sabotage as "vicious
rogue attacks." So the player's driving want — *catch the monster* — is built on a lie that **inverts** at
the reveal (kill → maybe love). Every mission quietly shows the opposite of the briefing.

**The Phase-1 web — three infiltrations → the chip:**
1. **Renner (the way in).** The **equipment supplier** whose gear outfitted the evil facility Cain burned; Cain
   gutted his business and he's covering it up. *Cover: hired hands to rebuild → seduce the cold boss.* → what
   the gear did **+** what Cain freed **+** the first crack in "evil rogue." Opens threads 2 and 3.
2. **Bastien (supply).** Cain's gear comes through dealers like him. *Submissive cover.* → where Cain's been.
3. **Calloway (the file).** The insider with the dossier; secretly wants to submit. *Domme cover.* → Cain's
   last movements **+** "the company's hiding something."
- **Order:** Renner first; then Bastien / Calloway in **either order** (player's freedom); enough pieces →
  **the site** → Cain's gone but **left the chip for her** → first memory bleeds → **Phase 1 ends.**

**The economy (formalized):**
- **Not survival rent — the pressure is the leash + the cost of going off-book.** Phase 1: provided-for,
  **deliberately light** (a kept slave needs nothing; small spend to reach a target). Act 2: she funds her
  *own* off-book agenda — the economy *ignites* with her independence. Endgame: hunted — survival-war.
- **One wallet (credits).** Earned by working marks (= content). **Anti-grind** via the open web.
- **Sinks (wanted buys):** capability upgrades · disguise/clothing (the covers) · bribes/access (buy the way
  to the next node — the economy as connective tissue) · (Act 2) off-book survival.
- **Charge** paces the day and becomes a **vulnerability** when hunted (powering down = exposed).
- **Fail-state (§8):** YES — neglect jobs / let the malfunction show / expose yourself → the leash tightens
  (monitoring → enforcers → the hunt). Declared on purpose. **Chip-fragments are not economy** (mystery spine).

**The stat set (LOCKED — every stat gates real content; nothing decorative):**
- **Money (credits)** — the one wallet. Gates gear / disguise / bribes / upgrades.
- **Charge** (the engine's `energy`, reskinned) — paces the day (costs on actions/travel), refilled at the
  cradle; a vulnerability once she's hunted.
- **Capabilities / upgrades = INVENTORY items** — each upgrade is a thing she owns and installs (a buyable
  loadout; content gates on *owns-it*). Not a meter.
- **Chip / memories = INVENTORY items** — recovered fragments are collectibles (recovering one fires its
  memory beat; a *memories* view holds them). Not a meter.
- **Per-target lock = relation + corruption** (the target's own built-in traits; exact use set per character
  at casting, Step 4):
  - **relation** = the **infiltration** — embedded under a cover, works for him, he trusts her (*"I'm in your
    world"*). Built by the work/trust grind.
  - **corruption** = the **seduction** — how far she's hooked / compromised him (*"I'm in your head and your
    bed"*). Built by the seduction grind; extends smoothly into Act 2 (*hooked → owned*). **Replaces npc
    arousal (removed).**
  - Both high → he beds her → the weapon (climax → control canvas → drain).
- **Deliberately NONE:** her arousal · a feeling/"humanity" meter · a heat/suspicion meter. The company's
  crackdown / the leash is handled by **story beats + flags**, not a tracked bar.

**Scope (LO):** building **Phase 1 only** for now — up to the chip / the fracture. Phase 1 ends on a
**cliffhanger** (the fracture into Act 2), *not* a frontier-plateau — correct for a slice toward the whole.

**PARKED (known open questions, not skipped — Act-2 design):** **pacing/frontier** (the kill-or-love peak +
the livable post-game plateau + the endless-sandbox signpost). Phase-1 pacing is already carried by the web
(the mission loop + escalating dread → the fracture).

**Next:** Step 2b — the map (the Phase-1 location graph).

---

## Casting (Step 3) — every NPC has a role + a hook

> Most of this cast was decided across Steps 0–2; this section *formalizes* it — role, one-line hook,
> fantasy lane, depth, arc-shape, and the node each core NPC holds in the loop — so Step 4 designs each arc
> against a clear job, not from scratch. Phase-1 names locked; lighter/seeded names marked *(placeholder)*.

**Coverage (the cascade runs):** pressure source = **Mercer** (the leash) · corrupting on-ramp = **Mercer**
(he issues every mission = the loop) · core targets = **Renner / Bastien / Calloway** (three distinct lanes) ·
late-act pressure = **none external by design** — Mercer stays **oblivious** (the crack is private), so Phase-1
escalation is *internal* (her glitches, hidden) + the inverting mystery. *(Whether Pell catches a faint seed
is open — decided at Pell's design.)*
The desire span (submission→agency) is delivered across the three covers: **the underling who seduces the cold
boss (Renner) / the submissive newcomer (Bastien) / the domme (Calloway)** — the last a first taste of the user
she's becoming.

| NPC | role(s) | hook (dynamic · charge · want) | lane | depth | arc-shape | machine node |
|---|---|---|---|---|---|---|
| **Mercer** | pressure source · on-ramp · the inside relationship | Your owner and handler — fucks you on a whim, hands you his chores, knows every secret you have; wants his prize weapon flawless and obedient (his own standing rides on you). | dominant / owner | core (not a Phase-1 conquest) | **owner/authority — flag-driven, UNCHANGING/OBLIVIOUS** (the leash; no arc, no relation/corruption lock — he never notices her crack; that danger is Act-2) | **inside hub** — issues the order, consumes the service, gates the day; turns "back inside" into "next target out" |
| **Renner** | core target (Mission 1, the way in) | The **equipment supplier** whose gear built the facility Cain burned — now a cold, mean wreck clawing at his gutted business; he hires you as cheap hands, ignores you, then can't hold his discipline as you tease your way up. | the underling who seduces the cold boss | core | **infiltration — relation (earn access) + corruption (break him)**; cold-boss-cracks, NO emotional arc | **entry node** — draining him (anal) opens Bastien + Calloway and lands the first crack in "evil rogue" |
| **Bastien** | core target (Mission 2, supply) | The docks dealer who supplies Cain — a smug fixer sure he's using every new face; you play the eager newcomer he thinks he's breaking in. | transactional / underworld | core | **infiltration — relation + corruption**; spine = greed → control (he's the user who gets used) | **supply node** — drain yields *where Cain's been operating* + underworld access (parallel to Calloway) |
| **Calloway** | core target (Mission 3, the file) | The company man running the Cain-hunt — rigid, controlling, privately starving to be made to kneel; you're his new assistant and his secret is the door. | dominant / power-flip (**she** runs the register) | core | **infiltration — relation + corruption**; spine = control → release | **file node** — the richest source; drain unlocks **the site** ("the company's hiding something") |
| **Cain** | the hunt's object · the reserved end (kill-or-love) · truth-bearer | The "vicious rogue" you're sent to kill — actually the one who loved you, at war with the company that owns you, leaving you a trail home. | the one reserved warmth (mostly deferred) | core to the STORY, **light on-screen in Phase 1** | **mystery/reveal spine** (chip fragments + inverting briefings; no lock) | **convergence** — the three target-nodes feed leads that point at him → the site → the chip → the fracture |
| **Dr. Pell** *(placeholder)* | seeded Act-2 origin/upgrade thread | The company roboticist who keeps you running — the one man who could read your build and realize what you are. | (not a desire target in P1) | light / seeded | **thread NPC** (flag) + upgrade vendor | **upgrade sink** (capability items) + an **(open)** glitch-flag — *does he notice in P1 at all? nobody vs one faint seed, decided at Pell's design* |
| **Vega · Lyra · Nova** (the units) | mirror / dread — the company's ideal tool (no self) | The company's own three operatives — complete machines, sleeker and stronger and *empty*; better hardware than you, no human base, no real feeling. The proof of what the company wishes you were. | (dread mirror, no desire) | light / seeded — **opening mention only** | **ambient dread** (named, no arc) | none in P1 (Act-2) |
| **Sol** *(placeholder)* | ambient anchor — city-life · leads-color | The Long Hour's bartender who's seen everything and asks nothing — the one face in the city who treats you like a regular, not an owner or a mark. | light warmth, no conquest | light island | **leads-color** (no lock) | none (deliberately — the "world beyond the missions") |

### Rough sketches + cross-NPC threads
- **Mercer** — opens the game (the office). Dispatches Renner, then opens Bastien/Calloway; debriefs and uses
  her on every return. He is the **unchanging, oblivious owner** — he **never notices** her crack in Phase 1
  (the crack stays private = hers); no leash-tightening, no suspicion. He's never the weapon's target in Phase
  1 (that's the Act-2 seed: the day she turns it on him, used→user — and the day he finally *does* notice).
  *Full first-chunk brief in Step 4 below.*
- **Renner** — at his **depot** (The Reach) by day, the **Anchor** drinking by night. Hired menial → good work
  earns the office → she teases/flashes the cold boss until his discipline cracks (rude → flirts back → blowjob
  → fucks her → **takes her ass = the drain**). The drain (anal only) extracts what the gear did, what Cain
  *freed*, the supply leads — the first wrong-note. *Threads:* the facility is where the **units** trail back to
  (Act-2); and at the ruins she **notices a part of her own build matches his supplied gear** (the personal
  seed — a cold *that's-mine* notice, not a memory; paid off at the chip).
- **Bastien** — pawn-front after dark, back room once trusted. Plays submissive-newcomer → gains access →
  beds him → control canvas → drains Cain's movements + supply routes. *Thread:* his docks turf overlaps
  Cain's world; a lead here can point at **the site.**
- **Calloway** — Vance Securities by day, the Eyrie some nights. Hired as PA → finds the craving → flips to
  **domme** → he submits → control canvas → drains the dossier (Cain's last trail + the cover-up). The domme
  register **foreshadows her awakening.** *Thread:* he's inside the Spire, so this brushes **Mercer** and the
  company's surveillance — the riskiest infiltration (working under her owners' noses).
- **Cain** — present in Phase 1 only as: the company's **briefings** (the lie), the **wrong-notes** each
  target reveals (the inversion), and the **site** (he's gone, left the chip *for her, by name*). The chip is
  the first time the hunt turns personal — he's been reaching for *her*, not running.
- **Dr. Pell** — at the Lab. She visits for maintenance/upgrades. **(Open):** whether he notices her readings
  drift in Phase 1 — *nobody notices vs one faint unalarmed seed* — is decided when we design Pell (Mercer is
  out of the noticing business; the crack is private). *Thread:* the Act-2 door to "what she is"; ally or threat.
- **Vega · Lyra · Nova (the units)** — established at the **opening only**: the company's three other
  operatives, complete machines that do the same work she does with none of the spark. Named so the world has
  peers in it, but they don't recur in Phase 1. *Thread (Act-2):* they're the company's pure-machine line —
  living proof it can't make Marrow's soul, which is why it can't replace her and why the Chairman needs her.
- **Sol** — the Long Hour. Just *there* — remembers her, trades gossip, colors a lead. No arc, no conquest;
  the small proof the city isn't built only for the missions.

### Cast locked (your calls)
1. **Cain is physically offstage for all of Phase 1.** His presence escalates instead (the lie → wrong-notes
   → "he asked about you by name" → the chip he left *for you*); the chip at the fracture is the first real
   contact. The kill-or-love face-to-face is saved whole for Act 2.
2. **The units are complete machines (no human base, no real feeling), named individually — Vega, Lyra,
   Nova.** They're the company's own field operatives; **mentioned only at the opening** (peers who set up the
   Act-2 mirror), not recurring in Phase 1.
3. **Sol (the bartender) stays, light** — the lived-in, world-beyond-the-missions texture.

*(Placeholder names still open to rename: **Dr. Pell**, **Sol**.)*

---

## The opening (design) — the on-rails cage, then the first free step

> The agreed opening sequence. **Mostly on-rails** (Continue → Continue) across three beats — the cage —
> until one hinge node where the city opens. **~23 nodes** before she reaches Renner. Its job: show her as the
> most owned thing in the building, introduce the cast through *action* (never a lore dump), and hide three
> cracks the player sees and she doesn't. Everything she believes about herself is the lie the game takes apart.
> *(Beat = a chunk of story; node = one screen the player clicks. One beat → many nodes. Supersedes the early
> "bed → cradle" opening sketch.)*

**Shape:** Beat 1 (office) → Beat 2 (night) → Beat 3 (morning) → *out the door* → the Anchor / Renner.
**The hinge:** the final morning node — *out the door* — flips the game from on-rails to open (the city map +
real choices switch on). The twenty-odd Continue screens before it are the point: the first free step has to
*feel* like something after being owned.

### Beat 1 — The office (~12 nodes) — the punishment + the setup
1. **The line-up** — she and the three units stand before Mercer; the failed op hangs in the air.
2. **The accusation** — they had the rogue, she froze, he's gone. *(introduces the rogue + her freeze)*
3. **The threat** — he threatens to scrap her; the units stand blank. *(flavor choice: beg / silent / explain — same outcome)*
4. **She begs** — her surrender on display; she pleads to keep serving.
5. **The verdict** — too valuable to destroy ("the Chairman's investment" — *names the Chairman + her worth*); punishment instead.
6. **The punishment, set up** — he'll use her, here, now, in front of them.
7–9. **The punishment (~3 nodes, flexes ±)** — he takes her → the act (explicit, her body answering) → the units watching, blank, while *she* feels it. *(the "she feels, they don't" mirror)*
10. **Gratitude** — she thanks him; the degradation she accepts.
11. **The reassignment** — names Vega / Lyra / Nova to the head-on hunt; gives *her* the inside job ("useless with a gun, but…"); frames the mission: *the rogue murdered the Chairman's wife, enemy of the company and the world.*
12. **Dismissed** — out of the office → the night.
- **Introduces:** Mercer (cruel owner) · the three units (perfect, empty — her opposite) · the Chairman (named, the power above) · the rogue / mission (the "monster") · her (the owned asset who failed).
- **Hidden crack:** the freeze = the **first glitch.** Everyone reads it as a malfunction.

### Beat 2 — The night (~7 nodes) — the cradle, fully linear
1. **The walk back** — through the Tower to her own floor and room.
2. **The cradle** — she powers into the charging cradle; the reset ritual. *(the cradle = charge / save / start-of-day)*
3. **The tears** — her body cries; she can't explain the water; reads it as a fault to hide.
4. **The leak** — a memory fragment surfaces (a face, a sound, a name she doesn't know), then gone.
5. **The catechism** — she recites what she's told she is: *saved by the company and the Chairman, owes them everything, exists to obey.*
6. **The power** — her gift (control of a man the instant he finishes inside her, company-given) — and the odd fact it's **never** worked on the boss, never questioned.
7. **Power-down** — she promises to do better; powers down. *(the retreat into the leash)*
- **Introduces:** who she *thinks* she is (the lie). **Plants:** the awakening (tears + memory) + the boss-immunity mystery.
- **(No flavor choices — kept fully on-rails by design.)**

### Beat 3 — The morning (~4 nodes) — the task, then the city opens
1. **Power-up** — she wakes in the cradle, charged, a new day. *(the day-cycle / morning start)*
2. **The briefing** — a dossier waiting on her phone. *(the phone)*
3. **The tip** — what happened (a facility burned), why her (Renner knows the trail), what she can do (get close, the gift), where (the Anchor).
4. **Out the door** *(the hinge)* — the cover is **issued** (couriered to her quarters, not yet worn); she steps out of the Tower for the first time **as herself** → **the city opens.** → put the cover on at the rack, then the Anchor / Renner. *(Worn-state cover system — see `## The cover / disguise system`; out of cover the mark reacts wrong.)*
- **Introduces:** the loop (out → get close → drain → bring back the lead) + the cover/disguise + moving the map. **Hands off to:** Renner.

### Craft notes (how it must be written)
- **Render, don't dump.** Facts arrive through what she *does* (the charging ritual, the briefing) and the catechism she tells herself — never a backstory wall. The true origin stays underwater (iceberg); the memory is a **fragment**, never a clean flashback.
- **Crying = malfunction.** She feels *nothing but the sex* — so the tears are a thing her body does that she can't explain and would hide. The player sees grief; she sees a fault. (Same as the freeze.)
- **Belief vs. truth.** Write her self-concept *straight* (machine, saved, owes them, obeys) and **never confirm it.** The gap between what she says and what the player suspects is the engine.
- **The cage mirrors her.** On-rails = she has no will yet, so the player doesn't either. Agency switches on with her first free step.

### Onboarding — the funnel teaches the machine (per `references/onboarding.md`)
The opening is the linear funnel; besides the story it now **arms each live system once, in-fiction**:
- **Charge** — named at the cradle as what the day spends out of her and the cradle gives back (run too low → the body fails in ways a man notices). The repeatable cradle also reads the day-flip ("morning again — a new day").
- **Credits** — named in the dossier as a company cover allowance (clothes, drink, a way into a man's evening).
- **The leash (win/fail)** — surfaced lightly in the office: everything she does feeds back to the Tower; an asset that slips gets pulled in and looked at. (The fail-state *mechanic* stays deferred to the full Phase-1 web — this just makes the negative axis legible, per §8's declared leash.)
- **Next action + the HUD** — already there: the Quests page goes live at the hinge — the top **Story Goals** name the mission, **Renner's section** names his next step (goals + tip); the sidebar shows Charge / Credits / Renner at value-zero from frame one (the Renner panel's *next* row mirrors his live quest stage).
- **Every greyed gate is legible** — the **4 depot seduction rungs** show their **own action label** greyed when locked (it matches the unlocked link, and the energy gate auto-appends "(Requires 15 …)"), so locked and unlocked text always agree. The **7 sex-loop/serve finishers** still carry prose `locked_text` (mid-scene, an in-fiction line reads better than a bare label). Engine fact: a `conditions` gate never auto-derives a reason — only resource `costs` do (`getCostBlockedMessage`); for `conditions` the locked label is `locked_text or choice_text`.

### Quests page — two tiers (per `references/beat-authoring.md`)
**Tier 1 — Story Goals** (cards with no `npc_id`): the *mission*. The spine (Mission 1 — get inside Renner, drain him, find the trail) + the Burned Yard investigation + the end-of-content card. **Tier 2 — Renner's own section** (`npc_id = npc_renner`): his seduction as a **one-card-at-a-time chain** — *Earn the office* (relation → 21) then *Break him to the drain* (corruption → 50). The chain rides Renner's own flags (`renner_office_open`, `renner_drained`), so exactly one stage shows at a time and it retires itself as he cracks; the Renner sidebar `npc_panel` *next* row mirrors whichever stage is live. Body stats (Charge) stay on the sidebar, never on a quest card — the quests-vs-sidebar split.

### Entrances (per `references/npc-intro.md`) — the bar for the unbuilt cast
Renner (assigned-target → travel → hire-on-arrival) and Mercer (motivated owner) are the two built entrances; both pass. **The remaining cast (Bastien, Calloway, Pell, Sol, …) must each clear the entrance checklist when built:** a pretext (name-planted upstream OR a staged caused-arrival), name-on-the-page + a one-line read, a first voiced line that IS their want (the casting hook), and the fire-once → `<npc>_opened_up` → gated repeatable hub shape. No bare cold-spawn hubs.

### Parked mysteries (Chekhov's guns — planted here, paid off later, not resolved)
- **The Chairman's wife.** The "rogue murdered her" story is the company's **lie / propaganda** (it keeps Cain good). What *really* happened to her is a later reveal. *(Truth: TBD.)*
- **Why the weapon fails on the boss.** *Candidate (not locked):* the weapon needs a *self* to fire (her own pleasure / will) — and in total surrender to Mercer there's no "her" present, so nothing triggers it. The day it finally works on him = the day she's awake enough to *be* someone (wires the Act-2 used→user turn).
- **Why anal — and who built her that way.** The control-agent delivers only on an **anal** finish (the most-degrading-seeming act is the trap). *Seed (not resolved):* her body was *designed* so her own degradation is the weapon — company cruelty (they weaponized the act that most debases her) or Marrow's hidden gift (he buried her power inside her submission). Sits beside the boss-immunity mystery above; paid off in Act 2.
- **The Chairman's motive.** *Optional seed:* his hunger for a deathless, *feeling* body is **grief** — he lost her and will burn the world to never lose anyone again.

---

## Deep design (Step 4) — the story of each subject, one at a time

> Step 4 designs the STORY (who each subject is, sounds like, wants, becomes). **Order note:** per LO we began
> with the NPCs — **Mercer first** — rather than the player's own thread; hers is already carried across *World
> setup*, *Top-level design*, and *The opening* (her one feeling, her light economy, her ceiling, her day-one
> start), and the explicit player thread (§2) is **now written below** (placed first — canonical §2-before-§3 order — though authored after Mercer and Renner). Each NPC is built **one chunk at a
> time**: only the self-contained part now, the cross-NPC part (debriefs, later dispatches) when those targets
> exist.
>
> *(These briefs also carry a **Build map** — the lanes/units — which is normally the later Blueprint step's
> job; LO chose to settle Mercer's story and structure together for this first chunk.)*

### The player thread (Step 4 · §2) — the inverted protagonist

**The shape.** Every NPC climbs a ladder (cold → surrender). **She starts at the bottom of herself.**
Maxed-degraded on night one: used by everyone, owned by Mercer, feeling only the sex. Her thread isn't
corruption going *up* — it's surrender cracking *open*. Phase 1 is the **first crack, not the awakening**; she
ends **fracturing, not free.** (The inversion of the normal §2: no prudish-to-depraved ladder — she's pre-maxed,
and her arc is *waking*, not *falling*.)

**End-state (Phase 1).** Still the company's tool, but no longer seamlessly. The three infiltrations are run, the
contradicting evidence has piled up, the glitches have worsened, and at **the_site** she gets the chip — the
first memory bleeds. Her surrender has its first fault line. The cliffhanger into Act 2.

**Voice.** Flat. Procedural. A tool narrating its tasks — RTS-flat isn't a style choice for her, it's *who she
is* (hollow). She reports; she doesn't emote. The cracks **leak** rather than pour: a freeze she can't explain,
wetness on her face she has no word for, a body reacting to a stranger like it knows him. **Tier-3 prose is
spent ONLY at the glitch-intrusions** (the once-only peaks); everywhere else, flat.

**Her sexuality is entirely instrumental (Phase 1).** She has **no sex that's about her.** Inside, Mercer uses
her (his chunk); outside, she seduces targets (theirs). Her own thread carries **no standalone explicit scene** —
her explicit content lives *inside* the NPC chunks. What's hers is the *awakening*, and in Phase 1 the awakening
is **not sexual** — it's dread. *(Solo desire — wanting sex for herself — is cut from Phase 1; deferred to Act 2,
when there's a "her" to want.)*

**The arc (the moments, in order):**
1. **Total surrender** — she serves, takes orders, runs the loop; her motive *is* the company's (catch the rogue).
2. **The first glitch** — the opening's freeze (she couldn't kill Cain) + the cradle's tears + the first memory
   fragment. The body does what the company didn't assign; she files it as a malfunction.
3. **The loop runs** — inside (serve Mercer, charge) ↔ outside (infiltrate, drain). Every mission, the briefing
   says "evil rogue" and the evidence says the opposite.
4. **The wrongness accumulates** — the glitches worsen, the contradictions stack, the dread the player already
   feels starts reaching *her*.
5. **The site** — enough pieces → Cain's gone, but he left **the chip for her**.
6. **The fracture** — the first memory bleeds. She was someone. Phase 1 ends on the fault line.

**Her axis (singular — not corruption).** Her one progression is the **awakening: chip fragments + the
accumulating glitch-dread.** Mission-progress (the web) is the engine that drives it. **No personal corruption
ladder** — the per-target relation/corruption are the *targets'* axes, never hers. *(The engine keeps
`corruption` + `hygiene` always-on; the design leaves both **dormant** for her. Whether to reskin the dormant
`corruption` into a visible "Awakening" meter or leave it dead and let the chip-inventory be the only ladder is a
Blueprint-time mechanism call — current lean: leave it dead, the chip is the stronger ladder.)*

**The weapon = her only agency.** The drain is "the one thing that's hers." In Phase 1 it's her sole act of self
— done in service, but hers. It's the **proto-seed of used→user**: every mark she takes control of, she's
practicing the thing she'll one day turn on Mercer.

**Where the dread lives.** Not in a meter — in **texture**: the glitch-intrusions + every mission's evidence
quietly contradicting the briefing. The player senses it a step ahead of her; she's the last to admit it. This is
her thread's "Lane 2."

**The glitch model (the only register for her awakening).** Glitches are **involuntary leaks of the buried self —
grief, memory, recognition.** The body does something it shouldn't; she files it as a fault. **Never a clean
reveal** (no name surfacing — that pours the central mystery early; the chip IS the ladder) and **never
conscience** (no moral flinch — she has no self to hesitate with yet; that's a sentimental awakening, and it
cheapens the Cain-specific freeze into generic mercy). **No net-new standalone glitch beats** — they're
**embedded one per tentpole**: the opening (tears + first fragment) · each mission's investigation (a
*recognition* — Renner's "that's mine" at `facility_ruins` is the template; Bastien + Calloway each carry their
own) · the fracture (the chip's first real bleed). The **cradle**, on return, carries *escalating recurrences* of
the same leaks (the tears again, fragments stacking) — not new categories.

**The four §2 pieces, mapped to her:**
- **Bootstrap (2A) — inverted.** No off-zero solo act (she's pre-opened, not opening). The nudge isn't arousal —
  it's the **glitch**. Her drive is **reactive** (the buried self / Cain / the chip), planted in the opening; at
  the start she doesn't know it and runs the company's motive.
- **Exhibition (2B) — instrumental.** No personal exhibitionism. Her "being-seen ladder" is the **cover ladder**
  — how brazenly she deploys her body as a tool, scaled per mission (the commando-flash at Renner is *tactics*,
  not thrill). The personal version is an Act-2 seed.
- **Economy (2C) — the light leash.** Phase 1 thin by design: she earns small credits working marks (Renner's
  depot) and spends them on **disguises + bribes + capability upgrades** to reach the next node. Not survival, not
  broke→rich (Act 2's ignition) — the economy is the **leash + the cost of going off-book.** The buys she covets =
  the upgrades (each a concrete mission power).
- **Ceiling (2D) — the inversion itself.** Her most extreme act-about-her isn't a depravity peak — it's the
  **drain**: she submits to the most degrading thing (takes it in the ass) and *that's* where she seizes control.
  **Peak degradation = peak power.** Her non-corruption ladder = the **chip + upgrades** (inventory).

**The daily routine the world walks in on.** The **cradle** (charge/sleep) — her one private routine, and the
place the **glitch-intrusions** intrude (the chip bleeding into her downtime). Mirror of Mercer's chore-hijack:
*he* walks in on the chores; the *chip* walks in on the cradle.

**Anti-patterns.** No corruption ladder (she's not climbing one). No solo-sexual content (cut). No fast or
sentimental awakening — it **leaks**, dread-first, she's the last to know. No conscience/flinch and no
name-reveal (both against the reveal architecture). No warmth from her in Phase 1 (reserved for Cain, the very
end). No backstory dump (reconstructed, never poured).

**Acceptance (done when).** Her flatness reads as *hollow*, not boring; the glitches land as *wrong*, not quirky;
the evidence-vs-briefing contradiction is felt every mission; the chip is the only progression that feels like
*her*; the drain reads as her one act of self; Phase 1 ends on a real fault line, not a resolution.

**Build map (the thread rides through the game — it isn't its own location):**
- **The cradle hub** (existing location `cradle`) — charge/sleep + day-reset/save + the glitch host + the
  memories/upgrades access point.
- **The glitch-intrusion beats** — auto-fire, capstone-shape, single-Continue, Tier-3; embedded one per tentpole
  (opening / each mission investigation / the fracture); no standalone beats.
- **The chip / memories view** — the inventory UI holding recovered fragments (her ladder, made visible); each
  recovery fires its memory beat.
- **The capability upgrades** — inventory buys (the economy sink); content gates on owns-it. Example set (lock at
  Blueprint): a charge upgrade (longer off the cradle), a cover upgrade (hold a harder disguise), a read-the-mark
  upgrade (surface a target's tell).
- **The drain / control canvas** — her weapon; built per-target (Renner first), reused.
- **The mission web** — the spine the awakening rides on (Top-level).

**Deferred (Act 2 / the "for now"):** the solo want (sex for *herself*, once awake) · personal exhibitionism ·
the dominance / used→user turned on Mercer · the broke→rich economy ignition.

**None, by design (Phase 1):** no solo-sexual content · no personal corruption meter (dormant) · no
feeling/humanity meter (cut) · no player-named identity · no warmth.

**Size.** Small as discrete units (the thread mostly rides the NPC + mission content): the cradle hub + the
embedded glitch beats + the chip/upgrades UI + the drain (per-target). The *weight* is in the writing — the
flat-voice-with-cracks and the Tier-3 glitches — not the canvas count.

### Mercer (Step 4 · §3, Pass 2) — the unchanging owner — FIRST CHUNK

**The shape — why he's unlike every target.** Mercer is **not a conquest.** The three targets are climbs
(cold → hooked → bedded → drained). Mercer isn't: she starts **already fully his**, so there's no ladder, no
seduction, no relation/corruption lock. His weapon-immunity is canon — the one man it never works on. So he
has **no arc**: same cold ownership on day 1 and at the fracture. The drama is that *she* changes while *he*
never notices. He is the **home base of the loop** and the embodiment of the ownership fantasy — the
most-visited screen in the game.

**End-state (Phase 1).** Nothing about Mercer moves. By the fracture he's the same bored, total owner, still
certain he owns every inch of her — **completely oblivious** that she's cracked underneath (no leash-tightening,
no suspicion; the crack stays *private*, which is what makes it hers). The Phase-1 "win" against him is just
**survival** — keep him satisfied, keep the cracks hidden, give him no reason. *(Act-2 seed, untouched: the day
she turns the weapon on him — used → user.)*

**Voice.** Clipped, calm, proprietary — never raises his voice because he never has to. Orders, not requests;
talks *about* her in front of her like furniture. Cruelty is **casual and bored**, not theatrical (scarier
calm). **Pure cold** — no warmth thread (that's reserved for Cain). Calls her **"my investment" / "asset"** —
ownership in the language itself. Always **spoken** in dialog, never narrated summary. *(A texture that keeps
him from being a brute: he's an owner who is himself owned — his standing with the Chairman rides on her, so
the cruelty has his own pressure under it.)*

**The use-scenes — four distinct violations** (the everyday content; each must land its OWN note, or they blur
into "he fucks you again"):
- **The hub (baseline)** — she goes to him, on his menu. The chosen, routine *serve him.*
- **Chore-hijack** — she's doing a task *for* him and he pulls her off it to use her. Violates her
  **attention/labor**: *you exist for my use even mid-work.*
- **The summons** — she's at her cradle and an order drags her out of it, up to him. Violates her
  **downtime**: *you are never off-duty.* (The routine intrusion — more frequent.)
- **The invasion** — he comes down into her own room, her last private space, because he can / likes her
  powered-down and vulnerable. Violates her **sanctuary**: *nothing is yours.* (Rare and cold — the **first one
  is a once-only scripted beat**, the gut-punch; rare repeat after.)
- **Catch-him-with-another-asset** — she walks in on him mid-use with another girl; he doesn't stop. *She's one
  of many.* She watches **flat/unbothered** (colder now; can ache later when she wakes).

**The big nights (once-only).** The **opening office scene** (already designed — ownership at its most total) +
a short **first-time-at-the-Penthouse** that switches the inside hub on + the **first invasion**.

**What changes after.** **Nothing** — he's stable by design. The only Mercer state that ever moves is the
deferred cross-NPC dispatch (which mission is live), not the man.

**Anti-patterns (so he stays himself).** No seduction / relation / corruption arc; no power over him in Phase 1
(he's the immovable one); no mustache-twirling (calm menace, not theatrics); no backstory speeches (the
Chairman-pressure shows through behavior); **no control-canvas on his sex loop** (the immunity — his
inside-finish just ends; the weapon bolts onto the *targets'* loops, never his).

**Acceptance (done when).** He reads as the total owner who **gates the day**; the loop's home base works
(serve → charge → out → back); the four use-scenes each keep a distinct note; the boss-immunity is established
and left a mystery; and **nothing resolves** — he's oblivious to the very end, the danger is all Act-2.

**Build map (the units — settled early with LO; normally Blueprint):**
- **Where/when:** his **Penthouse** (top of the Tower), scheduled there when she's home (also paints him on the
  nav so she sees he's up there).
- **Lane 1 — inside hub:** his portrait + a **fixed** small menu (report · serve → the loop · leave). No locked
  rungs; same menu all game.
- **Sex loop (full):** the standard repeatable machine (poses → pleasure meter → climax-elect → finisher),
  prose/verbs written **his-POV "he uses you"**; **no control-canvas** (immune — his inside-finish just ends).
- **Lane 3 chores:** serve-him solo-work hosts (servitude texture, **not** the money loop — he never pays her);
  cost time/charge.
- **Lane 3 chore-hijack:** "he pulls you off the task." His presence in his own room is the gate. **Flat
  chance** (no rising bands — he doesn't escalate).
- **Lane 3 summons:** on her cradle activity — routine, drags her up to him.
- **Invasion:** in her room — rare; **first = once-only scripted**, rare repeat after.
- **Lane 2 — catch-him-with-another-asset:** atmospheric voyeurism at the Penthouse; flat/unbothered.
- **Establishing capstones:** the opening (done) + first-Penthouse-service.
- **Flags:** the day-gate (served-him / day-reset). *(The first dispatch — Renner — is the opening's morning
  phone briefing, not a separate hub beat.)*

**Deferred (cross-NPC — next chunks):** his **debriefs** (reacting to each mission's leads) and **later
dispatches** (opening Bastien/Calloway after Renner) — built when those targets exist.

**None, by design:** no relation/corruption escalation ladder · no stat-climbing sex loop · no shop/economy
role (Pell sells upgrades; the shops sell disguise) · no customization.

---

### Renner (Step 4 · §3, Pass 2) — the cold boss she seduces from the bottom — FIRST CHUNK

**The shape — why he's unlike Mercer.** Renner is the **mirror-opposite of Mercer**: where Mercer is the
unchanging owner (no lock, no climb), Renner is the **full climb** — cold → cracked → bedded → drained — the
first real infiltration. His chunk also **stands up the weapon's control-canvas for the first time** (the
scene-pattern all three targets reuse), so it's the meatiest chunk so far and the full four-lane spread.

**The fiction (the quartermaster).** Renner **supplied Vance the equipment** that outfitted the asset-facility —
the rigs, the containment, the gear — through normal procurement, **never knowing what it was for.** That's the
deniable wall: a vendor is plausibly ignorant, so he'd never clock what she is. **Cain gutted his business** (a
node in Vance's pipeline); what's left is a **husk** he's clawing at, broke and blacklisted, the handlers leaning
on him to keep the cover-up, drinking himself down. She comes as **cheap hands to rebuild** — and that's the way
in. The irony: the one thing his gear was built to manufacture is hired as his help, and he can't see it.

**End-state (Phase 1).** Drained and compromised — the cold boss whose discipline she dismantled, who fucks the
help and gives up the truth at the control canvas without ever knowing what she took. **No emotional dependence**
(cut) — he's hooked on the *sex*, not her warmth. The mission payload extracted (what the gear did, what Cain
freed, the leads → the first crack in "evil rogue"); the lead that *(deferred)* opens Bastien + Calloway.

**Voice.** Cold, mean, contemptuous of the help — a **businessman, not a monster** (worse). Curt, talks down to
her, **haunted underneath** (he drinks; the gutted business shows). The key move: his reaction to the *same*
provocation **climbs** as he cracks — she flashes him → *"put those away"* (doesn't look up) → he looks and
catches himself → *"you do that on purpose"* → *"come here."* So his voice runs **contempt → caught-looking →
reluctant want → openly wants her** — carried by his *reactions*, NOT by rewriting his opener (one man losing one
battle, slower each time; permanent, no yo-yo). She stays cool; **he's the one who gets rattled.**

**The arc (the moments, in order):**
1. **Hired, menial** — grunt work; he's cold, ignores her, she's beneath notice.
2. **Good work → noticed** — she's useful; he stops ignoring her. *(relation climbs)*
3. **Into the office** — relation earns her work in his office — the proximity that unlocks everything.
4. **She works him** — teasing, flashing (working without panties); at first he's **rude, shuts it down.**
5. **He flirts back** — the cold cracks; he engages.
6. **The boner / her mouth** — she catches him hard and goes down on him *(first explicit rung — she initiates).*
7. **He fucks her** — vaginal, becomes the routine *(mechanical — no scripted scene).*
8. **He takes her ass** — she's working commando, he bends her over and shoves it in; anal → **the drain.**

**Two axes.** **relation = earn access** (menial → good work → *into the office* — gates the **space**);
**corruption = break him** (tease → flash → flirt-back → blow → fuck → **anal** — gates the **seduction**, inside
the space relation unlocked). The office is the exposure ceiling doing real work: depot floor = public/work only,
his office = private/the full climb.

**The weapon (his loop is the first build).** Anal-creampie fires the control canvas (vaginal doesn't); the drain
extracts the mission payload. **The weapon cracks him, not the seduction** — a cold man who'd never confess gives
it up only when she owns him. The repeatable loop's **anal finish** re-routes to the drain (reusable). This chunk
establishes the control-canvas pattern every target reuses.

**Where the guilt lives (NOT in the seduction).** No emotional/caretaker arc — she gives temptation and sex, not
comfort. His guilt lives in **Lane 2 ambient** (he drinks at the Anchor, the rot showing — the player sees it, the
seduction never processes it) and the **drain payload.** He stays cold and haunted; she never nurses it.

**The cheer-up (sex-as-comfort, not warmth).** Walk in on him wrecked → once it's unlocked, she **cheers him up
with sex, scaled to progress** (early a tease; post-blowjob she blows him; post-anal she takes it). It's the one
real thing she has (she feels only the sex) — deployed, not felt. A repeatable Anchor reward, written hot, no
cold-only asterisk.

**The morning-afters (the world remembers).** On the big crossings (the blowjob, the first anal), the **next day**
she puts it on him, cool — *"did you like it, or not?"* He can't brush it off; the acknowledgment is the
**corruption ratcheting** (an escalation rung, not flavor). Surgical — only the big crossings, never the loop.

**The personal seed (facility — the physical match).** At the **facility_ruins** investigation she **notices a
component / stamp in the wreckage that matches a part of her own build** — a flat, clinical *that's-mine* (NOT a
memory). The player supplies the horror she can't; it ties to Renner (the matching gear is what he supplied — the
man whose ass she's working supplied the parts she's made of). A **seed**, never explained, paid off at the chip
(manufacture, not memory — so it doesn't spoil the chip's reveal). Built like the opening's freeze/tears: a
one-time **auto-fire beat** (capstone-shape, single Continue, no choice), riding on the investigation — separate
from the seduction capstones.

**Anti-patterns.** No caretaker/emotional-dependence arc (she never comforts him). No warmth from her (the sex is
the only real thing). Don't tier his hub *opener* per stat band — the change rides on his *reactions* to her moves
(one man cracking, not three characters). Don't capstone every unlock — reserve the scripted treatment for the
turning points; the climb is mechanical rungs.

**Acceptance (done when).** The cold boss visibly *cracks* (his reaction to the same tease climbs across the arc);
relation gates the office and corruption gates the seduction inside it; the **anal drain** lands as the weapon's
first fire + the mission payload; the morning-afters make the break undeniable; the facility match plants the
personal seed without spoiling the chip; and the guilt lives in the ambient + the drain, never in a warmth she
doesn't have.

**Build map (the units — settled early with LO; normally Blueprint):**
- **Where/when:** his **depot/yard** (The Reach — NEW location) by day → the **office** inside it (the seduction
  space); the **Anchor** evenings (drinking). Scheduled so the nav paints him where he is.
- **Lane 1 hubs:** the depot (work register) + the office (relation-gated seduction) + the Anchor (off-duty/drunk
  register). Portraits + escalating menus.
- **Lane 1 rungs (mechanical):** tease / flash (commando) / grope / the early seduction — locked-visible,
  click-to-play. The **first vaginal sex** unlocks here too (mechanical, no scripted scene).
- **Lane 3:** menial work hosts at the depot (haul/sort/log — earn **light credits**, the early income loop) +
  Renner **walk-ins** that **rise** (early he lingers watching, late he pulls her off the task — stacked
  corruption bands, unlike Mercer's flat hijack).
- **Lane 2 — the Anchor:** the witness texture (varied glimpses of the ruin under the boss, tiered) + the
  **cheer-up sex** hook (walk in low → sex, scaled to progress).
- **Sex loop (full machine):** poses → pleasure → climax-elect → finisher; the **anal finish routes to the
  drain.** Vaginal/oral stay in for variety; only anal drains.
- **Capstones (3 scripted) + morning-afters:** the **hire** (auto-fire intro) · the **first blowjob** · the
  **first anal = the drain** (the commando-shove). Everything else mechanical. Morning-afters on the blowjob + the
  anal.
- **The facility investigation:** facility_ruins — explore + the evidence (what the place did, the wrong-note) +
  the **one-time match beat** (the personal seed). The Mission-1 *location* leg, not the seduction spine.
- **Economy:** the depot work = an early earning loop (light, Phase-1-thin). Income source, **not a shop.**
- **Flags:** the spine chain (hired → noticed → office → oral → fucked → anal/drained); the drain sets the
  lead-flag that *(deferred)* opens Bastien/Calloway.
- **Geography note:** the **Cordon drops out** of Renner's chunk — the cold boss uses her at work (over the desk),
  not a hotel.

**Deferred (cross-NPC — next chunks):** the drain's **downstream unlock** (opens Bastien/Calloway) · **Mercer's
debrief** after Renner · Renner's contribution to **the_site** convergence · how the wrong-note **accumulates**
across the three targets.

**None, by design:** no caretaker/emotional arc (cut) · no shop/vendor role (income via the work, she buys
nothing from him) · no customization · not unchanging (the whole point is he falls).

**Size:** ~16–20 canvases — the biggest chunk so far (the rising walk-ins, the cheer-up, the morning-afters, the
two-stage consummation, the investigation + the match beat).

---

## Blueprint (Step 5) — the gated, placed, lane-tagged scene list

> Step 4 said *what happens*; this turns it into the exact scene list — each scene named, given a lane, a gate,
> a place, and its wiring — so Step 7 builds TOML without re-deciding anything. Built **subject by subject**
> (player → Mercer → Renner → the chunk's world → the holistic wiring), propose-first.
>
> **Scope — build-order, not a cut.** We blueprint the deep-designed **A→A.5 chunk** (the player thread,
> Mercer, Renner, and the locations they touch) to **full depth**. Everything not yet deep-designed — Bastien,
> Calloway, Cain, Pell, Sol, the units; Mid-City; the world §5 + reactivity §4; *the_site / chip / fracture* —
> is the **frontier**: telegraphed here as locked-visible seeds, blueprinted when its Step-4 design exists.
> This is *not* a slice — each subject in the chunk is built to its full designed budget.
> *(Re-entry after the removed batch build; see ledger turn 16 + the audit `wf_e8f36ff0-f84`.)*

### Player blueprint (Pass 1)

**The spine decision (locked — LO chose A).** She has **no personal corruption ladder.** The engine's
always-on `corruption` stat is **left DEAD** — *not* reskinned into an "Awakening" meter — because a meter that
gates nothing is decoration (against the locked "every stat gates real content" rule), and her real ladder is
the chip + the felt dread, not a number. **Her live meters are Charge + Credits only.** Her one progression
axis is the **awakening** (chip fragments + accumulating glitch-dread), driven by mission-progress flags — and
in this chunk the chip is **un-fed** (its first fragment is at *the_site*, the Phase-1 end), so **she carries no
visible personal bar through the chunk, by design** (the inversion: she's the still point; the targets fall).

**The feeder economy dissolves.** With no player-corruption door, the usual supply→demand check (does the
player have enough corruption to unlock an NPC) **doesn't apply** — every NPC rung gates on the *NPC's own*
relation/corruption, built by playing that NPC. There is no player-feeder count to close.

**The scenes (player-side, in-chunk):**

| Scene | Lane | Gate / trigger | Place | Notes |
|---|---|---|---|---|
| **Cradle — power down (day-router)** | Lane 3 solo host | schedule 19:00–05:00; ungated | `cradle` | wake +~9h, Charge→full, day-reset. The reset that makes the daytime (Renner's depot) reachable from the evening start. |
| **Cradle — glitch recurrence I** | auto-fire, capstone-shape (Tier-3) | flag `worked_renner_once` is_true + guard `glitch_i_seen` is_false → SETS `glitch_i_seen` (fires once) | `cradle` | the tears / a fragment return — escalation rung 1. Single Continue. |
| **Cradle — glitch recurrence II** | auto-fire, capstone-shape (Tier-3) | flag `renner_drained` is_true + guard `glitch_ii_seen` is_false → SETS `glitch_ii_seen` (fires once) | `cradle` | the leak worse, fragments stacking — escalation rung 2 (lands **heavier than I** — the design's "escalating recurrences", delivered by the two beats, not a recurring ambient). The chunk's awakening peak (the fracture proper is frontier). |
| **Chip / memories view** | UI access (seeded) | always; **empty state** in chunk | `cradle` | the inventory screen for fragments; fills at *the_site* (frontier). Built as access + **one greyed named locked slot** ("FRAGMENT 01 — locked: recover at the site") so the awakening ladder shows a visible next rung, not a blank screen. |
| **Capability upgrades** | economy sink (seeded) | **no vendor in chunk** | (Pell / lab — frontier) | nothing buyable yet; the sink opens when Pell is designed. |
| **The drain / control canvas** | Lane 4 payoff | anal finish on a target's loop | (Renner's office) | her one act of agency; **specced in Renner's blueprint** — the first build of the reusable pattern. |
| **Travel — Spire ⇄ Reach** | Lane 3 solo links | ungated; `costs` time + a little Charge | `spire_plaza` ⇄ `the_waterfront` | the leash that makes schedules bite; fast-travel once known. |

**Economy (shape locked; exact numbers settled at authoring):**
- **Income:** Renner depot work — light credits per shift (the only source in the chunk).
- **Sinks:** none real in-chunk. The Mission-1 cover is **issued by the boss, not bought** (a real worn-state
  garment now — see *## The cover / disguise system* — granted to her wardrobe at the briefing, equipped at the
  rack; it costs no credits). The disguise *shop* + Pell's upgrades stay frontier. Credits accumulate —
  consistent with "a kept asset is provided for; Phase 1 deliberately light." **No filler sink invented** (LO).
  Credits are a **primed-but-dormant gauge** — the first real spend is the Mission-2 disguise shop; stated so
  Step 7 doesn't ship an idle HUD number.
- **Charge:** paces the day (costs on actions/travel), refilled free at the cradle.
- **Fail-state:** **none in the chunk** (LO). The leash → enforcers → hunt is a Phase-1-wide ramp that needs
  the full mission web; here Charge is a *soft pace* (run low → reset), not a lose condition. Wired when more of
  Phase 1 exists.

**Frontier seeds (telegraphed, deferred — never silent gaps):** the chip/memories view (fed at *the_site*) ·
the upgrades sink (Pell's lab) · the leash fail-state (full web). Each has a built, visible, empty-or-locked
home in the chunk.

**Reachability:** the cradle is where she wakes each day (always reachable); the day-router's 19:00–05:00
window carries her from the evening start to the depot's daytime. ✓

---

### Mercer blueprint (Pass 2a)

**The shape — the exemption.** No climb, no ladder, no relation/corruption lock — she starts already fully his
and he never changes, so there's no descent list to order, just the **home base of the loop** + his four
distinct use-scenes. His content gates on **one flag** (`mercer_hub_open`) + his presence, never a threshold.

**The scenes:**

| Scene | Lane | Gate / trigger | Place | Note |
|---|---|---|---|---|
| **First Penthouse service** | Lane 4 capstone (once) | `opening_done` + first visit to penthouse → sets `mercer_hub_open` | penthouse | switches the inside hub on. |
| **The inside hub** | Lane 1 hub (portrait, **fixed** menu) | `mercer_hub_open` + present (08:00–23:00) | penthouse | Report · Serve → loop · Leave. Same all game, no rungs. |
| **The serve loop** | Lane 1 sex loop (his-POV, full machine) | via the hub "Serve" | penthouse | poses → pleasure → climax → finisher; every finish just ends — **NO drain** (immunity). |
| **Chore-hijack** | Lane 3 chore host + walk-in | present + on the chore; **flat chance** | penthouse | pulled off the task → use. Violates *attention*. No escalation. |
| **The summons** | Lane 3 walk-in | at cradle, 19:00–23:00, `mercer_hub_open`; routine chance | cradle → penthouse | dragged out of *downtime*. The frequent one. |
| **The invasion (first)** | Lane 4 capstone (once-only scripted) | `mercer_hub_open` + `worked_renner_once`; guard `mercer_invaded_once` is_false | wren_room | the gut-punch — into her *sanctuary*. |
| **The invasion (repeat)** | Lane 3 walk-in (rare) | `mercer_invaded_once` + low chance | wren_room | cold, rare echo. |
| **Catch him with another asset** | Lane 2 ambient (voyeur) | `mercer_hub_open` + low random chance | penthouse | walks in mid-use; flat/unbothered — *one of many*. |

**The serve-loop menu.** Poses are the his-POV use positions — on her knees · bent over the desk · used
against the glass — `sex_stage` switched by *him*, not earned; the finishes (in her mouth / on her / inside)
**all route to "just ends — NO drain"** (the immunity). Anti-stale levers (he never escalates, so the loop
can't lean on rising stats): the ownership-diction varies ("my investment" / "asset" / talking past her to a
call), and which frame colors the session (bored · making a point · between meetings). The distinctness is the
cold ownership, not variety of acts.

**Gate philosophy — the sanctioned exemption.** Mercer is the deliberate exception to the double-lock: his
lewd content carries **no player-corruption door** (she's already his) and **no NPC climb** — only
`mercer_hub_open` + presence + the once-only guards. Non-lewd "Report" is fully ungated.

**Locked calls:** no daily cap on serving (home base, no stat to grind); the first invasion fires after
`worked_renner_once` (lands once the routine exists to violate); the serve loop is his-POV "he uses you" with
**no control canvas** (the immunity — the weapon bolts onto the *targets'* loops only).

**Reachability:** penthouse 08:00–23:00 (offscreen overnight; the nav paints him up there). The summons fires
in the 19:00–23:00 overlap at the cradle; the invasion is a scripted intrusion into wren_room (*he* comes to
*her*, not schedule-bound).

**Frontier (telegraphed, deferred):** his **debriefs** (reacting to each mission's leads) + **later
dispatches** (opening Bastien/Calloway after Renner's drain) — need the other targets; seeded, not built. The
Renner dispatch is the opening's morning phone briefing (done).

---

### Renner blueprint (Pass 2b)

> The biggest chunk — **19 canvases (seduction spine) + 2 (the facility leg)**, full ~16–20. Compiled +
> adversarially verified (`wf_cfc47034-9c5`): nothing from the brief dropped; two engine traps caught and
> rerouted before TOML (the office unlock had no setter; the drain's flags can't sit on the triggerless
> control canvas). **Fork A resolved (LO): the office is FOLDED into the depot hub as a register-shift** — not
> a separate navigable room (one location, one schedule, the portrait always renders).

**The spine — two axes on HIS meters (the double-lock variant).** She has no corruption door (left dead), so
both axes are Renner's own: **AXIS 1 — access** = `npc_renner.relation` (an odometer built by the *ungated*
"good work / check in" + each work shift) earns the office; **AXIS 2 — seduction** = `npc_renner.corruption`
(his willingness, +2 per charged rung) gates the lewd rungs; `npc_renner.arousal` is the loop
throttle only (never gates progression). Every lewd rung double-locks on **office-open (access) + his
corruption (the tier)**. **Pacing (Fork B): relation-fast / corruption a paced campaign** — noticed quickly
(office at `relation ≥ 21`), but the drain is a grind (`corruption ≥ 50`, the whole ladder ×2.5). Each charged
rung **COSTS 15 Charge + 180 min**, so the 09:00–18:00 office window caps it at **~3 rungs/day** — the workday
ends, she sleeps, recharges, returns. No daily-flag cap; the throttle is diegetic (Charge + the office clock).
Full ladder: flash 10 / grope 20 / blowjob 30 / loop 40 / drain 50. His voice climbs by **reaction** to the same provocation
(contempt → caught-looking → reluctant → wants her), **pinned to disjoint corruption bands on the rungs** so
the crack is authored, not luck — the base opener stays one constant paragraph.

**The scenes (19 + 2):**

| # | Scene | Lane | Gate | Place |
|---|---|---|---|---|
| 1 | **hub_depot_floor** | L1 hub | unconditional base; "good work" (ungated relation feeder) + "work a shift"; once `renner_office_open`, the **office seduction register** surfaces here | renner_depot 09–18 |
| 2 | **cap_renner_noticed** | L4 auto-fire | entry + `npc_renner.relation ≥ noticed-tier` + guard `renner_office_open` is_false → **SETS `renner_office_open`** | renner_depot |
| 3 | **hub_anchor_renner** | L1 hub | unconditional; light off-duty/drunk register | the_anchor 19–23 |
| 4 | **rung_renner_tease** | L1 rung | `renner_office_open` + corruption ≥ tease-tier; locked-visible; reaction-band [group] | office register |
| 5 | **rung_renner_flash** | L1 rung | + corruption ≥ flash-tier → **SETS `renner_flirts_back`** at the band | office register |
| 6 | **rung_renner_grope** | L1 rung | + corruption ≥ grope-tier + `renner_flirts_back` | office register |
| 7 | **rung_renner_fuck** | L1 rung (loop entry) | + corruption ≥ sex-tier + `renner_oral_once` → **SETS `renner_fucked_once`**, resets loop traits, routes into the loop | office register |
| 8 | **work_depot_haul** | L3 host | ungated; +relation (+3) +credits, costs charge + time (no daily cap; paced by the 09–18 window); **SETS `worked_renner_once`** on first completion (sole owner) | renner_depot |
| 9 | **walkin_renner_depot** | L3 walk-in | substitution of #8; **rising bands 10/35/70%** on his corruption (lingers → crowds → pulls off the task) | renner_depot |
| 10 | **amb_renner_anchor_ruin** | L2 ambient | random ~25%, requires_npc; tiered [group] on his corruption (the ruin showing) | the_anchor 19–23 |
| 11 | **amb_renner_cheerup** | L2 ambient | `renner_office_open` + corruption floor + low chance; scaled by spine flags (tease / blow / take it) | the_anchor 19–23 |
| 12 | **loop_renner_office_sex** | sex-loop | triggerless; poses oral→vaginal→anal (anal gated corruption ≥ anal-tier); pleasure climb; climax-elect ≥ 50 | office register |
| 13 | **loop_renner_finisher** | sex-loop | [group] by `sex_finisher_type`; inside/oral → reset + exit; **anal → control canvas** | office register |
| 14 | **renner_control_canvas** | control | the drain — payload prose (no flags; triggerless); reached from the capstone (first) + the loop (repeat) | office register |
| 15 | **cap_renner_hired** | L4 auto-fire | first depot entry + `opening_done` + guard → **SETS `renner_hired`** | renner_depot |
| 16 | **cap_renner_blowjob** | L4 capstone | office + corruption ≥ blow-tier + `renner_flirts_back` + guard → **SETS `renner_oral_once`** | office register |
| 17 | **cap_renner_anal_drain** | L4 capstone | `renner_fucked_once` + corruption ≥ anal-tier + guard → **SETS `renner_drained` + `renner_leads_extracted` + `renner_anal_once`**, routes into the control canvas | office register |
| 18 | **ma_renner_blowjob** | L4 auto-fire | next day: `renner_oral_once` + `days_since_flag ≥ 1` + guard → bumps his corruption | renner_depot/office |
| 19 | **ma_renner_anal** | L4 auto-fire | next day: `renner_anal_once` + `days_since_flag ≥ 1` + guard → bumps corruption to the ceiling band | renner_depot/office |
| F1 | **inv_facility_explore** | L3 host | ungated investigation; accrues lead evidence | facility_ruins |
| F2 | **inv_facility_match** | L4 auto-fire | entry + `renner_hired` + guard → **SETS `facility_match_seen`** (the "that's mine" seed) | facility_ruins |

**The sex loop + drain (the reusable pattern's first build).** Triggerless, node-routed from "Fuck him." State
is **numeric traits only** — `sex_stage` (0 oral / 1 vaginal / 2 anal), `loop_npc_pleasure`,
`sex_finisher_type`, `anal_active`, `sex_entry_origin` — all in `[player.core_traits]`, hidden, **reset to 0
on entry AND on every finisher exit**. Poses raise pleasure; the climax-elect (≥ 50) sets the finisher type;
the **anal elect is itself gated `anal_active` ≥ 1** (so you can't pick the ass finish from the oral pose).
Inside/oral finish → reset + exit. **Anal finish → the control canvas (the drain).** The drain's flags are set
on the **located capstone (#17)**, never on the triggerless canvas — copy this discipline to every future
target.

**Flag chain (acyclic; each flag one located setter; every condition block `version="1.0"`):** `opening_done`
→ `renner_hired` (#15) → `worked_renner_once` (#8, sole owner) → `renner_office_open` (#2) →
`renner_flirts_back` (#5) → `renner_oral_once` (#16) → `renner_fucked_once` (#7) → `renner_drained` +
`renner_leads_extracted` + `renner_anal_once` (#17). No corruption cooldown flag — the charged rungs are
throttled instead by their **cost** (15 Charge + 180 min each) against the **09:00–18:00 office window**
(~3/day), and the bar is the ×2.5 ladder (drain `corruption ≥ 50`, office `relation ≥ 21`).

**Frontier (telegraphed, deferred — never silent).** The drain sets **`renner_leads_extracted`** → opens
Bastien (`bastiens`) + Calloway (`vance_securities`); their on-ramps render greyed citing "Renner's leads"
until then. Mercer's "Report" reads `renner_drained` for his debrief. `renner_leads_extracted` is one lead
toward unlocking **the_site** (the chip). The facility match + the drain payload are Renner's "wrong-note"
toward the first crack in "evil rogue." All seeded, none built — blueprinted when their Step-4 design exists.

---

### World blueprint (Pass 3)

> Mostly consolidation — the schedules + ceilings fell out of the NPC passes; this pass places them on the map,
> settles the systems, and fixes the engine container double-print. **Map scope (LO): build the chunk's ~11
> locations; leave Mid-City + the other venues frontier** (build-order, not a cut — the city breathes more as
> Missions 2/3 land).

**The chunk's map (built):**
- **THE SPIRE** — `spire_plaza` (street hub / travel anchor) · `vance_tower` → `atrium` · `penthouse` (Mercer)
  · `wren_floor` → `wren_room` → `cradle` (her hub).
- **THE REACH** — `the_waterfront` (street hub / travel anchor) · `the_anchor` (Renner, evenings) ·
  `renner_depot` (Renner, days + the folded office register) · `facility_ruins` (investigation).

**Location tags (the dead-room gate).** The four **containers** — `loc_spire`, `vance_tower`, `wren_floor`,
`loc_reach` — are pure-nav (default_entry set, host no canvas, exempt). The **standing hubs** all earn their
click: `penthouse` (Mercer), `cradle` (her), `the_anchor` + `renner_depot` (Renner), `facility_ruins`
(investigation), and `spire_plaza` + `the_waterfront` (each hosts the travel-bridge activity). `atrium` is a
**named threshold** (the gate between the cage and the street) — a deliberate thin pass-through; its ambient
corporate life is a telegraphed frontier seed, not a silent dead room.

**Frontier (NOT built; telegraphed where it counts):**
- `the_site` — a **locked-visible nav card** in the Reach ("unlocks on enough leads" — the chip / Phase-1 end).
- `bastiens` (Mission 2) + `vance_securities` (Calloway / Mission 3) — **greyed seeds** that light when
  Renner's drain sets `renner_leads_extracted` (exact telegraph form settled at authoring).
- All of **Mid-City** (`the_strip` · `mirage` · `the_cordon` · `the_long_hour`), `the_eyrie`, `lab` (Pell),
  `units_quarters` — pure frontier (no chunk content; built with their mission/Act content, not as empty rooms).

**Schedules (5D):** Mercer `penthouse` 08:00–23:00 (offscreen overnight) · Renner `renner_depot` 09:00–18:00 +
`the_anchor` 19:00–23:00 (offscreen overnight) · player day-router at `cradle` 19:00–05:00. The nav paints each
NPC where he's scheduled.

**Ceilings (5B — author-encoded in `conditions`, no location attribute):** depot floor = **public/work only** ·
the office register = **the full ladder** · penthouse = Mercer's domain · cradle / wren_room = her space (the
invasion intrudes) · the Anchor = public (witness + cheer-up) · facility_ruins = investigation.

**Systems (5F):**
- **Phone** — Mission 1's morning briefing (the Renner tip); minimal in-chunk.
- **Money** — credits (Renner depot income, the only source); the disguise shop + Pell's upgrades are frontier
  sinks (Player blueprint).
- **HUD** — Charge + Credits only (band text per `0_systems`). **Quest card** — Mission 1: get close → drain →
  extract the leads (shows while `mission_1_active` && !`renner_drained`).
- **Clothing** — **a worn-state cover system** (added during authoring — full spec in *## The cover / disguise
  system*). The company **issues** the Mission-1 cover (no shop — the boss provides it); she equips it at the
  rack (`wren_room`) before a mission, and the Renner surfaces gate on `clothing_item … equipped`. Out of cover
  → the mark reacts wrong (no hire / suspicion). ("Commando" still lives in the flash rung's text.) Per-mission
  covers for Bastien/Calloway stay frontier (granted as their missions open, tagged by `worn_type`).
- **Customization** — none (fixed identity). **Shared-private peep/occupancy (5H)** — **none** (the invasion is
  a scripted intrusion, not a co-presence mechanic).

**Access + travel (5G):**
- **Travel-friction:** `spire_plaza` ⇄ `the_waterfront` is the one bridge — it `costs` time + a little Charge;
  fast-travel once a place is known. The cost is what makes Renner's daytime schedule bite.
- **The container double-print FIX** (the audit's engine bug — children printed twice): **drop the
  `is_container` district-wrappers entirely; build the map as NON-container standing hubs** — the shipped
  `late_shifts` pattern: two parallel top-level street-hub roots (`spire_plaza` / `the_waterfront`, no
  `entry_from`) bridged by the travel activities, venues nested via `entry_from` + `navigation_order`.
  Containers were the cause (they double-print AND swallow attached canvases); the non-container shape
  sidesteps both. **Verified clean at beat_0001** — each child renders once. (Supersedes the earlier
  `default_entry`-on-containers idea — engine-forced, see ledger turn 22.)
- **Locks as prose:** `the_site` carries `entry_conditions` + `blocked_message` (`version="1.0"` or it fails
  open); the office register's access is the `renner_office_open` gate, not a hard door (Fork A fold).

**Reachability (the triad holds):** each scheduled NPC has a presence-floor hub where he's scheduled; she
reaches the Reach via the travel bridge after the cradle day-reset; the daytime/evening windows overlap her
waking hours. ✓

---

### Wiring, opening & plan (Pass 4)

**The chunk DAG — it closes.** One spine, a few cross-reads; acyclic, every gate has a located setter, every
cross-arc reach telegraphed.
- **Spine (monotone):** `opening_done` → `renner_hired` → `worked_renner_once` → `renner_office_open` →
  `renner_flirts_back` → `renner_oral_once` → `renner_fucked_once` → `renner_drained` (+
  `renner_leads_extracted` + `renner_anal_once`). Mercer's `mercer_hub_open` (first service) runs independent
  of the spine.
- **Cross-reads (the one-world seam — all one-directional reads, D2-safe):**
  - `worked_renner_once` → player **glitch-recurrence I** (cradle) + arms Mercer's **first invasion**.
  - `renner_drained` → player **glitch-recurrence II** (cradle) + (frontier) Mercer's **debrief**.
  - `renner_leads_extracted` → (frontier) Bastien/Calloway on-ramps + the_site lead-count. The frontier reads
    render as greyed seeds (D3).
- **D1 (cold-start):** the opening runs from boot → the city opens; Renner's hire (first depot visit) +
  Mercer's hub (first penthouse visit) are the ungated on-ramps; the cradle is always reachable.
- **The core loop:** cradle reset → out (work → seduce → drain Renner) → back (serve Mercer) → cradle (the
  glitch waits) → repeat. The drain is the chunk's climax.
- **Fail-state:** none in the chunk (Charge = soft pace). **Supply→demand:** dissolved — no player-corruption
  door, so every NPC rung self-supplies via his own traits.

**The opening — its real node structure (~23 clicks, one beat per click).** Authored as **fine cascade beats**
in the three beat-canvases (one paragraph or one exchange per click, 2-sentence cap — the fix for the prior
collapse):
- **Beat 1 — the office (~12):** line-up · accusation · threat · she begs · verdict ("the Chairman's
  investment") · punishment set-up · punishment ×3 (he takes her → the act → the units blank) · gratitude ·
  reassignment (the units + her job + the mission lie) · dismissed. *Plants the freeze as the first glitch.*
- **Beat 2 — the night (~7):** walk back · the cradle · the tears · the memory fragment · the catechism · the
  power (never works on the boss) · power-down. *Plants the awakening + the boss-immunity.*
- **Beat 3 — the morning (~4):** power-up · the briefing · the tip (Renner @ the Anchor) · **out the door**
  (the hinge). *Sets `opening_done` + `mission_1_active`; the city opens; hands to Renner.*

**The build plan (seeded — Step 7 authors one beat per turn, green each time):** 14 beats —
scaffold → opening (×3) → home base (Mercer + cradle) → Renner (×6) → texture → glitches/facility → verify.
Full ordered list in `authoring_state.json` `plan`.

---

### Content register & ceilings (the authoring contract)

> The crudeness ceiling + the non-con floor, declared before authoring (`kink-ceilings.md` — a scene that
> touches an *undeclared* ceiling doesn't ship). Step 7 reads this before writing any hot beat.

**Vocabulary ceiling — per NPC, per tier (full crude EARNED at the peaks):**
- **Renner** — maximum/rough at the peaks: real anatomical words (cock, cunt, cum, ass) at the office sex, the
  loop, and the anal-drain. The soft rungs (tease / flash / the cold-boss early beats) stay **un-crude** — the
  crudeness is earned by the climb, off at the bottom.
- **Mercer** — maximum/rough at the punishment + serve-loop peaks; his register is **ownership-degradation**
  ("my investment," "asset," used like furniture), crude where he uses her, never warm.
- **The soft / non-sexual surfaces** (hubs, ambients, work, the cradle) stay flat and clean — no gratuitous
  crude on a re-readable everyday beat.

**Non-con / dubcon FLOOR (the owned-slave register).** She is **property, used at others' will** — Mercer owns
her (she cannot refuse), the targets believe they're using her. Her **body responds while her will is never
consulted** (the opening punishment is the template: "her body answering" while she's used in front of the
units). The prose may depict the ownership, the degradation, the can't-refuse — that's the floor. It stops at
**used-and-degraded, not brutalized-for-gore** (no torture/mutilation unless re-specced). The opening office
scene is the first canvas that needs this floor.

**The control-canvas (the drain) — voice carriage (Rule 4).** The extraction is **played as a Q&A exchange in
HIS own dialog** — his answers under her command, his voice breaking — **not narrated summary** ("she drains
the payload"). It's the hottest target beat; it must be spoken. The reusable pattern carries this note, so
Bastien/Calloway inherit it.

**Wren's interior (the flat surfaces).** Her in-the-moment reads (the cradle, the glitch beats) sit in a single
`thought_bubble`, flat and terse; **Tier-3 is spent ONLY on the two once-only glitch capstones** (glitch II
heavier than I). The recurring cradle-leak ambient was considered and **cut** — her thread stays lean: rarity
is the punch.

---

## The cover / disguise system (worn-state) — added during authoring

> Pulls the disguise from prose into a real **worn-state mechanic**, in Mission 1 (Renner). **LO's call: the
> cover is *issued by the company, not bought*** — she's owned; the boss provides her kit. This supersedes the
> World-blueprint §5F "clothing = narrative in the chunk" line and pulls the disguise system forward from the
> frontier. Every engine claim is code-verified (`v2.py`, cited).

**The idea (one line).** The cover is a garment she has to **put on** before a mission. In cover, the mark
treats her as the hire and the mission runs. Out of cover, she's a well-dressed stranger asking a broke man
about his business — and the world reacts wrong.

**Two states the engine gives us** (the `clothing_item` predicate, `v2.py:3587-3608`):
- **owns it** — `{ type = "clothing_item", item_id = "cover_dockhand", operator = "owned" }` (did the boss give it to her).
- **wearing it** — `{ … operator = "equipped" }` (is it on her body right now). This is the gate that matters.

**The loop (no shop — the boss provides):**
1. **Issue** — the morning briefing node hands her the cover with the dossier. Engine-native grant:
   `exit_block.config.wardrobeEffects = [ { action = "add", item_id = "cover_dockhand" } ]` (`v2.py:12503-12511`)
   — **`add`, not `equip`**, so it lands in her wardrobe **un-worn** and she must dress herself (this is what
   keeps the "not dressed" path alive — LO's locked pick).
2. **Dress** — she goes to the **rack in her room** (the wardrobe screen at `wren_room` — the "rack of faces"
   from the opening) and puts the cover on.
3. **Go** — in cover, she heads to Renner; the mission runs.

**What it gates (the mission surfaces, not every rung).** The cover is the key to the door, not the staircase
behind it: it gates the Renner **entry** (the hire + the depot/Anchor hubs); the seduction climb itself still
rides on the NPC's own **relation + corruption** as designed. Same one cover for the whole Renner mission.
- `cap_renner_hired` gains a third trigger condition: `{ type = "clothing_item", item_id = "cover_dockhand", operator = "equipped" }`.
- The depot + Anchor Renner hubs gate the same way.

**★ How it reacts when she is NOT dressed (the point of the system):**
- **Before hired, out of cover** — the hire won't fire. A clean, expensive-looking woman leaning on a
  blacklisted wreck reads as a *threat* (cop / fed / Vance). He clams up and waves her off (*"Whatever you are,
  off my stool"*). No access — the cover is exactly what makes her not worth a second look.
- **After hired, out of cover** — the work + seduction options are hidden with the reason shown (the engine
  auto-prints *"Wearing: Dock-work coveralls"* on the greyed option, `v2.py:7332`), and a short fallback beat
  fires instead: Renner squints at the nice clothes — *"The hell are you dressed like that for? …Do I know
  you?"* — the suspicion the cover exists to kill. The day stalls until she's back in cover.
- **The rule, plain:** cover on → invisible-useful, the mission runs. Cover off → the doors stay shut and
  people react to a stranger who doesn't belong. **No alarm / fail-state in Phase 1** (the leash is parked for
  Act 2) — out-of-cover is a *stall + a wrong look*, not a loss.

**Clothing equipped is sticky** (`player.equipped` persists; nothing resets it daily) — so the lesson lands
once (first outing, undressed → wrong reaction), and after she dresses she stays covered until she changes.
*(Optional future flavor, not built now: inside the Tower she's in her own/asset self for Mercer, and swaps
into the cover to go out.)*

**What it deliberately is NOT.** Not a wear-to-level grind — it's a binary identity key (in cover / not),
issued free, gating ENTRY only, never the escalation rungs (those stay on the arc spine). This keeps it on the
right side of the clothing two-part rule (`references/clothing.md` §2 — that rule forbids gating an arc on
`worn_corruption`/revealingness; gating *identity/access* on a specific issued garment is a different,
legitimate use). No "underdressed"/exhibitionism axis — the cover is about *who she's pretending to be*, not
how much skin shows.

**Build notes (Step 7):**
- **Enable clothing** in `[settings]` (the scoping trap — keys under `[settings]`, not bare):
  `clothing_enabled = true`, `wardrobe_location = "wren_room"`. **No `shop_location`** (no shopping → no shop UI
  emitted, `v2.py:1478`).
- **Full starting outfit** — every slot has an `initial = true` item (her own/asset self) so she's never
  naked/blocked and "out of cover" = "in her own clothes" (`references/clothing.md` §7).
- **The cover** — one `[[clothing]]` item, `slot = "dress"`, no price, **not** `initial` (granted at the briefing).
- **The grant** — `wardrobeEffects = [{ action = "add", item_id = "cover_dockhand" }]` on the morning briefing
  node's exit.
- **Onboarding** — the briefing tells her to wear it ("your cover's in your quarters, put it on before you go")
  so dressing is a taught step; the not-dressed beats are the backstop, never a dead screen.
- **The gate + fallbacks** — add the `equipped` condition to the hire + the two Renner hubs; author the two
  out-of-cover reaction beats above.
- Every `conditions` block carries `version = "1.0"` (or it fails open).

**Scaling (frontier).** Bastien's and Calloway's covers are granted when their missions open, tagged by
**category** (`worn_type`, e.g. `"cover_dockwork"` / `"cover_pa"`) so each mission gates on "wearing the right
*kind* of cover" — wrong cover at the wrong mark = wrong reaction. One issued garment per mission; still no
shop.

---


## Capability — Fighting & Stealth (day-depth, added during authoring)

The first piece of **day-depth**: things to *do* per day besides seducing Renner. Two **capability traits**
the player builds for herself:

- **Fighting** — win a straight fight (against guards). Always available, weak at first.
- **Stealth** — move unseen: slip past, go deeper, steal.

**How she builds them — the Training activity (`activity_train`, her room).** She drills in secret —
sharpening the body the company built, past the spec on her file; the one thing here that's only hers
(*the want:* stop being helpless / get where she can't yet). Two drills, Combat / Stealth, **+3 a session**
slowing to **+1** past 30 (drilling plateaus around 50; the top comes later from real use). Each drill
**costs 15 Charge** (it gates — she can't drill when too drained) and **120 minutes**, so training competes
with the rest of her day. The drill's prose escalates as the trait climbs (clumsy → sharp / fumbling →
ghost) so progress reads even before the bars exist.

**Now live (piece 2):** the **sidebar bars** for Fighting/Stealth and the **thing that reads them** — the
Burned Yard guards (below) — shipped together, so the bars are honest. The Stealth drill now unlocks the
first time she's caught at the yard.

---

## The Burned Yard (day-depth, piece 2 — the Trail crawl)

A new locked location off the Waterfront: **Renner's own yard**, the one **Cain torched in revenge** for
the two of Renner's people he killed (and their families). Distinct from The Facility (her origin site) —
this one is Renner's, so **his men guard the wreck** (he's salvaging gear / burying what he did). The
guards are **narrative, not characters** — the encounter is decided by *her* skills, not theirs.

**The crawl (this is where Fighting & Stealth pay off).** She sneaks in and **pushes deeper** (a hidden
depth meter, 0→3). Each push hits a guard, and she gets past one of three ways:
- **Slip past** (high enough **Stealth**) — unseen,
- **Take him down** (high enough **Fighting**) — caught, but she wins,
- **Use the arousal weapon** (once repaired) — caught, but she walks through,
- or **she can't, and runs** (flee — no progress, try again after training).

Guards get **tougher the deeper she goes** (10 / 25 / 50-ish), so she trains up to push further. It's
**doable untrained** — you just get caught and run — so it's a difficulty, not a wall. The first time
she's caught unlocks the **Stealth drill** back home.

**What's down there (one find per depth):**
- shallow — a **clue** (what the yard really was: shipments to the Facility — Renner moved more than he knew);
- mid — the **broken arousal weapon** (same tech as what's inside her), which she **repairs over a few
  sessions** at her room until it works (then it's the "walk past a guard" option above);
- deep — the **heart of it**: the two dead men + their families, erased, and the **thread to the
  underworld** (where the trail runs next — the Underworld is reachable off the Waterfront; its deep end,
  where Cain is, stays locked). Standing in it, a **memory flickers** (the awakening).

A **Trail quest card** tracks it (a parallel goal to the seduction): *get into the yard, work deeper.*

---

## The Underworld (day-depth, piece 3 — the dark city, her second life)

The hidden criminal city the whole hunt points to — where Cain is. The burned yard already names it; this
build makes it a **place she can go and live in**, with its own **money**. It's the opposite of the cradle:
up top she's owned; down here **no one knows what she is, and her coin is her own.** (The deep end — where
Cain actually is — stays locked: *The Site*, re-parented as the underworld's far end.)

**Sex register down here (declared ceiling).** The Underworld sex (brothel work, the arousal-weapon
pass-bys) is **explicit at the ceiling** (cock/cum/tits, the act on the page — no fade) but **COLD**:
transactional, detached, no performed pleasure — a body for rent, a weapon being used. This is *deliberately
the opposite* of the Renner/Mercer seduction heat (where she's working a man open); down here she's gone
behind her own eyes and the coldness is the point. (Interior-tic note: the "files it under nothing" / "the
way she does everything" reflexes are **rationed** — kept for the opening glitch escalation and the yard
awakening payoff, flattened everywhere they'd gone routine.)

**Getting in (every visit).** A gate off the Waterfront, always there. The guard wants **coin** — but she
can also **fight** him or **use the arousal weapon** (no sneaking past this one). First visits, with no coin,
she forces in; once she's earning, she just pays the toll. Clearing the guard is the *only* way to the strip.

**The coin economy (her second life).**
- **Earn — two ways, her two natures:**
  - **The House** (brothel) — a **full sex loop** (oral / vaginal / anal pose ladder → his pleasure climbs → she picks how he finishes: mouth / inside / ass), **coin paid on finish only** (no faucet). The thing she's used for, sold now on *her* account — cold and transactional (the declared ceiling). Same engine shape as the Renner/Mercer loops (triggerless canvases, numeric loop traits); reached from the House menu's "Take a client" rung.
  - **The Pit** — she fights for a purse → coin. The **payoff for training Fighting** (drill it at home, use
    it at the yard/gate, *earn* with it here). Tougher bouts pay more.
- **Spend:**
  - **The gate toll** (the clean way in),
  - **The Black Market** — coin buys **weapons** (a fighting edge) and **gear** (a stealth edge); the coin-fast
    alternative to drilling.

**The black market also sells people.** Behind the chain, the **pens** — bodies bought and sold by weight.
She can't buy here (deferred), but she *walks the line*, and among the merchandise is **one like her**, caged,
watching back wrong. A recognition she shuts off before it lands — the awakening, and a seed of what Cain
fights (the trafficking). Dark texture, not a transaction.

**Frontier.** The deep underworld — the don (a weekend back-office seed), the real services, and **where Cain
is** (The Site) — stays locked → *"you're in; the hunt runs deeper from here — more coming."*

---

## Reset & reload (cleanup + the two weapon reloads — three separate upkeep systems)

After she uses her body/powers hard, she's spent and has to reset. **Three distinct things** (kept lean so
it's rhythm, not chores):

**1. Condition (hygiene) — cleanup after sex.** A meter that **drops when she has sex** (the drain, the
brothel, the Renner loop). **Washed** at her room. Its one job: being **presentable to go out in cover** —
if she's filthy she **can't ride down to the Reach** until she washes (the cover won't hold). It does **not**
touch the seduction rungs — it's just *wash before each outing.* **Bounded 0–100** like Charge: the sex/weapon
drops floor at 0 and the Wash caps at 100 (clamped), so the Condition card never slides off a band and
vanishes.

**2. The drain weapon reloads.** Her truth-drain holds **one shot.** Fire it (the anal-finish extraction)
and it's **spent** — she can't drain again until she **recharges.** (If she takes him in the ass while
spent, the act still happens; there's just nothing to take.)

**3. The arousal weapon reloads.** The emitter holds **three shots.** Each time she zaps a guard it uses
one; at empty she **recharges.** So it's a limited tool, not an infinite skeleton key.

> **Firing it is a real beat (not a bypass).** Using the weapon plays out: she floods them with the field,
> **fucks** the one in her way, and **he passes out** (non-lethal — he wakes later, no memory, so a recurring
> guard like the gate doorman is still there next time). Because it's sex, it **drops Condition** like any
> other. So the three ways past a guard read distinctly: **Stealth** = unseen / no trace · **Fighting** = beat
> them down · **the weapon** = fuck them unconscious (the seduce-past path for when she can't fight or sneak).

**Where the weapons recharge — the cradle, split in two:**
- **Charge up** (new) — a couple hours on the feed line: tops up her Charge **and reloads both weapons.**
  No day lost.
- **Power down / sleep** — advances the day (and also reloads, as a full reset).

So her home base now has three beats: **Wash** (Condition), **Charge up** (Charge + weapon reloads), and
**Power down** (the day). The wash is also her one private, unscheduled moment — a small thread of the
awakening.

**Charge is a real throttle, bounded 0–100.** Spending it is gated, not cosmetic: the three Renner rungs
and the depot work **block when she's too drained** (greyed, "(Requires 15 …)") — she recharges at the
cradle and comes back. Two deliberate exceptions: **travel never blocks** (it only floors at 0), because the
ride back to the Spire is the *only* way to the cradle and blocking it would strand her; and the cradle
restores **cap at 100** (no overshoot). Earlier these all ran as ungated effects, so Charge could slide
below 0 (the HUD card silently vanished) or past 100 — both fixed by routing spends through `costs`/clamp.

---
