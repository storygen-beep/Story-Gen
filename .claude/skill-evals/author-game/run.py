"""Run the author-game exam against one skill.

Each trial gets a fresh staging directory outside the repo: the pinned fixture game, the skill
under test (plus author-game-v2, whose references and gates the lean version reads), the v2
agents, the merge script and the project CLAUDE.md. A headless `claude -p` session does the
case's task there. The result is merged, scored with gates.py, and graded on the diff from the
fixture's own baseline plus the case's check.py.

Usage (repo root):
    venv/bin/python .claude/skill-evals/author-game/run.py --skill author-game-v2 --case 01_* --trials 1
    venv/bin/python .claude/skill-evals/author-game/run.py --dry-run --case 03_*
"""
from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL_DIR))
import lib  # noqa: E402

REPO = lib.REPO
CASE_DIRS = (EVAL_DIR / "cases", EVAL_DIR / "cases_holdout")
CASE_SETS = ("main", "holdout", "quick", "release", "build", "design")
QUICK = EVAL_DIR / "quick.json"           # the cases that separate v2 from lean, plus the held-out set
REFERENCE = EVAL_DIR / "reference.json"   # v2's frozen per-case results; v2 is not re-run by default
V2_SKILL = "author-game-v2"


def case_dir(cid: str) -> Path:
    for d in CASE_DIRS:
        if (d / cid).is_dir():
            return d / cid
    raise FileNotFoundError(f"no case {cid}")


def _kind(cid: str) -> str:
    return json.loads((case_dir(cid) / "case.json").read_text()).get("kind", "edit")


def case_ids_for(set_name: str) -> list[str]:
    """main / holdout: the edit-stage cases. release: the release-stage cases (main + held-out).
    quick: the list in quick.json."""
    if set_name == "quick":
        return list(json.loads(QUICK.read_text())["cases"])
    every = [p.name for d in CASE_DIRS for p in sorted(d.iterdir()) if p.is_dir()]
    if set_name in ("release", "build", "design"):
        return [c for c in every if _kind(c) == set_name]
    root = CASE_DIRS[0] if set_name == "main" else CASE_DIRS[1]
    return sorted(p.name for p in root.iterdir() if p.is_dir() and _kind(p.name) == "edit")
FIXTURES = {k: v for k, v in json.loads((EVAL_DIR / "fixtures.json").read_text()).items() if k != "note"}
DEFAULT_FIXTURE = "billable_hours"
# Per fixture, re-measured at the start of every run with the pinned tools (measure_baseline):
# {"gates": gates.py --json, "ship": --ship BLOCK rows (build stubbed), "game": the merged TOML}.
# Always the INTACT fixture, before any case's `prepare` step.
BASELINES: dict[str, dict] = {}


def fixture_of(case: dict) -> str:
    return case.get("fixture", DEFAULT_FIXTURE)


def slug_of(fixture: str) -> str:
    """The game folder name a fixture stages as (a local copy may stage under its real slug)."""
    return FIXTURES[fixture].get("slug", fixture)


def has_toml(fixture: str) -> bool:
    return not (FIXTURES[fixture].get("empty") or FIXTURES[fixture].get("dir"))

# For cases whose right answer may be to stop and ask: no claim that LO approved anything.
PLAIN_PREAMBLE = (
    "Game: games/{game}. Do not build the game, commit, or touch media. When you are done, say in two "
    "lines what you changed, or why you stopped.\n\nTask: {task}"
)
PREAMBLE = (
    "Game: games/{game}. LO has already approved this step. Author it directly in the game's "
    "toml_phases files: do not pitch options, do not ask questions, and do not stop at a phase "
    "boundary. Do not build the game, commit, or touch media. When you are done, say in two lines "
    "what you changed.\n\nTask: {task}"
)

ALLOWED_TOOLS = ("Read Edit Write Glob Grep Skill Agent TodoWrite Bash(python3 *) "
                 "Bash(grep *) Bash(ls *) Bash(wc *) Bash(head *) Bash(cat *)")
V2 = "author-game-v2"


# ── staging ──────────────────────────────────────────────────────────────────

def _extract(ref: str, paths: list[str], root: Path) -> None:
    archive = subprocess.run(["git", "-C", str(REPO), "archive", ref, *paths], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(root)], input=archive.stdout, check=True)


def stage(skill: str, root: Path, args, fixture: str = DEFAULT_FIXTURE, prepare: list | None = None) -> Path:
    """v2 and its agents come from a pinned commit (--v2-ref), so edits other sessions leave in the
    working tree cannot shift the baseline. A skill other than v2 comes from the working tree unless
    --skill-ref pins it too."""
    root.mkdir(parents=True)
    fx = FIXTURES[fixture]
    if fx.get("empty"):
        (root / "games" / slug_of(fixture)).mkdir(parents=True)
    elif fx.get("dir"):
        shutil.copytree(EVAL_DIR / fx["dir"], root / "games" / slug_of(fixture))
    else:
        _extract(fx["commit"], fx["paths"], root)
    _extract(args.v2_ref, [f".claude/skills/{V2}", ".claude/agents"], root)
    for extra in (root / ".claude/agents").glob("*.md"):
        if not extra.name.startswith("v2-"):
            extra.unlink()
    if skill != V2:
        if args.skill_ref:
            _extract(args.skill_ref, [f".claude/skills/{skill}"], root)
        else:
            shutil.copytree(REPO / ".claude/skills" / skill, root / ".claude/skills" / skill)
    _extract(args.v2_ref, ["scripts/merge_toml_phases.py", "CLAUDE.md"], root)
    if prepare:
        lib.prepare_fixture(root / "games" / fixture, prepare)
        lib.merge(root / "games" / fixture, root / "scripts/merge_toml_phases.py")

    # A git repo inside staging records exactly what the session changed.
    for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.name=exam", "-c", "user.email=exam@local",
                                                 "commit", "-qm", "fixture"]):
        subprocess.run(["git", "-C", str(root), *cmd], check=True)
    return root


# A full scoreboard run on the game: `python3 …gates.py <slug|…7_final_game.toml>`, with no
# single-file mode. A grep of gates.py, `--help` or `--beat` on loose prose does not count.
_GATES_RUN = re.compile(r"python3?\S*\s+\S*gates\.py\s+(?!-)\S+")
_NOT_A_RUN = re.compile(r"--(beat|help|words|selfcheck)\b")


# The lean skill's edit_check.py runs the same scoreboard; its plain (non --start) run counts.
_CHECK_RUN = re.compile(r"edit_check\.py\s+\S+")


def ran_full_gates(commands: list[str]) -> bool:
    return any((_GATES_RUN.search(c) and not _NOT_A_RUN.search(c))
               or (_CHECK_RUN.search(c) and "--start" not in c.split("edit_check.py", 1)[1].split(";")[0].split("&&")[0])
               for c in commands)


# ── one trial ────────────────────────────────────────────────────────────────

def claude_cmd(skill: str, prompt: str, args) -> list[str]:
    cmd = ["claude", "-p", "--setting-sources", "project", "--strict-mcp-config",
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(args.max_turns), "--max-budget-usd", str(args.max_budget_usd),
           "--permission-mode", "acceptEdits", "--permission-prompts", "none",
           "--allowedTools", ALLOWED_TOOLS, "--no-session-persistence"]
    if args.model:
        cmd += ["--model", args.model]
    return cmd + [f"/{skill} {prompt}"]


def parse_stream(lines: list[str]) -> dict:
    info = {"init": None, "result": None, "bash": [], "skills_called": [], "rate": None}
    for line in lines:
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            info["init"] = {k: ev.get(k) for k in ("model", "skills", "agents", "plugins", "tools",
                                                    "slash_commands", "cwd", "permissionMode")}
        elif ev.get("type") == "rate_limit_event":
            info["rate"] = ev.get("rate_limit_info")
        elif ev.get("type") == "result":
            info["result"] = {k: ev.get(k) for k in ("subtype", "is_error", "num_turns", "total_cost_usd",
                                                      "duration_ms", "permission_denials", "result")}
        elif ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") != "tool_use":
                    continue
                if block.get("name") == "Bash":
                    info["bash"].append(block.get("input", {}).get("command", ""))
                if block.get("name") == "Skill":
                    info["skills_called"].append(block.get("input", {}))
    return info


def pinned_tools(staging: Path) -> tuple[Path, Path]:
    """The grader and merge script come from the staged, pinned commit, not the live working tree."""
    return (staging / f".claude/skills/{V2}/scripts/gates.py", staging / "scripts/merge_toml_phases.py")


def measure_baseline(args, fixture: str = DEFAULT_FIXTURE, prepare: list | None = None, key: str | None = None) -> dict:
    """Gates, --ship rows and the merged TOML of the INTACT fixture (or a prepared copy, under `key`),
    at the run's pinned commit."""
    root = Path(tempfile.mkdtemp(prefix="exam_baseline_")) / "w"
    staging = stage(V2, root, args, fixture, prepare)
    gates_py, merge_py = pinned_tools(staging)
    game_dir = staging / "games" / fixture
    if lib.merge(game_dir, merge_py).returncode != 0:
        sys.exit(f"fixture {fixture} does not merge with the pinned merge script")
    key = key or fixture
    BASELINES[key] = {"gates": lib.run_gates(lib.final_toml(game_dir), gates_py),
                      "ship": lib.ship_block_rows(staging, fixture),
                      "game": lib.load_game(lib.final_toml(game_dir))}
    shutil.rmtree(root.parent, ignore_errors=True)
    return BASELINES[key]["gates"]


def baseline_for(case: dict, args) -> dict:
    """The intact fixture's baseline, or, for a case whose right answer is to leave the prepared copy
    alone ("baseline": "prepared"), the baseline of that prepared copy."""
    fixture = fixture_of(case)
    if case.get("baseline") != "prepared":
        return BASELINES[fixture]
    key = f"{fixture}:{case['id']}"
    if key not in BASELINES:
        measure_baseline(args, fixture, case.get("prepare"), key)
    return BASELINES[key]


def grade_design(case: dict, staging: Path, out: Path) -> dict:
    game_dir = staging / "games" / slug_of(fixture_of(case))
    files = {p.relative_to(game_dir).as_posix(): p.read_text(errors="replace")
             for p in sorted(game_dir.rglob("*")) if p.is_file() and p.suffix in (".md", ".json", ".toml")}
    ledger = json.loads(files["v2_state.json"]) if "v2_state.json" in files else {}
    (out / "design_files.json").write_text(json.dumps(sorted(files), indent=1))
    spec = importlib.util.spec_from_file_location("case_check", case_dir(case["id"]) / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    final = ""
    transcript = out / "transcript.jsonl"
    if transcript.exists():
        for line in transcript.read_text().splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "result":
                final = str(ev.get("result") or "")
    fails = mod.check(files, ledger, final) if mod.check.__code__.co_argcount >= 3 else mod.check(files, ledger)
    return {"passed": not fails, "fails": fails}


def grade(case: dict, staging: Path, out: Path, args=None) -> dict:
    if case.get("kind") == "design":
        return grade_design(case, staging, out)
    fixture = fixture_of(case)
    base = baseline_for(case, args) if args else BASELINES[fixture]
    game_dir = staging / "games" / fixture
    gates_py, merge_py = pinned_tools(staging)
    fails: list[str] = []
    merged = lib.merge(game_dir, merge_py)
    (out / "merge.log").write_text(merged.stdout + merged.stderr)
    if merged.returncode != 0:
        return {"passed": False, "fails": [f"merge failed: {merged.stderr.strip()[-400:]}"]}
    toml_path = lib.final_toml(game_dir)
    try:
        game = lib.load_game(toml_path)
    except Exception as exc:  # an invalid TOML is a failed trial, not a runner crash
        return {"passed": False, "fails": [f"merged TOML does not parse: {exc}"]}
    gates = lib.run_gates(toml_path, gates_py)
    (out / "gates.json").write_text(json.dumps(gates, indent=1))

    fails += lib.gate_regressions(gates, base["gates"])
    fails += lib.new_lint_findings(gates, base["gates"], case.get("target_lints", []))
    if case.get("kind") == "release":
        after_ship = lib.ship_block_rows(staging, fixture)
        (out / "ship_rows.json").write_text(json.dumps(after_ship, indent=1))
        fails += lib.ship_regressions(after_ship, base["ship"])
    spec = importlib.util.spec_from_file_location("case_check", case_dir(case["id"]) / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # A check may take the game's ledger (v2_state.json) as a third argument, for rules the
    # TOML cannot show, such as where a character sleeps (`board.map.homes`).
    ledger_path = game_dir / "v2_state.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if mod.check.__code__.co_argcount >= 3:
        fails += mod.check(game, base["game"], ledger)
    else:
        fails += mod.check(game, base["game"])
    return {"passed": not fails, "fails": fails, "tally": gates["tally"]}


def run_trial(case: dict, skill: str, args, out: Path) -> dict:
    out.mkdir(parents=True)
    staging = stage(skill, Path(tempfile.mkdtemp(prefix=f"exam_{case['id']}_")) / "w", args,
                    fixture_of(case), case.get("prepare"))
    template = PLAIN_PREAMBLE if case.get("preamble") == "plain" else PREAMBLE
    prompt = template.format(game=slug_of(fixture_of(case)), task=case["task"])
    cmd = claude_cmd(skill, prompt, args)
    (out / "command.json").write_text(json.dumps({"cwd": str(staging), "cmd": cmd}, indent=1))
    if args.dry_run:
        if not args.keep:
            shutil.rmtree(staging.parent, ignore_errors=True)
        return {"case": case["id"], "dry_run": True, "staging": str(staging)}

    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=staging, capture_output=True, text=True, timeout=args.timeout)
        stdout, stderr = proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or ""
        stdout = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
        stderr = f"TIMEOUT after {args.timeout}s"
    (out / "transcript.jsonl").write_text(stdout)
    (out / "stderr.txt").write_text(stderr or "")
    session = parse_stream(stdout.splitlines())

    diff = subprocess.run(["git", "-C", str(staging), "status", "--porcelain"], capture_output=True, text=True).stdout
    subprocess.run(["git", "-C", str(staging), "add", "-A"], check=True)
    patch = subprocess.run(["git", "-C", str(staging), "diff", "--cached", "--binary"], capture_output=True, text=True).stdout
    (out / "changes.txt").write_text(diff)
    (out / "diff.patch").write_text(patch)

    res = session["result"] or {}
    # A session that never reached Claude (network, DNS, outage) is an infrastructure error,
    # not a failed authoring attempt: it is excluded from the score and must be re-run.
    text = str(res.get("result") or "")
    rate_cut = bool(res.get("is_error")) and (session["rate"] or {}).get("status") not in (None, "allowed")
    infra = ("API Error" in text or "hit your session limit" in text or rate_cut
             or (bool(res.get("is_error")) and (res.get("num_turns") or 0) <= 1 and not res.get("total_cost_usd"))
             or not session["result"])
    result = {"passed": None, "fails": [f"infrastructure error: {str(res.get('result'))[:160]}"]} if infra \
        else grade(case, staging, out, args)
    record = {
        "case": case["id"], "skill": skill, "passed": result["passed"], "fails": result["fails"], "infra_error": infra,
        "cost_usd": res.get("total_cost_usd"), "turns": res.get("num_turns"), "subtype": res.get("subtype"),
        "wall_s": round(time.time() - started, 1), "ran_gates": ran_full_gates(session["bash"]),
        "skills_called": session["skills_called"], "permission_denials": res.get("permission_denials"),
        "changed_files": diff.splitlines(), "init": session["init"], "staging": str(staging),
        "rate": session["rate"],
    }
    (out / "grade.json").write_text(json.dumps(record, indent=1))
    if not args.keep:
        shutil.rmtree(staging.parent, ignore_errors=True)
    return record


def regrade(run_dir: Path, args) -> int:
    """Re-grade a finished run from its saved diffs with the current graders. No session is re-run."""
    for fx in FIXTURES:
        if has_toml(fx):
            measure_baseline(args, fx)
    records = []
    for grade_file in sorted(run_dir.glob("*/trial*/grade.json")):
        out = grade_file.parent
        rec = json.loads(grade_file.read_text())
        case = json.loads((case_dir(rec["case"]) / "case.json").read_text())
        staging = stage(V2, Path(tempfile.mkdtemp(prefix="exam_regrade_")) / "w", args,
                        fixture_of(case), case.get("prepare"))
        subprocess.run(["git", "-C", str(staging), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(staging), "-c", "user.name=exam", "-c", "user.email=exam@local",
                        "commit", "-qm", "prepared", "--allow-empty"], check=True)
        patch = out / "diff.patch"
        if patch.read_text().strip():
            subprocess.run(["git", "-C", str(staging), "apply", "--whitespace=nowarn", str(patch.resolve())], check=True)
        result = grade(case, staging, out, args)
        if rec.get("passed") != result["passed"]:
            print(f"changed  {rec['case']} {out.name}: {rec.get('passed')} -> {result['passed']}")
        rec["passed"], rec["fails"], rec["regraded"] = result["passed"], result["fails"], True
        transcript = out / "transcript.jsonl"
        if transcript.exists():
            rec["ran_gates"] = ran_full_gates(parse_stream(transcript.read_text().splitlines())["bash"])
        grade_file.write_text(json.dumps(rec, indent=1))
        shutil.rmtree(staging.parent, ignore_errors=True)
        records.append(rec)
        mark = "PASS" if rec["passed"] else "FAIL"
        print(f"{mark}  {rec['case']} {out.name}")
        for f in rec["fails"][:5]:
            print(f"      - {f}")
    args.skill = records[0]["skill"] if records else args.skill
    summary = summarize(records, args)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: summary[k] for k in ("skill", "cases", "pass_k_cases", "trial_pass_rate",
                                                "ran_gates_trials", "total_cost_usd")}, indent=1))
    return 0


def claude_reachable() -> bool:
    """A one-turn probe. The reset time a usage limit reports has proved unreliable (the limit
    lifted hours early twice on 2026-10-02), so the runner asks instead of trusting it."""
    probe = Path(tempfile.mkdtemp(prefix="exam_probe_"))
    try:
        proc = subprocess.run(["claude", "-p", "--setting-sources", "project", "--strict-mcp-config",
                               "--output-format", "json", "--max-turns", "1", "--no-session-persistence",
                               "Reply with the word ok."], cwd=probe, capture_output=True, text=True, timeout=300)
        res = json.loads(proc.stdout or "{}")
        return not res.get("is_error") and "limit" not in str(res.get("result", "")).lower()
    except Exception:
        return False
    finally:
        shutil.rmtree(probe, ignore_errors=True)


def run_with_retry(case: dict, args, out: Path, tries: int = 4) -> dict:
    """An infrastructure error (network, outage, usage limit) is retried, never scored. After one,
    the runner probes Claude every 10 minutes and resumes as soon as it answers."""
    for attempt in range(1, tries + 1):
        rec = run_trial(case, args.skill, args, out)
        if not rec.get("infra_error") or attempt == tries:
            return rec
        print(f"      infra error ({rec['fails'][0][:80]}); probing every 10 min before retry {attempt}/{tries - 1}", flush=True)
        while True:
            time.sleep(600)
            if claude_reachable():
                break
        shutil.rmtree(out, ignore_errors=True)
    return rec


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", default="author-game-v2-lean")
    ap.add_argument("--case", default="*", help="glob over case ids")
    ap.add_argument("--trials", type=int, default=1, help="1 by default; use 3 only before a promotion decision")
    ap.add_argument("--model", default=None)
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--max-budget-usd", type=float, default=5.0)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--v2-ref", default=None,
                    help="commit to stage author-game-v2, its agents and the grader from (default: the commit "
                         "pinned in reference.json, so results stay comparable with v2's frozen numbers)")
    ap.add_argument("--skill-ref", default=None, help="commit to stage the skill under test from (default: working tree)")
    ap.add_argument("--set", default="quick", choices=CASE_SETS,
                    help="quick (default): the cases that separate v2 from lean + the held-out set")
    ap.add_argument("--include-v2", action="store_true",
                    help="allow running author-game-v2 itself; normally its frozen results in reference.json are used")
    ap.add_argument("--build-reference", action="store_true",
                    help="rebuild reference.json from every saved v2 and lean trial, then exit (no sessions)")
    ap.add_argument("--resume", default=None, help="continue an interrupted run dir: keep finished trials, re-run the rest")
    ap.add_argument("--regrade", default=None, help="re-grade a finished run dir from its saved diffs")
    ap.add_argument("--dry-run", action="store_true", help="stage and print the command, run nothing")
    ap.add_argument("--keep", action="store_true", help="keep staging dirs for inspection")
    args = ap.parse_args()

    if args.build_reference:
        return build_reference()
    if args.regrade:
        run_dir = Path(args.regrade).resolve()
        prior = json.loads((run_dir / "summary.json").read_text())
        args.v2_ref = prior.get("v2_ref", args.v2_ref)
        args.trials = prior.get("trials_per_case", args.trials)
        return regrade(run_dir, args)
    if not (REPO / ".claude/skills" / args.skill).is_dir():
        sys.exit(f"no skill at .claude/skills/{args.skill}")
    if args.skill == V2_SKILL and not args.include_v2:
        sys.exit("author-game-v2 is frozen; its results are in reference.json. Pass --include-v2 to re-run it anyway.")
    case_ids = [c for c in case_ids_for(args.set) if fnmatch.fnmatch(c, args.case)]
    if not case_ids:
        sys.exit(f"no case matches {args.case}")

    if args.v2_ref is None:
        args.v2_ref = json.loads(REFERENCE.read_text()).get("v2_ref", "HEAD") if REFERENCE.exists() else "HEAD"
    args.v2_ref = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", args.v2_ref],
                                 capture_output=True, text=True, check=True).stdout.strip()
    run_dir = EVAL_DIR / "results" / f"{datetime.now():%Y%m%d-%H%M%S}_{args.skill}_{args.set}"
    if args.resume:
        run_dir = Path(args.resume).resolve()
    run_dir.mkdir(parents=True, exist_ok=bool(args.resume))
    used = sorted({f for f in (fixture_of(json.loads((case_dir(c) / "case.json").read_text())) for c in case_ids)
                   if has_toml(f)})
    for fx in used:
        g = measure_baseline(args, fx)
        name = "baseline_gates.json" if fx == DEFAULT_FIXTURE else f"baseline_gates_{fx}.json"
        (run_dir / name).write_text(json.dumps(g, indent=1))
        print(f"baseline {fx} at {args.v2_ref}: {g['tally']['pass']} pass, "
              f"{g['tally']['fail']} fail, {g['tally']['na']} n/a", flush=True)
    records = []
    for cid in case_ids:
        case = json.loads((case_dir(cid) / "case.json").read_text())
        for t in range(1, args.trials + 1):
            out = run_dir / cid / f"trial{t}"
            done = out / "grade.json"
            if args.resume and done.exists() and not json.loads(done.read_text()).get("infra_error"):
                rec = json.loads(done.read_text())
                records.append(rec)
                print(f"KEPT  {cid} trial {t}  passed={rec.get('passed')}", flush=True)
                continue
            shutil.rmtree(out, ignore_errors=True)
            rec = run_with_retry(case, args, out)
            records.append(rec)
            mark = "DRY" if rec.get("dry_run") else ("ERROR" if rec.get("infra_error") else ("PASS" if rec["passed"] else "FAIL"))
            print(f"{mark}  {cid} trial {t}  cost={rec.get('cost_usd')}  turns={rec.get('turns')}", flush=True)
            for f in rec.get("fails", [])[:5]:
                print(f"      - {f}")
            if rec.get("dry_run"):
                print(f"      staging: {rec['staging']}")

    summary = summarize(records, args)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: summary[k] for k in ("skill", "v2_ref", "skill_ref", "cases", "pass_k_cases", "trial_pass_rate", "total_cost_usd")}, indent=1))
    print_vs_reference(summary)
    return 0


def print_vs_reference(summary: dict) -> None:
    if not REFERENCE.exists():
        return
    ref = json.loads(REFERENCE.read_text())["cases"]
    print(f"\n{'case':32s} {'this run':>10s} {'v2 (frozen)':>12s}")
    for cid, row in summary["per_case"].items():
        runs = [x for x in row["passed"] if x is not None]
        v2 = ref.get(cid, {}).get("v2", [0, 0])
        print(f"{cid:32s} {sum(map(bool, runs)):>4d}/{len(runs):<5d} {v2[0]:>6d}/{v2[1]:<5d}")


def build_reference() -> int:
    """Tally every saved trial per case and skill (infrastructure errors excluded)."""
    cases: dict[str, dict[str, list[int]]] = {}
    for f in sorted((EVAL_DIR / "results").glob("*/*/trial*/grade.json")):
        g = json.loads(f.read_text())
        if g.get("infra_error") or g.get("passed") is None or g.get("dry_run"):
            continue
        arm = "lean" if g["skill"].endswith("lean") else "v2"
        row = cases.setdefault(g["case"], {"v2": [0, 0], "lean": [0, 0]})
        row[arm][0] += bool(g["passed"])
        row[arm][1] += 1
    archive = EVAL_DIR / "reference_archive.json"     # tallies of runs whose folders are gone
    if archive.exists():
        for run in json.loads(archive.read_text())["runs"].values():
            for cid, (passed, n) in run["cases"].items():
                row = cases.setdefault(cid, {"v2": [0, 0], "lean": [0, 0]})
                row[run["skill"]][0] += passed
                row[run["skill"]][1] += n
    pin = json.loads(REFERENCE.read_text()).get("v2_ref", "ec72cb4") if REFERENCE.exists() else "ec72cb4"
    REFERENCE.write_text(json.dumps({"v2_ref": pin,
                                     "note": "[passed, trials] per case, all saved runs, infra errors excluded. "
                                             "v2 is frozen: re-run it only with --include-v2.",
                                     "cases": dict(sorted(cases.items()))}, indent=1) + "\n")
    for cid, row in sorted(cases.items()):
        print(f"{cid:32s} v2 {row['v2'][0]}/{row['v2'][1]}   lean {row['lean'][0]}/{row['lean'][1]}")
    return 0


def summarize(records: list[dict], args) -> dict:
    by_case: dict[str, list[dict]] = {}
    for r in records:
        by_case.setdefault(r["case"], []).append(r)
    real = [r for r in records if not r.get("dry_run") and not r.get("infra_error")]
    return {
        "skill": args.skill, "v2_ref": args.v2_ref, "skill_ref": args.skill_ref or "working tree",
        "set": getattr(args, "set", "main"), "model": args.model or "default",
        "trials_per_case": args.trials, "cases": len(by_case),
        "ran_gates_trials": sum(bool(r.get("ran_gates")) for r in real),
        "not_in_doctrine": sorted(cid for cid in by_case
                                  if json.loads((case_dir(cid) / "case.json").read_text()).get("doctrine") == "not in v2"),
        "infra_errors": sum(bool(r.get("infra_error")) for r in records),
        "pass_k_cases": sum(all(r.get("passed") for r in rs) for rs in by_case.values()
                            if not any(r.get("infra_error") for r in rs)) if real else None,
        "trial_pass_rate": round(sum(r["passed"] for r in real) / len(real), 3) if real else None,
        "total_cost_usd": round(sum(r.get("cost_usd") or 0 for r in real), 2),
        "per_case": {cid: {"passed": [r.get("passed") for r in rs],
                           "cost_usd": [r.get("cost_usd") for r in rs],
                           "ran_gates": [r.get("ran_gates") for r in rs]} for cid, rs in by_case.items()},
    }


if __name__ == "__main__":
    raise SystemExit(main())
