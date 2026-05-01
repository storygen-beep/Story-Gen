# Task D — Interactive Fiction Craft Techniques

Research extract of concrete, teachable craft from the published writings and talks of key IF/narrative-game designers. Organized by Sources → Findings (numbered techniques) → Deep Read Notes → Gaps.

---

## Sources

1. Emily Short — "Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures" (2016). https://emshort.blog/2016/04/12/beyond-branching-quality-based-and-salience-based-narrative-structures/
2. Emily Short — "Storylets: You Want Them" (2019). https://emshort.blog/2019/11/29/storylets-you-want-them/
3. Emily Short — "Pacing Storylet Structures" (2020). https://emshort.blog/2020/01/21/pacing-storylet-structures/
4. Emily Short — "Mailbag: Deep Conversation" (2018). https://emshort.blog/2018/09/11/mailbag-deep-conversation/
5. Emily Short — "Conversation" (article index / IF Theory chapter). https://emshort.blog/how-to-play/writing-if/my-articles/conversation/
6. Emily Short — "IF Comp 2012: howling dogs (Porpentine)" (2012). https://emshort.blog/2012/10/10/if-comp-2012-howling-dogs-porpentine/
7. Richard Evans & Emily Short — "Versu—A Simulationist Storytelling System" (2014 paper). https://www.semanticscholar.org/paper/Versu%E2%80%94A-Simulationist-Storytelling-System-Evans-Short/74c6364ae004ce58e3f15a20c1e6d22198a93e21
8. Dan Fabulich / Choice of Games — "7 Rules for Designing Great Stats" (2011). https://www.choiceofgames.com/2011/07/7-rules-for-designing-great-stats/
9. Choice of Games — "5 Rules for Writing Interesting Choices in Multiple-Choice Games" (2010). https://www.choiceofgames.com/2010/03/5-rules-for-writing-interesting-choices-in-multiple-choice-games/
10. Choice of Games — "A Taxonomy of Choices: Establishing Character" (2017). https://www.choiceofgames.com/2017/12/a-taxonomy-of-choices-establishing-character/
11. Jon Ingold / inkle — "The Problem of Failure" (Medium, inkle studios). https://medium.com/@inklestudios/the-problem-of-failure-518ec9c1c53e
12. Jon Ingold — "Narrative Sorcery: Coherent Storytelling in an Open World" GDC 2017. https://archive.org/details/narrative-sorcery-coherent-storytelling-in-an-open-world
13. D S Wadeson / Jon Ingold — "Introduction to Ink". https://medium.com/game-writing-guide/introduction-to-ink-3e6c224865f8
14. Meg Jayanth — "Forget Protagonists: Writing NPCs with Agency for 80 Days and Beyond" (GDC 2016; Medium). https://medium.com/@betterthemask/forget-protagonists-writing-npcs-with-agency-for-80-days-and-beyond-703201a2309
15. Chris Avellone — "Project Eternity and Characterization" (Obsidian forum blog). https://forums.obsidian.net/blogs/entry/168-project-eternity-and-characterization/
16. Brian Mitsoda — "Plot is Gameplay's Bitch" interview (tom-jubert.blogspot). http://tom-jubert.blogspot.com/2010/08/brian-mitsoda-talks-vampire-bloodlines.html
17. Ron Gilbert — "Why Adventure Games Suck" (Grumpy Gamer, 1989 reprint). https://grumpygamer.com/why_adventure_games_suck/
18. Porpentine — "Uses This" interview. https://usesthis.com/interviews/porpentine.heartscape/
19. Aaron Reed — "2012: Howling Dogs" (if50). https://if50.substack.com/p/2012-howling-dogs
20. Sam Barlow — interviews on Her Story / Immortality (NME, indienova, Hollywood Reporter). https://www.nme.com/features/gaming-features/the-path-to-immortality-sam-barlow-on-reviving-fmv-games-pokemon-snap-and-70s-brit-perv-filmmakers-3224955

---

## Findings (25 craft techniques)

### Narrative Architecture

1. **Emily Short's "quality-based narrative" (QBN)** — Replace boolean branching with numerical qualities that gate scene availability. A scene's prerequisite is not "visited X" but "quality_reputation >= 3 AND quality_clues_found >= 1." Qualities are written once; new scenes slot in without re-threading the graph. Critical for episodic/long-lived content. [1][2]

2. **Short's "salience-based narrative"** — Instead of picking the *next* scene, the engine picks the scene that *best fits* the current world state. Content is tagged with conditions like `(location=kitchen, pantry=empty)` and the system scores every candidate against the state, firing the most-salient one. Equal-salience pool fires randomly; less-salient content is fallback. Ideal for low-consequence dialogue layers on top of a spine. [1]

3. **Short's "waypoint narrative"** — Dialogue is attached not to topics but to *transitions between topics* (A→B, B→C). The engine pathfinds through the topic graph toward a trigger topic; already-used transitions are negatively weighted so NPCs don't loop. Player input can divert the route without breaking structure. [1]

4. **Storylet = content + prerequisites + effects** — Short's canonical three-part unit. Content is the passage/animation/dialogue fragment; prerequisites are world-state conditions; effects mutate state on exit. Everything else (progress stats, menace wheels, sorting hats) is a pattern *on top of* this triad. [2]

5. **Branch-and-bottleneck pattern** — Short's pacing rule: let branches diverge mid-scene but funnel players back to shared "bottleneck" beats before the next story peak. Preserves authored climaxes while permitting local variance. Maps 1:1 onto Ink's diverts-and-gathers. [2][3][13]

6. **Ink's weaves / knots / stitches / gathers** — A knot is a scene; a stitch is a sub-scene; a divert (`->`) jumps; a gather (`-`) is the reconvergence line that all branches above it fall through to. "Most story state is shared, only a few threads are properly divergent" — so word count stays tractable while characterization accumulates. [13]

### Pacing

7. **Short's "alternating freedom & constraint"** — Open, free sections feel *less* intense; climactic beats need tighter constraint. Deliberately alternate to keep the rhythm from going stale: exploratory storylets → narrow cliffhanger → exploratory. [3]

8. **"Cost-as-deceleration"** — Put resource requirements at the *start* of a storyline, not the end. The player has to leave the plot to go grind/gather, which paces the narrative automatically without the author writing filler. [3]

9. **"Rhombus acceleration passages"** — Before a climax, squeeze the choice set down to a linear minimal-choice sequence ("rhombus" = wide → narrow → point). This creates felt acceleration; it's the structural opposite of exploratory sandbox time. [3]

10. **"Menace wheels"** — Partially randomized "you got caught / you got sick / a patrol passed" events that absorb failure without blocking forward progress. Keeps systemic games from dead-ending while still punishing. [3]

### Characters & NPC modeling

11. **Versu's typed social memory** — NPCs don't remember events generically; they remember *typed social moves* ("insulted me", "flirted with me", "confided in me"). Future dialogue is gated on the type, not the event. A character who was insulted last scene has "insulted_me(player)=true" and all their lines consult it. [7]

12. **Social practices as coordination** — Versu's top-level innovation: autonomous agents don't plan against each other; they *share a social practice* (a dinner party, a courtship) that defines valid moves and expected responses. Characters stay coherent because the practice, not the agent, knows what's appropriate. [7]

13. **Avellone's "companion checklist"** — Every party NPC must tick: (a) combat-viable, (b) thematic resonance with the game's premise, (c) ego-stroking reactivity (barks, romance, comments on player actions), (d) distinct visual + vocal identity, (e) environmental barks on location/event changes, (f) mechanical niche not overlapping others. Miss any and players drop them. [15]

14. **Avellone's "reactivity is out-of-sequence storytelling"** — True companion reactivity means telling several stories in parallel, triggered by what the player did, not a fixed beat order. The companion's "story" is really N fragments, each gated on player action. [15]

15. **Mitsoda's "invisible stats rule"** — "I'd rather the player see as little dialogue, floating numbers, chart-o-graphs as possible." Relationship progress is measured by *in-game NPC responses*, not friend-o-meters. No UI number for disposition; the dialogue itself *is* the number. [16]

16. **Mitsoda's dialogue-disposition flagging** — Bloodlines' NPCs have an internal mood flag that drives animation behavior and response selection. Writers write for mood columns; the flag is hidden from the player but gates which column fires. Effectively a salience tag. [16]

17. **Mitsoda's clan/background column** — The Malkavian playthrough is a parallel column in the same dialogue tool: every line has a Malkavian variant. Treat PC background as a view onto the shared scene, not a separate script. [16]

18. **Jayanth's "NPC refusal as structure"** — The Murri girl in 80 Days *refuses* Passepartout's help because he's aligned with her oppressor. Refusal isn't an error state; it's a first-class design primitive. Build situations where the protagonist's privilege is a *barrier*, not an asset. [14]

19. **Jayanth's "contradictory NPC worldviews"** — Build worldbuilding *through* NPC disagreement, not through a bible doc. "Almost every NPC has a slightly different opinion of the Artificers' Guild." The world's reality is the envelope of those contradictions. [14]

20. **Jayanth's "some NPC stories aren't for the player"** — Preserve privacy. Ask "how much of this is for the player?" and deliberately leave chunks of NPC life inaccessible. The reality of the character is what the player *can't* see. [14]

### Choices, stats, player expression

21. **Choice of Games' "stats must characterize, not just gate"** — Fabulich's Rule 1+2: stats aren't a skill list; they're personality traits ("Calmness", "Cynicism") that have no right answer and express roleplay. If strength is just a lockpick-check, cut it. [8]

22. **Fabulich's "opposed stat pairs"** — Rule 6: avoid dominant-stat collapse by pairing (Cunning vs Honor, Ruthlessness vs Compassion). Every raise of one is a tradeoff, so no build dominates and no run is redundant. [8]

23. **Choice of Games' "every option must have real consequences"** — Rule 1 of interesting choices. If the fork is cosmetic, either cut it or promote it to a fake-choice *that the player will never detect as fake*. Uncovered fake choices read as cheating. [9][10]

24. **Choice of Games' "motivated forking"** — When a binary decision has two motivations (e.g. keep evidence *for the case* vs keep it *for personal blackmail*), add the variant as a third option that writes a *different* personality stat. Same fork, distinct characterization. [10]

25. **Choice of Games' "objective choices with trade-offs"** — Pair every Secondary-Variable gain with a narrative cost (attend the family dinner → your street rep drops). Prevents specialization from solving the dramatic tension the stat was supposed to create. [10]

### Prose-per-click, hypertext, structural devices

26. **Porpentine's variable-density link placement** — Links as single words, as punctuation, as embedded phrases, as explicit commands. Density varies per passage to control whether reading feels constrained, open, or laborious. The rhythm of *clicking* is a formal device, independent of plot. [6][18]

27. **Porpentine's "illusory choice as mood"** — The wording of options differs but the story proceeds identically. The *act* of choosing expresses hesitation or complicity rather than changing anything. Click-as-emotion, not click-as-fork. [6][19]

28. **Porpentine's "links as the sentence"** — Sentences stop mid-word, waiting for a click to finish the thought. The hypertext isn't a UI on top of prose; it *is* the prose's grammar. [19]

### Failure

29. **Ingold's "no fail state, only compromised understanding"** — Heaven's Vault has no fail screen; your translations are always "at least a bit wrong," and you proceed under degraded knowledge. Failure becomes an invisible tax on the story you experience, not a reset. [11]

30. **Ingold's "degraded protagonist as narrative"** — A Highland Song's design goal: keep the protagonist "soaked through and on the edge of hypothermia" without dying. Hardship becomes a persistent prose-state, not a life bar. [11]

31. **Ingold's "contradiction accounting"** — In Overboard! your own lies are tracked, so NPCs can confront you: "You said Malcolm's in your cabin? But you told me earlier…" Failure fuels dramatic tension instead of rollback. [11]

### Design rules for agency

32. **Gilbert's "Why Adventure Games Suck"** (selected) — (a) clear end objective from the start; (b) present the problem *before* the solution (no backward puzzles); (c) no penalty for items you couldn't have known to pick up; (d) reward intent, not typing: generous synonym parsing, proximity matching; (e) avoid "caging" — offer multiple paths instead of single-solution bottlenecks. [17]

### Non-linear structure

33. **Barlow's "fragment as autonomous unit"** — Her Story's 271 clips each stand alone as a narrative object; meaning emerges from juxtaposition. The player, not the author, orders them. Works when each fragment is independently coherent. [20]

34. **Barlow's "keyword as excavation tool"** — Search-as-interface: you type what you think matters and the corpus returns clips. Turns the act of *asking the right question* into the central mechanic. [20]

35. **Barlow's "match cut" navigation** — Immortality lets you click an object in a frame and jump to another scene containing that object. The film-editing technique becomes a player verb. Generalization: any visual/textual token on screen is a potential portal. [20]

---

## Deep Read Notes

### Emily Short — the three structural families [1]

Short's 2016 taxonomy is the field's reference framework:

- **Quality-based (QBN)** — numeric qualities, used by Fallen London/StoryNexus. Authors bookkeep progress flags (A-available → A-complete → B-available). Heavy tracking cost; extremely modular and DLC-friendly.
- **Salience-based** — rule-based content selection, used in Left 4 Dead's Director, Versu, Firewatch ambient dialogue. Low consequence per utterance; content pool must be authored for overlap so the system always has a good pick.
- **Waypoint-based** — transition-tagged dialogue, dynamically routed. Best model Short gives is conversation-as-graph-search. Player "surfaces the subtext" by bringing up topics NPCs resist. This is the structural argument for why "good" dialogue systems feel improvisational.

### Storylets [2][3]

The storylet definition (content + prereq + effect) is Short's tightest formulation and the one most useful to a generator pipeline: every "scene" we emit should be expressible as this triple. Short's pacing essay [3] is the companion piece — storylets alone are shapeless without a layer that alternates freedom/constraint, and without cost-as-deceleration you get a puddle of options with no arc.

Concrete pacing scaffolding from [3]:
- **Progress stat** — a counter the main plot advances by (Act I / Act II / Act III). Gates story-spine storylets.
- **Menace stat** — jeopardy level. When it hits threshold, the menace wheel fires (partially random setback storylets).
- **Familiar-mechanic breather** — before a climax, give the player something they've already learned (travel scene, known mini-system). Builds anticipation without new cognitive load.

### Versu / Character Engine [7][11]

Versu's key insight is the *social practice* — a script-like data structure defining the moves available in a context (dinner party, job interview, duel). Agents select moves from the practice by consulting their emotional/relational state. This is materially different from a dialogue tree because:
- multiple agents consult the *same* practice, giving coordination
- the practice makes "what's appropriate right now" machine-checkable
- a new agent dropped into the practice behaves sensibly without author-written lines for that combination

Typed memories in Versu: not "Alice remembers she saw Bob at 3pm" but "Alice has flag `insulted_by(Bob)=true`." Dialogue lines say "if insulted_by(speaker) then <cold response>". This maps to our flag system but with the twist that the flag is *typed* — SugarCube flags should model "Alice was flirted_with_by Player" not "Alice remembers flirt_scene_17".

### Meg Jayanth — NPCs with Agency [14]

Her central move: treat NPC agency as ethics, not nicety. Three structural techniques:
- **Refusal** — NPCs can say no to the protagonist and you have to reroute. The refusal becomes the content.
- **Independent goals** — NPCs pursue their plans regardless of player approval. Dragon Age II's Anders blows up the Chantry even if you're romancing him; this is a feature, not a bug.
- **Disagreement as worldbuilding** — don't write a bible; let NPCs contradict each other. The player derives the world from the envelope of views.

Applied to our system: every NPC should own a *goal* that runs in parallel to player action and completes (or fails) on its own schedule. They're not vending machines for content; they have an errand list.

### Choice of Games writing doctrine [8][9][10]

Three essays form a single house style:
- **Stats as characterization, not skills.** Opposing pairs; every stat must both *express* a trait AND *gate* content.
- **Choices have real consequences.** No dominant option. Fake choices only when they're invisible.
- **Establish character via choice taxonomy.** Primary (stats-affecting), Flavor (cosmetic recall), Fake (invisible flavor), Motivated Forking (same fork, different personality-write), Objective with Trade-off (gain + cost paired).

The Motivated Forking rule [10] is unusually actionable: wherever we have a binary, look for a *third option with the same outcome but a different motive*. Same narrative result, richer personality variable.

### Ingold on failure [11]

Inkle's formal position: failure is content, not state loss. Five specific techniques:
- no fail screens; degraded outcomes
- persistent damage/status as narrative color
- contradiction tracking (your past lies become NPC ammunition)
- rewinds that are available but *discouraged*
- failures within a single run compound into new situations rather than resetting

This is the anti-VN thesis: don't give the player a branch point with a "right" answer and a game-over; give them a path that keeps walking forward in a worse version of the world.

### Porpentine — prose pacing via link density [6][18][19]

Porpentine's craft innovation is making the click itself expressive. Variable link density per passage = variable reading speed. Words mid-sentence that end in a link force a pause. Choices that are functionally identical but *worded* differently make the player *feel* the choice without branching the tree.

This is the counter-argument to heavy branching: you can get emotional texture from hypertext without touching state.

---

## Gaps

- **Ron Gilbert on dialogue trees specifically.** His "Why Adventure Games Suck" is about puzzles; his blog posts on *Return to Monkey Island* mention a custom language called Yack but I didn't find a public design essay on how to write branching dialogue. Probably in his podcast/interview corpus rather than the blog.
- **Meg Jayanth's actual GDC 2016 talk transcript.** The Medium essay [14] is a good proxy but the talk has more examples. Full video at https://www.youtube.com/watch?v=FLtATD6CF0E — not fetched for time.
- **Jon Ingold's "Narrative Sorcery" full talk.** The archive page [12] only gave me the abstract. YouTube video at https://www.youtube.com/watch?v=HZft_U4Fc-U — recommend extracting "defensive logic" details from the full talk.
- **Leigh Alexander and Cara Ellison.** Both write more *about* games than they publish systematic craft essays. Ellison's *Embed With Games* is the closest to a craft text but it's anecdotal. Alexander's Reigns: Her Majesty design docs are not public. Not a rich lode for our purposes.
- **Jason Grinblat / Caves of Qud.** His talks (GDC 2018 "Procedurally Generating History"; Roguelike Celebration 2016 "Markov by Candlelight") are on YouTube/GDC Vault but deal more with procgen than with the *writing craft* of individual scenes. Procgen thinker, less relevant to prose-per-click.
- **Fallen London specific storylet design.** Short's general posts [1][2][3] cover the pattern, but Failbetter's internal style guide (if it exists publicly) would be denser. Didn't surface.
- **Chris Avellone's specific Planescape dialogue techniques.** Found the companion principles [15] but not his longer-form writing on the *line-level* craft of Torment dialogue. Blog is fragmented across Obsidian forums.
- **Brian Mitsoda on Dead State / Bloodlines 2.** The RPS interview [16] is the canonical one; follow-up interviews exist but are mostly promo.

Sources most worth a deeper pass next round: **Short's Versu paper [7]**, **Ingold's full "Narrative Sorcery" video [12]**, and **Jayanth's GDC 2016 video**. Those three together would roughly double the concrete-technique yield of this task.
