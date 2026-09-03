#!/usr/bin/env python3
"""Re-measure every beat written into a scene sheet, and compare it to what the sheet CLAIMS.

`the-sheets.md` S1, the incident this exists against:

    Every night_desk scene sheet said things like "5 beats · 1 explicit", and those beats were
    PARAGRAPHS. gates.py's Beat is one NODE. The design reported 75 beats; the build had 52.
    Mid-session the same game read 6 explicit by the sheet and 3 by the instrument on the same
    afternoon, and both numbers were given to LO in chat as if they measured the same thing.

    "A number written on a sheet is a PROMISE. It becomes a measurement when an instrument
    produces it and not before."

So a `[MEASURED]` line on a sheet is not trusted here. It is EXTRACTED, re-run through the real
instrument, and any disagreement is printed as a finding. The sheet does not get to grade itself.

Every threshold below is one `gates.py` already uses; none is new.

Exits non-zero on a mismatch, or on an explicit beat under the 3+ floor.
Self-test:  --selftest
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
SCENES = os.path.join(GAME, "sheets", "scenes")
REPO = os.path.dirname(os.path.dirname(GAME))
GATES = os.path.join(REPO, ".claude", "skills", "author-game-v2", "scripts", "gates.py")

# A beat is a blockquote immediately followed by a `[MEASURED]` line. Doctrine quotations are
# blockquotes too, which is why the marker is required rather than assumed -- a parser that took
# every blockquote would grade the evidence blocks.
CLAIM = re.compile(
    r"`\[MEASURED\]`\s*(?P<words>\d+)\s*w(?:ords)?\b.*?"
    r"\*\*(?P<expl>\d+)\s*explicit\*\*.*?"
    r"median sentence\s*\**(?P<med>\d+)",
    re.S)


def extract(path):
    """[(beat_text, claimed_dict, line_no)] for one sheet.

    TWO shapes, because a banded act node is a table and a one-shot beat is a blockquote, and
    a parser that read only the second left every band ungraded. D2a shipped with 9 claims and
    8 re-measured for exactly that reason.

      blockquote  a `> ` run followed within four lines by a `[MEASURED]` claim
      table cell  a row carrying a `[MEASURED]` claim; the beat is the cell BEFORE it

    Doctrine quotations are blockquotes too, which is why the claim marker is required rather
    than assumed — a parser taking every blockquote would grade the evidence blocks.
    """
    lines = open(path).read().splitlines()
    out, buf, start = [], [], None
    for i, line in enumerate(lines):
        # --- table-cell beats -------------------------------------------------
        if line.startswith("|") and "[MEASURED]" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            for j, cell in enumerate(cells):
                m = CLAIM.search(cell)
                if m and j > 0:
                    out.append((cells[j - 1],
                                {k: int(v) for k, v in m.groupdict().items()},
                                i + 1))
                    break
            continue
        # --- blockquote beats -------------------------------------------------
        if line.startswith("> "):
            if not buf:
                start = i + 1
            buf.append(line[2:].strip())
            continue
        if buf:
            window = "\n".join(lines[i:i + 4])
            m = CLAIM.search(window)
            if m:
                out.append((" ".join(buf),
                            {k: int(v) for k, v in m.groupdict().items()},
                            start))
            buf, start = [], None
    return out


def measure(text):
    """Run the REAL instrument. Never reimplement its counting here -- that is how two numbers
    that disagree both get reported as measurements."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(text + "\n")
        tmp = fh.name
    try:
        out = subprocess.run([sys.executable, GATES, "--beat", tmp],
                             capture_output=True, text=True).stdout
    finally:
        os.unlink(tmp)
    g = lambda pat: int(m.group(1)) if (m := re.search(pat, out)) else -1
    return {"words": g(r"words\s+(\d+)"),
            "expl": g(r"explicit words\s+(\d+)"),
            "med": g(r"median sentence\s+(\d+)"),
            "body": (re.search(r"body words by sentence\s+([\d ]+)", out) or [None, ""])[1].split()}


def check(scenes_dir):
    findings, beats = [], 0
    for fn in sorted(os.listdir(scenes_dir)):
        if not fn.endswith(".md"):
            continue
        for text, claim, ln in extract(os.path.join(scenes_dir, fn)):
            beats += 1
            got = measure(text)
            where = f"{fn}:{ln}"
            for key, label in (("words", "word count"), ("expl", "explicit"),
                               ("med", "median sentence")):
                if claim[key] != got[key]:
                    findings.append(
                        f"{where} — sheet CLAIMS {label} {claim[key]}, instrument says "
                        f"{got[key]}. A number on a sheet is a promise until an instrument "
                        f"produces it (S1).")
            # the floor, on beats the sheet itself calls explicit
            if claim["expl"] >= 3 and got["expl"] < 3:
                findings.append(f"{where} — below the 3+ floor at {got['expl']}")
            # the pivot: the last sentence of an explicit beat carries a body word
            if got["expl"] >= 3 and got["body"] and got["body"][-1] == "0":
                findings.append(
                    f"{where} — PIVOT: the last sentence of an explicit beat carries no body "
                    f"word (body by sentence: {' '.join(got['body'])})")
    return findings, beats


def selftest():
    findings, _ = check(SCENES)
    assert not findings, "self-test needs the real sheets clean first"
    ok = True
    with tempfile.TemporaryDirectory() as d:
        # a sheet that lies about its own explicit count
        open(os.path.join(d, "liar.md"), "w").write(
            "> You take his cock in your mouth and he holds your head.\n\n"
            "`[MEASURED]` 12 words · **3 explicit** · median sentence 12\n")
        f, _ = check(d)
        hit = [x for x in f if "CLAIMS explicit 3" in x]
        print(f"  [selftest] sheet overstates explicit : {'CAUGHT' if hit else 'MISSED'}")
        ok &= bool(hit)

    with tempfile.TemporaryDirectory() as d:
        # a beat that pivots off the body in its last sentence
        open(os.path.join(d, "pivot.md"), "w").write(
            "> He fucks your cunt against the shelving and his cock is deep in you. "
            "Afterwards you lie there deciding not to have noticed what it did to you.\n\n"
            "`[MEASURED]` 28 words · **3 explicit** · median sentence 14\n")
        f, _ = check(d)
        hit = [x for x in f if "PIVOT" in x]
        print(f"  [selftest] beat pivots off the body  : {'CAUGHT' if hit else 'MISSED'}")
        ok &= bool(hit)

    with tempfile.TemporaryDirectory() as d:
        # the same lie, in a TABLE CELL rather than a blockquote
        open(os.path.join(d, "table.md"), "w").write(
            "| band | beat | measured |\n|---|---|---|\n"
            "| low | He holds your tits and says nothing. | `[MEASURED]` 8 words · "
            "**3 explicit** · median sentence 8 |\n")
        f, n = check(d)
        hit = [x for x in f if "CLAIMS explicit 3" in x]
        print(f"  [selftest] TABLE claim overstates  : {'CAUGHT' if hit else 'MISSED'}"
              f"{'' if n else '  (parsed 0 rows — parser missed it)'}")
        ok &= bool(hit) and n == 1

    print("\n  self-test PASSED — the instrument can fail" if ok
          else "\n  self-test FAILED — do not trust a green run")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    fnd, n = check(SCENES)
    claims = sum(open(os.path.join(SCENES, f)).read().count("[MEASURED]")
                 for f in os.listdir(SCENES) if f.endswith(".md"))
    print(f"  check_beats — {n} beat(s) re-measured through gates.py --beat, "
          f"against {claims} [MEASURED] claim(s) in the sheets")
    if n != claims:
        print(f"  [FINDING] {claims - n} claim(s) are NOT re-measured — the parser cannot see "
              f"them, so they are promises, not measurements (S1)")
        fnd = fnd + ["unparsed claims"]
    if not fnd:
        print("  no findings — every sheet's numbers are the instrument's, every explicit beat "
              "clears 3+, and no explicit beat pivots off the body in its last sentence")
        sys.exit(0)
    for x in fnd:
        print(f"  [FINDING] {x}")
    sys.exit(1)
