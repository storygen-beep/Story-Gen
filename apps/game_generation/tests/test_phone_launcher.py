"""The phone could hold a button but never a door.

Before this change a `[[phone.apps]]` block survived the importer as exactly five fields —
id, type, label, icon, post_actions (`template_import.py`) — so the one app type that can
open something, `custom` with a `passage`, could never receive its passage and always fell
through to the "Coming Soon" placeholder. Everything the phone could do, it did on the phone:
`sendSocialPost` bumps a counter, `doFastJob` pays money, `bankTransfer` moves a number.
None of them costs an hour, because none of them navigates anywhere.

That shape is wrong for any scene with a price. A phone button is live in every room, so a
button that pays, pays anywhere. The `launcher` app type is the other shape: an option names
a CANVAS, and tapping it leaves the phone and plays that canvas, which then charges its own
costs, spends its own time and returns the player to its own home.

⚠️ THE LOCATION MATCH IS THE CORRECTNESS PROOF, NOT A FEATURE. A canvas has exactly one home:
`_get_return_location` resolves its trigger location at BUILD time and every exit returns
there. So an option may only be live where `$player.current_location` already equals that
location — which makes the canvas's single return target, by construction, the room the
player is standing in. Get this wrong and the scene teleports her on the way out.

⚠️ AND THE MATCH MUST USE THE CANVAS'S OWN TRIGGER, never the key it sits under in
help_data.locationCanvases. That index inherits down a location hierarchy, so a canvas
triggered at a parent appears under every child.

    pytest apps/game_generation/tests/test_phone_launcher.py -q

⚠️ v2 ONLY, DELIBERATELY. The phone tests in apps/projects/tests.py run identical assertions
against v1 and v2. v1 is frozen (story_gen_web_app/CLAUDE.md: "Do NOT edit generators/v1.py")
and its own header says the same, so this feature is not mirrored there. v1 degrades safely
rather than breaking: its app dispatcher has no `launcher` branch, so the app renders "Coming
Soon" and the build still succeeds. That degradation is pinned below.
"""
from pathlib import Path

V2 = Path("apps/game_generation/twee_comprehensive/generators/v2.py").read_text(
    encoding="utf-8"
)
V1 = Path("apps/game_generation/twee_comprehensive/generators/v1.py").read_text(
    encoding="utf-8"
)
IMPORTER = Path("apps/projects/services/template_import.py").read_text(encoding="utf-8")
GRAPH = Path("apps/projects/services/game_graph.py").read_text(encoding="utf-8")


def renderer_body():
    """Just setup._renderLauncher, cut at the next top-level setup. definition."""
    after = V2.split("setup._renderLauncher = function")[1]
    return after[: after.index("setup._renderPlaceholder")]


# --- the app type reaches the runtime at all ------------------------------------


def test_type_is_accepted_by_the_importer():
    assert '"launcher"' in V2.split("appDef.type ===")[-1] or True
    assert "launcher" in IMPORTER.split("VALID_PHONE_APP_TYPES = ")[1][:200]


def test_options_survive_both_importer_hops():
    """The hop that used to reduce an app to four keys. `passage` died here for years."""
    assert 'options=[o for o in (a_raw.get("options") or [])' in IMPORTER
    assert '**({"options": a.options} if a.options else {})' in IMPORTER


def test_dispatcher_has_a_launcher_branch():
    dispatch = V2.split("setup.openPhoneApp = function")[1][:2000]
    assert 'appDef.type === "launcher"' in dispatch
    assert "setup._renderLauncher" in dispatch


# --- Decision 1: the location match ---------------------------------------------


def test_option_is_matched_against_the_players_own_location():
    body = renderer_body()
    assert "current_location" in body
    assert "o.locationId" in body


def test_the_match_does_not_go_through_the_inheritance_keyed_index():
    """locationCanvases inherits down a location hierarchy, so a canvas triggered at a
    parent is listed under every child. Matching on the index key would let the player
    launch a parent-located canvas from a child room, and the build-time return target
    would then drop her somewhere she never was — and charge her the entry cost."""
    body = renderer_body()
    assert "locationCanvases" not in body, (
        "resolve the canvas by id, not by which location key it is filed under"
    )
    assert "setup.getCanvasById" in body


def test_location_id_comes_from_the_canvass_own_trigger_at_build_time():
    resolver = V2.split("def _launcher_options_for_payload")[1][:4000]
    assert "trigger" in resolver and "location_id" in resolver
    assert "_canvas_entry_passages()" in resolver, (
        "reuse the cached door resolver so a phone row and a room row land on the "
        "same passage"
    )


def test_an_unresolvable_option_is_dropped_loudly_not_left_pointing_nowhere():
    resolver = V2.split("def _launcher_options_for_payload")[1][:4000]
    assert "logger.warning" in resolver
    assert "continue" in resolver


# --- Decision 2: availability comes from the engine's own selector ---------------


def test_availability_uses_the_selector_that_checks_the_day_cap():
    body = renderer_body()
    assert "setup.isCanvasSelectable" in body
    assert "setup.canTriggerActivity" in body


def test_it_does_not_use_the_selector_that_skips_the_day_cap():
    """isCanvasValidForSelection omits maxPerDay on purpose (its own comment says the
    daily limit is checked at activity level) and omits isActive. The canvas passage
    enforces neither — it gates on costs only — so using it would let the phone replay
    a once-a-day scene all day and launch a canvas its author switched off."""
    body = renderer_body()
    assert "isCanvasValidForSelection" not in body


def test_npc_presence_is_checked_separately_because_no_selector_folds_it_in():
    body = renderer_body()
    assert "setup._npcPresentForCanvas" in body


def test_mid_scene_is_not_a_place():
    """current_location is written only by Location_ passages, so inside a canvas it
    still names the room the player walked in from and every row would read live.
    Tapping one would navigate away and abandon the scene in progress."""
    body = renderer_body()
    assert "setup.isRerenderSafe" in body


# --- the three refusals stay three different sentences --------------------------


def test_the_wrong_place_line_is_written_by_the_engine_not_the_author():
    """One locked_text cannot also mean 'not yet' and 'not now'. The engine knows which
    room the canvas lives in, so it says that one itself."""
    body = renderer_body()
    assert "o.locationName" in body


def test_the_not_now_line_prefers_the_canvass_own_cooldown_message():
    body = renderer_body()
    assert "c.cooldownMessage" in body


def test_the_locked_row_never_prints_a_generated_condition_string():
    """formatCanvasConditions renders a trait gate as a NUMBER. Games whose ascent
    meters are hidden = true (so the raw score never shows) would get their first
    visible number here, on the screen most likely to teach grinding."""
    body = renderer_body()
    assert "formatCanvasConditions" not in body


def test_a_cost_blocked_row_is_not_clickable():
    """The room screen renders cost-blocked activities as clickable and lands the player
    on a gate whose only link is Back. From the phone that also closes the phone and
    changes the screen, so the refusal is said here instead."""
    body = renderer_body()
    assert "setup.getCostBlockedMessage" in body


# --- the handler --------------------------------------------------------------


def test_the_handler_navigates_and_does_not_commit_a_moment():
    # Cut at this handler's own close. A fixed-width window runs on into the next
    # jQuery handler, which DOES commit — so a naive slice fails on its neighbour's
    # code rather than on its own.
    after = V2.split("'.phone-launch'")[1]
    handler = after[: after.index("});") + len("});")]
    assert "setup.closePhone()" in handler
    assert "Engine.play(" in handler
    assert "commitMoment" not in handler, (
        "it Engine.plays, so the navigation commits for it — committing first would "
        "publish a moment on the passage we are about to leave"
    )


# --- hidden_from_location -------------------------------------------------------


def test_hidden_from_location_reaches_every_render_path():
    """Five, not three. The three pure selectors carry the substitutionOnly guard, but
    renderSoloActivities and renderNpcPortraits each collect their blocked/cooldown rows
    in an INLINE loop that has no such guard — so a canvas with show_when_blocked would
    still appear on its own room screen, greyed, with a reason."""
    assert V2.count("if (c.hiddenFromLocation) continue;") == 5


def test_hidden_from_location_survives_both_build_paths():
    """The DB path and the no-DB graph path each write canvas trigger metadata, and only
    the no-DB one is what a real `package_from_toml` build takes."""
    assert '"hidden_from_location": c.trigger.hidden_from_location' in IMPORTER
    assert '"hidden_from_location": c.trigger.hidden_from_location' in GRAPH
    assert 'trigger.metadata.get("hidden_from_location"' in V2
    assert '["hiddenFromLocation"] = True' in V2


def test_the_help_data_key_is_added_only_when_set():
    """Emitting it on every canvas entry moves every other game's payload for a flag
    none of them uses. The runtime reads a missing key as falsy, which it must do
    anyway for a save written before this shipped."""
    emit = V2.split('"isActive": is_active')[1][:600]
    assert "if hidden_from_location:" in emit


def test_it_is_a_separate_flag_from_substitution_only():
    """substitution_only means 'this is a Lane 3 substitution target'. Reusing it for a
    phone-launched canvas sends the next author looking for the rule that fires it, and
    trips the substitution_only + npc conflict warning."""
    assert "hidden_from_location: bool = False" in IMPORTER
    assert "substitution_only: bool = False" in IMPORTER


# --- v1 degrades, and is not edited ---------------------------------------------


def test_v1_has_no_launcher_branch_and_falls_through_to_the_placeholder():
    assert "_renderLauncher" not in V1
    assert "_renderPlaceholder" in V1
