"""gymkit.py: what counts as gym clothes, and checked in today (the street gym, DECISIONS 225; sheets/places/gym.md).

Shared by college.py (Work out), jake.py (training with him) and dex.py (sessions with Dex): the part scripts run as
separate processes, so the rule lives here once.
"""
from canv import GC, P
from tomlw import cond, flag

TOP_ON = {"type": "clothing_slot", "slot": "top", "operator": "equipped"}
SPORTS_ONLY = [{"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"},
               {"type": "clothing_slot", "slot": "top", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}]

# Gym clothes to work out (LO, 2026-11-10, DECISIONS 225: "Gym clothes are to be required for workouts"; gym.md): a gym
# bottom (track pants, leggings, tiny shorts, sheer leggings) and a gym top (the tank, a T-shirt, or the sports bra with
# nothing over it). Conditions have no nested OR, so each is the AND of what it is not: no dress, a bottom on that is
# none of the other bottoms, and either a top on that is none of the other tops (GYM_A) or the sports bra alone (GYM_B).
_ITEM_OFF = lambda i: {"type": "clothing_item", "item_id": i, "operator": "unequipped"}
BOTTOM_OK = [{"type": "clothing_slot", "slot": "dress", "operator": "unequipped"},
             {"type": "clothing_slot", "slot": "bottom", "operator": "equipped"},
             *[_ITEM_OFF(i) for i in ("jeans", "sleep_shorts", "short_skirt", "micro_shorts", "split_skirt")]]
NO_OTHER_TOP = [_ITEM_OFF(i) for i in ("thin_top", "low_top", "crop_top")]
GYM_A = BOTTOM_OK + [TOP_ON] + NO_OTHER_TOP
GYM_B = BOTTOM_OK + SPORTS_ONLY
GYM_KITS = (GYM_A, GYM_B)
CHECKED_IN = flag("gym_in_today")   # the desk (gym.py): her card or a day pass, today
JEANS = {"type": "clothing_item", "item_id": "jeans", "operator": "equipped"}
DRESS_ON = {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}
SKIRT_ON = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
# Not in gym clothes: one line, by what she has on. Standalone groups, each true only out of both kits and never two at
# once (one bottom slot, one top slot), because an empty branch in a chain renders "No content" (the build refuses it).
_ITEM_ON = lambda i: {"type": "clothing_item", "item_id": i, "operator": "equipped"}


def not_gym(tail, G, T_or_P):
    """The not-in-gym-clothes line, ending on `tail` ("Change in the locker room."), as `T_or_P` blocks."""
    return [
        G(cond(DRESS_ON), T_or_P("Not in a dress. " + tail)),
        G(cond(JEANS), T_or_P("Not in jeans. " + tail)),
        G(cond(*[_ITEM_ON(i) for i in ("short_skirt", "micro_shorts", "split_skirt", "sleep_shorts")], logic="OR"),
          T_or_P("Not in that. " + tail)),
        G(cond({"type": "clothing_slot", "slot": "dress", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "bottom", "operator": "unequipped"}), T_or_P("Not like that. " + tail)),
        *[G(cond(*BOTTOM_OK, _ITEM_ON(i)), T_or_P("Not in that top. " + tail)) for i in ("thin_top", "low_top", "crop_top")],
        G(cond(*BOTTOM_OK, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, _ITEM_OFF("sports_bra")),
          T_or_P("Not like that. " + tail)),
    ]


from canv import G as _G
NOT_GYM_CLOTHES = not_gym("Gym clothes on the floor: the desk guy points you at the locker room before you get near a bench.", _G, P)


def kits(choice):
    """One copy of a workout button per gym kit (GYM_A, GYM_B), each with the kit added to its conditions."""
    import copy
    out_ = []
    for k in GYM_KITS:
        c = copy.deepcopy(choice)
        c.setdefault("conditions", cond())
        c["conditions"]["items"] = list(c["conditions"]["items"]) + list(k)
        out_.append(c)
    return out_
