"""`[ui] clothes_layout = "room"` (first_term DECISIONS 194).

Change Clothes and the clothes shop drawn as a dressing room. The wardrobe shows her
portrait beside a column of what she wears, one status line (her clothing state and
whether the `[ui] clothes_door` location's dress code lets her out), and a rail of what
she owns for the selected slot. The shop puts one piece on a stand (Buy, Buy and wear, or
the reason she can't) above a rack of what she does not own yet, with slot tabs. Without
the key both pages are the table pages, unchanged. A portrait rule's `when.wearing`
matches a garment in any slot.

    pytest apps/game_generation/tests/test_clothes_room.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"

# What the room needs on top of the fixture: a shop, priced garments (one she can't
# afford, one behind a trait, one behind a flag with locked_text), a door with a rule
# that names a garment type, a portrait with a `wearing` row, and the two [ui] keys.
ROOM_EXTRA = """
[[clothing]]
id    = "mini"
name  = "Mini skirt"
slot  = "bottom"
price = 5
type  = "mini"

[[clothing]]
id    = "heels"
name  = "Heels"
slot  = "shoes"
price = 60

[[clothing]]
id         = "lace"
name       = "Lace bra"
slot       = "bra"
price      = 5
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "charm", operator = "gte", value = 20 } ] }

[[clothing]]
id          = "tee"
name        = "Tee"
slot        = "top"
price       = 5
locked_text = "Held at the cleaners"
conditions  = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "held", operator = "is_false" } ] }

[[locations]]
id             = "loc_street"
name           = "Street"
description    = "The street."
entry_from     = "loc_home"
clothing_rules = [
  { conditions = { version = "1.0", logic = "AND", items = [ { type = "worn_type", operator = "eq", value = "mini" } ] }, slots_required = ["legwear"], message = "Not in the mini." },
  { slots_required = ["top", "bottom"], message = "Dress code." } ]

[player_portrait]
enabled       = true
default_image = "p/default.jpg"

[[player_portrait.outfits]]
image = "p/mini.jpg"
when  = { wearing = "mini" }

[ui]
clothes_layout = "room"
clothes_door   = "loc_street"
"""


def _room_text():
    with open(FIXTURE, encoding="utf-8") as fh:
        text = fh.read()
    text = text.replace("saved_outfits              = true\n",
                        'saved_outfits              = true\nshop_location              = "loc_gym"\n')
    text = text.replace('flag_keys   = ["started", "card_ok"]', 'flag_keys   = ["started", "card_ok", "held"]')
    return text + ROOM_EXTRA


def _room_raw(tmp_path):
    src = tmp_path / "room.toml"
    src.write_text(_room_text(), encoding="utf-8")
    return parse_toml(str(src))


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _passage(twee, name):
    return next(p for p in twee.split("\n:: ") if p.startswith(name + "\n") or p.startswith(name + " "))


# ── 1. the key, its checks, and what it leaves alone ─────────────────────────


def test_without_the_key_the_pages_are_the_table_pages():
    twee = _twee(parse_toml(FIXTURE))
    assert "setup.renderWardrobePage()" in _passage(twee, "WardrobePage")
    assert "renderWardrobeRoom" not in twee and "renderShopRoom" not in twee
    assert "clothes_door" not in twee


def test_the_room_replaces_both_pages(tmp_path):
    raw = _room_raw(tmp_path)
    assert validate(normalize(raw)) == []
    twee = _twee(raw)
    wardrobe = _passage(twee, "WardrobePage")
    shop = _passage(twee, "ShopPage")
    assert "setup.renderWardrobeRoom()" in wardrobe and "renderWardrobePage" not in wardrobe
    assert "setup.renderShopRoom()" in shop and "renderShopPage" not in shop
    # Back sits at the top, as on People and Quests; the wardrobe keeps its dress check.
    assert wardrobe.index("Back") < wardrobe.index("<h2>") and shop.index("Back") < shop.index("<h2>")
    assert "setup.checkLocationClothing(dest)" in wardrobe
    assert 'setup.clothes_door = "loc_street";' in twee
    assert twee.count("\n:: WardrobePage") == 1 and twee.count("\n:: ShopPage") == 1


@pytest.mark.parametrize("ui, needle", [
    ('clothes_layout = "rooms"', "clothes_layout must be one of"),
    ('clothes_layout = "room"\nclothes_door = "loc_nowhere"', "no location with id 'loc_nowhere'"),
    ('clothes_layout = "room"\nclothes_door = "loc_home"', "has no clothing_rules"),
    ('clothes_door = "loc_street"', 'read only by clothes_layout = "room"'),
])
def test_bad_keys_are_errors(tmp_path, ui, needle):
    text = _room_text().replace('clothes_layout = "room"\nclothes_door   = "loc_street"\n', ui + "\n")
    src = tmp_path / "bad.toml"
    src.write_text(text, encoding="utf-8")
    errors = validate(normalize(parse_toml(str(src))))
    assert any(needle in e for e in errors), errors


def test_room_needs_clothing(tmp_path):
    text = _room_text().replace("clothing_enabled           = true", "clothing_enabled           = false")
    src = tmp_path / "noclothes.toml"
    src.write_text(text, encoding="utf-8")
    errors = validate(normalize(parse_toml(str(src))))
    assert any('requires clothing to be enabled' in e for e in errors), errors


def test_locked_text_reaches_the_game_only_when_authored(tmp_path):
    twee = _twee(_room_raw(tmp_path))
    assert twee.count('"locked_text": "Held at the cleaners"') == 1


# ── 2. the room, played ───────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    d = tmp_path_factory.mktemp("room")
    src = d / "room.toml"
    src.write_text(_room_text(), encoding="utf-8")
    return build(src, d / "out")


def _wardrobe(g, slot=None):
    if slot:
        g.js("(s) => { SugarCube.setup.wardrobeSel = s; }", slot)
    g.play("WardrobePage")


@needs_browser
def test_the_wardrobe_shows_what_she_wears_and_the_door(html):
    with open_game(html) as g:
        g.js("() => SugarCube.setup.addToWardrobe('mini')")
        _wardrobe(g, "bottom")
        slots = g.js("() => [...document.querySelectorAll('.cr-slot')].map(e => e.dataset.slot + ':' + e.querySelector('.cr-v').textContent)")
        # Dress is not drawn: she owns none and wears none.
        assert slots == ["top:Blouse", "bottom:Skirt", "bra:Bra"]
        assert g.js("() => document.querySelector('.cr-door').textContent") == "✓ Fine to go out."
        assert g.js("() => document.querySelector('.cr-chip').textContent") == "No panties"
        # The fixture ships no media: the frame falls back to her name, and the engine's pick
        # is read from getPlayerPortrait, the call the page draws from.
        assert g.js("() => document.querySelector('.cr-portrait .cr-picname').textContent") == "Mara"
        assert g.js("() => SugarCube.setup.getPlayerPortrait()").endswith("p/default.jpg")
        # Tap the mini on the rail: she wears it, the door names the rule for it, and the
        # portrait's `wearing` row picks it up although the blouse is the dominant garment.
        g.js("() => document.querySelector('.cr-hang[data-wear=\"mini\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.sv("player.equipped.bottom") == "mini"
        assert g.js("() => document.querySelector('.cr-door').textContent") == "Not in the mini."
        assert g.js("() => SugarCube.setup.getPlayerPortrait()").endswith("p/mini.jpg")
        assert g.errors == []


@needs_browser
def test_a_dress_swaps_and_nothing_takes_off(html):
    with open_game(html) as g:
        g.js("() => SugarCube.setup.addToWardrobe('slip')")
        _wardrobe(g, "dress")
        assert g.js("() => document.querySelector('.cr-rail-hint').textContent") == "Takes off your top and bottom"
        g.js("() => document.querySelector('.cr-hang[data-wear=\"slip\"]').click()")
        g.page.wait_for_timeout(150)
        assert [g.sv("player.equipped.dress"), g.sv("player.equipped.top"), g.sv("player.equipped.bottom")] == ["slip", None, None]
        under = g.js("() => [...document.querySelectorAll('.cr-slot .cr-v')].map(e => e.textContent)")
        assert under[:2] == ["Under the dress", "Under the dress"]
        g.js("() => document.querySelector('.cr-hang[data-off=\"dress\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.sv("player.equipped.dress") is None
        assert g.errors == []


@needs_browser
def test_a_locked_garment_says_why_and_stays_off(html):
    with open_game(html) as g:
        g.js("() => { SugarCube.setup.addToWardrobe('tee'); SugarCube.setup.addToWardrobe('lace'); SugarCube.State.variables.flags.held = true; }")
        _wardrobe(g, "top")
        assert "Held at the cleaners" in g.js("() => document.querySelector('.cr-hang.is-locked').textContent")
        g.js("() => document.querySelector('.cr-hang.is-locked').click()")
        g.page.wait_for_timeout(150)
        assert g.sv("player.equipped.top") == "blouse"
        # A trait gate is named in numbers before any locked_text.
        _wardrobe(g, "bra")
        assert "Needs Charm 20+ (you have 10)" in g.js("() => document.querySelector('.cr-hang.is-locked').textContent")
        assert g.errors == []


@needs_browser
def test_the_shop_sells_only_what_she_can_still_buy(html):
    with open_game(html) as g:
        g.play("ShopPage")
        rack = g.js("() => [...document.querySelectorAll('.cr-peg')].map(e => e.dataset.pick + (e.classList.contains('is-cant') ? '!' : ''))")
        assert rack == ["mini", "heels!", "lace!", "tee"]
        tabs = g.js("() => [...document.querySelectorAll('.cr-tab')].map(e => e.textContent)")
        assert tabs == ["All", "Top", "Bottom", "Bra", "Shoes"]
        # The stand: the door's rule for the mini, and Buy and wear.
        assert "Not in the mini." in g.js("() => document.querySelector('.cr-stand').textContent")
        g.js("() => document.querySelector('.cr-buy-wear').click()")
        g.page.wait_for_timeout(150)
        assert g.sv("player.equipped.bottom") == "mini" and g.sv("player.core_traits.money") == 35
        assert g.js("() => document.querySelector('.cr-toast').textContent") == "Bought the mini skirt and put it on. $35 left."
        assert "mini" not in g.js("() => [...document.querySelectorAll('.cr-peg')].map(e => e.dataset.pick)")
        # What she can't buy says why, in place of the buttons.
        g.js("() => document.querySelector('.cr-peg[data-pick=\"heels\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.js("() => document.querySelector('.cr-stand-why').textContent") == "Need $25 more"
        assert g.js("() => document.querySelectorAll('.cr-stand .cr-buy').length") == 0
        g.js("() => document.querySelector('.cr-peg[data-pick=\"lace\"]').click()")
        g.page.wait_for_timeout(150)
        assert g.js("() => document.querySelector('.cr-stand-why').textContent") == "Needs Charm 20+ (you have 10)"
        # Everything bought: the rack says so.
        g.js("""() => { const v = SugarCube.State.variables; v.player.core_traits.money = 500;
                v.player.core_traits.charm = 20; ['heels', 'lace', 'tee'].forEach(i => SugarCube.setup.buyItem(i)); }""")
        g.play("ShopPage")
        assert g.js("() => document.querySelector('.cr-empty-note').textContent") == "You have bought everything here."
        assert g.errors == []
