"""The `--ship` BLOCK rows on systems (World and Systems PRD, Phase 6B, 2026-10-02).

  every system has a card — each card in board.systems[] fills its fields; a card involving
      money has a sink and a deadline, any other feeds something; zero cards is red, never n/a;
      an old meter-shaped entry is a meter, not a card.

LO B: a grandfathered game warns until it ships on or after the row's date; a game not in
SHIP_GRANDFATHERED (billable_hours, a new game) blocks. Fixtures are written here; nothing in
games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_ck8b as ck8b  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

CARD_ROW = "every system has a card"
METER = {"id": "money", "kind": "ambient", "key": "money", "fed_at": ["work"],
         "labels": ["work"], "read_by": "the rent"}


def state_with(*systems, **board):
    st = ws6.green_state()
    st["board"]["systems"] = list(systems)
    st["board"].update(board)
    return st


def card(**kw):
    c = ws6.green_card()
    c.update(kw)
    return {k: v for k, v in c.items() if v is not None}


# ── every system has a card ──────────────────────────────────────────────────

def test_a_filled_card_passes():
    ok, head, detail = gates._every_system_has_a_card(state_with(card()))
    assert ok is True and "1/1" in head, (head, detail)


def test_a_card_missing_fields_fails_and_names_them():
    ok, _, detail = gates._every_system_has_a_card(state_with(card(place=None, hook_link="")))
    assert ok is False and "place" in detail[0] and "hook_link" in detail[0], detail


def test_a_money_card_needs_a_sink_and_a_deadline():
    st = state_with(card(pay_ladder=[{"gate": "start", "pay": 70}], feeds=[]))
    ok, _, detail = gates._every_system_has_a_card(st)
    assert ok is False and "sink" in detail[0] and "deadline" in detail[0], detail
    st = state_with(card(pay_ladder=[{"gate": "start", "pay": 70}], feeds=[], reads=["nerve"],
                         sink="the rent", deadline="Friday"))
    assert gates._every_system_has_a_card(st)[0] is True


def test_a_cost_in_the_currency_is_money():
    st = state_with(card(cost="$250 every Friday"))
    assert gates._card_is_money(st["board"]["systems"][0], st)


def test_a_card_with_no_money_must_feed_something():
    ok, _, detail = gates._every_system_has_a_card(state_with(card(feeds=[], reads=["nerve"])))
    assert ok is False and "feeds[]" in detail[0], detail


def test_zero_systems_is_red_not_na():
    ok, head, _ = gates._every_system_has_a_card(state_with())
    assert ok is False and "zero systems is red" in head


def test_an_old_meter_shaped_ledger_is_read_as_meters_and_red():
    ok, head, _ = gates._every_system_has_a_card(state_with(METER))
    assert ok is False and "1 meter-shaped entry in board.systems[] read as meters" in head, head


def test_the_legacy_form_passes():
    gates._LEGACY_RULES.add("system_card")
    try:
        assert gates._every_system_has_a_card(state_with())[0] is True
    finally:
        gates._LEGACY_RULES.discard("system_card")


# ── LO B, on the real row ─────────────────────────────────────────────────────

def test_an_old_shape_ledger_blocks_a_game_not_grandfathered(tmp_path, monkeypatch):
    b = ck8b.ship(tmp_path, monkeypatch, "billable_hours", state=state_with(METER))
    assert b[CARD_ROW][0] is False


def test_a_grandfathered_game_warns(tmp_path, monkeypatch):
    ok, head = ck8b.ship(tmp_path, monkeypatch, "members_only", state=state_with(METER))[CARD_ROW]
    assert ok == "warn" and "system_card" in head and "blocks from your next release" in head


def test_a_grandfathered_game_shipped_since_blocks(tmp_path, monkeypatch):
    st = state_with(METER)
    st["releases"] = [{"version": "0.2", "shipped": "2026-10-02"}]
    assert ck8b.ship(tmp_path, monkeypatch, "members_only", state=st)[CARD_ROW][0] is False


def test_the_green_fixture_passes_the_row(tmp_path, monkeypatch):
    assert ck8b.ship(tmp_path, monkeypatch, "new_game")[CARD_ROW][0] is True
    assert gates._LEGACY_RULES == set()


def test_a_card_is_not_mistaken_for_a_meter():
    st = state_with(copy.deepcopy(METER), card())
    assert [c["id"] for c in gates._system_cards(st)] == ["shift"]
