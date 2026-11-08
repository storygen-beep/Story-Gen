"""A garment's `description`: one line the shop stand and Change Clothes show (first_term
DECISIONS 198, the gym clothes). It tells her what the piece does and the risk she takes in
it before she pays ("Rides up when you bend over", as Course of Temptation's shop does).
Written into the game only when authored.

    pytest apps/game_generation/tests/test_garment_description.py -q
"""
import pytest

from apps.projects.services.template_import import parse_toml

from .headless import build, needs_browser, open_game
from .test_clothes_room import _room_raw, _room_text, _twee

DESC = "Rides up when you bend over."


def _with_desc(text):
    # The room fixture's mini skirt gets the line; the heels stay without one.
    return text.replace('id    = "mini"\n', f'id    = "mini"\ndescription = "{DESC}"\n', 1)


def test_description_reaches_the_game_only_when_authored(tmp_path):
    assert '"description": "' + DESC not in _twee(_room_raw(tmp_path))
    src = tmp_path / "desc.toml"
    src.write_text(_with_desc(_room_text()), encoding="utf-8")
    assert _twee(parse_toml(str(src))).count(f'"description": "{DESC}"') == 1


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    d = tmp_path_factory.mktemp("desc")
    src = d / "desc.toml"
    src.write_text(_with_desc(_room_text()), encoding="utf-8")
    return build(src, d / "out")


@needs_browser
def test_the_stand_and_the_rail_show_the_line(html):
    with open_game(html) as g:
        g.play("ShopPage")
        g.js("() => document.querySelector('.cr-peg[data-pick=\"mini\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.js("() => document.querySelector('.cr-stand-desc').textContent") == DESC
        # A piece without one draws no empty line.
        g.js("() => document.querySelector('.cr-peg[data-pick=\"heels\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.js("() => document.querySelectorAll('.cr-stand-desc').length") == 0
        # Worn, Change Clothes says it under the slot's rail.
        g.js("() => { SugarCube.setup.addToWardrobe('mini'); SugarCube.setup.equipItem('mini'); SugarCube.setup.wardrobeSel = 'bottom'; }")
        g.play("WardrobePage")
        assert g.js("() => document.querySelector('.cr-desc').textContent") == "Mini skirt: " + DESC
        assert g.errors == []
