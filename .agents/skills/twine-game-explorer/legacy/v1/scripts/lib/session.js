// Session metadata — one record per run. Appends to sessions/ directory.

'use strict';

const fs = require('fs');
const path = require('path');

class SessionTracker {
  constructor(sessionsDir) {
    this.dir = sessionsDir;
    fs.mkdirSync(this.dir, { recursive: true });
    // Find next session number
    const existing = fs.readdirSync(this.dir).filter((f) => /^session_\d+\.json$/.test(f));
    const nums = existing.map((f) => Number(f.match(/\d+/)[0]));
    this.id = (nums.length ? Math.max(...nums) : 0) + 1;
    this.record = {
      session_id: this.id,
      start_ts: new Date().toISOString(),
      start_epoch_ms: Date.now(),
      end_ts: null,
      duration_s: 0,
      clicks: 0,
      choices_explored: 0,
      arrow_advances: 0,
      unique_states_seen: 0,
      new_unique_states: 0,
      frontier_size_start: 0,
      frontier_size_end: 0,
      reached_endings: [],
      completed: false,
      notes: [],
    };
  }

  recordClick() { this.record.clicks++; }
  recordChoice() { this.record.choices_explored++; }
  recordArrow() { this.record.arrow_advances++; }
  addNote(n) { this.record.notes.push(n); }
  setFrontierStart(n) { this.record.frontier_size_start = n; }
  setFrontierEnd(n) { this.record.frontier_size_end = n; }
  incNewUniqueState() { this.record.new_unique_states++; }
  setUniqueStates(n) { this.record.unique_states_seen = n; }
  recordEnding(passage) { this.record.reached_endings.push(passage); this.record.completed = true; }

  /** Write (idempotent; safe to call multiple times — keeps latest snapshot). */
  flush() {
    this.record.end_ts = new Date().toISOString();
    this.record.duration_s = Math.round((Date.now() - this.record.start_epoch_ms) / 1000);
    const file = path.join(this.dir, `session_${String(this.id).padStart(3, '0')}.json`);
    fs.writeFileSync(file, JSON.stringify(this.record, null, 2));
    return file;
  }
}

/** Aggregate all session files into a summary. */
function aggregateSessions(sessionsDir) {
  if (!fs.existsSync(sessionsDir)) return { sessions: [], totals: {} };
  const files = fs.readdirSync(sessionsDir).filter((f) => /^session_\d+\.json$/.test(f)).sort();
  const sessions = files.map((f) => JSON.parse(fs.readFileSync(path.join(sessionsDir, f), 'utf8')));
  const totals = {
    session_count: sessions.length,
    total_duration_s: sessions.reduce((s, r) => s + (r.duration_s || 0), 0),
    total_clicks: sessions.reduce((s, r) => s + (r.clicks || 0), 0),
    total_choices: sessions.reduce((s, r) => s + (r.choices_explored || 0), 0),
    any_completed: sessions.some((r) => r.completed),
  };
  return { sessions, totals };
}

module.exports = { SessionTracker, aggregateSessions };
