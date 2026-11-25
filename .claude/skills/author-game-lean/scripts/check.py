"""One check command for a game built with author-game-lean.

    python3 check.py games/<slug> [--release] [--against <git ref>]

Checks:
  merge      scripts/merge_toml_phases.py runs and the merged TOML parses (--no-dev under --release)
  reach      reach.py finds no scene, media spot or portrait that can never show
  approvals  every STATE.md piece with a built date has a current approval (approve.status == approved)
  builds     every canvas, place, person and sidebar item in the merged TOML is listed in the Builds: line
             of an APPROVED card (a changed card covers nothing; canvases from 6_dev_shortcuts.toml are
             skipped; a sidebar item, which has no id, is listed as `sidebar:<trait>`, or `sidebar:<label>`)
  talk, length, presence, creation, saves, speakers, goals
             the measured scene checks in scenes.py (its docstring says what each one can and can't see).
             `--against <git ref>` sets the build `saves` compares with; the default is the last commit of
             output/index.html, the build LO played.
  sheet      every card with a `Sheet:` block: each row matches the sheet sheet.py works out from the build
             (clock, place, who is there, what she wears, flags). A column it can't work out is INCOMPLETE. A card
             with no Sheet: block (every card from before 2026-11-24) is not compared; `--card` asks new ones for it.
  does       every card with a `Does:` block: what a script can see each built screen do (rules.GUARD's list: a
             person, an equip, a garment named, a price, a time on a label, a picture, a meter effect, a goal card,
             the last screen, a first meeting, a place entered, one-time or repeatable, the opening) is named
             on that screen's Does: line. Cards without Does: are not judged. A card whose Builds: names the
             Hints page (`story_hints`, `walkthrough:<id>`) names each entry's screen on its Does: (pages.py).
  pages      under [ui] quests_layout = "hints": every first meeting a scene sets (met_*), and every flag a
             hidden place waits on, is a `when` on some hint or walkthrough step unless the opening sets it;
             every flag a hint reads is set by some canvas. Under people_page = "cot": every person has
             stranger_name and people_tab (pages.py).
  people     under [engine.people] system = "cot": every person has gender, attracted, a people_type or hand-set
             values, and 1 to 4 traits, each with a job; no person keeps a meter from before the switch; every
             skill gate names one of her skills at a level 1 to 10, and no skill has a band table too (people.py).

    python3 check.py --rules games/<slug> <id>    the piece's rule list, from its Does: block (rules.py)
    python3 check.py --rules games/<slug> plan    the rules whose `when` is "the plan"

    python3 check.py --card games/<slug> <id>

  card       before LO's yes. A card with a Does: block: every trigger is known and written per screen, every
             screen has one, Does: and Sheet: name the same screens. An older card without Does: keeps the old
             check: the card's Craft: line cites every must-read id of every craft file it names,
             or skips one as `skip <id>: <reason>`; every named craft file exists; a card with a media spot
             names craft/media.md. Reads only; saves nothing.
  release    --release only: no dev canvas id or name is left in the merged TOML or the built HTML

    python3 check.py --beat <card or text file>

  beat       every beat marked explicit, from `[explicit]` to `[/explicit]` (or to the next blank line), has 3+
             words from v2's frozen EXPLICIT list (author-game-v2/scripts/gates.py:311-315, imported, never
             copied), and its last sentence has at least one (the pivot, C249). Reads only; saves nothing.
             A file with no marked beat is INCOMPLETE, never GREEN. The 7.5% game-wide floor (C255) waits.

Output: one verdict line (GREEN, RED <n>, or INCOMPLETE: <reason>), then every red, with NEW on the ones
that weren't red last run, then what was fixed since last run. It never says GREEN when a check was skipped.
Exit 0 green, 1 red, 2 incomplete. The last run is kept in games/<slug>/.check_last.json (git-ignored).
"""
import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]  # scripts -> author-game-lean -> skills -> .claude -> repo
MERGE = REPO / "scripts" / "merge_toml_phases.py"
MERGED = "7_final_game.toml"
DEV_PHASE = "6_dev_shortcuts.toml"  # scripts/merge_toml_phases.py:62
LAST = ".check_last.json"

sys.path.insert(0, str(HERE))
import approve  # noqa: E402
import reach  # noqa: E402
import scenes  # noqa: E402
import sheet  # noqa: E402
import rules  # noqa: E402
import pages  # noqa: E402
import people  # noqa: E402

GREEN, RED, INCOMPLETE = "green", "red", "incomplete"
# Every check a craft row's `judge` may name (SKILL.md, "Rule labels").
CHECKS = ("merge", "reach", "approvals", "builds", "release", "card", "beat", "sheet", "does",
          "talk", "length", "presence", "creation", "saves", "speakers", "goals", "pages", "people")
GATES = REPO / ".claude" / "skills" / "author-game-v2" / "scripts" / "gates.py"
BEAT_FLOOR = 3  # C254: an explicit beat has 3+ frozen-list words


# ── inputs ────────────────────────────────────────────────────────────────────────────────────────────────

def merge(game_dir, release=False):
    """Run the repo's merge script. Returns (status, rows)."""
    if not MERGE.is_file():
        return INCOMPLETE, [f"merge script not found at {MERGE}"]
    cmd = [sys.executable, str(MERGE), str(game_dir), "--validate"] + (["--no-dev"] if release else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        last = (p.stderr.strip() or p.stdout.strip() or f"exit {p.returncode}").splitlines()[-1]
        return RED, [f"merge failed: {last}"]
    return GREEN, []


def load_merged(game_dir):
    path = Path(game_dir) / "toml_phases" / MERGED
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def dev_canvases(game_dir):
    """{id: name} for the canvases in 6_dev_shortcuts.toml, or None when there is no such file."""
    path = Path(game_dir) / "toml_phases" / DEV_PHASE
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return {}
    return {c["id"]: c.get("name", "") for c in data.get("canvases", []) if c.get("id")}


def state_pieces(game_dir):
    """Rows of STATE.md's piece table as dicts, or None when there is no STATE.md or no table."""
    path = Path(game_dir) / "STATE.md"
    if not path.is_file():
        return None
    head, rows = None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            if head is not None and rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            if cells and cells[0] == "piece":
                head = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(head, cells))
        if row.get("piece") and not row["piece"].startswith("<"):
            rows.append(row)
    return rows if head is not None else None


def filled(cell):
    return bool(cell) and not cell.startswith("<")


def card_builds(game_dir):
    """{card id: set of canvas ids} from every card's Builds: line."""
    out = {}
    for path in sorted((Path(game_dir) / "cards").glob("*.md")):
        m = re.search(r"^Builds:\s*(.*)$", path.read_text(encoding="utf-8"), re.M)
        ids = {x.strip(" `") for x in (m.group(1).split(",") if m else [])}
        out[path.stem] = {x for x in ids if x and x.lower() != "none" and not x.startswith("<")}
    return out


# ── checks ────────────────────────────────────────────────────────────────────────────────────────────────

def check_reach(game):
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    rows = reach.rows(reach.check(game))
    return (RED, rows) if rows else (GREEN, [])


def check_approvals(game_dir):
    pieces = state_pieces(game_dir)
    if pieces is None:
        return INCOMPLETE, ["no STATE.md piece table"]
    rows = []
    for p in pieces:
        if filled(p.get("built", "")):
            s = approve.status(game_dir, p["piece"])
            if s != "approved":
                why = "its card changed after the yes" if s == "changed" else "no approval for its card"
                rows.append(f"piece `{p['piece']}` is built but {why}")
    return (RED, rows) if rows else (GREEN, [])


def sidebar_key(item):
    """A sidebar item has no id in the TOML; a card lists it as `sidebar:<trait>` (or `sidebar:<label>`)."""
    return "sidebar:" + str(item.get("trait") or item.get("label") or "?")


def built_things(game, dev):
    """(kind, id) for everything a card must approve: canvases (minus dev ones), places, people, sidebar items."""
    out = [("canvas", c.get("id")) for c in game.get("canvases", []) if c.get("id") not in dev]
    out += [("place", l.get("id")) for l in game.get("locations", [])]
    out += [("person", n.get("id")) for n in game.get("npcs", [])]
    out += [("sidebar item", sidebar_key(s)) for s in game.get("sidebar_items", []) if isinstance(s, dict)]
    return [(k, i) for k, i in out if i]


def check_builds(game_dir, game):
    """Every built canvas, place, person and sidebar item must be listed by an approved card.
    A changed card covers nothing."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    dev = dev_canvases(game_dir) or {}
    covered = set()
    for cid, ids in card_builds(game_dir).items():
        if approve.status(game_dir, cid) == "approved":
            covered |= ids
    rows = [f"{kind} `{i}` is built but never approved (no approved card lists it in Builds:)"
            for kind, i in built_things(game, dev) if i not in covered]
    return (RED, rows) if rows else (GREEN, [])


# ── the card check (before LO's yes) ───────────────────────────────────────────────────────────────────────

SKILL = HERE.parent


# The areas a card may name on its `Areas:` line: the craft sections of lists/COVERAGE.md, plus three
# topics that already have a craft file of their own (LO, 2026-11-22). An area's craft file is
# craft/<area, spaces as hyphens>.md unless AREA_FILES says otherwise. No file yet means no piece yet:
# piece.md step 1 writes the area's craft file first.
AREAS = ("want", "arc", "heat", "voice", "people", "places", "clock", "economy", "phone", "clothes", "media",
         "systems", "first hour", "returning player")
TOPICS = ("meters", "walk-ins", "body moments")
AREA_FILES = {"first hour": "craft/opening.md"}


def area_file(area):
    """The craft file an area or topic is written in."""
    return AREA_FILES.get(area, "craft/" + area.replace(" ", "-") + ".md")


def must_read(craft_file):
    """The ids in a craft file's `## Must read` table (first column)."""
    text = craft_file.read_text(encoding="utf-8")
    part = text.split("## Must read", 1)[-1].split("\n## ", 1)[0] if "## Must read" in text else ""
    return re.findall(r"^\| ([CL]\d+) \|", part, re.M)


def check_card(game_dir, card_id, skill=None):
    """Rows that make a card red before LO's yes. Reads only."""
    skill = Path(skill) if skill else SKILL
    path = Path(game_dir) / "cards" / f"{card_id}.md"
    if not path.is_file():
        return INCOMPLETE, [f"no card at {path}"]
    text = path.read_text(encoding="utf-8")
    rows = []
    has_screens = bool(re.search(r"^[ \t]*Screen \d", text, re.M))
    does = rules.card_does(text)
    if does is not None:
        # A card with Does: (2026-11-24 on): its rule list comes from Does:, so it has no Areas: or Craft: line and
        # no cite-every-id check; listing an id was never applying it (LO, relayed 2026-11-24: "Yes").
        rows += rules.does_problems(does, skill)
        mine = sheet.card_sheet(text)
        story = {s for s in does if not pages.is_page(s)}  # a Hints page screen has no sheet row
        if mine is not None and set(mine) != story:
            rows.append(f"Does: and Sheet: name different screens: {sorted(set(mine) ^ story)}")
        if has_screens and mine is None:
            rows.append("the card has screens and no Sheet: block (templates/piece-card.md); "
                        "write each screen's clock, place, who, wearing and flags before the prose")
        return (RED, rows) if rows else (GREEN, [])
    if has_screens:
        rows.append("the card has screens and no Does: block; name each screen's triggers (SKILL.md, Rule labels)")
        if sheet.card_sheet(text) is None:
            rows.append("the card has screens and no Sheet: block (templates/piece-card.md); "
                        "write each screen's clock, place, who, wearing and flags before the prose")
    # An older card, without Does: its Areas: and Craft: lines are checked as before.
    m = re.search(r"^Craft:[ \t]*(.*)$", text, re.M)
    line = m.group(1) if m else ""
    rows += [] if m else ["the card has no Craft: line"]
    named = re.findall(r"craft/[\w-]+\.md", line)
    media = re.search(r"^Media:\s*(\d+)", text, re.M)
    if media and int(media.group(1)) > 0 and "craft/media.md" not in named:
        rows.append(f"the card has {media.group(1)} media spot(s) and its Craft: line does not name craft/media.md")
    a = re.search(r"^Areas:[ \t]*(.*)$", text, re.M)
    areas = [x.strip().lower() for x in (a.group(1).split(",") if a else []) if x.strip()]
    if not a:
        rows.append("the card has no Areas: line")
    elif not areas:
        rows.append("the Areas: line names no area")
    for area in areas:
        if area not in AREAS + TOPICS:
            rows.append(f"Areas: `{area}` is not an area (see SKILL.md, Where things live)")
        elif not (skill / area_file(area)).is_file():
            rows.append(f"area `{area}` has no craft file yet: write {area_file(area)} first (piece.md step 1)")
        elif area_file(area) not in named:
            rows.append(f"area `{area}`: the Craft: line does not name {area_file(area)}")
    skips = dict(re.findall(r"skip ([CL]\d+):\s*([^·;]*)", line))
    for name in named:
        f = skill / name
        if not f.is_file():
            rows.append(f"the Craft: line names {name}, which does not exist")
            continue
        for i in must_read(f):
            if i in skips:
                if not skips[i].strip():
                    rows.append(f"{name}: `skip {i}` gives no reason")
            elif not re.search(rf"\b{i}\b", line):
                rows.append(f"{name}: must-read {i} is neither cited nor skipped with a reason")
    return (RED, rows) if rows else (GREEN, [])


def explicit_words():
    """v2's frozen EXPLICIT regex, loaded from gates.py so the list can never drift from the build's."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("v2_gates", GATES)
    gates = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gates)
    return gates.EXPLICIT


def marked_beats(text):
    """The beats marked explicit: `[explicit]` up to `[/explicit]`, or up to the next blank line."""
    beats = []
    for m in re.finditer(r"\[explicit\](.*?)(?:\[/explicit\]|\n[ \t>]*\n|\Z)", text, re.S | re.I):
        lines = [re.sub(r"^[ \t]*>?[ \t]*", "", l) for l in m.group(1).splitlines()]
        beats.append(" ".join(l for l in lines if l).strip())
    return beats


def last_sentence(beat):
    """The beat's last sentence, quotes and markdown stripped."""
    plain = re.sub(r"[*_\"“”]", "", beat).strip()
    parts = [s for s in re.split(r"(?<=[.!?…])\s+", plain) if s.strip()]
    return parts[-1] if parts else ""


def check_beats(path, words=None):
    """Rows that make the marked beats red. Reads only."""
    path = Path(path)
    if not path.is_file():
        return INCOMPLETE, [f"no file at {path}"]
    beats = marked_beats(path.read_text(encoding="utf-8"))
    if not beats:
        return INCOMPLETE, [f"{path.name} marks no beat with [explicit]"]
    words = words or explicit_words()
    rows = []
    for n, beat in enumerate(beats, 1):
        head = f"beat {n} (\"{beat[:40]}…\")"
        found = words.findall(beat)
        if len(found) < BEAT_FLOOR:
            rows.append(f"{head}: {len(found)} explicit word(s), needs {BEAT_FLOOR} (C254)")
        end = last_sentence(beat)
        if not words.search(end):
            rows.append(f"{head}: its last sentence has no explicit word, the pivot (C249): \"{end}\"")
    return (RED, rows) if rows else (GREEN, [])


def check_release(game_dir, game):
    """After a --no-dev merge, no dev canvas may survive in the TOML or in the built HTML."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    dev = dev_canvases(game_dir)
    if dev is None:
        return GREEN, []  # no dev file: nothing can leak from it
    rows = [f"dev canvas `{c['id']}` is in the release merge" for c in game.get("canvases", []) if c.get("id") in dev]
    html = sorted((Path(game_dir) / "output").rglob("*.html"))
    if not html:
        return (RED, rows) if rows else (INCOMPLETE, ["no built HTML in output/ to search for dev canvases"])
    for path in html:
        text = path.read_text(encoding="utf-8", errors="replace")
        for cid, name in dev.items():
            for s in filter(None, (cid, name)):
                if s in text:
                    rows.append(f"dev canvas {'id' if s == cid else 'name'} `{s}` is in {path.name}")
    return (RED, rows) if rows else (GREEN, [])


def not_built_yet(screens, game):
    """True when none of a card's Sheet:/Does: screens exist in the build. The overlap rule lets the next piece be
    carded and approved while the reader runs, so its rows describe screens that don't exist yet; it is judged from
    its first build on. (STATE.md's built date can't decide this: it is written when the piece closes, after the
    build's own check.) A card with some screens built and others missing is judged, and its missing ones are red."""
    built = {f"{c.get('id')}.{n.get('id')}" for c in game.get("canvases") or [] for n in c.get("nodes") or []}
    built |= set(pages.entries(game)) | set(pages.sidebar_entries(game)) | set(pages.people_entries(game))
    return bool(screens) and not (set(screens) & built)


def check_does(game_dir, game):
    """Each card's Does: against what the build shows. Cards without a Does: block are not judged."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    red = []
    builds = card_builds(game_dir)
    for path in sorted((Path(game_dir) / "cards").glob("*.md")):
        does = rules.card_does(path.read_text(encoding="utf-8"))
        if does is None:
            continue
        # A card that builds the Hints page names each entry it builds as a screen, so the goal-card rules reach it.
        # A person's People view fields and a sidebar item need not be named (pages.screens_for).
        red += [f"{path.stem}: {s} is built by this card and its Does: doesn't name it (a goal card is shown)"
                for s in sorted(pages.screens_for(game, builds.get(path.stem, ()), people=False)) if s not in does]
        if not not_built_yet(does, game):
            red += [f"{path.stem}: {r}" for r in rules.guard(does, game)]
    return (RED, red) if red else (GREEN, [])


def check_pages(game):
    """The Hints page's pointers and the People dialog's keys (pages.py)."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    rows = pages.problems(game)
    return (RED, rows) if rows else (GREEN, [])


def check_people(game):
    """CoT's people system, under the switch (people.py)."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    rows = people.problems(game)
    return (RED, rows) if rows else (GREEN, [])


def check_sheet(game_dir, game):
    """Each card's Sheet: against the computed one. Cards without a Sheet: block are not compared."""
    if game is None:
        return INCOMPLETE, ["the merged TOML did not parse"]
    red, inc = [], []
    for path in sorted((Path(game_dir) / "cards").glob("*.md")):
        mine, computed = sheet.for_card(game, game_dir, path.stem)
        if mine is None or not_built_yet(mine, game):
            continue
        r, i = sheet.compare(mine, computed)
        red += [f"{path.stem}: {x}" for x in r]
        inc += [f"{path.stem}: {x}" for x in i]
    if red:
        return RED, red + inc
    return (INCOMPLETE, inc) if inc else (GREEN, [])


def run_all(game_dir, release=False, against=None):
    results = {"merge": merge(game_dir, release)}
    game = load_merged(game_dir) if results["merge"][0] == GREEN else None
    results["reach"] = check_reach(game)
    results["approvals"] = check_approvals(game_dir)
    results["builds"] = check_builds(game_dir, game)
    results.update(scenes.run(game_dir, game, dev_canvases(game_dir) or {}, ref=against))
    results["sheet"] = check_sheet(game_dir, game)
    results["does"] = check_does(game_dir, game)
    results["pages"] = check_pages(game)
    results["people"] = check_people(game)
    if release:
        results["release"] = check_release(game_dir, game)
    return results


# ── report ────────────────────────────────────────────────────────────────────────────────────────────────

def report(results, last):
    """Lines to print and the exit code. Every red is printed; NEW marks reds absent last run."""
    reds = [(k, r) for k, (s, rows) in results.items() if s == RED for r in rows]
    incomplete = [(k, r) for k, (s, rows) in results.items() if s == INCOMPLETE for r in rows]
    last_reds = {(k, r) for k, v in last.items() if v[0] == RED for r in v[1]}
    last_inc = {k for k, v in last.items() if v[0] == INCOMPLETE}
    if reds:
        head = f"RED {len(reds)}" + (f" · INCOMPLETE: {'; '.join(r for _, r in incomplete)}" if incomplete else "")
        code = 1
    elif incomplete:
        head, code = f"INCOMPLETE: {'; '.join(f'{k}: {r}' for k, r in incomplete)}", 2
    else:
        head, code = "GREEN", 0
    lines = [head]
    lines += [f"  {'NEW ' if (k, r) not in last_reds else ''}RED [{k}] {r}" for k, r in reds]
    now_reds = set(reds)
    lines += [f"  FIXED [{k}] {r}" for k, r in sorted(last_reds - now_reds)]
    lines += [f"  NOW INCOMPLETE [{k}] {r}" for k, r in incomplete if k not in last_inc]
    lines += [f"  CHECKED AGAIN [{k}]" for k in sorted(last_inc) if k in results and results[k][0] != INCOMPLETE]
    changed = [l for l in lines[1:] if l.lstrip().startswith(("NEW", "FIXED", "NOW INCOMPLETE", "CHECKED AGAIN"))]
    if last and not changed:
        lines.append("  no change since last run")
    return lines, code


def card_main(argv):
    ap = argparse.ArgumentParser(description="Check one card before LO's yes.")
    ap.add_argument("game_dir")
    ap.add_argument("card_id")
    args = ap.parse_args(argv)
    status, rows = check_card(args.game_dir, args.card_id)
    print({GREEN: "GREEN", RED: f"RED {len(rows)}", INCOMPLETE: "INCOMPLETE"}[status])
    print("\n".join(f"  {r}" for r in rows))
    return {GREEN: 0, RED: 1, INCOMPLETE: 2}[status]


def rules_main(argv):
    ap = argparse.ArgumentParser(description="Print a piece's rule list, or the plan's.")
    ap.add_argument("game_dir")
    ap.add_argument("card_id")
    args = ap.parse_args(argv)
    rows = rules.table()
    if args.card_id == "plan":
        ids = rules.plan_rows()
        print(f"the plan: {len(ids)} rules")
        print("\n".join(rules.print_list(ids, rows)))
        return 0
    path = Path(args.game_dir) / "cards" / f"{args.card_id}.md"
    does = rules.card_does(path.read_text(encoding="utf-8")) if path.is_file() else None
    if does is None:
        print(f"INCOMPLETE: {path} has no Does: block")
        return 2
    lst = rules.rule_list(does, rows=rows)
    print(f"{args.card_id}: {len(lst)} rules over {len(does)} screen(s), {sum(len(v) for v in lst.values())} rule-screen pairs")
    print("\n".join(rules.print_list(lst, rows, lst)))
    return 0


def beat_main(argv):
    ap = argparse.ArgumentParser(description="Check the beats a card or file marks [explicit].")
    ap.add_argument("path")
    args = ap.parse_args(argv)
    status, rows = check_beats(args.path)
    print({GREEN: "GREEN", RED: f"RED {len(rows)}", INCOMPLETE: "INCOMPLETE"}[status])
    print("\n".join(f"  {r}" for r in rows))
    return {GREEN: 0, RED: 1, INCOMPLETE: 2}[status]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--card"]:
        return card_main(argv[1:])
    if argv[:1] == ["--beat"]:
        return beat_main(argv[1:])
    if argv[:1] == ["--rules"]:
        return rules_main(argv[1:])
    ap = argparse.ArgumentParser(description="Check a game built with author-game-lean.")
    ap.add_argument("game_dir")
    ap.add_argument("--release", action="store_true")
    ap.add_argument("--against", help="git ref of the build LO played, for the saves check")
    args = ap.parse_args(argv)
    game_dir = Path(args.game_dir)
    store = game_dir / LAST
    try:
        saved = json.loads(store.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        saved = {}
    mode = "release" if args.release else "dev"
    results = run_all(game_dir, args.release, args.against)
    lines, code = report(results, {k: tuple(v) for k, v in saved.get(mode, {}).items()})
    print("\n".join(lines))
    saved[mode] = {k: [s, rows] for k, (s, rows) in results.items()}
    store.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
