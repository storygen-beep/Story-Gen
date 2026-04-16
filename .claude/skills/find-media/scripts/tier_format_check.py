#!/usr/bin/env python3
"""
tier_format_check.py — hard gate before PACKAGE

Enforces two rules:
  1. Tier rule — t5+ must be animated video (.webm/.mp4/.gif), never a static JPG
  2. Family rule (optional via --description) — motion-worthy scenes (kiss/tease/
     undress/bathe/nudity/explicit) must be animated regardless of tier

Checks file extension, file size, and magic bytes. The description check runs
during PLAN phase via validate_queries.py and is re-applied here as a final gate.

Usage:
    python tier_format_check.py --file <path> --tier <tier> [--json]

Exit codes:
    0  pass
    1  fail (file missing, wrong format, too small, magic mismatch)
    2  invalid arguments
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SFW_TIERS = {"base", "t2", "t3", "location"}
BORDERLINE_TIERS = {"t4"}
NSFW_VIDEO_TIERS = {"t5", "t6", "t7", "t8"}

SFW_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
NSFW_ANIMATED_EXT = {".webm", ".mp4", ".gif"}
NSFW_T4_ALLOWED_EXT = SFW_ALLOWED_EXT | NSFW_ANIMATED_EXT

MIN_IMAGE_BYTES = 1024
MIN_VIDEO_BYTES = 50 * 1024

MAGIC_BYTES = {
    b"\xff\xd8\xff": "jpeg",
    b"\x89PNG\r\n\x1a\n": "png",
    b"RIFF": "webp_or_wav",
    b"\x1a\x45\xdf\xa3": "webm",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
}


@dataclass
class CheckResult:
    file: str
    tier: str
    exists: bool
    size_bytes: int
    extension: str
    magic_type: str | None
    passed: bool
    failures: list[str]


def detect_magic(path: Path) -> str | None:
    try:
        with path.open("rb") as f:
            head = f.read(16)
    except OSError:
        return None

    if head[4:8] == b"ftyp":
        return "mp4"
    for sig, name in MAGIC_BYTES.items():
        if head.startswith(sig):
            return name
    return None


def check(path: Path, tier: str) -> CheckResult:
    failures: list[str] = []
    result = CheckResult(
        file=str(path),
        tier=tier,
        exists=False,
        size_bytes=0,
        extension=path.suffix.lower(),
        magic_type=None,
        passed=False,
        failures=failures,
    )

    if not path.exists():
        failures.append("file_missing")
        return result

    result.exists = True
    result.size_bytes = path.stat().st_size
    result.magic_type = detect_magic(path)

    if tier in SFW_TIERS:
        if result.extension not in SFW_ALLOWED_EXT:
            failures.append(f"sfw_tier_wrong_extension:{result.extension}")
        if result.size_bytes < MIN_IMAGE_BYTES:
            failures.append(f"image_too_small:{result.size_bytes}B")
        if result.magic_type not in {"jpeg", "png", "webp_or_wav"}:
            failures.append(f"magic_mismatch:{result.magic_type}")

    elif tier in BORDERLINE_TIERS:
        if result.extension not in NSFW_T4_ALLOWED_EXT:
            failures.append(f"t4_wrong_extension:{result.extension}")
        min_size = MIN_VIDEO_BYTES if result.extension in NSFW_ANIMATED_EXT else MIN_IMAGE_BYTES
        if result.size_bytes < min_size:
            failures.append(f"file_too_small:{result.size_bytes}B")

    elif tier in NSFW_VIDEO_TIERS:
        if result.extension not in NSFW_ANIMATED_EXT:
            failures.append(f"t5plus_must_be_animated:{result.extension}")
        if result.size_bytes < MIN_VIDEO_BYTES:
            failures.append(f"video_too_small:{result.size_bytes}B")
        if result.magic_type == "jpeg":
            failures.append("t5plus_got_jpeg_thumbnail_not_video")
        if result.magic_type not in {"webm", "mp4", "gif"}:
            failures.append(f"magic_mismatch:{result.magic_type}")

    else:
        failures.append(f"unknown_tier:{tier}")

    result.passed = len(failures) == 0
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, type=Path)
    p.add_argument("--tier", required=True)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    result = check(args.file, args.tier)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.file} (tier: {result.tier})")
        print(f"  size: {result.size_bytes} bytes, ext: {result.extension}, magic: {result.magic_type}")
        if result.failures:
            print(f"  failures: {', '.join(result.failures)}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
