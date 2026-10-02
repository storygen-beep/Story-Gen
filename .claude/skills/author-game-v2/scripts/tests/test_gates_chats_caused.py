"""`every chat is caused by a scene` (World and Systems PRD, Phase 6B, 2026-10-02).

A `--ship` BLOCK row: every `[[phone.conversations]]` and `[[phone.calls]]` trigger holds a flag
(`is_true`) that a canvas sets, or that a reply sets in a conversation itself caused this way.
Dev canvases, the cheat page and the daily tick are not scenes. n/a (no phone) passes. Fixtures
only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_wardrobe_reads as wr  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

ROW = "every chat is caused by a scene"


def on(flag):
    return {"conditions": {"version": "1.0", "items": [
        {"type": "flag", "subject": "player", "flag_key": flag, "operator": "is_true"}]}}


def chat(cid, flag, sets=None):
    blocks = [{"type": "message", "sender": "npc", "content": "you up? come by"}]
    if sets:
        blocks.append({"type": "reply", "round": 1, "choices": [
            {"text": "Coming.", "flagEffects": [{"targetType": "player", "flag": sets}]}]})
    return {"id": cid, "app": "messages", "npc": "npc_a", "trigger": on(flag), "blocks": blocks}


def game(convs=(), calls=(), extra=None):
    g = ws6.green_game()        # `meet_a` sets met_a; `opening` sets opening_done
    g["phone"] = {"enabled": True, "conversations": list(convs), "calls": list(calls)}
    if extra:
        g.update(extra)
    return g


def caused(g):
    return gates._chats_are_caused(g)


def test_a_chat_on_a_flag_a_canvas_sets_passes():
    assert caused(game([chat("a", "met_a")]))[0] is True


def test_a_chain_through_a_caused_reply_passes_in_any_order():
    ok, head, _ = caused(game([chat("b", "said_yes"), chat("a", "met_a", sets="said_yes")]))
    assert ok is True and "2/2" in head


def test_an_uncaused_chat_and_its_chain_are_red():
    ok, _, detail = caused(game([chat("a", "nobody_sets", sets="x"), chat("b", "x")]))
    assert ok is False and len(detail) == 2 and "`nobody_sets`" in detail[0]


def test_a_flag_only_the_daily_tick_or_a_dev_canvas_sets_does_not_count():
    g = game([chat("a", "tick_flag"), chat("b", "dev_flag")], extra={
        "engine": {"daily_tick": {"flagEffects": [{"targetType": "player", "flag": "tick_flag"}]}}})
    g["canvases"].append({"id": "dev", "trigger": {"location": "work", **on("dev_mode_enabled")},
                          "nodes": [{"id": "n", "exit_block": {"config": {"flagEffects": [
                              {"flag": "dev_flag"}]}}}]})
    ok, _, detail = caused(g)
    assert ok is False and len(detail) == 2


def test_a_chat_with_no_flag_is_red():
    c = chat("a", "met_a")
    c["trigger"] = {}
    assert "holds no flag" in caused(game([c]))[2][0]


def test_a_call_needs_a_cause_too():
    call = {"id": "rings", "caller": "npc_a", "accept": "a_hub", "trigger": on("met_a")}
    assert caused(game(calls=[call]))[0] is True
    ok, _, detail = caused(game(calls=[dict(call, trigger=on("never"))]))
    assert ok is False and detail[0].startswith("call `rings`")


def test_no_phone_is_na_and_legacy_passes():
    assert caused(ws6.green_game())[0] is None
    gates._LEGACY_RULES.add("chat_caused")
    try:
        assert caused(game([chat("a", "nobody_sets")]))[0] is True
    finally:
        gates._LEGACY_RULES.discard("chat_caused")


def test_the_ship_row(tmp_path, monkeypatch):
    red = game([chat("a", "nobody_sets")])
    assert wr.ship(tmp_path, monkeypatch, "the_balance", red, ws6.green_state())[ROW] == "warn"
    assert wr.ship(tmp_path, monkeypatch, "billable_hours", red, ws6.green_state())[ROW] is False
    st = ws6.green_state()
    st["releases"] = [{"version": "0.2", "shipped": "2026-10-02"}]
    assert wr.ship(tmp_path, monkeypatch, "the_balance", red, st)[ROW] is False
    assert wr.ship(tmp_path, monkeypatch, "billable_hours", ws6.green_game(),
                   ws6.green_state())[ROW] is None
