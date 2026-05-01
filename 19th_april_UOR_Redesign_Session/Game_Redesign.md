# The Long Summer — Redesign Working Document

*Living document capturing finalized decisions as we iterate through the redesign of The Long Summer. Greenfield design — this doc stands alone and does not anchor on any prior codebase or pre-existing game content. Decision record, not analysis.*

**Started:** 2026-04-19
**Current scope of this pass:** Full pre-content redesign locked through 2026-04-22 — bible items answered, world designed, three NPC arcs locked, Prologue sketched, diner mechanics tiered, systems layer specified. Content authoring (scene prose, dialog, specific canvas writes) is the next pass.

---

## Status Key

- ✅ **FINALIZED** — locked, won't revisit unless new information forces it
- 🔄 **IN DISCUSSION** — proposed or partially agreed, not yet confirmed
- ❓ **OPEN** — not yet addressed, placeholder for future decision
- 🔒 **DEFERRED** — intentionally out of scope for current pass

---

## Section 1 — Game Identity

### 1.1 Title

✅ **"The Long Summer"**

Rationale: Atmospheric + evokes stretched time + works with open-ended duration (not locked to any specific timeframe) + carries rural/transformation weight across all tonal registers (sweet → dark).

### 1.2 Genre / Core Frame

✅ **Rural coming-of-age + economic pressure hybrid**

Combines the atmospheric-transformative-summer frame with economic pressure as the motor. Distinct from the three reference games:
- Not crime sandbox (Shady Deals)
- Not pure corruption descent (NLP)
- Not social transformation in a school (ZSL)

This is its own genre position: **building a personal future from scratch in a rural place, during a specific summer window.**

### 1.3 Core Fantasy (the one-line promise)

✅ **"A young woman's transformative summer in a rural town, where she's working to build a future from scratch — and the choices she makes about how to earn, who to trust, and who to become shape everything that comes after."**

### 1.4 What this game is NOT

✅ Explicit rejections:
- Not "just family drama" — the world beyond the house matters
- Not a pure descent / one-way corruption ratchet — building rather than falling
- Not empire-building or power fantasy — Maya's goal is personal future, not dominion
- Not a VN wearing game clothes — content-rich with real game properties

### 1.5 Tonal register

✅ Adult-content genre. Multiple tonal registers supported (sweet to dark) based on player choices. Sexual content present across engaged arcs; no arc-level "no sex" path, but granular refusal within arcs (ZSL model — confirmed in separate design discussion).

### 1.6 Thesis / direction-of-travel

✅ **One-sentence thesis** — functions as player-facing welcome-page text AND designer-facing north star:

> *"Take Maya through a long summer in a rural town that doesn't live by the rules she was raised on. She arrived carrying a moral code the place doesn't enforce. As she learns what her body and her wits can earn, you decide which parts of herself she keeps — and how much she walks away with."*

Why this thesis:
- **Leads with the TOWN as a moral frame**, not as scenery. The town's permissiveness is load-bearing (see Section 2.1).
- *"moral code the place doesn't enforce"* — locks the arc as *code-editing-under-pressure*, not *corruption-from-outside*. She's not being corrupted by a darker world; she's deciding piece by piece which of her rules still apply here.
- *"what her body and her wits can earn"* — dual-driver (body = corruption axis + public-reputation risk, wits = honest hustle, both earn).
- *"which parts of herself she keeps"* — two trackable outcomes (who she ends up being + cash in pocket) without naming a specific endgame.

Lens for every later content decision: does this scene/NPC/choice press on *which rules of her old code still apply*, and does it move either *who she's becoming* or *what she's walking away with*?

Prologue note (added 2026-04-22): the thesis assumes the player has PLAYED her old moral code, not just read about it. Phase 0 (the Prologue) exists to plant it through active play. By the time Phase 1 opens, the code is the player's own memory, not backstory.

---

## Section 2 — The World

### 2.1 Setting

✅ **Southern small town — permissive moral register.** Region name + era specifics deferred (❓) but tonal character locked as of 2026-04-22.

Scale and geography:
- Population around four thousand.
- Big enough for a diner, two churches, a community college, a high school, a short downtown strip, a truck stop on the highway.
- Small enough that everyone knows whose truck is parked where.
- Economic base: slow decline. Some surviving light industry, cycling wage work, old agriculture. Town peaked thirty years ago; hasn't decided whether it's dying or just resting.
- Climate / prose palette: heat that doesn't let up, red clay or pine, afternoon storms, insects, crickets at night, screen doors, church bells on Sundays.

**Moral register — load-bearing.** This is not a town of polite restraint. People here are selfish in the sense that you do things to get things. Men flirt and grope in the open at the diner. Sex happens in public-adjacent spaces without causing scandal. Transactional sexuality is visible if unspoken. The register is *heightened* — more charged than literary realism, less lurid than pornographic bait. The point of this register is craft-functional: it lets every sexual encounter in the game be *mechanical*, not *taboo-crossing*. The dramatic weight sits on Maya's internal reaction, not on social scandal.

What the register does for the design:
- Removes the "every sexual act needs a boundary-crossing scene" authoring burden.
- Makes the diner-shift tier mechanics plausible (Section 8).
- Relocates Maya's shame from *"I broke a rule"* to *"I wanted to hurt someone, I did, and I can do it again"* — the Prologue engine (Section 4).
- Makes Diana legible as the one adult in Maya's orbit still holding the old code (Section 2.7).

### 2.1.1 What the register is NOT

- Not a utopia. People are still hurt, still jealous, still lonely.
- Not a consent-free zone. Maya can refuse. NPCs refuse. The mechanical consent system (Section 3.8) is live.
- Not a cartoon. Even in a permissive register, the town has its own rules (just not the ones Maya was raised on). Violations of those rules have consequences. The sub-reputation system enforces this (Section 2.8).

### 2.1.2 Name + region

❓ **Deferred.** Picking the specific state (Alabama / Georgia / Mississippi / rural Carolinas) can happen when we draft prose. The mechanics don't hinge on it.

### 2.2 Time frame — Phase 1

✅ **Diana lives in the house from Day 1.** Mom is not a returning character — she's the household anchor the whole time (see Section 2.7). The old "Mom's return" phase boundary is retired.

🔒 **Phase 1 closing event deferred.** Per 2026-04-22 lock: the design is being laid out first; the end is defined later once the arcs are playable. No fixed duration, no calendar deadline, no scripted external event.

Candidate closing events held for later choice:
- Summer's end / academic-year start
- A Maya-internal recognition beat she chooses to trigger
- A discovery beat where one of her secrets breaks containment inside the household
- A specific arc Keep-tier outcome (e.g., Ryan's proposal is answered, Frank's arc hits its call-out)

None of these are decided yet. Phase 1 runs as long as it runs.

### 2.3 Economy (the world has a real economy)

✅ **The world has a working economy — money is a real resource, not decoration.**

World-level facts about the economy:
- Money tracked and visible to the player
- Real expenses exist (rent, living costs, costs tied to Maya's goal)
- Multiple kinds of income exist in this world — honest work, grey-area opportunities, dark options
- The world's economy is pressured enough that Maya must engage with it to reach her goal
- Darker earning options exist in this world but carry costs beyond money

*(How individual scenes express economic + emotional weight together is a scene-design question, not a world-design question — deferred to later passes.)*

### 2.4 Phase structure

✅ **Scope-expansion phases, not bounded acts.**

- **Phase 1:** Maya's arrival through Mom's return
- **Phase 2:** Post-Mom-return — same world + Mom active + recontextualized Phase 1 arcs (possibly new NPCs/locations)
- **Phase 3+:** Widening scope to broader town, new characters, new situations — TBD

Phase transitions ADD content; earlier content doesn't disappear. Each phase has its own pressures and opportunities. Phase 1 is what we're redesigning now; Phase 2+ are placeholders.

### 2.5 Mood / atmosphere

✅ **Southern heat + permissive undercurrent + Diana's old-world discipline inside one house.** The game's prose palette is slow, sensory, hot. Crickets, fans, screen doors, cheap coffee, pine resin, red clay. Inside Frank's property: order, routine, dinner at the table. Outside the property: the town's own rhythm, which does not match what Diana enforces at home. Maya lives in both registers simultaneously.

### 2.6 NPC design principle — mechanical gates first

✅ **NPCs are designed as mechanical gates FIRST, relationship targets SECOND.**

Every NPC is a NODE connecting Maya to specific game systems (economy, world access, services, information). A relationship arc may develop as one OUTCOME of deep engagement — but it rides on top of a concrete mechanical function, not instead of it.

Every NPC in the game should answer:
- What game system do they gate?
- What resource/service do they control?
- What does Maya get from them transactionally?

This applies to both:
- **Family/household NPCs** (Frank, Ryan, Jake) — deep arcs ride on top of concrete functions (rent, labor, information gateway, etc.)
- **World/town NPCs** (diner boss, regulars, professor, shopkeepers, etc.) — pure function, minimal or no relationship

Relationships layer ON TOP of function. Never the primary design frame.

### 2.7 Diana — household anchor

✅ **Diana is present from Day 1 of Phase 1. She does not leave.** She is not an arc NPC, not a dependency, not an obstacle. She is a *structural force* that makes the house a family.

**Who she is (locked 2026-04-22):**
- Widow. Her first husband — Maya's biological father — died some years back. She rebuilt her life and remarried Frank.
- Good relationship with Maya. Warm, present, not distant. Maya trusts her.
- Strict in a *father-shaped* way: rules, routines, schedules. Dinner at 6:30 because she holds it at 6:30. Chores have owners because she assigned them. The house is a family because she maintains it as one.
- Not a moralist, not a hypocrite. She isn't judging the town. She's holding her own line — and Maya's — because that's what she learned to do after the first husband died.

**Mechanical function:**
- Makes recurring group scenes exist (family dinner as a real daily scene, Sunday mornings as a real weekly scene).
- Provides the household's schedule anchor (the other NPCs' routines revolve around hers).
- Is the quiet witness in the house — not yet an active threat to Maya's secrets, but a *presence* Maya is aware of every time she makes a choice that violates Diana's trust.

**Why she's not an arc yet:**
Her dramatic weight is structural and silent. She isn't designed to discover-and-confront; she isn't positioned as an antagonist; she isn't positioned as a confidante. Whatever she knows, she says nothing about — not because she's hypocritical, but because she trusts Maya to find her own way until she doesn't. That trust is the thing Maya is violating. It's the heaviest kind of pressure in the game because it doesn't shout. Diana's possible arc (her eventually noticing, or a past Maya learns about, or her marriage to Frank fracturing) is reserved for Phase 2+.

**Voice / body deferred** to Section 10 in a later pass. Working placeholder: she uses Maya's name directly and often; she doesn't ask questions she doesn't want answered; she cooks with her hands, not recipes; she's on the porch alone most Sunday afternoons with a book or the newspaper.

### 2.8 Social structure — sub-reputation tracks

✅ **Three sub-reputations, one catch-all.** Each tracks independently. They don't have to agree.

- **Church crowd** (`rep_church`). Older, conservative, socially dominant on Sundays and at community events. Diana's crowd. To this crowd, Maya is *Diana's girl*, and what this crowd thinks of Maya reflects on Diana first. The fastest way to hurt Diana is to become visible to this crowd doing something they disapprove of. Rises slowly (they don't see Maya at work), falls fast (a single visible act can cost it).
- **Road crowd** (`rep_road`). Truckers, mechanics, farm hands, Ryan's business customers, regulars at the truck stop bar. Working class. Less performatively moral, more transactional. To this crowd, Maya is a face at the diner worth remembering. This crowd keeps its own counsel and doesn't feed back into the church crowd's channels. Rises fast (she's in front of them every shift), falls slowly.
- **College crowd** (`rep_college`). Younger, transient, some local, some from neighboring counties. Come and go by semester. Drift through the diner late. Not fully local — their opinions don't enter the town's permanent record. Rises irregularly. Mostly a Phase 2+ surface.
- **Ambient town** (not a tracked stat, just atmosphere). The clerk at the general store, the postmaster, the sheriff, the high school crowd on Friday nights. Register things without choosing a side. Background noise that makes the three named crowds legible *as* crowds.

**Mechanical use:** each of the three tracked reputations gates different NPC dialog lines, different customer types at the diner, different scene availability. Hints in the Guide Page reflect which direction Maya's reputations are drifting.

**Craft note:** because Maya works the 5–10pm shift (road + late college), her road reputation builds fastest. Church reputation is mostly mediated through Diana and through Sunday Main-Street visibility. The asymmetry is deliberate — different crowds offer different risks, and she can't cultivate them all at once.

### 2.9 Shadow layer — atmosphere only

🔒 **Deferred.** Per 2026-04-22 decision, no active shadow thread (drug underground, scandal history, etc.) for Phase 1. The town's permissive register carries its own ambient tension; no secondary dark plot is seeded yet. Reserved as a Future Consideration if later pacing needs it.

### 2.10 The calendar — Phase 1 minimum

✅ **One recurring event locked for Phase 1: Sunday.**

- **Sunday** — diner closed. Church service happens. Diana attends. Maya can go or not. The ambient weight of Sunday morning is Phase 1's only structural recurring beat.

🔒 **Deferred:** Friday football night, Saturday farmer's market, First-Saturday flea market, seasonal county fair. All held for Phase 2+ expansion. Adding them in Phase 1 would widen scope beyond the ability-to-ship target.

### 2.11 Phase 1 physical map — scope lock

✅ **Active in Phase 1:**
- **Frank's property** — house (hallway, kitchen, living room, bathroom, Maya's bedroom, Frank's office, Ryan's room, Jake's room), front porch, back porch, yard, creek, trail head, driveway.
- **Ryan's shop** — on the property edge (converted outbuilding or back-of-barn). Used-equipment flip operation. Customers visit here; they don't come inside the house. Distinct scene location from the house (matters for Frank's catch-trigger dynamics later).
- **The diner** — Main Street. 6am–10pm, six days, closed Sundays. Maya's primary workplace; Marge's authority.
- **Main Street** — general store, post office, gas station. Public errands.
- **Community college admin office** — single visit early (brochure, application), then gated until Maya has saved the admission money.

🔒 **Gated until Phase 2+:**
- The truck stop bar on the highway (named in ambient references but not visitable)
- The fairground
- The high school stadium
- The church interior (Diana attends; Maya is ambient-visit only)
- Full community college campus (classes, library, quad — tuition-gated)

Five active hubs. Manageable Phase 1 authoring surface.

### 2.12 Ryan's business — structure lock

✅ **Used-equipment flip.** Ryan buys broken or surplus machinery (farm equipment, small engines, trucks, lawn gear) at auction or from locals. He fixes what he can. He resells for margin. The business lives at his shop on the property edge.

- **Small tickets.** Ryan handles. Regular customers, phone or in-person, values under some threshold (TBD specific number — roughly below a few hundred dollars). Routine commerce.
- **Big tickets.** Maya closes. Values above the threshold, in-person, buyer needs to be worked. Maya's charm + eye contact + willingness-to-lean-in move the numbers. Corruption trait tiers gate which big-ticket buyers surface.
- **Crack-tier deal.** A specific buyer whose close requires more than flirt. Designed later; mechanically the trigger for Ryan's Crack tier (Section 7.4).

The business narrates the game's thesis (what her body and her wits can earn) as a literal P&L line.

---

## Section 3 — Maya (Player Character)

### 3.1 Who Maya is

✅ **Character profile:**
- **18 years old**, just out of high school
- Artist-inclined — draws/sketches as her primary self-expression and private sincerity
- Emotionally recovering from a recent breakup + friend-group collapse
- **Hardened** from that combination, NOT soft or naive — she learned *"don't give your heart, use your head"*
- Quiet in groups, sharper alone; uses drawing to process; observant and guarded
- Art is the one place she's sincere — even when she's being calculating outside, her art remains hers

### 3.2 Why Maya is here

✅ **Life fell apart + free housing option.** After the breakup + friend-group collapse, Maya's old environment became unworkable. Mom's (Diana's) extended absence made Frank's rural house the affordable path forward. Not sent against her will; not a deliberate spiritual retreat either. Circumstances drove her here.

Open specifics (deferred to Frank section / family setup pass):
- 🔒 Exact family history — how long Frank has been with Diana; closeness of prior relationship; Maya's relationship to Ryan/Jake before arrival
- ❓ Where Diana is specifically and why she's away
- ❓ Maya's living situation immediately before this summer

### 3.3 What Maya wants

✅ **Primary goal: save enough to move out and establish financial independence.** Maya is not chasing a degree or a specific program — she wants RESOURCES to leave and be her own person. Art is HER private thing, not her career plan (at least not in Phase 1).

✅ **Emotional goal:** rebuild a sense of self after the breakup + friend-group collapse. Figure out who she is when she's not defining herself through other people. The summer is her chance.

❓ Exact savings target number — TBD when economic system is scoped
❓ Terminal state for Phase 1 — what "success" looks like at Mom's return. Possibilities (all valid):
- Hit goal cleanly — ready to move out, intact
- Hit goal through darker routes — has the money but has become someone different
- Missed goal — facing Phase 2 without the financial escape she planned
- Chose to stay for her own reasons — rejected the plan

### 3.4 What's at stake for Maya

✅ **Real stakes, not just relationship meters:**
- **Economic:** hitting or missing the savings target
- **Personal:** who she becomes over the summer — she doesn't arrive as the woman she'll be at Mom's return
- **Temporal:** the summer is finite and un-replayable in-game (even without fixed duration, it ends when Mom returns)
- **Relational:** the house's dynamics shift based on her choices — some permanently

### 3.5 Maya's voice (narrative POV)

✅ **Third-person close through Maya.** The narrator sits inside her perception — the reader sees only what she notices, colored by how she's feeling. No omniscient asides, no cuts away to other characters' POVs.

✅ **Voice evolves across the summer:**
- **Early game:** cautious, wounded, observational. She watches, doesn't test. Sentences hold back.
- **Mid game:** a calculating streak surfaces. She notices her own effect on others and starts running small experiments. Voice gets sharper, more strategic.
- **Late game:** deliberately strategic where needed, but her private sincerity remains intact in her art and in moments alone. She's not a cynic — she's a young woman who learned how to use what she has.

❓ Specific verbal tics / internal sentence rhythm — reserved for Character Craft pass (after this doc's scope)

### 3.6 Maya's independent tracks

✅ **Maya has concrete life-tracks that are NOT about the men.** Each has its own content / activities / progression:
- **Art:** sketching, potentially selling work (her private sincerity + possible income stream)
- **Work:** diner job, side hustles, odd jobs (main legit income)
- **Money:** saving toward her goal — tracked visibly
- **Self:** processing past, ambient self-discovery, physical reawakening, the summer as rite of passage

Each track has its own hints on the Guide Page, separate from NPC-specific hints.

❓ Education / college track — TBD whether Maya is enrolled in anything during the summer, or whether college is just part of the setting backdrop

### 3.7 Maya's character arc — the corruption system

✅ **Maya starts unaware of her power and gets corrupted over the summer — systemically, not via a specific catalyst character or scripted awakening scene.**

She arrives wounded/guarded/closed-off. She leaves different. The summer is the transformation.

#### How change happens (drivers)

✅ Shady Deals-style hybrid — roughly:

- **~60% player-driven** — active choices at activities (flirt with a customer, reach past Frank at the stove, wear the revealing thing, take the darker job) accumulate corruption
- **~30% passive** — ambient exposure ticks stats slowly: diner shifts accumulate "being seen," walks through town hit passive gazes, time in the house of men adds charge
- **~10% soft-forced** — 2-3 scripted moments tied to economic state (rent shortfall → scene fires; she chooses HOW to handle, not whether it happens)

Maya CAN stay closer to pure if the player plays her that way — but economic pressure + ambient exposure tilt her unless actively resisted. She is not a passive victim of the world; she has agency.

#### How change is expressed to the player

✅ **No awakening scene.** Transformation is emergent from stats. No scripted "she realizes she's changed" moment. Player watches her evolve through:

- **Menu growth** — new options appear at activities as stats cross thresholds
- **Prose shifts** — same scene reads different at different corruption tiers (hesitant early → deliberate late)
- **Soft meters in the sidebar** — described in words, not numbers. *"You catch men watching you more often now"* rather than *"Corruption: 24"*
- **Guide Page voice shifts** — early hints read cautious; later hints read knowing
- **NPC reactions shift** — Frank, Ryan, Jake all notice her differently as stats accumulate; townspeople start recognizing her

✅ **Corruption stat is NOT shown as a visible number.** Player infers state from soft-meter descriptive text + menu availability + prose tone.

#### Stats tracked

Revised 2026-04-22 — see Section 3.8 for the full stat table.

- **Corruption** (primary — bundled axis; does the work of the previously-split awareness/confidence/exhibitionism/promiscuity stats)
- **Fitness** (slow-rising physical capability — new)
- **Beauty** (slow-rising physical appeal; supersedes the older "allure" proposal — new)
- **Calculation** (narrator voice axis + Prologue-inherited)
- **Money / Savings** (visible, weekly)
- **Energy / Hygiene** (maintenance; daily capacity / daily decay)
- **Sub-reputations** — `rep_church`, `rep_road`, `rep_college` (per Section 2.8)
- **Per-NPC stats** — handled in their respective arc sections

#### Starting state vs. late-state

**Day 1 Maya:** low corruption, moderate beauty, baseline fitness, calculation-tier carried from the Prologue, ~$400 cash. Closed off, wounded, observant but not yet testing.

**Late-phase Maya:** state depends on playthrough. High-engagement path = knowing, strategic, using her effect deliberately, near or at savings goal. Low-engagement path = more closed, may have missed goal, Phase 2 opens with a different baseline.

#### Forced events (the ~10%)

Only 2-3 scripted moments fire regardless of player choice, ALL tied to economic state:
- **First serious rent shortfall** — Frank's office scene fires. Maya chooses HOW (beg / charm / confess), not whether it happens.
- **Mid-summer economic reality check** — a moment where the savings math becomes undeniable.
- **(Possibly one more, TBD)**

These are not "punishment events." They're moments the WORLD creates that the player has to navigate.

### 3.8 Systems — the mechanical layer under the arc

✅ **Added 2026-04-22.** Multi-axis systems replacing the single "corruption meter." The research doc was explicit on this: corruption is a *shape*, not a magnitude. Multiple parallel axes let Maya's transformation have a *profile* rather than a score.

**Maya's core stats (player-owned):**

Revised 2026-04-22 — consolidated to a single `corruption` axis with supporting traits. The previous split (awareness / confidence / exhibitionism / promiscuity as separate axes) collapsed into one `corruption` meter with tiered bands. Fitness and beauty added as new long-term capability stats.

| Stat | What it tracks | How it moves | Surfaces as |
|---|---|---|---|
| **energy** | Daily capacity for activity | Decays per activity via canvas costs; restored by sleep | Hard gate on activities; low-energy scenes read different in prose |
| **hygiene** | Cleanliness, polish | Decays daily via `player.trait_decay` (F3); restored by shower | NPC dialog at low hygiene; tip ceiling at diner |
| **fitness** | Physical capability — stamina, strength | Rises slowly from solo exercise (jogging, creek swims) + physical side-work at Ryan's shop | Gates physical activities; walking to town without extra energy cost; Ryan's yard-work progression |
| **beauty** | Physical appeal | Rises slowly from maintenance (hygiene high, fitness rising) + clothing quality + specific self-care activities | Gates Jake's "Noticed" tier; tip ceiling at diner; NPC attention thresholds |
| **corruption** | **Bundled moral + social-willingness axis.** Does the work previously split across awareness, confidence, exhibitionism, and promiscuity: whether she registers lewd events as lewd, her readiness to use her body, her willingness to be seen, her willingness to be touched. Rises from transgressive acts she chose + ambient exposure. Never falls. | Rises from player choices at activities + ambient exposure + ~10% soft-forced events (per Section 3.7 drivers) | Tiered (low / mid / high / saturated). Gates Keep-tier branches per NPC, diner tier unlocks, Frank's catch-trigger, Ryan's big-deal, Jake's tease tier. Bands surface as Maya-voice sidebar text via the F1 `trait_words` widget. |
| **calculation** | Strategic thinking + narrator voice axis | Prologue-inherited baseline (high if she planned revenge, low if impulsive); rises from specific deliberate choices in Phase 1 | Shifts narrator prose register (early observes → late operates); gates a small set of strategic dialog options |
| **money** | Economic resource | Choice effects: tips, pay, expenses, rent | Visible stat; gates college admission target + rent eviction |
| **rep_church**, **rep_road**, **rep_college** | Three sub-reputation tracks per Section 2.8 | Rise and fall from visible public acts per their respective crowds' values | Gates NPC dialog, available customers at diner, gossip texture |

**Why the consolidation:** a single corruption axis keeps player state legible, reduces per-scene authoring burden (one tier check per scene instead of multi-axis), and fits the "words not numbers" surface cleanly (one `trait_words` bar with 4–5 bands carries the whole arc). The trade-off — losing the DoL-style distinction between "Maya's willingness to be seen" vs "Maya's willingness to be touched" — is accepted: corruption-tier gating plus NPC-specific trigger conditions (e.g., Frank's catch is gated on corruption tier + "in the living room") recovers most of the narrative distinction.

**Tier bands for corruption** (working draft; tune in content pass):
- **0–24 — Closed.** Pre-Prologue Maya. Private. Reactive. Registers lewd events as accidents. No tier-2 diner access, no arc escalations.
- **25–49 — Opening.** Post-Prologue arrival baseline if she committed the revenge. Notices being looked at. Chooses small public acts. Tier-1 diner fluent, Tier-2 accessible.
- **50–74 — Operating.** Mid-Phase-1 Maya. Uses her effect deliberately. Picks her targets. Tier-2 fluent, Tier-3 accessible with specific customer gates. Frank's catch-trigger fires in this band.
- **75–100 — Saturated.** Late Phase 1. She knows what she is. Tier-3 fluent, arc Crack beats gate here. Jake's tease and Ryan's big-deal corruption gates sit in this band.

All per-band descriptive strings (the `trait_words` text per band) are written in the content pass.

**Per-NPC stats (NPC-owned):**

| Stat | What it tracks | How it moves | Used for |
|---|---|---|---|
| **Arousal** | How primed this NPC is right now | Rises from Maya's behavior toward them; *decays per hours-not-days* | Gates which NPC responses surface in the short term |
| **Corruption** | NPC's own drift across the arc | Rises slowly from shared experiences; plateaus | Gates NPC-arc tier transitions |
| **Trust/Love** | Relationship stat per NPC | Rises from arc-appropriate choices; slow decay if ignored | Gates major arc beats |

**Arousal — hour-scale behavior via `modifier_effects`:** per-NPC arousal is implemented as a base trait (default `0`) plus temporary `modifier_effects` offsets that expire after configured hours. Maya's teasing choices apply offsets with `duration_hours` set to the desired decay window; the engine automatically clears expired offsets, and conditions that gate on arousal read the effective value (base + active offsets). This is natively supported — see `modifier_effects` in the TOML schema (`template_import.py:322-327`, runtime via `$game_state.active_modifiers`).

**The "words not numbers" rule:**
Per Section 3.7 locked principle — stats are NOT shown numerically to the player. They surface as:
- Sidebar soft-meter text (*"You catch men watching you more often now"*)
- Descriptive prose shifts in recurring scenes
- NPC dialog lines that change as stats cross thresholds
- Guide Page hints in Maya's voice

Dynamic sidebar-text gating on stat bands is now natively supported via the `trait_words` sidebar type (Engine PRD F1). Configure `[[sidebar_items]]` with `type = "trait_words"`, a target trait, and an ordered `bands` array of `{min, max, text}` entries — the widget reads the current trait value and renders the matching band's text. No `emotion_mappings` fallback needed.

**Economic system (reserved for content pass):**
- Maya's money (visible)
- Weekly rent to Frank (amount TBD)
- Food contribution (TBD)
- Bus cost or equivalent (TBD)
- College admission-money target (gates Section 2.11's college unlock)

Values TBD in the content pass. Structure locked here.

---

## Section 4 — Prologue / Phase 0

✅ **Revised 2026-04-23 as a single-canvas linear novel-prose prologue.** Supersedes the earlier 4-act / ~20-scene branching design. The Prologue is one canvas, nine sequential nodes, ~8,200 words of adult-novel-register prose with media at three structural beats. Source of truth for content lives in the canvas `prologue_morning_with_daniel` inside `games/the_long_summer/toml_phases/2_story_canvases.toml` (which concatenates into `6_final_game.toml`); this section specifies the design anchors.

**Second revision, 2026-04-23**: cast corrected (Sarah, not Emma, is Daniel's secret partner; Emma cut entirely); discovery changed from phone-text to visual (Maya walks in on Daniel + Sarah in an empty college classroom); added N2 morning sex scene between Maya and Daniel before they get out of bed; old N4 Sarah-couch scene cut; N9 final choice restructured to *voicemail to Sarah* vs *don't call.*

### 4.1 Why the Prologue exists

The game's thesis (Section 1.6) requires that Maya arrives in Phase 1 carrying a moral code the town doesn't enforce. If the player has only *read* that backstory, it's inert. If the player has *played* the moments that formed the code — including the revenge act that burned it — the code is a memory in their own head, not an author's claim. Every Phase-1 choice will be measured against what the player already did.

### 4.2 Dramatic question

*What's the line Maya won't cross?* — and the brutal answer the Prologue delivers is: *she already crossed it, deliberately, and she'll do it again if someone makes her angry enough.*

### 4.3 Form

✅ **One canvas. Nine sequential nodes. Linear with two player-choice nodes (N5, N9). ~8,000 words total.**

Prior approach (4 acts / 20+ scenes / multiple branching choices) was over-architected for what the Prologue actually needs to do. The Prologue's job is not to branch — the player's real branching begins in Phase 1. The Prologue's job is to give the player an *experience* they carry forward: a voice (Maya's), a shame (specific and felt), and a small set of flags that shape the opening of Phase 1.

Register: literary-transgressive adult fiction (Gaitskill / Moore / Reisz / Simone), not commercial erotica and not VN exposition.

### 4.4 Cast — Prologue only

- **Daniel.** Maya's boyfriend of ~2 years. The cheater.
- **Sarah.** Maya's best friend of three years. Daniel's secret partner. The symmetrical betrayal: the two people Maya trusted most were each other's secret. No confidante remains for Maya by the time she discovers.
- **Kevin.** Sarah's boyfriend of three years. Maya's revenge target. Quiet, decent. Humanized in N6 via a sincere question about Maya's art that Maya lies in response to. The lie is the beat the shame attaches to. Unlike in the prior design, Kevin is himself a victim of Sarah's cheating — when Maya tells him upstairs, he is learning about his own girlfriend in the same breath.
- **Diana.** Maya's mother. First appearance in N9 on the phone. Warm, tired, holds her own line without moralizing. Carries forward to Phase 1.

Daniel / Sarah / Kevin do not appear in Phase 1. (Emma does not exist in this design.)

### 4.5 Locked decisions

| # | Decision | Value |
|---|---|---|
| 1 | POV | Third-person close (Maya) |
| 2 | Tense | Past |
| 3 | Specific shame flavor | *"She felt competent, and that's the part she can't unfeel."* The shame is the recognition of her own agency in the act. |
| 4 | N1 register | Pure loving normalcy — Maya wakes up next to Daniel, same bed, no red flags. The unease beats (phone on balcony, unknown perfume) from the earlier draft are dropped. |
| 5 | N2 new — morning sex | Maya + Daniel, in bed as they wake up. Sleepy, familiar. Media clip. Establishes the normalcy Maya loses. Retrospectively becomes the scene she cannot unfeel once N3 lands. |
| 6 | N3 new — discovery | Wednesday afternoon, empty college classroom. Maya is looking for a quiet space to sketch, tries the third door on the Humanities third floor. Sees Daniel and Sarah. Closes the door quietly, walks out, sits on a bench outside the library for fifteen minutes. Media clip. |
| 7 | Kevin's humanity hook | N6: Kevin asks Maya a sincere question about a specific detail in her mural (the bird that's looking the wrong way). Maya lies in answer. Kevin believes her. The lie is what haunts. |
| 8 | N7 reveal line | *"Daniel is cheating on me."* (pause) *"With Sarah."* Kevin processes. The second half of the reveal tells Kevin his own girlfriend is cheating on him. Mutual wound. |
| 9 | Backed-out branch | **Dropped.** Maya commits. A single-canvas linear form cannot honestly support bail-out. |
| 10 | Diana's phone-call voice | N9. Warm, tired, holds her own line. Doesn't pry. Offers the house as a fact, not a rescue. ("It's a place to be, Maya. That's all I'm saying. It's a place to be.") |
| 11 | N9 final choice | Options: *"Leave Sarah a voicemail. One sentence. 'I saw you.'"* vs *"Don't call. Just drive in."* Sets `left_sarah_voicemail`. Replaces earlier "Call Sarah / don't call" pair — Sarah is not a confidante, she is the betrayer. |
| 12 | Media sourcing | File-based placeholders under `prologue/` in the media folder (`n2_morning_sex.webm`, `n3_classroom.webm`, `n7_reframing.webm`, plus images). Actual media sourcing is a separate pass. |

### 4.6 Canvas shape

Nine nodes, ~8,200 words. Only N5 and N9 take player input.

| Node | Beat | Words | Media |
|---|---|---|---|
| wake (N1) | Sunday morning. Maya wakes next to Daniel, same bed, pure loving intimacy. "Nothing was wrong. The morning was just the morning." | ~570 | — |
| bed (N2) | Morning sex. Sleepy, familiar, tender. *"He came saying her name. She said I love you back. She meant it."* The scene she will later be unable to unfeel. | ~770 | 1 video clip (morning sex) |
| classroom (N3) | Wednesday afternoon. Maya opens the third door of the Humanities third floor expecting silence. Sees Daniel + Sarah in the empty classroom. Closes the door quietly. Sits on a bench for fifteen minutes. | ~795 | 1 video clip (what Maya sees) |
| home (N4) | Her apartment, alone. Item four appears. Kevin selected — he is Sarah's boyfriend, the symmetrical target. | ~775 | — |
| prep (N5) | Preparation. **Player choice** — sets calculation tier (rehearsed / drink first / don't think) + `calc_tier_*` flag + `revenge_planned`. | ~610 | 1 image (getting ready) |
| party (N6) | The back porch. Kevin alone. The mural-bird question. Maya lies. Kevin believes her. | ~965 | 1 image (Kevin) |
| upstairs (N7) | The act. Reveal line: *"Daniel is cheating on me."* (pause) *"With Sarah."* Kevin processes his own loss. Full camera. Memory intrusions are the classroom (Sarah's mouth, olive backpack, fluorescent flicker). Reframing video mid-scene. Shame plants: *she is good at this.* | ~1,885 | 1 video clip (reframing beat) |
| after (N8) | Bathroom tile, the pink makeup bag with the cartoon strawberry. Kevin absent in this node. | ~745 | 1 image (mirror) |
| diana (N9) | Mon–Thu compressed. Kevin breaks up with Sarah Monday. Daniel's voicemail Tuesday. Sarah's careful paragraphs Wednesday. Diana's call Thursday. Drive. Frank's driveway. **Player choice** — *voicemail to Sarah* vs *don't call.* Sets `left_sarah_voicemail` on the voicemail branch. | ~1,100 | 1 image (driveway) |

### 4.7 Craft anchors (binding on the prose)

1. **Deep POV, free indirect discourse.** No "she thought." Maya's diction bleeds into narration.
2. **Voice before plot.** First ~300 words are atmosphere + voice. Nothing happens.
3. **Specificity of noun.** Every noun named. Not "coffee" — "yesterday's coffee, the one she hadn't dumped."
4. **Smell every ~500 words.** Scent is the missed sense.
5. **Camera consistency.** If betrayal is rendered in full, so is retaliation. No fade-outs at the physical act.
6. **No epiphany.** Prologue ends with Maya continuing, numbed, not understanding herself better. Gaitskill rule.
7. **Banned phrases:** "heart pounding," "drunk on," "electric," "every fiber of her being," "the world fell away," and their kin — the commercial-erotica tells that betray the register.
8. **Kevin is a person, not a mechanism.** N6 gives him one specific humanity beat. He remains unresolved on page; no redemption, no punishment.

### 4.8 Flags that carry into Phase 1

- `revenge_committed` — always set true on either N9 exit (bail-out branch dropped).
- `left_sarah_voicemail` — set by the N9 player choice (voicemail / don't call). Replaces the old `told_sarah`.
- `saw_daniel_and_sarah` — always set true on either N9 exit. Replaces the old `saw_the_thread` + `confirmed_visual` pair. Marker that Maya carries the classroom image.
- `calculation_tier` (+ `calc_tier_deliberate` / `calc_tier_moderate` / `calc_tier_impulsive`) — set by the N5 player choice plus calculation-trait adjustments (+5 / +3 / +1). Shapes Phase 1 narration voice and gates downstream activities.
- `prologue_complete` — always set true on either N9 exit.
- Legacy chain flags still set at N9 exit for Phase 1 compatibility: `met_daniel`, `prologue_cast_met`, `kevin_approach_branch`, `party_scheduled`, `prologue_morning_after_done`, `prologue_daniel_breakup_done`, `accepted_diana_offer`.

**Deleted during 2026-04-23 revision** (Emma and phone-discovery flags, no longer semantically valid): `emma_read`, `saw_emma_text`, `prologue_emma_done`, `sarah_suspicion_surfaced`, `sarah_knows_something`, `confirmed_visual`, `second_flag_landed`, `decided_to_look`. Player flag_keys went from 117 → 109.

The bundled `corruption` axis (Section 3) is not mutated during the Prologue; Phase 1 inherits corruption at baseline and the Prologue's outputs shape the prose register at arrival.

### 4.9 Phase 1 opening inherits

The Prologue is not optional backstory. A `calc_tier_deliberate` Maya lands at Frank's driveway reading as colder and more deliberate than a `calc_tier_impulsive` Maya; `left_sarah_voicemail` shapes whether Maya has closure-by-refusal or open-wound-kept-quiet as she arrives. That continuity is what makes the Prologue a phase, not a cutscene.

Specific Phase 1 arrival prose lives in the Phase 1 content pass (separate plan). This section's job is to lock the handoff shape.

### 4.10 What the Prologue TOML does NOT yet include

- Real media assets — all 5 images + 3 video clips are placeholder paths under `prologue/` (`n2_morning_sex.webm`, `n3_classroom.webm`, `n7_reframing.webm`). Media sourcing is a separate pass.
- Any stat configuration beyond what's needed to carry the flags forward.
- Phase 1 destination expansion — the prologue exits to `loc_front_porch`, which exists in the Phase 1 location graph.

---

## Section 5 — Chapter 1 (shape only — no beat list)

🔄 **Dramatic question locked 2026-04-22. Beat list deferred to content pass.**

### Dramatic question

*Can she be the girl she told herself she'd be when she got here?*

She arrived with a version of herself in mind — capable, hardened after what happened in the Prologue, not a victim, self-sufficient. Chapter 1 presses that self-image: she's broke, her plan requires help from men, the work is harder than expected, Diana is warmer than Maya braced for, and Maya's *body* is already doing things her *mind* hasn't admitted it's doing. The question isn't resolved in Chapter 1 — it's established. Her mind thinks it's running her; her body is already deciding.

### What remains locked

- **Chapter 1 = establishment chapter.** Maya's opening stretch in the house and the town.
- **Close event:** `first_rent_paid` flag. Chapter closes when the flag flips, not on a specific in-game day.
- **Design principle — establish, don't escalate.** No NPC-arc Touch/Crack/Keep beats. No Frank sexual-phase trigger. No explicit Jake or Ryan escalations. The chapter's job is to set the world, the rhythm, and the goals — and to let the player live in the tonal shock of arriving in this town carrying her Prologue moral code.
- **Boundary markers — NOT in Chapter 1:** no first flirt / tease / kiss / extra-tier with any NPC; no Frank's catch-trigger fires here; no Jake peek-beat; no Ryan big-ticket-deal; no college enrollment (brochure only); no truck stop bar; no deep Frank/Ryan/Jake scenes beyond polite household and Ryan's shop intro.

### What's deferred to content pass

- Beat list / scene list — to be designed as storylets against current state, not as a day-by-day schedule.
- Named NPC introductions (Marge, Cookie, Ryan-shop customers, trucker) — ordering emerges from the player's first visits, not from an authored calendar.
- Exact economic numbers (rent amount, tuition target, weekly costs).
- The specific Prologue → Phase 1 opening handoff scene.

---

## Section 6 — Chapter 2 (shape only — no beat list)

🔄 **Dramatic question + first-ambient-tilt moment locked 2026-04-22. Beat list deferred to content pass.**

### Dramatic question

*What does she already know how to do that she hasn't admitted yet?*

Chapter 2 is accumulation. The world has started responding to her in specific small ways. The pressured question is: she's doing things — holding eye contact a beat too long, letting a thumb brush hers without pulling away, keeping a sketch she should have torn up — that aren't accidents. She *knows how* to do them. The chapter leans into: when is she going to admit she's choosing?

### First ambient tilt — the chapter-closing beat

✅ **Marge hands her the key to close Thursdays alone.** *"You're steady. Thursdays are slow. Key's under the till."* That's the line. No drama, no fanfare. Maya walks the hour home with the key in her pocket, knowing three things:
- Marge trusts her.
- Marge has watched her enough to know who's in the diner after 9pm on a Thursday.
- Maya is now the kind of girl who closes a diner alone in a small town at night.

She doesn't know yet whether that's a gift or a setup. **Chapter 2 closes on her walking home with the key.**

### What remains locked

- **Chapter 2 = accumulation chapter.** The rhythm holds; the world starts having texture; the first ambient tilt lands as a seed the protagonist doesn't act on.
- **Close event:** `first_ambient_tilt` flag — set when Marge hands Maya the key.
- **Design principle — accumulate, don't escalate.** No deliberate corruption-tier-up choices. No NPC-arc Touch/Crack beats. Routine feels real because the ambient prose has started shifting (the accumulation toolkit — Chekhov detail-inventory shift, per the craft research).
- **Boundary markers — NOT in Chapter 2:** no NPC-arc Touch/Crack beats; no Frank catch-trigger; no Jake peek; no Ryan big-ticket deal; no explicit extras-tier at the diner; no threat or contrast NPCs.

### What's deferred to content pass

- Specific accumulation content that rewrites Chapter 1's recurring scenes (same diner shift, different inventory of details the narrator notices).
- The beat structure around the Marge-key moment (setup, execution, the walk home).
- Which Thursday regulars are worth naming by Chapter 2's close (Marge knows who's there — the player should start to as well).

---

## Section 7 — Story Arcs (rough sketch)

🔄 **Rough sketch.** Arc shapes, dramatic questions, tier structure, and gate hierarchy locked here. Node content, journal entries, linked canvases, and dialog beats deferred until bible + content pass.

This section sets the **shape** of what the `story_arc` will track. It does not pre-write every beat. The structure is one protagonist-backbone arc plus N parallel NPC arcs — a shape chosen because it lets Maya's external pressure (rent, town, mom) and her relational arcs (Frank, Ryan, Jake) progress on independent clocks while sharing gate flags at the critical crossings.

### 7.1 How arcs are structured in this engine

Two layers run in parallel:

**Backbone arc (Maya).** Thin but essential — 6–8 `story_arc` nodes across Chapters 1–2 with light touches in later chapters. Tracks Maya's external situation: arrival, the financial frame, the rent cycle, the town, Mom. Justifies why she stays and why the pressure matters.

**Per-NPC arcs (Frank, Ryan, Jake).** Dense but independent — each ~10–18 `story_arc` nodes across Chapters 3–6, with its own escalation tiers. Gates on backbone progression via `requires_group`, so the player must have lived a week in the house before any NPC arc opens.

Engine-level conventions that constrain these sketches:

- `story_arc.nodes[].linked_canvas` must point to a **non-repeatable** canvas (enforced at validation). Repeatable activity canvases carry *texture*, not *beats*. The arc is the skeleton; the activities are the skin.
- `requires_nodes` / `requires_group` are the gate primitives. Chains are linear; groups are N-of-M parallel unlocks.
- `journal_entry` is first-person Maya voice. `guide_hint` is what the Guide Page shows. `is_milestone = true` marks the beats that render prominently on the quest UI.
- `emotion_mappings` per NPC trait map ranges to descriptive labels — these surface automatically in the journal as the trait band shifts, so trait-band writing is a primary arc-surface-area for ambient change (see Section 10 voice specs).
- **Trigger-prose binding (added 2026-04-27).** A canvas's prose may not assert context that its trigger conditions, schedule block, or upstream flags do not enforce. Two sub-rules: (A) **Temporal coherence** — if prose names a specific weekday / hour / week / season / time-of-day, the canvas must enforce it via `[[canvases.trigger.schedules]]` (`weekdays`, `start_time`, `end_time`) and/or week-gating trigger conditions; otherwise the prose uses neutral framing (*"an evening," "later that week"*). (B) **Action causality** — if prose narrates a prior Maya-action (*"she had left the porch light on"*), that action must be flag-set by an upstream activity/canvas the player actually triggered; otherwise the prose describes the consequence without retconning the act. Worked failure: `frank_phase_a_test` ("The Porch Light") narrates Sunday W4 8:30pm + a Saturday-1am light-leaving the player never did, but its only trigger gate is `first_rent_paid is_true`. See `content_rewrite/standards.md` Rule 27/28 and `content_rewrite/qa_rubric.md` "Trigger-prose binding" section for authoring + validation enforcement.

### 7.2 Maya's backbone arc

**Arc line (one sentence, locked 2026-04-22):** *From the girl who wouldn't let her ex see her cry to a woman who has learned what her eye-contact is worth.*

**Dramatic questions:** per-chapter in Sections 5–6. Chapter 1: *can she be the girl she told herself she'd be?* Chapter 2: *what does she already know how to do that she hasn't admitted yet?*

**Tier structure:**

| Tier | Closing beat | Rough node count | Chapter |
|---|---|---|---|
| **Arrival** | enters the house; meets Frank / Ryan / Jake as strangers; meets Diana as already-present anchor | 2 nodes | Ch1 |
| **Orientation** | first full day; learns the house's rhythm | 1 node | Ch1 |
| **The math** | first concrete economic frame — rent, food, Ryan's shop + diner options, Maya's mental ledger | 1 node (milestone) | Ch1 |
| **First cycle** | first rent paid, first shift closed, pattern established | 1 node (milestone) — **closes Ch1** | Ch1 → Ch2 |
| **First tilt** | Marge hands her the key to close Thursdays alone (Section 6 lock) | 1 node (milestone) — **closes Ch2** | Ch2 |
| **Later touches** | backbone surfaces occasionally in later chapters for rent-pressure beats, Diana-call beats, whatever Phase 1 close event is eventually chosen. Node count TBD when Phase 1 ending is decided. | 2–3 nodes | Ch3+ |

**Accumulation pattern:** backbone doesn't carry the weekly texture — recurring activities do. Backbone nodes fire rarely and *feel* heavier because they're rare.

**Gate hierarchy:**
- Backbone nodes gate via `requires_nodes` (linear chain).
- **`group_settled_in`** — N-of-3 completion — opens when the backbone reaches *First cycle*. Unlocks the NPC arcs' entry tiers.
- **`first_ambient_tilt`** — single milestone flag — opens the *Noticed* / *Help* / *Know*-equivalent tier for any NPC the player has engaged with.

**What's still open for this arc:**
- Maya's midpoint crack (the quiet internal shift) — deferred per 2026-04-22 decision until the surrounding NPC cracks are concrete. They now are; this can be written any time.
- Phase 1 closing beat (what caps the "Later touches" tier) — deferred until the design is laid out in play.

---

### 7.3 Frank — discipline, and discipline cracking

**Arc line:** *The rule-enforcer loses control of the house he built his identity around — and discovers, through Maya, what he was holding the rules against.*

**Dramatic question:** *What does he hold his code against, and what happens when she names the thing underneath?*

**Designer truth (locked 2026-04-22):** *Frank wants to be chosen. Control of his house is scaffolding; underneath he wants Maya specifically — and admitting the wanting would collapse his whole self-image. The arc is the hidden wanting being forced to surface through his own discipline cracking.*

**NPC function (from Section 2.6):** landlord, household head, economic gatekeeper. Rules the house. Paperwork goes through him. Weekends require his logistics. A possible college reference later.

#### Two-phase structure

Frank's arc runs in **two distinct phases with a specific trigger event in between.**

**Phase A — Rules (non-sexual).** Starts Day 1.

| Tier | Shape | ~node count |
|---|---|---|
| **Meet** | arrival beat (backbone) + the first quiet morning on the porch | 1 backbone + 1 tier node |
| **Rules established** | Frank lays out the house code — curfew, chores, office-off-limits, expectations. Maya learns his code. | 1–2 nodes |
| **Abide (with small tests)** | Small transgressions and corrections: staying up later than allowed, borrowing without asking, skipping an assigned chore. Each met calmly but firmly. The dynamic of rules-and-obedience gets built without sexual charge. | 2–4 nodes |

This phase builds the weight that makes Phase B's trigger land. Weeks live here. Frank isn't just a landlord — he's a man holding a code, and Maya learns to navigate it.

**Trigger event — locked 2026-04-22:** *Frank catches Maya masturbating in the living room.* She's alone in the space. She chose it (or seemed to). Frank walks in. Neither speaks. The moment's ambiguity — *did she know he might come in?* — hangs over everything after. Sets `frank_caught` flag. Opens Phase B.

**Phase B — Sexual arc.** Starts when trigger fires.

| Tier | Shape | ~node count |
|---|---|---|
| **Restrict** | Frank tightens the rules. New prohibitions, extra chores, stricter curfew, specific new terms about dress or common-area behavior. Delivered calmly, without reference to what he saw. She knows what it's about. He knows she knows. | 2–3 nodes |
| **Tease under compliance** | Maya complies on the surface — does the chores, follows the rules — and teases underneath. Every extra chore becomes a proximity scene. Every new prohibition becomes material. | 3–5 nodes |
| **Crack** | Frank's discipline fails in a specific way. He enforces a rule in a way that reveals his attention (watches too long, is in the wrong place at the right time) or lets something pass that he used to enforce. She catches him. He knows she caught him. He doesn't walk it back. | 1 node (milestone) |
| **Call-out** | Maya names it: *"This is normal. Everyone has needs. Even you."* His authority-as-role collapses into man-who-wants. Dynamic inverts — now she can ask him for things. | 1 node (milestone) |
| **Keep** | branches — full sexual relationship (romantic weight), the arrangement (transactional weight), total rupture (fury or silence), power-inverted (she runs the house in some sense). 2–3 routes of roughly equal weight. | 3–5 nodes |

#### Accumulation patterns

- **Porch evenings (Phase A):** non-sexual recurring scene. Group-block variants by `frank.trust` + Maya's self-axis stats. Same porch, different attention inventory per tier.
- **Chore-supervision scenes (Phase B):** post-trigger, recurring. Every instance is a tease-under-compliance opportunity. Ambient prose tracks `frank.arousal` within a shift.
- **Office scenes:** tightly gated, high-charge. Where Phase B's Crack most plausibly fires.

#### Gate hierarchy

- **Phase A** opens Day 1. Runs in parallel with all other Phase 1 activity.
- **Trigger (`frank_caught`)** — gated on Maya's `corruption` reaching mid-tier (50+). She has to be the kind of Maya who'd choose the living room. Not random ambient; she picks it.
- **Restrict** — fires within 1–2 days of trigger.
- **Tease under compliance** — opens as soon as Restrict lands.
- **Crack** — gates on N completed chore-supervision scenes + `frank.arousal >= X`.
- **Call-out** — gates on Crack complete.
- **Keep branches** — gate on which flavor of Tease-under-compliance dominated (heavy teasing → arrangement route; restrained teasing → romantic route; resentful compliance → rupture route).

#### Craft lock — voice + body tells across phases (from Section 10)

- **Phase A:** Complete sentences, contractions dropped when serious, hands flat on surfaces, indirect mirror-gaze. *"Maya."* full-sentence-opener appears sparingly.
- **Post-trigger Restrict:** Same tells, longer pauses. Hands rest on surfaces longer. Jaw-tightening before he speaks happens more.
- **Crack tier:** *"Maya."* opener becomes routine. He watches her directly for a second before looking away. Hands press into the surface instead of resting.
- **Call-out tier:** Complete sentences break. The discipline has left the voice.

#### What's still for the content pass

- The exact prose of the living-room catch (both behaviors, the nothing-said beat, the next-morning breakfast).
- Specific rules Frank imposes during the Restrict tier.
- The Crack scene's precise setting (office? hallway? midnight kitchen?).
- The branching specifics of Keep routes (how the arrangement reads vs. how the romantic route reads, line-level).

---

### 7.4 Ryan — business partners, the big deal, the beach

**Arc line:** *He's the brother she works beside. The business is the thing he's trying to prove with. When her body closes the deal that saves them, he takes her to the beach and asks her to stay.*

**Dramatic question:** *What will she do for the business, and what does the thing she did mean to them both?*

**Designer truth (locked 2026-04-22):** *The business is what Ryan has to prove something with — mostly to Frank. He doesn't have Frank's discipline, doesn't have Jake's art, doesn't have Diana's steadiness. He has his hands and this operation. Losing it means losing the one thing that makes him legible to himself.*

**NPC function (from Section 2.6):** peer-male labor + economic partner. Ryan's shop is the secondary income channel to the diner. Her charm closes his big-ticket deals. They run a business together.

#### Tier structure

| Tier | Shape | ~node count |
|---|---|---|
| **Meet** | arrival beat (backbone) + first yard observation | 1 backbone + 1 tier node |
| **Help** | she joins the yard / truck work. He mentions money is tight. Small-ticket commerce in the background; she starts to see how the shop runs. | 2–3 nodes |
| **Partner** | she takes over customer-facing — greets walk-ins, handles the phone, closes walk-in deals with charm and eye contact. Business grows. Her corruption / charm traits gate bigger deal types. | 3–5 nodes |
| **The big deal** | a specific customer whose close requires more than flirt. She closes it with sex (blowjob or full, decided in content pass). The money lands. She walks back to the shop with the cash. | 1 node (milestone) |
| **Guilt + beach** | she returns distant. Ryan reads it. Doesn't ask what happened. Takes her to the beach the next day to console her. Neither of them plans what happens there. They cross their own line together — kiss, more, how far TBD by player track. At the end of the beach, **he asks her to stay** — proposes some form of commitment (marriage, coming-with-him, running-this-together, ambiguous per the designer pass). **This is Ryan's Crack.** | 1 node (milestone) |
| **Keep** | branches by her answer to the proposal + what she decides about the business after. **Yes:** engaged / committed. Sexual relationship opens. The guilt from the deal is the thing the engagement is trying to redeem. **Not yet:** they become lovers, but the proposal unanswered becomes a thread. Each subsequent scene carries its weight. **No:** they still cross lines that beach night, but he withdraws emotionally after. Business survives, romance doesn't. | 3–5 nodes per branch |

#### Accumulation pattern

Ryan's shop scenes are the recurring activity that carries his arc. Group-block variants by `ryan.trust` + `business_tier` (small / mid / big-ticket customers). Same shop, different customers and different Maya-energy per tier. After Crack, variants split by Keep-branch.

#### Gate hierarchy

- **Help** gates on `group_settled_in` + `first_ambient_tilt`.
- **Partner** gates on N completed Help scenes + `corruption` mid-tier (25+).
- **The big deal** gates on N completed Partner sessions + `corruption` high-tier (75+). The specific customer whose close requires sex surfaces only when Maya's corruption tier makes the close plausible. She can refuse this tier entirely and the arc caps at Partner.
- **Guilt + beach** fires automatically after the big deal. Ryan reads her mood; the beach is his move.
- **Keep branches** gate on her answer to the proposal + the tier-tone of her prior Partner work.

#### Craft lock — voice + body (from Section 10)

Ryan's tells:
- **Through Help and Partner:** fragments mid-sentence, hands always doing something, eye contact rare but landing hard. Owns uncertainty without apology. When stressed (customer pressure, a deal going south), goes silent and works harder.
- **During the big deal:** he's not in the scene — she is, alone. His voice is absent, which is itself characterization (he let her do it alone).
- **Beach Crack:** the voice-rule exception. One complete unfragmented sentence, possibly two. *"Stay with me"* / *"Marry me"* / *"Come with me when I go"* — whichever the designer picks — spoken without fragments for the first time in the game.
- **Post-Crack:** depends on Keep branch. Yes → new voice, less fragmented overall, she's the thing that steadied him. No → fragments return harder, hands stop earlier.

#### What's still for the content pass

- The specific big-ticket customer (archetype locked: sketchy buyer, probably a repeat customer who'd been hinting; specific identity TBD).
- Whether the big deal is blowjob or full sex.
- The exact form of the proposal — marriage-formal, commitment-informal, leaving-together.
- The beach's geography (nearest beach? lake? somewhere requiring a drive?) — "beach" might be pseudonymous for a specific water-adjacent place.
- Branch-specific scene writing for all three Keep routes.

---

### 7.5 Jake — hostility, forced notice, the hand

**Arc line:** *The brother who didn't want her wants her against his will, and what she does with his weakness is the arc.*

**Dramatic question:** *What happens when the person she least expected to want her wants her, and she's the one who decides what that's worth?*

**Designer truth (locked 2026-04-22):** *Jake doesn't want to want her because wanting her costs something he's been protecting. His art is beautiful women; she's not beautiful to him when she arrives; the moment she becomes beautiful is the moment his world edits itself against his will. The shame isn't that he wants her. The shame is that he ceased to be in control of the wanting.*

**NPC function (from Section 2.6):** college peer / artist. Draws nude women as his working register. Information gateway about the community college and the younger local scene. Holds the art-track gate that runs parallel to Maya's own sketching.

#### Tier structure

| Tier | Shape | ~node count |
|---|---|---|
| **Meet (hostile)** | arrival beat (backbone) + Jake's cold reception. She's the interloper, Diana's daughter, an outsider he didn't ask for. He doesn't acknowledge her at breakfast. His normal art is nude figures; she's not in that register for him yet. | 1 backbone + 1 tier node |
| **Noticed** | as Maya's `beauty` + `corruption` rise, Jake's reluctant attention catches. She sees him stealing glances. He's outwardly still dismissive. His body-rule tells (hands stop, eye contact brief-then-dropped) become readable as reluctant attraction. | 2–3 nodes |
| **Peeking + drawing** | Jake crosses a private line. He peeks at her — when she's masturbating at night, when she's bathing, wherever she's vulnerable. He draws what he sees. His secret sketchbook accumulates drawings of *her*, made from stolen looks. She doesn't know yet, but the player sees Jake's body language shift. | 2–3 nodes (some from Jake's POV, briefly, or inferred through Maya catching him in the hall afterward) |
| **Tease** | she notices he's noticing. She starts to use it. Linger in his doorway. Walk through the hallway deliberately. The dynamic is him trying not to want her and failing in small visible ways. | 2–3 nodes |
| **Caught** | she catches him — masturbating, probably in his room, probably with one of his drawings of her in view or nearby. He's mortified. She's calm. The power has inverted completely: he's been the voyeur, now she knows, and she's in control. | 1 node (milestone) |
| **The hand** | she offers. Her choice, deliberate. Handjob. He surrenders completely in the scene — she's in charge of what happens. Afterward both know they're changed. | 1 node (milestone) |
| **Keep** | branches — **she owns him** (he's addicted, she controls; she can use him for things outside sex — information, favors, leverage), **they become lovers** (mutual, the handjob was the start of something real), **he can't handle it and withdraws** (shame rebuilds, he starts avoiding her, the drawings get hidden again), **she uses him for a specific external thing** (e.g., information about the college, covering for something). | 3–5 nodes per branch |

#### Accumulation pattern

Solo sketching / bathroom / bedroom scenes (Maya's own recurring activities) accumulate Jake-peek variants. Group blocks in those passage sources insert ambient Jake-presence-noticed lines once his arc reaches Peeking tier. *Same solo activity, Maya's sense of being watched shifts per corruption tier.* The Chekhov detail-inventory technique — the protagonist notices the shadow in the hallway a week later than she should have.

#### Gate hierarchy

- **Meet (hostile)** opens Day 1. The cold reception is established early.
- **Noticed** gates on `group_settled_in` + Maya's `beauty` crossing a rising threshold — her physical appeal has to change visibly for Jake's attention to turn.
- **Peeking + drawing** fires automatically once Noticed is active, but it's *Jake's* action — not Maya's. It gates on nothing she does; it's him failing his own code.
- **Tease** gates on Maya's `corruption` reaching mid-tier — she notices his noticing (corruption-band does the work the old awareness stat did) and decides to use it.
(Tease gate condition folded into the Tease tier above — corruption mid-tier covers both "she notices his noticing" and "she acts on it.")
- **Caught** gates on N completed Tease scenes. The scene itself is a specific beat — she walks in on him, he's holding a drawing of her.
- **The hand** gates on Caught + Maya's deliberate choice. She can refuse and leave (which forks Keep into "he withdraws" or "she uses him cold-bloodedly").
- **Keep branches** gate on the flavor of her choice at Caught + her immediate follow-through.

#### Craft lock — voice + body (from Section 10)

- **Meet (hostile):** Clipped voice, monosyllabic when forced. Body hidden behind sketchbook, headphones, laptop screen. Flinches from accidental touch.
- **Noticed:** Voice still clipped. Body tells start betraying him — hands stop mid-doodle when she enters, eye contact for half a second then dropped. She starts reading these.
- **Peeking + drawing:** Off-screen mostly. But when she encounters him in the hallway afterward, he's too casual. Voice too quick. Eye contact too willing, as if to prove something. The wrong kind of calm.
- **Tease:** His voice starts breaking. The long sentences arrive — he gets verbose when he's not sure what she wants from him. Hedges constantly about himself.
- **Caught:** No voice at all. The mortification is physical. Hands stop completely. Eye contact dead.
- **The hand:** She talks; he doesn't. Maybe one line, monosyllabic. His body does the scene.
- **Keep branches:** voice diverges per branch. Owned → he becomes a follower voice. Lovers → the long sentences return differently, less defensive. Withdrawn → total silence, avoidance at meals.

#### What's still for the content pass

- The specific room Maya catches him in (his room? bathroom? living room late at night?).
- What his sketchbook contains, line-level — how many drawings of her, which moments, how detailed.
- Whether her peek into his sketchbook happens BEFORE the Caught scene (which would flavor it differently) or AT it (which would make it the trigger).
- The handjob scene's specific prose (what she says, what he doesn't).
- Branch-specific content for all four Keep routes.

---

### 7.6 Arc interactions and cross-gating

The three NPC arcs run on independent triggers but share a house. Four rules:

1. **Each arc has its own trigger and its own clock.** Frank's arc gates on a specific Maya beat (masturbating in the living room, Section 7.3). Ryan's arc gates on the business tier progression plus her corruption threshold for the big deal (Section 7.4). Jake's arc gates on Maya's physical transformation (beauty rising + corruption rising, Section 7.5). None of them depends on another arc having progressed first. Maya can run all three in parallel, or just one.

2. **At most one NPC at `Crack`-equivalent tier in any given chapter.** Frank's Crack + Call-out sequence, Ryan's Beach proposal, Jake's Caught + hand — if two of these fire in the same in-game week, both lose weight. Cross-gate so that entering a Crack-tier beat with one NPC suppresses Crack-tier entry for the others for some period. The player can still advance the others' *pre-Crack* tiers during the suppression window.

3. **`brothers_discover` milestone, late Phase 1.** The beat where the three men in the house (plus possibly Diana as silent witness) realize the others exist in Maya's orbit. Fires once, regardless of which arcs the player pushed. Shape varies by who's been active:
   - If Maya has pursued two or three arcs simultaneously: reckoning scene, all the hidden things surface, Maya has to pick a shape.
   - If Maya has pursued only one: the beat is smaller, more ambient — the other brothers register the thing they didn't see.
   - If Maya has pursued none (rare, possible): the beat is about Diana noticing something subtle, not about the brothers. (Reserved for that edge case.)

4. **Diana's silent-witness layer.** Diana is always present. Every time an arc advances a Crack-tier beat, there's a Diana-adjacent variant — did Maya come down to breakfast the next morning? Did Diana notice the way Maya didn't look at Frank? Diana never confronts in Phase 1, but her noticing is a flag that accumulates silently (`diana_awareness`, rising quietly). In Phase 1 this flag is atmospheric; in Phase 2+ it may become load-bearing for a Diana arc we haven't written yet.

### 7.7 Emotion mappings and Guide Page hints (arc surfaces)

Two `story_arc` subsystems directly carry the arc sketches into the running UI:

- **Emotion mappings.** Per Section 2.6 and the craft research (Chekhov's noticed-detail + DoL's Current Condition). Each NPC gets a 5-band `love` or `trust` mapping whose descriptions are **voice tells** rather than status labels. Example, Frank's trust progression: *"He watches the door more than he watches you."* → *"He nods when you walk in — doesn't look up."* → *"He saves you the chair with the good cushion."* → etc. These surface in the Quest page automatically as the trait band shifts; writing them is the bible's job.
- **Guide Page hints.** Per Section 1.6 and the craft research. Hints are Maya's voice, not player coaching. Target 30–50 hints across the arcs (backbone + three NPCs), each gated on a missing flag or a trait gap. Specific templates deferred.

### 7.8 What this section is NOT

- Not a node-by-node writeout. Each tier's node count is a budget, not a script.
- Not committed journal entries, linked canvases, or specific beat text. All deferred to bible + content pass.
- Not committed flag names — except the load-bearing ones (`group_settled_in`, `first_ambient_tilt`, `brothers_discover`, `drawing_started`, per-NPC trust/love). Specific flag spellings will be locked during content authoring.
- Not a guarantee that all three NPCs get equal depth. The arc shapes are sketched equally here because the redesign's intent is three deep arcs; actual node-count reality may shift when content is written.

---

## Section 8 — Schedules & Activities (rough sketch)

🔄 **Rough sketch — not yet locked.** Subject to revision as we move toward content design.

Captures the world's rhythm (NPC schedules) and Maya's available activities. Together these define what can happen when and where.

### NPC Schedules

#### Frank

**Weekday (Mon-Fri):**
| Time | What |
|---|---|
| 5:30am | Wake, gym/workout (out of house) |
| 6:30-7:30am | Kitchen — coffee, breakfast |
| 7:30am | Leaves for work |
| 8:00am-4:00pm | At work (NOT in house) |
| 4:00-4:30pm | Returns, shower |
| 4:30-5:30pm | Relaxes — porch, reading |
| 5:30-6:30pm | Cooking dinner (kitchen) |
| 6:30-7:30pm | Family dinner (table) |
| 7:30-8:00pm | Dishes / cleanup |
| 8:00-9:00pm | Paperwork in office OR TV in living room |
| 9:00-10:30pm | Porch whiskey OR continued office work |
| 10:30-11:00pm | Bed |
| Occasionally late | Up working at midnight, kitchen visits |

**Saturday:**
| Time | What |
|---|---|
| 7:00am | Wakes (slight sleep-in) |
| 7:00-8:00am | Porch coffee + newspaper |
| 8:00-11:00am | Errands — hardware store, town |
| 11:00am-3:00pm | Yard work / repairs / projects |
| 3:00-5:00pm | Beer, watch sports |
| 5:00-6:00pm | Grilling dinner outside |
| 6:00-7:30pm | Family dinner outdoors |
| 7:30-10:00pm | Porch whiskey (longer, more relaxed) |
| 10:00-11:00pm | Bed |

**Sunday:**
| Time | What |
|---|---|
| 7:30am | Porch coffee + newspaper |
| 8:30-10:00am | Church OR continued porch |
| 10:00am-1:00pm | Lazy at home, small projects |
| 1:00-2:30pm | Late lunch |
| 2:30-5:00pm | Nap, TV, reading |
| 5:00-6:30pm | Simple dinner (leftovers) |
| 6:30-9:00pm | Quiet porch evening |
| 9:00pm | Bed (early) |

#### Ryan

**Weekday:**
| Time | What |
|---|---|
| 6:30-7:00am | Wake |
| 7:00-8:00am | Kitchen (brief, overlaps Frank) |
| 8:00am-12:00pm | Yard work, property maintenance |
| 12:00-1:00pm | Lunch (often outside) |
| 1:00-3:00pm | More yard / fixing things |
| 3:00-5:00pm | Nap OR truck mechanic stuff |
| 5:00-6:00pm | Cleans up |
| 6:00-7:30pm | Family dinner |
| 7:30-9:00pm | Porch with Frank OR TV |
| 9:00-11:00pm | Out (bar Fridays) OR home |
| 11:00pm-1:00am | Bed |

**Saturday:** wakes 8am → helps Frank with errands OR works on truck → afternoon side projects (paid side-work for Maya available) → evening out with friends.

**Sunday:** wakes 9am → lazy day, fixes things → evening home.

#### Jake

**Weekday:**
| Time | What |
|---|---|
| 8:00-9:00am | Wakes |
| 9:00-10:00am | His room — sketches, studies |
| 10:00am-12:00pm | College (if enrolled / in session) OR room |
| 12:00-1:00pm | Lunch (kitchen, brief) |
| 1:00-5:00pm | His room — sketching, gaming, online |
| 5:00-6:00pm | Comes out, kitchen |
| 6:00-7:30pm | Family dinner |
| 7:30-10:00pm | His room OR yard sketching |
| 10:00pm-1:00am | Gaming/online late |
| 1:00am+ | Bed (latest of all) |

**Weekend:** wakes 10am+, mostly in his room. Sundays even more so.

#### Marge (diner owner)

At diner basically all open hours (6am open, 10pm close). Day off probably Sunday (diner closed Sundays — TBD).

#### Cookie (diner cook)

Works dinner shifts overlapping with Maya: 5pm-10pm Mon-Sat. Off Sundays (if diner closed).

#### Diner regulars (named)

| Regular | When |
|---|---|
| The Trucker (TBD name) | Friday evenings 6-8pm |
| The Church Couple | Sunday after church 11am-1pm (if diner open) |
| The Older Mechanic | Tuesday lunch noon-1pm |
| The College Kids | Late-night Fri/Sat 9-11pm |
| Others | TBD |

#### College admin clerk

Mon-Fri 9am-4pm. Closed weekends + holidays.

#### Mom (Diana)

Phone calls Sunday evenings 6-8pm window. Otherwise: not present, only mentioned.

---

### Maya's Activities (Player)

#### Solo activities (no NPC needed)

| Activity | Where | Time | Effect |
|---|---|---|---|
| Sleep | Bedroom | Until next morning | +energy, advance day |
| Shower | Bathroom | 15 min | +hygiene |
| Sketch in room | Bedroom | 30-60 min | +art, +calm |
| Sketch at creek | Creek | 1 hr | +art, +ambient nature |
| Walk the property | Property | 15-30 min | Ambient, possible encounters |
| Walk to town | Travel | 1 hr round trip | Required for town activities |
| Read | Anywhere | 30 min | Low-cost downtime |
| Cook for herself | Kitchen (off-Frank-hours) | 30 min | -$3 food, +full |
| Eat from fridge | Kitchen | 10 min | -$1 food, basic full |
| Look in mirror *(later game)* | Bathroom | 5 min | Self-perception scene at corruption tier |
| Look at brochure / journal | Bedroom | 10 min | Reflection / planning |

#### Activities with Frank

| Activity | Where | When | Time |
|---|---|---|---|
| Eat breakfast with Frank | Kitchen | Mon-Fri 6:30-7:30am | 30 min |
| Cook dinner with Frank | Kitchen | Mon-Fri 5:30-6:30pm | 1 hr |
| Help Frank with bookkeeping | Office | Mon-Fri 8-10pm (when offered) | 1-2 hr (paid) |
| Porch evening with Frank | Porch | Evenings 9pm+ | 30-60 min |
| Saturday hardware store run | Frank's truck | Sat morning | 2-3 hr |
| Help with weekend repairs | Property | Sat/Sun afternoon | 2-3 hr |

#### Activities with Ryan

| Activity | Where | When | Time |
|---|---|---|---|
| Help Ryan in yard | Yard | Weekdays 8am-3pm | 1-2 hr |
| Help Ryan with truck | Driveway | Sat afternoon | 3 hr (paid $30) |
| Watch Ryan working | Yard | Daytime | 30 min, ambient |
| Bring water out to Ryan | Yard | Hot afternoons | 15 min |

#### Activities with Jake

| Activity | Where | When | Time |
|---|---|---|---|
| Sketch with Jake | Jake's room or yard | When he's around | 1 hr |
| Watch Jake sketch | Wherever he is | Variable | 30 min |
| Knock on Jake's door | Hallway | Anytime he's home | Variable |
| Help with college stuff *(later)* | Various | When she enrolls | Variable |

#### Group activities

| Activity | Where | When | Time |
|---|---|---|---|
| Family dinner | Table | Daily 6:30-7:30pm | 1 hr |
| TV with whoever's home | Living room | Evenings | 1-2 hr |
| Saturday outdoor dinner | Backyard | Sat 6-7:30pm | 1.5 hr |

#### Diner activities (work)

| Activity | Where | When | Time |
|---|---|---|---|
| Diner shift | Diner | 5-10pm Mon-Sat (Sun TBD) | 5 hr |
| Drop by diner off-shift | Diner | Open hours | 30 min, ambient |
| Get groceries from diner | Diner | Open hours | 15 min |

#### Town activities

| Activity | Where | When | Time |
|---|---|---|---|
| Browse general store | Town | Open hours | 30 min |
| Visit college admin office | College | Mon-Fri 9-4 | 30 min |
| Get gas / supplies | Gas station | Open hours | 15 min |
| Mail something | Post office | Mon-Sat | 15 min |
| Attend church *(optional)* | Church | Sun morning | 1-2 hr |
| Walk to creek | Creek | Anytime daylight | 30 min each way |

#### Side income / extras (some open later)

| Activity | When |
|---|---|
| Side work with Ryan | Sat afternoons (paid) |
| Sell sketches *(when art track unlocks)* | Town, variable |
| Other gigs *(later content)* | TBD |

---

### Diner shift tier system (locked 2026-04-22)

The diner shift is not a single activity. It's a **tiered stance** the player picks at the start of each shift. The stance sets which customer interactions surface and which tip range is possible. Mechanically, each tier uses the same shift canvas with group-block variant prose (the Chekhov detail-inventory-shift technique, Section 3.8) — not four separate canvases.

| Tier | Stance | Tips | Gates |
|---|---|---|---|
| **0 — Distance** | Serve, smile, stay behind the counter | Base wage only | Always available from Day 1 |
| **1 — Play along** | Let them flirt, linger when they look, laugh at the jokes | Small tips. Occasional grope she lets pass (or doesn't — per-scene choice) | `corruption` low-tier (25+) + `rep_road` + minimum `beauty` threshold |
| **2 — Work the floor** | Tease actively, lean over the counter, hold the look, pick her targets | Much bigger tips. Groping becomes routine. Certain regulars tip heavily | `corruption` mid-tier (50+) + `beauty` threshold |
| **3 — Back booth / after close** | "Extra" is available. Specific regulars pay for sex acts | Shift-changing money | `corruption` high-tier (75+) + specific customer flags. **Scene-by-scene — she picks each instance individually, no mode toggle.** |

**Chapter 2 unlock:** Tier 3 "after close" is the reason the Marge-key moment (Section 6) lands — the key literally unlocks the after-hours space.

**Reputation effect:** Tier 2 and 3 shifts cost `rep_church` (visible) and raise `rep_road`. The asymmetry is deliberate: working the floor builds her reputation with the customers who see her doing it; it costs her reputation with the crowd who doesn't come Thursday nights but hears about it.

**Owner / appraisal — deferred.** Marge remains owner. No sexual content with Marge in Phase 1 — just shift dynamics, some intense shift-floor teasing as ambient. An appraisal-based sexual dynamic with the owner is reserved as a Future Consideration (Section 12 and `Future_Considerations.md`).

### Ryan's shop activities (locked 2026-04-22)

Ryan's shop on the property edge is a separate activity location from the house. Activities available there:

| Activity | What it is | When | Effect |
|---|---|---|---|
| Ride shotgun on pickup | Join Ryan fetching equipment from auction or a local seller | Saturdays / some weekdays | Ambient; introduces outside-the-house locations early; small pay |
| Work the shop (small-ticket) | Ryan does the close; Maya helps logistics | Weekday afternoons | Small pay; `ryan.trust` slowly up |
| Close a walk-in (mid-ticket) | Maya handles the customer; her charm moves the price | Weekday afternoons after Help tier | Mid pay; `ryan.trust` rise + `rep_road` rise |
| Close a big-ticket deal | Specific customer, requires more than charm. Corruption-gated | Gated by corruption threshold | Major pay; triggers Ryan's Crack (beach) after — this is the one specific deal |
| Help fix something | Non-commerce time with Ryan; ambient partnership | Weekend afternoons, certain rainy weekdays | `ryan.trust` up; no pay |

The business narrates the thesis on a P&L line. The customer types (small / mid / big) map to corruption-tier gating. Specific customer archetypes for the big-ticket tier are TBD in content pass.

---

### Design notes

**Overlap windows = where SCENES happen:**
- Frank in kitchen 6:30-7:30am + Maya in kitchen = breakfast scene
- Frank cooking 5:30-6:30pm + Maya in kitchen = cooking together
- Frank on porch 9pm+ + Maya on porch = porch scene
- Ryan in yard 8am-3pm + Maya in yard = yard scenes

**Solo windows = Maya's own time:**
- 12pm-5pm weekdays (Frank at work, Ryan working, Jake in room)
- Most mornings if she skips Frank breakfast
- Evenings after dinner (depending who's home)

**Conflicts force triage:**
- Wants Frank cooking + has 5pm diner shift → must choose
- Wants church Sunday + family Sunday lunch → must choose
- Can't do everything = real gameplay

**Schedules evolve later:**
- Early game: NPCs follow baseline schedules
- Mid-game (Maya pursuing Frank): some shifts (Frank stays late at office, kitchen visits at midnight)
- Late game: subtle reflection of Maya's effect on the household

---

## Section 9 — Navigation & Map (rough sketch)

🔄 **Rough sketch — not yet locked.** Subject to revision as we move toward content design.

Two-hub topology: Frank's Property + The Town, separated by a 1-hour walk. Mostly 2 levels of nesting (NLP-inspired hub-and-spoke pattern; avoids Shady Deals' 6-equal-regions failure mode).

### Top-level structure

```
                 ┌─────────────────────┐
                 │   FRANK'S PROPERTY   │
                 │     (primary hub)    │
                 │                      │
                 │   House + Backyard   │
                 │   + Creek + Trails   │
                 └──────────┬──────────┘
                            │
                       1hr walk
                       (one-way)
                            │
                 ┌──────────┴──────────┐
                 │       THE TOWN       │
                 │   (secondary hub)    │
                 │                      │
                 │  Diner + Stores +    │
                 │  College + Church    │
                 └─────────────────────┘
```

### Hub 1 — Frank's Property (primary)

```
PROPERTY
├── House
│   ├── Hallway (transit)
│   ├── Kitchen (Frank/Ryan/Jake at scheduled times)
│   ├── Living room (TV, evening hangouts)
│   ├── Bathroom (shower, mirror)
│   ├── Maya's bedroom (her base)
│   ├── Frank's office (LOCKED unless Frank home + stage threshold)
│   ├── Ryan's room (door usually closed, occasional access)
│   └── Jake's room (door cracked sometimes — knock or peek)
├── Front porch (Frank evenings, Ryan sometimes)
├── Back porch (Saturday outdoor dinners)
├── Backyard (Ryan working, Jake sketching sometimes)
│   ├── Creek (15-min walk, sketching, swimming, ambient)
│   └── Trail head (30-min walk, more isolated, future content)
├── Ryan's shop (property edge — converted outbuilding / back-of-barn)
│   ├── Inventory yard (machines Ryan's bought, awaiting fix or resale)
│   ├── Work bay (where Ryan does repair)
│   └── Customer-facing area (where deals close — where Maya works)
└── Driveway → walk to town (1 hour)
```

**Shop note:** distinct scene location from the house. Customers visit the shop but never enter the house — this matters for Frank's catch-trigger dynamics (Section 7.3). Seeing Maya at the shop is a different flavor than seeing her in the house.

### Hub 2 — The Town (secondary)

```
TOWN
├── Main Street (transit / arrival point)
├── The Diner (Marge, Cookie, regulars)
│   ├── Front (where Maya works)
│   └── Back office / kitchen (Marge's domain)
├── General store (clerk, supplies)
├── Gas station (clerk, transit info)
├── Post office (mailing, packages)
├── Church (Sunday morning, optional)
├── College campus
│   ├── Admin office (Mon-Fri 9-4)
│   ├── Classrooms (only when enrolled)
│   ├── Library (free study space)
│   └── Coffee bar / quad (later content)
├── [Future] Bar (later content)
└── [Bus stop] → leaving town (rare, Phase 2+)
```

### Travel time costs

| Travel | Time |
|---|---|
| Room to room (within house) | 0 (instant) |
| House to backyard | 0 |
| Backyard to creek | 15 min one way |
| Backyard to trail head | 30 min one way |
| **Property to town (walking)** | **60 min one way** |
| Property to town (Frank's truck — if available) | 15 min one way |
| Property to town (Ryan's truck — if available) | 15 min one way |
| Within town | 5-10 min |
| Town to college campus | 10 min |

### Time-of-day gating

See Section 8 for full schedules — Marge/Cookie/regulars/admin all tied to their location's open hours.

**Closed-state messaging follows NLP pattern:** visible message, NOT a missing link. *"The diner is closed. Opens at 6am."* Player learns the world's hours through play.

### Locked location handling

Three lock states:

1. **Hidden completely** — future content not yet introduced (e.g., bar before Phase 2)
2. **Visible but blocked** — known but not accessible. *"Door's locked. Frank's not home."* / *"You haven't been invited in."*
3. **Open** — default state for accessible locations

### NPC presence at locations

Driven by schedules from Section 8. Each location's "who's here" is computed from NPC schedule + day/time. Example: Maya enters kitchen at 6:45am Tuesday → game checks Frank's schedule → he's there → cooking-breakfast scene possible.

### UI presentation (proposal)

- **Sidebar:** current location, time, money, soft state notes
- **Main passage:** location description + who's here + activity buttons + sub-locations + exits + closed/locked options shown with reason
- **Optional:** simple "go-to" map page accessed via sidebar (in-fiction: Maya's phone map?)

### Why this works

- **Two clear hubs** → player forms a mental map quickly
- **Property and town feel different** (rhythms, NPCs, atmosphere)
- **1-hour town walk MATTERS** → forces planning, makes vehicle-rides valuable
- **NPC-at-location drives scenes** (uses Section 8 schedules)
- **Time-of-day gates content transparently** (player learns hours)
- **Max 2 nesting levels** (avoids burrowing problem from Shady Deals)

### What's NOT in this sketch

- Specific UI mockups (button layouts, exact prose)
- Late-game expansion locations (Phase 2+, the bar, etc.)
- Specific NPC presence per location at every time (covered by Section 8 schedules)
- Off-duty/home locations for world NPCs (Marge, Cookie etc. — deferred)
- Special locations like school events, parties (later content)

---

## Section 10 — Voice & Body Specs (rough sketch)

🔄 **Rough sketch — not yet locked.** Subject to revision in the Character Craft pass.

Voice and body rules per character. Functions as a writer's reference card — every scene authored should respect these specs so each character lands consistently.

**Design principle:** voice + body either **synced** (both doing the same psychological move) or **deliberately dissonant** (the mismatch reveals inner state). Pick one. Don't write generic.

---

### Frank (disciplined, wealthy, strict)

**Voice rules:**
1. **Complete sentences. Contractions DROPPED when serious.**
   - Casual: *"You looking for the salt?"*
   - Serious: *"You do not need to do that."*
2. **Statements where most people would ask questions.**
   - Most people: *"Do you want some coffee?"*
   - Frank: *"Coffee's fresh. Help yourself."*
3. **Technical/contractor vocabulary leaks when emotionally avoiding.** When Maya asks something hard: *"Foundation matters. Things settle wrong if you cut corners."*
4. **"Well." as a full sentence — buys time.** Used when he doesn't have the right answer ready.

**Body rules:**
1. **Hands flat on surfaces.** Counter, table, doorframe. Settled physicality, not fidgety.
2. **Watches Maya in mirrors and reflections more than directly.** Indirect gaze when noticing her.
3. **Jaw tightens before saying something difficult.** Microsecond pause + jaw set + measured speech.

**Distinctive tell:** Says *"Maya."* as a full sentence-opener when the next thing matters. *"Maya. About the rent."* / *"Maya. Look at me."* — using her name signals incoming weight.

**Integration:** **Synced — both do "controlled measured authority."** Voice deliberate, body still. Both refuse the easy reaction.

---

### Ryan (rural peer, labor, easy-going)

**Voice rules:**
1. **Fragments. Self-interrupting.** *"I was gonna — yeah. Nevermind."* Often abandons one thought mid-sentence.
2. **Colloquial without caricature.** Drops g's casually (*"workin' on the truck"*), uses "yeah/nah" instead of "yes/no" most of the time. NOT heavy regional accent — unforced informality.
3. **Owns uncertainty without apology.** *"I dunno. Maybe."* — comfortable not knowing (different from Lily's apologetic ramble).
4. **Compliments through indirection.** Doesn't say "you look nice" — says *"You ain't gonna get grease on that, are you?"* (notices what she's wearing without naming it).

**Body rules:**
1. **Always doing something with his hands.** Wiping grease, fixing something, holding a tool, rolling sleeves. If he stops, you notice.
2. **Eye contact rare — looks at his work or the horizon.** When he DOES make eye contact, it lands hard.
3. **Stretches after sustained tasks.** Rolls shoulder, cracks neck, sleeves get adjusted. Constant low-grade physicality.

**Distinctive tell:** When stressed, **goes silent and works harder.** Stress = withdrawal into physical labor.

**Integration:** **Synced — "comfortable in motion, slightly evasive in stillness."** Voice and body both prefer doing over talking.

---

### Jake (artist, college, awkward)

**Voice rules:**
1. **Long sentences when comfortable. Clipped to monosyllables when not.**
   - Comfortable: *"There's something about the way light hits the side of a face when it's evening — you don't even need to draw the rest."*
   - Uncomfortable: *"Yeah. No. Maybe."*
2. **Vocabulary shows education in unexpected ways.** Uses words like "indubitably" or "particular" or "ostensibly" without irony. Slightly anachronistic for a college kid.
3. **Hedges constantly when speaking about himself.** *"I mean, I think — I don't know if it's good, but..."* Different from Lily's apology — he's not sorry, he's uncertain about his own value.
4. **Asks too many follow-up questions when interested.** When Maya says something he finds interesting, he asks two or three questions in a row.

**Body rules:**
1. **Hides behind objects.** Sketchbook held up, headphones on, laptop screen between him and the room. Always partial cover.
2. **Hands move when thinking.** Tapping fingers, twisting a pencil, fidgeting with sleeve. When his hands stop, he's locked in.
3. **Flinches from unexpected touch.** A casual brush in the kitchen makes him pull back slightly. Small but consistent tell.

**Distinctive tell:** **Eye contact when surprised — never sustained.** When Maya says something unexpected, eyes dart up, hold for half a second, drop again.

**Integration:** **Synced — "guarded openness."** Voice verbose when safe, clipped when not. Body hidden behind things, briefly exposed when caught off-guard.

---

### Maya (PC — third-person close narration)

**Narration / internal voice rules:**
1. **Observes before reacting.** Internal monologue notices physical details first (the dust on Frank's sleeve, the shape of Ryan's hands, the smell of Jake's room) — then evaluates.
2. **Voice tightens or relaxes based on stage.**
   - **Early game:** cautious, watching, sentences hold back
   - **Mid game:** sharper, calculating, runs hidden math
   - **Late game:** more deliberate, tight when needed, sincere when she chooses to be
3. **Artist's eye in narration.** Describes people the way she'd sketch them — angles, light, what she'd shade darker.
   - *"Frank's profile from the kitchen door — half-lit, the line of his jaw harder than from the front."*
4. **Internal hedging when uncomfortable with what she's doing.** *"You don't have to. You don't have to. You do."* (the moment of doing the thing she said she wouldn't)

**Body rules:**
1. **Closed-off posture early game.** Arms folded, hands in pockets, shoulders pulled in. Opens up across stages.
2. **Sketches when processing.** Anxiety, confusion, big decisions — pencil comes out. Her sketches reveal what she can't say.
3. **Holds eye contact deliberately later in the arc.** Early she looks away; mid-game she experiments with holding it; late game she USES it.

**Distinctive tell:** **The pause.** When something charged happens, Maya pauses a beat too long before responding. Not paralysis — calculation. Reader/player learns to read her pauses.

**Integration:** **Evolves from dissonant to synced.** Early: body says closed-off, voice says calculating (mismatch — she's hardening but not yet ready). Late: body and voice both do "deliberate, knowing, controlled" (synced).

---

### Specs for world NPCs (Marge, Cookie, regulars, etc.)

🔒 **Deferred to content design pass.** Lighter specs than the family NPCs above — these characters are mechanical gates first, deep voice + body work less critical. Will sketch when we write their content.

---

## Section 11 — Open Questions (to resolve next)

1. ❓ Town: region, name, specific era feel (deferred by choice, not urgent)
2. ❓ Exact savings target number + economic scale (rent, tuition goal, weekly costs)
3. ❓ Maya's midpoint crack — specific content (deferred per 2026-04-22; surrounding arcs now concrete enough that this can be written)
4. ❓ Phase 1 closing event (deferred per 2026-04-22 until design is laid out in play)
5. ❓ Marge's past — her own history (locked as non-arc for now; content is a Future Consideration)
6. ❓ Ryan's business — specific big-ticket customer archetypes
7. ❓ Prologue content specifics — locations, beat-level choices, ex's name, friend-group geography
8. ❓ Diana's specific voice traits (reserved for Character Craft pass — Section 10 has only Frank / Ryan / Jake / Maya)

---

## Section 12 — Deliberately Deferred (for future passes)

- 🔒 **Arc node content per NPC** — journal entries, linked canvases, dialog beats for Frank / Ryan / Jake. Section 7 locks the shape; content writing is the next pass.
- 🔒 **Prologue content specifics** — Section 4 sketches the Prologue's shape; specific prose for the 20 scenes, the revenge-act beat-level choices, the confrontation tone, and the Prologue-cast voice work all waits.
- 🔒 **Activity specifications** — detailed per-activity content (solo + Frank + Ryan + Jake + diner + town + Ryan's shop). Section 8 lists activities at the catalog level; variant-prose tiers and node chains are a later pass.
- 🔒 **Diner tier 2–3 prose content** — the shift variants for Tier 2 (work the floor) and Tier 3 (after close), including customer archetypes and specific scene types. Tier system structure is locked (Section 8); prose is content pass.
- 🔒 **Ryan's big-ticket customers** — specific archetypes for the big-ticket tier, including the one customer whose close requires sex (Crack-tier trigger).
- 🔒 **Guide Page hint writing** — 30–50 hints target across backbone + three NPC arcs, Maya-voice. Per Section 7.7.
- 🔒 **Economic system specifics** — exact rent amount, income rates per activity tier, expense schedule. Structure locked in Section 3.8.
- 🔒 **Emotion-mapping band descriptions** — the voice-tell strings per NPC per trait band (Section 7.7).
- 🔒 **Content rating and NSFW scope per NPC** — per-arc tier of escalation + opt-out structure.
- 🔒 **World-NPC specs** — Marge, Cookie, diner regulars, college admin, town shopkeepers. Lighter than family-NPC specs. Section 10's "Specs for world NPCs" subsection.
- 🔒 **Diana's voice specs** — her voice + body rules + distinctive tells. Not in Section 10 yet.
- 🔒 **Diana arc for Phase 2+** — what Diana notices, when, and what she does with it. Reserved for the phase after Phase 1. `diana_awareness` flag accumulates silently in Phase 1.
- 🔒 **Prologue ex's name + friend-group details** — Daniel, Emma, Kevin, Sarah are placeholder names; may revise at content pass.
- 🔒 **Owner / appraisal sexual content at the diner** — an appraisal-based dynamic with Marge (or a male owner surfaced later). Reserved as a Future Consideration; not in Phase 1. Logged in `Future_Considerations.md`.
- 🔒 **Calendar expansions** — Friday football, Saturday farmer's market, First-Saturday flea market, county fair. Phase 2+ only. Phase 1 has Sunday only (Section 2.10).
- 🔒 **Shadow layer / criminal underground** — reserved per 2026-04-22 decision. The town has atmosphere-level tension but no active dark plot in Phase 1. Add in Phase 2+ only if pacing needs it.
- ✅ **Hour-scale arousal decay** — resolved. Engine audit (2026-04-22) confirmed native support via `modifier_effects` with `duration_hours`. Apply offsets on teasing choices; the engine clears expired offsets automatically. No engine work needed.
- ✅ **Dynamic sidebar-text gating** — resolved via Engine PRD F1. New `trait_words` sidebar type renders band-descriptive text from trait value. Shipped 2026-04-22.

---

## Change Log

### 2026-04-19 (document creation)
- Doc initialized
- **Direction locked:** Rural coming-of-age + economic pressure (Directions 1+2 combined)
- **Scope widened:** Game is no longer limited to family drama — world + Maya + NPCs must align
- **Phase model confirmed:** Scope-expansion phases, not bounded acts. Phase 1 ends at Mom's return.
- **Structural approach confirmed:**
  - Content-rich with game properties (not VN, not pure sandbox)
  - Activities carry story content; story arc = "what to do next" hints per track
  - Per-NPC parallel arc model (ZSL-style)
  - Every engaged NPC arc reaches sexual content; refusal is granular within arcs
- **Excluded:** full Path C (no-sex-ever-with-NPC branches). Player focus shifts, doesn't disappear.
- **Time limitation removed:** Explicit rejection of the 8-week / 56-day fixed window. Phase 1 has no fixed duration. Mom's return is a story-triggered event, not a calendar deadline.
- **Title locked:** "The Long Summer" — chosen for atmospheric fit, compatibility with open-ended duration, and tonal flexibility.

### 2026-04-20

- **Maya's character locked:**
  - Age 18, artist-inclined, hardened from recent breakup + friend-group collapse
  - Here because life fell apart + free housing via Mom's absence
  - Wants: save to move out / build financial independence (art is private, not career)
  - Voice evolves across summer: cautious → calculating → strategic-with-sincere-core
- **Framing locked:** Maya uses her effect on men deliberately — she's the active agent, not passive victim. "Lust as tool" framing.
- **Corruption system locked:**
  - Maya starts unaware, gets corrupted systemically over the summer
  - NO catalyst character or awakening scene — change is emergent from stats
  - Shady-style hybrid: ~60% player-driven, ~30% passive ambient exposure, ~10% soft-forced (economic-triggered)
  - Soft meters in sidebar (words, not numbers) — corruption stat NOT visibly numeric to player
  - 2-3 forced events only, all tied to economic state
- **Rejected alternative directions:**
  - NLP-style forced corruption (can't stay pure) — rejected; Maya has agency
  - ZSL-style pure player-drive with no passive pressure — rejected; world should push gently
  - Specific character-triggered awakening (coworker teacher, mother's letters, stranger) — rejected; narrative catalyst is too narrow to shape a game
  - Frank business crisis / "Miss Chen" subplot / Sarah (Frank's dead daughter) — rejected; Frank is stable, wealthy, disciplined instead (details in Frank's section — deferred)
- **NPC design principle locked (Section 2.6):** NPCs designed as mechanical gates FIRST, relationship targets SECOND. Applies to both family/household NPCs (Frank/Ryan/Jake) and world/town NPCs (diner boss, regulars, professor, shopkeepers). Relationships layer on top of function.
- **Thesis locked (Section 1.6):** *"Take Maya through a long summer in a rural town that doesn't yet know her — broke, alone, staying at her stepfather's place, and starting over. As she learns what her body and her wits can earn, you decide who she becomes — and how much she walks away with."* Functions as both player-facing welcome-page text and design north star. Leads with the TOWN to emphasize the game is not only about family or Frank.
- **Endgame design explicitly out of scope:** This is an ongoing game (like ZSL). We're setting up foundation + writing first few chapters, not designing endings. Mom's return is a known phase boundary; specific outcomes at that boundary are deferred indefinitely.
- **Chapter 1 rough sketch added (Section 4):** ~10 in-game days (Saturday → Monday rent), establishment chapter ending at first rent paid milestone. Maya arrives, gets diner job (Marge), meets Cookie, sees college campus + picks up brochure ($1,500 tuition+books target seeded), receives 2 Mom calls (Sunday cadence), polite household intros only. **Not locked** — subject to revision. No major arc beats fire in Chapter 1; design principle = "establish, don't escalate."
- **Chapter 2 rough sketch added (Section 5):** Days 11-21, second work-week into third. Accumulation chapter — world textures (named regulars, Cookie peer dynamic, Frank evening rhythm), college application submitted, Ryan side-work opened, Mom's call probing slightly, second rent paid, Marge offers more shifts. Closes on first ambient awareness tilt (trucker $20-tip moment) — a SEED, not a beat. **Not locked** — subject to revision. Design principle = "accumulate, don't escalate."
- **Schedules & Activities rough sketch added (Section 6):** Daily/weekly schedules for Frank (weekday/Sat/Sun), Ryan, Jake, Marge, Cookie, diner regulars, college admin, Diana. Plus Maya's activity inventory across solo / Frank / Ryan / Jake / group / diner work / town / side income categories. Includes design notes on overlap windows = scene opportunities, solo windows = Maya's own time, conflict forcing triage, schedule evolution later. **Not locked** — subject to revision in content design pass.
- **Navigation & Map rough sketch added (Section 7):** Two-hub topology (Frank's Property + The Town, separated by 1-hour walk). NLP-inspired hub-and-spoke pattern (max 2 levels nesting). Property hub layout (house with rooms, backyard, creek, trail head). Town hub layout (Main Street, diner, stores, post office, church, college campus). Travel time costs (1hr walking town, 15min by truck). Time-of-day gating with transparent closed-state messaging (NLP pattern). Three lock states: hidden / visible-but-blocked / open. UI proposal: sidebar + main passage + optional map page. **Not locked** — subject to revision.
- **Voice & Body Specs rough sketch added (Section 8):** Per-character voice rules (sentence-level patterns, vocabulary, recurring tells) + body rules (gestures, posture, eye contact, physical tells) for Frank (synced controlled-authority), Ryan (synced comfortable-in-motion), Jake (synced guarded-openness), Maya (evolves from dissonant to synced). Each NPC has 3-4 voice rules, 3 body rules, one distinctive tell, and a voice+body integration note. Design principle: voice + body either synced (same psychological move) or deliberately dissonant (mismatch reveals inner state). World NPC specs (Marge, Cookie, etc.) deferred to content pass. **Not locked** — subject to revision in Character Craft pass.

### 2026-04-21

- **Chapter 1 & 2 rough-sketch tables removed (Sections 4 & 5).** Day-by-day scene lists were calendar choreography against a hollow center — committed specific scenes to specific days without a dramatic question underneath. Cut because (a) scenes were interchangeable across days, (b) specificity pre-empted the storylet-gated design the craft research argues for (milestones as events, not dates), (c) chapters were written before the bible existed. Keeper pieces retained as placeholders: chapter concept (establishment / accumulation), close events (`first_rent_paid` / `first_ambient_tilt`), design principles, NOT-IN boundary markers. Real Chapter 1/2 beat design deferred to post-bible content pass.
- **Story Arcs rough sketch added (Section 6 — new section, pushing Schedules/Navigation/Voice/Questions/Deferred down to Sections 7/8/9/10/11).** Structure: Maya's 6–8-node backbone (Arrival → Orientation → The Math → First Cycle → First Tilt → Later Touches) plus three parallel NPC arcs, each with a Meet → Know/Work/Share → Touch → Crack → Keep tier table. All three NPC arcs give Keep-tier branches equal design weight — no arc has a single "default" ending. Cross-gating rules locked: one Crack per chapter, `brothers_discover` milestone at Phase 1 end, Frank's arc reactive to the others. Load-bearing flags locked: `group_settled_in`, `first_ambient_tilt`, `brothers_discover`, `drawing_started`, per-NPC trust/love. Tier node counts are budgets, not scripts. Specific node content, journal entries, linked canvases deferred to bible + content pass. **Not locked** — subject to bible-pass revision.
- **Sections 6–10 renumbered to 7–11.** Schedules & Activities → 7. Navigation & Map → 8. Voice & Body Specs → 9. Open Questions → 10. Deliberately Deferred → 11. Internal cross-ref in Navigation section updated ("See Section 6 for full schedules" → "See Section 8 for full schedules").

### 2026-04-22 — the big pass

Bible was effectively written and the redesign doc caught up to it in one sweep.

**Locked (14 of 15 bible questions + 11 new items emerged and answered):**
- Maya's one-sentence arc: *"From the girl who wouldn't let her ex see her cry to a woman who has learned what her eye-contact is worth."*
- Maya's shame engine: cheat-for-cheat with her ex in the Prologue. Her shame is *intent*, not *act*.
- Recurring obsession: two-layer motif — hands (public) + dicks + dreams of them (private).
- Voice axis: early prose observes; late prose operates.
- Chapter 1 dramatic question: mind self-sufficient, body already wanting.
- Chapter 2 dramatic question: what she already knows how to do and hasn't admitted.
- Frank's designer truth + two-phase arc: Rules (non-sexual) → Trigger (catches her masturbating in living room) → Restrict / Tease / Crack / Call-out / Keep. He wants to be chosen.
- Ryan's designer truth + business-and-beach arc: Help → Partner → Big deal closed with sex → Beach proposal → Keep branches based on her answer. The business is what he proves with, mostly to Frank.
- Jake's designer truth + hostility-to-hand arc: Meet hostile → Noticed → Peeking/drawing → Tease → Caught → Hand → Keep branches. He doesn't want to want her because wanting costs something he's been protecting.
- First ambient tilt locked: *Marge hands her the key to close Thursdays alone.* Sets `first_ambient_tilt`, closes Chapter 2.
- Phase 1 calendar minimum: Sunday only.
- Diana locked as widow-remarried, good relationship with Maya, strict-structural household anchor. Not an arc in Phase 1.
- Prologue locked as Phase 0 (new Section 4) — full playable phase, ~20 scenes, 4 acts, with placeholder cast (Daniel/Emma/Kevin/Sarah) and flags that carry into Phase 1.
- Cross-gating updated: each arc has its own trigger, max one Crack-tier beat per chapter, `brothers_discover` late-Phase-1 milestone, `diana_awareness` silent accumulator.

**Deferred by choice (2):**
- Maya's midpoint crack — surrounding arcs now concrete enough to write when we want.
- Phase 1 closing event — design laid out first; end decided later.

**Structural changes to the doc:**
- **Section 1.6 thesis rewritten** — moral-code-editing-under-pressure framing; removed "broke, alone" (Diana is present from Day 1).
- **Section 2 fully rewritten** — Southern permissive-register tonal lock, sub-reputation system (rep_church / rep_road / rep_college), Diana as 2.7 subsection (household anchor, widow-remarried, strict-structural, good relationship with Maya), shadow layer deferred, Phase 1 calendar minimum (Sunday only), Phase 1 physical-map scope lock (5 active hubs), Ryan's business structure (used-equipment flip, small/mid/big-ticket tiers).
- **Section 3.8 added** — systems layer: Maya's core stats (Energy, Hygiene, Awareness, Confidence, Corruption, Exhibitionism, Promiscuity), per-NPC stats (Arousal via `modifier_effects` duration_hours, Corruption, Trust/Love), "words not numbers" display rule, economic system reserved.
- **Section 4 added** — Prologue / Phase 0 rough sketch. Full phase with dramatic question, setting, cast, 4-act beat structure, mechanics active, flags carrying into Phase 1.
- **Chapter placeholders (Sections 5 & 6) — dramatic questions locked in both; first ambient tilt moment locked (Marge keys).**
- **Section 7 (Story Arcs) — three arc rewrites.** Frank's two-phase (Rules → Trigger → Sexual arc), Ryan's business-to-beach-proposal, Jake's hostility-to-hand. Each with designer truth, tier structure, gate hierarchy, voice/body craft lock. 7.6 cross-gating rewritten with new trigger model. 7.2 backbone updated.
- **Section 8 — diner tier system added** (0/1/2/3, group-block variant prose, scene-by-scene agency at Tier 3). **Ryan's shop activities subsection added.**
- **Section 9 — property map updated** to include Ryan's shop as a distinct scene location on the property edge.
- **Section 11 — open questions refreshed** (removed Mom-return items since Diana doesn't leave; added Prologue content, Ryan's big-ticket customers, Marge's past, Phase 1 closing).
- **Section 12 — deferred list updated** with 2026-04-22 context — structural locks, engineering flags, content-pass items.
- **Sections 6–11 renumbered to 7–12** (Prologue insertion at Section 4 pushed everything after Section 3 down by one).

**Engineering flags raised (not blocking the bible, blocking content pass):**
- ~~Per-hour NPC arousal decay isn't engine-native. Needs scheduled canvas resets or equivalent.~~ **Superseded 2026-04-22:** native support confirmed via `modifier_effects.duration_hours`.
- Dynamic sidebar-text gated on stat bands isn't engine-native. Needs sidebar-system extension or Quest-page work.

**Not locked (reserved for the content pass):**
- All individual scene prose, all dialog beats, all journal entries, all Guide Page hint lines, emotion-mapping band strings, exact economic numbers, town name, Prologue cast names (placeholders only), Marge's past content, Diana's voice specs.

### 2026-04-22 (second pass) — stat consolidation + two new traits

- **Four-axis split collapsed into a single `corruption` axis.** The previous same-day design had Maya's sexual/social drift across `awareness` / `confidence` / `exhibitionism` / `promiscuity` as four parallel stats. Consolidated to a single `corruption` meter with tiered bands (0–24 Closed / 25–49 Opening / 50–74 Operating / 75–100 Saturated). All gating language throughout Sections 3.7, 3.8, 4.6, 4.7, 7.3, 7.4, 7.5, 7.6, 8 updated to reference `corruption` tiers directly. **Why:** cleaner authoring surface (one tier check per scene), cleaner sidebar (one `trait_words` meter with 4–5 bands carries the whole arc), smaller player-facing cognitive load. **Trade-off accepted:** loses the DoL-style distinction between "willingness to be seen" vs "willingness to be touched." Recovered where needed via NPC-specific trigger conditions (e.g., Frank's catch-trigger is `corruption` + "in the living room," not `corruption` + `exhibitionism`).
- **`fitness` added** — slow-rising physical capability. Distinct from energy (daily capacity vs long-term stat). Gates physical activities (jogging, creek swims), Ryan's yard-work progression, stamina for long diner shifts.
- **`beauty` added** — slow-rising physical appeal. Supersedes the older "allure" proposal. Gates Jake's *Noticed* tier per Section 7.5, contributes to diner tip ceiling, general NPC attention thresholds.
- **Player trait set now reads (10 total):** `energy`, `hygiene`, `fitness`, `beauty`, `corruption`, `calculation`, `money`, `rep_church`, `rep_road`, `rep_college`.
- **Engine impact: zero.** All changes are new `[player].core_traits` names — no new schema primitives, no new widget types required. Works within the engine as it stands after the 2026-04-22 PRD implementation.
- **Content-pass impact: lower.** Tier bands and `trait_words` strings still need writing, but one 4-band corruption meter is considerably less authoring than four 4-band axes.
