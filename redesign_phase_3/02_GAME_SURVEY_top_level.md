# Game Survey — top-level design across 10 games (research for Step 2)

Live-played 10 adult sandbox/VN games for their **top-level shape** (drive · progression spine · day
loop · world logic · story shape · endings), NOT mechanics. This is the evidence base for designing
the **Top-level design step**. Per-game notes live in each `game_explorations/tl-<slug>/notes.md`;
key state dumps were read from `SugarCube.State.variables` (the fastest route to a game's real spine).

**Method note / access caveats:** mopoga games = SugarCube/Harlowe, drove directly (one needed a
manual reload past the PLAY button). gamcore.ch games are referer-gated + ad-walled + cross-origin —
The Company + Back to Freedom were reached via their CDN URLs (read full state); Young Maria was
title-screen + sidebar only (visual, no JS state). Confidence flagged per game.

---

## Per-game one-line top-level read

1. **Better Sit Home** — LINEAR linkreplace VN. Resort → witness cult → forced TG/fertility-pharma plot. Day/chapter labels but zero free-roam; "Fertility Tracker"+money are THEMATIC display, not an economy. *The linear extreme.*
2. **Lustbound** — MAXIMALIST multi-system sandbox. Supernatural frame (harvest "lust essence"); per-char relationship+perks; NPC body/gender TRANSFORMATION; combat; a seduction minigame; OnlyFans + prostitution economies; paperdoll; mom-house heat. *The kitchen-sink extreme.*
3. **Generic Porn Game (Origination)** — PURE open-ended life-sim. Explicitly "no fixed goals." Real-clock time; stat PORTFOLIO (energy/cash/fitness/intelligence/sexskill/stress); bank/university/hospital/hotel sub-systems; job interviews. *The toolbox-sandbox, zero narrative spine.*
4. **Gakko no Monogatari** — WHOLE-LIFE progression sim (Harlowe), strong literary prose. Transfer student → leveled social stats (confidence/fame/academic, each with level+desc) → CORPORATE-CAREER subsystem (rank/office/subordinates/promotions) → marriage. *Life-stage span: student → executive.*
5. **Galactic Outlaws** — RTS-MOLD family-corruption sandbox (sci-fi title, family-breakfast content — mislabeled). Per-NPC CORRUPTION + STAGE (mom/sis) + player stats + a mainquest. *Corroborates the RTS template.*
6. **Become Someone** — SCALE sandbox, closest to OUR engine. ~40 NPCs each with trust+corr(corruption)+questmain + an explicit SCHEDULE (loc-by-period); player int/str/charisma/dom/sub/money/debt; relationship states gf→slave→collar; named day periods. *Many parallel scheduled per-NPC arcs.*
7. **Emilie Finds a Way** — FEMALE-PC, INVERTED direction (Harlowe). Spine = Emilie's OWN traits (openminded/arousal/charisma/fitness/sharing) + per-PARTNER ADDICTION meters + staged activity tracks (gym/run/yoga 1-5). *Self-corruption as the whole spine; "addiction" reframes corruption.*
8. **The Company** — CORPORATE-TRANSFORMATION sandbox. Chapter-gated story; banded relationships (HATE→LOVE); deep gender/body TF system (male/female/bimbo/sissy/trans + days-in-state); Money/Paycheck + slave economy; factions. *Transformation as central mechanic + economy.*
9. **Young Maria** (access-limited, visual only) — FEMALE-PC SugarCube life-sim, SAME sidebar chassis as RTS/Become Someone (clock 08:00/Monday, money, energy 100/100, portrait). *Genre-standard sandbox chassis, female PC.*
10. **Back to Freedom** — DATING-SIM / harem sandbox. Per-NPC DUAL AXIS = LOVE + LUST across ~15 women + friendship/respect for guys; player corruption+money; GIFT economy (flower/chocolate/teddybear/perfume → meters); incest toggle; gallery. *Dating-sim two-axis (vs RTS corruption+arousal).*

---

## Cross-game patterns (the actual learnings)

### A. Structure is a SPECTRUM, and it's the FIRST top-level fork
`linear VN (Better Sit Home)` → `story-framed sandbox (Gakko, The Company — chapter spine over a sandbox)` → `open sandbox (Generic PG, RTS, Galactic, Become Someone, Back to Freedom)` → `maximalist multi-system (Lustbound)`.
**Implication:** the Top-level step must FIRST pick where on this spectrum the game sits — it governs everything downstream (a linear VN needs no economy/feeders; a sandbox lives or dies on them).

### B. The progression spine has TWO halves, and BOTH are menus (not "just corruption")
This is the biggest finding. Our skill hard-assumes corruption+arousal/relation. The survey shows a **menu of validated models**:

**Per-NPC escalation axis (how an arc climbs):**
| Model | Games | Shape |
|---|---|---|
| corruption + arousal | RTS, Galactic Outlaws | corrupt-the-other + readiness throttle |
| corruption + stage | Galactic Outlaws | corruption gates discrete stages |
| trust + corruption | Become Someone | warm-up + depravity, dual |
| **love + lust** | Back to Freedom | dating-sim: affection vs desire |
| relationship + perks | Lustbound | relationship tier unlocks perk picks |
| **addiction (per partner)** | Emilie | the PC gets addicted to each lover |
| banded relationship (HATE→LOVE) | The Company | discrete affection bands |
| relationship/friendship/respect | Become Someone, Back to Freedom | non-romance NPCs get a lighter single axis |

**Player-side spine (what the WHOLE game climbs):**
| Model | Games |
|---|---|
| player corruption as content-tier | RTS, Galactic, Back to Freedom (supporting) |
| stat PORTFOLIO (energy/fitness/int/charisma/…) | Generic PG, Gakko, Become Someone |
| self-traits / self-corruption (PC escalates) | Emilie, (Young Maria likely) |
| body/gender TRANSFORMATION state | The Company, Lustbound, Better Sit Home |
| magical/meta RESOURCE | Lustbound (lust essence) |
| leveled social stats w/ named tiers | Gakko (confidence/fame/academic levels) |

**Implication:** the Top-level step must let the author PICK the per-NPC axis model AND the player-side
spine from a menu — corruption+arousal is ONE option, not the default truth. (And these can be per-NPC:
a game can run dating love+lust on one NPC and corruption on another.)

### C. The day loop is near-universal (and a genre-standard HUD chassis)
Almost every sandbox shares: **day + time (slots/periods, sometimes a real clock) + energy + money +
sleep-advances-day**. The HUD is a near-identical chassis across RTS / Become Someone / Young Maria:
**left sidebar = clock + money + energy + character portrait + per-NPC relationship panel.** Generic PG
uses a real ISO clock (5-min ticks); most use named periods (Morning/Afternoon/…). Energy is the
per-action pacing resource; money the pressure.
**Implication:** the day loop is a near-default to CONFIRM, not design from scratch — pick slot-vs-clock,
the periods, and the pacing resource (energy). (This matches LC's day-cycle work already done.)

### D. World logic = "state opens the world" (the shared spine of every sandbox)
Universal: **player/NPC state meters gate content TIERS**, and **scheduled NPC presence gates
encounters** (explicit in Become Someone's loc-by-period; implicit elsewhere). The feeder economy
(activities raise meters → meters unlock content) is the engine of every sandbox here. Gift economies
(Back to Freedom) and resource economies (Lustbound lust essence) are variants of the same "spend an
input to move a meter to open content" loop.
**Implication:** confirms the feeder-economy concept is genre-core, not RTS-specific. The Top-level step
must design the "what opens as you progress" loop explicitly.

### E. Story shape & endings: mostly OPEN, spine-optional
- **Open sandbox, content-update-driven, soft/no endings:** Generic PG (none), RTS, Become Someone, Back to Freedom, Lustbound. Goals are self-set or per-NPC quest chains.
- **Chapter/story spine over a sandbox:** The Company (chapters), Gakko (life stages).
- **Hard linear with a fixed ending:** Better Sit Home.
**Implication:** endings are usually LIGHT in this genre — a Top-level step should treat "open sandbox
with milestone goals" as the default and "hard endings / chapter spine" as deliberate opt-ins. (Matches
LO's earlier lean.)

### F. Transformation & female-PC are common top-level FRAMES (not edge cases)
Body/gender transformation is a *central* top-level mechanic in 3/10 (The Company, Lustbound, Better
Sit Home) and a female PC in 3/10 (Emilie, Young Maria, + Back-to-Freedom-adjacent). These reframe the
whole spine (self-transformation/self-corruption rather than corrupt-the-other). Worth being a
first-class option in the Top-level step's "what kind of game" menu.

---

## Direct implications for the Top-level design step (Step 2)

The survey says the Top-level step should make the author choose, in roughly this order:
1. **Structure** on the linear↔sandbox spectrum (the master fork).
2. **Drive archetype** — debt/money survival · fresh-start self-direction · supernatural power · corrupt-the-household · harem-building · self-liberation · corporate-role. (Pick or blend.)
3. **Progression spine — BOTH halves, from a menu:**
   - per-NPC axis model (corruption+arousal / love+lust / trust+corruption / addiction / relationship+perks / banded). Can vary per NPC.
   - player-side spine (corruption-tier / stat-portfolio / self-traits / transformation / resource).
   - + the **feeder economy** that climbs them (carry-over from the content-design work).
4. **Day loop** — confirm the genre-standard chassis (slot-vs-clock, periods, energy pacing, money pressure, NPC schedules).
5. **World logic** — how state opens the world (tiers + scheduled presence).
6. **Story shape & endings** — default open-sandbox-with-milestones; opt into chapter-spine or hard endings.

**The single most important upgrade:** the spine is a **menu**, not "corruption." The current skill's
corruption+arousal/relation assumption is ONE valid model among many the genre uses. Step 2 should
offer the menu and record the choice in the design book, so NPC arcs (Step 3) build on the chosen axes.
