#!/usr/bin/env python3
"""Read ACROSS the person sheets — the thing the sheet format could not do.

`the-sheets.md` S5, the incident, three parts:

  * Del was declared 22:00-02:00 at the desk on one sheet and 22:00-02:00 in the office on
    another. He cannot be in both.
  * Marek was declared in the corridor 00:20-01:30 and in the bathroom 00:00-01:00 -- forty
    minutes of overlap.
  * And a rung needed him at the monitor at four in the morning. No sheet had him at the desk
    at that hour, so the rung was AUTHORED AND UNREACHABLE. It was found by writing schedule
    rows, not by reading sheets.

All three are "two documents each correct about one room, with nothing in the format reading
across them". This is the thing that reads across them.

It is NOT a gates.py mode and does not pretend to be. It reads the sheets, which is possible
here only because FORMAT.md put every row in a fixed column shape instead of in typography --
the exact reason the corpus-wide version of this check was costed and dropped on 2026-09-03.

Exits non-zero on any finding.  Self-test:  --selftest
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PEOPLE = os.path.join(os.path.dirname(HERE), "sheets", "people")
SCENES = os.path.join(os.path.dirname(HERE), "sheets", "scenes")

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_days(cell):
    """'Mon-Sun' -> all seven; 'Sun' -> one; 'Mon,Wed' -> two."""
    cell = cell.strip()
    if "-" in cell:
        a, _, b = cell.partition("-")
        try:
            i, j = DAYS.index(a.strip()), DAYS.index(b.strip())
        except ValueError:
            return set()
        return set(DAYS[i:j + 1]) if i <= j else set(DAYS[i:] + DAYS[:j + 1])
    return {d.strip() for d in cell.split(",") if d.strip() in DAYS}


def minutes(hhmm):
    h, _, m = hhmm.strip().partition(":")
    return int(h) * 60 + int(m)


def slots(a, b):
    """The set of minutes covered by [a, b), wrapping past midnight if b <= a.

    A set rather than an interval because the wrap case (23:00-08:00) is where interval
    arithmetic quietly gets it wrong, and this runs on fourteen rows.
    """
    a, b = minutes(a), minutes(b)
    if b > a:
        return set(range(a, b))
    return set(range(a, 1440)) | set(range(0, b))


def rows_under(text, heading, ncols):
    """Every markdown table row under a `## heading`, as stripped cell lists."""
    out = []
    body = text.split(heading, 1)[1] if heading in text else ""
    for line in body.splitlines():
        if line.startswith("## ") and out:
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != ncols or set(cells[0]) <= set("- "):
            continue
        out.append(cells)
    return out


def bare(cell):
    return cell.strip().strip("`*").strip()


def load(directory):
    people = {}
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".md"):
            continue
        who = fn[:-3]
        text = open(os.path.join(directory, fn)).read()
        sched = []
        for c in rows_under(text, "## Schedule grid", 5):
            if c[0].lower() == "location":
                continue
            sched.append({"loc": bare(c[0]), "days": parse_days(c[1]),
                          "slots": slots(c[2], c[3]), "raw": f"{c[2]}-{c[3]}"})
        arc = []
        for c in rows_under(text, "## The arc", 9):
            if not c[0].strip().isdigit():
                continue
            arc.append({"step": c[0], "name": bare(c[1]), "canvas": bare(c[2]),
                        "place": bare(c[3]), "slots": slots(c[4], c[5]),
                        "raw": f"{c[4]}-{c[5]}", "sex": bare(c[8]).lower()})
        meets = []
        for c in rows_under(text, "## The meeting", 8):
            if c[0].lower() == "canvas":
                continue
            meets.append({"canvas": bare(c[0]), "place": bare(c[1]),
                          "days": parse_days(c[2]), "slots": slots(c[3], c[4]),
                          "raw": f"{c[3]}-{c[4]}", "flag": bare(c[5]),
                          "words": bare(c[6])})
        people[who] = {"schedule": sched, "arc": arc, "meetings": meets}
    return people


def check(people):
    findings = []

    # 1 - is anyone in two places at once?  (Del)
    # 2 - does anyone overlap themselves?   (Marek)
    for who, p in people.items():
        for i, a in enumerate(p["schedule"]):
            for b in p["schedule"][i + 1:]:
                shared_days = a["days"] & b["days"]
                shared_time = a["slots"] & b["slots"]
                if shared_days and shared_time:
                    kind = ("in TWO PLACES at once" if a["loc"] != b["loc"]
                            else "OVERLAPPING HIMSELF")
                    findings.append(
                        f"{who}: {kind} — `{a['loc']}` {a['raw']} and `{b['loc']}` {b['raw']}"
                        f" share {len(shared_time)} min on {sorted(shared_days)}")

    # 3 - is every arc step reachable?  (the four-in-the-morning defect)
    for who, p in people.items():
        for step in p["arc"]:
            covering = [s for s in p["schedule"]
                        if s["loc"] == step["place"] and step["slots"] <= s["slots"]]
            if not covering:
                at = [f"`{s['loc']}` {s['raw']}" for s in p["schedule"]]
                findings.append(
                    f"{who} step {step['step']} ({step['canvas']}) is UNREACHABLE — "
                    f"needs him at `{step['place']}` {step['raw']}, but he is only at "
                    + (", ".join(at) or "NOWHERE"))

    # 4 - does every meeting fire where that character actually IS?  (F5)
    # `requires_npc` does not gate the auto-fire path (v2.py:4559), so a meeting whose window
    # is outside its own character's hours plays to an EMPTY ROOM. Vesper scored 0 of 18.
    for who, p in people.items():
        for m in p.get("meetings", []):
            covering = [s for s in p["schedule"]
                        if s["loc"] == m["place"] and m["slots"] <= s["slots"]
                        and m["days"] <= s["days"]]
            if not covering:
                at = [f"`{s['loc']}` {s['raw']}" for s in p["schedule"]]
                findings.append(
                    f"{who} MEETING {m['canvas']} plays to an EMPTY ROOM — fires at "
                    f"`{m['place']}` {m['raw']} on {sorted(m['days'])}, but he is only at "
                    + (", ".join(at) or "NOWHERE"))

    # 6 - does every arc step's canvas actually HAVE a scene sheet?
    # Nothing compared these two documents until 2026-09-03. A promised scene that was never
    # written is the class of defect the sheets phase exists to catch, and the-sheets.md S1's own
    # survey records `orientation` naming a canvas three times after it was deleted from the build.
    # Read from the SCENES dir if it exists; a game with no scene sheets yet is not failed.
    if os.path.isdir(SCENES):
        body = "".join(open(os.path.join(SCENES, f)).read()
                       for f in sorted(os.listdir(SCENES)) if f.endswith(".md"))
        if body:
            for who, p in people.items():
                for step in p["arc"]:
                    if step["canvas"] and step["canvas"] not in body:
                        findings.append(
                            f"{who} step {step['step']} names `{step['canvas']}` and NO scene "
                            f"sheet mentions it — a promised scene that was never written")

    # 5 - one flag per character.  (F8) One flag must never open more than one hub.
    seen = {}
    for who, p in people.items():
        for m in p.get("meetings", []):
            if m["flag"] in seen:
                findings.append(
                    f"MEETING FLAG `{m['flag']}` is shared by {seen[m['flag']]} and {who} — "
                    "one flag never opens the whole cast (F8)")
            seen[m["flag"]] = who
    return findings


def report(people, findings):
    print(f"  check_people — {len(people)} sheets · "
          f"{sum(len(p['schedule']) for p in people.values())} schedule rows · "
          f"{sum(len(p['arc']) for p in people.values())} arc steps · "
          f"{sum(len(p.get('meetings', [])) for p in people.values())} meetings")
    for who in sorted(people):
        p = people[who]
        n = len(p["arc"])
        nosex = sum(1 for s in p["arc"] if s["sex"] == "no")
        pct = (100 * nosex / n) if n else 0
        conv = any("CONVERSION" in s["name"].upper() for s in p["arc"])
        mt = p.get("meetings", [])
        mtxt = f"{mt[0]['canvas']} @ {mt[0]['raw']}" if mt else "NO MEETING"
        print(f"    {who:10} {n} steps · {nosex} without sex ({pct:.0f}%) · "
              f"conversion: {'yes' if conv else 'NO'} · {mtxt}")
    print()
    if not findings:
        print("  no findings — nobody double-booked, nobody overlapping, "
              "every arc step reachable, every meeting fires where he is")
        return 0
    for f in findings:
        print(f"  [FINDING] {f}")
    return 1


def selftest():
    """A check that has never failed is not known to work.

    Injects each of S5's three incidents into a copy of the real data and asserts that the
    checker catches each one. Runs on the real sheets, changes nothing on disk.
    """
    people = load(PEOPLE)
    assert not check(people), "self-test needs the real sheets to be clean first"
    ok = True

    a = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"])} for k, v in people.items()}
    a["renner"]["schedule"] = a["renner"]["schedule"] + [
        {"loc": "penthouse", "days": set(DAYS), "slots": slots("09:00", "18:00"), "raw": "09:00-18:00"}]
    hit = [f for f in check(a) if "TWO PLACES" in f]
    print(f"  [selftest] two places at once  : {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    b = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"])} for k, v in people.items()}
    b["kess"]["schedule"] = b["kess"]["schedule"] + [
        {"loc": "kess_berth", "days": set(DAYS), "slots": slots("21:00", "23:00"), "raw": "21:00-23:00"}]
    hit = [f for f in check(b) if "OVERLAPPING" in f]
    print(f"  [selftest] overlapping himself : {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    c = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"])} for k, v in people.items()}
    c["colm"]["arc"] = c["colm"]["arc"] + [
        {"step": "99", "name": "four in the morning", "canvas": "arc_colm_99",
         "place": "underworld_bar", "slots": slots("04:00", "05:00"), "raw": "04:00-05:00",
         "sex": "no"}]
    hit = [f for f in check(c) if "UNREACHABLE" in f]
    print(f"  [selftest] unreachable arc step: {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    e = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"]),
             "meetings": list(v["meetings"])} for k, v in people.items()}
    e["renner"]["meetings"] = [dict(e["renner"]["meetings"][0],
                                    slots=slots("04:00", "05:00"), raw="04:00-05:00")]
    hit = [f for f in check(e) if "EMPTY ROOM" in f]
    print(f"  [selftest] meeting to empty room: {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    g = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"]),
             "meetings": list(v["meetings"])} for k, v in people.items()}
    g["colm"]["meetings"] = [dict(g["colm"]["meetings"][0], flag="met_renner")]
    hit = [f for f in check(g) if "MEETING FLAG" in f]
    print(f"  [selftest] one flag, two hubs   : {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    h = {k: {"schedule": list(v["schedule"]), "arc": list(v["arc"]),
             "meetings": list(v["meetings"])} for k, v in people.items()}
    h["marsh"]["arc"] = h["marsh"]["arc"] + [
        {"step": "98", "name": "unwritten", "canvas": "arc_marsh_98",
         "place": "underworld_brothel", "slots": slots("20:00", "23:00"), "raw": "20:00-23:00",
         "sex": "no"}]
    hit = [f for f in check(h) if "never written" in f]
    print(f"  [selftest] arc step with no scene : {'CAUGHT' if hit else 'MISSED'}")
    ok &= bool(hit)

    print("\n  self-test PASSED — the instrument can fail" if ok
          else "\n  self-test FAILED — do not trust a green run")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    ppl = load(PEOPLE)
    sys.exit(report(ppl, check(ppl)))
