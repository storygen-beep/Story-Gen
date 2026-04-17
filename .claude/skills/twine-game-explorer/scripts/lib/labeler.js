// Labeler — applies semantic categories to a raw statistical profile.
//
// This is the ONE place regex-based guessing lives. Every label comes with
// a confidence rating so readers know what's evidence vs inference.
//
// Phases 3+4 split the work:
//   - Detector (Phase 3): records evidence, no labels
//   - Labeler  (Phase 4): reads evidence, produces labels — this file
//
// Extension point: replace this file (or add a sibling `labeler_llm.js`) with
// a model-based labeler that reads the same profile and produces richer
// semantic groupings. The rest of the pipeline doesn't care which labeler runs.

'use strict';

// Category regexes — the only place in the skill where semantic guessing
// happens. Tune here, once, with centralized impact.

const RULES = {
  // Body / appearance — matches as substring in the basename.
  body: /(breast|bust|boob|cup|hair|body|weight|height|skin|tan|belly|pregnancy|pregnan|piercing|tattoo|scar|outfit|clothing|makeup|nails)/i,

  // NPC-stat suffix: <prefix><stat> where stat ∈ [love, lust, trust, ...]
  // Prefix is the NPC name candidate. `addiction` and friends are common in
  // adult-game Twines that track per-NPC escalation meters — missing them
  // drops whole NPC rosters into the scalar fallback.
  npcStatSuffix: /^([a-z][a-z]{1,20}?)(love|lust|trust|respect|friendship|affection|submission|dominance|obedience|corruption|fear|jealousy|arousal|addiction|infatuation|devotion|attraction|bond|intimacy)$/i,

  // Player-level scalar stats (exact basename match).
  playerStat: /^(money|cash|gold|energy|stamina|sleep|hunger|fatigue|willpower|composure|charisma|intelligence|strength|dexterity|fitness|beauty|reputation|fame|skill|corruption)$/i,

  // Time / calendar basenames.
  time: /^(day|hour|week|month|year|turn|time|calendar|morning|evening|night|afternoon|weekday)$/i,

  // Flag suffixes — story milestone indicators.
  flagSuffix: /(_unlocked|_complete|_seen|_met|_first|_started|_done|_known|scene\d*|fucked|flag)$/i,
  flagPrefix: /^(seen|met|did|has|is_|got_|day\d+_)/i,

  // Item names.
  item: /^(flower|flowers|chocolate|teddybear|necklace|ring|diamond|dildo|gel|weed|(blue|pink|yellow|green|red)pill|pill|gift|wine|beer|cigarette|condom|key|map|book|letter|photo|camera|receipt|ticket)s?$/i,

  // Item-ownership prefix: `has<noun>` boolean flags are a strong
  // item-possession signal in adult-game conventions (hasdildo, haslube,
  // hasoutfit, hascoffee, hasplug). Inner noun is captured as item_name.
  itemOwnershipPrefix: /^has([a-z][a-z_0-9]{2,})$/i,
};

/**
 * Assign one or more labels to a variable based on its name and profile.
 * Returns { primary, tags, confidence, extras } where:
 *   - primary: the single best guess (for bucketing)
 *   - tags: additional labels that also apply
 *   - confidence: low / medium / high
 *   - extras: label-specific info (e.g. {npc, stat} for npc_stat)
 */
function labelVariable(name, profile) {
  const basename = name.split('.').pop().toLowerCase();
  const fullLower = name.toLowerCase();
  const tags = new Set();
  let primary = null;
  let extras = {};
  let confidence = 'low';

  // Boolean-like → flag
  if (profile.bool_values && profile.bool_values.length) {
    tags.add('flag');
    primary = primary || 'flag';
    confidence = 'high';
  }

  // Structural flag-name patterns
  if (RULES.flagSuffix.test(basename) || RULES.flagPrefix.test(basename)) {
    tags.add('flag');
    primary = primary || 'flag';
    confidence = confidence === 'high' ? 'high' : 'medium';
  }

  // NPC-stat flat pattern: angelalove → npc=angela, stat=love
  const npcFlat = basename.match(RULES.npcStatSuffix);
  if (npcFlat) {
    const npc = npcFlat[1];
    const stat = npcFlat[2].toLowerCase();
    extras = { npc, stat };
    primary = 'npc_stat';
    tags.add('npc_stat');
    confidence = 'high';
  }

  // NPC-stat nested pattern: npcs.angela.love
  const nestedNpc = fullLower.match(/^(?:\$?(?:npcs|relations|girls|characters)\.)?([a-z][a-z_0-9]{1,20})\.(love|lust|trust|respect|friendship|affection|corruption)$/);
  if (nestedNpc) {
    extras = { npc: nestedNpc[1], stat: nestedNpc[2] };
    primary = 'npc_stat';
    tags.add('npc_stat');
    confidence = 'high';
  }

  if (RULES.body.test(basename)) {
    tags.add('body');
    primary = primary || 'body';
    confidence = confidence === 'low' ? 'medium' : confidence;
  }

  if (RULES.playerStat.test(basename)) {
    tags.add('player_stat');
    primary = primary || 'player_stat';
    confidence = 'high';
  }

  if (RULES.time.test(basename)) {
    tags.add('time');
    primary = primary || 'time';
    confidence = 'high';
  }

  if (RULES.item.test(basename)) {
    tags.add('item');
    primary = primary || 'item';
    confidence = 'medium';
  }

  // `has<noun>` boolean flag → item ownership indicator. Promotes over the
  // `flag` structural label because it carries semantic role (it IS still
  // a flag; `item` is the more useful bucket for a reader). We require
  // boolean type so counters like `hashistory` or `hasword` don't slip in.
  const itemOwn = basename.match(RULES.itemOwnershipPrefix);
  if (itemOwn && profile.bool_values && profile.bool_values.length) {
    tags.add('item');
    if (!primary || primary === 'flag') primary = 'item';
    extras.item_name = itemOwn[1];
    if (confidence === 'low') confidence = 'medium';
  }

  // Structural fallbacks using profile shape
  if (!primary) {
    if (profile.types && profile.types.includes('number')) primary = 'scalar';
    else if (profile.types && profile.types.includes('string')) primary = 'string';
    else primary = 'misc';
    confidence = 'low';
  }

  return { primary, tags: Array.from(tags), confidence, extras };
}

/**
 * Produce a labeled view of the whole profile.
 * This is the shape report.js consumes.
 */
function labelProfile(profile) {
  const variables = {};
  const byCategory = {};
  const npcs = {};
  const bodyChanges = [];
  const items = [];
  const time = [];
  const playerStats = [];
  const flags = [];

  for (const [name, prof] of Object.entries(profile.variables || {})) {
    const label = labelVariable(name, prof);
    variables[name] = { profile: prof, label };

    const cat = label.primary;
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(name);

    if (cat === 'npc_stat' && label.extras.npc) {
      const npc = label.extras.npc;
      if (!npcs[npc]) npcs[npc] = { stats: new Set(), vars: [] };
      npcs[npc].stats.add(label.extras.stat);
      npcs[npc].vars.push({ name, stat: label.extras.stat, profile: prof });
    }
    if (cat === 'body') bodyChanges.push({ name, profile: prof });
    if (cat === 'item') items.push({
      name,
      item_name: label.extras.item_name || name,
      profile: prof,
    });
    if (cat === 'time') time.push({ name, profile: prof });
    if (cat === 'player_stat') playerStats.push({ name, profile: prof });
    if (label.tags.includes('flag')) flags.push({ name, profile: prof });
  }

  // Serialise NPC sets
  const npcsOut = {};
  for (const [n, d] of Object.entries(npcs)) {
    npcsOut[n] = { stats: Array.from(d.stats), vars: d.vars };
  }

  // Slice mutation log by category (body changes, economy events)
  const bodyMutations = (profile.mutations || []).filter((m) => {
    const v = variables[m.var];
    return v && v.label.primary === 'body';
  });
  const moneyMutations = (profile.mutations || []).filter((m) => {
    const v = variables[m.var];
    return v && (v.label.primary === 'player_stat') && /money|cash|gold|balance/i.test(m.var);
  });
  const economy = {
    income_events: moneyMutations.filter((m) => Number(m.after) > Number(m.before)),
    expense_events: moneyMutations.filter((m) => Number(m.after) < Number(m.before)),
  };

  return {
    variables,
    by_category: byCategory,
    npcs: npcsOut,
    body: { vars: bodyChanges, mutations: bodyMutations },
    items,
    time,
    player_stats: playerStats,
    flags,
    economy,
  };
}

module.exports = { labelProfile, labelVariable, RULES };
