# Twine engines — state APIs and gotchas

Read when the explorer misbehaves on a specific game and you suspect engine-detection or state-restore is the root cause.

## SugarCube v2 (most common, incl. Back to Freedom, many games on mopoga/dikgames)

**Detection:** `typeof SugarCube !== 'undefined'` AND `SugarCube.State` is an object.

**Read variables:** `SugarCube.State.variables` — the `$` namespace. Plain object; safe to deep-clone.

**Current passage:** `SugarCube.State.passage` (string) OR `SugarCube.State.active.title`.

**Marshal/unmarshal (fast snapshot):**
- `SugarCube.State.marshalForSave()` → plain object representing full engine state
- `SugarCube.State.unmarshalFromSave(obj)` → restores from that object
- Available in SugarCube 2.21.0+. If missing, fall back to save slots or path-replay.

**Save slots (slower fallback):**
- `Save.serialize()` → string
- `Save.deserialize(str)` → restores
- `Save.slots.save(N, title)` / `Save.slots.load(N)` for named slots
- `Save.autosave.get()` / `Save.autosave.set()` for the auto-save slot

**Gotchas:**
- Marshal includes the entire history stack — restoring also restores turn history
- Some games mutate `$` variables with non-serialisable values (Maps, custom classes). We strip those via a JSON replacer in `engine.js`
- Passage transitions happen via `SugarCube.engine.play(passageName)` — you can force-navigate if needed
- Side effects in `<<script>>` tags run on passage entry; restoring state doesn't always re-trigger them

## Harlowe v3+

**Detection:** `typeof Harlowe !== 'undefined'` OR window-scoped `State` with `passage` property.

**Read variables:** `State.variables`. Note: Harlowe wraps values in custom datatypes (changers, datamaps, datasets) that don't cleanly JSON-serialise — deep-clone carefully.

**Marshal:** Harlowe does NOT expose a clean marshal API. Options:
- Use `State.timeline` to inspect history, but restoring is hard
- Use the game's in-game save slots if the author added any
- Fall back to path-replay (record click sequence, reload game, re-click)

**Gotchas:**
- Harlowe's "timeline" is deeply coupled to its reactive datatypes — don't try to deep-copy it
- For games without save slots, path-replay is the only reliable option
- Expect the explorer to run much slower on Harlowe

## Chapbook

**Detection:** `typeof engine !== 'undefined'` AND `engine.state && typeof engine.state.get === 'function'`.

**Read variables:** `engine.state.all()` — returns plain key-value object.

**Set variables:** `engine.state.set(key, value)` — safe way to write back.

**Marshal:** No built-in marshal API. Do `JSON.stringify(engine.state.all())` for snapshot; restore by iterating `set()` for each key. But the `engine` also maintains a history stack we can't easily restore.

**Gotchas:**
- Chapbook makes the state object the source of truth but navigation (current passage) is separate. Need to `engine.go(passage)` after restoring variables.

## Unknown / custom engines

If detection returns `engine: 'unknown'`:
- Read variables: we can't
- Hash states: fall back to a hash of the visible DOM text (lossy — same text from different routes collides)
- Backtrack: only by path-replay (reload game, re-click sequence). Very slow.

The explorer will set `detection_failure: true` in the final report so you can triage manually.

## Common portal quirks

**mopoga.com:**
- Game embeds live at `mopoga.com/embed/<game>/` in an iframe on the landing page
- The landing page has a `PLAY <GAME> NOW` button that reveals the iframe
- Age disclaimers render inside the iframe as "Continue" buttons
- Character creation: text inputs + "Confirm"; avatar grid + "Confirm"
- Ad popups: handled by the `setup.js` page-close listener

**dikgames.com / similar:**
- Similar pattern — portal with PLAY button → embedded iframe
- Some add a second "click to start" inside the iframe

**itch.io:**
- Often delivers games via `/html/<hash>` iframe
- No portal disclaimer; may have "Run HTML5 game" button on the page
- Some games launch fullscreen — handle `[fullscreen]` requestFullscreen calls

## Diagnosing a broken game

1. Run the explorer with a short budget (5 min) and check the log
2. Look at `dom_recon.json` — if `engine: unknown`, detection failed
3. Open the game manually in Chrome DevTools; in the console, try:
   - `SugarCube`  (SugarCube)
   - `Harlowe`  or  `State`  (Harlowe)
   - `engine`  (Chapbook)
4. If you find a global that's not any of these, add it to `engine.js` introspect().
