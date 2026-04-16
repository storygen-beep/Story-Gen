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

const { V1HeuristicClassifier } = require('./lib/classifiers/v1_heuristic');
const { V2BehavioralClassifier } = require('./lib/classifiers/v2_behavioral');

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
// Default output folder lives inside the project's game_explorations/ so runs
// are co-located with the rest of the design-analysis work. Override with --out.
const DEFAULT_OUT = '/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/game_explorations';
const OUT_ROOT = args.out || DEFAULT_OUT;
const GAME_DIR = path.join(OUT_ROOT, GAME_NAME);
const BUDGET_MS = Number(args.budget_ms || 30 * 60 * 1000);
const CLASSIFIER_CHOICE = (args.classifier || 'v2').toLowerCase();
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

  const setupResult = await setupMod.doSetup(page, context, { url: URL });
  let gameFrame = setupResult.frame;
  log(`setup: portal=${setupResult.adapter} result=${JSON.stringify(setupResult.adapter_result)}`);
  log(`game frame: ${gameFrame.url()}`);

  // Engine detection with retry — iframe may reload its scripts shortly after
  // setup returns, so the first introspect can catch the frame before the
  // engine global is wired up. Retry with a fresh frame handle each time.
  let engineInfo = await engineMod.introspect(gameFrame);
  for (let attempt = 1; attempt <= 5 && engineInfo.engine === 'unknown'; attempt++) {
    log(`engine detection attempt ${attempt}: still unknown, waiting 3s`);
    await page.waitForTimeout(3000);
    // Re-fetch the game frame in case the iframe was replaced
    gameFrame = await setupMod.findGameFrame(page, { engineTimeoutMs: 1000 });
    engineInfo = await engineMod.introspect(gameFrame);
  }
  log(`engine: ${engineInfo.engine} v${engineInfo.version || '?'}  canMarshal=${engineInfo.canMarshal}  passage=${engineInfo.passage}`);
  if (engineInfo.saveCaps) log(`saveCaps: ${JSON.stringify(engineInfo.saveCaps)}`);

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

  // Classifier — decides which elements are real decisions vs chrome.
  // v2 (behavioral) is the default; v1 (regex) is preserved for comparison.
  let classifier;
  if (CLASSIFIER_CHOICE === 'v1') {
    classifier = new V1HeuristicClassifier({ workDir: GAME_DIR, log });
  } else {
    classifier = new V2BehavioralClassifier({ workDir: GAME_DIR, log });
  }
  await classifier.load();
  log(`classifier: ${classifier.name()} — ${classifier.describe()}`);

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

  // Helper: click a candidate element via Playwright's locator API when possible
  // (auto-scrolls into view, handles iframe offsets, checks actionability), with
  // coordinate-based fallback for icon-only or duplicate-text elements.
  //
  // Returns { ok, method } — ok=false means the click never reached a real
  // element, so observeOutcome should NOT burn it as chrome.
  async function clickCandidate(elem) {
    const text = (elem.t || '').trim();
    // Try locator-by-text first when we have unambiguous text (<120 chars,
    // non-empty). Playwright will scroll the target into view through nested
    // scroll containers AND translate iframe coords — both fix our offscreen
    // problems for free.
    if (text && text.length <= 120) {
      try {
        const loc = gameFrame.getByText(text, { exact: true }).first();
        await loc.click({ timeout: 2000 });
        return { ok: true, method: 'locator:text' };
      } catch (e) {
        // Fall through to coord click
      }
    }
    // Coord fallback — only dispatch if the element is actually inside the
    // iframe viewport. Elements at y<0 (scrolled above) or y>frameBox.height
    // (below) lead to misdirected clicks that burn good elements.
    const inViewport =
      elem.y >= 0 && elem.y + (elem.h || 0) <= frameBox.height + 20 &&
      elem.x >= 0 && elem.x + (elem.w || 0) <= frameBox.width + 20;
    if (!inViewport) {
      return { ok: false, method: 'coord:offscreen_skipped' };
    }
    try {
      await page.mouse.click(
        frameBox.x + elem.x + (elem.w || 0) / 2,
        frameBox.y + elem.y + (elem.h || 0) / 2,
      );
      return { ok: true, method: 'coord' };
    } catch (e) {
      return { ok: false, method: 'coord:error', error: e.message };
    }
  }

  // Helper: take one exploration step (classifier-driven)
  async function exploreStep() {
    // Note: we deliberately do NOT scrollToBottom() every tick. Games like
    // Emilie Finds a Way have primary entry buttons at the top of the scroll
    // container; scrolling to bottom puts them at y<0 and renders them
    // unreachable. The locator-first click path auto-scrolls into view as
    // needed, which handles both top-anchored and bottom-anchored UIs.

    const rawItems = await choicesMod.listInteractive(gameFrame);
    // Pre-filter: drop items clearly outside the reachable content region
    // (left/right sidebars, oversized containers, off-screen above/below). This
    // prevents the classifier from trying to click elements whose coordinates
    // would miss, which otherwise gets them burned as chrome.
    const items = choicesMod.filterToContentRegion(rawItems, {
      sidebarRightEdge: SIDEBAR_RIGHT,
      frameWidth: frameBox.width,
      frameHeight: frameBox.height,
    });
    const nowState = await engineMod.introspect(gameFrame);
    const nowHash = stateMod.hashState(nowState);

    const result = await classifier.classify(items, {
      frame: gameFrame,
      frameBox,
      sidebarRightEdge: SIDEBAR_RIGHT,
      passage: nowState.passage,
      priorMenu: lastMenuTexts,
      session,
    });

    // Log DIAG only on first 3 ticks that have non-empty item lists, so we capture
    // real page state — not empty frames before the iframe finishes rendering.
    if (diagDumps < 3 && rawItems.length > 0) {
      diagDumps++;
      const compact = items.map((i) => ({ t: (i.t || '').slice(0, 60), x: i.x, y: i.y, w: i.w, h: i.h, tag: i.tag }));
      log(`DIAG tick${diagDumps} classifier=${classifier.name()} raw=${rawItems.length} keptByFilter=${items.length} decisions=${result.decisions.length} advance=${result.advance ? JSON.stringify((result.advance.t || '').slice(0, 40)) : 'null'} menu=${result.menu_type}`);
      log(`DIAG items: ${JSON.stringify(compact.slice(0, 20))}`);
      if (items._rejected && items._rejected.length) {
        log(`DIAG filter_rejected (${items._rejected.length}): ${JSON.stringify(items._rejected.slice(0, 10))}`);
      }
      if (result.safe_to_ignore && result.safe_to_ignore.length) {
        log(`DIAG classifier_ignored (${result.safe_to_ignore.length}): ${JSON.stringify(result.safe_to_ignore.slice(0, 10))}`);
      }
    }

    // If the classifier tells us every available candidate is unproductive
    // ('exhausted' = all destinations already seen, or 'all_burned' = we've
    // clicked these enough times to be sure they teach nothing new), skip
    // the wasted click and try to backtrack from the frontier. This is what
    // breaks loops like Preferences ↔ Return before they spin.
    if ((result.menu_type === 'exhausted' || result.menu_type === 'all_burned') && frontier.size() > 0) {
      const nextEntry = frontier.pop();
      if (nextEntry) {
        const res = await engineMod.restore(page, gameFrame, nextEntry.snapshot, { reloadUrl: URL });
        if (res.ok) {
          log(`exhausted → restored via ${res.method} to state ${nextEntry.state_hash}`);
          staleTicks = 0;
          // Refresh prevState for diffing — we just jumped
          prevState = await engineMod.introspect(gameFrame);
          prevHash = stateMod.hashState(prevState);
          return;
        } else {
          log(`exhausted → restore failed: ${res.error}`);
        }
      }
    }

    let clicked = null;
    let clickLanded = true; // assume hit; flipped to false if clickCandidate reports ok:false
    const isDecision = result.decisions.length >= 2;

    if (isDecision) {
      // Real decision point — record, snapshot for backtracking, push remaining choices to frontier
      if (!choiceGraph.nodes[nowHash]) {
        choiceGraph.nodes[nowHash] = { passage: nowState.passage, options: result.decisions.map((d) => d.t), type: result.menu_type, first_seen_session: session.id };
      }
      const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
      const triedTexts = new Set(choiceGraph.edges.filter((e) => e.from === nowHash).map((e) => e.choice));
      const notYet = result.decisions.filter((d) => !triedTexts.has(d.t));
      const pick = notYet[0] || result.decisions[0];
      const remaining = notYet.slice(1).map((d) => d.t);
      if (remaining.length) {
        frontier.push({
          state_hash: nowHash,
          choices_left: remaining,
          snapshot: snapBlob,
          depth: (session.record.choices_explored || 0) + 1,
          added_at: Date.now(),
        });
      }
      const pickIdx = result.decisions.findIndex((d) => d.t === pick.t);
      await snap(page, 'choices', `${nowHash}_${pickIdx}_${(pick.t || 'opt').slice(0, 30).replace(/[^a-z0-9]/gi, '_')}`);
      const clickRes = await clickCandidate(pick);
      clickLanded = clickRes.ok;
      if (!clickRes.ok) log(`click fail (decision): ${clickRes.method}${clickRes.error ? ' — ' + clickRes.error : ''}`);
      choiceGraph.edges.push({ from: nowHash, choice: pick.t, choice_type: result.menu_type, picked_at: new Date().toISOString(), session: session.id, to: null });
      detector.observeChoice({
        passage: nowState.passage, classification: result.menu_type, options: result.decisions.map((d) => d.t),
        picked: pick.t, prices: (result.meta && result.meta.prices) || null, at_state_hash: nowHash,
      });
      session.recordChoice();
      session.recordClick();
      lastMenuTexts = result.decisions.map((d) => d.t);
      clicked = pick;
      await page.waitForTimeout(1800);
    } else if (result.advance) {
      const clickRes = await clickCandidate(result.advance);
      clickLanded = clickRes.ok;
      if (!clickRes.ok) log(`click fail (advance): ${clickRes.method}`);
      session.recordArrow();
      session.recordClick();
      clicked = result.advance;
      await page.waitForTimeout(1400);
    } else {
      // No candidates — blind click in lower-middle of content as a last resort.
      // This is intentional (not a specific element), so clickLanded stays true.
      const cx = SIDEBAR_RIGHT + (frameBox.width - SIDEBAR_RIGHT) / 2;
      const cy = frameBox.y + frameBox.height - 60;
      try { await page.mouse.click(cx, cy); } catch (e) {}
      session.recordClick();
      await page.waitForTimeout(1400);
    }

    // Post-click state observation
    const postState = await engineMod.introspect(gameFrame);
    const postHash = stateMod.hashState(postState);
    const diff = stateMod.diffVariables(prevState.variables, postState.variables);

    // Behavioral learning — tell the classifier what happened. Pass
    // clickLanded so missed clicks (off-screen coords, actionability timeout)
    // don't get mis-classified as chrome.
    if (clicked) {
      try { await classifier.observeOutcome({ clicked, before: nowState, after: postState, clickLanded }); }
      catch (e) { log('classifier.observeOutcome err: ' + e.message); }
    }

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
        try { await classifier.persist(); } catch (e) {}
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
  try { await classifier.persist(); } catch (e) { log('classifier persist err: ' + e.message); }
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
