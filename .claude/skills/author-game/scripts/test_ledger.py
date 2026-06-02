import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

import ledger


def test_init_ledger_has_v1_shape():
    led = ledger.init_ledger("demo")
    assert led["game_slug"] == "demo"
    assert led["schema_version"] == 1
    assert led["book_revision"] == 1
    assert led["plan"] == []
    assert led["next_up"] == []
    assert led["decisions_log"] == []
    assert led["structure_registry"] == {
        "locations": [], "npcs": [], "flags": [], "schedules": []
    }


def test_save_then_load_roundtrips(tmp_path):
    led = ledger.init_ledger("demo")
    ledger.save_ledger(tmp_path, led)
    assert (tmp_path / "authoring_state.json").exists()
    back = ledger.load_ledger(tmp_path)
    assert back == led


def test_saved_file_is_pretty_json(tmp_path):
    led = ledger.init_ledger("demo")
    ledger.save_ledger(tmp_path, led)
    text = (tmp_path / "authoring_state.json").read_text()
    assert text.endswith("\n")
    assert json.loads(text)["game_slug"] == "demo"


def test_add_structure_appends():
    led = ledger.init_ledger("demo")
    ledger.add_structure(led, "flags", "hired_at_diner")
    ledger.add_structure(led, "locations", "loc_diner_front")
    assert led["structure_registry"]["flags"] == ["hired_at_diner"]
    assert led["structure_registry"]["locations"] == ["loc_diner_front"]


def test_add_structure_rejects_duplicate():
    led = ledger.init_ledger("demo")
    ledger.add_structure(led, "flags", "hired_at_diner")
    with pytest.raises(ValueError, match="already registered"):
        ledger.add_structure(led, "flags", "hired_at_diner")


def test_add_structure_rejects_unknown_kind():
    led = ledger.init_ledger("demo")
    with pytest.raises(KeyError, match="unknown structure kind"):
        ledger.add_structure(led, "widgets", "x")


def test_add_beat_assigns_padded_id_and_queues():
    led = ledger.init_ledger("demo")
    b = ledger.add_beat(led, type="npc_intro", title="Meet Hank",
                        desc="d", target_phase="5_scenes.toml")
    assert b["id"] == "beat_0001"
    assert b["status"] == "planned"
    assert led["plan"][0]["id"] == "beat_0001"
    assert led["next_up"] == ["beat_0001"]
    b2 = ledger.add_beat(led, type="economic", title="Buy home",
                         desc="d", target_phase="0_systems_spec.toml")
    assert b2["id"] == "beat_0002"


def test_add_beat_rejects_bad_type():
    led = ledger.init_ledger("demo")
    with pytest.raises(ValueError, match="invalid beat type"):
        ledger.add_beat(led, type="nonsense", title="t", desc="d",
                        target_phase="5_scenes.toml")


def test_get_beat_returns_same_object():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    got = ledger.get_beat(led, "beat_0001")
    assert got["title"] == "t"


def test_mark_beat_updates_status_and_dequeues_when_validated():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    ledger.mark_beat(led, "beat_0001", "active")
    assert ledger.get_beat(led, "beat_0001")["status"] == "active"
    ledger.mark_beat(led, "beat_0001", "validated")
    assert ledger.get_beat(led, "beat_0001")["status"] == "validated"
    assert "beat_0001" not in led["next_up"]


def test_mark_beat_rejects_bad_status():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    with pytest.raises(ValueError, match="invalid status"):
        ledger.mark_beat(led, "beat_0001", "done")
