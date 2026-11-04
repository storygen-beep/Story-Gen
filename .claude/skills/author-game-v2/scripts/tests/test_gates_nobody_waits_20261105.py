"""Gate `nobody waits for themselves` (first_term's café job, LO 2026-11-05). Fixtures are built here."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
from test_gates_group2_checks import ch, cv, game, nd  # noqa: E402

WHEN_MET = {"version": "1.0", "logic": "AND",
            "items": [{"type": "flag", "subject": "player", "flag_key": "tom_met", "operator": "is_true"}]}
TOM = {"id": "npc_tom", "name": "Tom", "schedules": [{"location": "room", "start_time": "08:00", "end_time": "22:00",
                                                     "weekdays": [0], "when": WHEN_MET}]}
SETS_MET = [{"targetType": "player", "flag": "tom_met", "op": "set"}]


def meet(**trigger):
    return cv("meet", [nd("a", [ch("Go.", flagEffects=SETS_MET)])], **trigger)


def check(*canvases, npcs=(TOM,)):
    return gates._nobody_waits_for_themselves(game(*canvases, npcs=list(npcs)))


def test_a_row_that_needs_the_person_it_meets_fails():
    ok, _, rows = check(meet(requires_npc="npc_tom"))
    assert ok is False and "npc_tom" in rows[0] and "tom_met" in rows[0]


def test_a_swapped_in_scene_that_needs_them_fails():
    assert check(meet(requires_npc="npc_tom", is_repeatable=False, substitution_only=True))[0] is False


def test_a_portrait_scene_fails():
    assert check(meet(npc="npc_tom"))[0] is False


def test_the_meeting_without_the_need_passes():
    assert check(meet(), cv("hub", [nd("a", [ch("Go.")])], npc="npc_tom"))[0] is True


def test_a_one_time_scene_that_fires_by_itself_passes():
    # played on first_term: zoe_00_quad_meeting opens with Zoe placed nowhere
    assert check(meet(requires_npc="npc_tom", is_repeatable=False))[0] is True


def test_one_row_with_no_wait_lets_them_arrive():
    free = dict(TOM, schedules=TOM["schedules"] + [{"location": "room", "start_time": "22:00", "end_time": "23:00",
                                                   "weekdays": [0]}])
    assert check(meet(requires_npc="npc_tom"), npcs=[free])[0] is True


def test_a_flag_set_elsewhere_passes():
    phone = cv("other", [nd("a", [ch("Go.", flagEffects=SETS_MET)])])
    assert check(meet(requires_npc="npc_tom"), phone)[0] is True


def test_a_flag_nothing_sets_is_not_this_gates_defect():
    assert check(cv("hub", [nd("a", [ch("Go.")])], npc="npc_tom"))[0] is True
