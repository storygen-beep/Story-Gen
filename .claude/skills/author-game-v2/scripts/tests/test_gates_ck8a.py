"""CK8a (PRD v2, 2026-09-30): regex fixes.

  I3  · "she can say no" counts a no written as her spoken line (a leading quote mark).
  I10 · RUNGS: "ass" alone is not anal; "fucks your mouth / face" is oral, not vaginal.
        The lint that quotes the field distribution says a re-measure is pending.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def refusal_row(*texts):
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": [{"id": "room"}],
         "canvases": [{"id": "c", "trigger": {"location": "room"},
                       "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "He asks."}],
                                  "exit_block": {"type": "choices", "choices": [
                                      {"text": t, "targetType": "location", "locationId": "room"}
                                      for t in texts]}}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == "she can say no")


# ── I3 ────────────────────────────────────────────────────────────────────────

def test_a_quoted_no_counts():
    for t in ['"No."', '“Not tonight.”', "'No, not here.'", '"No"', "‘Tell him no’"]:
        r = refusal_row(t, "Go with him")
        assert r["pass_"] is True, (t, r["headline"])
        assert r["headline"].startswith("1 refusal(s)"), (t, r["headline"])


def test_leaving_is_still_not_a_refusal():
    r = refusal_row('"Leave the shop"', "Go with him")
    assert r["pass_"] is False


# ── I10 ───────────────────────────────────────────────────────────────────────

def rungs(text):
    return gates._rungs_of(text)[1]


def test_ass_alone_is_not_anal():
    assert "anal" not in rungs("He grabs your ass.")
    assert "anal" not in rungs("Her ass is red from the chair.")


def test_fucking_a_mouth_or_face_is_oral_not_vaginal():
    assert rungs("He fucks your mouth.") == {"oral"}
    assert rungs("He fucks her face until she gags.") == {"oral"}
    assert "oral" in rungs("He face-fucks you.")


def test_an_act_on_the_ass_is_anal_not_vaginal():
    assert rungs("He fucks your ass.") == {"anal"}
    assert "anal" in rungs("He pushes it in the ass.")
    assert "anal" in rungs("He works it up your ass.")


def test_plain_fucking_is_still_vaginal():
    assert rungs("He fucks you hard.") == {"vaginal"}


def test_the_ladder_lint_says_the_field_needs_remeasuring():
    text = ("He kisses you. His cock is hard, he fucks you, your cunt is wet, and you cum "
            "on his cock while he fucks you.")
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": [{"id": "room"}],
         "canvases": [{"id": "c", "trigger": {"location": "room"},
                       "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": text}]}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    summary, _ = gates.lint_ladder(model, g2)
    assert "re-measure pending" in summary


def test_a_hyphenated_face_fuck_is_oral_only():
    assert rungs("He is face-fucking her.") == {"oral"}
    assert rungs("He face-fucks you.") == {"oral"}
