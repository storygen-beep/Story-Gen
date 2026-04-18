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
 *
 * Implementation note: the final payload is JSON-serialized inside the page
 * (then re-parsed Node-side) to sidestep Playwright's wire format. Some
 * games — e.g. shady-deals — stash non-plain objects (Date subclasses,
 * custom classes) in SugarCube state. Playwright's default evaluate
 * serializer rejects those with "expected string, got object"; JSON
 * handles them via toJSON() / own-prop enumeration. Dates / Maps / Sets
 * are mapped through the same `__type` tagging `deep()` uses, so
 * downstream consumers see identical shape.
 */
async function introspect(frame) {
  const jsonStr = await frame.evaluate(() => {
    const __typedReplacer = (k, v) => {
      if (typeof v === 'function') return undefined;
      if (v instanceof Date) return { __type: 'Date', v: v.toISOString() };
      if (v instanceof Map) return { __type: 'Map', v: Array.from(v.entries()) };
      if (v instanceof Set) return { __type: 'Set', v: Array.from(v.values()) };
      return v;
    };
    const __introspectImpl = () => {
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

    // Rendered passage body extractor. Engine-aware with fallbacks.
    // Returns { body_text, body_html, modal_text } — never truncated.
    // body_text/html = the rendered narrative passage (the thing the player reads).
    // modal_text     = the active #ui-dialog's innerText when a modal is layered
    //                  over the passage, otherwise null.
    const readBody = (engineHint) => {
      const pickActive = (container, activeSel, fallbackSel) => {
        if (!container) return null;
        // SugarCube marks the active passage with .passage; some builds also use
        // .passage-active. Try the more specific selector first, fall back to
        // the last passage element (SugarCube transitions append and remove).
        if (activeSel) {
          const hit = container.querySelector(activeSel);
          if (hit) return hit;
        }
        if (fallbackSel) {
          const list = container.querySelectorAll(fallbackSel);
          if (list.length) return list[list.length - 1];
        }
        return container;
      };

      let bodyEl = null;
      if (engineHint === 'sugarcube') {
        const passages = document.getElementById('passages');
        bodyEl = pickActive(passages, '.passage.passage--active, .passage-active', '.passage');
      } else if (engineHint === 'harlowe') {
        // Harlowe renders passages into <tw-passage> inside <tw-story>.
        const twStory = document.querySelector('tw-story');
        bodyEl = twStory
          ? twStory.querySelector('tw-passage')
          : document.querySelector('tw-passage');
      } else if (engineHint === 'chapbook') {
        bodyEl = document.querySelector('.page-body, .page article, main');
      }
      // Engine-agnostic fallback
      if (!bodyEl) {
        bodyEl = document.getElementById('passages')
          || document.querySelector('tw-passage')
          || document.querySelector('.passage')
          || document.querySelector('main')
          || document.body;
      }

      const body_text = bodyEl ? String(bodyEl.innerText || '') : '';
      const body_html = bodyEl ? String(bodyEl.innerHTML || '') : '';

      // Modal overlay (SugarCube #ui-dialog). Captured separately so downstream
      // analysis can distinguish "player is reading passage X" from "player is
      // reading a modal layered over passage X".
      let modal_text = null;
      const dialog = document.getElementById('ui-dialog');
      if (dialog) {
        const cs = dialog.ownerDocument.defaultView
          ? dialog.ownerDocument.defaultView.getComputedStyle(dialog)
          : null;
        const open = dialog.classList.contains('open')
          || (cs && cs.display !== 'none' && cs.visibility !== 'hidden');
        if (open) {
          const body = dialog.querySelector('#ui-dialog-body') || dialog;
          const txt = String(body.innerText || '').trim();
          if (txt) modal_text = txt;
        }
      }

      return { body_text, body_html, modal_text };
    };

    // --- SugarCube ---
    if (typeof SugarCube !== 'undefined' && SugarCube && SugarCube.State) {
      // Namespace handling: some builds expose `State`/`Save`/`Engine` as
      // globals, others only as `SugarCube.State`/`SugarCube.Save`/`SugarCube.Engine`.
      // Resolve both.
      const S = SugarCube.State;
      const SaveNS = (typeof SugarCube.Save !== 'undefined') ? SugarCube.Save : (typeof Save !== 'undefined' ? Save : null);
      const EngineNS = (typeof SugarCube.Engine !== 'undefined') ? SugarCube.Engine : (typeof Engine !== 'undefined' ? Engine : null);
      const variables = deep(S.variables || {});
      const passage = S.passage || (S.active && S.active.title) || null;
      const turns = typeof S.turns === 'number' ? S.turns : (S.length || null);
      const caps = {
        // State-level primitive: `State.marshalForSave()` + `State.unmarshalForSave()`.
        // This is the low-level round-trip that skips Save.* validation entirely
        // (no Config.saves.id check, no onLoad handlers, no LZString round-trip).
        // Confirmed in SugarCube source at src/state.js ~147.
        stateMarshal: typeof S.marshalForSave === 'function' && typeof S.unmarshalForSave === 'function',
        // Engine.show() re-renders the current passage WITHOUT appending a new
        // history entry (vs Engine.play which would). Essential after state_marshal
        // restore so the DOM reflects the loaded state.
        engineShow: !!(EngineNS && typeof EngineNS.show === 'function'),
        // Public save API: Save.serialize / Save.deserialize. Rejects on games
        // that register onLoad handlers or set Config.saves.id — the bouncer we
        // saw on BTF and Emilie.
        serialize: !!(SaveNS && typeof SaveNS.serialize === 'function' && typeof SaveNS.deserialize === 'function'),
        slots: !!(SaveNS && SaveNS.slots && typeof SaveNS.slots.save === 'function' && typeof SaveNS.slots.load === 'function'),
        saveNamespace: SaveNS === (typeof Save !== 'undefined' ? Save : null) ? 'global' : (SaveNS ? 'SugarCube.Save' : 'none'),
      };
      const body = readBody('sugarcube');
      return {
        engine: 'sugarcube',
        version: (SugarCube.version && SugarCube.version.short) || null,
        passage, variables, turns,
        canMarshal: caps.stateMarshal || caps.serialize,
        saveCaps: caps,
        body_text: body.body_text,
        body_html: body.body_html,
        modal_text: body.modal_text,
      };
    }

    // --- Harlowe ---
    // Harlowe does not expose a clean global by default; the state sits inside the engine.
    // Look for the State structure commonly attached to window.Harlowe or window.State.
    if (typeof Harlowe !== 'undefined' && Harlowe && Harlowe.State) {
      const s = Harlowe.State;
      const body = readBody('harlowe');
      return {
        engine: 'harlowe',
        version: null,
        passage: (s.passage && s.passage.name) || null,
        variables: deep(s.variables || {}),
        turns: (s.timeline && s.timeline.length) || null,
        canMarshal: false, // Harlowe's timeline is harder to round-trip
        body_text: body.body_text,
        body_html: body.body_html,
        modal_text: body.modal_text,
      };
    }

    // --- Chapbook ---
    if (typeof engine !== 'undefined' && engine && engine.state && typeof engine.state.get === 'function') {
      const body = readBody('chapbook');
      return {
        engine: 'chapbook',
        version: null,
        passage: (typeof engine.story !== 'undefined' && engine.story.passage) || null,
        variables: deep(engine.state.all ? engine.state.all() : {}),
        turns: null,
        canMarshal: false,
        body_text: body.body_text,
        body_html: body.body_html,
        modal_text: body.modal_text,
      };
    }

    // Unknown engine — still try to grab whatever body text is on screen.
    const fallbackBody = readBody(null);
    return {
      engine: 'unknown',
      version: null,
      passage: null,
      variables: {},
      turns: null,
      canMarshal: false,
      body_text: fallbackBody.body_text,
      body_html: fallbackBody.body_html,
      modal_text: fallbackBody.modal_text,
    };
    };
    // Run the impl, JSON-serialize the whole tree in the page context so
    // Playwright only has to transport a string. Any throw is reported
    // back as an error marker for Node-side handling.
    try {
      const result = __introspectImpl();
      return JSON.stringify(result, __typedReplacer);
    } catch (e) {
      return JSON.stringify({ __introspect_error: String((e && e.message) || e) });
    }
  });
  const parsed = JSON.parse(jsonStr);
  if (parsed && parsed.__introspect_error) {
    throw new Error('engine.introspect failed in page: ' + parsed.__introspect_error);
  }
  return parsed;
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
  if (info.engine === 'sugarcube') {
    // PRIMARY: State.marshalForSave(). This is the low-level primitive that
    // `Save.marshal` calls internally after its validation gates — using it
    // directly bypasses Config.saves.id, onLoad handlers, and the LZString
    // round-trip. Works on games that reject Save.deserialize (BTF, Emilie).
    // Returns a plain JSON-friendly object (shape: {index, history, ...}).
    if (info.saveCaps && info.saveCaps.stateMarshal) {
      // Same JSON-string transport trick as introspect(): SugarCube's
      // marshalForSave() can return objects with non-plain fields (Dates,
      // custom classes) that Playwright's wire format rejects. Serialize
      // in-page, parse on Node side.
      const jsonStr = await frame.evaluate(() => {
        const __typedReplacer = (k, v) => {
          if (typeof v === 'function') return undefined;
          if (v instanceof Date) return { __type: 'Date', v: v.toISOString() };
          if (v instanceof Map) return { __type: 'Map', v: Array.from(v.entries()) };
          if (v instanceof Set) return { __type: 'Set', v: Array.from(v.values()) };
          return v;
        };
        try { return JSON.stringify({ ok: true, data: SugarCube.State.marshalForSave() }, __typedReplacer); }
        catch (e) { return JSON.stringify({ ok: false, error: String(e) }); }
      });
      const blob = JSON.parse(jsonStr);
      if (blob.ok) return { engine: 'sugarcube', mode: 'state_marshal', blob: blob.data, info };
    }
    // FALLBACK: public Save API. Many games disable `Config.saves.isAllowed`
    // during certain passages (mid-scene, char creation) so we temporarily force
    // it open around the serialize call, then restore the original check.
    if (info.saveCaps && info.saveCaps.serialize) {
      const jsonStr = await frame.evaluate(() => {
        const __typedReplacer = (k, v) => {
          if (typeof v === 'function') return undefined;
          if (v instanceof Date) return { __type: 'Date', v: v.toISOString() };
          if (v instanceof Map) return { __type: 'Map', v: Array.from(v.entries()) };
          if (v instanceof Set) return { __type: 'Set', v: Array.from(v.values()) };
          return v;
        };
        try {
          const S = (typeof SugarCube !== 'undefined' && SugarCube.Save) ? SugarCube.Save : (typeof Save !== 'undefined' ? Save : null);
          const CFG = (typeof SugarCube !== 'undefined' && SugarCube.Config) ? SugarCube.Config : (typeof Config !== 'undefined' ? Config : null);
          if (!S || typeof S.serialize !== 'function') return JSON.stringify({ ok: false, error: 'Save.serialize not reachable' });
          let original;
          if (CFG && CFG.saves) {
            original = CFG.saves.isAllowed;
            CFG.saves.isAllowed = () => true;
          }
          try {
            const data = S.serialize();
            return JSON.stringify({ ok: true, data }, __typedReplacer);
          } finally {
            if (CFG && CFG.saves && original !== undefined) CFG.saves.isAllowed = original;
          }
        } catch (e) { return JSON.stringify({ ok: false, error: String(e) }); }
      });
      const blob = JSON.parse(jsonStr);
      if (blob.ok) return { engine: 'sugarcube', mode: 'serialize', blob: blob.data, info };
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
  const errors = [];

  if (snap.engine === 'sugarcube') {
    // PRIMARY: state_marshal path. Skips Save.* module entirely, so no
    // onLoad handlers, no Config.saves.id check, no UI.alert popups. After
    // loading state, we call Engine.show() to re-render the current passage
    // (Engine.play would append a new turn; we want to replace, not append).
    if (snap.mode === 'state_marshal') {
      // Blob may contain tagged Date/Map/Set markers emitted by our
      // snapshot() JSON-string transport. Pass it as a string and revive
      // inside the page so SugarCube.State.unmarshalForSave receives
      // real Date/Map/Set instances, same as at save-time.
      const blobJson = JSON.stringify(snap.blob);
      const result = await frame.evaluate((blobJson) => {
        const data = JSON.parse(blobJson, (k, v) => {
          if (v && typeof v === 'object' && v.__type === 'Date') return new Date(v.v);
          if (v && typeof v === 'object' && v.__type === 'Map') return new Map(v.v);
          if (v && typeof v === 'object' && v.__type === 'Set') return new Set(v.v);
          return v;
        });
        // Step 1: load state. The actual restore — must succeed.
        if (typeof SugarCube === 'undefined' || !SugarCube.State) return { ok: false, error: 'SugarCube.State missing' };
        if (typeof SugarCube.State.unmarshalForSave !== 'function') return { ok: false, error: 'unmarshalForSave missing on this SugarCube version' };
        try { SugarCube.State.unmarshalForSave(data); }
        catch (e) { return { ok: false, error: 'unmarshalForSave threw: ' + String(e) }; }

        // Step 2: re-render. Best-effort — game-specific postdisplay/postrender
        // hooks can throw on programmatic transitions even though state is
        // already correct. Observed on Road to Success: a `postdisplay` task
        // dereferences a null on every passage transition (including programmatic
        // ones), but the underlying state is restored AND the DOM is updated
        // (the throw happens after the passage HTML is inserted). Capture the
        // error as a warning rather than invalidating the restore.
        const E = (typeof SugarCube.Engine !== 'undefined') ? SugarCube.Engine : (typeof Engine !== 'undefined' ? Engine : null);
        let render_warning = null;
        try {
          if (E && typeof E.show === 'function') {
            E.show();
          } else if (E && typeof E.play === 'function' && SugarCube.State.passage) {
            E.play(SugarCube.State.passage, true);
          }
        } catch (e) {
          render_warning = 'post-restore re-render threw (state restored, DOM update may be partial): ' + String(e);
        }
        return { ok: true, render_warning };
      }, blobJson);
      if (result.ok) return { ok: true, method: 'state_marshal', render_warning: result.render_warning || null };
      errors.push('state_marshal: ' + result.error);
    }
    // Try serialize path. We progressively disable guards that can cause
    // deserialize to return falsy — in order: just isAllowed, then isAllowed
    // + onLoad handler clearing, then isAllowed + onLoad + onSave. The most
    // common cause is a game-registered onLoad handler that rejects rapid or
    // programmatic loads.
    if (snap.mode === 'serialize') {
      const result = await frame.evaluate((data) => {
        const S = (typeof SugarCube !== 'undefined' && SugarCube.Save) ? SugarCube.Save : (typeof Save !== 'undefined' ? Save : null);
        const CFG = (typeof SugarCube !== 'undefined' && SugarCube.Config) ? SugarCube.Config : (typeof Config !== 'undefined' ? Config : null);
        if (!S || typeof S.deserialize !== 'function') return { ok: false, error: 'Save.deserialize not reachable' };

        const attempts = [];

        // Attempt 1: isAllowed override only (original behaviour)
        const tryLoad = (label, cleanup) => {
          let origIsAllowed;
          if (CFG && CFG.saves) {
            origIsAllowed = CFG.saves.isAllowed;
            CFG.saves.isAllowed = () => true;
          }
          try {
            const ok = S.deserialize(data);
            attempts.push({ label, ok: !!ok });
            return !!ok;
          } catch (e) {
            attempts.push({ label, ok: false, error: String(e) });
            return false;
          } finally {
            if (CFG && CFG.saves && origIsAllowed !== undefined) CFG.saves.isAllowed = origIsAllowed;
            if (cleanup) cleanup();
          }
        };

        if (tryLoad('isAllowed_only')) return { ok: true, method: 'isAllowed_only', attempts };

        // Attempt 2: also clear Save.onLoad handlers (the game-installed
        // bouncer lives here). We don't restore them — they'll be reapplied
        // on the next passage transition by the game's init code.
        if (S.onLoad && typeof S.onLoad.clear === 'function') {
          if (tryLoad('onLoad_cleared', null)) {
            return { ok: true, method: 'onLoad_cleared', attempts };
          }
        }

        // Attempt 3: also stub out Save.onSave in case something in the
        // current turn's save flag is blocking. (Less common but cheap.)
        if (S.onSave && typeof S.onSave.clear === 'function') {
          if (tryLoad('onSave_cleared', null)) {
            return { ok: true, method: 'onSave_cleared', attempts };
          }
        }

        return { ok: false, error: 'deserialize rejected through all guard-bypass attempts', attempts };
      }, snap.blob);
      if (result.ok) return { ok: true, method: 'serialize:' + result.method };
      errors.push('serialize: ' + result.error + ' (attempts: ' + JSON.stringify(result.attempts || []) + ')');
    }
    // Cross-mode attempt: if snap was marshal but marshal fails, don't try serialize
    // on raw marshal-shaped blob — that won't work (different formats).
  }

  if (snap.mode === 'path-replay') {
    if (!replayer || !reloadUrl) return { ok: false, error: 'path-replay requires replayer + reloadUrl' };
    await page.goto(reloadUrl, { waitUntil: 'domcontentloaded' }).catch(() => {});
    await replayer(snap.path);
    return { ok: true, method: 'path-replay' };
  }

  return {
    ok: false,
    error: `restore failed for snapshot {engine:${snap.engine}, mode:${snap.mode}}: ${errors.join(' | ') || 'no viable restore path'}`,
  };
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
