"""Record LO's yes against the exact text of a piece card, and report a card's approval status.

    python3 approve.py games/<slug> <id> "<LO's exact words>" [--date YYYY-MM-DD]

The yes is stored in games/<slug>/approvals.json with a sha256 of the raw bytes of
games/<slug>/cards/<id>.md. The file is append-only: a re-approved card gets a new record,
and the newest record for an id is the one that counts.

The limit, said plainly: this proves a yes was recorded against this exact card text.
It cannot prove LO typed it. The words are copied from chat by the session.

build.py and check.py import status() from here, so the rule lives in one place.
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

LIMIT = (
    "A record here proves a yes was recorded against this exact card text. "
    "It cannot prove LO typed it: the words are copied from chat by the session."
)


def card_path(game_dir, card_id):
    return Path(game_dir) / "cards" / f"{card_id}.md"


def card_hash(game_dir, card_id):
    """sha256 of the card file's raw bytes, or None when the card is missing."""
    path = card_path(game_dir, card_id)
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(game_dir):
    path = Path(game_dir) / "approvals.json"
    if not path.is_file():
        return {"limit": LIMIT, "approvals": []}
    return json.loads(path.read_text(encoding="utf-8"))


def latest(game_dir, card_id):
    """The newest approval record for a card, or None."""
    records = [r for r in load(game_dir)["approvals"] if r["card"] == card_id]
    return records[-1] if records else None


def status(game_dir, card_id):
    """'approved' when the newest record matches the card's current hash,
    'changed' when the card was edited after its last yes, 'missing' otherwise."""
    record = latest(game_dir, card_id)
    current = card_hash(game_dir, card_id)
    if record is None or current is None:
        return "missing"
    return "approved" if record["sha256"] == current else "changed"


def approve(game_dir, card_id, words, date=None):
    """Append one approval record. Returns a one-line message; raises SystemExit on refusal."""
    words = (words or "").strip()
    if not words:
        raise SystemExit("refused: LO's words are empty. Copy his exact reply.")
    current = card_hash(game_dir, card_id)
    if current is None:
        raise SystemExit(f"refused: no card at {card_path(game_dir, card_id)}")
    record = latest(game_dir, card_id)
    if record is not None and record["sha256"] == current:
        return f"no change: {card_id} is already approved at this exact text"
    data = load(game_dir)
    data["limit"] = LIMIT
    data["approvals"].append({
        "card": card_id,
        "sha256": current,
        "words": words,
        "date": date or datetime.date.today().isoformat(),
    })
    out = {"limit": data["limit"], "approvals": data["approvals"]}
    (Path(game_dir) / "approvals.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return f"approved: {card_id} sha256 {current[:12]}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Record LO's yes against a piece card's hash.")
    parser.add_argument("game_dir")
    parser.add_argument("card_id")
    parser.add_argument("words")
    parser.add_argument("--date")
    args = parser.parse_args(argv)
    print(approve(args.game_dir, args.card_id, args.words, args.date))


if __name__ == "__main__":
    sys.exit(main())
