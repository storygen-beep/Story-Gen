#!/usr/bin/env python3
"""Re-anchor the skill's `file:line` citations against live source.

WHY THIS EXISTS
---------------
`SKILL.md` operating rules: *"Every engine claim carries a `file:line`. If
`references/engine.md` doesn't have it, go read the code."* That rule is this skill's
main defence against asserting things about an engine nobody re-read — LO's first
standing rule. A citation that points at the wrong line defeats it in the worst way:
it sends the reader confidently to code that says something else.

Measured 2026-08-29, at HEAD, before the change that prompted the check: of the
citations written in the self-verifying form `v2.py:NNNN   <the code>` — which carry
their own expected content — **0 of 25 matched**. `engine.md` §20 placed the
`npc_at_location` branch at `v2.py:4131-4145`; it was at 4216, 85 lines out. The engine
has grown by thousands of lines since most citations were written and nothing
re-anchored them.

A blanket offset cannot fix this. Drift differs per citation, because insertions happened
at many points over many months. So this tool re-anchors each citation individually, by
searching the target file for what the citation's own context says should be there.

HOW A CITATION IS ANCHORED
--------------------------
Three strengths, and the tool only ever proposes a move for the first two:

  strong   the citation is written `v2.py:NNNN   <code>` — the code is the anchor, and
           the match must be exact.
  named    a backticked code identifier sits within a short window of the citation, e.g.
           "`window.advanceTime(minutes)` (`v2.py:5400`)". The identifier is the anchor.
  none     nothing nearby looks like code. Reported as UNVERIFIABLE and never touched —
           a human has to read the sentence.

  ⚠️ An anchor that matches in many scattered places is reported AMBIGUOUS, not guessed.

USAGE
-----
    python3 .claude/skills/author-game-v2/scripts/cite_check.py            # report
    python3 .claude/skills/author-game-v2/scripts/cite_check.py --fix      # rewrite
    python3 .claude/skills/author-game-v2/scripts/cite_check.py --strict   # exit 1 on drift

`--fix` rewrites ONLY citations whose anchor resolves to exactly one place. It never
touches AMBIGUOUS or UNVERIFIABLE ones, and it never invents an anchor.

⚠️ **RUN `--fix` BEFORE HAND-VERIFYING, NEVER AFTER.** It re-anchors on its own
heuristic and will happily overwrite a better line a human chose. Measured 2026-08-29,
on the pass that hand-fixed 21 citations: a following `--fix` moved the quest-effect row
off `setup.applyQuestEffect` onto `var qid = String(it.quest_id …)` in the goal
evaluator, moved an `is_true` citation off the operator test onto the DOCSTRING three
lines above it, and collapsed two pairs — the rent greeting onto the money print, and
the `rejection_passage` branch onto its own body. The pair guard below only fires while
both halves still share a target, which is exactly what a hand-fix undoes. Four of ten
rewrites had to be reverted.

⚠️ LO's decision, 2026-08-29: **a bad citation does not fail a build.** This tool is not
wired into `gates.py --selfcheck` and `--strict` exists for a human running it on
purpose, not for CI. A stale line number is a documentation defect; refusing to ship a
game over one would be the checklist failure `DOCTRINE_GAPS.md` §3a already ruled against.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(SKILL, "..", "..", ".."))

# The short names citations use, and what they resolve to. Citations are written
# relative to nothing in particular — `v2.py`, `generators/v2.py` and the full path all
# appear — so the map is keyed on the basename and the longer forms fall through to it.
TARGETS = {
    "v2.py": "apps/game_generation/twee_comprehensive/generators/v2.py",
    "template_import.py": "apps/projects/services/template_import.py",
    "models.py": "apps/stories/models.py",
    "game_service.py": "apps/game_generation/services/game_service.py",
    "gates.py": ".claude/skills/author-game-v2/scripts/gates.py",
}

# `v2.py:1234` or `v2.py:1234-1250`, backticked or bare, possibly path-prefixed.
CITE = re.compile(
    r"(?P<path>(?:[\w./-]*/)?(?P<base>[\w_]+\.py)):(?P<line>\d{2,6})(?:-(?P<end>\d{2,6}))?"
)
# A backticked chunk that looks like code rather than prose.
TICKED = re.compile(r"`([^`\n]{2,80})`")
CODEISH = re.compile(r"[_.(\[]|^[a-z]+[A-Z]")

# Anchors this common are worthless — they match everywhere.
MAX_MATCHES = 6

# A doc fragment that abbreviates on purpose can never match the source.
ELIDED = re.compile(r'\u2026|\.\.\.')

# `key = true` / `key = "x"` / `key = 3` — TOML the author writes, not engine code.
TOML_ASSIGN = re.compile(r'^[\w.]+\s*=\s*(true|false|-?\d|"|\[)', re.I)


# ⚠️ Both of these were found by the tool proposing a wrong fix on its first run, and
# both would have corrupted citations that were merely stale into ones that were false.
DOCFILE = re.compile(r"\.(md|toml|json|html|txt)\b", re.I)


def looks_like_code(tok: str) -> bool:
    """Is this backticked token a code anchor, or is it prose dressed as one?

    ⚠️ `engine.md` is backticked all over these files and appears once inside a v2.py
    COMMENT, so it resolved as a unique 'anchor' and re-pointed seven unrelated
    citations at that comment. A doc filename is never an anchor.
    """
    tok = tok.strip()
    if len(tok) < 6:                       # `.hour` is not an anchor
        return False
    if " " in tok.strip() and len(tok.split()) > 6:
        return False
    if CITE.search(tok):                   # the citation itself, or another one
        return False
    if DOCFILE.search(tok):                # engine.md, board.toml — documentation
        return False
    if tok.startswith(("$", "[", "#", ".", "§")):   # TOML / state / prose marker
        # ⚠️ `[` and not just `[[`: a SECTION marker is authoring syntax too.
        # `[group]` resolved onto a v2.py comment and `[project] version` onto an
        # error-message STRING, and both were then reported as drift against
        # hand-verified citations that pointed at the actual implementation.
        return False
    if TOML_ASSIGN.match(tok):
        # `show_when_locked = true` is authoring syntax, and v2.py carries TOML
        # examples inside its docstrings. Anchoring on one sent a citation to the
        # example instead of the branch that reads the field.
        return False
    return bool(CODEISH.search(tok))


def is_comment(line: str) -> bool:
    return line.strip().startswith(("#", "//", "*"))


def is_documentation(line: str) -> bool:
    """A source line that is TALKING about the code rather than being it.

    ⚠️ Scanning for triple-quoted docstrings would be wrong here and badly so:
    `v2.py` emits its whole JavaScript engine from inside Python f-strings, so
    "inside a string literal" describes most of the engine. What separates prose
    from implementation in this codebase is narrower and more reliable — **a line
    that carries a `file.py:NNNN` citation of its own is documentation.** Comments
    here cite line numbers; code does not.

    Measured case: `v2.py:9855` reads *"the same semantics adjacent [group] blocks
    already have (v2.py:14561)"* — a comment, and itself a stale citation. It was
    proposed as the anchor for the `[group]` chain over `_render_group_chain`.
    """
    return is_comment(line) or bool(CITE.search(line))


def in_string_literal(line: str, needle: str) -> bool:
    """Does `needle` appear ONLY inside quotes on this line?

    An error message that happens to contain the words `[project] version` is not
    where `[project] version` is implemented (`template_import.py:3013`).
    """
    stripped = re.sub(r'"[^"]*"|\'[^\']*\'', "", line)
    return needle not in stripped and needle in line


def brace_norm(text: str) -> str:
    """v2.py emits its JavaScript from inside Python f-strings, so every brace in the
    generated code is DOUBLED in the source.

    ⚠️ Without this the tool matched the wrong copy: the clamp line appears at :5851
    (the real template, `{{ clampFlag = true; }}`) and again at :19953 (a plain copy),
    and an anchor written with single braces matched ONLY the second — so a citation
    that was correct-ish resolved 'uniquely' to the wrong half of the file. Normalising
    makes both match, which reports AMBIGUOUS, which is the honest answer.
    """
    return text.replace("{{", "{").replace("}}", "}")


def read(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


class Citation:
    def __init__(self, md, mdline, col, base, line, end, raw, context, inline_code):
        self.md, self.mdline, self.col = md, mdline, col
        self.base, self.line, self.end = base, line, end
        self.raw, self.context, self.inline_code = raw, context, inline_code
        self.heading = ""
        self.verdict = "UNVERIFIABLE"
        self.anchor = None
        self.strength = "none"
        self.found: list[int] = []

    @property
    def proposal(self):
        return self.found[0] if len(self.found) == 1 else None


HEADING = re.compile(r"^#{1,4}\s+(.*)$")


def collect(md_path: str) -> list[Citation]:
    out = []
    heading = ""
    for n, text in enumerate(read(md_path), 1):
        hm = HEADING.match(text)
        if hm:
            heading = hm.group(1)
        for m in CITE.finditer(text):
            base = m.group("base")
            if base not in TARGETS:
                continue
            # a self-verifying citation: two or more spaces then code, to end of line
            tail = text[m.end():]
            inline = None
            tm = re.match(r"\s{2,}(\S.*)$", tail)
            if tm and not tm.group(1).lstrip().startswith(("—", "-", "·", "(", "|")):
                inline = tm.group(1).strip()
            lo, hi = max(0, m.start() - 200), min(len(text), m.end() + 200)
            c = Citation(md_path, n, m.start(), base,
                         int(m.group("line")),
                         int(m.group("end")) if m.group("end") else None,
                         m.group(0), text[lo:hi], inline)
            # A section heading names its subject — "## 20. `npc_at_location` — ..." —
            # and is a legitimate anchor for every citation inside that section, which
            # is where two thirds of them sit with no identifier on their own line.
            c.heading = heading
            out.append(c)
    return out


def resolve(c: Citation, src: list[str]) -> None:
    """Find where the citation's anchor actually is."""
    # 1 — strong: the code is written next to the citation
    if c.inline_code:
        frag = c.inline_code.split("//")[0].split("#")[0].strip()
        frag = frag.rstrip("\\").strip()
        # The column beside a citation is not always literal code. Two forms can never
        # be matched, and calling them MISSING sends the next reader chasing citations
        # that were fine: an ELIDED fragment (`def _media_pool_key(...)`, `["Monday",…]`)
        # deliberately abbreviates, and a PROSE column ("the overlay is emitted only
        # when") is a description. Separated so the number means something.
        if ELIDED.search(frag):
            c.verdict, c.strength, c.anchor = "ELIDED", "none", frag
            return
        if not CODEISH.search(frag):
            c.verdict, c.strength, c.anchor = "PROSE", "none", frag
            return
        if len(frag) >= 8:
            c.anchor, c.strength = frag, "strong"
            nfrag = brace_norm(frag)
            c.found = [i + 1 for i, l in enumerate(src) if nfrag in brace_norm(l)]
            if not c.found and len(nfrag) >= 18:
                # These docs abbreviate on purpose — `def _resolve_pool_dir(self,
                # pool_dir)` for a signature that carries type hints in the source. A
                # prefix still identifies the line, and calling the citation MISSING
                # because the doc is readable would be the tool's error, not the doc's.
                pre = nfrag[:24]
                c.found = [i + 1 for i, l in enumerate(src) if pre in brace_norm(l)]
                if c.found:
                    c.anchor = pre + "…"
            _verdict(c)
            return

    # 2a — a definition beats a call site. An anchor written as `advanceTime(minutes)`
    # matches every place the function is CALLED, while the sentence around the citation
    # almost always describes where it is DEFINED. On this tool's first run that sent
    # three clock citations to a call inside waitTime (:5534) instead of the definition
    # (:5492). So: if the anchor names a function, look for its definition first.
    for tok in sorted({t for t in TICKED.findall(c.context) if looks_like_code(t)},
                      key=len, reverse=True):
        m = re.match(r"^(?:window\.|setup\.)?(\w+)\s*\(", tok.strip())
        if not m:
            continue
        name = m.group(1)
        forms = [f"{name} = function(", f"def {name}(", f"function {name}("]
        hits = [i + 1 for i, l in enumerate(src)
                if any(f in l for f in forms) and not is_comment(l)]
        if len(hits) == 1:
            c.anchor, c.strength, c.found = f"{name} (definition)", "named", hits
            _verdict(c)
            return

    # 2b — named: a backticked identifier near the citation
    cands = [t for t in TICKED.findall(c.context) if looks_like_code(t)]
    # then, weaker, whatever the enclosing section is named after
    cands += [t for t in TICKED.findall(getattr(c, "heading", "") or "")
              if looks_like_code(t)]
    # longest first: the most specific identifier is the best anchor
    for tok in sorted(set(cands), key=len, reverse=True):
        needle = tok.strip()
        nneedle = brace_norm(needle)
        hits = [i + 1 for i, l in enumerate(src) if nneedle in brace_norm(l)]
        # Prefer real code over a mention of it. `show_when_locked = true` occurs once
        # as TOML inside a v2.py comment (:14380), and on this tool's first run the
        # citation using it was re-pointed at that comment instead of the branch that
        # implements it. A named anchor found ONLY in comments is not evidence.
        code_hits = [h for h in hits
                     if not is_documentation(src[h - 1])
                     and not in_string_literal(src[h - 1], needle)]
        if code_hits:
            hits = code_hits
        elif hits:
            continue
        if 1 <= len(hits) <= MAX_MATCHES:
            c.anchor, c.strength, c.found = needle, "named", hits
            _verdict(c)
            return
    c.verdict = "UNVERIFIABLE"


def _verdict(c: Citation) -> None:
    if not c.found:
        c.verdict = "MISSING"          # the anchor is not in the file at all
    elif c.line in c.found or (c.end and any(c.line <= f <= c.end for f in c.found)):
        c.verdict = "OK"
    elif len(c.found) == 1:
        c.verdict = "DRIFTED"
    else:
        # several matches: if one is far closer than the rest, still ambiguous —
        # proximity to a wrong number is not evidence.
        c.verdict = "AMBIGUOUS"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fix", action="store_true",
                    help="rewrite citations that resolve to exactly one line")
    ap.add_argument("--strict", action="store_true", help="exit 1 if anything drifted")
    ap.add_argument("--verbose", action="store_true", help="list every drifted citation")
    args = ap.parse_args()

    os.chdir(REPO)
    sources = {}
    for base, rel in TARGETS.items():
        if os.path.exists(rel):
            sources[base] = read(rel)

    md_files = []
    for root, _, files in os.walk(SKILL):
        for f in sorted(files):
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))

    cites: list[Citation] = []
    for md in md_files:
        cites.extend(collect(md))
    for c in cites:
        if c.base in sources:
            resolve(c, sources[c.base])

    tally = Counter(c.verdict for c in cites)
    strengths = Counter(c.strength for c in cites if c.verdict != "UNVERIFIABLE")
    total = len(cites)

    print()
    print("  author-game-v2 — are the file:line citations still true?")
    print("  " + "─" * 68)
    print(f"  citations found              {total}")
    for v in ("OK", "DRIFTED", "AMBIGUOUS", "MISSING", "ELIDED", "PROSE",
              "UNVERIFIABLE"):
        if tally[v]:
            mark = "PASS" if v == "OK" else ("FAIL" if v in ("DRIFTED", "MISSING") else "warn")
        # ELIDED and PROSE are shapes this tool cannot judge, never defects.
            print(f"  [{mark}]  {v:<26} {tally[v]:>5}"
                  f"   ({100 * tally[v] / max(total, 1):.0f}%)")
    print(f"  anchored by                 strong {strengths['strong']} · "
          f"named {strengths['named']}")
    print("  " + "─" * 68)

    # Two guards learned from this tool's own first run, both of which would have
    # turned merely-stale citations into false ones:
    #   1. A RANGE (`v2.py:5140-5145`) names a span. One anchor cannot reproduce a span,
    #      and the first run proposed collapsing a JS portrait range onto a Python
    #      parser line 6,000 lines away. Ranges are reported and never rewritten.
    #   2. Two citations on ONE markdown line resolving to the SAME target were
    #      distinguishing two lines; collapsing them destroys what the sentence said.
    fixable = [c for c in cites
               if c.verdict == "DRIFTED" and c.proposal and c.end is None]
    seen = Counter((c.md, c.mdline, c.proposal) for c in fixable)
    collapsed = {k for k, n in seen.items() if n > 1}
    if collapsed:
        fixable = [c for c in fixable
                   if (c.md, c.mdline, c.proposal) not in collapsed]
    if fixable and args.verbose:
        print()
        by_file = Counter(os.path.relpath(c.md, SKILL) for c in fixable)
        for f, n in by_file.most_common():
            print(f"    {f:<34} {n:>4} drifted")
        print()
        for c in fixable[:40]:
            print(f"    {os.path.relpath(c.md, SKILL)}:{c.mdline}  "
                  f"{c.raw} → {c.base}:{c.proposal}   [{c.strength}] {c.anchor[:46]!r}")
        if len(fixable) > 40:
            print(f"    … and {len(fixable) - 40} more")

    # The rest of DRIFTED: real drift the guards above refuse to rewrite. Listing it
    # is the whole point of --verbose — without this block a run whose drift is
    # ENTIRELY ranges and same-line pairs prints a count and nothing else, which is
    # what it did after the 2026-08-29 engine edits: "21 drifted", no way to see them.
    if args.verbose:
        held = [c for c in cites
                if c.verdict == "DRIFTED" and c not in set(fixable)]
        if held:
            print()
            print(f"    {len(held)} drifted but NOT auto-fixable — each needs a human:")
            for c in held[:40]:
                if c.end is not None:
                    why = "range: one anchor cannot name a span"
                elif not c.proposal:
                    why = "anchor resolves nowhere or to several lines"
                else:
                    why = "two citations on one line share a target"
                print(f"    {os.path.relpath(c.md, SKILL)}:{c.mdline}  "
                      f"{c.raw}   [{why}] {c.anchor[:40]!r}")
            if len(held) > 40:
                print(f"    … and {len(held) - 40} more")

    if args.fix and fixable:
        edits: dict[str, list[Citation]] = {}
        for c in fixable:
            edits.setdefault(c.md, []).append(c)
        changed = 0
        for md, cs in edits.items():
            lines = read(md)
            # right to left within a line, so earlier columns keep their offsets
            for c in sorted(cs, key=lambda c: (-c.mdline, -c.col)):
                text = lines[c.mdline - 1]
                new_raw = c.raw.replace(f":{c.line}", f":{c.proposal}", 1)
                if text[c.col:c.col + len(c.raw)] != c.raw:
                    continue                      # moved under us; skip rather than guess
                lines[c.mdline - 1] = text[:c.col] + new_raw + text[c.col + len(c.raw):]
                changed += 1
            with open(md, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
        print(f"\n  rewrote {changed} citation(s) that resolved to exactly one line.")
        print("  AMBIGUOUS and UNVERIFIABLE ones were not touched — they need a human.")

    if tally["DRIFTED"] or tally["MISSING"]:
        print(f"\n  {tally['DRIFTED'] + tally['MISSING']} citation(s) point at the wrong "
              f"line. Run with --fix to re-anchor the unambiguous ones.")
        if args.strict:
            return 1
    elif not tally["AMBIGUOUS"]:
        print("\n  every checkable citation is anchored.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
