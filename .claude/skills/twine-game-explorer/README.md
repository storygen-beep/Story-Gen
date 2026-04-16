# twine-game-explorer

A Claude Code skill for systematically exploring online Twine/SugarCube/Harlowe/Chapbook interactive-fiction games and producing a deep mechanical analysis report.

Claude drives a visible browser through the game, reads the Twine engine's internal state on every click, explores every choice using engine-level snapshot + restore for backtracking, deduplicates by state hash, and writes a full report at `{output_folder}/{game_name}/`.

Sessions persist — each run resumes from the last exploration frontier. A 30-minute session today and a 30-minute session tomorrow together cover the same ground as a single 60-minute session, but split across calendar time.

## What you get in the output folder

```
{game_name}/
├── report.md                 synthesized report (regenerated each session)
├── mechanics.md              "what patterns is this game using?"
├── coverage.md               exploration progress
├── variable_schema.json      every engine variable, categorised
├── npcs.json                 per-NPC stats + scenes
├── items.json                detected items
├── body_changes.json         body / appearance transitions observed
├── scene_catalog.json        every unique passage classified
├── choice_graph.json         every decision point + options + transitions
├── state_timeline.jsonl      full state snapshot history
├── sessions/                 per-session metadata (timing, clicks, completion)
├── saves/                    frontier queue + explored-hash set + latest engine snapshot (for resume)
├── screenshots/              scenes/, choices/, progress/
├── profile/                  persistent browser profile (cookies, localStorage)
└── session.log
```

## Install

```bash
cd .claude/skills/twine-game-explorer
npm install
```

Requires Node 18+. Will use the Chromium binary installed by `playwright-skill` if present; otherwise install it via `npx playwright install chromium`.

## Run manually

```bash
node scripts/explore.js \
  --url "https://mopoga.com/back-to-freedom" \
  --name "back_to_freedom" \
  --out "/absolute/path/to/game_explorations" \
  --budget-ms 1800000
```

Flags:
- `--url` (required): game URL
- `--name` (required): slug used as folder name
- `--out` (required): parent folder; skill writes to `{out}/{name}/`
- `--budget-ms`: wall-clock ms per session (default 1,800,000 = 30 min)
- `--fresh`: archive existing data and start clean (otherwise resumes)

Or, just ask Claude: *"play and map this twine game: https://example.com/some-game, output to /some/folder"* — the skill's description triggers it.

## Design choices

See `SKILL.md` for the model-facing instructions, `references/engines.md` for engine-API details, and `references/detection_patterns.md` for the heuristics used.

## Content note

The skill is engine-agnostic and will run against any Twine-family game, including adult ones. The report describes **mechanical patterns only** — stat systems, choice structures, scene classifications, variable schemas. It does not transcribe narrative text. Screenshots are preserved for manual review.
