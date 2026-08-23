"""Regression tests for `[[npcs]] tags` — the cast card's tag line.

Section G measured the field's best cast page (friends-of-mine's Characterpedia:
15 people, each with exactly four interests) and found we had no field for it.
`tags` is that field. Three things are locked here:

1.  **It parses and it is capped.** The cap is the doctrine — a fifth entry turns
    the line into a stat block, which is what the deliberately trivial fourth slot
    exists to prevent.
2.  **It reaches a packaged game through the NO-DB path.** This is the one that
    bit during implementation: `ai_behavior_config` is written in *two* places —
    `template_import.create_project_from_template` (the `--use-db` path) and
    `game_graph.build_game_graph` (the default). A field added only to the first
    reaches the database and never reaches a build, and the symptom is a silently
    empty `setup.npc_tags` with no error anywhere.
3.  **It is inert when unused.** A game that declares no tags must be unaffected.
"""

import pytest

from apps.projects.services.template_import import (
    NPC_TAGS_MAX,
    TemplateNPC,
    normalize,
)


def _minimal_game(npc_extra=None):
    """The smallest `normalize()` input that yields one NPC."""
    npc = {"id": "npc_boyd", "name": "Boyd"}
    npc.update(npc_extra or {})
    return {
        "project": {"name": "tagtest"},
        "player": {"name": "Cass"},
        "npcs": [npc],
        "locations": [{"id": "yard", "name": "The yard"}],
        "canvases": [],
    }


# ── 1. parse + cap ────────────────────────────────────────────────────────────

def test_tags_parse_into_the_npc():
    t = normalize(_minimal_game({"tags": ["The book", "The scale"]}))
    assert t.npcs[0].tags == ["The book", "The scale"]


def test_tags_default_to_empty():
    t = normalize(_minimal_game())
    assert t.npcs[0].tags == []


def test_tags_are_stripped():
    t = normalize(_minimal_game({"tags": ["  The book  "]}))
    assert t.npcs[0].tags == ["The book"]


def test_tags_at_the_cap_are_accepted():
    four = ["The book", "The scale", "Saturday", "Black coffee"]
    assert len(four) == NPC_TAGS_MAX
    t = normalize(_minimal_game({"tags": four}))
    assert t.npcs[0].tags == four


def test_tags_over_the_cap_are_rejected():
    over = ["One", "Two", "Three", "Four", "Five"]
    assert len(over) > NPC_TAGS_MAX
    with pytest.raises(ValueError, match=r"tags has 5 entries, max 4"):
        normalize(_minimal_game({"tags": over}))


def test_tags_must_be_a_list():
    with pytest.raises(TypeError, match=r"tags must be a list"):
        normalize(_minimal_game({"tags": "The book"}))


def test_tag_entries_must_be_strings():
    with pytest.raises(TypeError, match=r"tags\[1\] must be a string"):
        normalize(_minimal_game({"tags": ["The book", 7]}))


def test_empty_tag_entries_are_rejected():
    with pytest.raises(ValueError, match=r"tags\[0\] is empty"):
        normalize(_minimal_game({"tags": ["   "]}))


# ── 2. the no-DB path carries it ──────────────────────────────────────────────
#
# The default build never touches the database, so this is the path that matters.

def test_no_db_path_writes_tags_into_ai_behavior_config():
    from apps.projects.services.game_graph import build_game_graph

    t = normalize(_minimal_game({"tags": ["The book", "The scale"]}))
    graph = build_game_graph(t)
    cfg = graph.npcs[0].ai_behavior_config
    assert cfg["tags"] == ["The book", "The scale"], (
        "tags did not survive the no-DB path — check that game_graph.py writes "
        "them alongside arc_stages, not only template_import.py"
    )


def test_no_db_path_omits_the_key_when_unused():
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(_minimal_game()))
    assert "tags" not in graph.npcs[0].ai_behavior_config


# ── 3. the dataclass default is not shared ────────────────────────────────────

def test_tags_default_is_per_instance():
    a, b = TemplateNPC(id="a", name="A"), TemplateNPC(id="b", name="B")
    a.tags.append("mutated")
    assert b.tags == []
