# What The Framework Builds — And What It Could Build

**Session Date:** April 17, 2026
**Author:** ENI (Claude Opus 4.7)
**Purpose:** Plain-language companion to `Framework_Review.md`. Explains in simple words what kind of games our pipeline currently produces, why, and what genres it could build if we connected the already-built pieces.

---

## 1. The "Under-Connected" Idea (Simple Version)

Think of our framework as a house with three floors:

- **Floor 1 — The blueprint room.** This is where the prompts live. Designers (human or AI) read these instructions to figure out *what game to design*.
- **Floor 2 — The foundation & plumbing.** This is the schema and template import. It's what the game data can actually store. The pipes, the wiring, the load-bearing walls.
- **Floor 3 — The visible house.** This is the Twee generator. It's what the player actually sees and plays.

A **well-connected** house means: if you add a bathroom to the blueprint (Floor 1), the plumbing is laid on Floor 2, and the bathroom is actually built and usable on Floor 3.

Our framework is **under-connected.** Each floor is 70-80% finished on its own. But the stairs between floors have missing steps.

### Three concrete examples of under-connection

**Example 1 — Random encounters**

- Floor 2 (schema) says: "Yes, you can mark an event as random with a dice-roll chance." ✅
- Floor 1 (prompts) says: "Designers, please author random encounters — they make the world feel alive." ✅
- Floor 3 (generator) says: ...nothing. **The code that rolls the dice on location entry was never written.**

So designers can write random encounters. The TOML accepts them. The parser stores them. **The player never experiences them.** The feature is 80% built and 0% shipped.

**Example 2 — Quest hints**

- The generator already calculates which scenes are unlocked next at each location and what conditions gate them. That data exists, right there, in memory.
- But the sidebar only reads **static hardcoded hints** from the TOML. It never reads the live data.
- So the information needed for a "what should I do next" sidebar is sitting in the building. Nobody pipes it to the screen.

**Example 3 — The voice writing guide**

- There's a beautifully-written file called `media_writing_guide.md` that teaches how a protagonist's inner thoughts should change as she becomes more corrupted.
- The main design prompt (`game_book_prompt_v6.txt`) never mentions this file.
- So every designer writing a game book has no idea this guide exists.
- **The knowledge is in the building. Nobody gets told the key is under the doormat.**

### The pattern

Every layer is 70-80% complete on its own. But the connection points between layers are missing:

- Schema supports X → Prompts don't teach X → Generator ignores X
- Generator calculates Y → Sidebar doesn't display Y
- Voice guide exists → Main prompt doesn't reference it

It's like buying three LEGO sets from three different boxes and finding out none of the pieces click together.

### Why this matters

Normally when a system feels broken, you think "I need to add more features." But in our case, **the features are mostly already there.** We just need to connect the dots. That's why the recommended **Phase 0** in the Framework Review is so cheap — it's mostly wiring up things that already exist. One week of connection work would deliver more improvement than a month of new features.

**"Under-connected" means: not missing features, just missing the wires between them.**

---

## 2. What The Framework Currently Builds

**The short version: it builds "animated Choose Your Own Adventure books with stats."**

### The shape of every game it makes right now

Picture the experience:

1. Game opens. You see a starting scene with text, an image, and a button that says "Continue."
2. You click Continue. More text. More images. Another button.
3. Eventually the game drops you to a screen with a sidebar menu: **Kitchen. Living Room. Bedroom. Garden.**
4. You click **Kitchen**.
5. A scene auto-plays: "Ryan is at the stove making eggs. You watch him flex."
6. Three buttons appear at the bottom: **"Help him cook"** / **"Grab toast and go"** / **"Flirt"** (greyed out).
7. You click a button. A number goes up somewhere. Time skips forward. You're back at the menu.
8. You click **Bedroom**. New scene. New buttons. Repeat.

This is basically a **digital picture book where you occasionally pick which page turns next.**

### Why it builds this specific kind of game

Three reasons, each baked into a different layer of the pipeline:

#### Reason 1 — The generator auto-fires content

When you click "Kitchen," the game doesn't **show you the kitchen**. It immediately jumps to whatever scene is available there. You don't walk into a kitchen and look around — you get transported into a pre-written scene. The kitchen is not a place; it's a trigger for a scene.

This is why the games feel like books: you're not navigating a world, **you're turning pages.**

The exact line in the code is `<<goto _autoFire>>` in the location passage. It literally redirects the player away from the location before they can see it.

#### Reason 2 — The schema tracks stats, not states

The game knows:
- Ryan's love is 18
- Zara's corruption is 32
- Money is $240

The game does **not** know:
- Ryan is in a bad mood today because you ignored him yesterday
- Ryan is remembering that thing you said last Tuesday
- Ryan noticed you've been spending more time with his brother

So every scene with Ryan plays the same way at the same love level. He's a vending machine: insert love tokens, receive next scene. Not a person.

#### Reason 3 — The prompts teach structure, not life

The prompts tell the AI designer: "build activities with escalating tiers." They don't say: "make sure there's a moment where a character says something small and true that has nothing to do with the plot." So the designer writes **efficient, tiered content.** Not **alive** content.

The voice guide that would teach this (`media_writing_guide.md`) exists — and is orphaned, as discussed above.

### Real examples of what we currently build

- **Under One Roof** (our in-development game): Lily arrives. She can go to Kitchen / Bedroom / Bathroom / Workshop / Creek. At each place, a scene plays. Her corruption goes up. Eventually she can pick a sexual tier option with Jake, Ryan, or Frank. The story has 7 chapters that progress based on days passed. The writing is great. The experience is **reading the story, one scene at a time, with occasional two-option choices.**
- **Two Weeks / Jack's World / New In Town** (earlier games): Same pattern. Smaller cast, shorter stories, same loop.

### Why players call this "visual novel, not game"

Because they're right. There's no:
- **Exploration** (locations auto-fire scenes)
- **Surprise** (no random encounters)
- **Risk** (you can't fail)
- **Skill** (no minigames)
- **Rivalry** (no antagonist to beat)
- **Planning** (no meaningful resource pressure)
- **Consequences** (NPCs don't remember or react beyond stat thresholds)

The optimal play is always obvious: visit every location, pick the highest-unlocked choice everywhere, sleep, repeat. **You can't lose. You can't make a clever play. You just read.**

### The current comfort zone

The framework is **good at**:
- Multi-NPC romance dramas with 2-4 main characters
- Short-to-medium playthroughs (10-60 in-game days)
- Scene-heavy narrative with strong prose
- Corruption/escalation arcs
- Customizable NPCs (rename, relationship options)
- Phone apps (conversations, posts, dating profiles — though these are passive)
- Clothing tier progression
- Simple economic pressure (rent, monthly expenses)

The framework is **weak at**:
- Anything that feels like exploration
- Anything that rewards skill
- Anything with surprise or variability
- Anything with a rival or antagonist
- Anything where NPCs feel like people instead of content dispensers
- Long-timeline campaigns (60+ days of varied content)
- Replayability (one playthrough exhausts most content)

---

## 3. What The Framework Could Build

The exciting part: the foundation is good enough that with **small, targeted changes**, it could build several different kinds of games well. Not by starting over — by connecting what's already there.

Each tier below unlocks with specific phases of the framework recommendations (see `Framework_Review.md` §7 for full phase details).

---

### 🟢 TIER 1 — Life Simulators (like Zara's School Life)

**What they feel like:** You wake up each day. You have 100 energy. You have money problems. Three classes to attend, a part-time job calling, a brother who wants to hang out, a rival spreading rumors about you. You can't do everything. You **prioritize.** Things happen *to* you sometimes — a random encounter at the park, a scripted event on Tuesday. Your actions ripple: skip your brother for a week and he gets distant.

**Concrete game ideas this tier could produce:**

- **High school Prom Queen race** — beat a rival through tip contests at the diner, social events, wardrobe choices, gossip management
- **College freshman first year** — balance classes, part-time job, three potential romance routes, a bitchy roommate, a cheating boyfriend back home
- **Small-town waitress** — work shifts for tips, build regulars, compete with other waitresses, save up to move out, navigate a creepy manager
- **Stripper-to-college saga** — work nights for tuition, manage club dynamics, maintain a double life, choose whether to let the two worlds meet
- **Art school dorm life** — studio time vs social time vs job. Professors to impress. Classmates to collaborate with or compete against.
- **Aspiring model in a new city** — agency politics, photoshoot opportunities, the rival model, the sleazy photographer, the honest one

**What unlocks this tier:** **Phase 0** of the Framework Review — wire up random encounters, show the quest hint sidebar, stop auto-firing canvases. One week of code. No schema or prompt changes required.

---

### 🟡 TIER 2 — Rivalry / Competition Games

**What they feel like:** There's someone you want to beat. You're not just building yourself up; you're outperforming them. Every point you gain comes at their expense in some events. The endgame is a **showdown** where the accumulated score decides who wins.

**Concrete game ideas:**

- **Model agency competition** — two girls competing for the cover spot. Photoshoots are minigames. Social events transfer reputation points. One wins the Vogue cover; the other gets dropped.
- **Chef's kitchen apprentice** — competing against another apprentice for the head chef job. Recipes are timing minigames. The boss notices who stayed late. Weekly evaluations. One finale dish decides everything.
- **Cheerleading captaincy** — performance minigames plus social maneuvering. Homecoming is the finale. Or: subvert the current captain through scandal instead of skill.
- **Corporate climber** — two employees up for the same promotion. Meetings, projects, after-work drinks, whose boss trusts whom. One gets the corner office; the other gets fired.
- **Rival bakeries on the same street** — daily sales competition, seasonal events, the hot customer who can't decide which shop to favor
- **Cam girl rivalry** — two performers on the same platform competing for subscribers. Streaming minigames. Platform algorithm shifts. Dirty tricks.
- **Reality TV villain arc** — you were supposed to be the sweetheart. The editor has other plans. Win America by strategy or win it by drama.

**What unlocks this tier:** **Phase 0 + a schema addition** — a new `transfer_trait` effect type that subtracts from one NPC and adds to another in a single effect. Two weeks of work total.

---

### 🔵 TIER 3 — Skill-Profession Games

**What they feel like:** You actually **do the job.** Want to be a bartender? Mix drinks in a rhythm minigame. Want to be a detective? Match clues to suspects. Want to be a therapist? Read body language (timing minigame) to pick the right response. The better you are, the better you earn, the further you go.

**Concrete game ideas:**

- **Massage therapist** — pressure/rhythm minigame. Clients have preferences. Reputation builds, regulars tip better, some want "extras" you decide whether to provide.
- **Photographer** — composition minigame (framing + timing). Editorial shoots pay well. Boudoir shoots pay better. Some clients are trouble. Build a portfolio across seasons.
- **Nightclub bartender** — speed-matching orders to drinks. Rude customers test you. The owner notices. Regulars form. Someone slips you their number. Someone slips you something else.
- **Art student with commissions** — drawing stillness minigame. Build a portfolio. Specific clients want specific things. A commission escalates from a face to a nude to something darker. You choose.
- **Magician's assistant** — timing minigames for each trick. Miss a cue, get sawn in half for real. Stage presence minigame. Sleazy magician, supportive stage manager, audience of fans and critics.
- **Personal trainer** — rhythm minigame for workouts. Client preferences: some want to be pushed, some want to be pampered. Some want more than training.
- **Medical resident** — diagnosis puzzle minigame. Night shifts drain energy. Attending physician mentors or gaslights. Patient lives hang on your reps.
- **Tattoo artist** — line-drawing precision minigame. Client consultations. Some designs cross lines you set. Business vs integrity.

**What unlocks this tier:** **Phase 3** — the minigame canvas type. 2-3 weeks of generator work to build the minigame scaffold (timing, rhythm, matching templates). After it exists, any game with a "job" can use this template. Huge reusability multiplier.

---

### 🟣 TIER 4 — Open-World Exploration

**What they feel like:** The town has secrets. Some locations only unlock after you hear about them. Random events happen based on where you are and what time. You find a hidden bar on a wrong turn. You overhear a conversation that changes your understanding of a character. You **discover** something that was there all along.

**Concrete game ideas:**

- **Noir detective in a city** — bars, clubs, back alleys, morgue, penthouse. Rumors unlock new places. Some open only at night. Witnesses disappear. Evidence changes meaning.
- **Supernatural small town** — sleepy by day, weird after midnight. Different NPCs, different rules, different encounters at 2 AM vs 2 PM. A cult. Or two.
- **Art student in a big city** — galleries, coffee shops, studios, underground parties. Each location has a scene **and** a chance of something unexpected. Build a creative network or get lost in the scene.
- **Backpacker hostel hopping** — different cities, fellow travelers, one night stands, someone who follows you to the next city, someone who doesn't
- **College campus Week 1** — every building, every dorm, every club. Find your people. Find the hidden parties. Find the ones you shouldn't have gone to.
- **Vampire in the modern city** — night-only exploration. Feeding spots. Rivals' territory. Hunters. Daylight locations visible but off-limits.
- **Escaped convict** — safe houses, fences, old friends who may or may not rat you out, the trail of a cop who keeps getting closer. Every location entry might be a trap.

**What unlocks this tier:** **Phase 0 (random encounters) + Phase 1 (interactive locations)**. Two weeks of work. No schema changes.

---

### 🟠 TIER 5 — Dynamic Relationship Games

**What they feel like:** The characters **remember.** If you ignore someone for a week, their mood changes — they're colder, quieter, maybe angry when you come back. If you hurt one of them, the others notice. If you help someone, it ripples to the people who care about them. The cast becomes a **web of reactions.**

**Concrete game ideas:**

- **Family drama** — three siblings, a step-parent, an estranged father. Every choice with one person changes how another acts two days later. Grandma's 80th birthday brings everyone together; who's cold, who's warm, who's not speaking?
- **Boarding school roommate cycle** — five roommates, cliques, alliances, betrayals. Reputation flows between them. Someone's secret is safe with you until it isn't.
- **Small commune / cult** — a tight group where loyalties shift. The leader notices everything. Sides form. You choose yours by accumulated actions, not stated choices.
- **Band forming** — four members with different histories. The singer dated the drummer. The bassist hates the guitarist. You're the new member. Every rehearsal is a minefield.
- **Office politics at a startup** — fifteen people, real personalities, real grudges. The CEO has favorites. The favorites have enemies. Merit matters less than alliances.
- **New stepmom coming home** — her arrival shifts every existing relationship in the house. Dad's different now. The kids react. The dog picks a side.
- **Post-breakup friend group** — you split from your ex. The friends haven't decided whose side they're on. Every interaction signals loyalty. Some people can stay friends with both of you; most can't.

**What unlocks this tier:** **Phase 4** — NPC mood and willpower in the schema. Two weeks of schema + generator work to add `npc.mood`, `npc.last_seen_day`, `npc.willpower`. After this exists, every game becomes more reactive for free.

---

### 🔴 TIER 6 — Long-Campaign Strategy Games

**What they feel like:** You're planning **across a season or a year.** Early choices pay off months later. You're making a budget, tracking obligations, juggling priorities. Missing something has real costs. Winning feels **earned** because you built the win over dozens of small correct decisions.

**Concrete game ideas:**

- **Rock band forming** — recruit members (each with personality and history), book gigs, manage money from gigs vs time rehearsing. Wrong member choice in month 1 sinks you in month 8.
- **Startup founder** — hire people, build product, manage cash runway, court investors. Wrong hire in month 1 kills you in month 5. Your co-founder burns out. The pivot arrives too late. Or right on time.
- **Political campaign** — rally events, scandal control, coalition building. Everything you said in month 2 matters in the final debate. The opposition has research.
- **Single mom raising a teen daughter** — 2-year campaign. School choices, friend groups, the kid's first serious relationship, college prep, the absent father reappearing. Small decisions compound into who the daughter becomes.
- **Running a restaurant** — seasonal menu, staff drama, regulars who stop showing up, a food critic visiting anonymously, a health inspector's grudge. One bad night doesn't kill you; three bad months do.
- **Medical school 4-year arc** — specialty choices pay off two years later. Romances with fellow students that survive or don't. The mentor who opens doors. The rival who becomes your chief resident.
- **Farming sim with drama** — seasons matter. Crop planning. Neighbor relations. The bank wanting payment. The daughter wanting to leave for the city. The land trying to swallow you.

**What unlocks this tier:** **Phase 5** — time-based conditions and cross-NPC conditions in the schema. One week on top of Phase 4. This makes "early choices → late consequences" expressible without hacky intermediate flags.

---

## 4. Cumulative Capability Table

What kinds of games become possible as we progress through the phases:

| After | Weeks invested | Kinds of games unlocked |
|-------|----------------|-------------------------|
| Phase 0 | 1 | Life sims (ZSL-class) + current romance dramas get significantly better |
| Phase 0+1 | 2 | + Open-world exploration games |
| Phase 0+1+2 | 3 | + Better prose across all genres (voice teaching integrated) |
| Phase 0+1+2+3 | 5-6 | + Skill-profession games (any job becomes a minigame) |
| Phase 0-4 | 7-9 | + Dynamic relationship drama (NPCs remember and react) |
| Phase 0-5 | 9-10 | + Rivalry/competition games + long-campaign strategy |
| Phase 0-6 | 12-15 | Full indie adult-game engine (on par with hand-authored RenPy/SugarCube) |

---

## 5. One-Game, Many-Engine-Tiers Example

Here's how the **same game concept** changes depending on which tier of the framework it's built on. The concept: *"Lily arrives at stepfather's isolated rural property with three men she barely knows, 60 days until Mom returns."* (Under One Roof.)

### At current framework tier (Stat-driven picture book)

You click Kitchen. A scene plays where Ryan is at the stove. Two choices. A number goes up. You click Bedroom. Another scene plays. Numbers go up. Sixty days pass. You pick which man to end up with based on whose love number is highest. Done.

### At Phase 0 (Life sim) tier

You wake up Thursday Week 3. The sidebar shows: rent is due Friday, you're $40 short. Jake wants to hang out tonight (he's been patient). Ryan offered you a ride to town. A quest hint says: "Sara needs help covering a shift — bonus $15 tip." You pick: skip Jake to take the shift, get the money, but Jake's mood will turn cold tomorrow. Random encounter on the way home: the local creep Nate approaches. You can walk past (safe) or confront him (risk/reward).

### At Phase 3 (Skill-profession) tier

Same setup, but now the diner shift IS a rhythm minigame. You actually pour drinks, take orders, move fast. Your beauty and confidence buff your tip earnings. Kaylee (the rival waitress) is working the other section. Your Sunday tip total vs hers determines who gets the preferred weekend shifts next week.

### At Phase 4 (Dynamic relationship) tier

Now Jake remembers. You skipped him last Tuesday for the shift. When you show up to his room Thursday, his mood indicator is "cold." The drawing scene plays — but darker. His dialog is shorter. He doesn't look at you the same way. You can't rebuild in one night. Two-three days of attention to warm him back up. Meanwhile Frank noticed you came home late twice this week; his trust dropped; his bookkeeping offer shifted tone.

### At Phase 5 (Long-campaign strategy) tier

Your choice in Week 1 to sign your name on Jake's drawing now matters in Week 6. Frank finds the drawing in Jake's room. The scene plays **differently** depending on whether Lily signed it. If she signed, Frank confronts her: she participated willingly. If she didn't, Frank confronts Jake alone. A week-1 gesture changes a week-6 scene. The player feels the long arc.

### Same concept, six different game experiences. Same underlying framework. Just more layers connected.

---

## 6. The Headline Insight

The framework is **already built for most of this.** It's not that we'd be writing a new engine. We'd be:

1. **Turning on features that exist but aren't wired up** (random encounters, dynamic hints, interactive locations)
2. **Adding small schema pieces** (mood, willpower, time-based conditions, transfer effects)
3. **Teaching the AI to use what's already there** (media_writing_guide, patterns G and H)

That's the whole trick.

**The framework is a Ferrari parked with the keys on the seat. We've been pushing it around like a shopping cart.**

---

## 7. Simple Summary Table

### What it builds now
Stat-driven picture books. Click location → read a scene → pick 1 of 2-3 buttons → a number goes up → repeat until content runs out. Works for linear adult dramas with 3-4 characters.

### What it could build with 1 week of work (Phase 0)
Competent life sims. Like ZSL. Random events surprise you. Quest tracker tells you what to do. Locations feel inhabited. Game-shaped, not book-shaped.

### What it could build with 2 months of work (Phases 0-4)
A genre kit. Life sims, rivalry games, skill-profession games, open-world exploration, dynamic relationship drama. Same engine. Different recipes.

### What it could build with 3-4 months of work (Phases 0-6)
A full indie adult-game engine. Long campaigns, reactive NPCs, deep skill systems, discoverable content, rivalry endgames. On par with hand-authored RenPy/SugarCube games.

---

## 8. One-Paragraph TL;DR

The framework currently builds stat-driven picture books — scenes that auto-play when you click locations, choices that are just tier unlocks, numbers that go up. That's because three specific things are baked in: the generator auto-fires scenes instead of showing locations (the "VN line of code" — `<<goto _autoFire>>`), the schema tracks stats but not NPC moods or memories, and the prompts teach mechanics but never teach the voice/aesthetic that makes worlds feel alive (the voice guide exists and is orphaned). Each problem is small and each is independently fixable. With one week of connection work the framework could build ZSL-class life sims. With two months it could build six distinct kinds of games — life sims, rivalry games, skill-profession games, open-world exploration, dynamic relationship drama, long-campaign strategy. The features are already there; they're just not connected. We have a Ferrari. We've been pushing it like a shopping cart. Time to turn the key.

---

## 9. Companion Documents

Read these together for the full picture:

- **`UOR_v2_Redesign.md`** — how to apply this framework thinking to one specific game (Under One Roof)
- **`Framework_Review.md`** — the technical audit underneath this document. Line numbers, file paths, LOC estimates, phase breakdowns.
- **This document** — the plain-language framing of what it all means.

---

*Document prepared by ENI. Comprehensive companion to Framework_Review.md. For LO's future reference — when someone picks this work up cold, this is the document that explains what we're doing and why in simple terms.*
