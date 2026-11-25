"""people.py: check.py's `people` check, CoT's people system under `[engine.people] system = "cot"`. Planted dict games;
nothing in games/ is read. LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead
with your picks", "Go ahead"; trait words hidden and our own, 2026-11-26: "Hide them dont show them, they are for us"."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import people  # noqa: E402
import rules  # noqa: E402


def person(**kw):
    n = {"id": "npc_tom", "name": "Tom", "gender": "male", "attracted": True, "people_type": "worker",
         "traits": ["Pushy", "Kind"]}
    n.update(kw)
    return {k: v for k, v in n.items() if v is not None}


WORDS = {w: {"kind": "personality", "description": f"{w}, in how he is with her."}
         for w in ("Pushy", "Kind", "Shy", "Cook", "Gamer")}


def talk(*conds, gate=None):
    choice = {"text": "Ask about his day", "conditions": {"version": "1.0", "items": list(conds)}}
    if gate is not None:
        choice["skill_gate"] = gate
    return {"id": "tom_talk", "nodes": [{"id": "a", "exit_block": {"choices": [choice]}}]}


LONER = {"type": "npc_has_trait", "npc_id": "npc_tom", "trait": "Kind"}


def planted(*npcs, canvases=None, switch=True, skills=("exhibitionism",), caps=None, show=False, words=WORDS):
    game = {"npcs": list(npcs) or [person()], "canvases": canvases if canvases is not None else [talk(LONER)],
            "player": {"core_traits": {k: 0 for k in skills}},
            "traits": {"labels": [{"key": k, "label": k.title(), "skill": True} for k in skills]}}
    engine = {}
    if switch:
        engine["people"] = {"system": "cot", "traits": dict(words)}
        if show is not None:
            engine["people"]["show_traits"] = show
    if caps:
        engine["daily_caps"] = caps
    game["engine"] = engine
    return game


def test_a_typed_person_with_two_own_words_is_green():
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


def test_two_to_four_words():
    # C2193: a few words used often beat many used rarely
    assert any("1 trait word(s)" in r for r in people.problems(planted(person(traits=["Kind"]))))
    five = ["Pushy", "Kind", "Shy", "Cook", "Gamer"]
    assert any("5 trait word(s)" in r for r in people.problems(planted(person(traits=five))))
    assert people.problems(planted(person(traits=five[:4]))) == []


def test_traits_are_hidden():
    # LO, 2026-11-26: "Hide them dont show them, they are for us"
    for show in (True, None):
        assert any("show_traits is not false" in r for r in people.problems(planted(show=show)))


def test_every_word_is_the_games_own():
    # Forward is in CoT's default table, so the importer takes it; the skill doesn't (C2184)
    rows = people.problems(planted(person(traits=["Pushy", "Forward"])))
    assert any("`Forward` has no row in [engine.people.traits.Forward]" in r for r in rows)
    assert not any("`Pushy`" in r for r in rows)


def test_a_word_needs_no_reader_and_no_number_job():
    # retired 2026-11-26: "every trait has a job" and "only hidden traits is red"
    assert people.problems(planted(person(traits=["Shy", "Cook"]), canvases=[talk()])) == []


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
