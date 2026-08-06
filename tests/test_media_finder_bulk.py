"""`options/add_bulk` — the same shelf, written once instead of N times.

Every `options/add` rewrites the whole ledger, and `_options_lock` is global to the
game. Measured on vesper's live 5.7 MB store (2026-08-06): ~69 ms of pure serialize
per call, ~145 ms projected at 12 MB. An 88-slot harvest posts ~22,000 urls, so the
single-url path spends **~39 minutes holding the lock** — time that is serialized by
construction and that no amount of agent concurrency can overlap.

So this endpoint exists for exactly one reason, and that reason is the first thing
asserted here: **N items must produce ONE write and a byte-identical shelf.** If bulk
and single ever diverge, the fast path is silently a different feature.

The other load-bearing invariant is that a bad row is skipped and COUNTED, never
fatal and never silent. A harvest of 250 urls must not lose 249 because one carried a
`data:` scheme — and a silently-dropped tail reads downstream as "the query was thin",
which is what sends an agent rewriting a query that was fine.

    pytest tests/test_media_finder_bulk.py -q
"""
import json
from unittest.mock import patch

import pytest
from django.test import RequestFactory

import api.v1.media_finder as mf


@pytest.fixture
def games_root(tmp_path, monkeypatch):
    monkeypatch.setattr(mf, "GAMES_ROOT", tmp_path)
    (tmp_path / "g" / "videos").mkdir(parents=True)
    return tmp_path


def _post(view, payload):
    req = RequestFactory().post("/", data=json.dumps(payload), content_type="application/json")
    return view(req)


def _body(resp):
    return json.loads(resp.content)


def _ledger(games_root):
    return mf._read_options(games_root / "g")


def _shelf(games_root, slot):
    return _ledger(games_root)["options"].get(slot) or []


def _bulk(games_root, slot, items, query=None):
    body = {"game": "g", "file": slot, "items": items}
    if query is not None:
        body["query"] = query
    return _post(mf.options_add_bulk, body)


def _single(games_root, slot, url, query=None, **kw):
    body = {"game": "g", "file": slot, "url": url, "media_kind": "img"}
    if query is not None:
        body["query"] = query
    body.update(kw)
    return _post(mf.options_add, body)


def _comparable(entries):
    """Everything about an option except when it landed."""
    return [{k: v for k, v in e.items() if k != "added_at"} for e in entries]


# ── THE test: bulk and single must produce the same shelf ────────────────────

def test_bulk_shelf_is_identical_to_the_same_urls_added_one_at_a_time(games_root):
    urls = [f"https://x.test/{n}.gif" for n in range(12)]
    q = "alley blowjob gif"

    for u in urls:
        _single(games_root, "sex/single_t5.webm", u, query=q)
    _bulk(games_root, "sex/bulk_t5.webm",
          [{"url": u, "media_kind": "img"} for u in urls], query=q)

    assert _comparable(_shelf(games_root, "sex/bulk_t5.webm")) == \
           _comparable(_shelf(games_root, "sex/single_t5.webm"))


def test_bulk_registers_the_query_stub_exactly_like_single(games_root):
    """A `found_by` label with no record is an INVISIBLE BUCKET — the picker groups by
    the query table, so those options are only reachable through "All"."""
    _single(games_root, "sex/single_t5.webm", "https://x.test/a.gif", query="q one")
    _bulk(games_root, "sex/bulk_t5.webm", [{"url": "https://x.test/a.gif"}], query="q one")
    qs = _ledger(games_root)["queries"]
    assert [r["q"] for r in qs["sex/bulk_t5.webm"]] == [r["q"] for r in qs["sex/single_t5.webm"]]


# ── the whole point: one write, not N ────────────────────────────────────────

def test_bulk_writes_the_ledger_exactly_once(games_root):
    items = [{"url": f"https://x.test/{n}.gif"} for n in range(50)]
    with patch.object(mf, "_write_options", wraps=mf._write_options) as w:
        _bulk(games_root, "sex/a_t5.webm", items, query="q")
    assert w.call_count == 1


def test_single_path_still_writes_once_per_url(games_root):
    """The comparison that makes the number above mean something."""
    with patch.object(mf, "_write_options", wraps=mf._write_options) as w:
        for n in range(5):
            _single(games_root, "sex/a_t5.webm", f"https://x.test/{n}.gif", query="q")
    assert w.call_count == 5


def test_a_re_harvest_of_already_stocked_urls_writes_nothing(games_root):
    """The short-circuit that keeps a 400-url re-run from being 400 rewrites."""
    items = [{"url": f"https://x.test/{n}.gif"} for n in range(20)]
    _bulk(games_root, "sex/a_t5.webm", items, query="q")
    with patch.object(mf, "_write_options", wraps=mf._write_options) as w:
        resp = _bulk(games_root, "sex/a_t5.webm", items, query="q")
    assert w.call_count == 0
    assert _body(resp)["duplicates"] == 20 and _body(resp)["added"] == 0


def test_empty_items_is_accepted_and_writes_nothing(games_root):
    with patch.object(mf, "_write_options", wraps=mf._write_options) as w:
        resp = _bulk(games_root, "sex/a_t5.webm", [], query="q")
    assert w.call_count == 0
    assert _body(resp) == {"ok": True, "added": 0, "duplicates": 0, "invalid": 0, "count": 0}


# ── dedup credits the sibling query, same as single ──────────────────────────

def test_a_sibling_query_credits_an_already_stocked_url(games_root):
    """Cross-query duplicates are the common case, not the edge: `found_by` is a LIST."""
    _bulk(games_root, "sex/a_t5.webm", [{"url": "https://x.test/a.gif"}], query="first query")
    resp = _bulk(games_root, "sex/a_t5.webm", [{"url": "https://x.test/a.gif"}], query="second query")
    entry = _shelf(games_root, "sex/a_t5.webm")[0]
    assert entry["found_by"] == ["first query", "second query"]
    assert _body(resp)["added"] == 0 and _body(resp)["duplicates"] == 1
    assert len(_shelf(games_root, "sex/a_t5.webm")) == 1


def test_duplicates_inside_one_request_collapse_to_one_row(games_root):
    resp = _bulk(games_root, "sex/a_t5.webm",
                 [{"url": "https://x.test/a.gif"}] * 4, query="q")
    assert len(_shelf(games_root, "sex/a_t5.webm")) == 1
    assert _body(resp)["added"] == 1 and _body(resp)["duplicates"] == 3


# ── a bad row is skipped and COUNTED, never fatal ────────────────────────────

@pytest.mark.parametrize("bad", [
    {"url": "data:image/gif;base64,AAAA"},
    {"url": "javascript:alert(1)"},
    {"url": ""},
    {},
    "not-a-dict",
])
def test_one_bad_row_does_not_cost_the_good_ones(games_root, bad):
    resp = _bulk(games_root, "sex/a_t5.webm",
                 [{"url": "https://x.test/a.gif"}, bad, {"url": "https://x.test/b.gif"}],
                 query="q")
    assert _body(resp)["added"] == 2
    assert _body(resp)["invalid"] == 1
    assert len(_shelf(games_root, "sex/a_t5.webm")) == 2


def test_over_the_cap_is_REJECTED_not_truncated(games_root):
    """Silent truncation reads downstream as a thin query. Refuse instead."""
    items = [{"url": f"https://x.test/{n}.gif"} for n in range(mf._BULK_MAX_ITEMS + 1)]
    resp = _bulk(games_root, "sex/a_t5.webm", items, query="q")
    assert resp.status_code == 400
    assert _shelf(games_root, "sex/a_t5.webm") == []


def test_items_must_be_a_list(games_root):
    assert _post(mf.options_add_bulk,
                 {"game": "g", "file": "sex/a_t5.webm", "items": {"url": "x"}}).status_code == 400


def test_missing_game_or_file_is_a_400(games_root):
    assert _post(mf.options_add_bulk, {"game": "nope", "file": "a", "items": []}).status_code == 400
    assert _post(mf.options_add_bulk, {"game": "g", "file": "", "items": []}).status_code == 400


# ── docid / thumb validated exactly as the single path does ──────────────────

def test_a_malformed_docid_drops_the_FIELD_not_the_option(games_root):
    _bulk(games_root, "sex/a_t5.webm",
          [{"url": "https://x.test/a.gif", "docid": "no!"}], query="q")
    entry = _shelf(games_root, "sex/a_t5.webm")[0]
    assert entry["url"] == "https://x.test/a.gif" and "docid" not in entry


def test_a_thumb_off_gstatic_is_dropped(games_root):
    """The host pin is load-bearing: the picker PROXIES this url, so an unconstrained
    field would make the shelf a way to aim `proxy` at an arbitrary host."""
    _bulk(games_root, "sex/a_t5.webm",
          [{"url": "https://x.test/a.gif", "thumb": "https://evil.test/t.jpg"}], query="q")
    entry = _shelf(games_root, "sex/a_t5.webm")[0]
    assert "thumb" not in entry


def test_a_gstatic_thumb_and_good_docid_survive(games_root):
    _bulk(games_root, "sex/a_t5.webm", [{
        "url": "https://x.test/a.gif",
        "docid": "AbCd1234_-xy",
        "thumb": "https://encrypted-tbn0.gstatic.com/images?q=tbn:AAA",
    }], query="q")
    entry = _shelf(games_root, "sex/a_t5.webm")[0]
    assert entry["docid"] == "AbCd1234_-xy"
    assert entry["thumb"].startswith("https://encrypted-tbn0.gstatic.com/")


def test_docid_is_first_write_wins_like_the_single_path(games_root):
    _bulk(games_root, "sex/a_t5.webm",
          [{"url": "https://x.test/a.gif", "docid": "AAAAAAAA1111"}], query="q1")
    _bulk(games_root, "sex/a_t5.webm",
          [{"url": "https://x.test/a.gif", "docid": "BBBBBBBB2222"}], query="q2")
    assert _shelf(games_root, "sex/a_t5.webm")[0]["docid"] == "AAAAAAAA1111"


# ── key discipline: the shelf is keyed by slot_key, defaulting to file ───────

def test_slot_key_wins_over_file(games_root):
    _post(mf.options_add_bulk, {"game": "g", "file": "sex/old_path.webm",
                                "slot_key": "sex/stable_id", "query": "q",
                                "items": [{"url": "https://x.test/a.gif"}]})
    assert _shelf(games_root, "sex/stable_id")
    assert _shelf(games_root, "sex/old_path.webm") == []


def test_no_query_is_byte_identical_to_the_unlabelled_write(games_root):
    """~19,300 already-stocked options carry no label; an unlabelled bulk write must
    produce the same four keys the capture extension has always produced."""
    _bulk(games_root, "sex/a_t5.webm", [{"url": "https://x.test/a.gif"}])
    entry = _shelf(games_root, "sex/a_t5.webm")[0]
    assert set(entry) == {"url", "type", "media_kind", "added_at"}
    assert _ledger(games_root)["queries"] == {}


def test_bulk_rejects_GET(games_root):
    assert mf.options_add_bulk(RequestFactory().get("/")).status_code == 405
