# Task B — Life-Sim & Schedule-Based Narrative Design

Research target: concrete, teachable narrative-design techniques from life-sim, schedule-based, and storylet-driven games where repeated daily activity carries character-arc progression. Pulled from designer-authored writing (Kennedy, Short, Ingold, Martin), named-designer interviews, and structural breakdowns — filtered away from reviews/plot-recaps/impressions.

## Sources

[1] Emily Short. "Storylets: You Want Them." *Emily Short's Interactive Storytelling*. 2019-11-29. https://emshort.blog/2019/11/29/storylets-you-want-them/ | Source-Type: designer-blog | As Of: 2026-04-21 | Authority: Short is the co-designer of Versu and Failbetter's Creative Director as of 2020 — canonical primary source on storylet craft.

[2] Emily Short. "Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures." *Emily Short's Interactive Storytelling*. 2016-04-12. https://emshort.blog/2016/04/12/beyond-branching-quality-based-and-salience-based-narrative-structures/ | Source-Type: designer-blog | As Of: 2026-04-21 | Authority: Primary taxonomy used by most IF designers since; cited in GDC talks.

[3] Alexis Kennedy. "I've stopped talking about quality-based narrative, I've started talking about resource narrative." *Weather Factory*. https://weatherfactory.biz/qbn-to-resource-narratives/ | Source-Type: designer-blog | As Of: 2026-04-21 | Authority: Kennedy founded Failbetter Games, wrote Fallen London and Sunless Sea, now runs Weather Factory (Cultist Simulator, Book of Hours). Canonical primary source.

[4] Richard Moss. "Sunless Sea, 80 Days and the rise of modular storytelling." *Game Developer* (Gamasutra). https://www.gamedeveloper.com/design/-i-sunless-sea-i-i-80-days-i-and-the-rise-of-modular-storytelling | Source-Type: editorial-with-designer-quotes | As Of: 2026-04-21 | Authority: Direct quotes from Kennedy (Failbetter) and Ingold (inkle) on production mechanics.

[5] Bryant Francis. "How Citizen Sleeper was inspired by tabletop RPGs and gig work." *Game Developer*. https://www.gamedeveloper.com/business/how-citizen-sleeper-was-inspired-by-tabletop-rpgs-and-gig-work | Source-Type: designer-interview | As Of: 2026-04-21 | Authority: Gareth Damian Martin, sole designer of Citizen Sleeper.

[6] "An Interview With Citizen Sleeper Creator, Gareth Damian Martin." *Old Men Running The World*. https://oldmenrunningtheworld.com/an-interview-with-citizen-sleeper-creator-gareth-damian-martin/ | Source-Type: designer-interview | As Of: 2026-04-21 | Authority: Martin on Blades in the Dark, dice-first design.

[7] Leonhard Meyer. "Same but different — Comparing the Social Link System in Persona 3, 4 & 5." *Game Developer*. https://www.gamedeveloper.com/design/same-but-different---comparing-the-social-link-system-in-persona-3-4-5 | Source-Type: design-breakdown | As Of: 2026-04-21 | Authority: Structural comparison across the trilogy.

[8] "Unmasking the Depths of Persona 5." *Counter Arts / Medium*. https://medium.com/counterarts/the-psychology-behind-persona-5-3ee51e5f82b | Source-Type: design-analysis | As Of: 2026-04-21 | Authority: Secondary but structural; treats Confidants as writing, not mechanics.

[9] Megami Tensei Wiki. "Calendar / Persona 5." https://megamitensei.fandom.com/wiki/Calendar/Persona_5 | Source-Type: reference-wiki | As Of: 2026-04-21 | Authority: Structural truth of deadline-per-Palace design.

[10] Failbetter Games (quoted in Sam Goree). "Models of the Self in Disco Elysium." https://samgoree.github.io/2022/03/18/models-of-the-self.html | Source-Type: academic-adjacent blog | As Of: 2026-04-21 | Authority: Analyzes DE's individuated-stat model.

[11] "The Incredible System of Thought Cabinet in Disco Elysium." *Uncore*. https://uncore.substack.com/p/the-incredible-system-of-thought | Source-Type: design-breakdown | As Of: 2026-04-21 | Authority: Covers acquisition → internalization → effect loop.

[12] Ben Wessel. "Techniques of Thought: Cognition, Identity and Ideology in Disco Elysium." *Parallel Suns*. https://parallelsuns.com/blog/techniques-of-thought-cognition-identity-and-ideology-in-disco-elysium/ | Source-Type: design-analysis | As Of: 2026-04-21 | Authority: 403 on fetch but surfaces in search corpus; referenced for ideology-accretion.

[13] "These Heterogenous Tasks" review of Long Live the Queen. https://heterogenoustasks.wordpress.com/2014/12/13/long-live-the-queen/ | Source-Type: design-critique | As Of: 2026-04-21 | Authority: Sam Kabo Ashwell — narrative-design writer, IFComp judge; his "branch-and-bottleneck" terminology is canonical.

[14] "Kentucky Route Zero, Dialogue and 'Choice.'" *Albatross Junkyard*. https://albatrossjunkyard.wordpress.com/2020/01/30/kentucky-route-zero-dialogue-and-choice/ | Source-Type: design-analysis | As Of: 2026-04-21 | Authority: Focused structural read of KRZ's non-mechanical choices.

[15] Stardew Valley Wiki. "Friendship" & "Modding: Dialogue." https://stardewvalleywiki.com/Friendship / https://stardewvalleywiki.com/Modding:Dialogue | Source-Type: community-reference | As Of: 2026-04-21 | Authority: Surfaces the actual trigger grid (heart level × location × time × weather).

[16] Jake Tucker. "Introduction to Ink (by Jon Ingold)." *Medium / Game Writing Guide*. https://medium.com/game-writing-guide/introduction-to-ink-3e6c224865f8 | Source-Type: designer-derived tutorial | As Of: 2026-04-21 | Authority: Summarizes Ingold's pacing-over-flowchart argument.

---

## Findings

### Storylet & quality structure

1. **Storylets are [content + prerequisites + effects] atoms.** Short's three-part definition: a storylet is a piece of content (line, scene, animation), a set of prerequisites gating when it can play, and a set of effects on world state after it plays. This is the atomic unit life-sims keep reinventing — "heart event," "Confidant scene," "storylet," "card," "vignette" are all the same three-part object. [1]

2. **Quality-Based Narrative (QBN) — storylets unlocked by numerical qualities.** Failbetter's invented term. A "quality" is any numeric variable — inventory ("bottles of laudanum"), skill ("Dangerous 4"), relationship ("Aunt-knowledge 12"), or story progress. Writing is then framed as: *what passage is the player hungry for RIGHT NOW given current qualities*, not *what scene comes next*. Collapses inventory, stats, and story-state into one data type. [1][2]

3. **Resource Narrative — Kennedy's 2020+ reframe of QBN.** Kennedy abandoned "QBN" because it erased the distinction between different *kinds* of qualities. Resource narrative explicitly differentiates scarce/reproducible/fungible resources (fuel, heat, coin, secrets, time) from story-state flags, and insists events should "emerge in a natural-seeming way from the combination of resource states" — drama from the interaction of the resource types, not from external drama-manager AI. Examples: *Sunless Sea*, *Cultist Simulator*, *XCOM*, *Darkest Dungeon*. [3]

4. **"Poetic design" over drama-management.** Kennedy rejects abstract drama-manager AI in favor of *selecting and designing resource interactions* such that drama is the emergent shape of the resource system. E.g., in *Sunless Sea* the Terror/Fuel/Supplies triangle generates desperation without any AI having to script it. [3]

5. **Salience-Based Narrative — engine picks content, not player.** Short's taxonomy: content is tagged with conditional requirements (location, state, prior events) and the system picks whichever entry is "most salient" to the current context. Used by *Left 4 Dead* (Elan Ruskin's dialogue barks), *Firewatch* (location-and-adjacent-object reactions), and by ambient NPC commentary in Stardew. Good for reactive emotional overlays; risky for dramatic arcs because salience ≠ pacing. [2]

6. **Waypoint Narrative — story pathfinds toward authored beats.** Short's third structure. Dialogue is not authored *at* topics but *on transitions between topics*, and the engine "pathfinds" the conversation toward authored "trigger topics" that advance the plot. Player can detour, but the system tries to "heal the story" back. Scales with added content rather than exploding. (Used in Short's *Glass*; technically related to how many conversation-heavy Twines degrade gracefully.) [2]

7. **Anti-pattern: time caves.** Short's explicit warning. A "time cave" is a purely branching structure where every piece of content depends on the exact path taken. Negates storylet value — you lose the ability to add content later without re-auditing all branches. Most student Twines are time caves. [1]

8. **Branch-and-bottleneck.** Ashwell's canonical term for LLTQ-style structures: wide divergence during "free" weeks, narrow convergence at scheduled crisis events where hidden-stat checks fire. Prevents combinatorial explosion while still letting the player's build determine success/failure *at the bottleneck*. [13]

### Time pressure, schedules, and the daily tick

9. **Deadline-per-arc instead of a global deadline (Persona 5).** *Persona 5* abandoned the P3/P4 final-boss calendar and instead attached a deadline to each Palace, framed in-fiction as the target villain's schedule. Stakes are character-specific ("we steal Kamoshida's heart before expulsion is finalized") rather than abstract ("the world ends in 90 days"). This makes day-count pressure feel like a noir clock on a case rather than a score timer. [9]

10. **Dual-slot day structure forces triage.** *Persona 5* gives the player a Day slot and an Evening slot and that's it. Triage — which Confidant, which dungeon push, which stat to grind — *is* the gameplay loop. The writing is calibrated to the knowledge that any given scene is displacing another potential scene. [9]

11. **Fixed-tick clock mechanic (Citizen Sleeper/Blades in the Dark).** Martin imported *Blades in the Dark*'s clocks directly: a visible segmented circle that fills through player action or automatic tick. "Clocks create a sense of dread, mystery and anticipation as they tick along." Each clock is a *countable narrative threat* — heat level, debt collector arriving, mushroom harvest ripening — giving the player a graphic handle on otherwise-abstract pacing. [5][6]

12. **Dice rolled at session start (Citizen Sleeper).** Rather than roll-on-action, Martin rolls all daily dice at wake-up and displays them as slots. Player sees their capacity for the day *before* deciding how to spend it. This makes every day feel like a distinct constrained puzzle. Drawn from the gig-economy metaphor: "waking up and being very aware of the limits of what you can offer in a single day." [5]

13. **Mood as a secondary slot-state (Long Live the Queen).** LLTQ adds a mood axis (four sliders) to the training calendar. A skill trained in the right mood gains a large bonus, but mood only shifts on weekends and drifts from external events. This creates a second planning layer on top of the schedule: *when* to train, not just what. [13]

14. **Heart Event Trigger Grid (Stardew Valley).** Events fire when `heart_level ≥ N` AND `location matches` AND `time-of-day matches` AND (often) `weather matches` AND prior events have/haven't fired. Crucially, dialogue *also* rotates every 2 hearts. The "alive" feeling is the product of many overlapping schedule tables — not one script tree. [15]

15. **Dialogue rotation tied to relationship threshold.** Every 2 hearts, Stardew's villagers' *default* conversational dialogue pool is rewritten. The player doesn't see a single "rank-up scene" — they notice Sebastian stops being terse in spring, then a week later mentions his sister. Relationship progress is felt through *ambient* text change, not only scripted cutscenes. [15]

### Character-arc-across-daily-life craft

16. **Tiered Confidant rewrites (Persona 5).** Each of a Confidant's 10 ranks is built around a *single small dramatic question* — "will Yusuke accept he was exploited by Madarame?", "will Makoto stand up to her sister?". The scene resolves that question; rank-up unlocks a new dialogue pool and an ability (Baton Pass, Follow-Up). 10 ranks = 10 mini-arcs nested under one macro-arc. [7][8]

17. **Removal of Reversal/Break in P5 vs P3/P4.** Persona 3 and 4 penalized neglect — Social Links could *reverse* (scenes played in bad faith) or *break* (lock the arcana). P5 cut this. Leftover "Doubt" assets in P5 show the team half-implemented and pulled it. Design read: forcing guilt on the scheduler-protagonist read as punitive; removing it let players experiment. [7]

18. **Hidden inner-stat gates (Courage/Kindness/Knowledge).** P3–P5 gate *access* to Confidant scenes on inner stats that are themselves raised through specific activities (read books → Knowledge, eat scary ramen → Courage). So writing a rank-4 scene, the author can assume "the player has already demonstrated mid-level Charm in the world" — the character arc is earned by proof-of-growth *outside* that character's storyline. [7][8]

19. **Confidants embedded in non-Confidant activities (P5).** New in P5: going to a diner with Makoto or studying with Ann advances their rank passively. "Progress toward the next ranking up can feel very natural" because the same activity serves two mechanical purposes (stat-up + Confidant points). Writing-side, scenes are *shorter* and *more ambient* than P4's standalone hangouts. [7]

20. **Customer-as-vignette (VA-11 Hall-A, Coffee Talk).** Each shift is a vignette where 2–5 customers cycle through the bar. A single customer's arc spans multiple visits; the *order* customers appear and who shares the bar at once produces juxtaposition. The only player lever is drink composition — no dialogue tree. Arc advances by whether their drink matched their mood. This is a radical storylet minimalism: one input per scene. [sources: search result cluster on VA-11 Hall-A/Coffee Talk]

21. **Drives replace central plot (Citizen Sleeper).** No main quest. Player instead accrues "Drives" — emotionally-named long-term goals (Growing Pains, Left Behind, Fleet). Each Drive is its own storylet chain with its own clocks. Ending is selected by which Drives the player closed, not by a final choice. Net effect: every ending feels player-authored even though each Drive is fully linear internally. [5][6]

### Characterization through mechanics

22. **Skills-as-voices (Disco Elysium).** Harry's 24 skills (Logic, Empathy, Electrochemistry, Inland Empire, Authority, Shivers…) are literally characters — they interrupt with their own voice and italicized barks during dialogue. A high-Empathy Harry is interrupted by Empathy more often than a low-Empathy one. Characterization is thus a *distribution* over interruptive voices, not a trait sheet. [10]

23. **Thought Cabinet — internalization timer as belief-formation.** Thoughts are *acquired* from repeated exposure to an ideology in dialogue, *equipped* to an empty cabinet slot (you have few slots), and *internalized* over many in-game hours. During internalization the thought imposes a stat penalty; on completion it flips to bonuses and adds/removes dialogue options wholesale. This is a mechanic for belief-formation-takes-time — you can't "choose communist"; you have to think the same thoughts long enough. [11][12]

24. **Ideology accumulation through dialogue-option selection.** Every minor dialogue choice tagged communist/fascist/moralist/ultraliberal moves counters. "Nearly every interaction, even the most minor, can subtly push the protagonist towards one political belief or another." At day 3, if any single ideology has crossed threshold *and* the relevant thought is internalized, a Political Vision Quest unlocks. Picking one locks the others — so the ideology is *performed* before it's *confirmed*. [12]

25. **Clothes-as-stat (Disco Elysium).** Clothing changes skill values because clothes genuinely change how people see and self-conceive. Mechanically identical to other RPGs' gear, but renamed and reframed: the "crit hat" is a stupid hat that makes Harry think bold thoughts because he's wearing a stupid hat. Trick is the *naming* — fiction-first item design. [10]

### Choice that isn't mechanical

26. **Non-mechanical dialogue (Kentucky Route Zero).** Dialogue options rarely change events or availability. Instead they change *who is speaking this line, about what, in what register.* Choice is framed as *stage direction* rather than *decision*. Removes the "optimize for good ending" anxiety and lets players speak expressively. KRZ scripts explicitly written to read like stage plays with stage directions. [14]

27. **Choice framed as "who the storyteller is."** KRZ often hands the player a line choice for an NPC whose internal life the player has no access to. "You are not choosing what the character does — you are choosing what kind of story this is." [14]

### Scope and production

28. **Modular production cadence (Sunless Sea).** Kennedy built Sunless Sea in Early Access as "3–5 islands per monthly update." Because each island was a near-isolated storylet bundle, cutting or delaying one didn't break the rest. This is both a writing pattern *and* a scope-management pattern: modular content enables modular shipping. [4]

29. **Freelancer-safe authorship.** Because modules are isolated, Failbetter and inkle can hire freelance writers (Meg Jayanth wrote 750k words on *80 Days*) who don't need to coordinate internal world-state with each other. Every writer owns a city/island end-to-end. The quality variable contract is the API. [4]

30. **Core loop over arc.** Kennedy: "the strength of the core loops. You leave port; you cross the darkness; you find the lights on the far side." In a life-sim, the day (or week) is the loop; the arc is what persists across loops. Writing should hit the loop shape every cycle even when the arc doesn't advance — or the day feels empty. [4]

---

## Deep Read Notes

### Deep Read 1 — Emily Short, "Beyond Branching" (2016) — the taxonomy that matters

Short's central move is to stop talking about "branching narrative" as one thing and split it into three mechanisms for the same question: *which piece of content do I show next?* Quality-based narrative answers *"whichever storylet's prereqs are satisfied, and the player picks from the available menu."* Salience-based narrative answers *"whichever piece of tagged content best fits the current state — system picks, not player."* Waypoint narrative answers *"whichever dialogue transition best pathfinds the conversation toward the next authored trigger topic."* Crucially she notes these combine: Fallen London is QBN-dominant but uses salience for ambient Echo flavor text; Firewatch is salience-dominant but uses waypoints for the main story beats. The design takeaway for life-sim is: **don't pick one; layer them.** Put the Confidant arc on QBN, put villager "I saw you in the mines today" barks on salience, and put major cutscene progression on waypoints. Short also lays out the storylet anti-pattern — "time caves," where every choice is path-dependent — and argues this eliminates the main benefit of the structure, which is *extensibility*: you should be able to write a new storylet next year and have it slot in. Time caves can't do that. This is why Fallen London can still ship new content 15 years after launch: the QBN contract between a storylet and the world-state is small and stable. A branching-novel engine couldn't. [2]

### Deep Read 2 — Alexis Kennedy, QBN-to-Resource-Narrative (Weather Factory blog)

Kennedy's retraction of his own coinage is the densest piece of craft writing in modern IF. His complaint against QBN: the word "quality" collapses three different things — an *inventory resource* (2 bottles of laudanum), a *character trait* (Dangerous 4), and a *story flag* (met the Vake). They behave completely differently in play: resources drain and replenish, traits grow and plateau, flags never go away. Treating them as one type ("a number the player has") leads to designers writing storylets that confuse the player about which number matters. His proposed replacement — **resource narrative** — insists that drama emerges from the *interaction of differentiated resource types*: the story is good when Fuel (consumable, scarce, reproducible) pushes against Terror (accumulating, non-fungible, hard to shed) pushes against Story (flag-like, permanent). He rejects drama-managers because drama-managers have to *decide* when the story is interesting. Resource narrative lets the *ratios* decide. The rule he gives: events "should emerge in a natural-seeming way from the combination of resource states." For a life-sim builder this is actionable: don't design a unified "affinity" stat — design 3+ resource types with different behaviors (reputation that drains, secrets that accumulate, trust that plateaus) and let scenes fire where their ratios form dramatic shapes. This is why Sunless Sea's terror-fuel-supplies triangle produces desperation without scripting, and why most romance-sim "affection meters" don't. [3]

### Deep Read 3 — Martin on Citizen Sleeper's clock+dice system (Game Developer)

Martin's design origin is tabletop: *Blades in the Dark* gave him clocks and "success at a cost," and zero-hour gig work gave him the metaphor. The key decision was to **roll all dice at the start of the day**, not at the moment of action. Mechanically this changes the psychology of the day — the player wakes up, sees five dice (say: 6, 5, 2, 1, 1), and now has to plan. A 6 is a luxury — that goes on the hard job. The 1s are survival dice — fetch water, take a cheap shift. Narratively this lets the game **describe the dice** ("today your body cooperates," "your implants are glitching"), turning a RNG state into characterization of the body. Clocks then layer over this: every Drive has 2–5 visible clocks ticking at different rates, filled by specific dice-slot placements. The player reads the whole day as a *constrained allocation problem* where the constraints *are* the story: "I only have one good die, and the debt-collector clock ticks tomorrow if I don't use it on Sabine." This is the mechanic doing all the work — the writing just has to name the clocks well. The transferable craft rule: **if you want a narrative mechanic to feel weighty, let the player see the budget** *before* they spend it. Hidden RNG feels unfair; visible RNG feels strategic; visible RNG with named stakes feels story-shaped. [5][6]

---

## Gaps

- **Famitsu / Atlus primary sources on Persona writing process.** Japanese-language design interviews (Hashino, Soejima) exist but didn't surface in English web search. Finding one would upgrade the P5 findings from structural-inference to canonical.
- **Failbetter internal style guide / writer handbook.** Known to exist; referenced in Kennedy's GDC talks. Not publicly linkable. Would pin the Fallen London storylet-sizing conventions ("no more than 4 branches per storylet").
- **ConcernedApe's design notes on Stardew heart-event grid.** None found. The trigger grid is reverse-engineered from the Stardew wiki. Eric Barone's own framing is absent.
- **VA-11 Hall-A / Coffee Talk designer interviews.** Sukeban Games and Toge Productions have given interviews but none surfaced with structural craft claims. Relied on inference from play-writing.
- **Kentucky Route Zero dev interviews on non-mechanical choice.** Vice/Funambulism pieces exist but weren't deep-fetched; craft claims come from secondary Albatross Junkyard analysis.
- **Jon Ingold GDC 2015 "Writing for Heaven's Vault / 80 Days" talk.** Referenced in search; transcript/recording not pulled. Would tighten findings on pacing-vs-flowchart and the "improv frisbee" principle he describes.
- **Harvest Moon / Story of Seasons design history.** Japanese design lineage of heart events pre-Stardew is poorly documented in English. Trigger-grid is structurally similar but origin-point is hazy.
- **Princess Maker 2 primary design material.** Gainax-era Japanese materials from the 90s are effectively unreachable via web search. All claims are via LLTQ-as-descendant.
- **Thought-Cabinet internalization timer math.** Uncore piece surfaces the *existence* of the timer but not the actual hour-values per thought or the stat-penalty tuning. ZA/UM never published it; would require game-file inspection.
