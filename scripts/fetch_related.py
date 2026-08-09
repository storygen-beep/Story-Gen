#!/usr/bin/env python3
"""Fetch Google's related-images feed for one stocked option and shelve it.

Why this works at all (measured live, 2026-08-05): Google Images result pages
embed, in script metadata, triples `"<docid>",["<thumbnail>",h,w],["<file>",h,w]`
pairing every result's index id with its original media URL. The related feed for
an image is then a plain URL — `?udm=2&q=<query>&tbs=rimg:<blob>` — where the blob
is protobuf `field 1 (fixed64) = first 8 bytes of the base64url-decoded docid`,
base64url-encoded. A TRUNCATED blob built from the docid alone serves the real
feed (verified by host-signature match against Google's own full blob; the seed is
excluded from its own results). Ground truth: docid FvF5n0MlBjcrfM → CRbxeZ9DJQY3.

The fetch must run inside a real Chrome profile with SafeSearch off — Google
serves nothing usable to curl or a fresh headless profile. This script attaches
over CDP to a DEDICATED automation profile so the daily browser stays untouched:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \\
        --user-data-dir="$HOME/.chrome-find-media" --remote-debugging-port=9222

One-time setup in that profile, by hand: open google.com, accept/dismiss consent,
turn SafeSearch OFF (google.com/safesearch). Nothing else.

Results land through the same dev API the harvest skill uses: one options/add per
url (labelled, with its own docid so every stocked clip can seed the next hop) and
one queries/add closing record carrying `source:"related"` + `seed_url` — the pair
the picker derives "related fetched" from. Re-running the same seed TOPS UP the
same bucket; nothing is ever cleared.

The seed does not have to still be ON the shelf. Installing a clip consumes its
option row, so the id is looked up across three places, in order: the option's own
`url`, an option's `source_url` (a demoted pick, whose `url` is a local serve path),
and finally the slot's `picks` — what its INSTALLED files were before they were
installed. That is what lets a selected clip seed the next hop.

On a 409 from queries/add (label claimed by a different seed mid-run), the options
this run stocked carry the collided label — so the recovery is not just a rename:
re-pick a suffixed label, RE-STOCK every url under it (dedup makes that N cheap
found_by appends), then record. Done once; a second collision is reported, not
retried.

Exit codes:
  0  ok — one JSON result line on stdout
  3  Google captcha / unusual-traffic page — wait and retry later; NEVER solved here
  4  no usable seed — no stored Google id, no query, or an empty --seed-url.
     Refused WITHOUT touching the browser
  5  CDP connect failed (is the dedicated Chrome running with the debug port?)
  6  dev API unreachable or refused
  7  feed suspiciously clean (almost no urls, none on porn hosts) — likely the
     WRONG Chrome on the port, or SafeSearch is back on in the profile

Usage:
    python scripts/fetch_related.py --game media_lab_f \\
        --slot-key scenes/lab_eyecontact_t5.webm \\
        --seed-url https://cdn.nsfwgify.com/44903/kneeling-blowjob.gif
"""

import argparse
import base64
import json
import re
import sys
from collections import Counter
from pathlib import PurePosixPath
from urllib.parse import quote_plus, urlparse

import requests

DEFAULT_API = "http://localhost:8000"
DEFAULT_PORT = 9222

# The metadata triple: docid, thumbnail tuple, original-file tuple. Same-day join
# coverage measured at 84/97 — misses are lazy-loaded results, which the scroll
# pass below mostly recovers.
# Groups: 1 = docid, 2 = encrypted-tbn thumbnail, 3 = original file url. The
# thumbnail was matched-but-UNCAPTURED until 2026-08-06; the picker now renders it
# so triaging a 15 MB signed gif costs ~20 KB instead.
DOCID_TRIPLE_RE = re.compile(
    r'"([A-Za-z0-9_-]{10,20})",'
    r'\["(https://encrypted-tbn[^"]+)",\d+,\d+\],'
    r'\["(https?:[^"]+?)",\d+,\d+\]'
)

# The trailing `(?:\?…)?` lets a SIGNED url arrive whole; `normalize_media_url`
# then decides whether to keep the query. Backslash stays OUT of the class because
# Google escapes `=` as `=` — `_unescape` runs first, so by match time there
# are none left. Without that ordering the match dies at the first escape.
MEDIA_RE = re.compile(
    r'https?://[^\s"\'<>\\]+?\.(?:gif|mp4|webm)(?:\?[^\s"\'<>\\]*)?',
    re.IGNORECASE,
)

# The STILL counterpart. A slot whose declared file is `.jpg` harvests ZERO from a
# COMPLETELY FULL grid against MEDIA_RE — the extension group is the only thing
# between it and the very same results, and the failure reads as "bad query"
# because the error the caller gets is "no urls extracted".
#
# A second compiled constant rather than a group spliced in at call time: the two
# patterns sitting side by side is what makes the difference legible, and the
# animated path stays the exact object it has always been.
#
# `.gif` is deliberately NOT here. It is the animated set's, and a slot that
# wanted gifs would have declared one — see the FORMAT axis in the find-media
# skill (§3): the declared extension decides, never the MIME or the media_kind.
STILL_MEDIA_RE = re.compile(
    r'https?://[^\s"\'<>\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^\s"\'<>\\]*)?',
    re.IGNORECASE,
)

# Hosts whose media url is a signed TICKET, where the bare path is 470/173 bytes.
# Measured 2026-08-06: egl.phncdn.com/gif/<id>.gif serves 200/206 carrying
# ?validfrom&validto&hash on a 2025→2125 window, and 470 with the query removed.
# The "PornHub is discovery-only, never a download" doctrine came from fetching
# the stripped form — i.e. from urls this very function had already broken.
SIGNED_QUERY_HOSTS = ("phncdn.com",)

# Buckets that live in a side PANEL rather than on the shelf. A prefix is a bucket
# NAME, never a Google query, so pick_q must skip every one of them.
PANEL_PREFIXES = ("⇢ ", "◆ ")  # ⇢ related, ◆ pornhub
PANEL_SOURCES = ("related", "pornhub")

# Hosts that mean the result is furniture, not porn — the picker's chip verdict
# uses the same list. Only the sanity guard reads this here.
FURNITURE_RE = re.compile(
    r"(^|\.)(tenor|giphy|pinterest|tumblr|reddit|redd|gstatic|wikipedia|bbc|"
    r"istockphoto|shutterstock|gettyimages|alamy|dreamstime)\.",
    re.IGNORECASE,
)

CAPTCHA_RE = re.compile(r"unusual traffic|not a robot", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Pure functions — unit-tested, importable without playwright installed.
# ---------------------------------------------------------------------------


def docid_to_blob(docid: str) -> str:
    """Build the `tbs=rimg:` blob from a docid. Ground truth in the module docstring."""
    raw = base64.urlsafe_b64decode(docid + "=" * (-len(docid) % 4))
    if len(raw) < 8:
        raise ValueError(f"docid {docid!r} decodes to {len(raw)} bytes — need ≥8")
    return base64.urlsafe_b64encode(b"\x09" + raw[:8]).rstrip(b"=").decode("ascii")


def related_url(q: str, blob: str) -> str:
    return f"https://www.google.com/search?udm=2&q={quote_plus(q)}&tbs=rimg:{blob}"


def _stem(url: str) -> str:
    return PurePosixPath(urlparse(url).path).stem


def slug_query(seed_url: str) -> str:
    """Filename slug words as a last-resort query. `kneeling-blowjob.gif` →
    `kneeling blowjob gif` — the words the host itself filed the clip under."""
    words = [w for w in re.split(r"[^A-Za-z]+", _stem(seed_url)) if len(w) >= 3]
    return " ".join(words + ["gif"]) if words else ""


def pick_q(option: dict, queries: list, seed_url: str) -> str:
    """The text q for the feed URL. The feed is seeded by query AND image; keeping
    the slot's proven query pins the act while the visuals wander — which is what
    keeps a related hop from drifting off the slot's brief."""
    # A clip stocked BY a panel fetch carries that panel's label in found_by — a
    # bucket name, never a Google query. Only real text searches qualify. Missing
    # the ◆ case would send `◆ site:pornhub.com …` to Google as literal query text.
    found = [q for q in (option.get("found_by") or []) if not is_panel_label(q)]
    if found:
        return found[0]
    for rec in reversed(queries):  # stored oldest-first → newest wins
        q = rec.get("q") or ""
        if rec.get("source") not in PANEL_SOURCES and not is_panel_label(q):
            return q
    return slug_query(seed_url)


def pick_label(seed_url: str, queries: list, taken: set | None = None) -> str:
    """The chip label for this seed's bucket. Same seed reuses its label (top-up);
    a label owned by a DIFFERENT seed gets suffixed — two seeds can legitimately
    share a basename. `taken` forces extra labels off-limits (the 409 retry)."""
    base = "⇢ " + (_stem(seed_url) or "related")
    taken = taken or set()

    def owner(label):
        for rec in queries:
            if rec.get("q") == label:
                return rec.get("seed_url") or ""
        return None

    candidate, n = base, 1
    while True:
        own = owner(candidate)
        if candidate not in taken and (own is None or own == "" or own == seed_url):
            return candidate
        n += 1
        candidate = f"{base} ·{n}"


def is_panel_label(label: str) -> bool:
    """True for a bucket that belongs to a side panel rather than the shelf."""
    return any((label or "").startswith(p) for p in PANEL_PREFIXES)


def normalize_media_url(url: str) -> str:
    """The ONE canonical form of a media url.

    The query string is dropped unless the host SIGNS its urls, where the query
    IS the fetch ticket and dropping it yields a 470. Host-keyed, never
    caller-keyed: two runners sharing this module must agree on the key, or the
    same clip double-stocks as two rows — one dead, one alive, indistinguishable
    in the picker. `clean_media_urls` and `media_triples` must also agree, or
    every signed clip is stocked with an empty docid, which permanently disables
    its ⇢ button.
    """
    host = urlparse(url).netloc.lower()
    if any(host == h or host.endswith("." + h) for h in SIGNED_QUERY_HOSTS):
        return url
    return url.split("?")[0]


def clean_media_urls(html: str, still: bool = False) -> list:
    """§4's extract, in Python: unescape, dedupe, canonicalize, cut google/gstatic
    hosts, cut empty paths.

    `still=True` swaps the animated extension group for the still one — see
    STILL_MEDIA_RE. Everything downstream of the match is shared, so the two
    formats cannot drift apart on canonicalization or on which hosts get cut.
    The default is the animated set, which keeps every existing caller byte-
    identical.

    The phncdn cut that lived here until 2026-08-06 is GONE. It rested on a 470
    measured against urls this very function had already stripped the ticket from,
    so it was self-confirming: strip the signature, fetch the corpse, record the
    host as unfetchable. Signed phncdn urls fetch 200 and last until 2125.
    """
    html = _unescape(html)
    seen, out = set(), []
    for m in (STILL_MEDIA_RE if still else MEDIA_RE).finditer(html):
        u = normalize_media_url(m.group(0))
        if u in seen:
            continue
        seen.add(u)
        host = urlparse(u).netloc.lower()
        if not host or host.endswith("google.com") or host.endswith("gstatic.com"):
            continue
        # Empty-path cut: the filename must be more than a bare extension —
        # `https://host/.gif` is a truncated match, not a clip.
        name = urlparse(u).path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if not name:
            continue
        out.append(u)
    return out


def _unescape(html: str) -> str:
    """Google JSON-escapes embedded urls. Idempotent, so running it on the whole
    page and again on a single url is harmless."""
    return html.replace("\\u003d", "=").replace("\\u0026", "&").replace("\\/", "/")


def media_triples(html: str) -> list:
    """[(file url, docid, thumbnail url)] from the page's metadata triples.

    One parser, two thin readers below — DOCID_TRIPLE_RE's group indices are
    named in exactly one place so a regex change cannot silently shift them.
    """
    html = _unescape(html)
    return [
        (normalize_media_url(m.group(3)), m.group(1), m.group(2))
        for m in DOCID_TRIPLE_RE.finditer(html)
    ]


def docid_join(html: str) -> dict:
    """{file url → docid}. Keys are `normalize_media_url`d to match the shelf."""
    return {url: docid for url, docid, _thumb in media_triples(html)}


def thumb_join(html: str) -> dict:
    """{file url → encrypted-tbn url} — a ~20 KB stand-in for a 15 MB gif."""
    return {url: thumb for url, _docid, thumb in media_triples(html) if thumb}


def host_histogram(urls: list) -> list:
    counts = Counter(urlparse(u).netloc.replace("www.", "", 1) for u in urls)
    return [[h, n] for h, n in counts.most_common()]


def looks_suspiciously_clean(urls: list) -> bool:
    """<5 urls and none on a non-furniture host = the profile on the port is
    almost certainly SafeSearch-on (or the wrong Chrome entirely). A genuinely
    barren related feed still serves furniture; a sanitized one serves nothing."""
    porn = [u for u in urls if not FURNITURE_RE.search("." + urlparse(u).netloc + ".")]
    return len(urls) < 5 and not porn


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def _fail(code: int, msg: str):
    print(msg, file=sys.stderr)
    sys.exit(code)


def _api_post(api: str, endpoint: str, body: dict):
    try:
        return requests.post(
            f"{api}/api/v1/dev/media-finder/{endpoint}", json=body, timeout=15
        )
    except requests.RequestException as exc:
        _fail(6, f"dev API unreachable ({endpoint}): {exc}")


def _ensure_page_target(port: int) -> None:
    """Give the runner at least one page target before attaching.

    Measured 2026-08-05: with every window closed, Chrome keeps serving
    `/json/version` — so the port looks healthy — but `connect_over_cdp` dies at
    handshake with "Browser context management is not supported" and a websocket
    log that reads exactly like a flaky connection. It isn't flaky; there is
    simply nothing to attach to. `PUT /json/new` creates one, and the same
    connect then succeeds. This is why the runner window may be closed to the
    human and the fetch still works.
    """
    try:
        targets = requests.get(f"http://localhost:{port}/json/list", timeout=5).json()
    except (requests.RequestException, ValueError):
        return  # let connect_over_cdp report the real problem
    if any(t.get("type") == "page" for t in targets):
        return
    try:
        requests.put(f"http://localhost:{port}/json/new?about:blank", timeout=5)
    except requests.RequestException:
        return


def _settle(page, wheels: int = 4):
    """Scroll to pull lazy-loaded results into the DOM, then return the HTML."""
    for _ in range(wheels):
        page.mouse.wheel(0, 2400)
        page.wait_for_timeout(650)
    page.wait_for_timeout(400)
    return page.content()


def _check_captcha(page, html: str):
    if "/sorry/" in page.url or CAPTCHA_RE.search(html):
        _fail(
            3,
            "Google served a captcha / unusual-traffic page. Not solving it. "
            "Wait a while before retrying, and slow the pace if it recurs.",
        )


def _stock(
    api: str,
    game: str,
    file_: str,
    slot_key: str,
    label: str,
    urls: list,
    docids: dict,
    thumbs: dict | None = None,
) -> int:
    thumbs = thumbs or {}
    ok = 0
    for u in urls:
        # Anchor on `(\?|$)` so a SIGNED .webm is still typed as video — a signed
        # url no longer ends at its extension.
        is_vid = re.search(r"\.(mp4|webm)(\?|$)", u, re.IGNORECASE)
        r = _api_post(
            api,
            "options/add",
            {
                "game": game,
                "file": file_,
                "slot_key": slot_key,
                "url": u,
                "query": label,
                "type": "video" if is_vid else "gif",
                "media_kind": "video" if is_vid else "img",
                "docid": docids.get(u, ""),
                "thumb": thumbs.get(u, ""),
            },
        )
        if r.status_code == 200 and r.json().get("ok"):
            ok += 1
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--game", required=True)
    ap.add_argument("--slot-key", required=True)
    ap.add_argument("--seed-url", required=True)
    ap.add_argument(
        "--file", default="", help="bytes-destination path; defaults to --slot-key"
    )
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--api", default=DEFAULT_API)
    args = ap.parse_args()
    file_ = args.file or args.slot_key
    seed = args.seed_url.split("?")[0]
    # An empty seed would match every row whose url key is absent, and hand the
    # lookup below somebody else's docid.
    if not seed:
        _fail(4, "--seed-url is empty — nothing to fetch a related feed for")

    # -- the shelf: find the seed option, choose q + label BEFORE stocking -----
    try:
        r = requests.get(
            f"{args.api}/api/v1/dev/media-finder/options/list",
            params={"game": args.game, "file": args.slot_key},
            timeout=15,
        )
        shelf = r.json()
    except (requests.RequestException, ValueError) as exc:
        _fail(6, f"dev API unreachable (options/list): {exc}")
    options, queries = shelf.get("options") or [], shelf.get("queries") or []

    def matches(row: dict) -> bool:
        """Either url a row can be seeded by. `source_url` is where a DEMOTED pick's
        local bytes originally came from — its `url` is a `/games/…` serve path, so
        matching on that alone would miss every clip that was once installed."""
        return any(
            (row.get(key) or "").split("?")[0] == seed for key in ("url", "source_url")
        )

    option = next((o for o in options if matches(o)), None)
    if option is None:
        # Not on the shelf — but it may be INSTALLED. Grab consumes the option row
        # and copies its docid into `picks`, which is the whole reason a selected
        # clip can still seed a hop. Look there before giving up on the id.
        option = next((p for p in (shelf.get("picks") or []) if matches(p)), None)
    if option is None:
        # Not fatal: allow fetching related for a url the caller knows about even
        # if it is not on this shelf yet (it will be, as part of the harvest).
        option = {"url": seed}
        print("note: seed url is not on this slot's shelf", file=sys.stderr)

    # NO ID, NO RUN — refused before the browser is even touched.
    #
    # This used to fall back to hunting the id: run a text search, look for the
    # seed among the results, steal its id. LO killed it 2026-08-05 and he was
    # right. The guess-query ladder bottoms out at filename slug words, so on an
    # aged shelf it opened a Google tab, searched something nobody asked for, and
    # failed anyway — the clip no longer ranked. It read as a bug every time.
    # The real cure is a new search on the slot, which attaches ids to the
    # existing options it re-finds.
    docid = option.get("docid") or ""
    if not docid:
        _fail(
            4,
            "no Google id stored for this clip — not fetching. Run a search "
            "on this slot; any search that re-finds it attaches an id.",
        )

    q = pick_q(option, queries, seed)
    if not q:
        _fail(
            4,
            "no usable query for the feed URL: seed has no found_by, slot has "
            "no searches, and the filename has no slug words",
        )
    label = pick_label(seed, queries)
    print(f"q={q!r}  label={label!r}", file=sys.stderr)

    # -- the browser ----------------------------------------------------------
    from playwright.sync_api import sync_playwright  # deferred: pure fns import clean

    with sync_playwright() as p:
        _ensure_page_target(args.port)
        try:
            browser = p.chromium.connect_over_cdp(f"http://localhost:{args.port}")
        except Exception as exc:
            # Keep this SHORT. The endpoint relays the last ~400 chars of stderr,
            # so a pasted playwright traceback would push the actual sentence out
            # of the window and leave the human reading websocket ids.
            reason = str(exc).splitlines()[0][:120]
            _fail(5, f"Could not attach to the Chrome on :{args.port} — {reason}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            # -- the related feed — the ONLY navigation this script makes ------
            page.goto(
                related_url(q, docid_to_blob(docid)),
                wait_until="domcontentloaded",
                timeout=45000,
            )
            html = _settle(page)
            _check_captcha(page, html)
            urls = clean_media_urls(html)
            docids = docid_join(html)
            thumbs = thumb_join(html)
            hosts = host_histogram(urls)
            if looks_suspiciously_clean(urls):
                _fail(
                    7,
                    f"only {len(urls)} urls, none on porn hosts — suspiciously "
                    f"clean. Check the profile on :{args.port}: is SafeSearch "
                    "still OFF, and is it the dedicated find-media Chrome?",
                )

            # -- stock, then record — §5 order, never reversed ----------------
            stocked = _stock(
                args.api, args.game, file_, args.slot_key, label, urls, docids, thumbs
            )
            rec = _api_post(
                args.api,
                "queries/add",
                {
                    "game": args.game,
                    "file": file_,
                    "slot_key": args.slot_key,
                    "query": label,
                    "source": "related",
                    "seed_url": seed,
                    "urls": len(urls),
                    "stocked": stocked,
                    "hosts": hosts,
                },
            )
            if rec.status_code == 409:
                # Another seed claimed the label mid-run, so OUR options carry a
                # label that is not ours. Re-pick, RE-STOCK (dedup → cheap found_by
                # appends), re-record. Once.
                label2 = pick_label(seed, queries, taken={label})
                print(f"label collision — restocking under {label2!r}", file=sys.stderr)
                stocked = _stock(
                    args.api,
                    args.game,
                    file_,
                    args.slot_key,
                    label2,
                    urls,
                    docids,
                    thumbs,
                )
                rec = _api_post(
                    args.api,
                    "queries/add",
                    {
                        "game": args.game,
                        "file": file_,
                        "slot_key": args.slot_key,
                        "query": label2,
                        "source": "related",
                        "seed_url": seed,
                        "urls": len(urls),
                        "stocked": stocked,
                        "hosts": hosts,
                    },
                )
                label = label2
            if rec.status_code != 200:
                _fail(6, f"queries/add refused: {rec.status_code} {rec.text[:300]}")

            print(
                json.dumps(
                    {
                        "ok": True,
                        "label": label,
                        "urls": len(urls),
                        "stocked": stocked,
                        "docid_source": "stored",
                    }
                )
            )
        finally:
            page.close()


if __name__ == "__main__":
    main()
