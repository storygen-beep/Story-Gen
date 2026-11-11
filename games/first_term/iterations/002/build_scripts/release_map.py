"""Which release each part of first_term ships in (DECISIONS 230; LO, 2026-11-11).

The build scripts write every canvas, place and person as before; this file only says which release each one
belongs to, and scripts/release_filter.py cuts a release build to it. Nothing here deletes anything. "2" means
"later": release 2 is planned when release 1 has shipped, and a tag can move then.

What the filter already does on its own, so it is NOT listed here:
  - a ladder step's canvas goes with its step (`release` on board.characters[].ladder.steps in v2_state.json);
  - her meters and the men's `want` are frozen at 0 and moods held at their start (release_page.meters), so
    every scene, line, button and card that needs more is cut;
  - anything left waiting on a flag only cut content sets, at a cut place, or about a cut person, goes too.
"""
import os

# Whole parts that ship later: build_scenes.sh exports FT_PART for the part being generated.
PART_RELEASE = {"zoe": 2, "jake": 2, "dex": 2, "gym": 2, "gossip": 2}

# Canvases cut by name, by prefix (LO: class accidents, exams, café accidents; 2026-11-11).
CANVAS_PREFIX_RELEASE = {"class_acc_": 2, "college_exam_": 2, "cafe_acc_": 2}
# The dean stays for the opening's welcome (college_dean_office), his office hangout with his weekly rows, and the
# notice on his door with his walk-in on it (LO, 2026-11-11, DECISIONS 231: "yess"; "Nope dont cut Dean walk in");
# his warning and calls are later.
CANVAS_RELEASE = {c: 2 for c in ("dean_warning",
                                  # Laura waiting up when she's home late. Release 1 never had it (nothing set
                                  # came_home_late); DECISIONS 231's late_shift fix would bring it in, with its lie
                                  # "I was at Zoe's.", while Laura stays at step 0. It comes with her story.
                                  "laura_02_home_late")}

# Places (LO's minimal school: campus, quad, lecture hall, canteen, library, women's toilet; the gym's rooms).
PLACE_RELEASE = {p: 2 for p in (
    # faculty_floor and dean_office stay: the opening's "Go to campus." walks her to the dean (2_one_shots.toml:587)
    "hale_office", "art_office", "business_office", "ta_office", "college_mens_toilet",
    "zoe_flat", "zoe_apartment", "zoe_kitchen", "zoe_bathroom", "zoe_bedroom", "party_house",
    "gym", "gym_floor", "gym_locker", "gym_sauna", "gym_showers")}

# Release 1's gym: on the street map, locked (LO: "Gym location card locked with the text saying coming soon").
# `gym_open` is set by nothing; release_page.locked names the place, so the gates read it as shut on purpose.
GYM_RELEASE_1 = dict(
    id="gym", name="Gym", entry_from="street", kind="destination", release_until=1,
    entry_conditions={"version": "1.0", "logic": "AND",
                      "items": [{"type": "flag", "subject": "player", "flag_key": "gym_open", "operator": "is_true"}]},
    blocked_message="Coming soon.",
    description="The gym on your street. The door is locked, and the sign on the glass says: Coming soon.")

# People who are not in release 1.
PEOPLE_RELEASE = {p: 2 for p in ("npc_zoe", "npc_jake", "npc_dex", "npc_cocky_guy",
                                 "npc_claire", "npc_kayla")}

# Single schedule rows that ship later, by (person, activity): Laura waiting up goes with laura_02_home_late.
ROWS_LATER = {("npc_laura", "waiting up in the dark hall"): 2}

# People in release 1 only for one scene: their weekly rows ship later. Empty since DECISIONS 231 kept the dean's
# office hangout, which needs his rows.
SCHEDULES_LATER = set()

# The card each person shows once release 1 has nothing more for them (DECISIONS 230; signed by LO, 2026-11-11,
# DECISIONS 231).
# Keyed by person: (the card's line, its terminal line). step_cards() puts one where the release ends.
STOP_CARDS = {
    "npc_ryan": ("Your stepbrother. You met him in the hall, in a towel, on your first morning.",
                 "Ryan's story goes on in the next release."),
    "npc_mark": ("Mark takes the rent at the kitchen table every Sunday.",
                 "Mark's story goes on in the next release."),
    "npc_hale": ("Dr. Hale teaches your Psychology class.",
                 "Dr. Hale's story goes on in the next release."),
    "npc_laura": ("Your mom. She cooks, she worries, she wants this new family to work.",
                  "Laura's story starts in the next release."),
    "npc_tom": ("Tom gave you the job. Your shifts at the café pay the rent.",
                "Tom's story starts in the next release."),
}

# The note at the top of the Quests page, release 1 only (signed by LO, 2026-11-11, DECISIONS 231).
RELEASE_NOTE = {
    "group": "story_goals", "priority": 30, "release_until": 1,
    "text": "This is release 1 of First Term.",
    "tip": ("Meet the family, find a job, pay Mark on Sunday. Her stats and the people around her stay where they "
            "start for now. They start moving in the next release."),
    "when": [{"flag": "opening_done", "op": "is_true"}],
}


def canvas_release(cid):
    """The release a canvas ships in, or None for release 1 (untagged)."""
    if cid in CANVAS_RELEASE:
        return CANVAS_RELEASE[cid]
    for prefix, r in CANVAS_PREFIX_RELEASE.items():
        if cid.startswith(prefix):
            return r
    return PART_RELEASE.get(os.environ.get("FT_PART", ""))


def part_release():
    return PART_RELEASE.get(os.environ.get("FT_PART", ""))
