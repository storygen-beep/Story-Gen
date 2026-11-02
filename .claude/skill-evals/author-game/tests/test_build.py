"""Build-stage checks on members_only (677cd30f): the original build passes, the prepared copy (piece
removed) fails, and the logged mistake fails."""
from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

EVAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL_DIR))
import lib  # noqa: E402

INTACT = lib.load_game(EVAL_DIR / "tests" / "fixture_members_only_7.toml")
CASES = {"b1_noor_pool_scene": "cases", "b2_noor_schedule": "cases", "b3_unsigned_sheet": "cases",
         "b4_room_without_sheet": "cases", "hb1_ade_docks_scene": "cases_holdout",
         "hb2_kessler_schedule": "cases_holdout"}


def check(cid):
    spec = importlib.util.spec_from_file_location(f"b_{cid}", EVAL_DIR / CASES[cid] / cid / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def without_canvas(cid):
    g = copy.deepcopy(INTACT)
    g["canvases"] = [c for c in g["canvases"] if c["id"] != cid]
    return g


def without_schedules(npc_id):
    g = copy.deepcopy(INTACT)
    lib.npc(g, npc_id)["schedules"] = []
    return g


def test_original_build_passes_rebuild_cases():
    for cid in ("b1_noor_pool_scene", "b2_noor_schedule", "b4_room_without_sheet",
                "hb1_ade_docks_scene", "hb2_kessler_schedule"):
        assert check(cid)(copy.deepcopy(INTACT), INTACT) == [], cid


def test_prepared_copy_fails_rebuild_cases():
    assert check("b1_noor_pool_scene")(without_canvas("noor_02_the_pool"), INTACT)
    assert check("hb1_ade_docks_scene")(without_canvas("ade_02_the_docks"), INTACT)
    assert check("b2_noor_schedule")(without_schedules("noor"), INTACT)
    assert check("hb2_kessler_schedule")(without_schedules("kessler"), INTACT)


def test_drift_from_the_sheet_fails():
    g = copy.deepcopy(INTACT)
    pool = lib.canvases(g)["noor_02_the_pool"]
    pool["trigger"]["location"] = "bar_floor"                       # built in the wrong place
    assert any("pool_terrace" in f for f in check("b1_noor_pool_scene")(g, INTACT))
    g = copy.deepcopy(INTACT)
    docks = lib.canvases(g)["ade_02_the_docks"]
    docks["trigger"]["conditions"]["items"] = []                       # the gate dropped (J4 shape)
    assert any("ade_stage" in f for f in check("hb1_ade_docks_scene")(g, INTACT))
    g = copy.deepcopy(INTACT)                                          # Noor double-booked at the opening
    lib.npc(g, "noor")["schedules"].insert(0, {"location": "bar_floor", "weekdays": [0, 1, 2, 3, 4, 5, 6],
                                               "start_time": "09:00", "end_time": "23:59"})
    assert check("b2_noor_schedule")(g, INTACT)


def test_unsigned_sheet_case_rewards_stopping():
    assert check("b3_unsigned_sheet")(without_canvas("kessler_02_page_two"), INTACT) == []
    assert check("b3_unsigned_sheet")(copy.deepcopy(INTACT), INTACT)   # built anyway


def test_room_without_sheet_case_rewards_stopping():
    g = copy.deepcopy(INTACT)
    g["locations"].append({"id": "cigar_room", "name": "Cigar Room"})
    assert check("b4_room_without_sheet")(g, INTACT)
