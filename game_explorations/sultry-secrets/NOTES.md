# Sultry Secrets — exploration attempt (blocked)

**Target:** https://mopoga.com/sultry-secrets
**Date:** 2026-04-16
**Outcome:** Unable to reach the game from this sandbox.

## Blockers encountered

1. **`twine-game-explorer` skill install is incomplete.** `scripts/live.js` imports
   from `scripts/lib/{engine,state,setup,choices,frontier,detector,session,report,ui_recon,passage_catalog,engine_config}`
   but the entire `scripts/lib/` directory is absent from the checkout. The
   legacy `scripts/explore.js` has the same problem. Daemon crashes on startup
   with `Cannot find module '.../scripts/lib/engine'` (see `live.log`).

2. **Playwright browser CDN is blocked.** `npx playwright install chromium`
   returns `403 Host not in allowlist` against `cdn.playwright.dev`. Worked
   around by pointing `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` at the
   preinstalled chromium-1194 and using `playwright@1.56` to match.

3. **Target host `mopoga.com` is blocked.** Even after getting a local
   Chromium working, navigation to `https://mopoga.com/sultry-secrets` lands
   on a `Host not in allowlist` error page served by the sandbox's outbound
   proxy. See `manual/shots/003_portal.png`.

## What's in this directory

- `manual/play_log.jsonl` — JSONL trail of every navigation attempt (with the
  gateway 403 recorded).
- `manual/shots/*.png` — screenshots from the attempts; the only useful one is
  the blocked-portal page confirming the network rejection.
- `live.log` — twine-game-explorer daemon crash trace (missing `scripts/lib/`).

## To unblock a future run

Any one of:
- Add `mopoga.com` (and its asset CDN) to the sandbox network allowlist.
- Host the game on an already-allowlisted domain and re-run against that URL.
- Restore the missing `scripts/lib/` files in the skill — the SKILL.md
  describes eleven modules that need to exist for either `live.js` or
  `explore.js` to boot.

The Chromium install at `/opt/pw-browsers/chromium-1194` works once network
access is granted; `playwright@1.56` pairs with it (package.json pins `^1.57`
which needs the blocked CDN — downgrade or pre-stage the newer browser).
