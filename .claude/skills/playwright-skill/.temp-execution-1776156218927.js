const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME;
const SESSION_DIR = path.join(HOME, '.btf-session');
const PROFILE_DIR = path.join(SESSION_DIR, 'profile');
const SHOT_DIR = path.join(SESSION_DIR, 'screenshots');
const STATE_FILE = path.join(SESSION_DIR, 'state.json');
const LOG_FILE = path.join(SESSION_DIR, 'session.log');
const DOM_DUMP = path.join(SESSION_DIR, 'dom_recon.json');
const TARGET_URL = 'https://mopoga.com/back-to-freedom';
const DURATION_MS = 10 * 60 * 1000;
const TICK_MS = 1600;
const SCREENSHOT_EVERY_MS = 40 * 1000;
const STALE_THRESHOLD = 4;

fs.mkdirSync(PROFILE_DIR, { recursive: true });
fs.mkdirSync(SHOT_DIR, { recursive: true });

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  fs.appendFileSync(LOG_FILE, line + '\n');
}
async function shot(page, name) {
  const f = path.join(SHOT_DIR, `${Date.now()}_${name}.png`);
  try { await page.screenshot({ path: f }); return f; } catch (e) { log('shot fail: ' + e.message); return null; }
}

// DOM recon: dump every clickable / interactive element with coords + text
async function reconDom(frame) {
  return await frame.evaluate(() => {
    const out = [];
    const sel = 'button, a, input[type=button], input[type=submit], [onclick], [role=button], img[onclick], span[onclick], div[onclick]';
    for (const el of document.querySelectorAll(sel)) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const s = getComputedStyle(el);
      if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) continue;
      const t = (el.textContent || '').trim().slice(0, 120);
      const cls = (el.className && typeof el.className === 'string' ? el.className : '').slice(0, 80);
      out.push({ tag: el.tagName.toLowerCase(), t, cls, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
    }
    // scrollable containers
    const scr = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && el.scrollHeight > el.clientHeight + 10) {
        const r = el.getBoundingClientRect();
        scr.push({ cls: (el.className && typeof el.className === 'string' ? el.className : '').slice(0, 80), id: el.id, sh: el.scrollHeight, ch: el.clientHeight, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
      }
    }
    return { clickables: out, scrollables: scr };
  });
}

async function scrollToBottomInFrame(frame) {
  return await frame.evaluate(() => {
    const arr = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && el.scrollHeight > el.clientHeight + 10) {
        arr.push(el);
      }
    }
    arr.sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight));
    for (const el of arr.slice(0, 3)) el.scrollTop = el.scrollHeight;
    window.scrollTo(0, document.body.scrollHeight);
    return arr.length;
  });
}

async function domSignature(frame) {
  try {
    return await frame.evaluate(() => {
      // cheap signature: body length + text of first paragraph + time indicator text
      const body = document.body ? document.body.innerText : '';
      return body.length + '|' + body.slice(0, 200);
    });
  } catch (e) { return ''; }
}

(async () => {
  log('=== SESSION v5 START ===');
  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled', '--disable-popup-blocking'],
  });
  context.on('page', async (p) => {
    await p.waitForLoadState('domcontentloaded').catch(() => {});
    if (!p.url().includes('mopoga.com')) { log('closing popup: ' + p.url()); await p.close().catch(() => {}); }
  });
  let page = context.pages()[0] || await context.newPage();

  log('navigating');
  await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(3000);
  await shot(page, 'landing');

  const playBtn = page.locator('a:has-text("PLAY BACK TO FREEDOM"), button:has-text("PLAY BACK TO FREEDOM")').first();
  await playBtn.click({ timeout: 5000 }).catch((e) => log('play: ' + e.message));
  await page.waitForTimeout(6000);

  await page.waitForSelector('iframe[src*="embed"]', { timeout: 15000 }).catch(() => {});
  const gameFrame = page.frames().find((f) => f.url().includes('embed')) || page.frames().find((f) => f !== page.mainFrame());
  if (!gameFrame) { log('FATAL: no game frame'); await context.close(); return; }
  log('game frame: ' + gameFrame.url());
  await gameFrame.waitForLoadState('domcontentloaded').catch(() => {});
  await page.waitForTimeout(4000);

  // DISCLAIMER — loop until gone (the persistent profile might skip this if cookie set)
  for (let i = 1; i <= 6; i++) {
    const cBtn = gameFrame.locator('a:has-text("Continue"), button:has-text("Continue")').first();
    if (!(await cBtn.count().catch(() => 0))) break;
    log(`disclaimer ${i}`);
    await cBtn.click({ force: true, timeout: 3000 }).catch(() => {});
    await page.waitForTimeout(1600);
  }

  // NAME + AVATAR (skip if already past — persistent profile may remember)
  try {
    const inputs = await gameFrame.locator('input[type="text"], input:not([type])').all();
    if (inputs.length >= 2) {
      log('filling name');
      const names = ['MC', 'Smith'];
      for (let i = 0; i < Math.min(inputs.length, 2); i++) {
        if (await inputs[i].isVisible().catch(() => false)) {
          await inputs[i].fill(names[i]).catch(() => {});
        }
      }
      await page.waitForTimeout(800);
      const cBtn = gameFrame.locator('button:has-text("Confirm"), a:has-text("Confirm")').first();
      if (await cBtn.count().catch(() => 0)) {
        await cBtn.click({ force: true, timeout: 3000 }).catch(() => {});
        log('name confirm');
        await page.waitForTimeout(2500);
      }
    }
  } catch (e) { log('name err: ' + e.message); }

  // AVATAR screen — Confirm
  for (let i = 0; i < 3; i++) {
    const cBtn = gameFrame.locator('button:has-text("Confirm"):visible, a:has-text("Confirm"):visible').first();
    if (!(await cBtn.count().catch(() => 0))) break;
    log(`avatar/info confirm ${i}`);
    await cBtn.click({ force: true, timeout: 2000 }).catch(() => {});
    await page.waitForTimeout(2000);
  }
  await shot(page, 'post_setup');

  // ONE-TIME DOM RECON
  const recon = await reconDom(gameFrame);
  fs.writeFileSync(DOM_DUMP, JSON.stringify(recon, null, 2));
  log(`DOM recon: clickables=${recon.clickables.length} scrollables=${recon.scrollables.length}`);
  for (const s of recon.scrollables) log(`  scroll: cls=${s.cls} id=${s.id} h=${s.sh}/${s.ch}`);
  // Log clickables at top and bottom of viewport (likely advance/choice areas)
  const topClicks = recon.clickables.filter((c) => c.y < 80).slice(0, 10);
  const bottomClicks = recon.clickables.filter((c) => c.y > 600).slice(0, 10);
  for (const c of topClicks) log(`  top [${c.tag}] "${c.t.slice(0,40)}" @ ${c.x},${c.y}`);
  for (const c of bottomClicks) log(`  bot [${c.tag}] "${c.t.slice(0,40)}" @ ${c.x},${c.y}`);

  // PLAY LOOP
  const iframeEl = page.locator('iframe').first();
  const frameBox = (await iframeEl.boundingBox().catch(() => null)) || { x: 0, y: 0, width: 1440, height: 900 };
  const sidebarWidth = Math.max(200, frameBox.width * 0.18);
  const contentRegion = {
    x: frameBox.x + sidebarWidth + 20,
    y: frameBox.y + 60,
    width: frameBox.width - sidebarWidth - 40,
    height: frameBox.height - 120,
  };
  log('content region: ' + JSON.stringify(contentRegion));

  const sidebarTexts = /^(sandbox mode|options|achievements|gallery|guide|cheats|credits|saves|restart|changelog|bald games|money|home|menu|back|games|new games|top games|recently updated|faq|stats)$/i;

  const started = Date.now();
  let clicks = 0, choiceHits = 0, shots = 0, arrowClicks = 0;
  let lastShotAt = 0, lastSig = '', staleCount = 0;
  const observedChoices = [];

  log('entering play loop');
  while (Date.now() - started < DURATION_MS) {
    try {
      // 1. Scroll frame content to bottom (reveals any advance trigger)
      await scrollToBottomInFrame(gameFrame);
      await page.waitForTimeout(250);

      // 2. Re-scan interactive elements
      const snap = await gameFrame.evaluate(() => {
        const sel = 'button, a, input[type=button], [onclick], [role=button], img[onclick], div[onclick], span[onclick]';
        const out = [];
        for (const el of document.querySelectorAll(sel)) {
          const r = el.getBoundingClientRect();
          if (r.width < 8 || r.height < 8) continue;
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
          let t = (el.textContent || '').trim();
          if (!t) t = (el.getAttribute('value') || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim();
          out.push({ t, x: r.x, y: r.y, w: r.width, h: r.height, tag: el.tagName.toLowerCase() });
        }
        return { clickables: out, scrollY: window.scrollY, docH: document.body.scrollHeight };
      });

      // Filter to content-region clickables, exclude sidebar
      const candidates = snap.clickables.filter((c) => {
        if (c.w > 720 || c.h > 120) return false;
        // frame-relative; iframe content is in frame coords already
        if (c.x < sidebarWidth - 20) return false;
        if (sidebarTexts.test(c.t)) return false;
        if (!c.t && c.w < 30) return false;
        if (/^\$/.test(c.t)) return false;
        return true;
      });

      // Detect choice menu: multiple similar-sized buttons close together vertically
      const seen = new Set();
      const uniq = candidates.filter((c) => (seen.has(c.t) ? false : (seen.add(c.t), true)));

      let clicked = false;

      if (uniq.length >= 2 && uniq.length <= 8) {
        // Likely a choice menu in the content
        const list = uniq.map((c) => c.t.slice(0, 100));
        log(`CHOICE[${choiceHits}] (${list.length}): ${JSON.stringify(list)}`);
        observedChoices.push({ ts: new Date().toISOString(), options: list, picked: list[0] });
        await shot(page, `choice_${String(choiceHits).padStart(3, '0')}`);
        // Click first choice by coordinates (inside frame → add frameBox offset for page.mouse)
        const c = uniq[0];
        await page.mouse.click(frameBox.x + c.x + c.w / 2, frameBox.y + c.y + c.h / 2).catch(() => {});
        choiceHits++; clicks++; clicked = true;
        await page.waitForTimeout(2000);
      } else {
        // Advance: prefer top-right arrow (▶), else bottom-most clickable in content, else click at bottom of content
        // Look for arrow-like buttons in header area (y < 70)
        const arrow = candidates.find((c) => c.y < 70 && c.x > sidebarWidth + 100) ||
                      candidates.find((c) => /^[▶→›»]$/.test(c.t.trim()) || /next|continue|advance/i.test(c.t));
        if (arrow) {
          await page.mouse.click(frameBox.x + arrow.x + arrow.w / 2, frameBox.y + arrow.y + arrow.h / 2).catch(() => {});
          arrowClicks++; clicks++; clicked = true;
          await page.waitForTimeout(TICK_MS);
        } else if (candidates.length) {
          // Click the bottom-most candidate
          const byY = candidates.slice().sort((a, b) => b.y - a.y);
          const pick = byY[0];
          await page.mouse.click(frameBox.x + pick.x + pick.w / 2, frameBox.y + pick.y + pick.h / 2).catch(() => {});
          clicks++; clicked = true;
          await page.waitForTimeout(TICK_MS);
        } else {
          // Blind click at bottom of content
          const cx = contentRegion.x + contentRegion.width / 2;
          const cy = contentRegion.y + contentRegion.height - 40;
          await page.mouse.click(cx, cy).catch(() => {});
          clicks++;
          await page.waitForTimeout(TICK_MS);
        }
      }

      // Staleness check every few ticks
      if (clicks % 5 === 0) {
        const sig = await domSignature(gameFrame);
        if (sig === lastSig) {
          staleCount++;
          if (staleCount >= STALE_THRESHOLD) {
            log(`STALE x${staleCount} — escalating: press keys + click alternate region`);
            // Try pressing Enter / Space on focused iframe
            await gameFrame.locator('body').click({ force: true, position: { x: 400, y: 400 } }).catch(() => {});
            await page.keyboard.press('Enter').catch(() => {});
            await page.waitForTimeout(500);
            await page.keyboard.press('Space').catch(() => {});
            await page.waitForTimeout(500);
            // Click very bottom of the iframe
            await page.mouse.click(frameBox.x + frameBox.width * 0.6, frameBox.y + frameBox.height - 30).catch(() => {});
            staleCount = 0;
          }
        } else {
          staleCount = 0;
        }
        lastSig = sig;
      }

      if (Date.now() - lastShotAt > SCREENSHOT_EVERY_MS) {
        await shot(page, `progress_${String(shots).padStart(3, '0')}`);
        shots++;
        lastShotAt = Date.now();
        log(`tick ${Math.round((Date.now() - started) / 1000)}s clicks=${clicks} choices=${choiceHits} arrows=${arrowClicks} stale=${staleCount}`);
      }
    } catch (e) {
      log('loop err: ' + e.message);
      await page.waitForTimeout(2000);
    }
  }

  log(`=== TIME UP === clicks=${clicks} choices=${choiceHits} arrows=${arrowClicks} shots=${shots}`);
  await shot(page, 'zz_final_pre_save');

  // -- SAVE GAME -- try multiple strategies for the sidebar SAVES button
  const savedVia = [];
  const saveSelectors = [
    { kind: 'getByText', value: 'SAVES' },
    { kind: 'locator', value: 'text=/^\\s*SAVES\\s*$/' },
    { kind: 'locator', value: '*:has-text("SAVES"):not(:has(*))' },
    { kind: 'locator', value: '[class*="save" i]' },
  ];
  for (const ss of saveSelectors) {
    try {
      const loc = ss.kind === 'getByText' ? gameFrame.getByText(ss.value, { exact: true }) : gameFrame.locator(ss.value);
      const cnt = await loc.count().catch(() => 0);
      if (!cnt) continue;
      const visible = await loc.first().isVisible().catch(() => false);
      if (!visible) continue;
      log('SAVES via: ' + ss.value);
      await loc.first().click({ force: true, timeout: 3000 }).catch(() => {});
      await page.waitForTimeout(2500);
      await shot(page, 'zz_save_menu');
      // Try to click first save slot
      const slotSels = [
        'button:has-text("Save to Disk")',
        'button:has-text("Save 1")',
        'button:has-text("Slot 1")',
        'button:has-text("Empty Slot")',
        'button:has-text("SAVE")',
        '[class*="slot"]',
      ];
      for (const sel of slotSels) {
        const l = gameFrame.locator(sel).first();
        if (await l.count().catch(() => 0) && await l.isVisible().catch(() => false)) {
          await l.click({ force: true, timeout: 3000 }).catch(() => {});
          savedVia.push({ opener: ss.value, slot: sel });
          log('slot clicked: ' + sel);
          await page.waitForTimeout(2000);
          break;
        }
      }
      for (const sel of ['button:has-text("Yes"):visible', 'button:has-text("OK"):visible', 'button:has-text("Confirm"):visible']) {
        const l = gameFrame.locator(sel).first();
        if (await l.count().catch(() => 0)) {
          await l.click({ force: true, timeout: 2000 }).catch(() => {});
          log('confirm: ' + sel);
          await page.waitForTimeout(1500);
        }
      }
      await shot(page, 'zz_save_complete');
      break;
    } catch (e) { log('save attempt err: ' + e.message); }
  }

  // Dump storage from game frame + try IndexedDB presence
  let gameStorage = {};
  try {
    gameStorage = await gameFrame.evaluate(async () => {
      const ls = {};
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        const v = localStorage.getItem(k);
        ls[k] = typeof v === 'string' ? v.slice(0, 400) : v;
      }
      let idb = [];
      try { idb = (await indexedDB.databases?.()) || []; } catch (e) {}
      return {
        origin: location.origin,
        ls_keys: Object.keys(ls),
        ls_sample: ls,
        idb_names: idb.map((d) => d.name),
      };
    });
  } catch (e) { gameStorage = { error: e.message }; }

  const state = {
    last_session: new Date().toISOString(),
    target_url: TARGET_URL,
    game_frame_url: gameFrame.url(),
    duration_ms: Date.now() - started,
    clicks, choices: choiceHits, arrow_clicks: arrowClicks, screenshots: shots,
    saved_via: savedVia,
    cookies_count: (await context.cookies().catch(() => [])).length,
    game_storage: gameStorage,
    observed_choices: observedChoices,
    profile_dir: PROFILE_DIR,
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  log('state written');

  await page.waitForTimeout(3500);
  await context.close();
  log('=== SESSION END ===');
})();
