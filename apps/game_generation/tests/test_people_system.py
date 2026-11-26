"""`[engine.people] system = "cot"`: Course of Temptation's people system (2026-11-25).

What is checked, each against CoT's own code
(/Users/a0000/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt):

  * a game without the switch gets none of it, and every key only it reads is an error;
  * the importer's checks (unknown trait, unknown want, a value out of range, a gate on an
    unknown skill, a missing `attracted` or `gender`);
  * what each person wants (desired_relationship): hand-set, a professor by intimacy 0/1/2,
    and friend / fuckbuddy / hatefuck / rival / indifferent / date from the feelings, the
    lust tipping point (Chaste, Slut, female) and the traits;
  * a lust gain on a person who is not attracted is dropped; feelings hold in -1000..1000;
  * a trait shows by liking, by dislike twice as fast, a sex trait only after the partner
    flag (filter_known_traits);
  * fading after 14 days unseen, 10 a day, stopping at 100 and -100, control untouched
    (attitude_to_mean);
  * her skills: the level in the sidebar, a gate hidden / greyed / passed, the gain table,
    the daily cap (raise_skill);
  * the People view's meters and bubbles (no want line, as CoT); the three conditions.

    pytest apps/game_generation/tests/test_people_system.py -q
"""
import os

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.people_system import default_traits
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = os.path.join(
    os.path.dirname(__file__), "data", "people_system_2026_11_25.toml"
)
COT_PAGES = os.path.join(os.path.dirname(__file__), "data", "cot_pages_2026_11_25.toml")
HOME = "Location_loc_home"
CHAT = "Canvas_ben_chat_Node_talk"


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(mutate, path=FIXTURE):
    raw = parse_toml(path)
    mutate(raw)
    return validate(normalize(raw))


def _npc(raw, npc_id):
    return next(n for n in raw["npcs"] if n["id"] == npc_id)


def _choice(raw, text):
    canvas = next(c for c in raw["canvases"] if c["id"] == "ben_chat")
    choices = canvas["nodes"][0]["exit_block"]["choices"]
    return next(c for c in choices if c["text"] == text)


# ── 1. the switch ────────────────────────────────────────────────────────────


def test_the_fixture_is_clean():
    assert validate(normalize(parse_toml(FIXTURE))) == []


def test_without_the_switch_nothing_is_emitted():
    twee = _twee(parse_toml(COT_PAGES))
    assert "peopleSys" not in twee
    assert "people_cfg" not in twee


def test_with_the_switch_the_script_and_the_hooks_are_emitted():
    twee = _twee(parse_toml(FIXTURE))
    assert twee.count("setup.people_cfg = ") == 1
    for call in (
        "setup.peopleSys.dropEffect(",
        "setup.peopleSys.settle(",
        "setup.peopleSys.touched(",
        "setup.peopleSys.skillAllow(",
        "setup.peopleSys.sceneWith(",
        "setup.peopleSys.fadeDay();",
        "setup.peopleSys.checkCondition(it)",
        "setup.peopleSys.checkCondition(item)",
        "setup.peopleSys.shownValue(_k)",
        "setup.peopleSys.meterRows(",
        "setup.peopleSys.viewHtml(slug)",
    ):
        assert call in twee, call


def test_the_config_reaches_the_game_through_the_graph():
    graph = build_game_graph(normalize(parse_toml(FIXTURE)))
    cfg = graph.project.metadata["people_system"]
    assert cfg["npcs"]["ben"] == {
        "attracted": True,
        "gender": "male",
        "traits": ["Shy", "Nerd", "Groper"],
    }
    assert cfg["npcs"]["ian"]["want"] == "rival"
    assert cfg["npcs"]["holt"]["professor"] is True
    assert cfg["npcs"]["old"]["age"] == 50
    assert cfg["skills"] == {"exhibitionism": "Exhibitionism", "charm": "Charm"}
    assert cfg["fade"] is True
    # CoT's table is the default; the game's own trait sits beside it.
    assert cfg["traits"]["Shy"]["threshold"] == 100
    assert cfg["traits"]["Shy"]["kind"] == "personality"
    assert cfg["traits"]["Groper"] == default_traits()["Groper"]
    assert cfg["traits"]["Risktaker"]["threshold"] == 600
    assert cfg["traits"]["Gossip"]["threshold"] == 150


def test_cots_table_is_the_default():
    table = default_traits()
    shown = [t for t in table.values() if not t.get("hidden")]
    assert len(shown) == 51
    assert sum(t["kind"] == "sex" for t in shown) == 23
    assert table["Chaste"]["emoji"] == "🙏"
    assert table["Slut"]["threshold"] == 50
    assert table["Natural Odor"]["threshold"] == 10
    assert table["Confident"]["hidden"] is True


def test_every_person_carries_the_three_feelings():
    template = normalize(parse_toml(FIXTURE))
    by_id = {n.id: n for n in template.npcs}
    assert by_id["ben"].core_traits == {"friendship": 0, "lust": 0, "control": 0}
    assert by_id["liz"].core_traits == {
        "friendship": 300,
        "lust": -250,
        "control": -150,
    }
    assert by_id["holt"].core_traits["intimacy"] == 0


def test_a_skill_gate_becomes_a_condition_and_an_effect():
    template = normalize(parse_toml(FIXTURE))
    canvas = next(c for c in template.canvases if c.id == "ben_chat")
    strip = next(c for c in canvas.nodes[0].exit_block.choices if c.text == "Strip.")
    assert strip.conditions == {
        "version": "1.0",
        "logic": "AND",
        "items": [{"type": "skill_level", "skill": "exhibitionism", "level": 3}],
    }
    assert strip.locked_text == "Strip. (Needs Exhibitionism 3)"
    assert strip.effects[-1].trait == "exhibitionism"
    assert strip.effects[-1].value == {
        "type": "skill_gain",
        "skill": "exhibitionism",
        "level": 3,
    }


# ── 2. the importer's checks ─────────────────────────────────────────────────


def _has(errors, *parts):
    return any(all(p in e for p in parts) for e in errors)


def test_an_unknown_trait_is_an_error():
    def mutate(raw):
        _npc(raw, "ben")["traits"] = ["Shy", "Brooding"]

    assert _has(_errors(mutate), "npcs['ben'].traits", "unknown trait 'Brooding'")


def test_an_unknown_want_is_an_error():
    def mutate(raw):
        _npc(raw, "ian")["want"] = "lover"

    assert _has(_errors(mutate), "npcs['ian'].want", "unknown want 'lover'")


def test_a_feeling_out_of_range_is_an_error():
    def mutate(raw):
        _npc(raw, "liz")["core_traits"]["friendship"] = 1200

    assert _has(_errors(mutate), "npcs['liz'].core_traits.friendship", "-1000 to 1000")


def test_intimacy_is_zero_one_or_two_and_a_professors():
    def too_high(raw):
        _npc(raw, "holt")["core_traits"] = {"intimacy": 3}

    assert _has(_errors(too_high), "npcs['holt'].core_traits.intimacy", "0, 1 or 2")

    def not_a_professor(raw):
        _npc(raw, "ben")["core_traits"] = {"intimacy": 1}

    assert _has(_errors(not_a_professor), "npcs['ben']", "only for a professor")


def test_attracted_and_gender_are_required():
    def no_attracted(raw):
        del _npc(raw, "gus")["attracted"]

    assert _has(_errors(no_attracted), "npcs['gus'].attracted must be true or false")

    def no_gender(raw):
        del _npc(raw, "gus")["gender"]

    assert _has(_errors(no_gender), "npcs['gus'].gender must be")


def test_a_gate_on_an_unknown_skill_is_an_error():
    def mutate(raw):
        _choice(raw, "Strip.")["skill_gate"] = {"skill": "voyeurism", "level": 3}

    assert _has(_errors(mutate), "skill_gate", "unknown skill 'voyeurism'")

    def bad_level(raw):
        _choice(raw, "Strip.")["skill_gate"] = {"skill": "exhibitionism", "level": 11}

    assert _has(_errors(bad_level), "skill_gate.level", "1 to 10")


def test_a_skill_must_be_one_of_her_traits_in_range():
    def missing(raw):
        del raw["player"]["core_traits"]["charm"]

    assert _has(_errors(missing), "traits.labels[charm]", "not in [player] core_traits")

    def too_high(raw):
        raw["player"]["core_traits"]["charm"] = 1500

    assert _has(_errors(too_high), "core_traits.charm is a skill", "0 to 1000")


def test_the_conditions_are_checked():
    def item(raw):
        canvas = next(c for c in raw["canvases"] if c["id"] == "ben_chat")
        return canvas["nodes"][0]["blocks"][1]["props"]["conditions"]["items"][0]

    def bad_want(raw):
        item(raw)["any_of"] = ["fuckbuddy", "lover"]

    assert _has(_errors(bad_want), "unknown want 'lover'")

    def bad_npc(raw):
        item(raw)["npc_id"] = "nobody"

    assert _has(_errors(bad_npc), "`npc_wants` condition needs npc_id")

    def bad_trait(raw):
        canvas = next(c for c in raw["canvases"] if c["id"] == "ben_chat")
        canvas["nodes"][0]["blocks"][3]["props"]["conditions"]["items"][0][
            "trait"
        ] = "Brooding"

    assert _has(_errors(bad_trait), "unknown trait 'Brooding'", "npc_has_trait")


def test_the_engine_table_is_checked():
    def bad_system(raw):
        raw["engine"]["people"]["system"] = "dol"

    assert _has(_errors(bad_system), '[engine.people] system must be "cot"')

    def bad_key(raw):
        raw["engine"]["people"]["decay"] = True

    assert _has(_errors(bad_key), "[engine.people]: unknown key `decay`")

    def bad_kind(raw):
        raw["engine"]["people"]["traits"]["Gossip"]["kind"] = "hobby"

    assert _has(_errors(bad_kind), "[engine.people.traits.Gossip] kind must be")


def test_every_key_is_an_error_without_the_switch():
    def mutate(raw):
        del raw["engine"]["people"]

    errors = _errors(mutate)
    need = 'is read only under [engine.people] system = "cot"'
    assert _has(errors, "npcs['ben'].attracted", need)
    assert _has(errors, "npcs['ben'].traits", need)
    assert _has(errors, "npcs['ian'].want", need)
    assert _has(errors, "traits.labels[exhibitionism] skill", need)
    assert _has(errors, ".skill_gate", need)
    assert _has(errors, "`npc_wants` condition", need)
    assert _has(errors, "`npc_has_trait` condition", need)


# ── 3. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("people_system") / "out")


def _set(g, slug, **values):
    g.js(
        "([s, v]) => Object.assign(SugarCube.State.variables.npcs[s].core_traits, v)",
        [slug, values],
    )


def _flag(g, name, value=True):
    g.js("([n, v]) => { SugarCube.State.variables.flags[n] = v; }", [name, value])


def _want(g, slug, **values):
    _set(g, slug, **values)
    return g.js("(s) => SugarCube.setup.peopleSys.want(s)", slug)


def _feel(g, slug):
    return g.sv(f"npcs.{slug}.core_traits")


def _skill(g, key, value=None):
    if value is not None:
        g.js(
            "([k, v]) => { SugarCube.State.variables.player.core_traits[k] = v; }",
            [key, value],
        )
    return g.sv(f"player.core_traits.{key}")


def _days(g, n):
    g.js("(n) => { for (let i = 0; i < n; i++) advanceDay(); }", n)


def _links(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage a')].map(a => a.textContent.trim())"
    )


def _locked(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage .locked-choice')].map(a => a.textContent.trim())"
    )


def _text(g):
    return g.js("() => document.querySelector('.passage').innerText")


def _view(g, slug):
    g.js("(s) => SugarCube.setup.peopleView(s)", slug)
    g.page.wait_for_timeout(150)
    return g.js("() => document.querySelector('.passage').innerText")


@needs_browser
def test_a_hand_set_want_wins(html):
    with open_game(html) as g:
        g.play(HOME)
        assert _want(g, "ian") == "rival"
        assert _want(g, "ian", friendship=900, lust=900) == "rival"
        assert g.errors == []


@needs_browser
def test_a_professor_is_indifferent_until_intimacy_two(html):
    with open_game(html) as g:
        g.play(HOME)
        assert _want(g, "holt", lust=900, friendship=900, intimacy=0) == "indifferent"
        assert _want(g, "holt", intimacy=1) == "indifferent"
        assert _want(g, "holt", intimacy=2) == "fuckbuddy"
        # CoT professor_intimacy: a sex partner counts as 2 whatever the number says.
        _set(g, "holt", intimacy=0)
        _flag(g, "sex_partner_holt")
        assert _want(g, "holt") == "fuckbuddy"
        assert g.errors == []


@needs_browser
def test_the_want_is_worked_out_from_feelings_and_traits(html):
    with open_game(html) as g:
        g.play(HOME)
        cases = [
            # ben: Shy, Nerd, Groper: neither forward nor casual.
            ("ben", {"friendship": 0, "lust": 0}, "indifferent"),
            ("ben", {"friendship": 200, "lust": 0}, "friend"),
            ("ben", {"friendship": 199, "lust": 0}, "indifferent"),
            ("ben", {"friendship": -100, "lust": 0}, "rival"),
            ("ben", {"friendship": 150, "lust": 299}, "indifferent"),
            ("ben", {"friendship": 150, "lust": 300}, "date"),
            ("ben", {"friendship": 0, "lust": 300}, "indifferent"),
            ("ben", {"friendship": -100, "lust": 300}, "rival"),
            # cal: Forward (active, casual sex).
            ("cal", {"friendship": 200, "lust": 0}, "fuckbuddy"),
            ("cal", {"friendship": 100, "lust": 300}, "fuckbuddy"),
            ("cal", {"friendship": -100, "lust": 0}, "hatefuck"),
            ("cal", {"friendship": -100, "lust": 300}, "hatefuck"),
            ("cal", {"friendship": 0, "lust": 300}, "indifferent"),
            # dee: Chaste, never a fuckbuddy or a hatefuck.
            ("dee", {"friendship": 250, "lust": 1000}, "friend"),
            ("dee", {"friendship": -150, "lust": 1000}, "rival"),
            # eve: Slut, tipping point 200.
            ("eve", {"friendship": 150, "lust": 200}, "fuckbuddy"),
            ("eve", {"friendship": 150, "lust": 199}, "indifferent"),
            # fay: a dominant woman who dislikes her.
            ("fay", {"friendship": -100, "lust": 0}, "hatefuck"),
            ("fay", {"friendship": 200, "lust": 0}, "fuckbuddy"),
            # gus: not attracted.
            ("gus", {"friendship": 250, "lust": 0}, "friend"),
            ("gus", {"friendship": -150, "lust": 0}, "rival"),
            # old: 50, friendly and lusting, never a date.
            ("old", {"friendship": 150, "lust": 300}, "friend"),
        ]
        got = [(s, v, _want(g, s, **v)) for s, v, _ in cases]
        assert got == cases
        # A sex partner with any lust at all counts as past the tipping point.
        _flag(g, "sex_partner_ben")
        assert _want(g, "ben", friendship=150, lust=1) == "date"
        assert g.errors == []


@needs_browser
def test_the_lust_tipping_point(html):
    with open_game(html) as g:
        g.play(HOME)
        tip = {
            s: g.js("(s) => SugarCube.setup.peopleSys.tippingPoint(s)", s)
            for s in ("ben", "dee", "eve", "fay")
        }
        # 300; a woman +100; Chaste +800; Slut -200 (_cot_js.txt:114822-114836).
        assert tip == {"ben": 300, "dee": 1200, "eve": 200, "fay": 400}


@needs_browser
def test_lust_rises_only_for_a_person_who_is_attracted(html):
    with open_game(html) as g:
        g.play(CHAT)
        g.click("Flirt.")
        assert _feel(g, "ben")["lust"] == 50
        assert _feel(g, "gus") == {"friendship": 25, "lust": 0, "control": 0}
        # A fall is not a gain: it still lands on a person who is not attracted.
        g.js(
            "() => SugarCube.setup.applyAndNotifyTrait('npc', 'gus', 'lust', 'add', -30, false, null)"
        )
        assert _feel(g, "gus")["lust"] == -30
        assert g.errors == []


@needs_browser
def test_feelings_and_intimacy_hold_their_range(html):
    with open_game(html) as g:
        g.play(CHAT)
        g.click("Insult him.")
        assert _feel(g, "ben")["friendship"] == -1000
        g.play(CHAT)
        g.click("Stay after class.")
        assert _feel(g, "holt")["intimacy"] == 2
        # clamp = true (the engine's 0-100) does not cut a feeling short.
        g.js(
            "() => SugarCube.setup.applyAndNotifyTrait('npc', 'cal', 'friendship', 'add', 5000, true, null)"
        )
        assert _feel(g, "cal")["friendship"] == 1000
        assert g.errors == []


@needs_browser
def test_traits_show_by_liking_by_dislike_and_after_sex(html):
    with open_game(html) as g:
        g.play(HOME)

        def known(slug, **values):
            _set(g, slug, **values)
            return g.js("(s) => SugarCube.setup.peopleSys.knownTraits(s)", slug)

        assert known("ben", friendship=100) == []  # above the threshold, not at it
        assert known("ben", friendship=101) == ["Shy"]
        assert known("ben", friendship=201) == ["Shy", "Nerd"]
        # Dislike counts double: -51 reads as 102.
        assert known("ben", friendship=-50) == []
        assert known("ben", friendship=-51) == ["Shy"]
        assert known("ben", friendship=-101) == ["Shy", "Nerd"]
        # A sex trait: never by lust alone, only once they have slept together.
        assert known("ben", friendship=0, lust=900) == []
        _flag(g, "sex_partner_ben")
        assert known("ben", lust=200) == []
        assert known("ben", lust=201) == ["Groper"]
        # The game's own trait, at its own threshold.
        assert known("liz", friendship=150) == []
        assert known("liz", friendship=151) == ["Gossip"]
        assert g.errors == []


@needs_browser
def test_unseen_people_fade_to_a_hundred_and_stop(html):
    with open_game(html) as g:
        g.play(HOME)
        day = g.sv("game_state.time_state.day")
        _set(g, "ben", friendship=300, lust=-300, control=500)
        _set(g, "cal", friendship=300, lust=300)  # never seen: no clock, no fading
        _set(g, "eve", friendship=50, lust=-100)  # inside -100..100: never moves
        for slug in ("ben", "eve"):
            g.js(
                "([s, d]) => { SugarCube.State.variables.npcs[s].people_seen = d; }",
                [slug, day],
            )
        _days(g, 14)
        assert _feel(g, "ben") == {"friendship": 300, "lust": -300, "control": 500}
        _days(g, 1)  # the fifteenth day without her
        assert _feel(g, "ben") == {"friendship": 290, "lust": -290, "control": 500}
        _days(g, 19)
        assert _feel(g, "ben") == {"friendship": 100, "lust": -100, "control": 500}
        _days(g, 30)
        assert _feel(g, "ben") == {"friendship": 100, "lust": -100, "control": 500}
        assert _feel(g, "cal") == {"friendship": 300, "lust": 300, "control": 0}
        assert _feel(g, "eve") == {"friendship": 50, "lust": -100, "control": 0}
        assert g.errors == []


@needs_browser
def test_seen_is_a_feeling_change_and_a_scene_refreshes_it(html):
    with open_game(html) as g:
        g.play(HOME)
        assert g.sv("npcs.ben.people_seen") is None
        # A scene with nobody's feelings moved starts no clock (meters frozen: no fading).
        g.play(CHAT)
        g.click("Say nothing.")
        assert g.sv("npcs.ben.people_seen") is None
        _set(g, "ben", friendship=300)
        _days(g, 40)
        assert _feel(g, "ben")["friendship"] == 300
        # A feeling change starts it.
        g.play(CHAT)
        g.click("Flirt.")
        seen = g.sv("npcs.ben.people_seen")
        assert seen == g.sv("game_state.time_state.day")
        assert g.sv("npcs.gus.people_seen") == seen  # his friendship moved
        # Ten days on, a scene with Ben alone refreshes his day and not Gus's.
        _days(g, 10)
        g.js("() => SugarCube.setup.markCanvasTriggered('ben_chat')")
        if g.sv("npcs.ben.people_seen") == seen:
            # The engine keys the mark by its own canvas id; ask it for that id.
            g.js(
                """() => { const m = SugarCube.setup.help_data.canvasIdToNpcUuid;
                    Object.keys(m).forEach(k => SugarCube.setup.markCanvasTriggered(k)); }"""
            )
        assert g.sv("npcs.ben.people_seen") == seen + 10
        assert g.sv("npcs.gus.people_seen") == seen
        assert g.errors == []


@needs_browser
def test_fade_can_be_switched_off(html):
    with open_game(html) as g:
        g.play(HOME)
        g.js("() => { SugarCube.setup.people_cfg.fade = false; }")
        _set(g, "ben", friendship=300)
        g.js("() => { SugarCube.State.variables.npcs.ben.people_seen = 1; }")
        _days(g, 40)
        assert _feel(g, "ben")["friendship"] == 300


@needs_browser
def test_the_sidebar_shows_a_skill_as_its_level(html):
    with open_game(html) as g:
        g.play(HOME)
        rows = g.js(
            "() => [...document.querySelectorAll('#traits-widget .trait-item')]"
            ".map(li => li.innerText.replace(/\\s+/g, ' ').trim())"
        )
        assert "Charm 2" in rows and "Exhibitionism 0" in rows
        assert "Energy 100" in rows  # anything else reads as it is
        assert g.errors == []


@needs_browser
def test_a_skill_gate_is_hidden_greyed_or_open(html):
    with open_game(html) as g:
        g.play(CHAT)
        links = _links(g)
        assert (
            "Undo a button." in links
        )  # a level-1 gate is always open (CoT skillleveled)
        assert "Talk him round." in links  # Charm 2 against a level-2 gate
        assert "Lift your top." not in links and "Lift your top." not in _text(g)
        assert _locked(g) == ["Strip. (Needs Exhibitionism 3)"]
        _skill(g, "exhibitionism", 300)
        g.play(CHAT)
        links = _links(g)
        assert "Lift your top." in links and "Strip." in links
        assert _locked(g) == []
        assert g.errors == []


@needs_browser
def test_passing_a_gate_raises_the_skill(html):
    with open_game(html) as g:
        g.play(CHAT)
        g.click("Undo a button.")  # level 0 at a level-1 gate: 10 / 2
        assert _skill(g, "exhibitionism") == 5
        g.play(CHAT)
        g.click("Talk him round.")  # level 2 at a level-2 gate: 6
        assert _skill(g, "charm") == 256
        assert g.errors == []


@needs_browser
def test_the_gain_table(html):
    with open_game(html) as g:
        g.play(HOME)

        def gain(value, gate):
            _skill(g, "exhibitionism", value)
            return g.js(
                "(l) => SugarCube.setup.peopleSys.skillGain('exhibitionism', l)", gate
            )

        # At her own level: 10, 7, 6, 5, 4, 3 (CoT default_increase).
        assert [gain(v, max(1, v // 100)) for v in (0, 100, 200, 300, 400, 500)] == [
            5,  # level 0 has no gate of its own: a level-1 gate, halved
            7,
            6,
            5,
            4,
            3,
        ]
        assert gain(1000, 10) == 0
        # The gate is far below her level (_cot_js.txt:96759-96767).
        assert gain(200, 1) == 4  # one below, above level 1: / 1.5
        assert gain(300, 1) == 2  # two below: / 2.5
        assert gain(500, 2) == 1  # three below: / 3
        assert gain(400, 1) == pytest.approx(4 / 3)


@needs_browser
def test_a_skill_rises_under_its_daily_cap(html):
    with open_game(html) as g:
        g.play(HOME)

        def add(n):
            g.js(
                "(n) => SugarCube.setup.applyAndNotifyTrait('player', null, 'exhibitionism', 'add', n, false, null)",
                n,
            )
            return _skill(g, "exhibitionism")

        # Level 0: 30 a day.
        assert [add(10) for _ in range(4)] == [10, 20, 30, 30]
        _days(g, 1)
        assert add(100) == 60  # one gain is cut to the day's cap
        assert add(1) == 60
        # Level 1: 21 a day.
        _skill(g, "exhibitionism", 100)
        _days(g, 1)
        assert add(15) == 115
        assert add(15) == 121
        # A fall is not capped; the top is 1000; a `set` is not capped.
        assert add(-50) == 71
        _skill(g, "exhibitionism", 995)
        _days(g, 1)
        assert add(50) == 1000
        g.js(
            "() => SugarCube.setup.applyAndNotifyTrait('player', null, 'exhibitionism', 'set', 5000, false, null)"
        )
        assert _skill(g, "exhibitionism") == 1000
        # Another trait of hers is untouched by any of it.
        g.js(
            "() => SugarCube.setup.applyAndNotifyTrait('player', null, 'energy', 'add', -60, false, null)"
        )
        assert g.sv("player.core_traits.energy") == 40
        assert g.errors == []


@needs_browser
def test_the_people_view_shows_meters_bubbles_and_the_want(html):
    with open_game(html) as g:
        g.play(HOME)
        # Liz: friendship 300, lust -250, control -150, Gossip (threshold 150).
        text = _view(g, "liz")
        assert "Friendship" in text and "Lust" in text and "Her Submission" in text
        assert "Dislike" not in text and "Attracted" not in text
        assert "Personality" in text and "Gossip" in text
        assert "Wants to" not in text  # CoT never prints the want (LO 2026-11-25)
        widths = g.js(
            "() => [...document.querySelectorAll('.passage .people-meter-fill')].map(e => e.style.width)"
        )
        assert widths == ["30%", "0%", "15%"]
        # Ben at nothing: two meters, no Personality block.
        text = _view(g, "ben")
        assert "Friendship" in text and "Lust" in text
        assert "Dominance" not in text and "Submission" not in text
        assert "Personality" not in text and "???" not in text
        assert "Indifferent" not in text
        # Ben disliking her: "Dislike", two traits known and one still "???", a rival.
        _set(g, "ben", friendship=-150)
        text = _view(g, "ben")
        assert "Dislike" in text and "Friendship" not in text
        bubbles = g.js(
            "() => [...document.querySelectorAll('.passage .personality-traits-container .npc-display-infobubble')]"
            ".map(e => [e.textContent, e.className.split(' ').pop(), e.title])"
        )
        assert bubbles == [
            [
                "Shy",
                "known-trait-personality",
                "They tend to be passive or unsure during interactions.",
            ],
            [
                "Nerd",
                "known-trait-personality",
                "Likes science, geek culture, and the like.",
            ],
            ["???", "unknown-trait", "This trait is unknown."],
        ]
        assert "rival" not in text.lower()
        # Control shows from 100, or from the first point for a dominant or submissive person.
        _set(g, "ben", control=99)
        assert "Dominance" not in _view(g, "ben")
        _set(g, "ben", control=100)
        assert "His Dominance" in _view(g, "ben")
        _set(g, "ian", control=1)  # Sadist stands in the dominant set
        assert "His Dominance" in _view(g, "ian")
        # The list card carries the same meters.
        g.js("() => SugarCube.setup.peopleOpen()")
        g.page.wait_for_timeout(150)
        card = g.js(
            "() => document.querySelector('.passage .view-people-person[data-slug=\"liz\"]').innerText"
        )
        assert "Friendship" in card and "Lust" in card and "Her Submission" in card
        assert g.errors == []


@needs_browser
def test_the_conditions_branch_a_block_and_a_choice(html):
    with open_game(html) as g:
        g.play(CHAT)
        text = _text(g)
        assert "He goes red." in text  # npc_has_trait: Shy
        assert "He takes charge." not in text  # npc_has_trait set = "active"
        assert "He wants you in his bed." not in text  # npc_wants any_of
        assert "Ask what he wants." not in _links(g)  # npc_wants is_false indifferent
        _set(g, "ben", friendship=150, lust=300)  # he wants to date her
        g.play(CHAT)
        assert "He wants you in his bed." in _text(g)
        assert "Ask what he wants." in _links(g)
        # The second evaluator gives the same answers.
        checks = g.js(
            """() => { const c = SugarCube.setup.checkSingleCondition; return [
                c({type: 'npc_wants', npc_id: 'ben', value: 'date'}),
                c({type: 'npc_wants', npc_id: 'ben', value: 'date', operator: 'is_false'}),
                c({type: 'npc_has_trait', npc_id: 'ben', trait: 'Shy'}),
                c({type: 'npc_has_trait', npc_id: 'cal', set: 'casualsex'}),
                c({type: 'npc_has_trait', npc_id: 'ben', set: 'casualsex'}),
                c({type: 'skill_level', skill: 'charm', level: 2}),
                c({type: 'skill_level', skill: 'charm', level: 3}),
                c({type: 'skill_level', skill: 'exhibitionism', level: 1}),
            ]; }"""
        )
        assert checks == [True, False, True, True, False, True, False, True]
        assert g.errors == []


# ── show_traits = false: traits are the author's, the view prints none (LO 2026-11-26) ──


def test_show_traits_must_be_a_bool_and_is_written_only_when_false():
    errs = _errors(lambda raw: raw["engine"]["people"].update(show_traits="no"))
    assert any("show_traits must be true or false" in e for e in errs), errs

    raw = parse_toml(FIXTURE)
    assert '"show_traits"' not in _twee(raw)
    raw["engine"]["people"]["show_traits"] = False
    assert '"show_traits": false' in _twee(raw)


@needs_browser
def test_show_traits_false_prints_no_trait_and_no_unknown_bubble(html):
    with open_game(html) as g:
        g.play(HOME)
        assert "Gossip" in _view(g, "liz")
        g.js("() => { SugarCube.setup.people_cfg.show_traits = false; }")
        text = _view(g, "liz")
        assert "Friendship" in text
        assert "Personality" not in text and "Gossip" not in text and "???" not in text
        # scenes still read a trait
        assert g.js("() => SugarCube.setup.peopleSys.hasTrait('ben', 'Shy')") is True
