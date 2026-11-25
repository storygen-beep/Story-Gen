"""people.py: check.py's `people` check, CoT's people system under `[engine.people] system = "cot"`. Planted dict games;
nothing in games/ is read. LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead
with your picks", "Go ahead"."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import people  # noqa: E402
import rules  # noqa: E402


def person(**kw):
    n = {"id": "npc_tom", "name": "Tom", "gender": "male", "attracted": True, "people_type": "worker",
         "traits": ["Forward", "Loner"]}
    n.update(kw)
    return {k: v for k, v in n.items() if v is not None}


def talk(*conds, gate=None):
    choice = {"text": "Ask about his day", "conditions": {"version": "1.0", "items": list(conds)}}
    if gate is not None:
        choice["skill_gate"] = gate
    return {"id": "tom_talk", "nodes": [{"id": "a", "exit_block": {"choices": [choice]}}]}


LONER = {"type": "npc_has_trait", "npc_id": "npc_tom", "trait": "Loner"}


def planted(*npcs, canvases=None, switch=True, skills=("exhibitionism",), caps=None):
    game = {"npcs": list(npcs) or [person()], "canvases": canvases if canvases is not None else [talk(LONER)],
            "player": {"core_traits": {k: 0 for k in skills}},
            "traits": {"labels": [{"key": k, "label": k.title(), "skill": True} for k in skills]}}
    engine = {}
    if switch:
        engine["people"] = {"system": "cot"}
    if caps:
        engine["daily_caps"] = caps
    game["engine"] = engine
    return game


def test_a_typed_person_with_jobs_for_both_traits_is_green():
    assert people.problems(planted()) == []


def test_no_switch_no_check():
    assert people.problems(planted(person(gender=None, traits=[]), switch=False)) == []


def test_gender_and_attracted_are_needed():
    rows = people.problems(planted(person(gender=None, attracted=None)))
    assert any("`gender`" in r for r in rows) and any("`attracted`" in r for r in rows)


def test_a_person_with_no_type_and_nothing_hand_set_is_red():
    assert any("people_type" in r for r in people.problems(planted(person(people_type=None))))


def test_hand_set_values_stand_in_for_a_type():
    assert people.problems(planted(person(people_type=None, core_traits={"friendship": 300}))) == []
    assert people.problems(planted(person(people_type=None, want="rival"))) == []


def test_no_trait_is_red_and_five_is_too_many():
    assert any("no trait" in r for r in people.problems(planted(person(traits=[]))))
    five = ["Forward", "Shy", "Chaste", "Slut", "Dominant"]
    assert any("5 traits" in r for r in people.problems(planted(person(traits=five))))


def test_a_sex_trait_with_no_job_is_red():
    rows = people.problems(planted(person(traits=["Forward", "Groper"]), canvases=[talk()]))  # nothing reads Groper
    assert any("`Groper` has no job" in r for r in rows)
    assert not any("`Forward`" in r for r in rows)


def test_a_manner_or_hobby_trait_needs_no_reader():
    # P48 (LO, "Yes to both A and B", 2026-11-25): shown personality traits are learned on the People view.
    assert people.problems(planted(person(traits=["Bully", "Gamer", "Shy"]), canvases=[talk()])) == []


def test_chaste_has_a_job_without_a_set():
    assert people.problems(planted(person(traits=["Chaste"]), canvases=[talk()])) == []


def test_a_set_read_by_a_condition_gives_its_traits_a_job():
    cond = {"type": "npc_has_trait", "npc_id": "npc_tom", "set": "shy"}
    assert people.problems(planted(person(traits=["Shy"]), canvases=[talk(cond)])) == []


def test_an_old_person_meter_is_red():
    rows = people.problems(planted(person(core_traits={"warmth": 20}, trait_decay={"warmth": 1})))
    assert any("keeps `warmth`" in r for r in rows) and any("decays `warmth`" in r for r in rows)


def test_an_effect_on_an_old_person_meter_is_red():
    choice = {"text": "Smile", "effects": [{"targetType": "npc", "npcId": "npc_tom", "trait": "want", "op": "add",
                                            "value": 2}]}
    game = planted(canvases=[talk(LONER), {"id": "c", "nodes": [{"id": "a", "exit_block": {"choices": [choice]}}]}])
    assert any("moves `npc_tom`'s `want`" in r for r in people.problems(game))


def test_a_professor_keeps_intimacy():
    prof = person(professor=True, core_traits={"intimacy": 1})
    assert people.problems(planted(prof)) == []
    assert any("keeps `intimacy`" in r for r in people.problems(planted(person(core_traits={"intimacy": 1}))))


def test_a_skill_gate_names_one_of_her_skills():
    ok = planted(canvases=[talk(LONER, gate={"skill": "exhibitionism", "level": 2})])
    assert people.problems(ok) == []
    bad = people.problems(planted(canvases=[talk(LONER, gate={"skill": "corruption", "level": 12})]))
    assert any("`corruption`" in r for r in bad) and any("level 12" in r for r in bad)


def test_a_skill_level_condition_names_one_of_her_skills():
    cond = {"type": "skill_level", "skill": "nerve", "level": 2}
    assert any("`nerve`" in r for r in people.problems(planted(canvases=[talk(LONER, cond)])))


def test_a_skill_with_a_band_table_too_is_red():
    caps = {"exhibitionism": {"bands": [{"below": 101, "cap": 2}]}}
    assert any("cut it twice" in r for r in people.problems(planted(caps=caps)))


def test_a_skill_gate_is_a_meter_on_the_screen():
    assert "a meter is shown or paid" in rules.seen(planted(canvases=[talk(gate={"skill": "exhibitionism",
                                                                                "level": 1})]))["tom_talk.a"]


def test_check_runs_it():
    assert "people" in check.CHECKS
    assert check.check_people(planted(person(traits=[])))[0] == check.RED
    assert check.check_people(None)[0] == check.INCOMPLETE


def test_only_hidden_traits_is_red():
    # P48: Laura, Nadia, Zoe, Kayla and Tess had one hidden trait and an empty personality.
    rows = people.problems(planted(person(traits=["Loyal"]), canvases=[talk()]))
    assert any("only hidden traits" in r for r in rows)
    assert not any("only hidden" in r for r in people.problems(planted(person(traits=["Loyal", "Cook"]))))
