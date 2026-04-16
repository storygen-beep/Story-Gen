#!/usr/bin/env node
// TEMPLATE — per-game play script for twine-game-explorer.
//
// To use: copy this file into game_explorations/<your_game_slug>/scripts/play.js
// and fill in the TODOs marked below. The skill's SKILL.md has the full
// authoring workflow; the short version:
//
//   1. Probe the game: open the URL in a browser, observe the DOM, note the
//      main-menu entry button, sidebar items, any icon-font buttons.
//   2. Fill in URL, GAME_NAME, ENTRY_TEXT, and CHROME_TEXTS below.
//   3. Run: `node play.js --budget-ms 300000 --fresh`
//   4. Inspect report.md and the cache in saves/. Add newly-discovered chrome
//      texts to CHROME_TEXTS and re-run if the script gets stuck.
//
// Reference working examples:
//   - ../../emilie_finds_a_way/scripts/play.js — SugarCube + icon-font nav
//   - ../../back_to_freedom/scripts/play.js    — heavy sidebar + icon nav
//   - ../../road_to_success/scripts/play.js    — emoji-labeled sidebar

'use strict';

const fs = require('fs');
const path = require('path');

// Resolve the installed skill (the toolkit lives there, not here).
const SKILL_DIR = '/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/.claude/skills/twine-game-explorer';
const { chromium } = require(path.join(SKILL_DIR, 'node_modules/playwright'));
const engineMod = require(path.join(SKILL_DIR, 'scripts/lib/engine'));
const stateMod = require(path.join(SKILL_DIR, 'scripts/lib/state'));
const setupMod = require(path.join(SKILL_DIR, 'scripts/lib/setup'));
const { Frontier } = require(path.join(SKILL_DIR, 'scripts/lib/frontier'));
const { Detector } = require(path.join(SKILL_DIR, 'scripts/lib/detector'));
const { SessionTracker, aggregateSessions } = require(path.join(SKILL_DIR, 'scripts/lib/session'));
const reportMod = require(path.join(SKILL_DIR, 'scripts/lib/report'));

// ========== PER-GAME CONFIG — FILL IN ==========

// TODO: set to the game's public URL (landing page, not the embed iframe).
const URL = 'https://example.com/your-game-here';

// TODO: short slug matching the parent directory name.
const GAME_NAME = 'your_game_slug';

// TODO: the text of the main-menu button that starts the story.
// Null if the game has no separate entry (opens directly into play).
const ENTRY_TEXT = null;

// TODO: text labels of sidebar / header / menu items that are NOT story
// progression. Add any text that repeatedly shows up on every passage and
// isn't plot-advancing. Grows as you discover more during early runs.
const CHROME_TEXTS = new Set([
  // Examples from common SugarCube UIs — keep or remove per your game:
  // 'Toggle the UI bar',
  // 'Options', 'Achievements', 'Gallery', 'Cheats', 'Guide',
  // 'Credits', 'Saves', 'Restart', 'Sandbox Mode', 'Changelog',
]);

// Many adult SugarCube games use icon-font glyphs (Unicode Private-Use Area,
// U+E000–U+F8FF) for back/forward nav arrows on every passage. Clicking them
// creates infinite loops. Leave this on unless you know the game doesn't use
// any icon-font text.
function isIconText(t) {
  if (!t) return true;
  for (const ch of t) {
    const code = ch.codePointAt(0);
    if (code < 0xE000 || code > 0xF8FF) return false;
  }
  return true;
}

// ========== END PER-GAME CONFIG ==========

// Budgets and cadences (reasonable defaults; override via CLI if needed).
const DEFAULT_BUDGET_MS = 10 * 60 * 1000;
const STALE_LIMIT = 5;
const CLICK_DELAY_MS = 1200;
const CHOICE_DELAY_MS = 1500;

// ---- CLI parsing ----

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = (argv[i + 1] && !argv[i + 1].startsWith('--')) ? argv[++i] : true;
      out[k.replace(/-/g, '_')] = v;
    }
  }
  return out;
}

const args = parseArgs(process.argv);
const BUDGET_MS = Number(args.budget_ms || DEFAULT_BUDGET_MS);
const FRESH = !!args.fresh;

// ---- Directory prep ----

const GAME_DIR = path.resolve(__dirname, '..'); // parent of the scripts/ folder

function prepareGameDir() {
  if (FRESH && fs.existsSync(GAME_DIR)) {
    const stamp = new Date().toISOString().replace(/[:.]/g, '-');
    const archive = path.join(GAME_DIR, 'archive', stamp);
    fs.mkdirSync(archive, { recursive: true });
    for (const f of fs.readdirSync(GAME_DIR)) {
      // Preserve the scripts folder and any archive folder across --fresh runs.
      if (f === 'archive' || f === 'scripts') continue;
      fs.renameSync(path.join(GAME_DIR, f), path.join(archive, f));
    }
  }
  for (const s of [
    'saves', 'sessions',
    'screenshots/scenes', 'screenshots/choices', 'screenshots/progress',
    'profile',
  ]) fs.mkdirSync(path.join(GAME_DIR, s), { recursive: true });
}
prepareGameDir();

// ---- Output paths ----

const PROFILE_DIR = path.join(GAME_DIR, 'profile');
const SESSIONS_DIR = path.join(GAME_DIR, 'sessions');
const FRONTIER_FILE = path.join(GAME_DIR, 'saves', 'frontier.jsonl');
const EXPLORED_FILE = path.join(GAME_DIR, 'saves', 'explored_hashes.txt');
const LATEST_STATE_FILE = path.join(GAME_DIR, 'saves', 'latest_state.json');
const TIMELINE_FILE = path.join(GAME_DIR, 'state_timeline.jsonl');
const CHOICE_GRAPH_FILE = path.join(GAME_DIR, 'choice_graph.json');
const LOG_FILE = path.join(GAME_DIR, 'session.log');

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  fs.appendFileSync(LOG_FILE, line + '\n');
}

async function snap(page, category, name) {
  try {
    const file = path.join(GAME_DIR, 'screenshots', category, `${Date.now()}_${name}.png`);
    await page.screenshot({ path: file });
    return file;
  } catch (e) { return null; }
}

// Explored-hash set (persists across sessions for resume).
const explored = new Set();
if (fs.existsSync(EXPLORED_FILE)) {
  for (const h of fs.readFileSync(EXPLORED_FILE, 'utf8').split('\n').filter(Boolean)) explored.add(h);
}
function markExplored(h) {
  if (explored.has(h)) return false;
  explored.add(h);
  fs.appendFileSync(EXPLORED_FILE, h + '\n');
  return true;
}

const choiceGraph = fs.existsSync(CHOICE_GRAPH_FILE)
  ? JSON.parse(fs.readFileSync(CHOICE_GRAPH_FILE, 'utf8'))
  : { nodes: {}, edges: [] };
function persistChoiceGraph() {
  fs.writeFileSync(CHOICE_GRAPH_FILE, JSON.stringify(choiceGraph, null, 2));
}

// ---- Game-specific DOM probing ----

/**
 * List visible, text-bearing, non-chrome interactive elements in the game frame.
 * Returns items with text + bbox + tag. Clicks happen via text-locator
 * (auto-scrolls into view, handles iframe offsets), so we don't need to filter
 * by viewport bounds.
 */
async function listClickables(frame) {
  const raw = await frame.evaluate(() => {
    const sel = 'button, a, input[type=button], input[type=submit], [onclick], [role=button]';
    const out = [];
    for (const el of document.querySelectorAll(sel)) {
      const r = el.getBoundingClientRect();
      if (r.width < 8 || r.height < 8) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
      const t = (el.textContent || '').trim();
      if (t.length > 240) continue;
      out.push({ t, x: r.x, y: r.y, w: r.width, h: r.height, tag: el.tagName.toLowerCase() });
    }
    return out;
  });
  return raw.filter((c) => {
    if (!c.t) return false;                    // empty-text icons = unclickable by text
    if (isIconText(c.t)) return false;         // private-use-area icon-font glyphs
    if (CHROME_TEXTS.has(c.t)) return false;   // per-game chrome set
    if (c.t.startsWith('http')) return false;  // external links (patreon/social)
    return true;
  });
}

/** Click an element by its exact text — Playwright auto-scrolls into view. */
async function clickByText(frame, text) {
  try {
    const loc = frame.getByText(text, { exact: true }).first();
    await loc.click({ timeout: 2000 });
    return true;
  } catch (e) {
    return false;
  }
}

// ---- Main ----

(async () => {
  log(`=== ${GAME_NAME} play session  budget=${BUDGET_MS}ms fresh=${FRESH} ===`);

  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--disable-popup-blocking'],
  });
  const page = context.pages()[0] || await context.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(3000);

  const setupResult = await setupMod.doSetup(page, context, { url: URL });
  const gameFrame = setupResult.frame;
  log(`setup: portal=${setupResult.adapter}`);

  // Wait for the engine to wire up — iframe reload after PLAY can be slow.
  let engineInfo = await engineMod.introspect(gameFrame);
  for (let attempt = 1; attempt <= 5 && engineInfo.engine === 'unknown'; attempt++) {
    log(`engine unknown (attempt ${attempt}), waiting 3s`);
    await page.waitForTimeout(3000);
    engineInfo = await engineMod.introspect(gameFrame);
  }
  log(`engine: ${engineInfo.engine} passage=${engineInfo.passage}`);
  if (engineInfo.saveCaps) log(`saveCaps: ${JSON.stringify(engineInfo.saveCaps)}`);

  // Entry kickoff (idempotent — fires only if the entry text is still visible).
  if (ENTRY_TEXT) {
    const begun = await clickByText(gameFrame, ENTRY_TEXT);
    if (begun) {
      log(`entered story via "${ENTRY_TEXT}"`);
      await page.waitForTimeout(2500);
    } else {
      log(`entry button "${ENTRY_TEXT}" not found — session likely resuming mid-story`);
    }
  }

  // --- Initialize tracking ---
  const frontier = new Frontier(FRONTIER_FILE);
  const detector = new Detector();
  const session = new SessionTracker(SESSIONS_DIR);
  session.setFrontierStart(frontier.size());

  let prevState = await engineMod.introspect(gameFrame);
  let prevHash = stateMod.hashState(prevState);
  if (markExplored(prevHash)) session.incNewUniqueState();
  detector.observeState({
    state_hash: prevHash, passage: prevState.passage,
    variables: prevState.variables, diff: null, timestamp: Date.now(),
  });
  fs.appendFileSync(TIMELINE_FILE, JSON.stringify({
    ts: Date.now(), hash: prevHash, passage: prevState.passage, session: session.id,
  }) + '\n');

  const started = Date.now();
  let staleTicks = 0;

  async function attemptBacktrack() {
    const next = frontier.pop();
    if (!next) {
      log('stale and frontier empty — pressing Enter as escape');
      await page.keyboard.press('Enter').catch(() => {});
      return;
    }
    const res = await engineMod.restore(page, gameFrame, next.snapshot, { reloadUrl: URL });
    if (res.ok) {
      log(`backtracked via ${res.method} to ${next.state_hash}`);
      prevState = await engineMod.introspect(gameFrame);
      prevHash = stateMod.hashState(prevState);
    } else {
      log(`backtrack restore failed: ${res.error}`);
    }
  }

  async function playStep() {
    const clickables = await listClickables(gameFrame);
    const nowState = await engineMod.introspect(gameFrame);
    const nowHash = stateMod.hashState(nowState);

    if (nowState.passage && /end|credits|game\s*over|the\s*end/i.test(nowState.passage)) {
      session.recordEnding(nowState.passage);
      log(`ending reached: ${nowState.passage}`);
    }

    if (clickables.length === 0) {
      staleTicks++;
      if (staleTicks >= STALE_LIMIT) {
        await attemptBacktrack();
        staleTicks = 0;
      }
      await page.waitForTimeout(CLICK_DELAY_MS);
      return;
    }

    if (clickables.length >= 2) {
      if (!choiceGraph.nodes[nowHash]) {
        choiceGraph.nodes[nowHash] = {
          passage: nowState.passage,
          options: clickables.map((c) => c.t),
          first_seen_session: session.id,
        };
      }
      const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
      const triedTexts = new Set(
        choiceGraph.edges.filter((e) => e.from === nowHash).map((e) => e.choice)
      );
      const notYet = clickables.filter((c) => !triedTexts.has(c.t));
      const pick = notYet[0] || clickables[0];
      const remaining = notYet.slice(1).map((c) => c.t);
      if (remaining.length) {
        frontier.push({
          state_hash: nowHash, choices_left: remaining, snapshot: snapBlob,
          depth: (session.record.choices_explored || 0) + 1, added_at: Date.now(),
        });
      }
      await snap(page, 'choices', `${nowHash}_${pick.t.slice(0, 30).replace(/[^a-z0-9]/gi, '_')}`);
      const ok = await clickByText(gameFrame, pick.t);
      log(`choice (${clickables.length} opts) → ${JSON.stringify(pick.t)} ok=${ok}`);
      choiceGraph.edges.push({
        from: nowHash, choice: pick.t, choice_type: 'branch',
        picked_at: new Date().toISOString(), session: session.id, to: null,
      });
      detector.observeChoice({
        passage: nowState.passage, classification: 'branch',
        options: clickables.map((c) => c.t), picked: pick.t, at_state_hash: nowHash,
      });
      session.recordChoice();
      session.recordClick();
      await page.waitForTimeout(CHOICE_DELAY_MS);
    } else {
      const pick = clickables[0];
      await clickByText(gameFrame, pick.t);
      session.recordArrow();
      session.recordClick();
      await page.waitForTimeout(CLICK_DELAY_MS);
    }

    const postState = await engineMod.introspect(gameFrame);
    const postHash = stateMod.hashState(postState);
    const diff = stateMod.diffVariables(prevState.variables, postState.variables);
    fs.appendFileSync(TIMELINE_FILE, JSON.stringify({
      ts: Date.now(), hash: postHash, passage: postState.passage,
      session: session.id,
      diff_changed: Object.keys(diff.changed),
      diff_added: Object.keys(diff.added),
    }) + '\n');

    const lastEdge = choiceGraph.edges[choiceGraph.edges.length - 1];
    if (lastEdge && lastEdge.to === null) lastEdge.to = postHash;

    if (markExplored(postHash)) {
      session.incNewUniqueState();
      await snap(page, 'scenes', postHash);
    }
    detector.observeState({
      state_hash: postHash, passage: postState.passage,
      variables: postState.variables, diff, timestamp: Date.now(),
    });

    if (postHash === prevHash) {
      staleTicks++;
      if (staleTicks >= STALE_LIMIT) {
        await attemptBacktrack();
        staleTicks = 0;
      }
    } else {
      staleTicks = 0;
    }

    prevState = postState;
    prevHash = postHash;
  }

  // Main loop
  let lastShotAt = 0, lastFlushAt = 0;
  while (Date.now() - started < BUDGET_MS) {
    try {
      await playStep();

      if (Date.now() - lastShotAt > 45 * 1000) {
        await snap(page, 'progress', 'tick_' + session.record.clicks);
        lastShotAt = Date.now();
        log(`tick ${Math.round((Date.now() - started) / 1000)}s clicks=${session.record.clicks} choices=${session.record.choices_explored} unique=${explored.size} frontier=${frontier.size()}`);
      }
      if (Date.now() - lastFlushAt > 30 * 1000) {
        persistChoiceGraph();
        session.setFrontierEnd(frontier.size());
        session.setUniqueStates(explored.size);
        session.flush();
        try {
          const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
          fs.writeFileSync(LATEST_STATE_FILE, JSON.stringify(snapBlob, null, 2));
        } catch (e) {}
        lastFlushAt = Date.now();
      }
    } catch (e) {
      log('step err: ' + e.message);
      await page.waitForTimeout(1500);
    }
  }

  // Finalize
  persistChoiceGraph();
  session.setFrontierEnd(frontier.size());
  session.setUniqueStates(explored.size);
  session.flush();
  try {
    const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
    fs.writeFileSync(LATEST_STATE_FILE, JSON.stringify(snapBlob, null, 2));
  } catch (e) {}

  const sessionsSummary = aggregateSessions(SESSIONS_DIR);
  reportMod.write(GAME_DIR, detector, frontier, explored.size, sessionsSummary, {
    gameName: GAME_NAME, url: URL,
    engine: engineInfo.engine, engineVersion: engineInfo.version,
    canMarshal: engineInfo.canMarshal,
  });
  log('report written');
  await snap(page, 'progress', 'zz_final');
  await page.waitForTimeout(2000);
  await context.close();
  log('=== session end ===');
})().catch((e) => {
  console.error('FATAL:', e);
  process.exit(1);
});
