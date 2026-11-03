"""LO, 2026-11-03: "teach the button check to count per hour. Make the talking check skip
scenes where nobody else is there."

  `a place is not a catalogue` — a screen's count is the most distinct labels whose time
      items (`time_of_day`, `weekday`, the trigger's `schedules`) can hold at one step of the
      week; every other item counts as possibly true. The headline names the hour of the max.
  `somebody speaks` — a canvas where she is alone (no npc on the trigger, no dialog from
      anyone but her, no `npc_at_location is_present`, no named character who could be
      there) is left out of both sides of the ratio and out of the silent list.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}
CAT = "a place is not a catalogue"
TALK = "somebody speaks"


def row(game, name):
    model, g2 = gates.build(copy.deepcopy(game))
    return next(r for r in gates.run_gates(model, g2, {}) if r["gate"] == name)


def timed(start, end, days=None):
    items = [{"type": "time_of_day", "start_time": start, "end_time": end}]
    if days is not None:
        items.append({"type": "weekday", "weekdays": days})
    items.append({"type": "flag", "subject": "player", "flag_key": "x", "operator": "is_false"})
    return dict(V1, items=items)


def screen(choices, trigger_extra=None):
    trig = {"location": "kitchen", "is_repeatable": True}
    trig.update(trigger_extra or {})
    return {"project": {"id": "fx", "name": "fx"}, "locations": [{"id": "kitchen"}],
            "canvases": [{"id": "hub", "trigger": trig, "nodes": [
                {"id": "n", "blocks": [{"type": "paragraph", "content": "The kitchen."}],
                 "exit_block": {"choices": choices}},
                {"id": "m", "blocks": [{"type": "paragraph", "content": "Done."}]}]}]}


def act(label, conds=None):
    ch = {"text": label, "targetType": "node", "nodeId": "m"}
    if conds:
        ch["conditions"] = conds
    return ch


# ── a place is not a catalogue: per hour ─────────────────────────────────────

def test_morning_and_evening_buttons_never_share_the_screen():
    """12 labels on the node, but 6 are morning-only and 6 evening-only: 6 at once, pass."""
    ch = ([act(f"Morning {i}.", timed("06:30", "08:00")) for i in range(6)]
          + [act(f"Evening {i}.", timed("19:00", "21:00", [1])) for i in range(6)])
    r = row(screen(ch), CAT)
    assert r["pass_"] is True, r
    assert "hub: 6 at Mon 06:30" in r["headline"], r["headline"]


def test_the_hour_of_the_max_is_named():
    """Evening set is bigger and Tuesday-only: the peak is reported at Tue 19:00."""
    ch = ([act(f"Morning {i}.", timed("06:30", "08:00")) for i in range(2)]
          + [act(f"Evening {i}.", timed("19:00", "21:00", [1])) for i in range(5)]
          + [act("Talk to her.")])
    assert "hub: 6 at Tue 19:00" in row(screen(ch), CAT)["headline"]


def test_a_window_is_end_exclusive():
    """18:00-19:00 and 19:00-20:00 never overlap, the same rule the engine uses."""
    ch = ([act(f"Cook {i}.", timed("18:00", "19:00")) for i in range(5)]
          + [act(f"Dishes {i}.", timed("19:00", "20:00")) for i in range(5)])
    r = row(screen(ch), CAT)
    assert "hub: 5 at" in r["headline"] and r["pass_"] is True


def test_the_trigger_schedule_narrows_the_hours():
    """The canvas only shows 19:00-20:00, so the morning set is never on screen with it."""
    ch = ([act(f"Morning {i}.", timed("06:30", "08:00")) for i in range(9)]
          + [act(f"Evening {i}.", timed("19:00", "21:00")) for i in range(3)])
    sched = {"schedules": [{"start_time": "19:00", "end_time": "20:00"}]}
    r = row(screen(ch, sched), CAT)
    assert r["pass_"] is True and "hub: 3 at Mon 19:00" in r["headline"], r["headline"]


def test_untimed_buttons_still_go_red():
    """Nine labels with only flag conditions can all be live at once: 9 > 8, still red."""
    flag = dict(V1, items=[{"type": "flag", "subject": "player", "flag_key": "x",
                            "operator": "is_false"}])
    r = row(screen([act(f"Act {i}.", flag) for i in range(9)]), CAT)
    assert r["pass_"] is False
    assert any("9 decisions on one screen at any hour" in d for d in r["detail"]), r["detail"]


def test_overlapping_windows_still_go_red():
    """Nine labels whose windows all cover 20:00 are nine at once: red, at the hour named."""
    ch = [act(f"Evening {i}.", timed(f"{18 + i % 3}:00", "22:00", [2])) for i in range(9)]
    r = row(screen(ch), CAT)
    assert r["pass_"] is False
    assert any("9 decisions on one screen at Wed 20:00" in d for d in r["detail"]), r["detail"]


# ── somebody speaks: she alone needs no speech ───────────────────────────────

def words(n, w="quiet"):
    return " ".join([w] * n)


def canvas(cid, blocks, trig=None):
    t = {"location": "room", "is_repeatable": True}
    t.update(trig or {})
    return {"id": cid, "trigger": t, "nodes": [{"id": "n", "blocks": blocks}]}


def talk_game(*canvases, npcs=None):
    return {"project": {"id": "fx", "name": "fx"}, "locations": [{"id": "room"}],
            "npcs": npcs or [{"id": "npc_laura", "name": "Laura"}], "canvases": list(canvases)}


SOLO = canvas("mirror", [{"type": "paragraph", "content": words(300)}])
TALKY = canvas("hub_laura", [{"type": "paragraph", "content": words(50)},
                             {"type": "dialog", "content": words(20, "hello"),
                              "props": {"speaker": "npc", "npc_id": "npc_laura"}}],
               {"npc": "npc_laura"})


def test_a_solo_canvas_leaves_both_sides_of_the_ratio():
    r = row(talk_game(SOLO, TALKY), TALK)
    assert r["pass_"] is True, r["headline"]                 # 50:20, not 350:20
    assert "2.5:1" in r["headline"]
    assert "1 solo canvases skipped: she is alone" in r["headline"]
    assert not any(d.startswith("mirror:") for d in r["detail"])


def test_her_own_line_keeps_a_canvas_solo():
    me = canvas("mirror", [{"type": "paragraph", "content": words(300)},
                           {"type": "dialog", "content": "God.", "props": {"speaker": "player"}}])
    assert gates._solo_canvases(talk_game(me, TALKY)) == {"mirror"}


def test_a_person_present_and_silent_still_counts():
    """requires_npc puts Laura there and nobody talks: listed as silent, ratio red."""
    mute = canvas("laura_reads", [{"type": "paragraph", "content": words(300)}],
                  {"requires_npc": "npc_laura"})
    r = row(talk_game(mute, TALKY), TALK)
    assert r["pass_"] is False
    assert any(d.startswith("laura_reads: 300 words") for d in r["detail"]), r["detail"]
    assert "0 solo canvases skipped" in r["headline"]


def test_a_named_person_who_could_be_there_is_company():
    """Prose naming Laura, who has no schedule rows (could be anywhere), is not solo; the same
    canvas asking `npc_at_location is_absent` for her is."""
    named = canvas("bedroom", [{"type": "paragraph", "content": "Laura sleeps. " + words(100)}])
    assert gates._solo_canvases(talk_game(named, TALKY)) == set()
    away = copy.deepcopy(named)
    away["trigger"]["conditions"] = dict(V1, items=[{"type": "npc_at_location", "npc_id": "npc_laura",
                                                     "location_id": "room", "operator": "is_absent"}])
    assert gates._solo_canvases(talk_game(away, TALKY)) == {"bedroom"}


def test_a_presence_variant_or_a_stranger_line_is_company():
    group = canvas("park", [{"type": "group", "conditions": dict(V1, items=[
        {"type": "npc_at_location", "location_id": "room", "operator": "is_present"}]),
        "blocks": [{"type": "paragraph", "content": "Someone jogs past."}]},
        {"type": "paragraph", "content": words(80)}])
    stranger = canvas("street", [{"type": "dialog", "content": "Nice legs.",
                                  "props": {"speaker": "unknown"}},
                                 {"type": "paragraph", "content": words(80)}])
    assert gates._solo_canvases(talk_game(group, stranger, TALKY)) == set()
