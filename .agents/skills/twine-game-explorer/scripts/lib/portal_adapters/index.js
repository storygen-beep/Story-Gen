// Portal adapters — per-host recipes for getting from a landing URL into the
// actual game iframe.
//
// Each adapter exports:
//   name: string             — identifier for logging
//   enterGame(page): Promise — navigate portal UI to reveal the game iframe
//
// Add new adapters by creating scripts/lib/portal_adapters/<host>.js and
// registering it in the ADAPTERS map below.

'use strict';

const mopoga = require('./mopoga');
const generic = require('./generic');

const ADAPTERS = {
  'mopoga.com': mopoga,
  // 'dikgames.com': dikgames,
  // 'itch.io': itch,
};

function getAdapter(url) {
  try {
    const host = new URL(url).host.replace(/^www\./, '');
    if (ADAPTERS[host]) return ADAPTERS[host];
  } catch (e) {}
  return generic;
}

module.exports = { getAdapter, ADAPTERS };
