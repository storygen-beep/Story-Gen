// Handle the "pre-play" stages of a game: portal landing pages,
// age-gate disclaimers, character creation (name + avatar),
// any initial info modals before real gameplay begins.
//
// The setup phase is heuristic because different games / portals
// look different. We apply a series of probes in order, each idempotent.

'use strict';

async function dismissAllPopups(context, targetDomain) {
  context.on('page', async (p) => {
    try {
      await p.waitForLoadState('domcontentloaded');
    } catch (e) {}
    const u = p.url();
    if (!u.includes(targetDomain)) {
      try { await p.close(); } catch (e) {}
    }
  });
}

/** If the page has a big "PLAY ..." portal button, click it. */
async function clickPortalPlay(page) {
  const selectors = [
    'a:has-text("PLAY "):visible',
    'button:has-text("PLAY "):visible',
    'a:has-text("Play Now"):visible',
    'button:has-text("Play Now"):visible',
  ];
  for (const sel of selectors) {
    try {
      const loc = page.locator(sel).first();
      if ((await loc.count()) && (await loc.isVisible())) {
        await loc.click({ timeout: 5000 });
        return sel;
      }
    } catch (e) {}
  }
  return null;
}

/** Find the game's frame (iframe embed). */
async function findGameFrame(page, { timeoutMs = 20000 } = {}) {
  // Wait for any embed-ish iframe
  await page.waitForSelector('iframe', { timeout: timeoutMs }).catch(() => {});
  const frames = page.frames();
  // Prefer one whose URL contains 'embed' or the game's name
  let best = frames.find((f) => /embed|game|play/i.test(f.url()) && f !== page.mainFrame());
  if (!best) best = frames.find((f) => f !== page.mainFrame());
  return best || page.mainFrame();
}

/** Keep dismissing "Continue" / "I Agree" / "Accept" in the game frame until none left. */
async function dismissDisclaimers(frame, { maxAttempts = 8 } = {}) {
  const patterns = [
    'a:has-text("Continue")',
    'button:has-text("Continue")',
    'a:has-text("I Agree")',
    'button:has-text("I Agree")',
    'a:has-text("Accept")',
    'button:has-text("Accept")',
    'a:has-text("Enter")',
    'button:has-text("Enter")',
    'input[value="Continue" i]',
  ];
  let dismissed = 0;
  for (let i = 0; i < maxAttempts; i++) {
    let hit = false;
    for (const sel of patterns) {
      try {
        const loc = frame.locator(sel).first();
        if ((await loc.count()) && (await loc.isVisible())) {
          await loc.click({ force: true, timeout: 2500 }).catch(() => {});
          dismissed++; hit = true;
          await frame.page().waitForTimeout(1400).catch(() => {});
          break;
        }
      } catch (e) {}
    }
    if (!hit) break;
  }
  return dismissed;
}

/**
 * If the game presents text inputs asking for name, fill them.
 * Heuristic: look for 1-2 text inputs + a Confirm button within the frame.
 * names: array of strings to fill into successive inputs
 */
async function fillNameEntry(frame, { names = ['MC', 'Smith'] } = {}) {
  try {
    const inputs = await frame.locator('input[type="text"]:visible, input:not([type]):visible').all();
    if (inputs.length === 0) return { filled: 0 };
    for (let i = 0; i < Math.min(inputs.length, names.length); i++) {
      await inputs[i].fill(names[i]).catch(() => {});
    }
    const confirm = frame.locator('button:has-text("Confirm"):visible, a:has-text("Confirm"):visible, input[value="Confirm" i]:visible').first();
    if ((await confirm.count()) && (await confirm.isVisible())) {
      await confirm.click({ force: true, timeout: 3000 }).catch(() => {});
    }
    return { filled: Math.min(inputs.length, names.length) };
  } catch (e) {
    return { filled: 0, error: String(e) };
  }
}

/**
 * If an avatar selection grid is shown, pick the first option + Confirm.
 * (Can be overridden by caller later; for default exploration we pick a
 * deterministic avatar so the exploration graph is reproducible.)
 */
async function selectDefaultAvatar(frame) {
  try {
    const confirm = frame.locator('button:has-text("Confirm"):visible, a:has-text("Confirm"):visible').first();
    // If there's an image/button grid followed by Confirm, just click Confirm
    // (default is usually fine for introspection purposes)
    if ((await confirm.count()) && (await confirm.isVisible())) {
      await confirm.click({ force: true, timeout: 3000 }).catch(() => {});
      return true;
    }
  } catch (e) {}
  return false;
}

/**
 * Dismiss any stray OK / Confirm / Got-it modals after character creation.
 *
 * Important: only click when it's an *actual* modal (a single centered
 * confirmation button). If the frame also has several other distinct-text
 * clickable options visible, we're looking at a real choice menu (character
 * creation question, "Tell the truth / Lie for your friend", etc.) — clicking
 * Confirm there would blindly pick one answer and skip the decision tree.
 * In that case we bail out and let the play loop handle it.
 */
async function dismissInfoModals(frame, { rounds = 3 } = {}) {
  const confirmSel = 'button:has-text("OK"):visible, button:has-text("Confirm"):visible, button:has-text("Got it"):visible, a:has-text("OK"):visible, a:has-text("Confirm"):visible';
  for (let i = 0; i < rounds; i++) {
    const confirmLoc = frame.locator(confirmSel).first();
    if (!(await confirmLoc.count().catch(() => 0))) break;

    // Safety check: are there other distinct-text buttons/links alongside?
    // If so, this is a menu, not a modal. Bail.
    const otherDistinct = await frame.evaluate(() => {
      const all = document.querySelectorAll('button, a, [role="button"]');
      const texts = new Set();
      for (const el of all) {
        const r = el.getBoundingClientRect();
        if (r.width < 20 || r.height < 12) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
        const t = (el.textContent || '').trim();
        if (!t) continue;
        if (/^(ok|confirm|got it|continue)$/i.test(t)) continue;
        if (/^(home|menu|back|saves|options|gallery|cheats|guide|credits|achievements|restart|sandbox mode|changelog|faq)$/i.test(t)) continue;
        if (t.length > 220) continue;
        texts.add(t);
      }
      return texts.size;
    }).catch(() => 0);

    if (otherDistinct >= 2) break; // real menu; leave it for the play loop

    await confirmLoc.click({ force: true, timeout: 2500 }).catch(() => {});
    await frame.page().waitForTimeout(1200).catch(() => {});
  }
}

/**
 * Top-level setup: take a page on the portal, click through everything
 * until real gameplay begins. Returns the game frame handle.
 */
async function doSetup(page, context, { targetDomain = '', names = ['MC', 'Smith'] } = {}) {
  if (targetDomain) await dismissAllPopups(context, targetDomain);
  const portalClicked = await clickPortalPlay(page);
  if (portalClicked) await page.waitForTimeout(5000);
  const frame = await findGameFrame(page);
  await dismissDisclaimers(frame);
  await fillNameEntry(frame, { names });
  await page.waitForTimeout(2000);
  await selectDefaultAvatar(frame);
  await page.waitForTimeout(2000);
  await dismissInfoModals(frame);
  await page.waitForTimeout(1500);
  return frame;
}

module.exports = {
  dismissAllPopups,
  clickPortalPlay,
  findGameFrame,
  dismissDisclaimers,
  fillNameEntry,
  selectDefaultAvatar,
  dismissInfoModals,
  doSetup,
};
