#!/usr/bin/env node
// Live-play CLI + daemon for the twine-game-explorer skill.
//
// This is the primary first-pass tool for exploring a new browser-based
// Twine/SugarCube game. Claude drives the browser turn-by-turn:
//
//   node scripts/live.js start --url <URL> --slug <slug> --fresh
//   node scripts/live.js peek
//   node scripts/live.js click "Start the story"
//   node scripts/live.js dom --filter Continue
//   node scripts/live.js click --xy 560,190
//   node scripts/live.js snap --note "at apartment choice"
//   node scripts/live.js note "LOVE tracked per-NPC, not global"
//   node scripts/live.js finalize
//
// The first `start` forks a detached daemon process that owns the Playwright
// browser + Detector + Frontier + snapshot registry. Subsequent commands read
// the lockfile (game_explorations/<slug>/.live/daemon.json), POST to the
// daemon's localhost HTTP port, print the JSON response. The daemon idles out
// after --idle-ms (default 30 min) of no commands; clean shutdown on
// `finalize` or `stop`.
//
// Every command captures a fresh screenshot. The response envelope always
// includes {ok, command, screenshot, ...}. On error the screenshot still
// shows the current state — this is the critical feature the script-mode
// explorer lacks.

'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');
const child_process = require('child_process');

// ----------------------------------------------------------------------------
// Paths
// ----------------------------------------------------------------------------

const SKILL_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(SKILL_DIR, '../../..');
const GAME_EXPLORATIONS_ROOT = path.join(PROJECT_ROOT, 'game_explorations');

function gameDirs(slug) {
  const root = path.join(GAME_EXPLORATIONS_ROOT, slug);
  return {
    root,
    live: path.join(root, '.live'),
    lockfile: path.join(root, '.live', 'daemon.json'),
    profile: path.join(root, 'profile'),
    sessions: path.join(root, 'sessions'),
    saves: path.join(root, 'saves'),
    frontier: path.join(root, 'saves', 'frontier.jsonl'),
    explored: path.join(root, 'saves', 'explored_hashes.txt'),
    snapshotsDir: path.join(root, 'saves', 'snapshots'),
    screenshots: path.join(root, 'screenshots', 'live'),
    timeline: path.join(root, 'state_timeline.jsonl'),
    choiceGraph: path.join(root, 'choice_graph.json'),
    notes: path.join(root, 'notes.md'),
    sessionLog: path.join(root, 'session.log'),
    liveLog: path.join(root, 'live.log'),
    detectorSnap: path.join(root, 'saves', 'detector_snapshot.json'),
    playLog: path.join(root, 'play_log.jsonl'),
    uiMap: path.join(root, 'ui_map.json'),
    uiProbes: path.join(root, 'ui_probes'),
    pregameLog: path.join(root, 'pregame_auto_advance.jsonl'),
    sceneBodies: path.join(root, 'scene_bodies.jsonl'),
    passageCatalog: path.join(root, 'passage_catalog.json'),
    initialState: path.join(root, 'initial_state.json'),
    engineConfig: path.join(root, 'engine_config.json'),
    sidebarSnapshots: path.join(root, 'sidebar_snapshots.jsonl'),
    // M6.1 — navigation-intelligence data foundation (built at daemon
    // startup from passage_catalog, not at finalize).
    staticGraph: path.join(root, 'static_graph.json'),
    variableIndex: path.join(root, 'variable_index.json'),
  };
}

function ensureDirs(slug) {
  const d = gameDirs(slug);
  for (const p of [d.root, d.live, d.profile, d.sessions, d.saves, d.snapshotsDir, d.screenshots, d.uiProbes]) {
    fs.mkdirSync(p, { recursive: true });
  }
  return d;
}

// ----------------------------------------------------------------------------
// CLI arg parsing (shared)
// ----------------------------------------------------------------------------

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        out[k.replace(/-/g, '_')] = true;
      } else {
        out[k.replace(/-/g, '_')] = next;
        i++;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

// ----------------------------------------------------------------------------
// Entry point: decide between daemon mode and CLI mode
// ----------------------------------------------------------------------------

(async () => {
  const argv = process.argv.slice(2);
  const firstFlag = argv.find((a) => a.startsWith('--'));
  const isDaemonInternal = argv.includes('--daemon-internal');

  if (isDaemonInternal) {
    await runDaemon(parseArgs(argv));
    return;
  }

  const [subcommand, ...rest] = argv;
  const args = parseArgs(rest);

  try {
    switch (subcommand) {
      case 'start':    await cliStart(args); break;
      case 'peek':     await forward('peek', args); break;
      case 'click':    await forward('click', args); break;
      case 'fill':     await forward('fill', args); break;
      case 'keys':     await forward('keys', args); break;
      case 'eval':     await forward('eval', args); break;
      case 'dom':      await forward('dom', args); break;
      case 'snap':     await forward('snap', args); break;
      case 'restore':  await forward('restore', args); break;
      case 'frontier': await forward('frontier', args); break;
      case 'note':     await forward('note', args); break;
      case 'observe':  await forward('observe', args); break;
      case 'wait':     await forward('wait', args); break;
      case 'reload':   await forward('reload', args); break;
      case 'regions':  await forward('regions', args); break;
      // M6.2 navigation-intelligence query endpoints — read-only, no click.
      case 'path':         await forward('path', args); break;
      case 'requirements': await forward('requirements', args); break;
      case 'reachable':    await forward('reachable', args); break;
      case 'setters':      await forward('setters', args); break;
      case 'finalize': await cliFinalize(args); break;
      case 'stop':     await cliStop(args); break;
      case 'status':   await cliStatus(args); break;
      default:
        printUsage();
        process.exit(subcommand ? 2 : 0);
    }
  } catch (e) {
    console.error(JSON.stringify({ ok: false, error: e.message, stack: e.stack }, null, 2));
    process.exit(1);
  }
})();

function printUsage() {
  process.stdout.write(`twine-game-explorer live-play CLI

  start --url <URL> --slug <slug> [--fresh] [--idle-ms N] [--headless]
        [--skip-phase0] [--rerun-phase0] [--name "<str>"]
      Launch browser, run portal entry, begin a live session.
      By default, runs Phase 0 (pre-game auto-advance + UI recon) after portal
      entry. --skip-phase0 disables it. --rerun-phase0 refreshes an existing
      ui_map.json. --name sets the default for auto-filled name inputs
      (default: "Player").

  regions [--skip-buttons] [--skip-pregame]
      Re-run Phase 0b UI recon on the currently-loaded passage. Refreshes
      ui_map.json. --skip-buttons runs stages 1-4 only (fast, no Stage 5 chrome
      probing).

  peek
      Reread current state (passage + variables + clickables + screenshot).

  click <text>
  click --xy X,Y
  click --selector <css>
      Click an element. Text mode uses Playwright getByText + visible filter.

  fill --index N --value "<v>"
  fill --selector <css> --value "<v>"
      Fill a text input.

  keys <sequence>
      Keyboard press (Enter, Escape, ArrowDown, Tab, ...).

  eval <js>
      Run arbitrary JS inside the game iframe. Return value must be JSON-safe.

  dom [--visible] [--filter <regex>] [--limit N]
      Dump all interactive elements (tag, text, bbox). Debug tool for selector misses.

  snap [--note "<n>"]
      Engine snapshot; returns snap_id for later restore.

  restore <snap_id>
      Restore a snapshot.

  frontier push "<text1>" "<text2>" ... | pop | list
      Persistent DFS queue.

  note "<text>"
      Append a timestamped observation to notes.md.

  observe
      Force a detector observation on the current state.

  wait [--ms N]
      Wait N milliseconds (default 1000). For animations that outlast a click.

  reload
      Reload the iframe URL (recovery when the page is fully wedged).

  finalize
      Flush detector, write report.md + labeled artifacts, close daemon. notes.md,
      play_log.jsonl, saves/, and the persistent browser profile remain for resume.

  stop
      Close daemon without running the report (saves/ persists for resume).

  status
      Show daemon state (running / idle since when / snapshots taken).
`);
}

// ----------------------------------------------------------------------------
// CLIENT: helpers for non-start subcommands
// ----------------------------------------------------------------------------

function readLockfile(slug) {
  const d = gameDirs(slug);
  if (!fs.existsSync(d.lockfile)) return null;
  try { return JSON.parse(fs.readFileSync(d.lockfile, 'utf8')); }
  catch (e) { return null; }
}

function pidAlive(pid) {
  if (!pid) return false;
  try { process.kill(pid, 0); return true; } catch (e) { return false; }
}

function discoverSlug(args) {
  if (args.slug) return args.slug;
  // Try to find a running daemon by scanning .live/daemon.json files
  if (!fs.existsSync(GAME_EXPLORATIONS_ROOT)) return null;
  const candidates = fs.readdirSync(GAME_EXPLORATIONS_ROOT)
    .map((name) => {
      const lock = path.join(GAME_EXPLORATIONS_ROOT, name, '.live', 'daemon.json');
      if (!fs.existsSync(lock)) return null;
      try {
        const info = JSON.parse(fs.readFileSync(lock, 'utf8'));
        if (pidAlive(info.pid)) return info;
      } catch (e) {}
      return null;
    })
    .filter(Boolean);
  if (candidates.length === 1) return candidates[0].slug;
  if (candidates.length > 1) {
    throw new Error(`Multiple live daemons running (${candidates.map((c) => c.slug).join(', ')}). Pass --slug to disambiguate.`);
  }
  return null;
}

function httpRequest(port, body, { timeoutMs = 60000 } = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request({
      host: '127.0.0.1', port, path: '/cmd', method: 'POST',
      headers: { 'content-type': 'application/json', 'content-length': Buffer.byteLength(data) },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        try { resolve(JSON.parse(raw)); }
        catch (e) { resolve({ ok: false, error: 'daemon returned non-JSON: ' + raw.slice(0, 200) }); }
      });
    });
    req.setTimeout(timeoutMs, () => { req.destroy(new Error('daemon request timeout')); });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function forward(command, args) {
  const slug = discoverSlug(args);
  if (!slug) {
    console.error(JSON.stringify({ ok: false, error: 'No running daemon found. Run `live.js start` first, or pass --slug.' }, null, 2));
    process.exit(1);
  }
  const info = readLockfile(slug);
  if (!info) {
    console.error(JSON.stringify({ ok: false, error: `No lockfile for slug "${slug}". Did the daemon die? Try \`start --fresh\`.` }, null, 2));
    process.exit(1);
  }
  if (!pidAlive(info.pid)) {
    console.error(JSON.stringify({ ok: false, error: `Daemon PID ${info.pid} is dead. Stale lockfile; run \`start\` to relaunch.` }, null, 2));
    process.exit(1);
  }
  const response = await httpRequest(info.port, { cmd: command, args, argv: process.argv.slice(2) });
  console.log(JSON.stringify(response, null, 2));
  if (!response.ok) process.exit(1);
}

// ----------------------------------------------------------------------------
// CLI: start (spawn detached daemon)
// ----------------------------------------------------------------------------

async function cliStart(args) {
  if (!args.slug || typeof args.slug !== 'string') throw new Error('start requires --slug <slug>');

  // If --url is omitted, try to read it from existing ui_map.json for this slug.
  if (!args.url || typeof args.url !== 'string') {
    const uiMapPath = path.join(GAME_EXPLORATIONS_ROOT, args.slug, 'ui_map.json');
    if (fs.existsSync(uiMapPath)) {
      try {
        const existing = JSON.parse(fs.readFileSync(uiMapPath, 'utf8'));
        if (existing.url) args.url = existing.url;
      } catch (e) { /* fall through to error */ }
    }
    if (!args.url || typeof args.url !== 'string') {
      throw new Error('start requires --url <URL> (or an existing ui_map.json with the URL for this slug)');
    }
  }

  const slug = args.slug;
  const dirs = ensureDirs(slug);

  // Fresh: archive everything except scripts/, archive/, .live/ (we'll overwrite .live/).
  if (args.fresh) {
    const stamp = new Date().toISOString().replace(/[:.]/g, '-');
    const archive = path.join(dirs.root, 'archive', stamp);
    fs.mkdirSync(archive, { recursive: true });
    for (const f of fs.readdirSync(dirs.root)) {
      if (['archive', 'scripts', '.live'].includes(f)) continue;
      fs.renameSync(path.join(dirs.root, f), path.join(archive, f));
    }
    ensureDirs(slug); // re-create the structure
  }

  // If an existing daemon is already alive, bail early.
  const existing = readLockfile(slug);
  if (existing && pidAlive(existing.pid)) {
    console.log(JSON.stringify({
      ok: true,
      command: 'start',
      reused_existing: true,
      pid: existing.pid,
      port: existing.port,
      slug,
      message: `Daemon already running on port ${existing.port}. Use peek/click/etc or finalize/stop.`,
    }, null, 2));
    return;
  }
  // Clean stale lockfile
  if (fs.existsSync(dirs.lockfile)) fs.unlinkSync(dirs.lockfile);

  // Fork detached daemon
  const nodeExec = process.execPath;
  const scriptPath = __filename;
  const daemonArgs = [scriptPath, '--daemon-internal',
    '--url', args.url, '--slug', slug,
    '--idle-ms', String(args.idle_ms || 30 * 60 * 1000),
  ];
  if (args.headless) daemonArgs.push('--headless');
  if (args.fresh) daemonArgs.push('--fresh');
  if (args.skip_phase0) daemonArgs.push('--skip-phase0');
  if (args.rerun_phase0) daemonArgs.push('--rerun-phase0');
  if (args.skip_buttons) daemonArgs.push('--skip-buttons');
  if (args.name) { daemonArgs.push('--name', String(args.name)); }

  const outLog = fs.openSync(dirs.liveLog, 'a');
  const errLog = fs.openSync(dirs.liveLog, 'a');
  const child = child_process.spawn(nodeExec, daemonArgs, {
    detached: true,
    stdio: ['ignore', outLog, errLog],
    cwd: dirs.root,
  });
  child.unref();

  // Wait for lockfile. Phase 0 auto-run can take 30-90s on games with lots of chrome buttons;
  // skip-phase0 completes in 10-15s. Generous 180s timeout covers the worst case.
  const readyTimeoutMs = args.skip_phase0 ? 30000 : 180000;
  const deadline = Date.now() + readyTimeoutMs;
  let info = null;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 500));
    info = readLockfile(slug);
    if (info && info.ready) break;
  }
  if (!info || !info.ready) {
    throw new Error(`Daemon did not become ready within ${readyTimeoutMs}ms. Check ${dirs.liveLog}.`);
  }

  // Confirm liveness with a peek.
  const peekResult = await httpRequest(info.port, { cmd: 'peek', args: {} });
  // How much prior history do we have? (0 after --fresh.)
  const priorLogLines = fs.existsSync(dirs.playLog)
    ? fs.readFileSync(dirs.playLog, 'utf8').split('\n').filter(Boolean).length
    : 0;
  const priorSessions = fs.existsSync(dirs.sessions)
    ? fs.readdirSync(dirs.sessions).filter((f) => /^session_\d+\.json$/.test(f)).length
    : 0;
  console.log(JSON.stringify({
    ok: peekResult.ok,
    command: 'start',
    slug,
    pid: info.pid,
    port: info.port,
    url: info.url,
    engine: peekResult.engine,
    passage: peekResult.passage,
    saveCaps: peekResult.saveCaps,
    clickables: peekResult.clickables,
    screenshot: peekResult.screenshot,
    log: dirs.liveLog,
    ui_map: peekResult.ui_map || null,
    ui_map_path: peekResult.ui_map_path || null,
    ui_frame_hash: peekResult.ui_frame_hash || null,
    phase0: peekResult.phase0 || null,
    resumed_from_prior: {
      play_log_entries: priorLogLines,
      prior_sessions: priorSessions,
      notes_exists: fs.existsSync(dirs.notes),
      hint: (priorLogLines > 0 || priorSessions > 0)
        ? `Prior data present. Read ${dirs.notes} and ${dirs.playLog} to see what past sessions did.`
        : null,
    },
  }, null, 2));
}

async function cliFinalize(args) {
  const slug = discoverSlug(args);
  if (!slug) throw new Error('No running daemon (pass --slug to target a specific one).');
  const info = readLockfile(slug);
  if (!info || !pidAlive(info.pid)) throw new Error('Daemon not running.');
  const response = await httpRequest(info.port, { cmd: 'finalize', args });
  console.log(JSON.stringify(response, null, 2));
  // Daemon self-terminates after responding; wait briefly for PID to exit.
  const deadline = Date.now() + 10000;
  while (Date.now() < deadline && pidAlive(info.pid)) {
    await new Promise((r) => setTimeout(r, 200));
  }
}

async function cliStop(args) {
  const slug = discoverSlug(args);
  if (!slug) throw new Error('No running daemon.');
  const info = readLockfile(slug);
  if (!info) throw new Error('No lockfile.');
  if (!pidAlive(info.pid)) {
    if (fs.existsSync(info.lockfile || '')) fs.unlinkSync(info.lockfile);
    console.log(JSON.stringify({ ok: true, command: 'stop', note: 'daemon already dead; lockfile cleaned' }, null, 2));
    return;
  }
  const response = await httpRequest(info.port, { cmd: 'stop', args }, { timeoutMs: 10000 }).catch((e) => ({ ok: false, error: e.message }));
  console.log(JSON.stringify(response, null, 2));
}

async function cliStatus(args) {
  const slug = discoverSlug(args);
  if (!slug) {
    console.log(JSON.stringify({ ok: true, command: 'status', running: false, reason: 'no lockfile' }, null, 2));
    return;
  }
  const info = readLockfile(slug);
  if (!info) {
    console.log(JSON.stringify({ ok: true, command: 'status', running: false, reason: 'no lockfile' }, null, 2));
    return;
  }
  const alive = pidAlive(info.pid);
  if (!alive) {
    console.log(JSON.stringify({ ok: true, command: 'status', running: false, reason: 'stale lockfile (pid dead)', info }, null, 2));
    return;
  }
  const response = await httpRequest(info.port, { cmd: 'status', args }).catch((e) => ({ ok: false, error: e.message }));
  console.log(JSON.stringify({ ok: true, command: 'status', running: true, slug, info, daemon: response }, null, 2));
}

// ----------------------------------------------------------------------------
// DAEMON
// ----------------------------------------------------------------------------

async function runDaemon(args) {
  const slug = args.slug;
  const url = args.url;
  if (!slug || !url) throw new Error('daemon needs --slug and --url');
  const idleMs = Number(args.idle_ms) || 30 * 60 * 1000;
  const dirs = ensureDirs(slug);

  const dlog = makeLogger(dirs.liveLog);
  dlog(`=== daemon start slug=${slug} url=${url} pid=${process.pid} ===`);

  // Lazy-require playwright + skill libs (so CLI-only invocations don't pay the cost).
  const { chromium } = require(path.join(SKILL_DIR, 'node_modules/playwright'));
  const engineMod = require(path.join(SKILL_DIR, 'scripts/lib/engine'));
  const stateMod = require(path.join(SKILL_DIR, 'scripts/lib/state'));
  const setupMod = require(path.join(SKILL_DIR, 'scripts/lib/setup'));
  const choicesMod = require(path.join(SKILL_DIR, 'scripts/lib/choices'));
  const { Frontier } = require(path.join(SKILL_DIR, 'scripts/lib/frontier'));
  const { Detector } = require(path.join(SKILL_DIR, 'scripts/lib/detector'));
  const { SessionTracker, aggregateSessions } = require(path.join(SKILL_DIR, 'scripts/lib/session'));
  const reportMod = require(path.join(SKILL_DIR, 'scripts/lib/report'));
  const uiReconMod = require(path.join(SKILL_DIR, 'scripts/lib/ui_recon'));
  const passageCatalogMod = require(path.join(SKILL_DIR, 'scripts/lib/passage_catalog'));
  const engineConfigMod = require(path.join(SKILL_DIR, 'scripts/lib/engine_config'));

  // State
  const context = await chromium.launchPersistentContext(dirs.profile, {
    headless: !!args.headless,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--disable-popup-blocking'],
  });
  const page = context.pages()[0] || await context.newPage();
  dlog('browser launched');
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch((e) => dlog('goto err: ' + e.message));
  await page.waitForTimeout(3000);

  const setupResult = await setupMod.doSetup(page, context, { url });
  let gameFrame = setupResult.frame;
  dlog(`setup adapter=${setupResult.adapter}`);

  let engineInfo = await engineMod.introspect(gameFrame);
  for (let attempt = 1; attempt <= 5 && engineInfo.engine === 'unknown'; attempt++) {
    dlog(`engine unknown (attempt ${attempt}), waiting 3s`);
    await page.waitForTimeout(3000);
    engineInfo = await engineMod.introspect(gameFrame);
  }
  dlog(`engine: ${engineInfo.engine} passage=${engineInfo.passage}`);

  // --- M1: Pristine initial-state snapshot (before Phase 0a mutates anything) ---
  // We don't blindly overwrite on resume — the first session to see the game is
  // the authoritative one; later re-runs only write the file if it's missing.
  if (!fs.existsSync(dirs.initialState)) {
    try {
      const initialBlob = {
        captured_at: new Date().toISOString(),
        ts: Date.now(),
        engine: engineInfo.engine,
        engine_version: engineInfo.version,
        passage: engineInfo.passage,
        variables: engineInfo.variables,
        save_caps: engineInfo.saveCaps || null,
        state_hash: stateMod.hashState({
          passage: engineInfo.passage, variables: engineInfo.variables || {},
        }),
        body_text: engineInfo.body_text != null ? engineInfo.body_text : null,
        body_html: engineInfo.body_html != null ? engineInfo.body_html : null,
        modal_text: engineInfo.modal_text != null ? engineInfo.modal_text : null,
      };
      fs.writeFileSync(dirs.initialState, JSON.stringify(initialBlob, null, 2));
      dlog(`initial_state written (hash=${initialBlob.state_hash}, body_len=${(initialBlob.body_text || '').length})`);
    } catch (e) { dlog('initial_state write err: ' + e.message); }
  } else {
    dlog('initial_state already present — preserving existing snapshot');
  }

  // --- M1: Passage catalog dump (every passage Story exposes, with raw source) ---
  // One-shot per session. Overwrites on each start so the catalog reflects whatever
  // is loaded right now (useful if the game is updated between runs).
  try {
    const cat = await passageCatalogMod.dumpCatalog(gameFrame);
    if (cat && Array.isArray(cat.passages) && cat.passages.length) {
      fs.writeFileSync(dirs.passageCatalog, JSON.stringify({
        captured_at: new Date().toISOString(),
        engine: engineInfo.engine,
        engine_version: engineInfo.version,
        engine_hint: cat.engine_hint,
        total_passages: cat.passages.length,
        passages: cat.passages,
      }, null, 2));
      dlog(`passage_catalog: ${cat.passages.length} passages dumped (hint=${cat.engine_hint})`);
    } else {
      fs.writeFileSync(dirs.passageCatalog, JSON.stringify({
        captured_at: new Date().toISOString(),
        engine: engineInfo.engine,
        engine_version: engineInfo.version,
        error: 'Story/passages unreachable — no catalog available',
        total_passages: 0,
        passages: [],
      }, null, 2));
      dlog('passage_catalog: unreachable — wrote empty catalog with error note');
    }
  } catch (e) { dlog('passage_catalog err: ' + e.message); }

  // --- M6.1: Static navigation graph + variable setter index ---
  // Both derive from the passage catalog we just wrote. Building here —
  // rather than at finalize inside report.js — makes the navigation-
  // intelligence data available from turn 1, so the M6.2 query endpoints
  // (path / requirements / reachable / setters) can operate on it live.
  // We re-read the catalog from disk rather than hoisting `cat` out of
  // its try scope — one extra read of a file we just wrote is cheap and
  // keeps the passage_catalog block untouched.
  //
  // M6.2: We also hold the graph + index in daemon memory (below) so the
  // query endpoints don't re-read these multi-MB files on every call.
  let staticGraphData = null;
  let variableIndexData = null;
  let pathfinderCtx = null;
  try {
    const staticGraphMod = require(path.join(SKILL_DIR, 'scripts/lib/static_graph'));
    const variableIndexMod = require(path.join(SKILL_DIR, 'scripts/lib/variable_index'));
    let catForGraph = null;
    try { catForGraph = JSON.parse(fs.readFileSync(dirs.passageCatalog, 'utf8')); }
    catch (e) { dlog('static_graph: could not re-read passage_catalog: ' + e.message); }
    if (catForGraph) {
      staticGraphData = staticGraphMod.buildStaticGraph(catForGraph);
      fs.writeFileSync(dirs.staticGraph, JSON.stringify(staticGraphData, null, 2));
      dlog(`static_graph: ${staticGraphData.total_edges} edges over ${staticGraphData.total_passages} passages`);

      let initialForVars = null;
      try { initialForVars = JSON.parse(fs.readFileSync(dirs.initialState, 'utf8')); }
      catch (e) { /* tolerate missing initial_state */ }

      variableIndexData = variableIndexMod.buildVariableIndex(catForGraph, staticGraphData, initialForVars);
      fs.writeFileSync(dirs.variableIndex, JSON.stringify(variableIndexData, null, 2));
      dlog(`variable_index: ${variableIndexData.total_variables} vars, coverage=${variableIndexData.indexing_coverage}`);

      // Pathfinder context — adjacency map + var index reference, built once,
      // consulted by every M6.2 query handler without rescanning the graph.
      try {
        const pathfinderMod = require(path.join(SKILL_DIR, 'scripts/lib/pathfinder'));
        pathfinderCtx = pathfinderMod.buildContext(staticGraphData, variableIndexData);
        if (pathfinderCtx) {
          dlog(`pathfinder ready: ${pathfinderCtx.passageSet.size} passages, adjacency ${pathfinderCtx.adjacency.size}`);
        }
      } catch (e) { dlog('pathfinder init err: ' + e.message); }
    }
  } catch (e) { dlog('static_graph/variable_index err: ' + e.message); }

  // --- M3: Engine configuration dump (Config, Setting, version, State-shape, save-caps, Story-ifid) ---
  // One-shot, pre-Phase-0a. Captures the engine's *declared* configuration —
  // what this game boots with, before any player action. Separate from the
  // per-turn variable state captured by observeCurrentState.
  try {
    const cfg = await engineConfigMod.dumpEngineConfig(gameFrame);
    fs.writeFileSync(dirs.engineConfig, JSON.stringify(cfg, null, 2));
    const startHint = cfg && cfg.config && cfg.config.passages && cfg.config.passages.start;
    const ifidHint = cfg && cfg.story && cfg.story.ifid;
    dlog(`engine_config written (engine=${cfg && cfg.engine} start=${startHint || '?'} ifid=${ifidHint || '?'})`);
  } catch (e) { dlog('engine_config err: ' + e.message); }

  // Load explored hashes
  const explored = new Set();
  if (fs.existsSync(dirs.explored)) {
    for (const h of fs.readFileSync(dirs.explored, 'utf8').split('\n').filter(Boolean)) explored.add(h);
  }
  function markExplored(h) {
    if (explored.has(h)) return false;
    explored.add(h);
    fs.appendFileSync(dirs.explored, h + '\n');
    return true;
  }

  const detector = new Detector();
  const frontier = new Frontier(dirs.frontier);
  const session = new SessionTracker(dirs.sessions);
  session.setFrontierStart(frontier.size());

  const snapshots = new Map(); // snap_id -> {blob, note, taken_at, passage}

  // Phase 0 state (populated by ui_recon orchestrator; null if skipped or errored)
  let uiMap = null;
  let uiFrameHash = null;
  let phase0Result = null; // { ran: bool, duration_ms, error?, reused_existing? }

  let lastState = { passage: engineInfo.passage || null, variables: engineInfo.variables || {} };
  let lastHash = stateMod.hashState(lastState);
  const initialIsNewUnique = markExplored(lastHash);
  if (initialIsNewUnique) session.incNewUniqueState();
  detector.observeState({
    state_hash: lastHash, passage: lastState.passage,
    variables: lastState.variables, diff: null, timestamp: Date.now(),
  });
  // M1: write the first scene body too — otherwise the initial markExplored
  // consumes the unique-hash mark without persisting the narrative payload.
  if (initialIsNewUnique) {
    try {
      const bodyRec = {
        ts: Date.now(),
        state_hash: lastHash,
        passage: lastState.passage,
        engine: engineInfo.engine,
        body_text: engineInfo.body_text != null ? engineInfo.body_text : null,
        body_html: engineInfo.body_html != null ? engineInfo.body_html : null,
        modal_text: engineInfo.modal_text != null ? engineInfo.modal_text : null,
        variables_snapshot: lastState.variables,
        session: session.id,
        kind: 'start',
        entered_via: null,
      };
      fs.appendFileSync(dirs.sceneBodies, JSON.stringify(bodyRec) + '\n');
    } catch (e) { dlog('initial scene_bodies append err: ' + e.message); }
  }
  fs.appendFileSync(dirs.timeline, JSON.stringify({
    ts: Date.now(), hash: lastHash, passage: lastState.passage, session: session.id,
    kind: 'start', new_unique_state: initialIsNewUnique,
  }) + '\n');

  // ---- M4: sidebar_snapshots.jsonl emitter helpers ----
  // lastSidebarFingerprint tracks the most recently observed passive sidebar
  // content hash. When observeCurrentState sees a change, it appends a
  // passive_change entry so downstream analysis can see the evolving panel
  // content (quest text advancing, new phone contacts, stats shifting).
  let lastSidebarFingerprint = null;
  function writeSidebarProbes(uiMapObj, kind) {
    if (!uiMapObj || !Array.isArray(uiMapObj.chrome_probes)) return 0;
    let written = 0;
    for (const p of uiMapObj.chrome_probes) {
      if (p.skipped_reason) continue;
      if (!p.click_ok) continue;
      try {
        const rec = {
          ts: Date.now(),
          kind,                               // 'phase0_probe' or 'manual_regions'
          button_label: p.label || null,
          bbox: p.bbox || null,
          region_id: p.region_id || null,
          screenshot_path: p.screenshot_path || null,
          panel_text: p.panel_text != null ? p.panel_text : null,
          dialog_text: p.dialog_text != null ? p.dialog_text : null,
          post_click_text: p.post_click_text != null ? p.post_click_text : null,
          post_click_elements: p.post_click_elements || [],
          passage: (lastState && lastState.passage) || null,
          state_hash: lastHash || null,
          ui_frame_hash: (uiMapObj && uiMapObj.ui_frame_hash) || null,
        };
        fs.appendFileSync(dirs.sidebarSnapshots, JSON.stringify(rec) + '\n');
        written++;
      } catch (e) { dlog('sidebar_snapshots append err: ' + e.message); }
    }
    return written;
  }
  async function emitPassiveSidebarChange(kind, currentState = null, currentHash = null) {
    if (!uiMap || !Array.isArray(uiMap.regions_catalog) || !uiMap.regions_catalog.length) return;
    try {
      const snap = await uiReconMod.captureSidebarState(gameFrame, uiMap.regions_catalog);
      const fp = uiReconMod.fingerprintSidebar(snap);
      if (fp === lastSidebarFingerprint) return; // no change
      const prior = lastSidebarFingerprint;
      lastSidebarFingerprint = fp;
      // Skip the very first emit for the baseline seeding — that's
      // redundant with the Phase 0 probe batch.
      if (prior === null && kind === 'passive_change') return;
      // Prefer the passage/hash the caller supplied (captured post-click,
      // before lastState is updated). Falls back to the daemon-global lastState
      // for callers that don't supply one (baseline seeding paths).
      const pas = currentState && currentState.passage != null
        ? currentState.passage
        : (lastState && lastState.passage) || null;
      const hash = currentHash || lastHash || null;
      const rec = {
        ts: Date.now(),
        kind,                          // 'passive_change' or 'baseline'
        sidebar_fingerprint: fp,
        prior_fingerprint: prior,
        regions: snap.regions,         // full region payload (text + interactive)
        passage: pas,
        state_hash: hash,
        ui_frame_hash: (uiMap && uiMap.ui_frame_hash) || null,
      };
      fs.appendFileSync(dirs.sidebarSnapshots, JSON.stringify(rec) + '\n');
    } catch (e) { dlog('sidebar passive emit err: ' + e.message); }
  }

  // ---- Phase 0: pre-game auto-advance + UI recon (best-effort, never blocks the session) ----
  {
    const phase0Start = Date.now();
    const phase0Opts = {
      skipPhase0: !!args.skip_phase0,
      skipButtons: !!args.skip_buttons,
      rerun: !!args.rerun_phase0,
      name: args.name || 'Player',
      slug, url,
    };
    const dlog_p0 = (msg) => dlog('[phase0] ' + msg);
    try {
      uiMap = await uiReconMod.runPhase0({
        page, frame: gameFrame, context,
        engineMod, stateMod, engineInfo,
        dirs, snapshots,
        opts: phase0Opts,
        logger: dlog_p0,
      });
      if (uiMap && uiMap.ui_frame_hash) uiFrameHash = uiMap.ui_frame_hash;
      // M4: dump every probe's structured text into sidebar_snapshots.jsonl.
      // Idempotent — if Phase 0 reused an existing ui_map.json and no new
      // probes were run, writeSidebarProbes simply has nothing new to write,
      // BUT we still want the text there for first-time resumes, so we check
      // if the JSONL already has phase0 entries for this ui_frame_hash.
      try {
        const hasExistingPhase0 = fs.existsSync(dirs.sidebarSnapshots) && fs.readFileSync(dirs.sidebarSnapshots, 'utf8')
          .split('\n').some((ln) => {
            if (!ln.trim()) return false;
            try { const r = JSON.parse(ln); return r.kind === 'phase0_probe' && r.ui_frame_hash === (uiMap && uiMap.ui_frame_hash); }
            catch (e) { return false; }
          });
        if (!hasExistingPhase0) {
          const n = writeSidebarProbes(uiMap, 'phase0_probe');
          if (n) dlog_p0(`sidebar_snapshots: wrote ${n} phase0 probe entries`);
        } else {
          dlog_p0('sidebar_snapshots: phase0 entries already present for current ui_frame_hash, skipping');
        }
      } catch (e) { dlog_p0('sidebar_snapshots phase0 emit err: ' + e.message); }
      // M4: seed the baseline passive fingerprint so future observeCurrentState
      // calls can detect changes.
      try {
        const baseline = await uiReconMod.captureSidebarState(gameFrame, uiMap ? uiMap.regions_catalog : null);
        lastSidebarFingerprint = uiReconMod.fingerprintSidebar(baseline);
        const rec = {
          ts: Date.now(),
          kind: 'baseline',
          sidebar_fingerprint: lastSidebarFingerprint,
          prior_fingerprint: null,
          regions: baseline.regions,
          passage: (lastState && lastState.passage) || null,
          state_hash: lastHash || null,
          ui_frame_hash: uiFrameHash,
        };
        fs.appendFileSync(dirs.sidebarSnapshots, JSON.stringify(rec) + '\n');
      } catch (e) { dlog_p0('sidebar baseline seed err: ' + e.message); }
      phase0Result = {
        ran: !phase0Opts.skipPhase0,
        duration_ms: Date.now() - phase0Start,
        reused_existing: uiMap && fs.existsSync(dirs.uiMap) && !phase0Opts.rerun,
        regions_count: uiMap && uiMap.regions ? uiMap.regions.length : 0,
        probes_count: uiMap && uiMap.chrome_probes ? uiMap.chrome_probes.length : 0,
      };
      // After Phase 0a, the passage may have changed — re-observe state so clickables/hash are fresh.
      try {
        const postInfo = await engineMod.introspect(gameFrame);
        engineInfo = postInfo;
        lastState = { passage: postInfo.passage || null, variables: postInfo.variables || {} };
        lastHash = stateMod.hashState(lastState);
        const postPhase0IsNewUnique = markExplored(lastHash);
        if (postPhase0IsNewUnique) session.incNewUniqueState();
        detector.observeState({
          state_hash: lastHash, passage: lastState.passage,
          variables: lastState.variables, diff: null, timestamp: Date.now(),
        });
        // M1: persist the first post-Phase-0 scene body (the "gameplay start" passage)
        if (postPhase0IsNewUnique) {
          try {
            const bodyRec = {
              ts: Date.now(),
              state_hash: lastHash,
              passage: lastState.passage,
              engine: postInfo.engine,
              body_text: postInfo.body_text != null ? postInfo.body_text : null,
              body_html: postInfo.body_html != null ? postInfo.body_html : null,
              modal_text: postInfo.modal_text != null ? postInfo.modal_text : null,
              variables_snapshot: lastState.variables,
              session: session.id,
              kind: 'post_phase0',
              entered_via: null,
            };
            fs.appendFileSync(dirs.sceneBodies, JSON.stringify(bodyRec) + '\n');
          } catch (eb) { dlog_p0('post-phase0 scene_bodies append err: ' + eb.message); }
        }
      } catch (e) { dlog_p0('post-observe err: ' + e.message); }
    } catch (e) {
      dlog_p0('runPhase0 errored: ' + e.stack);
      phase0Result = { ran: true, duration_ms: Date.now() - phase0Start, error: e.message };
      uiMap = null;
    }
  }

  // -------- Helpers used by command handlers --------

  async function captureScreenshot(cmd) {
    const file = path.join(dirs.screenshots, `${Date.now()}_${cmd.replace(/[^a-z0-9]/gi, '_')}.png`);
    try { await page.screenshot({ path: file }); return file; } catch (e) { return null; }
  }

  async function listClickablesForResponse() {
    const raw = await choicesMod.listInteractive(gameFrame).catch(() => []);
    const ICON_LIMIT = (s) => {
      if (!s) return true;
      for (const ch of s) {
        const code = ch.codePointAt(0);
        if (code < 0xE000 || code > 0xF8FF) return false;
      }
      return true;
    };
    return raw
      .filter((c) => c.t && c.t.trim().length > 0)
      .map((c) => ({ ...c, icon_only: ICON_LIMIT(c.t) }));
  }

  async function observeCurrentState({ previousState = null, previousHash = null, classification = null, picked = null, options = null } = {}) {
    const nowInfo = await engineMod.introspect(gameFrame);
    const nowState = { passage: nowInfo.passage || null, variables: nowInfo.variables || {} };
    const nowHash = stateMod.hashState(nowState);
    const diff = previousState ? stateMod.diffVariables(previousState.variables, nowState.variables) : null;
    const ts = Date.now();
    detector.observeState({
      state_hash: nowHash, passage: nowState.passage,
      variables: nowState.variables, diff, timestamp: ts,
    });
    const isNewUniqueState = markExplored(nowHash);
    if (isNewUniqueState) {
      session.incNewUniqueState();
      await captureScreenshot('scene_' + nowHash);
      // M1: persist the full rendered body + pristine variable snapshot for
      // every never-before-seen state. Append-only JSONL; dedup is handled
      // by the markExplored gate, so every line is a genuinely new scene.
      try {
        const bodyRec = {
          ts,
          state_hash: nowHash,
          passage: nowState.passage,
          engine: nowInfo.engine,
          body_text: nowInfo.body_text != null ? nowInfo.body_text : null,
          body_html: nowInfo.body_html != null ? nowInfo.body_html : null,
          modal_text: nowInfo.modal_text != null ? nowInfo.modal_text : null,
          variables_snapshot: nowState.variables,
          session: session.id,
          kind: classification || 'observe',
          entered_via: picked || null,
        };
        fs.appendFileSync(dirs.sceneBodies, JSON.stringify(bodyRec) + '\n');
      } catch (e) { dlog('scene_bodies append err: ' + e.message); }
    }
    // M1: timeline now carries the full diff (before/after values) rather
    // than only changed-key names. Downstream analysis needs the actual
    // deltas to build the choice graph's effect_aggregate.
    fs.appendFileSync(dirs.timeline, JSON.stringify({
      ts, hash: nowHash, passage: nowState.passage, session: session.id,
      diff_full: diff ? {
        changed: diff.changed || {},
        added: diff.added || {},
        removed: diff.removed || {},
      } : null,
      // Back-compat: legacy key-name lists kept so any older reader still works.
      diff_changed: diff ? Object.keys(diff.changed) : [],
      diff_added: diff ? Object.keys(diff.added) : [],
      diff_removed: diff ? Object.keys(diff.removed) : [],
      kind: classification || 'observe',
      new_unique_state: isNewUniqueState,
    }) + '\n');
    if (picked && options) {
      detector.observeChoice({
        passage: previousState ? previousState.passage : nowState.passage,
        classification: classification || 'branch',
        options, picked, at_state_hash: previousHash || nowHash,
      });
    }
    // M4: passive sidebar change detection. Non-clicking, cheap
    // (one frame.evaluate). Emits a jsonl line iff the sidebar text/
    // interactive signature actually changed since the prior observation.
    // Pass the just-observed state so the record's passage/hash labels
    // reflect the post-action state, not the stale daemon-global lastState.
    try { await emitPassiveSidebarChange('passive_change', nowState, nowHash); } catch (e) { dlog('passive sidebar emit err: ' + e.message); }
    return { state: nowState, hash: nowHash, diff, info: nowInfo };
  }

  // Idle timeout
  let idleTimer = null;
  function resetIdle() {
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(async () => {
      dlog(`idle timeout after ${idleMs}ms, shutting down`);
      await shutdown({ reason: 'idle_timeout' });
    }, idleMs);
  }

  async function shutdown({ reason = 'manual', writeReport = false }) {
    dlog(`shutdown reason=${reason} writeReport=${writeReport}`);
    try {
      session.setFrontierEnd(frontier.size());
      session.setUniqueStates(explored.size);
      session.flush();
    } catch (e) { dlog('session flush err: ' + e.message); }

    try { fs.writeFileSync(dirs.detectorSnap, JSON.stringify(detector.serialize(), null, 2)); } catch (e) {}

    const artifacts = {
      notes: dirs.notes,
      play_log: dirs.playLog,
      state_timeline: dirs.timeline,
      choice_graph: dirs.choiceGraph,
      frontier: dirs.frontier,
      explored_hashes: dirs.explored,
      snapshots_dir: dirs.snapshotsDir,
      detector_snapshot: dirs.detectorSnap,
      live_log: dirs.liveLog,
      // M1 text-capture artifacts
      scene_bodies: dirs.sceneBodies,
      passage_catalog: dirs.passageCatalog,
      initial_state: dirs.initialState,
      // M3 engine configuration dump
      engine_config: dirs.engineConfig,
      // M4 sidebar snapshots
      sidebar_snapshots: dirs.sidebarSnapshots,
      // M6.1 navigation-intelligence data foundation (written at startup,
      // read by report.js at finalize — not re-derived).
      static_graph: dirs.staticGraph,
      variable_index: dirs.variableIndex,
    };

    if (writeReport) {
      try {
        const sessionsSummary = aggregateSessions(dirs.sessions);
        reportMod.write(dirs.root, detector, frontier, explored.size, sessionsSummary, {
          gameName: slug, url,
          engine: engineInfo.engine, engineVersion: engineInfo.version,
          canMarshal: engineInfo.canMarshal,
        });
        dlog('report written');
        Object.assign(artifacts, {
          report: path.join(dirs.root, 'report.md'),
          mechanics: path.join(dirs.root, 'mechanics.md'),
          coverage: path.join(dirs.root, 'coverage.md'),
          variable_schema: path.join(dirs.root, 'variable_schema.json'),
          variable_profile: path.join(dirs.root, 'variable_profile.json'),
          npcs: path.join(dirs.root, 'npcs.json'),
          items: path.join(dirs.root, 'items.json'),
          body_changes: path.join(dirs.root, 'body_changes.json'),
          scene_catalog: path.join(dirs.root, 'scene_catalog.json'),
          // M2 graphs (choice_graph is written here; static_graph is in the
          // pre-report artifact block — written at startup per M6.1).
          choice_graph: path.join(dirs.root, 'choice_graph.json'),
        });
      } catch (e) { dlog('report err: ' + e.message); }
    }

    try { await context.close(); } catch (e) {}
    try { if (fs.existsSync(dirs.lockfile)) fs.unlinkSync(dirs.lockfile); } catch (e) {}
    if (idleTimer) clearTimeout(idleTimer);
    if (server) { try { server.close(); } catch (e) {} }

    // M1: finalize-only per-turn screenshot cleanup.
    // Rationale: live/ screenshots are Claude's real-time decision feedback; they
    // aren't part of the durable design-reference corpus. Once the report has been
    // written, the text artifacts (scene_bodies, timeline, passage_catalog, etc.)
    // carry all the information downstream analysis needs. `stop`/idle/signal
    // paths preserve them on purpose so a resumed session can see prior visual
    // state if needed.
    // ui_probes/ and scenes/ are untouched — they're Phase-0 / scene-dedup
    // metadata, not per-turn churn.
    if (reason === 'finalize') {
      try {
        if (fs.existsSync(dirs.screenshots)) {
          const count = fs.readdirSync(dirs.screenshots).length;
          fs.rmSync(dirs.screenshots, { recursive: true, force: true });
          dlog(`live screenshots removed on finalize (${count} files)`);
          artifacts.live_screenshots_removed = count;
        }
      } catch (e) { dlog('screenshot cleanup err: ' + e.message); }
    }

    // Give HTTP response a moment to flush, then exit.
    setTimeout(() => process.exit(0), 250);
    return { ok: true, reason, artifacts };
  }

  // -------- HTTP server --------

  let server;
  const handlers = {
    async peek() {
      const nowInfo = await engineMod.introspect(gameFrame);
      engineInfo = nowInfo;
      const nowState = { passage: nowInfo.passage || null, variables: nowInfo.variables || {} };
      const nowHash = stateMod.hashState(nowState);
      const diff = stateMod.diffVariables(lastState.variables, nowState.variables);
      const clickables = await listClickablesForResponse();
      detector.observeState({
        state_hash: nowHash, passage: nowState.passage,
        variables: nowState.variables, diff, timestamp: Date.now(),
      });
      if (markExplored(nowHash)) session.incNewUniqueState();
      lastState = nowState; lastHash = nowHash;
      const screenshot = await captureScreenshot('peek');
      return {
        ok: true,
        engine: nowInfo.engine, engineVersion: nowInfo.version,
        saveCaps: nowInfo.saveCaps || null,
        passage: nowState.passage,
        state_hash: nowHash,
        variables_diff: diff,
        variable_summary: summarizeVariables(nowState.variables),
        clickables,
        hidden_chrome: clickables.filter((c) => c.x < 270 || (c.icon_only)).map((c) => ({ text: c.t, reason: c.icon_only ? 'icon_font' : 'left_sidebar' })),
        unique_states_seen: explored.size,
        frontier_size: frontier.size(),
        passage_body_text: nowInfo.body_text != null ? nowInfo.body_text : null,
        passage_body_html: nowInfo.body_html != null ? nowInfo.body_html : null,
        modal_text: nowInfo.modal_text != null ? nowInfo.modal_text : null,
        screenshot,
      };
    },

    async click({ args }) {
      // Three modes: text (positional from args._), --xy, --selector.
      const positional = (args._ || []).filter((a) => a !== 'click');
      const text = positional.length ? positional.join(' ') : null;
      const prevState = lastState; const prevHash = lastHash;
      const optionsBefore = (await listClickablesForResponse()).map((c) => c.t);
      // Capture pre-click marker for adaptive settle wait
      const preMarker = await uiReconMod.captureMarker(gameFrame);
      let clicked = false;
      let method = null;
      let error = null;
      try {
        if (args.selector) {
          await gameFrame.locator(args.selector).first().click({ force: !!args.force, timeout: 3500 });
          clicked = true; method = 'selector';
        } else if (args.xy) {
          const [xs, ys] = String(args.xy).split(',').map((n) => Number(n.trim()));
          if (!Number.isFinite(xs) || !Number.isFinite(ys)) throw new Error('--xy needs "X,Y" numeric');
          const result = await gameFrame.evaluate(({ x, y }) => {
            const el = document.elementFromPoint(x, y);
            if (!el) return { ok: false, error: 'no element at (' + x + ',' + y + ')' };
            el.click();
            return { ok: true, tag: el.tagName, text: (el.textContent || '').trim().slice(0, 120) };
          }, { x: xs, y: ys });
          if (!result.ok) throw new Error(result.error);
          clicked = true; method = `xy(${xs},${ys})`;
        } else if (text) {
          // Visible-only selector first (covers the BTF hidden-Continue case)
          const visibleSel = gameFrame.locator(`:visible:has-text(${JSON.stringify(text)})`).filter({ hasText: new RegExp('^\\s*' + escapeRegex(text) + '\\s*$') }).first();
          try {
            await visibleSel.click({ force: true, timeout: 2500 });
            clicked = true; method = 'visible-has-text';
          } catch (e) {
            // Fallback: exact getByText
            const loc = gameFrame.getByText(text, { exact: true }).first();
            await loc.click({ force: true, timeout: 2500 });
            clicked = true; method = 'getByText-exact';
          }
        } else {
          throw new Error('click needs a text arg, --xy X,Y, or --selector css');
        }
      } catch (e) { error = e.message; }

      if (clicked) { session.recordClick(); if (optionsBefore.length >= 2) session.recordChoice(); else session.recordArrow(); }

      // Adaptive wait — poll until passage/history/DOM changes vs preMarker.
      // If user passed --wait, treat as the timeout cap (default 5000ms).
      // Skip the wait if click never landed (no point polling).
      if (clicked) {
        await uiReconMod.waitForChange(page, gameFrame, preMarker, {
          timeoutMs: Number(args.wait || 5000),
          pollMs: 150,
          settleAfterChangeMs: 200,
        });
      }

      const obs = await observeCurrentState({
        previousState: prevState, previousHash: prevHash,
        classification: optionsBefore.length >= 2 ? 'branch' : 'advance',
        picked: clicked ? text : null,
        options: optionsBefore.length >= 2 ? optionsBefore : null,
      });
      lastState = obs.state; lastHash = obs.hash;
      const clickables = await listClickablesForResponse();
      const screenshot = await captureScreenshot('click');

      return {
        ok: clicked,
        method,
        error: error || undefined,
        clicked_text: clicked && text ? text : undefined,
        passage: obs.state.passage,
        passage_changed: obs.state.passage !== (prevState && prevState.passage),
        state_hash: obs.hash,
        state_changed: obs.hash !== prevHash,
        variables_diff: obs.diff,
        clickables,
        unique_states_seen: explored.size,
        frontier_size: frontier.size(),
        passage_body_text: obs.info && obs.info.body_text != null ? obs.info.body_text : null,
        passage_body_html: obs.info && obs.info.body_html != null ? obs.info.body_html : null,
        modal_text: obs.info && obs.info.modal_text != null ? obs.info.modal_text : null,
        screenshot,
      };
    },

    async fill({ args }) {
      if (!('value' in args)) throw new Error('fill requires --value "<v>"');
      const value = args.value;
      try {
        if (args.selector) {
          await gameFrame.locator(args.selector).first().fill(value, { timeout: 3000 });
        } else {
          const idx = Number(args.index != null ? args.index : 0);
          const inputs = await gameFrame.locator('input[type="text"]:visible, input:not([type]):visible, textarea:visible').all();
          if (!inputs[idx]) throw new Error(`no input at index ${idx} (found ${inputs.length})`);
          await inputs[idx].fill(value);
        }
      } catch (e) { return { ok: false, error: e.message, screenshot: await captureScreenshot('fill_err') }; }
      const screenshot = await captureScreenshot('fill');
      return { ok: true, screenshot };
    },

    async keys({ args }) {
      const seq = (args._ || []).filter((a) => a !== 'keys').join(' ').trim();
      if (!seq) throw new Error('keys requires a key sequence, e.g. `keys Enter`');
      const preMarker = await uiReconMod.captureMarker(gameFrame);
      try { await page.keyboard.press(seq); } catch (e) { return { ok: false, error: e.message }; }
      await uiReconMod.waitForChange(page, gameFrame, preMarker, { timeoutMs: Number(args.wait || 5000), pollMs: 150 });
      const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
      lastState = obs.state; lastHash = obs.hash;
      const screenshot = await captureScreenshot('keys');
      return { ok: true, pressed: seq, passage: obs.state.passage, state_hash: obs.hash, screenshot };
    },

    async eval({ args }) {
      const js = (args._ || []).filter((a) => a !== 'eval').join(' ').trim();
      if (!js) throw new Error('eval requires a JS expression or statement body');
      const preMarker = await uiReconMod.captureMarker(gameFrame);
      let result;
      try {
        result = await gameFrame.evaluate((src) => {
          // eslint-disable-next-line no-new-func
          const fn = new Function('return (async () => { ' + src + ' })();');
          return fn();
        }, js);
      } catch (e) {
        return { ok: false, error: e.message, screenshot: await captureScreenshot('eval_err') };
      }
      await uiReconMod.waitForChange(page, gameFrame, preMarker, { timeoutMs: Number(args.wait || 5000), pollMs: 150 });
      const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
      lastState = obs.state; lastHash = obs.hash;
      const screenshot = await captureScreenshot('eval');
      return { ok: true, result: safeJson(result), passage: obs.state.passage, state_hash: obs.hash, variables_diff: obs.diff, screenshot };
    },

    async dom({ args }) {
      const raw = await choicesMod.listInteractive(gameFrame).catch(() => []);
      let items = raw;
      if (args.visible) items = items.filter((c) => c.w > 4 && c.h > 4);
      if (args.filter) {
        const re = new RegExp(String(args.filter), 'i');
        items = items.filter((c) => re.test(c.t || '') || re.test(c.tag));
      }
      const limit = Number(args.limit || 200);
      return {
        ok: true,
        count: items.length,
        items: items.slice(0, limit),
        truncated: items.length > limit,
      };
    },

    async snap({ args }) {
      const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
      const id = 's' + crypto.createHash('sha1').update(JSON.stringify(snapBlob) + Date.now()).digest('hex').slice(0, 10);
      const record = { id, blob: snapBlob, note: args.note || null, taken_at: Date.now(), passage: lastState.passage, state_hash: lastHash };
      snapshots.set(id, record);
      try { fs.writeFileSync(path.join(dirs.snapshotsDir, `${id}.json`), JSON.stringify(record, null, 2)); } catch (e) {}
      return { ok: true, snap_id: id, passage: lastState.passage, state_hash: lastHash, note: record.note, mode: snapBlob.mode };
    },

    async restore({ args }) {
      const rest = (args._ || []).filter((a) => a !== 'restore');
      const id = rest[0];
      if (!id) throw new Error('restore requires a snap_id');
      let record = snapshots.get(id);
      if (!record) {
        const p = path.join(dirs.snapshotsDir, `${id}.json`);
        if (fs.existsSync(p)) record = JSON.parse(fs.readFileSync(p, 'utf8'));
      }
      if (!record) return { ok: false, error: `snap_id ${id} not found` };
      const preMarker = await uiReconMod.captureMarker(gameFrame);
      const res = await engineMod.restore(page, gameFrame, record.blob, { reloadUrl: url });
      if (!res.ok) return { ok: false, error: res.error, screenshot: await captureScreenshot('restore_err') };
      // Wait for the restore to manifest in the DOM (passage/history/text shifts back to snap state)
      await uiReconMod.waitForChange(page, gameFrame, preMarker, { timeoutMs: 5000, pollMs: 150 });
      const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
      lastState = obs.state; lastHash = obs.hash;
      const screenshot = await captureScreenshot('restore');
      return {
        ok: true,
        method: res.method,
        render_warning: res.render_warning || null,
        passage: obs.state.passage,
        state_hash: obs.hash,
        screenshot,
      };
    },

    async frontier({ args }) {
      const rest = (args._ || []).filter((a) => a !== 'frontier');
      const op = rest[0];
      if (op === 'push') {
        const texts = rest.slice(1);
        if (!texts.length) throw new Error('frontier push needs at least one choice text');
        const snapBlob = await engineMod.snapshot(gameFrame, { pathSoFar: [] });
        const pushed = frontier.push({
          state_hash: lastHash,
          choices_left: texts,
          snapshot: snapBlob,
          depth: session.record.choices_explored || 0,
          added_at: Date.now(),
        });
        return { ok: true, pushed, frontier_size: frontier.size() };
      }
      if (op === 'pop') {
        const entry = frontier.pop();
        if (!entry) return { ok: false, error: 'frontier empty' };
        const res = await engineMod.restore(page, gameFrame, entry.snapshot, { reloadUrl: url });
        if (!res.ok) return { ok: false, error: 'restore failed: ' + res.error, screenshot: await captureScreenshot('pop_err') };
        await page.waitForTimeout(1500);
        const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
        lastState = obs.state; lastHash = obs.hash;
        const screenshot = await captureScreenshot('pop');
        return { ok: true, popped: { state_hash: entry.state_hash, choices_left: entry.choices_left, depth: entry.depth }, passage: obs.state.passage, screenshot, frontier_size: frontier.size() };
      }
      if (op === 'list' || !op) {
        return { ok: true, size: frontier.size(), summary: frontier.summary(), entries: frontier.entries.map((e) => ({ state_hash: e.state_hash, depth: e.depth, choices_left: e.choices_left })) };
      }
      return { ok: false, error: 'unknown frontier op: ' + op };
    },

    async note({ args }) {
      const text = (args._ || []).filter((a) => a !== 'note').join(' ').trim();
      if (!text) throw new Error('note requires text');
      const ts = new Date().toISOString();
      fs.appendFileSync(dirs.notes, `- [${ts}] ${text}\n`);
      session.addNote(text);
      return { ok: true, note_recorded: text };
    },

    async observe() {
      const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
      lastState = obs.state; lastHash = obs.hash;
      return { ok: true, passage: obs.state.passage, state_hash: obs.hash, variables_diff: obs.diff };
    },

    async wait({ args }) {
      const ms = Number(args.ms || 1000);
      await page.waitForTimeout(ms);
      const screenshot = await captureScreenshot('wait');
      return { ok: true, waited_ms: ms, screenshot };
    },

    async reload() {
      await page.goto(url, { waitUntil: 'domcontentloaded' }).catch((e) => dlog('reload err: ' + e.message));
      await page.waitForTimeout(3000);
      const sr = await setupMod.doSetup(page, context, { url });
      gameFrame = sr.frame;
      engineInfo = await engineMod.introspect(gameFrame);
      const obs = await observeCurrentState({ previousState: lastState, previousHash: lastHash });
      lastState = obs.state; lastHash = obs.hash;
      const screenshot = await captureScreenshot('reload');
      return { ok: true, passage: obs.state.passage, state_hash: obs.hash, engine: engineInfo.engine, screenshot };
    },

    async regions({ args }) {
      // On-demand Phase 0b. Skips Phase 0a (we're mid-game).
      const start = Date.now();
      const opts = {
        skipPhase0: false,
        skipPregame: true, // regions subcommand never auto-advances — we're already in-game
        skipButtons: !!args.skip_buttons,
        rerun: true,       // explicit invocation always refreshes
        name: args.name || 'Player',
        slug, url,
      };
      const dlog_r = (m) => dlog('[regions] ' + m);
      try {
        const result = await uiReconMod.runPhase0({
          page, frame: gameFrame, context,
          engineMod, stateMod, engineInfo,
          dirs, snapshots,
          opts,
          logger: dlog_r,
        });
        uiMap = result;
        uiFrameHash = result && result.ui_frame_hash ? result.ui_frame_hash : null;
        // M4: dump fresh probes to sidebar_snapshots.jsonl (kind=manual_regions)
        // and refresh the passive baseline so subsequent observeCurrentState
        // calls diff against the latest frame.
        let sidebarProbesWritten = 0;
        try { sidebarProbesWritten = writeSidebarProbes(uiMap, 'manual_regions'); } catch (e) { dlog_r('sidebar probes write err: ' + e.message); }
        try {
          const baseline = await uiReconMod.captureSidebarState(gameFrame, uiMap ? uiMap.regions_catalog : null);
          lastSidebarFingerprint = uiReconMod.fingerprintSidebar(baseline);
          fs.appendFileSync(dirs.sidebarSnapshots, JSON.stringify({
            ts: Date.now(),
            kind: 'manual_regions_baseline',
            sidebar_fingerprint: lastSidebarFingerprint,
            regions: baseline.regions,
            passage: (lastState && lastState.passage) || null,
            state_hash: lastHash || null,
            ui_frame_hash: uiFrameHash,
          }) + '\n');
        } catch (e) { dlog_r('sidebar manual baseline err: ' + e.message); }
        const screenshot = await captureScreenshot('regions');
        return {
          ok: true,
          duration_ms: Date.now() - start,
          regions_count: result && result.regions ? result.regions.length : 0,
          probes_count: result && result.chrome_probes ? result.chrome_probes.length : 0,
          sidebar_probes_written: sidebarProbesWritten,
          ui_map_path: dirs.uiMap,
          screenshot,
        };
      } catch (e) {
        return { ok: false, error: e.message, stack: e.stack, screenshot: await captureScreenshot('regions_err') };
      }
    },

    // ----------------------------------------------------------------------
    // M6.2 — Navigation intelligence query endpoints.
    // All four are read-only lookups against the in-memory staticGraphData
    // + variableIndexData + pathfinderCtx. They do NOT click anything and
    // do NOT mutate daemon state. Claude uses them to plan before clicking.
    // ----------------------------------------------------------------------

    async path({ args }) {
      if (!pathfinderCtx) return { ok: false, error: 'pathfinder unavailable — static_graph missing or empty' };
      const pathfinderMod = require(path.join(SKILL_DIR, 'scripts/lib/pathfinder'));
      const positional = (args._ || []).filter((a) => a !== 'path');
      const to = positional.join(' ').trim();
      if (!to) return { ok: false, error: 'usage: path <target_passage> [--ignore-gates] [--max-hops N]' };
      const maxHops = args.max_hops ? Math.max(1, Math.min(50, Number(args.max_hops))) : 20;
      const ignoreGates = !!args.ignore_gates;
      return pathfinderMod.findPath(pathfinderCtx, {
        from: lastState.passage,
        to,
        variables: lastState.variables || {},
        maxHops,
        ignoreGates,
      });
    },

    async requirements({ args }) {
      if (!pathfinderCtx) return { ok: false, error: 'pathfinder unavailable — static_graph missing or empty' };
      const pathfinderMod = require(path.join(SKILL_DIR, 'scripts/lib/pathfinder'));
      const positional = (args._ || []).filter((a) => a !== 'requirements');
      const to = positional.join(' ').trim();
      if (!to) return { ok: false, error: 'usage: requirements <target_passage>' };
      if (!pathfinderCtx.passageSet.has(to) && to !== lastState.passage) {
        return { ok: false, error: `target passage "${to}" not in static graph` };
      }
      const result = pathfinderMod.computeRequirements(pathfinderCtx, {
        from: lastState.passage,
        to,
        variables: lastState.variables || {},
      });
      return { ok: true, ...result };
    },

    async reachable({ args }) {
      if (!pathfinderCtx) return { ok: false, error: 'pathfinder unavailable — static_graph missing or empty' };
      const pathfinderMod = require(path.join(SKILL_DIR, 'scripts/lib/pathfinder'));
      const positional = (args._ || []).filter((a) => a !== 'reachable');
      const hopsArg = args.max_hops || positional[0];
      const maxHops = hopsArg ? Math.max(1, Math.min(15, Number(hopsArg))) : 5;
      const result = pathfinderMod.reachableFrom(pathfinderCtx, {
        from: lastState.passage,
        variables: lastState.variables || {},
        maxHops,
      });
      // Cap each bucket for response envelope sanity (the full data is on disk).
      const cap = Number(args.cap) || 100;
      return {
        ok: true,
        ...result,
        open: result.open.slice(0, cap),
        gated_satisfiable: result.gated_satisfiable.slice(0, cap),
        gated_blocked: result.gated_blocked.slice(0, cap),
        truncated: {
          open: result.open.length > cap,
          gated_satisfiable: result.gated_satisfiable.length > cap,
          gated_blocked: result.gated_blocked.length > cap,
        },
      };
    },

    async setters({ args }) {
      if (!pathfinderCtx) return { ok: false, error: 'pathfinder unavailable — variable_index missing or empty' };
      const pathfinderMod = require(path.join(SKILL_DIR, 'scripts/lib/pathfinder'));
      const positional = (args._ || []).filter((a) => a !== 'setters');
      let varName = positional.join(' ').trim();
      if (!varName) return { ok: false, error: 'usage: setters <$variable>' };
      // Allow callers to omit the sigil — auto-add $ if missing.
      if (!varName.startsWith('$') && !varName.startsWith('_')) varName = '$' + varName;
      return pathfinderMod.lookupSetters(pathfinderCtx, varName);
    },

    async status() {
      return {
        ok: true,
        slug, url,
        pid: process.pid,
        port: server.address().port,
        idle_ms: idleMs,
        unique_states_seen: explored.size,
        passage: lastState.passage,
        state_hash: lastHash,
        snapshots_held: snapshots.size,
        frontier_size: frontier.size(),
        engine: engineInfo.engine,
      };
    },

    async finalize() {
      const result = await shutdown({ reason: 'finalize', writeReport: true });
      return { ok: true, command: 'finalize', ...result };
    },

    async stop() {
      const result = await shutdown({ reason: 'stop', writeReport: false });
      return { ok: true, command: 'stop', ...result };
    },
  };

  server = http.createServer((req, res) => {
    if (req.method !== 'POST' || req.url !== '/cmd') {
      res.statusCode = 404; res.end('not found'); return;
    }
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', async () => {
      let payload;
      try { payload = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}'); }
      catch (e) { res.statusCode = 400; res.end(JSON.stringify({ ok: false, error: 'bad json' })); return; }
      resetIdle();
      const cmd = payload.cmd;
      const handler = handlers[cmd];
      if (!handler) { res.statusCode = 404; res.end(JSON.stringify({ ok: false, error: 'unknown cmd: ' + cmd })); return; }
      const logEntry = { ts: new Date().toISOString(), session_id: session.id, cmd, args: summarizeArgsForLog(payload.args) };
      try {
        const result = await handler({ args: payload.args || {}, argv: payload.argv || [] });
        logEntry.ok = !!result.ok;
        if (result.passage != null) logEntry.passage = result.passage;
        if (result.state_hash != null) logEntry.state_hash = result.state_hash;
        if (result.clicked_text != null) logEntry.clicked_text = result.clicked_text;
        if (result.method) logEntry.method = result.method;
        if (result.state_changed != null) logEntry.state_changed = result.state_changed;
        if (!result.ok && result.error) logEntry.error = result.error;
        try { fs.appendFileSync(dirs.playLog, JSON.stringify(logEntry) + '\n'); } catch (_) {}
        // Enrich response envelope with Phase 0 metadata.
        // - ui_frame_hash: cheap fingerprint of the chrome region layout, included always
        // - ui_map_path: path to ui_map.json if present on disk, included always (lightweight)
        // - ui_map: full map inline — only on the commands Claude explicitly invokes to see it
        // - phase0: summary — only on the first response from `start`/`peek` so Claude can ack it ran
        const envelope = { command: cmd, ...result };
        if (uiFrameHash != null && envelope.ui_frame_hash == null) envelope.ui_frame_hash = uiFrameHash;
        if (envelope.ui_map_path == null && fs.existsSync(dirs.uiMap)) envelope.ui_map_path = dirs.uiMap;
        if ((cmd === 'peek' || cmd === 'regions') && uiMap && envelope.ui_map == null) envelope.ui_map = uiMap;
        if (cmd === 'peek' && phase0Result && envelope.phase0 == null) envelope.phase0 = phase0Result;
        res.statusCode = 200;
        res.setHeader('content-type', 'application/json');
        res.end(JSON.stringify(envelope));
      } catch (e) {
        dlog(`handler ${cmd} err: ${e.message}`);
        logEntry.ok = false; logEntry.error = e.message;
        try { fs.appendFileSync(dirs.playLog, JSON.stringify(logEntry) + '\n'); } catch (_) {}
        const scr = await captureScreenshot(cmd + '_err').catch(() => null);
        res.statusCode = 200;
        res.setHeader('content-type', 'application/json');
        res.end(JSON.stringify({ ok: false, command: cmd, error: e.message, stack: e.stack, screenshot: scr }));
      }
    });
  });

  server.listen(0, '127.0.0.1', () => {
    const port = server.address().port;
    const info = {
      slug, url, pid: process.pid, port,
      started_at: new Date().toISOString(),
      ready: true,
    };
    fs.writeFileSync(dirs.lockfile, JSON.stringify(info, null, 2));
    dlog(`daemon listening on 127.0.0.1:${port}`);
    resetIdle();
  });

  // Signal handlers
  const gracefulExit = async (sig) => {
    dlog(`signal ${sig}, shutting down`);
    await shutdown({ reason: 'signal:' + sig, writeReport: false });
  };
  process.on('SIGINT', () => gracefulExit('SIGINT'));
  process.on('SIGTERM', () => gracefulExit('SIGTERM'));
  process.on('uncaughtException', (e) => { dlog('uncaught: ' + e.stack); });
}

// ----------------------------------------------------------------------------
// Shared utils
// ----------------------------------------------------------------------------

function makeLogger(file) {
  return (msg) => {
    const line = `[${new Date().toISOString()}] ${msg}\n`;
    try { fs.appendFileSync(file, line); } catch (e) {}
  };
}

function escapeRegex(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function summarizeVariables(vars) {
  // Short JSON-ish view: top-level keys + their type/value summary
  const out = {};
  if (!vars || typeof vars !== 'object') return out;
  for (const [k, v] of Object.entries(vars)) {
    if (v && typeof v === 'object') {
      if (Array.isArray(v)) out[k] = `[array len=${v.length}]`;
      else out[k] = `{object keys=${Object.keys(v).length}}`;
    } else {
      const s = typeof v === 'string' ? v.slice(0, 80) : v;
      out[k] = s;
    }
  }
  return out;
}

function safeJson(v) {
  try {
    JSON.stringify(v);
    return v;
  } catch (e) {
    return String(v);
  }
}

function summarizeArgsForLog(args) {
  if (!args) return {};
  const out = {};
  if (Array.isArray(args._) && args._.length) out.positional = args._;
  for (const k of ['xy', 'selector', 'value', 'index', 'filter', 'limit', 'ms', 'note', 'force', 'visible']) {
    if (args[k] != null) out[k] = args[k];
  }
  return out;
}
