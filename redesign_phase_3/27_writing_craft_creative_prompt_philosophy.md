# 27 — Writing Craft & the Creative-Prompt Philosophy

How do the best sandbox adult Twine games actually *write* — and what does that teach us about the creative
prompts we use to generate content? This doc answers the prose/content question, the way doc 26 answered the
structure question. It pairs a source-grounded study of ten of the most popular sandbox Twine games on
mopoga/gamcore (raw passage source read off disk, not site blurbs) with three web-research angles on adult-IF
writing craft, then maps the findings against our current prose doctrine (`doctrine/05_rts_flat_prose.md`) and
says honestly where that doctrine is craft and where it is a single-game overfit.

**Position:** a research + analysis doc, **review-only — no skill or doctrine files were edited and nothing here
is implemented.** It is the future-lookup reference for an eventual prose-doctrine redesign; that redesign is a
separate decision LO makes *from* this doc, one task at a time. Produced 2026-06-18 by a 27-agent workflow (run
`wf_a8a600ff-1a6`): 10 source-grounded per-game writing profiles + 3 web dossiers → synthesize → **adversarially
verify each principle against the real text** → map to doctrine → completeness-critique. Every claim is tied to a
quoted line; inflated claims were downgraded (one principle was caught and corrected in verification, §4 P10).
Provenance + caveats in §8–§9.

**Companion to doc 26.** Doc 26 found the skill *won the structure war* (QBN + salience + open-map + loop-and-grow)
and named the one critical structural gap (no player-identity axis). This doc looks at the orthogonal layer — the
**words on the page** — and finds our prose doctrine is *more* RTS-overfit than the structure doctrine was, because
it is literally named "RTS-flat" and every worked example comes from one game.

---

## §1 — The reframe: density is downstream, not the master axis

Our prose doctrine is organized around a single variable: **density** (terse RTS-flat vs. earned literary
capstone). The most important finding of this research is that **density is not the master axis — it is a
*consequence*, and the genre's best games vary on at least three axes our doctrine never names.**

Two findings, in order of importance:

**(A) Density is forced, not chosen.** Where a game sits on the terse↔lush spectrum is determined by two
structural facts, not by taste:
1. **Media load** — how much of the erotic/world load is carried by an image/video beside the beat. When an
   explicit clip plays next to every line, prose that *describes the act* is redundant, so it collapses to a
   transition caption. When the words are the only porn (text-only games like CoC), prose must do everything.
2. **Re-read economy** — is the core loop a terse strategy grind (where identical repeated text would grate) or
   an immersive-romance fantasy (where cozy sensory texture *is* the product)?

RTS-flat is **one coherent economy** — media carries the heat + terseness keeps a grind re-readable — and it is
*faithfully* derived from RTS. But at least four other top games (New Life Project, Young Maria, Zara's School
Life, The Company) run **lusher** registers successfully because they pay the re-read-fatigue bill a *different*
way: RNG vignette rotation, corruption-forked interiority, combinatorial state-rendering — variety instead of
brevity. Density is real and structural; it is **not** a free taste knob, but it is **also not one-size-fits-all**,
and "everyone should write RTS-flat" is false.

**(B) Density is the *RTS* lens.** RTS's whole identity is a density *position* (ultra-terse caption-over-video),
so a doctrine derived from RTS inherits "density is the master variable." A non-RTS author would foreground three
*orthogonal* axes first — and these are the genuinely new creative-prompt territory (§5):
- **Fantasy-position** — is the second-person "you" a dom who takes, a sub it happens *to*, a blank self-insert,
  or a defined protagonist with narrated motive? Four different writing contracts.
- **Kink-keyed register** — diction is modulated by the kink being served, not held at one "crude-direct" setting.
- **Tonal color** — the committed voice itself ranges from grim-deadpan to coy-naive-warm to sardonic-noir.

So the corrected frame: **density is a forced consequence of media-load × re-read-economy; the *content*
decisions live on fantasy-position, kink, and tone.** What is universal is *neither* density *nor* tone — it is the
underlying craft (§3).

---

## §2 — The density spectrum (four bands, and what forces each)

Mapped terse → lush, with where each profiled game sits and *why its position is correct for its genre*:

| Band | Games | Unit | What forces it |
|---|---|---|---|
| **Ultra-terse caption-over-media** | RTS, Life at University, Lustbound, Become Someone's *ambient* tier | 1–2 sentences, ~15–35 words, zero environmental prose; the clip IS the scene, prose narrates the *transition* + carries dirty-talk | A clip plays beside every line → describing the act is redundant. RTS-flat lives here. |
| **Terse-charged survival** | Degrees of Lewdity | Same 2nd-person terseness, but a *thin* load-bearing sensory layer (a knife, a flickering bulb, students looking up) | In a PREY game the environment *is* the danger meter — sensory grounding is the threat, not ornament. |
| **Moderate stat-sim / webnovel** | Become Someone, The Company, Shady Deals | 25–70-word action paragraphs, fluent, lightly inferential; ONE establishing sense per setpiece then drop to action; narrator may editorialize the player's motive | Media-led *but narrative wish-fulfillment* — each clip wants a competent caption, and "being told you're winning" needs a confident motive-narrating middle voice. |
| **Lush-sensory life-sim / romance** | New Life Project, Young Maria, Zara's School Life | 40–160-word beats, every room grounded in smell/light/temperature *even in repeatables*, warm or coy interiority | Picture-LED-but-immersion-first — the cozy sensory texture IS the product; flattening it guts the appeal. Pays the re-read bill with *variety + state-forking*, not restraint. |

Zara's School Life is the outlier worth flagging: **third-person past tense** (the only one of ten), because it is
a corruption-*novel* wearing a sandbox, not an RTS-shape sandbox. It proves 2nd-person-present is the sandbox
default, not a law of erotic IF — and that the novel form is what 3rd-past is reserved for.

---

## §3 — What is genuinely universal (the shared craft)

Strip away density and tone, and a hard core survives in **all ten games + the web craft canon** (Failbetter,
Choice of Games, MetaStellar). This is the part that should hold at *every* density and become the spine of the
creative prompt. (Two axioms the completeness pass flagged as over-stated are reconciled here.)

1. **Second-person, present tense, for the live beat.** Near-universal (9/10; the lone exception is the
   novel-form Zara). "This is happening to you now." Past tense appears only in framing/recap.
2. **Crude-direct anatomy *as the default*, never euphemism, never clinical** — `cock/cunt/pussy/tits/ass/cum`
   used plainly *for charge and character.* (Reconciled: this is the **default explicit register**, not an
   absolute — lush romance/aftercare tiers deliberately *soften*, and that is a kink/tier choice, not a failure.
   See §5-B.)
3. **Render the state, don't label it.** Never "she felt aroused" / "her corruption rises" — render the
   observable tell (the catch of breath, the involuntary press-back, the changed word choice) and let the reader
   infer.
4. **Dialogue does the *primary* voicing.** Character is built from voiced lines + behavior, not narrated
   psychology. (Reconciled: "narration does *none* of the character work" is RTS-specific — in warm life-sims the
   *narration* carries motive and is the signature voice; the universal is that dialogue does the **primary**
   work, not that narration does nothing.)
5. **Escalation = the same slot re-rendered as state advances** — a branch swap, a line swap, a pool-tier pull,
   an interiority flip. Never thicker prose, never a narrator announcing the stat. (Most consistent finding across
   all ten games.)
6. **The HUD/sidebar carries the numbers** so prose never recites stats; deltas render as styled `+/-`, out of the
   prose.
7. **Image/video-first staging** — the beat opens on the picture; prose narrates *to* it. The denser the media,
   the terser the prose can be (this is the lever that sets §2's band).
8. **NPCs are people with independent wants** — they lie, coerce, refuse, scheme. Yes-men read as filler; the
   web corpus pans isolated arcs as "lukewarm" and praises arcs that *ripple into other characters*.
9. **Per-NPC held voice handle.** Each strong NPC has a nameable, consistently-held verbal tic/worldview
   (clipped-accented Volkov, silk-over-menace Sophie, chirpy-zoomer Lily). Where voices blur into one template,
   reviewers downgrade to "interchangeable."
10. **One committed voice, game-wide, never flinching** — tonal whiplash and hedged/milquetoast adult writing
    both read as quality defects. (The *content* of the voice varies hugely; the *discipline* of holding it is
    universal. Critical for generated content, where per-scene generation risks exactly the multi-author whiplash
    players route around.)
11. **Anti-repetition is the genre's #1 named weakness** — but *watching* it, not a universal *practice* (see §4
    P10): the player *complaint* is universal; the descriptor-substitution *engine* is titan-specific.

---

## §4 — The eleven creative-prompt principles

The synthesis payload: each principle is a droppable creative-direction directive, with how it *varies* across the
spectrum, and its adversarial-verify verdict. 10/11 held under verification; P10 was downgraded.

| # | Principle | Prompt directive (condensed) | Verdict |
|---|---|---|---|
| **P1** | **Set density from the media load, not taste** | Declare the media load for the beat *first*. Clip beside it → 1–2 sentence (~20–35w) transition caption; hand the heat to dialogue, don't re-describe the clip. No media → the words ARE the scene: write the specific image-forming detail the picture would have carried, still no environmental ritual. | ✅ supported |
| **P2** | **Specificity, not literary density** (the load-bearing thesis) | Replace every abstraction with ONE concrete named particular — specific body part, single object, one exact action, a named smell/texture. Never "they touched"; always what/where/how. Plain strong nouns, ≤1 earned image per beat, never stack adjectives. *Directness is the anti-purple move, not the crude move — flat is not less hot.* | ✅ supported |
| **P3** | **Render the state, don't label it** | Never name an emotion/arousal outright; render the observable tell and let the reader infer. Reserve narrated interiority for the PLAYER; build NPCs from voiced lines + a single observed tell. Only a warm/life-sim register may have the narrator infer the player's own motive. | ✅ supported |
| **P4** | **Crude-direct anatomy — for charge, never shock** | Real four-letter words plainly inside the act; never euphemism, never clinical. Function is arousal/character, NOT shock — no gross-out novelty. Plain at low corruption, filthier as the tier climbs. A lush romance register may pair ONE earned euphemism with the raw noun; a terse register stays purely crude. | ✅ supported |
| **P5** | **Escalation is a re-rendered slot, never thicker prose** | Show "you've changed" by re-rendering the SAME slot as state advances — branch variants keyed to a stat, so the identical action reads differently at each tier. Cheapest instrument that lands: swapped line, changed honorific ("Sir" that wasn't there), flipped reaction-voice (disgust→appetite), different pool. Never announce the stat; never thicken the prose. | ✅ supported |
| **P6** | **Variation, not brevity, defeats lush re-read fatigue** | Decide the re-read economy first. TERSE repeatables → one flat caption, rotate only the media. RICH repeatables → you MUST pay the variation bill: 6–10 RNG-selected vignettes and/or detail forked off stats. Reserve once-only literary spend for true capstones *only in a terse economy*. Never ship a high-frequency slot whose words are identical + generic every visit. | ✅ supported |
| **P7** | **Pace the act in beats** | Build a rise-and-fall arc: anticipation → first contact → escalation → climax → aftermath. Click-by-click if the engine supports it (each beat hands off to its clip); else one block that still hits every stage. Vary sentence length to the arc — longer breaths in anticipation, clipped at the peak. Close on a small aftermath beat, never a hard cut at orgasm. | ✅ supported |
| **P8** | **Sensory ritual OFF filler — spend only where load-bearing** | Treat environmental description as a budget. Strategy/media-led game → cut ambient scene-painting (HUD names place, image shows it). Prey/survival → spend sensory ONLY on what carries threat/exposure. Warm life-sim → ground the room in one sensory particular (that immersion IS the product). ALWAYS keep BODILY sensation on in sex — a *different* budget from ambient scenery. | ✅ supported |
| **P9** | **Every NPC: a held voice handle + a want they'll act on** | Assign each NPC ONE nameable voice handle and hold it in every line. Character through voiced dialogue + behavior, not narrated psychology. Give each a want they ACT on — let them lie, coerce, refuse, steer; never a yes-man. Where possible, ripple one NPC's arc into another's. Scale establishing-prose to density; the voice handle is mandatory at every density. | ✅ supported |
| **P10** | **Anti-repetition — watch it; descriptor-substitution is optional** | Repetition of body-part/action phrasing is the genre's most-named weakness — *watch it*. In **long, body-variable** scenes, resolve anatomy from state (DoL `penisdesc`, The Company body-config switch-ladders) so the same scene emits varied, body-aware lines. In **short terse captions** (RTS, Zara), keeping it terse + varying the clip is enough, and one repeated verb-noun is tolerable. | ⚠️ **overstated → corrected** |
| **P11** | **Pin ONE committed voice, never flinch** | Choose one register (hostile-prey-dread / dark-comic-deadpan / coy-naive-warmth / sardonic-street-noir) and pin it globally — same crudeness, pacing-grammar, worldview every scene; no per-scene drift. Commit hard: when the premise is dark/explicit, go there fully. Hedged, softened adult writing reads as fake. Sincerity + consistency beat prettiness. | ✅ supported |

**The P10 correction (the one adversarial catch worth reading in full).** The synthesist generalized a
**titan-specific engineering choice** into a universal law. Verification (verbatim-checked against source):
descriptor-substitution is *real* and load-bearing in exactly two games — DoL (`penisdesc` 1065×, `<<genitals`
1005×, `<<penis` 1325× across the corpus; e.g. *"His penisdesc dominates yours…"* gated on `penissize gte 4`, with
a *"compensates his lack of size with dexterity"* branch at `penissize lte 1`) and The Company (a switch-ladder
over `isChastity()/hasStrapon()/frontPlugged()/isSissy()`, each arm a correctly-worded sentence). But it is **not
universal**: RTS — *our own gold-standard game* — hardcodes the bare word "cock" **14 times in a single passage**
(`MarcusBedroomSex1`), with **5 `<<switch>>` in all 364 passages** and no anatomy macro anywhere; Zara's repeats
"cock" **94×** in a passage with 1 switch in 730 passages. The terse best-sellers *openly ignore* the rule and ship
successfully. **What is universal is the player *complaint* about repetition (the CoC pan is genuine), not the
practice of forbidding it.** Treat descriptor-substitution as a high-effort technique that pays off in long
body-variable scenes — not a law.

---

## §5 — The orthogonal content axes the density lens hides

The completeness pass surfaced the genuinely *new* creative-prompt territory — the axes our density-organized
doctrine never names. These are where the actual *content* decisions live, and a generator prompt that only sets
density will be blind to them. **This is the highest-value section for "how we write creative prompts."**

**A. Fantasy-position contract (the biggest missing axis).** The second-person "you" is not one thing. Four
contracts, each licensing different prose:
- **Dom / take** ("you take what you want") — agency-verbs, the player drives, NPC reactions foregrounded.
- **Sub / receive — it happens TO you** (DoL, Zara) — the prose foregrounds what is done to the player; agency
  language recedes; dread/appetite is the register.
- **Blank self-insert** (RTS) — minimal narrated interiority, the player projects; "you" is a camera.
- **Defined protagonist with narrated motive** (Become Someone: *"…partly because you just like seeing her in a
  bikini"*) — the narrator supplies the player's motive and read-of-the-room; inferential prose is the *signature*.

These determine how much interiority, agency-language and motive-narration the prose may use — *upstream* of
density. The prompt should declare the fantasy-position before sizing a single sentence.

**B. Kink-keyed register.** "Crude-direct, never euphemism" is itself an over-claim. The best games modulate diction
*by kink*:
- **corruption / incest** → relational-taboo nouns, *deliberately hammered* ("your sister," "mom") — **the repeated
  taboo word IS the charge**, which directly *contradicts* P10's anti-repetition. (This is the internal
  contradiction the doctrine must carve out: anti-repeat the *generic* descriptor, hammer the *taboo* one.)
- **degradation / humiliation** → demeaning second-person address.
- **romance / vanilla / aftercare** → deliberately *softens* toward warmth (the euphemism is earned here).
- **BDSM** → command-and-protocol diction.
- **prey / non-con** → resistance-and-threat register.

A creative prompt needs a kink→register table, not one global crudeness setting.

**C. Writing the non-/dubious-consent beat.** CLAUDE.md greenlights non-con as core content, yet there is *zero*
craft guidance for it. The real questions: whose agency the prose foregrounds (coercer vs. coerced); how
consent-state is *rendered through behavior/resistance, not labeled*; how a player-*refused* beat reads vs. a
forced-*on*-player beat; aftermath-beat discipline. This is a glaring hole for this project specifically.

**D. Transformation / body-state prose.** Pregnancy is already in the corpus; the genre canon (CoC, TF games, New
Life's gender-identity thread) lives on **continuous-state body description + before/after contrast** — a distinct
register that "render the tell, don't label it" doesn't reach. How to write a *changing* body (pregnancy, bimbo,
TF) over time is its own craft.

**E. Tonal-color menu + session pacing.** P11 says "hold one voice" but gives no menu for *choosing* it. The held
voice ranges across **comedic/camp (Lustbound), grim-deadpan (DoL, The Company), earnest-warm (Young Maria),
dry-transactional (RTS), sardonic-noir (Shady Deals)** — pick from the *fantasy*, then hold. And P7 paces the sex
*act* but nothing paces a *session/day*: the mundane→charged→explicit cadence, slow-burn vs. immediate contract,
how filler/world beats earn the payoff.

**F. Reactive-text discipline (generation-specific).** Prose must survive `@`-token substitution: player
name/build/pronouns, partner-rename, gendered second-person. "Genericize the untokenizable; resolve the
partner-noun from state; keep the second-person gender-safe" is a real creative constraint our memory already flags
on the mechanics side but no prose principle covers.

---

## §6 — Where `doctrine/05` is RTS-overfit (seven findings)

Verified places our prose doctrine over-generalizes one game. These read as *defects* when the target game is a
lush life-sim or a text-only scene:

1. **"Zero environmental sensory detail" is overfit.** RTS strips it because the video carries setting *and* it's
   a terse grind — but DoL keeps a thin sensory layer (the environment *is* the danger), and New Life / Young
   Maria / Zara / Shady Deals ground every hub because atmospheric immersion is *the product*. Correct universal:
   *"sensory off filler, spent where load-bearing,"* not *"zero."*
2. **"Literary density RESERVED for once-only Lane-4 capstones" is the biggest overfit — and RTS itself doesn't
   have it.** RTS's own capstones (`SellingMyStepsister`, the dad/trainer scenes) are *more flat beats*, not denser
   ones; the register never elevates. The reserved-literary-capstone tier is **our addition** for a no-media model,
   not an RTS property. Five games *invert* it — Zara/New Life/Young Maria/Shady Deals/Become Someone put the
   density ON repeatables (paid for with variety + state-forking) and reserve terseness for *navigation*.
3. **"≤2 sentences of stage direction per beat" is a media-economy artifact.** Holds for media-led games (the clip
   carries the rest) but Become Someone runs 4–8 narrated sentences, The Company 25–50-word blocks, Shady Deals
   3–5-sentence intros, New Life 60–120-word hubs — their prose does work the RTS video does. Beat length is forced
   by media load (P1), not fixed at 2.
4. **"No inferential prose" is overfit to the terse register.** Right for a terse strategy sandbox — but Become
   Someone's and Young Maria's *entire voice* is inferential (*"you can't help but buy into her"*), and it's their
   signature, not a defect.
5. **"Dialogue does the character work" implies narration does NONE** — but in Become Someone and Young Maria the
   *narration* carries equal character/motive weight, and Zara's headline craft move is corruption-forked
   *narrated* interiority. The universal is "dialogue does the **primary** voicing."
6. **The ~30-word image-first caption is the one RTS-flat claim genuinely correct AND externally supported**
   (Failbetter's literal 30-word root cap; Emily Short's restraint rule) — *but* as a **media-led-game unit**, not
   a genre law. A text-only game needs P1's other branch.
7. **POV/tense (2nd-person present) is treated as house style when it's the one near-universal FORCED choice** —
   so the doctrine is *right here but for the wrong reason* (genre law via Failbetter/CoG + 9/10 games, not RTS
   taste).

---

## §7 — Mapping to our doctrine + the highest-leverage changes

Full principle→doctrine table is in the workflow output; the actionable core:

**The five highest-leverage prose-doctrine changes (all `doctrine/05` + `content-framework`, analysis-only):**

1. **Rewrite Rule 3 (`05:50-61`) from "zero environmental sensory" to a genre-tuned budget** (P8). Media-led → cut;
   prey → spend on threat; life-sim → ground the room. Keep BODILY sensation always-on in sex (a separate budget).
   *This single change makes the doctrine portable across the three verified game shapes instead of universalizing
   RTS-flat.* Highest leverage.
2. **Add P1 (density forced by media load) as explicit doctrine** — "declare the media load first, then size the
   prose." Reframes Rule 8 (image-first) from "RTS always does this" to "this is the media-led branch of a
   spectrum."
3. **Add the repeatable-economics choice (P6) as a named decision** — two valid strategies (terse + media-rotation
   vs. lush + RNG-vignette/state-fork), chosen at Step-2 design time. The skill currently teaches "reserve density
   for capstones" without naming the choice behind it, so authors guess wrong and ship brittle repeatables.
4. **Elevate P3 (render-don't-label) to a universal principle separate from Rule 5.** Rule 5 ("no inferential
   prose") is a *lane restriction*; P3 ("render the tell, never name the emotion") is the universal *writing move*
   that still applies at the capstone tier (where interiority is *earned*, but still rendered).
5. **Soften P2's absolute metaphor ban → "disfavored, not banned."** "Specificity beats adjective-soup" is sound;
   the absolute ban on abstract climax metaphor is contradicted by DoL (a canonical, praised game). Default to
   concrete; allow a metaphor only if it carries specific charge.

Plus, from §5, the larger structural recommendation: **add the orthogonal axes (fantasy-position, kink-register,
non-con craft, transformation prose, tonal menu, reactive-text) as new content-design dimensions** — these are net
*additions*, not corrections, and they are where the creative-prompt guidance is currently thinnest.

**What is genuinely fine as-is (don't manufacture work):** RTS-flat is a *real, coherent house style* for an
image-first media-led game — the error is never in teaching it, only in *overstating its universality*. Rule 6
(crude diction per per-arc ceiling, `doctrine/08`), Rule 4 (dialogue-does-character-work), the Tier-3
capstone-density frame, the dual-register table, the thought-bubble primitive, and the anti-pattern catalogue
(`05:190-260`) are all correct and need no change. The fix is **scope**, not **replacement**: re-frame the terse-flat
rules as the *media-led branch*, keep the universal craft (§3) at every density, and add the axes the density lens
hid (§5).

---

## §8 — Caveats (read honestly)

- **Source is direct, dev-intent is not.** Per-game findings come from reading the *shipped* Twine passage source
  on disk — direct observation, but not dev-confirmed authorial intent. Quoted lines are short fair-use analysis
  snippets (≤~30 words) for criticism.
- **Web sources partially gated.** Some F95zone/wiki review threads returned HTTP 403; reader-praise findings lean
  on accessible reviews/devlogs + cross-corroboration, so treat the *critical-reception* claims as indicative.
- **The density-axis residue is acknowledged, not eliminated.** §1-B and §5 name that "density as master variable"
  is itself the RTS lens; the spectrum (§2) is still organized by density because that's how the *games* visibly
  differ — but the orthogonal axes (§5) are the corrective, and a redesign should lead with them.
- **The genre has no published prose *theory*.** All cited craft theory (Failbetter/Short/CoG/MetaStellar) is
  genre-neutral IF/erotica craft applied here; adult-specific findings are extrapolated from the games + reader
  reception, not a dev design doc.
- **Analysis only.** No skill, doctrine, or game file was edited. The redesign is LO's call, one task at a time.

---

## §9 — Provenance + per-game voice signatures

**Workflow:** run `wf_a8a600ff-1a6` (27 agents, ~1.57M subagent tokens): 10 source-grounded per-game profiles + 3
web dossiers → synthesis (11 principles) → per-principle adversarial verify (10 supported / 1 corrected) → doctrine
mapping → completeness critique. Full structured output in the task transcript.

**Source on disk:** `game_explorations/<slug>/passage_catalog.json` (raw Twine source) for every profiled game —
the `tl-*` folders mirror the gamcore/mopoga popularity lists 1:1.

**Per-game voice signature (the appendix — each game's one distinctive move):**

| Game | POV / density | Distinctive signature |
|---|---|---|
| **Road to Success** | 2nd-present / ultra-terse | The video is the scene; prose is a one-line caption announcing the next clip. Porn-storyboard captioning, not erotica. *No* reserved literary tier. |
| **Degrees of Lewdity** | 2nd-present / terse-charged | A self-looping, anatomy/attitude-**combinatorial sex engine**: one passage renders one state then links to itself, prose parameterized by anatomy + `$phase` attitude. |
| **Become Someone** | 2nd-present / moderate-uniform | **Second-person inner-monologue play-by-play** — the narrator supplies your motive and your read of the room in plain confident prose. |
| **The Company** | 2nd-present / moderate-lush | **Combinatorial variant-prose** — every beat written N times (switch-ladders over body/partner/dose) so the "you" never lies about who you are; deadpan dark-comedy. |
| **New Life Project** | 2nd-present / lush *in repeatables* | The TF/identity interior thread — the same repeatable masturbation passage tracks a stat to evolve a running becoming-a-girl confession. |
| **Shady Deals** | 2nd, tense-wobble / moderate-non-uniform | The **editorializing location caption** — every district label is a noir mood-line with a worldview; density varies by slot importance. |
| **Life at University** | 2nd-near-present / terse | Prose is a **caption layer for a video gallery** + a "sin log"; flips the protagonist's interior (disgust→appetite) on one corruption number. |
| **Young Maria** | 2nd-near-present / moderate | Coy-naive 2nd-person + sudden clinical filth, with the **visible LOCKED-TEASER** (`[Corruption 30, Relationship 40]`) making the ladder legible in-scene. |
| **Zara's School Life** | **3rd-past** / split (sex 5× denser) | The **corruption-gated in-place prose fork** — one sex beat written twice (trauma vs. appetite), `$PlayerCorruption` picks which sentence you read. |
| **Lustbound** | 2nd-present / bimodal | The **genital-matchup combinatorial engine** — one "scene" covers M/F, F/F-toys, strapon, trans, incest-perk via `<<if>>` trees; eroticism outsourced to clips. |

**Related docs:** doc 26 (`26_nonlinear_rpg_storytelling_research.md`, the structure companion); doc 21
(`21_field_survey_and_skill_review.md`); doc 18 (`18_step5_content_roster.md`, the archetype catalog); doctrine
`05_rts_flat_prose.md` (the file under the microscope), `08_kink_vocab_ceilings.md`, `content-framework.md`.

**Status:** Analysis only — nothing implemented. Recommended starting point if a prose-doctrine redesign begins:
the Rule-3 sensory-budget rewrite (§7 #1) + naming the fantasy-position axis (§5-A), in that order.
