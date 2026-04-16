'use strict';
// Phase 0 — Pre-game auto-advance + UI recon for the twine-game-explorer skill.
//
// Runs once, after `setup.js::doSetup` returns the game iframe, before Claude
// makes its first narrative click. Produces `game_explorations/<slug>/ui_map.json`
// — a structured catalog of every chrome region, every safe chrome button, and
// what each reveals (modal / panel / self-returning passage / no-visible-effect).
//
// Two halves:
//   Phase 0a — autoAdvancePregame: closes SugarCube modals, clicks forward
//              buttons (Play/Continue/Start/etc), fills name inputs, leaves
//              preference toggles at defaults. Terminates when no FORWARD_PATTERN
//              matches any visible clickable.
//   Phase 0b — runUiRecon: six stages (scan regions, detect toggles, probe
//              toggles, catalog contents, probe chrome buttons, write artifact).
//
// All DOM introspection runs via frame.evaluate(). Snap/restore are invoked via
// injected callables so this module doesn't pull in the engine module directly.

const fs = require('fs');
const path = require('path');

// ============================================================================
// Constants
// ============================================================================

const FORWARD_PATTERNS = [
  /^(play|start|begin|new\s+game)\b/i,
  /^(i\s+understand|i\s+agree|yes)\b/i,
  /^(i\s+)?(accept|confirm)$/i,
  /^(continue|next|proceed|start\s+your\s+journey)\b/i,
  /^(skip\s+intro|skip)\b/i,
];

const DANGER_PATTERNS = /\b(exit|quit|decline|cancel|back|not\s+my\s+type|no,?\s+thanks)\b/i;

const PROBE_SKIP = {
  destructive: /\b(restart|new\s+game|delete\s+save|reset|confirm\s+ending)\b/i,
  save_mutation: /\b(saves?|save\s+game|quick\s+save|save\s+slot)\b/i,
  exit: /\b(exit|quit|leave\s+game)\b/i,
  external: /\b(discord|patreon|subscribestar|reddit|twitter|support|feedback|report.?a.?bug)\b/i,
};

const MAX_PREGAME_CLICKS = 15;
const PROBE_BUDGET = 20;
const PROBE_TIMEOUT_MS = 8000;
const TOGGLE_PROBE_PASSES = 5;
const TOGGLE_SCORE_MIN = 5;
const REGION_MIN_AREA = 400;
const EDGE_TOLERANCE = 24;

const MODAL_CLOSE_SELECTORS = [
  '#ui-dialog-close',
  '.ui-close',
  'button[title="Close" i]',
  'button[aria-label="Close" i]',
  'a[title="Close" i]',
  'a[aria-label="Close" i]',
];

// ============================================================================
// Adaptive wait — poll engine + DOM until click takes effect
// ============================================================================

// Capture a "settlement marker" — a snapshot of indicators that change when a
// click takes effect. Used as the baseline for waitForChange.
async function captureMarker(frame) {
  return await frame.evaluate(() => {
    const out = {};
    try {
      if (typeof SugarCube !== 'undefined' && SugarCube.State) {
        out.passage = SugarCube.State.passage || '';
        out.historyLen = SugarCube.State.history ? SugarCube.State.history.length : 0;
      }
    } catch (e) {}
    try { out.bodyTextLen = (document.body.innerText || '').length; } catch (e) { out.bodyTextLen = 0; }
    return out;
  }).catch(() => ({}));
}

// Wait until the engine state OR DOM shows a change vs the baseline marker.
// Returns when any of these change:
//   - SugarCube.State.passage (passage navigation)
//   - SugarCube.State.history.length (turn appended via Engine.play)
//   - document.body.innerText.length (modal opened, content swapped, etc.)
// Caps at timeoutMs. Returns { settled, wait_ms, signal }.
async function waitForChange(page, frame, baseMarker, { timeoutMs = 5000, pollMs = 150, settleAfterChangeMs = 200 } = {}) {
  const startTime = Date.now();
  const deadline = startTime + timeoutMs;
  const DOM_LEN_THRESHOLD = 20; // ignore tiny text fluctuations (timer ticks etc.)

  while (Date.now() < deadline) {
    const post = await frame.evaluate(() => {
      const out = {};
      try {
        if (typeof SugarCube !== 'undefined' && SugarCube.State) {
          out.passage = SugarCube.State.passage || '';
          out.historyLen = SugarCube.State.history ? SugarCube.State.history.length : 0;
        }
      } catch (e) {}
      try { out.bodyTextLen = (document.body.innerText || '').length; } catch (e) { out.bodyTextLen = 0; }
      return out;
    }).catch(() => null);

    if (post) {
      const passageChanged = baseMarker.passage !== undefined && post.passage !== baseMarker.passage;
      const historyGrew = baseMarker.historyLen !== undefined && post.historyLen > baseMarker.historyLen;
      const domChanged = baseMarker.bodyTextLen !== undefined && Math.abs((post.bodyTextLen || 0) - (baseMarker.bodyTextLen || 0)) > DOM_LEN_THRESHOLD;

      if (passageChanged || historyGrew || domChanged) {
        // Click took effect. Brief settle wait so DOM finishes mid-render frames.
        await page.waitForTimeout(settleAfterChangeMs);
        return {
          settled: true,
          wait_ms: Date.now() - startTime,
          signal: passageChanged ? 'passage_changed' : (historyGrew ? 'history_grew' : 'dom_changed'),
        };
      }
    }
    await page.waitForTimeout(pollMs);
  }
  return { settled: false, wait_ms: Date.now() - startTime, signal: 'timeout' };
}

// ============================================================================
// Phase 0a — Pre-game auto-advance
// ============================================================================

async function autoAdvancePregame({ page, frame, engineMod, stateMod, dirs, name = 'Player', maxClicks = MAX_PREGAME_CLICKS, logger = () => {} }) {
  const trail = [];
  const seenPassages = new Set();
  const filledOnPassages = new Set(); // avoid re-filling same inputs in a loop
  let lastForwardText = null; // track consecutive same-passage + same-button clicks
  let lastForwardPassage = null;
  let samePassageSameButtonCount = 0;

  // Adaptive settle — wait until the engine is loaded AND an interactive element
  // exists in the main content area. Unlike waiting for all DOM to stabilize
  // (which takes 16s on BTF due to background images/animations), this checks
  // only for INTERACTION readiness: engine has a passage + at least one link/button
  // is visible in the content area. Then a brief 500ms extra for JS event handlers.
  {
    const settleDeadline = Date.now() + 10000;
    while (Date.now() < settleDeadline) {
      await page.waitForTimeout(300);
      const ready = await frame.evaluate(() => {
        try {
          if (typeof SugarCube !== 'undefined' && SugarCube.State && SugarCube.State.passage) {
            for (const el of document.querySelectorAll('a, button, [role="button"]')) {
              const cs = getComputedStyle(el);
              if (cs.visibility === 'hidden' || cs.display === 'none') continue;
              const r = el.getBoundingClientRect();
              if (r.x > 316 && r.width > 30 && r.height > 15) return true;
            }
          }
        } catch (e) {}
        return false;
      }).catch(() => false);
      if (ready) break;
    }
    await page.waitForTimeout(500);
  }

  for (let step = 0; step < maxClicks; step++) {
    let info;
    try { info = await engineMod.introspect(frame); } catch (e) { info = { passage: null, variables: {} }; }
    const passage = info.passage || '<unknown>';
    const hash = stateMod.hashState({ passage, variables: info.variables || {} });

    // A. Modal dismiss
    const modalMethod = await dismissModal(page, frame).catch(() => null);
    if (modalMethod) {
      trail.push({ step, passage, action: 'dismissed_modal', method: modalMethod });
      logger(`phase0a: dismissed modal (${modalMethod}) at "${passage}"`);
      await page.waitForTimeout(500);
      continue;
    }

    // B. Forward-button search
    const forward = await findForwardCandidate(frame).catch(() => null);
    if (forward) {
      try {
        const preFwdMarker = await captureMarker(frame);
        // Click via JS el.click() instead of Playwright locator — bypasses
        // visibility/stability checks that timeout on slow-transition games (BTF).
        const clickResult = await frame.evaluate((targetText) => {
          for (const el of document.querySelectorAll('a, button, [role="button"], [onclick]')) {
            const cs = getComputedStyle(el);
            if (cs.display === 'none') continue;
            const t = (el.textContent || '').trim();
            if (t === targetText) { el.click(); return { ok: true }; }
          }
          return { ok: false };
        }, forward.text);
        if (!clickResult.ok) throw new Error(`no clickable element with text "${forward.text}"`);
        trail.push({ step, passage, action: 'clicked_forward', text: forward.text, tier: forward.tier });
        logger(`phase0a: clicked "${forward.text}" (tier ${forward.tier}) on "${passage}"`);
        // Adaptive wait — handles slow-transition games (BTF) without slowing fast ones
        await waitForChange(page, frame, preFwdMarker, { timeoutMs: 5000, pollMs: 150 });

        // Post-click termination checks
        let newInfo;
        try { newInfo = await engineMod.introspect(frame); } catch (e) { newInfo = { passage: null, variables: {} }; }
        const newHash = stateMod.hashState({ passage: newInfo.passage, variables: newInfo.variables || {} });
        if (newHash === hash) {
          trail.push({ step, passage, action: 'terminated', reason: 'state_unchanged_after_click' });
          logger(`phase0a: terminated (state didn't change after click)`);
          break;
        }
        seenPassages.add(passage);
        if (seenPassages.has(newInfo.passage) && newInfo.passage !== passage) {
          trail.push({ step, passage: newInfo.passage, action: 'terminated', reason: 'cycle_detected' });
          logger(`phase0a: terminated (cycle — re-entered "${newInfo.passage}")`);
          break;
        }
        // Same passage + same button text + same source passage as last click = stuck.
        // The three-way check avoids false positives when the SAME button text ("Continue")
        // appears across different passages (intro2 → Continue → intro3 → Continue is fine;
        // intro3 → Continue → intro3 → Continue is stuck). One same-passage click is OK
        // (may be a legitimate scroll/advance). Fires on the second consecutive match.
        if (newInfo.passage === passage && forward.text === lastForwardText && passage === lastForwardPassage) {
          samePassageSameButtonCount++;
          if (samePassageSameButtonCount >= 1) {
            trail.push({ step, passage, action: 'terminated', reason: 'same_passage_same_button_consecutive' });
            logger(`phase0a: terminated (clicked "${forward.text}" on "${passage}" consecutively with no passage change)`);
            break;
          }
        } else {
          samePassageSameButtonCount = 0;
        }
        lastForwardText = forward.text;
        lastForwardPassage = passage;
        continue;
      } catch (e) {
        trail.push({ step, passage, action: 'click_failed', text: forward.text, error: e.message });
        logger(`phase0a: click failed for "${forward.text}": ${e.message}`);
        break;
      }
    }

    // C. Text input prefill — only once per passage (otherwise re-filling loops forever
    // when no forward match is available on a passage that has text inputs).
    if (!filledOnPassages.has(passage)) {
      const filledAny = await maybeFillNameInputs(frame, name).catch(() => false);
      if (filledAny) {
        filledOnPassages.add(passage);
        trail.push({ step, passage, action: 'filled_name', value: name });
        logger(`phase0a: filled name input(s) with "${name}"`);
        await page.waitForTimeout(500);
        continue;
      }
    }

    // D. No forward match, no modal, no input → terminate
    trail.push({ step, passage, action: 'terminated', reason: 'no_forward_pattern_match' });
    logger(`phase0a: terminated (no forward button match on passage "${passage}")`);
    break;
  }

  // Write trail to pregame log
  try {
    if (trail.length) {
      const lines = trail.map((e) => JSON.stringify({ ts: new Date().toISOString(), ...e })).join('\n') + '\n';
      fs.appendFileSync(dirs.pregameLog, lines);
    }
  } catch (e) { /* non-fatal */ }

  return { trail, terminated_at: trail.length > 0 ? trail[trail.length - 1] : null };
}

// Detect whether a blocking modal is currently visible.
// Returns a string tag describing the modal, or null if no blocking modal exists.
// Excludes SugarCube's always-present `#ui-overlay` (backdrop, not a real dialog).
async function detectBlockingModal(frame) {
  return await frame.evaluate(() => {
    // Primary signal: SugarCube's standard dialog
    const d = document.querySelector('#ui-dialog');
    if (d) {
      const cs = getComputedStyle(d);
      if (d.classList.contains('open') && cs.display !== 'none' && cs.visibility !== 'hidden') {
        return 'ui_dialog_open';
      }
    }
    // Secondary: any other high-z fixed element with substantial visible area
    const vw = window.innerWidth, vh = window.innerHeight;
    let best = null;
    for (const el of document.querySelectorAll('*')) {
      if (el.id === 'ui-overlay' || el.id === 'ui-dialog') continue; // already handled / always-present
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) continue;
      if (cs.position !== 'fixed') continue;
      const z = parseInt(cs.zIndex) || 0;
      if (z < 50) continue;
      const r = el.getBoundingClientRect();
      const visW = Math.max(0, Math.min(r.x + r.width, vw) - Math.max(r.x, 0));
      const visH = Math.max(0, Math.min(r.y + r.height, vh) - Math.max(r.y, 0));
      const visArea = visW * visH;
      if (visArea < 50000) continue; // require meaningful coverage
      if (visArea > vw * vh * 0.95) continue; // full-viewport = backdrop
      if (!best || z > best.z) {
        best = { z, id: el.id || '', cls: (el.className || '').toString().slice(0, 40) };
      }
    }
    return best ? `custom_modal:${best.id || best.cls || 'anon'}` : null;
  }).catch(() => null);
}

// Try standard modal close chain. Returns method name or null.
// IMPORTANT: only returns non-null if a blocking modal was detected before AND is gone after.
async function dismissModal(page, frame) {
  // Step 0: verify a blocking modal exists right now
  const initialModal = await detectBlockingModal(frame);
  if (!initialModal) return null;

  // Helper: after attempting a close, verify it's actually gone.
  const tryMethod = async (methodName, action) => {
    try {
      await action();
      await page.waitForTimeout(300);
      const still = await detectBlockingModal(frame);
      if (!still) return methodName;
    } catch (e) { /* fall through */ }
    return null;
  };

  // Step 1: SugarCube + generic close selectors
  for (const sel of MODAL_CLOSE_SELECTORS) {
    let visible = false;
    try { visible = await frame.locator(sel).first().isVisible({ timeout: 150 }); } catch (e) {}
    if (!visible) continue;
    const got = await tryMethod(sel, async () => {
      await frame.locator(sel).first().click({ force: true, timeout: 2000 });
    });
    if (got) return got;
  }

  // Step 2: × glyph text click (FontAwesome times U+F00D or Unicode ×/✕/✖/⨯)
  const xCandidates = ['×', '✕', '✖', '⨯', '\uf00d'];
  for (const ch of xCandidates) {
    let visible = false;
    try { visible = await frame.locator(`text="${ch}"`).first().isVisible({ timeout: 150 }); } catch (e) {}
    if (!visible) continue;
    const got = await tryMethod(`x_glyph:${ch.charCodeAt(0).toString(16)}`, async () => {
      await frame.locator(`text="${ch}"`).first().click({ force: true, timeout: 2000 });
    });
    if (got) return got;
  }

  // Step 3: Escape key
  const got = await tryMethod('escape_key', async () => {
    await page.keyboard.press('Escape');
  });
  if (got) return got;

  return null;
}

async function findForwardCandidate(frame) {
  const patterns = FORWARD_PATTERNS.map((p) => p.source);
  const dangerSrc = DANGER_PATTERNS.source;

  const candidates = await frame.evaluate(({ patternsSrc, dangerSrc }) => {
    const pats = patternsSrc.map((s) => new RegExp(s, 'i'));
    const danger = new RegExp(dangerSrc, 'i');
    const out = [];
    const els = document.querySelectorAll('a, button, [role="button"], [onclick]');
    for (const el of els) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.3) continue;
      const r = el.getBoundingClientRect();
      if (r.width * r.height < 100) continue;
      const txt = (el.textContent || '').trim();
      if (!txt || txt.length > 80) continue;
      if (danger.test(txt)) continue;
      // Strip leading non-word chars (emoji, icons) before pattern-testing, since forward
      // patterns anchor at ^ and game buttons often prefix with 🎮 / ▶️ / 🚀 etc.
      const stripped = txt.replace(/^[^\p{L}\p{N}]+/u, '');
      for (let tier = 0; tier < pats.length; tier++) {
        if (pats[tier].test(stripped)) {
          out.push({ text: txt, tier: tier + 1, bbox: { x: r.x, y: r.y, w: r.width, h: r.height } });
          break;
        }
      }
    }
    return out;
  }, { patternsSrc: patterns, dangerSrc }).catch(() => []);

  if (candidates.length) {
    candidates.sort((a, b) => a.tier - b.tier);
    const best = candidates[0];
    const escaped = best.text.replace(/"/g, '\\"');
    return { text: best.text, tier: best.tier, selector: `:text-is("${escaped}")`, bbox: best.bbox };
  }

  // Tier 5 fallback: exactly ONE non-chrome non-external clickable in the main content area
  // (catches transition buttons like "📚 History" or "Begin Chapter 2" that don't match any pattern).
  // Strict: only fires when low-ambiguity (≤2 visible non-chrome non-external candidates).
  const fallback = await frame.evaluate(({ dangerSrc }) => {
    const danger = new RegExp(dangerSrc, 'i');
    const externalRe = /\b(discord|patreon|subscribestar|reddit|twitter|support|feedback|report.?a.?bug|changelog)\b/i;
    const vw = window.innerWidth, vh = window.innerHeight;
    const out = [];
    for (const el of document.querySelectorAll('a, button, [role="button"]')) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.3) continue;
      const r = el.getBoundingClientRect();
      if (r.width * r.height < 1000) continue; // require a substantial button (not tiny icons)
      // Skip edge-flush (sidebar/chrome)
      if (r.x < 320 || r.x + r.width > vw - 320 || r.y < 50 || r.y + r.height > vh - 50) {
        // Allow if it's clearly central content (e.g. extends into the central region)
        if (r.x < 320 && r.x + r.width < vw - 320) continue;
        if (r.x > 320 && r.x + r.width > vw - 320) continue;
      }
      const txt = (el.textContent || '').trim();
      if (!txt || txt.length > 80) continue;
      if (danger.test(txt)) continue;
      if (externalRe.test(txt)) continue;
      const target = el.getAttribute('target') || '';
      const href = el.getAttribute('href') || '';
      if (target === '_blank' || /^https?:\/\//.test(href)) continue;
      out.push({ text: txt, bbox: { x: r.x, y: r.y, w: r.width, h: r.height } });
    }
    // De-dup by exact text
    const seen = new Set();
    const uniq = out.filter((c) => { if (seen.has(c.text)) return false; seen.add(c.text); return true; });
    return uniq;
  }, { dangerSrc }).catch(() => []);

  if (fallback.length === 1) {
    const best = fallback[0];
    const escaped = best.text.replace(/"/g, '\\"');
    return { text: best.text, tier: 5, selector: `:text-is("${escaped}")`, bbox: best.bbox };
  }

  return null;
}

async function maybeFillNameInputs(frame, name) {
  const inputs = await frame.$$('input[type="text"]:visible, input:not([type]):visible, textarea:visible').catch(() => []);
  if (!inputs.length) return false;
  for (let i = 0; i < Math.min(inputs.length, 2); i++) {
    try {
      const val = i === 0 ? name : (name === 'Player' ? 'Smith' : name);
      await inputs[i].fill(val);
    } catch (e) { /* keep going */ }
  }
  return true;
}

// ============================================================================
// Phase 0b Stage 1 — Region detection
// ============================================================================

async function scanRegions(frame) {
  const result = await frame.evaluate(({ EDGE, MIN_AREA }) => {
    const vw = window.innerWidth, vh = window.innerHeight;

    function classify(r) {
      const top = r.y < EDGE;
      const bot = r.y + r.height > vh - EDGE;
      const left = r.x < EDGE;
      const right = r.x + r.width > vw - EDGE;
      const fullW = r.width > vw * 0.6;
      const fullH = r.height > vh * 0.6;
      const coversAll = fullW && fullH && r.width > vw * 0.9 && r.height > vh * 0.9;
      if (coversAll) return 'overlay_or_page';
      if (top && left && !fullW && !fullH) return 'corner_tl';
      if (top && right && !fullW && !fullH) return 'corner_tr';
      if (bot && left && !fullW && !fullH) return 'corner_bl';
      if (bot && right && !fullW && !fullH) return 'corner_br';
      if (left && fullH) return 'left';
      if (right && fullH) return 'right';
      if (top && fullW) return 'top';
      if (bot && fullW) return 'bottom';
      if (top) return 'top_partial';
      if (bot) return 'bottom_partial';
      if (left) return 'left_partial';
      if (right) return 'right_partial';
      return 'floating';
    }

    // Pass A: structural scan
    const pool = [];
    const poolSet = new Set();
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) continue;
      if (el === document.body || el === document.documentElement) continue;
      const r = el.getBoundingClientRect();
      if (r.width * r.height < MIN_AREA) continue;
      if (r.x + r.width < 0 || r.y + r.height < 0 || r.x > vw || r.y > vh) continue;
      const touchesEdge = r.x < EDGE || r.y < EDGE || r.x + r.width > vw - EDGE || r.y + r.height > vh - EDGE;
      const positioned = ['fixed', 'sticky', 'absolute'].includes(cs.position);
      if (!touchesEdge && !positioned) continue;
      pool.push({ el, r, cs, positioned });
      poolSet.add(el);
    }

    // Identify the main-content area: largest element that spans all four edges
    let mainEl = null, mainArea = 0;
    for (const { el, r } of pool) {
      const spansAll = r.x < EDGE && r.y < EDGE && r.x + r.width > vw - EDGE && r.y + r.height > vh - EDGE;
      if (!spansAll) continue;
      const a = r.width * r.height;
      if (a > mainArea) { mainArea = a; mainEl = el; }
    }

    // Pass A: dedupe nested via parent.contains
    const candidates = [];
    for (const p of pool) {
      if (mainEl && (p.el === mainEl || mainEl.contains(p.el))) continue;
      let hasParentInPool = false;
      let parent = p.el.parentElement;
      while (parent && parent !== document.body) {
        if (poolSet.has(parent)) { hasParentInPool = true; break; }
        parent = parent.parentElement;
      }
      if (hasParentInPool) continue;

      const cls = (p.el.className && p.el.className.toString) ? p.el.className.toString() : '';
      const collapsed = /\b(stowed|collapsed|closed|hidden)\b/i.test(cls);

      candidates.push({
        pos_class: classify(p.r),
        tag: p.el.tagName.toLowerCase(),
        id: p.el.id || '',
        cls: cls.slice(0, 80),
        position_style: p.cs.position,
        z_index: p.cs.zIndex,
        collapsed,
        bbox: { x: Math.round(p.r.x), y: Math.round(p.r.y), w: Math.round(p.r.width), h: Math.round(p.r.height) },
        text_sample: (p.el.textContent || '').trim().slice(0, 80),
      });
    }

    // Pass B: corner/midpoint sampling to catch flow-laid-out regions we may have missed
    const samples = [
      { name: 'top_left', x: 10, y: 10 },
      { name: 'top_right', x: vw - 10, y: 10 },
      { name: 'bottom_left', x: 10, y: vh - 10 },
      { name: 'bottom_right', x: vw - 10, y: vh - 10 },
      { name: 'left_mid', x: 10, y: Math.floor(vh / 2) },
      { name: 'right_mid', x: vw - 10, y: Math.floor(vh / 2) },
      { name: 'top_mid', x: Math.floor(vw / 2), y: 10 },
      { name: 'bottom_mid', x: Math.floor(vw / 2), y: vh - 10 },
    ];
    const sampled = [];
    for (const s of samples) {
      const el = document.elementFromPoint(s.x, s.y);
      if (!el || el === document.documentElement || el === document.body) continue;
      if (mainEl && mainEl.contains(el)) continue;
      // Walk up to the nearest ancestor with meaningful id/class
      let cur = el;
      while (cur && cur !== document.body) {
        if (cur.id || (cur.className && cur.className.toString && cur.className.toString().trim())) break;
        cur = cur.parentElement;
      }
      if (!cur || cur === document.body) continue;
      const r = cur.getBoundingClientRect();
      const cs = getComputedStyle(cur);
      const cls = (cur.className && cur.className.toString) ? cur.className.toString() : '';
      sampled.push({
        sample: s.name,
        tag: cur.tagName.toLowerCase(),
        id: cur.id || '',
        cls: cls.slice(0, 80),
        position_style: cs.position,
        bbox: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
      });
    }

    return {
      viewport: { w: vw, h: vh },
      main_content: mainEl ? { tag: mainEl.tagName.toLowerCase(), id: mainEl.id || '', cls: (mainEl.className || '').toString().slice(0, 60) } : null,
      candidates,
      sampled,
    };
  }, { EDGE: EDGE_TOLERANCE, MIN_AREA: REGION_MIN_AREA }).catch(() => ({ viewport: null, main_content: null, candidates: [], sampled: [] }));

  // Merge: include sampled regions whose id isn't already covered by a candidate
  const covered = new Set(result.candidates.map((c) => c.id).filter(Boolean));
  for (const s of result.sampled || []) {
    if (!s.id || covered.has(s.id)) continue;
    result.candidates.push({
      pos_class: 'sampled',
      tag: s.tag, id: s.id, cls: s.cls,
      position_style: s.position_style,
      z_index: 'auto',
      collapsed: /\b(stowed|collapsed|closed|hidden)\b/i.test(s.cls || ''),
      bbox: s.bbox,
      text_sample: '',
      from_sampling: true,
    });
    covered.add(s.id);
  }

  return result;
}

// ============================================================================
// Phase 0b Stage 2 — Toggle candidate hunt
// ============================================================================

async function detectToggles(frame) {
  return await frame.evaluate(({ EDGE, MIN_SCORE }) => {
    const vw = window.innerWidth, vh = window.innerHeight;
    const TOGGLE_GLYPHS = ['≡', '☰', '◀', '▶', '▲', '▼', '‹', '›', '×', '✕'];
    const CLASS_HINT = /toggle|burger|drawer|collapse|expand|hamburger/i;
    const LABEL_HINT = /toggle|expand|collapse|menu|drawer|hamburger/i;

    const out = [];
    for (const el of document.querySelectorAll('button, a, div, span, i, svg')) {
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) continue;
      const r = el.getBoundingClientRect();
      if (r.width * r.height < 16) continue;
      if (r.x + r.width < 0 || r.y + r.height < 0 || r.x > vw || r.y > vh) continue;
      const txt = (el.textContent || '').trim();
      if (txt.length > 30 && !TOGGLE_GLYPHS.includes(txt)) continue;

      const title = el.getAttribute('title') || '';
      const aria = el.getAttribute('aria-label') || '';
      const ariaExpanded = el.getAttribute('aria-expanded');
      const cls = (el.className && el.className.toString) ? el.className.toString() : '';
      const cursorPointer = cs.cursor === 'pointer';
      const hasOnClick = !!el.onclick || !!el.getAttribute('onclick') || el.tagName === 'BUTTON' || el.tagName === 'A';
      const near = {
        top: r.y < EDGE, bot: r.y + r.height > vh - EDGE,
        left: r.x < EDGE, right: r.x + r.width > vw - EDGE,
      };
      const edgeFlush = near.top || near.bot || near.left || near.right;
      const small = r.width < 40 && r.height < 40;
      const narrow = (r.width < 30 && r.height > 80) || (r.height < 30 && r.width > 80);

      const reasons = [];
      let score = 0;
      if (ariaExpanded !== null) { score += 5; reasons.push(`aria-expanded=${ariaExpanded}`); }
      if (TOGGLE_GLYPHS.includes(txt)) { score += 4; reasons.push(`glyph:${txt}`); }
      if (LABEL_HINT.test(title) || LABEL_HINT.test(aria)) { score += 4; reasons.push('label-says-toggle'); }
      if (narrow && edgeFlush) { score += 4; reasons.push('narrow-edge-strip'); }
      if (small && edgeFlush) { score += 2; reasons.push('small-edge-button'); }
      if (CLASS_HINT.test(cls)) { score += 2; reasons.push('class-hint'); }
      if (cursorPointer && edgeFlush && small) { score += 1; reasons.push('clickable-edge-small'); }
      if (hasOnClick && edgeFlush && (small || narrow)) { score += 1; reasons.push('clickable-edge'); }

      if (score < MIN_SCORE) continue;
      out.push({
        score, reasons,
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        cls: cls.slice(0, 60),
        title, aria_label: aria, aria_expanded: ariaExpanded,
        text: txt.slice(0, 30),
        bbox: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
        edge: Object.keys(near).filter((k) => near[k]).join('+') || 'none',
      });
    }
    // Dedupe by bbox
    const seen = new Set();
    const kept = [];
    out.sort((a, b) => b.score - a.score);
    for (const c of out) {
      const key = `${c.bbox.x},${c.bbox.y},${c.bbox.w}x${c.bbox.h}`;
      if (seen.has(key)) continue;
      seen.add(key);
      kept.push(c);
    }
    return kept.slice(0, 20);
  }, { EDGE: EDGE_TOLERANCE, MIN_SCORE: TOGGLE_SCORE_MIN }).catch(() => []);
}

// ============================================================================
// Phase 0b Stage 3 — Toggle probe
// ============================================================================

async function probeToggles({ page, frame, snap, restore, variablesDiffFn, logger = () => {} }) {
  const results = [];
  let totalReveals = 0;

  for (let pass = 0; pass < TOGGLE_PROBE_PASSES; pass++) {
    const regions = await scanRegions(frame);
    const regionHashBefore = fingerprintRegions(regions);
    const toggles = await detectToggles(frame);
    if (!toggles.length) break;

    let passReveals = 0;
    for (const t of toggles) {
      // Skip already-probed this pass
      if (results.some((r) => r.bbox.x === t.bbox.x && r.bbox.y === t.bbox.y && r.pass === pass)) continue;

      let snapId = null;
      try { snapId = await snap(`toggle_probe_pass${pass}`); } catch (e) {}

      const variablesBefore = await getVariablesSnapshot(frame);

      const selector = t.id ? `#${t.id}` : buildFallbackSelector(t);
      let clickOk = false, clickErr = null;
      try {
        await frame.locator(selector).first().click({ force: true, timeout: 2500 });
        clickOk = true;
      } catch (e) { clickErr = e.message; }
      await page.waitForTimeout(250);

      const variablesAfter = await getVariablesSnapshot(frame);
      const diff = variablesDiffFn(variablesBefore, variablesAfter);
      const stateMutated = diff && (Object.keys(diff.changed || {}).length || Object.keys(diff.added || {}).length || Object.keys(diff.removed || {}).length);

      if (stateMutated) {
        if (snapId) { try { await restore(snapId); } catch (e) {} }
        results.push({ pass, ...t, result: 'stateful_chrome', state_mutated: true, error: clickErr || null });
        continue;
      }

      const regionsAfter = await scanRegions(frame);
      const regionHashAfter = fingerprintRegions(regionsAfter);
      if (regionHashAfter !== regionHashBefore) {
        results.push({ pass, ...t, result: 'reveal', error: clickErr || null });
        passReveals++;
        totalReveals++;
      } else {
        results.push({ pass, ...t, result: clickOk ? 'no_visible_effect' : 'click_failed', error: clickErr || null });
      }
    }

    logger(`phase0b stage3 pass ${pass}: ${passReveals} reveals (${toggles.length} candidates scanned)`);
    if (passReveals === 0) break; // no new regions appeared, stop re-scanning
  }

  return { probes: results, total_reveals: totalReveals };
}

// Hash region list by sorted {id, bbox}
function fingerprintRegions(regions) {
  const list = (regions.candidates || [])
    .map((c) => `${c.id || c.tag}:${c.bbox.x},${c.bbox.y},${c.bbox.w}x${c.bbox.h}:${c.collapsed ? 'c' : 'o'}`)
    .sort();
  return require('crypto').createHash('sha1').update(list.join('|')).digest('hex').slice(0, 16);
}

async function getVariablesSnapshot(frame) {
  return await frame.evaluate(() => {
    try { if (window.SugarCube && window.SugarCube.State) return JSON.parse(JSON.stringify(window.SugarCube.State.variables || {})); } catch (e) {}
    try { if (window.Harlowe) return {}; } catch (e) {}
    return {};
  }).catch(() => ({}));
}

function buildFallbackSelector(candidate) {
  if (candidate.title) return `[title="${candidate.title.replace(/"/g, '\\"')}" i]`;
  if (candidate.aria_label) return `[aria-label="${candidate.aria_label.replace(/"/g, '\\"')}" i]`;
  if (candidate.text) return `:text-is("${candidate.text.replace(/"/g, '\\"')}")`;
  return `${candidate.tag}.${(candidate.cls || '').split(/\s+/).filter(Boolean)[0] || ''}`;
}

// ============================================================================
// Phase 0b Stage 4 — Region content catalog
// ============================================================================

async function catalogRegions(frame, regions) {
  const idsToCatalog = (regions.candidates || [])
    .filter((c) => c.id)
    .filter((c) => ['left', 'right', 'top', 'bottom', 'left_partial', 'right_partial', 'sampled', 'corner_tl', 'corner_tr', 'corner_bl', 'corner_br', 'floating'].includes(c.pos_class));

  const cataloged = [];
  for (const region of idsToCatalog) {
    const entry = await frame.evaluate(({ id }) => {
      const root = document.getElementById(id);
      if (!root) return null;
      const rr = root.getBoundingClientRect();

      // Interactive elements
      const interactive = [];
      const inters = root.querySelectorAll('button, a, [onclick], [role="button"]');
      for (const el of inters) {
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const r = el.getBoundingClientRect();
        if (r.width * r.height < 20) continue;
        const txt = (el.textContent || '').trim();
        const href = el.getAttribute('href') || '';
        const target = el.getAttribute('target') || '';
        const title = el.getAttribute('title') || el.getAttribute('aria-label') || '';
        interactive.push({
          tag: el.tagName.toLowerCase(),
          id: el.id || '',
          cls: (el.className || '').toString().slice(0, 50),
          text: txt.slice(0, 60),
          title, href, target,
          external: target === '_blank' || /^https?:\/\//.test(href),
          bbox: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
        });
      }

      // Detection mode 1: heading-based cards
      const headings = [];
      for (const h of root.querySelectorAll('h1, h2, h3, h4, [class*=title], [class*=header], [class*=card-title]')) {
        const cs = getComputedStyle(h);
        if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const t = (h.textContent || '').trim().slice(0, 50);
        if (!t) continue;
        headings.push({ text: t, tag: h.tagName.toLowerCase(), cls: (h.className || '').toString().slice(0, 40) });
      }
      const seenHeading = new Set();
      const sections = headings.filter((h) => {
        if (seenHeading.has(h.text)) return false;
        seenHeading.add(h.text);
        return true;
      });

      // Detection mode 2: flat menu — if no headings but interactive <a> elements look like a menu
      let menu_list = null;
      if (sections.length === 0) {
        const aLinks = interactive.filter((i) => i.tag === 'a' && i.text && !i.external);
        if (aLinks.length >= 3) {
          // Check if they share x-coordinate and width (within 5px)
          const xs = aLinks.map((a) => a.bbox.x);
          const ws = aLinks.map((a) => a.bbox.w);
          const sameX = Math.max(...xs) - Math.min(...xs) < 5;
          const sameW = Math.max(...ws) - Math.min(...ws) < 5;
          if (sameX && sameW) {
            menu_list = aLinks.map((a) => a.text);
          }
        }
      }

      // Passive text samples — text nodes visible that aren't inside buttons/links
      const passive_text = [];
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode()) && passive_text.length < 20) {
        const t = node.textContent.trim();
        if (!t || t.length < 2) continue;
        const parent = node.parentElement;
        if (!parent) continue;
        if (parent.closest('button, a, [role="button"], [onclick]')) continue;
        passive_text.push(t.slice(0, 60));
      }

      return {
        id,
        bbox: { x: Math.round(rr.x), y: Math.round(rr.y), w: Math.round(rr.width), h: Math.round(rr.height) },
        cls: (root.className || '').toString(),
        collapsed: /\b(stowed|collapsed|closed|hidden)\b/i.test(root.className || ''),
        sections,
        menu_list,
        interactive,
        passive_text_samples: passive_text,
      };
    }, { id: region.id }).catch(() => null);

    if (entry) cataloged.push({ pos_class: region.pos_class, ...entry });
  }

  return cataloged;
}

// ============================================================================
// Phase 0b Stage 5 — Active chrome button probe
// ============================================================================

function classifySkip(label, href, target) {
  if (!label) return null;
  if (target === '_blank') return 'external';
  if (href && /^https?:\/\//.test(href)) return 'external';
  for (const [cat, re] of Object.entries(PROBE_SKIP)) {
    if (re.test(label)) return cat;
  }
  return null;
}

async function probeChromeButtons({ page, frame, regionsCataloged, snap, restore, dirs, budget = PROBE_BUDGET, logger = () => {} }) {
  // Flatten interactive buttons across all regions, de-duped by bbox
  const flat = [];
  const seen = new Set();
  for (const region of regionsCataloged) {
    for (const it of region.interactive || []) {
      const key = `${it.bbox.x},${it.bbox.y},${it.bbox.w}x${it.bbox.h}`;
      if (seen.has(key)) continue;
      seen.add(key);
      // Skip if clearly not a "real" button (empty text and no title)
      const label = it.text || it.title;
      if (!label) continue;
      // Skip history back/forward and ui-bar-toggle — those are handled elsewhere
      if (/^(ui-bar-toggle|history-backward|history-forward|right-ui-bar-toggle)$/.test(it.id || '')) continue;
      flat.push({ region_id: region.id, ...it, label });
    }
  }

  const probes = [];
  let probed = 0;
  for (const button of flat) {
    if (probed >= budget) {
      probes.push({ label: button.label, bbox: button.bbox, region_id: button.region_id, skipped_reason: 'budget_exceeded' });
      continue;
    }
    const skipReason = classifySkip(button.label, button.href, button.target);
    if (skipReason) {
      probes.push({ label: button.label, bbox: button.bbox, region_id: button.region_id, skipped_reason: skipReason });
      continue;
    }

    probed++;
    logger(`phase0b stage5: probing "${button.label}" (${probed}/${budget})`);
    const probe = await probeOneButton({ page, frame, button, snap, restore, dirs, logger });
    probes.push(probe);
  }

  return { probes, probed_count: probed };
}

async function probeOneButton({ page, frame, button, snap, restore, dirs, logger }) {
  const start = Date.now();
  const safeLabel = (button.label || 'unknown').replace(/[^a-zA-Z0-9_-]+/g, '_').slice(0, 50);
  const screenshotPath = path.join(dirs.uiProbes, `${safeLabel}.png`);

  let snapId = null;
  try { snapId = await snap(`probe_${safeLabel}`); } catch (e) {}

  let selector;
  if (button.id) {
    selector = `#${button.id}`;
  } else {
    const regionSel = button.region_id ? `#${button.region_id}` : '';
    const textSafe = button.label.replace(/"/g, '\\"');
    selector = regionSel ? `${regionSel} >> :text-is("${textSafe}")` : `:text-is("${textSafe}")`;
  }

  // Capture pre-click baseline so we can diff what the click revealed.
  // innerText is the right granularity: it's the rendered (post-CSS) text,
  // matching what the player actually sees.
  let preText = '';
  try {
    preText = await frame.evaluate(() => String(document.body.innerText || '')).catch(() => '');
  } catch (e) {}

  let clickOk = false, clickErr = null;
  const probePreMarker = await captureMarker(frame);
  try {
    await frame.locator(selector).first().click({ force: true, timeout: 3000 });
    clickOk = true;
  } catch (e) { clickErr = e.message; }

  if (clickOk) {
    await waitForChange(page, frame, probePreMarker, { timeoutMs: 4000, pollMs: 150 });
  }

  // ----- M4: structured post-click content extraction -----
  // Grab three views of the revealed content:
  //   panel_text        — innerText of the most likely panel container
  //                       (#ui-dialog if a modal opened, otherwise the full
  //                       body minus the pre-click baseline)
  //   dialog_text       — #ui-dialog innerText in isolation (null if no modal)
  //   post_click_text   — full-body innerText post-click (for completeness;
  //                       downstream analysis may want to diff its own way)
  //   post_click_elements — structured list of visible interactive elements
  //                         (tag, text, title, href, bbox) so downstream can
  //                         see e.g. "Phone panel revealed contacts: Kyle, Ben"
  //                         without re-parsing text.
  // No truncation — same contract as M1 body capture.
  let postContent = { post_click_text: '', dialog_text: null, panel_text: '', post_click_elements: [] };
  if (clickOk) {
    try {
      postContent = await frame.evaluate(({ baselineText }) => {
        const fullText = String(document.body.innerText || '');
        let dialogText = null;
        const dialog = document.getElementById('ui-dialog');
        if (dialog) {
          const cs = dialog.ownerDocument.defaultView
            ? dialog.ownerDocument.defaultView.getComputedStyle(dialog) : null;
          const open = dialog.classList.contains('open')
            || (cs && cs.display !== 'none' && cs.visibility !== 'hidden');
          if (open) {
            const body = dialog.querySelector('#ui-dialog-body') || dialog;
            const t = String(body.innerText || '').trim();
            if (t) dialogText = t;
          }
        }

        // panel_text: prefer the dialog's text when a modal opened; otherwise
        // diff baseline against full text to isolate the revealed delta.
        let panelText = dialogText || '';
        if (!panelText) {
          // Crude but effective: whatever is in fullText but not baselineText,
          // line-by-line. Ordering preserved from fullText.
          const baseLines = new Set((baselineText || '').split('\n').map((l) => l.trim()).filter(Boolean));
          const newLines = [];
          for (const line of fullText.split('\n')) {
            const t = line.trim();
            if (!t) continue;
            if (!baseLines.has(t)) newLines.push(line);
          }
          panelText = newLines.join('\n');
        }

        // Structured interactive elements currently visible. Same selector set
        // as the rest of the toolkit for consistency (choices.js).
        const elements = [];
        const sel = 'button, a, input[type=button], input[type=submit], [onclick], [role=button]';
        for (const el of document.querySelectorAll(sel)) {
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 4 || r.height < 4) continue;
          const txt = (el.textContent || '').trim();
          const title = el.getAttribute('title') || el.getAttribute('aria-label') || '';
          const href = el.getAttribute('href') || '';
          const target = el.getAttribute('target') || '';
          elements.push({
            tag: el.tagName.toLowerCase(),
            id: el.id || '',
            cls: String(el.className || '').slice(0, 60),
            text: txt,   // no truncation — same as M1 spec
            title, href, target,
            external: target === '_blank' || /^https?:\/\//.test(href),
            bbox: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
          });
        }

        return {
          post_click_text: fullText,
          dialog_text: dialogText,
          panel_text: panelText,
          post_click_elements: elements,
        };
      }, { baselineText: preText }).catch(() => postContent);
    } catch (e) { /* swallow — probe record still gets the PNG */ }
  }

  try { await page.screenshot({ path: screenshotPath, timeout: 3000 }); } catch (e) {}

  if (snapId) {
    try { await restore(snapId); } catch (e) {}
    await waitForChange(page, frame, probePreMarker, { timeoutMs: 3000, pollMs: 150 });
  }

  return {
    label: button.label, bbox: button.bbox, region_id: button.region_id,
    screenshot_path: screenshotPath,
    click_ok: clickOk,
    error: clickErr || null,
    duration_ms: Date.now() - start,
    // M4: structured panel content
    panel_text: postContent.panel_text || null,
    dialog_text: postContent.dialog_text || null,
    post_click_text: postContent.post_click_text || null,
    post_click_elements: postContent.post_click_elements || [],
  };
}

// ============================================================================
// M4: Passive sidebar state reader (non-clicking, safe to call every turn)
// ============================================================================

/**
 * Read the current contents of sidebar regions WITHOUT clicking anything.
 * Returns a compact structured snapshot + a content fingerprint hash so the
 * daemon can detect mid-game sidebar changes (stats updating, quest text
 * advancing, new phone contacts appearing, etc.) without disturbing the
 * game state.
 *
 * Takes the regions_catalog from Phase 0b as the set of regions to scan.
 * If no catalog is supplied (e.g. Phase 0 was skipped), falls back to any
 * element with id `ui-bar`, `sidebar`, or matching SugarCube conventions.
 */
async function captureSidebarState(frame, regionsCataloged) {
  const regionIds = (regionsCataloged || [])
    .filter((r) => r.id)
    .map((r) => r.id);
  const targetIds = regionIds.length
    ? regionIds
    : ['ui-bar', 'ui-bar-body', 'sidebar', 'right-ui-bar', 'right-ui-bar-body'];

  return await frame.evaluate((ids) => {
    const out = { regions: [], captured_at: Date.now() };
    for (const id of ids) {
      const root = document.getElementById(id);
      if (!root) continue;
      const cs = getComputedStyle(root);
      // Skip truly hidden regions; collapsed-but-visible-strip regions still
      // have some text so capture them.
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;

      const rr = root.getBoundingClientRect();
      const innerText = String(root.innerText || '');
      // Structured interactive list — cheap and high-signal.
      const interactive = [];
      for (const el of root.querySelectorAll('button, a, [onclick], [role="button"], input[type=button], input[type=submit]')) {
        const ecs = getComputedStyle(el);
        if (ecs.visibility === 'hidden' || ecs.display === 'none' || parseFloat(ecs.opacity) === 0) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) continue;
        const text = (el.textContent || '').trim();
        const title = el.getAttribute('title') || el.getAttribute('aria-label') || '';
        const href = el.getAttribute('href') || '';
        const target = el.getAttribute('target') || '';
        interactive.push({
          tag: el.tagName.toLowerCase(),
          id: el.id || '',
          text, title, href, target,
          external: target === '_blank' || /^https?:\/\//.test(href),
          bbox: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
        });
      }
      out.regions.push({
        id,
        bbox: { x: Math.round(rr.x), y: Math.round(rr.y), w: Math.round(rr.width), h: Math.round(rr.height) },
        collapsed: /\b(stowed|collapsed|closed|hidden)\b/i.test(root.className || ''),
        inner_text: innerText,
        interactive,
      });
    }
    return out;
  }, targetIds);
}

/**
 * Compact fingerprint of a sidebar state. Collapses whitespace so trivial
 * re-renders (e.g. cursor blink, transient class changes) don't trip the
 * change detector. The hash is a 16-char sha1 prefix — the same convention
 * the state hashes use.
 */
function fingerprintSidebar(sidebarState) {
  const crypto = require('crypto');
  const parts = [];
  for (const r of sidebarState.regions || []) {
    const text = (r.inner_text || '').replace(/\s+/g, ' ').trim();
    const interactiveSig = (r.interactive || []).map((i) => `${i.tag}|${i.text}|${i.title}|${i.href}`).join(';');
    parts.push(`${r.id}::${text}::${interactiveSig}`);
  }
  return crypto.createHash('sha1').update(parts.join('||')).digest('hex').slice(0, 16);
}

// ============================================================================
// Phase 0b Stage 6 — Write artifact
// ============================================================================

function writeUiMap(dirs, uiMapObj) {
  try {
    fs.mkdirSync(dirs.uiProbes, { recursive: true });
    fs.writeFileSync(dirs.uiMap, JSON.stringify(uiMapObj, null, 2));
  } catch (e) { /* non-fatal */ }
  // Seed notes.md with a UI frame section if not present
  try {
    const notesPath = dirs.notes;
    let existing = '';
    if (fs.existsSync(notesPath)) existing = fs.readFileSync(notesPath, 'utf8');
    if (!/## UI frame/.test(existing)) {
      const summary = renderNotesSummary(uiMapObj);
      const header = existing.startsWith('#') ? '' : `# Notes for ${uiMapObj.slug || 'game'}\n\n`;
      fs.writeFileSync(notesPath, header + summary + '\n' + existing);
    }
  } catch (e) { /* non-fatal */ }
}

function renderNotesSummary(uiMap) {
  const lines = ['## UI frame (auto-generated by Phase 0)', ''];
  if (uiMap.pregame_auto_advance && uiMap.pregame_auto_advance.trail && uiMap.pregame_auto_advance.trail.length) {
    lines.push('### Pre-game auto-advance');
    for (const e of uiMap.pregame_auto_advance.trail) {
      lines.push(`- step ${e.step} [${e.passage}] ${e.action}${e.text ? ` — "${e.text}"` : ''}${e.method ? ` (${e.method})` : ''}${e.reason ? ` (${e.reason})` : ''}`);
    }
    lines.push('');
  }
  lines.push('### Regions');
  for (const region of uiMap.regions_catalog || []) {
    lines.push(`- **${region.pos_class}** (${region.id || '<anon>'}) bbox=${JSON.stringify(region.bbox)}${region.collapsed ? ' **[collapsed]**' : ''}`);
    if (region.sections && region.sections.length) {
      lines.push(`  - sections: ${region.sections.map((s) => s.text).join(' / ')}`);
    }
    if (region.menu_list && region.menu_list.length) {
      lines.push(`  - menu: ${region.menu_list.join(' / ')}`);
    }
    if (region.passive_text_samples && region.passive_text_samples.length) {
      lines.push(`  - visible text: ${region.passive_text_samples.slice(0, 5).map((s) => s.replace(/\s+/g, ' ')).join(' | ')}`);
    }
  }
  if (uiMap.chrome_probes && uiMap.chrome_probes.length) {
    lines.push('');
    lines.push('### Chrome button probes');
    for (const p of uiMap.chrome_probes) {
      if (p.skipped_reason) {
        lines.push(`- ~~${p.label}~~ — skipped (${p.skipped_reason})`);
      } else {
        lines.push(`- **${p.label}** → ${p.click_ok ? `probed (screenshot: ${p.screenshot_path})` : `click failed: ${p.error}`}`);
      }
    }
  }
  lines.push('');
  return lines.join('\n');
}

// ============================================================================
// Orchestrator
// ============================================================================

async function runPhase0({ page, frame, context, engineMod, stateMod, engineInfo, dirs, snapshots, opts = {}, logger = () => {} }) {
  const {
    skipPhase0 = false,
    skipPregame = false,
    skipButtons = false,
    rerun = false,
    name = 'Player',
    slug = null,
    url = null,
  } = opts;

  if (skipPhase0) return null;
  if (fs.existsSync(dirs.uiMap) && !rerun) {
    try {
      const existing = JSON.parse(fs.readFileSync(dirs.uiMap, 'utf8'));
      logger(`phase0: ui_map.json exists, reusing (pass --rerun-phase0 to refresh)`);
      return existing;
    } catch (e) {
      logger(`phase0: existing ui_map.json unreadable, regenerating`);
    }
  }

  const ui = {
    slug, url,
    generated_at: new Date().toISOString(),
    engine: engineInfo ? engineInfo.engine : null,
    pregame_auto_advance: null,
    regions_catalog: [],
    chrome_probes: [],
  };

  try { fs.mkdirSync(dirs.uiProbes, { recursive: true }); } catch (e) {}

  // --- Phase 0a ---
  if (!skipPregame) {
    logger('phase0a: starting pre-game auto-advance');
    try {
      ui.pregame_auto_advance = await autoAdvancePregame({
        page, frame, engineMod, stateMod, dirs, name, logger,
      });
      logger(`phase0a: completed (${(ui.pregame_auto_advance.trail || []).length} steps)`);
    } catch (e) {
      ui.pregame_auto_advance = { error: e.message };
      logger(`phase0a: errored — ${e.message}`);
    }
  }

  // --- Phase 0b ---
  logger('phase0b: starting UI recon');

  // Build snap/restore callables backed by the daemon's snapshot registry
  const snap = async (note) => {
    const blob = await engineMod.snapshot(frame, { pathSoFar: [] });
    const crypto = require('crypto');
    const id = 'p0_' + crypto.createHash('sha1').update(JSON.stringify(blob) + Date.now()).digest('hex').slice(0, 8);
    snapshots.set(id, { id, blob, note: note || null, taken_at: Date.now(), passage: null, state_hash: null });
    return id;
  };
  const restore = async (id) => {
    const rec = snapshots.get(id);
    if (!rec) throw new Error(`snap ${id} not found`);
    return await engineMod.restore(page, frame, rec.blob, { reloadUrl: url });
  };

  // Stage 1 — scan regions
  let regions;
  try {
    regions = await scanRegions(frame);
    logger(`phase0b stage1: ${regions.candidates.length} regions found`);
  } catch (e) {
    ui.error = 'stage1: ' + e.message;
    logger(`phase0b stage1 errored: ${e.message}`);
    writeUiMap(dirs, ui);
    return ui;
  }

  // Stage 2+3 — toggle probe (only if there are any collapsed regions OR any toggle candidates)
  try {
    const collapsedExists = regions.candidates.some((c) => c.collapsed);
    if (collapsedExists) {
      const probeResult = await probeToggles({
        page, frame, snap, restore,
        variablesDiffFn: stateMod.diffVariables,
        logger,
      });
      ui.toggle_probes = probeResult;
      // Re-scan regions after toggle probing
      regions = await scanRegions(frame);
      logger(`phase0b stage3: after toggle probes, ${regions.candidates.length} regions visible`);
    } else {
      logger('phase0b stage3: skipped (no collapsed regions detected)');
    }
  } catch (e) {
    logger(`phase0b stage3 errored: ${e.message}`);
  }

  ui.regions = regions.candidates;
  ui.main_content = regions.main_content;

  // Stage 4 — catalog
  try {
    ui.regions_catalog = await catalogRegions(frame, regions);
    logger(`phase0b stage4: cataloged ${ui.regions_catalog.length} regions`);
  } catch (e) {
    ui.error = (ui.error || '') + ' stage4: ' + e.message;
    logger(`phase0b stage4 errored: ${e.message}`);
  }

  // Stage 5 — chrome button probes
  if (!skipButtons && ui.regions_catalog.length) {
    try {
      const probeRes = await probeChromeButtons({
        page, frame, regionsCataloged: ui.regions_catalog,
        snap, restore, dirs, logger,
      });
      ui.chrome_probes = probeRes.probes;
      ui.chrome_probes_count = probeRes.probed_count;
      logger(`phase0b stage5: probed ${probeRes.probed_count} buttons`);
    } catch (e) {
      ui.error = (ui.error || '') + ' stage5: ' + e.message;
      logger(`phase0b stage5 errored: ${e.message}`);
    }
  } else if (skipButtons) {
    logger('phase0b stage5: skipped (--skip-buttons)');
  }

  // Stage 6 — write
  ui.ui_frame_hash = fingerprintRegions({ candidates: ui.regions });
  writeUiMap(dirs, ui);
  logger(`phase0 complete: ui_map.json written`);

  return ui;
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Adaptive wait helpers
  captureMarker,
  waitForChange,
  // Phase 0a
  autoAdvancePregame,
  dismissModal,
  findForwardCandidate,
  // Phase 0b stages
  scanRegions,
  detectToggles,
  probeToggles,
  catalogRegions,
  probeChromeButtons,
  probeOneButton,
  writeUiMap,
  fingerprintRegions,
  // M4: passive sidebar readers
  captureSidebarState,
  fingerprintSidebar,
  // Orchestrator
  runPhase0,
  // Constants (exported for SKILL.md doc generation / tests)
  FORWARD_PATTERNS,
  DANGER_PATTERNS,
  PROBE_SKIP,
  MAX_PREGAME_CLICKS,
  PROBE_BUDGET,
  TOGGLE_SCORE_MIN,
};
