#!/usr/bin/env python3
"""
dedup_tracker.py — prevent the same asset from being used twice

Tracks used GIF IDs / URLs per game (and optionally globally across all games).
Reading immersion breaks when the same clip appears in two scenes.

State lives in:
    <repo>/games/<game>/.find-media/used_assets.jsonl   (per-game)
    ~/.find-media/used_global.jsonl                     (optional global, opt-in)

<repo> is resolved from this file's location, not the caller's cwd — override with
--games-root. Ledger rows are tolerated in any historical shape (see row_identity).

Usage:
    # Check if an asset is already used
    python dedup_tracker.py --check <asset_id> --game <game> [--global]

    # Record a newly-downloaded asset
    python dedup_tracker.py --record <asset_id> --game <game> --item <item_id> --source <src> [--global]

    # List all used assets for a game
    python dedup_tracker.py --list --game <game>

Exit codes (for --check):
    0  asset is NOT used (safe to download)
    1  asset IS already used (skip it)
    2  invalid arguments
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# The skill gets invoked from a subagent, from the review UI's cwd, from a game dir —
# a RELATIVE "games/<game>/..." path silently resolves against whatever cwd the caller
# happened to have and reads/writes a DIFFERENT ledger, which reads as "0 used assets"
# and re-ships clips. Anchor to the repo this skill lives in instead.
# scripts/ → find-media/ → skills/ → .claude/ → <repo root>
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_GAMES_ROOT = REPO_ROOT / "games"

# Ledger rows have been written by three different hands over the project's life, so a
# row may carry any of these instead of `normalized_id`. Order matters: `gif_id` names
# its own meaning, a bare `id` does not (see row_identity).
LEGACY_ID_FIELDS = ("gif_id", "raw_id", "asset_id", "url")
# Sources whose bare integer ids ARE PornHub gif ids.
PH_SOURCES = {"pornhub", "pornhub_gif", "phncdn", "ph"}

# Matches the gif id in any CDN path shaped /gif/<digits>. `\d+` stops at the first
# non-digit, so the `.gif` extension and any query string fall off for free.
CDN_GIF_PATH_RE = re.compile(r"/gif/(\d+)")

# The prefixes this function emits — used to make it idempotent.
NORMALIZED_PREFIXES = ("ph_gif:", "url:", "raw:")


def game_state_path(game: str, games_root: Path | None = None) -> Path:
    return (games_root or DEFAULT_GAMES_ROOT) / game / ".find-media" / "used_assets.jsonl"


def global_state_path() -> Path:
    return Path.home() / ".find-media" / "used_global.jsonl"


def normalize_asset_id(asset_id: str) -> str:
    """Normalize the asset ID so variations of the same asset dedup correctly.

    PornHub GIF URLs have signed time-limited query strings. Strip those.
    GIF IDs (bare integers) pass through.
    URLs for other sources get SHA-256 hashed so they're comparable.
    Idempotent — feeding an already-normalized id back in returns it unchanged.
    """
    asset_id = asset_id.strip()

    # Idempotence, and unwrap the double-normalized case: 22 vesper rows were recorded
    # by passing an id that had ALREADY been through this function, so they landed as
    # `raw:ph_gif:<id>` — a shape no lookup can ever match, leaving those clips silently
    # re-selectable. Each unwrap strips one `raw:`, so the recursion terminates.
    if asset_id.startswith(NORMALIZED_PREFIXES):
        inner = asset_id.split(":", 1)[1]
        if asset_id.startswith("raw:") and inner.startswith(NORMALIZED_PREFIXES):
            return normalize_asset_id(inner)
        return asset_id

    if asset_id.isdigit():
        return f"ph_gif:{asset_id}"

    if "pornhub.com/gif/" in asset_id:
        part = asset_id.split("pornhub.com/gif/")[1].split("?")[0].split("/")[0]
        return f"ph_gif:{part}"

    if asset_id.startswith(("http://", "https://")):
        # Direct-CDN gifs (https://egl.phncdn.com/gif/20158111.gif) carry the SAME gif
        # id as the pornhub.com/gif/<id> page URL but not the literal the branch above
        # matches, so they used to fall through to the url:<sha> branch and collide with
        # nothing — every already-used clip looked fresh. Checked AFTER the pornhub
        # branch so no existing ph_gif: record changes identity.
        m = CDN_GIF_PATH_RE.search(asset_id.split("?")[0])
        if m:
            return f"ph_gif:{m.group(1)}"
        base = asset_id.split("?")[0]
        digest = hashlib.sha256(base.encode()).hexdigest()[:16]
        return f"url:{digest}"

    return f"raw:{asset_id}"


def row_identity(entry: dict) -> str | None:
    """The normalized id for a ledger row, tolerating hand-written rows.

    22 of vesper's 227 rows were written by hand with a bare `gif_id` and no
    `normalized_id` at all, so a strict `entry["normalized_id"]` lookup could not see
    them and those 22 clips stayed silently re-selectable. Fall back to normalizing
    whatever id-ish field the row does carry.
    """
    nid = entry.get("normalized_id")
    if nid:
        # Re-normalized, not returned verbatim — 22 rows are stored double-normalized
        # (`raw:ph_gif:<id>`) and normalize_asset_id unwraps that shape.
        return normalize_asset_id(str(nid))

    for field_name in LEGACY_ID_FIELDS:
        value = entry.get(field_name)
        if value:
            return normalize_asset_id(str(value))

    # A bare `id` is source-dependent — PornHub gif ids and Pexels photo ids are both
    # plain integers — so only read it as a gif id when the row says so, otherwise a
    # Pexels photo id would block a same-numbered gif.
    value = entry.get("id")
    if value:
        value = str(value)
        if value.isdigit() and str(entry.get("source", "")).lower() not in PH_SOURCES:
            return f"raw:{value}"
        return normalize_asset_id(value)

    return None


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def is_used(asset_id: str, paths: list[Path]) -> tuple[bool, dict | None]:
    normalized = normalize_asset_id(asset_id)
    for p in paths:
        for entry in read_jsonl(p):
            if row_identity(entry) == normalized:
                return True, entry
    return False, None


def record(asset_id: str, game: str, item: str, source: str, also_global: bool,
           games_root: Path | None = None) -> dict:
    entry = {
        "normalized_id": normalize_asset_id(asset_id),
        "raw_id": asset_id,
        "game": game,
        "item_id": item,
        "source": source,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    append_jsonl(game_state_path(game, games_root), entry)
    if also_global:
        append_jsonl(global_state_path(), entry)
    return entry


def main() -> int:
    p = argparse.ArgumentParser()
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--check", metavar="ASSET_ID")
    grp.add_argument("--record", metavar="ASSET_ID")
    grp.add_argument("--list", action="store_true")

    p.add_argument("--game", required=True)
    p.add_argument("--item", default="")
    p.add_argument("--source", default="unknown")
    p.add_argument("--global", dest="use_global", action="store_true",
                   help="Also check or write the global used-assets list")
    p.add_argument("--games-root", type=Path, default=None, dest="games_root",
                   help=f"Override the games/ dir (default: {DEFAULT_GAMES_ROOT})")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    paths = [game_state_path(args.game, args.games_root)]
    if args.use_global:
        paths.append(global_state_path())

    if args.check:
        used, entry = is_used(args.check, paths)
        if args.json:
            print(json.dumps({"used": used, "entry": entry}))
        else:
            if used:
                assert entry is not None
                print(f"[USED] {args.check} — already used in game={entry.get('game')} "
                      f"item={entry.get('item_id')} on {entry.get('recorded_at')}")
            else:
                print(f"[FREE] {args.check} — safe to use")
        return 1 if used else 0

    if args.record:
        used, entry = is_used(args.record, paths)
        if used:
            if args.json:
                print(json.dumps({"recorded": False, "already_used": True, "entry": entry}))
            else:
                assert entry is not None
                print(f"[SKIP] {args.record} — already recorded for {entry.get('item_id')}")
            return 1
        new_entry = record(args.record, args.game, args.item, args.source,
                           args.use_global, args.games_root)
        if args.json:
            print(json.dumps({"recorded": True, "entry": new_entry}))
        else:
            print(f"[OK] recorded {args.record} → {new_entry['normalized_id']}")
        return 0

    if args.list:
        entries = read_jsonl(game_state_path(args.game, args.games_root))
        if args.json:
            print(json.dumps(entries, indent=2))
        else:
            print(f"{len(entries)} used assets for game={args.game}:")
            for e in entries:
                # row_identity, not e["normalized_id"] — hand-written rows don't have it
                # and a KeyError here used to kill the whole listing.
                ident = row_identity(e) or "(no id field)"
                item = e.get("item_id") or e.get("item") or "-"
                print(f"  {ident:40s}  item={item}  src={e.get('source', '-')}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
