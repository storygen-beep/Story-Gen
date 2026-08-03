// Portal adapter for mopoga.com
//
// Landing page pattern: big "PLAY <GAME> NOW" button that reveals the embed iframe
// beneath it. Once clicked, the game loads in an iframe at mopoga.com/embed/...

'use strict';

module.exports = {
  name: 'mopoga',

  async enterGame(page) {
    const selectors = [
      'a:has-text("PLAY ")',
      'button:has-text("PLAY ")',
      'a.play-button',
      '[class*="play-now"]',
    ];
    for (const sel of selectors) {
      try {
        const btn = page.locator(sel + ':visible').first();
        if ((await btn.count().catch(() => 0)) && (await btn.isVisible().catch(() => false))) {
          await btn.click({ timeout: 5000 }).catch(() => {});
          // Wait for the embed iframe to appear
          await page.waitForSelector('iframe[src*="embed"]', { timeout: 10000 }).catch(() => {});
          await page.waitForTimeout(3500);
          return { ok: true, via: sel };
        }
      } catch (e) {}
    }
    return { ok: false, reason: 'no portal PLAY button found' };
  },
};
