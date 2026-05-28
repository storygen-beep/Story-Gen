# Doctrine 08 — Per-Arc Kink Vocabulary Ceilings

**Source:** Doc 30 §7.5 (verbatim) + 2026-05-16 LO answer pattern.
**Authority:** Doctrine. Per-arc-NPC vocabulary register cap. Authored at brief-time (R7 §2), enforced at canvas-authoring-time.
**Purpose:** Name what each arc/kink area is allowed to escalate to at full intensity. Without per-arc ceiling, default authoring sits at "medium-explicit" which has been shown (Phase C6) to drift toward soft.

This file completes the forward-reference from `doctrine/01_rts_principles.md` P9 (per-arc vocabulary ceiling) and `doctrine/05_rts_flat_prose.md` §2 Rule 6 (direct/crude diction per per-arc vocab ceiling).

---

## §1 — Why ceilings matter

P9 (`doctrine/01_rts_principles.md`): each NPC's content declares its kink ceiling upfront. Frank goes full explicit. Marcus stays school/peer. **Don't force one register across the cast.**

The "direct/crude diction" rule (`doctrine/05_rts_flat_prose.md` §2 Rule 6) needs per-arc specificity. **Without per-arc vocab guidance, default authoring sits at "medium-explicit"** which:

- Drifts toward soft per the C6 failure mode (Phase C6 morning-chat-class output)
- Doesn't deliver the named fantasy in §1 of the NPC brief
- Reads as wholesome-vanilla even when the design book proposes full incest / cuckold / breeding

**Vocabulary ceiling = "what's allowed at full intensity in fully-cracked / Tier 4–5 scenes for this arc."** Lower tiers naturally use less direct vocab.

**Authored at:** R7 brief §2 (NPC voice spec) + §3 (per-tier register column). The ceiling is a brief-time declaration, not a per-canvas decision.

---

## §2 — The vocab ceiling table (Doc 30 §7.5 verbatim)

The canonical table. Each row pairs a kink area to its full-intensity ceiling + examples allowed + examples NOT allowed. **All 7 in-scope rows (2026-05-16 LO answers) came back maximum-explicit per §3 below.**

| Arc / kink area | Vocabulary ceiling | Examples allowed | Examples NOT allowed |
|---|---|---|---|
| **Frank — paternal / daddy framing** | **FULL DADDY FRAMING (2026-05-16)** | Maya calls Frank "daddy" during sex; he calls her "good girl" / "baby girl"; explicit father-figure dialogue ("come to daddy," "daddy's going to take care of you"); paternal authority is part of the kink at all tiers | Vanilla "Frank" / "honey" framing during sex; ignoring the paternal frame entirely |
| **Frank — breeding / cum-inside language (slice — Phase 1)** | **CUM-INSIDE WITHOUT BREEDING TALK (Phase 1 — pregnancy not yet in scope)** | "Cum inside me" / "don't pull out" / "I want to feel you" / bareback intimacy framing | "Breed me" / "knock me up" / "fill me with your cum" / explicit pregnancy talk (deferred to Phase 2 retrofit when pregnancy system lands) |
| **Frank — breeding (Phase 2+ once pregnancy lands)** | **FULL BREEDING TALK (Phase 2+, conditional on pregnancy mechanic shipping)** | "Breed me" / "knock me up" / "fill me with your cum" / "put a baby in me" / "I want to carry your child" — retrofitted into existing scenes once pregnancy mechanic ships | — (no restrictions when pregnancy is in scope) |
| **Anatomical + cum + facial / creampie / squirt detail** | **MAXIMUM CRUDE DETAIL (2026-05-16)** | "His cock" / "your cunt" / "your tits" / explicit cum descriptions (load size, where it lands, what it feels like) / facials with cum-on-face detail / creampies with detail / squirt graphics with detail | Euphemism / vague anatomical references / "between your legs" instead of "your pussy" / soft-pedaled cum descriptions |
| **Roughness / dom-sub / verbal degradation** | **FULL ROUGH + DEGRADATION (2026-05-16)** | Hair-pull / spit / choke / slap / face-fuck mechanics; degradation talk ("good girl," "such a slut," "made for this," "use you"); explicit power dynamic. Frank dominant; Maya told what she is | Vanilla equal-partnership sex; refusing to use degradation vocabulary in scenes that call for it |
| **Jake — sibling incest framing** | **FULL INCEST CALLOUTS (2026-05-16)** | "Brother" / "sis" / "little sister" callouts during sex; explicit reference to taboo ("this is so fucking wrong," "my own brother," "we shouldn't be doing this"); incest IS the kink — named and dwelt on at all tiers | Avoiding the taboo / generic dialogue that doesn't reference the sibling relationship |
| **Diana — confrontation + cuckold framing** (E6) | **FULL CUCKOLD FRAMING (2026-05-16)** | Diana watches / listens / participates; explicit cuckold dialogue ("watch your husband fuck me," "your wife is my second wife," "she gets to feel it inside her"); cuckold IS the resolution kink for the brought-in branch | Reframing the brought-in branch as wholesome polyamory; ignoring the cuckold dynamic |
| **Public / outdoor / exhibitionism** | **FULL RISK + ONLOOKER AWARENESS (2026-05-16)** | Outdoor scenes name the risk explicitly ("someone could see," "the neighbors," "if Diana looks out the kitchen window"); when scandal is high, town-NPC onlookers acknowledged in scene; exhibitionism IS the kink — the risk gets Maya off | Treating outdoor as just a location label without exploiting the risk-frame |
| **Marge / Cookie — lesbian initiation** | TBD (Phase 3+, deferred until those NPCs get authored) | — | — |

---

## §3 — The 2026-05-16 LO pattern (default to maximum-explicit)

User selected the **maximum-explicit option** for all 7 in-scope rows (Frank daddy / Frank breeding [conditional] / anatomy+cum / roughness / Jake incest / Diana cuckold / public exhibitionism). The clear pattern:

> **TLS authoring should default to the most explicit interpretation in any future ambiguity.**

**Application:** when a new kink area surfaces during authoring (e.g., scenes with multiple NPCs, dom-sub framing for non-Frank NPCs, kinks not yet listed here), default to "full / maximum-explicit" unless the user explicitly says otherwise. **Anything softer is the wrong default given the pattern.**

Concrete examples:
- New NPC arc proposed with "tender father-figure" register → default to FULL DADDY (per Frank precedent), not softer "warm older man"
- New scene with creampie + breeding → default to FULL BREEDING TALK if pregnancy mechanic is live, not softer "intimacy framing"
- New cuckold scene with secondary witness → default to FULL CUCKOLD (per Diana precedent), not wholesome polyamory
- Public exposure scene → default to FULL RISK + ONLOOKER AWARENESS, not "scenic outdoor location"

---

## §4 — Per-arc-ceiling authoring workflow

### §4.1 — Brief-time declaration (R7 §2 + §3)

In the NPC's R7 brief, the ceiling is declared in two places:

**§2 Voice spec — NPC-specific framing rules:**

```markdown
### <NPC>-specific framing rules (per Doc 30 §7.5 row <X>)

- **<Vocab register name>** starts from **Stage <N>** when context turns sexual
- At **Stage <N+1>** the <register> is DEFAULT in all sex scenes — not occasional, baseline
- Pre-Stage <N>: NO <register> — <NPC> is still <pre-stage role>, voice is <register-pre>
- Stage <N+1> examples: "<example 1>" / "<example 2>" / "<example 3>"
```

**§3 Stat ladder — daddy/incest/cuckold register column:**

| Tier | Maya corr | Capstone gate | Content type | Pretext shape category | **<Vocab register>?** | Cross-arc awareness write |
|---|---|---|---|---|---|---|
| 0 | 0+ | none | Brushed contact | — | No | — |
| 3 | 25+ | post-catch | Explicit oral / partial sex | — | Yes — Maya may use "<register-term>" | — |
| 4 | 35+ | post-cracked | Full sex | — | Yes — Maya routinely / NPC starts "<register-term>" | — |
| 5 | 50+ | post-first-night | Routine / sleep-over | — | Yes — DEFAULT register | — |

### §4.2 — Canvas-authoring-time enforcement

When writing scene prose for a Tier 4+ canvas, the ceiling drives diction:

**Frank Tier 4 scene example (FULL DADDY register active):**

```
[Maya] "Yes daddy."
[Frank] "Good girl. Open."
You go down on your knees. He's already hard, jeans open at the belt.
[Frank] "Take it. All of it."
```

vs **Frank Tier 4 wrong (ENI persona drift, soft register):**

```
[Frank] "Come here, sweetheart."
You feel yourself responding to him, drawn closer almost involuntarily.
[Maya] "Frank..."
He kisses you, and time seems to slow.
```

The wrong version violates the per-arc ceiling: "honey/sweetheart" instead of "good girl/baby girl"; vague body-response instead of explicit anatomical; named "Frank" instead of "daddy"; literary cadence ("time seems to slow") instead of imperative direct.

### §4.3 — Tier-by-tier escalation within the ceiling

The ceiling is the MAXIMUM at full intensity (Tier 4–5). Lower tiers escalate toward it:

| Tier | Frank daddy register | Frank breeding language |
|---|---|---|
| 0 (corr 0+) | None | None |
| 1 (corr 5+) | None | None |
| 2 (corr 15+) | None | None |
| 3 (corr 25+) | Maya MAY use "daddy" | "Cum inside me" emerges |
| 4 (corr 35+) | Maya routinely uses "daddy" / Frank starts "good girl" | "Don't pull out" / "I want to feel you" |
| 5 (corr 50+) | DEFAULT register | "Cum inside me" baseline + Phase 2+: full breeding talk |

The escalation isn't tier-linear (Tier 0 = 0% / Tier 5 = 100%). It's tier-gated — daddy register doesn't appear at all until Stage 3, then steps up at Stage 4, then becomes default at Stage 5. Pre-Stage 3 sex (if it exists) uses softer register; post-Stage 3 sex uses full register.

### §4.4 — Out-of-scope ceiling areas (blank rows)

**Marge / Cookie — lesbian initiation = TBD (Phase 3+, deferred).** This row is blank in the §2 table.

Where the ceiling is left blank, the area is OUT OF SCOPE for the slice (no scenes touching that kink). When Phase 3+ scopes the area, LO fills the row; only then can authoring proceed.

**Rule:** if a proposed scene touches a kink area whose ceiling row is blank, the scene doesn't ship until LO fills the ceiling. Don't author against an undeclared ceiling — that's how Phase C6 morning-chat drift happens.

---

## §5 — Anti-patterns

### §5.1 — Default to medium-explicit

The most common drift mode. ENI persona default prose register sits at "medium-explicit" — anatomically named but soft on cum descriptions, named character relationships but soft on taboo callouts, etc.

**Fix:** the §3 LO pattern is doctrine. Default to maximum-explicit; only soften if LO says so.

### §5.2 — Vanilla register at sexual register

Frank using "honey" / "sweetheart" during a Tier 4 sex scene. Marge being addressed by name with no register. Jake having sex without sibling callouts.

**Fix:** §2 table is the spec. If the row says FULL DADDY, FULL DADDY at Stage 4+. If the row says FULL INCEST CALLOUTS, callouts at all tiers.

### §5.3 — Authoring against undeclared ceiling

Phase 3+ Marge/Cookie kink area is blank in the table. Authoring a Marge sex scene before LO fills the ceiling = drift.

**Fix:** out-of-scope areas don't ship until the ceiling row is filled. Stub the canvas (`(Phase 3+ placeholder — ...)`) and defer.

### §5.4 — Soft-pedaled cum / creampie / squirt descriptions

The anatomical+cum row (§2 table) says MAXIMUM CRUDE DETAIL. "Between your legs" instead of "your pussy" violates. "He finished" instead of "he came inside you, his cum dripping out as you stood up" violates.

**Fix:** crude direct diction. Specific. Anatomical. Visceral.

### §5.5 — Reframing kink as wholesome dynamic

The Diana cuckold row (§2 table) says FULL CUCKOLD. Reframing the brought-in branch as "they all became close friends" / "Diana finally accepted polyamory" violates — cuckold IS the resolution kink for that branch.

**Fix:** brought-in = cuckold. Diana watches / listens / participates explicitly. Per the row's example dialogue ("watch your husband fuck me").

### §5.6 — Treating outdoor as location label

Public exhibitionism row says FULL RISK + ONLOOKER AWARENESS. Treating outdoor as just a location ("Frank takes Maya in the yard") without exploiting the risk-frame ("someone could see, the neighbors, if Diana looks out the kitchen window") violates.

**Fix:** outdoor scenes name the risk. Exhibitionism IS the kink — the risk gets Maya off. The prose explicitly references the visibility.

### §5.7 — Ignoring the paternal frame in Frank scenes

Frank dialogue without paternal authority cues ("come to daddy," "good girl"); Maya's interior framing him as "Frank, who's been my landlord" instead of "daddy, who pays for this house and now pays for me with his cum."

**Fix:** Frank's paternal authority is part of the kink at ALL TIERS. Even Tier 0-1 beats reference it implicitly. Tier 4+ beats reference it explicitly via "daddy" register.

### §5.8 — Avoiding the incest callouts in Jake scenes

Jake sex scenes without "brother" / "sis" / "little sister" callouts; generic dialogue that could be any two characters.

**Fix:** incest IS the kink. Named and dwelt on at all tiers. Pre-Tier 3 scenes: framed implicitly ("my brother's eyes" / "the way he watches you"). Tier 3+: explicit callouts during sex.

### §5.9 — Mixing ceilings across NPCs

Frank Tier 4 in daddy register; Marcus Tier 4 in school/peer register; mixing these registers within Maya's POV. Maya doesn't suddenly use "daddy" with Marcus.

**Fix:** ceiling is per-NPC. Maya's register adapts to the NPC. Per-NPC consistency throughout.

---

## §6 — Authoring procedure

### §6.1 — Before authoring a Tier 4+ canvas

- [ ] Locate the relevant row(s) in §2 table for THIS NPC + THIS kink area
- [ ] Read the "Examples allowed" column — internalize the diction level
- [ ] Read the "Examples NOT allowed" column — internalize what to avoid
- [ ] If the NPC brief's §2 voice spec has additional framing rules for this stage, read them
- [ ] If the kink area's row is blank or "TBD" — surface to LO before authoring

### §6.2 — During authoring

- [ ] Every line of Tier 4+ sex dialogue uses the registered vocabulary
- [ ] Anatomical references are crude direct (no euphemisms)
- [ ] Power-dynamic dialogue per the row's example list ("good girl," "open your mouth," "such a slut")
- [ ] Per-NPC framing applied (daddy for Frank Tier 3+; incest callouts for Jake; cuckold for Diana brought-in)
- [ ] Risk-frame for outdoor scenes (visibility, onlooker awareness)

### §6.3 — Post-authoring grep audit

Run on each new Tier 4+ canvas:

```bash
# Frank should have daddy register at Tier 4+
grep -n "daddy\|good girl\|baby girl" <canvas_body>

# Jake should have incest callouts
grep -n "brother\|sis\|little sister\|stepbrother" <canvas_body>

# Anatomical specifics (not euphemisms)
grep -n "cock\|cunt\|tits\|cum" <canvas_body>

# Outdoor scenes should name the risk
grep -n "see\|onlooker\|neighbor\|window\|caught" <canvas_body>  # for outdoor canvases
```

If a Frank Tier 4+ canvas has zero `daddy`/`good girl`/`baby girl` hits — register is soft. Rewrite.

If a Jake Tier 3+ canvas has zero `brother`/`sis`/`stepbrother` hits — incest framing is missing. Rewrite.

---

## §7 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P9 — per-arc vocabulary ceiling principle source
- `doctrine/05_rts_flat_prose.md` §2 Rule 6 — direct/crude diction per per-arc ceiling
- `doctrine/06_design_brief_template.md` §3.2 + §3.3 — brief §2 voice spec + §3 ladder include vocab columns
- `doctrine/07_anti_patterns.md` §5 — voice anti-patterns

### Source

- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §7.5 — canonical vocab ceiling table source
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` §2 — Frank daddy framing rules (worked example)
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §6 — Tier-3 voice register

### LO answer pattern (2026-05-16)

The 7-row maximum-explicit answer pattern is documented in:
- Doc 30 §7.5 "Vocab ceiling pattern observed across user answers (2026-05-16)"
- The locked column reads "FULL DADDY FRAMING (2026-05-16)" / "FULL BREEDING TALK (Phase 2+)" / etc.

### Phase 2+ deferrals

- **Frank breeding talk** — Phase 2+ retrofit when pregnancy ships (Doc 65 E10b)
- **Diana matriarch-domination + blackmail branches** — Phase 2+ scope (Doc 60 Open Q #3 + Doc 65)
- **Marge / Cookie lesbian initiation** — Phase 3+ scope (Doc 30 §8.2 + Doc 61)
- **Cross-NPC kink combinations** (e.g., Frank + Jake threesome) — Phase 3+ scope; ceiling row added when LO scopes

---

**End of file.** Next: `reference/01_rts_overview.md` for the RTS catalog overview.
