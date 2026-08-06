"""The pure half of scripts/fetch_related.py — blob construction, q/label picking,
extraction filters. No Playwright, no network, no Django.

The blob vector is GROUND TRUTH from the 2026-08-05 live probe: clicking the seed
clip's thumbnail made Google itself emit `tbs=rimg:CRbxeZ9DJQY3…` for docid
`FvF5n0MlBjcrfM`, and the truncated 9-byte blob was verified to serve the real
related feed (host-signature match, seed excluded). If construction drifts from
this vector, the feature silently degrades into a plain text search — Google
ignores a malformed tbs rather than erroring — so this file is what notices.

    pytest tests/test_fetch_related_blob.py -q
"""
import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "fetch_related", Path(__file__).parent.parent / "scripts" / "fetch_related.py"
)
fr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fr)


# ── docid → blob ─────────────────────────────────────────────────────────────

def test_blob_ground_truth_vector():
    assert fr.docid_to_blob("FvF5n0MlBjcrfM") == "CRbxeZ9DJQY3"


def test_blob_handles_unpadded_docid_lengths():
    # 11 chars ≡ 3 (mod 4) and 12 chars ≡ 0 — both must decode without error
    assert fr.docid_to_blob("l1dWn-tdD1UkwM")
    assert fr.docid_to_blob("AAAAAAAAAAAA")


def test_blob_refuses_a_docid_under_8_bytes():
    with pytest.raises(ValueError):
        fr.docid_to_blob("AAAA")  # 3 decoded bytes


def test_related_url_carries_query_and_blob():
    u = fr.related_url("kneeling blowjob gif", "CRbxeZ9DJQY3")
    assert u.startswith("https://www.google.com/search?udm=2&q=kneeling+blowjob+gif")
    assert u.endswith("&tbs=rimg:CRbxeZ9DJQY3")


# ── pick_q: found_by[0] → newest non-related search → filename slug ──────────

def test_pick_q_prefers_the_seeds_own_query():
    assert fr.pick_q({"found_by": ["alley bj gif"]}, [{"q": "other"}], "x") == "alley bj gif"


def test_pick_q_falls_back_to_the_newest_non_related_search():
    qs = [
        {"q": "old search", "source": "google"},
        {"q": "new search", "source": "google"},
        {"q": "⇢ some-clip", "source": "related"},  # newest, but never a q source
    ]
    assert fr.pick_q({}, qs, "x") == "new search"


def test_pick_q_last_resort_is_the_filename_slug():
    q = fr.pick_q({}, [], "https://a.b/44903/kneeling-blowjob.gif")
    assert q == "kneeling blowjob gif"


def test_pick_q_empty_when_nothing_is_usable():
    assert fr.pick_q({}, [], "https://a.b/12345.gif") == ""  # digits carry no words


# ── pick_label: same seed reuses, another seed suffixes ──────────────────────

def _rec(q, seed=None):
    r = {"q": q}
    if seed:
        r["seed_url"] = seed
    return r


def test_label_is_the_seed_stem():
    assert fr.pick_label("https://a.b/1/kneeling-blowjob.gif", []) == "⇢ kneeling-blowjob"


def test_same_seed_reuses_its_label_for_the_top_up():
    qs = [_rec("⇢ kneeling-blowjob", "https://a.b/1/kneeling-blowjob.gif")]
    assert fr.pick_label("https://a.b/1/kneeling-blowjob.gif", qs) == "⇢ kneeling-blowjob"


def test_another_seed_with_the_same_stem_gets_a_suffix():
    qs = [_rec("⇢ kneeling-blowjob", "https://a.b/1/kneeling-blowjob.gif")]
    assert fr.pick_label("https://a.b/2/kneeling-blowjob.gif", qs) == "⇢ kneeling-blowjob ·2"


def test_a_seedless_stub_is_adoptable():
    # the stock loop's auto-registered stub carries no seed_url — it is THIS run's
    qs = [_rec("⇢ kneeling-blowjob")]
    assert fr.pick_label("https://a.b/2/kneeling-blowjob.gif", qs) == "⇢ kneeling-blowjob"


def test_taken_forces_the_next_suffix():
    qs = [_rec("⇢ a", "https://a.b/1/a.gif"), _rec("⇢ a ·2", "https://a.b/2/a.gif")]
    got = fr.pick_label("https://a.b/3/a.gif", qs, taken={"⇢ a"})
    assert got == "⇢ a ·3"


# ── extraction filters — §4's cuts, in Python ────────────────────────────────

def test_clean_media_urls_applies_every_cut():
    html = " ".join([
        '"https://cdn.porn.test/a/b.gif?x=1"',      # keep, querystring stripped
        '"https://cdn.porn.test/a/b.gif"',          # duplicate after strip
        '"https://egl.phncdn.com/z.gif"',           # phncdn is NO LONGER cut
        '"https://encrypted-tbn0.gstatic.com/t.gif"',  # google furniture cut
        '"https://host.test/.gif"',                 # bare-extension cut
        '"https://host.test/real/clip.webm"',       # keep
    ])
    assert fr.clean_media_urls(html) == [
        "https://cdn.porn.test/a/b.gif",
        "https://egl.phncdn.com/z.gif",
        "https://host.test/real/clip.webm",
    ]


# ── signed urls: the ticket is the difference between 200 and 470 ────────────

SIGNED = ("https://egl.phncdn.com/gif/12345678.gif"
          "?validfrom=1754000000&validto=4882439600&hash=AbC%3D")

# how Google actually writes it into the results page
SIGNED_ESCAPED = ("https://egl.phncdn.com/gif/12345678.gif"
                  "?validfrom\\u003d1754000000\\u0026validto\\u003d4882439600"
                  "\\u0026hash\\u003dAbC%3D")


def test_a_signed_phncdn_url_survives_extraction_whole():
    """The ticket is what makes it fetchable — measured 200 with, 470 without."""
    got = fr.clean_media_urls(f'"{SIGNED_ESCAPED}"')
    assert got == [SIGNED]
    assert "validfrom=" in got[0] and "hash=" in got[0]


def test_a_signed_url_does_not_also_emit_its_stripped_twin():
    """Two rows for one clip — one alive, one 470 — would be indistinguishable
    in the picker. Dedup is on the exact byte string, so this must not happen."""
    html = f'"{SIGNED_ESCAPED}" "https://egl.phncdn.com/gif/12345678.gif"'
    got = fr.clean_media_urls(html)
    assert got == [SIGNED, "https://egl.phncdn.com/gif/12345678.gif"]
    assert len([u for u in got if u == SIGNED]) == 1


def test_an_unsigned_host_still_loses_its_query_string():
    """The regression guard for every existing host. SIGNED_QUERY_HOSTS has one
    entry, so nothing outside phncdn may change behaviour."""
    html = '"https://cdn.porn.test/a/b.gif?utm_source=x&sid=99"'
    assert fr.clean_media_urls(html) == ["https://cdn.porn.test/a/b.gif"]


def test_clean_media_urls_and_docid_join_agree_on_the_key():
    """If these disagree, docids.get(url) misses for every signed clip and the
    whole bucket is stocked with no docid — ⇢ dead forever, silently."""
    triple = (f'"FvF5n0MlBjcrfM",["https://encrypted-tbn0.gstatic.com/t",1,1],'
              f'["{SIGNED_ESCAPED}",290,500]')
    [url] = fr.clean_media_urls(triple)
    assert url in fr.docid_join(triple)
    assert fr.docid_join(triple)[url] == "FvF5n0MlBjcrfM"


def test_thumb_join_returns_the_encrypted_tbn_url():
    triple = ('"FvF5n0MlBjcrfM",["https://encrypted-tbn0.gstatic.com/t?id=9",290,499],'
              '["https://cdn.nsfwgify.com/1/a.gif",290,500]')
    assert fr.thumb_join(triple) == {
        "https://cdn.nsfwgify.com/1/a.gif": "https://encrypted-tbn0.gstatic.com/t?id=9"
    }


def test_media_triples_keeps_docid_and_thumb_aligned():
    """The tbn group became capturing on 2026-08-06, shifting the file url from
    group 2 to group 3. This is the test that notices if they ever slip."""
    triple = ('"AbCdEfGh12Xx",["https://encrypted-tbn0.gstatic.com/t",1,1],'
              '["https://cdn.nsfwgify.com/1/a.gif",1,1]')
    assert fr.media_triples(triple) == [
        ("https://cdn.nsfwgify.com/1/a.gif",
         "AbCdEfGh12Xx",
         "https://encrypted-tbn0.gstatic.com/t"),
    ]


# ── panel labels are bucket names, never queries ─────────────────────────────

def test_is_panel_label_covers_every_panel_prefix():
    assert fr.is_panel_label("⇢ kneeling-blowjob")
    assert fr.is_panel_label("◆ blowjob eye contact")
    assert not fr.is_panel_label("kneeling blowjob gif")
    assert not fr.is_panel_label("")


def test_pick_q_never_uses_a_pornhub_label_as_a_query():
    """The ◆ twin of the ⇢ case below. Without it, a related hop from a PornHub
    clip sends `◆ site:pornhub.com …` to Google as literal query text."""
    opt = {"found_by": ["◆ blowjob eye contact"]}
    qs = [{"q": "◆ blowjob eye contact", "source": "pornhub"}]
    assert fr.pick_q(opt, qs, "https://a.b/830899-ponytail.gif") == "ponytail gif"


def test_docid_join_reads_the_metadata_triple():
    triple = (
        '"FvF5n0MlBjcrfM",["https://encrypted-tbn0.gstatic.com/t",290,499],'
        '["https://cdn.nsfwgify.com/44903/kneeling-blowjob.gif",290,500]'
    )
    assert fr.docid_join(triple) == {
        "https://cdn.nsfwgify.com/44903/kneeling-blowjob.gif": "FvF5n0MlBjcrfM"
    }


def test_docid_join_unescapes_embedded_urls():
    triple = (
        '"AbCdEfGh12Xx",["https://encrypted-tbn0.gstatic.com/t",1,1],'
        '["https://h.test\\/a\\/b.gif?k\\u003dv\\u0026x",1,1]'
    )
    assert fr.docid_join(triple) == {"https://h.test/a/b.gif": "AbCdEfGh12Xx"}


def test_suspicious_guard_fires_only_on_thin_and_furniture_only():
    assert fr.looks_suspiciously_clean([])
    assert fr.looks_suspiciously_clean(["https://media.tenor.com/x/y.gif"])
    assert not fr.looks_suspiciously_clean(["https://cdn.porn.test/a/b.gif"])
    many = [f"https://media.tenor.com/{i}/y.gif" for i in range(9)]
    assert not fr.looks_suspiciously_clean(many)  # thin is half the signal


def test_host_histogram_folds_www_and_sorts_desc():
    urls = ["https://www.a.b/x.gif", "https://a.b/y.gif", "https://c.d/z.gif"]
    assert fr.host_histogram(urls) == [["a.b", 2], ["c.d", 1]]


def test_pick_q_never_uses_a_related_label_as_a_query():
    """A clip stocked BY a related fetch has the ⇢ label as its only found_by —
    recursing from it must fall through to a real query, never send the label."""
    opt = {"found_by": ["⇢ kneeling-blowjob"]}
    qs = [{"q": "⇢ kneeling-blowjob", "source": "related"}]
    q = fr.pick_q(opt, qs, "https://a.b/830899-ponytail.gif")
    assert q == "ponytail gif"


def test_no_stored_docid_means_no_run(monkeypatch):
    """The refusal must happen before playwright is imported or Chrome touched —
    the whole point of LO's ruling is that no tab ever opens."""
    import sys as _sys
    argv = ["fetch_related.py", "--game", "g", "--slot-key", "s/a.webm",
            "--seed-url", "https://x.test/a.gif"]
    monkeypatch.setattr(_sys, "argv", argv)
    monkeypatch.setattr(fr.requests, "get", lambda *a, **k: type("R", (), {
        "json": lambda self: {"options": [{"url": "https://x.test/a.gif"}], "queries": []}})())
    def boom(*a, **k):
        raise AssertionError("connected to a browser despite having no docid")
    monkeypatch.setattr(fr, "_ensure_page_target", boom)
    with pytest.raises(SystemExit) as e:
        fr.main()
    assert e.value.code == 4
