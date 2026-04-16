#!/usr/bin/env python3
"""
dedup_tracker.py — prevent the same asset from being used twice

Tracks used GIF IDs / URLs per game (and optionally globally across all games).
Reading immersion breaks when the same PornHub clip appears in two scenes.

State lives in:
    games/<game>/.find-media/used_assets.jsonl     (per-game)
    ~/.find-media/used_global.jsonl                (optional global, opt-in)

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
import sys
from datetime import datetime, timezone
from pathlib import Path


def game_state_path(game: str) -> Path:
    return Path(f"games/{game}/.find-media/used_assets.jsonl")


def global_state_path() -> Path:
    return Path.home() / ".find-media" / "used_global.jsonl"


def normalize_asset_id(asset_id: str) -> str:
    """Normalize the asset ID so variations of the same asset dedup correctly.

    PornHub GIF URLs have signed time-limited query strings. Strip those.
    GIF IDs (bare integers) pass through.
    URLs for other sources get SHA-256 hashed so they're comparable.
    """
    asset_id = asset_id.strip()

    if asset_id.isdigit():
        return f"ph_gif:{asset_id}"

    if "pornhub.com/gif/" in asset_id:
        part = asset_id.split("pornhub.com/gif/")[1].split("?")[0].split("/")[0]
        return f"ph_gif:{part}"

    if asset_id.startswith(("http://", "https://")):
        base = asset_id.split("?")[0]
        digest = hashlib.sha256(base.encode()).hexdigest()[:16]
        return f"url:{digest}"

    return f"raw:{asset_id}"


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
            if entry.get("normalized_id") == normalized:
                return True, entry
    return False, None


def record(asset_id: str, game: str, item: str, source: str, also_global: bool) -> dict:
    entry = {
        "normalized_id": normalize_asset_id(asset_id),
        "raw_id": asset_id,
        "game": game,
        "item_id": item,
        "source": source,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    append_jsonl(game_state_path(game), entry)
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
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    paths = [game_state_path(args.game)]
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
        new_entry = record(args.record, args.game, args.item, args.source, args.use_global)
        if args.json:
            print(json.dumps({"recorded": True, "entry": new_entry}))
        else:
            print(f"[OK] recorded {args.record} → {new_entry['normalized_id']}")
        return 0

    if args.list:
        entries = read_jsonl(game_state_path(args.game))
        if args.json:
            print(json.dumps(entries, indent=2))
        else:
            print(f"{len(entries)} used assets for game={args.game}:")
            for e in entries:
                print(f"  {e['normalized_id']:40s}  item={e.get('item_id', '-')}  src={e.get('source', '-')}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
