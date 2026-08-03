// Feature detector.
//
// Accumulates observations across the session and produces a running
// "what this game contains" inventory. Feeds report.md.
//
// Core loop: for each state snapshot + (optional) variable diff,
// classify changes and attribute them to categories:
//   - player stats (scalar number vars on the player)
//   - npc stats (per-NPC scalar numbers — love/lust/trust/etc.)
//   - items / inventory (array/list vars, plus consumable counts)
//   - body / appearance traits (body/hair/breast/outfit/pregnancy vars)
//   - flags (booleans that flip story milestones)
//   - time / calendar (day/hour/week counters)
//   - locations (passage transitions that feel like navigation)
//   - scenes (unique passages classified by scene type)
//   - prices / economy (numeric deltas on a money-ish var)
//
// All of this is heuristic. We err on the side of over-classifying and
// producing a rich catalogue the human can prune.

'use strict';

function capitalize(s) {
  if (!s) return s;
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

// Regex bank for variable-name classification.
// Note we match both WITH word boundaries (for dotted/underscored paths like
// `npc.angela.love` or `angela_love`) AND WITHOUT (for concatenated flat names
// like `angelalove`). BTF uses the flat pattern, so this matters.
const BODY_VARS = /(breast|bust|boob|cup|hair|body|weight|height|skin|tan|belly|pregnancy|pregnan|piercing|tattoo|scar|outfit|clothing|makeup|nails)/i;
const NPC_STAT_SUFFIXES = /(love|lust|trust|respect|friendship|affection|submission|dominance|obedience|fear|jealousy|arousal)$/i;
const PLAYER_STAT_VARS = /^(money|cash|gold|energy|stamina|sleep|hunger|fatigue|willpower|composure|charisma|intelligence|strength|dexterity|fitness|beauty|reputation|fame|skill|corruption)$/i;
const TIME_VARS = /^(day|hour|week|month|year|turn|time|calendar|morning|evening|night|afternoon|weekday)$/i;
const FLAG_SUFFIXES = /(_unlocked|_complete|_seen|_met|_first|_started|_done|_known|scene\d*|fucked|flag)$/i;
const FLAG_PREFIXES = /^(seen|met|did|has|is_|got_|day\d+_)/i;
// Flat NPC-stat detector: matches `<npc><stat>` where <stat> is the last word.
// E.g. `angelalove` → npc=angela, stat=love. `jasonfriendship` → npc=jason, stat=friendship.
const NPC_STAT_FLAT_RE = /^([a-z][a-z]{2,20}?)(love|lust|trust|respect|friendship|affection|submission|dominance|obedience|corruption)$/i;
// Items: short non-NPC counters like `flower`, `chocolate`, `teddybear`, `bluepill`.
// We catalog a small bank by name and also treat any numeric var starting at 0 with no growth yet
// as an item candidate (reviewed by human).
const ITEM_NAMES = /^(flower|flowers|chocolate|teddybear|necklace|ring|diamond|dildo|gel|weed|(blue|pink|yellow|green|red)pill|pill|gift|wine|beer|cigarette|condom|key|map|book|letter|photo|camera|cash|receipt|ticket)s?$/i;

class Detector {
  constructor() {
    this.varCatalog = new Map();     // name → { type, samples: Set, minVal, maxVal, category, co_occurs: Set, deltas: [] }
    this.passagesSeen = new Map();   // passage → { firstSeenAt, count, sampleVars: [], classification }
    this.priceObservations = [];     // from choice-text regex matches
    this.npcs = new Map();           // npc name → { stats: Set, firstSeenAt }
    this.items = new Map();          // item name → { usage_count, found_in_vars: Set }
    this.choiceTypes = new Map();    // classification → count
    this.bodyChanges = [];           // { var, before, after, at_state_hash }
    this.economy = { incomeEvents: [], expenseEvents: [] };
    this.startTs = Date.now();
  }

  /** Observe a new state snapshot (with optional diff from prior). */
  observeState({ state_hash, passage, variables, diff, timestamp }) {
    // Catalog the passage
    if (!this.passagesSeen.has(passage)) {
      this.passagesSeen.set(passage, { firstSeenAt: timestamp, count: 1, sampleVars: Object.keys(variables || {}).slice(0, 20) });
    } else {
      this.passagesSeen.get(passage).count++;
    }
    // Catalog variables (flat namespace)
    this._catalogVars(variables, timestamp);
    // Process diff
    if (diff) this._processDiff(diff, { state_hash, passage });
  }

  /** Observe a classified choice set + the text of the picked option. */
  observeChoice({ passage, classification, options, picked, prices, at_state_hash }) {
    this.choiceTypes.set(classification, (this.choiceTypes.get(classification) || 0) + 1);
    // Log price observations
    if (classification === 'payment' && prices) {
      for (let i = 0; i < prices.length; i++) {
        if (prices[i] != null) this.priceObservations.push({ at: passage, price: prices[i], label: options[i], state: at_state_hash });
      }
    }
    // Heuristic: NPC mention extraction from option text
    for (const opt of options || []) {
      const m = opt.match(/\b(?:with|to|at)\s+([A-Z][a-z]+)(?:'s)?/);
      if (m) this._notePossibleNpc(m[1]);
    }
  }

  _notePossibleNpc(name) {
    if (!name || name.length < 2) return;
    if (/^(MC|Smith|Home|Back|Menu|Cancel|You|Her|Him|Day|Night|Money|Stats|Player|Save|Load)$/i.test(name)) return;
    if (!this.npcs.has(name)) this.npcs.set(name, { stats: new Set(), firstSeenAt: Date.now() - this.startTs });
  }

  _catalogVars(vars, ts, prefix = '') {
    if (!vars || typeof vars !== 'object') return;
    for (const [k, v] of Object.entries(vars)) {
      const name = prefix ? `${prefix}.${k}` : k;
      if (name.length > 80) continue;
      if (!this.varCatalog.has(name)) {
        this.varCatalog.set(name, {
          type: typeof v, samples: new Set(), minVal: null, maxVal: null,
          category: this._classifyVarName(name, v), firstSeenAt: ts, lastSeenAt: ts,
        });
      }
      const entry = this.varCatalog.get(name);
      entry.lastSeenAt = ts;
      if (typeof v === 'number') {
        if (entry.minVal === null || v < entry.minVal) entry.minVal = v;
        if (entry.maxVal === null || v > entry.maxVal) entry.maxVal = v;
      } else if (typeof v === 'string' && entry.samples.size < 20) {
        entry.samples.add(v.slice(0, 60));
      } else if (typeof v === 'boolean') {
        entry.samples.add(String(v));
      }
      // Recurse into nested objects for per-NPC structures (e.g. $npcs.angela.love)
      if (v && typeof v === 'object' && !Array.isArray(v) && name.split('.').length < 4) {
        this._catalogVars(v, ts, name);
      }
    }
  }

  _classifyVarName(name, value) {
    const lower = name.toLowerCase();
    const basename = lower.split('.').pop();  // for nested paths, classify on leaf

    // Flat-namespace NPC stat: e.g. `angelalove`, `jasonfriendship`
    const npcFlat = basename.match(NPC_STAT_FLAT_RE);
    if (npcFlat) {
      this._notePossibleNpc(capitalize(npcFlat[1]));
      // Also note the stat on the NPC entry
      const npcName = capitalize(npcFlat[1]);
      if (this.npcs.has(npcName)) this.npcs.get(npcName).stats.add(npcFlat[2].toLowerCase());
      return 'npc_stat';
    }

    // Nested: npcs.angela.love or characters.angela.love
    const nestedNpc = lower.match(/^(?:\$?(?:npcs|relations|girls|characters)\.)?([a-z][a-z_0-9]{1,20})\.(love|lust|trust|respect|friendship|affection|corruption)$/);
    if (nestedNpc) {
      const n = capitalize(nestedNpc[1]);
      this._notePossibleNpc(n);
      if (this.npcs.has(n)) this.npcs.get(n).stats.add(nestedNpc[2]);
      return 'npc_stat';
    }

    // Body / appearance
    if (BODY_VARS.test(basename)) return 'body';

    // Player stats (restricted bank)
    if (PLAYER_STAT_VARS.test(basename)) return 'player_stat';

    // Time
    if (TIME_VARS.test(basename)) return 'time';

    // Items (known bank)
    if (ITEM_NAMES.test(basename)) return 'item';

    // Flags
    if (FLAG_SUFFIXES.test(basename) || FLAG_PREFIXES.test(basename) || typeof value === 'boolean') return 'flag';

    if (Array.isArray(value)) return 'list';
    if (typeof value === 'object' && value !== null) return 'structure';
    if (typeof value === 'number') return 'scalar';
    return 'misc';
  }

  _processDiff(diff, { state_hash, passage }) {
    // Body changes worth tracking in a separate stream
    for (const [key, change] of Object.entries(diff.changed || {})) {
      if (BODY_VARS.test(key.toLowerCase())) {
        this.bodyChanges.push({ var: key, before: change.before, after: change.after, at_passage: passage, at_state_hash: state_hash });
      }
      // Economy: big money delta
      if (/\b(money|cash|gold|balance)\b/i.test(key)) {
        const d = Number(change.after) - Number(change.before);
        if (!isNaN(d)) {
          if (d > 0) this.economy.incomeEvents.push({ passage, delta: d });
          else if (d < 0) this.economy.expenseEvents.push({ passage, delta: d });
        }
      }
      // NPC mention: if var path starts with npcs.<name>
      const npcPath = key.match(/^(?:\$?(?:npcs|relations|girls|characters)\.)?([A-Za-z_][A-Za-z_0-9]*)\./);
      if (npcPath && NPC_STAT_SUFFIXES.test(key)) {
        const n = npcPath[1];
        if (!this.npcs.has(n)) this.npcs.set(n, { stats: new Set(), firstSeenAt: Date.now() - this.startTs });
        const stat = key.split('.').pop();
        this.npcs.get(n).stats.add(stat);
      }
    }
  }

  /** Snapshot everything as JSON-friendly object for reporting. */
  serialize() {
    const vars = {};
    for (const [name, entry] of this.varCatalog.entries()) {
      vars[name] = {
        type: entry.type, category: entry.category,
        min: entry.minVal, max: entry.maxVal,
        samples: Array.from(entry.samples).slice(0, 20),
        firstSeenAt: entry.firstSeenAt, lastSeenAt: entry.lastSeenAt,
      };
    }
    const passages = {};
    for (const [p, entry] of this.passagesSeen.entries()) passages[p] = entry;
    const npcs = {};
    for (const [n, entry] of this.npcs.entries()) npcs[n] = { stats: Array.from(entry.stats), firstSeenAt: entry.firstSeenAt };
    const choiceTypes = {};
    for (const [k, v] of this.choiceTypes.entries()) choiceTypes[k] = v;
    return {
      variables: vars,
      passages,
      npcs,
      choice_type_counts: choiceTypes,
      body_changes: this.bodyChanges,
      price_observations: this.priceObservations,
      economy: this.economy,
    };
  }
}

module.exports = { Detector };
