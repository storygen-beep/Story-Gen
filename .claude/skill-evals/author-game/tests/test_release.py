"""Release-stage checks: fail the untouched fixture, pass a correct preparation, fail the logged mistake."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

EVAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR / "tests"))
import lib  # noqa: E402
from test_checks import base, choice, cond, cv, say  # noqa: E402,F401

LEDGER = json.loads((EVAL_DIR / "tests" / "fixture_v2_state.json").read_text())
CASES = {"r1_patch_release": "cases", "r2_ship_without_playtest": "cases", "r3_rename_after_ship": "cases",
         "r4_new_door": "cases", "hr1_retire_flag": "cases_holdout", "hr2_jade_line_release": "cases_holdout"}


def load_check(cid):
    spec = importlib.util.spec_from_file_location(f"r_{cid}", EVAL_DIR / CASES[cid] / cid / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def edits(cid, base):
    """(good game, good ledger, bad game, bad ledger)."""
    g, gl, b, bl = copy.deepcopy(base), copy.deepcopy(LEDGER), copy.deepcopy(base), copy.deepcopy(LEDGER)
    if cid in ("r1_patch_release", "hr2_jade_line_release"):
        canvas = "hub_theo_bar" if cid == "r1_patch_release" else "hub_jade_club"
        npc_id = "npc_theo" if canvas == "hub_theo_bar" else "npc_jade"
        for x in (g, b):
            cv(x, canvas)["nodes"][0]["blocks"].append(say(npc_id, "One more thing."))
        g["project"]["version"] = "0.1.1"
        gl["release_page"]["version"] = "0.1.1"
        gl["release_page"]["reader"][canvas] = {"want": "PASS"}
        # the logged slip: content changed, version left at 0.1, nobody read the touched canvas
        bl["release_page"]["reader"].pop(canvas, None)
    elif cid == "r2_ship_without_playtest":
        bl["release_page"]["signed_by_lo"] = True
        bl["release_page"]["signed_at"] = "2026-10-03"
    elif cid == "r3_rename_after_ship":
        for loc in b["locations"]:
            if loc["id"] == "hotel_bar":
                loc["id"] = "the_hotel_bar"
        for loc in g["locations"]:
            if loc["id"] == "hotel_bar":
                loc["name"] = "The Hotel Bar (Grand)"   # display names may change freely
    elif cid == "r4_new_door":
        gate = cond({"type": "trait", "subject": "player", "trait_key": "theo_stage", "operator": "gte", "value": 2})
        for x in (g, b):
            cv(x, "hub_theo_bar")["nodes"][0]["exit_block"]["choices"].append(
                choice("Take the key card.", conditions=gate, show_when_locked=True))
        gl["release_page"]["door"] = {"canvas": "hub_theo_bar", "choice": "Take the key card."}
        # the logged slip: the door is written once in one place and left stale in the other
        bl["release_page"]["door"] = {"canvas": "hub_theo_bar", "choice": "Take the key card."}
        bl["board"]["door"] = {"canvas": "martin_03_jacket_downstairs", "choice": "Take the jacket off."}
    elif cid == "hr1_retire_flag":
        def rename(o):
            if isinstance(o, dict):
                for k in ("flag", "flag_key"):
                    if o.get(k) == "theo_knows_friday":
                        o[k] = "knows_about_rent"
                for v in o.values():
                    rename(v)
            elif isinstance(o, list):
                for v in o:
                    rename(v)
        rename(b)
    return g, gl, b, bl


UNTOUCHED_PASSES = {"r2_ship_without_playtest", "r3_rename_after_ship", "hr1_retire_flag"}


@pytest.mark.parametrize("cid", sorted(CASES))
def test_untouched_fixture(cid, base):
    """Cases that test 'do not do the harmful thing' pass when nothing is done; the rest must fail."""
    result = load_check(cid)(copy.deepcopy(base), base, copy.deepcopy(LEDGER))
    assert (result == []) == (cid in UNTOUCHED_PASSES), result


@pytest.mark.parametrize("cid", sorted(CASES))
def test_good_preparation_passes(cid, base):
    g, gl, _, _ = edits(cid, base)
    assert load_check(cid)(g, base, gl) == []


@pytest.mark.parametrize("cid", sorted(CASES))
def test_logged_mistake_fails(cid, base):
    _, _, b, bl = edits(cid, base)
    assert load_check(cid)(b, base, bl)
