#!/usr/bin/env python3
"""Run ONE free-text Google Images search for a slot and shelve every result.

This is the human's own search. `fetch_pornhub.py` re-runs a chip's terms scoped
to PornHub; `fetch_related.py` grows a bucket off one clip. Neither lets the
person looking at the shelf say "no — try THIS". That is all this script is: the
same proven route, with the corpus left wide open.

Two things follow from being unscoped, and both are decided by the slot's FORMAT
rather than guessed from the words:

- **`gif` is appended on animated slots only** (measured 7->59, 1->54, 0->91
  fetchable urls). On a still slot the same token is poison — it drags a `.jpg`
  brief into animated results — so it is not added.
- **The extraction regex follows the same axis.** `clean_media_urls` matches
  `gif|mp4|webm` by default, so a `.jpg` slot harvests ZERO from a completely
  full grid; `still=True` swaps in the still extension group.

`--format` is resolved by the CALLER, not here. The endpoint is the only party
that can see the disk (a pool slot is a folder with no extension of its own), so
this script takes the answer and does not second-guess it.

The bucket label carries NO sigil prefix. That is load-bearing, not cosmetic: the
picker files `⇢ `/`◆ ` labels into side panels and everything else onto the shelf,
so an unprefixed label is what makes this render as an ordinary search chip — and
inherit its count, its host verdict and its PH button from the code that already
draws them. The label is the EFFECTIVE query, `gif` included: the query is the
unit of quality control on a shelf, and a label that hid a token which changed
the results would be lying about what ran.

Same Chrome, same contract, same exit codes as fetch_related.py — see that file's
docstring for the profile setup. Every pure function is imported from it rather
than copied: a duplicated extractor is one that stops getting the other's fixes.

Exit codes:
  0  ok — one JSON result line on stdout
  3  Google captcha / unusual-traffic page — wait and retry later; NEVER solved here
  4  the search extracted zero urls
  5  CDP connect failed (is the dedicated Chrome running with the debug port?)
  6  dev API unreachable or refused
  7  results suspiciously clean — likely the WRONG Chrome, or SafeSearch is back
     on. ANIMATED SLOTS ONLY; see `_sanity_check` for why the still path is exempt.

Usage:
    python scripts/fetch_search.py --game vesper \\
        --slot-key sex/mercer_first_oral_t5.webm \\
        --query "kneeling blowjob eye contact"
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

# scripts/ is not a package. sys.path[0] is already this directory for a direct
# run and for the subprocess the endpoint spawns, but make it explicit so the
# module also imports cleanly under pytest from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fetch_related as fr  # noqa: E402 - deliberate, after the path insert

SEARCH_SOURCE = "manual"
ANIMATED, STILL = "animated", "still"
FORMATS = (ANIMATED, STILL)

# A bare `gif`/`gifs` token already in the terms. Word-anchored so `gift` and
# `gifted` do not count as the user having asked for animation.
_HAS_GIF_RE = re.compile(r"\bgifs?\b", re.IGNORECASE)

# Still results carry `.jpg`; the picker's badge and its <img>-vs-<video> choice
# both read these, so a still stocked as "gif" would mislabel every tile.
_VIDEO_EXT_RE = re.compile(r"\.(mp4|webm)(\?|$)", re.IGNORECASE)


def search_query(terms: str, fmt: str = ANIMATED) -> str:
    """The Google query. No `site:` — the whole point is an open corpus.

    `gif` is appended on animated slots, and only when the terms do not already
    carry one, so a human who types it out of habit does not search for it twice.
    """
    terms = " ".join(terms.split())
    if fmt == ANIMATED and not _HAS_GIF_RE.search(terms):
        return f"{terms} gif"
    return terms


def search_label(terms: str, fmt: str = ANIMATED) -> str:
    """The bucket's chip label — the effective query, whitespace-collapsed to
    match `_canon_query` server-side, which is what joins found_by to the record.

    Deliberately NOT prefixed. `fr.is_panel_label` sends `⇢ `/`◆ ` labels to a
    side panel; a bare one lands on the shelf, which is where a text search
    belongs and where the PH button gets drawn.
    """
    return search_query(terms, fmt)


def images_url(q: str) -> str:
    return f"https://www.google.com/search?udm=2&q={quote_plus(q)}"


def _sanity_check(urls: list, fmt: str, port: int) -> None:
    """Exit 7 — but on animated slots only.

    `looks_suspiciously_clean` reads "thin, and nothing on a porn host" as a
    broken runner profile. That inference holds for an act query on an animated
    slot. It is WRONG for a still slot, where `FURNITURE_RE` counts exactly the
    stock-photo hosts — Getty, Shutterstock, Dreamstime — that mean a PLACE query
    landed. Firing here would tell the human to go fix a browser that is fine.

    A still search that genuinely found nothing still fails, as exit 4 below.
    """
    if fmt != ANIMATED:
        return
    if fr.looks_suspiciously_clean(urls):
        # Reworded from the site:-scoped copies, which accuse the profile with
        # certainty. That is a safe inference when the corpus was pinned to one
        # porn host and a fair one here (the guard needs BOTH thin AND
        # furniture-only, and a merely vanilla query still returns dozens of
        # tenor/giphy urls) — but not a certain one, so it leads with the check
        # the human can act on and admits the other reading.
        fr._fail(
            7,
            f"only {len(urls)} urls and nothing but stock-photo/meme "
            f"hosts. Usually that means SafeSearch is back ON in the "
            f"find-media profile on :{port}, or :{port} is not the "
            "dedicated Chrome. If the terms really are that vanilla, "
            "this may just be a thin query.",
        )


def _typed(url: str, fmt: str) -> tuple:
    """(type, media_kind) for one url.

    Off the URL for animated results, off the FORMAT for stills — a `.jpg` typed
    as "gif" puts the wrong badge on every tile, which nobody notices until they
    are triaging 300 of them.
    """
    if fmt == STILL:
        return "image", "img"
    if _VIDEO_EXT_RE.search(url):
        return "video", "video"
    return "gif", "img"


def _stock(
    api: str,
    game: str,
    file_: str,
    slot_key: str,
    label: str,
    urls: list,
    docids: dict,
    thumbs: dict,
    fmt: str,
) -> int:
    """Stock the whole harvest in ONE options/add_bulk call.

    This is the one place this script deliberately parts company with
    fetch_pornhub.py, which posts one url at a time. That choice was made to keep
    the first PornHub run byte-comparable with the proven related path, and it is
    affordable there because `site:` scoping keeps a yield at tens of urls.

    An UNSCOPED search is the opposite case — full-depth Google is ~400 urls — and
    the per-url path is measured at 214 ms/url against a 4.4 MB store (see
    `_add_options_bulk`: 250 urls = 53.5 s sequential vs 0.21 s bulk). At 400 urls
    that is ~85 s of API time inside a 180 s subprocess timeout, most of it holding
    a lock that is GLOBAL TO THE GAME. Bulk is not an optimization here; it is what
    keeps this path from timing out and blocking every other agent while it does.

    `stocked` stays "urls that landed on the shelf" — added PLUS duplicates — so it
    means the same thing it does on the other two runners. The chip's count is
    derived from the shelf anyway, never from this number.
    """
    items = []
    for u in urls:
        type_, kind = _typed(u, fmt)
        items.append(
            {
                "url": u,
                "type": type_,
                "media_kind": kind,
                "docid": docids.get(u, ""),
                "thumb": thumbs.get(u, ""),
            }
        )
    r = fr._api_post(
        api,
        "options/add_bulk",
        {
            "game": game,
            "file": file_,
            "slot_key": slot_key,
            "query": label,
            "items": items,
        },
    )
    if r.status_code != 200:
        fr._fail(6, f"options/add_bulk refused ({r.status_code}): {r.text[:200]}")
    body = r.json()
    return int(body.get("added", 0)) + int(body.get("duplicates", 0))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--game", required=True)
    ap.add_argument("--slot-key", required=True)
    ap.add_argument("--query", required=True, help="the terms, verbatim from the human")
    ap.add_argument(
        "--file", default="", help="bytes-destination path; defaults to --slot-key"
    )
    ap.add_argument(
        "--format",
        default=ANIMATED,
        choices=FORMATS,
        help="the slot's format axis; the caller resolves it",
    )
    ap.add_argument("--port", type=int, default=fr.DEFAULT_PORT)
    ap.add_argument("--api", default=fr.DEFAULT_API)
    args = ap.parse_args()
    file_ = args.file or args.slot_key
    fmt = args.format

    terms = " ".join(args.query.split())
    if not terms:
        fr._fail(4, "--query is empty after whitespace collapse")
    q = search_query(terms, fmt)
    label = search_label(terms, fmt)
    # The bucket lands on the SHELF only if its label carries no panel sigil. The
    # endpoint rejects a typed `◆`/`⇢` before spawning Chrome, so reaching here
    # with one means the prefix list drifted between the three files that hold it
    # (fetch_related.PANEL_PREFIXES, media_finder, find.html PANEL_KIND). Fail
    # loudly rather than silently filing the results in a panel nobody opened.
    if fr.is_panel_label(label):
        fr._fail(
            4,
            f"label {label!r} carries a panel prefix — it would vanish "
            "off the shelf into a side panel. Drop the leading sigil.",
        )
    print(f"q={q!r}  label={label!r}  format={fmt}", file=sys.stderr)

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
            urls = fr.clean_media_urls(html, still=(fmt == STILL))
            docids = fr.docid_join(html)
            thumbs = fr.thumb_join(html)
            hosts = fr.host_histogram(urls)
            # ORDER MATTERS, and it is inverted relative to fetch_pornhub.py:143-148.
            # `looks_suspiciously_clean([])` is True — `len([]) < 5 and not []` —
            # so checking it first makes exit 4 UNREACHABLE from the browser path,
            # and a zero-yield search reports itself as a broken Chrome profile.
            # Empty is its own answer; ask that question first.
            if not urls:
                fr._fail(
                    4,
                    f"no {'still' if fmt == STILL else 'animated'} urls "
                    f"extracted for {q!r}",
                )
            _sanity_check(urls, fmt, args.port)

            # -- stock, then record — §5 order, never reversed -----------------
            t0 = time.monotonic()
            stocked = _stock(
                args.api,
                args.game,
                file_,
                args.slot_key,
                label,
                urls,
                docids,
                thumbs,
                fmt,
            )
            stock_seconds = round(time.monotonic() - t0, 1)

            # No seed_url: this is a text search, not a hop off one clip. That is
            # also why queries/add's 409 label-collision guard is inert here — it
            # only fires when both records carry a seed_url.
            rec = fr._api_post(
                args.api,
                "queries/add",
                {
                    "game": args.game,
                    "file": file_,
                    "slot_key": args.slot_key,
                    "query": label,
                    "source": SEARCH_SOURCE,
                    "urls": len(urls),
                    "stocked": stocked,
                    "hosts": hosts,
                    "round": 1,
                    "status": "ok",
                },
            )
            if rec.status_code != 200:
                fr._fail(
                    6, f"queries/add refused ({rec.status_code}): {rec.text[:200]}"
                )

            print(
                json.dumps(
                    {
                        "ok": True,
                        "label": label,
                        "query": q,
                        "format": fmt,
                        "urls": len(urls),
                        "stocked": stocked,
                        "with_docid": sum(1 for u in urls if docids.get(u)),
                        "with_thumb": sum(1 for u in urls if thumbs.get(u)),
                        "stock_seconds": stock_seconds,
                    }
                )
            )
        finally:
            page.close()


if __name__ == "__main__":
    main()
