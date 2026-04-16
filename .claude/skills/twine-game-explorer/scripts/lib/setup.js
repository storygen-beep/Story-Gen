// Setup — the thin pre-play stage.
//
// Phase 5 rewrite: host-specific logic lives in `portal_adapters/`. This file
// only does work that's genuinely universal across Twine games:
//   1. Close stray cross-origin popup tabs (ads)
//   2. Delegate portal-entry to the right adapter
//   3. Find the game iframe
//   4. Dismiss the single-button age/warning disclaimer (unambiguous: a lone
//      "Continue" sitting in a warning context)
//   5. Prefill trivial character-creation inputs (name + avatar) with defaults
//      so the explorer doesn't have to type into text fields mid-DFS.
//
// Everything else — multi-option character-creation questions, UI-toggle
// prompts, tutorial dialogs — is handed off to the explorer / classifier.

'use strict';

const { getAdapter } = require('./portal_adapters');

const DEFAULT_NAMES = ['Player', 'Smith'];

function registerPopupCloser(context, targetDomain) {
  context.on('page', async (p) => {
    try { await p.waitForLoadState('domcontentloaded'); } catch (e) {}
    const u = p.url();
    if (!u.includes(targetDomain)) {
      try { await p.close(); } catch (e) {}
    }
  });
}

async function findGameFrame(page, { timeoutMs = 20000, engineTimeoutMs = 10000 } = {}) {
  await page.waitForSelector('iframe', { timeout: timeoutMs }).catch(() => {});
  const frames = page.frames();
  let best = frames.find((f) => /embed|game|play/i.test(f.url()) && f !== page.mainFrame());
  if (!best) best = frames.find((f) => f !== page.mainFrame());
  if (!best) return page.mainFrame();

  // Wait for the iframe's DOM to load fully
  await best.waitForLoadState('domcontentloaded').catch(() => {});

  // Poll for a Twine engine global — SugarCube usually initializes within a
  // few seconds of iframe load, but exact timing varies. Without this wait
  // the explorer can race ahead and see `engine: unknown`, which breaks
  // state hashing and stops all exploration progress.
  const pollEvery = 500;
  const maxPolls = Math.ceil(engineTimeoutMs / pollEvery);
  for (let i = 0; i < maxPolls; i++) {
    const has = await best.evaluate(() => {
      return !!(
        (typeof SugarCube !== 'undefined' && SugarCube && SugarCube.State) ||
        (typeof Harlowe !== 'undefined' && Harlowe && Harlowe.State) ||
        (typeof State !== 'undefined' && State && State.passage) ||
        (typeof engine !== 'undefined' && engine && engine.state && typeof engine.state.get === 'function')
      );
    }).catch(() => false);
    if (has) break;
    await page.waitForTimeout(pollEvery);
  }
  return best;
}

/**
 * Dismiss the age / content warning disclaimer.
 * We only click "Continue" when it's the ONLY button visible in the content area.
 * Two or more distinct buttons = a real decision, not a disclaimer — leave it
 * for the classifier.
 */
async function dismissDisclaimer(frame) {
  const continueSel = 'a:has-text("Continue"):visible, button:has-text("Continue"):visible, input[value="Continue" i]:visible';
  for (let attempt = 0; attempt < 4; attempt++) {
    const has = await frame.locator(continueSel).count().catch(() => 0);
    if (!has) return;
    // Verify it's actually a disclaimer (warning text visible + single forward button)
    const otherButtons = await frame.evaluate(() => {
      const all = document.querySelectorAll('button, a, [role="button"]');
      const texts = new Set();
      for (const el of all) {
        const r = el.getBoundingClientRect();
        if (r.width < 20 || r.height < 14) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
        const t = (el.textContent || '').trim();
        if (!t || t.length > 160) continue;
        if (/^(continue|toggle the ui bar|ok|confirm)$/i.test(t)) continue;
        if (/^(home|menu|back|saves|options|gallery|cheats|guide|credits|achievements|restart|sandbox mode|changelog|faq|help)$/i.test(t)) continue;
        texts.add(t);
      }
      return texts.size;
    }).catch(() => 0);
    if (otherButtons >= 2) return; // it's a menu, not a disclaimer

    await frame.locator(continueSel).first().click({ force: true, timeout: 2500 }).catch(() => {});
    await frame.page().waitForTimeout(1500).catch(() => {});
  }
}

/**
 * Prefill trivial character-creation: name text inputs + avatar Confirm.
 *
 * This is the one narrow concession to "not everything is a DFS choice" —
 * we don't want the explorer trying to enumerate alphabet permutations for a
 * name field, and avatar selection is cosmetic for a mechanical analysis.
 * Intentionally conservative: only fires if the screen has text inputs OR
 * a lone Confirm button with no competing choices.
 */
async function prefillCharacterCreation(frame, { names = DEFAULT_NAMES } = {}) {
  try {
    const inputs = await frame.locator('input[type="text"]:visible, input:not([type]):visible').all();
    if (inputs.length > 0) {
      for (let i = 0; i < Math.min(inputs.length, names.length); i++) {
        await inputs[i].fill(names[i]).catch(() => {});
      }
      await frame.page().waitForTimeout(600);
    }
    // Click Confirm only if it's the sole forward button (no competing multi-option menu)
    const confirmSel = 'button:has-text("Confirm"):visible, a:has-text("Confirm"):visible';
    const hasConfirm = await frame.locator(confirmSel).count().catch(() => 0);
    if (hasConfirm) {
      const otherChoices = await frame.evaluate(() => {
        const all = document.querySelectorAll('button, a, [role="button"]');
        const texts = new Set();
        for (const el of all) {
          const r = el.getBoundingClientRect();
          if (r.width < 20 || r.height < 14) continue;
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
          const t = (el.textContent || '').trim();
          if (!t || t.length > 160) continue;
          if (/^(confirm|toggle the ui bar)$/i.test(t)) continue;
          if (/^(home|menu|back|saves|options|gallery|cheats|guide|credits|achievements|restart|sandbox mode|changelog|faq|help)$/i.test(t)) continue;
          texts.add(t);
        }
        return texts.size;
      }).catch(() => 0);
      if (otherChoices < 2) {
        await frame.locator(confirmSel).first().click({ force: true, timeout: 2500 }).catch(() => {});
        await frame.page().waitForTimeout(1500);
      }
    }
  } catch (e) {}
}

/**
 * Top-level: take a landing URL, end up in the game's interactive frame.
 * Returns the game frame handle for the explorer to drive.
 */
async function doSetup(page, context, { url, names = DEFAULT_NAMES } = {}) {
  const host = (() => { try { return new URL(url).host; } catch (e) { return ''; } })();
  if (host) registerPopupCloser(context, host);

  const adapter = getAdapter(url);
  const adapterResult = await adapter.enterGame(page);

  const frame = await findGameFrame(page);
  await dismissDisclaimer(frame);
  await prefillCharacterCreation(frame, { names });

  return { frame, adapter: adapter.name, adapter_result: adapterResult };
}

module.exports = {
  doSetup,
  findGameFrame,
  dismissDisclaimer,
  prefillCharacterCreation,
  registerPopupCloser,
};
