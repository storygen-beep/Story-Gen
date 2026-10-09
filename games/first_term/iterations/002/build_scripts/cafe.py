"""The café job — the shift (sheets/systems/job.md). Tom's steps, the Friday repeat and Gary's
ten minutes are in tom.py."""
from canv import *
from tomlw import tod, wd

TM = "npc_tom"
out = []
# Clocking out: the uniform off, her own top and jeans back on (iteration 002: sweep A5-02).
CLOCK_OUT = [{"action": "unequip", "item_id": "cafe_uniform_normal"}, {"action": "unequip", "item_id": "cafe_uniform_sexy"}, {"action": "equip", "item_id": "tshirt"}, {"action": "equip", "item_id": "jeans"}]
CLOCK_IN = [{"action": "equip", "item_id": "cafe_uniform_normal"}, {"action": "equip", "item_id": "cafe_uniform_sexy"}]
SEXY_ON = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}
SEXY_OFF = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "unequipped"}
NO_CURFEW = cond(NO_CURFEW_ITEM)
FRI = [wd(4), tod("18:00", "19:00")]   # the Friday evening shift, as it starts (iteration 002: A5-04)

def money(n):
    return {"targetType": "player", "trait": "money", "op": "add", "value": n, "clamp": False}

def shift_choice(label, k, extra=()):
    prev = [flag(f"cafe_shift_{i}_today") for i in range(1, k)]
    return go(label, node="shift", mins=0, costs=[{"trait": "energy", "value": 20}],
              cond_=cond(*prev, flag(f"cafe_shift_{k}_today", False), *extra),
              flags=[fset(f"cafe_shift_{k}_today")], wardrobe=CLOCK_IN)

# the evening shift is shut under the curfew (job sheet: "the evening shift says why")
DAY = tod("08:00", "18:00")
EVE = tod("18:00", "19:00")   # an evening shift starts by 19:00 and is done by the 22:00 close (A5-04)
choices = []
for k in (1, 2, 3):
    choices.append(shift_choice("Work a shift (3 hours, 20 energy).", k, [DAY]))
    choices.append(shift_choice("Work a shift (3 hours, 20 energy).", k, [EVE, NO_CURFEW_ITEM]))

out.append({
    "id": "cafe_shift", "name": "Work a shift",
    "description": "The café shift: 3 hours, 20 energy, $8 plus tips ($4 in the normal uniform, $8 in the tight one at Daring; Friday's close doubles tips). Up to three a day, Monday to Saturday; the evening shift is shut under the curfew.",
    "trigger": {"location": "cafe", "is_repeatable": True, "priority": 4, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "08:00", "end_time": "19:00"}],
                "conditions": cond(flag("cafe_job"), flag("cafe_shift_3_today", False)),
                "metadata": {"show_when_blocked": True, "cooldown_message": "No more shifts today."}},
    "nodes": [
        node("counter", "The counter", [
            D(TM, "Uniform's in the back, @player. Three hours. Smile."),
            G(cond(trait("energy", "lt", 20)), T("You'd drop a tray. Not today.")),
            G(CURFEW_ON, G(cond(EVE), P("Mom's curfew. No evening shifts this week. Tom shrugs like it's your problem, because it is."))),
        ], choices + [go("Not today.", loc="cafe", mins=1)]),
        node("shift", "Three hours", [
            G(cond(tod("11:00", "14:00")), P("The lunch rush hits all at once: twelve coffees, a birthday, a baby that screams through all of it. You carry plates until your arms burn. A man at table two tells you you've got a lovely smile and leaves his number on a napkin under the tip.")),
            G(cond(tod("14:00", "18:00")), P("Slow afternoon. You wipe tables that are clean and refill sugar that's full, and the regulars at the counter watch you bend over to do it. One of them pretends to read his phone the whole time, upside down.")),
            POOL(
                P("A table of guys from the team come in and order nothing but coffee for an hour so they can watch you walk back and forth. Tom lets them. They tip like they're trying to impress each other."),
                P("Two women in gym clothes, a businessman on a call, a pensioner who wants his toast cut into soldiers. Your feet hurt, but you're good at this. You can feel it in the tips."),
                pid="cafe_shift_lines"),
            G(cond(SEXY_ON), P("In the tight uniform with the top button open, every man who orders leans a little further over the counter. Every one of them tips more.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
              P("No bra under the uniform. Every time you lean to pour, somebody stops talking.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                   {"type": "npc_at_location", "location_id": "cafe", "npc_id": "npc_gary", "operator": "is_present"}),
              D(TM, "Booth four's going to tip big today.")),
            G(cond(trait("tom_step", "gte", 1), ntrait(TM, "want", "gte", 30)), P("Tom reties your apron on his way past, both times you go by.")),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)), P("A woman at table three wrinkles her nose when you lean in. Her tip is coins.")),
        ], [
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_OFF, {"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), eff=[money(12)]),
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_OFF, wd(4), tod("08:00", "18:00")), eff=[money(12)]),
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_OFF, *FRI), eff=[money(16)]),
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_ON, {"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), eff=[money(16)]),
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_ON, wd(4), tod("08:00", "18:00")), eff=[money(16)]),
            go("Clock out.", loc="cafe", mins=180, wardrobe=CLOCK_OUT, cond_=cond(SEXY_ON, *FRI), eff=[money(24)]),
        ]),
    ]})

text = "# ── the café shift (sheets/systems/job.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("cafe:", len(out), "canvases")
