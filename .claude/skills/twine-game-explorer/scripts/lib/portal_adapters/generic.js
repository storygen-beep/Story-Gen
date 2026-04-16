// Generic portal adapter — fallback when URL's host has no dedicated adapter.
//
// Strategy: look for obvious "play / start / launch / begin" buttons on the
// landing page. If found, click one. If not, do nothing — the game may already
// be live, or the page IS the game.

'use strict';

const PLAY_WORDS = ['Play Now', 'Play Game', 'Start Game', 'Launch Game', 'Begin', 'Start', 'Play', 'Open Game'];

module.exports = {
  name: 'generic',

  async enterGame(page) {
    for (const word of PLAY_WORDS) {
      const sel = `button:has-text("${word}"):visible, a:has-text("${word}"):visible`;
      try {
        const btn = page.locator(sel).first();
        if ((await btn.count().catch(() => 0)) && (await btn.isVisible().catch(() => false))) {
          // Size check — avoid tiny accidental hits; real portal buttons are sizable
          const box = await btn.boundingBox().catch(() => null);
          if (!box || box.width < 40 || box.height < 20) continue;
          await btn.click({ timeout: 3000 }).catch(() => {});
          await page.waitForTimeout(3000);
          return { ok: true, via: word };
        }
      } catch (e) {}
    }
    return { ok: false, reason: 'no obvious portal entry button' };
  },
};
