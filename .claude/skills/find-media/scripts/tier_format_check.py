#!/usr/bin/env python3
"""
tier_format_check.py — hard gate before INSTALL

Enforces one rule, per tier: t5+ must be animated video (.webm/.mp4/.gif), never a
static JPG.

Checks file extension, file size, and magic bytes at EVERY tier. Magic bytes are the
only check that survives a third-party CDN — the Chrome/Google route fetches from a
dozen hosts, any of which can serve an HTML error page or a JPEG behind a .gif URL,
and neither shows up in the extension or the size.

The motion-vs-static content-family question is a separate axis and lives in
scene_semantics.py / validate_queries.py, which run during PLAN.

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


# t0/t1 are legal tags (scene_semantics.infer_tier_tagged accepts _t0.._t8); without
# them here a correctly-tagged low-tier slot failed the pre-install gate as
# "unknown_tier" — a rejection that described nothing wrong with the file.
SFW_TIERS = {"base", "t0", "t1", "t2", "t3", "location"}
BORDERLINE_TIERS = {"t4"}
NSFW_VIDEO_TIERS = {"t5", "t6", "t7", "t8"}

SFW_STATIC_EXT = {".jpg", ".jpeg", ".png", ".webp"}
NSFW_ANIMATED_EXT = {".webm", ".mp4", ".gif"}
# .gif is allowed at SFW tiers as of the Chrome/Google route. Google Images hands back
# gifs for SFW beats too, and the renderer picks <video> vs <img> from the bytes on
# disk — so a SFW gif is a valid asset, not a mis-fetch to reject.
SFW_ALLOWED_EXT = SFW_STATIC_EXT | {".gif"}
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

# Magic names grouped the same way extensions are, so "the bytes agree with the name"
# is one comparison instead of a per-tier allow-list that drifts.
ANIMATED_MAGIC = {"webm", "mp4", "gif"}
STATIC_MAGIC = {"jpeg", "png", "webp_or_wav"}


def ext_family(extension: str) -> str:
    return "animated" if extension in NSFW_ANIMATED_EXT else "static"


def magic_family(magic: str | None) -> str | None:
    if magic in ANIMATED_MAGIC:
        return "animated"
    if magic in STATIC_MAGIC:
        return "static"
    return None  # unrecognised → almost always an HTML error page saved as media


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
        # A SFW .gif keeps the image floor, not the video floor: the floor exists to
        # catch 0-byte and error-page stubs, and a short SFW gif is legitimately small.
        if result.size_bytes < MIN_IMAGE_BYTES:
            failures.append(f"image_too_small:{result.size_bytes}B")
        # Family comparison rather than a flat allow-list — now that .gif is legal at
        # SFW, a flat list would let gif BYTES pass inside a .jpg name.
        if magic_family(result.magic_type) != ext_family(result.extension):
            failures.append(f"magic_mismatch:{result.magic_type}")

    elif tier in BORDERLINE_TIERS:
        if result.extension not in NSFW_T4_ALLOWED_EXT:
            failures.append(f"t4_wrong_extension:{result.extension}")
        min_size = MIN_VIDEO_BYTES if result.extension in NSFW_ANIMATED_EXT else MIN_IMAGE_BYTES
        if result.size_bytes < min_size:
            failures.append(f"file_too_small:{result.size_bytes}B")
        # t4 used to skip magic bytes entirely — it was the one tier where an HTML
        # error page or a JPEG served behind a .gif URL sailed through to INSTALL.
        if result.magic_type is None:
            failures.append("magic_mismatch:None")
        elif magic_family(result.magic_type) != ext_family(result.extension):
            failures.append(
                f"magic_ext_family_mismatch:{result.extension}_holds_{result.magic_type}")

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
