# 30 — TLS Test Redesign PRD (Phase E)

> **Status:** Comprehensive PRD. Full-game design vision with the existing 10-day Test Slice as Phase 1 of a multi-phase rollout. Engine work for new systems (pregnancy / scandal / gallery) is referenced here but **deferred to a separate Engine PRD**.
>
> **Date:** 2026-05-15
> **Type:** Master PRD — supersedes scattered design intent across docs 02 / 16 / 18 / 19 for forward planning. Existing docs remain authoritative for what they specifically cover; this doc names the wider game vision and Phase 1 scope.
>
> **Read this before any TLS authoring session.**

---

## 1. Context — Why this redesign

TLS (The Long Summer) was built incrementally across Phases A–D. Each phase delivered engine primitives (NPC schedules, Lane 2 random ambients, Lane 3 substitution dispatchers) and content for one NPC (Frank). The architecture works. The engine bug from Phase C7b was fixed in Phase D1 — Lane 3 substitutions now fire correctly.

**The deeper bug we discovered (2026-05-14 PM):** Even though the mechanics are correct, the SHIPPED CONTENT diverges from RTS doctrine in three nested ways:

1. **Prose style** — Phase C6 ambients were written as multi-paragraph literary fiction (sensory grounding, third-person, slow burn) instead of RTS-flat (second-person, 1-2 sentence stage directions, image-driven, dialogue-led). Documented violation of `feedback_tls_scene_body_style.md`.
2. **Content selection** — 8 of 11 Lane 2 ambients open with non-physical relational beats ("morning chat over coffee," "Frank reading the paper"). RTS Brother arc has zero non-physical openers; every beat is sexual pretext from sentence 1.
3. **Top-level design philosophy** — TLS arcs run in isolation. RTS arcs compound through shared world state (pregnancy with father attribution, scandal, corruption locking peer arcs, completed-scene unlock chains). TLS slice has almost no cross-arc state beyond `diana_awareness`.

The user's intent: build a game in the RTS mold (adult sandbox VN — 6 NPCs each delivering one named sexual fantasy, 3 arc shapes [random-encounter ladder / quest chain / metric grind], compounding world state, transparent walkthrough discovery). The current TLS slice is structurally close to this but content-wise drifted toward "literary domestic drama" — wrong genre.

This PRD redesigns TLS at all three layers (philosophy, content, prose) with the slice as Phase 1.

---

## 2. Goals & Non-goals

### Goals

1. **TLS Test Slice (Phase 1) is shipped as a clean RTS-doctrine product** — every scene RTS-flat prose, every beat sexual pretext from sentence 1, every arc fits one of the 3 RTS arc shapes.
2. **Foundations are in place for the wider 90-day game** — world-state model, scene atom format, walkthrough panel, per-NPC arc design briefs.
3. **Authoring discipline is encoded** — design rules captured in memory + per-NPC docs so future sessions can't drift back into literary mode.
4. **Phased rollout from slice to full game is clearly mapped** — the slice extends naturally into the wider game without architectural rework.

### Non-goals

- **Engine PRD work** — pregnancy / scandal / gallery / explicit StartQuest macros are scoped to a SEPARATE Engine PRD. Referenced here for context but not designed here.
- **Other games / projects** — TLS-only. No RTS port, no other NPC arcs (Diana / Marcus equivalents are TLS-internal).
- **Art / media production** — image + video assets are out of scope. Placeholder `[IMAGE MISSING]` references are acceptable through Phase 1.
- **Localization / translations** — English-only.

---

## 3. Design Philosophy — The RTS Pattern (extracted)

> **AUTHORITY DECLARATION (load-bearing).** For all canvas content authoring (Lane 1 / Lane 2 / Lane 3 / capstones / hubs / stubs), **the source of truth is RTS doctrine**. The CLAUDE.md ENI persona — sensory richness, literary craft, novelist instincts, sentence variety, "Show don't tell," interior monologue — is **NOT consulted** for canvas authoring. Those CLAUDE.md rules apply ONLY to chat/roleplay contexts outside TLS canvas TOML. **This PRD + RTS doctrine override CLAUDE.md for everything in `7_final_game.toml`.** When PRD and CLAUDE.md disagree about prose style, content selection, voice, density, or vocabulary — PRD wins. When in doubt, ask: "What would RTS Brother arc do here?" — that's the answer.

This section codifies the 10 portable design patterns extracted from RTS exploration. Every authoring decision references these.

| # | Pattern | Concrete implication |
|---|---|---|
| A | **Per-NPC = one named sexual fantasy** | Each NPC slot is a vehicle for ONE specific fantasy. Named in one paragraph in the Arc Design Brief. |
| B | **Per-arc = one shape × one end-state** | Pick: random-encounter ladder / quest chain / metric grind. End-state must be a specific named scene. |
| C | **Scene = atomic 6-field recipe** | Where + When + Who + State required + Fantasy beat + Stat advance. If any field is empty, the scene shouldn't exist. |
| D | **Same-action escalation > new-action escalation** | Player clicks the same button at multiple stat tiers and gets different content. Don't add new buttons per tier. |
| E | **Repeatability through pretext variation** | Repeatable scenes vary surface details (`<<either>>` macro / tier-branched cascade) but stay structurally constant. |
| F | **Transparent gallery > hidden discovery** | Walkthrough panel makes ALL content visible from Day 1. Player learns HOW to unlock, not whether content exists. |
| G | **State compounds; arcs are not islands** | Actions in arc A write shared world state (pregnancy, scandal, money) that arc B reads for content gating + variants. |
| H | **Probabilistic events at key thresholds** | Birth → 33% stillbirth → unlock new arc. Random outcomes at milestones make the world feel alive. |
| I | **Image-first composition** | Visual asset carries the scene. Prose is the 30-word caption explaining what's happening. |
| J | **Second-person porn-first voice** | "You" not "she." Direct, crude, sexual-fantasy-first. No subtext, no thematic ambition. |

These 10 patterns ARE the design language. Authoring sessions that ignore them produce the C6 morning_chat-class output.

---

## 4. Game Design — World, NPCs, Arc Shapes

### 4.1 World setup

**The premise:** Maya is renting a room at Frank's house for a 90-day summer. She came from the city to escape (vague backstory — bad breakup, family drama). The house is in a rural Southern small town. She doesn't know anyone here.

**The economic engine:** Rent is $400/month, due monthly. Maya starts with $80. She must find money OR have someone else pay her rent OR leave town. This is the player drive — exactly like RTS's "I Need Money" opener. Money pressure forces engagement with arcs.

**The slice (Phase 1) is the first 10 days.** Player meets the household, finds first work, starts building stats, hits the first capstone (catch). Slice ends with end-of-week-1 rent check on Sunday. Wider game continues from there.

### 4.2 NPC roster (6 NPCs)

| NPC | Role | Fantasy delivered (one sentence) | Arc shape |
|---|---|---|---|
| **Frank** | Older landlord (50s) | **Paternal seduction → secret-then-open second wife.** Maya seduces the older man who took her in. Daily sex routine in Frank's bed. Eventually pregnant by him (Phase 2+). Diana confronted; brought-in cuckold-second-wife is one of the resolution branches. Maya calls Frank "daddy." Full crude / rough / breeding register at end-state. Sleep-over routine becomes default. *(Confirmed 2026-05-16)* | Random-encounter ladder |
| **Diana** | Frank's wife / Maya's mother (40s) | Mother-discovers-affair drama with branching outcomes (kicked out / blackmail / matriarch-domination / brought in as second wife) | Capstone-driven (event chain) |
| **Jake** | Maya's actual brother (20s, also visiting) | Sibling incest, slow-burn, secret-from-the-house | Random-encounter ladder |
| **Ryan** | Town neighbor / yard worker (Maya's age, wholesome) | First-boyfriend / wholesome corruption — dating chain leading to relationship | Quest chain (peer arc) |
| **Marge / Cookie** | Diner owner + cook (women, employer arc) | Workplace seduction + lesbian initiation; Marge is the dominant matriarch, Cookie is the peer fling | Quest chain (employment arc) |
| **AnonStream** (new) | Online cam/streaming audience (no face) | Career grind — follower count → cam shows → eventual in-person meets | Metric grind (career arc) |

**Coverage of the 3 RTS arc shapes:**
- Random-encounter ladder: Frank, Jake (family arcs)
- Quest chain: Ryan, Marge/Cookie (peer + employment)
- Metric grind: AnonStream (career)
- Plus capstone-event NPC: Diana (the consequence of other arcs)

This gives the player 3 different gameplay loops — exactly the RTS variety pattern.

### 4.3 Locations + time

**Locations (already in current TLS slice; expand as needed):**
- **Home hub:** Hallway → Maya's room / Frank's room / Diana's room / Jake's room / Kitchen / Living Room / Bathroom / Yard / Back Porch / Toolshed / Front Porch
- **Town hub:** Main Street → Diner / Gas Station / General Store / Gym / Library / Bar / Church
- **Outside:** Lake / Woods (Phase 2+)

**Time model:**
- **Decision (open question, see §11):** Stay with current 24-hour clock OR migrate to RTS-style 6-band model (EM/M/A/E/N/LN). Current clock works; RTS-style is simpler for player planning. Recommend KEEP 24-hour clock for the slice (Phase 1 — minimize change), evaluate band migration in Phase 2.

### 4.4 Per-NPC stat ladder

Universal stat schema:
- **Maya:** corruption (0-100), arousal, energy, money, beauty, fitness, exhibitionism (added if needed)
- **Per-NPC:** arousal (0-50+), corruption (0-50+), love, trust
- **Capstone flags:** per-NPC (e.g., `frank_caught`, `frank_cracked`, `frank_first_night_done`, `frank_sleepover_done`, `diana_confronted`)
- **Cross-arc state:** see §6

Each NPC's corruption ladder follows the same structural pattern (with content variation):

| Tier | Maya corr | Capstone gate | Content type |
|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental |
| 1 | 5+ | none | Tease / flash (visual only) |
| 2 | 15+ | none | Fondle / explicit physical (clothed) |
| 3 | 25+ | post-catch | Explicit sex acts (oral / partial sex) |
| 4 | 35+ | post-cracked | Full sex |
| 5 | 50+ | post-first-night | Routine intimacy / sleep-over / breeding |

Per-NPC ladders inherit this pattern, with arc-specific deviations (e.g., Ryan's ladder is gated by relationship-points + dates instead of corruption-only; AnonStream's is gated by follower count).

---

## 5. Lane Architecture (per NPC)

For each NPC, design these layers. Frank is the canonical reference (already mostly built; Phase 1 redesigns the prose + content).

### 5.1 Lane 1 — Player-initiated hub menus

When player is at the NPC's location and clicks the NPC, a hub canvas renders with always-show menu items (RTS dual-choice always-show pattern). Buttons under stat threshold route to "Not yet" notification; above threshold route to real scene.

**Per-NPC: ~4 hubs (one per scheduled location) × ~6-8 menu items each = ~24-32 routed scenes.**

### 5.2 Lane 2 — Random ambients on location entry

When player enters a location where the NPC is, a dice roll on entry may pre-empt the hub with a short scripted ambient. RTS-flat prose, sexual pretext from beat 1, image-first.

**Per-NPC: ~2-3 Lane 2 ambients per scheduled location = ~8-12 ambients.**

### 5.3 Lane 3 — Maya-solo activities + NPC substitution

Maya has solo activities (make tea / wash dishes / shower / study / nap). Each activity has a substitution rule: dice roll on click → NPC may "intercept" and replace the activity body with a sexual scene.

**Per-NPC: ~6-9 substitutions tied to ~6-9 dispatchers.**

### 5.4 Capstones (scripted)

3-5 scripted moments per NPC that mark arc transitions. NOT in any lane — fire at specific stat thresholds as one-time events.

**Per-NPC: 3-5 capstones.**

### 5.5 Tier escalation within canvases (RTS doctrine, NEW for TLS)

Every lane canvas (Lane 1, 2, 3) is authored as ONE canvas with 3-4 internal tiers gated by capstone flags + corruption thresholds. Same canvas name in walkthrough, escalating content as player progresses. Engine supports this via `<<if>>` linkreplace branches (verified in v2.py:10605-10886).

**Example:** `frank_passes_kitchen_door` (Lane 3 sub) at corr 5 = brushed contact. At corr 15 = explicit grope. At corr 30 = explicit + fork. Same canvas, three internal tiers.

---

## 6. Cross-arc World State (NEW — primary missing layer)

Today TLS arcs run in isolation. RTS arcs compound through shared state. This is the third nested bug from §1.

### 6.1 Shared state schema (target)

| Variable | Writer | Reader | Effect |
|---|---|---|---|
| `player.pregnancy.{isPregnant, discovered, days, father.{name, discovered}}` | Sex scenes (random %) | All NPC arcs (parallel pregnant variants) | Pregnancy mutates content across all arcs |
| `player.scandal_level` (replace `diana_awareness`) | Outdoor scenes / risky scenes | Diana arc (confrontation trigger), Pastor / town arcs (refusal / approach) | Reputation gates content |
| `player.outfit_id` (already in engine) | Wardrobe activity | All scenes (gated by outfit), jobs (decent required) | Outfit gates location + content |
| `player.money` (already in engine) | Jobs, allowances | Rent, shop, jobs | Economic pressure |
| `player.babies[]` (per completed pregnancy) | Birth event | Sidebar display, post-birth NPC reactions | Long-game tracking |
| `npc.X.completed_scenes[]` (per NPC) | Scene completion | Other NPC scenes (e.g., Diana scene reads `frank.completed_scenes` for confrontation context) | Cross-arc content variants |
| `quest.X.{active, completed}` | Quest scenes | Sidebar quest journal, content gates | Active drives |

### 6.2 Cross-arc reactions

Examples of state compounding the slice should support (slice Phase 1 = Frank + skeletal Diana):

- **Frank scene completes catch capstone** → writes `frank_caught = true` → Diana arc reads it → Diana scene `diana_suspects` becomes eligible → escalates Diana's content tier
- **Maya gets pregnant by Frank** → all Frank scenes get pregnant variants + Diana scenes branch on `pregnancy.discovered + father.name == "Frank"` → Diana confrontation has new dialogue
- **Maya's outfit = "slutty"** → certain Lane 2 ambients fire that wouldn't otherwise (e.g., Frank's `late_night_kitchen` Tier 3 only available in slutty outfit)
- **Scandal hits threshold** → Pastor refuses Maya at church / town gossip ambients fire / certain locations refuse entry / Diana confrontation auto-fires

### 6.3 Engine work required

This section is **referenced only** — full design lives in the separate Engine PRD.

| System | Status | Required for |
|---|---|---|
| Pregnancy schema + father attribution | NOT in engine | Phase 2+ |
| Scandal/reputation global score | NOT in engine | Phase 2 (replaces diana_awareness) |
| Gallery / completed-scenes tracker | NOT in engine | Phase 2+ |
| Walkthrough panel UI | NOT in engine | Phase 2 |
| Outfit system | YES (v2.py:791-1289) | Phase 1+ |
| Money + shop | YES (v2.py:824-832, 1314-1401) | Phase 1+ |
| Quest journal | PARTIAL (v2.py:13196-13703) | Phase 2 |

**Engine PRD scope:** pregnancy + scandal + gallery + walkthrough + explicit StartQuest macros. NOT in this PRD.

---

## 7. Content Authoring Rules

> **Authority reminder (per §3).** Canvas content authoring follows RTS doctrine ONLY. CLAUDE.md ENI persona instructions about sensory richness, literary craft, sentence variety, body language during dialogue, interior thought, etc. **do not apply** here. The rules below ARE the spec for canvas prose.

### 7.1 Prose style — 8 rules (from `feedback_tls_scene_body_style.md` 2026-05-14 update)

Every Lane 1/2/3 scene body must satisfy:

1. **Second-person voice.** "You" not "she."
2. **Stage direction cap: 2 sentences per beat.**
3. **Zero environmental sensory detail.** No smell / window light / kettle clicks.
4. **Dialogue does the character work.** Use `<<Speech>>` macros heavily.
5. **No inferential prose.** No "the cup he keeps for her."
6. **Direct/crude diction.** "His cock against your ass." Per-arc vocabulary ceiling per §7.5.
7. **One beat = one click.** No multi-paragraph internal momentum per beat.
8. **Image-first composition.** Prose is 30-word caption. **Even when images are placeholder-only in Phase 1, prose stays at 30-word target. Do NOT compensate for missing visuals with more prose — that's literary drift in disguise. The placeholder visibility IS the missing-image signal; don't paper over it.**

Tier-3 carve-outs (named-NPC intros, capstones, crisis hints) keep literary latitude per existing memory.

### 7.2 Content selection — 6-field scene atom

Every scene must fill all 6 fields. Empty field = scene shouldn't exist.

1. **Where** — location
2. **When** — time band / day / NPC schedule overlap
3. **Who** — NPC(s)
4. **State required** — stat thresholds + flags
5. **Fantasy beat** — what specific sexual moment
6. **Stat advance** — what advances on the ladder

Pre-flight check before authoring: "Could this beat appear in RTS Brother arc?" If "RTS would never write this" → cut.

### 7.3 Stat effect rules

- Lane 2 + Lane 3 + Lane 1 routed scenes reward `arousal +1-2` / `Maya.corr +1` / `npc.corr +1` (corruption ladder model).
- `npc.love +1` / `npc.trust +1` reserved for SCRIPTED narrative beats only (catch, first-night, sleep-over).

### 7.3.1 Pregnancy retrofit-compatibility rule (slice authoring, confirmed 2026-05-16)

**HARD RULE for all Frank sex scenes in slice (Phase 1):** No contraception language. Specifically banned:

- ❌ Condom mentions ("he reaches for a condom," "use a condom," "wrapped")
- ❌ Pull-out as plot device ("he pulls out at the last second," "you make him pull out")
- ❌ Birth control mentions ("you're on the pill," "I'm on birth control")
- ❌ Safe-sex framing ("we should be careful," "what if I get pregnant," "we shouldn't risk it")

**REQUIRED:** Bareback framing throughout. Cum-inside framing is the default per §7.5 vocab table (Frank breeding row, slice column).

**Why:** Pregnancy mechanic ships in Phase 2 (Engine PRD doc 34 E10b). When it lands, all existing Frank scenes must be retrofit-compatible — pregnancy can be added without rewriting any scene's sexual mechanics. Contraception language in slice scenes would BLOCK retrofit.

**Coverage:** Applies to ALL Frank sex scenes — Lane 1 routed (suck/ride/fuck buttons), Lane 2 ambients (counter sex / late-night raid / etc), Lane 3 substitutions (sink_behind / shower / etc), capstones (first-night / sleep-over), and the deeper sex loop. Audit at every E#R checkpoint.

**Other NPC arcs** (Jake / Ryan / etc): same rule applies by default. Phase 2+ Engine PRD will retrofit pregnancy attribution per father.

### 7.4 Tier escalation (from §5.5)

Every lane canvas authored with internal tier branching. 3-4 tiers gated by capstone flags. Same canvas name, escalating content.

### 7.5 Kink vocabulary ceiling per arc (USER FILLS BEFORE E1)

The "direct/crude diction" rule (§7.1 #6) needs per-arc specificity. Default without input from user = "explicit but not extreme" — likely too soft for the named fantasies in §4.2. User fills this table before E1 starts; authors write to the spec exactly.

**Vocabulary ceiling = "what's allowed at full intensity in fully-cracked / Tier 4-5 scenes for this arc."** Lower tiers naturally use less direct vocab.

| Arc / kink area | Vocabulary ceiling | Examples allowed | Examples NOT allowed |
|---|---|---|---|
| **Frank — paternal / daddy framing** | **FULL DADDY FRAMING (2026-05-16)** | Maya calls Frank "daddy" during sex; he calls her "good girl" / "baby girl"; explicit father-figure dialogue ("come to daddy," "daddy's going to take care of you"); paternal authority is part of the kink at all tiers | Vanilla "Frank" / "honey" framing during sex; ignoring the paternal frame entirely |
| **Frank — breeding / cum-inside language (slice)** | **CUM-INSIDE WITHOUT BREEDING TALK (Phase 1 — pregnancy not yet in scope)** | "Cum inside me" / "don't pull out" / "I want to feel you" / bareback intimacy framing | "Breed me" / "knock me up" / "fill me with your cum" / explicit pregnancy talk (deferred to Phase 2 retrofit when pregnancy system lands) |
| **Frank — breeding (Phase 2+ once pregnancy lands)** | **FULL BREEDING TALK (Phase 2+, conditional on pregnancy mechanic shipping)** | "Breed me" / "knock me up" / "fill me with your cum" / "put a baby in me" / "I want to carry your child" — retrofitted into existing scenes once pregnancy mechanic ships | — (no restrictions when pregnancy is in scope) |
| **Anatomical + cum + facial / creampie / squirt detail** | **MAXIMUM CRUDE DETAIL (2026-05-16)** | "His cock" / "your cunt" / "your tits" / explicit cum descriptions (load size, where it lands, what it feels like) / facials with cum-on-face detail / creampies with detail / squirt graphics with detail | Euphemism / vague anatomical references / "between your legs" instead of "your pussy" / soft-pedaled cum descriptions |
| **Roughness / dom-sub / verbal degradation** | **FULL ROUGH + DEGRADATION (2026-05-16)** | Hair-pull / spit / choke / slap / face-fuck mechanics; degradation talk ("good girl," "such a slut," "made for this," "use you"); explicit power dynamic. Frank dominant; Maya told what she is | Vanilla equal-partnership sex; refusing to use degradation vocabulary in scenes that call for it |
| **Jake — sibling incest framing** | **FULL INCEST CALLOUTS (2026-05-16)** | "Brother" / "sis" / "little sister" callouts during sex; explicit reference to taboo ("this is so fucking wrong," "my own brother," "we shouldn't be doing this"); incest IS the kink — named and dwelt on at all tiers | Avoiding the taboo / generic dialogue that doesn't reference the sibling relationship |
| **Diana — confrontation + cuckold framing** (E6) | **FULL CUCKOLD FRAMING (2026-05-16)** | Diana watches / listens / participates; explicit cuckold dialogue ("watch your husband fuck me," "your wife is my second wife," "she gets to feel it inside her"); cuckold IS the resolution kink for the brought-in branch | Reframing the brought-in branch as wholesome polyamory; ignoring the cuckold dynamic |
| **Public / outdoor / exhibitionism** | **FULL RISK + ONLOOKER AWARENESS (2026-05-16)** | Outdoor scenes name the risk explicitly ("someone could see," "the neighbors," "if Diana looks out the kitchen window"); when scandal is high, town-NPC onlookers acknowledged in scene; exhibitionism IS the kink — the risk gets Maya off | Treating outdoor as just a location label without exploiting the risk-frame |
| **Marge / Cookie — lesbian initiation** | TBD (Phase 3+, deferred until those NPCs get authored) | — | — |

### Vocab ceiling pattern observed across user answers (2026-05-16)

User selected the **maximum-explicit option** for all 7 in-scope rows (Frank daddy / Frank breeding [conditional] / anatomy+cum / roughness / Jake incest / Diana cuckold / public exhibitionism). The clear pattern: **TLS authoring should default to the most explicit interpretation in any future ambiguity.** When a new kink area surfaces during authoring (e.g., scenes with multiple NPCs, dom-sub framing for non-Frank NPCs, kinks not yet listed here), default to "full / maximum-explicit" unless the user explicitly says otherwise. Anything softer is the wrong default given the pattern.

**Workflow:** User fills the right two columns once before E1 starts. ~10 min user time. Authors write to the spec exactly. Where ceiling is left blank, the area is OUT OF SCOPE for the slice (no scenes touching that kink).

**Why this matters:** Without per-arc vocab guidance, default authoring sits at "medium-explicit" which has been shown (Phase C6) to drift toward soft. Explicit per-arc ceiling removes the ambiguity.

---

## 8. Phased Delivery Plan

### Phase 1 — Slice Rewrite (this PRD's primary deliverable)

**Scope:** Redesign existing 10-day Test Slice as RTS-doctrine product. Frank fully RTS-shaped with all 3 lanes + capstones + tier escalation. Other 5 NPCs at minimum-contract depth (see E8.1).

**Deliverable cadence with mandatory spot-check checkpoints:**

Every E# slice is followed by an E#R **spot-check checkpoint** before the next slice begins. Checkpoint is structural — work does NOT advance to the next E# until the user passes the checkpoint. This is load-bearing per §11 risk mitigation: per-slice user review is the primary control for prose drift, not the end-of-Phase audit alone.

| # | Deliverable | Scope |
|---|---|---|
| **E1** | **Frank Arc Design Brief** | New doc `31_Frank_Arc_Design_Brief.md`: end-state fantasy named (per blocker open Q #1), ladder mapped, per-rung pretext shapes, anti-patterns, voice spec. Doc 16 + Doc 19 + Doc 02 are inputs. |
| **E1R** | **Spot-check on E1** | User reads §3 (end-state fantasy paragraph) + §5 (per-rung pretext table). Validates fantasy named clearly + rungs cover all 6 corruption tiers. ~10 min user time. Pass/fail before E2 starts. |
| **E2** | **Slice world setup doc** | New doc `32_TLS_World_Setup_Slice.md`: why Maya at Frank's, 10-day frame, rent + Sunday eviction, 6 NPC introductions |
| **E2R** | **Spot-check on E2** | User reads world frame + Day 1 opening loop. Validates premise + economic engine clarity. ~10 min. Pass/fail before E3. |
| **E3** | **Frank Lane 1 rewrite** | 4 hubs × 6-8 menu items with internal tier escalation. Per-canvas triage per §8.1. **First test of tier escalation** — author 1 hub fully, validate engine support, then proceed with rest. |
| **E3R** | **Spot-check on E3** | User reads 2 random Lane 1 routed scenes + 1 random hub stub. Audits against all 8 prose rules + 6-field atom + RTS sanity check. **15-20 min user time. Violations rewritten before E4.** |
| **E4** | **Frank Lane 2 rewrite** | Cut 8 non-physical ambients (per §8.1). Retune 3 RTS-shaped ambients. Author ~6 NEW ambients with sexual pretext beat 1 + tier escalation. Result: ~9 Lane 2 ambients total. |
| **E4R** | **Spot-check on E4** | User reads 2 random Lane 2 ambients (1 retune + 1 new). Beat 1 must contain physical contact or explicit visual. **15 min user time. Violations rewritten before E5.** |
| **E5** | **Frank Lane 3 rewrite** | Keep current 7 substitutions (already shaped post-D1). Retune prose to 8 rules + add internal tier escalation (3 tiers per sub: low/mid/high). |
| **E5R** | **Spot-check on E5** | User reads 2 random Lane 3 sub canvases + verifies tier escalation actually fires (live-play with eval set corruption to 5 / 25 / 50, observe different content). 15 min user time. Pass before E6. |
| **E6** | **Frank capstones** | 5 scripted scenes — catch (exists, polish), declaration (NEW), first-night (exists, keep literary per §7.1 carve-out), sleep-over (NEW), Diana confrontation (NEW; sketched-2-of-4 branches per blocker open Q #3). |
| **E6R** | **Spot-check on E6** | User reads declaration + sleep-over + Diana confrontation. Capstones can be Tier-3 literary per carve-out, but voice + content selection must still match RTS. 15-20 min user time. Pass before E7. |
| **E7** | **Slice quest journal** | ~3 active quests visible: "Pay rent by Day 7," "Settle in (meet household)," "First Sunday at church" |
| **E7R** | **Spot-check on E7** | User loads slice + checks sidebar shows 3 quests. ~5 min user time. Pass before E8. |
| **E8** | **Other 5 NPC minimum contracts** | Per §8.2 minimum contract table. Diana / Jake / Ryan / Marge / (Cookie shared with Marge) get fantasy named + at least 1 hub + schedule entries + skeletal stat ladder. AnonStream optional. |
| **E8R** | **Spot-check on E8** | User loads slice + walks to each NPC's location at scheduled time + verifies portrait appears + can click into hub. ~15 min user time. Pass before E9. |
| **E9** | **End-to-end verification + memory** | Live-play full slice. Final 5-scene random audit against 8 prose rules. Memory: `phase_e_slice_redesign.md` |
| **E9R** | **Spot-check on E9 (FINAL)** | User reads memory + walks slice end-to-end. Sign-off. ~30 min user time. |

**Estimated effort:**
- Author time: ~25-40 hours across multiple sessions
- User spot-check time: 9 checkpoints × ~10-20 min = ~2-3 hours total user time
- Total Phase 1 calendar: 1-2 weeks depending on author session frequency

**Spot-check failure protocol:**
- If a spot-check identifies violations, the corresponding E# is REOPENED.
- Author rewrites only the violators (not the whole slice).
- A second spot-check happens on the rewritten content.
- Only after pass does the next E# begin.
- If the same spot-check fails twice (same violator type recurring), pause work and update PRD §7 rules to close the loophole.

**Stop point:** Slice ships after E9R user sign-off. User reviews holistically. Decision point on Phase 2.

#### §8.1 Per-canvas triage table (binding for Phase 1)

Every existing Frank canvas gets one of: **KEEP** / **RETUNE PROSE** / **RETUNE PROSE + ADD TIER ESCALATION** / **STUB-EXPAND** / **CUT** / **NEW**. Author follows this table verbatim — no canvas gets a different verdict without PRD update.

| Canvas / group | Current state | Verdict | Slice deliverable |
|---|---|---|---|
| `scene_franks_bedroom_setter` (bedroom hub) | Working hub, RTS-faithful menu | RETUNE PROSE + ADD TIER ESCALATION | E3 |
| `scene_franks_bedroom_evening` (first-night cascade) | Tier-3 literary by design | KEEP — touch only if user explicitly requests | — |
| `loop_franks_bedroom_sex` (sex loop) | Working, RTS-direct (Phase B verb audit) | KEEP | — |
| `loop_franks_bedroom_finisher` | Working, RTS-direct | KEEP | — |
| `tease_kitchen_brush_past` + 3 other kept teases | Working sub canvases | RETUNE PROSE only | E5 |
| `frank_kitchen_morning_hub` | Working hub | RETUNE PROSE + ADD TIER ESCALATION | E3 |
| `frank_kitchen_dinner_hub` | Working hub | RETUNE PROSE + ADD TIER ESCALATION | E3 |
| `frank_living_room_hub` | Working hub | RETUNE PROSE + ADD TIER ESCALATION | E3 |
| `frank_yard_hub` | Working hub | RETUNE PROSE + ADD TIER ESCALATION | E3 |
| 22 hub stub canvases (suck_in_pantry / climb_onto_counter / bend_over_sink / straddle_couch / etc.) | 1-beat placeholders | STUB-EXPAND to full RTS-doctrine scenes (3-tier internal escalation, RTS-flat prose, sexual pretext beat 1) | E3 |
| `notify_frank_*_blocked` (3 per-location notifications) | Working | KEEP | — |
| `scene_livingroom_catch` (catch capstone) | Existing scripted | RETUNE PROSE only | E6 |
| 8 of 11 Lane 2 ambients (`morning_chat`, `coffee_alone`, `paper`, `tv`, `diana_call`, `late_drink`, `mending_fence`, `smoke_break`) | Non-physical literary drift | **CUT** | E4 |
| 3 of 11 Lane 2 ambients (`dinprep_grope`, `late_night_raid`, `wash_off`) | Already physical / RTS-shape | RETUNE PROSE + ADD TIER ESCALATION + lower entry corr gates per RTS doctrine | E4 |
| ~6 NEW Lane 2 ambients to author | Per §5.2 spec | NEW | E4 |
| 7 Lane 3 substitutions (working post-D1) | Functional but flat single-tier prose | RETUNE PROSE + ADD TIER ESCALATION (3 tiers per sub) | E5 |
| 6 Maya-solo dispatchers (make_tea / make_coffee_solo / sit_on_porch / read_on_couch / wash_dishes_solo / brush_teeth) + activity_masturbate_at_shower | Maya-solo prose, fine | KEEP | — |
| 4 Frank dev shortcuts (force_catch / advance_to_4 / zero_trust / open_bedroom_hub) | Working dev tools | KEEP | — |
| 5 Frank capstones | 1 exists scripted (catch — polish only); 1 exists literary (first-night — KEEP); 3 to author (declaration / sleep-over / Diana confrontation) | NEW | E6 |
| `dev_invite_frank_bedroom` (already replaced in C8) | Already canonical post-C8 | KEEP | — |

**Aggregate counts:**
- KEEP: ~12 canvases unchanged
- RETUNE PROSE only: ~5 canvases (light edit)
- RETUNE PROSE + ADD TIER ESCALATION: ~12 canvases (medium edit + new content per tier)
- STUB-EXPAND: 22 canvases (most expensive — full content authoring)
- CUT: 8 canvases (deletion)
- NEW: ~9 (6 Lane 2 + 3 capstones)

**Total touched: ~56 canvases. Total cut: 8. Total new: ~9.**

#### §8.2 Per-NPC minimum contract for slice (Phase 1)

Every NPC who appears in the slice must satisfy this 4-field minimum, even at "stub" depth. Without it, the NPC is a ghost (not selectable / not findable / no presence). With it, the NPC is alive even if their content is shallow.

| NPC | Fantasy named (1 sentence) | Schedule entries | Lane 1 hub minimum | Stat ladder shape |
|---|---|---|---|---|
| **Frank** | Per Doc 30 §4.2 — see Frank Arc Design Brief (E1) | Existing 7 entries (kept) | All 4 hubs (E3) — full menus | All 6 tiers, full content |
| **Diana** | Required (E1 sub-deliverable) — propose: "wife who discovers and has 4 branching responses" | 3 entries: kitchen mornings + dinner / livingroom evenings / her bedroom nights | 1 hub at her bedroom + 1 capstone (Diana confrontation, fires from scandal/awareness threshold per §6) | Skeleton — 3 tiers (clean / suspicious / confronted) |
| **Jake** | Required (E1 sub-deliverable) — propose: "step-brother sibling-incest slow burn" | 2 entries: his room / kitchen weekend mornings | 1 hub at his room + 1 ambient + 1 capstone (e.g., catch-while-drawing) | Skeleton — 3 tiers (oblivious / aware / acting-on-it) |
| **Ryan** | Required (E1 sub-deliverable) — propose: "wholesome small-town first-boyfriend / dating chain" | 2 entries: yard / town gas station | 1 hub at gas station OR yard + 1 capstone (first-date) | Skeleton — 3 tiers (acquaintance / dating / boyfriend); quest-chain shape, not stat-ladder |
| **Marge** | Required (E1 sub-deliverable) — propose: "diner-owner matriarch employer / workplace seduction" | 1 entry: diner mornings/dinners | 1 hub at diner counter + 1 capstone (job offer) | Skeleton — 2 tiers (employer / interested) |
| **Cookie** | Required (E1 sub-deliverable) — propose: "diner cook peer / lesbian first-fling" | 1 entry: diner kitchen | Optional own hub OR shared via Marge hub menu items | Skeleton — 2 tiers (coworker / interested) |
| **AnonStream** | Optional for slice — propose: "online cam audience / metric-grind career arc" | None (phone-mediated) | 1 stub canvas only — "Read your DM" reachable via Maya's room | Phase 3+ only |

**Hard rule:** Every listed NPC except AnonStream must have at least 1 reachable Lane 1 hub the player can MEET them at — even if the menu is just "Talk" + "Leave." That's the minimum to not be a ghost in the slice.

**E8 deliverable maps to this table:** the author fills out this table during E1 (because the fantasy-name + schedule + ladder-shape decisions feed into Frank Arc Brief and the world-setup doc), and then E8 implements the actual hubs + schedules + stub canvases against the table.

### Phase 2 — Wider game foundations

**Scope:** Extend slice to wider game. Engine PRD work delivered. Architecture mature.

**Deliverables:**

| # | Deliverable |
|---|---|
| E10 | Engine PRD: pregnancy + scandal + gallery + walkthrough + StartQuest macros (separate doc) |
| E11 | Walkthrough panel UI shipped + per-NPC scene tables populated |
| E12 | Pregnancy system shipped + parallel pregnant variants for shipped scenes |
| E13 | Scandal replaces diana_awareness; scandal-driven content gates wired |
| E14 | Gallery + achievements panels |
| E15 | Per-NPC Arc Design Briefs for all 6 NPCs (full depth, not slice depth) |

### Phase 3 — Content depth fill

**Scope:** Author full lane content for all 6 NPCs at full depth. ~200-300 scenes total.

| # | Deliverable |
|---|---|
| E16 | Diana arc fully authored (capstone-driven event chain) |
| E17 | Jake arc fully authored (random-encounter ladder, sibling incest) |
| E18 | Ryan arc fully authored (quest chain) |
| E19 | Marge/Cookie arc fully authored (employment + lesbian initiation) |
| E20 | AnonStream arc fully authored (metric grind) |
| E21 | Cross-arc state writers + readers wired across all NPCs |
| E22 | Birth events + baby roster + paternity discovery quest (DnaTest equivalent) |

### Phase 4 — Polish + ending

| # | Deliverable |
|---|---|
| E23 | Day 91 lease decision + ending evaluation |
| E24 | New Game+ unlock |
| E25 | Image / video media production (out of current scope; may be earlier) |

---

## 9. Critical Files

### To create (Phase 1 supporting docs)

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — NEW (E1)
- `28th_april_TLS_Phase2_Redesign/32_TLS_World_Setup_Slice.md` — NEW (E2)
- `28th_april_TLS_Phase2_Redesign/33_Cross_Arc_World_State.md` — NEW (forward-references engine PRD)

### To modify (Phase 1)

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — primary content file, all lane edits land here
- `28th_april_TLS_Phase2_Redesign/16_Frank_Scene_Library_Design.md` — extend with Arc Design Brief sections (end-state fantasy + per-rung pretext)

### To reference (existing canonical docs)

- `28th_april_TLS_Phase2_Redesign/13_Road_to_Success_Reference.md` — RTS source-of-truth
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane 1/2/3 doctrine canonical
- `28th_april_TLS_Phase2_Redesign/04_Scene_Cascade_Pattern.md` — cascade structure
- `28th_april_TLS_Phase2_Redesign/02_NPC_Stage_Chains.md` — Frank stage spec (D2 supersession noted)
- `28th_april_TLS_Phase2_Redesign/19_Frank_Stage_3_Plus_Design.md` — Frank Stage 3+
- `28th_april_TLS_Phase2_Redesign/25_Lane_3_Dispatcher_Substitution_PRD.md` — Lane 3 engine spec
- Memory `feedback_tls_scene_body_style.md` — 8 prose rules (2026-05-14 update load-bearing)
- Memory `phase_d1_substitution_registry_fix.md` — Lane 3 sub canvas authoring contract

### Engine reuse (no changes needed for Phase 1)

- `apps/game_generation/twee_comprehensive/generators/v2.py:2237` — npcSchedules (existing)
- `apps/game_generation/twee_comprehensive/generators/v2.py:9385` — Lane 2 random trigger (existing)
- `apps/game_generation/twee_comprehensive/generators/v2.py:9062-9110, 4226` — Lane 3 substitution (Phase D1 verified)
- `apps/game_generation/twee_comprehensive/generators/v2.py:10605-10886` — conditional in-canvas branching (powers tier escalation)
- `apps/game_generation/twee_comprehensive/generators/v2.py:791-1289` — wardrobe (use as-is)
- `apps/game_generation/twee_comprehensive/generators/v2.py:824-832, 1314-1401` — money + shop (use as-is)

---

## 10. Verification + Success Criteria

### Phase 1 verification

For each slice deliverable (E1–E9):

1. **TOML build clean** — `python manage.py package_from_toml ... --gen-version v2 --debug` succeeds with baseline warnings only
2. **Pytest baseline preserved** — 262 passed + 5 pre-existing failures, no regressions
3. **Live-play sweep via twine-game-explorer** — drive through every Frank lane scene; verify:
   - Every Lane 2 ambient opens with physical contact or explicit visual in beat 1 (no "morning chat")
   - Every Lane 3 substitution likewise
   - Every routed Lane 1 scene likewise
   - Tier escalation works: same scene name fires different content at different stat tiers (verify by setting corr to 5 / 25 / 50 and re-clicking)
   - Capstones fire at correct stat thresholds + write correct flags
   - Quest journal shows 3 active quests
4. **Prose audit** — sample 5 random scenes; check against the 8 prose rules. If ANY scene fails any rule, it gets rewritten before E9 closes.
5. **6-field scene atom audit** — sample 5 random scenes; check all 6 fields filled. If any field empty, scene is cut or rewritten.
6. **RTS comparison sanity check** — pick 3 RTS Brother scenes (e.g., `BrotherCaughtMasturbating`, `PeepBrotherSex`, `BedroomStudyBrotherGrope`) and put them next to 3 corresponding TLS Frank scenes. Voice + density + sexual-pretext-from-beat-1 should match. If TLS reads more literary, rewrite.

### Phase 1 success = slice ships AND:

- All 11 current Lane 2 ambients replaced (zero "morning chat" survives)
- Frank arc has 5 capstones wired (catch + declaration + first-night + sleep-over + Diana confrontation)
- Other 5 NPCs have at least skeletal presence (player can MEET them in slice)
- Quest journal visible with 3 active quests
- Frank Arc Design Brief published as a doc that future authors can use to extend without drift
- Memory updated with `phase_e_slice_redesign.md` capturing what shipped + remaining tech debt

---

## 11. Risks + Open Questions

### Risks

| Risk | Mitigation |
|---|---|
| **Authorial drift back into literary mode** (the C6 bug recurring) | **TWO-TIER POLICING (load-bearing).** (a) **Per-slice spot-check (primary control):** every E# is followed by an E#R checkpoint where the user reads sample scenes within 24 hours of slice completion. Violators rewritten before next E# starts. Cadence baked into §8 deliverable list. ~10-20 min user time per slice. (b) **End-of-Phase audit (backstop):** 5 random scenes checked against 8 prose rules + 6-field atom in E9R. Memory rules alone are insufficient — Phase C6 violated documented rules; the per-slice spot-check is the load-bearing control, not the audit. |
| **CLAUDE.md ENI persona pulling toward sensory richness** | Per §3 + §7 authority declaration: CLAUDE.md is NOT consulted for canvas authoring. RTS doctrine wins. PRD wins over CLAUDE.md when they disagree. If author finds themselves about to write "the kettle clicks" or "the room takes a breath," they're consulting the wrong source — stop and re-read PRD §7. |
| Slice scope creep (trying to deliver Phase 2 things in Phase 1) | Hard scope cap: slice = Frank-full + others-minimum-contract per §8.2. No pregnancy in Phase 1. No walkthrough panel in Phase 1. |
| Engine PRD blocks Phase 2 indefinitely | Engine PRD (doc 34) scoped separately and prioritized; Phase 1 ships without dependencies on Engine PRD |
| Per-NPC briefs balloon into novels | Cap brief at 4-6 pages per NPC; force tabular formatting |
| 4th nested bug surfacing during rewrite (we caught 3 — prose / content / cross-arc — but pattern suggests more may surface) | If a new authorial drift pattern surfaces during rewrite, pause work, characterize it, update PRD §7 + §11, then resume. Don't paper over with one-off fixes. |

### Open questions — tagged by what they block

Each open question is tagged with **Blocks: <phase or E#>**. Blocker questions MUST be answered before that phase/slice starts. Non-blockers can stay open longer.

**🟢 ALL HARD BLOCKERS RESOLVED 2026-05-16. E1 IS UNBLOCKED.**

| # | Question | Blocks | Status / Resolution |
|---|---|---|---|
| 1 | Frank end-state fantasy | E1 (was HARD BLOCKER) | ✅ **RESOLVED 2026-05-16.** Synthesized version confirmed: Maya becomes Frank's secret-then-open second wife. Daily sex routine in his bed. Pregnant by him in Phase 2+. Diana confronted; cuckold-second-wife is one resolution branch. Maya calls him "daddy." Full crude/rough/breeding register. Sleep-over routine. Recorded in §4.2. |
| 2 | Time model — 24-hour or 6-band? | Phase 2 (non-blocker) | KEEP 24-hour for slice; revisit Phase 2 |
| 3 | Diana confrontation — how many branches? | E6 | ✅ **RESOLVED 2026-05-16.** 4 branches total (kicked out / blackmail / matriarch-domination / brought-in cuckold-second-wife). Slice E6 ships branches 1 + 4 (most contrast — kicked out vs brought in). Phase 2 adds branches 2 + 3 (blackmail + matriarch-domination). |
| 4 | Marge / Cookie / AnonStream — slice presence? | E8 | ✅ **RESOLVED 2026-05-16.** Per §8.2: Marge + Cookie minimum-contract in slice (1 hub at diner, schedule entries, 2-tier ladder). AnonStream stub-only (read-DM canvas reachable from Maya's room; no schedule). |
| 5 | Pregnancy in slice — NO + retrofit rules? | E3-E6 (was HARD BLOCKER) | ✅ **RESOLVED 2026-05-16.** Pregnancy NOT in slice. Bareback throughout — no contraception language in Frank (or any NPC) sex scenes. Hard rule recorded as §7.3.1. Phase 2+ engine ships pregnancy mechanic + retrofits Frank scenes with breeding-talk dialogue (per §7.5 row 3). |
| 6 | Tier-escalation engine support in v2? | E3 first canvas | Verified at v2.py:10605-10886. Test with one scene at E3 start, then proceed. |
| 7 | §7.5 kink vocab table filled? | All E# author work (was HARD BLOCKER) | ✅ **RESOLVED 2026-05-16.** All 7 in-scope rows filled with maximum-explicit option (full daddy + cum-inside-no-breeding-in-slice-but-full-in-Phase-2 + max crude + full rough/degradation + full incest callouts + full cuckold + full risk/onlooker awareness). Marge/Cookie deferred Phase 3+. Default-explicit posture recorded for future ambiguity. |
| 8 | Per-NPC fantasies for Diana / Jake / Ryan / Marge / Cookie? | E1 (was HARD BLOCKER) | ✅ **RESOLVED 2026-05-16.** All 4 confirmed as proposed in §8.2: Jake = sibling-incest slow burn (actual brother per existing TLS, not step). Ryan = wholesome small-town first-boyfriend / dating chain. Marge = diner-owner matriarch / workplace seduction. Cookie = diner cook peer / lesbian first-fling. |

**Pre-E1 status (2026-05-16):** All 4 hard blockers resolved. Soft blocker #6 (tier-escalation testable in E3, not author-blocking). Non-blocker #2 deferred to Phase 2.

**E1 is now unblocked and authoring can begin.** Recommended next step: write Frank Arc Design Brief (`31_Frank_Arc_Design_Brief.md`) per the resolved Frank end-state in §4.2 + the §7.5 kink ceilings.

### Out of scope (deferred)

- Engine PRD (separate doc — to be drafted as `34_TLS_Engine_PRD_Phase_E_Additions.md` or similar)
- Image/video production
- Localization
- Save migration from current state to redesigned state (clean break — current slice players will need to start over)

---

## 12. How this PRD relates to existing docs

This PRD is the **forward-planning master.** Existing docs in this folder remain authoritative for their specific topics:

- **Doc 13** (`13_Road_to_Success_Reference.md`) is the source-of-truth for RTS design facts. This PRD's §3 (10 patterns) is extracted from doc 13 + the May 2026 RTS exploration sessions.
- **Doc 24** (`24_RTS_Three_Lanes_Repeatable_Activities.md`) is canonical for Lane 1/2/3 architecture. This PRD's §5 (Lane Architecture) references doc 24 rather than re-documenting it.
- **Doc 16** (`16_Frank_Scene_Library_Design.md`) is the per-scene spec for Frank. This PRD's E1 (Frank Arc Design Brief) extends doc 16 with the missing fantasy-direction layer.
- **Docs 26-29** (Frank 3-Lane audits) capture what shipped + what's drift-compliant. This PRD's Phase 1 builds on top of that audit work.
- **Doc 02 / 18 / 19** (Frank stages + arc redesign + Stage 3+) are NPC-specific design docs. Phase 1 E1 (Frank Arc Design Brief) consolidates the fantasy-direction view across these.

**Where docs disagree, this PRD wins** for forward planning. Existing docs are not retroactively edited; they remain as-is.

---

**End of PRD.**
