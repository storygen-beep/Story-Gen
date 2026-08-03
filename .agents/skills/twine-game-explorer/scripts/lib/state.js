// State snapshot hashing + delta tracking.
//
// We hash {passage, sorted(variables)} to get a stable state identity.
// The hash is the dedup key for "have I seen this exact state before?"

'use strict';

const crypto = require('crypto');

/**
 * Produce a stable string form of the state for hashing.
 * Sorts keys so object-key order doesn't break dedup.
 */
function canonicalize(state) {
  const { passage, variables } = state;
  const seen = new WeakSet();
  const sortObj = (x) => {
    if (x && typeof x === 'object') {
      if (seen.has(x)) return '[circular]';
      seen.add(x);
      if (Array.isArray(x)) return x.map(sortObj);
      const out = {};
      for (const k of Object.keys(x).sort()) out[k] = sortObj(x[k]);
      return out;
    }
    return x;
  };
  return JSON.stringify({ passage: passage || null, variables: sortObj(variables || {}) });
}

function hashState(state) {
  const canon = canonicalize(state);
  return crypto.createHash('sha1').update(canon).digest('hex').slice(0, 16);
}

/**
 * Diff two variable objects: { added, removed, changed } where each
 * is a map of var-path -> {before, after}.
 * Used to detect which variables a single click mutated.
 */
function diffVariables(before, after) {
  const added = {}, removed = {}, changed = {};
  const walk = (b, a, path) => {
    const bk = b && typeof b === 'object' ? Object.keys(b) : [];
    const ak = a && typeof a === 'object' ? Object.keys(a) : [];
    const all = new Set([...bk, ...ak]);
    for (const k of all) {
      const p = path ? path + '.' + k : k;
      const bv = b ? b[k] : undefined;
      const av = a ? a[k] : undefined;
      if (bv === undefined && av !== undefined) {
        added[p] = { after: av };
      } else if (bv !== undefined && av === undefined) {
        removed[p] = { before: bv };
      } else if (typeof bv === 'object' && typeof av === 'object' && bv !== null && av !== null) {
        walk(bv, av, p);
      } else if (JSON.stringify(bv) !== JSON.stringify(av)) {
        changed[p] = { before: bv, after: av };
      }
    }
  };
  walk(before || {}, after || {}, '');
  return { added, removed, changed };
}

/** Compact human summary of a diff. */
function summarizeDiff(diff) {
  const parts = [];
  for (const [k, v] of Object.entries(diff.changed)) {
    parts.push(`${k}: ${JSON.stringify(v.before)} → ${JSON.stringify(v.after)}`);
  }
  for (const k of Object.keys(diff.added)) parts.push(`+${k}`);
  for (const k of Object.keys(diff.removed)) parts.push(`-${k}`);
  return parts.join('; ');
}

module.exports = { canonicalize, hashState, diffVariables, summarizeDiff };
