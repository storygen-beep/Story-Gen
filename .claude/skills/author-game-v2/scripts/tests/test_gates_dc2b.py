"""PRD v2 DC2b · B7 · H34: `--words` reads the Want's own places and people as names the fiction
teaches, and a `role:<name>` crude-ceiling key is not a name. Nothing in games/ is read or written."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

TEXT = "She sweeps the chandlery floor every night, and Oskar watches from the counter.\n"


def _want(tmp_path, want):
    (tmp_path / "v2_state.json").write_text(json.dumps({"want": want}))
    p = tmp_path / "WANT.md"
    p.write_text(TEXT)
    return str(p)


def _listed(path):
    names, _ = gates._words_declared_names(path)
    _summary, findings = gates.own_words_report(TEXT, names, suppress=gates._SKILL_META, shown=None)
    return names, " ".join(findings).lower()


def test_want_places_and_cast_are_names(tmp_path):
    path = _want(tmp_path, {"places": [{"id": "chandlery", "name": "The Chandlery"}],
                            "cast": [{"id": "oskar", "age": 40, "keeps": "want + power"}]})
    names, listed = _listed(path)
    assert {"chandlery", "The Chandlery", "oskar"} <= set(names)
    assert "chandlery" not in listed and "oskar" not in listed


def test_without_them_the_place_is_listed(tmp_path):
    _names, listed = _listed(_want(tmp_path, {}))
    assert "chandlery" in listed


def test_a_role_key_is_not_a_name(tmp_path):
    path = _want(tmp_path, {"crude_ceiling": {"npc_oskar": ["cock"], "role:night man": ["cock"]}})
    names, _ = gates._words_declared_names(path)
    assert "npc_oskar" in names
    assert not any(str(n).startswith("role:") for n in names)
