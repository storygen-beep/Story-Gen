"""The `--ship` BLOCK rows on systems (World and Systems PRD, Phase 6B, 2026-10-02).

  every system has a card — each card in board.systems[] fills its fields; a card involving
      money has a sink and a deadline, any other feeds something; zero cards is red, never n/a;
      an old meter-shaped entry is a meter, not a card.

  every system leads to a person or a sex scene — each card's leads_to[] names a person in
      board.characters or a canvas with an explicit beat, and it exists in the build.

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


# ── every system leads to a person or a sex scene ─────────────────────────────

LEADS_ROW = "every system leads to a person or a sex scene"


def leads(st, game=None):
    model, g = gates.build(game or ws6.green_game())
    return gates._every_system_leads_somewhere(model, g, st)


def hot_game():
    g = ws6.green_game()
    g["canvases"].append({"id": "backroom", "trigger": {"location": "work", "is_repeatable": True},
                          "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content":
                              "He fucks her, his cock deep in her wet cunt, and she comes."}]}]})
    return g


def test_a_card_leading_to_a_built_person_in_the_cast_passes():
    assert leads(state_with(card()))[0] is True


def test_a_card_leading_to_an_explicit_canvas_passes():
    assert leads(state_with(card(leads_to=["backroom"])), hot_game())[0] is True


def test_a_card_leading_to_a_dry_canvas_or_a_stranger_fails_and_says_why():
    ok, _, detail = leads(state_with(card(leads_to=["office", "npc_ghost"])))
    assert ok is False and "`office` a canvas with no explicit beat" in detail[0], detail
    assert "`npc_ghost` in neither the cast nor the build" in detail[0], detail


def test_a_person_not_in_board_characters_does_not_count():
    st = state_with(card())
    st["board"]["characters"] = []
    ok, _, detail = leads(st)
    assert ok is False and "not in board.characters" in detail[0], detail


def test_an_empty_leads_to_fails():
    ok, _, detail = leads(state_with(card(leads_to=[])))
    assert ok is False and "it is empty" in detail[0]


def test_zero_systems_is_red_for_leads_too():
    assert leads(state_with())[0] is False


def test_leads_warns_when_grandfathered_and_blocks_when_not(tmp_path, monkeypatch):
    st = state_with(card(leads_to=["office"]))
    assert ck8b.ship(tmp_path, monkeypatch, "probation", state=st)[LEADS_ROW][0] == "warn"
    assert ck8b.ship(tmp_path, monkeypatch, "billable_hours", state=st)[LEADS_ROW][0] is False
    st["releases"] = [{"version": "0.2", "shipped": "2026-10-03"}]
    assert ck8b.ship(tmp_path, monkeypatch, "probation", state=st)[LEADS_ROW][0] is False
    assert ck8b.ship(tmp_path, monkeypatch, "new_game")[LEADS_ROW][0] is True


def test_the_row_says_its_label_once(tmp_path, monkeypatch):
    head = ck8b.ship(tmp_path, monkeypatch, "new_game")[CARD_ROW][1]
    assert not head.startswith(CARD_ROW) and CARD_ROW not in head
    # A row named apart from its gate still names the gate.
    assert gates._gate_prefix("standing surface") == "standing surface: "
