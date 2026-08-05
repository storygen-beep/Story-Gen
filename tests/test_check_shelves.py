"""`manage.py check_shelves` — the alarm for orphaned shelves and verdicts.

A slot's shelf (stocked options) and verdict (approve/disapprove) are filed under
its declared file path. Move the path and both orphan silently: the options are
still on disk, just under a label nobody looks up, so the picker opens empty and
you re-run a search you did not need.

Two edits move a path routinely:
  * converting a slot to a pool — "a/b_t5.webm" becomes the folder "a/b_t5"
  * retagging a tier           — apply_retags.py rewrites _t4 -> _t5 in the TOML

⚠️ The load-bearing rule here is that an orphan is an EXACT-match failure. A key
whose extension-stripped stem matches a declared slot is STILL an orphan —
"a/b_t5.webm" and "a/b_t5" are different strings, so the shelf really is
unreachable. Getting this wrong makes the audit blind to the pool case, which is
the most common one. (It is the mistake the first hand-rolled measurement made.)

    pytest tests/test_check_shelves.py -q
"""
import json

import pytest
from django.core.management import call_command

import apps.game_generation.management.commands.check_shelves as cs


TOML = """
schema_version = "1.0"

[project]
id = "fixture"
title = "Fixture"
starting_canvas = "c1"

[player]
id = "player"
name = "P"

[[locations]]
id = "loc"
name = "Room"

[[canvases]]
id = "c1"
name = "C1"

[canvases.trigger]
location = "loc"
is_active = true

[[canvases.nodes]]
id = "base"
name = "Base"
blocks = [
%s
]

[canvases.nodes.exit_block]
type = "location"
text = "Done."
"""


@pytest.fixture
def game(tmp_path, monkeypatch):
    """A fixture game whose TOML + ledgers the test controls."""
    monkeypatch.setattr(cs, "GAMES_ROOT", tmp_path)
    root = tmp_path / "g"
    (root / "toml_phases").mkdir(parents=True)
    (root / ".find-media").mkdir(parents=True)
    (root / "videos").mkdir(parents=True)

    def write(blocks_toml, *, shelf=None, verdicts=None, queries=None):
        (root / "toml_phases" / "7_final_game.toml").write_text(TOML % blocks_toml)
        if shelf is not None or queries is not None:
            # `queries` omitted entirely when not asked for — that is the shape of
            # every ledger written before query provenance existed, and a repair
            # must not invent the root.
            blob = {"game": "g", "options": shelf if shelf is not None else {}}
            if queries is not None:
                blob["queries"] = queries
            (root / ".find-media" / "media_options.json").write_text(json.dumps(blob))
        if verdicts is not None:
            (root / ".find-media" / "media_reviews.json").write_text(
                json.dumps({"reviews": verdicts})
            )
        return root

    return write


def _run(capsys, repair=False):
    """Run the audit; return (exit_code, stdout)."""
    code = 0
    try:
        call_command("check_shelves", game="g", repair=repair)
    except SystemExit as exc:
        code = exc.code
    return code, capsys.readouterr().out


def _ledger(root, name, key):
    return json.loads((root / ".find-media" / name).read_text())[key]


SINGLE = '  { type = "video", props = { file = "sex/a_t5.webm", description = "d" } },'
POOL = '  { type = "video", props = { pool_dir = "sex/a_t5", pool = 4, description = "d" } },'


# ── the clean case ───────────────────────────────────────────────────────────

def test_matching_keys_are_not_flagged(game, capsys):
    game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "u"}]}, verdicts={"sex/a_t5.webm": {}})
    code, out = _run(capsys)

    assert code == 0
    assert "ORPHANED" not in out
    assert "No orphaned shelves or verdicts." in out


def test_a_game_with_no_ledgers_is_clean(game, capsys):
    game(SINGLE)
    code, out = _run(capsys)
    assert code == 0


# ── pool conversion: the case that motivated the whole thing ─────────────────

def test_pool_conversion_orphans_the_shelf_and_is_flagged(game, capsys):
    """The exact live failure: 148 options stranded when a slot became a pool.

    The stem matches ("sex/a_t5"), which is precisely why a stem-based check
    would MISS this — and why the audit must compare exact keys.
    """
    game(POOL, shelf={"sex/a_t5.webm": [{"url": "u1"}, {"url": "u2"}]})
    code, out = _run(capsys)

    assert code == 1
    assert "1 ORPHANED" in out
    assert "sex/a_t5.webm" in out
    assert "2 options stranded" in out
    assert "probably meant: sex/a_t5" in out


def test_pool_conversion_orphans_the_verdict_too(game, capsys):
    """Both ledgers move together — repairing only the shelf leaves the verdict
    behind, which is the mistake made by hand on media_lab."""
    game(POOL, verdicts={"sex/a_t5.webm": {"status": "approved"}})
    code, out = _run(capsys)

    assert code == 1
    assert "[verdict]" in out
    assert "probably meant: sex/a_t5" in out


# ── tier retag ───────────────────────────────────────────────────────────────

def test_tier_retag_is_flagged_with_the_new_tier_suggested(game, capsys):
    """apply_retags.py rewrites _t4 -> _t5 in the TOML and re-keys nothing."""
    game(SINGLE, shelf={"sex/a_t4.webm": [{"url": "u"}]})
    code, out = _run(capsys)

    assert code == 1
    assert "sex/a_t4.webm" in out
    assert "probably meant: sex/a_t5.webm" in out


# ── a genuinely deleted slot ─────────────────────────────────────────────────

def test_a_deleted_slot_is_flagged_with_no_false_suggestion(game, capsys):
    """Real case in vesper: the slot was removed from the game and its verdict
    left behind. Inventing a match here would send someone repairing a slot that
    no longer exists."""
    game(SINGLE, verdicts={"sex/totally_gone_t5.webm": {"status": "approved"}})
    code, out = _run(capsys)

    assert code == 1
    assert "sex/totally_gone_t5.webm" in out
    assert "no obvious match" in out
    assert "probably meant" not in out


# ── it must not touch anything ───────────────────────────────────────────────

def test_the_audit_is_read_only(game, capsys):
    """Diagnosis only. A repair that runs itself is a repair nobody reviewed."""
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "u"}]},
                verdicts={"sex/a_t5.webm": {"status": "approved"}})
    before = {
        p: p.read_bytes()
        for p in (root / ".find-media").iterdir() if p.is_file()
    }
    _run(capsys)

    assert all(p.read_bytes() == b for p, b in before.items()), "the audit rewrote a ledger"


# ── --repair ─────────────────────────────────────────────────────────────────

def test_repair_moves_a_confident_orphan(game, capsys):
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "u1"}, {"url": "u2"}]})
    code, out = _run(capsys, repair=True)

    assert "MOVED -> sex/a_t5" in out
    assert code == 0, "nothing should remain unresolved"
    opts = _ledger(root, "media_options.json", "options")
    assert opts["sex/a_t5"] == [{"url": "u1"}, {"url": "u2"}]
    assert "sex/a_t5.webm" not in opts


def test_repair_backs_the_ledger_up_first(game, capsys):
    """These files are the only record of a shelf; a bad merge is unrecoverable."""
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "u"}]})
    _run(capsys, repair=True)

    bak = root / ".find-media" / "media_options.json.bak"
    assert bak.is_file()
    assert "sex/a_t5.webm" in json.loads(bak.read_text())["options"]


def test_repair_refuses_to_merge_onto_an_existing_key(game, capsys):
    """Merging two shelves would silently mix two beats' candidates. A human decides."""
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "old"}], "sex/a_t5": [{"url": "new"}]})
    code, out = _run(capsys, repair=True)

    assert "refusing to merge" in out
    assert code == 1
    opts = _ledger(root, "media_options.json", "options")
    assert opts["sex/a_t5"] == [{"url": "new"}], "the destination was overwritten"
    assert opts["sex/a_t5.webm"] == [{"url": "old"}], "the source was consumed anyway"


def test_repair_never_invents_a_destination(game, capsys):
    """vesper's `sex/renner_anal_t5.webm` names a slot the author DELETED (the TOML
    says so in a comment). Moving its verdict would fabricate a decision about a
    different beat."""
    root = game(SINGLE, verdicts={"sex/totally_gone_t5.webm": {"status": "approved"}})
    code, out = _run(capsys, repair=True)

    assert "no obvious match" in out
    assert "MOVED" not in out
    assert code == 1
    assert "sex/totally_gone_t5.webm" in _ledger(root, "media_reviews.json", "reviews")


def test_repair_is_a_no_op_on_a_clean_game(game, capsys):
    root = game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "u"}]})
    before = (root / ".find-media" / "media_options.json").read_bytes()
    code, out = _run(capsys, repair=True)

    assert code == 0
    assert (root / ".find-media" / "media_options.json").read_bytes() == before
    assert not (root / ".find-media" / "media_options.json.bak").exists()


def test_repair_fixes_a_tier_retag(game, capsys):
    root = game(SINGLE, shelf={"sex/a_t4.webm": [{"url": "u"}]},
                verdicts={"sex/a_t4.webm": {"status": "approved"}})
    code, out = _run(capsys, repair=True)

    assert code == 0
    assert "sex/a_t5.webm" in _ledger(root, "media_options.json", "options")
    assert _ledger(root, "media_reviews.json", "reviews")["sex/a_t5.webm"]["status"] == "approved"


# ── a shelf is TWO roots now: candidates + which search found them ───────────

def test_repair_moves_the_query_table_with_the_shelf(game, capsys):
    """A shelf that outlived its labels reads as "everything came from an unknown
    search" — silently, with nothing anywhere able to tell that the link was lost."""
    root = game(POOL,
                shelf={"sex/a_t5.webm": [{"url": "u1", "found_by": ["q one"]}]},
                queries={"sex/a_t5.webm": [{"q": "q one", "urls": 84}]})
    code, out = _run(capsys, repair=True)

    assert code == 0, out
    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    assert blob["options"]["sex/a_t5"][0]["found_by"] == ["q one"]
    assert blob["queries"]["sex/a_t5"][0]["q"] == "q one"
    assert "sex/a_t5.webm" not in blob["options"]
    assert "sex/a_t5.webm" not in blob["queries"]


def test_repair_refuses_when_only_the_query_table_collides(game, capsys):
    """The destination has no shelf but DOES have a zero-yield search recorded
    against it. Checking only `options` would clobber that record."""
    root = game(POOL,
                shelf={"sex/a_t5.webm": [{"url": "old"}]},
                queries={"sex/a_t5": [{"q": "already here"}]})
    code, out = _run(capsys, repair=True)

    assert "refusing to merge" in out and "queries" in out
    assert code == 1
    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    assert blob["options"]["sex/a_t5.webm"] == [{"url": "old"}], "the source was consumed anyway"
    assert blob["queries"]["sex/a_t5"] == [{"q": "already here"}], "the destination was overwritten"


def test_a_queries_only_orphan_is_still_found_and_moved(game, capsys):
    """A search that yielded NOTHING leaves a record and no options. It is still a
    real orphan once the slot's path moves — and it reports honestly as 0 stranded."""
    root = game(POOL, shelf={}, queries={"sex/a_t5.webm": [{"q": "leaning forward gif", "urls": 0}]})
    code, out = _run(capsys, repair=True)

    assert "0 options stranded" in out
    assert code == 0, out
    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    assert blob["queries"]["sex/a_t5"][0]["q"] == "leaning forward gif"


def test_repair_does_not_invent_a_queries_root(game, capsys):
    """Every ledger written before 2026-08-05 has exactly {game, options, updated_at}.
    A re-key must not restructure a file it was only asked to re-label."""
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "u"}]})
    _run(capsys, repair=True)

    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    assert "queries" not in blob


def test_repair_writes_atomically_and_backs_up_what_it_mutated(game, capsys):
    root = game(POOL, shelf={"sex/a_t5.webm": [{"url": "u"}]},
                queries={"sex/a_t5.webm": [{"q": "q one"}]})
    before = (root / ".find-media" / "media_options.json").read_bytes()
    _run(capsys, repair=True)

    assert (root / ".find-media" / "media_options.json.bak").read_bytes() == before
    assert not list((root / ".find-media").glob("*.tmp")), "a staging file was stranded"


# ── suggestion helper, directly ──────────────────────────────────────────────

@pytest.mark.parametrize("orphan,declared,want", [
    ("sex/a_t5.webm", {"sex/a_t5"}, "sex/a_t5"),           # pool conversion
    ("sex/a_t4.webm", {"sex/a_t5.webm"}, "sex/a_t5.webm"),  # tier retag
    ("sex/a_t5.gif", {"sex/a_t5.webm"}, "sex/a_t5.webm"),   # extension-agnostic
    ("sex/gone.webm", {"sex/a_t5.webm"}, ""),               # nothing plausible
])
def test_suggest(orphan, declared, want):
    assert cs.Command._suggest(orphan, declared) == want
