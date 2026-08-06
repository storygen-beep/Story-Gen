#!/usr/bin/env python3
"""Run a PornHub-scoped Google Images search for one slot and shelve every result.

Why this exists (measured 2026-08-06): PornHub was recorded as "discovery-only —
never a download" on the strength of `egl.phncdn.com/gif/<id>.gif` returning 470
for every id tried. That measurement was taken on urls our own extractor had
already broken. Google's results HTML carries the COMPLETE signed url —
`…/gif/<id>.gif?validfrom=…&validto=…&hash=…` — JSON-escaped, and the old regex
terminated at the file extension, so the ticket was never captured. Fetch the
signed form and it serves 200; strip the query and the same url serves 470.

The tickets are not perishable: `validfrom` 2025 → `validto` 2125, a 99-year
window. (The 2-hour ticket in our older notes belongs to a different url class —
`kl*/pics/gifs/*.webm`, minted on a live PornHub page. This route never touches
pornhub.com at all, only the CDN, which is not blocked.)

Payload is real: GIF89a, up to 1280x720, 240 frames @25fps = 10.0s, 1-40 MB.
Large, but `.gif` renders animated in a built game via <img>, so nothing here is
blocked on a transcode.

Same Chrome, same contract, same exit codes as fetch_related.py — see that file's
docstring for the profile setup. Every pure function is imported from it rather
than copied: a duplicated extractor is one that stops getting the other's fixes.

Exit codes:
  0  ok — one JSON result line on stdout
  3  Google captcha / unusual-traffic page — wait and retry later; NEVER solved here
  4  the search extracted zero urls
  5  CDP connect failed (is the dedicated Chrome running with the debug port?)
  6  dev API unreachable or refused
  7  results suspiciously clean — likely the WRONG Chrome, or SafeSearch is back on

Usage:
    python scripts/fetch_pornhub.py --game media_lab_h \\
        --slot-key scenes/lab_eyecontact_t5.webm \\
        --query "blowjob eye contact looking up"
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

import requests

# scripts/ is not a package. sys.path[0] is already this directory for a direct
# run and for the subprocess the endpoint spawns, but make it explicit so the
# module also imports cleanly under pytest from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fetch_related as fr  # noqa: E402 - deliberate, after the path insert

PH_PREFIX = "◆ "
PH_SOURCE = "pornhub"


def ph_query(terms: str) -> str:
    """The Google query. `site:` pins the corpus to PornHub, and `gif` is what
    reaches its animated pages — measured 7→59, 1→54, 0→91 fetchable urls."""
    return f"site:pornhub.com {' '.join(terms.split())} gif"


def ph_label(terms: str) -> str:
    """The bucket's chip label. Built from the TERMS, not from `ph_query`, so the
    chip reads as the beat rather than as search syntax. Whitespace-collapsed to
    match `_canon_query` server-side, which is what joins found_by to the record.
    """
    return PH_PREFIX + " ".join(terms.split())


def images_url(q: str) -> str:
    return f"https://www.google.com/search?udm=2&q={quote_plus(q)}"


def _stock(api: str, game: str, file_: str, slot_key: str, label: str,
           urls: list, docids: dict, thumbs: dict) -> int:
    """One options/add per url. Mirrors fetch_related._stock, plus `thumb`.

    Deliberately NOT batched: making this byte-identical to the proven related
    path is what makes the first end-to-end run interpretable — a timing
    difference then points at the extractor, not at the store.
    """
    ok = 0
    for u in urls:
        is_vid = re.search(r"\.(mp4|webm)(\?|$)", u, re.IGNORECASE)
        r = fr._api_post(api, "options/add", {
            "game": game, "file": file_, "slot_key": slot_key, "url": u,
            "query": label,
            "type": "video" if is_vid else "gif",
            "media_kind": "video" if is_vid else "img",
            "docid": docids.get(u, ""),
            "thumb": thumbs.get(u, ""),
        })
        if r.status_code == 200 and r.json().get("ok"):
            ok += 1
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--game", required=True)
    ap.add_argument("--slot-key", required=True)
    ap.add_argument("--query", required=True, help="the beat's terms; site: is added here")
    ap.add_argument("--file", default="", help="bytes-destination path; defaults to --slot-key")
    ap.add_argument("--port", type=int, default=fr.DEFAULT_PORT)
    ap.add_argument("--api", default=fr.DEFAULT_API)
    args = ap.parse_args()
    file_ = args.file or args.slot_key

    terms = " ".join(args.query.split())
    if not terms:
        fr._fail(4, "--query is empty after whitespace collapse")
    q = ph_query(terms)
    label = ph_label(terms)
    print(f"q={q!r}  label={label!r}", file=sys.stderr)

    # -- the browser ----------------------------------------------------------
    from playwright.sync_api import sync_playwright  # deferred: pure fns import clean

    with sync_playwright() as p:
        fr._ensure_page_target(args.port)
        try:
            browser = p.chromium.connect_over_cdp(f"http://localhost:{args.port}")
        except Exception as exc:
            # Keep this SHORT — the endpoint relays only the last ~400 chars of
            # stderr, and a playwright traceback would push the sentence out.
            reason = str(exc).splitlines()[0][:120]
            fr._fail(5, f"Could not attach to the Chrome on :{args.port} — {reason}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            # -- the search — the ONLY navigation this script makes ------------
            page.goto(images_url(q), wait_until="domcontentloaded", timeout=45000)
            html = fr._settle(page)
            fr._check_captcha(page, html)
            urls = fr.clean_media_urls(html)
            docids = fr.docid_join(html)
            thumbs = fr.thumb_join(html)
            hosts = fr.host_histogram(urls)
            if fr.looks_suspiciously_clean(urls):
                fr._fail(7, f"only {len(urls)} urls, none on porn hosts — suspiciously "
                            f"clean. Check the profile on :{args.port}: is SafeSearch "
                            "still OFF, and is it the dedicated find-media Chrome?")
            if not urls:
                fr._fail(4, f"no urls extracted for {q!r}")

            # -- stock, then record — §5 order, never reversed -----------------
            t0 = time.monotonic()
            stocked = _stock(args.api, args.game, file_, args.slot_key, label,
                             urls, docids, thumbs)
            stock_seconds = round(time.monotonic() - t0, 1)

            # No seed_url: this is a text search, not a hop off one clip. That is
            # also why queries/add's 409 label-collision guard is inert here — it
            # only fires when both records carry a seed_url.
            rec = fr._api_post(args.api, "queries/add", {
                "game": args.game, "file": file_, "slot_key": args.slot_key,
                "query": label, "source": PH_SOURCE,
                "urls": len(urls), "stocked": stocked, "hosts": hosts,
                "round": 1, "status": "ok",
            })
            if rec.status_code != 200:
                fr._fail(6, f"queries/add refused ({rec.status_code}): {rec.text[:200]}")

            print(json.dumps({
                "ok": True, "label": label, "query": q,
                "urls": len(urls), "stocked": stocked,
                "with_docid": sum(1 for u in urls if docids.get(u)),
                "with_thumb": sum(1 for u in urls if thumbs.get(u)),
                "stock_seconds": stock_seconds,
            }))
        finally:
            page.close()


if __name__ == "__main__":
    main()
