// v2 classifier — behavioral.
//
// Idea: instead of trying to identify chrome / sidebar / arrow / choice via
// text regex + x-position, we LET THE ENGINE TELL US what each element does.
//
// Every click is an observation. Over time, the classifier builds a cache
// mapping element-identity → one of:
//   story     : clicking changes SugarCube passage (advances narrative)
//   action    : clicking changes State.variables but NOT passage
//                (inventory toggle, setting change, scene-internal action)
//   chrome    : clicking changes neither passage nor variables
//                (sidebar item that opens a modal auto-dismissed, dead link, etc.)
//   mixed     : varied outcomes across observations (rare; treat carefully)
//   pending   : never observed yet; cautiously try
//
// Element identity is deliberately coarse — text + tag + position bucket + size
// bucket — so the same button stays identified across passages and restores.
//
// Safety:
//   A tiny hardcoded regex prevents clicking obviously irreversible buttons
//   (Restart, Delete Save, New Game). This is the ONE intentional hardcode.
//
// Cache is persisted to saves/element_classes.json in the game's output dir,
// so learning survives across sessions.

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { Classifier } = require('./interface');

// The legitimate hardcode: elements matching any of these are NEVER clicked.
// Kept short and audited. Extend with care.
const IRREVERSIBLE_RE = /^(restart|new\s+game|delete\s+save|erase\s+save|clear\s+save|reset\s+progress|wipe\s+data)$/i;

// Engine-reserved: sidebar menus that open overlays and take control away —
// we know we don't want to trial-click these, they typically just open
// settings/gallery modals. Treating these as chrome before the first click
// saves time; once classified they'd land here anyway.
const CHROME_HINT_RE = /^(options|settings|achievements|gallery|cheats?|credits|saves?|guide|walkthrough|changelog|faq|help|about|menu|inventory|quests?|relations?|journal|map|stats?|phone|sandbox(\s+mode)?)$/i;

function hashElement(el) {
  // Stable-ish identity for an element across passage visits:
  //   text + tag + rounded-position-bucket + rounded-size-bucket.
  // We DON'T use exact coords — same button moves a few pixels between passages.
  const bucketX = Math.round((el.x || 0) / 100);
  const bucketY = Math.round((el.y || 0) / 100);
  const bucketW = Math.round((el.w || 0) / 50);
  const bucketH = Math.round((el.h || 0) / 25);
  const key = [
    (el.t || '').trim().slice(0, 120),
    (el.tag || '').toLowerCase(),
    `x${bucketX}`, `y${bucketY}`, `w${bucketW}`, `h${bucketH}`,
  ].join('|');
  return crypto.createHash('sha1').update(key).digest('hex').slice(0, 12);
}

class V2BehavioralClassifier extends Classifier {
  constructor(opts = {}) {
    super(opts);
    // Map of element-id → {
    //   class, text, tag, observations, passage_changes, var_changes, no_changes, last_seen_at
    // }
    this.cache = new Map();
    this.cacheFile = this.workDir ? path.join(this.workDir, 'saves', 'element_classes.json') : null;
    // Track passage-stability: elements seen on many passages → likely chrome
    // (even if we haven't trial-clicked them yet).
    this.elementAppearances = new Map(); // id → Set<passage>
    this.totalPassagesSeen = 0;
    this.passagesSeen = new Set();
    // Pending click — what we just decided to try, awaiting observeOutcome
    this._pendingClick = null;
  }

  name() { return 'v2-behavioral'; }
  describe() { return 'classifies elements by observed engine-state change after trial clicks; learns per game'; }

  async load() {
    if (!this.cacheFile || !fs.existsSync(this.cacheFile)) return;
    try {
      const raw = JSON.parse(fs.readFileSync(this.cacheFile, 'utf8'));
      for (const [id, entry] of Object.entries(raw.cache || {})) this.cache.set(id, entry);
      for (const [id, arr] of Object.entries(raw.appearances || {})) this.elementAppearances.set(id, new Set(arr));
      this.totalPassagesSeen = raw.totalPassagesSeen || 0;
      this.passagesSeen = new Set(raw.passagesSeen || []);
      this.log(`v2 cache loaded: ${this.cache.size} elements, ${this.passagesSeen.size} passages`);
    } catch (e) { this.log('v2 cache load failed: ' + e.message); }
  }

  async persist() {
    if (!this.cacheFile) return;
    const appearances = {};
    for (const [id, set] of this.elementAppearances.entries()) appearances[id] = Array.from(set);
    const data = {
      version: 2,
      updated_at: new Date().toISOString(),
      cache: Object.fromEntries(this.cache),
      appearances,
      totalPassagesSeen: this.totalPassagesSeen,
      passagesSeen: Array.from(this.passagesSeen),
    };
    fs.mkdirSync(path.dirname(this.cacheFile), { recursive: true });
    fs.writeFileSync(this.cacheFile, JSON.stringify(data, null, 2));
  }

  _recordAppearance(id, passage) {
    if (!this.elementAppearances.has(id)) this.elementAppearances.set(id, new Set());
    this.elementAppearances.get(id).add(passage || '?');
  }

  _isUbiquitous(id) {
    // An element present on more than half the passages we've ever seen is almost
    // certainly chrome (sidebar / header). Use this as a pre-classification hint.
    const appearances = this.elementAppearances.get(id);
    if (!appearances) return false;
    if (this.passagesSeen.size < 4) return false; // too little data
    return appearances.size / this.passagesSeen.size > 0.5;
  }

  _getClass(id) {
    const entry = this.cache.get(id);
    if (entry) return entry.class;
    if (this._isUbiquitous(id)) return 'chrome';
    return 'pending';
  }

  async classify(items, context) {
    const { passage } = context;
    if (passage && !this.passagesSeen.has(passage)) {
      this.passagesSeen.add(passage);
      this.totalPassagesSeen++;
    }

    const annotated = items.map((el) => {
      const id = hashElement(el);
      this._recordAppearance(id, passage);
      const cls = this._getClass(id);
      const irreversible = IRREVERSIBLE_RE.test((el.t || '').trim());
      const chromeHint = CHROME_HINT_RE.test((el.t || '').trim());
      return { ...el, _id: id, _class: cls, _irreversible: irreversible, _chromeHint: chromeHint };
    });

    // Destination-novelty check: if every destination we've recorded is already
    // in our global passagesSeen set, this element is "exhausted" — still
    // clickable if we have nothing better, but demoted within its band.
    const isExhausted = (a) => {
      const entry = this.cache.get(a._id);
      if (!entry || !entry.destinations || entry.destinations.length === 0) return false;
      return entry.destinations.every((p) => this.passagesSeen.has(p));
    };

    // Burn: a stronger retirement. After ≥3 clicks with zero novel destinations,
    // we've learned all this element can teach us. Stop picking it — not even
    // as fallback. This breaks loops like Preferences ↔ Return where both
    // elements are "story" class but lead only to each other's passages.
    const isBurned = (a) => {
      const entry = this.cache.get(a._id);
      if (!entry) return false;
      if (entry.observations < 3) return false;
      if (!entry.destinations || entry.destinations.length === 0) return false;
      return entry.destinations.every((p) => this.passagesSeen.has(p));
    };

    // Candidates: exclude chrome, irreversible, and burned elements.
    // Burned items are retired completely — they can't even be fallback picks.
    let burnedCount = 0;
    const candidates = annotated.filter((a) => {
      if (a._irreversible) return false;
      if (a._class === 'chrome') return false;
      if (a._chromeHint && a._class !== 'story' && a._class !== 'action') return false;
      if (isBurned(a)) { burnedCount++; return false; }
      return true;
    });
    const seen = new Set();
    const unique = candidates.filter((c) => (seen.has(c._id) ? false : (seen.add(c._id), true)));

    // Priority bands (highest to lowest):
    //   1. story (passage + vars change — real progress)
    //   2. pending (unknown, must trial-click to learn)
    //   3. action (vars change only — in-scene state like inventory toggle)
    //   4. navigation (passage-only change — menu open/close)
    //   5. mixed (observed both ways; uncertain)
    // Within each band, elements whose destinations are all already-seen go last.
    const bandOf = (c) => {
      if (c._class === 'story') return 1;
      if (c._class === 'pending') return 2;
      if (c._class === 'action') return 3;
      if (c._class === 'navigation') return 4;
      if (c._class === 'mixed') return 5;
      return 6;
    };
    const scored = unique.map((c) => ({
      el: c,
      band: bandOf(c),
      exhausted: isExhausted(c),
    }));
    scored.sort((a, b) => {
      if (a.band !== b.band) return a.band - b.band;
      if (a.exhausted !== b.exhausted) return a.exhausted ? 1 : -1;
      return 0;
    });
    const ordered = scored.map((s) => s.el);

    // Interpretation:
    // - If top band has 2+ non-exhausted candidates → branch (real decision point)
    // - If top band has exactly 1 non-exhausted → advance
    // - Otherwise fall back to whatever is available, even exhausted
    let decisions = [];
    let advance = null;
    let menuType = 'none';

    const fresh = scored.filter((s) => !s.exhausted);
    const topBand = fresh.length ? fresh[0].band : (scored.length ? scored[0].band : null);
    const topCandidates = fresh.filter((s) => s.band === topBand).map((s) => s.el);

    if (topCandidates.length >= 2) {
      decisions = topCandidates;
      menuType = topBand === 1 ? 'branch' : (topBand === 2 ? 'pending_menu' : 'navigation_menu');
    } else if (topCandidates.length === 1) {
      advance = topCandidates[0];
      menuType = topBand === 1 ? 'advance' : (topBand === 2 ? 'single' : 'navigation');
    } else if (ordered.length) {
      // All remaining candidates are exhausted (but not burned). Still pick to
      // avoid stalling — they may teach us something new if the state has
      // advanced since we last tried them.
      advance = ordered[0];
      menuType = 'exhausted';
    } else if (burnedCount > 0) {
      // Everything we can click is burned. Don't click — the orchestrator
      // should backtrack from the frontier. Nothing new to learn from here.
      menuType = 'all_burned';
    }

    const rejected = annotated
      .filter((a) => a._class === 'chrome' || a._irreversible || isBurned(a))
      .map((a) => {
        let reason = 'chrome';
        if (a._irreversible) reason = 'irreversible';
        else if (isBurned(a)) reason = 'burned';
        return { t: a.t, reason, id: a._id };
      });

    return { decisions, advance, safe_to_ignore: rejected, menu_type: menuType, meta: { cache_size: this.cache.size, burned_count: burnedCount } };
  }

  /**
   * Record what happened after a click.
   *
   * `clickLanded` (default true) indicates whether the click physically reached
   * the intended element. When false — because the element was offscreen, a
   * locator timeout fired, or coords were out of bounds — we record that an
   * attempt was made but do NOT count it toward the four outcome buckets.
   * Otherwise a missed click would look identical to a successful click on
   * a chrome element (no state change either way), and the classifier would
   * wrongly burn a potentially-important element as chrome.
   */
  async observeOutcome({ clicked, before, after, clickLanded = true }) {
    if (!clicked || !clicked._id) return;
    const id = clicked._id;

    let entry = this.cache.get(id);
    if (!entry) {
      entry = {
        class: 'pending',
        text: (clicked.t || '').slice(0, 120),
        tag: clicked.tag,
        observations: 0,
        passage_changes: 0,
        var_changes: 0,
        story_hits: 0,        // passage + vars both changed
        nav_hits: 0,          // passage only
        action_hits: 0,       // vars only
        no_changes: 0,
        missed_attempts: 0,   // click never landed — not counted toward outcome buckets
        destinations: [],     // unique post-click passages (for novelty check)
        last_seen_at: new Date().toISOString(),
      };
      this.cache.set(id, entry);
    }
    entry.last_seen_at = new Date().toISOString();

    if (!clickLanded) {
      entry.missed_attempts++;
      // Leave `class` unchanged — this observation tells us nothing about the
      // element's true behaviour. The element stays `pending` (or whatever it
      // already was) and can be retried on a later tick when coords are valid.
      return;
    }

    const passageChanged = (before && after) && (before.passage !== after.passage);
    let varsChanged = false;
    if (before && after) {
      try { varsChanged = JSON.stringify(before.variables || {}) !== JSON.stringify(after.variables || {}); } catch (e) {}
    }
    // Four-way outcome: distinguish real progress (passage + vars change)
    // from pure navigation (passage changes but vars don't — menu toggles).
    entry.observations++;
    if (passageChanged) entry.passage_changes++;
    if (varsChanged) entry.var_changes++;
    if (passageChanged && varsChanged) entry.story_hits++;
    else if (passageChanged) entry.nav_hits++;
    else if (varsChanged) entry.action_hits++;
    else entry.no_changes++;
    if (after && after.passage && !entry.destinations.includes(after.passage)) {
      entry.destinations.push(after.passage);
      if (entry.destinations.length > 20) entry.destinations.shift();
    }

    // Re-derive class from four-way tally: majority vote.
    const t = entry.observations;
    const s = entry.story_hits, n = entry.nav_hits, a = entry.action_hits, z = entry.no_changes;
    let newClass;
    if (s / t >= 0.5) newClass = 'story';
    else if (n / t >= 0.5) newClass = 'navigation';
    else if (a / t >= 0.5) newClass = 'action';
    else if (z / t >= 0.5) newClass = 'chrome';
    else newClass = 'mixed';
    entry.class = newClass;
  }
}

module.exports = { V2BehavioralClassifier, hashElement, IRREVERSIBLE_RE, CHROME_HINT_RE };
