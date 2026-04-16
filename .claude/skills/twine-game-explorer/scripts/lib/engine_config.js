// Engine configuration dump — one-shot snapshot of everything the engine
// exposes about itself that a comparison pipeline would want to know:
// passage-start name, save identity, history caps, user-facing settings,
// version, RNG state, save-slot metadata, and Twine-story identity (IFID).
//
// This runs once at daemon init, before Phase 0a mutates anything. The dump
// is the engine's *declared* configuration — separate from the per-turn
// variable state captured by scene_bodies / state_timeline.
//
// Out-of-scope by design:
//   - State.history array contents — each turn is massive and we already
//     capture per-turn state via observeCurrentState. We record length +
//     first-entry shape only.
//   - Save-slot blob contents — the full marshaled state is redundant with
//     scene_bodies. We record each slot's { title, date, description, id }.
//   - <img>/<video> asset URLs (user constraint) — not emitted anywhere.
//
// Engines:
//   - SugarCube v2 : full dump
//   - Harlowe      : best-effort (much of SugarCube's API doesn't exist)
//   - Chapbook     : minimal
//   - unknown      : returns { engine: 'unknown', error: ... }

'use strict';

/**
 * Dump engine configuration. Runs inside the game frame.
 * Returns a JSON-serializable object. Never throws — all enumeration is
 * wrapped in per-field try/catch so a single broken getter can't nuke the
 * whole artifact.
 */
async function dumpEngineConfig(frame) {
  return await frame.evaluate(() => {
    // ------------------------------------------------------------------
    // safeValue: depth-limited, cycle-safe, function-stripping walker.
    // Returns a value JSON.stringify can round-trip losslessly.
    // ------------------------------------------------------------------
    const MAX_DEPTH = 5;
    const ARRAY_CAP = 200;
    const KEYS_CAP = 400;
    const safeValue = (v, depth, seen) => {
      if (depth > MAX_DEPTH) return '<max_depth>';
      if (v === null || v === undefined) return v;
      const t = typeof v;
      if (t === 'function') return '<function>';
      if (t === 'string') return v;
      if (t === 'number' || t === 'boolean') return v;
      if (t === 'bigint') return String(v);
      if (t === 'symbol') return v.toString();
      if (v instanceof Date) return { __type: 'Date', v: v.toISOString() };
      if (v instanceof RegExp) return { __type: 'RegExp', v: v.toString() };
      if (t === 'object') {
        if (seen.has(v)) return '<circular>';
        seen.add(v);
        if (Array.isArray(v)) {
          const trimmed = v.length > ARRAY_CAP ? v.slice(0, ARRAY_CAP) : v;
          const out = trimmed.map((x) => {
            try { return safeValue(x, depth + 1, seen); }
            catch (e) { return '<error:' + String(e).slice(0, 80) + '>'; }
          });
          if (v.length > ARRAY_CAP) out.push('<truncated ' + (v.length - ARRAY_CAP) + ' more>');
          return out;
        }
        if (v instanceof Map) {
          const entries = Array.from(v.entries()).slice(0, ARRAY_CAP);
          return { __type: 'Map', entries: entries.map(([k, val]) => [safeValue(k, depth + 1, seen), safeValue(val, depth + 1, seen)]) };
        }
        if (v instanceof Set) {
          const items = Array.from(v.values()).slice(0, ARRAY_CAP);
          return { __type: 'Set', items: items.map((x) => safeValue(x, depth + 1, seen)) };
        }
        const out = {};
        let i = 0;
        for (const k of Object.keys(v)) {
          if (i++ >= KEYS_CAP) { out.__truncated = true; break; }
          try { out[k] = safeValue(v[k], depth + 1, seen); }
          catch (e) {
            const msg = String(e);
            // SugarCube 2.37+ throws "[DEPRECATED]" on legacy Config getters
            // that have moved (e.g. Config.saves.autosave → Save.autosave).
            // Collapse the verbose throw to a clean sentinel so downstream
            // analysis can skip these without extra logic.
            if (msg.includes('[DEPRECATED]')) out[k] = '<deprecated>';
            else out[k] = '<error:' + msg.slice(0, 80) + '>';
          }
        }
        return out;
      }
      return '<unknown:' + t + '>';
    };
    const dump = (v) => {
      try { return safeValue(v, 0, new WeakSet()); }
      catch (e) { return '<error:' + String(e).slice(0, 80) + '>'; }
    };

    // ------------------------------------------------------------------
    // Engine detection
    // ------------------------------------------------------------------
    const hasSugarCube = typeof SugarCube !== 'undefined' && SugarCube && SugarCube.State;
    const hasHarlowe   = typeof Harlowe   !== 'undefined' && Harlowe;
    const hasChapbook  = typeof engine    !== 'undefined' && engine && engine.state;

    const out = {
      captured_at: new Date().toISOString(),
      engine: hasSugarCube ? 'sugarcube' : hasHarlowe ? 'harlowe' : hasChapbook ? 'chapbook' : 'unknown',
    };

    // Twine <tw-storydata> element — embedded by the Twine compiler into every
    // published story. Its attributes are the canonical cross-engine identity
    // (ifid, name, format, format-version, creator). Prefer this over engine
    // globals because in newer SugarCube builds `Story` is not exposed as a
    // global and `SugarCube.Story.*` props live on a class prototype (Object.keys
    // returns `[]`, so a generic walker misses them).
    const readStorydata = () => {
      const node = document.querySelector('tw-storydata');
      if (!node) return null;
      const attrs = {};
      for (const a of node.attributes) attrs[a.name] = a.value;
      return {
        name: attrs['name'] || null,
        ifid: attrs['ifid'] || null,
        format: attrs['format'] || null,
        format_version: attrs['format-version'] || null,
        creator: attrs['creator'] || null,
        creator_version: attrs['creator-version'] || null,
        startnode: attrs['startnode'] || null,
        options: attrs['options'] || null,
        tags: attrs['tags'] || null,
        zoom: attrs['zoom'] || null,
      };
    };

    // ------------------------------------------------------------------
    // SugarCube — the primary case
    // ------------------------------------------------------------------
    if (hasSugarCube) {
      // Version — must use explicit accessors; own-property enumeration is empty
      // because SugarCube.version is a class instance with prototype methods.
      try {
        const V = SugarCube.version;
        out.version = {
          name: V.name || null,
          major: typeof V.major === 'number' ? V.major : null,
          minor: typeof V.minor === 'number' ? V.minor : null,
          patch: typeof V.patch === 'number' ? V.patch : null,
          prerelease: V.prerelease || null,
          build: V.build != null ? V.build : null,
          // short/long are methods; call them
          short: typeof V.short === 'function' ? V.short.call(V) : (typeof V.short === 'string' ? V.short : null),
          toString: typeof V.toString === 'function' ? V.toString.call(V) : null,
        };
      } catch (e) { out.version = { __error: String(e).slice(0, 120) }; }

      // Config — use the namespaced accessor so we get game-customized values
      try { out.config = dump(SugarCube.Config); } catch (e) { out.config = { __error: String(e).slice(0, 120) }; }

      // State shape (NOT contents — see scene_bodies for per-turn state)
      try {
        const S = SugarCube.State;
        out.state = {
          turn: typeof S.turn === 'number' ? S.turn : null,
          turns: typeof S.turns === 'number' ? S.turns : null,
          length: typeof S.length === 'number' ? S.length : null,
          bottom_title: (S.bottom && S.bottom.title) || null,
          active_title: (S.active && S.active.title) || null,
          temporary_keys: S.temporary && typeof S.temporary === 'object'
            ? Object.keys(S.temporary).slice(0, 100)
            : [],
          prng_present: !!(S.prng),
          prng_state: S.prng && S.prng.state !== undefined ? dump(S.prng.state) : null,
          history_length: Array.isArray(S.history) ? S.history.length
            : (typeof S.size === 'number' ? S.size : null),
          history_first_entry_shape: Array.isArray(S.history) && S.history[0]
            ? {
                keys: Object.keys(S.history[0]).slice(0, 30),
                title: S.history[0].title || null,
              }
            : null,
          history_last_entry_shape: Array.isArray(S.history) && S.history.length
            ? {
                keys: Object.keys(S.history[S.history.length - 1]).slice(0, 30),
                title: S.history[S.history.length - 1].title || null,
              }
            : null,
          has_marshalForSave: typeof S.marshalForSave === 'function',
          has_unmarshalForSave: typeof S.unmarshalForSave === 'function',
        };
      } catch (e) { out.state = { __error: String(e).slice(0, 120) }; }

      // Story identity (IFID is the canonical cross-game identifier). Read
      // from the embedded <tw-storydata> element — that's the stable source.
      // Also supplement with whatever the engine's own Story namespace exposes
      // via explicit accessors (Object.keys returns empty on class-prototype
      // properties so the generic walker would miss them).
      try {
        const sd = readStorydata();
        const storyOut = sd ? { ...sd } : {};
        const StoryNS = (typeof Story !== 'undefined' && Story) ? Story
                      : (SugarCube.Story ? SugarCube.Story : null);
        if (StoryNS) {
          try { if (typeof StoryNS.title === 'string' && StoryNS.title) storyOut.engine_title = StoryNS.title; } catch (_) {}
          try { if (typeof StoryNS.name === 'string' && StoryNS.name) storyOut.engine_name = StoryNS.name; } catch (_) {}
          try { if (typeof StoryNS.ifid === 'string' && StoryNS.ifid) storyOut.engine_ifid = StoryNS.ifid; } catch (_) {}
          try { if (typeof StoryNS.domId === 'string' && StoryNS.domId) storyOut.engine_dom_id = StoryNS.domId; } catch (_) {}
        }
        out.story = Object.keys(storyOut).length ? storyOut : null;
      } catch (e) { out.story = { __error: String(e).slice(0, 120) }; }

      // User settings (the game's own Setting definitions + current values)
      try {
        if (typeof SugarCube.settings !== 'undefined') {
          out.settings = dump(SugarCube.settings);
        }
      } catch (e) {}
      try {
        if (typeof Setting !== 'undefined' && Setting) {
          // Setting.list is a Map (newer) or Array (older) of definitions
          if (Setting.list !== undefined) {
            out.setting_definitions = dump(Setting.list);
          }
        }
      } catch (e) {}

      // Save capabilities + slot metadata (titles/dates only — never the
      // full state blob; that's huge and duplicates scene_bodies coverage)
      try {
        const SaveNS = SugarCube.Save || (typeof Save !== 'undefined' ? Save : null);
        if (SaveNS) {
          const caps = {
            has_serialize: typeof SaveNS.serialize === 'function',
            has_deserialize: typeof SaveNS.deserialize === 'function',
            has_slots: !!SaveNS.slots,
            has_autosave: !!SaveNS.autosave,
            slot_count: null,
            on_save_handlers: 0,
            on_load_handlers: 0,
          };
          try {
            if (SaveNS.onSave && typeof SaveNS.onSave.size === 'number') caps.on_save_handlers = SaveNS.onSave.size;
            if (SaveNS.onLoad && typeof SaveNS.onLoad.size === 'number') caps.on_load_handlers = SaveNS.onLoad.size;
          } catch (e) {}
          // Slot metadata
          if (SaveNS.slots) {
            try {
              if (typeof SaveNS.slots.count === 'function') caps.slot_count = SaveNS.slots.count();
            } catch (e) {}
            const slots = [];
            const n = caps.slot_count != null ? caps.slot_count : 8;
            for (let i = 0; i < n; i++) {
              try {
                const slot = typeof SaveNS.slots.get === 'function' ? SaveNS.slots.get(i) : null;
                if (!slot) { slots.push({ index: i, empty: true }); continue; }
                slots.push({
                  index: i,
                  empty: false,
                  id: slot.id || null,
                  title: slot.title || null,
                  date: slot.date ? new Date(slot.date).toISOString() : null,
                  description: slot.description || null,
                  metadata: slot.metadata ? dump(slot.metadata) : null,
                });
              } catch (e) { slots.push({ index: i, error: String(e).slice(0, 120) }); }
            }
            caps.slots_metadata = slots;
          }
          // Autosave slot
          try {
            if (SaveNS.autosave && typeof SaveNS.autosave.get === 'function') {
              const a = SaveNS.autosave.get();
              caps.autosave_metadata = a ? {
                id: a.id || null,
                title: a.title || null,
                date: a.date ? new Date(a.date).toISOString() : null,
                description: a.description || null,
              } : null;
            }
          } catch (e) {}
          out.save_caps = caps;
        }
      } catch (e) { out.save_caps = { __error: String(e).slice(0, 120) }; }

      return out;
    }

    // ------------------------------------------------------------------
    // Harlowe — much sparser API surface
    // ------------------------------------------------------------------
    if (hasHarlowe) {
      try { out.version = Harlowe.version || null; } catch (e) {}
      try { out.state = { active_title: (Harlowe.State && Harlowe.State.passage && Harlowe.State.passage.name) || null }; } catch (e) {}
      try { out.story = readStorydata(); } catch (e) {}
      return out;
    }

    // ------------------------------------------------------------------
    // Chapbook — minimal metadata surface
    // ------------------------------------------------------------------
    if (hasChapbook) {
      try {
        out.story = readStorydata() || {
          title: engine.story && engine.story.name ? engine.story.name : null,
          start: engine.story && engine.story.start ? engine.story.start : null,
        };
      } catch (e) {}
      return out;
    }

    // Even if no engine global is detected, a Twine-published story will
    // still have a <tw-storydata> element — grab the identity from there.
    out.error = 'No supported engine global detected';
    try { out.story = readStorydata(); } catch (e) {}
    return out;
  });
}

module.exports = { dumpEngineConfig };
