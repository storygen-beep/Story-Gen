"""World and Systems PRD W5: the pitch pack prints her life's threads (want.threads[], the-want.md §6)
for the her-life Pitcher, takes --thread, and lets --person name a new person only inside a thread.
Everything is written to a temp dir; nothing in games/ is read or written."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402

THREADS = [{"id": "job", "name": "the café shift", "person": "npc_boss", "place": "cafe",
            "system": "job", "link": "the tips pay what the house charges"},
           {"id": "dating", "name": "dating", "person": "npc_kai", "place": "dock",
            "system": "phone", "link": "a man she brings home"}]

STATE = {
    "phase": "idea",
    "want": {"fantasy_shape": "taboo_at_home",
             "places": [{"id": "home", "name": "The House"}, {"id": "cafe", "name": "The Café"}],
             "cast": [{"id": "npc_step", "age": 45, "keeps": "want + power"},
                      {"id": "npc_boss", "age": 38, "keeps": "step counter + memory flags"}],
             "threads": THREADS},
}


def idea(tmp_path, monkeypatch, capsys, *extra, state=STATE):
    d = tmp_path / "games" / "fx"
    d.mkdir(parents=True, exist_ok=True)
    (d / "v2_state.json").write_text(json.dumps(state))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["pitch_pack.py", "fx", *extra])
    assert pitch_pack.main() == 0
    return capsys.readouterr().out


def built(tmp_path, monkeypatch, capsys, person=None, thread=None):
    game = {"project": {"id": "fx"}, "locations": [{"id": "home"}, {"id": "cafe"}],
            "npcs": [{"id": "npc_step", "name": "Step"}], "canvases": []}
    monkeypatch.setattr(pitch_pack.gates, "_load", lambda path: game)
    sp = tmp_path / "v2_state.json"
    sp.write_text(json.dumps(STATE))
    monkeypatch.chdir(tmp_path)
    assert pitch_pack.pack("fx", "unused.toml", str(sp), person=person, thread=thread) == 0
    return capsys.readouterr().out


def test_idea_phase_prints_a_threads_section(tmp_path, monkeypatch, capsys):
    out = idea(tmp_path, monkeypatch, capsys)
    block = out[out.index("THREADS — 2"):out.index("PEOPLE —")]
    assert "job" in block and "person npc_boss" in block and "place cafe" in block
    assert "link into the hook: the tips pay what the house charges" in block
    # facts, never scores: the dating thread's person and place are not declared elsewhere
    assert "person not in want.cast; place not among PLACES" in " ".join(block.split())
    assert "her life, the threads 2 declared" in out


def test_thread_flag_prints_one_thread(tmp_path, monkeypatch, capsys):
    out = idea(tmp_path, monkeypatch, capsys, "--thread", "job")
    block = out[out.index("THREADS —"):out.index("PEOPLE —")]
    assert "<- your thread" in block and "dating" not in block
    assert "may add ONE new person" in block
    out = idea(tmp_path, monkeypatch, capsys, "--thread", "nope")
    assert "unknown thread `nope`" in out


def test_new_person_only_with_a_thread(tmp_path, monkeypatch, capsys):
    out = idea(tmp_path, monkeypatch, capsys, "--person", "npc_new")
    assert "unknown person `npc_new`" in out
    out = idea(tmp_path, monkeypatch, capsys, "--thread", "job", "--person", "npc_new")
    assert "new person `npc_new` — joins thread `job`" in out
    assert "unknown person" not in out


def test_no_threads_says_so(tmp_path, monkeypatch, capsys):
    st = {"phase": "idea", "want": {"cast": [{"id": "npc_a", "age": 30}]}}
    out = idea(tmp_path, monkeypatch, capsys, state=st)
    assert "THREADS — 0" in out and "none declared — want.threads[]" in out
    assert "her life, the threads not declared" in out


def test_idea_json_carries_threads_in_the_promise(tmp_path, monkeypatch, capsys):
    out = idea(tmp_path, monkeypatch, capsys, "--json")
    assert json.loads(out)["promise"]["threads"][0]["id"] == "job"


def test_built_pack_threads_and_the_caller_split(tmp_path, monkeypatch, capsys):
    out = built(tmp_path, monkeypatch, capsys)
    assert "THREADS — 2" in out
    assert "top two to two Pitchers, plus one thread" in " ".join(out.split())
    assert "three most owed" not in out and "top three" not in out
    out = built(tmp_path, monkeypatch, capsys, person="npc_new")
    assert "unknown person `npc_new`" in out
    out = built(tmp_path, monkeypatch, capsys, person="npc_new", thread="dating")
    assert "new person `npc_new` — joins thread `dating`" in out
