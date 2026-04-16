// Detect and classify interactive elements in the current game frame.
//
// Returns a list of "candidates" — clickable elements in the content region,
// excluding obvious sidebar/menu/nav items. Each has text, bounding box,
// and metadata (whether it's an arrow-like advance, a numbered/quiz option, etc.).
//
// Also classifies a batch of candidates as one of:
//   - "branch"       : 2-8 options, distinct text → narrative branch
//   - "action_loop"  : 5+ options with NSFW/action verbs → action menu
//   - "quiz"         : 3-5 options labelled a/b/c/d or 1/2/3/4 → quiz
//   - "payment"      : option text contains price ("$<number>")
//   - "location"     : "Go to X" / "Enter Y" style
//   - "advance"      : single arrow / Next / Continue

'use strict';

const SIDEBAR_TEXTS = /^(sandbox mode|options|achievements|gallery|guide|cheats|credits|saves|restart|changelog|bald games|money|home|menu|back|games|new games|top games|recently updated|ai .+|all games a-z|search|close|accept|cookies|sign in|login|register|faq|frequently asked questions|stats)$/i;
const ARROW_CHARS = /^[▶→›»▸▷◁◀←‹«◂◃]$/;
const PRICE_RE = /(?:^|\s)\$\s*\d+/;
const LOCATION_RE = /^(go to|enter|head to|visit|walk to)\b/i;
const QUIZ_SINGLE_RE = /^(a|b|c|d|e|1|2|3|4|5)$/i;
// Common verb patterns for action-menu items — ONLY the truly
// explicit, repeatable in-scene action vocabulary. Do NOT include general
// narrative verbs like "praise" or "tease" — those appear in normal
// branch choices ("Praise her / Warn her") and would cause misclassification.
const ACTION_VERB_RE = /^(lick (pussy|ass|balls|her)|blowjob|footjob|titjob|handjob|deepthroat|fuck(ing)?|make (her|him) cum|stand|cowgirl|doggy|missionary|reverse cowgirl|sideway|(missionary|doggy|cowgirl|behind|reverse cowgirl)\s+anal|anal|end|continue fucking|cum (in|on|inside)|lick balls)/i;

/** Grab all interactive elements in the frame with coords and text. */
async function listInteractive(frame) {
  return await frame.evaluate(() => {
    const sel = 'button, a, input[type=button], input[type=submit], [onclick], [role=button], img[onclick], div[onclick], span[onclick]';
    const out = [];
    for (const el of document.querySelectorAll(sel)) {
      const r = el.getBoundingClientRect();
      if (r.width < 8 || r.height < 8) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
      let t = (el.textContent || '').trim();
      if (!t) t = (el.getAttribute('value') || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim();
      out.push({
        t: t.slice(0, 240),
        x: Math.round(r.x),
        y: Math.round(r.y),
        w: Math.round(r.width),
        h: Math.round(r.height),
        tag: el.tagName.toLowerCase(),
      });
    }
    return out;
  });
}

/** Scroll every overflow-y scroll container within the frame to the bottom. */
async function scrollToBottom(frame) {
  await frame.evaluate(() => {
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
  }).catch(() => {});
}

function filterToContentRegion(items, { sidebarRightEdge = 270, frameWidth = null, rightSidebarStart = null } = {}) {
  const rightEdge = rightSidebarStart != null
    ? rightSidebarStart
    : (frameWidth != null ? frameWidth - Math.max(160, frameWidth * 0.18) : null);
  const reasons = [];
  const kept = items.filter((c) => {
    if (c.w > 720 || c.h > 120) { reasons.push({ t: c.t, reason: 'oversized', x: c.x, w: c.w }); return false; }
    if (c.x < sidebarRightEdge - 20) { reasons.push({ t: c.t, reason: 'left_sidebar', x: c.x }); return false; }
    if (rightEdge != null && c.x + c.w > rightEdge) { reasons.push({ t: c.t, reason: 'right_sidebar', x: c.x, w: c.w }); return false; }
    if (SIDEBAR_TEXTS.test(c.t)) { reasons.push({ t: c.t, reason: 'sidebar_text' }); return false; }
    if (/^\$/.test(c.t) && !/\s/.test(c.t)) { reasons.push({ t: c.t, reason: 'pure_price' }); return false; }
    if (!c.t && c.w < 30) { reasons.push({ t: c.t, reason: 'empty_small' }); return false; }
    return true;
  });
  kept._rejected = reasons;
  return kept;
}

/** Dedup a list by visible text. */
function dedupByText(items) {
  const seen = new Set();
  return items.filter((c) => (seen.has(c.t) ? false : (seen.add(c.t), true)));
}

/**
 * Classify a choice set.
 * Returns: { type, meta }
 */
function classify(items, { priorMenu = null } = {}) {
  if (items.length === 0) return { type: 'none' };
  if (items.length === 1) {
    const t = items[0].t;
    if (ARROW_CHARS.test(t.trim()) || /continue|next|advance/i.test(t)) return { type: 'advance' };
    return { type: 'single', meta: { text: t } };
  }

  const texts = items.map((c) => c.t.trim());
  const allQuiz = texts.every((t) => QUIZ_SINGLE_RE.test(t));
  if (allQuiz && texts.length >= 2 && texts.length <= 6) return { type: 'quiz', meta: { labels: texts } };

  const anyPrice = texts.some((t) => PRICE_RE.test(t));
  if (anyPrice) return { type: 'payment', meta: { prices: texts.map((t) => {
    const m = t.match(/\$\s*(\d+)/); return m ? Number(m[1]) : null;
  }) } };

  const allLoc = texts.every((t) => LOCATION_RE.test(t));
  if (allLoc) return { type: 'location', meta: { labels: texts } };

  const actionHits = texts.filter((t) => ACTION_VERB_RE.test(t.trim().toLowerCase())).length;
  // Action loops are long (5+ options) AND majority-action-vocabulary.
  // Short menus (2-4 options) with an occasional action word are normal branches.
  if (texts.length >= 5 && actionHits / texts.length >= 0.6) return { type: 'action_loop', meta: { actions: texts } };

  // Repeating menu check: only treat as action_loop if it's a large repeating menu
  // (short narrative menus may repeat when a click misses; don't punish that case)
  if (priorMenu && priorMenu.length === texts.length && texts.length >= 4 && priorMenu.every((t, i) => texts.includes(t))) {
    return { type: 'action_loop', meta: { actions: texts, repeat: true } };
  }

  if (texts.length >= 2 && texts.length <= 8) return { type: 'branch', meta: { options: texts } };
  return { type: 'other', meta: { labels: texts } };
}

/**
 * Pick the best element to click for "advance dialogue" when there's no choice.
 * Prefer top-header arrow, then bottom-most interactive in content, then blind click.
 */
function pickAdvance(items, { sidebarRightEdge = 270 } = {}) {
  const arrow = items.find((c) => c.y < 80 && c.x > sidebarRightEdge + 100);
  if (arrow) return arrow;
  const explicit = items.find((c) => ARROW_CHARS.test(c.t.trim()) || /next|continue|advance|skip/i.test(c.t));
  if (explicit) return explicit;
  const byY = items.slice().sort((a, b) => b.y - a.y);
  return byY[0] || null;
}

module.exports = {
  listInteractive, scrollToBottom, filterToContentRegion, dedupByText,
  classify, pickAdvance, SIDEBAR_TEXTS, ARROW_CHARS, PRICE_RE,
};
