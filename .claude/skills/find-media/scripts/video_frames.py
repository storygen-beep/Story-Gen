#!/usr/bin/env python3
"""
video_frames.py — ffmpeg frame extraction for find-media (NSFW shortlist + verify)

PornHub GIF clips have no meaningful poster frame, and a single frame is a
misleading way to judge a clip. Two modes solve that:

  rep    Representative still for CLIP ranking. Samples N evenly-spaced frames,
         picks the MEDIAN-by-file-size one (black/seam frames are tiny → they
         sort to the bottom and get skipped). Writes one .jpg.
  strip  Act-verification strip. Tiles N evenly-spaced frames into one 1xN image
         so the LLM/human can confirm the act holds across the loop, not just at
         one instant.

ffmpeg/ffprobe only — NO OpenCV, NO PIL, NO torch. Matches the skill's existing
lightweight inline ffmpeg usage so it runs under any python3 with ffmpeg on PATH.

Usage:
    # one representative still
    video_frames.py --video <clip> --mode rep --frames 3 --out <still.jpg> [--json]
    # batch: one rep still per clip in a dir (mirrors candidates for clip_shortlist)
    video_frames.py --videos-dir <dir> --mode rep --frames 3 --out-dir <frames_dir> [--json]
    # verification strip for one chosen clip
    video_frames.py --video <clip> --mode strip --frames 4 --out <strip.jpg> [--tile-px 320] [--json]

Exit codes:
    0  success (>=1 frame/strip written)
    1  no frames produced (corrupt / 0-byte clip)
    2  invalid arguments
    3  ffmpeg/ffprobe not on PATH → caller FALLS BACK to the harvest poster .jpg
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

VIDEO_EXTS = {".webm", ".mp4", ".gif", ".mov", ".mkv"}
MIN_FRAME_BYTES = 500


@dataclass
class FrameResult:
    mode: str
    inputs: list[str]
    outputs: list[str]
    frames_per_input: int
    passed: bool
    failures: list[str]


def _deps_present() -> bool:
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def probe_duration(video: Path) -> float | None:
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            stderr=subprocess.DEVNULL, timeout=20,
        ).strip()
        d = float(out)
        return d if d > 0 else None
    except (subprocess.SubprocessError, ValueError):
        return None


def even_fracs(n: int, lo: float, hi: float) -> list[float]:
    """N timestamps spread across (lo, hi) of the duration."""
    if n <= 1:
        return [(lo + hi) / 2]
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def extract_frame(video: Path, ts: float, out_path: Path, tile_px: int | None = None) -> bool:
    vf = []
    if tile_px:
        vf = ["-vf",
              f"scale={tile_px}:{tile_px}:force_original_aspect_ratio=decrease,"
              f"pad={tile_px}:{tile_px}:(ow-iw)/2:(oh-ih)/2:color=black"]
    cmd = ["ffmpeg", "-y", "-ss", f"{ts:.3f}", "-i", str(video),
           "-frames:v", "1", "-q:v", "3", *vf, str(out_path)]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=30, check=False)
    except subprocess.SubprocessError:
        return False
    return out_path.exists() and out_path.stat().st_size >= MIN_FRAME_BYTES


def rep_frame(video: Path, n: int, out_path: Path) -> bool:
    """Median-by-size of N samples in the middle of the clip (skips black/seam)."""
    dur = probe_duration(video)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        frames: list[Path] = []
        fracs = even_fracs(n, 0.15, 0.85) if dur else [0.0]
        for i, f in enumerate(fracs):
            ts = (dur * f) if dur else 1.0
            p = Path(td) / f"r{i}.jpg"
            if extract_frame(video, ts, p):
                frames.append(p)
        if not frames:
            return False
        frames.sort(key=lambda p: p.stat().st_size)
        shutil.copy(frames[len(frames) // 2], out_path)  # median by size
    return True


def strip_frames(video: Path, n: int, out_path: Path, tile_px: int) -> bool:
    """Tile N evenly-spaced frames (wider span) into one 1xN strip via ffmpeg."""
    dur = probe_duration(video) or 5.0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        good: list[Path] = []
        for i, f in enumerate(even_fracs(n, 0.05, 0.95)):
            p = Path(td) / f"x{i:03d}.jpg"
            if extract_frame(video, dur * f, p, tile_px=tile_px):
                good.append(p)
        if not good:
            return False
        # renumber contiguously so ffmpeg's image-sequence reader sees f000..fK
        seq_dir = Path(td) / "seq"
        seq_dir.mkdir()
        for i, p in enumerate(good):
            shutil.copy(p, seq_dir / f"f{i:03d}.jpg")
        cmd = ["ffmpeg", "-y", "-framerate", "1", "-i", str(seq_dir / "f%03d.jpg"),
               "-vf", f"tile={len(good)}x1", "-frames:v", "1", "-q:v", "3", str(out_path)]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=30, check=False)
        except subprocess.SubprocessError:
            return False
    return out_path.exists() and out_path.stat().st_size >= MIN_FRAME_BYTES


def main() -> int:
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--video", type=Path, help="single clip")
    src.add_argument("--videos-dir", type=Path, dest="videos_dir", help="batch: every clip in this dir")
    p.add_argument("--mode", choices=["rep", "strip"], required=True)
    p.add_argument("--frames", type=int, default=None, help="frames to sample (rep default 3, strip default 4)")
    p.add_argument("--out", type=Path, help="output file (single-clip modes)")
    p.add_argument("--out-dir", type=Path, dest="out_dir", help="output dir (--videos-dir batch)")
    p.add_argument("--tile-px", type=int, default=320, dest="tile_px", help="per-tile size for strip")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not _deps_present():
        msg = "ffmpeg/ffprobe not found on PATH"
        if args.json:
            print(json.dumps({"passed": False, "exit": 3, "error": msg}))
        else:
            print(f"[DEPS] {msg} — caller should fall back to the harvest poster .jpg", file=sys.stderr)
        return 3

    n = args.frames if args.frames else (4 if args.mode == "strip" else 3)
    result = FrameResult(mode=args.mode, inputs=[], outputs=[], frames_per_input=n, passed=False, failures=[])

    if args.videos_dir is not None:
        if args.mode != "rep":
            print("ERROR: --videos-dir only supports --mode rep", file=sys.stderr)
            return 2
        if not args.out_dir:
            print("ERROR: --videos-dir requires --out-dir", file=sys.stderr)
            return 2
        clips = sorted(c for c in args.videos_dir.iterdir() if c.suffix.lower() in VIDEO_EXTS)
        for clip in clips:
            result.inputs.append(str(clip))
            out = args.out_dir / f"{clip.stem}.jpg"
            if rep_frame(clip, n, out):
                result.outputs.append(str(out))
            else:
                result.failures.append(f"no_frame:{clip.name}")
    else:
        if not args.out:
            print("ERROR: --video requires --out", file=sys.stderr)
            return 2
        result.inputs.append(str(args.video))
        ok = (rep_frame if args.mode == "rep" else
              lambda v, k, o: strip_frames(v, k, o, args.tile_px))(args.video, n, args.out)
        if ok:
            result.outputs.append(str(args.out))
        else:
            result.failures.append(f"no_frame:{args.video.name}")

    result.passed = len(result.outputs) > 0

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        status = "OK" if result.passed else "FAIL"
        print(f"[{status}] mode={result.mode} wrote {len(result.outputs)}/{len(result.inputs)} "
              f"({n} frames sampled each)")
        for o in result.outputs:
            print(f"  -> {o}")
        if result.failures:
            print(f"  failures: {', '.join(result.failures)}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
