// Goal-pursuit navigator — the "smart autopilot" that replaces
// blind plan-and-execute with a greedy loop that checks runtime
// gate state at each step and resolves unsatisfied prerequisites
// up to a bounded depth.
//
// Extracted from scripts/tools/pathfinder_dryrun.js's navigate
// strategy so both the measurement harness and the live daemon can
// share one implementation. The only environmental dependency is a
// `call(cmd, positional, flags)` function that the caller provides —
// the harness wires it to an HTTP client, the daemon wires it to
// direct handler dispatch. All other state (tag map, narrative set,
// budget, depth limit) is passed via opts.
//
// Terminal abort reasons (same as harness):
//   reached                  — success
//   budget_exceeded          — ran out of steps across main + subgoals
//   state_loop_detected      — same state_hash seen ≥3 times
//   unreachable              — no topological path to target
//   not_navigable            — next step is non-clickable (goto w/o wrapper)
//   click_failed_true_gate   — gate evaluated true, click.ok=false
//   unknown_gate_blocked     — gate unknown, click.ok=false
//   divergence_detected      — click succeeded but landed elsewhere
//   prereq_depth_exhausted   — gate false, depth budget hit
//   prereq_no_setter         — gate false, no setter for gate vars
//   prereq_narrative_guarded — setter candidate is narrative-tagged
//   prereq_setter_at_self    — setter host is the current passage (no-op)
//   prereq_unreachable       — setter host unreachable topologically
//   prereq_subgoal_failed    — subgoal navigation itself failed
//   peek_failed              — daemon's peek returned !ok
//   navigate_threw           — unexpected exception inside the loop

'use strict';

const path = require('path');
const { evaluateGate, extractVars } = require(path.resolve(__dirname, 'gate_eval.js'));

const CLICKABLE_KINDS = new Set(['wiki', 'link', 'button']);

// -------- Small helpers shared by the loop --------

// Fetch live variables via daemon's eval endpoint rather than peek's
// truncated summarizeVariables. We need actual nested structure so gate
// conditions like `$player.energy` evaluate correctly. Fall back to peek's
// summary if eval fails.
async function fetchLiveVariables(call) {
  try {
    const res = await call('eval', [
      'return JSON.parse(JSON.stringify(SugarCube.State.variables || {}))',
    ]);
    if (res && res.ok && res.result && typeof res.result === 'object') return res.result;
  } catch (e) {}
  try {
    const peek = await call('peek');
    return (peek && peek.variable_summary) || {};
  } catch (e) {
    return {};
  }
}

// Evaluate an edge's gate stack as a conjunction. The parser ALREADY
// stores the final, post-negation condition in `frame.condition` —
// `<<else>>` branches are stored as `!(prior)` and `<<elseif>>` branches
// store their own condition. The `branch` field is informational only;
// do not re-negate based on it. Returns true/false/'unknown'.
//
// This sync variant is used by `simulateSetterSatisfies` — we're
// evaluating a HYPOTHETICAL state, so live eval (which calls real
// game helpers against REAL state) would be a correctness bug.
function evaluateEdgeGate(gate, variables) {
  if (!gate || !gate.length) return true;
  let combined = true;
  for (const frame of gate) {
    const cond = frame.condition || '';
    const r = evaluateGate(cond, variables);
    if (r.result === false) return false;
    if (r.result === 'unknown') combined = 'unknown';
  }
  return combined;
}

function parseValueExpr(expr) {
  if (typeof expr !== 'string') return { ok: false };
  const trimmed = expr.trim();
  if (!trimmed) return { ok: false };
  const sMatch =
    trimmed.match(/^"([^"\\]*(?:\\.[^"\\]*)*)"$/) ||
    trimmed.match(/^'([^'\\]*(?:\\.[^'\\]*)*)'$/);
  if (sMatch) return { ok: true, value: sMatch[1].replace(/\\(.)/g, '$1') };
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) return { ok: true, value: Number(trimmed) };
  if (trimmed === 'true') return { ok: true, value: true };
  if (trimmed === 'false') return { ok: true, value: false };
  if (trimmed === 'null') return { ok: true, value: null };
  return { ok: false };
}

function rootVarName(ref) {
  if (!ref) return ref;
  const stripped = ref.replace(/^[$_]/, '');
  const m = stripped.match(/^[A-Za-z_][A-Za-z0-9_]*/);
  return m ? m[0] : stripped;
}

// Simulate applying a setter to the current variables and return whether
// the target gate would flip to TRUE. Setters with non-literal value_expr
// or non-assignment op return false so the caller skips them.
function simulateSetterSatisfies(gate, currentVars, varSigilRef, setter) {
  if (!setter) return false;
  if (setter.op !== '=' && setter.op !== 'to') return false;
  const parsed = parseValueExpr(setter.value_expr);
  if (!parsed.ok) return false;
  const rootKey = rootVarName(varSigilRef);
  const pathSuffix = setter.path || null;
  const newVars = JSON.parse(JSON.stringify(currentVars || {}));
  if (!pathSuffix) {
    newVars[rootKey] = parsed.value;
  } else {
    if (/[\[\]]/.test(pathSuffix)) return false;
    const segments = pathSuffix.replace(/^\./, '').split('.').filter(Boolean);
    if (!segments.length) return false;
    let cur = newVars;
    if (!cur[rootKey] || typeof cur[rootKey] !== 'object') cur[rootKey] = {};
    cur = cur[rootKey];
    for (let i = 0; i < segments.length - 1; i++) {
      if (!cur[segments[i]] || typeof cur[segments[i]] !== 'object') cur[segments[i]] = {};
      cur = cur[segments[i]];
    }
    cur[segments[segments.length - 1]] = parsed.value;
  }
  return evaluateEdgeGate(gate, newVars) === true;
}

function varsInGate(gate) {
  if (!gate || !gate.length) return [];
  const seen = new Set();
  const out = [];
  for (const frame of gate) {
    for (const v of extractVars(frame.condition || '')) {
      if (!seen.has(v)) { seen.add(v); out.push(v); }
    }
  }
  return out;
}

function buildTagsMap(passageCatalog) {
  const map = new Map();
  for (const p of (passageCatalog && passageCatalog.passages) || []) {
    map.set(p.name, p.tags || []);
  }
  return map;
}

function isNarrativeTagged(passage, tagsMap, narrativeTagSet) {
  const tags = tagsMap.get(passage) || [];
  return tags.some((t) => narrativeTagSet.has(t.toLowerCase()));
}

async function findSatisfyingSetters(gate, currentVars, call, tagsMap, narrativeTagSet) {
  const vars = varsInGate(gate);
  const candidates = [];
  for (const v of vars) {
    let res;
    try { res = await call('setters', [v]); }
    catch (e) { continue; }
    if (!res || !res.ok) continue;
    const setters = res.setters || [];
    for (const s of setters) {
      if (s.kind !== 'passage_body' && s.kind !== 'edge_setter') continue;
      if (!simulateSetterSatisfies(gate, currentVars, v, s)) continue;
      const hostPassage = s.passage || s.from || null;
      if (!hostPassage) continue;
      candidates.push({
        var: v,
        host_passage: hostPassage,
        kind: s.kind,
        value_expr: s.value_expr,
        op: s.op,
        narrative_tagged: isNarrativeTagged(hostPassage, tagsMap, narrativeTagSet),
      });
    }
  }
  return candidates;
}

async function pickBestSetter(candidates, call) {
  if (!candidates.length) return null;
  const nonNarrative = candidates.filter((c) => !c.narrative_tagged);
  if (!nonNarrative.length) return { chosen: null, reason: 'all_narrative' };
  const sample = nonNarrative.slice(0, 6);
  const scored = [];
  for (const c of sample) {
    let hops = Infinity;
    try {
      const r = await call('path', [c.host_passage], { ignore_gates: true });
      if (r && r.ok && r.found) {
        hops = typeof r.path?.length === 'number' ? r.path.length : Infinity;
      }
    } catch (e) {}
    scored.push({ ...c, hops });
  }
  const reachable = scored.filter((c) => c.hops > 0 && c.hops !== Infinity);
  if (!reachable.length) {
    if (scored.some((c) => c.hops === 0)) {
      return { chosen: null, reason: 'setter_at_current_passage' };
    }
    return { chosen: null, reason: 'all_unreachable' };
  }
  reachable.sort((a, b) => a.hops - b.hops);
  return { chosen: reachable[0], reason: null };
}

// -------- Main loop --------

async function navigate(target, ctx) {
  const { call, tagsMap, narrativeTagSet, prereqDepth, trace, seenHashes } = ctx;
  // eslint-disable-next-line no-constant-condition
  while (true) {
    if (ctx.budget.remaining <= 0) {
      trace.push({ kind: 'abort', reason: 'budget_exceeded', at: target });
      return { reached: false, abort_reason: 'budget_exceeded' };
    }
    const peek = await call('peek');
    if (!peek || !peek.ok) {
      trace.push({ kind: 'abort', reason: 'peek_failed', at: target });
      return { reached: false, abort_reason: 'peek_failed' };
    }
    const currentPassage = peek.passage;
    if (currentPassage === target) {
      trace.push({ kind: 'reached', at: target });
      return { reached: true };
    }
    const stateHash = peek.state_hash;
    const seenCount = (seenHashes.get(stateHash) || 0) + 1;
    seenHashes.set(stateHash, seenCount);
    if (seenCount >= 3) {
      trace.push({ kind: 'abort', reason: 'state_loop_detected', at: target, hash: stateHash });
      return { reached: false, abort_reason: 'state_loop_detected' };
    }

    // Plan topologically (ignore_gates=true) so we can reason about the
    // gate on the first step ourselves, with prereq resolution as a
    // proper tool rather than a hidden filter.
    const planRes = await call('path', [target], { ignore_gates: true });
    if (!planRes || !planRes.ok || !planRes.found) {
      trace.push({ kind: 'abort', reason: 'unreachable', at: target });
      return { reached: false, abort_reason: 'unreachable' };
    }
    const nextStep = (planRes.path || [])[0];
    if (!nextStep) {
      trace.push({ kind: 'reached', at: target, note: 'empty_plan_after_nontarget_peek' });
      return { reached: true };
    }
    if (!CLICKABLE_KINDS.has(nextStep.edge_kind) || !nextStep.click_text) {
      trace.push({
        kind: 'abort', reason: 'not_navigable',
        at: currentPassage, edge_kind: nextStep.edge_kind, to: nextStep.to,
      });
      return { reached: false, abort_reason: 'not_navigable' };
    }

    const liveVars = await fetchLiveVariables(call);
    const gateResult = evaluateEdgeGate(nextStep.gate, liveVars);

    if (gateResult === true || gateResult === 'unknown') {
      const clickRes = await call('click', [nextStep.click_text]);
      if (!clickRes.ok) {
        const reason = gateResult === true ? 'click_failed_true_gate' : 'unknown_gate_blocked';
        trace.push({
          kind: 'abort', reason,
          at: currentPassage, click_text: nextStep.click_text, expected_to: nextStep.to,
          click_error: clickRes.error,
        });
        return { reached: false, abort_reason: reason };
      }
      const peekAfter = await call('peek');
      const actualPassage = peekAfter && peekAfter.passage;
      if (actualPassage !== nextStep.to) {
        trace.push({
          kind: 'abort', reason: 'divergence_detected',
          at: currentPassage, click_text: nextStep.click_text,
          expected_to: nextStep.to, actual: actualPassage,
        });
        return {
          reached: false, abort_reason: 'divergence_detected',
          expected_to: nextStep.to, actual_passage: actualPassage,
        };
      }
      ctx.budget.remaining -= 1;
      trace.push({
        kind: 'click', from: currentPassage, click_text: nextStep.click_text,
        to: actualPassage, gate_result: gateResult,
      });
      continue;
    }

    // gateResult === false — prereq resolution.
    if (ctx.depth >= prereqDepth) {
      trace.push({
        kind: 'abort', reason: 'prereq_depth_exhausted',
        at: currentPassage, blocking_gate: nextStep.gate,
      });
      return {
        reached: false, abort_reason: 'prereq_depth_exhausted',
        blocking_gate: nextStep.gate,
      };
    }
    const setterCandidates = await findSatisfyingSetters(
      nextStep.gate, liveVars, call, tagsMap, narrativeTagSet
    );
    if (!setterCandidates.length) {
      trace.push({
        kind: 'abort', reason: 'prereq_no_setter',
        at: currentPassage, blocking_gate: nextStep.gate,
      });
      return {
        reached: false, abort_reason: 'prereq_no_setter',
        blocking_gate: nextStep.gate,
      };
    }
    const picked = await pickBestSetter(setterCandidates, call);
    if (!picked || !picked.chosen) {
      let reason;
      if (picked && picked.reason === 'all_narrative') reason = 'prereq_narrative_guarded';
      else if (picked && picked.reason === 'setter_at_current_passage') reason = 'prereq_setter_at_self';
      else reason = 'prereq_unreachable';
      trace.push({
        kind: 'abort', reason,
        at: currentPassage, blocking_gate: nextStep.gate,
        candidates: setterCandidates.length,
      });
      return { reached: false, abort_reason: reason, blocking_gate: nextStep.gate };
    }
    const sub = picked.chosen;
    trace.push({
      kind: 'prereq_start', at: currentPassage, blocking_gate: nextStep.gate,
      sub_target: sub.host_passage, sub_var: sub.var, sub_value: sub.value_expr,
    });
    const subResult = await navigate(sub.host_passage, { ...ctx, depth: ctx.depth + 1 });
    trace.push({
      kind: 'prereq_end', sub_target: sub.host_passage, sub_reached: subResult.reached,
      sub_abort: subResult.abort_reason || null,
    });
    if (!subResult.reached) {
      return {
        reached: false, abort_reason: 'prereq_subgoal_failed',
        sub_abort: subResult.abort_reason,
      };
    }
    if (ctx.depth + 1 > ctx.subgoalMaxDepthReached) {
      ctx.subgoalMaxDepthReached = ctx.depth + 1;
    }
    // Loop continues from fresh state.
  }
}

// High-level wrapper — most callers want to pass a target and config,
// not build the ctx object themselves.
async function pursueGoal(target, {
  call,
  tagsMap,
  narrativeTagSet,
  prereqDepth = 2,
  budget = 15,
} = {}) {
  const trace = [];
  const ctx = {
    call, tagsMap, narrativeTagSet, prereqDepth, trace,
    seenHashes: new Map(),
    depth: 0,
    budget: { remaining: budget },
    subgoalMaxDepthReached: 0,
  };
  let result;
  try {
    result = await navigate(target, ctx);
  } catch (e) {
    return {
      reached: false,
      abort_reason: 'navigate_threw',
      error: e && e.message,
      trace,
      subgoal_max_depth: 0,
    };
  }
  return {
    reached: result.reached,
    abort_reason: result.reached ? null : result.abort_reason,
    expected_to: result.expected_to || null,
    actual_passage: result.actual_passage || null,
    blocking_gate: result.blocking_gate || null,
    sub_abort: result.sub_abort || null,
    trace,
    subgoal_max_depth: ctx.subgoalMaxDepthReached,
    steps_used: budget - ctx.budget.remaining,
  };
}

module.exports = {
  navigate,
  pursueGoal,
  buildTagsMap,
  CLICKABLE_KINDS,
  // Exposed helpers for tests + introspection:
  fetchLiveVariables,
  evaluateEdgeGate,
  parseValueExpr,
  simulateSetterSatisfies,
  findSatisfyingSetters,
  pickBestSetter,
};
