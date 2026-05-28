# Stages 04 — Game Listing Prompt (port)

**Status:** LLM-consumed prompt. Post-build listing/marketing stage.
**Replaces:** `prompts/game_listing_prompt.md` (3.7KB / 82 lines, 2026-03-28).
**Input:** the game's TOML metadata (typically `[project]` + `[player]` + `[[npcs]]` + capstone canvases + `[[quest_cards]]` + endings).
**Output:** publish-ready game description (100–150 words) + tags list (comma-separated from master list).

Used when publishing the game to adult distribution sites (Gamcore, F95Zone, itch.io, etc.).

---

## §0 — Context

Per `00_LEGACY_IGNORE.md` §6.3: the game is an RTS-shape sandbox. The listing should sell THAT shape — not legacy framings like "Single-NPC Romance" or "Multi-NPC Parallel Arcs." Per LO's 7 locked decisions (Doc 66 §6), every game generated against `prompts_v2/` is RTS-shape.

The listing is the player's first contact with the game. Sell the tension; mention the mechanic ONCE.

---

## §1 — Input

Paste the game's TOML metadata below. At minimum include:

- `[project]` block (title, description)
- `[player]` block (name, description)
- `[[npcs]]` blocks (names, descriptions, arc_stages)
- Capstone canvas descriptions (per `[[canvases]]` with `is_repeatable = false` + `priority ≥ 9`)
- `[[quest_cards]]` (especially the terminal-card text + any branch-distinguishing text)
- Endings / branch flags from the chain
- Any `[settings]` blocks (rent, clothing, time, etc.)

```toml
[PASTE TOML HERE]
```

---

## §2 — Description rules

Write a game description (**100–150 words**):

- **Hook first** — open with the emotional gut-punch, not a setup paragraph
- **Sell the tension, not the mechanics** — the player should feel the stakes before they understand the systems
- **Write like a back-of-book blurb** — short paragraphs, punchy rhythm, incomplete sentences are fine
- **End with a sharp line** — number of endings, a question, or the core dilemma stated plainly
- **Mention the core mechanic once**, briefly (sandbox / daily life sim / open world)
- **No filler** — every sentence earns its place or gets cut

### §2.1 — Banned phrases

- "explore a world of"
- "immersive experience"
- "embark on a journey"
- "in this game you"
- "delve", "landscape", "robust", "seamless", "innovative", "cutting-edge", "captivating"
- "features include:" followed by a bullet list
- "will you choose X or Y?" as the final line (too generic — be specific to THIS game)

### §2.2 — Tone reference

**Good:**

> Fourteen mornings. Fourteen nights. The wedding doesn't move.

**Good:**

> Frank's house. Frank's rules. Frank's bed eventually.
>
> Your mother knows.

**Bad:**

> Experience an immersive 14-day romantic visual novel with multiple branching paths.

### §2.3 — RTS-shape framing

Per LO §6.1 — every game is RTS-shape. The listing should land the shape implicitly:

- Time pressure (rent / deadline / wedding / etc.)
- Multiple NPCs in parallel (cast the listing names ~3–5 of the most load-bearing NPCs)
- The world-clock (mornings + nights + days passing)
- Implicit choice surface ("Frank's bed eventually" implies the player chose vs. didn't)
- Endings count if branches matter (Pattern F capstones → multiple endings)

Don't say "RTS-shape sandbox" in the listing — that's authoring vocabulary, not marketing copy. Land the shape via the prose.

### §2.4 — Per-arc-shape listing hooks

Pull from the cast's mix:

- **Family/ambient NPC dominant** (Frank-like): paternal authority + house-rules tension + secret-then-open arc
- **Slow-burn family** (Jake-like): proximity + restraint + the line crossing once and never going back
- **Peer/dating** (Ryan-like): first-boyfriend tension + town-eyes + commit-or-walk
- **Service** (Marge-like): workplace bond + matriarch arc + after-hours
- **Antagonist** (Diana-like): the threat in the next room + the confrontation chain pulled toward

Pick the 2–3 most marketable hooks from the cast. Don't try to list all 6 NPCs in a 100-word blurb.

---

## §3 — Tag rules

Select tags from the master list (§5). **Do not invent tags.**

- **Order:** genre first, then content type, then specific acts, then platform, then meta
- **Include all that genuinely apply** — if the game has oral scenes, tag it; if it doesn't, don't
- **Skip aspirational tags** — only tag what's actually in the game
- **Output as comma-separated plain text**, one line

### §3.1 — Tag selection from TOML

Walk the TOML to derive tags:

| Tag category | Source in TOML |
|---|---|
| Genre tags (Adventure / Sandbox / Visual Novel / etc.) | `[project].description` + canvas count + lane mix |
| `Sandbox Games` | RTS-shape default (always include) |
| `Erotic Games`, `Porn Games`, `NSFW Games`, `18+`, `XXX Games`, `Adult` | Always include for RTS-shape sandboxes |
| Body-type tags (Big Tits, Petite, etc.) | `[player].description` |
| Hair-color tags (Blondes, Brunettes, Redheads) | `[player].description` |
| Act tags (Blowjobs, Oral Sex, Anal Sex, etc.) | Grep capstone canvas bodies + Lane 4 cascade prose |
| Family/incest tags (Incest, Cheating, MILF, etc.) | NPC `description` blocks + arc shape mix |
| Setting tags (Visual Novel, Time-Based Games, Sandbox Games) | Engine type + canvas distribution |
| Engine tag (HTML Games, Twine) | Always Twine/SugarCube |
| Platform tags (iOS Porn Games, APK, itchio) | Build target |

### §3.2 — Required tag set for RTS-shape sandboxes

Default for every RTS-shape generated game:
- `Sandbox Games`
- `Adult`
- `Erotic Games`
- `Porn Games`
- `18+`
- `XXX Games`
- `NSFW Games`
- `Female Protagonist` (since Maya is the player POV)
- `HTML Games`
- `Visual Novel`

Add per-game based on TOML content.

---

## §4 — Output format

```
DESCRIPTION:
[Your description here, 100-150 words]

TAGS:
[comma-separated tags from master list]
```

---

## §5 — Master tag list (Gamcore English)

Do not invent tags outside this list.

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

---

## §6 — Worked example (TLS slice listing)

Input (excerpt): TLS `7_final_game.toml` Frank arc + Marge hire + Diana confrontation.

Output:

```
DESCRIPTION:
Maya rents a room at Frank's house for the summer. Frank's wife Diana sleeps
down the hall. The rent is due Sunday.

Frank watches her. Maya feels it — the way he holds her gaze a beat longer than
he should. The way he stops at her back in the narrow kitchen instead of going by.

Forty days. Five capstone moments. Diana finds out eventually.

A sandbox arc with one big yes and one big no — and a lot of small decisions
between them. Stay through morning, or leave before dawn. Pay the rent in cash,
or in something else.

The house decides which Maya you become.

TAGS:
Sandbox Games, Adult, Erotic Games, Porn Games, 18+, XXX Games, NSFW Games,
Female Protagonist, HTML Games, Visual Novel, Incest, Cheating, MILF, Cuckold Games,
Pregnant, Vanilla Sex, Hardcore, Oral Sex, Blowjobs, Time-Based Games, Sex Stories
```

---

## §7 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 design book
- `stages/02_toml_generation_prompt.md` — Stage 2 TOML (provides this stage's input)
- `stages/03_image_finder_prompt.md` — media fetcher

### Source

- `prompts/game_listing_prompt.md` — legacy port source (rules preserved; banned-phrases + tone reference verbatim; tag master list verbatim; RTS-shape framing added)
- Doc 66 §6 — LO's 7 locked decisions (game is RTS-shape)
- `00_LEGACY_IGNORE.md` §3.5 — no "Single-NPC Romance vs Multi-NPC Parallel Arcs" framing

---

**End of file.** Run on a completed game's TOML to produce a publish-ready listing.
