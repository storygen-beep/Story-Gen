"""L2 (PRD v2 phase 4 · I28, 2026-09-30): two `playtest.py` misreads, both verified live first.

  - "the guidance page resolves cards" read the cards as soon as `current_location` was set —
    the opening's FIRST node sets it, so the cards were read before the opening's exit set
    its flags (one game: 0 of 19, and 8 once the opening had exited). The cards are now read
    once the funnel lands on a `Location_` passage.
  - "a random event actually fires" swept six hours of a Monday only; an ambient scheduled
    for other days never came up. It now sweeps all seven days.

Each fixture is a real build (package_from_toml into tmp), played headless. Nothing in
games/ is read or written.
"""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

HEAD = '''
schema_version = "1.0"

[project]
id              = "l2_fx"
title           = "L2 Fixture"
description     = "An opening that sets its flag on the exit, a card behind it, and a Wednesday ambient."
starting_canvas = "opening"
quests_engine   = "v2"
version         = "0.1"

[time]
starting_hour = 9
starting_day  = "Monday"
starting_week = 1

[player]
id   = "player"
name = "Sam"

[player.core_traits]
money = 10

[[locations]]
id               = "yard"
name             = "Yard"
description      = "The yard behind the house."
navigation_order = ["shed"]

[[locations]]
id          = "shed"
name        = "Shed"
description = "The shed at the end of the yard."
entry_from  = "yard"

[[quest_cards]]
text     = "Find out what is in the shed."
priority = 10
when     = [ { flag = "{card_flag}", subject = "player", op = "is_true" } ]
goals    = [ { flag = "shed_seen", subject = "player", op = "is_true", label = "Look in the shed" } ]

[[canvases]]
id   = "opening"
name = "Opening"
[canvases.trigger]
location      = "yard"
is_repeatable = false
is_active     = true
priority      = 100
[[canvases.nodes]]
id     = "base"
name   = "Morning"
blocks = [ { type = "paragraph", content = "The yard is wet. The shed door hangs open." } ]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text       = "Walk over"
targetType = "node"
nodeId     = "two"

[[canvases.nodes]]
id     = "two"
name   = "The door"
blocks = [ { type = "paragraph", content = "Nobody is inside. It smells of oil." } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId  = "yard"
flagEffects = [ { targetType = "player", flag = "opening_done", op = "set" } ]

[[canvases]]
id   = "amb_wednesday"
name = "Wednesday"
[canvases.trigger]
location      = "shed"
is_repeatable = true
trigger_mode  = "random"
chance        = 1.0
priority      = 2
is_active     = true
{amb_conditions}
[[canvases.trigger.schedules]]
weekdays   = [2]
start_time = "11:00"
end_time   = "13:00"
[[canvases.nodes]]
id     = "base"
name   = "Rain"
blocks = [ { type = "paragraph", content = "Rain on the shed roof, loud as gravel." } ]
{extra}
'''

# The bad fixture's flag has a real setter (the build validator demands one), behind a gate the
# play-test never meets: 999 money.
LATER = '''
[[canvases]]
id   = "later"
name = "Later"
[canvases.trigger]
location      = "shed"
is_repeatable = false
is_active     = true
conditions    = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "money", operator = "gte", value = 999 } ] }
[[canvases.nodes]]
id     = "base"
name   = "Later"
blocks = [ { type = "paragraph", content = "The key is under the tin." } ]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text        = "Take the key"
targetType  = "location"
locationId  = "shed"
flagEffects = [ { targetType = "player", flag = "never_set", op = "set" } ]
'''
# On a CHOICE, not a `location` exit's config: check 5 plays every canvas's first node, and a
# location exit fires its effects on render, which would set the flag behind the play-test's back.


def _build(tmp_path_factory, name, card_flag, amb_conditions, extra=""):
    pytest.importorskip("playwright")
    d = tmp_path_factory.mktemp(name)
    src = d / "game.toml"
    src.write_text(HEAD.replace("{card_flag}", card_flag).replace("{amb_conditions}", amb_conditions)
                   .replace("{extra}", extra))
    res = subprocess.run([os.path.join(REPO, "venv", "bin", "python"), "manage.py",
                          "package_from_toml", "--file", str(src), "--output", str(d / "out"),
                          "--gen-version", "v2"], cwd=REPO, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout[-2000:] + res.stderr[-2000:]
    return str(d / "out" / "index.html"), str(src)


def _rows(build):
    import playtest
    html, src = build
    with playtest.open_game(html) as (page, errors):
        rep = playtest.universal(page, errors, playtest._load(src), playtest.Report())
    return {name: (status, detail) for status, name, detail in rep.rows}


@pytest.fixture(scope="module")
def good(tmp_path_factory):
    return _rows(_build(tmp_path_factory, "l2_good", "opening_done", ""))


@pytest.fixture(scope="module")
def bad(tmp_path_factory):
    never = ('conditions = { version = "1.0", logic = "AND", items = [ '
             '{ type = "flag", subject = "player", flag_key = "never_set", operator = "is_true" } ] }')
    return _rows(_build(tmp_path_factory, "l2_bad", "never_set", never, LATER))


def test_cards_are_read_after_the_opening_exits(good):
    status, detail = good["the guidance page resolves cards"]
    assert status == "PASS" and detail.startswith("1 of 1 declared cards resolve once the opening ends")


def test_an_ambient_off_monday_is_found(good):
    status, detail = good["a random event actually fires"]
    assert status == "PASS" and "each of the 7 days" in detail, detail


def test_a_card_nothing_opens_still_fails(bad):
    assert bad["the guidance page resolves cards"][0] == "FAIL"


def test_an_ambient_that_can_never_open_still_fails(bad):
    assert bad["a random event actually fires"][0] == "FAIL"
