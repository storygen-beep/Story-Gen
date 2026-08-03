"""Content-band derivation — apps/common/media_band.py.

Two groups of tests carry the weight:

⚠ `test_the_captivity_set_is_not_sfw` and `test_the_nude_stills_are_not_sfw` pin the
  22 vesper slots that a path-only rule sends to the SFW bucket. They are the whole
  reason this module scans descriptions at all. If they go red, clicking "SFW" on the
  review page shows gangbang clips.

⚠ `test_cocky_is_not_a_cock` and friends pin the false positives a looser word list
  produced on the first pass. Both are real shipped vesper captions.
"""
import pytest

from apps.common.media_band import (
    NSFW_BANDS,
    band_for,
    band_for_entry,
    is_nsfw,
)


# --------------------------------------------------------------------------
# precedence
# --------------------------------------------------------------------------

def test_an_authored_tier_beats_every_other_signal():
    """The override exists so a human can correct a derived band without renaming."""
    band, source = band_for("scenes/quiet_office.jpg", tier="t5")
    assert (band, source) == ("explicit", "authored")


def test_an_authored_tier_can_also_cool_a_path_down():
    """`base` — not `t2` — is what cools a slot all the way to clean; see the tease tests."""
    band, source = band_for("sex/misfiled_establishing_shot.jpg", tier="base")
    assert (band, source) == ("clean", "authored")


# --------------------------------------------------------------------------
# ⚠️ a tease is never SFW — LO, 2026-08-04
# --------------------------------------------------------------------------

@pytest.mark.parametrize("tier", ["t2", "t3", "t4"])
def test_every_tease_tier_is_nsfw(tier):
    """Any authored tier means the author put the beat on the sexual ladder.

    This deliberately diverges from find-media's SFW_TIERS, which lists t2/t3 as SFW —
    a set written as if SFW meant *wayfinding*. `rung_renner_tease_t2` sits on a
    repeatable hub gated `corruption >= 0` with no ceiling: clickable from the first
    minute of the game to the last. Calling that SFW is what let it ship as one
    unrotated clip.
    """
    band, source = band_for(f"scenes/rung_tease_{tier}.webm")
    assert (band, source) == ("borderline", "tier_suffix")
    assert is_nsfw(band)


@pytest.mark.parametrize("tier,expected", [
    ("base", "clean"), ("location", "clean"),
    ("t2", "borderline"), ("t3", "borderline"), ("t4", "borderline"),
    ("t5", "explicit"), ("t8", "explicit"),
])
def test_the_whole_tier_vocabulary_maps(tier, expected):
    """Only base / location / no-suffix is clean. Pins the full map in one place."""
    assert band_for("scenes/x.webm", tier=tier)[0] == expected


def test_an_untiered_non_sexual_path_is_still_clean():
    """The rule is about authored tiers, not a blanket promotion of everything."""
    assert band_for("locations/atrium.jpg") == ("clean", "default")


def test_an_unknown_tier_falls_through_rather_than_crashing():
    band, source = band_for("sex/x.webm", tier="banana")
    assert (band, source) == ("explicit", "folder")


def test_tier_suffix_beats_folder():
    band, source = band_for("sex/kiss_t4.webm")
    assert (band, source) == ("borderline", "tier_suffix")


def test_folder_beats_description():
    """A file under sex/ is explicit whatever its caption says."""
    band, source = band_for("sex/x.webm", description="a quiet office at night")
    assert (band, source) == ("explicit", "folder")


def test_a_pool_dir_ending_at_the_tier_still_matches():
    """`sex/brothel_oral_t5` has no extension — the suffix regex needs $, not just [._/]."""
    band, source = band_for("sex/brothel_oral_t5")
    assert (band, source) == ("explicit", "tier_suffix")


@pytest.mark.parametrize("path", [
    "sex/x_t5.webm",
    "videos/sex/x_t5.webm",   # serve_path form
    "/videos/sex/x_t5.webm",
])
def test_both_path_prefix_forms_normalise(path):
    """`file` is bare and `serve_path` is prefixed; a `"/sex/" in p` test misses the
    bare form, which is exactly how a first pass undercounted explicit slots 50/111."""
    assert band_for(path)[0] == "explicit"


def test_a_bare_sex_path_is_explicit_by_folder():
    assert band_for("sex/cell_frame.webm") == ("explicit", "folder")


def test_a_folder_merely_containing_sex_is_not_the_sex_root():
    """Root-segment match, not substring: `scenes/` must not inherit `sex/`'s band."""
    assert band_for("scenes/unisex_locker_room.jpg")[0] == "clean"


# --------------------------------------------------------------------------
# ⚠ the 22 slots a path-only rule gets wrong
# --------------------------------------------------------------------------

CAPTIVITY = [
    ("scenes/cell_turns_the_queue.webm",
     "line of men waiting their turn while a woman kneels used on the floor"),
    ("scenes/cell_turns_the_read_out.jpg",
     "used woman covered in cum kneeling aftermath gangbang exhausted"),
    ("scenes/cell_stutter_bastien_leans_in.webm",
     "woman used from behind while a clothed man sits close watching, not participating"),
    ("scenes/cell_he_does_not_stop_the_read_out_the_break.webm",
     "spent limp woman still being used by a group past collapse, dazed"),
]


@pytest.mark.parametrize("path,desc", CAPTIVITY)
def test_the_captivity_set_is_not_sfw(path, desc):
    """These live under scenes/ with no tier suffix. A path-only rule calls them clean."""
    band, source = band_for(path, description=desc)
    assert band == "explicit", f"{path} banded {band}"
    assert source == "description"
    assert is_nsfw(band)


def test_a_nude_subject_with_no_act_is_nudity_not_explicit():
    band, source = band_for(
        "scenes/cell_inventory_the_order.jpg",
        description="clothed man sitting in chair facing naked woman bare concrete room",
    )
    assert (band, source) == ("nudity", "description")
    assert is_nsfw(band)


def test_the_nude_stills_are_not_sfw():
    """12 salvage_session_N.jpg — the caption names a nude subject, the path says nothing."""
    band, source = band_for(
        "scenes/salvage_session_1.jpg",
        description="A broad-shouldered dock hand standing bare-chested by an industrial "
                    "work-cradle in a dim dry-dock, a naked woman waiting.",
        search_queries=["shirtless man standing workshop", "nude woman industrial dry dock dim"],
    )
    assert (band, source) == ("nudity", "description")


@pytest.mark.parametrize("state,expected", [
    ("naked", "nudity"),
    ("topless", "nudity"),
    ("bottomless", "nudity"),
    ("underwear", "borderline"),
    ("default", "clean"),
])
def test_player_portrait_states_band_structurally(state, expected):
    """No authoring needed: the engine already parses these state keys, so the band is
    structural. This also contradicts game_review.py's old comment that portraits are
    'always SFW regardless of how explicit the game is'."""
    band, source = band_for(f"portraits/wren_{state}.jpg", portrait_state=state)
    assert band == expected
    if expected != "clean":
        assert source == "portrait_state"


def test_an_npc_face_has_no_state_and_stays_clean():
    assert band_for("mercer.jpg", portrait_state=None) == ("clean", "default")


# --------------------------------------------------------------------------
# ⚠ false positives a looser word list produced — both are real vesper captions
# --------------------------------------------------------------------------

def test_a_stripped_hull_is_not_undressing():
    band, _ = band_for(
        "scenes/kess_berth_intro.jpg",
        description="A male ship-breaker on a work-cradle inside a drained dry-dock, "
                    "cutting-torch in hand, a stripped hull behind him.",
        search_queries=["man welder cutting torch industrial night"],
    )
    assert band == "clean"


def test_down_on_one_knee_is_not_kneeling_used():
    band, _ = band_for(
        "scenes/salvage_waterfront_dawn.jpg",
        description="A woman down on one knee on wet dock boards at dawn, one leg not "
                    "answering under her.",
        search_queries=["woman kneeling dock dawn grey", "figure collapsed pier morning"],
    )
    assert band == "clean"


def test_cocky_is_not_a_cock():
    """Word boundaries, not substrings — `cocky` is a shipped vesper caption."""
    band, _ = band_for("scenes/x.jpg", description="A young man leaning cocky against a cradle")
    assert band == "clean"


def test_analyst_is_not_anal():
    """vesper's cover story is a junior-analyst kit. `\\banal\\b` must not fire on it."""
    band, _ = band_for("clothing/cover_analyst.jpg", description="Junior-analyst kit (dress)")
    assert band == "clean"


def test_a_brothel_setting_alone_is_not_explicit():
    """The madam sits in a chair with a ledger. Setting is not an act."""
    band, _ = band_for(
        "scenes/rue_madam.jpg",
        description="A composed older woman in a dim red-lit brothel parlor, watching the "
                    "room from a worn velvet chair, a ledger and a cash box at her elbow.",
    )
    assert band == "clean"


# --------------------------------------------------------------------------
# entry adapter + contract
# --------------------------------------------------------------------------

def test_band_for_entry_reads_the_fields_the_enumerator_already_carries():
    entry = {
        "file": "scenes/cell_turns_the_queue.webm",
        "description": "line of men waiting their turn",
        "search_queries": [],
        "tier": None,
        "portrait_state": None,
    }
    assert band_for_entry(entry) == ("explicit", "description")


def test_band_for_entry_survives_a_bare_entry():
    """Five of the six enumerator categories build entries without tier/portrait_state."""
    assert band_for_entry({"file": "locations/atrium.jpg"}) == ("clean", "default")


def test_only_clean_is_sfw():
    assert not is_nsfw("clean")
    for band in NSFW_BANDS:
        assert is_nsfw(band)


def test_an_empty_path_does_not_crash():
    assert band_for("") == ("clean", "default")
