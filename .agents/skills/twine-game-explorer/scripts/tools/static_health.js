#!/usr/bin/env node
// Static health check for a game's Tier 1 artifacts.
//
// Reads static_graph.json, variable_index.json, passage_catalog.json,
// initial_state.json from game_explorations/<slug>/ and reports metrics
// that gate whether Tier 2 (autopilot) is worth building:
//
//   1. Ambiguous click-text rate — edges whose display text also appears
//      on edges from other source passages. High rate = click text is
//      not a reliable selector at runtime.
//   2. Dynamic-goto coverage gap — passages whose source contains
//      <<goto $var>> / <<goto _var>>. Static graph can't know where
//      these land.
//   3. Gate-eval unknown rate on initial state — gates that evaluateGate
//      can't resolve against fresh game variables. High rate = gate
//      evaluator is blind to much of the graph.
//   4. Complex-setter density — fraction of setters the variable-index
//      parser couldn't decode. Surfaces from variable_index.json.
//   5. indexing_coverage — "full" vs "partial".
//
// Pure read-only, no daemon, no browser. Output:
//   game_explorations/<slug>/static_health.json
//   game_explorations/<slug>/static_health.md
//
// Pass bar (per plan):
//   ambiguous_click_rate    <= 0.20
//   dynamic_goto_rate       <= 0.10
//   gate_unknown_rate       <= 0.30
//   complex_setter_density  <  0.05

'use strict';

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');
const { evaluateGate } = require(path.join(SKILL_DIR, 'scripts/lib/gate_eval'));

// Matches <<goto $var>> / <<goto _var>> / <<goto $obj.prop>> with optional
// whitespace. Does NOT match <<goto "literal">> (that IS in the static graph).
const DYNAMIC_GOTO_RE = /<<goto\s+[$_][A-Za-z_][A-Za-z0-9_]*/;

function parseArgs(argv) {
  const out = { slug: null, gamesRoot: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--slug') out.slug = argv[++i];
    else if (a === '--games-root') out.gamesRoot = argv[++i];
    else if (a === '--help' || a === '-h') {
      console.log('Usage: static_health.js --slug <slug> [--games-root <dir>]');
      process.exit(0);
    }
  }
  if (!out.slug) {
    console.error('ERROR: --slug is required');
    process.exit(1);
  }
  return out;
}

function loadJson(p) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); }
  catch (e) { return { __loadError: e.message, __path: p }; }
}

function evaluateEdgeGate(edge, variables) {
  // Reuses the same stack-as-conjunction logic as analyzeGateEval but
  // returns a single true/false/'unknown' for the whole edge.
  const gate = edge.gate || [];
  if (gate.length === 0) return true;
  let combined = true;
  for (const frame of gate) {
    // Parser stores the final post-negation condition already; `branch`
    // is informational. Do NOT re-negate on `branch === 'else'`.
    const cond = frame.condition || '';
    const r = evaluateGate(cond, variables);
    if (r.result === false) return false;
    if (r.result === 'unknown') combined = 'unknown';
  }
  return combined;
}

function analyzeAmbiguousClicks(staticGraph, initialState) {
  const edges = staticGraph.edges || [];
  const variables = (initialState && initialState.variables) || {};

  // Runtime ambiguity: within a single source passage, are there ≥2
  // outgoing edges sharing a click text whose gates could simultaneously
  // fire? The static parser emits one edge per <<if>>/<<elseif>> branch,
  // so raw duplicate count overcounts — gates within an elseif chain are
  // mutually exclusive.
  //
  // We bucket by (source, text), evaluate each edge's gate against the
  // initial state, then classify the bucket:
  //   - DEFINITE: ≥2 edges evaluate to `true` simultaneously → autopilot
  //     cannot disambiguate from the static graph alone.
  //   - POTENTIAL: exactly 1 true + ≥1 unknown, or ≥2 unknown → may or
  //     may not fire concurrently at runtime; depends on runtime state
  //     we can't compute. Counted separately.
  //   - SAFE: ≤1 edge evaluates to true/unknown → disambiguated by gates.
  const groups = new Map(); // `${from}\x00${text}` -> edges[]
  let totalEdgesWithText = 0;
  for (const e of edges) {
    const text = (e.display || '').trim();
    if (!text) continue;
    totalEdgesWithText++;
    const key = e.from + '\x00' + text;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(e);
  }

  let definiteAmbiguousEdges = 0;
  let potentialAmbiguousEdges = 0;
  const definiteTop = [];
  const potentialTop = [];
  let rawDuplicateBuckets = 0;

  for (const [key, groupEdges] of groups.entries()) {
    if (groupEdges.length < 2) continue;
    rawDuplicateBuckets++;
    const [from, text] = key.split('\x00');
    // Partition edges by gate-eval result. Only count as ambiguous if the
    // firing set spans ≥2 DISTINCT targets — two edges sharing (source,
    // text, target) are safe for autopilot because it doesn't matter
    // which DOM element gets clicked; they all land at the same place.
    const firingTrue = new Set();     // targets of true-gated edges
    const firingUnknown = new Set();  // targets of unknown-gated edges
    let trues = 0; let unknowns = 0; let falses = 0;
    for (const e of groupEdges) {
      const r = evaluateEdgeGate(e, variables);
      if (r === true) { trues++; firingTrue.add(e.to); }
      else if (r === false) { falses++; }
      else { unknowns++; firingUnknown.add(e.to); }
    }
    const definiteTargets = firingTrue.size;
    const potentialTargets = new Set(
      [...firingTrue, ...firingUnknown]
    ).size;
    if (definiteTargets >= 2) {
      definiteAmbiguousEdges += groupEdges.length;
      definiteTop.push({
        from, text,
        edge_count: groupEdges.length,
        distinct_firing_targets: definiteTargets,
        gate_true: trues, gate_unknown: unknowns, gate_false: falses,
      });
    } else if (potentialTargets >= 2) {
      potentialAmbiguousEdges += groupEdges.length;
      potentialTop.push({
        from, text,
        edge_count: groupEdges.length,
        distinct_potential_targets: potentialTargets,
        gate_true: trues, gate_unknown: unknowns, gate_false: falses,
      });
    }
  }
  definiteTop.sort((a, b) => b.edge_count - a.edge_count);
  potentialTop.sort((a, b) => b.edge_count - a.edge_count);

  return {
    total_edges_with_text: totalEdgesWithText,
    raw_duplicate_buckets: rawDuplicateBuckets,
    definite_ambiguous_edges: definiteAmbiguousEdges,
    definite_ambiguous_rate: totalEdgesWithText === 0
      ? 0
      : definiteAmbiguousEdges / totalEdgesWithText,
    potential_ambiguous_edges: potentialAmbiguousEdges,
    potential_ambiguous_rate: totalEdgesWithText === 0
      ? 0
      : potentialAmbiguousEdges / totalEdgesWithText,
    top_definite: definiteTop.slice(0, 10),
    top_potential: potentialTop.slice(0, 10),
  };
}

function analyzeDynamicGoto(passageCatalog) {
  const passages = passageCatalog.passages || [];
  let withDynamicGoto = 0;
  const samples = [];
  for (const p of passages) {
    const src = p.source_raw || '';
    if (DYNAMIC_GOTO_RE.test(src)) {
      withDynamicGoto++;
      if (samples.length < 10) {
        const m = src.match(/<<goto\s+[$_][^>]*>>/);
        samples.push({ passage: p.name, sample: m ? m[0] : null });
      }
    }
  }
  return {
    passages_with_dynamic_goto: withDynamicGoto,
    total_passages: passages.length,
    dynamic_goto_rate: passages.length === 0
      ? 0
      : withDynamicGoto / passages.length,
    samples,
  };
}

function analyzeGateEval(staticGraph, initialState) {
  // initial_state.json keys are stored WITHOUT the sigil (matches how
  // SugarCube's runtime object is keyed). gate_eval.resolveVar strips the
  // sigil before lookup, so we pass vars as-is.
  const variables = (initialState && initialState.variables) || {};
  const edges = staticGraph.edges || [];

  let gatedEdges = 0;
  let trueCount = 0;
  let falseCount = 0;
  // Split unknowns by variable class — temp-only unknowns resolve at
  // runtime (temp vars exist for the duration of a single render and are
  // absent from initial_state), so they shouldn't count against Tier 2
  // viability. Story-var unknowns are real evaluator gaps.
  let unknownTempOnly = 0;
  let unknownStoryOnly = 0;
  let unknownMixed = 0;
  const unknownStorySamples = [];

  for (const e of edges) {
    const gate = e.gate || [];
    if (gate.length === 0) continue;
    gatedEdges++;
    let combined = true;
    const conditions = [];
    for (const frame of gate) {
      // Parser already pre-negated `<<else>>` conditions; just use the
      // stored value. (Earlier revisions of this file double-negated
      // and caused false-negative gate evaluations.)
      const cond = frame.condition || '';
      conditions.push(cond);
      // Note: `elseif` frames carry the elseif's own condition, not the
      // cumulative negation of prior `if`s. Treating each frame standalone
      // is conservative — we may report some edges as `true` that are in
      // practice `false` because a prior if already matched. That
      // conservatism inflates clean-path expectations, not divergences,
      // so it's safe for this health check.
      const r = evaluateGate(cond, variables);
      if (r.result === false) { combined = false; break; }
      if (r.result === 'unknown') combined = 'unknown';
    }
    if (combined === true) trueCount++;
    else if (combined === false) falseCount++;
    else {
      const joined = conditions.join(' && ');
      const hasTemp = /_[A-Za-z]/.test(joined);
      const hasStory = /\$[A-Za-z]/.test(joined);
      if (hasTemp && !hasStory) unknownTempOnly++;
      else if (hasStory && !hasTemp) {
        unknownStoryOnly++;
        if (unknownStorySamples.length < 10) {
          unknownStorySamples.push({
            from: e.from, to: e.to, display: e.display, gate: e.gate,
          });
        }
      } else if (hasTemp && hasStory) unknownMixed++;
      else unknownMixed++; // gates referencing neither (shouldn't happen)
    }
  }
  const unknownCount = unknownTempOnly + unknownStoryOnly + unknownMixed;
  // Effective unknown rate treats temp-only as resolved-at-runtime.
  const effectiveUnknown = unknownStoryOnly + unknownMixed;

  return {
    gated_edges: gatedEdges,
    gate_true: trueCount,
    gate_false: falseCount,
    gate_unknown: unknownCount,
    gate_unknown_rate: gatedEdges === 0 ? 0 : unknownCount / gatedEdges,
    // Breakdown and the more meaningful "effective" rate:
    unknown_temp_only: unknownTempOnly,
    unknown_story_only: unknownStoryOnly,
    unknown_mixed: unknownMixed,
    effective_unknown: effectiveUnknown,
    effective_unknown_rate: gatedEdges === 0 ? 0 : effectiveUnknown / gatedEdges,
    unknown_story_samples: unknownStorySamples,
  };
}

function analyzeComplexSetters(variableIndex) {
  const totalVars = variableIndex.total_variables || 0;
  const complex = variableIndex.complex_setter_count || 0;
  const parseErrors = variableIndex.parse_errors || 0;
  const skippedScript = variableIndex.skipped_script_blocks || 0;
  const skippedWidget = variableIndex.skipped_widget_passages || 0;

  // Total setters across all variables (from the parsed side, excluding
  // complex_setters which is its own bucket).
  let parsedSetters = 0;
  for (const v of Object.values(variableIndex.variables || {})) {
    parsedSetters += (v.setters || []).length + (v.unsetters || []).length;
  }
  const totalSetters = parsedSetters + complex;
  return {
    total_variables: totalVars,
    parsed_setters: parsedSetters,
    complex_setter_count: complex,
    parse_errors: parseErrors,
    skipped_script_blocks: skippedScript,
    skipped_widget_passages: skippedWidget,
    complex_setter_density: totalSetters === 0
      ? 0
      : complex / totalSetters,
    indexing_coverage: variableIndex.indexing_coverage || 'unknown',
  };
}

function applyPassBar(report) {
  const checks = [
    {
      name: 'definite_ambiguous_rate',
      value: report.ambiguous_clicks.definite_ambiguous_rate,
      bar: 0.05,
      cmp: 'lte',
    },
    {
      name: 'potential_ambiguous_rate',
      value: report.ambiguous_clicks.potential_ambiguous_rate,
      bar: 0.20,
      cmp: 'lte',
    },
    {
      name: 'dynamic_goto_rate',
      value: report.dynamic_goto.dynamic_goto_rate,
      bar: 0.10,
      cmp: 'lte',
    },
    {
      name: 'effective_gate_unknown_rate',
      value: report.gate_eval.effective_unknown_rate,
      bar: 0.30,
      cmp: 'lte',
    },
    {
      name: 'complex_setter_density',
      value: report.complex_setters.complex_setter_density,
      bar: 0.05,
      cmp: 'lt',
    },
  ];
  const results = checks.map((c) => {
    const pass = c.cmp === 'lte' ? c.value <= c.bar : c.value < c.bar;
    return { ...c, pass };
  });
  const overall = results.every((r) => r.pass);
  return { checks: results, overall_pass: overall };
}

function renderMarkdown(slug, report, passBar) {
  const pct = (n) => (n * 100).toFixed(1) + '%';
  const badge = (pass) => (pass ? '✅' : '❌');
  const lines = [];
  lines.push(`# Static health — ${slug}`);
  lines.push('');
  lines.push(`Generated: ${report.generated_at}`);
  lines.push('');
  lines.push(`## Verdict: ${passBar.overall_pass ? '✅ PASS' : '❌ FAIL'}`);
  lines.push('');
  lines.push('| Metric | Value | Bar | Result |');
  lines.push('|---|---|---|---|');
  for (const c of passBar.checks) {
    const op = c.cmp === 'lte' ? '≤' : '<';
    lines.push(`| ${c.name} | ${pct(c.value)} | ${op} ${pct(c.bar)} | ${badge(c.pass)} |`);
  }
  lines.push('');

  lines.push('## 1. Click-text ambiguity');
  lines.push('');
  const ac = report.ambiguous_clicks;
  lines.push(`Edges bucketed by (source_passage, click_text). Raw duplicate buckets (≥2 edges sharing the key): **${ac.raw_duplicate_buckets}**. Most of these are expanded \`<<if>>/<<elseif>>\` chains where only one gate fires at a time — not a real runtime ambiguity.`);
  lines.push('');
  lines.push(`**Definite ambiguous** (≥2 edges in the bucket evaluate to \`true\` on initial state — autopilot *cannot* disambiguate):`);
  lines.push(`- ${ac.definite_ambiguous_edges} / ${ac.total_edges_with_text} edges (${pct(ac.definite_ambiguous_rate)})`);
  if (ac.top_definite.length) {
    lines.push('');
    lines.push('**Top offenders:**');
    for (const t of ac.top_definite) {
      lines.push(`- \`${t.from}\` → "${t.text}" × ${t.edge_count} (gates: ${t.gate_true} true, ${t.gate_unknown} unknown, ${t.gate_false} false)`);
    }
  }
  lines.push('');
  lines.push(`**Potential ambiguous** (bucket has ≥2 edges with gates that could fire concurrently at runtime — typically due to temp vars / runtime-computed state the evaluator flags as \`unknown\`):`);
  lines.push(`- ${ac.potential_ambiguous_edges} / ${ac.total_edges_with_text} edges (${pct(ac.potential_ambiguous_rate)})`);
  if (ac.top_potential.length) {
    lines.push('');
    lines.push('**Top offenders:**');
    for (const t of ac.top_potential.slice(0, 10)) {
      lines.push(`- \`${t.from}\` → "${t.text}" × ${t.edge_count} (gates: ${t.gate_true} true, ${t.gate_unknown} unknown, ${t.gate_false} false)`);
    }
  }
  lines.push('');

  lines.push('## 2. Dynamic-goto coverage gap');
  lines.push('');
  const dg = report.dynamic_goto;
  lines.push(`- ${dg.passages_with_dynamic_goto} / ${dg.total_passages} passages contain \`<<goto $var>>\` or similar (${pct(dg.dynamic_goto_rate)})`);
  if (dg.samples.length) {
    lines.push('');
    lines.push('**Sample passages:**');
    for (const s of dg.samples) {
      lines.push(`- \`${s.passage}\` → \`${s.sample}\``);
    }
  }
  lines.push('');

  lines.push('## 3. Gate-eval on initial state');
  lines.push('');
  const ge = report.gate_eval;
  lines.push(`- ${ge.gated_edges} edges have non-empty gate stack`);
  lines.push(`- true: ${ge.gate_true} | false: ${ge.gate_false} | unknown: ${ge.gate_unknown}`);
  lines.push(`- raw unknown rate: ${pct(ge.gate_unknown_rate)}`);
  lines.push('');
  lines.push('**Unknown breakdown by gate variable class:**');
  lines.push(`- temp-var-only (\`_var\` — resolves at runtime): ${ge.unknown_temp_only}`);
  lines.push(`- story-var-only (\`$var\` — real evaluator gap): ${ge.unknown_story_only}`);
  lines.push(`- mixed: ${ge.unknown_mixed}`);
  lines.push('');
  lines.push(`**Effective unknown rate** (temp-only gates excluded since they resolve at runtime when the current passage is being rendered): ${pct(ge.effective_unknown_rate)}`);
  lines.push('');
  if (ge.unknown_story_samples.length) {
    lines.push('**Sample story-var unknown gates** (these are the real evaluator gaps — autopilot will see `unknown` here even at runtime):');
    for (const s of ge.unknown_story_samples) {
      const condStr = (s.gate || []).map((f) => `[${f.branch}] ${f.condition}`).join(' ∧ ');
      lines.push(`- \`${s.from}\` → \`${s.to}\` (click: "${s.display}") — ${condStr}`);
    }
  }
  lines.push('');

  lines.push('## 4. Complex setters');
  lines.push('');
  const cs = report.complex_setters;
  lines.push(`- total variables: ${cs.total_variables}`);
  lines.push(`- parsed setters: ${cs.parsed_setters}`);
  lines.push(`- complex (unparseable) setters: ${cs.complex_setter_count}`);
  lines.push(`- parse errors: ${cs.parse_errors}`);
  lines.push(`- skipped script blocks: ${cs.skipped_script_blocks}`);
  lines.push(`- skipped widget passages: ${cs.skipped_widget_passages}`);
  lines.push(`- complex setter density: ${pct(cs.complex_setter_density)}`);
  lines.push(`- indexing coverage: \`${cs.indexing_coverage}\``);
  lines.push('');

  return lines.join('\n');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const gamesRoot = args.gamesRoot
    ? path.resolve(args.gamesRoot)
    : path.resolve(process.cwd(), 'game_explorations');
  const slugDir = path.join(gamesRoot, args.slug);

  if (!fs.existsSync(slugDir)) {
    console.error(`ERROR: slug directory not found: ${slugDir}`);
    process.exit(1);
  }

  const staticGraph = loadJson(path.join(slugDir, 'static_graph.json'));
  const variableIndex = loadJson(path.join(slugDir, 'variable_index.json'));
  const passageCatalog = loadJson(path.join(slugDir, 'passage_catalog.json'));
  const initialState = loadJson(path.join(slugDir, 'initial_state.json'));

  for (const [name, obj] of [
    ['static_graph.json', staticGraph],
    ['variable_index.json', variableIndex],
    ['passage_catalog.json', passageCatalog],
    ['initial_state.json', initialState],
  ]) {
    if (obj.__loadError) {
      console.error(`ERROR: ${name} — ${obj.__loadError}`);
      process.exit(1);
    }
  }

  const report = {
    generated_at: new Date().toISOString(),
    slug: args.slug,
    ambiguous_clicks: analyzeAmbiguousClicks(staticGraph, initialState),
    dynamic_goto: analyzeDynamicGoto(passageCatalog),
    gate_eval: analyzeGateEval(staticGraph, initialState),
    complex_setters: analyzeComplexSetters(variableIndex),
  };
  const passBar = applyPassBar(report);
  report.pass_bar = passBar;

  fs.writeFileSync(
    path.join(slugDir, 'static_health.json'),
    JSON.stringify(report, null, 2),
  );
  fs.writeFileSync(
    path.join(slugDir, 'static_health.md'),
    renderMarkdown(args.slug, report, passBar),
  );

  console.log(`Static health report written to ${slugDir}/static_health.{json,md}`);
  console.log('');
  console.log(`Verdict: ${passBar.overall_pass ? 'PASS' : 'FAIL'}`);
  for (const c of passBar.checks) {
    const pct = (c.value * 100).toFixed(1);
    const op = c.cmp === 'lte' ? '<=' : '<';
    console.log(`  ${c.pass ? 'OK ' : 'XX '} ${c.name}: ${pct}%  (bar: ${op} ${(c.bar * 100).toFixed(0)}%)`);
  }
}

main();
