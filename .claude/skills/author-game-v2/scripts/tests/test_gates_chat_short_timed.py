"""`a chat is short and timed` (World and Systems PRD, Phase 6B, 2026-10-02): a WARN, a scored
gate that never blocks. Bubbles of 3–7 words, at most 3 in one message; every conversation
trigger has a delay and an hour window; a call needs the timing only. n/a with no phone.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_chats_caused as cc  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

TIMED = {"conditions": {"version": "1.0", "items": [
    {"type": "days_since_flag", "flag_key": "met_a", "operator": "gte", "value": 1},
    {"type": "time_of_day", "operator": "between", "value": ["18:00", "23:00"]}]}}


def msg(text, rnd=None, sender="npc"):
    return {"type": "message", "sender": sender, "content": text, **({"round": rnd} if rnd else {})}


def chat(*blocks, trigger=TIMED):
    return {"id": "a", "app": "messages", "npc": "npc_a", "trigger": trigger, "blocks": list(blocks)}


def run(convs=(), calls=()):
    return gates._chats_short_and_timed(cc.game(convs, calls))


def test_short_and_timed_passes():
    assert run([chat(msg("you up? come by"), msg("door's open tonight"))])[0] is True


def test_a_long_or_a_one_word_bubble_warns():
    ok, _, d = run([chat(msg("this message is far too long to be a text at all"), msg("hey"))])
    assert ok is False and "12-word bubble" in d[0] and "1-word bubble" in d[1]


def test_four_bubbles_in_one_message_warn_and_a_reply_resets_the_run():
    b = [msg("one two three")] * 4
    assert any("more than 3 bubbles" in x for x in run([chat(*b)])[2])
    split = b[:2] + [{"type": "reply", "round": 1, "choices": []}] + b[:2]
    assert run([chat(*split)])[0] is True


def test_an_untimed_trigger_warns():
    ok, _, d = run([chat(msg("you up? come by"), trigger=cc.on("met_a"))])
    assert ok is False and "a delay" in d[0] and "an hour window" in d[0]


def test_hours_since_flag_and_weekday_count():
    t = {"conditions": {"items": [{"type": "hours_since_flag", "flag_key": "met_a"},
                                  {"type": "weekday", "weekdays": [5]}]}}
    assert run([chat(msg("you up? come by"), trigger=t)])[0] is True


def test_a_call_needs_timing_only():
    call = {"id": "rings", "caller": "npc_a", "accept": "a_hub", "trigger": TIMED}
    assert run(calls=[call])[0] is True
    assert run(calls=[dict(call, trigger=cc.on("met_a"))])[0] is False


def test_no_phone_is_na():
    assert gates._chats_short_and_timed(ws6.green_game())[0] is None


def test_it_is_not_a_ship_block():
    assert "a chat is short and timed" not in gates.SHIP_BLOCK_GATES
