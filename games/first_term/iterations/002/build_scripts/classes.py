"""The class timetable, one source of truth (college.md, "The timetable screen"): the class canvases in
college.py and the [[ui.timetable]] rows gen_world.py writes both read these, so the screen can never
disagree with the classes (2026-11-01, DECISIONS 112, 121)."""


def sched(*rows):
    return [{"weekdays": w, "start_time": a, "end_time": b} for w, a, b in rows]


PSYCH = sched(([0, 2, 4], "08:30", "10:00"), ([3], "13:00", "14:30"))
BUSI = sched(([0, 2], "10:15", "11:45"), ([1], "13:00", "14:30"))
BIO = sched(([1, 3], "10:15", "11:45"), ([0], "13:00", "14:30"))
FIG = sched(([1, 3], "08:30", "10:00"), ([2], "13:00", "14:30"))

# (the class, its schedule, the room, the lecturer)
CLASSES = [
    ("Psychology", PSYCH, "lecture_hall", "npc_hale"),
    ("Business", BUSI, "lecture_hall", "npc_business_lecturer"),
    ("Biology", BIO, "lecture_hall", "npc_bio_ta"),
    ("Figure drawing", FIG, "lecture_hall", "npc_art_lecturer"),
]


LATE_MINUTES = 45   # a class can be joined until 45 minutes in, late after 15 (DECISIONS 235; college.py late_copy)


def late_until(start):
    h, m = map(int, start.split(":")); m += LATE_MINUTES
    return f"{h + m // 60:02d}:{m % 60:02d}"


def timetable_rows():
    """One [[ui.timetable]] row per class slot, sorted by day then hour."""
    rows = []
    for name, sch, place, lecturer in CLASSES:
        for r in sch:
            rows.append({"class": name, "place": place, "lecturer": lecturer, "weekdays": r["weekdays"],
                         "from": r["start_time"], "to": r["end_time"], "late_until": late_until(r["start_time"])})
    return sorted(rows, key=lambda r: (min(r["weekdays"]), r["from"]))
