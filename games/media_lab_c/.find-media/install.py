#!/usr/bin/env python3
"""install.py — put a judged pick into games/<game>/videos/, no Django required.

This session has no Django, so `POST /api/v1/dev/media-finder/grab` is unavailable.
This replicates the two rules that endpoint's target-path logic actually enforces
(api/v1/media_finder.py:451-527), and nothing else:

  1. Target is games/<game>/videos/<subfolder>/<stem>.<ext-from-SOURCE-url> — the
     extension comes from the source, NOT from what the TOML declared, because the
     renderer matches extension-agnostically.
  2. Any existing file sharing that stem is deleted first, whatever its extension,
     so the generator never sees an orphan it can't match.

The bytes are already on disk from fetch_candidates.py, so this is grab's
`local_path` branch: a copy, no network, no expiry.

Usage:  install.py <item_id> <candidate_index>
"""
import json
import pathlib
import shutil
import sys

GAME = "media_lab_c"
ROOT = pathlib.Path("games") / GAME
EVIDENCE = ROOT / ".find-media" / "evidence"


def main() -> int:
    item_id, idx = sys.argv[1], sys.argv[2].zfill(2)
    cand_dir = EVIDENCE / item_id / "candidates"
    manifest = json.loads((cand_dir / "manifest.json").read_text())

    # manifest entries carry the source url next to the local filename they produced
    entries = manifest if isinstance(manifest, list) else manifest.get("candidates", [])
    hit = next((e for e in entries if pathlib.Path(e["name"]).stem == idx), None)
    if hit is None:
        print(f"FAIL {item_id}: no manifest entry for candidate {idx}", file=sys.stderr)
        return 1

    src = cand_dir / hit["name"]
    if not src.is_file():
        print(f"FAIL {item_id}: candidate {idx} not on disk", file=sys.stderr)
        return 1

    # The slot's TOML-declared path decides the folder and the stem; the source decides the ext.
    declared = SLOT_FILE[item_id]
    subfolder = str(pathlib.PurePosixPath(declared).parent)
    stem = pathlib.PurePosixPath(declared).stem
    out_dir = ROOT / "videos" / subfolder
    out_dir.mkdir(parents=True, exist_ok=True)

    for existing in out_dir.iterdir():          # rule 2 — clear the stem, any extension
        if existing.is_file() and existing.stem == stem:
            existing.unlink()

    dest = out_dir / f"{stem}{src.suffix}"      # rule 1 — extension from the source
    shutil.copy2(src, dest)
    size = dest.stat().st_size
    print(f"{item_id:<22} <- {idx}  {size // 1024:>6}KB  {dest}")
    print(f"    url: {hit.get('url')}")
    return 0


SLOT_FILE = {
    "lab_eyecontact_t5": "scenes/lab_eyecontact_t5.webm",
    "lab_tease_t4": "scenes/lab_tease_t4.webm",
    "lab_flash_t4": "scenes/lab_flash_t4.webm",
    "lab_alley_t5": "scenes/lab_alley_t5.webm",
    "lab_finish_inside_t5": "scenes/lab_finish_inside_t5.webm",
    "lab_finish_facial_t5": "scenes/lab_finish_facial_t5.webm",
    "lab_group_t5": "scenes/lab_group_t5.webm",
    "lab_behind_t5": "scenes/lab_behind_t5.webm",
    "lab_passive_t5": "scenes/lab_passive_t5.webm",
    "lab_room": "scenes/lab_room.jpg",
}

if __name__ == "__main__":
    sys.exit(main())
