"""Cross-release saves: what survives a new build, and what the engine promises.

SugarCube never re-runs `:: Start` on load. A player who saved on 0.2 and opens
0.3 therefore arrives with 0.2's variable skeleton, and every key 0.3 added is
`undefined` — which is a crash, not a missing feature, the first time anything
reads it.

`setup.backfillStateDefaults` is the seam that heals that. Before this suite it
knew three keys — flags, `player.core_traits`, npcs — so turning ON any optional
system in a patch release (phone, rent, passes, inventory, clothing) left the
whole sub-map undefined in every existing save, and the only remedy was an author
remembering to hand-write an `ndef` guard at each read site. Exactly two such
guards were ever written, both after something broke.

Two halves, and the second is the one that matters:

  * **Python** — `:: Start` and `setup.stateDefaults` are serialized from the SAME
    dicts, so the defaults can never fall behind what a fresh game starts with.
    That is the property the old string-block build could not hold.
  * **Node** — the migration is executed against synthetic old saves. Source greps
    cannot tell a correct fill-if-absent from one that clobbers an earned value;
    running it can. Skipped when node is absent.

⚠️ The depth is deliberately NOT uniform, and `test_wardrobe_is_not_filled_into`
is the reason: `$player.wardrobe` is an id -> garment map, so a depth-2 fill hands
back a garment the player sold. `$game_state` sub-maps are engine bookkeeping and
are safe to fill into. If someone ever "tidies" this into one uniform merge, that
test goes red.

    pytest apps/game_generation/tests/test_save_migration.py -q
"""
import json
import os
import re
import shutil
import subprocess
import textwrap

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

# Checked-in, media-free — the same fixture test_nodb_equivalence.py builds on.
FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
# A real game that turns ON phone + clothing + inventory + customization, i.e. every
# optional sub-map at once. Skipped where the game folder is not checked out.
RICH = "games/the_inheritance/toml_phases/7_final_game.toml"

needs_node = pytest.mark.skipif(
    shutil.which("node") is None, reason="node not installed"
)
needs_rich = pytest.mark.skipif(
    not os.path.exists(RICH), reason="the_inheritance TOML not present"
)


# --- building -------------------------------------------------------------------


def build(toml_path=FIXTURE):
    graph = build_game_graph(normalize(parse_toml(toml_path)))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def brace_span(text, start):
    """Slice the balanced {...} that begins at or after `start`."""
    i = text.index("{", start)
    depth, j = 0, i
    while True:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i : j + 1]
        j += 1


def start_var(twee, name):
    """The object `:: Start` assigns to $name, parsed."""
    body = twee.split(":: Start\n", 1)[1]
    head = "<<set $%s = " % name
    return json.loads(brace_span(body, body.index(head) + len(head)))


def state_defaults(twee):
    return json.loads(brace_span(twee, twee.index("setup.stateDefaults = ")))


def backfill_source(twee):
    return "setup.backfillStateDefaults = function (sv) " + brace_span(
        twee, twee.index("setup.backfillStateDefaults = function (sv)")
    )


# --- Python: Start and the defaults cannot drift apart ---------------------------


def test_defaults_carry_the_whole_skeleton():
    sd = state_defaults(build())
    assert sorted(sd) == ["flags", "game_state", "npcs", "player"]


# The only keys Start and the defaults are allowed to disagree on, and the reason.
# A save written before the stamp existed carries no origin_*; filling it from the
# running build would make it claim to have STARTED there. Absent = unknown = true.
DELIBERATE_DIVERGENCE = {"origin_version", "origin_schema"}


def divergence(twee):
    """Keys where the defaults and :: Start disagree, and what SHOULD disagree.

    A game with no `[project] version` writes null for origin_version in both
    places, so only origin_schema differs there — the expectation is derived from
    what Start actually wrote rather than hardcoded, so both kinds of game are
    checked exactly instead of one being waved through."""
    sd = state_defaults(twee)["game_state"]
    started = start_var(twee, "game_state")
    differ = {k for k in set(sd) | set(started) if sd.get(k) != started.get(k)}
    expected = {k for k in DELIBERATE_DIVERGENCE if started.get(k) is not None}
    return differ, expected


def test_defaults_are_what_start_writes_apart_from_the_documented_divergence():
    """The property the old build could not hold: Start serialized a hand-maintained
    string block while the defaults dict listed three keys, so every new sub-map was
    a silent omission. Both now come off one object.

    Whitelisted, not relaxed — a NEW disagreement fails here even though the two
    known ones are allowed."""
    twee = build()
    sd = state_defaults(twee)
    assert sd["player"] == start_var(twee, "player")
    assert sd["flags"] == start_var(twee, "flags")
    assert sd["npcs"] == start_var(twee, "npcs")
    differ, expected = divergence(twee)
    assert differ == expected, differ


def test_origin_is_unknown_in_the_defaults_and_known_in_start():
    """Both halves. If the defaults ever carried a real origin, every pre-stamp save
    would be relabelled as having started on whatever build first migrated it."""
    twee = build()
    sd = state_defaults(twee)["game_state"]
    started = start_var(twee, "game_state")
    assert sd["origin_schema"] is None and sd["origin_version"] is None
    assert started["origin_schema"] == started["last_schema"]
    assert isinstance(started["origin_schema"], int)


def test_the_build_stamps_its_own_identity():
    """setup.buildSchema must equal what SugarCube writes into the save, or the
    load hook compares a save against a number no save ever carried."""
    twee = build()
    stamped = re.search(r"Config\.saves\.version = (\d+);", twee).group(1)
    assert re.search(r"setup\.buildSchema = (\d+);", twee).group(1) == stamped
    assert start_var(twee, "game_state")["origin_schema"] == int(stamped)


def test_the_load_hook_records_and_never_refuses():
    """LO's call: a schema mismatch is logged, not rejected. A throw inside
    Config.saves.onLoad aborts the load with UI.alert — that is the reject
    mechanism, and it must stay unused until someone decides otherwise."""
    twee = build()
    hook = twee.split("Config.saves.onLoad = function (save)", 1)[1]
    hook = hook[: hook.index("\n}};") if "\n}};" in hook else hook.index("\n};")]
    assert "throw" not in hook, "the load hook must not refuse a save"
    assert "State.variables" not in hook, (
        "onLoad runs before State.unmarshalForSave — writing there edits the "
        "pre-load state and is silently discarded"
    )
    assert "setup.saveOrigin" in hook


def test_bookkeeping_maps_are_present_in_a_bare_game():
    """A game with no optional system still needs the engine's own maps, or the
    backfill has nothing to restore them from."""
    gs = state_defaults(build())["game_state"]
    for key in (
        "quests",
        "bank",
        "fast_jobs",
        "time_state",
        "media_cycle",
        "scheduled",
    ):
        assert key in gs, key


@needs_rich
def test_every_optional_sub_map_reaches_the_defaults():
    """The regression this whole change exists for. A game with the phone on must
    put `phone` in the defaults, not only in Start — otherwise a save from before
    the phone shipped never gets one."""
    twee = build(RICH)
    sd = state_defaults(twee)
    assert "phone" in sd["game_state"]
    assert "inventory" in sd["game_state"]
    assert "wardrobe" in sd["player"] and "equipped" in sd["player"]
    assert sd["player"] == start_var(twee, "player")
    differ, expected = divergence(twee)
    assert differ == expected, differ


VERSIONED = "games/mrs_vance/toml_phases/7_final_game.toml"


@pytest.mark.skipif(not os.path.exists(VERSIONED), reason="mrs_vance TOML not present")
def test_a_declared_version_is_recorded_and_still_unknown_in_the_defaults():
    """The other half of the divergence, which the version-less fixtures cannot
    show: when `[project] version` exists, Start records it as the origin and the
    defaults still say unknown."""
    twee = build(VERSIONED)
    started = start_var(twee, "game_state")
    sd = state_defaults(twee)["game_state"]
    assert started["origin_version"], "game declares a version; Start dropped it"
    assert started["last_version"] == started["origin_version"]
    assert sd["origin_version"] is None
    differ, expected = divergence(twee)
    assert differ == expected == DELIBERATE_DIVERGENCE, differ


# --- Node: run the migration --------------------------------------------------


def run_backfill(twee, saves, tmp_path, mutate=""):
    """Execute the generated backfill over each save in `saves`; return them after.

    `mutate` is JS run between the two backfill passes, used to prove idempotence
    and to prove a migrated save does not alias the shared defaults.
    """
    program = textwrap.dedent(
        """
        var setup = {};
        setup.stateDefaults = __DEFAULTS__;
        __BACKFILL__
        var saves = __SAVES__;
        saves.forEach(function (sv) { setup.backfillStateDefaults(sv); });
        __MUTATE__
        console.log(JSON.stringify({
            saves: saves,
            defaults: setup.stateDefaults
        }));
        """
    )
    program = (
        program.replace("__DEFAULTS__", json.dumps(state_defaults(twee)))
        .replace("__BACKFILL__", backfill_source(twee))
        .replace("__SAVES__", json.dumps(saves))
        .replace("__MUTATE__", mutate)
    )
    script = tmp_path / "backfill.js"
    script.write_text(program, encoding="utf-8")
    out = subprocess.run(
        ["node", str(script)], capture_output=True, text=True, check=False
    )
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def old_save(twee, drop_game_state=(), drop_player=(), **overrides):
    """A save as an EARLIER release would have written it: the current skeleton with
    keys the older build did not have removed, plus whatever the player earned."""
    sd = state_defaults(twee)
    sv = json.loads(json.dumps(sd))  # deep copy
    sv["game_state"] = dict(sv["game_state"])
    for k in drop_game_state:
        sv["game_state"].pop(k, None)
    for k in drop_player:
        sv["player"].pop(k, None)
    for k, v in overrides.items():
        sv[k] = v
    return sv


@needs_node
def test_a_sub_map_the_old_release_never_had_is_restored(tmp_path):
    twee = build()
    sv = old_save(twee, drop_game_state=("fast_jobs", "bank"))
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["game_state"]["fast_jobs"] == {"xp": 0, "cooldowns": {}}
    assert got["game_state"]["bank"] == {"balance": 0}


@needs_node
def test_a_new_key_inside_an_existing_sub_map_is_restored(tmp_path):
    """Depth 2 on $game_state. A release that adds `cooldowns` to an already-shipped
    `fast_jobs` must reach the players who already have `fast_jobs`."""
    twee = build()
    sv = old_save(twee)
    del sv["game_state"]["fast_jobs"]["cooldowns"]
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["game_state"]["fast_jobs"]["cooldowns"] == {}


@needs_node
def test_an_earned_value_is_never_overwritten(tmp_path):
    """The single property that makes this safe to run on every passage."""
    twee = build()
    sv = old_save(twee)
    sv["game_state"]["bank"]["balance"] = 500
    sv["game_state"]["visited_locations"] = ["kitchen", "yard"]
    sv["player"]["core_traits"] = dict(sv["player"]["core_traits"])
    first_trait = sorted(sv["player"]["core_traits"])[0]
    sv["player"]["core_traits"][first_trait] = 99
    sv["player"]["name"] = "Renamed"
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["game_state"]["bank"]["balance"] == 500
    assert got["game_state"]["visited_locations"] == ["kitchen", "yard"]
    assert got["player"]["core_traits"][first_trait] == 99
    assert got["player"]["name"] == "Renamed"


@needs_node
def test_an_emptied_list_is_not_re_seeded(tmp_path):
    """Arrays are never merged at any depth. A player who cleared their scheduled
    queue must not find it refilled."""
    twee = build()
    sv = old_save(twee)
    sv["game_state"]["scheduled"] = []
    sv["game_state"]["visited_nodes"] = ["node_a"]
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["game_state"]["scheduled"] == []
    assert got["game_state"]["visited_nodes"] == ["node_a"]


@needs_node
def test_a_new_player_trait_appears(tmp_path):
    """The behaviour that already existed, pinned so the rewrite kept it."""
    twee = build()
    sv = old_save(twee)
    trait = sorted(sv["player"]["core_traits"])[0]
    del sv["player"]["core_traits"][trait]
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert trait in got["player"]["core_traits"]


@needs_node
@needs_rich
def test_wardrobe_is_not_filled_into(tmp_path):
    """⚠️ The asymmetry. $player is filled at TOP LEVEL ONLY. `wardrobe` is an
    id -> garment map, so a depth-2 fill would silently hand back a starting garment
    the player sold, discarded or was stripped of. `equipped` likewise.

    If this goes red because someone unified the merge depth, the fix is to restore
    the asymmetry, not to relax the test."""
    twee = build(RICH)
    sd = state_defaults(twee)
    if not sd["player"].get("wardrobe"):
        pytest.skip("game has no starting garments to lose")
    sv = old_save(twee)
    sold = sorted(sv["player"]["wardrobe"])[0]
    del sv["player"]["wardrobe"][sold]
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert (
        sold not in got["player"]["wardrobe"]
    ), "backfill re-granted a garment the player no longer owns"


@needs_node
@needs_rich
def test_the_phone_reaches_a_save_written_before_it_shipped(tmp_path):
    twee = build(RICH)
    sv = old_save(
        twee,
        drop_game_state=("phone", "inventory"),
        drop_player=("wardrobe", "equipped"),
    )
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["game_state"]["phone"]["matches"] == {}
    assert got["game_state"]["inventory"] == {}
    assert "wardrobe" in got["player"] and "equipped" in got["player"]


@needs_node
def test_a_whole_new_npc_arrives_and_an_old_one_keeps_what_she_earned(tmp_path):
    twee = build()
    sd = state_defaults(twee)
    if not sd["npcs"]:
        pytest.skip("fixture has no NPCs")
    who = sorted(sd["npcs"])[0]
    sv = old_save(twee)
    kept_trait = sorted(sv["npcs"][who]["core_traits"])[0]
    sv["npcs"][who]["core_traits"][kept_trait] = 77
    got = run_backfill(twee, [sv], tmp_path)["saves"][0]
    assert got["npcs"][who]["core_traits"][kept_trait] == 77
    # and a save that predates her entirely gets her whole record
    sv2 = old_save(twee)
    del sv2["npcs"][who]
    got2 = run_backfill(twee, [sv2], tmp_path)["saves"][0]
    assert got2["npcs"][who]["core_traits"] == sd["npcs"][who]["core_traits"]


@needs_node
def test_running_it_twice_changes_nothing(tmp_path):
    """It fires on EVERY passage, so a second pass must be a no-op."""
    twee = build()
    sv = old_save(twee, drop_game_state=("bank",))
    once = run_backfill(twee, [sv], tmp_path)["saves"][0]
    twice = run_backfill(twee, [once], tmp_path)["saves"][0]
    assert once == twice


@needs_node
def test_a_fresh_save_is_untouched(tmp_path):
    twee = build()
    sv = old_save(twee)
    assert run_backfill(twee, [json.loads(json.dumps(sv))], tmp_path)["saves"][0] == sv


@needs_node
def test_a_migrated_save_does_not_alias_the_shared_defaults(tmp_path):
    """setup.stateDefaults is one object shared by every save in the session. If the
    backfill assigned a default sub-map by reference, the first player action would
    edit the template that every later backfill reads from — and a second save would
    inherit the first save's state."""
    twee = build()
    a = old_save(twee, drop_game_state=("bank",))
    b = old_save(twee, drop_game_state=("bank",))
    out = run_backfill(
        twee, [a, b], tmp_path, mutate="saves[0].game_state.bank.balance = 999;"
    )
    assert out["saves"][0]["game_state"]["bank"]["balance"] == 999
    assert (
        out["saves"][1]["game_state"]["bank"]["balance"] == 0
    ), "saves alias each other"
    assert (
        out["defaults"]["game_state"]["bank"]["balance"] == 0
    ), "defaults were mutated"


# --- Node: the provenance stamp -------------------------------------------------


def passage_provenance_block(twee):
    """The `last_*` stamp exactly as the :passagestart handler ships it.

    Lifted from the built game rather than retyped, so the test cannot pass against
    a snippet that no longer matches what runs."""
    head = "if (sv.game_state && sv.game_state.last_schema !== setup.buildSchema) {"
    body = twee[twee.index(head) :]
    depth, j = 0, body.index("{")
    while True:
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    return body[: j + 1]


def run_passage(twee, saves, tmp_path):
    """Backfill, then the provenance stamp — the :passagestart order."""
    build_ver = json.loads(re.search(r"setup\.buildVersion = (.+?);", twee).group(1))
    build_schema = int(re.search(r"setup\.buildSchema = (\d+);", twee).group(1))
    program = """
        var setup = {};
        setup.stateDefaults = %s;
        setup.buildVersion = %s;
        setup.buildSchema = %d;
        %s
        var saves = %s;
        saves.forEach(function (sv) {
            setup.backfillStateDefaults(sv);
            %s
        });
        console.log(JSON.stringify(saves));
    """ % (
        json.dumps(state_defaults(twee)),
        json.dumps(build_ver),
        build_schema,
        backfill_source(twee),
        json.dumps(saves),
        passage_provenance_block(twee),
    )
    script = tmp_path / "provenance.js"
    script.write_text(program, encoding="utf-8")
    out = subprocess.run(
        ["node", str(script)], capture_output=True, text=True, check=False
    )
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


@needs_node
def test_a_save_from_before_the_stamp_is_marked_unknown_not_relabelled(tmp_path):
    """⚠️ The failure the divergence exists to prevent. Every save in the wild today
    predates this stamp. If the defaults carried a real origin, the first launch of
    the next release would quietly rewrite all of them to say they started there —
    and the provenance would be worse than useless, because it would look right."""
    twee = build()
    sv = old_save(twee, drop_game_state=("origin_version", "origin_schema"))
    got = run_passage(twee, [sv], tmp_path)[0]
    assert got["game_state"]["origin_schema"] is None
    assert got["game_state"]["origin_version"] is None


@needs_node
def test_an_older_origin_survives_and_the_running_build_is_stamped(tmp_path):
    """ "Started on X, now running Y" — the pair a bug report needs."""
    twee = build()
    sv = old_save(twee)
    sv["game_state"]["origin_version"] = "0.1.4"
    sv["game_state"]["origin_schema"] = 111
    sv["game_state"]["last_version"] = "0.1.4"
    sv["game_state"]["last_schema"] = 111
    got = run_passage(twee, [sv], tmp_path)[0]["game_state"]
    assert got["origin_version"] == "0.1.4" and got["origin_schema"] == 111
    assert got["last_schema"] == int(
        re.search(r"setup\.buildSchema = (\d+);", build()).group(1)
    )


@needs_node
def test_a_fresh_save_on_the_current_build_is_not_dirtied(tmp_path):
    """The stamp is guarded on a difference; a same-build passage must write nothing."""
    twee = build()
    sv = old_save(twee)
    assert run_passage(twee, [json.loads(json.dumps(sv))], tmp_path)[0] == sv


# --- the seam is actually wired up ----------------------------------------------


def test_the_backfill_runs_on_every_passage():
    """A correct migration that nothing calls is not a migration.

    Anchored on the handler REGISTRATION, not the first mention of the event —
    `:passagestart` is named in three comments before the handler is bound."""
    twee = build()
    handler = twee.split("$(document).on(':passagestart'", 1)[1][:6000]
    assert "setup.backfillStateDefaults" in handler
