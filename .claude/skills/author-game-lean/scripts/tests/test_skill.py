"""The skill's own text. Each rule is a function over a skill folder: the real skill must pass it, and a temp copy
with a planted bug must fail it, so no green here is a check that cannot go red."""
import re
import shutil
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[2]
REPO = SKILL.parents[2]
PHASES = ["SKILL.md", "plan.md", "piece.md", "build.md", "release.md"]

# Files that exist per game, not in the skill or the repo; a pointer to one of these is not checked.
PER_GAME = {"STATE.md", "NOTES.md", "approvals.json", "7_final_game.toml", "6_dev_shortcuts.toml", "output/", "output_dev/"}
# A bare `v2.py` in a cite means the engine SKILL.md rule 3 names; it is the only short name a cite may use.
ALIASES = {"v2.py": "apps/game_generation/twee_comprehensive/generators/v2.py"}
CITE = re.compile(r"([\w./-]*\.\w+):(\d+(?:[-,]\d+)*)")


def instruction_files(skill):
    return [p for p in skill.rglob("*.md") if "lists" not in p.relative_to(skill).parts]


def size_problems(skill):
    rows = []
    for p in instruction_files(skill):
        if p.name == "CHANGELOG.md":
            continue  # a diary, not an instruction file (C2170; LO, 2026-11-24)
        n = len(p.read_text(encoding="utf-8").splitlines())
        cap = 200 if p == skill / "SKILL.md" else 400
        if n >= cap:
            rows.append(f"{p.relative_to(skill)}: {n} lines (cap {cap})")
    return rows


def missing_pointers(skill, repo=REPO):
    rows = []
    for tok in re.findall(r"`([^`\s]+)`", (skill / "SKILL.md").read_text(encoding="utf-8")):
        path = tok.split(":")[0]
        if "<" in path or path.startswith("games/") or path in PER_GAME:
            continue
        if not (path.endswith("/") or re.search(r"\.\w+$", path)):
            continue  # not a file name: a flag, a phase name, a module
        if not ((skill / path).exists() or (repo / path).exists()):
            rows.append(f"SKILL.md points at `{tok}`, which does not exist")
    return rows


def bad_cites(skill, repo=REPO):
    """A `file:line` cite whose file is missing or whose line is past the end of the file.
    It does NOT catch drift: a cite that still lands inside the file but on the wrong line passes.
    Green here means every cite points somewhere real, not that it points at the right thing."""
    rows = []
    for path in id_files(skill):
        name = path.relative_to(skill)
        for f, lines in CITE.findall(path.read_text(encoding="utf-8")):
            f = ALIASES.get(f, f)
            target = next((b / f for b in (repo, skill) if (b / f).is_file()), None)
            if target is None:
                rows.append(f"{name}: cite `{f}:{lines}` names a missing file")
                continue
            last = max(int(x) for x in re.split(r"[-,]", lines))
            n = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
            if last > n:
                rows.append(f"{name}: cite `{f}:{lines}` is past the end ({n} lines)")
    return rows


def id_files(skill):
    """The phase files and every craft file: anything that cites a C- or L-id as a rule."""
    return [skill / n for n in PHASES] + sorted((skill / "craft").glob("*.md"))


def unknown_ids(skill):
    """C-ids not in lists/COVERAGE.md and L-ids not in lists/LESSONS.md, cited in a phase or craft file."""
    known = set(re.findall(r"^\| (C\d+) \|", (skill / "lists" / "COVERAGE.md").read_text(encoding="utf-8"), re.M))
    known |= set(re.findall(r"^\| (L\d+) \|", (skill / "lists" / "LESSONS.md").read_text(encoding="utf-8"), re.M))
    cited = {c for p in id_files(skill) for c in re.findall(r"\b([CL]\d{2,5})\b", p.read_text(encoding="utf-8"))}
    return sorted(cited - known)


def plain_python3(skill):
    """A runnable command on plain python3 (3.10 here, no tomllib). The CHANGELOG is history, not instructions."""
    rows = []
    for p in instruction_files(skill):
        if p.name == "CHANGELOG.md":
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"(^\s*|`)python3 ", line):
                rows.append(f"{p.relative_to(skill)}:{i}: {line.strip()[:80]}")
    return rows


# ── the real skill passes ─────────────────────────────────────────────────────────────────────────────────────

def test_sizes():
    assert size_problems(SKILL) == []


def test_pointers():
    assert missing_pointers(SKILL) == []


def test_cites():
    assert bad_cites(SKILL) == []


def test_ids():
    assert unknown_ids(SKILL) == []


def test_no_plain_python3():
    assert plain_python3(SKILL) == []


# ── planted bugs fail ─────────────────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def copy(tmp_path):
    dst = tmp_path / "skill"
    shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return dst


def append(path, text):
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def test_planted_long_front_door(copy):
    lines = (copy / "SKILL.md").read_text().splitlines()
    (copy / "SKILL.md").write_text("\n".join(lines + ["x"] * (200 - len(lines))) + "\n")
    assert size_problems(copy) == ["SKILL.md: 200 lines (cap 200)"]


def test_planted_long_instruction_file_and_lists_do_not_count(copy):
    (copy / "plan.md").write_text("x\n" * 400)
    (copy / "lists" / "BIG.md").write_text("x\n" * 2000)
    (copy / "CHANGELOG.md").write_text("x\n" * 2000)
    assert size_problems(copy) == ["plan.md: 400 lines (cap 400)"]


def test_planted_missing_pointer(copy):
    append(copy / "SKILL.md", "\nSee `templates/gone.md`.\n")
    assert missing_pointers(copy) == ["SKILL.md points at `templates/gone.md`, which does not exist"]


def test_planted_cite_past_the_end(copy):
    append(copy / "build.md", "\nSee `scripts/merge_toml_phases.py:9999`.\n")
    assert len(bad_cites(copy)) == 1 and "past the end" in bad_cites(copy)[0]


def test_planted_cite_to_a_missing_file(copy):
    append(copy / "piece.md", "\nSee `scripts/nowhere.py:3`.\n")
    assert len(bad_cites(copy)) == 1 and "missing file" in bad_cites(copy)[0]


def test_planted_unknown_c_id(copy):
    append(copy / "plan.md", "\nAs C9999 says.\n")
    assert unknown_ids(copy) == ["C9999"]


def test_planted_unknown_l_id_in_a_craft_file(copy):
    append(copy / "craft" / "opening.md", "\nSee L9999.\n")
    assert unknown_ids(copy) == ["L9999"]


def test_planted_plain_python3(copy):
    append(copy / "release.md", "\n    python3 .claude/skills/author-game-lean/scripts/check.py games/<slug>\n")
    assert len(plain_python3(copy)) == 1


# ── piece.md points the card at the craft files (LO, 2026-11-20) ──────────────────────────────────────────────

def piece_misses_craft(skill):
    """piece.md must send the card to craft/, and every craft file it names must exist."""
    text = (skill / "piece.md").read_text(encoding="utf-8")
    rows = [] if "craft/" in text else ["piece.md does not name craft/"]
    rows += [f"piece.md names `{m}`, which does not exist" for m in re.findall(r"`(craft/[\w-]+\.md)`", text)
             if not (skill / m).is_file()]
    return rows


def test_piece_names_craft():
    assert piece_misses_craft(SKILL) == []


def test_planted_piece_without_craft(copy):
    p = copy / "piece.md"
    p.write_text(p.read_text().replace("craft/", "notes/"))
    assert piece_misses_craft(copy) == ["piece.md does not name craft/"]


def test_planted_piece_names_a_missing_craft_file(copy):
    append(copy / "piece.md", "\nAlso read `craft/phone.md`.\n")
    assert piece_misses_craft(copy) == ["piece.md names `craft/phone.md`, which does not exist"]


# ── the reader is in the loop (LO, 2026-11-20) ──────────────────────────────────────────────────────────────

def reader_missing(skill):
    """SKILL.md's loop, build.md and release.md all name reader.md, and the file exists."""
    rows = [] if (skill / "reader.md").is_file() else ["reader.md does not exist"]
    loop = (skill / "SKILL.md").read_text(encoding="utf-8").split("## The loop", 1)[-1].split("## Always", 1)[0]
    rows += [] if "`reader.md`" in loop else ["SKILL.md's loop does not name reader.md"]
    rows += [f"{n} does not name reader.md" for n in ("build.md", "release.md")
             if "`reader.md`" not in (skill / n).read_text(encoding="utf-8")]
    return rows


def test_reader_in_the_loop():
    assert reader_missing(SKILL) == []


def test_planted_loop_without_reader(copy):
    p = copy / "SKILL.md"
    p.write_text(p.read_text().replace("**Read** (`reader.md`)", "**Read**"))
    assert reader_missing(copy) == ["SKILL.md's loop does not name reader.md"]


def test_planted_reader_file_gone(copy):
    (copy / "reader.md").unlink()
    assert "reader.md does not exist" in reader_missing(copy)


def piece_misses_card_check(skill):
    """change 6 (2026-11-20): piece.md runs `check.py --card` and no longer checks by hand."""
    text = (skill / "piece.md").read_text(encoding="utf-8")
    rows = [] if "check.py --card" in text else ["piece.md does not run check.py --card"]
    rows += ["piece.md still checks the card by hand"] if "check by hand" in text else []
    return rows


def test_piece_names_the_card_check():
    assert piece_misses_card_check(SKILL) == []


def test_planted_piece_back_to_hand_check(copy):
    p = copy / "piece.md"
    p.write_text(p.read_text().replace("check.py --card", "check by hand"))
    assert piece_misses_card_check(copy) == ["piece.md does not run check.py --card",
                                             "piece.md still checks the card by hand"]


# ── SKILL.md's area table matches check.py's list (LO, 2026-11-22) ───────────────────────────────────────────

def area_table_misses(skill):
    """Every area and topic check.py accepts is named in SKILL.md, and every file the table names exists."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("lean_check", skill / "scripts" / "check.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    table = text.split("**Areas.**", 1)[-1] if "**Areas.**" in text else ""
    rows = [f"SKILL.md's area table does not name `{a}`" for a in mod.AREAS + mod.TOPICS if a not in table]
    rows += [f"SKILL.md's area table names `{f}`, which does not exist"
             for f in re.findall(r"`(craft/[\w-]+\.md)`", table) if not (skill / f).is_file()]
    return rows


def test_area_table_matches_check():
    assert area_table_misses(SKILL) == []


def test_planted_area_missing_from_the_table(copy):
    p = copy / "SKILL.md"
    text = p.read_text()  # drop the area wherever it sits: its own row, or inside the no-file row
    text = re.sub(r"^\| economy \|.*\n", "", text, flags=re.M).replace("economy, ", "")
    p.write_text(text)
    assert area_table_misses(copy) == ["SKILL.md's area table does not name `economy`"]


# ── rule labels (the rule pipeline, Part A + F, LO 2026-11-24) ──────────────────────────────────────────────

# The craft files labelled so far; the rest are labelled one area at a time, and each is added here.
LABELLED = sorted(f"craft/{p.name}" for p in (SKILL / "craft").glob("*.md"))
# Ids shared with another file whose one home LO hasn't chosen yet (shown to LO 2026-11-24). Remove each as he answers.
PENDING_HOMES = set()


def triggers(skill):
    part = (skill / "SKILL.md").read_text(encoding="utf-8").split("## Rule labels", 1)[-1].split("\n## ", 1)[0]
    return set(re.findall(r"^\| ([a-z][^|]*?) \| ", part, re.M)) - {"when"}


def check_names():
    sys.path.insert(0, str(SKILL / "scripts"))
    import check
    return set(check.CHECKS)


def must_rows(path):
    """[(id, cells)] of a craft file's must-read table."""
    text = path.read_text(encoding="utf-8")
    part = text.split("## Must read", 1)[-1].split("\n## ", 1)[0] if "## Must read" in text else ""
    return [(m.group(1), [c.strip() for c in m.group(0).strip().strip("|").split("|")])
            for m in re.finditer(r"^\| ([CL]\d+) \|.*$", part, re.M)]


def label_problems(skill, labelled=None):
    rows, when_ok, checks = [], triggers(skill), check_names()
    for name in labelled or LABELLED:
        for rid, cells in must_rows(skill / name):
            if len(cells) != 5:
                rows.append(f"{name} {rid}: {len(cells)} columns, needs id | asks | failure | when | judge")
                continue
            _, asks, failure, when, judge = cells
            if asks.startswith("see "):
                continue  # a pointer to the row's home
            bad = [w.strip() for w in when.split(",") if w.strip() not in when_ok]
            if bad or not when.strip():
                rows.append(f"{name} {rid}: `when` {bad or when!r} is not in SKILL.md's Rule labels")
            kind, _, named = judge.partition("+")
            kind = kind.strip()
            if kind not in ("script", "reader", "note"):
                rows.append(f"{name} {rid}: judge `{judge}` is not script, reader or note")
            names = [x.strip() for x in named.split(",") if x.strip()]
            if kind == "script" and not names:
                rows.append(f"{name} {rid}: a script row names its check")
            rows += [f"{name} {rid}: judge names `{x}`, which is not in check.py's CHECKS" for x in names
                     if x not in checks]
            if kind in ("script", "reader") and failure in ("", "—", "-"):
                rows.append(f"{name} {rid}: a {kind} row needs a real failure, or says why it stays blocking")
    return rows


def home_problems(skill, labelled=None, pending=PENDING_HOMES):
    """An id's row text lives in one craft file; every other file's row points there ("see craft/x.md")."""
    labelled = set(labelled or LABELLED)
    homes = {}
    for path in sorted((skill / "craft").glob("*.md")):
        for rid, cells in must_rows(path):
            if not (len(cells) > 1 and cells[1].startswith("see ")):
                homes.setdefault(rid, []).append(f"craft/{path.name}")
    return [f"{rid}: row text in {', '.join(files)}; keep it in one and point from the rest"
            for rid, files in sorted(homes.items())
            if len(files) > 1 and rid not in pending and labelled & set(files)]


def test_labels():
    assert label_problems(SKILL) == []


def test_one_home():
    assert home_problems(SKILL) == []


def test_checks_names_every_check():
    sys.path.insert(0, str(SKILL / "scripts"))
    import check
    import scenes
    assert {"talk", "length", "presence", "creation", "saves", "speakers", "goals", "sheet"} <= set(check.CHECKS)
    assert set(scenes.run(None, None)) <= set(check.CHECKS)


def test_planted_unknown_when_is_red(copy):
    p = copy / "craft" / "voice.md"
    p.write_text(p.read_text().replace("| C442 | say it, don't hint it: tell the player what is happening | — · kept "
                                       "blocking: the voice, LO's (2026-11-22) | always |", "| C442 | say it, don't "
                                       "hint it: tell the player what is happening | — · kept blocking: the voice, "
                                       "LO's (2026-11-22) | sometimes |"))
    assert any("C442" in r and "when" in r for r in label_problems(copy))


def test_planted_reader_row_with_no_failure_is_red(copy):
    p = copy / "craft" / "voice.md"
    p.write_text(p.read_text().replace("| — · kept blocking: the voice, LO's (2026-11-22) | always | reader |",
                                       "| — | always | reader |", 1))
    assert any("real failure" in r for r in label_problems(copy))


def test_planted_script_row_naming_no_check_is_red(copy):
    p = copy / "craft" / "voice.md"
    p.write_text(p.read_text().replace("| always | reader + presence, sheet, creation |", "| always | script |"))
    assert any("names its check" in r for r in label_problems(copy))
    p.write_text(p.read_text().replace("| always | script |", "| always | script + vibes |"))
    assert any("`vibes`" in r for r in label_problems(copy))


def test_planted_second_copy_of_a_row_is_red(copy):
    p = copy / "craft" / "people.md"
    t = p.read_text()
    p.write_text(t.replace("| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — |",
                           "| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — |\n| C442 | say it | — |"))
    assert home_problems(copy) == ["C442: row text in craft/people.md, craft/voice.md; keep it in one and point "
                                   "from the rest"]


def test_a_pointer_is_not_a_second_copy(copy):
    p = copy / "craft" / "people.md"
    p.write_text(p.read_text().replace("| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — |",
                                       "| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — |\n"
                                       "| C442 | see `craft/voice.md` | | | |"))
    assert home_problems(copy) == []


def test_an_unlabelled_file_is_not_judged(copy):
    assert label_problems(copy, ["craft/voice.md"]) == []
    (copy / "craft" / "new-area.md").write_text("## Must read\n\n| id | what it asks | the failure it stops |\n|---|---|---|\n| C442 | x | — |\n")
    assert label_problems(copy, ["craft/new-area.md"])  # an unlabelled file is red once it's listed
