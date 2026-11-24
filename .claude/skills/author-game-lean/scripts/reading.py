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
scene. Verdicts are PASS, FAIL, N/A or WAIVED (a FAIL LO waived in NOTES.md, in his words). A FAIL always names the
screen of the line judged; --record refuses a "*" FAIL.

What goes on the work list:
  - every row that fires on a screen that is new or whose hash changed, asked for that screen only (on a card
    with Does:, a row fires on a screen when it is `always` or a trigger on the screen's Does: line);
  - a "*" verdict is NOT asked again when one screen changes: a "*" PASS means "passes on every screen it fires
    on", so it carries for the screens that didn't change. Only SCENE_WIDE tests (B1, B2, B9) are asked again on
    "*" when any screen changes, and so is every "*" verdict on a card without Does:;
  - every FAIL from the last pass, except on a `note` row: a note's FAIL carries like a PASS and comes back only
    when its screen or its rule changes (a note never holds; P10's C151 FAILs could never leave the list);
  - when only a screen's facts changed (its sheet row, or the schedule rows of the people it names) and not its
    text: only the rows that read facts (FACT_ROWS, FACT_WHEN, FACT_CHECKS; see reads_facts);
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
# Scene tests that judge the scene as a whole and can't be placed on one screen: B1 (an earlier canvas showed him
# wanting it), B2 (this scene goes one step further than the last one with him), B9 (companion and rival, from
# PLAN.md). A "*" verdict on one of these is asked again on "*" whenever any screen of the scene changes.
SCENE_WIDE = ("B1", "B2", "B9")
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
    out.update({t: (set() if t in SCENE_WIDE else set(does)) for t in scene_tests(skill)})  # scene-wide: "*" only
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
            out[key] = {"text": digest({"node": node, "trigger": trig}),
                        "facts": digest({"facts": facts, "sheet": sheet_rows.get(key)}),
                        # the single hash records written before 2026-11-24 hold, to read them as they are
                        "all": digest({"node": node, "trigger": trig, "facts": facts, "sheet": sheet_rows.get(key)})}
    return out


# Rows that read facts a schedule or the sheet holds (who is where, the clock, her clothes, the flags). Only these are
# asked again when a screen's facts change and its text doesn't. A truth break from a moved fact is a line that is no
# longer true, and every such line is judged by the truth rule (C460, C461) and scene test B10 (true on every visit),
# which apply on every screen; so a fact change can't slip past, whatever else stays carried.
FACT_ROWS = ("C460", "C461", "B8", "B10")
FACT_WHEN = ("the clock moves", "a garment is named", "she dresses or undresses")  # not "a person is on screen":
# those rows judge how a person sounds or is named, not where they are (LO, relayed 2026-11-24)
FACT_CHECKS = ("presence", "sheet")


def reads_facts(rid, table):
    if rid in FACT_ROWS:
        return True
    r = table.get(rid)
    return bool(r) and (bool(set(r["when"]) & set(FACT_WHEN)) or bool(set(r["checks"]) & set(FACT_CHECKS)))


def screen_change(old, new):
    """None, "text" or "facts". An old single-hash record compares against the combined hash; a change there counts
    as a text change, the safe reading."""
    if old is None:
        return "text"
    if isinstance(old, str):
        return None if old == new["all"] else "text"
    if old.get("text") != new["text"]:
        return "text"
    return "facts" if old.get("facts") != new["facts"] else None


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
    where = row_screens(game_dir, card_id, skill)
    table = rules.table(skill)
    kind = {s: screen_change(old_sc.get(s), sc[s]) for s in sc if s != WHOLE}
    changed = {s for s, k in kind.items() if k}
    gone = {s for s in old_sc if s not in sc}
    wanted = {}

    def want(row, screen, why):
        wanted.setdefault((row, screen), why)

    for s in sorted(changed):
        for r in sorted(rows):
            if where is None or s in where.get(r, ()):
                if kind[s] == "facts" and where is not None and not reads_facts(r, table):
                    continue  # only a fact moved (a schedule, the sheet): this row doesn't read facts
                why = "screen is new" if s not in old_sc else ("screen changed" if kind[s] == "text" else "a fact changed")
                want(r, s, why)
    judged = set()
    for v in rec.get("verdicts", []):
        r, s = v["row"], v["screen"]
        judged.add(r)
        if s in gone or (r not in rows and r not in old_rows):
            continue
        note = where is not None and table.get(r, {}).get("judge") == "note"
        if v["verdict"] == "FAIL" and not note:
            want(r, s, "failed last pass")
        elif r in rows and old_rows.get(r) != rows[r]:
            want(r, s, "its rule's text changed")
        elif s == WHOLE and any(k == "text" for k in kind.values()) and (r in SCENE_WIDE or where is None):
            want(r, s, "a screen of the scene changed")
        elif (r, s) not in wanted:
            # A note's FAIL is shown in the notes and never holds (reader.md, build.md): it carries like a PASS and
            # comes back only when its screen or its rule changes. A "*" PASS holds on every screen the row fires on. A changed screen it fires on is already asked
            # above, for that screen only; the "*" verdict carries for the rest.
            carried.append(dict(v, carried=True))
    for i in rec.get("pending", []):
        if (i["screen"] == WHOLE or i["screen"] in sc) and i["row"] in rows:
            want(i["row"], i["screen"], "still to ask: " + i["why"].replace("still to ask: ", ""))
    for r in sorted(set(rows) - judged):
        want(r, WHOLE, "never judged")
    items = [{"row": r, "screen": s, "why": w} for (r, s), w in sorted(wanted.items())]
    return {"items": items, "carried": carried, "screens": sc, "rows": rows}


# ── recording a pass ──────────────────────────────────────────────────────────────────────────────────────

def record(game_dir, card_id, reader_out, skill=SKILL, game=None):
    """Merge one batch of verdicts into the record. reader_out is {"verdicts": [...], "causes": [...]}.
    Returns the new record. A verdict not on the work list is refused, so the record can't drift. The batch may be
    partial: what it doesn't answer is kept as `pending` and asked again next time; the pass number moves on only
    when the last pass had nothing pending."""
    work = work_list(game_dir, card_id, skill=skill, game=game)
    asked = {(i["row"], i["screen"]) for i in work["items"]}
    rec = load_record(game_dir, card_id) or {}
    table = rules.table(skill)
    notes_on = row_screens(game_dir, card_id, skill) is not None  # labels apply to a card with Does:
    new = []
    for v in reader_out.get("verdicts", []):
        if v.get("verdict") not in VERDICTS:
            raise ValueError(f"{v.get('row')} on {v.get('screen')}: verdict must be one of {VERDICTS}")
        key = (v.get("row"), v.get("screen", WHOLE))
        if key not in asked and not (key[1] != WHOLE and (key[0], WHOLE) in asked):
            raise ValueError(f"{key[0]} on {key[1]} was not on the work list")
        note = notes_on and table.get(key[0], {}).get("judge") == "note"
        if v["verdict"] == "FAIL" and not v.get("cause") and not note:
            raise ValueError(f"{key[0]} on {key[1]}: a FAIL names its cause")
        if v["verdict"] == "FAIL" and key[1] == WHOLE:
            raise ValueError(f"{key[0]}: a FAIL names the screen of the line judged, never \"*\"")
        new.append({"row": key[0], "screen": key[1], "verdict": v["verdict"], "line": v.get("line", ""),
                    "why": v.get("why", ""), "cause": None if note else v.get("cause"), "note": note,
                    "screen_hash": work["screens"].get(key[1]), "row_hash": work["rows"].get(key[0]),
                    "carried": False})
    answered = {(v["row"], v["screen"]) for v in new}
    # An item asked on "*" and answered on screens counts as answered.
    answered |= {(r, WHOLE) for r, _ in answered}
    # A batch may be partial (a pass can die mid-way): the items it doesn't answer stay pending, and the next
    # work list asks them again whatever the hashes say (LO, relayed 2026-11-24).
    pending = [i for i in work["items"] if (i["row"], i["screen"]) not in answered]
    unanswered = {(i["row"], i["screen"]) for i in pending}
    # A carried verdict is replaced only by a new verdict on the same screen, or when its row was asked on "*"
    # again and answered (then the new verdicts are the whole answer). A "*" PASS survives a new verdict on one
    # screen. An unanswered item keeps the verdict it had, so a FAIL not yet asked again is still a FAIL.
    redone = {(v["row"], v["screen"]) for v in new}
    whole_again = {r for r, s in asked if s == WHOLE and (r, s) in answered}
    kept = [v for v in work["carried"] if (v["row"], v["screen"]) not in redone and v["row"] not in whole_again]
    kept += [dict(v, carried=True) for v in rec.get("verdicts", []) if (v["row"], v["screen"]) in unanswered]
    causes = reader_out.get("causes", [])
    # A later batch of the same pass may name a cause an earlier batch gave.
    old_causes = {c.get("id"): c for c in rec.get("causes", [])} if rec.get("pending") else {}
    known = {c.get("id") for c in causes} | set(old_causes)
    for v in new:
        if v["verdict"] == "FAIL" and not v["note"] and v["cause"] not in known:
            raise ValueError(f"cause `{v['cause']}` is not in causes")
    causes = list({**old_causes, **{c.get("id"): c for c in causes}}.values())  # a batch adds to its pass's causes
    out = {"piece": card_id, "pass": rec.get("pass", 0) + (0 if rec.get("pending") else 1),
           "screens": work["screens"], "rows": work["rows"],
           "verdicts": sorted(kept + new, key=lambda v: (v["row"], v["screen"])), "causes": causes,
           "pending": pending, "asked": len(work["items"]), "answered": len(work["items"]) - len(pending)}
    path = record_path(game_dir, card_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return out


def by_cause(rec):
    """Lines of the FAIL table grouped by cause: one head line per cause, then the rows it breaks."""
    lines = []
    fails = [v for v in rec.get("verdicts", []) if v["verdict"] == "FAIL" and not v.get("note")]
    for c in rec.get("causes", []):
        mine = [v for v in fails if v["cause"] == c.get("id")]
        if mine:
            lines.append(f"{c['id']} · {c.get('what', '')} ({len(mine)} row(s))")
            lines += [f"  {v['row']} | {v['screen']} | {v['line'][:80]}" for v in mine]
    notes = [v for v in rec.get("verdicts", []) if v["verdict"] == "FAIL" and v.get("note")]
    if notes:
        lines.append(f"notes, shown and never holding ({len(notes)})")
        lines += [f"  {v['row']} | {v['screen']} | {v['line'][:80]}" for v in notes]
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
        fails = sum(1 for v in rec["verdicts"] if v["verdict"] == "FAIL" and not v.get("note"))
        print(f"recorded {rec['answered']} of {rec['asked']}; {len(rec['pending'])} still to ask")
        print(f"pass {rec['pass']}: {len(rec['verdicts'])} verdicts, {fails} FAIL that hold")
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
