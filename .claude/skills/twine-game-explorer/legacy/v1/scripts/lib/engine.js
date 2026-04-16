// Engine detection + state marshal / unmarshal.
//
// Twine games run on a small set of engines. Each exposes state differently.
// We detect which one is running and provide a uniform (detect, snapshot, restore, readVariables)
// interface to the caller.
//
// Engines we support:
//   - SugarCube v2 (most common, including BTF): SugarCube.State.*
//   - Harlowe: harlowe.State or similar
//   - Chapbook: engine.state
//   - Unknown: path-replay fallback (record click sequence, restart, replay)

'use strict';

/**
 * Run inside the game's frame (browser context) to detect engine + pull state.
 * Returns: { engine, passage, variables, turns, canMarshal }
 */
async function introspect(frame) {
  return await frame.evaluate(() => {
    // Helper to safely JSON-stringify-then-parse a structure, to strip non-serialisable
    const deep = (o) => {
      try {
        return JSON.parse(JSON.stringify(o, (k, v) => {
          if (typeof v === 'function') return undefined;
          if (v instanceof Date) return { __type: 'Date', v: v.toISOString() };
          if (v instanceof Map) return { __type: 'Map', v: Array.from(v.entries()) };
          if (v instanceof Set) return { __type: 'Set', v: Array.from(v.values()) };
          return v;
        }));
      } catch (e) { return { __error: String(e) }; }
    };

    // --- SugarCube ---
    if (typeof SugarCube !== 'undefined' && SugarCube && SugarCube.State) {
      const S = SugarCube.State;
      const variables = deep(S.variables || {});
      const passage = S.passage || (S.active && S.active.title) || null;
      const turns = typeof S.turns === 'number' ? S.turns : (S.length || null);
      return {
        engine: 'sugarcube',
        version: (SugarCube.version && SugarCube.version.short) || null,
        passage, variables, turns,
        canMarshal: typeof S.marshalForSave === 'function',
      };
    }

    // --- Harlowe ---
    // Harlowe does not expose a clean global by default; the state sits inside the engine.
    // Look for the State structure commonly attached to window.Harlowe or window.State.
    if (typeof Harlowe !== 'undefined' && Harlowe && Harlowe.State) {
      const s = Harlowe.State;
      return {
        engine: 'harlowe',
        version: null,
        passage: (s.passage && s.passage.name) || null,
        variables: deep(s.variables || {}),
        turns: (s.timeline && s.timeline.length) || null,
        canMarshal: false, // Harlowe's timeline is harder to round-trip
      };
    }

    // --- Chapbook ---
    if (typeof engine !== 'undefined' && engine && engine.state && typeof engine.state.get === 'function') {
      return {
        engine: 'chapbook',
        version: null,
        passage: (typeof engine.story !== 'undefined' && engine.story.passage) || null,
        variables: deep(engine.state.all ? engine.state.all() : {}),
        turns: null,
        canMarshal: false,
      };
    }

    // Unknown engine
    return {
      engine: 'unknown',
      version: null,
      passage: null,
      variables: {},
      turns: null,
      canMarshal: false,
    };
  });
}

/**
 * Snapshot full engine state (for later restore).
 * Returns an opaque blob (object) that restore() can consume.
 * For SugarCube, uses the engine's own marshal. For others, fall back to path-replay:
 *   the caller should pass in `pathSoFar` (array of click descriptors) so we can
 *   record it as the restore primitive.
 */
async function snapshot(frame, { pathSoFar = [] } = {}) {
  const info = await introspect(frame);
  if (info.engine === 'sugarcube' && info.canMarshal) {
    const blob = await frame.evaluate(() => {
      try {
        // marshalForSave returns a plain object in SugarCube v2
        return { ok: true, data: SugarCube.State.marshalForSave() };
      } catch (e) { return { ok: false, error: String(e) }; }
    });
    if (blob.ok) {
      return { engine: 'sugarcube', mode: 'marshal', blob: blob.data, info };
    }
  }
  // Fallback: record path-replay snapshot (just the path)
  return { engine: info.engine, mode: 'path-replay', path: pathSoFar.slice(), info };
}

/**
 * Restore state from a snapshot. Requires page + frame for path-replay mode.
 * path-replay mode needs a `replayer` callback: async ({clickFn}) => void
 * that replays each step of snapshot.path through the UI. The explorer provides this.
 */
async function restore(page, frame, snap, { replayer = null, reloadUrl = null } = {}) {
  if (snap.mode === 'marshal' && snap.engine === 'sugarcube') {
    const result = await frame.evaluate((data) => {
      try {
        if (typeof SugarCube === 'undefined' || !SugarCube.State || typeof SugarCube.State.unmarshalFromSave !== 'function') {
          return { ok: false, error: 'unmarshalFromSave missing' };
        }
        SugarCube.State.unmarshalFromSave(data);
        return { ok: true };
      } catch (e) { return { ok: false, error: String(e) }; }
    }, snap.blob);
    if (result.ok) return { ok: true, method: 'marshal' };
    // fallthrough if unmarshal failed
  }

  if (snap.mode === 'path-replay') {
    if (!replayer || !reloadUrl) return { ok: false, error: 'path-replay requires replayer + reloadUrl' };
    await page.goto(reloadUrl, { waitUntil: 'domcontentloaded' }).catch(() => {});
    await replayer(snap.path);
    return { ok: true, method: 'path-replay' };
  }

  return { ok: false, error: 'no restore path available for snapshot mode ' + snap.mode };
}

/**
 * Read just the variables (lightweight; called every tick).
 */
async function readVariables(frame) {
  try {
    const info = await introspect(frame);
    return info;
  } catch (e) { return { engine: 'error', error: String(e) }; }
}

module.exports = { introspect, snapshot, restore, readVariables };
