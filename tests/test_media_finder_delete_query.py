"""Deleting one SEARCH from a slot — the query table's first delete path.

A human can now type his own queries into the picker, so he will type bad ones.
Until this endpoint the only doors out of a poisoned shelf were `options/remove`
one url at a time, or `options/clear`, which empties the whole slot — and neither
has ever removed a query RECORD. A search box without a bucket delete is a loaded
gun with no safety.

⚠️ The load-bearing test here is `test_a_sole_label_option_is_dropped_not_emptied`.
`found_by: []` and "no found_by key" are the same value to the picker
(`foundBy(o)` is `o.found_by || []`), and it reads that as the Q_UNLABELLED
bucket — whose chip says "Stocked before searches were recorded — no search can be
attributed to these". So relabelling a sole-owner option to empty would silently
migrate it into a bucket that then lies about its provenance, and the delete would
visibly delete nothing. The invariant this file pins is:

    NO option in the store ever carries `found_by: []`.

`test_no_option_anywhere_is_left_with_an_empty_found_by` asserts it over the whole
ledger rather than over one row, because the failure mode is a silent migration,
not an exception.

    pytest tests/test_media_finder_delete_query.py -q
"""
import json

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


def _ledger(games_root):
    return mf._read_options(games_root / "g")


def _shelf(games_root, slot=SLOT):
    return _ledger(games_root)["options"].get(slot, [])


def _queries(games_root, slot=SLOT):
    return _ledger(games_root)["queries"].get(slot, [])


def _add(games_root, url, query, slot=SLOT):
    return _post(
        mf.options_add,
        {
            "game": "g",
            "file": slot,
            "url": url,
            "media_kind": "img",
            "query": query,
        },
    )


def _rm(query="oral gif", slot=SLOT, game="g"):
    return _post(mf.queries_remove, {"game": game, "file": slot, "query": query})


def _urls(games_root, slot=SLOT):
    return {o["url"] for o in _shelf(games_root, slot)}


# ── the three cases ──────────────────────────────────────────────────────────


def test_a_sole_label_option_is_dropped_not_emptied(games_root):
    """THE test. Emptying found_by instead of dropping the row would move this
    option into the "Older searches" bucket, whose tooltip then asserts something
    false about a row whose provenance we knew and just deleted."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    res = _rm()
    assert res.status_code == 200
    assert _body(res)["removed"] == 1
    assert _shelf(games_root) == [], "the option survived the delete"


def test_a_multi_label_option_survives_and_loses_only_that_label(games_root):
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _add(games_root, "https://x.test/a.gif", "kneeling gif")  # same url, 2nd search
    assert _shelf(games_root)[0]["found_by"] == ["oral gif", "kneeling gif"]

    body = _body(_rm())
    assert body["removed"] == 0 and body["relabelled"] == 1
    assert _shelf(games_root)[0]["found_by"] == ["kneeling gif"]


def test_an_option_that_never_carried_the_label_is_untouched(games_root):
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _add(games_root, "https://x.test/b.gif", "kneeling gif")
    before = [o for o in _shelf(games_root) if o["url"].endswith("b.gif")][0]
    _rm()
    after = [o for o in _shelf(games_root) if o["url"].endswith("b.gif")][0]
    assert after == before, "an unrelated option was rewritten"


def test_no_option_anywhere_is_left_with_an_empty_found_by(games_root):
    """The invariant, asserted over the WHOLE ledger — the failure is a silent
    migration into Q_UNLABELLED, not an exception, so one row is not enough."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _add(games_root, "https://x.test/b.gif", "oral gif")
    _add(games_root, "https://x.test/b.gif", "kneeling gif")
    _add(games_root, "https://x.test/c.gif", "oral gif", slot="sex/other_t5.webm")
    _rm()
    for slot, options in _ledger(games_root)["options"].items():
        for option in options:
            assert option.get("found_by") != [], f"{slot} {option['url']} emptied"


def test_a_duplicated_label_still_drops_the_row(games_root):
    """Defensive: `_apply_option` guards against a repeated label, but a hand edit
    can produce one. Filtering it out must leave [] -> drop, never [] -> keep."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    data = _ledger(games_root)
    data["options"][SLOT][0]["found_by"] = ["oral gif", "oral gif"]
    mf._write_options(games_root / "g", data)

    assert _body(_rm())["removed"] == 1
    assert _shelf(games_root) == []


# ── the record, and the other slots ──────────────────────────────────────────


def test_the_record_leaves_the_query_table(games_root):
    _add(games_root, "https://x.test/a.gif", "oral gif")
    assert [r["q"] for r in _queries(games_root)] == ["oral gif"]
    assert _body(_rm())["record_removed"] is True
    assert _queries(games_root) == []


def test_other_slots_are_untouched(games_root):
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _add(games_root, "https://x.test/a.gif", "oral gif", slot="sex/other_t5.webm")
    _rm()
    assert _urls(games_root, "sex/other_t5.webm") == {"https://x.test/a.gif"}
    assert [r["q"] for r in _queries(games_root, "sex/other_t5.webm")] == ["oral gif"]


def test_previous_picks_survive(games_root):
    """Undo history is never search noise — options_clear's precedent. A previous
    pick carries no label, so it must fall through untouched."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    mf._add_option(
        games_root / "g",
        "g",
        SLOT,
        url="/games/g/.find-media/previous/old.gif",
        type_="image",
        media_kind="img",
        local_path="g/.find-media/previous/old.gif",
        origin="previous",
    )
    _rm()
    survivors = _shelf(games_root)
    assert len(survivors) == 1 and survivors[0]["origin"] == "previous"


def test_deleting_a_related_bucket_clears_it_from_the_table(games_root):
    """⇢ buckets are deletable too. relBySeed is rebuilt from the records on every
    poll, so the seed's button reverts to "get related" — which is the point."""
    _add(games_root, "https://x.test/a.gif", "⇢ kneeling-blowjob")
    _post(
        mf.queries_add,
        {
            "game": "g",
            "file": SLOT,
            "query": "⇢ kneeling-blowjob",
            "source": "related",
            "seed_url": "https://x.test/seed.gif",
        },
    )
    assert _body(_rm("⇢ kneeling-blowjob"))["record_removed"] is True
    assert _queries(games_root) == []


# ── ADOPTED vs INTRODUCED — the case that destroyed real data ────────────────
#
# Found the hard way on games/media_lab, 2026-08-09: two live searches then two
# deletes turned a 137-option shelf into 82. `_apply_option` adopts an
# already-shelved url by appending the new label to the EXISTING row, and 1294 of
# that game's 1296 options predate provenance and carry no label at all — so a
# search that merely re-found one made it look sole-owned, and the delete
# destroyed an option that had been there for weeks. 55 real options were lost.
#
# The fix is `added_at >= record.at`: an option stamped before the search first
# ran cannot have been introduced by it. These tests are the ones that should
# have existed first.


def _stock_legacy(games_root, url, added_at="2026-01-01T00:00:00+00:00"):
    """An option from before query provenance existed — no found_by at all."""
    data = _ledger(games_root)
    data["options"].setdefault(SLOT, []).append(
        {
            "url": url,
            "type": "gif",
            "media_kind": "img",
            "added_at": added_at,
        }
    )
    mf._write_options(games_root / "g", data)


def test_a_legacy_option_adopted_by_a_search_survives_that_searchs_deletion(games_root):
    """⚠️ THE data-loss test. The search re-found a url that was already on the
    shelf; deleting the search must not delete the row it did not create."""
    _stock_legacy(games_root, "https://x.test/old.gif")
    _add(games_root, "https://x.test/old.gif", "oral gif")  # adopts it
    assert _shelf(games_root)[0]["found_by"] == ["oral gif"], "setup: not adopted"

    body = _body(_rm())
    assert body["removed"] == 0, "an option the search did not introduce was destroyed"
    assert body["unlabelled"] == 1
    assert _urls(games_root) == {"https://x.test/old.gif"}


def test_an_adopted_option_goes_back_to_carrying_no_label(games_root):
    """POPPED, not set to []. An option with no labels reads as Q_UNLABELLED —
    "stocked before searches were recorded" — which for this row is true again."""
    _stock_legacy(games_root, "https://x.test/old.gif")
    _add(games_root, "https://x.test/old.gif", "oral gif")
    _rm()
    survivor = _shelf(games_root)[0]
    assert "found_by" not in survivor, survivor


def test_an_option_the_search_really_introduced_is_still_dropped(games_root):
    """The other half: the guard must not make delete a no-op. An option stocked
    at or after the query's first run is the search's own and goes."""
    _add(games_root, "https://x.test/new.gif", "oral gif")
    assert _body(_rm())["removed"] == 1
    assert _shelf(games_root) == []


def test_a_mixed_shelf_splits_correctly(games_root):
    """One legacy adoptee, one genuine find, one shared with another search."""
    _stock_legacy(games_root, "https://x.test/old.gif")
    _add(games_root, "https://x.test/old.gif", "oral gif")
    _add(games_root, "https://x.test/new.gif", "oral gif")
    _add(games_root, "https://x.test/shared.gif", "oral gif")
    _add(games_root, "https://x.test/shared.gif", "kneeling gif")

    body = _body(_rm())
    assert (body["removed"], body["relabelled"], body["unlabelled"]) == (1, 1, 1)
    assert _urls(games_root) == {"https://x.test/old.gif", "https://x.test/shared.gif"}


# ── idempotency, orphans, and the durable line ───────────────────────────────


def test_an_unknown_query_is_a_clean_no_op_not_a_404(games_root):
    """A double-click plus the 3 s poll makes a second call likely, and a red
    toast for a successful operation is worse than a no-op."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _rm()
    res = _rm()
    assert res.status_code == 200
    body = _body(res)
    assert body["removed"] == 0 and body["record_removed"] is False


def test_an_orphan_label_is_stripped_but_the_option_is_kept(games_root):
    """A found_by entry whose record is missing — reachable after a hand edit, or a
    crash between _ensure_query and queries/add. The option pass runs regardless,
    so the stale label is repaired; but with no record there is no `at` to prove
    the search introduced the row, and this endpoint deletes only what it can show
    it created. Strip, keep."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    data = _ledger(games_root)
    data["queries"][SLOT] = []  # record gone, label still on the option
    mf._write_options(games_root / "g", data)

    body = _body(_rm())
    assert body["removed"] == 0 and body["unlabelled"] == 1
    assert body["record_removed"] is False
    assert "found_by" not in _shelf(games_root)[0]


def test_the_deletion_appends_a_durable_ledger_line(games_root):
    """media_options.json is rewritten whole and reads back EMPTY if torn, so the
    jsonl is the copy that survives. A deletion is a query-history event."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    _post(
        mf.queries_add,
        {
            "game": "g",
            "file": SLOT,
            "query": "oral gif",
            "source": "manual",
            "urls": 41,
        },
    )
    _rm()
    lines = (
        (games_root / "g" / ".find-media" / "query_ledger.jsonl")
        .read_text()
        .splitlines()
    )
    row = json.loads(lines[-1])
    assert row["status"] == "deleted"
    assert row["query"] == "oral gif"
    assert row["source"] == "manual", "the deleted record's own source, not a default"


def test_the_write_restamps_game_and_updated_at(games_root):
    _add(games_root, "https://x.test/a.gif", "oral gif")
    before = _ledger(games_root)["updated_at"]
    _rm()
    data = _ledger(games_root)
    assert data["game"] == "g" and data["updated_at"] > before


def test_it_keys_on_slot_key_not_file(games_root):
    """The shelf is keyed by the slot's STABLE identity; `file` is where the bytes
    go. A tagged slot whose path moved must still find its own bucket."""
    _add(games_root, "https://x.test/a.gif", "oral gif", slot="stable-id")
    res = _post(
        mf.queries_remove,
        {
            "game": "g",
            "file": "sex/moved_t5.webm",
            "slot_key": "stable-id",
            "query": "oral gif",
        },
    )
    assert _body(res)["removed"] == 1
    assert _shelf(games_root, "stable-id") == []


def test_the_label_is_canonicalized_before_the_join(games_root):
    """_canon_query is the exact-string join key between found_by and the record.
    Retyped whitespace must not miss the bucket."""
    _add(games_root, "https://x.test/a.gif", "oral gif")
    assert _body(_rm("  oral   gif "))["removed"] == 1


# ── refusals ────────────────────────────────────────────────────────────────


def test_get_is_405(games_root):
    assert mf.queries_remove(RequestFactory().get("/")).status_code == 405


@pytest.mark.parametrize(
    "payload",
    [
        {"game": "", "file": SLOT, "query": "oral gif"},
        {"game": "../etc", "file": SLOT, "query": "oral gif"},
        {"game": "g", "file": "", "query": "oral gif"},
        {"game": "g", "file": SLOT, "query": ""},
        {"game": "g", "file": SLOT, "query": "   "},
    ],
)
def test_bad_input_is_a_400(games_root, payload):
    assert _post(mf.queries_remove, payload).status_code == 400
