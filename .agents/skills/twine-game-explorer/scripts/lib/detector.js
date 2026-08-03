// Detector — pure statistical variable + choice profiler.
//
// Phase 3 rewrite: collection and labelling are now separated. This module
// records observations; it does NOT categorize. `lib/labeler.js` reads the
// serialized profile at report-time and applies semantic labels there.
//
// What this records per variable:
//   - type samples (which JS types this var has held)
//   - value range / sample distribution (for numbers and strings)
//   - mutation frequency (how many times it changed across the session)
//   - co-change edges (which OTHER vars changed at the same click)
//   - passages it was seen on (for ubiquity detection)
//
// What it records globally:
//   - passages visited + visit counts
//   - choice records (timestamp, passage, options, picked, prices)
//   - mutation events (bounded list for labeller to slice by category)
//   - prefix clusters (names sharing a leading token — candidate entity groups)

'use strict';

const MUTATION_LOG_CAP = 5000;
const NUM_VALUES_PER_VAR_CAP = 500;
const STRING_VALUES_PER_VAR_CAP = 50;

class Detector {
  constructor() {
    this.vars = new Map();           // name -> VarProfile
    this.passages = new Map();       // passage -> { first_ts, visit_count }
    this.choices = [];               // { ts, passage, classification, options, picked, prices, at_state_hash }
    this.coChange = new Map();       // "a||b" -> count (sorted key)
    this.mutations = [];             // bounded event log: {ts, passage, var, before, after}
    this.startTs = Date.now();
  }

  /** Flatten nested object to dotted-path map. Safe against cycles. */
  _flatten(obj, prefix = '', depth = 0, out = {}) {
    if (depth > 4 || !obj || typeof obj !== 'object') return out;
    for (const [k, v] of Object.entries(obj)) {
      const name = prefix ? `${prefix}.${k}` : k;
      if (name.length > 120) continue;
      if (v && typeof v === 'object' && !Array.isArray(v)) {
        this._flatten(v, name, depth + 1, out);
      } else {
        out[name] = v;
      }
    }
    return out;
  }

  _ensureVar(name, ts) {
    if (!this.vars.has(name)) {
      this.vars.set(name, {
        type_samples: new Set(),
        number_values: [],
        string_values: new Set(),
        bool_values: new Set(),
        mutation_count: 0,
        first_ts: ts,
        last_ts: ts,
        passages_seen_on: new Set(),
      });
    }
    return this.vars.get(name);
  }

  /** Record one state snapshot + optional diff from previous. */
  observeState({ state_hash, passage, variables, diff, timestamp }) {
    const ts = timestamp || Date.now();

    if (passage) {
      if (!this.passages.has(passage)) this.passages.set(passage, { first_ts: ts, visit_count: 0 });
      this.passages.get(passage).visit_count++;
    }

    const flat = this._flatten(variables || {});
    for (const [name, value] of Object.entries(flat)) {
      const v = this._ensureVar(name, ts);
      v.type_samples.add(typeof value);
      v.last_ts = ts;
      if (passage) v.passages_seen_on.add(passage);
      if (typeof value === 'number' && Number.isFinite(value)) {
        if (v.number_values.length < NUM_VALUES_PER_VAR_CAP) v.number_values.push(value);
      } else if (typeof value === 'string') {
        if (v.string_values.size < STRING_VALUES_PER_VAR_CAP) v.string_values.add(value.slice(0, 120));
      } else if (typeof value === 'boolean') {
        v.bool_values.add(value);
      }
    }

    if (diff) {
      const changedNames = Object.keys(diff.changed || {});
      // Mutation counts
      for (const name of changedNames) {
        if (this.vars.has(name)) this.vars.get(name).mutation_count++;
      }
      // Bounded mutation log (for labeler to slice by semantic category later)
      for (const [name, delta] of Object.entries(diff.changed || {})) {
        if (this.mutations.length >= MUTATION_LOG_CAP) break;
        this.mutations.push({
          ts, passage, state_hash, var: name,
          before: delta.before, after: delta.after,
        });
      }
      // Co-change edges (which vars moved in the same click)
      for (let i = 0; i < changedNames.length; i++) {
        for (let j = i + 1; j < changedNames.length; j++) {
          const key = [changedNames[i], changedNames[j]].sort().join('||');
          this.coChange.set(key, (this.coChange.get(key) || 0) + 1);
        }
      }
    }
  }

  /** Record one choice event — options + picked + prices + classification. */
  observeChoice({ passage, classification, options, picked, prices, at_state_hash, timestamp }) {
    this.choices.push({
      ts: timestamp || Date.now(),
      passage,
      classification: classification || 'unknown',
      options: options || [],
      picked,
      prices: prices || null,
      at_state_hash,
    });
  }

  /** Emit the statistical profile — no labels, just evidence. */
  serialize() {
    const variables = {};
    for (const [name, v] of this.vars.entries()) {
      const profile = {
        types: Array.from(v.type_samples),
        mutation_count: v.mutation_count,
        first_ts: v.first_ts,
        last_ts: v.last_ts,
        passages_seen_on_count: v.passages_seen_on.size,
      };
      if (v.number_values.length) {
        const nums = v.number_values;
        const unique = new Set(nums);
        profile.number_stats = {
          count: nums.length,
          unique_count: unique.size,
          min: Math.min(...nums),
          max: Math.max(...nums),
          first: nums[0],
          last: nums[nums.length - 1],
          is_monotonic_increasing: nums.every((x, i) => i === 0 || x >= nums[i - 1]),
          is_boolean_like: unique.size <= 2,
        };
      }
      if (v.string_values.size) {
        profile.string_samples = Array.from(v.string_values).slice(0, 20);
      }
      if (v.bool_values.size) {
        profile.bool_values = Array.from(v.bool_values);
      }
      variables[name] = profile;
    }

    // Prefix clusters — variables with shared leading token (2+ letters)
    const prefixes = new Map();
    for (const name of this.vars.keys()) {
      const base = name.split('.').pop();
      const m = base.match(/^([a-z]{2,})/i);
      if (!m) continue;
      const p = m[1].toLowerCase();
      if (!prefixes.has(p)) prefixes.set(p, []);
      prefixes.get(p).push(name);
    }
    const prefix_clusters = {};
    for (const [p, names] of prefixes.entries()) {
      if (names.length >= 2) prefix_clusters[p] = names;
    }

    // Co-change edges observed 2+ times
    const co_change = {};
    for (const [key, count] of this.coChange.entries()) {
      if (count >= 2) co_change[key] = count;
    }

    const passages = {};
    for (const [p, e] of this.passages.entries()) {
      passages[p] = { first_ts: e.first_ts, visit_count: e.visit_count };
    }

    const choices = {
      total: this.choices.length,
      by_classification: this.choices.reduce((acc, c) => {
        const cl = c.classification || 'unknown';
        acc[cl] = (acc[cl] || 0) + 1;
        return acc;
      }, {}),
      price_observations: this.choices.flatMap((c) => {
        if (!c.prices) return [];
        return c.prices
          .map((p, i) => p != null ? { passage: c.passage, price: p, label: (c.options || [])[i] } : null)
          .filter(Boolean);
      }),
      recent: this.choices.slice(-50),
    };

    return {
      generated_at: new Date().toISOString(),
      variables,
      prefix_clusters,
      co_change,
      passages,
      choices,
      mutations: this.mutations.slice(-500), // cap serialized output
    };
  }
}

module.exports = { Detector };
