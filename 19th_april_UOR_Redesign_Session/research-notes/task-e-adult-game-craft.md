# Task E — Adult-Game Narrative Craft (Ethnography)

Scope: craft discussions from the communities that actually make long-form corruption/transformation/lifesim adult games. No smut content — only structure, pacing, character, consent, and system-narrative integration talk.

Date of gather: 2026-04-21. Research budget: ~15 searches, 6 deep reads attempted (3 hit 403 on the first attempt — Miraheze wiki cluster and the Vren patreon page all block automated fetches; recovered intent via cross-referenced search snippets and adjacent pages).

---

## Sources

### Primary — developer writing
- **Vrelnir interview (Degrees of Lewdity)** — Sad Girl Theory, Jan 2022: https://sadgirltheory.com/2022/01/06/degrees-of-lewdity-conversation-with-vrelnir/ [deep read, clean fetch]
- **Vrelnir Writer's Guide** — Gitgud wiki: https://gitgud.io/Vrelnir/degrees-of-lewdity/-/wikis/Writing/Writer's-Guide [attempted fetch; page gated, captured via search snippets + Changes diff view]
- **Vrelnir — English Class writing doc** — https://gitgud.io/Vrelnir/degrees-of-lewdity/-/wikis/Writing/English-Class [surfaced via search, not fetched full]
- **Vren — "The Gameplay Loop of Lab Rats 2"** — https://www.patreon.com/posts/game-design-loop-19898042 [patreon 403; content captured via search snippets + devlog follow-ups]
- **Lab Rats 2 character_guide.txt** — https://gitgud.io/lab-rats-2-mods/lr2mods/-/blob/develop/game/character_guide.txt [GitLab UI gated; captured via search snippets]
- **Anthaum (Course of Temptation) devlog v0.7.7** — https://anarchothaumaturgist.itch.io/course-of-temptation/devlog/1451561/course-of-temptation-march-update-v077 [deep read, clean fetch]
- **Splendid Ostrich Patreon (Newlife)** — https://www.patreon.com/splendidostrich/about [meta only — most craft talk is Patreon-gated]
- **Majalis (Tales of Androgyny) combat-design forum thread** — https://itch.io/t/2065484/combat-design [deep read, clean fetch]
- **Vren Roadmap — Phase 1 vs Phase 2 split** — https://www.patreon.com/posts/lab-rats-2-19120079

### Primary — craft theorists
- **Emily Short — Interactive Romance category** — https://emshort.blog/category/interactive-romance/ [deep read, clean fetch]
- **Emily Short — "Procedural Text Generation in IF" (2014)** — https://emshort.blog/2014/11/18/procedural-text-generation-in-if/ [deep read, clean fetch]
- **Michelle Clough — *Passion and Play*** — https://www.routledge.com/Passion-and-Play-...-9780367404659 [book-level survey; TOC + author-quote capture]
- **Gamasutra/Gamedev "Ways of designing intimacy in games"** — https://www.gamedeveloper.com/design/ways-to-design-intimacy-in-games [deep read, clean fetch]
- **Nguyen & Ruberg — "Challenges of Designing Consent" (CHI 2020)** — https://ourglasslake.com/wp-content/uploads/2020/06/Nguyen-Ruberg-Designing-Consent-CHI-2020.pdf [academic]
- **Choice of Games — "Making erotic content a choice" forum thread** — https://forum.choiceofgames.com/t/making-erotic-content-a-choice/11853

### Reference wikis (Miraheze blocks WebFetch, used via snippets)
- Degrees of Lewdity Wiki — Lewdity Stats, Traits, Trauma, Current Condition, Bodywriting, Attitudes
- Course of Temptation Wiki
- Tales of Androgyny Wiki

---

## Findings — 20+ craft techniques

### Structure and transformation arc

**1. Vrelnir's Control-vs-Trauma dual-track (DoL).** Corruption isn't a single meter going up. Trauma accrues through non-consensual acts; Control is restored through *transgressive* acts the PC performs voluntarily. Quote: *"High trauma can be managed as long as the PC has a sense of control. The main way to restore control is to push the boundaries of the PC's inhibitions, performing acts they feel are transgressive."* Design consequence: the PC's self-authored slide is how she climbs out of trauma — narrative and mechanics agree that corruption is an agency-restoration strategy, not a passive drift. Originally conceived as binary (gained/lost), later converted to incremental for pacing. [Sad Girl Theory interview]

**2. DoL's Awareness layer — mechanical effects narrate themselves twice.** Every action has a mechanical resolution and an Awareness-gated narrative resolution. Low Awareness (0/7) renders lewd events oblivious/unwitting — the PC narrates them as accidents or confusion. High Awareness (7/7) renders the same event with full erotic recognition. Same stat tick, different prose. Promiscuity gain can be suppressed or allowed based on Awareness, because "you wouldn't necessarily view something as lewd" without the perception to frame it that way. Design consequence: writers don't need five separate events for five corruption tiers — one event with Awareness-conditional text handles the arc. [DoL wiki + Vrelnir interview]

**3. Lewdity triad — Promiscuity / Exhibitionism / Deviancy as parallel corruption axes.** DoL doesn't run one corruption number. It runs three separate axes, each unlocking different actions at each tier. A low axis *hides* access to intense actions; a high axis *dampens* impact of mild ones. The PC can be a deep exhibitionist and a shallow promiscuity stat — giving the transformation-arc shape instead of a single monotonic rise. Each restores Control at rates matching the PC's internal lewdity profile. [DoL Lewdity Stats wiki]

**4. Lab Rats 2's three-loop model (business / corruption / research) — loops intersect but do not collapse.** Vren's design blog names three loops: (a) business = make serums → sell → reinvest, (b) corruption = make NPCs sluttier and make it stick, (c) research = unlock new traits for better serums. Interesting play happens *at the intersections* — serum tier from the research loop feeds corruption velocity; corruption unlocks business roles. Craft lesson: never collapse to a single loop; the pacing comes from which loop the player prioritizes this session. [Vren "Gameplay Loop of Lab Rats 2"]

**5. Phase 1 vs Phase 2 — infrastructure-before-character.** Vren openly splits development: Phase 1 = mechanical scaffolding (dynamic outfits, personality slots, trance system); Phase 2 = unique named characters with authored storylines. Phase 2 is unbuildable without Phase 1's text-generation muscle. Craft lesson for long-form: write the variation engine first, stamp authored content onto it second. [Vren roadmap post]

**6. Course of Temptation "inclinations" — traits as narrative accumulator, not just stat.** CoT collects *inclinations* (personality traits) through actions. During encounters, PC inclinations negotiate with NPC inclinations to shape what happens. Acts aren't picked from a corruption-tier menu; they're surfaced based on the overlap of two personality sets. Craft consequence: the same tier of "slutty" feels different depending on *which* inclinations the PC earned getting there. [CoT site + wiki via snippets]

**7. NPC memory as corruption receipt.** CoT: "NPCs will remember you — that time you flashed them, that one drunken encounter — and can start rumors about you." The PC's corruption becomes *externalized* as the town's gossip about her, which then gates future events. Transformation isn't a number on the HUD; it's what the neighbor says when she passes. [CoT design summary]

**8. DoL Bodywriting — corruption receipts that survive the event.** Messages written on the PC's body persist across scenes. NPCs react to what's written. A drunk scene ends; the slur on her thigh outlasts it, and the bus driver reads it tomorrow. Mechanism: the corruption arc has physical lag — she can't undo last night until she can get to a shower that isn't surveilled. [DoL Bodywriting wiki]

**9. Free Cities — procgen NPC body/accent pipeline.** Accents tiered by intelligence × education × nationality × ethnicity. Body descriptions assembled from slots. Means a slave-management game of 50+ NPCs can make each one feel specific without authoring 50 hand-written descriptions. Craft tradeoff: recognized as "pure systems" — less emotional arc per NPC, more breadth. [Free Cities blog + Reddit summaries]

### Pacing of intimate content

**10. Anthaum's "infrastructure update" vs "content update" rhythm.** CoT alternates: one monthly patch adds systems (chainable texting, likeability algorithms, portrait crafting); the next adds content that leans on those systems. Prevents the common trap of shipping content that stales the engine, or engine that stales without content. Quote: *"Most of this was under-the-hood coding work enabling responses to chain into longer conversations."* [CoT devlog v0.7.7]

**11. Robert Yang (via Gamedev Intimacy article) — "show up every day" pacing.** *Rinse and Repeat HD* uses a real-time schedule: players must actually show up for a partner regularly. Intimacy is about "learning what the other person wants" over elapsed time, not stat threshold. Craft lesson: clock-based pacing beats meter-based pacing for making repeat intimacy feel earned. [Gamedev.com "Ways of designing intimacy"]

**12. Heart's Choice / CoG pacing norm — consent is continuous, not one-time.** CoG's guidance for romance writers: leave room for characters to say "no" comfortably at every step, and romances should be two-way (the NPC can refuse the PC even after an established arc). Craft tool: model "romance" as a series of micro-consents, each re-negotiable, not a boolean unlocked by stats. [CoG forum thread "Make romance a two way thing?"]

**13. Michelle Clough's show-vs-fade-to-black decision matrix (*Passion and Play*).** Frames the first-intimate-scene question as a narrative-function choice, not a content-gating one: fade-to-black preserves interiority and is correct when the scene's purpose is relational; explicit is correct when the scene's purpose is character-revelatory or embodied. The choice is per-scene, not per-game. [*Passion and Play* TOC + author summaries]

**14. Vrelnir on placing the first lewd event early, not gated behind grind.** DoL opens in the orphanage and the first sexually-charged encounters can occur within the first in-game week via random street events. Vrelnir's implicit pacing: the *first* incident is lightweight and early so the *second* can carry weight. Stat-gated first intimacies create a grind-feeling; ambient-incident first intimacies create a world-feeling. [DoL + tips wiki]

### Consent, refusal, coercion craft

**15. Vrelnir on asymmetric consent — player consents to the game; PC doesn't consent to scenarios.** Direct quote: *"The lack of consent on the part of PC is important, and the player is affected by that. They consent to play the game, but not necessarily to every little annoyance."* This is the design justification for writing coercive scenes as story rather than puppet-show — the *game-frame consent* (the player chose this genre) is explicitly separated from *scene-frame consent* (the PC's agency within the scenario). The player's awareness of this split is what makes the coercion legible as fiction. [Sad Girl Theory interview]

**16. DoL combat — arousal as attrition clock with Willpower as counter-stat.** Combat integrates sexual stakes without reducing them to a minigame. When Arousal caps, the PC orgasms and is stunned 3 turns with only two options available. Willpower — raised by *enduring* orgasms and pain — cuts stun short. Restoring Control post-combat requires committing a Promiscuity/Exhibitionism/Deviancy act matching your lewdity level. Craft lesson: consent is embedded in the mechanic — the player recognizes which acts the PC will accept by what restores her Control. [DoL Combat wiki]

**17. Nguyen & Ruberg (CHI 2020) — consent as system-level mechanic, not a dialogue option.** Academic frame: consent should be continuously negotiable, boundary-holding belongs to the party whose boundary it is, and consent mechanics should tolerate mid-scene modification. Design implication: any scene with a "safeword" escape is already more mechanically honest than a scene with only pre-scene yes/no. [Nguyen & Ruberg PDF]

**18. Majalis's "multiple combat outcomes" — surrender, first-blood, persuasion as parallel win states.** Tales of Androgyny combat includes charisma-based persuasion (convincing opponents to surrender, taunting them into rage, theatric feints). Sexual outcomes are one of several ways a fight resolves, not a penalty path. Craft consequence: the PC's *willingness* modifies which resolutions surface. Short-term sex wins cost long-term willingness. [Majalis itch.io thread]

### Avoiding stat-grind feel in repeat interactions

**19. Emily Short — opacity kills engagement.** Quote: *"the character trait system may have been doing important things, but it was opaque enough that eventually I started to ignore it."* Craft rule: if the player can't see the stat move, the stat isn't narrative — it's noise. Make every tick visible, either numerically or through a sensory line. [Emily Short, on Regency Love]

**20. Short — generative player creativity as antidote to grind.** Quote: *"creative ownership"* — players fill in detail beyond explicit choices. Translation: don't write every variation; write the *frame* + a few variations, and let the player's imagination do the nesting. Works because long-form adult games trade on private imagination anyway. [Short on Hollywood Visionary]

**21. Short — procedural text generation toolkit (2014 essay).** Four concrete variation mechanisms: (a) **`[one of]…[as decreasingly likely options]` / `[sticky random]`** — Inform's text cycles for NPC idles; (b) **clause composition** — assemble individual action clauses then combine intelligently (Savoir-Faire pattern); (c) **state-aware selection** — rules about what details merit mention based on world-model state; (d) **person/tense shifts** — refresh long sequences by changing narrator position, not just words. [Short's procgen essay]

**22. Lab Rats 2 — opinions revealed through interaction, not listed upfront.** NPCs' opinions (likes/dislikes) are *hidden* at first meeting and reveal as the relevant interaction triggers them. Creates a "discovery curve" for each NPC that resists the min-max shortcut. [LR2 character_guide snippets]

**23. Lab Rats 2 — personality-clustered opinion inheritance with override slots.** Characters sharing the same personality share many opinions (cheap authorship); each personality adds private "titles" for self and for you (cheap uniqueness). Authoring pattern: two hand-authored layers (personality archetype + per-NPC overrides) produce the appearance of N unique voices. [LR2 character_guide]

**24. LR2 — object/setting-mediated sluttiness.** What a girl will do on a park bench differs from what she'll do in her own bedroom. Obedience-high girls respond to commands; slutty-high girls prefer to lead. Text variation is thus 3-axis (NPC state × setting × lead-type), which avoids the "60 lines per NPC" trap by multiplying instead of enumerating. [LR2 wiki summaries]

### Economic pressure as narrative

**25. Vren's business loop as narrative pressure pump, not minigame.** Money is the reason the PC does research she wouldn't otherwise do, which is the reason the corruption loop has access to new serums. The economy narrates the escalation. Without the cashflow crunch, there's no in-character justification for tier-3 serums — the narrative wants them because the P&L needs them. [Vren gameplay loop post]

**26. DoL — status/class as structural vulnerability (not a number).** Quote: the PC's victimization rate isn't "violence saturating the town equally," it's her social position (abandoned youth, no parental protection) leaving her exposed. Economic/class pressure is narrated *structurally* rather than as a grind meter — she can't decline the only job that pays because there's no safety net scripted to catch her. [Sad Girl Theory interview]

### Moment of self-recognition

**27. DoL Traits — narrative echoes of accumulated acts.** Traits (acquired via repeated matching acts) change flavor text *across the game*, not just in trigger scenes. The PC starts noticing her own patterns — the self-recognition isn't authored as a dramatic monologue; it's distributed across dozens of later scenes where the prose *acknowledges* what she's become. [DoL Traits wiki]

**28. Current Condition / Attitudes — PC self-description shifts.** The game's descriptive strings for the PC's current state update based on the cumulative stat profile. The PC literally gets described differently to the player as she changes. Craft lesson: the "I've changed" moment isn't a scene — it's the slow realization that the text has been describing a different person for a while now. [DoL Current Condition wiki]

**29. Robert Yang — inverse kinematics as "learning the other person."** Tactile mini-mechanics (scrubbing in the right places) encode *discovery of preferences* as gameplay. The self-recognition runs the other way too — "what I now know about them" is the narrative payload, proceduralized. [Gamedev.com intimacy article]

---

## Deep Read Notes

### Sad Girl Theory × Vrelnir (2022)
Three load-bearing claims the designer makes explicit:
1. **Control is the resource; Trauma is the antagonist.** Incremental, not binary. PC agency is modeled as her capacity to *transgress upward* — which is a thornier and more honest model of how trauma survivors actually cope than "virtue meter falls."
2. **The game's consent is meta.** Player-to-game consent ≠ PC-to-scenario consent. Vrelnir refuses to make all encounters consensual because collapsing the two levels would erase what the PC's resistance *means*.
3. **Structural analysis via systems, not speeches.** Vrelnir admits "I'm not educated at all on it" re: structural violence, but the game's institutions (school discipline, police, orphanage) are modeled as closed hierarchies with no appeal — players *experience* the critique through exhaustion of options.

### Emily Short — Interactive Romance category
Core transferable craft:
- **Team mechanics dilute singular-repository-of-virtues problem.** Black Closet: "you are not alone." Applying to adult games — NPC coteries, roommates, rivals add texture that 1-on-1 romance arcs lack.
- **Opacity is the killer.** A hidden trait system is functionally off.
- **Dialogue density matters but shape matters more.** Regency Love had "lots and lots of talking" but "slightly peculiar choices" in how the talking branched — Short's implicit rule: volume can't compensate for structural clunkiness.
- **Generative ownership** — under-specified moments let the player's imagination finish the scene; over-specified moments feel like puppetry.

### Emily Short — Procedural Text Generation in IF (2014)
Four mechanisms, all directly applicable to adult-game repeat-visit variation:
1. `[one of]...[sticky random]` for idle/ambient text (NPC background behavior).
2. Clause composition — assemble per-event clauses, combine intelligently per temporal/state rules (prevents "she did X. she did Y. she did Z." flat lists).
3. State-aware selection via Room Description Control — rules about which details merit mention.
4. Person/tense shifts for long sequences — re-frame the narrator instead of re-wording the sentence.

### Gamedev.com — Ways of Designing Intimacy
Five operational rules extracted:
- Reject the "kindness coin" — romance as side-quest with pre-set unlock kills it (Robert Yang).
- Design through **meaningful verbs** — silence, scrubbing, caressing, washing (Sharang Biswas).
- **Physicality + feedback loops** teach preferences via gameplay (*Rinse and Repeat HD*).
- **Real-time schedules** make intimacy about showing up, not grinding stats.
- **Art direction** — eroticism lives in the image and the viewer's imagination, not in explicit depiction.

### Course of Temptation v0.7.7 devlog (Anthaum)
Rhythm discipline: the author openly distinguishes "under-the-hood coding work" patches from content-and-roadmap patches. Texting chain prototype was this month's engine investment — next month's content leans on it. Implication for our pipeline: long-form adult-game production requires explicit phase-flagging so content doesn't outrun engine, and engine doesn't rot without content validating it.

### Majalis (Tales of Androgyny) — combat design thread
The designer (Majalis) is careful *not* to frame combat-sex as penalty. Persuasion, taunting, theatric feints share the decision tree with sexual outcomes. Combat was originally a SFW turn-based system; sexual outcomes were layered onto it as *additional resolutions*. Means: the combat-sex interface isn't "you lost, here's a scene" — it's "one of N resolutions, conditioned on PC willingness." Aligns with the consent-is-continuous craft rule.

---

## Gaps

- **No fetch of Vrelnir's actual Writer's Guide body.** The gitgud wiki returned gateway content, not full markdown. Captured intent via interview + wiki corpus. Recommend manual fetch through browser context if deeper stylistic rules (specific sentence-level dos/don'ts, banned phrasings, sensory-density targets) are wanted.
- **Miraheze wiki cluster (DoL, CoT, ToA) all returned 403 to WebFetch.** Search snippets gave enough to extract mechanics; for full Traits enumeration, Trauma thresholds, and Bodywriting rules, a direct browser read is needed.
- **Vren's design-blog posts on Patreon are 403-walled.** The core "gameplay loop of Lab Rats 2" post is cited here via search snippets only — Vren has written more substantial design essays behind Patreon that this task did not reach. Highest-value unread: Vren's Trance design post and his "opinions vs personalities" post.
- **Splendid Ostrich (Newlife) design writing is almost entirely Patreon-gated.** Itch.io blog has release notes, not craft. The game is perhaps the most serious transformation-sim in terms of character-arc writing, and its design discourse is the single biggest blind spot of this pass.
- **No primary-source data from TFGames forums.** TFGS threads are gated by account login for serious discussion forums, and do not index well. A forum-scraping pass (authenticated) would surface at least 3–5 more technique threads on "writing the corruption arc" that I know exist by reputation but couldn't retrieve.
- **No r/lewdgames, r/CHYOA, or Reddit adult-game subthread captures.** Generic searches did not surface the craft-discussion threads specifically. A targeted Reddit-API pass would be needed.
- **Jason Rohrer and Adrienne Shaw citations** — mentioned in the prompt for adjacent craft perspective (game-as-autobiography, sexuality in games) — not retrieved. Shaw's work is academic and likely worth a separate pass if the frame of "serious-treatment of adult content" needs theoretical backing.
- **Choice of Games editorial guidelines for Heart's Choice** are internal/sent-to-accepted-authors. Public-facing page is promotional. Anyone with an author contact there could get the actual doc.
- **NarraScope 2019 program** mentioned interactive-erotic-fiction panels — the talk recordings/notes may have additional craft material not captured here.

---

## Short synthesis for downstream use

The strongest single craft rule that recurs across every serious source: **don't let the corruption arc be one number going up.** Every major design statement — DoL's Control/Trauma/Awareness/Promiscuity/Exhibitionism/Deviancy split, LR2's three-loop model, CoT's inclinations, Short's opacity warning, Clough's scene-function framing — points at the same thing: corruption is a *shape*, not a magnitude, and the shape is what makes the transformation feel like a story instead of a spreadsheet.

The second strongest: **the "I've changed" moment is distributed, not staged.** DoL's Traits and Current Condition, CoT's NPC memory and rumors, Yang's real-time showing-up schedule — all push recognition into ambient text that runs *across* scenes. Long-form adult games that try to stage the realization as a single dramatic beat fail; games that let the player realize weeks later, in passing, that the descriptive text has been calling her something different for a while — those land.
