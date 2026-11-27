"""scenes.py: each check passes a clean game and goes red on a planted break, so no green here can't go red."""
import copy
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scenes  # noqa: E402

GREEN, RED = scenes.GREEN, scenes.RED


def para(text):
    return {"type": "paragraph", "content": text}


def say(text, npc="npc_mom"):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def group(*blocks, **cond):
    return {"type": "group", "props": {"conditions": cond or {"version": "1.0"}}, "blocks": list(blocks)}


def node(nid, *blocks, to=()):
    return {"id": nid, "blocks": list(blocks),
            "exit_block": {"type": "choices", "choices": [{"text": f"Go to {t}", "targetType": "node", "nodeId": t,
                                                            "flagEffects": [{"flag": f"went_{t}", "op": "set"}]}
                                                           for t in to]}}


def clean():
    """A small game every check passes: Mom in the kitchen 7-9 every day, one scene there, one name field printed."""
    return {
        "player": {"customization_fields": [{"id": "name", "label": "Your name"}], "flag_keys": ["met_mom"],
                   "core_traits": {"energy": 100}},
        "traits": {"labels": [{"key": "energy"}]},
        "sidebar_items": [{"type": "trait_bar", "trait": "energy", "max": 100}],
        "locations": [{"id": "kitchen"}],
        "npcs": [{"id": "npc_mom", "name": "Laura", "role": "Mom",
                  "schedules": [{"location": "kitchen", "start_time": "07:00", "end_time": "09:00"}]}],
        "quest_cards": [{"npc_id": "npc_mom", "goals": [{"label": "Pay the rent", "flag": "paid", "op": "is_true"}]}],
        "canvases": [{
            "id": "breakfast",
            "trigger": {"location": "kitchen", "is_repeatable": True,
                        "conditions": {"version": "1.0", "items": [
                            {"type": "time_of_day", "start_time": "07:00", "end_time": "09:00"}]}},
            "nodes": [node("a", para("Mom is at the stove."), say("Morning, @player. Eggs?"), to=["b"]),
                      node("b", para("She slides the plate over."), say("Eat. You're late."))],
        }],
    }


# ── talk ──

def test_talk_clean_is_green():
    assert scenes.check_talk(clean()) == (GREEN, [])


def test_planted_silent_person_is_red_talk():
    g = clean()
    g["canvases"][0]["nodes"][1]["blocks"] = [para("Mom slides the plate over and watches you eat every bite of it, "
                                                   "slowly, without a word, the radio on low behind her.")]
    status, rows = scenes.check_talk(g)
    assert status == RED and "breakfast" in rows[0] and "a > b" in rows[0]


def test_talk_judges_every_path_and_the_worst_variant():
    g = clean()
    long = para("Mom stands at the window a long time with the cup in both hands and says nothing at all to you.")
    g["canvases"][0]["nodes"][0]["blocks"] = [group(para("Mom is at the stove.")), group(long), say("Eggs?")]
    status, rows = scenes.check_talk(g)
    assert status == RED  # the silent window variant is one the player can get


def test_a_person_in_one_group_is_company_only_in_that_variant():
    """LO 2026-11-27, the TV list: Mom named in one group, the other group has nobody, and the next screen is hers
    alone. The empty variant is not counted as company, so the path is green."""
    g = clean()
    present = {"version": "1.0", "logic": "AND", "items": [
        {"type": "npc_at_location", "npc_id": "npc_mom", "location_id": "kitchen", "operator": "is_present"}]}
    g["canvases"][0]["nodes"] = [
        node("a", group(para("Mom is at the stove."), say("Eggs?"), **present),
             group(para("You curl up at the end of the couch with the remote and find something to watch.")), to=["b"]),
        node("b", para("You watch the screen a long time with the sound right down and your knees pulled up."))]
    assert scenes.check_talk(g) == (GREEN, [])


def test_a_silent_person_in_their_own_group_is_still_red():
    g = clean()
    g["canvases"][0]["nodes"] = [node("a", group(para(
        "Mom stands at the window a long time with the cup in both hands and says nothing at all to you.")),
        group(para("Nobody's in.")))]
    status, rows = scenes.check_talk(g)
    assert status == RED and "breakfast" in rows[0]


def test_quoted_speech_in_a_paragraph_counts_as_speech():
    assert scenes.text_split(para('Mom looks up. "Is that mine?"')) == (3, 3)


def test_a_scene_she_is_alone_in_needs_no_speech():
    g = clean()
    g["canvases"][0]["nodes"] = [node("a", para("You stand under the shower a long time and let the water run "
                                               "down your back until it goes cold."))]
    assert scenes.check_talk(g) == (GREEN, [])


# ── length ──

def test_length_clean_is_green():
    assert scenes.check_length(clean()) == (GREEN, [])


def test_planted_long_screen_is_red_length():
    g = clean()
    g["canvases"][0]["nodes"][0]["blocks"].append(para("word " * 160))
    status, rows = scenes.check_length(g)
    assert status == RED and "breakfast · a" in rows[0]


def test_adjacent_groups_count_their_longest_only():
    blocks = [group(para("word " * 100)), group(para("word " * 100))]
    assert scenes.screen_words(blocks) == 100


# ── presence ──

def test_presence_clean_is_green():
    assert scenes.check_presence(clean()) == (GREEN, [])


def test_planted_speaker_outside_her_rows_is_red_presence():
    g = clean()
    g["canvases"][0]["trigger"]["conditions"]["items"][0]["end_time"] = "10:00"
    status, rows = scenes.check_presence(g)
    assert status == RED and "Laura speaks at kitchen" in rows[0] and "09:00" in rows[0]


def test_a_scene_bound_to_the_speaker_is_not_red():
    g = clean()
    g["canvases"][0]["trigger"]["conditions"]["items"][0]["end_time"] = "10:00"
    g["canvases"][0]["trigger"]["requires_npc"] = "npc_mom"
    assert scenes.check_presence(g) == (GREEN, [])


# ── creation ──

def test_creation_clean_is_green():
    assert scenes.check_creation(clean()) == (GREEN, [])


def test_planted_name_never_printed_is_red_creation():
    g = clean()
    g["canvases"][0]["nodes"][0]["blocks"][1]["content"] = "Morning. Eggs?"
    status, rows = scenes.check_creation(g)
    assert status == RED and "`name`" in rows[0]


def test_name_at_the_end_of_a_sentence_counts():
    g = clean()
    g["canvases"][0]["nodes"][0]["blocks"][1]["content"] = "Eggs, @player."
    assert scenes.check_creation(g) == (GREEN, [])


# ── saves ──

def test_saves_same_build_is_green(tmp_path):
    assert scenes.check_saves(tmp_path, clean(), baseline=clean(), ref="x") == (GREEN, [])


def test_planted_removed_flag_and_scene_are_red_saves(tmp_path):
    now = clean()
    now["player"]["flag_keys"] = []
    now["canvases"][0]["id"] = "breakfast_2"
    status, rows = scenes.check_saves(tmp_path, now, baseline=clean(), ref="x")
    assert status == RED and any("flag `met_mom`" in r for r in rows) and any("scene `breakfast`" in r for r in rows)


def test_planted_flag_set_by_a_new_choice_is_red_until_notes_say_same_meaning(tmp_path):
    now = clean()
    now["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["text"] = "Skip breakfast"
    status, rows = scenes.check_saves(tmp_path, now, baseline=clean(), ref="x")
    assert status == RED and "flag `went_b`" in rows[0]
    (tmp_path / "NOTES.md").write_text("Same meaning: went_b · LO: yes\n")
    assert scenes.check_saves(tmp_path, now, baseline=clean(), ref="x") == (GREEN, [])


def test_planted_meter_range_change_is_red_saves(tmp_path):
    now = clean()
    now["sidebar_items"][0]["max"] = 10
    status, rows = scenes.check_saves(tmp_path, now, baseline=clean(), ref="x")
    assert status == RED and "meter `energy`" in rows[0]


def test_saves_reads_the_last_played_build_from_git(tmp_path):
    import tomllib  # noqa: F401  (the game below is written as TOML by hand)
    g = tmp_path / "games" / "tiny"
    (g / "toml_phases").mkdir(parents=True)
    (g / "output").mkdir()
    toml = g / "toml_phases" / "7_final_game.toml"
    toml.write_text('[player]\nflag_keys = ["met_mom"]\n')
    (g / "output" / "index.html").write_text("<html></html>")
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(git + ["add", "."], cwd=tmp_path, check=True)
    subprocess.run(git + ["commit", "-qm", "played"], cwd=tmp_path, check=True)
    toml.write_text('[player]\nflag_keys = []\n')
    ref, base = scenes.played(g)
    assert ref and base["player"]["flag_keys"] == ["met_mom"]
    status, rows = scenes.check_saves(g, {"player": {"flag_keys": []}})
    assert status == RED and "flag `met_mom`" in rows[0]


def test_nothing_played_yet_is_green(tmp_path):
    assert scenes.played(tmp_path) == (None, None)


# ── speakers and goals ──

def test_speakers_clean_is_green():
    assert scenes.check_speakers(clean()) == (GREEN, [])


@pytest.mark.parametrize("props", [{}, {"speaker": "npc", "npcId": "npc_nobody"}])
def test_planted_unnamed_or_unknown_speaker_is_red(props):
    g = clean()
    g["canvases"][0]["nodes"][0]["blocks"][1]["props"] = props
    assert scenes.check_speakers(g)[0] == RED


def test_goals_clean_is_green():
    assert scenes.check_goals(clean()) == (GREEN, [])


@pytest.mark.parametrize("goal", [{"label": "Pay the rent", "flag": "paid", "op": "is_false"},
                                  {"label": "Rent left", "trait": "debt", "op": "lte", "value": 0},
                                  {"label": "3 Sundays paid", "trait": "paid", "op": "gte", "value": 3}])
def test_planted_goal_that_reads_wrong_is_red(goal):
    g = copy.deepcopy(clean())
    g["quest_cards"][0]["goals"] = [goal]
    assert scenes.check_goals(g)[0] == RED


# ── clock conditions: weekday and OR (P21's build, 2026-11-24: 13 false reds from ignored weekday items) ──

import who_is_where  # noqa: E402

MON_SAT = list(range(6))


def weekday_game(scene_days=MON_SAT, mom_days=MON_SAT):
    g = clean()
    g["npcs"][0]["schedules"][0]["weekdays"] = mom_days
    g["canvases"][0]["trigger"]["conditions"]["items"].append({"type": "weekday", "weekdays": scene_days})
    return g


def test_a_weekday_gated_scene_has_no_sunday_presence_red():
    assert scenes.check_presence(weekday_game()) == (GREEN, [])


def test_a_planted_sunday_scene_with_mom_off_on_sunday_stays_red():
    status, rows = scenes.check_presence(weekday_game(scene_days=list(range(7))))
    assert status == RED and "Sun" in rows[0]


def test_an_or_of_two_windows_covers_both():
    g = clean()
    g["npcs"][0]["schedules"].append({"location": "kitchen", "start_time": "18:00", "end_time": "19:00"})
    g["canvases"][0]["trigger"]["conditions"] = {"version": "1.0", "logic": "OR", "items": [
        {"type": "time_of_day", "start_time": "07:00", "end_time": "09:00"},
        {"type": "time_of_day", "start_time": "18:00", "end_time": "19:00"}]}
    slots = scenes.fire_slots(g["canvases"][0]["trigger"])
    assert (0, 7 * 60) in slots and (0, 18 * 60) in slots and (0, 12 * 60) not in slots
    assert scenes.check_presence(g) == (GREEN, [])
    g["npcs"][0]["schedules"].pop()  # Mom gone in the evening: the evening window is red
    assert scenes.check_presence(g)[0] == RED


def test_an_or_with_a_non_clock_item_never_narrows():
    cond = {"version": "1.0", "logic": "OR", "items": [
        {"type": "time_of_day", "start_time": "07:00", "end_time": "09:00"},
        {"type": "flag", "flag_key": "x", "operator": "is_true"}]}
    assert who_is_where.when_slots(cond) == set(who_is_where.SLOTS)


def test_an_empty_weekday_list_never_holds():
    assert who_is_where.item_slots({"type": "weekday", "weekdays": []}) == set()


def test_the_sheet_reads_the_weekday_too():
    import sheet
    g = weekday_game()
    row = sheet.compute(g, {"breakfast"})["breakfast.a"]
    assert row["who"] == "npc_mom" and row["clock"] == "07:00–09:00 +0 · Mon Tue Wed Thu Fri Sat"


# ── a line inside a group shows only when the group holds (P10's build, 2026-11-24) ──

def weekend_game(line_in_group=True, group_cond=None):
    g = clean()
    g["npcs"][0]["schedules"][0]["weekdays"] = [5]  # Mom in the kitchen Saturday mornings only
    g["canvases"][0]["trigger"]["conditions"]["items"].append({"type": "weekday", "weekdays": [5, 6]})
    line = say("Saturday. Eggs?")
    group_cond = group_cond or {"version": "1.0", "items": [{"type": "weekday", "weekdays": [5]}]}
    blocks = [para("The kitchen's quiet."), group(line, **group_cond) if line_in_group else line]
    g["canvases"][0]["nodes"] = [node("a", *blocks)]
    return g


def test_a_saturday_group_line_on_a_weekend_scene_is_green_on_sunday():
    assert scenes.check_presence(weekend_game()) == (GREEN, [])


def test_the_same_line_outside_the_group_is_red_on_sunday():
    status, rows = scenes.check_presence(weekend_game(line_in_group=False))
    assert status == RED and "Sun" in rows[0]


def test_a_group_with_a_time_window_narrows_too():
    g = clean()
    g["npcs"][0]["schedules"][0]["end_time"] = "08:00"  # Mom leaves at 8, the scene runs to 9
    g["canvases"][0]["nodes"][0]["blocks"] = [para("Mom is at the stove."), group(
        say("Morning. Eggs?"), version="1.0", items=[{"type": "time_of_day", "start_time": "07:00", "end_time": "08:00"}])]
    g["canvases"][0]["nodes"][1]["blocks"] = [para("She slides the plate over.")]
    assert scenes.check_presence(g) == (GREEN, [])
    g["canvases"][0]["nodes"][0]["blocks"][1] = say("Morning. Eggs?")  # out of the group: 08:00-09:00 is red
    assert scenes.check_presence(g)[0] == RED


def test_a_rescale_lo_accepted_is_waived_for_that_meter_only(tmp_path):
    # first_term_lean P48: exhibitionism 0-100 to a CoT skill; LO, typed in main-lean 2026-11-25: "its fine".
    now = clean()
    now["sidebar_items"][0]["max"] = 1000
    (tmp_path / "NOTES.md").write_text('- 2026-11-25 Rescaled: `energy` · LO, on his old save: "its fine"\n')
    assert scenes.check_saves(tmp_path, now, baseline=clean(), ref="x") == (GREEN, [])
    (tmp_path / "NOTES.md").write_text('- 2026-11-25 Rescaled: `money` · LO: "its fine"\n')
    assert scenes.check_saves(tmp_path, now, baseline=clean(), ref="x")[0] == RED


def test_a_rescale_without_los_words_or_date_is_refused(tmp_path):
    now = clean()
    now["sidebar_items"][0]["max"] = 1000
    for line in ("Rescaled: energy · LO: yes\n", 'Rescaled: energy · LO: "its fine"\n', "2026-11-25 Rescaled: energy\n"):
        (tmp_path / "NOTES.md").write_text(line)
        status, rows = scenes.check_saves(tmp_path, now, baseline=clean(), ref="x")
        assert status == RED and "is refused" in rows[0]


# ── repeats (C2202) ──

def repeat_game(*blocks, trigger_items=(), sets=()):
    g = clean()
    c = g["canvases"][0]
    c["trigger"]["conditions"]["items"] += list(trigger_items)
    c["nodes"] = [node("a", para("Mom is at the stove."), *blocks)]
    if sets:
        c["nodes"][0]["exit_block"]["choices"] = [{"text": "Go", "targetType": "location", "locationId": "kitchen",
                                                   "flagEffects": [{"flag": f, "op": "set"} for f in sets]}]
    return g


def test_repeats_clean_is_green():
    assert scenes.check_repeats(clean()) == (GREEN, [])


@pytest.mark.parametrize("line", ["Morning, new girl.", "Say your name. Louder.", "Next time I'll show you.",
                                  "Next rehearsal, you're on the stage."])
def test_planted_once_only_line_on_a_repeatable_is_red(line):
    assert scenes.check_repeats(repeat_game(say(line)))[0] == RED


def test_the_same_line_on_a_flags_not_yet_side_is_green():
    held = {"version": "1.0", "items": [{"type": "flag", "subject": "player", "flag_key": "shown", "operator": "is_false"}]}
    assert scenes.check_repeats(repeat_game(group(say("Next time I'll show you."), **held))) == (GREEN, [])


def test_a_repeatable_that_sets_the_flag_its_trigger_waits_on_plays_once():
    wait = {"type": "flag", "subject": "player", "flag_key": "first_done", "operator": "is_false"}
    g = repeat_game(say("So you're the new girl."), trigger_items=[wait], sets=["first_done"])
    assert scenes.check_repeats(g) == (GREEN, [])


def test_her_own_line_and_a_one_time_scene_are_not_judged():
    g = repeat_game({"type": "dialog", "content": "I'm the new girl.", "props": {"speaker": "player"}})
    assert scenes.check_repeats(g) == (GREEN, [])
    g = repeat_game(say("Nice to meet you."))
    g["canvases"][0]["trigger"]["is_repeatable"] = False
    assert scenes.check_repeats(g) == (GREEN, [])


@pytest.mark.parametrize("block", [say("Next time, then, darling."), say("You'll be counting the jar next time."),
                                   para("You step off with your face hot. Next time, you'll stand by the doors.")])
def test_planted_promise_in_any_form_or_in_narration_is_red(block):
    assert scenes.check_repeats(repeat_game(block))[0] == RED


def test_a_kept_appointment_and_her_first_meeting_words_in_narration_are_green():
    g = repeat_game(say("Short. Next Sunday, then. Both weeks."), para("He calls you the new girl."))
    assert scenes.check_repeats(g) == (GREEN, [])


def test_a_flag_a_tick_unsets_does_not_make_a_scene_play_once():
    wait = {"type": "flag", "subject": "player", "flag_key": "partied", "operator": "is_false"}
    g = repeat_game(say("Next time, then. I'm holding you to it."), trigger_items=[wait], sets=["partied"])
    assert scenes.check_repeats(g) == (GREEN, [])
    g["engine"] = {"weekly_tick": {"flagEffects": [{"targetType": "player", "flag": "partied", "op": "unset"}]}}
    assert scenes.check_repeats(g)[0] == RED


def test_a_flag_inside_an_or_is_not_a_plays_once_gate():
    either = {"type": "group", "logic": "OR", "items": [
        {"type": "flag", "subject": "player", "flag_key": "came", "operator": "is_false"},
        {"type": "days_since_flag", "subject": "player", "flag_key": "came", "operator": "gte", "value": 3}]}
    g = repeat_game(say("I'll check it next time."), trigger_items=[either], sets=["came"])
    assert scenes.check_repeats(g)[0] == RED
