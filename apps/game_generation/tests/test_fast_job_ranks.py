"""E6 (World and Systems PRD) — a rank per job.

Before this, the phone's fast jobs kept one global XP count for every job and each job
paid one fixed `income`, so a job could not promote her. Opt-in per job:

    ranks = [ { xp = 0, title = "Barback", income = 10 },
              { xp = 2, title = "Server",  income = { type = "trait", trait = "charm", add = 20 } } ]

Each shift adds one to `$game_state.fast_jobs.job_xp[id]`; her rank is the last one
whose `xp` she has reached on that job, and its `income` (a number or a value table)
replaces the job's. The board shows the title and the xp to the next rank; a promotion
toasts. The global `xp` (read by `xp_req`) still counts every shift.

    pytest apps/game_generation/tests/test_fast_job_ranks.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch2_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e6") / "out")


def _work(g, job):
    g.js("() => { SugarCube.State.variables.game_state.fast_jobs.cooldowns = {}; }")
    g.js("(j) => SugarCube.setup.doFastJob(j)", job)


def _money(g):
    return g.sv("player.core_traits.money")


def _board(g):
    return g.js("""() => { if (!jQuery('.phone-frame').length) SugarCube.setup.openPhone();
                           SugarCube.setup.openPhoneApp('jobs');
                           return jQuery('.phone-frame').html(); }""")


@needs_browser
def test_a_job_climbs_its_ranks_and_pays_each_ranks_income(html):
    with open_game(html) as g:
        assert g.sv("game_state.fast_jobs.job_xp") == {}
        start = _money(g)
        paid = []
        for _ in range(5):
            before = _money(g)
            _work(g, "bar_job")
            paid.append(_money(g) - before)
        # Barback twice (10), Server twice (charm 10 + 20 = 30), then Head server (60)
        assert paid == [10, 10, 30, 30, 60]
        assert _money(g) == start + 140
        assert g.sv("game_state.fast_jobs.job_xp") == {"bar_job": 5}
        assert g.sv("game_state.fast_jobs.xp") == 5  # the global count still runs
        assert g.errors == []


@needs_browser
def test_the_board_shows_the_rank_and_the_next_one(html):
    with open_game(html) as g:
        board = _board(g)
        assert "Barback · 0/2 xp" in board and "$10" in board
        _work(g, "bar_job")
        _work(g, "bar_job")
        board = _board(g)
        assert "Server · 2/4 xp" in board and "$30" in board
        assert g.js("() => jQuery('.phone-notify').text()").find("Bar: Server") >= 0
        _work(g, "bar_job")
        _work(g, "bar_job")
        assert "Head server" in _board(g) and "/" not in _board(g).split("Head server")[1].split("</div>")[0]
        assert g.errors == []


@needs_browser
def test_a_job_without_ranks_counts_no_job_xp(html):
    with open_game(html) as g:
        before = _money(g)
        _work(g, "flat")
        assert _money(g) == before + 20
        assert "flat" not in g.sv("game_state.fast_jobs.job_xp")
        assert g.errors == []


@needs_browser
def test_a_save_made_before_e6_gets_job_xp_and_starts_at_the_first_rank(html):
    """The save string was written by the PRE-change engine: this fixture built at
    e8dcadc (that engine ignores `ranks` and pays `income` = 5), then played headless:
    $flags.started set, Engine.play Location_loc_home, doFastJob('bar_job') twice (the
    cooldown cleared between), Engine.play Location_loc_home, then Save.serialize().
    Its fast_jobs state is {xp: 2, cooldowns: {...}} with no job_xp."""
    with open_game(html) as g:
        assert g.load_save(read_data("e6_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.fast_jobs.job_xp") == {}  # backfilled
        assert g.sv("game_state.fast_jobs.xp") == 2       # kept
        before = _money(g)
        _work(g, "bar_job")
        assert _money(g) == before + 10  # shifts before the change do not count toward rank
        assert g.sv("game_state.fast_jobs.job_xp") == {"bar_job": 1}
        assert g.errors == []
