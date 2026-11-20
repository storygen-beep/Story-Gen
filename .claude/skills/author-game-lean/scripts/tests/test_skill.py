"""The skill's own text. Each rule is a function over a skill folder: the real skill must pass it, and a temp copy
with a planted bug must fail it, so no green here is a check that cannot go red."""
import re
import shutil
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[2]
REPO = SKILL.parents[2]
PHASES = ["SKILL.md", "plan.md", "piece.md", "build.md", "release.md"]

# Files that exist per game, not in the skill or the repo; a pointer to one of these is not checked.
PER_GAME = {"STATE.md", "NOTES.md", "approvals.json", "7_final_game.toml", "6_dev_shortcuts.toml", "output/", "output_dev/"}
CITE = re.compile(r"([\w./-]*\.\w+):(\d+(?:[-,]\d+)*)")


def instruction_files(skill):
    return [p for p in skill.rglob("*.md") if "lists" not in p.relative_to(skill).parts]


def size_problems(skill):
    rows = []
    for p in instruction_files(skill):
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
    for name in PHASES:
        for f, lines in CITE.findall((skill / name).read_text(encoding="utf-8")):
            target = next((b / f for b in (repo, skill) if (b / f).is_file()), None)
            if target is None:
                rows.append(f"{name}: cite `{f}:{lines}` names a missing file")
                continue
            last = max(int(x) for x in re.split(r"[-,]", lines))
            n = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
            if last > n:
                rows.append(f"{name}: cite `{f}:{lines}` is past the end ({n} lines)")
    return rows


def unknown_c_ids(skill):
    known = set(re.findall(r"^\| (C\d+) \|", (skill / "lists" / "COVERAGE.md").read_text(encoding="utf-8"), re.M))
    cited = {c for name in PHASES for c in re.findall(r"\b(C\d{3,5})\b", (skill / name).read_text(encoding="utf-8"))}
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


def test_c_ids():
    assert unknown_c_ids(SKILL) == []


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
    assert unknown_c_ids(copy) == ["C9999"]


def test_planted_plain_python3(copy):
    append(copy / "release.md", "\n    python3 .claude/skills/author-game-lean/scripts/check.py games/<slug>\n")
    assert len(plain_python3(copy)) == 1
