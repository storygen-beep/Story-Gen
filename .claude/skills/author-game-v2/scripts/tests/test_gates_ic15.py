"""IC15: the spine. SP2's optional step fields leave the ladder check untouched, and the spine's
SP1–SP7 are rule definitions `--selfcheck` resolves."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
from test_gates_ws4 import game, ladder, problems, state  # noqa: E402

SKILL_DIR = os.path.dirname(os.path.dirname(HERE))


def test_sp2_step_fields_do_not_change_the_ladder_check():
    lad = ladder()
    for st in lad["steps"]:
        st.update(hint="Jo is at the shed after five.", her_line_low="Not him. Not yet.",
                  her_line_high="You want him to ask.", who_notices="nobody",
                  refusal="parked")
    assert problems(game(), state(lad)) == []


def test_the_spine_pages_are_rules_selfcheck_resolves():
    defs = gates._rule_definitions(SKILL_DIR)
    assert defs["the-spine.md"] == {f"SP{i}" for i in range(1, 8)}
    broken, _unwritten = gates._orphan_rules(SKILL_DIR, defs)
    assert not [b for b in broken if "SP" in b[2]]
