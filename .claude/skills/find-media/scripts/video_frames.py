#!/usr/bin/env python3
"""
video_frames.py — ffmpeg frame extraction for find-media (NSFW shortlist + verify)

Harvested clips have no meaningful poster frame, and a single frame is a
misleading way to judge a clip. Two modes solve that:

  rep    Representative still, one per candidate — the tile of a CONTACT SHEET.
         Samples N evenly-spaced frames and picks the MEDIAN-by-file-size one
         (black/seam frames are tiny → they sort to the bottom and get skipped).
         Writes one .jpg.
  strip  Act-verification strip. Tiles N evenly-spaced frames into one 1xN image
         so the act can be confirmed across the loop, not just at one instant.

Both batch modes assemble ONE image for review: --sheet tiles rep frames into a
contact sheet, --board stacks strips into a labelled board. That assembled image
is what gets read; reading per-candidate strips one at a time measured 3x the
cost for identical verdicts (2026-07-29).

Nothing here ranks or scores. ffmpeg cuts, resizes, labels and glues — the
judging is done by whoever reads the output, so tile order is the caller's fetch
order and carries no claim about quality.

ffmpeg/ffprobe only — NO OpenCV, NO PIL, NO torch, no model of any kind. Runs
under any python3 with ffmpeg on PATH.

Usage:
    # one representative still
    video_frames.py --video <clip> --mode rep --frames 3 --out <still.jpg> [--json]
    # batch: one rep still per clip in a dir (+ --sheet for the contact sheet)
    video_frames.py --videos-dir <dir> --mode rep --frames 3 --out-dir <frames_dir> [--json]
    # verification strip for one chosen clip
    video_frames.py --video <clip> --mode strip --frames 4 --out <strip.jpg> [--tile-px 320] [--json]
    # batch: one strip per STOCKED OPTION in a dir → <stem>_strip.jpg
    video_frames.py --videos-dir <dir> --mode strip --frames 4 --out-dir <frames_dir> [--json]

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
from dataclasses import asdict, dataclass, field
from pathlib import Path

VIDEO_EXTS = {".webm", ".mp4", ".gif", ".mov", ".mkv"}
# A still IS its own representative frame. Candidate pools are mixed — a location or
# clothing slot fetches .jpg while a scene slot fetches .gif — and excluding stills from
# batch rep mode meant those candidates silently vanished from the contact sheet, which
# reads as "the harvest found nothing" rather than "this tool skipped them".
# rep mode only: a still has no loop, so there is nothing for strip mode to claim.
STILL_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MIN_FRAME_BYTES = 500

# Measured: the CDN gifs this skill fetches run ~2s (1.9s and 3.8s on two sampled
# from games/). The old 5.0s fallback made ffmpeg seek PAST THE END for the back half
# of the strip, and an out-of-range seek returns the LAST frame — so a strip of a 2s
# clip showed the same final frame 2-3 times and read as a held pose that isn't there.
SHORT_CLIP_FALLBACK_SEC = 2.0
# `-count_frames` decodes the whole file. Only worth it on small clips, and every clip
# on this route is well under this.
MAX_COUNT_FRAMES_BYTES = 25 * 1024 * 1024
# With no duration at all, take fewer samples rather than spread guesses across a
# length we don't know.
UNKNOWN_DURATION_MAX_FRAMES = 3


@dataclass
class FrameResult:
    mode: str
    inputs: list[str]
    outputs: list[str]
    frames_per_input: int
    passed: bool
    failures: list[str]
    sheet: str | None = None
    boards: list[str] = field(default_factory=list)


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


def _ffprobe_json(video: Path, entries: str) -> dict:
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", entries, "-of", "json", str(video)],
            stderr=subprocess.DEVNULL, timeout=30,
        )
        streams = json.loads(out).get("streams") or []
    except (subprocess.SubprocessError, ValueError, json.JSONDecodeError):
        return {}
    return streams[0] if streams else {}


def _positive_float(value: object) -> float | None:
    try:
        f = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return f if f > 0 else None


def probe_clip_geometry(video: Path) -> tuple[float | None, int | None]:
    """(duration_seconds, frame_count) — either may be None.

    format=duration is the cheap answer but GIFs and truncated CDN downloads report it
    as N/A, which is exactly when the 5.0s fallback used to sample past the end. So
    fall back to the video stream's own duration, then to frame count ÷ average rate,
    then to actually counting frames on a small file. Frame count is returned too so
    the caller can refuse to ask for more distinct frames than the clip contains.
    """
    dur = probe_duration(video)
    s = _ffprobe_json(video, "stream=duration,nb_frames,avg_frame_rate")

    if dur is None:
        dur = _positive_float(s.get("duration"))

    nb: int | None = None
    raw_nb = _positive_float(s.get("nb_frames"))
    if raw_nb:
        nb = int(raw_nb)

    # avg_frame_rate is a rational string like "30000/1001" or "10/1".
    fps: float | None = None
    rate = str(s.get("avg_frame_rate") or "")
    if "/" in rate:
        num, _, den = rate.partition("/")
        n_f, d_f = _positive_float(num), _positive_float(den)
        if n_f and d_f:
            fps = n_f / d_f

    if nb is None and dur is None:
        try:
            small_enough = video.stat().st_size <= MAX_COUNT_FRAMES_BYTES
        except OSError:
            small_enough = False
        if small_enough:
            # -count_frames is its own (expensive) invocation, hence the separate call.
            counted = None
            try:
                out = subprocess.check_output(
                    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                     "-show_entries", "stream=nb_read_frames",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
                    stderr=subprocess.DEVNULL, timeout=60,
                ).strip()
                counted = _positive_float(out)
            except (subprocess.SubprocessError, ValueError):
                counted = None
            if counted:
                nb = int(counted)

    if dur is None and nb and fps:
        dur = nb / fps

    return dur, nb


def sample_plan(n: int, dur: float | None, nb_frames: int | None) -> tuple[float, int]:
    """(seconds to spread samples across, how many samples to take).

    Never sample past the end — an over-long duration guess makes ffmpeg return the
    LAST frame for every out-of-range timestamp, which fakes a held pose. And never ask
    for more frames than the clip actually has, or the extra samples are byte-identical
    duplicates that make a 4-tile strip look like it proves something it doesn't.
    """
    span = dur if dur and dur > 0 else SHORT_CLIP_FALLBACK_SEC
    count = n
    if nb_frames and nb_frames > 0:
        count = min(count, nb_frames)
    if dur is None:
        count = min(count, UNKNOWN_DURATION_MAX_FRAMES)
    return span, max(1, count)


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


def still_rep(image: Path, out_path: Path) -> bool:
    """A still's rep frame is itself — just normalise it so it tiles with the clips.

    No -ss: seeking a single-image input lands past EOF and yields no frame at all,
    which is how a mixed pool loses exactly its image candidates.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", str(image), "-frames:v", "1", "-q:v", "3", str(out_path)]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=30, check=False)
    except subprocess.SubprocessError:
        return False
    return out_path.exists() and out_path.stat().st_size >= MIN_FRAME_BYTES


def contact_sheet(frames: list[Path], out_path: Path, tile_px: int, cols: int = 4) -> bool:
    """Tile rep frames into ONE numbered sheet — the image JUDGE actually Reads.

    The number burned into each tile is the candidate's index, so a judgement can name
    "tile 07" and that maps straight back to 07.gif and to manifest.json. Without the
    label you are reading an anonymous grid and cannot act on what you see.
    """
    if not frames:
        return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = (len(frames) + cols - 1) // cols
    with tempfile.TemporaryDirectory() as td:
        seq = Path(td)
        for i, src in enumerate(sorted(frames)):
            label = src.stem.split("_")[0]
            # pad to a uniform tile first: tile= requires every input to match exactly
            vf = (f"scale={tile_px}:{tile_px}:force_original_aspect_ratio=decrease,"
                  f"pad={tile_px}:{tile_px}:(ow-iw)/2:(oh-ih)/2:color=black,"
                  f"drawtext=text='{label}':x=6:y=6:fontsize={max(18, tile_px // 7)}:"
                  f"fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=5")
            cmd = ["ffmpeg", "-y", "-i", str(src), "-vf", vf,
                   "-frames:v", "1", "-q:v", "3", str(seq / f"t{i:03d}.jpg")]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=30, check=False)
            except subprocess.SubprocessError:
                return False
        made = sorted(seq.glob("t*.jpg"))
        if not made:
            return False
        # blank filler so the final row is complete
        for j in range(len(made), rows * cols):
            filler = seq / f"t{j:03d}.jpg"
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                            f"color=c=black:s={tile_px}x{tile_px}:d=1",
                            "-frames:v", "1", "-update", "1", str(filler)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=30, check=False)
        tiles = sorted(seq.glob("t*.jpg"))

        # hstack rows then vstack them, NOT the tile= filter. Measured 2026-07-28: fed 8
        # correct 320x320 tiles, `tile=4x2` emitted a sheet containing only ONE of them
        # (reproduced in pure shell, so it is ffmpeg's behaviour here, not this script).
        # hstack/vstack is explicit about which input goes where and was verified correct.
        inputs: list[str] = []
        for t in tiles:
            inputs += ["-i", str(t)]
        parts = []
        for r in range(rows):
            refs = "".join(f"[{r * cols + c}:v]" for c in range(cols))
            parts.append(f"{refs}hstack=inputs={cols}[r{r}]")
        if rows > 1:
            refs = "".join(f"[r{r}]" for r in range(rows))
            parts.append(f"{refs}vstack=inputs={rows}[out]")
            final = "[out]"
        else:
            final = "[r0]"
        cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(parts),
               "-map", final, "-frames:v", "1", "-update", "1", "-q:v", "3", str(out_path)]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=120, check=False)
        except subprocess.SubprocessError:
            return False
    return out_path.exists() and out_path.stat().st_size >= MIN_FRAME_BYTES


def strip_board(strips: list[Path], out_path: Path, tile_px: int, cols: int = 4,
                rows_per_board: int = 6) -> list[Path]:
    """Stack per-candidate STRIPS into labelled boards — one row per candidate.

    This is the strip-mode analogue of contact_sheet(), and it is what makes JUDGE
    affordable. A contact sheet answers "which candidates are worth a strip"; a board
    answers "which candidate passes the gates", because every row is a whole LOOP, not
    one instant. Six rows of four frames at 320px is 1280x1920 — the geometry that
    carried the 2026-07-27 run, still ~260px per frame after the reader's downscale,
    which is enough to call eye contact.

    History, so this is not dropped a second time: the 2026-07-28 promotion of the
    ad-hoc `strips.sh` into this script kept `--sheet` for rep mode ONLY and silently
    lost strip boarding. The next run therefore read strips one at a time — 52 image
    reads where 15 would have done — and the lost minutes were misattributed to the
    experiment being measured rather than to the missing feature. Boards are not a
    nicety; without them batch JUDGE costs 3x for nothing.

    Returns the boards written (>6 candidates spills to <stem>_2.jpg, _3.jpg, ...).
    """
    if not strips:
        return []
    out_path.parent.mkdir(parents=True, exist_ok=True)
    width = cols * tile_px
    written: list[Path] = []
    chunks = [strips[i:i + rows_per_board] for i in range(0, len(strips), rows_per_board)]
    for b, chunk in enumerate(chunks):
        target = out_path if b == 0 else out_path.with_name(f"{out_path.stem}_{b + 1}{out_path.suffix}")
        with tempfile.TemporaryDirectory() as td:
            seq = Path(td)
            rows: list[Path] = []
            for i, src in enumerate(chunk):
                # "08_strip" -> "08"; the label is the candidate index, so a verdict can
                # name row 08 and it maps straight back to 08.gif and to manifest.json.
                label = src.stem.split("_")[0]
                # Strips differ in width when a clip yields fewer frames than asked
                # (3 frames = 960px, 4 = 1280px). vstack demands identical widths, so
                # pad every row to cols*tile_px before stacking or ffmpeg drops them.
                vf = (f"scale={width}:{tile_px}:force_original_aspect_ratio=decrease,"
                      f"pad={width}:{tile_px}:0:(oh-ih)/2:color=black,"
                      f"drawtext=text='{label}':x=8:y=8:fontsize={max(20, tile_px // 6)}:"
                      f"fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=6")
                row = seq / f"r{i:03d}.jpg"
                try:
                    subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vf", vf,
                                    "-frames:v", "1", "-q:v", "3", str(row)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=30, check=False)
                except subprocess.SubprocessError:
                    continue
                if row.exists() and row.stat().st_size >= MIN_FRAME_BYTES:
                    rows.append(row)
            if not rows:
                continue
            if len(rows) == 1:
                shutil.copy(rows[0], target)
            else:
                # vstack, not tile= — same reason contact_sheet() avoids it (measured
                # 2026-07-28: tile= silently emitted one input of eight).
                inputs: list[str] = []
                for r in rows:
                    inputs += ["-i", str(r)]
                refs = "".join(f"[{i}:v]" for i in range(len(rows)))
                cmd = ["ffmpeg", "-y", *inputs, "-filter_complex",
                       f"{refs}vstack=inputs={len(rows)}[out]", "-map", "[out]",
                       "-frames:v", "1", "-update", "1", "-q:v", "3", str(target)]
                try:
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=120, check=False)
                except subprocess.SubprocessError:
                    continue
        if target.exists() and target.stat().st_size >= MIN_FRAME_BYTES:
            written.append(target)
    return written


def rep_frame(video: Path, n: int, out_path: Path) -> bool:
    """Median-by-size of N samples in the middle of the clip (skips black/seam)."""
    dur, nb = probe_clip_geometry(video)
    span, count = sample_plan(n, dur, nb)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        frames: list[Path] = []
        fracs = even_fracs(count, 0.15, 0.85)
        for i, f in enumerate(fracs):
            ts = span * f
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
    dur, nb = probe_clip_geometry(video)
    span, count = sample_plan(n, dur, nb)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        good: list[Path] = []
        for i, f in enumerate(even_fracs(count, 0.05, 0.95)):
            p = Path(td) / f"x{i:03d}.jpg"
            if extract_frame(video, span * f, p, tile_px=tile_px):
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
    p.add_argument("--sheet", type=Path, default=None,
                   help="batch rep mode only: also tile every rep frame into ONE numbered "
                        "contact sheet at this path — the single image JUDGE reads")
    p.add_argument("--sheet-cols", type=int, default=4, dest="sheet_cols")
    p.add_argument("--board", type=Path, default=None,
                   help="batch STRIP mode only: also stack every candidate's strip into ONE "
                        "labelled board (one row per candidate) — the single image JUDGE "
                        "reads. Spills to <stem>_2.jpg beyond --board-rows candidates.")
    p.add_argument("--board-rows", type=int, default=6, dest="board_rows",
                   help="candidates per board (default 6 — the 1280x1920 geometry that is "
                        "still legible after the reader's downscale)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.sheet and not (args.videos_dir is not None and args.mode == "rep"):
        print("ERROR: --sheet requires --videos-dir with --mode rep", file=sys.stderr)
        return 2
    if args.board and not (args.videos_dir is not None and args.mode == "strip"):
        print("ERROR: --board requires --videos-dir with --mode strip", file=sys.stderr)
        return 2

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
        # Batch strip is allowed: the deliverable is >=6 STOCKED options per slot, and
        # every one of them needs its own strip before the human sees it — thumbnails
        # lie (3 of 5 and 4 of 6 shortlisted candidates died on the strip in one
        # session). One call per option would be six shell round-trips per slot.
        if not args.out_dir:
            print("ERROR: --videos-dir requires --out-dir", file=sys.stderr)
            return 2
        # rep mode also accepts stills (a still is its own rep frame); strip mode cannot —
        # there is no loop to make a claim about.
        accepted = VIDEO_EXTS | STILL_EXTS if args.mode == "rep" else VIDEO_EXTS
        clips = sorted(c for c in args.videos_dir.iterdir() if c.suffix.lower() in accepted)
        rep_paths: list[Path] = []
        for clip in clips:
            result.inputs.append(str(clip))
            # Distinct suffix so a strip run and a rep run can share one out-dir.
            out = args.out_dir / (f"{clip.stem}.jpg" if args.mode == "rep"
                                  else f"{clip.stem}_strip.jpg")
            if args.mode == "rep":
                ok = (still_rep(clip, out) if clip.suffix.lower() in STILL_EXTS
                      else rep_frame(clip, n, out))
            else:
                ok = strip_frames(clip, n, out, args.tile_px)
            if ok:
                result.outputs.append(str(out))
                rep_paths.append(out)
            else:
                result.failures.append(f"no_frame:{clip.name}")

        if args.sheet:
            if contact_sheet(rep_paths, args.sheet, args.tile_px, args.sheet_cols):
                result.sheet = str(args.sheet)
            else:
                result.failures.append("no_sheet")

        if args.board:
            boards = strip_board(rep_paths, args.board, args.tile_px,
                                 args.sheet_cols, args.board_rows)
            if boards:
                result.boards = [str(b) for b in boards]
            else:
                result.failures.append("no_board")
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
        if result.sheet:
            print(f"  CONTACT SHEET -> {result.sheet}   (Read this one image, not the tiles)")
        for b in result.boards:
            print(f"  STRIP BOARD -> {b}   (Read this one image, not the per-clip strips)")
        if result.failures:
            print(f"  failures: {', '.join(result.failures)}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
