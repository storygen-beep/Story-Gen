// Variable setter index.
//
// For every $variable the game exposes, which passages (and wiki-link
// edges) <<set>> or <<unset>> it, and to what value. Complement to
// static_graph.js — the graph tells you which passages link to which;
// the variable index tells you which passages MUTATE which variables.
// Join them and you can answer "to reach passage X I need
// $y === z; where does $y get set to z?".
//
// What we parse:
//   - <<set $x = v>> and <<set $x to v>>  (passage bodies)
//   - Compound forms: +=, -=, *=, /=, %=, &&=, ||=, ??=, ++, --
//   - Multi-statement: <<set $x = 1, $y = 2>>  (split on top-level commas)
//   - Object-property writes: <<set $player.clothing = "uniform">>
//     emit TWO records: one under `$player` (path: ".clothing") and one
//     under the dotted full key `$player.clothing`. Either lookup works.
//   - <<unset $x>> and multi-target variants
//   - Edge setters from static_graph.json (wiki-link setter suffix
//     `[[A|B][$x += 1]]`) — SugarCube allows `;` as a statement
//     separator inside these, so we normalize before re-using the
//     regular <<set>> parser.
//
// What we skip on purpose:
//   - <<script>>...<</script>> blocks. Too brittle to parse statically;
//     block count recorded, indexing_coverage flips to "partial".
//   - Widget bodies (tag `widget`). Widgets fire on invocation, not on
//     display — their setters belong to their callers, which would
//     require call-graph analysis. Out of scope.
//   - Passages tagged `script`, `stylesheet`, or `Twine.private` — not
//     narrative content.
//   - Unparseable clauses. Emitted into `complex_setters` with the
//     raw arg so nothing is silently dropped.
//
// Gate stack mirrors static_graph.js exactly: every emitted record
// carries `gate: [{condition, branch}, ...]` describing the enclosing
// <<if>>/<<elseif>>/<<else>> chain (empty array = unconditional).

'use strict';

const SKIP_TAGS = new Set(['script', 'stylesheet', 'Twine.private', 'widget']);

// Token regex. Script-block span matches FIRST so we don't pick up
// macros inside JS. Then /closer + name + optional args.
const TOKEN_RE = /<<script>>[\s\S]*?<<\/script>>|<<(\/?)(\w+)(?:\s+([\s\S]*?))?>>/g;

// Longest first. 'to' and '=' are handled specially in parseSetClause.
const COMPOUND_OPS = ['+=', '-=', '*=', '/=', '%=', '&&=', '||=', '??='];
const INC_DEC = ['++', '--'];

// ---------------------------------------------------------------------------
// Clause splitting — commas at top level only (outside strings / brackets).
// ---------------------------------------------------------------------------

function splitStatements(arg) {
  const out = [];
  let depth = 0;
  let inStr = null;
  let buf = '';
  for (let i = 0; i < arg.length; i++) {
    const ch = arg[i];
    const prev = i > 0 ? arg[i - 1] : '';
    if (inStr) {
      buf += ch;
      if (ch === inStr && prev !== '\\') inStr = null;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; buf += ch; continue; }
    if (ch === '(' || ch === '[' || ch === '{') { depth++; buf += ch; continue; }
    if (ch === ')' || ch === ']' || ch === '}') { depth--; buf += ch; continue; }
    if (ch === ',' && depth === 0) {
      const s = buf.trim();
      if (s) out.push(s);
      buf = '';
      continue;
    }
    buf += ch;
  }
  const last = buf.trim();
  if (last) out.push(last);
  return out;
}

// ---------------------------------------------------------------------------
// LHS parsing — pull the primary $variable and any dotted/bracket accessor.
// ---------------------------------------------------------------------------

const LHS_RE = /^\$([A-Za-z_][A-Za-z0-9_]*)((?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]+\])*)/;

function parseLhs(clause) {
  const m = clause.match(LHS_RE);
  if (!m) return null;
  return {
    primary_var: '$' + m[1],
    path: m[2] || null,
    after: clause.slice(m[0].length).trimStart(),
  };
}

// ---------------------------------------------------------------------------
// <<set>> clause parser. Returns an array of records:
//   { primary_var, path, op, value_expr }   (length 1, or 2 if path present)
//   [{ complex: true, raw_arg }]            (parse failure)
// ---------------------------------------------------------------------------

function parseSetClause(clause) {
  const trimmed = clause.trim();
  if (!trimmed) return [];

  const lhs = parseLhs(trimmed);
  if (!lhs) return [{ complex: true, raw_arg: trimmed }];

  const after = lhs.after;
  let op = null;
  let rhs = '';

  // Increment / decrement: must be exactly `++` or `--` with nothing after
  // (or trailing whitespace).
  if (after === '++' || after === '--') {
    op = after;
    rhs = '';
  } else {
    // Compound operators first (longest-first to avoid matching `=` inside `+=`).
    for (const candidate of COMPOUND_OPS) {
      if (after.startsWith(candidate)) {
        op = candidate;
        rhs = after.slice(candidate.length).trim();
        break;
      }
    }
    // 'to' keyword — must be word-bounded (not a prefix of 'total' etc.).
    if (op == null && /^to\b/.test(after)) {
      op = 'to';
      rhs = after.slice(2).trim();
    }
    // Plain assignment. Disambiguate from `==`/`===` which shouldn't appear
    // on a <<set>> LHS but could if the parser's wrong — bail to complex.
    if (op == null && after.startsWith('=') && !after.startsWith('==')) {
      op = '=';
      rhs = after.slice(1).trim();
    }
  }

  if (op == null) return [{ complex: true, raw_arg: trimmed }];

  const records = [
    { primary_var: lhs.primary_var, path: lhs.path, op, value_expr: rhs || null },
  ];
  return records;
}

function parseSetArg(arg) {
  if (!arg || !arg.trim()) return [];
  const clauses = splitStatements(arg);
  const out = [];
  for (const c of clauses) {
    for (const r of parseSetClause(c)) out.push(r);
  }
  return out;
}

// ---------------------------------------------------------------------------
// <<unset>> arg parser. Space- or comma-separated $identifiers.
// ---------------------------------------------------------------------------

function parseUnsetArg(arg) {
  if (!arg || !arg.trim()) return [];
  const tokens = arg.split(/[,\s]+/).filter(Boolean);
  const out = [];
  for (const tok of tokens) {
    const lhs = parseLhs(tok);
    if (!lhs) { out.push({ complex: true, raw_arg: tok }); continue; }
    out.push({ primary_var: lhs.primary_var, path: lhs.path });
  }
  return out;
}

// ---------------------------------------------------------------------------
// Edge setter: SugarCube allows `;` as a statement separator inside the
// setter suffix. Normalize to `,` then reuse parseSetArg.
// ---------------------------------------------------------------------------

function parseEdgeSetter(setterStr) {
  if (!setterStr) return [];
  // Split on `;` at top level, then run each piece through parseSetArg.
  // Simpler than a full re-implementation — we just replace top-level
  // semicolons with commas and reuse splitStatements' top-level awareness.
  const out = [];
  let depth = 0;
  let inStr = null;
  let buf = '';
  const flush = () => {
    const s = buf.trim();
    if (s) for (const r of parseSetArg(s)) out.push(r);
    buf = '';
  };
  for (let i = 0; i < setterStr.length; i++) {
    const ch = setterStr[i];
    const prev = i > 0 ? setterStr[i - 1] : '';
    if (inStr) {
      buf += ch;
      if (ch === inStr && prev !== '\\') inStr = null;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; buf += ch; continue; }
    if (ch === '(' || ch === '[' || ch === '{') { depth++; buf += ch; continue; }
    if (ch === ')' || ch === ']' || ch === '}') { depth--; buf += ch; continue; }
    if (ch === ';' && depth === 0) { flush(); continue; }
    buf += ch;
  }
  flush();
  return out;
}

// ---------------------------------------------------------------------------
// Passage-level scanner. Tracks gate stack, emits setter + unsetter records
// with `gate` snapshot attached.
// ---------------------------------------------------------------------------

function parsePassage(passageName, source) {
  const setters = [];
  const unsetters = [];
  let scriptBlocks = 0;
  let parseErrors = 0;
  const gateStack = [];
  const snapshotGate = () => gateStack.map((g) => ({ condition: g.condition, branch: g.branch }));

  let m;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(source)) !== null) {
    const full = m[0];
    if (full.startsWith('<<script>>')) { scriptBlocks++; continue; }

    const isClose = m[1] === '/';
    const macro = (m[2] || '').toLowerCase();
    const args = m[3] || '';

    if (!isClose && macro === 'if') {
      gateStack.push({ condition: args.trim(), branch: 'if' });
      continue;
    }
    if (!isClose && (macro === 'elseif' || macro === 'else')) {
      if (gateStack.length) {
        gateStack[gateStack.length - 1] = {
          condition: macro === 'else'
            ? `!(${gateStack[gateStack.length - 1].condition})`
            : args.trim(),
          branch: macro,
        };
      }
      continue;
    }
    if ((isClose && macro === 'if') || (!isClose && macro === 'endif')) {
      gateStack.pop();
      continue;
    }

    if (!isClose && macro === 'set') {
      for (const r of parseSetArg(args)) {
        if (r.complex) {
          parseErrors++;
          setters.push({ complex: true, raw_arg: r.raw_arg, passage: passageName, gate: snapshotGate() });
        } else {
          setters.push({
            primary_var: r.primary_var,
            path: r.path,
            op: r.op,
            value_expr: r.value_expr,
            passage: passageName,
            gate: snapshotGate(),
          });
        }
      }
      continue;
    }
    if (!isClose && macro === 'unset') {
      for (const r of parseUnsetArg(args)) {
        if (r.complex) {
          parseErrors++;
          unsetters.push({ complex: true, raw_arg: r.raw_arg, passage: passageName, gate: snapshotGate() });
        } else {
          unsetters.push({
            primary_var: r.primary_var,
            path: r.path,
            passage: passageName,
            gate: snapshotGate(),
          });
        }
      }
      continue;
    }
    // Anything else: ignored.
  }

  return { setters, unsetters, script_blocks: scriptBlocks, parse_errors: parseErrors };
}

// ---------------------------------------------------------------------------
// Index assembly.
// ---------------------------------------------------------------------------

function ensureVar(variables, key) {
  if (!variables[key]) {
    variables[key] = { setters: [], unsetters: [] };
  }
  return variables[key];
}

/**
 * Build the variable setter index. Pure function — no I/O.
 *
 * @param {object} catalog       passage_catalog payload
 * @param {object} staticGraph   static_graph payload (for edge setters)
 * @param {object|null} initialState initial_state payload (for initial values)
 * @returns {object} JSON-serializable index.
 */
function buildVariableIndex(catalog, staticGraph, initialState) {
  const variables = {};
  const complexSetters = [];
  let skippedScriptBlocks = 0;
  let skippedWidgetPassages = 0;
  let skippedPassages = 0;
  let parseErrors = 0;

  const passages = (catalog && Array.isArray(catalog.passages)) ? catalog.passages : [];

  const fileSetter = (rec) => {
    // Record under primary_var with path preserved.
    const vPrimary = ensureVar(variables, rec.primary_var);
    const copy = { ...rec };
    delete copy.primary_var;
    vPrimary.setters.push(copy);
    // Also file under dotted full key if path present.
    if (rec.path) {
      const fullKey = rec.primary_var + rec.path;
      const vFull = ensureVar(variables, fullKey);
      vFull.setters.push({ ...copy });
    }
  };
  const fileUnsetter = (rec) => {
    const vPrimary = ensureVar(variables, rec.primary_var);
    const copy = { ...rec };
    delete copy.primary_var;
    vPrimary.unsetters.push(copy);
    if (rec.path) {
      const fullKey = rec.primary_var + rec.path;
      const vFull = ensureVar(variables, fullKey);
      vFull.unsetters.push({ ...copy });
    }
  };

  for (const p of passages) {
    const tags = Array.isArray(p.tags) ? p.tags : [];
    if (tags.some((t) => SKIP_TAGS.has(t))) {
      skippedPassages++;
      if (tags.includes('widget')) skippedWidgetPassages++;
      continue;
    }
    const src = typeof p.source_raw === 'string' ? p.source_raw : '';
    if (!src) continue;

    let result;
    try {
      result = parsePassage(p.name, src);
    } catch (e) {
      parseErrors++;
      continue;
    }
    skippedScriptBlocks += result.script_blocks;
    parseErrors += result.parse_errors;

    for (const s of result.setters) {
      if (s.complex) {
        complexSetters.push({ kind: 'passage_body', ...s });
        continue;
      }
      fileSetter({ kind: 'passage_body', ...s });
    }
    for (const u of result.unsetters) {
      if (u.complex) {
        complexSetters.push({ kind: 'passage_body_unset', ...u });
        continue;
      }
      fileUnsetter({ kind: 'passage_body', ...u });
    }
  }

  // Edge setters — inherit the edge's gate so downstream consumers know
  // these setters fire only when the edge is actually traversed AND the
  // enclosing passage gate was satisfied.
  const edges = (staticGraph && Array.isArray(staticGraph.edges)) ? staticGraph.edges : [];
  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    if (!e.setter) continue;
    let parsed;
    try {
      parsed = parseEdgeSetter(e.setter);
    } catch (err) {
      parseErrors++;
      continue;
    }
    for (const r of parsed) {
      if (r.complex) {
        parseErrors++;
        complexSetters.push({
          kind: 'edge_setter',
          edge_index: i,
          from: e.from,
          to: e.to,
          raw_arg: r.raw_arg,
          gate: Array.isArray(e.gate) ? e.gate : [],
        });
        continue;
      }
      fileSetter({
        kind: 'edge_setter',
        edge_index: i,
        from: e.from,
        to: e.to,
        primary_var: r.primary_var,
        path: r.path,
        op: r.op,
        value_expr: r.value_expr,
        gate: Array.isArray(e.gate) ? e.gate : [],
      });
    }
  }

  // Seed initial values from initial_state.json.
  const initialVars = (initialState && initialState.variables) || {};
  for (const [name, val] of Object.entries(initialVars)) {
    const key = name.startsWith('$') ? name : '$' + name;
    const v = ensureVar(variables, key);
    v.initial_value = val;
  }

  const isPartial = skippedScriptBlocks > 0
    || skippedWidgetPassages > 0
    || parseErrors > 0
    || complexSetters.length > 0;

  return {
    generated_at: new Date().toISOString(),
    indexing_coverage: isPartial ? 'partial' : 'full',
    total_variables: Object.keys(variables).length,
    skipped_script_blocks: skippedScriptBlocks,
    skipped_widget_passages: skippedWidgetPassages,
    skipped_passages: skippedPassages,
    parse_errors: parseErrors,
    complex_setter_count: complexSetters.length,
    variables,
    complex_setters: complexSetters,
  };
}

module.exports = {
  buildVariableIndex,
  parseSetArg,
  parseUnsetArg,
  parseEdgeSetter,
  parsePassage,
  splitStatements,
};
