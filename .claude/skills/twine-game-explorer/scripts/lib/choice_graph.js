// Dynamic choice graph — every observed (from_passage, clicked_text, to_passage)
// triple, aggregated across every play_log entry in the session history.
//
// Where the data comes from:
//   - `play_log.jsonl`      : one line per command. Click entries carry
//                              `clicked_text`, `passage` (= POST-click passage),
//                              `state_hash` (= POST-click hash), `state_changed`.
//                              The PRE-click passage we compute by walking the
//                              log chronologically and tracking prev_passage.
//   - `state_timeline.jsonl`: one line per observeCurrentState call. Carries
//                              `hash`, `passage`, `kind`, and (M1 addition)
//                              `diff_full` with `{changed, added, removed}` of
//                              full before/after variable values.
//   - `initial_state.json`  : the passage+hash we started from (before Phase 0a).
//
// Join strategy: walk play_log forward; for each click, the edge is
//   (prev_passage, clicked_text) -> entry.passage
// and we pull the effect from the timeline entry whose `hash` matches
// entry.state_hash AND whose timestamp is closest to the click. Timeline is
// append-only so the match is effectively "the nearest non-earlier entry".
//
// Aggregation shape (per unique edge tuple):
//   {
//     from, clicked_text, to,
//     observation_count,
//     classifications: { branch: N, advance: M, ... },
//     first_observed_ts, last_observed_ts,
//     same_state: boolean (true if to === from in every observation),
//     effect_aggregate: {
//       <var_name>: {
//         count, changes_count,
//         before_values: [...], after_values: [...],
//         numeric_stats: { min_delta, max_delta, mean_delta } | null,
//         always_same_delta: boolean
//       }
//     }
//   }
//
// Non-click state-advancing commands (`keys`, `eval`, `reload`, `restore`,
// frontier `pop`) are recorded separately as `synthetic_edges` so downstream
// analysis can see Claude's out-of-band nudges without mixing them into the
// player-choice graph.

'use strict';

const fs = require('fs');

const STATE_ADVANCING_CMDS = new Set(['keys', 'eval', 'reload', 'restore', 'pop']);
const NO_STATE_CMDS = new Set(['peek', 'dom', 'snap', 'note', 'observe', 'wait', 'status', 'regions', 'frontier']);
// Note: 'frontier' is mixed — `push`/`list` don't change state, `pop` does. We
// special-case pop by inspecting args.

function readJsonl(path) {
  if (!fs.existsSync(path)) return [];
  const out = [];
  const raw = fs.readFileSync(path, 'utf8');
  for (const line of raw.split('\n')) {
    if (!line.trim()) continue;
    try { out.push(JSON.parse(line)); } catch (e) { /* skip malformed */ }
  }
  return out;
}

function readJson(path) {
  if (!fs.existsSync(path)) return null;
  try { return JSON.parse(fs.readFileSync(path, 'utf8')); } catch (e) { return null; }
}

// Index timeline entries by hash. Many entries can share a hash (we revisit
// states); we keep all so match-by-timestamp picks the best one later.
function indexTimelineByHash(entries) {
  const ix = new Map();
  for (const e of entries) {
    const h = e.hash;
    if (!h) continue;
    if (!ix.has(h)) ix.set(h, []);
    ix.get(h).push(e);
  }
  return ix;
}

// Parse an ISO timestamp (play_log) or numeric ts (timeline) to milliseconds.
function toMs(ts) {
  if (ts == null) return null;
  if (typeof ts === 'number') return ts;
  const n = Date.parse(ts);
  return Number.isFinite(n) ? n : null;
}

// Find the timeline entry whose hash matches and whose ts is closest (within
// a small tolerance) to the click's ts. Falls back to any-hash-match.
function findTimelineMatch(timelineByHash, targetHash, targetTs) {
  if (!targetHash) return null;
  const bucket = timelineByHash.get(targetHash);
  if (!bucket || !bucket.length) return null;
  if (targetTs == null) return bucket[0];
  let best = bucket[0];
  let bestDelta = Math.abs((bucket[0].ts || 0) - targetTs);
  for (const e of bucket) {
    const d = Math.abs((e.ts || 0) - targetTs);
    if (d < bestDelta) { bestDelta = d; best = e; }
  }
  return best;
}

// Fold a single diff into an edge's effect_aggregate.
function recordEffect(agg, diffFull) {
  if (!diffFull) return;
  const consider = (map, kind) => {
    for (const [name, delta] of Object.entries(map || {})) {
      if (!agg[name]) {
        agg[name] = {
          count: 0, changes_count: 0,
          before_values: [], after_values: [],
          numeric_deltas: [],
          kinds: {},
        };
      }
      const a = agg[name];
      a.count++;
      a.kinds[kind] = (a.kinds[kind] || 0) + 1;
      const before = delta.before;
      const after = delta.after;
      // Keep bounded samples to avoid unbounded blow-up on verbose vars.
      if (a.before_values.length < 50) a.before_values.push(before);
      if (a.after_values.length < 50) a.after_values.push(after);
      if (JSON.stringify(before) !== JSON.stringify(after)) a.changes_count++;
      if (typeof before === 'number' && typeof after === 'number' && Number.isFinite(before) && Number.isFinite(after)) {
        a.numeric_deltas.push(after - before);
      }
    }
  };
  consider(diffFull.changed, 'changed');
  consider(diffFull.added, 'added');
  consider(diffFull.removed, 'removed');
}

// Finalize an effect_aggregate: compute numeric stats, drop scratch fields.
function finalizeEffect(agg) {
  const out = {};
  for (const [name, a] of Object.entries(agg)) {
    const rec = {
      count: a.count,
      changes_count: a.changes_count,
      kinds: a.kinds,
      before_values: a.before_values,
      after_values: a.after_values,
    };
    if (a.numeric_deltas.length) {
      const deltas = a.numeric_deltas;
      const min = Math.min(...deltas);
      const max = Math.max(...deltas);
      const sum = deltas.reduce((s, x) => s + x, 0);
      const mean = sum / deltas.length;
      const allEqual = deltas.every((d) => d === deltas[0]);
      rec.numeric_stats = {
        sample_count: deltas.length,
        min_delta: min,
        max_delta: max,
        mean_delta: Number(mean.toFixed(4)),
        always_same_delta: allEqual,
      };
    } else {
      rec.numeric_stats = null;
    }
    out[name] = rec;
  }
  return out;
}

/**
 * Build the choice graph from on-disk session artifacts. Accepts a `dirs`
 * object (same shape live.js uses) so we can decouple path conventions.
 *
 * @param {object} dirs - { playLog, timeline, initialState }
 * @param {object} staticGraphIndex - optional { byFromAndTo: Map(`from||to` -> [edgeIdx]), edges }
 *                                    used to cross-reference observed edges with the static graph
 * @returns {object} JSON-serializable choice graph
 */
function buildChoiceGraph(dirs, staticGraphIndex = null) {
  const playLog = readJsonl(dirs.playLog);
  const timeline = readJsonl(dirs.timeline);
  const initial = readJson(dirs.initialState) || {};
  const timelineByHash = indexTimelineByHash(timeline);

  // Walk play_log forward, tracking prev_passage. Start from whatever passage
  // the first valid entry lands on; initial_state is the pre-Phase-0a anchor.
  let prevPassage = initial.passage || null;

  const edgeMap = new Map();       // key: from|clicked|to  ->  aggregated record
  const syntheticMap = new Map();  // key: cmd|prev|to      ->  aggregated record (for keys/eval/reload/restore/pop)
  const orphanClicks = [];         // click entries we couldn't resolve (no prev_passage)

  const keyForEdge = (from, clicked, to) => `${from || '∅'}|${clicked || '∅'}|${to || '∅'}`;

  for (let i = 0; i < playLog.length; i++) {
    const e = playLog[i];
    const cmd = e.cmd;
    const clickText = e.clicked_text || null;
    const postPassage = e.passage != null ? e.passage : null;
    const postHash = e.state_hash || null;
    const ts = toMs(e.ts);

    if (cmd === 'click' && e.ok) {
      const from = prevPassage;
      const to = postPassage;
      if (from == null) {
        orphanClicks.push({ index: i, ts: e.ts, clicked_text: clickText, to });
      } else {
        const key = keyForEdge(from, clickText, to);
        if (!edgeMap.has(key)) {
          edgeMap.set(key, {
            from, clicked_text: clickText, to,
            observation_count: 0,
            classifications: {},
            first_observed_ts: ts,
            last_observed_ts: ts,
            same_state_hits: 0,
            effect_scratch: {},
          });
        }
        const agg = edgeMap.get(key);
        agg.observation_count++;
        agg.last_observed_ts = ts;
        const tm = findTimelineMatch(timelineByHash, postHash, ts);
        const kind = (tm && tm.kind) || 'click';
        agg.classifications[kind] = (agg.classifications[kind] || 0) + 1;
        if (e.state_changed === false) agg.same_state_hits++;
        recordEffect(agg.effect_scratch, tm && tm.diff_full);
      }
      // After a click, prev advances to the post-click passage.
      if (postPassage) prevPassage = postPassage;
      continue;
    }

    // State-advancing non-click commands — logged as synthetic edges so we
    // don't fake them as player choices. Frontier pop is special.
    const isFrontierPop = cmd === 'frontier' && e.args && Array.isArray(e.args.positional) && e.args.positional[0] === 'pop';
    const cmdKey = isFrontierPop ? 'pop' : cmd;
    if (STATE_ADVANCING_CMDS.has(cmdKey) && e.ok && postPassage) {
      const from = prevPassage;
      const key = `${cmdKey}|${from || '∅'}|${postPassage}`;
      if (!syntheticMap.has(key)) {
        syntheticMap.set(key, {
          cmd: cmdKey, from, to: postPassage,
          observation_count: 0,
          first_observed_ts: ts,
          last_observed_ts: ts,
          effect_scratch: {},
        });
      }
      const s = syntheticMap.get(key);
      s.observation_count++;
      s.last_observed_ts = ts;
      const tm = findTimelineMatch(timelineByHash, postHash, ts);
      recordEffect(s.effect_scratch, tm && tm.diff_full);
      if (postPassage) prevPassage = postPassage;
      continue;
    }

    // No-state commands don't move prev_passage.
    if (postPassage) prevPassage = postPassage; // refresh even for peeks
  }

  const observedEdges = [];
  for (const [, rec] of edgeMap) {
    observedEdges.push({
      from: rec.from,
      clicked_text: rec.clicked_text,
      to: rec.to,
      observation_count: rec.observation_count,
      classifications: rec.classifications,
      first_observed_ts: rec.first_observed_ts,
      last_observed_ts: rec.last_observed_ts,
      same_state_hits: rec.same_state_hits,
      is_self_loop: rec.from === rec.to,
      effect_aggregate: finalizeEffect(rec.effect_scratch),
    });
  }

  const syntheticEdges = [];
  for (const [, rec] of syntheticMap) {
    syntheticEdges.push({
      cmd: rec.cmd,
      from: rec.from,
      to: rec.to,
      observation_count: rec.observation_count,
      first_observed_ts: rec.first_observed_ts,
      last_observed_ts: rec.last_observed_ts,
      effect_aggregate: finalizeEffect(rec.effect_scratch),
    });
  }

  // Cross-reference coverage against the static graph if provided.
  let coverage = null;
  if (staticGraphIndex && staticGraphIndex.edges && staticGraphIndex.byFromTo) {
    const observedPairs = new Set();
    for (const oe of observedEdges) observedPairs.add(`${oe.from}|${oe.to}`);
    let observedStaticCount = 0;
    const observedStaticEdges = [];
    const unobservedStaticEdges = [];
    for (let idx = 0; idx < staticGraphIndex.edges.length; idx++) {
      const se = staticGraphIndex.edges[idx];
      const pair = `${se.from}|${se.to}`;
      if (observedPairs.has(pair)) {
        observedStaticCount++;
        observedStaticEdges.push(idx);
      } else {
        unobservedStaticEdges.push(idx);
      }
    }
    coverage = {
      static_edges_total: staticGraphIndex.edges.length,
      observed_static_edges: observedStaticCount,
      unobserved_static_edges: unobservedStaticEdges.length,
      coverage_ratio: staticGraphIndex.edges.length
        ? Number((observedStaticCount / staticGraphIndex.edges.length).toFixed(4))
        : null,
      observed_only_edges: observedEdges.filter((e) => {
        const key = `${e.from}|${e.to}`;
        return !staticGraphIndex.byFromTo.has(key);
      }).length,
    };
  }

  return {
    generated_at: new Date().toISOString(),
    total_observed_edges: observedEdges.length,
    total_synthetic_edges: syntheticEdges.length,
    total_play_log_entries: playLog.length,
    total_timeline_entries: timeline.length,
    initial_passage: initial.passage || null,
    orphan_clicks: orphanClicks,
    observed_edges: observedEdges.sort((a, b) => b.observation_count - a.observation_count),
    synthetic_edges: syntheticEdges,
    coverage,
  };
}

/** Build the lookup index the cross-reference pass needs. */
function indexStaticGraph(staticGraph) {
  if (!staticGraph || !Array.isArray(staticGraph.edges)) return null;
  const byFromTo = new Map();
  for (let i = 0; i < staticGraph.edges.length; i++) {
    const e = staticGraph.edges[i];
    const key = `${e.from}|${e.to}`;
    if (!byFromTo.has(key)) byFromTo.set(key, []);
    byFromTo.get(key).push(i);
  }
  return { edges: staticGraph.edges, byFromTo };
}

module.exports = { buildChoiceGraph, indexStaticGraph };
