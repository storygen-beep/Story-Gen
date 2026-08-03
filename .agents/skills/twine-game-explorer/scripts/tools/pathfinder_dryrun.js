#!/usr/bin/env node
// pathfinder_dryrun.js — Tier 2 viability measurement harness.
//
// Drives the existing twine-game-explorer daemon through planned click
// chains and records what actually happens at each hop. Zero new daemon
// endpoints; zero modification to shipped skill code. Talks to the daemon
// via the same POST /cmd HTTP transport used by the regular CLI.
//
// Per trial:
//   1. snap                         → capture pre-trial state
//   2. pick target passage          → random_reachable | preset
//   3. path <target>                → get planned click chain
//   4. for each step:
//        click <click_text>
//        peek
//        classify match | divergence | click_failed
//      break on first non-match
//   5. restore <snap_id>            → reset for next trial
//
// Usage:
//   node pathfinder_dryrun.js --slug <slug> --trials N [--seed N]
//                             [--max-depth N] [--target-strategy S]
//
// Writes:
//   game_explorations/<slug>/dryrun_report.json
//   game_explorations/<slug>/dryrun_report.md
//
// A daemon must already be running for <slug> — start with:
//   node .claude/skills/twine-game-explorer/scripts/live.js start \
//     --url <URL> --slug <slug> [--headless]

'use strict';

const fs = require('fs');
const http = require('http');
const path = require('path');

// Navigate strategy lives in a shared lib so the live daemon can use it
// via an in-process call helper. We only need the high-level wrapper and
// the tags-map builder — nothing else from gate_eval is used directly
// here (the shared navigator owns that dependency).
const { pursueGoal, buildTagsMap } = require(path.resolve(__dirname, '..', 'lib', 'navigator.js'));

// ---------------------------------------------------------------------------
// CLI parsing
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const out = {
    slug: null,
    trials: 50,
    seed: 1,
    maxDepth: 7,
    targetStrategy: 'random_reachable',
    presetFile: null,
    gamesRoot: null,
    reportSuffix: '',
    // Execution strategy: `full_plan` (original — plan once, execute blindly)
    // or `navigate` (greedy re-plan per step, resolve prerequisites up to
    // --prereq-depth levels, abort cleanly on unresolvable / runaway / guard).
    strategy: 'full_plan',
    prereqDepth: 2,
    budget: 15,
    narrativeTags: 'scene,event,story,narrative',
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slug') out.slug = argv[++i];
    else if (a === '--trials') out.trials = Math.max(1, Number(argv[++i]));
    else if (a === '--seed') out.seed = Number(argv[++i]);
    else if (a === '--max-depth') out.maxDepth = Math.max(1, Number(argv[++i]));
    else if (a === '--games-root') out.gamesRoot = argv[++i];
    else if (a === '--report-suffix') out.reportSuffix = argv[++i];
    else if (a === '--strategy') out.strategy = argv[++i];
    else if (a === '--prereq-depth') out.prereqDepth = Math.max(0, Number(argv[++i]));
    else if (a === '--budget') out.budget = Math.max(1, Number(argv[++i]));
    else if (a === '--narrative-tags') out.narrativeTags = argv[++i];
    else if (a === '--target-strategy') {
      const v = argv[++i];
      if (v.startsWith('preset:')) {
        out.targetStrategy = 'preset';
        out.presetFile = v.slice('preset:'.length);
      } else {
        out.targetStrategy = v; // 'random_reachable'
      }
    } else if (a === '--help' || a === '-h') {
      console.log(
        'Usage: pathfinder_dryrun.js --slug <slug> [--trials N] [--seed N]\n' +
          '                           [--strategy full_plan|navigate]\n' +
          '                           [--prereq-depth N] [--budget N]\n' +
          '                           [--narrative-tags scene,event,...]\n' +
          '                           [--max-depth N]\n' +
          '                           [--target-strategy random_reachable|preset:<file>]\n' +
          '                           [--games-root <dir>] [--report-suffix <s>]\n'
      );
      process.exit(0);
    }
  }
  if (!out.slug) {
    console.error('ERROR: --slug is required');
    process.exit(1);
  }
  if (out.strategy !== 'full_plan' && out.strategy !== 'navigate') {
    console.error(`ERROR: --strategy must be full_plan or navigate (got "${out.strategy}")`);
    process.exit(1);
  }
  return out;
}

// ---------------------------------------------------------------------------
// Seeded PRNG — mulberry32. Used for reproducible random target picks.
// ---------------------------------------------------------------------------

function mulberry32(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------------------------------------------------------------------------
// Daemon client — lockfile discovery + HTTP POST to /cmd.
// ---------------------------------------------------------------------------

function readLockfile(slugDir) {
  const lock = path.join(slugDir, '.live', 'daemon.json');
  if (!fs.existsSync(lock)) return null;
  try { return JSON.parse(fs.readFileSync(lock, 'utf8')); }
  catch (e) { return null; }
}

function pidAlive(pid) {
  if (!pid) return false;
  try { process.kill(pid, 0); return true; } catch (e) { return false; }
}

function postCmd(port, body, { timeoutMs = 60000 } = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request(
      {
        host: '127.0.0.1',
        port,
        path: '/cmd',
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'content-length': Buffer.byteLength(data),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf8');
          try { resolve(JSON.parse(raw)); }
          catch (e) { resolve({ ok: false, error: 'daemon returned non-JSON: ' + raw.slice(0, 200) }); }
        });
      }
    );
    req.setTimeout(timeoutMs, () => { req.destroy(new Error('daemon request timeout')); });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function makeDaemonClient(port) {
  // Mirror live.js: send {cmd, args: {_:[cmd, ...positional], ...flags}, argv}.
  // Handlers filter out the command name themselves (e.g. live.js:1104).
  async function call(cmd, positional = [], flags = {}, { timeoutMs } = {}) {
    const args = { _: [cmd, ...positional], ...flags };
    const argv = [cmd, ...positional];
    for (const [k, v] of Object.entries(flags)) {
      argv.push('--' + k, String(v));
    }
    return postCmd(port, { cmd, args, argv }, { timeoutMs });
  }
  return call;
}

// ---------------------------------------------------------------------------
// Divergence classification helpers — all use static data loaded once.
// ---------------------------------------------------------------------------

const DYNAMIC_GOTO_RE = /<<goto\s+[$_][A-Za-z_][A-Za-z0-9_]*/;
const RANDOM_EVENT_TAG_RE = /^(random|event|interrupt)$/i;
const RANDOM_EVENT_NAME_RE = /random|event|interrupt/i;

function buildClassifier(staticGraph, passageCatalog) {
  // Map: source -> map(text -> edges[]) — lets us check per-source-passage
  // ambiguity for a given click text.
  const outgoingByText = new Map();
  for (const e of staticGraph.edges || []) {
    const text = (e.display || '').trim();
    if (!text) continue;
    const perFrom = outgoingByText.get(e.from) || new Map();
    const edges = perFrom.get(text) || [];
    edges.push(e);
    perFrom.set(text, edges);
    outgoingByText.set(e.from, perFrom);
  }
  const passageByName = new Map();
  for (const p of passageCatalog.passages || []) {
    passageByName.set(p.name, p);
  }
  return {
    classifyDivergence(sourcePassage, clickText, actualPassage) {
      // 1. Click was reported ok but the passage didn't change. This
      //    happens when Playwright's locator matches a parent element
      //    (e.g. a wrapping <p>/<section>) instead of the actual <a>, so
      //    SugarCube's delegated click handler never fires. From
      //    autopilot's perspective the click is ineffective — treat as
      //    its own bucket so selector-reliability issues are visible.
      if (actualPassage === sourcePassage) return 'click_ineffective';
      // 2. Dynamic-goto on the source passage (static graph couldn't
      //    know the target).
      const src = passageByName.get(sourcePassage);
      if (src && DYNAMIC_GOTO_RE.test(src.source_raw || '')) {
        return 'dynamic_goto';
      }
      // 3. Random-event landing passage (name or tag).
      const actual = passageByName.get(actualPassage);
      if (actual) {
        const tags = actual.tags || [];
        if (tags.some((t) => RANDOM_EVENT_TAG_RE.test(t))) {
          return 'random_event';
        }
        if (RANDOM_EVENT_NAME_RE.test(actualPassage)) {
          return 'random_event';
        }
      }
      // 4. Ambiguous click text: ≥2 outgoing edges from source with same
      //    text going to DIFFERENT targets (matches static_health logic).
      const perFrom = outgoingByText.get(sourcePassage);
      if (perFrom) {
        const shared = perFrom.get(clickText || '');
        if (shared && shared.length >= 2) {
          const targets = new Set(shared.map((e) => e.to));
          if (targets.size >= 2) return 'ambiguous_click';
        }
      }
      // 5. Default: unknown — the interesting bucket, genuine mismatches
      //    that don't fall into known categories.
      return 'unknown';
    },
  };
}

// ---------------------------------------------------------------------------
// Target picking
// ---------------------------------------------------------------------------

async function pickTargets(call, strategy, presetFile, maxHops, rand) {
  if (strategy === 'preset') {
    if (!presetFile) throw new Error('preset strategy needs --target-strategy preset:<file>');
    const raw = fs.readFileSync(presetFile, 'utf8');
    const targets = raw
      .split('\n')
      .map((l) => l.replace(/#.*$/, '').trim())
      .filter((l) => l.length > 0);
    return { kind: 'preset', targets, cursor: 0 };
  }
  // random_reachable: query reachable once, then pick randomly from `open`
  // and `gated_satisfiable` (gates evaluate true OR unknown — both are
  // cases where autopilot might plan a path). `gated_blocked` is skipped:
  // pathfinder won't even plan through those without --ignore-gates.
  const res = await call('reachable', [], { max_hops: Math.max(5, maxHops) });
  if (!res.ok) throw new Error('reachable query failed: ' + (res.error || 'unknown'));
  const open = (res.open || []).map((o) => ({ passage: o.passage, class: 'open' }));
  const satisfiable = (res.gated_satisfiable || []).map((o) => ({
    passage: o.passage, class: 'gated_satisfiable',
  }));
  const pool = [...open, ...satisfiable];
  if (!pool.length) {
    throw new Error('no reachable passages; daemon at a terminal/isolated passage?');
  }
  return { kind: 'random', pool, rand };
}

function nextTarget(picker) {
  if (picker.kind === 'preset') {
    if (picker.cursor >= picker.targets.length) return null;
    return { passage: picker.targets[picker.cursor++], class: 'preset' };
  }
  const idx = Math.floor(picker.rand() * picker.pool.length);
  return picker.pool[idx];
}

// ---------------------------------------------------------------------------
// Navigate strategy — goal-pursuit loop
// ---------------------------------------------------------------------------
//
// Unlike full_plan (plan once, execute blindly), navigate re-plans after
// every click against LIVE variable state. When the next step's gate
// evaluates false, it consults the variable_index to find setter passages
// that would satisfy the gate, chooses a non-narrative-tagged candidate,
// and pursues that passage as a sub-goal (bounded by prereqDepth).
//
// Terminal states surface as abort_reason on the trial record:
//   reached                  → success
//   budget_exceeded          → ran out of steps across main + subgoals
//   state_loop_detected      → same state_hash seen 3+ times, bail out
//   unreachable              → pathfinder says no path, even ignoring gates
//   not_navigable            → next edge is goto/non-wiki or lacks click_text
//   click_failed_true_gate   → gate said true but click ok=false (selector bug / hidden by dyn state)
//   unknown_gate_blocked     → gate unknown, click ok=false (confirms false at runtime)
//   divergence_detected      → clicked fine but landed somewhere unexpected
//   prereq_depth_exhausted   → gate false, depth limit hit, can't resolve deeper
//   prereq_no_setter         → gate false, no setter found for gate vars
//   prereq_narrative_guarded → all candidate setters are narrative-tagged
//   prereq_subgoal_failed    → subgoal pursuit itself failed

// Per-trial outer wrapper for the navigate strategy. Sets up snap/restore,
// instantiates ctx, invokes navigate, captures timing.
async function runNavigateTrial(call, trialId, target, opts) {
  const trial = {
    trial_id: trialId,
    target,
    strategy: 'navigate',
    outcome: null,
    abort_reason: null,
    navigate_trace: [],
    subgoal_max_depth: 0,
    distinct_passages_visited: 0,
    total_ms: 0,
    snap_id: null,
    pre_trial_passage: null,
    steps: [], // kept for compatibility with summarize/report
  };
  const tStart = Date.now();
  const snapRes = await call('snap', [], { note: `nav-trial-${trialId}-start` });
  if (!snapRes.ok) {
    trial.outcome = 'snap_failed';
    trial.abort_reason = 'snap_failed';
    trial.total_ms = Date.now() - tStart;
    return trial;
  }
  trial.snap_id = snapRes.snap_id;
  trial.pre_trial_passage = snapRes.passage;

  const result = await pursueGoal(target, {
    call,
    tagsMap: opts.tagsMap,
    narrativeTagSet: opts.narrativeTagSet,
    prereqDepth: opts.prereqDepth,
    budget: opts.budget,
  });
  trial.navigate_trace = result.trace || [];
  trial.subgoal_max_depth = result.subgoal_max_depth || 0;
  trial.distinct_passages_visited = new Set(
    trial.navigate_trace
      .filter((ev) => ev.kind === 'click' || ev.kind === 'reached')
      .map((ev) => ev.to || ev.at)
      .filter(Boolean)
  ).size;
  if (result.reached) {
    trial.outcome = 'clean';
  } else {
    trial.outcome = 'aborted';
    trial.abort_reason = result.abort_reason;
    if (result.expected_to) trial.expected_to = result.expected_to;
    if (result.actual_passage) trial.actual_passage = result.actual_passage;
    if (result.blocking_gate) trial.blocking_gate = result.blocking_gate;
    if (result.sub_abort) trial.sub_abort = result.sub_abort;
    if (result.error) trial.error = result.error;
  }
  // Restore regardless so next trial starts from same baseline.
  const restoreRes = await call('restore', [trial.snap_id]);
  trial.restore_ok = !!restoreRes.ok;
  trial.restore_passage = restoreRes.passage || null;
  trial.restore_contamination_risk = !restoreRes.ok || restoreRes.passage !== trial.pre_trial_passage;
  trial.total_ms = Date.now() - tStart;
  return trial;
}

// ---------------------------------------------------------------------------
// Per-trial execution
// ---------------------------------------------------------------------------

async function runTrial(
  call,
  trialId,
  target,
  maxDepth,
  classifier,
  { beforePassage } = {}
) {
  const trial = {
    trial_id: trialId,
    target,
    strategy: 'full_plan',
    pre_trial_passage: beforePassage,
    outcome: null,
    plan_length: 0,
    steps: [],
    total_ms: 0,
    snap_id: null,
  };
  const tStart = Date.now();

  // Snap pre-trial state.
  const snapRes = await call('snap', [], { note: `trial-${trialId}-start` });
  if (!snapRes.ok) {
    trial.outcome = 'snap_failed';
    trial.error = snapRes.error || 'snap returned !ok';
    trial.total_ms = Date.now() - tStart;
    return trial;
  }
  trial.snap_id = snapRes.snap_id;
  trial.pre_trial_passage = snapRes.passage; // authoritative

  // Plan.
  const planRes = await call('path', [target]);
  if (!planRes || !planRes.ok || !planRes.found) {
    trial.outcome = 'plan_failed';
    trial.error = planRes ? planRes.error || planRes.summary : 'no response';
    trial.plan_response_summary = planRes ? planRes.summary : null;
    await call('restore', [trial.snap_id]);
    trial.total_ms = Date.now() - tStart;
    return trial;
  }
  const plan = planRes.path || [];
  trial.plan_length = plan.length;
  if (plan.length === 0) {
    // Zero-step plan = already at target. Count as clean.
    trial.outcome = 'clean';
    trial.total_ms = Date.now() - tStart;
    await call('restore', [trial.snap_id]);
    return trial;
  }
  if (plan.length > maxDepth) {
    trial.outcome = 'plan_too_long';
    trial.plan_length = plan.length;
    await call('restore', [trial.snap_id]);
    trial.total_ms = Date.now() - tStart;
    return trial;
  }

  // Execute step by step.
  let cleanSoFar = true;
  for (let i = 0; i < plan.length; i++) {
    const step = plan[i];
    const expected_from = step.from;
    const expected_to = step.to;
    const click_text = step.click_text;
    const stepRecord = {
      step_index: i,
      expected_from,
      expected_to,
      click_text,
      edge_kind: step.edge_kind,
      gate_result: step.gate_result,
      outcome: null,
      actual_passage: null,
      divergence_cause: null,
      step_ms: 0,
    };
    const sStart = Date.now();
    // Dynamic-goto edges / edges without click text can't be executed via
    // the text-based click endpoint. Mark as not_executable.
    if (!click_text || step.edge_kind === 'goto') {
      stepRecord.outcome = 'not_executable';
      stepRecord.divergence_cause = step.edge_kind === 'goto' ? 'dynamic_goto' : 'no_click_text';
      stepRecord.step_ms = Date.now() - sStart;
      trial.steps.push(stepRecord);
      cleanSoFar = false;
      trial.outcome = 'diverged';
      trial.diverged_at_step = i;
      trial.divergence_cause = stepRecord.divergence_cause;
      break;
    }
    const clickRes = await call('click', [click_text]);
    if (!clickRes.ok) {
      stepRecord.outcome = 'click_failed';
      stepRecord.click_error = clickRes.error || 'click returned !ok';
      stepRecord.step_ms = Date.now() - sStart;
      trial.steps.push(stepRecord);
      cleanSoFar = false;
      trial.outcome = 'click_failed';
      trial.diverged_at_step = i;
      break;
    }
    // Peek is implicit in click's response, but we call peek anyway for
    // the canonical `passage` field and for timing consistency.
    const peekRes = await call('peek');
    stepRecord.actual_passage = peekRes.passage || clickRes.passage;
    stepRecord.step_ms = Date.now() - sStart;
    if (stepRecord.actual_passage === expected_to) {
      stepRecord.outcome = 'match';
    } else {
      stepRecord.outcome = 'divergence';
      stepRecord.divergence_cause = classifier.classifyDivergence(
        expected_from,
        click_text,
        stepRecord.actual_passage
      );
      trial.steps.push(stepRecord);
      cleanSoFar = false;
      trial.outcome = 'diverged';
      trial.diverged_at_step = i;
      trial.divergence_cause = stepRecord.divergence_cause;
      trial.expected_to = expected_to;
      trial.actual_passage = stepRecord.actual_passage;
      break;
    }
    trial.steps.push(stepRecord);
  }
  if (cleanSoFar) trial.outcome = 'clean';

  // Restore regardless of outcome, so next trial starts from same state.
  const restoreRes = await call('restore', [trial.snap_id]);
  trial.restore_ok = !!restoreRes.ok;
  trial.restore_passage = restoreRes.passage || null;
  if (!restoreRes.ok || restoreRes.passage !== trial.pre_trial_passage) {
    // Restore failure or landed at unexpected passage — this trial's
    // successor may be contaminated. Flag so Stage 3b detects it.
    trial.restore_contamination_risk = true;
  } else {
    trial.restore_contamination_risk = false;
  }
  trial.total_ms = Date.now() - tStart;
  return trial;
}

// ---------------------------------------------------------------------------
// Aggregation
// ---------------------------------------------------------------------------

function summarizeTrials(trials) {
  let clean = 0;
  let diverged = 0;
  let clickFailed = 0;
  let planFailed = 0;
  let planTooLong = 0;
  let snapFailed = 0;
  let aborted = 0; // navigate-strategy abortive outcomes
  const divergenceBuckets = {};
  const abortReasonBuckets = {}; // navigate-strategy abort reasons
  const perDepthCount = {}; // depth -> {trials, failures}
  const sourceCounts = {}; // `${from}` -> {divergences, trials_involving}
  let restoreMishaps = 0;

  // Navigate-specific counters.
  let subgoalsAttempted = 0;
  let subgoalsSucceeded = 0;
  let navClickEvents = 0;
  let navPrereqEvents = 0;
  for (const t of trials) {
    if (t.restore_contamination_risk) restoreMishaps++;
    if (t.outcome === 'clean') clean++;
    else if (t.outcome === 'aborted') {
      aborted++;
      const reason = t.abort_reason || 'unknown';
      abortReasonBuckets[reason] = (abortReasonBuckets[reason] || 0) + 1;
    } else if (t.outcome === 'diverged') {
      diverged++;
      const cause = t.divergence_cause || 'unknown';
      divergenceBuckets[cause] = (divergenceBuckets[cause] || 0) + 1;
    } else if (t.outcome === 'click_failed') clickFailed++;
    else if (t.outcome === 'plan_failed') planFailed++;
    else if (t.outcome === 'plan_too_long') planTooLong++;
    else if (t.outcome === 'snap_failed') snapFailed++;

    const depth = t.plan_length || 0;
    const bucket = perDepthCount[depth] || { trials: 0, failures: 0 };
    bucket.trials++;
    if (t.outcome !== 'clean') bucket.failures++;
    perDepthCount[depth] = bucket;

    if (t.outcome === 'diverged' || t.outcome === 'click_failed') {
      const lastStep = t.steps && t.steps.length ? t.steps[t.steps.length - 1] : null;
      if (lastStep && lastStep.expected_from) {
        const sc = sourceCounts[lastStep.expected_from] || { divergences: 0, trials_involving: 0 };
        sc.divergences++;
        sc.trials_involving++;
        sourceCounts[lastStep.expected_from] = sc;
      }
    }

    // Scan navigate trace events: count subgoal attempts/successes and
    // per-event totals for latency stats below.
    if (t.strategy === 'navigate' && Array.isArray(t.navigate_trace)) {
      for (const ev of t.navigate_trace) {
        if (ev.kind === 'click') navClickEvents++;
        if (ev.kind === 'prereq_start') {
          subgoalsAttempted++;
          navPrereqEvents++;
        }
        if (ev.kind === 'prereq_end' && ev.sub_reached) subgoalsSucceeded++;
      }
    }
  }

  const n = trials.length || 1;
  // For navigate strategy, measurable = clean + aborted (we explicitly
  // aborted with a known reason). For full_plan, measurable = clean +
  // diverged + clickFailed as before.
  const measurable = clean + diverged + clickFailed + aborted;
  const pct = (c) => c / n;
  const ratePerDepth = {};
  for (const [d, b] of Object.entries(perDepthCount)) {
    ratePerDepth[d] = {
      trials: b.trials,
      failure_rate: b.trials ? b.failures / b.trials : 0,
    };
  }
  // Divergence breakdown as fraction of TOTAL trials (consistent with
  // plan's decision table). click_failed is its own rate.
  const divergenceBreakdown = {};
  for (const [k, v] of Object.entries(divergenceBuckets)) {
    divergenceBreakdown[k] = v / n;
  }
  const worstSources = Object.entries(sourceCounts)
    .map(([passage, s]) => ({ passage, ...s }))
    .sort((a, b) => b.divergences - a.divergences)
    .slice(0, 10);

  // Per-step median latency (across clean+diverged+click_failed trials
  // that made at least one click attempt).
  const stepLatencies = [];
  for (const t of trials) {
    for (const s of t.steps || []) {
      if (typeof s.step_ms === 'number' && s.step_ms > 0) stepLatencies.push(s.step_ms);
    }
  }
  stepLatencies.sort((a, b) => a - b);
  const medianStepMs =
    stepLatencies.length === 0 ? 0 : stepLatencies[Math.floor(stepLatencies.length / 2)];

  // Per target-class breakdown — how does open-gate pool differ from
  // gated-satisfiable (unknown-gate) pool?
  const perClass = {};
  for (const t of trials) {
    const c = t.target_class || 'unknown';
    const bucket = perClass[c] || { trials: 0, clean: 0, diverged: 0, click_failed: 0, plan_failed: 0 };
    bucket.trials++;
    if (t.outcome === 'clean') bucket.clean++;
    else if (t.outcome === 'diverged') bucket.diverged++;
    else if (t.outcome === 'click_failed') bucket.click_failed++;
    else if (t.outcome === 'plan_failed') bucket.plan_failed++;
    perClass[c] = bucket;
  }
  for (const c of Object.keys(perClass)) {
    const b = perClass[c];
    b.clean_rate = b.trials ? b.clean / b.trials : 0;
    b.clean_rate_of_measurable =
      b.trials && b.clean + b.diverged + b.click_failed > 0
        ? b.clean / (b.clean + b.diverged + b.click_failed)
        : 0;
  }

  // Per-strategy breakdown. Useful when reports from different strategies
  // are combined, or for a single-strategy run as a one-key dict.
  const perStrategy = {};
  for (const t of trials) {
    const s = t.strategy || 'unknown';
    const b = perStrategy[s] || {
      trials: 0, clean: 0, aborted: 0, diverged: 0, click_failed: 0,
      plan_failed: 0, plan_too_long: 0, snap_failed: 0,
    };
    b.trials++;
    if (t.outcome === 'clean') b.clean++;
    else if (t.outcome === 'aborted') b.aborted++;
    else if (t.outcome === 'diverged') b.diverged++;
    else if (t.outcome === 'click_failed') b.click_failed++;
    else if (t.outcome === 'plan_failed') b.plan_failed++;
    else if (t.outcome === 'plan_too_long') b.plan_too_long++;
    else if (t.outcome === 'snap_failed') b.snap_failed++;
    perStrategy[s] = b;
  }
  for (const s of Object.keys(perStrategy)) {
    const b = perStrategy[s];
    const m = b.clean + b.aborted + b.diverged + b.click_failed;
    b.clean_rate_of_measurable = m ? b.clean / m : 0;
    b.clean_rate_of_total = b.trials ? b.clean / b.trials : 0;
  }

  // Abort-reason breakdown as fraction of total trials (navigate-focused).
  const abortReasonBreakdown = {};
  for (const [k, v] of Object.entries(abortReasonBuckets)) abortReasonBreakdown[k] = v / n;

  return {
    trial_count: trials.length,
    measurable_trials: measurable,
    clean_completion_rate: measurable ? clean / measurable : 0,
    clean_completion_rate_of_total: pct(clean),
    divergence_rate: pct(diverged),
    click_failed_rate: pct(clickFailed),
    plan_failed_rate: pct(planFailed),
    plan_too_long_rate: pct(planTooLong),
    snap_failed_rate: pct(snapFailed),
    aborted_rate: pct(aborted),
    restore_mishap_rate: pct(restoreMishaps),
    divergence_breakdown: divergenceBreakdown,
    abort_reason_breakdown: abortReasonBreakdown,
    per_strategy: perStrategy,
    per_depth: ratePerDepth,
    per_target_class: perClass,
    worst_source_passages: worstSources,
    median_step_ms: medianStepMs,
    subgoals_attempted: subgoalsAttempted,
    subgoals_succeeded: subgoalsSucceeded,
    subgoal_success_rate: subgoalsAttempted ? subgoalsSucceeded / subgoalsAttempted : null,
    navigate_click_events: navClickEvents,
    navigate_prereq_events: navPrereqEvents,
  };
}

function renderMarkdown(slug, seed, trialCount, summary, trials) {
  const pct = (n) => (n * 100).toFixed(1) + '%';
  const lines = [];
  lines.push(`# Pathfinder dryrun — ${slug}`);
  lines.push('');
  lines.push(`Trials: ${summary.trial_count}  |  Seed: ${seed}  |  Median step latency: ${summary.median_step_ms}ms`);
  lines.push('');
  lines.push('## Summary');
  lines.push('');
  lines.push('| Metric | Value |');
  lines.push('|---|---|');
  lines.push(`| clean_completion_rate (of measurable) | ${pct(summary.clean_completion_rate)} |`);
  lines.push(`| clean_completion_rate (of total) | ${pct(summary.clean_completion_rate_of_total)} |`);
  lines.push(`| aborted_rate | ${pct(summary.aborted_rate || 0)} |`);
  lines.push(`| divergence_rate | ${pct(summary.divergence_rate)} |`);
  lines.push(`| click_failed_rate | ${pct(summary.click_failed_rate)} |`);
  lines.push(`| plan_failed_rate | ${pct(summary.plan_failed_rate)} |`);
  lines.push(`| plan_too_long_rate | ${pct(summary.plan_too_long_rate)} |`);
  lines.push(`| snap_failed_rate | ${pct(summary.snap_failed_rate)} |`);
  lines.push(`| restore_mishap_rate | ${pct(summary.restore_mishap_rate)} |`);
  if (summary.subgoals_attempted != null && summary.subgoals_attempted > 0) {
    lines.push(`| subgoals_attempted | ${summary.subgoals_attempted} |`);
    lines.push(`| subgoal_success_rate | ${pct(summary.subgoal_success_rate || 0)} |`);
  }
  lines.push('');
  // Per-strategy breakdown.
  if (summary.per_strategy && Object.keys(summary.per_strategy).length) {
    lines.push('## Per-strategy breakdown');
    lines.push('');
    lines.push('| Strategy | Trials | Clean | Aborted | Diverged | ClickFailed | clean / measurable | clean / total |');
    lines.push('|---|---|---|---|---|---|---|---|');
    for (const [s, b] of Object.entries(summary.per_strategy)) {
      lines.push(`| ${s} | ${b.trials} | ${b.clean} | ${b.aborted} | ${b.diverged} | ${b.click_failed} | ${pct(b.clean_rate_of_measurable)} | ${pct(b.clean_rate_of_total)} |`);
    }
    lines.push('');
  }
  // Abort reason breakdown (navigate).
  if (summary.abort_reason_breakdown && Object.keys(summary.abort_reason_breakdown).length) {
    lines.push('## Abort reason breakdown (navigate)');
    lines.push('');
    for (const [k, v] of Object.entries(summary.abort_reason_breakdown)) {
      lines.push(`- ${k}: ${pct(v)}`);
    }
    lines.push('');
  }
  lines.push('## Divergence breakdown (fraction of total trials)');
  lines.push('');
  if (Object.keys(summary.divergence_breakdown).length) {
    for (const [k, v] of Object.entries(summary.divergence_breakdown)) {
      lines.push(`- ${k}: ${pct(v)}`);
    }
  } else {
    lines.push('_No divergences recorded._');
  }
  lines.push('');
  lines.push('## Failure rate by plan depth');
  lines.push('');
  lines.push('| Depth | Trials | Failure rate |');
  lines.push('|---|---|---|');
  const depths = Object.keys(summary.per_depth).map(Number).sort((a, b) => a - b);
  for (const d of depths) {
    const b = summary.per_depth[String(d)];
    lines.push(`| ${d} | ${b.trials} | ${pct(b.failure_rate)} |`);
  }
  lines.push('');
  lines.push('## Worst-offender source passages');
  lines.push('');
  if (summary.worst_source_passages.length) {
    lines.push('| Source passage | Divergences | Trials involving |');
    lines.push('|---|---|---|');
    for (const s of summary.worst_source_passages) {
      lines.push(`| \`${s.passage}\` | ${s.divergences} | ${s.trials_involving} |`);
    }
  } else {
    lines.push('_No divergent trials._');
  }
  lines.push('');
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const gamesRoot = args.gamesRoot
    ? path.resolve(args.gamesRoot)
    : path.resolve(process.cwd(), 'game_explorations');
  const slugDir = path.join(gamesRoot, args.slug);
  if (!fs.existsSync(slugDir)) {
    console.error(`ERROR: slug directory not found: ${slugDir}`);
    process.exit(1);
  }
  const lock = readLockfile(slugDir);
  if (!lock) {
    console.error(
      `ERROR: no running daemon for slug "${args.slug}". Start one with:\n` +
        `  node .claude/skills/twine-game-explorer/scripts/live.js start --slug ${args.slug} --url <URL>`
    );
    process.exit(1);
  }
  if (!pidAlive(lock.pid)) {
    console.error(
      `ERROR: daemon lockfile exists but PID ${lock.pid} is dead. Relaunch with:\n` +
        `  node .claude/skills/twine-game-explorer/scripts/live.js start --slug ${args.slug}`
    );
    process.exit(1);
  }
  const staticGraph = JSON.parse(fs.readFileSync(path.join(slugDir, 'static_graph.json'), 'utf8'));
  const passageCatalog = JSON.parse(fs.readFileSync(path.join(slugDir, 'passage_catalog.json'), 'utf8'));
  const classifier = buildClassifier(staticGraph, passageCatalog);
  // Navigate-strategy inputs: tags map for narrative guard + tag set from CLI.
  const tagsMap = buildTagsMap(passageCatalog);
  const narrativeTagSet = new Set(
    (args.narrativeTags || '').split(',').map((t) => t.trim().toLowerCase()).filter(Boolean)
  );

  const call = makeDaemonClient(lock.port);
  const rand = mulberry32(args.seed);

  // Health check — call status.
  const status = await call('status');
  if (!status.ok) {
    console.error('ERROR: daemon status not OK: ' + (status.error || 'unknown'));
    process.exit(1);
  }
  console.log(
    `Daemon up: slug=${status.slug} pid=${status.pid} engine=${status.engine} passage=${status.passage}`
  );
  console.log(
    `Loaded ${staticGraph.edges.length} edges, ${passageCatalog.passages.length} passages.`
  );

  const picker = await pickTargets(
    call,
    args.targetStrategy,
    args.presetFile,
    args.maxDepth,
    rand
  );
  if (picker.kind === 'random') {
    console.log(`Target pool: ${picker.pool.length} reachable passages.`);
  } else {
    console.log(`Preset targets: ${picker.targets.length} from ${args.presetFile}`);
  }

  const trials = [];
  const trialCount = args.targetStrategy === 'preset' ? picker.targets.length : args.trials;
  console.log(`Strategy: ${args.strategy}  |  prereq-depth: ${args.prereqDepth}  |  budget: ${args.budget}  |  narrative-tags: {${[...narrativeTagSet].join(', ')}}`);
  for (let i = 0; i < trialCount; i++) {
    const target = nextTarget(picker);
    if (target == null) break;
    let trial;
    if (args.strategy === 'navigate') {
      trial = await runNavigateTrial(call, i, target.passage, {
        tagsMap,
        narrativeTagSet,
        prereqDepth: args.prereqDepth,
        budget: args.budget,
      });
    } else {
      trial = await runTrial(call, i, target.passage, args.maxDepth, classifier);
    }
    trial.target_class = target.class;
    trials.push(trial);
    let marker;
    if (trial.outcome === 'clean') marker = 'OK';
    else if (trial.outcome === 'aborted') marker = `ABRT(${trial.abort_reason})`;
    else if (trial.outcome === 'diverged') marker = `DIV(${trial.divergence_cause})`;
    else marker = String(trial.outcome || 'unknown').toUpperCase();
    const extra = args.strategy === 'navigate'
      ? `sub_depth=${trial.subgoal_max_depth || 0} visited=${trial.distinct_passages_visited || 0}`
      : `plan=${trial.plan_length}`;
    process.stdout.write(
      `[${i + 1}/${trialCount}] ${marker.padEnd(28).slice(0, 28)} target=${String(target.passage).padEnd(26).slice(0, 26)} ${extra} ${trial.total_ms}ms\n`
    );
  }

  const summary = summarizeTrials(trials);
  const suffix = args.reportSuffix ? '_' + args.reportSuffix : '';
  const report = {
    slug: args.slug,
    seed: args.seed,
    trial_count: trials.length,
    target_strategy: args.targetStrategy + (args.presetFile ? ':' + args.presetFile : ''),
    max_depth: args.maxDepth,
    generated_at: new Date().toISOString(),
    summary,
    trials,
  };
  const jsonPath = path.join(slugDir, `dryrun_report${suffix}.json`);
  const mdPath = path.join(slugDir, `dryrun_report${suffix}.md`);
  fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
  fs.writeFileSync(mdPath, renderMarkdown(args.slug, args.seed, trials.length, summary, trials));

  console.log('');
  console.log('======== Summary ========');
  console.log(`  clean_completion_rate (of measurable): ${(summary.clean_completion_rate * 100).toFixed(1)}%`);
  console.log(`  clean_completion_rate (of total):      ${(summary.clean_completion_rate_of_total * 100).toFixed(1)}%`);
  console.log(`  aborted_rate: ${((summary.aborted_rate || 0) * 100).toFixed(1)}%`);
  console.log(`  divergence_rate: ${(summary.divergence_rate * 100).toFixed(1)}%`);
  console.log(`  click_failed_rate: ${(summary.click_failed_rate * 100).toFixed(1)}%`);
  console.log(`  plan_failed_rate: ${(summary.plan_failed_rate * 100).toFixed(1)}%`);
  console.log(`  median_step_ms: ${summary.median_step_ms}ms`);
  console.log(`  restore_mishap_rate: ${(summary.restore_mishap_rate * 100).toFixed(1)}%`);
  if (summary.subgoals_attempted > 0) {
    console.log(`  subgoals: ${summary.subgoals_succeeded}/${summary.subgoals_attempted} succeeded (${((summary.subgoal_success_rate || 0) * 100).toFixed(1)}%)`);
  }
  if (summary.abort_reason_breakdown && Object.keys(summary.abort_reason_breakdown).length) {
    console.log('  abort reasons:');
    for (const [k, v] of Object.entries(summary.abort_reason_breakdown)) {
      console.log(`    ${k.padEnd(32)} ${((v) * 100).toFixed(1)}%`);
    }
  }
  console.log(`Report: ${jsonPath}`);
}

main().catch((e) => {
  console.error('FATAL: ' + (e && e.stack ? e.stack : e));
  process.exit(1);
});
