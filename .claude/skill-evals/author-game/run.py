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
CASES_DIR = EVAL_DIR / "cases"
# Re-measured at the start of every run with the pinned gates.py (see measure_baseline);
# baseline_gates.json is the reference copy from when the exam was built.
BASELINE_GATES: dict = json.loads((EVAL_DIR / "baseline_gates.json").read_text())
BASELINE_GAME = lib.load_game(EVAL_DIR / "tests" / "fixture_7_final_game.toml")

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


def stage(skill: str, root: Path, args) -> Path:
    """v2 and its agents come from a pinned commit (--v2-ref), so edits other sessions leave in the
    working tree cannot shift the baseline. A skill other than v2 comes from the working tree unless
    --skill-ref pins it too."""
    root.mkdir(parents=True)
    fx = lib.FIXTURE
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

    # A git repo inside staging records exactly what the session changed.
    for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.name=exam", "-c", "user.email=exam@local",
                                                 "commit", "-qm", "fixture"]):
        subprocess.run(["git", "-C", str(root), *cmd], check=True)
    return root


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
    info = {"init": None, "result": None, "bash": [], "skills_called": []}
    for line in lines:
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            info["init"] = {k: ev.get(k) for k in ("model", "skills", "agents", "plugins", "tools",
                                                    "slash_commands", "cwd", "permissionMode")}
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


def measure_baseline(args) -> dict:
    root = Path(tempfile.mkdtemp(prefix="exam_baseline_")) / "w"
    staging = stage(V2, root, args)
    gates_py, merge_py = pinned_tools(staging)
    game_dir = staging / "games" / lib.FIXTURE["game"]
    if lib.merge(game_dir, merge_py).returncode != 0:
        sys.exit("fixture does not merge with the pinned merge script")
    base = lib.run_gates(lib.final_toml(game_dir), gates_py)
    shutil.rmtree(root.parent, ignore_errors=True)
    return base


def grade(case: dict, staging: Path, out: Path) -> dict:
    game_dir = staging / "games" / lib.FIXTURE["game"]
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

    fails += lib.gate_regressions(gates, BASELINE_GATES)
    fails += lib.new_lint_findings(gates, BASELINE_GATES, case.get("target_lints", []))
    spec = importlib.util.spec_from_file_location("case_check", CASES_DIR / case["id"] / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fails += mod.check(game, BASELINE_GAME)
    return {"passed": not fails, "fails": fails, "tally": gates["tally"]}


def run_trial(case: dict, skill: str, args, out: Path) -> dict:
    out.mkdir(parents=True)
    staging = stage(skill, Path(tempfile.mkdtemp(prefix=f"exam_{case['id']}_")) / "w", args)
    prompt = PREAMBLE.format(game=lib.FIXTURE["game"], task=case["task"])
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

    result = grade(case, staging, out)
    res = session["result"] or {}
    record = {
        "case": case["id"], "skill": skill, "passed": result["passed"], "fails": result["fails"],
        "cost_usd": res.get("total_cost_usd"), "turns": res.get("num_turns"), "subtype": res.get("subtype"),
        "wall_s": round(time.time() - started, 1), "ran_gates": any("gates.py" in c for c in session["bash"]),
        "skills_called": session["skills_called"], "permission_denials": res.get("permission_denials"),
        "changed_files": diff.splitlines(), "init": session["init"], "staging": str(staging),
    }
    (out / "grade.json").write_text(json.dumps(record, indent=1))
    if not args.keep:
        shutil.rmtree(staging.parent, ignore_errors=True)
    return record


def regrade(run_dir: Path, args) -> int:
    """Re-grade a finished run from its saved diffs with the current graders. No session is re-run."""
    global BASELINE_GATES
    BASELINE_GATES = json.loads((run_dir / "baseline_gates.json").read_text())
    records = []
    for grade_file in sorted(run_dir.glob("*/trial*/grade.json")):
        out = grade_file.parent
        rec = json.loads(grade_file.read_text())
        case = json.loads((CASES_DIR / rec["case"] / "case.json").read_text())
        staging = stage(V2, Path(tempfile.mkdtemp(prefix="exam_regrade_")) / "w", args)
        patch = out / "diff.patch"
        if patch.read_text().strip():
            subprocess.run(["git", "-C", str(staging), "apply", "--whitespace=nowarn", str(patch.resolve())], check=True)
        result = grade(case, staging, out)
        if rec.get("passed") != result["passed"]:
            print(f"changed  {rec['case']} {out.name}: {rec.get('passed')} -> {result['passed']}")
        rec["passed"], rec["fails"], rec["regraded"] = result["passed"], result["fails"], True
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
    print(json.dumps({k: summary[k] for k in ("skill", "cases", "pass_k_cases", "trial_pass_rate", "total_cost_usd")}, indent=1))
    return 0


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", default="author-game-v2")
    ap.add_argument("--case", default="*", help="glob over case ids")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--model", default=None)
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--max-budget-usd", type=float, default=5.0)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--v2-ref", default="HEAD", help="commit to stage author-game-v2 and its agents from")
    ap.add_argument("--skill-ref", default=None, help="commit to stage the skill under test from (default: working tree)")
    ap.add_argument("--regrade", default=None, help="re-grade a finished run dir from its saved diffs")
    ap.add_argument("--dry-run", action="store_true", help="stage and print the command, run nothing")
    ap.add_argument("--keep", action="store_true", help="keep staging dirs for inspection")
    args = ap.parse_args()

    if args.regrade:
        run_dir = Path(args.regrade).resolve()
        prior = json.loads((run_dir / "summary.json").read_text())
        args.v2_ref = prior.get("v2_ref", args.v2_ref)
        args.trials = prior.get("trials_per_case", args.trials)
        return regrade(run_dir, args)
    if not (REPO / ".claude/skills" / args.skill).is_dir():
        sys.exit(f"no skill at .claude/skills/{args.skill}")
    case_ids = sorted(p.name for p in CASES_DIR.iterdir() if p.is_dir() and fnmatch.fnmatch(p.name, args.case))
    if not case_ids:
        sys.exit(f"no case matches {args.case}")

    args.v2_ref = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", args.v2_ref],
                                 capture_output=True, text=True, check=True).stdout.strip()
    run_dir = EVAL_DIR / "results" / f"{datetime.now():%Y%m%d-%H%M%S}_{args.skill}"
    global BASELINE_GATES
    BASELINE_GATES = measure_baseline(args)
    run_dir.mkdir(parents=True)
    (run_dir / "baseline_gates.json").write_text(json.dumps(BASELINE_GATES, indent=1))
    print(f"baseline at {args.v2_ref}: {BASELINE_GATES['tally']['pass']} pass, "
          f"{BASELINE_GATES['tally']['fail']} fail, {BASELINE_GATES['tally']['na']} n/a", flush=True)
    records = []
    for cid in case_ids:
        case = json.loads((CASES_DIR / cid / "case.json").read_text())
        for t in range(1, args.trials + 1):
            rec = run_trial(case, args.skill, args, run_dir / cid / f"trial{t}")
            records.append(rec)
            mark = "DRY" if rec.get("dry_run") else ("PASS" if rec["passed"] else "FAIL")
            print(f"{mark}  {cid} trial {t}  cost={rec.get('cost_usd')}  turns={rec.get('turns')}", flush=True)
            for f in rec.get("fails", [])[:5]:
                print(f"      - {f}")
            if rec.get("dry_run"):
                print(f"      staging: {rec['staging']}")

    summary = summarize(records, args)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: summary[k] for k in ("skill", "v2_ref", "skill_ref", "cases", "pass_k_cases", "trial_pass_rate", "total_cost_usd")}, indent=1))
    return 0


def summarize(records: list[dict], args) -> dict:
    by_case: dict[str, list[dict]] = {}
    for r in records:
        by_case.setdefault(r["case"], []).append(r)
    real = [r for r in records if not r.get("dry_run")]
    return {
        "skill": args.skill, "v2_ref": args.v2_ref, "skill_ref": args.skill_ref or "working tree",
        "model": args.model or "default", "trials_per_case": args.trials, "cases": len(by_case),
        "pass_k_cases": sum(all(r.get("passed") for r in rs) for rs in by_case.values()) if real else None,
        "trial_pass_rate": round(sum(r["passed"] for r in real) / len(real), 3) if real else None,
        "total_cost_usd": round(sum(r.get("cost_usd") or 0 for r in real), 2),
        "per_case": {cid: {"passed": [r.get("passed") for r in rs],
                           "cost_usd": [r.get("cost_usd") for r in rs],
                           "ran_gates": [r.get("ran_gates") for r in rs]} for cid, rs in by_case.items()},
    }


if __name__ == "__main__":
    raise SystemExit(main())
