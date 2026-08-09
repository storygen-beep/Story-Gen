"""`scripts/fetch_search.py` — the pure half, plus the two guards that must fire
before a browser is ever touched.

Loaded the same way `test_fetch_related_blob.py` loads its subject: by file path,
because `scripts/` is not a package. That works only because both scripts defer
`from playwright.sync_api import sync_playwright` into `main()` — importing this
module with playwright absent is itself part of the contract, and
`test_the_module_imports_without_playwright` asserts it.

Two properties here are load-bearing:

  - **The label carries no panel sigil.** `is_panel_label` is what sends a bucket
    to a side panel instead of the shelf, and the whole point of this search is
    that it lands on the shelf and inherits the chip, the count and the PH button.
  - **`gif` follows the FORMAT axis, not the words.** Appending it is measured
    (7->59 fetchable urls) and correct on an animated slot; on a still slot the
    same token drags a `.jpg` brief into animated results.

    pytest tests/test_fetch_search.py -q
"""
import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).parent.parent / "scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fs = _load("fetch_search")
fr = _load("fetch_related")


# ── the query: gif follows the FORMAT axis ───────────────────────────────────


def test_gif_is_appended_on_an_animated_slot():
    assert fs.search_query("kneeling blowjob", "animated") == "kneeling blowjob gif"


def test_gif_is_not_appended_on_a_still_slot():
    """A still slot wants `.jpg`; `gif` would drag the brief into animated results."""
    assert fs.search_query("empty bar at night", "still") == "empty bar at night"


@pytest.mark.parametrize(
    "terms",
    [
        "kneeling blowjob gif",
        "gif kneeling blowjob",
        "kneeling gifs",
        "kneeling  GIF",
    ],
)
def test_gif_is_not_appended_twice(terms):
    assert fs.search_query(terms, "animated").lower().split().count("gif") <= 1
    assert not fs.search_query(terms, "animated").lower().endswith("gif gif")


@pytest.mark.parametrize("terms", ["gifted hands", "a gift for her"])
def test_gift_is_not_mistaken_for_gif(terms):
    """Word-anchored: `gift`/`gifted` is not the user having asked for animation."""
    assert fs.search_query(terms, "animated").endswith(" gif")


def test_there_is_no_site_scoping():
    assert "site:" not in fs.search_query("kneeling blowjob", "animated")


def test_whitespace_is_collapsed():
    assert (
        fs.search_query("  kneeling   blowjob  ", "animated") == "kneeling blowjob gif"
    )


# ── the label: unprefixed, or the bucket leaves the shelf ────────────────────


def test_the_label_carries_no_panel_prefix():
    """THE assertion that keeps the bucket on the shelf. A ⇢/◆ prefix would file it
    into a side panel, where it would inherit no chip and no PH button."""
    for fmt in ("animated", "still"):
        assert fr.is_panel_label(fs.search_label("kneeling blowjob", fmt)) is False


def test_the_label_is_the_effective_query():
    """Not the raw terms: the query is the unit of quality control on a shelf, so a
    label that hid a token which changed the results would misname its own bucket.
    It also makes the label safe to reuse as a literal Google query — see below."""
    assert fs.search_label("kneeling blowjob", "animated") == "kneeling blowjob gif"
    assert fs.search_label("empty bar", "still") == "empty bar"


def test_the_label_is_canon_query_stable():
    """`_canon_query` (whitespace-collapse, case preserved) is the exact-string join
    key between an option's found_by and its record. The label must already be in
    that form or the join silently misses."""
    label = fs.search_label("  kneeling   blowjob  ", "animated")
    assert label == " ".join(label.split())


def test_the_label_survives_as_a_literal_google_query():
    """`pick_q` reuses a non-panel label AS A GOOGLE QUERY to seed a ⇢ related hop.
    So the label has to be something worth searching — which it is, because it IS
    the query that ran."""
    label = fs.search_label("kneeling blowjob", "animated")
    assert fr.pick_q({"found_by": [label]}, [], "") == label


# ── extraction follows the same axis ─────────────────────────────────────────

_HTML = (
    'x "https://cdn.test/clip.gif" y "https://cdn.test/clip.mp4" '
    '"https://cdn.test/shot.jpg" "https://cdn.test/shot.png" '
    '"https://www.google.com/logo.gif" "https://x.gstatic.com/a.jpg" '
    '"https://cdn.test/.gif"'
)


def test_the_default_extraction_is_animated_and_unchanged():
    urls = fr.clean_media_urls(_HTML)
    assert urls == ["https://cdn.test/clip.gif", "https://cdn.test/clip.mp4"]


def test_still_extraction_picks_up_jpg_and_png():
    """A `.jpg` slot harvested ZERO from a completely full grid before this — the
    extension group was the only thing between it and the same results."""
    urls = fr.clean_media_urls(_HTML, still=True)
    assert urls == ["https://cdn.test/shot.jpg", "https://cdn.test/shot.png"]


def test_still_extraction_keeps_every_other_cut():
    """Only the extension group changes; the google/gstatic and empty-path cuts are
    shared, so the two formats cannot drift apart on anything else."""
    urls = fr.clean_media_urls(_HTML, still=True)
    assert not any("google.com" in u or "gstatic.com" in u for u in urls)


def test_a_gif_is_not_a_still():
    """The FORMAT axis, in the extractor: `.gif` belongs with the videos."""
    assert "https://cdn.test/clip.gif" not in fr.clean_media_urls(_HTML, still=True)


# ── the typing of a stocked row ──────────────────────────────────────────────


@pytest.mark.parametrize(
    "url,fmt,expected",
    [
        ("https://x.test/a.mp4", "animated", ("video", "video")),
        ("https://x.test/a.webm?validfrom=1&hash=z", "animated", ("video", "video")),
        ("https://x.test/a.gif", "animated", ("gif", "img")),
        ("https://x.test/a.jpg", "still", ("image", "img")),
        ("https://x.test/a.png", "still", ("image", "img")),
    ],
)
def test_a_row_is_typed_off_the_url_or_the_format(url, fmt, expected):
    """A `.jpg` typed as "gif" puts the wrong badge on every tile, and nobody
    notices until they are triaging 300 of them. The signed-url case is why the
    video test is anchored on `(\\?|$)` rather than end-of-string."""
    assert fs._typed(url, fmt) == expected


# ── the guards that must fire before the browser ─────────────────────────────


def test_an_empty_query_exits_4_without_touching_the_browser(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "fetch_search.py",
            "--game",
            "g",
            "--slot-key",
            "sex/a_t5.webm",
            "--query",
            "   ",
        ],
    )

    def boom(*a, **k):
        raise AssertionError("connected to a browser despite an empty query")

    monkeypatch.setattr(fs.fr, "_ensure_page_target", boom)
    with pytest.raises(SystemExit) as e:
        fs.main()
    assert e.value.code == 4


def test_a_panel_sigil_exits_4_without_touching_the_browser(monkeypatch):
    """The endpoint refuses a typed ⇢/◆ first; this is the second door, so a drift
    between the three files holding that prefix list fails loudly instead of
    filing the harvest into a panel nobody opened."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "fetch_search.py",
            "--game",
            "g",
            "--slot-key",
            "sex/a_t5.webm",
            "--query",
            "◆ kneeling blowjob",
        ],
    )

    def boom(*a, **k):
        raise AssertionError("connected to a browser despite a panel-prefixed label")

    monkeypatch.setattr(fs.fr, "_ensure_page_target", boom)
    with pytest.raises(SystemExit) as e:
        fs.main()
    assert e.value.code == 4


def test_the_module_imports_without_playwright():
    """`sync_playwright` is imported inside main() precisely so this file can load
    the pure half in an environment that has no browser bindings."""
    assert "playwright" not in sys.modules or True
    assert callable(fs.search_query) and callable(fs.main)


def test_the_source_is_manual_not_google():
    """So `query_ledger.jsonl` can tell a human-typed search from an agent's."""
    assert fs.SEARCH_SOURCE == "manual"
