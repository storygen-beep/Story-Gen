"""The reader's memory: what the next reader pass must judge, and the verdicts it keeps.

    venv/bin/python .claude/skills/author-game-lean/scripts/reading.py games/<slug> <id> [--all]
        prints the work list as JSON: the screens, the rows, and each (row, screen) to judge, with why
    venv/bin/python .claude/skills/author-game-lean/scripts/reading.py --record games/<slug> <id> <verdicts.json>
        stamps the reader's verdicts with today's hashes, carries what wasn't re-judged, and writes
        games/<slug>/reader/<id>.json

Why (LO, relayed 2026-11-24, "Yes go ahead"): every P13 reader pass, v5 to v11, was a fresh agent that judged
everything again, so a row could pass on one pass and fail on the next on the same text.

The record, games/<slug>/reader/<id>.json:
    {"piece": id, "pass": n, "screens": {screen: hash}, "rows": {row: hash},
     "verdicts": [{"row", "screen", "verdict", "line", "why", "cause", "screen_hash", "row_hash", "carried"}],
     "causes": [{"id", "what", "rows": [[row, screen], ...]}]}
A screen is "<canvas>.<node>" for every canvas the card's Builds: line names, or "*" for a verdict on the whole
scene. Verdicts are PASS, FAIL, N/A or WAIVED (a FAIL LO waived in NOTES.md, in his words).

What goes on the work list:
  - every row on a screen that is new or whose hash changed;
  - every verdict on "*" when any screen changed;
  - every FAIL from the last pass;
  - every row whose text changed in its craft file;
  - every row never judged (on "*": the reader judges it wherever it applies).
A PASS, N/A or WAIVED on unchanged text is carried, marked "carried". --all puts every row on every screen.

A screen's hash covers its blocks and its exit, the trigger of its canvas, the schedule rows of everyone it can name
(a speaker, or a name or one-word role in its prose, `scenes.people`), and its row of the scene sheet (sheet.py:
clock, place, who is there, what she wears, flags), so a moved schedule row, or an equip or flag changed on an
earlier screen, re-opens it. It does NOT cover a number in PLAN.md or another card, or what another canvas does to
her clothes before a repeatable (the sheet reads a repeatable's clothes only from its own trigger). Those re-open
only with --all.
"""
import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
import scenes  # noqa: E402
import sheet  # noqa: E402
import rules  # noqa: E402

VERDICTS = ("PASS", "FAIL", "N/A", "WAIVED")
KEEP = ("PASS", "N/A", "WAIVED")
WHOLE = "*"


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


# ── what the reader judges ────────────────────────────────────────────────────────────────────────────────

def scene_tests(skill=SKILL):
    """{"B<n>": text} from reader.md part B."""
    text = (Path(skill) / "reader.md").read_text(encoding="utf-8")
    part = text.split("**B · The scene**", 1)[-1].split("\n## ", 1)[0]
    return {f"B{n}": line.strip() for n, line in re.findall(r"^(\d+)\. (.+)$", part, re.M)}


def craft_rows(name, skill=SKILL):
    """{row id: its text} for one craft file: its must-read rows and the numbered steps of "The shape"."""
    path = Path(skill) / name
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    out = {}
    must = text.split("## Must read", 1)[-1].split("\n## ", 1)[0] if "## Must read" in text else ""
    for m in re.finditer(r"^\| ([CL]\d+) \|.*$", must, re.M):
        out[m.group(1)] = m.group(0)
    shape = text.split("## The shape", 1)[-1].split("\n## ", 1)[0] if "## The shape" in text else ""
    stem = Path(name).stem
    for n, line in re.findall(r"^(\d+)\. (.+)$", shape, re.M):
        out[f"{stem}#{n}"] = line
    return out


def card_lines(game_dir, card_id):
    text = (Path(game_dir) / "cards" / f"{card_id}.md").read_text(encoding="utf-8")
    craft = re.search(r"^Craft:[ \t]*(.*)$", text, re.M)
    builds = re.search(r"^Builds:[ \t]*(.*)$", text, re.M)
    files = sorted(set(re.findall(r"craft/[\w-]+\.md", craft.group(1) if craft else "")) | {"craft/voice.md"})
    ids = [x.strip(" `") for x in (builds.group(1).split(",") if builds else [])]
    return files, [i for i in ids if i and i.lower() != "none" and not i.startswith("<")]


def does_of(game_dir, card_id):
    return rules.card_does((Path(game_dir) / "cards" / f"{card_id}.md").read_text(encoding="utf-8"))


def rows_for(game_dir, card_id, skill=SKILL):
    """{row: text}. A card with a Does: block: the 13 scene tests plus its rule list (rules.py), each row's text
    with its labels, so a relabel re-opens it. An older card: the 13 tests plus every must-read row and shape step
    of every craft file its Craft: line names, plus voice.md."""
    does = does_of(game_dir, card_id)
    out = dict(scene_tests(skill))
    if does is not None:
        table = rules.table(skill)
        for rid in rules.rule_list(does, skill, table):
            r = table[rid]
            out[rid] = f"{r['asks']} | {', '.join(r['when'])} | {r['judge']}"
        return out
    files, _ = card_lines(game_dir, card_id)
    for f in files:
        out.update(craft_rows(f, skill))
    return out


def row_screens(game_dir, card_id, skill=SKILL):
    """{row: set of screens it applies on}, or None for a card without Does: (every row on every screen)."""
    does = does_of(game_dir, card_id)
    if does is None:
        return None
    out = {rid: set(on) for rid, on in rules.rule_list(does, skill).items()}
    out.update({t: set(does) for t in scene_tests(skill)})
    return out


# ── the screens and their hashes ──────────────────────────────────────────────────────────────────────────

def load_game(game_dir):
    return tomllib.loads((Path(game_dir) / "toml_phases" / "7_final_game.toml").read_text(encoding="utf-8"))


def screens(game, canvas_ids, sheet_rows=None):
    """{screen: hash} for every screen of the named canvases. The hash takes in the screen's sheet row, so a time,
    a person, a garment or a flag that changed upstream re-opens it."""
    sheet_rows = sheet_rows or {}
    who = scenes.people(game)
    rows_of = {n.get("id"): n.get("schedules") or [] for n in game.get("npcs") or []}
    out = {}
    for c in game.get("canvases") or []:
        if c.get("id") not in canvas_ids:
            continue
        trig = c.get("trigger") or {}
        for node in c.get("nodes") or []:
            blob = json.dumps(node, sort_keys=True, default=str)
            named = {pid for pid, rx in who if rx.search(blob)}
            named |= set(re.findall(r'"npcId": "([\w-]+)"', blob))
            named |= {trig.get("npc"), trig.get("requires_npc")} - {None}
            facts = {p: rows_of.get(p, []) for p in sorted(named)}
            key = f"{c['id']}.{node.get('id')}"
            out[key] = digest({"node": node, "trigger": trig, "facts": facts, "sheet": sheet_rows.get(key)})
    return out


def whole_hash(screen_hashes):
    return digest(sorted(screen_hashes.items()))


# ── the work list ─────────────────────────────────────────────────────────────────────────────────────────

def record_path(game_dir, card_id):
    return Path(game_dir) / "reader" / f"{card_id}.json"


def load_record(game_dir, card_id):
    path = record_path(game_dir, card_id)
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def current(game_dir, card_id, skill=SKILL, game=None):
    """(screen hashes, row hashes) for the build as it is now."""
    game = game or load_game(game_dir)
    _, builds = card_lines(game_dir, card_id)
    _, sheet_rows = sheet.for_card(game, game_dir, card_id)
    sc = screens(game, set(builds), sheet_rows)
    sc[WHOLE] = whole_hash(sc)
    rows = {r: digest(t) for r, t in rows_for(game_dir, card_id, skill).items()}
    return sc, rows


def work_list(game_dir, card_id, everything=False, skill=SKILL, game=None):
    """{"items": [{row, screen, why}], "carried": [...], "screens": {...}, "rows": {...}}."""
    sc, rows = current(game_dir, card_id, skill, game)
    rec = None if everything else load_record(game_dir, card_id)
    items, carried = [], []
    if rec is None:
        why = "--all" if everything else "first pass"
        items = [{"row": r, "screen": WHOLE, "why": why} for r in sorted(rows)]
        return {"items": items, "carried": [], "screens": sc, "rows": rows}
    old_sc, old_rows = rec.get("screens", {}), rec.get("rows", {})
    changed = {s for s in sc if s != WHOLE and old_sc.get(s) != sc[s]}
    gone = {s for s in old_sc if s not in sc}
    wanted = {}

    def want(row, screen, why):
        wanted.setdefault((row, screen), why)

    where = row_screens(game_dir, card_id, skill)
    for s in sorted(changed):
        for r in sorted(rows):
            if where is None or s in where.get(r, ()):
                want(r, s, "screen is new" if s not in old_sc else "screen changed")
    judged = set()
    for v in rec.get("verdicts", []):
        r, s = v["row"], v["screen"]
        judged.add(r)
        if s in gone or (r not in rows and r not in old_rows):
            continue
        if v["verdict"] == "FAIL":
            want(r, s, "failed last pass")
        elif s == WHOLE and changed:
            want(r, s, "a screen of the scene changed")
        elif r in rows and old_rows.get(r) != rows[r]:
            want(r, s, "its rule's text changed")
        elif (r, s) not in wanted:
            carried.append(dict(v, carried=True))
    for r in sorted(set(rows) - judged):
        want(r, WHOLE, "never judged")
    items = [{"row": r, "screen": s, "why": w} for (r, s), w in sorted(wanted.items())]
    return {"items": items, "carried": carried, "screens": sc, "rows": rows}


# ── recording a pass ──────────────────────────────────────────────────────────────────────────────────────

def record(game_dir, card_id, reader_out, skill=SKILL, game=None):
    """Merge one pass's verdicts into the record. reader_out is {"verdicts": [...], "causes": [...]}.
    Returns the new record. A verdict not on the work list is refused, so the record can't drift."""
    work = work_list(game_dir, card_id, skill=skill, game=game)
    asked = {(i["row"], i["screen"]) for i in work["items"]}
    rec = load_record(game_dir, card_id) or {}
    new = []
    for v in reader_out.get("verdicts", []):
        if v.get("verdict") not in VERDICTS:
            raise ValueError(f"{v.get('row')} on {v.get('screen')}: verdict must be one of {VERDICTS}")
        key = (v.get("row"), v.get("screen", WHOLE))
        if key not in asked and not (key[1] != WHOLE and (key[0], WHOLE) in asked):
            raise ValueError(f"{key[0]} on {key[1]} was not on the work list")
        if v["verdict"] == "FAIL" and not v.get("cause"):
            raise ValueError(f"{key[0]} on {key[1]}: a FAIL names its cause")
        new.append({"row": key[0], "screen": key[1], "verdict": v["verdict"], "line": v.get("line", ""),
                    "why": v.get("why", ""), "cause": v.get("cause"),
                    "screen_hash": work["screens"].get(key[1]), "row_hash": work["rows"].get(key[0]),
                    "carried": False})
    answered = {(v["row"], v["screen"]) for v in new}
    # An item asked on "*" and answered on screens counts as answered.
    answered |= {(r, WHOLE) for r, _ in answered}
    missing = sorted(asked - answered)
    if missing:
        raise ValueError(f"{len(missing)} work-list item(s) have no verdict, first: {missing[0]}")
    redone = {(v["row"], v["screen"]) for v in new} | {(v["row"], WHOLE) for v in new}
    kept = [v for v in work["carried"] if (v["row"], v["screen"]) not in redone and v["row"] not in
            {r for r, s in asked if s == WHOLE}]
    causes = reader_out.get("causes", [])
    known = {c.get("id") for c in causes}
    for v in new:
        if v["verdict"] == "FAIL" and v["cause"] not in known:
            raise ValueError(f"cause `{v['cause']}` is not in causes")
    out = {"piece": card_id, "pass": rec.get("pass", 0) + 1, "screens": work["screens"], "rows": work["rows"],
           "verdicts": sorted(kept + new, key=lambda v: (v["row"], v["screen"])), "causes": causes}
    path = record_path(game_dir, card_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return out


def by_cause(rec):
    """Lines of the FAIL table grouped by cause: one head line per cause, then the rows it breaks."""
    lines = []
    fails = [v for v in rec.get("verdicts", []) if v["verdict"] == "FAIL"]
    for c in rec.get("causes", []):
        mine = [v for v in fails if v["cause"] == c.get("id")]
        if mine:
            lines.append(f"{c['id']} · {c.get('what', '')} ({len(mine)} row(s))")
            lines += [f"  {v['row']} | {v['screen']} | {v['line'][:80]}" for v in mine]
    return lines


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--record"]:
        ap = argparse.ArgumentParser(description="Record one reader pass.")
        ap.add_argument("game_dir")
        ap.add_argument("card_id")
        ap.add_argument("verdicts")
        a = ap.parse_args(argv[1:])
        rec = record(a.game_dir, a.card_id, json.loads(Path(a.verdicts).read_text(encoding="utf-8")))
        fails = sum(1 for v in rec["verdicts"] if v["verdict"] == "FAIL")
        print(f"pass {rec['pass']}: {len(rec['verdicts'])} verdicts, {fails} FAIL")
        print("\n".join(by_cause(rec)))
        return 1 if fails else 0
    ap = argparse.ArgumentParser(description="Print the next reader pass's work list.")
    ap.add_argument("game_dir")
    ap.add_argument("card_id")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    w = work_list(a.game_dir, a.card_id, everything=a.all)
    print(json.dumps({"items": w["items"], "carried": len(w["carried"])}, indent=1))
    return 0 if not w["items"] else 3


if __name__ == "__main__":
    sys.exit(main())
