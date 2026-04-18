// Static passage-link graph.
//
// Walks the raw passage source captured in `passage_catalog.json` and emits
// every navigation edge the game *could* traverse — regardless of whether
// Claude ever clicked it during live play. This is the complement to the
// dynamic observations in choice_graph.js: together they tell you coverage
// (how much of the possible graph we actually explored).
//
// Edge kinds we recognize:
//   - wiki     : `[[Display|Target]]`, `[[Target]]`, `[[Display->Target]]`,
//                `[[Target<-Display]]`. Setter suffix `[[A|B][$x += 1]]` is
//                stripped and the setter source is recorded alongside.
//   - link     : `<<link "Display" "Target">>` macro with explicit target arg.
//                The common wrapper form `<<link "Display">>...<</link>>` is
//                NOT an edge — it fires an in-passage `<<replace>>`. Any wiki
//                link inside the body is emitted independently as a wiki edge.
//   - goto     : `<<goto "Target">>` or `<<goto [[Target]]>>`
//   - return   : `<<return "Target">>` forced-target variant
//   - include  : `<<include "Target">>` / `<<display "Target">>` —
//                transclusion, not navigation, recorded so static analysis
//                can spot widget/fragment reuse.
//
// Gate inference: we maintain a stack of open `<<if>>` / `<<elseif>>` /
// `<<else>>` branches (closed by `<</if>>` or `<<endif>>` — both forms are
// in the wild). Every emitted edge carries a `gate` array (outermost to
// innermost). Empty gate = unconditionally reachable from the passage.
//
// Passages tagged `script`, `stylesheet`, or `Twine.private` are skipped —
// they aren't narrative content.

'use strict';

const SKIP_TAGS = new Set(['script', 'stylesheet', 'Twine.private']);

// Token regex. Order matters: wiki links first so nothing else can claim them.
// We allow single `]` chars inside wiki-link content (to support setters like
// `[[A|B][$x += 1]]`) via a negative-lookahead tempered alternation.
const TOKEN_RE = /\[\[((?:[^\]]|\](?!\]))+)\]\]|<<(\/?)(\w+)(?:\s+([\s\S]*?))?>>/g;

// Parse the inside of a wiki link. Handles three separators and a setter suffix.
//   `Display|Target`           -> { display: 'Display', target: 'Target' }
//   `Display->Target`          -> { display: 'Display', target: 'Target' }
//   `Target<-Display`          -> { display: 'Display', target: 'Target' }
//   `Target`                   -> { display: 'Target',  target: 'Target' }
//   `Display|Target][$x += 1`  -> { display, target, setter: '$x += 1' }
function parseWikiContent(raw) {
  let setter = null;
  // Setter suffix is everything after the first `]` that isn't followed by
  // another `]`. Split at the first bare `]`.
  const setterIdx = raw.search(/\](?!\])/);
  let body = raw;
  if (setterIdx !== -1) {
    body = raw.slice(0, setterIdx);
    const rest = raw.slice(setterIdx + 1).trim();
    // Drop a leading `[` if present (setter blocks look like `[$x += 1]`, but
    // the outer `]` already consumed one of the pair — we keep the content).
    setter = rest.replace(/^\[/, '').replace(/\]$/, '').trim() || null;
  }
  body = body.trim();

  let display = null;
  let target = null;
  if (body.includes('->')) {
    const [d, t] = body.split('->');
    display = d.trim();
    target = t.trim();
  } else if (body.includes('<-')) {
    const [t, d] = body.split('<-');
    display = d.trim();
    target = t.trim();
  } else if (body.includes('|')) {
    const [d, t] = body.split('|');
    display = d.trim();
    target = t.trim();
  } else {
    display = body;
    target = body;
  }
  return { display, target, setter };
}

// Parse the argument list of a <<link "..." "..." >> macro.
// Returns { display, target } — target may be null for the wrapper form.
function parseLinkArgs(body) {
  if (!body) return { display: null, target: null };
  body = body.trim();

  // Two double-quoted strings: "Display" "Target"
  const twoQuoted = body.match(/^"((?:[^"\\]|\\.)*)"\s+"((?:[^"\\]|\\.)*)"/);
  if (twoQuoted) return { display: twoQuoted[1], target: twoQuoted[2] };

  // Wiki-linked form: [[Target]] or [[Display|Target]] (SugarCube accepts this)
  const wiki = body.match(/^\[\[((?:[^\]]|\](?!\]))+)\]\]/);
  if (wiki) return parseWikiContent(wiki[1]);

  // Single quoted display only — wrapper form, target comes from body later
  const oneQuoted = body.match(/^"((?:[^"\\]|\\.)*)"/);
  if (oneQuoted) return { display: oneQuoted[1], target: null };

  return { display: null, target: null };
}

// Parse the argument list of a <<button ...>> macro. Two forms:
//   <<button 'Display' 'Target'>>       — direct navigation; emit edge here.
//   <<button 'Display'>>...<</button>>   — wrapper; body may contain
//       <<goto 'Target'>> (optionally under <<if>>s). Goto edges emitted
//       with display=label so click text matches the DOM.
// Accepts both single- and double-quoted strings for each arg.
function parseButtonArgs(body) {
  if (!body) return { display: null, target: null };
  body = body.trim();
  const quoteRe = /^(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')/;
  const first = body.match(quoteRe);
  if (!first) return { display: null, target: null };
  const display = first[1] != null ? first[1] : first[2];
  const rest = body.slice(first[0].length).trim();
  if (!rest) return { display, target: null };
  const second = rest.match(quoteRe);
  if (!second) return { display, target: null };
  const target = second[1] != null ? second[1] : second[2];
  return { display, target };
}

// Tokenize the args of <<case VAL1 VAL2 ...>>. Whitespace-separated at the
// top level, respecting quoted strings (so `<<case "a b" 2>>` → ['"a b"','2']).
// Values are preserved as-is (with quotes if present) so the synthesized
// gate condition `<switchExpr> is "a b"` is well-formed SugarCube.
function parseCaseValues(args) {
  const out = [];
  let buf = '';
  let inStr = null;
  for (let i = 0; i < args.length; i++) {
    const ch = args[i];
    const prev = i > 0 ? args[i - 1] : '';
    if (inStr) {
      buf += ch;
      if (ch === inStr && prev !== '\\') inStr = null;
      continue;
    }
    if (ch === '"' || ch === "'") { inStr = ch; buf += ch; continue; }
    if (/\s/.test(ch)) {
      if (buf.trim()) out.push(buf.trim());
      buf = '';
      continue;
    }
    buf += ch;
  }
  if (buf.trim()) out.push(buf.trim());
  return out;
}

// Parse the argument of <<goto>>, <<return>>, <<include>>, <<display>>.
// Accepts either a quoted passage name or a wiki-link form.
function parseTargetArg(body) {
  if (!body) return null;
  body = body.trim();
  const q = body.match(/^"((?:[^"\\]|\\.)*)"/);
  if (q) return q[1];
  const sq = body.match(/^'((?:[^'\\]|\\.)*)'/);
  if (sq) return sq[1];
  const w = body.match(/^\[\[((?:[^\]]|\](?!\]))+)\]\]/);
  if (w) return parseWikiContent(w[1]).target;
  // Bareword target (uncommon): accept only if it looks like a plain identifier
  // to avoid matching expressions like `$var + 1`.
  if (/^[A-Za-z][A-Za-z0-9_ \-]*$/.test(body)) return body.trim();
  return null; // dynamic expression — record as unresolved
}

/**
 * Parse one passage's source. Returns { edges, unresolved_count }.
 */
function parsePassage(passageName, source) {
  const edges = [];
  let unresolved = 0;
  // Gate stack: each entry is an array of conditions representing the current
  // if/elseif/else chain. We push on <<if>>, mutate top on <<elseif>>/<<else>>,
  // and pop on <</if>> / <<endif>>. <<switch>>/<<case>> also push/replace
  // gate frames so edges inside each case carry the right condition.
  const gateStack = [];
  const snapshotGate = () => gateStack.map((g) => ({ condition: g.condition, branch: g.branch }));

  // Switch tracker: one entry per open <<switch>>. Tracks the switch
  // expression, the values of cases seen so far (so <<default>> can emit
  // a proper negation), and whether we're currently inside a case block
  // (so we know whether a <<case>>/<<default>>/<</switch>> must pop a
  // previously-pushed gate frame before pushing a new one).
  const switchStack = [];
  const exitCurrentCase = () => {
    const top = switchStack[switchStack.length - 1];
    if (top && top.in_case) {
      gateStack.pop();
      top.in_case = false;
    }
  };

  // Button/link wrapper tracker: when a <<button 'Label'>> or
  // <<link 'Label'>> opens without an explicit target, push its label so
  // any <<goto 'X'>> fired from the body carries display=label. Pop on
  // the matching close tag. Entries are { kind: 'button'|'link', label }.
  const wrapperStack = [];
  const currentWrapperLabel = () => {
    for (let i = wrapperStack.length - 1; i >= 0; i--) {
      if (wrapperStack[i].label) return wrapperStack[i].label;
    }
    return null;
  };

  let m;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(source)) !== null) {
    if (m[1] !== undefined) {
      // Wiki link: m[1] is the content inside [[...]]
      const parsed = parseWikiContent(m[1]);
      if (parsed.target && !looksDynamic(parsed.target)) {
        edges.push({
          from: passageName,
          to: parsed.target,
          display: parsed.display,
          setter: parsed.setter,
          kind: 'wiki',
          gate: snapshotGate(),
          index: m.index,
        });
      } else if (parsed.target) {
        unresolved++;
      }
      continue;
    }
    const isClose = m[2] === '/';
    const macro = (m[3] || '').toLowerCase();
    const args = m[4] || '';

    // Gate control flow
    if (!isClose && macro === 'if') {
      gateStack.push({ condition: args.trim(), branch: 'if' });
      continue;
    }
    if (!isClose && (macro === 'elseif' || macro === 'else')) {
      if (gateStack.length) {
        gateStack[gateStack.length - 1] = {
          condition: macro === 'else' ? `!(${gateStack[gateStack.length - 1].condition})` : args.trim(),
          branch: macro,
        };
      }
      continue;
    }
    if ((isClose && macro === 'if') || (!isClose && macro === 'endif')) {
      gateStack.pop();
      continue;
    }

    // Switch/case control flow. Every <<case ...>> synthesizes a gate
    // frame `<switchExpr> is <value>` (or `(... or ...)` for multi-value
    // cases). <<default>> synthesizes the negation of all prior cases.
    // This lets downstream gate-eval correctly recognize that edges
    // inside different cases are mutually exclusive — previously they
    // emitted with empty gates and looked unconditionally reachable,
    // which is why navigate's gate check was wrongly approving clicks
    // on switch-branch content that wasn't actually rendered.
    if (!isClose && macro === 'switch') {
      switchStack.push({ expr: args.trim(), cases_seen: [], in_case: false });
      continue;
    }
    if (!isClose && macro === 'case') {
      const top = switchStack[switchStack.length - 1];
      if (!top) continue;
      exitCurrentCase();
      const values = parseCaseValues(args);
      if (!values.length) continue;
      top.cases_seen.push(...values);
      const cond = values.length === 1
        ? `${top.expr} is ${values[0]}`
        : '(' + values.map((v) => `${top.expr} is ${v}`).join(' or ') + ')';
      gateStack.push({ condition: cond, branch: 'case' });
      top.in_case = true;
      continue;
    }
    if (!isClose && macro === 'default') {
      const top = switchStack[switchStack.length - 1];
      if (!top) continue;
      exitCurrentCase();
      const priorDisjunction = top.cases_seen
        .map((v) => `${top.expr} is ${v}`)
        .join(' or ');
      const cond = priorDisjunction ? `!(${priorDisjunction})` : 'true';
      gateStack.push({ condition: cond, branch: 'default' });
      top.in_case = true;
      continue;
    }
    if ((isClose && macro === 'switch') || (!isClose && macro === 'endswitch')) {
      exitCurrentCase();
      switchStack.pop();
      continue;
    }

    // Navigation macros
    if (!isClose && macro === 'goto') {
      const t = parseTargetArg(args);
      if (t) {
        // If we're inside a <<button>>/<<link>> wrapper, the real click
        // target is the wrapper — the goto inside its body fires only
        // after the user clicks the wrapper's label. Inherit the label
        // as display AND adopt the wrapper's kind so downstream
        // consumers (navigate's wiki-only filter, harness classifier)
        // treat it as a clickable edge rather than an automatic goto.
        const wrapperTop = wrapperStack[wrapperStack.length - 1];
        const display = wrapperTop ? wrapperTop.label : null;
        const kind = wrapperTop ? wrapperTop.kind : 'goto';
        edges.push({ from: passageName, to: t, display, setter: null, kind, gate: snapshotGate(), index: m.index });
      } else if (args.trim()) unresolved++;
      continue;
    }
    if (!isClose && macro === 'return' && args.trim()) {
      const t = parseTargetArg(args);
      if (t) edges.push({ from: passageName, to: t, display: null, setter: null, kind: 'return', gate: snapshotGate(), index: m.index });
      else unresolved++;
      continue;
    }
    if (!isClose && (macro === 'include' || macro === 'display')) {
      const t = parseTargetArg(args);
      if (t) edges.push({ from: passageName, to: t, display: null, setter: null, kind: 'include', gate: snapshotGate(), index: m.index });
      else if (args.trim()) unresolved++;
      continue;
    }
    if (!isClose && macro === 'link') {
      const { display, target } = parseLinkArgs(args);
      if (target && !looksDynamic(target)) {
        edges.push({ from: passageName, to: target, display, setter: null, kind: 'link', gate: snapshotGate(), index: m.index });
      } else {
        // Wrapper form — push label so embedded <<goto>> / wiki links
        // carry it as display text. (Wiki links already self-describe,
        // so the label primarily benefits <<goto>>-based navigation.)
        wrapperStack.push({ kind: 'link', label: display || null });
      }
      continue;
    }
    if (isClose && macro === 'link') {
      // Pop only if the last frame is a link wrapper — explicit-target
      // <<link>> didn't push anything.
      const top = wrapperStack[wrapperStack.length - 1];
      if (top && top.kind === 'link') wrapperStack.pop();
      continue;
    }
    if (!isClose && macro === 'button') {
      // Same two-form handling as <<link>>.
      const { display, target } = parseButtonArgs(args);
      if (target && !looksDynamic(target)) {
        // Direct navigation form: <<button 'Label' 'Target'>>. Emit an
        // edge immediately with kind='button' so the navigator knows it
        // came from a widget click (same click semantics as wiki, but
        // tagged distinctly so consumers can reason about edge-kind
        // coverage). No body to scan either way — a two-arg button
        // is typically self-closing in practice.
        edges.push({
          from: passageName, to: target, display, setter: null,
          kind: 'button', gate: snapshotGate(), index: m.index,
        });
      }
      // Always push, even for the two-arg form, so <</button>> pops a
      // matching frame regardless of body/no-body usage. If there's a
      // body with additional <<goto>>s, they'll be picked up with the
      // same label via currentWrapperLabel() below.
      wrapperStack.push({ kind: 'button', label: display || null });
      continue;
    }
    if (isClose && macro === 'button') {
      const top = wrapperStack[wrapperStack.length - 1];
      if (top && top.kind === 'button') wrapperStack.pop();
      continue;
    }
    // Unrecognized macro / close-tag: ignored.
  }
  return { edges, unresolved };
}

// Heuristic — target contains an expression rather than a static passage name.
function looksDynamic(t) {
  if (!t) return false;
  return /[`$]/.test(t) || /\s[+\-*/]\s/.test(t);
}

/**
 * Build the full static graph from a parsed passage_catalog.json payload.
 * Input shape: { passages: [{ name, tags, source_raw }, ...], engine, ... }
 * Returns a JSON-serializable graph object.
 */
function buildStaticGraph(catalog) {
  if (!catalog || !Array.isArray(catalog.passages)) {
    return {
      generated_at: new Date().toISOString(),
      error: 'no passage catalog supplied',
      total_passages: 0,
      total_edges: 0,
      edges: [],
    };
  }

  const passageNames = new Set(catalog.passages.map((p) => p.name));
  const edges = [];
  const byFrom = {};
  const byTo = {};
  const perPassageStats = {};
  const unresolvedTargets = new Set();
  let skipped = 0;
  let parseErrors = 0;

  for (const p of catalog.passages) {
    const tags = p.tags || [];
    if (tags.some((t) => SKIP_TAGS.has(t))) { skipped++; continue; }
    try {
      const { edges: pEdges, unresolved } = parsePassage(p.name, p.source_raw || '');
      perPassageStats[p.name] = { edge_count: pEdges.length, unresolved, tags };
      for (const e of pEdges) {
        edges.push(e);
        if (!byFrom[e.from]) byFrom[e.from] = [];
        byFrom[e.from].push(edges.length - 1);
        if (!byTo[e.to]) byTo[e.to] = [];
        byTo[e.to].push(edges.length - 1);
        if (!passageNames.has(e.to)) unresolvedTargets.add(e.to);
      }
    } catch (err) {
      parseErrors++;
    }
  }

  // Edge-kind histogram
  const byKind = {};
  for (const e of edges) byKind[e.kind] = (byKind[e.kind] || 0) + 1;

  // Passages that have no outgoing nav (dead ends)
  const deadEnds = [];
  for (const p of catalog.passages) {
    if (tags_skip(p.tags)) continue;
    if (!byFrom[p.name] || byFrom[p.name].length === 0) deadEnds.push(p.name);
  }

  // Passages that are never targeted (unreachable from any other passage — good
  // candidates for start passages or dead code).
  const untargeted = [];
  for (const p of catalog.passages) {
    if (tags_skip(p.tags)) continue;
    if (!byTo[p.name]) untargeted.push(p.name);
  }

  return {
    generated_at: new Date().toISOString(),
    total_passages: catalog.passages.length,
    skipped_passages: skipped,
    parse_errors: parseErrors,
    total_edges: edges.length,
    edges_by_kind: byKind,
    edges,
    unresolved_targets: Array.from(unresolvedTargets).sort(),
    dead_end_passages: deadEnds.slice(0, 200),
    untargeted_passages: untargeted.slice(0, 200),
    per_passage_stats: perPassageStats,
  };
}

function tags_skip(tags) {
  return (tags || []).some((t) => SKIP_TAGS.has(t));
}

module.exports = { buildStaticGraph, parsePassage, parseWikiContent, parseLinkArgs, parseButtonArgs, parseCaseValues, parseTargetArg };
