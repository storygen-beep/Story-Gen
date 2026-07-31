"""The find-media JSON ledgers must survive concurrent writers.

Before `apps/common/json_ledger.py`, both ledgers were unlocked read-modify-write
staging through a SHARED tmp filename. Measured over the real HTTP path, 40
concurrent adds to one shelf: 25x200 / 15x500, and only **16 of 40** landed —
nine of those "200 OK" responses had silently discarded their candidate.

That mattered the moment find-media ran more than one slot at a time. These tests
pin both halves of the fix: no lost updates (the lock), and no writer stealing
another's staging file (the pid+thread tmp name).
"""
import json
import threading
from pathlib import Path

import pytest

from api.v1.media_finder import _add_option, _drop_option, _options_path, _read_options
from apps.common.json_ledger import ledger_lock, write_json_atomic


@pytest.fixture()
def game_dir(tmp_path: Path) -> Path:
    d = tmp_path / "fakegame"
    (d / ".find-media").mkdir(parents=True)
    return d


def _run_concurrently(fns):
    """Start every callable at once and surface anything they raise."""
    errors = []

    def wrap(fn):
        def inner():
            try:
                fn()
            except Exception as exc:  # noqa: BLE001 — the assertion is "nothing raised"
                errors.append(exc)

        return inner

    threads = [threading.Thread(target=wrap(fn)) for fn in fns]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return errors


def test_forty_concurrent_adds_all_land(game_dir: Path):
    """The exact case that lost 24 of 40. Every distinct url must survive."""
    n = 40
    errors = _run_concurrently(
        [
            (
                lambda i=i: _add_option(
                    game_dir,
                    "fakegame",
                    f"sex/slot_{i % 4}",
                    url=f"https://example.com/{i}.gif",
                )
            )
            for i in range(n)
        ]
    )

    assert errors == [], f"writers raised: {errors!r}"
    data = _read_options(game_dir)
    landed = sum(len(v) for v in data["options"].values())
    assert landed == n, f"lost {n - landed} of {n} options"

    urls = {o["url"] for lst in data["options"].values() for o in lst}
    assert urls == {f"https://example.com/{i}.gif" for i in range(n)}


def test_concurrent_adds_to_one_slot_all_land(game_dir: Path):
    """Same shelf key for every writer — maximum contention on one list."""
    n = 30
    errors = _run_concurrently(
        [
            (
                lambda i=i: _add_option(
                    game_dir,
                    "fakegame",
                    "sex/one_slot",
                    url=f"https://example.com/{i}.gif",
                )
            )
            for i in range(n)
        ]
    )

    assert errors == []
    assert len(_read_options(game_dir)["options"]["sex/one_slot"]) == n


def test_concurrent_add_and_drop_leave_a_valid_ledger(game_dir: Path):
    """Mixed mutations must never produce an unparseable file.

    `_read_options` swallows a parse error and returns {} — a torn ledger reads
    back as an EMPTY shelf, so corruption here is silent total loss, not a crash.
    """
    for i in range(20):
        _add_option(
            game_dir, "fakegame", "sex/mixed", url=f"https://example.com/{i}.gif"
        )

    errors = _run_concurrently(
        [
            (
                lambda i=i: _add_option(
                    game_dir,
                    "fakegame",
                    "sex/mixed",
                    url=f"https://example.com/new{i}.gif",
                )
            )
            for i in range(15)
        ]
        + [
            (
                lambda i=i: _drop_option(
                    game_dir,
                    "fakegame",
                    "sex/mixed",
                    url=f"https://example.com/{i}.gif",
                )
            )
            for i in range(20)
        ]
    )

    assert errors == []
    raw = _options_path(game_dir).read_text(encoding="utf-8")
    parsed = json.loads(raw)  # must not raise — that is the whole point
    assert len(parsed["options"]["sex/mixed"]) == 15


def test_no_stray_tmp_files_left_behind(game_dir: Path):
    """A shared tmp name is what produced the 15 hard 500s."""
    _run_concurrently(
        [
            (
                lambda i=i: _add_option(
                    game_dir, "fakegame", "sex/slot", url=f"https://example.com/{i}.gif"
                )
            )
            for i in range(20)
        ]
    )
    leftovers = [
        p.name for p in (game_dir / ".find-media").iterdir() if p.name.endswith(".tmp")
    ]
    assert leftovers == []


def test_dedupe_still_holds_under_concurrency(game_dir: Path):
    """Every writer posts the SAME url — dedupe must leave exactly one.

    Unlocked, the read-then-check-then-append window let several writers all miss
    each other's entry and append duplicates.
    """
    errors = _run_concurrently(
        [
            (
                lambda: _add_option(
                    game_dir, "fakegame", "sex/dupe", url="https://example.com/same.gif"
                )
            )
            for _ in range(20)
        ]
    )
    assert errors == []
    assert len(_read_options(game_dir)["options"]["sex/dupe"]) == 1


def test_reviews_ledger_survives_concurrent_writers(game_dir: Path):
    """The review ledger has two writers in different modules — the UI and
    `media_finder._clear_review_status` when `grab` replaces the bytes."""
    from api.v1.media_review import _read_reviews, _reviews_lock, _write_reviews

    def upsert(i):
        with _reviews_lock(game_dir):
            ledger = _read_reviews(game_dir)
            ledger["reviews"][f"sex/slot_{i}"] = {"status": "approved", "note": str(i)}
            _write_reviews(game_dir, ledger)

    errors = _run_concurrently([(lambda i=i: upsert(i)) for i in range(30)])
    assert errors == []
    assert len(_read_reviews(game_dir)["reviews"]) == 30


def test_lock_creates_missing_parent_dir(tmp_path: Path):
    """A first-ever write for a game has no `.find-media/` yet."""
    target = tmp_path / "brand_new" / ".find-media" / "media_options.json"
    with ledger_lock(target):
        write_json_atomic(target, {"game": "brand_new", "options": {}})
    assert json.loads(target.read_text())["game"] == "brand_new"


def test_failed_write_does_not_strand_a_tmp_file(tmp_path: Path):
    """Serialisation blows up mid-write — the staging file must not survive."""
    target = tmp_path / "ledger.json"

    class Unserialisable:
        pass

    with pytest.raises(TypeError):
        write_json_atomic(target, {"bad": Unserialisable()})

    assert [p.name for p in tmp_path.iterdir() if p.name.endswith(".tmp")] == []
