"""No-DB build guards.

After the UUID→slug migration the build is fully deterministic (the generator
mints no UUIDs of its own; every id is a constant slug, and the IFID is a stable
uuid5 of the project slug). So the invariants worth guarding are:

1. **Reproducibility** — two independent builds of the same TOML are byte-identical
   (no random churn). This is what makes cross-release `index.html` snapshots
   diffable and NPC saves survive rebuilds ($npcs is keyed by the stable slug ids).
2. **Zero database interaction** — generating from the in-memory graph touches the
   DB zero times.

(The Stage-1 DB-vs-graph equivalence test was retired here: once ids are slugs the
DB path's uuid4 ids and the graph path's slug ids intentionally differ.)
"""
import os

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml
from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)

# Self-contained checked-in fixture (no media needed).
FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
# The real v2 game — checked only when its merged TOML + media are present.
VESPER = "games/vesper/toml_phases/7_final_game.toml"
VESPER_OPTS = {"video_folder": "games/vesper/videos", "video_path": "./videos"}


def _twee_graph(toml_path: str, options: dict) -> str:
    graph = build_game_graph(normalize(parse_toml(toml_path)))
    return TweeComprehensiveGeneratorV2().generate(
        graph.project, dict(options), graph=graph
    )


def test_nodb_build_is_reproducible():
    # Two independent builds must be byte-identical — no UUID/random churn.
    assert _twee_graph(FIXTURE, {}) == _twee_graph(FIXTURE, {})


@pytest.mark.skipif(
    not (os.path.exists(VESPER) and os.path.isdir("games/vesper/videos")),
    reason="Vesper merged TOML / media not present",
)
def test_nodb_build_is_reproducible_vesper():
    assert _twee_graph(VESPER, VESPER_OPTS) == _twee_graph(VESPER, VESPER_OPTS)


@pytest.mark.django_db
def test_nodb_generate_makes_zero_queries():
    graph = build_game_graph(normalize(parse_toml(FIXTURE)))
    with CaptureQueriesContext(connection) as ctx:
        TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    assert len(ctx.captured_queries) == 0, [
        q["sql"][:100] for q in ctx.captured_queries
    ]
