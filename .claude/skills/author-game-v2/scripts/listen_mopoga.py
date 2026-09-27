#!/usr/bin/env python3
"""
listen_mopoga.py — what players said on mopoga since a release (the-release.md loop step 8).

Usage:
    python3 scripts/listen_mopoga.py <slug> --since YYYY-MM-DD [--out PATH]

WHY THIS EXISTS. The Great Games Study (round 4b) found the field's real test of an idea is the
response after release, and the loop had no step for it. The v2-listener agent runs this, reads
F95 and gamcore by other means, and writes `listen[]` in the game's `v2_state.json`.

⚠️ IT READS AND NOTHING ELSE, AND IT ALWAYS EXITS 0.
  · It fetches one public comment feed. It never posts, likes or replies.
  · It never writes under `games/`. The comment dump goes to --out (default: the system temp dir).
  · It scores nothing. It prints comments sorted by likes and four keyword counts; the summary is
    written by the agent and read by LO.

The page comes from `v2_state.json` → `listen_sources.mopoga` (a page slug). A game with no page
declared prints "no mopoga page declared" and stops. The feed is mopoga's Isso comment API, the
same one the study read (`https://mopoga.com/comments/?uri=%2F<page>`).
"""

import datetime
import html
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request

API = "https://mopoga.com/comments/?uri={uri}&nested_limit=100"

# Four keyword buckets. A list to read, never a score — a comment can land in several.
BUCKETS = {
    "cheat / code": r"\bcheat|\bcode\b",
    "how / where / stuck": r"\bhow (?:do|to|can)\b|\bwhere\b|\bstuck\b|can't find|cannot find",
    "praise": r"\blove\b|\bgreat\b|\bamazing\b|\bbest\b|\bawesome\b|\bhot\b",
    "request": r"\bplease\b|\bwish\b|\bwould love\b|\badd\b|\bmore\b|\bwant\b",
}


def _state(slug):
    path = f"games/{slug}/v2_state.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def fetch(page):
    """The raw Isso thread for one mopoga page. Raises on any network error."""
    uri = urllib.parse.quote("/" + page.strip("/"), safe="")
    req = urllib.request.Request(API.format(uri=uri), headers={"User-Agent": "listen_mopoga/1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def flatten(thread):
    """Every comment and reply as {id, created, likes, text, parent}."""
    out = []

    def walk(items, parent):
        for c in items or []:
            try:
                created = float(c.get("created") or 0)
            except (TypeError, ValueError):
                created = 0.0
            try:
                likes = int(c.get("likes") or 0)
            except (TypeError, ValueError):
                likes = 0
            text = re.sub(r"<[^>]+>", " ", str(c.get("text") or ""))
            text = re.sub(r"\s+", " ", html.unescape(text)).strip()
            out.append(dict(id=str(c.get("id")), created=created, likes=likes, text=text, parent=parent))
            walk(c.get("replies"), str(c.get("id")))

    walk((thread or {}).get("replies"), None)
    return out


def since_filter(comments, since):
    cut = datetime.datetime.strptime(since, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc).timestamp()
    return [c for c in comments if c["created"] >= cut]


def buckets(comments):
    return {name: sum(1 for c in comments if re.search(rx, c["text"], re.I))
            for name, rx in BUCKETS.items()}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or "--since" not in argv:
        print(__doc__)
        return 0
    slug = argv[0]
    since = argv[argv.index("--since") + 1] if argv.index("--since") + 1 < len(argv) else ""
    out = argv[argv.index("--out") + 1] if "--out" in argv and argv.index("--out") + 1 < len(argv) \
        else os.path.join(tempfile.gettempdir(), f"listen_mopoga_{slug}.json")
    if os.path.abspath(out).startswith(os.path.abspath("games") + os.sep):
        print("refusing to write under games/ — pass --out somewhere else")
        return 0
    try:
        datetime.datetime.strptime(since, "%Y-%m-%d")
    except ValueError:
        print(f"--since must be YYYY-MM-DD, got {since!r}")
        return 0

    page = ((_state(slug).get("listen_sources") or {}).get("mopoga") or "").strip()
    if not page:
        print(f"no mopoga page declared for {slug} "
              f"(v2_state.json → listen_sources.mopoga). Nothing fetched.")
        return 0
    try:
        comments = flatten(fetch(page))
    except Exception as exc:                      # network, HTTP, JSON — all reported, none raised
        print(f"fetch failed: {exc}")
        return 0

    new = sorted(since_filter(comments, since), key=lambda c: (-c["likes"], -c["created"]))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(dict(slug=slug, page=page, since=since, comments=new), fh, indent=1)

    print(f"LISTEN — mopoga /{page} since {since}: {len(new)} of {len(comments)} comment(s)")
    print("  keyword counts (a comment can be in several; a list to read, never a score):")
    for name, n in buckets(new).items():
        print(f"    {name:<22}{n:>4}")
    print()
    for c in new[:40]:
        day = datetime.datetime.fromtimestamp(c["created"], datetime.timezone.utc).strftime("%Y-%m-%d")
        tag = "reply" if c["parent"] else "top"
        print(f"  +{c['likes']:<3} {day} mopoga#{c['id']} ({tag}): {c['text'][:200]}")
    print()
    print(f"  full dump: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
