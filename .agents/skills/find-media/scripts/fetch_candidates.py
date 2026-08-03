#!/usr/bin/env python3
"""
fetch_candidates.py — pull stocked candidate URLs down to disk so they can be judged

The Chrome route stocks URLs (free, no bytes). JUDGE needs BYTES: a contact sheet needs
one rep frame per candidate, and a frame strip needs the actual file. This script is the
bridge, and it exists because that bridge used to be re-improvised per game — the skill
shipped no fetcher at all, only a "manual curl" line, so every run re-paid the setup cost
and re-discovered the same failures.

Two lessons are baked into the code rather than left to prose:

1. **Referer = the URL's OWN origin. NEVER the search engine's.** Attaching
   `Referer: https://www.google.com/` — the natural thing to do right after scraping a
   Google results page — trips hotlink protection. Measured 2026-07-27: 403 on
   cdn.sexxxgif.com, cdn.nsfwgify.com, porngif.co, cdn.xgifer.com and cdn.hardcoregify.com;
   200 on all of them with no referer or their own origin. It killed 13 of 29 fetches in
   one run and presents as "those hosts are down".

2. **Kill STALLS, not slow files — these are different, and confusing them costs
   candidates.** urllib's `timeout=` applies per read operation, so it is exactly a stall
   detector: it fires when no bytes arrive for that long. That is the gate you want, and
   `--timeout` owns it. The separate `--deadline` is only a runaway backstop and is
   deliberately generous.

   This was measured the hard way. A flat 20s wall-clock cap looked reasonable and threw
   away good clips: `101534-sultry-bj-on-knees.gif` is **6.6 MB and takes 36.8s at
   0.18 MB/s — with a longest gap between chunks of 4.9s.** It never stalls; it is just
   big on a slow host. A deadline tight enough to kill hangs is far too tight for honest
   large files, so the two jobs get two knobs.

**On `--workers`:** default 3, and deliberately modest. These CDNs throttle concurrency —
measured at 8 workers, per-file time went 7.8s -> 34.1s for only ~1.5x total throughput,
and five benchmarks across one afternoon disagreed with each other (0.8x - 2.6x). Treat
concurrency as a hedge against a stalled straggler, NOT as a speed feature. Do not raise
this number on the strength of one good measurement; see the "network timing is weather"
box in references/chrome_route.md.

Usage (wave 1, then top-up only if the shelf comes up short):

    fetch_candidates.py --game media_lab --file scenes/lab_eyecontact_t5.webm \
        --want eyecontact,kneeling,on-knees --avoid facial,cum --top 8
    fetch_candidates.py --game media_lab --file scenes/lab_eyecontact_t5.webm \
        --want eyecontact,kneeling,on-knees --avoid facial,cum --more

Exit codes: 0 ok, 1 nothing fetched, 2 usage/resolution error, 3 unused (no optional deps).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.request
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

CHUNK = 256 * 1024
MAX_BYTES = 200 * 1024 * 1024      # nothing we want is this big; guards a runaway stream
MIN_BYTES = 1024                   # fetch sanity: below this it is an error page, not media
KNOWN_EXTS = (".mp4", ".webm", ".mov", ".mkv", ".jpg", ".jpeg", ".png", ".webp", ".gif")


def rank(url: str, want: list[str], avoid: list[str]) -> int:
    """Score a candidate URL by what its slug claims about the beat.

    A slug is a TERM MINE and worth ZERO as a correctness claim — `back-alley-slut.gif`
    turned out to be a woman flashing on a lit street, and `three-men-fuck-one-woman.gif`
    showed two. So this only decides FETCH ORDER; the frame strip decides truth.
    """
    slug = url.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
    words = re.split(r"[-_]+", slug)
    descriptive = sum(1 for w in words if len(w) > 2 and not w.isdigit()) >= 2
    score = 0
    for kw in want:
        if kw in slug:
            score += 10
    for kw in avoid:
        # `avoid` may name a HOST as well as a slug word (e.g. shutterstock for watermarks)
        if kw in slug or kw in url.lower():
            score -= 25
    if descriptive:
        score += 3
    # tube-site hover previews are sampled from a full video, not authored loops
    if "preview" in slug and url.endswith(".mp4"):
        score -= 4
    return score


def ext_for(url: str) -> str:
    low = url.lower()
    return next((e for e in KNOWN_EXTS if low.endswith(e)), ".gif")


def fetch_one(url: str, dest: Path, socket_timeout: float, deadline: float) -> tuple[int | None, str]:
    """Download one URL to dest. Returns (bytes_written, reason)."""
    parsed = urlparse(url)
    req = urllib.request.Request(url, headers={
        "User-Agent": BROWSER_UA,
        # own origin — see module docstring, lesson 1
        "Referer": f"{parsed.scheme}://{parsed.hostname}/",
    })
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=socket_timeout) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            parts: list[bytes] = []
            total = 0
            while True:
                # wall-clock guard: the socket timeout above cannot do this job
                if time.monotonic() - started > deadline:
                    return None, f"DEADLINE>{deadline:g}s"
                block = resp.read(CHUNK)
                if not block:
                    break
                parts.append(block)
                total += len(block)
                if total > MAX_BYTES:
                    return None, "TOOBIG"
            data = b"".join(parts)
    except Exception as exc:  # noqa: BLE001 — every failure is just "drop this candidate"
        return None, f"ERR {type(exc).__name__}"

    if len(data) < MIN_BYTES:
        return None, f"TINY {len(data)}B"
    head = data[:64].lstrip().lower()
    if "text/html" in content_type or head.startswith(b"<!doctype") or head.startswith(b"<html"):
        return None, "HTML"

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data), "ok"


def load_shelf(games_root: Path, game: str, file_: str) -> list[str]:
    path = games_root / game / ".find-media" / "media_options.json"
    if not path.exists():
        raise SystemExit(f"ERROR: no options store at {path} — has the Chrome route stocked this game yet?")
    data = json.loads(path.read_text(encoding="utf-8"))
    options = data.get("options", {})
    if file_ not in options:
        known = "\n  ".join(sorted(options)[:12]) or "(none)"
        raise SystemExit(f"ERROR: slot {file_!r} not in the options store. Known slots:\n  {known}")
    # http(s) only: `origin: previous` entries are local /games/... paths, already on disk
    return [o["url"] for o in options[file_] if str(o.get("url", "")).startswith("http")]


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch stocked candidates for one media slot.")
    ap.add_argument("--game", required=True)
    ap.add_argument("--file", required=True, dest="file_",
                    help="the slot's TOML-declared path, verbatim, e.g. scenes/alley_bj_t5.webm")
    ap.add_argument("--want", default="", help="comma-separated slug keywords to prefer")
    ap.add_argument("--avoid", default="", help="comma-separated slug/host keywords to penalise")
    ap.add_argument("--top", type=int, default=8, help="how many to land this wave (default 8)")
    ap.add_argument("--more", action="store_true",
                    help="wave 2: skip URLs already fetched, keep numbering going")
    ap.add_argument("--workers", type=int, default=3,
                    help="concurrent fetches (default 3 — a hedge, not a speed feature)")
    ap.add_argument("--max-tries", type=int, default=0, dest="max_tries",
                    help="stop after this many attempts even if short (default: 4x --top). "
                         "Guards against walking a 140-deep shelf when the network is down.")
    ap.add_argument("--timeout", type=float, default=10.0,
                    help="STALL gate: abort if no bytes arrive for this long (default 10s). "
                         "This is the real gate — a healthy 6.6MB file showed a 4.9s worst gap.")
    ap.add_argument("--deadline", type=float, default=120.0,
                    help="runaway backstop on total time (default 120s). Deliberately generous: "
                         "a genuine 6.6MB file took 36.8s at 0.18MB/s. Use --timeout to kill hangs.")
    ap.add_argument("--out-dir", type=Path, dest="out_dir", default=None)
    ap.add_argument("--games-root", type=Path, dest="games_root", default=Path("games"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.top < 1 or args.workers < 1:
        print("ERROR: --top and --workers must be >= 1", file=sys.stderr)
        return 2

    item = PurePosixPath(args.file_).stem
    out_dir = args.out_dir or Path("/tmp/fm") / item
    manifest_path = out_dir / "manifest.json"

    want = [w.strip().lower() for w in args.want.split(",") if w.strip()]
    avoid = [w.strip().lower() for w in args.avoid.split(",") if w.strip()]

    try:
        urls = load_shelf(args.games_root, args.game, args.file_)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2

    existing: list[dict] = []
    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    if not args.more:
        existing = []          # wave 1 owns the directory's numbering

    already = {e["url"] for e in existing}
    next_index = max((int(Path(e["name"]).stem) for e in existing), default=-1) + 1

    pool = [u for u in urls if u not in already]
    pool.sort(key=lambda u: -rank(u, want, avoid))

    out_dir.mkdir(parents=True, exist_ok=True)

    kept: list[dict] = []
    dead: list[tuple[str, str]] = []
    tried = 0
    cursor = 0
    # Chunked so we over-fetch by at most (workers-1): submit a slice, then walk its
    # results in RANK order — completion order must never decide what the human sees first.
    max_tries = args.max_tries if args.max_tries > 0 else args.top * 4
    while len(kept) < args.top and cursor < len(pool) and tried < max_tries:
        need = args.top - len(kept)
        chunk = pool[cursor:cursor + max(need, args.workers)]
        cursor += len(chunk)
        tried += len(chunk)
        staged = [(u, out_dir / f".staging-{i:03d}{ext_for(u)}") for i, u in enumerate(chunk)]
        if args.workers == 1:
            results = [fetch_one(u, p, args.timeout, args.deadline) for u, p in staged]
        else:
            with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
                results = list(ex.map(
                    lambda sp: fetch_one(sp[0], sp[1], args.timeout, args.deadline), staged))
        for (url, staging), (size, why) in zip(staged, results):
            if size and len(kept) < args.top:
                final = out_dir / f"{next_index + len(kept):02d}{staging.suffix}"
                staging.replace(final)
                kept.append({"name": final.name, "url": url, "bytes": size})
            else:
                staging.unlink(missing_ok=True)
                if size:
                    dead.append((url, "surplus (shelf already full this wave)"))
                else:
                    dead.append((url, why))

    manifest = existing + kept
    manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")

    if args.json:
        print(json.dumps({
            "item": item, "out_dir": str(out_dir), "wave": "more" if args.more else "first",
            "fetched": len(kept), "tried": tried, "dead": len(dead),
            "total_on_disk": len(manifest),
            "kept": kept,
            "dead_detail": [{"url": u, "reason": r} for u, r in dead],
        }, indent=2))
    else:
        wave = "wave 2 (--more)" if args.more else "wave 1"
        print(f"=== {item}: {wave} — fetched {len(kept)}/{tried} tried, "
              f"{len(dead)} dead, {len(manifest)} on disk")
        if len(kept) < args.top and tried >= max_tries:
            print(f"  ⚠️  stopped at the {max_tries}-attempt cap, still {args.top - len(kept)} short — "
                  f"network trouble or a thin shelf. Re-run --more, or run a sibling query.")
        for k in kept:
            print(f"  {k['name']}  {k['bytes'] // 1024:5d}KB  {k['url']}")
        if dead:
            print("  -- dead --")
            for u, why in dead[:12]:
                print(f"     {why:22s} {u}")
            if len(dead) > 12:
                print(f"     ... and {len(dead) - 12} more")
        print(f"  manifest: {manifest_path}")

    return 0 if kept else 1


if __name__ == "__main__":
    sys.exit(main())
