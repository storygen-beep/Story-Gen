"""Per-state refusals on a locked location — `blocked_messages`.

A location has one `blocked_message`, and a door shut for two different reasons can
only say one of them. Vesper 0.2.4 hit it: Kess's berth was already locked until the
salvage, with its own line, and 0.2.4 also shuts it while Wren is in Vega's body. One
string would lie in one of the two states.

`blocked_messages = [{conditions, text}]` is a first-match list in front of the
`blocked_message` fallback, the same shape `description_variants` already uses. The
nav card (setup.navDestBlockedReason) and the blocked passage read the same list in
the same order, so they can never disagree.

Like description_variants, an entry must not FAIL OPEN: triggerConditionsSatisfied
returns TRUE for conditions without `version`, so such an entry would always match
and the real reason would never show. The importer refuses it.

    pytest apps/game_generation/tests/test_location_blocked_messages.py -q
"""
import pytest

from apps.projects.services.template_import import _parse_blocked_messages

IN_VEGA = {"version": "1.0", "logic": "AND",
           "items": [{"type": "flag", "subject": "player", "flag_key": "in_vega", "operator": "is_true"}]}


def test_absent_means_empty():
    assert _parse_blocked_messages({"id": "berth"}) == []


def test_a_good_entry_is_kept_as_written():
    got = _parse_blocked_messages({"id": "berth", "blocked_messages": [{"conditions": IN_VEGA, "text": "Not in this body."}]})
    assert got == [{"conditions": IN_VEGA, "text": "Not in this body."}]


@pytest.mark.parametrize("entry", [
    {"conditions": {"items": IN_VEGA["items"]}, "text": "x"},          # no version: would fail OPEN
    {"conditions": {"version": "1.0", "items": []}, "text": "x"},      # nothing to match on
    {"conditions": IN_VEGA, "text": "   "},                             # no text
    {"conditions": IN_VEGA},
    "Not in this body.",
])
def test_a_bad_entry_is_refused(entry):
    with pytest.raises((TypeError, ValueError)):
        _parse_blocked_messages({"id": "berth", "blocked_messages": [entry]})


def test_the_generator_reads_the_list_before_the_fallback():
    """The JS reason helper must try blocked_messages before blocked_message, or the
    nav card would show the old line while the passage showed the new one."""
    import inspect
    from apps.game_generation.twee_comprehensive.generators import v2
    src = inspect.getsource(v2)
    fn = src[src.index("setup.navDestBlockedReason = function"):]
    fn = fn[:fn.index("\n}};")]
    assert fn.index("blocked_messages") < fn.index("if (loc.blocked_message)")
