#!/usr/bin/env python3
"""Every built piece gets played: by Claude in Chrome as it lands, by LO before a release.

Added 2026-11-02, reshaped the same day on LO's call: "both, but don't want development to be
blocked by it." Nothing here stops anyone building. The only hold is at a release:
`release_upload.py` and the pre-commit ship check refuse a public (non-dev) build while any
piece has no play note from LO. LO's own ten minutes of play found more than every gate
(2026-10-08), so a release must not go out unplayed by him.

    pieces.py done    <slug> <piece-id> "<what the piece holds>"
        Records the piece in v2_state.json build.pieces[]. Development carries on.

    pieces.py chrome  <slug> <piece-id> "<what the Chrome play found>"
        The building session plays the piece itself in Claude in Chrome (the dev build:
        does it fire, is every line true, can she climb) and records what it found. Taste,
        "is it hot", is LO's call, not this note's.

    pieces.py played  <slug> <piece-id | --all> "<LO's own words>"
        LO's play note. --all puts one note on every piece that has none (LO played the
        release as a whole). The note must be LO's words; "skipped by LO: <reason>" is how a
        skip is said out loud. Each note also goes on a line under "## Play notes" in
        DECISIONS.md.

    pieces.py status        <slug>  every piece, with its Chrome and LO notes
    pieces.py release-check <slug>  exits 1 while any piece has no LO note (the release hold)

The ledger is written back in its own format (indent 2, UTF-8, trailing newline).
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

PLAY_SECTION = "## Play notes"

CHROME_CHECKS = (
    "Does it happen? Every step and scene in the piece fires when it should, once.",
    "Is it true? No line names clothes she isn't wearing, a time it isn't, or a past that "
    "hasn't happened.",
    "Can she climb? There is a choice at her current stage that raises her meter.",
)
LO_CHECK = "Is it hot? At each step something happens to her body, not only talk. (LO's call.)"


def game_dir(slug: str, root: str = REPO) -> str:
    return os.path.join(root, "games", slug)


def _state_path(slug: str, root: str) -> str:
    return os.path.join(game_dir(slug, root), "v2_state.json")


def load_state(slug: str, root: str = REPO) -> dict:
    with open(_state_path(slug, root), encoding="utf-8") as fh:
        return json.load(fh)


def save_state(slug: str, state: dict, root: str = REPO) -> None:
    path = _state_path(slug, root)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def pieces_of(state: dict) -> list:
    return ((state.get("build") or {}).get("pieces")) or []


def unplayed_by_lo(slug: str, root: str = REPO) -> list:
    """Pieces with no play note from LO. A game with no ledger or no pieces has none."""
    if not os.path.exists(_state_path(slug, root)):
        return []
    return [p for p in pieces_of(load_state(slug, root)) if not p.get("played")]


def _now() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def _piece(state: dict, slug: str, piece_id: str) -> dict:
    match = [p for p in pieces_of(state) if p.get("id") == piece_id]
    if not match:
        raise SystemExit(f"no piece {piece_id!r} in {slug}'s ledger")
    return match[0]


def _append_play_note(slug: str, line: str, root: str) -> None:
    path = os.path.join(game_dir(slug, root), "DECISIONS.md")
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if PLAY_SECTION not in text:
        sep = "" if not text or text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        text += f"{sep}{PLAY_SECTION}\n\nOne line per play of a built piece, written by `pieces.py`.\n\n"
    # The new line goes at the end of the Play notes section, before the next heading.
    after = text.index(PLAY_SECTION) + len(PLAY_SECTION)
    nxt = re.search(r"^## ", text[after:], re.M)
    cut = after + nxt.start() if nxt else len(text)
    head = text[:cut].rstrip("\n")
    # A list line follows the last list line directly; the first one follows a blank line.
    joint = "\n" if head.splitlines()[-1].startswith("- ") else "\n\n"
    text = head + joint + line + "\n" + ("\n" + text[cut:] if nxt else "")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def done(slug: str, piece_id: str, what: str, root: str = REPO) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", piece_id):
        raise SystemExit(f"piece id must be lowercase letters, digits, - or _: {piece_id!r}")
    if not what.strip():
        raise SystemExit("say what the piece holds, in one line")
    state = load_state(slug, root)
    pieces = state.setdefault("build", {}).setdefault("pieces", [])
    if any(p.get("id") == piece_id for p in pieces):
        raise SystemExit(f"piece {piece_id!r} is already recorded; pick a new id")
    pieces.append({"id": piece_id, "what": what.strip(), "built_at": _now(),
                   "chrome": None, "played": None})
    save_state(slug, state, root)
    return "\n".join([
        f"Recorded piece {piece_id!r} of {slug}: {what.strip()}. Development is not blocked.",
        "",
        "Next, play it yourself in Claude in Chrome on the dev build "
        f"(games/{slug}/output/index.html), using the dev jumps to reach the piece:",
        *[f"  {i}. {c}" for i, c in enumerate(CHROME_CHECKS, 1)],
        "Then record what you found, fix what is broken, and tell LO in one line:",
        f'  python3 .claude/skills/author-game-v2/scripts/pieces.py chrome {slug} {piece_id} "<what you found>"',
        "",
        f"LO plays before the release: {LO_CHECK}",
    ])


def chrome(slug: str, piece_id: str, report: str, root: str = REPO) -> str:
    report = report.strip()
    if not report:
        raise SystemExit("an empty Chrome report is refused: say what fired, what was false, the climb")
    state = load_state(slug, root)
    piece = _piece(state, slug, piece_id)
    at = _now()
    piece["chrome"] = {"at": at, "report": report}   # a replay replaces the last report
    save_state(slug, state, root)
    _append_play_note(slug, f'- {at[:10]} · {piece_id} · played by Claude in Chrome: "{report}"', root)
    return f"recorded the Chrome play of {piece_id!r}. LO's play before the release is still owed."


def played(slug: str, piece_id: str, note: str, root: str = REPO) -> str:
    note = note.strip()
    if not note:
        raise SystemExit("an empty play note is refused: write what LO found, in his words")
    state = load_state(slug, root)
    if piece_id == "--all":
        targets = [p for p in pieces_of(state) if not p.get("played")]
        if not targets:
            raise SystemExit(f"every piece of {slug} already has LO's note")
    else:
        targets = [_piece(state, slug, piece_id)]
        if targets[0].get("played"):
            raise SystemExit(f"piece {piece_id!r} already has LO's note ({targets[0]['played']['at']})")
    at = _now()
    for p in targets:
        p["played"] = {"at": at, "note": note}
    save_state(slug, state, root)
    ids = ", ".join(p["id"] for p in targets)
    _append_play_note(slug, f'- {at[:10]} · {ids} · played by LO: "{note}"', root)
    left = unplayed_by_lo(slug, root)
    tail = (f"still without LO's note: {', '.join(p['id'] for p in left)}" if left
            else "every piece has LO's note; the release hold is clear.")
    return f"recorded LO's note on {ids}. {tail}"


def status(slug: str, root: str = REPO) -> tuple[str, int]:
    pieces = pieces_of(load_state(slug, root))
    if not pieces:
        return f"{slug}: no pieces recorded", 0
    rows = []
    for p in pieces:
        c = (p.get("chrome") or {}).get("at") or "-"
        lo = (p.get("played") or {}).get("note") or "-"
        rows.append(f"  {p['id']:<28} built {p['built_at']}  Chrome {c:<16}  LO: {lo}")
    owed = sum(1 for p in pieces if not p.get("played"))
    return (f"{slug}: {len(pieces)} pieces, {owed} without LO's note\n" + "\n".join(rows),
            1 if owed else 0)


def release_check(slug: str, root: str = REPO) -> tuple[str, int]:
    owed = unplayed_by_lo(slug, root)
    if not owed:
        return f"{slug}: every piece has LO's play note", 0
    lines = [f"{slug}: {len(owed)} piece(s) without LO's play note. A release waits for it:"]
    lines += [f"  {p['id']}: {p['what']}" for p in owed]
    lines += ["LO plays the dev build, then:",
              f'  python3 .claude/skills/author-game-v2/scripts/pieces.py played {slug} --all "<his words>"']
    return "\n".join(lines), 1


def main(argv: list) -> int:
    cmds = {"done", "chrome", "played", "status", "release-check"}
    if len(argv) < 2 or argv[0] not in cmds:
        print(__doc__)
        return 2
    cmd, slug = argv[0], argv[1]
    if not os.path.exists(_state_path(slug, REPO)):
        print(f"no ledger: games/{slug}/v2_state.json")
        return 2
    if cmd in {"done", "chrome", "played"}:
        if len(argv) != 4:
            print(f'usage: pieces.py {cmd} <slug> <piece-id> "<text>"')
            return 2
        print({"done": done, "chrome": chrome, "played": played}[cmd](slug, argv[2], argv[3]))
        return 0
    text, code = (status if cmd == "status" else release_check)(slug)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
