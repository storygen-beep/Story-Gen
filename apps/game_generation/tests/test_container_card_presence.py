"""A building's card shows who is in its rooms (first_term playtest 2026-11-10).

The map card's presence badges and NEW mark read one location id. A container (Home,
Zoe's Flat) holds nobody itself: its people stand in the rooms under it, so the card from
outside was blank on Zoe's party night while she and Jake were in her living room. A
container's card now reads the container and every room under it, by parent_location, at
any depth. A plain room's card keeps the single-id calls, so its output is unchanged.
Conditions, doors and the in-room portrait gate keep exact ids.

    pytest apps/game_generation/tests/test_container_card_presence.py -q
"""
import re

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

from .headless import build, needs_browser, open_game

# loc_mall is a container; loc_mall_food and loc_mall_shop are its rooms.
FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"


def _graph():
    return build_game_graph(normalize(parse_toml(FIXTURE)))


def _gen_and_twee():
    graph = _graph()
    gen = TweeComprehensiveGeneratorV2()
    return gen, gen.generate(graph.project, {}, graph=graph)


def _loc(gen, slug):
    return next(l for l in gen.locations if ((getattr(l, "properties", None) or {}).get("slug") == slug))


def test_a_container_reads_itself_and_every_room_under_it():
    gen, _ = _gen_and_twee()
    ids = gen._card_loc_ids(_loc(gen, "loc_mall"))
    want = {str(_loc(gen, s).id) for s in ("loc_mall", "loc_mall_food", "loc_mall_shop")}
    assert set(ids) == want and ids[0] == str(_loc(gen, "loc_mall").id)


def test_a_plain_room_keeps_the_single_id_calls():
    gen, _ = _gen_and_twee()
    loc = _loc(gen, "loc_bar")
    new_call, npcs_call = gen._card_presence_calls(loc)
    assert new_call == f'setup.locationHasNewCanvases("{loc.id}")'
    assert npcs_call == f'setup.getNpcsPresentAtLocation("{loc.id}")'


def test_the_container_card_uses_the_many_id_calls():
    gen, twee = _gen_and_twee()
    food = str(_loc(gen, "loc_mall_food").id)
    calls = re.findall(r"getNpcsPresentAtLocations\(\[([^\]]*)\]\)", twee)
    assert calls and any(f"'{food}'" in c for c in calls), calls
    assert "locationsHaveNewCanvases([" in twee


@needs_browser
def test_the_helper_finds_someone_in_a_room_under_the_card(tmp_path):
    html = build(FIXTURE, tmp_path / "out")
    gen, _ = _gen_and_twee()
    ids = gen._card_loc_ids(_loc(gen, "loc_mall"))
    with open_game(html) as g:
        # Put an NPC in the food court by stubbing the schedule lookup the helper reads.
        found = g.js("""(ids) => {
            const s = SugarCube.setup, slug = Object.keys(s.npc_slug_map || {})[0];
            const real = s.getNpcLocation;
            s.getNpcLocation = (n) => (n === slug ? {location: ids[1]} : null);
            s.npcSchedules = Object.assign({}, s.npcSchedules, {[slug]: [{}]});
            const many = s.getNpcsPresentAtLocations(ids).length, one = s.getNpcsPresentAtLocation(ids[0]).length;
            s.getNpcLocation = real;
            return [many, one];
        }""", ids)
        assert found == [1, 0], found
        assert g.errors == []
