"""shape.py: the coverage list (SKILL.md "Never build an unknown on a guess";
`templates/sheets/coverage.md`; `state.md` `board.coverage[]`).

  every system has a coverage entry — each board.systems[] card is a `system` topic; kinds and
      statuses are the declared ones.
  no topic is unknown — an `unknown` WARNS by name, never fails (LO: warn, never block).
  every coverage source exists — `covered` names a skill file (and its rule id is in it);
      `scouted` names a scout card on disk; `lo` and `placeholder` carry a source.

All three are n/a until the spine is finished. A game in `gates.SHIP_GRANDFATHERED` with no list,
or with a bad entry, WARNS until it ships on or after COVERAGE_SINCE; billable_hours is not
grandfathered. Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

CARD = {"id": "intern_job", "name": "the internship", "place": "firm", "feeds": ["money"],
        "reads": ["nerve"]}
ROWS = ("every system has a coverage entry", "no topic is unknown", "every coverage source exists")


def verdicts(state, strict=True, slug=None, root=None):
    got = {n: (ok, h, d) for n, ok, h, d in shape.check(state, strict, slug, root)[0]}
    return {r: got[r] for r in ROWS}


def ledger(coverage=None, systems=(CARD,), slug="fx", releases=None):
    st = {"slug": slug, "phase": "board", "want": {}, "board": {"systems": list(systems)}}
    if coverage is not None:
        st["board"]["coverage"] = coverage
    if releases is not None:
        st["releases"] = releases
    return st


def entry(topic, status="covered", source="templates/cards/job.md", kind="system"):
    return {"topic": topic, "kind": kind, "status": status, "source": source}


GOOD = [entry("intern_job"),
        entry("a party", "lo", "LO, 2026-10-02: one party a week, at the club", "scene"),
        entry("the landlord", "placeholder", "release page: the landlord is a name only", "mechanic"),
        entry("her room", "covered", "references/the-map.md R2", "place")]


def test_a_full_list_passes_every_row():
    v = verdicts(ledger(GOOD))
    assert all(v[r][0] is True for r in ROWS), v


def test_lenient_is_na():
    v = verdicts(ledger(GOOD), strict=False)
    assert all(v[r][0] is None for r in ROWS)


def test_a_system_card_with_no_entry_fails():
    ok, _h, detail = verdicts(ledger(GOOD[1:]))["every system has a coverage entry"]
    assert ok is False and "intern_job" in detail[0]


def test_an_entry_by_the_cards_name_counts():
    v = verdicts(ledger([entry("the internship")] + GOOD[1:]))
    assert v["every system has a coverage entry"][0] is True


def test_a_bad_kind_or_status_fails():
    bad = GOOD + [entry("a car", "maybe", "x", "vehicle")]
    ok, _h, detail = verdicts(ledger(bad))["every system has a coverage entry"]
    assert ok is False and any("kind" in d for d in detail) and any("status" in d for d in detail)


def test_an_unknown_warns_by_name_and_never_fails():
    ok, head, _d = verdicts(ledger(GOOD + [entry("a car", "unknown", "", "mechanic")]))["no topic is unknown"]
    assert ok == "warn" and "a car" in head


def test_a_covered_source_that_does_not_exist_fails():
    ok, _h, detail = verdicts(ledger(GOOD + [entry("a gym", "covered", "templates/cards/no_such.md")]))[
        "every coverage source exists"]
    assert ok is False and "no_such.md" in detail[0]


def test_a_covered_rule_id_the_file_does_not_have_fails():
    ok, _h, detail = verdicts(ledger(GOOD + [entry("a bar", "covered", "references/the-map.md R99", "place")]))[
        "every coverage source exists"]
    assert ok is False and "R99" in detail[0]


def test_a_scouted_card_must_exist(tmp_path):
    card = tmp_path / "games" / "fx" / "scout" / "a_party.md"
    st = ledger(GOOD + [entry("a club night", "scouted", "games/fx/scout/a_party.md", "scene")])
    ok, _h, detail = verdicts(st, root=str(tmp_path))["every coverage source exists"]
    assert ok is False and "no scout card" in detail[0]
    card.parent.mkdir(parents=True)
    card.write_text("# Scout card — a party (scene)\n")
    assert verdicts(st, root=str(tmp_path))["every coverage source exists"][0] is True


def test_lo_and_placeholder_need_a_source():
    ok, _h, detail = verdicts(ledger(GOOD + [entry("a car", "lo", "", "mechanic")]))[
        "every coverage source exists"]
    assert ok is False and "no source" in detail[0]


def test_no_list_fails_a_game_not_grandfathered():
    v = verdicts(ledger(None, slug="billable_hours"))
    assert v["every system has a coverage entry"][0] is False
    assert v["every coverage source exists"][0] is False
    assert v["no topic is unknown"][0] == "warn"


def test_no_list_warns_on_a_grandfathered_game():
    v = verdicts(ledger(None, slug="members_only"))
    assert all(v[r][0] == "warn" for r in ROWS) and "grandfathered" in v[ROWS[0]][1]


def test_a_bad_entry_warns_on_a_grandfathered_game():
    v = verdicts(ledger(GOOD[1:] + [entry("a gym", "covered", "templates/cards/no_such.md")], slug="members_only"))
    assert v["every system has a coverage entry"][0] == "warn"
    assert v["every coverage source exists"][0] == "warn"


def test_a_grandfathered_game_that_shipped_since_fails():
    st = ledger(None, slug="members_only", releases=[{"version": "0.3", "shipped": "2026-10-03"}])
    assert verdicts(st)["every system has a coverage entry"][0] is False
