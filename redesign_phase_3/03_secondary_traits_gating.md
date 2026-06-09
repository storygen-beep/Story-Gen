# Secondary-trait gating logic (study for the progression engine)

Source-read study of HOW non-corruption player stats gate content, so each menu/spine choice has a
real rulebook (LO's concern: "how would Claude know how it works — I'm worried it'll write randomly").
Studied live: **RTS** (north-star), **Generic Porn Game** (stat-portfolio), **Gakko no Monogatari**
(leveled-tier). Method = read `SugarCube.State.variables` + grep the StoryJS/passages for each stat's
GATE sites (`<<if>>`/requirement objects) and RAISE sites (mutators).

---

## The headline finding

Secondary traits don't gate one way — they gate in a **small set of distinct PATTERNS**, and **each
stat that matters owns a SEPARATE content domain.** Also, every game studied **declares more stats
than it meaningfully gates** (the dead-stat trap — see §3). So "add intelligence and it'll gate stuff"
is naive; a stat only earns its keep if it owns a domain and gates it by one of the patterns below.

---

## §1 — The six gating PATTERNS (the rulebook)

| Pattern | What it does | Evidence | When to use |
|---|---|---|---|
| **Hard content tier** | point thresholds gate the CORE (lewd) content tiers; the primary spine | RTS corruption 0/5/15/30/45 + exhibitionism (the `requirementsMC` ladder) | the main progression spine (one per game) |
| **Banded capability** | thresholds (`lte20` / `gte50` / `gte70`) switch/unlock content per band; the stat OWNS a domain | GPG fitness (124 uses: gte70/gte50/lt50/lte20), sexskill (gt50/lte20) | a secondary stat that changes a specific domain's content by level |
| **Leveled-tier track** | raw points → a derived LEVEL (often exponential spacing) → NAMED ranks; content gates on the level | Gakko confidence 30/90/270/540/1080/2160/4320→lvl1-8; fame 25/50/100/200→"Nobody→Sensation"; academic→"Grade…→Graduate" | a long self-improvement ladder you want to FEEL like leveling up |
| **Inverse / maintenance** | HIGH value BLOCKS or degrades; must be managed DOWN via a restore loop | GPG stress (gt25&lte50 / gte100 breakdown); RTS energy drain | a pressure stat the player fights to keep low (stress/hygiene/drunkness) |
| **Action cost** | `>0` to act, `<1` blocked; paces the day, spent per action | energy EVERYWHERE (GPG 147 uses `gt 0`; RTS energy) — this is our engine's `costs` | the per-action pacing resource (every sandbox needs one) |
| **Soft modifier** | feeds OUTCOMES (earnings / NPC reaction / success chance), never a hard lock; often COMPUTED (base+clothing+drugs) | RTS beauty (83 uses, `getBeauty()` = base+modifiers, no `>=N` gate), fitness/social/intelligence in RTS | flavor/reward stats that reward investment without gating content |

**Key nuance — the same stat can be one pattern in one game and another elsewhere.** Fitness is a SOFT
modifier in RTS but a BANDED capability gate in GPG. The pattern is a design CHOICE per game, not a
property of the stat. That's exactly why each game needs its rulebook written.

---

## §2 — Domain separation (the "division of labor" LO asked for)

When a game uses multiple stats meaningfully, **each gates a DIFFERENT content domain — no two gate the
same thing.** Observed mapping:
- **corruption** → lewd/explicit content tiers (the spine) + (in our design) the NPC-corruption cascade.
- **exhibitionism** → public/display content (RTS's second hard axis, parallel to corruption).
- **fitness** → physical/attractiveness/gym/sport domain (GPG bands; feeds beauty).
- **sexskill** → sexual-performance quality & options (GPG bands).
- **academic / intelligence** → school grades → jobs/career domain (Gakko academic→Graduate→corporate).
- **fame / social / charisma** → reputation & who-engages-you (Gakko fame "Nobody→Sensation"; social access).
- **beauty** → soft reward on earnings/reactions (RTS), often computed from clothing.
- **stress** (inverse) → a brake on the whole system; gates nothing positive, blocks when high.
- **energy / money** → the universal pacing (cost) + pressure (economy) pair.

This is the answer to "not the whole game depends on one trait": **distribute gates across domains** so
the spine (corruption) carries the lewd progression while other stats carry career/reputation/physical
arcs — several legs, not one rail.

---

## §3 — The dead-stat trap (the failure to avoid)

**Intelligence is declared + raised but barely gates anything in BOTH RTS and GPG:**
- RTS: 20 mentions, **0** `>=N` gates (it's set to 0, raised `+=1`, never checked as a hard gate).
- GPG: 27 mentions, **0** `<<if>>` gates; only raise/decay sites (read `+intelligence`, some acts `−`).

So even shipped games carry stats that climb but gate nothing — a visible bar that does nothing (our
skill already names this the **dead-meter** failure for NPC traits; it applies to player stats too).
**RULE:** every secondary stat must OWN a domain and gate it (by a §1 pattern), or be cut. A stat that
only climbs is decoration. (If you want a pure reward stat, make it a SOFT modifier that visibly
changes outcomes — that's not dead, it feeds something.)

---

## §4 — How stats are RAISED (the feeder principle generalizes)

Every stat has dedicated RAISE activities — the feeder economy isn't just for corruption:
- read/study → intelligence/academic; gym/sport → fitness; sex acts → sexskill; lewd/public acts →
  corruption/exhibitionism; social events → fame/social; rest/shower → lower stress.
- Leveled-tier stats (Gakko) use **exponential** costs (each level needs ~2-4× the prior) so late
  progression slows — classic RPG pacing. Banded stats (GPG) use flat thresholds.
- Inverse stats need a **restore loop** (sleep/shower lowers stress) or the game spirals (our existing
  stat-restore-infrastructure rule).

---

## §5 — RTS specifically (the north-star's actual stat policy)

Important correction to the "RTS knows how stats work" assumption: **RTS is corruption-DOMINANT and
keeps secondary stats SOFT.** Hard gates = corruption + exhibitionism (the `requirementsMC` ladder)
only. money + energy = economy + cost. beauty/fitness/social/intelligence = soft modifiers / lightly
used (beauty most, 83 uses, but COMPUTED + feeds outcomes, not a `>=N` lock; intelligence nearly dead).
So RTS does NOT model "intelligence gates this arc" — that's the **stat-portfolio games** (GPG, Gakko,
Become Someone). If our design wants real multi-stat gating, the rulebook comes from THOSE, not RTS.

---

## §6 — Implications for our progression engine (the MC-corruption cascade + multi-trait)

1. **corruption = the hard content-tier spine** (RTS Hard-content-tier pattern) — gates lewd AND the
   "corrupt yourself before you can corrupt NPCs" cascade. One spine, the backbone.
2. **Each secondary trait OWNS a domain and gates it** (§2) by a chosen §1 pattern — pick deliberately:
   banded (capability), leveled-tier (a felt ladder), inverse (a managed brake), or soft (a reward).
3. **energy = action cost** (already our `costs`); **money = pressure** (already have). Universal pair.
4. **Optional maintenance stat** (stress/hygiene) = inverse gate + restore loop (only if it earns its keep).
5. **No dead stats** (§3) — a trait without a gated domain is cut or made an explicit soft modifier.
6. **Every stat needs RAISE activities** (§4) — the feeder economy applies to ALL traits, not just corruption.

**This IS the rulebook that answers LO's worry:** when we offer a stat in the design, we also state its
pattern (§1), its domain (§2), its raise loop (§4), and confirm it's not dead (§3) — so Claude authors
to explicit rules, never "writes randomly."

---

## Open follow-ups
- Become Someone (int/str/end/charisma + dom/sub) not yet source-studied — would corroborate the
  portfolio model + add the dom/sub axis logic. Study before finalizing the menu if we keep multi-stat.
- Decide our actual stat set + each one's pattern/domain when we design the progression engine (next).
