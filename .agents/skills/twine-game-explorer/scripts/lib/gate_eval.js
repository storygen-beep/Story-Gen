// Gate expression evaluator — L0 + L1 only.
//
// L0: extract every $var / _var mentioned in the condition and resolve their
//     current values, so downstream consumers can READ the gate (and Claude
//     can reason over it) even when we can't compute a truth value.
// L1: evaluate the common forms against the current variable state:
//     - boolean combinators: &&, ||, !, SugarCube `and`/`or`/`not` keywords
//     - comparisons: ===, !==, ==, !=, >, <, >=, <=
//     - bare truthy check:  `$x`
//     - negation:           `!$x`, `not $x`
//     - paren grouping:     `(...)`, `!(...)`
//
// Anything we can't interpret (method calls, ternary expressions, arithmetic
// on the LHS, function calls) returns `result: 'unknown'` — the variables
// involved are still extracted so callers can present them. We prefer
// "unknown" over guessing false; M6.2's `requirements` treats unknown gates
// as needing further investigation.
//
// Sigil semantics:
//   $var  — persistent story variable, lookups go to `variables[name]`
//           (no sigil in SugarCube's runtime object; we strip it).
//   _var  — temporary per-render variable. Often absent from `variables`;
//           we return UNKNOWN so the pathfinder doesn't treat missing temp
//           vars as falsy.

'use strict';

const UNKNOWN = Symbol('UNKNOWN');

// Matches a var reference with optional dotted/bracket accessor. Used for
// both the lexer and the standalone extractor.
const VAR_RE = /[$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*/g;

/**
 * Extract unique $var / _var references from a condition string.
 * Order of first appearance is preserved.
 */
function extractVars(s) {
  if (!s) return [];
  VAR_RE.lastIndex = 0;
  const seen = new Set();
  const out = [];
  let m;
  while ((m = VAR_RE.exec(s)) !== null) {
    if (!seen.has(m[0])) { seen.add(m[0]); out.push(m[0]); }
  }
  return out;
}

/**
 * Resolve a var reference against the runtime variables object.
 * Returns UNKNOWN if the root is absent (truly don't know) or if an accessor
 * step can't be resolved statically (e.g. `$npcs[$i]` where $i is unknown).
 * Returns the actual JS value otherwise (may be null / 0 / '').
 */
function resolveVar(ref, variables) {
  if (!variables || typeof variables !== 'object') return UNKNOWN;
  const m = ref.match(/^[$_]([A-Za-z_][A-Za-z0-9_]*)((?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*)/);
  if (!m) return UNKNOWN;
  const root = m[1];
  const accessor = m[2] || '';
  if (!Object.prototype.hasOwnProperty.call(variables, root)) return UNKNOWN;
  let cur = variables[root];
  if (!accessor) return cur;
  let rest = accessor;
  while (rest.length > 0) {
    if (cur == null) return undefined;
    if (rest[0] === '.') {
      const mm = rest.match(/^\.([A-Za-z_][A-Za-z0-9_]*)/);
      if (!mm) return UNKNOWN;
      cur = cur[mm[1]];
      rest = rest.slice(mm[0].length);
    } else if (rest[0] === '[') {
      const mm = rest.match(/^\[([^\]]*)\]/);
      if (!mm) return UNKNOWN;
      const inner = mm[1].trim();
      const sMatch = inner.match(/^["']([^"']*)["']$/);
      const nMatch = inner.match(/^-?\d+$/);
      let key;
      if (sMatch) key = sMatch[1];
      else if (nMatch) key = Number(nMatch[0]);
      else {
        // Variable-indexed access like $arr[$i] — dynamic, can't resolve.
        return UNKNOWN;
      }
      cur = cur[key];
      rest = rest.slice(mm[0].length);
    } else {
      return UNKNOWN;
    }
  }
  return cur;
}

// ---------------------------------------------------------------------------
// Top-level split — respects strings and bracket depth.
// ---------------------------------------------------------------------------

/**
 * Split `s` on the first matcher that hits at top-level (depth 0, outside
 * strings). Returns array of trimmed non-empty parts; single-element array
 * if no split was found.
 *
 * `matchers` is an array of RegExps with ^ anchor that each try to match
 * at a single scan position.
 */
function topLevelSplit(s, matchers) {
  const splits = [];
  let i = 0;
  let depth = 0;
  let inStr = null;
  while (i < s.length) {
    const ch = s[i];
    const prev = i > 0 ? s[i - 1] : '';
    if (inStr) {
      if (ch === inStr && prev !== '\\') inStr = null;
      i++; continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = ch; i++; continue; }
    if (ch === '(' || ch === '[' || ch === '{') { depth++; i++; continue; }
    if (ch === ')' || ch === ']' || ch === '}') { depth--; i++; continue; }
    let matched = false;
    if (depth === 0) {
      const rest = s.slice(i);
      for (const re of matchers) {
        re.lastIndex = 0;
        const m = re.exec(rest);
        if (m && m.index === 0) {
          splits.push({ start: i, end: i + m[0].length });
          i += m[0].length;
          matched = true;
          break;
        }
      }
    }
    if (!matched) i++;
  }
  if (splits.length === 0) return [s.trim()].filter((p) => p.length > 0);
  const parts = [];
  let start = 0;
  for (const { start: b, end: e } of splits) {
    parts.push(s.slice(start, b));
    start = e;
  }
  parts.push(s.slice(start));
  return parts.map((p) => p.trim()).filter((p) => p.length > 0);
}

const OR_MATCHERS = [/^\|\|/, /^\s+or\s+/];
const AND_MATCHERS = [/^&&/, /^\s+and\s+/];

// ---------------------------------------------------------------------------
// Literal parser.
// ---------------------------------------------------------------------------

function parseLiteralOrVar(s, variables) {
  s = s.trim();
  if (!s) return UNKNOWN;
  // Strings
  const dq = s.match(/^"((?:[^"\\]|\\.)*)"$/);
  if (dq) return dq[1];
  const sq = s.match(/^'((?:[^'\\]|\\.)*)'$/);
  if (sq) return sq[1];
  // Booleans / null / undefined
  if (s === 'true') return true;
  if (s === 'false') return false;
  if (s === 'null') return null;
  if (s === 'undefined') return undefined;
  // Numbers
  if (/^-?\d+$/.test(s)) return parseInt(s, 10);
  if (/^-?\d+\.\d+$/.test(s)) return parseFloat(s);
  // Variable reference
  if (/^[$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*$/.test(s)) {
    const v = resolveVar(s, variables);
    return v;   // may be UNKNOWN
  }
  return UNKNOWN;
}

// SugarCube accepts word aliases for comparison operators. We normalize them
// before comparing.
const WORD_OPS = {
  eq: '==', neq: '!=', is: '===', isnot: '!==',
  gt: '>', lt: '<', gte: '>=', lte: '<=',
};

function compareOp(lhs, op, rhs) {
  const normalized = WORD_OPS[op] || op;
  switch (normalized) {
    case '===': return lhs === rhs;
    case '!==': return lhs !== rhs;
    case '==':  return lhs == rhs;    // eslint-disable-line eqeqeq
    case '!=':  return lhs != rhs;    // eslint-disable-line eqeqeq
    case '>':   return lhs > rhs;
    case '<':   return lhs < rhs;
    case '>=':  return lhs >= rhs;
    case '<=':  return lhs <= rhs;
    default:    return false;
  }
}

// ---------------------------------------------------------------------------
// Main evaluator.
// ---------------------------------------------------------------------------

function mergeInvolved(a, b) {
  return { ...a, ...b };
}

function scrubVal(v) {
  // Convert UNKNOWN sentinel to a serializable tag so callers can present it.
  if (v === UNKNOWN) return { __unknown: true };
  if (v === undefined) return { __undefined: true };
  return v;
}

function gatherInvolved(conditionStr, variables) {
  const involved = extractVars(conditionStr);
  const out = {};
  for (const v of involved) {
    const val = resolveVar(v, variables);
    out[v] = scrubVal(val);
  }
  return out;
}

/**
 * Evaluate a gate condition. Returns:
 *   { result: true | false | 'unknown', variables_involved: {name: value} }
 */
function evaluateGate(condition, variables) {
  const s = (condition || '').trim();
  if (!s) return { result: true, variables_involved: {} };

  const involved = gatherInvolved(s, variables || {});

  // OR split first (lowest precedence).
  const orParts = topLevelSplit(s, OR_MATCHERS);
  if (orParts.length > 1) {
    const results = orParts.map((p) => evaluateGate(p, variables));
    let allFalse = true;
    for (const r of results) {
      if (r.result === true) return { result: true, variables_involved: involved };
      if (r.result !== false) allFalse = false;
    }
    return { result: allFalse ? false : 'unknown', variables_involved: involved };
  }

  // AND split.
  const andParts = topLevelSplit(s, AND_MATCHERS);
  if (andParts.length > 1) {
    const results = andParts.map((p) => evaluateGate(p, variables));
    let allTrue = true;
    for (const r of results) {
      if (r.result === false) return { result: false, variables_involved: involved };
      if (r.result !== true) allTrue = false;
    }
    return { result: allTrue ? true : 'unknown', variables_involved: involved };
  }

  // Strip balanced outer parens.
  if (s.startsWith('(') && s.endsWith(')')) {
    let depth = 0; let ok = true;
    for (let i = 0; i < s.length; i++) {
      if (s[i] === '(') depth++;
      else if (s[i] === ')') { depth--; if (depth === 0 && i < s.length - 1) { ok = false; break; } }
    }
    if (ok) return evaluateGate(s.slice(1, -1), variables);
  }

  // Negation wrapper: !(...) or not (...).
  let negMatch = s.match(/^!\s*\(([\s\S]+)\)\s*$/);
  if (!negMatch) negMatch = s.match(/^not\s+\(([\s\S]+)\)\s*$/);
  if (negMatch) {
    const inner = evaluateGate(negMatch[1], variables);
    if (inner.result === 'unknown') return { result: 'unknown', variables_involved: involved };
    return { result: !inner.result, variables_involved: involved };
  }

  // Comparison: $var OP literal/var. Accepts both JS-style symbolic operators
  // AND SugarCube word aliases (eq, neq, is, isnot, lt, gt, lte, gte).
  const CMP_RE = /^([$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*)\s*(===|!==|==|!=|>=|<=|>|<|\b(?:eq|neq|is|isnot|lte|gte|lt|gt)\b)\s*(.+)$/;
  const cmp = s.match(CMP_RE);
  if (cmp) {
    const lhs = resolveVar(cmp[1], variables || {});
    if (lhs === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    const rhs = parseLiteralOrVar(cmp[3], variables || {});
    if (rhs === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    return { result: compareOp(lhs, cmp[2], rhs), variables_involved: involved };
  }

  // Reverse comparison: literal OP $var. Word aliases accepted here too.
  const CMP_REV_RE = /^(.+?)\s*(===|!==|==|!=|>=|<=|>|<|\b(?:eq|neq|is|isnot|lte|gte|lt|gt)\b)\s*([$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*)$/;
  const cmpRev = s.match(CMP_REV_RE);
  if (cmpRev) {
    const rhs = resolveVar(cmpRev[3], variables || {});
    if (rhs === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    const lhs = parseLiteralOrVar(cmpRev[1], variables || {});
    if (lhs === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    return { result: compareOp(lhs, cmpRev[2], rhs), variables_involved: involved };
  }

  // Bare $var truthy check.
  if (/^[$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*$/.test(s)) {
    const val = resolveVar(s, variables || {});
    if (val === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    return { result: !!val, variables_involved: involved };
  }

  // !$var or not $var (negated truthy).
  const negVar = s.match(/^(?:!|not\s+)([$_][A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\[[^\]]*\])*)$/);
  if (negVar) {
    const val = resolveVar(negVar[1], variables || {});
    if (val === UNKNOWN) return { result: 'unknown', variables_involved: involved };
    return { result: !val, variables_involved: involved };
  }

  return { result: 'unknown', variables_involved: involved };
}

module.exports = {
  evaluateGate,
  extractVars,
  resolveVar,
  UNKNOWN,
  // Exported for testing.
  topLevelSplit,
  parseLiteralOrVar,
  compareOp,
};
