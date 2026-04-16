// Report generator.
//
// Phase 3+4 split:
//   - Detector produces a pure statistical profile (no labels)
//   - Labeler applies semantic labels with confidence
//   - This file renders both into human-readable artifacts
//
// Outputs:
//   report.md             top-level human-readable synthesis
//   mechanics.md          design patterns observed
//   coverage.md           exploration coverage summary
//   variable_profile.json raw statistical evidence (phase 3 output)
//   variable_schema.json  labeled view of variables (back-compat with older runs)
//   npcs.json             per-NPC stats and vars
//   items.json            detected items
//   body_changes.json     body-trait vars and transitions
//   scene_catalog.json    every passage seen and its visit count

'use strict';

const fs = require('fs');
const path = require('path');
const { labelProfile } = require('./labeler');
const { aggregateSessions } = require('./session');
const { buildStaticGraph } = require('./static_graph');
const { buildChoiceGraph, indexStaticGraph } = require('./choice_graph');

function fmtTime(s) {
  if (!s) return '0s';
  const m = Math.floor(s / 60);
  const ss = s % 60;
  return m ? `${m}m ${ss}s` : `${ss}s`;
}

function write(outRoot, detector, frontier, exploredCount, sessionsSummary, extras = {}) {
  fs.mkdirSync(outRoot, { recursive: true });

  // 1. Produce the statistical profile (evidence, no labels)
  const profile = detector.serialize();
  fs.writeFileSync(path.join(outRoot, 'variable_profile.json'), JSON.stringify(profile, null, 2));

  // 2. Apply labels
  const labeled = labelProfile(profile);

  // 3. Per-category JSONs
  fs.writeFileSync(path.join(outRoot, 'variable_schema.json'),
    JSON.stringify(Object.fromEntries(
      Object.entries(labeled.variables).map(([n, v]) => [n, {
        ...v.profile,
        label: v.label.primary,
        label_confidence: v.label.confidence,
        tags: v.label.tags,
      }])
    ), null, 2));

  fs.writeFileSync(path.join(outRoot, 'npcs.json'),
    JSON.stringify(labeled.npcs, null, 2));

  fs.writeFileSync(path.join(outRoot, 'items.json'),
    JSON.stringify({
      note: 'Labeled at report time from the raw variable profile. See variable_profile.json for raw evidence.',
      items: labeled.items,
    }, null, 2));

  fs.writeFileSync(path.join(outRoot, 'body_changes.json'),
    JSON.stringify({
      variables: labeled.body.vars,
      transitions: labeled.body.mutations,
    }, null, 2));

  fs.writeFileSync(path.join(outRoot, 'scene_catalog.json'),
    JSON.stringify(profile.passages, null, 2));

  // --- M2 static graph + M6.1 dynamic choice graph ---
  // As of M6.1, `static_graph.json` is written at daemon STARTUP (inside
  // live.js, after passage_catalog.json is dumped) — not rebuilt here.
  // This keeps a single source of truth and lets M6.2 navigation-intelligence
  // endpoints query it live.  We just read the startup-written file.
  //
  // Backward-compat: older exploration dirs that predate M6.1 won't have
  // the startup artifact. Fall back to building on the spot from the
  // catalog so `finalize` keeps working on those dirs.
  let staticGraph = null;
  let choiceGraph = null;
  try {
    const staticGraphPath = path.join(outRoot, 'static_graph.json');
    if (fs.existsSync(staticGraphPath)) {
      staticGraph = JSON.parse(fs.readFileSync(staticGraphPath, 'utf8'));
    } else {
      const catalogPath = path.join(outRoot, 'passage_catalog.json');
      if (fs.existsSync(catalogPath)) {
        const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
        staticGraph = buildStaticGraph(catalog);
        fs.writeFileSync(staticGraphPath, JSON.stringify(staticGraph, null, 2));
      } else {
        staticGraph = {
          generated_at: new Date().toISOString(),
          error: 'neither static_graph.json nor passage_catalog.json found',
          total_passages: 0, total_edges: 0, edges: [],
        };
      }
    }
  } catch (e) {
    staticGraph = { error: 'static graph load failed: ' + e.message, total_edges: 0, edges: [] };
  }
  try {
    const graphDirs = {
      playLog: path.join(outRoot, 'play_log.jsonl'),
      timeline: path.join(outRoot, 'state_timeline.jsonl'),
      initialState: path.join(outRoot, 'initial_state.json'),
    };
    const staticIdx = staticGraph && staticGraph.edges && staticGraph.edges.length
      ? indexStaticGraph(staticGraph) : null;
    choiceGraph = buildChoiceGraph(graphDirs, staticIdx);
    fs.writeFileSync(path.join(outRoot, 'choice_graph.json'), JSON.stringify(choiceGraph, null, 2));
  } catch (e) {
    choiceGraph = { error: 'choice graph build failed: ' + e.message, observed_edges: [] };
    fs.writeFileSync(path.join(outRoot, 'choice_graph.json'), JSON.stringify(choiceGraph, null, 2));
  }

  // 4. report.md
  const lines = [];
  lines.push(`# ${extras.gameName || 'Game'} — Exploration Report`);
  lines.push('');
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Source URL: ${extras.url || 'n/a'}`);
  lines.push('');
  lines.push('## Session Summary');
  lines.push('');
  lines.push(`- Sessions run: ${sessionsSummary.totals.session_count}`);
  lines.push(`- Total wall-clock: ${fmtTime(sessionsSummary.totals.total_duration_s)}`);
  lines.push(`- Total clicks: ${sessionsSummary.totals.total_clicks}`);
  lines.push(`- Total choices explored: ${sessionsSummary.totals.total_choices}`);
  lines.push(`- Unique states seen: ${exploredCount}`);
  lines.push(`- Unexplored frontier (queued for next session): ${frontier.size()}`);
  lines.push(`- Any ending reached: ${sessionsSummary.totals.any_completed ? 'yes' : 'not yet'}`);
  lines.push('');

  lines.push('## Engine');
  lines.push(`Detected engine: **${extras.engine || 'unknown'}**${extras.engineVersion ? ' v' + extras.engineVersion : ''}`);
  if (extras.canMarshal === false) lines.push('> Fast state snapshot unavailable — backtracking uses fallback.');
  lines.push('');

  // Variable schema, grouped by label
  lines.push('## Variable schema (labeled at report time)');
  lines.push('');
  const order = ['player_stat', 'npc_stat', 'body', 'time', 'item', 'flag', 'scalar', 'string', 'misc'];
  for (const cat of order) {
    const names = labeled.by_category[cat];
    if (!names || !names.length) continue;
    lines.push(`### ${cat} (${names.length})`);
    lines.push('');
    lines.push('| name | type | range / samples | mutations | confidence |');
    lines.push('|---|---|---|---|---|');
    for (const name of names.slice(0, 40)) {
      const v = labeled.variables[name];
      const prof = v.profile;
      const types = (prof.types || []).join(',');
      let rangeCell = '—';
      if (prof.number_stats) {
        rangeCell = `${prof.number_stats.min}..${prof.number_stats.max}`;
      } else if (prof.string_samples && prof.string_samples.length) {
        rangeCell = prof.string_samples.slice(0, 3).map((s) => '`' + String(s).slice(0, 20) + '`').join(', ');
      } else if (prof.bool_values && prof.bool_values.length) {
        rangeCell = prof.bool_values.join(', ');
      }
      lines.push(`| \`${name}\` | ${types} | ${rangeCell} | ${prof.mutation_count} | ${v.label.confidence} |`);
    }
    if (names.length > 40) lines.push(`| … | … | … | … | and ${names.length - 40} more |`);
    lines.push('');
  }

  // NPCs
  lines.push('## NPCs detected');
  lines.push('');
  if (Object.keys(labeled.npcs).length) {
    lines.push('| npc | stats observed | var count |');
    lines.push('|---|---|---|');
    for (const [n, d] of Object.entries(labeled.npcs)) {
      lines.push(`| ${n} | ${d.stats.join(', ')} | ${d.vars.length} |`);
    }
  } else {
    lines.push('_No NPCs detected yet._');
  }
  lines.push('');

  // Body / appearance
  lines.push('## Body / appearance traits');
  lines.push('');
  if (labeled.body.vars.length) {
    for (const v of labeled.body.vars.slice(0, 30)) lines.push(`- \`${v.name}\``);
    lines.push('');
    if (labeled.body.mutations.length) {
      lines.push(`Transitions observed: ${labeled.body.mutations.length}`);
      for (const m of labeled.body.mutations.slice(0, 20)) {
        lines.push(`- \`${m.var}\`: \`${JSON.stringify(m.before)}\` → \`${JSON.stringify(m.after)}\` at \`${m.passage}\``);
      }
    }
  } else {
    lines.push('_No body/appearance variables detected._');
  }
  lines.push('');

  // Choice type distribution
  lines.push('## Choice type distribution');
  lines.push('');
  const byCls = profile.choices.by_classification;
  if (Object.keys(byCls).length) {
    lines.push('| type | count |');
    lines.push('|---|---|');
    for (const [k, v] of Object.entries(byCls).sort((a, b) => b[1] - a[1])) {
      lines.push(`| ${k} | ${v} |`);
    }
  } else {
    lines.push('_No choices classified yet._');
  }
  lines.push('');

  // Economy
  lines.push('## Economy');
  lines.push('');
  const priceObs = profile.choices.price_observations || [];
  const incomeN = labeled.economy.income_events.length;
  const expenseN = labeled.economy.expense_events.length;
  lines.push(`- Price-labeled choices observed: ${priceObs.length}`);
  lines.push(`- Money income events: ${incomeN}`);
  lines.push(`- Money expense events: ${expenseN}`);
  if (priceObs.length) {
    const prices = priceObs.map((p) => p.price).filter((x) => Number.isFinite(x));
    if (prices.length) {
      lines.push(`- Price range: $${Math.min(...prices)} – $${Math.max(...prices)}`);
    }
    lines.push('');
    lines.push('| price | label | at passage |');
    lines.push('|---|---|---|');
    for (const p of priceObs.slice(0, 20)) lines.push(`| $${p.price} | ${p.label} | ${p.passage} |`);
  }
  lines.push('');

  // Prefix clusters (possible entity groups)
  lines.push('## Variable prefix clusters');
  lines.push('');
  lines.push('Variables sharing a leading token — candidate entity groups (verify manually).');
  lines.push('');
  const clusterEntries = Object.entries(profile.prefix_clusters || {}).sort((a, b) => b[1].length - a[1].length).slice(0, 20);
  if (clusterEntries.length) {
    for (const [p, names] of clusterEntries) {
      lines.push(`- **${p}** (${names.length}): ${names.slice(0, 6).map((n) => '`' + n + '`').join(', ')}${names.length > 6 ? ', …' : ''}`);
    }
  } else {
    lines.push('_No prefix clusters detected._');
  }
  lines.push('');

  // Sessions
  lines.push('## Sessions');
  lines.push('');
  lines.push('| # | started | duration | clicks | choices | new states | completed |');
  lines.push('|---|---|---|---|---|---|---|');
  for (const s of sessionsSummary.sessions) {
    lines.push(`| ${s.session_id} | ${s.start_ts} | ${fmtTime(s.duration_s)} | ${s.clicks} | ${s.choices_explored} | ${s.new_unique_states} | ${s.completed ? 'yes' : 'no'} |`);
  }
  lines.push('');

  // M2: Graph coverage section — where did we actually go vs. where could we go?
  lines.push('## Graph coverage (observed vs. static)');
  lines.push('');
  if (staticGraph && choiceGraph) {
    const se = staticGraph.total_edges || 0;
    const oe = choiceGraph.total_observed_edges || 0;
    const cov = (choiceGraph.coverage && choiceGraph.coverage.coverage_ratio != null)
      ? (choiceGraph.coverage.coverage_ratio * 100).toFixed(2) + '%' : 'n/a';
    const observedStatic = choiceGraph.coverage ? choiceGraph.coverage.observed_static_edges : 0;
    const observedOnly = choiceGraph.coverage ? choiceGraph.coverage.observed_only_edges : 0;
    lines.push(`- Static-graph edges (every navigation parsed from passage source): **${se}**`);
    lines.push(`- Observed edges during play: **${oe}** unique \`(from, clicked_text, to)\` tuples.`);
    lines.push(`- Static edges covered by at least one observation: **${observedStatic}** (a single observation covers every static edge with the same \`(from, to)\` pair — gated branches collapse to one observable move).`);
    lines.push(`- Observed-only edges (no matching static edge, typically self-loop \`<<link>>\` wrappers that \`<<replace>>\` in-place): **${observedOnly}**.`);
    lines.push(`- Coverage: **${cov}** of the static graph explored.`);
    lines.push(`- Synthetic edges (Claude's out-of-band \`eval\`/\`keys\`/\`restore\`/\`pop\`): ${choiceGraph.total_synthetic_edges || 0}`);
    lines.push('');
    const byKind = staticGraph.edges_by_kind || {};
    if (Object.keys(byKind).length) {
      lines.push('### Static edge kinds');
      lines.push('| kind | count |');
      lines.push('|---|---|');
      for (const [k, v] of Object.entries(byKind).sort((a, b) => b[1] - a[1])) {
        lines.push(`| ${k} | ${v} |`);
      }
      lines.push('');
    }
    if (staticGraph.unresolved_targets && staticGraph.unresolved_targets.length) {
      lines.push(`### Unresolved static targets (${staticGraph.unresolved_targets.length})`);
      lines.push('Targets that appear in passage source but don\'t resolve to a known passage — typically dynamic expressions like `` <<goto `func()`>> `` or referenced-but-never-defined passages.');
      lines.push('');
      for (const t of staticGraph.unresolved_targets.slice(0, 20)) lines.push(`- \`${t}\``);
      if (staticGraph.unresolved_targets.length > 20) lines.push(`- … and ${staticGraph.unresolved_targets.length - 20} more`);
      lines.push('');
    }
  } else {
    lines.push('_Graph generation skipped or failed — see `static_graph.json` / `choice_graph.json` for details._');
    lines.push('');
  }

  lines.push('## See also');
  lines.push('- `variable_profile.json` — raw statistical evidence, no labels');
  lines.push('- `variable_schema.json` — variables with applied labels + confidence');
  lines.push('- `mechanics.md` — design patterns observed');
  lines.push('- `coverage.md` — frontier + explored counts');
  lines.push('- `static_graph.json` — every navigation edge parsed from passage source (M2, written at startup as of M6.1)');
  lines.push('- `choice_graph.json` — observed edges with per-edge effect aggregates (M2)');
  lines.push('- `variable_index.json` — every game variable → passages/edges that `<<set>>`/`<<unset>>` it, with enclosing `<<if>>` gates (M6.1)');
  lines.push('- `passage_catalog.json` — every passage with raw source + tags (M1)');
  lines.push('- `scene_bodies.jsonl` — full rendered body per unique state (M1)');
  lines.push('- `initial_state.json` — pristine pre-Phase-0a snapshot (M1)');
  lines.push('- `state_timeline.jsonl` — per-observation state + full diff values (M1)');
  lines.push('- `engine_config.json` — SugarCube Config/Setting/version/save-caps + State.history shape + Story IFID (M3)');
  lines.push('- `sidebar_snapshots.jsonl` — sidebar panel text captures across Phase 0 probes + passive mid-game changes (M4)');

  fs.writeFileSync(path.join(outRoot, 'report.md'), lines.join('\n'));

  // 5. mechanics.md — design patterns observed
  const mech = [];
  mech.push(`# ${extras.gameName || 'Game'} — Mechanical Patterns`);
  mech.push('');
  mech.push('> Design patterns detected. Framed for "what could this game teach mine?"');
  mech.push('');

  const pattern = (title, present, detail) => {
    mech.push(`### ${title}`);
    mech.push(present ? `**Present.** ${detail}` : `_Not detected._`);
    mech.push('');
  };

  const hasMoney = (labeled.by_category.player_stat || []).some((n) => /money|cash|gold/i.test(n));
  const hasTime = (labeled.by_category.time || []).length > 0;
  const hasPayment = (byCls.payment || 0) > 0;
  const hasQuiz = (byCls.quiz || 0) > 0;
  const hasActionLoop = (byCls.action_loop || 0) > 0;
  const hasBody = labeled.body.vars.length > 0;
  const hasMultipleNpcs = Object.keys(labeled.npcs).length > 1;
  const hasLocation = (byCls.location || 0) > 0;

  pattern('Money / economic system', hasMoney,
    `Money-like variable(s) detected. Income events: ${labeled.economy.income_events.length}. Expense events: ${labeled.economy.expense_events.length}.`);
  pattern('Time / calendar system', hasTime,
    `${(labeled.by_category.time || []).length} time-like variable(s). Choices may be day-anchored.`);
  pattern('Payment choices (visible prices)', hasPayment,
    `${byCls.payment} payment-type choices observed — prices appear directly in option text.`);
  pattern('Quiz / correct-answer puzzles', hasQuiz,
    `${byCls.quiz} quiz-style choice instances. Wrong answers likely block content.`);
  pattern('Action-menu loops (in-scene mini-game)', hasActionLoop,
    `${byCls.action_loop} action-loop choice instances.`);
  pattern('Body / appearance transformation', hasBody,
    `${labeled.body.vars.length} body-like variable(s). Transitions: ${labeled.body.mutations.length}.`);
  pattern('Multi-NPC parallel threads', hasMultipleNpcs,
    `${Object.keys(labeled.npcs).length} NPCs detected with dedicated stat vars.`);
  pattern('Location trilemmas / day-end navigation', hasLocation,
    `${byCls.location} explicit "Go to X" choices.`);

  mech.push('## Scenes catalogued');
  mech.push(`- Unique passages seen: ${Object.keys(profile.passages).length}`);
  const top = Object.entries(profile.passages).sort((a, b) => b[1].visit_count - a[1].visit_count).slice(0, 15);
  mech.push('- Most-visited passages:');
  for (const [p, info] of top) mech.push(`  - \`${p}\` × ${info.visit_count}`);
  mech.push('');

  fs.writeFileSync(path.join(outRoot, 'mechanics.md'), mech.join('\n'));

  // 6. coverage.md
  const cov = [];
  cov.push(`# ${extras.gameName || 'Game'} — Coverage`);
  cov.push('');
  cov.push(`- Unique states visited: ${exploredCount}`);
  cov.push(`- Queued for future sessions: ${frontier.size()}`);
  const fs_summary = frontier.summary();
  cov.push(`- Deepest unexplored branch: depth ${fs_summary.deepest}`);
  cov.push('');
  cov.push('Frontier lives in `saves/frontier.jsonl`. LIFO / DFS pop order.');
  fs.writeFileSync(path.join(outRoot, 'coverage.md'), cov.join('\n'));
}

module.exports = { write };
