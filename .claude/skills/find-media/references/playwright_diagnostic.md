# Playwright Diagnostic (failure-only)

Use Playwright MCP ONLY when the harvest script fails in a way that needs a human-in-the-loop debug session — usually because a site changed its DOM or anti-bot behavior.

## Non-goal: never use MCP for the hot path

The harvest script (`scripts/nsfw_harvest.js`) processes 3–5 items per Playwright page load. Playwright MCP ships an accessibility snapshot per action — that's ~30× the token cost for the same batch. Microsoft itself now recommends Playwright CLI over MCP for coding agents because CLI uses 4× fewer tokens.

If you're tempted to use MCP because "it's easier than editing the script," stop. The script IS the easier path when it works. MCP is only for when the script is broken and you need to figure out why.

## When to spawn MCP

Three specific failure modes:

1. **Age gate broke** — the harvest script returns 0 candidates and the log shows the age-gate click timeout. PornHub changed the button text or selector. MCP → open the page, Read the snapshot, identify the new selector, patch the script.
2. **DOM extraction returning empty** — `data-webm` / `data-mp4` attributes on `<video>` elements returned null. Site moved to lazy-loading or restructured the results grid. MCP → navigate to the search results, Read the snapshot, find where the data moved.
3. **New source trial** — user asks "can we also pull from <new site>?" MCP → poke around, understand the flow, THEN write a new script. Don't build the script until MCP has confirmed the flow works.

Outside these three cases, debugging by reading `scripts/nsfw_harvest.js` output is faster than spawning a browser.

## One-time MCP setup

Tor-routed, for when the failure is NSFW-side:

```bash
claude mcp add playwright npx '@playwright/mcp@latest' -- --proxy-server socks5://127.0.0.1:9050
```

Important: use `socks5://`, NOT `socks5h://`. There's a documented Playwright bug where `socks5h://localhost:9050` throws `ERR_NO_SUPPORTED_PROXIES`. Chromium's SOCKS5 client already routes DNS through the proxy, so `socks5://` achieves DNS-through-Tor without the bug.

For SFW-side debugging (GIPHY/Unsplash/etc), no proxy is needed — install MCP without the `--proxy-server` flag, or add a second MCP entry:

```bash
claude mcp add playwright-direct npx '@playwright/mcp@latest'
```

MCP can be removed when debugging is done:

```bash
claude mcp remove playwright
```

## The debug loop (template)

When a specific failure triggers MCP use:

1. **Reproduce the failure** — run `scripts/nsfw_harvest.js` with the failing query so you have concrete error output
2. **Spawn MCP** — navigate to the same URL the script targeted
3. **Take a snapshot** — `browser_snapshot` returns the accessibility tree
4. **Identify the fix** — compare the snapshot to what the script expected. Common diffs:
   - Button text changed (age gate)
   - Selector moved (results moved from `<li>` to `<article>`)
   - Data attribute renamed (`data-webm` → `data-video-src`)
5. **Patch the script** — edit `scripts/nsfw_harvest.js`. Keep the change minimal — don't rewrite the script, just fix the specific extraction.
6. **Re-run the script** — verify the fix works against the failing query AND at least one previously-working query (regression check)
7. **Remove MCP if done** — `claude mcp remove playwright`

## Handoff pattern

MCP finds the fix → patch the script → future runs use the cheap script path.

Do NOT leave the pipeline routing through MCP. The goal of the diagnostic phase is to restore the hot-path script, not to permanently migrate to MCP.

## Exploratory pattern (new source)

When adding a new media source, Simon Willison's lesson applies: "have it show you a login page, then login yourself with your own credentials and tell it what to do next. Cookies will persist for the duration of the session." This is the one case where MCP's visible-browser approach wins over scripting.

Pattern:
1. Install MCP without `--headless` so you see the browser
2. Navigate to the new source, handle any age gate or login yourself
3. Ask Claude to search for a test query and extract the relevant data structure
4. Claude proposes a Node script that does the same thing headlessly
5. Verify the script works for a few queries
6. Add the script as `scripts/<source>_harvest.js`
7. Update `references/nsfw_pipeline.md` or `references/sfw_pipeline.md` to list the new source
8. Remove MCP

MCP is the training wheels, not the bike.
