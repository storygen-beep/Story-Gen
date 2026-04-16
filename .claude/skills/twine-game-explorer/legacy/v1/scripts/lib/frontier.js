// Persistent frontier queue for DFS exploration.
//
// An entry in the frontier is:
//   { state_hash, choices_left: [idx, idx, ...], snapshot, depth, added_at }
//
// - state_hash: identity of the state where these choices sit
// - choices_left: choice indices we haven't yet explored from this state
// - snapshot: opaque engine-state blob (from engine.snapshot) to restore from
// - depth: how deep we are in the choice tree
// - added_at: timestamp
//
// Persistent: written to frontier.jsonl as an append-only log, then compacted
// on load.

'use strict';

const fs = require('fs');
const path = require('path');

class Frontier {
  constructor(filePath) {
    this.filePath = filePath;
    this.entries = [];
    this._load();
  }

  _load() {
    if (!fs.existsSync(this.filePath)) {
      this.entries = [];
      return;
    }
    const raw = fs.readFileSync(this.filePath, 'utf8');
    const lines = raw.split('\n').filter(Boolean);
    // Compact: later "pop:<hash>" records remove earlier "push:<hash>" with matching hash+depth
    const byKey = new Map();
    let tombstones = new Set();
    for (const line of lines) {
      try {
        const r = JSON.parse(line);
        if (r.op === 'push') {
          byKey.set(r.entry.state_hash + ':' + r.entry.depth + ':' + JSON.stringify(r.entry.choices_left), r.entry);
        } else if (r.op === 'pop') {
          tombstones.add(r.key);
        } else if (r.op === 'replace') {
          byKey.set(r.key, r.entry);
        }
      } catch (e) { /* skip malformed */ }
    }
    this.entries = [...byKey.entries()].filter(([k]) => !tombstones.has(k)).map(([, v]) => v);
  }

  _append(rec) {
    fs.appendFileSync(this.filePath, JSON.stringify(rec) + '\n');
  }

  push(entry) {
    // Dedup: if same state_hash + same choices_left is already queued, skip
    const key = entry.state_hash + ':' + entry.depth + ':' + JSON.stringify(entry.choices_left);
    if (this.entries.some((e) => e.state_hash === entry.state_hash && e.depth === entry.depth)) return false;
    this.entries.push(entry);
    this._append({ op: 'push', entry, key });
    return true;
  }

  /** Pop the most recently added entry (LIFO = DFS). */
  pop() {
    if (!this.entries.length) return null;
    const entry = this.entries.pop();
    const key = entry.state_hash + ':' + entry.depth + ':' + JSON.stringify(entry.choices_left);
    this._append({ op: 'pop', key });
    return entry;
  }

  /** Update entry in-place (e.g. after removing one consumed choice from choices_left). */
  replace(oldKey, newEntry) {
    const idx = this.entries.findIndex((e) => (e.state_hash + ':' + e.depth + ':' + JSON.stringify(e.choices_left)) === oldKey);
    if (idx >= 0) this.entries[idx] = newEntry;
    const newKey = newEntry.state_hash + ':' + newEntry.depth + ':' + JSON.stringify(newEntry.choices_left);
    this._append({ op: 'replace', key: newKey, entry: newEntry });
  }

  size() { return this.entries.length; }

  summary() {
    return {
      size: this.entries.length,
      deepest: this.entries.reduce((m, e) => Math.max(m, e.depth), 0),
      oldest_added_at: this.entries.reduce((m, e) => Math.min(m, e.added_at || Infinity), Infinity),
    };
  }
}

module.exports = { Frontier };
