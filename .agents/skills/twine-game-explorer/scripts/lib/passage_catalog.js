// Passage catalog dump — a one-shot enumeration of every passage the
// game defines, regardless of whether Claude ever navigates to it.
//
// For a static-analysis / design-reference corpus this is the single
// highest-value artifact: one JSON file contains the entire game's
// source (including widgets, StoryJS, StoryCSS, StoryInit, StoryCaption,
// etc. — they're all just tagged passages in Twine).
//
// We preserve the source byte-for-byte. No truncation, no sanitisation,
// no macro expansion. Downstream consumers can parse `[[Target]]`,
// `<<link>>`, `<<if>>`, `<<set>>` out of the raw source themselves.
//
// Engines covered:
//   - SugarCube v2: Story.passages (object: name -> Passage instance)
//   - Harlowe:      Harlowe.API_ACCESS? Varies by version — best effort
//   - Chapbook:     engine.story.passages (array)
// For unknown engines we return null; live.js logs and keeps going.

'use strict';

/**
 * Enumerate every passage the game exposes. Returns an array of
 * { name, tags, source_raw } objects, or null when the passage store
 * is unreachable.
 *
 * Runs inside the game frame (browser context).
 */
async function dumpCatalog(frame) {
  return await frame.evaluate(() => {
    const out = [];

    // --- SugarCube v2 ---
    // Story.passages is typically a plain object keyed by passage name
    // ({ "Passage Name": Passage }), but some builds expose it as a Map.
    if (typeof Story !== 'undefined' && Story && Story.passages) {
      const src = Story.passages;
      const pushEntry = (name, p) => {
        if (!p) return;
        const tags = Array.isArray(p.tags) ? p.tags.slice() : [];
        const text = typeof p.text === 'string' ? p.text : '';
        out.push({ name: String(name), tags, source_raw: text });
      };
      if (src instanceof Map || (typeof src.forEach === 'function' && src.constructor && src.constructor.name === 'Map')) {
        src.forEach((p, name) => pushEntry(name, p));
      } else if (typeof src === 'object') {
        for (const [name, p] of Object.entries(src)) pushEntry(name, p);
      }
      if (out.length) return { engine_hint: 'sugarcube', passages: out };
    }

    // --- Chapbook ---
    if (typeof engine !== 'undefined' && engine && engine.story && Array.isArray(engine.story.passages)) {
      for (const p of engine.story.passages) {
        if (!p) continue;
        out.push({
          name: String(p.name || ''),
          tags: Array.isArray(p.tags) ? p.tags.slice() : [],
          source_raw: typeof p.source === 'string' ? p.source : (typeof p.text === 'string' ? p.text : ''),
        });
      }
      if (out.length) return { engine_hint: 'chapbook', passages: out };
    }

    // --- Harlowe ---
    // Harlowe doesn't expose a clean public passage map; parse the embedded
    // <tw-passagedata> elements from the original Twine HTML. These survive
    // even after the engine boots.
    const passageNodes = document.querySelectorAll('tw-passagedata');
    if (passageNodes.length) {
      for (const node of passageNodes) {
        const name = node.getAttribute('name') || '';
        const tagsAttr = node.getAttribute('tags') || '';
        const tags = tagsAttr.trim() ? tagsAttr.trim().split(/\s+/) : [];
        out.push({
          name,
          tags,
          source_raw: String(node.textContent || ''),
        });
      }
      if (out.length) return { engine_hint: 'harlowe-embedded', passages: out };
    }

    return null;
  });
}

module.exports = { dumpCatalog };
