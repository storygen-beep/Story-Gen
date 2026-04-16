# Feature detection patterns

Heuristics the `Detector` uses to classify variables and choices. Load this when the report's inventory has wrong/missing categories.

## Variable categories (from name + type)

Order of precedence (first match wins):

1. **body** — regex: `breast|bust|boob|cup|hair|body|weight|height|skin|tan|belly|pregnancy|piercing|tattoo|scar|outfit|clothing|makeup|nails|age`
2. **npc_stat** — regex: `love|lust|trust|respect|friendship|affection|corruption|submission|dominance|obedience|fear|jealousy|arousal`
3. **player_stat** — regex: `money|cash|gold|energy|stamina|sleep|hunger|fatigue|willpower|composure|charisma|intelligence|strength|dexterity|fitness|beauty|reputation|fame|skill`
4. **time** — regex: `day|hour|week|month|year|turn|time|calendar|morning|evening|night|afternoon|weekday`
5. **flag** — name ends with `_unlocked|_complete|_seen|_met|_first|_started|_done|_known|flag` OR value type is boolean
6. **list** — value is an Array → likely inventory
7. **structure** — value is a non-null object → likely nested per-NPC or per-scene record
8. **scalar** — any remaining number
9. **misc** — fallback

Caveats: the same regex can match in different contexts. For example a game with variable `hair_choices` (a list of hair colors) would match `body` first and land in the wrong bucket. The report includes all samples so reviewers can reclassify. We prefer over-classifying and letting the human correct.

## NPC detection

Two paths:

**Path A: nested variable structure**
If a variable path looks like `npcs.<Name>.<stat>` or `characters.<Name>.<stat>` or `relations.<Name>.<stat>` or `girls.<Name>.<stat>` AND `<stat>` matches an NPC-stat regex, record `<Name>` as an NPC and add `<stat>` to its stats set.

**Path B: mention in choice text**
Regex: `\b(?:with|to|at)\s+([A-Z][a-z]+)(?:'s)?`
e.g., "Go to Angela's room" → candidate NPC "Angela"
Filter out common noise: MC, Smith, Home, Back, Menu, Cancel, etc.

Combine both; the NPC table in the report lists both sources.

## Choice type classification

Applied to a deduplicated set of visible choice texts:

| Type | Pattern |
|---|---|
| `advance` | exactly one option; text is arrow character (▶ → ›) or contains "continue"/"next" |
| `quiz` | 2–6 options, all single letter/digit (a/b/c/d/1/2/3/4) |
| `payment` | any option text contains `$<digits>` |
| `location` | all options start with `go to|enter|head to|visit|walk to` |
| `action_loop` | ≥4 options, ≥50% match a verb from the action lexicon (lick/kiss/tease/strip/fuck/…); OR same menu seen two ticks in a row |
| `branch` | 2–8 options, none of the above |
| `other` | fallback if above don't apply |

Action lexicon (tuned for adult/combat games, extensible): `lick kiss grope fondle tease strip undress fuck deepthroat blowjob footjob titjob handjob make her cum end continue stand cowgirl doggy missionary anal reverse cowgirl sideway touch slap punish praise command reward`

## Economy heuristics

- **Price observation**: any choice where text matches `\$\d+` — parse the integer
- **Income event**: state diff where a money-like variable increased (delta > 0)
- **Expense event**: same variable decreased

Money-like variable names: `money | cash | gold | balance`

## Body-change transitions

When a variable whose name matches body regex changes value across a single click, log:
```json
{ "var": "breast_size", "before": 2, "after": 3, "at_passage": "...", "at_state_hash": "..." }
```

Useful for finding the exact choice that triggers a body transformation.

## Scene classification

Each unique passage is tagged with its first-seen classification from the choice type that appeared in it. Over sessions, the classification can be refined (a passage that looked like "branch" on first visit may be reclassified as "action_loop" if the same options reappear next visit).

## Flag chain detection

For each boolean variable that transitions from false→true, look backwards in `state_timeline.jsonl` for other boolean variables that were true at that moment. Build adjacency: "when X went true, Y and Z were already true". This approximates the flag-chain prerequisite graph without needing to parse the game's source.

Output goes in `flag_chains.json` (optional; only written if any chains are detected).

## Tuning knobs

If a game's variables don't match these patterns:
- Add terms to the category regexes at the top of `scripts/lib/detector.js`
- Add action verbs to `ACTION_VERB_RE` in `scripts/lib/choices.js`
- Add nav terms to `LOCATION_RE`
- Tighten / loosen price regex if a game uses non-dollar currency
