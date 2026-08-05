"""Query provenance — every option remembers WHICH SEARCH found it.

A slot's shelf used to be one undifferentiated pile. Three searches ran on
`media_lab_f/scenes/lab_eyecontact_t5.webm` (84 + 77 + 77 urls) and all 226 results
landed in the same list with no record of which search produced which url — so "these
results are wrong" had nowhere to land, because a bad shelf is nearly always ONE bad
query and the page could not say which.

Two invariants are load-bearing and both are asserted here:

  1. **Silent for callers that don't opt in.** ~19,300 options are already stocked with
     no label, and `media_capture_extension/content.js` still posts without one. An
     `options/add` with no `query` must be byte-identical to the pre-2026-08-05 write,
     or this is a migration instead of a feature.
  2. **Nothing is ever destroyed to make a refetch legible.** The query table survives
     `grab`, `options/remove`, `options/clear {before}` and `pool/unselect`; a bucket
     empties to 0 and its record stays, because "this search ran and everything from it
     was thrown away" is a fact worth keeping.

    pytest tests/test_media_finder_queries.py -q
"""
import json
from pathlib import Path
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


def _get(view, qs):
    return view(RequestFactory().get("/?" + qs))


def _ledger(games_root):
    return mf._read_options(games_root / "g")


def _add(games_root, url, query=None, **kw):
    body = {"game": "g", "file": "sex/a_t5.webm", "url": url, "media_kind": "img"}
    if query is not None:
        body["query"] = query
    body.update(kw)
    return _post(mf.options_add, body)


# ── the reader: one normalizer, so a new root can't be forgotten ─────────────

def test_read_options_shapes_a_missing_file(games_root):
    data = mf._read_options(games_root / "g")
    assert data["options"] == {} and data["queries"] == {}


def test_read_options_shapes_a_corrupt_file(games_root):
    p = games_root / "g" / ".find-media" / "media_options.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{not json")
    data = mf._read_options(games_root / "g")
    assert data["options"] == {} and data["queries"] == {}


def test_read_options_shapes_a_legacy_file(games_root):
    """THE migration test: every one of the 10 live ledgers has exactly these three
    roots. They must read correctly with zero writes."""
    p = games_root / "g" / ".find-media" / "media_options.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({
        "game": "g", "updated_at": "2026-08-01T00:00:00+00:00",
        "options": {"sex/a_t5.webm": [{"url": "https://x.test/a.gif", "type": "gif",
                                       "media_kind": "img", "added_at": "2026-08-01T00:00:00+00:00"}]},
    }))
    data = mf._read_options(games_root / "g")
    assert data["queries"] == {}
    assert len(data["options"]["sex/a_t5.webm"]) == 1
    assert "found_by" not in data["options"]["sex/a_t5.webm"][0]


# ── options/add: opt-in, and the label is a LIST ─────────────────────────────

def test_add_without_a_query_is_byte_identical(games_root):
    _add(games_root, "https://x.test/a.gif")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert set(entry) == {"url", "type", "media_kind", "added_at"}


def test_add_with_a_query_tags_the_entry(games_root):
    _add(games_root, "https://x.test/a.gif", query="alley blowjob gif")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert entry["found_by"] == ["alley blowjob gif"]


def test_a_second_query_finding_the_same_url_appends_to_found_by(games_root):
    """Dedup is by url, so a sibling query legitimately re-finding a stocked url is
    the COMMON case. A single-valued field would hide that result under chip #2."""
    _add(games_root, "https://x.test/a.gif", query="q one")
    res = _add(games_root, "https://x.test/a.gif", query="q two")

    body = json.loads(res.content)
    assert body["duplicate"] is True and body["count"] == 1
    opts = _ledger(games_root)["options"]["sex/a_t5.webm"]
    assert len(opts) == 1 and opts[0]["found_by"] == ["q one", "q two"]


def test_re_running_the_same_query_writes_nothing(games_root):
    """The no-op short-circuit is load-bearing, not an optimization: without it a
    re-harvest of 400 already-stocked urls becomes 400 whole-file rewrites of a
    2.9 MB ledger, one per url, all under the lock."""
    _add(games_root, "https://x.test/a.gif", query="q one")
    before = _ledger(games_root)["updated_at"]
    _add(games_root, "https://x.test/a.gif", query="q one")
    assert _ledger(games_root)["updated_at"] == before


def test_add_auto_registers_an_unseen_query(games_root):
    """A `found_by` label with no record is an invisible bucket — the picker groups by
    the query table, so those options would only be reachable through All."""
    _add(games_root, "https://x.test/a.gif", query="q one")
    recs = _ledger(games_root)["queries"]["sex/a_t5.webm"]
    assert len(recs) == 1
    assert recs[0]["q"] == "q one" and recs[0]["auto"] is True and recs[0]["runs"] == 1


def test_auto_registration_does_not_count_options_as_runs(games_root):
    for i in range(5):
        _add(games_root, f"https://x.test/{i}.gif", query="q one")
    recs = _ledger(games_root)["queries"]["sex/a_t5.webm"]
    assert len(recs) == 1 and recs[0]["runs"] == 1


def test_query_text_is_whitespace_canonicalized_but_not_case_folded(games_root):
    _add(games_root, "https://x.test/a.gif", query="  alley   blowjob gif ")
    _add(games_root, "https://x.test/b.gif", query="alley blowjob gif")
    _add(games_root, "https://x.test/c.gif", query="Alley blowjob gif")
    recs = _ledger(games_root)["queries"]["sex/a_t5.webm"]
    assert [r["q"] for r in recs] == ["alley blowjob gif", "Alley blowjob gif"]


def test_a_previous_pick_carries_no_found_by(games_root):
    """Undo history is not a search result. Filing it under a query would be a
    category error, and it is reachable through All."""
    mf._add_option(games_root / "g", "g", "sex/a_t5.webm", url="/games/g/.find-media/previous/x.gif",
                   local_path="g/.find-media/previous/x.gif", origin="previous", query="q one")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert "found_by" not in entry
    assert _ledger(games_root)["queries"].get("sex/a_t5.webm") in (None, [])


# ── queries/add ──────────────────────────────────────────────────────────────

def _q(games_root, query="q one", **kw):
    body = {"game": "g", "file": "sex/a_t5.webm", "query": query}
    body.update(kw)
    return _post(mf.queries_add, body)


def test_queries_add_records_a_zero_yield_search(games_root):
    """The record that stops a dead query being re-run three rounds later. It has no
    options at all, so nothing else in the system would remember it."""
    res = _q(games_root, "leaning forward gif", urls=0, stocked=0, hosts=[])
    assert json.loads(res.content)["ok"] is True
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["urls"] == 0 and rec["stocked"] == 0
    assert _ledger(games_root)["options"].get("sex/a_t5.webm") in (None, [])


def test_queries_add_upserts_and_bumps_runs(games_root):
    _q(games_root, urls=84, stocked=41)
    first = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]["at"]
    res = _q(games_root, urls=90, stocked=12)

    assert json.loads(res.content)["duplicate"] is True
    recs = _ledger(games_root)["queries"]["sex/a_t5.webm"]
    assert len(recs) == 1
    assert recs[0]["at"] == first          # first run never moves
    assert recs[0]["runs"] == 2
    assert recs[0]["urls"] == 90 and recs[0]["stocked"] == 12   # newest evidence wins


def test_enriching_an_auto_stub_is_not_a_second_run(games_root):
    """The stock loop opens the stub, then `queries/add` describes that SAME run."""
    _add(games_root, "https://x.test/a.gif", query="q one")
    _q(games_root, "q one", urls=84, stocked=1)
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["runs"] == 1 and "auto" not in rec and rec["urls"] == 84


def test_queries_add_stores_real_hostnames_and_echoes_none(games_root):
    """The caller is a javascript_tool REPL whose RETURN VALUE passes a secret-scanner
    that redacts bare dotted hostnames — echoing them would blank the confirmation."""
    res = _q(games_root, hosts=[["i.xgroovy.com", 12], ["nsfwgify.com", 9]])
    assert "xgroovy" not in res.content.decode()
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["hosts"] == [["i.xgroovy.com", 12], ["nsfwgify.com", 9]]


def test_queries_add_refuses_a_DOT_transformed_host(games_root):
    """Irreversible if it lands: a host legitimately containing " DOT " is
    indistinguishable from a mangled one, so nothing could ever undo it."""
    res = _q(games_root, hosts=[["i DOT xgroovy DOT com", 12]])
    assert res.status_code == 400
    assert "DOT" in json.loads(res.content)["error"]
    assert _ledger(games_root)["queries"] == {}


@pytest.mark.parametrize("bad", [
    "notalist",
    [["host"]],
    [["host", "notanint"]],
    [[123, 4]],
    [["x" * 300, 4]],
])
def test_queries_add_drops_a_malformed_histogram_but_keeps_the_record(games_root, bad):
    res = _q(games_root, hosts=bad)
    assert res.status_code == 200
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert "hosts" not in rec


def test_queries_add_keys_on_slot_key_not_file(games_root):
    _post(mf.queries_add, {"game": "g", "file": "sex/a_t5.webm", "slot_key": "renner_oral",
                           "query": "q one"})
    qs = _ledger(games_root)["queries"]
    assert "renner_oral" in qs and "sex/a_t5.webm" not in qs


def test_queries_add_requires_a_game_and_a_query(games_root):
    assert _post(mf.queries_add, {"game": "g", "file": "sex/a_t5.webm", "query": "  "}).status_code == 400
    assert _post(mf.queries_add, {"game": "nope", "file": "a", "query": "q"}).status_code == 400


def test_queries_add_appends_the_durable_ledger_line(games_root):
    """media_options.json is rewritten whole and reads back EMPTY if torn, so the
    append-only jsonl is the copy that survives. Writing it here is also what makes
    the skill's "machine-written record" claim true for the first time."""
    _q(games_root, "alley blowjob gif", source="google", urls=84, round=2)
    lines = (games_root / "g" / ".find-media" / "query_ledger.jsonl").read_text().strip().split("\n")
    row = json.loads(lines[0])
    assert row["slot"] == "sex/a_t5.webm"
    assert row["query"] == "alley blowjob gif"
    assert row["urls_yielded"] == 84 and row["round"] == 2 and row["source"] == "google"
    assert len(row["date"]) == 10        # day granularity, same as the hand-written schema

    _q(games_root, "second gif")
    lines = (games_root / "g" / ".find-media" / "query_ledger.jsonl").read_text().strip().split("\n")
    assert len(lines) == 2               # append-only, never rewritten


# ── survival across every write path ─────────────────────────────────────────

def _seed(games_root):
    _add(games_root, "https://x.test/a.gif", query="q one")
    _q(games_root, "q one", urls=84, stocked=1, hosts=[["x.test", 1]])


def test_grab_preserves_the_query_table(games_root):
    _seed(games_root)

    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {"game": "g", "file": "sex/a_t5.webm", "url": "https://x.test/a.gif"})
    assert json.loads(res.content)["success"]
    assert _ledger(games_root)["queries"]["sex/a_t5.webm"][0]["q"] == "q one"


def test_options_remove_preserves_the_table_and_restamps_game(games_root):
    _seed(games_root)
    _post(mf.options_remove, {"game": "g", "file": "sex/a_t5.webm", "url": "https://x.test/a.gif"})
    data = _ledger(games_root)
    assert data["options"]["sex/a_t5.webm"] == []
    assert data["queries"]["sex/a_t5.webm"][0]["q"] == "q one"   # bucket empties to 0, chip stays
    assert data["game"] == "g"


def test_options_clear_before_preserves_the_table(games_root):
    _seed(games_root)
    _post(mf.options_clear, {"game": "g", "file": "sex/a_t5.webm"})
    data = _ledger(games_root)
    assert data["options"]["sex/a_t5.webm"] == []
    assert len(data["queries"]["sex/a_t5.webm"]) == 1


def test_pool_unselect_preserves_the_table(games_root):
    _post(mf.queries_add, {"game": "g", "slot_key": "sex/pool_t5", "query": "q one"})
    pool = games_root / "g" / "videos" / "sex" / "pool_t5"
    pool.mkdir(parents=True)
    (pool / "c1.gif").write_bytes(b"\x00" * 2000)
    res = _post(mf.pool_unselect, {"game": "g", "dir": "sex/pool_t5", "filename": "c1.gif"})
    assert json.loads(res.content)["success"]
    assert _ledger(games_root)["queries"]["sex/pool_t5"][0]["q"] == "q one"


# ── options/list ─────────────────────────────────────────────────────────────

def test_options_list_returns_both_arrays(games_root):
    _seed(games_root)
    body = json.loads(_get(mf.options_list, "game=g&file=sex/a_t5.webm").content)
    assert len(body["options"]) == 1 and len(body["queries"]) == 1
    assert body["options"][0]["found_by"] == ["q one"]


def test_options_list_on_an_unknown_slot_returns_empty_arrays(games_root):
    body = json.loads(_get(mf.options_list, "game=g&file=nope").content)
    assert body == {"options": [], "queries": []}


# ── docid: Google's index id, captured at harvest, first-write-wins ──────────

def test_add_with_docid_stores_it(games_root):
    _add(games_root, "https://x.test/a.gif", query="q one", docid="FvF5n0MlBjcrfM")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert entry["docid"] == "FvF5n0MlBjcrfM"


def test_add_without_docid_leaves_no_docid_key(games_root):
    _add(games_root, "https://x.test/a.gif", query="q one")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert "docid" not in entry
    assert set(entry) == {"url", "type", "media_kind", "added_at", "found_by"}


def test_duplicate_add_enriches_a_missing_docid(games_root):
    _add(games_root, "https://x.test/a.gif", query="q one")
    _add(games_root, "https://x.test/a.gif", query="q one", docid="FvF5n0MlBjcrfM")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert entry["docid"] == "FvF5n0MlBjcrfM"
    assert entry["found_by"] == ["q one"]  # no double-append


def test_duplicate_add_with_docid_and_no_query_still_writes(games_root):
    """Enriching a shelved url with a docid must not require a query. The dup
    branch used to return on empty q before looking at anything else, which
    silently swallowed the write."""
    _add(games_root, "https://x.test/a.gif")
    _add(games_root, "https://x.test/a.gif", docid="FvF5n0MlBjcrfM")
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert entry["docid"] == "FvF5n0MlBjcrfM"
    assert "found_by" not in entry


def test_docid_is_never_overwritten(games_root):
    _add(games_root, "https://x.test/a.gif", docid="FvF5n0MlBjcrfM")
    _add(games_root, "https://x.test/a.gif", docid="l1dWn_tdD1UkwM")
    assert _ledger(games_root)["options"]["sex/a_t5.webm"][0]["docid"] == "FvF5n0MlBjcrfM"


def test_identical_duplicate_add_writes_nothing(games_root):
    _add(games_root, "https://x.test/a.gif", query="q one", docid="FvF5n0MlBjcrfM")
    before = _ledger(games_root)["updated_at"]
    _add(games_root, "https://x.test/a.gif", query="q one", docid="FvF5n0MlBjcrfM")
    assert _ledger(games_root)["updated_at"] == before


@pytest.mark.parametrize("bad", ["short", "has space", "has.dot", "x" * 65, "⇢nope"])
def test_malformed_docid_is_dropped_but_option_stored(games_root, bad):
    res = _add(games_root, "https://x.test/a.gif", query="q one", docid=bad)
    assert json.loads(res.content)["ok"]
    entry = _ledger(games_root)["options"]["sex/a_t5.webm"][0]
    assert "docid" not in entry


# ── seed_url: what marks a related-fetch record, and the 409 guard ───────────

def test_queries_add_stores_seed_url(games_root):
    _q(games_root, "⇢ a", source="related", seed_url="https://x.test/a.gif", urls=51)
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["seed_url"] == "https://x.test/a.gif"
    assert rec["source"] == "related"


@pytest.mark.parametrize("bad", ["ftp://x.test/a.gif", "not-a-url", "https://x.test/" + "a" * 2048])
def test_queries_add_refuses_a_bad_seed_url(games_root, bad):
    res = _q(games_root, "⇢ a", source="related", seed_url=bad)
    assert res.status_code == 400


def test_related_top_up_bumps_runs_and_keeps_seed_url(games_root):
    _q(games_root, "⇢ a", source="related", seed_url="https://x.test/a.gif", urls=51)
    _q(games_root, "⇢ a", source="related", seed_url="https://x.test/a.gif", urls=60)
    recs = _ledger(games_root)["queries"]["sex/a_t5.webm"]
    assert len(recs) == 1
    assert recs[0]["runs"] == 2 and recs[0]["urls"] == 60
    assert recs[0]["seed_url"] == "https://x.test/a.gif"


def test_queries_add_refuses_a_label_collision(games_root):
    """Same label, DIFFERENT seed → 409, and the first seed's record is untouched.
    Without the guard, _upsert_query's update() would silently reseat the chip."""
    _q(games_root, "⇢ a", source="related", seed_url="https://x.test/1/a.gif")
    res = _q(games_root, "⇢ a", source="related", seed_url="https://x.test/2/a.gif")
    assert res.status_code == 409
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["seed_url"] == "https://x.test/1/a.gif" and rec["runs"] == 1


def test_collision_guard_lets_a_stub_be_adopted(games_root):
    """The stock loop auto-registers the label as a seedless stub; the closing
    queries/add enriches that SAME run — it must not read as a collision."""
    _add(games_root, "https://y.test/r1.gif", query="⇢ a")
    res = _q(games_root, "⇢ a", source="related", seed_url="https://x.test/a.gif", urls=51)
    assert res.status_code == 200
    rec = _ledger(games_root)["queries"]["sex/a_t5.webm"][0]
    assert rec["seed_url"] == "https://x.test/a.gif" and rec["runs"] == 1


def test_seed_url_lands_in_the_jsonl_ledger(games_root):
    _q(games_root, "⇢ a", source="related", seed_url="https://x.test/a.gif")
    lines = (games_root / "g" / ".find-media" / "query_ledger.jsonl").read_text().splitlines()
    row = json.loads(lines[-1])
    assert row["seed_url"] == "https://x.test/a.gif" and row["source"] == "related"


# ── related/fetch: the orchestrator, subprocess mocked ───────────────────────

class _Proc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def _rf(payload=None):
    body = {"game": "g", "file": "sex/a_t5.webm", "url": "https://x.test/a.gif"}
    body.update(payload or {})
    return _post(mf.related_fetch, body)


def test_related_fetch_runner_down_is_a_fast_503_with_the_launch_command(games_root):
    with patch.object(mf.requests, "get", side_effect=mf.requests.ConnectionError("no")):
        res = _rf()
    assert res.status_code == 503
    assert "chrome-find-media" in json.loads(res.content)["error"]


def test_related_fetch_relays_the_runner_result(games_root):
    out = json.dumps({"ok": True, "label": "⇢ a", "urls": 51, "stocked": 41})
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(0, stdout="note\n" + out)):
        res = _rf()
    body = json.loads(res.content)
    assert body["ok"] and body["label"] == "⇢ a" and body["stocked"] == 41


def test_related_fetch_maps_captcha_to_502(games_root):
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(3, stderr="captcha")):
        res = _rf()
    assert res.status_code == 502


def test_related_fetch_maps_missing_docid_to_404(games_root):
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(4, stderr="not in grid")):
        res = _rf()
    assert res.status_code == 404


def test_related_fetch_timeout_is_a_504(games_root):
    exc = mf.subprocess.TimeoutExpired(cmd="fetch_related.py", timeout=180)
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", side_effect=exc):
        res = _rf()
    assert res.status_code == 504


def test_related_fetch_garbage_stdout_is_a_500_not_a_crash(games_root):
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(0, stdout="")):
        res = _rf()
    assert res.status_code == 500


def test_related_fetch_second_concurrent_call_is_a_429(games_root):
    """One browser, one fetch: while the lock is held the endpoint refuses fast
    instead of queueing a second CDP client onto the runner's one websocket."""
    with patch.object(mf.requests, "get"):
        mf._RELATED_FETCH_LOCK.acquire()
        try:
            res = _rf()
        finally:
            mf._RELATED_FETCH_LOCK.release()
    assert res.status_code == 429
    assert "one fetch at a time" in json.loads(res.content)["error"]


def test_related_fetch_releases_the_lock_after_a_run(games_root):
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(0, stdout='{"ok": true}')):
        _rf()
    assert mf._RELATED_FETCH_LOCK.acquire(blocking=False)
    mf._RELATED_FETCH_LOCK.release()


def test_related_fetch_cdp_failure_message_is_readable_not_a_ws_log(games_root):
    """Exit 5 used to relay the stderr TAIL — which is playwright's websocket log,
    so the tile showed `<ws disconnected> code=1000` and the real sentence had been
    truncated away. The endpoint owns this message now; the log rides in `detail`."""
    noise = "x" * 500 + "<ws disconnected> ws://localhost:9222/devtools/browser/abc code=1000"
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(5, stderr=noise)):
        res = _rf()
    body = json.loads(res.content)
    assert res.status_code == 503
    assert "<ws" not in body["error"] and "could not be driven" in body["error"]
    assert "<ws" in body["detail"]


def test_related_fetch_sanitized_feed_names_the_profile_not_the_query(games_root):
    with patch.object(mf.requests, "get"), \
         patch.object(mf.subprocess, "run", return_value=_Proc(7, stderr="only 2 urls")):
        res = _rf()
    body = json.loads(res.content)
    assert res.status_code == 503 and "SafeSearch" in body["error"]
