// Pathfinder for the twine-game-explorer navigation intelligence layer.
//
// Given the static graph (M2) and variable setter index (M6.1), this module
// answers four questions that used to require turn-by-turn probing:
//
//   `path <to>`          — shortest click chain from current passage to `to`,
//                          with every enclosing <<if>> gate evaluated against
//                          the current variable state.
//   `requirements <to>`  — same path, plus for every blocking gate, the list
//                          of passages whose <<set>> would satisfy it (joined
//                          with reachability from the current state).
//   `reachable [N]`      — partition every passage reachable within N hops
//                          into `open` / `gated_satisfiable` / `gated_blocked`.
//   `setters <var>`      — direct lookup into variable_index.
//
// Design decisions:
//   - BFS over NAV_KINDS (wiki, link, goto, return). `include` edges are
//     transclusion, not navigation — excluded.
//   - Self-loops (from === to) skipped.
//   - Gate policies let the same BFS serve all four endpoints:
//       'strict'         : only traverse gates that evaluate TRUE
//       'allow_unknown'  : traverse TRUE + unknown (default — we don't know
//                          for sure the gate is blocking)
//       'ignore'         : traverse regardless (for requirements extraction)
//   - Adjacency built once at daemon startup; every query is O(V+E).
//
// Runtime variable sigil: the SugarCube runtime object holds `PlayerClothes`
// (no prefix); the static graph / variable_index use `$PlayerClothes`. The
// gate evaluator handles that translation — we just pass `variables` through.

'use strict';

const { evaluateGate, UNKNOWN } = require('./gate_eval');

// `button` edges are SugarCube <<button>> widgets whose label the parser
// captures as display text and whose body gotos inherit that label — they
// navigate identically to wiki links from the player's perspective.
// Include them in BFS so reachable/path/requirements work on widget-heavy
// games like road-to-success.
const NAV_KINDS = new Set(['wiki', 'link', 'goto', 'return', 'button']);

/**
 * Build a reusable context from staticGraph + variableIndex.
 * Returns null if the static graph is unusable.
 */
function buildContext(staticGraph, variableIndex) {
  if (!staticGraph || !Array.isArray(staticGraph.edges)) return null;
  const adjacency = new Map();
  const passageSet = new Set();
  for (let i = 0; i < staticGraph.edges.length; i++) {
    const e = staticGraph.edges[i];
    if (!NAV_KINDS.has(e.kind)) continue;
    if (e.from === e.to) continue;
    if (!adjacency.has(e.from)) adjacency.set(e.from, []);
    adjacency.get(e.from).push({ ...e, _idx: i });
    passageSet.add(e.from);
    passageSet.add(e.to);
  }
  return { staticGraph, variableIndex, adjacency, passageSet };
}

/**
 * Evaluate the combined gate chain on an edge. Each <<if>> level in the
 * edge's `gate` array is a nested condition that must ALL hold (AND).
 */
function evaluateEdgeGate(edge, variables) {
  if (!edge.gate || !edge.gate.length) {
    return { result: true, variables_involved: {}, conditions: [] };
  }
  const involved = {};
  const conditions = [];
  let allTrue = true;
  let anyFalse = false;
  for (const g of edge.gate) {
    const r = evaluateGate(g.condition, variables);
    conditions.push({ condition: g.condition, branch: g.branch, result: r.result });
    Object.assign(involved, r.variables_involved);
    if (r.result === false) anyFalse = true;
    else if (r.result !== true) allTrue = false;
  }
  if (anyFalse) return { result: false, variables_involved: involved, conditions };
  if (allTrue) return { result: true, variables_involved: involved, conditions };
  return { result: 'unknown', variables_involved: involved, conditions };
}

function gatePermits(result, policy) {
  if (policy === 'ignore') return true;
  if (result === true) return true;
  if (result === false) return false;
  // unknown
  return policy === 'allow_unknown';
}

function stepFromEdge(edge, gateEval) {
  return {
    from: edge.from,
    to: edge.to,
    click_text: edge.display || null,
    edge_kind: edge.kind,
    gate: edge.gate && edge.gate.length ? edge.gate : null,
    gate_result: gateEval.result,
    gate_conditions: gateEval.conditions.length ? gateEval.conditions : null,
    setter: edge.setter || null,
    edge_index: edge._idx,
  };
}

/**
 * BFS from `from` to `to`. Returns the path array (empty if from===to) or
 * null if no path found within maxHops.
 *
 * Ties are broken by the first edge encountered (insertion order of static
 * graph), which keeps results deterministic across runs.
 */
function bfsPath(ctx, { from, to, variables, maxHops = 20, gatePolicy = 'allow_unknown' }) {
  if (!ctx || !ctx.adjacency) return null;
  if (!ctx.passageSet.has(from) && from !== to) return null;
  if (!ctx.passageSet.has(to) && from !== to) return null;
  if (from === to) return [];
  const visited = new Set([from]);
  const queue = [{ passage: from, path: [] }];
  while (queue.length > 0) {
    const { passage, path } = queue.shift();
    if (path.length >= maxHops) continue;
    const edges = ctx.adjacency.get(passage) || [];
    for (const e of edges) {
      if (visited.has(e.to)) continue;
      const g = evaluateEdgeGate(e, variables);
      if (!gatePermits(g.result, gatePolicy)) continue;
      const step = stepFromEdge(e, g);
      const newPath = path.concat([step]);
      if (e.to === to) return newPath;
      visited.add(e.to);
      queue.push({ passage: e.to, path: newPath });
    }
  }
  return null;
}

/**
 * All-reachable partition from `from`, respecting gates in the chosen policy.
 * Traverses through TRUE gates only (so `gated_*` entries are terminal — we
 * don't pretend to know what lies past a gate we haven't satisfied).
 */
function reachableFrom(ctx, { from, variables, maxHops = 5 }) {
  const open = [];
  const gatedSatisfiable = [];
  const gatedBlocked = [];
  if (!ctx || !ctx.adjacency) {
    return { from, max_hops: maxHops, open, gated_satisfiable: gatedSatisfiable, gated_blocked: gatedBlocked };
  }
  const visitedMinHops = new Map();   // passage -> hops
  const queue = [{ passage: from, hops: 0 }];
  visitedMinHops.set(from, 0);
  while (queue.length > 0) {
    const { passage, hops } = queue.shift();
    if (hops >= maxHops) continue;
    const edges = ctx.adjacency.get(passage) || [];
    for (const e of edges) {
      const g = evaluateEdgeGate(e, variables);
      const base = {
        passage: e.to,
        hops: hops + 1,
        via: e.display || null,
        from_passage: passage,
        edge_kind: e.kind,
      };
      if (g.result === true) {
        if (!visitedMinHops.has(e.to) || visitedMinHops.get(e.to) > hops + 1) {
          visitedMinHops.set(e.to, hops + 1);
          open.push(base);
          queue.push({ passage: e.to, hops: hops + 1 });
        }
      } else if (g.result === false) {
        gatedBlocked.push({
          ...base,
          blocking_gate: (e.gate[0] && e.gate[0].condition) || null,
          variables_involved: g.variables_involved,
        });
      } else {
        gatedSatisfiable.push({
          ...base,
          gate_condition: (e.gate[0] && e.gate[0].condition) || null,
          variables_involved: g.variables_involved,
        });
      }
    }
  }
  return {
    from,
    max_hops: maxHops,
    open_count: open.length,
    gated_satisfiable_count: gatedSatisfiable.length,
    gated_blocked_count: gatedBlocked.length,
    open,
    gated_satisfiable: gatedSatisfiable,
    gated_blocked: gatedBlocked,
  };
}

/**
 * Requirements — for every blocking gate on the ignore-gates path to `to`,
 * extract variables and look up setter candidates in variable_index.
 */
function computeRequirements(ctx, { from, to, variables }) {
  if (!ctx) return { ok: false, error: 'pathfinder context unavailable' };
  if (from === to) {
    return {
      target: to, from, currently_reachable: true,
      path: [], blocking_gates: [],
      summary: 'Already at target.',
    };
  }

  // First try strict path — if all gates pass, we're good.
  let path = bfsPath(ctx, { from, to, variables, gatePolicy: 'strict' });
  if (path) {
    return {
      target: to, from, currently_reachable: true,
      path,
      blocking_gates: [],
      summary: `Already reachable in ${path.length} click${path.length === 1 ? '' : 's'}: ${pathSummary(path)}`,
    };
  }

  // Fall back to ignore-gates to see whether any path exists at all.
  path = bfsPath(ctx, { from, to, variables, gatePolicy: 'ignore' });
  if (!path) {
    return {
      target: to, from, currently_reachable: false,
      path: null, blocking_gates: [],
      summary: `No path exists from ${from} to ${to} in the static graph.`,
    };
  }

  // For each step whose gate evaluated false/unknown, extract requirements.
  const blockingGates = [];
  for (let i = 0; i < path.length; i++) {
    const step = path[i];
    if (step.gate_result === true) continue;
    const variablesBreakdown = {};
    const conds = step.gate_conditions || [];
    const condStr = conds.map((c) => c.condition).join(' && ');
    // Union of every variable mentioned across nested gate levels.
    const allInvolved = {};
    for (const c of conds) {
      const r = evaluateGate(c.condition, variables);
      Object.assign(allInvolved, r.variables_involved);
    }
    for (const [varName, currentVal] of Object.entries(allInvolved)) {
      // Extract values the gate wants this variable to hold (from `==` / `eq`
      // comparisons). Used to rank setters so the most-relevant ones surface
      // first in the summary.
      const desiredValues = extractDesiredValues(condStr, varName);
      variablesBreakdown[varName] = {
        current_value: currentVal,
        desired_values: desiredValues,
        setters: findSettersForVar(ctx, varName, { from, variables, desiredValues }),
      };
    }
    blockingGates.push({
      step: i + 1,
      edge: { from: step.from, to: step.to, click_text: step.click_text, edge_kind: step.edge_kind },
      condition: condStr,
      gate_result: step.gate_result,
      variables: variablesBreakdown,
    });
  }

  return {
    target: to, from,
    currently_reachable: false,
    path,
    blocking_gates: blockingGates,
    summary: formatRequirementsSummary(to, blockingGates, path),
  };
}

/**
 * Extract the set of "target values" the gate condition wants a variable to
 * have. Handles the common `<var> (==|===|eq) <literal>` pattern. Returns
 * an array of raw literal strings (as they appear in source — quoted strings
 * keep their quotes, numbers stay unquoted) so they can be string-compared
 * against variable_index setters' `value_expr`, which is also the raw source.
 *
 * When the gate is too complex (method calls, arithmetic, etc.) we return
 * an empty array — the caller falls back to surfacing all setters unranked.
 */
function extractDesiredValues(conditionStr, varName) {
  if (!conditionStr || !varName) return [];
  const escaped = varName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // varName OP literal
  const re = new RegExp(
    `${escaped}\\s*(?:===|==|\\beq\\b|\\bis\\b)\\s*("(?:[^"\\\\]|\\\\.)*"|'(?:[^'\\\\]|\\\\.)*'|true|false|null|-?\\d+(?:\\.\\d+)?)`,
    'g',
  );
  // literal OP varName (reverse form)
  const reRev = new RegExp(
    `("(?:[^"\\\\]|\\\\.)*"|'(?:[^'\\\\]|\\\\.)*'|true|false|null|-?\\d+(?:\\.\\d+)?)\\s*(?:===|==|\\beq\\b|\\bis\\b)\\s*${escaped}`,
    'g',
  );
  const seen = new Set();
  const out = [];
  for (const p of [re, reRev]) {
    let m;
    p.lastIndex = 0;
    while ((m = p.exec(conditionStr)) !== null) {
      if (!seen.has(m[1])) { seen.add(m[1]); out.push(m[1]); }
    }
  }
  return out;
}

/**
 * For a given variable name, return candidate setter passages + reachability.
 * Only includes passage_body setters (edge_setters fire as a side effect of
 * edge traversal, which is already captured in the path itself).
 *
 * If `desiredValues` is provided (from gate analysis), setters whose
 * `value_expr` matches any desired value are flagged and sorted first.
 */
function findSettersForVar(ctx, varName, { from, variables, desiredValues = [] }) {
  if (!ctx.variableIndex || !ctx.variableIndex.variables) return [];
  const v = ctx.variableIndex.variables[varName];
  if (!v || !Array.isArray(v.setters)) return [];
  const out = [];
  const seen = new Set();
  for (const s of v.setters) {
    if (s.kind !== 'passage_body') continue;
    if (s.complex) continue;
    const key = `${s.passage}|${s.op}|${s.value_expr}`;
    if (seen.has(key)) continue;
    seen.add(key);
    let pathToSetter = null;
    let reachableNow = false;
    if (s.passage === from) {
      pathToSetter = [];
      reachableNow = true;
    } else {
      pathToSetter = bfsPath(ctx, { from, to: s.passage, variables, gatePolicy: 'strict' });
      reachableNow = pathToSetter !== null;
    }
    const matchesDesired = desiredValues.length > 0 && desiredValues.includes(s.value_expr);
    out.push({
      passage: s.passage,
      op: s.op,
      value_expr: s.value_expr,
      gate: s.gate || [],
      reachable_now: reachableNow,
      hops: pathToSetter ? pathToSetter.length : null,
      path_to_setter: pathToSetter,
      matches_gate_target: matchesDesired,
    });
  }
  // Sort priority: gate-target matches first, then reachable, then by hops,
  // then alphabetical on value_expr (stable tiebreaker).
  out.sort((a, b) => {
    if (a.matches_gate_target !== b.matches_gate_target) return a.matches_gate_target ? -1 : 1;
    if (a.reachable_now !== b.reachable_now) return a.reachable_now ? -1 : 1;
    const ah = a.hops == null ? Infinity : a.hops;
    const bh = b.hops == null ? Infinity : b.hops;
    if (ah !== bh) return ah - bh;
    return String(a.value_expr).localeCompare(String(b.value_expr));
  });
  return out;
}

/**
 * Direct lookup — return the variable's setters + unsetters + initial_value
 * from the index. No reachability computation (that's what `requirements`
 * is for). Cheap.
 */
function lookupSetters(ctx, varName) {
  if (!ctx.variableIndex || !ctx.variableIndex.variables) {
    return { variable: varName, ok: false, error: 'variable_index unavailable' };
  }
  const v = ctx.variableIndex.variables[varName];
  if (!v) {
    return {
      variable: varName, ok: true, found: false,
      note: 'variable not present in index — check spelling (must include $ or _ prefix)',
    };
  }
  return {
    variable: varName, ok: true, found: true,
    initial_value: v.initial_value,
    setters: v.setters || [],
    unsetters: v.unsetters || [],
  };
}

// ---------------------------------------------------------------------------
// Summary-string formatters — designed to be read directly by Claude.
// ---------------------------------------------------------------------------

function pathSummary(path) {
  if (!path || !path.length) return '(already there)';
  return path.map((s) => s.click_text || `${s.edge_kind}→${s.to}`).join(' → ');
}

function formatPathSummary(from, to, path, blocking) {
  if (!path) return `No path from ${from} to ${to} within hop budget.`;
  const head = `${path.length} step${path.length === 1 ? '' : 's'}: ${pathSummary(path)}`;
  if (!blocking || !blocking.length) return `${head}. All gates satisfied.`;
  const first = blocking[0];
  const firstVar = Object.keys(first.variables_involved || {})[0];
  const firstVal = firstVar ? first.variables_involved[firstVar] : null;
  return `${head}. BLOCKED at step ${first.step} by \`${first.condition}\`` +
    (firstVar ? ` (currently ${firstVar} = ${JSON.stringify(firstVal)})` : '') +
    `. Use \`requirements ${to}\` to see how to satisfy.`;
}

function formatRequirementsSummary(to, blockingGates, path) {
  if (!blockingGates.length) return `${to} is reachable — no blocking gates.`;
  const lines = [];
  lines.push(`${to} is NOT currently reachable. Path length ${path.length}, ${blockingGates.length} blocking gate${blockingGates.length === 1 ? '' : 's'}:`);
  for (const bg of blockingGates) {
    lines.push(`  step ${bg.step} (${bg.edge.from} → ${bg.edge.to}): ${bg.condition}`);
    for (const [varName, info] of Object.entries(bg.variables)) {
      const cur = info.current_value && info.current_value.__unknown ? 'unknown' : JSON.stringify(info.current_value);
      const wantClause = info.desired_values && info.desired_values.length
        ? `, wants ${info.desired_values.join(' or ')}` : '';
      // Pick the best setter: (a) matches gate target AND reachable, else
      // (b) any reachable, else (c) any setter.
      const bestMatch = info.setters.find((s) => s.matches_gate_target && s.reachable_now);
      const anyReachable = info.setters.find((s) => s.reachable_now);
      const pick = bestMatch || anyReachable;
      if (pick) {
        const tag = pick.matches_gate_target ? '✓ matches gate' : 'reachable';
        lines.push(`    ${varName} (currently ${cur}${wantClause}) — setter: ${pick.passage} (${pick.op} ${pick.value_expr}) [${tag}, ${pick.hops} click${pick.hops === 1 ? '' : 's'}].`);
      } else if (info.setters.length) {
        lines.push(`    ${varName} (currently ${cur}${wantClause}) — ${info.setters.length} setter(s) found but none currently reachable.`);
      } else {
        lines.push(`    ${varName} (currently ${cur}${wantClause}) — no <<set>> found in the index. May be JS-driven or set via widget.`);
      }
    }
  }
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// High-level wrappers used by the live.js handlers.
// ---------------------------------------------------------------------------

function findPath(ctx, { from, to, variables, maxHops = 20, ignoreGates = false }) {
  if (!ctx) return { ok: false, error: 'pathfinder context unavailable' };
  if (!from) return { ok: false, error: 'no current passage known' };
  if (!to) return { ok: false, error: 'missing target passage argument' };
  if (from !== to && !ctx.passageSet.has(to)) {
    return { ok: false, error: `target passage "${to}" not in static graph` };
  }
  const gatePolicy = ignoreGates ? 'ignore' : 'allow_unknown';
  const path = bfsPath(ctx, { from, to, variables, maxHops, gatePolicy });
  if (!path) {
    // Differentiate "gate blocked" from "no edge at all": if ignore-gates
    // finds a path, the issue is blocking conditions, not connectivity.
    let hint = null;
    if (!ignoreGates) {
      const alt = bfsPath(ctx, { from, to, variables, maxHops, gatePolicy: 'ignore' });
      if (alt) {
        hint = `blocked by gates. Use \`requirements ${to}\` to see what's needed, or \`path ${to} --ignore-gates\` to see the gated path.`;
      } else {
        hint = `no edge chain from ${from} to ${to} in the static graph (within ${maxHops} hops).`;
      }
    }
    return {
      ok: true, found: false, from, to, length: 0, path: null,
      reason: hint || `no path within ${maxHops} hops (gate policy: ${gatePolicy})`,
      summary: hint
        ? `No path from ${from} to ${to} — ${hint}`
        : `No path from ${from} to ${to} within ${maxHops} hops (gate policy: ${gatePolicy}).`,
    };
  }
  const blockingGates = [];
  for (let i = 0; i < path.length; i++) {
    const step = path[i];
    if (step.gate_result === true) continue;
    const involved = {};
    for (const c of step.gate_conditions || []) {
      const r = evaluateGate(c.condition, variables);
      Object.assign(involved, r.variables_involved);
    }
    blockingGates.push({
      step: i + 1,
      condition: (step.gate_conditions || []).map((c) => c.condition).join(' && '),
      gate_result: step.gate_result,
      variables_involved: involved,
    });
  }
  return {
    ok: true,
    found: true,
    from, to,
    length: path.length,
    path,
    all_gates_satisfied: blockingGates.length === 0,
    blocking_gates: blockingGates,
    summary: formatPathSummary(from, to, path, blockingGates),
  };
}

module.exports = {
  buildContext,
  bfsPath,
  reachableFrom,
  computeRequirements,
  findSettersForVar,
  lookupSetters,
  findPath,
  evaluateEdgeGate,
  pathSummary,
  NAV_KINDS,
};
