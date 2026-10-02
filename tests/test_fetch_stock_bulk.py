"""`_stock` in `scripts/fetch_related.py` and `scripts/fetch_pornhub.py` — ONE write.

Both runners used to post one `options/add` per url. Every `options/add` rewrites
the whole shelf under a lock that is global to the game (214 ms/url on a 4.4 MB
store; vesper's is ~30 MB), which is why the ⇢ Related and ◆ PornHub buttons were
slow while the free-text search — already bulk — was fast. These tests pin the
contract that replaced it: one `options/add_bulk` per run, the same typing rule,
and a return value that still means "urls that landed on the shelf".

Loaded by file path like `test_fetch_search.py`, because `scripts/` is not a package.

    pytest tests/test_fetch_stock_bulk.py -q
"""
import importlib.util
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).parent.parent / "scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fr = _load("fetch_related")
ph = _load("fetch_pornhub")

URLS = [
    "https://cdn.example.com/a.gif",
    "https://cdn.example.com/b.webm?sig=abc",
    "https://cdn.example.com/c.mp4",
]


class _Resp:
    def __init__(self, status, body):
        self.status_code = status
        self._body = body
        self.text = str(body)

    def json(self):
        return self._body


def _recorder(monkeypatch, module, status=200, body=None):
    calls = []

    def fake_post(api, endpoint, payload):
        calls.append((endpoint, payload))
        return _Resp(status, body or {"added": 2, "duplicates": 1, "invalid": 0})

    monkeypatch.setattr(module, "_api_post", fake_post)
    return calls


def _run(stock):
    return stock(
        "http://api",
        "g",
        "sex/a_t5.webm",
        "sex/a_t5.webm",
        "⇢ label",
        URLS,
        {URLS[0]: "doc0"},
        {URLS[1]: "thumb1"},
    )


def test_related_stocks_in_one_bulk_call(monkeypatch):
    calls = _recorder(monkeypatch, fr)
    assert _run(fr._stock) == 3  # added + duplicates
    assert len(calls) == 1
    endpoint, payload = calls[0]
    assert endpoint == "options/add_bulk"
    assert payload["query"] == "⇢ label"
    assert payload["slot_key"] == "sex/a_t5.webm"
    assert [i["url"] for i in payload["items"]] == URLS


def test_pornhub_stocks_through_the_same_bulk_call(monkeypatch):
    # fetch_pornhub imports fetch_related as `fr` on its own path, so patch that copy.
    calls = _recorder(monkeypatch, ph.fr)
    assert _run(ph._stock) == 3
    assert [c[0] for c in calls] == ["options/add_bulk"]


def test_items_keep_the_typing_rule_docid_and_thumb(monkeypatch):
    calls = _recorder(monkeypatch, fr)
    _run(fr._stock)
    items = {i["url"]: i for i in calls[0][1]["items"]}
    assert items[URLS[0]]["type"] == "gif" and items[URLS[0]]["media_kind"] == "img"
    # a SIGNED .webm still types as video — the `(\?|$)` anchor
    assert items[URLS[1]]["type"] == "video"
    assert items[URLS[1]]["media_kind"] == "video"
    assert items[URLS[2]]["type"] == "video"
    assert items[URLS[0]]["docid"] == "doc0" and items[URLS[1]]["docid"] == ""
    assert items[URLS[1]]["thumb"] == "thumb1" and items[URLS[0]]["thumb"] == ""


def test_a_refused_bulk_write_exits_6(monkeypatch):
    _recorder(monkeypatch, fr, status=500, body={"error": "boom"})
    with pytest.raises(SystemExit) as e:
        _run(fr._stock)
    assert e.value.code == 6
