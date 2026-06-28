#!/usr/bin/env python3
"""
apply_retags.py — rewrite tier suffixes in a game's source toml_phases

Takes the accepted retags from the tier audit (validate_queries.py's TagProposals,
once the auto ones are taken and the asks are confirmed) and fixes the `file=` suffix
at the SOURCE so the tag is genuinely correct. After this, re-run
`scripts/merge_toml_phases.py` + `manage.py package_from_toml` so the change lands.

Mechanical + stdlib-only — keeps the TOML edit out of the LLM's hands and auditable.
Never touches the generated 7_final_game.toml (per CLAUDE.md). Matches a path only when
it appears as a quoted string, so `couch_kiss.jpg` won't clobber `couch_kiss_2.jpg`.

Input: a JSON list of accepted retags, `[{"file": "<current path>", "tier": "<tN|base>"}]`
(via --accepted <path> or stdin). `file` is the path exactly as it appears in the TOML
`file=`; any existing _tN/_base suffix is stripped before the new tier is appended.

Usage:
    apply_retags.py --phases-dir games/<game>/toml_phases --accepted retags.json [--dry-run] [--json]
    echo '[{"file":"activities/couch_kiss.jpg","tier":"t4"}]' | apply_retags.py --phases-dir <dir> --dry-run

Exit codes:
    0  applied (or dry-run) cleanly
    1  one or more retags matched nothing in the phases (caller should check the path)
    2  invalid arguments
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

TAG_SUFFIX_RE = re.compile(r"_(t[0-8]|base)$")
# The merge output is "<N>_final_game.toml" (N varies per game) — never edit it; the
# merge regenerates it from the source phases (CLAUDE.md).
GENERATED_SUFFIX = "_final_game.toml"


@dataclass
class RetagResult:
    file_old: str
    file_new: str
    tier: str
    occurrences: int
    phase_files: list[str] = field(default_factory=list)


def retag_path(path: str, tier: str) -> str:
    """Strip any existing _tN/_base suffix from the stem, append _<tier>."""
    p = Path(path)
    stem = TAG_SUFFIX_RE.sub("", p.stem)
    return str(p.with_name(f"{stem}_{tier}{p.suffix}"))


def load_accepted(accepted_path: Path | None) -> list[dict]:
    raw = accepted_path.read_text() if accepted_path else sys.stdin.read()
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("accepted") or data.get("retags") or []
    return [d for d in data if isinstance(d, dict) and d.get("file") and d.get("tier")]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--phases-dir", type=Path, required=True, dest="phases_dir")
    p.add_argument("--accepted", type=Path, help="JSON [{file,tier}]; omit to read stdin")
    p.add_argument("--dry-run", action="store_true", dest="dry_run")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not args.phases_dir.is_dir():
        print(f"ERROR: phases dir not found: {args.phases_dir}", file=sys.stderr)
        return 2
    try:
        accepted = load_accepted(args.accepted)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: could not read accepted retags: {e}", file=sys.stderr)
        return 2
    if not accepted:
        print("No accepted retags provided — nothing to do.", file=sys.stderr)
        return 0

    phase_files = [f for f in sorted(args.phases_dir.glob("*.toml")) if not f.name.endswith(GENERATED_SUFFIX)]
    texts = {f: f.read_text() for f in phase_files}

    results: list[RetagResult] = []
    for entry in accepted:
        old, tier = entry["file"], entry["tier"]
        new = retag_path(old, tier)
        if new == old:
            continue
        touched, total = [], 0
        for f in phase_files:
            t = texts[f]
            n = t.count(f'"{old}"') + t.count(f"'{old}'")
            if n:
                texts[f] = t.replace(f'"{old}"', f'"{new}"').replace(f"'{old}'", f"'{new}'")
                touched.append(f.name)
                total += n
        results.append(RetagResult(old, new, tier, total, touched))

    if not args.dry_run:
        for f, t in texts.items():
            f.write_text(t)

    changed = sorted({pf for r in results for pf in r.phase_files})
    missing = [r for r in results if r.occurrences == 0]

    if args.json:
        print(json.dumps({
            "dry_run": args.dry_run,
            "retags": [asdict(r) for r in results],
            "changed_phase_files": changed,
            "unmatched": [r.file_old for r in missing],
            "next": "re-run scripts/merge_toml_phases.py + manage.py package_from_toml, then re-fetch the missing-media list",
        }, indent=2))
    else:
        mode = "DRY-RUN (no writes)" if args.dry_run else "APPLIED"
        print(f"[{mode}] {len(results)} retags, {len(changed)} phase files affected")
        for r in results:
            where = ", ".join(r.phase_files) if r.phase_files else "⚠️ NO MATCH IN PHASES"
            print(f"  {r.file_old}  →  {r.file_new}   ({r.occurrences}× in {where})")
        if not args.dry_run and changed:
            print("\nNEXT: re-run scripts/merge_toml_phases.py + manage.py package_from_toml, "
                  "then re-fetch the missing-media list.")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
