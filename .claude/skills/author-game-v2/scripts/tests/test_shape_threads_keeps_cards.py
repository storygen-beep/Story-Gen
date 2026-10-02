"""shape.py: her life's threads, what each man keeps, the meters as declared variables, and a card
for every declared system (the-want.md §6, the-meters.md W1, the-systems.md S2a).

Grandfathering: a game in `gates.SHIP_GRANDFATHERED` WARNS where `keeps` or a missing card would FAIL
a new game. billable_hours is not grandfathered. n/a: the threads row before any thread is written
(lenient), the keeps row with no cast, the card row until the spine is finished (strict).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

CARD = {"id": "intern_job", "name": "the internship", "place": "firm", "feeds": ["money", "office_talk"],
        "reads": ["nerve"]}


def verdict(state, row, strict=False, slug=None):
    for name, ok, head, detail in shape.check(state, strict, slug)[0]:
        if name == row:
            return ok, detail
    raise AssertionError(f"row missing: {row}")


def ledger(threads=(), cast=(), systems=(), meters=(), slug="fx"):
    return {"slug": slug, "phase": "idea",
            "want": {"threads": list(threads), "cast": list(cast)},
            "board": {"systems": list(systems), "meters": list(meters)}}


def thread(i, person, system="none yet"):
    return {"id": i, "person": person, "place": "p", "system": system, "link": "…"}


ADULTS = [{"id": f"npc_{c}", "age": 30, "keeps": "want + power"} for c in "abcdefg"]

# ── her life has threads ─────────────────────────────────────────────────────

def test_four_to_six_threads_with_cast_people_pass():
    st = ledger([thread(str(i), f"npc_{c}") for i, c in enumerate("abcd")], ADULTS)
    assert verdict(st, "her life has threads")[0] is True


def test_three_threads_warn():
    st = ledger([thread(str(i), f"npc_{c}") for i, c in enumerate("abc")], ADULTS)
    assert verdict(st, "her life has threads")[0] == "warn"


def test_a_thread_person_not_in_the_cast_fails():
    st = ledger([thread("job", "npc_zed")] + [thread(str(i), f"npc_{c}") for i, c in enumerate("abc")], ADULTS)
    ok, detail = verdict(st, "her life has threads")
    assert ok is False and "npc_zed" in detail[0]


def test_a_thread_person_with_no_age_fails():
    cast = [{"id": "npc_a", "keeps": "want + power"}]
    ok, detail = verdict(ledger([thread("job", "npc_a")], cast), "her life has threads")
    assert ok is False and "no age" in detail[0]


def test_no_threads_is_na_lenient_and_warns_strict():
    assert verdict(ledger(), "her life has threads")[0] is None
    assert verdict(ledger(), "her life has threads", strict=True)[0] == "warn"


# ── each man's keeps is named ───────────────────────────────────────────────

def test_billable_hours_keeps_strings_pass():
    cast = [{"id": "npc_martin", "age": 52, "keeps": "want + power"},
            {"id": "npc_ethan", "age": 25, "keeps": "step counter + memory flags"},
            {"id": "npc_diane", "age": 49, "keeps": "none — a schedule system"},
            {"id": "npc_pierce", "age": 58, "keeps": "none — a risk system"}]
    assert verdict(ledger(cast=cast, slug="billable_hours"), "each man's keeps is named")[0] is True


MEMBERS_ONLY = [{"id": "julian", "age": 46, "keeps": "nothing: the climb is hers; he holds the tab"},
                {"id": "ade", "age": 34, "keeps": "step counter + memory flags"}]


def test_members_only_keeps_string_warns_grandfathered():
    ok, detail = verdict(ledger(cast=MEMBERS_ONLY, slug="members_only"), "each man's keeps is named")
    assert ok == "warn" and "julian" in detail[0]


def test_the_same_string_fails_a_game_that_is_not_grandfathered():
    ok, _ = verdict(ledger(cast=MEMBERS_ONLY, slug="billable_hours"), "each man's keeps is named")
    assert ok is False


def test_the_slug_argument_names_the_game_when_the_ledger_has_none():
    st = ledger(cast=MEMBERS_ONLY)
    st.pop("slug")
    assert verdict(st, "each man's keeps is named", slug="members_only")[0] == "warn"


def test_none_needs_the_dash_and_a_reason():
    cast = [{"id": "npc_a", "age": 30, "keeps": "none"}]
    assert verdict(ledger(cast=cast), "each man's keeps is named")[0] is False


def test_a_missing_keeps_fails_only_when_strict():
    cast = [{"id": "npc_a", "age": 30}]
    assert verdict(ledger(cast=cast), "each man's keeps is named")[0] is True
    assert verdict(ledger(cast=cast), "each man's keeps is named", strict=True)[0] is False


def test_no_cast_is_na():
    assert verdict(ledger(), "each man's keeps is named")[0] is None


# ── the meters are declared variables ───────────────────────────────────────

def test_a_step_reading_a_meter_key_or_a_card_feed_is_declared():
    st = ledger(systems=[CARD], meters=[{"id": "outfit", "key": "worn_exposure", "kind": "body"}])
    st["board"]["characters"] = [{"id": "npc_a", "ladder": {"counter": "a_stage", "steps": [
        {"n": 1, "canvas": "c", "where": "x", "when": {"days": ["Mon"], "from": "09:00", "to": "10:00"},
         "gate": [{"trait": "worn_exposure", "op": "gte", "value": 1},
                  {"trait": "office_talk", "op": "gte", "value": 2}]}]}}]
    assert verdict(st, "a step's variables are declared")[0] is True


# ── every system has a card ─────────────────────────────────────────────────

def test_cards_and_the_threads_systems_pass_strict():
    st = ledger([thread("job", "npc_a", "intern_job")], ADULTS, systems=[CARD])
    assert verdict(st, "every system has a card", strict=True)[0] is True


def test_a_thread_naming_a_system_with_no_card_fails():
    st = ledger([thread("job", "npc_a", "friday_money")], ADULTS, systems=[CARD])
    ok, detail = verdict(st, "every system has a card", strict=True)
    assert ok is False and "friday_money" in detail[0]


def test_meter_shaped_rows_only_fail_a_new_game_and_warn_a_grandfathered_one():
    old = [{"id": "look", "key": "look", "kind": "body", "fed_at": [], "labels": [], "read_by": []}]
    assert verdict(ledger(systems=old), "every system has a card", strict=True)[0] is False
    assert verdict(ledger(systems=old, slug="members_only"), "every system has a card",
                   strict=True)[0] == "warn"


def test_the_card_row_is_na_while_the_spine_is_written():
    assert verdict(ledger(), "every system has a card")[0] is None
