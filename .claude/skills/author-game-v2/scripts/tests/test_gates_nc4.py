"""NC4 (PRD v2 phase 4 · D3a · D4 · J5, 2026-09-30): one name per trait.

Every trait an effect changes has a `[[traits.labels]]` label (the toast names them all,
D1b), and a sidebar item's own `label`, when set, is that label.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(labels=None, sidebar=None):
    return {"traits": {"labels": labels if labels is not None else [
                {"key": "nerve", "label": "Nerve", "in_dump": False}]},
            "sidebar_items": sidebar or [],
            "canvases": [{"id": "c", "nodes": [{"id": "n", "exit_block": {"config": {
                "effects": [{"trait": "nerve", "op": "add", "value": 2}]}}}]}]}


def test_a_labelled_trait_and_a_matching_sidebar_pass():
    ok, _h, detail, _n = gates._one_name_per_trait(
        game(sidebar=[{"type": "trait_bar", "trait": "nerve", "label": "Nerve"}]))
    assert ok is True, detail


def test_a_sidebar_item_with_no_label_of_its_own_passes():
    assert gates._one_name_per_trait(game(sidebar=[{"type": "trait_words", "trait": "nerve"}]))[0]


def test_nothing_moved_and_no_sidebar_is_na():
    assert gates._one_name_per_trait({"canvases": []})[0] is None


def test_a_moved_trait_with_no_label_fails():
    ok, _h, detail, _n = gates._one_name_per_trait(game(labels=[{"key": "nerve", "hidden": True}]))
    assert ok is False and detail[0].startswith("`nerve` is changed by an effect and has no")


def test_a_sidebar_label_that_differs_fails():
    ok, _h, detail, _n = gates._one_name_per_trait(
        game(sidebar=[{"type": "trait_bar", "trait": "nerve", "label": "Courage"}]))
    assert ok is False and '"Courage"; its label is "Nerve"' in detail[0]


# ── follow-ups: every list that toasts ───────────────────────────────────────

def test_costs_substitution_jobs_and_phone_counters_are_moved_traits():
    g = {"traits": {"labels": []},
         "canvases": [{"id": "c", "trigger": {"pre_substitution_effects": [
                          {"trait": "nerve", "op": "add", "value": 1}]},
                       "nodes": [{"id": "n", "exit_block": {"choices": [
                           {"text": "Buy", "costs": [{"trait": "energy", "value": 5}]}]}}]}],
         "fast_jobs": [{"id": "j", "income": 10}],
         "phone": {"apps": [{"id": "feed", "post_actions": [{"label": "Post", "counter_trait": "posts"}]}]}}
    ok, _h, detail, _n = gates._one_name_per_trait(g)
    named = {d.split("`")[1] for d in detail}
    assert ok is False and named == {"nerve", "energy", "money", "posts"}


def test_the_message_names_the_tidied_key():
    g = {"traits": {"labels": []}, "canvases": [{"id": "c", "nodes": [{"id": "n", "exit_block": {
        "config": {"effects": [{"trait": "kessler_stage", "op": "add", "value": 1}]}}}]}]}
    assert '("Kessler stage")' in gates._one_name_per_trait(g)[2][0]
