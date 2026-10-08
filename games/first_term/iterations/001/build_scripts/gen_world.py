"""Emit games/first_term/toml_phases/1_metadata_and_locations.toml from world_data + people_data."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from tomlw import *
from world_data import LOCATIONS, children
from people_data import PEOPLE

OUT = sys.argv[1]
PHASES = os.path.dirname(OUT)
import tomllib, glob

def _walk_flags(o, acc):
    if isinstance(o, dict):
        for k, val in o.items():
            if k in ("flag", "flag_key") and isinstance(val, str):
                acc.add(val)
            else:
                _walk_flags(val, acc)
    elif isinstance(o, list):
        for i in o:
            _walk_flags(i, acc)

FLAGS = set()
for f in sorted(glob.glob(os.path.join(PHASES, "*.toml"))):
    b = os.path.basename(f)
    if b.startswith("1_") or b.startswith("7_"):
        continue
    try:
        _walk_flags(tomllib.load(open(f, "rb")), FLAGS)
    except Exception as e:
        print("WARN cannot parse", b, e)
for loc in LOCATIONS:
    if loc.get("hidden_until"):
        FLAGS.add(loc["hidden_until"])
for p in PEOPLE:
    _walk_flags(p["schedules"], FLAGS)
FLAGS -= {"rent_carried"}          # the engine declares its own (template_import.py:8947)
L = []
w = L.append

w("""# =============================================================================
# First Term — 1 · the player, the map and the people
#
# Built 2026-10-08 from the signed sheets: sheets/places/*.md (31 places; the corner
# shop and the men's toilet are not in 0.1, SP7), sheets/people/*.md (21 people) and
# the ledger (board.locations, board.characters). The schedules keep each sheet's row
# order, because the engine takes the first matching row (v2.py:4304-4318).
#
# ⚠️ [[npcs]] and their [[npcs.schedules]] must stay in THIS file (TOML scoping).
# =============================================================================

[player]
id   = "player"
name = "Ella"
customizable = true
description  = "You, 18. First term of college, still living at home."

flag_keys = FLAGKEYS

[player.core_traits]
# her two stages (SP2 §1): 0-100, the stages start at 0, 20, 40, 60 and 80
corruption    = 0
exhibitionism = 0
# the needs (board.needs): energy is spent, hygiene falls a little each night
energy  = 100
hygiene = 80
money   = 0
# the talk tracks and her other meters (board.meters)
campus_talk     = 0
laura_suspicion = 0
followers       = 0
intelligence    = 0
grade_psych     = 50
grade_art       = 50
grade_business  = 50
grade_bio       = 50
complaints      = 0
paid_full_streak = 0
drinks_tonight  = 0
# the curfew: days left (set 7 when Laura grounds her; one off each night)
curfew_days     = 0
# the seven step counters (board.characters[].ladder.counter)
ryan_step  = 0
laura_step = 0
mark_step  = 0
tom_step   = 0
zoe_step   = 0
hale_step  = 0
jake_step  = 0

[player.trait_decay]
hygiene = 10

[[player.customization_fields]]
id      = "name"
type    = "text"
label   = "Your name"
default = "Ella"

[[player.customization_fields]]
id      = "nickname"
type    = "text"
label   = "What Ryan calls you"
default = "El"
""")

L[0] = L[0].replace("flag_keys = FLAGKEYS", "flag_keys = " + vlist(sorted(FLAGS)))

# ── locations ──
w("\n# ── the map: the street is the ground, the only root (board.map, the-map.md R0, R3) ──\n")
for loc in LOCATIONS:
    w("\n[[locations]]")
    w(f"id          = {q(loc['id'])}")
    w(f"name        = {q(loc['name'])}")
    w(f"kind        = {q(loc['kind'])}")
    w(f"description = {q(loc['description'])}")
    w(f"image       = {q('locations/' + loc['id'] + '.jpg')}")
    w(f"image_search_queries = [{q(loc['name'].lower())}]")
    if loc.get("entry_from"):
        w(f"entry_from  = {q(loc['entry_from'])}")
    kids = children(loc["id"])
    w(f"navigation_order = {v(kids)}")
    if loc.get("costs"):
        w(f"costs = {v(loc['costs'])}")
    if loc.get("hours"):
        w(f"hours = {v(loc['hours'])}")
    if loc.get("closed_text"):
        w(f"closed_text = {q(loc['closed_text'])}")
    if loc.get("hidden_until"):
        w(f"hidden_until = {{ flag = {q(loc['hidden_until'])} }}")
    if loc.get("rules"):
        w("clothing_rules = [")
        for r in loc["rules"]:
            w(f"  {v(r)},")
        w("]")
    if loc.get("variants"):
        w("description_variants = [")
        for c, t in loc["variants"]:
            w(f"  {{ conditions = {v(c)}, text = {q(t)} }},")
        w("]")
    if loc.get("door"):
        d = loc["door"]
        w("\n[locations.door]")
        w(f"description = {q(d['description'])}")
        w(f"no_answer   = {q(d['no_answer'])}")
        for o in d["options"]:
            w("\n[[locations.door.options]]")
            w(f"text = {q(o['text'])}")
            if o.get("conditions"):
                w(f"conditions = {v(o['conditions'])}")
            if o.get("show_when_locked"):
                w("show_when_locked = true")
            if o.get("locked_text"):
                w(f"locked_text = {q(o['locked_text'])}")
            w(f"goes_to = {v(o['goes_to'])}")

# ── people ──
w("\n\n# ── the people: 21, everyone 18 or older (want.cast[].age, SP5) ──")
for p in PEOPLE:
    w("\n[[npcs]]")
    w(f"id           = {q(p['id'])}")
    w(f"name         = {q(p['name'])}")
    w(f"description  = {q(p['relationship'] + ' Age ' + str(p['age']) + '.')}")
    w(f"portrait     = {q('portraits/' + p['id'].replace('npc_', '') + '.jpg')}")
    w(f"relationship = {q(p['relationship'])}")
    w(f"role         = {q(p['role'])}")
    if p["tags"]:
        w(f"tags         = {v(p['tags'])}")
    if p["show"]:
        w(f"show_traits  = {v(p['show'])}")
    w(f"core_traits  = {v(p['core'])}")
    for r in p["schedules"]:
        w("\n[[npcs.schedules]]")
        w(f"location   = {q(r['location'])}")
        w(f"weekdays   = {v(r['weekdays'])}")
        w(f"start_time = {q(r['start_time'])}")
        w(f"end_time   = {q(r['end_time'])}")
        w(f"activity   = {q(r['activity'])}")
        if r.get("when"):
            w(f"when       = {v(r['when'])}")

open(OUT, "w").write("\n".join(L) + "\n")
print("wrote", OUT, len(LOCATIONS), "places", len(PEOPLE), "people")
