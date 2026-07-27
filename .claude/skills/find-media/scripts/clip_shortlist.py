#!/usr/bin/env python3
"""
clip_shortlist.py — local CLIP pre-ranking + labeled montage for find-media JUDGE

Embeds every candidate image with openai/clip-vit-base-patch32, ranks by cosine
similarity to a text caption, prints the ranked list as JSON, and writes ONE
labeled contact-sheet montage of the top-K. The LLM then does a SINGLE Read on
that montage instead of viewing ~15 thumbnails one by one.

CLIP is a PRE-FILTER, never the decider. Demo evidence:
  SFW: top-1 60% / top-3 88% — a strong shortlister.
  NSFW act-judging: 25-31% — CANNOT pick the act → use it as a COARSE CULL only
  (caption the cull on SETTING + people, NOT the act; let the LLM judge the act).
Caption policy: feed the validated SEARCH QUERY, never narrative prose (60 vs 32%).

Runs ONLY where torch/transformers/PIL are importable and the model is cached —
that is the GLOBAL Framework python on this machine, not the django venv. Invoke
via the explicit interpreter (see SKILL.md): set FIND_MEDIA_PY or rely on the
hard-coded default. If deps/model are unavailable it exits 3 so the caller can
fall back to direct thumbnail viewing — it never crashes a run.

Usage:
    clip_shortlist.py --candidates-dir <dir> --caption "<query>" --top-k 5 \
        --montage-out <evidence>/<item>/montage_shortlist.jpg [--item-id <id>] \
        [--grid-cols 5] [--tile-px 256] [--device auto] [--json]
    clip_shortlist.py --manifest <candidates.jsonl> --caption "<query>" ...

Exit codes:
    0  success (>=1 candidate ranked, montage written)
    1  no candidate images found
    2  invalid arguments
    3  CLIP/torch/transformers/PIL unavailable OR model not cached → caller FALLS
       BACK to direct thumbnail evaluation (prints a notice; does not crash)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Pin offline BEFORE transformers is imported: the model is already cached, so we
# never want a surprise network fetch mid-run. A missing cache then raises cleanly
# and we map it to exit 3 (fall back) rather than a multi-minute silent download.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

MODEL = "openai/clip-vit-base-patch32"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MONTAGE_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@dataclass
class Ranked:
    rank: int
    id: str
    path: str
    score: float
    montage_label: str | None


def _fallback(msg: str, as_json: bool) -> int:
    if as_json:
        print(json.dumps({"passed": False, "exit": 3, "error": msg}))
    else:
        print(f"[CLIP-UNAVAILABLE] {msg}\n"
              "  → fall back to direct thumbnail evaluation (Read each candidate). "
              "Install torch on the Framework python or set FIND_MEDIA_PY to enable.",
              file=sys.stderr)
    return 3


def candidate_id(path: Path) -> str:
    """Recover a stable id. Harvest/rep frames are '<i>_<gifId>' → gifId."""
    stem = path.stem
    m = re.match(r"^\d+_(.+)$", stem)
    return m.group(1) if m else stem


def load_candidates(args) -> list[tuple[str, Path]]:
    """Return [(id, image_path)] from a dir or a candidates.jsonl manifest."""
    out: list[tuple[str, Path]] = []
    if args.candidates_dir is not None:
        for p in sorted(args.candidates_dir.iterdir()):
            if p.suffix.lower() in IMAGE_EXTS:
                out.append((candidate_id(p), p))
    else:
        with args.manifest.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                raw = (rec.get("frame_path") or rec.get("thumbnail_path")
                       or rec.get("local_path") or rec.get("path"))
                if not raw:
                    continue
                p = Path(raw)
                if p.exists() and p.suffix.lower() in IMAGE_EXTS:
                    out.append((str(rec.get("id") or candidate_id(p)), p))
    return out


def build_montage(ranked: list[Ranked], id_to_path: dict[str, Path],
                  out_path: Path, caption: str, item_id: str,
                  cols: int, tile_px: int) -> None:
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        hfont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except OSError:
        font = hfont = ImageFont.load_default()

    shown = [r for r in ranked if r.montage_label]
    band = 26
    header = 44
    rows = (len(shown) + cols - 1) // cols
    W, H = cols * tile_px, header + rows * (tile_px + band)
    sheet = Image.new("RGB", (W, H), (15, 15, 15))
    dr = ImageDraw.Draw(sheet)
    dr.text((6, 4), f"{item_id}  |  caption: {caption}"[:120], fill=(255, 255, 0), font=hfont)

    for k, r in enumerate(shown):
        rr, cc = divmod(k, cols)
        x, y = cc * tile_px, header + rr * (tile_px + band)
        try:
            im = Image.open(id_to_path[r.id]).convert("RGB")
            im.thumbnail((tile_px, tile_px))
            sheet.paste(im, (x + (tile_px - im.width) // 2, y + (tile_px - im.height) // 2))
        except Exception:
            dr.rectangle([x, y, x + tile_px, y + tile_px], outline=(80, 80, 80))
        ly = y + tile_px
        dr.rectangle([x, ly, x + tile_px, ly + band], fill=(0, 0, 0))
        dr.text((x + 4, ly + 4), f"{r.montage_label}  {r.id[:16]}  {r.score:.3f}",
                fill=(0, 255, 0), font=font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=85)


def main() -> int:
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--candidates-dir", type=Path, dest="candidates_dir")
    src.add_argument("--manifest", type=Path)
    p.add_argument("--caption", required=True)
    p.add_argument("--montage-out", type=Path, dest="montage_out", required=True)
    p.add_argument("--top-k", type=int, default=5, dest="top_k")
    p.add_argument("--item-id", default="", dest="item_id")
    p.add_argument("--grid-cols", type=int, default=5, dest="grid_cols")
    p.add_argument("--tile-px", type=int, default=256, dest="tile_px")
    p.add_argument("--device", choices=["auto", "mps", "cpu"], default="auto")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    candidates = load_candidates(args)
    if not candidates:
        if args.json:
            print(json.dumps({"passed": False, "exit": 1, "error": "no candidate images found"}))
        else:
            print("[EMPTY] no candidate images found — re-harvest or broaden the query", file=sys.stderr)
        return 1

    # Deps + model load are the only places we can hit exit-3 (fall back).
    try:
        import torch
        from PIL import Image
        from transformers import CLIPModel, CLIPProcessor
    except ImportError as e:
        return _fallback(f"import failed: {e}", args.json)

    device = args.device
    if device == "auto":
        device = "mps" if torch.backends.mps.is_available() else "cpu"

    try:
        model = CLIPModel.from_pretrained(MODEL).to(device).eval()
        proc = CLIPProcessor.from_pretrained(MODEL)
    except OSError as e:
        return _fallback(f"model '{MODEL}' not cached ({e})", args.json)

    ids = [c[0] for c in candidates]
    paths = [c[1] for c in candidates]
    try:
        imgs = [Image.open(p).convert("RGB") for p in paths]
    except Exception as e:  # noqa: BLE001 — a bad file shouldn't crash the run
        return _fallback(f"could not open candidate image: {e}", args.json)

    with torch.no_grad():
        ie = model.get_image_features(**proc(images=imgs, return_tensors="pt").to(device))
        te = model.get_text_features(
            **proc(text=[args.caption], return_tensors="pt", padding=True, truncation=True).to(device))
    ie = torch.nn.functional.normalize(ie, dim=1)
    te = torch.nn.functional.normalize(te, dim=1)
    sims = (te @ ie.T).squeeze(0).float().cpu().tolist()

    order = sorted(range(len(candidates)), key=lambda i: sims[i], reverse=True)
    k = min(args.top_k, len(order))
    ranked: list[Ranked] = []
    for rank, i in enumerate(order):
        label = MONTAGE_LABELS[rank] if rank < k and rank < len(MONTAGE_LABELS) else None
        ranked.append(Ranked(rank=rank + 1, id=ids[i], path=str(paths[i]),
                             score=round(sims[i], 4), montage_label=label))

    build_montage(ranked, dict(zip(ids, paths)), args.montage_out,
                  args.caption, args.item_id or "(item)", args.grid_cols, args.tile_px)

    payload = {
        "item_id": args.item_id, "caption": args.caption, "model": "clip-vit-base-patch32",
        "device": device, "candidate_count": len(candidates), "top_k": k,
        "montage_path": str(args.montage_out),
        "ranked": [asdict(r) for r in ranked],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"[OK] ranked {len(candidates)} candidates on {device}; montage → {args.montage_out}")
        print(f"  caption: {args.caption!r}  (top-{k} labeled A..{MONTAGE_LABELS[k-1]})")
        for r in ranked[:k]:
            print(f"  {r.montage_label}  rank{r.rank:>2}  score {r.score:.3f}  id={r.id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
