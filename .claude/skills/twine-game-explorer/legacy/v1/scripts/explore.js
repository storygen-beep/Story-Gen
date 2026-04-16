#!/usr/bin/env node
// Main exploration driver.
//
// Usage:
//   node scripts/explore.js --url <URL> --name <game_name> --out <output_folder> [--budget-ms <N>] [--fresh]
//
// Side-effects:
//   Writes everything under {output_folder}/{game_name}/. See SKILL.md for directory layout.
//   Session state persists across invocations — re-running continues the DFS from the frontier.

'use strict';

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const engineMod = require('./lib/engine');
const stateMod = require('./lib/state');
const choicesMod = require('./lib/choices');
const setupMod = require('./lib/setup');
const { Frontier } = require('./lib/frontier');
const { Detector } = require('./lib/detector');
const { SessionTracker, aggregateSessions } = require('./lib/session');
const reportMod = require('./lib/report');

// --- CLI parsing ---
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
if (!args.url || !args.name) {
  console.error('Usage: explore.js --url <URL> --name <game_name> --out <folder> [--budget-ms N] [--fresh]');
  process.exit(2);
}

const URL = args.url;
const GAME_NAME = args.name;
const OUT_ROOT = args.out || path.join(require('os').homedir(), 'twine-explorer');
const GAME_DIR = path.join(OUT_ROOT, GAME_NAME);
const BUDGET_MS = Number(args.budget_ms || 30 * 60 * 1000);
const FRESH = !!args.fresh;

// --- Prepare directories ---
if (FRESH && fs.existsSync(GAME_DIR)) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const archive = path.join(GAME_DIR, 'archive', stamp);
  fs.mkdirSync(archive, { recursive: true });
  for (const f of fs.readdirSync(GAME_DIR)) {
    if (f === 'archive') continue;
    fs.renameSync(path.join(GAME_DIR, f), path.join(archive, f));
  }
}
const SUBS = ['saves', 'sessions', 'screenshots/scenes', 'screenshots/choices', 'screenshots/progress', 'profile'];
for (const s of SUBS) fs.mkdirSync(path.join(GAME_DIR, s), { recursive: true });

const PROFILE_DIR = path.join(GAME_DIR, 'profile');
const SESSIONS_DIR = path.join(GAME_DIR, 'sessions');
const FRONTIER_FILE = path.join(GAME_DIR, 'saves', 'frontier.jsonl');
const EXPLORED_FILE = path.join(GAME_DIR, 'saves', 'explored_hashes.txt');
const LATEST_STATE_FILE = path.join(GAME_DIR, 'saves', 'latest_state.json');
const TIMELINE_FILE = path.join(GAME_DIR, 'state_timeline.jsonl');
const CHOICE_GRAPH_FILE = path.join(GAME_DIR, 'choice_graph.json');
const LOG_FILE = path.join(GAME_DIR, 'session.log');
const DOM_DUMP = path.join(GAME_DIR, 'dom_recon.json');

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

// Load explored hashes
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

// Load existing choice graph (merge)
const choiceGraph = fs.existsSync(CHOICE_GRAPH_FILE)
  ? JSON.parse(fs.readFileSync(CHOICE_GRAPH_FILE, 'utf8'))
  : { nodes: {}, edges: [] };
function persistChoiceGraph() {
  fs.writeFileSync(CHOICE_GRAPH_FILE, JSON.stringify(choiceGraph, null, 2));
}

// --- Main ---
(async () => {
  log(`=== twine-explorer session start  game=${GAME_NAME}  url=${URL}  budget=${BUDGET_MS}ms ===`);

  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--disable-popup-blocking'],
  });

  let page = context.pages()[0] || await context.newPage();

  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(3000);
  await snap(page, 'progress', 'landing');

  // Derive the portal host (for stray-popup killing)
  const host = (() => { try { return new URL(URL).host; } catch (e) { return ''; } })();
  const gameFrame = await setupMod.doSetup(page, context, { targetDomain: host });
  log(`setup complete; game frame: ${gameFrame.url()}`);

  // Engine detection
  const engineInfo = await engineMod.introspect(gameFrame);
  log(`engine: ${engineInfo.engine} v${engineInfo.version || '?'}  canMarshal=${engineInfo.canMarshal}  passage=${engineInfo.passage}`);

  if (engineInfo.engine === 'unknown') {
    log('WARNING: engine not recognized — state hashing will rely on DOM text only, and backtracking is disabled beyond path-replay.');
  }

  // Compute sidebar edge from iframe bounding box (for choice filtering)
  const iframeEl = page.locator('iframe').first();
  const frameBox = (await iframeEl.boundingBox().catch(() => null)) || { x: 0, y: 0, width: 1440, height: 900 };
  const SIDEBAR_RIGHT = Math.max(140, frameBox.width * 0.14);
  let diagDumps = 0;

  // Initialize state-tracking primitives
  const frontier = new Frontier(FRONTIER_FILE);
  const detector = new Detector();
  const session = new SessionTracker(SESSIONS_DIR);
  session.setFrontierStart(frontier.size());

  // Prior state for diffing
  let prevState = await engineMod.introspect(gameFrame);
  let prevHash = stateMod.hashState(prevState);
  if (markExplored(prevHash)) session.incNewUniqueState();
  detector.observeState({ state_hash: prevHash, passage: prevState.passage, variables: prevState.variables, diff: null, timestamp: Date.now() });
  fs.appendFileSync(TIMELINE_FILE, JSON.stringify({ ts: Date.now(), hash: prevHash, passage: prevState.passage, vars_hash: prevHash }) + '\n');

  const started = Date.now();
  let staleTicks = 0;
  let lastMenuTexts = null;

  // If frontier has entries (resume scenario), restore from top entry at kickoff
  if (frontier.size() > 0) {
    log(`resuming from persistent frontier (${frontier.size()} entries)`);
  }

  // Helper: take one exploration step
  async function exploreStep() {
    // Scroll to bottom so any advance button at page bottom is in view
    await choicesMod.scrollToBottom(gameFrame);

    const items = await choicesMod.listInteractive(gameFrame);
    const filtered = choicesMod.filterToContentRegion(items, { sidebarRightEdge: SIDEBAR_RIGHT, frameWidth: frameBox.width });
    const uniq = choicesMod.dedupByText(filtered);
    const klass = choicesMod.classify(uniq, { priorMenu: lastMenuTexts });

    if (diagDumps < 3) {
      diagDumps++;
      const compact = items.map((i) => ({ t: i.t.slice(0, 60), x: i.x, y: i.y, w: i.w, h: i.h, tag: i.tag }));
      log(`DIAG tick${diagDumps} frameW=${Math.round(frameBox.width)} sidebarL=${Math.round(SIDEBAR_RIGHT)} rawItems=${items.length} kept=${uniq.length}`);
      log(`DIAG items: ${JSON.stringify(compact.slice(0, 30))}`);
      if (filtered._rejected) log(`DIAG rejected: ${JSON.stringify(filtered._rejected.slice(0, 15))}`);
    }

    const nowState = await engineMod.introspect(gameFrame);
    const nowHash = stateMod.hashState(nowState);
    const sameAsPrev = nowHash === prevHash;

    // Is this a real decision point?
    const isDecision = ['branch', 'payment', 'quiz', 'location', 'other'].includes(klass.type) && uniq.length >= 2;
    const isActionLoop = klass.type === 'action_loop';

    if (isDecision && !sameAsPrev) {
      // Record the choice node in the graph
      if (!choiceGraph.nodes[nowHash]) {
        choiceGraph.nodes[nowHash] = { passage: nowState.passage, options: uniq.map((u) => u.t), type: klass.type, first_seen_session: session.id };
      }
      // Take snapshot for backtracking before picking
      const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });

      // Choose which unexplored option to try first
      const priorNode = choiceGraph.nodes[nowHash];
      const triedTexts = new Set((choiceGraph.edges.filter((e) => e.from === nowHash)).map((e) => e.choice));
      const notYet = uniq.filter((u) => !triedTexts.has(u.t));
      const pick = notYet[0] || uniq[0];

      // Push frontier entry for the REMAINING options (those we won't try this tick)
      const remaining = notYet.slice(1).map((u) => u.t);
      if (remaining.length) {
        frontier.push({
          state_hash: nowHash,
          choices_left: remaining,
          snapshot: snapBlob,
          depth: (session.record.choices_explored || 0) + 1,
          added_at: Date.now(),
        });
      }

      // Click the chosen option
      const pickIdx = uniq.findIndex((u) => u.t === pick.t);
      await snap(page, 'choices', `${nowHash}_${pickIdx}_${pick.t.slice(0, 30).replace(/[^a-z0-9]/gi, '_')}`);
      try {
        await page.mouse.click(frameBox.x + pick.x + pick.w / 2, frameBox.y + pick.y + pick.h / 2);
      } catch (e) { log('click fail: ' + e.message); }

      // Edge (from, choice, to, diff) filled after observing post-click state
      choiceGraph.edges.push({ from: nowHash, choice: pick.t, choice_type: klass.type, picked_at: new Date().toISOString(), session: session.id, to: null });
      detector.observeChoice({
        passage: nowState.passage, classification: klass.type, options: uniq.map((u) => u.t),
        picked: pick.t, prices: (klass.meta && klass.meta.prices) || null, at_state_hash: nowHash,
      });
      session.recordChoice();
      session.recordClick();
      lastMenuTexts = uniq.map((u) => u.t);
      await page.waitForTimeout(1800);
    } else if (isActionLoop) {
      // Sample once: pick first option, note that this is an action loop, don't enumerate
      if (!choiceGraph.nodes[nowHash]) {
        choiceGraph.nodes[nowHash] = { passage: nowState.passage, options: uniq.map((u) => u.t), type: 'action_loop', first_seen_session: session.id, note: 'action loop — sampled once' };
      }
      const pick = uniq[0];
      try {
        await page.mouse.click(frameBox.x + pick.x + pick.w / 2, frameBox.y + pick.y + pick.h / 2);
      } catch (e) {}
      detector.observeChoice({
        passage: nowState.passage, classification: 'action_loop', options: uniq.map((u) => u.t),
        picked: pick.t, prices: null, at_state_hash: nowHash,
      });
      session.recordClick();
      lastMenuTexts = uniq.map((u) => u.t);
      await page.waitForTimeout(1500);
    } else {
      // Advance: use arrow / bottom-most interactive / blind click
      const adv = choicesMod.pickAdvance(filtered, { sidebarRightEdge: SIDEBAR_RIGHT, frameWidth: frameBox.width });
      if (adv) {
        try {
          await page.mouse.click(frameBox.x + adv.x + adv.w / 2, frameBox.y + adv.y + adv.h / 2);
        } catch (e) {}
        session.recordArrow();
      } else {
        const cx = SIDEBAR_RIGHT + (frameBox.width - SIDEBAR_RIGHT) / 2;
        const cy = frameBox.y + frameBox.height - 60;
        try { await page.mouse.click(cx, cy); } catch (e) {}
      }
      session.recordClick();
      await page.waitForTimeout(1400);
    }

    // Post-click state observation
    const postState = await engineMod.introspect(gameFrame);
    const postHash = stateMod.hashState(postState);
    const diff = stateMod.diffVariables(prevState.variables, postState.variables);
    fs.appendFileSync(TIMELINE_FILE, JSON.stringify({
      ts: Date.now(), hash: postHash, passage: postState.passage,
      session: session.id,
      diff_changed: Object.keys(diff.changed),
      diff_added: Object.keys(diff.added),
    }) + '\n');

    // Update graph edge "to"
    const lastEdge = choiceGraph.edges[choiceGraph.edges.length - 1];
    if (lastEdge && lastEdge.from === nowHash && lastEdge.to === null) lastEdge.to = postHash;

    // Detector
    if (markExplored(postHash)) {
      session.incNewUniqueState();
      await snap(page, 'scenes', postHash);
    }
    detector.observeState({ state_hash: postHash, passage: postState.passage, variables: postState.variables, diff, timestamp: Date.now() });

    // Ending detection — very rough: passage name contains "ending" / "game over"
    if (postState.passage && /end|credits|game\s*over|the\s*end/i.test(postState.passage)) {
      session.recordEnding(postState.passage);
      log(`ending reached: ${postState.passage}`);
    }

    // Stale detection: if post == prev (no state change), increment stale counter
    if (postHash === prevHash) {
      staleTicks++;
      if (staleTicks >= 5) {
        log(`stale x${staleTicks} — trying backtrack from frontier`);
        const nextEntry = frontier.pop();
        if (nextEntry) {
          // Restore
          const res = await engineMod.restore(page, gameFrame, nextEntry.snapshot, { reloadUrl: URL });
          if (res.ok) {
            log(`restored via ${res.method} to state ${nextEntry.state_hash}`);
            staleTicks = 0;
          } else {
            log('restore failed: ' + (res.error || 'unknown'));
          }
        } else {
          // No frontier left; try dismissing modals first, then advance via Enter
          await page.keyboard.press('Escape').catch(() => {});
          await page.waitForTimeout(300);
          await page.keyboard.press('Enter').catch(() => {});
          staleTicks = 0;
        }
      }
    } else {
      staleTicks = 0;
    }

    prevState = postState;
    prevHash = postHash;
  }

  // Periodic snapshots + persistence
  let lastProgressShot = 0;
  let lastFlush = 0;

  while (Date.now() - started < BUDGET_MS) {
    try {
      await exploreStep();

      if (Date.now() - lastProgressShot > 45 * 1000) {
        await snap(page, 'progress', 'tick_' + session.record.clicks);
        lastProgressShot = Date.now();
        log(`tick ${Math.round((Date.now() - started) / 1000)}s  clicks=${session.record.clicks} choices=${session.record.choices_explored} unique=${explored.size} frontier=${frontier.size()}`);
      }
      if (Date.now() - lastFlush > 30 * 1000) {
        persistChoiceGraph();
        session.setFrontierEnd(frontier.size());
        session.setUniqueStates(explored.size);
        session.flush();
        // Persist latest state snapshot so resume can short-cut
        try {
          const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
          fs.writeFileSync(LATEST_STATE_FILE, JSON.stringify(snapBlob, null, 2));
        } catch (e) {}
        lastFlush = Date.now();
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

  // Generate reports
  const sessionsSummary = aggregateSessions(SESSIONS_DIR);
  reportMod.write(GAME_DIR, detector, frontier, explored.size, sessionsSummary, {
    gameName: GAME_NAME, url: URL, engine: engineInfo.engine, engineVersion: engineInfo.version, canMarshal: engineInfo.canMarshal,
  });
  log(`report written to ${path.join(GAME_DIR, 'report.md')}`);

  await snap(page, 'progress', 'zz_final');
  log('=== session end ===');
  await page.waitForTimeout(2000);
  await context.close();
})().catch((e) => {
  console.error('FATAL:', e);
  process.exit(1);
});
