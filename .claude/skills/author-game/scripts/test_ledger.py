import json
import os
import sys

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
