#!/usr/bin/env python3
"""Mirror games/<slug>/sheets/**.md into Notion, one board per game.

    Game Sheets (page)
      └─ Games (database)          one row per game — the list
           └─ <game> (row)
                └─ Sheets (database)   that game's sheets, its own board


Disk is authoritative for sheet content. Notion carries the review verdict back:
Status, the four-part rubric, and comments. A sheet body that changed since its
sign-off re-opens its row and voids the verdict that was given on the old body.

Design and rationale: prd_notion_sheet_review.md
Doctrine it mirrors:  .claude/skills/author-game-v2/references/the-sheets.md

    init         create (or adopt) the Games database under the parent page
    push         send sheets to Notion; re-open rows whose body moved since sign-off
    pull         read Status, verdict checkboxes and comments back
    status       print every disk/Notion disagreement; writes nothing
    install-hook symlink the post-commit hook that pushes on every commit
    watch        poll for local edits and push them (opt-in; see the docstring)

Stdlib only, so the git hook runs without a virtualenv.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path

API = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"
REPO = Path(__file__).resolve().parent.parent
ENV_FILE = Path.home() / ".config" / "notion_sheets.env"
CONFIG_FILE = REPO / ".notion_sheets.json"
GAMES_DB_TITLE = "Games"
SHEETS_DB_TITLE = "Sheets"

# One body change voids the verdict it was given on the old body. Flip to False
# to keep the four checkboxes across an edit.
CLEAR_VERDICT_ON_CHANGE = True

# Notion REST allows ~3 requests/second per connection.
REQUEST_INTERVAL = 0.34
DIFF_CHAR_CAP = 1500

STATUSES = ["REVIEW", "READY", "GAME-READY"]
VERDICT = ["Character", "Coherence", "Correctness", "Convenience"]

# Kind comes from the directory a sheet sits in, except for the named
# game-level sheets, which are identified by filename wherever they sit.
DIR_KIND = {"places": "place", "people": "person", "scenes": "scene", "systems": "system"}

# Review order is a property of the KIND, and the-sheets.md already fixes it:
# the decision sheet is what everything is reconciled against, system sheets are
# "written FIRST and the place sheets are written against them" (SY1-SY3), a
# person sheet is a place x hours grid so it needs its places, and a scene is one
# rung of a person. Numbering the files instead would collide with the 43 whose
# digits are already RUNG numbers (ray_03_the_offer).
KIND_ORDER = {"decision": 1, "system": 2, "place": 3, "person": 4, "scene": 5,
              "opening": 6, "guidance": 7, "index": 8, "format": 9, "sheet": 9}

# Generated, not authored — never mirrored back as a sheet.
ORDER_FILE = "REVIEW_ORDER.md"
FILE_KIND = {
    # RELEASE says what is in the first build and what waits, so it is read
    # against everything else the same way DECISIONS is — hence kind "decision"
    # and the same first slot in the review order.
    "RELEASE": "decision",
    "OPENING": "opening",
    "GUIDANCE": "guidance",
    "SYSTEMS": "system",
    "DECISIONS": "decision",
    "INDEX": "index",
    "FORMAT": "format",
}

GAMES_PROPERTIES = {
    "Name": {"type": "title", "title": {}},
    "Sheets": {"type": "number", "number": {"format": "number"}},
    "In review": {"type": "number", "number": {"format": "number"}},
    "Ready": {"type": "number", "number": {"format": "number"}},
    "Last pushed": {"type": "date", "date": {}},
    "Play": {"type": "url", "url": {}},
    "Built": {"type": "date", "date": {}},
}

SHEET_PROPERTIES = {
    "Name": {"type": "title", "title": {}},
    "Path": {"type": "rich_text", "rich_text": {}},
    "Order": {"type": "number", "number": {"format": "number"}},
    "Kind": {"type": "select", "select": {"options": []}},
    "Status": {
        "type": "select",
        "select": {
            "options": [
                {"name": "REVIEW", "color": "yellow"},
                {"name": "READY", "color": "green"},
                {"name": "GAME-READY", "color": "blue"},
            ]
        },
    },
    "Character": {"type": "checkbox", "checkbox": {}},
    "Coherence": {"type": "checkbox", "checkbox": {}},
    "Correctness": {"type": "checkbox", "checkbox": {}},
    "Convenience": {"type": "checkbox", "checkbox": {}},
    "Gate-required": {"type": "checkbox", "checkbox": {}},
    "Approved at": {"type": "rich_text", "rich_text": {}},
    "Words": {"type": "number", "number": {"format": "number"}},
    "Last pushed": {"type": "date", "date": {}},
}


# --------------------------------------------------------------------------- io


def load_token() -> str:
    token = os.environ.get("NOTION_TOKEN")
    if not token and ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("NOTION_TOKEN="):
                token = line.split("=", 1)[1].strip()
                break
    if not token:
        sys.exit(f"no NOTION_TOKEN in the environment or {ENV_FILE}")
    return token


_last_call = 0.0


def api(method: str, path: str, body: dict | None = None, token: str = "") -> dict:
    """One Notion request, paced and retried on 429."""
    global _last_call
    for attempt in range(5):
        wait = REQUEST_INTERVAL - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(
            f"{API}{path}",
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                _last_call = time.time()
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            _last_call = time.time()
            payload = exc.read().decode()
            if exc.code == 429 and attempt < 4:
                time.sleep(float(exc.headers.get("Retry-After", 2)) + 0.5)
                continue
            raise SystemExit(f"{method} {path} -> {exc.code}\n{payload[:600]}")
    raise SystemExit(f"{method} {path} -> rate limited after 5 attempts")


def load_config() -> dict:
    return json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}


def save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else ""


# ------------------------------------------------------------------------ sheets


@dataclass
class Sheet:
    path: str          # repo-relative, the join key
    game: str
    kind: str
    status: str
    order: int
    words: int
    title: str
    body: str          # normalised, ready for Notion


def normalise(md: str) -> str:
    """The 6 <pre> schedule grids become fenced code.

    The language is pinned to `text`: left bare, Notion guessed `javascript`
    for a schedule grid and syntax-coloured it into noise.
    """
    return md.replace("<pre>", "```text").replace("</pre>", "```")


def parse_sheet(path: Path) -> Sheet:
    rel = str(path.relative_to(REPO))
    raw = path.read_text()
    first = raw.split("\n", 1)[0]
    marker = re.search(r"\[(REVIEW|READY|GAME-READY)\]", first)
    stem = path.stem
    kind = FILE_KIND.get(stem.upper()) or DIR_KIND.get(path.parent.name, "sheet")
    game = path.relative_to(REPO / "games").parts[0]
    order = KIND_ORDER.get(kind, 9)
    return Sheet(
        path=rel,
        game=game,
        kind=kind,
        status=marker.group(1) if marker else "REVIEW",
        order=order,
        words=len(raw.split()),
        # The game is the board now, so it leaves the title and the order
        # takes its place: sorting by name is sorting by review order.
        title=f"{order} · {kind} · {stem}",
        body=normalise(raw),
    )


def game_dirs(games: list[str] | None) -> list[Path]:
    base = REPO / "games"
    if games:
        return [base / g for g in games]
    return [d for d in sorted(base.iterdir()) if (d / "sheets").is_dir()]


def discover(games: list[str] | None, paths: list[str] | None) -> list[Sheet]:
    """Every reviewable document for these games, in review order.

    DECISIONS.md is one of the six sheet types and carries a status marker, but
    it lives at the game root rather than under sheets/ — so it is collected
    explicitly. It is order 1: everything else reconciles against it.
    """
    if paths:
        found = [REPO / p for p in paths]
    else:
        found = []
        for game_dir in game_dirs(games):
            found += sorted(game_dir.glob("sheets/**/*.md"))
            if (game_dir / "DECISIONS.md").exists():
                found.append(game_dir / "DECISIONS.md")
    sheets = [parse_sheet(p) for p in found if p.exists() and p.name != ORDER_FILE]
    return sorted(sheets, key=lambda s: (s.order, s.path))


# ------------------------------------------------------------------------- notion


def prop_text(prop: dict) -> str:
    return "".join(x.get("plain_text", "") for x in prop.get("rich_text", []))


def fetch_rows(data_source_id: str, token: str) -> dict[str, dict]:
    """Every sheet row in one game's board, keyed on Path."""
    rows: dict[str, dict] = {}
    cursor = None
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        page = api("POST", f"/data_sources/{data_source_id}/query", body, token)
        for row in page["results"]:
            props = row["properties"]
            rows[prop_text(props.get("Path", {}))] = {
                "id": row["id"],
                "url": row.get("url", ""),
                "status": (props.get("Status", {}).get("select") or {}).get("name"),
                "approved_at": prop_text(props.get("Approved at", {})),
                "verdict": {v: props.get(v, {}).get("checkbox", False) for v in VERDICT},
            }
        if not page.get("has_more"):
            return rows
        cursor = page["next_cursor"]


def properties_for(sheet: Sheet, status: str, extra: dict | None = None) -> dict:
    """A sheet row. No Game column — the board it sits in is the game."""
    props = {
        "Name": {"title": [{"text": {"content": sheet.title}}]},
        "Path": {"rich_text": [{"text": {"content": sheet.path}}]},
        "Order": {"number": sheet.order},
        "Kind": {"select": {"name": sheet.kind}},
        "Status": {"select": {"name": status}},
        "Words": {"number": sheet.words},
        "Last pushed": {"date": {"start": date.today().isoformat()}},
    }
    props.update(extra or {})
    return props


def changes_block(approved_sha: str, sheet: Sheet) -> str:
    """The diff since sign-off, rendered at the top of the page."""
    diff = git("diff", approved_sha, "--", sheet.path)
    if not diff.strip():
        return ""
    head = (git("rev-parse", "--short", "HEAD") or "HEAD").strip()
    lines = [l for l in diff.splitlines() if not l.startswith(("diff --git", "index "))]
    text = "\n".join(lines)
    if len(text) > DIFF_CHAR_CAP:
        kept = text[:DIFF_CHAR_CAP].rsplit("\n", 1)[0]
        dropped = len(text[len(kept):].splitlines())
        text = f"{kept}\n… {dropped} more lines — git diff {approved_sha[:7]}..HEAD -- {sheet.path}"
    return (
        f"## ⚠ CHANGES SINCE APPROVAL\n\n"
        f"`{approved_sha[:7]}` (approved) → `{head}` (HEAD)\n\n"
        f"```diff\n{text}\n```\n\n---\n\n"
    )


def pick_parent(results: list[dict]) -> str:
    """The page to hang the Games database off.

    Only pages the integration was explicitly shared with come back from search,
    and a workspace-level one is the deliberate choice; a nested page is almost
    always something a previous run created. Refuses to guess between two.
    """
    pages = [r for r in results if r["object"] == "page"]
    if not pages:
        sys.exit("no page is shared with this integration — share one in Notion first")
    top = [p for p in pages if p.get("parent", {}).get("type") == "workspace"]
    candidates = top or pages
    if len(candidates) > 1:
        listing = "\n".join(f"  {p['id']}  {p.get('url','')}" for p in candidates)
        sys.exit(f"several pages are shared — pass --parent <page_id>:\n{listing}")
    return candidates[0]["id"]


def make_views(database_id: str, data_source_id: str, token: str) -> None:
    """A board and a filtered table per game.

    Grouping is not settable through /views (see prd §15.1) — Notion picks a
    default and it is a two-tap change in the UI.
    """
    for name, kind in [("Board", "board"), ("All sheets", "table")]:
        api("POST", "/views", {"database_id": database_id,
                               "data_source_id": data_source_id,
                               "type": kind, "name": name}, token)


def ensure_game(game: str, cfg: dict, token: str) -> dict:
    """The game's row in Games, and the Sheets board living inside it.

    Adopts whatever already exists — a row with this name, a child database
    called Sheets — so a lost config file costs nothing.
    """
    known = cfg.setdefault("games", {})
    if game in known:
        return known[game]

    rows = api("POST", f"/data_sources/{cfg['games_data_source_id']}/query",
               {"page_size": 100}, token)["results"]
    row = next((r for r in rows if "".join(
        x.get("plain_text", "") for x in r["properties"]["Name"]["title"]) == game), None)
    if row is None:
        row = api("POST", "/pages", {
            "parent": {"type": "data_source_id",
                       "data_source_id": cfg["games_data_source_id"]},
            "properties": {"Name": {"title": [{"text": {"content": game}}]}},
        }, token)
        print(f"  + game row  {game}")

    children = api("GET", f"/blocks/{row['id']}/children?page_size=100", None, token)
    db_id = next((b["id"] for b in children["results"]
                  if b["type"] == "child_database"
                  and b["child_database"]["title"] == SHEETS_DB_TITLE), None)
    if db_id is None:
        db = api("POST", "/databases", {
            "parent": {"type": "page_id", "page_id": row["id"]},
            "title": [{"text": {"content": SHEETS_DB_TITLE}}],
            "initial_data_source": {"properties": SHEET_PROPERTIES},
        }, token)
        db_id = db["id"]
        make_views(db_id, db["data_sources"][0]["id"], token)
        print(f"  + board     {game}")
    else:
        db = api("GET", f"/databases/{db_id}", None, token)

    known[game] = {"row_id": row["id"], "database_id": db_id,
                   "data_source_id": db["data_sources"][0]["id"],
                   "url": row.get("url", "")}
    save_config(cfg)
    return known[game]


def update_game_row(game: str, game_cfg: dict, statuses: list[str], token: str) -> None:
    """Counts, plus the Play link and the build date if the game has a build.

    `play_url` is set by hand in .notion_sheets.json, never guessed: where a
    game is allowed to be hosted is a decision, not something a sync infers.
    """
    props = {
        "Sheets": {"number": len(statuses)},
        "In review": {"number": statuses.count("REVIEW")},
        "Ready": {"number": sum(s in ("READY", "GAME-READY") for s in statuses)},
        "Last pushed": {"date": {"start": date.today().isoformat()}},
    }
    props["Play"] = {"url": game_cfg.get("play_url") or None}
    built = REPO / "games" / game / "output" / "index.html"
    if built.exists():
        props["Built"] = {"date": {"start": date.fromtimestamp(
            built.stat().st_mtime).isoformat()}}
    api("PATCH", f"/pages/{game_cfg['row_id']}", {"properties": props}, token)


def write_review_order(game: str, sheets: list[Sheet]) -> None:
    """The same order Notion shows, as a file you can read without a browser."""
    rows = "\n".join(
        f"| {s.order} | {s.kind} | `{s.path.split('/', 2)[2]}` | `[{s.status}]` | {s.words:,} |"
        for s in sheets)
    body = f"""# REVIEW ORDER — {game}

**Generated by `scripts/notion_sheets_sync.py` on every push. Do not edit.**

Order is a property of the sheet's **kind**, not of its filename — `the-sheets.md`
already fixes it. The decision sheet is what every other sheet is reconciled
against (S6); system sheets are *"written FIRST and the place sheets are written
against them"* (SY1-SY3); a person sheet is a place x hours grid, so it needs its
places (S5); a scene is one rung of a person.

Filenames are deliberately not numbered: 43 sheets already carry a two-digit
number and it means the **rung** (`ray_03_the_offer`), so a second number would
mean two things in one name.

| # | kind | sheet | status | words |
|---|---|---|---|---|
{rows}

**{len(sheets)} documents · {sum(1 for s in sheets if s.status == 'REVIEW')} in review**
"""
    # A game whose only sheet is the root-level DECISIONS.md has no sheets/ dir
    # yet — discover() collects that file explicitly, so this is a supported
    # state and must not crash the push after Notion has already been written.
    order_path = REPO / "games" / game / "sheets" / ORDER_FILE
    order_path.parent.mkdir(parents=True, exist_ok=True)
    order_path.write_text(body)


def by_game(sheets: list[Sheet]) -> dict[str, list[Sheet]]:
    grouped: dict[str, list[Sheet]] = {}
    for sheet in sheets:
        grouped.setdefault(sheet.game, []).append(sheet)
    return grouped


# ----------------------------------------------------------------------- commands


def cmd_init(args, token: str) -> None:
    cfg = load_config()
    if cfg.get("games_data_source_id") and not args.force:
        print(f"already initialised: Games {cfg['games_database_id']}")
        return

    search = api("POST", "/search", {"page_size": 50}, token)
    live = [r for r in search["results"] if not r.get("in_trash")]
    existing = next((d for d in live if d["object"] == "database" and "".join(
        x.get("plain_text", "") for x in d.get("title", [])) == GAMES_DB_TITLE), None)

    if existing and not args.force:
        db = api("GET", f"/databases/{existing['id']}", None, token)
    else:
        parent_id = args.parent or pick_parent(live)
        print(f"parent page: {parent_id}")
        db = api("POST", "/databases", {
            "parent": {"type": "page_id", "page_id": parent_id},
            "title": [{"text": {"content": GAMES_DB_TITLE}}],
            "initial_data_source": {"properties": GAMES_PROPERTIES},
        }, token)

    cfg.update({"games_database_id": db["id"],
                "games_data_source_id": db["data_sources"][0]["id"],
                "url": db.get("url", ""), "games": cfg.get("games", {})})
    save_config(cfg)
    print(f"Games database {db['id']}\n{db.get('url','')}")


def cmd_push(args, token: str) -> None:
    cfg = load_config()
    if not cfg.get("games_data_source_id"):
        sys.exit("run `init` first")
    sheets = discover(args.game, args.paths)
    if not sheets:
        print("no sheets matched")
        return

    for game, group in sorted(by_game(sheets).items()):
        print(f"\n{game}")
        game_cfg = ensure_game(game, cfg, token)
        rows = fetch_rows(game_cfg["data_source_id"], token)
        created = reopened = updated = 0
        statuses: list[str] = []

        for sheet in group:
            row = rows.get(sheet.path)
            if row is None:
                api("POST", "/pages", {
                    "parent": {"type": "data_source_id",
                               "data_source_id": game_cfg["data_source_id"]},
                    "properties": properties_for(sheet, sheet.status),
                    "markdown": sheet.body,
                }, token)
                created += 1
                statuses.append(sheet.status)
                continue

            prefix = ""
            status = row["status"] or sheet.status
            extra: dict = {}
            if row["approved_at"]:
                prefix = changes_block(row["approved_at"], sheet)
                if prefix:
                    status = "REVIEW"
                    if CLEAR_VERDICT_ON_CHANGE:
                        extra.update({v: {"checkbox": False} for v in VERDICT})

            api("PATCH", f"/pages/{row['id']}",
                {"properties": properties_for(sheet, status, extra)}, token)
            api("PATCH", f"/pages/{row['id']}/markdown",
                {"type": "replace_content",
                 "replace_content": {"new_str": prefix + sheet.body}}, token)
            statuses.append(status)
            if prefix:
                reopened += 1
                print(f"  REOPEN  {sheet.path}  (changed since {row['approved_at'][:7]})")
            else:
                updated += 1

        if not args.paths:
            update_game_row(game, game_cfg, statuses, token)
            write_review_order(game, group)
        print(f"  {created} new · {reopened} re-opened · {updated} updated"
              f"  ->  {game_cfg.get('url','')}")


def cmd_pull(args, token: str) -> None:
    cfg = load_config()
    if not cfg.get("games"):
        sys.exit("nothing pushed yet")
    head = (git("rev-parse", "HEAD") or "").strip()
    comments: list[str] = []

    for game, game_cfg in sorted(cfg["games"].items()):
        if args.game and game not in args.game:
            continue
        sheets = {s.path: s for s in discover([game], None)}
        rows = fetch_rows(game_cfg["data_source_id"], token)
        print(f"\n{game}")

        for path, row in sorted(rows.items()):
            sheet = sheets.get(path)
            if sheet is not None and row["status"] and row["status"] != sheet.status:
                file = REPO / path
                first, rest = file.read_text().split("\n", 1)
                file.write_text(re.sub(r"\[(REVIEW|READY|GAME-READY)\]",
                                       f"[{row['status']}]", first, count=1) + "\n" + rest)
                print(f"  {sheet.status} -> {row['status']}  {path}")
                if row["status"] in ("READY", "GAME-READY") and head:
                    api("PATCH", f"/pages/{row['id']}", {"properties": {
                        "Approved at": {"rich_text": [{"text": {"content": head}}]}}}, token)
                    missing = [v for v in VERDICT if not row["verdict"][v]]
                    if missing:
                        print(f"      verdict incomplete — missing {', '.join(missing)}")

            for c in api("GET", f"/comments?block_id={row['id']}", None, token).get("results", []):
                text = "".join(x.get("plain_text", "") for x in c.get("rich_text", []))
                comments.append(f"  {path}\n    {text}\n    {row['url']}")

    print("\ncomments:")
    print("\n".join(comments) if comments else "  none open")


def cmd_status(args, token: str) -> None:
    cfg = load_config()
    if not cfg.get("games"):
        sys.exit("nothing pushed yet")
    total_disk = total_notion = 0

    for game in sorted({s.game for s in discover(args.game, None)} | set(cfg["games"])):
        if args.game and game not in args.game:
            continue
        sheets = {s.path: s for s in discover([game], None)}
        game_cfg = cfg["games"].get(game)
        rows = fetch_rows(game_cfg["data_source_id"], token) if game_cfg else {}
        total_disk += len(sheets)
        total_notion += len(rows)
        print(f"\n{game}  —  {len(sheets)} on disk · {len(rows)} in notion")
        for path, sheet in sorted(sheets.items()):
            row = rows.get(path)
            if row is None:
                print(f"  not in notion   {path}")
            elif row["status"] != sheet.status:
                print(f"  disk {sheet.status:<10} notion {row['status']:<10} {path}")
        for path in sorted(rows):
            if path not in sheets:
                print(f"  gone from disk  {path}")

    print(f"\n{total_disk} on disk · {total_notion} in notion")


def cmd_install_hook(args, token: str) -> None:
    """Point .git/hooks/post-commit at the checked-in hook.

    A hook inside .git is not versioned, so the real file lives in scripts/hooks
    and this makes the link.
    """
    hooks = Path(git("rev-parse", "--git-dir").strip() or REPO / ".git") / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    link = hooks / "post-commit"
    target = REPO / "scripts" / "hooks" / "post-commit"
    if link.exists() or link.is_symlink():
        if link.is_symlink() and link.resolve() == target:
            print(f"already installed: {link}")
            return
        if not args.force:
            sys.exit(f"{link} exists and is not our hook — rerun with --force to replace")
        link.unlink()
    link.symlink_to(os.path.relpath(target, hooks))
    print(f"installed {link} -> {os.path.relpath(target, hooks)}")


def cmd_watch(args, token: str) -> None:
    """Push local edits as they happen. Opt-in, foreground, and noisy by design.

    This is NOT installed as a daemon, deliberately. A save is not a sign-off:
    a body change re-opens the row and clears the four verdict boxes, so a
    watcher left running during authoring will wipe a verdict LO is in the
    middle of giving. Run it when you want live sync and stop it when you don't.
    """
    print(f"watching {'/'.join(args.game) if args.game else 'every game'} "
          f"every {args.interval}s — ctrl-c to stop")
    seen = {s.path: (REPO / s.path).stat().st_mtime for s in discover(args.game, None)}
    while True:
        time.sleep(args.interval)
        changed = []
        for sheet in discover(args.game, None):
            mtime = (REPO / sheet.path).stat().st_mtime
            if seen.get(sheet.path) != mtime:
                seen[sheet.path] = mtime
                changed.append(sheet.path)
        if not changed:
            continue
        print(f"\n{time.strftime('%H:%M:%S')} — {len(changed)} changed")
        push_args = argparse.Namespace(game=None, paths=changed)
        cmd_push(push_args, token)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="create or adopt the Games database")
    p_init.add_argument("--force", action="store_true", help="create a new database")
    p_init.add_argument("--parent", help="page id to hang the database off")

    for name, help_text in [("push", "send sheets to Notion"),
                            ("pull", "read verdicts and comments back"),
                            ("status", "print disk/Notion disagreements")]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--game", action="append", help="limit to a game slug (repeatable)")
        if name == "push":
            p.add_argument("--paths", nargs="*", help="explicit repo-relative sheet paths")

    p_hook = sub.add_parser("install-hook", help="install the post-commit hook")
    p_hook.add_argument("--force", action="store_true", help="replace an existing hook")

    p_watch = sub.add_parser("watch", help="poll for local edits and push them")
    p_watch.add_argument("--game", action="append", help="limit to a game slug")
    p_watch.add_argument("--interval", type=int, default=10, help="seconds between polls")

    args = parser.parse_args()
    if not hasattr(args, "paths"):
        args.paths = None
    if not hasattr(args, "game"):
        args.game = None
    {"init": cmd_init, "push": cmd_push, "pull": cmd_pull, "status": cmd_status,
     "install-hook": cmd_install_hook, "watch": cmd_watch}[args.cmd](args, load_token())


if __name__ == "__main__":
    main()
