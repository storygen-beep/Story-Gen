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

## Environment setup on Claude Code on the web

The cloud sandbox (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`) enforces a strict egress allowlist and ships a preinstalled Chromium under `/opt/pw-browsers/`. A cold run from a fresh session hits four predictable walls — here's the fix for each.

### 1. Allowlist the target host + the Playwright CDN

In **claude.ai/code → environment settings → Network access**, switch from **Trusted** to **Custom** (keep the "Also include default list" checkbox ticked) and add:

```
mopoga.com
*.mopoga.com
cdn.playwright.dev
```

`*.mopoga.com` covers the sub-CDN the game iframe pulls from. `cdn.playwright.dev` is only needed if the preinstalled chromium (see §3) doesn't match your Playwright version. Changes take effect on the **next** session — the running one stays on the old policy.

Verify from bash:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://mopoga.com/     # want 200/30x, NOT 403
```

A `HTTP/2 403` with `x-deny-reason: host_not_allowed` means the allowlist hasn't applied yet.

### 2. Install the skill's Node dependencies

From a fresh clone, `scripts/lib/` **is tracked** in the repo but `node_modules/` is not. Run:

```bash
cd .claude/skills/twine-game-explorer
npm install
```

If `npm install` fails with a 403 on a non-npmjs host, an npm dependency is reaching for a blocked CDN — re-check §1. The default npm registry (`registry.npmjs.org`) is already on the Trusted list.

### 3. Use the preinstalled Chromium (skip the 300 MB download)

`npx playwright install chromium` will 403 on `cdn.playwright.dev` unless you allowlisted it in §1. But the sandbox already has a Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (Chromium 141, Playwright revision 1194). Pin Playwright to the version that ships with that revision and point the binary path at `/opt/pw-browsers`:

```bash
cd .claude/skills/twine-game-explorer
npm install playwright@1.56       # 1.56 ships chromium rev 1194 — matches preinstall
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
```

If Playwright's bundled revision drifts from 1194, `npm install playwright@<matching-version>` — check `node_modules/playwright-core/browsers.json` for the revision each version expects.

### 4. Accept the sandbox's MITM TLS

The egress proxy terminates TLS with its own certificate. Chromium reports `ERR_CERT_AUTHORITY_INVALID` against any allowlisted HTTPS host unless the browser context ignores cert errors:

```js
await chromium.launchPersistentContext(userDataDir, {
  ignoreHTTPSErrors: true,
  args: ['--no-sandbox', '--ignore-certificate-errors'],
});
```

`scripts/live.js` should already handle this in `scripts/lib/setup.js`; mention it here because anyone wiring a fallback driver (e.g. `/tmp/explore_sultry.js` during a skill-broken session) will hit it immediately.

### Quick smoke test

After the four steps above, from a fresh session:

```bash
cd .claude/skills/twine-game-explorer && npm install && \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node scripts/live.js start --url https://mopoga.com/<slug> --slug <slug> --fresh
```

A successful start returns a JSON envelope with `passage`, `clickables`, and a `screenshot` path under `game_explorations/<slug>/screenshots/live/`. If it times out on "Daemon did not become ready," `tail game_explorations/<slug>/live.log` will show which of the four walls you hit.

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
