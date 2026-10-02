"""E1b (World and Systems PRD): the clothing warning names the player, not "Emma".

`setup.validateClothing` hard-coded "Emma" in its three warnings, so every clothing
game told its player that a stranger needed to get dressed. It now reads
`$player.name` (customization included), falling back to "Player" like the hints do.

The function is executed in node against a real build of the checked-in fixture with
clothing switched on; a source grep alone cannot tell which name reaches the text.

    pytest apps/game_generation/tests/test_clothing_warning_name.py -q
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
V2 = Path("apps/game_generation/twee_comprehensive/generators/v2.py")

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def _twee_with_clothing():
    data = parse_toml(FIXTURE)
    data.setdefault("settings", {})["clothing_enabled"] = True
    graph = build_game_graph(normalize(data))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _fn_source(twee, head):
    i = twee.index(head)
    j = twee.index("{", i)
    depth = 0
    for k in range(j, len(twee)):
        depth += {"{": 1, "}": -1}.get(twee[k], 0)
        if depth == 0:
            return twee[i : k + 1]
    raise AssertionError(head)


def _run(twee, player, tmp_path):
    program = (
        "var setup = {}; var State = { variables: " + json.dumps(
            {"player": player, "flags": {}}) + " };\n"
        + _fn_source(twee, "setup.validateClothing = function()") + ";\n"
        + "setup.clothingRequirements = { body_coverage: true, always_required: ['shoes'],"
        + " conditional: { bra: { until_flag: 'free' } } };\n"
        + "console.log(JSON.stringify(setup.validateClothing()));\n"
    )
    script = tmp_path / "clothing.js"
    script.write_text(program, encoding="utf-8")
    out = subprocess.run(["node", str(script)], capture_output=True, text=True, check=False)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_no_hard_coded_name_is_left_in_the_engine():
    assert "Emma" not in V2.read_text(encoding="utf-8")


@needs_node
def test_every_warning_names_the_player(tmp_path):
    issues = _run(_twee_with_clothing(), {"name": "Mara", "equipped": {}}, tmp_path)
    assert issues == [
        "Mara needs to be wearing a top and bottom, or a dress.",
        "Mara needs to put on shoes.",
        "Mara needs bra.",
    ]


@needs_node
def test_a_player_with_no_name_falls_back_to_player(tmp_path):
    issues = _run(_twee_with_clothing(), {"equipped": {}}, tmp_path)
    assert all(i.startswith("Player needs") for i in issues), issues
