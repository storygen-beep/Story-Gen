"""The human's own search — `search/fetch` — and the runner plumbing it shares.

Two things are tested here, and the first one matters beyond this feature.

**The parametrized `_RUNNERS` suite.** `related_fetch`, `pornhub_fetch` and
`search_fetch` were three copies of the same ~40 lines of preflight / lock /
shell / exit-code mapping until the third caller made that indefensible; they now
share `_run_runner`. The copies had already cost something measurable: exit 5's
message had to be fixed once (it was relaying playwright's websocket log into a
user-facing tile) and the fix landed in only one of the two places it lived.
`pornhub_fetch` had ZERO tests at the time this file was written, while
`related_fetch` had ten. Parametrizing the shared shapes across all three fixes
that asymmetry and pins the factoring.

The ten `related_fetch` tests in test_media_finder_queries.py are deliberately
left exactly as they were — they are the regression proof that the refactor
preserved behaviour, and duplicating them here would weaken that.

**Format resolution.** `_resolve_format` decides whether a slot wants animation,
and it must NOT read `media_kind`: `_IMAGE_SUFFIXES` contains `.gif`, so a `_t5`
gif pool reports as "img" while being animated. Reading the kind instead of the
suffix would search that pool as stills and drop `gif` from the query — the exact
query-poisoning the axis exists to prevent. `test_a_gif_pool_is_animated_not_still`
is the one that catches it.

    pytest tests/test_media_finder_search.py -q
"""
import json
from unittest.mock import patch

import pytest
from django.test import RequestFactory

import api.v1.media_finder as mf

SLOT = "sex/a_t5.webm"


@pytest.fixture
def games_root(tmp_path, monkeypatch):
    monkeypatch.setattr(mf, "GAMES_ROOT", tmp_path)
    (tmp_path / "g" / "videos").mkdir(parents=True)
    return tmp_path


def _post(view, payload):
    req = RequestFactory().post(
        "/", data=json.dumps(payload), content_type="application/json"
    )
    return view(req)


def _body(res):
    return json.loads(res.content)


class _Proc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def _sf(payload=None):
    body = {"game": "g", "file": SLOT, "query": "kneeling blowjob"}
    body.update(payload or {})
    return _post(mf.search_fetch, body)


# ── the shared runner plumbing, across every runner ──────────────────────────
#
# One row per endpoint, carrying only what makes its request valid. Everything
# asserted below is owned by `_run_runner`, so a divergence between the three is
# exactly what these are for.
_RUNNERS = [
    (mf.related_fetch, {"url": "https://x.test/a.gif"}),
    (mf.pornhub_fetch, {"query": "kneeling gif"}),
    (mf.search_fetch, {"query": "kneeling gif"}),
]
_RUNNER_IDS = ["related", "pornhub", "search"]


def _run(view, extra):
    body = {"game": "g", "file": SLOT}
    body.update(extra)
    return _post(view, body)


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_runner_down_is_a_fast_503_with_the_launch_command(games_root, view, extra):
    with patch.object(
        mf.requests, "get", side_effect=mf.requests.ConnectionError("no")
    ):
        res = _run(view, extra)
    assert res.status_code == 503
    assert "chrome-find-media" in _body(res)["error"]


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_a_second_concurrent_call_is_a_429(games_root, view, extra):
    """One browser, one fetch — whichever runner. Concurrent CDP clients contend
    on the runner's single debug websocket and lose intermittently."""
    with patch.object(mf.requests, "get"):
        mf._RELATED_FETCH_LOCK.acquire()
        try:
            res = _run(view, extra)
        finally:
            mf._RELATED_FETCH_LOCK.release()
    assert res.status_code == 429
    assert "one fetch at a time" in _body(res)["error"]


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_the_lock_is_released_after_a_run(games_root, view, extra):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout='{"ok": true}')
    ):
        _run(view, extra)
    assert mf._RELATED_FETCH_LOCK.acquire(blocking=False)
    mf._RELATED_FETCH_LOCK.release()


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_a_timeout_is_a_504(games_root, view, extra):
    exc = mf.subprocess.TimeoutExpired(cmd="runner.py", timeout=180)
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", side_effect=exc
    ):
        res = _run(view, extra)
    assert res.status_code == 504


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_garbage_stdout_is_a_500_not_a_crash(games_root, view, extra):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout="")
    ):
        res = _run(view, extra)
    assert res.status_code == 500


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_cdp_failure_reads_as_a_sentence_not_a_websocket_log(games_root, view, extra):
    """Exit 5 used to relay the stderr TAIL, which is playwright's websocket log,
    so the tile showed `<ws disconnected> code=1000` and the real sentence had been
    truncated away. The helper owns this message; the log rides in `detail`."""
    noise = (
        "x" * 500
        + "<ws disconnected> ws://localhost:9222/devtools/browser/abc code=1000"
    )
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(5, stderr=noise)
    ):
        res = _run(view, extra)
    body = _body(res)
    assert res.status_code == 503
    assert "<ws" not in body["error"] and "could not be driven" in body["error"]
    assert "<ws" in body["detail"]


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_an_unmapped_nonzero_exit_is_a_500(games_root, view, extra):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(9, stderr="boom")
    ):
        res = _run(view, extra)
    assert res.status_code == 500 and "exited 9" in _body(res)["error"]


@pytest.mark.parametrize("view,extra", _RUNNERS, ids=_RUNNER_IDS)
def test_a_leading_dash_value_is_joined_with_equals(games_root, view, extra):
    """⚠️ argparse REJECTS `--query -cartoon` ("expected one argument") and exits 2,
    which would surface as a bare `500 runner exited 2`. `-word` is ordinary Google
    negation syntax, so a free-text box makes this reachable, not theoretical.
    `--flag=value` is never re-scanned for option-likeness."""
    extra = dict(extra)
    if "query" in extra:
        extra["query"] = "-cartoon"
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout='{"ok": true}')
    ) as run:
        _run(view, extra)
    argv = run.call_args[0][0]
    for arg in argv:
        assert (
            arg != "-cartoon"
        ), "a leading-dash value was passed as its own argv element"
    assert not any(
        a.startswith("-")
        and " " not in a
        and "=" not in a
        and a not in ("--game", "--slot-key", "--file", "--format")
        for a in argv[2:]
    ), argv


# ── search/fetch: what is NOT shared ─────────────────────────────────────────


def test_it_relays_the_runner_result(games_root):
    out = json.dumps({"ok": True, "label": "kneeling gif", "urls": 380, "stocked": 341})
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout="note\n" + out)
    ):
        res = _sf()
    body = _body(res)
    assert body["ok"] and body["label"] == "kneeling gif" and body["stocked"] == 341


def test_it_shells_fetch_search_with_the_resolved_format(games_root):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout='{"ok": true}')
    ) as run:
        _sf()
    argv = run.call_args[0][0]
    assert "fetch_search.py" in argv[1]
    assert "--format" in argv and argv[argv.index("--format") + 1] == "animated"
    assert "--query=kneeling blowjob" in argv


def test_captcha_is_a_502(games_root):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(3, stderr="captcha")
    ):
        assert _sf().status_code == 502


def test_zero_urls_names_the_slots_format_not_the_query(games_root):
    """The most likely real failure of a free-text box: the search worked and the
    extractor found nothing of the right KIND. Saying "bad query" would send the
    human to rewrite terms that were fine."""
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(4, stderr="none")
    ):
        res = _sf()
    assert res.status_code == 404
    assert "ANIMATED" in _body(res)["error"]


def test_zero_urls_on_a_still_slot_names_stills(games_root):
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(4, stderr="none")
    ):
        res = _sf({"file": "scenes/room_base.jpg"})
    assert res.status_code == 404
    assert "STILL" in _body(res)["error"]


def test_the_thin_result_sentence_admits_both_readings(games_root):
    """The site:-scoped copies accuse the profile with certainty. Unscoped, a thin
    result can also just be a thin query, and the sentence must not lie."""
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(7, stderr="only 2 urls")
    ):
        res = _sf()
    body = _body(res)
    assert res.status_code == 503
    assert "SafeSearch" in body["error"] and "thin query" in body["error"]


def test_get_is_405(games_root):
    assert mf.search_fetch(RequestFactory().get("/")).status_code == 405


@pytest.mark.parametrize(
    "payload",
    [
        {"query": ""},
        {"query": "   "},
        {"query": "x" * 201},
        # Only control characters that SURVIVE whitespace collapse — `\n` and `\t` are
        # folded to a space by `" ".join(query.split())` before the guard runs, which
        # makes a pasted multi-line query a legitimate single-line one.
        {"query": "kneeling\x00gif"},
        {"query": "kneeling\x07gif"},
        {"file": "", "slot_key": ""},
    ],
)
def test_bad_input_is_a_400(games_root, payload):
    # The mock is the POINT, not scaffolding: every refusal here must land before
    # the runner is touched. Without it, a guard that silently stopped working
    # would spawn a real Chrome and run a real Google search from the test suite —
    # which is exactly what happened while writing this file.
    with patch.object(mf.subprocess, "run") as run:
        res = _sf(payload)
    assert res.status_code == 400
    assert run.call_count == 0, "a rejected request still reached the runner"


def test_a_pasted_newline_is_collapsed_not_rejected(games_root):
    """`\\n` and `\\t` fold into spaces before the control-character guard, so a
    query pasted out of a document is a valid one-line query rather than a 400."""
    with patch.object(mf.requests, "get"), patch.object(
        mf.subprocess, "run", return_value=_Proc(0, stdout='{"ok": true}')
    ) as run:
        res = _sf({"query": "kneeling\nblowjob"})
    assert res.status_code == 200
    assert "--query=kneeling blowjob" in run.call_args[0][0]


@pytest.mark.parametrize("query", ["◆ kneeling gif", "⇢ kneeling gif"])
def test_a_typed_panel_sigil_is_refused_before_chrome_is_spawned(games_root, query):
    """A ⇢/◆ prefix files a bucket into a side panel purely on its label. A typed
    one would vanish off the shelf it was meant to land on, with no error anywhere.
    Only a human can type one, so only this endpoint has to refuse it."""
    with patch.object(mf.subprocess, "run") as run:
        res = _sf({"query": query})
    assert res.status_code == 400
    assert run.call_count == 0, "Chrome was spawned for a query that could never land"


def test_a_bad_game_is_a_400(games_root):
    assert _sf({"game": "../etc"}).status_code == 400


# ── format resolution ────────────────────────────────────────────────────────


def _fmt(games_root, slot, file_="", declared=""):
    return mf._resolve_format(games_root / "g", slot, file_ or slot, declared)


@pytest.mark.parametrize(
    "slot,expected",
    [
        ("sex/a_t5.webm", "animated"),
        ("sex/a_t5.mp4", "animated"),
        ("sex/a_t5.gif", "animated"),
        ("scenes/room_base.jpg", "still"),
        ("scenes/room_base.JPG", "still"),
        ("scenes/room_base.png", "still"),
        ("scenes/room_base.webp", "still"),
    ],
)
def test_a_single_slot_resolves_off_its_suffix(games_root, slot, expected):
    assert _fmt(games_root, slot) == expected


def test_an_explicit_format_wins(games_root):
    assert _fmt(games_root, "sex/a_t5.webm", declared="still") == "still"
    assert _fmt(games_root, "scenes/room_base.jpg", declared="animated") == "animated"


def test_a_nonsense_declared_format_falls_through_to_the_suffix(games_root):
    assert _fmt(games_root, "scenes/room_base.jpg", declared="banana") == "still"


def test_a_pool_resolves_off_its_first_member(games_root):
    pool = games_root / "g" / "videos" / "sex" / "oral_t5"
    pool.mkdir(parents=True)
    (pool / "c1.jpg").write_bytes(b"x")
    assert _fmt(games_root, "sex/oral_t5") == "still"


def test_a_gif_pool_is_animated_not_still(games_root):
    """⚠️ THE trap. `_IMAGE_SUFFIXES` contains `.gif`, so this pool reports
    media_kind "img" — reading the KIND instead of the SUFFIX would search a
    `_t5` gif pool as stills and strip `gif` from the query."""
    pool = games_root / "g" / "videos" / "sex" / "oral_t5"
    pool.mkdir(parents=True)
    (pool / "c1.gif").write_bytes(b"x")
    assert _fmt(games_root, "sex/oral_t5") == "animated"


def test_an_empty_pool_falls_back_to_animated(games_root):
    (games_root / "g" / "videos" / "sex" / "oral_t5").mkdir(parents=True)
    assert _fmt(games_root, "sex/oral_t5") == "animated"


def test_an_unknown_slot_falls_back_to_animated(games_root):
    assert _fmt(games_root, "sex/nothing_here") == "animated"


def test_the_declared_file_answers_when_the_slot_key_is_an_id(games_root):
    """A tagged slot's key carries no extension; `file` still says where the bytes
    go, and that is the one with a suffix to read."""
    assert _fmt(games_root, "stable-id", file_="scenes/room_base.jpg") == "still"
