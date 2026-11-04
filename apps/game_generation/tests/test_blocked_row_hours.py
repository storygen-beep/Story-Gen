"""H67 — a greyed `show_when_blocked` row shows its hours only when the clock shut it.

The row's `cooldown_message` says when it opens. That is true only if waiting can open it. A row
shut by a meter or a flag used to grey out with its hours anyway ("Party nights, 10 PM-2 AM" on a
row that needs Corruption 60), which tells the player to come back at a time that will not help.
`setup.onlyTheClockShut` asks whether the row passes once the clock is taken out; if not, it hides.

    pytest apps/game_generation/tests/test_blocked_row_hours.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
LOC = "loc_bar"


def _row(cid, conditions="", schedules=""):
    return f"""

[[canvases]]
id   = "{cid}"
name = "{cid}"

[canvases.trigger]
location          = "{LOC}"
is_repeatable     = true
show_when_blocked = true
cooldown_message  = "HOURS_{cid}"
{conditions}
{schedules}

[[canvases.nodes]]
id = "base"
name = "Base"
blocks = [{{ type = "paragraph", content = "A row." }}]
"""


def _conds(*items, logic="AND"):
    return f'conditions = {{ version = "1.0", logic = "{logic}", items = [{", ".join(items)}] }}'


SHUT_CLOCK = '{ type = "time_of_day", start_time = "03:00", end_time = "03:01" }'
HIGH_METER = '{ type = "trait", subject = "player", trait_key = "corr", operator = "gte", value = 60 }'
LOW_METER = '{ type = "trait", subject = "player", trait_key = "corr", operator = "gte", value = 0 }'
UNSET_FLAG = '{ type = "flag", subject = "player", flag_key = "started", operator = "is_true" }'
AT_HOUR3 = """
[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "03:00"
end_time = "03:01"
"""

ROWS = (
    _row("clock_only", _conds(SHUT_CLOCK))
    + _row("clock_and_met", _conds(LOW_METER, SHUT_CLOCK))
    + _row("clock_and_meter", _conds(HIGH_METER, SHUT_CLOCK))
    + _row("meter_only", _conds(HIGH_METER))
    + _row("flag_with_schedule", _conds(UNSET_FLAG), AT_HOUR3)
    + _row("schedule_only", "", AT_HOUR3)
    + _row("either_clock_or_meter", _conds(HIGH_METER, SHUT_CLOCK, logic="OR"))
)


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    """The first_term shapes on the default build path, into a scratch dir."""
    root = tmp_path_factory.mktemp("blocked_row_hours")
    toml = root / "fixture.toml"
    with open(FIXTURE, encoding="utf-8") as fh:
        toml.write_text(fh.read() + ROWS, encoding="utf-8")
    return build(toml, root / "out")


@needs_browser
def test_the_row_shows_its_hours_only_when_the_clock_shut_it(html):
    with open_game(html) as game:
        game.js("""() => { const sv = SugarCube.State.variables;
            sv.game_state.time_state.current_hour = 12; sv.game_state.time_state.current_minute = 0; }""")
        out = game.js("(l) => SugarCube.setup.renderSoloActivities(l)", LOC)
        assert not game.errors, game.errors
    for shown in ("clock_only", "clock_and_met", "schedule_only", "either_clock_or_meter"):
        assert f"HOURS_{shown}" in out, (shown, out)
    for hidden in ("clock_and_meter", "meter_only", "flag_with_schedule"):
        assert hidden not in out, (hidden, out)


def test_the_helper_is_on_the_blocked_branch_only():
    """The daily-limit branch stays as it was: a limit is the clock's to reopen."""
    src = open("apps/game_generation/twee_comprehensive/generators/v2.py", encoding="utf-8").read()
    assert src.count("c.showWhenBlocked && setup.onlyTheClockShut(c)") == 1
