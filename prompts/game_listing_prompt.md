# Game Listing Generator

Generate a publish-ready game description and tags for adult game distribution sites.

## Input

Paste the game's TOML metadata below. At minimum include:
- `[project]` block (title, description)
- `[player]` block (name, description)
- `[[npcs]]` blocks (names, descriptions, traits)
- Story arc nodes (scene names, descriptions, journal entries)
- Activity names and tier types
- Ending IDs and descriptions
- Any `[settings]` blocks (rent, clothing, time, etc.)

```toml
[PASTE TOML HERE]
```

## Description Rules

Write a game description (100-150 words):

- **Hook first** — open with the emotional gut-punch, not a setup paragraph
- **Sell the tension, not the mechanics** — the player should feel the stakes before they understand the systems
- **Write like a back-of-book blurb** — short paragraphs, punchy rhythm, incomplete sentences are fine
- **End with a sharp line** — number of endings, a question, or the core dilemma stated plainly
- **Mention the core mechanic once**, briefly (daily life sim, visual novel, open world, etc.)
- **No filler** — every sentence earns its place or gets cut

### Banned phrases
- "explore a world of", "immersive experience", "embark on a journey", "in this game you"
- "delve", "landscape", "robust", "seamless", "innovative", "cutting-edge", "captivating"
- "will you choose X or Y?" as the final line (too generic — be specific to THIS game)
- "features include:" followed by a bullet list

### Tone reference
Good: "Fourteen mornings. Fourteen nights. The wedding doesn't move."
Bad: "Experience an immersive 14-day romantic visual novel with multiple branching paths."

## Tag Rules

Select tags from the master list below. **Do not invent tags.**

- **Order**: genre first, then content type, then specific acts, then platform, then meta
- **Include all that genuinely apply** — if the game has oral scenes, tag it; if it doesn't, don't
- **Skip aspirational tags** — only tag what's actually in the game
- **Output as comma-separated plain text**, one line

### Master Tag List (Gamcore English)

```
2D, 3D, Adventure, Action Games, Ahegao, Aliens, Alcohol, Anal Sex, Arcade, Asians,
Babysitter, Ball Games, Big Cocks, Big Tits, Blackjack, Blondes, Blowjobs, Boobjob,
Booty Call, Brunettes, Business Management, CG Galleries, Cheating, Chinese, Craps,
Cuckold Games, Cyberpunk, Demons, Dirty Ernie Show, Ejaculation, Elves, Erotic Games,
Fantasy, Femboy Games, Femdom, Fetish, Flash, Footjob, Free Games, Free Strip Games,
French, Fuck Town, Glamour, Group Sex, Halloween, Handjob, Hardcore, Harem,
Heroes, Hentai, High Resolution, Horror, HTML Games, Incest, Interracial Sex,
Japanese, Licking, Logic Games, Love, Masturbation, Medical, Medieval Games, MILF,
Milking, Mobile Games, Monster Sex, Music, Naked Games, Netorare Games, NSFW Games,
Nuns, Numbers, Oral Sex, Overwatch, Paranormal Games, Parodies, Perversion, Physics,
Platform Games, Point and Click, Poker, Police, Porn Games, Pregnant, Puzzles, Quests,
Quickies, Quiz, Real People, Redheads, Robots, Role-Playing Games, Roulette, Rule34,
BDSM, Sandbox Games, Schoolgirls, Sex, Sex Chat, Sex Stories, Sex Toys, Sexy Asses,
Sexy Nurses, Shemale, Shooter, Simulation, Space, Sports, Stars, Strip,
Strategy Games, Teen Sex, Time-Based Games, Transgender, TV and Film, Uncensored,
Vanilla Sex, Video, Virtual Girls, Visual Novel, Zombies,
AI Porn Games, Female Protagonist, Meet and Fuck, 18+, XXX Games, Criminals,
Clothing, Cartoons, Censored, Jokes, Songs, Recommendations, Walkthroughs,
Public Sex, RPG Maker, RenPy, Unity, Tyrano, iOS Porn Games, APK, itchio
```

## Output Format

```
DESCRIPTION:
[Your description here, 100-150 words]

TAGS:
[comma-separated tags from master list]
```
