# Task F — Variant Prose Techniques for Repeatable Scenes

Concrete craft and engineering techniques for writing a scene that repeats (same location, same NPC, same activity) but reads differently at different stages of a character arc. Scope: QBN/salience narrative, Ink/80 Days, Hades barks, Left 4 Dead Response System, Subcutanean's "quantum text," and close-third fiction craft (Munro, Chekhov via Saunders).

---

## Sources

1. Emily Short — "Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures" https://emshort.blog/2016/04/12/beyond-branching-quality-based-and-salience-based-narrative-structures/
2. Emily Short — "Storylets: You Want Them" https://emshort.blog/2019/11/29/storylets-you-want-them/
3. Emily Short — "80 Days (Meg Jayanth / inkle)" https://emshort.blog/2014/08/05/80-days-meg-jayanth-inkle/
4. Failbetter Games — Fallen London Writer Guidelines III https://www.failbettergames.com/news/fallen-london-writer-guidelines-part-iii
5. Failbetter Games — "Narrative Snippets: StoryNexus Tricks" https://www.failbettergames.com/news/narrative-snippets-storynexus-tricks
6. Inkle — "Writing with Ink" (official docs) https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
7. Inkle — 80 Days press kit https://www.inklestudios.com/press/80days/
8. Inkle — "Open sourcing 80 Days' narrative scripting language: ink" https://www.gamedeveloper.com/design/open-sourcing-80-days-narrative-scripting-language-ink
9. Jon Ingold GDC 2015 — "Adventures in Text" https://archive.org/details/GDC2015Ingold
10. Jon Ingold GDC 2017 — "Narrative Sorcery: Coherent Storytelling in an Open World" https://archive.org/details/narrative-sorcery-coherent-storytelling-in-an-open-world
11. Elan Ruskin GDC 2012 — "AI-driven Dynamic Dialog through Fuzzy Pattern Matching. Empower Your Writers!" slides https://steamcdn-a.akamaihd.net/apps/valve/2012/GDC2012_Ruskin_Elan_DynamicDialog.pdf
12. Valve Developer Wiki — Response System https://developer.valvesoftware.com/wiki/Response_System
13. Greg Kasavin GDC 2021 — "Breathing Life into Greek Myth: The Dialogue of Hades" https://www.gdcvault.com/play/1026975/Breathing-Life-into-Greek-Myth
14. GamesHub — "Hades' Greg Kasavin breaks down Supergiant's unique approach to narrative" https://www.gameshub.com/news/features/hades-greg-kasavin-breaks-down-supergiants-unique-approach-to-narrative-262459-2193/
15. GamesRadar — "Hades 2 has an epic script of over 400,000 words and 30,000 voice lines" https://www.gamesradar.com/games/hades/hades-2-has-an-epic-script-of-over-400-000-words-and-30-000-voice-lines-around-50-percent-more-than-the-original-roguelike/
16. Aaron Reed — "A Minimal Syntax For Quantum Text" https://medium.com/@aareed/a-minimal-syntax-for-quantum-text-ac5b34308593
17. Aaron Reed — "Subcutanean: Generating the Final Books" https://medium.com/@aareed/subcutanean-generating-the-final-books-abfed50a79d7
18. Andrew Plotkin — "Subcutanean and variations thereof" https://blog.zarfhome.com/2020/05/subcutanean-and-variations-thereof.html
19. Moral Anxiety Studio — "Deep Dive: How to design for impact and narrative variance with Roadwarden" https://www.gamedeveloper.com/design/deep-dive-roadwarden
20. Origin Story podcast — Gareth Damian Martin on Citizen Sleeper https://www.originstory.show/episodes/citizen-sleeper
21. Kate Compton — "Practical procedural generation (for everyone!)" https://www.gamedeveloper.com/design/practical-procedural-generation-for-everyone-
22. Kate Compton / Michael Mateas — "Tracery: An Author-Focused Generative Text Tool" http://www.fdg2015.org/papers/fdg2015_extended_abstract_18.pdf
23. Darius Kazemi — Corpora project https://github.com/dariusk/corpora
24. George Saunders — A Swim in a Pond in the Rain (Random House 2021). Review: https://slate.com/culture/2021/01/george-saunders-chekhov-swim-pond-rain-review.html ; "The Darling" chapter notes: https://rajivmote.wordpress.com/2023/12/12/lessons-from-the-darling-a-swim-in-a-pond-in-the-rain/
25. Causeway Lit — "Free Indirect Style in Runaway" (Munro) https://causewaylit.com/issue-10-memory/craft-essays-10/free-indirect-style-in-runaway/
26. Alexis Kennedy — "How I Got Into Games, Part I: Echo Bazaar" https://medium.com/sex-lies-and-videogames/how-i-got-into-games-part-1-echo-bazaar-371ba792b3e0
27. A Sharp / David Dunham interview (Runeblog) — Six Ages https://elruneblog.blogspot.com/2018/07/interview-with-david-dunham-lead.html
28. AppUnwrapper — Interview with Reigns dev François Alliot https://www.appunwrapper.com/2016/08/17/interview-with-reigns-developer-francois-alliot/

---

## Findings (26)

### Engine / Architecture Findings

**F1. Failbetter QBN — "free-floating storylets gated by qualities."** Fallen London doesn't link passage A → passage B. It exposes whichever storylets qualify right now. Same diner location = a *deck* of storylets; the ones that appear tonight depend on `relationship_maya`, `shift_count`, `witnessed_fight`, etc. The engine does the selection; the writer authors the storylet + its qualifications. [Short, "Beyond Branching"]

**F2. Fallen London's hard word budget forces compression.** Roots ≤30 words. Branches ≤20. Results ≤100. Failbetter's writing tools go red past 100. This is why their prose reads dense and evocative — *the budget forbids throat-clearing*. The whole design implication: if a scene will recur 50 times, each instance has to land in one breath. [Failbetter Guidelines III]

**F3. StoryNexus had inline quality templating.** Embedded text could branch inside a storylet based on a quality value — so a single storylet file narrates differently for suspicious/besotted/indifferent Maya without being three storylets. This is the "1-3 varied lines per revisit" budget in practice. [Short, "Beyond Branching"; Failbetter news]

**F4. Salience systems pick the single best line from a pool.** Valve's and Emily Short's formulation: each line is tagged with a condition-set (location=kitchen, pantry=empty, time=late). When a trigger fires, the engine counts matched conditions and picks *the most specific match*. Fallbacks handle the unspecified cases. [Short; Ruskin GDC 2012]

**F5. Valve Response System — "rule + criteria + response."** Every bark is stored as a rule: a **concept** (`TLK_DANGER`, `TLK_HURT`), **criteria** matched against world facts (health<30, teammate_down=true, map=no_mercy, lines_said_this_minute<3), and a **response** (the actual line or list). More criteria = higher specificity = wins selection. [Ruskin slides]

**F6. The Valve writer's pipeline is "write a line, tag it."** Writers author freely and the programmer-facing tag system is the gate. This is load-bearing for scale: the writer can keep writing variants all day, and the engine picks the one that fits tonight's state. No giant switch statement, no combinatorial branch tree. [Ruskin; Valve Wiki]

**F7. Hades scales by voice lines, not scenes.** 21,000 voice lines in Hades 1; 30,000 in Hades 2. Most are one-liners tied to context slots: current weapon, current boon, run number, last boss beat, last death type, current room, last gift given, who you've met in what order. Writers author *to slots*, not to scenes. Same conversation with Achilles plays completely different prose if you spoke to Patroclus in Elysium first. [GamesRadar; Kasavin GDC 2021]

**F8. Hades' philosophy — "give characters lots to say."** Kasavin: the only real solution to repetition in a roguelike is sheer volume plus context awareness. Dionysus comments on nectar inventory; Ares on weapon. Each god has opinions on things their domain touches, so the same "talk to god in lounge" scene hits a fresh line for 50+ hours. [GamesHub; Kasavin]

**F9. Hades' "priority" ordering for subplots.** Some subplots can fire in any order (Orpheus/Eurydice, Achilles/Patroclus). The engine tracks who you've met, with whom, how many times, and walks each subplot forward independently. Patch notes explicitly mention re-tuning *requirements and priority* so subplots advance reliably. [Supergiant patch notes via GamesRadar]

**F10. Ink's `{a|b|c}` is the atomic unit of revisit variation.** Default `{...|...|...}` is a stopping sequence — advances once per visit, holds on the last. `{&...}` cycles. `{!...}` once-only then silent. `{~...}` shuffle. This maps exactly onto arc stages: week 1/2/3 get different lines with zero state-tracking; you just revisit the passage. [Inkle Ink docs]

**F11. Ink's `{cond: A | B}` is state-gated prose.** `{met_blofeld.learned_his_name: Franz | kept a secret}` — inline, inside normal prose, no passage explosion. Combine with sequences and conditions nest freely: `{met_blofeld: "His name was {learned_name: Franz|a whisper}." | "I missed him."}` [Inkle Ink docs]

**F12. Ink's `knot.visited` counter is free stage-gating.** Any knot tracks its own visit count as a variable. `{diner: ==1: The first time... | ==2: Again — ... | >=5: You know the ashtray by heart now.}` No flags, no writer bookkeeping. Pattern: author the arc stages *inside the passage*, not as separate passages. [Inkle docs]

**F13. 80 Days — story fragments per route, not per city pair.** Every city has associated story content; every **route between neighboring cities** also carries unique content. Ingold's architecture: a fragment library with tags, filtered by cargo/weather/season/route-count, shuffled into the display. Average player sees ~5 fragments per city; authored pool is much larger. [Inkle press kit; Short review]

**F14. Reigns — card reprinting uses context.** Cards re-enter the deck with modified text based on which previous cards you answered and how. The "devil" card shows up differently depending on your church/treasury/military state. Writer authors a base card plus variant overrides. [AppUnwrapper interview]

**F15. Roadwarden — player's own description choices become canon.** When the player describes the city to NPCs (choosing flavor from a list), those flavor choices *become the city* in later scenes. The scene doesn't change; the details the narrator has previously committed to change. Player-authored salience. [GameDeveloper deep dive]

**F16. Roadwarden's "attitude" selector is a prose modifier.** Five attitudes (friendly / playful / distanced / intimidating / vulnerable) are selected before a conversation and rewrite the same scene's surface. Same encounter structure, different register. [GameDeveloper]

**F17. Citizen Sleeper — prose pull-back as a structural tool.** Martin explicitly uses prose (vs. dialogue) to "pull back, stretch out, compress time, or reposition perspective." The same station location is described differently across cycles by changing *which strand of the station the narrator is foregrounding* (a shift, a bar, a character's absence). Same place, different narrator attention. [Origin Story podcast]

**F18. Subcutanean's narrator-trait system.** Reed varies three axes per copy: laconic↔voluble, optimist↔pessimist, slang↔formal. The axis is fixed at generation time and runs consistently through the whole book. Named variables + hundreds of anonymous micro-variables (word/phrase swaps) produce 209–239 page books from one source. [Plotkin; Reed "Generating the Final Books"]

**F19. Subcutanean tracks callbacks.** When scene A inserts a detail, scene B's variant can reflect it: "perhaps with just a well-placed 'again'." The quantum text system records which variants fired so downstream prose can acknowledge them. [Plotkin]

**F20. Reed's `.quant` minimal syntax — `[a|b]`, `[text|]`, weighted `[25>A|B]`, traits via `[DEFINE verbose]` and `[verbose>...]`.** Two places variables can appear: after `DEFINE`, or before `>`. Deliberately no AND/OR compounds — one hierarchical level only, to keep the writer in flow. [Reed Medium]

**F21. Tracery — expansion grammars with `#symbol#`.** Kate Compton's JSON format: `"origin": ["The #animal# sees #event#."]` expands recursively. Used by 3000+ bots. Practical point for variant prose: even the *simplest* template substitution ("The #weather# #verb# against the #diner-surface#") produces believable variation if the symbol pools are curated. [Compton Tracery paper]

**F22. Corpora — curated word lists beat random dictionaries.** Darius Kazemi's insight: you don't want *every* adjective; you want the *right small set* that fits your voice. Copy your `adjs.json` from project to project. For variant prose: per-location curated detail pools (diner-smells: burnt coffee, fryer grease, rain-soaked wool, cheap bleach) beat Thesaurus.com. [Kazemi Corpora]

### Fiction-Craft Findings

**F23. Saunders on "The Darling" — pattern + variation as structure.** Chekhov's story is "founded on pattern — repetition and then variation on that repetition — creating a pleasurable rhythm of expectation and resolution." Olenka's house is described four times across four relationships. The house doesn't change. The *objects the narrator notices*, and *what the objects mean*, change with each husband. Chekhov's trick: the narrator silently adopts the new husband's worldview, so we feel the drift without being told. This is the exact template for "week 3 Maya notices the ashtray she didn't see in week 1." [Saunders, *Swim in a Pond in the Rain*]

**F24. Munro — "she noticed" is the wrong verb.** Free-indirect-style lesson: "She noticed her mother was angry" is one verb away from "Her mother was angry." The second sentence is stronger *because* we're already inside her head. For variant prose: don't write "Maya sees the ashtray now." Write "The ashtray sits between them. Full." The reader registers the noticing without being narrated to. [Causeway Lit on Munro]

**F25. Munro's POV shifts accelerate understanding.** Quick POV micro-shifts (a single sentence from the waitress, then back) can reveal character state more efficiently than paragraphs of PC thought. For repeatable diner scenes: the waitress's line *about* Maya is a different variant than Maya's internal line. Alternate them by stage. [Causeway Lit]

**F26. Kennedy's Echo Bazaar voice — "welcoming menace."** Kennedy designed a house voice ("delicious friend," "definitely a story for adults") that's consistent across thousands of storylets. The voice is the glue; the variants sit inside it. For a project with hundreds of variants: define the voice first, then variants inherit tone automatically. [Kennedy, Medium]

---

## Deep Read Notes

### DR1 — Ink's sequence-and-condition stack (from the official docs)

The power move is nesting. Inside a passage that says "You enter the diner," you can write:

```
You enter the diner. {The bell still sticks. | The bell sticks, as always. | You don't hear the bell anymore.}
{week >= 3: Maya is at the counter, not looking up. | Maya looks up.}
{&The fluorescent above booth three flickers.|The rain on the window.|The smell of burnt coffee.|The clatter of someone's plate hitting tile.}
```

Three different mechanics in one passage:
- A 3-element stopping sequence that permanently hardens to "you don't hear the bell anymore" from visit 3 onward
- A hard state gate on week count
- A cycle of ambient details that rotates each visit

This is F12 + F10 + F11 composed. Every variant is inside one passage source. The git-diff on that file is small. The player's experience is "this scene keeps feeling different."

### DR2 — Valve Response System concrete example (Ruskin slides)

A bark rule has three parts:

```
rule "Scout_HurtByHunter":
  criteria:
    WhoSaid = Scout
    Concept = TLK_WOUNDED
    HealthBelow = 30
    AttackerClass = Hunter
    TimeSinceLastBark > 8
    MapName = no_mercy_01
  response: "Freakin' hunter! Get it OFF me!"
```

The engine collects *all* rules matching `Concept=TLK_WOUNDED` and picks the one with the most matched criteria. Writers author dozens of variants at different specificity tiers: generic wounded bark, wounded-by-hunter bark, wounded-by-hunter-on-this-map bark, wounded-by-hunter-on-this-map-with-low-team bark. When you play, the engine serves the deepest-matching line it has. **Takeaway for a story system: write the generic first; add variants with more tags over time; the engine automatically upgrades the player's experience as specificity grows.**

### DR3 — Hades dialogue scaffolding (Kasavin)

Three observed techniques:
- **Relational acknowledgement.** "It's nice having someone just notice and care that there was a small change about you, like a haircut or a new pair of shoes." Translate: when flag X changes, *at least one* NPC should have a line that notices. Not all NPCs — just one, for specificity.
- **Domain-gated commentary.** Dionysus comments on alcohol; Ares on violence. Each NPC has a narrow "domain of salience" — they only bark when something in their lane happens. This keeps voices distinct and prevents everyone saying the same generic "congrats."
- **Priority stack for subplots.** Multiple subplots compete for the single "talk to NPC" slot this run. The engine picks the highest-priority unfinished beat. Patch notes explicitly tune priority so "subplots advance reliably" — i.e., the writer's team *adjusts* which beat surfaces when several qualify.

### DR4 — Subcutanean narrator traits across scenes (Plotkin + Reed)

Reed's `[DEFINE verbose|taciturn]` fires once at book-generation time. Then every passage sprinkled with `[verbose>an extra descriptive sentence rolls through here]` gets that sentence or doesn't. The practical effect Plotkin describes:

> "Orion may be more laconic or more voluble; he may be an optimist or a pessimist; he may prefer slang or avoid it. These choices are maintained throughout the text."

The insight that applies to a weekly-diner-scene system: the *character arc stage* acts like a narrator trait. Week 1 Maya = hopeful/polite. Week 5 Maya = tired/curt. The same scene gets different variant-insertions because Maya's "narrator trait" has moved along the axis. One axis, consistent application, cumulative effect.

### DR5 — Saunders on "The Darling" — mechanism for noticed-detail-grows

In the Chekhov story, Olenka's house is described each time a new husband moves in. The *inventory* of what gets mentioned shifts:
- Husband 1 (theater manager): backstage gossip, posters on the walls, the smell of greasepaint on his jacket
- Husband 2 (timber merchant): stacks of account books, the smell of pine resin, workers tramping through the hall
- Husband 3 (veterinarian): iodine on the washstand, a horse bridle by the door, coarse soap in the dish

Same house. The *house* isn't narrated as changing. Olenka's ambient attention changes because her husband's concerns have become her concerns. Chekhov never writes "she was adopting his worldview"; he writes the objects she now notices first.

**Direct translation for a diner scene across a character arc:**
- Week 1 (tentative): the bell above the door, the laminated menu, Maya's name tag
- Week 3 (entangled): the specific booth, Maya's second cigarette, the ashtray refill
- Week 6 (complicit): the rear exit, the till's drawer sticking, who sits by the window

The diner is static authored content. The *detail inventory* the passage selects from shifts by arc stage. This is Ink's `{stage==1: A | stage==2: B | stage==3: C}` but driven by fiction craft, not engine capability.

### DR6 — Fallen London's "tiny mandarin" principle (reconstructed)

I couldn't locate a canonical Failbetter blog post using that exact phrase — it appears to be community shorthand rather than an official term, and search didn't surface it directly. The underlying principle is observable across Failbetter's output and matches Short's QBN analysis: *one small prose change per quality-level-up creates the illusion of deep world-reactivity*. Players remember the detail that changed, not the 95% that didn't. Design budget in their published storylets: roughly 1–3 varied lines per revisit at most, plus a new title/summary when the quality tier rolls over. This is worth flagging as **inferred from corpus**, not quoted.

---

## Practical Composition — the six techniques, ranked by effort/payoff

1. **Ink sequences inside the passage** (F10/F12). Highest payoff per line of code. A `{&...|...|...}` cycle on ambient detail makes every revisit feel fresh with zero state tracking.
2. **State-gated inline variants** (F11). `{stage>=3: X | Y}` — the arc-stage gate belongs inside the passage, not as a passage copy.
3. **Narrator-trait axis** (F18/F24). Pick 1–2 axes (hopeful↔worn; polite↔curt) that move with arc stage; tag prose inserts by axis; apply consistently.
4. **Noticed-detail inventory shift** (F23/DR5). Per stage, curate which objects in the room the passage mentions first. Don't rewrite the room — rewrite attention.
5. **Domain-gated NPC barks** (F8/DR3). One NPC per salient domain; they only bark when something in their lane changes. Prevents "everybody notices everything."
6. **Specificity tiers + fallback** (F5/DR2). Write one generic variant first. Ship it. Add more-tagged variants opportunistically; engine auto-upgrades.

**Authoring budgets observed:**
- Failbetter: ≤30/≤20/≤100-word discipline; 1–3 varied lines per revisit
- 80 Days: ~5 fragments visible per city out of much larger pool per city/route
- Hades: ~21k lines total, ~500 per major NPC; players see a novel's worth across 50h
- Subcutanean: "several hundred" micro-variables + a handful of named narrator traits; output varies 209–239 pages from one source

---

## Gaps

- **Six Ages / King of Dragon Pass event variance** — confirmed conceptually (events vary by clan chief, family, war state per player-facing descriptions) but no primary source from Dunham detailing the scripting architecture was reachable. Would want the A Sharp design notes or a Dunham GDC/podcast transcript specifically on event-text conditioning.
- **"Tiny mandarin" Kennedy quote** — not locatable under that name. Likely community shorthand. Principle stands (F3, DR6) but the attributed pull-quote in your ask is reconstructed, not sourced.
- **Ingold's exact per-city-fragment count in 80 Days** — press kit and Short confirm "a small story per city and per route" and ~half-million words total, but the specific "15–20 variants per city, 5–6 shown per visit" number in your ask wasn't in any primary source I reached. The architecture is real; the exact numbers are anecdotal.
- **Citizen Sleeper scripting format** — Martin's craft talks are about prose philosophy, not scripting. How cycle-variants are authored (Ink? custom?) wasn't in the reachable interviews.
- **GDC Vault Ingold 2017 audio** — Archive.org link exists but I couldn't fetch the slides' specific claims about fragment-tagging architecture within this research pass. Would be the single best deep-read next step.
- **Reed's Subcutanean exact variant count per chapter** — "several hundred" is as precise as the public posts get. A chapter-level breakdown exists in his ICIDS-adjacent writing but wasn't in the Medium posts fetched.
- **Roadwarden scripting internals** — confirmed at the design level (attitude system, player-description feedback) but the authoring format (Ren'Py? custom?) and variant-density numbers weren't in the deep-dive article.
