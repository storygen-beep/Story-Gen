// Generate the human-readable artifacts:
//   - report.md        top-level synthesis
//   - mechanics.md     "what this game does that yours could borrow"
//   - coverage.md      what's explored vs queued
//   - npcs.json, items.json, body_changes.json, etc. (JSON cuts of the detector state)

'use strict';

const fs = require('fs');
const path = require('path');
const { aggregateSessions } = require('./session');

function fmtTime(s) {
  if (!s) return '0s';
  const m = Math.floor(s / 60);
  const ss = s % 60;
  return m ? `${m}m ${ss}s` : `${ss}s`;
}

function group(obj, fn) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    const g = fn(k, v);
    if (!out[g]) out[g] = [];
    out[g].push([k, v]);
  }
  return out;
}

function write(outRoot, detector, frontier, exploredCount, sessionsSummary, extras = {}) {
  fs.mkdirSync(outRoot, { recursive: true });
  const detData = detector.serialize();

  // Per-category JSONs
  const byCategory = group(detData.variables, (k, v) => v.category);
  fs.writeFileSync(path.join(outRoot, 'variable_schema.json'), JSON.stringify(detData.variables, null, 2));

  const bodyVars = (byCategory['body'] || []).map(([k, v]) => ({ name: k, ...v }));
  fs.writeFileSync(path.join(outRoot, 'body_changes.json'), JSON.stringify({
    variables: bodyVars,
    transitions: detData.body_changes,
  }, null, 2));

  fs.writeFileSync(path.join(outRoot, 'npcs.json'), JSON.stringify(detData.npcs, null, 2));

  const itemVars = (byCategory['item'] || []).map(([k, v]) => ({ name: k, ...v }));
  fs.writeFileSync(path.join(outRoot, 'items.json'), JSON.stringify({
    known_items: itemVars,
    list_vars: (byCategory['list'] || []).map(([k, v]) => ({ name: k, ...v })),
    note: 'Items detected by name pattern (flower, pill, teddybear, etc.) or by being an array-typed variable. Verify manually.',
  }, null, 2));

  fs.writeFileSync(path.join(outRoot, 'scene_catalog.json'), JSON.stringify(detData.passages, null, 2));

  // report.md
  const report = [];
  report.push(`# ${extras.gameName || 'Game'} — Exploration Report`);
  report.push('');
  report.push(`Generated: ${new Date().toISOString()}`);
  report.push(`Source URL: ${extras.url || 'n/a'}`);
  report.push('');
  report.push('## Session Summary');
  report.push('');
  report.push(`- Sessions run: ${sessionsSummary.totals.session_count}`);
  report.push(`- Total wall-clock: ${fmtTime(sessionsSummary.totals.total_duration_s)}`);
  report.push(`- Total clicks: ${sessionsSummary.totals.total_clicks}`);
  report.push(`- Total choices explored: ${sessionsSummary.totals.total_choices}`);
  report.push(`- Unique states seen: ${exploredCount}`);
  report.push(`- Unexplored frontier (queued for next session): ${frontier.size()}`);
  report.push(`- Any ending reached: ${sessionsSummary.totals.any_completed ? 'yes' : 'not yet'}`);
  report.push('');

  report.push('## Engine');
  report.push(`Detected engine: **${extras.engine || 'unknown'}**${extras.engineVersion ? ' v' + extras.engineVersion : ''}`);
  if (extras.canMarshal === false) report.push('> Fast state snapshot (marshal API) unavailable — falling back to path-replay for backtracking.');
  report.push('');

  report.push('## Variable schema (inferred)');
  report.push('');
  for (const cat of ['player_stat', 'npc_stat', 'body', 'time', 'item', 'flag', 'list', 'structure', 'scalar', 'misc']) {
    const rows = byCategory[cat] || [];
    if (!rows.length) continue;
    report.push(`### ${cat} (${rows.length})`);
    report.push('');
    report.push('| name | type | range | samples |');
    report.push('|---|---|---|---|');
    for (const [name, v] of rows.slice(0, 40)) {
      const range = v.type === 'number'
        ? (v.min != null && v.max != null ? `${v.min}..${v.max}` : '—')
        : '—';
      const samples = (v.samples || []).slice(0, 5).map((s) => '`' + String(s).slice(0, 24) + '`').join(', ');
      report.push(`| \`${name}\` | ${v.type} | ${range} | ${samples} |`);
    }
    if (rows.length > 40) report.push(`| … | … | … | and ${rows.length - 40} more |`);
    report.push('');
  }

  report.push('## NPCs detected');
  report.push('');
  if (Object.keys(detData.npcs).length) {
    report.push('| name | stats observed | first seen (s) |');
    report.push('|---|---|---|');
    for (const [n, d] of Object.entries(detData.npcs)) {
      report.push(`| ${n} | ${(d.stats || []).join(', ')} | ${Math.round((d.firstSeenAt || 0) / 1000)} |`);
    }
  } else {
    report.push('_No NPCs detected yet._');
  }
  report.push('');

  report.push('## Body / appearance traits');
  report.push('');
  if (bodyVars.length) {
    report.push('Variables matching body/appearance patterns:');
    report.push('');
    for (const v of bodyVars) report.push(`- \`${v.name}\` (${v.type}${v.min != null ? `, range ${v.min}..${v.max}` : ''})`);
    report.push('');
    if (detData.body_changes.length) {
      report.push(`Transitions observed: ${detData.body_changes.length}`);
      for (const t of detData.body_changes.slice(0, 20)) {
        report.push(`- \`${t.var}\`: \`${JSON.stringify(t.before)}\` → \`${JSON.stringify(t.after)}\` at passage \`${t.at_passage}\``);
      }
    }
  } else {
    report.push('_No body/appearance variables detected._');
  }
  report.push('');

  report.push('## Choice type distribution');
  report.push('');
  if (Object.keys(detData.choice_type_counts).length) {
    report.push('| type | count |');
    report.push('|---|---|');
    for (const [k, v] of Object.entries(detData.choice_type_counts).sort((a, b) => b[1] - a[1])) {
      report.push(`| ${k} | ${v} |`);
    }
  } else {
    report.push('_No choices classified yet._');
  }
  report.push('');

  report.push('## Economy (price observations)');
  report.push('');
  if (detData.price_observations.length) {
    const prices = detData.price_observations.map((p) => p.price).filter(Boolean);
    report.push(`Price range observed: $${Math.min(...prices)} to $${Math.max(...prices)} across ${prices.length} price choices`);
    report.push('');
    report.push('| price | label | at passage |');
    report.push('|---|---|---|');
    for (const p of detData.price_observations.slice(0, 30)) {
      report.push(`| $${p.price} | ${p.label} | ${p.at} |`);
    }
  } else {
    report.push('_No price choices observed._');
  }
  report.push('');

  report.push('## Sessions');
  report.push('');
  report.push('| # | started | duration | clicks | choices | new states | completed |');
  report.push('|---|---|---|---|---|---|---|');
  for (const s of sessionsSummary.sessions) {
    report.push(`| ${s.session_id} | ${s.start_ts} | ${fmtTime(s.duration_s)} | ${s.clicks} | ${s.choices_explored} | ${s.new_unique_states} | ${s.completed ? 'yes' : 'no'} |`);
  }
  report.push('');

  report.push('## See also');
  report.push('- `mechanics.md` — design patterns observed');
  report.push('- `coverage.md` — exploration coverage + unexplored frontier');
  report.push('- `choice_graph.json` — every decision point mapped');
  report.push('- `state_timeline.jsonl` — full state snapshot history');
  report.push('- `screenshots/` — scenes and choices');

  fs.writeFileSync(path.join(outRoot, 'report.md'), report.join('\n'));

  // mechanics.md — design patterns the game uses
  const mech = [];
  mech.push(`# ${extras.gameName || 'Game'} — Mechanical Patterns`);
  mech.push('');
  mech.push('> Design patterns detected, framed for "what could my game borrow from this?"');
  mech.push('');

  const pattern = (title, present, detail) => {
    mech.push(`### ${title}`);
    mech.push(present ? `**Present.** ${detail}` : `_Not detected._`);
    mech.push('');
  };

  const hasMoney = Object.keys(detData.variables).some((k) => /\b(money|cash|gold|balance)\b/i.test(k));
  const hasTime = Object.keys(detData.variables).some((k) => /\b(day|hour|week)\b/i.test(k));
  const hasPayment = (detData.choice_type_counts.payment || 0) > 0;
  const hasQuiz = (detData.choice_type_counts.quiz || 0) > 0;
  const hasActionLoop = (detData.choice_type_counts.action_loop || 0) > 0;
  const hasBody = bodyVars.length > 0;
  const hasMultipleNpcs = Object.keys(detData.npcs).length > 1;
  const hasLocation = (detData.choice_type_counts.location || 0) > 0;

  pattern('Money / economic system', hasMoney,
    `Money-like variable(s) detected. Prices surface in choice text (${hasPayment ? 'yes — payment choices seen' : 'no payment choices yet'}). Income/expense events: ${detData.economy.incomeEvents.length}/${detData.economy.expenseEvents.length}.`);
  pattern('Time / calendar system', hasTime,
    'Day/hour/week counters appear in state. Game is likely day-anchored — choices may be tied to specific days.');
  pattern('Payment choices (visible prices)', hasPayment,
    `${detData.choice_type_counts.payment} choice(s) with in-choice prices observed — the game surfaces "this costs $X" directly in the UI.`);
  pattern('Quiz / correct-answer puzzles', hasQuiz,
    `${detData.choice_type_counts.quiz} quiz-style choices (a/b/c/d labels). Wrong answers likely block content.`);
  pattern('Action-menu loops (in-scene mini-game)', hasActionLoop,
    `${detData.choice_type_counts.action_loop} action-loop choice instances. Intimate / combat scenes use cyclic action menus as gameplay rather than linear narration.`);
  pattern('Body / appearance transformation', hasBody,
    `${bodyVars.length} body-like variable(s). Transitions observed: ${detData.body_changes.length}. The game tracks visible player transformation.`);
  pattern('Multi-NPC parallel threads', hasMultipleNpcs,
    `${Object.keys(detData.npcs).length} NPCs detected concurrently in play. NPC threads run in parallel, not sequentially.`);
  pattern('Location trilemmas / day-end navigation', hasLocation,
    `${detData.choice_type_counts.location} explicit "Go to X" choices — end-of-day location decisions that lock out the alternatives.`);

  mech.push('## Scenes catalogued');
  mech.push(`- Unique passages seen: ${Object.keys(detData.passages).length}`);
  const passageTop = Object.entries(detData.passages).sort((a, b) => b[1].count - a[1].count).slice(0, 15);
  mech.push('- Most-visited passages:');
  for (const [p, info] of passageTop) mech.push(`  - \`${p}\` × ${info.count}`);
  mech.push('');

  fs.writeFileSync(path.join(outRoot, 'mechanics.md'), mech.join('\n'));

  // coverage.md
  const cov = [];
  cov.push(`# ${extras.gameName || 'Game'} — Coverage`);
  cov.push('');
  cov.push(`- Unique states visited (explored): ${exploredCount}`);
  cov.push(`- Queued for future sessions: ${frontier.size()}`);
  const summary = frontier.summary();
  cov.push(`- Deepest unexplored branch: depth ${summary.deepest}`);
  cov.push('');
  cov.push('Frontier is stored in `saves/frontier.jsonl` — each line is a push/pop op. The explorer pops LIFO (DFS).');
  fs.writeFileSync(path.join(outRoot, 'coverage.md'), cov.join('\n'));
}

module.exports = { write };
